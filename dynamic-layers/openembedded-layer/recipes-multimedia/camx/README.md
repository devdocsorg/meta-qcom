# camx

Installs prebuilt Qualcomm CamX camera libraries, one recipe per SoC platform; each recipe unpacks the camxlib, camx, chicdk, and test archives for its platform and splits them into packages.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [camxlib-hamoa_1.0.48.bb](camxlib-hamoa_1.0.48.bb) — Sets the hamoa platform and archive checksums for `common.inc`, and also packages the x1e80100 DSP skel files as camxlib-hamoa-skel.
- [camxlib-kodiak_1.0.44.bb](camxlib-kodiak_1.0.44.bb) — Stand-alone kodiak recipe that does not use `common.inc`: it also depends on sensinghub and qcom-sensors-binaries, drops OpenCL or OpenGL libraries when those distro features are off, and packages camx-kodiak, chicdk-kodiak, and skel files.
- [camxlib-lemans_1.0.48.bb](camxlib-lemans_1.0.48.bb) — Sets the lemans platform for `common.inc`, provides camxlib-monaco, packages the camera-nhx test tool and its JSON files as camx-nhx and the DSP skel files as camxlib-lemans-skel, and drops OpenCL files when opencl is off.
- [camxlib-shikra_1.0.48.bb](camxlib-shikra_1.0.48.bb) — Sets the shikra platform for `common.inc`, adds a sensinghub dependency, and drops the GPU camera node when opencl is off.
- [camxlib-talos_1.0.48.bb](camxlib-talos_1.0.48.bb) — Sets the talos platform for `common.inc` and drops the iwarp and hidrx camera components unless both opengl and opencl are enabled.
- [common.inc](common.inc) — Shared by the hamoa, lemans, shikra, and talos recipes: fetches the camxlib, camx, chicdk, camxcommon, and camxtest archives for `PLATFORM`, installs them for aarch64, and creates the camx-`PLATFORM` and chicdk-`PLATFORM` packages.
