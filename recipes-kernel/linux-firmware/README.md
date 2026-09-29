# linux-firmware

Qualcomm changes to the linux-firmware recipe; BitBake applies the bbappend to every linux-firmware version.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [linux-firmware_%.bbappend](linux-firmware_%25.bbappend) — For Qualcomm machines, manages the ath6k AR6004 hw1.3 `bdata.bin` through update-alternatives so that `firmware-ath6kl` can provide an updated copy.
