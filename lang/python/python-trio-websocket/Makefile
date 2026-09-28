#
# This is free software, licensed under the GNU General Public License v2.
# See /LICENSE for more information.
#
# 为 selenium 4.9.0 移植 (OpenWrt 21.02.5 / python3.9)。selenium 4.9.0 直接依赖
#

include $(TOPDIR)/rules.mk

PKG_NAME:=python-trio-websocket
PKG_VERSION:=0.12.2
PKG_RELEASE:=1

PYPI_NAME:=trio-websocket
PYPI_SOURCE_NAME:=trio_websocket
PKG_HASH:=22c72c436f3d1e264d0910a3951934798dcc5b00ae56fc4ee079d46c7cf20fae

PKG_MAINTAINER:=syb999
PKG_LICENSE:=MIT
PKG_LICENSE_FILES:=LICENSE

include ../pypi.mk
include $(INCLUDE_DIR)/package.mk
include ../python3-package.mk

define Package/python3-trio-websocket
  SUBMENU:=Python
  SECTION:=lang
  CATEGORY:=Languages
  TITLE:=WebSocket client library built on Trio
  URL:=https://github.com/python-trio/trio-websocket
  DEPENDS:=+python3-light +python3-asyncio +python3-trio +python3-wsproto +python3-outcome +python3-exceptiongroup
endef

define Package/python3-trio-websocket/description
  WebSocket client/protocol implementation for Trio.
  selenium 4.9.0 的 WebDriver BiDi/CDP 连接依赖。
endef

$(eval $(call Py3Package,python3-trio-websocket))
$(eval $(call Py3Package,python3-trio-websocket-src))

$(eval $(call BuildPackage,python3-trio-websocket))
$(eval $(call BuildPackage,python3-trio-websocket-src))
