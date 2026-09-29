# minkipc

Builds MinkIPC, a capability-based message passing framework for communicating with QTEE, together with the qteesupplicant service and the OP-TEE test suite adapted for QTEE.

## Folders

- [files/](files/) — Patches for the bundled OP-TEE test suite that remove the regression suite from the default list, stub PKCS#11 tests that do not apply to QTEE, fix a static initialization issue, and keep X.509 subject and issuer names const.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [minkipc_1.2.10.bb](minkipc_1.2.10.bb) — Builds [minkipc](https://github.com/qualcomm/minkipc) 1.2.10 with [optee_client](https://github.com/OP-TEE/optee_client) and [optee_test](https://github.com/OP-TEE/optee_test) 4.0.0, and packages the qteesupplicant and sfsconfig systemd services and the QTEE trusted applications separately.
