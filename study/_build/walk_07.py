# -*- coding: utf-8 -*-
"""Walkthrough for 07_kmeans.py."""
from walkkit import p, expr, chain, chainset, steps, cases, values, point, ascii_art

PICTURE = ([
    ("in", "Points, and no labels at all",
     "This is the difference from everything before it. Nobody tells you the answer, "
     "because there is no answer to tell."),
    ("arw", "pick K starting centroids &mdash; at K of the actual data points"),
    ("loop", "repeat until nothing changes", [
        ("op", "ASSIGN", "Give every point to its nearest centroid. <b>Centroids are held "
                         "fixed.</b>"),
        ("arw", "now the groups have changed, so the middles have moved"),
        ("op", "MOVE", "Put each centroid at the mean of its own points. <b>Assignments "
                       "are held fixed.</b>"),
    ]),
    ("arw", "nothing moved this round"),
    ("out", "K groups", "And a cost, J, which you can compare against another run."),
], "The whole program in one picture",
   "Each step freezes what the other one changes. That is not a detail &mdash; it is the "
   "entire convergence proof.")

WALK = {

"prelude": (
    p("""The first <b>unsupervised</b> file in the lane. There is no y. Nobody knows the
right answer, and there is no right answer to know &mdash; only groupings that are more or
less useful.""")
    + point("""That changes what &ldquo;working&rdquo; means. There is no accuracy to
report, so the algorithm has to bring its own measure of quality, and choosing <b>K</b>
becomes a question the data cannot answer.""")
),

"data": (
    p("""Six points, in two dimensions, chosen so you can see the answer before the
algorithm finds it.""")
    + ascii_art("""   7 |              *  (5, 7)
   6 |
   5 |        *  *     (3.5,5) (4.5,5)
   4 |      *          (3, 4)
   3 |
   2 |   *             (1.5, 2)
   1 | *               (1, 1)
     +--------------------------
       1  2  3  4  5""")
    + p("""Two obvious clumps: the bottom-left pair, and the four up and to the right. Or is
it three clumps? That ambiguity is real, and it is what the local-optima section is
about.""")
),

"assign": (
    p("""Step one. <b>Centroids are fixed.</b> Give every point to its nearest one.""")
    + expr("c[i] = argmin&#8342; &#8214; x[i] - &mu;[k] &#8214;&sup2;",
           "for each point, which centroid is closest")
    + point("""<b>argmin</b>, not <b>min</b> &mdash; you want <b>which</b> centroid, not how
far away it was. That distinction is exactly the one in the Foundations entry on max
versus argmax.""")
    + p("""The distance is <b>squared</b> and never square-rooted. The square root would not
change which centroid is nearest &mdash; it is a monotonic function &mdash; so it is skipped.
And squared distance is what makes the mean the right answer in the next step.""")
),

"move": (
    p("""Step two. <b>Assignments are fixed.</b> Move each centroid to the mean of its own
points.""")
    + expr("&mu;[k] = mean of the points currently assigned to k")
    + point("""Why the <b>mean</b> specifically? Because the mean is the <b>exact
minimiser</b> of squared distance. Not a sensible heuristic &mdash; the provably optimal
answer to &ldquo;what single point is closest to all of these?&rdquo;""")
    + p("""If you measured with absolute distance instead, the optimal answer would be the
<b>median</b>, and you would have a different algorithm (k-medians). The choice of distance
picks the choice of centre.""")
),

"cost": (
    p("""The cost, called <b>distortion</b>: the average squared distance from each point to
its own centroid.""")
    + expr("J = (1/m) &Sigma; &#8214; x[i] - &mu;[c[i]] &#8214;&sup2;")
    + point("""<b>J can never increase.</b> Step 1 gives every point its <i>nearest</i>
centroid, which cannot be worse than where it was. Step 2 moves each centroid to the point
that minimises distance to its own group.""")
    + p("""Since J only falls and cannot fall forever, the algorithm <b>must</b> stop. That
is the entire convergence proof, in two sentences, and it is unusually clean for a machine
learning algorithm.""")
    + point("""It also gives you a free debugging rule: <b>if your implementation ever shows
J rising, you have a bug</b> &mdash; almost always moving some centroids before finishing all
the assignments.""")
),

"fit": (
    p("""The two steps in a loop, until nothing changes. Convergence is detected by
assignments <b>not moving</b>, not by a tolerance on J &mdash; because assignments are
discrete, so &ldquo;nothing changed&rdquo; is exact rather than approximate.""")
),

"local_optima": (
    p("""The same data, the same algorithm, two different starting points. This is the
section that matters.""")
    + values([("start at points 1 and 4", "J = 1.7778", "clusters [0,0,0,1,1,1]"),
              ("start at points 1 and 3", "J = 1.3125", "clusters [0,0,1,1,1,1]")],
             "two runs, two different answers")
    + point("""<b>Both runs converged.</b> Neither is broken. They landed on genuinely
different groupings, and one of them is <b>26% worse</b> than the other.""")
    + p("""That is a <b>local optimum</b>: a grouping where no single point wants to move
and no centroid wants to shift, but which is still not the best available. Course 1's convex
cost bowl guaranteed this could not happen. K-means has no such guarantee.""")
    + point("""Look at the difference: run A put the point at (3, 4) with the bottom-left
pair; run B put it with the top-right group. Both are defensible groupings of an ambiguous
point &mdash; and the numbers say B fits better.""")
),

"restarts": (
    p("""The fix, and it is refreshingly blunt: <b>run it many times and keep the best</b>.""")
    + chain(["50 random restarts", "best J = 1.3125"], "which is run B, the better one")
    + point("""The tiebreaker is <b>free</b>. J is already computed, it is exactly what the
algorithm was minimising, and lower is unambiguously better. No held-out set, no judgement
call &mdash; which is unusual enough to be worth appreciating.""")
    + p("""Note the cluster labels came back as <code>[1,1,0,0,0,0]</code> rather than
<code>[0,0,1,1,1,1]</code>. That is the <b>same grouping</b> with the two labels swapped.
Cluster numbers are arbitrary names, never meaningful &mdash; and comparing two runs by
label equality is a classic mistake.""")
),

"elbow": (
    p("""The last section: how do you choose <b>K</b>? Here are 120 points drawn from
<b>3</b> genuine blobs, so the right answer is known.""")
    + values([("K = 1", "J = 23.648", ""),
              ("K = 2", "J = 9.094", "a drop of <b>14.554</b>"),
              ("K = 3", "J = 0.722", "a drop of <b>8.372</b>"),
              ("K = 4", "J = 0.616", "a drop of <b>0.106</b>")],
             "distortion as K rises, and how much each K bought")
    + point("""Read the <b>drops</b>, not the values. Going to 3 bought <b>8.372</b>. Going
to 4 bought <b>0.106</b> &mdash; about eighty times less. That collapse is the
&ldquo;elbow&rdquo;, and here it points squarely at <b>K = 3</b>, which is the truth.""")
    + p("""So the method works &mdash; on data with three <b>clearly separated</b> blobs.
Real data rarely obliges, and the curve usually bends smoothly with no obvious corner. Andrew
says he rarely uses it, and that is an honest assessment rather than a modesty.""")
    + point("""You <b>cannot</b> choose K by minimising J, because J falls forever: at
K = m every point is its own cluster and J = 0 exactly. The elbow is an attempt to work
around that, and the more reliable alternative is to judge K by <b>what the clusters are
for</b>.""")
),
}
