"""Parse the runnable scratch/code/*.py files and execute them section by section.

The point of this module is that the code shown on the page is read from the
file that actually runs, and the output shown underneath it is what that exact
code printed. Neither can drift from the other.
"""
import contextlib
import io
import os
import re
import sys

MARK = re.compile(r"^# %% SECTION: (\w+)\s*$", re.M)


def split_sections(src):
    """[(name, code)] — everything before the first marker is 'prelude'."""
    parts, last, name = [], 0, "prelude"
    for m in MARK.finditer(src):
        parts.append((name, src[last:m.start()]))
        name, last = m.group(1), m.end()
    parts.append((name, src[last:]))
    return [(n, c.strip("\n")) for n, c in parts if c.strip()]


def run_sections(path):
    """Execute the file one section at a time, capturing each section's output.

    Everything runs in a single shared namespace and in file order, so this is
    exactly equivalent to running the script — it just records which print()
    belonged to which block.
    """
    src = open(path, encoding="utf-8").read()
    sections = split_sections(src)
    ns = {"__name__": "__main__", "__file__": path}
    out = []
    cwd = os.getcwd()
    os.chdir(os.path.dirname(path))
    try:
        for name, code in sections:
            buf = io.StringIO()
            try:
                with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
                    exec(compile(code, path, "exec"), ns)
                err = None
            except Exception as e:              # a broken example must not build silently
                err = "%s: %s" % (type(e).__name__, e)
            out.append((name, code, buf.getvalue().rstrip("\n"), err))
    finally:
        os.chdir(cwd)
    return out


def hl(src):
    """Highlighting for the runnable files — the same single left-to-right pass
    the lessons use. Sequential re.sub passes tore their own markup open here:
    `class` is a Python keyword, so the keyword pass matched the class=
    attribute of every span the docstring and comment passes had inserted."""
    from kit import highlight
    return highlight(src)


def render_section(name, code, output, err, prose):
    import html as _h
    parts = ['<section class="sx" id="sx-%s">' % name]
    if prose:
        parts.append('<div class="sx-prose">%s</div>' % prose)
    parts.append('<div class="sx-code"><pre><code>%s</code></pre></div>' % hl(code))
    if err:
        parts.append('<div class="sx-out err"><span class="lbl">error</span>'
                     '<pre>%s</pre></div>' % _h.escape(err))
    elif output:
        parts.append('<div class="sx-out"><span class="lbl">output</span>'
                     '<pre>%s</pre></div>' % _h.escape(output))
    parts.append('</section>')
    return "".join(parts)
