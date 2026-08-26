# -*- coding: utf-8 -*-
"""C1 W2 — many features, vectorization, scaling, and curved fits."""
from problemkit import P, m, pre, cols

L = []
def add(*a, **k): L.append(P(*a, **k))

add("c1w2-p01", level=1, tag="multiple features",
    lesson="c1/w2-01-multiple-features.html",
    ask="A model has %s and %s, with features "
        "%s. Predict the price of a house with 1200 sq ft, 3 bedrooms, 2 floors, 20 years old."
        % (m("<b>w</b> = [0.1, 4, 10, −2]"), m("b = 80"),
           m("[size, bedrooms, floors, age]")),
    hint="This is a dot product plus b. Multiply each feature by its own weight, add them "
         "all up, then add b.",
    steps=[("size", "0.1 × 1200 = 120"),
           ("bedrooms", "4 × 3 = 12"),
           ("floors", "10 × 2 = 20"),
           ("age — note the negative weight", "−2 × 20 = −40"),
           ("Sum the four, then add b", "120 + 12 + 20 − 40 + 80")],
    answer=m("f(x) = 192") + ", i.e. <b>$192,000</b>",
    why="The negative weight on age is the model saying “older is worth less”. Signs of "
        "weights are readable; magnitudes are not, unless the features are scaled.")

add("c1w2-p02", level=2, tag="vectorization",
    lesson="c1/w2-02-vectorization.html",
    ask="Rewrite this as a single NumPy expression, and say how many Python-level operations "
        "each version performs when %s."
        % m("n = 100,000")
        + pre("f = 0\nfor j in range(n):\n    f = f + w[j] * x[j]\nf = f + b"),
    steps=[("The loop is a dot product plus b", "f = np.dot(w, x) + b"),
           ("Loop version: 100,000 multiplications, 100,000 additions, all interpreted",
            "~200,000 Python steps"),
           ("Vector version: one call into compiled code",
            "1 Python step"),
           ("The compiled code also uses SIMD — several multiplications per clock cycle — "
            "and the loop cannot", "typically 10–100× faster")],
    answer=pre("f = np.dot(w, x) + b") + "One Python operation instead of about 200,000.",
    why="Vectorization is not a style preference. It is the reason the same algorithm is "
        "usable on real data instead of merely correct on toy data.")

add("c1w2-p03", level=2, tag="feature scaling",
    lesson="c1/w2-05-feature-scaling.html",
    ask="A feature has values %s. Rescale 2000 using each method:<br>"
        "(a) max scaling, (b) mean normalization, (c) z-score. "
        "Take %s and %s."
        % (m("300 to 2000"), m("μ = 1150"), m("σ = 500")),
    hint="All three are “subtract something, divide by something”. Only the somethings change.",
    steps=[("(a) max scaling: divide by the largest value",
            "2000 ÷ 2000 = 1"),
           ("(b) mean normalization: (x − μ) ÷ (max − min)",
            "(2000 − 1150) ÷ (2000 − 300) = 850 ÷ 1700 = 0.5"),
           ("(c) z-score: (x − μ) ÷ σ",
            "(2000 − 1150) ÷ 500 = 850 ÷ 500 = 1.7")],
    answer="(a) %s &nbsp; (b) %s &nbsp; (c) %s" % (m("1.0"), m("0.5"), m("1.7")),
    why="Z-score is the default in the labs. Its output is “how many standard deviations "
        "from typical”, which is comparable across features measured in different units.")

add("c1w2-p04", level=3, tag="why scaling matters",
    lesson="c1/w2-05-feature-scaling.html",
    ask="Feature 1 ranges 0–2000, feature 2 ranges 0–5. Explain, using the gradient formula "
        "%s, why gradient descent struggles — and why a single α cannot suit both weights."
        % m("∂J/∂w<sub>j</sub> = (1/m) Σ (error) · x<sub>j</sub>"),
    steps=[("The gradient for w_j is multiplied by that feature's own x", "big x → big gradient"),
           ("Feature 1's gradients are ~400× larger than feature 2's",
            "2000 / 5 = 400"),
           ("One α multiplies both", "α small enough for w₁ is 400× too small for w₂"),
           ("Result: w₁ oscillates or w₂ crawls — the contour plot is a long thin valley",
            "zig-zag descent"),
           ("After scaling, both features have similar spread", "contours become round, "
            "steps go straight at the minimum")],
    answer="Because each weight's gradient carries a factor of its own feature, a feature "
           "400× bigger produces gradients 400× bigger. A single α is then either too big for "
           "one weight or too small for the other. Scaling makes the gradients comparable, "
           "turning a thin valley into a round bowl.",
    why="This is the clearest example in the course of a maths detail with an entirely "
        "practical consequence. Scaling is not tidiness; it is what makes α choosable.")

add("c1w2-p05", level=2, tag="convergence",
    lesson="c1/w2-06-checking-convergence.html",
    ask="Your cost readings over 400 iterations are:"
        + cols(["iteration", "J"], [[0, 5.42], [100, 0.61], [200, 0.30], [300, 0.29], [400, 0.289]])
        + "Has it converged? What automatic test could you have used, and what is the risk "
          "of that test?",
    steps=[("Look at the changes", "5.42 → 0.61 → 0.30 → 0.29 → 0.289"),
           ("The last 100 iterations moved it by 0.001", "essentially flat"),
           ("An automatic test declares convergence when J falls by less than ε in one "
            "iteration, e.g. ε = 0.001", "automatic convergence test"),
           ("Risk: choosing ε is as hard as choosing α — too big and you stop early on a "
            "plateau, too small and you never stop", "prefer looking at the curve")],
    answer="Yes — it is flat by iteration 300. An <b>automatic convergence test</b> stops when "
           "J decreases by less than a chosen ε. The risk is that ε is just as hard to pick "
           "as α: a temporary plateau looks exactly like convergence.",
    why="Andrew Ng's own advice is to look at the plot rather than trust ε. The plot also "
        "tells you <i>why</i> it stopped, which a boolean never does.")

add("c1w2-p06", level=2, tag="learning rate",
    lesson="c1/w2-07-choosing-the-learning-rate.html",
    ask="You try %s and J increases every iteration. You try %s and J barely moves in "
        "1000 iterations. Describe the search strategy you should use and roughly how many "
        "values you would test." % (m("α = 1.0"), m("α = 0.0001")),
    steps=[("α = 1.0 diverges — steps overshoot the minimum and climb the far wall", "too big"),
           ("α = 0.0001 crawls — each step is a rounding error", "too small"),
           ("The usable α is somewhere between; search multiplicatively, not additively",
            "…0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1…"),
           ("Each is roughly 3× the last, so a handful of tries covers four orders of magnitude",
            "about 6–8 values")],
    answer="Search in multiples of about 3 between the two failures: 0.001, 0.003, 0.01, "
           "0.03, 0.1, 0.3. Run each for a few dozen iterations, plot J, and take the "
           "largest α whose curve still falls smoothly.",
    why="Multiplicative search is the right shape because α's effect is multiplicative. "
        "Trying 0.1, 0.2, 0.3 wastes your time in one narrow band.")

add("c1w2-p07", level=3, tag="feature engineering",
    lesson="c1/w2-08-feature-engineering.html",
    ask="You have %s and %s of a plot of land, and you believe <b>area</b> drives the price. "
        "Your model %s fits poorly. What feature would you add, "
        "and why can the original model not learn this on its own?"
        % (m("frontage"), m("depth"), m("f = w₁·frontage + w₂·depth + b")),
    hint="Write out what the model can and cannot express. Can any choice of w₁ and w₂ ever "
         "produce frontage × depth?",
    steps=[("Area is frontage × depth", "a product of two features"),
           ("The model can only add weighted features — it never multiplies two of them "
            "together", "w₁x₁ + w₂x₂ can never equal x₁x₂"),
           ("So create the feature yourself", "x₃ = frontage × depth"),
           ("New model", "f = w₁x₁ + w₂x₂ + w₃x₃ + b")],
    answer="Add %s. A linear model can only take a weighted <i>sum</i> of "
           "its inputs; it has no way to form a product. If a product matters, you must hand "
           "it to the model." % m("x₃ = frontage × depth"),
    why="This is the whole idea of feature engineering, and it is also why neural networks "
        "matter: they build their own combinations, so you do not have to guess them.")

add("c1w2-p08", level=2, tag="polynomial regression",
    lesson="c1/w2-09-polynomial-regression.html",
    ask="You fit %s with %s ranging from 1 to 1000. What are the ranges of "
        "%s and %s, and what does that force you to do?"
        % (m("f = w₁x + w₂x² + w₃x³ + b"), m("x"), m("x²"), m("x³")),
    steps=[("x ranges 1 to 1000", "range 1000"),
           ("x² ranges 1 to 1,000,000", "range 10⁶"),
           ("x³ ranges 1 to 1,000,000,000", "range 10⁹"),
           ("Their gradients differ by the same factors", "no single α can work")],
    answer="%s and %s. Polynomial features make scaling "
           "<b>mandatory</b>, not optional — without it gradient descent cannot converge on "
           "all three weights at once." % (m("1 to 10⁶"), m("1 to 10⁹")),
    why="Course 1 introduces scaling before polynomials for exactly this reason. The moment "
        "you square a feature you have created a scaling problem.")

add("c1w2-p09", level=2, tag="vectorized gradient",
    lesson="c1/w2-04-gradient-descent-multiple-features.html",
    ask="Write the vectorized gradient computation for linear regression: given %s, "
        "%s, %s and %s, produce %s (shape %s) and %s (a scalar) with no Python loop."
        % (m("X (m, n)"), m("y (m,)"), m("w (n,)"), m("b"), m("dj_dw"), m("(n,)"), m("dj_db")),
    hint="Compute all m errors at once first. Then note that Σ error·x_j over examples is "
         "exactly one matrix–vector product.",
    steps=[("All predictions at once", "f = X @ w + b        → shape (m,)"),
           ("All errors at once", "err = f - y            → shape (m,)"),
           ("For each feature j we need Σ err<sup>(i)</sup> x_j<sup>(i)</sup> — that is column j of X dotted "
            "with err, for every j at once", "X.T @ err          → shape (n,)"),
           ("Divide by m", "dj_dw = (X.T @ err) / m"),
           ("The b gradient is just the mean error", "dj_db = err.mean()")],
    answer=pre("f     = X @ w + b\nerr   = f - y\ndj_dw = (X.T @ err) / m\ndj_db = err.mean()"),
    why="Those four lines replace a double loop over m examples and n features. Check the "
        "shapes as you write them: (m,n)ᵀ @ (m,) → (n,), one gradient per weight.")

add("c1w2-p10", level=3, tag="scaling at prediction time",
    lesson="c1/w2-05-feature-scaling.html",
    ask="You z-score your training features using %s and %s, train, and get good results. "
        "A new house arrives with size 1800. What exactly must you do before predicting, and "
        "what is the classic mistake?" % (m("μ = 1150"), m("σ = 500")),
    steps=[("Scale the new example with the TRAINING μ and σ", "(1800 − 1150) ÷ 500 = 1.3"),
           ("Then predict on the scaled value", "f = w·1.3 + b"),
           ("Classic mistake 1: forgetting to scale at all — the model sees 1800 where it "
            "expects about 1.3", "wildly wrong prediction"),
           ("Classic mistake 2: recomputing μ and σ from the new data",
            "the numbers must be frozen at training time")],
    answer="Compute %s using the training μ and σ, then predict. The mistake is "
           "either not scaling the new point, or re-deriving μ and σ from the test data — "
           "both change the meaning of every weight." % m("(1800 − 1150)/500 = 1.3"),
    why="μ and σ are part of the trained model. Ship them alongside w and b, or the model is "
        "unusable on anything new.")

add("c1w2-p11", level=1, tag="shapes",
    lesson="c1/w2-01-multiple-features.html",
    ask="With %s training examples and %s features, give the shape of "
        "%s, %s, %s, %s and the predictions."
        % (m("m = 500"), m("n = 4"), m("X"), m("y"), m("w"), m("b")),
    steps=[("X: one row per example, one column per feature", "(500, 4)"),
           ("y: one true answer per example", "(500,)"),
           ("w: one weight per feature", "(4,)"),
           ("b: a single number", "scalar, shape ()"),
           ("X @ w + b: (500,4) @ (4,) → (500,)", "(500,)")],
    answer="%s, %s, %s, %s scalar, predictions %s"
           % (m("X: (500,4)"), m("y: (500,)"), m("w: (4,)"), m("b:"), m("(500,)")),
    why="Write these five shapes at the top of every assignment before you write any code. "
        "Most lab errors are a shape you never checked.")

add("c1w2-p12", level=2, tag="normal equation",
    lesson="c1/w2-04-gradient-descent-multiple-features.html",
    ask="Scikit-learn's <code>LinearRegression</code> solves for w and b in one shot with no "
        "learning rate and no iterations. Give two reasons the course still teaches gradient "
        "descent.",
    steps=[("The closed form requires inverting an n×n matrix", "cost grows roughly with n³"),
           ("With 10,000 features that is impractical, and with 10 million examples the "
            "matrix may not fit in memory", "does not scale"),
           ("Second reason: it only exists for linear regression",
            "no closed form for logistic regression or neural networks"),
           ("Gradient descent works on all of them, unchanged", "one algorithm, everywhere")],
    answer="(1) The closed form needs a matrix inverse costing about n³, so it is unusable "
           "with many features. (2) It exists <i>only</i> for linear regression — logistic "
           "regression and every neural network need gradient descent.",
    why="This is why Week 1's loop is worth the effort: it is the one algorithm that carries "
        "you through all three courses unchanged.")

add("c1w2-p13", level=3, tag="diagnosis",
    lesson="c1/w2-06-checking-convergence.html",
    ask="Your cost starts at 5.4, drops to 0.9 in ten iterations, then jumps to 1200 and "
        "then to NaN. Explain the sequence of events precisely, and give the fix.",
    hint="What happens to the gradient when a step overshoots the bottom of a bowl and lands "
         "further up the far side than it started?",
    steps=[("Early steps are on a gentle slope, so α·gradient is a sensible size", "J falls"),
           ("One step overshoots the minimum and lands higher on the opposite wall",
            "J rises to 1200"),
           ("Higher up, the gradient is larger, so the next step is larger still", "runaway"),
           ("Within a few iterations the numbers exceed floating-point range",
            "inf − inf → NaN"),
           ("Fix: reduce α — and scale the features, which is usually the underlying cause",
            "α ÷ 10, then scale")],
    answer="α is too large. Overshooting lands the parameters somewhere steeper, which makes "
           "the next step bigger, which diverges geometrically until the values overflow to "
           "NaN. Reduce α (start with a tenth) and scale the features.",
    why="NaN is almost never a mysterious numerical problem in this course. It is nearly "
        "always divergence, and divergence is nearly always α or unscaled features.")

SET = dict(course="C1", week=2, title="Many features, scaling and curves",
           lede="Week 2 is where the model stops being a line on a page and starts being "
                "matrices with shapes. Most of these problems are shape problems in disguise "
                "— which is exactly what the assignments turn out to be.",
           problems=L)
