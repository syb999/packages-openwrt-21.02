#
# This is free software, licensed under the GNU General Public License v2.
# See /LICENSE for more information.
#
# 为 selenium 4.9.0 移植 (OpenWrt 21.02.5 / python3.9)。trio 依赖链
#

include $(TOPDIR)/rules.mk

PKG_NAME:=python-outcome
PKG_VERSION:=1.3.0
PKG_RELEASE:=1

PYPI_NAME:=outcome
PKG_HASH:=588ef4dc10b64e8df160d8d1310c44e1927129a66d6d2ef86845cef512c5f24c

PKG_MAINTAINER:=syb999
PKG_LICENSE:=MIT
PKG_LICENSE_FILES:=LICENSE

include ../pypi.mk
include $(INCLUDE_DIR)/package.mk
include ../python3-package.mk

define Package/python3-outcome
  SUBMENU:=Python
  SECTION:=lang
  CATEGORY:=Languages
  TITLE:=Capture the outcome of Python function calls
  URL:=https://github.com/python-trio/outcome
  DEPENDS:=+python3-light +python3-attrs
endef

define Package/python3-outcome/description
  Capture the outcome of a function call (return value or exception) as a value.
  trio 运行时依赖。
endef

$(eval $(call Py3Package,python3-outcome))
$(eval $(call Py3Package,python3-outcome-src))

$(eval $(call BuildPackage,python3-outcome))
$(eval $(call BuildPackage,python3-outcome-src))
