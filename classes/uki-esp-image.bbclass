# Create an ESP image that has a type #2 EFI UKI and systemd-boot
#
# Copyright (c) 2025 Qualcomm Innovation Center, Inc.
#
# SPDX-License-Identifier: MIT
#

# Optional subfolder, dependant on where the ESP partition gets mounted
# intended to only have a leading slash, no trailing slash e.g. '/EFI', or just empty, ''
ESPFOLDER ?= "/EFI"

# @description Copy the unified kernel image (`UKI_FILENAME`) from the deploy
#   directory into `EFI/Linux` under `ESPFOLDER` in the image root filesystem.
# @noargs
# @exitcode 0 The UKI is in the root filesystem's ESP folder.
# @exitcode >0 The directory or install command failed; BitBake stops the task.
# @example
#   bitbake -c ukiesp esp-qcom-image
do_ukiesp() {
	mkdir -p ${IMAGE_ROOTFS}${ESPFOLDER}/EFI/Linux

	# Copy over files from deploy into the rootfs
	install -m 0755 ${DEPLOY_DIR_IMAGE}/${UKI_FILENAME} ${IMAGE_ROOTFS}${ESPFOLDER}/EFI/Linux
}

addtask ukiesp after do_rootfs uki before do_image
