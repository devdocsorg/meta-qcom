DESCRIPTION = "An override for adbd unit - start adbd depending on the kernel command line"
SECTION = "console/utils"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

S = "${UNPACKDIR}"

SRC_URI = " \
    file://50-adbd-cmdline.conf \
"

# @description Install a systemd drop-in that starts adbd only when debugging is enabled.
# adbd then starts when "adbd" is on the kernel command line or /etc/usb-debugging-enabled exists.
# @noargs
# @exitcode 0 The drop-in is in ${systemd_unitdir}/system/android-tools-adbd.service.d.
# @example
#   bitbake android-tools-adbd-cmdline -c install
do_install() {
    install -d ${D}${systemd_unitdir}/system/android-tools-adbd.service.d
    install -m 0644 ${S}/50-adbd-cmdline.conf ${D}${systemd_unitdir}/system/android-tools-adbd.service.d
}

FILES:${PN} += " \
    ${systemd_unitdir}/system/ \
"
