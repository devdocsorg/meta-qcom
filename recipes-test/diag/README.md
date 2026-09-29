# diag

Recipe for the open-source diag router. It and `diag-router` both provide `virtual-diag-router` and conflict with each other; `conf/layer.conf` prefers this one by default.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [diag_git.bb](diag_git.bb) — Builds DIAG, which routes diagnostic messages between the host and the SoC's subsystems.
