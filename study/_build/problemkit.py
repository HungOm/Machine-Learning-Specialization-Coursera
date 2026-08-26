"""Helpers for problem sets.

A problem set is one page per week. Problems are deliberately *interleaved* —
mixed up rather than grouped by lesson — because practising one topic in a block
feels much better than it works. Mixing forces you to first decide what kind of
problem it is, which is the part you actually have to do in an exam or a job.

Ids (`pid`) are permanent: they key your self-grades in localStorage, so renaming
one throws away that record. Append, never renumber.
"""
from kit import vec, hat, dotov, barov, sqrt  # noqa: F401
import html as _h


def P(pid, ask, steps, answer, lesson, level=2, why=None, hint=None, tag="",
      gist=None, check=None):
    """One problem.

    pid    : permanent id, e.g. "f0w1-p07"
    ask    : the question (HTML)
    steps  : [(what you are doing, the arithmetic)] — every line of the working
    answer : the final answer (HTML), shown boxed
    lesson : lesson file this leans on, e.g. "f0/w1-04-slope.html"
    level  : 1 warm-up · 2 core · 3 stretch
    why    : optional — what the problem is really testing
    hint   : optional — one nudge, revealed separately from the solution
    gist   : optional — the question re-said in plain words, with no notation,
             before the arithmetic starts. Shown first inside the solution, so
             the problem is self-contained even if the lesson is a distant memory.
    check  : optional — a SECOND way to land on the same answer: a sanity check
             computed differently, or what the number actually means. The steps
             show you can get the answer; this shows you can trust it.
    """
    return dict(pid=pid, ask=ask, steps=steps, answer=answer, lesson=lesson,
                level=level, why=why, hint=hint, tag=tag, gist=gist, check=check)


LEVEL_NAME = {1: "warm-up", 2: "core", 3: "stretch"}


def render(p, n, up="../"):
    parts = []
    parts.append('<article class="prob" data-pid="%s" id="%s">' % (p["pid"], p["pid"]))
    parts.append(
        '<header><span class="pn">%d</span>'
        '<span class="plv l%d">%s</span>'
        '%s'
        '<a class="pl" href="%s%s">↗ lesson</a></header>'
        % (n, p["level"], LEVEL_NAME[p["level"]],
           '<span class="ptag">%s</span>' % _h.escape(p["tag"]) if p["tag"] else "",
           up, p["lesson"]))
    parts.append('<div class="pask">%s</div>' % p["ask"])
    if p.get("hint"):
        parts.append('<details class="phint"><summary>stuck? one hint</summary>'
                     '<div>%s</div></details>' % p["hint"])
    gist = ('<div class="pgist"><span class="tag">In plain words</span>%s</div>'
           % p["gist"]) if p.get("gist") else ""
    work = "".join('<li><span class="ws">%s</span><span class="wa">%s</span></li>'
                   % (w, a) for w, a in p["steps"])
    check = ('<div class="pcheck"><span class="tag">A second way to see it</span>%s</div>'
             % p["check"]) if p.get("check") else ""
    why = ('<div class="pwhy"><span class="tag">What this is really testing</span>%s</div>'
           % p["why"]) if p.get("why") else ""
    parts.append(
        '<details class="psol"><summary>worked solution</summary>'
        '<div class="psol-b">%s<ol class="work">%s</ol>'
        '<div class="pans"><span>answer</span>%s</div>%s%s</div></details>'
        % (gist, work, p["answer"], check, why))
    parts.append('</article>')
    return "".join(parts)


# ---------------------------------------------------------------- shorthands
def m(x):
    """inline maths"""
    return '<span class="v">%s</span>' % x


def frac(a, b):
    return '<span class="frac"><span>%s</span><span>%s</span></span>' % (a, b)


def cols(headers, rows):
    h = "".join("<th>%s</th>" % x for x in headers)
    body = ""
    for row in rows:
        body += "<tr>" + "".join(
            '<td class="num">%s</td>' % c if isinstance(c, (int, float)) else "<td>%s</td>" % c
            for c in row) + "</tr>"
    return ('<table class="data"><thead><tr>%s</tr></thead><tbody>%s</tbody></table>'
            % (h, body))


def pre(src):
    return "<pre><code>%s</code></pre>" % _h.escape(src.strip("\n"))
