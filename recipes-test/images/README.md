# images

Initramfs image recipes for board bring-up and tests, each building on the previous one: tiny, test, test-full, and the kerneltest variants that add the machine's essential packages.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [initramfs-kerneltest-full-image.bb](initramfs-kerneltest-full-image.bb) — `initramfs-test-full-image` plus the machine's essential packages from `MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS`.
- [initramfs-kerneltest-image.bb](initramfs-kerneltest-image.bb) — `initramfs-test-image` plus the machine's essential packages, without the `qairt-sdk-hexagon` packages.
- [initramfs-test-full-image.bb](initramfs-test-full-image.bb) — Larger test ramdisk that adds tools such as stress-ng, igt-gpu-tools tests, kexec, FastRPC and real-time tests, and benchmarks from optional layers to `initramfs-test-image`.
- [initramfs-test-image.bb](initramfs-test-image.bb) — Small test ramdisk that adds bootrr, adbd, a diag router, networking, audio, Bluetooth, and storage tools, and `mybw` to `initramfs-tiny-image`.
- [initramfs-tiny-image.bb](initramfs-tiny-image.bb) — Tiny ramdisk for board bring-up with busybox, udev, `debugcc`, the Qualcomm boot packagegroups, and root auto-login on the console under systemd; it also installs `PACKAGE_INSTALL_<layer>` packages for each optional layer in the build.
