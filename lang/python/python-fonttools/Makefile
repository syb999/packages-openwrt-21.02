#
# This is free software, licensed under the GNU General Public License v2.
# See /LICENSE for more information.
#

include $(TOPDIR)/rules.mk

PKG_NAME:=python-fonttools
PKG_VERSION:=4.51.0
PKG_RELEASE:=1

PYPI_NAME:=fonttools
PKG_HASH:=dc0673361331566d7a663d7ce0f6fdcbfbdc1f59c6e3ed1165ad7202ca183c68

PKG_MAINTAINER:=syb999
PKG_LICENSE:=MIT
PKG_LICENSE_FILES:=LICENSE

include ../pypi.mk
include $(INCLUDE_DIR)/package.mk
include ../python3-package.mk

# Keep it pure Python: the optional Cython accelerators are only built when
# asked for explicitly, and this tree ships no matching Cython pin for them.
PYTHON3_PKG_SETUP_VARS:=FONTTOOLS_WITH_CYTHON=0

define Package/python3-fonttools
  SUBMENU:=Python
  SECTION:=lang
  CATEGORY:=Languages
  TITLE:=Tools to manipulate font files
  URL:=https://github.com/fonttools/fonttools
  DEPENDS:=+python3-light
endef

define Package/python3-fonttools/description
  fontTools is a library for manipulating fonts, written in Python.
endef

$(eval $(call Py3Package,python3-fonttools))
$(eval $(call Py3Package,python3-fonttools-src))

$(eval $(call BuildPackage,python3-fonttools))
$(eval $(call BuildPackage,python3-fonttools-src))
