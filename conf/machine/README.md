# machine

Machine configurations for Qualcomm boards; set `MACHINE` to a file name without `.conf`. Each file requires a SoC include from `include/` and sets the board's devicetrees, firmware packages, and boot and partition files.

## Folders

- [include/](include/README.md) — SoC includes and settings shared by the machine files.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [glymur-crd.conf](glymur-crd.conf) — Qualcomm Glymur Compute Reference Device.
- [iq-615-evk.conf](iq-615-evk.conf) — Qualcomm IQ-615 Evaluation Kit, based on QCS615.
- [iq-8275-evk.conf](iq-8275-evk.conf) — Qualcomm IQ-8275 Evaluation Kit, based on QCS8275.
- [iq-9075-evk-open-fw-spl.conf](iq-9075-evk-open-fw-spl.conf) — IQ-9075 Evaluation Kit with open boot firmware, booting through a U-Boot SPL instead of the TF-A BL2/FIP loader.
- [iq-9075-evk-open-fw.conf](iq-9075-evk-open-fw.conf) — IQ-9075 Evaluation Kit with open boot firmware: adds TF-A and OP-TEE and uses `u-boot-qcom` as the bootloader.
- [iq-9075-evk.conf](iq-9075-evk.conf) — Qualcomm IQ-9075 Evaluation Kit, based on QCS9075.
- [iq-x5121-evk.conf](iq-x5121-evk.conf) — Qualcomm Purwa IoT Evaluation Kit, based on IQ-X5121.
- [iq-x7181-evk.conf](iq-x7181-evk.conf) — Qualcomm Hamoa IoT Evaluation Kit, based on IQ-X7181, including its UEFI capsule settings.
- [kaanapali-mtp.conf](kaanapali-mtp.conf) — Qualcomm Kaanapali development kit.
- [qcm6490-idp.conf](qcm6490-idp.conf) — Qualcomm QCM6490 Integrated Development Platform.
- [qcom-armv7a.conf](qcom-armv7a.conf) — Unified 32-bit machine for Snapdragon ARMv7-A (Krait) SoCs that builds Android boot images for several older boards.
- [qcom-armv8a.conf](qcom-armv8a.conf) — Generic 64-bit machine that builds one kernel with the devicetrees of many Qualcomm boards, plus Android boot images and DTB images for them.
- [qcs615-ride.conf](qcs615-ride.conf) — Qualcomm QCS615 ADP Air Beta Evaluation Kit.
- [qcs6490-rb3gen2-core-kit.conf](qcs6490-rb3gen2-core-kit.conf) — Deprecated name that only requires `rb3gen2-core-kit.conf`.
- [qcs8300-ride-sx.conf](qcs8300-ride-sx.conf) — Qualcomm QCS8300 Ride SX Beta Evaluation Kit.
- [qcs9100-ride-sx.conf](qcs9100-ride-sx.conf) — Qualcomm QCS9100 Ride SX Beta Evaluation Kit.
- [qrb2210-rb1-core-kit.conf](qrb2210-rb1-core-kit.conf) — Deprecated name that only requires `rb1-core-kit.conf`.
- [rb1-core-kit.conf](rb1-core-kit.conf) — Qualcomm RB1 Development Kit with QRB2210 (QCM2290), using U-Boot and `qbootctl` to mark boots as successful.
- [rb3gen2-core-kit-open-fw.conf](rb3gen2-core-kit-open-fw.conf) — RB3Gen2 Development Kit with open boot firmware: adds TF-A and OP-TEE and uses `u-boot-qcom` as the bootloader.
- [rb3gen2-core-kit.conf](rb3gen2-core-kit.conf) — Qualcomm RB3Gen2 Development Kit (Core Kit) with QCS6490.
- [sdx75-idp.conf](sdx75-idp.conf) — Qualcomm SDX75 IDP board, with UBI filesystem parameters for its NAND flash.
- [shikra-evk.conf](shikra-evk.conf) — Qualcomm Shikra Alpha Evaluation Kit.
- [sm8750-mtp.conf](sm8750-mtp.conf) — Qualcomm SM8750 development kit.
