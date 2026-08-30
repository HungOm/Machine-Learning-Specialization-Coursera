# -*- coding: utf-8 -*-
"""The gist of C1 Week 2."""
import numpy as np
from kit import key, trap, decode
from gistkit import gistline, flow, sameskel, chain, bynumbers, retell, ladder, h2
from walkkit import cases, values, point, expr, chainset

_X = np.array([[2104., 5, 45], [1416., 3, 40], [852., 2, 35]])
_mu, _sd = _X.mean(0), _X.std(0)
_Xs = (_X - _mu) / _sd
_raw_rng = (_X.max(0) - _X.min(0))
_sc_rng = (_Xs.max(0) - _Xs.min(0))

def _n(v, p=3):
    s = "%.*f" % (p, v)
    return s.rstrip("0").rstrip(".") if "." in s else s

GIST = dict(
    course="C1", week="2", title="Regression with Multiple Variables", mins=11,
    scratch=["01-linear-regression"],
    lede="The same loop as last week, on a wider table. Nine lessons, and only two of them "
         "are genuinely new ideas.",
    body="".join([
        gistline("""Last week: one input, one weight. This week: many inputs, many weights,
and <b>the loop does not change at all</b>. What changes is the notation for a wider table,
one line of preparation that makes it trainable, and the discovery that you can bend the
line by feeding it cleverer columns."""),

        h2("🖼", "The week in one picture"),
        flow([
            ("in", "A wider table",
             "m houses, but now <b>n</b> facts about each: size, bedrooms, floors, age. "
             "<b>X</b> is (m, n) and <b>y</b> is (m,)."),
            ("arw", "and this step is new, and not optional"),
            ("op", "Scale every column",
             "<code>(x − μ) / σ</code>. Without it the cost surface is a long thin canyon "
             "and gradient descent zig-zags across it."),
            ("arw", "start from any guess"),
            ("loop", "repeat, exactly as last week", [
                ("op", "Predict, all at once",
                 "<b>f = X @ w + b</b>. One dot product per house, every house in one "
                 "operation."),
                ("arw", "the same squared miss, averaged"),
                ("op", "Cost", "Unchanged from Week 1."),
                ("arw", "now n slopes instead of 1"),
                ("op", "Gradient",
                 "<b>(X.T @ err) / m</b> gives one slope per feature, plus one for the bias."),
                ("back", "Move all n+1 numbers", "Simultaneously, from the old values."),
            ]),
            ("arw", "check it is actually converging, by plotting J"),
            ("out", "A fitted model on n features",
             "And, if you engineered a column, possibly a curve rather than a line."),
        ], cap="""Compare with last week's picture. One box is added at the top and one at
the bottom; the loop in the middle is identical."""),

        h2("🔁", "Same skeleton, and what changed"),
        sameskel("""<b>Predict → measure the miss → find the slopes → step downhill →
repeat.</b> Every box in that sentence is the same box as Week 1. Nothing about the
<i>algorithm</i> changed this week.""",
                 [("How many weights", "one, <b>w</b>", "<b>n</b> of them, a vector"),
                  ("The prediction", "<code>w*x + b</code>", "<code>w @ x + b</code> — a dot product"),
                  ("How many slopes", "two", "n + 1, computed in one matrix multiply"),
                  ("Preparation", "none needed", "<b>feature scaling</b> — now mandatory"),
                  ("What the model can fit", "a straight line", "still a straight line — "
                                                                "in whatever features you "
                                                                "hand it"),
                  ("Checking it worked", "look at the numbers", "<b>plot J against "
                                                                "iterations</b>")]),

        h2("🔢", "Why scaling is not tidying"),
        bynumbers("""Three houses, three features. Look at what the raw columns actually
span, then at what they span after scaling.""",
                  [("size, raw range", _n(_raw_rng[0], 1), "square feet"),
                   ("bedrooms, raw range", _n(_raw_rng[1], 1), "a count"),
                   ("age, raw range", _n(_raw_rng[2], 1), "years"),
                   ("size &mu;, &sigma;", "%s, %s" % (_n(_mu[0]), _n(_sd[0])), "computed on the training set only"),
                   ("size, scaled range", _n(_sc_rng[0], 3), ""),
                   ("bedrooms, scaled range", _n(_sc_rng[1], 3), ""),
                   ("age, scaled range", _n(_sc_rng[2], 3), "all three now comparable"),
                   ("2104 sq ft becomes", _n(_Xs[0][0], 4), "just over one standard deviation above average")],
                  close="""Size spans <b>%s</b> and bedrooms spans <b>%s</b> — a ratio of
about <b>417 to 1</b>. One shared learning rate cannot suit both: a step small enough not to
diverge on size is far too small to move bedrooms at all. After scaling all three spans are
within 2%% of each other, and one &alpha; works for everything."""
                  % (_n(_raw_rng[0],1), _n(_raw_rng[1],1))),

        h2("⛓", "The two genuinely new ideas"),
        chain([
            dict(name="Vectorization",
                 does="Replace the loop over features with a dot product. Same maths, same "
                      "answer, dramatically faster.",
                 formula=None,
                 code="f = X @ w + b        # not: for j in range(n): ...",
                 trap="It is not &ldquo;NumPy is clever&rdquo;. The loop pays Python "
                      "interpreter overhead <b>per element</b>; <code>@</code> hands one "
                      "contiguous block to compiled code that uses <b>SIMD</b> — one "
                      "instruction multiplying several pairs at once — and often several "
                      "cores. 10–100&times;, and the same reason GPUs matter.",
                 feeds="a model that can handle hundreds of features without the code "
                       "getting longer."),
            dict(name="Feature engineering",
                 does="Compute a new column yourself and hand it over, because the model "
                      "cannot invent it.",
                 code="X3 = X1 * X2          # area = frontage x depth",
                 trap="A linear model is a <b>weighted sum</b>. There is no choice of "
                      "w&#8321; and w&#8322; that produces a <b>product</b> — it is outside "
                      "what the model can represent, so no amount of data or training will "
                      "find it.",
                 feeds="and if the new column is a POWER of an old one, you get curves."),
            dict(name="Polynomial regression",
                 does="Feed it x, x&sup2;, x&sup3; and it fits a curve — while remaining, "
                      "in every technical sense, linear regression.",
                 code="X = np.c_[x, x**2, x**3]",
                 trap="&ldquo;Linear&rdquo; means linear in the <b>parameters w</b>, not in "
                      "x. But if x runs 1–1000 then x&sup3; runs 1–1,000,000,000, which "
                      "makes <b>scaling mandatory</b> rather than merely advisable.",
                 feeds=None),
        ]),

        h2("📉", "The cheapest diagnostic in machine learning"),
        key("""<p>Plot <b>J against iteration number</b>. Three lines of matplotlib, and it
diagnoses four situations by eye:</p>
<p><b>Falls then flattens</b> → converged; stop. <b>Falls, still falling</b> → run it
longer. <b>Oscillates</b> → &alpha; too large; reduce it. <b>Increases steadily</b> → &alpha;
far too large, or a bug.</p>
<p>And the rule that never fails: <b>if J ever increases between two iterations, &alpha; is
too large.</b> To choose &alpha;, try a ladder roughly ×3 apart — 0.001, 0.003, 0.01, 0.03,
0.1 — and keep the largest one that still falls smoothly. ×3 rather than +0.1 because
&alpha; acts multiplicatively, so equal <b>ratios</b> matter, not equal differences.</p>"""),

        h2("🚧", "The two scaling traps"),
        trap("""<p><b>Scaling before splitting.</b> Compute &mu; and &sigma; on the whole
dataset and you have leaked test information into training. Your test score comes out
optimistic and nothing tells you.</p>
<p><b>Forgetting to scale at prediction time.</b> The model was trained on standardised
inputs. Feed it a raw <code>2000</code> and it returns nonsense — with no error, because
2000 is a perfectly valid number.</p>
<p>One rule prevents both: <b>fit the scaler on the training set only</b>, then apply those
same numbers everywhere — validation, test, and every future prediction. That is exactly why
<code>sklearn</code> separates <code>fit</code> from <code>transform</code>.</p>"""),

        h2("🗣", "Say the week back"),
        retell([
            "What <b>n</b> is and what <b>m</b> is, and which one is rows.",
            "What <b>x<sub>2</sub><sup>(3)</sup></b> refers to — how many numbers is it?",
            "Why the vectorised form is not a shorthand for the sum but literally equal to it.",
            "Why <code>np.dot</code> is faster than a loop, without saying &ldquo;NumPy is clever&rdquo;.",
            "What unscaled features do to the shape of the cost surface, and why that slows descent.",
            "The z-score formula, and roughly what range you are aiming for.",
            "The two feature-scaling traps, and the one rule that prevents both.",
            "The four shapes of a J-against-iterations plot.",
            "Why &alpha; is searched in a ×3 ladder rather than in equal steps.",
            "Why a linear model cannot learn that <b>area = frontage × depth</b>.",
            "Why polynomial regression is still called linear regression, and what it forces you to do.",
        ]),

        h2("🪜", "Where this week sits in the whole arc"),
        ladder("C1 W2", """This is the week the algorithm stops being a toy. One feature was
enough to see the loop; <b>n</b> features is what real data looks like, and the vectorised
form you learn here is the exact same code shape you will write for a neural network — where
<b>X @ W</b> is a layer rather than a model. Feature engineering is also the last week where
<b>you</b> invent the useful combinations by hand; from C2 W1 onwards a hidden layer does
it for you, and that hand-off is the whole argument for neural networks."""),
    ]),
)
