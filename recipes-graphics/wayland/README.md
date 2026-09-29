# wayland

Qualcomm changes to the [OpenEmbedded-Core](https://git.openembedded.org/openembedded-core) `weston` and `weston-init` recipes. Each bbappend adds its own subfolder to the search path, so BitBake finds the local files there by name.

## Folders

- [weston/](weston/) — [Weston](https://gitlab.freedesktop.org/wayland/weston) patches that work around Adreno shader compiler limitations, stop newly enabled outputs from waiting on a deferred repaint, and keep spare primary and cursor planes off the DRM backend's overlay plane list.
- [weston-init/](weston-init/) — The `weston.service` drop-in and the `weston-start.sh` script that the `weston-init` bbappend installs.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [weston-init.bbappend](weston-init.bbappend) — For Qualcomm machines, makes DRM the default backend and starts Weston through `weston-start.sh`, which passes any further KMS-capable DRM cards to Weston as `--additional-devices`.
- [weston_%.bbappend](weston_%25.bbappend) — For Qualcomm machines, applies the four patches in `weston/`.
