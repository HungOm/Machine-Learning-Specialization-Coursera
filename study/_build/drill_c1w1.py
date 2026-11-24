# -*- coding: utf-8 -*-
"""Quiz drills — C1 W1. One concept per mock-quiz question, four methods each.

Every number below is COMPUTED here at import time and formatted into the text,
never typed. The examples are new: none repeats the quiz question or the
lesson's own worked example (the 1,000 / 2,000 sq ft houses).
"""
import numpy as np
from drillkit import D, M
from masterykit import code


def n(x, d=2):
    """Format a number for prose: d decimals, trailing zeros trimmed."""
    s = ("%." + str(d) + "f") % x
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    if s in ("-0", "-0.0"):
        s = "0"
    return "&minus;" + s[1:] if s.startswith("-") else s


def _row(vals, d=3):
    return "[" + ", ".join(n(v, d) for v in vals) + "]"


def _cost(w, b, x, y):
    return np.sum((w * x + b - y) ** 2) / (2 * len(x))


# ---------------------------------------------------------------- q02 the model
W2, B2 = 180.0, 60.0                      # $1000s per 1000 sq ft, $1000s
X2 = np.array([0.8, 1.5, 2.4])            # 1000 sq ft
F2 = W2 * X2 + B2
SPOT2_BAD = (W2 + B2) * 1.5
SPOT2_OK = W2 * 1.5 + B2
# taxi: recover w and b from two observed fares
TX = np.array([4.0, 9.0]); TY = 1.8 * TX + 3.5
TW, TB = np.linalg.solve(np.column_stack([TX, np.ones(2)]), TY)
T12 = TW * 12 + TB

# ---------------------------------------------------------------- q03 cost
X3 = np.array([1.0, 2.0, 3.0]); Y3 = np.array([2.0, 4.0, 5.0])
WA, BA = 1.5, 0.5
WB, BB = 2.0, 0.0
FA, FB = WA * X3 + BA, WB * X3 + BB
JA, JB = _cost(WA, BA, X3, Y3), _cost(WB, BB, X3, Y3)
# the missing-square bug: errors cancel
YS3 = np.array([3.0, 5.0]); FS3 = np.array([4.0, 4.0])
ES3 = FS3 - YS3
BUG3 = np.sum(ES3) / (2 * 2)
OK3 = np.sum(ES3 ** 2) / (2 * 2)
# one miss of 10 against ten misses of 1
BIG3 = 10.0 ** 2
SMALL3 = 10 * 1.0 ** 2

# ---------------------------------------------------------------- q04 sign of the step
W4, A4 = 2.0, 0.1
G4 = np.array([-4.0, 3.0, 0.0])
NEW4 = W4 - A4 * G4
SPOT4_BAD = W4 - A4 * 4.0
# J(w) = (w - 3)^2, alpha = 0.25
A4b = 0.25
L4, R4 = 1.0, 5.0
GL4, GR4 = 2 * (L4 - 3), 2 * (R4 - 3)
NL4, NR4 = L4 - A4b * GL4, R4 - A4b * GR4


# ---------------------------------------------------------------- q05 learning rate
def _run5(a, k=4):
    w, js = 0.0, []
    for _ in range(k):
        w = w - a * 4 * (w - 1)
        js.append(2 * (w - 1) ** 2)
    return js


J5_SMALL = _run5(0.1)
J5_BIG = _run5(0.6)
J5_START = 2 * (0.0 - 1) ** 2
_w = 0.0
STEPS5 = 0
while abs(_w - 1) <= 1e6:
    _w = _w - 0.6 * 4 * (_w - 1)
    STEPS5 += 1
FACTOR5 = abs(1 - 0.6 * 4)

# ---------------------------------------------------------------- q06 contours
P6 = np.array([[5.0, 1.0], [2.0, 4.0], [-1.0, 1.0]])
J6 = (P6[:, 0] - 2) ** 2 + (P6[:, 1] - 1) ** 2
F6 = P6[:, 0] * 1.0 + P6[:, 1]           # prediction at x = 1
E6 = np.array([[5.0, 1.0], [2.0, 2.0]])
JE6 = (E6[:, 0] - 2) ** 2 + 9 * (E6[:, 1] - 1) ** 2
DE6 = np.sqrt((E6[:, 0] - 2) ** 2 + (E6[:, 1] - 1) ** 2)

# ---------------------------------------------------------------- q08 simultaneous update
X8 = np.array([1.0, 2.0, 3.0]); Y8 = 2 * X8 + 1
A8 = 0.1
E8 = 0 * X8 + 0 - Y8
DW8, DB8 = np.mean(E8 * X8), np.mean(E8)
W8_OK, B8_OK = 0 - A8 * DW8, 0 - A8 * DB8
E8b = W8_OK * X8 + 0 - Y8                 # recomputed with the NEW w
DB8_BAD = np.mean(E8b)
B8_BAD = 0 - A8 * DB8_BAD


# ---------------------------------------------------------------- q09 convergence
def _gd(x, y, a, iters):
    w = b = 0.0
    js = []
    for _ in range(iters):
        e = w * x + b - y
        w, b = w - a * np.mean(e * x), b - a * np.mean(e)
        js.append(_cost(w, b, x, y))
    return w, b, np.array(js)


_rng = np.random.default_rng(1)
X9 = _rng.uniform(0, 1, 30)
Y9 = 0.4 * X9 + 3.0 + _rng.normal(0, 1.2, 30)
_, _, JS9 = _gd(X9, Y9, 0.5, 400)
J9_MODEL = JS9[-1]
J9_BASE = _cost(0.0, np.mean(Y9), X9, Y9)


def _first_below(js, eps):
    d = np.abs(np.diff(js))
    hit = np.nonzero(d < eps)[0]
    return hit[0] + 2 if len(hit) else None


XU = np.array([1.1, 1.6, 2.0, 2.7, 3.1]); YU = 150 * XU + 80   # price in $1000s
_, _, JK = _gd(XU, YU, 0.1, 3000)
_, _, JD = _gd(XU, YU * 1000, 0.1, 3000)                      # same, in dollars
STOP_K = _first_below(JK, 1e-3)
STOP_D = _first_below(JD, 1e-3)

# ---------------------------------------------------------------- q10 parameters
W10, B10 = 0.18, 25.0                     # $1000s per sq ft, $1000s
EXTRA10 = W10 * 150
P10 = W10 * 1400 + B10
DOLLARS10 = W10 * 1000
WS, BS = 4.5, 38.0                        # exam points per hour, points
S6 = WS * 6 + BS
WS_MIN = WS / 60


DRILLS = [

# =================================================================== q01
D("c1w1-q01",
  recall=M("Two questions, in order, from a blank page.",
    """<p>Without looking, write the two questions you ask to place any problem in the map of machine
learning, in the order you ask them. Then write one sentence each defining <b>regression</b> and
<b>classification</b>.</p>""",
    """<ol><li><b>Does the training data contain the answer?</b> Yes &rarr; supervised. No &rarr;
unsupervised.</li>
<li><b>If supervised, is the answer a number or a category?</b> A number on a scale &rarr; regression.
One of a small set of categories &rarr; classification.</li></ol>
<p>Regression predicts a quantity (price, days, temperature). Classification predicts a label from a
fixed list (spam / not spam, which digit).</p>""",
    "First ask whether the answers are in the data, then ask whether the answer is a number or a category.",
    "If someone shows you lots of examples with the answers written on the back, you are learning with a "
    "teacher. Then ask: is the answer &ldquo;how much&rdquo; or &ldquo;which one&rdquo;?",
    [("label", "the right answer stored next to each example"),
     ("supervised", "learning from examples that come with their answers"),
     ("regression", "predicting a number, like a price"),
     ("classification", "predicting a category, like spam or not spam")]),

  work=M("Sort six problems into four boxes.",
    """<p>Put each problem in one box: <b>supervised regression</b>, <b>supervised classification</b>,
<b>unsupervised</b>, or <b>not enough information</b>.</p>
<ol><li>Predict a parcel's delivery time in hours, from 20,000 past deliveries with their actual times.</li>
<li>Decide whether an X-ray shows a fracture, from 5,000 X-rays marked by doctors.</li>
<li>Find groups of shoppers who buy similar things; nobody has defined the groups.</li>
<li>Predict tomorrow's electricity demand in megawatts from five years of hourly demand.</li>
<li>Predict which of 12 product categories a new listing belongs to, from 80,000 categorised listings.</li>
<li>Flag credit-card payments that look unlike a customer's normal pattern; almost none are labelled
as fraud.</li></ol>""",
    """<ol><li>Supervised <b>regression</b> &mdash; past times are labels; hours is a quantity.</li>
<li>Supervised <b>classification</b> &mdash; marked by doctors; fracture yes/no.</li>
<li><b>Unsupervised</b> (clustering) &mdash; no labels, the groups are discovered.</li>
<li>Supervised <b>regression</b> &mdash; each past hour comes with the demand that followed.</li>
<li>Supervised <b>classification</b> &mdash; 12 categories is a fixed list, however many there are.</li>
<li><b>Unsupervised</b> (anomaly detection) &mdash; with almost no fraud labels, you model what normal
looks like and flag what does not fit.</li></ol>""",
    "Labels decide supervised or not; the type of answer decides regression or classification.",
    "Ask two things: did someone write the answers down, and is the answer a number or a name?",
    [("clustering", "finding groups in data nobody has labelled"),
     ("anomaly detection", "spotting things that look unusual compared with normal")]),

  spot=M("A loan team calls their problem regression. Find the slip.",
    """<p>&ldquo;We have 50,000 past loan applications, each marked <code>1</code> if it was repaid and
<code>0</code> if it defaulted. The output is a number &mdash; 0 or 1 &mdash; so this is
<b>regression</b>.&rdquo;</p>
<p>Which part of the reasoning is wrong?</p>""",
    """<p>The first half is right: the marks are labels, so this is supervised. The slip is
<b>&ldquo;the output is a number&rdquo;</b>. 0 and 1 are <b>codes for two categories</b> (repaid,
defaulted), not quantities on a scale &mdash; there is no meaningful 0.5 loan. That makes it
<b>classification</b>.</p>""",
    "Numbers used as codes for categories are still categories.",
    "If you call the red team &ldquo;team 1&rdquo; and the blue team &ldquo;team 2&rdquo;, you have not "
    "turned colours into amounts. They are still just two teams.",
    [("code", "a number that stands for a name, not an amount"),
     ("default", "when a loan is not paid back")]),

  transfer=M("One hospital dataset, three different questions.",
    """<p>A hospital has records for thousands of past patients, including how long each stayed and
whether they came back within 30 days. Name the kind of problem for each question:</p>
<ol><li>How many days will this new patient stay?</li>
<li>Will this patient be readmitted within 30 days?</li>
<li>Are there natural groups of patients with similar records that nobody has named yet?</li></ol>""",
    """<ol><li>Supervised <b>regression</b> &mdash; past stays are labels, days is a quantity.</li>
<li>Supervised <b>classification</b> &mdash; past readmissions are labels, the answer is yes/no.</li>
<li><b>Unsupervised</b> clustering &mdash; the groups are not in the data; you are discovering them.</li></ol>
<p>The data did not decide the problem type. <b>The question did.</b></p>""",
    "The same data can be supervised or unsupervised, depending on what you ask of it.",
    "A box of photos can be used to guess someone's age, to sort happy from sad faces, or just to put "
    "similar photos in piles. Same photos, different game.",
    [("readmitted", "came back into hospital"),
     ("problem type", "the kind of question you are asking the data")]),
),

# =================================================================== q02
D("c1w1-q02",
  recall=M("Write the model and name every part.",
    """<p>From memory, write the linear regression model for one feature. Name what each of
<var>f</var>, <var>x</var>, <var>w</var> and <var>b</var> is, and say which two the algorithm learns.</p>""",
    """<p><var>f</var>(<var>x</var>) = <var>w</var><var>x</var> + <var>b</var>.</p>
<ul><li><var>x</var> &mdash; the input (the feature).</li>
<li><var>f</var>(<var>x</var>) &mdash; the prediction, also written <var>&#375;</var>.</li>
<li><var>w</var> &mdash; the weight: how steeply the prediction rises per unit of <var>x</var>.</li>
<li><var>b</var> &mdash; the bias: where the line sits when <var>x</var> = 0.</li></ul>
<p>The algorithm learns <b><var>w</var> and <var>b</var></b>. <var>x</var> is given.</p>""",
    "A prediction is the input times a weight, plus a starting amount.",
    "Start with a fixed amount, then add the same extra bit for every unit of the thing you measured. "
    "That total is the guess.",
    [("weight w", "how much the guess goes up for each extra unit of x"),
     ("bias b", "the starting amount before x adds anything"),
     ("prediction", "the model's guess, f(x)")]),

  work=M("Three predictions from one line.",
    """<p>A model has <var>w</var> = %s and <var>b</var> = %s, with <var>x</var> in 1000s of sq ft and the
price in $1000s. Predict the price of houses of %s, %s and %s thousand sq ft.</p>""" % (
        n(W2, 0), n(B2, 0), n(X2[0], 1), n(X2[1], 1), n(X2[2], 1)),
    """<ul><li>%s &times; %s + %s = <b>%s</b> &rarr; $%sk</li>
<li>%s &times; %s + %s = <b>%s</b> &rarr; $%sk</li>
<li>%s &times; %s + %s = <b>%s</b> &rarr; $%sk</li></ul>
<p>Multiply first, then add. Notice the gaps: each extra 0.1 thousand sq ft adds the same %s.</p>""" % (
        n(W2, 0), n(X2[0], 1), n(B2, 0), n(F2[0], 0), n(F2[0], 0),
        n(W2, 0), n(X2[1], 1), n(B2, 0), n(F2[1], 0), n(F2[1], 0),
        n(W2, 0), n(X2[2], 1), n(B2, 0), n(F2[2], 0), n(F2[2], 0), n(W2 * 0.1, 0)),
    "Multiply x by w, then add b.",
    "If every room costs the same and there is a fixed fee too, you count the rooms, multiply, then "
    "add the fee at the end.",
    [("multiply first", "do the times before the plus"),
     ("$1000s", "the price column is in thousands, so 330 means $330,000")]),

  spot=M("One line of working, in the wrong order.",
    """<p>With <var>w</var> = %s and <var>b</var> = %s, someone predicts for <var>x</var> = 1.5:</p>
<p><var>f</var>(1.5) = (%s + %s) &times; 1.5 = %s</p>
<p>Where is the error, and what is the right answer?</p>""" % (
        n(W2, 0), n(B2, 0), n(W2, 0), n(B2, 0), n(SPOT2_BAD, 0)),
    """<p>They added <var>b</var> to <var>w</var> before multiplying, so <var>b</var> got scaled by
<var>x</var> too. <var>b</var> is added <b>last</b>: %s &times; 1.5 + %s = <b>%s</b>.</p>
<p>The bias shifts the whole line up; it never grows with <var>x</var>.</p>""" % (
        n(W2, 0), n(B2, 0), n(SPOT2_OK, 0)),
    "The bias is added once, at the end; only w multiplies x.",
    "A delivery fee is paid once. It does not get bigger because you ordered more pizzas.",
    [("bias", "the fixed amount added at the end"),
     ("scaled", "multiplied, made bigger or smaller")]),

  transfer=M("A taxi meter is a linear model. Recover its w and b.",
    """<p>Two taxi rides in the same city cost $%s for %s km and $%s for %s km. Assume
fare = <var>w</var> &times; km + <var>b</var>.</p>
<ol><li>Find <var>w</var> and <var>b</var>. What does each mean on the meter?</li>
<li>What will a %s km ride cost?</li></ol>""" % (
        n(TY[0], 2), n(TX[0], 0), n(TY[1], 2), n(TX[1], 0), "12"),
    """<ol><li>Slope: (%s &minus; %s) / (%s &minus; %s) = <b>%s</b> dollars per km &mdash; that is
<var>w</var>, the per-km rate. Then <var>b</var> = %s &minus; %s &times; %s = <b>%s</b> dollars &mdash;
the flag-fall you pay before the car moves.</li>
<li>%s &times; 12 + %s = <b>$%s</b>.</li></ol>""" % (
        n(TY[1], 2), n(TY[0], 2), n(TX[1], 0), n(TX[0], 0), n(TW, 2),
        n(TY[0], 2), n(TW, 2), n(TX[0], 0), n(TB, 2), n(TW, 2), n(TB, 2), n(T12, 2)),
    "Any rate-plus-fixed-fee price is the same model as a house price.",
    "A taxi charges a starting fee and then the same amount for every kilometre. Work out those two "
    "numbers and you can price any trip.",
    [("rate", "how much is added for each one unit more"),
     ("flag-fall", "the fixed starting charge in a taxi")]),
),

# =================================================================== q03
D("c1w1-q03",
  recall=M("Write J and three facts about it.",
    """<p>From memory, write the squared error cost <var>J</var>(<var>w</var>, <var>b</var>) for linear
regression. Then write three true facts about it.</p>""",
    """<p><var>J</var>(<var>w</var>, <var>b</var>) = (1/2<var>m</var>) &Sigma;<sub><var>i</var></sub>
(<var>f</var>(<var>x</var><sup>(<var>i</var>)</sup>) &minus; <var>y</var><sup>(<var>i</var>)</sup>)&sup2;</p>
<ul><li>It is <b>never negative</b>: it is a sum of squares.</li>
<li>It scores <b>the whole dataset</b> with one number, not one example.</li>
<li>For linear regression it is a <b>bowl</b> with exactly one minimum.</li></ul>
<p>The 2 in 2<var>m</var> is convention: it cancels when you differentiate.</p>""",
    "J turns &ldquo;how wrong is this line on all the data&rdquo; into one number.",
    "For every point, measure how far the line misses it, square that, then take the average. A "
    "smaller score means a better line.",
    [("cost J", "one number that says how wrong the line is overall"),
     ("&Sigma; (sigma)", "add up all of these"),
     ("m", "how many training examples there are"),
     ("squared", "a number times itself, which is never negative")]),

  work=M("Score two lines on three points.",
    """<p>Data: <var>x</var> = [1, 2, 3], <var>y</var> = [2, 4, 5]. Compute <var>J</var> for line A
(<var>w</var> = %s, <var>b</var> = %s) and line B (<var>w</var> = %s, <var>b</var> = %s). Which is the
better line under this cost?</p>""" % (n(WA, 1), n(BA, 1), n(WB, 1), n(BB, 1)),
    """<p>Line A predicts %s; errors %s; squared sum %s; <var>J</var> = %s / 6 &asymp; <b>%s</b>.</p>
<p>Line B predicts %s; errors %s; squared sum %s; <var>J</var> = %s / 6 &asymp; <b>%s</b>.</p>
<p><b>Line A</b> is better: lower <var>J</var>.</p>""" % (
        _row(FA, 1), _row(FA - Y3, 1), n(np.sum((FA - Y3) ** 2), 2), n(np.sum((FA - Y3) ** 2), 2), n(JA, 4),
        _row(FB, 1), _row(FB - Y3, 1), n(np.sum((FB - Y3) ** 2), 2), n(np.sum((FB - Y3) ** 2), 2), n(JB, 4)),
    "Predict, subtract, square, add, divide by 2m.",
    "Throw darts at a few targets. For each, measure how far you missed and square it. Add them up. "
    "The player with the smaller total threw better.",
    [("error", "prediction minus the true value"),
     ("2m", "twice the number of examples &mdash; here 2 &times; 3 = 6")]),

  spot=M("A cost that says a bad line is perfect.",
    """<p>Someone codes the cost without the square:</p>%s
<p>On two houses with <var>y</var> = [3, 5] and predictions [4, 4], it prints %s. They conclude the
line is perfect. What went wrong?</p>""" % (code("J = np.sum(f - y) / (2 * m)"), n(BUG3, 1)),
    """<p>The errors are %s: one too high, one too low. Without squaring they <b>cancel</b>, so the sum is
0 even though both predictions miss. With the square, <var>J</var> = (1 + 1) / 4 = <b>%s</b>.</p>
<p>The square is what stops misses in opposite directions hiding each other.</p>""" % (
        _row(ES3, 0), n(OK3, 2)),
    "Squaring stops positive and negative misses cancelling out.",
    "If you were 1 metre too far left and then 1 metre too far right, you did not hit the target "
    "twice. You missed twice.",
    [("cancel", "a plus and a minus adding up to zero"),
     ("np.sum", "NumPy's add-them-all-up")]),

  transfer=M("Why squared error suits some jobs and not others.",
    """<p>A delivery firm compares two forecasting models. Model P misses one delivery by 10 hours and
the other nine exactly. Model Q misses all ten deliveries by 1 hour each.</p>
<ol><li>Compare their total squared error.</li>
<li>When is that ranking what the firm wants, and when not?</li></ol>""",
    """<ol><li>P: 10&sup2; = <b>%s</b>. Q: ten &times; 1&sup2; = <b>%s</b>. Squared error ranks <b>Q</b> far
better, even though both miss by 10 hours in total.</li>
<li>Squaring punishes <b>big misses</b> much more than small ones. Good when one huge miss is a disaster
(a perishable delivery). Not what you want if every hour late costs the same &mdash; then the plain
size of the errors would be a fairer score.</li></ol>""" % (n(BIG3, 0), n(SMALL3, 0)),
    "Squaring makes one big miss cost far more than several small ones.",
    "Being very late once can be worse than being a little late every day. Squaring the misses is a way "
    "of saying big mistakes matter much more.",
    [("total squared error", "all the misses squared and added"),
     ("outlier", "one point far away from the rest")]),
),

# =================================================================== q04
D("c1w1-q04",
  recall=M("The update rule and why one rule goes both ways.",
    """<p>From memory, write the gradient descent update for <var>w</var>. Then explain in two sentences
why the same rule moves <var>w</var> up when the slope is negative and down when it is positive.</p>""",
    """<p><var>w</var> &larr; <var>w</var> &minus; &alpha; &part;<var>J</var>/&part;<var>w</var></p>
<p>The minus sign means &ldquo;go against the slope&rdquo;. If the slope is negative, subtracting a
negative <b>adds</b>, so <var>w</var> rises; if positive, <var>w</var> falls. Either way it moves
downhill, because the sign is carried by the derivative.</p>""",
    "Always step against the slope.",
    "If the ground slopes down to your right, step right. If it slopes down to your left, step left. "
    "One rule: walk the way that goes down.",
    [("&part;J/&part;w", "the slope of the cost when you change w"),
     ("&alpha; (alpha)", "the learning rate &mdash; how big each step is"),
     ("&larr;", "&ldquo;becomes&rdquo; &mdash; replace the old value")]),

  work=M("Three slopes, three steps.",
    """<p><var>w</var> = %s and &alpha; = %s. Compute the new <var>w</var> when
&part;<var>J</var>/&part;<var>w</var> is (a) %s, (b) %s, (c) %s.</p>""" % (
        n(W4, 0), n(A4, 1), n(G4[0], 0), n(G4[1], 0), n(G4[2], 0)),
    """<ol type="a"><li>%s &minus; %s &times; (%s) = <b>%s</b> &mdash; up.</li>
<li>%s &minus; %s &times; %s = <b>%s</b> &mdash; down.</li>
<li>%s &minus; %s &times; 0 = <b>%s</b> &mdash; no change: a flat point.</li></ol>""" % (
        n(W4, 0), n(A4, 1), n(G4[0], 0), n(NEW4[0], 2),
        n(W4, 0), n(A4, 1), n(G4[1], 0), n(NEW4[1], 2),
        n(W4, 0), n(A4, 1), n(NEW4[2], 2)),
    "Negative slope pushes w up, positive pushes it down, zero leaves it.",
    "Like a ball on a hill: it rolls whichever way is down, and stops where it is flat.",
    [("flat point", "where the slope is zero, so the step is zero"),
     ("minus a negative", "the same as adding")]),

  spot=M("A sign dropped in one line.",
    """<p>&ldquo;<var>w</var> = %s, &alpha; = %s, and &part;<var>J</var>/&part;<var>w</var> = &minus;4. The
slope is downhill already, so the step is %s &minus; %s &times; 4 = %s.&rdquo;</p>
<p>Find the error.</p>""" % (n(W4, 0), n(A4, 1), n(W4, 0), n(A4, 1), n(SPOT4_BAD, 2)),
    """<p>They used 4 instead of <b>&minus;4</b>. The rule is <var>w</var> &minus; &alpha; &times;
(&minus;4) = %s + %s = <b>%s</b>. With the sign kept, <var>w</var> goes <b>up</b>, which is downhill
on <var>J</var>. Dropping the sign walks uphill.</p>""" % (n(W4, 0), n(A4 * 4, 1), n(NEW4[0], 2)),
    "Keep the derivative's sign inside the rule; it decides the direction.",
    "If the map says &ldquo;turn minus left&rdquo;, that means turn right. Ignore the minus and you go "
    "the wrong way.",
    [("sign", "whether a number is plus or minus"),
     ("downhill", "the direction that makes the cost smaller")]),

  transfer=M("Start on both sides of the valley.",
    """<p>A cost <var>J</var>(<var>w</var>) = (<var>w</var> &minus; 3)&sup2; has slope 2(<var>w</var> &minus; 3).
With &alpha; = %s, take one step from <var>w</var> = %s and one from <var>w</var> = %s. Where does each
land, and what do you notice?</p>""" % (n(A4b, 2), n(L4, 0), n(R4, 0)),
    """<p>From %s: slope = %s, new <var>w</var> = %s &minus; %s &times; (%s) = <b>%s</b>.</p>
<p>From %s: slope = %s, new <var>w</var> = %s &minus; %s &times; %s = <b>%s</b>.</p>
<p>Both move <b>towards 3</b>, the bottom, from opposite sides, with the same rule.</p>""" % (
        n(L4, 0), n(GL4, 0), n(L4, 0), n(A4b, 2), n(GL4, 0), n(NL4, 2),
        n(R4, 0), n(GR4, 0), n(R4, 0), n(A4b, 2), n(GR4, 0), n(NR4, 2)),
    "Whichever side you start on, the rule heads for the bottom.",
    "Two kids at opposite edges of a bowl both roll towards the middle. Nobody had to tell them which "
    "way: the slope did.",
    [("minimum", "the lowest point of the cost"),
     ("valley", "the bowl shape of the cost")]),
),

# =================================================================== q05
D("c1w1-q05",
  recall=M("Two learning-rate failures and their signatures.",
    """<p>From memory: describe what the learning curve looks like when &alpha; is too small and when it is
too large. Then give the one check that tells a too-large &alpha; from a bug.</p>""",
    """<ul><li>Too small: <var>J</var> falls, but very slowly.</li>
<li>Too large: <var>J</var> <b>rises</b> or zig-zags &mdash; each step overshoots the minimum.</li></ul>
<p>The check: set &alpha; very small. Correct gradient descent must then lower <var>J</var> every
step. If it still rises, the gradient code is wrong.</p>""",
    "Rising cost means steps too big; confirm with a tiny step.",
    "Tiny steps get you down the hill slowly. Giant jumps make you leap right over the bottom and "
    "land higher up the other side.",
    [("learning rate &alpha;", "how big each step is"),
     ("overshoot", "jump past the place you wanted to land"),
     ("learning curve", "a graph of the cost as training goes on")]),

  work=M("Four steps with a small and a large &alpha;.",
    """<p><var>J</var>(<var>w</var>) = 2(<var>w</var> &minus; 1)&sup2;, slope 4(<var>w</var> &minus; 1), start
<var>w</var> = 0 (so <var>J</var> = %s). Compute <var>J</var> after each of four steps with
&alpha; = 0.1 and with &alpha; = 0.6.</p>""" % n(J5_START, 0),
    """<ul><li>&alpha; = 0.1: <var>J</var> = %s &mdash; falling.</li>
<li>&alpha; = 0.6: <var>J</var> = %s &mdash; <b>rising</b> every step.</li></ul>
<p>Each step multiplies the distance to the minimum by (1 &minus; 4&alpha;): 0.6 for the small rate,
&minus;1.4 for the large one. Bigger than 1 in size means it grows.</p>""" % (
        _row(J5_SMALL, 4), _row(J5_BIG, 2)),
    "When the step overshoots by more than it corrects, the cost climbs.",
    "If each jump lands you further from the middle than before, you are getting worse each time.",
    [("factor", "the number you multiply by each step"),
     ("diverge", "get further and further from the answer")]),

  spot=M("A rising cost, treated with more iterations.",
    """<p>&ldquo;My cost goes up on almost every iteration. It must need longer to settle, so I raised the
number of iterations from 1,000 to 1,000,000.&rdquo;</p>
<p>What is wrong with this fix?</p>""",
    """<p>More iterations only help a cost that is <b>falling</b> slowly. A cost that rises is
overshooting; more iterations just overshoot more times, until the numbers overflow. The fix is to
<b>lower &alpha;</b> (try ten times smaller), then confirm <var>J</var> falls.</p>""",
    "If the cost is going up, waiting longer makes it worse, not better.",
    "If every step takes you further from home, walking for longer does not get you home. You need "
    "smaller steps.",
    [("iteration", "one step of gradient descent"),
     ("overflow", "a number getting too big for the computer to store")]),

  transfer=M("Your cost printed nan. Explain it.",
    """<p>Training prints a cost of <code>nan</code> after a while. Using the same cost as above with
&alpha; = 0.6, how many steps until the distance to the minimum passes one million? What does
<code>nan</code> most likely mean, and what do you change?</p>""",
    """<p>The distance grows by a factor of %s each step, so it passes one million after <b>%d
steps</b>. Keep going and the numbers overflow to <code>inf</code>, and inf &minus; inf gives
<code>nan</code>.</p>
<p>So <code>nan</code> is usually the end point of a <b>diverging</b> run. Lower &alpha; first.</p>""" % (
        n(FACTOR5, 1), STEPS5),
    "A nan cost is often a learning rate so large the numbers exploded.",
    "If you double a number again and again it gets huge very fast, until the calculator gives up "
    "and shows an error.",
    [("nan", "&ldquo;not a number&rdquo; &mdash; what you get when maths breaks"),
     ("inf", "infinity &mdash; a number too big to store")]),
),

# =================================================================== q06
D("c1w1-q06",
  recall=M("What a contour plot of J shows.",
    """<p>From memory: what does one contour line on a plot of <var>J</var>(<var>w</var>, <var>b</var>)
connect? Where is the minimum? Which way does the gradient point relative to a contour?</p>""",
    """<ul><li>One contour joins every (<var>w</var>, <var>b</var>) with the <b>same value of
<var>J</var></b>.</li>
<li>The minimum is the <b>centre</b> of the innermost ring.</li>
<li>The gradient is <b>perpendicular</b> to the contour, pointing uphill; gradient descent moves the
opposite way.</li></ul>""",
    "Each ring is one cost level, like a height line on a hiking map.",
    "A hiking map draws a line round all the places at the same height. A contour plot does the same "
    "for the cost: every point on a ring is equally wrong.",
    [("contour", "a line joining points with the same value"),
     ("perpendicular", "at a right angle, like a T"),
     ("level set", "all the points where the value is the same")]),

  work=M("Three points on one ring, three different lines.",
    """<p>Take a cost shaped like <var>J</var>(<var>w</var>, <var>b</var>) = (<var>w</var> &minus; 2)&sup2;
+ (<var>b</var> &minus; 1)&sup2;. Compute <var>J</var> at (%s, %s), (%s, %s) and (%s, %s). Then compute
each line's prediction <var>f</var> = <var>w</var><var>x</var> + <var>b</var> at <var>x</var> = 1.</p>""" % (
        n(P6[0, 0], 0), n(P6[0, 1], 0), n(P6[1, 0], 0), n(P6[1, 1], 0), n(P6[2, 0], 0), n(P6[2, 1], 0)),
    """<p><var>J</var> = %s, %s, %s &mdash; all <b>the same</b>, so all three are on one contour.</p>
<p>Predictions at <var>x</var> = 1: %s, %s, %s. Equally wrong overall, but <b>different lines</b> giving
different answers.</p>""" % (n(J6[0], 0), n(J6[1], 0), n(J6[2], 0), n(F6[0], 0), n(F6[1], 0), n(F6[2], 0)),
    "Same contour means same cost, not same line or same prediction.",
    "Three kids can all score 7 out of 10 on a test while getting different questions wrong.",
    [("(w, b)", "one choice of slope and starting amount &mdash; one line"),
     ("equally wrong", "the same cost, even if the mistakes are different")]),

  spot=M("&ldquo;Closer to the centre means lower cost.&rdquo;",
    """<p>The cost is <var>J</var> = (<var>w</var> &minus; 2)&sup2; + 9(<var>b</var> &minus; 1)&sup2;, a long
ellipse. Someone says: &ldquo;Point (2, 2) is only %s from the centre (2, 1), and (5, 1) is %s away, so
(2, 2) must have the lower cost.&rdquo; Check it.</p>""" % (n(DE6[1], 0), n(DE6[0], 0)),
    """<p>Compute: <var>J</var>(5, 1) = %s and <var>J</var>(2, 2) = %s. <b>Equal</b> &mdash; both on the same
contour. On an ellipse, distance from the centre does not decide the cost; the squeezed direction rises
much faster. &ldquo;Same distance, same cost&rdquo; only holds for circles.</p>""" % (
        n(JE6[0], 0), n(JE6[1], 0)),
    "On stretched contours, near and far points can share the same cost.",
    "On a narrow valley, one step sideways can climb as high as many steps along the floor.",
    [("ellipse", "a stretched circle, like an oval"),
     ("centre", "the lowest point, in the middle of the rings")]),

  transfer=M("Read a real hiking map with the same idea.",
    """<p>On a hiking map, contour lines are drawn every 20 m of height. In one area the lines are 2 mm
apart; in another they are 10 mm apart. Which area is steeper? If a cost plot looked like that, where
would gradient descent take its biggest steps?</p>""",
    """<p>The <b>2 mm</b> area: lines close together mean height changes quickly &mdash; steep.</p>
<p>On a cost plot, closely packed contours mean a large gradient, so the <b>step</b> &alpha; &times; gradient
is biggest there. Far-apart rings near the minimum mean small slopes and small steps.</p>""",
    "Contours packed close together mean steep ground and big steps.",
    "On a map, when the lines are squashed together, the hill is steep. When they are spread out, it "
    "is nearly flat.",
    [("steep", "height changing fast over a short distance"),
     ("gradient", "how steep it is, and which way is up")]),
),

# =================================================================== q07
D("c1w1-q07",
  recall=M("Unsupervised learning, and its three kinds.",
    """<p>From memory: define unsupervised learning in one sentence, give the one test that tells it
apart from supervised, and name three kinds of unsupervised problem.</p>""",
    """<p>Unsupervised learning finds <b>structure in data that has no labels</b>.</p>
<p>The test: <b>does the training data contain the answer you want to predict?</b> If no, it is
unsupervised.</p>
<p>Kinds: <b>clustering</b> (find groups), <b>anomaly detection</b> (find unusual points),
<b>dimensionality reduction</b> (compress many features into fewer).</p>""",
    "No labels: the algorithm has to find the pattern on its own.",
    "Nobody tells you the answers. You just look at a big pile of things and notice which ones go "
    "together.",
    [("unsupervised", "learning without any answers given"),
     ("structure", "a pattern, like groups"),
     ("dimensionality reduction", "squashing many measurements into a few")]),

  work=M("Sort five problems: labels or not?",
    """<p>For each, say whether the training data contains the answer, and so whether it is supervised
or unsupervised:</p>
<ol><li>Group 2 million songs by how they sound; no genres given.</li>
<li>Predict a song's play count next month from past songs' play counts.</li>
<li>Find factory sensor readings that look unlike normal operation.</li>
<li>Decide whether a review is positive, from 40,000 reviews with star ratings.</li>
<li>Compress 300 survey answers per person into 3 summary scores.</li></ol>""",
    """<ol><li>No answer in the data &rarr; <b>unsupervised</b> (clustering).</li>
<li>Past play counts are labels &rarr; <b>supervised</b> (regression).</li>
<li>No labels of &ldquo;broken&rdquo; &rarr; <b>unsupervised</b> (anomaly detection).</li>
<li>Star ratings act as labels &rarr; <b>supervised</b> (classification).</li>
<li>No answer to predict &rarr; <b>unsupervised</b> (dimensionality reduction).</li></ol>""",
    "Look for the answer column; if there isn't one, it is unsupervised.",
    "Ask: did anyone write the right answers next to the examples? If not, the computer has to find "
    "the pattern by itself.",
    [("play count", "how many times a song was played"),
     ("star rating", "the 1&ndash;5 stars a reviewer gave")]),

  spot=M("&ldquo;We chose the number of groups, so it is supervised.&rdquo;",
    """<p>&ldquo;We split our customers into 5 groups with k-means. Because <b>we</b> decided there should
be 5 groups, a human supervised it, so this is supervised learning.&rdquo;</p>
<p>What is wrong?</p>""",
    """<p>&ldquo;Supervised&rdquo; is about <b>labels in the training data</b>, not about whether a human
made any choices. Choosing <var>k</var> = 5 is a setting; no customer came with a correct group. So it
is still <b>unsupervised</b> clustering.</p>""",
    "Supervised means the data has answers, not that a person set things up.",
    "Deciding to sort your toys into 5 boxes is not the same as someone telling you which box each "
    "toy belongs in.",
    [("k-means", "a method that finds k groups in unlabelled data"),
     ("setting", "a choice you make before training, like how many groups")]),

  transfer=M("Unsupervised first, then supervised.",
    """<p>A support team has 100,000 unlabelled customer emails. They want, eventually, to route each new
email to the right team automatically. Describe how an unsupervised step could help before any
supervised model exists.</p>""",
    """<p>First <b>cluster</b> the emails (unsupervised) to discover the main kinds of request &mdash;
refunds, login problems, shipping. People then name the clusters and label a sample, which creates
<b>labels</b>. With labels, a <b>supervised classifier</b> can route new emails.</p>
<p>Unsupervised learning often finds the categories that supervised learning later predicts.</p>""",
    "Finding groups without labels can be the step that creates labels.",
    "First sort the post into piles that look alike. Then give each pile a name. Now you can teach "
    "someone to put new letters in the right pile.",
    [("route", "send each email to the right team"),
     ("classifier", "a model that picks a category")]),
),

# =================================================================== q08
D("c1w1-q08",
  recall=M("Write the update so both use the old values.",
    """<p>From memory, write the gradient descent update for <var>w</var> and <var>b</var> so that it is
<b>simultaneous</b>. Then say in one sentence what goes wrong if you are not careful.</p>""",
    """<p>Compute both slopes first, from the current values:</p>
<p>tmp_w = <var>w</var> &minus; &alpha; &part;<var>J</var>/&part;<var>w</var>;
tmp_b = <var>b</var> &minus; &alpha; &part;<var>J</var>/&part;<var>b</var>; then <var>w</var> = tmp_w,
<var>b</var> = tmp_b.</p>
<p>Update <var>w</var> first and then compute <var>b</var>'s slope, and you measure the slope at a
point you have already moved away from.</p>""",
    "Work out both changes first, then make them together.",
    "Look at the map once and decide both moves, then make them. Don't move one foot, look again, "
    "and change your plan for the other.",
    [("simultaneous", "at the same time, from the same starting point"),
     ("tmp", "a temporary holder for the new value")]),

  work=M("One step done right, and done in order.",
    """<p>Data <var>x</var> = [1, 2, 3], <var>y</var> = [3, 5, 7]. Start <var>w</var> = 0, <var>b</var> = 0,
&alpha; = %s, with &part;<var>J</var>/&part;<var>w</var> = mean(err &times; <var>x</var>) and
&part;<var>J</var>/&part;<var>b</var> = mean(err).</p>
<ol><li>Do one simultaneous step.</li>
<li>Now do it the wrong way: update <var>w</var>, recompute the errors, then update <var>b</var>.</li></ol>""" % n(A8, 1),
    """<ol><li>Errors %s. Slopes: %s and %s. New <var>w</var> = <b>%s</b>, new <var>b</var> =
<b>%s</b>.</li>
<li><var>w</var> becomes %s as before, but the errors recomputed with it are %s, giving a <var>b</var> slope of
%s and <var>b</var> = <b>%s</b> instead of %s.</li></ol>
<p>Same data, same &alpha;, a different <var>b</var> &mdash; and no error message.</p>""" % (
        _row(E8, 0), n(DW8, 3), n(DB8, 3), n(W8_OK, 4), n(B8_OK, 4),
        n(W8_OK, 4), _row(E8b, 3), n(DB8_BAD, 3), n(B8_BAD, 4), n(B8_OK, 4)),
    "Updating in order quietly changes the answer.",
    "If two friends share a pizza and the first one takes their slice before you count, you count a "
    "different pizza.",
    [("err", "prediction minus truth for each example"),
     ("mean", "the average")]),

  spot=M("Four lines of code. One of them breaks the rule.",
    """<p>Find the line that makes this update not simultaneous:</p>%s""" % code(
        "err = w * x + b - y\n"
        "w = w - alpha * np.mean(err * x)\n"
        "err = w * x + b - y\n"
        "b = b - alpha * np.mean(err)"),
    """<p><b>Line 3.</b> It recomputes <code>err</code> with the <b>new</b> <code>w</code>, so <code>b</code>'s
slope comes from a different point. Delete line 3 &mdash; then both updates use the errors computed at
the old <code>w</code> and <code>b</code>.</p>
<p>It still runs and usually still converges, which is exactly why this bug survives.</p>""",
    "Compute the errors once per step, before changing anything.",
    "It is like checking the weather, getting dressed, then checking again and packing for different "
    "weather. Check once.",
    [("recompute", "work it out again"),
     ("converge", "settle down to a final answer")]),

  transfer=M("Many weights at once: is it automatic?",
    """<p>Next week <var>w</var> becomes a vector of many weights, updated with one line
<code>w = w - alpha * dj_dw</code>. Is the update automatically simultaneous? What about
<var>b</var>?</p>""",
    """<p>For the weights, <b>yes</b>: <code>dj_dw</code> is computed in full before that line runs, so every
weight uses the same old values.</p>
<p>For <var>b</var>, only if <code>dj_db</code> is <b>also</b> computed before <code>w</code> changes.
Compute both gradients first, then update both.</p>""",
    "Vector updates are simultaneous within the vector; b still has to be done in the right order.",
    "If you work out everyone's new seat first and then all move at once, nobody gets confused. One "
    "late person still needs the old plan.",
    [("vector", "a list of numbers handled together"),
     ("dj_dw", "the code name for all the weights' slopes")]),
),

# =================================================================== q09
D("c1w1-q09",
  recall=M("What a flat learning curve tells you, and what it doesn't.",
    """<p>From memory: what does it mean when the learning curve flattens? Name two things that flat curve
does <b>not</b> tell you.</p>""",
    """<p>Flat means <b>converged</b>: the parameters have stopped changing meaningfully, so more
iterations will not lower <var>J</var>.</p>
<p>It does <b>not</b> tell you that the fit is good, and it does not tell you how the model does on new
data.</p>""",
    "Converged means finished, not necessarily good.",
    "When you stop getting better at a game, it means you've done all you can with that strategy. It "
    "doesn't mean you're good at the game.",
    [("converged", "stopped changing, settled"),
     ("learning curve", "cost plotted against iteration")]),

  work=M("Find the stopping point with a convergence test.",
    """<p>A convergence test stops when <var>J</var> changes by less than &epsilon; = 0.001 in one iteration.
A model of house price (in $1000s) against size is trained with &alpha; = 0.1. The same data is then
trained with the price in <b>dollars</b>. At which iteration does each run stop?</p>""",
    """<p>Price in $1000s: stops at iteration <b>%s</b>. Price in dollars: <b>%s</b>.</p>
<p>The dollar run's <var>J</var> is a million times larger, so its changes stay above 0.001 far longer.
A fixed &epsilon; means different things at different scales &mdash; check the curve, not just the
test.</p>""" % (STOP_K, STOP_D if STOP_D else "not within 3,000"),
    "A fixed stopping threshold depends on the units of the cost.",
    "Saying &ldquo;stop when it changes by less than 1&rdquo; means something very different in "
    "centimetres than in kilometres.",
    [("&epsilon; (epsilon)", "a tiny number used as a &ldquo;close enough&rdquo; threshold"),
     ("convergence test", "a rule that stops training once J barely changes")]),

  spot=M("&ldquo;Flat curve, so the model is accurate.&rdquo;",
    """<p>&ldquo;My learning curve went flat at <var>J</var> = %s. It has converged, so the model is a good
fit.&rdquo;</p>
<p>A baseline that ignores <var>x</var> and always predicts the average price has <var>J</var> = %s.
What should they conclude?</p>""" % (n(J9_MODEL, 3), n(J9_BASE, 3)),
    """<p>The model has converged &mdash; that part is right. But it is only <b>%s</b> better than
predicting the average every time. Converged tells you the optimiser finished, not that the model is
any good. Compare against a baseline before calling a fit good.</p>""" % n(J9_BASE - J9_MODEL, 3),
    "Always compare a converged cost against a simple baseline.",
    "Finishing a race does not mean you won it. Check how you did against someone who just walked.",
    [("baseline", "a very simple guess to compare against"),
     ("average", "the mean of all the prices")]),

  transfer=M("Two curves, two diagnoses.",
    """<p>Curve A is still falling clearly at iteration 1,000. Curve B fell fast and has been flat since
iteration 200. For each, say what you would do next.</p>""",
    """<p><b>A</b> has not converged: more iterations, or a larger &alpha; (about &times;3), then look
again.</p>
<p><b>B</b> has converged: running longer is pointless. To lower <var>J</var> further you need a
different model (better features), not more steps &mdash; and to judge it, test on data it has not
seen.</p>""",
    "Still falling: keep going or step bigger. Flat: change the model, not the run.",
    "If you're still improving, keep practising. If you've stopped improving, practising the same "
    "way won't help; try something different.",
    [("iteration", "one step of training"),
     ("unseen data", "examples the model did not train on")]),
),

# =================================================================== q10
D("c1w1-q10",
  recall=M("What w and b mean, with their units.",
    """<p>From memory: in <var>f</var>(<var>x</var>) = <var>w</var><var>x</var> + <var>b</var>, what does
<var>w</var> mean and what does <var>b</var> mean? What are the units of each when <var>x</var> is in
sq ft and price in $1000s?</p>""",
    """<p><var>w</var> is a <b>rate</b>: the change in prediction for one extra unit of <var>x</var>. Units:
$1000s <b>per sq ft</b>.</p>
<p><var>b</var> is an <b>offset</b>: the prediction when <var>x</var> = 0. Units: $1000s.</p>""",
    "w is a rate per unit of x; b is the value at x = 0.",
    "w says how much more you pay for each extra bit. b is what you'd pay for nothing at all.",
    [("rate", "how much changes for each one unit more"),
     ("offset", "a fixed amount the line is shifted by"),
     ("units", "what a number is measured in")]),

  work=M("Read a model in plain words.",
    """<p>price ($1000s) = %s &times; size (sq ft) + %s.</p>
<ol><li>How much does an extra 150 sq ft add?</li>
<li>Predict a 1,400 sq ft house.</li>
<li>What is <var>w</var> in dollars per square foot?</li></ol>""" % (n(W10, 2), n(B10, 0)),
    """<ol><li>%s &times; 150 = <b>%s</b>, i.e. $%s,000.</li>
<li>%s &times; 1400 + %s = <b>%s</b>, i.e. $%s,000.</li>
<li>%s thousand dollars = <b>$%s</b> per sq ft.</li></ol>""" % (
        n(W10, 2), n(EXTRA10, 1), n(EXTRA10, 0), n(W10, 2), n(B10, 0), n(P10, 0), n(P10, 0),
        n(W10, 2), n(DOLLARS10, 0)),
    "Multiply w by the change in x to get the change in price.",
    "If each extra tile costs a bit, then 150 extra tiles cost 150 bits.",
    [("$1000s", "thousands of dollars"),
     ("per sq ft", "for every square foot")]),

  spot=M("A unit slip that makes houses cheap.",
    """<p>&ldquo;The model is price ($1000s) = %s &times; size (sq ft) + %s. So each extra square foot adds
<b>%s dollars</b>.&rdquo;</p>
<p>Where is the slip?</p>""" % (n(W10, 2), n(B10, 0), n(W10, 2)),
    """<p>Price is in <b>thousands</b> of dollars, so <var>w</var> = %s means %s thousand dollars per square
foot = <b>$%s</b>. Reading the units off the price column is part of reading <var>w</var>.</p>""" % (
        n(W10, 2), n(W10, 2), n(DOLLARS10, 0)),
    "w carries the units of the output divided by the units of the input.",
    "If the price tag says &ldquo;in thousands&rdquo; and you forget, you'll think a house costs the "
    "same as a sandwich.",
    [("units of w", "output units per input unit"),
     ("thousands", "multiply by 1,000 to get dollars")]),

  transfer=M("An exam-score model, then change the units.",
    """<p>A model predicts exam score (points) = %s &times; hours studied + %s.</p>
<ol><li>What do %s and %s mean? Predict the score for 6 hours.</li>
<li>If you measure study time in <b>minutes</b> instead, what happens to <var>w</var> and
<var>b</var>?</li></ol>""" % (n(WS, 1), n(BS, 0), n(WS, 1), n(BS, 0)),
    """<ol><li><var>w</var> = %s: each extra hour adds %s points. <var>b</var> = %s: the predicted score with
no study at all. For 6 hours: %s &times; 6 + %s = <b>%s</b>.</li>
<li><var>w</var> becomes %s / 60 = <b>%s</b> points per minute; <var>b</var> stays <b>%s</b>, because zero
hours and zero minutes are the same thing. The predictions do not change.</li></ol>""" % (
        n(WS, 1), n(WS, 1), n(BS, 0), n(WS, 1), n(BS, 0), n(S6, 0), n(WS, 1), n(WS_MIN, 3), n(BS, 0)),
    "Changing the units of x rescales w; b and the predictions stay the same.",
    "Saying &ldquo;6 hours&rdquo; or &ldquo;360 minutes&rdquo; is the same amount of studying, so the "
    "guessed score can't change. Only the per-unit number changes.",
    [("per minute", "for each minute, instead of each hour"),
     ("rescale", "multiply or divide to change units")]),
),
]
