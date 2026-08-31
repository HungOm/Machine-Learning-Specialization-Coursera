# -*- coding: utf-8 -*-
"""Active Mastery for 07_kmeans.py.

Depth note (brief §6): the interesting content here is that J is NOT what
gets optimised globally -- two runs on identical data reach 1.7778 and
1.3125 -- so the predictions target NON-DETERMINISM across seeds, and the
invariant is monotonicity rather than optimality.
"""
from masterykit import (section, prose, code, out, semantics, ledger, drill, peek,
                        predict, lab, breaks, invariant, wrong, reconstruct,
                        connections, recall, check)

AM = dict(
    lede="Eleven cards on the first file with <b>no y at all</b> &mdash; and on the fact that "
         "running it twice on the same six points gives two different answers.",
    sections=[

section("0", "&#129517;", "Before you run", "before", kind="orient",
    hook="Six points, no labels, and no single right answer.",
    body=prose("""<p>The first <b>unsupervised</b> file in the lane. There is no <b>y</b>.
Nobody knows the right answer and there is no right answer to know &mdash; only groupings that
are more or less useful.</p>
<p>That changes what &ldquo;working&rdquo; means: there is no accuracy to report, so the
algorithm has to <b>bring its own measure of quality</b>, and choosing <b>K</b> becomes a
question the data cannot answer.</p>
<p><b>Watch for:</b> the same six points giving <b>J = 1.7778</b> from one start and
<b>1.3125</b> from another; and the elbow test working perfectly on data built to have an
elbow.</p>""")
    + connections([], [], "../gist/c31.html", "C3 Week 1 &mdash; the gist",
        extra=[("lab", "../scratch/06-decision-tree.html", "Contrast with 06",
                "also gradient-free &mdash; but <b>deterministic</b>, which this is not")])),

section("1", "&#127991;&#65039;", "What every variable is", "vars", kind="semantics",
    hook="Six 2-D points with no units, and a cost whose units are squared distance.",
    body=semantics([
        ("X", "(6, 2) float64", "the points to cluster",
         "<b>One row = one point in a plane.</b> Abstract coordinates &mdash; the file gives "
         "them no real-world meaning, and inventing one would add nothing.",
         "<i>arbitrary length units</i>",
         "<code>X[3]</code> is [5.0, 7.0] &mdash; the point furthest up and to the right.",
         "Both columns are on the same scale here (1&ndash;7), which is why no scaling step "
         "appears. Make one column span 0&ndash;1000 and distance would be dominated by it "
         "entirely."),
        ("idx", "(6,) int64", "the assignment",
         "<b>Which cluster each point currently belongs to.</b> One entry per point.",
         "<i>cluster label &mdash; arbitrary</i>",
         "<code>idx</code> is [1,1,0,0,0,0]: points 1 and 2 in cluster 1, the rest in "
         "cluster 0.",
         "<b>The numbers are names, not values.</b> [1,1,0,0,0,0] and [0,0,1,1,1,1] are the "
         "<i>same grouping</i>. Comparing two runs by label equality is a classic mistake."),
        ("c", "(2, 2) float64", "the centroids",
         "<b>One row per cluster</b>, each a point in the same space as the data &mdash; the "
         "mean of its members.",
         "<b>same units as X</b>",
         "<code>c[1]</code> is [1.25, 1.5] &mdash; the middle of the bottom-left pair.",
         "A centroid is <b>not</b> a data point. It usually sits where no observation is, "
         "which is fine for a mean and worth remembering when you try to interpret one."),
        ("J", "float", "the distortion",
         "The <b>average squared distance</b> from each point to its own centroid. The "
         "algorithm's own measure of quality, since there is no accuracy to report.",
         "<b>(length units)&sup2;</b>",
         "<b>1.3125</b> for the better of the two runs. The unit is squared, which is why "
         "nobody quotes it in isolation &mdash; only compares it.",
         "It can <b>never increase</b> across a step. If yours does, you have a bug, not a "
         "tuning problem."),
        ("init", "list of 2", "the starting centroids",
         "<b>Which two data points the run began from.</b> The single thing that differs "
         "between the two runs.",
         "<i>indices</i>",
         "Starting at points 1 and 4 gives J = <b>1.7778</b>; starting at 1 and 3 gives "
         "<b>1.3125</b>. Same data, same code, <b>26% worse</b>.",
         "This is the whole reason for restarts. K-means is <b>not</b> deterministic, unlike "
         "the decision tree in file 06."),
        ("blobs", "(120, 2) float64", "the elbow-test data",
         "120 points drawn from <b>three</b> genuine clusters &mdash; so here the right answer "
         "<i>is</i> known, which is what makes the elbow test checkable.",
         "<i>arbitrary</i>",
         "Spanning roughly &minus;1.2 to 11.1 in x. Three well-separated blobs, chosen so the "
         "elbow is unambiguous.",
         "On real data the curve usually bends smoothly with no corner, which is why Andrew "
         "says he rarely uses the method."),
    ],
    """The row that carries this file is <b>J</b>. It is the only quality measure available
&mdash; there is no y to be right or wrong about &mdash; and it is simultaneously the thing
that <b>cannot</b> be used to choose K.""")
    + drill("""<p>Without scrolling: run A produced <code>idx = [0,0,0,1,1,1]</code> and run B
produced <code>[0,0,1,1,1,1]</code>. Say out loud <b>which point moved</b>, and what that
means about it.</p>""",
    """<p><b>Point 3</b>, at <code>[3.0, 4.0]</code>.</p>
<p>Run A put it with the bottom-left pair; run B put it with the top-right group. It is the
<b>ambiguous</b> point &mdash; genuinely between the two clumps &mdash; and the numbers say run
B fits better: <b>J = 1.3125</b> against <b>1.7778</b>.</p>
<p>If you said &ldquo;the labels changed&rdquo; you read the cluster numbers as values. They
are names: <code>[1,1,0,0,0,0]</code> is the same grouping as
<code>[0,0,1,1,1,1]</code>.</p>""")),

section("2", "&#128302;", "Prediction checkpoints", "predict", kind="predict",
    hook="Four, and the first is about the same code giving two answers.",
    body=predict([
        ("""The same six points, the same algorithm, two different starting centroids.
<b>Predict whether both runs converge</b>, and whether they reach the same answer.""",
         """<p><b>Both converge. They reach different answers.</b></p>
<p>Run A settles at <b>J = 1.7778</b> with clusters [0,0,0,1,1,1]; run B at <b>J = 1.3125</b>
with [0,0,1,1,1,1]. Neither is broken &mdash; both are <b>local optima</b>, points where no
single reassignment improves anything.</p>
<p>Course 1's convex bowl guaranteed this could not happen. K-means has no such guarantee, and
run A is <b>26% worse</b> for no reason other than where it started.</p>"""),
        ("""J falls at every step by construction. <b>Predict what J does as you increase
K</b> from 1 to 6 on six points.""",
         """<p>It falls all the way to <b>exactly 0</b> at K = 6, where every point is its own
cluster.</p>
<p>Which is why <b>you cannot choose K by minimising J</b>: the answer is always &ldquo;use as
many clusters as you have points&rdquo;. Perfect score, zero information.</p>"""),
        ("""120 points from three real blobs. Predict the shape of J against K = 1, 2, 3, 4
&mdash; specifically the size of each <b>drop</b>.""",
         """<p>J goes <b>23.648 &rarr; 9.094 &rarr; 0.722 &rarr; 0.616</b>.</p>
<p>Read the <b>drops</b>, not the values: going to K = 2 bought <b>14.554</b>, to K = 3 bought
<b>8.372</b>, and to K = 4 bought <b>0.106</b> &mdash; about <b>eighty times less</b>.</p>
<p>That collapse is the elbow, and it points squarely at K = 3, which is the truth. It works
here because the blobs are cleanly separated; on real data the curve usually has no
corner.</p>"""),
        ("""50 random restarts are run and the best kept. Predict which J it lands on, and
which cluster labels it prints.""",
         """<p><b>J = 1.3125</b> &mdash; run B's answer, the better one.</p>
<p>But it prints <code>[1,1,0,0,0,0]</code> rather than <code>[0,0,1,1,1,1]</code>. <b>Same
grouping, labels swapped.</b> Cluster numbers are arbitrary names assigned by whichever
centroid happened to be first.</p>
<p>Anyone comparing two clusterings with <code>==</code> on the label arrays will conclude
they disagree when they are identical.</p>"""),
    ],
    """The first one is the point of the file: same input, same code, two answers, both
correct terminations.""")),

section("3", "&#128295;", "Modify the copy", "lab", kind="lab",
    hook="Five, including one that shows why the mean is not an arbitrary choice.",
    body=lab([
        ("L1", "Change a value",
         "Start from points <b>0 and 1</b> &mdash; the two closest points in the set &mdash; "
         "and see where it converges.",
         "init = [0, 1]        # both from the bottom-left corner",
         """<p>It still converges, and usually to the <b>good</b> answer &mdash; the two
centroids separate on the first move because one of them immediately captures the whole
top-right group.</p>
<p>Worth noticing: a &ldquo;bad&rdquo; initialisation is not simply two close points. It is an
initialisation whose <b>first assignment</b> splits the data the wrong way, and that is harder
to predict by eye than it sounds.</p>"""),
        ("L2", "Change a parameter",
         "Set K = 3 on the six points and read the resulting J.",
         "K = 3        # was 2",
         """<p>J drops well below 1.3125 &mdash; more clusters always fit better.</p>
<p>And that is the trap in one line: <b>J alone would tell you K = 6 is best.</b> The number
improves monotonically while the clustering becomes less and less useful, which is why the
choice of K has to come from outside the data.</p>"""),
        ("L3", "Change the data",
         "Multiply the second column by 100 &mdash; as if it were measured in centimetres "
         "rather than metres &mdash; and re-run.",
         "X = X * np.array([1.0, 100.0])",
         """<p>The clustering changes completely: the second column now dominates the distance
entirely, so the algorithm effectively clusters on <b>that column alone</b>.</p>
<p>Squared distance adds the columns' contributions, so a column with a hundredfold larger
range contributes ten thousand times as much. K-means is <b>not</b> scale-invariant, unlike the
decision tree in file 06.</p>
<p>The file gets away without scaling only because both columns already span 1&ndash;7.</p>"""),
        ("L4", "Change an assumption",
         "Move each centroid to the <b>median</b> of its members instead of the mean, and "
         "watch J.",
         "c[k] = np.median(X[idx == k], axis=0)      # was .mean(axis=0)",
         """<p>J is <b>no longer guaranteed to fall</b>, and on some runs it rises &mdash;
which under the file's own invariant would look like a bug.</p>
<p>It is not a bug: the <b>mean is the exact minimiser of squared distance</b>. Swap in the
median and you are minimising something else (absolute distance), so the cost you are still
<i>measuring</i> can go up.</p>
<p>That is why the pairing is not arbitrary: squared distance &rarr; mean; absolute distance
&rarr; median, which is a different algorithm called k-medians.</p>"""),
        ("L5", "Explain it",
         "Explain why the assign step uses <code>argmin</code> of <b>squared</b> distance and "
         "never takes a square root.",
         None,
         """<p>Because the square root is <b>monotonic</b>: whichever centroid is nearest by
squared distance is nearest by actual distance too. Taking the root would change every number
and no decision, so it is pure cost.</p>
<p>The second reason is deeper: keeping the square is what makes the <b>mean</b> the right
centroid in the next step. The two halves of the algorithm agree only because both use the
same distance.</p>"""),
    ],
    """L4 is the one worth running. It shows that &ldquo;use the mean&rdquo; is a
<b>consequence</b> of the cost, not a convention.""")),

section("4", "&#128165;", "Break it, then repair it", "break", kind="debug",
    hook="Four, one of which crashes on a genuinely reachable input.",
    body=breaks([
        ("for k in range(K):\n    c[k] = X[idx == k].mean(axis=0)        # no empty check",
         "Initialise both centroids at the <b>same</b> point and run one iteration.",
         """<p>One cluster gets <b>every</b> point and the other gets none, so
<code>X[idx == k]</code> is empty. <code>np.mean</code> of an empty slice emits
<code>RuntimeWarning: Mean of empty slice</code> and returns <b>nan</b>, and from then on every
distance to that centroid is nan.</p>
<p>Because nan comparisons are always False, <code>argmin</code> never chooses it &mdash; so
the cluster stays empty forever and you silently have K&minus;1 clusters.</p>
<p>The invariant: <b>every centroid must own at least one point.</b> The standard fix is to
re-seed an empty centroid onto the point furthest from its own centroid, and it is also why
initialising at <b>real data points</b> matters &mdash; a random coordinate can land in empty
space and collect nothing.</p>"""),
        ("d = ((X[:, None, :] - c[None, :, :]) ** 2).sum(axis=1)      # wrong axis",
         "Sum the squared differences over the wrong axis in the distance computation. "
         "Predict whether it errors.",
         """<p>The array is <b>(6, 2, 2)</b> &mdash; points &times; centroids &times;
features &mdash; and summing <code>axis=1</code> collapses the <b>centroids</b> instead of the
<b>features</b>. The result is still (6, 2), so <code>argmin</code> runs happily and returns
nonsense.</p>
<p>Every point gets assigned by a quantity that mixes both centroids together. No error, a
plausible clustering, and a J that still decreases &mdash; because the invariant only checks
that <i>something</i> is being minimised.</p>
<p>The defence is the shape ledger: you want to sum over <b>features</b>, which is the
<b>last</b> axis. <code>axis=-1</code> says what you mean and survives a change in
dimensionality.</p>"""),
        ("if np.array_equal(idx, old_idx): break        # replaced with:\nif abs(J - oldJ) < 1e-9: break",
         "Stop on the cost converging rather than on the assignments not moving. Does it "
         "still terminate?",
         """<p>Usually, but not reliably. Assignments are <b>discrete</b>, so
&ldquo;nothing changed&rdquo; is <b>exact</b> and guarantees a fixed point. A float tolerance
can trigger a step early on a plateau, or fail to trigger while two points swap back and forth
with a J difference below the threshold.</p>
<p>The invariant: <b>converge on the discrete thing when there is one.</b> A tolerance is what
you use when there is no exact test available, not by default.</p>"""),
        ("J = ((X - c[idx]) ** 2).sum()        # sum, not mean",
         "Report the total squared distance rather than the average. Predict what changes.",
         """<p>The reported numbers all scale by m &mdash; 1.3125 becomes 7.875 on six points
&mdash; and <b>all the conclusions are identical</b>, because every comparison in this file is
between runs on the <b>same</b> dataset.</p>
<p>It breaks the moment you compare across datasets of different sizes: a total grows with m
whether or not the clustering is worse. The invariant: <b>divide by m when the number will
ever be compared across datasets</b>, which is the same argument as the 1/m in file 01's
cost.</p>"""),
    ],
    """The first break is the one that happens by accident in real code, and the second is the
one you will never notice.""")),

section("5", "&#9878;&#65039;", "The invariant", "invariant", kind="invariant",
    hook="J can never rise — and that is the whole convergence proof.",
    body=invariant("""<p><b>J never increases, at either step. That is not a diagnostic
convenience &mdash; it is the entire proof that the algorithm terminates.</b></p>""",
    """<p>Step 1 gives every point its <b>nearest</b> centroid, which cannot be worse than
where it was. Step 2 moves each centroid to the mean of its members, and the mean is the
<b>exact minimiser</b> of squared distance to a set of points. So neither step can raise J.</p>
<p>Since J only falls and cannot fall forever, the algorithm <b>must</b> stop. Two sentences,
and unusually clean for a machine-learning algorithm.</p>
<p>Note carefully what it does <b>not</b> prove: that you reach the <b>best</b> answer. The two
runs here both satisfy the invariant perfectly and land on 1.7778 and 1.3125. Monotone descent
guarantees termination, never optimality &mdash; and conflating the two is the central
misconception about this algorithm.</p>""",
    """prev = np.inf
for _ in range(50):
    idx = assign(X, c)
    J1 = cost(X, c, idx);  assert J1 <= prev + 1e-12, "assign raised J"
    c = move(X, idx, K)
    J2 = cost(X, c, idx);  assert J2 <= J1 + 1e-12, "move raised J"
    prev = J2
assert all((idx == k).sum() > 0 for k in range(K)), "empty cluster\"""")),

section("6", "&#129535;", "Wrong mental models", "wrong", kind="myths",
    hook="Five, and the first is the one this file was built to break.",
    body=wrong([
        ("K-means minimises J, so it finds the best clustering.",
         """<p>It finds a <b>local</b> minimum. The file's two runs both converge and land on
<b>1.7778</b> and <b>1.3125</b> &mdash; the first is 26% worse and equally &ldquo;done&rdquo;.</p>
<p>The invariant guarantees J never rises, which proves <b>termination</b>, not optimality.
That is why you run it 50&ndash;1000 times and keep the lowest J &mdash; and the tiebreaker is
free, because J is already computed and lower is unambiguously better.</p>"""),
        ("The cluster numbers mean something.",
         """<p>They are arbitrary names. <code>[1,1,0,0,0,0]</code> and
<code>[0,0,1,1,1,1]</code> are the <b>same grouping</b> &mdash; the file prints both across
different runs.</p>
<p>Compare two clusterings with <code>==</code> on the label arrays and you will conclude they
disagree when they are identical. Comparing clusterings properly needs a metric that ignores
labelling.</p>"""),
        ("You choose K by minimising J.",
         """<p>J falls forever. At <b>K = m</b> every point is its own cluster and J is
<b>exactly 0</b>, so &ldquo;minimise J&rdquo; always answers &ldquo;use as many clusters as you
have points&rdquo;.</p>
<p>The elbow method looks for the bend instead &mdash; and it works beautifully on this file's
three clean blobs (a drop of 8.372 to K = 3, then 0.106 to K = 4) and is often ambiguous on
real data. The reliable alternative is judging K by <b>what the clusters are for</b>.</p>"""),
        ("A centroid is one of the data points.",
         """<p>It is the <b>mean</b> of its members, which usually sits where no observation
is. <code>c[1]</code> here is [1.25, 1.5], and no point in <code>X</code> is there.</p>
<p>Only the <b>initialisation</b> uses real data points &mdash; and that is deliberate, so no
centroid starts in empty space with nothing to collect.</p>"""),
        ("Like the decision tree, it needs no feature scaling.",
         """<p>The opposite. A tree only <b>compares</b> values, so rescaling changes nothing.
K-means computes <b>squared distances</b>, which <b>add</b> the columns' contributions &mdash;
so a column with a hundredfold larger range contributes ten thousand times as much and
dominates the clustering entirely.</p>
<p>This file happens not to scale because both its columns already span 1&ndash;7. That is a
property of the data, not a licence.</p>"""),
    ])),

section("7", "&#127959;&#65039;", "Reconstruction challenge", "reconstruct", kind="rebuild",
    hook="Rebuild it, then prove it is non-deterministic.",
    body=reconstruct([
        ("Explain", "In three sentences, describe the algorithm and say what each step holds "
         "fixed.",
         """<p>Give every point to its nearest centre, with the centres held fixed. Then move
every centre to the middle of the points it just received, with the assignments held fixed.
Repeat until nothing moves.</p>
<p>Each step freezing what the other changes is exactly why the cost cannot rise.</p>"""),
        ("Skeleton", "Write the signatures for assign, move, cost and fit.",
         """<p><code>assign(X, c)</code> &rarr; idx; <code>move(X, idx, K)</code> &rarr; c;
<code>cost(X, c, idx)</code> &rarr; float; <code>fit(X, K, init)</code> &rarr; (idx, c, J).</p>
<p><code>fit</code> must take <code>init</code> as an argument rather than choosing it
internally &mdash; otherwise you cannot reproduce the two-run comparison that is the point of
the file.</p>"""),
        ("Core", "Write assign and move from memory, vectorised, with no Python loop over "
         "points.",
         """<p><code>d = ((X[:, None, :] - c[None, :, :]) ** 2).sum(axis=-1)</code> then
<code>idx = d.argmin(axis=1)</code>.</p>
<p>Two details: <code>axis=-1</code> sums over <b>features</b>, and getting that axis wrong
gives a legal shape and a wrong answer. And <b>no square root</b> &mdash; it is monotonic, so
it changes no decision and costs time.</p>"""),
        ("Minimal", "Build the smallest dataset where two initialisations give different "
         "final costs.",
         """<p>Four points in two obvious pairs, plus <b>one ambiguous point</b> midway between
them, with K = 2. Start once with the ambiguous point as a centroid and once without.</p>
<p>That is exactly the structure of this file's six points, with the ambiguity concentrated in
<code>X[2] = [3.0, 4.0]</code>.</p>"""),
        ("Verify", "Check your rebuild without comparing to the original.",
         """<p>Assert J never rises across either step, assert no cluster is ever empty, and
assert that <b>at least two different final J values</b> appear across 50 random
initialisations.</p>
<p>That last one is the unusual check: you are proving your implementation is
<b>non-deterministic</b>, because a k-means that always returns the same answer on this data
has a bug &mdash; most likely a fixed initialisation.</p>"""),
    ],
    """The verify stage is the interesting one: correctness here includes reproducing the
variability, not eliminating it.""")),

section("8", "&#128279;", "Connections", "conn", kind="links",
    hook="Gradient-free like 06, but non-deterministic — and the first file with no y.",
    body=connections(
        [("lab", "../scratch/06-decision-tree.html", "Contrast with 06",
          "also gradient-free, but <b>deterministic</b> and scale-invariant"),
         ("lab", "../scratch/01-linear-regression.html", "Contrast with 01",
          "there the cost had one minimum; here it has several")],
        [("lab", "../scratch/08-pca.html", "On to 08",
          "the other unsupervised file &mdash; and one with an exact answer"),
         ("lab", "../scratch/11-retrieval.html", "On to 11",
          "distance in a learned space, used for search rather than grouping")],
        "../gist/c31.html", "C3 Week 1 &mdash; the gist",
        extra=[("docs", "../reference.html", "Reference &mdash; C3 W1",
                "<code>c3w1-distortion</code> and <code>c3w1-init</code> carry the "
                "monotonicity argument and the restart fix")])),

section("9", "&#9670;", "Recall sheet", "recall", kind="recall",
    hook="Six cards, weighted to the non-determinism.",
    body=recall([
        ("Same six points, two initialisations. What are the two costs, and is either wrong?",
         "<b>J = 1.7778</b> and <b>J = 1.3125</b>. <b>Neither is wrong</b> &mdash; both "
         "converged. The first is a <b>local optimum</b>, 26% worse, and that is why you run "
         "50&ndash;1000 restarts and keep the lowest J."),
        ("Why can J never increase?",
         "Assign gives every point its <b>nearest</b> centroid (cannot be worse); move puts "
         "each centroid at the <b>mean</b>, which is the exact minimiser of squared distance. "
         "Since it only falls and cannot fall forever, it must stop."),
        ("Why the <b>mean</b> specifically, in the move step?",
         "Because the mean is the exact minimiser of <b>squared</b> distance. Use absolute "
         "distance and the optimal centre is the <b>median</b> &mdash; a different algorithm. "
         "The distance choice picks the centre."),
        ("Why is <code>[1,1,0,0,0,0]</code> the same answer as <code>[0,0,1,1,1,1]</code>?",
         "Cluster numbers are <b>arbitrary names</b> assigned by whichever centroid came "
         "first. Comparing clusterings with <code>==</code> on labels reports disagreement "
         "between identical groupings."),
        ("A cluster ends up empty. Trace what happens on the next three lines.",
         "<code>np.mean</code> of an empty slice returns <b>nan</b>, so every distance to that "
         "centroid is nan; nan comparisons are False so <code>argmin</code> never picks it; so "
         "it stays empty <b>forever</b> and you silently have K&minus;1 clusters."),
        ("Does k-means need feature scaling?",
         "<b>Yes</b> &mdash; unlike a decision tree. It sums squared differences, so a column "
         "with a 100&times; larger range contributes 10,000&times; as much. This file skips it "
         "only because both columns span 1&ndash;7."),
    ],
    """Cover and answer aloud.""")),

section("10", "&#9989;", "Mastery check", "check", kind="check",
    hook="Five, none in the C3 W1 quiz.",
    body=check([
        ("""Your k-means gives the same answer on every run. Is that good news?""",
         """<p><b>No &mdash; it is a symptom.</b> K-means is non-deterministic by nature, and
this file's own six points produce two different costs from two starts.</p>
<p>Identical results every time usually means the initialisation is fixed &mdash; a hardcoded
seed or a deterministic choice such as &ldquo;the first K points&rdquo;. You are then getting
one local optimum reproducibly, and the restart machinery is doing nothing.</p>"""),
        ("""Your implementation reports J rising between iterations. Name the two most likely
causes.""",
         """<p>Either you are <b>moving centroids before finishing all the assignments</b>
&mdash; mixing the two steps, so neither is holding the other fixed &mdash; or you have swapped
the mean for something else, such as a median, which does not minimise squared
distance.</p>
<p>It is not a tuning problem. Monotone descent is guaranteed by the algorithm, so a rise is
always a bug.</p>"""),
        ("""One of your clusters ends up empty. Explain what happens next, and the standard
fix.""",
         """<p><code>np.mean</code> of an empty slice returns <b>nan</b>, so every distance to
that centroid is nan; nan comparisons are False, so <code>argmin</code> never selects it and
the cluster stays empty <b>forever</b>. You silently have K&minus;1 clusters.</p>
<p>The fix: <b>re-seed the empty centroid</b> onto the point furthest from its own centroid.
And initialise at <b>real data points</b>, so no centroid starts in empty space.</p>"""),
        ("""Someone rescales one feature from metres to centimetres and the clustering changes
completely. Bug or expected?""",
         """<p><b>Expected.</b> Squared distance <b>adds</b> the columns' contributions, so a
100&times; larger range contributes 10,000&times; as much and that column dominates
entirely.</p>
<p>K-means is not scale-invariant. A decision tree is, because it only ever compares. If both
features matter equally, scale them before clustering.</p>"""),
        ("""You cluster customers and your manager asks &ldquo;is K = 4 right?&rdquo;. Answer
honestly, using the file.""",
         """<p>The data cannot answer it. J falls monotonically with K, so it always prefers
more clusters; the elbow works on this file's <b>deliberately separated</b> blobs and is
usually ambiguous on real data.</p>
<p>The honest answer is to judge K by <b>what the clusters are for</b> &mdash; do four
segments produce better campaigns than three? That is a business question with a real answer,
and it is the only one available.</p>"""),
    ],
    """None of these appears in the <a href="../quiz/c31.html">C3 W1 mock quiz</a>, which
covers the two steps, the distortion and anomaly detection.""")),
    ],
)
