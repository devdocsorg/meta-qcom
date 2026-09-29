# qca-swiss-army-knife

Holds the recipe for [qca-swiss-army-knife](https://github.com/qca/qca-swiss-army-knife), the Qualcomm Atheros (QCA) driver development utilities. BitBake finds the recipe's patch and helper scripts by name in the `qca-swiss-army-knife/` subfolder.

## Folders

- [qca-swiss-army-knife/](qca-swiss-army-knife/) — A patch that switches the upstream scripts to `/usr/bin/env python3`, and four scripts that write the `board-2.json` description of ath10k (SNOC and PCI) and ath11k (AHB and PCI) board data files.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [qca-swiss-army-knife_git.bb](qca-swiss-army-knife_git.bb) — Installs the scripts from [qca-swiss-army-knife](https://github.com/qca/qca-swiss-army-knife) and the four local `board-2.json` generator scripts into `bindir`, for the target, the build host, and the SDK.
