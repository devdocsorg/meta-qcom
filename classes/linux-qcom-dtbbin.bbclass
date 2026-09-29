#
# Copyright (c) 2024 Qualcomm Innovation Center, Inc. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause-Clear
#

inherit_defer ${@bb.utils.contains('QCOM_DTB_DEFAULT', 'multi-dtb', 'dtb-fit-image', '', d)}

DTBBIN_DEPLOYDIR = "${WORKDIR}/qcom_dtbbin_deploy-${PN}"
DTBBIN_SIZE ?= "4096"

do_qcom_dtbbin_deploy[depends] += "dosfstools-native:do_populate_sysroot mtools-native:do_populate_sysroot"
do_qcom_dtbbin_deploy[cleandirs] = "${DTBBIN_DEPLOYDIR}"
# @description Put each kernel DTB in its own vfat image, dtb-<name>-image.vfat.
# DTBOs are skipped. Each image is DTBBIN_SIZE KiB and holds the DTB as combined-dtb.dtb.
# When QCOM_DTB_DEFAULT is multi-dtb, dtb-multi-dtb-image.vfat also holds qclinuxfitImage
# as qclinux_fit.img. sstate publishes ${DTBBIN_DEPLOYDIR} to ${DEPLOY_DIR_IMAGE}.
# @noargs
# @exitcode 0 The images are in ${DTBBIN_DEPLOYDIR}.
# @exitcode >0 A DTB is missing from the deploy directory, or mkfs.vfat or mcopy failed.
# @example
#   bitbake virtual/kernel -c qcom_dtbbin_deploy
do_qcom_dtbbin_deploy() {
    # Source the DTBs from what do_deploy published: unlike ${D}, which
    # only exists when do_install ran in this build, DEPLOY_DIR_IMAGE is
    # also populated when do_deploy is restored from sstate.
    deployDir="${DEPLOY_DIR_IMAGE}"
    if [ -n "${KERNEL_DEPLOYSUBDIR}" ]; then
        deployDir="${DEPLOY_DIR_IMAGE}/${KERNEL_DEPLOYSUBDIR}"
    fi

    for dtbf in ${KERNEL_DEVICETREE}; do
        bbdebug 1 " combining: $dtbf"
        dtb=`normalize_dtb "$dtbf"`
        dtb_ext=${dtb##*.}
        # Skip DTBOs
        [ "$dtb_ext" = "dtbo" ] && continue
        dtb_base_name=`basename $dtb .$dtb_ext`
        mkdir -p ${DTBBIN_DEPLOYDIR}/$dtb_base_name
        cp $deployDir/$dtb_base_name.dtb ${DTBBIN_DEPLOYDIR}/$dtb_base_name/combined-dtb.dtb
        mkfs.vfat -S ${QCOM_VFAT_SECTOR_SIZE} -C ${DTBBIN_DEPLOYDIR}/dtb-${dtb_base_name}-image.vfat ${DTBBIN_SIZE}
        mcopy -i "${DTBBIN_DEPLOYDIR}/dtb-${dtb_base_name}-image.vfat" -vsmpQ ${DTBBIN_DEPLOYDIR}/$dtb_base_name/* ::/
        rm -rf ${DTBBIN_DEPLOYDIR}/$dtb_base_name
    done

    if ${@bb.utils.contains('QCOM_DTB_DEFAULT', 'multi-dtb', 'true', 'false', d)}; then
        # Generate an image with qclinuxfitImage (multi-dtb image) alongside individual DTB images.
        mkfs.vfat -S ${QCOM_VFAT_SECTOR_SIZE} -C ${DTBBIN_DEPLOYDIR}/dtb-multi-dtb-image.vfat ${DTBBIN_SIZE}
        mcopy -i "${DTBBIN_DEPLOYDIR}/dtb-multi-dtb-image.vfat" -vsmpQ ${DEPLOY_DIR_IMAGE}/qclinuxfitImage ::/qclinux_fit.img
    fi
}
addtask qcom_dtbbin_deploy after do_deploy before do_build

# Setup sstate, see deploy.bbclass
SSTATETASKS += "do_qcom_dtbbin_deploy"
do_qcom_dtbbin_deploy[sstate-inputdirs] = "${DTBBIN_DEPLOYDIR}"
do_qcom_dtbbin_deploy[sstate-outputdirs] = "${DEPLOY_DIR_IMAGE}"

# Restore the output of do_qcom_dtbbin_deploy from the shared state cache.
#
# Example:
#     BitBake runs it in place of do_qcom_dtbbin_deploy when sstate holds the output:
#     ``bitbake virtual/kernel -c qcom_dtbbin_deploy``
python do_qcom_dtbbin_deploy_setscene () {
    sstate_setscene(d)
}
addtask do_qcom_dtbbin_deploy_setscene

do_qcom_dtbbin_deploy[stamp-extra-info] = "${MACHINE_ARCH}"
