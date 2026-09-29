# qdl

Holds the recipe for [qdl](https://github.com/linux-msm/qdl), the Qualcomm Download tool that flashes images to Qualcomm SoCs over the EDL (Emergency Download) USB protocol. BitBake finds the recipe's patch by name in `files/`.

## Folders

- [files/](files/) — A patch that makes qdl's libzip-based zip container support an optional Meson feature.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [qdl_2.8.bb](qdl_2.8.bb) — Builds [qdl](https://github.com/linux-msm/qdl) 2.8 with Meson for the target, the build host, and the SDK, leaving zip container support off unless the `zip` `PACKAGECONFIG` option is set.
