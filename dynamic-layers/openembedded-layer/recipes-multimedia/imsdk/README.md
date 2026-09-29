# imsdk

Additions to the IMSDK GStreamer plugin recipes of this layer that BitBake parses only when the meta-oe layer from [meta-openembedded](https://github.com/openembedded/meta-openembedded) is in the build.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [gst-plugins-imsdk-oss_%.bbappend](gst-plugins-imsdk-oss_%25.bbappend) — Enables the ml, messaging, python-apps, redissink, sample-apps, and builder-cpp PACKAGECONFIG options for every machine.
- [gst-plugins-imsdk-prop_%.bbappend](gst-plugins-imsdk-prop_%25.bbappend) — Enables the camera and camera-apps PACKAGECONFIG options for every machine.
- [gst-plugins-imsdk-python_2.0.2.bb](gst-plugins-imsdk-python_2.0.2.bb) — Builds the IMSDK GStreamer Python binding overrides that complement python-gi, using the shared IMSDK include files, and requires the gobject-introspection-data distro feature.
