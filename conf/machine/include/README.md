# conf/machine/include

Settings shared by machines: each SoC family's include, the common Qualcomm settings, and the FIT device tree tables.

## Files

- [fit-dtb-compatible-linux-qcom.inc](fit-dtb-compatible-linux-qcom.inc) — Adds FIT_DTB_COMPATIBLE entries for overlays that only the linux-qcom kernels build.
- [fit-dtb-compatible.inc](fit-dtb-compatible.inc) — Maps each device tree compatible string to its DTB and overlays for the FIT image.
- [qcom-apq8016.inc](qcom-apq8016.inc) — Sets up the APQ8016 SoC family.
- [qcom-apq8064.inc](qcom-apq8064.inc) — Sets up the APQ8064 SoC family.
- [qcom-apq8096.inc](qcom-apq8096.inc) — Sets up the APQ8096 SoC family.
- [qcom-base.inc](qcom-base.inc) — Sets the kernel, image types, qcomflash package, and root device shared by current Qualcomm SoCs.
- [qcom-common-binary.inc](qcom-common-binary.inc) — Pins the versions of the binary recipes.
- [qcom-common.inc](qcom-common.inc) — Sets machine features, device trees, boot image, DTB image, console, and real-time settings for every Qualcomm machine.
- [qcom-glymur.inc](qcom-glymur.inc) — Sets up the Glymur SoC family.
- [qcom-hamoa.inc](qcom-hamoa.inc) — Sets up the Hamoa SoC family.
- [qcom-kaanapali.inc](qcom-kaanapali.inc) — Sets up the Kaanapali SoC family.
- [qcom-purwa.inc](qcom-purwa.inc) — Sets up the Purwa SoC family.
- [qcom-qcm2290.inc](qcom-qcm2290.inc) — Sets up the QCM2290 (QRB2210) SoC family.
- [qcom-qcs404.inc](qcom-qcs404.inc) — Sets up the QCS404 SoC family.
- [qcom-qcs615.inc](qcom-qcs615.inc) — Sets up the QCS615 SoC family.
- [qcom-qcs6490.inc](qcom-qcs6490.inc) — Sets up the QCS6490 SoC family.
- [qcom-qcs8300.inc](qcom-qcs8300.inc) — Sets up the QCS8300 SoC family.
- [qcom-qcs9100.inc](qcom-qcs9100.inc) — Sets up the QCS9100 SoC family.
- [qcom-sa8155p.inc](qcom-sa8155p.inc) — Sets up the SA8155P SoC family.
- [qcom-sdm845.inc](qcom-sdm845.inc) — Sets up the SDM845 SoC family.
- [qcom-sdx55.inc](qcom-sdx55.inc) — Sets up the SDX55 SoC family.
- [qcom-sdx75.inc](qcom-sdx75.inc) — Sets up the SDX75 SoC family.
- [qcom-shikra.inc](qcom-shikra.inc) — Sets up the Shikra SoC family.
- [qcom-sm8250.inc](qcom-sm8250.inc) — Sets up the SM8250 SoC family.
- [qcom-sm8750.inc](qcom-sm8750.inc) — Sets up the SM8750 SoC family.
- [qcom-u-boot-common.inc](qcom-u-boot-common.inc) — Maps each U-Boot configuration to its defconfig and MBN header version.
- [qcom-uboot-spl-fit.inc](qcom-uboot-spl-fit.inc) — Switches a machine to the U-Boot SPL FIT boot flow.
- [README.md](README.md) — Introduces this folder and indexes its contents.
