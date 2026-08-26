# -*- coding: utf-8 -*-
"""C2 · Week 2 — Training, activations, softmax, optimisation."""
from kit import (kid, key, warn, trap, note, card, eq, eqp, decode, table, demo,
                 quiz, links, code, h2, grid2, grid3)

L = []

# ============================================================ 1
L.append(dict(
    slug="01-tensorflow-training", title="TensorFlow implementation of training", mins=9, tag="code",
    lede="Three lines of code, three ideas you already know from Course 1. This lesson is the map; the "
         "next one opens the box.",
    body=(
        h2("🎈", "The idea, in plain words")
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
    slug="02-training-details", title="Training details", mins=12, tag="core",
    lede="Opening the box: what the loss function actually is, why it is shaped the way it is, and what "
         "gradient descent does with it.",
    body=(
        h2("🎈", "The idea, in plain words")
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
        ], "binary cross-entropy — the loss for ONE example — click it")
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
        ], "repeat for every weight and every bias, over and over — click a part")
        + decode([
            (":=", "“becomes”", "Assignment, not equality. The new w is computed from the old one."),
            ("<var class='hl-a'>α</var>", "“alpha”, the learning rate", "Step size. Too small → glacial. Too big → it overshoots and diverges."),
            ("∂J/∂w", "“the partial derivative”", "“If I nudge this one weight up a hair, how much does the total cost go up?” Backprop computes all of them at once."),
        ])
        + note("""<p>In Course 1 you differentiated by hand. In a network with 20,000 weights that is not
possible, so TensorFlow builds a <b>computation graph</b> and applies the chain rule automatically. That
is what lessons 13–15 of this week explain, and why they are optional-but-worth-it.</p>""",
               "Where the derivatives come from")

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
    slug="03-sigmoid-alternatives", title="Alternatives to the sigmoid activation", mins=10, tag="core",
    lede="ReLU, and why one strange-looking bent line replaced the elegant S-curve almost everywhere.",
    body=(
        h2("🎈", "The idea, in plain words")
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
        ], "ReLU — rectified linear unit — click it")
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
        h2("🎈", "The idea, in plain words")
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
    slug="05-why-activations", title="Why do we need activation functions?", mins=10, tag="maths",
    lede="The three-line proof that a network with no activation function is just a very expensive straight "
         "line — and the picture of what non-linearity buys you.",
    body=(
        h2("🎈", "The idea, in plain words")
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
        ], "layer 1, with a linear activation — click it", small=True)
        + eqp([
            '<var>a</var><sup>[2]</sup> = ',
            ('<var>W</var><sup>[2]</sup><var>a</var><sup>[1]</sup>', "matmul-f0", "whole layer, one multiply"),
            ' + <var>b</var><sup>[2]</sup> = <var>W</var><sup>[2]</sup>(',
            ('<var>W</var><sup>[1]</sup><var>x</var>', "matmul-f0", "whole layer, one multiply"),
            ' + <var>b</var><sup>[1]</sup>) + <var>b</var><sup>[2]</sup>',
        ], "substitute layer 1 into layer 2 — click a part", small=True)
        + eqp([
            '<var>a</var><sup>[2]</sup> = ',
            ('<span class="hl-a">(<var>W</var><sup>[2]</sup><var>W</var><sup>[1]</sup>)</span>', "matmul-f0", "two matrices collapse into one"),
            '<var>x</var> + <span class="hl-a">(<var>W</var><sup>[2]</sup><var>b</var><sup>[1]</sup> + <var>b</var><sup>[2]</sup>)</span> = <var>W</var>′<var>x</var> + <var>b</var>′',
        ], "multiply out — and it collapses to a single layer — click it")
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
        h2("🎈", "The idea, in plain words")
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
    slug="07-softmax", title="Softmax", mins=12, tag="maths",
    lede="The generalisation of sigmoid to N classes. Two moves — exponentiate, then divide by the total — "
         "and every property you need follows from them.",
    body=(
        h2("🎈", "The idea, in plain words")
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
        ], "step 1 — one score per class, exactly as before — click a part")
        + eqp([
            '<var>a</var><sub><var>j</var></sub> <span class="op">=</span> ',
            ('<span class="frac"><span><var>e</var><sup><var>z</var><sub><var>j</var></sub></sup></span>'
             '<span><var>e</var><sup><var>z</var><sub>1</sub></sup> + <var>e</var><sup><var>z</var><sub>2</sub></sup> + … + <var>e</var><sup><var>z</var><sub><var>N</var></sub></sup></span></span>',
             "softmax-native", "turns scores into probabilities"),
            ' <span class="op">=</span> <var>P</var>(<var>y</var> = <var>j</var> | <var>x</var>)',
        ], "step 2 — softmax — click it")
        + decode([
            ("<var>e</var><sup><var>z</var></sup>", "“e to the z”", "Always positive, and it grows fast. It turns differences in z into ratios in a."),
            ("the denominator", "“the total”", "The same sum for every class — that is the shared budget everyone divides into."),
            ("<var>a</var><sub><var>j</var></sub>", "“a sub j”", "The probability of class j. Between 0 and 1, and Σa<sub>j</sub> = 1 by construction."),
            ("soft-max", "“a gentle argmax”", "If one z is far above the rest, its a → 1 and the others → 0. If they are close, the probabilities are close."),
        ])
        + key("""<p>Softmax is the <b>only</b> activation in this course where each output depends on all
the other outputs. Every other activation squashes its own z alone. That coupling is what makes the
probabilities sum to 1.</p>""")

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

        + h2("🔢", "And the loss that goes with it")
        + eqp([
            ('<var>L</var> <span class="op">=</span> <span class="op">−</span>log(<var>a</var><sub><var>y</var></sub>)', "logarithm-f0", "huge penalty if the true class's probability is near 0"),
        ], "sparse categorical cross-entropy — only the TRUE class’s probability is scored — click it")
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
    slug="08-softmax-output-layer", title="Neural network with Softmax output", mins=9, tag="code",
    lede="Bolting softmax onto the end of a network: ten output units, one shared normalisation, and the "
         "code that trains it.",
    body=(
        h2("🎈", "The idea, in plain words")
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
        ], "the Week 2 assignment network — click a part", small=True)
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
    slug="09-improved-softmax", title="Improved implementation of softmax", mins=11, tag="core",
    lede="Why `from_logits=True` exists. A short lesson about floating-point arithmetic that will save you "
         "from a class of bug that is invisible until it isn’t.",
    body=(
        h2("🎈", "The idea, in plain words")
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
        ], "two steps — a gets rounded before log ever sees it — click a part", small=True)
        + """<p>The stable route substitutes one into the other and simplifies, so <var>a</var> is never
built at all:</p>"""
        + eqp([
            ('<var>L</var> = −log<span class="paren">(</span><span class="frac"><span>1</span><span>1 + <var>e</var><sup>−<var>z</var></sup></span></span><span class="paren">)</span> = log(1 + <var>e</var><sup>−<var>z</var></sup>)',
             "logarithm-f0", "same loss, one rounding step instead of two"),
        ], "one step, algebraically identical, numerically far safer — click it")
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
    slug="10-multi-label", title="Classification with multiple outputs (multi-label)", mins=8, tag="core",
    lede="A short but genuinely confusable distinction: several answers can be true at once, so softmax is "
         "the wrong tool.",
    body=(
        h2("🎈", "The idea, in plain words")
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
    slug="11-advanced-optimization", title="Advanced optimization (Adam)", mins=10, tag="core",
    lede="Gradient descent with one fixed step size is leaving performance on the table. Adam gives every "
         "parameter its own learning rate and adjusts it as it goes.",
    body=(
        h2("🎈", "The idea, in plain words")
        + kid("""<p>Imagine walking down a valley in fog, taking steps of exactly the same size every time.</p>
<ul><li>If your steps are too small, you’ll be walking until next Tuesday.</li>
<li>If they’re too big, you’ll stride straight over the bottom and up the other side, back and forth
forever.</li></ul>
<p>A sensible walker does something obvious: <b>if I keep going the same direction, take bigger steps.
If I keep flip-flopping, take smaller ones.</b></p>
<p>That’s Adam. And it does it separately for every single parameter — long strides along the flat
direction, tiny careful ones across the steep one.</p>""")

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
        ], "two running averages, kept per parameter — click it", small=True)
        + eqp([
            '<var>w</var> <span class="op">←</span> <var>w</var> <span class="op">−</span> ',
            ('<span class="frac"><span><var class="hl-a">α</var> <var>m̂</var></span><span>√<span class="sqrt"><var>v̂</var></span> + <var>ε</var></span></span>',
             "adam-moments", "step shrinks where gradients are erratic"),
        ], "the update — divide by how bumpy this parameter has been — click it")
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
    slug="12-additional-layer-types", title="Additional layer types (convolutional)", mins=9, tag="intuition",
    lede="Dense layers look at everything. Convolutional layers look at a small window — and that one "
         "restriction buys speed, less data, and less overfitting.",
    body=(
        h2("🎈", "The idea, in plain words")
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
    slug="13-what-is-a-derivative", title="What is a derivative? (optional)", mins=9, tag="optional",
    lede="Start of the optional back-propagation section. A derivative is one honest question: if I nudge "
         "this up a hair, how much does that change?",
    body=(
        h2("🎈", "The idea, in plain words")
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
        ], "rise over run, with the run shrunk to almost nothing — click it")
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
        h2("🎈", "The idea, in plain words")
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
        ], "the chain rule — multiply the local slopes along the path — click it")
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
    slug="15-larger-network-example", title="Larger neural network example (optional)", mins=8, tag="optional",
    lede="Scaling the computation graph up to a real network, and the cost argument that makes training "
         "possible at all.",
    body=(
        h2("🎈", "The idea, in plain words")
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
