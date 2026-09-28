#
# This is free software, licensed under the GNU General Public License v2.
# See /LICENSE for more information.
#
# 为 selenium 4.9.0 移植 (OpenWrt 21.02.5 / python3.9)。trio 依赖链
#

include $(TOPDIR)/rules.mk

PKG_NAME:=python-sortedcontainers
PKG_VERSION:=2.4.0
PKG_RELEASE:=1

PYPI_NAME:=sortedcontainers
PKG_HASH:=25caa5a06cc30b6b83d11423433f65d1f9d76c4c6a0c90e3379eaa43b9bfdb88

PKG_MAINTAINER:=syb999
PKG_LICENSE:=Apache-2.0
PKG_LICENSE_FILES:=LICENSE

include ../pypi.mk
include $(INCLUDE_DIR)/package.mk
include ../python3-package.mk

define Package/python3-sortedcontainers
  SUBMENU:=Python
  SECTION:=lang
  CATEGORY:=Languages
  TITLE:=Pure-Python sorted list/dict/set containers
  URL:=http://www.grantjenks.com/docs/sortedcontainers/
  DEPENDS:=+python3-light
endef

define Package/python3-sortedcontainers/description
  Pure-Python sorted container types (SortedList/SortedDict/SortedSet).
  trio 运行时依赖。
endef

$(eval $(call Py3Package,python3-sortedcontainers))
$(eval $(call Py3Package,python3-sortedcontainers-src))

$(eval $(call BuildPackage,python3-sortedcontainers))
$(eval $(call BuildPackage,python3-sortedcontainers-src))
