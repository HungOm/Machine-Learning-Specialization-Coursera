# -*- coding: utf-8 -*-
"""Active Mastery for 06_decision_tree.py.

Depth note (brief §6): the variable table here is genuinely THIN -- ten
animals, three binary columns, one label. There is no units story to tell
and pretending otherwise would pad it. The weight is in the break section
and in the pure-noise overfitting demonstration.
"""
from masterykit import (section, prose, code, out, semantics, ledger, drill, peek,
                        predict, lab, breaks, invariant, wrong, reconstruct,
                        connections, recall, check)

AM = dict(
    lede="Eleven cards on the one file in this lane with <b>no gradient, no learning rate and "
         "nothing random</b> &mdash; and on the 90% accuracy it reaches on pure noise.",
    sections=[

section("0", "&#129517;", "Before you run", "before", kind="orient",
    hook="Ten animals. No gradients, no alpha, no initialisation.",
    body=prose("""<p>Every other file in this lane descends a gradient. This one does not.
There is no learning rate, no initialisation, nothing random, and no cost minimised by
stepping. It is <b>greedy search</b>: take the best split available now, recurse into both
halves, stop when a rule says to.</p>
<p><b>Watch for:</b> ear shape beating face shape by a factor of eight; a continuous feature
scoring higher than any binary one; and the last block reaching <b>90% training accuracy on
data with no pattern in it whatsoever</b>.</p>""")
    + connections([], [], "../gist/c24.html", "C2 Week 4 &mdash; the gist",
        extra=[("lab", "../scratch/04-backpropagation.html", "Contrast with 04",
                "everything that file needs &mdash; alpha, init, gradients &mdash; is absent here")])),

section("1", "&#127991;&#65039;", "What every variable is", "vars", kind="semantics",
    hook="Honestly thin: three yes/no columns and one label. The interesting variable is entropy.",
    body=semantics([
        ("X", "(10, 3) int64", "the animal table",
         "<b>One row = one animal.</b> Three yes/no traits, in the order given by "
         "<code>FEATURES</code>.",
         "<b>0 / 1 &mdash; a yes/no flag</b>",
         "<code>X[3]</code> is [1, 0, 1] &mdash; animal #4 has pointy ears, <b>not</b> a round "
         "face, and whiskers.",
         "These are <b>flags, not quantities</b>. There is no sense in which 1 is twice 0, "
         "which is exactly why one-hot encoding exists for unordered categories."),
        ("FEATURES", "list of 3 str", "the column names",
         "<b>['ear shape', 'face shape', 'whiskers']</b> &mdash; the only reason the printed "
         "tree is readable.",
         "<i>names</i>",
         "<code>FEATURES[0]</code> is 'ear shape', and the root splits on it.",
         "Lose this list and the tree prints &ldquo;feature 0&rdquo;, which is correct and "
         "useless. Naming is not decoration in a model you have to explain."),
        ("y", "(10,) int64", "the labels",
         "<b>1 = cat, 0 = not a cat.</b> Five of each.",
         "<i>class label</i>",
         "<code>y</code> is [1,1,0,0,1,1,0,1,0,0] &mdash; exactly five cats, which is why "
         "root entropy is exactly 1.0.",
         "Make it 9 cats and 1 other and the root entropy drops to 0.469 &mdash; there is "
         "simply less to explain, so every gain looks smaller."),
        ("H", "float", "entropy",
         "<b>How mixed a group is</b>, in bits. The one genuinely quantitative idea in the "
         "file.",
         "<b>bits</b>",
         "H = <b>1.0</b> at 5/10 means one full yes/no question's worth of uncertainty. "
         "H(0.8) = 0.7219, and H(0.2) is the <b>same</b> &mdash; entropy is symmetric.",
         "H = 0 at both p = 0 and p = 1. It measures <b>mess</b>, not cat-ness."),
        ("gain", "float", "information gain",
         "How many bits of mess a split removes, <b>weighted</b> by how many examples go each "
         "way.",
         "<b>bits</b>",
         "Ear shape scores <b>0.2781</b>; face shape <b>0.0349</b>. Ear shape is worth about "
         "<b>eight times</b> as much.",
         "Drop the weights and splitting one example into its own pure branch scores "
         "brilliantly every time. That is the single most common bug when writing this from "
         "scratch."),
        ("tree", "dict", "the model itself",
         "A nested dict: <code>{leaf, feature, gain, n, yes, no}</code>. The whole trained "
         "model is this one object.",
         "<i>structure</i>",
         "<code>tree['feature']</code> is <b>0</b> and <code>tree['gain']</code> is "
         "<b>0.2781</b> &mdash; the root split, and how much it bought.",
         "There are <b>no weights anywhere</b>. Nothing here is a number to be nudged, which "
         "is why none of file 01's machinery appears."),
        ("weight", "(10,) float64", "a continuous feature",
         "<b>The animals' weights in kilograms</b> &mdash; the one column here with a real "
         "physical unit.",
         "<b>kg</b>",
         "<code>weight[9]</code> is <b>20.0</b> &mdash; animal #10 weighs 20&nbsp;kg, which is "
         "not a cat.",
         "The tree finds a threshold of <b>9.00 kg</b> with gain <b>0.6100</b> &mdash; more "
         "than double the best binary feature. A well-chosen number often beats a flag."),
    ],
    """This table is short because the file is honestly short on quantities: three flags, one
label, one real measurement. The variable worth understanding is <b>entropy</b>, and it is
the only one with a unit."""),
    ),

section("2", "&#128302;", "Prediction checkpoints", "predict", kind="predict",
    hook="Four, ending on an accuracy that should alarm you.",
    body=predict([
        ("""Root entropy is <b>1.0</b>. Before reading the table, predict which of the three
features wins the root split, and roughly by how much.""",
         """<p><b>Ear shape</b>, at <b>0.2781</b> &mdash; against whiskers <b>0.1245</b> and
face shape <b>0.0349</b>. About <b>eight times</b> face shape.</p>
<p>Look at why: ear shape splits 5/5 leaving both halves at H = 0.7219, while face shape
leaves 0.9852 and 0.9183 &mdash; barely tidier than where it started. A 50/50 split that
separates well beats a lopsided one that does not.</p>"""),
        ("""H(0.8) = 0.7219. <b>Predict H(0.2)</b> before computing it.""",
         """<p><b>Identical &mdash; 0.7219.</b> Entropy is symmetric.</p>
<p>It measures <b>mess</b>, not how many cats there are. A bag that is 80% cats and a bag that
is 20% cats are equally surprising to reach into. That is also why H = 0 at <i>both</i>
p = 0 and p = 1.</p>"""),
        ("""The continuous <code>weight</code> feature is tried against the three binary ones.
Predict whether it wins, and how many thresholds get tested.""",
         """<p>It <b>wins comfortably</b>: gain <b>0.6100</b> at a threshold of
<b>9.00 kg</b>, more than double ear shape's 0.2781.</p>
<p>It tests <b>9</b> candidates &mdash; the midpoints between consecutive distinct sorted
values, which is m &minus; 1 for 10 animals.</p>
<p>This is also why <b>trees need no feature scaling</b>: the algorithm only ever asks
&ldquo;above or below?&rdquo;, and a comparison is unchanged by multiplying every weight by a
thousand.</p>"""),
        ("""The last block trains on <b>pure noise</b> &mdash; 40 examples, 6 random binary
features, labels with no relationship to them. Predict the training accuracy at depth 6.""",
         """<p><b>0.900.</b> Ninety percent, on data containing no pattern at all.</p>
<p>And it climbs <b>smoothly</b>: 0.675 at depth 1, 0.700 at 2, 0.800 at 3, 0.900 at 6.
Nothing anywhere warns you. On a real dataset that curve is indistinguishable from
progress.</p>
<p>Every point of that 90% is memorisation, and it is the clearest argument in the lane for a
validation set: <b>training accuracy cannot tell these two situations apart.</b></p>"""),
    ],
    """The last one is the point of the file. Commit to a number before you look.""")),

section("3", "&#128295;", "Modify the copy", "lab", kind="lab",
    hook="Five, including the one that makes a useless feature win.",
    body=lab([
        ("L1", "Change a value",
         "Flip <code>y[2]</code> from 0 to 1 so there are six cats. Re-run and compare the "
         "root gain.",
         "y = np.array([1, 1, 1, 0, 1, 1, 0, 1, 0, 0])     # was 0 at index 2",
         """<p>Root entropy falls from <b>1.0</b> to about <b>0.971</b> &mdash; six/four is
slightly tidier than five/five &mdash; and the gains shift with it.</p>
<p>The useful observation: <b>gain is relative to where you started.</b> A smaller root
entropy means less available to remove, so every split scores lower without any split having
got worse.</p>"""),
        ("L2", "Change a parameter",
         "Cap the tree at <code>max_depth=1</code> &mdash; a single split, sometimes called a "
         "decision stump. What accuracy do you get?",
         "tree = build(X, y, depth=0, max_depth=1)",
         """<p>Around <b>0.8</b> rather than 1.00. One question &mdash; &ldquo;pointy
ears?&rdquo; &mdash; already gets most of the way.</p>
<p>Worth sitting with: the full tree's <b>1.00</b> is not four times better than the stump's
0.8. It is the same signal plus memorised detail, and the stump is far more likely to survive
new animals.</p>"""),
        ("L3", "Change the data",
         "Add an ID column &mdash; a unique number per animal &mdash; and let the tree "
         "consider it. Predict its gain.",
         "X = np.c_[X, np.arange(10)]\nFEATURES = FEATURES + ['animal id']",
         """<p>It scores a <b>perfect</b> gain of <b>1.0</b> and wins the root immediately.
Every leaf holds exactly one animal, so every leaf is perfectly pure.</p>
<p>And the rule &ldquo;if id = 4 then cat&rdquo; tells you <b>nothing</b> about a new animal,
which has an id the tree has never seen. Pure memorisation with a perfect score.</p>
<p>C4.5 fixes this with <b>gain ratio</b>, which penalises high-cardinality features. The
practical fix is simpler: never feed an identifier &mdash; order number, timestamp, email
&mdash; to a tree.</p>"""),
        ("L4", "Change an assumption",
         "Delete the weights from the gain formula &mdash; average the two child entropies "
         "instead. Then re-run L3's ID experiment.",
         "gain = H(parent) - 0.5 * (H(left) + H(right))     # unweighted",
         """<p>Now <b>every</b> split that shaves off one pure example looks excellent, because
that branch's H = 0 counts for as much as the branch holding the other nine.</p>
<p>The tree degenerates into peeling off one example at a time. This is the most common bug
when implementing a tree from scratch, and it does not crash &mdash; it just builds a
maximally overfitted tree that scores perfectly on training data.</p>
<p>The weights are what make gain an <b>expected</b> reduction rather than an average of two
unrelated numbers.</p>"""),
        ("L5", "Explain it",
         "Explain why this file has no <code>alpha</code>, no random seed for the model, and "
         "no initialisation &mdash; and what it has instead.",
         None,
         """<p>Because it does not <b>search a continuous space</b>. Gradient descent starts
somewhere and steps; a tree <b>enumerates</b> every feature and every threshold, scores each
exactly, and takes the best. There is nothing to initialise and no step size to choose.</p>
<p>What it has instead is <b>greed</b>: it takes the best split available <i>now</i>, never
reconsidering. That is why a tree is deterministic but not optimal &mdash; the globally best
tree may require a first split that looks worse.</p>"""),
    ],
    """L3 and L4 are the pair worth running together: one shows a useless feature winning, the
other shows how to build a tree that always overfits.""")),

section("4", "&#128165;", "Break it, then repair it", "break", kind="debug",
    hook="Four breaks. This is where this file's weight is.",
    body=breaks([
        ("def entropy(p):\n    return -p * np.log2(p) - (1-p) * np.log2(1-p)     # no guard",
         "Remove the guard for p = 0 and p = 1, then compute the entropy of a pure node.",
         """<p><code>log2(0)</code> is <b>&minus;inf</b>, and <code>0 * -inf</code> is
<b>nan</b> &mdash; so a <b>perfectly pure node</b>, the best possible outcome, returns nan.</p>
<p>Then every gain involving it is nan, and <code>nan &gt; best</code> is <b>False</b>, so the
tree silently refuses to make good splits and picks worse ones.</p>
<p>The invariant: <b>H(0) = H(1) = 0 by definition</b>, taken as the limit. The guard is not
defensive coding, it is the definition.</p>"""),
        ("i = np.argmax(gains)        # gains may contain a nan",
         "Combine the previous break with argmax and predict which feature gets chosen.",
         """<p><code>np.argmax</code> on an array containing <b>nan</b> returns the index of
the <b>nan</b> &mdash; nan compares False against everything, and argmax keeps whatever it saw
first that nothing beat.</p>
<p>So the tree confidently splits on the feature whose gain could not be computed. No error,
no warning, a plausible-looking tree.</p>
<p>The invariant: <b>check for nan before argmax</b>, or better, make nan impossible upstream.
This is a two-bug interaction, which is why it is worth meeting deliberately.</p>"""),
        ("for t in np.unique(values):        # in best_threshold: values, not midpoints",
         "Split on the observed values rather than the midpoints between them. Does anything "
         "break?",
         """<p>Nothing errors, and the accuracy is usually identical on <b>this</b> data.</p>
<p>But a threshold sitting exactly <i>on</i> a data point makes the split depend on whether
you wrote <code>&lt;</code> or <code>&le;</code>, and a new animal weighing exactly 9.2&nbsp;kg
&mdash; a value that <b>was</b> in the training set &mdash; can now fall either way depending
on that choice.</p>
<p>Midpoints put the boundary in the gap where no data lives, so the comparison operator
stops mattering. The invariant: <b>a decision boundary should not sit on a training
example.</b></p>"""),
        ("def build(X, y, depth, max_depth=99):\n    # stopping rules removed entirely",
         "Remove every stopping rule and grow the tree until all leaves are pure. Then run "
         "it on the <b>noise</b> dataset.",
         """<p>Training accuracy on the noise data goes to <b>1.00</b> &mdash; up from the
0.900 the depth-6 tree manages.</p>
<p>A tree with no stopping rule can always reach a perfect training score, provided no two
identical rows carry different labels. That is not a property of the data; it is a property
of the algorithm.</p>
<p>The invariant: <b>every stopping rule exists for one reason &mdash; keeping the tree
small.</b> The tree does not know it is memorising, and its training accuracy improves at
every depth.</p>"""),
    ],
    """The first two compound: one produces a nan, and the second makes argmax choose it. That
interaction is far more instructive than either alone.""")),

section("5", "&#9878;&#65039;", "The invariant", "invariant", kind="invariant",
    hook="Gain is never negative, and a pure node has zero entropy.",
    body=invariant("""<p><b>Information gain is never negative, entropy is zero at both ends
and maximal at 0.5, and the predictions must reproduce the training labels exactly.</b></p>""",
    """<p>The first is the one that catches real bugs. Splitting cannot <i>increase</i>
expected mess, so a negative gain means your weights are wrong or your entropy is &mdash;
almost always the missing <code>w_left</code> and <code>w_right</code>.</p>
<p>The second pins the entropy function: <b>H(0) = H(1) = 0</b> and <b>H(0.5) = 1</b>,
symmetric about the middle. Get the guard wrong and H(0) is nan rather than 0.</p>
<p>The third is weaker than it looks. The file reports <b>10/10</b>, and that is expected of a
tree grown until its leaves are pure &mdash; it is a check that the <i>prediction path</i>
works, not evidence that the model is any good. The noise experiment exists to make exactly
that point.</p>""",
    """for p in (0.0, 0.5, 1.0, 0.8):
    h = entropy(p)
    assert np.isfinite(h) and 0.0 <= h <= 1.0
assert entropy(0.0) == 0.0 and entropy(1.0) == 0.0
assert abs(entropy(0.8) - entropy(0.2)) < 1e-12
assert all(g >= -1e-12 for g in gains)""")),

section("6", "&#129535;", "Wrong mental models", "wrong", kind="myths",
    hook="Five, and the first one is the reason people ship broken trees.",
    body=wrong([
        ("The feature with the highest information gain is the most useful feature.",
         """<p>An <b>ID column</b> scores a perfect 1.0 and is worth nothing. Every leaf holds
one animal, every leaf is pure, maximum gain &mdash; and &ldquo;if id = 4 then cat&rdquo;
generalises to nothing.</p>
<p>Gain rewards <b>purity on the training set</b>, and high-cardinality features achieve that
by memorising. This is why C4.5 introduced gain ratio, and why you never feed an identifier to
a tree.</p>"""),
        ("100% training accuracy means the model works.",
         """<p>The file reaches <b>0.900 on pure noise</b> &mdash; 40 examples, 6 random
features, labels generated independently of them.</p>
<p>A tree grown until its leaves are pure can nearly always reach a perfect training score.
That is a property of the algorithm, not of the data, and it is why the training score is
uninformative here.</p>"""),
        ("Entropy measures how many cats there are.",
         """<p>It measures <b>mess</b>. H = 0 at <b>both</b> p = 0 and p = 1: all cats and no
cats are equally tidy.</p>
<p>And it is symmetric &mdash; H(0.8) = H(0.2) = 0.7219. If you expected 80% cats to be
&ldquo;better&rdquo; than 20%, you were reading it as a score rather than as
uncertainty.</p>"""),
        ("A deeper tree is a better tree.",
         """<p>On the noise data, depth 1 gives 0.675 and depth 6 gives 0.900 &mdash; every
extra level buys training accuracy and <b>zero</b> real signal.</p>
<p>Depth is the main thing you regularise in a tree, and the stopping rules exist precisely to
prevent depth from being free.</p>"""),
        ("Trees need feature scaling like everything else.",
         """<p>They need <b>none</b>. The algorithm only ever asks &ldquo;is this value above
or below that one?&rdquo;, and a comparison is unchanged by multiplying every weight by a
thousand.</p>
<p>Gradient descent cares about scale because it takes <b>steps</b>, and a step sized for one
axis is wrong for another. A tree never takes a step. That is the cleanest illustration in the
lane of why scaling is about the <i>optimiser</i>, not about tidiness.</p>"""),
    ])),

section("7", "&#127959;&#65039;", "Reconstruction challenge", "reconstruct", kind="rebuild",
    hook="Rebuild it, then prove it by making it fail on noise.",
    body=reconstruct([
        ("Explain", "In three sentences, describe the algorithm without the words "
         "<i>entropy</i> or <i>gain</i>.",
         """<p>Look at every question you could ask about the data and, for each, see how
cleanly it splits the group into two more uniform halves. Ask the question that separates
best, then repeat the whole procedure on each half. Stop when a group is already uniform, or
too small, or you have asked too many questions.</p>"""),
        ("Skeleton", "Write the signatures for entropy, information gain, the continuous threshold "
         "search, and the recursive build.",
         """<p><code>entropy(y)</code> &mdash; note it takes the <b>labels</b>, not a probability
&mdash; <code>information_gain(X, y, feature)</code>, <code>best_threshold(values, y)</code>
for the continuous case, and <code>build(X, y, depth=0, max_depth=3, min_samples=1,
used=())</code> returning the nested dict.</p>
<p><code>build</code> is the only recursive one, and it must return a <b>leaf</b> dict when a
stopping rule fires &mdash; that base case is where most rebuilds go wrong.</p>"""),
        ("Core", "Write entropy and weighted gain from memory, guards included.",
         """<p><code>entropy(y)</code> computes p from the labels first &mdash; <code>p = y.mean()</code>
&mdash; then returns <b>0.0</b> when p is 0 or 1, else
<code>-p*log2(p) - (1-p)*log2(1-p)</code>.</p>
<p><code>information_gain</code>: <code>H(parent) - (n_l/n)*H(left) - (n_r/n)*H(right)</code>. If you
wrote <code>0.5*(H_l + H_r)</code> you have built the L4 bug, and your tree will peel off one
example at a time.</p>"""),
        ("Minimal", "Build the smallest dataset where a <b>stump</b> beats a full tree on "
         "held-out data.",
         """<p>Any dataset with one strong feature and several noise features, split into
train and test. The stump finds the real signal; the full tree splits further on noise and
does worse on the test half.</p>
<p>This is bias/variance made concrete, and you can build it in about six lines with
<code>rng.integers</code>.</p>"""),
        ("Verify", "Check your rebuild without comparing to the original.",
         """<p>Four assertions: <code>entropy(0) == entropy(1) == 0</code>;
<code>entropy(0.5) == 1</code>; <code>entropy(0.8) == entropy(0.2)</code>; and every gain
&ge; 0.</p>
<p>Then the real test: run it on <b>pure noise</b> and confirm training accuracy climbs with
depth. If it does not, your stopping rules are firing when they should not.</p>"""),
    ],
    """The verify stage is unusual here: you prove the rebuild is right partly by confirming
it <b>overfits</b>, because that is a genuine property of the algorithm.""")),

section("8", "&#128279;", "Connections", "conn", kind="links",
    hook="The odd one out: no gradients anywhere.",
    body=connections(
        [("lab", "../scratch/04-backpropagation.html", "Contrast with 04",
          "alpha, initialisation and gradients &mdash; all absent here"),
         ("lab", "../scratch/01-linear-regression.html", "Contrast with 01",
          "scaling matters there and is irrelevant here, for a reason worth knowing")],
        [("lab", "../scratch/07-kmeans.html", "On to 07",
          "another algorithm with no gradient, and one that is <b>not</b> deterministic")],
        "../gist/c24.html", "C2 Week 4 &mdash; the gist",
        extra=[("docs", "../reference.html", "Reference &mdash; C2 W4",
                "<code>c2w4-infogain</code> and <code>c2w4-id-column</code> cover the two "
                "traps this file demonstrates")])),

section("9", "&#9670;", "Recall sheet", "recall", kind="recall",
    hook="Six cards, mostly about what gain rewards.",
    body=recall([
        ("Root entropy here is exactly <b>1.0</b>. Why exactly?",
         "Five cats out of ten &mdash; p = 0.5 &mdash; which is maximum mess: exactly "
         "<b>one bit</b> of uncertainty. Base 2 is what makes it come out at 1."),
        ("Ear shape scores 0.2781 and face shape 0.0349. What makes the difference?",
         "Ear shape splits 5/5 and leaves both halves at H = 0.7219. Face shape leaves 0.9852 "
         "and 0.9183 &mdash; barely tidier than the root. It is about <b>how much mess is "
         "removed</b>, not how evenly it splits."),
        ("What do the weights in the gain formula prevent?",
         "Splitting off a <b>single</b> example into its own perfectly pure branch scoring "
         "brilliantly every time. Without them the tree peels off one example per split, "
         "forever. It is the most common from-scratch bug."),
        ("Remove the p = 0 guard from <code>entropy</code>. What does a <b>pure</b> node return, "
         "and what does <code>argmax</code> do next?",
         "<code>0 * log2(0)</code> is <b>nan</b>, so the <i>best possible</i> node scores nan. "
         "And <code>np.argmax</code> returns the <b>nan&rsquo;s index</b> &mdash; nan compares "
         "False against everything &mdash; so the tree splits on the feature it could not score."),
        ("The continuous <code>weight</code> feature: how many thresholds are tried, and what "
         "wins?",
         "<b>m &minus; 1 = 9</b> midpoints between consecutive distinct sorted values. Best is "
         "<b>9.00 kg</b> with gain <b>0.6100</b> &mdash; more than double ear shape."),
        ("Training accuracy on <b>pure noise</b>, at depth 1 and depth 6?",
         "<b>0.675</b> and <b>0.900</b>. Forty examples, six random features, labels unrelated "
         "to them. It climbs smoothly and nothing warns you."),
    ],
    """Cover and answer aloud.""")),

section("10", "&#9989;", "Mastery check", "check", kind="check",
    hook="Five, none in the C2 W4 quiz.",
    body=check([
        ("""A colleague reports a feature with information gain <b>0.98</b> and wants to ship
it. What do you ask first?""",
         """<p><b>How many distinct values does it take?</b> A gain that high on a real problem
usually means a near-identifier &mdash; order number, timestamp, customer id, email.</p>
<p>The test: does the rule it produces say anything about a <b>row you have never seen</b>? If
every leaf holds one example, the answer is no.</p>"""),
        ("""Your tree returns nan for some gains and picks an odd root. Name both bugs.""",
         """<p>First: the entropy function is missing its guard, so a <b>pure node</b> gives
<code>0 * log2(0)</code> = nan. Second: <code>np.argmax</code> on an array containing nan
returns the <b>nan's index</b>, because nan compares False against everything.</p>
<p>So a nan does not just corrupt one number &mdash; it wins the selection. Fix the guard and
the argmax is fine.</p>"""),
        ("""Explain, in one sentence, why this file needs no feature scaling when files 01, 02
and 05 all do.""",
         """<p>Because a tree only ever <b>compares</b> values &mdash; above or below a
threshold &mdash; and a comparison is unchanged by rescaling, whereas gradient descent takes
<b>steps</b> and a step sized for one feature is wrong for another.</p>"""),
        ("""Your tree scores 1.00 on training data. What do you now know about its
performance on new data?""",
         """<p><b>Nothing at all.</b> The file demonstrates 0.900 on data with no pattern in it,
and a tree with no stopping rule can nearly always reach 1.00.</p>
<p>You need a held-out set. Training accuracy for an unconstrained tree measures the algorithm,
not the data.</p>"""),
        ("""You are asked to make a tree that always overfits, without touching max_depth.
What one change achieves it?""",
         """<p>Remove the <b>weights</b> from the gain formula. Then splitting off a single
pure example scores maximally every time, and the tree peels examples off one at a time until
every leaf holds one.</p>
<p>Worth knowing as a bug signature: a tree that is far too deep with tiny leaves usually
means the weighting is wrong, not that max_depth is too high.</p>"""),
    ],
    """None of these appears in the <a href="../quiz/c24.html">C2 W4 mock quiz</a>, which
covers entropy, information gain, one-hot encoding and ensembles.""")),
    ],
)
