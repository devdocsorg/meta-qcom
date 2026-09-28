# Machine configurations

One file per supported board or generic target; set `MACHINE` to the file
name without `.conf`. The [configuration reference](../../docs/source/user/CONFIGURATION.md#machine-settings)
explains the settings they use.

## Folders

- [include/](include/README.md) — Holds the SoC and shared machine settings that these files require.

## Files

- [README.md](README.md) — Indexes this folder.
- [glymur-crd.conf](glymur-crd.conf) — Configures the Qualcomm Glymur Compute Reference Device.
- [iq-615-evk.conf](iq-615-evk.conf) — Configures the Qualcomm IQ-615 Evaluation Kit (EVK) based on QCS615.
- [iq-8275-evk.conf](iq-8275-evk.conf) — Configures the Qualcomm IQ-8275 Evaluation Kit (EVK) based on QCS8275.
- [iq-9075-evk-open-fw-spl.conf](iq-9075-evk-open-fw-spl.conf) — Configures the Qualcomm IQ-9075 Evaluation Kit (EVK) with open boot firmware and U-Boot SPL.
- [iq-9075-evk-open-fw.conf](iq-9075-evk-open-fw.conf) — Configures the Qualcomm IQ-9075 Evaluation Kit (EVK) with open boot firmware support.
- [iq-9075-evk.conf](iq-9075-evk.conf) — Configures the Qualcomm IQ-9075 Evaluation Kit (EVK) based on QCS9075.
- [iq-x5121-evk.conf](iq-x5121-evk.conf) — Configures the Qualcomm Purwa IoT Evaluation Kit (EVK) based on IQ-X5121.
- [iq-x7181-evk.conf](iq-x7181-evk.conf) — Configures the Qualcomm Hamoa IoT Evaluation Kit (EVK) based on IQ-X7181.
- [kaanapali-mtp.conf](kaanapali-mtp.conf) — Configures the Qualcomm Kaanapali Development Kit.
- [qcm6490-idp.conf](qcm6490-idp.conf) — Configures the Qualcomm QCM6490 Integrated Development Platform.
- [qcom-armv7a.conf](qcom-armv7a.conf) — Configures the Qualcomm Snapdragon ARMv7-a (with Krait cores).
- [qcom-armv8a.conf](qcom-armv8a.conf) — Generic ARMv8-A machine covering many Qualcomm boards with one image.
- [qcs615-ride.conf](qcs615-ride.conf) — Configures the Qualcomm QCS615 ADP Air Beta Evaluation Kit (EVK).
- [qcs6490-rb3gen2-core-kit.conf](qcs6490-rb3gen2-core-kit.conf) — Deprecated name that requires `rb3gen2-core-kit.conf`.
- [qcs8300-ride-sx.conf](qcs8300-ride-sx.conf) — Configures the Qualcomm QCS8300 Ride SX Beta Evaluation Kit (EVK).
- [qcs9100-ride-sx.conf](qcs9100-ride-sx.conf) — Configures the Qualcomm QCS9100 Ride SX Beta Evaluation Kit (EVK).
- [qrb2210-rb1-core-kit.conf](qrb2210-rb1-core-kit.conf) — Deprecated name that requires `rb1-core-kit.conf`.
- [rb1-core-kit.conf](rb1-core-kit.conf) — Configures the Qualcomm RB1 Development Kit (Core Kit).
- [rb3gen2-core-kit-open-fw.conf](rb3gen2-core-kit-open-fw.conf) — Configures the Qualcomm RB3Gen2 Development Kit (Core Kit with open boot firmware).
- [rb3gen2-core-kit.conf](rb3gen2-core-kit.conf) — Configures the Qualcomm RB3Gen2 Development Kit (Core Kit).
- [sdx75-idp.conf](sdx75-idp.conf) — Configures the Qualcomm SDX75 IDP.
- [shikra-evk.conf](shikra-evk.conf) — Configures the Qualcomm Shikra Alpha Evaluation Kit (EVK).
- [sm8750-mtp.conf](sm8750-mtp.conf) — Configures the Qualcomm SM8750 Development Kit.
