# Configuration reference

This page lists the settings meta-qcom maintains: kas files, the layer
configuration, machine configurations, kernel and U-Boot fragments, files installed
on the target, environment variables, and CI workflows. Standard variables link to
the [Yocto Project variable glossary](https://docs.yoctoproject.org/ref-manual/variables.html);
the rows here explain this layer's values.

## How settings load

A kas file names the layers, `machine`, `distro`, and `target`, and writes its
`local_conf_header` entries into `conf/local.conf`
([kas project configuration](https://kas.readthedocs.io/en/latest/userguide/project-configuration.html)).
BitBake then reads each layer's `conf/layer.conf`, `conf/local.conf`, the machine file
`conf/machine/<machine>.conf` with its `require` chain, and the distro. Because
`local.conf` is read first, it overrides the weak defaults (`?=` and `??=`) in
machine files but not their plain assignments (`=`); `:append`, `:remove`, and
`:pn-<recipe>` overrides apply after all files are read
([BitBake syntax](https://docs.yoctoproject.org/bitbake/bitbake-user-manual/bitbake-user-manual-metadata.html)).
Machine files require an SoC include (`conf/machine/include/qcom-<soc>.inc`), which
requires `qcom-base.inc` (current platforms) and `qcom-common.inc`.

## kas files

Combine files with colons, machine first:
`kas-container build ci/<machine>.yml[:ci/<distro>.yml][:ci/<fragment>.yml]`.

| File | Purpose and local settings |
| --- | --- |
| [base.yml](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/ci/base.yml) | Common base: meta-qcom, [OE-Core](https://github.com/openembedded/openembedded-core) with three meta-qcom patches (igt-gpu-tools on non-x86, U-Boot SPL BSS padding, Shikra WLAN firmware), and [BitBake](https://github.com/openembedded/bitbake), all on `master`; `distro: nodistro`, `machine: unset`, target `core-image-base`. See the next table for its `local.conf` settings. |
| [base.lock.yml](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/ci/base.lock.yml) | Commit pins for the repositories the kas files name; kas applies them because the lock file sits beside `base.yml`. |
| `glymur-crd`, `iq-615-evk`, `iq-8275-evk`, `iq-9075-evk`, `iq-x5121-evk`, `iq-x7181-evk`, `kaanapali-mtp`, `qcm6490-idp`, `qcom-armv7a`, `qcs615-ride`, `qcs8300-ride-sx`, `qcs9100-ride-sx`, `rb1-core-kit`, `rb3gen2-core-kit`, `shikra-evk`, `sm8750-mtp` (`.yml`) | Include `base.yml` and set `machine` to the file's name. `qcs6490-rb3gen2-core-kit.yml` and `qrb2210-rb1-core-kit.yml` are symlinks to the `rb3gen2` and `rb1` files. |
| `iq-9075-evk-open-fw`, `iq-9075-evk-open-fw-spl`, `rb3gen2-core-kit-open-fw` (`.yml`) | Machine files that also include `meta-arm.yml` for the open TF-A and OP-TEE firmware. |
| [sdx75-idp.yml](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/ci/sdx75-idp.yml) | Machine file whose target is `core-image-minimal`. |
| [qcom-armv8a.yml](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/ci/qcom-armv8a.yml) | Generic Armv8 machine; `PREFERRED_PROVIDER_virtual/dtb = "devicetree-dummy"` and `QCOM_BOOTIMG_DEVICETREE = "qcom-armv8-dummy.dtb"` add a placeholder devicetree. |
| [qcom-distro.yml](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/ci/qcom-distro.yml) | Selects `distro: qcom-distro` from [meta-qcom-distro](https://github.com/qualcomm-linux/meta-qcom-distro) (`main`) and adds [meta-ai](https://github.com/qualcomm-linux/meta-ai) (`main`), [meta-openembedded](https://github.com/openembedded/meta-openembedded) (seven layers), [meta-virtualization](https://git.yoctoproject.org/meta-virtualization), [meta-audioreach](https://github.com/AudioReach/meta-audioreach), [meta-selinux](https://git.yoctoproject.org/meta-selinux) with three meta-qcom patches, [meta-updater](https://github.com/uptane/meta-updater), and [meta-security](https://git.yoctoproject.org/meta-security) with meta-tpm; `SKIP_META_VIRT_SANITY_CHECK = "1"`; targets the multimedia, proprietary multimedia, container orchestration, and networking images. |
| `qcom-distro-catchall`, `qcom-distro-selinux`, `qcom-distro-sota` (`.yml`) | Include `qcom-distro.yml` and select the distro of the same name; catchall and selinux narrow the targets. |
| `qcom-distro-kvm.yml`, `qcom-distro-multimedia-image.yml` | Include `qcom-distro.yml`; the first appends `kvm` to `MACHINE_FEATURES`, the second builds only `qcom-multimedia-image`. |
| `linux-qcom-next.yml`, `linux-qcom-next-rt.yml`, `linux-qcom-6.18.yml`, `linux-qcom-rt-6.18.yml`, `linux-yocto-dev.yml` | Select the kernel with `PREFERRED_PROVIDER_virtual/kernel` (and `PREFERRED_VERSION_virtual/kernel = "6.18%"` for 6.18); `linux-yocto-dev` also removes the `version-going-backwards` QA error for that recipe. |
| [u-boot-qcom.yml](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/ci/u-boot-qcom.yml) | `PREFERRED_PROVIDER_virtual/bootloader = "u-boot-qcom"`. |
| [kernel-fit-image.yml](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/ci/kernel-fit-image.yml) | U-Boot FIT boot: removes `linux-qcom-bootimg` from and adds `kernel-fit-extra-artifacts` to `KERNEL_CLASSES`, sets `QCOM_ESP_IMAGE = "esp-qcom-fit-image"` and an empty `EFI_PROVIDER`. |
| `capsule.yml`, `capsule-test-keys.yml` | Build the UEFI capsule (`firmware-qcom-capsule` as `virtual/qcom-capsule-firmware` and its runtime package); the second signs it with the development keys in `ci/test-keys/` (`CAPSULE_ROOT_CER`, `CAPSULE_CERT_PEM`, `CAPSULE_ROOT_PUB`, `CAPSULE_SUB_PUB`), never for production. |
| [meta-arm.yml](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/ci/meta-arm.yml), [dpdk.yml](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/ci/dpdk.yml), [test-oe-nogl.yml](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/ci/test-oe-nogl.yml) | Add [meta-arm](https://git.yoctoproject.org/meta-arm) with meta-arm-toolchain, [meta-dpdk](https://git.yoctoproject.org/meta-dpdk), or meta-oe from [meta-openembedded](https://github.com/openembedded/meta-openembedded); the last also removes `opengl` from `DISTRO_FEATURES`. |
| [debug.yml](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/ci/debug.yml) | `DEBUG_BUILD = "1"`, a debug filesystem image (`IMAGE_GEN_DEBUGFS = "1"`, `IMAGE_FSTYPES_DEBUGFS = "tar.zst"`), and ftrace events on the kernel command line through `KERNEL_CMDLINE_EXTRA_FTRACE`. |
| [performance.yml](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/ci/performance.yml) | Appends `quiet`, a dumb console terminal, root-only udev triggering, and no efivarfs in the initramfs to the kernel command line. |
| [ci.yml](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/ci/ci.yml) | CI build settings, commented in the file: includes `mirror.yml` and `ccache.yml`, `OEBasicHash` signatures, zstd firmware compression, RPM packages, memory-bounded parallelism, job-local git clones with mirror tarballs, and shallow kernel fetches. |
| [ccache.yml](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/ci/ccache.yml) | Enables ccache (200 GB under `${SSTATE_DIR}/ccache`) only for the listed large recipes. |
| `mirror.yml`, `mirror-tarballs.yml`, `mirror-download-test.yml`, `mirror-download-disable.yml` | Use the Yocto Project sstate mirror; generate mirror tarballs; fetch only from `QLI_MIRRORS`; or drop the `qli-mirrors` class. |
| [nospdx.yml](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/ci/nospdx.yml), [world.yml](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/ci/world.yml) | Skip SPDX 3.0 image documents; build `world` limited to this layer's recipes. |

`base.yml` writes these `local.conf` settings:

| Setting | Purpose | Value and default |
| --- | --- | --- |
| `CONF_VERSION` | Configuration format version checked by OE-Core. | `2`. |
| `INHERIT` | Adds `buildstats-summary`, `buildhistory`, `rm_work`, and `image-buildinfo`. | Unset: none of these classes run. |
| `BB_DISKMON_DIRS` | Stops tasks when `TMPDIR`, `DL_DIR`, `SSTATE_DIR`, or `/tmp` runs low, and halts at a lower limit. | Weak default (`??=`); unset: OE-Core's default monitoring. |
| `MIRRORS:append` | Falls back to the CodeLinaro mirrors for GitHub, other git, and HTTPS sources. | Unset: only upstream sources and OE-Core mirrors. |
| `KERNEL_CMDLINE_EXTRA:append` | Adds `qcom_scm.download_mode=1`, so a crash enters download mode. | Unset: the machine's command line. |
| `DISTRO_FEATURES:append` | Adds `efi`, `pam`, and `pni-names` (predictable network interface names). | Unset: the distro's features. |
| `EXTRA_IMAGE_FEATURES` | `allow-empty-password empty-root-password allow-root-login`: root logs in without a password, for development only. | Unset: root has no password login. |
| `IMAGE_ROOTFS_EXTRA_SPACE` | 307200 KiB of free space in the root filesystem. | Unset: `0`. |
| `WATCHDOG_RUNTIME_SEC:pn-systemd` | systemd's hardware watchdog period, 30 seconds. | Unset: no runtime watchdog. |
| `OS_RELEASE_FIELDS:append`, `BUILD_ID` | Records `BUILD_ID` in `/etc/os-release`, `local-${DATETIME}` unless CI's generated `ci/build-id.yml` sets it. | Weak default (`?=`). |

## Layer configuration

[conf/layer.conf](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/conf/layer.conf)
registers the layer; its lines are:

| Setting | Purpose and value |
| --- | --- |
| `BBPATH`, `BBFILES`, `BBFILE_COLLECTIONS`, `BBFILE_PATTERN_qcom`, `BBFILE_PRIORITY_qcom` | Standard layer registration: the `qcom` collection's recipes are `recipes-*/*/*.bb` and `.bbappend`, at priority 6. |
| `LAYERDIR_qcom` | Layer root, so kas files and recipes can use files such as `ci/test-keys/`. |
| `LAYERDEPENDS_qcom`, `LAYERRECOMMENDS_qcom`, `LAYERSERIES_COMPAT_qcom` | Requires OE-Core (`core`), recommends `openembedded-layer` and `meta-arm`, and supports the `wrynose` series. |
| `LICENSE_PATH` | Adds `licenses/`, which holds the texts of `LicenseRef-LICENSE.qcom` and `LicenseRef-LICENSE.qcom-2`. |
| `BBFILES_DYNAMIC` | Parses `dynamic-layers/<collection>/` only when that collection is present: `ai`, `meta-arm`, `networking-layer` (no recipes yet), `openembedded-layer`, `qcom-distro`, `selinux`, and `virtualization-layer`. |
| `QLI_BASELINE` | Qualcomm Linux baseline, `main`: the path under which the `qli-mirrors` class finds its mirrored downloads. |
| `INHERIT += "qli-mirrors"` | Adds the Qualcomm Linux source mirrors to every build; `mirror-download-disable.yml` removes it. |
| `PREFERRED_RPROVIDER_virtual-diag-router` | Weak default `diag`, so images get one diagnostics router when `diag` and `diag-router` both exist. |
| `addpylib` | Makes `lib/qcom/` importable as the `qcom` Python module. |
| `SIGGEN_EXCLUDE_SAFE_RECIPE_DEPS` | Keeps `kgsl-dlkm`, a runtime-only dependency, out of `qcom-adreno`'s task signatures. |

## Machine configuration

Each machine file in
[conf/machine/](https://github.com/devdocsorg/meta-qcom/tree/docs/layer-documentation/conf/machine)
requires its SoC include (or `qcom-common.inc` for the generic `qcom-armv7a` and
`qcom-armv8a`) and sets the variables below. `qcs6490-rb3gen2-core-kit` and
`qrb2210-rb1-core-kit` are deprecated names that only require `rb3gen2-core-kit` and
`rb1-core-kit`; the `-open-fw` machines require their base board file.
"Weak" means `?=` or `??=`, which `local.conf` can override.

| Variable | Purpose | Type and default | Example |
| --- | --- | --- | --- |
| `SOC_FAMILY` | SoC name, added to the overrides by `soc-family.inc`. | String, set by each SoC include. | `qcm6490` |
| `MACHINEOVERRIDES =. "qcom:"` | Adds the `qcom` override that this layer's `:qcom` appends use. | Set by `qcom-common.inc`. | — |
| `DEFAULTTUNE` and the `arch-*`/`tune-*` include | CPU tuning for the SoC. | Set by each SoC include. | `armv8-2a-crypto` |
| `MACHINE_FEATURES` | Hardware features: `alsa bluetooth usbgadget usbhost wifi` from `qcom-common.inc`, plus `efi`, `pci`, `phone`, `screen`, `ext2`, `ext3`, `opengl`, `usb`, `tpm2`, `kvm` (selects the KVM boot firmware configuration and U-Boot Gunyah exit), `optee` (open OP-TEE firmware), and `m2connector`, which no recipe in this layer reads. | Space-separated list; some boards replace the default with `=`. | `efi pci tpm2` |
| `KERNEL_DEVICETREE` | Devicetrees and overlays the kernel builds. | Weak list per board. | `qcom/qcs6490-rb3gen2.dtb` |
| `LINUX_QCOM_KERNEL_DEVICETREE` | Extra devicetrees that exist only in the `linux-qcom*` kernels, appended to `KERNEL_DEVICETREE` for those kernels and FIT images built from them. | Weak list; default empty. | `qcom/kodiak-staging.dtbo` |
| `FIT_DTB_COMPATIBLE[<compatible>]` | Maps each board compatible string to a devicetree and its overlays for the multi-DTB FIT image; `fit-dtb-compatible.inc` holds the upstream set and `fit-dtb-compatible-linux-qcom.inc` adds the `linux-qcom*` ones. | Flag per compatible; `dtb-fit-image.bbclass` fails on a devicetree that no entry covers. | `FIT_DTB_COMPATIBLE[qcom_apq8016-sbc] = "apq8016-sbc"` |
| `QCOM_DTB_DEFAULT` | Devicetree image placed in the flash package as `dtb.bin`; `multi-dtb` builds the multi-DTB FIT image instead. | Weak; default `multi-dtb`. | `qcs8300-ride` |
| `MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS`, `MACHINE_EXTRA_RRECOMMENDS` | Board packages: `packagegroup-qcom-boot-essential`/`-additional`, the SoC and board firmware, Hexagon DSP, FastCV, and QAIRT packages, and tools such as `qrtr`, `rmtfs`, `tqftpserv`, `pd-mapper`, `fastrpc`, `qbootctl`, `qps615-dlkm`, and `packagegroup-optee`. | Appended lists. | `packagegroup-rb3gen2-firmware` |
| `QCOM_BOOT_FIRMWARE`, `QCOM_CDT_FIRMWARE` | Recipes that deploy the boot firmware and the CDT (board configuration data table) for the flash package. | Recipe name; default empty (none added). | `firmware-qcom-boot-qcs6490` |
| `QCOM_BOOT_FILES_SUBDIR` | Deploy subdirectory holding those firmware files. | Path; default empty. | `qcm6490` |
| `QCOM_CDT_FILE` | CDT file name, without `.bin`, copied as `cdt.bin`. | String; default empty. | `cdt_core_kit` |
| `QCOM_PARTITION_FILES_SUBDIR`, `QCOM_PARTITION_FILES_SUBDIR_SPINOR` | Partition tables for the main storage and for SPI-NOR. | Weak path; defaults `${QCOM_BOOT_FILES_SUBDIR}` and empty. | `partitions/qcs6490-rb3gen2/ufs` |
| `QCOM_XBL_CONFIG`, `QCOM_UEFI_DTB` | Boot firmware configuration and UEFI devicetree files; the `kvm` feature selects the `_kvm` variants. | Weak file names. | `xbl_config.elf` |
| `PREFERRED_PROVIDER_virtual/kernel` | Kernel recipe: `linux-qcom-next` on current platforms, `linux-yocto` otherwise. | Weak. | `linux-qcom-6.18` via its kas file |
| `KERNEL_IMAGETYPE`, `KERNEL_IMAGETYPES`, `KERNEL_ALT_IMAGETYPE` | Kernel images to build: `Image`, `Image.gz`, and `vmlinux` on current platforms, `zImage` on Armv7. | Weak strings. | `Image` |
| `KERNEL_CLASSES` | Adds `linux-qcom-dtbbin` (devicetree partition images) and, on `qcom-armv7a`/`qcom-armv8a`, `linux-qcom-bootimg` (Android boot images). | Appended list. | — |
| `IMAGE_CLASSES`, `IMAGE_FSTYPES`, `IMAGE_ROOTFS_ALIGNMENT`, `EXTRA_IMAGECMD:ext4` | Adds `image_types_qcom` and the `qcomflash` package, a 4096-aligned `ext4` root filesystem with 4096-byte blocks, and `ubi` images on SDX55/SDX75. | Appended or set per include. | `ext4 qcomflash` |
| `MKUBIFS_ARGS`, `UBINIZE_ARGS` | UBI geometry for the SDX75 IDP NAND. | Weak strings. | `-m 4096 -p 262144` |
| `SERIAL_CONSOLES`, `SERIAL_CONSOLE` | Login console `ttyMSM0` at 115200 baud. | Weak. | `115200;ttyMSM0` |
| `QCOM_BOOTIMG_ROOTFS`, `SD_QCOM_BOOTIMG_ROOTFS`, `QCOM_BOOTIMG_PAGE_SIZE`, `QCOM_BOOTIMG_KERNEL_BASE` | Root device, page size, and kernel base for Android boot images; `[<dtb>]` flags override them per board in `qcom-armv8a.conf`. | Weak; defaults `PARTLABEL=rootfs`, `4096`, `0x80000000`. | `PARTLABEL=system` |
| `KERNEL_CMDLINE_EXTRA` | Board command-line additions, such as `clk_ignore_unused pd_ignore_unused`, `arm64.nopauth`, and `systemd.tpm2_wait=false`. | String; flags per devicetree on `qcom-armv8a`. | `arm64.nopauth` |
| `QCOM_RT_CPU`, `QCOM_IRQAFF`, `QCOM_RCU_NOCBS`, `QCOM_RCU_EXPEDITED`, `QCOM_CPUIDLE_OFF` | Real-time tuning, added to the command line as `isolcpus`, `irqaffinity`, `rcu_nocbs`, `rcupdate.rcu_expedited`, and `cpuidle.off` (through `RT_ARGS_*` and `RT_KERNEL_CMDLINE`, with `efi=runtime`) only for `linux-qcom-rt` and `linux-qcom-next-rt`. | CPU lists or `1`; weak default empty (argument omitted). | `QCOM_RT_CPU = "7"` |
| `QCOM_VFAT_SECTOR_SIZE` | Sector size of the devicetree and ESP images. | Weak; `4096` (UFS), `512` on QCM2290. | `512` |
| `EFI_PROVIDER`, `EFI_LINUX_IMG` | EFI boot manager and unified kernel image name. | Weak; `systemd-boot`, `linux-${MACHINE}.efi`. | — |
| `FIT_DTB_MKIMAGE_EXTRA_OPTS` | `mkimage` options for the devicetree FIT: external data (`-E`) and 8-byte alignment (`-B 8`). | Weak string. | `-E -B 8` |
| `INITRAMFS_MAXSIZE` | Initramfs size limit, 640 MiB, and 960 MiB for the full test initramfs images. | KiB. | `655360` |
| `UBOOT_CONFIG`, `UBOOT_CONFIG[<name>]`, `UBOOT_CONFIG_DEFAULT`, `UBOOT_INITIAL_ENV`, `UBOOT_ENTRYPOINT` | U-Boot configurations to build and their defconfigs, the default one, no initial environment file, and the entry point on QCM6490 and QCS9100. | Board names; weak defaults. | `qcs6490-rb3gen2` |
| `BOARD_MBN_HEADER[<name>]` | MBN header version used to sign each U-Boot configuration. | `v5` or `v6`. | `v6` |
| `PREFERRED_PROVIDER_virtual/bootloader`, `EXTRA_IMAGEDEPENDS` | `u-boot-qcom` or `u-boot` as the boot loader; open-firmware boards also build their TF-A, and `qcom-armv*` images their Android boot images. | Recipe names. | `u-boot-qcom` |
| `QCOM_UBOOT_SPL_FIT`, `UBOOT_FITIMAGE_ENABLE`, `UBOOT_FIT_*`, `SPL_BINARY`, `QCOM_XBL_CONFIG` in `qcom-uboot-spl-fit.inc` | U-Boot SPL FIT boot: packs TF-A (`atf`) and OP-TEE with U-Boot in a FIT configuration described as `post-ddr`, with `xbl_config_spl.elf`. | `1` to enable; default `0`. | `1` |
| `QCOM_UBOOT_SPL_FIT_ATF`, `QCOM_UBOOT_SPL_FIT_TEE`, `QCOM_UBOOT_SPL_SWIV_PLATFORM`, `QCOM_UBOOT_SPL_ENTRY`, `UBOOT_FIT_*_LOADADDRESS`/`ENTRYPOINT` | QCS9100 recipes and addresses for that FIT; no recipe reads `QCOM_UBOOT_SPL_ENTRY`. | Weak recipe names and addresses. | `0x1c200000` |
| `QCOM_FIT_BOOT_CONF` | FIT configuration that the U-Boot boot script selects. | Weak string. | `#conf-lemans-evk.dtb#conf-lemans-el2.dtbo` |
| `CAPSULE_GUID`, `CAPSULE_FLASH_TYPE`, `CAPSULE_ENTRIES`, `CAPSULE_ENTRY_<name>[...]` | UEFI capsule identity and, per entry, the binary and its destination and backup partitions. | GUIDs and names, IQ-X7181 only. | `CAPSULE_ENTRIES = "dtb"` |
| `VIRTUAL-RUNTIME_qcom-capsule-firmware` | Capsule package added to images. | Weak; default empty. | `firmware-qcom-capsule` |
| `VERSION_abseil-cpp`, `VERSION_protobuf`, `PREFERRED_VERSION_*` | Versions of abseil-cpp and protobuf that the prebuilt binaries need. | Weak; `20260107.1` and empty (any version). | `20260107.1` |
| `XSERVER`, `XSERVER_OPENGL` | X server packages, with modesetting and GLX when `opengl` is a distro feature. | Weak lists. | — |

## Kernel and U-Boot fragments

These files hold Kconfig options: `=y` builds a feature in, `=m` as a module, and
`# CONFIG_X is not set` disables it; options not listed keep the kernel's or U-Boot's
defconfig value ([Kconfig](https://www.kernel.org/doc/html/latest/kbuild/kconfig.html)).
Comments in each file group the options by board or purpose.

| Files | Used by |
| --- | --- |
| `recipes-kernel/linux/linux-qcom-next/configs/bsp-additions.cfg`, `linux-qcom-6.18/configs/bsp-additions.cfg` | The `linux-qcom*` kernels, on top of the upstream defconfig and `prune.config`/`qcom.config`, plus `hardening.config` with the `hardened` distro feature and the debug configs with `DEBUG_BUILD`. |
| `recipes-kernel/linux/linux-yocto-7.2/` (`qcom.scc` and `bsp/`) | `linux-yocto` 7.2, as kernel-cache metadata: `.scc` files select the fragments per machine ([kernel metadata](https://docs.yoctoproject.org/kernel-dev/advanced.html)). |
| `recipes-kernel/linux/linux-yocto-dev/configs/qcom.cfg` | `linux-yocto-dev` on Qualcomm machines. |
| `recipes-bsp/u-boot/files/*.cfg` | `u-boot-qcom`: disable the capsule tool, runtime EFI variables, Gunyah EL2 exit, SPL FIT signatures with `SPL_SIGN_ENABLE`, and TF-A/OP-TEE support. |

## Files installed on the target

| File | Effect |
| --- | --- |
| `recipes-core/systemd/systemd/99-dma-heap.rules` | `/dev/dma_heap/system` belongs to group `dmaheap`, mode 0660. |
| `recipes-graphics/kgsl-dlkm/kgsl-dlkm/kgsl.rules` | `/dev/kgsl-3d0` belongs to group `render`, mode 0660, with seat access. |
| `recipes-bsp/partition/mount-tee-partition/` | `persist.rules` mounts the `persist` partition at `/var/lib/tee` through `var-lib-tee.mount`; `format-tee-partition.service` creates its ext4 filesystem first when missing. |
| `recipes-kernel/iris-video-module/iris-video-dlkm/blacklist-video.conf.*` | Two modprobe blocklists: `.venus` blocks the upstream `qcom_iris` and `venus` drivers, and `.vidc` blocks `iris_vpu`, preferred through update-alternatives on QCS615 and Shikra. |
| `recipes-support/qbootctl/files/qbootctl-bless-boot.service.in` | Marks the current A/B boot slot good with `qbootctl -m` once `boot-complete.target` is reached. |
| `recipes-bsp/u-boot/u-boot-scr-qcom-fit/boot.cmd.in` | U-Boot script that loads `/fitImage` with the kernel command line and `QCOM_FIT_BOOT_CONF`. |
| `dynamic-layers/.../android-tools-adbd-cmdline/50-adbd-cmdline.conf`, `recipes-graphics/wayland/weston-init/additional-devices.conf`, `dynamic-layers/.../android-tools-conf/qcom/android-gadget-setup.machine` | systemd drop-ins and a USB gadget identity, commented in the files. |

## Environment variables

[.env.example](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/.env.example)
documents the variables that `kas-container` and the `ci/` scripts read; nothing
loads that file.

## CI workflows

| Workflow | Trigger and checks |
| --- | --- |
| `pr.yml` | Pull requests to `master` that change more than Markdown: runs `build-yocto.yml` with the `pr` profile. |
| `push.yml`, `nightly-build.yml`, `weekly-build.yml` | Pushes to `master`, 00:22 UTC Sunday to Friday, and 00:22 UTC Saturday: builds, then `test.yml` and `publish-results.yml`. |
| `nightly-build-wrynose.yml` | Nightly: runs `nightly-build.yml` on the `wrynose` branch. |
| `build-yocto.yml`, `compile.yml` | Called: locks the kas repositories, runs `yocto-patchreview`, `yocto-check-layer`, and `oe-selftest`, then builds the machine, distro, and kernel matrix. |
| `test.yml`, `test-distro.yml`, `test-pr.yml`, `test-pr-wrynose.yml` | Boot and pre-merge tests on LAVA devices, for builds and for completed pull request builds, with a pull request comment. |
| `publish-results.yml` | Called: publishes test results. |
| `markdownlint.yml` | Markdown changes: checks every `*.md` against `.github/.markdownlint.yaml`. |
| `documentation.yml` | Pull requests and pushes to `master`: builds this site and checks function reference coverage and offline browsing. |
| `repolinter.yml` | Pushes and pull requests to `master`: the organisation's repository lint rules. |
| `backport.yml` | Merged pull requests labelled `backport wrynose`: opens the backport pull request. |
| `stales.yml`, `sstate-cleanup.yml` | Daily and weekly: close stale issues and pull requests; expire unused shared-state files. |

The workflows are in
[.github/workflows/](https://github.com/devdocsorg/meta-qcom/tree/docs/layer-documentation/.github/workflows),
and the composite actions they use are in
[.github/actions/](https://github.com/devdocsorg/meta-qcom/tree/docs/layer-documentation/.github/actions),
with their inputs described in each `action.yml`. `.github/.markdownlint.yaml`,
`.github/CODEOWNERS`, and `.gitignore` are commented in place.
