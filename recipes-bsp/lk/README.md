# lk

Recipes for the Little Kernel (LK) bootloader used on DragonBoard 410c and 820c. Each recipe builds LK from [lk](https://git.codelinaro.org/linaro/qcomlt/lk) with the settings of the shared `lk.inc` and deploys the images it builds.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [lk-db410c-sd-boot_git.bb](lk-db410c-sd-boot_git.bb) — Builds the SD card boot flavour of LK for DragonBoard 410c from the `release/LA.BR.1.2.7-03810-8x16.0+sdboot` branch.
- [lk-db410c_git.bb](lk-db410c_git.bb) — Builds LK for DragonBoard 410c from the `release/LA.BR.1.2.7-03810-8x16.0` branch.
- [lk-db820c_git.bb](lk-db820c_git.bb) — Builds LK for DragonBoard 820c (msm8996) from the `release/LA.HB.1.3.2-19600-8x96.0` branch with verified boot enabled.
- [lk.inc](lk.inc) — Shared by the three `lk-*` recipes; fetches LK and a prebuilt arm-eabi 4.8 GCC, builds `emmc_appsboot.mbn` for `LK_SOC` (msm8916 by default), signs it with `qtestsign`, and deploys signed and unsigned copies under `LK_MACHINE`.
