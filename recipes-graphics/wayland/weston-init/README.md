# Weston start-up files

Files the weston-init append installs to start Weston with every KMS-capable DRM card.

## Files

- [additional-devices.conf](additional-devices.conf) — Replaces the weston.service ExecStart with weston-start.sh.
- [README.md](README.md) — Indexes this folder.
- [weston-start.sh](weston-start.sh) — Starts Weston with the first KMS card and passes the others as additional devices.
