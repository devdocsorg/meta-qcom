# gpsd

Adds Qualcomm PDS service support to the gpsd recipe from [meta-openembedded](https://github.com/openembedded/meta-openembedded).

## Folders

- [gpsd/](gpsd/) — The patch that introduces Qualcomm PDS service support in gpsd.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [gpsd_%.bbappend](gpsd_%25.bbappend) — Adds `gpsd-<version>/` and `gpsd/` to the file search path and applies the Qualcomm PDS service patch on Qualcomm machines.
