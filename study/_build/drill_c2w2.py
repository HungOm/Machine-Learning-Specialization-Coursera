# -*- coding: utf-8 -*-
"""Quiz drills — C2 W2. One concept per mock-quiz question, four methods each.

Every number below is COMPUTED here at import time and formatted into the text,
never typed. If a value is wrong, it is wrong in the arithmetic, where you can
see it, not in a sentence. TensorFlow is never executed here: its behaviour is
described in prose, and every number comes from NumPy.
"""
import math

import numpy as np
from drillkit import D, M
from masterykit import code


def n(x, d=2):
    """Format a number for prose: d decimals, trailing zeros trimmed."""
    s = ("%." + str(d) + "f") % x
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return "&minus;" + s[1:] if s.startswith("-") else s


def sci(x, d=1):
    """Scientific notation for prose, e.g. 1.5 &times; 10<sup>&minus;5</sup>."""
    if x == 0:
        return "0"
    e = int(math.floor(math.log10(abs(x))))
    m = x / 10 ** e
    exp = ("&minus;%d" % -e) if e < 0 else ("%d" % e)
    return "%s &times; 10<sup>%s</sup>" % (n(m, d), exp)


def sig(z):
    return 1 / (1 + np.exp(-z))


def softmax(z):
    e = np.exp(z - np.max(z))
    return e / e.sum()


def _row(vals, d=3):
    return "[" + ", ".join(n(v, d) for v in vals) + "]"


# ---------------------------------------------------------------- q01 three steps
N_IN1, H1, OUT1 = 3, 4, 1
P1 = (N_IN1 * H1 + H1) + (H1 * OUT1 + OUT1)
M1, BATCH1, EPOCHS1 = 1000, 32, 5
STEPS1 = math.ceil(M1 / BATCH1)
UPD1 = STEPS1 * EPOCHS1
LAST1 = M1 - (STEPS1 - 1) * BATCH1

# ---------------------------------------------------------------- q02 hidden activations
LAYERS2 = 8
DS_BEST2 = sig(0.0) * (1 - sig(0.0))
DS_Z2 = sig(2.0) * (1 - sig(2.0))
PROD_BEST2 = DS_BEST2 ** LAYERS2
PROD_Z2 = DS_Z2 ** LAYERS2
DS_5 = sig(5.0) * (1 - sig(5.0))
# transfer: ReLU hidden layer, linear output, a negative prediction
H2 = np.maximum(0, np.array([1.4, -0.7, 2.0]))
W2o = np.array([-1.5, 0.8, -0.6]); B2o = 0.5
OUT2 = H2 @ W2o + B2o

# ---------------------------------------------------------------- q03 output activations
Z3 = -1.2
SIG3, LIN3, RELU3 = sig(Z3), Z3, max(0.0, Z3)
Z3b = 3.0
SIG3b = sig(Z3b)
PRICE3 = 250.0
BEST_ERR3 = (PRICE3 - 1.0) ** 2

# ---------------------------------------------------------------- q04 numerical stability
Z4 = np.array([2.0, 1.0, 0.0])
SM4 = softmax(Z4)
Z4big = Z4 + 800
with np.errstate(over="ignore", invalid="ignore"):
    NAIVE4 = np.exp(Z4big) / np.exp(Z4big).sum()
SHIFT4 = np.exp(Z4big - Z4big.max()) / np.exp(Z4big - Z4big.max()).sum()
# double softmax: softmax applied to probabilities that already came out of a softmax
Z4d = np.array([3.0, 1.0, -1.0])
P4d = softmax(Z4d)
DOUBLE4 = softmax(P4d)
# binary: confidently wrong in float32
ZB4 = np.float32(-120.0)
with np.errstate(over="ignore", divide="ignore"):
    SIGB4 = np.float32(1) / (np.float32(1) + np.exp(-ZB4))
    NAIVEB4 = -np.log(SIGB4)
STABLEB4 = np.logaddexp(0.0, -float(ZB4))

# ---------------------------------------------------------------- q05 softmax outputs
Z5 = np.array([1.0, 2.5, 0.2, -1.0])
S5 = softmax(Z5)
Z5up = Z5.copy(); Z5up[1] += 1.0
S5up = softmax(Z5up)
S5x2 = softmax(2 * Z5)
S5p10 = softmax(Z5 + 10)
W5 = np.array([0.5, 0.3, 0.2])   # sunny, cloudy, rain — a softmax output
NOTRAIN5 = 1 - W5[2]

# ---------------------------------------------------------------- q06 why non-linearity
W6a = np.array([[1.0, -2.0], [0.5, 3.0]]); b6a = np.array([1.0, -1.0])
W6b = np.array([[2.0, 1.0]]); b6b = np.array([0.5])
X6 = np.array([2.0, -1.0])
TWO6 = W6b @ (W6a @ X6 + b6a) + b6b
WC6 = W6b @ W6a
BC6 = W6b @ b6a + b6b
ONE6 = WC6 @ X6 + BC6
XS6 = np.array([-2.0, -1.0, 0.0, 1.0, 2.0])
ABS6 = np.maximum(0, XS6) + np.maximum(0, -XS6)
XOR_X6 = np.array([[0., 0], [0, 1], [1, 0], [1, 1]])
XH1 = np.maximum(0, XOR_X6[:, 0] + XOR_X6[:, 1])
XH2 = np.maximum(0, XOR_X6[:, 0] + XOR_X6[:, 1] - 1)
XOR6 = XH1 - 2 * XH2

# ---------------------------------------------------------------- q07 Adam
def adam_steps(grads, lr=0.001, b1=0.9, b2=0.999, eps=1e-8):
    m = v = 0.0
    out = []
    for t in range(1, len(grads) + 1):
        g_ = grads[t - 1]
        m = b1 * m + (1 - b1) * g_
        v = b2 * v + (1 - b2) * g_ * g_
        mh = m / (1 - b1 ** t)
        vh = v / (1 - b2 ** t)
        out.append(lr * mh / (np.sqrt(vh) + eps))
    return out


A7 = 0.001
SMALL7 = adam_steps([0.001] * 3, lr=A7)
BIG7 = adam_steps([10.0] * 3, lr=A7)
GD_SMALL7, GD_BIG7 = A7 * 0.001, A7 * 10.0
LR1_7 = adam_steps([0.003], lr=1.0)[0]
FLIP7 = adam_steps([1.0, -1.0] * 5, lr=A7)
STEADY7 = adam_steps([1.0] * 10, lr=A7)

# ---------------------------------------------------------------- q08 multi-label
Z8 = np.array([2.0, -0.5, 1.2])          # car, bus, pedestrian
SIG8 = sig(Z8)
YES8 = SIG8 >= 0.5
SM8 = softmax(Z8)
SUM8 = SIG8.sum()
COMBOS8 = 2 ** 5

# ---------------------------------------------------------------- q09 derivatives
def J9(w):
    return w ** 3 - 2 * w


W9 = 1.5
EXACT9 = 3 * W9 ** 2 - 2
EST9 = {}
for _e in (1e-3, 1e-6, 1e-15, 1e-16):
    EST9[_e] = (J9(W9 + _e) - J9(W9)) / _e
ERR9_TINY = abs(EST9[1e-15] - EXACT9)
ERR9_GOOD = abs(EST9[1e-6] - EXACT9)


def P9(p):
    return (p - 8) * (100 - 3 * p)


DP9 = {p: 124 - 6 * p for p in (18.0, 22.0)}
FD9 = {p: (P9(p + 1e-4) - P9(p)) / 1e-4 for p in (18.0, 22.0)}
PEAK9 = 124 / 6

# ---------------------------------------------------------------- q10 backprop
W10, X10, B10, Y10 = 2.0, 1.5, -0.5, 4.0
C10 = W10 * X10
A10 = C10 + B10
D10 = A10 - Y10
J10 = 0.5 * D10 ** 2
DJ_DD10 = D10
DJ_DA10 = DJ_DD10 * 1.0
DJ_DC10 = DJ_DA10 * 1.0
DJ_DW10 = DJ_DC10 * X10
DJ_DB10 = DJ_DA10 * 1.0
WRONG10 = DJ_DC10 * W10


def _J10(w, b):
    return 0.5 * (w * X10 + b - Y10) ** 2


FD_W10 = (_J10(W10 + 1e-6, B10) - _J10(W10 - 1e-6, B10)) / 2e-6
PARAMS10 = 1_000_000
T_FWD10 = 0.01
NUM_T10 = 2 * PARAMS10 * T_FWD10
BP_T10 = 2 * T_FWD10


DRILLS = [

# =================================================================== q01
D("c2w2-q01",
  recall=M("Three calls, three objects you already built in C1.",
    """<p>From memory: what does each of <code>Sequential</code>, <code>compile</code> and
<code>fit</code> stand for, in the words you used in Course 1? Then list what happens
<b>inside</b> <code>fit</code>, in order, for one update.</p>""",
    """<ul><li><code>Sequential</code> &mdash; <b>the model</b>: how <var>f</var>(<var>x</var>) is computed.</li>
<li><code>compile</code> &mdash; <b>the loss and cost</b> (and which optimiser will minimise it).</li>
<li><code>fit</code> &mdash; <b>gradient descent</b>: the training loop.</li></ul>
<p>Inside <code>fit</code>, for one update: forward pass on a batch &rarr; loss &rarr; backpropagation
for every gradient &rarr; the optimiser updates every parameter. Then repeat, batch after batch,
epoch after epoch.</p>""",
    "Model, loss, optimiser: every training script is these three, dressed up.",
    "Building a paper plane: first you fold the plane, then you decide what counts as a good flight, "
    "then you keep throwing it and adjusting the folds.",
    [("model", "the recipe that turns an input into a prediction"),
     ("loss", "a number that says how wrong one prediction was"),
     ("optimiser", "the rule that nudges the weights to make the loss smaller"),
     ("epoch", "one full pass through all the training data")]),

  work=M("Count the parameters and the updates in one fit call.",
    """<p>A network takes %d inputs, has one hidden <code>Dense</code> layer of %d units and an output
layer of %d unit.</p>
<ol><li>How many parameters (weights and biases) does it have?</li>
<li>You call <code>fit</code> on %s examples with <code>batch_size=%d</code> and
<code>epochs=%d</code>. How many gradient-descent updates happen?</li></ol>""" % (
        N_IN1, H1, OUT1, "{:,}".format(M1), BATCH1, EPOCHS1),
    """<ol><li>Hidden: %d&times;%d weights + %d biases = %d. Output: %d&times;%d + %d = %d. Total
<b>%d</b>.</li>
<li>%s / %d rounds up to <b>%d</b> batches per epoch (the last one has only %d examples), so
%d &times; %d = <b>%d</b> updates. Each one changes all %d parameters at once.</li></ol>""" % (
        N_IN1, H1, H1, N_IN1 * H1 + H1, H1, OUT1, OUT1, H1 * OUT1 + OUT1, P1,
        "{:,}".format(M1), BATCH1, STEPS1, LAST1, STEPS1, EPOCHS1, UPD1, P1),
    "fit runs one update per batch, for every epoch, and each update moves every parameter.",
    "If you have a big pile of homework and do it in small stacks, you check your answers after each "
    "stack, not only at the very end.",
    [("batch", "a small group of examples used for one update"),
     ("batch_size", "how many examples go in each group (Keras uses 32 if you do not say)"),
     ("parameter", "a weight or bias the network learns")]),

  spot=M("Three lines in the wrong order.",
    """<p>A training script:</p>%s<p>What goes wrong, and why does it have to?</p>""" % code(
        "model = Sequential([Dense(25, activation='relu'), Dense(1, activation='sigmoid')])\n"
        "model.fit(X, y, epochs=10)\n"
        "model.compile(loss=BinaryCrossentropy())"),
    """<p><code>fit</code> is called <b>before</b> <code>compile</code>. Keras refuses to train: the
model must be compiled before fit.</p>
<p>It has to fail, because <code>fit</code> is gradient descent <b>on a cost</b>, and until
<code>compile</code> runs there is no cost to differentiate and no optimiser to take the steps.
Swap the last two lines.</p>""",
    "You cannot run gradient descent before saying what it should minimise.",
    "You cannot start a race before someone says where the finish line is.",
    [("compile", "the step that attaches the loss and the optimiser to the model"),
     ("fit", "the step that actually trains"),
     ("cost", "the average loss over all the training examples")]),

  transfer=M("A different framework, the same three pieces.",
    """<p>In another framework you write your own loop:</p>
<ol><li>define a network object;</li><li>pick a loss function and an optimiser object;</li>
<li><code>for</code> each batch: compute predictions, compute the loss, call a backward function,
call the optimiser's step function.</li></ol>
<p>Match each piece to <code>Sequential</code>, <code>compile</code> and <code>fit</code>. What does
Keras's <code>fit</code> hide from you?</p>""",
    """<p>Step 1 is <code>Sequential</code>. Step 2 is <code>compile</code>. Step 3 is
<code>fit</code>, written out by hand.</p>
<p><code>fit</code> hides the loop itself: splitting the data into batches, the forward pass, the
backward pass (backpropagation) and the parameter update, repeated for every epoch. Same three ideas,
just less typing.</p>""",
    "Every framework splits training into model, loss and optimiser; only how much it hides changes.",
    "Whether you bake with a bread machine or by hand, it is still dough, oven and time. The machine "
    "just does the kneading for you.",
    [("framework", "a library that builds and trains networks for you"),
     ("backward function", "the call that runs backpropagation"),
     ("loop", "code that repeats the same steps many times")]),
),

# =================================================================== q02
D("c2w2-q02",
  recall=M("ReLU, the sigmoid's slope, and why it matters in deep networks.",
    """<p>From memory: write ReLU and its derivative. What is the largest value the sigmoid's
derivative ever takes? Explain in two sentences why that number makes sigmoid a poor hidden
activation in a deep network.</p>""",
    """<p>ReLU: <var>g</var>(<var>z</var>) = max(0, <var>z</var>). Its derivative is <b>1</b> for
<var>z</var> &gt; 0 and 0 for <var>z</var> &lt; 0.</p>
<p>The sigmoid's derivative peaks at <b>%s</b>, at <var>z</var> = 0. Backpropagation multiplies
one such slope per layer, so the gradient reaching the early layers shrinks by at least a factor
of 4 per layer: the early layers barely learn. ReLU passes a slope of exactly 1 wherever a unit
is active.</p>""" % n(DS_BEST2, 2),
    "ReLU's slope is 1 where it is on, so gradients survive many layers; the sigmoid's is at most 0.25.",
    "Whispering a message down a line of ten people, each passing on only a quarter of what they "
    "heard: by the end nothing is left. ReLU passes the message on at full volume.",
    [("ReLU", "keep positive numbers as they are, turn negatives into 0"),
     ("vanishing gradient", "the learning signal shrinking to almost nothing on its way back"),
     ("hidden layer", "a layer between the input and the output")]),

  work=M("Multiply the slopes through eight layers.",
    """<p>Backprop multiplies one activation slope per layer. Through %d layers, compute the product
of the slopes for:</p>
<ol><li>sigmoid at its very best (<var>z</var> = 0 in every layer);</li>
<li>sigmoid with <var>z</var> = 2 in every layer;</li><li>ReLU with every unit active.</li></ol>""" % LAYERS2,
    """<ol><li><var>g</var>&prime;(0) = %s, so %s<sup>%d</sup> &asymp; <b>%s</b>.</li>
<li><var>g</var>&prime;(2) = &sigma;(2)(1 &minus; &sigma;(2)) &asymp; %s, so the product is
&asymp; <b>%s</b>.</li>
<li>1<sup>%d</sup> = <b>1</b>.</li></ol>
<p>Even in the sigmoid's best case the first layer hears about %s of the signal; the realistic case
is far worse.</p>""" % (
        n(DS_BEST2, 2), n(DS_BEST2, 2), LAYERS2, sci(PROD_BEST2, 2), n(DS_Z2, 4), sci(PROD_Z2, 1),
        LAYERS2, sci(PROD_BEST2, 1)),
    "Slopes multiply through layers, so anything below 1 shrinks the gradient exponentially.",
    "Take a quarter of a quarter of a quarter, eight times. The piece of cake left is too small to see.",
    [("g&prime;(z)", "the slope of the activation at z"),
     ("product", "the result of multiplying numbers together"),
     ("exponentially", "shrinking by the same factor again and again, so very fast")]),

  spot=M("&ldquo;Sigmoid never has a zero gradient, so it is the safer choice.&rdquo;",
    """<p>&ldquo;ReLU's gradient is exactly 0 for negative <var>z</var>, so those units cannot learn.
The sigmoid's gradient is never zero. So for hidden layers the sigmoid is the safer choice.&rdquo;</p>
<p>The first two sentences are true. Where does the reasoning fail?</p>""",
    """<p>&ldquo;Never zero&rdquo; is not &ldquo;big enough&rdquo;. At <var>z</var> = 5 the sigmoid's
slope is &asymp; <b>%s</b>, and through several layers these tiny numbers multiply towards zero
anyway. That is the vanishing gradient.</p>
<p>ReLU's zero applies only to units that are off <b>for that example</b>; every active unit passes
a slope of exactly 1. In practice that trains deep networks far better, which is why ReLU is the
default.</p>""" % n(DS_5, 4),
    "A slope that is tiny everywhere is worse than one that is exactly 1 where it matters.",
    "A tap that always drips a little is not better than one that runs fully when you open it.",
    [("saturate", "when the sigmoid is flat at either end and its slope is nearly 0"),
     ("active unit", "a ReLU unit whose input is positive, so it passes its value on")]),

  transfer=M("Negative targets with ReLU hidden layers.",
    """<p>You predict tomorrow's temperature change, which is often negative. A colleague says: &ldquo;We
can't use ReLU in the hidden layers, because ReLU outputs are never negative.&rdquo;</p>
<p>A hidden layer outputs <var>a</var> = ReLU([1.4, &minus;0.7, 2.0]). The linear output unit has
<var>w</var> = [%s] and <var>b</var> = %s. Compute <var>a</var> and the prediction. Is the colleague
right?</p>""" % (", ".join(n(v, 1) for v in W2o), n(B2o, 1)),
    """<p><var>a</var> = [%s]. Prediction = %s &times; %s + %s &times; %s + %s &times; %s + %s =
<b>%s</b>, negative.</p>
<p>The colleague is wrong. ReLU limits the <b>hidden</b> values; the output layer is linear, and
its weights can be negative, so the prediction can be any real number. The output activation is
chosen from the range of <var>y</var>; the hidden one stays ReLU.</p>""" % (
        _row(H2, 1), n(W2o[0], 1), n(H2[0], 1), n(W2o[1], 1), n(H2[1], 1), n(W2o[2], 1),
        n(H2[2], 1), n(B2o, 1), n(OUT2, 2)),
    "Hidden activations shape the features; the output layer sets the range of the prediction.",
    "Building blocks can all be positive, but if you are allowed to take some away at the end, you "
    "can still end up below zero.",
    [("linear output", "an output with no squashing, so any number is allowed"),
     ("range", "the set of values something can take")]),
),

# =================================================================== q03
D("c2w2-q03",
  recall=M("Range of y &rarr; output activation, for four kinds of target.",
    """<p>From memory, fill in the output activation <b>and</b> the loss for: (1) a yes/no label,
(2) any real number, (3) a non-negative amount, (4) exactly one of several classes. What decides
the hidden activation?</p>""",
    """<ol><li>Yes/no &rarr; <b>sigmoid</b>, binary cross-entropy.</li>
<li>Any real number &rarr; <b>linear</b>, mean squared error.</li>
<li>Non-negative &rarr; <b>ReLU</b>, mean squared error.</li>
<li>Exactly one class &rarr; <b>softmax</b>, (sparse) categorical cross-entropy.</li></ol>
<p>The hidden activation does not depend on the task: <b>ReLU</b> by default.</p>""",
    "The output activation is read off the range of y; the hidden one is ReLU.",
    "A cup is for drinks, a plate for food, a box for toys. You pick the container by what has to go "
    "in it.",
    [("output activation", "the squashing (or not) on the final layer"),
     ("binary cross-entropy", "the log loss for yes/no answers"),
     ("non-negative", "zero or bigger")]),

  work=M("One raw score, three output activations.",
    """<p>The last layer produces <var>z</var> = %s. Compute the prediction with a sigmoid, a linear and
a ReLU output. Then do the same for <var>z</var> = %s. Which output could predict tomorrow's
temperature in &deg;C?</p>""" % (n(Z3, 1), n(Z3b, 1)),
    """<p><var>z</var> = %s: sigmoid <b>%s</b>, linear <b>%s</b>, ReLU <b>%s</b>.</p>
<p><var>z</var> = %s: sigmoid <b>%s</b>, linear <b>%s</b>, ReLU <b>%s</b>.</p>
<p>Only the <b>linear</b> output can reach &minus;1.2&deg;C and 30&deg;C alike. The sigmoid is
trapped between 0 and 1, and ReLU can never go below zero.</p>""" % (
        n(Z3, 1), n(SIG3, 4), n(LIN3, 1), n(RELU3, 1),
        n(Z3b, 1), n(SIG3b, 4), n(Z3b, 1), n(Z3b, 1)),
    "The same score means a different prediction under each output activation.",
    "The same push on a door does different things if the door opens both ways, only one way, or "
    "only a little bit.",
    [("sigmoid", "squashes into a number between 0 and 1"),
     ("ReLU", "keeps positives, turns negatives into 0"),
     ("linear", "leaves the number as it is")]),

  spot=M("A house-price model that never gets close.",
    """<p>A model predicts house prices in $1000s (around %s). Its output layer is
<code>Dense(1, activation='sigmoid')</code> with mean squared error. Training &ldquo;converges&rdquo;
but every prediction is below 1. A colleague suggests training for longer. What is the real
problem?</p>""" % n(PRICE3, 0),
    """<p>The <b>output activation</b>. A sigmoid can never exceed 1, so even a perfect network predicts
at most 1 for a %s house. The squared error for that house can never drop below (%s &minus; 1)<sup>2</sup>
= <b>%s</b>, however long you train.</p>
<p>Use a <b>linear</b> output (or ReLU, since prices are never negative).</p>""" % (
        n(PRICE3, 0), n(PRICE3, 0), "{:,.0f}".format(BEST_ERR3)),
    "A capped output activation silently caps every prediction; more training cannot fix it.",
    "If your measuring jug only goes up to one litre, you can never measure a bucket, however "
    "carefully you pour.",
    [("cap", "an upper limit the output cannot pass"),
     ("converge", "settle down and stop improving")]),

  transfer=M("Four new targets.",
    """<p>Choose the output layer (units and activation) for each:</p>
<ol><li>the chance it rains tomorrow;</li><li>tomorrow's rainfall in millimetres;</li>
<li>which of 5 bus routes a rider takes today (one only);</li>
<li>the change in a share price tomorrow.</li></ol>""",
    """<ol><li>1 unit, <b>sigmoid</b>: a probability of yes.</li>
<li>1 unit, <b>ReLU</b>: an amount that is zero or more.</li>
<li>5 units, <b>softmax</b>: exactly one route.</li>
<li>1 unit, <b>linear</b>: up or down, any size.</li></ol>""",
    "Ask what values the answer can take, and pick the output that can produce exactly those.",
    "Is the answer yes or no, a how-much that can't be negative, one choice out of a few, or any "
    "number at all? Each has its own kind of answer box.",
    [("unit", "one output number of a layer"),
     ("softmax", "turns several scores into chances that add up to 1")]),
),

# =================================================================== q04
D("c2w2-q04",
  recall=M("from_logits=True: what it changes, and the catch.",
    """<p>From memory: what does <code>from_logits=True</code> tell the loss? What must the output
layer's activation be? What does <code>model.predict</code> return afterwards, and how do you get
probabilities?</p>""",
    """<p>It tells the loss it is receiving <b>raw scores</b> <var>z</var> (logits), so it computes
softmax and log <b>together</b> with a rearranged, stable formula.</p>
<p>The output layer must be <b>linear</b>. <code>model.predict</code> then returns logits (they can be
negative and do not sum to 1); apply softmax yourself to get probabilities.</p>""",
    "Hand the loss raw scores so it never has to compute a fragile probability first.",
    "Instead of rounding a number and then doing more maths with the rounded number, you do all the "
    "maths in one go and round only at the end.",
    [("logit", "the raw score before any squashing"),
     ("numerical stability", "getting the right answer even though computers round numbers"),
     ("overflow", "a number too big for the computer to store, so it becomes infinity")]),

  work=M("Softmax on large scores, naive and shifted.",
    """<p>Compute softmax of <var>z</var> = [%s]. Now add 800 to every score and compute it again
two ways: directly with <code>np.exp</code>, and after subtracting the largest score first.</p>""" % (
        ", ".join(n(v, 0) for v in Z4)),
    """<p>Softmax of [%s] = <b>%s</b>.</p>
<p>Plus 800, direct: e<sup>802</sup> overflows to <code>inf</code>, and inf/inf gives
<b>[%s]</b>.</p>
<p>Plus 800, shifted: subtract 802 first and you get <b>%s</b> &mdash; identical to the original,
because softmax only depends on the differences between scores.</p>""" % (
        ", ".join(n(v, 0) for v in Z4), _row(SM4, 4),
        ", ".join("nan" if np.isnan(v) else n(v, 4) for v in NAIVE4), _row(SHIFT4, 4)),
    "Subtracting the largest score changes nothing mathematically and prevents overflow.",
    "If everyone in a race started 800 metres further back, the winner would not change. Measuring "
    "from the leader keeps the numbers small.",
    [("inf", "infinity &mdash; what a computer gives when a number is too big"),
     ("nan", "not a number &mdash; what you get from infinity divided by infinity"),
     ("shift", "add or subtract the same amount from every score")]),

  spot=M("from_logits=True on top of a softmax layer.",
    """<p>The output layer is <code>Dense(3, activation='softmax')</code> and the loss is
<code>SparseCategoricalCrossentropy(from_logits=True)</code>. The model trains, but its confidence
looks oddly low. For scores <var>z</var> = [%s], the layer outputs <var>p</var> = %s. What does the
loss actually see?</p>""" % (", ".join(n(v, 0) for v in Z4d), _row(P4d, 3)),
    """<p>The loss is told these are logits, so it applies softmax <b>again</b>: softmax(%s) =
<b>%s</b>. The confident %s has been flattened to %s.</p>
<p>The softmax is applied twice. Fix: a <b>linear</b> output layer with <code>from_logits=True</code>,
or keep the softmax layer and set <code>from_logits=False</code>.</p>""" % (
        _row(P4d, 3), _row(DOUBLE4, 3), n(P4d[0], 3), n(DOUBLE4[0], 3)),
    "from_logits=True needs a linear output layer, or softmax gets applied twice.",
    "Squashing an orange that has already been juiced does not give you more juice; it just makes "
    "a mess.",
    [("double softmax", "applying softmax to numbers that are already probabilities"),
     ("from_logits=False", "telling the loss it is getting probabilities")]),

  transfer=M("The same trap in a yes/no model, in 32-bit floats.",
    """<p>A binary classifier stores numbers as 32-bit floats. For one example with true label 1 it
produces a raw score <var>z</var> = %s (confidently wrong). Compute the loss &minus;log(&sigma;(<var>z</var>))
naively in float32, then with the stable form log(1 + e<sup>&minus;<var>z</var></sup>).</p>""" % n(ZB4, 0),
    """<p>Naive: e<sup>%s</sup> overflows float32, so &sigma;(<var>z</var>) rounds to <b>%s</b>, and
&minus;log(0) = <b>%s</b>. One example turns the whole cost into infinity.</p>
<p>Stable: log(1 + e<sup>%s</sup>) &asymp; <b>%s</b>, a large but finite loss that still pushes the
model the right way. This is what <code>BinaryCrossentropy(from_logits=True)</code> does with a linear
output.</p>""" % (
        n(-ZB4, 0), n(SIGB4, 1), "inf" if np.isinf(NAIVEB4) else n(NAIVEB4, 2),
        n(-ZB4, 0), n(STABLEB4, 2)),
    "The same fix works for yes/no outputs: give the loss the raw score.",
    "A thermometer that breaks when it gets too hot tells you nothing. A sturdier one reads 120 "
    "degrees, which is useful even if it is bad news.",
    [("float32", "a way of storing numbers that keeps about 7 digits"),
     ("underflow", "a number too small to store, so it becomes 0")]),
),

# =================================================================== q05
D("c2w2-q05",
  recall=M("Softmax, and four things true of every output.",
    """<p>From memory: write the softmax formula for output <var>j</var>. Then list four facts about
its outputs.</p>""",
    """<p><var>a</var><sub>j</sub> = e<sup><var>z</var><sub>j</sub></sup> / &Sigma;<sub>k</sub>
e<sup><var>z</var><sub>k</sub></sup>.</p>
<ul><li>Each is between 0 and 1, and together they <b>sum to 1</b>.</li>
<li>The prediction is the <b>argmax</b>.</li>
<li>They are <b>coupled</b>: raising one score lowers every other output.</li>
<li>Adding the same constant to every score changes nothing.</li></ul>""",
    "Softmax shares one unit of probability among the classes, so they compete.",
    "Sharing one pizza: if one friend gets a bigger slice, everyone else's slice has to get smaller.",
    [("&Sigma; (sigma)", "add them all up"),
     ("argmax", "which position holds the biggest value"),
     ("coupled", "connected, so changing one changes the others")]),

  work=M("Compute a softmax, then raise one score.",
    """<p>Scores <var>z</var> = [%s]. Compute the softmax and the predicted class. Then add 1 to the
second score only and recompute. What happened to the other three outputs?</p>""" % (
        ", ".join(n(v, 1) for v in Z5)),
    """<p>Softmax = <b>%s</b> (sum %s); predicted class: <b>2</b>.</p>
<p>With <var>z</var><sub>2</sub> + 1: <b>%s</b>. Output 2 rose from %s to %s, and <b>all three
others fell</b>, although their own scores did not change.</p>""" % (
        _row(S5, 4), n(S5.sum(), 0), _row(S5up, 4), n(S5[1], 4), n(S5up[1], 4)),
    "Raising one score takes probability away from every other class.",
    "In a vote with fixed votes, if one candidate gains, the others must lose some.",
    [("score / logit", "the raw number for one class before softmax"),
     ("predicted class", "the class with the highest output")]),

  spot=M("&ldquo;Softmax only cares about differences, so doubling is harmless.&rdquo;",
    """<p>&ldquo;Softmax only depends on differences between scores. So doubling every score changes
nothing, just like adding 10 to every score.&rdquo; For <var>z</var> = [%s], test both claims.</p>""" % (
        ", ".join(n(v, 1) for v in Z5)),
    """<p>Adding 10: <b>%s</b> &mdash; unchanged, correct.</p>
<p>Doubling: <b>%s</b> &mdash; different. Doubling also doubles every <b>difference</b>, so the
largest class gets more confident (%s &rarr; %s). The reasoning fails at &ldquo;just like adding&rdquo;:
adding keeps differences fixed, multiplying does not.</p>""" % (
        _row(S5p10, 4), _row(S5x2, 4), n(S5[1], 4), n(S5x2[1], 4)),
    "Adding a constant leaves softmax unchanged; multiplying makes it sharper.",
    "If everyone in your class grows 10 cm, the tallest kid is still tallest by the same amount. If "
    "everyone doubles in height, the gaps double too.",
    [("difference", "how far apart two numbers are"),
     ("sharper", "more sure of the top answer")]),

  transfer=M("Weather tomorrow: what can you say from one softmax?",
    """<p>A weather model's softmax over (sunny, cloudy, rain) is [%s]. What is the probability it
does <b>not</b> rain? Could you do the same subtraction if the model used three independent sigmoids
instead?</p>""" % ", ".join(n(v, 1) for v in W5),
    """<p>With softmax the classes are exclusive and sum to 1, so P(not rain) = 1 &minus; %s =
<b>%s</b>.</p>
<p>With independent sigmoids, no: the outputs need not sum to 1, each answers its own yes/no
question, and &ldquo;1 minus the others&rdquo; has no meaning. You would read the rain output on its
own: P(not rain) = 1 &minus; that one output.</p>""" % (n(W5[2], 1), n(NOTRAIN5, 1)),
    "Softmax outputs form one shared budget; sigmoid outputs are separate questions.",
    "If exactly one of three things will happen, the chances must add to a whole. If they are three "
    "separate questions, they don't have to.",
    [("exclusive", "only one can be true at a time"),
     ("independent", "each can be true or false on its own")]),
),

# =================================================================== q06
D("c2w2-q06",
  recall=M("Why stacked linear layers collapse.",
    """<p>From memory: write two linear layers as one formula and show that it is a single linear
layer. What are the combined weight matrix and bias?</p>""",
    """<p><var>a</var> = <var>W</var><sub>2</sub>(<var>W</var><sub>1</sub><var>x</var> + <var>b</var><sub>1</sub>)
+ <var>b</var><sub>2</sub> = (<var>W</var><sub>2</sub><var>W</var><sub>1</sub>)<var>x</var> +
(<var>W</var><sub>2</sub><var>b</var><sub>1</sub> + <var>b</var><sub>2</sub>).</p>
<p>That is one layer with <var>W</var> = <var>W</var><sub>2</sub><var>W</var><sub>1</sub> and
<var>b</var> = <var>W</var><sub>2</sub><var>b</var><sub>1</sub> + <var>b</var><sub>2</sub>. Without an
activation in between, any number of layers collapses like this.</p>""",
    "Linear on top of linear is still linear; only a non-linearity makes depth count.",
    "Two magnifying glasses stacked together are still just one stronger magnifying glass.",
    [("linear", "made only of multiplying by numbers and adding"),
     ("composition", "doing one function, then another on its result"),
     ("collapse", "many layers behaving exactly like one")]),

  work=M("Two layers, then the one layer they equal.",
    """<p>Layer 1: <var>W</var><sub>1</sub> = [[1, &minus;2], [0.5, 3]], <var>b</var><sub>1</sub> = [1, &minus;1].
Layer 2: <var>W</var><sub>2</sub> = [[2, 1]], <var>b</var><sub>2</sub> = [0.5]. No activations.</p>
<ol><li>Compute the output for <var>x</var> = [2, &minus;1] through both layers.</li>
<li>Compute <var>W</var><sub>2</sub><var>W</var><sub>1</sub> and <var>W</var><sub>2</sub><var>b</var><sub>1</sub>
+ <var>b</var><sub>2</sub>, and the output of that single layer.</li></ol>""",
    """<ol><li><var>W</var><sub>1</sub><var>x</var> + <var>b</var><sub>1</sub> = [%s]; then layer 2
gives <b>%s</b>.</li>
<li><var>W</var> = [%s], <var>b</var> = %s; <var>W</var><var>x</var> + <var>b</var> = <b>%s</b>.</li></ol>
<p>Same answer: the two-layer network is exactly this one layer.</p>""" % (
        ", ".join(n(v, 1) for v in W6a @ X6 + b6a), n(TWO6[0], 2),
        ", ".join(n(v, 1) for v in WC6[0]), n(BC6[0], 1), n(ONE6[0], 2)),
    "Two linear layers multiply out to one, so they can never learn more than one.",
    "Two steps of &lsquo;double it, then add one&rsquo; can always be replaced by a single rule that "
    "does the same.",
    [("W", "a table of weights"),
     ("b", "the bias added at the end")]),

  spot=M("&ldquo;ReLU is piecewise linear, so ReLU networks are linear too.&rdquo;",
    """<p>&ldquo;ReLU is just two straight lines joined at 0. Straight lines are linear. So a network of
ReLUs is a linear model and has the same collapse problem.&rdquo;</p>
<p>Test it: compute ReLU(<var>x</var>) + ReLU(&minus;<var>x</var>) for <var>x</var> = [%s]. Where does
the argument break?</p>""" % ", ".join(n(v, 0) for v in XS6),
    """<p>The result is <b>%s</b>: that is |<var>x</var>|, a V shape, which no single straight line can
produce.</p>
<p>The argument breaks at &ldquo;straight pieces, so linear&rdquo;. A linear function must be one
straight line everywhere; ReLU bends at 0. Adding many units with bends in different places can
approximate any curve.</p>""" % _row(ABS6, 0),
    "One bend is enough: combining many ReLUs builds curves no linear model can.",
    "A paperclip is made of straight bits, but bend them and you get a shape no straight wire can make.",
    [("piecewise linear", "made of straight pieces joined at bends"),
     ("|x|", "the size of x, ignoring its sign")]),

  transfer=M("XOR: one hidden layer does what no line can.",
    """<p>XOR is 1 when exactly one input is 1. No linear model gets all four cases right. Use
<var>h</var><sub>1</sub> = ReLU(<var>x</var><sub>1</sub> + <var>x</var><sub>2</sub>),
<var>h</var><sub>2</sub> = ReLU(<var>x</var><sub>1</sub> + <var>x</var><sub>2</sub> &minus; 1) and output
<var>h</var><sub>1</sub> &minus; 2<var>h</var><sub>2</sub>. Compute it for (0,0), (0,1), (1,0), (1,1).</p>""",
    """<p><var>h</var><sub>1</sub> = [%s], <var>h</var><sub>2</sub> = [%s], output = <b>[%s]</b>:
exactly XOR.</p>
<p>The ReLU bend in <var>h</var><sub>2</sub> switches on only when both inputs are 1, and that is what
lets the network subtract back down. Remove the ReLUs and it collapses to one linear function, which
cannot do this.</p>""" % (
        ", ".join(n(v, 0) for v in XH1), ", ".join(n(v, 0) for v in XH2),
        ", ".join(n(v, 0) for v in XOR6)),
    "Non-linear hidden units let a network represent patterns no single line can.",
    "&lsquo;One or the other, but not both&rsquo; needs a rule that changes its mind when both "
    "happen. A straight line can't change its mind.",
    [("XOR", "exclusive or: true when exactly one input is true"),
     ("hidden unit", "one neuron in a hidden layer")]),
),

# =================================================================== q07
D("c2w2-q07",
  recall=M("Adam's two running averages, and its defaults.",
    """<p>From memory: what two quantities does Adam keep for <b>every</b> parameter? Write the update.
What are the usual defaults for the learning rate, &beta;<sub>1</sub>, &beta;<sub>2</sub> and
&epsilon;?</p>""",
    """<p>A running average of the gradient, <var>m</var>, and of the <b>squared</b> gradient,
<var>v</var>. Update: <var>w</var> &larr; <var>w</var> &minus; &alpha;&middot;<var>m&#770;</var> /
(&radic;<var>v&#770;</var> + &epsilon;), where the hats are bias-corrected averages.</p>
<p>Defaults: &alpha; = 10<sup>&minus;3</sup>, &beta;<sub>1</sub> = 0.9, &beta;<sub>2</sub> = 0.999,
&epsilon; &asymp; 10<sup>&minus;8</sup>. Dividing by &radic;<var>v</var> gives each parameter its own
effective step size.</p>""",
    "Adam divides each parameter's step by how big its gradients have been, so each gets its own pace.",
    "Like a hiker who takes long strides on flat paths and small careful steps on bumpy ones, "
    "separately for each foot.",
    [("momentum (m)", "an average of recent gradients &mdash; the direction you've been going"),
     ("v", "an average of squared gradients &mdash; how big the gradients have been"),
     ("&epsilon; (epsilon)", "a tiny number that stops division by zero")]),

  work=M("Two parameters, tiny and huge gradients: compare step sizes.",
    """<p>Parameter A always has gradient 0.001; parameter B always has gradient 10. With &alpha; =
%s, compute the step size each takes for three steps under plain gradient descent, then under Adam
(&beta;<sub>1</sub> = 0.9, &beta;<sub>2</sub> = 0.999, with bias correction).</p>""" % n(A7, 3),
    """<p>Plain gradient descent: A moves %s per step, B moves %s per step &mdash; a 10,000&times;
difference.</p>
<p>Adam: A moves <b>%s</b>, B moves <b>%s</b>, every step. Both are &asymp; &alpha;, because Adam
divides each gradient by its own typical size.</p>""" % (
        sci(GD_SMALL7, 0), n(GD_BIG7, 2), _row(SMALL7, 6), _row(BIG7, 6)),
    "Adam takes roughly the same-sized step for each parameter, whatever the scale of its gradient.",
    "Two kids walking: one on sand, one on ice. Adam gives each the right stride so they keep pace.",
    [("step size", "how far a parameter moves in one update"),
     ("bias correction", "a fix that stops the averages starting too close to 0")]),

  spot=M("&ldquo;Adam adapts, so the learning rate doesn't matter.&rdquo;",
    """<p>&ldquo;Adam adapts the learning rate automatically, so I set <code>learning_rate=1.0</code>
and let it sort itself out.&rdquo; On the first step, a parameter has gradient 0.003. How far does
Adam move it?</p>""",
    """<p>On step 1 the bias-corrected <var>m&#770;</var>/&radic;<var>v&#770;</var> is just the sign of
the gradient, so the step is &alpha; &times; 1 &asymp; <b>%s</b> &mdash; a full unit, for a gradient
of only 0.003. Every parameter jumps by about 1 at once, and training is likely to blow up.</p>
<p>Adam adapts <b>around</b> &alpha;; it does not remove it. Start at 10<sup>&minus;3</sup>.</p>""" % (
        n(LR1_7, 4)),
    "Adam's steps are about the size of the learning rate, so a huge learning rate means huge steps.",
    "A clever car that adjusts its speed to the road still drives too fast if you set the top speed "
    "to 300.",
    [("learning rate", "the base step size you choose"),
     ("blow up", "the cost shoots up and turns into nan")]),

  transfer=M("A gradient that flips sign every step.",
    """<p>A parameter sits in a narrow valley, so its gradient alternates +1, &minus;1, +1, &minus;1
&hellip; for 10 steps. Compute Adam's step on each step (&alpha; = %s), and compare with a parameter
whose gradient is +1 every step.</p>""" % n(A7, 3),
    """<p>Alternating: steps <b>%s</b>. After the first few steps the momentum <var>m</var> nearly
cancels out, so the steps shrink well below &alpha; and keep switching direction.</p>
<p>Steady: steps <b>%s</b>, all &asymp; &alpha;. Adam moves fast in directions that agree from step to
step and holds back in directions that keep flipping. That is how it calms a zig-zag.</p>""" % (
        _row(FLIP7, 5), _row(STEADY7, 5)),
    "Momentum cancels in directions that keep flipping and builds up in directions that agree.",
    "If someone keeps saying &lsquo;left, right, left, right&rsquo;, you stop moving much. If they "
    "keep saying &lsquo;forward&rsquo;, you walk on confidently.",
    [("oscillate", "swing back and forth"),
     ("narrow valley", "a cost shape that is steep one way and flat the other")]),
),

# =================================================================== q08
D("c2w2-q08",
  recall=M("Multi-label vs multiclass: one question decides it.",
    """<p>From memory: what single question decides between softmax and sigmoids at the output? Write
the output layer and loss for each case.</p>""",
    """<p><b>Can two answers be true at once?</b></p>
<ul><li>No (multiclass): <var>n</var> units, <b>softmax</b>, (sparse) categorical cross-entropy.</li>
<li>Yes (multi-label): <var>n</var> units, <b>sigmoid on each</b>, binary cross-entropy on each.</li></ul>""",
    "Several answers can be true &rarr; independent sigmoids. Exactly one &rarr; softmax.",
    "&lsquo;Which flavour is your one scoop?&rsquo; has one answer. &lsquo;Which toppings do you "
    "want?&rsquo; can have several.",
    [("multiclass", "exactly one class is correct"),
     ("multi-label", "any combination of labels can be correct"),
     ("independent sigmoids", "one separate yes/no output per label")]),

  work=M("Same scores, sigmoids and softmax.",
    """<p>For one image the output scores for (car, bus, pedestrian) are <var>z</var> = [%s].
Compute the sigmoid of each and decide yes/no at 0.5. Then compute the softmax of the same scores.
Which reads the scene correctly if a car and a pedestrian are both present?</p>""" % (
        ", ".join(n(v, 1) for v in Z8)),
    """<p>Sigmoids: <b>%s</b> &rarr; car <b>%s</b>, bus <b>%s</b>, pedestrian <b>%s</b>.</p>
<p>Softmax: <b>%s</b> &mdash; one shared budget, read as &ldquo;car&rdquo; only.</p>
<p>The sigmoids report both objects. Softmax can only pick one.</p>""" % (
        _row(SIG8, 3), "yes" if YES8[0] else "no", "yes" if YES8[1] else "no",
        "yes" if YES8[2] else "no", _row(SM8, 3)),
    "Sigmoids answer each label separately; softmax forces them to compete.",
    "Three separate light switches can all be on. A dial can only point at one setting.",
    [("threshold", "the cut-off, like 0.5, above which you say yes"),
     ("scene", "everything in one picture")]),

  spot=M("&ldquo;The outputs sum to more than 1, so the model is broken.&rdquo;",
    """<p>A multi-label model with three sigmoid outputs gives %s for one image. A teammate says:
&ldquo;These add up to %s. Probabilities must sum to 1, so something is broken.&rdquo; Who is
right?</p>""" % (_row(SIG8, 3), n(SUM8, 3)),
    """<p>The model is fine. Each sigmoid is the probability of <b>its own</b> yes/no event, and the
events are not exclusive, so there is no reason for them to add to 1. The sum rule applies only to
exclusive classes, as in softmax.</p>""",
    "Only exclusive classes have to sum to 1; independent labels don't.",
    "The chance it is sunny and the chance you eat ice cream are separate questions. Their chances "
    "don't have to add up to anything.",
    [("probability", "a chance between 0 and 1"),
     ("exclusive", "only one can happen")]),

  transfer=M("Four new problems: softmax or sigmoids?",
    """<p>Choose the output for each:</p>
<ol><li>tagging a song with any of 20 moods;</li><li>a film's age rating (U, PG, 12, 15, 18);</li>
<li>which diseases an X-ray shows, from a list of 14;</li><li>the language a text is written in.</li></ol>
<p>And: if you used softmax over every combination of 5 labels instead, how many classes would that
need?</p>""",
    """<ol><li><b>Sigmoids</b> (20 units): a song can be calm and happy.</li>
<li><b>Softmax</b> (5 units): exactly one rating.</li>
<li><b>Sigmoids</b> (14 units): a patient can have several findings.</li>
<li><b>Softmax</b>, if each text has one language.</li></ol>
<p>All combinations of 5 labels: 2<sup>5</sup> = <b>%d</b> classes, and it grows exponentially &mdash;
which is why independent sigmoids are used instead.</p>""" % COMBOS8,
    "Decide by whether the answers exclude each other, not by how many there are.",
    "A film gets one age rating, but a song can feel more than one way.",
    [("2<sup>5</sup>", "2 multiplied by itself 5 times"),
     ("combination", "a set of labels that are all true together")]),
),

# =================================================================== q09
D("c2w2-q09",
  recall=M("What a derivative is, and how to estimate one.",
    """<p>From memory: define the derivative of <var>J</var>(<var>w</var>) in words. Write the
nudge formula for estimating it. What do its sign and size tell gradient descent?</p>""",
    """<p>How much <var>J</var> changes per unit change in <var>w</var>, for a tiny nudge: the slope at
that point.</p>
<p>Estimate: (<var>J</var>(<var>w</var> + &epsilon;) &minus; <var>J</var>(<var>w</var>)) / &epsilon; for a
small &epsilon;.</p>
<p>Sign: which way is uphill (step the other way). Size: how steep, so how big the step
&alpha;&middot;slope is.</p>""",
    "A derivative is the slope: how fast the output changes when you nudge the input.",
    "On a slide, the derivative is how steep it is where you're sitting. Steep means you'll whoosh; "
    "flat means you'll barely move.",
    [("derivative", "the slope of a function at one point"),
     ("&epsilon; (epsilon)", "a tiny nudge"),
     ("slope", "how much it goes up for each step across")]),

  work=M("Estimate a slope by nudging, and check it.",
    """<p><var>J</var>(<var>w</var>) = <var>w</var><sup>3</sup> &minus; 2<var>w</var>. At <var>w</var> =
%s, estimate the derivative with &epsilon; = 0.001 and &epsilon; = 0.000001. Compare with the exact
derivative 3<var>w</var><sup>2</sup> &minus; 2.</p>""" % n(W9, 1),
    """<p>&epsilon; = 0.001: <b>%s</b>. &epsilon; = 0.000001: <b>%s</b>. Exact: 3 &times; %s<sup>2</sup>
&minus; 2 = <b>%s</b>.</p>
<p>The smaller nudge gets closer, as it should: the estimate becomes the slope as &epsilon; shrinks.</p>""" % (
        n(EST9[1e-3], 6), n(EST9[1e-6], 6), n(W9, 1), n(EXACT9, 2)),
    "Nudge, measure the change, divide by the nudge: that approaches the true slope.",
    "To see how steep a hill is, take one tiny step and see how much higher you got.",
    [("estimate", "a close guess worked out from numbers"),
     ("exact", "the true value from the formula")]),

  spot=M("&ldquo;Smaller &epsilon; is always more accurate.&rdquo;",
    """<p>&ldquo;The estimate gets better as &epsilon; shrinks, so I use &epsilon; = 10<sup>&minus;12</sup>
to be really accurate.&rdquo; For the same <var>J</var> at <var>w</var> = %s, the estimate with
&epsilon; = 10<sup>&minus;15</sup> is %s. Exact is %s. What went wrong?</p>""" % (
        n(W9, 1), n(EST9[1e-15], 4), n(EXACT9, 2)),
    """<p>Its error is about <b>%s</b>, against about <b>%s</b> for &epsilon; = 10<sup>&minus;6</sup>.
With &epsilon; that tiny, <var>J</var>(<var>w</var> + &epsilon;) and <var>J</var>(<var>w</var>) agree
in almost every digit the computer stores, and subtracting them leaves mostly rounding noise. At
&epsilon; = 10<sup>&minus;16</sup> the two values are identical and the estimate is <b>%s</b>.</p>
<p>&ldquo;Always&rdquo; is the error: in exact maths smaller is better, but in floating point there
is a sweet spot.</p>""" % (n(ERR9_TINY, 2), sci(ERR9_GOOD, 1), n(EST9[1e-16], 0)),
    "Too large a nudge is inaccurate maths; too small a nudge is drowned in rounding.",
    "Measuring a step that is thinner than a hair with a ruler marked only in millimetres just gives "
    "you guesswork.",
    [("rounding error", "small mistakes from the computer keeping only so many digits"),
     ("floating point", "how computers store decimal numbers")]),

  transfer=M("A shop's profit, and which way to move the price.",
    """<p>A shop's daily profit at price <var>p</var> is <var>P</var>(<var>p</var>) =
(<var>p</var> &minus; 8)(100 &minus; 3<var>p</var>), whose derivative is 124 &minus; 6<var>p</var>. At a
price of $18 and of $22, what is the derivative, and should the price go up or down? Check one by
nudging.</p>""",
    """<p>At $18: <b>%s</b> (nudge estimate %s) &mdash; positive, so raising the price raises profit.</p>
<p>At $22: <b>%s</b> (nudge estimate %s) &mdash; negative, so lower it. The best price is where the
derivative is 0: <var>p</var> = 124/6 &asymp; <b>$%s</b>.</p>
<p>Gradient descent does the same thing for a cost, just walking downhill instead of up.</p>""" % (
        n(DP9[18.0], 0), n(FD9[18.0], 3), n(DP9[22.0], 0), n(FD9[22.0], 3), n(PEAK9, 2)),
    "The sign of the derivative says which way to move; zero marks the top or bottom.",
    "If raising your lemonade price a little earns you more, raise it. If it earns you less, you "
    "went too far.",
    [("profit", "money earned minus money spent"),
     ("maximum", "the highest point")]),
),

# =================================================================== q10
D("c2w2-q10",
  recall=M("Forward, then backward: what each pass does.",
    """<p>From memory: what does the forward pass compute and store? Where does the backward pass
start, and what does it multiply at each node? Why is it so much cheaper than nudging every weight?</p>""",
    """<p>Forward: every node's value, left to right, <b>stored</b> for later.</p>
<p>Backward: start with &part;<var>J</var>/&part;<var>J</var> = 1 and walk right to left, multiplying
by each node's <b>local derivative</b> (the chain rule). Every gradient comes out of one backward
pass, which costs about the same as one forward pass &mdash; instead of one or two extra forward
passes per weight.</p>""",
    "Backprop is the chain rule applied once, backwards, giving every gradient for the price of one pass.",
    "Following a domino run backwards from the last domino, you can say how much each one mattered, "
    "one link at a time.",
    [("computation graph", "a diagram of every small calculation and how they connect"),
     ("chain rule", "multiply the slopes of each step to get the slope of the whole chain"),
     ("local derivative", "the slope of one small step on its own")]),

  work=M("Forward and backward on a five-node graph.",
    """<p><var>c</var> = <var>w</var><var>x</var>, <var>a</var> = <var>c</var> + <var>b</var>,
<var>d</var> = <var>a</var> &minus; <var>y</var>, <var>J</var> = &frac12;<var>d</var><sup>2</sup>, with
<var>w</var> = %s, <var>x</var> = %s, <var>b</var> = %s, <var>y</var> = %s. Do the forward pass, then
the backward pass for &part;<var>J</var>/&part;<var>w</var> and &part;<var>J</var>/&part;<var>b</var>.</p>""" % (
        n(W10, 1), n(X10, 1), n(B10, 1), n(Y10, 1)),
    """<p>Forward: <var>c</var> = %s, <var>a</var> = %s, <var>d</var> = %s, <var>J</var> = %s.</p>
<p>Backward: &part;<var>J</var>/&part;<var>d</var> = <var>d</var> = %s; through + and &minus; the slope
passes unchanged, so &part;<var>J</var>/&part;<var>a</var> = &part;<var>J</var>/&part;<var>c</var> = %s
and &part;<var>J</var>/&part;<var>b</var> = <b>%s</b>; &part;<var>c</var>/&part;<var>w</var> =
<var>x</var>, so &part;<var>J</var>/&part;<var>w</var> = %s &times; %s = <b>%s</b>.</p>
<p>A nudge check gives %s.</p>""" % (
        n(C10, 1), n(A10, 1), n(D10, 2), n(J10, 4), n(DJ_DD10, 2), n(DJ_DC10, 2), n(DJ_DB10, 2),
        n(DJ_DC10, 2), n(X10, 1), n(DJ_DW10, 4), n(FD_W10, 4)),
    "Store values going forward, multiply local slopes coming back.",
    "Going forward you write down every number. Coming back you ask each step &lsquo;how much did "
    "you pass on?&rsquo; and multiply.",
    [("forward pass", "working out every value from left to right"),
     ("backward pass", "working out every slope from right to left"),
     ("&part;J/&part;w", "how much J changes when w is nudged")]),

  spot=M("One local derivative, the wrong way round.",
    """<p>For the same graph, a student writes:</p>
<p>&part;<var>J</var>/&part;<var>c</var> = %s. Since <var>c</var> = <var>w</var><var>x</var>, the local
derivative is <var>w</var>, so &part;<var>J</var>/&part;<var>w</var> = %s &times; %s = %s.</p>
<p>Find the slip and give the right value.</p>""" % (
        n(DJ_DC10, 2), n(DJ_DC10, 2), n(W10, 1), n(WRONG10, 2)),
    """<p>The local derivative of <var>c</var> = <var>w</var><var>x</var> <b>with respect to
<var>w</var></b> is <var>x</var>, not <var>w</var>: nudge <var>w</var> by 1 and <var>c</var> moves by
<var>x</var>. So &part;<var>J</var>/&part;<var>w</var> = %s &times; %s = <b>%s</b>, which matches the nudge
check (%s).</p>""" % (n(DJ_DC10, 2), n(X10, 1), n(DJ_DW10, 4), n(FD_W10, 4)),
    "For a product, the slope with respect to one factor is the other factor.",
    "If you buy x apples at w pounds each, one more pound per apple costs you x more pounds, not w.",
    [("with respect to", "which input you are nudging"),
     ("product", "two things multiplied together")]),

  transfer=M("Why nobody trains by nudging.",
    """<p>A network has %s parameters and one forward pass takes %s seconds. How long does one gradient
take if you estimate every derivative by nudging each weight up and down (two forward passes per
weight)? How long with backprop (about one forward plus one backward pass)?</p>""" % (
        "{:,}".format(PARAMS10), n(T_FWD10, 2)),
    """<p>Nudging: 2 &times; %s &times; %s s = <b>%s s</b>, about %s hours, for <b>one</b> update.</p>
<p>Backprop: about %s s. Nudging is still useful for one thing: checking a hand-written backprop on
a few weights.</p>""" % (
        "{:,}".format(PARAMS10), n(T_FWD10, 2), "{:,.0f}".format(NUM_T10), n(NUM_T10 / 3600, 1),
        n(BP_T10, 2)),
    "Backprop's cost does not grow with the number of weights the way nudging does.",
    "Checking every light bulb in a stadium one by one takes all night. A map showing which wire "
    "feeds which bulb tells you at once.",
    [("gradient check", "using nudges to test that backprop's answers are right"),
     ("update", "one step of changing the weights")]),
),
]
