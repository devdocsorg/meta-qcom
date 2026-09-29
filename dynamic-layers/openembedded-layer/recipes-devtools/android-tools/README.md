# android-tools

Controls when adbd starts and how its USB gadget is set up, on top of the android-tools recipes from [meta-openembedded](https://github.com/openembedded/meta-openembedded).

## Folders

- [android-tools-adbd-cmdline/](android-tools-adbd-cmdline/) — The systemd drop-in `50-adbd-cmdline.conf` that android-tools-adbd-cmdline installs.
- [android-tools-conf/](android-tools-conf/) — A replacement `android-gadget-start` script that binds the adb gadget to the USB controller named by `adbd.udc=` or else the fastest one, and the Qualcomm `android-gadget-setup.machine` file that sets the USB manufacturer, model, and serial number.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [android-tools-adbd-cmdline.bb](android-tools-adbd-cmdline.bb) — Installs a systemd drop-in for `android-tools-adbd.service` that starts adbd only when the kernel command line contains `adbd` or `/etc/usb-debugging-enabled` exists.
- [android-tools-conf_%.bbappend](android-tools-conf_%25.bbappend) — Makes android-tools-conf use the `android-gadget-start` script from `android-tools-conf/` and, on Qualcomm machines, adds `android-gadget-setup.machine`.
