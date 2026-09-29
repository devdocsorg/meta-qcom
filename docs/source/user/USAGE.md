# Build, flash, and boot an image

This tutorial builds `core-image-base` for the Qualcomm RB3 Gen 2 Core Kit
(`rb3gen2-core-kit`), flashes it, and logs in on the board. For another board, use
its kas file from `ci/` and the matching board preparation.

## Prerequisites

- A Linux host prepared as the
  [Yocto Project system requirements](https://docs.yoctoproject.org/ref-manual/system-requirements.html)
  describe, with Docker or Podman and the
  [kas-container](https://github.com/siemens/kas/blob/master/kas-container) script on
  your `PATH`.
- The QDL tool and its `udev` rule, from [Build QDL tool](flashing.md#build-qdl-tool).
- An RB3 Gen 2 Core Kit with its micro USB debug cable and a USB-C cable.

## 1. Build the image

From an empty working directory:

```sh
git clone https://github.com/qualcomm-linux/meta-qcom.git -b master
kas-container build meta-qcom/ci/rb3gen2-core-kit.yml
```

Expected result: the build ends without errors and creates the flashable package
`build/tmp/deploy/images/rb3gen2-core-kit/core-image-base-rb3gen2-core-kit.rootfs.qcomflash/`,
with a `.qcomflash.tar.gz` archive of the same files beside it. The
[README](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/README.md#quick-build) covers shared
caches and native kas.

## 2. Flash the board

Follow [Prepare the Board](flashing.md#prepare-the-board) and
[Flash images](flashing.md#flash-images), running QDL from the package directory
created in step 1.

Expected result: with the board in EDL mode, QDL starts flashing on its own, prints
the progress shown in [Flash images](flashing.md#flash-images), and exits without an
error.

## 3. Log in

Power-cycle the board with the serial console open at 115200 baud. `ci/base.yml`
allows root login without a password, so log in as `root` and run:

```sh
uname -m
```

Expected result: the login prompt names the host `rb3gen2-core-kit`, and the command
prints `aarch64`.
