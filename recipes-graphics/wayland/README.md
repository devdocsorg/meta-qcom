# Weston

Appends, patches, and start-up files that adapt the Weston compositor to Qualcomm machines.

## Folders

- [weston/](weston/README.md) — Holds the patches the Weston append applies.
- [weston-init/](weston-init/README.md) — Holds the service drop-in and start script the weston-init append installs.

## Files

- [README.md](README.md) — Indexes this folder.
- [weston-init.bbappend](weston-init.bbappend) — Uses the DRM backend and starts Weston through weston-start.sh on Qualcomm machines.
- [weston_%.bbappend](weston_%25.bbappend) — Applies the Weston patches on Qualcomm machines.
