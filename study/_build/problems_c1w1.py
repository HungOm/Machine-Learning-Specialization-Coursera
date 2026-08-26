# -*- coding: utf-8 -*-
"""C1 W1 — the model, the cost, and gradient descent, by hand."""
from problemkit import P, m, pre, cols

L = []
def add(*a, **k): L.append(P(*a, **k))

add("c1w1-p01", level=1, tag="the model",
    lesson="c1/w1-04-linear-regression-model.html",
    ask="A house-price model is %s, where %s is size in square feet and %s is price in "
        "thousands. Predict the price of a 1500 sq ft house, and say what %s and %s mean "
        "in plain words." % (m("f(x) = 0.2x + 50"), m("x"), m("f(x)"), m("w = 0.2"), m("b = 50")),
    steps=[("Substitute x = 1500", "f(1500) = 0.2 × 1500 + 50"),
           ("Multiply first", "0.2 × 1500 = 300"),
           ("Then add b", "300 + 50 = 350")],
    answer="%s, i.e. <b>$350,000</b>. %s: each extra square foot adds $200. %s: the price a "
           "0 sq ft house would cost — the line's starting height, not a meaningful house."
           % (m("f(1500) = 350"), m("w = 0.2"), m("b = 50")),
    why="w is a rate and b is an offset. Every model in this specialization has this same "
        "pair, however many features there are.")

add("c1w1-p02", level=2, tag="cost function",
    lesson="c1/w1-05-cost-function-formula.html",
    ask="Training set: %s. For the model %s (so %s), compute %s."
        % (m("(1, 1), (2, 2), (3, 3)"), m("f(x) = 0.5x"), m("w = 0.5, b = 0"),
           m("J(0.5, 0)")),
    hint="Four columns: x, prediction, error, error². Then sum and divide by 2m.",
    steps=[("Predictions with w = 0.5", "f(1)=0.5, f(2)=1.0, f(3)=1.5"),
           ("Errors, prediction minus target", "0.5−1 = −0.5, &nbsp; 1−2 = −1, &nbsp; 1.5−3 = −1.5"),
           ("Squares", "0.25, 1, 2.25"),
           ("Sum", "3.5"),
           ("Divide by 2m with m = 3", "3.5 ÷ 6")],
    answer=m("J(0.5, 0) ≈ 0.583"),
    why="Note the perfect model here would be w = 1, giving J = 0. Cost measures how wrong "
        "a particular choice of w and b is — it is a score for the line, not for the data.")

add("c1w1-p03", level=2, tag="cost intuition",
    lesson="c1/w1-06-cost-function-intuition.html",
    ask="Same data %s. Compute %s and %s. What do the three numbers "
        "(with %s from the previous problem) tell you about the shape of %s?"
        % (m("(1,1), (2,2), (3,3)"), m("J(1, 0)"), m("J(1.5, 0)"), m("J(0.5,0) ≈ 0.583"), m("J(w)")),
    steps=[("w = 1: predictions are 1, 2, 3 — exactly the targets", "all errors 0 → J = 0"),
           ("w = 1.5: predictions are 1.5, 3, 4.5", "errors 0.5, 1, 1.5"),
           ("Square and sum", "0.25 + 1 + 2.25 = 3.5"),
           ("Divide by 2m = 6", "3.5 ÷ 6 ≈ 0.583"),
           ("Compare the three", "J(0.5) ≈ 0.583,  J(1) = 0,  J(1.5) ≈ 0.583")],
    answer="%s and %s. The cost is a <b>symmetric bowl</b> with its lowest point at "
           "%s — equally wrong in either direction."
           % (m("J(1,0) = 0"), m("J(1.5,0) ≈ 0.583"), m("w = 1")),
    why="That bowl shape is why gradient descent works at all: from anywhere on it, downhill "
        "leads to the same single bottom. Squared error was chosen to guarantee this.")

add("c1w1-p04", level=2, tag="gradient descent",
    lesson="c1/w1-09-implementing-gradient-descent.html",
    ask="You are at %s with %s and %s, and %s. Perform one update step. "
        "Show the new %s and %s."
        % (m("w = 3, b = 1"), m("∂J/∂w = 4"), m("∂J/∂b = −2"), m("α = 0.1"), m("w"), m("b")),
    hint="The rule is: new = old − α × (its own derivative). Both updates use the OLD values.",
    steps=[("w update", "w = 3 − 0.1 × 4 = 3 − 0.4"),
           ("b update — note the minus of a minus", "b = 1 − 0.1 × (−2) = 1 + 0.2"),
           ("Both use the old w and b, computed before either changed",
            "this is what “simultaneous update” means")],
    answer="%s and %s" % (m("w = 2.6"), m("b = 1.2")),
    why="Updating w and then using the new w to compute b's gradient is the classic "
        "gradient-descent bug. It often still converges, which is why it survives so long.")

add("c1w1-p05", level=3, tag="the gradient formulas",
    lesson="c1/w1-12-gradient-descent-for-linear-regression.html",
    ask="With data %s and current %s, compute %s and %s using<br>"
        "%s and %s"
        % (m("(1, 2), (2, 4)"), m("w = 0, b = 0"), m("∂J/∂w"), m("∂J/∂b"),
           m("∂J/∂w = (1/m) Σ (f(x<sup>(i)</sup>) − y<sup>(i)</sup>) x<sup>(i)</sup>"),
           m("∂J/∂b = (1/m) Σ (f(x<sup>(i)</sup>) − y<sup>(i)</sup>)")),
    hint="With w = 0 and b = 0 every prediction is 0, so every error is just −y.",
    steps=[("Predictions", "f(1) = 0, f(2) = 0"),
           ("Errors (prediction − target)", "0−2 = −2, &nbsp; 0−4 = −4"),
           ("For ∂J/∂w, multiply each error by its own x", "(−2)(1) = −2, &nbsp; (−4)(2) = −8"),
           ("Sum and divide by m = 2", "(−2 + −8) ÷ 2 = −5"),
           ("For ∂J/∂b, just average the errors", "(−2 + −4) ÷ 2 = −3")],
    answer="%s and %s. Both negative, so the update <b>increases</b> both w and b — correct, "
           "since the line starts flat at zero and needs to rise."
           % (m("∂J/∂w = −5"), m("∂J/∂b = −3")),
    why="The only difference between the two formulas is the extra x. That x is why features "
        "on wildly different scales produce wildly different gradients — the reason scaling matters.")

add("c1w1-p06", level=2, tag="learning rate",
    lesson="c1/w1-11-learning-rate.html",
    ask="You plot %s against iteration number and see each of these. Diagnose each and say "
        "what to do:<br>(a) a curve that falls smoothly and flattens<br>"
        "(b) a curve that rises<br>(c) a curve that falls but is still falling steeply at "
        "the last iteration<br>(d) a curve that zig-zags up and down" % m("J"),
    steps=[("(a) falling and flattening", "working, and converged — stop, or leave it"),
           ("(b) rising", "α too large — J should never increase. Try α ÷ 3"),
           ("(c) still falling steeply", "not converged yet — run more iterations, or raise α"),
           ("(d) zig-zag", "α too large: each step overshoots the bottom and lands up the "
            "far side. Reduce α")],
    answer="(a) converged &nbsp;(b) α too big &nbsp;(c) needs more iterations &nbsp;(d) α too big",
    why="A rising J is never a data problem or a formula problem first — check α before you "
        "check anything else. Andrew Ng's advice: try 0.001, 0.01, 0.1, 1, each 3× the last.")

add("c1w1-p07", level=1, tag="supervised vs unsupervised",
    lesson="c1/w1-02-supervised-learning.html",
    ask="Label each as supervised regression, supervised classification, or unsupervised:<br>"
        "(a) predict tomorrow's temperature<br>(b) decide if a transaction is fraud<br>"
        "(c) group customers into segments nobody has defined<br>"
        "(d) predict how many days until a machine fails",
    steps=[("(a) a number, from labelled history", "supervised regression"),
           ("(b) one of two labels, from labelled examples", "supervised classification"),
           ("(c) no labels at all — the groups are the output", "unsupervised"),
           ("(d) a number again, even though it sounds like an event", "supervised regression")],
    answer="(a) regression (b) classification (c) unsupervised (d) regression",
    why="The give-away is not the subject matter, it is: <i>is there a right answer in the "
        "training data, and is that answer a number or a category?</i>")

add("c1w1-p08", level=3, tag="two steps of gradient descent",
    lesson="c1/w1-13-running-gradient-descent.html",
    ask="Data: %s. Start at %s, fix %s at 0 (do not update it), and use %s. "
        "Run <b>two</b> steps of gradient descent on %s. Is the cost going down?"
        % (m("(1, 2), (2, 4)"), m("w = 0"), m("b"), m("α = 0.1"), m("w")),
    hint="Reuse the gradient from problem 5 for the first step. Then recompute it with the "
         "new w — it changes every step.",
    steps=[("Step 1 gradient (from problem 5, with w = 0)", "∂J/∂w = −5"),
           ("Step 1 update", "w = 0 − 0.1(−5) = 0.5"),
           ("Step 2: predictions with w = 0.5", "f(1) = 0.5, f(2) = 1.0"),
           ("Errors", "0.5 − 2 = −1.5, &nbsp; 1.0 − 4 = −3.0"),
           ("Times x, summed, ÷ m", "[(−1.5)(1) + (−3.0)(2)] ÷ 2 = (−1.5 − 6.0) ÷ 2 = −3.75"),
           ("Step 2 update", "w = 0.5 − 0.1(−3.75) = 0.875"),
           ("Cost check: J(0) = (4 + 16)/4 = 5; J(0.5) = (2.25 + 9)/4 = 2.8125; "
            "J(0.875) = (1.265625 + 5.0625)/4 ≈ 1.582", "5 → 2.81 → 1.58")],
    answer="%s then %s, with cost falling %s. It is heading for %s, where the fit is exact."
           % (m("w = 0.5"), m("w = 0.875"), m("5 → 2.81 → 1.58"), m("w = 2")),
    why="Notice the steps get smaller as you approach the bottom, without α changing. The "
        "gradient shrinks on its own — that is why a fixed learning rate still converges.")

add("c1w1-p09", level=2, tag="reading a contour plot",
    lesson="c1/w1-07-visualizing-the-cost-function.html",
    ask="On a contour plot of %s, you see tight concentric ellipses. "
        "(a) Where is the best model? (b) What does a very stretched, thin ellipse tell you? "
        "(c) Which direction does gradient descent step in?" % m("J(w, b)"),
    steps=[("(a) contours are lines of equal cost, like height on a map",
            "the innermost ring is the minimum"),
           ("(b) stretched contours mean cost changes fast one way and slowly the other",
            "features on very different scales"),
           ("(c) the gradient points straight uphill, so the step goes straight downhill",
            "perpendicular to the contour line")],
    answer="(a) the centre of the innermost ellipse &nbsp;(b) badly scaled features &nbsp;"
           "(c) perpendicular to the contour, downhill",
    why="A thin valley is exactly what makes gradient descent zig-zag: it keeps bouncing "
        "across the narrow direction while creeping along the long one. Scaling makes the "
        "ellipse circular and the path direct.")

add("c1w1-p10", level=2, tag="cost vs error",
    lesson="c1/w1-05-cost-function-formula.html",
    ask="Why does the cost function square the errors instead of just adding them up? "
        "Give two distinct reasons, using %s as an example."
        % m("errors of +3 and −3"),
    steps=[("Plain sum", "3 + (−3) = 0 — a terrible model scores perfectly"),
           ("Squares cannot cancel", "9 + 9 = 18 — the badness survives"),
           ("Second reason: squaring makes J a smooth bowl with one minimum, so the "
            "derivative exists everywhere and downhill always leads to the same place",
            "absolute values give a kink at zero")],
    answer="(1) Positive and negative errors would cancel, so a bad model could score 0. "
           "(2) Squaring gives a smooth, single-minimum bowl that is easy to differentiate "
           "and safe to descend.",
    why="The ½ in front is a third, smaller convenience: it cancels the 2 that comes down "
        "when you differentiate the square, leaving a tidy gradient.")

add("c1w1-p11", level=3, tag="units and interpretation",
    lesson="c1/w1-04-linear-regression-model.html",
    ask="Two people fit the same house data. One uses size in <b>square feet</b> and gets "
        "%s. The other uses size in <b>thousands of square feet</b>. What w should the "
        "second person get, and what does that tell you about comparing w values between "
        "models?" % m("w = 0.2"),
    hint="If x is divided by 1000, then to keep w·x the same, w must be multiplied by 1000.",
    steps=[("First model, 1500 sq ft", "0.2 × 1500 = 300"),
           ("Second model sees x = 1.5", "w × 1.5 must also be 300"),
           ("Solve", "w = 300 ÷ 1.5 = 200")],
    answer="%s. A weight's size means nothing on its own — it depends entirely on the units "
           "of its feature." % m("w = 200"),
    why="This is why you cannot rank feature importance by comparing raw weights, and part of "
        "why regularization is only fair after scaling: it penalises big weights, and "
        "“big” is a statement about units.")

add("c1w1-p12", level=1, tag="notation",
    lesson="c1/w1-04-linear-regression-model.html",
    ask="In the standard notation, what does each of these mean? "
        "%s, %s, %s, %s, %s"
        % (m("m"), m("x<sup>(i)</sup>"), m("y<sup>(i)</sup>"), m("ŷ"), m("f<sub>w,b</sub>(x)")),
    steps=[("m", "how many training examples there are"),
           ("x<sup>(i)</sup>", "the input of the i-th example — the bracketed i is an index, not a power"),
           ("y<sup>(i)</sup>", "the true output of the i-th example"),
           ("ŷ (“y hat”)", "the predicted output"),
           ("f_{w,b}(x)", "the model — a function of x, with w and b as its settings")],
    answer="m = number of examples · x<sup>(i)</sup>, y<sup>(i)</sup> = the i-th input and its true answer · "
           "ŷ = the prediction · f<sub>w,b</sub>(x) = the model itself.",
    why="The superscript in brackets is an index. Reading x⁽²⁾ as “x squared” makes every "
        "formula in the course incomprehensible, and it is a very easy mistake to make.")

add("c1w1-p13", level=2, tag="when linear fails",
    lesson="c1/w1-04-linear-regression-model.html",
    ask="You fit a straight line and get a large cost that will not improve however long you "
        "train. The learning-rate plot looks healthy — J falls smoothly and flattens. "
        "What are the two possible explanations, and how would you tell them apart?",
    steps=[("Explanation 1: the relationship is not straight", "a line cannot fit a curve, "
            "however well you optimise it"),
           ("Explanation 2: the features do not carry the information",
            "no function of these inputs predicts y well"),
           ("How to tell: plot predictions against actuals, or residuals against x",
            "a pattern in the residuals means a shape you have not modelled"),
           ("A curved residual pattern points at explanation 1", "add polynomial features")],
    answer="Either the true relationship is curved (fix: polynomial or engineered features) "
           "or the features are uninformative (fix: get better features). Plot the "
           "<b>residuals against x</b> — a visible curve means the first, formless scatter "
           "means the second.",
    why="Gradient descent converging tells you it found the best <i>line</i>. It says nothing "
        "about whether a line was ever the right thing to look for.")

SET = dict(course="C1", week=1, title="Regression, cost and gradient descent",
           lede="The whole of Week 1 is one loop: predict, measure how wrong you are, step "
                "downhill, repeat. These problems make you run that loop by hand, which is "
                "the only way it stops being a slogan.",
           problems=L)
