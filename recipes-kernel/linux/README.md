# Linux kernel recipes

Recipes for the Qualcomm kernels and changes to the linux-yocto kernels, with their fragments and patches.

## Folders

- [linux-qcom-6.18/](linux-qcom-6.18/README.md) — Holds the patch and configuration fragment for linux-qcom 6.18.
- [linux-qcom-next/](linux-qcom-next/README.md) — Holds the configuration fragment for linux-qcom-next.
- [linux-yocto-7.2/](linux-yocto-7.2/README.md) — Holds the kernel metadata and patches for linux-yocto 7.2.
- [linux-yocto-dev/](linux-yocto-dev/README.md) — Holds the fragment and patches for linux-yocto-dev.

## Files

- [README.md](README.md) — Indexes this folder.
- [linux-qcom-next-rt_git.bb](linux-qcom-next-rt_git.bb) — Builds linux-qcom-next with the real-time configuration.
- [linux-qcom-next_git.bb](linux-qcom-next_git.bb) — Builds the qcom-next kernel from [qualcomm-linux/kernel](https://github.com/qualcomm-linux/kernel).
- [linux-qcom-rt_6.18.bb](linux-qcom-rt_6.18.bb) — Builds linux-qcom 6.18 with the real-time configuration.
- [linux-qcom_6.18.bb](linux-qcom_6.18.bb) — Builds the 6.18 kernel from [qualcomm-linux/kernel](https://github.com/qualcomm-linux/kernel).
- [linux-yocto-dev.bbappend](linux-yocto-dev.bbappend) — Adds Qualcomm patches and configuration to linux-yocto-dev.
- [linux-yocto-qcom.inc](linux-yocto-qcom.inc) — Shared settings that add the Qualcomm kernel metadata to linux-yocto.
- [linux-yocto_7.2.bbappend](linux-yocto_7.2.bbappend) — Adds Qualcomm metadata and patches to linux-yocto 7.2.
- [qcom-dtb-metadata_1.1.bb](qcom-dtb-metadata_1.1.bb) — Builds and deploys the Qualcomm device tree metadata blob.
