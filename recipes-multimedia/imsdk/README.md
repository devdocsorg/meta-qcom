# imsdk

Recipes for the Qualcomm IMSDK GStreamer plugins, split into base libraries, open-source plugins, and proprietary plugins, all built from one source tree on ARMv8 machines with OpenGL.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [gst-plugins-imsdk-base_2.0.2.bb](gst-plugins-imsdk-base_2.0.2.bb) — Builds the common base libraries that the other IMSDK plugin recipes depend on.
- [gst-plugins-imsdk-common.inc](gst-plugins-imsdk-common.inc) — Shared by the three IMSDK plugin recipes: source, license, dependencies, and the `PACKAGECONFIG` options that switch plugin groups on and off.
- [gst-plugins-imsdk-oss_2.0.2.bb](gst-plugins-imsdk-oss_2.0.2.bb) — Builds the open-source IMSDK plugins, by default the software, tools, and video processing groups.
- [gst-plugins-imsdk-packaging.inc](gst-plugins-imsdk-packaging.inc) — Shared by the three IMSDK plugin recipes: splits the plugins into GStreamer-style packages, with runtime modules and configuration files in separate packages.
- [gst-plugins-imsdk-prop_2.0.2.bb](gst-plugins-imsdk-prop_2.0.2.bb) — Builds the proprietary IMSDK plugins, by default the QAIRT machine learning and smart video encoder plugins.
- [smart-venc-ctrl-algo_1.0.2.bb](smart-venc-ctrl-algo_1.0.2.bb) — Installs the prebuilt smart video encoder control library that tunes encoding parameters at runtime.
