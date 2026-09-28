# OP-TEE

Builds the Qualcomm OP-TEE trusted OS and its trusted application devkit.

## Files

- [README.md](README.md) — Indexes this folder.
- [optee-os-qcom-kodiak_git.bb](optee-os-qcom-kodiak_git.bb) — Builds OP-TEE OS for the Kodiak platform.
- [optee-os-qcom-lemans_git.bb](optee-os-qcom-lemans_git.bb) — Builds OP-TEE OS for the Lemans platform.
- [optee-os-qcom.inc](optee-os-qcom.inc) — Shares the Qualcomm OP-TEE source and deploy step.
- [optee-os-tadevkit-qcom_git.bb](optee-os-tadevkit-qcom_git.bb) — Builds the OP-TEE trusted application devkit.
- [optee-qcom.inc](optee-qcom.inc) — Maps QCM6490 and QCS9100 machines to their OP-TEE platform.
- [optee-test_%.bbappend](optee-test_%25.bbappend) — Builds optee-test against the Qualcomm devkit and platform settings.
