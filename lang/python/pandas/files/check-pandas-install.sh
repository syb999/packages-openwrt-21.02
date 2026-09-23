#!/bin/sh
#
# Sanity check the pandas installation in the build tree before it is packed.
#
# 1) The pure Python part must be present. For py3 packages the metadata of
#    setup.py decides what gets installed: as soon as the name/version/packages
#    are not visible to the setuptools that runs the build (pandas 2.x has them
#    in the [project] table of pyproject.toml, which setuptools < 61 ignores),
#    the build still succeeds but the package contains the extension modules
#    only, which fails at import time on the target.
#
# 2) No extension module may refer to a pandas_* symbol that no extension
#    provides. Linking a shared object tolerates unresolved symbols, so a
#    broken build (or a broken parallel build, see the Makefile) produces an
#    extension module that only fails at import time on the target, with e.g.
#      pandas/_libs/tslibs/timedeltas.so: pandas_timedelta_to_timedeltastruct:
#      symbol not found
#
# Usage: check-pandas-install.sh <target-nm> <site-packages/pandas dir>
#
# Call it on $(PKG_INSTALL_DIR), i.e. before the .pyc conversion and before the
# strip step; the .so inside an .ipk cannot be read by nm anymore.

NM="$1"
DIR="$2"

if [ -z "$NM" ] || [ ! -d "$DIR" ]; then
	echo "ERROR: usage: $0 <target-nm> <site-packages/pandas dir>"
	exit 2
fi

failed=0

for f in __init__.py core/frame.py _libs/__init__.py; do
	if [ ! -f "$DIR/$f" ]; then
		echo "ERROR: $DIR/$f is missing, the pure Python part was not installed"
		failed=1
	fi
done

for so in $(find "$DIR" -name '*.so'); do
	defined=$("$NM" -D --defined-only "$so" 2>/dev/null | wc -l)
	if [ "$defined" -lt 2 ]; then
		echo "ERROR: $so: cannot read the symbol table of this extension module"
		failed=1
		continue
	fi
	sym=$("$NM" -D --undefined-only "$so" 2>/dev/null | awk '{print $2}' | grep '^pandas_')
	if [ -n "$sym" ]; then
		echo "ERROR: $so refers to shared pandas C symbols that are not linked in:"
		echo "$sym"
		failed=1
	fi
done

if [ "$failed" != 0 ]; then
	echo "ERROR: the pandas installation is incomplete or broken, do not use this package"
	exit 1
fi

echo "OK: pandas installation is complete and all extension modules link their shared C sources"
