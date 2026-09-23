#
# Copyright (C) 2026 OpenWrt.org
#
# This is free software, licensed under the GNU General Public License v2.
# See /LICENSE for more information.
#

include $(TOPDIR)/rules.mk

PKG_NAME:=pandas
PKG_VERSION:=2.0.1
PKG_RELEASE:=1

PYPI_NAME:=$(PKG_NAME)
PKG_HASH:=19b8e5270da32b41ebf12f0e7165efa7024492e9513fb46fb631c5022ae5709d

PKG_MAINTAINER:=OpenWrt.org

PKG_LICENSE:=BSD-3-Clause
PKG_LICENSE_FILES:=LICENSE
PKG_CPE_ID:=cpe:/a:pandas:pandas

# Setup.py of pandas:
#  - imports numpy and uses numpy.get_include() to build the C extensions, so a
#    numpy matching the target (python3-numpy) must be importable by the host
#    Python that runs setup.py;
#  - the sdist ships no Cython generated C sources, and setup.py aborts unless
#    Cython >= 0.29.33 is present. The Cython pin in ../host-pip-requirements/
#    is shared with numpy and satisfies both (numpy >= 0.29.24, pandas >= 0.29.33).
#
# Both are host build dependencies (pip, pinned in ../host-pip-requirements/).
#
# pandas 2.x moved its name/version/dependencies to the [project] table of
# pyproject.toml (read by setuptools >= 61 only) and gets versioneer from its
# build requirements; 002-setup-build-without-versioneer.patch makes setup.py
# work with the setuptools 58.1.0 that this tree uses.
#
# Runtime dependencies: numpy (declared >= 1.20.3, the feed has 1.21.5),
# python-dateutil (declared >= 2.8.2, the feed has 2.8.1 - works in practice),
# pytz, and the IANA timezone data (declared as the tzdata package, but pandas
# only needs it through zoneinfo, i.e. the system /usr/share/zoneinfo is enough).
HOST_PYTHON3_PACKAGE_BUILD_DEPENDS:=numpy Cython

# Build against the numpy package of this feed (PKG_BUILD_DEPENDS uses the
# source package name, the ipk dependency below uses the package name).
PKG_BUILD_DEPENDS:=numpy

# files.pythonhosted.org is unreachable behind the CN firewall, so the host
# build dependencies are fetched from a PyPI mirror. Set PYPI_HOST_INDEX_URL=
# to fall back to the default index.
PYPI_HOST_INDEX_URL?=https://mirrors.aliyun.com/pypi/simple

include ../pypi.mk
include $(INCLUDE_DIR)/package.mk
include ../python3-package.mk

PYTHON3_PKG_HOST_PIP_INSTALL_ARGS+=$(if $(PYPI_HOST_INDEX_URL),--index-url $(PYPI_HOST_INDEX_URL))

# Do NOT let setuptools compile in parallel here: several extensions share the
# same C source (e.g. pandas/_libs/tslibs/src/datetime/np_datetime.c) and thus
# the same object file, and setuptools' parallel build compiles it from several
# jobs at once into that one path. When an extension is linked while that object
# is being rewritten, ld (-shared tolerates unresolved symbols) silently emits
# an extension without the symbols of the shared source, which shows up only as
# an ImportError on the target, e.g.
#   pandas/_libs/tslibs/timedeltas.so: pandas_timedelta_to_timedeltastruct:
#   symbol not found
# The result is checked below, so a broken link cannot get into the package.
PYTHON3_PKG_SETUP_GLOBAL_ARGS:=

define Build/Compile
	$(call Py3Build/Compile/Default)
	$(SHELL) ./files/check-pandas-install.sh "$(TARGET_NM)" "$(PKG_INSTALL_DIR)/$(PYTHON3_PKG_DIR)/pandas"
endef

# 001-setup-use-target-byteorder.patch uses this to pick the endianness of the
# target instead of the one of the build host.
PYTHON3_PKG_SETUP_VARS:=PANDAS_TARGET_BYTEORDER=$(if $(CONFIG_BIG_ENDIAN),big,little)

define Package/python3-pandas
  SUBMENU:=Python
  SECTION:=lang
  CATEGORY:=Languages
  TITLE:=Powerful data structures for data analysis, time series, and statistics
  URL:=https://pandas.pydata.org/
  DEPENDS:=+python3 +python3-numpy +python3-dateutil +python3-pytz +libstdcpp
endef

define Package/python3-pandas/description
pandas is a Python package providing fast, flexible, and expressive data
structures designed to make working with "relational" or "labeled" data both
easy and intuitive. It aims to be the fundamental high-level building block
for doing practical, real world data analysis in Python.

This package is built against the numpy package of this feed.
endef

$(eval $(call Py3Package,python3-pandas))
$(eval $(call Py3Package,python3-pandas-src))

$(eval $(call BuildPackage,python3-pandas))
$(eval $(call BuildPackage,python3-pandas-src))
