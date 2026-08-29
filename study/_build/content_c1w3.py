# -*- coding: utf-8 -*-
"""C1 · Week 3 — Classification, logistic regression, regularisation."""
from kit import (kid, key, warn, trap, note, card, eq, eqp, decode, table, demo,
                 quiz, links, code, h2, grid2, grid3, pretest, explain, lenses)

REPO = "../../C1%20-%20Supervised%20Machine%20Learning%20-%20Regression%20and%20Classification"
L = []

# ============================================================ 1
L.append(dict(
    slug="01-motivations", title="Motivations: why not linear regression?", mins=9, tag="intuition",
    lede="A reasonable-looking idea that fails for two specific reasons — and seeing exactly how it fails "
         "is the best possible motivation for what replaces it.",
    body=(
        pretest("""<p>Tumour size in, benign-or-malignant out. You fit a straight line and threshold at 0.5. <b>Guess what one far-away data point does to that boundary.</b></p>""",
        """<p>Watch for the two separate problems this creates. One is about outliers; the other is that the output can exceed 1, which is meaningless for a yes/no answer.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>You want to predict whether a tumour is malignant. Answer: yes or no. Write yes as 1 and
no as 0, fit a straight line through the data, and call anything above 0.5 a yes.</p>
<p>It looks like it works. Then you add <b>one</b> more patient with a very large tumour — obviously
malignant, nothing surprising about it — and the line tilts, the 0.5 crossing point slides right, and
tumours you were correctly calling malignant are suddenly called benign.</p>
<p>Nothing about the disease changed. Only the maths broke.</p>""")

        + lenses(
            """<p>A doctor asked whether a lump is malignant. Not <b>how malignant</b> — the question has two
answers.</p>
<p>Fitting a straight line through yes-and-no answers produces predictions like 1.4 and −0.3, which are
not answers to the question that was asked. The tool is wrong for the job, and the failure is not
subtle once you look at it.</p>""",
            """<p>The technical problem is that a linear model is <b>unbounded</b>, and probabilities live in [0, 1].</p>
<p>Statisticians solve this with a link function, and the logistic link is the standard choice for binary
outcomes. If you have fitted a logit or probit model, this is that, arrived at from the other
direction.</p>""",
            """<p>The classic picture, and it is worth drawing yourself: data points at <var>y</var> = 0 and
<var>y</var> = 1, a fitted straight line running through them, and one new point far to the right.</p>
<p>Adding that single far-right point <b>rotates the line</b> and moves the decision boundary, changing
predictions for patients whose data did not change at all. That instability is the argument.</p>""",
            """<p>This lesson matters because linear regression on a binary outcome is a mistake people actually make,
and it does not announce itself.</p>
<p>The model trains, the loss decreases, and the errors are concentrated exactly where the stakes are
highest — at the extremes. Knowing the failure by sight is worth more than knowing the fix.</p>""",
            """So the next lesson's S-shaped curve is a direct response to the specific failure below.""")

        + h2("🎬", "Watch it move")
        + demo("classmotivation", "Press the button to add one large tumour",
               "count the misclassified points before and after")

        + h2("🔢", "The two problems")
        + grid2(
            card("<h3>1 · Unbounded output</h3><p>A straight line will happily predict −0.4 or 1.8. "
                 "Neither can be read as “is it malignant?”, and neither can be read as a probability. "
                 "The output has no meaning outside 0…1.</p>"),
            card("<h3>2 · Outliers move the boundary</h3><p>Squared error punishes the line for being "
                 "far from a point — even a point that is emphatically, unambiguously in one class. "
                 "So a clear-cut example drags the decision boundary. That is exactly backwards.</p>"))
        + key("""<p>The second problem is the deeper one. In classification, an example that is <b>very
obviously</b> in its class should barely influence the boundary at all. Squared error makes it influence
the boundary <em>most</em>.</p>""")

        + h2("🔬", "Binary classification vocabulary")
        + decode([
            ("binary classification", "“two classes”", "Exactly two possible outputs. The subject of this week."),
            ("class / category", "“the answer”", "Malignant or benign, spam or not, fraud or legitimate."),
            ("negative class (0)", "“the absence of the thing”", "Not spam, benign, no fraud. “Negative” does not mean bad — it means the thing is not there."),
            ("positive class (1)", "“the presence of the thing”", "Spam, malignant, fraud. Which class you call positive is your choice, and it matters for the metrics in Course 2."),
            ("decision boundary", "“the line between them”", "The set of inputs where the model switches from predicting 0 to predicting 1."),
        ])

        + h2("✅", "Check yourself")
        + quiz([
            ("Linear regression predicts −0.3 for a tumour. How do you interpret that?",
             "<p>You cannot. It is not a probability and it is not a class. The output is unbounded and "
             "therefore meaningless here — the first of the two problems.</p>"),
            ("Why should an obviously-malignant huge tumour NOT move the boundary?",
             "<p>Because it is unambiguous. It carries no information about where the difficult cases "
             "divide. Squared error does not know that, and treats “far from the line” as “badly "
             "fitted”.</p>"),
            ("Is “negative class” a value judgement?",
             "<p>No. It just means the thing being detected is absent. A benign tumour is the negative "
             "class and is obviously the better outcome.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("lab", REPO + "/week3/Optional%20Labs/C1_W3_Lab01_Classification_Soln.ipynb",
             "Optional lab: Classification",
             "In this repo. Shows exactly this failure interactively — add the outlier yourself and watch the boundary move."),
        ])
    )))

# ============================================================ 2
L.append(dict(
    slug="02-logistic-regression", title="Logistic regression", mins=16, tag="core",
    lede="Take the same wx + b and squash it through the sigmoid. The output becomes a probability, and "
         "both problems from the last lesson disappear.",
    body=(
        pretest("""<p>You need any number, however large, squashed into the range 0 to 1. <b>Sketch the shape a function would need to do that</b> — what must it do at very large positive and very large negative inputs?</p>""",
        """<p>Watch for g(0) = 0.5 exactly, and for why the curve flattening at the extremes is a feature rather than a flaw.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>The straight line was fine — it just went off to infinity in both directions.</p>
<p>So put it through a squasher. Whatever number comes out of wx + b, no matter how enormous, the squasher
turns it into something between 0 and 1. Very negative becomes almost 0. Very positive becomes almost 1.
Zero becomes exactly 0.5.</p>
<p>Now the output is a <b>chance</b>, which is exactly what you wanted all along.</p>""")

                + lenses(
            """<p>A door bouncer deciding entry. Everything about you feeds in — age, dress, sobriety, the length
of the queue — and one binary decision comes out. But internally he is not thinking in binary: he is
thinking “borderline”, “definitely fine”, “absolutely not”.</p>
<p>That inner confidence, squashed into a scale from 0 to 1, is what logistic regression produces.
The yes/no is only what happens at the very end, when a threshold is applied.</p>""",
            """<p>You may know this as the <b>logit model</b> — it is the workhorse of epidemiology, credit
scoring and political science, and it long predates machine learning.</p>
<p>What the sigmoid is doing is mapping the whole real line onto (0, 1) so that a linear score can be
read as a probability. In statistics that is expressed as modelling the log-odds linearly, which is
the same statement written from the other end.</p>""",
            """<p>A dimmer switch, not a light switch.</p>
<p>Linear regression gives you a number that can run off in either direction forever. The sigmoid
bends both ends of that line back, so however extreme the score, the output stays between fully off
and fully on — and sits at exactly half-way when the score is zero.</p>""",
            """<p>Credit scoring is logistic regression at industrial scale, and it is regulated precisely because
it is interpretable: a bank can be required to say which factors moved a decision, and this model can
answer.</p>
<p>That auditability is why it survives in high-stakes settings where a neural network would be
rejected — an argument for simple models that has nothing to do with accuracy.</p>""",
            """So the S-shaped curve below is a confidence dial, and the threshold that turns it into a decision
is a separate choice entirely.""")
        + h2("🎬", "Watch it move")
        + demo("logistic", "The sigmoid, and the sigmoid applied to tumour data",
               "drag w and b and watch the S-curve slide and steepen")

        + h2("🔢", "The maths, decoded")
        + eqp([
            ('<var>g</var>(<var>z</var>) <span class="op">=</span> <span class="frac"><span>1</span><span>1 <span class="op">+</span> <var>e</var><sup>−<var>z</var></sup></span></span>',
             "sigmoid-squash", "the squasher — click for what it does"),
        ], "the sigmoid (logistic) function")
        + eqp([
            '<var>z</var> <span class="op">=</span> ',
            ('<var class="hl-b">w⃗ · x⃗</var>', "dot-product-f0", "multiply matching entries, add them up"),
            ' <var class="hl-b">+ b</var> &nbsp;&nbsp;→&nbsp;&nbsp; <var>f</var>(<var>x</var>) <span class="op">=</span> ',
            ('<var>g</var>(<var>z</var>) <span class="op">=</span> <span class="frac"><span>1</span><span>1 + <var>e</var><sup>−(<var>w⃗·x⃗</var>+<var>b</var>)</sup></span></span>',
             "sigmoid-squash", "the same squasher, z filled in"),
        ], "the model — the old line, squashed — hover or click any part")
        + decode([
            ("<var>z</var>", "“zee”", "The raw output of the linear part. Any number at all. Often called the <b>logit</b>."),
            ("<var>e</var>", "“Euler’s number”", "About 2.71828. Its properties make the derivative come out unusually tidy — that is why it, rather than some other base."),
            ("<var>g</var>(<var>z</var>)", "“g of z”, the sigmoid", "The squasher. Always strictly between 0 and 1, never reaching either."),
            ("<var>f</var>(<var>x</var>)", "“the model output”", "A probability: P(y = 1 | x). Not a class — a chance."),
            ("g(0) = 0.5", "“the midpoint”", "Because e⁰ = 1, so 1/(1+1) = 0.5. This is why the decision boundary sits at z = 0."),
        ])

        + h2("🧮", "Sigmoid values worth knowing")
        + table(["z", "g(z)", "Read as"],
                [["−5", "0.007", "almost certainly class 0"],
                 ["−2", "0.12", "probably class 0"],
                 ["0", "<b>0.50</b>", "completely undecided"],
                 ["2", "0.88", "probably class 1"],
                 ["5", "0.993", "almost certainly class 1"]])
        + key("""<p>Read the output as <b>P(y = 1 | x; w, b)</b> — “the probability that y is 1, given this
input x, with these parameters w and b”. If f(x) = 0.7 then there is a 70% chance of malignant and,
necessarily, a 30% chance of benign.</p>""")

        + h2("🔬", "How this fixes both problems")
        + """<ul>
<li><b>Unbounded output:</b> gone by construction. The sigmoid cannot return anything outside 0…1.</li>
<li><b>Outliers moving the boundary:</b> largely gone too. Push a point far to the right and z becomes very
large, but g(z) is already ≈ 0.999 and barely moves. The sigmoid has <em>saturated</em>, so extra distance
costs almost nothing — which is precisely the behaviour you wanted.</li>
</ul>"""
        + note("""<p>The name is a historical accident. It is called logistic <b>regression</b> and it is a
<b>classification</b> algorithm. The “logistic” part comes from the logistic function, which was named in
the 1840s while modelling population growth. Everyone finds this confusing once and then stops noticing.</p>""",
               "About the name")

        + h2("💻", "In code")
        + code("""
def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def predict(X, w, b):
    z = np.dot(X, w) + b
    return sigmoid(z)              # probabilities, one per row
""")

        + h2("✅", "Check yourself")
        + quiz([
            ("w = 1, b = −3, x = 2. What is z, and what is f(x)?",
             "<p>z = 1(2) − 3 = <b>−1</b>. g(−1) = 1/(1 + e¹) ≈ <b>0.27</b> — probably benign.</p>"),
            ("f(x) = 0.7. What is the probability the tumour is benign?",
             "<p><b>0.3.</b> The two probabilities must sum to 1, so P(y=0) = 1 − 0.7.</p>"),
            ("Can the sigmoid ever output exactly 0 or exactly 1?",
             "<p>Mathematically no — it approaches them asymptotically. In floating point it can round to "
             "them, which causes the log(0) problem that Course 2 Week 2 lesson 9 is about.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("lab", REPO + "/week3/Optional%20Labs/C1_W3_Lab02_Sigmoid_function_Soln.ipynb",
             "Optional lab: Sigmoid Function",
             "In this repo. Plots it, and applies it to the tumour data."),
            ("docs", "https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression",
             "scikit-learn — LogisticRegression",
             "The production version. Note that it regularises by default (C = 1.0), which is the subject of the end of this week."),
        ])
    )))

# ============================================================ 3
L.append(dict(
    slug="03-decision-boundary", title="The decision boundary", mins=10, tag="maths",
    lede="Where the model changes its mind. It is always the line z = 0 — but what that looks like in your "
         "data depends entirely on which features you supplied.",
    body=(
        pretest("""<p>The model outputs 0.5. <b>What does that say about the input — and what is special about the set of all inputs that produce exactly 0.5?</b></p>""",
        """<p>Watch for the chain: f ≥ 0.5 means g(z) ≥ 0.5 means z ≥ 0. The boundary is where z is exactly zero.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>The model gives you a probability. At some point you have to actually decide.</p>
<p>The usual rule: if the chance is 0.5 or more, say yes. Below that, say no.</p>
<p>Now here is the neat bit. The sigmoid is exactly 0.5 when z = 0. So the place where the model changes
its mind is simply <b>wherever z = 0</b> — and z is just the old straight-line formula. The boundary is a
line, and you already know how to draw it.</p>""")

        + lenses(
            """<p>A fence across a field. On one side the animals are sheep, on the other they are goats.</p>
<p>The fence is not the animals and it is not a rule about any one animal. It is a line you can draw such
that what falls either side is mostly one kind, and the model's whole job is to place it.</p>""",
            """<p>The boundary is where <var>z</var> = 0, equivalently where the predicted probability is exactly
0.5.</p>
<p>Anyone who has worked with hyperplanes or with SVMs will recognise the object: a linear boundary in
feature space, and a set of points that the model is genuinely undecided about.</p>""",
            """<p>A scatter of two-coloured points with a straight line through them.</p>
<p>Everything on one side is predicted 1, everything on the other 0. Points near the line are the uncertain
ones, and the sigmoid gives them probabilities near 0.5 — which is exactly the information you want about
a borderline case.</p>""",
            """<p>The important nuance is that the boundary is linear <b>in the features you supply</b>.</p>
<p>Add <var>x</var>₁² and <var>x</var>₂² as columns and the boundary becomes a circle in the original
space, while remaining a straight line in the expanded one. That single trick is how a linear classifier
handles non-linear problems, and it is the same move as polynomial regression last week.</p>""",
            """So the boundary below is where <var>z</var> crosses zero, and its shape is decided by which columns
you handed the model.""")

        + h2("🎬", "Watch it move")
        + demo("decisionboundary", "Linear features, then polynomial features",
               "the shaded regions are what the model predicts everywhere")

        + h2("🔢", "The maths, decoded")
        + eqp([
            ('<var>f</var>(<var>x</var>) <span class="op">≥</span> 0.5', "func-f", "the model's output"),
            ' &nbsp;↔&nbsp; ',
            ('<var>g</var>(<var>z</var>) <span class="op">≥</span> 0.5', "sigmoid-squash", "the sigmoid"),
            ' &nbsp;↔&nbsp; <var class="hl-a"><var>z</var> <span class="op">≥</span> 0</var> &nbsp;↔&nbsp; ',
            ('<var>w⃗ · x⃗ + b</var> <span class="op">≥</span> 0', "dot-product-f0", "multiply matching entries, add them up"),
        ], "predict 1 exactly when z ≥ 0 — hover or click a part", small=True)
        + decode([
            ("decision boundary", "“where it changes its mind”", "The set of x satisfying w·x + b = 0."),
            ("threshold 0.5", "“a choice, not a law”", "You can move it. Course 2 Week 3 shows when you should — for example when a missed cancer costs far more than a false alarm."),
            ("linear boundary", "“a straight line”", "What you get with the raw features x₁ and x₂. In three dimensions it is a plane; in n dimensions, a hyperplane."),
            ("non-linear boundary", "“a curve”", "What you get once you add polynomial features. The <em>model</em> is still linear in z."),
        ])
        + key("""<p>The shape of the boundary is a property of the <b>features you supply</b>, not of
logistic regression. Give it x₁ and x₂ and you can only get a straight line. Give it x₁² and x₂² and you
can get a circle. Give it enough terms and you can get almost anything — with all the overfitting risk that
implies.</p>""")

        + h2("🧮", "A worked boundary")
        + """<p>Suppose w₁ = 1, w₂ = 1, b = −3. The boundary is where:</p>
<p style="text-align:center"><code>x₁ + x₂ − 3 = 0</code>, i.e. <code>x₁ + x₂ = 3</code></p>
<p>That is a straight line through (3, 0) and (0, 3). Above and to the right of it, z &gt; 0 and the model
predicts 1. Below and to the left, it predicts 0.</p>
<p>Now change to w₁ = 1, w₂ = 1, b = −1 with features x₁² and x₂². The boundary is x₁² + x₂² = 1 — the unit
<b>circle</b>. Inside it the model predicts 0; outside, 1.</p>"""

        + explain("""<p>f ≥ 0.5 turned out to mean z ≥ 0. <b>Why does the messy sigmoid condition simplify to a statement about z alone?</b></p>""",
            """<p>Because the sigmoid is monotonic — it never goes back down. So “is g(z) above 0.5” is answerable from z alone, and since g(0) = 0.5 exactly, the threshold in z is exactly 0. The curve drops out entirely.</p>""")
        + h2("🕳", "Traps")
        + trap("""<p><b>Thinking a curved boundary means the model is non-linear.</b> It is linear in z
throughout. Only the features changed.</p>""")
        + trap("""<p><b>Assuming 0.5 is always right.</b> It is the default, not a requirement. It is the
right threshold when the two kinds of mistake cost the same, and they very often do not.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("w = [2, 3], b = −6. What is the decision boundary?",
             "<p>2x₁ + 3x₂ − 6 = 0, i.e. 2x₁ + 3x₂ = 6 — a straight line through (3, 0) and (0, 2).</p>"),
            ("You want a circular boundary. What features do you need?",
             "<p>x₁² and x₂². Then z = w₁x₁² + w₂x₂² + b, and z = 0 is an ellipse (a circle when "
             "w₁ = w₂).</p>"),
            ("f(x) = 0.49 and f(x) = 0.51. How different are these two predictions really?",
             "<p>Barely at all — the model is essentially undecided in both cases. Thresholding at 0.5 "
             "turns them into opposite answers, which is a good reason to keep the probability rather "
             "than only the class.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("lab", REPO + "/week3/Optional%20Labs/C1_W3_Lab03_Decision_Boundary_Soln.ipynb",
             "Optional lab: Decision Boundary",
             "In this repo. Plots the boundary for both linear and polynomial features."),
            ("play", "https://playground.tensorflow.org/",
             "TensorFlow Playground",
             "Set it to Classification, pick the circle dataset, and try with and without x² features. Two minutes, and very convincing."),
        ])
    )))

# ============================================================ 4
L.append(dict(
    slug="04-cost-function-for-logistic-regression", title="Cost function for logistic regression",
    mins=16, tag="maths",
    lede="Squared error worked beautifully in Week 1 and fails here. Understanding why is the point of this "
         "lesson.",
    body=(
        pretest("""<p>Squared error worked fine for regression. <b>Guess why it is a bad choice once the model output goes through a sigmoid.</b></p>""",
        """<p>Watch for the word “convex”, and for what a bumpy cost surface does to the guarantee you had in Week 1.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>You have a way to score a line: measure how far off each point is and square it. It
worked perfectly for house prices.</p>
<p>Try it here and you get a landscape full of bumps and dips instead of one clean bowl. Gradient descent
walks down into the nearest dip, stops, and announces it has finished — while a much better answer sits in
a different dip nearby.</p>
<p>So you need a different way of scoring. Not because squared error is wrong in principle, but because
the <b>shape</b> it produces here is unusable.</p>""")

        + lenses(
            """<p>Marking a forecaster who gives probabilities rather than answers. She said 90% rain and it rained —
a small penalty. She said 90% rain and it stayed dry — a large one.</p>
<p>The penalty has to punish <b>confident and wrong</b> far more harshly than <b>uncertain and wrong</b>,
or she will simply say 100% to everything.</p>""",
            """<p>Squared error is the obvious choice and it fails here for a reason worth knowing: with a sigmoid
inside it, the cost surface is <b>non-convex</b>, full of local minima that gradient descent gets stuck
in.</p>
<p>If you have hit a non-convex optimisation before, you know the symptom — the answer depends on where
you started. The logistic loss is chosen specifically to restore convexity.</p>""",
            """<p>Two curves, one for each true label.</p>
<p>When <var>y</var> = 1, the penalty is −log(<var>f</var>): almost nothing when <var>f</var> is near 1,
and rising to <b>infinity</b> as <var>f</var> approaches 0. That vertical asymptote is the mechanism —
being confidently wrong is unboundedly expensive.</p>""",
            """<p>The infinite penalty is the whole design, and it is why the model cannot game the loss by being
certain.</p>
<p>It is also why numerical implementations clip probabilities away from exactly 0 and 1: an actual
infinity in the loss makes every gradient NaN, and the whole model dies in one step. This is the same
concern that <code>from_logits</code> addresses in C2.</p>""",
            """So the log below is not a mathematical flourish. It is what makes confident errors unaffordable and
the surface convex.""")

        + h2("🎬", "Watch it move")
        + demo("logcost", "Bumpy versus bowl-shaped",
               "the same optimiser, two very different landscapes")

        + h2("🔢", "What went wrong")
        + """<p>In Week 1, f = wx + b, so (f − y)² was a quadratic in w and b — and quadratics are convex,
guaranteed.</p>
<p>Now f = g(wx + b), with a sigmoid in the middle. Squaring the error of a squashed function is
no longer convex in general — the guarantee is gone, and where you end up can depend on where you
started.</p>
<p>Two honest caveats, because they matter for what you will actually see. Losing the guarantee does not
mean every data set produces a visibly bumpy surface; small problems often have just one minimum anyway.
And the failure you are most likely to meet is not a wrong valley at all — it is gradient descent
barely moving, for the reason worked out further down this page.</p>"""
        + decode([
            ("convex", "“one bowl”", "Exactly one minimum. Gradient descent with a small enough α always finds it."),
            ("non-convex", "“many valleys”", "Several local minima. Where you end up depends on where you began."),
            ("loss", "“the error on ONE example”", "Written L(f, y). This is what needs redesigning."),
            ("cost", "“the average loss over all m examples”", "Written J(w, b). J = (1/m) Σ L. Note there is no 1/2 here — there is no square to differentiate."),
        ])
        + warn("""<p><b>Loss</b> and <b>cost</b> are used interchangeably in a lot of writing, and this
course keeps them distinct on purpose: loss is per-example, cost is the average. Course 2 relies on the
distinction, and interviewers ask about it.</p>""")

        + h2("🔢", "The new loss")
        + eqp([
            '<var>L</var>(<var>f</var>, <var>y</var>) <span class="op">=</span> <span class="paren">{</span> ',
            ('<span class="op">−</span>log(<var>f</var>)', "logarithm-f0", "huge penalty if f is near 0"),
            ' &nbsp;&nbsp; if <var>y</var> = 1<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ',
            ('<span class="op">−</span>log(1 <span class="op">−</span> <var>f</var>)', "logarithm-f0", "huge penalty if f is near 1"),
            ' &nbsp;&nbsp; if <var>y</var> = 0',
        ], "the logistic loss — hover or click a part")
        + """<p>Two cases, and only one is ever active for any given example. The next lesson looks at the
shape of these curves in detail; the point here is simply that this loss makes J <b>convex</b> again, and
gradient descent gets its guarantee back.</p>"""
        + key("""<p>Why a logarithm specifically? Two reasons, both good. It makes the overall cost convex.
And it is the <b>negative log-likelihood</b> — the choice of w and b that makes the data you actually
observed most probable. It is not an arbitrary trick; it falls out of statistics.</p>""")

        + h2("🧮", "Watch squared error actually fail")
        + """<p>The claim is that squared error, which worked perfectly for linear regression, breaks
for logistic regression. Here it is failing. Six points, a sigmoid model, and gradient descent run
from a deliberately poor start (<var>w</var> = −5, <var>b</var> = 10) for 3,000 steps:</p>"""
        + table(["cost function used", "ends at", "final accuracy"],
                [["squared error", "w = −9.30, b = 3.51", "<b>0.33</b> — worse than guessing"],
                 ["log loss", "w = 7.11, b = −17.60", "<b>1.00</b> — solved"]])
        + """<p>Same data, same start, same α, same number of steps. One gets there; the other is
still stuck 3,000 iterations later.</p>
<p>The mechanism is in the derivative. With squared error the gradient carries an extra factor of
<var>g</var>′(<var>z</var>) = <var>g</var>(1 − <var>g</var>), and that factor collapses when the
sigmoid saturates — at <var>z</var> = ±5 it is already about 0.007, at ±10 it is 0.00005. A badly
placed model is <em>confidently</em> wrong, which is exactly where the gradient dies, so it receives
almost no signal to correct itself.</p>
<p>Log loss is built so that factor cancels. Its gradient is simply
(<var>f</var> − <var>y</var>)<var>x</var> — no <var>g</var>′ anywhere — so a confidently wrong
prediction produces a <em>large</em> correction rather than a vanishing one.</p>"""
        + explain("""<p>The cure is a cost function whose derivative cancels the sigmoid’s slope.
<b>Why is “confidently wrong should hurt most” the right principle to build in?</b></p>""",
                  """<p>Because the model’s output is a probability, and a probability of 0.99
attached to a wrong answer is a much more serious error than 0.51 attached to the same wrong answer —
it means the model has learned something actively false, not merely that it is undecided. Squared
error caps the penalty at 1 and, worse, flattens the gradient exactly there. Log loss sends the
penalty to infinity as the prediction approaches certainty in the wrong direction, so the steepest
correction is applied precisely where the model is most badly wrong.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("Why is squared error non-convex for logistic regression?",
             "<p>Because f now contains a sigmoid. Squaring the error of a squashed function produces a "
             "surface with multiple local minima rather than a single bowl.</p>"),
            ("What does “convex” buy you, concretely?",
             "<p>A guarantee: gradient descent with a small enough α reaches the global minimum from any "
             "starting point. No dependence on initialisation, no local minima to worry about.</p>"),
            ("What is the difference between loss and cost, in this course's usage?",
             "<p><b>Loss</b> is the error on one example. <b>Cost</b> J is the average loss over all m "
             "examples — the thing you actually minimise.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("lab", REPO + "/week3/Optional%20Labs/C1_W3_Lab04_LogisticLoss_Soln.ipynb",
             "Optional lab: Logistic Loss",
             "In this repo. Plots the squared-error surface and the logistic one side by side. The difference is obvious once you see it."),
            ("book", "https://www.deeplearningbook.org/contents/ml.html",
             "Deep Learning — chapter 5.5, maximum likelihood",
             "Where the log loss comes from. It is the negative log-likelihood, not an invention."),
        ])
    )))

# ============================================================ 5
L.append(dict(
    slug="05-logistic-loss", title="The logistic loss, in detail", mins=14, tag="maths",
    lede="Two curves that between them encode a strong opinion: being confident and wrong should cost you "
         "enormously.",
    body=(
        pretest("""<p>The true answer is 1 and your model says 0.01 — confidently wrong. <b>How much should that cost, compared with saying 0.5 and admitting you do not know?</b></p>""",
        """<p>−log(0.01) is about 4.6; −log(0.5) is about 0.69. Watch for why the penalty must grow without limit as confidence in the wrong answer rises.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>A game where you announce how sure you are, and get penalty points for being wrong.</p>
<p>The rule is harsh but fair. Say “99% sure it’s malignant” about a benign tumour and you pay a fortune.
Say “55% sure” about the same tumour and you pay very little.</p>
<p>The more confident you were, the more it costs when you turn out to be wrong. And if you were confident
and <em>right</em>, you pay almost nothing.</p>""")

                + lenses(
            """<p>A weather forecaster who says “100% chance of sun” on a day it pours.</p>
<p>That is a far worse failure than saying “60% chance” and being wrong, and everyone feels the
difference instinctively. Confidence has to be paid for: if you claim certainty and are wrong, the
penalty should be severe. If you hedge, you lose a little either way.</p>""",
            """<p>This is the negative log-likelihood, and it is not an arbitrary choice — it is what
<b>maximum likelihood estimation</b> produces for a Bernoulli outcome.</p>
<p>In other words, minimising this loss means choosing the parameters that make the data you actually
observed as probable as possible. The formula is a consequence of that principle, not a design
decision someone made for convenience.</p>""",
            """<p>A curve that dives towards negative infinity as the predicted probability approaches zero.</p>
<p>Get it right with confidence and the cost is a hair above zero. Hedge at 0.5 and you pay 0.69
every time. Be certain and wrong, and the cost runs away without limit. That vertical wall on the
left is the entire mechanism.</p>""",
            """<p>This is why calibrated probability matters in deployment. A medical model that says “90%
likely malignant” must be right about nine times in ten when it says that, or clinicians cannot use
the number at all.</p>
<p>Log loss is what trains a model to be honest about its own uncertainty — accuracy alone would let
it be confidently wrong for free.</p>""",
            """So the values below are worth having a feel for: 0.69 is a shrug, and anything above about 3 is a
confident mistake.""")
        + h2("🎬", "Watch it move")
        + demo("logloss", "Drag the prediction, switch the true answer",
               "the loss climbs towards infinity as you become confidently wrong")

        + h2("🔢", "The two cases")
        + table(["If the truth is…", "the loss is…", "f near 0", "f = 0.5", "f near 1"],
                [["<b>y = 1</b>", "−log(f)", "→ ∞ (terrible)", "0.69", "→ 0 (perfect)"],
                 ["<b>y = 0</b>", "−log(1 − f)", "→ 0 (perfect)", "0.69", "→ ∞ (terrible)"]])
        + decode([
            ("−log(f)", "“minus log f”", "Zero when f = 1, and shooting to infinity as f → 0. Exactly the penalty structure you want when the truth is 1."),
            ("log", "“natural log”", "Base e. Its job here is turning a tiny probability into a huge penalty: log(0.001) = −6.9."),
            ("the minus sign", "“flip it positive”", "Logs of numbers below 1 are negative; the minus makes the loss positive, so bigger means worse."),
            ("0.69", "“the coin-flip loss”", "−log(0.5) = 0.693. A useful reference point: any model doing better than 0.69 average loss is doing better than guessing."),
        ])
        + key("""<p>The asymmetry is the whole design. The loss for a correct confident answer approaches
zero; the loss for an incorrect confident answer approaches <b>infinity</b>. This is what forces the model
to be honest about uncertainty rather than always shouting.</p>""")

        + h2("🧮", "Numbers worth having a feel for")
        + """<ul>
<li>y = 1, f = 0.99 → −log(0.99) = <b>0.01</b>. Confident and right: essentially free.</li>
<li>y = 1, f = 0.5 → −log(0.5) = <b>0.69</b>. Hedging: a moderate cost.</li>
<li>y = 1, f = 0.1 → −log(0.1) = <b>2.30</b>. Wrong: expensive.</li>
<li>y = 1, f = 0.01 → −log(0.01) = <b>4.61</b>. Confidently wrong: very expensive.</li>
</ul>
<p>Note how the cost accelerates. Going from 0.5 to 0.1 roughly triples the loss; going from 0.1 to 0.01
doubles it again.</p>"""

        + h2("🔬", "Why this makes J convex")
        + """<p>The informal reason: −log(f) is a convex function of f, and f = g(z) composed with the log
turns out to be convex in z. Adding convex functions preserves convexity, so the average over all m
examples is convex too.</p>
<p>The formal proof involves showing the second derivative is non-negative everywhere, and it is not needed
to use the result. What is worth taking away is that the sigmoid and the log loss are a matched pair —
pairing the sigmoid with squared error, or the log loss with a different activation, loses the
property.</p>"""

        + h2("✅", "Check yourself")
        + quiz([
            ("y = 0 and f = 0.9. What is the loss?",
             "<p>−log(1 − 0.9) = −log(0.1) = <b>2.30</b>. Confidently wrong, and priced accordingly.</p>"),
            ("y = 1 and f = 0.999. What is the loss?",
             "<p>−log(0.999) ≈ <b>0.001</b>. Confident and right — almost nothing.</p>"),
            ("Why does the loss go to infinity rather than plateauing at some large value?",
             "<p>Because the model claimed something true was essentially impossible. An infinite penalty "
             "is the honest price of infinite confidence in a falsehood — and it makes the gradient large "
             "exactly where a big correction is needed.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("lab", REPO + "/week3/Optional%20Labs/C1_W3_Lab04_LogisticLoss_Soln.ipynb",
             "Optional lab: Logistic Loss",
             "In this repo. Both curves, plotted and explorable."),
            ("docs", "https://scikit-learn.org/stable/modules/model_evaluation.html#log-loss",
             "scikit-learn — log loss",
             "The same quantity, used as an evaluation metric. Useful when you want to score probabilities rather than classes."),
        ])
    )))

# ============================================================ 6
L.append(dict(
    slug="06-simplified-cost-function", title="The simplified cost function", mins=13, tag="maths",
    lede="Two cases collapse into one line, using nothing more than the fact that y is always 0 or 1.",
    body=(
        pretest("""<p>Two formulas, one for y = 1 and one for y = 0. <b>Guess how you would collapse them into a single line with no <code>if</code></b>, given y is only ever 0 or 1.</p>""",
        """<p>Try multiplying one by y and the other by (1 − y). Watch which term vanishes in each case.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>You have two rules: one for when the answer is yes, one for when it is no. Awkward to
write, awkward to code, awkward to differentiate.</p>
<p>Trick: multiply the first rule by y and the second by (1 − y). Since y is only ever 0 or 1, one of those
multipliers is always <b>zero</b>, so one of the two terms always vanishes.</p>
<p>Two rules, one formula, no <code>if</code> statement.</p>""")

        + lenses(
            """<p>Two rules written as one line, using the fact that one of the two terms always switches itself off.</p>
<p>A small piece of algebraic housekeeping with a real payoff: code with no <code>if</code> in the inner
loop, and a formula that vectorises across a whole dataset at once.</p>""",
            """<p>The trick is multiplying by <var>y</var> and (1 − <var>y</var>) so that exactly one term survives,
and it is the standard way to write a two-case function as one expression.</p>
<p>Anyone who has used an indicator variable to collapse a piecewise definition has done exactly this.</p>""",
            """<p>The single line, with the two halves covered in turn.</p>
<p>Set <var>y</var> = 1 and the second term vanishes. Set <var>y</var> = 0 and the first does. Do that
substitution on paper once and the formula stops looking like something to memorise.</p>""",
            """<p>This expression is <b>binary cross-entropy</b>, and it is the same object you will meet in C2 for
neural networks and in C3 for recommenders with binary labels.</p>
<p>Learning it properly once here is worth a great deal later, because it is the loss function you will
use most often in the whole specialization.</p>""",
            """So the one line below is the two-case rule from the previous lesson, folded together.""")

        + h2("🎬", "Watch it move")
        + demo("simplifiedcost", "The two terms, and one of them disappearing",
               "watch which half survives as the true label flips")

        + h2("🔢", "The maths, decoded")
        + eqp([
            '<var>L</var>(<var>f</var>, <var>y</var>) <span class="op">=</span> ',
            ('<span class="op">−</span><var class="hl-a">y</var> log(<var>f</var>) <span class="op">−</span> (1 <span class="op">−</span> <var class="hl-a">y</var>) log(1 <span class="op">−</span> <var>f</var>)',
             "logloss-native", "the two-case trick, in one line"),
        ], "the same loss, written without a case split — hover or click it")
        + """<p>Check both cases:</p>
<ul>
<li><b>y = 1:</b> −1·log(f) − (1−1)·log(1−f) = −log(f) − 0 = <b>−log(f)</b> ✓</li>
<li><b>y = 0:</b> −0·log(f) − (1−0)·log(1−f) = 0 − log(1−f) = <b>−log(1−f)</b> ✓</li>
</ul>
<p>Nothing has changed. It is the identical loss with the branching hidden inside the arithmetic.</p>"""
        + eqp([
            ("<var>J</var>(<var>w⃗</var>, <var>b</var>)", "cost-j", "the cost"),
            ' <span class="op">=</span> <span class="op">−</span>',
            ('<span class="frac"><span>1</span><span><var>m</var></span></span>', "avg-factor", "the average"),
            ('<span class="big">Σ</span><sub><var>i</var>=1</sub><sup><var>m</var></sup>', "sigma", "for every example"),
            ('<span class="paren">[</span> <var>y</var><sup>(<var>i</var>)</sup> log(<var>f</var>(<var>x</var><sup>(<var>i</var>)</sup>))'
             ' <span class="op">+</span> (1 <span class="op">−</span> <var>y</var><sup>(<var>i</var>)</sup>) log(1 <span class="op">−</span> <var>f</var>(<var>x</var><sup>(<var>i</var>)</sup>)) <span class="paren">]</span>',
             "logloss-native", "the two-case trick, in one line"),
        ], "and the cost is the average over all m examples — hover or click any part")
        + decode([
            ("binary cross-entropy", "“the standard name”", "What this loss is called everywhere outside this course. You will use it for every binary classifier in Course 2."),
            ("no 1/2", "“note its absence”", "The 1/2 in Week 1’s cost existed only to cancel the 2 from differentiating a square. There is no square here."),
            ("the minus outside", "“applied to the whole sum”", "Both log terms are negative (logs of numbers below 1), so one minus at the front makes J positive."),
        ])
        + key("""<p>This is <b>binary cross-entropy</b>. You will meet it again in Course 2 Week 2 as the
loss for a neural network classifier, and in Course 3 Week 2 for recommender systems with binary labels.
It is the same formula every time.</p>""")

        + h2("💻", "In code")
        + code("""
def compute_cost_logistic(X, y, w, b):
    m = X.shape[0]
    f = sigmoid(np.dot(X, w) + b)                   # (m,) probabilities
    cost = -y * np.log(f) - (1 - y) * np.log(1 - f) # (m,) losses
    return np.sum(cost) / m
""")
        + warn("""<p>That code will produce <code>-inf</code> if f ever rounds to exactly 0 or 1. Real
implementations clip f into [1e−15, 1 − 1e−15], or rearrange the formula to avoid building f at all.
Course 2 Week 2 lesson 9 covers this properly under the name <code>from_logits=True</code>.</p>""")

        + h2("🧮", "Checking that one line really is two")
        + """<p>The two-case loss and the one-line version are claimed to be identical. The way to
believe it is to substitute both possible values of <var>y</var>:</p>"""
        + table(["y", "−y log(f) − (1−y) log(1−f)", "collapses to"],
                [["1", "−<b>1</b>·log(f) − <b>0</b>·log(1−f)", "<b>−log(f)</b>"],
                 ["0", "−<b>0</b>·log(f) − <b>1</b>·log(1−f)", "<b>−log(1−f)</b>"]])
        + """<p>Because <var>y</var> is only ever 0 or 1, one of the two terms is always multiplied by
zero and vanishes. It is an <b>if-statement written as arithmetic</b>. The numbers:</p>"""
        + table(["f", "loss if y = 1", "loss if y = 0"],
                [["0.90", "<b>0.105</b>", "2.303"],
                 ["0.50", "0.693", "0.693"],
                 ["0.10", "2.303", "<b>0.105</b>"],
                 ["0.01", "<b>4.605</b>", "0.010"]])
        + """<p>The reason to bother: an <code>if</code> cannot be differentiated or vectorised, and a
product can. This single expression is what lets the cost be written as one NumPy line over the whole
data set, and it is why the derivative comes out as cleanly as it does in the next lesson.</p>"""
        + explain("""<p>The trick relies entirely on <var>y</var> being exactly 0 or 1. <b>What breaks
if y could be 0.5?</b></p>""",
                  """<p>Neither term vanishes, so you get a blend — 0.5 of the y=1 loss plus 0.5 of the
y=0 loss. Interestingly that is not nonsense: it is the cross-entropy between the true distribution
and the predicted one, and it is exactly what soft labels and label smoothing use deliberately. So
the formula generalises gracefully; what stops being true is the <em>reading</em> of it as “pick one
of two cases”. With 0/1 labels it is a switch; in general it is a weighted average.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("Show the combined formula reduces to −log(f) when y = 1.",
             "<p>−1·log(f) − (1−1)·log(1−f) = −log(f) − 0·log(1−f) = <b>−log(f)</b>. The second term is "
             "multiplied by zero.</p>"),
            ("Why is there no 1/2 in the logistic cost?",
             "<p>Because the 1/2 in the squared-error cost existed only to cancel the 2 that appears when "
             "you differentiate a square. There is no square here, so nothing to cancel.</p>"),
            ("What is this loss called outside this course?",
             "<p><b>Binary cross-entropy</b>, or sometimes just log loss. Same formula, three names.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("lab", REPO + "/week3/Optional%20Labs/C1_W3_Lab05_Cost_Function_Soln.ipynb",
             "Optional lab: Cost Function for Logistic Regression",
             "In this repo. Implements the combined formula and plots J over the parameter space."),
            ("docs", "https://www.tensorflow.org/api_docs/python/tf/keras/losses/BinaryCrossentropy",
             "tf.keras.losses.BinaryCrossentropy",
             "The same loss, as you will use it in Course 2."),
        ])
    )))

# ============================================================ 7
L.append(dict(
    slug="07-gradient-descent-logistic", title="Gradient descent for logistic regression", mins=14, tag="core",
    lede="The update rule is character-for-character identical to linear regression. Only the meaning of f "
         "has changed — and that is genuinely all.",
    body=(
        pretest("""<p>New model, new cost function. <b>Guess how much the gradient descent update rule has to change.</b></p>""",
        """<p>The answer surprises people. Watch for what stays character-for-character identical, and for the one definition that quietly changed underneath it.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>You changed the model. You changed the cost. And when you work out the derivative, you
get… exactly the same formula as before.</p>
<p>It looks like a mistake. It is not. The sigmoid and the log loss are built to fit together, and when you
compose them the messy bits cancel out perfectly.</p>""")

        + lenses(
            """<p>The same fog-walk down the same kind of hill. Different scoring function, identical procedure.</p>
<p>And there is a genuine surprise waiting: the update rule comes out looking exactly like the one from
linear regression, which is either a coincidence or a sign that something deeper is going on. It is the
second.</p>""",
            """<p>The derivative of the logistic loss with respect to <var>w</var><sub>j</sub> is the <b>same
expression</b> as for squared error in linear regression: (<var>f</var> − <var>y</var>)
<var>x</var><sub>j</sub>.</p>
<p>This is not an accident — it holds for any generalised linear model with its canonical link, and the
logs and exponentials cancel exactly. Worth knowing, because it means one implementation serves
both.</p>""",
            """<p>Two update rules written one above the other, identical character for character.</p>
<p>The only difference is hidden inside <var>f</var>: a dot product in one case, a sigmoid of a dot product
in the other. Same algorithm, different model plugged in.</p>""",
            """<p>The practical consequences carry across too: feature scaling still helps for the same reason, the
learning-curve diagnostics still apply, and simultaneous update is still mandatory.</p>
<p>Everything you learned in Weeks 1 and 2 about running gradient descent transfers without
modification, which is the real payoff of the identical form.</p>""",
            """So the update below looks familiar because it genuinely is the same, with <var>f</var> redefined.""")

        + h2("🎬", "Watch it move")
        + demo("gdlogistic", "The same update, a different f",
               "the formula is identical; only what f means has changed")

        + h2("🔢", "The maths, decoded")
        + eqp([
            ('<var>w</var><sub><var>j</var></sub> <span class="op">:=</span>', "assign-op", "becomes, not equals"),
            ' <var>w</var><sub><var>j</var></sub> <span class="op">−</span> ',
            ('<var>α</var>', "alpha-lr", "the learning rate"),
            ' ',
            ('<span class="frac"><span>1</span><span><var>m</var></span></span>', "avg-factor", "the average"),
            ('<span class="big">Σ</span>', "sigma", "for every example"),
            (' <span class="paren">(</span> <var class="hl-a"><var>f</var>(<var>x⃗</var><sup>(<var>i</var>)</sup>)</var> <span class="op">−</span> <var>y</var><sup>(<var>i</var>)</sup> <span class="paren">)</span>',
             "error-term", "predicted − actual"),
            ('<var>x</var><sub><var>j</var></sub><sup>(<var>i</var>)</sup>', "times-xi", "only in the wⱼ-derivative"),
        ], "identical to Week 2 — except for what f is — hover or click a part")
        + table(["", "Linear regression", "Logistic regression"],
                [["the model f", "<code>w·x + b</code>", "<code>g(w·x + b)</code>"],
                 ["the cost J", "squared error", "log loss"],
                 ["the update rule", "as above", "<b>exactly as above</b>"]])
        + key("""<p>Same rule, different f. That is the whole difference. Everything you learned about
gradient descent in Weeks 1 and 2 — simultaneous updates, feature scaling, plotting J against iterations,
choosing α by trying a ladder — <b>carries over unchanged</b>.</p>""")

        + h2("🔬", "Is the identical formula a coincidence?")
        + """<p>No, and it is worth knowing why. The sigmoid has a remarkably tidy derivative:
g′(z) = g(z)(1 − g(z)). When you differentiate the log loss through the sigmoid, that factor cancels
exactly against the 1/f and 1/(1−f) coming from the logarithm.</p>
<p>Pair the sigmoid with squared error instead and the cancellation does not happen — you get an extra
g′(z) factor that shrinks the gradient to nearly zero exactly where the model is confidently wrong. Which
is the worst possible place for the gradient to vanish.</p>
<p>So the tidy formula is a symptom of a well-matched pair, not an accident. This same pairing logic
reappears in Course 2 with softmax and cross-entropy.</p>"""

        + h2("💻", "In code")
        + code("""
def compute_gradient_logistic(X, y, w, b):
    m = X.shape[0]
    f = sigmoid(np.dot(X, w) + b)      # <- the ONLY line that differs
    err = f - y
    dj_dw = np.dot(X.T, err) / m
    dj_db = np.sum(err) / m
    return dj_dw, dj_db
""")
        + """<p>Diff this against the linear regression version from Week 2 and exactly one line
changes.</p>"""

        + h2("🧮", "The identical formula, checked")
        + """<p>The derivative of the logistic cost is:</p>"""
        + eq("""<span class="frac"><span>∂<var>J</var></span><span>∂<var>w</var><sub>j</sub></span></span>
<span class="op">=</span> <span class="frac"><span>1</span><span><var>m</var></span></span>
<span class="op">Σ</span> <span class="paren">(</span><var>f</var>(<var>x</var><sup>(i)</sup>)
<span class="op">−</span> <var>y</var><sup>(i)</sup><span class="paren">)</span>
<var>x</var><sub>j</sub><sup>(i)</sup>""", "exactly what linear regression had")
        + """<p>Character for character, this is the linear regression update from Week 1. Only
<var>f</var> has changed — from <var>w</var>·<var>x</var> + <var>b</var> to
<var>g</var>(<var>w</var>·<var>x</var> + <var>b</var>). Worked on the six-point data with
<var>w</var> = [1, 1], <var>b</var> = −3:</p>"""
        + table(["x", "y", "z", "f = g(z)", "f − y"],
                [["[0.5, 1.5]", "0", "−1.0", "0.2689", "+0.2689"],
                 ["[1.0, 1.0]", "0", "−1.0", "0.2689", "+0.2689"],
                 ["[1.5, 0.5]", "0", "−1.0", "0.2689", "+0.2689"],
                 ["[3.0, 0.5]", "1", "+0.5", "0.6225", "−0.3775"],
                 ["[2.0, 2.0]", "1", "+1.0", "0.7311", "−0.2689"],
                 ["[1.0, 2.5]", "1", "+0.5", "0.6225", "−0.3775"]])
        + """<p>All six are classified correctly, yet every residual is substantial — the model is
right but not confident, so gradient descent keeps pushing. Positive residuals pull the weights down,
negative ones push them up, each in proportion to its own <var>x</var>.</p>"""
        + warn("""<p>The formula being identical does <b>not</b> make the algorithms identical. The
same expression means different things because <var>f</var> is different, J is a different function,
and the two cannot be swapped. It is a lucky coincidence of the maths, not a shared
implementation.</p>""")
        + explain("""<p>Two quite different models and two quite different cost functions produce
literally the same derivative. <b>Is that a coincidence?</b></p>""",
                  """<p>No — it is designed. Log loss was chosen partly <em>because</em> its derivative
cancels the sigmoid’s <var>g</var>′ factor, which is the same cancellation that rescued the previous
lesson’s stuck gradient descent. Squared error paired with an identity function does the same thing
for linear regression. Both are instances of a general pattern: pair the right loss with the right
output function and the messy chain-rule factor disappears, leaving (prediction − target) × input.
The same form shows up again for softmax in Course 2.</p>""")

        + h2("🔤", "The words, decoded")
        + decode([
            ("gradient", "“gradient”", "The vector of all the partial derivatives — one per parameter. Points uphill; you step the other way."),
            ("partial derivative", "“partial d J by d w”", "How much J changes when you nudge <em>one</em> parameter, holding the rest still. Written ∂J/∂w."),
            ("simultaneous update", "“update together”", "Compute every derivative from the <b>old</b> parameters, then assign. Updating one before computing the next is the classic bug."),
            ("chain rule", "“chain rule”", "How to differentiate a function inside a function. It is why the sigmoid's own slope shows up in the derivative — and why the log loss is built to cancel it."),
        ])
        + h2("✅", "Check yourself")
        + quiz([
            ("What is the only difference between the two gradient computations?",
             "<p>The definition of f: <code>np.dot(X, w) + b</code> becomes "
             "<code>sigmoid(np.dot(X, w) + b)</code>. One line.</p>"),
            ("Does feature scaling still help here?",
             "<p><b>Yes</b>, for exactly the same reason — it makes the cost surface rounder and lets you "
             "use a larger α.</p>"),
            ("Why would pairing the sigmoid with squared error be a bad idea beyond non-convexity?",
             "<p>The gradient would pick up an extra g′(z) factor, which is near zero when the model is "
             "confidently wrong. Learning would stall precisely where the biggest correction is needed.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("lab", REPO + "/week3/Optional%20Labs/C1_W3_Lab06_Gradient_Descent_Soln.ipynb",
             "Optional lab: Gradient Descent for Logistic Regression",
             "In this repo. The full implementation, with the decision boundary updating as it trains."),
            ("lab", REPO + "/week3/Optional%20Labs/C1_W3_Lab07_Scikit_Learn_Soln.ipynb",
             "Optional lab: Logistic Regression with scikit-learn",
             "The three-line production version, to compare against yours."),
        ])
    )))

# ============================================================ 8
L.append(dict(
    slug="08-the-problem-of-overfitting", title="The problem of overfitting", mins=20, tag="core",
    lede="The most important concept in applied machine learning, and the first place you meet it. A model "
         "that is perfect on your data and useless on anything else.",
    body=(
        pretest("""<p>A model scores 100% on the data it trained on. <b>Is that good news?</b> Commit before reading.</p>""",
        """<p>Watch for the difference between fitting and learning, and for the two named failure modes at either extreme.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Two ways to be a bad student.</p>
<p><b>Too simple:</b> you only ever learned “the answer is always 4”. You get the homework wrong and the
exam wrong. You are not confused — you are under-prepared. That is <b>underfitting</b>.</p>
<p><b>Too clever:</b> you memorised last year’s paper word for word. Perfect on it, hopeless on this
year’s. You didn’t learn the subject, you learned the paper. That is <b>overfitting</b>.</p>
<p>The awkward part: both look like “the model is bad”, and they need <em>opposite</em> fixes.</p>""")

                + lenses(
            """<p>A student who memorises last year’s exam paper word for word.</p>
<p>On that paper, perfect marks. On this year’s paper, which asks the same ideas in different words,
he is lost — because he never learned the ideas, only the answers. Meanwhile a student who only
skimmed the topic does badly on both.</p>
<p>Those two failures are opposites, they look identical from the outside (“bad marks”), and they need
opposite fixes. That is the whole lesson.</p>""",
            """<p>If you have fitted a model in any field, you know this as the <b>bias–variance trade-off</b>,
and the tell is the same everywhere: excellent in-sample fit, poor out-of-sample performance.</p>
<p>Econometrics calls the extreme version overparameterisation; a curve through <em>n</em> points
using <em>n</em> parameters explains everything and predicts nothing. The R² will be beautiful and
the forecast will be worthless.</p>""",
            """<p>Two lines drawn through the same scatter of dots.</p>
<p>One is a gentle curve that misses every point slightly. The other visits every single point exactly
— and to do so it swings wildly up and down between them. Ask both to predict a new point and the
wiggly one is wrong by a mile. The wiggle <em>is</em> the overfitting, drawn.</p>""",
            """<p>A hiring model trained on a company’s past hires learns the company’s past hiring habits,
including the ones nobody would defend out loud. It fits the historical data superbly.</p>
<p>Overfitting is not only a statistical failure; it is how a model ends up confidently reproducing
patterns that were never meant to be a rule. Which is why the fix — regularisation — matters well
beyond accuracy.</p>""",
            """So the two words below, underfitting and overfitting, are worth learning as opposites, because
every diagnostic in Course 2 is about telling them apart.""")
        + h2("🎬", "Watch it move")
        + demo("overfitting", "Three fits, and the same story for classification",
               "click between regression and classification — the pattern is identical")

        + h2("🔢", "The vocabulary")
        + table(["", "Underfitting", "Just right", "Overfitting"],
                [["also called", "<b>high bias</b>", "good generalisation", "<b>high variance</b>"],
                 ["on training data", "poor", "good", "<b>excellent</b>"],
                 ["on new data", "poor", "good", "<b>poor</b>"],
                 ["the model is", "too simple", "about right", "too flexible"],
                 ["the fix", "more features, more capacity", "—", "more data, fewer features, regularisation"]])
        + decode([
            ("overfitting", "“memorising”", "The model fits the training data almost perfectly, including its noise, and fails on anything new."),
            ("high variance", "“unstable”", "Retrain on a slightly different sample and you get a wildly different model. Hence “variance”."),
            ("underfitting", "“too simple to learn”", "The model cannot represent the pattern even in the data it has seen."),
            ("high bias", "“a strong preconception”", "The model insists the answer is a straight line no matter what the data says."),
            ("generalisation", "“doing well on new data”", "The only thing anybody actually cares about."),
        ])
        + key("""<p><b>Training performance is not the goal.</b> A model that gets 100% on its training data
may be excellent or worthless, and the training score cannot tell you which. This realisation is what
Course 2 Week 3 is built on.</p>""")

        + h2("🔬", "Why more flexibility is dangerous")
        + """<p>A degree-8 polynomial through 9 data points can pass through <em>every single one</em>
exactly. The training error is zero. It is also wiggling violently between the points, and its predictions
between and beyond them are nonsense.</p>
<p>The model has spent its flexibility fitting the <b>noise</b> — the random scatter that will be different
next time — rather than the <b>signal</b>. And it has no way of telling the difference, because both look
identical in the training data.</p>"""

        + h2("🧮", "Overfitting, on the microchip data")
        + """<p>The Week 3 assignment’s second data set: 118 microchips, each with two test scores,
pass or fail. Two features is not enough to separate them, so the assignment maps them up to degree 6
— every product <var>x</var><sub>1</sub><sup>a</sup><var>x</var><sub>2</sub><sup>b</sup> up to total
power 6:</p>"""
        + table(["", "value"],
                [["training examples", "118"],
                 ["raw features", "2"],
                 ["features after mapping", "<b>27</b>"]])
        + """<p>Fit that with no regularisation and it reaches <b>83.9%</b> training accuracy, with a
boundary that wanders in and out to capture individual points. The largest fitted weight is
<b>7.454</b> and the average magnitude is <b>3.139</b> — large numbers, which is the fingerprint.</p>
<p>Big weights are what a wiggly boundary is <em>made of</em>. To swing sharply near one training
point, the model needs large coefficients on the high-order terms, so they nearly cancel over most
of the space and then briefly dominate. That is why the next two lessons attack the weights directly
rather than the boundary.</p>"""
        + warn("""<p>83.9% is a <em>training</em> number, and this lesson is the reason not to trust
it. Course 2 Week 3 supplies the tool that makes it measurable — a held-out set — which Course 1
does not yet have.</p>""")
        + explain("""<p>Overfitting is usually described as “too many features”, but 27 features on
118 examples is not obviously too many. <b>What is the more precise condition?</b></p>""",
                  """<p>That the model has enough flexibility to fit variation that will not recur.
Counting features against examples is a rough proxy — what matters is how much the fitted function
would <em>change</em> if you resampled the data. Degree-6 terms let the boundary bend sharply in
regions containing one or two points, so those points determine the shape there, and a different
sample would give a different shape. Regularisation works precisely because it attacks that
flexibility without removing the features.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Judging a model by its training accuracy.</b> It is the one number that cannot
distinguish a good model from a memoriser. You need data the model has never seen — the subject of Course
2 Week 3.</p>""")
        + trap("""<p><b>Assuming more complex is better.</b> Extra capacity buys you the ability to overfit
as readily as the ability to fit.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("Your model gets 100% on training data and 60% on new data. Which problem?",
             "<p><b>Overfitting</b> / high variance. It memorised rather than generalised.</p>"),
            ("Your model gets 62% on training and 60% on new data. Which problem?",
             "<p><b>Underfitting</b> / high bias. It cannot even fit the data it has seen, so more data "
             "will not help.</p>"),
            ("Why does a degree-8 polynomial through 9 points have zero training error and still be bad?",
             "<p>Because it has exactly enough freedom to pass through every point, so it fits the noise "
             "as faithfully as the signal. Between and beyond the points its predictions are wild.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("lab", REPO + "/week3/Optional%20Labs/C1_W3_Lab08_Overfitting_Soln.ipynb",
             "Optional lab: Overfitting",
             "In this repo. Interactive — add data points and change the degree, and watch it happen."),
            ("docs", "https://scikit-learn.org/stable/auto_examples/model_selection/plot_underfitting_overfitting.html",
             "scikit-learn — underfitting vs overfitting",
             "The canonical figure, with runnable code."),
        ])
    )))

# ============================================================ 9
L.append(dict(
    slug="09-addressing-overfitting", title="Addressing overfitting", mins=8, tag="core",
    lede="Three options, and a clear reason why the third one is usually where you start.",
    body=(
        pretest("""<p>Your model is overfitting. <b>List every fix you can think of before reading</b> — there are three main ones and most people get two.</p>""",
        """<p>Watch for which fix is usually the most effective and least available, and which one this week is really about.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Your model memorised. Three ways to stop it:</p>
<ol>
<li><b>Show it more examples.</b> Memorise ten photos, easy. Memorise ten million, impossible — you have to
learn the actual pattern instead.</li>
<li><b>Give it fewer things to look at.</b> Fewer knobs means less to fiddle with.</li>
<li><b>Stop it turning the knobs so far.</b> Keep every knob, but don’t let any of them go to extremes.</li>
</ol>""")

        + lenses(
            """<p>Three ways to stop a student memorising the mark scheme instead of learning the subject.</p>
<p>Give them more past papers. Cut the syllabus to what matters. Or mark them down for over-elaborate
answers. All three work, they cost different amounts, and you would try them in that order.</p>""",
            """<p>The three options are more data, fewer features, and regularisation, and the trade-off is
practical.</p>
<p>More data is the best fix and usually the most expensive. Feature selection is cheap and discards
information permanently. Regularisation keeps every feature and merely shrinks its influence, which is
why it is the default.</p>""",
            """<p>Three fits through the same points: a straight line missing the trend, a smooth curve following it,
and a wild curve passing exactly through every point.</p>
<p>The third has <b>zero training error</b> and is useless. Holding that picture is what makes “zero
training error” read as a warning rather than an achievement.</p>""",
            """<p>Feature selection has a specific hidden cost: it is a decision made on your training data, so
removing a feature that looked useless on 200 rows can remove one that mattered.</p>
<p>Regularisation avoids the irreversible choice by shrinking rather than deleting, and letting the data
decide how much — which is the argument for the rest of the week.</p>""",
            """So the three options below are a ranked list, and the third is where the remaining lessons go.""")

        + h2("🎬", "Watch it move")
        + demo("addressing", "The three options, with what each costs",
               "each row shows the benefit and the drawback")

        + h2("🔢", "The three options")
        + grid3(
            card("<h3>1 · More data</h3><p><b>The best fix</b> when it is available. With enough examples "
                 "even a flexible model cannot wiggle — there is no room left between the points.</p>"
                 "<p style='color:var(--ink-faint)'>Often expensive, slow, or simply impossible. Course 2 "
                 "Week 3 covers cheaper ways to get more, including augmentation.</p>"),
            card("<h3>2 · Fewer features</h3><p>Feature selection. Fewer parameters means less capacity to "
                 "memorise noise.</p>"
                 "<p style='color:var(--ink-faint)'>You may throw away a feature that genuinely carried "
                 "information, and you usually cannot tell in advance which.</p>"),
            card("<h3>3 · Regularisation</h3><p>Keep every feature, but shrink the weights towards zero. "
                 "A soft version of deleting a feature.</p>"
                 "<p style='color:var(--ink-faint)'>The one to reach for first, and the subject of the "
                 "rest of this week.</p>"))
        + key("""<p>Regularisation usually beats feature selection because it does not force a binary
choice. A feature that matters a little keeps a small weight; one that matters not at all gets shrunk
towards nothing. You do not have to decide in advance which is which.</p>""")

        + h2("🔬", "What the weights look like when overfitting")
        + """<p>A characteristic symptom: an overfit polynomial has <b>enormous</b> coefficients, often with
alternating signs — +4200, −18000, +31000. Those huge opposing terms are what produce the violent
wiggles between the data points.</p>
<p>That observation is the whole idea behind regularisation. If large weights cause wiggling, then
<b>penalising large weights</b> should stop the wiggling. It is a direct, almost crude, response to an
observed symptom — and it works remarkably well.</p>"""

        + h2("🔤", "The words, decoded")
        + decode([
            ("regularization", "“regularisation”", "Adding a penalty for large weights so the fitted curve stays smooth."),
            ("lambda (λ)", "“lambda”", "How hard to penalise. 0 = no penalty; very large = every weight crushed to nearly zero."),
            ("feature selection", "“feature selection”", "Dropping features by hand. Works, but throws away whatever information they carried."),
            ("generalisation", "“generalisation”", "Performance on data the model has never seen. The only thing that actually matters."),
        ])
        + h2("✅", "Check yourself")
        + quiz([
            ("You are overfitting and cannot collect more data. What are your options?",
             "<p>Fewer features, or regularisation. Try regularisation first — it keeps all the "
             "information available.</p>"),
            ("Why does more data reduce overfitting?",
             "<p>Because there is no longer room to pass through every point with a wild curve. The "
             "model is forced towards the pattern that explains all of them at once.</p>"),
            ("What do the weights of an overfit polynomial typically look like?",
             "<p>Very large, often with alternating signs. Huge opposing terms produce the violent "
             "oscillations — which is exactly what regularisation targets.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("lab", REPO + "/week3/Optional%20Labs/C1_W3_Lab08_Overfitting_Soln.ipynb",
             "Optional lab: Overfitting",
             "In this repo. Try all three fixes and see each one work."),
            ("book", "https://info.deeplearning.ai/machine-learning-yearning-book",
             "Andrew Ng — Machine Learning Yearning",
             "Free. The practical version of “what should I try next?”, expanded into a whole book."),
        ])
    )))

# ============================================================ 10
L.append(dict(
    slug="10-cost-function-with-regularization", title="The cost function with regularization",
    mins=20, tag="maths",
    lede="Add one term that punishes large weights. λ decides how much it matters, and that single dial "
         "spans the whole range from overfit to underfit.",
    body=(
        pretest("""<p>You want the model to fit the data <em>and</em> keep its weights small. <b>Guess how you would tell it to care about both, using one number.</b></p>""",
        """<p>Watch for the extra term added to the cost, and for what λ = 0 and λ = enormous each do to the fit.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>You have been telling the model one thing: “fit the data.” So it does, extravagantly.</p>
<p>Now tell it two things: “fit the data, <b>and</b> keep your numbers small.” It has to balance them,
which means it will only use a big weight when a big weight really earns its keep.</p>
<p>λ decides how loudly you say the second thing. Say it quietly and nothing changes. Shout it and the
model flattens into a straight line.</p>""")

                + lenses(
            """<p>A packing list with a weight limit.</p>
<p>You can take anything, but every item costs you against the allowance — so you take the umbrella
only if you genuinely expect rain. The limit does not forbid anything; it forces each item to justify
its place.</p>
<p>Regularisation is a weight limit on the model’s parameters. Every feature can still be used, but
each one now has to earn its coefficient.</p>""",
            """<p>This is <b>ridge regression</b> — Hoerl and Kennard, 1970 — arriving in machine learning under a
new name.</p>
<p>Statisticians introduced it to handle collinear predictors, where ordinary least squares produces
enormous, unstable coefficients that swing wildly with tiny changes in the data. Shrinking them
trades a little bias for a large reduction in variance. Same cure, same reason, fifty years earlier.</p>""",
            """<p>A curve on a leash.</p>
<p>Without the leash it can lunge to reach every training point. With it, it can still move, but every
metre of slack pulls back. Turn λ up and the leash shortens until the curve is dragged flat; turn it
to zero and the leash is gone.</p>""",
            """<p>Measured on the microchip dataset in this course: λ = 0 gives a mean weight magnitude of
<b>3.14</b>; λ = 1 gives <b>0.56</b>; λ = 100 gives <b>0.017</b> and an accuracy collapse to 0.61.</p>
<p>That last number is the honest half — regularisation is not free, and past a point it destroys the
model. λ is a dial you tune against held-out data, not a switch you turn on.</p>""",
            """So the extra term below is a price list, and λ is how expensive you have decided complexity should
be.""")
        + h2("🎬", "Watch it move")
        + demo("regcost", "Drag λ from 0 to 10,000",
               "watch both the curve and the bar chart of weight sizes")

        + h2("🔢", "The maths, decoded")
        + eqp([
            ("<var>J</var>(<var>w⃗</var>, <var>b</var>)", "cost-j", "the cost"),
            ' <span class="op">=</span> ',
            ('<span class="frac"><span>1</span><span>2<var>m</var></span></span>', "avg-factor", "the average"),
            ('<span class="big">Σ</span>', "sigma", "for every example"),
            ('( <var>f</var>(<var>x</var><sup>(<var>i</var>)</sup>) <span class="op">−</span> <var>y</var><sup>(<var>i</var>)</sup> )',
             "error-term", "predicted − actual — the fit term"),
            ('<sup>2</sup>', "squared-term", "squared"),
            ' <span class="op">+</span> ',
            ('<span class="frac"><span><var class="hl-a">λ</var></span><span>2<var>m</var></span></span> <span class="big">Σ</span><sub><var>j</var>=1</sub><sup><var>n</var></sup> <var>w</var><sub><var>j</var></sub><sup>2</sup>',
             "reg-penalty", "the penalty term — keeps weights small"),
        ], "fit the data … and keep the weights small — hover or click any part")
        + decode([
            ("first term", "“the fit term”", "The original cost. Wants to match the data as closely as possible."),
            ("second term", "“the penalty term”", "Wants every weight near zero. These two pull in opposite directions."),
            ("<var class='hl-a'>λ</var>", "“lambda”", "The regularisation parameter. Decides which term wins. λ ≥ 0."),
            ("Σ<var>w</var><sub>j</sub>²", "“the size of the weights”", "Sum of squares. Large weights are penalised much more than small ones — squaring again."),
            ("j = 1 … n", "“note where the sum starts”", "It starts at 1, not 0. <b>b is not regularised.</b>"),
            ("λ / 2m", "“scaled the same way”", "Dividing by m means λ does not need re-tuning when the dataset size changes."),
        ])

        + h2("🎚", "What λ does, at the extremes")
        + table(["λ", "What wins", "The model", "The problem"],
                [["0", "the fit term only", "the original, unregularised model", "<b>overfits</b>"],
                 ["small (0.01–1)", "mostly fit, a little restraint", "follows the trend, ignores noise", "usually about right"],
                 ["large (1000+)", "the penalty term", "all w ≈ 0, so f(x) ≈ b — a flat line", "<b>underfits</b>"]])
        + key("""<p>λ moves you smoothly along the whole spectrum from overfit to underfit. That makes it a
single dial with enormous leverage — and it raises the obvious question of how to choose it, which
Course 2 Week 3 answers properly with a cross-validation set.</p>""")

        + h2("🔬", "Why b is left out")
        + """<p>Shrinking b would only slide the whole curve up or down. It does nothing about wiggliness,
which is the actual problem. So convention leaves it alone.</p>
<p>Andrew notes you can include it and it makes very little practical difference. scikit-learn does not
regularise the intercept either. It is one of those conventions that is worth knowing is a convention.</p>"""
        + note("""<p>This is <b>L2 regularisation</b>, also called ridge regression, or “weight decay” in
deep learning. Its sibling <b>L1</b> penalises Σ|w<sub>j</sub>| instead, and has the interesting property
of driving some weights to <em>exactly</em> zero — performing feature selection automatically. That is
called lasso, and it is not covered in this course.</p>""", "L2, and its sibling L1")

        + h2("🧮", "What λ does to the weights — measured")
        + """<p>Same 118 microchips, same 27 features, three values of λ:</p>"""
        + table(["λ", "largest |w|", "mean |w|", "training accuracy"],
                [["0", "<b>7.454</b>", "3.139", "0.839"],
                 ["<b>1</b>", "2.020", "0.559", "<b>0.831</b>"],
                 ["100", "<b>0.055</b>", "0.017", "<b>0.610</b>"]])
        + """<p>Read the middle row against the top one. λ = 1 shrinks the average weight by a factor
of <b>5.6</b> and costs 0.8 percentage points of training accuracy. That is the trade working
exactly as intended: a far simpler function that fits the data almost as well, and which will
generalise better precisely because it is less beholden to individual points.</p>
<p>Now the bottom row. λ = 100 drives every weight to nearly zero — the largest is 0.055 — and
accuracy collapses to 0.610, barely above the base rate. The model has been penalised into
predicting essentially a constant. This is underfitting, produced deliberately, and it is why λ is
something you tune rather than set.</p>"""
        + note("""<p><var>b</var> is not penalised. Shrinking it towards zero would push predictions
towards <var>g</var>(0) = 0.5 regardless of the data, which constrains the model without buying any
smoothness — the wiggliness lives in the <var>w</var>s.</p>""")
        + explain("""<p>Regularisation makes the training cost worse by construction, and here it made
training accuracy worse too. <b>Why is that the right thing to want?</b></p>""",
                  """<p>Because training accuracy is not the objective — it is the quantity being
spent. What you actually want is performance on data you have not seen, and the only lever available
is how much the fitted function is allowed to contort itself around individual training points. λ
buys smoothness with training fit. The λ = 100 row shows the trade going too far, which is the
honest half of the lesson: the penalty has no idea what a good model looks like, so the amount is
your decision, made by measuring on held-out data.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Regularising unscaled features.</b> The penalty treats all weights equally, so a
feature measured in millions naturally gets a tiny weight and is effectively exempt from the penalty.
<b>Always scale before regularising.</b></p>""")
        + trap("""<p><b>Picking λ by looking at the training cost.</b> Increasing λ always increases the
training error — that is the entire point. Choosing λ requires data the model was not fitted on, which is
Course 2 Week 3.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("λ is enormous. What does the model look like?",
             "<p>Every w ≈ 0, so f(x) ≈ b — a horizontal line at the mean of y. Extreme underfitting.</p>"),
            ("λ = 0. What have you got?",
             "<p>The original unregularised cost. Whatever overfitting you had, you still have.</p>"),
            ("Why is b excluded from the penalty?",
             "<p>Because shrinking the intercept only shifts the curve vertically. It does nothing about "
             "the wiggliness that regularisation exists to control.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("lab", REPO + "/week3/Optional%20Labs/C1_W3_Lab09_Regularization_Soln.ipynb",
             "Optional lab: Regularization",
             "In this repo. Regularised cost and gradient for both linear and logistic regression."),
            ("docs", "https://scikit-learn.org/stable/modules/linear_model.html#ridge-regression",
             "scikit-learn — Ridge regression",
             "This exact penalty. Note that sklearn calls the parameter <code>alpha</code>, not lambda — because <code>lambda</code> is a reserved word in Python."),
            ("docs", "https://scikit-learn.org/stable/modules/linear_model.html#lasso",
             "scikit-learn — Lasso (L1)",
             "The sibling that zeroes weights outright, performing feature selection as a side effect."),
        ])
    )))

# ============================================================ 11
L.append(dict(
    slug="11-regularized-gradient-descent", title="Regularized linear and logistic regression",
    mins=10, tag="core",
    lede="One extra term in the update rule, which rearranges into something with a memorable name: weight "
         "decay. And it is the same for both algorithms.",
    body=(
        pretest("""<p>The cost gained an extra term. <b>Guess what that does to the update rule</b> — and what it means for a weight that the data is not actively pushing up.</p>""",
        """<p>Watch for the rearrangement into “shrink, then step”. It is why this is also called weight decay.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Before each step downhill, shrink every weight a tiny bit — multiply it by something
like 0.9998.</p>
<p>Then take the ordinary step.</p>
<p>Over thousands of iterations that constant nibbling keeps the weights small, unless the data keeps
pushing them back up. A weight only stays large if it is genuinely earning its place.</p>""")

        + lenses(
            """<p>The same walk downhill with a light spring pulling every parameter back towards zero.</p>
<p>A parameter that genuinely earns its size holds against the spring. One that grew large to
accommodate a single odd data point gets quietly pulled back in, and the fit stops chasing noise.</p>""",
            """<p>The extra term in the gradient is (λ/<var>m</var>)<var>w</var><sub>j</sub>, and rearranging shows
what it does: each step multiplies <var>w</var><sub>j</sub> by a factor slightly less than 1 before the
usual update.</p>
<p>That is why it is called <b>weight decay</b>, and it is exactly the ridge regression penalty you may
already know.</p>""",
            """<p>The familiar update line with one term added on the end.</p>
<p>And one deliberate omission worth noticing: <b><var>b</var> is not regularised</b>. The bias sets the
overall level rather than the sensitivity to any feature, and shrinking it towards zero just biases every
prediction downwards for no benefit.</p>""",
            """<p>Regularisation and feature scaling are entangled in a way that catches people: the penalty treats all
weights alike, so an unscaled feature with a large range gets an artificially small weight and is
penalised as though it mattered less.</p>
<p>Scale first, then regularise. Doing it the other way round applies an uneven penalty you did not
intend and cannot see.</p>""",
            """So the one extra term below is the spring, and λ is how strong you make it.""")

        + h2("🎬", "Watch it move")
        + demo("reglinlog", "The rearranged update, and the shrink factor",
               "drag α and λ and watch (1 − αλ/m) change")

        + h2("🔢", "The maths, decoded")
        + eqp([
            ('<var>w</var><sub><var>j</var></sub> <span class="op">:=</span>', "assign-op", "becomes, not equals"),
            ' <var>w</var><sub><var>j</var></sub> <span class="op">−</span> ',
            ('<var>α</var>', "alpha-lr", "the learning rate"),
            ' <span class="paren">[</span> ',
            ('<span class="frac"><span>1</span><span><var>m</var></span></span><span class="big">Σ</span>( <var>f</var> <span class="op">−</span> <var>y</var> )<var>x</var><sub><var>j</var></sub>',
             "error-term", "the ordinary derivative"),
            ' <span class="op">+</span> ',
            ('<span class="frac"><span><var class="hl-a">λ</var></span><span><var>m</var></span></span><var>w</var><sub><var>j</var></sub>',
             "reg-penalty", "pulls wⱼ toward zero"),
            ' <span class="paren">]</span>',
        ], "the regularised update — one extra term — hover or click a part")
        + eqp([
            ('<var>w</var><sub><var>j</var></sub> <span class="op">:=</span>', "assign-op", "becomes, not equals"),
            ' ',
            ('<var class="hl-a">(1 <span class="op">−</span> <var>α</var><var>λ</var>/<var>m</var>)</var> <var>w</var><sub><var>j</var></sub>',
             "reg-penalty", "shrink wⱼ a little first"),
            ' <span class="op">−</span> ',
            ('<var>α</var>', "alpha-lr", "the learning rate"),
            (' <span class="frac"><span>1</span><span><var>m</var></span></span><span class="big">Σ</span>( <var>f</var> <span class="op">−</span> <var>y</var> )<var>x</var><sub><var>j</var></sub>',
             "error-term", "then step, as usual"),
        ], "…which rearranges into: shrink first, then step — hover or click a part")
        + decode([
            ("(1 − αλ/m)", "“the shrink factor”", "A number just below 1. With α = 0.01, λ = 1, m = 50 it is 0.9998."),
            ("weight decay", "“the name for this”", "Because each iteration multiplies w by slightly less than 1, weights decay towards zero unless the data pushes back."),
            ("λ = 0", "“no regularisation”", "The factor becomes exactly 1 and you are back to ordinary gradient descent."),
            ("b update", "“unchanged”", "b is not regularised, so its update has no extra term at all."),
        ])
        + key("""<p>Every single iteration multiplies w<sub>j</sub> by a number slightly below 1 <em>before
doing anything else</em>. That is weight decay, and it is literally what the name describes.</p>""")

        + h2("🔁", "And it is identical for logistic regression")
        + """<p>Character for character. The only thing that differs, as always, is what f means:</p>"""
        + table(["", "Linear regression", "Logistic regression"],
                [["f", "<code>w·x + b</code>", "<code>g(w·x + b)</code>"],
                 ["regularised update", "as above", "<b>exactly as above</b>"]])
        + """<p>Which means one implementation of the regularised gradient serves both algorithms with a
single line changed — and it is the same line that changed in lesson 7.</p>"""

        + h2("💻", "In code")
        + code("""
def compute_gradient_reg(X, y, w, b, lambda_):
    m, n = X.shape
    f = sigmoid(np.dot(X, w) + b)         # or just np.dot(X, w) + b for linear
    err = f - y
    dj_dw = np.dot(X.T, err) / m
    dj_db = np.sum(err) / m

    dj_dw += (lambda_ / m) * w            # <- the ONLY new line
    # note: dj_db is deliberately NOT regularised

    return dj_dw, dj_db
""")

        + h2("🌍", "Where you will see this again")
        + """<p>Every modern deep-learning optimiser has a <code>weight_decay</code> argument, and it is
this. PyTorch’s <code>AdamW</code>, TensorFlow’s kernel regularisers, and the
<code>kernel_regularizer=l2(0.01)</code> you will write in Course 2 Week 3 are all the same idea.</p>
<p>The formula you just derived on a two-parameter regression is the one keeping billion-parameter models
from memorising their training sets.</p>"""

        + h2("🎓", "That is Course 1")
        + """<p>You now have two complete algorithms — linear regression and logistic regression — plus
gradient descent, vectorisation, feature scaling, feature engineering, and regularisation.</p>
<p>Course 2 replaces the model with a neural network and keeps everything else. The cost function, the
gradient descent, the scaling, the regularisation, the overfitting story — all of it carries straight
over. That is why this course is worth doing properly before moving on.</p>"""

        + h2("✅", "Check yourself")
        + quiz([
            ("α = 0.01, λ = 1, m = 50. What is the shrink factor?",
             "<p>1 − (0.01 × 1)/50 = 1 − 0.0002 = <b>0.9998</b>. Tiny per step, and it compounds over "
             "thousands of iterations.</p>"),
            ("Why does the b update have no regularisation term?",
             "<p>Because b was excluded from the penalty term in the cost, so its derivative has no extra "
             "piece.</p>"),
            ("How much does the regularised gradient code differ between linear and logistic regression?",
             "<p>One line — whether f has a sigmoid around it. The regularisation term is identical.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("lab", REPO + "/week3/Optional%20Labs/C1_W3_Lab09_Regularization_Soln.ipynb",
             "Optional lab: Regularization",
             "In this repo. Both regularised gradients, side by side."),
            ("lab", REPO + "/week3/C1W3A1/C1_W3_Logistic_Regression.ipynb",
             "Week 3 assignment: Logistic Regression",
             "In this repo. The graded exercise — you implement the cost, the gradient, and the regularised versions of both."),
            ("paper", "https://arxiv.org/abs/1711.05101",
             "Loshchilov & Hutter (2017) — Decoupled Weight Decay Regularization",
             "How this exact idea is applied in modern deep learning, and a subtle bug in how Adam had been doing it for years."),
        ])
    )))

WEEK = dict(
    course="C1", week=3, title="Classification",
    time="~6–7 h with labs",
    goal="Build logistic regression from the sigmoid up, understand why it needs its own cost function, "
         "and meet overfitting and regularisation for the first time.",
    lessons=L,
)
