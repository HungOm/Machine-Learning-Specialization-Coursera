# -*- coding: utf-8 -*-
"""C1 W3 — classification, logistic loss, overfitting and regularization."""
from problemkit import P, m, pre, cols

L = []
def add(*a, **k): L.append(P(*a, **k))

add("c1w3-p01", level=1, tag="sigmoid",
    lesson="c1/w3-02-logistic-regression.html",
    ask="For %s with %s and %s, compute %s and %s for %s. "
        "Use %s and %s."
        % (m("z = wx + b"), m("w = 2"), m("b = −4"), m("z"), m("g(z)"), m("x = 1, 2, 3"),
           m("e<sup>2</sup> ≈ 7.389"), m("e<sup>−2</sup> ≈ 0.135")),
    hint="Two stages every time: first the straight line z, then squash it through "
         "g(z) = 1/(1 + e^(−z)).",
    steps=[("x = 1", "z = 2−4 = −2 → g = 1/(1+e²) = 1/8.389 ≈ 0.119"),
           ("x = 2", "z = 4−4 = 0 → g = 1/(1+1) = 0.5"),
           ("x = 3", "z = 6−4 = 2 → g = 1/(1+e⁻²) = 1/1.135 ≈ 0.881")],
    answer=cols(["x", "z", "g(z)"], [[1, -2, 0.119], [2, 0, 0.5], [3, 2, 0.881]]),
    why="x = 2 gives exactly 0.5. That is the decision boundary, and it sits precisely where "
        "z = 0 — never where x = 0.")

add("c1w3-p02", level=2, tag="decision boundary",
    lesson="c1/w3-03-decision-boundary.html",
    ask="A classifier has %s, %s. With a 0.5 threshold, "
        "(a) write the equation of the decision boundary, (b) classify %s, "
        "(c) classify %s."
        % (m("<b>w</b> = [1, 1]"), m("b = −3"), m("(1, 1)"), m("(2, 2)")),
    hint="The threshold 0.5 on g(z) means exactly z = 0, because g(0) = 0.5.",
    steps=[("Predict 1 when g(z) ≥ 0.5, which happens when z ≥ 0", "boundary is z = 0"),
           ("Write z out", "x₁ + x₂ − 3 = 0, i.e. x₁ + x₂ = 3"),
           ("Point (1,1): z = 1+1−3 = −1", "z < 0 → predict 0"),
           ("Point (2,2): z = 2+2−3 = 1", "z > 0 → predict 1")],
    answer="(a) %s &nbsp;(b) predict %s &nbsp;(c) predict %s"
           % (m("x₁ + x₂ = 3"), m("0"), m("1")),
    why="The boundary is a straight line, and you never have to compute a sigmoid to find "
        "it — just set z = 0. That is why it is called a linear classifier.")

add("c1w3-p03", level=2, tag="logistic loss",
    lesson="c1/w3-05-logistic-loss.html",
    ask="The loss for one example is %s when %s and %s when %s. "
        "Compute the loss for each case:<br>"
        "(a) %s (b) %s (c) %s (d) %s<br>"
        "Use %s, %s, %s."
        % (m("−log(f)"), m("y = 1"), m("−log(1 − f)"), m("y = 0"),
           m("y=1, f=0.9"), m("y=1, f=0.1"), m("y=0, f=0.1"), m("y=0, f=0.9"),
           m("log 0.9 ≈ −0.105"), m("log 0.1 ≈ −2.303"), m("natural log")),
    steps=[("(a) y = 1, confident and right", "−log(0.9) ≈ 0.105  → small"),
           ("(b) y = 1, confident and wrong", "−log(0.1) ≈ 2.303  → large"),
           ("(c) y = 0, so use 1 − f = 0.9", "−log(0.9) ≈ 0.105  → small"),
           ("(d) y = 0, so use 1 − f = 0.1", "−log(0.1) ≈ 2.303  → large")],
    answer="(a) %s (b) %s (c) %s (d) %s — <b>confidently wrong is punished about 22× harder "
           "than confidently right is rewarded.</b>"
           % (m("0.105"), m("2.303"), m("0.105"), m("2.303")),
    why="As f approaches 0 while y = 1, the loss goes to infinity. The model is told, in the "
        "strongest possible terms, never to be certain and wrong.")

add("c1w3-p04", level=3, tag="the combined cost",
    lesson="c1/w3-06-simplified-cost-function.html",
    ask="Show that %s "
        "reduces to the right thing for both %s and %s. Then use it to compute the cost of "
        "these three examples: %s."
        % (m("L = −y log(f) − (1 − y) log(1 − f)"), m("y = 1"), m("y = 0"),
           m("(y=1, f=0.9), (y=0, f=0.2), (y=1, f=0.4)")),
    hint="Put y = 1 into the formula and see what happens to the second term. Then put y = 0 "
         "and watch the first term vanish.",
    steps=[("y = 1: the second term has (1 − 1) = 0 in front", "L = −log(f)  ✓"),
           ("y = 0: the first term has 0 in front", "L = −log(1 − f)  ✓"),
           ("Example 1 (y=1, f=0.9)", "−log(0.9) ≈ 0.105"),
           ("Example 2 (y=0, f=0.2)", "−log(0.8) ≈ 0.223"),
           ("Example 3 (y=1, f=0.4)", "−log(0.4) ≈ 0.916"),
           ("Average over m = 3", "(0.105 + 0.223 + 0.916) ÷ 3 ≈ 0.415")],
    answer="It collapses to −log(f) when y = 1 and −log(1 − f) when y = 0. "
           "Cost ≈ %s" % m("0.415"),
    why="One expression instead of an if-statement, so it can be vectorized. The multiply-by-"
        "zero trick to switch off a term appears again in softmax and in collaborative filtering.")

add("c1w3-p05", level=2, tag="why not squared error",
    lesson="c1/w3-04-cost-function-for-logistic-regression.html",
    ask="Why is squared error not used for logistic regression? Name the property it loses "
        "and say what goes wrong for gradient descent.",
    steps=[("Squared error on a sigmoid gives a cost surface with many local dips",
            "non-convex"),
           ("Gradient descent only guarantees “downhill”, and downhill from where you "
            "started may end in a local minimum", "the answer depends on the starting point"),
           ("Logistic loss is convex — one bowl, one bottom", "any start reaches the same "
            "minimum"),
           ("Second problem: squared error gives tiny gradients when the sigmoid saturates, "
            "so a badly wrong confident prediction barely learns", "slow to correct")],
    answer="It loses <b>convexity</b>. Squaring the output of a sigmoid makes a lumpy surface "
           "with many local minima, so gradient descent's result depends on where it started. "
           "Logistic loss restores the single-bowl shape.",
    why="This is the honest answer to “why this strange-looking formula” — it was chosen "
        "specifically so that the optimizer you already have keeps working.")

add("c1w3-p06", level=2, tag="overfitting",
    lesson="c1/w3-08-the-problem-of-overfitting.html",
    ask="Three models on the same data give:"
        + cols(["model", "training error", "test error"],
               [["A", 0.42, 0.44], ["B", 0.08, 0.11], ["C", 0.001, 0.38]])
        + "Diagnose each and say what you would do about it.",
    steps=[("A: high on both, and they agree", "underfitting / high bias"),
           ("B: low on both, and they agree", "a good fit — ship it"),
           ("C: near zero training, high test — a huge gap", "overfitting / high variance"),
           ("Fixes: A needs more capacity (more features, polynomials); C needs less "
            "(regularization, fewer features, more data)", "opposite directions")],
    answer="A underfits (add features or polynomial terms). B is well fitted. C overfits "
           "(regularize, drop features, or get more data).",
    why="The gap between training and test error is the diagnostic, not either number alone. "
        "A training error of 0.001 is a warning sign, not an achievement.")

add("c1w3-p07", level=3, tag="regularized cost",
    lesson="c1/w3-10-cost-function-with-regularization.html",
    ask="With %s, %s and %s, compute the regularization term "
        "%s. Then say what happens to it as λ → 0 and as λ → ∞."
        % (m("<b>w</b> = [3, −4, 1]"), m("λ = 2"), m("m = 10"),
           m("(λ/2m) Σ w<sub>j</sub><sup>2</sup>")),
    steps=[("Square each weight", "9, 16, 1"),
           ("Sum", "9 + 16 + 1 = 26"),
           ("Multiply by λ/2m", "(2 ÷ 20) × 26 = 0.1 × 26"),
           ("λ → 0: the term vanishes", "back to plain logistic regression — may overfit"),
           ("λ → ∞: the only way to keep cost small is w ≈ 0",
            "the model becomes f = g(b), a flat constant — underfits badly")],
    answer="%s. λ → 0 removes regularization entirely; λ → ∞ crushes every weight to zero, "
           "leaving a model that predicts the same thing for every input." % m("2.6"),
    why="Note b is not in the sum. Penalising b would push the model's baseline towards zero "
        "for no benefit — b sets the level, it does not create wiggle.")

add("c1w3-p08", level=3, tag="regularized gradient",
    lesson="c1/w3-11-regularized-gradient-descent.html",
    ask="The regularized update for %s is "
        "%s. "
        "With %s, %s and %s, rewrite the update as “shrink, then step” and compute the "
        "shrink factor."
        % (m("w<sub>j</sub>"),
           m("w<sub>j</sub> := w<sub>j</sub> − α[ (1/m)Σ(f−y)x<sub>j</sub> + (λ/m)w<sub>j</sub> ]"),
           m("α = 0.01"), m("λ = 1"), m("m = 100")),
    hint="Pull the w_j terms together: w_j − α(λ/m)w_j = w_j(1 − αλ/m).",
    steps=[("Group the two w_j terms", "w_j(1 − αλ/m) − α·(1/m)Σ(f−y)x_j"),
           ("Compute the factor", "1 − (0.01 × 1 ÷ 100) = 1 − 0.0001 = 0.9999"),
           ("Read it: every iteration multiplies w by 0.9999 first…", "a 0.01% shrink"),
           ("…then takes the ordinary gradient step", "unchanged from before")],
    answer="%s — each iteration shrinks every weight by 0.01%% and <i>then</i> does the "
           "usual step. This is why regularization is also called <b>weight decay</b>."
           % m("w<sub>j</sub> := 0.9999 w<sub>j</sub> − α·(1/m)Σ(f−y)x<sub>j</sub>"),
    why="Seeing the update as “decay then step” explains the whole mechanism: weights are "
        "pulled towards zero constantly, and only a genuine gradient signal keeps them large.")

add("c1w3-p09", level=2, tag="threshold",
    lesson="c1/w3-03-decision-boundary.html",
    ask="A cancer screening model outputs probabilities. Give the consequence of moving the "
        "decision threshold from 0.5 down to 0.1, and say when you would do it.",
    steps=[("Lower threshold means more cases cross it", "more positive predictions"),
           ("More true positives caught", "fewer missed cancers — higher recall"),
           ("But also more false alarms", "more healthy people sent for tests — lower precision"),
           ("Choose by the cost of each error, not by the maths",
            "a missed cancer costs far more than an unnecessary scan")],
    answer="It catches more real cases (higher recall) at the cost of more false alarms "
           "(lower precision). You do it whenever a <b>miss is more expensive than a false "
           "alarm</b> — screening being the standard example.",
    why="0.5 is a default, not a law. The threshold is a business decision applied after "
        "training; the model itself never has to change.")

add("c1w3-p10", level=1, tag="classification vs regression",
    lesson="c1/w3-01-motivations.html",
    ask="Why can you not simply fit a straight line to 0/1 labels and threshold it at 0.5? "
        "Give two problems.",
    steps=[("Problem 1: a line is unbounded", "it predicts 1.4 and −0.3, which are not "
            "probabilities"),
           ("Problem 2: one far-away point drags the whole line",
            "adding a single extreme x shifts the fitted line and therefore moves the "
            "threshold crossing"),
           ("The sigmoid fixes both: output is always in (0,1), and far-away points saturate "
            "rather than pulling", "bounded and robust")],
    answer="(1) A line is unbounded, so it outputs impossible probabilities. (2) A single "
           "distant example tilts the line and silently moves the decision boundary. The "
           "sigmoid is bounded and saturates, so it does neither.",
    why="The lab that demonstrates this (C1_W3_Lab01) adds one far-right point and watches "
        "the linear boundary move while the logistic one stays put.")

add("c1w3-p11", level=3, tag="regularization and scaling",
    lesson="c1/w3-09-addressing-overfitting.html",
    ask="You regularize a model whose features are size (0–2000) and bedrooms (1–5), "
        "<b>without</b> scaling first. Explain why the penalty is unfair, and which feature "
        "gets unfairly punished.",
    hint="For a feature to have the same influence, a big-range feature needs a small weight "
         "and a small-range feature needs a big weight. Now penalise weights.",
    steps=[("To contribute ~200 to the price, size (≈1000) needs w ≈ 0.2",
            "small weight"),
           ("To contribute ~200, bedrooms (≈3) needs w ≈ 67", "large weight"),
           ("The penalty Σw² sees 0.04 versus 4,489", "over 100,000× harsher on bedrooms"),
           ("So the optimizer shrinks the bedrooms weight hard and leaves size alone",
            "the penalty is about units, not importance")],
    answer="Bedrooms is punished. A small-range feature needs a large weight to have any "
           "effect, and Σw² penalises exactly that. Regularization is only meaningful after "
           "the features are on a common scale.",
    why="Scaling is presented in Week 2 as a speed fix. In Week 3 it becomes a correctness "
        "issue: unscaled regularization silently deletes your small-range features.")

add("c1w3-p12", level=2, tag="reading a fit",
    lesson="c1/w3-08-the-problem-of-overfitting.html",
    ask="For each situation, say whether λ should go up, go down, or stay:<br>"
        "(a) training error 0.02, cross-validation error 0.31<br>"
        "(b) training error 0.29, cross-validation error 0.30<br>"
        "(c) training error 0.05, cross-validation error 0.07",
    steps=[("(a) big gap → overfitting", "increase λ to constrain the model"),
           ("(b) both high and equal → underfitting", "decrease λ, or add features"),
           ("(c) both low and close", "leave it alone")],
    answer="(a) increase λ &nbsp;(b) decrease λ &nbsp;(c) leave it",
    why="λ moves you along one axis: more λ means more bias and less variance. This is the "
        "exact dial that Course 2 Week 3 turns into a systematic procedure.")

add("c1w3-p13", level=3, tag="putting it together",
    lesson="c1/w3-07-gradient-descent-logistic.html",
    ask="Write the vectorized cost and gradient for <b>regularized logistic regression</b>: "
        "given %s, %s, %s, %s and %s, produce the cost and both gradients with no loop."
        % (m("X (m,n)"), m("y (m,)"), m("w (n,)"), m("b"), m("lam")),
    hint="Only three things change from linear regression: a sigmoid on the prediction, a "
         "log-loss instead of squared error, and a λ term on w (never on b).",
    steps=[("Forward", "z = X @ w + b ;  f = 1/(1 + np.exp(-z))"),
           ("Log loss, averaged", "cost = -np.mean(y*np.log(f) + (1-y)*np.log(1-f))"),
           ("Add the penalty — w only, never b",
            "cost += (lam/(2*m)) * np.sum(w**2)"),
           ("The gradient is identical in form to linear regression",
            "err = f - y ;  dj_dw = (X.T @ err)/m ;  dj_db = err.mean()"),
           ("Add the penalty's own derivative, which is (λ/m)w",
            "dj_dw += (lam/m) * w")],
    answer=pre("z = X @ w + b\nf = 1 / (1 + np.exp(-z))\ncost = -np.mean(y*np.log(f) + (1-y)*np.log(1-f))\ncost += (lam / (2*m)) * np.sum(w**2)\n\nerr   = f - y\ndj_dw = (X.T @ err) / m + (lam / m) * w\ndj_db = err.mean()"),
    why="Compare this with the linear-regression version in C1 W2 problem 9: the gradient "
        "lines are <i>character for character the same</i>. Only f changed. That is not a "
        "coincidence — it falls out of the maths of both losses.")

SET = dict(course="C1", week=3, title="Classification, loss and regularization",
           lede="Two things happen this week: the output gets squashed into a probability, "
                "and the cost gets a second job — fit the data, and stay simple. Most of "
                "these problems are about the second job.",
           problems=L)
