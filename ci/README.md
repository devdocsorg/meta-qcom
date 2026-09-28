# CI build configuration

kas fragments that compose builds, as `ci/<machine>.yml` plus optional distro,
kernel, and feature fragments, and the helper scripts CI runs. The
[configuration reference](../docs/source/user/CONFIGURATION.md) explains their settings.

## Folders

- [test-keys/](test-keys/README.md) — Holds development keys for signing UEFI capsules.

## Files

- [README.md](README.md) — Indexes this folder.
- [base.lock.yml](base.lock.yml) — Pins every layer repository to a commit for reproducible builds.
- [base.yml](base.yml) — Defines the common kas base: nodistro, the core layers and their patches, and shared `local.conf` settings.
- [capsule-test-keys.yml](capsule-test-keys.yml) — Signs UEFI capsules with the development keys in `test-keys/`.
- [capsule.yml](capsule.yml) — Adds UEFI capsule generation to the flash package.
- [ccache.yml](ccache.yml) — Enables ccache for the compiler, toolchain, kernel, and large C++ recipes.
- [ci.yml](ci.yml) — Applies the CI mirror, cache, parallelism, and git fetch settings.
- [debug.yml](debug.yml) — Builds debug images with debug filesystems and an ftrace kernel command line.
- [dpdk.yml](dpdk.yml) — Adds the [meta-dpdk](https://git.yoctoproject.org/meta-dpdk) layer.
- [glymur-crd.yml](glymur-crd.yml) — Builds the `glymur-crd` machine.
- [iq-615-evk.yml](iq-615-evk.yml) — Builds the `iq-615-evk` machine.
- [iq-8275-evk.yml](iq-8275-evk.yml) — Builds the `iq-8275-evk` machine.
- [iq-9075-evk-open-fw-spl.yml](iq-9075-evk-open-fw-spl.yml) — Builds the `iq-9075-evk-open-fw-spl` machine.
- [iq-9075-evk-open-fw.yml](iq-9075-evk-open-fw.yml) — Builds the `iq-9075-evk-open-fw` machine.
- [iq-9075-evk.yml](iq-9075-evk.yml) — Builds the `iq-9075-evk` machine.
- [iq-x5121-evk.yml](iq-x5121-evk.yml) — Builds the `iq-x5121-evk` machine.
- [iq-x7181-evk.yml](iq-x7181-evk.yml) — Builds the `iq-x7181-evk` machine.
- [kaanapali-mtp.yml](kaanapali-mtp.yml) — Builds the `kaanapali-mtp` machine.
- [kas-container-shell-helper.sh](kas-container-shell-helper.sh) — Runs a CI helper script inside a kas-container shell.
- [kas-shell-helper.sh](kas-shell-helper.sh) — Runs a CI helper script inside a native kas shell.
- [kernel-fit-image.yml](kernel-fit-image.yml) — Switches the kernel to the U-Boot FIT image flow.
- [linux-qcom-6.18.yml](linux-qcom-6.18.yml) — Selects the linux-qcom 6.18 kernel.
- [linux-qcom-next-rt.yml](linux-qcom-next-rt.yml) — Selects the linux-qcom-next real-time kernel.
- [linux-qcom-next.yml](linux-qcom-next.yml) — Selects the linux-qcom-next kernel.
- [linux-qcom-rt-6.18.yml](linux-qcom-rt-6.18.yml) — Selects the linux-qcom 6.18 real-time kernel.
- [linux-yocto-dev.yml](linux-yocto-dev.yml) — Selects the linux-yocto-dev kernel.
- [meta-arm.yml](meta-arm.yml) — Adds the meta-arm and meta-arm-toolchain layers from [meta-arm](https://git.yoctoproject.org/meta-arm).
- [mirror-download-disable.yml](mirror-download-disable.yml) — Disables the Qualcomm Linux download mirrors for mirror checks.
- [mirror-download-test.yml](mirror-download-test.yml) — Fetches only from the Qualcomm Linux download mirrors for mirror checks.
- [mirror-tarballs.yml](mirror-tarballs.yml) — Generates mirror tarballs for fetched git repositories.
- [mirror.yml](mirror.yml) — Uses the Yocto Project shared-state mirror.
- [nospdx.yml](nospdx.yml) — Skips SPDX generation for images.
- [oe-selftest.sh](oe-selftest.sh) — Runs the layer's oe-selftest cases.
- [performance.yml](performance.yml) — Adds quiet, fast-boot kernel command-line options.
- [qcm6490-idp.yml](qcm6490-idp.yml) — Builds the `qcm6490-idp` machine.
- [qcom-armv7a.yml](qcom-armv7a.yml) — Builds the `qcom-armv7a` machine.
- [qcom-armv8a.yml](qcom-armv8a.yml) — Builds the `qcom-armv8a` machine.
- [qcom-distro-catchall.yml](qcom-distro-catchall.yml) — Selects the qcom-distro-catchall distro, which enables a superset of qcom-distro features.
- [qcom-distro-kvm.yml](qcom-distro-kvm.yml) — Adds the kvm machine feature to qcom-distro builds.
- [qcom-distro-multimedia-image.yml](qcom-distro-multimedia-image.yml) — Builds only qcom-multimedia-image with qcom-distro.
- [qcom-distro-selinux.yml](qcom-distro-selinux.yml) — Selects the qcom-distro-selinux distro.
- [qcom-distro-sota.yml](qcom-distro-sota.yml) — Selects the qcom-distro-sota distro.
- [qcom-distro.yml](qcom-distro.yml) — Selects qcom-distro and adds its layers and image targets.
- [qcs615-ride.yml](qcs615-ride.yml) — Builds the `qcs615-ride` machine.
- [qcs6490-rb3gen2-core-kit.yml](qcs6490-rb3gen2-core-kit.yml) — Links to `rb3gen2-core-kit.yml` for the deprecated machine name.
- [qcs8300-ride-sx.yml](qcs8300-ride-sx.yml) — Builds the `qcs8300-ride-sx` machine.
- [qcs9100-ride-sx.yml](qcs9100-ride-sx.yml) — Builds the `qcs9100-ride-sx` machine.
- [qrb2210-rb1-core-kit.yml](qrb2210-rb1-core-kit.yml) — Links to `rb1-core-kit.yml` for the deprecated machine name.
- [rb1-core-kit.yml](rb1-core-kit.yml) — Builds the `rb1-core-kit` machine.
- [rb3gen2-core-kit-open-fw.yml](rb3gen2-core-kit-open-fw.yml) — Builds the `rb3gen2-core-kit-open-fw` machine.
- [rb3gen2-core-kit.yml](rb3gen2-core-kit.yml) — Builds the `rb3gen2-core-kit` machine.
- [schemacheck.py](schemacheck.py) — Validates LAVA job YAML files against the LAVA schema.
- [sdx75-idp.yml](sdx75-idp.yml) — Builds the `sdx75-idp` machine.
- [shikra-evk.yml](shikra-evk.yml) — Builds the `shikra-evk` machine.
- [sm8750-mtp.yml](sm8750-mtp.yml) — Builds the `sm8750-mtp` machine.
- [test-oe-nogl.yml](test-oe-nogl.yml) — Builds with [meta-oe](https://github.com/openembedded/meta-openembedded) and without OpenGL.
- [u-boot-qcom.yml](u-boot-qcom.yml) — Selects u-boot-qcom as the boot loader.
- [world.yml](world.yml) — Builds `world` for this layer's recipes.
- [yocto-buildstats.sh](yocto-buildstats.sh) — Charts and summarises the latest build statistics.
- [yocto-check-layer.sh](yocto-check-layer.sh) — Runs yocto-check-layer for every machine in the layer.
- [yocto-patchreview.sh](yocto-patchreview.sh) — Checks the layer's patches for sign-off and Upstream-Status tags.
