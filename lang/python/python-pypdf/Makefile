#
# This is free software, licensed under the GNU General Public License v2.
# See /LICENSE for more information.
#

include $(TOPDIR)/rules.mk

PKG_NAME:=python-pypdf
PKG_VERSION:=4.3.1
PKG_RELEASE:=1

PYPI_NAME:=pypdf
PKG_HASH:=b2f37fe9a3030aa97ca86067a56ba3f9d3565f9a791b305c7355d8392c30d91b

PKG_MAINTAINER:=syb999
PKG_LICENSE:=BSD-3-Clause
PKG_LICENSE_FILES:=LICENSE

include ../pypi.mk
include $(INCLUDE_DIR)/package.mk
include ../python3-package.mk

define Package/python3-pypdf
  SUBMENU:=Python
  SECTION:=lang
  CATEGORY:=Languages
  TITLE:=Pure Python PDF library (fork of PyPDF2)
  URL:=https://pypdf.readthedocs.io/
  DEPENDS:=+python3-light +python3-typing-extensions
endef

define Package/python3-pypdf/description
  A pure Python library built as a PDF toolkit: extracting document
  information, splitting/merging pages, cropping, encrypting and decrypting.
  Import name: pypdf.
endef

$(eval $(call Py3Package,python3-pypdf))
$(eval $(call Py3Package,python3-pypdf-src))

$(eval $(call BuildPackage,python3-pypdf))
$(eval $(call BuildPackage,python3-pypdf-src))
