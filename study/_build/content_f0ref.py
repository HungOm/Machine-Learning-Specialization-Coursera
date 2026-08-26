# -*- coding: utf-8 -*-
"""Quick-refresher badges for the notation Foundations Week 1 and Week 2 teach.

Unlike the other refresher modules (trig, projections, growth, means — things
the course uses but never explains), every symbol here IS taught in this site,
in F0 W1 "The Maths You Actually Need" or F0 W2 "NumPy in five minutes". The
badge is a fast way back to that lesson the fifth time you meet Sigma notation
and cannot quite remember what it means, without leaving the page you are on.

TERMS feeds the little badges that appear beside the first mention of a symbol
on a page. Each one carries its own link back to the exact F0 lesson, via
more_href / more_label — read by build_gloss() in build.py.
"""

ANCHOR = "f0ref"

F0 = "f0/w1-%s.html"
F0W2 = "f0/w2-%s.html"

# what to badge on a page, longest first (the builder sorts by length too)
PATTERNS = [
    (r"matrix multiplication", "matmul-f0"),
    (r"normal distribution", "normal-dist-f0"),
    (r"standard deviation", "variance-f0"),
    (r"dot product", "dot-product-f0"),
    (r"partial derivatives?", "partial-f0"),
    (r"\bargmax\b|\bargmin\b", "argmax-f0"),
    (r"\bmatri(?:x|ces)\b", "matrix-f0"),
    (r"\btranspose[dsn]?\b", "transpose-f0"),
    (r"\bexponentials?\b", "exponential-f0"),
    (r"\blogarithms?\b", "logarithm-f0"),
    (r"\blog\b", "logarithm-f0"),
    (r"\bprobabilit(?:y|ies)\b", "probability-f0"),
    (r"\bvariance\b", "variance-f0"),
    (r"\bderivatives?\b", "derivative-f0"),
    (r"\bvectors?\b", "vector-f0"),
    (r"\bslope\b", "slope-f0"),
    (r"Σ", "sigma"),
    (r"Π(?!\w)", "pi-notation"),
    (r"∂", "partial-f0"),
    (r"∇", "nabla"),
    # F0 W2 — NumPy mechanics. Kept to patterns confirmed safe against this
    # corpus: "shape", "axis" and "flatten" were tried and dropped, since each
    # collides constantly with an ordinary-English or plotting-axis sense here
    # (a cost curve "flattens", "ear shape", the "x-axis") — badging those
    # would attach the wrong explanation more often than the right one.
    (r"\bbroadcasting\b", "broadcasting-f0"),
    (r"\belementwise\b", "elementwise-f0"),
    (r"\bindexing\b|\bslicing\b", "indexing-f0"),
]

TERMS = [
 dict(key="sigma", label="Σ", say="“capital sigma”",
      gist="<b>Add all of these up.</b> A for-loop, written as one symbol.",
      body="<div class='gq'>Σ<sub>i=1</sub><sup>m</sup> (…)</div>"
           "<p>Start at i = 1 (the bottom number), stop at i = m (the top number), and add up "
           "whatever the expression after Σ works out to be, once per i.</p>",
      ml="Every cost function in this specialization opens with a Σ — J(w,b), the log loss, "
         "cross-entropy, the k-means cost. Read it once here and you can read all of them.",
      more_href=F0 % "07-sigma-notation", more_label="F0 W1 · Σ — summation notation"),

 dict(key="pi-notation", label="Π", say="“capital pi”",
      gist="<b>Multiply all of these together</b> — the same idea as Σ, with × instead of +.",
      body="<div class='gq'>Π<sub>i=1</sub><sup>m</sup> (…)</div>"
           "<p>Starts its running total at <b>1</b>, not 0 — multiplying by 0 would wipe out the "
           "whole calculation before it began.</p>",
      ml="Rare in this specialization — mainly the naive-Bayes-style “multiply all the "
         "probabilities” calculations.",
      more_href=F0 % "08-pi-notation", more_label="F0 W1 · Π — multiplying them all"),

 dict(key="partial-f0", label="∂J/∂w", say="“partial”, or “curly dee”",
      gist="The slope of J in <b>one direction only</b> — change w a little, hold everything else still, "
           "and see how much J moves.",
      body="<p>Picture standing on a hillside with two dials, w and b. A partial derivative asks: "
           "“if I turn <i>only</i> the w dial, which way does the height change?” — "
           "ignoring what turning b would do.</p>"
           "<div class='gq'>J = w² + b², at w = 3, b = 4</div><p>∂J/∂w = 2w = <b>6</b> — b is frozen and contributes nothing. ∂J/∂b = 2b = <b>8</b>, freezing w instead.</p>",
      ml="This is the piece gradient descent actually computes — one partial derivative per "
         "parameter, however many thousands there are.",
      more_href=F0 % "06-partial-derivatives", more_label="F0 W1 · Partial derivatives"),

 dict(key="nabla", label="∇J", say="“nabla”, or “del”",
      gist="<b>The gradient</b> — every partial derivative collected into one list.",
      body="<p>∇J is not one number. For a model with w₁, w₂ and b, it is the list "
           "[∂J/∂w₁, ∂J/∂w₂, ∂J/∂b] — one slope per parameter, "
           "bundled together. It points in the direction J grows fastest, which is why gradient descent "
           "steps in the <i>opposite</i> direction.</p>"
           "<div class='gq'>J = w² + b², at (3, 4) → ∇J = [6, 8]</div><p>Not one number — one per parameter, bundled. A network with a million weights has a million-entry gradient, built exactly this way.</p>",
      ml="A neural network with a million weights has a million-entry gradient. Same idea, just a longer list.",
      more_href=F0 % "06-partial-derivatives", more_label="F0 W1 · Partial derivatives"),

 dict(key="dot-product-f0", label="a · b", say="“the dot product”",
      gist="Multiply matching entries of two vectors, then add up the results. One number out.",
      body="<div class='gq'>a · b = a₁b₁ + a₂b₂ + … + aₙbₙ</div>"
           "<p>[1, 2, 3] · [4, 5, 6] = 4 + 10 + 18 = <b>32</b>.</p>",
      ml="w · x is the entire linear regression model before b is added. Every layer of a neural "
         "network is a stack of dot products.",
      more_href=F0 % "10-dot-product", more_label="F0 W1 · The dot product"),

 dict(key="vector-f0", label="vector", say="“vector”",
      gist="An ordered list of numbers, treated as one thing. [3, 7, 1] is a vector of length 3.",
      body="<p>The order matters — [3, 7] and [7, 3] are different vectors. In this specialization, "
           "a vector is almost always one training example's features, or one layer's worth of weights.</p>"
           "<div class='gq'>one house = [1400, 3, 2, 18]</div><p>Square feet, bedrooms, floors, age — a length-4 vector, and one row of your training set. Stack 100 of them and you have a (100, 4) matrix.</p>",
      ml="x with an arrow (x⃗) or in bold (<b>x</b>) both mean the same thing: “all the "
         "features of one example, together.”",
      more_href=F0 % "09-vectors", more_label="F0 W1 · Vectors"),

 dict(key="matrix-f0", label="matrix", say="“matrix”",
      gist="A grid of numbers — rows and columns. A stack of vectors.",
      body="<p>Shape is always written <b>rows × columns</b>. A (100, 4) matrix is 100 examples, "
           "each with 4 features — 100 rows, 4 columns.</p>"
           "<div class='gq'>X.shape → (100, 4)</div><p>100 houses down, 4 measurements across. Rows first, always — <code>X[7]</code> is house 7, <code>X[:, 2]</code> is every house's floor count.</p>",
      ml="The whole training set X is one matrix. Every layer's weights W is a matrix, one column per unit.",
      more_href=F0 % "11-matrices", more_label="F0 W1 · Matrices and shapes"),

 dict(key="matmul-f0", label="AB", say="“matrix multiplication”",
      gist="Row of the first, dotted with column of the second, for every combination. Not elementwise.",
      body="<p>(m, n) times (n, k) gives (m, k) — the inner dimensions must match, and they "
           "disappear from the answer's shape.</p>"
           "<div class='gq'>(2 × <b>3</b>) @ (<b>3</b> × 4) = (2 × 4)</div><p>The inner 3s must match and then vanish. Try (2×3) @ (2×3) and NumPy refuses — 3 ≠ 2.</p>",
      ml="A whole layer's forward pass is one matrix multiplication: every unit's dot product with the "
         "input, computed at once.",
      more_href=F0 % "12-matrix-multiplication", more_label="F0 W1 · Matrix multiplication"),

 dict(key="transpose-f0", label="A<sup>T</sup>", say="“a transpose”",
      gist="Flip a matrix over its diagonal — rows become columns, columns become rows.",
      body="<p>A (100, 4) matrix transposed becomes (4, 100). The numbers do not change, only which "
           "direction they are read in.</p>"
           "<div class='gq'>[[1, 2, 3]] is (1, 3) → .T is (3, 1)</div><p>Same three numbers, turned on their side. Nothing about the data changed; what you can multiply it with did.</p>",
      ml="Used constantly to make shapes line up for a dot product or matrix multiply — "
         "<code>X.T @ err</code> is a very common line in this course.",
      more_href=F0 % "13-transpose", more_label="F0 W1 · Transpose"),

 dict(key="exponential-f0", label="e<sup>x</sup>", say="“e to the x”",
      gist="A curve that keeps multiplying by the same amount — growth (or decay) that compounds.",
      body="<div class='gq'>e ≈ 2.71828…</div>"
           "<p>e<sup>x</sup> grows slowly at first, then explodes. e<sup>−x</sup> does the mirror "
           "image — it shrinks towards 0 and never quite gets there.</p>",
      ml="The sigmoid is built from e<sup>−z</sup>. Get comfortable with which way it bends before "
         "meeting logistic regression.",
      more_href=F0 % "14-exponentials", more_label="F0 W1 · Exponentials and e"),

 dict(key="logarithm-f0", label="log", say="“log”",
      gist="The opposite of an exponential — “what power do I need?” instead of "
           "“what does this power give me?”",
      body="<div class='gq'>log(1) = 0 &nbsp;·&nbsp; log(0.01) = large and negative</div>"
           "<p>log turns a number close to 0 into a large negative number — which is exactly the "
           "shape a loss function wants: confidently wrong should hurt a lot.</p>",
      ml="The log loss / cross-entropy cost is built entirely from log. −log(f) is the whole "
         "penalty for a wrong classification.",
      more_href=F0 % "15-logarithms", more_label="F0 W1 · Logarithms"),

 dict(key="probability-f0", label="P(x)", say="“probability of x”",
      gist="A number from 0 to 1 saying how likely something is. 0 = never, 1 = certain.",
      body="<p>All the probabilities of every possible outcome must add up to exactly <b>1</b>.</p>"
           "<div class='gq'>P(spam) = 0.7 → P(not spam) = 0.3</div><p>They must add to 1, because one of them has to happen. That single constraint is what makes a classifier's outputs readable as chances.</p>",
      ml="Logistic regression's output is literally a probability. Anomaly detection compares a "
         "probability against a threshold.",
      more_href=F0 % "16-probability", more_label="F0 W1 · Probability basics"),

 dict(key="variance-f0", label="σ²", say="“sigma squared”, or “standard deviation”",
      gist="How spread out a set of numbers is around its own average — <b>and</b> a second, looser use "
           "of the same word for “too sensitive to which examples happened to be in the training set”.",
      body="<div class='gq'>variance = average of (each value − the mean)²</div>"
           "<p>That is the precise, statistical meaning — feature scaling, anomaly detection, a "
           "regression tree's impurity measure. <b>“High variance”</b> in the bias/variance discussion "
           "(overfitting) borrows the word rather than computing this formula: it means the model would "
           "give a wildly different answer if trained on a different sample of the same data. Related "
           "in spirit, not the same calculation.</p>"
           "<p>Standard deviation (σ) is just the square root of variance, back in the original "
           "units instead of squared ones.</p>",
      ml="Feature scaling divides by σ. A regression tree's impurity measure is variance, not entropy. "
         "See “bias and variance” (C2 W3) for the looser, diagnostic sense of the word.",
      more_href=F0 % "17-mean-variance", more_label="F0 W1 · Mean, variance and standard deviation"),

 dict(key="normal-dist-f0", label="N(μ, σ²)", say="“normal distribution”",
      gist="The bell curve — fully described by just two numbers: where it is centred (μ) and "
           "how wide it is (σ²).",
      body="<p>Most values land near the mean μ; the chance of a value drops off the further it is "
           "from μ, at a rate set by σ.</p>"
           "<div class='gq'>heights: μ = 170 cm, σ = 10 cm</div><p>Someone 180 cm is exactly 1σ above the mean — common. At 200 cm they are 3σ out, which is where anomaly detection starts paying attention.</p>",
      ml="Anomaly detection fits a normal distribution to “normal” data, then flags anything "
         "the curve says is very unlikely.",
      more_href=F0 % "18-normal-distribution", more_label="F0 W1 · The normal distribution"),

 dict(key="argmax-f0", label="argmax", say="“arg-max”",
      gist="<b>Which one</b> has the highest score — not the score itself. max answers “how "
           "high”; argmax answers “which”.",
      body="<div class='gq'>scores = [0.1, 0.7, 0.2] &nbsp;→&nbsp; max = 0.7, argmax = 1</div>"
           "<p>argmax returns the <i>position</i> of the winner, not its value.</p>",
      ml="Turning softmax's output into an actual class prediction is exactly this: argmax over the "
         "probabilities.",
      more_href=F0 % "19-min-max-argmax", more_label="F0 W1 · min, max, argmin and argmax"),

 dict(key="derivative-f0", label="dJ/dw", say="“the derivative”",
      gist="The slope of a curve at one exact point — a single number with a sign.",
      body="<p>Positive means the curve rises to the right there; negative means it falls. Zero means "
           "flat — momentarily neither rising nor falling.</p>"
           "<div class='gq'>J = w², at w = 3 → dJ/dw = 2w = 6</div><p>Positive, so the cost rises as w rises: step left. At w = −3 it is −6, so step right. The sign alone tells you which way.</p>",
      ml="Gradient descent's entire update rule is built from one idea: subtract a small multiple of "
         "the derivative, so you move downhill.",
      more_href=F0 % "05-derivatives", more_label="F0 W1 · What a derivative actually is"),

 dict(key="slope-f0", label="slope", say="“slope”",
      gist="Rise over run — how much y changes for each step across in x.",
      body="<div class='gq'>slope = (change in y) ÷ (change in x)</div>",
      ml="The w in f(x) = wx + b <i>is</i> a slope: dollars of price per square foot, in the housing "
         "example.",
      more_href=F0 % "04-slope", more_label="F0 W1 · Slope — rise over run"),

 dict(key="broadcasting-f0", label="broadcasting", say="“broadcasting”",
      gist="NumPy silently <b>stretching</b> a smaller array to match a bigger one, so a shape "
           "mismatch you would expect to error out just... works.",
      body="<p>Add a length-4 vector to every row of a (100, 4) matrix, and NumPy repeats the vector "
           "100 times without you writing a loop or copying anything in memory.</p>"
           "<p>Convenient, and a real source of silent bugs when the shapes you meant to line up "
           "don't, and NumPy broadcasts them anyway instead of raising an error.</p>"
           "<div class='gq'>(100, 4) − (4,) → (100, 4)</div><p>The 4-number row is reused for all 100 rows without being copied. That is feature scaling in one line — and the reason a shape mistake can run silently instead of erroring.</p>",
      ml="Feature scaling is one broadcast: (X − mu) divides a whole matrix by a single row of "
         "per-feature values.",
      more_href=F0W2 % "08-broadcasting", more_label="F0 W2 · Broadcasting"),

 dict(key="elementwise-f0", label="elementwise", say="“element-wise”",
      gist="Apply an operation to each matching pair of entries separately — position 1 with "
           "position 1, position 2 with position 2, and so on.",
      body="<div class='gq'>[1, 2, 3] + [10, 20, 30] = [11, 22, 33]</div>"
           "<p>Not a dot product, not matrix multiplication — no numbers get summed together. Every "
           "output position depends on exactly one pair of inputs.</p>",
      ml="<code>w * x</code> in NumPy is elementwise. The dot product is elementwise multiplication "
         "<i>then</i> a sum — one extra step.",
      more_href=F0W2 % "07-elementwise", more_label="F0 W2 · Elementwise arithmetic"),

 dict(key="indexing-f0", label="x[i]", say="“indexing”, and “slicing”",
      gist="Indexing pulls out <b>one</b> element by position. Slicing pulls out a <b>range</b> of them.",
      body="<div class='gq'>x[0] &nbsp;→ one value &nbsp;&nbsp;·&nbsp;&nbsp; x[1:3] &nbsp;→ a sub-array</div>"
           "<p>Counting starts at <b>0</b>, and a slice's end index is not included — "
           "<code>x[1:3]</code> gives positions 1 and 2, not 3.</p>",
      ml="<code>X[:, j]</code> — every row, column j — is how a single feature gets pulled out of a "
         "whole training set.",
      more_href=F0W2 % "04-indexing-slicing", more_label="F0 W2 · Indexing and slicing"),
]
