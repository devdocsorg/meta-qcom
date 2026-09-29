# qcom

Python package that BitBake makes importable as `qcom` through the `addpylib` line in `conf/layer.conf`.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [dtb_only_fitimage.py](dtb_only_fitimage.py) — Extends the OpenEmbedded FIT image classes with `QcomItsNodeRoot`, which writes a DTB-only FIT image with Qualcomm DTB metadata and compatible strings for `dtb-fit-image.bbclass`.
