# abl2esp

Recipe for abl2esp, a minimal replacement for Qualcomm's Android Bootloader (ABL) that the `qcomflash` image type includes when the machine sets `ABL_SIGNATURE_VERSION`.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [abl2esp_1.0.bb](abl2esp_1.0.bb) — Deploys the prebuilt abl2esp ELF images for signature versions v5, v6, and v7, which look for `EFI/boot/bootaa64.efi` on any filesystem and start it.
