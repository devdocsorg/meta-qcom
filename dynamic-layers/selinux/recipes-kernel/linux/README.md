# linux

Adds SELinux support to the Qualcomm kernel recipes by requiring `linux-yocto_selinux.inc` from [meta-selinux](https://git.yoctoproject.org/meta-selinux), which adds the `selinux.cfg` kernel configuration fragment when the selinux distro feature is enabled.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [linux-qcom-next_git.bbappend](linux-qcom-next_git.bbappend) — Applies the SELinux kernel include to linux-qcom-next.
- [linux-qcom_%.bbappend](linux-qcom_%25.bbappend) — Applies the SELinux kernel include to every linux-qcom version.
