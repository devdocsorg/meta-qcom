# SELinux kernel configuration

Adds the [meta-selinux](https://git.yoctoproject.org/meta-selinux) kernel configuration to the Qualcomm kernel recipes.

## Files

- [README.md](README.md) — Indexes this folder.
- [linux-qcom-next_git.bbappend](linux-qcom-next_git.bbappend) — Requires `linux-yocto_selinux.inc` for linux-qcom-next.
- [linux-qcom_%.bbappend](linux-qcom_%25.bbappend) — Requires `linux-yocto_selinux.inc` for linux-qcom.
