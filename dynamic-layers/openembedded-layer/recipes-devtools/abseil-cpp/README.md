# abseil-cpp

Keeps an older copy of the abseil-cpp recipe from [meta-openembedded](https://github.com/openembedded/meta-openembedded) so that prebuilt binary recipes built against it keep working; `conf/machine/include/qcom-common-binary.inc` sets `PREFERRED_VERSION` to this version.

## Folders

- [abseil-cpp/](abseil-cpp/) — Patches the recipe applies: one makes Abseil always include `<asm/sgidefs.h>`, and one carries PowerPC fixes.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [abseil-cpp_20260107.1.bb](abseil-cpp_20260107.1.bb) — Builds Abseil 20260107.1 as shared libraries, split into one `libabsl-*` package per library, for target, native, and nativesdk.
