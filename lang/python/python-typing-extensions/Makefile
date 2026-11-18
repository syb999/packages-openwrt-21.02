#
# Copyright (C) 2021 CZ.NIC, z. s. p. o. (https://www.nic.cz/)
#
# This is free software, licensed under the GNU General Public License v2.
# See /LICENSE for more information.
#

include $(TOPDIR)/rules.mk

PKG_NAME:=python-typing-extensions
PKG_VERSION:=4.12.2
PKG_RELEASE:=1

# 3.7.4.3 (the 21.02 upstream version) has no TypeAlias (3.10.0.0) nor Self
# (4.0.0), which pypdf imports on python < 3.10 / < 3.11. 4.x is a superset of
# the 3.x API, so the packages that only use Protocol/Literal from it
# (python-pptx, python-twisted, python-aiohttp) are unaffected.
PYPI_NAME:=typing-extensions
PYPI_SOURCE_NAME:=typing_extensions
PKG_HASH:=1a7ead55c7e559dd4dee8856e3a88b41225abfe1ce8df57b7c13915fe121ffb8

PKG_MAINTAINER:=Jan Pavlinec <jan.pavlinec@nic.cz>
PKG_LICENSE:=PSF-2.0
PKG_LICENSE_FILES:=LICENSE

include ../pypi.mk
include $(INCLUDE_DIR)/package.mk
include ../python3-package.mk

define Package/python3-typing-extensions
  SUBMENU:=Python
  SECTION:=lang
  CATEGORY:=Languages
  TITLE:=Module with type hints for Python
  URL:=https://github.com/python/typing
  DEPENDS:= \
	+python3-light
endef

define Package/python3-typing-extensions/description
  Backported and Experimental Type Hints for Python.
endef

$(eval $(call Py3Package,python3-typing-extensions))
$(eval $(call BuildPackage,python3-typing-extensions))
$(eval $(call BuildPackage,python3-typing-extensions-src))
