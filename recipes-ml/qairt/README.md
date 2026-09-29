# qairt

Recipe for the prebuilt Qualcomm AI Runtime (QAIRT) SDK. Machines pull in the Hexagon DSP package that matches their SoC, such as `qairt-sdk-hexagon-v68`.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [qairt-sdk_2.50.0.260828.bb](qairt-sdk_2.50.0.260828.bb) — Installs the prebuilt Qualcomm AI Runtime SDK headers, libraries, and tools for running ML models on the CPU, GPU, and NPU, with the Hexagon DSP libraries split into one package per Hexagon version.
