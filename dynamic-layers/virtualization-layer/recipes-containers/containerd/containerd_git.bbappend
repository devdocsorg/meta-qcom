# @description Give the owner write and execute permission on the whole source tree.
# The Go build leaves files there without write permission, which stops rm_work removing them.
# @noargs
# @exitcode 0 The owner can write to and enter everything under ${S}.
# @example
#   bitbake containerd -c compile
do_compile:append:qcom() {
    chmod -R u+wx ${S}
}
