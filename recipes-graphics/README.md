# recipes-graphics

Graphics recipes and bbappends for Qualcomm Adreno GPUs and the Wayland display stack. BitBake parses the `.bb` and `.bbappend` files in these subfolders through the layer's `recipes-*/*/*.bb` and `recipes-*/*/*.bbappend` patterns.

## Folders

- [adreno/](adreno/README.md) — Prebuilt Adreno user-mode libraries for OpenGL ES, Vulkan, and OpenCL.
- [kgsl-dlkm/](kgsl-dlkm/README.md) — Out-of-tree KGSL kernel driver for Adreno GPUs.
- [mesa/](mesa/README.md) — Backported patches and freedreno settings for [Mesa](https://gitlab.freedesktop.org/mesa/mesa) on Qualcomm machines.
- [msm-gbm-backend/](msm-gbm-backend/README.md) — GBM backend library for MSM that libgbm loads at runtime.
- [wayland/](wayland/README.md) — [Weston](https://gitlab.freedesktop.org/wayland/weston) patches and Weston startup changes for Qualcomm machines.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
