# recipes-bsp

Board support recipes for Qualcomm machines: boot firmware, device firmware, bootloaders, partition layouts, firmware images, and the packagegroups that machine configurations install. BitBake parses the `.bb` and `.bbappend` files in these subfolders through the layer's `recipes-*/*/*.bb` and `recipes-*/*/*.bbappend` patterns.

## Folders

- [devicetree/](devicetree/README.md) — Placeholder device tree recipe for the generic `qcom-armv8` machine.
- [firmware/](firmware/README.md) — Camera firmware, ath6kl firmware, and placeholder board firmware recipes that install files under `/lib/firmware`.
- [firmware-boot/](firmware-boot/README.md) — Prebuilt boot binaries and CDT (Configuration Data Table) files that are deployed for flashing.
- [hexagon-dsp-binaries/](hexagon-dsp-binaries/README.md) — Hexagon DSP libraries and executables, split into one package per board and DSP.
- [images/](images/README.md) — Tiny initramfs images that carry only a board's firmware files.
- [lk/](lk/README.md) — Little Kernel (LK) bootloader for DragonBoard 410c and 820c.
- [packagegroups/](packagegroups/README.md) — Packagegroups that collect per-board firmware, Hexagon DSP binaries, kernel modules, and core Qualcomm userspace.
- [partition/](partition/README.md) — Partition tables and flashing files, raw-partition udev rules, and the `persist` partition mount.
- [u-boot/](u-boot/README.md) — Qualcomm U-Boot build, FIT boot script, and the U-Boot bbappend for Qualcomm machines.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
