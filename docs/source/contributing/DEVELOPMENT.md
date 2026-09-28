# Set up your development environment

This walkthrough prepares a checkout, builds the documentation site with its
function reference, and runs the documentation checks. Layer builds and the
layer's own checks use the procedures linked in step 4.

## Prerequisites

Tested with Git 2.55, GNU Make 4.4, curl 8.21, GNU Awk 5.4 (shdoc needs `gawk`),
[uv](https://docs.astral.sh/uv/getting-started/installation/) 0.12, which
installs Python 3.12, and Chromium 151. Setup needs network access; reading
the built site does not.

## 1. Clone the review branch

```sh
git clone https://github.com/devdocsorg/meta-qcom.git -b docs/layer-documentation
cd meta-qcom
git switch -c my-change
```

Send the finished change to the project as described in the
[contribution guide](CONTRIBUTING.md).

## 2. Install the documentation tools

```sh
make -f docs/source/Makefile setup
```

This creates `.venv` from `docs/source/requirements.lock` and fills
`.docs-tools` with [shdoc](https://github.com/reconquest/shdoc) 1.4 and the
[BitBake](https://github.com/openembedded/bitbake) and
[openembedded-core](https://github.com/openembedded/openembedded-core)
revisions pinned in `ci/base.lock.yml`. Both folders stay
out of commits. No other configuration is needed; the environment settings
that the build helpers read are listed in `.env.example`.

## 3. Build and check the site

```sh
make -f docs/source/Makefile check
```

The `check` target rebuilds `docs/site` strictly, confirms every function is
documented and rendered, opens a copy of the site in headless Chromium with
networking disabled, and fails if the committed site differs from the rebuild.
Expected result: exit status 0, a `Function reference:` line reporting that
every function is documented and rendered, and a JSON summary with empty
`network_requests` and `browser_errors`. Commit the regenerated `docs/site`
with its sources, then rerun the check.

Without system Chromium, run `make -f docs/source/Makefile browser` once to
install Playwright's user-local browser. `make -f docs/source/Makefile html`
builds the site without the browser and committed-output checks.

Pull requests that change Markdown also run
[markdownlint](https://github.com/DavidAnson/markdownlint-cli2) 0.22.1 with
`.github/.markdownlint.yaml`:

```sh
npx markdownlint-cli2@0.22.1 --config .github/.markdownlint.yaml "**/*.md" "#.venv" "#.docs-tools" "#docs/source/contributing/.generated"
```

## 4. Build and check the layer

Follow the README's [quick build](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/README.md#quick-build)
and the agent guide's [routine checks](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/AGENTS.md#4-run-routine-checks-via-ci-helper-scripts).
Before opening or updating a pull request, run the CI-equivalent checks in the
[order the agent guide gives](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/AGENTS.md#6-pull-request--contribution-workflow).

## Document functions

The site's function reference comes from comments in the source. The build
fails when a function lacks them or a tracked file has a format with no
configured extractor.

- Shell functions and BitBake shell tasks: an [shdoc](https://github.com/reconquest/shdoc)
  block directly above the function, with `@description`, `@arg` or `@noargs`,
  `@exitcode`, and `@example`.
- Python functions and BitBake Python tasks: a docstring, or a comment block
  directly above the definition, with a purpose sentence and Google-style
  `Args:`, `Returns:`, `Raises:`, and `Example:` sections.

`.github/test_reference_coverage.py` generates the pages and checks coverage;
its module comment lists the formats it reads.

After an intentional documentation tool update, regenerate the lock with
`uv pip compile --python-version 3.12 docs/source/requirements.txt -o docs/source/requirements.lock`,
run setup, and rebuild before committing source and output together.
