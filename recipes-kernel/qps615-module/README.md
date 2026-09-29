# qps615-module

Recipes for the QPS615 PCIe Ethernet bridge, which several machines add through `MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS`.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [qps615-dlkm_git.bb](qps615-dlkm_git.bb) — Builds the Qualcomm fork of the TC956x host driver as a kernel module for the QPS615 bridge and pulls in its firmware.
- [qps615-firmware_6.0.0.bb](qps615-firmware_6.0.0.bb) — Installs the QPS615 PCIe bridge firmware `TC956X_Firmware_PCIeBridge.bin` into the firmware directory.
