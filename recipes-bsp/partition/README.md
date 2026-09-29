# partition

Recipes for Qualcomm partition layouts and partition setup on the running system. Three of them build [qcom-ptool](https://github.com/qualcomm-linux/qcom-ptool) through the shared `qcom-ptool.inc`, and one mounts the `persist` partition for the TEE.

## Folders

- [mount-tee-partition/](mount-tee-partition/) — The systemd mount and service units, udev rule, and filesystem check script that `mount-tee-partition_1.0.bb` installs.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [mount-tee-partition_1.0.bb](mount-tee-partition_1.0.bb) — Installs a systemd unit that mounts the `persist` partition at `/var/lib/tee`, a service that first creates or recreates its ext4 filesystem when it is missing or corrupted, and a udev rule that starts the mount when the partition appears.
- [qcom-partition-conf_git.bb](qcom-partition-conf_git.bb) — Deploys the per-platform GPT partition binaries and QDL flashing XML files (`rawprogram*.xml`, `patch*.xml`, and `contents.xml` when present) from qcom-ptool into `partitions/<platform>` in the deploy directory.
- [qcom-ptool-native.bb](qcom-ptool-native.bb) — Builds the qcom-ptool Python command-line tool for the build host, which the other partition recipes run to generate their output.
- [qcom-ptool.inc](qcom-ptool.inc) — Shared by the three qcom-ptool recipes; sets the homepage, license, and pinned Git source of qcom-ptool.
- [qcom-raw-partitions-udev-rules_git.bb](qcom-raw-partitions-udev-rules_git.bb) — Runs `qcom-ptool gen_udev_rules` to generate and install `55-qcom-raw-partitions-noblkid.rules`, which stops udev from probing known Qualcomm raw GPT partitions for filesystems.
