# -*- coding: utf-8 -*-
"""Quiz drills -- C3 W1. One concept per mock-quiz question, four methods each.

Every number below is COMPUTED here at import time and formatted into the text,
never typed. The k-means runs really run (assign, move, repeat) on a handful of
1-D points small enough to redo with a pencil; the Gaussian fractions come from
the error function, not from memory. Scenario inputs (a confusion table, the
counts in a split) are stated once as data; everything derived is computed.
"""
import itertools
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


def pc(x, d=1):
    """A fraction as a percentage string, e.g. 0.125 -> '12.5%'."""
    return n(100 * x, d) + "%"


def big(x):
    return "{:,.0f}".format(x)


def sci(x, d=1):
    """A number in scientific form for prose, e.g. 3.1 &times; 10<sup>5</sup>."""
    e = int(np.floor(np.log10(abs(x))))
    return "%s &times; 10<sup>%d</sup>" % (n(x / 10.0 ** e, d), e)


def _row(vals, d=2):
    return ", ".join(n(v, d) for v in vals)


def _phi(z):
    """Standard normal CDF."""
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def _within(k):
    """Fraction of a Gaussian within k standard deviations of the mean."""
    return _phi(k) - _phi(-k)


def _gauss(x, mu, var):
    return np.exp(-(x - mu) ** 2 / (2 * var)) / np.sqrt(2 * np.pi * var)


def _skew(v):
    v = np.asarray(v, float)
    return np.mean((v - v.mean()) ** 3) / np.std(v) ** 3


def _col(v):
    return np.asarray(v, float).reshape(-1, 1)


def _assign(X, mu):
    d2 = np.sum((X[:, None, :] - mu[None, :, :]) ** 2, axis=2)
    return np.argmin(d2, axis=1)


def _cost(X, c, mu):
    return np.mean(np.sum((X - mu[c]) ** 2, axis=1))


def _move(X, c, mu, w=None):
    out = mu.copy()
    if w is None:
        w = np.ones(len(X))
    for k in range(len(mu)):
        if np.any(c == k):
            out[k] = np.sum(w[c == k][:, None] * X[c == k], axis=0) / np.sum(w[c == k])
    return out


def _run(X, mu0, w=None, iters=100):
    """Full k-means from fixed starting centroids. One row per round:
    (assignments, centroids before the move, J after assign, centroids after, J after move)."""
    mu = np.array(mu0, float)
    hist = []
    for _ in range(iters):
        c = _assign(X, mu)
        ja = _cost(X, c, mu)
        new = _move(X, c, mu, w)
        hist.append((c, mu.copy(), ja, new.copy(), _cost(X, c, new)))
        if np.allclose(new, mu):
            break
        mu = new
    return hist


def _best_of(X, K, rng, starts):
    best = None
    for _ in range(starts):
        h = _run(X, X[rng.choice(len(X), K, replace=False)])
        c, mu, J = h[-1][0], h[-1][3], h[-1][4]
        if best is None or J < best[0]:
            best = (J, mu, c)
    return best


def _best_1d(x, K):
    """Exact best J in 1-D: optimal clusters are contiguous, so try every set of cuts."""
    m = len(x)
    best = None
    for cuts in itertools.combinations(range(1, m), K - 1):
        b = (0,) + cuts + (m,)
        J = sum(np.sum((x[b[i]:b[i + 1]] - x[b[i]:b[i + 1]].mean()) ** 2) for i in range(K)) / m
        if best is None or J < best:
            best = J
    return best


def _prf(tp, fp, fn):
    p = tp / (tp + fp) if (tp + fp) else 0.0
    r = tp / (tp + fn)
    f = 2 * p * r / (p + r) if (p + r) else 0.0
    return p, r, f


# ---------------------------------------------------------------- q01 the two steps
X1 = np.array([1.0, 2.0, 4.0, 7.0, 9.0, 10.0])
MU1_0 = np.array([1.0, 4.0])
H1 = _run(_col(X1), _col(MU1_0))
C1a, MU1a = H1[0][0], H1[0][3][:, 0]
C1b, MU1b = H1[1][0], H1[1][3][:, 0]
SW1 = X1[C1a != C1b]                       # the point that changes sides
ROUNDS1 = len(H1)
assert len(SW1) == 1 and ROUNDS1 == 3


def _members(x, c, k):
    return ", ".join(n(v, 0) for v in x[c == k])


# the slip: a random assignment every round instead of the nearest centroid
SEED1 = 3
_rs1 = np.random.RandomState(SEED1)
MU1s = MU1_0.copy()
JS1 = []
for _it in range(8):
    _c = _rs1.randint(0, 2, 6)
    assert np.any(_c == 0) and np.any(_c == 1)
    MU1s = np.array([X1[_c == 0].mean(), X1[_c == 1].mean()])
    JS1.append(np.mean((X1 - MU1s[_c]) ** 2))
JS1 = np.array(JS1)
RISES1 = int(np.sum(JS1[1:] > JS1[:-1]))
# transfer: households along a road, a bus stop is a weighted centroid
P1t = np.array([0.0, 1.0, 2.0, 7.0, 8.0, 12.0])
W1t = np.array([1.0, 1.0, 4.0, 2.0, 1.0, 1.0])
S1t_0 = np.array([0.0, 12.0])
H1t = _run(_col(P1t), _col(S1t_0), w=W1t)
C1t, S1t = H1t[-1][0], H1t[-1][3][:, 0]
U1t = np.array([P1t[C1t == 0].mean(), P1t[C1t == 1].mean()])

# ---------------------------------------------------------------- q02 initialisation
X2 = np.array([0.0, 2.0, 10.0, 13.0, 20.0, 22.0])
BAD2 = np.array([0.0, 2.0, 10.0])
GOOD2 = np.array([0.0, 10.0, 20.0])
HB2 = _run(_col(X2), _col(BAD2))
HG2 = _run(_col(X2), _col(GOOD2))
CB2, MUB2, JB2 = HB2[-1][0], HB2[-1][3][:, 0], HB2[-1][4]
CG2, MUG2, JG2 = HG2[-1][0], HG2[-1][3][:, 0], HG2[-1][4]
RATIO2 = JB2 / JG2
# the slip: one seeded start reused fifty times
RESTARTS2, TARGET2 = 50, 0.99
_same2 = []
for _a in range(RESTARTS2):
    _same2.append(round(_run(_col(X2), _col(BAD2))[-1][4], 9))
SAME2 = len(set(_same2))
_rs2 = np.random.RandomState(0)
FRESH2 = []
for _a in range(RESTARTS2):
    _i = _rs2.choice(6, 3, replace=False)
    FRESH2.append(_run(_col(X2), _col(X2[_i]))[-1][4])
FRESH2 = np.array(FRESH2)
GOODN2 = int(np.sum(np.abs(FRESH2 - JG2) < 1e-9))
BEST2 = FRESH2.min()
# transfer: chance a random start puts exactly one centroid in each of K equal clusters
KS2 = (2, 3, 5, 8, 10)
LUCK2 = []
for _k in KS2:
    _p = np.prod(np.arange(1, _k + 1)) / _k ** _k
    LUCK2.append((_k, _p, int(np.ceil(np.log(1 - TARGET2) / np.log(1 - _p)))))

# ---------------------------------------------------------------- q03 the cost J
J1 = [(H1[0][2], H1[0][4]), (H1[1][2], H1[1][4]), (H1[2][2], H1[2][4])]
_own3 = MU1_0[H1[0][0]]
SUM3 = " + ".join("(%s&minus;%s)&sup2;" % (n(a, 0), n(b, 0)) for a, b in zip(X1, _own3))
# the slip: the cost line forgets to square
X3 = np.array([1.0, 1.0, 1.0, 11.0, 30.0, 32.0])
MU3_0 = np.array([1.0, 31.0])
H3 = _run(_col(X3), _col(MU3_0))
C3, MU3 = H3[0][0], H3[0][3][:, 0]
assert len(H3) == 2
ABS3_A = np.mean(np.abs(X3 - MU3_0[C3]))
ABS3_M = np.mean(np.abs(X3 - MU3[C3]))
SQ3_A, SQ3_M = H3[0][2], H3[0][4]
MED3 = np.median(X3[C3 == 0])
# transfer: J at K = 1 is the variance, so J has a scale to compare against
VAR3 = np.var(X1)
FIN3 = H1[-1][4]
EXPL3 = 1 - FIN3 / VAR3

# ---------------------------------------------------------------- q04 choosing k
_rng4 = np.random.default_rng(4)
STARTS4, SIDE4 = 10, 10.0
_cent4 = np.array([[2.0, 2.0], [8.0, 3.0], [5.0, 8.0]])
BLOB4 = np.concatenate([_cent4[k] + _rng4.normal(0, 0.7, (50, 2)) for k in range(3)])
UNIF4 = _rng4.uniform(0, SIDE4, (150, 2))
KS4 = np.arange(1, 8)
JB4 = np.array([_best_of(BLOB4, k, _rng4, STARTS4)[0] for k in KS4])
JU4 = []
DIST4 = []
for _k in range(1, 9):
    _J, _mu, _c = _best_of(UNIF4, _k, _rng4, STARTS4)
    JU4.append(_J)
    DIST4.append(np.mean(np.sqrt(np.sum((UNIF4 - _mu[_c]) ** 2, axis=1))))
JU4 = np.array(JU4)
DIST4 = np.array(DIST4)
DB4 = JB4[:-1] - JB4[1:]
DU4 = JU4[:len(KS4) - 1] - JU4[1:len(KS4)]
RB4 = DB4[1:] / DB4[:-1]
RU4 = DU4[1:] / DU4[:-1]
assert np.argmin(RB4) == 1                 # the collapse is after K = 3
# the slip: argmin over K
X4s = np.array([1.0, 2.0, 3.0, 11.0, 12.0, 13.0, 21.0, 22.0, 23.0])
JS4 = np.array([_best_1d(X4s, k) for k in range(1, len(X4s) + 1)])
PICK4 = int(np.argmin(JS4)) + 1
# transfer: depots priced in money
RENT4, SHOPS4, DROPS4, PERKM4 = 3000, 150, 20, 1.5
TRIP4 = SHOPS4 * DROPS4 * 2 * PERKM4       # cost per km of average distance, per month
TOT4 = RENT4 * np.arange(1, 9) + TRIP4 * DIST4
KBEST4 = int(np.argmin(TOT4)) + 1

# ---------------------------------------------------------------- q05 the unusual split
NORM5, ANOM5 = 10000, 20
TR5, CV5 = int(0.6 * NORM5), int(0.2 * NORM5)
TE5 = NORM5 - TR5 - CV5
ACV5 = ANOM5 // 2
ATE5 = ANOM5 - ACV5
SHARE5 = ACV5 / (CV5 + ACV5)
# one anomaly slipped into a small training set
N5 = np.array([4.0, 5.0, 5.0, 6.0, 5.0, 4.0, 6.0, 5.0])
BAD5 = 50.0
Q5 = 9.0                                   # an anomaly waiting in cross-validation
MU5, VAR5 = N5.mean(), N5.var()
_c5 = np.append(N5, BAD5)
MU5c, VAR5c = _c5.mean(), _c5.var()
Z5, Z5c = (Q5 - MU5) / np.sqrt(VAR5), (Q5 - MU5c) / np.sqrt(VAR5c)
P5, P5c = _gauss(Q5, MU5, VAR5), _gauss(Q5, MU5c, VAR5c)
ZN5c = np.abs(N5 - MU5c) / np.sqrt(VAR5c)
# the slip: shuffle everything and split 60/20/20
_y5 = np.concatenate([np.zeros(NORM5), np.ones(ANOM5)])
_perm5 = np.random.default_rng(5).permutation(NORM5 + ANOM5)
_ys5 = _y5[_perm5]
_a5, _b5 = int(0.6 * len(_ys5)), int(0.8 * len(_ys5))
RTR5, RCV5, RTE5 = int(_ys5[:_a5].sum()), int(_ys5[_a5:_b5].sum()), int(_ys5[_b5:].sum())
EXP5 = (0.6 * ANOM5, 0.2 * ANOM5, 0.2 * ANOM5)
# transfer: two anomalies in total
TINY5, LINE5 = 2, 50000
STEPS5 = np.arange(TINY5 + 1) / TINY5

# ---------------------------------------------------------------- q06 which technique
PROB6 = [("card fraud, three known schemes", 6000, 3, "no"),
         ("jet-engine failures", 12, 9, "yes"),
         ("scratched phone screens", 800, 1, "no"),
         ("server intrusions", 40, 25, "yes")]
PER6 = [(nm, pos, kinds, pos / kinds, new) for nm, pos, kinds, new in PROB6]
FRAUD6, TXN6 = 6000, 2000000
RATE6 = FRAUD6 / TXN6
NOTES6 = 4000

# ---------------------------------------------------------------- q07 feature transforms
X7 = np.array([1.0, 10.0, 10.0, 100.0, 100.0, 100.0, 1000.0, 1000.0, 10000.0])
MU7, SD7 = X7.mean(), X7.std()
L7 = np.log10(X7)
LMU7, LSD7 = L7.mean(), L7.std()
NEG7 = _phi(-MU7 / SD7)                    # the raw Gaussian's mass on impossible negatives
ZHI7, ZLO7 = (X7.max() - MU7) / SD7, (X7.min() - MU7) / SD7
LZHI7, LZLO7 = (L7.max() - LMU7) / LSD7, (L7.min() - LMU7) / LSD7
SK7, LSK7 = _skew(X7), _skew(L7)
MM7 = (X7 - X7.min()) / (X7.max() - X7.min())
MSK7 = _skew(MM7)
# transfer: a LEFT-skewed feature (battery level, mostly near full)
B7 = 100 * np.random.default_rng(7).beta(9, 1.3, 5000)
BT7 = [("x (raw)", _skew(B7)), ("x ** 3", _skew(B7 ** 3)), ("x ** 6", _skew(B7 ** 6)),
       ("np.log(101 - x)", _skew(np.log(101 - B7)))]

# ---------------------------------------------------------------- q08 metrics
CVN8, CVA8 = 2000, 10
FLAG8, HIT8 = 14, 8
TP8, FP8 = HIT8, FLAG8 - HIT8
FN8, TN8 = CVA8 - TP8, CVN8 - (FLAG8 - HIT8)
N8 = CVN8 + CVA8
ACC8 = (TP8 + TN8) / N8
NULL8 = CVN8 / N8
P8, R8, F8 = _prf(TP8, FP8, FN8)
# the slip: tune epsilon by accuracy. (label, TP, FP) at four thresholds
SW8 = [("&epsilon;<sub>0</sub> (below every p)", 0, 0), ("&epsilon;<sub>1</sub>", 3, 4),
       ("&epsilon;<sub>2</sub>", 7, 9), ("&epsilon;<sub>3</sub>", 9, 30)]
SWS8 = []
for _lab, _tp, _fp in SW8:
    _acc = (_tp + CVN8 - _fp) / N8
    SWS8.append((_lab, _tp, _fp, _acc, _prf(_tp, _fp, CVA8 - _tp)[2]))
IACC8 = int(np.argmax([s[3] for s in SWS8]))
IF18 = int(np.argmax([s[4] for s in SWS8]))
assert IACC8 == 0 and IF18 == 2
# transfer: a vendor's "1% false alarms, 90% caught" at a 0.1% base rate
VOL8, BASE8, FAR8, REC8 = 100000, 0.001, 0.01, 0.90
VA8 = VOL8 * BASE8
VTP8 = REC8 * VA8
VFP8 = FAR8 * (VOL8 - VA8)
VPREC8 = VTP8 / (VTP8 + VFP8)

# ---------------------------------------------------------------- q09 independence
T9 = np.array([2.0, 4.0, 6.0, 8.0, 10.0])          # network traffic
C9 = np.array([2.1, 3.9, 6.2, 7.8, 10.0])          # CPU load
NEW9 = (3.0, 9.0)                                  # low traffic, high CPU: stuck in a loop
MT9, VT9, MC9, VC9 = T9.mean(), T9.var(), C9.mean(), C9.var()
ZT9 = (NEW9[0] - MT9) / np.sqrt(VT9)
ZC9 = (NEW9[1] - MC9) / np.sqrt(VC9)
PTR9 = _gauss(T9, MT9, VT9) * _gauss(C9, MC9, VC9)
PNEW9 = _gauss(NEW9[0], MT9, VT9) * _gauss(NEW9[1], MC9, VC9)
LOWER9 = int(np.sum(PTR9 < PNEW9))
R9 = C9 / T9
RNEW9 = NEW9[1] / NEW9[0]
ZR9 = (RNEW9 - R9.mean()) / R9.std()
# the slip: raise epsilon until the stuck server is caught, on 1,000 normal servers
_rng9 = np.random.default_rng(9)
BT9 = _rng9.normal(6, 2, 1000)
BC9 = BT9 * (1 + _rng9.normal(0, 0.05, 1000))
BP9 = _gauss(BT9, BT9.mean(), BT9.var()) * _gauss(BC9, BC9.mean(), BC9.var())
BPNEW9 = _gauss(NEW9[0], BT9.mean(), BT9.var()) * _gauss(NEW9[1], BC9.mean(), BC9.var())
BFLAG9 = np.mean(BP9 < BPNEW9)
_br9 = BC9 / BT9
BZR9 = (RNEW9 - _br9.mean()) / _br9.std()
BZMAX9 = (_br9.max() - _br9.mean()) / _br9.std()
# transfer: children's height and weight; the ratio is BMI
_rng9b = np.random.default_rng(19)
HT9 = _rng9b.normal(140, 12, 2000)
BMI9 = _rng9b.normal(17.5, 1.5, 2000)
WT9 = BMI9 * (HT9 / 100) ** 2
KID9 = (158.0, 30.0)
ZH9 = (KID9[0] - HT9.mean()) / HT9.std()
ZW9 = (KID9[1] - WT9.mean()) / WT9.std()
KBMI9 = KID9[1] / (KID9[0] / 100) ** 2
ZB9 = (KBMI9 - BMI9.mean()) / BMI9.std()

# ---------------------------------------------------------------- q10 the normal distribution
MU10, SD10 = 50.0, 5.0
LO10, HI10 = 40.0, 60.0
W1_10, W2_10, W3_10 = _within(1), _within(2), _within(3)
R1_10, R2_10, R3_10 = round(100 * W1_10), round(100 * W2_10), round(100 * W3_10, 1)   # the 68 / 95 / 99.7 rule
K10 = (HI10 - MU10) / SD10
A10, B10, T10 = MU10 - SD10, MU10 + SD10, MU10 + 3 * SD10
RULE_45_60 = R1_10 / 2 + R2_10 / 2
EX_45_60 = _phi(2) - _phi(-1)
RULE_65 = (100 - R3_10) / 2
EX_65 = 1 - _phi(3)
# the slip: dividing by the variance
VAR10 = SD10 ** 2
ZBAD10 = (HI10 - MU10) / VAR10
FBAD10 = _within(ZBAD10)
# transfer: ten features, each with its own 3-sigma alarm
NF10, DAY10 = 10, 1000000
ONE10 = 1 - W3_10
ANY10 = 1 - W3_10 ** NF10
ALERTS10 = ANY10 * DAY10

MU = "&mu;"
SIG = "&sigma;"
EPS = "&epsilon;"
CI = "<var>c</var><sup>(<var>i</var>)</sup>"
XI = "<var>x</var><sup>(<var>i</var>)</sup>"
MUK = "&mu;<sub><var>k</var></sub>"


DRILLS = [

# =================================================================== q01
D("c3w1-q01",
  recall=M("Both steps, in symbols, and what each holds fixed.",
    """<p>From memory: write the two steps of k-means using %s, %s and %s. For each step, say which
quantity it updates and which it holds fixed. When does the loop stop?</p>""" % (CI, XI, MUK),
    """<p><b>Assign:</b> %s := arg min<sub><var>k</var></sub> &#8214;%s &minus; %s&#8214;&sup2; &mdash; each
point joins its nearest centroid. Updates <var>c</var>; holds every &mu; fixed.</p>
<p><b>Move:</b> %s := the mean of the points with %s = <var>k</var>. Updates &mu;; holds every
assignment fixed.</p>
<p>Repeat until an assign step changes nothing. Randomness enters only once, when the starting
centroids are chosen; after that both steps are deterministic.</p>""" % (CI, XI, MUK, MUK, CI),
    "Join the nearest centroid, move each centroid to the middle of its points, repeat until nothing changes.",
    "Everyone runs to the nearest flag, then each flag walks to the middle of its crowd. Do it again "
    "until nobody has to run anywhere.",
    [("centroid", "the centre of a cluster, an average position"),
     ("assign", "decide which group each point belongs to"),
     ("arg min", "which choice gives the smallest value &mdash; the choice, not the value")]),

  work=M("Run k-means by hand on six points.",
    """<p>Six points on a line: <var>x</var> = %s. Use <var>K</var> = 2 and start the centroids at
%s<sub>1</sub> = %s and %s<sub>2</sub> = %s. Run assign, move, assign, move, &hellip; until nothing
changes. Which point changes cluster along the way?</p>""" % (
        _row(X1, 0), MU, n(MU1_0[0], 0), MU, n(MU1_0[1], 0)),
    """<p><b>Round 1.</b> Assign: cluster 1 = {%s}, cluster 2 = {%s}. Move: %s<sub>1</sub> = <b>%s</b>,
%s<sub>2</sub> = <b>%s</b>.</p>
<p><b>Round 2.</b> Assign: the point <b>%s</b> is now %s from %s<sub>1</sub> but %s from %s<sub>2</sub>,
so it <b>switches</b>. Cluster 1 = {%s}, cluster 2 = {%s}. Move: %s<sub>1</sub> = <b>%s</b>,
%s<sub>2</sub> = <b>%s</b>.</p>
<p><b>Round 3.</b> Assign: nothing changes, so the run has converged after %d assign steps.</p>
<p>The starting centroid at %s was badly placed; it did not matter, because the move step dragged it
to where its points actually were.</p>""" % (
        _members(X1, C1a, 0), _members(X1, C1a, 1), MU, n(MU1a[0]), MU, n(MU1a[1]),
        n(SW1[0], 0), n(abs(SW1[0] - MU1a[0])), MU, n(abs(SW1[0] - MU1a[1])), MU,
        _members(X1, C1b, 0), _members(X1, C1b, 1), MU, n(MU1b[0]), MU, n(MU1b[1]),
        ROUNDS1, n(MU1_0[1], 0)),
    "Each move changes who is nearest, so you assign again until the groups stop changing.",
    "When the flag walks to the middle of its crowd, some kids at the edge are now closer to the "
    "other flag, so they switch. When nobody switches, you are done.",
    [("round", "one assign step followed by one move step"),
     ("converged", "an assign step changed nothing, so nothing else will change either")]),

  spot=M("A loop that never settles.",
    """<p>Same six points, <var>K</var> = 2. A classmate's loop:</p>%s
<p>After each round they print the cost: %s. It never gets near the %s that real k-means reaches.
Which line is wrong?</p>""" % (
        code("for it in range(8):\n"
             "    c = np.random.randint(0, 2, 6)\n"
             "    mu[0] = x[c == 0].mean()\n"
             "    mu[1] = x[c == 1].mean()"),
        ", ".join(n(v) for v in JS1), n(H1[-1][4])),
    """<p><b>Line 2.</b> The assign step must give each point its <b>nearest</b> centroid,
<code>np.argmin((x[i] - mu) ** 2)</code>. A fresh random label every round throws away everything the
move step learned.</p>
<p>With random halves, each centroid is the mean of a random handful, so both hover near the overall
mean: after 8 rounds they sit at %s and %s. The cost went up in %d of the %d steps &mdash; impossible for
real k-means, and the symptom that gives the bug away. Random choices belong only to the start.</p>""" % (
        n(MU1s[0]), n(MU1s[1]), RISES1, len(JS1) - 1),
    "Randomness picks the starting centroids once; every assign step after that is &ldquo;nearest&rdquo;.",
    "If every round the kids picked a flag by drawing straws instead of running to the nearest one, "
    "the flags would wander around the middle for ever.",
    [("np.random.randint", "draws random whole numbers"),
     ("deterministic", "same input, same output, every time")]),

  transfer=M("Bus stops for houses of different sizes.",
    """<p>Houses along a road at positions %s km, holding %s people. Two bus stops start at %s and %s km.
Each person walks to the nearer stop. Run k-means where the move step puts each stop where its
<b>people</b> are, not where its houses are. Where do the stops end up?</p>""" % (
        _row(P1t, 0), _row(W1t, 0), n(S1t_0[0], 0), n(S1t_0[1], 0)),
    """<p>A house with 4 people is the same as 4 points at that spot, so the move step becomes a
<b>weighted mean</b>: &Sigma; (people &times; position) / &Sigma; people.</p>
<p>Assign: houses at {%s} use stop 1, {%s} use stop 2. Move: stop 1 = <b>%s</b> km, stop 2 =
<b>%s</b> km. The next assign step changes nothing, so it has converged.</p>
<p>Unweighted, the stops would sit at %s and %s km. The crowded house pulls stop 1 towards it. The
two steps are unchanged; only &ldquo;the mean&rdquo; learned to count people.</p>""" % (
        _members(P1t, C1t, 0), _members(P1t, C1t, 1), n(S1t[0]), n(S1t[1]), n(U1t[0]), n(U1t[1])),
    "If some points count more, the move step uses a weighted mean and nothing else changes.",
    "A house with four kids pulls the bus stop towards it four times as hard as a house with one.",
    [("weighted mean", "an average where some values count more than others"),
     ("weight", "how many times a point counts")]),
),

# =================================================================== q02
D("c3w1-q02",
  recall=M("Why one run is not enough, and how to pick the winner.",
    """<p>From memory: why can two runs of k-means on the same data give different answers? How should
the starting centroids be chosen, how many runs are typical, and how do you pick the winner?</p>""",
    """<p>k-means only ever reaches a <b>local</b> optimum: a spot where neither step can improve
<var>J</var>. Which one it reaches depends entirely on the starting centroids.</p>
<p>Start each run at <var>K</var> <b>distinct training examples</b> chosen at random. Run it 50 to
1,000 times and keep the run with the <b>lowest <var>J</var></b>. All runs use the same <var>K</var>,
so their costs are comparable.</p>""",
    "k-means finds a local optimum that depends on the start, so run it many times and keep the lowest J.",
    "Roll a ball down a bumpy hill from many places and keep the one that ended up in the deepest dip.",
    [("local optimum", "a spot no single step can improve, though a better spot exists elsewhere"),
     ("restart", "run the whole algorithm again from a new random start"),
     ("J", "the cost: average squared distance from each point to its own centroid")]),

  work=M("Two starts, two answers.",
    """<p>Points: %s. <var>K</var> = 3. Run k-means to convergence from two starts, then compute
<var>J</var> for each:</p>
<ol><li>Start A: centroids at %s.</li><li>Start B: centroids at %s.</li></ol>
<p>Which run do you keep?</p>""" % (_row(X2, 0), _row(GOOD2, 0), _row(BAD2, 0)),
    """<p><b>Start A</b> ends at centroids %s with clusters {%s}, {%s}, {%s}: <var>J</var> = <b>%s</b>.</p>
<p><b>Start B</b> ends at %s: two centroids share the left pair and the third has to cover {%s}.
<var>J</var> = <b>%s</b>, about <b>%s times</b> worse.</p>
<p>Run B converged correctly &mdash; no assign step could improve it &mdash; and is still wrong. Keep
A, the lower <var>J</var>.</p>""" % (
        _row(MUG2), _members(X2, CG2, 0), _members(X2, CG2, 1), _members(X2, CG2, 2), n(JG2, 3),
        _row(MUB2), _members(X2, CB2, 2), n(JB2, 3), n(RATIO2, 0)),
    "A converged run can still be a bad one; only comparing J across runs exposes it.",
    "Two flags landed on the same small crowd, so the other two crowds had to share one flag. "
    "Nobody will ever move to fix it.",
    [("converge", "reach a point where nothing changes any more"),
     ("compare runs", "line up the final J of each run and keep the smallest")]),

  spot=M("Fifty restarts that are all the same run.",
    """<p>A script meant to run k-means %d times on the six points above:</p>%s
<p>It reports %d costs and every one is %s. Which line defeats the restarts?</p>""" % (
        RESTARTS2,
        code("np.random.seed(0)\n"
             "start = X[np.random.choice(6, 3, replace=False)]\n"
             "for attempt in range(50):\n"
             "    mu = start.copy()\n"
             "    mu = run_kmeans(X, mu)"),
        RESTARTS2, n(JB2, 3)),
    """<p><b>Line 2</b>, because it sits <b>outside</b> the loop. The start is drawn once and reused, and
once the start is fixed, both steps are deterministic, so %d runs give <b>%d</b> distinct answer.</p>
<p>Move the random choice inside the loop. Done that way, %d of the %d fresh starts reach
<var>J</var> = %s, and the lowest over all %d is <b>%s</b>. The randomness is in the start and
nowhere else, so the restarts must vary the start.</p>""" % (
        RESTARTS2, SAME2, GOODN2, RESTARTS2, n(JG2, 3), RESTARTS2, n(BEST2, 3)),
    "Restarts only help if each one starts somewhere new.",
    "Dropping the ball from the very same spot fifty times gives you the same dip fifty times.",
    [("seed", "a number that makes random draws repeat exactly"),
     ("np.random.choice", "picks items at random; <code>replace=False</code> means no repeats")]),

  transfer=M("How lucky does a random start need to be?",
    """<p>Suppose the data has <var>K</var> equal-sized, well-separated clusters and you pick <var>K</var>
random training points as the start. The chance that every cluster gets exactly one is
<var>K</var>! / <var>K</var><sup><var>K</var></sup>. Compute it for <var>K</var> = %s, and how many
restarts give a %s chance of at least one such start.</p>""" % (
        ", ".join(str(k) for k, _, _ in LUCK2), pc(TARGET2, 0)),
    """<table><thead><tr><th>K</th><th>chance of one-per-cluster</th><th>restarts for %s</th></tr></thead>
<tbody>%s</tbody></table>
<p>The chance collapses as <var>K</var> grows, which is why a handful of runs is plenty at
<var>K</var> = 2 and a handful is hopeless at <var>K</var> = 10. These counts are pessimistic: an imperfect start often still
slides into the good answer, and k-means++ deliberately spreads the starts apart. The shape is the
point &mdash; the risk of a bad local optimum climbs steeply with <var>K</var>.</p>""" % (pc(TARGET2, 0), "".join(
        "<tr><td>%d</td><td>%s</td><td>%s</td></tr>" % (k, pc(p, 2), big(r)) for k, p, r in LUCK2)),
    "The more clusters, the less likely a random start is a good one, so the more restarts you need.",
    "Dropping two flags so each lands in a different playground is easy. Dropping ten so every one of "
    "ten playgrounds gets exactly one almost never happens by luck.",
    [("K!", "K &times; (K&minus;1) &times; &hellip; &times; 1, the number of ways to order K things"),
     ("k-means++", "a smarter start that places each new centroid far from the ones already chosen")]),
),

# =================================================================== q03
D("c3w1-q03",
  recall=M("Write J and three facts about it.",
    """<p>From memory: write the k-means cost <var>J</var> using %s, %s and &mu;. Then state: can it rise
between iterations? Can it choose <var>K</var>? Is it convex? When can you compute it?</p>""" % (XI, CI),
    """<p><var>J</var> = (1/<var>m</var>) &Sigma;<sub><var>i</var></sub> &#8214;%s &minus;
&mu;<sub><var>c</var><sup>(<var>i</var>)</sup></sub>&#8214;&sup2; &mdash; the average squared distance
from each point to its <b>own</b> centroid.</p>
<ul><li><b>Never rises</b>: both steps can only lower it, so a rise means a bug.</li>
<li><b>Cannot choose <var>K</var></b>: it falls automatically as <var>K</var> grows, to 0 at
<var>K</var> = <var>m</var>.</li>
<li><b>Not convex</b>: there are local optima, hence restarts.</li>
<li><b>Computable at any iteration</b>, which is what lets you plot it and watch it fall.</li></ul>""" % XI,
    "J is the average squared distance to your own centroid; both steps shrink it, and it cannot pick K.",
    "Tie everyone to their flag with elastic. The score is how stretched the elastic is on average. "
    "Running to a nearer flag and moving flags to the middle both make it less stretched.",
    [("distortion", "another name for J"),
     ("convex", "bowl-shaped with only one bottom; J is not"),
     ("&mu;<sub>c<sup>(i)</sup></sub>", "the centroid of the cluster point i belongs to")]),

  work=M("Score the six-point run at every half-step.",
    """<p>Go back to the run on %s (start %s). Compute <var>J</var> after each assign and after each
move. Check it never rises.</p>""" % (_row(X1, 0), _row(MU1_0, 0)),
    """<table><thead><tr><th>round</th><th>after assign</th><th>after move</th></tr></thead><tbody>%s</tbody></table>
<p>For example, after the first assign: (%s) / %d = <b>%s</b>.</p>
<p>Every number is at most the one before. The move steps buy the big drops here; the round-2 assign
step, where the point %s switched, bought %s more.</p>""" % (
        "".join("<tr><td>%d</td><td>%s</td><td>%s</td></tr>" % (i + 1, n(a, 3), n(b, 3))
                for i, (a, b) in enumerate(J1)),
        SUM3, len(X1), n(J1[0][0], 3), n(SW1[0], 0), n(J1[0][1] - J1[1][0], 3)),
    "J falls at every half-step and stops when nothing moves.",
    "Each time anyone moves, the elastic bands get a little looser, never tighter.",
    [("half-step", "one assign step or one move step on its own"),
     ("monotone", "only ever going one way &mdash; here, down or flat")]),

  spot=M("&ldquo;J went up, so the move step is broken.&rdquo;",
    """<p>Points %s, <var>K</var> = 2, start %s. A team's cost line:</p>%s
<p>It prints %s after the assign step and %s after the move step. They conclude the move step has a
bug. Where is the bug really?</p>""" % (
        _row(X3, 0), _row(MU3_0, 0), code("J = np.mean(np.abs(x - mu[c]))"), n(ABS3_A), n(ABS3_M)),
    """<p><b>The cost line.</b> It measures plain distance; <var>J</var> uses <b>squared</b> distance. The
move step puts the centroid at the mean, %s, which is the best point for squared distance &mdash; and
not for plain distance, where the median, %s, would win.</p>
<p>With the square, <code>J = np.mean((x - mu[c]) ** 2)</code> goes %s &rarr; <b>%s</b>, down as
promised. The algorithm was fine; the alarm was measuring the wrong thing.</p>""" % (
        n(MU3[0]), n(MED3, 0), n(SQ3_A), n(SQ3_M)),
    "The never-rises check only works on the cost k-means actually minimises: squared distance.",
    "If you check that a game is getting easier by timing the wrong level, you will think it got "
    "harder when it didn't.",
    [("np.abs", "the size of a number with its sign dropped"),
     ("median", "the middle value when the numbers are put in order")]),

  transfer=M("Is J = %s good? Give it a yardstick." % n(FIN3),
    """<p>The six-point run finished at <var>J</var> = %s. A colleague asks whether that is small.
<var>J</var> has units (distance squared), so the raw number means nothing on its own. What would
<var>J</var> be with <var>K</var> = 1, and what fraction of the spread did two clusters remove?</p>""" % n(FIN3),
    """<p>With one cluster the centroid is the overall mean, so <var>J</var> is the average squared
distance from the mean &mdash; exactly the <b>variance</b> &sigma;&sup2; of the data: <b>%s</b>.</p>
<p>Two clusters took that to %s, removing <b>%s</b> of the spread. That is a scale-free number you
can compare across datasets and units; raw <var>J</var> is not. The same &sigma;&sup2; returns later
this week as half of a Gaussian.</p>""" % (n(VAR3), n(FIN3), pc(EXPL3)),
    "J at K = 1 is the variance, so 1 &minus; J / variance says how much spread the clusters explain.",
    "Saying a puzzle took 20 minutes means nothing until you know it usually takes 2 hours.",
    [("variance", "the average squared distance from the mean"),
     ("scale-free", "doesn't change if you switch units, like metres to centimetres")]),
),

# =================================================================== q04
D("c3w1-q04",
  recall=M("The elbow, and what to do when there isn't one.",
    """<p>From memory: what is the elbow method? Why can you not just pick the <var>K</var> with the
lowest <var>J</var>? What does Andrew recommend when the curve has no bend?</p>""",
    """<p>Plot the best <var>J</var> for each <var>K</var> and look for the <var>K</var> where the drops
suddenly become small.</p>
<p>The lowest <var>J</var> is always at the largest <var>K</var> you tried &mdash; down to 0 at one
cluster per point &mdash; so minimising it picks nonsense.</p>
<p>Often the curve has no clear bend. Then choose <var>K</var> by <b>what the clusters are for</b>:
the t-shirt maker weighs better fit against more production lines.</p>""",
    "J always falls as K rises, so pick K by its purpose when the curve gives no clear bend.",
    "How many teams should the class split into? It depends on the game, not on the kids.",
    [("elbow", "the point where a falling curve suddenly flattens"),
     ("downstream purpose", "what the clusters will be used for afterwards")]),

  work=M("Two J curves: find the elbow, or prove there is none.",
    """<p>Best-of-%d <var>J</var> for two sets of %d points in 2-D &mdash; one built from three blobs,
one spread evenly:</p>
<table><thead><tr><th>K</th>%s</tr></thead><tbody><tr><th>blobs</th>%s</tr><tr><th>even</th>%s</tr></tbody></table>
<p>For each, compute the drop from each <var>K</var> to the next, and each drop divided by the one
before. Where is the elbow?</p>""" % (
        STARTS4, len(UNIF4), "".join("<th>%d</th>" % k for k in KS4), "".join("<td>%s</td>" % n(v, 3) for v in JB4),
        "".join("<td>%s</td>" % n(v, 3) for v in JU4[:len(KS4)])),
    """<table><thead><tr><th></th>%s</tr></thead><tbody>
<tr><th>blobs: drop</th>%s</tr><tr><th>blobs: ratio</th><td></td>%s</tr>
<tr><th>even: drop</th>%s</tr><tr><th>even: ratio</th><td></td>%s</tr></tbody></table>
<p><b>Blobs:</b> going 3 &rarr; 4 buys only %s of what 2 &rarr; 3 bought. That collapse is the elbow, at
<var>K</var> = 3.</p>
<p><b>Even:</b> every drop is %s to %s of the one before. No collapse, no elbow &mdash; this is the
smooth curve the quiz describes, and the data really has no natural number of groups. Choose by
purpose.</p>""" % (
        "".join("<th>%d&rarr;%d</th>" % (k, k + 1) for k in KS4[:-1]),
        "".join("<td>%s</td>" % n(v, 2) for v in DB4), "".join("<td>%s</td>" % n(v, 2) for v in RB4),
        "".join("<td>%s</td>" % n(v, 2) for v in DU4), "".join("<td>%s</td>" % n(v, 2) for v in RU4),
        pc(RB4[1], 0), pc(RU4.min(), 0), pc(RU4.max(), 0)),
    "An elbow is a sudden collapse in the drops; a steady shrink means there is none.",
    "If each extra helper saves a bit less time than the last, there is no magic number of helpers. "
    "If the fourth saves almost nothing, three was the number.",
    [("drop", "how much J falls when you add one more cluster"),
     ("ratio", "this drop divided by the previous one")]),

  spot=M("Picking K with argmin.",
    """<p>Nine points: %s. A script computes the best <var>J</var> for every <var>K</var> from 1 to 9,
then:</p>%s
<p>It prints <code>best_K = %d</code>. Which line is wrong?</p>""" % (
        _row(X4s, 0), code("best_K = np.argmin(J_by_K) + 1"), PICK4),
    """<p><b>The <code>best_K</code> line.</b> The <var>J</var> values are %s: strictly falling, ending at <b>%s</b> when
every point is its own cluster. <code>argmin</code> will always return the largest <var>K</var> it is
given.</p>
<p>The drops tell the truth: 2 &rarr; 3 removes %s, 3 &rarr; 4 only %s. The elbow is at 3, which is how
the points were laid out.</p>""" % (
        _row(JS4, 2), n(JS4[-1], 0), n(JS4[1] - JS4[2], 2), n(JS4[2] - JS4[3], 2)),
    "J rewards more clusters automatically, so the smallest J is never the answer for K.",
    "If you gave a prize for the tidiest groups, the winner would always put every kid in a group "
    "of one.",
    [("argmin", "the position of the smallest value in a list"),
     ("monotone decreasing", "every value is at most the one before")]),

  transfer=M("How many delivery depots? Let money choose K.",
    """<p>%d shops are spread evenly over a %s km &times; %s km area (the &ldquo;even&rdquo; data above,
in km). Each depot costs %s a month in rent. Each shop gets %d deliveries a month, each a round trip
at %s per km. k-means places the depots; the average shop-to-depot distance for each <var>K</var>
is:</p>
<table><thead><tr><th>K</th>%s</tr></thead><tbody><tr><th>avg km</th>%s</tr></tbody></table>
<p>Which <var>K</var> do you pick?</p>""" % (
        SHOPS4, n(SIDE4, 0), n(SIDE4, 0), big(RENT4), DROPS4, n(PERKM4, 2),
        "".join("<th>%d</th>" % k for k in range(1, 9)),
        "".join("<td>%s</td>" % n(v, 2) for v in DIST4)),
    """<p>Monthly cost = %s &times; <var>K</var> + %d &times; %d &times; 2 &times; %s &times; avg km =
%s&times;<var>K</var> + %s &times; avg km.</p>
<table><thead><tr><th>K</th>%s</tr></thead><tbody><tr><th>total</th>%s</tr></tbody></table>
<p>The cheapest is <b><var>K</var> = %d</b>. The <var>J</var> curve for this data had no elbow; the
business question had a clear answer. (k-means minimises squared distance rather than distance, which
is close enough for planning.)</p>""" % (
        big(RENT4), SHOPS4, DROPS4, n(PERKM4, 2), big(RENT4), big(TRIP4),
        "".join("<th>%d</th>" % k for k in range(1, 9)), "".join("<td>%s</td>" % big(v) for v in TOT4),
        KBEST4),
    "When the curve is silent, put a price on each extra cluster and let the cost decide.",
    "More depots mean shorter drives but more rent. The right number is where the total bill is "
    "smallest.",
    [("trade-off", "getting more of one good thing costs you some of another"),
     ("depot", "a warehouse the delivery vans start from")]),
),

# =================================================================== q05
D("c3w1-q05",
  recall=M("Where the normal examples go, and where the anomalies go.",
    """<p>From memory: how do you split a dataset of many normal examples and a few known anomalies for
anomaly detection? What is each set used for? What does Andrew suggest with only a couple of
anomalies?</p>""",
    """<ul><li><b>Training</b>: normal examples only (about 60%% of them). Fit &mu;<sub><var>j</var></sub>
and &sigma;<sub><var>j</var></sub>&sup2;.</li>
<li><b>Cross-validation</b>: normal examples plus about half the anomalies. Choose %s and the
features.</li>
<li><b>Test</b>: normal examples plus the other anomalies. Measure once.</li></ul>
<p>With very few anomalies, drop the test set and use cross-validation only, accepting that the final
number will be optimistic.</p>""" % EPS,
    "Fit on normal examples only; spend every anomaly on choosing &epsilon; and measuring.",
    "To learn what a healthy heartbeat sounds like, listen only to healthy hearts. Keep the few sick "
    "ones for testing whether you can tell.",
    [("anomaly", "an example that is unusual, like a faulty engine"),
     ("&epsilon;", "the threshold: flag anything with p(x) below it")]),

  work=M("Split the 10,020, then see what one stray anomaly does.",
    """<p>(a) Split %s normal examples and %d anomalies the standard way.</p>
<p>(b) A small training set should be the normal values %s, but one anomaly, %s, slipped in. Compute
&mu; and &sigma;&sup2; with and without it. How many standard deviations from &mu; is a cross-validation
anomaly at %s in each case?</p>""" % (big(NORM5), ANOM5, _row(N5, 0), n(BAD5, 0), n(Q5, 0)),
    """<p>(a) Training: <b>%s normal, 0 anomalies</b>. Cross-validation: %s normal + %d anomalies.
Test: %s normal + %d anomalies. Anomalies are only %s of the cross-validation set.</p>
<p>(b) Clean: &mu; = %s, &sigma;&sup2; = %s, so %s is <b>%s</b> standard deviations out &mdash; flagged
easily. With the stray anomaly: &mu; = %s, &sigma;&sup2; = <b>%s</b>, so %s is now only <b>%s</b>
&mdash; closer to the mean than every one of the eight genuine normals, which sit %s to %s out.
p(%s) rose by a factor of about %s.</p>
<p>The model's whole job is to describe normal. One contaminating point widened that description until
another anomaly looked typical.</p>""" % (
        big(TR5), big(CV5), ACV5, big(TE5), ATE5, pc(SHARE5, 2),
        n(MU5), n(VAR5), n(Q5, 0), n(Z5, 2), n(MU5c, 2), n(VAR5c, 1), n(Q5, 0), n(abs(Z5c), 2),
        n(ZN5c.min(), 2), n(ZN5c.max(), 2), n(Q5, 0), sci(P5c / P5)),
    "Anomalies in the training set stretch the model of normal until anomalies look normal.",
    "If one shouting kid is in the room while you learn what a quiet class sounds like, you'll decide "
    "quiet classes are quite loud.",
    [("contaminate", "mix something in that shouldn't be there"),
     ("standard deviation", "&sigma;, the typical distance from the mean")]),

  spot=M("A shuffled 60/20/20 split.",
    """<p>A team's pipeline for %s normal examples and %d anomalies:</p>
<ol><li>Shuffle all %s examples together.</li>
<li>Take the first 60%% as training, the next 20%% as cross-validation, the last 20%% as test.</li>
<li>Fit &mu; and &sigma;&sup2; per feature on the training set.</li>
<li>Choose %s by F1 on cross-validation.</li></ol>
<p>Which line breaks the method, and what does it cost?</p>""" % (
        big(NORM5), ANOM5, big(NORM5 + ANOM5), EPS),
    """<p><b>Line 2</b> (together with line 1). It treats anomalies like any other example, so on average
<b>%s</b> of the %d land in training, leaving only %s for cross-validation and %s for test. One real
shuffle gave %d / %d / %d.</p>
<p>Two losses: the anomalies in training are fitted as if they were normal, widening &sigma;; and
%s is now chosen from a handful of anomalies, so recall can only move in steps of %s. Split the normal
examples 60/20/20 and put every anomaly in cross-validation and test.</p>""" % (
        n(EXP5[0], 0), ANOM5, n(EXP5[1], 0), n(EXP5[2], 0), RTR5, RCV5, RTE5, EPS, pc(1 / RCV5, 0)),
    "The anomalies never go in training; the random split is exactly the thing to avoid.",
    "If you hide half your few test questions inside the textbook you learn from, you have fewer left "
    "to test yourself with, and you've learned some wrong answers.",
    [("shuffle", "mix the order randomly"),
     ("recall", "the fraction of real anomalies the detector catches")]),

  transfer=M("Only two anomalies, ever.",
    """<p>A new production line has %s normal parts on record and only %d known faults. How would you
split it, and how finely can you measure recall?</p>""" % (big(LINE5), TINY5),
    """<p>Train on normal parts only. Put both faults, with some normal parts, in cross-validation and
<b>drop the test set</b> &mdash; Andrew's advice when anomalies are this scarce.</p>
<p>With %d anomalies, recall can only be %s. One fault more or less changes it by %s, so you are
choosing %s from almost no evidence, and the number you report is optimistic because the same two
faults chose it. Say so in the report, and collect more faults before trusting it.</p>""" % (
        TINY5, ", ".join(pc(v, 0) for v in STEPS5), pc(1 / TINY5, 0), EPS),
    "With very few anomalies, skip the test set and treat the cross-validation number as optimistic.",
    "If you only have two practice questions, getting one wrong swings your score by half. That "
    "score can't tell you much.",
    [("resolution", "the smallest change a measurement can show"),
     ("optimistic", "looks better than it will really be")]),
),

# =================================================================== q06
D("c3w1-q06",
  recall=M("The one question that decides it.",
    """<p>From memory: what question decides between anomaly detection and supervised learning? List
two more factors from the comparison table, and give one example of each.</p>""",
    """<p>The deciding question: <b>will future positive examples look like the ones you already have?</b>
Yes &rarr; supervised. No &rarr; anomaly detection.</p>
<p>Also: anomaly detection suits very few positives (0 to 20 or so) and many different kinds of
anomaly; supervised learning needs enough positives of each kind to learn what they look like.</p>
<p>Examples: aircraft-engine faults &rarr; anomaly detection; spam &rarr; supervised.</p>""",
    "If future positives will resemble past ones, learn them with a classifier; if not, model normal.",
    "If tomorrow's tricks look like yesterday's, learn the tricks. If every trick is brand new, learn "
    "what normal looks like and watch for anything else.",
    [("positive example", "an example of the thing you're hunting for, like a fraud"),
     ("classifier", "a model that learns what each class looks like from labels"),
     ("density estimation", "modelling how likely each normal-looking x is")]),

  work=M("Positives per kind, for four problems.",
    """<p>For each problem, compute positive examples per known kind, then decide:</p>
<table><thead><tr><th>problem</th><th>positives</th><th>known kinds</th><th>new kinds expected?</th></tr></thead><tbody>%s</tbody></table>""" % "".join(
        "<tr><td>%s</td><td>%s</td><td>%d</td><td>%s</td></tr>" % (nm, big(pos), k, new)
        for nm, pos, k, new in PROB6),
    """<table><thead><tr><th>problem</th><th>per kind</th><th>choose</th></tr></thead><tbody>%s</tbody></table>
<p>Hundreds or thousands of examples of each kind, and no new kinds expected &rarr; a classifier can
learn them. A handful per kind with new kinds on the way &rarr; model normal instead.</p>""" % "".join(
        "<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (
            nm, big(per) if per >= 100 else n(per, 1), "<b>supervised</b>" if new == "no" else "<b>anomaly detection</b>")
        for nm, pos, k, per, new in PER6),
    "Count examples per kind and ask whether new kinds will appear.",
    "If you've seen a thousand of each trick, you can learn the tricks. If you've seen one of each and "
    "more are coming, you can't.",
    [("kind", "one type of positive, like one fraud scheme"),
     ("per kind", "positives divided by the number of kinds")]),

  spot=M("&ldquo;Fraud is rare, so anomaly detection.&rdquo;",
    """<p>A bank has %s transactions, of which %s are fraud from schemes it expects to keep seeing. An
analyst writes:</p>
<ol><li>Fraud is only %s of transactions.</li>
<li>A rare class means anomaly detection.</li>
<li>So we fit Gaussians to normal transactions and set %s on cross-validation.</li></ol>
<p>Which line is wrong?</p>""" % (big(TXN6), big(FRAUD6), pc(RATE6), EPS),
    """<p><b>Line 2.</b> Rarity as a percentage is not the test. %s labelled frauds is plenty to learn
from, and they are expected to resemble future fraud, so a <b>supervised</b> classifier will do better
here. The analyst would be throwing away %s labels.</p>
<p>A skewed class is a reason to use precision and recall instead of accuracy, not a reason to switch
algorithms. A bank may still run a detector alongside, for the schemes nobody has seen.</p>""" % (
        big(FRAUD6), big(FRAUD6)),
    "A rare class is not the test; whether the positives repeat themselves is.",
    "Lions are rare at the zoo, but if you've got six thousand lion photos you can learn what a lion "
    "looks like.",
    [("skewed", "one class is much bigger than the other"),
     ("label", "the known answer for an example: fraud or not")]),

  transfer=M("Counterfeit banknotes.",
    """<p>A central bank holds %s seized counterfeits, almost all from two printing gangs it has since
caught. New counterfeiters will use new printers and new tricks. What would you build?</p>""" % big(NOTES6),
    """<p><b>Both.</b> A classifier trained on the %s seized notes will catch more notes from those two
gangs' presses, should any still be in circulation. But the real threat is the <b>next</b>
counterfeiter, whose notes look like neither gang's, so add a density model of <b>genuine</b> notes
that flags anything improbable.</p>
<p>Many positives does not settle it on its own: the positives you have are all of a kind that will
not recur.</p>""" % big(NOTES6),
    "Many positives only help if future positives look like them.",
    "Knowing two forgers' handwriting won't help you spot a third forger. Knowing real money really "
    "well will.",
    [("counterfeit", "a fake copy, made to look real"),
     ("genuine", "the real thing")]),
),

# =================================================================== q07
D("c3w1-q07",
  recall=M("Why transform, how, and where.",
    """<p>From memory: why should a skewed feature be transformed before fitting the Gaussian model? Name
three transforms. Where else must the same transform be applied? Why does scaling to 0&ndash;1 not
help?</p>""",
    """<p>The model fits one Gaussian per feature. On a skewed feature that bell sits in the wrong place
and is too wide, so ordinary large values look anomalous.</p>
<p>Transforms: <code>np.log(x + c)</code>, <code>np.sqrt(x)</code>, <code>x ** 0.3</code> (any fractional
power). Plot the histogram, try, plot again.</p>
<p>Apply the identical transform to cross-validation, test and live data. Scaling only shifts and
stretches: the shape, and the skew, are unchanged.</p>""",
    "Transform skewed features until they look like a bell, and use the same transform everywhere.",
    "If the hill is lopsided, squash the long side until it looks like a proper hill, because the "
    "computer only knows proper hills.",
    [("skewed", "lopsided, with a long tail on one side"),
     ("transform", "apply the same function, like log, to every value")]),

  work=M("Fit the bell before and after taking logs.",
    """<p>A feature's training values: %s.</p>
<ol><li>Take log<sub>10</sub> of each and compute their &mu; and &sigma;.</li>
<li>Raw, the fit is &mu; = %s, &sigma; = %s. How many &sigma; from &mu; are the smallest and largest
values, on each scale?</li></ol>""" % (_row(X7, 0), big(MU7), big(SD7)),
    """<p>Logs: %s, so &mu; = <b>%s</b>, &sigma; = <b>%s</b>.</p>
<table><thead><tr><th></th><th>value %s</th><th>value %s</th></tr></thead><tbody>
<tr><td>raw</td><td>%s&sigma;</td><td>%s&sigma;</td></tr>
<tr><td>log</td><td>%s&sigma;</td><td>%s&sigma;</td></tr></tbody></table>
<p>Each extreme appears once. On the raw scale %s looks %s times as far out as %s; after the log they
are equally unusual. The raw bell also puts <b>%s</b> of its probability on negative values, which this
feature can never take. The skewness drops from %s to %s.</p>""" % (
        _row(L7, 0), n(LMU7, 2), n(LSD7, 3), n(X7.min(), 0), big(X7.max()),
        n(ZLO7, 2), n(ZHI7, 2), n(LZLO7, 2), n(LZHI7, 2),
        big(X7.max()), n(abs(ZHI7 / ZLO7), 1), n(X7.min(), 0), pc(NEG7, 0), n(SK7, 2), n(LSK7, 2)),
    "On a skewed feature the bell is in the wrong place; after the log it fits.",
    "One giant in a room of children makes the &ldquo;average height&rdquo; useless. Counting how many "
    "times you multiply by ten, instead of counting centimetres, puts everyone back on a fair scale.",
    [("log<sub>10</sub>", "how many times you multiply 10 to get the number: log<sub>10</sub>(1000) = 3"),
     ("skewness", "a number for lopsidedness: 0 is a symmetric bell")]),

  spot=M("Scaling sold as a fix for skew.",
    """<p>For the feature above, a teammate writes:</p>%s
<p>&ldquo;Now it is between 0 and 1, so the Gaussian fits.&rdquo; Which line fails to do its job?</p>""" % code(
        "x = (x - x.min()) / (x.max() - x.min())\n"
        "mu, var = x.mean(), x.var()"),
    """<p><b>Line 1.</b> Subtracting and dividing by constants moves and stretches the values; it never
changes their shape. The skewness is %s before and <b>%s</b> after &mdash; identical. Every value keeps
the same number of &sigma; from the mean, so the same values get flagged.</p>
<p>Replace it with a shape-changing transform, <code>x = np.log10(x)</code>, which takes the skewness to
%s. Scale afterwards if you like.</p>""" % (n(SK7, 2), n(MSK7, 2), n(LSK7, 2)),
    "Scaling changes the units, not the shape; only a transform like log fixes skew.",
    "Shrinking a photo of a lopsided hill doesn't make it less lopsided.",
    [("min-max scaling", "squeezing values into 0 to 1"),
     ("shape", "how the values are spread: bell, lopsided, two humps")]),

  transfer=M("A feature skewed the other way.",
    """<p>Phone battery level at the moment of a crash, in %%: most readings sit near 100, with a long tail
down towards %s. The skewness is %s &mdash; lopsided to the <b>left</b>. <code>np.log(x)</code> would make
it worse. What would you try?</p>""" % (n(B7.min(), 0), n(BT7[0][1], 2)),
    """<p>Either stretch the crowded top with a power <b>above</b> 1, or flip the feature so the tail points
right and then take a log:</p>
<table><thead><tr><th>transform</th><th>skewness</th></tr></thead><tbody>%s</tbody></table>
<p>Here <code>x ** 6</code> wins. The flip, 101 &minus; x, reverses the order, which does not matter: the
Gaussian is symmetric, so an unusual value is unusual on either side. Same procedure as always
&mdash; try, re-plot, keep the most bell-like.</p>""" % "".join(
        "<tr><td><code>%s</code></td><td>%s</td></tr>" % (nm, n(s, 2)) for nm, s in BT7),
    "For a left tail, use a power above 1, or flip the feature and take a log.",
    "If the hill leans the other way, you squash the other side.",
    [("left-skewed", "the long tail points towards small values"),
     ("power above 1", "like x squared: spreads out the big values")]),
),

# =================================================================== q08
D("c3w1-q08",
  recall=M("Why accuracy lies, and what to report instead.",
    """<p>From memory: why is accuracy useless for judging an anomaly detector? Which metrics do you use,
and which class is the &ldquo;positive&rdquo; one?</p>""",
    """<p>Anomalies are a tiny fraction of the data, so a detector that flags <b>nothing</b> scores near
100%% accuracy and is worthless.</p>
<p>Treat anomaly as <var>y</var> = 1 and report <b>precision</b> (of the flags, how many were real),
<b>recall</b> (of the real anomalies, how many were flagged) and <b>F1</b>. Choose %s by F1 on the
cross-validation set.</p>""" % EPS,
    "On rare anomalies, accuracy rewards doing nothing; precision, recall and F1 do not.",
    "If only one sweet in a jar of a thousand is poisoned, saying &ldquo;all safe&rdquo; is right 999 "
    "times and still a terrible food taster.",
    [("precision", "of everything you flagged, the fraction that was really an anomaly"),
     ("recall", "of all real anomalies, the fraction you flagged"),
     ("F1", "one score that is low if either precision or recall is low")]),

  work=M("Score a detector on the cross-validation set.",
    """<p>Cross-validation: %s normal examples and %d anomalies. At the chosen %s the detector flags %d
examples, %d of them real anomalies. Compute accuracy, precision, recall and F1, then the accuracy of a
detector that flags nothing.</p>""" % (big(CVN8), CVA8, EPS, FLAG8, HIT8),
    """<p>TP = %d, FP = %d, FN = %d, TN = %s.</p>
<p>Accuracy = (%d + %s) / %s = <b>%s</b>. Precision = %d / %d = <b>%s</b>. Recall = %d / %d =
<b>%s</b>. F1 = <b>%s</b>.</p>
<p>Flag-nothing accuracy = %s / %s = <b>%s</b>. The two accuracies differ by %s points; the useful
detector and the useless one are nearly indistinguishable. Recall separates them: %s against 0.</p>""" % (
        TP8, FP8, FN8, big(TN8), TP8, big(TN8), big(N8), pc(ACC8, 2), TP8, FLAG8, n(P8, 3), TP8, CVA8,
        n(R8, 2), n(F8, 3), big(CVN8), big(N8), pc(NULL8, 2), n(100 * (ACC8 - NULL8), 2), n(R8, 2)),
    "Accuracy barely moves between useful and useless detectors; recall and precision do.",
    "The kid who catches 8 of 10 hiding friends and the kid who catches none get almost the same "
    "&ldquo;right answers&rdquo; score, because most of the garden is empty.",
    [("TP / FP / FN / TN", "caught / false alarm / missed / correctly ignored"),
     ("base rate", "how common anomalies are to begin with")]),

  spot=M("Tuning &epsilon; by accuracy.",
    """<p>Same cross-validation set. A script tries four thresholds and keeps the best:</p>
<table><thead><tr><th>threshold</th><th>TP</th><th>FP</th></tr></thead><tbody>%s</tbody></table>
<ol><li>For each threshold, compute accuracy on cross-validation.</li>
<li>Keep the threshold with the highest accuracy.</li>
<li>Report it.</li></ol>
<p>Which line is wrong, and which threshold does it choose?</p>""" % "".join(
        "<tr><td>%s</td><td>%d</td><td>%d</td></tr>" % (lab, tp, fp) for lab, tp, fp, _, _ in SWS8),
    """<table><thead><tr><th>threshold</th><th>accuracy</th><th>F1</th></tr></thead><tbody>%s</tbody></table>
<p><b>Line 1</b> (and so line 2). Accuracy is highest at %s, which flags <b>nothing</b> &mdash; every
anomaly gets past, because catching each one costs at least one false alarm and accuracy counts those
equally. F1 picks %s, catching %d of %d. Score thresholds by F1.</p>""" % (
        "".join("<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (lab, pc(a, 2), n(f, 3))
                for lab, _, _, a, f in SWS8),
        SWS8[IACC8][0], SWS8[IF18][0], SWS8[IF18][1], CVA8),
    "Choose &epsilon; by F1; accuracy will happily choose a detector that never fires.",
    "If you mark a guard only on how few times they shout wrongly, the best guard never shouts at "
    "all &mdash; even at a real burglar.",
    [("threshold", "&epsilon;, the cut-off below which p(x) counts as an anomaly"),
     ("sweep", "try many thresholds and score each one")]),

  transfer=M("&ldquo;%s of normal traffic passes, %s of fraud caught.&rdquo;" % (pc(1 - FAR8, 0), pc(REC8, 0)),
    """<p>A vendor's detector wrongly flags %s of normal transactions and catches %s of fraud. Fraud is
%s of your transactions. Out of %s transactions, how many alerts are real?</p>""" % (
        pc(FAR8, 0), pc(REC8, 0), pc(BASE8), big(VOL8)),
    """<p>Fraud: %s &times; %s = %s cases, of which %s &times; %s = <b>%s</b> are caught. Normal: %s,
of which %s &times; %s = <b>%s</b> are wrongly flagged.</p>
<p>Precision = %s / (%s + %s) = <b>%s</b>. Only about 1 alert in %s is fraud; the rest is noise
for your investigators. Both of the vendor's numbers were true and neither was precision. On rare
anomalies, always ask for it.</p>""" % (
        big(VOL8), pc(BASE8), big(VA8), pc(REC8, 0), big(VA8), big(VTP8), big(VOL8 - VA8), pc(FAR8, 0),
        big(VOL8 - VA8), big(VFP8), big(VTP8), big(VTP8), big(VFP8), pc(VPREC8), n(1 / VPREC8, 0)),
    "A small false-alarm rate on a huge normal class still swamps the real anomalies.",
    "If a smoke alarm beeps wrongly once in a hundred days, but there's a fire once in a thousand, "
    "most beeps are still about toast.",
    [("false-alarm rate", "the fraction of normal examples wrongly flagged"),
     ("precision", "of the alarms, the fraction that were real")]),
),

# =================================================================== q09
D("c3w1-q09",
  recall=M("What independence means here, and the two fixes.",
    """<p>From memory: write p(<var>x</var>) for the anomaly model. What does multiplying the
per-feature Gaussians assume? What kind of anomaly does that assumption miss, and what are the two
fixes?</p>""",
    """<p>p(<var>x</var>) = &prod;<sub><var>j</var></sub> p(<var>x</var><sub><var>j</var></sub>;
&mu;<sub><var>j</var></sub>, &sigma;<sub><var>j</var></sub>&sup2;). Multiplying assumes the features
are <b>independent</b>: knowing one tells you nothing about another.</p>
<p>It misses anomalies that live only in the <b>combination</b> &mdash; each feature ordinary on its
own, the pair impossible. Fixes: engineer a feature for the combination, such as a <b>ratio</b>, or use
a <b>multivariate Gaussian</b> that models correlations.</p>""",
    "Multiplying per-feature bells can't see an odd combination of ordinary values; a ratio feature can.",
    "Being tall is normal and being light is normal, but a very tall, very light person is unusual. "
    "Checking height and weight separately never notices.",
    [("independent", "knowing one tells you nothing about the other"),
     ("&prod;", "multiply all of them together"),
     ("multivariate Gaussian", "one bell over several features at once, which can tilt")]),

  work=M("A stuck server that looks fine, feature by feature.",
    """<p>Five normal servers have network traffic %s and CPU load %s. A new server has traffic %s and
CPU %s.</p>
<ol><li>Fit &mu; and &sigma;&sup2; per feature. How many &sigma; out is the new server on each?</li>
<li>Compute CPU / traffic for every server. How many &sigma; out is the new one?</li></ol>""" % (
        _row(T9, 0), _row(C9, 1), n(NEW9[0], 0), n(NEW9[1], 0)),
    """<p>(1) Traffic: &mu; = %s, &sigma;&sup2; = %s, so <b>%s&sigma;</b>. CPU: &mu; = %s, &sigma;&sup2; = %s,
so <b>%s&sigma;</b>. Both ordinary. p(<var>x</var>) = %s, which is <b>higher</b> than for %d of the five
genuine servers: the model rates the broken machine as more normal than real ones.</p>
<p>(2) Ratios: %s, with &mu; = %s and &sigma; = %s. The new server's ratio is %s, which is <b>%s&sigma;</b>
out. One engineered feature turned an invisible anomaly into an unmissable one.</p>""" % (
        n(MT9, 0), n(VT9, 0), n(ZT9, 2), n(MC9, 0), n(VC9, 2), n(ZC9, 2), n(PNEW9, 4), LOWER9,
        _row(R9, 3), n(R9.mean(), 3), n(R9.std(), 3), n(RNEW9, 0), n(ZR9, 0)),
    "Two ordinary values can make an impossible pair, and only a feature about the pair can see it.",
    "A shop that's busy with lots of customers is normal. A shop that's busy with no customers is "
    "strange, and you only notice if you look at both together.",
    [("ratio", "one number divided by another"),
     ("engineered feature", "a new feature you build from the ones you have")]),

  spot=M("&ldquo;Raise &epsilon; until it's caught.&rdquo;",
    """<p>On a fleet of %s normal servers (traffic and CPU move together), the independent model misses
the stuck server above. An engineer's fix:</p>
<ol><li>Compute p(<var>x</var>) for the stuck server.</li>
<li>Set %s just above it, so the stuck server is flagged.</li>
<li>Ship it.</li></ol>
<p>Which line is wrong?</p>""" % (big(len(BT9)), EPS),
    """<p><b>Line 2.</b> &epsilon; is one dial for <b>every</b> example. Raising it to catch this server also
flags <b>%s</b> of the normal fleet, because the model ranks those normal servers as less probable than
the broken one. The missing signal is not a threshold problem; the model cannot represent it.</p>
<p>Add the ratio feature: the stuck server's ratio is %s&sigma; out, while the most extreme normal server
is %s&sigma; out. It can be caught with no false alarms.</p>""" % (
        pc(BFLAG9), n(BZR9, 0), n(BZMAX9, 1)),
    "Moving &epsilon; changes how many things you flag, not what the model can see.",
    "Turning up a smoke alarm won't make it smell gas. It just beeps at more toast.",
    [("false alarm", "a normal example flagged as an anomaly"),
     ("fleet", "all the servers together")]),

  transfer=M("A tall, light child.",
    """<p>A school nurse's anomaly model uses height and weight for %s children. One child is %s cm and
%s kg. Compute how many &sigma; out each feature is. Then suggest one feature that would catch a
worryingly thin child.</p>""" % (big(len(HT9)), n(KID9[0], 0), n(KID9[1], 0)),
    """<p>Height: <b>%s&sigma;</b>. Weight: <b>%s&sigma;</b>. Neither is remarkable, so the product is
unremarkable.</p>
<p>The right combined feature is a ratio doctors already use: <b>BMI</b> = weight / height&sup2; (in
metres). This child's is %s against a group mean of %s, which is <b>%s&sigma;</b> out. The ratio
fix carries straight over from servers to children.</p>""" % (
        n(ZH9, 2), n(ZW9, 2), n(KBMI9, 1), n(BMI9.mean(), 1), n(ZB9, 1)),
    "When the anomaly is in how two features relate, build the feature that measures the relation.",
    "Tall is fine and light is fine. Tall and very light together is what a doctor notices.",
    [("BMI", "body-mass index: weight divided by height squared"),
     ("combined feature", "one number made from two")]),
),

# =================================================================== q10
D("c3w1-q10",
  recall=M("The bell, its two numbers, and the %d&ndash;%d&ndash;%s rule." % (R1_10, R2_10, n(R3_10, 1)),
    """<p>From memory: write p(<var>x</var>) for a Gaussian with mean &mu; and variance &sigma;&sup2;. How
do you estimate &mu; and &sigma;&sup2; from data? What fraction lies within 1, 2 and 3 standard
deviations?</p>""",
    """<p>p(<var>x</var>) = 1 / (&radic;(2&pi;) &sigma;) &middot; exp(&minus;(<var>x</var> &minus;
&mu;)&sup2; / (2&sigma;&sup2;)).</p>
<p>&mu; = (1/<var>m</var>) &Sigma; %s; &sigma;&sup2; = (1/<var>m</var>) &Sigma; (%s &minus;
&mu;)&sup2;. &sigma; is the square root of &sigma;&sup2;.</p>
<p>Within &plusmn;1&sigma;: about <b>%d%%</b>. &plusmn;2&sigma;: about <b>%d%%</b>. &plusmn;3&sigma;:
about <b>%s%%</b>.</p>""" % (XI, XI, R1_10, R2_10, n(R3_10, 1)),
    "Two numbers fix the bell; about %d, %d and %s percent lie within 1, 2 and 3 sigma." % (
        R1_10, R2_10, n(R3_10, 1)),
    "Most people are near average height, fewer are very tall or very short, and almost nobody is "
    "three steps away from the middle.",
    [("&mu;", "the mean, where the peak is"),
     ("&sigma;", "the standard deviation, how wide the bell is"),
     ("&sigma;&sup2;", "the variance, &sigma; times itself")]),

  work=M("Fractions of a bell with &mu; = %s, &sigma; = %s." % (n(MU10, 0), n(SD10, 0)),
    """<p>A Gaussian has &mu; = %s and &sigma; = %s. Using the rule, estimate the fraction of values:</p>
<ol><li>between %s and %s;</li><li>between %s and %s;</li><li>between %s and %s;</li>
<li>above %s.</li></ol>""" % (n(MU10, 0), n(SD10, 0), n(LO10, 0), n(HI10, 0), n(A10, 0), n(B10, 0),
                             n(A10, 0), n(HI10, 0), n(T10, 0)),
    """<ol><li>%s and %s are %s&sigma; either side: <b>%d%%</b> (exactly %s).</li>
<li>&plusmn;1&sigma;: <b>%d%%</b> (exactly %s).</li>
<li>Half of the &plusmn;1&sigma; band below plus half of the &plusmn;2&sigma; band above:
%d/2 + %d/2 = <b>%s%%</b> (exactly %s).</li>
<li>%s is +3&sigma;. Outside &plusmn;3&sigma; is %s%%, split between two tails: <b>%s%%</b> (exactly
%s).</li></ol>
<p>Fractions are areas between two points; the height of the curve at a point is not a fraction.</p>""" % (
        n(LO10, 0), n(HI10, 0), n(K10, 0), R2_10, pc(W2_10, 2), R1_10, pc(W1_10, 2),
        R1_10, R2_10, n(RULE_45_60, 1), pc(EX_45_60, 2), n(T10, 0), n(100 - R3_10, 1), n(RULE_65, 2),
        pc(EX_65, 3)),
    "Convert every boundary to &sigma;s from the mean, then read off the rule.",
    "Count how many &ldquo;steps&rdquo; from the middle each edge is. One step each way holds about "
    "two-thirds; two steps hold nearly everyone.",
    [("&plusmn;2&sigma;", "from two standard deviations below the mean to two above"),
     ("tail", "the thin part of the bell far from the middle")]),

  spot=M("Dividing by the variance.",
    """<p>A classmate fits the data with NumPy and asks what fraction lies below %s:</p>%s
<p>The fit gives &mu; = %s and <code>var</code> = %s, so they get <code>z</code> = %s, and conclude only
about %s of values lie between %s and %s. Which line is wrong?</p>""" % (
        n(HI10, 0), code("mu, var = x.mean(), x.var()\n"
             "z = (60 - mu) / var"),
        n(MU10, 0), n(VAR10, 0), n(ZBAD10, 1), pc(FBAD10, 0), n(LO10, 0), n(HI10, 0)),
    """<p><b>Line 2.</b> <code>x.var()</code> returns the variance &sigma;&sup2;, but a <var>z</var>-score divides
by the standard deviation &sigma; = &radic;%s = %s. Correct: <code>z = (60 - mu) / np.sqrt(var)</code> =
<b>%s</b>, and the fraction between %s and %s is about <b>%d%%</b>, not %s.</p>
<p>The same slip in an anomaly detector would make every point look far more ordinary than it is.</p>""" % (
        n(VAR10, 0), n(SD10, 0), n(K10, 0), n(LO10, 0), n(HI10, 0), R2_10, pc(FBAD10, 0)),
    "Distances are measured in &sigma;, never in &sigma;&sup2;.",
    "If you measure your step in square metres instead of metres, you'll get a silly number of steps.",
    [("z-score", "how many standard deviations a value is from the mean"),
     ("x.var()", "NumPy's variance &mdash; the square of the standard deviation")]),

  transfer=M("Ten features, ten 3&sigma; alarms.",
    """<p>A monitoring system checks %d independent, Gaussian features and alarms if <b>any</b> one is
beyond &plusmn;3&sigma;. What fraction of perfectly normal examples trip it? With %s normal
transactions a day, how many false alarms?</p>""" % (NF10, big(DAY10)),
    """<p>One feature stays inside with probability %s. All %d stay inside with probability %s<sup>%d</sup>
= %s, so <b>%s</b> of normal examples trip at least one alarm &mdash; about %s times the one-feature
rate of %s.</p>
<p>That is <b>%s</b> false alarms a day. Per-feature rules add up, which is the same reason
p(<var>x</var>) shrinks as you add features and %s must be re-tuned whenever the feature set
changes.</p>""" % (
        n(W3_10, 4), NF10, n(W3_10, 4), NF10, n(W3_10 ** NF10, 4), pc(ANY10, 2), n(ANY10 / ONE10, 0),
        pc(ONE10, 2), big(ALERTS10), EPS),
    "Many features each with a small false-alarm rate add up to a large one.",
    "One coin rarely lands on its edge. Toss ten coins every second all day and you'll see it a lot.",
    [("false-alarm rate", "how often a normal example is flagged"),
     ("independent", "one feature's alarm doesn't make another's more or less likely")]),
),
]
