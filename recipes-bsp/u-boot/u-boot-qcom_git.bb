require recipes-bsp/u-boot/u-boot-common.inc
require recipes-bsp/u-boot/u-boot.inc

DEPENDS += "bc-native dtc-native gnutls-native python3-pyelftools-native qtestsign-native xxd-native"

QCOM_UBOOT_SPL_FIT ?= "0"
QCOM_UBOOT_SPL_FIT_ATF ?= ""
QCOM_UBOOT_SPL_FIT_TEE ?= ""

# BL31 and OP-TEE go into the FIT, swiv annotates the SPL before signing.
DEPENDS += "${@bb.utils.contains('QCOM_UBOOT_SPL_FIT', '1', '${QCOM_UBOOT_SPL_FIT_ATF} ${QCOM_UBOOT_SPL_FIT_TEE} swiv-build-utility-native', '', d)}"

COMPATIBLE_MACHINE:aarch64 = "(qcom)"

PV = "2026.07+2026.10-rc1+git"

# tag: qcom-next-v2026.10-rc1-20260915
SRCREV = "5ec66cb5c3f29e2da1f55464109cae3fe8545b69"
SRCBRANCH = "nobranch=1"

SRC_URI = "git://github.com/qualcomm-linux/u-boot.git;${SRCBRANCH};protocol=https;name=uboot"
SRC_URI += " \
    file://0001-Add-support-for-OpenSSL-Provider-API.patch \
    file://disable-eficapsule-tool.cfg \
    file://efi-rt-volatile-store.cfg \
    ${@bb.utils.contains('MACHINE_FEATURES', 'optee', 'file://tfa-optee.cfg', '', d)} \
    ${@bb.utils.contains('MACHINE_FEATURES', 'kvm', 'file://gunyah-exit.cfg', '', d)} \
    ${@bb.utils.contains('SPL_SIGN_ENABLE', '1', 'file://spl-fit-signature.cfg', '', d)} \
"

# Build BOARD_MBN_HEADER as a "?"-separated list with one MBN header version per UBOOT_CONFIG.
#
# Each value comes from the BOARD_MBN_HEADER[<config>] flag, or is empty when the flag is not
# set, so uboot_config_get_indexed_value can look it up by the configuration's index.
#
# Example:
#     With UBOOT_CONFIG = "qcs6490-rb3gen2", parsing ``bitbake u-boot-qcom`` sets
#     BOARD_MBN_HEADER to "v6 ? ".
python __anonymous() {
    ubootconfig = (d.getVar('UBOOT_CONFIG') or "").split()

    if len(ubootconfig) > 0:
        for config in ubootconfig:
            # Get the MBN header version for this specific config
            mbn_header = d.getVarFlag('BOARD_MBN_HEADER', config)

            if not mbn_header:
                mbn_header = ""

            d.appendVar('BOARD_MBN_HEADER', mbn_header + " ? ")
}

# @description Stage the FIT inputs or sign u-boot.elf for one built U-Boot configuration.
# With QCOM_UBOOT_SPL_FIT = "1", bl31.bin and tee-raw.bin are copied into the build directory for
# the FIT; otherwise, when the configuration has an MBN header version, qtestsign signs
# u-boot.elf as u-boot.mbn.
# @arg $1 int Index of the configuration in UBOOT_MACHINE and UBOOT_CONFIG.
# @arg $2 string U-Boot defconfig name, from UBOOT_MACHINE.
# @arg $3 string Configuration name, from UBOOT_CONFIG.
# @exitcode 0 The FIT inputs or u-boot.mbn are in the build directory, or nothing was needed.
# @example
#   uboot_compile_config $i $config $type
uboot_compile_config:append() {
    config_mbn_header=$(uboot_config_get_indexed_value "${BOARD_MBN_HEADER}" $i)

    if [ "${QCOM_UBOOT_SPL_FIT}" = "1" ]; then
        # Where uboot-sign's /incbin/ defaults expect them.
        install -m 0644 ${RECIPE_SYSROOT}/firmware/${QCOM_UBOOT_SPL_FIT_ATF}/bl31.bin ${B}/${builddir}/bl31.bin
        install -m 0644 ${RECIPE_SYSROOT}${nonarch_base_libdir}/firmware/tee-raw.bin ${B}/${builddir}/tee-raw.bin
    elif [ -n "${config_mbn_header}" ]; then
        export CRYPTOGRAPHY_OPENSSL_NO_LEGACY=1
        qtestsign -${config_mbn_header} aboot -o ${B}/${builddir}/u-boot.mbn ${B}/${builddir}/u-boot.elf
    fi
}

# @description Build the signed SPL image u-boot-spl.mbn when QCOM_UBOOT_SPL_FIT is "1".
# Rebuild the SPL ELF after uboot-sign, add the SWIV segment and sign it as TZ.
# @arg $1 string Configuration name from UBOOT_CONFIG, or empty without UBOOT_CONFIG.
# @arg $2 string Name of the U-Boot binary for the configuration.
# @exitcode 0 u-boot-spl.mbn is in the build directory, or QCOM_UBOOT_SPL_FIT is not "1".
# @example
#   uboot_assemble_fitimage_helper ${type} ${config_binary}
uboot_assemble_fitimage_helper:append() {
    if [ "${QCOM_UBOOT_SPL_FIT}" = "1" ]; then
        mbn_header=$(uboot_config_get_indexed_value "${BOARD_MBN_HEADER}" $i)
        [ -n "${mbn_header}" ] || mbn_header="v6"

        rm -f spl/u-boot-spl.elf
        (unset LDFLAGS CFLAGS; oe_runmake -C ${S} O=${B}/${builddir} ${UBOOT_MAKE_OPTS} spl/u-boot-spl.elf)

        export CRYPTOGRAPHY_OPENSSL_NO_LEGACY=1
        swiv_build_utility u-boot-spl-swiv.elf spl/u-boot-spl.elf ${QCOM_UBOOT_SPL_SWIV_PLATFORM}
        qtestsign -${mbn_header} tz -o u-boot-spl.mbn u-boot-spl-swiv.elf
        rm -f u-boot-spl-swiv.elf
    fi
}

# @description Deploy the signed MBN image of one U-Boot configuration when it was built.
# With QCOM_UBOOT_SPL_FIT = "1" this is u-boot-spl.mbn, deployed as u-boot-spl-<type>.mbn;
# otherwise u-boot.mbn is deployed as u-boot-<type>.mbn.
# @arg $1 string U-Boot defconfig name, from UBOOT_MACHINE.
# @arg $2 string Configuration name, from UBOOT_CONFIG.
# @exitcode 0 The MBN image is in ${DEPLOYDIR}, or none was built.
# @example
#   uboot_deploy_config $config $type
uboot_deploy_config:append() {
    if [ "${QCOM_UBOOT_SPL_FIT}" = "1" ]; then
        if [ -f ${B}/${builddir}/u-boot-spl.mbn ]; then
            install -m 0644 ${B}/${builddir}/u-boot-spl.mbn ${DEPLOYDIR}/u-boot-spl-${type}.mbn
        fi
    elif [ -f ${B}/${builddir}/u-boot.mbn ]; then
        install -m 0644 ${B}/${builddir}/u-boot.mbn ${DEPLOYDIR}/u-boot-${type}.mbn
    fi
}
