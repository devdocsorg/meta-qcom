# u-boot

Recipes for U-Boot on Qualcomm machines: the Qualcomm U-Boot build, a FIT boot script, and a bbappend that packs the [OpenEmbedded-Core](https://git.openembedded.org/openembedded-core) `u-boot` build into an Android-style boot image for chainloading from ABL.

## Folders

- [files/](files/) — The OpenSSL Provider API patch and the configuration fragments that `u-boot-qcom_git.bb` adds to disable the `mkeficapsule` tool and enable EFI runtime variables, OP-TEE, Gunyah EL2 exit handling, and SPL FIT signatures.
- [u-boot-scr-qcom-fit/](u-boot-scr-qcom-fit/) — The `boot.cmd.in` template that `u-boot-scr-qcom-fit.bb` turns into `boot.scr`.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [u-boot-qcom_git.bb](u-boot-qcom_git.bb) — Builds U-Boot from [qualcomm-linux/u-boot](https://github.com/qualcomm-linux/u-boot) with the OpenEmbedded-Core U-Boot includes, signs `u-boot.elf` as an MBN with `qtestsign` for configurations that set an MBN header version, and, when `QCOM_UBOOT_SPL_FIT` is `1`, builds a SWIV-annotated, signed SPL with BL31 and OP-TEE in the FIT.
- [u-boot-scr-qcom-fit.bb](u-boot-scr-qcom-fit.bb) — Generates and deploys a `boot.scr` script that loads `/fitImage` and boots it with `bootm`, filling in the kernel command line and the optional FIT configuration.
- [u-boot_%.bbappend](u-boot_%25.bbappend) — For Qualcomm machines, packs each `u-boot` configuration with its kernel-deployed device tree into an Android-style boot image using the `skales` `mkbootimg`, and links the preferred bootloader's image as `boot-${MACHINE}.img`.
