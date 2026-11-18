#
# This is free software, licensed under the GNU General Public License v2.
# See /LICENSE for more information.
#

include $(TOPDIR)/rules.mk

PKG_NAME:=python-mpmath
PKG_VERSION:=1.3.0
PKG_RELEASE:=1

PYPI_NAME:=mpmath
PKG_HASH:=7a28eb2a9774d00c7bc92411c19a89209d5da7c4c9a9e227be8330a23a25b91f

PKG_MAINTAINER:=syb999
PKG_LICENSE:=BSD-3-Clause
PKG_LICENSE_FILES:=LICENSE

include ../pypi.mk
include $(INCLUDE_DIR)/package.mk
include ../python3-package.mk

define Package/python3-mpmath
  SUBMENU:=Python
  SECTION:=lang
  CATEGORY:=Languages
  TITLE:=Arbitrary-precision floating-point arithmetic
  URL:=https://mpmath.org/
  DEPENDS:=+python3-light
endef

define Package/python3-mpmath/description
  Pure Python library for real and complex floating-point arithmetic with
  arbitrary precision. Runtime dependency of sympy.
endef

$(eval $(call Py3Package,python3-mpmath))
$(eval $(call Py3Package,python3-mpmath-src))

$(eval $(call BuildPackage,python3-mpmath))
$(eval $(call BuildPackage,python3-mpmath-src))
