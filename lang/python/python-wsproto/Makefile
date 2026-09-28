#
# This is free software, licensed under the GNU General Public License v2.
# See /LICENSE for more information.
#
# 为 selenium 4.9.0 移植 (OpenWrt 21.02.5 / python3.9)。trio-websocket 依赖链
#

include $(TOPDIR)/rules.mk

PKG_NAME:=python-wsproto
PKG_VERSION:=1.2.0
PKG_RELEASE:=1

PYPI_NAME:=wsproto
PKG_HASH:=ad565f26ecb92588a3e43bc3d96164de84cd9902482b130d0ddbaa9664a85065

PKG_MAINTAINER:=syb999
PKG_LICENSE:=MIT
PKG_LICENSE_FILES:=LICENSE

include ../pypi.mk
include $(INCLUDE_DIR)/package.mk
include ../python3-package.mk

define Package/python3-wsproto
  SUBMENU:=Python
  SECTION:=lang
  CATEGORY:=Languages
  TITLE:=Pure-Python WebSocket protocol implementation
  URL:=https://github.com/python-hyper/wsproto
  DEPENDS:=+python3-light +python3-h11
endef

define Package/python3-wsproto/description
  A pure-Python WebSocket (RFC 6455) protocol stack, built on h11.
  1.3.x 要求 python>=3.10, 本树是 3.9.16, 故固定 1.2.0。
endef

$(eval $(call Py3Package,python3-wsproto))
$(eval $(call Py3Package,python3-wsproto-src))

$(eval $(call BuildPackage,python3-wsproto))
$(eval $(call BuildPackage,python3-wsproto-src))
