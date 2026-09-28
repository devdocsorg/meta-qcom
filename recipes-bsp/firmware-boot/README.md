# Boot firmware

Recipes that deploy prebuilt non-HLOS boot binaries and CDT (Configuration Data Table) files for the flashable image.

## Files

- [README.md](README.md) — Indexes this folder.
- [firmware-qcom-boot-common.inc](firmware-qcom-boot-common.inc) — Shared deploy task that copies the boot firmware binaries into the deploy directory.
- [firmware-qcom-boot-dragonboard410c-sdcard_17.09.bb](firmware-qcom-boot-dragonboard410c-sdcard_17.09.bb) — Deploys the prebuilt SD-card bootloader images for the DragonBoard 410c.
- [firmware-qcom-boot-dragonboard410c_1036.1.bb](firmware-qcom-boot-dragonboard410c_1036.1.bb) — Deploys the prebuilt bootloader images and firehose programmer for the DragonBoard 410c.
- [firmware-qcom-boot-dragonboard820c_01700.1.bb](firmware-qcom-boot-dragonboard820c_01700.1.bb) — Deploys the prebuilt bootloader images and firehose programmer for the DragonBoard 820c.
- [firmware-qcom-boot-glymur.inc](firmware-qcom-boot-glymur.inc) — Sets the download location, licence, and deploy subdirectory of the Glymur CRD boot firmware.
- [firmware-qcom-boot-glymur_00084.bb](firmware-qcom-boot-glymur_00084.bb) — Selects Glymur CRD boot firmware release 00084 and pins its download checksums.
- [firmware-qcom-boot-iq-x7181.inc](firmware-qcom-boot-iq-x7181.inc) — Sets the download location, licence, and deploy subdirectory of the IQ-X7181 EVK boot firmware.
- [firmware-qcom-boot-iq-x7181_00028.bb](firmware-qcom-boot-iq-x7181_00028.bb) — Selects IQ-X7181 EVK boot firmware release 00028 and pins its download checksums.
- [firmware-qcom-boot-kaanapali.inc](firmware-qcom-boot-kaanapali.inc) — Sets the download location, licence, and deploy subdirectory of the Kaanapali MTP boot firmware.
- [firmware-qcom-boot-kaanapali_00036.bb](firmware-qcom-boot-kaanapali_00036.bb) — Selects Kaanapali MTP boot firmware release 00036 and pins its download checksums.
- [firmware-qcom-boot-qcs615.inc](firmware-qcom-boot-qcs615.inc) — Sets the download location, licence, and deploy subdirectory of the QCS615 boot firmware.
- [firmware-qcom-boot-qcs615_00142.bb](firmware-qcom-boot-qcs615_00142.bb) — Selects QCS615 boot firmware release 00142 and pins its download checksums.
- [firmware-qcom-boot-qcs6490.inc](firmware-qcom-boot-qcs6490.inc) — Sets the download location, licence, and deploy subdirectory of the QCS6490 (RB3 Gen 2) boot firmware.
- [firmware-qcom-boot-qcs6490_00142.bb](firmware-qcom-boot-qcs6490_00142.bb) — Selects QCS6490 (RB3 Gen 2) boot firmware release 00142 and pins its download checksums.
- [firmware-qcom-boot-qcs8300.inc](firmware-qcom-boot-qcs8300.inc) — Sets the download location, licence, and deploy subdirectory of the QCS8300 boot firmware.
- [firmware-qcom-boot-qcs8300_00142.bb](firmware-qcom-boot-qcs8300_00142.bb) — Selects QCS8300 boot firmware release 00142 and pins its download checksums.
- [firmware-qcom-boot-qcs9100.inc](firmware-qcom-boot-qcs9100.inc) — Sets the download location, licence, and deploy subdirectory of the QCS9100 boot firmware.
- [firmware-qcom-boot-qcs9100_00142.bb](firmware-qcom-boot-qcs9100_00142.bb) — Selects QCS9100 boot firmware release 00142 and pins its download checksums.
- [firmware-qcom-boot-qrb2210-rb1_23.12.bb](firmware-qcom-boot-qrb2210-rb1_23.12.bb) — Deploys the prebuilt bootloader images for the Qualcomm RB1.
- [firmware-qcom-boot-qrb2210.inc](firmware-qcom-boot-qrb2210.inc) — Sets the download location, licence, and deploy subdirectory of the QRB2210 boot firmware.
- [firmware-qcom-boot-qrb2210_00021.bb](firmware-qcom-boot-qrb2210_00021.bb) — Selects QRB2210 boot firmware release 00021 and pins its download checksums.
- [firmware-qcom-boot-shikra.inc](firmware-qcom-boot-shikra.inc) — Sets the download location, licence, and deploy subdirectory of the Shikra EVK boot firmware.
- [firmware-qcom-boot-shikra_00086.bb](firmware-qcom-boot-shikra_00086.bb) — Selects Shikra EVK boot firmware release 00086 and pins its download checksums.
- [firmware-qcom-boot-sm8750.inc](firmware-qcom-boot-sm8750.inc) — Sets the download location, licence, and deploy subdirectory of the SM8750 MTP boot firmware.
- [firmware-qcom-boot-sm8750_00045.bb](firmware-qcom-boot-sm8750_00045.bb) — Selects SM8750 MTP boot firmware release 00045 and pins its download checksums.
- [firmware-qcom-cdt-common.inc](firmware-qcom-cdt-common.inc) — Shared deploy task that copies CDT binaries into the deploy directory.
- [firmware-qcom-cdt-glymur.bb](firmware-qcom-cdt-glymur.bb) — Deploys the CDT (Configuration Data Table) binaries for Glymur CRD.
- [firmware-qcom-cdt-iq-x7181.bb](firmware-qcom-cdt-iq-x7181.bb) — Deploys the CDT (Configuration Data Table) binaries for IQ-X7181 EVK.
- [firmware-qcom-cdt-kaanapali.bb](firmware-qcom-cdt-kaanapali.bb) — Deploys the CDT (Configuration Data Table) binaries for Kaanapali MTP.
- [firmware-qcom-cdt-qcs615.bb](firmware-qcom-cdt-qcs615.bb) — Deploys the CDT (Configuration Data Table) binaries for QCS615.
- [firmware-qcom-cdt-qcs6490.bb](firmware-qcom-cdt-qcs6490.bb) — Deploys the CDT (Configuration Data Table) binaries for QCS6490 (RB3 Gen 2).
- [firmware-qcom-cdt-qcs8300.bb](firmware-qcom-cdt-qcs8300.bb) — Deploys the CDT (Configuration Data Table) binaries for QCS8300.
- [firmware-qcom-cdt-qcs9100.bb](firmware-qcom-cdt-qcs9100.bb) — Deploys the CDT (Configuration Data Table) binaries for QCS9100.
- [firmware-qcom-cdt-qrb2210.bb](firmware-qcom-cdt-qrb2210.bb) — Deploys the CDT (Configuration Data Table) binaries for QRB2210.
- [firmware-qcom-cdt-shikra.bb](firmware-qcom-cdt-shikra.bb) — Deploys the CDT (Configuration Data Table) binaries for Shikra EVK.
- [firmware-qcom-cdt-sm8750.bb](firmware-qcom-cdt-sm8750.bb) — Deploys the CDT (Configuration Data Table) binaries for SM8750 MTP.
