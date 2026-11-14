#
# This is free software, licensed under the GNU General Public License v2.
# See /LICENSE for more information.
#

include $(TOPDIR)/rules.mk

PKG_NAME:=python-kiwisolver
PKG_VERSION:=1.3.2
PKG_RELEASE:=1

PYPI_NAME:=kiwisolver
PKG_HASH:=fc4453705b81d03568d5b808ad8f09c77c47534f6ac2e72e733f9ca4714aa75c

PKG_MAINTAINER:=syb999
PKG_LICENSE:=BSD-3-Clause
PKG_LICENSE_FILES:=LICENSE

# The C++ sources are wrapped with cppy (header-only, arch independent), so it
# is installed into the host Python by ../../host-pip-requirements/cppy.txt.
HOST_PYTHON3_PACKAGE_BUILD_DEPENDS:=cppy

# 1.3.2 is the last release whose sdist is a plain setup.py tree without the
# setuptools_scm generated version.h of 1.4.x; source files need cppy >= 1.1.
PYPI_HOST_INDEX_URL?=https://mirrors.aliyun.com/pypi/simple

include ../pypi.mk
include $(INCLUDE_DIR)/package.mk
include ../python3-package.mk

PYTHON3_PKG_HOST_PIP_INSTALL_ARGS+=$(if $(PYPI_HOST_INDEX_URL),--index-url $(PYPI_HOST_INDEX_URL))

define Package/python3-kiwisolver
  SUBMENU:=Python
  SECTION:=lang
  CATEGORY:=Languages
  TITLE:=A fast implementation of the Cassowary constraint solver
  URL:=https://github.com/nucleic/kiwi
  DEPENDS:=+python3-light +libstdcpp
endef

define Package/python3-kiwisolver/description
  Kiwi is an efficient C++ implementation of the Cassowary constraint solving
  algorithm, used by matplotlib for its layout managers.
endef

$(eval $(call Py3Package,python3-kiwisolver))
$(eval $(call Py3Package,python3-kiwisolver-src))

$(eval $(call BuildPackage,python3-kiwisolver))
$(eval $(call BuildPackage,python3-kiwisolver-src))
