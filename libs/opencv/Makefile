#
# Copyright (C) 2026 OpenWrt.org
#
# This is free software, licensed under the GNU General Public License v2.
# See /LICENSE for more information.
#

include $(TOPDIR)/rules.mk

PKG_NAME:=opencv
PKG_VERSION:=4.8.1
PKG_RELEASE:=3

# Source: the sdist of opencv-python-headless, which vendors the complete OpenCV
# source tree (opencv/). Using that sdist keeps this package on exactly the
# source that the PyPI package is built from, and it is the only archive that is
# reachable fast from CN networks: the opencv git archive on github/codeload
# crawls at ~1 MB/min here, while the PyPI mirrors deliver ~50 MB/min.
PKG_SOURCE:=opencv-python-headless-4.8.1.78.tar.gz
PKG_SOURCE_URL:= \
	https://mirrors.aliyun.com/pypi/packages/0c/3a/062caf910026a174b15a24b959bc401e756fda7f42d9d404dec8b166f359/ \
	https://files.pythonhosted.org/packages/0c/3a/062caf910026a174b15a24b959bc401e756fda7f42d9d404dec8b166f359/
PKG_HASH:=bc7197b42352f6f865c302a49140b889ec7cd957dd697e2d7fc016ad0d3f28f1

# the archive is named after the PyPI project, so its single top level directory
# has to be stripped to get the build directory the build expects (the unpack
# command needs HOST_TAR, hence it is set after the includes below)

PKG_MAINTAINER:=OpenWrt.org

PKG_LICENSE:=Apache-2.0
PKG_LICENSE_FILES:=LICENSE.txt

PKG_BUILD_PARALLEL:=1
PKG_USE_NINJA:=1
PKG_USE_MIPS16:=0

# numpy headers for the python bindings, numpy itself has to be built for the
# target as well (cv2 imports it at runtime), and ffmpeg provides the videoio
# backends for video files and network streams.
PKG_BUILD_DEPENDS:=numpy ffmpeg
HOST_PYTHON3_PACKAGE_BUILD_DEPENDS:=numpy

# Only for PYTHON3_VERSION / PYTHON3_INC_DIR / HOST_PYTHON3_BIN and the host pip
# install of the numpy build dependency; the build itself is done by cmake.mk.
PYTHON3_PKG_BUILD:=0
include $(TOPDIR)/feeds/packages/lang/python/python3-package.mk

include $(INCLUDE_DIR)/package.mk
include $(INCLUDE_DIR)/cmake.mk

# strip the single top level directory of the PyPI named archive
PKG_UNPACK=$(HOST_TAR) -C $(PKG_BUILD_DIR) --strip-components=1 -xf $(DL_DIR)/$(PKG_SOURCE)

# the OpenCV source tree inside the sdist
CMAKE_SOURCE_SUBDIR:=opencv
CMAKE_BINARY_SUBDIR:=build

define Package/libopencv
  SECTION:=libs
  CATEGORY:=Libraries
  TITLE:=OpenCV - computer vision and machine learning library
  URL:=https://opencv.org/
  DEPENDS:=+libstdcpp +libpthread +librt +libatomic +zlib +libjpeg-turbo +libpng +libtiff +libwebp +libffmpeg-full
endef

define Package/libopencv/description
 OpenCV (Open Source Computer Vision Library) is an open source computer
 vision and machine learning software library.
endef

define Package/python3-opencv
  SECTION:=lang
  CATEGORY:=Languages
  SUBMENU:=Python
  TITLE:=OpenCV Python bindings (cv2), headless
  URL:=https://opencv.org/
  DEPENDS:=+libopencv +python3 +python3-numpy
endef

define Package/python3-opencv/description
 Python bindings for OpenCV (the "cv2" module), built without any GUI support:
 the equivalent of the opencv-python-headless package on PyPI, built from the
 same source (4.8.1) instead of a prebuilt manylinux wheel.

 Modules: core, imgproc, imgcodecs, videoio (V4L2 and ffmpeg), calib3d, features2d,
 flann, ml, objdetect, photo, video, dnn. No highgui/GTK/Qt, no IPP and no quirc:
 those either need a GUI stack or download prebuilt blobs during the build, which
 cannot work here.

 Video I/O uses the ffmpeg libraries of the feed (libffmpeg-full), so in addition
 to USB/V4L2 cameras this can open video files and network streams.
endef

# Everything that would download prebuilt blobs during the build (ippicv, ade,
# quirc) or needs a GUI stack stays off. ffmpeg comes from the feed instead of
# the prebuilt binaries the OpenCV build would download.
CMAKE_OPTIONS += \
	-DCMAKE_BUILD_TYPE=Release \
	-DBUILD_DOCS=OFF -DBUILD_EXAMPLES=OFF -DBUILD_TESTS=OFF -DBUILD_PERF_TESTS=OFF \
	-DBUILD_opencv_apps=OFF -DBUILD_opencv_ts=OFF -DBUILD_JAVA=OFF -DBUILD_opencv_java=OFF \
	-DBUILD_opencv_js=OFF -DBUILD_opencv_world=OFF -DBUILD_opencv_gapi=OFF \
	-DBUILD_opencv_stitching=OFF -DBUILD_opencv_superres=OFF -DBUILD_opencv_videostab=OFF \
	-DBUILD_opencv_highgui=OFF -DBUILD_opencv_python2=OFF -DBUILD_opencv_python3=ON \
	-DENABLE_PRECOMPILED_HEADERS=OFF \
	-DWITH_IPP=OFF -DWITH_ITT=OFF -DWITH_OPENCL=OFF -DWITH_OPENCLAMDFFT=OFF \
	-DWITH_OPENCLAMDBLAS=OFF -DWITH_GTK=OFF -DWITH_QT=OFF -DWITH_WIN32UI=OFF \
	-DWITH_1394=OFF -DWITH_GSTREAMER=OFF -DWITH_FFMPEG=ON -DWITH_V4L=ON -DWITH_LIBV4L=OFF \
	-DWITH_OPENNI=OFF -DWITH_OPENNI2=OFF -DWITH_VTK=OFF -DWITH_EIGEN=OFF -DWITH_LAPACK=OFF \
	-DWITH_JASPER=OFF -DWITH_OPENEXR=OFF -DWITH_QUIRC=OFF \
	-DWITH_PNG=ON -DWITH_JPEG=ON -DWITH_TIFF=ON -DWITH_WEBP=ON \
	-DWITH_OPENMP=OFF -DWITH_OPENJPEG=OFF \
	-DPYTHON3_EXECUTABLE=$(HOST_PYTHON3_BIN) \
	-DPYTHON3_INCLUDE_DIR=$(PYTHON3_INC_DIR) \
	-DPYTHON3_LIBRARY=$(STAGING_DIR)/usr/lib/libpython$(PYTHON3_VERSION).so \
	-DPYTHON3_NUMPY_INCLUDE_DIRS=$(HOST_PYTHON3_DIR)/lib/python$(PYTHON3_VERSION)/site-packages/numpy/core/include \
	-DOPENCV_PYTHON3_INSTALL_PATH=$(PYTHON3_PKG_DIR)

define Build/Prepare
	$(call Build/Prepare/Default)
	$(call Py3Build/InstallBuildDepends)
endef

PYTHON3_PKG_DIR_ABS:=$(PKG_INSTALL_DIR)$(PYTHON3_PKG_DIR)

# cmake installs everything into $(PKG_INSTALL_DIR); make sure the python
# bindings were really produced for the target before the package is packed
# (cmake silently builds without them when it cannot find python or numpy).
define Build/Install
	$(call Build/Install/Default)
	$(SHELL) ./files/check-opencv-install.sh "$(TARGET_CROSS)readelf" "$(PYTHON3_PKG_DIR_ABS)" "$(PKG_INSTALL_DIR)/usr/lib" "libavcodec"
endef

define Package/libopencv/install
	$(INSTALL_DIR) $(1)/usr/lib
	$(CP) $(PKG_INSTALL_DIR)/usr/lib/libopencv_*.so* $(1)/usr/lib/
endef

define Package/python3-opencv/install
	$(INSTALL_DIR) $(1)$(PYTHON3_PKG_DIR)
	$(CP) $(PYTHON3_PKG_DIR_ABS)/cv2* $(1)$(PYTHON3_PKG_DIR)/
endef

$(eval $(call BuildPackage,libopencv))
$(eval $(call BuildPackage,python3-opencv))
