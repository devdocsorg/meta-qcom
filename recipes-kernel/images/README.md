# Boot partition images

Image recipes for the EFI System Partition and the initramfs that pivots into the root filesystem.

## Files

- [README.md](README.md) — Indexes this folder.
- [esp-qcom-common.inc](esp-qcom-common.inc) — Shared VFAT and size settings for the ESP images.
- [esp-qcom-fit-image.bb](esp-qcom-fit-image.bb) — Builds an ESP holding a FIT image and its U-Boot boot script.
- [esp-qcom-image.bb](esp-qcom-image.bb) — Builds an ESP holding systemd-boot and a unified kernel image.
- [initramfs-rootfs-image.bb](initramfs-rootfs-image.bb) — Builds a ramdisk that loads modules and pivots into the root filesystem.
