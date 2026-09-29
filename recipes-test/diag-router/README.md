# diag-router

Recipe for the prebuilt Qualcomm diagnostics router on ARMv8 machines. It and `diag` both provide `virtual-diag-router` and conflict with each other; `conf/layer.conf` prefers `diag` by default.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [diag-router_1.0.3.bb](diag-router_1.0.3.bb) — Installs the prebuilt application that routes diagnostic traffic.
