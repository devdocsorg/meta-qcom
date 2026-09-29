# rmtfs

Recipe for the RMTFS QMI service, which serves the modem's remote filesystem partitions from the host storage.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [rmtfs_1.3.bb](rmtfs_1.3.bb) — Builds the `rmtfs` service with its systemd unit, plus a separate `rmtfs-dir` package with the `rmtfs-dir.service` unit.
