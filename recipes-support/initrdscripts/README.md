# initrdscripts

Recipe for an extra initramfs-framework module, used by `initramfs-rootfs-image`.

## Folders

- [files/](files/) — The `copy-modules.sh` script that the recipe installs.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [initramfs-module-copy-modules_1.0.bb](initramfs-module-copy-modules_1.0.bb) — Installs an initramfs-framework module that, when the `copy_modules` boot parameter is set, copies the running kernel's modules from the initramfs into the rootfs.
