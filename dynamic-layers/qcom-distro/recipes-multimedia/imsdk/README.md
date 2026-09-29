# imsdk

Appends to the IMSDK GStreamer plugin recipes of this layer that turn on features needing tensorflow-lite from [meta-qcom-distro](https://github.com/qualcomm-linux/meta-qcom-distro).

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [gst-plugins-imsdk-oss_%.bbappend](gst-plugins-imsdk-oss_%25.bbappend) — Enables the `tflite` PACKAGECONFIG option, which builds the TensorFlow Lite inference plugin, for every machine.
