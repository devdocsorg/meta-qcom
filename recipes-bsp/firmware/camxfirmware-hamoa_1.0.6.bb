SUMMARY = "Qualcomm camera firmware for Hamoa"
DESCRIPTION = "Qualcomm camera firmware to support camera functionality on Hamoa"
LICENSE = "LicenseRef-LICENSE.qcom-2"
LIC_FILES_CHKSUM = "file://usr/share/doc/${BPN}/LICENSE.QCOM-2.txt;md5=165287851294f2fb8ac8cbc5e24b02b0"

PBT_BUILD_DATE = "260911"
PBT_BRANCH = "master"
SRC_URI = "https://qartifactory-edge.qualcomm.com/artifactory/qsc_releases/software/chip/component/camx.qclinux.0.0/${PBT_BUILD_DATE}/prebuilt_yocto_${PBT_BRANCH}/${BPN}_${PV}_armv8-2a.tar.gz"
SRC_URI[sha256sum] = "21c27f927c8a8d5caa97ae70a49fa57d513c8c6b9232fba2dc0503f6b7fd0fac"

S = "${UNPACKDIR}"

FW_QCOM_NAME = "x1e80100"
require recipes-bsp/firmware/firmware-qcom.inc

# Disable configure and compile steps since this recipe uses prebuilt binaries.
do_configure[noexec] = "1"
do_compile[noexec] = "1"

# @function do_install
# @description Install the Hamoa camera firmware and its licence, and link it for Purwa.
# CAMERA_ICP.mbn goes to ${FW_QCOM_PATH}, and ${FW_QCOM_BASE_PATH}/x1p42100 gets a symlink to it
# whose name carries the suffix that do_install:append gives the compressed file.
# @noargs
# @exitcode 0 The firmware, licence, and x1p42100 symlink are under ${D}.
# @example
#   bitbake camxfirmware-hamoa -c install

# Return the file name suffix that FIRMWARE_COMPRESSION gives the installed firmware files.
#
# Args:
#     d (bb.data_smart.DataSmart): The recipe's datastore.
#
# Returns:
#     str: "" when FIRMWARE_COMPRESSION is empty, ".zst" for "zstd", and otherwise "."
#     followed by the value, such as ".xz".
#
# Example:
#     In do_install, ``CAMERA_ICP.mbn${@fw_compr_file_suffix(d)}`` expands to
#     ``CAMERA_ICP.mbn.zst`` when FIRMWARE_COMPRESSION is "zstd".
def fw_compr_file_suffix(d):
    compr = d.getVar('FIRMWARE_COMPRESSION')
    if compr == '':
        return ''
    if compr == 'zstd':
        compr = 'zst'
    return '.' + compr

do_install() {
    install -d ${D}${FW_QCOM_PATH}
    install -m 0644 ${S}/usr/lib/firmware/qcom/x1e80100/CAMERA_ICP.mbn ${D}${FW_QCOM_PATH}
    install -d ${D}${datadir}/doc/${BPN}
    install -m 0644 ${S}/usr/share/doc/${BPN}/LICENSE.QCOM-2.txt ${D}${datadir}/doc/${BPN}

    # Purwa and Hamoa platforms use same CAMX firmware.
    # Create symlinks under x1p42100 to satisfy platform-specific
    # lookup paths and avoid binary duplication for Purwa
    install -d ${D}${FW_QCOM_BASE_PATH}/x1p42100
    ln -sf ../${FW_QCOM_NAME}/CAMERA_ICP.mbn${@fw_compr_file_suffix(d)} ${D}${FW_QCOM_BASE_PATH}/x1p42100/
}

PACKAGE_BEFORE_PN += "camxfirmware-purwa"
FILES:camxfirmware-purwa = "${FW_QCOM_BASE_PATH}/x1p42100"
