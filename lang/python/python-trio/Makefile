#
# This is free software, licensed under the GNU General Public License v2.
# See /LICENSE for more information.
#
# 为 selenium 4.9.0 移植 (OpenWrt 21.02.5 / python3.9)。selenium 4.9.0 直接依赖
#

include $(TOPDIR)/rules.mk

PKG_NAME:=python-trio
PKG_VERSION:=0.22.2
PKG_RELEASE:=1

PYPI_NAME:=trio
PKG_HASH:=3887cf18c8bcc894433420305468388dac76932e9668afa1c49aa3806b6accb3

PKG_MAINTAINER:=syb999
PKG_LICENSE:=MIT
PKG_LICENSE_FILES:=LICENSE

include ../pypi.mk
include $(INCLUDE_DIR)/package.mk
include ../python3-package.mk

define Package/python3-trio
  SUBMENU:=Python
  SECTION:=lang
  CATEGORY:=Languages
  TITLE:=An async/await-native I/O library
  URL:=https://github.com/python-trio/trio
  DEPENDS:=+python3-light +python3-asyncio +python3-logging +python3-attrs +python3-idna +python3-sortedcontainers +python3-outcome +python3-sniffio +python3-exceptiongroup
endef

define Package/python3-trio/description
  Trio is an async I/O library with a focus on usability and correctness.
  selenium 4.9.0 用它承载 WebDriver 的 HTTP/BiDi 传输。
  0.23+ 要求 attrs>=23.2 (本树 attrs 为 21.2.0), 故固定 0.22.2。
endef

$(eval $(call Py3Package,python3-trio))
$(eval $(call Py3Package,python3-trio-src))

$(eval $(call BuildPackage,python3-trio))
$(eval $(call BuildPackage,python3-trio-src))
