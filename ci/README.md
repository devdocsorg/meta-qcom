# ci

kas files and helper scripts that CI uses and that local builds reuse; the [configuration guide](../docs/source/user/CONFIGURATION.md) explains every setting.

## Folders

- [test-keys/](test-keys/README.md) — Development-only keys for signing UEFI capsules in CI.

## Files

- [base.lock.yml](base.lock.yml) — Pins the repositories used by the kas files to exact commits.
- [base.yml](base.yml) — Defines the common build: repositories, oe-core patches, local.conf defaults, and the default image.
- [capsule-test-keys.yml](capsule-test-keys.yml) — Signs UEFI capsules with the development keys in test-keys.
- [capsule.yml](capsule.yml) — Builds the UEFI firmware capsule and adds it to the flashable package.
- [ccache.yml](ccache.yml) — Enables ccache for the recipes that compile the most.
- [ci.yml](ci.yml) — Adds the CI-only settings for signatures, parallelism, Git clones, and caches.
- [debug.yml](debug.yml) — Builds with debugging flags, a debug file system, and kernel tracing.
- [dpdk.yml](dpdk.yml) — Adds the [meta-dpdk](https://git.yoctoproject.org/meta-dpdk) layer.
- [glymur-crd.yml](glymur-crd.yml) — Builds for the glymur-crd machine.
- [iq-615-evk.yml](iq-615-evk.yml) — Builds for the iq-615-evk machine.
- [iq-8275-evk.yml](iq-8275-evk.yml) — Builds for the iq-8275-evk machine.
- [iq-9075-evk-open-fw-spl.yml](iq-9075-evk-open-fw-spl.yml) — Builds for the iq-9075-evk-open-fw-spl machine with [meta-arm](https://git.yoctoproject.org/meta-arm).
- [iq-9075-evk-open-fw.yml](iq-9075-evk-open-fw.yml) — Builds for the iq-9075-evk-open-fw machine with [meta-arm](https://git.yoctoproject.org/meta-arm).
- [iq-9075-evk.yml](iq-9075-evk.yml) — Builds for the iq-9075-evk machine.
- [iq-x5121-evk.yml](iq-x5121-evk.yml) — Builds for the iq-x5121-evk machine.
- [iq-x7181-evk.yml](iq-x7181-evk.yml) — Builds for the iq-x7181-evk machine.
- [kaanapali-mtp.yml](kaanapali-mtp.yml) — Builds for the kaanapali-mtp machine.
- [kas-container-shell-helper.sh](kas-container-shell-helper.sh) — Runs a CI helper script inside a kas-container shell.
- [kas-shell-helper.sh](kas-shell-helper.sh) — Runs a CI helper script inside a native kas shell with a work folder outside the checkout.
- [kernel-fit-image.yml](kernel-fit-image.yml) — Boots a U-Boot FIT kernel image from the ESP instead of an Android boot image.
- [linux-qcom-6.18.yml](linux-qcom-6.18.yml) — Selects the linux-qcom 6.18 kernel.
- [linux-qcom-next-rt.yml](linux-qcom-next-rt.yml) — Selects the real-time linux-qcom-next kernel.
- [linux-qcom-next.yml](linux-qcom-next.yml) — Selects the linux-qcom-next kernel.
- [linux-qcom-rt-6.18.yml](linux-qcom-rt-6.18.yml) — Selects the real-time linux-qcom 6.18 kernel.
- [linux-yocto-dev.yml](linux-yocto-dev.yml) — Selects the linux-yocto-dev kernel.
- [meta-arm.yml](meta-arm.yml) — Adds the [meta-arm](https://git.yoctoproject.org/meta-arm) and meta-arm-toolchain layers.
- [mirror-download-disable.yml](mirror-download-disable.yml) — Fetches without the Qualcomm Linux download mirror.
- [mirror-download-test.yml](mirror-download-test.yml) — Fetches only from the Qualcomm Linux download mirror to check that it is complete.
- [mirror-tarballs.yml](mirror-tarballs.yml) — Writes mirror tarballs for Git sources.
- [mirror.yml](mirror.yml) — Reuses the Yocto Project's public shared state cache.
- [nospdx.yml](nospdx.yml) — Skips SPDX image documents.
- [oe-selftest.sh](oe-selftest.sh) — Runs this layer's oe-selftest cases in a temporary build folder.
- [performance.yml](performance.yml) — Adds kernel arguments that shorten boot time.
- [qcm6490-idp.yml](qcm6490-idp.yml) — Builds for the qcm6490-idp machine.
- [qcom-armv7a.yml](qcom-armv7a.yml) — Builds for the generic qcom-armv7a machine.
- [qcom-armv8a.yml](qcom-armv8a.yml) — Builds for the generic qcom-armv8a machine with a dummy device tree.
- [qcom-distro-catchall.yml](qcom-distro-catchall.yml) — Builds the qcom-distro-catchall distribution and its images.
- [qcom-distro-kvm.yml](qcom-distro-kvm.yml) — Adds the kvm machine feature to a qcom-distro build.
- [qcom-distro-multimedia-image.yml](qcom-distro-multimedia-image.yml) — Builds only qcom-multimedia-image with qcom-distro.
- [qcom-distro-selinux.yml](qcom-distro-selinux.yml) — Builds the qcom-distro-selinux distribution and its images.
- [qcom-distro-sota.yml](qcom-distro-sota.yml) — Builds the qcom-distro-sota distribution.
- [qcom-distro.yml](qcom-distro.yml) — Adds [meta-qcom-distro](https://github.com/qualcomm-linux/meta-qcom-distro) and its layers and builds the Qualcomm Linux images.
- [qcs615-ride.yml](qcs615-ride.yml) — Builds for the qcs615-ride machine.
- [qcs6490-rb3gen2-core-kit.yml](qcs6490-rb3gen2-core-kit.yml) — Links to rb3gen2-core-kit.yml under the machine's older name.
- [qcs8300-ride-sx.yml](qcs8300-ride-sx.yml) — Builds for the qcs8300-ride-sx machine.
- [qcs9100-ride-sx.yml](qcs9100-ride-sx.yml) — Builds for the qcs9100-ride-sx machine.
- [qrb2210-rb1-core-kit.yml](qrb2210-rb1-core-kit.yml) — Links to rb1-core-kit.yml under the machine's older name.
- [rb1-core-kit.yml](rb1-core-kit.yml) — Builds for the rb1-core-kit machine.
- [rb3gen2-core-kit-open-fw.yml](rb3gen2-core-kit-open-fw.yml) — Builds for the rb3gen2-core-kit-open-fw machine with [meta-arm](https://git.yoctoproject.org/meta-arm).
- [rb3gen2-core-kit.yml](rb3gen2-core-kit.yml) — Builds for the rb3gen2-core-kit machine.
- [README.md](README.md) — Introduces this folder and indexes its contents.
- [schemacheck.py](schemacheck.py) — Validates LAVA job YAML files against the LAVA schema.
- [sdx75-idp.yml](sdx75-idp.yml) — Builds core-image-minimal for the sdx75-idp machine.
- [shikra-evk.yml](shikra-evk.yml) — Builds for the shikra-evk machine.
- [sm8750-mtp.yml](sm8750-mtp.yml) — Builds for the sm8750-mtp machine.
- [test-oe-nogl.yml](test-oe-nogl.yml) — Builds with meta-oe and without OpenGL.
- [u-boot-qcom.yml](u-boot-qcom.yml) — Selects u-boot-qcom as the boot loader.
- [world.yml](world.yml) — Builds every recipe in this layer.
- [yocto-buildstats.sh](yocto-buildstats.sh) — Charts and summarises the latest build's task statistics.
- [yocto-check-layer.sh](yocto-check-layer.sh) — Runs yocto-check-layer on this layer for all its machines.
- [yocto-patchreview.sh](yocto-patchreview.sh) — Checks the layer's patches for sign-off and Upstream-Status tags.
