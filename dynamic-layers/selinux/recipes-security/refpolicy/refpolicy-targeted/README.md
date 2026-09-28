# Policy patches

Patches that the refpolicy-targeted append applies.

## Files

- [README.md](README.md) — Indexes this folder.
- [0001-Add-SELinux-policy-for-camera-nhx.patch](0001-Add-SELinux-policy-for-camera-nhx.patch) — Adds a policy for camera-nhx.
- [0002-Enable-the-tunable-flag-tee_supplicant_qtee.patch](0002-Enable-the-tunable-flag-tee_supplicant_qtee.patch) — Enables the `tee_supplicant_qtee` tunable, on machines without the `optee` feature.
- [0003-seatd-allow-self-fifo_file-read-write-for-signal-han.patch](0003-seatd-allow-self-fifo_file-read-write-for-signal-han.patch) — Lets seatd read and write its own FIFOs for signal handling.
- [0004-kernel-allow-module-loaders-to-use-net_admin.patch](0004-kernel-allow-module-loaders-to-use-net_admin.patch) — Lets module loaders use `net_admin`.
