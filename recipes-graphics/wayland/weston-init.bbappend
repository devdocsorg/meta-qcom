FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"

DEFAULTBACKEND:qcom ?= "drm"

SRC_URI:append:qcom = " \
    file://additional-devices.conf \
    file://weston-start.sh \
"

# @description Install the weston.service drop-in and weston-start.sh, which passes extra KMS cards to Weston.
# @noargs
# @exitcode 0 The task finished; any failing command fails the task and stops the build.
# @example
#   bitbake -c install weston-init
do_install:append:qcom() {
    install -d ${D}${systemd_system_unitdir}/weston.service.d
    install -m 0644 ${UNPACKDIR}/additional-devices.conf \
        ${D}${systemd_system_unitdir}/weston.service.d/additional-devices.conf
    sed -i -e 's:@bindir@:${bindir}:g' \
        ${D}${systemd_system_unitdir}/weston.service.d/additional-devices.conf

    install -d ${D}${bindir}
    install -m 0755 ${UNPACKDIR}/weston-start.sh \
        ${D}${bindir}/weston-start.sh
    sed -i -e 's:@bindir@:${bindir}:g' \
        ${D}${bindir}/weston-start.sh
}

FILES:${PN} += "${systemd_system_unitdir}/weston.service.d/additional-devices.conf"
FILES:${PN} += "${bindir}/weston-start.sh"
