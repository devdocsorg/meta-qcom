DESCRIPTION = "EFI System Partition Image with U-Boot FIT kernel for Qualcomm boards"

inherit image

# Skip the recipe unless the machine and kernel are set up for the U-Boot FIT image flow.
#
# Raises:
#     bb.parse.SkipRecipe: When neither UBOOT_MACHINE nor UBOOT_CONFIG is set, or when
#         KERNEL_CLASSES does not include kernel-fit-extra-artifacts.
#
# Example:
#     BitBake runs this while parsing the recipe: ``bitbake esp-qcom-fit-image`` with the
#     ``ci/kernel-fit-image.yml`` kas fragment enabled.
python () {
    if not (d.getVar('UBOOT_MACHINE') or d.getVar('UBOOT_CONFIG')):
        raise bb.parse.SkipRecipe("Either UBOOT_MACHINE or UBOOT_CONFIG must be set in the %s machine configuration." % d.getVar('MACHINE'))
    if 'kernel-fit-extra-artifacts' not in (d.getVar('KERNEL_CLASSES') or '').split():
        raise bb.parse.SkipRecipe("KERNEL_CLASSES must include kernel-fit-extra-artifacts; enable it via the kernel-fit-image kas fragment.")
}

require esp-qcom-common.inc

PACKAGE_INSTALL = ""

# @description Replace the image root filesystem with the FIT image and the U-Boot boot script.
# Setup boot files for FIT image-based boot
# @noargs
# @exitcode 0 The root filesystem holds only fitImage and boot.scr.
# @exitcode 1 No FIT image or no boot.scr is found in ${DEPLOY_DIR_IMAGE} (bbfatal).
# @example
#   bitbake esp-qcom-fit-image -c image
setup_fit_boot_files() {
    # Remove skeleton directories and base files created by the image class
    find ${IMAGE_ROOTFS} -mindepth 1 -maxdepth 1 -exec rm -rf {} +

    # Copy FIT image from deploy directory:
    # Prefer fit with initrd when available, otherwise fall back to the kernel fit
    fit_image="${DEPLOY_DIR_IMAGE}/fitImage"
    fit_image_initrd=""
    if [ -n "${INITRAMFS_IMAGE}" ]; then
        fit_image_initrd="${DEPLOY_DIR_IMAGE}/fitImage-${INITRAMFS_IMAGE}-${MACHINE}"
    fi

    if [ -n "${fit_image_initrd}" ] && [ -f "${fit_image_initrd}" ]; then
        bbnote "Using FIT image with initrd: ${fit_image_initrd}"
        cp ${fit_image_initrd} ${IMAGE_ROOTFS}/fitImage
    elif [ -f "${fit_image}" ]; then
        bbnote "Using FIT image: ${fit_image}"
        cp ${fit_image} ${IMAGE_ROOTFS}/fitImage
    else
        bbfatal "No FIT image found."
    fi

    # Copy U-Boot boot script from deploy directory
    if [ -f ${DEPLOY_DIR_IMAGE}/boot.scr ]; then
        cp ${DEPLOY_DIR_IMAGE}/boot.scr ${IMAGE_ROOTFS}
    else
        bbfatal "boot.scr not found in DEPLOY_DIR_IMAGE"
    fi
}

IMAGE_PREPROCESS_COMMAND:append = " setup_fit_boot_files"

# Dependencies on FIT image and boot script, used to load fit
do_image[depends] += "linux-yocto-fitimage:do_deploy u-boot-scr-qcom-fit:do_deploy"
