# msm-gbm-backend

Holds the recipe for [gbm-msm-backend](https://github.com/qualcomm-linux/gbm-msm-backend), the MSM backend of the [Mesa](https://gitlab.freedesktop.org/mesa/mesa) GBM library, which libgbm loads with `dlopen()` at runtime. BitBake finds the recipe's patches by name in `files/`.

## Folders

- [files/](files/) — Two patches that set the install paths of the backend library, its configuration XML, and its header.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [msm-gbm-backend.bb](msm-gbm-backend.bb) — Builds `msm_gbm.so` and its `default_fmt_alignment.xml` configuration from [gbm-msm-backend](https://github.com/qualcomm-linux/gbm-msm-backend) with Meson for Qualcomm machines; requires the `opengl` distro feature.
