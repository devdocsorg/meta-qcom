#
# Copyright (c) 2015-2023 Linaro
# Copyright (c) 2016 Matt Madison <matt@madison.systems>
# Copyright (c) 2017 Artur Mądrzak <artur@madrzak.eu>
# Copyright (c) 2024 Ola Jeppsson <ola@snap.com>
# Copyright (c) 2024 Qualcomm Innovation Center, Inc.
#
# SPDX-License-Identifier: MIT
#

QIMG_DEPLOYDIR = "${WORKDIR}/qcom_deploy-${PN}"

# Define INITRAMFS_IMAGE to create kernel+initramfs Android boot images in
# addition to default boot images. For example add the following line to your
# conf/local.conf:
#
# INITRAMFS_IMAGE = "initramfs-kerneltest-image"
#

# Add the initramfs and external device tree dependencies of do_qcom_img_deploy.
#
# When ``PREFERRED_PROVIDER_virtual/dtb`` is set, it also points ``EXTERNAL_KERNEL_DEVICETREE``
# at the provider's device trees in the recipe sysroot.
#
# Args:
#     d (bb.data_smart.DataSmart): The recipe datastore.
#
# Returns:
#     None
#
# Example:
#     ``bitbake virtual/kernel``
python __anonymous () {
    if d.getVar('INITRAMFS_IMAGE') != '':
        d.appendVarFlag('do_qcom_img_deploy', 'depends', ' ${INITRAMFS_IMAGE}:do_image_complete')

    providerdtb = d.getVar("PREFERRED_PROVIDER_virtual/dtb")
    if providerdtb:
        d.appendVarFlag('do_qcom_img_deploy', 'depends', ' virtual/dtb:do_populate_sysroot')
        d.setVar('EXTERNAL_KERNEL_DEVICETREE', "${RECIPE_SYSROOT}/boot/devicetree")
}

# @function do_qcom_img_deploy.make_dtb_image
# Build the boot images for one device tree, including SD card and initramfs variants when configured.
#
# Args:
#     dtbf (str): Device tree path from ``KERNEL_DEVICETREE`` or ``QCOM_BOOTIMG_DEVICETREE``.
#     external (bool): True for a device tree from ``EXTERNAL_KERNEL_DEVICETREE``.
#
# Returns:
#     None
#
# Raises:
#     bb.BBHandledException: ``QCOM_BOOTIMG_ROOTFS`` is undefined.
#
# Example:
#     ``make_dtb_image("qcom/qcs6490-rb3gen2.dtb")``

# @function do_qcom_img_deploy.make_dtb_image.getVarDTB
# Return a variable's per-DTB flag value, or the variable itself when the flag is unset.
#
# Args:
#     name (str): Variable name, such as ``QCOM_BOOTIMG_PAGE_SIZE``.
#
# Returns:
#     str: The value for the current device tree.
#
# Example:
#     ``getVarDTB("QCOM_BOOTIMG_ROOTFS")``

# @function do_qcom_img_deploy.make_dtb_image.make_image_internal
# Run mkbootimg for one image and point its link name at it.
#
# Args:
#     output (str): Image path.
#     output_link (str): Link path.
#     rootfs (str): Root device for the command line, or "" for none.
#     initrd (str): Ramdisk path; defaults to the placeholder initrd.
#
# Returns:
#     None
#
# Raises:
#     subprocess.CalledProcessError: mkbootimg failed.
#
# Example:
#     ``make_image_internal(output, output_link, "/dev/sda1")``

# @function do_qcom_img_deploy.make_dtb_image.make_image
# Build a boot image named from a template, the device tree, and the kernel image name.
#
# Args:
#     template (str): File name template with device tree and kernel name fields.
#     rootfs (str): Root device for the command line.
#
# Returns:
#     str: The image path.
#
# Example:
#     ``make_image("boot-%s-%s.img", rootfs)``

# @function do_qcom_img_deploy.make_dtb_image.make_initramfs_image
# Build a boot image that carries the initramfs, and link it under an initramfs name.
#
# Args:
#     template (str): File name template with initramfs, device tree, and kernel name fields.
#     rootfs (str): Root device for the command line.
#     initrd (str): Initramfs path.
#     initrd_image_name (str): Initramfs image name used in the file name.
#
# Returns:
#     str: The image path.
#
# Example:
#     ``make_initramfs_image("boot-%s-%s-%s.img", rootfs, initrd, "initramfs-kerneltest-image")``

# Build Android boot images for each device tree with skales mkbootimg.
#
# Each image holds the kernel with an appended DTB, a placeholder or ``INITRAMFS_IMAGE``
# ramdisk, and the command line built from ``SERIAL_CONSOLES``, ``QCOM_BOOTIMG_ROOTFS``,
# and ``KERNEL_CMDLINE_EXTRA``.
#
# Args:
#     d (bb.data_smart.DataSmart): The recipe datastore.
#
# Returns:
#     None: Images and links are written to ``QIMG_DEPLOYDIR``.
#
# Raises:
#     bb.BBHandledException: The initramfs image, ARCH, root file system, or device tree settings are missing or unsupported.
#
# Example:
#     ``bitbake -c qcom_img_deploy virtual/kernel``
python do_qcom_img_deploy() {
    import shutil
    import subprocess

    subdir = d.getVar("KERNEL_DEPLOYSUBDIR")
    if subdir is not None:
        qcom_deploy_dir = os.path.join(d.getVar("QIMG_DEPLOYDIR"), subdir)
        image_dir = os.path.join(d.getVar("DEPLOY_DIR_IMAGE"), subdir)
    else:
        qcom_deploy_dir = d.getVar("QIMG_DEPLOYDIR")
        image_dir = d.getVar("DEPLOY_DIR_IMAGE")

    initrd = None
    if d.getVar('INITRAMFS_IMAGE') != '':
        initrd_image_name = d.getVar("INITRAMFS_IMAGE_NAME")
        baseinitrd = os.path.join(d.getVar("DEPLOY_DIR_IMAGE"), initrd_image_name)
        for img in (".cpio.gz", ".cpio.lz4", ".cpio.lzo", ".cpio.lzma", ".cpio.xz", ".cpio"):
            if os.path.exists(baseinitrd + img):
                initrd = baseinitrd + img
                break
        if not initrd:
            bb.fatal("Could not find initramfs image %s for bundling" % d.getVar("INITRAMFS_IMAGE"))

    workdir = d.getVar("WORKDIR")
    kernel = os.path.join(workdir, "kernel-dtb")
    definitrd = os.path.join(workdir, "initrd.img")
    external_dtbdir = d.getVar("EXTERNAL_KERNEL_DEVICETREE")
    mkbootimg = os.path.join(d.getVar("STAGING_BINDIR_NATIVE"), "skales", "mkbootimg")
    kernel_image_name = d.getVar("KERNEL_IMAGE_NAME")
    kernel_link_name = d.getVar("KERNEL_IMAGE_LINK_NAME")
    output_img =  os.path.join(qcom_deploy_dir, "boot-%s.img" % (kernel_link_name))
    output_sd_img =  os.path.join(qcom_deploy_dir, "boot-sd-%s.img" % (kernel_link_name))

    arch = d.getVar("ARCH")
    if arch == "arm":
        kernel_name = "zImage"
    elif arch == "arm64":
        kernel_name = "Image.gz"
    else:
        bb.fatal("Unuspported ARCH %s" % arch)

    # Consume the kernel image and DTBs published by do_deploy: unlike
    # ${B} and ${D}, DEPLOY_DIR_IMAGE is also populated when do_deploy
    # is restored from sstate.
    kernel_src = os.path.join(image_dir, kernel_name)

    if os.path.exists(output_img):
        os.unlink(output_img)
    if os.path.exists(output_sd_img):
        os.unlink(output_sd_img)

    with open(definitrd, "w") as f:
        f.write("This is not an initrd\n")

    def make_dtb_image(dtbf, external=False):
        dtb = os.path.basename(dtbf)
        dtb_name = dtb.rsplit('.', 1)[0]

        def getVarDTB(name):
            var = d.getVarFlag(name, dtb_name)
            return d.getVar(name) if var is None else var

        def make_image_internal(output, output_link, rootfs, initrd = definitrd):
            rootfs_cmdline = "root=%s " % (rootfs) if rootfs else ""
            subprocess.check_call([mkbootimg,
                "--kernel", kernel,
                "--ramdisk", initrd,
                "--output", output,
                "--pagesize", getVarDTB("QCOM_BOOTIMG_PAGE_SIZE"),
                "--base", getVarDTB("QCOM_BOOTIMG_KERNEL_BASE"),
                "--cmdline", "%srw rootwait %s %s" % (rootfs_cmdline, consoles, getVarDTB("KERNEL_CMDLINE_EXTRA") or "")])
            if os.path.exists(output_link):
                os.unlink(output_link)
            os.symlink(os.path.basename(output), output_link)

        def make_image(template, rootfs):
            output = os.path.join(qcom_deploy_dir, template % (dtb_name, kernel_image_name))
            output_link =  os.path.join(qcom_deploy_dir, template % (dtb_name, kernel_link_name))
            make_image_internal(output, output_link, rootfs)
            return output

        def make_initramfs_image(template, rootfs, initrd, initrd_image_name):
            output = os.path.join(qcom_deploy_dir, template % (initrd_image_name, dtb_name, kernel_image_name))
            output_link =  os.path.join(qcom_deploy_dir, template % (initrd_image_name, dtb_name, kernel_link_name))
            make_image_internal(output, output_link, rootfs, initrd)
            output_link =  os.path.join(qcom_deploy_dir, template % ("initramfs", dtb_name, kernel_link_name))
            if os.path.exists(output_link):
                os.unlink(output_link)
            os.symlink(os.path.basename(output), output_link)
            return output

        consoles = ' '.join(map(lambda c: "console=%(tty)s,%(rate)sn8" % dict(zip(("rate", "tty"), c.split(';'))), getVarDTB("SERIAL_CONSOLES").split()))

        # prepare kernel image with appended dtb
        dtbdir = external_dtbdir if external else image_dir
        with open(kernel, 'wb') as wfd:
            with open(kernel_src, 'rb') as rfd:
                shutil.copyfileobj(rfd, wfd)
            with open(os.path.join(dtbdir, dtb), 'rb') as rfd:
                shutil.copyfileobj(rfd, wfd)

        rootfs = getVarDTB("QCOM_BOOTIMG_ROOTFS")
        if rootfs is None:
            bb.fatal("QCOM_BOOTIMG_ROOTFS is undefined")

        template = "boot-%s-%s-ext-dtb.img" if external else "boot-%s-%s.img"
        output = make_image(template, rootfs)
        if not os.path.exists(output_img):
            os.symlink(os.path.basename(output), output_img)

        if initrd:
            template = "boot-%s-%s-%s-ext-dtb.img" if external else "boot-%s-%s-%s.img"
            make_initramfs_image(template, rootfs, initrd, d.getVar("INITRAMFS_IMAGE"))

        sd_rootfs = getVarDTB("SD_QCOM_BOOTIMG_ROOTFS")
        if sd_rootfs:
            template = "boot-sd-%s-%s-ext-dtb.img" if external else "boot-sd-%s-%s.img"
            output = make_image(template, sd_rootfs)
            if not os.path.exists(output_sd_img):
                os.symlink(os.path.basename(output), output_sd_img)

            if initrd:
                template = "boot-sd-%s-%s-%s-ext-dtb.img" if external else "boot-sd-%s-%s-%s.img"
                make_initramfs_image(template, rootfs, initrd, d.getVar("INITRAMFS_IMAGE"))

    if not d.getVar("QCOM_BOOTIMG_DEVICETREE") and not d.getVar("KERNEL_DEVICETREE"):
        bb.fatal("Either QCOM_BOOTIMG_DEVICETREE or KERNEL_DEVICETREE needed for linux-qcom-bootimg.bbclass")

    if d.getVar("KERNEL_DEVICETREE"):
        for dtbf in d.getVar("KERNEL_DEVICETREE").split():
            make_dtb_image(dtbf)

    if d.getVar("QCOM_BOOTIMG_DEVICETREE") and not external_dtbdir:
        bb.fatal("QCOM_BOOTIMG_DEVICETREE requires PREFERRED_PROVIDER_virtual/dtb to be set")

    if d.getVar("QCOM_BOOTIMG_DEVICETREE"):
        for dtbf in d.getVar("QCOM_BOOTIMG_DEVICETREE").split():
            make_dtb_image(dtbf, external=True)
}

do_qcom_img_deploy[depends] += "skales-native:do_populate_sysroot"
do_qcom_img_deploy[vardeps] = "QCOM_BOOTIMG_PAGE_SIZE QCOM_BOOTIMG_KERNEL_BASE KERNEL_CMDLINE_EXTRA QCOM_BOOTIMG_ROOTFS"

addtask qcom_img_deploy after do_deploy before do_build

# Setup sstate, see deploy.bbclass
SSTATETASKS += "do_qcom_img_deploy"
do_qcom_img_deploy[sstate-inputdirs] = "${QIMG_DEPLOYDIR}"
do_qcom_img_deploy[sstate-outputdirs] = "${DEPLOY_DIR_IMAGE}"

# Restore the boot images from the shared state cache.
#
# Args:
#     d (bb.data_smart.DataSmart): The recipe datastore.
#
# Returns:
#     None: The cached images are placed in ``DEPLOY_DIR_IMAGE``.
#
# Example:
#     ``bitbake -c qcom_img_deploy_setscene virtual/kernel``
python do_qcom_img_deploy_setscene () {
    sstate_setscene(d)
}
addtask do_qcom_img_deploy_setscene
do_qcom_img_deploy[dirs] = "${QIMG_DEPLOYDIR}"
do_qcom_img_deploy[cleandirs] = "${QIMG_DEPLOYDIR}"
do_qcom_img_deploy[stamp-extra-info] = "${MACHINE_ARCH}"

# We do not need kernel image in /boot, these images are flashed into separate partition.
RDEPENDS:${KERNEL_PACKAGE_NAME}-base = ""
