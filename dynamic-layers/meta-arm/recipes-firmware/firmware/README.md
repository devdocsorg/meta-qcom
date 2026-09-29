# firmware

Produces the UEFI firmware management protocol (FMP) capsule used to update boot firmware on Qualcomm boards.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [firmware-qcom-capsule_1.0.bb](firmware-qcom-capsule_1.0.bb) — Builds the capsule through `qcom-capsule.bbclass` for hamoa, qcm6490, qcs615, qcs8300, and qcs9100 machines, and provides `virtual/qcom-capsule-firmware`.
