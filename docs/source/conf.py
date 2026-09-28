# Copyright (c) 2026 DevDocs
# SPDX-License-Identifier: BSD-3-Clause
"""Configure the layer's Markdown site for hosted and direct-file browsing."""
import sys
from pathlib import Path

# Keep imports during the build from writing __pycache__ into the checkout.
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
# The reference extension, the pinned BitBake and OE-Core libraries that the
# layer's Python modules import, and the layer's own Python library.
sys.path[:0] = [str(ROOT / ".github"), str(ROOT / ".docs-tools/bitbake/lib"),
                str(ROOT / ".docs-tools/oe-core/meta/lib"), str(ROOT / "lib")]

# Optional string; default 'Project name not set'.
project = "meta-qcom"
# Optional list; default []. Render Markdown with MyST, extract Python
# docstrings, read Google-style sections, and generate the function reference.
extensions = ["myst_parser", "sphinx.ext.autodoc", "sphinx.ext.napoleon", "test_reference_coverage"]
# Optional boolean; default True. Show each method's own documentation rather
# than a docstring inherited from OE-Core's base class.
autodoc_inherit_docstrings = False
# Optional string; default 'index'. README owns the homepage content.
root_doc = "README"
# Optional integer; default 0. Preserve links to Markdown headings.
myst_heading_anchors = 4
# Optional boolean; default False. Reject unresolved cross-references.
nitpicky = True
# Optional list; default []. Type names in reference signatures that have no
# local target; they remain plain text.
nitpick_ignore_regex = [(r"py:.*", r".*")]
# Optional list; default []. Do not parse build templates as documentation.
exclude_patterns = [".templates/**"]
# Optional list; default []. Resolve the additional HTML template locally.
templates_path = [".templates"]
# Optional mapping; default {}. Generate an entry point without a second source index.
html_additional_pages = {"index": "index.html"}
# Optional boolean; default True. Avoid fetch() of local files for search excerpts.
html_show_search_summary = False
# Optional boolean; default True. Page sources stay in the repository, not the site.
html_copy_source = False
# Optional boolean; default True. No copyright holder is configured, so omit the empty notice.
html_show_copyright = False
