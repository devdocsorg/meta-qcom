# imsdk

Appends to the IMSDK GStreamer plugin recipes of this layer that turn on features needing onnx and onnxruntime from [meta-ai](https://github.com/qualcomm-linux/meta-ai).

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [gst-plugins-imsdk-oss_%.bbappend](gst-plugins-imsdk-oss_%25.bbappend) — On Qualcomm machines, adds the `onnx` PACKAGECONFIG option, which builds the ONNX inference plugin and depends on onnx and onnxruntime.
