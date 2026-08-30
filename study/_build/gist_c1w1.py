# -*- coding: utf-8 -*-
"""The gist of C1 Week 1 — the whole week as one connected picture.

Nothing here is new material. Every claim on this page is taught in one of the
week's thirteen lessons; what this page adds is the joins between them, which
are exactly what a lesson-per-idea layout cannot show.

The arithmetic in the worked pass is COMPUTED below, not typed, so the page and
the numbers on it cannot disagree.
"""
from kit import decode, eq, eqp, key, kid, trap
from gistkit import (gistline, flow, carried, chain, bynumbers, retell, ladder, h2)

# ------------------------------------------------------------------ arithmetic
# Three houses small enough to check with a pencil. Sizes in 1000 sqft, prices
# in $100k. One full pass of the algorithm, from w = b = 0.
X = [1.0, 2.0, 3.0]
Y = [3.0, 5.0, 8.0]
M = len(X)
ALPHA = 0.1


def _predict(w, b):
    return [w * x + b for x in X]


def _cost(w, b):
    f = _predict(w, b)
    return sum((fi - yi) ** 2 for fi, yi in zip(f, Y)) / (2 * M)


def _grads(w, b):
    f = _predict(w, b)
    err = [fi - yi for fi, yi in zip(f, Y)]
    dw = sum(e * x for e, x in zip(err, X)) / M
    db = sum(err) / M
    return err, dw, db


_W0, _B0 = 0.0, 0.0
_ERR0, _DW0, _DB0 = _grads(_W0, _B0)
_J0 = _cost(_W0, _B0)
_W1 = _W0 - ALPHA * _DW0
_B1 = _B0 - ALPHA * _DB0
_J1 = _cost(_W1, _B1)

# and where it settles, so the page can say so truthfully
_w, _b = 0.0, 0.0
for _ in range(2000):
    _, _dw, _db = _grads(_w, _b)
    _w, _b = _w - ALPHA * _dw, _b - ALPHA * _db
_JEND = _cost(_w, _b)


def _n(x, p=4):
    """Format a number without a trailing-zero tail, so 2.5 is not 2.5000."""
    s = "%.*f" % (p, x)
    return s.rstrip("0").rstrip(".") if "." in s else s


# ------------------------------------------------------------------ the page
GIST = dict(
    course="C1", week="1", title="Introduction to Machine Learning",
    mins=12,
    scratch=["01-linear-regression"],
    lede="Thirteen lessons, one loop. This page is the week with the lessons removed — what "
         "goes in, what happens to it, what comes out, and which part runs again.",
    body="".join([
        gistline("""Pick a formula with a couple of unknown numbers in it. Write down a score that
says how wrong those numbers are. Then keep nudging them in whichever direction makes the score
fall. That is the entire week — and every algorithm in the rest of the specialization is a
variation on those three moves.""")

        + h2("🖼", "The week in one picture")
        + flow([
            ("in", "The data",
             "<b>m</b> houses. Each one is a size <var>x</var> and the price <var>y</var> it "
             "actually sold for. The prices are the part that makes this <i>supervised</i> "
             "learning: someone already knew the right answer."),
            ("arw", "start from any guess at all — <var>w</var> = 0, <var>b</var> = 0 will do"),
            ("loop", "repeat — typically a few hundred to a few thousand times", [
                ("op", "Predict",
                 "<var>f</var> = <var>w</var><var>x</var> + <var>b</var>, for all m houses at once."),
                ("arw", "subtract the real price from each prediction"),
                ("op", "Measure the miss",
                 "<var>J</var> = the average squared error, halved. <b>One number</b> "
                 "standing for the whole line."),
                ("arw", "ask which way that number falls"),
                ("op", "Slope of the cost",
                 "Two slopes, because there are two knobs: one for <var>w</var>, one for "
                 "<var>b</var>. Together they point straight downhill."),
                ("arw", "take one small step of size <var>α</var> in that direction"),
                ("back", "Move both knobs",
                 "<var>w</var> and <var>b</var> each drop by <var>α</var> × their own slope, "
                 "<b>at the same instant</b>."),
            ]),
            ("arw", "until the cost stops falling"),
            ("out", "A fitted line",
             "The <var>w</var> and <var>b</var> that no small change improves. Feed it a size it "
             "has never seen and it returns a price."),
        ], cap="""Everything else in the week is a detail hanging off one of these boxes. The
learning rate is how big the step is. Cost-function intuition is what the third box looks like when
you draw it. Nothing in Week 1 lives outside this picture."""),

        kid("""<p>You have a list of houses. For each one you know its size, and you know the
price it sold for.</p>
<p>You want a rule that turns a size into a price. The rule here is about as simple as a rule can
be: take the size, multiply it by one number, then add a second number. Those two numbers are the
only things you get to choose. Everything else is fixed.</p>
<p>At the start you have no idea what they should be, so you guess. Zero and zero will do.</p>
<p>Now check the guess. Go through every house. Work out what your rule predicts. See how far off
it is. Square each miss, so that being too high and being too low both count as bad, and take the
average. That gives you one number, and it tells you how bad your guess was.</p>
<p>Here is the only clever part. For each of your two numbers, you work out which way to nudge it
to make that average smaller. Then you nudge it — not far, just a small step.</p>
<p>Then you do the whole thing again. And again. A few thousand times.</p>
<p>Each time round, the average gets a little smaller. When it stops getting smaller, you stop.
The two numbers you are holding at that point are the answer.</p>"""),

        h2("🧱", "What this week rests on"),
        carried("""Not one piece of maths in this week is new. All of it was met in Foundations;
the week just puts it in a particular order and gives the arrangement a name.""",
                [("A derivative", "F0 W1 · 05",
                  "reads off which way the cost falls, and how steeply"),
                 ("A partial derivative", "F0 W1 · 06",
                  "two knobs means two slopes — one per knob, each measured with the other held still"),
                 ("Σ, summation", "F0 W1 · 07",
                  "adds the miss over all m houses"),
                 ("The mean", "F0 W1 · 17",
                  "divides that sum by m, so a bigger dataset does not automatically look worse"),
                 ("NumPy arrays", "F0 W2 · 03, 07",
                  "makes <code>f = w * x + b</code> compute all m predictions in one line"),
                 ("The dot product", "F0 W1 · 10",
                  "not needed yet — one feature. Next week it replaces the sum entirely")]),

        h2("⛓", "The pieces, in the order they hand to each other"),
        chain([
            dict(name="The model",
                 does="A straight line with two knobs on it. <var>w</var> tilts the line; "
                      "<var>b</var> slides it up and down.",
                 formula=eqp([
                     ('<var>f</var><sub><var>w</var>,<var>b</var></sub>(<var>x</var>)', "func-f",
                      "the prediction for one house"),
                     ' <span class="op">=</span> <var class="hl-a">w</var><var>x</var> '
                     '<span class="op">+</span> <var class="hl-b">b</var>',
                 ], "two unknown numbers, and that is the whole model"),
                 say="f of x equals w times x, plus b.",
                 code="f = w * x + b",
                 trap="Dropping <var>b</var> nails the line to the origin — it would insist a "
                      "house of zero size is worth exactly nothing, and then bend the slope to "
                      "compensate.",
                 feeds="a predicted price for every house. Useless on its own, until you can say "
                       "how wrong it is."),
            dict(name="The cost",
                 does="Squash all m misses down to a single number, so that two candidate lines "
                      "can be compared.",
                 formula=eqp([
                     ('<var>J</var>(<var>w</var>,<var>b</var>)', "cost-j", "how bad this line is"),
                     ' <span class="op">=</span> ',
                     ('<span class="frac"><span class="n">1</span><span class="d">2<var>m</var></span></span>',
                      "avg-factor", "average, and halve"),
                     ('<span class="sum">Σ</span>', "squared-term", "add over every house"),
                     ' (',
                     ('<var>f</var>(<var>x</var><sup>(<var>i</var>)</sup>) <span class="op">−</span> <var>y</var><sup>(<var>i</var>)</sup>',
                      "error-term", "this house’s miss"),
                     ')<sup>2</sup>',
                 ], "the average squared miss, halved"),
                 say="J of w and b equals one over two m, times the sum over every house of the "
                     "miss squared. The miss is the prediction minus the real price.",
                 code="cost = np.mean((f - y) ** 2) / 2",
                 trap="The square is not neutral. A single miss of 10 costs the same as a hundred "
                      "misses of 1, so one strange house can drag the whole line towards itself.",
                 feeds="one number. The question becomes: which way should w and b move to make "
                       "that number smaller?"),
            dict(name="The gradient",
                 does="The slope of the cost with respect to each knob — steepness and direction "
                      "in one quantity.",
                 formula=eq('<span class="frac"><span class="n">∂<var>J</var></span>'
                            '<span class="d">∂<var>w</var></span></span> '
                            '<span class="op">=</span> '
                            '<span class="frac"><span class="n">1</span><span class="d"><var>m</var></span></span>'
                            '<span class="sum">Σ</span>(<var>f</var>(<var>x</var><sup>(<var>i</var>)</sup>) '
                            '<span class="op">−</span> <var>y</var><sup>(<var>i</var>)</sup>)'
                            '<var>x</var><sup>(<var>i</var>)</sup>'
                            '<span class="gap"></span>'
                            '<span class="frac"><span class="n">∂<var>J</var></span>'
                            '<span class="d">∂<var>b</var></span></span> '
                            '<span class="op">=</span> '
                            '<span class="frac"><span class="n">1</span><span class="d"><var>m</var></span></span>'
                            '<span class="sum">Σ</span>(<var>f</var>(<var>x</var><sup>(<var>i</var>)</sup>) '
                            '<span class="op">−</span> <var>y</var><sup>(<var>i</var>)</sup>)',
                            "same sum, twice — the w version carries an extra x"),
                 say="The slope of J in the w direction equals one over m, times the sum of "
                     "every miss times that house&#8217;s size. The b slope is the same sum, "
                     "without the size.",
                 code="err   = f - y\ndj_dw = np.mean(err * x)\ndj_db = np.mean(err)",
                 trap="The extra <var>x</var> on the <var>w</var> slope is not a typo and not "
                      "optional: it says a miss on a <i>large</i> house is stronger evidence that "
                      "the <i>slope</i> is wrong. The bias has no such factor, because b affects "
                      "every house equally.",
                 feeds="two numbers saying which way is downhill — but not how far to walk."),
            dict(name="The update",
                 does="Walk downhill. Both knobs move, each by its own slope times one shared "
                      "step size.",
                 formula=eqp([
                     '<var class="hl-a">w</var> <span class="op">:=</span> <var class="hl-a">w</var> <span class="op">−</span> ',
                     ('<var>α</var>', "alpha-lr", "how big a step"),
                     '<span class="frac"><span class="n">∂<var>J</var></span><span class="d">∂<var>w</var></span></span>'
                     '<span class="gap"></span>'
                     '<var class="hl-b">b</var> <span class="op">:=</span> <var class="hl-b">b</var> <span class="op">−</span> ',
                     ('<var>α</var>', "alpha-lr", "the same step size"),
                     '<span class="frac"><span class="n">∂<var>J</var></span><span class="d">∂<var>b</var></span></span>',
                 ], "minus, because the slope points uphill and you want the other way"),
                 say="w becomes w minus alpha times the w slope. b becomes b minus alpha times "
                     "the b slope.",
                 code="w = w - alpha * dj_dw\nb = b - alpha * dj_db",
                 trap="Both updates must use the <b>old</b> w and b. Overwrite w first and the "
                      "b update is computed on a line that no longer exists — the classic Week 1 "
                      "bug, and it does not crash, it just quietly converges to the wrong answer.",
                 feeds=None),
        ]),

        h2("🔢", "The same pass, on numbers you can check"),
        bynumbers(
            """Three houses: sizes <b>%s</b> thousand square feet, prices <b>%s</b> hundred
thousand. Start at <var>w</var> = 0 and <var>b</var> = 0, with <var>α</var> = %s. Here is
<b>one</b> trip round the loop, in full.""" % (
                ", ".join(_n(x, 1) for x in X), ", ".join(_n(y, 1) for y in Y), _n(ALPHA, 2)),
            [("predictions <var>f</var>", ", ".join(_n(v, 2) for v in _predict(_W0, _B0)),
              "w = 0 and b = 0, so every house is predicted to be worth nothing"),
             ("misses <var>f</var> − <var>y</var>", ", ".join(_n(v, 2) for v in _ERR0),
              "all negative — every prediction is too low"),
             ("cost <var>J</var>", _n(_J0, 4),
              "the average of those misses squared, halved"),
             ("∂<var>J</var>/∂<var>w</var>", _n(_DW0, 4),
              "each miss weighted by that house&#8217;s size, averaged"),
             ("∂<var>J</var>/∂<var>b</var>", _n(_DB0, 4),
              "the same misses, unweighted, averaged"),
             ("new <var>w</var>", _n(_W1, 4),
              "0 &minus; %s &times; (%s). Two minuses: the step goes <b>up</b>" % (_n(ALPHA, 2), _n(_DW0, 4))),
             ("new <var>b</var>", _n(_B1, 4),
              "0 &minus; %s &times; (%s)" % (_n(ALPHA, 2), _n(_DB0, 4))),
             ("cost after one step", _n(_J1, 4),
              "down from %s. That fall is the only evidence that any of this works" % _n(_J0, 4))],
            close="""Run the same three lines 2,000 times and the cost settles at <b>%s</b>, with
<var>w</var> = %s and <var>b</var> = %s. Nothing else happens. There is no second idea in Week 1 —
only this, repeated.""" % (_n(_JEND, 4), _n(_w, 3), _n(_b, 3))),

        h2("🌀", "The two loops people confuse"),
        key("""<p>There are two different repetitions in this week and they are easy to mistake for
each other, because both are written with a Σ or a <code>for</code>.</p>
<p><b>The inner one runs over the m houses</b> and it happens <i>inside a single step</i>. Its job is
to produce two numbers, the gradients. It is finished before the knobs move at all.</p>
<p><b>The outer one runs over the steps</b> — iteration 1, 2, 3, … Its job is to move the knobs a
little each time.</p>
<p>So one full trip round the outer loop looks at <b>every</b> house exactly once. If you find
yourself updating <var>w</var> inside the loop over houses, you have merged the two, and you have
accidentally invented a different algorithm (a real one — stochastic gradient descent — but not
this one, and it will not match the lesson&#8217;s numbers).</p>"""),

        h2("🔡", "Every symbol this week, in one table"),
        decode([
            ("<var>x</var>", "“x”", "The input. One number per house this week: its size."),
            ("<var>y</var>", "“y”", "The true answer from the data — what the house actually sold for."),
            ("<var>ŷ</var>", "“y hat”", "The <b>prediction</b>. Plain y is truth, y-hat is a guess."),
            ("<var>m</var>", "“m”", "How many training examples there are."),
            ("<var>x</var><sup>(<var>i</var>)</sup>", "“x superscript i”",
             "The i-th example. <b>Round brackets always mean “which example”</b>, never a power."),
            ("<var>w</var>", "“w”, weight or slope", "How much the price rises per unit of size."),
            ("<var>b</var>", "“b”, bias or intercept", "The prediction when x is zero; slides the line vertically."),
            ("<var>f</var>", "“f of x”", "The model itself. Older material calls it h, for hypothesis."),
            ("<var>J</var>", "“J of w, b”", "The cost — one number saying how badly this line fits."),
            ("<var>α</var>", "“alpha”", "The learning rate: how far to step each iteration."),
            ("∂", "“partial dee”",
             "A derivative when there is more than one variable — the slope in one direction, others held still."),
            (":=", "“becomes”",
             "Assignment, not a claim of equality. <code>w := w − …</code> means <i>replace</i> w."),
        ]),

        h2("🚧", "What this week deliberately cannot do yet"),
        trap("""<p>Knowing the edges of the week is what stops the next one feeling arbitrary.</p>
<p><b>One input only.</b> Size, and nothing else. Bedrooms and age are Week 2.</p>
<p><b>Straight lines only.</b> The model literally cannot bend. Curves arrive in Week 2 as feature
engineering, not as a new algorithm.</p>
<p><b>Numbers out, never categories.</b> “How much?” is answerable; “is this spam?” is not, because
a straight line runs off to ±∞ and a probability may not. That is Week 3, and it changes exactly
two things: a squashing function on the output and a different cost.</p>
<p><b>Every example, every step.</b> With a million houses each step reads all million. Real systems
do not, and that is a later refinement — not a correction to anything here.</p>"""),

        h2("🗣", "Say the week back"),
        retell([
            "What makes a problem <i>supervised</i>, and which column of the table makes it so.",
            "What the model is, in one line, and what each of its two numbers does to the line.",
            "Why a cost function has to squash m misses into a single number.",
            "Why the misses are squared, and one consequence of that choice.",
            "What a gradient is, in plain words, without saying the word derivative.",
            "Why the <var>w</var> gradient carries an extra <var>x</var> and the <var>b</var> gradient does not.",
            "Why the update <b>subtracts</b> the gradient.",
            "What <var>α</var> controls, and what going too large and too small each look like.",
            "Why both knobs must be updated from the old values.",
            "Which of the two loops runs over houses and which runs over steps.",
        ]),

        h2("🪜", "Where this week sits in the whole arc"),
        ladder("C1 W1", """This is the loop itself, met at the one size where the whole of it fits
on a single page: two knobs, one straight line, three houses you can check with a pencil. Every
week after this one swaps a box in the picture for a bigger box &mdash; the line becomes a network,
the squared miss becomes a different score, the single step becomes a cleverer one &mdash; and
leaves the <b>shape</b> untouched. If the shape is solid now, the rest of the specialization is
mostly vocabulary. If it is not, nothing later will fix it, because nothing later re-teaches
it."""),
    ]),
)
