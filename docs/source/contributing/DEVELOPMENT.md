# Set up your development environment

This walkthrough prepares a checkout, installs the documentation tools, builds the
site with its function reference, and runs the checks. Building images and running
the layer's own checks use kas-container, as the [agent guide](AGENTS.md) describes.

## Prerequisites

Tested with Git 2.55, GNU Make 4.4, GNU Awk 5.4 (for shdoc), curl,
[uv](https://docs.astral.sh/uv/getting-started/installation/) 0.12 (it installs
Python 3.12 for the tools), and Chromium 151 for the offline browser check. Image
builds and the layer checks also need Docker or Podman and `kas-container`; see the
agent guide's [prerequisites](AGENTS.md#1-prerequisites). Installing the tools
needs network access; reading the built site does not.

## 1. Clone and create a branch

```sh
git clone https://github.com/devdocsorg/meta-qcom.git -b docs/layer-documentation
cd meta-qcom
git switch -c docs/my-change
```

This review branch holds the documentation tools. Send the pull request to
the project as the [contribution guide](CONTRIBUTING.md#where-to-send-changes) describes.

## 2. Install the documentation tools

```sh
make -f docs/source/Makefile setup
```

This creates `.venv/` with the locked Python packages from
[requirements.lock](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/docs/source/requirements.lock),
the checksum-verified shdoc, and the BitBake parser at the revision
[ci/base.lock.yml](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/ci/base.lock.yml)
pins. `.venv/` is ignored by Git. The Makefile uses a POSIX shell; on Windows, use WSL.

## 3. Build and check the site

```sh
make -f docs/source/Makefile check
```

Expected result: exit status 0, a line starting `Reference coverage:` and ending
`documented and rendered.`, `docs/site/index.html`, and a final JSON line reporting
the pages visited, a `bitbake` search result, and no network requests or browser
errors. The check builds the site, copies it, and opens it through `file://` with
networking disabled; it uses system Chromium when available, otherwise run
`make -f docs/source/Makefile browser` first. To rebuild the site without the browser
check, run `make -f docs/source/Makefile html`. Open `docs/site/index.html` directly
in the browser; `docs/site/` is generated and ignored by Git. The
[Documentation workflow](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/.github/workflows/documentation.yml)
runs the same setup and check on every pull request.

The build fails when a function in a recipe, class, include, append, script,
workflow step, or Python module has no documentation comment or no complete rendered
entry, and when a tracked file has a format that no extractor reads. Document a new
function where the reference expects it:

- Shell functions and BitBake shell tasks: a shdoc block (`@description`,
  `@arg` or `@noargs`, `@exitcode`, `@example`) directly above the definition.
- BitBake Python functions: a Google-style comment block (purpose, `Args:`,
  `Returns:`, `Example:`) directly above the definition.
- Python modules: Google-style docstrings.

Never put these comments inside a BitBake function body: body text is part of the
task signature. Where a comment would fall inside a preceding Python function, or
for a function nested in a task, write the block outside every function body and
start it with `# @function NAME`, using the dotted name for nested functions.
[test_reference_coverage.py](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/.github/test_reference_coverage.py)
lists the formats it reads.

## 4. Run the layer's checks

Before opening or updating a pull request, run the CI-equivalent layer checks in
the order the agent guide's
[pull request workflow](AGENTS.md#6-pull-request--contribution-workflow) lists. The
Markdown Lint workflow checks every Markdown file against
[.markdownlint.yaml](https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/.github/.markdownlint.yaml)
when Markdown changes; with Node.js installed, run it locally with
`npx markdownlint-cli2@0.22.1 --config .github/.markdownlint.yaml "**/*.md" "#.venv"`.

After an intentional documentation tool update, regenerate the lock with
`uv pip compile --python-version 3.12 docs/source/requirements.txt -o docs/source/requirements.lock`,
run setup, and rebuild before committing the requirements and lock.
