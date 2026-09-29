# openembedded-layer

Recipes and appends that BitBake parses only when the `openembedded-layer` collection, the meta-oe layer in [meta-openembedded](https://github.com/openembedded/meta-openembedded), is in the build.

## Folders

- [recipes-connectivity/](recipes-connectivity/README.md) — Appends that add Qualcomm modem support to libqmi and ModemManager.
- [recipes-devtools/](recipes-devtools/README.md) — Abseil, adbd start-up configuration, and the Mink IDL compiler.
- [recipes-multimedia/](recipes-multimedia/README.md) — The camera service, prebuilt CamX camera libraries, and IMSDK GStreamer additions.
- [recipes-navigation/](recipes-navigation/README.md) — The gpsd append and the Qualcomm location HAL.
- [recipes-security/](recipes-security/README.md) — MinkIPC and the QCOM-TEE library for talking to the Qualcomm Trusted Execution Environment.
- [recipes-support/](recipes-support/README.md) — Sensor libraries, prebuilt sensor services, and the OpenCV append.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
