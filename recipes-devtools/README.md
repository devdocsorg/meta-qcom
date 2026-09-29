# recipes-devtools

Development and build tools for Qualcomm platforms, covering flashing, firmware signing, boot image creation, and firmware conversion. Most of these recipes also build for the host through `BBCLASSEXTEND`, so other recipes can use them at build time as `-native` dependencies.

## Folders

- [debugcc/](debugcc/README.md) — Tool to debug Qualcomm clock controllers.
- [pil-squasher/](pil-squasher/README.md) — Tool that converts MDT firmware images to MBN files.
- [qc-image-unpacker/](qc-image-unpacker/README.md) — Unpacker for Android Qualcomm images.
- [qca-swiss-army-knife/](qca-swiss-army-knife/README.md) — Qualcomm Atheros driver development utilities and board data JSON generators.
- [qdl/](qdl/README.md) — Qualcomm Download tool that flashes images over the EDL USB protocol.
- [qmic/](qmic/README.md) — QMI compiler.
- [qtestsign/](qtestsign/README.md) — Tool that signs Qualcomm ELF firmware images.
- [skales/](skales/README.md) — Boot image creation tool (`mkbootimg`) for Qualcomm SoCs.
- [swiv-build-utility/](swiv-build-utility/README.md) — Tool that adds a SWIV segment to boot firmware ELF images before signing.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
