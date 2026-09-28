SUMMARY = "Quick hack to measure memory read performance."
HOMEPAGE = "https://github.com/andersson/mybw"
LICENSE = "BSD-3-Clause"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/BSD-3-Clause-Clear;md5=7a434440b651f4a472ca93716d01033a"

SRCREV = "f4bdeee1266c273e308d0651522bb59afb5b8211"
SRC_URI = "git://github.com/andersson/mybw;protocol=https;branch=main \
           file://0001-makefile-Allow-CFLAGS-LDFLAGS-from-environment.patch \
           "

PV = "0.0+git"

# @description Build mybw with the upstream Makefile.
# @noargs
# @exitcode 0 The `mybw` binary is built.
# @exitcode >0 The build failed; BitBake stops the task.
# @example
#   bitbake -c compile mybw
do_compile () {
	oe_runmake
}

# @description Install the `mybw` binary into `${bindir}`.
# @noargs
# @exitcode 0 The binary is in the install directory.
# @exitcode >0 An install command failed; BitBake stops the task.
# @example
#   bitbake -c install mybw
do_install () {
	install -d ${D}${bindir}
	install -m 0755 mybw ${D}${bindir}/mybw
}

LDFLAGS += "-lgcc"
