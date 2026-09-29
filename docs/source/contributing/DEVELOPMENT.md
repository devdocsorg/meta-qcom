# Set up your development environment

This walkthrough prepares a checkout, runs the layer's own checks, and
rebuilds this documentation site with its function reference.

## Prerequisites

- Git, and Docker or Podman with
  [kas-container](https://github.com/siemens/kas/blob/master/kas-container) for
  builds and the layer checks. Tested with Git 2.55, Docker 29.7, and
  kas-container 4.8.2.
- For the documentation: GNU Make, GNU Awk (for shdoc), curl,
  [uv](https://docs.astral.sh/uv/getting-started/installation/), and Chromium.
  Tested with Make 4.4, GNU Awk 5.4, uv 0.12.3, and Chromium 151. uv installs
  Python 3.12 when it is missing.

Setup needs network access; reading the built site does not. On Windows, use WSL.

## 1. Clone the review branch

```sh
git clone https://github.com/devdocsorg/meta-qcom.git -b docs/layer-documentation
cd meta-qcom
git switch -c docs/my-change
```

This branch carries the documentation tools until they reach `master`. The
[contribution guide](CONTRIBUTING.md) says where to send changes.

## 2. Build and run the layer checks

Build an image and run the CI helper checks in the order the
[agent guide](AGENTS.md) gives: `yocto-patchreview` and `oe-selftest`
routinely, and `yocto-check-layer` before opening or updating a pull request.
Its environment settings are listed in
[.env.example](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/.env.example),
and the [configuration guide](../user/CONFIGURATION.md) explains the kas files.

## 3. Install the documentation tools

```sh
make -f docs/source/Makefile setup
```

This creates `.venv/` with the locked Python packages from
[requirements.lock](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/docs/source/requirements.lock),
shdoc v1.4 (checked against its SHA-256), and the BitBake parser at the commit
[ci/base.lock.yml](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/ci/base.lock.yml)
pins. Expected result: exit status 0. Keep `.venv/` out of commits.

## 4. Document functions and build the site

Document each function where it is defined, in its language's form:

- Shell functions and BitBake shell tasks take shdoc annotations (`@description`,
  `@arg` or `@noargs`, `@exitcode`, `@example`) in the comment block directly
  above the definition.
- BitBake Python functions take a Google-style comment block directly above
  the definition, with `Args`, `Returns`, and `Example` sections. Never put
  documentation inside a task body, as it would change the task's signature.
  A function nested in a Python function, or one that directly follows a
  Python `def` whose body would absorb the comment, is documented in a block
  starting `# @function NAME` (dotted for nested functions) elsewhere in the
  file, outside every function body.
- Python files take Google-style docstrings with an `Example` section.

```sh
make -f docs/source/Makefile html
```

Expected result: exit status 0, a `Reference coverage: ... documented and
rendered.` line, and `docs/site/index.html`. The build fails on an undocumented
function, a missing rendered entry, or a source format that
[test_reference_coverage.py](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/.github/test_reference_coverage.py)
cannot read; extend that script when adding a format. Commit the source and
the regenerated `docs/site/` together.

## 5. Check the site

```sh
make -f docs/source/Makefile check
```

This rebuilds the site, opens a copy through `file://` in headless Chromium
with networking disabled, follows every link and anchor, runs a search, and
fails if `docs/site/` differs from the committed output. Expected result: exit
status 0 and a JSON line reporting the pages visited and no network requests.
Without a system Chromium, run `make -f docs/source/Makefile browser` first.
The [documentation workflow](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/.github/workflows/documentation.yml)
runs the same targets.

After changing
[requirements.txt](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/docs/source/requirements.txt),
regenerate the lock with
`uv pip compile --python-version 3.12 docs/source/requirements.txt -o docs/source/requirements.lock`,
then run setup and rebuild.
