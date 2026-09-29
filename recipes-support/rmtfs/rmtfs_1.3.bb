SUMMARY = "RMTFS QMI service"
HOMEPAGE = "https://github.com/linux-msm/rmtfs.git"
SECTION = "devel"

LICENSE = "BSD-3-Clause"
LIC_FILES_CHKSUM = "file://LICENSE;md5=ca25dbf5ebfc1a058bfc657c895aac2f"

inherit systemd

SRCREV = "b30a3eb38f9af283f18dbd3c7755653efc52c094"
SRC_URI = "git://github.com/linux-msm/${BPN}.git;branch=master;protocol=https;tag=v${PV}"
DEPENDS = "qmic-native qrtr udev"

# @description Install rmtfs and its service with the source's install target.
# @noargs
# @exitcode 0 The task finished; any failing command fails the task and stops the build.
# @example
#   bitbake -c install rmtfs
do_install () {
    oe_runmake install DESTDIR=${D} prefix=${prefix} servicedir=${systemd_unitdir}/system
}

SYSTEMD_PACKAGES = "${PN} ${PN}-dir"

SYSTEMD_SERVICE:${PN} = "rmtfs.service"
RDEPENDS:${PN} += "qrtr"

PACKAGES += "${PN}-dir"
SYSTEMD_SERVICE:${PN}-dir = "rmtfs-dir.service"
RDEPENDS:${PN}-dir += "${PN}"
