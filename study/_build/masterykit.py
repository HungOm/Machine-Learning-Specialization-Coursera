# -*- coding: utf-8 -*-
"""Active Mastery — the appended practice layer on the build-lane pages.

DESIGN CONSTRAINT, stated once: this module only ever produces markup that is
APPENDED after the generated lesson. It never touches the lesson's own prose,
code or output, and build_scratch renders it strictly after the last section.

Everything here reuses the site's existing visual vocabulary — .sx, .sx-prose,
.wpoint, .runbox, ul.links.plain — and adds only .am-prefixed classes for the
few things that have no existing equivalent. No second design system.

Answers always live inside <details>, so a learner who scrolls has to CHOOSE to
reveal. That is the whole reason this layer is worth having rather than being
more prose.
"""


def _det(summary, body, cls="am-rev"):
    return ('<details class="%s"><summary>%s</summary><div class="am-b">%s</div>'
            '</details>' % (cls, summary, body))


def section(num, icon, title, anchor, body):
    """One numbered Active Mastery section, in the site's existing .sx shape."""
    return ('<section class="sx am-sec" id="am-%s">'
            '<h3 class="am-h"><span class="am-n">%s</span>'
            '<span class="ico">%s</span>%s</h3>%s</section>'
            % (anchor, num, icon, title, body))


def prose(html):
    return '<div class="sx-prose">%s</div>' % html


def code(src, lang="python"):
    from kit import highlight
    return '<div class="sx-code"><pre><code>%s</code></pre></div>' % highlight(src.strip("\n"))


def out(text):
    import html as _h
    return ('<div class="sx-out"><span class="lbl">output</span><pre>%s</pre></div>'
            % _h.escape(text.strip("\n")))


# ---------------------------------------------------------------- 1. semantics
def semantics(rows, intro, tag="What every variable is, in the world"):
    """The runtime-variable table. Seven columns, and the two that matter are
    'in the world' and 'units' — a learner who cannot fill those in has not
    understood the program, however well they follow the algebra.

    rows: (name, shape_dtype, in_code, in_world, units, one_element, if_changed)
    """
    r = "".join(
        '<tr><td class="am-v"><code>%s</code></td><td class="am-sh">%s</td><td>%s</td>'
        '<td class="am-w">%s</td><td class="am-u">%s</td><td>%s</td><td>%s</td></tr>' % x
        for x in rows)
    cols = ('<colgroup><col class="c-name"><col class="c-shape"><col class="c-code">'
            '<col class="c-world"><col class="c-unit"><col class="c-elem">'
            '<col class="c-chg"></colgroup>')
    return ('<div class="am-sem"><span class="am-tag">%s</span><p>%s</p>'
            '<p class="am-hint">Seven columns &mdash; <b>scroll this table sideways</b> '
            'for &ldquo;one element, read aloud&rdquo; and &ldquo;if it changed&rdquo;, '
            'which are the two that do the work.</p>'
            '<div class="am-scroll"><table class="am-semtab">' + cols + '<thead><tr>'
            '<th>name</th><th>shape &amp; dtype</th><th>in code</th>'
            '<th>in the world</th><th>units</th><th>one element, read aloud</th>'
            '<th>if it changed</th></tr></thead><tbody>%s</tbody></table></div></div>'
            % (tag, intro, r))


def ledger(rows, intro, tag="Shape ledger"):
    """Where m and n travel through the program. Almost every bug in these files
    is a shape or axis bug, so the ledger is not decoration."""
    r = "".join('<tr><td><code>%s</code></td><td class="am-sh">%s</td><td>%s</td></tr>' % x
                for x in rows)
    return ('<div class="am-led"><span class="am-tag">%s</span><p>%s</p>'
            '<table class="am-ledtab"><thead><tr><th>array</th><th>shape</th>'
            '<th>what the axes are</th></tr></thead><tbody>%s</tbody></table></div>'
            % (tag, intro, r))


def drill(ask, reveal, tag="Do this now"):
    """An instruction, not an explanation. The reveal is always hidden."""
    return ('<div class="am-drill"><span class="am-tag">%s</span>%s%s</div>'
            % (tag, ask, _det("I have said it out loud &mdash; check me", reveal)))


def peek(intro, helper, points, reveal):
    """Instrument-your-copy drill: a paste-in helper and three named call sites."""
    lis = "".join('<li><code>%s</code> &mdash; %s</li>' % x for x in points)
    return ('<div class="am-peek"><span class="am-tag">Instrument your copy</span>'
            '<p>%s</p>%s<p>Paste it into <b>your copy</b> of the file, then call it at '
            'these three places and <b>narrate every printed line in world-words before '
            'you read on</b>:</p><ol class="am-pts">%s</ol>%s</div>'
            % (intro, code(helper), lis,
               _det("what you should have seen", reveal)))


# ---------------------------------------------------------------- 2. predictions
def predict(items, intro, tag="Predict before you run"):
    """Commit first. The research point is the attempt, so the answer is hidden
    and the prompt asks for a written commitment rather than a thought."""
    lis = ""
    for i, (ask, answer) in enumerate(items, 1):
        lis += ('<li><div class="am-ask">%s</div>%s</li>'
                % (ask, _det("I have written my answer down", answer)))
    return ('<div class="am-pred"><span class="am-tag">%s</span><p>%s</p>'
            '<ol class="am-plist">%s</ol></div>' % (tag, intro, lis))


# ---------------------------------------------------------------- 3. lab
def lab(levels, intro, tag="Modify the copy"):
    """L1 value -> L2 parameter -> L3 data -> L4 assumption -> L5 explain.
    Each level names the real edit to make in the real file."""
    out_ = ['<div class="am-lab"><span class="am-tag">%s</span><p>%s</p>' % (tag, intro)]
    for lvl, title, ask, edit, answer in levels:
        out_.append('<div class="am-lvl"><div class="am-lvl-h">'
                    '<span class="am-lvl-n">%s</span><b>%s</b></div>'
                    '<p class="am-ask">%s</p>%s%s</div>'
                    % (lvl, title, ask, code(edit) if edit else "",
                       _det("what happens, and why", answer)))
    out_.append("</div>")
    return "".join(out_)


# ---------------------------------------------------------------- 4. break
def breaks(items, intro, tag="Break it, then repair it"):
    """Each break must teach the INVARIANT, not the error message."""
    lis = ""
    for edit, ask, answer in items:
        lis += ('<li>%s<p class="am-ask">%s</p>%s</li>'
                % (code(edit), ask, _det("what breaks, and what it tells you", answer)))
    return ('<div class="am-break"><span class="am-tag">%s</span><p>%s</p>'
            '<ol class="am-blist">%s</ol></div>' % (tag, intro, lis))


# ---------------------------------------------------------------- 5-6
def invariant(statement, why, check, tag="The invariant"):
    return ('<div class="wpoint am-inv"><span class="wp-t">%s</span>%s'
            '<div class="am-inv-w">%s</div>%s</div>'
            % (tag, statement, why, code(check)))


def wrong(items, tag="Wrong mental models"):
    lis = ""
    for claim, why in items:
        lis += ('<li><div class="am-wrong">&#10007; &ldquo;%s&rdquo;</div>%s</li>'
                % (claim, _det("why that is wrong here", why)))
    return ('<div class="am-wm"><span class="am-tag">%s</span>'
            '<p>Each of these is a belief that survives reading the lesson and fails the '
            'moment you run something. Decide whether you hold it <b>before</b> you '
            'open the reveal.</p><ol class="am-wlist">%s</ol></div>' % (tag, lis))


# ---------------------------------------------------------------- 7
def reconstruct(stages, intro, tag="Reconstruction challenge"):
    lis = ""
    for name, ask, check in stages:
        lis += ('<li><b>%s</b><p class="am-ask">%s</p>%s</li>'
                % (name, ask, _det("how to check yourself", check)))
    return ('<div class="am-recon"><span class="am-tag">%s</span><p>%s</p>'
            '<ol class="am-rlist">%s</ol></div>' % (tag, intro, lis))


# ---------------------------------------------------------------- 8
def connections(back, fwd, gist_href, gist_label, extra=None):
    def _ul(items):
        return "".join('<li><span class="kind lab">%s</span><span>'
                       '<a href="%s">%s</a><span class="d">%s</span></span></li>'
                       % (k, h, t, d) for k, h, t, d in items)
    rows = _ul(back) + _ul(fwd)
    rows += ('<li><span class="kind play">gist</span><span><a href="%s">%s</a>'
             '<span class="d">the week this file belongs to, as one picture</span>'
             '</span></li>' % (gist_href, gist_label))
    if extra:
        rows += _ul(extra)
    return ('<div class="am-conn"><span class="am-tag">Connections</span>'
            '<ul class="links plain">%s</ul></div>' % rows)


# ---------------------------------------------------------------- 9
def recall(cards, blank_intro, tag="Recall sheet"):
    """Cards in the shape review.html already consumes, so they can be added to
    the deck rather than re-implemented. Nothing here duplicates an existing cid.
    """
    rows = "".join('<tr><td class="am-q">%s</td><td>%s</td></tr>' % (q, a)
                   for q, a in cards)
    blanks = "".join("<li>%s</li>" % q for q, _ in cards)
    return ('<div class="am-recall"><span class="am-tag">%s</span>'
            '<p>%s</p><ol class="am-blank">%s</ol>'
            '%s'
            '<p class="am-note">These are written in the same shape as the '
            '<a href="../review.html">spaced-repetition deck</a> and deliberately do '
            '<b>not</b> repeat any card already in it.</p></div>'
            % (tag, blank_intro, blanks,
               _det("show the answers", '<table class="am-rectab"><tbody>%s</tbody></table>' % rows)))


# ---------------------------------------------------------------- 10
def check(items, intro, tag="Mastery check"):
    lis = ""
    for ask, answer in items:
        lis += ('<li><p class="am-ask">%s</p>%s</li>'
                % (ask, _det("check", answer)))
    return ('<div class="am-check"><span class="am-tag">%s</span><p>%s</p>'
            '<ol class="am-clist">%s</ol></div>' % (tag, intro, lis))


# ---------------------------------------------------------------- wrapper
def render(am):
    """Assemble one page's Active Mastery block."""
    body = "".join(am["sections"])
    return ('<section id="active-mastery" class="am-root">'
            '<div class="am-head"><h2><span class="ico">&#127919;</span>Active Mastery</h2>'
            '<p class="am-lede">%s</p>'
            '<p class="am-rule">Everything above this line is the lesson, unchanged. '
            'Everything below asks you to <b>do</b> something with it. '
            '<b>Answers are hidden</b> &mdash; predict first, then reveal.</p></div>'
            '%s</section>' % (am["lede"], body))
