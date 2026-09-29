# swiv-build-utility

Holds the recipe for the Qualcomm SWIV (Software Image Version) build utility from [boot-firmware-ci](https://github.com/qualcomm-linux/boot-firmware-ci). The Qualcomm U-Boot recipe uses its native build to annotate the SPL before signing it.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [swiv-build-utility_git.bb](swiv-build-utility_git.bb) — Installs `swiv_build_utility` from [boot-firmware-ci](https://github.com/qualcomm-linux/boot-firmware-ci), which adds the SWIV segment that the Qualcomm secure boot chain requires to a boot firmware ELF image, for the target, the build host, and the SDK.
