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
the renderers; nothing is executed. Python's ast module reads Python files,
tree-sitter-bash reads shell scripts, workflow and composite-action run steps,
and Makefile recipes, and BitBake's own statement parser, pinned by the
Makefile's setup, splits recipes and classes into shell and Python functions.
Adapting a repository means adding its source formats to discover() and a
renderer for each language that defines functions to RENDERERS.
"""
import ast
import html as htmllib
import re
import subprocess
import sys
import textwrap
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
# BitBake's parser, cloned at the revision the Makefile's setup pins.
sys.path.insert(0, str(ROOT / ".venv/bitbake/lib"))
# Formats verified to hold no function definitions: documentation, locks,
# patches to other projects' sources, kernel configuration fragments and
# kernel-cache (.scc) directives, devicetree sources, udev rules, systemd
# units and drop-ins (.conf outside conf/), modprobe settings, a U-Boot
# script template, and keys.
PLAIN_SUFFIXES = (".md", ".txt", ".lock", ".patch", ".cfg", ".scc", ".dts", ".rules",
                  ".service", ".mount", ".conf", ".venus", ".vidc", ".pem", ".cer")
PLAIN_NAMES = ("LICENSE", "CODEOWNERS", ".gitignore", ".env.example", ".markdownlint.yaml",
               "boot.cmd.in", "qbootctl-bless-boot.service.in")
PLAIN_PREFIXES = ("licenses/",)
BITBAKE_SUFFIXES = (".bb", ".bbappend", ".bbclass", ".inc")


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


def comment_block(lines, start):
    """Return the comment lines directly above a line.

    Args:
        lines (list[str]): The file's lines.
        start (int): Zero-based index of the definition line.

    Returns:
        list[str]: The stripped comment lines, top first; empty when there is none.

    Example:
        ``comment_block(["# @description Run.", "f() {"], 1)`` returns ``["# @description Run."]``.
    """
    comments = []
    while start - len(comments) > 0 and lines[start - len(comments) - 1].lstrip().startswith("#"):
        comments.insert(0, lines[start - len(comments) - 1].strip())
    return comments


def shell_functions(path, where, text, prefix="", offset=0):
    """List the shell functions defined in a shell text.

    Args:
        path (str): Source path, used in reports.
        where (str): Location inside the file, such as a workflow step, or "".
        text (str): Shell code.
        prefix (str): Name of the enclosing BitBake function, or "" at file level.
        offset (int): Line number in the file of the text's first line, minus one.

    Returns:
        list[dict]: One entry per function with its name, line, and comment block.
        Functions inside a BitBake function take their documentation from a
        ``# @function`` block, because comments in the body are part of the task.

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
        doc = "" if prefix else "\n".join(comment_block(lines, start))
        functions.append({"language": "shell", "path": path, "where": where, "name": prefix + name,
                          "line": offset + start + 1, "doc": doc})
    return functions


def python_functions(path, text, prefix="", offset=0, language="python"):
    """List the functions and methods defined in Python code.

    Args:
        path (str): Source path, used in reports.
        text (str): Python source.
        prefix (str): Qualified name of the enclosing function, or "".
        offset (int): Line number in the file of the text's first line, minus one.
        language (str): Language recorded for the functions found.

    Returns:
        list[dict]: One entry per function with its qualified name, line,
        docstring, signature, and whether it is nested in another function.

    Raises:
        SyntaxError: The Python parser cannot read the text.

    Example:
        ``python_functions("tool.py", "def f():\\n    pass\\n")`` finds ``f``.
    """
    functions, stack = [], [(ast.parse(text, path), prefix, bool(prefix))]
    while stack:
        node, prefix, nested = stack.pop()
        for child in ast.iter_child_nodes(node):
            is_function = isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef))
            if is_function:
                functions.append({"language": language, "path": path, "where": "", "name": prefix + child.name,
                                  "line": offset + child.lineno, "doc": ast.get_docstring(child) or "",
                                  "signature": f"{child.name}({ast.unparse(child.args)})",
                                  "params": [a.arg for a in child.args.posonlyargs + child.args.args
                                             + child.args.kwonlyargs if a.arg not in ("self", "cls")],
                                  "nested": nested})
            name = prefix + child.name + "." if is_function or isinstance(child, ast.ClassDef) else prefix
            stack.append((child, name, nested or is_function))
    return sorted(functions, key=lambda function: function["line"])


def expression_free(text):
    """Replace BitBake inline Python expressions with a placeholder.

    Args:
        text (str): A BitBake shell function body.

    Returns:
        str: The body with each ``${@...}`` replaced by ``BITBAKE_EXPRESSION``,
        which BitBake substitutes before the shell runs.

    Example:
        ``expression_free("echo ${@d.getVar('PN')}")`` returns ``"echo BITBAKE_EXPRESSION"``.
    """
    out, index = [], 0
    while (start := text.find("${@", index)) >= 0:
        depth, end = 0, start + 1
        while end < len(text):
            depth += {"{": 1, "}": -1}.get(text[end], 0)
            if depth == 0:
                break
            end += 1
        out += [text[index:start], "BITBAKE_EXPRESSION"]
        index = end + 1
    return "".join(out) + text[index:]


def named_blocks(lines, bodies):
    """Find ``# @function NAME`` documentation blocks outside function bodies.

    Args:
        lines (list[str]): The file's lines.
        bodies (list[tuple[int, int]]): One-based first and last lines of each function.

    Returns:
        dict[str, str]: Documentation text by function name, without the ``@function`` line.

    Example:
        ``named_blocks(["# @function f.g", "# @description Run."], [])`` returns
        ``{"f.g": "# @description Run."}``.
    """
    blocks = {}
    for index, line in enumerate(lines):
        match = re.match(r"# @function (\S+)$", line.strip())
        if match and not any(first <= index + 1 <= last for first, last in bodies):
            block = []
            while index + 1 + len(block) < len(lines) and lines[index + 1 + len(block)].lstrip().startswith("#"):
                block.append(lines[index + 1 + len(block)].strip())
            blocks[match[1]] = "\n".join(block)
    return blocks


def bitbake_functions(path, text):
    """List the shell and Python functions in a BitBake recipe, append, class, or include.

    BitBake's statement parser splits the file without evaluating metadata or
    running tasks. Shell bodies go to the shell parser and Python bodies to
    Python's parser, so functions nested in a task are found too.

    Args:
        path (str): Source path, used in reports.
        text (str): BitBake metadata.

    Returns:
        list[dict]: One entry per function. A function's documentation is the
        comment block directly above its definition, or a ``# @function NAME``
        block when that comment would fall inside another function's body.

    Raises:
        ValueError: BitBake's parser or an embedded-language parser cannot read the file.

    Example:
        ``bitbake_functions("recipes-x/x/x.bb", "do_install() {\\n    :\\n}\\n")`` finds ``do_install``.
    """
    import bb.parse
    from bb.parse import ast as bbast
    from bb.parse.parse_py import BBHandler
    statements, starts = bbast.StatementGroup(), []
    BBHandler.__infunc__, BBHandler.__inpython__, BBHandler.__body__, BBHandler.__residue__ = [], False, [], []
    try:
        lines = text.splitlines()
        for number, line in enumerate(lines + [""], 1):
            BBHandler.feeder(number, line.rstrip(), path, Path(path).name, statements, eof=number > len(lines))
            # Record where each shell/Python function or Python def begins.
            if (BBHandler.__infunc__ and BBHandler.__infunc__[2] == number
                    or BBHandler.__inpython__ and len(BBHandler.__body__) == 1):
                starts.append(number)
        if BBHandler.__infunc__ or BBHandler.__residue__:
            raise ValueError(f"{path}: BitBake's parser found an unclosed function or expression")
    except (bb.parse.ParseError, bb.BBHandledException) as error:
        raise ValueError(f"{path}: BitBake's parser cannot read it: {error}") from error
    nodes = [node for node in statements if isinstance(node, (bbast.MethodNode, bbast.PythonMethodNode))]
    bodies = [(start, start + len(node.body) - (0 if isinstance(node, bbast.MethodNode) else 1))
              for start, node in zip(starts, nodes)]
    named, functions = named_blocks(lines, bodies), []
    for (start, last), node in zip(bodies, nodes):
        above = comment_block(lines, start - 1)
        inside = any(first <= start - len(above) <= end for first, end in bodies if (first, end) != (start, last))
        if isinstance(node, bbast.PythonMethodNode):
            found = python_functions(path, "\n".join(node.body), offset=start - 1, language="bitbake-python")
            found[0]["where"] = ""
        elif node.python:
            body = textwrap.dedent("\n".join(node.body))
            try:
                found = python_functions(path, body, node.func_name + ".", start, "bitbake-python")
            except SyntaxError as error:
                raise ValueError(f"{path}:{start}: Python's parser cannot read {node.func_name}: {error}") from error
            found.insert(0, {"language": "bitbake-python", "path": path, "where": "", "name": node.func_name,
                             "line": start, "signature": f"python {node.func_name}()", "params": [],
                             "nested": False})
        else:
            found = [{"language": "shell", "path": path, "where": "", "name": node.func_name, "line": start}]
            found += shell_functions(path, f" (in {node.func_name})", expression_free("\n".join(node.body)),
                                     node.func_name + ".", start)
        for function in found:
            if function is found[0]:
                function["doc"] = named.get(function["name"], "" if inside else "\n".join(above))
            else:
                function["doc"] = named.get(function["name"], "")
            if function["language"] == "bitbake-python":
                function["doc"] = "\n".join(re.sub(r"^# ?", "", line) for line in function["doc"].splitlines())
        functions += found
    return functions


def bitbake_configuration(path, text, where=""):
    """Check that BitBake configuration text holds only statements its parser accepts.

    BitBake configuration files cannot define functions; their parser rejects
    any line it cannot read, so a definition there is reported instead of skipped.

    Args:
        path (str): Source path, used in reports.
        text (str): BitBake configuration, such as a ``.conf`` file or a kas
            ``local_conf_header`` entry.
        where (str): Location inside the file, or "".

    Raises:
        ValueError: The configuration parser cannot read a line.

    Example:
        ``bitbake_configuration("conf/layer.conf", 'BBPATH .= ":${LAYERDIR}"')`` returns ``None``.
    """
    import bb.parse
    from bb.parse import ast as bbast
    from bb.parse.parse_py import ConfHandler
    statements, joined = bbast.StatementGroup(), ""
    for number, line in enumerate(text.splitlines(), 1):
        joined += line.rstrip()
        if joined.endswith("\\"):
            joined = joined[:-1]
            continue
        if joined.strip() and not joined.lstrip().startswith("#"):
            try:
                ConfHandler.feeder(number, joined.strip(), path, statements, baseconfig=True)
            except bb.parse.ParseError as error:
                raise ValueError(f"{path}{where}:{number}: BitBake configuration cannot define functions or "
                                 f"hold this statement, so no extractor is configured for it: {joined.strip()!r}"
                                 ) from error
        joined = ""


def step_functions(path, owner, steps, default):
    """List the functions defined in the run steps of a workflow job or composite action.

    Args:
        path (str): Source path, used in reports.
        owner (str): The job or action, used in reports.
        steps (list[dict]): The steps.
        default (str): The shell used when a step names none.

    Returns:
        tuple[list[dict], list[str]]: The functions found, and problems with
        steps whose language has no configured extractor.

    Example:
        ``step_functions("action.yml", "action", [{"run": "f() { :; }"}], "bash")`` finds ``f``.
    """
    functions, problems = [], []
    for number, step in enumerate(steps or [], 1):
        where = f" ({owner}, step {number})"
        if "run" not in step:
            continue
        shell = str(step.get("shell", default))
        # GitHub substitutes expressions before the shell runs.
        run = re.sub(r"\$\{\{.*?\}\}", "GITHUB_EXPRESSION", str(step["run"]))
        if re.match(r"(ba)?sh\b", shell):
            functions += shell_functions(path, where, run)
        elif shell == "python":
            try:
                found = python_functions(path, run, language="embedded-python")
            except SyntaxError as error:
                raise ValueError(f"{path}{where}: Python's parser cannot read it: {error}") from error
            functions += [dict(function, where=where) for function in found]
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
        if path.startswith("docs/site/") or not full.is_file() or full.is_symlink():
            continue  # Generated output and links derive from other sources; deleted files have no content.
        text = full.read_text(errors="replace")
        try:
            if (full.suffix in (".sh", ".machine") or re.match(r"#!.*\b(ba)?sh\b", text.split("\n", 1)[0])):
                functions += shell_functions(path, "", text)
            elif full.suffix == ".py":
                functions += python_functions(path, text)
            elif full.suffix in BITBAKE_SUFFIXES:
                functions += bitbake_functions(path, text)
            elif full.suffix == ".conf" and path.startswith("conf/"):
                bitbake_configuration(path, text)
            elif full.suffix in (".yml", ".yaml") and path.startswith(".github/workflows/"):
                workflow = yaml.safe_load(text) or {}
                default = ((workflow.get("defaults") or {}).get("run") or {}).get("shell", "bash")
                for job_id, job in (workflow.get("jobs") or {}).items():
                    shell = ((job.get("defaults") or {}).get("run") or {}).get("shell", default)
                    found, failed = step_functions(path, f"job {job_id}", job.get("steps"), shell)
                    functions, problems = functions + found, problems + failed
            elif full.name in ("action.yml", "action.yaml") and path.startswith(".github/actions/"):
                action = (yaml.safe_load(text) or {}).get("runs") or {}
                found, failed = step_functions(path, "action", action.get("steps"), "bash")
                functions, problems = functions + found, problems + failed
            elif full.suffix in (".yml", ".yaml") and "header" in (config := yaml.safe_load(text) or {}):
                # kas configuration: its conf headers are BitBake configuration.
                for key in ("local_conf_header", "bblayers_conf_header"):
                    for name, value in (config.get(key) or {}).items():
                        bitbake_configuration(path, str(value), f" ({key} {name})")
            elif full.name == "Makefile":
                # Each recipe line runs in the shell after make turns $$ into $.
                recipes = [line[1:].lstrip("@-+").replace("$$", "$")
                           for line in text.splitlines() if line.startswith("\t")]
                functions += shell_functions(path, " (recipes)", "\n".join(recipes))
            elif full.suffix == ".html" and "<script" not in text.lower():
                pass  # Templates without scripts define no functions.
            elif (full.suffix not in PLAIN_SUFFIXES and full.name not in PLAIN_NAMES
                  and not path.startswith(PLAIN_PREFIXES)):
                problems.append(f"{path}: no function extractor is configured for this format; "
                                "add it to .github/test_reference_coverage.py")
        except (SyntaxError, ValueError, yaml.YAMLError) as error:
            problems.append(f"{path}: {error}")
    return functions, problems


def static_python_section(function):
    """Return a reference section for a Python function that autodoc cannot import.

    Napoleon converts the Google-style comment or docstring to reStructuredText
    without importing anything.

    Args:
        function (dict): A function found by ``python_functions`` or ``bitbake_functions``.

    Returns:
        str: A Markdown section headed by the function's name, with its signature.

    Example:
        ``static_python_section({"name": "f", "signature": "f(d)", "doc": "Run."})``
    """
    body = str(GoogleDocstring(function["doc"], Config(napoleon_use_param=False, napoleon_use_rtype=False)))
    return (f"### {function['name']}\n\n```python\n{function['signature']}\n```\n\n"
            f"```{{eval-rst}}\n{body}\n```\n\n")


def section_text(function, html):
    """Return the plain text of a function's rendered section.

    Args:
        function (dict): A function with a ``name``.
        html (str): The built reference page.

    Returns:
        str: The section's text with tags removed, typographic quotes and dashes
        made plain, and whitespace collapsed; empty when the section is missing.

    Example:
        ``section_text({"name": "f"}, '<section id="f"><p>Run it.</p>')`` returns ``"Run it."``.
    """
    start = html.find(f'<section id="{make_id(function["name"])}">')
    if start < 0:
        return ""
    end = html.find("<section", start + 1)
    text = htmllib.unescape(re.sub(r"<[^>]+>", " ", html[start:end if end > 0 else len(html)]))
    text = text.translate(str.maketrans("\u2018\u2019\u201c\u201d\u2013\u2014", "''\"\"--"))
    return " ".join(text.split())


def shows_purpose(purpose, function, html):
    """Return whether a function's description renders without losing characters.

    Markup in a comment, such as a pair of ``*`` in file patterns, would otherwise
    turn into emphasis and silently change the rendered text.

    Args:
        purpose (str): The function's description paragraph.
        function (dict): The function, with a ``name``.
        html (str): The built reference page.

    Returns:
        bool: True when the purpose, without code quoting, appears in the section.

    Example:
        ``shows_purpose("Copy *.bin files.", {"name": "f"}, html)``
    """
    expected = " ".join(re.sub(r"`+", "", purpose).replace("--", "-").split())
    return bool(expected) and expected in section_text(function, html).replace("--", "-")


class PythonAutodoc:
    """Render Python docstrings with Sphinx autodoc and napoleon.

    autodoc imports each module by file name, so it suits modules whose import
    has no side effects; conf.py mocks the BitBake and OpenEmbedded modules they
    import. Functions nested in other functions are rendered statically.
    """

    def missing(self, function):
        """Return the required docstring parts a Python function lacks.

        Args:
            function (dict): A function found by ``python_functions``.

        Returns:
            list[str]: The missing parts; empty when the docstring is complete.

        Example:
            ``PythonAutodoc().missing({"doc": "", "params": []})`` returns ``["docstring", "Example"]``.
        """
        return [part for part, present in (("docstring", function["doc"].strip()),
                                           ("Args", "Args:" in function["doc"] or not function["params"]),
                                           ("Example", "Example" in function["doc"])) if not present]

    def page(self, path, functions):
        """Return the reference content for one Python file.

        Args:
            path (str): Source path of a module importable by its file name.
            functions (list[dict]): The functions defined in it.

        Returns:
            str: MyST content that renders the module with autodoc.

        Example:
            ``PythonAutodoc().page(".github/tool.py", functions)``
        """
        nested = [function for function in functions if function["nested"]]
        return (f"```{{eval-rst}}\n.. automodule:: {Path(path).stem}\n"
                "   :members:\n   :private-members:\n   :undoc-members:\n   :special-members: __init__\n```\n\n"
                + ("## Nested functions\n\n" if nested else "")
                + "".join(static_python_section(function) for function in nested))

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
        if function["nested"]:
            return f'<section id="{make_id(function["name"])}">' in html
        return f'id="{Path(function["path"]).stem}.{function["name"]}"' in html


class BitBakePython:
    """Render BitBake Python functions statically; autodoc cannot import BitBake metadata.

    The documentation is the Google-style comment block above the definition,
    or a ``# @function NAME`` block for a function nested in a Python task.
    """

    def missing(self, function):
        """Return the required documentation parts a BitBake Python function lacks.

        Args:
            function (dict): A function found by ``bitbake_functions``.

        Returns:
            list[str]: The missing parts; empty when the comment is complete.

        Example:
            ``BitBakePython().missing({"doc": "", "params": ["d"]})`` returns
            ``["comment", "Args", "Example"]``.
        """
        return [part for part, present in (("comment", function["doc"].strip()),
                                           ("Args", "Args:" in function["doc"] or not function["params"]),
                                           ("Example", "Example:" in function["doc"])) if not present]

    def page(self, path, functions):
        """Return the reference content for a BitBake file's Python functions.

        Args:
            path (str): Source path.
            functions (list[dict]): Its BitBake Python functions.

        Returns:
            str: A Markdown section per function.

        Example:
            ``BitBakePython().page("classes/x.bbclass", functions)``
        """
        return "## Python functions\n\n" + "".join(static_python_section(function) for function in functions)

    def rendered(self, function, html):
        """Return whether the built page holds the function's entry.

        Args:
            function (dict): A function found by ``bitbake_functions``.
            html (str): The built reference page.

        Returns:
            bool: True when the page has a section for the function.

        Example:
            ``BitBakePython().rendered({"name": "do_x", "doc": "Run."}, '<section id="do-x">Run.')``
            returns ``True``.
        """
        return shows_purpose(function["doc"].strip().split("\n\n")[0], function, html)


class Shdoc:
    """Render shell functions with the pinned shdoc, which the Makefile's setup installs.

    shdoc reads the ``@description``, ``@arg`` or ``@noargs``, ``@exitcode``, and
    ``@example`` annotations in the comment block above each definition, and runs
    on GNU Awk.
    """

    TAGS = (("@description",), ("@arg", "@noargs"), ("@exitcode",), ("@example",))

    def missing(self, function):
        """Return the required annotations a shell function's comment block lacks.

        Args:
            function (dict): A function found by ``shell_functions``.

        Returns:
            list[str]: The missing annotations; empty when the function can be
            rendered completely.

        Example:
            ``Shdoc().missing({"name": "f", "doc": ""})`` returns all four annotations.
        """
        return ["/".join(tags) for tags in self.TAGS if not any(tag in function["doc"] for tag in tags)]

    def page(self, path, functions):
        """Return the reference content for one source file; a shdoc failure stops the build.

        Args:
            path (str): Source path.
            functions (list[dict]): The shell functions defined in it.

        Returns:
            str: shdoc's Markdown output.

        Example:
            ``Shdoc().page("ci/build.sh", functions)``
        """
        # shdoc reads names of letters, digits, and _-:.; a BitBake name can also
        # hold ${VAR}, so shdoc sees a stub name that is swapped back afterwards.
        stubs = {function["name"]: re.sub(r"[^\w.:-]", "", function["name"]) for function in functions}
        # Each comment block with a stub definition, so embedded functions render too.
        source = "".join(f"{self.escaped(function['doc'])}\n{stubs[function['name']]}() {{\n    :\n}}\n\n"
                         for function in functions)
        output = subprocess.run(["gawk", "-f", str(ROOT / ".venv/bin/shdoc")], input=source,
                                capture_output=True, text=True, check=True).stdout
        for name, stub in stubs.items():
            output = output.replace(f"### {stub}\n", f"### {name}\n").replace(f"[{stub}]", f"[{name}]")
        return output + "\n"

    @staticmethod
    def escaped(doc):
        """Escape Markdown markup in a comment block, outside its example.

        shdoc copies descriptions into Markdown as they are, so ``*`` in a file
        pattern or ``<name>`` in a path would become emphasis or HTML.

        Args:
            doc (str): The comment block.

        Returns:
            str: The block with ``*`` and ``<`` escaped in every line before ``@example``
            and in tag lines after it.

        Example:
            ``Shdoc.escaped("# @description Copy *.bin files.")`` returns
            ``"# @description Copy \\*.bin files."``.
        """
        lines, example = [], False
        for line in doc.splitlines():
            if re.match(r"#\s*@", line):
                example = line.strip().startswith("# @example")
            lines.append(line if example else re.sub(r"([*<])", r"\\\1", line))
        return "\n".join(lines)

    def rendered(self, function, html):
        """Return whether the built page holds the function's entry with its purpose intact.

        Args:
            function (dict): A function found by ``shell_functions``.
            html (str): The built reference page.

        Returns:
            bool: True when the page has a section for the function whose text
            includes its whole ``@description``.

        Example:
            ``Shdoc().rendered({"name": "_is_dir", "doc": "# @description Check."},
            '<section id="is-dir">Check.')`` returns ``True``.
        """
        purpose = re.search(r"@description\s+(.*(?:\n#(?!\s*@).*)*)", function["doc"])
        text = purpose and re.sub(r"\n#[ \t]?", " ", purpose[1])
        return bool(text) and shows_purpose(text, function, html)


# Renderers by language. Each provides missing(function), page(path, functions),
# and rendered(function, html), as PythonAutodoc and Shdoc do.
RENDERERS = {"python": PythonAutodoc(), "shell": Shdoc(), "bitbake-python": BitBakePython()}


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
            page = f"# {path}\n\n"
            for language, renderer in RENDERERS.items():
                defined = [function for function in functions if function["path"] == path
                           and function["language"] == language]
                page += renderer.page(path, defined) if defined else ""
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
