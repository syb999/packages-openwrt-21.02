#
# Copyright (C) 2006-2012 OpenWrt.org
# Copyright (C) 2017-2018 Luiz Angelo Daros de Luca <luizluca@gmail.com>
#
# This is free software, licensed under the GNU General Public License v2.
# See /LICENSE for more information.
#
# CUPS core/image libraries only (no scheduler). The CUPS daemon and the
# command line tools live in package/21.02-other-package/cups, which reuses
# exactly the same upstream version and tarball. Keep both in sync: a single
# version of the CUPS source tree must be used for libraries and daemon,
# otherwise libcups.so.2 and the daemon end up from different releases.
#

include $(TOPDIR)/rules.mk

PKG_NAME:=cups
PKG_VERSION:=2.3.3
PKG_RELEASE:=1

PKG_SOURCE:=$(PKG_NAME)-$(PKG_VERSION)-source.tar.gz
PKG_SOURCE_URL:=https://github.com/apple/cups/releases/download/v$(PKG_VERSION)/
PKG_HASH:=261fd948bce8647b6d5cb2a1784f0c24cc52b5c4e827b71d726020bcc502f3ee
PKG_MAINTAINER:=Luiz Angelo Daros de Luca <luizluca@gmail.com>
PKG_LICENSE:=Apache-2.0
PKG_LICENSE_FILES:=LICENSE.txt
PKG_CPE_ID:=cpe:/a:apple:cups

# Separate build directory from the cups daemon package (same PKG_NAME and
# PKG_VERSION are used by both Makefiles).
PKG_BUILD_DIR:=$(BUILD_DIR)/$(PKG_NAME)-libs-$(PKG_VERSION)

include $(INCLUDE_DIR)/package.mk

PKG_UNPACK:=$(HOST_TAR) -C $(PKG_BUILD_DIR) --strip-components=1 -xzf $(DL_DIR)/$(PKG_SOURCE)

define Package/libcups/Default
  URL:=http://www.cups.org/
  SUBMENU:=Printing
endef

define Package/libcups
$(call Package/libcups/Default)
  SECTION:=libs
  CATEGORY:=Libraries
  DEPENDS:=+zlib +libpthread +libpng +libjpeg +libusb-1.0
  TITLE:=Common UNIX Printing System - Core library
endef

define Package/libcups/description
	Common UNIX Printing System - Core library
endef

define Package/libcupsimage
$(call Package/libcups/Default)
  SECTION:=libs
  CATEGORY:=Libraries
  DEPENDS:=+libcups +zlib +libpng +libjpeg
  TITLE:=Common UNIX Printing System - Image library
endef

define Package/libcupsimage/description
	Common UNIX Printing System - Image library
endef

TARGET_LDFLAGS+=-Wl,-rpath-link=$(STAGING_DIR)/usr/lib

CONFIGURE_ARGS+=--with-cups-user="nobody" \
		--with-cups-group="nogroup" \
		--with-components="core" \
		--with-pdftops="none" \
		--without-perl \
		--without-python \
		--without-php \
		--enable-shared \
		--enable-image \
		--enable-libusb \
		--disable-acl \
		--disable-dbus \
		--disable-dnssd \
		--disable-launchd \
		--disable-ldap \
		--disable-pam \
		--disable-slp \
		--disable-gnutls \
		--disable-openssl \
		--disable-cdsassl \
		--disable-ssl \
		--disable-gssapi \
		--disable-tiff \
		UNAME="Linux" \
		LIBS="$(TARGET_LDFLAGS) -lz -lpng -ljpeg"

define Build/Compile
	$(MAKE) -C $(PKG_BUILD_DIR)/cups \
		$(TARGET_CONFIGURE_OPTS) \
		DSTROOT="$(PKG_INSTALL_DIR)" \
		STRIP="/bin/true" \
		libcups.so.2 install-libs install-headers
	$(INSTALL_DIR) $(PKG_INSTALL_DIR)/usr/bin
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/cups-config $(PKG_INSTALL_DIR)/usr/bin
endef

define Package/libcups/install
	$(INSTALL_DIR) $(1)/usr/lib
	$(CP) $(PKG_INSTALL_DIR)/usr/lib/libcups.so.* $(1)/usr/lib/
endef

define Package/libcupsimage/install
	$(INSTALL_DIR) $(1)/usr/lib
	$(CP) $(PKG_INSTALL_DIR)/usr/lib/libcupsimage.so.* $(1)/usr/lib/
endef

define Build/InstallDev
	$(INSTALL_DIR) $(1)/usr/bin
	$(INSTALL_BIN) $(PKG_INSTALL_DIR)/usr/bin/cups-config $(1)/usr/bin/

	$(INSTALL_DIR) $(1)/usr/include
	$(CP) $(PKG_INSTALL_DIR)/usr/include/cups $(1)/usr/include/

	$(INSTALL_DIR) $(1)/usr/lib
	$(CP) $(PKG_INSTALL_DIR)/usr/lib*/libcups*.so* $(1)/usr/lib/
endef

$(eval $(call BuildPackage,libcups))
$(eval $(call BuildPackage,libcupsimage))
