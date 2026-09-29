# camera-service

Builds the Qualcomm Linux embedded camera service, with client and server modules.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [camera-service_1.0.6.bb](camera-service_1.0.6.bb) — Builds [camera-service](https://github.com/qualcomm/camera-service) 1.0.6 with CMake for aarch64, enables `qti-cam-server.service`, and splits the common, client, generic server, and kodiak server libraries into separate packages.
