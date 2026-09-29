# lib

Python code used by BitBake and by oe-selftest. `conf/layer.conf` adds this folder to BitBake's Python path with `addpylib ${LAYERDIR}/lib qcom`, so classes can import the `qcom` package, and oe-selftest loads test cases from `oeqa/selftest/cases/` in every layer of the build.

## Folders

- [oeqa/](oeqa/README.md) — oe-selftest test cases for this layer.
- [qcom/](qcom/README.md) — Python helpers that the layer's classes import as the `qcom` package.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
