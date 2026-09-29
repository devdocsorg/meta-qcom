# hexagonrpc

Recipe for hexagonrpc, an alternative FastRPC implementation for sensor use cases.

## Folders

- [hexagonrpc/](hexagonrpc/) — Two build fix patches, one for a sign-compare error in the listener and one for the `fastrpc_apps_mem_init()` argument.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [hexagonrpc_git.bb](hexagonrpc_git.bb) — Builds the FastRPC ioctl wrapper and reverse tunnel that talk to the sensor manager on the DSP and serve files to the remote processors.
