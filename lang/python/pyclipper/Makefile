#
# Copyright (C) 2026 OpenWrt.org
#
# This is free software, licensed under the GNU General Public License v2.
# See /LICENSE for more information.
#

include $(TOPDIR)/rules.mk

PKG_NAME:=pyclipper
PKG_VERSION:=1.3.0.post6
PKG_RELEASE:=1

PYPI_NAME:=$(PKG_NAME)
PKG_SOURCE:=$(PYPI_NAME)-$(PKG_VERSION).tar.gz
PKG_SOURCE_URL:= \
	https://mirrors.aliyun.com/pypi/packages/4a/b2/550fe500e49c464d73fabcb8cb04d47e4885d6ca4cfc1f5b0a125a95b19a/ \
	https://files.pythonhosted.org/packages/4a/b2/550fe500e49c464d73fabcb8cb04d47e4885d6ca4cfc1f5b0a125a95b19a/
PKG_HASH:=42bff0102fa7a7f2abdd795a2594654d62b786d0c6cd67b72d469114fdeb608c

PKG_MAINTAINER:=OpenWrt.org

PKG_LICENSE:=MIT
PKG_LICENSE_FILES:=LICENSE

# The sdist ships the cython generated C++ (distribution mode), so no Cython is
# needed; setup.py only wants setuptools_scm for the version it writes into
# src/pyclipper/_version.py.
HOST_PYTHON3_PACKAGE_BUILD_DEPENDS:=setuptools-scm

include ../pypi.mk
include $(INCLUDE_DIR)/package.mk
include ../python3-package.mk

# there is no git checkout to derive the version from
PYTHON3_PKG_SETUP_VARS:=SETUPTOOLS_SCM_PRETEND_VERSION=$(PKG_VERSION)

define Package/python3-pyclipper
  SUBMENU:=Python
  SECTION:=lang
  CATEGORY:=Languages
  TITLE:=Cython wrapper for the C++ Clipper library (polygon clipping)
  URL:=https://github.com/fonttools/pyclipper
  DEPENDS:=+python3 +libstdcpp
endef

define Package/python3-pyclipper/description
 pyclipper is a Cython wrapper for the C++ translation of the Angus Johnson's
 Clipper library (ver 6.4.2), used by text detectors such as RapidOCR to expand
 the detected text polygons (DB postprocessing).
endef

$(eval $(call Py3Package,python3-pyclipper))
$(eval $(call Py3Package,python3-pyclipper-src))

$(eval $(call BuildPackage,python3-pyclipper))
$(eval $(call BuildPackage,python3-pyclipper-src))
