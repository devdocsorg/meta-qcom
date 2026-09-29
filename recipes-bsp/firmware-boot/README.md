# firmware-boot

Recipes that fetch prebuilt Qualcomm boot firmware (NHLOS boot binaries) and CDT (Configuration Data Table) files and copy them into a per-platform subdirectory of the image deploy directory through a `do_deploy` task. Each versioned recipe that requires a platform `.inc` sets only the archive checksums and takes everything else from that `.inc`.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [firmware-qcom-boot-common.inc](firmware-qcom-boot-common.inc) — Shared by all `firmware-qcom-boot-*` recipes; skips configure and compile and deploys the `.bin`, `.elf`, `.fv`, `.lzma`, `.mbn`, `.melf`, `.xz`, and `qsahara_*.xml` files of the main archive and optional immutable archive into `QCOM_BOOT_IMG_SUBDIR`, leaving out `gpt_*.bin` and `zeros_*.bin`.
- [firmware-qcom-boot-dragonboard410c-sdcard_17.09.bb](firmware-qcom-boot-dragonboard410c-sdcard_17.09.bb) — Deploys the prebuilt DragonBoard 410c SD card bootloader images from the 17.09 rescue release into `dragonboard410c`.
- [firmware-qcom-boot-dragonboard410c_1036.1.bb](firmware-qcom-boot-dragonboard410c_1036.1.bb) — Deploys the DragonBoard 410c bootloaders, CDT, EFS seed image, and eMMC firehose programmer from board support package r1036.1 into `dragonboard-410c`, after building `lk-db410c`.
- [firmware-qcom-boot-dragonboard820c_01700.1.bb](firmware-qcom-boot-dragonboard820c_01700.1.bb) — Deploys the DragonBoard 820c bootloaders, CDT, and UFS firehose programmer from board support package r01700.1 into `dragonboard-820c`, after building `lk-db820c`.
- [firmware-qcom-boot-glymur.inc](firmware-qcom-boot-glymur.inc) — Shared by `firmware-qcom-boot-glymur_*.bb`; fetches the Glymur boot binaries and license and deploys the `spinor` files into `glymur-crd/spinor`.
- [firmware-qcom-boot-glymur_00084.bb](firmware-qcom-boot-glymur_00084.bb) — Glymur CRD boot binaries, release 00084.
- [firmware-qcom-boot-iq-x7181.inc](firmware-qcom-boot-iq-x7181.inc) — Shared by `firmware-qcom-boot-iq-x7181_*.bb`; fetches the Hamoa boot binaries, their immutable companion archive, and the license, and deploys them into `iq-x7181/spinor`.
- [firmware-qcom-boot-iq-x7181_00028.bb](firmware-qcom-boot-iq-x7181_00028.bb) — IQ-X7181 boot binaries, release 00028.
- [firmware-qcom-boot-kaanapali.inc](firmware-qcom-boot-kaanapali.inc) — Shared by `firmware-qcom-boot-kaanapali_*.bb`; fetches the Kaanapali MTP boot binaries and deploys them into `kaanapali`.
- [firmware-qcom-boot-kaanapali_00036.bb](firmware-qcom-boot-kaanapali_00036.bb) — Kaanapali MTP boot binaries, release 00036.
- [firmware-qcom-boot-qcs615.inc](firmware-qcom-boot-qcs615.inc) — Shared by `firmware-qcom-boot-qcs615_*.bb`; fetches the QCS615 boot binaries and deploys them into `qcs615`.
- [firmware-qcom-boot-qcs615_00142.bb](firmware-qcom-boot-qcs615_00142.bb) — QCS615 boot binaries, release 00142.
- [firmware-qcom-boot-qcs6490.inc](firmware-qcom-boot-qcs6490.inc) — Shared by `firmware-qcom-boot-qcs6490_*.bb`; fetches the QCM6490 boot binaries and their immutable companion archive for the RB3 Gen2 platform and deploys them into `qcm6490`.
- [firmware-qcom-boot-qcs6490_00142.bb](firmware-qcom-boot-qcs6490_00142.bb) — QCS6490 boot binaries, release 00142.
- [firmware-qcom-boot-qcs8300.inc](firmware-qcom-boot-qcs8300.inc) — Shared by `firmware-qcom-boot-qcs8300_*.bb`; fetches the QCS8300 boot binaries and their immutable companion archive, deploys them into `qcs8300`, and also deploys the SAIL NOR flashing files into `qcs8300/sail_nor` when the archive has them.
- [firmware-qcom-boot-qcs8300_00142.bb](firmware-qcom-boot-qcs8300_00142.bb) — QCS8300 boot binaries, release 00142.
- [firmware-qcom-boot-qcs9100.inc](firmware-qcom-boot-qcs9100.inc) — Shared by `firmware-qcom-boot-qcs9100_*.bb`; fetches the QCS9100 boot binaries and their immutable companion archive, deploys them into `qcs9100`, and also deploys the SAIL NOR flashing files into `qcs9100/sail_nor` when the archive has them.
- [firmware-qcom-boot-qcs9100_00142.bb](firmware-qcom-boot-qcs9100_00142.bb) — QCS9100 boot binaries, release 00142.
- [firmware-qcom-boot-qrb2210-rb1_23.12.bb](firmware-qcom-boot-qrb2210-rb1_23.12.bb) — Deploys the prebuilt RB1 eMMC bootloader images from the 23.12 rescue release into `qrb2210-rb1`.
- [firmware-qcom-boot-qrb2210.inc](firmware-qcom-boot-qrb2210.inc) — Shared by `firmware-qcom-boot-qrb2210_*.bb`; fetches the QRB2210 (Agatti) boot binaries and deploys them into `qrb2210`.
- [firmware-qcom-boot-qrb2210_00021.bb](firmware-qcom-boot-qrb2210_00021.bb) — QRB2210 boot binaries, release 00021.
- [firmware-qcom-boot-shikra.inc](firmware-qcom-boot-shikra.inc) — Shared by `firmware-qcom-boot-shikra_*.bb`; fetches the Shikra EVK boot binaries and deploys them into `shikra`.
- [firmware-qcom-boot-shikra_00086.bb](firmware-qcom-boot-shikra_00086.bb) — Shikra EVK boot binaries, release 00086.
- [firmware-qcom-boot-sm8750.inc](firmware-qcom-boot-sm8750.inc) — Shared by `firmware-qcom-boot-sm8750_*.bb`; fetches the SM8750 MTP (Pakala) boot binaries and deploys them into `sm8750`.
- [firmware-qcom-boot-sm8750_00045.bb](firmware-qcom-boot-sm8750_00045.bb) — SM8750 MTP boot binaries, release 00045.
- [firmware-qcom-cdt-common.inc](firmware-qcom-cdt-common.inc) — Shared by all `firmware-qcom-cdt-*` recipes; sets the Qualcomm Linux CDT download location and deploys every `*cdt*.bin` file it unpacks into `QCOM_CDT_SUBDIR`.
- [firmware-qcom-cdt-glymur.bb](firmware-qcom-cdt-glymur.bb) — Deploys the SC8480XP CRD (Glymur) CDT into `glymur-crd/spinor`.
- [firmware-qcom-cdt-iq-x7181.bb](firmware-qcom-cdt-iq-x7181.bb) — Deploys the IQ-X7181 (Hamoa) EVK CDT into `iq-x7181/spinor`.
- [firmware-qcom-cdt-kaanapali.bb](firmware-qcom-cdt-kaanapali.bb) — Deploys the SM8850 MTP (Kaanapali) CDT into `kaanapali`.
- [firmware-qcom-cdt-qcs615.bb](firmware-qcom-cdt-qcs615.bb) — Deploys the QCS615 ADP Air and IQ-615 EVK CDTs into `qcs615`.
- [firmware-qcom-cdt-qcs6490.bb](firmware-qcom-cdt-qcs6490.bb) — Deploys the QCM6490 IDP CDT and the RB3 Gen2 core, industrial, vision, and industrial mezzanine kit CDTs into `qcm6490`.
- [firmware-qcom-cdt-qcs8300.bb](firmware-qcom-cdt-qcs8300.bb) — Deploys the QCS8300 Ride SX and IQ-8275 EVK pro SKU CDTs into `qcs8300`.
- [firmware-qcom-cdt-qcs9100.bb](firmware-qcom-cdt-qcs9100.bb) — Deploys the QCS9100 Ride SX v3 and RB8 core kit CDTs into `qcs9100`.
- [firmware-qcom-cdt-qrb2210.bb](firmware-qcom-cdt-qrb2210.bb) — Deploys the RB1 core kit CDT into `qrb2210`.
- [firmware-qcom-cdt-shikra.bb](firmware-qcom-cdt-shikra.bb) — Deploys the CQ2390 and IQ2390 ITP CDTs for the Shikra EVK into `shikra`.
- [firmware-qcom-cdt-sm8750.bb](firmware-qcom-cdt-sm8750.bb) — Deploys the SM8750 MTP (WCN7881) CDT into `sm8750`.
