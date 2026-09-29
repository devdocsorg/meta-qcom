# recipes-kernel/images

ESP and ramdisk image recipes.

## Files

- [esp-qcom-common.inc](esp-qcom-common.inc) — Shares the ESP image settings.
- [esp-qcom-fit-image.bb](esp-qcom-fit-image.bb) — Builds an ESP image with a U-Boot FIT kernel and boot script.
- [esp-qcom-image.bb](esp-qcom-image.bb) — Builds an ESP image with systemd-boot and a unified kernel image.
- [initramfs-rootfs-image.bb](initramfs-rootfs-image.bb) — Builds a ramdisk that mounts and switches to the root file system.
- [README.md](README.md) — Introduces this folder and indexes its contents.
