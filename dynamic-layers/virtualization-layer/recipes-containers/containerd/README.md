# containerd

Changes the containerd recipe from [meta-virtualization](https://git.yoctoproject.org/meta-virtualization) for Qualcomm machines.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [containerd_git.bbappend](containerd_git.bbappend) — On Qualcomm machines, makes the whole source tree writable and searchable by its owner after `do_compile`.
