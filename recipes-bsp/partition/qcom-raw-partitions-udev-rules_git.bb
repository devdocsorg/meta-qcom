SUMMARY = "udev rules for Qualcomm raw partitions"
DESCRIPTION = "udev rules that skip filesystem probing for known Qualcomm raw GPT partitions"

require qcom-ptool.inc

DEPENDS = "qcom-ptool-native"

inherit allarch

QCOM_RAW_PARTITIONS_RULES = "${B}/55-qcom-raw-partitions-noblkid.rules"

# @description Generate udev rules that skip filesystem probing of known Qualcomm raw partitions.
# qcom-ptool gen_udev_rules writes them to ${QCOM_RAW_PARTITIONS_RULES}.
# @noargs
# @exitcode 0 ${QCOM_RAW_PARTITIONS_RULES} exists.
# @example
#   bitbake qcom-raw-partitions-udev-rules -c compile
do_compile() {
    cd ${S}
    ${STAGING_BINDIR_NATIVE}/qcom-ptool gen_udev_rules \
        --output ${QCOM_RAW_PARTITIONS_RULES}
}

# @description Install the generated raw partition udev rules into ${nonarch_libdir}/udev/rules.d.
# @noargs
# @exitcode 0 55-qcom-raw-partitions-noblkid.rules is under ${D}.
# @example
#   bitbake qcom-raw-partitions-udev-rules -c install
do_install() {
    install -Dm 0644 ${QCOM_RAW_PARTITIONS_RULES} \
        ${D}${nonarch_libdir}/udev/rules.d/55-qcom-raw-partitions-noblkid.rules
}

FILES:${PN} = " \
    ${nonarch_libdir}/udev/rules.d/55-qcom-raw-partitions-noblkid.rules \
"
