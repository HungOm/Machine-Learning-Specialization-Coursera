# -*- coding: utf-8 -*-
"""Foundations · Week 3 — The maths behind the curtain."""
from kit import (kid, key, warn, trap, note, card, eq, eqp, decode, table, demo,
                 quiz, links, code, h2, grid2, grid3, pretest, explain, lenses)

L = []

def lesson(slug, title, mins, lede, body):
    L.append(dict(slug=slug, title=title, mins=mins, tag="foundations", lede=lede, body=body))


# ============================================================ 1
lesson("01-eigenvectors", "Eigenvectors — the directions a matrix leaves alone", 15,
    "PCA told you the principal components 'are the eigenvectors of the covariance matrix' and "
    "moved on. This is what that sentence means, and why an eigenvector is the right object for "
    "that job.",
    pretest("""<p>A matrix multiplication generally rotates a vector <em>and</em> changes its length. <b>Guess what is special about the vectors it does not rotate</b> — the ones that only get longer or shorter.</p>""",
    """<p>Watch for the fact that those directions are a property of the matrix itself, not of anything you chose.</p>""")
    + h2("🎈", "The idea, in plain words")
    + kid("""<p>Multiplying by a matrix usually does two things to a vector: turns it, and stretches
it. But for most matrices there are a few special directions where the turning does not happen —
the vector comes out pointing exactly the same way, just longer or shorter.</p>
<p>Those directions are the <b>eigenvectors</b>. How much each one stretches is its
<b>eigenvalue</b>. They are not something you pick; they are baked into the matrix, and finding them
is how you find out what the matrix fundamentally does.</p>""")

    + lenses(
        """<p>Stretching a sheet of rubber.</p>
<p>Draw arrows all over it, then pull it diagonally. Almost every arrow ends up pointing somewhere
new. But the arrows that happened to lie <em>along</em> the pull, and the ones exactly across it,
still point the same way — they just got longer or shorter.</p>
<p>Those two directions were not chosen by you. They are a fact about how you pulled.</p>""",

        """<p>If you have met resonance in physics or a mode shape in engineering, this is the same
object: the eigenvectors of a system are the configurations it can be in without changing shape.</p>
<p>The defining equation is <var>A</var><b>v</b> = <var>λ</var><b>v</b> — applying the matrix is
equivalent, <em>for that vector only</em>, to multiplying by a single number.</p>""",

        """<p>A spinning object with an axis.</p>
<p>Everything on the object moves as it spins, except the points on the axis. The axis is the
direction the rotation leaves alone — an eigenvector, with eigenvalue 1.</p>""",

        """<p>Google's original PageRank was an eigenvector computation, and so is every structural
resonance analysis: bridges, aircraft wings, buildings in earthquakes.</p>
<p>The Tacoma Narrows bridge failed because wind excited a mode the designers had not analysed. When
engineers say “find the modes”, they mean find the eigenvectors — because those are the directions
where a small repeated push accumulates instead of cancelling.</p>""",

        """So the equation below says one thing: for these particular directions, a whole matrix
collapses into a single number.""")

    + h2("🎬", "Watch it move")
    + demo("f0-eigen", "The directions that do not turn",
           "rotate the input vector and watch where the output stops swinging")

    + h2("🔢", "The maths, decoded")
    + eq("""<var>A</var><var class="ov vec">v</var> <span class="op">=</span> <var>λ</var>
<var class="ov vec">v</var>""", "applying A does nothing but scale v")
    + decode([
        ("<var>A</var>", "“the matrix”", "The transformation. Must be square — the same number of rows as columns."),
        ("<var class='ov vec'>v</var>", "“an eigenvector”", "A direction A does not rotate. Any multiple of it is also one, so only the direction matters."),
        ("<var>λ</var>", "“lambda”, the eigenvalue", "How much that direction is stretched. λ = 2 doubles it; λ = 0.5 halves it; a negative λ flips it."),
    ])

    + h2("🧮", "Worked, by hand")
    + """<p>Take <var>A</var> = [[2, 1], [1, 2]] and try the vector [1, 1]:</p>"""
    + eq("""<span class="paren">[</span>2 1 <span class="op">;</span> 1 2<span class="paren">]</span>
<span class="paren">[</span>1 <span class="op">;</span> 1<span class="paren">]</span>
<span class="op">=</span> <span class="paren">[</span>3 <span class="op">;</span> 3<span class="paren">]</span>
<span class="op">=</span> 3 <span class="paren">[</span>1 <span class="op">;</span> 1<span class="paren">]</span>""",
         "same direction, three times as long — so λ = 3")
    + """<p>Now try [1, −1]:</p>"""
    + eq("""<span class="paren">[</span>2 1 <span class="op">;</span> 1 2<span class="paren">]</span>
<span class="paren">[</span>1 <span class="op">;</span> −1<span class="paren">]</span>
<span class="op">=</span> <span class="paren">[</span>1 <span class="op">;</span> −1<span class="paren">]</span>
<span class="op">=</span> 1 <span class="paren">[</span>1 <span class="op">;</span> −1<span class="paren">]</span>""",
         "unchanged — so λ = 1")
    + """<p>Two eigenvectors, eigenvalues 3 and 1. Every other direction gets rotated; these two do
not. Check the first one yourself: 2(1) + 1(1) = 3, and 1(1) + 2(1) = 3.</p>"""
    + explain("""<p>Any multiple of an eigenvector is also an eigenvector — [2, 2] works exactly as
well as [1, 1]. <b>Why does that mean only the direction carries information?</b></p>""",
              """<p>Because the defining equation is homogeneous: if
<var>A</var><b>v</b> = <var>λ</var><b>v</b>, then <var>A</var>(<var>c</var><b>v</b>) =
<var>c</var><var>A</var><b>v</b> = <var>λ</var>(<var>c</var><b>v</b>) for any constant. The length
cancels off both sides, so it was never part of the claim. That is why implementations return
<em>unit</em> eigenvectors — the length is an arbitrary choice, and normalising makes the answer
canonical.</p>""")

    + h2("🔬", "And now PCA makes sense")
    + """<p>Course 3 said the principal components are the eigenvectors of the covariance matrix. Here
is why that is the right object rather than a convenient one.</p>
<p>The covariance matrix describes how the data is spread. Its eigenvectors are the directions that
spread does not rotate — the natural axes of the cloud. And each eigenvalue <em>is</em> the variance
along its own eigenvector.</p>"""
    + table(["five points, centred", "covariance", "eigenvalues", "first eigenvector"],
            [["(−2, −2.4) … (2, 2.6)", "[[2.00, 2.40], [2.40, 3.04]]", "4.976 and 0.064", "[0.628, 0.778]"]])
    + """<p>So the first component keeps 4.976 ÷ (4.976 + 0.064) = <b>98.7%</b> of the variance. “Find
the direction of greatest spread” and “find the largest eigenvector of the covariance matrix” are the
same instruction — which is exactly what PCA needed and never explained.</p>"""

    + h2("🕳", "Traps")
    + trap("""<p><b>Expecting every matrix to have real eigenvectors.</b> A pure rotation has none in
the real plane — it turns everything. Symmetric matrices (like every covariance matrix) always have
real eigenvalues and perpendicular eigenvectors, which is why PCA is well behaved.</p>""")

    + h2("✅", "Check yourself")
    + quiz([
        ("Verify that [1, −1] is an eigenvector of [[2, 1], [1, 2]] and give its eigenvalue.",
         "<p>Row 1: 2(1) + 1(−1) = 1. Row 2: 1(1) + 2(−1) = −1. The result is [1, −1] itself, so "
         "<b>λ = 1</b>.</p>"),
        ("Why is “direction of greatest variance” the same as “largest eigenvector of the covariance matrix”?",
         "<p>Because each eigenvalue of the covariance matrix is precisely the variance along its "
         "eigenvector. Maximising variance over directions is therefore maximising the "
         "eigenvalue.</p>"),
        ("A matrix has an eigenvalue of 0. What does that mean geometrically?",
         "<p>Some direction is squashed to nothing — the matrix collapses that whole direction to "
         "the origin, so it is not invertible. A zero eigenvalue is exactly a singular matrix.</p>"),
    ])

    + h2("🔗", "Go deeper")
    + links([
        ("lesson", "c3/w2-14-pca-algorithm.html", "C3 W2 · The PCA algorithm",
         "Where this was used as a black box. Worth rereading now."),
        ("video", "https://www.3blue1brown.com/lessons/eigenvalues",
         "3Blue1Brown — eigenvectors", "The animation of the directions that do not turn."),
    ]))


# ============================================================ 2
lesson("02-svd", "SVD — the one factorisation worth knowing", 14,
    "Every matrix, without exception, decomposes into a rotation, a stretch, and another rotation. "
    "It is what PCA actually computes in practice, and it underlies compression and recommender "
    "systems too.",
    pretest("""<p>Eigenvectors only exist for square matrices, and not always then. <b>Guess whether there is something similar that works for ANY matrix</b> — including a 4778 × 443 ratings matrix.</p>""",
    """<p>Watch for the answer being three matrices rather than one.</p>""")
    + h2("🎈", "The idea, in plain words")
    + kid("""<p>Any matrix at all — square or not, invertible or not — can be pulled apart into three
simple pieces: <b>rotate, stretch, rotate</b>. Nothing else. That is the singular value
decomposition.</p>
<p>The middle piece is a list of stretch amounts, in decreasing order. And because they are ordered,
you can simply <em>throw away the small ones</em> — which turns out to be the best possible way to
approximate the matrix with less data.</p>""")

    + lenses(
        """<p>Describing any journey as: turn, walk, turn.</p>
<p>However winding the route looked, you can always express where you ended up as a rotation, a
straight-line distance, and another rotation. SVD is the claim that every linear transformation
decomposes that way — no exceptions.</p>""",

        """<p><var>A</var> = <var>UΣV</var><sup>T</sup>, where U and V are orthogonal (rotations) and
Σ is diagonal (stretches).</p>
<p>The Eckart–Young theorem is the reason it matters: truncating Σ to its largest <var>k</var> values
gives the <b>provably best</b> rank-<var>k</var> approximation to A. Not a good heuristic — optimal,
under the usual norms.</p>""",

        """<p>A stack of transparencies, ordered by how much they matter.</p>
<p>The first one carries most of the picture. The second adds detail. By the fiftieth you are adding
almost nothing. Keep the first few and discard the rest, and you have compressed the image with the
least possible loss.</p>""",

        """<p>This is the mathematics behind image compression, latent semantic analysis, noise
reduction, and the recommender system you built in Course 3 — matrix factorisation is SVD's idea,
adapted for a matrix with missing entries.</p>
<p>It is also how <code>numpy.linalg.pinv</code> and most least-squares solvers work internally, since
SVD handles the near-singular cases that the normal equations do not.</p>""",

        """So the three matrices below are what <code>PCA()</code> actually calls, and knowing that
turns two black boxes into one idea.""")

    + h2("🎬", "Watch it move")
    + demo("f0-svd", "Rotate, stretch, rotate",
           "one matrix pulled apart into its three pieces, and rebuilt from the largest few")

    + h2("🔢", "The maths, decoded")
    + eq("""<var>A</var> <span class="op">=</span> <var>U</var> <var>Σ</var>
<var>V</var><sup>T</sup>""", "any matrix at all, without exception")
    + decode([
        ("<var>U</var>", "“U”", "A rotation in the output space. Its columns are orthogonal unit vectors."),
        ("<var>Σ</var>", "“sigma”, the singular values", "A diagonal matrix of stretch factors, always ≥ 0 and always sorted largest first."),
        ("<var>V</var><sup>T</sup>", "“V transpose”", "A rotation in the input space, applied first."),
        ("rank-k truncation", "“keeping the top k”", "Zero out all but the largest k singular values. Provably the best possible approximation using that much information."),
    ])

    + h2("🧮", "And the link to eigenvectors")
    + """<p>Take the same five centred points from the last lesson and compute both:</p>"""
    + table(["", "value"],
            [["singular values of the centred data", "4.988 and 0.567"],
             ["their squares ÷ n", "<b>4.976 and 0.064</b>"],
             ["eigenvalues of the covariance matrix", "<b>4.976 and 0.064</b>"],
             ["first row of V<sup>T</sup>", "[0.628, 0.778]"],
             ["first eigenvector of the covariance", "[0.628, 0.778]"]])
    + key("""<p>They are the same computation. PCA can be done either by eigendecomposing the
covariance matrix or by taking the SVD of the centred data — and real implementations use the SVD,
because forming the covariance matrix explicitly loses precision.</p>""")

    + h2("🕳", "Traps")
    + trap("""<p><b>Forgetting to centre the data.</b> SVD of uncentred data finds the direction of
greatest <em>magnitude</em>, not of greatest variance — and the first component usually just points
at the mean. PCA subtracts the mean first for exactly this reason.</p>""")

    + h2("✅", "Check yourself")
    + quiz([
        ("Why does SVD work for a 4778 × 443 matrix when eigendecomposition does not?",
         "<p>Eigendecomposition requires a square matrix. SVD is defined for any shape, because it "
         "uses two different rotations — one in the input space and one in the output space — "
         "rather than one basis for both.</p>"),
        ("What does “keep the top 2 singular values” achieve?",
         "<p>The best possible rank-2 approximation of the matrix, by the Eckart–Young theorem. Not "
         "a reasonable heuristic — provably optimal.</p>"),
        ("Why do real PCA implementations use SVD rather than eigendecomposition?",
         "<p>Numerical precision. Forming the covariance matrix squares the data, which squares the "
         "condition number and loses accuracy. Taking the SVD of the centred data avoids ever "
         "forming it.</p>"),
    ])

    + h2("🔗", "Go deeper")
    + links([
        ("lesson", "c3/w2-03-collaborative-filtering.html", "C3 W2 · Collaborative filtering",
         "Matrix factorisation — SVD's idea, adapted for a matrix that is 98% missing."),
    ]))


# ============================================================ 3
lesson("03-maximum-likelihood", "Maximum likelihood — where the loss functions came from", 15,
    "You were told cross-entropy 'comes from statistics' and squared error is 'natural'. Both are "
    "consequences of one principle, and deriving them is what turns a loss function from a "
    "convention into a decision.",
    pretest("""<p>You have data and a model with unknown parameters. <b>Guess a principled way to choose them</b> — something better than “try values until the errors look small”.</p>""",
    """<p>Watch for turning the question around: instead of asking how well the model fits the data, ask how probable the data is under the model.</p>""")
    + h2("🎈", "The idea, in plain words")
    + kid("""<p>Turn the question around. Instead of “how wrong is my model?”, ask: <b>if my model were
true, how likely was the data I actually observed?</b></p>
<p>Then pick the parameters that make the observed data as likely as possible. That is maximum
likelihood, and it is where nearly every loss function in this specialization comes from — including
the two you were told to accept.</p>""")

    + lenses(
        """<p>A detective with two suspects.</p>
<p>You do not ask which suspect feels guilty. You ask: <em>if this one did it, how likely is
everything we found?</em> Then again for the other. The suspect under whom the evidence is least
surprising is the one you charge.</p>
<p>Maximum likelihood is that reasoning, made arithmetic.</p>""",

        """<p>The likelihood is P(data | parameters), viewed as a function of the parameters with the
data held fixed. Maximise it — or equivalently minimise its negative logarithm, which turns products
into sums and stops the numbers underflowing.</p>
<p>The payoff is that the loss function stops being a design choice. Assume Gaussian noise and you
<em>derive</em> squared error. Assume a Bernoulli outcome and you <em>derive</em> cross-entropy.</p>""",

        """<p>A curve of “how probable is my data” plotted against the parameter.</p>
<p>It has a peak. The parameter at that peak is the estimate. Everything else — gradient descent, the
loss surface, the bowl — is machinery for finding that peak.</p>""",

        """<p>This is the reason two of the most-used loss functions in machine learning are the ones
they are, and it changes what you do when neither fits.</p>
<p>Count data with a Poisson assumption gives a different loss again. Knowing the derivation is what
lets you write the right loss for an unusual problem rather than reaching for MSE and hoping.</p>""",

        """So the negative log below is not a trick to make the algebra tidy — it is the principle,
written down.""")

    + h2("🎬", "Watch it move")
    + demo("f0-mle", "The likelihood curve, and its peak",
           "drag the parameter and watch how probable your data becomes")

    + h2("🧮", "Worked: a coin")
    + """<p>Flip a coin 10 times, get 7 heads. What is the most likely bias <var>p</var>?</p>"""
    + eq("""<var>L</var>(<var>p</var>) <span class="op">=</span> <var>p</var><sup>7</sup>
<span class="op">·</span> (1 − <var>p</var>)<sup>3</sup>""",
         "the probability of exactly this data, if the bias were p")
    + table(["p", "likelihood", "−log likelihood"],
            [["0.5", "0.000977", "6.932"],
             ["0.6", "0.001792", "6.325"],
             ["<b>0.7</b>", "<b>0.002224</b>", "<b>6.109</b> ← smallest"],
             ["0.8", "0.001678", "6.390"]])
    + """<p>The peak is at <var>p</var> = 0.7 = 7/10, which is the answer intuition would have given
— but now it is <em>derived</em> rather than assumed, and the same derivation works where intuition
has nothing to say.</p>"""

    + h2("🔬", "Deriving the two losses you already use")
    + grid2(
        card("<h3>Squared error</h3><p>Assume the target is the model's prediction plus Gaussian "
             "noise. The probability of one observation is proportional to "
             "<var>e</var><sup>−(y−f)²/2σ²</sup>.</p><p>Take the negative log and the exponential "
             "disappears, leaving <b>(y − f)²</b> plus constants. Minimising squared error <em>is</em> "
             "maximum likelihood under Gaussian noise.</p>"),
        card("<h3>Cross-entropy</h3><p>Assume a binary outcome with probability <var>f</var>. The "
             "probability of one observation is "
             "<var>f</var><sup><var>y</var></sup>(1−<var>f</var>)<sup>1−<var>y</var></sup>.</p>"
             "<p>Take the negative log and you get exactly <b>−y log f − (1−y) log(1−f)</b> — the "
             "logistic loss from C1 W3, with nothing added.</p>"))
    + key("""<p>This is the answer to a question C1 W3 raised and left open. The logarithm in the
logistic loss is not there to make the surface convex — convexity is a <em>consequence</em>. It is
there because the likelihood is a product, and taking the log of a product gives a sum.</p>""")

    + h2("🕳", "Traps")
    + trap("""<p><b>Reading the likelihood as “the probability that the parameters are right”.</b> It
is the probability of the <em>data</em>, given the parameters — the other way round. Getting a
probability over parameters requires Bayes' theorem and a prior, which is a different framework.</p>""")

    + h2("✅", "Check yourself")
    + quiz([
        ("Why take the log of the likelihood?",
         "<p>Two reasons. It turns a product over examples into a sum, which is far easier to "
         "differentiate. And it stops the product of thousands of small probabilities underflowing "
         "to zero in floating point.</p>"),
        ("Which noise assumption produces squared error?",
         "<p>Gaussian. The exponential in the normal density and the logarithm in the negative "
         "log-likelihood cancel, leaving the squared term.</p>"),
        ("What would you do for count data that cannot be negative?",
         "<p>Assume a distribution that fits — Poisson, say — write its negative log-likelihood, "
         "and use that as the loss. The framework tells you what to do; MSE would be the wrong "
         "answer.</p>"),
    ])

    + h2("🔗", "Go deeper")
    + links([
        ("lesson", "c1/w3-05-logistic-loss.html", "C1 W3 · The logistic loss",
         "Where you were told this 'comes from statistics'. This is the statistics."),
    ]))


# ============================================================ 4
lesson("04-jacobian", "The Jacobian — derivatives when everything is a vector", 14,
    "A derivative when there is one input and one output is a number. With many of each it is a "
    "grid — and that grid is what backpropagation actually multiplies.",
    pretest("""<p>A function takes 3 numbers and returns 2. <b>Guess how many partial derivatives that has</b>, and what shape they naturally arrange into.</p>""",
    """<p>Watch for one derivative per (output, input) pair.</p>""")
    + h2("🎈", "The idea, in plain words")
    + kid("""<p>With one input and one output, the derivative is one number: nudge the input, see how
much the output moves.</p>
<p>With 3 inputs and 2 outputs there are 6 questions to ask — how much does each output move when
each input is nudged. Arrange those 6 numbers in a grid with one row per output and one column per
input, and you have the <b>Jacobian</b>. It is not a new idea; it is bookkeeping for derivatives you
already know how to take.</p>""")

    + lenses(
        """<p>A mixing desk with three sliders and two speakers.</p>
<p>Nudge slider 1: how much does the left speaker change? And the right? Now slider 2. Six answers,
naturally laid out as a table with speakers down the side and sliders across the top.</p>
<p>Nobody would call that table a difficult concept. It is just all six answers, written down
tidily.</p>""",

        """<p>The Jacobian of <var>f</var>: ℝ<sup><var>n</var></sup> → ℝ<sup><var>m</var></sup> is the
<var>m</var> × <var>n</var> matrix with entries ∂<var>f<sub>i</sub></var>/∂<var>x<sub>j</sub></var>.</p>
<p>It is the best linear approximation to <var>f</var> at a point — the multi-dimensional version of
the tangent line. And the chain rule becomes matrix multiplication, which is precisely what makes
backpropagation expressible as a sequence of matmuls.</p>""",

        """<p>A rectangle of numbers: outputs down the side, inputs across the top.</p>
<p>Read the shape and you know what the function does — a (2, 3) Jacobian belongs to a function
taking 3 numbers to 2. The shape is the signature.</p>""",

        """<p>This is what every autodiff framework computes, and the reason backpropagation is
efficient rather than merely possible.</p>
<p>Frameworks never build the full Jacobian for a large layer — they compute <b>Jacobian-vector
products</b> instead, because for a scalar loss you only ever need one row of it. That single
optimisation is the difference between backprop being cheap and being unusable.</p>""",

        """So the grid below is the object <code>tape.gradient</code> is manipulating on your
behalf.""")

    + h2("🎬", "Watch it move")
    + demo("f0-jacobian", "One derivative per input-output pair",
           "nudge each input and watch its column of the grid respond")

    + h2("🔢", "The maths, decoded")
    + eq("""<var>J</var><sub><var>ij</var></sub> <span class="op">=</span>
<span class="frac"><span>∂<var>f<sub>i</sub></var></span><span>∂<var>x<sub>j</sub></var></span></span>""",
         "row i, column j: how much output i moves when input j is nudged")
    + table(["function", "Jacobian shape", "also called"],
            [["ℝ → ℝ", "1 × 1", "the ordinary derivative"],
             ["ℝ<sup>n</sup> → ℝ", "1 × n", "the <b>gradient</b> — one row"],
             ["ℝ<sup>n</sup> → ℝ<sup>m</sup>", "m × n", "the Jacobian"],
             ["a cost function of w", "1 × (number of parameters)", "what gradient descent steps along"]])
    + note("""<p>The gradient you have used since Course 1 is a Jacobian with one row — because a
cost function has exactly one output. That is the whole relationship between the two words.</p>""",
           "The gradient is a special case")

    + h2("🔬", "Why the chain rule becomes matrix multiplication")
    + """<p>Compose two functions and their Jacobians multiply:</p>"""
    + eq("""<var>J</var><sub><var>f</var>∘<var>g</var></sub> <span class="op">=</span>
<var>J<sub>f</sub></var> <span class="op">·</span> <var>J<sub>g</sub></var>""",
         "the chain rule, in one line, for any dimensions")
    + """<p>A network is a long composition of layers, so its derivative is a long product of
Jacobians. Backpropagation is that product, evaluated <b>right to left</b> — and the order is the
entire trick: right to left keeps a vector at every step, while left to right would build enormous
intermediate matrices.</p>"""
    + explain("""<p>Both orders compute the identical answer, since matrix multiplication is
associative. <b>Why is right-to-left dramatically cheaper?</b></p>""",
              """<p>Because the loss is a <em>scalar</em>, so the leftmost Jacobian is a single row.
Starting from that end, every product is (1 × n) times (n × m), which stays a row vector — cheap, and
no large matrix ever exists. Starting from the right, you multiply big matrix by big matrix repeatedly
and only collapse to a row at the very last step, having built and stored several huge intermediates
on the way. Same answer, wildly different cost — and that asymmetry is exactly why it is called
<em>back</em>propagation.</p>""")

    + h2("🕳", "Traps")
    + trap("""<p><b>Getting the shape backwards.</b> Rows are outputs, columns are inputs. A (2, 3)
Jacobian means 3 inputs and 2 outputs. Transposing it silently is a very common bug when writing
derivatives by hand.</p>""")

    + h2("✅", "Check yourself")
    + quiz([
        ("A layer maps 512 inputs to 256 outputs. What is its Jacobian's shape?",
         "<p>(256, 512) — rows are outputs, columns are inputs. Note that is 131,072 numbers, which "
         "is why frameworks never build it explicitly.</p>"),
        ("How is the gradient related to the Jacobian?",
         "<p>It is a Jacobian with a single row, because a cost function has a single output. Same "
         "object, special case.</p>"),
        ("Why does backprop go backwards rather than forwards?",
         "<p>Because the loss is a scalar, so starting from the loss end keeps everything a row "
         "vector. Going forwards would build large matrix-by-matrix products and only collapse at "
         "the end.</p>"),
    ])

    + h2("🔗", "Go deeper")
    + links([
        ("lesson", "c2/w2-14-computation-graph.html", "C2 W2 · Computation graph",
         "Backpropagation as a walk through a graph — this is the algebra underneath it."),
    ]))


# ============================================================ 5
lesson("05-softmax-gradient", "Why softmax and cross-entropy cancel", 14,
    "Course 2 said the messy factor 'magically cancels'. It does, it is not magic, and deriving it "
    "once explains why these two functions are always paired.",
    pretest("""<p>Softmax has a genuinely messy derivative, and so does the log in cross-entropy. <b>Guess what the two of them together produce</b> — the answer is much simpler than either part.</p>""",
    """<p>Watch for a result you could write on one line.</p>""")
    + h2("🎈", "The idea, in plain words")
    + kid("""<p>Softmax's derivative is awkward: because every output depends on every input through
the shared denominator, it is a full grid rather than a simple list.</p>
<p>Cross-entropy's derivative involves dividing by the predicted probability, which blows up when
that probability is small.</p>
<p>Put them together and both messes cancel exactly, leaving <b>predicted minus actual</b>. One
subtraction. That is why these two are always paired — not convention, but because their derivatives
were made for each other.</p>""")

    + lenses(
        """<p>Two awkward gear ratios that happen to be reciprocals.</p>
<p>Each on its own is an odd number to work with. Put them in series and the awkwardness cancels
exactly, and the machine turns at a clean 1:1. Neither part was designed to be simple; the
<em>combination</em> was.</p>""",

        """<p>Softmax's Jacobian is ∂<var>p<sub>i</sub></var>/∂<var>z<sub>j</sub></var> =
<var>p<sub>i</sub></var>(<var>δ<sub>ij</sub></var> − <var>p<sub>j</sub></var>) — an
<var>n</var> × <var>n</var> matrix. Cross-entropy contributes a −1/<var>p<sub>y</sub></var>.</p>
<p>Multiply them and the <var>p<sub>y</sub></var> terms cancel, collapsing the whole product to
<b>p − y</b>. The same cancellation happens for sigmoid with binary cross-entropy, which is why C1 W3's
update rule looked identical to linear regression's.</p>""",

        """<p>Two pages of algebra, and a one-line answer at the bottom.</p>
<p>That collapse is the thing to remember. If you ever derive it and do not land on
<code>p - y</code>, you have made an error somewhere in the middle.</p>""",

        """<p>Every classification network you will ever train relies on this. It is why the loss and
the output activation are specified <em>together</em> in every framework, and why
<code>from_logits=True</code> exists — it lets the framework use the cancelled form directly rather
than computing softmax and then undoing it.</p>
<p>Mixing a softmax output with squared error, by contrast, gives you the uncancelled mess and a
model that trains much worse for no benefit.</p>""",

        """So the one-line result below is worth memorising, and the derivation below it is worth
doing once.""")

    + h2("🎬", "Watch it move")
    + demo("f0-softmax-grad", "Two messes, one clean answer",
           "change the scores and watch the gradient stay exactly p − y")

    + h2("🧮", "The result, verified numerically")
    + """<p>Take scores <var>z</var> = [2, 1, 0.5] with the true class being the first one:</p>"""
    + table(["", "value"],
            [["softmax p", "[0.6285, 0.2312, 0.1402]"],
             ["one-hot y", "[1, 0, 0]"],
             ["<b>p − y</b>", "<b>[−0.3715, 0.2312, 0.1402]</b>"],
             ["numerical derivative of the loss", "<b>[−0.3715, 0.2312, 0.1402]</b>"]])
    + """<p>The numerical derivative was computed by nudging each score by 10⁻⁶ and measuring the
change in the loss. It matches <b>p − y</b> to four decimal places — the cancellation is real, not a
simplification someone made for teaching.</p>"""
    + eq("""<span class="frac"><span>∂<var>L</var></span><span>∂<var>z</var></span></span>
<span class="op">=</span> <var class="ov vec">p</var> <span class="op">−</span>
<var class="ov vec">y</var>""", "the whole gradient, for any number of classes")

    + h2("🔬", "Why it cancels")
    + """<p>The loss only involves the true class's probability: <var>L</var> = −log
<var>p<sub>y</sub></var>. So differentiating gives a factor of −1/<var>p<sub>y</sub></var>.</p>
<p>Softmax's derivative for that same output carries a factor of <var>p<sub>y</sub></var>. The two
meet and cancel — which is exactly why the messy denominator never appears in the final
expression.</p>"""
    + key("""<p>This is the same cancellation as C1 W3's sigmoid and log loss, generalised from two
classes to N. Both are instances of one pattern: pair the right output function with the right loss
and the chain-rule factor disappears, leaving (prediction − target).</p>""")

    + h2("🕳", "Traps")
    + trap("""<p><b>Pairing softmax with squared error.</b> The cancellation does not happen, so you
get the full messy Jacobian and a gradient that dies where the softmax saturates — the same failure
mode as C1 W3's squared-error-on-a-sigmoid experiment.</p>""")

    + h2("✅", "Check yourself")
    + quiz([
        ("What is ∂L/∂z for softmax with cross-entropy?",
         "<p><b>p − y</b> — the predicted distribution minus the one-hot target. One subtraction, "
         "for any number of classes.</p>"),
        ("Why is this the same result as C1 W3's logistic regression gradient?",
         "<p>Because sigmoid + binary cross-entropy is the two-class case of softmax + "
         "cross-entropy. Same cancellation, same (prediction − target) × input form.</p>"),
        ("What does from_logits=True let a framework do?",
         "<p>Skip computing softmax and then undoing it. It can evaluate the cancelled expression "
         "directly from the raw scores, which is both faster and numerically far more stable.</p>"),
    ])

    + h2("🔗", "Go deeper")
    + links([
        ("lesson", "c2/w2-09-improved-softmax.html", "C2 W2 · Improved softmax",
         "The practical consequence — why from_logits=True exists."),
    ]))


WEEK = dict(course="F0", week=3, title="The Maths Behind the Curtain", lessons=L)
