require optee-os-qcom.inc
require optee-qcom.inc

SUMMARY = "OP-TEE Trusted OS TA devkit"
DESCRIPTION = "OP-TEE TA devkit for build TAs"
HOMEPAGE = "https://www.op-tee.org/"

DEPENDS += "python3-pycryptodome-native"
DEPENDS:append:toolchain-clang = " lld-native"

# @description Install the trusted application devkit under
#   `${includedir}/optee/export-user_ta`.
# @noargs
# @exitcode 0 The devkit is in the install directory.
# @exitcode >0 A command failed; BitBake stops the task.
# @example
#   bitbake -c install optee-os-tadevkit-qcom
do_install() {
    #install TA devkit
    install -d ${D}${includedir}/optee/export-user_ta/
    for f in ${B}/export-ta_${OPTEE_ARCH}/* ; do
        cp -aR $f ${D}${includedir}/optee/export-user_ta/
    done
}

# @description Replace the inherited OP-TEE deploy step, so the devkit
#   deploys nothing.
# @noargs
# @exitcode 0 A message is printed and nothing is deployed.
# @example
#   bitbake -c deploy optee-os-tadevkit-qcom
do_deploy() {
        echo "Do not inherit do_deploy from optee-os."
}

FILES:${PN} = "${includedir}/optee/"

# Build paths are currently embedded
INSANE_SKIP:${PN}-dev += "buildpaths"
