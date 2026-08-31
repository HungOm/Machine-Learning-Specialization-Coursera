# -*- coding: utf-8 -*-
"""Active Mastery for 02_logistic_regression.py. Values read off the running file."""
from masterykit import (section, prose, code, out, semantics, ledger, drill, peek,
                        predict, lab, breaks, invariant, wrong, reconstruct,
                        connections, recall, check)

AM = dict(
    lede="Eleven cards on the file where the output stops being a number and becomes a "
         "<b>probability</b> &mdash; and where two knobs start fighting each other.",
    sections=[

section("0", "&#129517;", "Before you run", "before", kind="orient",
    hook="Eighty students, two exam scores, and a threshold you choose yourself.",
    body=prose("""<p>Forty students who failed and forty who passed, each with two exam
scores. The blobs <b>overlap on purpose</b> &mdash; a perfectly separable dataset would let
the weights grow without limit and hide everything this file shows about &lambda;.</p>
<p><b>Three things to watch.</b> The gradient is character-for-character the same as file
01's. The accuracy goes <i>up</i> as &lambda; grows. And the last block shows &alpha; and
&lambda; are not independent knobs &mdash; a &lambda; that is safe at one learning rate
destroys the model at another.</p>""")
    + connections([], [], "../gist/c13.html", "C1 Week 3 &mdash; the gist",
        extra=[("lab", "../scratch/01-linear-regression.html", "File 01 first",
                "this is that file with two substitutions")])),

section("1", "&#127991;&#65039;", "What every variable is", "vars", kind="semantics",
    hook="Exam scores in points, probabilities in nothing, and a lambda that is not a property of students.",
    body=semantics([
        ("X", "(80, 2) float64", "the score table",
         "<b>One row = one student.</b> Two exam scores, out of 100.",
         "<b>exam points</b>",
         "<code>X[0]</code> is [45.01, 53.58] &mdash; student #1 scored <b>45 and 54</b>.",
         "Wider spread makes the classes easier to separate; more overlap makes it harder. "
         "The file deliberately chose overlap."),
        ("y", "(80,) float64", "the labels",
         "<b>0 = failed, 1 = passed.</b> Not a quantity &mdash; a name written as a number.",
         "<i>none &mdash; a class label</i>",
         "<code>y[0]</code> is 0.0: student #1 failed. The first 40 are all 0, the last 40 "
         "all 1.",
         "It is only ever 0 or 1, which is exactly why the two-term log loss collapses to "
         "one term per student."),
        ("Xs", "(80, 2) float64", "scaled scores",
         "The same students as &ldquo;how many standard deviations from the class average&rdquo;.",
         "<b>standard deviations</b>",
         "<code>Xs[0,0]</code> is &minus;0.6147 &mdash; student #1 was a bit below average "
         "on exam 1.",
         "This is what the model actually trains on, so w below is in <i>these</i> units."),
        ("w", "(2,) float64", "learned weights",
         "How much each exam pushes the decision. Trained on <b>scaled</b> scores.",
         "<b>log-odds per standard deviation</b>",
         "<code>w[0]</code> = 4.7222 against <code>w[1]</code> = 2.8503 &mdash; exam 1 "
         "matters about <b>1.66&times;</b> as much as exam 2.",
         "The <b>ratio</b> is the interpretable part. The absolute size is mostly a statement "
         "about how confident the model has been allowed to become, which is what &lambda; "
         "controls."),
        ("b", "float", "the bias",
         "Where the boundary sits when both scores are exactly average.",
         "<b>log-odds</b>",
         "&minus;0.0952 &mdash; almost exactly zero, so an average student is a near "
         "coin-flip. That is what a balanced 40/40 dataset should give.",
         "Shift it and you move the boundary without changing its tilt."),
        ("z", "(80,)", "the weighted sum",
         "The raw score before squashing. <b>Any</b> number: negative, zero, large.",
         "<b>log-odds</b>",
         "z = 0 is exactly the decision boundary, because that is where the sigmoid returns "
         "0.5.",
         "Every unit of z multiplies the odds by <b>e</b> &asymp; 2.718. That is what "
         "&ldquo;log-odds&rdquo; means in practice."),
        ("prob", "(80,) float64", "sigmoid output",
         "<b>P(this student passed)</b>. The model's actual answer.",
         "<b>probability, 0&ndash;1</b>",
         "<code>prob[0]</code> is 0.0171 &mdash; a <b>1.7%</b> chance student #1 passed. They "
         "did not.",
         "It never reaches 0 or 1 exactly, which is why the cost has to clip before taking a "
         "logarithm."),
        ("pred", "(80,) int", "the decision",
         "<b>Not the model's output.</b> The output is <code>prob</code>; this is what you "
         "get after applying a cut-off <b>you</b> chose.",
         "<i>class label</i>",
         "<code>pred = (prob >= 0.5)</code>. The 0.5 is a decision about consequences, not "
         "something learned.",
         "Move it to 0.9 and precision rises while recall falls. The model does not change "
         "at all."),
        ("lam", "float", "the regularisation strength",
         "The fine for large weights. <b>Not a property of students</b> &mdash; a statement "
         "about how much confidence you will permit.",
         "<i>unitless</i>",
         "At &lambda; = 0 the weight vector has length <b>5.5154</b>; at &lambda; = 100 it is "
         "<b>0.3225</b> &mdash; seventeen times smaller.",
         "And accuracy goes <b>up</b>, from 0.950 to 0.963. Less confidence, better "
         "decisions."),
    ],
    """Two rows carry the file. <b>prob</b> and <b>pred</b> are different things &mdash; one
is the model, one is your policy. And <b>lam</b> is the first quantity in this lane that
describes <i>you</i> rather than the data.""")
    + ledger([
        ("X, Xs", "(80, 2)", "<b>m=80</b> students &times; <b>n=2</b> exams"),
        ("y, prob, pred", "(80,)", "one per student. All flat, never (80,1)"),
        ("w", "(2,)", "one per <b>feature</b>"),
        ("Xs @ w", "(80,)", "n summed away &rarr; one score per student"),
        ("Xs.T @ err", "(2,)", "m summed away &rarr; one slope per feature"),
    ],
    """Identical to file 01's ledger, with m = 80 instead of 8. Nothing about the shapes
changed when the problem changed from regression to classification &mdash; which is the point
of the whole file.""")
    + drill("""<p><code>w = [4.7222, 2.8503]</code>. Without computing anything, say out
loud: <b>which exam does this model care about more, and by how much?</b> Then say what you
would need in order to state that in <i>exam points</i> rather than in the units above.</p>""",
    """<p>Exam 1, by a factor of <b>4.7222 / 2.8503 = 1.66</b>.</p>
<p>To restate it in points you need the column spreads &mdash; <code>X.std(0)</code>, which this file computes inline rather than storing. The weights are per
<b>standard deviation</b>, so dividing each by its column's spread converts them to
per-point. Without that division the ratio is still meaningful (both are in the same units)
but the individual numbers are not in exam points.</p>
<p>This is the same trap as file 01's <code>w[0]</code>, and it is worth meeting twice.</p>""")
    + peek("""Print what the model actually believes about individual students.""",
"""import numpy as np

def peek(name, arr):
    a = np.asarray(arr)
    first = a[0] if a.ndim > 1 else a
    print(f"{name:8s} shape={str(a.shape):7s} dtype={a.dtype}  "
          f"min={a.min():.4g}  max={a.max():.4g}")
    print(f"         first row: {np.round(np.atleast_1d(first)[:6], 4).tolist()}")""",
    [("peek(&quot;X&quot;, X); peek(&quot;y&quot;, y)", "after the <code>data</code> section"),
     ("peek(&quot;prob&quot;, prob); peek(&quot;pred&quot;, pred)", "after <code>evaluate</code>"),
     ("print(np.sort(prob)[38:42])", "the four students nearest the decision boundary")],
    prose("""<p>The last line is the interesting one. Sorting the probabilities and looking at
the middle shows you the students the model is genuinely unsure about &mdash; and those are
the only ones whose classification changes when you move the threshold.</p>
<p>Everything else is already confidently on one side. That is why moving a threshold trades
precision against recall in <b>small</b> steps rather than flipping the whole
dataset.</p>"""))),

section("2", "&#128302;", "Prediction checkpoints", "predict", kind="predict",
    hook="Including one where the accuracy goes the way most people do not expect.",
    body=predict([
        ("""Before reading the &lambda; table: as &lambda; goes from 0 to 100 the weights get
much smaller. <b>Predict what happens to training accuracy</b> &mdash; up, down, or flat.""",
         """<p>It goes <b>up</b>: 0.950 at &lambda; = 0, then <b>0.963</b> at &lambda; = 1, 10
and 100.</p>
<p>Most people predict down, reasoning that a penalised model must fit worse. But the
penalty removes <b>confidence</b>, not correctness &mdash; the boundary barely moves, the
model just stops shouting. And one student it was confidently wrong about is now merely
mildly wrong, which flips them to the right side.</p>"""),
        ("""The gradient here is <code>(X.T @ err) / m</code>, exactly as in file 01. Given
that the model now has a sigmoid in it, <b>is that a coincidence?</b>""",
         """<p><b>No.</b> The sigmoid's derivative is <code>g(1&minus;g)</code> and the
logarithm in the loss contributes <code>1/f</code>; they <b>cancel exactly</b>, leaving the
plain error term.</p>
<p>That cancellation is why sigmoid and log loss are a matched pair. Swap either half for
something else and the tidiness disappears &mdash; which is precisely the argument in C1 W3
for not using squared error here.</p>"""),
        ("""Accuracy is <b>0.950</b> with TP 38, FP 2, FN 2, TN 38. Predict precision and
recall before computing them.""",
         """<p>Both <b>0.950</b>, and F1 is 0.950 too.</p>
<p>They coincide only because FP and FN happen to both be 2, and accuracy agrees because the
classes are balanced 40/40. On a lopsided dataset all four numbers come apart immediately
&mdash; which is the entire point of C2 W3's insistence on reporting more than accuracy.</p>"""),
        ("""The decay experiment tries &alpha; = 0.5 with &lambda; = 320. The shrink factor
is <code>1 &minus; &alpha;&lambda;/m</code>. Compute it, then predict the outcome.""",
         """<p>1 &minus; (0.5 &times; 320 / 80) = <b>&minus;1.000</b> exactly &mdash; the
knife edge.</p>
<p>The weights <b>flip sign every iteration without shrinking</b>, so the run neither settles
nor blows up: it ends at <b>|w| = 538.06</b>. At &lambda; = 1000 the factor is &minus;5.25
and it diverges outright.</p>
<p>The rule: you are safe only while <code>&alpha;&lambda;/m &lt; 2</code>, so with m = 80
and &lambda; = 1000, &alpha; must be below <b>0.160</b>.</p>"""),
    ],
    """The last one is the most valuable thing in the file and appears in no lecture. Compute
the factor by hand before you look.""")),

section("3", "&#128295;", "Modify the copy", "lab", kind="lab",
    hook="Five edits, ending at the threshold &mdash; which is a decision, not a parameter.",
    body=lab([
        ("L1", "Change a value",
         "Move the decision threshold from 0.5 to <b>0.9</b>. Predict what happens to TP, FP, "
         "FN and TN before you run it.",
         "pred = (prob >= 0.9).astype(int)",
         """<p><b>FP falls, FN rises.</b> You now only call someone a pass when you are 90%
sure, so false alarms nearly vanish and misses go up.</p>
<p>Precision rises, recall falls, and <b>the model has not changed at all</b> &mdash;
<code>w</code>, <code>b</code> and <code>prob</code> are identical. You changed your policy,
not your model. That distinction is the whole reason the file's comment says
&ldquo;the threshold is a separate choice&rdquo;.</p>"""),
        ("L2", "Change a parameter",
         "Set <code>lam = 1000</code> at the file's usual <code>alpha = 0.5</code>. Predict "
         "the outcome from the shrink factor alone.",
         "w, b = gradient_descent(Xs, y, alpha=0.5, iters=2000, lam=1000)",
         """<p>Factor = 1 &minus; (0.5 &times; 1000 / 80) = <b>&minus;5.25</b>. The weights
flip sign <b>and grow</b> every iteration, so it <b>diverges</b> &mdash; you get
<code>inf</code> then <code>nan</code>.</p>
<p>The instructive part: the fix is <b>not</b> a smaller &lambda;. Keep &lambda; = 1000 and
drop &alpha; to 0.05 and the factor is back to 0.375, and the weights land at 0.041. Two
knobs, one constraint between them.</p>"""),
        ("L3", "Change the data",
         "Pull the two blobs apart so they no longer overlap, and re-run with "
         "<code>lam = 0</code>. Watch <code>np.linalg.norm(w)</code>.",
         "neg = rng.normal([30, 30], 6, size=(40, 2))\npos = rng.normal([85, 85], 6, size=(40, 2))",
         """<p>The weights <b>grow without limit</b> &mdash; run it longer and they keep
growing.</p>
<p>With perfectly separable data there is no best answer: any boundary that separates the
classes can be made better simply by scaling the weights up, which pushes every probability
closer to 0 or 1 and lowers the log loss forever. The optimum is at infinity.</p>
<p>This is why the file's blobs overlap on purpose, and it is the cleanest possible argument
for regularisation: &lambda; is what makes the problem <b>well-posed</b>, not just
better-behaved.</p>"""),
        ("L4", "Change an assumption",
         "Regularise the bias too &mdash; add <code>b</code> to the penalty and its gradient. "
         "Does anything visibly break?",
         "cost += (lam / (2*m)) * (np.sum(w**2) + b**2)\ndj_db += (lam / m) * b",
         """<p>Nothing crashes, and on <b>this</b> dataset almost nothing changes &mdash;
because b is already ~&minus;0.095, so shrinking it costs nothing.</p>
<p>Make the classes imbalanced (say 70 fails to 10 passes) and it does damage: the true b
should be strongly negative to reflect that passing is rare, and the penalty drags it towards
zero, systematically over-predicting passes.</p>
<p>The invariant: <b>shrinking w flattens confidence, which is the point; shrinking b just
moves the boundary for no reason.</b> Here the harm is invisible, which makes it a good
lesson about why &ldquo;it did not break&rdquo; is weak evidence.</p>"""),
        ("L5", "Explain it",
         "Explain why <code>prob</code> can never be exactly 0 or 1, and why the code clips it "
         "anyway.",
         None,
         """<p>The sigmoid is <code>1/(1+e^-z)</code>, and <code>e^-z</code> is never zero and
never infinite for a finite z, so the result is strictly between 0 and 1. Mathematically no
clipping is needed.</p>
<p>But <b>floating point</b> is not mathematics. At around z = &plusmn;37 the result rounds to
exactly 0.0 or 1.0 in float64, and <code>log(0)</code> is <code>-inf</code>, which poisons
the whole cost. <code>np.clip(f, 1e-12, 1-1e-12)</code> keeps it representable.</p>
<p>So the clip guards against the <b>machine</b>, not against the maths &mdash; which is the
same category of fix as file 05's max-subtraction.</p>"""),
    ],
    """L3 is the one worth doing properly. It shows that regularisation is not a tuning
nicety here &mdash; without it the problem has no finite answer at all.""")),

section("4", "&#128165;", "Break it, then repair it", "break", kind="debug",
    hook="Three breaks, one of which produces a perfect-looking model.",
    body=breaks([
        ("def sigmoid(z):\n    return 1.0 / (1.0 + np.exp(-z))     # the textbook one",
         "Replace the two-branch sigmoid with the textbook one-liner and call it with "
         "<code>-1000</code>. Predict what you see.",
         """<p>A <code>RuntimeWarning: overflow encountered in exp</code>, and the result is
still <b>0.0</b> &mdash; the right answer, with a warning.</p>
<p>That is what makes it insidious: it is <b>not</b> wrong here, just noisy. It becomes wrong
when the overflow lands somewhere a warning is suppressed, or when <code>inf/inf</code> gives
<code>nan</code> instead. The two-branch version guarantees the exponent is never positive,
so there is nothing to overflow.</p>"""),
        ("prob = sigmoid(X @ w + b)      # raw X, not Xs",
         "Score the students using the <b>unscaled</b> table with weights trained on the "
         "scaled one. Predict the accuracy.",
         """<p>It collapses &mdash; roughly <b>0.5</b>, a coin flip, and <b>no error is
raised</b>. The shapes are perfectly valid; the numbers are meaningless.</p>
<p>Exam scores run 15&ndash;99 while the weights expect values around &plusmn;2, so every z
is enormous and every probability saturates to 0 or 1 on the wrong side.</p>
<p>This is <b>training/serving skew</b>, four files before file 14 names it. The invariant:
<b>whatever transform the weights were trained through must be applied at prediction time,
with the same numbers.</b></p>"""),
        ("y[:40] = 1; y[40:] = 0      # labels swapped",
         "Swap every label. Predict what the trained weights do and what accuracy you get.",
         """<p>Accuracy stays <b>0.950</b> and the weights simply <b>flip sign</b>:
<code>w</code> becomes about [&minus;4.72, &minus;2.85].</p>
<p>Nothing warns you, and every metric looks excellent. The model has learned the mirror
problem perfectly &mdash; it now predicts &ldquo;fail&rdquo; for good students with the same
skill it used to predict &ldquo;pass&rdquo;.</p>
<p>The invariant that catches it: <b>check the sign of a weight against what you know about
the world</b>. Higher exam scores should push towards <i>pass</i>. A negative w[0] here is a
labelling bug, and only domain knowledge can see it.</p>"""),
    ],
    """The third one is the most important break in this file: every number looks right and
the model is exactly backwards.""")),

section("5", "&#9878;&#65039;", "The invariant", "invariant", kind="invariant",
    hook="Analytic against numerical, to eleven decimal places.",
    body=invariant("""<p><b>The hand-derived gradient must match a numerical measurement, and
the cost must never rise between iterations.</b></p>""",
    """<p>The file checks the first and prints the result: analytic and numeric both give
<b>[&minus;0.33510702, &minus;0.36844957]</b>, differing by <b>6.785e&minus;11</b>. That is
the floating-point noise floor, not agreement by luck.</p>
<p>It matters more here than in file 01 because the gradient now involves a sigmoid and a
logarithm whose derivatives happen to cancel. That cancellation is easy to get <i>almost</i>
right, and a nearly-right gradient trains happily to a worse answer with no symptom.</p>
<p>The second invariant needs no calculus at all: with a small enough &alpha;, the cost is
<b>mathematically guaranteed</b> to fall. So if it does not, the gradient is wrong &mdash;
which is exactly the &alpha;-versus-bug test.</p>""",
    """num = numeric_gradient(lambda w: compute_cost(Xs, y, w, b0, lam), w0)
assert np.max(np.abs(ana - num)) < 1e-8

c0 = compute_cost(Xs, y, w, b, lam)
dw, db = compute_gradient(Xs, y, w, b, lam)
assert compute_cost(Xs, y, w - 1e-4*dw, b - 1e-4*db, lam) <= c0""")),

section("6", "&#129535;", "Wrong mental models", "wrong", kind="myths",
    hook="Four, and the last one costs people whole afternoons.",
    body=wrong([
        ("The model outputs a class.",
         """<p>It outputs a <b>probability</b>. <code>prob[0] = 0.0171</code> is the model's
entire answer about student #1.</p>
<p><code>pred = (prob >= 0.5)</code> is <b>your</b> line, added afterwards. The 0.5 is not
learned, is not optimal, and should depend on what a false alarm costs versus a miss. Treating
the class as the output makes the threshold invisible &mdash; and then you cannot tune the one
knob that costs nothing to tune.</p>"""),
        ("Regularisation trades accuracy for generalisation.",
         """<p>Here it improves <b>both</b>: 0.950 &rarr; 0.963 on the training data itself,
while |w| falls from 5.5154 to 0.3225.</p>
<p>The penalty removes unearned <b>confidence</b> rather than correctness. The boundary
barely moves; the probabilities stop being extreme. It is not always free &mdash; push
&lambda; high enough and it does underfit &mdash; but the reflexive &ldquo;regularisation
costs accuracy&rdquo; is not what the numbers say.</p>"""),
        ("You can pick &lambda; independently of &alpha;.",
         """<p>The regularised update is <code>w := w(1 &minus; &alpha;&lambda;/m) &minus;
&alpha;&middot;gradient</code>. Both knobs appear in the <b>same product</b>.</p>
<p>At &alpha; = 0.5, &lambda; = 100 is fine (factor 0.375). At &lambda; = 320 the factor is
exactly <b>&minus;1</b> and |w| ends at 538. At &lambda; = 1000 it diverges. Same &lambda;
values are harmless at &alpha; = 0.05.</p>
<p>Safe only while <b>&alpha;&lambda;/m &lt; 2</b>.</p>"""),
        ("Training diverged, so my learning rate is too high.",
         """<p>Maybe &mdash; or your &lambda; is too high <i>for that</i> learning rate, which
is a different fix. Or your gradient has a sign error, which no amount of tuning repairs.</p>
<p>The test that separates them: set &alpha; absurdly small, say 1e&minus;4. If the cost now
falls, it was a step-size problem. If it still does not, <b>it is a bug</b>, because with a
small enough step a correct gradient is guaranteed to reduce the cost.</p>
<p>People lose afternoons here by tuning when they should be checking.</p>"""),
    ])),

section("7", "&#127959;&#65039;", "Reconstruction challenge", "reconstruct", kind="rebuild",
    hook="Rebuild it as a diff from file 01, which is what it actually is.",
    body=reconstruct([
        ("Explain", "In three sentences, state exactly what changed from file 01 &mdash; and "
         "what did not.",
         """<p>Two things changed: a <b>sigmoid</b> on the output so it can be read as a
probability, and <b>log loss</b> instead of squared error so that confident mistakes cost
enormously. A third thing was added: a <b>&lambda;</b> penalty on w.</p>
<p>What did not change: the gradient formula, the update rule, feature scaling, the shapes,
and the debugging method.</p>"""),
        ("Skeleton", "Write the signatures, and say which one gained an argument.",
         """<p><code>sigmoid(z)</code>, <code>compute_cost(X, y, w, b, lam=0.0)</code>,
<code>compute_gradient(X, y, w, b, lam=0.0)</code>,
<code>gradient_descent(X, y, alpha, iters, lam=0.0)</code>.</p>
<p>Everything that touches the cost gained <code>lam</code>, defaulting to 0 &mdash; so the
file can run the unregularised version by simply not passing it.</p>"""),
        ("Core", "Write the overflow-proof sigmoid from memory. Two branches.",
         """<p>For <code>z &ge; 0</code>: <code>1/(1+exp(-z))</code>. For <code>z &lt; 0</code>:
<code>exp(z)/(1+exp(z))</code>.</p>
<p>Multiply the top and bottom of the first by <code>exp(z)</code> and you get the second, so
they are the same formula &mdash; each arranged so the exponent it feeds to
<code>exp</code> is never positive. Check yours with <code>sigmoid(-1000)</code>: it must
return 0.0 with no warning.</p>"""),
        ("Minimal", "Build the smallest thing that shows &lambda; shrinking the weights: two "
         "&lambda; values, and print <code>np.linalg.norm(w)</code> for each.",
         """<p>Train at &lambda; = 0 and &lambda; = 100 on the same data and print both norms.
You should see roughly <b>5.5</b> and <b>0.32</b>.</p>
<p>If your two norms are similar, either your penalty is not reaching the gradient or your
&lambda; is being ignored &mdash; check that <code>(lam/m)*w</code> is actually added to
<code>dj_dw</code>.</p>"""),
        ("Verify", "Prove your rebuild is right without comparing to the original.",
         """<p>Three self-contained checks. Gradient check against a numerical estimate to
about 1e&minus;8. <code>sigmoid(-1000) == 0.0</code> with no warning. And
<code>g(-z) == 1 - g(z)</code>, which the file itself asserts.</p>
<p>If all three pass, the mathematics is right regardless of how you wrote it.</p>"""),
    ],
    """This file is a diff from file 01. Rebuilding it as a diff is both faster and more
honest than rebuilding it from scratch.""")),

section("8", "&#128279;", "Connections", "conn", kind="links",
    hook="Back to 01, forward to 03 &mdash; where this unit becomes a neuron.",
    body=connections(
        [("lab", "../scratch/01-linear-regression.html", "Back to 01",
          "same gradient, same update, same scaling")],
        [("lab", "../scratch/03-forward-propagation.html", "On to 03",
          "<b>one neuron is exactly this unit</b>: dot, bias, squash"),
         ("lab", "../scratch/05-softmax.html", "On to 05",
          "this output generalised from two classes to N")],
        "../gist/c13.html", "C1 Week 3 &mdash; the gist",
        extra=[("docs", "../reference.html", "Reference &mdash; C1 W3",
                "<code>c1w3-weight-decay</code> derives the shrink factor this file "
                "demonstrates")])),

section("9", "&#9670;", "Recall sheet", "recall", kind="recall",
    hook="Six cards, mostly about the two knobs.",
    body=recall([
        ("Why does the sigmoid here have <b>two branches</b>?",
         "So the exponent fed to <code>exp</code> is never positive. The textbook one-liner "
         "overflows at large negative z; these two are algebraically identical and each is "
         "safe on its own half."),
        ("<code>prob</code> and <code>pred</code> &mdash; which is the model's output?",
         "<b>prob.</b> <code>pred</code> is prob plus a threshold <b>you</b> chose. Changing "
         "the threshold changes every metric and changes the model not at all."),
        ("What happens to |w| and to accuracy as &lambda; goes 0 &rarr; 100?",
         "|w| falls <b>5.5154 &rarr; 0.3225</b> (17&times; smaller) and accuracy <b>rises</b> "
         "0.950 &rarr; 0.963. Less confidence, better decisions."),
        ("Write the shrink factor, and the condition for stability.",
         "<b>1 &minus; &alpha;&lambda;/m</b>. Stable while <b>&alpha;&lambda;/m &lt; 2</b>, "
         "i.e. &alpha; &lt; 2m/&lambda;. With m = 80 and &lambda; = 1000 that means "
         "&alpha; &lt; <b>0.160</b>."),
        ("At &alpha; = 0.5 and &lambda; = 320 the factor is exactly &minus;1. What happens?",
         "The weights <b>flip sign every step without shrinking</b> &mdash; neither settling "
         "nor exploding. The run ends at <b>|w| = 538.06</b>."),
        ("Your training diverged. Name the test that tells you whether it is &alpha; or a bug.",
         "Set &alpha; absurdly small (1e&minus;4). If the cost now falls it was the step size; "
         "if it still does not, the gradient is wrong &mdash; a small enough step is "
         "<b>guaranteed</b> to reduce the cost if the gradient is right."),
    ],
    """Cover them and answer aloud first.""")),

section("10", "&#9989;", "Mastery check", "check", kind="check",
    hook="Five, and none of them is in the C1 W3 quiz.",
    body=check([
        ("""Compute the shrink factor for &alpha; = 0.2, &lambda; = 500, m = 80, and say what
happens.""",
         """<p>1 &minus; (0.2 &times; 500 / 80) = 1 &minus; 1.25 = <b>&minus;0.25</b>.</p>
<p>Negative but greater than &minus;1, so the weights <b>flip sign every step while
shrinking</b>: 10 &rarr; &minus;2.5 &rarr; 0.625. Ugly, oscillating, but it converges. Push
&alpha;&lambda;/m past 2 and it would not.</p>"""),
        ("""Your model reports accuracy 0.95, precision 0.95, recall 0.95. What does that tell
you about the <b>dataset</b>, not the model?""",
         """<p>That it is <b>balanced</b>, and that FP happens to equal FN. Accuracy only
agrees with precision and recall when the classes are of similar size.</p>
<p>On a 0.5%-positive dataset, <code>print("negative")</code> scores 99.5% accuracy with
precision undefined and recall 0. Three matching numbers is a fact about your data.</p>"""),
        ("""You score new students with the raw exam scores instead of the scaled ones. Does
it crash, and what accuracy do you get?""",
         """<p>It does <b>not</b> crash &mdash; the shapes are fine. Accuracy collapses to
about <b>0.5</b>.</p>
<p>Scores of 15&ndash;99 fed to weights expecting &plusmn;2 give enormous z values, so every
probability saturates. This is training/serving skew, and the invariant is that the
prediction path must apply the <b>same</b> transform with the <b>same</b> numbers.</p>"""),
        ("""Someone swaps every label in the dataset and retrains. Which reported number
catches it?""",
         """<p><b>None of them.</b> Accuracy, precision, recall and F1 are all unchanged at
0.950 &mdash; the mirror problem is exactly as learnable.</p>
<p>What catches it is the <b>sign of w</b>: higher exam scores must push towards <i>pass</i>,
so a negative w[0] is a labelling bug. Only domain knowledge sees this, which is why
&ldquo;check the coefficient signs against what you know&rdquo; is a real review step.</p>"""),
        ("""Explain why perfectly separable data makes the unregularised problem have <b>no
answer</b>.""",
         """<p>If a boundary separates the classes cleanly, scaling every weight up by 10
pushes each probability closer to 0 or 1 and <b>lowers the log loss</b> &mdash; and you can
do that forever. The optimum is at infinity, so there is no finite best w.</p>
<p>&lambda; supplies the missing constraint, which is why the file's blobs overlap on
purpose. Regularisation here makes the problem <b>well-posed</b>, not merely
better-behaved.</p>"""),
    ],
    """None of these appears in the <a href="../quiz/c13.html">C1 W3 mock quiz</a>, which
covers the sigmoid, the decision boundary, log loss and the regularised cost. Every question
here needs a number this file printed.""")),
    ],
)
