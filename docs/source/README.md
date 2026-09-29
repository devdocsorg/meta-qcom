# meta-qcom documentation

Build and flash an image with the [user guides](user/README.md), or prepare a
change with the [contributor guides](contributing/README.md), which include the
reference for every function in the layer.

```{toctree}
:hidden:

user/README
contributing/README
```

## Folders

- [user/](user/README.md) — Holds the flashing tutorial, configuration reference, and production security recommendations.
- [contributing/](contributing/README.md) — Holds the contribution, development, and agent guides and the function reference.
- [.templates/](https://github.com/devdocsorg/meta-qcom/tree/docs/layer-documentation/docs/source/.templates) — Supplies the generated site's entry-point redirect.

## Files

- [Makefile](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/docs/source/Makefile) — Provides the shared local and CI setup, build, and check commands.
- [README.md](README.md) — Introduces the guides and supplies the site's homepage.
- [conf.py](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/docs/source/conf.py) — Configures Markdown rendering, Python autodoc, local navigation, and search.
- [requirements.txt](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/docs/source/requirements.txt) — Pins the direct documentation packages.
- [requirements.lock](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/docs/source/requirements.lock) — Locks direct and transitive documentation packages for reproducible builds.
