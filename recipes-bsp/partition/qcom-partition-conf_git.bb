SUMMARY = "Partition configuration for Qualcomm devices"
DESCRIPTION = "GPT partition binaries and QDL scripts for Qualcomm reference devices"

require qcom-ptool.inc

DEPENDS = "qcom-ptool-native"

inherit deploy allarch

do_install[noexec] = "1"

# @description Deploy the GPT binaries, programming and patch XML files, zero images,
#   and optional `contents.xml` of every platform that qcom-ptool generated
#   to `partitions/` in the deploy directory, keeping each platform's subdirectory.
# @noargs
# @exitcode 0 The partition files are in `DEPLOYDIR`.
# @exitcode >0 An expected file is missing or a copy failed; BitBake stops the task.
# @example
#   bitbake -c deploy qcom-partition-conf
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
