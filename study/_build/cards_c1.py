# -*- coding: utf-8 -*-
"""Review cards — Course 1."""
from cardkit import C, deck, blk, steps, bullets, two, hint

W1 = deck("C1", 1, "Introduction to Machine Learning", [
    C("c1w1-model", "formula",
      "The <b>linear regression model</b> — write it out.",
      blk("<var>f</var><sub><var>w</var>,<var>b</var></sub>(<var>x</var>) = <var>wx</var> + <var>b</var>")
      + bullets(["<b>w</b> — the slope (weight): how much y rises per unit of x",
                 "<b>b</b> — the intercept (bias): the prediction when x = 0",
                 "both are <b>learned</b>; x is your data"]),
      "c1/w1-04-linear-regression-model.html"),

    C("c1w1-notation", "concept",
      "What do these three superscripts mean?<br>"
      + blk("<var>x</var><sup>(2)</sup> &nbsp;·&nbsp; <var>x</var><sup>2</sup> &nbsp;·&nbsp; <var>a</var><sup>[2]</sup>"),
      bullets(["<b>x<sup>(2)</sup></b> — round brackets: training <b>example</b> number 2",
               "<b>x<sup>2</sup></b> — plain: x <b>squared</b>",
               "<b>a<sup>[2]</sup></b> — square brackets: <b>layer</b> 2 (Course 2)"])
      + hint("The bracket style carries the meaning. The course is consistent about it."),
      "c1/w1-04-linear-regression-model.html"),

    C("c1w1-cost", "formula",
      "The <b>squared error cost function</b> — write it out.",
      blk("<var>J</var>(<var>w</var>,<var>b</var>) = <span class='fr'><span>1</span><span>2<var>m</var></span></span> "
          "<span class='sum'>Σ</span><sub><var>i</var>=1</sub><sup><var>m</var></sup> "
          "( <var>f</var>(<var>x</var><sup>(<var>i</var>)</sup>) − <var>y</var><sup>(<var>i</var>)</sup> )<sup>2</sup>")
      + bullets(["square → makes errors positive, and punishes big misses disproportionately",
                 "1/m → the average, so J does not grow just because you collected more data",
                 "the 2 → pure convenience; it cancels when you differentiate"]),
      "c1/w1-05-cost-function-formula.html"),

    C("c1w1-cost-shape", "concept",
      "What <b>shape</b> is J(w) for linear regression, and why does the shape matter?",
      "<p>A <b>parabola</b> — and with two parameters, a <b>bowl</b> (convex).</p>"
      + bullets(["it is a sum of squared linear terms, so it is a quadratic",
                 "a convex surface has <b>exactly one</b> minimum",
                 "so gradient descent always finds the global optimum, from any starting point"])
      + hint("You lose this guarantee entirely once you build a neural network."),
      "c1/w1-06-cost-function-intuition.html"),

    C("c1w1-contour", "concept",
      "On a <b>contour plot</b> of J(w, b), what does a single ring represent?",
      "<p>A set of (w, b) pairs that all produce <b>different lines that fit equally badly</b> — same J, "
      "different model.</p>"
      + bullets(["rings close together → steep, J changes fast",
                 "rings far apart → flat",
                 "the bullseye → the best possible w and b",
                 "<b>elongated</b> rings → an awkward valley, cured by feature scaling"]),
      "c1/w1-07-visualizing-the-cost-function.html"),

    C("c1w1-gd-update", "formula",
      "The <b>gradient descent update rule</b> — and the one implementation detail that is easy to get wrong.",
      blk("<var>w</var> := <var>w</var> − <var>α</var> ∂<var>J</var>/∂<var>w</var> &nbsp;&nbsp;&nbsp; "
          "<var>b</var> := <var>b</var> − <var>α</var> ∂<var>J</var>/∂<var>b</var>")
      + "<p><b>Simultaneous update.</b> Compute <em>both</em> derivatives from the old values first, "
        "<em>then</em> assign both.</p>"
      + hint("The sequential version still often reduces J — which is exactly why the bug is hard to spot."),
      "c1/w1-09-implementing-gradient-descent.html"),

    C("c1w1-gd-sign", "concept",
      "Why does <b>subtracting</b> the derivative always move you towards the minimum?",
      bullets(["positive slope → uphill is to the right → subtracting moves w <b>left</b> ✓",
               "negative slope → uphill is to the left → subtracting a negative moves w <b>right</b> ✓",
               "at the minimum the slope is 0, so nothing moves — it stops on its own"])
      + hint("And the steps shrink automatically near the bottom, because the slope shrinks. "
             "You never need to reduce α by hand."),
      "c1/w1-10-gradient-descent-intuition.html"),

    C("c1w1-alpha", "concept",
      "What are the <b>four regimes</b> of the learning rate α?",
      bullets(["<b>far too small</b> — converges, glacially",
               "<b>about right</b> — falls fast, then flattens",
               "<b>too large</b> — overshoots, J oscillates",
               "<b>far too large</b> — diverges; J grows, then <code>NaN</code>"])
      + hint("<b>If J ever increases between iterations, α is too large.</b> The single most useful "
             "debugging rule in the specialization."),
      "c1/w1-11-learning-rate.html"),

    C("c1w1-alpha-debug", "trap",
      "Your model will not learn. How do you tell whether it is <b>α</b> or a <b>bug</b>?",
      "<p>Set α absurdly small — <code>0.0001</code>.</p>"
      + bullets(["J now decreases → the gradient is fine, α was too large",
                 "J still does not decrease → it is <b>not</b> α. There is a bug, usually a sign error "
                 "or a wrong index in the gradient"])
      + hint("With a small enough step, J is mathematically <em>guaranteed</em> to fall — if the gradient "
             "is correct."),
      "c1/w1-11-learning-rate.html"),

    C("c1w1-derivatives", "formula",
      "The two <b>derivatives</b> for linear regression.",
      blk("∂<var>J</var>/∂<var>w</var> = <span class='fr'><span>1</span><span><var>m</var></span></span> "
          "<span class='sum'>Σ</span> ( <var>f</var>(<var>x</var><sup>(<var>i</var>)</sup>) − <var>y</var><sup>(<var>i</var>)</sup> ) "
          "<b>· <var>x</var><sup>(<var>i</var>)</sup></b>")
      + blk("∂<var>J</var>/∂<var>b</var> = <span class='fr'><span>1</span><span><var>m</var></span></span> "
            "<span class='sum'>Σ</span> ( <var>f</var>(<var>x</var><sup>(<var>i</var>)</sup>) − <var>y</var><sup>(<var>i</var>)</sup> )")
      + "<p>The only difference is the <b>· x<sup>(i)</sup></b> on the w version — because an example with "
        "a large x is more sensitive to a change in w.</p>"
      + hint("This is where the 2 in 1/2m goes: differentiating the square brings down a 2 that cancels it."),
      "c1/w1-12-gradient-descent-for-linear-regression.html"),

    C("c1w1-batch", "concept",
      "What does <b>“batch”</b> gradient descent mean, and what are the alternatives?",
      bullets(["<b>batch</b> — every update uses all m examples (what Course 1 uses)",
               "<b>stochastic</b> — one example per update; noisy, many more steps per second",
               "<b>mini-batch</b> — a subset (32–512); the practical compromise, used by all deep learning"])
      + hint("The name “batch” is why the compromise is called <em>mini</em>-batch."),
      "c1/w1-13-running-gradient-descent.html"),

    C("c1w1-three-parts", "concept",
      "What are the <b>three parts</b> that every algorithm in this specialization is built from?",
      steps(["a <b>model</b> — what f(x) is allowed to look like",
             "a <b>cost function</b> — one number saying how wrong it is",
             "an <b>optimiser</b> — gradient descent, which makes that number smaller"])
      + hint("Course 2 makes the model a neural network. Course 3 changes the cost. The structure never "
             "changes."),
      "c1/w1-13-running-gradient-descent.html"),
    C("c1w1-drill-cost", "drill",
      "x = [1, 2], y = [300, 500], w = 100, b = 100. Compute J(w, b).",
      blk("f(1) = 200, f(2) = 300 &nbsp;&rarr;&nbsp; errors −100, −200")
      + blk("J = <span class='fr'><span>1</span><span>2(2)</span></span> ( 100² + 200² ) = "
            "<span class='fr'><span>1</span><span>4</span></span> (50,000) = <b>12,500</b>")
      + hint("The perfect fit (w=200, b=100) gives J=0 exactly — this is what \u201calmost right\u201d costs."),
      "c1/w1-05-cost-function-formula.html"),
])

W2 = deck("C1", 2, "Regression with Multiple Variables", [
    C("c1w2-multi-model", "formula",
      "The model with <b>n features</b>, in both forms.",
      blk("<var>f</var>(<var>x</var>) = <var>w</var><sub>1</sub><var>x</var><sub>1</sub> + <var>w</var><sub>2</sub><var>x</var><sub>2</sub> + … + <var>w<sub>n</sub>x<sub>n</sub></var> + <var>b</var>")
      + blk("<var>f</var>(<var>x</var>) = <b>w⃗ · x⃗</b> + <var>b</var>", "vectorised")
      + hint("n = number of features. m = number of examples. Keep them straight."),
      "c1/w2-01-multiple-features.html"),

    C("c1w2-subscripts", "concept",
      "What is <b>x<sub>2</sub><sup>(3)</sup></b>?",
      "<p>Feature <b>2</b> of training example <b>3</b> — one single number.</p>"
      + bullets(["<b>subscript</b> = which feature (which column)",
                 "<b>superscript in round brackets</b> = which example (which row)"]),
      "c1/w2-01-multiple-features.html"),

    C("c1w2-dot-vs-star", "trap",
      "In NumPy, what is the difference between <code>w * x</code> and <code>np.dot(w, x)</code>?",
      two("<code>[10, 40, 90]</code><br>elementwise — returns an <b>array</b>",
          "<code>140</code><br>multiplies <b>and sums</b> — returns a <b>number</b>",
          "w * x → ", "np.dot(w, x) → ")
      + hint("A neuron needs the number. Also: a Python <em>list</em> times 2 repeats it; a NumPy "
             "<em>array</em> times 2 doubles it. No error either way."),
      "c1/w2-02-vectorization.html"),

    C("c1w2-why-fast", "concept",
      "Why is <code>np.dot</code> faster than a for loop? (not “because NumPy is clever maths”)",
      bullets(["the loop pays <b>Python interpreter overhead per element</b>",
               "np.dot hands a contiguous block to <b>compiled</b> library code (BLAS)",
               "which uses <b>SIMD</b> — one instruction multiplying several pairs at once",
               "and often multiple cores"])
      + hint("Same maths, same answer, 10–100× the speed. This is also why GPUs matter."),
      "c1/w2-03-why-vectorization-is-fast.html"),

    C("c1w2-scaling-why", "concept",
      "Why does <b>feature scaling</b> speed up gradient descent?",
      "<p>Wildly different feature ranges make the cost bowl a <b>long thin canyon</b>.</p>"
      + bullets(["the step is perpendicular to the contour, which in a canyon points <b>across</b> the "
                 "valley, not along it → zig-zagging",
                 "and you must keep α small to stop it bouncing out, making the crawl slower still",
                 "scaled → near-circular contours → a direct path, and a much larger α is safe"])
      + hint("Both effects pull the same way, which is why the speedup is often an order of magnitude."),
      "c1/w2-05-feature-scaling.html"),

    C("c1w2-scaling-how", "formula",
      "The three <b>feature scaling</b> methods.",
      bullets(["<b>divide by max:</b> x := x / max &nbsp;→ 0…1",
               "<b>mean normalisation:</b> x := (x − μ) / (max − min) &nbsp;→ ≈ −0.5…0.5",
               "<b>z-score:</b> x := (x − μ) / σ &nbsp;→ mean 0, sd 1 &nbsp;<b>(the usual choice)</b>"])
      + hint("Aim for roughly −1…1. Andrew's rules of thumb: −3…3 fine, −0.3…0.3 fine. "
             "0…0.001 or −100…100 needs rescaling."),
      "c1/w2-05-feature-scaling.html"),

    C("c1w2-scaling-trap", "trap",
      "What are the two classic <b>feature scaling</b> mistakes?",
      bullets(["<b>Computing μ and σ on the whole dataset</b> before splitting — leaks test information "
               "into training",
               "<b>Forgetting to scale at prediction time</b> — the model was trained on standardised "
               "inputs; feeding it a raw 2000 gives nonsense"])
      + hint("Fit the scaler on <b>train only</b>, then apply those same numbers everywhere. "
             "<code>sklearn.pipeline.Pipeline</code> exists to stop you forgetting."),
      "c1/w2-05-feature-scaling.html"),

    C("c1w2-convergence", "concept",
      "You plot J against iterations. What do the four shapes mean?",
      bullets(["<b>falls, then flattens</b> → healthy and converged; stop",
               "<b>falls, still falling</b> → healthy; run longer",
               "<b>oscillates</b> → α too large; reduce it",
               "<b>increases steadily</b> → α far too large, or a bug"])
      + hint("Three lines of matplotlib, and the cheapest diagnostic in machine learning."),
      "c1/w2-06-checking-convergence.html"),

    C("c1w2-alpha-ladder", "concept",
      "How do you <b>choose α</b> in practice?",
      steps(["try a ladder roughly ×3 apart: 0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1",
             "plot J against iterations for each",
             "keep the <b>largest</b> α that still decreases smoothly",
             "optionally back off one notch for safety"])
      + hint("×3 rather than +0.1 because α acts multiplicatively — equal ratios matter, not equal "
             "differences."),
      "c1/w2-07-choosing-the-learning-rate.html"),

    C("c1w2-feateng", "concept",
      "Why can a linear model not learn that <b>area = frontage × depth</b> matters?",
      "<p>Because its formula is a <b>weighted sum</b>: w₁x₁ + w₂x₂ + b. There is no choice of w₁ and w₂ "
      "that produces a <em>product</em>. It is outside what the model can represent.</p>"
      + "<p>So you compute x₃ = x₁ × x₂ yourself and hand it over. That is <b>feature engineering</b>, and "
        "it is where domain knowledge enters an ML system.</p>"
      + hint("Products, ratios, differences, logs. Neural networks reduce the need for this — they do not "
             "remove it."),
      "c1/w2-08-feature-engineering.html"),

    C("c1w2-polyreg", "concept",
      "Why is <b>polynomial regression</b> still called <em>linear</em> regression?",
      "<p>Because “linear” refers to being linear in the <b>parameters w</b>, not in x.</p>"
      + "<p>f = w₁x + w₂x² + w₃x³ + b is a weighted sum of features. That the features happen to be powers "
        "of x changes nothing about the algorithm.</p>"
      + hint("But it makes feature scaling <b>mandatory</b>: if x is 1–1000 then x³ is 1–10⁹."),
      "c1/w2-09-polynomial-regression.html"),
    C("c1w2-drill-zscore", "drill",
      "A feature has &mu; = 218.67, &sigma; = 39.96. A house has x = 200. What is its z-score?",
      blk("<var>z</var> = (200 − 218.67) / 39.96 = −18.67 / 39.96 = <b>−0.47</b>")
      + hint("Negative means below average — this house is a bit smaller than typical, by about half a "
             "standard deviation."),
      "c1/w2-05-feature-scaling.html"),
])

W3 = deck("C1", 3, "Classification", [
    C("c1w3-why-not-linreg", "concept",
      "Two reasons <b>linear regression fails</b> at classification.",
      steps(["<b>Unbounded output.</b> It will predict −0.4 or 1.8, which cannot be read as a class or a "
             "probability.",
             "<b>Outliers move the boundary.</b> Squared error punishes the line for being far from a "
             "point — even one that is unambiguously in its class. So a clear-cut example drags the "
             "decision boundary."])
      + hint("The second is the deeper one. In classification, an obvious example should barely influence "
             "the boundary; squared error makes it influence it <em>most</em>."),
      "c1/w3-01-motivations.html"),

    C("c1w3-sigmoid", "formula",
      "The <b>sigmoid</b>, and the logistic regression model.",
      blk("<var>g</var>(<var>z</var>) = <span class='fr'><span>1</span><span>1 + <var>e</var><sup>−<var>z</var></sup></span></span>")
      + blk("<var>z</var> = <b>w⃗·x⃗</b> + <var>b</var> &nbsp;→&nbsp; <var>f</var>(<var>x</var>) = <var>g</var>(<var>z</var>)")
      + bullets(["always strictly between 0 and 1 — never reaches either",
                 "<b>g(0) = 0.5</b>, because e⁰ = 1",
                 "read the output as <b>P(y = 1 | x; w, b)</b>"]),
      "c1/w3-02-logistic-regression.html"),

    C("c1w3-sigmoid-values", "number",
      "Sigmoid values worth knowing: g(−5), g(−2), g(0), g(2), g(5)?",
      bullets(["g(−5) ≈ <b>0.007</b>", "g(−2) ≈ <b>0.12</b>", "g(0) = <b>0.50</b>",
               "g(2) ≈ <b>0.88</b>", "g(5) ≈ <b>0.993</b>"])
      + hint("Past about ±5 the sigmoid has saturated — extra distance changes almost nothing. That is "
             "exactly why outliers stop dragging the boundary."),
      "c1/w3-02-logistic-regression.html"),

    C("c1w3-boundary", "concept",
      "Where is the <b>decision boundary</b>, and what determines its shape?",
      "<p>Wherever <b>z = 0</b> — because g(0) = 0.5 exactly.</p>"
      + blk("<var>f</var> ≥ 0.5 &nbsp;↔&nbsp; <var>z</var> ≥ 0 &nbsp;↔&nbsp; <b>w⃗·x⃗</b> + <var>b</var> ≥ 0")
      + "<p>The shape is a property of the <b>features you supply</b>, not of logistic regression. "
        "x₁, x₂ → a straight line. x₁², x₂² → a circle.</p>"
      + hint("The model is always linear in z. A curved boundary does not make it a non-linear model."),
      "c1/w3-03-decision-boundary.html"),

    C("c1w3-why-not-sq-error", "concept",
      "Why can't logistic regression use <b>squared error</b>?",
      "<p>Because f now has a <b>sigmoid inside it</b>. Squaring the error of a squashed function produces "
      "a <b>non-convex</b> surface — many local minima instead of one bowl.</p>"
      + hint("There is a second reason too: the gradient would pick up a g′(z) factor that is near zero "
             "exactly where the model is confidently wrong — learning stalls where it is needed most."),
      "c1/w3-04-cost-function-for-logistic-regression.html"),

    C("c1w3-logloss", "formula",
      "The <b>logistic loss</b> — both the two-case and the one-line form.",
      blk("<var>L</var> = −log(<var>f</var>) &nbsp;if <var>y</var> = 1 &nbsp;·&nbsp; "
          "−log(1 − <var>f</var>) &nbsp;if <var>y</var> = 0")
      + blk("<var>L</var>(<var>f</var>, <var>y</var>) = <b>−<var>y</var> log(<var>f</var>) − (1 − <var>y</var>) log(1 − <var>f</var>)</b>",
            "the combined version")
      + "<p>Since y is only ever 0 or 1, one term is always multiplied by zero and disappears.</p>"
      + hint("This is <b>binary cross-entropy</b>. You will use it for every binary classifier in Course 2 "
             "and Course 3."),
      "c1/w3-06-simplified-cost-function.html"),

    C("c1w3-logloss-shape", "concept",
      "What does the logistic loss do to a <b>confidently wrong</b> prediction?",
      "<p>The penalty goes to <b>infinity</b>.</p>"
      + bullets(["y = 1, f = 0.99 → loss <b>0.01</b> — confident and right, essentially free",
                 "y = 1, f = 0.5 → loss <b>0.69</b> — hedging, moderate cost",
                 "y = 1, f = 0.01 → loss <b>4.61</b> — confidently wrong, very expensive"])
      + hint("−log(0.5) = 0.693 is the coin-flip reference point. A model averaging below it is beating "
             "guesswork."),
      "c1/w3-05-logistic-loss.html"),

    C("c1w3-why-log", "concept",
      "Why a <b>logarithm</b> in the loss? Two reasons.",
      bullets(["it makes the overall cost <b>convex</b>, so gradient descent gets its guarantee back",
               "it is the <b>negative log-likelihood</b> — the w and b that make the observed data most "
               "probable"])
      + hint("It is not an arbitrary trick; it falls out of statistics. And the sigmoid + log loss are a "
             "<em>matched pair</em> — the tidiness disappears if you mix and match."),
      "c1/w3-04-cost-function-for-logistic-regression.html"),

    C("c1w3-gd-logistic", "formula",
      "The gradient descent update for <b>logistic</b> regression.",
      blk("<var>w<sub>j</sub></var> := <var>w<sub>j</sub></var> − <var>α</var> "
          "<span class='fr'><span>1</span><span><var>m</var></span></span> <span class='sum'>Σ</span> "
          "( <var>f</var>(<var>x</var><sup>(<var>i</var>)</sup>) − <var>y</var><sup>(<var>i</var>)</sup> ) <var>x<sub>j</sub></var><sup>(<var>i</var>)</sup>")
      + "<p><b>Character-for-character identical</b> to linear regression. The only difference is what f "
        "means: <code>g(w·x + b)</code> instead of <code>w·x + b</code>.</p>"
      + hint("Not a coincidence — g′(z) = g(z)(1−g(z)) cancels exactly against the 1/f from the logarithm."),
      "c1/w3-07-gradient-descent-logistic.html"),

    C("c1w3-overfit", "distinguish",
      "<b>Underfitting</b> vs <b>overfitting</b> — the names, the symptoms, the fixes.",
      two(bullets(["also called <b>high bias</b>", "poor on training data", "poor on new data",
                   "the model is too simple"]),
          bullets(["also called <b>high variance</b>", "<b>excellent</b> on training data",
                   "poor on new data", "the model is too flexible"]),
          "Underfitting", "Overfitting")
      + hint("Both look like “the model is bad”, and they need <b>opposite</b> fixes. That is why naming "
             "them matters."),
      "c1/w3-08-the-problem-of-overfitting.html"),

    C("c1w3-address-overfit", "concept",
      "Three ways to <b>address overfitting</b>, and why the third is usually first.",
      steps(["<b>more data</b> — the best fix, and often impossible",
             "<b>fewer features</b> — you may throw away one that mattered",
             "<b>regularisation</b> — keep every feature, shrink the weights"])
      + hint("Regularisation beats feature selection because it does not force a binary choice: a feature "
             "that matters a little keeps a small weight."),
      "c1/w3-09-addressing-overfitting.html"),

    C("c1w3-regcost", "formula",
      "The <b>regularised cost function</b>.",
      blk("<var>J</var> = <span class='fr'><span>1</span><span>2<var>m</var></span></span> <span class='sum'>Σ</span>( <var>f</var> − <var>y</var> )<sup>2</sup> "
          "+ <span class='fr'><span><var>λ</var></span><span>2<var>m</var></span></span> "
          "<span class='sum'>Σ</span><sub><var>j</var>=1</sub><sup><var>n</var></sup> <var>w<sub>j</sub></var><sup>2</sup>")
      + bullets(["first term: <b>fit the data</b>. second term: <b>keep the weights small</b>",
                 "λ = 0 → no penalty, overfits. λ enormous → all w ≈ 0, f ≈ b, underfits",
                 "the sum starts at <b>j = 1</b> — <b>b is not regularised</b>"])
      + hint("Shrinking b only slides the curve up and down; it does nothing about wiggliness."),
      "c1/w3-10-cost-function-with-regularization.html"),

    C("c1w3-weight-decay", "formula",
      "Rearrange the regularised update rule. What is the resulting name?",
      blk("<var>w<sub>j</sub></var> := <b>(1 − <var>αλ</var>/<var>m</var>)</b> <var>w<sub>j</sub></var> "
          "− <var>α</var> <span class='fr'><span>1</span><span><var>m</var></span></span> <span class='sum'>Σ</span>( <var>f</var> − <var>y</var> )<var>x<sub>j</sub></var>")
      + "<p><b>Weight decay.</b> Every iteration multiplies w by a number just below 1 <em>before</em> "
        "taking the ordinary step.</p>"
      + hint("This is the <code>weight_decay</code> argument in every modern optimiser — AdamW, "
             "<code>kernel_regularizer=l2(0.01)</code>, all of it."),
      "c1/w3-11-regularized-gradient-descent.html"),
    C("c1w3-drill-sigmoid", "drill",
      "w = 1, b = 0, x = 1.5. Compute z, then g(z).",
      blk("<var>z</var> = 1(1.5) + 0 = 1.5")
      + blk("<var>g</var>(1.5) = 1 / (1 + <var>e</var><sup>−1.5</sup>) = 1 / (1 + 0.223) = <b>0.818</b>")
      + hint("Above 0.5, so this example is classified y&#770; = 1 — and fairly confidently."),
      "c1/w3-02-logistic-regression.html"),
])

DECKS = [W1, W2, W3]
