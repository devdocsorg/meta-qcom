# recipes-bsp/partition/mount-tee-partition

Files that mount-tee-partition installs.

## Files

- [check-tee-partition-fs.sh](check-tee-partition-fs.sh) — Creates an ext4 file system on the persist partition when it has none or is corrupted.
- [format-tee-partition.service](format-tee-partition.service) — Runs the check script before the partition is mounted.
- [persist.rules](persist.rules) — Starts the mount when the persist partition appears.
- [README.md](README.md) — Introduces this folder and indexes its contents.
- [var-lib-tee.mount](var-lib-tee.mount) — Mounts the persist partition at /var/lib/tee.
