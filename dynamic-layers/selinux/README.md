# selinux

Appends that BitBake parses only when the `selinux` layer collection from [meta-selinux](https://git.yoctoproject.org/meta-selinux) is in the build; they add SELinux support to the Qualcomm kernels and adjust the reference policy.

## Folders

- [recipes-kernel/](recipes-kernel/README.md) — Appends that add the SELinux kernel configuration to the Qualcomm kernel recipes.
- [recipes-security/](recipes-security/README.md) — The reference policy append and its patches.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
