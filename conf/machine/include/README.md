# Machine include files

Shared machine settings: one include per SoC family, which a machine
configuration requires, and the common files those SoC includes require.

## Files

- [README.md](README.md) — Indexes this folder.
- [fit-dtb-compatible-linux-qcom.inc](fit-dtb-compatible-linux-qcom.inc) — Adds FIT compatible entries for device trees that only the linux-qcom kernels build.
- [fit-dtb-compatible.inc](fit-dtb-compatible.inc) — Maps device tree compatible strings to the DTB and overlays that the multi-DTB FIT image includes.
- [qcom-apq8016.inc](qcom-apq8016.inc) — Sets the APQ8016 SoC family, CPU tune, and SoC package groups.
- [qcom-apq8064.inc](qcom-apq8064.inc) — Sets the APQ8064 SoC family, CPU tune, and SoC package groups.
- [qcom-apq8096.inc](qcom-apq8096.inc) — Sets the APQ8096 SoC family, CPU tune, and SoC package groups.
- [qcom-base.inc](qcom-base.inc) — Sets the kernel provider and image types, the dtb.bin class, and the ext4 and qcomflash image formats shared by current SoCs.
- [qcom-common-binary.inc](qcom-common-binary.inc) — Pins the abseil-cpp and protobuf versions that the binary recipes need.
- [qcom-common.inc](qcom-common.inc) — Sets the shared machine features, device tree, boot image, EFI, FIT, and real-time kernel defaults.
- [qcom-glymur.inc](qcom-glymur.inc) — Sets the Glymur SoC family, CPU tune, and SoC package groups.
- [qcom-hamoa.inc](qcom-hamoa.inc) — Sets the Hamoa SoC family, CPU tune, and SoC package groups.
- [qcom-kaanapali.inc](qcom-kaanapali.inc) — Sets the Kaanapali SoC family, CPU tune, and SoC package groups.
- [qcom-purwa.inc](qcom-purwa.inc) — Sets the Purwa SoC family, CPU tune, and SoC package groups.
- [qcom-qcm2290.inc](qcom-qcm2290.inc) — Sets the QCM2290 (QRB2210) SoC family, CPU tune, and SoC package groups.
- [qcom-qcs404.inc](qcom-qcs404.inc) — Sets the QCS404 SoC family, CPU tune, and SoC package groups.
- [qcom-qcs615.inc](qcom-qcs615.inc) — Sets the QCS615 SoC family, CPU tune, and SoC package groups.
- [qcom-qcs6490.inc](qcom-qcs6490.inc) — Sets the QCS6490 SoC family, CPU tune, and SoC package groups.
- [qcom-qcs8300.inc](qcom-qcs8300.inc) — Sets the QCS8300 SoC family, CPU tune, and SoC package groups.
- [qcom-qcs9100.inc](qcom-qcs9100.inc) — Sets the QCS9100 SoC family, CPU tune, and SoC package groups.
- [qcom-sa8155p.inc](qcom-sa8155p.inc) — Sets the SA8155P SoC family, CPU tune, and SoC package groups.
- [qcom-sdm845.inc](qcom-sdm845.inc) — Sets the SDM845 SoC family, CPU tune, and SoC package groups.
- [qcom-sdx55.inc](qcom-sdx55.inc) — Sets the SDX55 SoC family, CPU tune, and SoC package groups.
- [qcom-sdx75.inc](qcom-sdx75.inc) — Sets the SDX75 SoC family, CPU tune, and SoC package groups.
- [qcom-shikra.inc](qcom-shikra.inc) — Sets the Shikra SoC family, CPU tune, and SoC package groups.
- [qcom-sm8250.inc](qcom-sm8250.inc) — Sets the SM8250 SoC family, CPU tune, and SoC package groups.
- [qcom-sm8750.inc](qcom-sm8750.inc) — Sets the SM8750 SoC family, CPU tune, and SoC package groups.
- [qcom-u-boot-common.inc](qcom-u-boot-common.inc) — Maps U-Boot boards to their defconfigs and MBN header versions.
- [qcom-uboot-spl-fit.inc](qcom-uboot-spl-fit.inc) — Enables the U-Boot SPL FIT boot flow for machines that opt in.
