# -*- coding: utf-8 -*-
"""The gist of C1 Week 3."""
import math
from kit import key, trap
from gistkit import gistline, flow, sameskel, chain, bynumbers, retell, ladder, h2
from walkkit import cases, values, point, expr, chainset

_sig = lambda z: 1 / (1 + math.exp(-z))

def _n(v, p=4):
    s = "%.*f" % (p, v)
    return s.rstrip("0").rstrip(".") if "." in s else s

GIST = dict(
    course="C1", week="3", title="Classification", mins=12,
    scratch=["02-logistic-regression"],
    lede="Predicting a class instead of a number. Eleven lessons, and the loop is untouched "
         "— two things change and everything else follows from them.",
    body="".join([
        gistline("""Two substitutions. Put a <b>squash</b> on the output so it can be a
probability, and swap the squared miss for a <b>logarithm</b> so that confident mistakes
cost enormously. Everything else in the week — the boundary, overfitting, regularisation —
follows from those two."""),

        h2("🖼", "The week in one picture"),
        flow([
            ("in", "The same table, a different y",
             "y is now <b>0 or 1</b> — failed or passed, spam or not — rather than a price."),
            ("arw", "start from any guess"),
            ("loop", "repeat", [
                ("op", "The weighted sum, unchanged",
                 "<b>z = w · x + b</b>. Any number at all comes out: −40, 0, +17."),
                ("arw", "and here is change number one"),
                ("op", "Squash it — the sigmoid",
                 "Turns any number into 0…1. Now it can be read as <b>P(y = 1)</b>."),
                ("arw", "and here is change number two"),
                ("op", "The log loss",
                 "Right and confident is nearly free. <b>Wrong and confident costs "
                 "enormously</b>, heading for infinity."),
                ("arw", "plus a fine for large weights — that is λ"),
                ("op", "The gradient",
                 "<b>Character for character identical to linear regression.</b> Only what "
                 "f means has changed."),
                ("back", "Step downhill", "Exactly as before."),
            ]),
            ("arw", "the cost stops falling"),
            ("out", "A probability for any example", "Between 0 and 1."),
            ("arw", "and only THEN, separately"),
            ("stop", "A decision",
             "0.5 is the usual cut-off and it is <b>your choice</b>, not something the model "
             "learned."),
        ], cap="""Two boxes changed. The gradient box did not change at all — which is not a
coincidence, and is the neatest result in Course 1."""),

        h2("🔁", "Same skeleton, and what changed"),
        sameskel("""<b>Predict → measure the miss → find the slopes → step downhill →
repeat.</b> Unchanged. So is feature scaling, so is plotting J, so is the &alpha; ladder.""",
                 [("What y contains", "any number — a price", "<b>0 or 1</b> — a class"),
                  ("The output", "<code>w·x + b</code>", "<code>g(w·x + b)</code> — squashed to 0…1"),
                  ("The cost", "squared error", "<b>log loss</b> (binary cross-entropy)"),
                  ("Why that cost", "punishes big misses", "punishes <b>confident</b> misses, "
                                                           "without limit"),
                  ("The gradient formula", "(f − y)·x", "<b>(f − y)·x</b> — identical"),
                  ("New this week", "&mdash;", "<b>regularisation</b>, and it applies to "
                                               "both algorithms")]),

        h2("🔢", "Why not squared error? The numbers"),
        bynumbers("""Suppose the true answer is <b>1</b> and the model says 0.99, then 0.5,
then 0.01. Compare what each cost charges.""",
                  [("said 0.99 — squared error", _n((1-0.99)**2, 4), "0.0001. Fine."),
                   ("said 0.99 — log loss", _n(-math.log(0.99), 4), "also nearly free"),
                   ("said 0.50 — squared error", _n((1-0.5)**2, 4), "0.25"),
                   ("said 0.50 — log loss", _n(-math.log(0.5), 4), "the coin-flip reference point"),
                   ("said 0.01 — squared error", _n((1-0.01)**2, 4), "only 0.98 — barely worse than hedging"),
                   ("said 0.01 — log loss", _n(-math.log(0.01), 4), "<b>4.61 — over 6&times; the hedge</b>")],
                  close="""Squared error charges <b>0.98</b> for being 99%% confident and
completely wrong, against <b>0.25</b> for admitting you do not know. That is barely a
penalty. Log loss charges <b>4.61</b> against <b>0.69</b> — and heads for infinity as the
model approaches certainty about something false. <b>&minus;log(0.5) = 0.693</b> is worth
memorising: a classifier averaging below it is beating a coin flip."""),

        h2("⛓", "The pieces, in the order they hand to each other"),
        chain([
            dict(name="The sigmoid",
                 does="Turns any number into a probability. Very negative → near 0. Zero → "
                      "exactly 0.5. Very positive → near 1.",
                 formula=None,
                 say="g of z equals one over one plus e to the minus z.",
                 code="f = 1 / (1 + np.exp(-z))",
                 trap="Written naively it <b>overflows</b> at large negative z, because "
                      "<code>exp(1000)</code> does not fit in a float. Real code splits it "
                      "into two algebraically identical halves — see the build lane's file 02.",
                 feeds="a number between 0 and 1, which can now be scored as a probability."),
            dict(name="The log loss",
                 does="Two cases wearing one coat. Because y is always 0 or 1, one of the "
                      "two terms is always multiplied by zero and vanishes.",
                 say="minus y times log f, plus one minus y times log one minus f.",
                 code="loss = -(y*np.log(f) + (1-y)*np.log(1-f))",
                 trap="<code>log(0)</code> is infinite, so probabilities must be clipped "
                      "away from exactly 0 and 1 before the logarithm sees them.",
                 feeds="one number — and, remarkably, a gradient you have already met."),
            dict(name="The gradient",
                 does="Identical to linear regression. The only difference is that f now "
                      "means g(w·x + b).",
                 code="dj_dw = (X.T @ (f - y)) / m",
                 trap="This is <b>not a coincidence</b>. The sigmoid's derivative is "
                      "<b>g(1−g)</b> and the logarithm contributes <b>1/f</b>; they cancel "
                      "exactly. Pair either half with something else and the tidiness "
                      "disappears.",
                 feeds="the same descent step as always."),
            dict(name="Regularisation",
                 does="Add a fine for large weights, so the model stops becoming needlessly "
                      "certain.",
                 code="cost += (lam / (2*m)) * np.sum(w**2)",
                 trap="<b>b is never regularised.</b> Shrinking w flattens the model's "
                      "confidence, which is the point; shrinking b only slides the boundary "
                      "towards the origin, for no reason.",
                 feeds=None),
        ]),

        h2("🚧", "Two things that are decisions, not results"),
        key("""<p><b>The threshold is yours.</b> The model outputs 0.42. Whether that means
&ldquo;fail&rdquo; depends on a cut-off <b>you</b> choose. Raise it to 0.9 when a false alarm
is expensive; drop it to 0.15 when a miss is much worse. The model cannot help you — it does
not know what an action costs.</p>
<p><b>The boundary's shape is yours too.</b> The dividing line sits wherever <b>z = 0</b>.
With features x&#8321;, x&#8322; that is a <b>straight line</b>. With x&#8321;&sup2;,
x&#8322;&sup2; it is a <b>circle</b>. The model is always linear in z — a curved boundary
does not make it a neural network, it means you fed it curved features.</p>"""),

        h2("⚠️", "The hidden constraint nobody mentions"),
        trap("""<p>Rearranging the regularised update gives
<code>w := w(1 − αλ/m) − α·gradient</code>. So every iteration multiplies w by a shrink
factor <b>before</b> the ordinary step — which is why regularisation is also called
<b>weight decay</b>.</p>
<p>If <b>αλ/m</b> exceeds 2, that factor goes past <b>&minus;1</b> and the weights flip sign
and <b>grow</b> every iteration. A λ that is perfectly safe at one learning rate destroys the
model at another, and the symptom is &ldquo;training diverged&rdquo; — which sends most people
hunting for a bug in the gradient.</p>
<p>The build lane's file 02 demonstrates this with real numbers, including the exact knife
edge where the factor hits &minus;1.</p>"""),

        h2("🗣", "Say the week back"),
        retell([
            "Two reasons linear regression fails at classification — and which is the worse one.",
            "What the sigmoid guarantees about its output, and what g(0) is.",
            "Where the decision boundary is, and why it is <b>there</b>.",
            "What determines whether the boundary is straight or curved.",
            "Why squared error stops being usable once there is a sigmoid inside f.",
            "The log loss, as two cases, and why they can be folded into one line.",
            "What <b>&minus;log(0.5) = 0.693</b> is the reference point for.",
            "Why the logistic gradient is identical to the linear one, and why that is not luck.",
            "Underfitting vs overfitting: the symptoms, and why they need opposite fixes.",
            "What &lambda; does at 0 and at enormous, and why <b>b</b> is left out of the sum.",
            "Why &alpha; and &lambda; are not independent knobs.",
        ]),

        h2("🪜", "Where this week sits in the whole arc"),
        ladder("C1 W3", """This week completes the toolkit: you can now predict a
<b>number</b> and a <b>class</b>, and you can stop a model from over-committing. Everything
here reappears immediately. The sigmoid becomes the activation of a single neuron in C2 W1 —
<b>one neuron is exactly one logistic regression unit</b>. The log loss becomes the output
loss of every binary classifier you build. And regularisation becomes the
<code>weight_decay</code> argument in every modern optimiser. Course 1 ends here, and almost
nothing in it is left behind."""),
    ]),
)
