
include $(TOPDIR)/rules.mk

PKG_NAME:=pyzbar
PKG_VERSION:=0.1.9
PKG_RELEASE:=1

PKG_SOURCE_URL:=https://github.com/NaturalHistoryMuseum/pyzbar
PKG_SOURCE_PROTO:=git
PKG_SOURCE_VERSION:=ff2892666fa7cd305f0a95f9808159809c6fc222
PKG_HASH:=b94e99df64aefa320771049725a624ce336c201f9903783f63a40e2eb93abc9a

PKG_BUILD_DIR:=$(BUILD_DIR)/pypi/pyzbar-$(PKG_VERSION)

include $(INCLUDE_DIR)/package.mk
include $(TOPDIR)/feeds/packages/lang/python/python3-package.mk

define Package/python3-pyzbar
  SUBMENU:=Python
  SECTION:=lang
  CATEGORY:=Languages
  TITLE:=barcodes and QR codes
  URL:=https://github.com/NaturalHistoryMuseum/pyzbar
  DEPENDS:=+zbar +python3
endef

define Package/python3-pyzbar/description
  Read one-dimensional barcodes and QR codes 
  from Python 2 and 3 using the zbar library.
endef


$(eval $(call Py3Package,python3-pyzbar))
$(eval $(call BuildPackage,python3-pyzbar))
$(eval $(call BuildPackage,python3-pyzbar-src))
