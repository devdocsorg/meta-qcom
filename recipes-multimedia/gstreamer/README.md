# gstreamer

Appends that add Qualcomm-specific formats and fixes to the GStreamer plugin recipes; BitBake applies each bbappend to every version of its recipe, and the patches apply only to Qualcomm machines.

## Folders

- [gstreamer1.0-plugins-bad/](gstreamer1.0-plugins-bad/) — Patches that add NV12_Q08C support to the Wayland sink and fix its buffer handling in PAUSED and for gap buffers.
- [gstreamer1.0-plugins-base/](gstreamer1.0-plugins-base/) — Patches that add the NV12_Q08C and NV12_Q10LE32C compressed video formats and change the stride alignment logic of video meta.
- [gstreamer1.0-plugins-good/](gstreamer1.0-plugins-good/) — Patches for the V4L2 elements (QC08C and QC10C formats, encoder and decoder fixes, gap and empty buffers) and for the PulseAudio elements, including a new `pulsedirectsink` element.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [gstreamer1.0-plugins-bad_%.bbappend](gstreamer1.0-plugins-bad_%25.bbappend) — For Qualcomm machines, adds the patches from `gstreamer1.0-plugins-bad/` to the Wayland elements.
- [gstreamer1.0-plugins-base_%.bbappend](gstreamer1.0-plugins-base_%25.bbappend) — For Qualcomm machines, adds the patches from `gstreamer1.0-plugins-base/` for the Qualcomm compressed video formats.
- [gstreamer1.0-plugins-good_%.bbappend](gstreamer1.0-plugins-good_%25.bbappend) — For Qualcomm machines, adds the patches from `gstreamer1.0-plugins-good/` for the V4L2 and PulseAudio elements.
