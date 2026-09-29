# recipes-test

Test and diagnostic tools for Qualcomm boards and the initramfs images that bundle them for board bring-up and kernel testing. BitBake loads every `.bb` and `.bbappend` one folder down through the `recipes-*/*/` pattern in `conf/layer.conf`.

## Folders

- [bootrr/](bootrr/README.md) — A low-level boot test tool for Qualcomm boards.
- [diag/](diag/README.md) — The open-source diagnostics router.
- [diag-router/](diag-router/README.md) — The prebuilt Qualcomm diagnostics router.
- [images/](images/README.md) — Initramfs images for bring-up and testing.
- [libdiag/](libdiag/README.md) — The prebuilt Qualcomm diagnostics library and utilities.
- [mybw/](mybw/README.md) — A memory read bandwidth benchmark.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
