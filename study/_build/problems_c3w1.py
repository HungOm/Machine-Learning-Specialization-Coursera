# -*- coding: utf-8 -*-
"""C3 W1 — clustering and anomaly detection."""
from problemkit import P, m, pre, cols

L = []
def add(*a, **k): L.append(P(*a, **k))

PTS = cols(["#", "x₁", "x₂"],
           [[1, 1.0, 1.0], [2, 1.5, 2.0], [3, 3.0, 4.0],
            [4, 5.0, 7.0], [5, 3.5, 5.0], [6, 4.5, 5.0]])

add("c3w1-p01", level=2, tag="k-means assignment",
    lesson="c3/w1-03-kmeans-algorithm.html",
    ask="Run <b>one assignment step</b> of k-means on these six points with %s, "
        "centroids starting at %s and %s." % (m("k = 2"), m("(1, 1)"), m("(5, 7)")) + PTS,
    hint="For each point compute the distance to both centroids and take the nearer. You can "
         "compare squared distances and skip the square roots entirely.",
    steps=[("Point 2 (1.5, 2): to c₁ √(0.25+1) = 1.118, to c₂ √(12.25+25) = 6.10",
            "→ cluster 1"),
           ("Point 3 (3, 4): to c₁ √(4+9) = 3.61, to c₂ √(4+9) = 3.61",
            "an exact tie — break it consistently, say towards the lower index"),
           ("Point 5 (3.5, 5): to c₁ 4.72, to c₂ 2.5", "→ cluster 2"),
           ("Point 6 (4.5, 5): to c₁ 5.32, to c₂ 2.06", "→ cluster 2"),
           ("Points 1 and 4 are the centroids themselves", "distance 0 to their own")],
    answer="Cluster 1: points <b>1, 2, 3</b> · Cluster 2: points <b>4, 5, 6</b>. "
           "(Point 3 is exactly equidistant — a genuine tie, resolved by convention.)",
    why="Ties are rare with real data but the tie-breaking rule must still be deterministic, "
        "or the same code gives different answers on different runs.")

add("c3w1-p02", level=2, tag="k-means move",
    lesson="c3/w1-03-kmeans-algorithm.html",
    ask="Continue from the previous answer: compute the new centroid positions, then check "
        "whether a second assignment step would change anything.",
    steps=[("Cluster 1 holds (1,1), (1.5,2), (3,4)",
            "mean = ((1+1.5+3)/3, (1+2+4)/3) = (1.833, 2.333)"),
           ("Cluster 2 holds (5,7), (3.5,5), (4.5,5)",
            "mean = ((5+3.5+4.5)/3, (7+5+5)/3) = (4.333, 5.667)"),
           ("Re-assign point 3 (3,4): to c₁ √(1.36+2.78) = 2.03, to c₂ √(1.78+2.78) = 2.14",
            "still cluster 1 — just"),
           ("No point changes cluster", "converged")],
    answer="%s and %s. Nothing moves on the next step, so it has converged."
           % (m("c₁ = (1.833, 2.333)"), m("c₂ = (4.333, 5.667)")),
    why="k-means always converges, because both steps can only lower the cost and there are "
        "finitely many assignments. It just does not always converge to the <i>best</i> answer.")

add("c3w1-p03", level=3, tag="local optima",
    lesson="c3/w1-05-initializing-kmeans.html",
    ask="On the same six points, two initialisations give different final answers:<br>"
        "<b>A</b> starts at points 1 and 4 → clusters {1,2,3} and {4,5,6}, %s<br>"
        "<b>B</b> starts at points 1 and 3 → clusters {1,2} and {3,4,5,6}, %s<br>"
        "Which is better, what does that prove about k-means, and what is the standard fix?"
        % (m("J = 1.778"), m("J = 1.313")),
    steps=[("Lower cost is better", "B, at 1.313, beats A's 1.778"),
           ("Both are converged — neither can improve by another step",
            "both are local optima"),
           ("So the answer k-means gives depends on where it started", "not a global optimum"),
           ("Fix: run it many times from different random initialisations",
            "typically 50–1000 times"),
           ("Keep the run with the lowest J", "the cost function is the referee")],
    answer="<b>B</b> is better (J = 1.313 versus 1.778). This proves k-means finds a "
           "<b>local</b> optimum that depends on initialisation. The fix is to run it many "
           "times from random starts and keep the lowest-cost result.",
    why="This is why the cost function matters even though k-means has no gradient descent: "
        "J is how you choose between runs. Without it you would have no way to tell A from B.")

add("c3w1-p04", level=2, tag="k-means cost",
    lesson="c3/w1-04-kmeans-cost.html",
    ask="The k-means cost is %s. "
        "Explain why this cost can never increase during either step of the algorithm, "
        "taking each step in turn."
        % m("J = (1/m) Σ ‖x<sup>(i)</sup> − μ<sub>c(i)</sub>‖²"),
    steps=[("Assignment step: each point is moved to the nearest centroid",
            "its own term can only shrink or stay equal"),
           ("Centroids do not move during this step", "so no other term changes"),
           ("Move step: each centroid becomes the mean of its points",
            "the mean is exactly the point that minimises the sum of squared distances"),
           ("So each cluster's contribution can only shrink or stay equal",
            "assignments do not change during this step"),
           ("J is bounded below by 0 and never rises", "it must converge")],
    answer="The assignment step moves each point to its nearest centroid, which can only "
           "reduce that point's term. The move step sets each centroid to its cluster's "
           "<b>mean</b>, and the mean is precisely the minimiser of summed squared distance. "
           "Neither step can increase J, and J ≥ 0, so it converges.",
    why="If your implementation ever shows J rising, you have a bug — usually assignments and "
        "centroids being updated in the wrong order or from mixed states.")

add("c3w1-p05", level=2, tag="choosing k",
    lesson="c3/w1-06-choosing-k.html",
    ask="You run k-means for k = 1…8 and record J: %s. "
        "(a) Why can J never increase as k grows? (b) Where is the “elbow”? "
        "(c) Why is the elbow method often unhelpful in practice?"
        % m("[52.1, 24.3, 11.8, 9.9, 8.7, 7.8, 7.1, 6.5]"),
    steps=[("(a) more centroids means every point can be at least as close as before",
            "J is non-increasing in k, by construction"),
           ("(b) look for where the drop suddenly flattens", "52 → 24 → 12 → 9.9: the big "
            "falls stop after k = 3"),
           ("(c) real curves are usually smooth with no sharp corner",
            "the elbow is a matter of opinion"),
           ("Better: choose k by what the clusters are for",
            "3 T-shirt sizes vs 5 is a business decision, not a maths one")],
    answer="(a) Adding a centroid can only bring points closer, so J never rises. "
           "(b) About <b>k = 3</b>. (c) Real J curves are usually smooth, so different people "
           "see the elbow in different places — and the right k is usually decided by the "
           "downstream use, not the plot.",
    why="Note you can never choose k by minimising J, since J is always lowest at k = m, "
        "where every point is its own cluster and the cost is exactly zero.")

add("c3w1-p06", level=2, tag="Gaussian",
    lesson="c3/w1-08-gaussian-distribution.html",
    ask="A feature has values %s. Compute %s and %s (dividing by %s), then "
        "compute %s using %s."
        % (m("[3, 4, 5, 6, 7]"), m("μ"), m("σ²"), m("m"), m("p(x = 7)"),
           m("p(x) = (1/√(2πσ²)) e<sup>−(x−μ)²/(2σ²)</sup>")),
    steps=[("Mean", "(3+4+5+6+7) ÷ 5 = 25 ÷ 5 = 5"),
           ("Squared deviations", "4, 1, 0, 1, 4"),
           ("Variance", "10 ÷ 5 = 2, so σ = 1.414"),
           ("Exponent at x = 7", "−(7−5)² ÷ (2×2) = −4 ÷ 4 = −1"),
           ("Front factor", "1 ÷ √(2π×2) = 1 ÷ √12.566 = 1 ÷ 3.545 = 0.282"),
           ("Multiply", "0.282 × e⁻¹ = 0.282 × 0.368")],
    answer="%s, %s, %s" % (m("μ = 5"), m("σ² = 2"), m("p(7) ≈ 0.1038")),
    why="Compare with p(5) ≈ 0.282 at the mean. Two standard deviations out is already about "
        "2.7× less likely — and that ratio is what anomaly detection thresholds.")

add("c3w1-p07", level=3, tag="anomaly detection",
    lesson="c3/w1-09-anomaly-detection-algorithm.html",
    ask="Two features are fitted as %s and %s. "
        "With %s, classify %s, %s and %s. "
        "Use %s and %s."
        % (m("μ₁ = 5, σ₁² = 2"), m("μ₂ = 10, σ₂² = 4"), m("ε = 0.001"),
           m("(5, 10)"), m("(8, 10)"), m("(5, 16)"),
           m("p₁(5)=0.2821, p₁(8)=0.0297"), m("p₂(10)=0.1995, p₂(16)=0.0022")),
    hint="The features are assumed independent, so the joint probability is the product. "
         "Compare the product against ε, not each feature separately.",
    steps=[("(5, 10) — both at their means", "0.2821 × 0.1995 = 0.0563"),
           ("(8, 10) — first feature 2σ out", "0.0297 × 0.1995 = 0.0059"),
           ("(5, 16) — second feature 3σ out", "0.2821 × 0.0022 = 0.00063"),
           ("Compare each with ε = 0.001",
            "0.0563 > ε · 0.0059 > ε · 0.00063 < ε")],
    answer="%s normal · %s normal · %s <b>anomaly</b>"
           % (m("(5,10)"), m("(8,10)"), m("(5,16)")),
    why="Notice no single feature is impossible on its own. Anomaly detection multiplies, so "
        "several mildly odd values — or one very odd one — can push the product below ε.")

add("c3w1-p08", level=2, tag="anomaly vs supervised",
    lesson="c3/w1-11-anomaly-vs-supervised.html",
    ask="Choose anomaly detection or supervised learning for each, and give the reason:<br>"
        "(a) 20 known fraud cases, 10,000 legitimate, and new fraud tactics appear monthly<br>"
        "(b) 6,000 spam and 6,000 legitimate emails, spam looks much like last year's<br>"
        "(c) finding never-before-seen faults in aircraft engines<br>"
        "(d) predicting which of 5 known machine faults has occurred",
    steps=[("(a) very few positives, and future positives will look different from past ones",
            "anomaly detection"),
           ("(b) plenty of both classes, and future positives resemble past ones",
            "supervised"),
           ("(c) “never before seen” is the definition of the anomaly case",
            "anomaly detection"),
           ("(d) 5 known, well-represented categories", "supervised, multi-class")],
    answer="(a) anomaly (b) supervised (c) anomaly (d) supervised",
    why="The deciding question is not how many positives you have — it is whether the "
        "<i>next</i> positive will look like the ones you have already seen. If not, no "
        "supervised model can learn it.")

add("c3w1-p09", level=3, tag="choosing features",
    lesson="c3/w1-12-choosing-features.html",
    ask="A feature's histogram is strongly right-skewed with a long tail. What transformation "
        "does the course suggest and why? Give the two forms of the transformation.",
    steps=[("The algorithm assumes each feature is roughly Gaussian",
            "a skewed feature breaks that assumption"),
           ("A log compresses large values much more than small ones",
            "the long tail is pulled in"),
           ("Plain log fails on zeros, since log(0) = −∞",
            "so add a small constant"),
           ("Two usual forms", "np.log(x + c) or x**p for a small power p"),
           ("Check the histogram afterwards and tune c or p until it looks bell-shaped",
            "this is a manual, visual step")],
    answer="Take %s (or %s for a small power). The log squashes the long tail so "
           "the feature becomes roughly Gaussian, which is what the algorithm assumes. The "
           "constant %s exists to survive zeros." % (m("log(x + c)"), m("x<sup>p</sup>"), m("c")),
    why="This is one of the few genuinely manual steps in the whole specialization — you look "
        "at a histogram, choose a transform, and look again.")

add("c3w1-p10", level=3, tag="tuning epsilon",
    lesson="c3/w1-10-developing-anomaly-detection.html",
    ask="You have 10,000 normal engines and 20 known faulty ones. Describe how to split this "
        "data and how to choose %s, and explain why the faulty examples must not go in "
        "the training set." % m("ε"),
    steps=[("Training set: normal examples only — this is where μ and σ² are fitted",
            "e.g. 6,000 normal"),
           ("Cross-validation: 2,000 normal + 10 faulty", "used to choose ε"),
           ("Test: 2,000 normal + 10 faulty", "used once, at the end"),
           ("Sweep ε over many values, compute F1 on the cross-validation set each time",
            "not accuracy — the data is extremely skewed"),
           ("Faulty examples must not train μ and σ² because they would widen the fitted "
            "Gaussian", "which makes the anomalies look normal")],
    answer="Fit μ and σ² on <b>normal examples only</b>; put the faulty ones in the "
           "cross-validation and test sets. Sweep ε and pick the value maximising <b>F1</b> "
           "on cross-validation. Including faults in training would inflate σ² and make the "
           "very things you are hunting look ordinary.",
    why="This is the one place where a labelled example is deliberately withheld from "
        "training. The model is meant to describe “normal”, so anything abnormal would "
        "corrupt the description.")

add("c3w1-p11", level=1, tag="clustering uses",
    lesson="c3/w1-01-what-is-clustering.html",
    ask="For each, say whether clustering is the right tool and what the clusters would mean:"
        "<br>(a) group news articles by topic, with no topic list<br>"
        "(b) sort emails into spam and not spam<br>(c) decide how many T-shirt sizes to make<br>"
        "(d) segment customers for a marketing campaign",
    steps=[("(a) no labels, and the groupings are the goal", "yes — clusters are topics"),
           ("(b) you have labelled examples and two known classes",
            "no — supervised classification"),
           ("(c) group body measurements; k is the number of sizes", "yes — clusters are sizes"),
           ("(d) no predefined segments", "yes — clusters are segments")],
    answer="(a) yes (b) <b>no</b> — supervised (c) yes (d) yes",
    why="(c) is the clearest example of k being a business decision. Three sizes fit worse "
        "than five but cost less to manufacture — no cost function knows that.")

add("c3w1-p12", level=2, tag="k-means edge case",
    lesson="c3/w1-05-initializing-kmeans.html",
    ask="During k-means a centroid ends up with <b>no points assigned to it</b>. What breaks, "
        "and what are the two standard responses?",
    steps=[("The move step computes the mean of that cluster's points",
            "the mean of an empty set is 0/0"),
           ("Response 1: drop that centroid", "you now have k − 1 clusters"),
           ("Response 2: re-initialise it at a random data point", "keeps k intact"),
           ("The course's default is to drop it; keeping k matters if k was chosen for an "
            "external reason", "like a fixed number of T-shirt sizes")],
    answer="The move step divides by zero, since the cluster has no points to average. Either "
           "<b>eliminate</b> that centroid (leaving k − 1 clusters) or <b>re-initialise</b> it "
           "at a randomly chosen data point.",
    why="This is much more common than it sounds when k is large or the initialisation is "
        "unlucky — it is one of the reasons k-means++ initialisation exists.")

SET = dict(course="C3", week=1, title="Clustering and anomaly detection",
           lede="Two unsupervised algorithms that look unrelated and share a shape: fit "
                "something simple to the data, then measure how well each point matches. "
                "Both are small enough to run by hand, and doing so is worth it.",
           problems=L)
