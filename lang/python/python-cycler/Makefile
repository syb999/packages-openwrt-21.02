#
# This is free software, licensed under the GNU General Public License v2.
# See /LICENSE for more information.
#

include $(TOPDIR)/rules.mk

PKG_NAME:=python-cycler
PKG_VERSION:=0.11.0
PKG_RELEASE:=1

PYPI_NAME:=cycler
PKG_HASH:=9c87405839a19696e837b3b818fed3f5f69f16f1eec1a1ad77e043dcea9c772f

PKG_MAINTAINER:=syb999
PKG_LICENSE:=BSD-3-Clause
PKG_LICENSE_FILES:=LICENSE

include ../pypi.mk
include $(INCLUDE_DIR)/package.mk
include ../python3-package.mk

define Package/python3-cycler
  SUBMENU:=Python
  SECTION:=lang
  CATEGORY:=Languages
  TITLE:=Composable style cycles
  URL:=https://github.com/matplotlib/cycler
  DEPENDS:=+python3-light
endef

define Package/python3-cycler/description
  Composable style cycles, used by matplotlib to cycle through property
  values such as colors, line styles and markers.
endef

$(eval $(call Py3Package,python3-cycler))
$(eval $(call Py3Package,python3-cycler-src))

$(eval $(call BuildPackage,python3-cycler))
$(eval $(call BuildPackage,python3-cycler-src))
