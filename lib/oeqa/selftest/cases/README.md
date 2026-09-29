# cases

oe-selftest test modules for this layer. `ci/oe-selftest.sh` runs every `.py` module in this folder with `oe-selftest --run-tests` when no module is named.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [qcom_fitimage.py](qcom_fitimage.py) — Tests the DTB-only FIT image generation of `dtb-fit-image.bbclass`: unit tests of the generated ITS, integration tests on a built `qclinuxfitImage`, and checks that each machine's devicetrees and the `FIT_DTB_COMPATIBLE` entries exist in the kernel builds.
