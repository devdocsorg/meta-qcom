# libssc

Builds libssc, a library that exposes the sensors managed by the Qualcomm Sensor Core.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [libssc_git.bb](libssc_git.bb) — Builds libssc 0.2.2+ with Meson and GObject introspection against libqmi, and removes its Python mocking server from the install.
