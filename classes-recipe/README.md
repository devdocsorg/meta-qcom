# Recipe classes

BitBake classes that recipes inherit to generate FIT, flashing, and capsule
images, or to add adbd to an image.

## Files

- [README.md](README.md) — Indexes this folder.
- [dtb-fit-image.bbclass](dtb-fit-image.bbclass) — Builds a DTB-only FIT image with one configuration per compatible string.
- [image-adbd.bbclass](image-adbd.bbclass) — Installs adbd in an image and enables it at boot with the `enable-adbd` image feature.
- [image_types_qcom.bbclass](image_types_qcom.bbclass) — Defines the `qcomflash` image type, a directory and tarball ready for flashing with QDL.
- [qcom-capsule.bbclass](qcom-capsule.bbclass) — Builds a signed UEFI firmware update capsule from the boot binaries.
