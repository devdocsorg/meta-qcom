# dynamic-layers/openembedded-layer/recipes-devtools/android-tools

adb configuration for Qualcomm machines.

## Folders

- [android-tools-adbd-cmdline/](android-tools-adbd-cmdline/README.md) — Holds the adbd service drop-in.
- [android-tools-conf/](android-tools-conf/README.md) — Holds the USB gadget scripts.

## Files

- [android-tools-adbd-cmdline.bb](android-tools-adbd-cmdline.bb) — Starts adbd when the kernel command line or a marker file asks for it.
- [android-tools-conf_%.bbappend](android-tools-conf_%.bbappend) — Adds the Qualcomm USB gadget identity on Qualcomm machines.
- [README.md](README.md) — Introduces this folder and indexes its contents.
