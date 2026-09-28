# Configuration reference

Builds combine kas fragments from `ci/`, the layer settings in `conf/layer.conf`,
and a machine configuration from `conf/machine/`. Standard BitBake and Yocto
variables keep their upstream meaning; follow the links for their full
definitions. The tables cover what this layer sets and why.

## How settings load

kas reads the fragments named on its command line from left to right, joined
with `:`; a later fragment overrides the same key in an earlier one, and
`header.includes` pulls in other fragments first
([kas project configuration](https://kas.readthedocs.io/en/5.5/userguide/project-configuration.html)).
kas writes the `local_conf_header` entries into `conf/local.conf` and adds
each repository's layers to `conf/bblayers.conf`. `machine` selects a file in
`conf/machine/`, which `require`s its SoC include, which requires
`qcom-base.inc` and `qcom-common.inc`. BitBake then applies its
[assignment operators](https://docs.yoctoproject.org/bitbake/2.18/bitbake-user-manual/bitbake-user-manual-metadata.html#basic-syntax):
`=` and `:=` set a value, `?=` sets it only when unset, `??=` is the weakest
default, and `+=`, `:append`, and `:remove` edit an existing value.

## Build fragments

Compose a build as `ci/<machine>.yml[:ci/<distro>.yml][:ci/<kernel>.yml][:<options>]`.
Every fragment uses kas format version 14.

| Fragment | Purpose and settings |
| --- | --- |
| `ci/base.yml` | Common base: `nodistro`, `master` branches, [openembedded-core](https://github.com/openembedded/openembedded-core) with the three `patches/oe-core` patches, [bitbake](https://github.com/openembedded/bitbake), and target `core-image-base`. Its `local_conf_header` entries are in the next table. |
| `ci/base.lock.yml` | Pins each layer to a commit (`overrides.repos.<name>.commit`); kas loads it whenever `ci/base.yml` is used. CI regenerates it with `kas lock` before building. |
| `ci/<machine>.yml` | One per machine in `conf/machine/`: includes `ci/base.yml` and sets `machine`. The `-open-fw` machines also include `ci/meta-arm.yml`; `ci/sdx75-idp.yml` builds `core-image-minimal`; `ci/qcom-armv8a.yml` sets `PREFERRED_PROVIDER_virtual/dtb = "devicetree-dummy"` and `QCOM_BOOTIMG_DEVICETREE = "qcom-armv8-dummy.dtb"`. `ci/qcs6490-rb3gen2-core-kit.yml` and `ci/qrb2210-rb1-core-kit.yml` link to the renamed machines' fragments. |
| `ci/qcom-distro.yml` | Selects `qcom-distro` from [meta-qcom-distro](https://github.com/qualcomm-linux/meta-qcom-distro), adds [meta-openembedded](https://github.com/openembedded/meta-openembedded) (seven layers), [meta-ai](https://github.com/qualcomm-linux/meta-ai), [meta-virtualization](https://git.yoctoproject.org/meta-virtualization) (`SKIP_META_VIRT_SANITY_CHECK = "1"`), [meta-audioreach](https://github.com/AudioReach/meta-audioreach), [meta-selinux](https://git.yoctoproject.org/meta-selinux) with the three `patches/selinux` patches, [meta-updater](https://github.com/uptane/meta-updater), and [meta-security](https://git.yoctoproject.org/meta-security) with meta-tpm, and builds the four `qcom-*-image` targets. |
| `ci/qcom-distro-catchall.yml`, `-selinux.yml`, `-sota.yml` | Include `ci/qcom-distro.yml` and switch to the `qcom-distro-catchall`, `qcom-distro-selinux`, or `qcom-distro-sota` distro; the first two narrow the target list. |
| `ci/qcom-distro-kvm.yml`, `-multimedia-image.yml` | Include `ci/qcom-distro.yml`; add `kvm` to `MACHINE_FEATURES`, or build only `qcom-multimedia-image`. |
| `ci/linux-qcom-6.18.yml`, `ci/linux-qcom-rt-6.18.yml` | Set `PREFERRED_PROVIDER_virtual/kernel` to `linux-qcom` or `linux-qcom-rt` with `PREFERRED_VERSION_virtual/kernel = "6.18%"`. |
| `ci/linux-qcom-next.yml`, `ci/linux-qcom-next-rt.yml` | Select `linux-qcom-next` or `linux-qcom-next-rt`. |
| `ci/linux-yocto-dev.yml` | Selects `linux-yocto-dev` and drops the `version-going-backwards` QA error for it. |
| `ci/u-boot-qcom.yml` | Sets `PREFERRED_PROVIDER_virtual/bootloader = "u-boot-qcom"`. |
| `ci/kernel-fit-image.yml` | U-Boot FIT kernel flow: removes `linux-qcom-bootimg` from `KERNEL_CLASSES`, adds `kernel-fit-extra-artifacts`, and sets `QCOM_ESP_IMAGE = "esp-qcom-fit-image"` and an empty `EFI_PROVIDER`. |
| `ci/capsule.yml`, `ci/capsule-test-keys.yml` | Build the UEFI capsule (`firmware-qcom-capsule` as provider and runtime package), and sign it with the development keys in `ci/test-keys/` (`CAPSULE_ROOT_CER`, `CAPSULE_CERT_PEM`, `CAPSULE_ROOT_PUB`, `CAPSULE_SUB_PUB`). Never use those keys in production. |
| `ci/meta-arm.yml`, `ci/dpdk.yml` | Add [meta-arm](https://git.yoctoproject.org/meta-arm) with meta-arm-toolchain, or [meta-dpdk](https://git.yoctoproject.org/meta-dpdk), on `master`. |
| `ci/debug.yml` | `DEBUG_BUILD = "1"`, debug filesystem images as `tar.zst`, and an ftrace kernel command line (`KERNEL_CMDLINE_EXTRA_FTRACE`). |
| `ci/performance.yml` | Appends `quiet systemd.tty.term.console=dumb initramfs.udev-root-only=1 initramfs.efivarfs=0` to the kernel command line. |
| `ci/nospdx.yml` | Removes `create-spdx-image-3.0` from `IMAGE_CLASSES`. |
| `ci/test-oe-nogl.yml` | Adds meta-oe from [meta-openembedded](https://github.com/openembedded/meta-openembedded) and removes `opengl` from `DISTRO_FEATURES`. |
| `ci/world.yml` | Builds `world` limited to this layer (`EXCLUDE_FROM_WORLD` is `1`, and `0` for `layer-qcom`); a commented line would also include `layer-qcom-distro`. |
| `ci/ci.yml` | CI settings; includes `ci/mirror.yml` and `ci/ccache.yml`, and sets `BB_SIGNATURE_HANDLER = "OEBasicHash"`, `FIRMWARE_COMPRESSION:qcom-armv8a = "zst"`, `PACKAGE_CLASSES = "package_rpm"`, memory-bounded parallelism (`BB_PRESSURE_MAX_MEMORY`, `PARALLEL_MAKE`, `do_compile[number_threads]`), job-local git clones, and shallow qcom kernel fetches. Its comments give the reasons. |
| `ci/ccache.yml` | Enables ccache in `${SSTATE_DIR}/ccache` (200G) for the compiler, toolchain, kernel, and large C++ recipes only. |
| `ci/mirror.yml` | Uses the Yocto Project shared-state mirror. |
| `ci/mirror-download-disable.yml`, `-test.yml`, `-tarballs.yml` | Mirror maintenance: drop `qli-mirrors`, fetch only from `QLI_MIRRORS` (`BB_FETCH_PREMIRRORONLY`), or generate mirror tarballs. |

`ci/base.yml` writes these `local_conf_header` entries:

| Entry | Settings |
| --- | --- |
| `base` | `CONF_VERSION = "2"`; inherits `buildstats-summary`, `buildhistory`, `rm_work`, and `image-buildinfo`. |
| `diskmon` | `BB_DISKMON_DIRS ??=` stops tasks below 1G free (100M for `/tmp`) and halts below 100M (10M) in `TMPDIR`, `DL_DIR`, and `SSTATE_DIR`. |
| `clo-mirrors` | `MIRRORS:append` sends GitHub, other git, and HTTPS fetches to CodeLinaro mirrors when the original fails. |
| `cmdline` | Appends `qcom_scm.download_mode=1` to `KERNEL_CMDLINE_EXTRA`. |
| `extra` | Adds `efi pam pni-names` to `DISTRO_FEATURES`, passwordless root login (`EXTRA_IMAGE_FEATURES`), `IMAGE_ROOTFS_EXTRA_SPACE = "307200"` (KiB), and a 30 s systemd watchdog. |
| `os-release` | Adds `BUILD_ID` to `/etc/os-release`; `BUILD_ID ?= "local-${DATETIME}"`, which CI overrides through the generated, ignored `ci/build-id.yml`. |

## Layer settings

`conf/layer.conf` registers the layer with BitBake
([layer variables](https://docs.yoctoproject.org/6.0/ref-manual/variables.html#term-BBFILE_COLLECTIONS)).

| Setting | Local value and purpose |
| --- | --- |
| `BBPATH`, `BBFILES` | Add the layer and its `recipes-*/*/*.bb` and `.bbappend` files. |
| `LAYERDIR_qcom` | Layer root, so recipes can use files such as `ci/test-keys/`. |
| `BBFILE_COLLECTIONS`, `BBFILE_PATTERN_qcom`, `BBFILE_PRIORITY_qcom` | Collection `qcom`, priority `6`. |
| `LAYERDEPENDS_qcom`, `LAYERRECOMMENDS_qcom`, `LAYERSERIES_COMPAT_qcom` | Requires `core`; recommends `openembedded-layer` and `meta-arm`; compatible with `wrynose`. |
| `LICENSE_PATH` | Adds `licenses/` for the Qualcomm licences. |
| `BBFILES_DYNAMIC` | Adds `dynamic-layers/<collection>/` recipes only when that collection is present: `ai`, `meta-arm`, `networking-layer`, `openembedded-layer`, `qcom-distro`, `selinux`, `virtualization-layer`. |
| `QLI_BASELINE` | `main`, the Qualcomm Linux baseline name. |
| `INHERIT += "qli-mirrors"` | Adds the Qualcomm Linux download mirrors from `classes/qli-mirrors.bbclass`. |
| `PREFERRED_RPROVIDER_virtual-diag-router` | `?= "diag"`, which picks `diag` when `diag-router` is also available. |
| `addpylib` | Makes `lib/` importable as the `qcom` Python namespace. |
| `SIGGEN_EXCLUDE_SAFE_RECIPE_DEPS` | Keeps the runtime-only `qcom-adreno->kgsl-dlkm` dependency out of task signatures. |

## Machine settings

Each `conf/machine/<machine>.conf` requires one SoC include, such as
`qcom-qcs6490.inc`, which sets `SOC_FAMILY`, `DEFAULTTUNE`, and the SoC
package groups. `qcom-common.inc` holds the shared defaults and requires
`qcom-common-binary.inc` (binary recipe versions) and `qcom-u-boot-common.inc`.
The machine files set these Qualcomm settings:

| Setting | Purpose | Type and default | Safe example |
| --- | --- | --- | --- |
| `QCOM_BOOT_FIRMWARE`, `QCOM_CDT_FIRMWARE` | Recipes that deploy boot firmware and the CDT into the flash package. | Recipe name; `""` skips it. | `firmware-qcom-boot-qcs6490` |
| `QCOM_BOOT_FILES_SUBDIR`, `QCOM_CDT_FILE` | Deploy subfolder with those files, and the CDT file name without `.bin`. | Path and name; `""`. | `qcm6490`, `cdt_core_kit` |
| `QCOM_PARTITION_FILES_SUBDIR`, `QCOM_PARTITION_FILES_SUBDIR_SPINOR` | Partition layouts from `qcom-partition-conf` for the main storage and SPI-NOR. | Path; defaults to the boot subfolder, and `""`. | `partitions/qcs6490-rb3gen2/ufs` |
| `QCOM_DTB_DEFAULT` | Device tree packed as `dtb.bin`, or `multi-dtb` for the FIT with every DTB. | DTB name; `??= "multi-dtb"`. | `qcs615-ride` |
| `LINUX_QCOM_KERNEL_DEVICETREE` | Device trees built only by the `linux-qcom*` kernels, added to `KERNEL_DEVICETREE` for them. | DTB list; `""`. | `qcom/kodiak-el2.dtbo` |
| `QCOM_RT_CPU`, `QCOM_IRQAFF`, `QCOM_RCU_NOCBS`, `QCOM_RCU_EXPEDITED`, `QCOM_CPUIDLE_OFF` | Real-time kernel arguments `isolcpus`, `irqaffinity`, `rcu_nocbs`, `rcupdate.rcu_expedited`, and `cpuidle.off`; `qcom-common.inc` builds them into `RT_ARGS_*` and `RT_KERNEL_CMDLINE`, with `efi=runtime`, and appends them only with `linux-qcom-rt` or `linux-qcom-next-rt`. | CPU list or `1`; `""` omits the argument. | `7`, `0-6` |
| `QCOM_XBL_CONFIG`, `QCOM_UEFI_DTB` | Boot firmware variant; the `kvm` machine feature picks the KVM files. | File name. | `xbl_config.elf` |
| `QCOM_BOOTIMG_*`, `SD_QCOM_BOOTIMG_ROOTFS`, `QCOM_VFAT_SECTOR_SIZE` | Android boot image kernel base, page size, and root device (for SD-card boot images too), and the VFAT sector size. | Address, size, or device; `0x80000000`, `4096`, `PARTLABEL=rootfs`, `4096`. | `2048` |
| `UBOOT_CONFIG` and its `[<board>]` flags, `BOARD_MBN_HEADER[<board>]` | U-Boot board, its defconfig, and the MBN header version. | Board name; `""` builds none. | `qcs6490-rb3gen2` |
| `CAPSULE_GUID`, `CAPSULE_FLASH_TYPE`, `CAPSULE_ENTRIES`, `CAPSULE_ENTRY_<name>[...]` | UEFI capsule identity and the partitions it updates (`iq-x7181-evk`). | GUID, type, and names. | `CAPSULE_ENTRIES = "dtb"` |
| `VIRTUAL-RUNTIME_qcom-capsule-firmware` | Capsule package added to `MACHINE_EXTRA_RRECOMMENDS`. | Package name; `""`. | `firmware-qcom-capsule` |
| `QCOM_UBOOT_SPL_FIT`, `SPL_BINARY`, `UBOOT_FIT_*`, `QCOM_FIT_BOOT_CONF` | U-Boot SPL FIT boot flow from `qcom-uboot-spl-fit.inc`, whose comments explain each setting, and the FIT configuration it boots. | `1` or unset; name. | `1` |
| `QCOM_UBOOT_SPL_ENTRY`, `QCOM_UBOOT_SPL_FIT_ATF`, `QCOM_UBOOT_SPL_FIT_TEE`, `QCOM_UBOOT_SPL_SWIV_PLATFORM` | SoC inputs for that flow: SPL entry address, TF-A and OP-TEE recipes, and SWIV platform (`qcom-qcs9100.inc`, with the `UBOOT_FIT_*` load addresses). | Address, recipe, or name. | `lemans` |
| `FIT_DTB_MKIMAGE_EXTRA_OPTS` | mkimage options for the DTB FIT. | Options; `-E -B 8`. | `-E -B 8` |
| `VERSION_abseil-cpp`, `VERSION_protobuf` | Versions the binary recipes need; `""` leaves protobuf unpinned. | Version. | `20260107.1` |

The machines also set standard variables:
[`MACHINE_FEATURES`](https://docs.yoctoproject.org/6.0/ref-manual/variables.html#term-MACHINE_FEATURES)
(base `alsa bluetooth usbgadget usbhost wifi`, plus per-board features),
[`KERNEL_DEVICETREE`](https://docs.yoctoproject.org/6.0/ref-manual/variables.html#term-KERNEL_DEVICETREE),
[`MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS`](https://docs.yoctoproject.org/6.0/ref-manual/variables.html#term-MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS)
and `MACHINE_EXTRA_RRECOMMENDS` (board firmware and package groups),
kernel image types and classes, `EXTRA_IMAGECMD:ext4` (4096-byte blocks),
`EXTRA_IMAGEDEPENDS` (Android boot images for the generic machines, TF-A for the
open-firmware ones),
`MACHINEOVERRIDES` (adds `qcom`), `XSERVER` and `XSERVER_OPENGL`, `EFI_PROVIDER`
(`systemd-boot`) and `EFI_LINUX_IMG` (the unified kernel image name),
`PREFERRED_PROVIDER_virtual/kernel` (default
`linux-qcom-next`, `linux-yocto` for `qcom-armv8a`), `SERIAL_CONSOLES`
(`115200;ttyMSM0`), `IMAGE_FSTYPES` (`ext4` and `qcomflash`; `ubi` with
`MKUBIFS_ARGS` and `UBINIZE_ARGS` for `sdx75-idp`), and `INITRAMFS_MAXSIZE`.
`qcom-armv8a` and `qcom-armv7a` are generic machines covering several boards.
`qcs6490-rb3gen2-core-kit` and `qrb2210-rb1-core-kit` are deprecated names
that require `rb3gen2-core-kit` and `rb1-core-kit`.

## Environment settings

The layer reads no environment variables at parse time. The build helpers in
`ci/` and kas read the settings listed in [.env.example](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/.env.example);
nothing loads that file automatically, so export the ones you need.

## Continuous integration

| Workflow | Trigger and check |
| --- | --- |
| [pr.yml](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/.github/workflows/pr.yml) | Pull requests to `master` that change more than Markdown: builds the `pr` profile of `build-yocto.yml`. |
| [push.yml](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/.github/workflows/push.yml) | Pushes to `master`: full build, LAVA tests, and published results. |
| [nightly-build.yml](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/.github/workflows/nightly-build.yml), [nightly-build-wrynose.yml](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/.github/workflows/nightly-build-wrynose.yml), [weekly-build.yml](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/.github/workflows/weekly-build.yml) | Schedules: nightly `master` and `wrynose` builds and tests that skip unchanged inputs, and the weekly superset. |
| [build-yocto.yml](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/.github/workflows/build-yocto.yml), [compile.yml](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/.github/workflows/compile.yml) | Called workflows: `kas lock`, patch review, `yocto-check-layer`, oe-selftest, and the machine, distro, and kernel build matrix. |
| [test.yml](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/.github/workflows/test.yml), [test-distro.yml](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/.github/workflows/test-distro.yml), [test-pr.yml](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/.github/workflows/test-pr.yml), [test-pr-wrynose.yml](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/.github/workflows/test-pr-wrynose.yml), [publish-results.yml](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/.github/workflows/publish-results.yml) | Boot and pre-merge tests in the LAVA lab after a build, and their published results. |
| [markdownlint.yml](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/.github/workflows/markdownlint.yml) | Changes to Markdown: lints `**/*.md` with `.github/.markdownlint.yaml`. |
| [documentation.yml](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/.github/workflows/documentation.yml) | Pull requests and pushes to `master`: runs the documentation `setup` and `check` targets. |
| [repolinter.yml](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/.github/workflows/repolinter.yml) | Pull requests and pushes to `master`: repository policy lint, including source licence headers. |
| [backport.yml](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/.github/workflows/backport.yml), [stales.yml](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/.github/workflows/stales.yml), [sstate-cleanup.yml](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/.github/workflows/sstate-cleanup.yml) | Maintenance: backport pull requests for merged changes labelled `backport wrynose`, stale issue handling, and shared-state cache expiry. |

The `.github/actions/` folder holds the composite actions these workflows use.
`.github/.markdownlint.yaml`, `.github/CODEOWNERS`, `.gitignore`, and
`docs/source/conf.py` explain their settings in comments beside them.
