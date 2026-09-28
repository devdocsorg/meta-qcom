# Run from the repository root: make -f docs/source/Makefile <target>.
# setup installs the pinned documentation toolchain in .venv and .docs-tools.
# html removes stale generated pages, builds the site strictly, and checks
# that every discovered function has a documented, rendered reference entry.
# check verifies output is committed and direct-file search avoids fetch().
.PHONY: setup html check browser

TOOLS := .docs-tools
# shdoc 1.4 renders shell and BitBake shell function comments.
SHDOC_REV := b3436134f08428f8bbe2e54bc4dc20da85cd300b
# The reference parses metadata with the BitBake and OE-Core revisions pinned
# for builds in ci/base.lock.yml.
BITBAKE_REV = $(shell sed -n '/^ *bitbake:/{n;s/.*commit: *//p;}' ci/base.lock.yml)
OECORE_REV = $(shell sed -n '/^ *oe-core:/{n;s/.*commit: *//p;}' ci/base.lock.yml)

setup:
	uv venv --python 3.12 --clear .venv
	uv pip install --python .venv/bin/python -r docs/source/requirements.lock
	rm -rf $(TOOLS)
	mkdir -p $(TOOLS)
	curl -fsSL -o $(TOOLS)/shdoc https://raw.githubusercontent.com/reconquest/shdoc/$(SHDOC_REV)/shdoc
	git init -q $(TOOLS)/bitbake
	git -C $(TOOLS)/bitbake fetch -q --depth=1 https://github.com/openembedded/bitbake $(BITBAKE_REV)
	git -C $(TOOLS)/bitbake checkout -q FETCH_HEAD
	git init -q $(TOOLS)/oe-core
	git -C $(TOOLS)/oe-core sparse-checkout set meta/lib
	git -C $(TOOLS)/oe-core fetch -q --depth=1 --filter=blob:none https://github.com/openembedded/openembedded-core $(OECORE_REV)
	git -C $(TOOLS)/oe-core checkout -q FETCH_HEAD

html:
	rm -rf docs/site docs/source/contributing/.generated
	.venv/bin/sphinx-build -W --keep-going -E -a -b html -d docs/.doctrees docs/source docs/site
	.venv/bin/python .github/finalise_site.py
	.venv/bin/python .github/test_reference_coverage.py

# Install a user-local browser only when system Chromium is unavailable.
browser:
	.venv/bin/playwright install chromium

check: html
	.venv/bin/python .github/check_offline.py docs/site kas-container
	test -f docs/site/index.html
	grep -q 'SHOW_SEARCH_SUMMARY: false' docs/site/_static/documentation_options.js
	git diff --exit-code -- docs/site
	test -z "$$(git ls-files --others --exclude-standard docs/site)"
