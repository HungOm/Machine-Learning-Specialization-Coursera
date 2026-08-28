# -*- coding: utf-8 -*-
"""Review cards — Foundations."""
from cardkit import C, deck, blk, steps, bullets, two, hint

W1 = deck("F0", 1, "The Maths You Actually Need", [
    C("f0-function", "concept",
      "What does <b>f(3)</b> mean — and what does it definitely <em>not</em> mean?",
      "<p>“Put 3 into the machine called f.” It is <b>not</b> f multiplied by 3.</p>"
      + "<p>A function is a rule where the same input always gives the same output.</p>"
      + hint("A model <em>is</em> a function. Training does not change the function — it changes numbers "
             "inside it, which is what the subscript in f<sub>w,b</sub>(x) is telling you."),
      "f0/w1-01-what-is-a-function.html"),

    C("f0-superscripts", "trap",
      "Three superscripts: <b>x<sup>(2)</sup></b> · <b>x<sup>2</sup></b> · <b>a<sup>[2]</sup></b>. "
      "What does each mean?",
      bullets(["<b>x<sup>(2)</sup></b> — round brackets: training <b>example</b> 2",
               "<b>x<sup>2</sup></b> — nothing: x <b>squared</b>",
               "<b>a<sup>[2]</sup></b> — square brackets: <b>layer</b> 2"])
      + hint("The bracket style carries the meaning, and the courses are consistent about it. Reading "
             "a<sup>[2]</sup> as “a squared” is the most common notation error in Course 2."),
      "f0/w1-01-what-is-a-function.html"),

    C("f0-slope", "formula",
      "<b>Slope</b> — the formula, and the two letters it goes by.",
      blk("slope = <span class='fr'><span>rise</span><span>run</span></span> = "
          "<span class='fr'><span>change in y</span><span>change in x</span></span>")
      + "<p>Written <b>m</b> in school maths, <b>w</b> in machine learning. Same thing.</p>"
      + hint("“If I step 1 to the right, how far up do I go?” Positive = uphill, negative = downhill, "
             "zero = flat."),
      "f0/w1-04-slope.html"),

    C("f0-derivative", "concept",
      "What <b>is</b> a derivative, and what are the only three things you need to know about it?",
      "<p>The <b>slope of a curve at one exact point</b> — found by taking two points very close together "
      "and shrinking the gap to nothing.</p>"
      + bullets(["it is a <b>slope</b>", "its <b>sign</b> says which way is uphill",
                 "its <b>size</b> says how steep"])
      + blk("<var>f</var>′(<var>x</var>) = lim<sub><var>h</var>→0</sub> "
            "<span class='fr'><span><var>f</var>(<var>x</var>+<var>h</var>) − <var>f</var>(<var>x</var>)</span><span><var>h</var></span></span>")
      + hint("You never need to differentiate by hand in this specialization. TensorFlow does it."),
      "f0/w1-05-derivatives.html"),

    C("f0-partial", "concept",
      "What is a <b>partial derivative</b>, and what does the curly ∂ tell you?",
      "<p><b>Freeze every variable except one</b>, and a hill becomes an ordinary curve whose slope you "
      "already know how to find.</p>"
      + "<p>The curly ∂ (rather than a straight d) is purely a notice that other variables exist and are "
        "being held still.</p>"
      + hint("Collect all the partials into one list and you have the <b>gradient</b>, ∇J — which points "
             "straight uphill. That is why gradient descent subtracts it."),
      "f0/w1-06-partial-derivatives.html"),

    C("f0-sigma", "formula",
      "<b>Σ</b> — what is it, and how do you read it out loud?",
      blk("<span class='sum'>Σ</span><sub><var>i</var>=1</sub><sup><var>m</var></sup> <var>x<sub>i</sub></var>")
      + "<p>A <b>for loop</b>. Counter underneath, stop on top, thing-to-add beside it.</p>"
      + bullets(["read as: “now do this for every training example, and add up the results”",
                 "in code: <code>np.sum(x)</code>"])
      + hint("Σ(x²) squares each then adds. (Σx)² adds then squares. For [1,2] those are 5 and 9."),
      "f0/w1-07-sigma-notation.html"),

    C("f0-pi", "formula",
      "<b>Π</b> — what does it mean, and why does code usually avoid it?",
      "<p>Capital pi: <b>multiply them all together</b>. (Nothing to do with 3.14159 — that is lowercase π.)</p>"
      + blk("log(<var>a</var> × <var>b</var>) = log(<var>a</var>) + log(<var>b</var>)")
      + "<p>Multiplying many numbers below 1 underflows to exactly zero, so code computes "
        "<code>np.sum(np.log(p))</code> instead.</p>"
      + hint("The shrinking is the <em>point</em> in anomaly detection: five mild oddities multiply into "
             "one genuinely rare event."),
      "f0/w1-08-pi-notation.html"),

    C("f0-vector-length", "formula",
      "What is a <b>vector</b>, and how do you find its length?",
      "<p>A list of numbers in order. In ML, almost always <b>one row of your spreadsheet</b>.</p>"
      + blk("‖<var>x⃗</var>‖ = √<span class='sqrt'><var>x</var><sub>1</sub><sup>2</sup> + <var>x</var><sub>2</sub><sup>2</sup> + …</span>")
      + "<p><code>np.linalg.norm(x)</code>. For [3, 4] it is √(9+16) = <b>5</b>.</p>"
      + hint("Double bars ‖x‖ for a vector's length; single bars |x| for one number's absolute value."),
      "f0/w1-09-vectors.html"),

    C("f0-dot", "formula",
      "The <b>dot product</b> — both formulas, and what the answer means.",
      blk("<var>a⃗</var> · <var>b⃗</var> = <span class='sum'>Σ</span> <var>a<sub>i</sub>b<sub>i</sub></var> "
          "= ‖<var>a⃗</var>‖‖<var>b⃗</var>‖ cos <var>θ</var>")
      + bullets(["multiply the pairs, add them up → <b>one number</b>",
                 "positive = pointing the same way · zero = at right angles · negative = opposed"])
      + hint("<code>a @ b</code>, not <code>a * b</code>. The star keeps them separate; the @ collapses "
             "them. A neuron needs the collapse."),
      "f0/w1-10-dot-product.html"),

    C("f0-shape-rule", "formula",
      "The <b>matrix multiplication shape rule</b>, and the trick for checking it in your head.",
      blk("(<var>m</var> × <b><var>n</var></b>) × (<b><var>n</var></b> × <var>p</var>) = (<var>m</var> × <var>p</var>)")
      + "<p>Write the shapes side by side. <b>Middles match → legal. The answer is the outer two.</b></p>"
      + hint("The inner number gets summed away and never appears in the result. And A@B ≠ B@A — usually "
             "one of them is not even defined."),
      "f0/w1-12-matrix-multiplication.html"),

    C("f0-transpose", "concept",
      "What does <b>transpose</b> do, and why do you keep needing it?",
      "<p>Swaps rows and columns. (2,3) becomes (3,2). The numbers do not change — only where they sit.</p>"
      + "<p>You need it for one boring reason: <b>making two shapes line up</b> so a multiplication is "
        "defined.</p>"
      + hint("<code>M.T</code>. And it is <b>not</b> reshape — both can give (3,2) from a (2,3), and the "
             "numbers land in different places."),
      "f0/w1-13-transpose.html"),

    C("f0-exp", "concept",
      "Two facts about <b>e<sup>z</sup></b> that explain why it is everywhere in this specialization.",
      bullets(["it is <b>always positive</b>, whatever z is → which is why softmax uses it",
               "it <b>grows very fast</b>, turning differences in scores into ratios in probability"])
      + "<p>e ≈ 2.718. <code>np.exp(z)</code>. e<sup>0</sup> = 1, always.</p>"
      + hint("Why e and not 10? Because the derivative of e<sup>x</sup> is e<sup>x</sup> itself — which "
             "makes every derivative in the course come out clean."),
      "f0/w1-14-exponentials.html"),

    C("f0-log", "concept",
      "The two jobs <b>logarithms</b> do in machine learning.",
      steps(["<b>turn tiny into huge</b> — −log(0.001) = 6.9, which makes cross-entropy a usable loss",
             "<b>turn multiplying into adding</b> — log(a×b) = log(a) + log(b), which stops products of "
             "many probabilities underflowing to zero"])
      + "<p><code>np.log</code> is base e (the ML default). <code>np.log2</code> for entropy.</p>"
      + hint("−log(1) = 0, so a confident correct answer costs nothing. −log(0) = ∞, so a confident wrong "
             "one costs everything. That asymmetry is the whole design."),
      "f0/w1-15-logarithms.html"),

    C("f0-prob-rules", "formula",
      "The four <b>probability</b> rules, and the one that powers anomaly detection.",
      bullets(["always between <b>0</b> and <b>1</b>",
               "P(not A) = <b>1 − P(A)</b>",
               "<b>AND</b> of independent things → <b>multiply</b>",
               "<b>OR</b> of exclusive things → <b>add</b>"])
      + "<p>P(y=1 <b>|</b> x) — the bar means “<b>given</b>”.</p>"
      + hint("The multiplying rule is why five mild oddities become one rare event — the engine behind "
             "anomaly detection."),
      "f0/w1-16-probability.html"),

    C("f0-variance", "algorithm",
      "How do you compute a <b>standard deviation</b> — and why is there a squaring step?",
      steps(["find the <b>mean</b> μ",
             "find each value's <b>deviation</b> from μ",
             "<b>square</b> them",
             "average those squares → the <b>variance</b> σ²",
             "square root → the <b>standard deviation</b> σ"])
      + "<p>Squaring is necessary because the raw deviations <b>always add to exactly zero</b> — the ones "
        "above the mean cancel the ones below.</p>"
      + hint("<code>x.mean()</code>, <code>x.var()</code>, <code>x.std()</code>. The square root at the "
             "end puts the answer back into the original units."),
      "f0/w1-17-mean-variance.html"),

    C("f0-normal", "number",
      "The <b>bell curve</b>: what fraction lies within 1, 2 and 3 standard deviations?",
      bullets(["μ ± 1σ → <b>68%</b>", "μ ± 2σ → <b>95%</b>", "μ ± 3σ → <b>99.7%</b>",
               "beyond ± 4σ → about 1 in 15,000"])
      + "<p>Two numbers describe the whole curve: <b>μ</b> (where the top is) and <b>σ</b> (how wide).</p>"
      + hint("p(x) is a <b>density</b>, not a probability — it can exceed 1 when σ is small. Only the "
             "<em>area</em> is a probability, and it totals 1."),
      "f0/w1-18-normal-distribution.html"),

    C("f0-argmax", "distinguish",
      "<b>max</b> vs <b>argmax</b> — and where you meet the difference.",
      two("the biggest <b>value</b><br>x = [12, 31, 7] → <b>31</b>",
          "the <b>position</b> of the biggest<br>x = [12, 31, 7] → <b>1</b>",
          "max", "argmax")
      + "<p>“arg” means “the input that does it”. So argmax<sub>a</sub> Q(s,a) is <b>the action</b>, not "
        "the score.</p>"
      + hint("Classification uses <code>np.argmax(probs, axis=1)</code>; K-means uses argmin over "
             "distances; RL policies are argmax over actions."),
      "f0/w1-19-min-max-argmax.html"),
    C("f0-drill-dotprod", "drill",
      "Compute the dot product: <b>a</b> = [1, 2, 3], <b>b</b> = [4, 5, 6].",
      blk("<var>a</var>·<var>b</var> = 1(4) + 2(5) + 3(6) = 4 + 10 + 18 = <b>32</b>")
      + hint("Pair up, multiply, add. Same recipe for a vector of 3 numbers or 3 million."),
      "f0/w1-10-dot-product.html"),
])

W2 = deck("F0", 2, "Python, NumPy and pandas", [
    C("f0-list-vs-array", "trap",
      "<code>x * 2</code> — what happens if x is a <b>list</b>, and if x is a <b>NumPy array</b>?",
      two("<code>[1,2,3,1,2,3]</code><br>repeats the list", "<code>[2,4,6]</code><br>doubles each number",
          "list", "array")
      + "<p>No error either way. <b>Always <code>np.array(my_list)</code> before doing maths.</b></p>"
      + hint("The difference is memory: a list holds pointers to objects of any type; an array holds raw "
             "numbers of one type in a solid block. That layout is where the speed comes from."),
      "f0/w2-03-lists-vs-arrays.html"),

    C("f0-slicing", "formula",
      "<code>x[1:4]</code> — which elements, and what is the rule everyone gets wrong?",
      "<p>Positions <b>1, 2, 3</b>. It <b>stops before 4</b>.</p>"
      + bullets(["<code>x[0]</code> first · <code>x[-1]</code> last",
                 "<code>x[:3]</code> from the start · <code>x[3:]</code> to the end",
                 "<code>M[:, 2]</code> — all rows, column 2"])
      + hint("Handy consequence: the number you get is just (end − start). And a slice is a <b>view</b>, "
             "not a copy — changing it changes the original."),
      "f0/w2-04-indexing-slicing.html"),

    C("f0-axis", "concept",
      "<code>axis=0</code> vs <code>axis=1</code> — and the rule that makes it permanent.",
      "<p><b>The axis you name is the one that disappears.</b></p>"
      + bullets(["(3,4) with <code>axis=0</code> → <b>(4,)</b> — one answer per <b>column</b>",
                 "(3,4) with <code>axis=1</code> → <b>(3,)</b> — one answer per <b>row</b>"])
      + "<p>One statistic per <b>feature</b> → axis=0. One prediction per <b>example</b> → axis=1.</p>"
      + hint("Do not guess it — work out which number in the shape you want gone. That is your axis."),
      "f0/w2-05-shape-and-axis.html"),

    C("f0-broadcast", "formula",
      "The <b>broadcasting</b> rule, and the silent bug it causes.",
      "<p>Line the shapes up <b>from the right</b>. Compatible if <b>equal</b>, or if <b>one is 1</b>.</p>"
      + bullets(["(1000,4) + (4,) → (1000,4) ✓ — how a bias row is added to every example",
                 "(3,1) + (1,3) → <b>(3,3)</b> ⚠ — both stretch. Nine numbers where you wanted three, "
                 "and <b>no error</b>"])
      + hint("When a result has a surprising shape, broadcasting is almost always what happened. "
             "Print the shapes of both operands."),
      "f0/w2-08-broadcasting.html"),

    C("f0-star-vs-at", "trap",
      "<code>a * b</code> vs <code>a @ b</code> — what is the difference, and why is it dangerous?",
      two("elementwise<br>[1,2,3]*[4,5,6] = <b>[4,10,18]</b><br>same length out",
          "dot / matrix multiply<br>[1,2,3]@[4,5,6] = <b>32</b><br>collapses to one number",
          "*", "@")
      + "<p>On two square matrices <b>both run</b> and give the same shape. Only one is right, and nothing "
        "warns you.</p>"
      + hint("Prefer <code>@</code> over <code>np.dot</code> — np.dot behaves differently once you go past "
             "2 dimensions."),
      "f0/w2-09-dot-in-code.html"),

    C("f0-mask", "code",
      "What does <code>(preds == y).mean()</code> compute, and why does it work?",
      "<p><b>Accuracy.</b></p>"
      + steps(["the comparison gives an array of True/False — a <b>mask</b>",
               "True counts as 1 and False as 0",
               "so the mean of that array is the <b>fraction that are True</b>"])
      + hint("Use <code>&amp;</code> and <code>|</code> (not <code>and</code>/<code>or</code>) to combine "
             "masks, and give each condition its own brackets."),
      "f0/w2-11-boolean-masks.html"),

    C("f0-reshape", "distinguish",
      "<code>reshape(3,2)</code> vs <code>.T</code> on a (2,3) array — same shape, same result?",
      "<p><b>Same shape, different numbers.</b> From [[1,2,3],[4,5,6]]:</p>"
      + two("[[1,2],[3,4],[5,6]]<br>re-cuts the same sequence",
            "[[1,4],[2,5],[3,6]]<br>mirrors the positions",
            "reshape(3,2)", ".T")
      + hint("<code>reshape(1,-1)</code> is the fix when a library insists on 2-D. And <code>.T</code> "
             "does nothing at all to a 1-D array."),
      "f0/w2-12-reshape.html"),

    C("f0-pandas-five", "code",
      "The <b>five pandas calls</b> to run on every new dataset, before modelling anything.",
      bullets(["<code>df.head()</code> — look at it",
               "<code>df.shape</code> — how much is there",
               "<code>df.info()</code> — types, and <b>missing values</b>",
               "<code>df.describe()</code> — the scale of each feature",
               "<code>df.columns</code> — the exact spelling of the names"])
      + hint("<code>info()</code> catches the classic bug: a numeric column that arrived as text because "
             "of one stray “N/A”."),
      "f0/w2-13-pandas-dataframes.html"),

    C("f0-to-numpy", "code",
      "How do you get <b>X</b> and <b>y</b> out of a DataFrame — and what is the shape trap?",
      "<pre><code>X = df[['size','beds']].to_numpy()   # (m, 2)\n"
      "y = df['price'].to_numpy()          # (m,)</code></pre>"
      + "<p>Select the columns <b>before</b> converting — afterwards the names are gone.</p>"
      + hint("<code>df['price']</code> gives (m,) but <code>df[['price']]</code> gives (m,1). Libraries "
             "want y as (m,). If you end up with (m,1), use <code>y.ravel()</code>."),
      "f0/w2-14-pandas-to-numpy.html"),

    C("f0-traceback", "algorithm",
      "How do you read a Python <b>traceback</b>?",
      steps(["read the <b>last line</b> first — it names the error and describes it in plain English",
             "then the frame just above it — that is where it broke",
             "work upwards only if you still need to know how you got there"])
      + "<p>Two habits fix most of them: <b>print the shapes</b>, and <b>print the types</b>.</p>"
      + hint("The middle lines are just the chain of calls. Almost none of a traceback matters."),
      "f0/w2-15-reading-errors.html"),

    C("f0-five-errors", "trap",
      "The five errors you will actually hit — and the fix for each.",
      bullets(["<b>ValueError: shapes not aligned</b> → print both shapes; transpose one",
               "<b>IndexError: out of bounds</b> → counting starts at 0; last is <code>x[-1]</code>",
               "<b>TypeError: can only concatenate list</b> → <code>np.array(my_list)</code>",
               "<b>NameError: not defined</b> → typo, or you never ran the import cell",
               "<b>KeyError: 'Price'</b> → <code>print(df.columns)</code>; it is probably lowercase"]),
      "f0/w2-15-reading-errors.html"),

    C("f0-function-read", "concept",
      "You meet a function you have never seen. What <b>three things</b> tell you almost everything?",
      steps(["its <b>name</b> — good code names things honestly",
             "its <b>parameters</b> — what it needs, matched <b>in order</b> unless you name them",
             "what it <b>returns</b> — one value, or a tuple of several"])
      + "<p>That is enough to <em>use</em> it without reading the body — which is exactly what every "
        "graded exercise asks of you.</p>"
      + hint("No <code>return</code> means it hands back <code>None</code>, which fails confusingly "
             "somewhere downstream rather than where the problem is."),
      "f0/w2-16-functions.html"),
])

W3 = deck("F0", 3, "The Maths Behind the Curtain", [
    C("f0-eigen", "formula",
      "What does %s say, and what makes those directions special?" % "<b>Av = λv</b>",
      blk("<var>A</var><b>v</b> = <var>λ</var><b>v</b>")
      + bullets(["<b>v</b> is an eigenvector — a direction the matrix does not <b>rotate</b>",
                 "<var>λ</var> is the eigenvalue — how much that direction is stretched",
                 "for these directions only, a whole matrix collapses to one number"])
      + hint("A = [[2,1],[1,2]]: A[1,1] = [3,3] so λ = 3; A[1,−1] = [1,−1] so λ = 1."),
      "f0/w3-01-eigenvectors.html"),

    C("f0-pca-why", "concept",
      "Why are the principal components the <b>eigenvectors of the covariance matrix</b>?",
      "<p>Because each eigenvalue <b>is</b> the variance along its own eigenvector.</p>"
      + bullets(["“find the direction of greatest variance” and “find the largest eigenvector of "
                 "the covariance matrix” are therefore the same instruction",
                 "covariance matrices are symmetric, so their eigenvalues are real and their "
                 "eigenvectors perpendicular — which is why PCA is well behaved"])
      + hint("Eigenvalues 4.976 and 0.064 → the first component keeps 98.7% of the variance."),
      "f0/w3-01-eigenvectors.html"),

    C("f0-svd", "formula",
      "State the SVD, and say why it is more general than eigendecomposition.",
      blk("<var>A</var> = <var>U</var> <var>Σ</var> <var>V</var><sup>T</sup>")
      + bullets(["rotate (V<sup>T</sup>), stretch (Σ), rotate (U)",
                 "works for <b>any</b> matrix — eigendecomposition needs a square one",
                 "Σ is sorted largest first, so truncating to the top k gives the "
                 "<b>provably best</b> rank-k approximation"])
      + hint("Singular values squared and divided by n give exactly the covariance eigenvalues. "
             "Real PCA uses SVD because forming the covariance matrix loses precision."),
      "f0/w3-02-svd.html"),

    C("f0-mle", "concept",
      "State the maximum likelihood principle, and say what it derives.",
      "<p>Choose the parameters that make the <b>data you actually observed</b> as probable as "
      "possible.</p>"
      + bullets(["assume Gaussian noise → you derive <b>squared error</b>",
                 "assume a Bernoulli outcome → you derive <b>cross-entropy</b>",
                 "take the negative log: products become sums, and nothing underflows"])
      + hint("10 flips, 7 heads: L(p) = p⁷(1−p)³ peaks at p = 0.7. The loss function stops being a "
             "convention and becomes a consequence of what you assumed."),
      "f0/w3-03-maximum-likelihood.html"),

    C("f0-jacobian", "distinguish",
      "What is a Jacobian, and how does it relate to the gradient you already use?",
      blk("<var>J<sub>ij</sub></var> = ∂<var>f<sub>i</sub></var>/∂<var>x<sub>j</sub></var>")
      + bullets(["rows are <b>outputs</b>, columns are <b>inputs</b>",
                 "ℝⁿ → ℝᵐ gives an m × n grid",
                 "the <b>gradient is a Jacobian with one row</b>, because a cost has one output"])
      + hint("The chain rule becomes matrix multiplication. Backprop evaluates that product right "
             "to left, which keeps a row vector at every step instead of building huge matrices."),
      "f0/w3-04-jacobian.html"),

    C("f0-softmax-grad", "formula",
      "What is ∂L/∂z for softmax with cross-entropy — and why is it so simple?",
      blk("∂<var>L</var>/∂<var>z</var> = <b>p − y</b>")
      + "<p>Softmax's derivative carries a factor of p<sub>y</sub>; the log in cross-entropy "
        "contributes 1/p<sub>y</sub>. They cancel exactly.</p>"
      + hint("z = [2, 1, 0.5] with true class 1 → p = [0.6285, 0.2312, 0.1402], so the gradient is "
             "[−0.3715, 0.2312, 0.1402]. Same cancellation as sigmoid + log loss in C1 W3."),
      "f0/w3-05-softmax-gradient.html"),
])

DECKS = [W1, W2, W3]
