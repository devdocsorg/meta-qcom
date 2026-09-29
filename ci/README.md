# ci

Configuration fragments for [kas](https://github.com/siemens/kas) and helper scripts that the layer's CI uses to build and check meta-qcom. kas merges the chosen fragments into the `local.conf` and `bblayers.conf` that BitBake reads, for example `kas build ci/base.yml:ci/<machine>.yml:ci/capsule.yml`.

## Folders

- [test-keys/](test-keys/README.md) — Test certificates and keys for signing UEFI capsules in CI builds.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [base.lock.yml](base.lock.yml) — Pins the commit of every layer repository that the CI fragments fetch, so builds are reproducible.
- [base.yml](base.yml) — Base fragment for every build: fetches [openembedded-core](https://github.com/openembedded/openembedded-core) with the patches from `patches/oe-core/` and [bitbake](https://github.com/openembedded/bitbake), sets the shared `local.conf` settings, and builds `core-image-base`.
- [capsule-test-keys.yml](capsule-test-keys.yml) — Points the UEFI capsule signing variables at the files in `test-keys/`, for CI and development builds only.
- [capsule.yml](capsule.yml) — Enables UEFI FMP capsule generation by selecting `firmware-qcom-capsule` as the capsule firmware provider.
- [ccache.yml](ccache.yml) — Enables ccache with a 200 GB cache under `SSTATE_DIR`, only for large recipes such as the compilers, the kernels, OpenCV, and Rust.
- [ci.yml](ci.yml) — CI runner settings: includes `mirror.yml` and `ccache.yml`, limits compile parallelism to fit the runners' memory, keeps git clones job-local, and fetches the qcom kernels shallow.
- [debug.yml](debug.yml) — Enables `DEBUG_BUILD`, a debug filesystem tarball, and ftrace options on the kernel command line.
- [dpdk.yml](dpdk.yml) — Adds the [meta-dpdk](https://git.yoctoproject.org/meta-dpdk) layer.
- [glymur-crd.yml](glymur-crd.yml) — Builds for the `glymur-crd` machine on top of `base.yml`.
- [iq-615-evk.yml](iq-615-evk.yml) — Builds for the `iq-615-evk` machine on top of `base.yml`.
- [iq-8275-evk.yml](iq-8275-evk.yml) — Builds for the `iq-8275-evk` machine on top of `base.yml`.
- [iq-9075-evk-open-fw-spl.yml](iq-9075-evk-open-fw-spl.yml) — Builds for the `iq-9075-evk-open-fw-spl` machine on top of `base.yml` and `meta-arm.yml`.
- [iq-9075-evk-open-fw.yml](iq-9075-evk-open-fw.yml) — Builds for the `iq-9075-evk-open-fw` machine on top of `base.yml` and `meta-arm.yml`.
- [iq-9075-evk.yml](iq-9075-evk.yml) — Builds for the `iq-9075-evk` machine on top of `base.yml`.
- [iq-x5121-evk.yml](iq-x5121-evk.yml) — Builds for the `iq-x5121-evk` machine on top of `base.yml`.
- [iq-x7181-evk.yml](iq-x7181-evk.yml) — Builds for the `iq-x7181-evk` machine on top of `base.yml`.
- [kaanapali-mtp.yml](kaanapali-mtp.yml) — Builds for the `kaanapali-mtp` machine on top of `base.yml`.
- [kas-container-shell-helper.sh](kas-container-shell-helper.sh) — Runs a given script inside a `kas-container` shell for `base.yml` (or `KAS_YAMLS`), passing it the repository and work directories.
- [kas-shell-helper.sh](kas-shell-helper.sh) — Runs a given script in a local `kas shell` for `base.yml`, with the kas work directory outside the checkout.
- [kernel-fit-image.yml](kernel-fit-image.yml) — Switches to the U-Boot FIT kernel flow: drops the Android boot image class, enables `kernel-fit-extra-artifacts`, and uses `esp-qcom-fit-image` as the ESP image.
- [linux-qcom-6.18.yml](linux-qcom-6.18.yml) — Selects the `linux-qcom` 6.18 kernel.
- [linux-qcom-next-rt.yml](linux-qcom-next-rt.yml) — Selects the `linux-qcom-next-rt` real-time kernel.
- [linux-qcom-next.yml](linux-qcom-next.yml) — Selects the `linux-qcom-next` kernel.
- [linux-qcom-rt-6.18.yml](linux-qcom-rt-6.18.yml) — Selects the `linux-qcom-rt` 6.18 real-time kernel.
- [linux-yocto-dev.yml](linux-yocto-dev.yml) — Selects the `linux-yocto-dev` kernel and skips its `version-going-backwards` QA check.
- [meta-arm.yml](meta-arm.yml) — Adds the `meta-arm` and `meta-arm-toolchain` layers from [meta-arm](https://git.yoctoproject.org/meta-arm).
- [mirror-download-disable.yml](mirror-download-disable.yml) — Removes the `qli-mirrors` class so that a fetch into a clean `DL_DIR` uses only the original sources.
- [mirror-download-test.yml](mirror-download-test.yml) — Fetches only from the Qualcomm Linux download mirror (`QLI_MIRRORS`), to check that the mirror has every source.
- [mirror-tarballs.yml](mirror-tarballs.yml) — Sets `BB_GENERATE_MIRROR_TARBALLS` so that git sources are also saved as mirror tarballs.
- [mirror.yml](mirror.yml) — Uses the public Yocto Project sstate mirror.
- [nospdx.yml](nospdx.yml) — Turns off SPDX 3.0 SBOM generation for images.
- [oe-selftest.sh](oe-selftest.sh) — Runs oe-selftest for the modules in `lib/oeqa/selftest/cases/` (or the ones named), with `rb3gen2-core-kit` as the default machine.
- [performance.yml](performance.yml) — Adds kernel command-line options for a quiet boot with less initramfs work.
- [qcm6490-idp.yml](qcm6490-idp.yml) — Builds for the `qcm6490-idp` machine on top of `base.yml`.
- [qcom-armv7a.yml](qcom-armv7a.yml) — Builds for the generic 32-bit `qcom-armv7a` machine on top of `base.yml`.
- [qcom-armv8a.yml](qcom-armv8a.yml) — Builds for the generic 64-bit `qcom-armv8a` machine on top of `base.yml`, with `devicetree-dummy` as the devicetree provider.
- [qcom-distro-catchall.yml](qcom-distro-catchall.yml) — Builds the multimedia, proprietary multimedia, and container orchestration images with the `qcom-distro-catchall` distro.
- [qcom-distro-kvm.yml](qcom-distro-kvm.yml) — Builds the `qcom-distro` images with the `kvm` machine feature.
- [qcom-distro-multimedia-image.yml](qcom-distro-multimedia-image.yml) — Builds only `qcom-multimedia-image` with `qcom-distro`.
- [qcom-distro-selinux.yml](qcom-distro-selinux.yml) — Builds the multimedia and proprietary multimedia images with the `qcom-distro-selinux` distro.
- [qcom-distro-sota.yml](qcom-distro-sota.yml) — Builds the `qcom-distro` images with the `qcom-distro-sota` distro.
- [qcom-distro.yml](qcom-distro.yml) — Adds [meta-qcom-distro](https://github.com/qualcomm-linux/meta-qcom-distro) and the layers it uses ([meta-openembedded](https://github.com/openembedded/meta-openembedded), [meta-ai](https://github.com/qualcomm-linux/meta-ai), [meta-virtualization](https://git.yoctoproject.org/meta-virtualization), [meta-audioreach](https://github.com/AudioReach/meta-audioreach), [meta-selinux](https://git.yoctoproject.org/meta-selinux) with the patches from `patches/selinux/`, [meta-updater](https://github.com/uptane/meta-updater), and [meta-security](https://git.yoctoproject.org/meta-security)), then builds the `qcom-distro` images.
- [qcs615-ride.yml](qcs615-ride.yml) — Builds for the `qcs615-ride` machine on top of `base.yml`.
- [qcs6490-rb3gen2-core-kit.yml](qcs6490-rb3gen2-core-kit.yml) — Symlink to `rb3gen2-core-kit.yml`, kept for the deprecated machine name.
- [qcs8300-ride-sx.yml](qcs8300-ride-sx.yml) — Builds for the `qcs8300-ride-sx` machine on top of `base.yml`.
- [qcs9100-ride-sx.yml](qcs9100-ride-sx.yml) — Builds for the `qcs9100-ride-sx` machine on top of `base.yml`.
- [qrb2210-rb1-core-kit.yml](qrb2210-rb1-core-kit.yml) — Symlink to `rb1-core-kit.yml`, kept for the deprecated machine name.
- [rb1-core-kit.yml](rb1-core-kit.yml) — Builds for the `rb1-core-kit` machine on top of `base.yml`.
- [rb3gen2-core-kit-open-fw.yml](rb3gen2-core-kit-open-fw.yml) — Builds for the `rb3gen2-core-kit-open-fw` machine on top of `base.yml` and `meta-arm.yml`.
- [rb3gen2-core-kit.yml](rb3gen2-core-kit.yml) — Builds for the `rb3gen2-core-kit` machine on top of `base.yml`.
- [schemacheck.py](schemacheck.py) — Validates every `.yaml` file under a given directory against the LAVA job schema.
- [sdx75-idp.yml](sdx75-idp.yml) — Builds `core-image-minimal` for the `sdx75-idp` machine on top of `base.yml`.
- [shikra-evk.yml](shikra-evk.yml) — Builds for the `shikra-evk` machine on top of `base.yml`.
- [sm8750-mtp.yml](sm8750-mtp.yml) — Builds for the `sm8750-mtp` machine on top of `base.yml`.
- [test-oe-nogl.yml](test-oe-nogl.yml) — Adds the `meta-oe` layer and removes `opengl` from `DISTRO_FEATURES`, to test the layer without OpenGL.
- [u-boot-qcom.yml](u-boot-qcom.yml) — Selects `u-boot-qcom` as the bootloader.
- [world.yml](world.yml) — Builds `world`, limited to the recipes in this layer.
- [yocto-buildstats.sh](yocto-buildstats.sh) — Draws the latest build statistics as SVG charts with pybootchartgui.
- [yocto-check-layer.sh](yocto-check-layer.sh) — Runs yocto-check-layer on a fresh clone of the layer for every machine in `conf/machine/`.
- [yocto-patchreview.sh](yocto-patchreview.sh) — Runs the OpenEmbedded patch review script and fails if any patch has a malformed Signed-off-by or Upstream-Status tag.
