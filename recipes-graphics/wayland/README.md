# recipes-graphics/wayland

Weston changes for Qualcomm machines.

## Folders

- [weston/](weston/README.md) — Holds the Weston patches.
- [weston-init/](weston-init/README.md) — Holds the Weston service drop-in and start script.

## Files

- [README.md](README.md) — Introduces this folder and indexes its contents.
- [weston-init.bbappend](weston-init.bbappend) — Uses the DRM backend and starts Weston with every KMS-capable card.
- [weston_%.bbappend](weston_%.bbappend) — Applies the Weston patches on Qualcomm machines.
