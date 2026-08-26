"""Run the reference snippets and capture what they actually produce.

Same discipline as the from-scratch lane: the result shown beside a snippet is
the result that snippet produced when the page was built, so the two cannot
drift. A snippet that raises is reported by the build rather than shipped.

Style rule: NumPy, consistently. The whole specialization is NumPy — every lab,
every assignment, every from-scratch file — and writing Σ as a Python for loop
would be modelling the exact habit Course 1 spends a week talking you out of.
"""
import ast
import io
import contextlib
import re
import textwrap


def _fmt(v):
    """Short, readable repr — arrays without the word 'array', floats trimmed."""
    import numpy as np
    if v is None:
        return None
    if isinstance(v, np.ndarray):
        with np.printoptions(precision=4, suppress=True, threshold=24, linewidth=68):
            s = repr(v)
        s = re.sub(r"^array\(", "", s)
        s = re.sub(r"(,\s*dtype=\w+)?\)$", "", s)
        return re.sub(r"\s+", " ", s)
    # NumPy scalars subclass the Python types, so they must be tested FIRST —
    # otherwise np.float64(5.0) reprs as "np.float64(5.0)" under NumPy 2.
    if isinstance(v, np.bool_):
        return repr(bool(v))
    if isinstance(v, np.integer):
        return repr(int(v))
    if isinstance(v, np.floating):
        return repr(round(float(v), 6))
    if isinstance(v, bool):
        return repr(v)
    if isinstance(v, float):
        return repr(round(v, 6))
    if isinstance(v, tuple):
        # a one-element tuple must keep its comma, or a shape (4,) reads as (4)
        inner = ", ".join(_fmt(x) for x in v)
        return "(" + inner + ("," if len(v) == 1 else "") + ")"
    s = repr(v)
    return s if len(s) <= 90 else s[:87] + "…"


def run(src):
    """(source, result-string, error). The last expression's value is the result."""
    src = textwrap.dedent(src).strip("\n")
    ns = {}
    try:
        import numpy as np
        import pandas as pd
        ns["np"] = np
        ns["pd"] = pd
        tree = ast.parse(src)
        tail = None
        if tree.body and isinstance(tree.body[-1], ast.Expr):
            tail = ast.Expression(tree.body[-1].value)
            tree.body = tree.body[:-1]
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            exec(compile(tree, "<snippet>", "exec"), ns)
            val = eval(compile(tail, "<snippet>", "eval"), ns) if tail else None
        printed = buf.getvalue().strip()
        out = printed if printed else _fmt(val)
        return src, out, None
    except Exception as e:
        return src, None, "%s: %s" % (type(e).__name__, e)


def render(src, out, err, highlight):
    body = ['<div class="refcode"><span class="lbl">in NumPy</span>']
    body.append("<pre><code>%s</code></pre>" % highlight(src))
    if err:
        body.append('<div class="rc-err">%s</div>' % err)
    elif out:
        body.append('<div class="rc-out"><span>&#8594;</span>%s</div>'
                    % re.sub(r"<", "&lt;", out))
    body.append("</div>")
    return "".join(body)
