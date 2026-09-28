# ADB configuration

Configures the ADB daemon and USB gadget on Qualcomm boards.

## Folders

- [android-tools-adbd-cmdline/](android-tools-adbd-cmdline/README.md) — systemd drop-in for the adbd service.
- [android-tools-conf/](android-tools-conf/README.md) — Gadget start script and machine settings.

## Files

- [README.md](README.md) — Indexes this folder.
- [android-tools-adbd-cmdline.bb](android-tools-adbd-cmdline.bb) — Installs a drop-in that starts adbd from a kernel argument or a flag file.
- [android-tools-conf_%.bbappend](android-tools-conf_%25.bbappend) — Adds the Qualcomm `android-gadget-setup.machine` settings.
