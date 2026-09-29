# @description Make the containerd sources writable after compiling, so later tasks can remove them.
# @noargs
# @exitcode 0 The task finished; any failing command fails the task and stops the build.
# @example
#   bitbake -c compile containerd
do_compile:append:qcom() {
    chmod -R u+wx ${S}
}
