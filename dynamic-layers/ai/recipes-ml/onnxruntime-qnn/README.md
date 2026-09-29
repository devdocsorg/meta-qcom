# onnxruntime-qnn

Builds the ONNX Runtime QNN execution provider, a plugin that lets ONNX Runtime run models on Qualcomm hardware through the Qualcomm AI Runtime SDK (QAIRT).

## Folders

- [files/](files/) — Patches the recipe applies: one renames the installed pkg-config file to `libonnxruntime_providers_qnn.pc`, and one fixes the ONNX Runtime header include path and multiarch library path.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [onnxruntime-qnn_2.4.0.bb](onnxruntime-qnn_2.4.0.bb) — Builds version 2.4.0 of the plugin library `libonnxruntime_providers_qnn.so` with CMake against onnxruntime and qairt-sdk, for aarch64 machines only.
