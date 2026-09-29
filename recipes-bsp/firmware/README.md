# firmware

Recipes that install Qualcomm device firmware under `/lib/firmware` and split it into packages that board packagegroups can recommend. All recipes here except `firmware-ath6kl_git.bb` require the shared `firmware-qcom.inc`.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [camxfirmware-hamoa_1.0.6.bb](camxfirmware-hamoa_1.0.6.bb) — Installs the prebuilt Hamoa camera firmware (`CAMERA_ICP.mbn`) under `qcom/x1e80100` and adds a `camxfirmware-purwa` package that links the same file under `qcom/x1p42100` for Purwa.
- [camxfirmware-kodiak_1.0.7.bb](camxfirmware-kodiak_1.0.7.bb) — Installs the prebuilt Kodiak camera firmware (`CAMERA_ICP_170.elf`) under `qcom/qcm6490`.
- [camxfirmware-lemans_1.0.7.bb](camxfirmware-lemans_1.0.7.bb) — Installs the prebuilt Lemans camera firmware (`CAMERA_ICP.mbn`) under `qcom/sa8775p` and adds a `camxfirmware-monaco` package that links the same file under `qcom/qcs8300` for Monaco.
- [camxfirmware-talos_1.0.1.bb](camxfirmware-talos_1.0.1.bb) — Installs the prebuilt Talos camera firmware (`CAMERA_ICP.elf`) under `qcom/qcs615`.
- [firmware-ath6kl_git.bb](firmware-ath6kl_git.bb) — Installs the extra AR6004 hw1.3 and hw3.0 firmware files for the Qualcomm Atheros ath6kl driver from [ath6kl-firmware](https://github.com/qca/ath6kl-firmware), using an alternative for the `bdata.bin` file that [linux-firmware](https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git) also provides.
- [firmware-qcom-qcm6490-idp.bb](firmware-qcom-qcm6490-idp.bb) — Placeholder for the QCM6490 IDP board that declares an empty `linux-firmware-qcom-qcm6490-modem` package, because the modem firmware itself comes from a separate layer.
- [firmware-qcom-rb3gen2.bb](firmware-qcom-rb3gen2.bb) — Placeholder for the RB3 Gen2 board that declares an empty `linux-firmware-qcom-qcs6490-modem` package, because the modem firmware itself comes from a separate layer.
- [firmware-qcom.inc](firmware-qcom.inc) — Shared by the four `camxfirmware-*` recipes and the two board placeholder recipes; sets the `/lib/firmware/qcom/<name>` install path, the file patterns of the split `linux-firmware-qcom-<name>-*` packages, and optional `xz` or `zstd` compression through `FIRMWARE_COMPRESSION`.
