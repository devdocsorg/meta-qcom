# patches

Patches that the kas configuration in `ci/` applies to other layers' repositories after checking them out, before BitBake parses them. They are not applied by any recipe in this layer.

## Folders

- [oe-core/](oe-core/) — Patches for [openembedded-core](https://github.com/openembedded/openembedded-core) that `ci/base.yml` applies: an igt-gpu-tools build fix for non-x86 targets, a linux-firmware backport of Shikra WLAN firmware, and a uboot-sign fix that keeps the SPL BSS padding.
- [selinux/](selinux/) — Patches for [meta-selinux](https://git.yoctoproject.org/meta-selinux) that `ci/qcom-distro.yml` applies: nativesdk support for libsepol and libselinux, and a libselinux-python build fix for SWIG 4.5.0.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
