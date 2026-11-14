#
# This is free software, licensed under the GNU General Public License v2.
# See /LICENSE for more information.
#

include $(TOPDIR)/rules.mk

PKG_NAME:=python-xlsxwriter
PKG_VERSION:=3.2.1
PKG_RELEASE:=1

PYPI_NAME:=XlsxWriter
PKG_HASH:=97618759cb264fb6a93397f660cca156ffa9561743b1823dafb60dc4474e1902

PKG_MAINTAINER:=syb999

PKG_LICENSE:=BSD-2-Clause
PKG_LICENSE_FILES:=LICENSE.txt

include ../pypi.mk
include $(INCLUDE_DIR)/package.mk
include ../python3-package.mk

# Pure Python; only python-pptx uses it here, to write the workbook behind a
# chart's embedded data (pptx.chart.xlsx imports it unconditionally).

define Package/python3-xlsxwriter
  SUBMENU:=Python
  SECTION:=lang
  CATEGORY:=Languages
  TITLE:=Python module for creating Excel XLSX files
  URL:=https://github.com/jmcnamara/XlsxWriter
  DEPENDS:=+python3-light +python3-decimal
endef

define Package/python3-xlsxwriter/description
  XlsxWriter is a Python module for writing files in the Excel 2007+ XLSX
  file format.
endef

$(eval $(call Py3Package,python3-xlsxwriter))
$(eval $(call Py3Package,python3-xlsxwriter-src))

$(eval $(call BuildPackage,python3-xlsxwriter))
$(eval $(call BuildPackage,python3-xlsxwriter-src))
