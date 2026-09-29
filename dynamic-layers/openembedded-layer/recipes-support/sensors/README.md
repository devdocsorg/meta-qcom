# sensors

Builds the Qualcomm Sensing Hub library and installs the prebuilt sensor services that use it.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [qcom-sensors-binaries_1.2.1.bb](qcom-sensors-binaries_1.2.1.bb) — Installs prebuilt sensor libraries, test applications, registry configuration, and the `sscrpcd` systemd service, for aarch64 machines only.
- [sensinghub_1.0.6.bb](sensinghub_1.0.6.bb) — Builds version 1.0.6 of the [sensinghub](https://github.com/qualcomm/sensinghub) userspace libraries for talking to the Qualcomm Sensing Hub.
