SUMMARY = "Systemd unit to mount persist parition at /var/lib/tee"
DESCRIPTION  = "Mount persist partition at /var/lib/tee to store \
encryped data and support security functions"
LICENSE = "BSD-3-Clause-Clear"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/BSD-3-Clause-Clear;md5=7a434440b651f4a472ca93716d01033a"

SRC_URI = " \
    file://var-lib-tee.mount \
    file://check-tee-partition-fs.sh \
    file://format-tee-partition.service \
    file://persist.rules \
"

inherit features_check systemd
REQUIRED_DISTRO_FEATURES = "systemd"

INHIBIT_DEFAULT_DEPS = "1"

S = "${UNPACKDIR}"

do_compile[noexec] = "1"

# @description Install the units, script, and udev rule that mount the persist partition.
# This installs var-lib-tee.mount, format-tee-partition.service (with @sbindir@ replaced by
# ${sbindir}), check-tee-partition-fs.sh in ${sbindir}, and persist.rules as 99-persist.rules.
# @noargs
# @exitcode 0 The files are under ${D}.
# @example
#   bitbake mount-tee-partition -c install
do_install() {
    install -Dm 0644 ${UNPACKDIR}/var-lib-tee.mount \
            ${D}${systemd_system_unitdir}/var-lib-tee.mount
    install -Dm 0755 ${UNPACKDIR}/check-tee-partition-fs.sh \
            ${D}${sbindir}/check-tee-partition-fs.sh
    install -Dm 0644 ${UNPACKDIR}/format-tee-partition.service \
            ${D}${systemd_system_unitdir}/format-tee-partition.service
    sed -i -e "s,@sbindir@,${sbindir},g" \
            ${D}${systemd_system_unitdir}/format-tee-partition.service
    install -Dm 0644 ${UNPACKDIR}/persist.rules \
            ${D}${nonarch_base_libdir}/udev/rules.d/99-persist.rules
}

PACKAGES = "${PN}"

SYSTEMD_SERVICE:${PN} = "var-lib-tee.mount format-tee-partition.service"

RDEPENDS:${PN} += "e2fsprogs-e2fsck e2fsprogs-mke2fs util-linux-blkid"
