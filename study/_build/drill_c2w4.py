# -*- coding: utf-8 -*-
"""Quiz drills — C2 W4. One concept per mock-quiz question, four methods each.

Every number below is COMPUTED here at import time and formatted into the text,
never typed. If a value is wrong, it is wrong in the arithmetic, where you can
see it, not in a sentence.
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


def big(x):
    return "{:,.0f}".format(x)


def H(p):
    """Two-class entropy in bits, with the 0 log 0 = 0 convention."""
    if p <= 0 or p >= 1:
        return 0.0
    return float(-p * np.log2(p) - (1 - p) * np.log2(1 - p))


def Hy(y):
    y = np.asarray(y, dtype=float)
    return 0.0 if len(y) == 0 else H(y.mean())


def gain(y, mask):
    """Weighted information gain of splitting y by a boolean mask."""
    y = np.asarray(y, dtype=float)
    left, right = y[mask], y[~mask]
    return Hy(y) - (len(left) / len(y) * Hy(left) + len(right) / len(y) * Hy(right))


def var_red(y, mask):
    y = np.asarray(y, dtype=float)
    left, right = y[mask], y[~mask]
    return np.var(y) - (len(left) / len(y) * np.var(left) + len(right) / len(y) * np.var(right))


def best_stump(x, y):
    """Best single threshold on x by variance reduction: (t, left mean, right mean)."""
    xs = np.unique(x)
    best = None
    for i in range(1, len(xs)):
        t = (xs[i - 1] + xs[i]) / 2
        r = var_red(y, x <= t)
        if best is None or r > best[0] + 1e-12:
            best = (r, t, y[x <= t].mean(), y[x > t].mean())
    return best[1], best[2], best[3]


# ---------------------------------------------------------------- q01 entropy
MIX1 = [(10, 0), (7, 3), (3, 7), (9, 1), (5, 5)]
H1 = [H(a / (a + b)) for a, b in MIX1]
with np.errstate(divide="ignore", invalid="ignore"):
    _p = 1.0
    NAIVE1 = -_p * np.log2(_p) - (1 - _p) * np.log2(1 - _p)
P4 = np.array([0.25, 0.25, 0.25, 0.25])
H4 = float(-np.sum(P4 * np.log2(P4)))
P2of4 = np.array([0.5, 0.5])
H2of4 = float(-np.sum(P2of4 * np.log2(P2of4)))
P_SKEW4 = np.array([0.7, 0.1, 0.1, 0.1])
H_SKEW4 = float(-np.sum(P_SKEW4 * np.log2(P_SKEW4)))

# ---------------------------------------------------------------- q02 weighting
Y2 = np.array([1.] * 10 + [0.] * 10)
# split A: a tiny pure leaf of 2 positives; the other 18 hold 8 positives, 10 negatives
A2 = np.zeros(20, dtype=bool); A2[:2] = True
# split B: 10 / 10, with 8 and 2 positives
B2 = np.zeros(20, dtype=bool); B2[:8] = True; B2[10:12] = True
HA_L, HA_R = Hy(Y2[A2]), Hy(Y2[~A2])
HB_L, HB_R = Hy(Y2[B2]), Hy(Y2[~B2])
GA_W, GB_W = gain(Y2, A2), gain(Y2, B2)
GA_U = Hy(Y2) - (HA_L + HA_R) / 2
GB_U = Hy(Y2) - (HB_L + HB_R) / 2
# transfer: two classes' pass rates
NA_T, RA_T, NB_T, RB_T = 3, 1.0, 30, 0.5
UNW_T = (RA_T + RB_T) / 2
W_T = (NA_T * RA_T + NB_T * RB_T) / (NA_T + NB_T)

# ---------------------------------------------------------------- q03 greedy
NF3 = 10
GREEDY_D2 = NF3 + 2 * (NF3 - 1)
EXH_D2 = NF3 * (NF3 - 1) ** 2
EXH_D3 = NF3 * (NF3 - 1) ** 2 * (NF3 - 2) ** 4
# XOR: neither feature helps alone, both together are perfect
X3a = np.array([0, 0, 1, 1, 0, 0, 1, 1]); X3b = np.array([0, 1, 0, 1, 0, 1, 0, 1])
Y3 = (X3a != X3b).astype(float)
G3a, G3b = gain(Y3, X3a == 1), gain(Y3, X3b == 1)
_left = X3a == 0
G3_DEPTH2_L = gain(Y3[_left], X3b[_left] == 1)
G3_DEPTH2_R = gain(Y3[~_left], X3b[~_left] == 1)
# instability: one added row flips the root
GA3 = np.array([0, 0, 0, 0, 1, 1, 0, 0, 0, 0])
GB3 = np.array([0, 1, 1, 1, 1, 0, 0, 0, 0, 0])
YI3 = np.array([1, 1, 0, 0, 1, 1, 0, 1, 1, 1])
GAIN_A0, GAIN_B0 = gain(YI3, GA3 == 1), gain(YI3, GB3 == 1)
GA3b, GB3b, YI3b = np.append(GA3, 0), np.append(GB3, 0), np.append(YI3, 1)
GAIN_A1, GAIN_B1 = gain(YI3b, GA3b == 1), gain(YI3b, GB3b == 1)

# ---------------------------------------------------------------- q04 regression trees
Y4 = np.array([150., 160, 170, 300, 320, 340])
V4 = np.var(Y4)
S4a = np.array([True, True, True, False, False, False])     # tight groups
S4b = np.array([True, False, False, True, False, True])     # same sizes, mixed
VR4a, VR4b = var_red(Y4, S4a), var_red(Y4, S4b)
VA_L, VA_R = np.var(Y4[S4a]), np.var(Y4[~S4a])
MA_L, MA_R = Y4[S4a].mean(), Y4[~S4a].mean()
S4c = np.array([True, True, False, False, False, False])
VR4c = var_red(Y4, S4c)
# entropy that treats every price as its own class
HC_ROOT = np.log2(6)
HC_CHILD = np.log2(3)
GC = HC_ROOT - HC_CHILD     # same for ANY 3 / 3 split of six distinct prices
DEPTH4 = 3
LEAVES4 = 2 ** DEPTH4

# ---------------------------------------------------------------- q05 extrapolation
X5 = np.array([100., 150, 200, 250, 300, 400])
Y5 = 2 * X5 + 50
T5, L5, R5 = best_stump(X5, Y5)
LIN5 = np.polyfit(X5, Y5, 1)
XQ5 = 2000.0
LINQ5 = np.polyval(LIN5, XQ5)
# a forest of stumps, each on a bootstrap sample: its predictions stay inside [min y, max y]
_rng5 = np.random.default_rng(5)
_preds = []
for _ in range(200):
    _idx = _rng5.integers(0, len(X5), len(X5))
    if len(np.unique(X5[_idx])) < 2:
        continue
    _t, _l, _r = best_stump(X5[_idx], Y5[_idx])
    _preds.append(_r if XQ5 > _t else _l)
FOREST5 = float(np.mean(_preds))
YMAX5 = Y5.max()
# trend transfer: 24 months growing 5% a month
MONTHS5 = np.arange(1, 25)
SALES5 = 100 * 1.05 ** (MONTHS5 - 1)
LAST5 = SALES5[-1]
TRUE30 = 100 * 1.05 ** 29

# ---------------------------------------------------------------- q06 bootstrap
MS6 = [2, 5, 10, 100, 1000]
UNIQ6 = [1 - (1 - 1 / m) ** m for m in MS6]
LIMIT6 = 1 - math.exp(-1)
_rng6 = np.random.default_rng(6)
_fr = []
for _ in range(20000):
    _fr.append(len(np.unique(_rng6.integers(0, 10, 10))) / 10)
SIM6 = float(np.mean(_fr))
_rng6b = np.random.default_rng(7)
ONE_BAG6 = np.sort(_rng6b.integers(0, 10, 10)) + 1
ONE_BAG_UNIQ6 = len(np.unique(ONE_BAG6))
NOREP6 = len(np.unique(_rng6b.permutation(10))) / 10
NPAT6, NTREE6 = 300, 100
OOB_TREES6 = NTREE6 * (1 - 1 / NPAT6) ** NPAT6

# ---------------------------------------------------------------- q07 random forests
NF7, K7 = 16, 4
P_AVAIL7 = K7 / NF7
NTREES7 = 500
ROOT_DOM7 = NTREES7 * P_AVAIL7
NF7b = 100
K7b = math.isqrt(NF7b)
SIG7 = 1.0


def forest_var(rho, b):
    return rho * SIG7 + (1 - rho) * SIG7 / b


FV_HI_500, FV_HI_1000 = forest_var(0.9, 500), forest_var(0.9, 1000)
FV_LO_500 = forest_var(0.3, 500)

# ---------------------------------------------------------------- q08 boosting
X8 = np.array([1., 2, 3, 4, 5, 6])
Y8 = np.array([3., 4, 9, 10, 15, 16])
ETA8 = 0.5
_pred = np.full(len(Y8), Y8.mean())
SSE8 = [float(np.sum((Y8 - _pred) ** 2))]
ROUNDS8 = []
for _ in range(3):
    _res = Y8 - _pred
    _t, _l, _r = best_stump(X8, _res)
    ROUNDS8.append((_t, _l, _r))
    _pred = _pred + ETA8 * np.where(X8 <= _t, _l, _r)
    SSE8.append(float(np.sum((Y8 - _pred) ** 2)))
PRED8 = _pred
INIT8 = Y8.mean()
RES8_0 = Y8 - INIT8
# the bug: every round fits y itself, not the residual
_bug = np.zeros(len(Y8))
for _ in range(4):
    _t, _l, _r = best_stump(X8, Y8)
    _bug = _bug + ETA8 * np.where(X8 <= _t, _l, _r)
BUG8 = _bug
# transfer: learning rate vs number of trees on data a stump fits exactly
T8_01 = math.ceil(math.log(0.01) / math.log(1 - 0.1))
T8_005 = math.ceil(math.log(0.01) / math.log(1 - 0.05))

# ---------------------------------------------------------------- q09 choosing a model
NUM9 = 12
CATS9 = [5, 40, 200]
WIDTH9 = NUM9 + sum(CATS9)
X9 = np.array([2., 5, 7, 11, 13, 20]); Y9 = np.array([0., 0, 1, 1, 0, 1])


def best_gain(x, y):
    xs = np.unique(x)
    best = (0.0, None)
    for i in range(1, len(xs)):
        t = (xs[i - 1] + xs[i]) / 2
        g = gain(y, x <= t)
        if g > best[0] + 1e-12:
            best = (g, t)
    return best


G9, T9 = best_gain(X9, Y9)
G9s, T9s = best_gain(X9 * 1000, Y9)
G9l, T9l = best_gain(np.log(X9), Y9)
ORDERS9 = math.factorial(30)
ORD_EXP9 = len(str(ORDERS9)) - 1
ORD_MANT9 = ORDERS9 / 10 ** ORD_EXP9

# ---------------------------------------------------------------- q10 high-cardinality
Y10 = np.array([1., 1, 1, 0, 0, 0, 0, 0])
H10 = Hy(Y10)
ID10 = np.arange(8)
GID10 = H10                      # every leaf holds one row, so every leaf is pure
REAL10 = np.array([True, True, True, True, False, False, False, False])
Y10r = np.array([1., 1, 1, 0, 0, 0, 0, 0])
GREAL10 = gain(Y10r, REAL10)
ROWS10, PC10 = 40000, 3000
PER10 = ROWS10 / PC10


def _row(vals, d=3):
    return "[" + ", ".join(n(v, d) for v in vals) + "]"


def _ints(vals):
    return "[" + ", ".join("%d" % v for v in vals) + "]"


DRILLS = [

# =================================================================== q01
D("c2w4-q01",
  recall=M("The entropy formula and its three landmark values.",
    """<p>From a blank page: write the two-class entropy <var>H</var>(<var>p</var>), say what
<var>p</var> is, and give <var>H</var> at <var>p</var> = 0, 0.5 and 1. Why is
<var>H</var>(0.8) the same as <var>H</var>(0.2)?</p>""",
    """<p><var>H</var>(<var>p</var>) = &minus;<var>p</var> log<sub>2</sub>(<var>p</var>) &minus;
(1 &minus; <var>p</var>) log<sub>2</sub>(1 &minus; <var>p</var>), where <var>p</var> is the fraction
of the node in one class.</p>
<ul><li><var>H</var>(0) = 0 and <var>H</var>(1) = 0: a pure node, no uncertainty.</li>
<li><var>H</var>(0.5) = 1: the most mixed a two-class node can be.</li></ul>
<p>The formula is symmetric in <var>p</var> and 1 &minus; <var>p</var>. Entropy measures <b>how
mixed</b> a node is, not which class is winning.</p>""",
    "Entropy is 0 when a group is all one kind and 1 when it is a perfect half-and-half mix.",
    "If every sweet in the bag is a lemon one, you know exactly what you will pull out: no surprise. "
    "If half are lemon and half are cherry, every pull is a surprise. Entropy is how surprised you "
    "expect to be.",
    [("entropy", "a number for how mixed up a group is"),
     ("pure node", "a group where every example is the same class"),
     ("log<sub>2</sub>", "the logarithm in base 2, which makes the answer come out in bits")]),

  work=M("Five nodes, five entropies.",
    """<p>Compute <var>H</var> for nodes with these (cats, dogs) counts:
%s.</p><p>Which two come out equal, and why?</p>""" % ", ".join("(%d, %d)" % ab for ab in MIX1),
    """<ul>%s</ul>
<p>(7, 3) and (3, 7) are equal: the mix is the same, only the majority has swapped. (10, 0) is pure;
(5, 5) is the maximum. Note how fast <var>H</var> rises: a node that is 90%% one class still has
entropy %s, not 0.1.</p>""" % (
        "".join("<li>(%d, %d): <var>p</var> = %s, <var>H</var> = <b>%s</b></li>"
                % (a, b, n(a / (a + b), 1), n(h, 3)) for (a, b), h in zip(MIX1, H1)),
        n(H1[3], 3)),
    "Entropy depends only on the mix, and it climbs steeply as soon as a node stops being pure.",
    "A bag with one dog among nine cats is still quite a surprising bag, more than you might guess.",
    [("p", "the fraction of the group in one class"),
     ("bits", "the unit entropy comes out in when the log is base 2")]),

  spot=M("A pure node that comes out as nan.",
    """<p>Someone codes entropy straight from the formula and tests it on a pure node:</p>%s
<p>It prints <code>%s</code> with a warning. Where is the mistake, and what should a pure node give?</p>""" % (
        code("p = 1.0\nH = -p * np.log2(p) - (1 - p) * np.log2(1 - p)"), NAIVE1),
    """<p>The second term is 0 &times; log<sub>2</sub>(0) = 0 &times; (&minus;&infin;), which the computer
calls <code>nan</code>. But the formula is meant to use the convention <b>0 log 0 = 0</b> &mdash;
the limit of <var>p</var> log <var>p</var> as <var>p</var> shrinks to 0.</p>
<p>A pure node should give <b>0</b>. The fix is to return 0 whenever <var>p</var> is 0 or 1 before
taking any logs.</p>""",
    "A class with no members contributes nothing to entropy, even though log 0 is not a number.",
    "If there are no cherry sweets at all, they cannot surprise you. The formula needs to be told "
    "that, because on its own it trips over the empty group.",
    [("nan", "&ldquo;not a number&rdquo; &mdash; what a computer gives for 0 times infinity"),
     ("convention", "an agreed rule for an edge case"),
     ("limit", "the value something heads towards as you get closer and closer")]),

  transfer=M("Four classes instead of two: is the maximum still 1?",
    """<p>A fruit-sorting node holds four kinds of fruit. Entropy generalises to
<var>H</var> = &minus;&Sigma; <var>p</var><sub>k</sub> log<sub>2</sub> <var>p</var><sub>k</sub>.
Compute it for an equal four-way mix, for a node with only two kinds in equal amounts, and for
70%% / 10%% / 10%% / 10%%. Is 1 still the ceiling?</p>""",
    """<ul><li>Four equal kinds: <var>H</var> = <b>%s</b> bits.</li>
<li>Two equal kinds: <var>H</var> = <b>%s</b> bit.</li>
<li>70 / 10 / 10 / 10: <var>H</var> &asymp; <b>%s</b> bits.</li></ul>
<p>No: with <var>k</var> classes the ceiling is log<sub>2</sub> <var>k</var>, so 2 bits for four. The
&ldquo;between 0 and 1&rdquo; rule is a two-class fact, not a property of entropy.</p>""" % (
        n(H4, 3), n(H2of4, 3), n(H_SKEW4, 3)),
    "Entropy's maximum grows with the number of classes: log base 2 of how many there are.",
    "Guessing a fruit from four kinds is harder than guessing a coin from two sides, so the "
    "surprise score can go higher.",
    [("multi-class", "more than two possible answers"),
     ("&Sigma;", "add up over every class"),
     ("ceiling", "the largest value something can reach")]),
),

# =================================================================== q02
D("c2w4-q02",
  recall=M("Write information gain with its weights.",
    """<p>From memory, write the information gain of a split, name each weight, and say in one
sentence what would go wrong without the weights.</p>""",
    """<p>Gain = <var>H</var>(root) &minus; ( <var>w</var><sup>left</sup> <var>H</var>(left) +
<var>w</var><sup>right</sup> <var>H</var>(right) ), where <var>w</var><sup>left</sup> is the
<b>fraction of the node's examples</b> that go left, and likewise right.</p>
<p>Without the weights, a tiny pure child would count as much as a huge messy one, so splits
that peel off two or three examples would look brilliant.</p>""",
    "Gain is the drop in entropy, with each child counted in proportion to how many examples it holds.",
    "If you tidy one sock drawer out of ten, the bedroom is not nine-tenths tidier. You have to count "
    "how much of the room each drawer is.",
    [("information gain", "how much a split reduces the mess"),
     ("w<sup>left</sup>", "the share of examples that went to the left child"),
     ("weighted average", "an average where bigger groups count for more")]),

  work=M("Two splits, scored with and without weights.",
    """<p>A node has 20 examples, 10 positive. Two candidate splits:</p>
<ul><li><b>A</b>: left 2 (both positive), right 18 (8 positive).</li>
<li><b>B</b>: left 10 (8 positive), right 10 (2 positive).</li></ul>
<p>Compute each split's gain properly, then again with a plain average of the two child entropies.
Which split does each version choose?</p>""",
    """<p>Root entropy = %s. Child entropies: A gives %s and %s; B gives %s and %s.</p>
<ul><li><b>Weighted</b>: A gains %s, B gains <b>%s</b> &rarr; picks <b>B</b>.</li>
<li><b>Plain average</b>: A &ldquo;gains&rdquo; <b>%s</b>, B gains %s &rarr; picks <b>A</b>.</li></ul>
<p>The unweighted version is fooled by A's two-example pure leaf; the other 18 examples are left
almost as mixed as before.</p>""" % (
        n(Hy(Y2), 3), n(HA_L, 3), n(HA_R, 3), n(HB_L, 3), n(HB_R, 3),
        n(GA_W, 3), n(GB_W, 3), n(GA_U, 3), n(GB_U, 3)),
    "Weighting by size stops a tiny tidy corner from outscoring a split that tidies everything.",
    "Sorting two toys perfectly and leaving eighteen in a heap is not better than sorting all twenty "
    "pretty well.",
    [("candidate split", "one possible question the tree could ask here"),
     ("child entropy", "how mixed one side is after the split")]),

  spot=M("A gain function with a /2 where a weight belongs.",
    """<p>A from-scratch implementation:</p>%s
<p>It runs, and every gain looks plausible. Which part is wrong, and what does it do to split A
above?</p>""" % code("def gain(y, left, right):\n"
                       "    return entropy(y) - (entropy(left) + entropy(right)) / 2"),
    """<p>The <code>/ 2</code> treats both children as equally important. It should weight each by
its share: <code>len(left) / len(y)</code> and <code>len(right) / len(y)</code>.</p>
<p>On split A it reports %s instead of %s &mdash; and the tree would pick A, isolating two examples
and learning almost nothing. Nothing crashes; the bug only shows on new data.</p>""" % (
        n(GA_U, 3), n(GA_W, 3)),
    "A plain average of child entropies is a silent bug: it trains, scores well, and generalises badly.",
    "It is like saying a class of 2 and a class of 30 count the same when you work out the whole "
    "school's score.",
    [("len(left)", "how many examples went to the left side"),
     ("silent bug", "a mistake that gives no error, just a worse answer")]),

  transfer=M("The same weighting, in a school report.",
    """<p>Class A has %d students and %s%% passed. Class B has %d students and %s%% passed. The
head reports the school's pass rate as the average of the two class rates. What is wrong, what is
the real rate, and how is this the same mistake as unweighted information gain?</p>""" % (
        NA_T, n(RA_T * 100, 0), NB_T, n(RB_T * 100, 0)),
    """<p>The average of the rates is %s%%, but only %d of %d students passed: the real rate is
<b>%s%%</b>. The tiny perfect class is counted as if it were as big as the large one.</p>
<p>Information gain has exactly this shape: an average of child scores, which must be weighted by
how many examples each child holds.</p>""" % (
        n(UNW_T * 100, 1), int(NA_T * RA_T + NB_T * RB_T), NA_T + NB_T, n(W_T * 100, 1)),
    "Whenever you average averages, weight each one by how many things it summarises.",
    "Three kids all getting full marks does not make the whole school brilliant if thirty other kids "
    "only got half.",
    [("pass rate", "the share of students who passed"),
     ("average of averages", "averaging group scores without counting how big each group is")]),
),

# =================================================================== q03
D("c2w4-q03",
  recall=M("The tree-building loop, and what greedy means.",
    """<p>From memory: write the steps of building a decision tree, three ways it stops, and what
&ldquo;greedy&rdquo; means here.</p>""",
    """<ol><li>At the current node, score every feature's split by information gain.</li>
<li>Split on the best one.</li><li>Repeat on each child.</li></ol>
<p>Stop when a node is pure, when a maximum depth is reached, when too few examples remain, or when
the best gain is below a threshold.</p>
<p><b>Greedy</b>: take the split that looks best <i>now</i> and never revisit it. No lookahead, no
undoing.</p>""",
    "The tree picks the best question one node at a time and never goes back to change an earlier one.",
    "It is like choosing each step of a walk by whichever path looks most downhill right now, never "
    "checking the map for a better route.",
    [("greedy", "always taking the best-looking choice right now"),
     ("recursion", "doing the same job again on each smaller piece"),
     ("stopping criterion", "the rule that says when to stop splitting")]),

  work=M("Count what greedy checks against what exhaustive would.",
    """<p>There are %d yes/no features. A depth-2 tree uses one feature at the root and one in each
child (never repeating a feature down a path).</p>
<ol><li>How many gain computations does greedy make to build it?</li>
<li>How many different depth-2 trees exist? And depth-3 trees?</li></ol>""" % NF3,
    """<ol><li>%d at the root, then %d in each of 2 children: <b>%s</b>.</li>
<li>Depth 2: %d &times; %d &times; %d = <b>%s</b>. Depth 3: %d &times; %d<sup>2</sup> &times;
%d<sup>4</sup> = <b>%s</b>.</li></ol>
<p>Greedy's cost grows gently with depth; the count of possible trees explodes. That is why
finding the best tree is hard and greedy is the practical choice.</p>""" % (
        NF3, NF3 - 1, big(GREEDY_D2), NF3, NF3 - 1, NF3 - 1, big(EXH_D2),
        NF3, NF3 - 1, NF3 - 2, big(EXH_D3)),
    "Checking every possible tree explodes with depth; greedy checks a handful of splits per node.",
    "Trying every possible route through a maze takes forever. Picking the best-looking turn each "
    "time is quick, even if it is not always perfect.",
    [("exhaustive search", "trying every possibility"),
     ("depth", "how many questions you ask from the top to a leaf")]),

  spot=M("&ldquo;Neither feature helps, so the data is unlearnable.&rdquo;",
    """<p>Eight examples with two yes/no features, and the label is 1 exactly when the two features
<b>differ</b>. Someone computes the root gains: feature 1 gives %s, feature 2 gives %s. They write:
&ldquo;no split has any gain, so no tree can beat guessing.&rdquo; Find the faulty step.</p>""" % (
        n(G3a, 3), n(G3b, 3)),
    """<p>&ldquo;No split has gain <b>now</b>&rdquo; does not mean &ldquo;no tree can do better&rdquo;.
Split on feature 1 anyway, then on feature 2 inside each child: those second splits gain %s and %s
&mdash; every leaf is pure.</p>
<p>This is greedy's blind spot. Looking one step ahead, both features look useless; together they
explain everything. A gain threshold at the root would stop the tree before it found that.</p>""" % (
        n(G3_DEPTH2_L, 3), n(G3_DEPTH2_R, 3)),
    "A split worth nothing on its own can set up a perfect split underneath it; greedy cannot see that.",
    "Neither &ldquo;is it raining?&rdquo; nor &ldquo;do you have an umbrella?&rdquo; alone tells you "
    "if someone gets wet. Ask both and you know for sure.",
    [("XOR", "&ldquo;one or the other but not both&rdquo;"),
     ("lookahead", "checking what a choice makes possible later")]),

  transfer=M("Add one house and the root changes.",
    """<p>Ten houses, with &ldquo;has a garden&rdquo; = %s, &ldquo;has a garage&rdquo; = %s and
&ldquo;sold within a month&rdquo; = %s. Which feature is the root? Now add one house with no garden,
no garage, sold within a month. What happens to the root &mdash; and what should that make you
think about reading one tree's structure as &ldquo;what matters&rdquo;?</p>""" % (
        _ints(GA3), _ints(GB3), _ints(YI3)),
    """<p>Before: garden gains %s, garage %s &rarr; <b>garden</b> is the root. After one extra house:
garden %s, garage %s &rarr; <b>garage</b> takes the root, and the whole tree below it is rebuilt.</p>
<p>A single tree's shape is unstable, so &ldquo;the root feature is the most important&rdquo; is a
fragile claim. That instability is a large part of why many trees, averaged, replaced one.</p>""" % (
        n(GAIN_A0, 3), n(GAIN_B0, 3), n(GAIN_A1, 3), n(GAIN_B1, 3)),
    "When two splits are close, one new example can flip the root and rebuild the whole tree.",
    "If two kids are almost equally fast, one more race can change who is captain, and then the "
    "whole team gets picked differently.",
    [("root", "the first question at the top of the tree"),
     ("unstable", "changes a lot when the data changes a little")]),
),

# =================================================================== q04
D("c2w4-q04",
  recall=M("What changes for a regression tree, and what stays.",
    """<p>From memory: what two things change when a decision tree predicts a number instead of a
class? Write the replacement for information gain.</p>""",
    """<p><b>Changes</b>: the impurity measure (variance instead of entropy) and the leaf's output
(the <b>mean</b> of its examples instead of a majority vote).</p>
<p>Variance reduction = Var(root) &minus; ( <var>w</var><sup>left</sup> Var(left) +
<var>w</var><sup>right</sup> Var(right) ), with the same size weights as before.</p>
<p><b>Stays</b>: the greedy loop, the stopping rules, the threshold search.</p>""",
    "Swap entropy for variance and majority vote for the mean; the rest of the algorithm is unchanged.",
    "For yes/no questions the tree makes piles of the same kind. For numbers, it makes piles of "
    "numbers that are close together, and guesses the pile's average.",
    [("variance", "the average squared distance from the mean: how spread out numbers are"),
     ("leaf mean", "the average target of the examples that end in that leaf")]),

  work=M("Variance reduction for two splits of six prices.",
    """<p>Six house prices (in $1000s): %s, sorted by size. Compute the variance reduction for
splitting after the 3rd house and after the 2nd house. Which wins, and what does each leaf
predict?</p>""" % _ints(Y4),
    """<p>Root variance = %s.</p>
<ul><li>After the 3rd: children variances %s and %s, reduction <b>%s</b>.</li>
<li>After the 2nd: reduction <b>%s</b>.</li></ul>
<p>The first wins easily. Its leaves predict the means: <b>%s</b> and <b>%s</b>.</p>""" % (
        n(V4, 1), n(VA_L, 1), n(VA_R, 1), n(VR4a, 1), n(VR4c, 1), n(MA_L, 1), n(MA_R, 1)),
    "The best split leaves numbers tightly bunched on each side, and each leaf predicts its average.",
    "Put the cheap houses together and the expensive houses together, then guess each group's "
    "middle price.",
    [("reduction", "how much smaller the spread got"),
     ("$1000s", "prices counted in thousands, so 150 means $150,000")]),

  spot=M("Entropy on prices, treating each price as a class.",
    """<p>To reuse their classification code, someone treats every distinct price as its own class.
For the six prices above, they score two 3 / 3 splits: tight groups
({150, 160, 170} | {300, 320, 340}) and mixed groups ({150, 300, 340} | {160, 170, 320}). Both
get the same gain. What went wrong?</p>""",
    """<p>Every price is distinct, so every 3 / 3 split scores log<sub>2</sub> 6 &minus;
log<sub>2</sub> 3 = <b>%s</b> &mdash; whichever prices go where. Entropy treats 300 versus 320 as
just as different as 150 versus 340.</p>
<p>Variance sees the difference: the tight split reduces variance by <b>%s</b>, the mixed one by
only <b>%s</b>. A numeric target needs a measure that knows how far apart numbers are.</p>""" % (
        n(GC, 3), n(VR4a, 1), n(VR4b, 1)),
    "Entropy only counts labels; for numbers you need variance, which measures distance.",
    "If you only check whether two prices are the same or not, $300 and $301 look as different as "
    "$300 and $3 million.",
    [("distinct", "all different from each other"),
     ("numeric target", "an answer that is a number, not a category")]),

  transfer=M("How many different prices can a depth-3 tree say?",
    """<p>A depth-%d regression tree prices 10,000 houses. At most how many <b>different</b> prices can
it output? Sketch its prediction against house size.</p>""" % DEPTH4,
    """<p>At most <b>%d</b> &mdash; one per leaf, 2<sup>%d</sup>. All 10,000 houses get one of those
values.</p>
<p>Against size, the prediction is a <b>staircase</b>: flat steps, jumping at each threshold.
Smoother predictions need more leaves (or many trees averaged).</p>""" % (LEAVES4, DEPTH4),
    "A regression tree predicts one fixed value per leaf, so its output is a staircase.",
    "It is like a price list with only eight prices on it. Every house has to be matched to one of "
    "the eight.",
    [("staircase", "flat steps with sudden jumps, not a smooth curve"),
     ("2<sup>3</sup>", "2 &times; 2 &times; 2 = 8")]),
),

# =================================================================== q05
D("c2w4-q05",
  recall=M("Why a tree cannot continue a trend.",
    """<p>From memory: what does a regression tree predict for an input far beyond anything in its
training data, and why? Name a model that behaves differently.</p>""",
    """<p>It predicts the value of the <b>last leaf</b> on that side &mdash; the mean of the training
examples there. A tree only asks &ldquo;above or below this threshold?&rdquo;, so past the largest
threshold every input lands in the same leaf, for ever.</p>
<p>A linear model behaves differently: it keeps following its slope, for better or worse.</p>""",
    "A tree's predictions are flat beyond its training range: it repeats the edge value forever.",
    "If the biggest dog you have ever seen weighed 40 kg, a tree guesses 40 kg for a dog the size of "
    "a horse.",
    [("extrapolate", "guess beyond the range you have seen"),
     ("piecewise constant", "flat in each region, jumping between regions")]),

  work=M("A stump and a line, asked about a 2,000 m&sup2; house.",
    """<p>Sizes %s m&sup2; with prices exactly 2 &times; size + 50 (in $1000s). Fit the best single
split (by variance reduction) and a straight line. What does each predict for 2,000 m&sup2;?</p>""" % (
        _ints(X5)),
    """<p>The best stump splits at <b>%s m&sup2;</b>, predicting %s on the left and %s on the right.
For 2,000 m&sup2; it says <b>%s</b>.</p>
<p>The line recovers price = 2 &times; size + 50 and says <b>%s</b>. Here the line is right because
the data really is linear; the tree cannot follow the trend at all.</p>""" % (
        n(T5, 0), n(L5, 1), n(R5, 1), n(R5, 1), n(LINQ5, 0)),
    "Beyond the training data a tree repeats its edge value; a line keeps its slope.",
    "The tree remembers the last price it saw and keeps saying it. The line says &ldquo;bigger house, "
    "bigger price&rdquo; and keeps going.",
    [("stump", "a tree with just one split"),
     ("m&sup2;", "square metres, a measure of floor area")]),

  spot=M("&ldquo;A forest will fix the extrapolation.&rdquo;",
    """<p>&ldquo;One tree flatlines past the data, but a random forest averages %d trees, so it will
extrapolate fine.&rdquo; A forest of stumps on bootstrap samples of the data above predicts
<b>%s</b> for 2,000 m&sup2;. Where is the reasoning wrong?</p>""" % (len(_preds), n(FOREST5, 1)),
    """<p>Averaging cannot leave the range of what is being averaged. Every tree outputs a mean of
training prices, so every tree &mdash; and the average &mdash; stays at or below the largest
training price, <b>%s</b>. The forest predicts %s; the true value is %s.</p>
<p>Ensembles reduce variance. They do not add a trend that no single tree can represent.</p>""" % (
        n(YMAX5, 0), n(FOREST5, 1), n(LINQ5, 0)),
    "An average of flat-lining trees still flatlines; no ensemble of trees can predict above the training maximum.",
    "If every friend's guess is at most 850, the average of their guesses cannot be 4,050.",
    [("ensemble", "many models combined into one answer"),
     ("training maximum", "the largest answer seen in the training data")]),

  transfer=M("Sales growing every month, predicted with a tree.",
    """<p>Monthly sales grew 5%% a month for 24 months, from 100 to %s. A tree is trained on
(month number &rarr; sales). What does it predict for month 30, what is the trend value, and how
would you rescue the tree?</p>""" % n(LAST5, 1),
    """<p>The tree returns its last leaf's mean: at most <b>%s</b>, the final month, and less if that
leaf averages several months. Continuing the trend gives <b>%s</b>.</p>
<p>Rescue: have the tree predict something that does <i>not</i> run off the edge &mdash; the
month-on-month <b>change</b> or <b>growth ratio</b>, or the residual after a linear trend &mdash;
and add the trend back. Then month 30 looks like the months it has seen.</p>""" % (
        n(LAST5, 1), n(TRUE30, 1)),
    "To use a tree on a trend, model what stays in range (the change) and add the trend back yourself.",
    "If you are growing taller every year, guess how much you will grow next year, not your height, "
    "because that number stays about the same.",
    [("trend", "a steady rise or fall over time"),
     ("residual", "what is left after taking the trend away")]),
),

# =================================================================== q06
D("c2w4-q06",
  recall=M("Sampling with replacement, and the 63% rule.",
    """<p>From memory: describe one bootstrap sample of a dataset of size <var>m</var>, give the
fraction of original examples it contains on average, and say what the rest are used for.</p>""",
    """<p>Draw <var>m</var> times from the <var>m</var> examples, <b>putting each one back</b>, so
examples can repeat. The bag is the same size as the original.</p>
<p>On average about <b>63%%</b> of the originals appear at least once (1 &minus; 1/<var>e</var>).
The ~37%% left out are the <b>out-of-bag</b> examples: a free validation set for that tree.</p>""",
    "Draw with putting back, as many times as there are examples; about 63% show up, 37% are left out.",
    "Pull a marble from a bag, write it down, put it back, and do that ten times. Some marbles come "
    "out twice, some never.",
    [("with replacement", "each drawn example goes back, so it can be drawn again"),
     ("bootstrap sample", "one new training set made this way"),
     ("out-of-bag", "the examples a particular bag happened to miss")]),

  work=M("The 63% from the formula, and from a simulation.",
    """<p>The chance an example is never drawn is (1 &minus; 1/<var>m</var>)<sup><var>m</var></sup>.
Compute the expected fraction that <i>does</i> appear for <var>m</var> = %s, and compare
<var>m</var> = 10 with a simulation.</p>""" % ", ".join(str(m) for m in MS6),
    """<ul>%s</ul>
<p>The limit is 1 &minus; 1/<var>e</var> = <b>%s</b>. Simulating 20,000 bags of size 10 gives an
average of <b>%s</b>, against the formula's %s. One such bag, sorted: %s &mdash; only %d distinct
examples.</p>""" % (
        "".join("<li><var>m</var> = %d: <b>%s</b></li>" % (m, n(u, 4)) for m, u in zip(MS6, UNIQ6)),
        n(LIMIT6, 4), n(SIM6, 4), n(UNIQ6[2], 4), _ints(ONE_BAG6), ONE_BAG_UNIQ6),
    "The fraction of examples a bootstrap bag contains settles near 63% once the dataset is not tiny.",
    "Ten pulls from ten marbles usually shows you only six or seven different marbles.",
    [("1/<var>e</var>", "about 0.368, a famous number from maths"),
     ("simulation", "doing the random process many times on a computer and averaging")]),

  spot=M("A bootstrap with one wrong argument.",
    """<p>A bagging implementation draws each tree's training set like this:</p>%s
<p>All 100 trees come out identical. Why?</p>""" % code(
        "idx = np.random.choice(m, size=m, replace=False)\nX_bag = X[idx]"),
    """<p><code>replace=False</code> draws <var>m</var> examples from <var>m</var> without putting any
back &mdash; a shuffle. Every bag contains <b>%s</b> of the data, every time, just reordered. Trees
built on the same data are the same tree.</p>
<p>It must be <code>replace=True</code>. Repeats and gaps are what make the bags differ.</p>""" % (
        "%s%%" % n(NOREP6 * 100, 0)),
    "Without replacement every bag is the full dataset reshuffled, so every tree is identical.",
    "Taking every marble out once just gives you the same marbles in a new order. Nothing changes.",
    [("replace=False", "never draw the same example twice"),
     ("permutation", "the same items in a different order")]),

  transfer=M("How many trees can vote on each patient for free?",
    """<p>A clinical forest has %d trees trained on %d patients. You want each patient's
out-of-bag prediction: the vote of only the trees that never saw that patient. On average, how
many trees is that?</p>""" % (NTREE6, NPAT6),
    """<p>Each tree misses a given patient with probability (1 &minus; 1/%d)<sup>%d</sup>, so about
<b>%s</b> of the %d trees can vote on each patient.</p>
<p>That gives an honest validation estimate for every patient, without holding any of the %d
back &mdash; which matters when patients are scarce.</p>""" % (
        NPAT6, NPAT6, n(OOB_TREES6, 1), NTREE6, NPAT6),
    "Each example is unseen by about 37% of the trees, and they give you a free test score for it.",
    "Each patient can ask the trees that never met them for an opinion, a bit like a blind taste test.",
    [("out-of-bag prediction", "a vote from only the trees that did not train on that example"),
     ("validation estimate", "a guess at how well the model does on new data")]),
),

# =================================================================== q07
D("c2w4-q07",
  recall=M("The two sources of randomness in a forest.",
    """<p>From memory: name both random ingredients of a random forest, say when the feature subset
is drawn, and give the usual size of the subset for classification.</p>""",
    """<ol><li><b>Rows</b>: each tree gets its own bootstrap sample.</li>
<li><b>Features</b>: at <b>every split</b>, only a random subset of <var>k</var> features may be
chosen from &mdash; usually <var>k</var> &asymp; &radic;<var>n</var>.</li></ol>
<p>The subset is redrawn at every node, not once per tree. That stops one dominant feature from
being the root of every tree, so the trees disagree and their average is better.</p>""",
    "Bootstrap the rows per tree, and pick a fresh random handful of features at every split.",
    "If every judge has the same favourite question, they all ask it first and agree on everything. "
    "Hide some questions from each judge each time, and you get a range of opinions worth averaging.",
    [("random forest", "many trees, each made different by randomness, voting together"),
     ("feature subset", "the few features a split is allowed to choose from"),
     ("&radic;<var>n</var>", "the square root of the number of features")]),

  work=M("How often can the dominant feature be the root?",
    """<p>%d features, of which one is far stronger than the rest. A forest of %d trees allows
<var>k</var> = %d features per split. In how many trees, on average, can the strong feature be the
root? Compare plain bagging. And what <var>k</var> would you use with %d features?</p>""" % (
        NF7, NTREES7, K7, NF7b),
    """<p>The strong feature is in the root's subset with probability %d / %d = %s, so it can be the
root in about <b>%s</b> of %d trees. With bagging it is the root of <b>all %d</b>.</p>
<p>With %d features, &radic;%d = <b>%d</b>.</p>""" % (
        K7, NF7, n(P_AVAIL7, 2), n(ROOT_DOM7, 0), NTREES7, NTREES7, NF7b, NF7b, K7b),
    "Feature subsets let other features lead most of the trees, which makes the trees different.",
    "If the best player is only allowed to play in a quarter of the matches, the other players get "
    "to show what they can do.",
    [("dominant feature", "one feature much more useful than the others"),
     ("bagging", "bootstrap samples plus averaging, without feature subsets")]),

  spot=M("Features drawn once per tree.",
    """<p>&ldquo;My random forest: for each tree, I pick 4 random features out of 16, then grow the
whole tree using only those 4.&rdquo; Which step departs from the algorithm, and what does it cost?</p>""",
    """<p>The subset must be drawn <b>at every node</b>, not once per tree. Drawn once per tree, a tree
that misses the strong feature can <i>never</i> use it anywhere, so it is a weak tree all the way
down; and trees that got it use it everywhere, so they look alike.</p>
<p>Per-node draws let every tree use every feature somewhere, while still mixing up which feature
leads at each split.</p>""",
    "Redraw the feature subset at every split; drawing it once per tree makes weak trees.",
    "It is like hiding a different few questions from a judge every round, not locking a whole "
    "pile of questions away for the entire contest.",
    [("per node", "fresh at every split in the tree"),
     ("per tree", "chosen once, then fixed for the whole tree")]),

  transfer=M("More trees, or less alike trees?",
    """<p>For averaging <var>B</var> trees, each with variance 1 and pairwise correlation &rho;, the
variance of the average is &rho; + (1 &minus; &rho;)/<var>B</var>. Your forest has &rho; = 0.9 and
<var>B</var> = 500. A colleague wants 1,000 trees; you want to lower &rho; to 0.3. Compare.</p>""",
    """<ul><li>&rho; = 0.9, 500 trees: <b>%s</b>.</li><li>&rho; = 0.9, 1,000 trees: <b>%s</b>.</li>
<li>&rho; = 0.3, 500 trees: <b>%s</b>.</li></ul>
<p>Doubling the trees barely moves it: the &rho; term is a floor that more trees never remove.
Making trees less alike is what helps &mdash; which is exactly what the feature subsets are for.</p>""" % (
        n(FV_HI_500, 4), n(FV_HI_1000, 4), n(FV_LO_500, 4)),
    "Averaging only cancels errors the trees do not share, so making trees differ beats adding more.",
    "Asking a hundred people who all copied the same answer is no better than asking one.",
    [("correlation &rho;", "how much two trees tend to make the same mistakes"),
     ("variance of the average", "how much the forest's answer wobbles")]),
),

# =================================================================== q08
D("c2w4-q08",
  recall=M("Boosting against a forest, point by point.",
    """<p>From memory: contrast boosting with a random forest on how trees are built (order), what
each tree is fitted to, typical depth, and the role of the learning rate.</p>""",
    """<ul><li><b>Order</b>: boosting is sequential; a forest builds trees independently.</li>
<li><b>Fitted to</b>: each boosted tree fits the <b>errors left by the trees so far</b>; forest trees
each fit the target on their own bootstrap sample.</li>
<li><b>Depth</b>: boosted trees are shallow (often 3&ndash;6); forest trees are grown deep.</li>
<li><b>Learning rate</b>: shrinks each boosted tree's contribution so the sequence does not chase
noise.</li></ul>""",
    "Boosting adds shallow trees one after another, each correcting what the previous ones got wrong.",
    "A forest is a crowd answering at once. Boosting is one student redoing only the questions they "
    "got wrong, a little at a time.",
    [("boosting", "building trees in sequence, each fixing the last ones' mistakes"),
     ("residual", "the truth minus the current prediction"),
     ("learning rate", "how much of each new tree's correction you actually use")]),

  work=M("Three rounds of boosting, by hand.",
    """<p>Data: <var>x</var> = %s, <var>y</var> = %s. Start by predicting the mean. Each round, fit
the best one-split stump to the <b>residuals</b> and add %s &times; its output. Track the squared
error.</p>""" % (_ints(X8), _ints(Y8), n(ETA8, 1)),
    """<p>Start: predict %s everywhere; residuals %s; squared error %s.</p>
<ol>%s</ol>
<p>Final predictions %s. Each round only fixes part of the remaining error, and the error keeps
falling: %s.</p>""" % (
        n(INIT8, 2), _row(RES8_0, 2), n(SSE8[0], 2),
        "".join("<li>Stump splits at %s: left %s, right %s &rarr; squared error <b>%s</b></li>"
                % (n(t, 1), n(l, 2), n(r, 2), n(e, 2))
                for (t, l, r), e in zip(ROUNDS8, SSE8[1:])),
        _row(PRED8, 2), " &rarr; ".join(n(e, 1) for e in SSE8)),
    "Each round fits what is still wrong and adds back a fraction of that fix.",
    "Guess the average, see where you were off, fix half of that, look again, fix half of what is left.",
    [("stump", "a tree with a single split"),
     ("round", "one more tree added to the sequence")]),

  spot=M("A boosting loop that fits the wrong target.",
    """<p>An implementation, where <code>fit_stump(x, t)</code> returns the best stump's predictions
for target <code>t</code>:</p>%s
<p>On the data above, after 4 rounds the predictions are %s against <var>y</var> = %s. Find the
faulty line.</p>""" % (
        code("pred = np.zeros(m)\nfor t in range(4):\n    step = fit_stump(x, y)\n"
             "    pred = pred + 0.5 * step"),
        _row(BUG8, 2), _ints(Y8)),
    """<p><code>fit_stump(x, y)</code> fits the <b>original target</b> every round, so every tree is the
same tree, and 4 &times; 0.5 = 2 copies of it are added up: the predictions overshoot to double.</p>
<p>It should be <code>fit_stump(x, y - pred)</code>: each new tree fits the <b>residual</b>, what is
still wrong.</p>""",
    "Each boosted tree must fit the residual; fitting y again just stacks copies of the same tree.",
    "If you keep re-answering the whole test instead of only your mistakes, you just write the same "
    "answers twice.",
    [("y - pred", "what the model still gets wrong"),
     ("overshoot", "go past the right answer")]),

  transfer=M("Halve the learning rate: how many more trees?",
    """<p>On data that one stump fits exactly, each round removes the fraction &eta; of the remaining
error, so after <var>T</var> rounds the error is (1 &minus; &eta;)<sup><var>T</var></sup> of where it
started. How many rounds to get below 1%% with &eta; = 0.1? With &eta; = 0.05? What does that say
about tuning the two settings?</p>""",
    """<p>&eta; = 0.1: <b>%d</b> rounds. &eta; = 0.05: <b>%d</b> rounds &mdash; roughly double.</p>
<p>Learning rate and number of trees trade off directly, so tune them together: fix a small rate and
let early stopping on validation data choose the number of trees.</p>""" % (T8_01, T8_005),
    "A smaller learning rate needs proportionally more trees; tune the two together.",
    "Taking half-size steps means walking about twice as many steps to the same place.",
    [("&eta; (eta)", "the learning rate"),
     ("early stopping", "stop adding trees when validation error stops improving")]),
),

# =================================================================== q09
D("c2w4-q09",
  recall=M("When trees, when neural networks.",
    """<p>From memory: what kind of data do tree ensembles usually win on, what kind do neural networks
win on, and give two practical reasons for each.</p>""",
    """<p><b>Trees</b> (especially boosted): <b>tabular, structured</b> data &mdash; spreadsheet
columns. Fast to train, little preprocessing (no scaling, handle mixed types), and small trees are
readable.</p>
<p><b>Neural networks</b>: <b>unstructured</b> data &mdash; images, audio, text. They learn the
features themselves, support transfer learning from pretrained models, and can be chained with
other networks.</p>""",
    "Spreadsheets go to boosted trees; pictures, sound and text go to neural networks.",
    "Trees are great at reading tables of facts. Neural networks are great at looking at pictures "
    "and listening to sounds.",
    [("tabular", "data in rows and columns, like a spreadsheet"),
     ("unstructured", "raw pixels, sound or text, with no columns"),
     ("transfer learning", "starting from a model already trained on a similar task")]),

  work=M("Preprocessing a spreadsheet: tree versus network.",
    """<p>A table has %d numeric columns on very different scales and 3 categorical columns with
%s categories. (a) How wide is the network's input after one-hot encoding, and does it need
scaling? (b) Feature 1 = %s with labels %s: compute the best threshold's gain on the raw values,
times 1000, and after taking logs.</p>""" % (
        NUM9, ", ".join(str(c) for c in CATS9), _ints(X9), _ints(Y9)),
    """<p>(a) %d + %s = <b>%d</b> inputs, and the numeric ones must be scaled.</p>
<p>(b) Best gain: raw <b>%s</b>, &times;1000 <b>%s</b>, log <b>%s</b> &mdash; identical. A tree only
compares values with thresholds, so any order-preserving rescaling leaves its splits unchanged.
Scaling is simply unnecessary for trees.</p>""" % (
        NUM9, " + ".join(str(c) for c in CATS9), WIDTH9, n(G9, 4), n(G9s, 4), n(G9l, 4)),
    "Trees ignore scale and handle categories directly; networks need encoding and scaling first.",
    "A tree only asks &ldquo;bigger or smaller than this?&rdquo;, so it does not care if you measure "
    "in metres or millimetres.",
    [("one-hot encoding", "one yes/no column per category"),
     ("order-preserving", "keeps which value is bigger the same")]),

  spot=M("&ldquo;Reshape the CSV into an image and use a CNN.&rdquo;",
    """<p>&ldquo;My 40,000-row CSV has 30 columns. I'll reshape each row into a 5 &times; 6 grid and use
a convolutional network, since CNNs are the most powerful models.&rdquo; Which step is the
mistake?</p>""",
    """<p>The reshape. A convolution assumes <b>neighbouring</b> values are related, as neighbouring
pixels are. Column order in a spreadsheet is arbitrary: there are 30! &asymp; <b>%s &times;
10<sup>%d</sup></b> ways to order the columns, each a different &ldquo;image&rdquo; of the same
data.</p>
<p>The CNN would learn patterns in an accident of column order. For a table, start with
gradient-boosted trees.</p>""" % (n(ORD_MANT9, 2), ORD_EXP9),
    "Models built for images assume neighbours matter; spreadsheet columns have no neighbours.",
    "Gluing the pages of a phone book into a picture does not make it a picture of anything.",
    [("CNN", "a convolutional neural network, built for images"),
     ("convolution", "looking at small patches of neighbouring values"),
     ("30!", "30 &times; 29 &times; 28 &times; &hellip; &times; 1")]),

  transfer=M("Product photos plus a table of facts.",
    """<p>You predict whether an online listing sells, from its <b>photo</b> and a table of price,
category, seller rating and days listed. Which model, or models, and how do they fit together?</p>""",
    """<p>Use each where it is strong. A pretrained <b>neural network</b> turns each photo into a short
vector of learned features (transfer learning); that vector is joined to the table's columns, and a
<b>gradient-boosted tree</b> model makes the prediction.</p>
<p>A single network trained on both is also possible, but the split pipeline is cheaper to train and
usually strong on the tabular half.</p>""",
    "Mixed data can use both: a network to read the unstructured part, trees for the table.",
    "Let the picture expert describe the photo in a few numbers, then let the table expert decide.",
    [("embedding", "a short list of numbers a network uses to describe something"),
     ("pipeline", "models or steps used one after another")]),
),

# =================================================================== q10
D("c2w4-q10",
  recall=M("Why an ID column fools a tree.",
    """<p>From memory: why does a unique-ID column get the highest possible information gain, why is
it useless, and name two ways to handle high-cardinality columns that do carry information.</p>""",
    """<p>Every ID is unique, so splitting on it puts each example in its own pure leaf: gain equals
the parent's whole entropy, the maximum possible. But a new customer has an ID the tree has never
seen, so nothing transfers &mdash; pure memorisation.</p>
<p>Drop IDs. For real high-cardinality columns (postcodes, product codes): group rare values,
use a coarser version (region instead of postcode), or a target or hash encoding fitted on
training data only.</p>""",
    "A column with a different value for every row lets a tree memorise, and memorising is not learning.",
    "If you learn that &ldquo;the kid called Sam got an A&rdquo;, it tells you nothing about the new "
    "kid called Alex.",
    [("high-cardinality", "a column with a huge number of different values"),
     ("memorisation", "remembering the training examples instead of a rule"),
     ("target encoding", "replacing a category by the average answer for it")]),

  work=M("Gain of an ID column against a real feature.",
    """<p>A node of 8 customers, labels %s. Compute the information gain of splitting on
<code>customer_id</code> (every value different) and of a real yes/no feature that is yes for the
first four.</p>""" % _ints(Y10),
    """<p>Parent entropy = %s. Splitting on the ID gives 8 one-customer leaves, all pure: gain =
<b>%s</b>, the maximum possible.</p>
<p>The real feature gives left (3 of 4 positive) and right (0 of 4): gain = <b>%s</b>. The ID wins
on paper, and is the one feature guaranteed to be useless on the next customer.</p>""" % (
        n(H10, 3), n(GID10, 3), n(GREAL10, 3)),
    "An ID always scores the maximum gain, which is exactly why gain alone cannot be trusted with it.",
    "Putting every child in their own room makes every room perfectly tidy, but teaches you nothing "
    "about how to sort children.",
    [("parent entropy", "how mixed the node was before splitting"),
     ("one-customer leaf", "a leaf holding a single example")]),

  spot=M("&ldquo;order_id has the highest gain, so keep it.&rdquo;",
    """<p>A churn tree: training accuracy 100%%, validation 52%%. The feature report says
<code>order_id</code> has gain %s and <code>has_coupon</code> %s. The proposed fix: &ldquo;one-hot
encode order_id so the tree uses it properly.&rdquo; Find both faulty steps.</p>""" % (
        n(GID10, 3), n(GREAL10, 3)),
    """<p>First, highest gain &ne; most informative: an ID's gain is maximal by construction, and the
100%% / 52%% gap is the memorisation showing.</p>
<p>Second, one-hot encoding an ID makes it worse: one column per order, the same memorisation, and
far more columns. The fix is to <b>drop</b> <code>order_id</code>.</p>""",
    "A train/validation gap plus an ID at the top of the feature report means: drop the ID.",
    "Giving every order its own label does not help the tree. It just gives it more things to memorise.",
    [("churn", "customers leaving"),
     ("validation accuracy", "how often the model is right on data it did not train on")]),

  transfer=M("Postcodes: real information, too many values.",
    """<p>%s rows, and a postcode column with %s distinct postcodes. Unlike an ID, postcode really does
affect price. How many rows does the average postcode have, why is that a problem, and what would
you do?</p>""" % (big(ROWS10), big(PC10)),
    """<p>About <b>%s</b> rows per postcode on average &mdash; and many postcodes far fewer. A split on a
rare postcode is fitted to a handful of rows: noise.</p>
<p>Use a coarser level that still carries the signal (district or region), group rare postcodes
into &ldquo;other&rdquo;, or target-encode postcodes using training data only. Keep the information;
lose the cardinality.</p>""" % n(PER10, 1),
    "Keep what a high-cardinality column means, but at a level with enough examples per value.",
    "Instead of a rule for every single street, make a rule for each neighbourhood, where you have "
    "enough houses to be sure.",
    [("postcode", "a short code for a small area"),
     ("coarser level", "a bigger grouping, like region instead of street")]),
),
]
