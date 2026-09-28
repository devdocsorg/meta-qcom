# Trusted Firmware-A

Builds Qualcomm Trusted Firmware-A with OP-TEE and packs a signed FIP ELF image.

## Files

- [README.md](README.md) — Indexes this folder.
- [trusted-firmware-a-qcom-lemans-evk_git.bb](trusted-firmware-a-qcom-lemans-evk_git.bb) — Builds TF-A for the Lemans EVK platform.
- [trusted-firmware-a-qcom-rb3gen2_git.bb](trusted-firmware-a-qcom-rb3gen2_git.bb) — Builds TF-A for RB3 Gen 2 with the SC7280 qtiseclib blob.
- [trusted-firmware-a-qcom.inc](trusted-firmware-a-qcom.inc) — Shares the Qualcomm TF-A source, build targets, and FIP signing.
