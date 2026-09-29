FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"

SRC_URI:append:qcom = " \
    file://0001-Add-SELinux-policy-for-camera-nhx.patch \
    ${@bb.utils.contains('MACHINE_FEATURES', 'optee', '', 'file://0002-Enable-the-tunable-flag-tee_supplicant_qtee.patch', d)} \
    file://0003-seatd-allow-self-fifo_file-read-write-for-signal-han.patch \
    file://0004-kernel-allow-module-loaders-to-use-net_admin.patch \
"

# Space-separated policy boolean/tunable settings in name=value format.
# This is compatible with the proposed generic meta-selinux interface so the
# local hook can be removed once an equivalent upstream implementation exists.
POLICY_BOOLEANS ?= ""

# @description Write each POLICY_BOOLEANS setting into the policy's booleans.conf.
# A new "name = value" line replaces any earlier line for the same name, and the
# policy build uses these values as the boolean and tunable defaults.
# @noargs
# @exitcode 0 booleans.conf holds one line for each setting.
# @exitcode 1 bbfatal stops the build on an entry without "=", a bad name, or a bad value.
# @example
#   set_qcom_policy_booleans
set_qcom_policy_booleans() {
    touch "${S}/policy/booleans.conf"

    for setting in ${POLICY_BOOLEANS}; do
        name="${setting%%=*}"
        value="${setting#*=}"

        if [ "${name}" = "${setting}" ]; then
            bbfatal "Invalid POLICY_BOOLEANS entry: ${setting}"
        fi

        case "${name}" in
            ""|*[!A-Za-z0-9_]*)
                bbfatal "Invalid policy boolean name: ${name}"
                ;;
        esac

        case "${value}" in
            true|false) ;;
            *)
                bbfatal "Invalid value for ${name}: ${value}"
                ;;
        esac

        sed -i "/^[[:space:]]*${name}[[:space:]]*=/d" \
            "${S}/policy/booleans.conf"
        echo "${name} = ${value}" >> "${S}/policy/booleans.conf"
    done
}

# @description Apply POLICY_BOOLEANS to booleans.conf before the policy is compiled.
# @noargs
# @exitcode 0 The settings are in booleans.conf and compilation continues.
# @exitcode 1 An invalid POLICY_BOOLEANS entry stops the build.
# @example
#   bitbake refpolicy-targeted -c compile
do_compile:prepend:qcom() {
    set_qcom_policy_booleans
}

# Qualcomm platforms preload qrtr and qrtr_smd from modules-load.d.
POLICY_BOOLEANS:append:qcom = " kernel_module_load_net_admin=true"
