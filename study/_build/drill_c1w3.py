# -*- coding: utf-8 -*-
"""Quiz drills — C1 W3. One concept per mock-quiz question, four methods each.

Every number below is COMPUTED here at import time and formatted into the text,
never typed. If a value is wrong, it is wrong in the arithmetic, where you can
see it, not in a sentence.
"""
import math
import warnings

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


def _row(vals, d=3):
    return "[" + ", ".join(n(v, d) for v in vals) + "]"


# ---------------------------------------------------------------- q01 why not linear
X1 = np.array([1., 2, 3, 4, 5, 6]); Y1 = np.array([0., 0, 0, 1, 1, 1])
P1 = np.polyfit(X1, Y1, 1)
CROSS1 = (0.5 - P1[1]) / P1[0]
F1_AT4 = np.polyval(P1, 4)
X1b = np.append(X1, 20.0); Y1b = np.append(Y1, 1.0)
P1b = np.polyfit(X1b, Y1b, 1)
CROSS1b = (0.5 - P1b[1]) / P1b[0]
F1b_AT4 = np.polyval(P1b, 4)
F1b_AT20 = np.polyval(P1b, 20)

# ---------------------------------------------------------------- q02 sigmoid
Z2 = np.array([-4., -1, 0, 1, 4])
G2 = g(Z2)
Z2_90 = np.log(0.9 / 0.1)
G2_POS2 = g(2.0)
G2_BAD = 1 / (1 + np.exp(2.0))
G2_3, G2_M3 = g(3.0), g(-3.0)
Z2_99 = np.log(0.99 / 0.01)

# ---------------------------------------------------------------- q03 reading the output
W3 = np.array([1.5, -0.8]); B3 = -1.0
XP3 = np.array([2.0, 1.5])
Z3 = XP3 @ W3 + B3
F3 = g(Z3)
T3_LOW = 0.2
ZT3_LOW = np.log(T3_LOW / (1 - T3_LOW))
T3_HIGH = 0.7
ZT3_HIGH = np.log(T3_HIGH / (1 - T3_HIGH))

# ---------------------------------------------------------------- q04 why not squared error
WS4 = np.array([-6.0, -3.0, 0.0])
SQ4 = (g(WS4) - 1) ** 2
LG4 = -np.log(g(WS4))
SQ4_MID_AVG = (SQ4[0] + SQ4[2]) / 2
LG4_MID_AVG = (LG4[0] + LG4[2]) / 2
S4 = g(-6.0)
GRAD4_SQ = 2 * (S4 - 1) * S4 * (1 - S4)      # d/dw of (g(w) - 1)^2 at x = 1
GRAD4_LOG = S4 - 1                           # d/dw of -log g(w) at x = 1
RATIO4 = GRAD4_LOG / GRAD4_SQ

# ---------------------------------------------------------------- q05 the loss curve
F5 = np.array([0.9, 0.5, 0.1, 0.01])
L5 = -np.log(F5)
L5_BAD = -np.log(0.95)
L5_OK = -np.log(1 - 0.95)
L5_GOOD = -np.log(0.99)
L5_AWFUL = -np.log(1e-4)
AVG5 = (99 * L5_GOOD + L5_AWFUL) / 100
EQUIV5 = L5_AWFUL / L5_GOOD

# ---------------------------------------------------------------- q06 overfitting
_rng6 = np.random.default_rng(3)
XT6 = np.linspace(0, 1, 10)
YT6 = 1 + 2 * XT6 - 3 * XT6 ** 2 + _rng6.normal(0, 0.15, 10)
XV6 = np.linspace(0.05, 0.95, 10)
YV6 = 1 + 2 * XV6 - 3 * XV6 ** 2 + _rng6.normal(0, 0.15, 10)
ERR6 = {}
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    for _d in (1, 2, 9):
        _p = np.polyfit(XT6, YT6, _d)
        ERR6[_d] = (np.sqrt(np.mean((np.polyval(_p, XT6) - YT6) ** 2)),
                    np.sqrt(np.mean((np.polyval(_p, XV6) - YV6) ** 2)))

# ---------------------------------------------------------------- q07 regularization
M7 = 4
W7 = np.array([3.0, -2.0, 0.5])
LAM7 = 2.0
PEN7 = LAM7 / (2 * M7) * np.sum(W7 ** 2)
# a lambda sweep on the q06 data: degree-9 features, z-scored, b not penalised
_F = np.column_stack([XT6 ** k for k in range(1, 10)])
_FV = np.column_stack([XV6 ** k for k in range(1, 10)])
_mu, _sd = _F.mean(axis=0), _F.std(axis=0)
_ZT, _ZV = (_F - _mu) / _sd, (_FV - _mu) / _sd
LAMS7 = (0.001, 0.01, 0.1, 1.0, 10.0, 100.0)
SWEEP7 = {}
for _lam in LAMS7:
    _w = np.linalg.solve(_ZT.T @ _ZT + _lam * np.eye(9), _ZT.T @ (YT6 - YT6.mean()))
    _b = YT6.mean()
    SWEEP7[_lam] = (np.sqrt(np.mean((_ZT @ _w + _b - YT6) ** 2)),
                    np.sqrt(np.mean((_ZV @ _w + _b - YV6) ** 2)),
                    np.linalg.norm(_w))
BEST7 = LAMS7[0]
for _lam in LAMS7:
    if SWEEP7[_lam][1] < SWEEP7[BEST7][1]:
        BEST7 = _lam

# ---------------------------------------------------------------- q08 what gets regularized
A8, LAM8, M8 = 0.1, 2.0, 4
SHRINK8 = 1 - A8 * LAM8 / M8
W8 = np.array([2.0, -1.0]); G8 = np.array([0.3, -0.1])
NEWW8 = W8 * SHRINK8 - A8 * G8
B8, GB8 = 5.0, 0.2
NEWB8 = B8 - A8 * GB8
M8b, LAM8b, YBAR8 = 50, 10.0, 310.0
BPEN8 = M8b * YBAR8 / (M8b + LAM8b)   # b with a penalty, features zero-mean

# ---------------------------------------------------------------- q09 the update rule
X9 = np.array([0.5, 1.5, -1.0]); Y9 = np.array([1.0, 1.0, 0.0])
W9, B9, A9 = 0.4, -0.2, 0.5
F9 = g(W9 * X9 + B9)
E9 = F9 - Y9
DW9 = np.mean(E9 * X9)
DB9 = np.mean(E9)
NW9, NB9 = W9 - A9 * DW9, B9 - A9 * DB9
DW9_WRONG = np.mean(E9 * F9 * (1 - F9) * X9)

# ---------------------------------------------------------------- q10 fixing overfitting
NF10_6 = math.comb(6 + 2, 2) - 1     # monomials of degree 1..6 in two features
NF10_2 = math.comb(2 + 2, 2) - 1
NF10_3 = math.comb(3 + 2, 2) - 1


DRILLS = [

# =================================================================== q01
D("c1w3-q01",
  recall=M("Two reasons a straight line fails at yes/no.",
    """<p>From memory, give the <b>two</b> separate reasons linear regression is a poor fit for a 0/1
target. Then say what logistic regression changes to fix each one.</p>""",
    """<ol><li><b>Range:</b> a line is unbounded, so it predicts values below 0 and above 1, which cannot
be probabilities.</li>
<li><b>Leverage:</b> a far-away but perfectly ordinary example tilts the whole line and slides the
0.5 crossing, changing predictions for cases whose data did not change.</li></ol>
<p>Logistic regression passes the line through a sigmoid: the output is squeezed into (0, 1), and the
cost no longer rewards fitting extreme points with a straight ramp.</p>""",
    "A straight line goes on forever and gets dragged by far-away points; yes/no needs neither.",
    "Imagine a seesaw used to vote yes or no. One very heavy kid sitting at the far end tips the whole "
    "thing, and suddenly kids in the middle get counted wrong even though nothing about them changed.",
    [("binary target", "an answer that is only ever 0 or 1, no or yes"),
     ("unbounded", "can keep growing past any limit"),
     ("decision boundary", "the place where the guess switches from 0 to 1")]),

  work=M("Fit a line, then add one far-away example.",
    """<p>Tumour sizes <var>x</var> = [1, 2, 3, 4, 5, 6] with labels <var>y</var> = [0, 0, 0, 1, 1, 1].
A least-squares line gives <var>f</var>(<var>x</var>) = %s<var>x</var> %s.</p>
<ol><li>Where does the line cross 0.5? What class does a tumour of size 4 get?</li>
<li>Add one more example: size 20, label 1 (clearly malignant). The new least-squares line is
<var>f</var>(<var>x</var>) = %s<var>x</var> + %s. Where does it cross 0.5 now, and what happens to the
size-4 tumour? What does the line predict at size 20?</li></ol>""" % (
        n(P1[0], 4), "&minus; " + n(-P1[1], 4) if P1[1] < 0 else "+ " + n(P1[1], 4),
        n(P1b[0], 4), n(P1b[1], 4)),
    """<ol><li>Solve %s<var>x</var> %s = 0.5: <var>x</var> = <b>%s</b>. At size 4, <var>f</var> = %s,
above 0.5, so class <b>1</b>.</li>
<li>Crossing moves to <b>%s</b>. At size 4, <var>f</var> = %s &mdash; now below 0.5, so the
prediction <b>flips to 0</b>, although nothing about that tumour changed. At size 20 the line says
<b>%s</b>, which is not a probability at all.</li></ol>
<p>Both reasons in one example: one clear-cut point moved the boundary, and the output left [0, 1].</p>""" % (
        n(P1[0], 4), "&minus; " + n(-P1[1], 4) if P1[1] < 0 else "+ " + n(P1[1], 4),
        n(CROSS1, 2), n(F1_AT4, 3), n(CROSS1b, 2), n(F1b_AT4, 3), n(F1b_AT20, 3)),
    "One obvious example can flip the answer for a different case, and the line can say more than 100%.",
    "A big, clearly-sick case far away pulled the ruler flat, so a medium case in the middle got called "
    "healthy. That is unfair to the medium case: nothing about it changed.",
    [("least squares", "the line with the smallest total squared miss"),
     ("crossing 0.5", "the size where the line's answer changes from no to yes"),
     ("flip", "the predicted class changes from 1 to 0")]),

  spot=M("&ldquo;Just clip the line to [0, 1].&rdquo;",
    """<p>A classmate's fix: &ldquo;Linear regression's only problem is that it goes above 1 and below 0.
So I clip its output to [0, 1] and threshold at 0.5. Problem solved.&rdquo;</p>
<p>On the tumour data (sizes 1&ndash;6, labels 0,0,0,1,1,1, plus one extra example at size 20 with
label 1), does clipping rescue the size-4 tumour? Find the step in the argument that fails.</p>""",
    """<p>&ldquo;Its <b>only</b> problem&rdquo; is the failing step. Clipping fixes the range but not the
<b>leverage</b>. The far point still tilts the line: the 0.5 crossing still moves from %s to %s, and
the size-4 tumour is still predicted %s &rarr; class 0. Clipping a value of %s changes nothing.</p>
<p>The boundary is decided where the line crosses 0.5, which is in the middle of the data &mdash;
exactly where clipping does not act.</p>""" % (n(CROSS1, 2), n(CROSS1b, 2), n(F1b_AT4, 3), n(F1b_AT4, 3)),
    "Clipping hides the out-of-range numbers but leaves the dragged boundary where it was.",
    "Cutting off the ends of a bent ruler does not straighten the middle of it.",
    [("clip", "force any value below 0 up to 0, and above 1 down to 1"),
     ("leverage", "how much one point can pull the whole fitted line")]),

  transfer=M("Five targets: which model?",
    """<p>For each target, would you reach for linear or logistic regression?</p>
<ol><li>Tomorrow's maximum temperature.</li><li>Whether a loan will default.</li>
<li>The sale price of a used car.</li><li>Whether a photo contains a face.</li>
<li>The chance of rain tomorrow, to print on a weather app.</li></ol>""",
    """<ol><li><b>Linear</b> &mdash; a quantity on a continuous scale.</li>
<li><b>Logistic</b> &mdash; a yes/no outcome.</li>
<li><b>Linear</b> &mdash; a continuous amount.</li>
<li><b>Logistic</b> &mdash; yes/no.</li>
<li><b>Logistic</b> &mdash; you want a probability between 0 and 1, which is exactly what its output
is. A line could print &ldquo;120% chance of rain&rdquo;.</li></ol>""",
    "Ask what the target is: an amount (linear) or a yes/no with a probability (logistic).",
    "If the answer is &ldquo;how much?&rdquo;, use a ruler. If the answer is &ldquo;yes or no, and how "
    "sure?&rdquo;, use a dial that only goes from 0 to 1.",
    [("continuous", "can be any number, like 21.7 degrees"),
     ("probability", "a chance between 0 (never) and 1 (certain)")]),
),

# =================================================================== q02
D("c1w3-q02",
  recall=M("The sigmoid, from a blank page.",
    """<p>Write the sigmoid formula. Then, without a calculator: its value at <var>z</var> = 0, what it
approaches as <var>z</var> &rarr; +&infin; and &minus;&infin;, its range, and how <var>g</var>(&minus;<var>z</var>)
relates to <var>g</var>(<var>z</var>).</p>""",
    """<p><var>g</var>(<var>z</var>) = 1 / (1 + <var>e</var><sup>&minus;<var>z</var></sup>).</p>
<ul><li><var>g</var>(0) = 1/2.</li><li><var>z</var> &rarr; +&infin;: <var>g</var> &rarr; 1.
<var>z</var> &rarr; &minus;&infin;: <var>g</var> &rarr; 0.</li>
<li>Range: strictly between 0 and 1 &mdash; it never reaches either.</li>
<li>Symmetry: <var>g</var>(&minus;<var>z</var>) = 1 &minus; <var>g</var>(<var>z</var>).</li></ul>""",
    "The sigmoid squeezes any number into a value between 0 and 1, with 0 landing exactly at a half.",
    "It is a dimmer switch. Turn the knob far one way and the light is almost off; far the other way, "
    "almost fully on. Right in the middle, it is exactly half bright.",
    [("sigmoid", "the S-shaped squashing curve"),
     ("<var>e</var>", "a fixed number, about 2.718, that shows up in growth and decay"),
     ("&rarr; &infin;", "keeps getting bigger without stopping")]),

  work=M("Five values of the sigmoid, and one in reverse.",
    """<ol><li>Compute <var>g</var>(<var>z</var>) for <var>z</var> = &minus;4, &minus;1, 0, 1, 4.</li>
<li>Which <var>z</var> gives <var>g</var>(<var>z</var>) = 0.9? (Hint: solve
1/(1 + <var>e</var><sup>&minus;<var>z</var></sup>) = 0.9 for <var>z</var>.)</li></ol>""",
    """<ol><li>%s. Notice the pairs: <var>g</var>(&minus;1) + <var>g</var>(1) = 1, and the same for
&plusmn;4.</li>
<li>0.9 = 1/(1 + <var>e</var><sup>&minus;<var>z</var></sup>) gives <var>e</var><sup>&minus;<var>z</var></sup>
= 1/9, so <var>z</var> = ln 9 &asymp; <b>%s</b>. To be 90%% sure, the model needs <var>z</var> above
about 2.2 &mdash; not 0.9.</li></ol>""" % (
        ", ".join("<var>g</var>(%s) &asymp; <b>%s</b>" % (n(z, 0), n(v, 4)) for z, v in zip(Z2, G2)),
        n(Z2_90, 3)),
    "Equal steps in z do not give equal steps in probability; the curve is steep near 0 and flat at the ends.",
    "Pushing a swing near the bottom moves it a lot. Pushing it when it is already high hardly moves it "
    "at all.",
    [("ln", "the natural log: the power you raise e to, to get a number"),
     ("symmetric", "the left half is a flipped copy of the right half")]),

  spot=M("A sign slip in a sigmoid.",
    """<p>The working for <var>g</var>(2):</p>
<p><var>g</var>(2) = 1 / (1 + <var>e</var><sup>2</sup>) = 1 / (1 + 7.389) = %s</p>
<p>&ldquo;So a positive <var>z</var> of 2 gives about a 12%% chance of class 1.&rdquo; Find the error.</p>""" % n(G2_BAD, 4),
    """<p>The exponent should be <b>&minus;<var>z</var></b>: <var>g</var>(2) = 1/(1 + <var>e</var><sup>&minus;2</sup>)
= 1/(1 + 0.135) &asymp; <b>%s</b>.</p>
<p>The check that catches it: a <b>positive</b> <var>z</var> must give <b>more</b> than 0.5. The slip
computed <var>g</var>(&minus;2) instead &mdash; and indeed %s + %s = 1.</p>""" % (
        n(G2_POS2, 4), n(G2_POS2, 4), n(G2_BAD, 4)),
    "Positive z means above a half; if you get below a half, look for a missing minus sign.",
    "If the knob is turned towards &ldquo;on&rdquo;, the light cannot be dimmer than half. A dim answer "
    "means you turned the knob the wrong way.",
    [("exponent", "the small raised number: how many times to multiply"),
     ("sanity check", "a quick test that the answer is in the right ballpark")]),

  transfer=M("Use the symmetry instead of a calculator.",
    """<ol><li>You are told <var>g</var>(3) &asymp; %s. Without computing anything, what is
<var>g</var>(&minus;3)?</li>
<li>A spam filter only marks mail as spam when it is at least 99%% sure. What value of
<var>z</var> = <var>w</var>&middot;<var>x</var> + <var>b</var> does an email need?</li></ol>""" % n(G2_3, 4),
    """<ol><li><var>g</var>(&minus;3) = 1 &minus; <var>g</var>(3) &asymp; <b>%s</b>.</li>
<li><var>z</var> = ln(0.99 / 0.01) = ln 99 &asymp; <b>%s</b>. In general, the <var>z</var> for
probability <var>p</var> is ln(<var>p</var> / (1 &minus; <var>p</var>)), the <b>log-odds</b>.</li></ol>""" % (
        n(G2_M3, 4), n(Z2_99, 3)),
    "z is the log-odds: the sigmoid turns it into a probability, and ln(p/(1&minus;p)) turns it back.",
    "If 95 kids out of 100 like ice cream, then 5 do not. You did not need to ask the 5 &mdash; you "
    "worked it out from the 95.",
    [("log-odds", "ln of (chance yes / chance no) &mdash; the number z really is"),
     ("odds", "how many times more likely yes is than no")]),
),

# =================================================================== q03
D("c1w3-q03",
  recall=M("What the number coming out actually means.",
    """<p>From memory: what does the output <var>f</var>(<var>x</var>) of logistic regression estimate?
How do you turn it into a class? Where is the decision boundary, in terms of <var>z</var>?</p>""",
    """<p><var>f</var>(<var>x</var>) estimates <b>P(<var>y</var> = 1 | <var>x</var>)</b> &mdash; the
probability the label is 1.</p>
<p>The class comes from a <b>threshold you choose</b>: predict 1 if <var>f</var> &ge; 0.5 (the usual
default).</p>
<p>With threshold 0.5 the boundary is where <var>z</var> = <var>w</var>&middot;<var>x</var> + <var>b</var> = 0,
because <var>g</var>(0) = 0.5.</p>""",
    "The output is a probability of class 1; the class is a separate decision made with a threshold.",
    "The weather app says 30% chance of rain. Whether you take an umbrella is your choice &mdash; the "
    "30% is just the app's best guess.",
    [("P(y = 1 | x)", "the chance the answer is yes, given this example"),
     ("threshold", "the cut-off you pick for saying yes"),
     ("decision boundary", "the line where the guess switches")]),

  work=M("One patient, two thresholds.",
    """<p>A model has <var>w</var> = [%s, %s] and <var>b</var> = %s. A patient has
<var>x</var> = [%s, %s].</p>
<ol><li>Compute <var>z</var>, <var>f</var> and the class at threshold 0.5.</li>
<li>What class at threshold %s? What <var>z</var> does that threshold correspond to?</li></ol>""" % (
        n(W3[0], 1), n(W3[1], 1), n(B3, 0), n(XP3[0], 0), n(XP3[1], 1), n(T3_HIGH, 1)),
    """<ol><li><var>z</var> = %s&times;%s + (%s)&times;%s + (%s) = <b>%s</b>; <var>f</var> = <var>g</var>(%s)
&asymp; <b>%s</b>; above 0.5, so class <b>1</b>.</li>
<li>%s is below %s, so class <b>0</b>. Threshold %s corresponds to <var>z</var> = ln(%s/%s) &asymp;
<b>%s</b>: the boundary has moved, but the probability %s has not changed at all.</li></ol>""" % (
        n(W3[0], 1), n(XP3[0], 0), n(W3[1], 1), n(XP3[1], 1), n(B3, 0), n(Z3, 2), n(Z3, 2), n(F3, 3),
        n(F3, 3), n(T3_HIGH, 1), n(T3_HIGH, 1), n(T3_HIGH, 1), n(1 - T3_HIGH, 1), n(ZT3_HIGH, 3), n(F3, 3)),
    "The model gives one probability; different thresholds turn it into different decisions.",
    "The guess is &ldquo;69% sure it is a cat&rdquo;. A careful friend wants 70% before saying cat, so "
    "they say not-cat. Same guess, stricter rule.",
    [("z", "the score before squashing: w times x, plus b"),
     ("class", "the final yes/no label"),
     ("threshold", "how sure you need to be to say yes")]),

  spot=M("Three outputs read aloud. One reading is wrong.",
    """<p>A classmate reads three outputs from a logistic model (threshold 0.5):</p>
<ol><li>&ldquo;0.30: predicts class 0, and it is 70% sure of that.&rdquo;</li>
<li>&ldquo;0.50: exactly on the decision boundary.&rdquo;</li>
<li>&ldquo;0.92: there is a 92% chance this example is class 0.&rdquo;</li></ol>
<p>Which line is wrong, and what should it say?</p>""",
    """<p><b>Line 3.</b> The output is always the probability of <b>class 1</b>. 0.92 means a 92%
chance of class 1 (and 8% of class 0), so it predicts 1.</p>
<p>Lines 1 and 2 are right: 0.30 is a 70% estimate for class 0, and 0.5 is <var>z</var> = 0, the
boundary itself.</p>""",
    "The output always speaks about class 1, whatever class you end up predicting.",
    "The dial only ever measures &ldquo;how much yes&rdquo;. To get &ldquo;how much no&rdquo;, you take "
    "it away from 1.",
    [("class 1", "the &ldquo;yes&rdquo; class the model was trained to detect"),
     ("complement", "1 minus the probability &mdash; the chance of the other answer")]),

  transfer=M("A screening test that must not miss.",
    """<p>A clinic uses the model to decide who gets a follow-up scan. Missing a sick patient is far
worse than an unneeded scan. Should the threshold go up or down from 0.5? If they choose %s, where is
the new boundary in terms of <var>z</var>, and what happens to the number of people sent for scans?</p>""" % n(T3_LOW, 1),
    """<p><b>Down.</b> A lower threshold says &ldquo;yes&rdquo; more readily, so fewer sick patients
are missed, at the price of more false alarms.</p>
<p>Threshold %s means <var>z</var> = ln(%s/%s) &asymp; <b>%s</b>: the boundary shifts towards the
&ldquo;healthy&rdquo; side, and more people fall on the scan side of it. The model itself is
unchanged &mdash; you did not retrain anything.</p>""" % (
        n(T3_LOW, 1), n(T3_LOW, 1), n(1 - T3_LOW, 1), n(ZT3_LOW, 3)),
    "Choose the threshold from the cost of each kind of mistake, after training.",
    "A smoke alarm is set to beep easily. A few false beeps from toast are fine, because missing a real "
    "fire would be terrible.",
    [("false alarm", "saying yes when the true answer was no"),
     ("miss", "saying no when the true answer was yes"),
     ("retrain", "learn the weights again from data")]),
),

# =================================================================== q04
D("c1w3-q04",
  recall=M("Why logistic regression has its own loss.",
    """<p>From memory: write the logistic loss for one example with <var>y</var> = 1 and with
<var>y</var> = 0. Then give the reason squared error is not used, in one sentence that contains the
word <i>convex</i>.</p>""",
    """<p><var>y</var> = 1: &minus;log(<var>f</var>). <var>y</var> = 0: &minus;log(1 &minus; <var>f</var>).</p>
<p>With a sigmoid inside, squared error makes the cost <b>non-convex</b> in <var>w</var> and <var>b</var>
&mdash; it can have flat stretches and more than one dip &mdash; so gradient descent can stall. The
logistic loss keeps the cost <b>convex</b>: one bowl, one minimum.</p>""",
    "The log loss is chosen so the cost is one smooth bowl that gradient descent can always walk down.",
    "Rolling a ball into a bowl always ends at the bottom. On a bumpy hillside, it can get stuck in a "
    "small dip halfway down.",
    [("convex", "bowl-shaped: any straight line between two points on it lies on or above it"),
     ("loss", "the penalty for one example"),
     ("cost", "the average loss over all examples")]),

  work=M("Test convexity with three points.",
    """<p>One example: <var>x</var> = 1, <var>y</var> = 1, and no bias, so <var>f</var> = <var>g</var>(<var>w</var>).
Compare two costs at <var>w</var> = &minus;6, &minus;3 and 0:</p>
<ul><li>squared error: (<var>g</var>(<var>w</var>) &minus; 1)&sup2;</li>
<li>logistic loss: &minus;log <var>g</var>(<var>w</var>)</li></ul>
<p>A convex curve must have its value at the midpoint (&minus;3) <b>at or below</b> the average of the
two ends. Check each.</p>""",
    """<table><thead><tr><th><var>w</var></th><th>squared error</th><th>logistic loss</th></tr></thead><tbody>
%s</tbody></table>
<p>Squared error: midpoint %s, average of the ends %s. The midpoint is <b>above</b> &mdash; not
convex.</p>
<p>Logistic loss: midpoint %s, average of the ends %s. Below &mdash; consistent with a bowl.</p>""" % (
        "".join("<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (n(w, 0), n(s, 4), n(l, 4))
                for w, s, l in zip(WS4, SQ4, LG4)),
        n(SQ4[1], 4), n(SQ4_MID_AVG, 4), n(LG4[1], 4), n(LG4_MID_AVG, 4)),
    "Squared error with a sigmoid inside flattens out where the model is badly wrong; that breaks the bowl.",
    "A bowl dips in the middle. This squared-error curve bulges up in the middle instead, like a hill "
    "&mdash; so it is not a bowl.",
    [("midpoint", "the point halfway between two others"),
     ("plateau", "a flat stretch where the slope is almost zero")]),

  spot=M("&ldquo;It is a square, so it is a bowl.&rdquo;",
    """<p>The argument:</p>
<ol><li>(<var>f</var> &minus; <var>y</var>)&sup2; is a parabola in <var>f</var>, so it is convex in
<var>f</var>.</li>
<li>Therefore the squared-error cost is convex in <var>w</var> and <var>b</var>.</li>
<li>So gradient descent on squared error always finds the best logistic model.</li></ol>
<p>Which step fails?</p>""",
    """<p><b>Step 2.</b> Convex in <var>f</var> does not mean convex in <var>w</var>. Here
<var>f</var> = <var>g</var>(<var>w</var>&middot;<var>x</var> + <var>b</var>), and the sigmoid bends.
Squaring a bent function of <var>w</var> can produce bumps and flat stretches &mdash; the Work-it card
measures one.</p>
<p>For linear regression the step is fine, because there <var>f</var> is a straight-line function of
<var>w</var>.</p>""",
    "What matters is the shape with respect to the parameters, after the sigmoid has been applied.",
    "A bowl looked at through a wavy window does not look like a bowl any more. The sigmoid is the wavy "
    "window.",
    [("parameters", "the numbers being learned: w and b"),
     ("parabola", "the U-shaped curve of something squared")]),

  transfer=M("Why a confidently wrong model learns slowly with squared error.",
    """<p>Same single example (<var>x</var> = 1, <var>y</var> = 1) at <var>w</var> = &minus;6, where the
model says <var>f</var> &asymp; %s &mdash; almost certain, and wrong. Compute the slope of each cost
with respect to <var>w</var>:</p>
<ul><li>squared error: 2(<var>f</var> &minus; 1)&middot;<var>f</var>(1 &minus; <var>f</var>)</li>
<li>logistic loss: <var>f</var> &minus; 1</li></ul>
<p>What does that mean for gradient descent?</p>""" % n(S4, 4),
    """<p>Squared error: slope &asymp; <b>%s</b>. Logistic loss: slope &asymp; <b>%s</b> &mdash; about
<b>%s times</b> larger.</p>
<p>With squared error the model is stuck on a plateau exactly when it is most wrong: the
<var>f</var>(1 &minus; <var>f</var>) factor from the sigmoid is nearly zero there. The log in the
logistic loss cancels that factor, so a bad mistake produces a strong push.</p>""" % (
        n(GRAD4_SQ, 5), n(GRAD4_LOG, 4), n(RATIO4, 0)),
    "The logistic loss gives the biggest push exactly where the model is most confidently wrong.",
    "If you are very wrong, a good teacher corrects you loudly. Squared error whispers instead, just when "
    "you most need to hear it.",
    [("slope / gradient", "how steeply the cost changes, which sets the step size"),
     ("cancel", "two factors that undo each other when multiplied")]),
),

# =================================================================== q05
D("c1w3-q05",
  recall=M("Sketch the two loss curves.",
    """<p>Sketch &minus;log(<var>f</var>) (used when <var>y</var> = 1) and &minus;log(1 &minus; <var>f</var>)
(used when <var>y</var> = 0) for <var>f</var> from 0 to 1. Mark the value at the confident-and-right
end, at <var>f</var> = 0.5, and what happens at the confident-and-wrong end.</p>""",
    """<p><var>y</var> = 1: zero at <var>f</var> = 1, ln 2 &asymp; 0.693 at 0.5, and rising without
bound as <var>f</var> &rarr; 0.</p>
<p><var>y</var> = 0: the mirror image &mdash; zero at <var>f</var> = 0, rising without bound as
<var>f</var> &rarr; 1.</p>
<p>The loss is never negative.</p>""",
    "Right and sure costs nothing; wrong and sure costs without limit.",
    "Guessing right and being sure wins full marks. Saying &ldquo;I am totally sure&rdquo; and being "
    "wrong costs you more and more, with no limit.",
    [("&minus;log", "minus the log: turns a small chance into a big penalty"),
     ("without bound", "keeps growing, no ceiling")]),

  work=M("Four losses for a true positive.",
    """<p>The true label is <var>y</var> = 1. Compute the loss &minus;log(<var>f</var>) for
<var>f</var> = 0.9, 0.5, 0.1 and 0.01. How much worse is 0.01 than 0.1?</p>""",
    """<p>%s.</p>
<p>Going from 0.1 to 0.01 adds about <b>%s</b>: every factor of 10 in the wrong direction adds the
same amount, ln 10 &asymp; 2.303. The loss punishes being confidently wrong far more than being
unsure.</p>""" % (
        "; ".join("<var>f</var> = %s &rarr; <b>%s</b>" % (n(f, 2), n(l, 3)) for f, l in zip(F5, L5)),
        n(L5[3] - L5[2], 3)),
    "Each factor of ten more confidently wrong adds the same fixed amount of loss.",
    "Every time you say &ldquo;ten times more sure&rdquo; about a wrong answer, you lose another big "
    "chunk of points.",
    [("factor of 10", "ten times bigger or smaller"),
     ("ln 10", "about 2.3: the loss added per factor of ten")]),

  spot=M("The right loss for the wrong label.",
    """<p>The working for one example with true label <var>y</var> = 0 and model output
<var>f</var> = 0.95:</p>
<p>loss = &minus;log(<var>f</var>) = &minus;log(0.95) = %s. &ldquo;Tiny loss &mdash; a good
prediction.&rdquo;</p>
<p>Find the error and give the right loss.</p>""" % n(L5_BAD, 3),
    """<p>For <var>y</var> = 0 the loss is <b>&minus;log(1 &minus; <var>f</var>)</b> = &minus;log(0.05)
&asymp; <b>%s</b>. The model said 95%% chance of class 1 and the answer was 0: a confident mistake,
so a large loss.</p>
<p>The combined form &minus;<var>y</var> log <var>f</var> &minus; (1 &minus; <var>y</var>) log(1 &minus; <var>f</var>)
picks the right term automatically: with <var>y</var> = 0 the first term vanishes.</p>""" % n(L5_OK, 3),
    "Use log(f) when the answer is 1 and log(1&minus;f) when it is 0.",
    "If the right answer was &ldquo;no&rdquo;, you score how much &ldquo;no&rdquo; you said &mdash; "
    "not how much &ldquo;yes&rdquo;.",
    [("label", "the true answer for an example"),
     ("combined form", "one formula that switches between the two cases using y")]),

  transfer=M("One disaster in a hundred predictions.",
    """<p>A model sees 100 examples, all with <var>y</var> = 1. On 99 it outputs <var>f</var> = 0.99. On
one it outputs <var>f</var> = 0.0001. Compute the average loss. About how many good predictions does
that one disaster cost as much as?</p>""",
    """<p>Each good prediction: &minus;log(0.99) &asymp; %s. The disaster: &minus;log(0.0001) &asymp;
%s.</p>
<p>Average: (99 &times; %s + %s) / 100 &asymp; <b>%s</b>. The one disaster costs as much as about
<b>%s</b> good predictions &mdash; it dominates the cost.</p>
<p>That is why code clips <var>f</var> to stay a hair away from exactly 0 and 1: at exactly 0 the
loss would be infinite.</p>""" % (
        n(L5_GOOD, 5), n(L5_AWFUL, 3), n(L5_GOOD, 5), n(L5_AWFUL, 3), n(AVG5, 4), n(EQUIV5, 0)),
    "A single confident mistake can outweigh hundreds of good predictions in the average.",
    "One really loud wrong note can ruin a song that was otherwise played nicely.",
    [("average loss", "the cost: add up every loss and divide by how many"),
     ("clip", "keep a number just inside a range so the maths cannot blow up")]),
),

# =================================================================== q06
D("c1w3-q06",
  recall=M("Three fits, three names.",
    """<p>From memory: describe underfitting, a good fit and overfitting by what happens to
<b>training</b> error and to error on <b>new</b> data. Give the bias/variance name for the two
failure cases.</p>""",
    """<ul><li><b>Underfit (high bias):</b> high training error and high error on new data.</li>
<li><b>Good fit:</b> both low, and close to each other.</li>
<li><b>Overfit (high variance):</b> very low training error, much higher error on new data &mdash; a
big gap.</li></ul>""",
    "Overfitting is the gap: great on seen data, poor on unseen data.",
    "Learning the answers to last year's test by heart gets you 100% on last year's test, and not much "
    "on this year's.",
    [("bias", "the model is too simple to capture the pattern"),
     ("variance", "the model changes a lot with the exact data it saw"),
     ("generalise", "do well on examples it was not trained on")]),

  work=M("Read a real train/test table.",
    """<p>Ten training points were drawn from a smooth curve plus noise, and ten fresh test points from
the same curve. Polynomials of degree 1, 2 and 9 were fitted. Root-mean-square error:</p>
<table><thead><tr><th>degree</th><th>train</th><th>test</th></tr></thead><tbody>%s</tbody></table>
<p>Label each fit as underfit, good or overfit, with the evidence.</p>""" % "".join(
        "<tr><td>%d</td><td>%s</td><td>%s</td></tr>" % (d, n(ERR6[d][0], 3) if ERR6[d][0] > 1e-6 else "&asymp; 0",
                                                         n(ERR6[d][1], 3)) for d in (1, 2, 9)),
    """<ul><li><b>Degree 1: underfit.</b> Both errors are high (%s and %s): a line cannot bend.</li>
<li><b>Degree 2: good.</b> Lowest test error (%s), close to its training error (%s).</li>
<li><b>Degree 9: overfit.</b> Ten parameters through ten points pass through every one, so the
training error is essentially zero &mdash; and the test error is the worst of the three (%s).</li></ul>""" % (
        n(ERR6[1][0], 3), n(ERR6[1][1], 3), n(ERR6[2][1], 3), n(ERR6[2][0], 3), n(ERR6[9][1], 3)),
    "Judge a model on data it has not seen; zero training error is a warning, not a win.",
    "Drawing a line that wiggles through every single dot is easy. It just does not tell you where the "
    "next dot will land.",
    [("RMS error", "a typical size of the mistakes"),
     ("degree", "the highest power of x in the polynomial"),
     ("test data", "examples kept aside to check the model")]),

  spot=M("&ldquo;Training error is tiny, so it must be overfitting.&rdquo;",
    """<p>&ldquo;My model's training error is 0.02 and its error on new data is 0.03. A training error
that low means it has memorised the data &mdash; it is overfitting, so I will add regularisation.&rdquo;</p>
<p>Where does the reasoning go wrong?</p>""",
    """<p>&ldquo;Training error that low means overfitting&rdquo; is the error. Overfitting is a <b>gap</b>
between training and new-data error. Here they are 0.02 and 0.03 &mdash; close. This model
generalises; nothing needs fixing, and extra regularisation would only cost accuracy.</p>""",
    "Low training error alone proves nothing; look at the gap to new data.",
    "Getting full marks on homework is only a problem if you then fail the real test. If you do well on "
    "both, you just learned it.",
    [("gap", "how much worse the model does on new data than on training data"),
     ("memorise", "remember the exact examples instead of the pattern")]),

  transfer=M("Face unlock that only works indoors.",
    """<p>A face-unlock model was trained on 20 photos of each employee, all taken in the same office
under the same lights. It recognises everyone perfectly on those photos, but often fails the same
people outdoors. Underfit or overfit? What one measurement would confirm it?</p>""",
    """<p><b>Overfit</b> (high variance): it has learned details specific to the training photos &mdash;
that lighting, that background &mdash; rather than the faces.</p>
<p>Confirm it by measuring error on a <b>held-out set of new photos</b> (other places, other light):
low training error with high held-out error is the signature.</p>""",
    "If performance collapses on data unlike the training set, the model learned the setting, not the idea.",
    "If you only ever practise spelling words in one notebook, you might struggle to spell them on a "
    "different page. You learned the notebook, not the words.",
    [("held-out set", "examples kept away from training, used only to check"),
     ("high variance", "another name for overfitting")]),
),

# =================================================================== q07
D("c1w3-q07",
  recall=M("The regularized cost, and what &lambda; does.",
    """<p>Write the regularized cost for linear regression. Then say what happens to the weights, the
training error and the error on new data at <var>&lambda;</var> = 0 and at a very large
<var>&lambda;</var>.</p>""",
    """<p><var>J</var> = (1/2<var>m</var>) &Sigma;(<var>f</var> &minus; <var>y</var>)&sup2; +
(<var>&lambda;</var>/2<var>m</var>) &Sigma;<sub><var>j</var></sub> <var>w</var><sub><var>j</var></sub>&sup2;.</p>
<ul><li><var>&lambda;</var> = 0: no penalty &mdash; the ordinary fit, free to overfit.</li>
<li>Very large <var>&lambda;</var>: every weight is pushed near 0, so <var>f</var> &asymp; <var>b</var>,
a flat line. Training error rises and the model underfits.</li></ul>
<p>Error on new data traces a <b>U</b> against <var>&lambda;</var>: too small overfits, too large
underfits, the best is in between.</p>""",
    "&lambda; trades training fit for simpler weights; the best value sits at the bottom of a U.",
    "It is a lead on a dog. No lead and the dog runs everywhere; a lead that is too short and it cannot "
    "walk at all. The best lead is in between.",
    [("&lambda; (lambda)", "how strongly big weights are penalised"),
     ("penalty term", "the extra cost added for large weights"),
     ("U-shape", "goes down, reaches a lowest point, then goes back up")]),

  work=M("Add up a regularized cost.",
    """<p>A model with <var>m</var> = %d examples has three weights <var>w</var> = [%s]. Its ordinary
squared-error cost is some value <var>J</var><sub>fit</sub>. With <var>&lambda;</var> = %s, how much
does the penalty add? Which weight contributes most, and does <var>b</var> contribute anything?</p>""" % (
        M7, ", ".join(n(v, 1) for v in W7), n(LAM7, 0)),
    """<p>Penalty = <var>&lambda;</var>/(2<var>m</var>) &times; &Sigma;<var>w</var><sub><var>j</var></sub>&sup2;
= %s/%d &times; (%s) = %s/%d &times; %s = <b>%s</b>.</p>
<p>The weight 3 contributes most (9 of the %s), because squaring punishes large weights much more than
small ones. <var>b</var> contributes <b>nothing</b>: it is not in the penalty.</p>""" % (
        n(LAM7, 0), 2 * M7, " + ".join(n(v * v, 2) for v in W7), n(LAM7, 0), 2 * M7,
        n(np.sum(W7 ** 2), 2), n(PEN7, 4), n(np.sum(W7 ** 2), 2)),
    "The penalty adds &lambda;/2m times the sum of squared weights, and the largest weights dominate it.",
    "Each weight pays a tax that grows with the square of its size. Big weights pay a lot more tax than "
    "small ones.",
    [("&Sigma;w<sub>j</sub>&sup2;", "add up every weight times itself"),
     ("2m", "twice the number of examples &mdash; it keeps the scale steady")]),

  spot=M("&ldquo;Training error went up, so regularization failed.&rdquo;",
    """<p>&ldquo;I raised <var>&lambda;</var> from 1 to 100. Training error went up from 0.18 to 0.27.
So regularization made the model worse. Back to <var>&lambda;</var> = 0.&rdquo;</p>
<p>What is wrong with this conclusion?</p>""",
    """<p>Training error <b>is supposed to rise</b> as <var>&lambda;</var> grows &mdash; that is the
price paid on purpose. The decision needs error on <b>new</b> (cross-validation) data, which they did
not look at. It may have fallen, and <var>&lambda;</var> = 0 may be the overfit end of the U.</p>""",
    "Choose &lambda; by validation error, never by training error.",
    "Wearing a seatbelt makes you a tiny bit less free to move. That is not a reason to stop wearing it "
    "&mdash; you judge it by what happens in a crash.",
    [("cross-validation set", "examples used to choose settings like &lambda;"),
     ("trade-off", "giving up some of one thing to get more of another")]),

  transfer=M("A real &lambda; sweep: pick the value.",
    """<p>A degree-9 polynomial (features z-scored, <var>b</var> not penalised) was fitted to 10 training
points for each <var>&lambda;</var>. Root-mean-square errors:</p>
<table><thead><tr><th><var>&lambda;</var></th><th>train</th><th>validation</th><th>size of <var>w</var></th></tr></thead>
<tbody>%s</tbody></table>
<p>Which <var>&lambda;</var> do you pick? Describe both trends.</p>""" % "".join(
        "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (
            n(k, 3), n(SWEEP7[k][0], 4), n(SWEEP7[k][1], 4), n(SWEEP7[k][2], 2)) for k in LAMS7),
    """<p>Pick <b><var>&lambda;</var> = %s</b>, the lowest validation error (%s).</p>
<p>Training error rises steadily as <var>&lambda;</var> grows, and the weights shrink. Validation
error falls, bottoms out at %s, then rises again &mdash; the U. Left of the bottom the model is too
free; right of it, too rigid.</p>""" % (n(BEST7, 3), n(SWEEP7[BEST7][1], 4), n(BEST7, 3)),
    "Pick &lambda; at the bottom of the validation curve, not where training error is lowest.",
    "Try leads of different lengths and keep the one where the dog walks best on a new street &mdash; "
    "not the one where it does best in your own garden.",
    [("sweep", "trying a range of values one after another"),
     ("validation error", "error on data used only for choosing")]),
),

# =================================================================== q08
D("c1w3-q08",
  recall=M("The regularized update, both parameters.",
    """<p>From memory, write the regularized gradient-descent update for <var>w</var><sub><var>j</var></sub>
and for <var>b</var>. Rewrite the <var>w</var><sub><var>j</var></sub> update to show the
&ldquo;shrink, then step&rdquo; form.</p>""",
    """<p><var>w</var><sub><var>j</var></sub> &larr; <var>w</var><sub><var>j</var></sub> &minus; &alpha;[(1/<var>m</var>)&Sigma;(<var>f</var> &minus; <var>y</var>)<var>x</var><sub><var>j</var></sub>
+ (<var>&lambda;</var>/<var>m</var>)<var>w</var><sub><var>j</var></sub>]</p>
<p><var>b</var> &larr; <var>b</var> &minus; &alpha;(1/<var>m</var>)&Sigma;(<var>f</var> &minus; <var>y</var>)
&mdash; <b>no penalty term</b>.</p>
<p>Shrink form: <var>w</var><sub><var>j</var></sub> &larr; <var>w</var><sub><var>j</var></sub>(1 &minus; &alpha;<var>&lambda;</var>/<var>m</var>)
&minus; &alpha;&middot;(usual gradient).</p>""",
    "Regularization shrinks every weight a little each step; b is left alone.",
    "Each step, every weight gets trimmed a tiny bit, like a hedge. The starting height b is not "
    "trimmed &mdash; it is not a branch.",
    [("&alpha; (alpha)", "the learning rate: step size"),
     ("shrink factor", "the number just below 1 that each weight is multiplied by"),
     ("<var>b</var>", "the bias: the baseline level of the prediction")]),

  work=M("One regularized step by hand.",
    """<p>&alpha; = %s, <var>&lambda;</var> = %s, <var>m</var> = %d. Current <var>w</var> = [%s] and
<var>b</var> = %s. The ordinary (unregularized) gradients are [%s] for <var>w</var> and %s for
<var>b</var>.</p>
<ol><li>Compute the shrink factor.</li><li>Compute the new <var>w</var> and new <var>b</var>.</li></ol>""" % (
        n(A8, 1), n(LAM8, 0), M8, ", ".join(n(v, 0) for v in W8), n(B8, 0),
        ", ".join(n(v, 1) for v in G8), n(GB8, 1)),
    """<ol><li>1 &minus; &alpha;<var>&lambda;</var>/<var>m</var> = 1 &minus; %s&times;%s/%d = <b>%s</b>.</li>
<li><var>w</var> = [%s]&times;%s &minus; %s&times;[%s] = <b>[%s]</b>.
<var>b</var> = %s &minus; %s&times;%s = <b>%s</b> &mdash; no shrink factor.</li></ol>""" % (
        n(A8, 1), n(LAM8, 0), M8, n(SHRINK8, 3), ", ".join(n(v, 0) for v in W8), n(SHRINK8, 3),
        n(A8, 1), ", ".join(n(v, 1) for v in G8), ", ".join(n(v, 3) for v in NEWW8),
        n(B8, 0), n(A8, 1), n(GB8, 1), n(NEWB8, 3)),
    "Multiply each weight by the shrink factor, then take the usual step; b only takes the usual step.",
    "First everyone's height gets trimmed by 5%, then they each take their normal step. The baseline "
    "skips the trim.",
    [("update", "replacing the old value with the new one"),
     ("unregularized gradient", "the slope from the data alone, before the penalty")]),

  spot=M("One extra line in the gradient code.",
    """<p>Regularized gradient code (linear model):</p>%s
<p>Which line is wrong, and what does it do to the predictions?</p>""" % code(
        "err = X @ w + b - y\n"
        "dj_dw = (X.T @ err) / m + (lambda_ / m) * w\n"
        "dj_db = np.sum(err) / m + (lambda_ / m) * b"),
    """<p>The <b><code>dj_db</code></b> line: <var>b</var> must not be penalised. The penalty would
drag <var>b</var> towards 0, which shifts <b>every</b> prediction towards 0 for no gain &mdash;
<var>b</var> sets the overall level, not the sensitivity to any feature.</p>
<p>Fix: <code>dj_db = np.sum(err) / m</code>.</p>""",
    "Only the weights are penalised; penalising b biases every prediction.",
    "The trim is for the branches that stick out, not for the ground the hedge stands on. Lower the "
    "ground and the whole hedge sinks.",
    [("<code>lambda_</code>", "the code name for &lambda; (lambda is a reserved word in Python)"),
     ("bias the predictions", "push them all in one direction")]),

  transfer=M("Body temperature in Kelvin.",
    """<p>A model predicts body temperature in Kelvin (around %s K) from %d patients. The features are
zero-mean, so without a penalty <var>b</var> ends up at the average, %s. If someone wrongly penalised
<var>b</var> with <var>&lambda;</var> = %s, <var>b</var> would settle at <var>m</var>&middot;<span>y&#772;</span>/(<var>m</var> + <var>&lambda;</var>).
What would that be, and why is it absurd?</p>""" % (n(YBAR8, 0), M8b, n(YBAR8, 0), n(LAM8b, 0)),
    """<p><var>b</var> = %d &times; %s / (%d + %s) &asymp; <b>%s K</b> &mdash; about %s degrees too cold for
every patient.</p>
<p>The penalty has nothing to do with overfitting here; it just drags the baseline towards zero. And
it would give a different model in Celsius, where zero is somewhere else. Leaving <var>b</var>
unpenalised makes the fit independent of where zero happens to be.</p>""" % (
        M8b, n(YBAR8, 0), M8b, n(LAM8b, 0), n(BPEN8, 1), n(YBAR8 - BPEN8, 0)),
    "b carries the level of the target; penalising it ties the model to an arbitrary zero point.",
    "If a rule said &ldquo;everyone's height must be pulled towards the floor&rdquo;, it would be silly: "
    "the floor is just where you started measuring.",
    [("Kelvin", "a temperature scale that starts at absolute zero; the body is about 310"),
     ("<span>y&#772;</span> (y-bar)", "the average of the targets")]),
),

# =================================================================== q09
D("c1w3-q09",
  recall=M("The logistic update, and why it looks familiar.",
    """<p>Write the gradient-descent updates for logistic regression. What is <var>f</var> here, and what
is the one difference from linear regression's updates?</p>""",
    """<p><var>w</var><sub><var>j</var></sub> &larr; <var>w</var><sub><var>j</var></sub> &minus; &alpha;(1/<var>m</var>)&Sigma;(<var>f</var> &minus; <var>y</var>)<var>x</var><sub><var>j</var></sub>;
<var>b</var> &larr; <var>b</var> &minus; &alpha;(1/<var>m</var>)&Sigma;(<var>f</var> &minus; <var>y</var>).</p>
<p>Here <var>f</var> = <var>g</var>(<var>w</var>&middot;<var>x</var> + <var>b</var>). The expressions are
<b>identical</b> to linear regression's; only the definition of <var>f</var> differs. The sigmoid's
derivative cancels against the log in the loss.</p>""",
    "Same update formula as linear regression, with f passed through the sigmoid.",
    "Two recipes with the same steps, but one uses a different first ingredient. You follow the same "
    "instructions either way.",
    [("update rule", "how the weights change on each step"),
     ("(f &minus; y)", "the error: prediction minus truth")]),

  work=M("One logistic gradient step on three examples.",
    """<p>One feature: <var>x</var> = [%s], <var>y</var> = [%s]. Current <var>w</var> = %s,
<var>b</var> = %s, &alpha; = %s. Compute the predictions, the errors, both gradients, and the new
<var>w</var> and <var>b</var>.</p>""" % (
        ", ".join(n(v, 1) for v in X9), ", ".join(n(v, 0) for v in Y9), n(W9, 1), n(B9, 1), n(A9, 1)),
    """<p><var>z</var> = <var>w</var><var>x</var> + <var>b</var> = [%s], so <var>f</var> = [%s].</p>
<p>Errors <var>f</var> &minus; <var>y</var> = [%s].</p>
<p>&part;J/&part;<var>w</var> = mean(error &times; <var>x</var>) = <b>%s</b>;
&part;J/&part;<var>b</var> = mean(error) = <b>%s</b>.</p>
<p>New <var>w</var> = %s &minus; %s&times;(%s) = <b>%s</b>; new <var>b</var> = %s &minus; %s&times;(%s) =
<b>%s</b>.</p>""" % (
        ", ".join(n(v, 3) for v in W9 * X9 + B9), ", ".join(n(v, 4) for v in F9),
        ", ".join(n(v, 4) for v in E9), n(DW9, 4), n(DB9, 4),
        n(W9, 1), n(A9, 1), n(DW9, 4), n(NW9, 4), n(B9, 1), n(A9, 1), n(DB9, 4), n(NB9, 4)),
    "Squash, subtract the truth, average error times x: that is the whole step.",
    "Make a guess, see how far off each guess was, then nudge the knob in the direction that would have "
    "made the guesses better.",
    [("mean", "add up and divide by how many"),
     ("&part;J/&part;w", "how the cost changes when w changes")]),

  spot=M("An extra sigmoid-derivative factor.",
    """<p>A teammate &ldquo;derived&rdquo; the logistic gradient as:</p>%s
<p>On the Work-it data (<var>x</var> = [%s], <var>y</var> = [%s], <var>w</var> = %s, <var>b</var> = %s)
it gives %s instead of %s. Which is right, and where does the extra factor come from?</p>""" % (
        code("f = 1 / (1 + np.exp(-(w * x + b)))\n"
             "dj_dw = np.mean((f - y) * f * (1 - f) * x)"),
        ", ".join(n(v, 1) for v in X9), ", ".join(n(v, 0) for v in Y9), n(W9, 1), n(B9, 1),
        n(DW9_WRONG, 4), n(DW9, 4)),
    """<p><b>%s</b> is right: <code>np.mean((f - y) * x)</code>. The <code>f * (1 - f)</code> factor is
the sigmoid's derivative, and it belongs to the gradient of <b>squared error</b> with a sigmoid
inside. With the logistic loss it cancels against the derivative of the log, leaving just
(<var>f</var> &minus; <var>y</var>)<var>x</var>.</p>
<p>The extra factor is also why squared error learns slowly when the model is confidently wrong:
<var>f</var>(1 &minus; <var>f</var>) is near zero there.</p>""" % n(DW9, 4),
    "With the logistic loss, the sigmoid's derivative cancels; adding it back computes the wrong gradient.",
    "Two things that undo each other were both kept in by mistake &mdash; like adding salt to a recipe "
    "that already counted it.",
    [("derivative", "the slope of a function at a point"),
     ("cancel", "multiply by something and divide by the same thing")]),

  transfer=M("Turn working linear-regression code into logistic.",
    """<p>Your linear-regression training loop works: it computes predictions, the gradient lines for
<var>w</var> and <var>b</var>, and prints the squared-error cost every 100 steps. What is the minimum
set of changes to train logistic regression instead?</p>""",
    """<ol><li>Predictions: wrap them in the sigmoid, <code>f = 1 / (1 + np.exp(-(X @ w + b)))</code>.</li>
<li>The printed cost: switch to the logistic loss, so the curve you watch means something.</li></ol>
<p>The two gradient lines and the update lines stay <b>exactly as they are</b>. The targets must be 0/1
labels.</p>""",
    "Change how f is computed (and what you monitor); the gradient and update code are reused unchanged.",
    "You keep the same bike and the same pedalling. You only swap the front wheel.",
    [("training loop", "the repeated steps that adjust the weights"),
     ("monitor", "keep watching a number to see that training is working")]),
),

# =================================================================== q10
D("c1w3-q10",
  recall=M("Three fixes for overfitting, and two non-fixes.",
    """<p>From memory: list three ways to reduce overfitting, and say what each gives up. Then name two
actions that look helpful and make overfitting <b>worse</b>.</p>""",
    """<p><b>Fixes:</b> collect more data (costs time and money); use fewer features or a lower
polynomial degree (throws information away); regularize, i.e. increase <var>&lambda;</var> (keeps
every feature, shrinks the weights).</p>
<p><b>Make it worse:</b> decreasing <var>&lambda;</var>, and adding more features or higher
powers. (Training for more iterations does not fix it either &mdash; the training fit is already too
good.)</p>""",
    "Overfitting is fixed by less freedom or more data; never by more freedom.",
    "If a puppy runs wild, you can give it more space to learn the rules (more data), fewer toys (fewer "
    "features), or a lead (regularization). Taking the lead off does not help.",
    [("capacity", "how complicated a pattern the model can represent"),
     ("feature selection", "keeping only some of the input columns")]),

  work=M("Count the features a polynomial creates.",
    """<p>You have two raw measurements, <var>x</var><sub>1</sub> and <var>x</var><sub>2</sub>. Mapping
them to <b>every</b> polynomial term up to degree <var>d</var> (<var>x</var><sub>1</sub>,
<var>x</var><sub>2</sub>, <var>x</var><sub>1</sub>&sup2;, <var>x</var><sub>1</sub><var>x</var><sub>2</sub>,
&hellip;) creates how many features for <var>d</var> = 2, 3 and 6? (The count of terms of degree 1
to <var>d</var> in two variables is (<var>d</var>+1)(<var>d</var>+2)/2 &minus; 1.)</p>""",
    """<p><var>d</var> = 2: <b>%d</b>. <var>d</var> = 3: <b>%d</b>. <var>d</var> = 6: <b>%d</b>.</p>
<p>Going from degree 2 to degree 6 multiplies the number of weights by more than five. With only a
few dozen examples, %d free weights can fit the noise &mdash; which is why the degree is a lever on
overfitting, and why regularization is used alongside high-degree features.</p>""" % (
        NF10_2, NF10_3, NF10_6, NF10_6),
    "Raising the polynomial degree adds features fast, and every feature is more room to overfit.",
    "Each new power is another dial to turn. With lots of dials and only a few examples, you can twist "
    "them until they fit anything &mdash; even the mistakes.",
    [("polynomial term", "a product of the inputs raised to powers, like x<sub>1</sub>&sup2;x<sub>2</sub>"),
     ("degree", "the highest total power allowed")]),

  spot=M("A remedy list with one step backwards.",
    """<p>The model fits training data almost perfectly and does badly on new data. More data is not
available. A plan:</p>
<ol><li>Increase <var>&lambda;</var> and check validation error.</li>
<li>If still overfitting, drop the degree from 6 to 3.</li>
<li>Train for twice as many iterations so the weights settle properly.</li>
<li>Re-check validation error after each change.</li></ol>
<p>Which step works against the goal?</p>""",
    """<p><b>Step 3.</b> The training fit is already too good. More iterations push the model even
closer to the training data &mdash; the wrong direction. Steps 1, 2 and 4 each reduce the model's
freedom or measure the effect, which is right.</p>""",
    "When the model already fits training data too well, more training does not help.",
    "If you have already memorised last year's test, reading it ten more times will not help with this "
    "year's.",
    [("validation error", "error on data used to check changes"),
     ("iterations", "how many update steps gradient descent takes")]),

  transfer=M("Three options, three costs.",
    """<p>A defect classifier uses %d polynomial features built from 2 sensor readings and has 40
training examples. Training accuracy is 100%%, validation accuracy is 61%%. Three options: (a) add
<var>&lambda;</var>; (b) drop to degree 2 (%d features); (c) wait a month for 400 more examples. Which
do you try first, and what does each cost?</p>""" % (NF10_6, NF10_2),
    """<p>Try <b>(a) first</b>: it is cheap, reversible, and keeps all %d features &mdash; you just tune
<var>&lambda;</var> on the validation set.</p>
<p>(b) is also cheap but throws away the higher-order terms permanently; worth it if
<var>&lambda;</var> alone does not close the gap. (c) is the most reliable fix for high variance, but
costs a month.</p>
<p>All three target the same symptom; none of them is &ldquo;train longer&rdquo; or &ldquo;decrease
<var>&lambda;</var>&rdquo;.</p>""" % NF10_6,
    "Start with the cheapest reversible fix for high variance, measure, then escalate.",
    "If your bike wobbles, first try lowering the seat a bit. If that is not enough, swap the wheel. "
    "Buying a new bike works too, but takes much longer.",
    [("reversible", "you can undo it easily"),
     ("high variance", "the overfitting symptom: great on training, poor on new data")]),
),
]
