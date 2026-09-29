#!/bin/sh
# Copyright (C) 2022 Linaro Ltd.
# SPDX-License-Identifier: MIT

# @description Tell initramfs-framework whether to run the copy_modules module.
# It runs when the kernel command line has copy_modules and the initramfs has modules
# for the running kernel.
# @noargs
# @exitcode 0 bootparam_copy_modules is set and /lib/modules/$(uname -r) exists.
# @exitcode 1 The module is skipped.
# @example
#   copy_modules_enabled && copy_modules_run
copy_modules_enabled() {
	[ -n "${bootparam_copy_modules}" -a -d /lib/modules/`uname -r` ]
}

# @description Replace the root filesystem's modules for the running kernel with the initramfs copy.
# @noargs
# @exitcode 0 The modules are copied to $ROOTFS_DIR/lib/modules, or ROOTFS_DIR is unset.
# @example
#   copy_modules_enabled && copy_modules_run
copy_modules_run() {
	if [ -n "$ROOTFS_DIR" ]; then
		rm -rf $ROOTFS_DIR/lib/modules/`uname -r`
		mkdir -p $ROOTFS_DIR/lib/modules
		cp -a /lib/modules/`uname -r` $ROOTFS_DIR/lib/modules
	else
		debug "No rootfs has been set"
	fi
}
