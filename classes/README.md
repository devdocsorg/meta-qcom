# classes

BitBake classes that can be used from configuration files (`INHERIT`, `KERNEL_CLASSES`) as well as from recipes. BitBake finds them through `BBPATH`, which `conf/layer.conf` extends with the layer root.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [linux-qcom-bootimg.bbclass](linux-qcom-bootimg.bbclass) — Kernel class that packs the kernel, devicetree, and optional initramfs into Android boot images (`boot-*.img`) with skales `mkbootimg`, in the `do_qcom_img_deploy` task.
- [linux-qcom-dtbbin.bbclass](linux-qcom-dtbbin.bbclass) — Kernel class that puts each devicetree (and the multi-DTB FIT image when `QCOM_DTB_DEFAULT` is `multi-dtb`) into a small VFAT image for the DTB partition, in the `do_qcom_dtbbin_deploy` task.
- [qli-mirrors.bbclass](qli-mirrors.bbclass) — Adds the Qualcomm Linux download mirror for the current `QLI_BASELINE` to `MIRRORS` as a fallback for every fetcher; `conf/layer.conf` inherits it globally.
- [uki-esp-image.bbclass](uki-esp-image.bbclass) — Image class that copies the Unified Kernel Image into `EFI/Linux` of the image rootfs to build an EFI System Partition.
