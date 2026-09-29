SUMMARY = "Prebuilt bootlader images for Dragonboard 820c"

LICENSE = "LicenseRef-LICENSE.qcom"
LIC_FILES_CHKSUM = "file://LICENSE;md5=4d087ee0965cb059f1b2f9429e166f64"

SRC_URI = "https://artifacts.codelinaro.org/artifactory/clo-549-96boards-backup/96boards/dragonboard820c/qualcomm/firmware/linux-board-support-package-r${PV}.zip"
SRC_URI[sha256sum] = "6ee9c461b2b5dd2d3bd705bb5ea3f44b319ecb909b2772f305ce12439e089cd9"

BOOTBINARIES = "linux-board-support-package-r${PV}"

QCOM_BOOT_IMG_SUBDIR = "dragonboard-820c"

include firmware-qcom-boot-common.inc

DEPENDS = "lk-db820c"

# @description Make allarch's handler return at once, so PACKAGE_ARCH is not set to "all".
# Disable archall as we depend on arch-specific package
# @noargs
# @exitcode 0 PACKAGE_ARCH keeps its architecture-specific default.
# @example
#   bitbake -e firmware-qcom-boot-dragonboard820c | grep '^PACKAGE_ARCH='
allarch_package_arch_handler:prepend() {
    return
}

# @description Deploy the Dragonboard 820c boot files, replacing the common do_deploy.
# The bootloaders-linux .mbn, .elf, and sec.dat files, the CDT, the UFS firehose programmer,
# and the LICENSE file are copied to ${DEPLOYDIR}/${QCOM_BOOT_IMG_SUBDIR}.
# @noargs
# @exitcode 0 The boot files are in ${DEPLOYDIR}/${QCOM_BOOT_IMG_SUBDIR}.
# @example
#   bitbake firmware-qcom-boot-dragonboard820c -c deploy
do_deploy() {
    install -d ${DEPLOYDIR}/${QCOM_BOOT_IMG_SUBDIR}
    find "${S}/bootloaders-linux" -maxdepth 1 \( -name '*.mbn' -o -name '*.elf' -o -name 'sec.dat' \) -exec install -m 0644 {} ${DEPLOYDIR}/${QCOM_BOOT_IMG_SUBDIR} \;

    install -m 0644 ${S}/cdt-linux/sbc_1.0_8096.bin ${DEPLOYDIR}/${QCOM_BOOT_IMG_SUBDIR}
    install -m 0644 ${S}/loaders/prog_ufs_firehose_8996_ddr.elf ${DEPLOYDIR}/${QCOM_BOOT_IMG_SUBDIR}

    install -m 0644 ${S}/LICENSE ${DEPLOYDIR}/${QCOM_BOOT_IMG_SUBDIR}
}
