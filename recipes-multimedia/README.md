# recipes-multimedia

Camera, computer vision, and GStreamer recipes for Qualcomm machines. BitBake loads every `.bb` and `.bbappend` one folder down through the `recipes-*/*/` pattern in `conf/layer.conf`.

## Folders

- [camx/](camx/README.md) — The CamX camera kernel driver and the CamX common headers.
- [fastcv/](fastcv/README.md) — The prebuilt Qualcomm FastCV computer vision library.
- [gstreamer/](gstreamer/README.md) — Qualcomm patches for the GStreamer base, good, and bad plugins.
- [imsdk/](imsdk/README.md) — The Qualcomm IMSDK GStreamer plugins and the smart video encoder control library.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
