# Persist partition files

Files that mount-tee-partition_1.0.bb installs to prepare and mount the persist partition.

## Files

- [README.md](README.md) — Indexes this folder.
- [check-tee-partition-fs.sh](check-tee-partition-fs.sh) — Creates or recreates an ext4 filesystem on the persist partition when it is missing or corrupted.
- [format-tee-partition.service](format-tee-partition.service) — Runs the filesystem check before `/var/lib/tee` is mounted.
- [persist.rules](persist.rules) — Starts the `/var/lib/tee` mount when the persist partition appears.
- [var-lib-tee.mount](var-lib-tee.mount) — Mounts the persist partition at `/var/lib/tee`.
