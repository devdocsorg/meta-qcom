# adreno

Holds the recipe for the prebuilt Qualcomm Adreno GPU user-mode libraries, which the recipe splits into packages according to the enabled distro features.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [qcom-adreno_1.877.3.bb](qcom-adreno_1.877.3.bb) — Installs the prebuilt Adreno libraries for OpenGL ES and EGL (with `glvnd`), Vulkan, and OpenCL with their ICD files, plus a modprobe configuration, for AArch64 Qualcomm machines; the EGL and Vulkan packages depend on `kgsl-dlkm` and `msm-gbm-backend`.
