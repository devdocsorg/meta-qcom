# kgsl-dlkm

Holds the recipe for the Qualcomm [kgsl](https://github.com/qualcomm-linux/kgsl) kernel driver that manages Adreno GPUs, built as an out-of-tree kernel module. BitBake finds the recipe's udev rule by name in the `kgsl-dlkm/` subfolder.

## Folders

- [kgsl-dlkm/](kgsl-dlkm/) — Holds `kgsl.rules`, the udev rule that gives the `render` group access to `/dev/kgsl-3d0`.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [kgsl-dlkm_1.0.14.bb](kgsl-dlkm_1.0.14.bb) — Builds the `msm_kgsl` module from [kgsl](https://github.com/qualcomm-linux/kgsl) version 1.0.14 for AArch64 machines, installs `kgsl.rules`, and blacklists `msm_kgsl` so that it does not load automatically.
