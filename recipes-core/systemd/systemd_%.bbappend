FILESEXTRAPATHS:prepend:qcom := "${THISDIR}/${PN}:"

SRC_URI:append:qcom = " \
    file://99-dma-heap.rules \
"

# Create a group dmaheap and add this group to /dev/dma_heap/system through
# dma-heap rules.
GROUPADD_PARAM:udev:append:qcom = "; -r dmaheap"

# @description On Qualcomm machines, install `99-dma-heap.rules`, which gives the
#   `dmaheap` group access to `/dev/dma_heap/system`.
# @noargs
# @exitcode 0 The rule is in the install directory.
# @exitcode >0 An install command failed; BitBake stops the task.
# @example
#   bitbake -c install systemd
do_install:append:qcom() {
    install -d ${D}${nonarch_libdir}/udev/rules.d
    install -m 0644 ${UNPACKDIR}/99-dma-heap.rules \
        ${D}${nonarch_libdir}/udev/rules.d/
}

FILES:${PN}-udev-rules:append:qcom = " ${nonarch_libdir}/udev/rules.d/99-dma-heap.rules"
