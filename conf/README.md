# conf

Layer configuration that BitBake reads when the layer is listed in `bblayers.conf`, and the machine configurations selected with `MACHINE`.

## Folders

- [machine/](machine/README.md) — Machine configurations for the supported Qualcomm boards and their shared includes.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [layer.conf](layer.conf) — Registers the layer with BitBake: recipe and dynamic-layer file patterns, priority 6, `wrynose` compatibility, the `qli-mirrors` class, the default diag router provider, and the `lib/` Python path.
