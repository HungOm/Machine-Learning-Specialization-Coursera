from kit import vec, hat, dotov, barov, sqrt  # noqa: F401
# -*- coding: utf-8 -*-
"""Helpers for authoring spaced-repetition cards.

IMPORTANT: a card's `cid` is its permanent identity. The learner's scheduling
state (interval, ease, due date) is keyed on it in localStorage. Renaming a cid
silently resets that card's progress, so treat cids as append-only.
"""

KINDS = {
    "formula":   ("Formula", "state it from memory"),
    "concept":   ("Concept", "explain it in your own words"),
    "algorithm": ("Algorithm", "list the steps"),
    "distinguish": ("Distinguish", "what is the difference?"),
    "trap":      ("Trap", "what goes wrong?"),
    "code":      ("Code", "what does this line do?"),
    "number":    ("Number", "recall the value"),
}


def C(cid, kind, front, back, lesson, extra=None):
    """One card. front/back are HTML fragments."""
    assert kind in KINDS, "unknown kind: %s" % kind
    return {
        "id": cid,
        "kind": kind,
        "front": front,
        "back": back,
        "lesson": lesson,
        "extra": extra or "",
    }


def deck(course, week, title, cards):
    return {"course": course, "week": week, "title": title, "cards": cards}


# ---- small inline maths helpers, matching base.css ----------------------
def m(s):
    """inline maths span"""
    return '<span class="cm">%s</span>' % s


def blk(s, label=None):
    """block maths"""
    lab = '<span class="lbl">%s</span>' % label if label else ""
    return '<div class="ceq">%s%s</div>' % (lab, s)


def steps(items):
    return "<ol class='csteps'>" + "".join("<li>%s</li>" % i for i in items) + "</ol>"


def bullets(items):
    return "<ul class='cbul'>" + "".join("<li>%s</li>" % i for i in items) + "</ul>"


def two(a, b, la="", lb=""):
    return ('<div class="ctwo"><div><b>%s</b>%s</div><div><b>%s</b>%s</div></div>'
            % (la, a, lb, b))


def hint(s):
    return '<div class="chint">%s</div>' % s


# ---- beginner-friendly decoding, shown under every answer ---------------
def plain(gist, syms=None, also=None):
    """A no-jargon explanation to sit beside the formal answer.

    gist : one or two sentences with no notation in them at all
    syms : [(symbol, how you say it out loud, what it actually means)]
    also : an optional closing line, e.g. a everyday analogy
    """
    out = ['<div class="cplain"><span class="cplain-tag">In plain English</span>']
    out.append('<p>%s</p>' % gist)
    if syms:
        rows = "".join(
            '<tr><td class="sy">%s</td><td class="sa">%s</td><td>%s</td></tr>' % r
            for r in syms)
        out.append('<table class="cdec"><thead><tr><th>symbol</th><th>say it</th>'
                   '<th>what it means</th></tr></thead><tbody>%s</tbody></table>' % rows)
    if also:
        out.append('<p class="calso">%s</p>' % also)
    out.append('</div>')
    return "".join(out)
