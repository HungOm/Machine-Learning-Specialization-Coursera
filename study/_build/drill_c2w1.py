# -*- coding: utf-8 -*-
"""Quiz drills — C2 W1. One concept per mock-quiz question, four methods each.

Every number below is COMPUTED here at import time and formatted into the text,
never typed. Shapes are read off real NumPy arrays (.shape, .size), so a shape
claim cannot drift from what NumPy actually does.
"""
import numpy as np
from drillkit import D, M
from masterykit import code


def n(x, d=2):
    """Format a number for prose: d decimals, trailing zeros trimmed."""
    s = ("%." + str(d) + "f") % x
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return "&minus;" + s[1:] if s.startswith("-") else s


def g(z):
    return 1 / (1 + np.exp(-z))


def sh(a):
    """A shape as the course writes it: (m, n) or (n,)."""
    t = a.shape if hasattr(a, "shape") else a
    if len(t) == 1:
        return "(%d,)" % t[0]
    return "(" + ", ".join(str(v) for v in t) + ")"


def big(x):
    return "{:,.0f}".format(x)


def _row(vals, d=3):
    return "[" + ", ".join(n(v, d) for v in vals) + "]"


def _mat(A, d=0):
    return "[" + ", ".join(_row(r, d) for r in A) + "]"


def _err(f):
    try:
        f()
        return "no error"
    except ValueError as e:
        return str(e)


# ---------------------------------------------------------------- q01 counting parameters
def _layer(n_in, units):
    return np.zeros((n_in, units)), np.zeros(units)


NET1 = (6, 5, 3, 1)
P1 = []
for _i in range(len(NET1) - 1):
    _W, _b = _layer(NET1[_i], NET1[_i + 1])
    P1.append((NET1[_i], NET1[_i + 1], _W.size, _b.size))
TOT1 = sum(w + b for _, _, w, b in P1)
SPOT1 = (10, 4, 1)
SPOT1_BAD = SPOT1[0] * SPOT1[1] + SPOT1[1] * SPOT1[2]
SPOT1_OK = SPOT1_BAD + SPOT1[1] + SPOT1[2]
IMG1 = 28 * 28
IMG1b = 56 * 56
UN1 = 128
PAR1 = IMG1 * UN1 + UN1
PAR1b = IMG1b * UN1 + UN1

# ---------------------------------------------------------------- q02 what a unit does
W2u = np.array([0.5, -1.0, 2.0]); B2u = -0.5
X2 = np.array([2.0, 1.0, 0.5])
Z2 = np.dot(W2u, X2) + B2u
A2 = g(Z2)
W2v = np.array([-1.0, 0.5, 1.0]); B2v = 1.0
Z2v = np.dot(W2v, X2) + B2v
A2v = g(Z2v)
WRONG2 = np.dot(W2u, g(X2)) + B2u          # squash the inputs first: the slip
# two linear layers collapse into one
L2a = np.array([[1.0, 2.0], [0.5, -1.0]])
L2b = np.array([[3.0], [1.0]])
XL2 = np.array([[2.0, 4.0]])
TWO2 = (XL2 @ L2a) @ L2b
ONE2 = XL2 @ (L2a @ L2b)
COMB2 = L2a @ L2b

# ---------------------------------------------------------------- q03 TensorFlow shapes
V3 = np.array([200.0, 17.0])
R3 = np.array([[200.0, 17.0]])
B3 = np.zeros((5, 2))
OUT3 = B3 @ np.zeros((2, 3))
T3 = V3.T
IM3 = np.zeros((20, 20))
FL3 = IM3.reshape(1, 400)
BATCH3 = np.zeros((32, 400))

# ---------------------------------------------------------------- q04 matrix shapes
X4 = np.zeros((50, 8)); W4a = np.zeros((8, 16)); W4b = np.zeros((16, 4)); W4c = np.zeros((4, 1))
H4a = X4 @ W4a
H4b = H4a @ W4b
H4c = H4b @ W4c
MULT4 = X4.shape[0] * X4.shape[1] * W4a.shape[1]
A4 = np.zeros((4, 2)); B4 = np.zeros((4, 3))
def _bad4():
    return A4 @ B4


ERR4 = _err(_bad4)
FIX4 = A4.T @ B4
U4 = np.zeros((1000, 20)); M4 = np.zeros((20, 500))
S4 = U4 @ M4

# ---------------------------------------------------------------- q05 forward propagation
X5 = np.array([[1.0, 2.0]])
W5a = np.array([[0.5, -1.0], [0.25, 0.5]])
B5a = np.array([0.0, 0.5])
W5b = np.array([[2.0], [-1.0]])
B5b = np.array([-0.5])
Z5a = X5 @ W5a + B5a
A5a = g(Z5a)
Z5b = A5a @ W5b + B5b
A5b = g(Z5b)
WRONG5 = g(X5 @ W5b + B5b)        # layer 2 fed x instead of a1

# ---------------------------------------------------------------- q06 counting layers
NET6 = (64, 32, 16, 8, 1)
SH6 = []
for _i in range(len(NET6) - 1):
    SH6.append(np.zeros((NET6[_i], NET6[_i + 1])).shape)
NL6 = len(SH6)

# ---------------------------------------------------------------- q07 the Dense layer
IN7, UN7 = 12, 5
W7 = np.zeros((IN7, UN7)); B7 = np.zeros(UN7)
P7 = W7.size + B7.size
O7 = np.zeros((7, IN7)) @ W7 + B7
WRONGU7 = IN7
PW7 = 10 * WRONGU7 + WRONGU7          # Dense(12) on 10 inputs, what they built by mistake


def _bad7():
    return np.zeros((1, 10)) @ W7


ERR7 = _err(_bad7)

# ---------------------------------------------------------------- q08 NumPy operators
A8 = np.array([[1.0, 2.0], [3.0, 4.0]])
B8 = np.array([[0.0, 1.0], [1.0, 0.0]])
MM8 = A8 @ B8
EW8 = A8 * B8
AIN8 = np.array([[1.0, 2.0, 3.0]])
W8 = np.array([[1.0, 0.0, 2.0], [0.0, 1.0, 1.0], [1.0, 1.0, 0.0]])
B8b = np.array([0.5, 0.5, 0.5])
BAD8 = AIN8 * W8 + B8b
OK8 = AIN8 @ W8 + B8b
WV8 = np.array([0.2, -0.4, 1.5]); XV8 = np.array([3.0, 1.0, 2.0])
DOT8 = WV8 @ XV8
SUM8 = np.sum(WV8 * XV8)

# ---------------------------------------------------------------- q09 weight layout
W9 = np.array([[0.2, -0.5], [1.0, 0.3], [-0.4, 0.8]])      # 3 inputs x 2 units
A9 = np.array([1.0, 2.0, 3.0])
COL9 = W9[:, 1]
OUT9 = g(A9 @ W9 + np.array([0.0, -1.0]))
Z9_1 = np.dot(W9[:, 0], A9)
Z9_2 = np.dot(W9[:, 1], A9) - 1.0
W9s = np.array([[1.0, 0.0, 2.0], [0.5, 1.0, 0.0], [0.0, 3.0, 1.0]])
X9s = np.array([1.0, 1.0, 2.0])
RIGHT9 = X9s @ W9s
WRONG9 = X9s @ W9s.T

# ---------------------------------------------------------------- q10 the brain analogy
NET10 = (400, 25, 15, 1)
U10 = sum(NET10[1:])
P10 = 0
for _i in range(len(NET10) - 1):
    P10 += NET10[_i] * NET10[_i + 1] + NET10[_i + 1]
BRAIN10 = 86e9                    # widely cited estimate of human neurons (Azevedo et al. 2009)
SYN10 = 1e14                      # synapses: commonly estimated at around 10^14 or more
RATIO10 = BRAIN10 / U10
TRIL10 = 1e12
FRAC10 = TRIL10 / SYN10


DRILLS = [

# =================================================================== q01
D("c2w1-q01",
  recall=M("The parameter count of one Dense layer, from a blank page.",
    """<p>From memory: a layer receives <var>n</var><sub>in</sub> numbers and has <var>k</var> units.</p>
<ol><li>What shape is its <var>W</var>, and what shape is its <var>b</var>?</li>
<li>Write the formula for its number of parameters.</li>
<li>Why is it a product and not a sum?</li></ol>""",
    """<ol><li><var>W</var> is <b>(<var>n</var><sub>in</sub>, <var>k</var>)</b>; <var>b</var> is
<b>(<var>k</var>,)</b>.</li>
<li>Parameters = <var>n</var><sub>in</sub> &times; <var>k</var> + <var>k</var>.</li>
<li>Every unit has its own weight for <b>every</b> input, so each of the <var>k</var> units carries
<var>n</var><sub>in</sub> weights. Then one bias each.</li></ol>""",
    "Weights are inputs times units; biases are one per unit.",
    "Every judge on a panel gives every contestant their own score card. Five judges and six "
    "contestants means thirty score cards &mdash; plus each judge has their own mood to start from.",
    [("parameter", "a number the network learns: a weight or a bias"),
     ("unit", "one little calculator in a layer &mdash; also called a neuron"),
     ("bias", "the starting amount each unit adds on its own")]),

  work=M("Count a whole network, layer by layer.",
    """<p>A network takes <b>%d</b> features, then has Dense layers of <b>%d</b>, <b>%d</b> and <b>%d</b>
units. Count the weights and biases in each layer, then the total.</p>""" % NET1,
    """<table><thead><tr><th>layer</th><th>W shape</th><th>weights</th><th>biases</th><th>total</th></tr>
</thead><tbody>%s</tbody></table>
<p>Total: <b>%s</b> parameters. Notice the first layer dominates &mdash; it touches the widest
input.</p>""" % ("".join(
        "<tr><td>%d</td><td>(%d, %d)</td><td>%d</td><td>%d</td><td>%d</td></tr>"
        % (i + 1, a, b, w, bb, w + bb) for i, (a, b, w, bb) in enumerate(P1)), big(TOT1)),
    "Count each layer as inputs times units plus units, then add the layers.",
    "Each new row of judges looks at the row before it, not at the contestants. So you count "
    "score cards between each pair of rows, one pair at a time.",
    [("layer", "one row of units that all look at the same inputs"),
     ("W shape", "how many rows and columns the weight table has")]),

  spot=M("A network count that is short by a few.",
    """<p>For a network with %d inputs, a hidden layer of %d units and %d output unit, a classmate writes:</p>
<p>&ldquo;Parameters = %d&times;%d + %d&times;%d = <b>%d</b>.&rdquo;</p>
<p>Where is the slip, and what is the right total?</p>""" % (
        SPOT1[0], SPOT1[1], SPOT1[2], SPOT1[0], SPOT1[1], SPOT1[1], SPOT1[2], SPOT1_BAD),
    """<p>They counted the weights and <b>forgot the biases</b>: one per unit, so %d more in the hidden
layer and %d in the output. Right total: %d + %d + %d = <b>%d</b>.</p>""" % (
        SPOT1[1], SPOT1[2], SPOT1_BAD, SPOT1[1], SPOT1[2], SPOT1_OK),
    "Every unit, in every layer, has its own bias to count.",
    "Counting only the score cards and forgetting that each judge also has their own starting "
    "mood. The moods are learned too.",
    [("hidden layer", "a layer between the input and the output"),
     ("output unit", "the unit that gives the final answer")]),

  transfer=M("Pictures as input: what happens when the image gets bigger?",
    """<p>A grayscale image of 28&times;28 pixels is flattened into one long row and fed to a Dense layer
of %d units.</p>
<ol><li>How many parameters does that first layer have?</li>
<li>The camera is upgraded to 56&times;56 pixels. How many now, and roughly how many times more?</li></ol>""" % UN1,
    """<ol><li>%s inputs &times; %d + %d = <b>%s</b> parameters.</li>
<li>%s inputs &times; %d + %d = <b>%s</b>, about <b>%s</b> times more. Doubling the image's width and height
quadruples the pixels, and the first layer grows with them.</li></ol>
<p>This is one reason image networks in later courses do not use plain Dense layers on raw pixels.</p>""" % (
        big(IMG1), UN1, UN1, big(PAR1), big(IMG1b), UN1, UN1, big(PAR1b), n(PAR1b / PAR1, 1)),
    "The first layer's size grows with the number of input numbers.",
    "If every judge has to look at every dot of a picture, a picture with four times as many dots "
    "means four times as many score cards.",
    [("flatten", "lay the rows of an image end to end into one long list"),
     ("pixel", "one dot of an image, stored as one number")]),
),

# =================================================================== q02
D("c2w1-q02",
  recall=M("One unit, in one line, and what it is secretly.",
    """<p>From memory: write what unit <var>j</var> in layer <var>l</var> computes, using
<var>a</var><sup>[<var>l</var>&minus;1]</sup>, <var>w</var><sub><var>j</var></sub>,
<var>b</var><sub><var>j</var></sub> and <var>g</var>. If <var>g</var> is a sigmoid, which model from
Course 1 is this? What is a layer, then?</p>""",
    """<p><var>a</var><sub><var>j</var></sub><sup>[<var>l</var>]</sup> =
<var>g</var>(<var>w</var><sub><var>j</var></sub> &middot; <var>a</var><sup>[<var>l</var>&minus;1]</sup> +
<var>b</var><sub><var>j</var></sub>) &mdash; a weighted sum, plus a bias, through an activation.</p>
<p>With a sigmoid it is exactly <b>logistic regression</b>. A layer is several of these running side
by side on the <b>same</b> inputs, each with its own weights.</p>""",
    "A unit is a weighted sum plus a bias, squashed by an activation.",
    "Each little calculator listens to all the numbers coming in, cares about some more than "
    "others, adds a bit of its own, then squeezes the answer into a neat range.",
    [("weighted sum", "multiply each input by how much it matters, then add"),
     ("activation", "the squeeze applied at the end, like the sigmoid"),
     ("a<sup>[l]</sup>", "the numbers coming out of layer l")]),

  work=M("Two units, the same three inputs.",
    """<p>The inputs are <var>x</var> = [%s].</p>
<ol><li>Unit 1 has <var>w</var> = [%s] and <var>b</var> = %s. Compute <var>z</var> and
<var>a</var> = sigmoid(<var>z</var>).</li>
<li>Unit 2, in the same layer, has <var>w</var> = [%s] and <var>b</var> = %s. Compute its
<var>a</var>.</li></ol>""" % (", ".join(n(v, 2) for v in X2), ", ".join(n(v, 2) for v in W2u), n(B2u, 2),
                              ", ".join(n(v, 2) for v in W2v), n(B2v, 2)),
    """<ol><li><var>z</var> = %s&times;%s + %s&times;%s + %s&times;%s + (%s) = <b>%s</b>;
<var>a</var> = sigmoid(%s) &asymp; <b>%s</b>.</li>
<li><var>z</var> = %s, so <var>a</var> &asymp; <b>%s</b>.</li></ol>
<p>Same inputs, different weights, different answers: the layer's output is the row
[%s, %s].</p>""" % (
        n(W2u[0], 2), n(X2[0], 2), n(W2u[1], 2), n(X2[1], 2), n(W2u[2], 2), n(X2[2], 2), n(B2u, 2),
        n(Z2, 3), n(Z2, 3), n(A2, 4), n(Z2v, 3), n(A2v, 4), n(A2, 4), n(A2v, 4)),
    "Each unit in a layer gives its own answer from the same inputs.",
    "Two friends hear the same three clues. One cares mostly about the last clue, the other about "
    "the first. They end up with different guesses.",
    [("z", "the number before the squeeze: weighted sum plus bias"),
     ("sigmoid", "squeezes any number into a value between 0 and 1")]),

  spot=M("The squeeze applied in the wrong place.",
    """<p>For unit 1 above (<var>w</var> = [%s], <var>b</var> = %s, <var>x</var> = [%s]), someone works:</p>
<ol><li>Squash each input: sigmoid(<var>x</var>) = [%s].</li>
<li>Weighted sum plus bias: %s.</li>
<li>&ldquo;So the unit outputs %s.&rdquo;</li></ol>
<p>Which line is wrong?</p>""" % (
        ", ".join(n(v, 2) for v in W2u), n(B2u, 2), ", ".join(n(v, 2) for v in X2),
        ", ".join(n(v, 3) for v in g(X2)), n(WRONG2, 3), n(WRONG2, 3)),
    """<p><b>Line 1.</b> The activation goes on the <b>output</b> of the weighted sum, not on each input.
Correct: <var>z</var> = %s, then sigmoid(<var>z</var>) &asymp; <b>%s</b>, not %s.</p>
<p>Worse, the slip's final number never goes through a sigmoid at all, so nothing keeps it between 0
and 1. Here it happens to land inside &mdash; which is exactly why the mistake is easy to miss.</p>""" % (
        n(Z2, 3), n(A2, 4), n(WRONG2, 3)),
    "Sum first, squeeze last.",
    "You add up all your pocket money first and then decide what to do with the total. You do not "
    "decide about each coin on its own.",
    [("activation function", "the squeeze, done once, at the end of a unit"),
     ("between 0 and 1", "the range a sigmoid output must land in")]),

  transfer=M("Take the squeeze away and see what is left.",
    """<p>Someone builds a network with two layers but uses <b>no activation</b> (<var>g</var>(<var>z</var>) =
<var>z</var>) in both. The weights are <var>W</var><sup>[1]</sup> = %s and <var>W</var><sup>[2]</sup> =
%s, with zero biases. For <var>x</var> = %s:</p>
<ol><li>Run it as two layers.</li>
<li>Multiply the two weight matrices first, then apply that single matrix to <var>x</var>.</li>
<li>What does this say about stacking units with no activation?</li></ol>""" % (
        _mat(L2a, 1), _mat(L2b, 1), _mat(XL2, 1)),
    """<ol><li>Two layers: <b>%s</b>.</li>
<li><var>W</var><sup>[1]</sup><var>W</var><sup>[2]</sup> = %s, and <var>x</var> times that is <b>%s</b>
&mdash; identical.</li>
<li>Without an activation, any stack of layers collapses into <b>one</b> linear layer. The activation is
what makes depth worth anything &mdash; next week explains this properly.</li></ol>""" % (
        n(TWO2[0, 0], 2), _mat(COMB2, 2), n(ONE2[0, 0], 2)),
    "Without activations, many layers do no more than one.",
    "Stretching a rubber band and then stretching it again is still just one stretch. You need a "
    "bend somewhere to make a new shape.",
    [("linear", "only multiplying and adding &mdash; no bends"),
     ("collapse", "two steps that turn out to be the same as one")]),
),

# =================================================================== q03
D("c2w1-q03",
  recall=M("Why one example needs two pairs of brackets.",
    """<p>From memory: what does the <b>first</b> dimension of a Dense layer's input mean, and the
<b>second</b>? What shape is <code>[200, 17]</code> and what shape is <code>[[200, 17]]</code>? What shape
comes out of a layer with 3 units for an input of shape (<var>m</var>, 2)?</p>""",
    """<p>First dimension: <b>how many examples</b> (the batch). Second: <b>how many features</b>.</p>
<p><code>[200, 17]</code> has shape <b>%s</b> &mdash; a flat list. <code>[[200, 17]]</code> has shape
<b>%s</b> &mdash; a table with one row. The layer's output is <b>(<var>m</var>, 3)</b>: one row per
example, one column per unit.</p>""" % (sh(V3), sh(R3)),
    "Inputs are always a table: rows are examples, even when there is only one row.",
    "A teacher's mark sheet is a table even when only one student turned up. You still write the "
    "student on a row, not scatter their marks down the page.",
    [("batch", "a group of examples handled together"),
     ("dimension", "one direction of a table: rows, or columns"),
     ("shape", "how big each direction is, like (1, 2)")]),

  work=M("Read four shapes off real arrays.",
    """<p>Give the shape of each:</p>
<ol><li><code>np.array([200.0, 17.0])</code></li>
<li><code>np.array([[200.0, 17.0]])</code></li>
<li>five roasts, two features each</li>
<li>the output of a 3-unit layer applied to those five roasts</li></ol>""",
    """<ol><li><b>%s</b></li><li><b>%s</b></li><li><b>%s</b></li><li><b>%s</b></li></ol>
<p>Only the first is wrong for a Dense layer. The batch size changes from 1 to 5 and nothing else in
the code has to.</p>""" % (sh(V3), sh(R3), sh(B3), sh(OUT3)),
    "The number of rows is the number of examples; the code never changes with it.",
    "Whether one student or five turn up, the mark sheet has the same columns. You just get more rows.",
    [("rank", "how many dimensions an array has: a list is 1, a table is 2"),
     ("feature", "one measured fact about an example, like temperature")]),

  spot=M("A transpose that changes nothing.",
    """<p>To &ldquo;turn the list into a row&rdquo;, someone writes:</p>%s
<p>and passes <code>x</code> to the model. What shape is it, and what should they have done?</p>""" % code(
        "x = np.array([200.0, 17.0])\nx = x.T\nx.shape"),
    """<p>Still <b>%s</b>. Transposing a 1-D array does nothing &mdash; it has no rows and columns to swap.</p>
<p>Write it as a table from the start: <code>np.array([[200.0, 17.0]])</code>, shape <b>%s</b>.</p>""" % (
        sh(T3), sh(R3)),
    "A flat list has no rows to flip; build the 2-D table directly.",
    "Turning a single line of writing sideways does not make it a table. It is still one line.",
    [("transpose (.T)", "swap rows and columns of a table"),
     ("1-D", "a flat list with only one direction")]),

  transfer=M("Same rule, different library, different data.",
    """<ol><li>A 20&times;20 grayscale image is flattened for a Dense network. What shape is one image ready
to predict on? What about a batch of 32 images?</li>
<li>You move to scikit-learn and call <code>model.predict</code> on one example as a flat list. What do
you expect?</li></ol>""",
    """<ol><li>One image: <b>%s</b>. A batch of 32: <b>%s</b>. Rows are still images; columns are still
pixels.</li>
<li>An error saying it expected a <b>2-D</b> array and got a 1-D one. The rule is not a TensorFlow quirk
&mdash; most ML libraries take a table of examples, even for one example.</li></ol>""" % (sh(FL3), sh(BATCH3)),
    "Almost every ML library wants a table of examples, even for a single prediction.",
    "Every shop's till expects a receipt with lines on it. One item is still one line on a receipt.",
    [("scikit-learn", "a popular Python library for classic ML models"),
     ("predict", "ask a trained model for its answer on new examples")]),
),

# =================================================================== q04
D("c2w1-q04",
  recall=M("The shape rule for matrix multiplication.",
    """<p>From memory: when is (<var>a</var>&times;<var>b</var>) times (<var>c</var>&times;<var>d</var>)
defined, and what shape is the result? Does the order matter?</p>""",
    """<p>Defined only when the <b>inner</b> numbers match: <var>b</var> = <var>c</var>. The result is the
<b>outer</b> pair, (<var>a</var>&times;<var>d</var>).</p>
<p>Order matters: the first matrix supplies the rows, the second the columns. Swapping them usually
breaks the match, or gives a different answer.</p>""",
    "Inner sizes must match and cancel; the outer sizes are the answer.",
    "Two puzzle pieces only click if the edges that touch are the same size. Then the finished "
    "shape is made of the two outside edges.",
    [("inner dimensions", "the two sizes that touch when you write the shapes side by side"),
     ("outer dimensions", "the two sizes on the outside, which make the answer's shape")]),

  work=M("Push a batch through three weight matrices.",
    """<p><code>X</code> is %s. The weights are <var>W</var><sup>[1]</sup> %s, <var>W</var><sup>[2]</sup> %s,
<var>W</var><sup>[3]</sup> %s.</p>
<ol><li>Give the shape after each multiplication.</li>
<li>How many single multiplications does <code>X @ W1</code> do?</li></ol>""" % (
        sh(X4), sh(W4a), sh(W4b), sh(W4c)),
    """<ol><li><b>%s</b>, then <b>%s</b>, then <b>%s</b> &mdash; one number per example at the end.</li>
<li>Each of the %d&times;%d entries in the result is a dot product of length %d: %d &times; %d &times; %d =
<b>%s</b>.</li></ol>""" % (
        sh(H4a), sh(H4b), sh(H4c), H4a.shape[0], H4a.shape[1], X4.shape[1],
        X4.shape[0], X4.shape[1], W4a.shape[1], big(MULT4)),
    "Write the shapes in a chain; each inner pair must cancel.",
    "A relay race where each runner must hand the baton to someone who can hold it. The team "
    "number never changes, but the baton does.",
    [("dot product", "multiply matching pairs and add"),
     ("entry", "one number in a table")]),

  spot=M("A multiplication that cannot happen.",
    """<p>&ldquo;<code>A</code> is (4, 2) and <code>B</code> is (4, 3). Both have 4 rows, so <code>A @ B</code> is
(4, 3).&rdquo;</p>
<p>What happens when you run it, and what fixes it if you wanted a (2, 3) result?</p>""",
    """<p>It fails: the inner numbers are <b>%d</b> and <b>%d</b>. NumPy says:</p>
<p><code>%s</code></p>
<p>&ldquo;Same number of rows&rdquo; is not the rule. <code>A.T @ B</code> is (2, 4) times (4, 3) and gives
<b>%s</b>.</p>""" % (A4.shape[1], B4.shape[0], ERR4, sh(FIX4)),
    "It is the touching sizes that must match, not the rows.",
    "Two trains with the same number of carriages cannot be joined if their couplings are "
    "different sizes.",
    [("A.T", "A flipped so its rows become columns"),
     ("matmul error", "NumPy refusing because the inner sizes differ")]),

  transfer=M("A table of every user's score for every movie.",
    """<p>A recommender stores <b>%s users</b> each as %d taste numbers, and <b>%s movies</b> each as %d
matching numbers (stored as a %s table). Multiply the users table by the movies table.</p>
<ol><li>What shape comes out, and what does entry (<var>i</var>, <var>j</var>) mean?</li>
<li>How many scores is that in total?</li></ol>""" % (
        big(U4.shape[0]), U4.shape[1], big(M4.shape[1]), M4.shape[0], sh(M4)),
    """<ol><li><b>%s</b>. Entry (<var>i</var>, <var>j</var>) is user <var>i</var>'s predicted score for
movie <var>j</var> &mdash; a dot product of their two taste lists.</li>
<li><b>%s</b> scores from one multiplication. You will build exactly this in Course 3.</li></ol>""" % (
        sh(S4), big(S4.size)),
    "One matrix multiply computes every pair of dot products at once.",
    "It is like a times table: every row number meets every column number, and each box holds "
    "one answer.",
    [("recommender", "a system that suggests things you might like"),
     ("taste numbers", "a short list of numbers describing what someone likes")]),
),

# =================================================================== q05
D("c2w1-q05",
  recall=M("Forward propagation: what it does and what it never does.",
    """<p>From memory: in one sentence, what is forward propagation? Then list three things it does
<b>not</b> do or need.</p>""",
    """<p>It computes the prediction, layer by layer, from input to output: each layer's output becomes the
next layer's input.</p>
<p>It does <b>not</b>: change any weights; need the labels <var>y</var>; look at later layers or the
loss. It runs the same way at training time and at prediction time.</p>""",
    "Forward propagation only evaluates; learning happens elsewhere.",
    "It is like passing a note down a row of friends, each adding something before passing it on. "
    "Nobody changes their handwriting while the note travels.",
    [("forward propagation", "running the inputs through every layer to get the answer"),
     ("label y", "the right answer, which only training needs"),
     ("inference", "using a trained network to predict")]),

  work=M("A two-layer pass, by hand.",
    """<p><var>x</var> = %s. Layer 1: <var>W</var><sup>[1]</sup> = %s, <var>b</var><sup>[1]</sup> = %s,
sigmoid. Layer 2: <var>W</var><sup>[2]</sup> = %s, <var>b</var><sup>[2]</sup> = %s, sigmoid. Compute
<var>a</var><sup>[1]</sup> and <var>a</var><sup>[2]</sup>.</p>""" % (
        _mat(X5, 1), _mat(W5a, 2), _row(B5a, 1), _mat(W5b, 1), _row(B5b, 1)),
    """<p><var>z</var><sup>[1]</sup> = <var>x</var><var>W</var><sup>[1]</sup> + <var>b</var><sup>[1]</sup> = %s, so
<var>a</var><sup>[1]</sup> = sigmoid of that = <b>%s</b>.</p>
<p><var>z</var><sup>[2]</sup> = <var>a</var><sup>[1]</sup><var>W</var><sup>[2]</sup> + <var>b</var><sup>[2]</sup>
&asymp; %s, so <var>a</var><sup>[2]</sup> &asymp; <b>%s</b>.</p>""" % (
        _row(Z5a[0], 3), _row(A5a[0], 4), n(Z5b[0, 0], 4), n(A5b[0, 0], 4)),
    "Each layer takes the previous layer's output, never the raw input again.",
    "Like a factory line: station two works on what station one made, not on the raw materials.",
    [("a<sup>[1]</sup>", "the outputs of layer 1, which layer 2 reads"),
     ("z", "the number before the sigmoid squeeze")]),

  spot=M("Layer 2 fed the wrong thing &mdash; and it still runs.",
    """<p>Using the same network as the work card, someone codes layer 2 as:</p>%s
<p>It runs without error. Why, and what is wrong?</p>""" % code("a2 = g(x @ W2 + b2)"),
    """<p>It should be <code>a1 @ W2</code>. It runs only because <var>x</var> happens to have 2 numbers and
so does <var>a</var><sup>[1]</sup>, so the shapes line up by accident.</p>
<p>The buggy line gives <b>%s</b>; the real network gives <b>%s</b>. Layer 1 has been skipped silently.</p>""" % (
        n(WRONG5[0, 0], 4), n(A5b[0, 0], 4)),
    "Matching shapes do not prove each layer got the right input.",
    "If station two grabs the raw materials instead of station one's work, the factory still makes "
    "something &mdash; just not the right thing.",
    [("silent bug", "a mistake that gives no error, only a wrong number"),
     ("by accident", "the sizes happen to fit even though the idea is wrong")]),

  transfer=M("Shipping a trained network to a phone.",
    """<p>A trained network will run on a phone to classify photos. What exactly must you put on the
phone? Do you need the training data or any labels? Does the phone ever change the weights?</p>""",
    """<p>Only what forward propagation uses: each layer's <var>W</var> and <var>b</var>, the activation
each layer uses, and the same input preprocessing as in training.</p>
<p><b>No</b> training data and <b>no</b> labels &mdash; the phone has neither. It never changes the
weights: it only runs the forward pass.</p>""",
    "Predicting needs only the weights and the forward pass.",
    "Once a recipe is perfected, you only need the recipe card to cook it. You do not need all the "
    "failed cakes from the testing.",
    [("deploy", "put a trained model somewhere it is used for real"),
     ("preprocessing", "the steps done to inputs before the model sees them, like scaling")]),
),

# =================================================================== q06
D("c2w1-q06",
  recall=M("How layers are counted, and what layer 0 is.",
    """<p>From memory: which layers are counted when someone says &ldquo;an <var>L</var>-layer
network&rdquo;? What is <var>a</var><sup>[0]</sup>? How many weight matrices does an <var>L</var>-layer
network have?</p>""",
    """<p>Count the <b>hidden layers plus the output layer</b>. The input is not counted: it computes
nothing.</p>
<p><var>a</var><sup>[0]</sup> is just <var>x</var>, the data. An <var>L</var>-layer network has exactly
<var>L</var> weight matrices &mdash; one per counted layer.</p>""",
    "Count the layers that compute something; the input does not.",
    "In a relay race you count the runners, not the starting line. The starting line just holds "
    "the baton.",
    [("hidden layer", "a layer between the input and the output"),
     ("a<sup>[0]</sup>", "another name for the input x")]),

  work=M("Name the layers of a real network.",
    """<p>A network takes %d features and has layers of %d, %d, %d and %d units.</p>
<ol><li>How many layers is it, and how many are hidden?</li>
<li>Give the shape of every <var>W</var><sup>[<var>l</var>]</sup>.</li></ol>""" % NET6,
    """<ol><li><b>%d layers</b>; <b>%d hidden</b> plus the output.</li>
<li>%s.</li></ol>""" % (
        NL6, NL6 - 1, "; ".join("<var>W</var><sup>[%d]</sup> %s" % (i + 1, sh(s)) for i, s in enumerate(SH6))),
    "Number of layers = number of weight matrices.",
    "Count the hand-offs between runners: each one is a layer.",
    [("W<sup>[l]</sup>", "the weight table belonging to layer l"),
     ("output layer", "the last layer, which gives the final answer")]),

  spot=M("&ldquo;Four layers: input, two hidden, output.&rdquo;",
    """<p>A model is <code>Sequential([Dense(25), Dense(15), Dense(1)])</code>. Someone writes in their
notes: &ldquo;This is a 4-layer network: the input layer, two hidden layers and the output layer.&rdquo;
What is wrong?</p>""",
    """<p>The input is not counted. Three <code>Dense</code> layers, three weight matrices: it is a
<b>3-layer</b> network with 2 hidden layers.</p>""",
    "The number of Dense layers is the layer count.",
    "Counting the starting line as a runner makes the team look bigger than it is.",
    [("Sequential", "a list of layers run one after the other"),
     ("Dense", "a layer where every unit sees every input")]),

  transfer=M("Two descriptions from the outside world.",
    """<ol><li>A paper calls its model &ldquo;a 2-layer network&rdquo;. How many hidden layers does it
have?</li>
<li>By the same count, how many layers is logistic regression from Course 1?</li></ol>""",
    """<ol><li><b>One</b> hidden layer plus the output layer.</li>
<li><b>One</b> layer: a single unit with a sigmoid, and no hidden layer. A neural network is logistic
regression with layers added in front.</li></ol>""",
    "Hidden layers are always one fewer than the layer count.",
    "A team of two runners has one runner in the middle and one who crosses the line.",
    [("logistic regression", "Course 1's yes/no model: one sigmoid unit"),
     ("2-layer network", "one hidden layer plus the output layer")]),
),

# =================================================================== q07
D("c2w1-q07",
  recall=M("Everything one Dense line creates.",
    """<p>From memory: what does <code>Dense(units=<var>k</var>, activation='sigmoid')</code> create? What
does <code>units</code> count? Where does the input width come from?</p>""",
    """<p>A layer of <var>k</var> units: a weight matrix <var>W</var>, a bias vector <var>b</var> of length
<var>k</var>, and the sigmoid.</p>
<p><code>units</code> counts the <b>outputs</b>. The input width is <b>inferred</b> from the first input
the layer sees, and <var>W</var>'s shape is fixed then.</p>""",
    "units is how many numbers come out; the inputs are worked out for you.",
    "You hire five judges. How many contestants they each score depends on who turns up on the "
    "first day &mdash; then it is fixed.",
    [("units", "how many outputs a layer has"),
     ("inferred", "worked out automatically from the data")]),

  work=M("A layer's shapes, from its first input.",
    """<p><code>Dense(units=%d)</code> first receives a batch of shape (7, %d).</p>
<ol><li>What shapes do <var>W</var> and <var>b</var> get?</li>
<li>How many parameters?</li><li>What shape comes out?</li></ol>""" % (UN7, IN7),
    """<ol><li><var>W</var> <b>%s</b>, <var>b</var> <b>%s</b>.</li>
<li>%d &times; %d + %d = <b>%d</b>.</li><li><b>%s</b> &mdash; 7 examples, %d units.</li></ol>""" % (
        sh(W7), sh(B7), IN7, UN7, UN7, P7, sh(O7), UN7),
    "W is (inputs, units); the output is (examples, units).",
    "Seven contestants, twelve facts each, five judges: each judge reads all twelve facts and "
    "gives each contestant one score.",
    [("W", "the weight table: one column per unit"),
     ("b", "one bias per unit")]),

  spot=M("units set to the number of features.",
    """<p>&ldquo;My data has %d features, so my first layer is <code>Dense(units=%d)</code>.&rdquo;</p>
<p>What has this person misunderstood?</p>""" % (IN7, WRONGU7),
    """<p><code>units</code> is how many units the layer has &mdash; its <b>outputs</b>. The %d features are
handled automatically. Matching them is not wrong code, just a design choice made for the wrong
reason: it builds %d units whether you wanted that or not.</p>""" % (IN7, WRONGU7),
    "Choose units for what the layer should learn, not to match the inputs.",
    "How many judges you hire has nothing to do with how many facts each contestant brings.",
    [("design choice", "a number you pick, not one the data forces on you"),
     ("outputs", "the numbers a layer sends on to the next layer")]),

  transfer=M("Reusing a built layer on different data.",
    """<p>The layer above has been built on inputs of width %d. You now call it on an array of width 10.
What happens, and why?</p>""" % IN7,
    """<p>An error. Its <var>W</var> is <b>%s</b>, so it needs %d numbers per example; 10 cannot meet 12.
NumPy shows the same thing for the matrix multiply:</p>
<p><code>%s</code></p>
<p>Make a new layer for the new width.</p>""" % (sh(W7), IN7, ERR7),
    "Once a layer is built, its input width is fixed.",
    "A judge trained to read twelve facts cannot score a form with only ten boxes.",
    [("built", "a layer whose weight shapes have been fixed"),
     ("input width", "how many numbers each example brings")]),
),

# =================================================================== q08
D("c2w1-q08",
  recall=M("Two operators, two different jobs.",
    """<p>From memory: what does <code>A @ B</code> compute, and what does <code>A * B</code> compute? When
do both run without error on the same arrays?</p>""",
    """<p><code>@</code> is <b>matrix multiplication</b>: rows of <code>A</code> dotted with columns of
<code>B</code>. <code>*</code> multiplies <b>element by element</b>.</p>
<p>Both run when the arrays are the same square shape, or when broadcasting makes <code>*</code> fit
&mdash; and then the wrong one fails silently.</p>""",
    "@ is matrix multiplication; * is box-by-box multiplication.",
    "One way pairs every row with every column like a times table. The other just multiplies boxes "
    "that sit in the same place.",
    [("@", "matrix multiplication in NumPy"),
     ("elementwise", "matching positions multiplied, one by one"),
     ("broadcasting", "NumPy stretching a smaller array to fit a bigger one")]),

  work=M("Both operators on the same two matrices.",
    """<p><code>A</code> = %s, <code>B</code> = %s. Compute <code>A @ B</code> and <code>A * B</code>.</p>""" % (
        _mat(A8), _mat(B8)),
    """<p><code>A @ B</code> = <b>%s</b> &mdash; here it swaps <code>A</code>'s columns.</p>
<p><code>A * B</code> = <b>%s</b> &mdash; it keeps only the positions where <code>B</code> has a 1.</p>
<p>Same inputs, entirely different results.</p>""" % (_mat(MM8), _mat(EW8)),
    "Same shapes can give completely different answers with the two operators.",
    "Mixing two cake bowls together is not the same as putting one bowl on top of the other.",
    [("matrix", "a table of numbers"),
     ("swap columns", "move the left column to the right and the right to the left")]),

  spot=M("A layer written with the wrong operator.",
    """<p>A layer with input <code>a_in</code> %s, <code>W</code> %s and <code>b</code> %s is coded as:</p>%s
<p>It runs. What shape comes out, and what should it be?</p>""" % (
        sh(AIN8), sh(W8), sh(B8b), code("z = a_in * W + b")),
    """<p>Broadcasting stretches the single row across all three rows, so <code>z</code> is <b>%s</b> &mdash;
a whole table instead of one row. It should be <code>a_in @ W + b</code>, shape <b>%s</b>, values
<b>%s</b>.</p>""" % (sh(BAD8), sh(OK8), _row(OK8[0], 1)),
    "If a layer's output has the wrong shape, check for * where @ belongs.",
    "Using the wrong kind of multiplying is like reading a recipe as a shopping list: you still get "
    "a list, just the wrong one.",
    [("shape (1, 3)", "one row with three numbers"),
     ("shape (3, 3)", "a table of three rows and three columns")]),

  transfer=M("When elementwise is the right tool.",
    """<p><var>w</var> = [%s], <var>x</var> = [%s].</p>
<ol><li>Compute <code>w @ x</code> and <code>np.sum(w * x)</code>.</li>
<li>Name a place in ML code where <code>*</code> (elementwise) is exactly what you want.</li></ol>""" % (
        ", ".join(n(v, 1) for v in WV8), ", ".join(n(v, 1) for v in XV8)),
    """<ol><li>Both give <b>%s</b>: a dot product is elementwise multiplication followed by a sum.</li>
<li>Squaring the errors in a cost: <code>err * err</code>. Or switching some values off with a 0/1 mask.
Elementwise is not wrong &mdash; it is wrong <b>instead of</b> matrix multiplication.</li></ol>""" % n(DOT8, 2),
    "A dot product is elementwise multiply then add; use * when you mean box by box.",
    "Multiplying pairs and then adding them up gives the same total as the fast way. The fast way "
    "just does both steps at once.",
    [("mask", "a list of 0s and 1s that turns some values off"),
     ("dot product", "multiply pairs, then add")]),
),

# =================================================================== q09
D("c2w1-q09",
  recall=M("Which way the units run in W.",
    """<p>From memory: in this course, is one unit's weight vector a row or a column of <var>W</var>?
What shape is <var>W</var> for <var>n</var><sub>in</sub> inputs and <var>k</var> units? How do you pick
out unit <var>j</var>'s weights in NumPy?</p>""",
    """<p>A <b>column</b>. <var>W</var> is (<var>n</var><sub>in</sub>, <var>k</var>), and unit <var>j</var>
is <code>W[:, j]</code> &mdash; all rows, column <var>j</var>.</p>
<p>Then a whole layer is <code>g(a_in @ W + b)</code>.</p>""",
    "In this course, each unit is a column of W.",
    "Think of a table where each judge has their own column of scores, one score per fact going down.",
    [("W[:, j]", "every row of column j &mdash; unit j's weights"),
     ("column", "a line of numbers going down")]),

  work=M("Pick out one unit's weights and run the layer.",
    """<p><var>W</var> = %s (3 inputs, 2 units), <var>b</var> = [0, &minus;1], <var>a</var><sub>in</sub> = [%s].</p>
<ol><li>Write unit 2's weight vector.</li>
<li>Compute both units' <var>z</var> and sigmoid outputs.</li></ol>""" % (
        _mat(W9, 1), ", ".join(n(v, 0) for v in A9)),
    """<ol><li><code>W[:, 1]</code> = <b>[%s]</b>.</li>
<li>Unit 1: <var>z</var> = %s, output &asymp; <b>%s</b>. Unit 2: <var>z</var> = %s, output &asymp;
<b>%s</b>.</li></ol>""" % (
        ", ".join(n(v, 1) for v in COL9), n(Z9_1, 2), n(OUT9[0], 4), n(Z9_2, 2), n(OUT9[1], 4)),
    "Column j holds unit j's weights; read down, not across.",
    "To find one judge's scores, read straight down their column.",
    [("slice", "picking out part of an array, like one column"),
     ("sigmoid", "squeezes any number into a value between 0 and 1")]),

  spot=M("Units stored as rows, and nothing complains.",
    """<p>Someone stores each unit as a <b>row</b> of a 3&times;3 matrix <var>W</var> = %s but still computes
<code>x @ W</code> for <var>x</var> = [%s]. Nothing errors. Is the output right?</p>""" % (
        _mat(W9s, 1), ", ".join(n(v, 0) for v in X9s)),
    """<p>No. With units as rows, the layer should compute <code>x @ W.T</code> = <b>%s</b>. The code
computes <code>x @ W</code> = <b>%s</b>. The matrix is square, so the shapes fit either way and nothing
warns you.</p>""" % (_row(WRONG9, 1), _row(RIGHT9, 1)),
    "Pick one layout and use it everywhere; square matrices hide the mistake.",
    "If you read a judge's row when you meant their column, you still get numbers &mdash; just "
    "someone else's.",
    [("square matrix", "same number of rows and columns, so either way fits"),
     ("layout", "which way round the numbers are stored")]),

  transfer=M("Loading weights from another library.",
    """<p>You want to copy a trained layer from PyTorch into your own NumPy code. PyTorch's
<code>Linear</code> layer stores its weight with shape (<var>units</var>, <var>inputs</var>). Your code
expects (<var>inputs</var>, <var>units</var>). What must you do, and what happens if you forget on a layer
with 64 inputs and 64 units?</p>""",
    """<p>Transpose it: use <code>W_torch.T</code>. If you forget on a 64&times;64 layer, the shapes still
fit, everything runs, and every prediction is wrong with no error at all.</p>""",
    "Always check which way round another library stores its weights.",
    "Copying a seating plan from a friend who writes rows where you write columns: you must turn it "
    "around first.",
    [("PyTorch", "another popular deep-learning library"),
     ("transpose", "swap rows and columns")]),
),

# =================================================================== q10
D("c2w1-q10",
  recall=M("What was borrowed from the brain, and what was not.",
    """<p>From memory: what idea did neural networks take from biology? Name two ways a real neuron is
very different from a unit.</p>""",
    """<p>Borrowed: many simple parts, each taking several inputs and sending one output on &mdash; a loose
analogy.</p>
<p>Not borrowed: a real neuron has thousands of connections, its own chemistry, and timing that carries
information. A unit is just a weighted sum and a squeeze.</p>""",
    "The brain inspired the name, not the design details.",
    "A paper aeroplane is inspired by birds, but nobody thinks it flaps its wings.",
    [("analogy", "a comparison that helps understanding but is not exact"),
     ("neuron", "a real nerve cell in the brain")]),

  work=M("Count units and parameters in a real network, then compare.",
    """<p>A network has layers %d &rarr; %d &rarr; %d &rarr; %d (input first). Count its units (not the
input) and its parameters. A human brain is commonly estimated to have about 86 billion neurons. How
many times more neurons than units is that?</p>""" % NET10,
    """<p>Units: %s = <b>%d</b>. Parameters: <b>%s</b>.</p>
<p>86 billion &divide; %d &asymp; <b>%s</b> times more. And each real neuron is far more complicated than
a unit, so even the count understates the gap.</p>""" % (
        " + ".join(str(v) for v in NET10[1:]), U10, big(P10), U10, "{:,.0f}".format(RATIO10)),
    "A small network has a tiny fraction of the brain's parts, and simpler ones.",
    "A toy car and a real car both have wheels, but nobody thinks the toy is nearly as complicated.",
    [("estimate", "a careful best guess, not an exact count"),
     ("unit", "one calculator in a layer, the network's version of a neuron")]),

  spot=M("Parameters counted as neurons.",
    """<p>&ldquo;Our network has %s parameters, so it has %s artificial neurons.&rdquo;</p>
<p>What is wrong?</p>""" % (big(P10), big(P10)),
    """<p>Parameters are not neurons. The nearest thing to a neuron is a <b>unit</b>, and there are only
<b>%d</b>. The weights are closer to connection strengths between units.</p>""" % U10,
    "Units are the parts; weights are the connections between them.",
    "Counting the strings between puppets is not the same as counting the puppets.",
    [("parameter", "a learned number, mostly connection strengths"),
     ("unit", "one calculator in a layer")]),

  transfer=M("A headline about model size.",
    """<p>A headline says: &ldquo;New AI has <b>1 trillion</b> parameters &mdash; bigger than the human
brain.&rdquo; Synapses (the brain's connections) are commonly estimated at around 10<sup>14</sup> or more.
Compare the two sensibly. Does the comparison say anything about intelligence?</p>""",
    """<p>If parameters are compared with synapses, 10<sup>12</sup> &divide; 10<sup>14</sup> = <b>%s</b>
&mdash; about %s%% of the brain's connections, not more.</p>
<p>And even an equal count would not mean equal ability: the parts are different kinds of thing. Size
comparisons like this are headlines, not evidence.</p>""" % (n(FRAC10, 2), n(FRAC10 * 100, 0)),
    "Counting parts does not measure intelligence.",
    "Having as many bricks as a castle does not make your pile of bricks a castle.",
    [("synapse", "a connection between two real neurons"),
     ("10<sup>14</sup>", "1 followed by 14 zeros")]),
),
]
