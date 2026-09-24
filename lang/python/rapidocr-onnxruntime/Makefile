#
# Copyright (C) 2026 OpenWrt.org
#
# This is free software, licensed under the GNU General Public License v2.
# See /LICENSE for more information.
#

include $(TOPDIR)/rules.mk

PKG_NAME:=rapidocr-onnxruntime
PKG_VERSION:=1.4.4
PKG_RELEASE:=1

# The project only publishes a pure Python wheel (py3-none-any), there is no
# source distribution. The wheel also carries the PP-OCRv4 models (det 4.7 MB,
# rec 10.9 MB, cls 0.6 MB).
PKG_SOURCE:=rapidocr_onnxruntime-$(PKG_VERSION)-py3-none-any.whl
PKG_SOURCE_URL:= \
	https://mirrors.aliyun.com/pypi/packages/ba/12/1e5497183bdbe782dbb91bad1d0d2297dba4d2831b2652657f7517bfc6df/ \
	https://files.pythonhosted.org/packages/ba/12/1e5497183bdbe782dbb91bad1d0d2297dba4d2831b2652657f7517bfc6df/
PKG_HASH:=971d7d5f223a7a808662229df1ef69893809d8457d834e6373d3854bc1782cbf

PKG_MAINTAINER:=OpenWrt.org
PKG_LICENSE:=Apache-2.0

# wheel only package: no setup.py is run, the wheel is unpacked and installed
PYTHON3_PKG_BUILD:=0
include ../python3-package.mk

include $(INCLUDE_DIR)/package.mk

# the wheel is a zip without a single top level directory
PKG_UNPACK=unzip -q -o $(DL_DIR)/$(PKG_SOURCE) -d $(PKG_BUILD_DIR)

REC_MODEL:=rapidocr_onnxruntime/models/ch_PP-OCRv4_rec_infer.onnx

# The recognizer is exported with a dynamic input shape whose reshape targets are
# computed at runtime from Shape/Slice/Concat chains; OpenCV's dnn cannot resolve
# those. Fixing the input to the width RapidOCR pads its crops to (config.yaml:
# rec_img_shape: [3, 48, 320]) makes the model run on cv2.dnn through
# python3-onnxruntime-cvdnn, with the same output as onnxruntime (max abs
# difference 1.5e-06 on identical input). patch 002 keeps the batch width at 320.
define Build/Compile
	$(HOST_PYTHON3_BIN) ./files/make_onnx_input_fixed.py \
		$(PKG_BUILD_DIR)/$(REC_MODEL) $(PKG_BUILD_DIR)/$(REC_MODEL).fixed x 1,3,48,320
	mv $(PKG_BUILD_DIR)/$(REC_MODEL).fixed $(PKG_BUILD_DIR)/$(REC_MODEL)
	$(INSTALL_DATA) ./files/polygon_stub.py \
		$(PKG_BUILD_DIR)/rapidocr_onnxruntime/ch_ppocr_det/polygon_stub.py
endef

define Package/python3-rapidocr-onnxruntime
  SUBMENU:=Python
  SECTION:=lang
  CATEGORY:=Languages
  TITLE:=RapidOCR - PP-OCRv4 text detection and recognition
  URL:=https://github.com/RapidAI/RapidOCR
  DEPENDS:=+python3 +python3-numpy +python3-opencv +python3-pillow +python3-yaml \
	+python3-pyclipper +python3-onnxruntime-cvdnn
endef

define Package/python3-rapidocr-onnxruntime/description
 RapidOCR runs the PP-OCRv4 detection, angle classification and recognition
 models and returns text boxes with the recognised text. This package uses the
 wheel from PyPI (it is pure Python and ships the models) together with
 python3-onnxruntime-cvdnn as inference backend, because the upstream
 onnxruntime has no musl/aarch64 release.

 The declared dependencies pyclipper, Pillow and PyYAML are used by the code;
 six and tqdm are declared upstream but never imported, so they are not pulled
 in. shapely is only needed for the polygon area/perimeter in the DB
 postprocessing and is replaced by an equivalent numpy implementation
 (patch 001), which avoids the GEOS dependency.
endef

define Package/python3-rapidocr-onnxruntime/install
	$(INSTALL_DIR) $(1)$(PYTHON3_PKG_DIR)
	$(CP) $(PKG_BUILD_DIR)/rapidocr_onnxruntime $(1)$(PYTHON3_PKG_DIR)/
	$(CP) $(PKG_BUILD_DIR)/rapidocr_onnxruntime-$(PKG_VERSION).dist-info $(1)$(PYTHON3_PKG_DIR)/
endef

$(eval $(call BuildPackage,python3-rapidocr-onnxruntime))
