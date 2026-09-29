# Configuration

meta-qcom is configured through kas files, the layer's BitBake configuration,
variables that its classes and machine includes read, and a few environment
variables for the helper scripts.

## How settings combine

`kas-container build` takes kas files joined with `:`, such as
`ci/rb3gen2-core-kit.yml:ci/qcom-distro.yml:ci/linux-qcom-6.18.yml`. Each file
adds to or overrides the files before it, and `header.includes` pulls in other
files first, as the
[kas project configuration](https://kas.readthedocs.io/en/latest/userguide/project-configuration.html)
describes. kas writes every `local_conf_header` entry into `conf/local.conf`,
so those lines follow
[BitBake's assignment rules](https://docs.yoctoproject.org/bitbake/bitbake-user-manual/bitbake-user-manual-metadata.html):
`?=` and `??=` set defaults that a plain `=` elsewhere replaces, and
`:append`, `:remove`, and `+=` adjust a value. Standard variables are defined
in the [Yocto Project variable glossary](https://docs.yoctoproject.org/ref-manual/variables.html);
the tables below explain this layer's choices.

The helper scripts read the environment variables listed with safe examples
in [.env.example](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/.env.example).
Nothing loads that file automatically; export the values in your shell.

## kas files

Every file below is in [ci/](https://github.com/devdocsorg/meta-qcom/tree/docs/layer-documentation/ci).
Files that set only a machine share one row.

| File | Setting | Purpose | Type and default | Safe example |
| --- | --- | --- | --- | --- |
| `<machine>.yml` | `header.includes`, `machine` | Build one board: include `base.yml` (the `-open-fw` variants also include `meta-arm.yml`) and name a [machine configuration](https://github.com/devdocsorg/meta-qcom/tree/docs/layer-documentation/conf/machine). `qcs6490-rb3gen2-core-kit.yml` and `qrb2210-rb1-core-kit.yml` are links to `rb3gen2-core-kit.yml` and `rb1-core-kit.yml`. | Machine name; `base.yml` sets `unset` | `machine: rb3gen2-core-kit` |
| `sdx75-idp.yml` | `target` | Build the smaller `core-image-minimal` for this modem board. | Image list; `base.yml` builds `core-image-base` | `target: [core-image-minimal]` |
| `qcom-armv8a.yml` | `PREFERRED_PROVIDER_virtual/dtb`, `QCOM_BOOTIMG_DEVICETREE` | Build the generic machine with the dummy device tree from `devicetree-dummy`. | Recipe name; DTB file name | `QCOM_BOOTIMG_DEVICETREE = "qcom-armv8-dummy.dtb"` |
| `base.yml` | `header.version`, `distro`, `defaults.repos.branch`, `machine`, `target` | Common base: kas format 14, no distribution policy, `master` branches, no machine, and `core-image-base`. | kas fields | `distro: nodistro` |
| `base.yml` | `repos` | Use this layer, [openembedded-core](https://github.com/openembedded/openembedded-core) (layer `meta`), and [bitbake](https://github.com/openembedded/bitbake), applying the three [oe-core patches](https://github.com/devdocsorg/meta-qcom/tree/docs/layer-documentation/patches/oe-core). | Repository map | `oe-core: {url: https://github.com/openembedded/openembedded-core}` |
| `base.yml` | `CONF_VERSION`, `INHERIT` (`buildstats-summary`, `buildhistory`, `rm_work`, `image-buildinfo`) | Record build statistics, history, and image build information, and delete work files after each recipe. | Integer; class names | `INHERIT += "rm_work"` |
| `base.yml` | `BB_DISKMON_DIRS` | Stop tasks when build, download, cache, or `/tmp` space runs low, and halt when it is nearly exhausted. | Weak default of action, folder, space, and inodes entries | `STOPTASKS,${TMPDIR},1G,100K` |
| `base.yml` | `MIRRORS:append` | Fall back to the CodeLinaro Yocto mirrors for Git and HTTPS downloads. | Pattern and URL pairs | `git://github.com git://git.codelinaro.org/clo/yocto-mirrors/github/` |
| `base.yml` | `KERNEL_CMDLINE_EXTRA:append` | Enable Qualcomm download mode after a crash (`qcom_scm.download_mode=1`). | Kernel arguments | `" qcom_scm.download_mode=1"` |
| `base.yml` | `DISTRO_FEATURES:append`, `EXTRA_IMAGE_FEATURES`, `IMAGE_ROOTFS_EXTRA_SPACE`, `WATCHDOG_RUNTIME_SEC:pn-systemd` | Add EFI, PAM, and predictable interface names; allow a password-less root login for development; add 300 MiB of free space; set the systemd watchdog to 30 seconds. | Feature lists; KiB; seconds | `IMAGE_ROOTFS_EXTRA_SPACE = "307200"` |
| `base.yml` | `OS_RELEASE_FIELDS:append`, `BUILD_ID` | Record a build identifier in `/etc/os-release`; CI replaces the local default through the generated `ci/build-id.yml`. | Weak string default `local-${DATETIME}` | `BUILD_ID = "12345"` |
| `base.lock.yml` | `overrides.repos.<name>.commit` | Pin the eleven repositories used by the CI files to exact commits. | Commit SHA per repository | `bitbake: {commit: 6f5ecebb...}` |
| `ci.yml` | `header.includes`, `BB_SIGNATURE_HANDLER`, `FIRMWARE_COMPRESSION:qcom-armv8a`, `PACKAGE_CLASSES` | CI settings: include `mirror.yml` and `ccache.yml`, use basic task hashes, compress firmware with zstd, and package RPMs (a workaround for [bug 16010](https://bugzilla.yoctoproject.org/show_bug.cgi?id=16010)). | kas list; strings | `PACKAGE_CLASSES = "package_rpm"` |
| `ci.yml` | `BB_PRESSURE_MAX_MEMORY`, `PARALLEL_MAKE`, `do_compile[number_threads]` | Hold back new tasks under memory pressure and compile at most 8 recipes at once with 4 make jobs each, so CI builds fit in memory. | Integer; make option; integer | `PARALLEL_MAKE = "-j 4"` |
| `ci.yml` | `GITDIR`, `BB_GENERATE_MIRROR_TARBALLS`, `BB_GIT_SHALLOW:pn-<kernel>` | Keep Git clones job-local, share them as mirror tarballs, and fetch the four `linux-qcom` kernels shallow. | Folder; `"0"` or `"1"` | `BB_GIT_SHALLOW:pn-linux-qcom = "1"` |
| `ccache.yml` | `INHERIT`, `CCACHE_MAXSIZE`, `CCACHE_TOP_DIR`, `HOSTTOOLS`, `ASSUME_PROVIDED` | Use the host's ccache, with up to 200 GB kept under the shared state folder. | Class; size; folder; tool names | `CCACHE_MAXSIZE = "200G"` |
| `ccache.yml` | `CCACHE_DISABLE`, `CCACHE_DISABLE:pn-<recipe>` | Disable ccache except for the compilers, C library, kernels, `chromium-ozone-wayland`, `opencv`, and `rust`, which benefit from it. | `"0"` or `"1"` | `CCACHE_DISABLE:pn-glibc = "0"` |
| `capsule.yml` | `PREFERRED_PROVIDER_virtual/qcom-capsule-firmware`, `VIRTUAL-RUNTIME_qcom-capsule-firmware` | Build the UEFI capsule, install it in the image, and add it to the qcomflash package. | Recipe name; unset by default | `"firmware-qcom-capsule"` |
| `capsule-test-keys.yml` | `CAPSULE_ROOT_CER`, `CAPSULE_CERT_PEM`, `CAPSULE_ROOT_PUB`, `CAPSULE_SUB_PUB` | Sign the capsule with the development keys in [ci/test-keys](https://github.com/devdocsorg/meta-qcom/tree/docs/layer-documentation/ci/test-keys); never use them for products. | File paths; empty by default | `${LAYERDIR_qcom}/ci/test-keys/QcFMPRoot.cer` |
| `debug.yml` | `DEBUG_BUILD`, `IMAGE_GEN_DEBUGFS`, `IMAGE_FSTYPES_DEBUGFS`, `KERNEL_CMDLINE_EXTRA_FTRACE`, `KERNEL_CMDLINE_EXTRA:append` | Build with debugging compiler flags, produce a debug file system tarball, and start the kernel with timer, IRQ, workqueue, scheduler, power, regulator, thermal, and RPMh tracing. | `"1"`; image type; kernel arguments | `IMAGE_FSTYPES_DEBUGFS = "tar.zst"` |
| `dpdk.yml` | `repos.meta-dpdk` | Add the [meta-dpdk](https://git.yoctoproject.org/meta-dpdk) layer from its `master` branch. | Repository | `url: https://git.yoctoproject.org/meta-dpdk` |
| `kernel-fit-image.yml` | `KERNEL_CLASSES`, `QCOM_ESP_IMAGE`, `EFI_PROVIDER` | Boot a U-Boot FIT image from `esp-qcom-fit-image` instead of an Android boot image and systemd-boot. | Class list; image recipe; empty string | `QCOM_ESP_IMAGE = "esp-qcom-fit-image"` |
| `linux-qcom-6.18.yml`, `linux-qcom-rt-6.18.yml`, `linux-qcom-next.yml`, `linux-qcom-next-rt.yml`, `linux-yocto-dev.yml` | `PREFERRED_PROVIDER_virtual/kernel`, `PREFERRED_VERSION_virtual/kernel`, `ERROR_QA:remove:pn-linux-yocto-dev` | Select the kernel; the 6.18 files pin `6.18%`, and `linux-yocto-dev` allows its version to go backwards. Otherwise machines that include `qcom-base.inc` use `linux-qcom-next` and the generic machines use `linux-yocto`. | Recipe name; version pattern | `PREFERRED_PROVIDER_virtual/kernel = "linux-qcom-next"` |
| `meta-arm.yml` | `repos.meta-arm` | Add the `meta-arm` and `meta-arm-toolchain` layers of [meta-arm](https://git.yoctoproject.org/meta-arm) for the open firmware machines. | Repository | `branch: master` |
| `mirror.yml` | `SSTATE_MIRRORS` | Reuse the Yocto Project's public shared state cache. | Mirror pairs | `file://.* http://sstate.yoctoproject.org/all/PATH;downloadfilename=PATH` |
| `mirror-tarballs.yml` | `BB_GENERATE_MIRROR_TARBALLS` | Write mirror tarballs for Git sources. | `"0"` or `"1"` | `"1"` |
| `mirror-download-test.yml`, `mirror-download-disable.yml` | `BB_FETCH_PREMIRRORONLY`, `PREMIRRORS`, `INHERIT:remove` | With a clean download folder and `bitbake --runall fetch world`, check that the Qualcomm Linux mirror holds every source, or fetch without it. | `"1"`; mirror pairs; class name | `INHERIT:remove = "qli-mirrors"` |
| `nospdx.yml` | `IMAGE_CLASSES:remove` | Skip SPDX 3.0 image documents. | Class name | `"create-spdx-image-3.0"` |
| `performance.yml` | `KERNEL_CMDLINE_EXTRA:append` | Boot quietly, with a dumb console terminal, udev triggered only for the root device, and no efivarfs mount in the initramfs. | Kernel arguments | `" quiet"` |
| `qcom-distro.yml` | `distro`, `defaults.repos.branch`, `repos`, `SKIP_META_VIRT_SANITY_CHECK`, `target` | Build the [Qualcomm Linux distribution](https://github.com/qualcomm-linux/meta-qcom-distro) with [meta-ai](https://github.com/qualcomm-linux/meta-ai), [meta-openembedded](https://github.com/openembedded/meta-openembedded), [meta-virtualization](https://git.yoctoproject.org/meta-virtualization), [meta-audioreach](https://github.com/AudioReach/meta-audioreach), [meta-selinux](https://git.yoctoproject.org/meta-selinux) with three [patches](https://github.com/devdocsorg/meta-qcom/tree/docs/layer-documentation/patches/selinux), [meta-updater](https://github.com/uptane/meta-updater), and [meta-security](https://git.yoctoproject.org/meta-security), and its four images. | kas fields | `distro: qcom-distro` |
| `qcom-distro-catchall.yml`, `qcom-distro-selinux.yml`, `qcom-distro-sota.yml` | `distro`, `target` | Build the distribution's catch-all, SELinux, or software-update variant. | Distribution name; image list | `distro: qcom-distro-selinux` |
| `qcom-distro-kvm.yml` | `MACHINE_FEATURES:append` | Add the `kvm` machine feature, which selects the KVM XBL configuration and UEFI device trees. | Feature list | `" kvm"` |
| `qcom-distro-multimedia-image.yml` | `target` | Build only `qcom-multimedia-image`. | Image list | `target: [qcom-multimedia-image]` |
| `test-oe-nogl.yml` | `repos.meta-openembedded`, `DISTRO_FEATURES:remove` | Build with the `meta-oe` layer of [meta-openembedded](https://github.com/openembedded/meta-openembedded) and without OpenGL. | Layer list; feature | `DISTRO_FEATURES:remove = "opengl"` |
| `u-boot-qcom.yml` | `PREFERRED_PROVIDER_virtual/bootloader` | Build U-Boot from `u-boot-qcom`. | Recipe name | `"u-boot-qcom"` |
| `world.yml` | `EXCLUDE_FROM_WORLD`, `EXCLUDE_FROM_WORLD:layer-qcom`, `target` | Build every recipe of this layer (`bitbake world`); a commented line would add the recipes of [meta-qcom-distro](https://github.com/qualcomm-linux/meta-qcom-distro). | `"0"` or `"1"` | `EXCLUDE_FROM_WORLD:layer-qcom = "0"` |

## Layer configuration

[conf/layer.conf](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/conf/layer.conf)
registers the layer with the standard `BBPATH`, `BBFILES`, `BBFILE_COLLECTIONS`,
`BBFILE_PATTERN_qcom`, `BBFILE_PRIORITY_qcom` (6), `LAYERDEPENDS_qcom` (core),
`LAYERRECOMMENDS_qcom` (openembedded-layer and meta-arm), `LAYERSERIES_COMPAT_qcom`
(wrynose), and `LICENSE_PATH` settings. Its local choices:

| Setting | Purpose | Type and default | Safe example |
| --- | --- | --- | --- |
| `LAYERDIR_qcom` | Layer root, so files such as the CI test keys can be referenced from any build folder. | Folder | `${LAYERDIR_qcom}/ci/test-keys` |
| `BBFILES_DYNAMIC` | Add the recipes under [dynamic-layers](https://github.com/devdocsorg/meta-qcom/tree/docs/layer-documentation/dynamic-layers) only when their layer collection is present. | Collection and pattern pairs | `ai:${LAYERDIR}/dynamic-layers/ai/*/*/*.bb` |
| `QLI_BASELINE` | Qualcomm Linux baseline folder on the download mirror. | String; `main` | `QLI_BASELINE = "main"` |
| `INHERIT += "qli-mirrors"` | Fall back to the Qualcomm Linux download mirror. | Class name | `INHERIT:remove = "qli-mirrors"` |
| `PREFERRED_RPROVIDER_virtual-diag-router` | Choose `diag` when both diag routers are available. | Weak recipe name default `diag` | `"diag-router"` |
| `addpylib` | Make [lib/qcom](https://github.com/devdocsorg/meta-qcom/tree/docs/layer-documentation/lib/qcom) importable as `qcom`. | Folder and namespace | `addpylib ${LAYERDIR}/lib qcom` |
| `SIGGEN_EXCLUDE_SAFE_RECIPE_DEPS` | Keep the kernel graphics module out of the Adreno task signatures, as it is a runtime-only dependency. | Dependency pairs | `qcom-adreno->kgsl-dlkm` |

## Layer variables

Machines, images, and `local.conf` can set these variables. Machine files set
the board-specific values; the
[machine includes](https://github.com/devdocsorg/meta-qcom/tree/docs/layer-documentation/conf/machine/include)
explain them beside each setting.

| Variable | Read by | Purpose | Type and default | Safe example |
| --- | --- | --- | --- | --- |
| `QCOM_BOOT_FIRMWARE`, `QCOM_CDT_FIRMWARE`, `QCOM_PARTITION_CONF` | `image_types_qcom` | Recipes that deploy the boot firmware, CDT, and partition tables for the qcomflash package. | Recipe name; empty, empty, `qcom-partition-conf` | `"firmware-qcom-boot-qcs6490"` |
| `QCOM_BOOT_FILES_SUBDIR`, `QCOM_PARTITION_FILES_SUBDIR`, `QCOM_PARTITION_FILES_SUBDIR_SPINOR` | `image_types_qcom` | Deploy folders holding the board's boot firmware and partition files. | Folder; empty, the boot folder, empty | `"qcm6490"` |
| `QCOM_CDT_FILE`, `QCOM_XBL_CONFIG`, `QCOM_UEFI_DTB` | `image_types_qcom` | CDT name and XBL configuration and UEFI device tree files to package; the last two select KVM variants when `kvm` is a machine feature. | File name; unset, `xbl_config.elf`, `uefi_dtbs.xz` | `"cdt_ride_sx"` |
| `QCOM_ESP_IMAGE`, `QCOM_ESP_FILE`, `QCOM_DTB_FILE`, `IMAGE_QCOMFLASH_FS_TYPE` | `image_types_qcom` | ESP image recipe and file, DTB image name, and root file system type in the package. | `esp-qcom-image` with the `efi` machine feature; derived path; `dtb.bin`; `ext4` | `QCOM_DTB_FILE = "dtb.bin"` |
| `QCOM_CAPSULE_FIRMWARE` | `image_types_qcom` | Capsule recipe added to the package. | Recipe name; the capsule provider | `"firmware-qcom-capsule"` |
| `QCOM_UBOOT_SPL_FIT`, `QCOM_UBOOT_SPL_IMAGE`, `QCOM_UBOOT_FIT_IMAGE` | `image_types_qcom`, `u-boot-qcom` | Package the signed SPL and U-Boot FIT instead of `uefi.elf`; set by `qcom-uboot-spl-fit.inc`. | `"0"` or `"1"`; file names | `QCOM_UBOOT_SPL_FIT = "1"` |
| `QCOM_UBOOT_SPL_FIT_ATF`, `QCOM_UBOOT_SPL_FIT_TEE`, `QCOM_UBOOT_SPL_ENTRY`, `QCOM_UBOOT_SPL_SWIV_PLATFORM` | `u-boot-qcom`, SoC includes | Firmware recipes, load address, and SWIV platform for the SPL FIT flow. | Recipe names; address; platform | `"trusted-firmware-a-qcom-lemans-evk"` |
| `BOARD_MBN_HEADER[<config>]` | `u-boot-qcom` | MBN header version used to sign U-Boot for each `UBOOT_CONFIG`. | `v5` or `v6` | `BOARD_MBN_HEADER[qcs6490-rb3gen2] = "v6"` |
| `QCOM_BOOTIMG_ROOTFS`, `SD_QCOM_BOOTIMG_ROOTFS`, `QCOM_BOOTIMG_PAGE_SIZE`, `QCOM_BOOTIMG_KERNEL_BASE`, `QCOM_BOOTIMG_DEVICETREE` | `linux-qcom-bootimg` | Root device, SD card root device, page size, kernel base, and external device trees for Android boot images; per-DTB flags override them. | `PARTLABEL=rootfs`; unset; `4096`; `0x80000000`; unset | `QCOM_BOOTIMG_ROOTFS[sm8450-hdk] = "PARTLABEL=userdata"` |
| `INITRAMFS_IMAGE` | `linux-qcom-bootimg` | Also build boot images that carry this initramfs. | Image recipe; empty | `"initramfs-kerneltest-image"` |
| `QCOM_DTB_DEFAULT`, `QCOM_VFAT_SECTOR_SIZE`, `DTBBIN_SIZE` | `linux-qcom-dtbbin` | Default DTB image (`multi-dtb` adds the FIT image), vfat sector size, and DTB image size. | Name; `4096` bytes; `4096` KiB | `QCOM_VFAT_SECTOR_SIZE = "512"` |
| `FIT_DTB_COMPATIBLE[<compatible>]`, `LINUX_QCOM_FIT_DTB_COMPATIBLE`, `FIT_DTB_MKIMAGE_EXTRA_OPTS`, `MKIMAGE` | `dtb-fit-image` | Device trees and overlays for each compatible string (commas written as underscores), the include that lists them, mkimage options, and mkimage path. | DTB names; include path; options; path | `FIT_DTB_COMPATIBLE[qcom_qcs6490-iot] = "qcs6490-rb3gen2"` |
| `LINUX_QCOM_KERNEL_DEVICETREE` | `linux-qcom` kernels | Device trees that only the `linux-qcom` kernels build. | DTB list; empty | `"qcom/talos-evk-camx.dtbo"` |
| `QCOM_RT_CPU`, `QCOM_IRQAFF`, `QCOM_RCU_NOCBS`, `QCOM_RCU_EXPEDITED`, `QCOM_CPUIDLE_OFF` | `qcom-common.inc` | Isolated CPUs, IRQ affinity, RCU callback offload, expedited RCU, and disabled CPU idle for the real-time kernels. | CPU lists or `"1"`; empty | `QCOM_RT_CPU = "7"` |
| `ESPFOLDER` | `uki-esp-image` | Folder in the ESP that holds `EFI/Linux`. | Path; `/EFI` (`esp-qcom-image` uses the root) | `ESPFOLDER = ""` |
| `QLI_MIRRORS_URI`, `QLI_MIRRORS` | `qli-mirrors` | Qualcomm Linux mirror location and the fetch patterns that fall back to it. | URL; mirror pairs | `https://artifacts.codelinaro.org/artifactory/qli-ci/downloads/main` |
| `CAPSULE_*`, `XBLCONFIG_DTB`, `XBLCONFIG_DTB_SECTION`, `BOOTBINS_DIR` | `qcom-capsule` | Capsule version, GUID, keys, flash layout, and XBL configuration patching, documented beside each setting in the [class](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/classes-recipe/qcom-capsule.bbclass). | See the class | `CAPSULE_FLASH_TYPE = "UFS"` |
| `QCOM_FIT_BOOT_CONF` | `u-boot-scr-qcom-fit` | FIT configuration that boot.scr boots. | `#conf-...` string; empty | `"#conf-lemans-evk.dtb#conf-lemans-el2.dtbo"` |
| `POLICY_BOOLEANS` | `refpolicy-targeted` | SELinux booleans and tunables to set, as `name=value` pairs. | List; empty | `"tee_supplicant_qtee=true"` |
| `PACKAGE_INSTALL_<layer>` | `initramfs-tiny-image` | Packages added only when that layer collection is present. | Package list | `PACKAGE_INSTALL_openembedded-layer = "htop"` |

## Repository settings

| File | Settings |
| --- | --- |
| [.gitignore](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/.gitignore) | Ignores Python caches, the CI-generated `ci/build-id.yml`, a local `kas-container` copy, `.env` files except `.env.example`, and the documentation environment and intermediates. |
| [.github/CODEOWNERS](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/.github/CODEOWNERS) | Assigns the layer maintainers to all paths and the CI maintainers to `ci/`. |
| [.github/.markdownlint.yaml](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/.github/.markdownlint.yaml) | Turns off the line-length and inline HTML rules, allows repeated headings in different sections, and requires a first-line heading. |
| [issue templates](https://github.com/devdocsorg/meta-qcom/tree/docs/layer-documentation/.github/ISSUE_TEMPLATE) | Each template's front matter names it (`name`) and says when to use it (`about`); both are required strings. |

## Continuous integration

| Workflow | Trigger | What it does |
| --- | --- | --- |
| [pr.yml](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/.github/workflows/pr.yml) | Pull requests to `master` that change more than Markdown | Runs `build-yocto.yml` with the `pr` profile and records which workflow run belongs to the pull request. |
| [push.yml](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/.github/workflows/push.yml), [nightly-build.yml](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/.github/workflows/nightly-build.yml), [weekly-build.yml](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/.github/workflows/weekly-build.yml) | Pushes to `master`; nightly except Saturday; Saturday | Build, test on LAVA boards, and publish results; the weekly profile adds the costly builds. |
| [nightly-build-wrynose.yml](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/.github/workflows/nightly-build-wrynose.yml) | Daily | Starts the nightly build on `wrynose`. |
| [build-yocto.yml](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/.github/workflows/build-yocto.yml), [compile.yml](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/.github/workflows/compile.yml) | Called by the build workflows | Lock the kas files, run `yocto-patchreview`, `yocto-check-layer`, and `oe-selftest`, and build each machine, distribution, and kernel combination. |
| [test.yml](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/.github/workflows/test.yml), [test-distro.yml](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/.github/workflows/test-distro.yml), [test-pr.yml](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/.github/workflows/test-pr.yml), [test-pr-wrynose.yml](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/.github/workflows/test-pr-wrynose.yml), [publish-results.yml](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/.github/workflows/publish-results.yml) | After builds, and after "Build on PR" completes | Submit LAVA test jobs with the [actions](https://github.com/devdocsorg/meta-qcom/tree/docs/layer-documentation/.github/actions), comment on pull requests, and publish the "Test Results" check. |
| [markdownlint.yml](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/.github/workflows/markdownlint.yml), [repolinter.yml](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/.github/workflows/repolinter.yml), [documentation.yml](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/.github/workflows/documentation.yml) | Pull requests and pushes to `master` | Lint Markdown, check the organisation's repository rules, and rebuild and check this documentation. |
| [backport.yml](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/.github/workflows/backport.yml) | Merged pull requests to `master` labelled `backport wrynose` | Opens the backport pull request. |
| [stales.yml](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/.github/workflows/stales.yml), [sstate-cleanup.yml](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/.github/workflows/sstate-cleanup.yml) | Daily; weekly | Mark inactive issues and pull requests stale; expire unused shared state files. |
