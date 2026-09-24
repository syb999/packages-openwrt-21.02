#!/usr/bin/env python3
"""Rewrite the input shape of an ONNX model to a fixed value.

Why: RapidOCR's recognizer is exported with a dynamic input shape, and the reshape
targets inside the graph are computed at runtime from Shape/Slice/Concat chains.
OpenCV's dnn module cannot resolve those when the input shape is unknown
("computeShapeByReshapeMask: srcTotal == dstTotal" at load/forward time). With a
fixed input shape the whole shape arithmetic is known at load time and cv2.dnn
runs the model - verified to produce the same output as onnxruntime
(max abs difference 1.5e-06 on the same input).

Only the graph input's shape is touched, the rest of the file is copied
verbatim, so no onnx/protobuf runtime is needed on the build host:

    make_onnx_input_fixed.py <in.onnx> <out.onnx> <input-name> d1,d2,...
"""

import sys


def read_varint(data, pos):
    value = 0
    shift = 0
    while True:
        byte = data[pos]
        pos += 1
        value |= (byte & 0x7F) << shift
        if not byte & 0x80:
            return value, pos
        shift += 7
        if shift > 70:
            raise ValueError("varint too long")


def encode_varint(value):
    out = bytearray()
    while True:
        byte = value & 0x7F
        value >>= 7
        if value:
            out.append(byte | 0x80)
        else:
            out.append(byte)
            return bytes(out)


def iter_fields(data):
    """Yield (field_number, wire_type, content) of a protobuf message.

    For length delimited fields the content is the payload without the length
    prefix, so everything can be re-encoded with encode_field().
    """
    pos = 0
    end = len(data)
    while pos < end:
        key, pos = read_varint(data, pos)
        field, wire = key >> 3, key & 7
        start = pos
        if wire == 0:
            value, pos = read_varint(data, pos)
            content = data[start:pos]
        elif wire == 1:
            content = data[pos:pos + 8]
            pos += 8
        elif wire == 2:
            length, pos = read_varint(data, pos)
            content = data[pos:pos + length]
            pos += length
        elif wire == 5:
            content = data[pos:pos + 4]
            pos += 4
        else:
            raise ValueError("unsupported protobuf wire type %d" % wire)
        yield field, wire, content


def encode_field(field, wire, content):
    tag = encode_varint((field << 3) | wire)
    if wire == 2:
        return tag + encode_varint(len(content)) + content
    return tag + content


def encode_shape(dims):
    body = b"".join(encode_field(1, 2, encode_field(1, 0, encode_varint(d)))
                    for d in dims)
    return body


def fix_tensor_shape(tensor_type, dims):
    """Return a rebuilt TensorProto (field 1 of TypeProto) with fixed dims."""
    out = []
    for field, wire, content in iter_fields(tensor_type):
        if field == 2 and wire == 2:            # shape
            out.append(encode_field(2, 2, encode_shape(dims)))
        else:
            out.append(encode_field(field, wire, content))
    return b"".join(out)


def fix_type(type_proto, dims):
    out = []
    for field, wire, content in iter_fields(type_proto):
        if field == 1 and wire == 2:            # tensor_type
            out.append(encode_field(1, 2, fix_tensor_shape(content, dims)))
        else:
            out.append(encode_field(field, wire, content))
    return b"".join(out)


def fix_value_info(value_info, dims):
    out = []
    for field, wire, content in iter_fields(value_info):
        if field == 2 and wire == 2:            # type
            out.append(encode_field(2, 2, fix_type(content, dims)))
        else:
            out.append(encode_field(field, wire, content))
    return b"".join(out)


def value_info_name(value_info):
    for field, wire, content in iter_fields(value_info):
        if field == 1 and wire == 2:
            return content.decode("utf-8", "replace")
    return None


def fix_graph(graph, input_name, dims):
    out = []
    fixed = False
    for field, wire, content in iter_fields(graph):
        if field == 11 and wire == 2 and not fixed:      # graph.input
            if value_info_name(content) == input_name:
                out.append(encode_field(11, 2, fix_value_info(content, dims)))
                fixed = True
                continue
        out.append(encode_field(field, wire, content))
    if not fixed:
        raise SystemExit("ERROR: no graph input named %r in the model" % input_name)
    return b"".join(out)


def fix_model(model, input_name, dims):
    out = []
    fixed = False
    for field, wire, content in iter_fields(model):
        if field == 7 and wire == 2 and not fixed:       # ModelProto.graph
            out.append(encode_field(7, 2, fix_graph(content, input_name, dims)))
            fixed = True
            continue
        out.append(encode_field(field, wire, content))
    if not fixed:
        raise SystemExit("ERROR: the model has no graph")
    return b"".join(out)


def main():
    if len(sys.argv) != 5:
        raise SystemExit("usage: %s <in.onnx> <out.onnx> <input-name> d1,d2,..."
                         % sys.argv[0])
    in_path, out_path, input_name, dims_arg = sys.argv[1:]
    dims = [int(d) for d in dims_arg.split(",")]

    with open(in_path, "rb") as fp:
        model = fp.read()
    result = fix_model(model, input_name, dims)
    with open(out_path, "wb") as fp:
        fp.write(result)
    print("%s: input %r set to %s (%d -> %d bytes)"
          % (out_path, input_name, dims, len(model), len(result)))


if __name__ == "__main__":
    main()
