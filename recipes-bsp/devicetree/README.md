# devicetree

Holds a placeholder device tree recipe for the generic `qcom-armv8` machine. The recipe inherits the `devicetree` class, which compiles the device tree sources listed in `SRC_URI`.

## Folders

- [files/](files/) — Holds `qcom-armv8-dummy.dts`, the empty device tree source that the recipe fetches by name.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [devicetree-dummy.bb](devicetree-dummy.bb) — Compiles the empty `qcom-armv8-dummy.dts` device tree and is compatible only with the `qcom-armv8` machine.
