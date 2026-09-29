# userspace-resource-manager

Recipe for the Userspace Resource Manager (URM) daemon.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [userspace-resource-manager_0.4.9.bb](userspace-resource-manager_0.4.9.bb) — Builds the URM daemon, which monitors system resources and applies policies through cgroups and sysfs, with its `urm.service` unit; by default it also builds the classifier and tests, and the state detector when systemd is enabled.
