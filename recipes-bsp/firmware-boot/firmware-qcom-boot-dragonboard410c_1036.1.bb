SUMMARY = "Prebuilt bootlader images for Dragonboard 410c"

LICENSE = "LicenseRef-LICENSE.qcom"
LIC_FILES_CHKSUM = "file://LICENSE;md5=4d087ee0965cb059f1b2f9429e166f64"

SRC_URI = "https://artifacts.codelinaro.org/artifactory/clo-549-96boards-backup/96boards/dragonboard410c/qualcomm/firmware/linux-board-support-package-r${PV}.zip"
SRC_URI[sha256sum] = "93070f58fa3aa6467baa881935c37c4da2df2a8af3248746931ce3d11a3a1200"

BOOTBINARIES = "linux-board-support-package-r${PV}"

QCOM_BOOT_IMG_SUBDIR = "dragonboard-410c"

include firmware-qcom-boot-common.inc

DEPENDS = "lk-db410c"

# Disable archall as we depend on arch-specific package
# @description Prepend a Python `return` to the allarch class's event handler,
#   so this recipe keeps a machine-specific package architecture.
# @noargs
# @example
#   bitbake firmware-qcom-boot-dragonboard410c
allarch_package_arch_handler:prepend() {
    return
}

# @description Deploy the bootloaders, CDT, EFS seed image, eMMC firehose
#   programmer, and licence from the board support package to
#   `QCOM_BOOT_IMG_SUBDIR` in the deploy directory, replacing the common
#   boot-binaries deploy task.
# @noargs
# @exitcode 0 The files are in `DEPLOYDIR`.
# @exitcode >0 A command failed; BitBake stops the task.
# @example
#   bitbake -c deploy firmware-qcom-boot-dragonboard410c
do_deploy() {
    install -d ${DEPLOYDIR}/${QCOM_BOOT_IMG_SUBDIR}
    find "${S}/bootloaders-linux" -maxdepth 1 -name '*.mbn' -exec install -m 0644 {} ${DEPLOYDIR}/${QCOM_BOOT_IMG_SUBDIR} \;

    install -m 0644 ${S}/cdt-linux/sbc_1.0_8016.bin ${DEPLOYDIR}/${QCOM_BOOT_IMG_SUBDIR}
    install -m 0644 ${S}/efs-seed/fs_image_linux.tar.gz.mbn.img ${DEPLOYDIR}/${QCOM_BOOT_IMG_SUBDIR}
    install -m 0644 ${S}/loaders/prog_emmc_firehose_8916.mbn ${DEPLOYDIR}/${QCOM_BOOT_IMG_SUBDIR}

    install -m 0644 ${S}/LICENSE ${DEPLOYDIR}/${QCOM_BOOT_IMG_SUBDIR}
}
