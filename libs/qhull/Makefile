#
# This is free software, licensed under the GNU General Public License v2.
# See /LICENSE for more information.
#

include $(TOPDIR)/rules.mk

PKG_NAME:=qhull
PKG_VERSION:=2020.2
PKG_RELEASE:=1

PKG_SOURCE:=qhull-2020-src-8.0.2.tgz
PKG_SOURCE_URL:=http://www.qhull.org/download
PKG_HASH:=b5c2d7eb833278881b952c8a52d20179eab87766b00b865000469a45c1838b7e

PKG_MAINTAINER:=syb999
PKG_LICENSE:=Qhull
PKG_LICENSE_FILES:=COPYING.txt

PKG_BUILD_PARALLEL:=1

include $(INCLUDE_DIR)/package.mk
include $(INCLUDE_DIR)/cmake.mk

CMAKE_OPTIONS += \
	-DBUILD_SHARED_LIBS=ON \
	-DBUILD_STATIC_LIBS=OFF

# Only libqhull_r is needed (matplotlib links -lqhull_r for _tri); skip the
# command line tools and the C++ interface.
define Package/libqhull/install
	$(INSTALL_DIR) $(1)/usr/lib
	$(CP) $(PKG_INSTALL_DIR)/usr/lib/libqhull_r.so* $(1)/usr/lib/
endef

define Package/libqhull
  SECTION:=libs
  CATEGORY:=Libraries
  TITLE:=Qhull convex hull library (reentrant)
  URL:=http://www.qhull.org/
  DEPENDS:=+libstdcpp
endef

define Package/libqhull/description
  Qhull computes the convex hull, Delaunay triangulation, Voronoi diagram,
  halfspace intersection and furthest-site Delaunay triangulation.
endef

define Build/InstallDev
	$(INSTALL_DIR) $(1)/usr/include $(1)/usr/lib
	$(CP) $(PKG_INSTALL_DIR)/usr/include/libqhull_r $(1)/usr/include/
	$(CP) $(PKG_INSTALL_DIR)/usr/lib/libqhull_r.so* $(1)/usr/lib/
endef

$(eval $(call BuildPackage,libqhull))
