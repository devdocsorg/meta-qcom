# qbootctl

Recipe for qbootctl, which `rb1-core-kit` installs so that the boot firmware does not fall back to the other A/B slot.

## Folders

- [files/](files/) — The `qbootctl-bless-boot.service.in` systemd unit template that the recipe installs.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [qbootctl_git.bb](qbootctl_git.bb) — Builds qbootctl, a port of the Qualcomm Android bootctrl HAL, with a systemd service that runs `qbootctl -m` to mark the current slot as good once boot completes.
