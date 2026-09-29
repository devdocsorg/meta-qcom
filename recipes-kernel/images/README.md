# images

Image recipes for boot partitions: the EFI System Partition (ESP) images that the `qcomflash` image type packs as `efi.bin`, and a small initramfs.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [esp-qcom-common.inc](esp-qcom-common.inc) — Shared by the two ESP image recipes: a 512 MB VFAT image with the machine's sector size and no image features.
- [esp-qcom-fit-image.bb](esp-qcom-fit-image.bb) — ESP image for the U-Boot FIT flow, holding the kernel `fitImage` and the U-Boot `boot.scr`; skipped unless the machine sets a U-Boot config and `kernel-fit-extra-artifacts` is enabled.
- [esp-qcom-image.bb](esp-qcom-image.bb) — ESP image for EFI machines, holding systemd-boot and a Unified Kernel Image that, except on a few machines, carries no devicetree and uses the one from the firmware.
- [initramfs-rootfs-image.bb](initramfs-rootfs-image.bb) — Initramfs with the initramfs-framework rootfs, udev, and copy-modules modules, for pivoting into the rootfs.
