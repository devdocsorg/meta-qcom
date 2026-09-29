# recipes-bsp/partition

Recipes for partition tables, the [qcom-ptool](https://github.com/qualcomm-linux/qcom-ptool) partition tool, and the persist partition.

## Folders

- [mount-tee-partition/](mount-tee-partition/README.md) — Holds the persist partition's mount unit, check script, service, and udev rule.

## Files

- [mount-tee-partition_1.0.bb](mount-tee-partition_1.0.bb) — Mounts the persist partition at /var/lib/tee, creating its file system when needed.
- [qcom-partition-conf_git.bb](qcom-partition-conf_git.bb) — Deploys each platform's partition tables and flashing XML files.
- [qcom-ptool-native.bb](qcom-ptool-native.bb) — Builds the [qcom-ptool](https://github.com/qualcomm-linux/qcom-ptool) partition tool for the build host.
- [qcom-ptool.inc](qcom-ptool.inc) — Pins the [qcom-ptool](https://github.com/qualcomm-linux/qcom-ptool) source.
- [qcom-raw-partitions-udev-rules_git.bb](qcom-raw-partitions-udev-rules_git.bb) — Installs udev rules that skip file system probing on raw partitions.
- [README.md](README.md) — Introduces this folder and indexes its contents.
