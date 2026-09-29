# recipes-support

Userspace daemons, libraries, and tools that Qualcomm SoCs need to talk to their remote processors and boot firmware, plus initramfs helpers. BitBake loads every `.bb` and `.bbappend` one folder down through the `recipes-*/*/` pattern in `conf/layer.conf`.

## Folders

- [abl2esp/](abl2esp/README.md) — A minimal Android Bootloader replacement that starts the EFI loader from the ESP.
- [fastrpc/](fastrpc/README.md) — The FastRPC library and daemons for offloading work to the Hexagon DSPs.
- [hexagonrpc/](hexagonrpc/README.md) — An alternative FastRPC implementation for sensor use cases.
- [initrdscripts/](initrdscripts/README.md) — An initramfs-framework module that copies kernel modules into the rootfs.
- [libdmabufheap/](libdmabufheap/README.md) — A library for the DMA-BUF heap framework.
- [libvmmem/](libvmmem/README.md) — A library for the membuf framework.
- [pd-mapper/](pd-mapper/README.md) — The protection domain mapper service.
- [qbootctl/](qbootctl/README.md) — A tool that marks the current A/B boot slot as good.
- [qmi-framework/](qmi-framework/README.md) — A QMI messaging library for IPC clients and servers.
- [qrtr/](qrtr/README.md) — The QRTR IPC router library and tools.
- [rmtfs/](rmtfs/README.md) — The remote filesystem service for the modem.
- [rpmsg-export/](rpmsg-export/README.md) — A tool that exports rpmsg endpoints as character devices.
- [rust-android-sparse/](rust-android-sparse/README.md) — A Rust implementation of the Android sparse image format.
- [time-services/](time-services/README.md) — A daemon that sets the system time from the modem.
- [tqftpserv/](tqftpserv/README.md) — A TFTP server over QRTR for the remote processors.
- [userspace-resource-manager/](userspace-resource-manager/README.md) — A daemon that manages system resources by policy.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
