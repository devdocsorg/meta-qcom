# Copyright (c) 2026 DevDocs
# SPDX-License-Identifier: BSD-3-Clause
"""Find every function definition and check its native reference.

Usage: test_reference_coverage.py generate | check

docs/source/conf.py runs "generate" before Sphinx reads its sources: it fails
on source formats without a configured extractor, on functions without a
configured renderer, and on undocumented functions, then writes one reference
page per source file to docs/source/contributing/.generated/. The Makefile
runs "check" after the HTML build: it fails when a function has no rendered
reference entry.

Functions are found in tracked and staged files with parsers, independently of
the renderers; nothing is executed. BitBake's own statement parser, pinned by
ci/base.lock.yml and installed by the Makefile's setup, splits recipes,
classes, and includes into shell and Python functions without evaluating
them, and reads configuration files and kas local.conf snippets, which cannot
define functions. Python's ast module reads Python files and Python function
bodies, and tree-sitter-bash reads shell scripts, shell task bodies, workflow
and action run steps, kernel-cache (.scc) files, and Makefile recipes.
Adapting a repository means adding its source formats to discover() and a
renderer for each language that defines functions to RENDERERS.
"""
import ast
import html
import re
import subprocess
import sys
from pathlib import Path

import tree_sitter_bash
import yaml
from docutils.nodes import make_id
from sphinx.ext.napoleon import Config
from sphinx.ext.napoleon.docstring import GoogleDocstring
from tree_sitter import Language, Parser

ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / "docs/source/contributing/.generated"
SITE = ROOT / "docs/site/contributing/.generated"
SHELL = Parser(Language(tree_sitter_bash.language()))
sys.path.insert(0, str(ROOT / ".venv/bitbake/lib"))
from bb.parse import ParseError, ast as bbast  # noqa: E402  BitBake is installed by the Makefile's setup.
from bb.parse.parse_py import BBHandler, ConfHandler  # noqa: E402

# Formats verified to hold no function definitions: documentation, locks,
# kernel configuration fragments, patches to upstream sources, device tree
# sources, keys and certificates, udev rules, modprobe configuration, and
# licence texts.
PLAIN_SUFFIXES = (".md", ".txt", ".lock", ".cfg", ".patch", ".dts", ".pem", ".cer", ".rules",
                  ".venus", ".vidc", ".qcom", ".qcom-2")
PLAIN_NAMES = ("LICENSE", "NOTICE", "README", "CODEOWNERS", ".gitignore", ".env.example", ".markdownlint.yaml")
METADATA_SUFFIXES = (".bb", ".bbappend", ".bbclass", ".inc")
# A documentation block for a function whose comment cannot sit directly above
# its definition: a function nested in a Python function, or one that follows a
# Python function whose body would absorb the comment.
FUNCTION_BLOCK = re.compile(r"#\s*@function\s+(\S+)$")


def page_name(path):
    """Return the generated page name for a repository-relative source path.

    Args:
        path (str): Source path, such as ``ci/build.sh``.

    Returns:
        str: The page name without a suffix, such as ``ci-build.sh``.

    Example:
        ``page_name("ci/build.sh")`` returns ``"ci-build.sh"``.
    """
    return path.replace("/", "-")


def comment_above(lines, start):
    """Return the comment block directly above a line.

    Args:
        lines (list[str]): The file's lines.
        start (int): Zero-based index of the definition line.

    Returns:
        str: The ``#`` lines directly above the definition, stripped, or "".

    Example:
        ``comment_above(["# Say hello.", "f() {"], 1)`` returns ``"# Say hello."``.
    """
    comments = []
    while start - len(comments) > 0 and lines[start - len(comments) - 1].lstrip().startswith("#"):
        comments.insert(0, lines[start - len(comments) - 1].strip())
    return "\n".join(comments)


def function_blocks(lines, spans):
    """Collect the ``# @function NAME`` documentation blocks outside function bodies.

    Args:
        lines (list[str]): The file's lines.
        spans (list[tuple[int, int]]): Zero-based first and last lines of each
            function, whose comments belong to the function body.

    Returns:
        dict[str, str]: The comment block after each ``@function`` line, by name.

    Example:
        ``function_blocks(["# @function outer.inner", "# Say hello."], [])``
        returns ``{"outer.inner": "# Say hello."}``.
    """
    blocks = {}
    for index, line in enumerate(lines):
        m = FUNCTION_BLOCK.match(line.strip())
        if not m or any(first <= index <= last for first, last in spans):
            continue
        comments = []
        for following in lines[index + 1:]:
            if not following.lstrip().startswith("#") or FUNCTION_BLOCK.match(following.strip()):
                break
            comments.append(following.strip())
        blocks[m.group(1)] = "\n".join(comments)
    return blocks


def shell_functions(path, where, text, prefix="", blocks=None):
    """List the shell functions defined in a shell text.

    Args:
        path (str): Source path, used in reports.
        where (str): Location inside the file, such as a workflow step, or "".
        text (str): Shell code.
        prefix (str): Name of the enclosing BitBake task for nested functions, or "".
        blocks (dict[str, str] | None): ``@function`` blocks that document nested
            functions, whose comments cannot sit above them without changing the task.

    Returns:
        list[dict]: One entry per function with its name, line, and comment block.

    Raises:
        ValueError: The shell parser cannot read the text.

    Example:
        ``shell_functions("ci/build.sh", "", "f() { :; }")`` finds ``f``.
    """
    tree = SHELL.parse(text.encode())
    if tree.root_node.has_error:
        raise ValueError(f"{path}{where}: the shell parser cannot read it")
    found, stack = [], [tree.root_node]
    while stack:
        node = stack.pop()
        if node.type == "function_definition":
            found.append((node.start_point[0], node.child_by_field_name("name").text.decode()))
        stack.extend(node.children)
    lines, functions = text.splitlines(), []
    for start, name in sorted(found):
        if prefix:
            name = f"{prefix}.{name}"
            doc = (blocks or {}).get(name, "")
        else:
            doc = comment_above(lines, start)
        functions.append({"language": "shell", "path": path, "where": where, "name": name,
                          "line": start + 1, "doc": doc})
    return functions


def python_functions(path, text):
    """List the functions and methods defined in a Python file.

    Args:
        path (str): Source path, used in reports.
        text (str): Python source.

    Returns:
        list[dict]: One entry per function with its qualified name, line, and
        docstring. Functions nested in other functions are included and marked
        ``nested``, because autodoc cannot import them.

    Example:
        ``python_functions("tool.py", "def f():\\n    pass\\n")`` finds ``f``.
    """
    functions, stack = [], [(ast.parse(text, path), "", False)]
    while stack:
        node, prefix, in_function = stack.pop()
        for child in ast.iter_child_nodes(node):
            is_function = isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef))
            if is_function:
                functions.append({"language": "python", "path": path, "where": "", "name": prefix + child.name,
                                  "line": child.lineno, "doc": ast.get_docstring(child) or "",
                                  "nested": in_function})
            name = prefix + child.name + "." if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef,
                                                                     ast.ClassDef)) else prefix
            stack.append((child, name, in_function or is_function))
    return sorted(functions, key=lambda function: function["line"])


def expression_free(text):
    """Replace BitBake inline Python expressions, which BitBake expands before a shell task runs.

    Args:
        text (str): A shell task body.

    Returns:
        str: The body with each ``${@...}`` expression replaced by a placeholder word.

    Example:
        ``expression_free("echo ${@d.getVar('PN')}")`` returns ``"echo BITBAKE_EXPRESSION"``.
    """
    result, index = [], 0
    while (start := text.find("${@", index)) >= 0:
        depth, end = 0, start + 1
        while end < len(text):
            depth += {"{": 1, "}": -1}.get(text[end], 0)
            if depth == 0:
                break
            end += 1
        result.append(text[index:start] + "BITBAKE_EXPRESSION")
        index = end + 1
    return "".join(result) + text[index:]


def reset_bitbake_parser():
    """Clear the BitBake parser's module state after a file that failed to parse.

    Returns:
        None: The next file starts outside any function.

    Example:
        ``reset_bitbake_parser()``
    """
    vars(BBHandler).update({"__infunc__": [], "__inpython__": False, "__body__": [], "__residue__": []})


def bitbake_functions(path, text):
    """List the shell and Python functions in a BitBake recipe, class, or include.

    BitBake's statement parser finds each definition, including ``fakeroot`` and
    ``python`` modifiers, override suffixes, anonymous functions, and ``def``
    functions. Functions nested in a shell or Python task are found by parsing the
    task body. Nothing is evaluated.

    Args:
        path (str): Source path.
        text (str): File contents.

    Returns:
        list[dict]: One entry per function with its language, name, line, and comment block.

    Raises:
        ValueError: The BitBake, shell, or Python parser cannot read the file.

    Example:
        ``bitbake_functions("recipes-bsp/x/x.bb", "do_install() {\\n    :\\n}\\n")`` finds ``do_install``.
    """
    BBHandler.cached_statements.pop(str(ROOT / path), None)
    try:
        statements = BBHandler.get_statements(path, str(ROOT / path), "")
    except (ParseError, SyntaxError) as error:
        reset_bitbake_parser()
        raise ValueError(f"{path}: the BitBake parser cannot read it: {error}")
    lines, defined = text.splitlines(), []
    for statement in statements:
        if isinstance(statement, bbast.MethodNode):
            start = statement.lineno - len(statement.body) - 1
            python = statement.python or statement.func_name == "__anonymous"
            defined.append((start, statement.lineno - 1, statement.func_name, python,
                            "\n".join(statement.body), "def _(d):\n"))
        elif isinstance(statement, bbast.PythonMethodNode):
            start = next(i for i in range(min(statement.lineno, len(lines)) - 1, -1, -1)
                         if lines[i].rstrip() == statement.body[0])
            defined.append((start, start + len(statement.body) - 1, statement.function, True,
                            "\n".join(statement.body[1:]), statement.body[0] + "\n"))
    spans = [(start, end) for start, end, *_ in defined]
    blocks = function_blocks(lines, spans)
    functions = []
    for start, end, name, python, body, header in defined:
        doc = blocks.get(name) or comment_above(lines, start)
        functions.append({"language": "static-python" if python else "shell", "path": path, "where": "",
                          "name": name, "line": start + 1, "doc": doc})
        if python:
            try:
                found = python_functions(path, header + body)
            except SyntaxError as error:
                raise ValueError(f"{path}:{start + 1}: the Python parser cannot read {name}: {error}")
            for nested in found:
                if nested["nested"]:
                    qualified = name + nested["name"][nested["name"].index("."):]
                    functions.append({"language": "static-python", "path": path, "where": "",
                                      "name": qualified, "line": start + nested["line"],
                                      "doc": blocks.get(qualified, "")})
        else:
            functions += shell_functions(path, f" (in {name})", expression_free(body), name, blocks)
    return functions


def configuration_statements(path, where, text):
    """Check BitBake configuration text, which cannot define functions, with BitBake's parser.

    Args:
        path (str): Source path, used in reports.
        where (str): Location inside the file, such as a kas ``local_conf_header`` entry, or "".
        text (str): BitBake configuration text.

    Raises:
        ValueError: The configuration parser rejects a line, such as a function definition.

    Example:
        ``configuration_statements("conf/layer.conf", "", 'BBPATH .= ":${LAYERDIR}"')``
    """
    statements, residue = bbast.StatementGroup(), ""
    for lineno, line in enumerate(text.splitlines(), 1):
        line = residue + line.rstrip()
        if line.endswith("\\"):
            residue = line[:-1]
            continue
        residue = ""
        if line.strip() and not line.lstrip().startswith("#"):
            try:
                ConfHandler.feeder(lineno, line.strip(), path, statements, baseconfig=True)
            except ParseError as error:
                raise ValueError(f"{path}{where}:{lineno}: BitBake configuration cannot hold this line, and "
                                 f"no function extractor is configured for it: {error}")


def run_steps(path, steps, default_shell):
    """List the shell functions in workflow or composite-action run steps.

    Args:
        path (str): Source path, used in reports.
        steps (list[dict]): The steps of one job or composite action.
        default_shell (str): The shell used by steps that do not name one.

    Returns:
        tuple[list[dict], list[str]]: The functions found and the unsupported steps.

    Example:
        ``run_steps(".github/workflows/ci.yml", [{"run": "f() { :; }"}], "bash")`` finds ``f``.
    """
    functions, problems = [], []
    for number, step in enumerate(steps or [], 1):
        where = f" (step {number})"
        if "run" not in step:
            continue
        shell = str(step.get("shell", default_shell))
        # GitHub substitutes expressions before the shell runs.
        run = re.sub(r"\$\{\{.*?\}\}", "GITHUB_EXPRESSION", str(step["run"]))
        if re.match(r"(ba)?sh\b", shell):
            functions += shell_functions(path, where, run)
        elif shell == "python":
            # Embedded Python cannot be imported, so its functions render statically.
            functions += [dict(function, language="static-python", where=where)
                          for function in python_functions(path, run)]
        else:
            problems.append(f"{path}{where}: shell {shell!r} has no configured extractor")
    return functions, problems


def discover():
    """Find every function in the tracked sources.

    Returns:
        tuple[list[dict], list[str]]: The functions found, and the problems that
        stop the build, such as a source format without an extractor.

    Example:
        ``functions, problems = discover()``
    """
    listed = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, text=True, check=True).stdout
    functions, problems = [], []
    for path in sorted(set(filter(None, listed.split("\0")))):
        full = ROOT / path
        if path.startswith("docs/site/") or not full.is_file():
            continue  # Generated output derives from these sources; deleted files have no content.
        text = full.read_text(errors="replace")
        first = text.split("\n", 1)[0]
        try:
            if full.suffix in METADATA_SUFFIXES:
                functions += bitbake_functions(path, text)
            elif full.suffix == ".conf" and "conf" in Path(path).parts[:-1]:
                configuration_statements(path, "", text)
            elif full.suffix in (".sh", ".scc", ".machine") or re.match(r"#!.*\b(ba)?sh\b", first):
                # Kernel-cache .scc files are shell fragments, and android-gadget-setup.machine
                # is sourced by a shell script.
                functions += shell_functions(path, "", text)
            elif full.suffix == ".py":
                functions += python_functions(path, text)
            elif path.startswith(".github/workflows/") and full.suffix in (".yml", ".yaml"):
                workflow = yaml.safe_load(text) or {}
                default = ((workflow.get("defaults") or {}).get("run") or {}).get("shell", "bash")
                for job_id, job in (workflow.get("jobs") or {}).items():
                    shell = ((job.get("defaults") or {}).get("run") or {}).get("shell", default)
                    found, failed = run_steps(f"{path} (job {job_id})", job.get("steps"), shell)
                    functions, problems = functions + found, problems + failed
            elif path.startswith(".github/actions/") and full.name in ("action.yml", "action.yaml"):
                runs = (yaml.safe_load(text) or {}).get("runs") or {}
                if runs.get("using") != "composite":
                    problems.append(f"{path}: {runs.get('using')!r} actions have no configured extractor")
                found, failed = run_steps(path, runs.get("steps"), "")
                functions, problems = functions + found, problems + failed
            elif full.suffix in (".yml", ".yaml") and "header" in (config := yaml.safe_load(text) or {}):
                # kas configuration: local_conf_header entries are BitBake configuration.
                for name, snippet in (config.get("local_conf_header") or {}).items():
                    configuration_statements(path, f" (local_conf_header {name})", str(snippet))
            elif full.name == "Makefile":
                # Each recipe line runs in the shell after make turns $$ into $.
                recipes = [line[1:].lstrip("@-+").replace("$$", "$")
                           for line in text.splitlines() if line.startswith("\t")]
                functions += shell_functions(path, " (recipes)", "\n".join(recipes))
            elif full.suffix == ".html" and "<script" not in text.lower():
                pass  # Templates without scripts define no functions.
            elif first.startswith("[") or re.match(r"#.*\n(#.*\n|\n)*\[\w+\]", text):
                # systemd units and drop-ins hold settings; a shell started with -c would hold code.
                if re.search(r"\b(ba)?sh\s+-c\b", text):
                    problems.append(f"{path}: shell code in a systemd unit has no configured extractor")
            elif full.suffix == ".in" and "bootm" in text:
                pass  # U-Boot hush scripts cannot define functions.
            elif full.suffix not in PLAIN_SUFFIXES and full.name not in PLAIN_NAMES:
                problems.append(f"{path}: no function extractor is configured for this format; "
                                "add it to .github/test_reference_coverage.py")
        except (SyntaxError, ValueError) as error:
            problems.append(f"{path}: {error}")
    return functions, problems


def description(doc):
    """Return the ``@description`` text of a shdoc comment block.

    Args:
        doc (str): The comment block, with its ``#`` markers.

    Returns:
        str: The description, joined across its lines, or "" when there is none.

    Example:
        ``description("# @description Say hello.")`` returns ``"Say hello."``.
    """
    text, found = [], False
    for line in doc.splitlines():
        line = re.sub(r"^#\s?", "", line.strip())
        if line.startswith("@"):
            if found:
                break
            found = line.startswith("@description")
            line = line[len("@description"):] if found else ""
        if found:
            text.append(line.strip())
    return " ".join(filter(None, text))


def visible(text, markup=False):
    """Return text as a reader sees it, for comparing a comment with its rendered page.

    Sphinx turns quotes and double hyphens into typographic characters, and
    Markdown drops backticks, so both sides are normalised the same way.

    Args:
        text (str): Comment text, or an HTML page when ``markup`` is True.
        markup (bool): Remove HTML tags and entities first. Defaults to False.

    Returns:
        str: The readable text with plain quotes and hyphens and single spaces.

    Example:
        ``visible("<p>Deploy u-boot-&lt;type&gt;.mbn</p>", markup=True)`` returns ``"Deploy u-boot-<type>.mbn"``.
    """
    if markup:
        text = html.unescape(re.sub(r"<[^>]+>", " ", text))
    for typographic, plain in (("\u2018", "'"), ("\u2019", "'"), ("\u201c", '"'), ("\u201d", '"'),
                               ("\u2013", "--"), ("\u2014", "---"), ("`", "")):
        text = text.replace(typographic, plain)
    return " ".join(text.split())


def google_rst(doc):
    """Convert a Google-style comment or docstring to reStructuredText with napoleon.

    Args:
        doc (str): The documentation text, without comment markers.

    Returns:
        str: reStructuredText with Parameters, Returns, Raises, and Example fields.

    Example:
        ``google_rst("Say hello.\\n\\nExample:\\n    ``f()``")``
    """
    config = Config(napoleon_use_param=False, napoleon_use_rtype=False)
    # Outside a Python domain directive these fields render with their names as written.
    rst = re.sub(r"^:returns:", ":Returns:", str(GoogleDocstring(doc, config)), flags=re.M)
    return re.sub(r"^:raises ", ":Raises ", rst, flags=re.M)


def heading(name):
    """Return a Markdown heading text that shows a function name literally.

    Args:
        name (str): A function name, such as ``__anonymous``.

    Returns:
        str: The name with leading underscores escaped.

    Example:
        ``heading("__anonymous")`` returns ``"\\\\_\\\\_anonymous"``.
    """
    return re.sub(r"(?<![\w])_+", lambda m: "\\_" * len(m.group(0)), name)


class PythonAutodoc:
    """Render Python docstrings with Sphinx autodoc and napoleon.

    autodoc imports each module by its file name from the module's folder, so it
    suits modules whose import has no side effects; docs/source/conf.py mocks the
    BitBake and OpenEmbedded modules they import. Functions nested in other
    functions cannot be imported and are rendered from their docstrings.
    """

    def missing(self, function):
        """Return the required docstring parts a Python function lacks.

        Args:
            function (dict): A function found by ``python_functions``.

        Returns:
            list[str]: The missing parts; empty when the docstring is complete.

        Example:
            ``PythonAutodoc().missing({"doc": ""})`` returns ``["docstring", "Example"]``.
        """
        return [part for part, present in (("docstring", function["doc"].strip()),
                                           ("Example", "Example" in function["doc"])) if not present]

    def page(self, path, functions):
        """Return the reference page for one Python file.

        Args:
            path (str): Source path of a module importable by its file name.
            functions (list[dict]): The functions defined in it.

        Returns:
            str: A MyST page that renders the module with autodoc, followed by
            any nested functions.

        Example:
            ``PythonAutodoc().page(".github/tool.py", functions)``
        """
        page = (f"# {path}\n\n```{{eval-rst}}\n.. automodule:: {Path(path).stem}\n"
                "   :members:\n   :private-members:\n   :special-members: __init__\n   :undoc-members:\n```\n")
        nested = [function for function in functions if function.get("nested")]
        if nested:
            page += "\n## Nested functions\n" + "".join(
                f"\n### {heading(function['name'])}\n\n```{{eval-rst}}\n{google_rst(function['doc'])}\n```\n"
                for function in nested)
        return page

    def rendered(self, function, html):
        """Return whether the built page holds the function's entry.

        Args:
            function (dict): A function found by ``python_functions``.
            html (str): The built reference page.

        Returns:
            bool: True when the page has an anchored entry for the function.

        Example:
            ``PythonAutodoc().rendered(function, html)``
        """
        if function.get("nested"):
            return f'<section id="{make_id(function["name"])}">' in html
        return f'id="{Path(function["path"]).stem}.{function["name"]}"' in html


class Shdoc:
    """Render shell functions with the pinned shdoc, which the Makefile's setup installs.

    shdoc reads the ``@description``, ``@arg`` or ``@noargs``, ``@exitcode``, and
    ``@example`` annotations in the comment block above each definition, and runs
    on GNU Awk. BitBake shell tasks take the same annotations above the task.
    """

    TAGS = (("@description",), ("@arg", "@noargs"), ("@exitcode",), ("@example",))

    def missing(self, function):
        """Return the required annotations a shell function's comment block lacks.

        Args:
            function (dict): A function found by ``shell_functions``.

        Returns:
            list[str]: The missing annotations, or a note that shdoc cannot render
            the name; empty when the function can be rendered completely.

        Example:
            ``Shdoc().missing({"name": "f", "doc": ""})`` returns all four annotations.
        """
        missing = ["/".join(tags) for tags in self.TAGS if not any(tag in function["doc"] for tag in tags)]
        if not re.fullmatch(r"[\w.:-]+", function["name"]):
            missing.append("a name shdoc can render")
        return missing

    def page(self, path, functions):
        """Return shdoc's reference for one source file's shell functions; a shdoc failure stops the build.

        Args:
            path (str): Source path.
            functions (list[dict]): The shell functions defined in it.

        Returns:
            str: Markdown holding shdoc's output.

        Example:
            ``Shdoc().page("ci/build.sh", functions)``
        """
        # Each comment block with a stub definition, so embedded functions render too.
        source = "".join(f"{function['doc']}\n{function['name']}() {{\n    :\n}}\n\n" for function in functions)
        output = subprocess.run(["gawk", "-f", str(ROOT / ".venv/bin/shdoc")], input=source,
                                capture_output=True, text=True, check=True).stdout
        # Outside code blocks, MyST would read a placeholder such as <type> as raw HTML and drop it.
        lines, fenced = [], False
        for line in output.splitlines():
            fenced ^= line.startswith("```")
            lines.append(line if fenced or line.startswith("```") else html.escape(line, quote=False))
        return "\n".join(lines) + "\n"

    def rendered(self, function, html):
        """Return whether the built page holds the function's entry.

        Args:
            function (dict): A function found by ``shell_functions``.
            html (str): The built reference page.

        Returns:
            bool: True when the page has a section for the function that shows its
            whole description.

        Example:
            ``Shdoc().rendered({"name": "f", "doc": "# @description Hi."}, '<section id="f"><p>Hi.</p>')``
            returns ``True``.
        """
        return f'<section id="{make_id(function["name"])}">' in html and visible(description(function["doc"])) in visible(html, markup=True)


class StaticPython:
    """Render Python functions that cannot be imported: BitBake Python and embedded Python.

    autodoc cannot import BitBake metadata or workflow steps, and ``py:function``
    cannot parse override names such as ``populate_packages:prepend``, so each
    function's Google-style comment block or docstring is converted with napoleon
    and rendered under its own heading. A nested BitBake function, or one whose
    comment would fall inside a preceding Python function's body, is documented
    in a ``# @function NAME`` block outside every function body.
    """

    def missing(self, function):
        """Return the required comment parts a BitBake Python function lacks.

        Args:
            function (dict): A function found by ``bitbake_functions``.

        Returns:
            list[str]: The missing parts; empty when the comment is complete.

        Example:
            ``StaticPython().missing({"doc": ""})`` returns ``["comment", "Example"]``.
        """
        return [part for part, present in (("comment", function["doc"].strip()),
                                           ("Example", "Example:" in function["doc"])) if not present]

    def page(self, path, functions):
        """Return the statically rendered Python part of one file's reference page.

        Args:
            path (str): Source path.
            functions (list[dict]): The Python functions defined in it.

        Returns:
            str: A MyST section with one heading and converted comment per function.

        Example:
            ``StaticPython().page("classes/x.bbclass", functions)``
        """
        sections = []
        for function in functions:
            doc = function["doc"]
            if all(line.startswith("#") for line in doc.splitlines()):
                doc = "\n".join(re.sub(r"^# ?", "", line) for line in doc.splitlines())
            sections.append(f"\n### {heading(function['name'])}\n\n```{{eval-rst}}\n{google_rst(doc)}\n```\n")
        return "## Python functions\n" + "".join(sections)

    def rendered(self, function, html):
        """Return whether the built page holds the function's entry.

        Args:
            function (dict): A function found by ``bitbake_functions``.
            html (str): The built reference page.

        Returns:
            bool: True when the page has a section for the function.

        Example:
            ``StaticPython().rendered({"name": "__anonymous"}, '<section id="anonymous">')`` returns ``True``.
        """
        return f'<section id="{make_id(function["name"])}">' in html


# Renderers by language. Each provides missing(function), page(path, functions),
# and rendered(function, html), as PythonAutodoc, Shdoc, and StaticPython do.
RENDERERS = {"python": PythonAutodoc(), "shell": Shdoc(), "static-python": StaticPython()}


def main():
    """Generate the reference pages or check the rendered entries.

    Returns:
        None: Exits with a message when a problem is found.

    Example:
        ``python .github/test_reference_coverage.py check``
    """
    mode = sys.argv[1] if len(sys.argv) == 2 else ""
    if mode not in ("generate", "check"):
        raise SystemExit(__doc__)
    functions, problems = discover()
    for function in functions:
        location = f"{function['path']}:{function['line']}{function['where']}"
        renderer = RENDERERS.get(function["language"])
        if renderer is None:
            problems.append(f"{location}: {function['name']} is a {function['language']} function, and no "
                            f"{function['language']} renderer is configured; add one to RENDERERS")
        elif missing := renderer.missing(function):
            problems.append(f"{location}: {function['name']} is undocumented; missing {', '.join(missing)}")
    if not problems and mode == "generate":
        PAGES.mkdir(parents=True, exist_ok=True)
        for path in sorted({function["path"] for function in functions}):
            defined = [function for function in functions if function["path"] == path]
            if defined[0]["language"] == "python":
                page = RENDERERS["python"].page(path, defined)
            else:
                page = f"# {path}\n\n"
                for language in ("shell", "static-python"):
                    if selected := [function for function in defined if function["language"] == language]:
                        page += RENDERERS[language].page(path, selected)
            # Generated pages follow the extractor's output, not the authored style rules.
            (PAGES / f"{page_name(path)}.md").write_text(f"<!-- markdownlint-disable-file -->\n{page}")
    elif not problems:
        for function in functions:
            built = SITE / f"{page_name(function['path'])}.html"
            content = built.read_text() if built.is_file() else ""
            if not RENDERERS[function["language"]].rendered(function, content):
                problems.append(f"{function['path']}:{function['line']}: {function['name']} has no complete "
                                f"rendered entry in {built.relative_to(ROOT)}")
    for problem in problems:
        print(f"reference coverage: {problem}", file=sys.stderr)
    if problems:
        raise SystemExit(f"Reference coverage failed with {len(problems)} problem(s).")
    print(f"Reference coverage: {len(functions)} function(s) documented"
          + (" and rendered." if mode == "check" else "; pages generated."))


if __name__ == "__main__":
    main()
