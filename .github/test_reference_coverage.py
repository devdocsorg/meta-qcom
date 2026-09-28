# Copyright (c) 2026 DevDocs
# SPDX-License-Identifier: BSD-3-Clause
"""Generate the native function reference and check its coverage.

Sphinx loads this file as an extension. Before Sphinx reads its sources, the
extension finds every function in the tracked files, fails on undocumented
functions or unsupported formats, and writes one Markdown page per source file
to ``docs/source/contributing/.generated/``. Run this file after the build to
check that every function has a rendered entry.

BitBake metadata is split with BitBake's own statement parser, shell code with
tree-sitter-bash, and Python with the standard ``ast`` module. Shell functions
carry shdoc tags. Python functions carry a docstring or, where the code cannot
change, a Google-style comment block that the reference reads as pydoc does.
Anonymous BitBake Python blocks run at parse time and have no name to
reference. Nested Python functions need documentation but render only as part
of their enclosing function.
"""
import ast
import inspect
import os
from pathlib import Path
import re
import subprocess
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/source/contributing/.generated'
SITE = ROOT / 'docs/site/contributing/.generated'
TOOLS = ROOT / '.docs-tools'
SOURCE = 'https://github.com/devdocsorg/meta-qcom/blob/docs/layer-documentation/'
BITBAKE = {'.bb', '.bbappend', '.bbclass', '.inc'}
# Formats without function definitions: patches, kernel configuration
# fragments, device trees, keys, udev and systemd units, U-Boot scripts,
# modprobe files (.venus, .vidc), licences, and repository metadata.
DATA = {'.patch', '.cfg', '.scc', '.md', '.pem', '.cer', '.dts', '.rules', '.service',
        '.mount', '.in', '.lock', '.txt', '.html', '.venus', '.vidc', '.example'}
DATA_NAMES = {'.gitignore', 'CODEOWNERS', 'Makefile', 'LICENSE'}


class ReferenceError(Exception):
    """Report undocumented functions or formats the reference cannot read."""


def comments_above(lines, index):
    """Return the comment block that ends just above a line, without ``#``.

    Example:
        ``comments_above(['# Say hi.', 'hi() {'], 1)`` returns ``['Say hi.']``.
    """
    block = []
    while index > 0 and lines[index - 1].lstrip().startswith('#'):
        index -= 1
        block.insert(0, re.sub(r'^\s*# ?', '', lines[index]))
    return block


def record(path, name, line, kind, documented, render=True):
    """Return one function record for the coverage checks.

    Example:
        ``record('ci/a.sh', 'f', 3, 'shell', True)``
    """
    return {'path': path, 'name': name, 'line': line, 'kind': kind,
            'documented': documented, 'render': render}


def shell_definitions(path, text, offset=0):
    """Find shell functions with tree-sitter-bash and check their shdoc tags.

    Args:
        path (str): Repository-relative source path.
        text (str): Shell source, such as a script or a BitBake task body.
        offset (int): File line number of the text's first line, minus one.

    Returns:
        list[dict]: Records whose ``documented`` flag requires shdoc's
        ``@description`` and ``@example`` tags.

    Example:
        ``shell_definitions('ci/a.sh', 'f() { :; }')[0]['documented']`` is ``False``.
    """
    import tree_sitter
    import tree_sitter_bash
    parser = tree_sitter.Parser(tree_sitter.Language(tree_sitter_bash.language()))
    lines, found, pending = text.splitlines(), [], [parser.parse(text.encode()).root_node]
    while pending:
        node = pending.pop()
        if node.type == 'function_definition':
            line = node.start_point[0]
            tags = {c.split(' ')[0] for c in comments_above(lines, line)}
            found.append(record(path, node.child_by_field_name('name').text.decode(), offset + line + 1,
                                'shell', {'@description', '@example'} <= tags))
        pending.extend(node.children)
    return sorted(found, key=lambda item: item['line'])


def python_definitions(path, tree, lines, offset=0):
    """Find Python functions, methods, and nested functions in a syntax tree.

    Args:
        path (str): Repository-relative source path.
        tree (ast.Module): Parsed source.
        lines (list[str]): Lines of the file that holds the source.
        offset (int): File line number of the source's first line, minus one.

    Returns:
        list[dict]: Records that require a purpose and an ``Example:`` section
        in the docstring or comment block; nested functions do not render.

    Example:
        ``python_definitions('a.py', ast.parse('def f(): pass'), ['def f(): pass'])``
    """
    found = []

    def visit(node, prefix, nested):
        """Record the functions below a node, qualified by class and function.

        Example:
            ``visit(tree, '', False)`` walks a whole module.
        """
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                first = min([child.lineno] + [d.lineno for d in child.decorator_list]) - 1
                text = '\n'.join([ast.get_docstring(child) or ''] + comments_above(lines, offset + first))
                found.append(record(path, prefix + child.name, offset + child.lineno, 'python',
                                    bool(re.search(r'^\s*Examples?:', text, re.M)), not nested))
                visit(child, prefix + child.name + '.', True)
            else:
                visit(child, prefix + child.name + '.' if isinstance(child, ast.ClassDef) else prefix, nested)
    visit(tree, '', False)
    return found


def check_bitbake_conf(path, text):
    """Reject function definitions in BitBake configuration text.

    Args:
        path (str): Source path, with the kas entry name for kas fragments.
        text (str): A ``.conf`` file or a kas ``local_conf_header`` entry.

    Raises:
        ReferenceError: If BitBake cannot read a line as configuration.

    Example:
        ``check_bitbake_conf('conf/layer.conf', 'A = "1"')`` returns ``None``.
    """
    from bb.parse import ParseError
    from bb.parse.ast import StatementGroup
    from bb.parse.parse_py import ConfHandler
    statements, pending = StatementGroup(), ''
    for number, line in enumerate(text.splitlines(), 1):
        line = pending + line.rstrip()
        pending = line[:-1] if line.endswith('\\') else ''
        if pending or not line.strip() or line.lstrip().startswith('#'):
            continue
        try:
            # BitBake reads layer.conf as base configuration, which allows addpylib.
            ConfHandler.feeder(number, line, path, statements, baseconfig=path.endswith('layer.conf'))
        except ParseError as error:
            raise ReferenceError(f'{path}:{number}: unsupported definition in BitBake '
                                 f'configuration; configure extraction for it ({error})') from None


def bitbake_definitions(path):
    """Find shell and Python functions in BitBake recipe metadata.

    Returns:
        tuple[list[dict], list[str], list[tuple]]: Records, shdoc input for
        each shell function, and ``(name, signature, comment)`` per Python one.

    Example:
        ``bitbake_definitions('classes/linux-qcom-dtbbin.bbclass')``
    """
    from bb.parse import ast as bbast
    from bb.parse.parse_py import BBHandler
    BBHandler.__infunc__, BBHandler.__body__, BBHandler.__residue__ = [], [], []
    BBHandler.__inpython__ = False
    lines = (ROOT / path).read_text().splitlines()
    found, shell, python = [], [], []
    for node in BBHandler.get_statements(path, str(ROOT / path), os.path.basename(path)):
        if not isinstance(node, (bbast.MethodNode, bbast.PythonMethodNode)):
            continue
        start = node.lineno - len(node.body) - 1
        if isinstance(node, bbast.PythonMethodNode):
            if not lines[start].startswith('def '):
                raise ReferenceError(f'{path}:{start + 1}: cannot locate a Python definition')
            tree = ast.parse('\n'.join(node.body))
            found += python_definitions(path, tree, lines, start)
            name = tree.body[0].name
            python.append((name, f'{name}({ast.unparse(tree.body[0].args)})', comments_above(lines, start)))
            continue
        name, body = node.func_name, node.body[:-1]
        header = BBHandler.__func_start_regexp__.match(lines[start])
        if not header or (header.group('func') or '__anonymous') != name:
            raise ReferenceError(f'{path}:{start + 1}: cannot locate the definition of {name}')
        if name == '__anonymous':
            continue
        comment = comments_above(lines, start)
        if node.python:
            # Parse the task body as BitBake compiles it: a function of d.
            records = python_definitions(path, ast.parse('def _(d):\n' + '\n'.join(body)), lines, start)
            for item in records:
                item['name'] = name + item['name'][1:]
            found += records
            python.append((name, f'{name}(d)', comment))
        else:
            tags = {c.split(' ')[0] for c in comment}
            found.append(record(path, name, start + 1, 'shell', {'@description', '@example'} <= tags))
            found += shell_definitions(path, '\n'.join(body), start + 1)
            shell.append('\n'.join(['# ' + c if c else '#' for c in comment] + [f'{name}() {{', *body, '}']))
    return found, shell, python


def workflow_definitions(path, text):
    """Find functions in the ``run`` blocks of a GitHub Actions file.

    Returns:
        tuple[list[dict], list[str]]: Records and the shell ``run`` blocks.

    Raises:
        ReferenceError: If a Python ``run`` block defines a function.

    Example:
        ``workflow_definitions('w.yml', 'steps:\\n  - run: echo hi\\n')``
    """
    found, blocks, pending = [], [], [yaml.compose(text)]
    while pending:
        node = pending.pop()
        if isinstance(node, yaml.MappingNode):
            values = {key.value: value for key, value in node.value if isinstance(key, yaml.ScalarNode)}
            run, shell = values.get('run'), getattr(values.get('shell'), 'value', '')
            if isinstance(run, yaml.ScalarNode) and shell == 'python':
                if any(isinstance(n, ast.FunctionDef) for n in ast.walk(ast.parse(run.value))):
                    raise ReferenceError(f'{path}:{run.start_mark.line + 1}: unsupported Python function '
                                         'in a run block; configure extraction for it')
            elif isinstance(run, yaml.ScalarNode):
                blocks.append(run.value)
                found += shell_definitions(path, run.value, run.start_mark.line + (run.style in ('|', '>')))
            pending += [value for _, value in node.value]
        elif isinstance(node, yaml.SequenceNode):
            pending += node.value
    return found, blocks


def classify(path):
    """Return a tracked file's format, or fail when none is configured.

    Example:
        ``classify('conf/layer.conf')`` returns ``'conf'``.
    """
    file = ROOT / path
    suffix = file.suffix
    first = file.open(errors='replace').readline() if file.is_file() else ''
    if path.startswith('docs/site/'):
        return 'data'
    if suffix in BITBAKE:
        return 'bitbake'
    if suffix == '.conf':
        # BitBake reads conf/ files; others are installed systemd or modprobe files.
        return 'conf' if 'conf' in Path(path).parts[:-1] else 'data'
    if suffix in ('.yml', '.yaml'):
        if path.startswith(('.github/workflows/', '.github/actions/')):
            return 'workflow'
        return 'kas' if path.startswith('ci/') else 'data'
    # .machine files are shell fragments that android-gadget-setup sources.
    if suffix in ('.sh', '.machine') or re.match(r'#!\S*(/|env )(ba|da)?sh\b', first):
        return 'shell'
    if suffix == '.py' or re.match(r'#!\S*python', first):
        return 'python'
    if suffix in DATA or file.name in DATA_NAMES or file.name.startswith('LICENSE'):
        return 'data'
    raise ReferenceError(f'{path}: unsupported source format; configure its native extractor '
                         'or classify it as data in .github/test_reference_coverage.py')


def discover():
    """Find every function in the tracked files and what each page renders.

    Returns:
        tuple[list[dict], dict]: Function records, and page content by path.

    Raises:
        ReferenceError: If a function is undocumented or a format unsupported.

    Example:
        ``functions, pages = discover()``
    """
    for extra in (TOOLS / 'bitbake/lib', TOOLS / 'oe-core/meta/lib', ROOT / 'lib'):
        if str(extra) not in sys.path:
            sys.path.append(str(extra))
    if not (TOOLS / 'bitbake/lib/bb').is_dir() or not (TOOLS / 'shdoc').is_file():
        raise ReferenceError('The pinned BitBake parser or shdoc is missing; '
                             'run "make -f docs/source/Makefile setup"')
    found, pages, problems = [], {}, []
    for entry in subprocess.check_output(['git', 'ls-files', '-s'], cwd=ROOT, text=True).splitlines():
        mode, path = entry.split()[0], entry.split('\t', 1)[1]
        if mode == '120000':
            continue  # Symlinks are documented through their targets.
        try:
            kind = classify(path)
            text = (ROOT / path).read_text(errors='replace') if kind != 'data' else ''
            records, page = [], {}
            if kind == 'bitbake':
                records, shell, python = bitbake_definitions(path)
                page = {'shell': shell, 'python': python}
            elif kind == 'conf':
                check_bitbake_conf(path, text)
            elif kind == 'kas':
                for key, value in ((yaml.safe_load(text) or {}).get('local_conf_header') or {}).items():
                    check_bitbake_conf(f'{path} (local_conf_header {key})', value or '')
            elif kind == 'workflow':
                records, blocks = workflow_definitions(path, text)
                page = {'shell': blocks}
            elif kind == 'shell':
                records, page = shell_definitions(path, text), {'shell': [text]}
            elif kind == 'python':
                records, page = python_definitions(path, ast.parse(text), text.splitlines()), {'module': path}
        except (ReferenceError, SyntaxError, yaml.YAMLError) as error:
            problems.append(str(error))
            continue
        except Exception as error:  # BitBake ParseError and other parser failures.
            problems.append(f'{path}: cannot parse ({error}); fix the syntax or configure extraction')
            continue
        problems += [f"{r['path']}:{r['line']}: undocumented function {r['name']}; add "
                     + ('shdoc @description and @example tags' if r['kind'] == 'shell'
                        else 'a docstring or comment with an Example: section')
                     for r in records if not r['documented']]
        found += records
        if records:
            pages[path] = page
    if problems:
        raise ReferenceError('Function reference coverage failed:\n' + '\n'.join(problems))
    return found, pages


def module_name(path):
    """Return the import name of a Python file: dotted under ``lib/``, else its stem.

    Example:
        ``module_name('lib/qcom/dtb_only_fitimage.py')`` returns ``'qcom.dtb_only_fitimage'``.
    """
    parts = Path(path).with_suffix('').parts
    return '.'.join(parts[1:]) if parts[0] == 'lib' else parts[-1]


def generate(app):
    """Write every reference page before Sphinx reads its sources.

    Args:
        app (sphinx.application.Sphinx): The running Sphinx application.

    Raises:
        ReferenceError: If discovery or shdoc fails.

    Example:
        Sphinx calls ``generate(app)`` on its ``builder-inited`` event.
    """
    from sphinx.ext.napoleon.docstring import GoogleDocstring
    _, pages = discover()
    OUT.mkdir(parents=True, exist_ok=True)
    for stale in OUT.glob('*.md'):
        stale.unlink()
    for path, page in sorted(pages.items()):
        text = [f'# {Path(path).name}', '', f'Source: [{path}]({SOURCE}{path})', '']
        if page.get('shell'):
            result = subprocess.run(['gawk', '-f', str(TOOLS / 'shdoc')], input='\n\n'.join(page['shell']),
                                    capture_output=True, text=True)
            if result.returncode:
                raise ReferenceError(f'{path}: shdoc failed: {result.stderr}')
            text.append(result.stdout.strip())
        if page.get('python'):
            text += ['', '## Python functions', '']
            for name, signature, comment in page['python']:
                body = str(GoogleDocstring(comment, app.config, what='function')).splitlines()
                text += [f'### {name}', '', '```{eval-rst}', f'.. py:function:: {signature}', '   :no-index:',
                         '', *('   ' + line if line else '' for line in body), '```', '']
        if page.get('module'):
            if not path.startswith('lib/'):
                sys.path.append(str(ROOT / Path(path).parent))
            text += ['```{eval-rst}', f'.. automodule:: {module_name(path)}', '   :members:',
                     '   :private-members:', '   :undoc-members:', '   :special-members: __init__', '```']
        (OUT / (path.replace('/', '-') + '.md')).write_text('\n'.join(text).rstrip() + '\n')


def comment_docstring(app, what, name, obj, options, lines):
    """Make a plain-text docstring safe for reST and append the comment block above it.

    Words such as ``qcom_`` would become reST references and indented lists
    would be errors, except under Google-style headers such as ``Args:``.

    Example:
        A method with only ``# Return the root node.`` above it renders that sentence.
    """
    if what not in ('class', 'function', 'method'):
        return
    safe, indent = [], 0
    for line in lines:
        current = len(line) - len(line.lstrip())
        if line.strip() and safe and safe[-1].strip() and current > indent \
                and not re.fullmatch(r'\s*[A-Z][a-z]+( [a-z]+)?:\s*', safe[-1]):
            safe.append('')
        safe.append(re.sub(r'(\w)_(?=\W|$)', r'\1\\_', line))
        indent = current if line.strip() else indent
    extra = [re.sub(r'^\s*# ?', '', line) for line in (inspect.getcomments(obj) or '').splitlines()]
    lines[:] = safe + ([''] if safe and extra else []) + extra


def skip_data(app, what, name, obj, skip, options):
    """Leave data attributes out of the reference; it documents functions and classes.

    Example:
        ``skip_data(app, 'class', 'COMPAT_SKIP_PATTERNS', set(), False, {})`` returns ``True``.
    """
    return True if not callable(obj) else None


def setup(app):
    """Register reference generation and comment docstrings with Sphinx.

    Example:
        ``extensions = ["test_reference_coverage"]`` in ``conf.py``.
    """
    app.connect('builder-inited', generate)
    # Run before napoleon so comment blocks get the same section parsing.
    app.connect('autodoc-process-docstring', comment_docstring, priority=400)
    app.connect('autodoc-skip-member', skip_data)
    return {'parallel_read_safe': True}


def main():
    """Exit with status 1 when a discovered function has no entry in the built site.

    Example:
        ``.venv/bin/python .github/test_reference_coverage.py`` after ``sphinx-build``.
    """
    from docutils.nodes import make_id
    found, _ = discover()
    missing = []
    for item in (r for r in found if r['render']):
        page = SITE / (item['path'].replace('/', '-') + '.html')
        html = page.read_text() if page.is_file() else ''
        anchor = (f"{module_name(item['path'])}.{item['name']}" if item['path'].endswith('.py')
                  else make_id(item['name']))
        if not re.search(f'id="{re.escape(anchor)}(-[0-9]+)?"', html):
            missing.append(f"{item['path']}:{item['line']}: missing rendered entry for {item['name']}")
    if missing:
        sys.exit('Function reference coverage failed:\n' + '\n'.join(missing))
    print(f'Function reference: {len(found)} functions documented and rendered')


if __name__ == '__main__':
    main()
