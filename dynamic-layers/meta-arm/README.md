# meta-arm

Recipes and appends that reuse recipe code from [meta-arm](https://git.yoctoproject.org/meta-arm); BitBake parses them only when the `meta-arm` layer collection is in the build. They build Trusted Firmware-A, OP-TEE, and UEFI capsule updates for Qualcomm boards.

## Folders

- [recipes-bsp/](recipes-bsp/README.md) — Trusted Firmware-A recipes for individual boards.
- [recipes-devtools/](recipes-devtools/README.md) — The native UEFI capsule generation tool.
- [recipes-firmware/](recipes-firmware/README.md) — The UEFI firmware update capsule recipe.
- [recipes-security/](recipes-security/README.md) — OP-TEE OS recipes, the OP-TEE test append, and the OP-TEE package group.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
