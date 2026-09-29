# optee

Builds OP-TEE OS from the [Qualcomm optee_os](https://github.com/qualcomm-linux/optee_os) fork for Qualcomm SoCs, reusing `optee-os.inc` from [meta-arm](https://git.yoctoproject.org/meta-arm), and points optee-test at the Qualcomm TA devkit.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [optee-os-qcom-kodiak_git.bb](optee-os-qcom-kodiak_git.bb) — Builds OP-TEE OS for the `qcom-kodiak` platform and deploys it to the `optee-kodiak` folder; trusted-firmware-a-qcom-rb3gen2 uses it.
- [optee-os-qcom-lemans_git.bb](optee-os-qcom-lemans_git.bb) — Builds OP-TEE OS for the `qcom-lemans` platform and deploys it to the `optee-lemans` folder; trusted-firmware-a-qcom-lemans-evk uses it.
- [optee-os-qcom.inc](optee-os-qcom.inc) — Shared by the three optee-os recipes here: fetches OP-TEE OS 4.10.0-qcom and replaces the meta-arm `do_deploy` so each recipe can pick its deploy folder through `OPTEE_DEPLOY`.
- [optee-os-tadevkit-qcom_git.bb](optee-os-tadevkit-qcom_git.bb) — Builds the OP-TEE TA devkit, used to build trusted applications, from the Qualcomm OP-TEE OS source and installs it under `/usr/include/optee/export-user_ta`.
- [optee-qcom.inc](optee-qcom.inc) — Shared by optee-os-tadevkit-qcom and the optee-test append: limits the recipe to qcm6490 and qcs9100 machines and sets `OPTEEMACHINE` to `qcom-kodiak` or `qcom-lemans`.
- [optee-test_%.bbappend](optee-test_%25.bbappend) — On Qualcomm machines, builds optee-test against optee-os-tadevkit-qcom instead of optee-os-tadevkit and applies `optee-qcom.inc`.
