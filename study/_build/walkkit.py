# -*- coding: utf-8 -*-
"""Visual pieces for the plain-words walkthroughs.

A walkthrough written as paragraphs is a wall, however plain the words are —
and a wall is the one thing a reader with no maths background will not push
through. These helpers pull the things that carry the meaning OUT of the
sentence flow and give them room: an expression on its own line, two cases side
by side, a worked value chain with arrows, a numbered set of steps.

Nothing here changes what is said. It changes how much of it you can see at a
glance, which for this reader is most of the battle.
"""


def p(text):
    return "<p>%s</p>" % text


def expr(code, says="", label=""):
    """One expression, on its own, with room around it and a plain reading under.

    Inline code buried mid-sentence is invisible; the eye skates over it. The
    same characters set on their own line with air around them get read.
    """
    lab = '<span class="wx-l">%s</span>' % label if label else ""
    say = '<span class="wx-s">%s</span>' % says if says else ""
    return '<div class="wx">%s<code class="wx-c">%s</code>%s</div>' % (lab, code, say)


def chain(items, cap=""):
    """A short horizontal run of values with arrows between them.

    For "0.99 → cost 0.01" — a two-step story that costs a whole sentence to
    write out and is instant to read as a chain.
    """
    body = '<span class="wc-a">→</span>'.join('<span class="wc-i">%s</span>' % x
                                              for x in items)
    c = '<span class="wc-cap">%s</span>' % cap if cap else ""
    return '<div class="wchain">%s%s</div>' % (body, c)


def chainset(rows, tag=""):
    """Several arrow-chains in ONE panel, each with its note on the right.

    Three separate chain() boxes stacked up waste half the page and read as
    three unrelated facts. Grouped, they read as what they are: the same
    quantity at three settings, which is the comparison being made.
    """
    out = []
    for items, note in rows:
        body = '<span class="wc-a">→</span>'.join('<span class="wc-i">%s</span>' % x
                                                  for x in items)
        out.append('<div class="wcs-row"><span class="wcs-c">%s</span>'
                   '<span class="wcs-n">%s</span></div>' % (body, note))
    t = '<span class="wcs-t">%s</span>' % tag if tag else ""
    return '<div class="wchainset">%s%s</div>' % (t, "".join(out))


def steps(items, tag=""):
    """Numbered steps with the number set big, so the sequence is visible."""
    lis = "".join('<li><span class="ws-n">%d</span><span class="ws-b">%s</span></li>'
                  % (i, x) for i, x in enumerate(items, 1))
    t = '<span class="ws-t">%s</span>' % tag if tag else ""
    return '<div class="wsteps">%s<ol>%s</ol></div>' % (t, lis)


def cases(items, tag=""):
    """Two or three parallel cases, side by side rather than stacked in prose.

    Anything of the shape "if y = 1 … but if y = 0 …" reads far better as two
    panels than as two sentences, because the reader can see they are the same
    shape with one thing swapped.
    """
    cols = "".join('<div class="wk-case"><span class="wk-h">%s</span>'
                   '<div class="wk-b">%s</div></div>' % (h, b) for h, b in items)
    t = '<span class="wk-t">%s</span>' % tag if tag else ""
    return '<div class="wcases">%s<div class="wk-row">%s</div></div>' % (t, cols)


def values(rows, tag=""):
    """label → value → aside. For "here is what it printed and what it means"."""
    r = "".join('<tr><td class="wv-l">%s</td><td class="wv-v">%s</td>'
                '<td class="wv-n">%s</td></tr>' % x for x in rows)
    t = '<span class="wv-t">%s</span>' % tag if tag else ""
    return '<div class="wvals">%s<table>%s</table></div>' % (t, r)


def point(text, tag="The point"):
    """The one sentence to keep, set apart so it is not lost in a paragraph."""
    return '<div class="wpoint"><span class="wp-t">%s</span>%s</div>' % (tag, text)


def ascii_art(art, cap=""):
    """A small drawing, in a monospace block, for the few things a picture beats
    a sentence at — the shape of a curve, a boundary on a scatter.

    Kept deliberately rare and deliberately tiny. This is the one place a <pre>
    of characters earns its keep, and every character used still has to survive
    glyphcheck.py.
    """
    c = '<span class="wa-cap">%s</span>' % cap if cap else ""
    return '<div class="wart"><pre>%s</pre>%s</div>' % (art, c)
