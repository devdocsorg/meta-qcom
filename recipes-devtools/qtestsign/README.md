# qtestsign

Holds the recipe for [qtestsign](https://github.com/msm8916-mainline/qtestsign), a Python tool that signs Qualcomm ELF firmware images. The LK and Qualcomm U-Boot recipes use its native build to sign their bootloader images.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [qtestsign_git.bb](qtestsign_git.bb) — Installs [qtestsign](https://github.com/msm8916-mainline/qtestsign) into the Python site-packages directory with a `qtestsign` command, for the target, the build host, and the SDK.
