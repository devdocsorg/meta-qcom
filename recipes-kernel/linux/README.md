# linux

Kernel recipes for Qualcomm machines: the linux-qcom kernels built from the Qualcomm Linux [kernel](https://github.com/qualcomm-linux/kernel) repository, their real-time variants, the Qualcomm additions to linux-yocto, and the DTB metadata blob.

## Folders

- [linux-qcom-6.18/](linux-qcom-6.18/) — Local files for `linux-qcom` and `linux-qcom-rt` 6.18: a patch to the gen-mach-types tool and the `bsp-additions.cfg` config fragment.
- [linux-qcom-next/](linux-qcom-next/) — The `bsp-additions.cfg` config fragment for `linux-qcom-next` and `linux-qcom-next-rt`.
- [linux-yocto-7.2/](linux-yocto-7.2/) — Kernel metadata for linux-yocto 7.2: BSP `.scc` and `.cfg` files for `qcom-armv7a` and `qcom-armv8a`, the `qcom.scc` entry point, and two devicetree patches.
- [linux-yocto-dev/](linux-yocto-dev/) — Devicetree patches and the `qcom.cfg` config fragment for linux-yocto-dev.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [linux-qcom-next-rt_git.bb](linux-qcom-next-rt_git.bb) — Real-time variant of `linux-qcom-next` that also merges the kernel's `rt.config` fragment.
- [linux-qcom-next_git.bb](linux-qcom-next_git.bb) — Builds the kernel from the `qcom-next` branch with `defconfig` and the Qualcomm config fragments; its `linux-qcom-next-upstream` variant follows the branch tip.
- [linux-qcom-rt_6.18.bb](linux-qcom-rt_6.18.bb) — Real-time variant of `linux-qcom` 6.18 that also merges the kernel's `rt.config` fragment.
- [linux-qcom_6.18.bb](linux-qcom_6.18.bb) — Builds the 6.18 kernel from the `qcom-6.18.y` branch with `defconfig` and the Qualcomm config fragments; its `linux-qcom-6.18.y-upstream` variant follows the branch tip.
- [linux-yocto-dev.bbappend](linux-yocto-dev.bbappend) — For Qualcomm machines, adds devicetree patches and the `qcom.cfg` fragment to linux-yocto-dev and builds it from `defconfig`.
- [linux-yocto-qcom.inc](linux-yocto-qcom.inc) — Shared by the linux-yocto bbappends: makes linux-yocto compatible with `qcom-armv8a` and `qcom-armv7a` and adds the Qualcomm kernel metadata from `linux-yocto-<version>/`.
- [linux-yocto_7.2.bbappend](linux-yocto_7.2.bbappend) — For Qualcomm machines, applies `linux-yocto-qcom.inc` to linux-yocto 7.2 and adds a DB820c regulator workaround and a Hamoa IoT EVK camera overlay patch.
- [qcom-dtb-metadata_1.1.bb](qcom-dtb-metadata_1.1.bb) — Builds and deploys `qcom-metadata.dtb`, the Qualcomm DTB metadata that `dtb-fit-image.bbclass` puts first in the DTB FIT image.
