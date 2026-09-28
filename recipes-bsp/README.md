# Board support recipes

Recipes for boot firmware, device firmware, bootloaders, partition tables, and per-board package groups.

## Folders

- [devicetree/](devicetree/README.md) — Builds a placeholder device tree for the generic armv8 machine.
- [firmware/](firmware/README.md) — Packages Qualcomm camera, Wi-Fi, and board firmware files.
- [firmware-boot/](firmware-boot/README.md) — Deploys the prebuilt boot firmware and CDT binaries flashed with each image.
- [hexagon-dsp-binaries/](hexagon-dsp-binaries/README.md) — Packages the Hexagon DSP libraries and executables used through FastRPC.
- [images/](images/README.md) — Builds small initramfs images that carry each board's firmware files.
- [lk/](lk/README.md) — Builds the Little Kernel bootloader for the DragonBoard 410c and 820c.
- [packagegroups/](packagegroups/README.md) — Groups the firmware and support packages each board needs.
- [partition/](partition/README.md) — Generates GPT partition files and mounts the persist partition for the TEE.
- [u-boot/](u-boot/README.md) — Builds U-Boot for Qualcomm boards and its FIT boot script.

## Files

- [README.md](README.md) — Indexes this folder.
