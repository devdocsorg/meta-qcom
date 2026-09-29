# images

Image recipes for tiny initramfs images that contain only a board's firmware files. Each image requires the shared `initramfs-firmware-image.inc` and adds the board's firmware packagegroup to `PACKAGE_INSTALL`.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [initramfs-firmware-dragonboard410c-image.bb](initramfs-firmware-dragonboard410c-image.bb) — Builds a tiny initramfs with the DragonBoard 410c firmware from `packagegroup-dragonboard410c-firmware`.
- [initramfs-firmware-dragonboard820c-image.bb](initramfs-firmware-dragonboard820c-image.bb) — Builds a tiny initramfs with the DragonBoard 820c firmware from `packagegroup-dragonboard820c-firmware`.
- [initramfs-firmware-dragonboard845c-image.bb](initramfs-firmware-dragonboard845c-image.bb) — Builds a tiny initramfs with the DragonBoard 845c firmware from `packagegroup-dragonboard845c-firmware`.
- [initramfs-firmware-glymur-crd-image.bb](initramfs-firmware-glymur-crd-image.bb) — Builds a tiny initramfs with the Glymur CRD firmware from `packagegroup-glymur-crd-firmware`.
- [initramfs-firmware-image.inc](initramfs-firmware-image.inc) — Shared by all `initramfs-firmware-*-image.bb` recipes; inherits `core-image`, builds in the `INITRAMFS_FSTYPES` formats, drops the kernel dependencies, fixes the root filesystem size at 8192 KB with no extra space, and does not install `/init`.
- [initramfs-firmware-iq-x5121-evk-image.bb](initramfs-firmware-iq-x5121-evk-image.bb) — Builds a tiny initramfs with the IQ-X5121 EVK firmware from `packagegroup-purwa-iot-evk-firmware`.
- [initramfs-firmware-iq-x7181-evk-image.bb](initramfs-firmware-iq-x7181-evk-image.bb) — Builds a tiny initramfs with the IQ-X7181 EVK firmware from `packagegroup-hamoa-iot-evk-firmware`.
- [initramfs-firmware-kaanapali-mtp-image.bb](initramfs-firmware-kaanapali-mtp-image.bb) — Builds a tiny initramfs with the Kaanapali MTP firmware from `packagegroup-kaanapali-mtp-firmware`.
- [initramfs-firmware-mega-image.bb](initramfs-firmware-mega-image.bb) — Builds a large image with `linux-firmware` and the firmware and Hexagon DSP packagegroups of many boards, to check their files for conflicts.
- [initramfs-firmware-qcs615-ride-image.bb](initramfs-firmware-qcs615-ride-image.bb) — Builds a tiny initramfs with the QCS615 Ride firmware from `packagegroup-qcs615-ride-firmware`.
- [initramfs-firmware-qcs8300-ride-image.bb](initramfs-firmware-qcs8300-ride-image.bb) — Builds a tiny initramfs with the QCS8300 Ride firmware from `packagegroup-qcs8300-ride-firmware`.
- [initramfs-firmware-rb1-image.bb](initramfs-firmware-rb1-image.bb) — Builds a tiny initramfs with the RB1 firmware from `packagegroup-rb1-firmware`, leaving out the recommended `linux-firmware-qcom-venus-6.0`.
- [initramfs-firmware-rb2-image.bb](initramfs-firmware-rb2-image.bb) — Builds a tiny initramfs with the RB2 firmware from `packagegroup-rb2-firmware`, leaving out the recommended `linux-firmware-qcom-venus-6.0`.
- [initramfs-firmware-rb3gen2-image.bb](initramfs-firmware-rb3gen2-image.bb) — Builds a tiny initramfs with the RB3 Gen2 firmware from `packagegroup-rb3gen2-firmware`.
- [initramfs-firmware-rb5-image.bb](initramfs-firmware-rb5-image.bb) — Builds a tiny initramfs with the RB5 firmware from `packagegroup-rb5-firmware`.
- [initramfs-firmware-sa8775p-ride-image.bb](initramfs-firmware-sa8775p-ride-image.bb) — Builds a tiny initramfs with the SA8775P Ride firmware from `packagegroup-sa8775p-ride-firmware`.
- [initramfs-firmware-shikra-evk-image.bb](initramfs-firmware-shikra-evk-image.bb) — Builds a tiny initramfs with the Shikra EVK firmware from `packagegroup-shikra-evk-firmware`.
- [initramfs-firmware-sm8750-mtp-image.bb](initramfs-firmware-sm8750-mtp-image.bb) — Builds a tiny initramfs with the SM8750 MTP firmware from `packagegroup-sm8750-mtp-firmware`.
