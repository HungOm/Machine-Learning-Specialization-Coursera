# -*- coding: utf-8 -*-
"""Active Mastery for 05_softmax.py. Values read off the running file.

Depth note (brief §6): this file's centre of gravity is NUMERICAL, not
conceptual. Two of its five printed blocks exist only to break the naive
version, so predictions and breaks carry the weight here.
"""
from masterykit import (section, prose, code, out, semantics, ledger, drill, peek,
                        predict, lab, breaks, invariant, wrong, reconstruct,
                        connections, recall, check)

AM = dict(
    lede="Eleven cards on the file that spends most of its length <b>breaking</b> the obvious "
         "implementation &mdash; because that is what <code>from_logits=True</code> is for.",
    sections=[

section("0", "&#129517;", "Before you run", "before", kind="orient",
    hook="Three data regimes in one file, and only one of them has names.",
    body=prose("""<p>Softmax turns arbitrary scores into probabilities that sum to 1. The
concept takes two lines. The <b>numerics</b> take the rest of the file.</p>
<p><b>Three regimes to keep apart.</b> <code>logits</code> and <code>yv</code> are random
numbers used only to check a gradient. <code>X</code> and <code>y</code> are three synthetic
blobs used to train. And <code>raw = [3.0, 2.5, &minus;1.0]</code> is the only thing here with
real names: <b>car, bus, pedestrian</b>.</p>
<p><b>Watch for:</b> a nan, a &minus;inf, and the fact that adding 100 to every score changes
nothing at all.</p>""")
    + connections([], [], "../gist/c22.html", "C2 Week 2 &mdash; the gist",
        extra=[("lab", "../scratch/02-logistic-regression.html", "File 02 first",
                "this is that file's output generalised from two classes to N")])),

section("1", "&#127991;&#65039;", "What every variable is", "vars", kind="semantics",
    hook="Nine variables. Only three of them are about anything.",
    body=semantics([
        ("z", "(3,) float64", "the stability demo input",
         "<b>Nothing.</b> <code>[400, 0, &minus;400]</code> chosen purely to make the naive "
         "route underflow.",
         "<i>none</i>",
         "<code>z[0]</code> is 400. Not 400 of anything &mdash; just far enough out to break "
         "float64.",
         "Shrink it to [4, 0, &minus;4] and every failure in this file disappears. The "
         "numbers were picked to expose the bug."),
        ("logits", "(5, 4) float64", "random scores for the gradient check",
         "<b>Nothing.</b> Five fake examples, four fake classes, drawn from a normal.",
         "<i>none &mdash; log-odds-ish</i>",
         "<code>logits[0]</code> is [10.16, &minus;3.34, &minus;6.82]&hellip; &mdash; the "
         "first row of noise.",
         "Only the <b>gradient</b> is being checked here, and a gradient is correct or not "
         "regardless of what the numbers mean."),
        ("yv", "(5,) int64", "the true classes for that check",
         "<b>Nothing.</b> Random integers 0&ndash;3.",
         "<i>class index</i>",
         "<code>yv</code> is [3, 0, 0, 3, 3] &mdash; it is an <b>index</b>, not a quantity. "
         "Class 3 is not three times class 1.",
         "This is the difference between an integer label and a number. Averaging class "
         "labels is meaningless; averaging their probabilities is not."),
        ("means", "(3, 2) float64", "the blob centres",
         "Where the three synthetic clusters sit: <b>(0,0), (4,4), (8,0)</b>. Abstract "
         "2-D points, but genuinely separable.",
         "<i>arbitrary units</i>",
         "The blobs are 4 apart with a spread of 1.1, so they overlap slightly &mdash; which "
         "is why the model reaches 0.994 and not 1.000.",
         "Move them to 1 apart and accuracy collapses; to 20 apart and it hits 1.0. The "
         "difficulty is a dial the file set."),
        ("X, Xs", "(180, 2) float64", "the training points",
         "180 points, 60 per class. <code>Xs</code> is the scaled version the model actually "
         "trains on.",
         "<i>arbitrary</i> / standard deviations",
         "<code>X[0]</code> is a point from blob 0; <code>Xs[0]</code> is that same point in "
         "standard deviations from the overall mean.",
         "Same scaling story as files 01 and 02: <b>W below is per standard deviation</b>, "
         "not per raw unit."),
        ("W, b", "(2, 3) and (3,)", "the learned parameters",
         "<b>One column per class.</b> Two features feeding three class scores.",
         "<i>log-odds per standard deviation</i>",
         "<code>W.shape[1]</code> is <b>3</b> &mdash; the class count. Adding a fourth class "
         "means a fourth column here and a fourth entry in b.",
         "Softmax is <b>shift-invariant</b>, so adding the same constant to every column of "
         "b changes literally nothing about the predictions."),
        ("P", "(m, k) float64", "softmax output",
         "<b>P(class j | this example)</b>. Each <b>row</b> sums to exactly 1.",
         "<b>probability</b>",
         "The rows sum to 1, not the columns. Getting that axis backwards is the classic "
         "softmax bug and it produces plausible nonsense.",
         "Every output depends on <b>all</b> the scores &mdash; the only activation where "
         "that is true, and the reason they are coupled."),
        ("raw", "(3,) float64", "the multi-label demo scores",
         "<b>The one thing here with real names:</b> <code>[3.0, 2.5, &minus;1.0]</code> is "
         "<b>car, bus, pedestrian</b>.",
         "<i>log-odds</i>",
         "<code>raw[0]</code> = 3.0 is the score for <b>car</b>. Through a sigmoid that is "
         "<b>0.9526</b> &mdash; a 95% chance there is a car.",
         "Push the pedestrian score up and, under <b>softmax</b>, car and bus must both go "
         "<i>down</i>. Under <b>sigmoids</b> they need not move at all. That is the whole "
         "distinction."),
        ("eps", "float", "the gradient-check nudge",
         "A property of the <b>check</b>, not the model. 1e&minus;6.",
         "<i>unitless</i>",
         "Never used in training. Delete the check and the classifier is identical.",
         "Same trade as file 04: too large measures a chord, too small loses the difference "
         "to cancellation."),
    ],
    """Read the <b>units</b> column. Six of these nine mean nothing physical &mdash; they are
scaffolding for demonstrating numerics. <code>raw</code> is the exception, and it is the row
that makes the last section land."""),
    ),

section("2", "&#128302;", "Prediction checkpoints", "predict", kind="predict",
    hook="Four, and two of them are about numbers a float cannot hold.",
    body=predict([
        ("""<code>softmax_naive([1000, 999, 998])</code>. The correct answer is
[0.665, 0.245, 0.090]. <b>Predict what the naive version returns.</b>""",
         """<p><b>[nan, nan, nan]</b> &mdash; all three destroyed.</p>
<p><code>exp(1000)</code> has 435 digits and does not fit in a float, so it becomes
<code>inf</code>. Then <code>inf / inf</code> is <b>nan</b>, and nan spreads through
everything downstream like ink.</p>
<p>The maths was never extreme. Only the intermediate step was.</p>"""),
        ("""Does <code>softmax([2,1,0])</code> equal <code>softmax([12,11,10])</code>? Commit
before checking.""",
         """<p><b>Yes, identically</b> &mdash; both are
<b>[0.665241, 0.244728, 0.090031]</b>.</p>
<p>Softmax depends only on the <b>differences</b> between scores. Adding a constant multiplies
the top and bottom by the same factor, which cancels exactly.</p>
<p>That is not a curiosity: it is <i>why</i> subtracting the max is free, and therefore why
the stable version is allowed to exist.</p>"""),
        ("""<code>softmax([400, 0, -400])</code> then <code>log</code> of it. Predict the
third element.""",
         """<p><b>&minus;inf</b>.</p>
<p>The probability underflows to exactly <code>0.0</code> &mdash; 1.9e&minus;174 is fine, but
the third is smaller than float64 can represent &mdash; and <code>log(0)</code> is negative
infinity. A gradient of inf is no gradient at all.</p>
<p><code>log_softmax</code> computed <b>directly</b> gives <b>&minus;800</b>, which is
perfectly usable. Same maths, different order of operations, and only one survives.</p>"""),
        ("""Training starts at loss <b>1.0986</b>. Is that number arbitrary?""",
         """<p><b>No</b> &mdash; it is <b>log(3)</b> = 1.0986, exactly the loss of assigning
1/3 to every one of three classes.</p>
<p>So it is a check, not a coincidence: a 3-class model whose initial loss is <i>not</i>
log(3) has a bug in its initialisation. For k classes the number to expect is log(k).</p>"""),
    ],
    """Two of these are about float64's limits rather than about softmax. That ratio is
honest: the concept is easy and the implementation is where the work is.""")),

section("3", "&#128295;", "Modify the copy", "lab", kind="lab",
    hook="Five, ending on the axis mistake that produces plausible nonsense.",
    body=lab([
        ("L1", "Change a value",
         "Change <code>z</code> from [400, 0, &minus;400] to [40, 0, &minus;40] and re-run "
         "the <code>logsoftmax</code> block. Does the &minus;inf go away?",
         "z = np.array([40., 0., -40.])       # was 400",
         """<p><b>Yes</b> &mdash; e<sup>&minus;80</sup> is about 1.8e&minus;35, which float64
holds comfortably, so the naive route returns &minus;80 rather than &minus;inf.</p>
<p>Which is the uncomfortable part: <b>the naive version works right up until it does
not</b>. It fails on a cliff, not a slope, and nothing in a normal test run tells you how
close you are to the edge.</p>"""),
        ("L2", "Change a parameter",
         "Remove the max-subtraction from <code>softmax</code> and re-run the whole file. "
         "Which blocks break?",
         "def softmax(z, axis=-1):\n    e = np.exp(z)          # was np.exp(z - z.max(axis, keepdims=True))\n"
         "    return e / e.sum(axis, keepdims=True)",
         """<p>The <code>stable</code> block breaks immediately &mdash; it prints nan for
[1000, 999, 998]. <b>Training still works fine</b>, because those logits stay small.</p>
<p>So a test suite built only from the training path would pass. The failure needs an input
nobody thought to try, which is exactly why the file includes one.</p>"""),
        ("L3", "Change the data",
         "Move the blobs from 4 apart to <b>1</b> apart and retrain. Predict the accuracy "
         "before you run it.",
         "means = np.array([[0., 0.], [1., 1.], [2., 0.]])    # was 4 and 8",
         """<p>Accuracy falls sharply &mdash; roughly the 0.6&ndash;0.8 range rather than
0.994 &mdash; because with a spread of 1.1 the blobs now overlap heavily.</p>
<p>The model is not worse. <b>The problem is harder</b>, and a linear boundary cannot separate
clouds that genuinely intersect. Distinguishing &ldquo;my model is bad&rdquo; from &ldquo;this
problem has a ceiling&rdquo; is exactly what C2 W3's baseline section is for.</p>"""),
        ("L4", "Change an assumption",
         "Add the same constant to every column of <code>b</code> after training, then "
         "re-measure accuracy.",
         "b = b + 5.0        # every class shifted equally",
         """<p><b>Accuracy is unchanged</b>, to the last example.</p>
<p>Softmax is shift-invariant, so adding the same number to every score is a no-op. That
means <code>b</code> is <b>over-parameterised</b> by exactly one degree of freedom: you could
fix b[0] = 0 and lose nothing.</p>
<p>Try adding 5.0 to only <b>one</b> column and it changes everything &mdash; which is the
proof that it is the <i>differences</i> that carry the model.</p>"""),
        ("L5", "Explain it",
         "Change <code>softmax(logits, axis=1)</code> to <code>axis=0</code> in "
         "<code>grad_logits</code>. Predict whether it errors, then explain what it now "
         "computes.",
         "P = softmax(logits, axis=0)      # was axis=1",
         """<p><b>No error.</b> The shapes are identical, so everything downstream runs.</p>
<p>But it now normalises down <b>columns</b> instead of across <b>rows</b> &mdash; so instead
of &ldquo;the probability of each class for this example&rdquo; you get &ldquo;the probability
of each example for this class&rdquo;, which is not a thing anyone wants. Rows no longer sum
to 1.</p>
<p>The gradient check catches it instantly. Without the check you get a model that trains,
converges, and is quietly wrong &mdash; the single most valuable habit in this lane.</p>"""),
    ],
    """L2 is the one to sit with: the bug it introduces is invisible to every test built from
the happy path.""")),

section("4", "&#128165;", "Break it, then repair it", "break", kind="debug",
    hook="Four breaks, three of them silent.",
    body=breaks([
        ("P = softmax(logits, axis=1)\nreturn (P - onehot) / m        # drop the / m",
         "Remove the division by m from the gradient. Predict what the check reports.",
         """<p>It fails by a factor of exactly <b>5</b> &mdash; which is m, the number of
examples in the check.</p>
<p><b>A round-number ratio is always a scaling bug</b>, never a calculus one. That single
heuristic localises it before you re-derive anything, and it is the same signal as file 04's
factor-of-4.</p>"""),
        ("loss = -np.log(P[np.arange(m), y])        # P built from softmax, not log_softmax",
         "Compute the loss by taking softmax and then log, rather than log_softmax directly. "
         "When does it break?",
         """<p>Not on this training data &mdash; and that is the problem. It breaks when any
probability underflows to exactly 0, which needs a logit gap of roughly 750 or more.</p>
<p>Then <code>log(0)</code> is &minus;inf, the loss is inf, and every gradient is nan. The
model does not degrade; it stops entirely, at some unpredictable point during a long
run.</p>
<p>The invariant: <b>never form a probability you only intend to take the log of.</b> That is
precisely what <code>from_logits=True</code> buys you in Keras.</p>"""),
        ("onehot = np.zeros_like(P)\nonehot[y, np.arange(m)] = 1        # indices swapped",
         "Swap the two indices when building the one-hot. Predict whether it errors.",
         """<p>On a <b>square</b> batch &mdash; 4 examples, 4 classes &mdash; it does
<b>not</b> error. It silently marks the wrong cells and you train against transposed
labels.</p>
<p>Here m = 5 and k = 4, so it happens to raise an <code>IndexError</code>. That is
<b>luck</b>, not safety: change the batch size to 4 and the same bug goes quiet.</p>
<p>The invariant: <b>a shape check that passes is not a correctness check.</b> The gradient
check is what actually catches this.</p>"""),
        ("Xs = X        # skip the scaling",
         "Train on the raw blob coordinates instead of the scaled ones.",
         """<p>It still converges, but <b>more slowly</b> &mdash; and the useful observation
is <i>why it is not worse</i>.</p>
<p>The blobs span roughly 0&ndash;8 in <b>both</b> features, so the two columns are already on
similar scales. There is no canyon here, unlike file 01 where age spanned 32 and size 1.73.</p>
<p>The invariant: <b>scaling matters when features have different ranges</b>, not as a ritual.
Knowing when a step is unnecessary is as useful as knowing when it is not.</p>"""),
    ],
    """Two of these four break only on inputs the training path never produces. That is the
theme of the whole file.""")),

section("5", "&#9878;&#65039;", "The invariant", "invariant", kind="invariant",
    hook="Rows sum to 1, shifting changes nothing, and the gradient is p − y.",
    body=invariant("""<p><b>Every softmax row sums to exactly 1; adding a constant to every
score changes nothing; and the gradient is exactly <code>p &minus; y</code>.</b></p>""",
    """<p>The three together pin the implementation down completely. The first catches an axis
mistake. The second is what makes the max-subtraction legal &mdash; and the file demonstrates
it by printing <code>softmax([2,1,0])</code> and <code>softmax([12,11,10])</code> as identical
to six decimals.</p>
<p>The third is the payoff: the softmax derivative carries a factor of <b>p</b> and the log
inside cross-entropy contributes <b>1/p</b>, and they annihilate. The file checks it
numerically and reports <b>2.805e&minus;10</b>. Same cancellation as sigmoid and log loss in
file 02, which is why these pairs are always used together.</p>""",
    """assert np.allclose(softmax(logits, axis=1).sum(axis=1), 1.0)
assert np.allclose(softmax(z), softmax(z + 100.0))
assert np.max(np.abs(ana - num)) < 1e-7""")),

section("6", "&#129535;", "Wrong mental models", "wrong", kind="myths",
    hook="Five, and the last one decides an architecture.",
    body=wrong([
        ("The max-subtraction is an approximation for stability.",
         """<p>It is <b>exact</b>. Softmax depends only on the differences between scores, so
subtracting the maximum multiplies numerator and denominator by the same factor and cancels
perfectly.</p>
<p>You are not trading accuracy for safety &mdash; you are getting the identical answer by a
route that cannot overflow. The file proves it by printing both.</p>"""),
        ("Underflow is less serious than overflow.",
         """<p>Overflow gives you <code>nan</code>, which is <b>loud</b> &mdash; it propagates
and you notice immediately.</p>
<p>Underflow gives you <code>0.0</code>, which is a perfectly ordinary number. It only becomes
&minus;inf once something takes its log, possibly thousands of iterations later. The quiet
failure is the dangerous one.</p>"""),
        ("<code>from_logits=True</code> is a performance flag.",
         """<p>It is a <b>correctness</b> flag. It tells the loss to take the <b>raw scores</b>
and apply an algebraically rearranged formula that never builds the intermediate probability
&mdash; so nothing can round to 0 or 1 and produce an infinite log.</p>
<p>And it carries a real trap: your output layer must then actually be <b>linear</b>. Leave a
softmax on it as well and the squash is applied <b>twice</b>. It trains, badly, and nothing
warns you.</p>"""),
        ("Softmax outputs are independent probabilities.",
         """<p>They are <b>coupled by construction</b>. The denominator contains every score,
so raising one probability <b>must</b> lower the others &mdash; they are forced to sum to
1.</p>
<p>It is the only activation with this property, and you cannot compute one softmax output on
its own.</p>"""),
        ("Softmax is the default output for any multi-class problem.",
         """<p>Only when the classes are <b>mutually exclusive</b>. The file's last block is
the counterexample: the same scores <code>[3.0, 2.5, &minus;1.0]</code> for <b>car, bus,
pedestrian</b> give <b>[0.6154, 0.3733, 0.0113]</b> under softmax and
<b>[0.9526, 0.9241, 0.2689]</b> under independent sigmoids, summing to <b>2.1457</b>.</p>
<p>A photo can contain a car <b>and</b> a bus. Softmax cannot say that &mdash; it is built to
make the options compete. The question that picks the head is not about accuracy: <b>can two
answers be true at once?</b></p>"""),
    ])),

section("7", "&#127959;&#65039;", "Reconstruction challenge", "reconstruct", kind="rebuild",
    hook="Rebuild it so it survives inputs the training data never produces.",
    body=reconstruct([
        ("Explain", "In three sentences, say what softmax does and what its two moves each "
         "accomplish.",
         """<p>It turns a list of arbitrary scores into probabilities. <b>exp</b> makes
everything positive, because scores routinely are not and probabilities may not be. <b>Dividing
by the total</b> forces them to sum to exactly 1, which is what makes it a distribution.</p>"""),
        ("Skeleton", "Write the four signatures, and say which two exist only for numerics.",
         """<p><code>softmax(z, axis=-1)</code>, <code>log_softmax(z, axis=-1)</code>,
<code>cross_entropy(logits, y)</code>, <code>grad_logits(logits, y)</code>.</p>
<p><code>log_softmax</code> exists <b>only</b> for numerics &mdash; mathematically it is
log(softmax(z)). And <code>cross_entropy</code> takes <b>logits</b>, not probabilities, for
the same reason.</p>"""),
        ("Core", "Write the stable softmax and log_softmax from memory.",
         """<p><code>e = np.exp(z - z.max(axis, keepdims=True)); return e / e.sum(axis, keepdims=True)</code>.</p>
<p>And <code>log_softmax</code> is <code>z - z.max(...) - np.log(np.exp(z - z.max(...)).sum(axis, keepdims=True))</code>
&mdash; the log of the sum, never the log of a probability.</p>
<p><code>keepdims=True</code> is not optional: without it the subtraction broadcasts against
the wrong axis and you get a silently wrong answer on any non-square input.</p>"""),
        ("Minimal", "Build the smallest input that makes a naive implementation fail, and "
         "one that makes it fail <b>silently</b>.",
         """<p>Loud: <code>[1000, 999, 998]</code> &rarr; nan from overflow.</p>
<p>Silent: <code>[400, 0, &minus;400]</code> &rarr; the third probability underflows to
exactly 0.0, which looks like a perfectly ordinary probability until something takes its
log.</p>"""),
        ("Verify", "Check your rebuild without comparing to the original.",
         """<p>Four self-contained assertions: rows sum to 1; <code>softmax(z)</code> equals
<code>softmax(z + 100)</code>; <code>softmax([1000,999,998])</code> contains no nan; and your
analytic gradient matches a numerical one to ~1e&minus;7.</p>
<p>If the shift test passes but the [1000,...] test fails, you have the maths right and the
implementation wrong &mdash; which is the whole point of this file.</p>"""),
    ],
    """The verify stage here is unusually strong: four assertions fully pin the
implementation.""")),

section("8", "&#128279;", "Connections", "conn", kind="links",
    hook="02 generalised to N classes; 04's backward pass, reused.",
    body=connections(
        [("lab", "../scratch/02-logistic-regression.html", "Back to 02",
          "sigmoid + log loss is this file with k = 2"),
         ("lab", "../scratch/04-backpropagation.html", "Back to 04",
          "the same cancellation, and the same gradient check")],
        [("lab", "../scratch/12-fine-tuning.html", "On to 12",
          "a 4-class head trained exactly this way, then adapted")],
        "../gist/c22.html", "C2 Week 2 &mdash; the gist",
        extra=[("docs", "../reference.html", "Reference &mdash; F0 W3",
                "<code>f0-softmax-grad</code> derives why the p and 1/p cancel")])),

section("9", "&#9670;", "Recall sheet", "recall", kind="recall",
    hook="Six cards, mostly numerical.",
    body=recall([
        ("Why is subtracting the max <b>free</b> rather than an approximation?",
         "Softmax depends only on the <b>differences</b> between scores. Subtracting a "
         "constant multiplies top and bottom by the same factor, which cancels exactly. "
         "<code>softmax([2,1,0])</code> and <code>softmax([12,11,10])</code> are identical."),
        ("<code>softmax([1000,999,998])</code> naively returns what, and why?",
         "<b>[nan, nan, nan]</b>. <code>exp(1000)</code> overflows to <code>inf</code>, then "
         "<code>inf/inf</code> is nan. The correct answer is [0.665, 0.245, 0.090]."),
        ("Softmax then log, versus log_softmax directly, on [400, 0, &minus;400]?",
         "<b>[0, &minus;400, &minus;inf]</b> versus <b>[0, &minus;400, &minus;800]</b>. The "
         "third probability underflows to exactly 0 and log(0) is &minus;inf. Same maths, "
         "different order, only one survives."),
        ("A 3-class model's first loss is 1.0986. Is that a coincidence?",
         "No &mdash; it is <b>log(3)</b>, the loss of assigning 1/3 to every class. For k "
         "classes expect log(k). A different starting loss means an initialisation bug."),
        ("What is <code>&part;L/&part;z</code> for softmax + cross-entropy?",
         "<b>p &minus; y</b> &mdash; predicted probabilities minus the one-hot truth. The "
         "softmax derivative's <b>p</b> and the log's <b>1/p</b> annihilate. Checked at "
         "<b>2.805e&minus;10</b>."),
        ("Same scores [3.0, 2.5, &minus;1.0] for car/bus/pedestrian. Softmax vs sigmoids?",
         "Softmax <b>[0.6154, 0.3733, 0.0113]</b>, sum 1. Sigmoids <b>[0.9526, 0.9241, "
         "0.2689]</b>, sum <b>2.1457</b>. A photo can hold a car AND a bus; softmax cannot "
         "say that."),
    ],
    """Cover them and answer aloud.""")),

section("10", "&#9989;", "Mastery check", "check", kind="check",
    hook="Five, none in the C2 W2 quiz.",
    body=check([
        ("""Your loss becomes <code>nan</code> after 4,000 iterations of a long run that was "
         "fine before. Name the most likely cause and the fix.""",
         """<p>A probability <b>underflowed to 0</b> and something took its log. As the model
grows more confident the logit gaps widen, so this arrives <b>partway through</b> a run rather
than at the start &mdash; which is what makes it confusing.</p>
<p>The fix is not a smaller learning rate: compute the loss from <b>logits</b> via
log_softmax, so the probability is never formed. That is <code>from_logits=True</code>.</p>"""),
        ("""A colleague says the max-subtraction &ldquo;loses a bit of precision but stops the
crash&rdquo;. Correct them.""",
         """<p>It loses <b>nothing</b>. Shift-invariance makes it exact: identical output, by a
route that cannot overflow. The file demonstrates it directly by printing
<code>softmax([2,1,0])</code> and <code>softmax([12,11,10])</code> as the same six
decimals.</p>"""),
        ("""You add 5.0 to every entry of <code>b</code>. Predict the change in accuracy, and
say what that tells you about the parameterisation.""",
         """<p><b>Zero change.</b> Softmax is shift-invariant, so a uniform shift across all
classes is a complete no-op.</p>
<p>Which means <code>b</code> carries <b>one redundant degree of freedom</b> &mdash; you could
pin b[0] = 0 and lose nothing at all. Shift <b>one</b> column and everything changes, which
proves the model lives in the differences.</p>"""),
        ("""You are detecting car, bus and pedestrian in dashcam frames. Which output head,
and what is the one question that decides it?""",
         """<p><b>Independent sigmoids</b>, because a frame can contain a car <b>and</b> a bus
<b>and</b> a pedestrian.</p>
<p>The deciding question is not about accuracy: <b>can two answers be true at once?</b> If
yes, softmax is actively wrong &mdash; it is built to make the options compete, so raising one
probability forces the others down.</p>"""),
        ("""Your gradient check fails by exactly 5 on a batch of 5. What kind of bug, and
where would you look first?""",
         """<p>A <b>scaling</b> bug &mdash; a missing <code>/ m</code>. A round-number ratio is
never a calculus error.</p>
<p>Look at the last division in <code>grad_logits</code>. Same signal as file 04's
factor-of-4, and it saves you re-deriving anything.</p>"""),
    ],
    """None of these appears in the <a href="../quiz/c22.html">C2 W2 mock quiz</a>, which
covers ReLU, the softmax formula, Adam and the backprop cost. These need this file's
output.""")),
    ],
)
