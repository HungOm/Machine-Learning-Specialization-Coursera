# -*- coding: utf-8 -*-
"""Line-by-line walkthrough for 01_linear_regression.py."""
from walkkit import p, expr, chain, chainset, steps, cases, values, point, ascii_art

PICTURE = ([
    ("in", "Eight houses",
     "Each one has <b>three</b> numbers describing it &mdash; size, bedrooms, age &mdash; "
     "and the price it actually sold for."),
    ("arw", "start with every weight at zero"),
    ("loop", "repeat 1,500 times", [
        ("op", "Predict",
         "<b>f = X @ w + b</b>. One dot product per house: multiply each feature by its "
         "weight and add them up."),
        ("arw", "subtract the real price from each prediction"),
        ("op", "Measure the miss",
         "The average squared error, halved. <b>One number</b> for the whole model."),
        ("arw", "ask which way that number falls"),
        ("op", "Slope of the cost",
         "One slope per weight, plus one for the bias. Four numbers, all at once."),
        ("arw", "step downhill by &alpha;"),
        ("back", "Nudge all four numbers", "Each drops by &alpha; times its own slope."),
    ]),
    ("arw", "the cost has stopped falling"),
    ("out", "A price for any house",
     "Give it a size, a bedroom count and an age, and it returns a number."),
], "The whole program in one picture",
   "This is the picture the entire specialization is built on. Every later file swaps one "
   "box for a bigger one and leaves the shape alone.")

WALK = {

"prelude": (
    p("""Imports, and nothing else. Pure NumPy &mdash; no scikit-learn, no TensorFlow.
Everything below is arithmetic you could do on paper if you had the patience and the
time.""")
    + point("""The goal of this file: predict <b>a number</b>. How much is this house worth?
That is <b>regression</b>. File 02 will predict a <b>class</b> instead, and almost nothing
else will change.""")
),

"data": (
    p("""Eight houses. Each one has three numbers describing it, and one number to
predict.""")
    + values([("m = 8", "examples", "how many houses &mdash; the number of <b>rows</b>"),
              ("n = 3", "features", "size, bedrooms, age &mdash; the number of "
                                    "<b>columns</b>"),
              ("X", "(8, 3)", "the table of houses"),
              ("y", "(8,)", "the eight prices")],
             "the shapes, which are the thing to hold on to")
    + point("""<b>Rows are examples, columns are features.</b> That convention holds for the
whole specialization, and almost every shape error you will hit comes from momentarily
forgetting it.""")
    + p("""Eight houses is far too few to build anything real. It is exactly the right number
to <b>check by hand</b>, which is what this file is for.""")
),

"cost": (
    p("""The cost squashes all eight misses into <b>one number</b>, so two candidate models
can be compared.""")
    + expr("f = X @ w + b\ncost = np.mean((f - y) ** 2) / 2",
           "predict everything, then average the squared misses")
    + steps(["<code>X @ w</code> &mdash; one dot product per house. "
             "<b>(8,3) @ (3,) &rarr; (8,)</b>: eight predictions, in one operation.",
             "<code>+ b</code> &mdash; broadcasting adds the same bias to all eight.",
             "<code>f - y</code> &mdash; eight misses.",
             "<code>** 2</code> &mdash; square them, so too-high and too-low both count as "
             "bad and cannot cancel.",
             "<code>np.mean(...) / 2</code> &mdash; average, then halve."])
    + point("""The <b>&divide; 2</b> is pure convenience. Differentiating a square brings a
2 down in front; putting a 2 underneath in advance means it cancels and the gradient comes
out clean. It moves the cost's value but not <b>where its minimum is</b>, which is all that
matters.""")
),

"gradient": (
    p("""Two lines of arithmetic that carry the entire idea of learning.""")
    + expr("err   = f - y\ndj_dw = (X.T @ err) / m\ndj_db = err.mean()")
    + steps(["<code>err</code> &mdash; how wrong each house was. Eight numbers.",
             "<code>X.T</code> &mdash; the transpose, which turns the table on its side so "
             "the shapes line up: <b>(3,8) @ (8,) &rarr; (3,)</b>.",
             "That gives <b>one slope per feature</b> &mdash; each miss weighted by that "
             "house's value for that feature, then summed.",
             "<code>err.mean()</code> &mdash; the bias slope, with <b>no</b> feature "
             "weighting."])
    + point("""Why the feature weighting? Because <b>a miss on a big house is stronger
evidence that the size weight is wrong</b> than a miss on a small one. The bias has no such
factor because <b>b affects every house equally</b>, so no house's opinion counts for
more.""")
),

"check_gradient": (
    p("""This block is a <b>test</b>, and it is the reason to trust everything after it.""")
    + cases([("The calculus version",
              "<code>compute_gradient</code> &mdash; the formula you derived. Fast, and "
              "capable of being <b>silently wrong</b>."),
             ("The measured version",
              "Nudge one weight up a hair, nudge it down a hair, see how much the cost "
              "moved, divide. <b>No calculus involved</b>, so it cannot repeat a calculus "
              "mistake.")],
            "two independent ways to get the same slope")
    + values([("analytic", "[&minus;795.83, &minus;1150.94, &minus;6547.42]", "from the formula"),
              ("numeric", "[&minus;795.83, &minus;1150.94, &minus;6547.42]", "from measuring"),
              ("max difference", "3.9e&minus;06", "floating-point noise, not an error"),
              ("bias difference", "7.2e&minus;07", "same")],
             "what this block printed")
    + point("""The measured version is far too slow to train with &mdash; it re-runs the
whole cost twice for <b>every</b> weight &mdash; but it is exactly right for checking. This
is a real professional habit: <b>a wrong gradient does not crash</b>. It trains happily and
converges to the wrong answer.""")
),

"scaling": (
    p("""Look at what the columns actually contain before scaling.""")
    + values([("before", "[1.73, 2.0, 32.0]", "the range of each column"),
              ("after", "[3.04, 2.83, 3.30]", "all comparable")],
             "column ranges")
    + point("""Age spans <b>32</b> while size spans <b>1.73</b> &mdash; roughly
<b>18&times;</b> wider. That single fact makes the cost surface a long thin canyon rather
than a bowl.""")
    + p("""In a canyon, a gradient step points <b>across</b> the valley rather than along
it, so the path zig-zags; and &alpha; has to stay small enough not to bounce out, which
makes the crawl slower still. Scaling turns the canyon back into something round.""")
    + expr("Xs = (X - X.mean(0)) / X.std(0)",
           "subtract each column's mean, divide by its spread")
    + point("""<code>axis=0</code> is doing real work in <code>X.mean(0)</code>: it means
&ldquo;<b>one mean per column</b>&rdquo;, which is one per feature. Use <code>axis=1</code>
and you would get one per house, which is meaningless.""")
),

"descent": (
    p("""Three lines, repeated 1,500 times. Watch the cost column.""")
    + values([("iteration 0", "58,285", "the cost when every weight is still zero"),
              ("iteration 200", "240.9", "almost all the progress, in the first 200 steps"),
              ("iteration 600", "237.29", "refining"),
              ("iteration 1200", "237.2592", "converged &mdash; nothing is moving")],
             "what training printed")
    + point("""The shape is the important part: <b>an enormous drop, then a long
flattening</b>. By iteration 200 it is 99.6% of the way there, and the remaining 1,300
iterations buy four decimal places.""")
    + p("""That shape is what a healthy run looks like. If the cost ever <b>rises</b>
between two iterations, &alpha; is too large &mdash; and that one rule is the most useful
piece of debugging in the whole specialization.""")
),

"predict": (
    p("""The model is trained. Now use it.""")
    + chain(["2000 sq ft, 3 bed, 22 yrs", "$365.0k"], "a house it has never seen")
    + p("""And here it is against the eight houses it <b>was</b> trained on:""")
    + values([("predicted", "372, 336, 394, 229, 531, 364, 219, 506", ""),
              ("actual", "400, 330, 369, 232, 540, 400, 200, 480", "")],
             "training predictions vs. the truth (in $1000s)")
    + point("""It is close but nowhere near exact &mdash; house 1 is out by <b>28</b>, house
6 by <b>36</b>. That is <b>correct behaviour</b>, not failure. A model that hit all eight
exactly would have memorised eight houses and learned nothing about houses in general.""")
    + p("""New input must be scaled with the <b>same</b> mean and standard deviation the
training used. Feeding a raw 2000 into a model trained on standardised inputs returns
nonsense, silently.""")
),

"compare": (
    p("""The final check, and the most convincing one in the file. Linear regression has a
<b>closed-form</b> solution &mdash; the normal equation &mdash; that gets the exact answer
in one step with no iteration at all.""")
    + values([("normal equation", "[&minus;61.281, 71.749, 94.137, 0.019]", "solved directly"),
              ("gradient descent", "[&minus;61.280, 71.750, 94.137, 0.019]", "1,500 small steps"),
              ("agree to 3 dp", "True", "")],
             "two completely different methods, one answer")
    + point("""So the sixty lines above really do compute linear regression, and not merely
something that <i>looks</i> like it. Two independent methods arriving at the same four
numbers is about as strong a check as you get.""")
    + p("""Then why bother with gradient descent, if a formula solves it exactly? Because
the normal equation needs to <b>invert a matrix</b>, which costs roughly n&sup3; and becomes
impossible past a few thousand features &mdash; and because it exists <b>only</b> for
linear regression. Gradient descent works on everything in the rest of this
specialization.""")
),
}
