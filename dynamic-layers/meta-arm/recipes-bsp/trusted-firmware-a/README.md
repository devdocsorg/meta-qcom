# trusted-firmware-a

Builds Trusted Firmware-A from the [Qualcomm trusted-firmware-a](https://github.com/qualcomm-linux/trusted-firmware-a) fork with OP-TEE as the secure payload, reusing `trusted-firmware-a.inc` from [meta-arm](https://git.yoctoproject.org/meta-arm). Each board recipe sets its platform and FIP load address and shares everything else through the include file.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [trusted-firmware-a-qcom-lemans-evk_git.bb](trusted-firmware-a-qcom-lemans-evk_git.bb) — Builds Trusted Firmware-A for the `lemans_evk` platform with FIP load address 0xaf000000, using OP-TEE from optee-os-qcom-lemans.
- [trusted-firmware-a-qcom-rb3gen2_git.bb](trusted-firmware-a-qcom-rb3gen2_git.bb) — Builds Trusted Firmware-A for the `rb3gen2` platform with FIP load address 0x9fc00000, using OP-TEE from optee-os-qcom-kodiak and the sc7280 `libqtisec.a` from [qc_blobs](https://github.com/coreboot/qc_blobs).
- [trusted-firmware-a-qcom.inc](trusted-firmware-a-qcom.inc) — Shared by both board recipes: fetches version 2.15.0-qcom, sets OP-TEE as BL32 and U-Boot as BL33, and wraps the FIP in an ELF signed with qtestsign, or builds only BL31 when `QCOM_UBOOT_SPL_FIT` is 1.
