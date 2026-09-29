# recipes-bsp/u-boot

Recipes for U-Boot on Qualcomm boards.

## Folders

- [files/](files/README.md) — Holds the U-Boot patch and configuration fragments.
- [u-boot-scr-qcom-fit/](u-boot-scr-qcom-fit/README.md) — Holds the FIT boot script template.

## Files

- [README.md](README.md) — Introduces this folder and indexes its contents.
- [u-boot-qcom_git.bb](u-boot-qcom_git.bb) — Builds U-Boot from the Qualcomm fork, signing it or building the SPL FIT flow.
- [u-boot-scr-qcom-fit.bb](u-boot-scr-qcom-fit.bb) — Builds boot.scr, which boots a FIT kernel image.
- [u-boot_%.bbappend](u-boot_%.bbappend) — Wraps U-Boot in an Android boot image so ABL can chainload it.
