# classes-recipe

BitBake classes that only recipes inherit, found through `BBPATH`, which `conf/layer.conf` extends with the layer root.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [dtb-fit-image.bbclass](dtb-fit-image.bbclass) — Builds `qclinuxfitImage`, a DTB-only FIT image with the Qualcomm DTB metadata and one configuration per compatible string from `FIT_DTB_COMPATIBLE`, using the `qcom.dtb_only_fitimage` helper in `lib/`.
- [image-adbd.bbclass](image-adbd.bbclass) — Installs adbd in an image when the `openembedded-layer` collection is in the build and enables it at boot when `IMAGE_FEATURES` contains `enable-adbd`.
- [image_types_qcom.bbclass](image_types_qcom.bbclass) — Adds the `qcomflash` image type, a tarball holding the rootfs, ESP, DTB and boot images, boot firmware, and partition files needed to flash a board.
- [qcom-capsule.bbclass](qcom-capsule.bbclass) — Builds and signs a UEFI FMP capsule for Qualcomm boot firmware updates and injects the OEM root certificate into `xbl_config.elf`.
