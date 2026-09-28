FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"

DEFAULTBACKEND:qcom ?= "drm"

SRC_URI:append:qcom = " \
    file://additional-devices.conf \
    file://weston-start.sh \
"

# @description On Qualcomm machines, add the `additional-devices.conf` drop-in for
#   `weston.service` and the `weston-start.sh` script, replacing
#   `@bindir@` in both with the installed binary directory.
# @noargs
# @exitcode 0 The drop-in and script are in the install directory.
# @exitcode >0 An install or sed command failed; BitBake stops the task.
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
