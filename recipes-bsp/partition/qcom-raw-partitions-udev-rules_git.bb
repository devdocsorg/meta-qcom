SUMMARY = "udev rules for Qualcomm raw partitions"
DESCRIPTION = "udev rules that skip filesystem probing for known Qualcomm raw GPT partitions"

require qcom-ptool.inc

DEPENDS = "qcom-ptool-native"

inherit allarch

QCOM_RAW_PARTITIONS_RULES = "${B}/55-qcom-raw-partitions-noblkid.rules"

# @description Generate the udev rules that skip filesystem probing on Qualcomm raw
#   partitions with `qcom-ptool gen_udev_rules`.
# @noargs
# @exitcode 0 The rules file is in the build directory.
# @exitcode >0 qcom-ptool failed; BitBake stops the task.
# @example
#   bitbake -c compile qcom-raw-partitions-udev-rules
do_compile() {
    cd ${S}
    ${STAGING_BINDIR_NATIVE}/qcom-ptool gen_udev_rules \
        --output ${QCOM_RAW_PARTITIONS_RULES}
}

# @description Install the generated `55-qcom-raw-partitions-noblkid.rules` into the
#   udev rules directory.
# @noargs
# @exitcode 0 The rules file is in the install directory.
# @exitcode >0 The install command failed; BitBake stops the task.
# @example
#   bitbake -c install qcom-raw-partitions-udev-rules
do_install() {
    install -Dm 0644 ${QCOM_RAW_PARTITIONS_RULES} \
        ${D}${nonarch_libdir}/udev/rules.d/55-qcom-raw-partitions-noblkid.rules
}

FILES:${PN} = " \
    ${nonarch_libdir}/udev/rules.d/55-qcom-raw-partitions-noblkid.rules \
"
