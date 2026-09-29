# This is a bbappend to add support for generating Android style boot images for chainloading u-boot from ABL

DEPENDS:append:qcom = " skales-native xxd-native"

# Don't add extra dependencies for non-qcom machines and layers
COMPILE_EXTRA_DEPENDS = ""
COMPILE_EXTRA_DEPENDS:qcom = "virtual/kernel:do_deploy"
do_compile[depends] += "${COMPILE_EXTRA_DEPENDS}"

# @description Wrap the gzip-compressed U-Boot and the configuration's DTB in an Android boot image, u-boot-<type>.bin.
# @arg $1 integer Index of the configuration in UBOOT_CONFIG.
# @arg $2 string U-Boot configuration name.
# @arg $3 string Configuration type.
# @exitcode 0 The function finished; any failing command fails the calling task.
# @example
#   uboot_compile_config 1 qcm6490_defconfig qcs6490-rb3gen2
uboot_compile_config:append:qcom() {
    cd ${B}/${builddir}
    touch empty-file
    rm -f u-boot-nodtb.bin.gz
    gzip -k u-boot-nodtb.bin
    cat u-boot-nodtb.bin.gz ${DEPLOY_DIR_IMAGE}/${type}.dtb > u-boot-nodtb.bin.gz-${type}
    ${STAGING_BINDIR_NATIVE}/skales/mkbootimg --base 0x80000000 --pagesize 4096 --kernel u-boot-nodtb.bin.gz-${type} --cmdline "root=/dev/notreal" --ramdisk empty-file --output u-boot-${type}.bin
}

# @description Symlink the 'main' u-boot.bin to boot.img so the qcom image bbclass pick it up
# @arg $1 string U-Boot configuration name.
# @arg $2 string Configuration type.
# @exitcode 0 The function finished; any failing command fails the calling task.
# @example
#   uboot_deploy_config qcm6490_defconfig qcs6490-rb3gen2
uboot_deploy_config:append:qcom() {
    if [ "${@d.getVar('PREFERRED_PROVIDER_virtual/bootloader')}" = "${PN}" ] ; then
        cd ${DEPLOYDIR} && ln -sf u-boot-${type}-${PV}-${PR}.bin boot-${MACHINE}.img
    fi
}
