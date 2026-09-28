# Device firmware

Recipes that install prebuilt firmware files under the firmware directory, split into per-subsystem packages where the shared include asks for it.

## Files

- [README.md](README.md) — Indexes this folder.
- [camxfirmware-hamoa_1.0.6.bb](camxfirmware-hamoa_1.0.6.bb) — Installs the Hamoa camera firmware and links it for Purwa.
- [camxfirmware-kodiak_1.0.7.bb](camxfirmware-kodiak_1.0.7.bb) — Installs the Kodiak (QCM6490) camera firmware.
- [camxfirmware-lemans_1.0.7.bb](camxfirmware-lemans_1.0.7.bb) — Installs the Lemans camera firmware and links it for Monaco.
- [camxfirmware-talos_1.0.1.bb](camxfirmware-talos_1.0.1.bb) — Installs the Talos (QCS615) camera firmware.
- [firmware-ath6kl_git.bb](firmware-ath6kl_git.bb) — Installs extra Atheros AR6004 firmware files that linux-firmware does not carry.
- [firmware-qcom-qcm6490-idp.bb](firmware-qcom-qcm6490-idp.bb) — Placeholder for the QCM6490 IDP modem firmware, which another layer provides.
- [firmware-qcom-rb3gen2.bb](firmware-qcom-rb3gen2.bb) — Placeholder for the RB3 Gen 2 modem firmware, which another layer provides.
- [firmware-qcom.inc](firmware-qcom.inc) — Shared firmware paths, split packages, QA settings, and optional compression.
