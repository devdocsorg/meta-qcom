# dynamic-layers/meta-arm/recipes-security/optee

Recipes for the Qualcomm fork of OP-TEE.

## Files

- [optee-os-qcom-kodiak_git.bb](optee-os-qcom-kodiak_git.bb) — Builds OP-TEE OS for Kodiak.
- [optee-os-qcom-lemans_git.bb](optee-os-qcom-lemans_git.bb) — Builds OP-TEE OS for Lemans.
- [optee-os-qcom.inc](optee-os-qcom.inc) — Shares the OP-TEE OS fetch and deployment.
- [optee-os-tadevkit-qcom_git.bb](optee-os-tadevkit-qcom_git.bb) — Builds the trusted application development kit.
- [optee-qcom.inc](optee-qcom.inc) — Selects the OP-TEE platform for each SoC.
- [optee-test_%.bbappend](optee-test_%.bbappend) — Builds the OP-TEE tests against the Qualcomm development kit.
- [README.md](README.md) — Introduces this folder and indexes its contents.
