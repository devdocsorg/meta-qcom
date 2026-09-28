# U-Boot

Recipes that build U-Boot for Qualcomm boards and the boot script for FIT-based boot.

## Folders

- [files/](files/README.md) — Holds the U-Boot patch and configuration fragments.
- [u-boot-scr-qcom-fit/](u-boot-scr-qcom-fit/README.md) — Holds the boot script template.

## Files

- [README.md](README.md) — Indexes this folder.
- [u-boot-qcom_git.bb](u-boot-qcom_git.bb) — Builds the Qualcomm U-Boot fork and signs its images.
- [u-boot-scr-qcom-fit.bb](u-boot-scr-qcom-fit.bb) — Compiles and deploys `boot.scr`, which loads and boots the FIT image.
- [u-boot_%.bbappend](u-boot_%25.bbappend) — Wraps upstream U-Boot in Android boot images so ABL can chainload it on Qualcomm machines.
