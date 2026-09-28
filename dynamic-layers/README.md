# Dynamic layers

Recipes and appends that extend other layers. [conf/layer.conf](../conf/layer.conf) adds each subfolder's recipes only when the layer collection it is named after is in the build (see `BBFILES_DYNAMIC`).

## Folders

- [ai/](ai/README.md) — Additions for the `ai` collection from [meta-ai](https://github.com/qualcomm-linux/meta-ai).
- [meta-arm/](meta-arm/README.md) — Trusted firmware, OP-TEE, and capsule recipes for the `meta-arm` collection from [meta-arm](https://git.yoctoproject.org/meta-arm).
- [openembedded-layer/](openembedded-layer/README.md) — Recipes and appends for the `openembedded-layer` collection (meta-oe) from [meta-openembedded](https://github.com/openembedded/meta-openembedded).
- [qcom-distro/](qcom-distro/README.md) — Additions for the `qcom-distro` collection from [meta-qcom-distro](https://github.com/qualcomm-linux/meta-qcom-distro).
- [selinux/](selinux/README.md) — SELinux kernel and policy appends for the `selinux` collection from [meta-selinux](https://git.yoctoproject.org/meta-selinux).
- [virtualization-layer/](virtualization-layer/README.md) — Container appends for the `virtualization-layer` collection from [meta-virtualization](https://git.yoctoproject.org/meta-virtualization).

## Files

- [README.md](README.md) — Indexes this folder.
