#
# This is free software, licensed under the GNU General Public License v2.
# See /LICENSE for more information.
#
# 为 selenium 4.9.0 移植 (OpenWrt 21.02.5 / python3.9)。trio-websocket 依赖链
#

include $(TOPDIR)/rules.mk

PKG_NAME:=python-h11
PKG_VERSION:=0.14.0
PKG_RELEASE:=1

PYPI_NAME:=h11
PKG_HASH:=8f19fbbe99e72420ff35c00b27a34cb9937e902a8b810e2c88300c6f0a3b699d

PKG_MAINTAINER:=syb999
PKG_LICENSE:=MIT
PKG_LICENSE_FILES:=LICENSE

include ../pypi.mk
include $(INCLUDE_DIR)/package.mk
include ../python3-package.mk

define Package/python3-h11
  SUBMENU:=Python
  SECTION:=lang
  CATEGORY:=Languages
  TITLE:=Pure-Python HTTP/1.1 protocol library
  URL:=https://github.com/python-hyper/h11
  DEPENDS:=+python3-light
endef

define Package/python3-h11/description
  A pure-Python, bring-your-own-I/O implementation of HTTP/1.1. wsproto 依赖。
endef

$(eval $(call Py3Package,python3-h11))
$(eval $(call Py3Package,python3-h11-src))

$(eval $(call BuildPackage,python3-h11))
$(eval $(call BuildPackage,python3-h11-src))
