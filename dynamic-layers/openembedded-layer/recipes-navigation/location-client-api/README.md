# location-client-api

Builds the Qualcomm location hardware abstraction layer (HAL) libraries that location services and applications use.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [location-hal_1.0.2.bb](location-hal_1.0.2.bb) — Builds [location-hal-qcom](https://github.com/qualcomm-linux/location-hal-qcom) 1.0.2 with autotools, installs `/etc/gps.conf`, and creates the `locclient` group and `gps` system user that control access to the location daemon socket.
