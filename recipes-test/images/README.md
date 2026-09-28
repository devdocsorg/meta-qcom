# Test images

Initramfs image recipes for board bring-up and running tests.

## Files

- [initramfs-kerneltest-full-image.bb](initramfs-kerneltest-full-image.bb) — Extends the full test image with the machine's essential packages.
- [initramfs-kerneltest-image.bb](initramfs-kerneltest-image.bb) — Extends the test image with the machine's essential packages except the QAIRT Hexagon libraries.
- [initramfs-test-full-image.bb](initramfs-test-full-image.bb) — Builds a larger ramdisk for running tests such as bootrr.
- [initramfs-test-image.bb](initramfs-test-image.bb) — Builds a small ramdisk for running tests such as bootrr.
- [initramfs-tiny-image.bb](initramfs-tiny-image.bb) — Builds a tiny ramdisk for board bring-up with root auto-login.
- [README.md](README.md) — Indexes this folder.
