#
# This is free software, licensed under the GNU General Public License v2.
# See /LICENSE for more information.
#
# 为 selenium 4.9.0 移植 (OpenWrt 21.02.5 / python3.9)。trio 依赖链, 需补 setup.py
#

include $(TOPDIR)/rules.mk

PKG_NAME:=python-sniffio
PKG_VERSION:=1.3.1
PKG_RELEASE:=1

PYPI_NAME:=sniffio
PKG_HASH:=f4324edc670a0f49750a81b895f35c3adb843cca46f0530f79fc1babb23789dc

PKG_MAINTAINER:=syb999
PKG_LICENSE:=MIT
PKG_LICENSE_FILES:=LICENSE

include ../pypi.mk
include $(INCLUDE_DIR)/package.mk
include ../python3-package.mk

define Package/python3-sniffio
  SUBMENU:=Python
  SECTION:=lang
  CATEGORY:=Languages
  TITLE:=Detect which async library is running
  URL:=https://github.com/python-trio/sniffio
  DEPENDS:=+python3-light
endef

define Package/python3-sniffio/description
  Sniff out which async library your code is running under (asyncio or trio).
  trio 运行时依赖。原始 sdist 只有 pyproject.toml, 用补丁补 setup.py 走本树
  标准的 setup.py install 流程。
endef

$(eval $(call Py3Package,python3-sniffio))
$(eval $(call Py3Package,python3-sniffio-src))

$(eval $(call BuildPackage,python3-sniffio))
$(eval $(call BuildPackage,python3-sniffio-src))
