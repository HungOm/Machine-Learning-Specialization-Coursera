# -*- coding: utf-8 -*-
"""Helpers for the week-gist pages — one page per week, the whole thing at once.

Every lesson page teaches one idea thoroughly. That is the right shape for
meeting an idea the first time and the wrong shape for seeing how the ideas
join: after thirteen self-contained lessons the *joins* are the part nobody has
drawn. A gist page draws them, and only them. It teaches nothing new — if a
sentence here is not already somewhere in the week, it does not belong here.

Everything renders as ordinary HTML, never as preformatted ASCII art. A <pre>
of box-drawing characters looks right in one font at one width and falls apart
in reader mode, in print, and on a phone — and the site already has a glyph
checker precisely because unrenderable characters are a real bug here.
"""

import html as _h


# ---------------------------------------------------------------- one line
def gistline(text):
    """The whole week in a single sentence, before anything else."""
    return '<p class="gistline">%s</p>' % text


# ---------------------------------------------------------------- the picture
_KINDS = {"in", "op", "out", "back", "stop", "note"}


def _steps(items, depth=0):
    out = []
    for it in items:
        kind = it[0]
        if kind == "arw":
            label = it[1] if len(it) > 1 else ""
            out.append('<li class="fl-arw"><span class="a">↓</span>'
                       '<span class="l">%s</span></li>' % label)
        elif kind == "loop":
            _, label, inner = it
            out.append('<li class="fl-loop"><span class="fl-loop-t">%s</span>'
                       '<ol class="flow inner">%s</ol>'
                       '<span class="fl-loop-b"><span class="a">↑</span>'
                       'and round again</span></li>' % (label, _steps(inner, depth + 1)))
        else:
            if kind not in _KINDS:
                raise ValueError("unknown flow kind %r" % kind)
            title = it[1]
            body = it[2] if len(it) > 2 else ""
            out.append('<li class="fl k-%s"><span class="fl-t">%s</span>'
                       '<span class="fl-b">%s</span></li>' % (kind, title, body))
    return "".join(out)


def flow(items, tag="The week in one picture", cap=""):
    """A vertical pipeline: boxes, labelled arrows, and repeated bands.

    items is a list of tuples:
      (kind, title, body)      kind in in/op/out/back/stop/note
      ("arw", label)           a labelled arrow between two boxes
      ("loop", label, [items]) a band that repeats, with a return arrow

    The picture is the point of the whole page. Read top to bottom it says what
    goes in, what happens to it, what comes out, and which part runs again.
    """
    c = '<p class="flow-cap">%s</p>' % cap if cap else ""
    return ('<figure class="flowd"><figcaption class="tag">%s</figcaption>'
            '<ol class="flow">%s</ol>%s</figure>' % (tag, _steps(items), c))


# ---------------------------------------------------------------- what carried over
def carried(intro, rows, tag="What this week rests on",
            head=("You already have", "Where it came from", "What it turns into here")):
    """The join backwards: nothing here is new, and here is where each piece was met.

    On a week that follows another ML week this is the delta table — the same
    skeleton, and the two or three things that actually changed. On the first
    week of a course it points back at the foundations instead.
    """
    r = "".join("<tr><td><b>%s</b></td><td>%s</td><td>%s</td></tr>" % x for x in rows)
    return ('<div class="carry"><span class="tag">%s</span><p>%s</p>'
            '<table class="carrytab"><thead><tr><th>%s</th><th>%s</th><th>%s</th></tr></thead>'
            '<tbody>%s</tbody></table></div>'
            % (tag, intro, head[0], head[1], head[2], r))


def sameskel(same, changes, tag="Same skeleton, and what changed"):
    """Explicit continuity: the loop that does not change, then the diff.

    same    — html: the skeleton carried over unchanged
    changes — [(what, from_, to)] rows
    """
    r = "".join("<tr><td><b>%s</b></td><td class=\"was\">%s</td><td class=\"now\">%s</td></tr>" % x
                for x in changes)
    return ('<div class="skel"><span class="tag">%s</span>'
            '<div class="skel-same">%s</div>'
            '<table class="skeltab"><thead><tr><th>What</th><th>Last time</th>'
            '<th>This week</th></tr></thead><tbody>%s</tbody></table></div>'
            % (tag, same, r))


# ---------------------------------------------------------------- the chain
def chain(steps, tag="The pieces, in the order they hand to each other"):
    """The week's algorithm as a numbered chain, each link naming the next.

    Each step is a dict:
      name    — what the piece is called
      does    — one line: what it does, in plain words
      formula — the formula, in the site's usual eq/eqp markup (optional)
      code    — the NumPy line that is this formula (optional)
      trap    — the one thing that goes wrong here (optional)
      feeds   — what it hands to the next link (omit on the last)
    """
    out = ['<div class="chainw"><span class="tag">%s</span><ol class="chain">' % tag]
    for i, s in enumerate(steps, 1):
        out.append('<li class="ch-step"><div class="ch-h"><span class="ch-n">%d</span>'
                   '<b>%s</b></div><p class="ch-does">%s</p>' % (i, s["name"], s["does"]))
        if s.get("formula"):
            out.append('<div class="ch-f">%s</div>' % s["formula"])
        if s.get("code"):
            from kit import highlight
            out.append('<div class="ch-c"><span class="lbl">the same thing in code</span>'
                       '<pre><code>%s</code></pre></div>' % highlight(s["code"].strip("\n")))
        if s.get("trap"):
            out.append('<p class="ch-t"><span class="lbl">where it goes wrong</span>%s</p>'
                       % s["trap"])
        if s.get("feeds"):
            out.append('<p class="ch-next"><span class="a">↓</span>%s</p>' % s["feeds"])
        out.append("</li>")
    out.append("</ol></div>")
    return "".join(out)


# ---------------------------------------------------------------- worked numbers
def bynumbers(intro, rows, close="", tag="The same thing with numbers small enough to check"):
    """One pass of the week's algorithm, arithmetic shown, on numbers a person
    can verify with a pencil.

    rows is [(label, value, comment)]. Every value on a gist page is computed in
    the content module and formatted in — never typed from memory — so the page
    cannot drift from the arithmetic it claims.
    """
    r = "".join('<tr><td class="lb">%s</td><td class="vl">%s</td><td>%s</td></tr>' % x
                for x in rows)
    c = "<p>%s</p>" % close if close else ""
    return ('<div class="bynum"><span class="tag">%s</span><p>%s</p>'
            '<table class="bynumtab"><tbody>%s</tbody></table>%s</div>'
            % (tag, intro, r, c))


# ---------------------------------------------------------------- retell
def retell(items, tag="Say the week back, with the page shut"):
    """The closed-book test that this page is FOR.

    Not a summary to read — a list of sentences to reproduce. Reading a summary
    is the technique Dunlosky et al. rate lowest; producing one from memory is
    the technique they rate highest. So this states the instruction plainly and
    numbers the beats so a gap is obvious.
    """
    lis = "".join("<li>%s</li>" % x for x in items)
    return ('<div class="retell"><span class="tag">%s</span>'
            '<p>Cover everything above. Say these out loud, in order, in your own words. '
            'The one you stumble on names the lesson to reopen &mdash; that stumble is the '
            'whole value of the exercise.</p>'
            '<ol class="rt">%s</ol></div>' % (tag, lis))


# ---------------------------------------------------------------- the ladder
# One ladder, defined once, marked differently on each page. The rungs are the
# order the site actually teaches them in, and the last three are past the
# specialization on purpose: they are where the user is going.
LADDER = [
    ("F0",      "Arithmetic, slopes, vectors, NumPy",       "the notation everything else is written in"),
    ("C1 W1",   "Linear regression and gradient descent",   "predict a number; roll downhill to fit it"),
    ("C1 W2",   "Many features, vectorised",                "the same fit, on wide data, fast"),
    ("C1 W3",   "Logistic regression and regularization",   "predict a class; keep the weights sane"),
    ("C2 W1",   "Forward propagation",                      "stack the units — what a network computes"),
    ("C2 W2",   "Training a network, softmax, Adam",        "backprop: which weight caused the mistake"),
    ("C2 W3",   "Bias, variance, error analysis",           "what to actually do when it is wrong"),
    ("C2 W4",   "Decision trees and ensembles",             "the other family, and when it wins"),
    ("C3 W1",   "Clustering and anomaly detection",         "learning with no labels at all"),
    ("C3 W2",   "Recommenders and PCA",                     "learned features, and squeezing dimensions"),
    ("C3 W3",   "Reinforcement learning",                   "learning from a reward instead of an answer"),
    ("C4 W1",   "Embeddings and tokenization",              "how text becomes numbers"),
    ("C4 W2",   "Attention",                                "how a model decides which words matter"),
    ("C4 W3",   "Transformers",                             "the architecture translation is built on"),
    ("C4 W4",   "Fine-tuning a pretrained model",           "teach a multilingual model one more language"),
]

DESTINATION = ("A K’Cho ↔ English translator, fine-tuned from a pretrained "
               "multilingual model")


def ladder(here, why, tag="Where this sits on the way to the translator"):
    """The rung ladder, with one rung marked and one sentence on why it matters.

    The site otherwise answers "what is this idea"; this answers "why am I
    reading it". Keeping the ladder in one place means the route cannot say two
    different things on two different pages.
    """
    rows = []
    seen_here = False
    for tagname, title, note in LADDER:
        if tagname == here:
            cls, seen_here = "at", True
        elif seen_here:
            cls = "ahead"
        else:
            cls = "done"
        rows.append('<li class="rung %s"><span class="rw">%s</span>'
                    '<span class="rt">%s</span><span class="rn">%s</span></li>'
                    % (cls, tagname, title, note))
    return ('<div class="ladder"><span class="tag">%s</span>'
            '<p class="dest"><span class="lbl">where the ladder goes</span>%s</p>'
            '<ol class="rungs">%s</ol>'
            '<p class="why"><span class="lbl">why this rung</span>%s</p></div>'
            % (tag, DESTINATION, "".join(rows), why))


# ---------------------------------------------------------------- misc
def h2(icon, text, anchor=None):
    a = ' id="%s"' % anchor if anchor else ""
    return '<h2%s><span class="ico">%s</span>%s</h2>' % (a, icon, text)


def esc(s):
    return _h.escape(s)
