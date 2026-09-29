# meta-qcom documentation

meta-qcom is the OpenEmbedded/Yocto Project hardware enablement layer for Qualcomm
based platforms. Start with the [build, flash, and boot tutorial](user/USAGE.md), or
follow [development environment setup](contributing/DEVELOPMENT.md) to change the
layer.

```{toctree}
:hidden:

user/README
contributing/README
```

## Folders

- [user/](user/README.md) — Explains how to build, flash, configure, and secure images made with the layer.
- [contributing/](contributing/README.md) — Owns contribution guidance, agent guidance, development setup, and the function reference.
- [.templates/](https://github.com/devdocsorg/meta-qcom/tree/docs/layer-documentation/docs/source/.templates) — Supplies the generated site's entry-point redirect.

## Files

- [Makefile](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/docs/source/Makefile) — Provides the shared local and CI setup, build, and check commands.
- [README.md](README.md) — Introduces the guides and supplies the site's homepage.
- [conf.py](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/docs/source/conf.py) — Configures Markdown rendering, the function reference, local navigation, and search.
- [requirements.txt](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/docs/source/requirements.txt) — Pins the documentation packages.
- [requirements.lock](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/docs/source/requirements.lock) — Locks direct and transitive documentation dependencies for reproducible builds.
