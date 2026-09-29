# recipes-kernel/linux

Kernel recipes and linux-yocto appends; linux-yocto-7.2 and linux-yocto-dev hold kernel metadata and patches that the build reads as a whole, so they have no README.

## Folders

- [linux-qcom-6.18/](linux-qcom-6.18/README.md) — Holds the linux-qcom 6.18 patch and configuration fragment.
- [linux-qcom-next/](linux-qcom-next/README.md) — Holds the linux-qcom-next configuration fragment.
- [linux-yocto-7.2/](linux-yocto-7.2/) — Holds the linux-yocto 7.2 BSP descriptions, configuration fragments, and patches.
- [linux-yocto-dev/](linux-yocto-dev/) — Holds the linux-yocto-dev configuration fragment and patches.

## Files

- [linux-qcom-next-rt_git.bb](linux-qcom-next-rt_git.bb) — Builds linux-qcom-next with the real-time configuration.
- [linux-qcom-next_git.bb](linux-qcom-next_git.bb) — Builds the linux-qcom-next kernel from [qualcomm-linux/kernel](https://github.com/qualcomm-linux/kernel).
- [linux-qcom-rt_6.18.bb](linux-qcom-rt_6.18.bb) — Builds linux-qcom 6.18 with the real-time configuration.
- [linux-qcom_6.18.bb](linux-qcom_6.18.bb) — Builds the linux-qcom 6.18 kernel from [qualcomm-linux/kernel](https://github.com/qualcomm-linux/kernel).
- [linux-yocto-dev.bbappend](linux-yocto-dev.bbappend) — Adds Qualcomm machines, patches, and configuration to linux-yocto-dev.
- [linux-yocto-qcom.inc](linux-yocto-qcom.inc) — Adds Qualcomm machines and kernel metadata to linux-yocto.
- [linux-yocto_7.2.bbappend](linux-yocto_7.2.bbappend) — Adds Qualcomm support and patches to linux-yocto 7.2.
- [qcom-dtb-metadata_1.1.bb](qcom-dtb-metadata_1.1.bb) — Builds the device tree metadata blob that the FIT image carries.
- [README.md](README.md) — Introduces this folder and indexes its contents.
