# recipes-kernel

Recipes for the kernels, out-of-tree kernel modules, kernel firmware, devicetree metadata, and boot partition images of Qualcomm machines. BitBake loads every `.bb` and `.bbappend` one folder down through the `recipes-*/*/` pattern in `conf/layer.conf`.

## Folders

- [images/](images/README.md) — Images for the EFI System Partition and an initramfs that pivots into the rootfs.
- [iris-video-module/](iris-video-module/README.md) — Out-of-tree Iris video driver module.
- [linux/](linux/README.md) — The Qualcomm Linux kernels and the Qualcomm additions to linux-yocto.
- [linux-firmware/](linux-firmware/README.md) — Qualcomm changes to the linux-firmware recipe.
- [qps615-module/](qps615-module/README.md) — Kernel module and firmware for the QPS615 PCIe Ethernet bridge.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
