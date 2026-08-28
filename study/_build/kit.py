"""Small helpers so lesson content stays readable."""
import html as _h
import re

# ---------------------------------------------------------------- callouts
def _call(kind, tag, body):
    return ('<div class="callout %s"><span class="tag">%s</span>%s</div>'
            % (kind, tag, body))

def kid(body, tag="In plain English"):
    return _call("kid", tag, body)

def key(body, tag="The one thing to remember"):
    return _call("key", tag, body)

def warn(body, tag="Watch out"):
    return _call("warn", tag, body)

def trap(body, tag="Common trap"):
    return _call("trap", tag, body)

def note(body, tag="Why this matters"):
    return _call("", tag, body)

def pretest(ask, watch, tag="Before you read"):
    """A question asked BEFORE the lesson explains anything.

    The research point is the attempt, not the answer: trying and failing
    before instruction improves later retention (Richland, Kornell & Kao 2009).
    So this deliberately does NOT reveal an answer — committing to a guess
    unlocks only what to watch for as you read. Giving the answer here would
    turn it back into something to read rather than something to attempt.
    """
    return (h2("\u2753", tag)
            + '<div class="pretest">%s'
              '<details class="pt"><summary>I have committed to an answer</summary>'
              '<div class="pt-b">%s</div></details></div>' % (ask, watch))


def explain(ask, because, tag="Say it out loud"):
    """A self-explanation prompt, placed at a worked example.

    Chi et al. (1994): learners asked to explain a worked step back to
    themselves outperform learners who read the same step. The effect comes
    from asking WHY a step follows, not from asking what it says — so these
    prompts ask for a justification, and the reveal gives the reason rather
    than repeating the arithmetic.
    """
    return ('<div class="explain"><span class="tag">%s</span>%s'
            '<details class="ex"><summary>said it &mdash; now check</summary>'
            '<div class="ex-b">%s</div></details></div>' % (tag, ask, because))


def chapter_open(rests_on, able_to, leads_to, hook):
    """The chapter opener: arrive knowing why you are here.

    A book tells you what you are walking into. Each lesson in this site is
    self-contained, which is a strength inside the lesson and leaves the joins
    between chapters silent — so this names what the chapter rests on, what it
    buys you, and where it goes next.
    """
    return ('<div class="chopen"><span class="tag">Before this chapter</span>'
            '<p class="hook">%s</p>'
            '<table class="chgrid"><tbody>'
            '<tr><td>Rests on</td><td>%s</td></tr>'
            '<tr><td>You will be able to</td><td>%s</td></tr>'
            '<tr><td>Leads to</td><td>%s</td></tr>'
            '</tbody></table></div>' % (hook, rests_on, able_to, leads_to))


def chapter_close(items):
    """The chapter closer: retrieval practice at the boundary.

    Placed where the research says it works — at a join, before the next
    chapter overwrites what you just read. Questions only; no answers, because
    the point is the attempt and the lessons above are the answer key.
    """
    lis = "".join("<li>%s</li>" % q for q in items)
    return ('<div class="chclose"><span class="tag">Before moving on</span>'
            '<p>Cover the chapter and answer these from memory. Anything you '
            'fumble names the lesson to reread.</p>'
            '<ol class="chq">%s</ol></div>' % lis)


def card(body):
    return '<div class="card">%s</div>' % body

# ---------------------------------------------------------------- maths
def eq(inner, label=None, small=False):
    lab = '<span class="lbl">%s</span>' % label if label else ""
    return '<div class="eq%s">%s%s</div>' % (" small" if small else "", lab, inner)

def eqp(parts, label=None, small=False):
    """A formula with colour-coded, click-to-explain parts.

    parts: a list where each item is either a plain string (an operator,
    a bracket, glue — rendered unstyled) or a 3-tuple (html, key, tag):
      html — the fragment to render, in the usual eq() markup
      key  — a GLOSS key (existing, or from content_formulaparts.py) —
             reuses the site's normal hover/click popup unchanged
      tag  — a short label shown under this part, specific to what it
             means IN THIS formula (the same key can carry a different
             tag in a different formula)

    Colour cycles 1-5 across distinct keys, left to right — a key repeated
    later in the same formula (α appearing in both the w and b update) keeps
    the colour it was first given, rather than cycling onward.
    """
    out, colors_seen = [], {}
    COLORS = 5
    for p in parts:
        if isinstance(p, str):
            out.append('<span class="fanat-part plain"><span class="term">%s</span></span>' % p)
            continue
        frag, gkey, tag = p
        if gkey not in colors_seen:
            colors_seen[gkey] = (len(colors_seen) % COLORS) + 1
        c = colors_seen[gkey]
        out.append(
            '<span class="fanat-part" data-c="%d">'
            '<span class="term"><span class="gterm" data-g="%s">%s</span></span>'
            '<span class="tick"></span><span class="tag">%s</span></span>'
            % (c, gkey, frag, tag))
    lab = '<span class="lbl">%s</span>' % label if label else ""
    return ('<div class="fanat-eq%s">%s<div class="fanat-row">%s</div></div>'
            % (" small" if small else "", lab, "".join(out)))

def decode(rows, head=("Symbol", "Say it out loud", "What it actually is")):
    r = "".join("<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % x for x in rows)
    return ('<table class="decode"><thead><tr><th>%s</th><th>%s</th><th>%s</th></tr></thead>'
            '<tbody>%s</tbody></table>' % (head[0], head[1], head[2], r))

def table(headers, rows):
    h = "".join("<th>%s</th>" % x for x in headers)
    body = ""
    for row in rows:
        body += "<tr>" + "".join(
            '<td class="num">%s</td>' % c if isinstance(c, (int, float)) else "<td>%s</td>" % c
            for c in row) + "</tr>"
    return '<table class="data"><thead><tr>%s</tr></thead><tbody>%s</tbody></table>' % (h, body)

# ---------------------------------------------------------------- demo
def demo(anim, title, hint="", opts=None):
    o = ""
    if opts:
        o = " " + " ".join('data-%s="%s"' % (k, v) for k, v in opts.items())
    return ('<div class="demo"><div class="demo-head"><span class="t">▶ %s</span>'
            '<span class="h">%s</span></div>'
            '<div class="demo-body" data-anim="%s"%s></div></div>'
            % (title, hint, anim, o))

# ---------------------------------------------------------------- quiz
def quiz(items):
    out = ['<div class="quiz">']
    for q, a in items:
        out.append('<details class="q"><summary>%s</summary><div class="a">%s</div></details>' % (q, a))
    out.append("</div>")
    return "".join(out)

# ---------------------------------------------------------------- links
def links(items):
    out = ['<ul class="links">']
    for kind, url, title, desc in items:
        out.append('<li><span class="kind %s">%s</span><span><a href="%s" target="_blank" rel="noopener">%s</a>'
                   '<span class="d">%s</span></span></li>' % (kind, kind, url, title, desc))
    out.append("</ul>")
    return "".join(out)

# ---------------------------------------------------------------- code
# Highlighting is ONE left-to-right pass, not a series of re.sub calls.
#
# The series version had a real bug: `class` is a Python keyword, so the keyword
# pass matched the class= attribute inside spans the earlier passes had already
# inserted, tearing them open. 1,404 broken spans across 87 pages. A single
# alternation cannot do that, because re.sub never rescans what it substituted.
#
# Alternation order settles ties at the same position (a docstring must win over
# a plain string). Different positions settle themselves: whichever token starts
# first wins, so a # inside a string stays part of the string and a quote inside
# a comment stays part of the comment.
KEYWORDS = ("False|None|True|and|as|assert|async|await|break|class|continue|def|del|elif|"
            "else|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|"
            "pass|print|raise|return|try|while|with|yield")

TOKEN = re.compile(
    r"(?P<d>&quot;&quot;&quot;.*?&quot;&quot;&quot;|&#x27;&#x27;&#x27;.*?&#x27;&#x27;&#x27;)"
    r"|(?P<c>\#[^\n]*)"
    r"|(?P<s>&quot;[^&\n]*?&quot;|&#x27;[^&\n]*?&#x27;)"
    r"|(?P<k>\b(?:" + KEYWORDS + r")\b)"
    r"|(?P<n>\b\d+\.?\d*(?:e-?\d+)?\b)",
    re.S)


def highlight(src):
    """Escape, then wrap tokens. Escaping first means the inserted markup is the
    only unescaped angle bracket in the result, which is what makes it safe."""
    def wrap(m):
        return '<span class="tok-%s">%s</span>' % (m.lastgroup, m.group(0))
    return TOKEN.sub(wrap, _h.escape(src))


def code(src, lang="python"):
    return "<pre><code>%s</code></pre>" % highlight(src.strip("\n"))


# ---------------------------------------------------------------- section
def lenses(trade, bridge, object_, stakes, foldback):
    """Five short views of one idea, before the formal treatment.

    The site's default order is: plain words, then the maths. That works, but
    it offers exactly ONE way in. A reader who has never met a formula and a
    reader with an economics degree need different doors into the same room,
    and neither door is the equation.

    So each treated lesson gets five beats, in this fixed order:

      trade    — a craft, market or kitchen scene, felt in the body. Assumes
                 no formal education whatsoever.
      bridge   — "you already know this under another name", aimed at someone
                 schooled in an adjacent field (stats, econ, engineering).
      object_  — ONE concrete thing to picture. Not a metaphor for the maths;
                 a picture the maths is literally describing.
      stakes   — a real deployed system where this idea costs or saves money,
                 time or safety. Answers "why does this exist at all".
      foldback — one closing line handing the reader back to the formal
                 version, which now reads as the summary of all four.

    This is ADDITIVE. It never replaces kid() — the plain-words opener stays
    exactly where it is, the same way the review deck's plain-English layer
    sits beside the formal answer rather than instead of it.

    `object` is a builtin, hence the trailing underscore on the parameter.
    """
    beats = [("trade", "\U0001f527", "If you have never seen a formula", trade),
             ("bridge", "\U0001f309", "If you know a neighbouring field", bridge),
             ("object", "\U0001f441", "One thing to picture", object_),
             ("stakes", "\u2696\ufe0f", "Where this really costs something", stakes)]
    out = ['<div class="lenses">']
    for cls, ico, tag, body in beats:
        out.append('<div class="lens %s"><span class="tag"><span class="ico">%s</span>%s</span>%s</div>'
                   % (cls, ico, tag, body))
    out.append('<p class="lens-fold">%s</p>' % foldback)
    out.append("</div>")
    return "".join(out)


def h2(icon, text, anchor=None):
    a = ' id="%s"' % anchor if anchor else ""
    return '<h2%s><span class="ico">%s</span>%s</h2>' % (a, icon, text)

def grid2(a, b):
    return '<div class="grid2">%s%s</div>' % (a, b)

def grid3(a, b, c):
    return '<div class="grid3">%s%s%s</div>' % (a, b, c)


# ---------------------------------------------------------------- overset marks
# The combining marks people reach for (U+20D7 x-vector arrow especially) are
# missing from every font macOS ships, so they render as tofu boxes. Draw them.
def vec(x):
    """x with an arrow above it — a vector."""
    return '<span class="ov vec">%s</span>' % x

def hat(x):
    """x with a caret above it — an estimate."""
    return '<span class="ov hat">%s</span>' % x

def dotov(x):
    """x with a dot above it — a rate of change."""
    return '<span class="ov dot">%s</span>' % x

def barov(x):
    """x with a bar above it — a mean."""
    return '<span class="ov bar">%s</span>' % x

def sqrt(inner):
    """A radical whose vinculum covers the radicand, not the sign."""
    return '\u221a<span class="sqrt">%s</span>' % inner
