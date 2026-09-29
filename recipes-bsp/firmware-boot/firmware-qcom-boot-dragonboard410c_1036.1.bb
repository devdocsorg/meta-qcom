SUMMARY = "Prebuilt bootlader images for Dragonboard 410c"

LICENSE = "LicenseRef-LICENSE.qcom"
LIC_FILES_CHKSUM = "file://LICENSE;md5=4d087ee0965cb059f1b2f9429e166f64"

SRC_URI = "https://artifacts.codelinaro.org/artifactory/clo-549-96boards-backup/96boards/dragonboard410c/qualcomm/firmware/linux-board-support-package-r${PV}.zip"
SRC_URI[sha256sum] = "93070f58fa3aa6467baa881935c37c4da2df2a8af3248746931ce3d11a3a1200"

BOOTBINARIES = "linux-board-support-package-r${PV}"

QCOM_BOOT_IMG_SUBDIR = "dragonboard-410c"

include firmware-qcom-boot-common.inc

DEPENDS = "lk-db410c"

# @description Make allarch's handler return at once, so PACKAGE_ARCH is not set to "all".
# Disable archall as we depend on arch-specific package
# @noargs
# @exitcode 0 PACKAGE_ARCH keeps its architecture-specific default.
# @example
#   bitbake -e firmware-qcom-boot-dragonboard410c | grep '^PACKAGE_ARCH='
allarch_package_arch_handler:prepend() {
    return
}

# @description Deploy the Dragonboard 410c boot files, replacing the common do_deploy.
# The bootloaders-linux .mbn files, the CDT, the EFS seed image, the eMMC firehose programmer,
# and the LICENSE file are copied to ${DEPLOYDIR}/${QCOM_BOOT_IMG_SUBDIR}.
# @noargs
# @exitcode 0 The boot files are in ${DEPLOYDIR}/${QCOM_BOOT_IMG_SUBDIR}.
# @example
#   bitbake firmware-qcom-boot-dragonboard410c -c deploy
do_deploy() {
    install -d ${DEPLOYDIR}/${QCOM_BOOT_IMG_SUBDIR}
    find "${S}/bootloaders-linux" -maxdepth 1 -name '*.mbn' -exec install -m 0644 {} ${DEPLOYDIR}/${QCOM_BOOT_IMG_SUBDIR} \;

    install -m 0644 ${S}/cdt-linux/sbc_1.0_8016.bin ${DEPLOYDIR}/${QCOM_BOOT_IMG_SUBDIR}
    install -m 0644 ${S}/efs-seed/fs_image_linux.tar.gz.mbn.img ${DEPLOYDIR}/${QCOM_BOOT_IMG_SUBDIR}
    install -m 0644 ${S}/loaders/prog_emmc_firehose_8916.mbn ${DEPLOYDIR}/${QCOM_BOOT_IMG_SUBDIR}

    install -m 0644 ${S}/LICENSE ${DEPLOYDIR}/${QCOM_BOOT_IMG_SUBDIR}
}
