# Partition tables

Recipes that generate GPT partition files with
[qcom-ptool](https://github.com/qualcomm-linux/qcom-ptool) and handle the persist partition.

## Folders

- [mount-tee-partition/](mount-tee-partition/README.md) — Holds the unit, rule, and script that mount the persist partition at `/var/lib/tee`.

## Files

- [README.md](README.md) — Indexes this folder.
- [mount-tee-partition_1.0.bb](mount-tee-partition_1.0.bb) — Installs the units and rule that mount the persist partition at `/var/lib/tee`.
- [qcom-partition-conf_git.bb](qcom-partition-conf_git.bb) — Deploys the GPT binaries and flashing XML files for each Qualcomm platform.
- [qcom-ptool-native.bb](qcom-ptool-native.bb) — Builds the qcom-ptool command-line tool for use during the build.
- [qcom-ptool.inc](qcom-ptool.inc) — Shared source and licence settings for the qcom-ptool recipes.
- [qcom-raw-partitions-udev-rules_git.bb](qcom-raw-partitions-udev-rules_git.bb) — Installs udev rules that skip filesystem probing on raw Qualcomm partitions.
