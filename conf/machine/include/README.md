# include

SoC includes and shared settings that the machine files in `conf/machine/` pull in with `require conf/machine/include/<file>`. A SoC include sets `SOC_FAMILY`, the CPU tuning, and the packages every board with that SoC needs.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [fit-dtb-compatible-linux-qcom.inc](fit-dtb-compatible-linux-qcom.inc) — Extends `fit-dtb-compatible.inc` with `FIT_DTB_COMPATIBLE` entries whose overlays exist only in the linux-qcom kernels, which select it through `LINUX_QCOM_FIT_DTB_COMPATIBLE`.
- [fit-dtb-compatible.inc](fit-dtb-compatible.inc) — Maps devicetree compatible strings to the DTB and overlays of each FIT configuration (`FIT_DTB_COMPATIBLE`) for `dtb-fit-image.bbclass`.
- [qcom-apq8016.inc](qcom-apq8016.inc) — APQ8016 SoC settings: Cortex-A53 tuning, `qrtr`, `rmtfs`, and `fastrpc`, and 2048-byte boot image pages; no machine in this layer requires it.
- [qcom-apq8064.inc](qcom-apq8064.inc) — APQ8064 SoC settings: Cortex-A15 tuning and 2048-byte boot image pages; no machine in this layer requires it.
- [qcom-apq8096.inc](qcom-apq8096.inc) — APQ8096 SoC settings: ARMv8-A CRC and crypto tuning, `qrtr`, `rmtfs`, and `fastrpc`; no machine in this layer requires it.
- [qcom-base.inc](qcom-base.inc) — Defaults shared by the current SoC includes: the `linux-qcom-next` kernel, DTB image generation, the 4096-aligned ext4 and `qcomflash` image types, and the serial console.
- [qcom-common-binary.inc](qcom-common-binary.inc) — Sets the `abseil-cpp` and `protobuf` versions that the prebuilt binary recipes are built against; required by `qcom-common.inc`.
- [qcom-common.inc](qcom-common.inc) — Settings every Qualcomm machine requires: the `qcom` machine override, default machine features, the linux-qcom-only devicetrees, XBL config and UEFI DTB selection, boot image and FIT options, and systemd-boot as the EFI provider.
- [qcom-glymur.inc](qcom-glymur.inc) — Glymur SoC settings: ARMv8.6-A tuning, the Glymur boot packagegroups, and no systemd wait for the TPM; used by `glymur-crd`.
- [qcom-hamoa.inc](qcom-hamoa.inc) — Hamoa SoC settings: ARMv8.6-A tuning and the Hamoa boot packagegroups; used by `iq-x7181-evk`.
- [qcom-kaanapali.inc](qcom-kaanapali.inc) — Kaanapali SoC settings: ARMv8.6-A tuning and the boot packagegroup; used by `kaanapali-mtp`.
- [qcom-purwa.inc](qcom-purwa.inc) — Purwa SoC settings: ARMv8.6-A tuning and the Purwa boot packagegroups; used by `iq-x5121-evk`.
- [qcom-qcm2290.inc](qcom-qcm2290.inc) — QCM2290 (QRB2210) SoC settings: Cortex-A53 tuning, 512-byte VFAT sectors, and the SoC boot packagegroups; used by `rb1-core-kit`.
- [qcom-qcs404.inc](qcom-qcs404.inc) — QCS404 SoC settings: ARMv8-A tuning and `qrtr`; no machine in this layer requires it.
- [qcom-qcs615.inc](qcom-qcs615.inc) — QCS615 SoC settings: ARMv8.2-A tuning and the QCS615 boot packagegroups; used by `iq-615-evk` and `qcs615-ride`.
- [qcom-qcs6490.inc](qcom-qcs6490.inc) — QCS6490 SoC settings (`SOC_FAMILY` `qcm6490`): ARMv8.2-A tuning and the QCS6490 boot packagegroups; used by `rb3gen2-core-kit` and `qcm6490-idp`.
- [qcom-qcs8300.inc](qcom-qcs8300.inc) — QCS8300 SoC settings: ARMv8.2-A tuning, `arm64.nopauth` so every core boots with KVM, and the QCS8300 boot packagegroups; used by `iq-8275-evk` and `qcs8300-ride-sx`.
- [qcom-qcs9100.inc](qcom-qcs9100.inc) — QCS9100 SoC settings: ARMv8.2-A tuning, the QCS9100 boot packagegroups, and the load addresses and TF-A and OP-TEE recipes for the SPL FIT boot flow; used by `iq-9075-evk` and `qcs9100-ride-sx`.
- [qcom-sa8155p.inc](qcom-sa8155p.inc) — SA8155P SoC settings: ARMv8.2-A tuning and the boot packagegroups; no machine in this layer requires it.
- [qcom-sdm845.inc](qcom-sdm845.inc) — SDM845 SoC settings: ARMv8.2-A tuning and the boot packagegroups; no machine in this layer requires it.
- [qcom-sdx55.inc](qcom-sdx55.inc) — SDX55 SoC settings: Cortex-A7 tuning, `qrtr` and `rmtfs`, and UBI images; no machine in this layer requires it.
- [qcom-sdx75.inc](qcom-sdx75.inc) — SDX75 SoC settings: Cortex-A55 tuning, the `linux-qcom-next` kernel, the `qrtr`, `rmtfs`, `tqftpserv`, and `pd-mapper` services, and UBI images; used by `sdx75-idp`.
- [qcom-shikra.inc](qcom-shikra.inc) — Shikra SoC settings: ARMv8.2-A tuning and the Shikra boot packagegroups; used by `shikra-evk`.
- [qcom-sm8250.inc](qcom-sm8250.inc) — SM8250 SoC settings: ARMv8.2-A tuning and the boot packagegroups; no machine in this layer requires it.
- [qcom-sm8750.inc](qcom-sm8750.inc) — SM8750 SoC settings: ARMv8.6-A tuning and the boot packagegroup; used by `sm8750-mtp`.
- [qcom-u-boot-common.inc](qcom-u-boot-common.inc) — U-Boot defconfig and MBN header version for each `UBOOT_CONFIG` board name, plus the U-Boot entry points; required by `qcom-common.inc`.
- [qcom-uboot-spl-fit.inc](qcom-uboot-spl-fit.inc) — Opt-in SPL FIT boot flow, where the XBL loads a U-Boot SPL that loads a FIT holding BL31, OP-TEE, and U-Boot; required by `iq-9075-evk-open-fw-spl.conf`.
