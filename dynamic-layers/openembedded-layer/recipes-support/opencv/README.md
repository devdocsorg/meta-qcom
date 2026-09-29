# opencv

Changes the OpenCV recipe from [meta-openembedded](https://github.com/openembedded/meta-openembedded) for Qualcomm machines.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [opencv_%.bbappend](opencv_%25.bbappend) — On Qualcomm machines, enables the `tests` PACKAGECONFIG option, and on aarch64 Qualcomm machines also enables `fastcv`.
