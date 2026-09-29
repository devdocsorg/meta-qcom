# iris-video-module

Recipe for the out-of-tree Qualcomm Iris video driver, built as a kernel module for ARMv8 machines.

## Folders

- [iris-video-dlkm/](iris-video-dlkm/) — The two modprobe blacklist files that the recipe installs: one blocks the upstream `qcom_iris` and Venus drivers, the other blocks this recipe's `iris_vpu` module.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [iris-video-dlkm_1.0.28.bb](iris-video-dlkm_1.0.28.bb) — Builds the Iris video driver module and uses update-alternatives to choose, per SoC, whether it or the upstream video drivers are blacklisted.
