#
# Copyright (C) 2026 OpenWrt.org
#
# This is free software, licensed under the GNU General Public License v2.
# See /LICENSE for more information.
#

include $(TOPDIR)/rules.mk

PKG_NAME:=onnxruntime-cvdnn
PKG_VERSION:=0.1.0
PKG_RELEASE:=1

PKG_MAINTAINER:=OpenWrt.org
PKG_LICENSE:=Apache-2.0

# Pure Python package: it provides the onnxruntime Python API (the subset that
# model code such as RapidOCR uses) implemented on top of python3-opencv, so
# that packages which depend on onnxruntime can run on targets where the real
# ONNX Runtime is not available (it ships glibc wheels only and no source
# release, i.e. nothing that can be built for musl).
PYTHON3_PKG_BUILD:=0
include ../python3-package.mk

include $(INCLUDE_DIR)/package.mk

# nothing to compile, the module is a single Python file
define Build/Compile
endef

define Package/python3-onnxruntime-cvdnn
  SUBMENU:=Python
  SECTION:=lang
  CATEGORY:=Languages
  TITLE:=onnxruntime Python API implemented with OpenCV dnn (CPU only)
  URL:=https://onnxruntime.ai/
  DEPENDS:=+python3 +python3-numpy +python3-opencv
endef

define Package/python3-onnxruntime-cvdnn/description
 A small, CPU only implementation of the onnxruntime Python API on top of
 python3-opencv (cv2.dnn): InferenceSession, SessionOptions,
 GraphOptimizationLevel, get_available_providers(), get_device() and the
 model metadata (custom_metadata_map), which is read from the ONNX file with a
 tiny protobuf scanner.

 It installs the module "onnxruntime", so code written for onnxruntime runs
 unchanged as long as it stays inside the API subset above and its models only
 use operators that cv2.dnn implements. This is not the real ONNX Runtime.
endef

define Package/python3-onnxruntime-cvdnn/install
	$(INSTALL_DIR) $(1)$(PYTHON3_PKG_DIR)
	$(INSTALL_DATA) ./files/onnxruntime.py $(1)$(PYTHON3_PKG_DIR)/
endef

$(eval $(call BuildPackage,python3-onnxruntime-cvdnn))
