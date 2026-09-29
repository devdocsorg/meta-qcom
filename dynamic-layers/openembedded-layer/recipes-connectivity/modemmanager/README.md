# modemmanager

Changes the ModemManager recipe from [meta-openembedded](https://github.com/openembedded/meta-openembedded) for Qualcomm machines and holds the patches it applies.

## Folders

- [files/](files/) — ModemManager patches that add TA storage for SMS, QRTR and mhi_net support for PCIe-attached SDX modems, and BAM-DMUX support for QMI modems.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [modemmanager_%.bbappend](modemmanager_%25.bbappend) — On Qualcomm machines, enables the `qrtr` PACKAGECONFIG option, adds json-glib to `DEPENDS`, and applies the sixteen patches from `files/`.
