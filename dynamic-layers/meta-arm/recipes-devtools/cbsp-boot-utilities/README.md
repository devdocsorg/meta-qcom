# cbsp-boot-utilities

Builds the host-side capsule generation tool that `qcom-capsule.bbclass` runs to create UEFI firmware update capsules.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [cbsp-boot-utilities-native_1.0.bb](cbsp-boot-utilities-native_1.0.bb) — Installs `qcom-capsule-tool` from the `uefi_capsule_generation` folder of [cbsp-boot-utilities](https://github.com/quic/cbsp-boot-utilities) as a native Python package, along with the default `FvUpdate.xml` that the capsule class falls back to.
