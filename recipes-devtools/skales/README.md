# skales

Holds the recipe for [skales](https://git.codelinaro.org/clo/qsdk/oss/tools/skales), which provides the `mkbootimg` tool for creating Qualcomm boot images. The U-Boot bbappend in `recipes-bsp/u-boot` uses its native build. BitBake finds the recipe's patch by name in `files/`.

## Folders

- [files/](files/) — A patch that makes `mkbootimg` run with Python 3.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [skales_git.bb](skales_git.bb) — Installs `mkbootimg` from [skales](https://git.codelinaro.org/clo/qsdk/oss/tools/skales) into `${bindir}/skales`, for the target and the build host.
