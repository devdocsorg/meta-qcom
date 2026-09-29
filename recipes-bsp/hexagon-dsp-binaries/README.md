# hexagon-dsp-binaries

Recipe for the Hexagon DSP libraries from [dsp-binaries](https://github.com/linux-msm/dsp-binaries) and executables that run on the matching DSP firmware through the FastRPC interface. BitBake builds the versioned `.bb` recipe, which takes its source, packaging, and license settings from the shared `.inc`.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [hexagon-dsp-binaries.inc](hexagon-dsp-binaries.inc) — Shared by `hexagon-dsp-binaries_*.bb`; fetches [dsp-binaries](https://github.com/linux-msm/dsp-binaries) at the tag matching `PV`, installs it with `make install`, and splits it into one package per board and DSP plus per-board config packages generated from the `conf.d` YAML files, leaving the base package empty.
- [hexagon-dsp-binaries_20260910.bb](hexagon-dsp-binaries_20260910.bb) — Release 20260910 of the Hexagon DSP binaries; pins the source revision and license checksums.
