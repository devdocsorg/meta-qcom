# refpolicy

Changes the targeted SELinux reference policy from [meta-selinux](https://git.yoctoproject.org/meta-selinux) for Qualcomm machines.

## Folders

- [refpolicy-targeted/](refpolicy-targeted/) — Policy patches that add a camera-nhx policy, enable the `tee_supplicant_qtee` tunable, let seatd read and write its own FIFO, and let kernel module loaders use `net_admin`.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [refpolicy-targeted_git.bbappend](refpolicy-targeted_git.bbappend) — On Qualcomm machines, applies the policy patches (the `tee_supplicant_qtee` patch only when the machine lacks the `optee` feature), writes `POLICY_BOOLEANS` name=value settings into `policy/booleans.conf` before compiling, and turns on `kernel_module_load_net_admin`.
