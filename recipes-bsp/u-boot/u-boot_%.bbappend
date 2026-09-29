# This is a bbappend to add support for generating Android style boot images for chainloading u-boot from ABL

DEPENDS:append:qcom = " skales-native xxd-native"

# Don't add extra dependencies for non-qcom machines and layers
COMPILE_EXTRA_DEPENDS = ""
COMPILE_EXTRA_DEPENDS:qcom = "virtual/kernel:do_deploy"
do_compile[depends] += "${COMPILE_EXTRA_DEPENDS}"

# @description Wrap the U-Boot binary of one configuration in an Android boot image for ABL.
# u-boot-nodtb.bin is gzipped, the <type>.dtb from ${DEPLOY_DIR_IMAGE} is appended, and skales
# mkbootimg writes the result, with an empty ramdisk, as u-boot-<type>.bin.
# @arg $1 int Index of the configuration in UBOOT_MACHINE and UBOOT_CONFIG.
# @arg $2 string U-Boot defconfig name, from UBOOT_MACHINE.
# @arg $3 string Configuration name, from UBOOT_CONFIG; also the name of the device tree.
# @exitcode 0 u-boot-<type>.bin in the build directory is the Android boot image.
# @example
#   uboot_compile_config $i $config $type
uboot_compile_config:append:qcom() {
    cd ${B}/${builddir}
    touch empty-file
    rm -f u-boot-nodtb.bin.gz
    gzip -k u-boot-nodtb.bin
    cat u-boot-nodtb.bin.gz ${DEPLOY_DIR_IMAGE}/${type}.dtb > u-boot-nodtb.bin.gz-${type}
    ${STAGING_BINDIR_NATIVE}/skales/mkbootimg --base 0x80000000 --pagesize 4096 --kernel u-boot-nodtb.bin.gz-${type} --cmdline "root=/dev/notreal" --ramdisk empty-file --output u-boot-${type}.bin
}

# @description Link boot-${MACHINE}.img to the deployed U-Boot image when PN is the bootloader.
# Symlink the 'main' u-boot.bin to boot.img so the qcom image bbclass pick it up
# @arg $1 string U-Boot defconfig name, from UBOOT_MACHINE.
# @arg $2 string Configuration name, from UBOOT_CONFIG.
# @exitcode 0 The link exists, or PN is not the preferred virtual/bootloader provider.
# @example
#   uboot_deploy_config $config $type
uboot_deploy_config:append:qcom() {
    if [ "${@d.getVar('PREFERRED_PROVIDER_virtual/bootloader')}" = "${PN}" ] ; then
        cd ${DEPLOYDIR} && ln -sf u-boot-${type}-${PV}-${PR}.bin boot-${MACHINE}.img
    fi
}
