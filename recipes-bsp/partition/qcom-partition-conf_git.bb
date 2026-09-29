SUMMARY = "Partition configuration for Qualcomm devices"
DESCRIPTION = "GPT partition binaries and QDL scripts for Qualcomm reference devices"

require qcom-ptool.inc

DEPENDS = "qcom-ptool-native"

inherit deploy allarch

do_install[noexec] = "1"

# @description Deploy the partition tables and flashing XML files of each platform.
# Every directory under ${S}/platforms that holds gpt_main0.bin is a platform; its GPT, zeros,
# patch, rawprogram, and wipe files, and contents.xml when present, go to
# ${DEPLOYDIR}/partitions/<platform directory>.
# @noargs
# @exitcode 0 The partition files are in ${DEPLOYDIR}/partitions.
# @example
#   bitbake qcom-partition-conf -c deploy
do_deploy() {
    cd ${S}/platforms
    for gpt in `find . -name gpt_main0.bin` ; do
        QCOM_PLATFORM_SUBDIR=${gpt%%/gpt_main0.bin}
        install -d ${DEPLOYDIR}/partitions/${QCOM_PLATFORM_SUBDIR}
        install -m 0644 ${QCOM_PLATFORM_SUBDIR}/gpt_backup*.bin -D ${DEPLOYDIR}/partitions/${QCOM_PLATFORM_SUBDIR}
        install -m 0644 ${QCOM_PLATFORM_SUBDIR}/gpt_both*.bin -D ${DEPLOYDIR}/partitions/${QCOM_PLATFORM_SUBDIR}
        install -m 0644 ${QCOM_PLATFORM_SUBDIR}/gpt_empty*.bin -D ${DEPLOYDIR}/partitions/${QCOM_PLATFORM_SUBDIR}
        install -m 0644 ${QCOM_PLATFORM_SUBDIR}/gpt_main*.bin -D ${DEPLOYDIR}/partitions/${QCOM_PLATFORM_SUBDIR}
        install -m 0644 ${QCOM_PLATFORM_SUBDIR}/patch*.xml -D ${DEPLOYDIR}/partitions/${QCOM_PLATFORM_SUBDIR}
        install -m 0644 ${QCOM_PLATFORM_SUBDIR}/rawprogram*.xml -D ${DEPLOYDIR}/partitions/${QCOM_PLATFORM_SUBDIR}
        install -m 0644 ${QCOM_PLATFORM_SUBDIR}/zeros_*.bin -D ${DEPLOYDIR}/partitions/${QCOM_PLATFORM_SUBDIR}
        install -m 0644 ${QCOM_PLATFORM_SUBDIR}/wipe_rawprogram_PHY*.xml -D ${DEPLOYDIR}/partitions/${QCOM_PLATFORM_SUBDIR}
        if [ -e "${QCOM_PLATFORM_SUBDIR}/contents.xml" ]; then
            install -m 0644 ${QCOM_PLATFORM_SUBDIR}/contents.xml ${DEPLOYDIR}/partitions/${QCOM_PLATFORM_SUBDIR}
        fi
    done
}
addtask deploy before do_build after do_compile
