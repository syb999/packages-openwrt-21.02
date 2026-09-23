#!/bin/sh
#
# Verify that the OpenCV build really produced the python bindings (cv2) for the
# target architecture.
#
# The failure this guards against: when CMake does not find the Python
# interpreter or the numpy headers it silently builds without the python3
# module. The build succeeds, the package is simply empty, and it only shows up
# as "ModuleNotFoundError: No module named 'cv2'" on the target. The second trap
# is building the module against the host python (x86-64) instead of the target.
#
# Usage: check-opencv-install.sh <target-readelf> <site-packages> <lib dir> [required lib substring]
#
# Call it after "ninja install", i.e. on $(PKG_INSTALL_DIR); after the strip
# step of the ipk build the .so cannot be read with readelf anymore.

READELF="$1"
SITE="$2"
LIBDIR="$3"
REQUIRED_LIB="$4"

if [ -z "$READELF" ] || [ ! -d "$SITE" ]; then
	echo "ERROR: usage: $0 <target-readelf> <site-packages> <lib dir>"
	exit 2
fi

failed=0

# 1) the module and its loader package must be there at all
modules=$(find "$SITE" -maxdepth 2 -name 'cv2*' 2>/dev/null)
if [ -z "$modules" ]; then
	echo "ERROR: no cv2 module in $SITE - OpenCV was built without python3 bindings"
	exit 1
fi
if [ ! -f "$SITE/cv2/__init__.py" ]; then
	echo "ERROR: $SITE/cv2/__init__.py (the loader) is missing"
	failed=1
fi

# 2) the extension module must be built for the target and must be a real
#    CPython extension. Note that a python extension on Linux does not link
#    against libpython: its Py* symbols are undefined by design and get resolved
#    from the interpreter when the module is imported.
for so in $(find "$SITE" -name 'cv2*.so'); do
	if ! "$READELF" -h "$so" >/dev/null 2>&1; then
		echo "ERROR: $so is not a readable ELF object"
		failed=1
		continue
	fi
	if "$READELF" -h "$so" 2>/dev/null | grep -q 'X86-64'; then
		echo "ERROR: $so was built for the build host (x86-64), not for the target"
		failed=1
	fi
	if ! "$READELF" --dyn-syms "$so" 2>/dev/null | grep -q 'PyInit_'; then
		echo "ERROR: $so does not look like a CPython extension module (no PyInit_*)"
		failed=1
	fi
	if [ "$("$READELF" --dyn-syms "$so" 2>/dev/null | grep -c ' UND .*Py')" = 0 ]; then
		echo "ERROR: $so does not use the Python C API at all"
		failed=1
	fi
	if ! "$READELF" -d "$so" 2>/dev/null | grep -q 'libopencv_'; then
		echo "ERROR: $so does not link against libopencv_*"
		failed=1
	fi
done

# 3) the opencv libraries themselves. The optional backend (e.g. libavcodec for
#    the ffmpeg videoio backend) is linked by one of these libraries, not by the
#    python module, which only links libopencv_*.
if [ -n "$LIBDIR" ]; then
	if [ -z "$(find "$LIBDIR" -maxdepth 1 -name 'libopencv_core.so*' 2>/dev/null)" ]; then
		echo "ERROR: libopencv_core.so* is missing in $LIBDIR"
		failed=1
	fi
	if [ -n "$REQUIRED_LIB" ]; then
		found=0
		for lib in $(find "$LIBDIR" -maxdepth 1 -name 'libopencv_*.so*' 2>/dev/null); do
			if "$READELF" -d "$lib" 2>/dev/null | grep -q "$REQUIRED_LIB"; then
				found=1
				break
			fi
		done
		if [ "$found" = 0 ]; then
			echo "ERROR: no libopencv_* library links against $REQUIRED_LIB (backend missing?)"
			failed=1
		fi
	fi
fi

if [ "$failed" != 0 ]; then
	echo "ERROR: the OpenCV installation is incomplete or broken, do not use this package"
	exit 1
fi

echo "OK: cv2 is present and built for the target"
