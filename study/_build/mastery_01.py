# -*- coding: utf-8 -*-
"""Active Mastery for 01_linear_regression.py.

Every shape and value below was read off the running file. The one that
matters most: `w` lives in SCALED space, so w[0] = 40.894 is dollars per
standard deviation of size, NOT per 1000 sq ft. Divide by sigma[0] = 0.57
and you get 71.749, which is the physical number. That distinction is the
single most useful thing in this file's variable table and the lesson does
not spell it out, because it does not need to -- it is checking the maths,
not the units.
"""
from masterykit import (section, prose, code, out, semantics, ledger, drill, peek,
                        predict, lab, breaks, invariant, wrong, reconstruct,
                        connections, recall, check)

AM = dict(
    lede="Eleven cards that make you use <code>01_linear_regression.py</code> rather than "
         "read it again &mdash; starting with what its numbers are <b>in dollars</b>.",
    sections=[

section("0", "&#129517;", "Before you run", "before", kind="orient",
    hook="Eight houses, three columns, and one number you can check against a formula.",
    body=prose("""<p>Eight real-shaped houses: <b>size</b> in thousands of square feet,
<b>bedrooms</b>, and <b>age</b> in years, predicting a price in <b>$1000s</b>.</p>
<p><b>Three things to watch.</b> The cost drops from 58,285 to 240.9 in the first 200
iterations and then crawls. The analytic and numeric gradients agree to six decimal places.
And at the very end, a completely different method &mdash; the normal equation, which needs
no iteration at all &mdash; lands on the same four numbers.</p>
<p>That last one is the strongest check in the whole build lane: two unrelated routes to one
answer.</p>""")
    + connections([], [], "../gist/c11.html", "C1 Week 1 &mdash; the gist",
        extra=[("lab", "../scratch/02-logistic-regression.html", "Then 02",
                "the same skeleton with a squash and a different cost")])),

section("1", "&#127991;&#65039;", "What every variable is", "vars", kind="semantics",
    hook="Nine variables. One of them is in units nobody expects.",
    body=semantics([
        ("X", "(8, 3) float64", "the feature table",
         "<b>One row = one house that sold.</b> Column 0 size, column 1 bedrooms, column 2 age.",
         "1000 sq ft &middot; count &middot; years",
         "<code>X[2,1]</code> is 3.0 &mdash; house #3 had <b>3 bedrooms</b>.",
         "Add a column and every weight vector, every gradient and the normal equation all "
         "grow by one. n is not a free parameter."),
        ("y", "(8,) float64", "the answers",
         "What each house <b>actually sold for</b>.",
         "<b>$1000s</b>",
         "<code>y[0]</code> is 400.0 &mdash; house #1 sold for <b>$400,000</b>.",
         "Everything downstream inherits this unit. The cost is in <i>dollars squared</i> "
         "because of it."),
        ("mu", "(3,) float64", "column means",
         "The average house in this dataset: 2.05 thousand sq ft, exactly 3 bedrooms, 21 "
         "years old.",
         "same as each column",
         "<code>mu[1]</code> is exactly 3.0 &mdash; the bedroom counts happen to average "
         "precisely 3.",
         "These are computed on the <b>training set only</b>. Recompute them at prediction "
         "time and you have the skew bug from file 14."),
        ("sigma", "(3,) float64", "column spreads",
         "How much houses vary: &plusmn;0.57 thousand sq ft, &plusmn;0.71 bedrooms, "
         "&plusmn;9.7 years.",
         "same as each column",
         "<code>sigma[2]</code> is 9.7082 &mdash; ages in this set spread nearly a decade.",
         "It is the <b>divisor</b> that puts w into scaled units. Change it and w changes "
         "meaning, not just value."),
        ("Xs", "(8, 3) float64", "the scaled table",
         "The same houses, restated as &ldquo;how many standard deviations from average&rdquo;.",
         "<b>standard deviations</b>",
         "<code>Xs[0,0]</code> is 0.0811 &mdash; house #1 is a <b>very average size</b>, "
         "one twelfth of a deviation above the mean.",
         "This is the table gradient descent actually sees. It never meets a square foot."),
        ("w", "(3,) float64", "the learned weights",
         "<b>The trap.</b> These are trained on <code>Xs</code>, so they are dollars per "
         "<b>standard deviation</b>, not per physical unit.",
         "<b>$1000s per standard deviation</b>",
         "<code>w[0]</code> is 40.894: one standard deviation more size (0.57 thousand sq ft) "
         "is worth <b>$40,894</b>.",
         "Divide by <code>sigma</code> to get the physical number: 40.894 &divide; 0.57 = "
         "<b>71.749</b>, i.e. <b>$71.75 per square foot</b>. That is the number you would "
         "quote to a person."),
        ("b", "float", "the bias",
         "The prediction when every <b>scaled</b> feature is zero &mdash; which is the "
         "<b>average house</b>, not a house of zero size.",
         "<b>$1000s</b>",
         "368.875 &mdash; the average house in this set is worth about <b>$368,875</b>.",
         "This is why scaling makes b <i>more</i> meaningful, not less. Unscaled, b is "
         "&minus;61.28: the price of a nonexistent house with no floor, no bedrooms and an "
         "age of zero."),
        ("dj_dw", "(3,) float64", "the gradient",
         "How much total cost moves per unit change in each weight. <b>Its sign is the whole "
         "message.</b>",
         "cost per unit of w",
         "At the check point <code>dj_dw</code> is [&minus;795.8, &minus;1150.9, "
         "&minus;6547.4] &mdash; all <b>negative</b>, so every weight is currently too small "
         "and all three must go up.",
         "The magnitudes are wildly different here because this check runs on <b>unscaled</b> "
         "data &mdash; which is exactly the canyon that scaling fixes."),
        ("alpha", "float", "the learning rate",
         "The fraction of the gradient to trust in one step. <b>Not a property of houses at "
         "all.</b>",
         "<i>unitless</i>",
         "The parameter / hyperparameter line, drawn in units: everything above describes "
         "the world; this describes your search.",
         "Too big and the cost rises; too small and you wait. Neither changes what the right "
         "answer is."),
    ],
    """The row to stop on is <b>w</b>. Every other variable means what you would guess. That
one does not, and getting it wrong makes you quote a house price per standard deviation to
somebody who asked about square feet.""")
    + ledger([
        ("X", "(8, 3)", "<b>m=8</b> houses &times; <b>n=3</b> features"),
        ("y", "(8,)", "one price per house. <b>Not</b> (8,1)"),
        ("w", "(3,)", "one weight per <b>feature</b> &mdash; matches n, never m"),
        ("X @ w", "(8,)", "<b>(8,3) @ (3,) &rarr; (8,)</b>: the n is summed away"),
        ("X.T @ err", "(3,)", "<b>(3,8) @ (8,) &rarr; (3,)</b>: now the <b>m</b> is summed away"),
        ("mu, sigma", "(3,)", "one per column, from <code>axis=0</code>"),
    ],
    """Two dot products, and they sum away opposite axes. Predicting collapses <b>n</b> and
leaves one number per house; the gradient collapses <b>m</b> and leaves one number per
feature. If you can say which axis disappears where, you can debug this file blind.""")
    + drill("""<p>Without scrolling: <code>w[1] = 66.5647</code> and
<code>sigma[1] = 0.7071</code>. Say out loud, in one sentence, <b>what an extra bedroom is
worth</b> in dollars.</p>""",
    """<p>66.5647 &divide; 0.7071 = <b>94.137</b>, and y is in $1000s, so an extra bedroom is
worth about <b>$94,000</b>.</p>
<p>Check it against the normal equation printed at the end of the file: its second weight is
<b>94.1371</b>. Same number, reached without any scaling at all.</p>
<p>If you answered &ldquo;66.5&rdquo; you quoted the scaled weight, which is dollars per 0.71
of a bedroom &mdash; a quantity that does not exist.</p>""")
    + peek("""Print the four things worth knowing about any array.""",
"""import numpy as np

def peek(name, arr):
    a = np.asarray(arr)
    first = a[0] if a.ndim > 1 else a
    print(f"{name:8s} shape={str(a.shape):7s} dtype={a.dtype}  "
          f"min={a.min():.4g}  max={a.max():.4g}")
    print(f"         first row: {np.round(np.atleast_1d(first)[:6], 4).tolist()}")""",
    [("peek(&quot;X&quot;, X); peek(&quot;y&quot;, y)", "right after the <code>data</code> section"),
     ("peek(&quot;Xs&quot;, Xs); peek(&quot;mu&quot;, mu); peek(&quot;sigma&quot;, sigma)", "right after the <code>scaling</code> section"),
     ("peek(&quot;w&quot;, w)", "after <code>descent</code>, then divide it by <code>sigma</code> and print that too")],
    prose("""<p>The last one is the point. <code>w</code> prints as
<b>[40.894, 66.565, 0.180]</b> and <code>w / sigma</code> prints as
<b>[71.749, 94.137, 0.019]</b> &mdash; and only the second row is in units a person
uses.</p>
<p>Notice the third number: <b>+0.0185</b>, so this model believes an extra <b>year of
age adds about $18</b>. Positive. With eight houses that is noise, not a finding, and being
able to say so is the difference between reading an output and understanding it.</p>"""))),

section("2", "&#128302;", "Prediction checkpoints", "predict", kind="predict",
    hook="Four commitments, including the sign of a weight you have not seen.",
    body=predict([
        ("""Before looking at the output: the third feature is <b>age in years</b>, and older
houses are usually worth less. <b>Write down the sign you expect for w[2].</b>""",
         """<p><b>Positive</b> &mdash; <code>w[2] = +0.1797</code> scaled, <b>+0.0185</b>
raw. The model believes an extra year adds about <b>$18</b>.</p>
<p>Most people predict negative, and the world agrees with them. The model does not, because
with <b>8 houses</b> the age column carries almost no signal and whatever pattern it found is
noise. The honest reading is not &ldquo;old houses are worth more&rdquo; &mdash; it is
&ldquo;this coefficient is indistinguishable from zero at this sample size&rdquo;.</p>"""),
        ("""The cost starts at <b>58,285</b>. Given y is in $1000s and the cost is a
<b>halved mean squared error</b>, what does 58,285 mean in dollars? Estimate before
reading.""",
         """<p>The units are <b>($1000s)&sup2;</b>, which is why nobody quotes it. To get
back to dollars: multiply by 2, take the square root. &radic;(2 &times; 58,285) &asymp;
<b>341</b>, so the typical miss at iteration 0 is about <b>$341,000</b> &mdash; on houses
worth $200k to $540k.</p>
<p>That is what &ldquo;every weight is zero&rdquo; costs: the model predicts 0 for everything
and is wrong by roughly the whole price.</p>"""),
        ("""Will the cost still be falling at iteration 1,500? Commit to yes or no
<b>before</b> reading the printed column.""",
         """<p>Effectively <b>no</b>. It reads 237.2595 at iteration 1,000 and 237.2592 at
1,200 &mdash; a change in the fourth decimal place.</p>
<p>By iteration 200 it is at 240.9, which is <b>99.6%</b> of the total progress. The
remaining 1,300 iterations buy four decimal places. That shape &mdash; huge drop, long flat
tail &mdash; is what a healthy run looks like at every scale in this lane.</p>"""),
        ("""The file ends by comparing gradient descent against the <b>normal equation</b>.
Predict how closely they agree: 1 decimal place, 3, or 8?""",
         """<p><b>3</b>, and the file says so explicitly: <code>agree to 3 dp: True</code>.
Gradient descent gives <b>[&minus;61.280, 71.750, 94.137, 0.019]</b> against the exact
<b>[&minus;61.281, 71.749, 94.137, 0.019]</b>.</p>
<p>Not 8, because gradient descent <b>approaches</b> the answer and was stopped after a
finite number of steps. Not 1, because it got very close. The gap is the residual of an
iterative method, not an error.</p>"""),
    ],
    """Write each one down. The first is the interesting one: most people get it wrong, and
being wrong about it is more informative than being right.""")),

section("3", "&#128295;", "Modify the copy", "lab", kind="lab",
    hook="Five edits, ending in one that breaks the model without raising anything.",
    body=lab([
        ("L1", "Change a value",
         "Set <code>alpha</code> to <code>1.5</code> and re-run <code>descent</code>. Predict "
         "what the cost column does before you look.",
         "w, b, hist = gradient_descent(Xs, y, alpha=1.5, iters=1500)",
         """<p>It <b>diverges</b> &mdash; the cost grows, then becomes <code>inf</code>, then
<code>nan</code>. Each step overshoots the bottom by more than it started from, so the
overshoot compounds.</p>
<p>The rule this demonstrates: <b>if the cost ever increases between two iterations, alpha is
too large.</b> That single check is the most useful piece of debugging in Course 1, and it
costs one <code>print</code>.</p>"""),
        ("L2", "Change a parameter",
         "Drop <code>iters</code> to <b>50</b>. How much worse is the model, in dollars?",
         "w, b, hist = gradient_descent(Xs, y, alpha=0.1, iters=50)",
         """<p>Much less worse than you would guess. The cost after 50 iterations is still in
the high hundreds rather than 237, so the typical miss is roughly <b>$40k</b> instead of
<b>$22k</b>.</p>
<p>Worth noticing: 50 iterations gets you a usable model. The other 1,450 are polish. On a
dataset of 8 houses that polish is almost certainly fitting noise.</p>"""),
        ("L3", "Change the data",
         "Add a ninth house that is <b>enormous and cheap</b> &mdash; 5.0 thousand sq ft, 4 "
         "bedrooms, 10 years old, sold for 250. Re-run and compare <code>w[0]</code>.",
         "X = np.vstack([X, [5.00, 4, 10]])\ny = np.append(y, 250.0)",
         """<p><code>w[0]</code> collapses &mdash; the size weight falls sharply, because one
house is now insisting that size is nearly worthless.</p>
<p>With <b>m = 9</b>, a single contradictory example carries about <b>11%</b> of the total
squared error, and squared error punishes distance quadratically. This is the outlier
sensitivity that C1 W3 gives as reason two for not using squared error on
classification.</p>"""),
        ("L4", "Change an assumption",
         "Remove the bias entirely &mdash; force <code>b = 0</code> and never update it. "
         "Predict what happens to the weights.",
         "def gradient_descent(X, y, alpha, iters):\n"
         "    w, b = np.zeros(X.shape[1]), 0.0\n"
         "    for i in range(iters):\n"
         "        dw, db = compute_gradient(X, y, w, b)\n"
         "        w = w - alpha * dw      # b is never updated",
         """<p>The weights <b>inflate wildly</b> and the cost settles far higher. With scaled
features the average house sits at the origin, so with no bias the model is forced to predict
<b>$0</b> for an average house and must contort every weight to compensate.</p>
<p>This is the cleanest demonstration that <b>b is not a rounding term</b>. It carries the
entire level of the data; the weights only carry the differences from that level.</p>"""),
        ("L5", "Explain it",
         "Without looking: explain why <code>X.T @ err</code> has shape (3,) and not (8,), "
         "and what would have to be true for it to come out (8,).",
         None,
         """<p><code>X.T</code> is <b>(3, 8)</b> and <code>err</code> is <b>(8,)</b>. The
inner dimension &mdash; the <b>8</b>, the examples &mdash; is what gets summed away, leaving
one number per <b>feature</b>.</p>
<p>For an (8,) result you would need <code>X @ something_of_shape_3</code>, which is the
<i>prediction</i> step, not the gradient step. The two dot products in this file collapse
opposite axes, and that is the whole difference between them.</p>"""),
    ],
    """Work on a copy. Each level moves one step further from the surface, and L4 is the one
that teaches something the lesson never states outright.""")),

section("4", "&#128165;", "Break it, then repair it", "break", kind="debug",
    hook="Three breaks. Two of them raise nothing at all.",
    body=breaks([
        ("dj_dw = (X.T @ err) / m\ndj_db = err.mean()\nreturn -dj_dw, dj_db      # sign flipped",
         "Flip the sign of the <code>w</code> gradient only. <b>Predict whether it crashes, "
         "diverges, or converges to something wrong.</b>",
         """<p>It <b>diverges</b>, loudly &mdash; the cost climbs to <code>inf</code>. With
the sign flipped, the update walks <b>uphill</b> in w while still walking downhill in b, so
each step makes things worse.</p>
<p>The invariant: <b>subtracting the gradient must reduce the cost.</b> That is checkable in
one line &mdash; compute the cost before and after a single step &mdash; and it is why
plotting J is worth three lines of matplotlib.</p>"""),
        ("Xs = (X - X.mean(0)) / X.std(0)\nw, b, hist = gradient_descent(X, y, 0.1, 1500)   # note: X, not Xs",
         "Scale the data and then train on the <b>unscaled</b> table anyway. Predict the "
         "symptom.",
         """<p>It <b>diverges</b> at <code>alpha = 0.1</code>. The age column spans 32 while
size spans 1.73, so the cost surface is a canyon roughly <b>18&times;</b> longer than it is
wide, and a step sized for one axis is catastrophic on the other.</p>
<p>What makes this instructive: the <b>fix is not a smaller alpha</b>. A small enough alpha
converges, glacially, along the canyon floor. Scaling changes the <i>shape</i> of the problem
rather than the size of the steps.</p>"""),
        ("y = y.reshape(-1, 1)      # (8,) becomes (8,1)",
         "Make y a column vector instead of a flat array. <b>Predict whether anything "
         "errors.</b>",
         """<p><b>Nothing errors.</b> That is the whole point of including it.</p>
<p><code>f - y</code> broadcasts <b>(8,)</b> against <b>(8,1)</b> into <b>(8,8)</b> &mdash;
an 8&times;8 matrix of every prediction against every truth. The cost becomes a number that
means nothing, the gradient shape is wrong, and the model trains to nonsense without a single
warning.</p>
<p>The invariant, and it is the most valuable one in this file: <b>y must be (m,), not
(m,1)</b>. If a result has a surprising shape, broadcasting is almost always what happened
&mdash; and the defence is <code>print(y.shape)</code>, not more staring.</p>"""),
    ],
    """Predict the failure <b>mode</b>, not just the failure: loud, quiet, or silent. The
third one is silent, and silent is the one that costs you a day.""")),

section("5", "&#9878;&#65039;", "The invariant", "invariant", kind="invariant",
    hook="Two independent methods must land on the same four numbers.",
    body=invariant("""<p><b>Gradient descent and the normal equation must agree, and the
analytic gradient must match a numerical measurement.</b></p>""",
    """<p>These are two different kinds of check and the file runs both. The gradient check
says <i>your calculus is right</i> &mdash; it compares a derivative you differentiated by
hand against one measured by nudging a weight and watching the cost, and they agree to
<b>3.9e&minus;06</b>. The normal-equation check says <i>the whole program computes linear
regression</i> &mdash; a closed-form solution needing no iteration lands on the same
<b>[&minus;61.28, 71.75, 94.14, 0.0185]</b>.</p>
<p>A wrong gradient does not crash. It trains happily and converges somewhere worse, with no
symptom at all. These ten lines are how you find out.</p>""",
    """num = numeric_gradient(lambda w: compute_cost(X, y, w, b), w0)
assert np.max(np.abs(ana_w - num)) < 1e-4

Xb = np.c_[np.ones(m), X]
assert np.allclose(np.linalg.lstsq(Xb, y, rcond=None)[0],
                   np.r_[b_raw, w_raw], atol=1e-3)""")),

section("6", "&#129535;", "Wrong mental models", "wrong", kind="myths",
    hook="Five beliefs that survive the lesson and fail on the numbers.",
    body=wrong([
        ("w[0] is the price per square foot.",
         """<p>Not as printed. <code>w[0] = 40.894</code> was learned on <b>scaled</b>
features, so it is dollars per <b>standard deviation</b> &mdash; per 0.57 thousand sq ft.</p>
<p>The price per unit area is <code>w[0] / sigma[0]</code> = <b>71.749</b>, i.e. about
<b>$71.75 per square foot</b>. Quote the first number to an estate agent and you are out by
a factor of 1.75.</p>"""),
        ("b is the base price of a house.",
         """<p>Only because the features are scaled. In <b>scaled</b> space b = 368.875, which
is the price of the <b>average</b> house &mdash; genuinely meaningful.</p>
<p>In <b>raw</b> space the same model has b = <b>&minus;61.28</b>: minus sixty-one thousand
dollars, for a house with no floor area, no bedrooms and an age of zero. It is an
<b>anchor</b> that makes the line pass through the data, not a price. Any interpretation of b
depends entirely on what zero means for your features.</p>"""),
        ("A lower cost is always a better model.",
         """<p>Lower on <b>this</b> data. The file has <b>8 houses and 4 parameters</b>, so
the model has enormous freedom relative to the evidence.</p>
<p>There is no held-out set here at all, deliberately &mdash; this file is checking that
gradient descent works, not that the model generalises. Reading its final cost as a quality
score is exactly the mistake C2 W3 exists to prevent.</p>"""),
        ("Feature scaling is about making the numbers tidy.",
         """<p>It changes the <b>shape of the cost surface</b>. Age spans 32 and size spans
1.73 &mdash; roughly <b>18&times;</b> &mdash; which makes the bowl a long thin canyon.</p>
<p>A gradient step points <b>perpendicular to the contour</b>, which in a canyon points
across the valley rather than along it. You zig-zag, and you must keep alpha small enough not
to bounce out, which makes the crawl slower still. Scaling buys you a better direction
<b>and</b> a bigger step.</p>"""),
        ("The normal equation makes gradient descent pointless.",
         """<p>For <i>this</i> problem it is strictly better: exact, no alpha, no iterations.
The file uses it precisely because it is a trustworthy second opinion.</p>
<p>But it needs to invert an n&times;n matrix, which costs roughly <b>n&sup3;</b> and becomes
impractical past a few thousand features &mdash; and it exists <b>only</b> for linear
regression. Gradient descent works on every single thing in the rest of this lane.</p>"""),
    ])),

section("7", "&#127959;&#65039;", "Reconstruction challenge", "reconstruct", kind="rebuild",
    hook="Rebuild it, then prove it with the check the file itself uses.",
    body=reconstruct([
        ("Explain", "In four sentences, without the words <i>gradient</i> or <i>derivative</i>, "
         "say what this program does.",
         """<p>Roughly: it guesses a set of multipliers, one per column, plus an offset. It
uses them to predict every house's price and measures how far off it is on average. It then
works out which way to nudge each multiplier to make that average smaller, and nudges it a
little. It repeats until nudging stops helping.</p>"""),
        ("Skeleton", "From memory, write the signatures of <code>compute_cost</code>, "
         "<code>compute_gradient</code> and <code>gradient_descent</code>.",
         """<p><code>compute_cost(X, y, w, b)</code>, <code>compute_gradient(X, y, w, b)</code>
returning <code>(dj_dw, dj_db)</code>, and <code>gradient_descent(X, y, alpha, iters)</code>
returning the learned <code>w, b</code> and the cost history.</p>
<p>The detail worth getting right: the gradient returns a <b>tuple</b>, because there are two
different shapes &mdash; <b>(3,)</b> for the weights and a <b>scalar</b> for the bias.</p>"""),
        ("Core", "Write the cost and the gradient from scratch, vectorised, with no Python "
         "loop over examples.",
         """<p><code>f = X @ w + b</code>; <code>cost = np.mean((f - y) ** 2) / 2</code>;
<code>dj_dw = (X.T @ (f - y)) / m</code>; <code>dj_db = (f - y).mean()</code>.</p>
<p>If you wrote a loop over <code>range(m)</code> it is still correct &mdash; check it
against the vectorised version and they must agree exactly, which is the same check file 03
runs on its two versions of <code>dense</code>.</p>"""),
        ("Minimal", "Fit the same data with <b>no</b> gradient descent at all, in one line.",
         """<p><code>np.linalg.lstsq(np.c_[np.ones(m), X], y, rcond=None)[0]</code> gives
<b>[&minus;61.281, 71.749, 94.137, 0.0185]</b> directly.</p>
<p>That one line is the whole file's answer. Everything else exists to show that an iterative
method reaches it too &mdash; which matters because the iterative method is the one that
survives into every later file.</p>"""),
        ("Verify", "Prove your rebuild is right without comparing it to the original source.",
         """<p>Two checks, both self-contained. Run a numerical gradient against your analytic
one and require agreement to about 1e&minus;5. Then solve the same problem with
<code>lstsq</code> and require your trained weights &mdash; converted back to raw space by
dividing by <code>sigma</code> &mdash; to match to three decimals.</p>
<p>If both pass, your rebuild is correct regardless of how you wrote it.</p>"""),
    ],
    """Each stage checks itself. You should never need to open the original to know whether
you got it right.""")),

section("8", "&#128279;", "Connections", "conn", kind="links",
    hook="The first file in the lane. Everything after it is this loop with one box swapped.",
    body=connections(
        [("lab", "../f0/w1-10-dot-product.html", "Back to the dot product",
          "the operation inside every prediction here")],
        [("lab", "../scratch/02-logistic-regression.html", "On to 02 &mdash; logistic regression",
          "same skeleton; a squash on the output and a different cost"),
         ("lab", "../scratch/03-forward-propagation.html", "On to 03 &mdash; forward propagation",
          "this unit, stacked into layers")],
        "../gist/c11.html", "C1 Week 1 &mdash; the gist",
        extra=[("docs", "../reference.html", "Reference &mdash; C1 W1",
                "<code>c1w1-derivatives</code> and <code>c1w1-drill-cost</code> cover the "
                "algebra this file implements")])),

section("9", "&#9670;", "Recall sheet", "recall", kind="recall",
    hook="Six cards about units and shapes &mdash; none of them in your deck.",
    body=recall([
        ("<code>w[0] = 40.894</code>. What is that a price <b>per</b>?",
         "Per <b>standard deviation of size</b> (0.57 thousand sq ft), because w was trained "
         "on scaled features. Per square foot it is <code>w[0]/sigma[0]</code> = <b>71.749</b>, "
         "about <b>$71.75</b>."),
        ("What are the units of the cost <code>J</code>, and why does nobody report it?",
         "<b>($1000s)&sup2;</b> &mdash; squaring the miss squares the unit. To get back to "
         "dollars: &radic;(2J). At J = 58,285 that is a typical miss of about <b>$341,000</b>."),
        ("What does <code>b = 368.875</code> mean here, and what is it in raw space?",
         "In scaled space it is the price of the <b>average</b> house, ~$368,875. In raw space "
         "the same model has <b>b = &minus;61.28</b> &mdash; an anchor, not a price."),
        ("Why does <code>X.T @ err</code> give (3,) while <code>X @ w</code> gives (8,)?",
         "They sum away opposite axes. Predicting collapses <b>n</b>, leaving one number per "
         "house; the gradient collapses <b>m</b>, leaving one number per feature."),
        ("<code>w[2]</code> is <b>positive</b> for house age. Is the model saying old houses "
         "are worth more?",
         "No. It is +0.0185 (~$18/year) on <b>8 houses</b> &mdash; indistinguishable from "
         "zero at this sample size. The honest reading is &ldquo;no signal&rdquo;, not "
         "&ldquo;a finding&rdquo;."),
        ("What breaks, silently, if <code>y</code> has shape (8,1) instead of (8,)?",
         "<code>f - y</code> broadcasts to <b>(8,8)</b> &mdash; every prediction against every "
         "truth. No error, meaningless cost, wrong gradient shape."),
    ],
    """Cover the answers and say each one aloud first. Producing it from memory is what makes
it stick.""")),

section("10", "&#9989;", "Mastery check", "check", kind="check",
    hook="Five questions, and none of them is in the C1 W1 quiz.",
    body=check([
        ("""State, in dollars, what one extra bedroom is worth according to this model &mdash;
and show the arithmetic that gets you from a printed number to that answer.""",
         """<p><code>w[1] = 66.5647</code>, <code>sigma[1] = 0.7071</code>, so
66.5647 &divide; 0.7071 = <b>94.137</b>, and y is in $1000s &rarr; about <b>$94,000</b>.</p>
<p>Confirm against the normal equation's second weight: <b>94.1371</b>. If you cannot do this
conversion, you cannot report this model's findings to anyone.</p>"""),
        ("""Name the one variable in this file whose value says nothing about houses, and say
what it is a property of instead.""",
         """<p><code>alpha</code>. It is a property of your <b>search</b>, not of the data
&mdash; it controls how far you step, and changing it changes how long you wait, never what
the right answer is. That is the parameter / hyperparameter line.</p>"""),
        ("""The cost at iteration 0 is 58,285 and at the end 237.26. Convert both to a typical
error in dollars.""",
         """<p>&radic;(2 &times; 58,285) &asymp; <b>$341,000</b>, and &radic;(2 &times; 237.26)
&asymp; <b>$21,800</b>.</p>
<p>So the model went from being wrong by roughly a whole house price to being wrong by about
$22k on houses worth $200k&ndash;$540k. Stating a cost in the unit somebody can act on is a
skill this file never asks for and every real project does.</p>"""),
        ("""Without running it: you scale <code>X</code> but pass raw <code>X</code> to
<code>gradient_descent</code>. Does it crash, converge slowly, or diverge &mdash; and why?""",
         """<p><b>Diverges</b>, at this alpha. Nothing about the shapes is wrong, so nothing
raises &mdash; but age spans 32 while size spans 1.73, and a step sized for one is
catastrophic for the other.</p>
<p>The tell is the cost column rising. A smaller alpha would converge, slowly; scaling fixes
the <b>shape</b> rather than the step size.</p>"""),
        ("""Why does this file bother with the normal equation at all, given it is strictly
better here?""",
         """<p>As an <b>independent check</b>. Two unrelated methods landing on the same four
numbers is strong evidence the sixty lines above really compute linear regression and not
merely something that looks like it.</p>
<p>And it is not better in general: it inverts an n&times;n matrix (~n&sup3;) and exists only
for linear regression. Gradient descent is what survives into every later file.</p>"""),
    ],
    """None of these appears in the <a href="../quiz/c11.html">C1 W1 mock quiz</a>, which
covers the model, the cost formula, the update rule and the learning rate. Every question
here needs a number this file printed.""")),
    ],
)
