# -*- coding: utf-8 -*-
"""C3 · Week 1 — Clustering and anomaly detection."""
from kit import (kid, key, warn, trap, note, card, eq, eqp, decode, table, demo,
                 quiz, links, code, h2, grid2, grid3, pretest, explain)

REPO = "../../C3%20-%20Unsupervised%20Learning,%20Recommenders,%20Reinforcement%20Learning"
L = []

# ============================================================ 1
L.append(dict(
    slug="01-what-is-clustering", title="What is clustering?", mins=8, tag="intuition",
    lede="The first algorithm in this specialization with no y at all. Nobody tells it the answer, and "
         "nobody can mark it right or wrong.",
    body=(
        pretest("""<p>Supervised learning had x and y. <b>Guess what you can still do with only x</b> — and how you would know your answer was any good.</p>""",
        """<p>Watch for what replaces “correct” when there is no answer key. Two different clusterings can both be defensible.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Tip a big box of Lego onto the floor. Nobody tells you what the piles should be. But you
start making them anyway — the reds here, the blues there, the wheels in their own corner.</p>
<p>You weren’t given the answer. You just noticed that some pieces belong together.</p>
<p>That’s clustering. The computer looks at a pile of data and asks: <b>are there natural groups in
here?</b></p>""")

        + h2("🎬", "Watch it move")
        + demo("whatisclustering", "The same points, with and without labels",
               "left: you were given y. right: the algorithm has to find the groups itself")

        + h2("🔢", "Supervised vs unsupervised, precisely")
        + table(["", "Supervised", "Unsupervised"],
                [["Training data", "(x, y) pairs", "<b>x only</b>"],
                 ["The question", "predict y for a new x", "what structure is in x?"],
                 ["Can you score it?", "yes — compare against y", "<b>not directly</b>"],
                 ["Examples so far", "regression, classification, trees", "clustering, anomaly detection, PCA"]])
        + decode([
            ("cluster", "“a group”", "A set of points that are more similar to each other than to points outside it."),
            ("unsupervised", "“no answer key”", "The dataset has no y column. There is nothing to compare a prediction against."),
            ("K", "“how many groups”", "You choose it in advance. The algorithm will not tell you — that is Lesson 6."),
            ("centroid", "“the middle of a cluster”", "The average position of all the points in that cluster. Marked ✕ in every diagram."),
        ])
        + key("""<p>Because there is no y, there is <b>no single correct answer</b>. Two sensible clusterings
of the same data can both be defensible. That is unfamiliar and slightly uncomfortable coming from Course
2 — and it is the honest situation.</p>""")

        + h2("🌍", "Where it gets used")
        + grid3(
            card("<h3>Market segmentation</h3><p>Group customers by behaviour so you can talk to each group "
                 "differently. The classic commercial use.</p>"),
            card("<h3>Genetics</h3><p>Group people or genes by expression patterns. The famous heat-map "
                 "pictures in genomics papers are clustering output.</p>"),
            card("<h3>Astronomy</h3><p>Group stars into galaxies and structures — nobody labelled the sky "
                 "in advance.</p>"))
        + """<p>Andrew’s own examples in the video include grouping DeepLearning.AI learners by why they are
taking the course — to grow skills, to develop a career, to stay current. Nobody filled in a form saying
which they were; the clustering revealed it.</p>"""

        + h2("🕳", "Traps")
        + trap("""<p><b>Expecting clustering to be “right”.</b> It finds structure that exists in the
distances you gave it. Change the features or the scaling and you get different clusters, all equally
valid.</p>""")
        + trap("""<p><b>Forgetting to scale features.</b> Clustering is entirely built on distance. A feature
measured in dollars (0–100,000) will completely drown one measured in years (0–80). <b>Standardise
first.</b></p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("You have customer purchase histories with no labels and want to find natural groups. Supervised or unsupervised?",
             "<p><b>Unsupervised</b> — there is no y. If you had a “churned / did not churn” column you "
             "could do supervised learning instead.</p>"),
            ("Why can't you compute an accuracy for a clustering?",
             "<p>Because there is nothing to compare against. There are internal measures (silhouette "
             "score, distortion) but they measure tightness, not correctness.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("docs", "https://scikit-learn.org/stable/modules/clustering.html",
             "scikit-learn — clustering",
             "K-means plus a dozen others (DBSCAN, hierarchical, spectral). The comparison figure at the top is the most useful thing on the page."),
            ("docs", "https://scikit-learn.org/stable/auto_examples/cluster/plot_cluster_comparison.html",
             "Comparing clustering algorithms on toy datasets",
             "One picture showing where K-means fails and other methods do not. Worth thirty seconds."),
            ("lab", REPO + "/week1/C3W1A/C3W1A1/C3_W1_KMeans_Assignment.ipynb",
             "Week 1 assignment: K-means",
             "In this repo. You implement it from scratch, then use it to compress an image."),
        ])
    )))

# ============================================================ 2
L.append(dict(
    slug="02-kmeans-intuition", title="K-means intuition", mins=9, tag="core",
    lede="Two steps, repeated until nothing changes. That really is the entire algorithm.",
    body=(
        pretest("""<p>Scatter 100 points and 3 flags on a playground. <b>Describe the two-step dance that would sort everyone into three sensible groups.</b></p>""",
        """<p>Whatever you described is probably the algorithm. Watch for which step moves the people and which moves the flags.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>You want to split the class into 3 groups for a game. Here is how:</p>
<ol><li>Drop 3 flags randomly on the playground.</li>
<li><b>Everyone run to your nearest flag.</b> Now you have three groups.</li>
<li><b>Each flag moves to the middle of its own group.</b></li>
<li>Go back to step 2.</li></ol>
<p>Do it a few times and it stops changing — everyone is already at their nearest flag, and every flag is
already in the middle. Done.</p>""")

        + h2("🎬", "Watch it move")
        + demo("kmeansintuition", "Assign, then move, then assign, then move",
               "press ‘step’ to go one half-step at a time")

        + h2("🔢", "The two steps, named")
        + table(["Step", "What it does", "What it holds fixed"],
                [["<b>assign</b>", "each point joins the nearest centroid", "the centroids"],
                 ["<b>move</b>", "each centroid jumps to the mean of its points", "the assignments"]])
        + decode([
            ("centroid μ<sub>k</sub>", "“mu kay”", "The centre of cluster k. Not necessarily a real data point — it is an average."),
            ("c<sup>(i)</sup>", "“c superscript i”", "Which cluster example i currently belongs to. An integer from 1 to K."),
            ("nearest", "“smallest distance”", "Ordinary straight-line distance, squared: ‖x<sup>(i)</sup> − μ<sub>k</sub>‖²."),
            ("convergence", "“nothing moved”", "When an assign step changes no assignments, the algorithm is finished. It always gets there."),
        ])
        + key("""<p>Neither step is clever. What makes it work is that <b>both steps reduce the same
quantity</b> — the total squared distance from points to their own centroid. Lesson 4 makes that
precise.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>An empty cluster.</b> If a centroid ends up with no points, its mean is undefined
(0/0). Standard fixes: delete it and continue with K−1, or re-initialise it at a random point. The
assignment mentions this explicitly.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("What happens if you run the assign step twice with no move step in between?",
             "<p>Nothing changes the second time. Every point is already at its nearest centroid.</p>"),
            ("Must a centroid be one of the data points?",
             "<p>No. It is an <em>average</em>, so it usually sits at a location where no data point is. "
             "(The variant that insists on real points is called k-medoids.)</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("paper", "https://projecteuclid.org/ebooks/berkeley-symposium-on-mathematical-statistics-and-probability/Proceedings-of-the-Fifth-Berkeley-Symposium-on-Mathematical-Statistics-and/chapter/Some-methods-for-classification-and-analysis-of-multivariate-observations/bsmsp/1200512992",
             "MacQueen (1967) — Some methods for classification and analysis of multivariate observations",
             "Where the name “k-means” comes from. Lloyd described the same procedure in 1957 inside Bell Labs; it was not published until 1982."),
            ("play", "https://www.naftaliharris.com/blog/visualizing-k-means-clustering/",
             "Visualizing K-means clustering",
             "Click to place your own centroids and step through by hand. Excellent."),
        ])
    )))

# ============================================================ 3
L.append(dict(
    slug="03-kmeans-algorithm", title="The K-means algorithm", mins=14, tag="core",
    lede="The same two steps, written as maths and as code — with the notation that shows up in the "
         "assignment.",
    body=(
        pretest("""<p>K-means alternates two steps until nothing changes. <b>Guess whether it is guaranteed to stop</b> — and whether stopping means it found the best answer.</p>""",
        """<p>Watch for the difference between converging and converging to the <em>right</em> place.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>You have a pile of dots and you want to sort them into two groups, but nobody
has told you what the groups are.</p>
<p>So you guess. Drop two pins on the page at random. Every dot joins whichever pin it is nearer
to &mdash; that is group one and group two. Now look at each group and move its pin to the middle
of the dots that joined it.</p>
<p>Some dots are now nearer the <i>other</i> pin, so they switch sides. Move the pins again.
Repeat until nobody switches. That is the whole algorithm, and the two steps below are those two
sentences written in symbols.</p>""")

        +h2("🔢", "The maths, decoded")
        + eqp([
            ('<var>c</var><sup>(<var>i</var>)</sup> <span class="op">:=</span>', "assign-op", "becomes, not equals"),
            ' <span class="op">arg min</span><sub><var>k</var></sub> ',
            ('‖ <var>x</var><sup>(<var>i</var>)</sup> <span class="op">−</span> <var class="hl-a">μ</var><sub><var>k</var></sub> ‖<sup>2</sup>',
             "sq-distance", "distance to each candidate centroid"),
        ], "step 1 — assign every point to its nearest centroid — hover or click a part")
        + eqp([
            ('<var class="hl-a">μ</var><sub><var>k</var></sub> <span class="op">:=</span>', "assign-op", "becomes, not equals"),
            ' ',
            ('<span class="frac"><span>1</span><span>|<var>C</var><sub><var>k</var></sub>|</span></span>', "avg-factor", "the average"),
            ('<span class="big">Σ</span><sub><var>i</var> ∈ <var>C</var><sub><var>k</var></sub></sub> <var>x</var><sup>(<var>i</var>)</sup>', "sigma", "over this cluster's own points"),
        ], "step 2 — move every centroid to the mean of its own points — hover or click a part")
        + decode([
            ("arg min", "“the k that makes it smallest”", "Not the smallest distance itself — the <em>index</em> of whichever centroid is nearest."),
            ("‖ · ‖²", "“squared distance”", "(x₁−μ₁)² + (x₂−μ₂)² + … Squaring avoids a square root and makes the maths cleaner; it does not change which centroid is closest."),
            ("|C<sub>k</sub>|", "“how many are in cluster k”", "The count of points currently assigned to k."),
            (":=", "“becomes”", "Assignment, not equality. The new value is computed from the old ones."),
        ])

        + h2("🎬", "Watch it move")
        + demo("kmeansalgo", "The full algorithm — change K and watch it re-converge",
               "the shaded regions show which centroid owns which patch of space")

        + h2("💻", "In code")
        + code("""
import numpy as np

def find_closest_centroids(X, centroids):
    K = centroids.shape[0]
    idx = np.zeros(X.shape[0], dtype=int)
    for i in range(X.shape[0]):
        distances = np.linalg.norm(X[i] - centroids, axis=1)   # one distance per centroid
        idx[i] = np.argmin(distances)                          # <- arg min
    return idx

def compute_centroids(X, idx, K):
    centroids = np.zeros((K, X.shape[1]))
    for k in range(K):
        points = X[idx == k]                                   # boolean mask
        if len(points) > 0:
            centroids[k] = points.mean(axis=0)                 # <- the mean
    return centroids

for _ in range(max_iters):
    idx = find_closest_centroids(X, centroids)
    centroids = compute_centroids(X, idx, K)
""")
        + """<p>Those two functions are the graded exercises in the Week 1 assignment. The loop underneath
is given to you.</p>"""
        + warn("""<p><code>np.linalg.norm(X[i] - centroids, axis=1)</code> relies on broadcasting:
<code>X[i]</code> is shape (n,) and <code>centroids</code> is (K, n), so the subtraction produces (K, n)
and the norm along axis 1 gives K distances. If you are unsure, print the shapes.</p>""")

        + h2("🧮", "One real run, iteration by iteration")
        + """<p>The assignment’s 300-point data set, started from the centroids the lab hands you —
[3, 3], [6, 2], [8, 5]. Watch where they end up:</p>"""
        + table(["", "centroid 0", "centroid 1", "centroid 2"],
                [["start", "(3.00, 3.00)", "(6.00, 2.00)", "(8.00, 5.00)"],
                 ["after 10 iterations", "(1.95, 5.03)", "(3.04, 1.02)", "(6.03, 3.00)"]])
        + """<p>Cluster sizes at the end: <b>98, 102, 100</b> — a near-perfect three-way split of the
300 points, which is a good sign that <var>K</var> = 3 matched the data. Nothing supervised
happened; no label was ever supplied. The only inputs were the points, the number 3, and three
starting positions.</p>
<p>Note how far the centroids travelled. Centroid 0 started at (3, 3) — in the middle of what turned
out to be cluster 1’s territory — and migrated to (1.95, 5.03). The starting positions do not have
to be good. They have to be <em>different</em>.</p>"""
        + explain("""<p>Both steps are simple, and neither one “knows” where the clusters are.
<b>Why does alternating them find the clusters anyway?</b></p>""",
                  """<p>Because each step improves the other’s input. Given fixed centroids, the best
possible assignment is “join the nearest” — that is not a guess, it is optimal. Given fixed
assignments, the best possible centroid is the mean of its members — also optimal. Neither step can
solve the whole problem, but each one is exactly right given the other’s current answer, so
alternating them can only ever improve the arrangement. The next lesson turns “can only improve”
into a number you can watch.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("X has 300 points in 2-D and K = 5. What are the shapes of idx and centroids?",
             "<p><code>idx</code> is <b>(300,)</b> — one cluster index per point. <code>centroids</code> "
             "is <b>(5, 2)</b> — five centres, each with two coordinates.</p>"),
            ("Why square the distance instead of taking the square root?",
             "<p>It is cheaper, and the ordering is identical — whichever centroid minimises the squared "
             "distance also minimises the distance. Squared distance is also what the cost function uses.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("docs", "https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html",
             "sklearn.cluster.KMeans",
             "The production version. Note <code>n_init</code> (Lesson 5) and <code>init='k-means++'</code>."),
            ("lab", REPO + "/week1/C3W1A/C3W1A1/C3_W1_KMeans_Assignment.ipynb",
             "Week 1 assignment: K-means",
             "In this repo. You write both functions above, then use K-means to compress an image to 16 colours."),
        ])
    )))

# ============================================================ 4
L.append(dict(
    slug="04-kmeans-cost", title="The optimization objective", mins=14, tag="maths",
    lede="K-means is not a heuristic that happens to work. It is gradient-free minimisation of one specific "
         "cost, and both steps provably reduce it.",
    body=(
        pretest("""<p>K-means looks like a heuristic that happens to work. <b>Guess what single quantity both of its steps are secretly reducing.</b></p>""",
        """<p>Watch for the elastic-band picture, and for why the cost can never increase — which makes it a debugging test.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Imagine every person is tied to their flag with an elastic band. The further away, the
more it stretches, and stretched elastic is uncomfortable.</p>
<p>The total discomfort in the whole playground is what K-means is trying to make as small as possible.
Running to your nearest flag reduces it. Moving each flag to the middle reduces it. So it goes down, and
down, and eventually stops.</p>""")

        + h2("🔢", "The maths, decoded")
        + eqp([
            '<var>J</var> <span class="op">=</span> ',
            ('<span class="frac"><span>1</span><span><var>m</var></span></span>', "avg-factor", "the average"),
            ('<span class="big">Σ</span><sub><var>i</var>=1</sub><sup><var>m</var></sup>', "sigma", "for every point"),
            ('‖ <var>x</var><sup>(<var>i</var>)</sup> <span class="op">−</span> <var>μ</var><sub><var>c</var><sup>(<var>i</var>)</sup></sub> ‖<sup>2</sup>',
             "sq-distance", "distance to its own centroid, squared"),
        ], "the distortion — average squared distance from each point to its own centroid — hover or click a part")
        + decode([
            ("<var>J</var>", "“the distortion”", "One number measuring how tight the clusters are. Smaller is tighter."),
            ("μ<sub>c<sup>(i)</sup></sub>", "“the centroid that x-i belongs to”", "A double subscript: c<sup>(i)</sup> is which cluster, and μ of that is its centre. Read it inside out."),
            ("both steps", "“coordinate descent”", "Step 1 minimises J over c with μ fixed. Step 2 minimises J over μ with c fixed. Alternating like this is a classic optimisation strategy."),
        ])
        + key("""<p><b>J can never increase.</b> Not on an assign step, not on a move step. If your
implementation ever shows J going up, you have a bug — most often, updating the centroids before finishing
the assignments.</p>""")

        + h2("🎬", "Watch it move")
        + demo("kmeanscost", "J after every half-step",
               "blue dots follow an assign step, green dots follow a move step — the line only descends")

        + h2("🔬", "Why the mean is the right move")
        + """<p>Step 2 says “move to the mean”. Why the mean specifically, and not the median or something
else? Because the mean is <em>exactly</em> the point that minimises the sum of squared distances to a set
of points. Differentiate Σ(x − μ)² with respect to μ, set it to zero, and μ = the average falls out.</p>
<p>So the move step is not a heuristic — it is the exact solution to “where should this centroid go to
minimise J, given these assignments?”. Using squared distance and using the mean are two halves of one
decision.</p>"""

        + h2("🧮", "Watch J fall, and never rise")
        + """<p>The same run, scored after every iteration:</p>"""
        + table(["iteration", "J (distortion)", ""],
                [["0", "4.0868", "starting positions"],
                 ["1", "3.5479", ""],
                 ["2", "3.3325", ""],
                 ["3", "2.8775", ""],
                 ["4", "1.5490", "big move — a whole group changed hands"],
                 ["5", "0.8975", ""],
                 ["6", "<b>0.8889</b>", "converged"],
                 ["7–9", "0.8889", "nothing moves again"]])
        + """<p>Every number is lower than the one above it, and then it stops dead. That is not luck
and it is not approximately true — it is <b>guaranteed</b>. The assign step moves points to a nearer
centroid, which can only shorten distances. The move step puts each centroid at the mean of its
members, and the mean is by definition the point minimising summed squared distance to them. Neither
step can increase J, so the sequence is non-increasing and bounded below by zero, so it must
converge.</p>"""
        + warn("""<p>This is the single most useful debugging check you have. If your implementation
ever prints a J larger than the previous one, you have a bug — almost always an assign step and a
move step in the wrong order, or a centroid updated before all assignments were computed.</p>""")
        + explain("""<p>J is guaranteed to stop falling, yet K-means is famous for finding bad
answers. <b>How are both true at once?</b></p>""",
                  """<p>Because “cannot go up” is a much weaker promise than “ends up lowest”.
The guarantee says you will reach a point where no single assign-or-move step improves anything —
a <em>local</em> minimum. It says nothing about whether some completely different arrangement scores
better. Convergence is about the algorithm running out of improvements available <em>from where it
is</em>, and where it is was decided by the starting positions. That is precisely the gap the next
lesson closes.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Assuming convergence means optimal.</b> J stops decreasing at a <em>local</em>
minimum. There is no guarantee it is the global one — which is exactly what the next lesson is about.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("Your J goes 5.2 → 4.1 → 4.4 → 3.9. What has gone wrong?",
             "<p>J increased from 4.1 to 4.4, which is impossible. A bug — most likely the centroids are "
             "being updated inside the assignment loop instead of after it.</p>"),
            ("What is J when K = m (one centroid per point)?",
             "<p><b>Zero.</b> Every point is its own centroid, at distance 0. Which is why you cannot "
             "choose K by minimising J.</p>"),
            ("Why does the move step use the mean rather than the median?",
             "<p>Because J is a sum of <em>squared</em> distances, and the mean is the exact minimiser of "
             "that. (The median minimises absolute distances — a different cost, and a different "
             "algorithm.)</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("paper", "https://ieeexplore.ieee.org/document/1056489",
             "Lloyd (1982) — Least squares quantization in PCM",
             "The algorithm’s other name is “Lloyd’s algorithm”. Written in 1957, published 25 years later."),
            ("book", "https://web.stanford.edu/~boyd/vmls/",
             "Boyd & Vandenberghe — Introduction to Applied Linear Algebra, ch. 4",
             "Free. A clean derivation of k-means as an optimisation problem."),
        ])
    )))

# ============================================================ 5
L.append(dict(
    slug="05-initializing-kmeans", title="Initializing K-means", mins=13, tag="core",
    lede="Where you drop the flags decides where you end up. The fix costs one for-loop and is worth "
         "every cycle.",
    body=(
        pretest("""<p>Where you put the flags initially changes the answer. <b>Guess the cheap fix</b> — you are allowed to run the whole thing more than once.</p>""",
        """<p>Watch for how you would choose between the runs, given there is no y to score against.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Roll a ball down a bumpy hill. It stops in a dip — but which dip depends entirely on
where you let go. Some dips are deeper than others.</p>
<p>K-means is exactly like this. Start the flags in a bad place and it settles into a bad answer, quite
happily, with nothing moving.</p>
<p>So: <b>do it fifty times from fifty different starts, and keep whichever run ended up in the deepest
dip.</b> You already have a number that measures depth — that is J.</p>""")

        + h2("🎬", "Watch it move")
        + demo("kmeansinit", "Three random starts, three different answers",
               "same data, same algorithm — and one run is measurably worse")

        + h2("🔢", "The recipe")
        + code("""
best_J, best_centroids, best_idx = float('inf'), None, None

for attempt in range(50):                       # 50 to 1000 is typical
    centroids = X[np.random.choice(m, K, replace=False)]   # K random TRAINING POINTS
    for _ in range(max_iters):
        idx = find_closest_centroids(X, centroids)
        centroids = compute_centroids(X, idx, K)
    J = distortion(X, idx, centroids)
    if J < best_J:
        best_J, best_centroids, best_idx = J, centroids, idx
""")
        + decode([
            ("random initialisation", "“drop the flags randomly”", "Pick K of your actual training examples at random and use them as the starting centroids. Do <b>not</b> pick random coordinates in space."),
            ("<code>replace=False</code>", "“no duplicates”", "Two identical starting centroids collapse into one and you effectively get K−1 clusters."),
            ("local optimum", "“a dip that is not the deepest”", "A configuration where no single step improves J, but a different starting point would have found better."),
            ("<code>n_init</code>", "“how many attempts”", "scikit-learn’s name for this. It defaults to 10 (and to 1 with k-means++ in newer versions — check your version)."),
        ])
        + key("""<p>You already have the tiebreaker for free: <b>pick the run with the lowest J</b>. No
extra machinery, no held-out set, no judgement call.</p>""")

        + h2("🔬", "k-means++")
        + """<p>The smarter initialisation everyone actually uses. Instead of picking all K centroids
uniformly at random, pick the first at random and then pick each subsequent one with probability
proportional to its squared distance from the nearest already-chosen centroid — so new centroids tend to
land far away from existing ones.</p>
<p>Arthur & Vassilvitskii proved this gives an expected result within O(log K) of optimal, and in practice
it converges faster and to better solutions. It is scikit-learn’s default.</p>"""

        + h2("🧮", "Fifty random starts, measured")
        + """<p>Run the whole algorithm 50 times on the same 300 points, each time starting from
three randomly chosen training examples, and record the final J:</p>"""
        + table(["Final J reached", "how many of the 50 runs"],
                [["<b>0.8889</b> — the good answer", "<b>43</b>"],
                 ["≈ 2.855 – 2.861 — a bad local optimum", "7"]])
        + """<p>Seven runs in fifty — about one in seven — converged to an arrangement more than
<b>three times worse</b>, and each of those runs terminated perfectly happily, having genuinely run
out of improvements. Nothing inside a single run can detect this. Its J stopped falling exactly as
the theory promises.</p>
<p>Hence the recipe, which is not a workaround but the standard method: run it 50 to 1,000 times,
keep the run with the lowest J, throw the rest away. Here that costs 50× the compute and turns a
14% chance of a bad answer into essentially zero.</p>"""
        + explain("""<p>Every one of those 50 runs converged correctly. <b>So why does taking the
minimum J across runs give a better answer than any run could give on its own?</b></p>""",
                  """<p>Because J is comparable <em>between</em> runs even though no run can see
outside itself. Each run reports an honest score for the arrangement it found, and those scores sit
on the same scale, so the comparison is meaningful even when every individual run is blind. You are
not improving the algorithm; you are sampling its outcomes and using the one number that lets you
rank them. This works only because K-means has an explicit cost function — which is exactly why the
previous lesson bothered to define one.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Running it once.</b> With K = 2 or 3 you will usually be fine. With K = 8 on real
data, a single run is close to a coin flip.</p>""")
        + trap("""<p><b>Initialising at random coordinates rather than random data points.</b> A centroid
placed in an empty region of space may attract no points at all.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("Three runs give J = 0.42, 0.31, 0.44. Which clustering do you keep?",
             "<p>The one with <b>J = 0.31</b>. Lowest distortion wins — no other criterion needed.</p>"),
            ("Why does the risk of a bad local optimum grow with K?",
             "<p>More centroids means exponentially more ways to arrange them badly — two flags in one "
             "blob while another blob has none.</p>"),
            ("Would running 1000 times guarantee the global optimum?",
             "<p>No. It makes it very likely, not certain. Finding the true global optimum of k-means is "
             "NP-hard.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("paper", "https://theory.stanford.edu/~sergei/papers/kMeansPP-soda.pdf",
             "Arthur & Vassilvitskii (2007) — k-means++: The Advantages of Careful Seeding",
             "The initialisation everyone uses now, with the proof. Short and readable."),
            ("docs", "https://scikit-learn.org/stable/modules/clustering.html#k-means",
             "scikit-learn — k-means, including k-means++",
             "See <code>n_init</code> and <code>init</code>."),
        ])
    )))

# ============================================================ 6
L.append(dict(
    slug="06-choosing-k", title="Choosing the number of clusters", mins=14, tag="core",
    lede="There is no correct K, and the popular method is worse than its reputation. The useful answer is "
         "less mathematical and more honest.",
    body=(
        pretest("""<p>You must pick the number of clusters. If you set k equal to the number of points, <b>what is the cost?</b> Commit before reading.</p>""",
        """<p>Zero — every point is its own cluster. Watch for why the cost curve alone therefore cannot choose k for you.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>How many groups should the class split into? Two? Five? Twenty?</p>
<p>There isn’t a right answer hiding in the children. It depends on <b>what the groups are for</b>. Two
teams for a football match. Five for a quiz. Twenty if everyone is doing their own project.</p>
<p>Same with data. The number of clusters depends on what you plan to do with them.</p>""")

        + h2("🎬", "Watch it move")
        + demo("elbow", "The elbow method, and the method that actually works",
               "J always falls as K rises — so J alone can never choose K for you")

        + h2("🔢", "Why you cannot just minimise J")
        + """<p>J decreases monotonically with K. More centroids can only fit tighter. At K = m every point
is its own cluster and J = 0 exactly. So “choose the K with the lowest J” always answers “as many clusters
as you have points”, which is useless.</p>"""
        + decode([
            ("elbow method", "“look for the bend”", "Plot J against K and pick the point where the curve stops dropping steeply. Sometimes obvious, often not."),
            ("downstream purpose", "“what is it for?”", "Evaluate each K by how well it serves the actual later use. The method Andrew recommends."),
            ("silhouette score", "“a tightness score”", "A per-point measure of how much better its own cluster fits than the next best. Unlike J, it does have an interior maximum — so it <em>can</em> suggest a K."),
        ])
        + key("""<p>Andrew is unusually direct in this video: he does not often use the elbow method, because
on real data the curve is usually a smooth slope with no clear bend. <b>Choose K by what the clusters are
for.</b></p>""")

        + h2("👕", "The t-shirt example, which is the real lesson")
        + grid2(
            card("<h3>K = 3</h3><p>S, M, L. Cheaper to manufacture, simpler inventory, and each shirt fits "
                 "a bit less well.</p>"),
            card("<h3>K = 5</h3><p>XS, S, M, L, XL. Better fit, more customers happy, and five production "
                 "lines instead of three.</p>"))
        + """<p>Both clusterings are correct. The choice is a trade between fit quality and manufacturing
cost — a business decision that the data cannot make for you. Your job is to run both and present the
trade-off honestly.</p>"""

        + h2("🧮", "The elbow, on real data")
        + """<p>Best-of-20 runs at each <var>K</var>, on the same 300 points:</p>"""
        + table(["K", "J", "improvement over K−1"],
                [["1", "6.5255", "—"],
                 ["2", "3.0444", "3.48"],
                 ["<b>3</b>", "<b>0.8889</b>", "<b>2.16</b>"],
                 ["4", "0.7049", "0.18"],
                 ["5", "0.5391", "0.17"],
                 ["6", "0.4027", "0.14"],
                 ["7", "0.3417", "0.06"]])
        + """<p>Read the third column, not the second. Going 2 → 3 buys 2.16. Going 3 → 4 buys 0.18 —
twelve times less. That collapse is the elbow, and here it is unmistakable, because the data really
was built from three clusters.</p>"""
        + warn("""<p>Do not take the clarity of this table as typical. It is clean because the data
is synthetic and genuinely has three groups. On real data J almost always declines smoothly with no
visible bend, and the elbow method gives you nothing. Note also the second column never stops
falling — J at K = 7 is the lowest on the table. <b>Minimising J always chooses the largest K you
allow</b>, right up to one cluster per point and J = 0, which is why J alone can never select
K.</p>""")
        + explain("""<p>J is the objective K-means minimises, yet you must not choose K by minimising
it. <b>Why is the algorithm’s own cost function disqualified from this one decision?</b></p>""",
                  """<p>Because J only measures fit, and K controls capacity. Adding a centroid can
never make the fit worse — it can always sit on a point that was previously far from anything — so J
is monotonically decreasing in K by construction, and comparing across K compares models of
different sizes with a score that rewards size. It is the identical trap as choosing polynomial
degree by training error in Course 2 Week 3. There the fix was held-out data; here there are no
labels to hold out, so the fix has to come from outside the data entirely — from what the clusters
are <em>for</em>.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Comparing J across different K values to pick K.</b> It is a valid comparison
between <em>runs at the same K</em> (Lesson 5) and an invalid one across different K.</p>""")
        + trap("""<p><b>Presenting one clustering as “the” answer.</b> Show two or three, with what each
would mean in practice.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("You are clustering to compress an image into a fixed palette. How do you choose K?",
             "<p>By the trade-off you care about: file size versus visual quality. Try 8, 16, 32 colours "
             "and look at the results. The purpose picks K.</p>"),
            ("Why does J keep falling as K rises?",
             "<p>More centroids means every point can be closer to one. At K = m, J = 0.</p>"),
            ("Is the silhouette score a better way to choose K?",
             "<p>Often yes, because unlike J it has an interior maximum. But it still measures geometric "
             "tightness rather than usefulness — treat it as evidence, not as the decision.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("docs", "https://scikit-learn.org/stable/auto_examples/cluster/plot_kmeans_silhouette_analysis.html",
             "scikit-learn — silhouette analysis for choosing K",
             "The best available automated approach, with the plots to go with it."),
            ("paper", "https://rss.onlinelibrary.wiley.com/doi/10.1111/1467-9868.00293",
             "Tibshirani, Walther & Hastie (2001) — Estimating the number of clusters via the gap statistic",
             "A principled statistical alternative to squinting at an elbow."),
        ])
    )))

# ============================================================ 7
L.append(dict(
    slug="07-finding-unusual-events", title="Finding unusual events", mins=9, tag="intuition",
    lede="The second unsupervised algorithm. Learn what normal looks like from normal examples only, then "
         "flag anything improbable.",
    body=(
        pretest("""<p>Aircraft engines, mostly fine, occasionally faulty — and you have almost no examples of faulty. <b>Guess why a classifier is the wrong tool.</b></p>""",
        """<p>Watch for the shift: instead of learning what broken looks like, learn what normal looks like and flag departures.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>You have tested ten thousand aircraft engines. Every single one was fine — you have
never actually seen a broken one.</p>
<p>A new engine arrives. You cannot ask “does this look like a broken engine?”, because you have no idea
what one looks like.</p>
<p>So you ask a different question: <b>“is this engine WEIRD?”</b> Is it hotter than any engine you have
ever seen? Does it shake in a way none of the others did?</p>
<p>Weird isn’t the same as broken. But weird is worth a closer look — and it is a question you can actually
answer.</p>""")

        + h2("🎬", "Watch it move")
        + demo("anomalyintro", "Drag the test engine around",
               "the further it sits from the crowd, the lower its probability")

        + h2("🔢", "The setup")
        + decode([
            ("anomaly detection", "“spot the odd one out”", "Given a dataset of normal examples, decide whether a new example is unusual."),
            ("density estimation", "“learn where the data lives”", "Build a model p(x) of how likely each possible x is. The technical name for what this algorithm does."),
            ("p(x)", "“probability of x”", "High where the training examples were dense, low out in empty space."),
            ("ε", "“epsilon”, the threshold", "Flag it if p(x) < ε. You choose ε — Lesson 10 shows how."),
        ])
        + key("""<p>Anomaly detection is trained on <b>normal examples only</b>. This is why it can catch a
failure mode that has never occurred before — something no supervised classifier can do, because it has
never seen that class.</p>""")

        + h2("🌍", "Where it is used")
        + grid3(
            card("<h3>Fraud</h3><p>Login frequency, typing speed, transaction pattern. Unusual behaviour "
                 "→ extra verification, not an automatic block.</p>"),
            card("<h3>Manufacturing</h3><p>Engines, circuit boards, batteries. Anything that could fail in "
                 "a way nobody has documented.</p>"),
            card("<h3>Computer clusters</h3><p>Memory use, disk access, CPU load. A machine behaving "
                 "unlike its thousand siblings is worth a look.</p>"))
        + warn("""<p>Note what happens in the fraud case: flagged accounts get <b>additional
verification</b>, not a ban. Anomaly detectors produce suspicion, not proof — designing the human response
matters as much as the model.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("You have 10,000 normal engines and 20 faulty ones. Where do the 20 go?",
             "<p><b>Not into training.</b> They go into the cross-validation and test sets, so you can "
             "measure whether the detector catches them. Training uses normal examples only.</p>"),
            ("Why can anomaly detection catch a failure mode never seen before?",
             "<p>Because it does not model failures at all. It models normality, and anything far from "
             "normal is flagged — whatever the reason.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("docs", "https://scikit-learn.org/stable/modules/outlier_detection.html",
             "scikit-learn — novelty and outlier detection",
             "Isolation Forest, One-Class SVM, Local Outlier Factor — the alternatives to the Gaussian method."),
            ("paper", "https://arxiv.org/abs/1901.03407",
             "Chalapathy & Chawla (2019) — Deep Learning for Anomaly Detection: A Survey",
             "Where the field went after the Gaussian model — autoencoders, GANs, and their trade-offs."),
            ("lab", REPO + "/week1/C3W1A/C3W1A2/C3_W1_Anomaly_Detection.ipynb",
             "Week 1 assignment: anomaly detection",
             "In this repo. Server computers, two features, then 11 features."),
        ])
    )))

# ============================================================ 8
L.append(dict(
    slug="08-gaussian-distribution", title="The Gaussian (normal) distribution", mins=15, tag="maths",
    lede="The bell curve, and the two numbers that define it completely. This is the only new maths in the "
         "anomaly-detection half of the week.",
    body=(
        pretest("""<p>A thousand adult heights, one bar per height. <b>Sketch the shape, then guess how many numbers you need to describe it exactly.</b></p>""",
        """<p>Two. Watch for what each controls, and for how you would estimate both from data.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Measure the height of a thousand adults and draw a bar for each height. You get a
hill: lots of people near the middle, fewer as you go out, almost none at the extremes.</p>
<p>That hill shape turns up everywhere, and it takes exactly <b>two numbers</b> to describe:</p>
<ul><li><b>μ</b> — where the top of the hill is (the average).</li>
<li><b>σ</b> — how wide the hill is (how spread out things are).</li></ul>
<p>Knowing those two, you can say how surprising any particular height is.</p>""")

        + h2("🔢", "The maths, decoded")
        + eqp([
            '<var>p</var>(<var>x</var>) <span class="op">=</span> ',
            ('<span class="frac"><span>1</span><span>√<span class="sqrt">2π</span> <var class="hl-b">σ</var></span></span>',
             "normal-dist-f0", "scales the curve to sum to 1"),
            ('<var>e</var><sup>−<span class="frac"><span>(<var>x</var> − <var class="hl-a">μ</var>)<sup>2</sup></span><span>2<var class="hl-b">σ</var><sup>2</sup></span></span></sup>',
             "exponential-f0", "falls off fast, away from μ"),
        ], "the Gaussian / normal density — hover or click a part")
        + decode([
            ("<var class='hl-a'>μ</var>", "“mu”, the mean", "Where the peak sits. Estimated from data as the plain average."),
            ("<var class='hl-b'>σ</var>", "“sigma”, the standard deviation", "How wide the hill is. Small σ = a tall narrow spike."),
            ("σ²", "“sigma squared”, the variance", "The average squared distance from the mean. σ is its square root."),
            ("(x − μ)²", "“how far from the middle, squared”", "The only place x appears. Symmetric, so ±2 from the mean are equally likely."),
            ("<var>e</var><sup>−(…)</sup>", "“e to the minus”", "Makes the value fall off fast as you move away from μ. This is the bell shape."),
            ("1 / (√2π σ)", "“the normalising constant”", "Nothing conceptual — it scales the curve so the total area is exactly 1."),
        ])
        + eqp([
            '<var>μ</var> <span class="op">=</span> ',
            ('<span class="frac"><span>1</span><span><var>m</var></span></span>', "avg-factor", "the average"),
            ('<span class="big">Σ</span> <var>x</var><sup>(<var>i</var>)</sup>', "sigma", "add up every point"),
            '&nbsp;&nbsp;&nbsp;&nbsp;<var>σ</var><sup>2</sup> <span class="op">=</span> ',
            ('<span class="frac"><span>1</span><span><var>m</var></span></span>', "avg-factor", "the average"),
            ('<span class="big">Σ</span> (<var>x</var><sup>(<var>i</var>)</sup> <span class="op">−</span> <var>μ</var>)<sup>2</sup>',
             "variance-f0", "average squared distance from μ"),
        ], "fitting it to data — just the average, and the average squared deviation — hover or click a part", small=True)

        + h2("🎬", "Watch it move")
        + demo("gaussian", "Drag μ and σ",
               "the shaded region is ±2σ, which always holds about 95% of everything")

        + h2("🧮", "Numbers worth knowing")
        + table(["Range", "Fraction of the data inside", "In anomaly terms"],
                [["μ ± 1σ", "68%", "completely ordinary"],
                 ["μ ± 2σ", "95%", "still normal"],
                 ["μ ± 3σ", "99.7%", "getting unusual"],
                 ["beyond μ ± 4σ", "0.006%", "about 1 in 15,000 — worth a look"]])
        + note("""<p>Statistics courses divide by (m−1) rather than m when estimating the variance, to make
the estimator unbiased. Andrew uses m, and notes that with any reasonable amount of data the difference is
negligible. Do not lose time on it.</p>""", "m or m−1?")

        + h2("🧮", "Fitted to the real server data")
        + """<p>The anomaly-detection assignment gives you 307 servers with two measurements each —
throughput and latency. Fitting a Gaussian per feature is two lines, and here is what they
return:</p>"""
        + code("""
mu  = X.mean(axis=0)                  # [14.1122, 14.9977]
var = X.var(axis=0)                   # [ 1.8326,  1.7097]   -> sd [1.3537, 1.3076]
""")
        + """<p>So a typical server sits at about (14.1, 15.0), and “typical” means within roughly
±1.35 on each axis. Those four numbers <em>are</em> the model — there is nothing else to it. The
whole of training is one call to <code>mean</code> and one to <code>var</code>.</p>
<p>What the numbers buy you is a scale. A server at throughput 14.1 is dead average. One at 17.5 is
2.5 standard deviations out, which the Gaussian says should happen about once in 160 servers. One at
20 is 4.4 out — about once in 200,000. The distribution turns “that looks high” into a
probability.</p>"""
        + explain("""<p>The whole model is a mean and a variance per feature. <b>Why is
<code>var</code> doing more work here than <code>mean</code>?</b></p>""",
                  """<p>Because the mean only says where the centre is, while the variance says how
much distance <em>counts</em>. Move a point 3 units from the centre and its probability depends
entirely on whether the spread is 1.35 or 13.5 — the same displacement is a once-in-a-thousand
anomaly in the first case and utterly ordinary in the second. Anomaly detection is a statement about
distance measured in standard deviations, so the variance is what sets the ruler, and a feature
whose variance is badly estimated will either flag everything or nothing.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>p(x) is a density, not a probability.</b> It can exceed 1 when σ is small — that is
fine. Only the <em>area</em> under the curve is a probability, and the total area is 1.</p>""")
        + trap("""<p><b>Assuming your data is Gaussian.</b> Plenty of real features are not — incomes,
response times, file sizes are all heavily skewed. Lesson 12 shows how to fix that.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("μ = 10, σ = 2. Is x = 16 unusual?",
             "<p>It is 3σ above the mean. About 0.15% of values fall that far above — <b>unusual</b>, "
             "though not extraordinary.</p>"),
            ("What happens to p(x) at x = μ as σ shrinks?",
             "<p>It <b>rises</b>, because the same total area is squeezed into a narrower peak. With "
             "σ = 0.1, p(μ) ≈ 4. Densities are allowed to exceed 1.</p>"),
            ("You estimate σ² from data and get 0. What does that mean?",
             "<p>Every training value was identical. The Gaussian collapses to a spike and any different "
             "value has p ≈ 0 — the feature is useless, and numerically dangerous.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("video", "https://www.3blue1brown.com/lessons/gaussian-integral",
             "3Blue1Brown — why π is in the Gaussian",
             "Where that √2π comes from. Not needed, and delightful."),
            ("docs", "https://seeing-theory.brown.edu/probability-distributions/index.html",
             "Seeing Theory — probability distributions",
             "Interactive. Drag the parameters and watch the shape respond."),
            ("video", "https://www.youtube.com/watch?v=cy8r7WSuT1I",
             "StatQuest — The Normal Distribution, clearly explained",
             "Five minutes, and it sticks."),
        ])
    )))

# ============================================================ 9
L.append(dict(
    slug="09-anomaly-detection-algorithm", title="The anomaly detection algorithm", mins=10, tag="core",
    lede="One Gaussian per feature, multiplied together. Four steps, and the multiplication is where the "
         "power comes from.",
    body=(
        pretest("""<p>Each feature alone looks unremarkable — 1.5σ off, nothing dramatic. <b>Guess what happens when a point is 1.5σ off on six features at once.</b></p>""",
        """<p>Watch for the multiplication. Six mild oddities combine into something astronomically unlikely, and that is the whole trick.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>You check each thing separately. Is the temperature odd? A bit. Is the vibration odd?
A bit. Is the noise odd? A bit.</p>
<p>Now here is the trick: you <b>multiply</b> the “not odd” chances together. Being slightly unusual in
one way is common. Being slightly unusual in <em>five</em> ways at once is very rare — because
0.3 × 0.3 × 0.3 × 0.3 × 0.3 is tiny.</p>""")

        + h2("🔢", "The maths, decoded")
        + eqp([
            ('<var>p</var>(<var>x</var>)', "probability-f0", "a number from 0 to 1"),
            ' <span class="op">=</span> ',
            ('<span class="big">Π</span><sub><var>j</var>=1</sub><sup><var>n</var></sup>', "pi-notation", "multiply every feature's probability"),
            ' <var>p</var>(<var>x</var><sub><var>j</var></sub>; <var>μ</var><sub><var>j</var></sub>, <var>σ</var><sub><var>j</var></sub><sup>2</sup>)',
        ], "multiply the per-feature probabilities together — hover or click a part")
        + decode([
            ("<span class='big'>Π</span>", "“product over j”", "Like Σ but multiplying instead of adding. Capital pi."),
            ("<var>p</var>(x<sub>j</sub>; μ<sub>j</sub>, σ<sub>j</sub>²)", "“the Gaussian for feature j”", "Each feature gets its own μ and σ, fitted independently. The semicolon means “parameterised by”."),
            ("<var>n</var>", "“how many features”", "Two in the pictures, eleven in the assignment, dozens in practice."),
            ("independence", "“the assumption”", "The product formula assumes the features are statistically independent. They usually are not — and it works well anyway."),
        ])

        + h2("🎬", "Watch it move")
        + demo("anomalyalgo", "Two features, one product, one threshold",
               "drag ε and watch which points get flagged")

        + h2("🔢", "The four steps")
        + """<ol>
<li><b>Choose features</b> x₁ … x<sub>n</sub> that you think might expose an anomaly.</li>
<li><b>Fit each one:</b> μ<sub>j</sub> = mean of that feature, σ<sub>j</sub>² = its variance. n Gaussians, fitted independently.</li>
<li><b>For a new x:</b> compute p(x) = Π<sub>j</sub> p(x<sub>j</sub>; μ<sub>j</sub>, σ<sub>j</sub>²).</li>
<li><b>Flag it</b> if p(x) &lt; ε.</li>
</ol>"""
        + key("""<p>The multiplication is what makes this work. A point that is 1.5σ off on one feature is
unremarkable. A point that is 1.5σ off on <b>six</b> features simultaneously has a p(x) hundreds of times
smaller — even though no single feature looked alarming.</p>""")

        + h2("💻", "In code")
        + code("""
def estimate_gaussian(X):
    mu  = X.mean(axis=0)                 # one mean per feature      -> shape (n,)
    var = X.var(axis=0)                  # one variance per feature  -> shape (n,)
    return mu, var

def multivariate_gaussian(X, mu, var):
    # product over features, computed for every row at once
    p = np.exp(-((X - mu) ** 2) / (2 * var)) / np.sqrt(2 * np.pi * var)
    return np.prod(p, axis=1)

mu, var = estimate_gaussian(X_train)     # normal examples only
p = multivariate_gaussian(X_cv, mu, var)
anomalies = p < epsilon
""")
        + warn("""<p>With many features the product <b>underflows</b>: 30 probabilities of 0.1 each
multiply to 10⁻³⁰, and with more features you eventually hit exactly 0.0 in floating point. The standard
fix is to work with <b>log p(x) = Σ log p(x<sub>j</sub>)</b> — sums instead of products. Same ranking, no underflow.
This is the same numerical-stability lesson as C2 W2 L9.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>A feature with variance 0.</b> Division by zero, and p becomes NaN or infinite.
Happens when a column is constant. Drop the feature, or add a tiny epsilon to the variance.</p>""")
        + trap("""<p><b>Worrying about the independence assumption.</b> It is technically wrong almost
always, and the algorithm works regardless. If correlated features genuinely matter, the multivariate
Gaussian (with a full covariance matrix) is the extension — at the cost of needing far more data.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("Three features, each with p = 0.1 for this example. What is p(x)?",
             "<p>0.1 × 0.1 × 0.1 = <b>0.001</b>. Each feature alone was only mildly unusual; together they "
             "are a thousand-to-one shot.</p>"),
            ("Why does p(x) get smaller as you add more features, even for normal examples?",
             "<p>Because you are multiplying more numbers below 1. This means ε must be re-tuned whenever "
             "you change the feature set — it is not transferable.</p>"),
            ("What does the independence assumption actually claim?",
             "<p>That knowing one feature tells you nothing about another. Rarely true — CPU load and "
             "network traffic move together — but the algorithm tolerates it well.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("docs", "https://scikit-learn.org/stable/modules/generated/sklearn.covariance.EllipticEnvelope.html",
             "sklearn — EllipticEnvelope",
             "The multivariate Gaussian version, which does model correlations between features."),
            ("docs", "https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html",
             "sklearn — IsolationForest",
             "A tree-based anomaly detector that makes no distributional assumption at all. Often the better first thing to try in practice."),
            ("lab", REPO + "/week1/C3W1A/C3W1A2/C3_W1_Anomaly_Detection.ipynb",
             "Week 1 assignment: anomaly detection",
             "In this repo. You implement estimate_gaussian and select_threshold."),
        ])
    )))

# ============================================================ 10
L.append(dict(
    slug="10-developing-anomaly-detection", title="Developing and evaluating an anomaly detection system",
    mins=16, tag="core",
    lede="How to tune ε when you have almost no labelled anomalies — and why this half-supervised setup is "
         "not cheating.",
    body=(
        pretest("""<p>You have almost no labelled anomalies. <b>Guess how to tune the threshold ε anyway</b>, and where your few precious anomalies should go.</p>""",
        """<p>Watch for which split gets the labelled anomalies, and why the training set deliberately does not.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>You built the weird-detector. Now: is it any good?</p>
<p>You do actually have a few known-broken engines — say twenty, collected over the years. Not enough to
learn from, but enough to <b>test</b> with.</p>
<p>So: train on the ten thousand good ones. Then hide the twenty broken ones among some good ones and see
how many the detector spots. Turn the ε dial until it catches most of them without crying wolf constantly.</p>""")

        + h2("🎬", "Watch it move")
        + demo("anomalyeval", "Sweep ε and watch precision, recall and F1",
               "the panel on the right shows how the data is split")

        + h2("🔢", "The split")
        + table(["Set", "Contents", "Used for"],
                [["<b>training</b>", "6000 normal, 0 anomalies", "fitting μ and σ — normal examples only"],
                 ["<b>cross-validation</b>", "2000 normal, 10 anomalies", "choosing ε, and choosing features"],
                 ["<b>test</b>", "2000 normal, 10 anomalies", "one final honest measurement"]])
        + """<p>With <em>very</em> few anomalies (say 2 in total) Andrew suggests dropping the test set and
using cross-validation only — accepting that your final number will be optimistic. Better an honest
compromise than pretending 2 examples give a reliable test estimate.</p>"""
        + decode([
            ("unsupervised training", "“normal only”", "μ and σ are fitted without ever seeing an anomaly."),
            ("supervised evaluation", "“a few labels for tuning”", "The handful of known anomalies are used only to choose ε and to score. This is not cheating — it is the only way to tune anything."),
            ("skewed classes", "“1% positives or fewer”", "Which is why accuracy is meaningless here, exactly as in C2 W3 L16."),
        ])
        + key("""<p>Report <b>precision, recall and F1</b>, never accuracy. A detector that flags nothing at
all scores 99.5% accuracy on a dataset that is 0.5% anomalies — and is worthless.</p>""")

        + h2("💻", "Choosing ε")
        + code("""
def select_threshold(y_val, p_val):
    best_epsilon, best_F1 = 0, 0
    step = (p_val.max() - p_val.min()) / 1000

    for epsilon in np.arange(p_val.min(), p_val.max(), step):
        predictions = (p_val < epsilon)
        tp = np.sum((predictions == 1) & (y_val == 1))
        fp = np.sum((predictions == 1) & (y_val == 0))
        fn = np.sum((predictions == 0) & (y_val == 1))
        if tp + fp == 0 or tp + fn == 0:
            continue
        prec = tp / (tp + fp)
        rec  = tp / (tp + fn)
        F1 = 2 * prec * rec / (prec + rec)
        if F1 > best_F1:
            best_F1, best_epsilon = F1, epsilon

    return best_epsilon, best_F1
""")
        + """<p>That is the second graded function in the assignment. Note the sweep: ε is searched over the
range of observed p values, not over a fixed grid — the scale of p depends entirely on how many features
you have.</p>"""

        + h2("🧮", "Choosing ε, and what changes in 11 dimensions")
        + """<p>Sweep ε over 1,000 values and score each against the cross-validation set’s known
anomalies. The assignment’s two data sets give very different answers:</p>"""
        + table(["Data set", "features", "cv anomalies", "best ε", "best F1"],
                [["servers, 2-D", "2", "9 of 307", "<b>8.99 × 10⁻⁵</b>", "<b>0.875</b>"],
                 ["servers, 11-D", "11", "10 of 100", "<b>1.38 × 10⁻¹⁸</b>", "0.615"]])
        + """<p>Two things to take from this. First, <b>ε is not a probability you can reason about
and it is not transferable</b>. It fell by fourteen orders of magnitude simply because p(x) is a
product of eleven per-feature probabilities instead of two, and multiplying eleven numbers each well
below 1 produces a very small number for <em>every</em> example, normal ones included. Never
hand-pick ε; always sweep it.</p>
<p>Second, F1 dropped from 0.875 to 0.615 on the harder set. That is the honest result: 11 features
give more ways to be unusual, but also more ways for a normal server to look unusual by chance in
one of them.</p>
<p>At the chosen ε the 2-D model flags <b>6 of its 307 training servers</b> — about 2%. That is
expected and correct. The training set was assumed normal, not certified normal, and a threshold
tight enough to catch real anomalies will always clip a few ordinary points in the tails.</p>"""
        + explain("""<p>The cross-validation set contains <em>labelled</em> anomalies, yet the model
is fitted on unlabelled data and no label is ever used in fitting. <b>What are those labels actually
buying?</b></p>""",
                  """<p>One number: ε. Everything else — μ, σ² — comes from the unlabelled data, so
the model of “normal” is built without supervision. But the model outputs a probability, and nothing
in the data says how improbable is improbable enough. That single cut point is a decision about
consequences, and the only way to set it defensibly is to check it against cases where you know the
answer. It is a supervised choice bolted onto an unsupervised model — which is why nine labelled
anomalies are enough, when nine would be hopeless for training a classifier.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Putting anomalies in the training set.</b> Then the model learns they are normal, and
p(x) for an anomaly stops being small. Training must be normal-only.</p>""")
        + trap("""<p><b>Tuning ε on the test set.</b> Same optimistic-bias problem as everywhere else. ε is
a hyperparameter — it belongs to cross-validation.</p>""")
        + trap("""<p><b>Reusing an old ε after changing the features.</b> Adding a feature multiplies p by
another factor below 1, shifting the whole scale. Re-tune every time.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("You have 10,000 normal and 20 anomalous examples. Propose a split.",
             "<p>Train: 6000 normal. CV: 2000 normal + 10 anomalies. Test: 2000 normal + 10 anomalies. "
             "Anomalies never appear in training.</p>"),
            ("Your detector flags nothing and scores 99.8% accuracy. What are precision and recall?",
             "<p>Recall = <b>0</b> — it caught nothing. Precision is undefined (0/0), reported as 0. "
             "The 99.8% is pure class imbalance.</p>"),
            ("Why is using labelled anomalies to choose ε not 'cheating'?",
             "<p>Because they are used for evaluation and hyperparameter choice, not for fitting μ and σ. "
             "The learned model of normality never sees them — exactly like a cross-validation set in "
             "supervised learning.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("docs", "https://scikit-learn.org/stable/modules/model_evaluation.html#precision-recall-f-measure-metrics",
             "scikit-learn — precision, recall, F-measure",
             "The metrics from C2 W3, applied here."),
            ("book", "https://info.deeplearning.ai/machine-learning-yearning-book",
             "Machine Learning Yearning",
             "The chapters on evaluation metrics and dev/test set design apply directly."),
        ])
    )))

# ============================================================ 11
L.append(dict(
    slug="11-anomaly-vs-supervised", title="Anomaly detection vs. supervised learning", mins=10, tag="core",
    lede="You have a few labelled positives. Should you build a classifier or a detector? One question "
         "decides it.",
    body=(
        pretest("""<p>You have 20 positive examples. <b>Guess what decides between anomaly detection and a supervised classifier</b> — it is not only the number.</p>""",
        """<p>Watch for the question about future anomalies looking like past ones. That is the real deciding factor.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Two different jobs that look identical from the outside.</p>
<p><b>Spam</b>: you have seen a million spam emails. New spam looks a lot like old spam. So <em>learn what
spam looks like</em> — supervised.</p>
<p><b>Aircraft engine faults</b>: engines fail in ways nobody has ever seen. Tomorrow’s failure might look
nothing like the three you have on record. So <em>learn what normal looks like</em> and flag anything
else — anomaly detection.</p>""")

        + h2("🎬", "Watch it move")
        + demo("anomalyvssupervised", "Two columns, five deciding factors",
               "each row highlights which approach it favours")

        + h2("🔢", "The comparison")
        + table(["", "Anomaly detection", "Supervised learning"],
                [["Positive examples", "very few (0–20)", "many (100s+)"],
                 ["Negative examples", "many", "many"],
                 ["Types of anomaly", "many, and future ones may be unlike past ones", "enough examples of each type; future looks like past"],
                 ["What it learns", "what NORMAL looks like", "what each CLASS looks like"],
                 ["Novel failure modes", "<b>can catch them</b>", "cannot — never seen them"],
                 ["Examples", "fraud, manufacturing faults, machine monitoring, intrusion detection", "spam, weather, disease from symptoms, recurring known defects"]])
        + key("""<p>The deciding question: <b>do you expect future positive examples to look like the ones
you already have?</b> Yes → supervised. No → anomaly detection.</p>""")

        + h2("🔬", "The same domain, both answers")
        + grid2(
            card("<h3>Manufacturing — scratches</h3><p>You see scratched parts every day, hundreds of "
                 "examples, and they all look like scratches. <b>Supervised.</b></p>"),
            card("<h3>Manufacturing — anything else</h3><p>Aircraft engines fail in genuinely novel ways. "
                 "You cannot enumerate them. <b>Anomaly detection.</b></p>"))
        + """<p>Same factory, same cameras, different answers — because the structure of the positive class
differs. This is why the question is about the <em>failure modes</em>, not about the industry.</p>"""
        + note("""<p>Fraud detection drifts over time. Fraudsters actively change tactics to evade whatever
you deployed last month, so this year’s fraud genuinely does not look like last year’s. That adversarial
pressure is precisely why fraud is usually anomaly detection rather than classification.</p>""",
               "Why fraud is on the anomaly side")

        + h2("🔤", "The words, decoded")
        + decode([
            ("positive example", "“a positive”", "An example of the thing you are looking for — a fraud, a defect. The rare class."),
            ("skewed classes", "“imbalanced”", "One class vastly outnumbers the other. Makes accuracy useless as a metric."),
            ("novel anomaly", "“something new”", "A failure unlike anything in your data. Anomaly detection can catch these; a classifier cannot."),
            ("density estimation", "“how likely is this”", "Modelling what normal looks like, then flagging the improbable. What p(x) &lt; ε is doing."),
        ])
        + h2("✅", "Check yourself")
        + quiz([
            ("Detecting previously unknown security exploits in server logs. Which?",
             "<p><b>Anomaly detection.</b> “Previously unknown” is the giveaway — you cannot train a "
             "classifier on attacks that have not been invented yet.</p>"),
            ("Detecting whether a photo contains a cat, with 50,000 labelled cat photos. Which?",
             "<p><b>Supervised.</b> Plenty of positives, and future cats look like past cats.</p>"),
            ("You have 30 examples of one defect type and expect only that type. Which?",
             "<p>Borderline, leaning <b>supervised</b> — 30 is thin but workable, especially with "
             "augmentation and transfer learning (C2 W3 L12–13). The key is that you expect only that "
             "one type.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("paper", "https://dl.acm.org/doi/10.1145/1541880.1541882",
             "Chandola, Banerjee & Kumar (2009) — Anomaly Detection: A Survey",
             "The standard reference. The taxonomy in section 2 is the useful part."),
            ("docs", "https://scikit-learn.org/stable/modules/outlier_detection.html#overview-of-outlier-detection-methods",
             "scikit-learn — outlier vs novelty detection",
             "A distinction worth knowing: outlier detection assumes the training data is already contaminated; novelty detection assumes it is clean."),
        ])
    )))

# ============================================================ 12
L.append(dict(
    slug="12-choosing-features", title="Choosing what features to use", mins=14, tag="core",
    lede="Feature choice matters far more here than in supervised learning — because there is no label to "
         "tell the algorithm which features to ignore.",
    body=(
        pretest("""<p>A feature's histogram is heavily lopsided, not a bell at all. <b>Guess what you would do before feeding it to a Gaussian model.</b></p>""",
        """<p>Watch for the transformations, and for the error-analysis loop that tells you which new feature to invent.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>In supervised learning, a useless feature is mostly harmless — the model just learns to
give it a weight near zero, because the answers tell it to.</p>
<p>Anomaly detection has no answers. So it takes <b>every</b> feature equally seriously. Feed it a useless
one and it will faithfully flag things that are unusual in a way nobody cares about.</p>
<p>Which means: choosing the features <em>is</em> the job here.</p>""")

        + h2("🎬", "Watch it move")
        + demo("featurechoice", "A skewed feature, transformed until it is bell-shaped",
               "drag c in log(x + c) and watch the histogram straighten out")

        + h2("🔢", "Idea 1 — make your features Gaussian")
        + """<p>The algorithm assumes each feature is roughly bell-shaped. When one is not, transform it
until it is. Plot a histogram, apply a transform, plot again, repeat.</p>"""
        + table(["Transform", "Good for", "Note"],
                [["<code>log(x)</code>", "strongly right-skewed data", "fails on zeros — use log(x + c)"],
                 ["<code>log(x + c)</code>", "the same, with zeros present", "tune c by eye; 1 is a common start"],
                 ["<code>np.sqrt(x)</code>", "mildly skewed counts", "same as x<sup>0.5</sup>"],
                 ["<code>x ** 0.3</code>", "in between", "any fractional power is fair game"]])
        + warn("""<p><b>Apply the identical transform to the cross-validation and test sets, and to
production data.</b> A transform fitted on training data and forgotten at inference time is a classic
production bug.</p>""")

        + h2("🔬", "Idea 2 — invent features from your errors")
        + """<p>An anomaly slipped through with a perfectly normal p(x). Do not shrug. <b>Look at that
example by hand</b> and ask what makes it unusual that your current features fail to capture.</p>
<p>Andrew’s example, and it is a good one. A server in a data centre:</p>
<ul>
<li>x₁ = CPU load — normal.</li>
<li>x₂ = network traffic — normal.</li>
<li>But the machine is stuck in an infinite loop: <b>very high CPU with almost no network traffic</b>.</li>
</ul>
<p>Neither feature alone is unusual. Their <b>ratio</b> is wildly unusual. So add x₃ = CPU / network
traffic, and the anomaly becomes obvious.</p>"""
        + key("""<p>This is <b>error analysis</b> (C2 W3 L11), applied to anomaly detection. Look at the
examples you got wrong, and build the feature that would have caught them.</p>""")

        + h2("🧮", "Making a feature Gaussian — measured")
        + """<p>Take a heavily skewed feature, of the kind you get from counts and durations — most
values small, a long tail to the right. <b>Skewness</b> measures the lopsidedness: 0 is a perfect
bell, and anything above about 1 is badly lopsided. Try the usual transforms on 10,000 values:</p>"""
        + table(["Transform", "skewness", ""],
                [["<code>x</code> (raw)", "<b>+4.200</b>", "hopeless — a long right tail"],
                 ["<code>np.sqrt(x)</code>", "+1.566", "better, still lopsided"],
                 ["<code>x ** 0.25</code>", "+0.719", "close"],
                 ["<code>np.log(x + 0.001)</code>", "<b>−0.031</b>", "essentially a perfect bell"]])
        + """<p>The log wins here, and it usually does for counts and durations. The lesson is the
<em>procedure</em>, not the answer: plot a histogram, try <code>log</code>, <code>sqrt</code> and a
fractional power, and keep whichever looks most symmetric. The small constant inside the log exists
only to keep zeros finite — <code>log(0)</code> is −∞ and would poison the whole product.</p>
<p>Why bother: the algorithm’s only tool is a Gaussian, so feeding it a feature with a long right
tail means it will place the mean too high, overestimate the spread, and treat genuinely extreme
values as ordinary. Transforming the feature is not cosmetic — it is making the data match the one
assumption the model has.</p>"""
        + explain("""<p>Applying <code>log</code> to a feature does not change which examples are
largest — the ordering is untouched. <b>So why does it change which examples get flagged?</b></p>""",
                  """<p>Because the model does not rank examples, it scores them against a bell. What
the log changes is the <em>spacing</em>: on the raw scale a handful of huge values sit enormously far
from the crowd, which inflates the estimated variance so much that the bell becomes too wide to call
anything unusual. Compressing the tail brings those points to a sane distance, the variance shrinks
to reflect the bulk of the data, and now a genuinely extreme value stands out. Order is preserved;
what changes is how many standard deviations each gap is worth.</p>""")

        + h2("🔤", "The words, decoded")
        + decode([
            ("skew", "“lopsidedness”", "How far a distribution leans. 0 is a symmetric bell; large positive means a long right tail."),
            ("transform", "“transform”", "Applying log or a root to make a feature look Gaussian. Changes spacing, not order."),
            ("Gaussian", "“normal distribution”", "The bell curve. The one shape this algorithm knows how to model."),
            ("error analysis", "“error analysis”", "Looking at the anomalies you <em>missed</em> and inventing a feature that would have caught them."),
        ])
        + h2("🕳", "Traps")
        + trap("""<p><b>Adding features that are noisy but not informative.</b> Every extra feature is
another chance for a normal example to look unusual by accident, which raises your false-alarm rate. Fewer,
better features beat more features here.</p>""")
        + trap("""<p><b>Transforming after splitting inconsistently.</b> Decide the transform once, apply it
everywhere, and put it in the same pipeline as the model.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("A feature's histogram has a long right tail. What do you try first?",
             "<p><code>log(x + c)</code>, then re-plot the histogram. Adjust c until it looks roughly "
             "symmetric.</p>"),
            ("An anomaly gets a high p(x) — the detector missed it. What now?",
             "<p>Look at that example by hand and work out what makes it strange. Then engineer a feature "
             "that captures it — often a ratio, a difference, or a rate.</p>"),
            ("Why does feature choice matter more here than in supervised learning?",
             "<p>Because there is no y to tell the algorithm which features to down-weight. It treats "
             "every feature as equally important, so an irrelevant one directly generates false alarms.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("docs", "https://scikit-learn.org/stable/modules/preprocessing.html#non-linear-transformation",
             "scikit-learn — power transforms",
             "<code>PowerTransformer</code> (Box-Cox, Yeo-Johnson) finds the best exponent for you, instead of you guessing c."),
            ("docs", "https://scikit-learn.org/stable/auto_examples/preprocessing/plot_map_data_to_normal.html",
             "Mapping data to a normal distribution",
             "Before-and-after histograms for every transform, on real distributions."),
            ("lab", REPO + "/week1/C3W1A/C3W1A2/C3_W1_Anomaly_Detection.ipynb",
             "Week 1 assignment, part 2",
             "In this repo. Scaling from 2 features to 11 — where feature choice starts to bite."),
        ])
    )))

WEEK = dict(
    course="C3", week=1, title="Unsupervised Learning",
    time="~5–7 h with labs",
    goal="Find structure in unlabelled data with K-means, and flag improbable examples with a Gaussian "
         "anomaly detector — including how to evaluate both when there is no y.",
    lessons=L,
)
