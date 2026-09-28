# systemd changes

A bbappend that adds Qualcomm udev rules to systemd.

## Folders

- [systemd/](systemd/README.md) — Holds the udev rule that the bbappend installs.

## Files

- [README.md](README.md) — Indexes this folder.
- [systemd_%.bbappend](systemd_%25.bbappend) — Installs the DMA heap rule and creates the `dmaheap` group on Qualcomm machines.
