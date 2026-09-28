# Global classes

BitBake classes that recipes, images, or configuration can inherit, such as
kernel boot-image generation and the Qualcomm Linux download mirrors.

## Files

- [README.md](README.md) — Indexes this folder.
- [linux-qcom-bootimg.bbclass](linux-qcom-bootimg.bbclass) — Builds Android boot images with skales mkbootimg from the kernel and each device tree.
- [linux-qcom-dtbbin.bbclass](linux-qcom-dtbbin.bbclass) — Packs each kernel device tree into a VFAT image for the dtb partition.
- [qli-mirrors.bbclass](qli-mirrors.bbclass) — Adds the Qualcomm Linux download mirrors selected by `QLI_BASELINE`.
- [uki-esp-image.bbclass](uki-esp-image.bbclass) — Copies a unified kernel image into an EFI System Partition image.
