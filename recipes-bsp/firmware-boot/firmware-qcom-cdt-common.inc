LICENSE = "BSD-3-Clause"
LIC_FILES_CHKSUM = "file://${COREBASE}/meta/files/common-licenses/BSD-3-Clause;md5=550794465ba0ec5312d6919e203a55f9"

inherit allarch

CDT_ARTIFACTORY = "artifacts.codelinaro.org/artifactory/codelinaro-le/Qualcomm_Linux"

S = "${UNPACKDIR}"

QCOM_CDT_SUBDIR ?= "${QCOM_BOOT_FILES_SUBDIR}"

INHIBIT_DEFAULT_DEPS = "1"

do_configure[noexec] = "1"
do_compile[noexec] = "1"

inherit deploy

# @description Deploy every CDT binary found under ${UNPACKDIR} to ${DEPLOYDIR}/${QCOM_CDT_SUBDIR}.
# A CDT binary is any file whose name matches *cdt*.bin, ignoring case.
# @noargs
# @exitcode 0 The CDT binaries are in ${DEPLOYDIR}/${QCOM_CDT_SUBDIR}.
# @example
#   bitbake firmware-qcom-cdt-qcs6490 -c deploy
do_deploy() {
    install -d ${DEPLOYDIR}/${QCOM_CDT_SUBDIR}
    find "${UNPACKDIR}" -iname '*cdt*.bin' -exec install -m 0644 {} ${DEPLOYDIR}/${QCOM_CDT_SUBDIR} \;
}
addtask deploy before do_build after do_install
