#
# Copyright (c) 2024 Linaro
# Copyright (c) 2024-2025 Qualcomm Innovation Center, Inc.
#
# SPDX-License-Identifier: MIT

# This class can install adbd into the target image when openembedded-layer is available.
# The adbd daemon is disabled unless IMAGE_FEATURES contains the 'enable-adbd'
# Also one can disable adbd by removing /etc/usb-debugging-enabled from rootfs manually.

IMAGE_FEATURES[validitems] += "enable-adbd"

PACKAGE_INSTALL:append = " ${@bb.utils.contains("BBFILE_COLLECTIONS", "openembedded-layer", "android-tools-adbd android-tools-adbd-cmdline", "", d)}"

# @description Create /etc/usb-debugging-enabled in the root filesystem so adbd starts at boot.
# @noargs
# @exitcode 0 The function finished; any failing command fails the calling task.
# @example
#   IMAGE_FEATURES += "enable-adbd"
#   bitbake initramfs-test-image
enable_adbd_at_boot () {
    touch ${IMAGE_ROOTFS}/etc/usb-debugging-enabled
}

ROOTFS_POSTPROCESS_COMMAND += "${@bb.utils.contains('IMAGE_FEATURES', [ 'enable-adbd' ], 'enable_adbd_at_boot; ', '',d)}"

addtask oelayer_check before do_build
do_oelayer_check[nostamp] = "1"
# Warn when an image inherits image-adbd without the meta-openembedded layer that provides adbd.
#
# Args:
#     d (bb.data_smart.DataSmart): The recipe datastore.
#
# Returns:
#     None
#
# Example:
#     ``bitbake -c oelayer_check initramfs-test-image``
python do_oelayer_check() {
    if 'openembedded-layer' not in d.getVar('BBFILE_COLLECTIONS').split():
        bb.warn("'image-adbd' is inherited but the meta-openembedded layer"
                " is not included in bblayers. ADBD may not work as expected.")
}

