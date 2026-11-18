#
# This is free software, licensed under the GNU General Public License v2.
# See /LICENSE for more information.
#

include $(TOPDIR)/rules.mk

PKG_NAME:=python-midiutil
PKG_VERSION:=1.2.1
PKG_RELEASE:=1

PYPI_NAME:=midiutil
PYPI_SOURCE_NAME:=MIDIUtil
PKG_HASH:=79fa983bd1efc60785f68a8fe78fa8f45b8d7ec5898bf7cb7f3f7f3336d6a90a

PKG_MAINTAINER:=syb999
PKG_LICENSE:=MIT
PKG_LICENSE_FILES:=LICENSE

include ../pypi.mk
include $(INCLUDE_DIR)/package.mk
include ../python3-package.mk

define Package/python3-midiutil
  SUBMENU:=Python
  SECTION:=lang
  CATEGORY:=Languages
  TITLE:=MIDI file writing library
  URL:=https://github.com/MarkCWirt/MIDIUtil
  DEPENDS:=+python3-light
endef

define Package/python3-midiutil/description
  Pure Python library to write Standard MIDI Files (import name: midiutil).
endef

$(eval $(call Py3Package,python3-midiutil))
$(eval $(call Py3Package,python3-midiutil-src))

$(eval $(call BuildPackage,python3-midiutil))
$(eval $(call BuildPackage,python3-midiutil-src))
