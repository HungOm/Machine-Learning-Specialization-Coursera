# -*- coding: utf-8 -*-
"""C2 · Week 2 — Training, activations, softmax, optimisation."""
from kit import (kid, key, warn, trap, note, card, eq, eqp, decode, table, demo,
                 quiz, links, code, h2, grid2, grid3, pretest, explain, lenses)

L = []

# ============================================================ 1
L.append(dict(
    slug="01-tensorflow-training", title="TensorFlow implementation of training", mins=13, tag="code",
    lede="Three lines of code, three ideas you already know from Course 1. This lesson is the map; the "
         "next one opens the box.",
    body=(
        pretest("""<p>Course 1 took a week to build gradient descent by hand. <b>Guess how many lines TensorFlow needs to train a whole network.</b></p>""",
        """<p>Watch for the three calls, and for which one contains everything you built by hand.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Teaching a model is like teaching a dog three things:</p>
<ol><li><b>What tricks exist</b> — sit, roll over, play dead. (that’s the model)</li>
<li><b>What counts as wrong</b> — “no, that was a sit, I said roll.” (that’s the loss)</li>
<li><b>Practise until it improves</b> — again, and again, and again. (that’s fit)</li></ol>
<p>You did all three in Course 1 with logistic regression, by hand. TensorFlow just gives each step a name
and does the boring part for you.</p>""")

        + h2("💻", "The whole of training, in code")
        + code("""
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.losses import BinaryCrossentropy

# 1. define the model
model = Sequential([
    Dense(units=25, activation='relu'),
    Dense(units=15, activation='relu'),
    Dense(units=1,  activation='sigmoid'),
])

# 2. say what "wrong" means
model.compile(loss=BinaryCrossentropy())

# 3. minimise it
model.fit(X, Y, epochs=100)
""")
        + decode([
            ("<code>Sequential</code>", "“the architecture”", "Exactly what f(x) is allowed to look like. Nothing has been learned yet — the weights are random."),
            ("<code>compile(loss=…)</code>", "“the rule for wrongness”", "Which cost function to minimise. It does <b>not</b> train anything; it just records the setting."),
            ("<code>fit(X, Y, epochs=100)</code>", "“practise”", "Run gradient descent. One <b>epoch</b> = one full sweep over the training set."),
            ("<code>epochs</code>", "“how many sweeps”", "Too few and it hasn’t learned; too many and it starts memorising. Week 3 tells you how to choose."),
        ], head=("Line", "Say it out loud", "What it does"))

        + h2("🎬", "Watch it move")
        + demo("trainsteps", "The three steps, and their Course 1 twins",
               "each panel shows the neural-network version and the logistic-regression version side by side")

        + h2("🔗", "The parallel with Course 1, written out")
        + table(["Step", "Logistic regression (by hand)", "Neural network (TensorFlow)"],
                [["1. Model",
                  "<code>z = np.dot(w,x)+b</code><br><code>f = 1/(1+np.exp(-z))</code>",
                  "<code>Sequential([Dense(...), ...])</code>"],
                 ["2. Loss",
                  "<code>loss = -y*log(f) - (1-y)*log(1-f)</code>",
                  "<code>model.compile(loss=BinaryCrossentropy())</code>"],
                 ["3. Minimise",
                  "<code>w = w - alpha*dj_dw</code><br><code>b = b - alpha*dj_db</code>",
                  "<code>model.fit(X, Y, epochs=100)</code>"]])
        + key("""<p>Nothing conceptually new has happened. The model got bigger, so the derivatives got
harder to write down by hand — and TensorFlow computes them for you. That is the <em>entire</em> service
the framework provides.</p>""")

        + h2("🧮", "The same three steps, counted")
        + """<p>Here is the Week 2 assignment’s network, and what each of the three steps is actually
responsible for:</p>"""
        + code("""
model = Sequential([                              # step 1
    tf.keras.Input(shape=(400,)),
    Dense(25, activation='relu',   name='L1'),
    Dense(15, activation='relu',   name='L2'),
    Dense(10, activation='linear', name='L3'),
])
model.compile(loss=SparseCategoricalCrossentropy(from_logits=True),   # step 2
              optimizer=tf.keras.optimizers.Adam(1e-3))
model.fit(X, y, epochs=40)                        # step 3
""")
        + table(["Step", "What it decides", "In numbers"],
                [["1 · define the model", "how many unknowns there are",
                  "(400×25+25) + (25×15+15) + (15×10+10) = <b>10,575</b> parameters"],
                 ["2 · define the loss", "what “wrong” means for this problem",
                  "one function; the only line that knows this is a 10-class problem"],
                 ["3 · minimise it", "the actual values of all 10,575",
                  "40 passes over 5,000 examples"]])
        + """<p>Course 1 had you write all three by hand for two parameters. Nothing has changed except
the count — and that the derivatives are now found by backpropagation instead of by you.</p>"""
        + explain("""<p>Step 1 never mentions classification, and step 3 never mentions it either.
<b>Why is the problem type visible only in step 2?</b></p>""",
                  """<p>Because layers are just arithmetic — <var>g</var>(<var>a</var><var>W</var> +
<var>b</var>) is the same operation whether you are predicting a price or a digit, and gradient
descent only ever asks “which way is downhill”. The loss is the single place where you say what
counts as an error, so it is the only place the answer’s <em>type</em> can enter. Swap
<code>SparseCategoricalCrossentropy</code> for <code>MeanSquaredError</code> and the identical
network becomes a regressor.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Believing the library because it is a library.</b> Andrew’s warning in this lesson is
worth repeating: use frameworks, but know what they are doing. When your loss goes to NaN at epoch 3, only
the underlying understanding will save you.</p>""")
        + trap("""<p><b>Forgetting <code>metrics=['accuracy']</code>.</b> Without it, <code>fit</code> prints
only the loss, which is hard to interpret. Add it and you get a human-readable number per epoch.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("What has the model learned right after <code>compile()</code>?",
             "<p><b>Nothing.</b> compile only records the loss and optimiser. The weights are still random.</p>"),
            ("You call fit(X, Y, epochs=100) twice. How many epochs has the model seen?",
             "<p><b>200.</b> Keras continues from the existing weights; it does not reset.</p>"),
            ("Why is BinaryCrossentropy the right loss here and not mean squared error?",
             "<p>Because the output is a probability for a yes/no label. Cross-entropy punishes confident "
             "wrong answers extremely hard, and gives a convex, well-behaved cost for classification. "
             "MSE on probabilities trains slowly and badly.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("docs", "https://keras.io/api/models/model_training_apis/",
             "Keras — compile / fit reference",
             "Every argument, including callbacks and validation_split, which you will want in Week 3."),
            ("docs", "https://www.tensorflow.org/guide/basic_training_loops",
             "TensorFlow — writing a training loop from scratch",
             "What fit() actually does, unrolled. Read once; it demystifies the magic permanently."),
            ("lab", "../../C2%20-%20Advanced%20Learning%20Algorithms/week2/C2W2A1/C2_W2_Assignment.ipynb",
             "Week 2 assignment",
             "In this repo. Builds and trains a 25→15→10 digit classifier with exactly these three steps."),
        ])
    )))

# ============================================================ 2
L.append(dict(
    slug="02-training-details", title="Training details", mins=15, tag="core",
    lede="Opening the box: what the loss function actually is, why it is shaped the way it is, and what "
         "gradient descent does with it.",
    body=(
        pretest("""<p>Training needs three ingredients: a model, a way to score it, and a way to improve it. <b>Name the TensorFlow call for each</b> before reading.</p>""",
        """<p>Watch for how exactly the three map onto what you already know from Course 1. Nothing new is happening — only the names.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Imagine a game where you guess how likely something is, from 0% to 100%, and you get
<b>penalty points</b> for being wrong.</p>
<p>The rule is cruel but fair: the more <b>confident</b> you were, the bigger the penalty when you turn out
to be wrong. Saying “99% sure it’s a cat” about a dog costs you a fortune. Saying “55% sure” about the same
dog costs you a little.</p>
<p>Training is just: play this game millions of times, and after every guess, nudge your brain slightly in
whatever direction would have reduced the penalty.</p>""")

        + h2("🔢", "The maths, decoded — the loss")
        + eqp([
            '<var>L</var>(<var>f</var>, <var>y</var>) <span class="op">=</span> ',
            ('<span class="op">−</span><var>y</var> log(<var>f</var>) <span class="op">−</span> (1 <span class="op">−</span> <var>y</var>) log(1 <span class="op">−</span> <var>f</var>)',
             "logloss-native", "the two-case trick, in one line"),
        ], "binary cross-entropy — the loss for ONE example — hover or click it")
        + """<p>It looks like two terms, but only ever one is alive:</p>"""
        + table(["If the truth is…", "…the formula becomes", "Meaning"],
                [["y = 1", "L = −log(f)", "f near 1 → loss ≈ 0. f near 0 → loss → ∞."],
                 ["y = 0", "L = −log(1 − f)", "f near 0 → loss ≈ 0. f near 1 → loss → ∞."]])
        + decode([
            ("<var>L</var>", "“the loss”", "How wrong you were on <b>one</b> example."),
            ("<var>J</var>", "“the cost”", "The average loss over <b>all m</b> examples. J = (1/m)ΣL. The thing you actually minimise."),
            ("<var>f</var>", "“f of x”", "The model’s predicted probability, between 0 and 1."),
            ("log", "“natural log”", "Base <var>e</var>. Its job here is turning “tiny probability” into “huge penalty” — log(0.001) = −6.9."),
            ("−", "“the minus sign”", "log of a number below 1 is negative; the minus flips it positive so that “big number = bad”."),
        ])

        + h2("🎬", "Watch it move")
        + demo("losscurve", "The loss curve — drag the prediction",
               "switch the true label and watch which curve you are being scored on")

        + h2("📉", "And then gradient descent")
        + eqp([
            ('<var>w</var><sub><var>j</var></sub><sup>[<var>l</var>]</sup> <span class="op">:=</span>', "assign-op", "becomes, not equals"),
            ' <var>w</var><sub><var>j</var></sub><sup>[<var>l</var>]</sup> <span class="op">−</span> ',
            ('<var class="hl-a">α</var>', "alpha-lr", "the learning rate"),
            (' <span class="frac"><span>∂<var>J</var></span><span>∂<var>w</var><sub><var>j</var></sub><sup>[<var>l</var>]</sup></span></span>',
             "partial-f0", "the slope, at this weight"),
        ], "repeat for every weight and every bias, over and over — hover or click a part")
        + decode([
            (":=", "“becomes”", "Assignment, not equality. The new w is computed from the old one."),
            ("<var class='hl-a'>α</var>", "“alpha”, the learning rate", "Step size. Too small → glacial. Too big → it overshoots and diverges."),
            ("∂J/∂w", "“the partial derivative”", "“If I nudge this one weight up a hair, how much does the total cost go up?” Backprop computes all of them at once."),
        ])
        + note("""<p>In Course 1 you differentiated by hand. In a network with 20,000 weights that is not
possible, so TensorFlow builds a <b>computation graph</b> and applies the chain rule automatically. That
is what lessons 13–15 of this week explain, and why they are optional-but-worth-it.</p>""",
               "Where the derivatives come from")

        + h2("🧮", "The loss, in numbers")
        + """<p>The logistic loss is −log(<var>f</var>) when <var>y</var> = 1 and
−log(1 − <var>f</var>) when <var>y</var> = 0. Abstract until you tabulate it:</p>"""
        + table(["model says f =", "loss if the truth is y = 1", "loss if the truth is y = 0"],
                [["0.90", "<b>0.105</b> — right and confident, nearly free", "2.303 — confidently wrong"],
                 ["0.50", "0.693", "0.693 — a shrug costs the same either way"],
                 ["0.10", "2.303 — confidently wrong", "<b>0.105</b>"],
                 ["0.01", "<b>4.605</b> — certain and wrong", "0.010"]])
        + """<p>Read the first column downwards. Being right costs almost nothing. Being wrong costs
something. Being <em>certain</em> and wrong costs 4.6 — and it keeps climbing without limit as
<var>f</var> → 0, because −log(0) is infinite. That asymmetry is the whole design: the loss is far
more interested in punishing confident mistakes than in rewarding confident successes.</p>"""
        + explain("""<p>A simpler-looking choice would be |<var>y</var> − <var>f</var>|, which is 0.9
for the “certain and wrong” row instead of 4.605. <b>Why is the log version better for
learning?</b></p>""",
                  """<p>Two reasons, and both matter. First, |<var>y</var> − <var>f</var>| is bounded
by 1 — a catastrophically wrong prediction is treated as barely worse than a mildly wrong one, so
the model has little reason to fix it. The log is unbounded, so it does. Second, and decisively, the
squared/absolute error paired with a sigmoid is not convex in general, while the log
loss is — and, more practically, squared error's gradient carries a g′(z) factor that dies
exactly where the model is confidently wrong — which is what makes gradient descent reliable here at all. It is the same
argument you met in Course 1 when logistic regression dropped squared error.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Loss vs cost.</b> Loss = one example. Cost = the average over the dataset. The course
is careful about this and so are interviewers.</p>""")
        + trap("""<p><b>Using MSE for classification.</b> It <em>runs</em>, and it trains badly: the gradient
is tiny exactly where the model is confidently wrong, which is where you most need a big correction.</p>""")
        + warn("""<p>For <b>regression</b> with a neural network you swap the loss for
<code>MeanSquaredError()</code> and the output activation for <code>'linear'</code>. Same three steps,
two different settings.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("y = 1 and f = 0.9. What is the loss? Now y = 1 and f = 0.1.",
             "<p>−log(0.9) ≈ <b>0.105</b>. And −log(0.1) ≈ <b>2.303</b> — twenty times worse for the same "
             "single example.</p>"),
            ("Why does the loss go to infinity as f → 0 when y = 1?",
             "<p>Because the model claimed something true was impossible. Infinite penalty is the honest "
             "price of infinite confidence in a falsehood.</p>"),
            ("What happens to training if α is far too large?",
             "<p>Each step overshoots the minimum, the cost oscillates or explodes to NaN. If your loss "
             "becomes NaN, lowering α is the first thing to try.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("video", "https://www.3blue1brown.com/lessons/gradient-descent",
             "3Blue1Brown — Gradient descent",
             "The best visual account of “nudge everything downhill” there is."),
            ("docs", "https://www.tensorflow.org/api_docs/python/tf/keras/losses/BinaryCrossentropy",
             "tf.keras.losses.BinaryCrossentropy",
             "Note the <code>from_logits</code> argument — Lesson 9 explains why it matters."),
            ("book", "https://www.deeplearningbook.org/contents/ml.html",
             "Deep Learning — chapter 5.5, maximum likelihood",
             "Where cross-entropy comes from: it is the negative log-likelihood of the data under the model."),
        ])
    )))

# ============================================================ 3
L.append(dict(
    slug="03-sigmoid-alternatives", title="Alternatives to the sigmoid activation", mins=14, tag="core",
    lede="ReLU, and why one strange-looking bent line replaced the elegant S-curve almost everywhere.",
    body=(
        pretest("""<p>Sigmoid squashes everything into 0…1. <b>Guess why that is a problem for a layer in the middle of a deep network</b>, even though it is fine at the output.</p>""",
        """<p>Watch for what happens to the slope when the input is large. No slope means no learning.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Sigmoid squashes everything into 0…1. That’s useful for a final “how likely?” answer,
but it’s a terrible way to pass a message along a chain.</p>
<p>Why? Because once a number is very big or very small, sigmoid flattens it completely. 100 and 1000 both
come out as “basically 1”. The neuron has stopped being able to tell them apart — and worse, it stops being
able to learn, because learning needs the curve to have a <b>slope</b>.</p>
<p>ReLU is blunter and better: <b>if it’s negative, say zero. Otherwise, pass it straight through.</b>
That’s the whole function. And on the positive side it never flattens.</p>""")

        + h2("🔢", "The maths, decoded")
        + eqp([
            ('<var>g</var>(<var>z</var>) <span class="op">=</span> max(0, <var>z</var>)', "relu-native", "0 below zero, unchanged above"),
        ], "ReLU — rectified linear unit — hover or click it")
        + table(["z", "sigmoid(z)", "ReLU(z)", "sigmoid slope", "ReLU slope"],
                [["−10", "0.00005", "0", "0.00005 — dead", "0 — dead"],
                 ["−1", "0.269", "0", "0.197", "0"],
                 ["0", "0.5", "0", "0.25 — the best it gets", "0 / 1 (undefined at exactly 0)"],
                 ["1", "0.731", "1", "0.197", "1"],
                 ["10", "0.99995", "10", "0.00005 — dead", "1 — still learning"]])
        + decode([
            ("ReLU", "“rel-you”", "Rectified Linear Unit. “Rectified” is borrowed from electronics: a rectifier passes current one way only."),
            ("max(0, z)", "“zero or z, whichever is bigger”", "One comparison. No exponential, no division. Enormously cheaper than sigmoid."),
            ("saturation", "“going flat”", "When the activation stops responding to changes in z. Slope ≈ 0 means gradient ≈ 0 means no learning."),
            ("vanishing gradient", "“the signal fades”", "In a deep stack, slopes below 1 multiply together and shrink towards zero. Early layers stop learning entirely."),
        ])

        + h2("🎬", "Watch it move")
        + demo("activations", "The activation zoo — drag z, watch the slope",
               "the dashed line is the slope; flat slope means learning has stalled")
        + """<p>Select sigmoid and drag z out to ±6. The dashed slope line goes flat and the readout warns
you. Now do the same on ReLU: on the positive side the slope stays exactly 1, no matter how far out you go.
That difference, multiplied across ten layers, is why ReLU won.</p>"""

        + h2("⚖️", "The scorecard")
        + grid2(
            card("<h3>Why ReLU wins</h3><ul>"
                 "<li>Slope is exactly 1 on the positive side — gradients survive deep stacks.</li>"
                 "<li>One <code>max</code>, no <code>exp</code> — meaningfully faster.</li>"
                 "<li>Outputs exact zeros, so many units switch off: sparse, and cheap.</li></ul>"),
            card("<h3>What it costs</h3><ul>"
                 "<li><b>Dying ReLU</b>: a unit stuck at z &lt; 0 for every example has zero gradient "
                 "forever and never recovers.</li>"
                 "<li>Not zero-centred, and unbounded above.</li>"
                 "<li>Variants exist — Leaky ReLU, ELU, GELU — but plain ReLU remains the default.</li></ul>"))

        + h2("🧮", "Why ReLU trains faster, in numbers")
        + """<p>The argument is about <em>slopes</em>, because gradient descent moves in proportion to
them. Here are both functions and both slopes:</p>"""
        + table(["z", "relu = max(0,z)", "sigmoid", "slope of relu", "slope of sigmoid"],
                [["−3", "0.0", "0.0474", "0", "<b>0.0452</b>"],
                 ["−1", "0.0", "0.2689", "0", "0.1966"],
                 ["&nbsp;0", "0.0", "0.5000", "0", "<b>0.2500</b> ← its best ever"],
                 ["+1", "1.0", "0.7311", "<b>1</b>", "0.1966"],
                 ["+3", "3.0", "0.9526", "<b>1</b>", "<b>0.0452</b>"]])
        + """<p>Sigmoid’s slope never exceeds 0.25, and away from the middle it collapses. Now recall
that backpropagation <em>multiplies</em> these slopes together, one per layer. Stack five sigmoid
layers and the gradient reaching the first layer is scaled by</p>"""
        + table(["Five layers of…", "gradient scaled by"],
                [["sigmoid at its very best (0.25)", "0.25⁵ = <b>0.00098</b> — a 1,000× shrink"],
                 ["sigmoid at |z| = 3 (0.0452)", "0.0452⁵ = <b>0.00000019</b> — effectively dead"],
                 ["ReLU on the active side (1)", "1⁵ = <b>1</b> — untouched"]])
        + """<p>That is the vanishing gradient problem in one table, and it is why the early layers of
a deep sigmoid network barely learn at all. ReLU’s slope is exactly 1 wherever it is active, so the
signal arrives at layer 1 undiminished.</p>"""
        + explain("""<p>ReLU is flat for every negative <var>z</var>, so <em>its</em> slope is 0 there
— seemingly the same flaw. <b>Why is that far less damaging than sigmoid’s two flat tails?</b></p>""",
                  """<p>Because ReLU is flat in one region and perfectly steep in the other, and a
unit sitting in the flat region is simply switched off for that example — other units, and the same
unit on other examples, still pass a full-strength gradient. Sigmoid is flat at <em>both</em> ends,
so a unit that is confidently anything is always attenuating, and every unit in every layer
attenuates simultaneously. One is a switch; the other is a leak in every pipe at once.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Using sigmoid in hidden layers because it feels more “neural”.</b> It trains
noticeably slower and it is the classic cause of a deep network that will not learn at all.</p>""")
        + trap("""<p><b>Using ReLU on the output of a binary classifier.</b> ReLU can output 7.3, which is
not a probability. Output layers must match the question — see the next lesson.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("ReLU(−3) and ReLU(0.4)?",
             "<p><b>0</b> and <b>0.4</b>. Negative becomes zero; positive passes through unchanged.</p>"),
            ("Why does a slope near zero stop learning?",
             "<p>Gradient descent moves by α × slope. Slope ≈ 0 means the step size is ≈ 0 — the weight "
             "barely moves no matter how wrong it is.</p>"),
            ("What is a “dead” ReLU unit and why is it permanent?",
             "<p>A unit whose z is negative for every training example. Its gradient is 0 always, so its "
             "weights never update, so its z never changes. A lower learning rate or a Leaky ReLU avoids it.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("paper", "https://proceedings.mlr.press/v15/glorot11a.html",
             "Glorot, Bordes & Bengio (2011) — Deep Sparse Rectifier Neural Networks",
             "The paper that made the case for ReLU. Readable, and the sparsity argument is elegant."),
            ("paper", "https://www.cs.toronto.edu/~fritz/absps/reluICML.pdf",
             "Nair & Hinton (2010) — Rectified linear units improve restricted Boltzmann machines",
             "The earlier result that introduced ReLU to deep networks."),
            ("docs", "https://cs231n.github.io/neural-networks-1/#actfun",
             "CS231n — commonly used activation functions",
             "Every variant, with honest pros and cons including the dying-ReLU problem."),
            ("lab", "../../C2%20-%20Advanced%20Learning%20Algorithms/week2/optional-labs/C2_W2_Relu.ipynb",
             "Optional lab: ReLU",
             "In this repo. Shows ReLU units switching on one by one to build a piecewise function."),
        ])
    )))

# ============================================================ 4
L.append(dict(
    slug="04-choosing-activations", title="Choosing activation functions", mins=9, tag="core",
    lede="A short lesson with a genuinely useful rule: ReLU inside, and let the output layer match the "
         "shape of the question.",
    body=(
        pretest("""<p>Hidden layers and the output layer. <b>Guess whether they should use the same activation function</b>, and what decides the output one.</p>""",
        """<p>Watch for the rule: the output activation is decided by what you are predicting, hidden layers almost always get ReLU.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>The last layer is the one that speaks to you, so it has to speak the right language.</p>
<ul><li>If the answer is “yes or no”, it must say a chance between 0 and 1 → <b>sigmoid</b>.</li>
<li>If the answer is a number that could be negative (a temperature change) → <b>linear</b>.</li>
<li>If the answer is a number that can’t be negative (a price) → <b>ReLU</b>.</li>
<li>If the answer is “which one of these ten?” → <b>softmax</b>.</li></ul>
<p>The middle layers don’t talk to you at all, so they don’t need to be polite: use ReLU and stop
thinking about it.</p>""")

        + h2("🎬", "Watch it move")
        + demo("actchoice", "Pick your problem, get your activation",
               "hidden layers are always the same; only the output changes")

        + h2("🔢", "The rules, written down")
        + table(["Output layer", "Task", "Why", "Keras"],
                [["<b>sigmoid</b>", "binary classification", "must be a probability in 0…1", "<code>Dense(1, activation='sigmoid')</code>"],
                 ["<b>linear</b>", "regression, any sign", "the answer can be −3 or +12", "<code>Dense(1, activation='linear')</code>"],
                 ["<b>ReLU</b>", "regression, non-negative", "prices, counts, durations", "<code>Dense(1, activation='relu')</code>"],
                 ["<b>softmax</b>", "multiclass, one answer", "probabilities across classes summing to 1", "<code>Dense(10, activation='softmax')</code>"],
                 ["<b>ReLU</b>", "<i>every hidden layer</i>", "fast, and gradients survive", "<code>Dense(25, activation='relu')</code>"]])
        + key("""<p>“Linear activation” means <em>no activation</em>: g(z) = z. Keras calls it
<code>'linear'</code> and it is the default if you omit the argument. Saying “no activation function” and
“linear activation function” are the same sentence.</p>""")

        + h2("🔬", "Why not sigmoid in hidden layers, one more time")
        + """<p>Three independent reasons, any one of which would be enough:</p>
<ol>
<li><b>Speed.</b> <code>exp</code> and division are far more expensive than <code>max</code>, and you do
this hundreds of millions of times per epoch.</li>
<li><b>Gradients.</b> Sigmoid’s slope peaks at 0.25. Stack ten layers and the multiplied slope is at best
0.25¹⁰ ≈ 0.000001. The early layers receive essentially no signal.</li>
<li><b>Empirics.</b> Networks with ReLU hidden layers simply train faster and reach better minima.</li>
</ol>"""

        + h2("🔤", "The words, decoded")
        + decode([
            ("activation function", "“the squasher”", "The g applied after the weighted sum. What makes a network more than a stack of straight lines."),
            ("output layer", "“the last layer”", "Its activation is decided by the <b>problem</b>: sigmoid for binary, linear for any-sign regression, ReLU for never-negative."),
            ("hidden layer", "“a middle layer”", "Any layer that is not the output. ReLU, almost always."),
            ("vanishing gradient", "“the gradient dies”", "Slopes multiplied together shrink towards zero, so early layers stop learning. Sigmoid's flat tails cause it; ReLU's slope of 1 does not."),
        ])
        + h2("🕳", "Traps")
        + trap("""<p><b>Mixing up multi-class and multi-label.</b> Softmax = exactly one answer is correct.
Several sigmoids = several answers can be correct at once. Lesson 10 covers this in full.</p>""")
        + trap("""<p><b>Using ReLU on the output for a price prediction and being surprised at all the
zeros.</b> ReLU floors at 0, so the model can never predict a small positive value smoothly near the
boundary. If some outputs really should be 0, that’s a feature; if not, use linear.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("Predicting tomorrow’s temperature change in °C. Output activation?",
             "<p><b>linear</b> — the answer can be negative.</p>"),
            ("Classifying an X-ray into one of 5 diagnoses. Output layer?",
             "<p><code>Dense(5, activation='softmax')</code> — five units, one softmax across them.</p>"),
            ("Someone hands you a 12-layer net using sigmoid everywhere that will not train. First fix?",
             "<p>Change every hidden layer to ReLU. Vanishing gradients through 12 sigmoids is almost "
             "certainly the cause.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("docs", "https://keras.io/api/layers/activations/",
             "Keras — the full activation list",
             "Includes gelu, selu, swish. Worth knowing they exist; not needed for this course."),
            ("paper", "https://arxiv.org/abs/1710.05941",
             "Ramachandran, Zoph & Le (2017) — Searching for Activation Functions (Swish)",
             "Google searched the space of activation functions automatically. The winner barely beats ReLU — "
             "which is itself an interesting result."),
        ])
    )))

# ============================================================ 5
L.append(dict(
    slug="05-why-activations", title="Why do we need activation functions?", mins=14, tag="maths",
    lede="The three-line proof that a network with no activation function is just a very expensive straight "
         "line — and the picture of what non-linearity buys you.",
    body=(
        pretest("""<p>Take away the activation functions entirely — every layer is just Wx + b. <b>Guess what a 100-layer network can then compute.</b></p>""",
        """<p>Try composing two of them algebraically before reading. Watch for what the answer says about why non-linearity is not optional.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Take a straight stick. Tape another straight stick to the end of it, perfectly in line.
What do you have? A longer straight stick.</p>
<p>Do it a hundred times. Still a straight stick.</p>
<p>Layers with no activation function are exactly that. To make a <b>bend</b>, at least one joint has to be
allowed to <em>not</em> be straight. The activation function is the joint.</p>""")

        + h2("🔢", "The proof, in three lines")
        + eqp([
            '<var>a</var><sup>[1]</sup> = ',
            ('<var>W</var><sup>[1]</sup><var>x</var>', "matmul-f0", "whole layer, one multiply"),
            ' + <var>b</var><sup>[1]</sup>',
        ], "layer 1, with a linear activation — hover or click it", small=True)
        + eqp([
            '<var>a</var><sup>[2]</sup> = ',
            ('<var>W</var><sup>[2]</sup><var>a</var><sup>[1]</sup>', "matmul-f0", "whole layer, one multiply"),
            ' + <var>b</var><sup>[2]</sup> = <var>W</var><sup>[2]</sup>(',
            ('<var>W</var><sup>[1]</sup><var>x</var>', "matmul-f0", "whole layer, one multiply"),
            ' + <var>b</var><sup>[1]</sup>) + <var>b</var><sup>[2]</sup>',
        ], "substitute layer 1 into layer 2 — hover or click a part", small=True)
        + eqp([
            '<var>a</var><sup>[2]</sup> = ',
            ('<span class="hl-a">(<var>W</var><sup>[2]</sup><var>W</var><sup>[1]</sup>)</span>', "matmul-f0", "two matrices collapse into one"),
            '<var>x</var> + <span class="hl-a">(<var>W</var><sup>[2]</sup><var>b</var><sup>[1]</sup> + <var>b</var><sup>[2]</sup>)</span> = <var>W</var>′<var>x</var> + <var>b</var>′',
        ], "multiply out — and it collapses to a single layer — hover or click it")
        + """<p>The two matrices multiplied together are <em>just another matrix</em>. The two biases
combined are <em>just another vector</em>. Your two-layer network is algebraically identical to a
one-layer network. Add a hundred layers and it is <em>still</em> identical to a one-layer network.</p>"""
        + key("""<p>Without a non-linear g, depth buys you <b>nothing at all</b> — not less accuracy, exactly
zero extra expressive power. All those parameters, and you have re-derived linear regression.</p>""")

        + h2("🧮", "A worked example, with real numbers")
        + """<p>Let layer 1 be a<sup>[1]</sup> = 2x + 1, and layer 2 be a<sup>[2]</sup> = 3a<sup>[1]</sup> − 1
(so W<sup>[1]</sup> = 2, b<sup>[1]</sup> = 1, W<sup>[2]</sup> = 3, b<sup>[2]</sup> = −1). Feed in x = 5:</p>
<ul>
<li>Layer 1: a<sup>[1]</sup> = 2(5) + 1 = <b>11</b>.</li>
<li>Layer 2: a<sup>[2]</sup> = 3(11) − 1 = <b>32</b>.</li>
</ul>
<p>Now collapse them first, then feed in x = 5 once: W′ = W<sup>[2]</sup>W<sup>[1]</sup> = 3×2 = 6, and
b′ = W<sup>[2]</sup>b<sup>[1]</sup> + b<sup>[2]</sup> = 3×1 − 1 = 2. So a′ = 6x + 2 = 6(5) + 2 =
<b>32</b> — the same answer, with one multiply-add instead of two.</p>"""
        + code("""
def layer(x, W, b):
    return W @ x + b

x  = np.array([5.0])
W1, b1 = np.array([[2.0]]), np.array([1.0])
W2, b2 = np.array([[3.0]]), np.array([-1.0])

a1 = layer(x, W1, b1)
a2 = layer(a1, W2, b2)                     # two linear layers, run in sequence

W_combined = W2 @ W1
b_combined = W2 @ b1 + b2
direct = layer(x, W_combined, b_combined)  # one combined layer

a2, direct     # (array([32.]), array([32.])) -- identical, for any x
""")

        + explain("""<p>Two linear layers collapsed to <code>6x + 2</code>. <b>Why does no amount of depth escape this?</b></p>""",
            """<p>Because a linear function of a linear function is linear, and that argument applies again to the result. Each collapse produces something of the same form, so it can be collapsed again — a hundred times if need be. Depth adds parameters and no new expressive power.</p>""")
                + lenses(
            """<p>Three translators in a row, each translating word-for-word with no interpretation.</p>
<p>English → French → German → Russian. You could have hired one translator to go straight from
English to Russian and got the identical result. The chain bought you nothing, because none of them
added anything of their own.</p>
<p>That is a network with no activation functions: however many layers, it collapses into one.</p>""",
            """<p>Formally: the composition of linear maps is a linear map. Multiply matrices
<var>W</var>₂(<var>W</var>₁<var>x</var>) and you can pre-multiply them into a single
<var>W</var> — with fewer parameters and identical behaviour.</p>
<p>Anyone with linear algebra can see immediately that depth without non-linearity is not merely
inefficient, it is provably pointless. The activation function is what breaks that collapse.</p>""",
            """<p>A stack of flat sheets of glass, versus a stack of lenses.</p>
<p>Light through ten sheets of flat glass comes out going the same way it went in — you could have used
one sheet. Each lens bends it, so ten lenses can do something no single lens can. The activation is
the curvature.</p>""",
            """<p>This is the reason the field stalled for decades. The 1969 critique of the perceptron showed a
single linear layer cannot learn XOR, and without a workable way to train non-linear multi-layer
networks the interest drained away — the first “AI winter”.</p>
<p>The non-linearity is not a refinement. It is the difference between a model that can only draw
straight lines and one that can, in principle, approximate anything.</p>""",
            """So the three-line proof below is worth following once carefully — it justifies every hidden layer
you will ever build.""")
        + h2("🎬", "Watch it move")
        + demo("relubuild", "Straight sticks vs. bent ones",
               "drag the slider to add ReLU units — each one adds exactly one kink")
        + """<p>The left panel is any number of linear layers: always a line. On the right, each ReLU unit
contributes one “knee” where its output stops being zero and starts rising. Enough knees, positioned and
scaled by training, and you can trace any curve you like.</p>"""

        + h2("🔬", "Universal approximation, honestly stated")
        + """<p>The theorem (Cybenko 1989, Hornik 1991) says: a network with <b>one</b> hidden layer and
enough units can approximate any continuous function on a bounded region, to any accuracy you like.</p>"""
        + warn("""<p>Read the small print. The theorem says such a network <em>exists</em>. It does not say
you can <b>find</b> it with gradient descent, or that the number of units needed is reasonable, or that it
will generalise to new data. Depth matters in practice precisely because deep networks need exponentially
fewer units than shallow ones for many functions.</p>""")

        + h2("🔤", "The words, decoded")
        + decode([
            ("linear function", "“a straight line”", "f(x) = wx + b. Composing two of them gives another one — which is the whole problem."),
            ("composition", "“a function of a function”", "Feeding one layer's output into the next. With linear layers it collapses; with a non-linearity it does not."),
            ("expressive power", "“what it can represent”", "The set of shapes a model can take. Adding linear layers adds parameters and no expressive power at all."),
            ("universal approximation", "“it can fit anything”", "The theorem that a big enough one-hidden-layer network can approximate any continuous function. True, and much less useful than it sounds — it says nothing about whether you can <em>find</em> those weights."),
        ])
        + h2("🕳", "Traps")
        + trap("""<p><b>“Linear activation is a kind of activation, so I’m fine.”</b> No. Linear is the
identity, and identity functions compose into the identity. It has to be genuinely non-linear.</p>""")
        + trap("""<p><b>Putting linear in hidden layers to “keep things simple”.</b> This silently reduces
your entire network to logistic regression. It will train — badly — and you will not get an error message.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("A 100-layer network with linear activation everywhere and a sigmoid output. What is it equivalent to?",
             "<p>Plain <b>logistic regression</b>. All 100 linear layers collapse into one matrix, then the "
             "sigmoid is applied. Millions of parameters, zero extra power.</p>"),
            ("Why does a single ReLU unit add exactly one “kink”?",
             "<p>Because ReLU changes behaviour at exactly one point: z = 0. Where the unit’s "
             "w·x + b crosses zero, its contribution switches from flat to sloped.</p>"),
            ("If universal approximation holds for one hidden layer, why do we build deep networks?",
             "<p>Because “enough units” can mean astronomically many. Depth lets you reuse intermediate "
             "features, which is exponentially more efficient for the functions we care about — and it is "
             "what gradient descent actually manages to find.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("paper", "https://link.springer.com/article/10.1007/BF02551274",
             "Cybenko (1989) — Approximation by superpositions of a sigmoidal function",
             "The original universal approximation theorem."),
            ("paper", "https://www.sciencedirect.com/science/article/abs/pii/089360809190009T",
             "Hornik (1991) — Approximation capabilities of multilayer feedforward networks",
             "Generalises Cybenko: it is the depth and the non-linearity that matter, not the specific squashing function."),
            ("play", "https://playground.tensorflow.org/#activation=linear&dataset=spiral",
             "Playground: set activation to Linear on the spiral dataset",
             "Watch a deep network fail completely. Then switch to ReLU. This takes 60 seconds and you will never forget it."),
        ])
    )))

# ============================================================ 6
L.append(dict(
    slug="06-multiclass", title="Multiclass classification", mins=8, tag="intuition",
    lede="From “is it a 1?” to “which of the ten digits is it?” — what changes, and what stays exactly "
         "the same.",
    body=(
        pretest("""<p>Not spam-or-not, but which of ten handwritten digits. <b>Guess what has to change about the output layer.</b></p>""",
        """<p>Watch for how many outputs you need, and for what they must collectively add up to.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Before, you had one question with two answers: yes or no. One number told you
everything, because “70% yes” automatically means “30% no”.</p>
<p>Now you have <b>ten</b> possible answers — is it a 0, a 1, a 2, … a 9? One number isn’t enough any more.
You need ten numbers, one per digit, and they have to share a budget of 100%.</p>""")

        + h2("🔢", "The maths, decoded")
        + eq("""<var>y</var> <span class="op">∈</span> {1, 2, …, <var>N</var>}
&nbsp;&nbsp;&nbsp;
<var>P</var>(<var>y</var> = <var>j</var> | <var>x</var>) for each <var>j</var>""",
             "the target is now one of N labels, not just 0 or 1")
        + decode([
            ("<var>N</var>", "“the number of classes”", "10 for digits, 3 for iris species, 2 for the binary case you already know."),
            ("<var>y</var> ∈ {1..N}", "“y is one of these”", "A category, not a quantity. Class 7 is not “bigger” than class 3 — the numbers are just names."),
            ("P(y=j | x)", "“probability of class j given x”", "One number per class. All N of them must sum to exactly 1."),
            ("multiclass", "“pick exactly one”", "Mutually exclusive. A digit cannot be both a 3 and an 8."),
        ])
        + note("""<p>Binary classification is just multiclass with N = 2. Sigmoid is exactly what softmax
reduces to when N = 2. Nothing is being replaced here — the general case is being unlocked.</p>""",
               "The special case you already know")

        + h2("🎬", "Watch it move")
        + demo("multiclass", "Two classes vs. four",
               "toggle between one boundary and four regions, and watch the output layer change shape")

        + h2("🌍", "Where this shows up")
        + grid3(
            card("<h3>Handwriting</h3><p>10 digits. The Week 2 assignment, and the original MNIST benchmark "
                 "that defined the field for a decade.</p>"),
            card("<h3>Manufacturing</h3><p>Is this defect a scratch, a dent, a discolouration, or a chip? "
                 "One label per part.</p>"),
            card("<h3>Medicine</h3><p>Which of five disease stages does this scan show? Note that here the "
                 "classes have an <em>order</em>, which plain multiclass ignores.</p>"))

        + h2("🕳", "Traps")
        + trap("""<p><b>Treating class labels as numbers.</b> If you feed “class = 7” into a regression, the
model will think 7 is closer to 6 than to 2. For unordered categories that is nonsense — which is why
you use N output units, not one.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("How many output units for a 10-digit classifier? For a yes/no classifier?",
             "<p><b>10</b> with softmax, and <b>1</b> with sigmoid. (You <em>could</em> use 2 with softmax "
             "for the binary case — it is equivalent, just wasteful.)</p>"),
            ("Your model outputs [0.1, 0.5, 0.2] for a 3-class problem. Anything wrong?",
             "<p>Yes — they sum to 0.8, not 1. Either it is not a softmax, or something has gone wrong. "
             "Softmax outputs always sum to 1.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("docs", "https://scikit-learn.org/stable/modules/multiclass.html",
             "scikit-learn — multiclass and multioutput algorithms",
             "A clear taxonomy: multiclass vs multilabel vs multioutput. Worth reading once to fix the vocabulary."),
            ("lab", "../../C2%20-%20Advanced%20Learning%20Algorithms/week2/optional-labs/C2_W2_Multiclass_TF.ipynb",
             "Optional lab: Multiclass classification",
             "In this repo. Four blobs, four output units, and a plot of the regions the network carves out."),
        ])
    )))

# ============================================================ 7
L.append(dict(
    slug="07-softmax", title="Softmax", mins=16, tag="maths",
    lede="The generalisation of sigmoid to N classes. Two moves — exponentiate, then divide by the total — "
         "and every property you need follows from them.",
    body=(
        pretest("""<p>Ten raw scores, some negative, adding to nothing in particular. You need ten probabilities adding to exactly 1. <b>Guess the two moves that get you there.</b></p>""",
        """<p>Make everything positive, then share out the total. Watch for why exponentiating is the natural way to do the first.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Ten judges each shout a score. Some scores are negative, some are huge, and they don’t
add up to anything sensible. You need to turn them into “what fraction of the vote did each judge win?”</p>
<p>Two moves:</p>
<ol><li><b>Make everything positive.</b> Raise <var>e</var> to the power of each score. Negative scores
become small positive numbers; big scores become very big positive numbers. Nothing is negative any more.</li>
<li><b>Share out the budget.</b> Add them all up, then divide each one by that total. Now they add to
exactly 1.</li></ol>
<p>That’s softmax. The name means “a soft version of picking the maximum” — instead of the winner taking
everything, the winner takes most of it and the others keep a little.</p>""")

        + h2("🔢", "The maths, decoded")
        + eqp([
            '<var>z</var><sub><var>j</var></sub> <span class="op">=</span> ',
            ("<var>w</var><sub><var>j</var></sub> · <var>x</var>", "dot-product-f0", "multiply matching entries, add them up"),
            ' <span class="op">+</span> <var>b</var><sub><var>j</var></sub> <span class="op">&nbsp;&nbsp;for&nbsp;&nbsp;</span> <var>j</var> <span class="op">=</span> 1 … <var>N</var>',
        ], "step 1 — one score per class, exactly as before — hover or click a part")
        + eqp([
            '<var>a</var><sub><var>j</var></sub> <span class="op">=</span> ',
            ('<span class="frac"><span><var>e</var><sup><var>z</var><sub><var>j</var></sub></sup></span>'
             '<span><var>e</var><sup><var>z</var><sub>1</sub></sup> + <var>e</var><sup><var>z</var><sub>2</sub></sup> + … + <var>e</var><sup><var>z</var><sub><var>N</var></sub></sup></span></span>',
             "softmax-native", "turns scores into probabilities"),
            ' <span class="op">=</span> <var>P</var>(<var>y</var> = <var>j</var> | <var>x</var>)',
        ], "step 2 — softmax — hover or click it")
        + decode([
            ("<var>e</var><sup><var>z</var></sup>", "“e to the z”", "Always positive, and it grows fast. It turns differences in z into ratios in a."),
            ("the denominator", "“the total”", "The same sum for every class — that is the shared budget everyone divides into."),
            ("<var>a</var><sub><var>j</var></sub>", "“a sub j”", "The probability of class j. Between 0 and 1, and Σa<sub>j</sub> = 1 by construction."),
            ("soft-max", "“a gentle argmax”", "If one z is far above the rest, its a → 1 and the others → 0. If they are close, the probabilities are close."),
        ])
        + key("""<p>Softmax is the <b>only</b> activation in this course where each output depends on all
the other outputs. Every other activation squashes its own z alone. That coupling is what makes the
probabilities sum to 1.</p>""")

                + lenses(
            """<p>Dividing a bonus pot between four sales staff by performance.</p>
<p>Everyone gets something, the whole pot is handed out, and the best performer gets the largest share.
Two constraints — nothing negative, and it all adds to 100% — and those two are exactly what softmax
enforces on a set of scores.</p>""",
            """<p>This is the multinomial extension of the logistic function — in statistics, multinomial logistic
regression. Where sigmoid produced one probability, softmax produces a full distribution over N
categories.</p>
<p>The exponential is not decoration: it guarantees positivity and it makes the result depend only on
score <em>differences</em>, which is why adding a constant to every score changes nothing.</p>""",
            """<p>A pie chart that redraws itself as you change the numbers.</p>
<p>Push one score up and its slice grows — and everyone else’s shrinks, even though their own scores
never moved. The pie is always exactly one pie. That forced competition is what makes softmax right
for “pick one” and wrong for “tick all that apply”.</p>""",
            """<p>Every language model, including the one writing this, ends in a softmax — over roughly 50,000
possible next tokens, at every single step of generation.</p>
<p>The temperature setting you may have seen in an API is a divisor applied to the scores just before
this function. Low temperature sharpens the distribution towards the top choice; high temperature
flattens it. That is the whole mechanism behind “creative” versus “deterministic” output.</p>""",
            """So exponentiating and normalising below is the operation sitting at the end of nearly every
classifier in production today.""")
        + h2("🎬", "Watch it move")
        + demo("softmax", "Raw scores → positive → shares of 1",
               "drag any z and watch every other probability move in response")
        + """<p>Raise z₁ and watch z₂, z₃ and z₄’s probabilities all fall, even though their own scores
did not change. They are competing for the same 100%.</p>"""

        + h2("🧮", "A worked example on paper")
        + table(["Class", "z", "e^z", "a = e^z / Σ"],
                [["1", "2.0", "7.39", "<b>0.649</b>"],
                 ["2", "1.0", "2.72", "<b>0.239</b>"],
                 ["3", "0.1", "1.11", "<b>0.097</b>"],
                 ["4", "−0.5", "0.61", "<b>0.054</b>"],
                 ["", "", "Σ = 11.83", "Σ = <b>1.000</b>"]])
        + """<p>Note how a gap of 1.0 in z becomes a ratio of about 2.7× in probability — that is
<var>e</var>¹. Softmax converts <em>differences</em> in scores into <em>ratios</em> in probability, which
is exactly the behaviour you want from evidence.</p>"""

        + explain("""<p>Raising one z made every other probability fall, though their own scores never changed. <b>Why?</b></p>""",
            """<p>Because they share a denominator. Every output is divided by the same total, so growing one term grows the total and shrinks everyone else's share. The outputs are competing for a fixed 100% — which is exactly what makes them a probability distribution.</p>""")
        + h2("🔢", "And the loss that goes with it")
        + eqp([
            ('<var>L</var> <span class="op">=</span> <span class="op">−</span>log(<var>a</var><sub><var>y</var></sub>)', "logarithm-f0", "huge penalty if the true class's probability is near 0"),
        ], "sparse categorical cross-entropy — only the TRUE class’s probability is scored — hover or click it")
        + """<p>That is the whole loss. If the true class is 3 and the model gave class 3 a probability of
0.097, the loss is −log(0.097) = 2.33. If it had given class 3 a probability of 0.9, the loss would be
0.105. The other nine probabilities never appear — but pushing a<sub>3</sub> up necessarily pushes the
others down, because they share a budget.</p>"""

        + h2("🕳", "Traps")
        + trap("""<p><b>Applying softmax twice.</b> Softmax of a softmax is a valid computation and a
completely wrong model. If your output layer already has <code>activation='softmax'</code>, do not also
pass <code>from_logits=True</code> to the loss.</p>""")
        + trap("""<p><b>Expecting softmax to say “I don’t know”.</b> It always sums to 1, so it always names
a most-likely class — even for an input completely unlike anything in training. Calibrated uncertainty is
a genuinely hard, separate problem.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("z = [1, 1, 1]. What is a?",
             "<p>[<b>1/3, 1/3, 1/3</b>]. Equal scores → equal probabilities, whatever their value.</p>"),
            ("z = [10, 1, 1] vs z = [110, 101, 101]. Do these give the same a?",
             "<p><b>Yes</b> — identical. Softmax only cares about <em>differences</em> between the z’s. "
             "Adding a constant to every z changes nothing. This fact is the basis of the numerical fix "
             "in Lesson 9.</p>"),
            ("With N = 2, show softmax reduces to sigmoid.",
             "<p>a₁ = e^z₁/(e^z₁+e^z₂) = 1/(1 + e^(z₂−z₁)) = sigmoid(z₁ − z₂). One sigmoid on the "
             "difference of the two scores.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("docs", "https://cs231n.github.io/linear-classify/#softmax",
             "CS231n — the softmax classifier",
             "Includes the information-theory reading of cross-entropy and a worked numerical-stability example."),
            ("paper", "https://link.springer.com/chapter/10.1007/978-3-642-76153-9_28",
             "Bridle (1990) — Probabilistic interpretation of feedforward classification network outputs",
             "Where the name and the probabilistic justification come from."),
            ("lab", "../../C2%20-%20Advanced%20Learning%20Algorithms/week2/optional-labs/C2_W2_SoftMax.ipynb",
             "Optional lab: Softmax",
             "In this repo. Plots how the probabilities shift as you move the z values."),
        ])
    )))

# ============================================================ 8
L.append(dict(
    slug="08-softmax-output-layer", title="Neural network with Softmax output", mins=13, tag="code",
    lede="Bolting softmax onto the end of a network: ten output units, one shared normalisation, and the "
         "code that trains it.",
    body=(
        pretest("""<p>Your network ends in 10 softmax units. <b>Guess how the loss knows which of the ten was correct</b> — and whether it scores all ten or just one.</p>""",
        """<p>Watch for which probability the loss actually looks at. Only one term survives.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Everything before the last layer stays exactly the same. You just widen the final panel
of judges from one seat to ten, and then make those ten share out 100% between them.</p>""")

        + h2("🔢", "The architecture")
        + eqp([
            '<var>x</var> → 25 ',
            ("ReLU", "relu-native", "0 below zero, unchanged above"),
            ' → 15 ',
            ("ReLU", "relu-native", "0 below zero, unchanged above"),
            ' → ',
            ('<span class="hl-a">10 softmax</span>', "softmax-native", "turns scores into probabilities"),
            ' → probabilities',
        ], "the Week 2 assignment network — hover or click a part", small=True)
        + """<p>Layers 1 and 2 are unchanged from a binary network. Only the output layer differs, in two
ways: it has 10 units instead of 1, and its activation couples those 10 units together.</p>"""
        + decode([
            ("<code>Dense(10)</code>", "“ten output units”", "One per class. Each has its own weight vector and bias — 10 separate z’s."),
            ("<code>activation='softmax'</code>", "“normalise across the ten”", "The only activation that reads all ten z’s to produce each a."),
            ("<code>SparseCategoricalCrossentropy</code>", "“the multiclass loss”", "“Sparse” = your labels are integers 0–9, not one-hot vectors."),
            ("<code>CategoricalCrossentropy</code>", "“the one-hot version”", "Same loss, but expects labels as [0,0,1,0,…]. Choose based on how your Y is stored."),
        ], head=("Piece", "Say it out loud", "What it does"))

        + h2("🎬", "Watch it move")
        + demo("softmaxnn", "Ten outputs, one shared budget",
               "the dashed box is the softmax — it spans all ten units at once")

        + h2("💻", "In code (the version you will replace next lesson)")
        + code("""
model = Sequential([
    Dense(units=25, activation='relu'),
    Dense(units=15, activation='relu'),
    Dense(units=10, activation='softmax'),     # <- 10 units, softmax
])
model.compile(loss=SparseCategoricalCrossentropy())
model.fit(X, Y, epochs=100)

p = model.predict(X_new)      # shape (m, 10) — a row of 10 probabilities per example
pred = np.argmax(p, axis=1)   # the index of the largest = the predicted class
""")
        + warn("""<p>This code is <b>correct but not what you should ship</b>. Lesson 9 shows a numerically
better version that gives the same answers with less rounding error. Andrew teaches it in this order
deliberately: understand the honest version first, then the fast one.</p>""")

        + h2("🧮", "The output layer of the digit network")
        + """<p>The assignment’s last layer takes the 15 activations of layer 2 and produces 10
scores:</p>"""
        + table(["", "shape", "count"],
                [["<var>W</var><sup>[3]</sup>", "(15, 10)", "150 weights"],
                 ["<var>b</var><sup>[3]</sup>", "(10,)", "10 biases"],
                 ["output <var>z</var><sup>[3]</sup>", "(1, 10)", "one score per digit"]])
        + """<p>Ten units, one per class — and each one is an ordinary neuron with its own weights.
What makes the layer a <em>softmax</em> layer is not the units, it is the single step applied to all
ten scores together afterwards, which divides each by the total so they sum to 1.</p>
<p>That coupling is the whole difference from everything before it. In every previous layer, unit 3
could be computed without ever looking at unit 7. Here it cannot: <var>a</var><sub>3</sub> depends
on <var>z</var><sub>7</sub> through the shared denominator. Push one score up and every other
probability falls, whether or not its own score changed.</p>"""
        + explain("""<p>Softmax is monotonic: the largest <var>z</var> always becomes the largest
<var>a</var>. <b>So why compute it at prediction time at all?</b></p>""",
                  """<p>For the <em>decision</em>, you needn’t — <code>np.argmax(z)</code> and
<code>np.argmax(softmax(z))</code> always agree, which is exactly why the preferred implementation
can leave the last layer linear and still classify correctly. You compute it when you want the
<em>confidence</em>: “digit 3, and I am 0.97 sure” is a different and often more useful answer than
“digit 3”, and a raw score of 4.2 is not interpretable on its own.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Forgetting <code>argmax</code>.</b> <code>predict</code> gives you ten probabilities,
not a digit. <code>np.argmax(p, axis=1)</code> turns each row into the winning class index.</p>""")
        + trap("""<p><b>Getting <code>axis</code> wrong.</b> <code>axis=1</code> takes the max across each
row (per example). <code>axis=0</code> takes it down each column, which asks a completely different and
useless question.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("How many parameters in the output layer of 15 → 10 with softmax?",
             "<p>15 × 10 = 150 weights + 10 biases = <b>160</b>. Softmax itself has no parameters at all — "
             "it is a fixed formula.</p>"),
            ("predict returns shape (500, 10). What is in row 3?",
             "<p>The ten class probabilities for training example 3, summing to 1.</p>"),
            ("Your labels are stored as [[0,0,1],[1,0,0],…]. Which loss?",
             "<p><code>CategoricalCrossentropy</code> — the one-hot version. Use "
             "<code>SparseCategoricalCrossentropy</code> when labels are plain integers.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("docs", "https://www.tensorflow.org/api_docs/python/tf/keras/losses/SparseCategoricalCrossentropy",
             "tf.keras.losses.SparseCategoricalCrossentropy",
             "Read the from_logits note at the top — it is the subject of the next lesson."),
            ("lab", "../../C2%20-%20Advanced%20Learning%20Algorithms/week2/C2W2A1/C2_W2_Assignment.ipynb",
             "Week 2 assignment — handwritten digits, all ten",
             "In this repo. This exact architecture, trained on 5000 20×20 images."),
        ])
    )))

# ============================================================ 9
L.append(dict(
    slug="09-improved-softmax", title="Improved implementation of softmax", mins=15, tag="core",
    lede="Why `from_logits=True` exists. A short lesson about floating-point arithmetic that will save you "
         "from a class of bug that is invisible until it isn’t.",
    body=(
        pretest("""<p>The obvious implementation computes the probability, then takes its log. <b>Guess what goes wrong numerically</b> when the probability is very small.</p>""",
        """<p>Watch for <code>from_logits=True</code>, and for why rearranging the algebra avoids a rounding step that destroys the answer.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Imagine a calculator that only keeps 7 digits. Ask it for 1/3 and it says 0.3333333 —
close, but slightly wrong. Now multiply that by 3: you get 0.9999999, not 1.</p>
<p>One rounding is harmless. But if you round, then round the rounded number, then round <em>that</em>, the
errors pile up. Sometimes they pile up so badly that the answer is 0 when it should be 0.0000001 — and then
you take a logarithm of 0 and everything explodes.</p>
<p>The fix isn’t a better calculator. The fix is to <b>rearrange the sum</b> so the dangerous middle step
never happens.</p>""")

        + h2("🔢", "The maths, decoded")
        + """<p>The naive route computes <var>a</var> first, then the loss:</p>"""
        + eqp([
            ('<var>a</var> = <span class="frac"><span>1</span><span>1 + <var>e</var><sup>−<var>z</var></sup></span></span>', "sigmoid-squash", "the squasher"),
            ' &nbsp;&nbsp;then&nbsp;&nbsp; ',
            ('<var>L</var> = −log(<var>a</var>)', "logarithm-f0", "huge penalty if a is near 0"),
        ], "two steps — a gets rounded before log ever sees it — hover or click a part", small=True)
        + """<p>The stable route substitutes one into the other and simplifies, so <var>a</var> is never
built at all:</p>"""
        + eqp([
            ('<var>L</var> = −log<span class="paren">(</span><span class="frac"><span>1</span><span>1 + <var>e</var><sup>−<var>z</var></sup></span></span><span class="paren">)</span> = log(1 + <var>e</var><sup>−<var>z</var></sup>)',
             "logarithm-f0", "same loss, one rounding step instead of two"),
        ], "one step, algebraically identical, numerically far safer — hover or click it")
        + decode([
            ("logits", "“the raw z’s”", "The scores <em>before</em> any sigmoid or softmax. The word is standard everywhere in ML."),
            ("<code>from_logits=True</code>", "“I’ll give you z, not a”", "Tells Keras to do the squashing inside the loss, using the rearranged formula."),
            ("<code>activation='linear'</code>", "“don’t squash”", "The output layer now emits raw z. Required when from_logits=True."),
            ("float32", "“7 decimal digits”", "The default precision. Roughly 7 significant digits — enough until you subtract two nearly-equal numbers."),
        ])

        + h2("🎬", "Watch it move")
        + demo("numstab", "The round-trip vs. the direct route",
               "drag z past ±16 and watch the naive path lose the answer entirely")
        + """<p>At z = 20, sigmoid(z) = 0.999999998. In float32 that rounds to exactly 1.0, so −log(a) = 0:
the model is told it made <em>no error at all</em>, and learning stops. The direct formula gives
2.06 × 10⁻⁹ — small, but not zero, and still a usable gradient.</p>"""

        + h2("💻", "The two versions")
        + grid2(
            card("<h3>❌ Naive</h3><pre style='margin:8px 0'><code>Dense(10, activation='softmax')\n"
                 "...\nmodel.compile(\n  loss=SparseCategoricalCrossentropy()\n)\n\n"
                 "p = model.predict(X)   # probabilities</code></pre>"),
            card("<h3>✅ Stable</h3><pre style='margin:8px 0'><code>Dense(10, activation='linear')\n"
                 "...\nmodel.compile(\n  loss=SparseCategoricalCrossentropy(\n"
                 "          from_logits=True)\n)\n\n"
                 "logits = model.predict(X)\np = tf.nn.softmax(logits)</code></pre>"))
        + warn("""<p>The catch, and it is the one everybody hits: with <code>from_logits=True</code> your
model’s output is <b>no longer a probability</b>. <code>predict</code> returns raw scores that can be
negative or above 1. You must apply <code>tf.nn.softmax()</code> yourself before interpreting them.</p>""")

        + h2("🔬", "Why exp is so dangerous")
        + """<p>Two failure modes, and softmax has both:</p>
<ul>
<li><b>Overflow.</b> <code>exp(1000)</code> is larger than any float32 can hold → <code>inf</code>. Then
<code>inf/inf</code> → <code>NaN</code>, and every weight in the network becomes NaN on the next update.</li>
<li><b>Underflow.</b> <code>exp(−1000)</code> → exactly 0. Then <code>log(0)</code> → <code>−inf</code>.</li>
</ul>
<p>The standard trick, which the framework applies for you: subtract the largest z before exponentiating.
From Lesson 7 you know softmax is unchanged by adding a constant to every z, so this is free —
<code>exp(z − max(z))</code> has a largest term of exactly <code>exp(0) = 1</code> and can never overflow.</p>"""

        + h2("🧮", "What actually goes wrong — run it and see")
        + """<p>Softmax on a well-behaved vector is fine:</p>"""
        + code("""
z = np.array([1., 2., 3., 4.])
np.exp(z) / np.exp(z).sum()        # -> [0.0321 0.0871 0.2369 0.6439]
""")
        + """<p>Now add 1000 to every score. Mathematically <b>nothing should change</b> — softmax
only cares about differences between scores, and every difference is identical. In floating point:</p>"""
        + code("""
z = np.array([1001., 1002., 1003., 1004.])
np.exp(z) / np.exp(z).sum()        # -> [nan nan nan nan]     RuntimeWarning: overflow
""")
        + """<p>Every answer destroyed. <code>e¹⁰⁰⁴</code> is about 10⁴³⁶, and a 64-bit float stops at
roughly 10³⁰⁸, so <code>np.exp</code> returns <code>inf</code> and <code>inf/inf</code> is
<code>nan</code>. Subtract the largest score first and the identical formula returns
<b>[0.0321, 0.0871, 0.2369, 0.6439]</b> — correct to the last digit.</p>
<p>The second failure is quieter. The loss needs log(<var>a</var>), and if <var>a</var> has already
been rounded to 1e−12 on its way through the exponential, then log of it is −27.63 — a number
computed from almost no surviving precision. Passing <code>from_logits=True</code> lets TensorFlow
keep the raw scores and rearrange log(e<sup>z</sup>/Σe<sup>z</sup>) algebraically before evaluating
anything, so neither failure can occur.</p>"""
        + warn("""<p>The cost of the fix: <code>model.predict</code> now returns raw scores, not
probabilities. They can be negative and will not sum to 1. Call
<code>tf.nn.softmax(...)</code> yourself when you want probabilities.</p>""")
        + explain("""<p>Subtracting the maximum score from every score changes the answer not at all.
<b>Why is it exactly cancelling?</b></p>""",
                  """<p>Write it out. Each numerator becomes e<sup>z−c</sup> = e<sup>z</sup>·e<sup>−c</sup>,
and the denominator becomes Σe<sup>z</sup>·e<sup>−c</sup> = e<sup>−c</sup>Σe<sup>z</sup>. The
factor e<sup>−c</sup> appears once above and once below, so it cancels — the ratio is untouched.
Choosing <var>c</var> as the maximum simply guarantees the largest exponent is e⁰ = 1, so nothing
can overflow.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Setting <code>from_logits=True</code> while leaving <code>activation='softmax'</code>.</b>
Now softmax is applied twice. Training will “work” and the model will be quietly wrong. Change both or
neither.</p>""")
        + trap("""<p><b>Reporting logits as confidences.</b> A logit of 8.2 is not 82%. Run it through
softmax first, or your dashboard will lie to your users.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("Why is log(1 + e^−z) better than −log(sigmoid(z)) when they are algebraically identical?",
             "<p>Because the first never builds the intermediate value that rounds to exactly 1 or 0. "
             "Same maths, fewer chances to round.</p>"),
            ("With from_logits=True, what does model.predict return and how do you get probabilities?",
             "<p>Raw logits. Apply <code>tf.nn.softmax(logits)</code> (or <code>tf.nn.sigmoid</code> for "
             "binary) to convert.</p>"),
            ("Softmax subtracts max(z) before exponentiating. Why is that safe?",
             "<p>Because softmax depends only on differences between the z’s. Subtracting the same constant "
             "from all of them leaves every probability unchanged, while making the largest exponent 0.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("docs", "https://cs231n.github.io/linear-classify/#softmax",
             "CS231n — “Practical issues: numeric stability”",
             "The max-subtraction trick, written out with numbers."),
            ("paper", "https://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html",
             "Goldberg (1991) — What Every Computer Scientist Should Know About Floating-Point Arithmetic",
             "The canonical reference. Long, but sections 1–2 explain every bug in this lesson."),
            ("docs", "https://www.tensorflow.org/api_docs/python/tf/nn/softmax",
             "tf.nn.softmax",
             "What you call on logits at prediction time."),
        ])
    )))

# ============================================================ 10
L.append(dict(
    slug="10-multi-label", title="Classification with multiple outputs (multi-label)", mins=12, tag="core",
    lede="A short but genuinely confusable distinction: several answers can be true at once, so softmax is "
         "the wrong tool.",
    body=(
        pretest("""<p>One photo, three questions: is there a car? a bus? a pedestrian? <b>Is this the same as multiclass?</b> Commit before reading.</p>""",
        """<p>Watch for what can be true simultaneously here but not in multiclass — and what that changes about the output activation.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>“Which single animal is this?” — cat, dog or horse. Exactly one is right. That’s
<b>multi-class</b>.</p>
<p>“Is there a car in this photo? Is there a bus? Is there a person?” — the answer could be yes, yes, yes.
Or no, no, no. They don’t compete. That’s <b>multi-label</b>.</p>
<p>Multi-class shares one budget of 100%. Multi-label gives every question its own separate 100%.</p>""")

        + h2("🎬", "Watch it move")
        + demo("multilabel", "Three questions, three independent answers",
               "toggle objects in the photo — the three probabilities move independently")

        + h2("🔢", "The maths, decoded")
        + table(["", "Multi-class", "Multi-label"],
                [["Question", "which ONE of N?", "which of N are present?"],
                 ["Target y", "a single integer, e.g. 7", "a vector, e.g. [1, 0, 1]"],
                 ["Output layer", "<code>Dense(N, 'softmax')</code>", "<code>Dense(N, 'sigmoid')</code>"],
                 ["Loss", "SparseCategoricalCrossentropy", "BinaryCrossentropy"],
                 ["Outputs sum to", "exactly 1", "anything from 0 to N"],
                 ["Outputs are", "coupled — one rises, others fall", "independent — each on its own"]])
        + key("""<p>Multi-label is <b>N separate binary classifiers that happen to share hidden layers</b>.
That sharing is the whole benefit: the features useful for spotting a car are also useful for spotting a
bus, so they get learned once.</p>""")

        + h2("💻", "In code")
        + code("""
# multi-label: 3 independent yes/no questions
model = Sequential([
    Dense(units=25, activation='relu'),
    Dense(units=15, activation='relu'),
    Dense(units=3,  activation='sigmoid'),   # 3 sigmoids, NOT softmax
])
model.compile(loss=BinaryCrossentropy())     # binary loss, applied to all 3

# Y has shape (m, 3): each row is something like [1, 0, 1]
""")

        + h2("🧮", "The same three scores, two different questions")
        + """<p>Take one output layer with three units and scores <var>z</var> = [2.2, −2.2, 1.4].
What you do to them next decides what the network is claiming:</p>"""
        + table(["", "unit 1 (car?)", "unit 2 (bus?)", "unit 3 (pedestrian?)", "sum"],
                [["<b>sigmoid</b> — multi-label", "0.900", "0.100", "0.802", "<b>1.802</b>"],
                 ["<b>softmax</b> — multi-class", "0.684", "0.008", "0.307", "<b>1.000</b>"]])
        + """<p>The sigmoid row says: <em>almost certainly a car, almost certainly also a pedestrian,
probably no bus.</em> Three independent yes/no answers, and there is no reason for them to add to
anything in particular — a street can contain all three at once.</p>
<p>The softmax row says: <em>if I must pick exactly one, it is the car.</em> The three now compete
for a fixed budget of 1.0.</p>"""
        + explain("""<p>Unit 2’s score never changed, yet it fell from 0.100 to 0.008 — an eightfold
drop. <b>Where did that probability go?</b></p>""",
                  """<p>To its rivals. Under sigmoid each unit is scored on its own merits, so unit 2
is judged solely on <var>z</var> = −2.2 and gets 0.100 regardless of what the others scored. Under
softmax the denominator is the sum over <em>all three</em>, so unit 2 is judged on how it compares —
and next to a 2.2 and a 1.4 it looks far worse than it did alone. Nothing about the bus evidence
changed; the question changed from “is there a bus?” to “is the bus the best answer?”.</p>""")

        + h2("🔤", "The words, decoded")
        + decode([
            ("multi-label", "“several labels at once”", "Each example can carry any number of tags. Independent sigmoids, one per tag."),
            ("multi-class", "“one of N”", "Exactly one answer out of several. Softmax, and the probabilities sum to 1."),
            ("independent outputs", "“independent”", "Each unit answers its own yes/no question and ignores the others. Nothing forces the outputs to add to anything."),
            ("threshold", "“the cut-off”", "The number each sigmoid output is compared against, usually 0.5, and one per label."),
        ])
        + h2("🕳", "Traps")
        + trap("""<p><b>Using softmax for multi-label.</b> It forces the probabilities to compete. A photo
containing both a car and a bus can then never score high on both — the model is structurally prevented
from being right.</p>""")
        + trap("""<p><b>Thresholding all labels at 0.5.</b> Rare labels usually need a lower threshold.
Week 3’s precision/recall lesson is how you choose one per label.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("Tagging a news article with any of 20 topics. Which setup?",
             "<p><b>Multi-label</b>: 20 sigmoid units and BinaryCrossentropy. An article can be about both "
             "politics and economics.</p>"),
            ("A model outputs [0.9, 0.8, 0.85]. Multi-class or multi-label?",
             "<p><b>Multi-label</b> — they sum to 2.55, which softmax could never produce.</p>"),
            ("Why not just train three separate networks?",
             "<p>You can, and sometimes should. But one shared network learns the common visual features "
             "once instead of three times: less data needed, less compute, usually better results.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("docs", "https://scikit-learn.org/stable/modules/multiclass.html#multilabel-classification",
             "scikit-learn — multilabel classification",
             "Including how to score it, which is subtler than accuracy."),
            ("paper", "https://arxiv.org/abs/2011.11197",
             "Liu et al. (2020) — The Emerging Trends of Multi-Label Learning",
             "A survey. If you end up doing this for real, the evaluation-metrics section is the useful part."),
        ])
    )))

# ============================================================ 11
L.append(dict(
    slug="11-advanced-optimization", title="Advanced optimization (Adam)", mins=18, tag="core",
    lede="Gradient descent with one fixed step size is leaving performance on the table. Adam gives every "
         "parameter its own learning rate and adjusts it as it goes.",
    body=(
        pretest("""<p>Gradient descent uses one α for every parameter. <b>Guess why that is a compromise</b> when some parameters need big steps and others need tiny ones.</p>""",
        """<p>Watch for what Adam keeps track of per parameter, and for why it is the default in practice.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Imagine walking down a valley in fog, taking steps of exactly the same size every time.</p>
<ul><li>If your steps are too small, you’ll be walking until next Tuesday.</li>
<li>If they’re too big, you’ll stride straight over the bottom and up the other side, back and forth
forever.</li></ul>
<p>A sensible walker does something obvious: <b>if I keep going the same direction, take bigger steps.
If I keep flip-flopping, take smaller ones.</b></p>
<p>That’s Adam. And it does it separately for every single parameter — long strides along the flat
direction, tiny careful ones across the steep one.</p>""")

                + lenses(
            """<p>Walking down an unfamiliar staircase in the dark. On the long even flights you lengthen your
stride; on the bit where the steps are shallow and irregular you shorten right up.</p>
<p>You do not consciously compute anything — you adjust your step by how the last few steps went. Adam
does exactly this, per parameter, and its whole advantage is that it does not have to use one stride
length for the whole staircase.</p>""",
            """<p>If you have used a PID controller, the two terms will look familiar: Adam keeps a running average
of the gradient (momentum, like the integral term) and of its squared magnitude (the scale it divides
by).</p>
<p>The second is the interesting one. Dividing by the recent magnitude makes each parameter’s step
roughly dimensionless — which is why one learning rate can suit parameters whose gradients differ by
orders of magnitude.</p>""",
            """<p>A ball rolling down a long narrow valley, versus one on a marble.</p>
<p>Plain gradient descent bounces wall to wall across the narrow direction, barely progressing along
the floor. Adam is what happens when the ball learns that the side-to-side direction is not worth
much travel and the along-the-valley direction is.</p>""",
            """<p>Measured on this site’s ill-conditioned test problem: with the best hand-tuned single learning
rate, gradient descent reaches a cost of <b>0.018</b>. Adam reaches <b>8 × 10⁻⁸</b> — eight orders of
magnitude lower, starting from a rate ten times larger.</p>
<p>The honest caveat: on a well-scaled problem with a well-chosen α, plain gradient descent can match
it. Adam’s real value is that it is forgiving, which matters far more in practice than the best
case.</p>""",
            """So the two running averages below are all it keeps — and one extra argument is all it costs you.""")
        + h2("🎬", "Watch it move")
        + demo("adam", "Same valley, two walkers",
               "red = plain gradient descent, green = Adam. Try raising α and watch red start bouncing")
        + """<p>The valley is deliberately <b>elongated</b>: steep across, gentle along. Plain gradient
descent has to pick one α for both directions — small enough not to bounce across the valley, which makes
it crawl along it. Adam maintains a separate step size per direction and gets both right.</p>"""

        + h2("🔢", "The maths, decoded")
        + """<p>You are not asked to implement Adam, but the shape of it is easy and worth seeing.</p>"""
        + eqp([
            ('<var>m</var> <span class="op">←</span> <var>β</var><sub>1</sub><var>m</var> + (1−<var>β</var><sub>1</sub>)<var>g</var> &nbsp;&nbsp;&nbsp; <var>v</var> <span class="op">←</span> <var>β</var><sub>2</sub><var>v</var> + (1−<var>β</var><sub>2</sub>)<var>g</var><sup>2</sup>',
             "adam-moments", "recent direction and size"),
        ], "two running averages, kept per parameter — hover or click it", small=True)
        + eqp([
            '<var>w</var> <span class="op">←</span> <var>w</var> <span class="op">−</span> ',
            ('<span class="frac"><span><var class="hl-a">α</var> <var>m̂</var></span><span>√<span class="sqrt"><var>v̂</var></span> + <var>ε</var></span></span>',
             "adam-moments", "step shrinks where gradients are erratic"),
        ], "the update — divide by how bumpy this parameter has been — hover or click it")
        + decode([
            ("<var>g</var>", "“the gradient”", "∂J/∂w for this one parameter, right now."),
            ("<var>m</var>", "“momentum”", "A running average of recent gradients. If they keep pointing the same way, m grows — bigger steps."),
            ("<var>v</var>", "“the second moment”", "A running average of <b>squared</b> gradients: how bumpy this parameter has been lately."),
            ("√<var>v</var> in the denominator", "“divide by the bumpiness”", "Consistently large gradients → smaller steps. Consistently tiny gradients → bigger steps."),
            ("<var>β</var><sub>1</sub>, <var>β</var><sub>2</sub>", "“the decay rates”", "0.9 and 0.999 by default. How much history each average keeps. Almost never worth changing."),
            ("<var>ε</var>", "“epsilon”", "About 10⁻⁸. Only there to stop division by zero."),
        ])
        + note("""<p><b>Adam = ADAptive Moment estimation.</b> The two “moments” are the mean (m) and the
uncentred variance (v) of the gradient. It is not named after a person.</p>""", "Where the name comes from")

        + h2("💻", "In code — it is one argument")
        + code("""
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
    loss=SparseCategoricalCrossentropy(from_logits=True),
)
""")
        + """<p><code>1e-3</code> is the default and a genuinely good starting point. Adam is far less
sensitive to α than plain gradient descent, but it is not immune: if training is unstable, try 1e-4; if it
is painfully slow, try 1e-2.</p>"""

        + h2("🧮", "Where a single learning rate fails")
        + """<p>The clearest case is a cost bowl that is far steeper in one direction than another —
which is what unscaled features produce. Take
<var>J</var> = <var>w</var><sub>1</sub>² + 100<var>w</var><sub>2</sub>², starting at (1, 1). The
second direction is 100 times steeper. Plain gradient descent must pick <em>one</em> α for both:</p>"""
        + table(["Optimizer", "α", "after 200 steps", "final J"],
                [["gradient descent", "0.011", "w₂ blows up to 6.9 × 10¹⁵", "<b>diverges</b>"],
                 ["gradient descent", "0.010", "w₂ oscillates, stuck at 1.0", "100"],
                 ["gradient descent", "0.005 (safe)", "w₁ still at 0.134 — barely moved", "0.018"],
                 ["<b>Adam</b>", "0.05", "both at 0.0000", "<b>0.00000008</b>"]])
        + """<p>Read the middle two rows together, because that is the trap. Any α above 0.01 makes
the steep direction diverge, so α must be chosen small enough for <em>it</em> — and that same small
α then starves the shallow direction, which crawls. One number cannot serve both.</p>
<p>Adam keeps a running estimate of each parameter’s own gradient scale and divides by it, so every
parameter effectively gets its own step size: large where the surface is flat, small where it is
steep. It reached a cost eight orders of magnitude lower than the best hand-tuned single rate, with
a starting α ten times larger.</p>"""
        + note("""<p>This is also why Adam is not magic. On a well-scaled problem with a well-chosen
α, plain gradient descent can beat it. Adam’s value is that it is <em>forgiving</em> — it removes
most of the tuning, which matters far more in practice than the best case does.</p>""")
        + explain("""<p>Adam is described as “an adaptive learning rate”, yet you still pass it an α.
<b>What is that α doing, if the rate adapts?</b></p>""",
                  """<p>It sets the scale, not the direction-by-direction size. Adam divides each
gradient by its own recent magnitude, which makes every parameter’s raw step roughly ±1 — dimensionless.
α then multiplies that normalised step, so it fixes how far “one step” goes overall while Adam keeps
deciding how to split it between parameters. That is why Adam tolerates an α ten times larger here:
α is no longer being forced to absorb the 100× difference in curvature.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Thinking Adam removes the need to tune α.</b> It reduces it a lot. It does not
eliminate it. α still sets the overall scale of every step.</p>""")
        + trap("""<p><b>Assuming Adam is always best.</b> For some problems — famously large image
classifiers — well-tuned SGD with momentum generalises slightly better. Adam is the best <em>default</em>,
not the best in every case.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("A parameter's gradient has been +0.5 for twenty steps. What does Adam do?",
             "<p>Momentum m grows towards 0.5 and the direction is consistent, so Adam <b>increases</b> the "
             "effective step — it strides confidently downhill.</p>"),
            ("Another parameter's gradient flips +2, −2, +2, −2. What does Adam do?",
             "<p>m averages towards ~0 while v stays large, so the step shrinks. It stops thrashing.</p>"),
            ("Why does Adam need one α per parameter rather than one global α?",
             "<p>Because different parameters live on wildly different scales — a weight on a pixel and a "
             "weight on a bias term have completely different sensible step sizes.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("paper", "https://arxiv.org/abs/1412.6980",
             "Kingma & Ba (2014) — Adam: A Method for Stochastic Optimization",
             "One of the most-cited papers in ML. Algorithm 1 on page 2 is the whole method in eight lines."),
            ("paper", "https://distill.pub/2017/momentum/",
             "Distill — Why Momentum Really Works",
             "Interactive. Drag the parameters and watch the optimiser path change. Outstanding."),
            ("paper", "https://arxiv.org/abs/1711.05101",
             "Loshchilov & Hutter (2017) — Decoupled Weight Decay Regularization (AdamW)",
             "The fix that made Adam competitive again on large models. AdamW is now the default in most modern training code."),
            ("docs", "https://www.tensorflow.org/api_docs/python/tf/keras/optimizers/Adam",
             "tf.keras.optimizers.Adam",
             "The arguments, with the defaults straight from the paper."),
        ])
    )))

# ============================================================ 12
L.append(dict(
    slug="12-additional-layer-types", title="Additional layer types (convolutional)", mins=13, tag="intuition",
    lede="Dense layers look at everything. Convolutional layers look at a small window — and that one "
         "restriction buys speed, less data, and less overfitting.",
    body=(
        pretest("""<p>A Dense layer connects every input to every unit. For a 1000×1000 image that is a million inputs per unit. <b>Guess what a cheaper layer might do instead.</b></p>""",
        """<p>Watch for the idea of a unit that only looks at part of the input, and why that is both faster and often better.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>A dense neuron reads the whole picture at once — all million pixels. That’s like reading
an entire book to answer “is there a comma on page 3?”</p>
<p>A convolutional neuron only reads a small <b>window</b> — say 5 pixels — and there are lots of them, each
looking at a different window, all using the <b>same</b> set of weights.</p>
<p>Two big wins. First, far fewer weights to learn. Second, a detector that learned to spot an edge in the
top-left automatically spots edges everywhere else too, because it is literally the same detector, moved
along.</p>""")

        + h2("🎬", "Watch it move")
        + demo("conv", "A sliding window over an EKG trace",
               "each unit sees only five readings — and every unit shares the same weights")

        + h2("🔢", "The maths, decoded")
        + decode([
            ("convolution", "“slide and multiply”", "Take a small weight vector (the kernel), slide it along the input, and compute a dot product at each position."),
            ("kernel / filter", "“the little detector”", "The shared weight vector. A 5-wide kernel has 5 weights — reused at every position."),
            ("weight sharing", "“one detector, many places”", "The reason a conv layer has so few parameters. This is the key idea."),
            ("receptive field", "“what this unit can see”", "The window of input a unit depends on. It grows as you stack layers — that is Lesson 3 of Week 1 made precise."),
        ])
        + table(["", "Dense layer", "Convolutional layer"],
                [["Each unit sees", "every input", "a small window"],
                 ["Weights per unit", "one per input (e.g. 400)", "one per window position (e.g. 5)"],
                 ["Weights shared?", "no — every unit has its own", "yes — all units share one kernel"],
                 ["Good for", "tabular data, small inputs", "images, audio, time series"],
                 ["Needs", "lots of data", "less data (fewer parameters to pin down)"]])
        + key("""<p>Fewer parameters means faster training, less memory, and less capacity to memorise the
training set. The restriction <em>is</em> the benefit — it encodes the true fact that in an image, nearby
pixels matter to each other and position shouldn’t change what a thing is.</p>""")

        + h2("🔬", "Layer types you will meet later")
        + grid3(
            card("<h3>Convolutional</h3><p>Windows + weight sharing. Images, audio, anything with spatial "
                 "or temporal structure.</p>"),
            card("<h3>Recurrent</h3><p>Keeps a memory of what it saw earlier. Was standard for sequences "
                 "before transformers.</p>"),
            card("<h3>Attention / transformer</h3><p>Every position decides which other positions to look "
                 "at. Behind essentially every modern large model.</p>"))
        + """<p>None of these change anything you have learned. Each is still
<var>a</var> = <var>g</var>(weighted sum + bias) — they differ only in <em>which</em> inputs are in the sum
and <em>which</em> weights are shared.</p>"""

        + h2("🧮", "Counting the parameters a convolution saves")
        + """<p>Take the assignment’s 20 × 20 digit — 400 pixels — and give it a first hidden layer
of the two kinds:</p>"""
        + table(["Layer", "What each unit sees", "Parameters"],
                [["<code>Dense(25)</code>", "all 400 pixels", "400 × 25 + 25 = <b>10,025</b>"],
                 ["<code>Conv2D(8, (3,3))</code>", "a 3 × 3 window, slid over the image",
                  "(3 × 3 + 1) × 8 = <b>80</b>"]])
        + """<p>125 times fewer parameters, and the convolutional version usually does <em>better</em>
on images. That combination is why convolution took over computer vision.</p>
<p>The saving comes from <b>weight sharing</b>. A dense unit needs a separate weight for every pixel
position, so it must learn “what an edge looks like” independently at each of the 400 locations. A
convolutional filter has nine weights that are reused at every position — learn the edge once, and it
is detected everywhere. Fewer parameters means less to fit, which means less overfitting and less
data needed.</p>"""
        + explain("""<p>Weight sharing is a hard constraint: it forbids the layer from treating the
top-left corner differently from the centre. <b>Why is losing that freedom an advantage on images
but not on, say, a table of customer records?</b></p>""",
                  """<p>Because on an image the constraint is <em>true</em>. A vertical edge is a
vertical edge wherever it appears, so a detector that works in the corner should work in the centre,
and forcing that saves the model from relearning the same thing 400 times. On a table of customer
records, column 3 is “age” and column 7 is “postcode” — they have nothing in common, adjacency means
nothing, and sliding a window across them would impose a similarity that does not exist. The right
architecture is the one whose built-in assumption matches the data.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Using a dense layer on large images.</b> A 1000×1000 RGB image into a 100-unit dense
layer is 300 million weights in the first layer alone. It will not train, and it will overfit anything it
does manage to learn.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("A 1-D conv layer with kernel width 5 over a 100-long input. How many weights? How many outputs?",
             "<p><b>5 weights</b> (+1 bias) for the kernel, shared. Outputs: 100 − 5 + 1 = <b>96</b> "
             "positions. Compare with a dense layer: 100 × 96 = 9,600 weights.</p>"),
            ("Why does weight sharing help with limited data?",
             "<p>Fewer parameters to estimate, and each one is trained by every window position — so each "
             "weight sees far more evidence.</p>"),
            ("Why is a conv layer a bad choice for a table of customer records?",
             "<p>Because “nearby columns are related” is false for tabular data. Column order is arbitrary, "
             "so a sliding window encodes an assumption that simply is not true.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("docs", "https://cs231n.github.io/convolutional-networks/",
             "CS231n — Convolutional Neural Networks",
             "The best free explanation of conv layers anywhere. Read the “Convolutional Layer” section."),
            ("paper", "http://yann.lecun.com/exdb/publis/pdf/lecun-98.pdf",
             "LeCun et al. (1998) — Gradient-based learning applied to document recognition",
             "LeNet-5. Convolutional networks reading cheques, in production, in the 1990s."),
            ("paper", "https://arxiv.org/abs/1706.03762",
             "Vaswani et al. (2017) — Attention Is All You Need",
             "The transformer. Not needed for this course, but this is the paper the last decade is built on."),
            ("play", "https://poloclub.github.io/cnn-explainer/",
             "CNN Explainer",
             "Interactive, in-browser walkthrough of a real convolutional network, layer by layer."),
        ])
    )))

# ============================================================ 13
L.append(dict(
    slug="13-what-is-a-derivative", title="What is a derivative? (optional)", mins=13, tag="optional",
    lede="Start of the optional back-propagation section. A derivative is one honest question: if I nudge "
         "this up a hair, how much does that change?",
    body=(
        pretest("""<p>Nudge one weight by a tiny amount and the cost changes a little. <b>Guess what the ratio of those two changes is called</b>, and what its sign tells you.</p>""",
        """<p>Watch for how little calculus you actually need: a number, a sign, and a size.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>You’re standing on a hill. You shuffle one tiny step to the east and check: did I go up
or down, and by how much?</p>
<ul><li>Went up a lot → steep uphill east → the derivative is a big positive number.</li>
<li>Went down a little → gentle downhill east → a small negative number.</li>
<li>Didn’t change → flat → zero.</li></ul>
<p>That’s a derivative. It is the answer to “what happens if I nudge?” — nothing more mysterious than
that.</p>""")

        + h2("🔢", "The maths, decoded")
        + eqp([
            ('<span class="frac"><span>∂<var>J</var></span><span>∂<var>w</var></span></span>', "partial-f0", "the slope, at w"),
            ' <span class="op">≈</span> <span class="frac"><span><var>J</var>(<var>w</var> + <var>ε</var>) − <var>J</var>(<var>w</var>)</span><span><var>ε</var></span></span> <span class="op">&nbsp;as&nbsp;</span> <var>ε</var> <span class="op">→</span> 0',
        ], "rise over run, with the run shrunk to almost nothing — hover or click it")
        + decode([
            ("∂", "“partial dee”", "Derivative with respect to <b>one</b> variable while the rest are held still. Curly ∂ = several variables about; straight d = only one."),
            ("<var>ε</var>", "“epsilon”", "A tiny nudge. 0.001, or smaller. The formula becomes exact as it shrinks to zero."),
            ("∂J/∂w", "“how J responds to w”", "The units are “change in cost per unit of weight”. It has a sign: positive means increasing w increases the cost."),
            ("gradient", "“all of them at once”", "The vector of every partial derivative. It points in the steepest-uphill direction — so we step the other way."),
        ])
        + key("""<p>Gradient descent uses <b>two</b> pieces of information from the derivative: the
<b>sign</b> tells it which way is downhill, and the <b>size</b> tells it how far it can safely go.</p>""")

        + h2("🎬", "Watch it move")
        + demo("deriv", "Rise over run, with a shrinkable nudge",
               "shrink ε and watch the measured slope converge on the true derivative")

        + h2("🧮", "The three rules that cover this course")
        + table(["Function", "Derivative", "In words"],
                [["J = w²", "2w", "steeper the further from zero"],
                 ["J = w³", "3w²", "the power comes down and drops by one"],
                 ["J = 3w", "3", "a straight line has the same slope everywhere"],
                 ["J = c (constant)", "0", "flat: nudging w changes nothing"]])
        + note("""<p>You will not be asked to differentiate anything by hand in this course.
<b>SymPy</b> can do it symbolically if you are curious — the optional lab uses it — and TensorFlow does it
automatically for the actual network. The point of this lesson is to know what the machine is computing.</p>""",
               "You don’t have to do this by hand")

        + h2("🧮", "The lab’s own experiment")
        + """<p>The optional derivatives lab does not define a derivative — it measures one. Take
<var>J</var> = <var>w</var>², sit at <var>w</var> = 3, nudge, and divide:</p>"""
        + code("""
J         = 3**2                     # 9
J_epsilon = (3 + 0.001)**2           # 9.006001
k = (J_epsilon - J) / 0.001          # 6.001
""")
        + table(["nudge ε", "(J(3+ε) − J(3)) / ε", "true derivative 2w"],
                [["0.001", "6.001000", "6"],
                 ["0.000001", "6.000001", "6"]])
        + """<p>So the derivative of <var>w</var>² at <var>w</var> = 3 is <b>6</b>, and the sentence
it stands for is: <em>if I increase w by a tiny amount, J increases by about six times as much.</em>
That is the only fact gradient descent ever uses — it tells you which way is uphill, and by how much
per unit of movement.</p>"""
        + explain("""<p>Smaller ε gives a better answer, and ε = 0 gives the exact one.
<b>Why can you not simply use a very tiny ε in code?</b></p>""",
                  """<p>Because the numerator is a subtraction of two nearly equal numbers, and floats
have finite precision. At ε = 10⁻¹⁵, J(3+ε) and J(3) agree in almost every stored digit, so the
difference is built from the few noisy digits left — and dividing that noise by an equally tiny ε
amplifies it. The error falls as ε shrinks, then rises again once cancellation dominates. This is
exactly why real training uses backpropagation, which computes derivatives <em>symbolically</em>
rather than by nudging.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Taking ε too small in code.</b> With floating point, ε = 10⁻¹⁵ makes
<code>J(w+ε) − J(w)</code> round to zero and the estimate becomes garbage. There is a sweet spot around
10⁻⁴ to 10⁻⁷ — the same rounding problem as Lesson 9, from the other direction.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("J(w) = w². At w = 3, what is the derivative, and what does gradient descent do?",
             "<p>2w = <b>6</b>. Positive, so increasing w increases cost — gradient descent <em>decreases</em> "
             "w, moving towards 0.</p>"),
            ("At w = 0 the derivative of w² is 0. What does gradient descent do?",
             "<p><b>Nothing.</b> It has reached a flat point. Here that is the true minimum; in a bigger "
             "network it might be a saddle point or a local minimum.</p>"),
            ("Why ∂ instead of d?",
             "<p>Because J depends on thousands of parameters. ∂J/∂w means “vary this one, freeze all the "
             "others”.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("video", "https://www.3blue1brown.com/topics/calculus",
             "3Blue1Brown — Essence of Calculus",
             "Chapters 1–3 cover everything you need. If calculus never clicked at school, this is the fix."),
            ("docs", "https://www.khanacademy.org/math/differential-calculus",
             "Khan Academy — Differential Calculus",
             "Free, with practice problems. Use it if you want the mechanical fluency."),
            ("docs", "https://docs.sympy.org/latest/tutorials/intro-tutorial/calculus.html",
             "SymPy — symbolic differentiation",
             "<code>diff(w**2, w)</code> → <code>2*w</code>. The optional lab uses this."),
        ])
    )))

# ============================================================ 14
L.append(dict(
    slug="14-computation-graph", title="Computation graph (optional)", mins=11, tag="optional",
    lede="How a machine differentiates something nobody wrote a formula for: break the calculation into "
         "tiny steps, then walk backwards multiplying local slopes.",
    body=(
        pretest("""<p>A network has a million weights. <b>Guess how many times you would have to run it forwards to measure every derivative by nudging</b> — then guess whether that is affordable.</p>""",
        """<p>Two million forward passes. Watch for how backprop gets all of them in roughly one backward pass instead.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Suppose a chain of gears: turn gear A and it turns B, which turns C, which turns D.</p>
<p>You want to know: if I turn A by one notch, how far does D move? You don’t need to understand the whole
machine. You just need each pair: A→B is ×2, B→C is ×3, C→D is ×0.5. Multiply them: 2 × 3 × 0.5 = <b>3</b>.
Turn A one notch, D moves three.</p>
<p>That’s the chain rule, and that’s backpropagation. Every node only needs to know its own little
multiplier.</p>""")

        + h2("🔢", "The maths, decoded")
        + eqp([
            ('<span class="frac"><span>∂<var>J</var></span><span>∂<var>w</var></span></span>', "partial-f0", "the slope, at w"),
            ' <span class="op">=</span> <span class="frac"><span>∂<var>J</var></span><span>∂<var>d</var></span></span> <span class="op">·</span> <span class="frac"><span>∂<var>d</var></span><span>∂<var>a</var></span></span> <span class="op">·</span> <span class="frac"><span>∂<var>a</var></span><span>∂<var>c</var></span></span> <span class="op">·</span> <span class="frac"><span>∂<var>c</var></span><span>∂<var>w</var></span></span>',
        ], "the chain rule — multiply the local slopes along the path — hover or click it")
        + decode([
            ("computation graph", "“the wiring diagram”", "Every intermediate value is a node; every arrow is one elementary operation (× or + or exp)."),
            ("forward pass", "“left to right”", "Compute every node’s value and remember it. You need those values on the way back."),
            ("backward pass", "“right to left”", "Start with ∂J/∂J = 1 and multiply by each node’s local derivative as you go."),
            ("local derivative", "“this node’s own slope”", "How much this node’s output changes when its input does. For c = w·x it is simply x."),
        ])

        + h2("🎬", "Watch it move")
        + demo("compgraph", "Forward, then backward",
               "blue = values flowing right, orange = derivatives flowing left")

        + h2("🧮", "The worked example, on paper")
        + """<p>Take w = 3, x = −2, b = 1, y = 2. The graph is
c = w·x → a = c + b → d = a − y → J = ½d².</p>"""
        + table(["Forward", "Value", "Backward", "Value"],
                [["c = w·x = 3(−2)", "−6", "∂J/∂d = d", "−7"],
                 ["a = c + b = −6+1", "−5", "∂J/∂a = ∂J/∂d · 1", "−7"],
                 ["d = a − y = −5−2", "−7", "∂J/∂c = ∂J/∂a · 1", "−7"],
                 ["J = ½d² = ½(49)", "24.5", "<b>∂J/∂w = ∂J/∂c · x</b>", "<b>14</b>"]])
        + """<p>Check it the slow way: nudge w from 3 to 3.001 and recompute J. You get 24.514, an increase
of 0.014 for a nudge of 0.001 — a slope of 14. The chain rule and the brute-force nudge agree, as they
must.</p>"""
        + key("""<p>The magic is the <b>reuse</b>. ∂J/∂a is computed once and then used by everything
upstream of a. In a network with a million weights, one backward sweep gets you all million derivatives.
Nudging each weight separately would cost a million forward passes.</p>""")

        + explain("""<p>Backprop gets every derivative in roughly one backward pass, where nudging each weight would need two per weight. <b>Why is it so much cheaper?</b></p>""",
            """<p>Because the chain rule lets each node reuse the result already computed downstream of it. Nudging recomputes the whole network from scratch for every single weight; backprop computes each shared piece once and passes it back.</p>""")
        + h2("🕳", "Traps")
        + trap("""<p><b>Forgetting you need the forward values.</b> The backward pass uses numbers computed
during the forward pass (like x, to get ∂c/∂w). That is why training uses far more memory than inference —
every intermediate activation has to be kept.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("For c = w·x with x = −2, what is ∂c/∂w?",
             "<p><b>−2</b>, which is x. For a product, the derivative with respect to one factor is the "
             "other factor.</p>"),
            ("Why compute derivatives right-to-left instead of left-to-right?",
             "<p>Because there is one output and many parameters. Going backwards from the single J reuses "
             "the shared part of every path. Forward-mode would redo that work once per parameter.</p>"),
            ("What is ∂J/∂J?",
             "<p><b>1</b>. It is where every backward pass starts.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("paper", "https://www.nature.com/articles/323533a0",
             "Rumelhart, Hinton & Williams (1986) — Learning representations by back-propagating errors",
             "The paper. Two pages, and it changed everything."),
            ("video", "https://www.youtube.com/watch?v=VMj-3S1tku0",
             "Karpathy — The spelled-out intro to neural networks and backpropagation",
             "Builds an autodiff engine from scratch in Python, live. Long, and the single best resource on this topic."),
            ("docs", "https://cs231n.github.io/optimization-2/",
             "CS231n — Backpropagation, intuitions",
             "Local gradients, gates, and the “gradient flow” mental model."),
        ])
    )))

# ============================================================ 15
L.append(dict(
    slug="15-larger-network-example", title="Larger neural network example (optional)", mins=12, tag="optional",
    lede="Scaling the computation graph up to a real network, and the cost argument that makes training "
         "possible at all.",
    body=(
        pretest("""<p>You have seen the chain rule on a tiny graph. <b>Guess what changes when the network is large</b> — the idea, or only the bookkeeping?</p>""",
        """<p>Watch for the answer being bookkeeping. The rule is identical; there is just more of it.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Same gear-chain trick, just a much bigger machine — thousands of gears, in rows.</p>
<p>Here’s the amazing part. You might think that to find out how each of a million gears affects the final
one, you’d have to test each gear separately: a million experiments. You don’t. <b>One</b> careful walk
backwards through the machine tells you about every gear at once.</p>""")

        + h2("🎬", "Watch it move")
        + demo("bignet", "Forward, then backward, through a whole network",
               "blue sweeps right computing activations, orange sweeps left computing derivatives")

        + h2("🔢", "The cost argument")
        + table(["Method", "Cost for N parameters", "For N = 1,000,000"],
                [["Nudge each parameter and re-run", "N forward passes", "1,000,000 passes — hopeless"],
                 ["Forward-mode autodiff", "N forward sweeps", "still 1,000,000 — no better"],
                 ["<b>Backpropagation</b>", "<b>1 forward + 1 backward</b>", "<b>≈ 2 passes</b>"]])
        + """<p>That ratio is why deep learning exists. Backprop is not merely a nice trick — without it,
training anything with more than a few hundred parameters would be computationally out of reach.</p>"""
        + key("""<p>Backprop costs about <b>two</b> forward passes, regardless of how many parameters you
have. Reverse-mode automatic differentiation is efficient exactly when you have many inputs and one output —
which is precisely the shape of a loss function.</p>""")

        + h2("🔬", "What TensorFlow is doing while you sleep")
        + """<p>Every operation you write inside a <code>tf.GradientTape</code> block is recorded on a tape:
the operation, its inputs, and its output. When you ask for gradients, TensorFlow replays that tape
backwards, applying each operation’s known local derivative rule.</p>"""
        + code("""
with tf.GradientTape() as tape:
    logits = model(X, training=True)
    loss = loss_fn(Y, logits)

grads = tape.gradient(loss, model.trainable_variables)   # one backward sweep
optimizer.apply_gradients(zip(grads, model.trainable_variables))
""")
        + """<p>That is <code>model.fit()</code>, unrolled. Nothing else is hiding in there. Worth reading
twice — once you can see the tape, the framework stops feeling like magic.</p>"""

        + h2("🧮", "How much arithmetic is that, actually")
        + """<p>The Week 2 network is 400 → 25 → 15 → 10. One forward pass costs one multiply-add per
weight:</p>"""
        + table(["Layer", "multiply-adds"],
                [["400 → 25", "10,000"],
                 ["25 → 15", "375"],
                 ["15 → 10", "150"],
                 ["<b>one example</b>", "<b>10,525</b>"]])
        + """<p>Now the training run: 5,000 examples, 40 epochs.</p>"""
        + eq("""10,525 <span class="op">×</span> 5,000 <span class="op">×</span> 40
<span class="op">=</span> <b>2.1 billion</b>""", "multiply-adds, just for the forward passes")
        + """<p>Backpropagation adds roughly two to three times that again, so the real figure is
somewhere near six billion operations — for a network small enough to describe in four lines, on a
data set that fits in memory. It finishes in under a minute, which is a fact about hardware, not
about the problem being small.</p>
<p>This is the arithmetic that made vectorisation non-negotiable, and it is the reason a matrix
multiply that runs 93 times faster is not a micro-optimisation.</p>"""
        + explain("""<p>Backpropagation computes a derivative for all 10,575 parameters, yet costs
about the same as a <em>few</em> forward passes — not 10,575 of them. <b>Why?</b></p>""",
                  """<p>Because it reuses shared work. Nudging one parameter at a time and re-running
the network would indeed cost one forward pass each, and almost every one of those passes would
recompute the same intermediate quantities. Backprop instead sweeps once from the output backwards,
and at each step the quantity it already carries is exactly what every parameter in that layer
needs. The total is proportional to the number of <em>connections traversed once</em>, which is one
network’s worth — not to the number of parameters differentiated.</p>""")

        + h2("🔤", "The words, decoded")
        + decode([
            ("multiply-add", "“a MAC”", "One multiplication plus one addition — the unit that hardware and cost estimates are counted in."),
            ("FLOPs", "“flops”", "Floating-point operations. How compute budgets are quoted; one multiply-add is two FLOPs."),
            ("epoch", "“epoch”", "One full pass over the whole training set."),
            ("throughput", "“throughput”", "Examples processed per second. What vectorisation and GPUs actually buy you."),
        ])
        + h2("🕳", "Traps")
        + trap("""<p><b>Memory, not speed, is usually the wall.</b> Every intermediate activation is kept for
the backward pass, so memory grows with depth × batch size. “Out of memory” during training almost always
means: reduce the batch size.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("A network has 10 million parameters. Roughly how expensive is one gradient computation?",
             "<p>About <b>two forward passes</b>. The parameter count affects the cost of a single pass, "
             "but not the <em>number</em> of passes.</p>"),
            ("Why does training need much more memory than inference?",
             "<p>Because the backward pass needs the forward pass’s intermediate values, so they must all "
             "be stored. Inference can throw each layer away as soon as the next is computed.</p>"),
            ("What is on the “tape” in tf.GradientTape?",
             "<p>The sequence of operations performed, with their inputs, so each can be replayed backwards "
             "using its known derivative rule.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("docs", "https://www.tensorflow.org/guide/autodiff",
             "TensorFlow — Introduction to gradients and automatic differentiation",
             "GradientTape explained properly, with the gotchas."),
            ("paper", "https://arxiv.org/abs/1502.05767",
             "Baydin et al. (2015) — Automatic Differentiation in Machine Learning: a Survey",
             "Forward mode vs reverse mode, and exactly when each one wins. The clearest treatment there is."),
            ("video", "https://www.youtube.com/watch?v=VMj-3S1tku0",
             "Karpathy — micrograd, built live",
             "150 lines of Python that implement everything in this lesson. The best way to truly own it."),
        ])
    )))

WEEK = dict(
    course="C2", week=2, title="Neural Network Training",
    time="~7–9 h with labs",
    goal="Train networks properly: the loss function, ReLU vs sigmoid, softmax for multiclass, "
         "numerically stable implementations, Adam, and how backprop actually works.",
    lessons=L,
)
