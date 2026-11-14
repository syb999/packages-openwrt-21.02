#
# This is free software, licensed under the GNU General Public License v2.
# See /LICENSE for more information.
#

include $(TOPDIR)/rules.mk

PKG_NAME:=python-matplotlib
PKG_VERSION:=3.5.3
PKG_RELEASE:=1

PYPI_NAME:=matplotlib
PKG_HASH:=339cac48b80ddbc8bfd05daae0a3a73414651a8596904c2a881cfd1edb65f26c

PKG_MAINTAINER:=syb999
PKG_LICENSE:=PSF-2.0
PKG_LICENSE_FILES:=LICENSE/LICENSE

# setup.py imports numpy to get the include dir of the C++ extensions.
# 001-setup-no-build-time-downloads.patch drops setup_requires (numpy,
# setuptools_scm, certifi, setuptools_scm_git_archive) and use_scm_version,
# which would otherwise make setuptools fetch those from PyPI. The sdist ships
# lib/matplotlib/_version.py and PY_PKG_VERSION is passed by python3-package.mk.
HOST_PYTHON3_PACKAGE_BUILD_DEPENDS:=numpy

# Build against the numpy and qhull of this tree (source package names).
PKG_BUILD_DEPENDS:=numpy qhull

include ../pypi.mk
include $(INCLUDE_DIR)/package.mk
include ../python3-package.mk

# files/mplsetup.cfg makes setupext.py link the system freetype and qhull
# instead of its bundled copies. Do not build the extensions in parallel:
# src/py_converters.cpp is compiled into several extensions and setuptools'
# --parallel would race on that one object file (see the pandas notes).
PYTHON3_PKG_SETUP_VARS:=MPLSETUPCFG=$(PKG_BUILD_DIR)/mplsetup.cfg

define Build/Prepare
	$(call Build/Prepare/Default)
	$(CP) ./files/mplsetup.cfg $(PKG_BUILD_DIR)/mplsetup.cfg
endef

define Package/python3-matplotlib
  SUBMENU:=Python
  SECTION:=lang
  CATEGORY:=Languages
  TITLE:=Python plotting package
  URL:=https://matplotlib.org/
  DEPENDS:=+python3-light +python3-numpy +python3-pillow +python3-cycler \
	+python3-kiwisolver +python3-fonttools +python3-pyparsing +python3-packaging \
	+python3-dateutil +python3-logging +python3-decimal +python3-urllib \
	+libfreetype +libqhull +libstdcpp
endef

define Package/python3-matplotlib/description
  Matplotlib is a comprehensive library for creating static, animated, and
  interactive visualizations in Python. Built with the Agg backend only.
endef

$(eval $(call Py3Package,python3-matplotlib))
$(eval $(call Py3Package,python3-matplotlib-src))

$(eval $(call BuildPackage,python3-matplotlib))
$(eval $(call BuildPackage,python3-matplotlib-src))
