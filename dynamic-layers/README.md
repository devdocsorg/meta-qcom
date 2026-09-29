# dynamic-layers

Recipes and appends that BitBake parses only when another layer is also in the build. `BBFILES_DYNAMIC` in `conf/layer.conf` ties each subfolder to a layer collection name, so the `.bb` and `.bbappend` files in its `<category>/<recipe>/` folders are added only when that collection is present.

## Folders

- [ai/](ai/README.md) — Machine learning recipes and appends for the `ai` collection from [meta-ai](https://github.com/qualcomm-linux/meta-ai).
- [meta-arm/](meta-arm/README.md) — Trusted Firmware-A, OP-TEE, and UEFI capsule recipes for the `meta-arm` collection from [meta-arm](https://git.yoctoproject.org/meta-arm).
- [openembedded-layer/](openembedded-layer/README.md) — Modem, camera, sensor, location, TEE, and developer tool recipes for the `openembedded-layer` collection, which is the meta-oe layer in [meta-openembedded](https://github.com/openembedded/meta-openembedded).
- [qcom-distro/](qcom-distro/README.md) — An IMSDK append for the `qcom-distro` collection from [meta-qcom-distro](https://github.com/qualcomm-linux/meta-qcom-distro).
- [selinux/](selinux/README.md) — SELinux kernel configuration and policy changes for the `selinux` collection from [meta-selinux](https://git.yoctoproject.org/meta-selinux).
- [virtualization-layer/](virtualization-layer/README.md) — A containerd append for the `virtualization-layer` collection from [meta-virtualization](https://git.yoctoproject.org/meta-virtualization).

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
