# libqmi

Changes the libqmi recipe from [meta-openembedded](https://github.com/openembedded/meta-openembedded) for Qualcomm machines.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [libqmi_%.bbappend](libqmi_%25.bbappend) — On Qualcomm machines, adds the `qrtr` PACKAGECONFIG option, which enables libqmi's QRTR support.
