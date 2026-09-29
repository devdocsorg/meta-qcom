# fastrpc

Recipe for the Qualcomm FastRPC library and daemons, which let applications on the CPU call code on the Hexagon DSPs; limited to ARMv8 machines.

## Folders

- [fastrpc/](fastrpc/) — The `run-ptest` script that runs `fastrpc_test` for the package tests.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [fastrpc_1.0.7.bb](fastrpc_1.0.7.bb) — Builds the FastRPC libraries, the per-DSP RPC daemons with their systemd services, the udev rules, and a `fastrpc-tests` package with ptest support.
