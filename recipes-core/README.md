# recipes-core

Qualcomm changes to core system recipes from [OpenEmbedded-Core](https://git.openembedded.org/openembedded-core). BitBake applies the `.bbappend` files in these subfolders through the layer's `recipes-*/*/*.bbappend` pattern.

## Folders

- [systemd/](systemd/README.md) — Adds a `dmaheap` group and a udev rule for `/dev/dma_heap/system` to systemd on Qualcomm machines.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
