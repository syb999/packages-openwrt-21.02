#
# This is free software, licensed under the GNU General Public License v2.
# See /LICENSE for more information.
#

include $(TOPDIR)/rules.mk

PKG_NAME:=python-sympy
PKG_VERSION:=1.13.3
PKG_RELEASE:=1

PYPI_NAME:=sympy
PKG_HASH:=b27fd2c6530e0ab39e275fc9b683895367e51d5da91baa8d3d64db2565fec4d9

PKG_MAINTAINER:=syb999
PKG_LICENSE:=BSD-3-Clause
PKG_LICENSE_FILES:=LICENSE

include ../pypi.mk
include $(INCLUDE_DIR)/package.mk
include ../python3-package.mk

define Package/python3-sympy
  SUBMENU:=Python
  SECTION:=lang
  CATEGORY:=Languages
  TITLE:=Computer algebra system for symbolic mathematics
  URL:=https://sympy.org/
  DEPENDS:=+python3-light +python3-mpmath
endef

define Package/python3-sympy/description
  SymPy is a pure Python library for symbolic mathematics. It aims to become
  a full-featured computer algebra system while keeping the code as simple as
  possible. mpmath is required at runtime.
endef

$(eval $(call Py3Package,python3-sympy))
$(eval $(call Py3Package,python3-sympy-src))

$(eval $(call BuildPackage,python3-sympy))
$(eval $(call BuildPackage,python3-sympy-src))
