# @description On Qualcomm machines, make the source tree writable by its
#   owner after compiling.
# @noargs
# @exitcode 0 The permissions are updated.
# @exitcode >0 A command failed; BitBake stops the task.
# @example
#   bitbake -c compile containerd
do_compile:append:qcom() {
    chmod -R u+wx ${S}
}
