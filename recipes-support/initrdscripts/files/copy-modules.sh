#!/bin/sh
# Copyright (C) 2022 Linaro Ltd.
# SPDX-License-Identifier: MIT

# @description Report whether the copy_modules boot parameter is set and the running kernel's modules exist.
# @noargs
# @exitcode 0 The module should run.
# @exitcode 1 The parameter is unset or the modules folder is missing.
# @example
#   copy_modules_enabled && copy_modules_run
copy_modules_enabled() {
	[ -n "${bootparam_copy_modules}" -a -d /lib/modules/`uname -r` ]
}

# @description Replace the root filesystem's modules for the running kernel with the initramfs copy.
# @noargs
# @exitcode 0 The modules are copied, or ROOTFS_DIR is unset and nothing is copied.
# @example
#   copy_modules_run
copy_modules_run() {
	if [ -n "$ROOTFS_DIR" ]; then
		rm -rf $ROOTFS_DIR/lib/modules/`uname -r`
		mkdir -p $ROOTFS_DIR/lib/modules
		cp -a /lib/modules/`uname -r` $ROOTFS_DIR/lib/modules
	else
		debug "No rootfs has been set"
	fi
}
