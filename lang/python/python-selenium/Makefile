#
# This is free software, licensed under the GNU General Public License v2.
# See /LICENSE for more information.
#
# 为 selenium 4.9.0 移植 (OpenWrt 21.02.5 / python3.9)。移植主体
#

include $(TOPDIR)/rules.mk

PKG_NAME:=python-selenium
PKG_VERSION:=4.9.0
PKG_RELEASE:=1

PYPI_NAME:=selenium
PKG_HASH:=478fae77cdfaec32adb1e68d59632c8c191f920535282abcaa2d1a3d98655624

PKG_MAINTAINER:=syb999
PKG_LICENSE:=Apache-2.0
PKG_LICENSE_FILES:=LICENSE

include ../pypi.mk
include $(INCLUDE_DIR)/package.mk
include ../python3-package.mk

define Package/python3-selenium
  SUBMENU:=Python
  SECTION:=lang
  CATEGORY:=Languages
  TITLE:=Python bindings for Selenium WebDriver
  URL:=https://www.selenium.dev/
  DEPENDS:=+python3-light +python3-logging +python3-openssl +python3-urllib +python3-urllib3 +python3-certifi +python3-pysocks +python3-trio +python3-trio-websocket
endef

define Package/python3-selenium/description
  Python bindings for Selenium / WebDriver, 用于驱动 chromedriver。
  固定 4.9.0: 4.10+ 改用 urllib3 2.x 并要求 typing_extensions~=4.9, 而本树
  urllib3 为 1.25.11 (4.9.0 声明的 ~=1.26 是纯元数据约束, 运行期可用)。
endef

$(eval $(call Py3Package,python3-selenium))
$(eval $(call Py3Package,python3-selenium-src))

$(eval $(call BuildPackage,python3-selenium))
$(eval $(call BuildPackage,python3-selenium-src))
