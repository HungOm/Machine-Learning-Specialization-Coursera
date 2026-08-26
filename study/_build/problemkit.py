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
      gist=None, check=None, fade=None):
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
    fade   : optional — how many trailing steps to hide behind "your turn".
             None means decide from the length (see fade_count). 0 disables it
             for a problem whose last step is not something you could work out.
    """
    return dict(pid=pid, ask=ask, steps=steps, answer=answer, lesson=lesson,
                level=level, why=why, hint=hint, tag=tag, gist=gist, check=check,
                fade=fade)


def fade_count(n_steps, fade=None):
    """How many trailing steps to blank — BACKWARD fading.

    Reading a finished solution feels like understanding and mostly is not.
    Completing one is the version that shows up in the results (Sweller &
    Cooper 1985's completion effect; Renkl & Atkinson 2003 on fading).

    Backwards, because the last step is the one you are most ready to do: every
    step before it is still there as support. Longer solutions carry more
    support, so they can afford to give back two.
    """
    if fade is not None:
        return max(0, min(int(fade), n_steps - 1))
    if n_steps >= 5:
        return 2
    if n_steps >= 3:
        return 1
    return 0


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
    steps = p["steps"]
    nf = fade_count(len(steps), p.get("fade"))
    first_faded = len(steps) - nf
    rows = []
    for i, (w, a) in enumerate(steps):
        if i >= first_faded:
            rows.append('<li class="wfade"><span class="ws">%s</span>'
                        '<details class="wf"><summary>your turn</summary>'
                        '<span class="wa">%s</span></details></li>' % (w, a))
        else:
            rows.append('<li><span class="ws">%s</span><span class="wa">%s</span></li>' % (w, a))
    work = "".join(rows)
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
