# meta-qcom documentation

meta-qcom is the OpenEmbedded and Yocto Project hardware enablement layer for
Qualcomm platforms. Start with the [flashing tutorial](user/flashing.md), look
up build settings in the [configuration reference](user/CONFIGURATION.md), or
prepare a change with the [development setup](contributing/DEVELOPMENT.md).

```{toctree}
:hidden:

user/README
contributing/README
```

## Folders

- [user/](user/README.md) — Holds the tutorial, configuration reference, and production security guidance.
- [contributing/](contributing/README.md) — Holds the contribution and development guides and the function reference.
- [.templates/](https://github.com/devdocsorg/meta-qcom/tree/docs/layer-documentation/docs/source/.templates) — Supplies the generated site's entry-point redirect.

## Files

- [Makefile](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/docs/source/Makefile) — Provides the shared local and CI setup, build, and check commands.
- [README.md](README.md) — Introduces the guides and supplies the site's homepage.
- [conf.py](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/docs/source/conf.py) — Configures Markdown rendering, the function reference, local navigation, and search.
- [requirements.txt](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/docs/source/requirements.txt) — Declares the documentation packages.
- [requirements.lock](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/docs/source/requirements.lock) — Locks direct and transitive documentation dependencies for reproducible builds.
