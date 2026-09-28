# KGSL GPU driver

Recipe for the out-of-tree KGSL kernel module that drives Adreno GPUs.

## Folders

- [kgsl-dlkm/](kgsl-dlkm/README.md) — Holds the udev rule the recipe installs.

## Files

- [kgsl-dlkm_1.0.14.bb](kgsl-dlkm_1.0.14.bb) — Builds the msm_kgsl module, blacklisted by default, and installs its udev rule.
- [README.md](README.md) — Indexes this folder.
