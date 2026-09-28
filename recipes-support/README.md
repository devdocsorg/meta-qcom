# Support services and libraries

Recipes for the daemons, libraries, and boot helpers that Qualcomm SoCs need at runtime, such as QRTR, FastRPC, and remote file systems.

## Folders

- [abl2esp/](abl2esp/README.md) — Deploys the ABL replacement that boots an EFI loader from the ESP.
- [fastrpc/](fastrpc/README.md) — Builds the FastRPC library, daemons, and tests.
- [hexagonrpc/](hexagonrpc/README.md) — Builds the alternative FastRPC implementation for sensors.
- [initrdscripts/](initrdscripts/README.md) — Adds an initramfs module that copies kernel modules to the root file system.
- [libdmabufheap/](libdmabufheap/README.md) — Builds the Qualcomm DMA-BUF heap library.
- [libvmmem/](libvmmem/README.md) — Builds the Qualcomm libvmmem library.
- [pd-mapper/](pd-mapper/README.md) — Builds the protection domain mapper service.
- [qbootctl/](qbootctl/README.md) — Builds the A/B boot slot control tool and its bless-boot service.
- [qmi-framework/](qmi-framework/README.md) — Builds the QMI framework.
- [qrtr/](qrtr/README.md) — Builds the QRTR library and tools.
- [rmtfs/](rmtfs/README.md) — Builds the remote file system service for the modem.
- [rpmsg-export/](rpmsg-export/README.md) — Builds the tool that exports RPMSG channels as devices.
- [rust-android-sparse/](rust-android-sparse/README.md) — Builds the Android sparse image tools.
- [time-services/](time-services/README.md) — Builds the daemon that syncs time from the modem.
- [tqftpserv/](tqftpserv/README.md) — Builds the TFTP server over QRTR.
- [userspace-resource-manager/](userspace-resource-manager/README.md) — Builds the user-space resource management daemon.

## Files

- [README.md](README.md) — Indexes this folder.
