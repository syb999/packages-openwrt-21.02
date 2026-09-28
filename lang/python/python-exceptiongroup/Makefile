#
# This is free software, licensed under the GNU General Public License v2.
# See /LICENSE for more information.
#
# 为 selenium 4.9.0 移植 (OpenWrt 21.02.5 / python3.9)。trio 依赖链, 需补 setup.py
#

include $(TOPDIR)/rules.mk

PKG_NAME:=python-exceptiongroup
PKG_VERSION:=1.2.2
PKG_RELEASE:=1

PYPI_NAME:=exceptiongroup
PKG_HASH:=47c2edf7c6738fafb49fd34290706d1a1a2f4d1c6df275526b62cbb4aa5393cc

PKG_MAINTAINER:=syb999
PKG_LICENSE:=MIT
PKG_LICENSE_FILES:=LICENSE

include ../pypi.mk
include $(INCLUDE_DIR)/package.mk
include ../python3-package.mk

define Package/python3-exceptiongroup
  SUBMENU:=Python
  SECTION:=lang
  CATEGORY:=Languages
  TITLE:=Backport of PEP 654 exception groups
  URL:=https://github.com/agronholm/exceptiongroup
  DEPENDS:=+python3-light
endef

define Package/python3-exceptiongroup/description
  Backport of PEP 654 (exception groups) for Python < 3.11.
  trio / trio-websocket 运行时依赖。原始 sdist 是 src 布局且只有 flit_scm 后端,
  用补丁补 setup.py 走本树标准的 setup.py install 流程。
endef

$(eval $(call Py3Package,python3-exceptiongroup))
$(eval $(call Py3Package,python3-exceptiongroup-src))

$(eval $(call BuildPackage,python3-exceptiongroup))
$(eval $(call BuildPackage,python3-exceptiongroup-src))
