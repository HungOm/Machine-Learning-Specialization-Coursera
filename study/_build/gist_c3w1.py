# -*- coding: utf-8 -*-
"""The gist of C3 Week 1."""
import math
from kit import key, trap
from gistkit import gistline, flow, sameskel, chain, bynumbers, retell, ladder, h2
from walkkit import cases, values, point, expr, chainset, ascii_art

_peak = 1 / math.sqrt(2*math.pi)

GIST = dict(
    course="C3", week="1", title="Unsupervised Learning", mins=12,
    scratch=["07-kmeans"],
    lede="Twelve lessons on learning with no answer key at all — and on the strange problems "
         "that creates when there is nothing to measure yourself against.",
    body="".join([
        gistline("""Everything until now had a <b>y</b>. This week does not. Two algorithms,
and both have to bring their own idea of what &ldquo;good&rdquo; means: <b>k-means</b> groups
points that are close together, and <b>anomaly detection</b> learns what normal looks like and
flags what is not."""),

        h2("🖼", "The week in one picture"),
        flow([
            ("note", "Two algorithms, one theme",
             "Both learn from unlabelled data, and both therefore have to decide for "
             "themselves what a good answer is."),
            ("in", "Points, no labels", "k-means"),
            ("arw", "pick K centroids, at K of the actual data points"),
            ("loop", "repeat until nothing moves", [
                ("op", "ASSIGN", "Every point to its nearest centroid. <b>Centroids fixed.</b>"),
                ("op", "MOVE", "Every centroid to the mean of its points. <b>Assignments "
                               "fixed.</b>"),
            ]),
            ("out", "K groups, and a cost J", "which you can compare against another run"),
            ("in", "Normal examples, no labels", "anomaly detection"),
            ("arw", "fit one Gaussian per feature"),
            ("op", "Learn what normal looks like",
             "Just a mean and a variance per column. No optimisation at all."),
            ("arw", "multiply the per-feature probabilities together"),
            ("stop", "p(x) < &epsilon; → anomaly",
             "Mildly unusual in five ways at once <b>multiplies</b> into something very rare."),
        ], cap="""The two halves share a difficulty rather than a mechanism: with no labels,
nothing in the data tells you how many clusters there are, or where to set &epsilon;."""),

        h2("🔁", "What changed, and it is more than it looks"),
        sameskel("""Feature scaling still matters. Vectorised NumPy is still how it is
written. And you are still fitting parameters to data.""",
                 [("The data", "X and y", "<b>X only</b>"),
                  ("What you learn", "a mapping x &rarr; y", "<b>structure in x</b>"),
                  ("How you know it worked", "accuracy on held-out data", "<b>you often "
                                                                          "cannot</b>"),
                  ("The cost", "given by the problem", "<b>chosen by the algorithm</b> — "
                                                       "distortion, or probability"),
                  ("Guaranteed optimum", "yes for C1, no for networks", "<b>no</b> — k-means "
                                                                        "has local optima"),
                  ("How you choose settings", "a validation set", "<b>a downstream purpose</b>, "
                                                                  "or a few labels borrowed "
                                                                  "for evaluation only")]),

        h2("🔢", "The same six points, two answers"),
        bynumbers("""k-means run twice on identical data, from different starting
centroids.""",
                  [("started at points 1 and 4", "J = 1.7778", "clusters [0,0,0,1,1,1]"),
                   ("started at points 1 and 3", "J = 1.3125", "clusters [0,0,1,1,1,1]"),
                   ("difference", "26%", "worse, for the same algorithm on the same data"),
                   ("50 random restarts", "best J = 1.3125", "keeps the better one")],
                  close="""<b>Both runs converged.</b> Neither is broken. They found genuinely
different groupings of one ambiguous point, and one is a <b>local optimum</b>. Course 1's
convex bowl guaranteed this could not happen; k-means has no such guarantee — so you run it
50 to 1000 times and keep the lowest J. The tiebreaker is <b>free</b>: J is already computed
and lower is unambiguously better."""),

        h2("❓", "The question the data cannot answer"),
        key("""<p><b>You cannot choose K by minimising J.</b> J falls forever — at K = m every
point is its own cluster and J = 0 exactly. &ldquo;Minimise J&rdquo; always answers &ldquo;use
as many clusters as you have points&rdquo;.</p>
<p>The <b>elbow method</b> plots J against K and looks for the bend. On the build lane's three
clean blobs it works perfectly: going to K=3 buys <b>8.372</b>, going to K=4 buys
<b>0.106</b> — about eighty times less. On real data the curve usually bends smoothly with no
corner, and Andrew says he rarely uses it.</p>
<p>The reliable alternative is <b>downstream purpose</b>: judge K by how well the clusters
serve the actual use. T-shirt sizes — does 3 or 5 sell better? That is a business question
with a real answer, and the data alone was never going to have one.</p>"""),

        h2("⛓", "Anomaly detection, piece by piece"),
        chain([
            dict(name="Fit a Gaussian per feature",
                 does="Compute a mean and a variance for each column. That is the entire "
                      "training procedure.",
                 code="mu = X.mean(0)\nvar = X.var(0)",
                 trap="<b>p(x) is a density, not a probability.</b> It can exceed 1 — and "
                      "routinely does when &sigma; is small. Only the <b>area</b> under the "
                      "curve is a probability, and the total area is 1.",
                 feeds="a curve per feature, saying what is normal for that column."),
            dict(name="Multiply them together",
                 does="One probability per feature, all multiplied.",
                 say="p of x equals the product over j of p of x j.",
                 code="p = np.prod(gaussian(X, mu, var), axis=1)",
                 trap="It assumes the features are <b>independent</b>, which they usually are "
                      "not — height and weight move together. It works anyway, because it is "
                      "cheap and the errors tend to be conservative. And in practice you sum "
                      "<b>logs</b>, because multiplying dozens of small densities underflows "
                      "to zero.",
                 feeds="one number per example. Now: how small is too small?"),
            dict(name="Choose &epsilon;",
                 does="Flag anything below the threshold.",
                 trap="This needs <b>labels</b> — so the split is unusual: train on "
                      "<b>normal only</b>, and put your handful of known anomalies in CV and "
                      "test. Training stays unsupervised; evaluation borrows just enough "
                      "supervision to tune one number.",
                 feeds=None),
        ]),

        h2("🎯", "The one question that picks the algorithm"),
        key("""<p><b>Do you expect future positive examples to look like the ones you already
have?</b></p>
<p><b>No</b> → anomaly detection. Very few positives, many different failure types, and future
ones may be unlike anything seen. Learn what <b>normal</b> looks like. Fraud, manufacturing
faults.</p>
<p><b>Yes</b> → supervised learning. Plenty of positives sharing a recognisable pattern. Learn
what the <b>positive class</b> looks like. Spam, disease screening.</p>
<p>Fraud is the clean example: every genuinely new fraud is new <b>by definition</b> — the
profitable ones are the ones nobody has seen. A supervised model can only catch frauds
resembling last year's, which is exactly the set that no longer matters.</p>"""),

        h2("📊", "Four numbers about the bell curve"),
        values([("&mu; &plusmn; 1&sigma;", "68%", "the bulk"),
                ("&mu; &plusmn; 2&sigma;", "95%", "the one people quote"),
                ("&mu; &plusmn; 3&sigma;", "99.7%", "almost all of it"),
                ("beyond &plusmn; 4&sigma;", "0.006%", "about <b>1 in 15,000</b>"),
                ("peak height, standard normal", "%.3f" % _peak, "1/&radic;(2&pi;) — and note "
                                                                 "it is <b>not</b> 1")],
               "worth knowing outright"),
        point("""At scale that last row is your entire false-alarm budget. A 4&sigma; event
is rare — but score <b>a million</b> transactions a day and it happens about <b>60 times</b>.
Rare is not never, and choosing &epsilon; is choosing how many false alarms you will tolerate.""",
              "Why 1 in 15,000 matters"),

        h2("🚧", "Choosing features matters more here than anywhere"),
        trap("""<p>There is no label to correct a bad feature choice, so two habits do the
work:</p>
<p><b>Make each feature roughly Gaussian.</b> Plot a histogram. If it is skewed, apply
<code>log(x + c)</code>, <code>&radic;x</code> or <code>x&#8304;&#183;&#179;</code>, and plot
again. The model assumes a bell; give it something bell-shaped.</p>
<p><b>Invent features from your errors.</b> Look at the anomaly that slipped through and ask
what would have caught it. The classic: a broken server with <b>normal CPU</b> and <b>normal
network traffic</b> looks fine on both — but the <b>ratio</b> is wildly abnormal, because it
is working hard while talking to nobody. Neither raw feature could ever see it.</p>"""),

        h2("🗣", "Say the week back"),
        retell([
            "The two steps of k-means, and what each one holds fixed.",
            "Why J can never increase — and what it means if yours does.",
            "Why the <b>mean</b> specifically, in the move step.",
            "What a local optimum looks like here, and the fix.",
            "Why you cannot choose K by minimising J.",
            "The Gaussian formula, and how you fit it — in one sentence.",
            "Why p(x) can be greater than 1.",
            "Why anomaly detection <b>multiplies</b> the per-feature probabilities.",
            "How you split the data when you have only 20 known anomalies, and why train has none.",
            "The one question that decides anomaly detection vs supervised learning.",
            "The two ideas for choosing features here, and the CPU/network example.",
        ]),

        h2("🪜", "Where this week sits in the whole arc"),
        ladder("C3 W1", """The first week with no <b>y</b>, and the shift is bigger than the
algorithms. Without labels there is no accuracy to report, so every algorithm must supply its
own measure of quality — and some questions, like how many clusters there are, have no answer
in the data at all. That is not a gap in the methods; it is the nature of the problem, and
getting comfortable with it is the real content of this week. Week 2 keeps the no-labels
setting and adds something stranger still: learning the <b>features themselves</b>."""),
    ]),
)
