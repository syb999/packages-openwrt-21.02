"""A small, CPU-only implementation of the onnxruntime Python API on top of
OpenCV's dnn module.

Why this exists: the upstream onnxruntime package is a large C++ library that is
published as prebuilt manylinux (glibc) wheels only - there is no source
distribution and no musl/aarch64 build that could be used on OpenWrt. OpenCV
itself can run ONNX models (cv2.dnn) and is already available as python3-opencv
on OpenWrt, so this module implements the subset of the onnxruntime API that
model loading/inference code (e.g. RapidOCR) uses:

    from onnxruntime import InferenceSession, SessionOptions, \
        GraphOptimizationLevel, get_available_providers, get_device

    session = InferenceSession(path, sess_options=opts, providers=[...])
    session.run(output_names, {input_name: ndarray})
    session.get_inputs() / get_outputs()          -> objects with a .name
    session.get_modelmeta().custom_metadata_map   -> parsed from the ONNX file
    session.get_providers()

Limitations: CPU only, one execution provider, no graph optimizations beyond
what cv2.dnn does, and only the operators cv2.dnn implements. Shapes are not
validated (cv2.dnn raises instead). Not a replacement for the real onnxruntime
if your models need operators or providers that cv2.dnn does not have.

The ONNX metadata (custom_metadata_map) is read with a tiny protobuf scanner
instead of the onnx/protobuf packages, which are not available here either.
"""

import os
import tempfile
from enum import Enum, IntEnum

import cv2
import numpy as np

__version__ = "0.1.0"

__all__ = [
    "InferenceSession",
    "SessionOptions",
    "GraphOptimizationLevel",
    "ExecutionMode",
    "get_available_providers",
    "get_device",
    "set_default_logger_severity",
    "ONNXRuntimeError",
]


class GraphOptimizationLevel(IntEnum):
    ORT_DISABLE_ALL = 0
    ORT_ENABLE_BASIC = 1
    ORT_ENABLE_EXTENDED = 2
    ORT_ENABLE_ALL = 99


class ExecutionMode(IntEnum):
    ORT_SEQUENTIAL = 0
    ORT_PARALLEL = 1


class ONNXRuntimeError(RuntimeError):
    pass


class SessionOptions:
    """Accepts the attributes that callers set; the ones that map to OpenCV
    (thread count) are applied when the session is created."""

    def __init__(self, *args, **kwargs):
        self.log_severity_level = 2
        self.log_verbosity_level = 0
        self.enable_cpu_mem_arena = True
        self.enable_mem_pattern = True
        self.enable_profiling = False
        self.graph_optimization_level = GraphOptimizationLevel.ORT_ENABLE_ALL
        self.execution_mode = ExecutionMode.ORT_SEQUENTIAL
        self.intra_op_num_threads = 0
        self.inter_op_num_threads = 0
        self.provider_options = {}
        for k, v in kwargs.items():
            setattr(self, k, v)


def get_available_providers():
    return ["CPUExecutionProvider"]


def get_device():
    return "CPU"


def set_default_logger_severity(severity):
    return None


def _read_varint(data, pos):
    result = 0
    shift = 0
    while True:
        if pos >= len(data):
            raise ValueError("truncated varint")
        b = data[pos]
        pos += 1
        result |= (b & 0x7F) << shift
        if not b & 0x80:
            return result, pos
        shift += 7
        if shift > 63:
            raise ValueError("varint too long")


def _iter_fields(data):
    """Yield (field_number, wire_type, value) of a serialized protobuf message."""
    pos = 0
    end = len(data)
    while pos < end:
        key, pos = _read_varint(data, pos)
        field, wire = key >> 3, key & 0x07
        if wire == 0:
            value, pos = _read_varint(data, pos)
        elif wire == 1:
            value = data[pos:pos + 8]
            pos += 8
        elif wire == 2:
            length, pos = _read_varint(data, pos)
            value = data[pos:pos + length]
            pos += length
        elif wire == 5:
            value = data[pos:pos + 4]
            pos += 4
        else:
            raise ValueError("unsupported protobuf wire type %d" % wire)
        yield field, wire, value


def _parse_onnx_header(data):
    """Return (metadata_props, input_names, input_dims, graph_outputs, opset).

    Only the few top level fields we need are decoded:
      ModelProto.graph = 7, ModelProto.metadata_props = 14, ModelProto.opset_import = 8
      GraphProto.input = 11, GraphProto.output = 12, ValueInfoProto.name = 1,
      ValueInfoProto.type = 2 (tensor_type = 1, shape = 2, dim = 1),
      StringStringEntryProto.key = 1 / value = 2, OperatorSetIdProto.version = 2

    input_dims is a list of lists with one entry per input dimension: the fixed
    dim_value as int, or None when the dimension is symbolic/unknown.
    graph_outputs is a list of (name, rank) tuples.
    """
    metadata = {}
    graph_inputs = []
    input_dims = []
    graph_outputs = []
    opset = None

    def value_info(content):
        name = None
        dims = []
        for f, w, v in _iter_fields(content):
            if f == 1 and w == 2:
                name = v.decode("utf-8", "replace")
            elif f == 2 and w == 2:                       # TypeProto
                for f2, w2, v2 in _iter_fields(v):
                    if f2 == 1 and w2 == 2:               # tensor_type
                        for f3, w3, v3 in _iter_fields(v2):
                            if f3 == 2 and w3 == 2:       # shape
                                for f4, w4, v4 in _iter_fields(v3):
                                    if f4 != 1 or w4 != 2:
                                        continue
                                    value = None
                                    for f5, w5, v5 in _iter_fields(v4):
                                        if f5 == 1 and w5 == 0:      # dim_value
                                            value = v5[0] if isinstance(v5, bytes) else v5
                                    dims.append(value)
        return name, dims

    for field, wire, value in _iter_fields(data):
        if field == 14 and wire == 2:
            key = val = None
            for f2, w2, v2 in _iter_fields(value):
                if f2 == 1 and w2 == 2:
                    key = v2.decode("utf-8", "replace")
                elif f2 == 2 and w2 == 2:
                    val = v2.decode("utf-8", "replace")
            if key is not None:
                metadata[key] = val
        elif field == 7 and wire == 2:
            for f2, w2, v2 in _iter_fields(value):
                if f2 == 11 and w2 == 2:
                    name, dims = value_info(v2)
                    if name is not None:
                        graph_inputs.append(name)
                        input_dims.append(dims)
                elif f2 == 12 and w2 == 2:
                    name, dims = value_info(v2)
                    graph_outputs.append((name, len(dims) or None))
        elif field == 8 and wire == 2:
            for f2, w2, v2 in _iter_fields(value):
                if f2 == 2 and w2 == 0:
                    opset = v2
    return metadata, graph_inputs, input_dims, graph_outputs, opset


class _NodeArg:
    """Stand-in for onnxruntime.NodeArg (name/shape/type)."""

    def __init__(self, name, shape=None, type_str="tensor(float)"):
        self.name = name
        self.shape = shape
        self.type = type_str

    def __repr__(self):
        return "NodeArg(name=%r, shape=%r, type=%r)" % (self.name, self.shape, self.type)


class _ModelMetadata:
    def __init__(self, metadata_map, producer_name="", graph_name=""):
        self.custom_metadata_map = metadata_map
        self.producer_name = producer_name
        self.graph_name = graph_name

    def __repr__(self):
        return "_ModelMetadata(custom_metadata_map=%r)" % (self.custom_metadata_map,)


class InferenceSession:
    def __init__(self, path_or_bytes, sess_options=None, providers=None,
                 provider_options=None, **kwargs):
        self._sess_options = sess_options
        self._providers = self._normalize_providers(providers)

        raw = None
        path = None
        if isinstance(path_or_bytes, (bytes, bytearray, np.ndarray)):
            raw = np.frombuffer(bytes(path_or_bytes), dtype=np.uint8).copy()
        else:
            path = os.fspath(path_or_bytes)
            if not os.path.isfile(path):
                raise ONNXRuntimeError("model file not found: %s" % path)
            with open(path, "rb") as fp:
                raw = np.frombuffer(fp.read(), dtype=np.uint8).copy()

        if raw is None or raw.size == 0:
            raise ONNXRuntimeError("empty model")

        self._tmp_path = None
        self._net = self._make_net(raw, path)

        if path is not None:
            with open(path, "rb") as fp:
                (self._metadata, graph_inputs, graph_input_dims, graph_outputs,
                 self._opset) = _parse_onnx_header(fp.read())
        else:
            (self._metadata, graph_inputs, graph_input_dims, graph_outputs,
             self._opset) = _parse_onnx_header(raw.tobytes())

        self._graph_inputs = graph_inputs
        self._input_names = self._resolve_input_names(graph_inputs)
        self._input_dims = self._resolve_input_dims(graph_inputs, graph_input_dims)
        self._output_names = [str(n) for n in self._net.getUnconnectedOutLayersNames()]
        self._output_ranks = self._resolve_output_ranks(graph_outputs)
        # a model exported with a fixed batch size can only be run one batch at a
        # time, see run()
        self._fixed_batch = self._input_dims[0] if self._input_dims else None

        if sess_options is not None:
            threads = getattr(sess_options, "intra_op_num_threads", 0)
            if isinstance(threads, int) and threads > 0:
                cv2.setNumThreads(threads)

    @staticmethod
    def _normalize_providers(providers):
        result = []
        for p in providers or ["CPUExecutionProvider"]:
            result.append(p[0] if isinstance(p, (tuple, list)) else p)
        if "CPUExecutionProvider" not in result:
            result.append("CPUExecutionProvider")
        return result

    def _make_net(self, raw, path):
        last_error = None
        for candidate in (path, raw):
            if candidate is None:
                continue
            try:
                return cv2.dnn.readNetFromONNX(candidate)
            except Exception as exc:      # cv2.error and friends
                last_error = exc
        # last resort: cv2 wants a real file
        fd, tmp = tempfile.mkstemp(suffix=".onnx")
        try:
            with os.fdopen(fd, "wb") as fp:
                fp.write(raw.tobytes())
            self._tmp_path = tmp
            return cv2.dnn.readNetFromONNX(tmp)
        except Exception:
            raise ONNXRuntimeError("cv2.dnn cannot load this ONNX model: %s" % last_error)

    def _resolve_input_names(self, graph_inputs):
        """Prefer the names cv2.dnn knows (they come from the ONNX graph), fall
        back to the ONNX graph inputs and finally to any layer name."""
        layers = [str(n) for n in self._net.getLayerNames()]
        known = [name for name in graph_inputs if name in layers]
        if known:
            return known
        if graph_inputs:
            return graph_inputs
        return layers[:1]

    def _resolve_output_ranks(self, graph_outputs):
        """Rank (number of dimensions) declared for each graph output, aligned
        with the output layer names cv2.dnn reports."""
        by_name = {name: rank for name, rank in graph_outputs if name is not None}
        ranks = []
        for name in self._output_names:
            if name in by_name:
                ranks.append(by_name[name])
            else:
                ranks.append(None)
        if all(r is None for r in ranks) and len(graph_outputs) == len(ranks):
            ranks = [rank for _, rank in graph_outputs]
        return ranks

    @staticmethod
    def _normalize_output(array, rank):
        """cv2.dnn sometimes keeps an extra singleton dimension (e.g. (N, 1, 2)
        for an output declared as (N, 2)), which confuses code that indexes the
        result the way onnxruntime's does. Drop singleton dimensions until the
        rank matches the declared one, never touching the batch dimension."""
        while rank is not None and array.ndim > rank:
            for axis in range(array.ndim - 1, 0, -1):
                if array.shape[axis] == 1:
                    array = np.squeeze(array, axis=axis)
                    break
            else:
                break
        return array

    def _resolve_input_dims(self, graph_inputs, input_dims):
        """Declared dimensions of the input cv2.dnn will be fed (by name, else
        the first one). Entries are ints for fixed dimensions and None for
        symbolic ones."""
        for name, dims in zip(graph_inputs, input_dims):
            if self._input_names and name == self._input_names[0]:
                return dims
        return input_dims[0] if input_dims else []

    # -- onnxruntime API -------------------------------------------------
    def run(self, output_names, input_feed, run_options=None):
        if not input_feed:
            raise ONNXRuntimeError("input_feed is empty")
        feeds = [np.ascontiguousarray(v) for v in input_feed.values()]
        names = list(output_names) if output_names else list(self._output_names)
        if not names:
            raise ONNXRuntimeError("model has no output layers")

        if len(feeds) == 1:
            blob = feeds[0]
            batch = int(blob.shape[0]) if blob.ndim else 1
            step = self._fixed_batch
            if step and batch > step and batch % step == 0:
                # the model was exported with a fixed batch size and cv2.dnn
                # cannot run it with more than that, so the chunks are run one
                # after another and the outputs are stitched together
                chunks = []
                for start in range(0, batch, step):
                    self._net.setInput(np.ascontiguousarray(blob[start:start + step]))
                    chunks.append(self._forward(names))
                return [np.concatenate([chunk[i] for chunk in chunks], axis=0)
                        for i in range(len(chunks[0]))]
            self._net.setInput(blob)
        else:
            for name, blob in zip(self._input_names, feeds):
                self._net.setInput(blob, name)
        return self._forward(names)

    def _forward(self, names):
        outs = self._net.forward(names) if len(names) > 1 else [self._net.forward(names[0])]
        if not isinstance(outs, (list, tuple)):
            outs = [outs]
        result = []
        for index, out in enumerate(outs):
            array = np.asarray(out)
            if index < len(self._output_ranks):
                array = self._normalize_output(array, self._output_ranks[index])
            result.append(array)
        return result

    def get_inputs(self):
        return [_NodeArg(n) for n in self._input_names]

    def get_outputs(self):
        return [_NodeArg(n) for n in self._output_names]

    def get_providers(self):
        return list(self._providers)

    def set_providers(self, providers, provider_options=None):
        self._providers = self._normalize_providers(providers)

    def get_modelmeta(self):
        return _ModelMetadata(dict(self._metadata))

    def get_session_options(self):
        return self._sess_options

    def end_profiling(self):
        return ""

    def __del__(self):
        tmp = getattr(self, "_tmp_path", None)
        if tmp:
            try:
                os.unlink(tmp)
            except OSError:
                pass
