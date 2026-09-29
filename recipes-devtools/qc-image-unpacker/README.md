# qc-image-unpacker

Holds the recipe for [qc_image_unpacker](https://github.com/anestisb/qc_image_unpacker), a tool that unpacks Android Qualcomm images. BitBake finds the recipe's patches by name in the `qc-image-unpacker/` subfolder.

## Folders

- [qc-image-unpacker/](qc-image-unpacker/) — Two patches: one fixes a `strrchr()` const build error with glibc 2.43 and later, the other makes the tool fail when an image cannot be opened.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [qc-image-unpacker_git.bb](qc-image-unpacker_git.bb) — Builds [qc_image_unpacker](https://github.com/anestisb/qc_image_unpacker) with the two local patches and installs the `qc_image_unpacker` binary for the target, the build host, and the SDK.
