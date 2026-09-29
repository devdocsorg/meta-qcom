# mesa

Qualcomm changes to the [OpenEmbedded-Core](https://git.openembedded.org/openembedded-core) `mesa` recipe. The bbappend adds its local files to the search path, so BitBake finds the patches by name in the `mesa/` subfolder.

## Folders

- [mesa/](mesa/) — Patches backported from [Mesa](https://gitlab.freedesktop.org/mesa/mesa) that add A830v1 and A722 GPU support to freedreno and fix freedreno and rusticl OpenCL behaviour.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [mesa.bbappend](mesa.bbappend) — For Qualcomm machines, applies the five patches in `mesa/` and enables the `freedreno` and `tools` `PACKAGECONFIG` options.
