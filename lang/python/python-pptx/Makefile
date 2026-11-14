#
# This is free software, licensed under the GNU General Public License v2.
# See /LICENSE for more information.
#

include $(TOPDIR)/rules.mk

PKG_NAME:=python-pptx
PKG_VERSION:=1.0.2
PKG_RELEASE:=1

PYPI_NAME:=python-pptx
# The sdist uses the normalized name (python_pptx-1.0.2.tar.gz).
PYPI_SOURCE_NAME:=python_pptx
PKG_HASH:=479a8af0eaf0f0d76b6f00b0887732874ad2e3188230315290cd1f9dd9cc7095

PKG_MAINTAINER:=syb999

PKG_LICENSE:=MIT
PKG_LICENSE_FILES:=LICENSE

include ../pypi.mk
include $(INCLUDE_DIR)/package.mk
include ../python3-package.mk

# The sdist is pyproject.toml only ([project] table, needs setuptools >= 61)
# with a src/ layout; this tree builds with setuptools 58.1.0 and a plain
# "setup.py install", so 001-add-setup-py.patch supplies the metadata and the
# package_data (pptx/templates/*, needed by Presentation() without arguments).
# typing_extensions is only imported for Protocol here, which the 3.x version
# in this feed provides.

define Package/python3-pptx
  SUBMENU:=Python
  SECTION:=lang
  CATEGORY:=Languages
  TITLE:=Create, read, and update PowerPoint 2007+ (.pptx) files
  URL:=https://github.com/scanny/python-pptx
  DEPENDS:=+python3-light +python3-decimal +python3-xml +python3-typing-extensions \
	+python3-lxml +python3-pillow +python3-xlsxwriter
endef

define Package/python3-pptx/description
  python-pptx is a Python library for creating, reading, and updating
  PowerPoint 2007+ (.pptx) files.
endef

$(eval $(call Py3Package,python3-pptx))
$(eval $(call Py3Package,python3-pptx-src))

$(eval $(call BuildPackage,python3-pptx))
$(eval $(call BuildPackage,python3-pptx-src))
