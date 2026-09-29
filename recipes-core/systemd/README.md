# systemd

Qualcomm changes to the [OpenEmbedded-Core](https://git.openembedded.org/openembedded-core) `systemd` recipe. The bbappend adds its local files to the search path, so BitBake finds them by name in the `systemd/` subfolder.

## Folders

- [systemd/](systemd/) — Holds `99-dma-heap.rules`, the udev rule that the bbappend installs.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [systemd_%.bbappend](systemd_%25.bbappend) — For Qualcomm machines, creates a `dmaheap` system group and installs `99-dma-heap.rules` in the udev rules package, which gives that group read and write access to `/dev/dma_heap/system`.
