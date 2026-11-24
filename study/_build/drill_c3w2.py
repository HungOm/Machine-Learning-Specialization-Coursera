# -*- coding: utf-8 -*-
"""Quiz drills -- C3 W2. One concept per mock-quiz question, four methods each.

Every number below is COMPUTED here at import time and formatted into the text,
never typed. Ratings matrices keep missing cells as NaN beside an r(i,j) mask,
PCA directions come from a real eigen-decomposition (sign fixed so the text is
stable), and the feedback-loop rounds are simulated, not asserted. Scenario
inputs (a tower's layer widths, a time budget) are stated once as data;
everything derived from them is computed.
"""
import numpy as np
from drillkit import D, M
from masterykit import code


def n(x, d=2):
    """Format a number for prose: d decimals, trailing zeros trimmed."""
    s = ("%." + str(d) + "f") % x
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    if s == "-0":
        s = "0"
    return "&minus;" + s[1:] if s.startswith("-") else s


def pc(x, d=1):
    """A fraction as a percentage string, e.g. 0.125 -> '12.5%'."""
    return n(100 * x, d) + "%"


def big(x):
    return "{:,.0f}".format(x)


def _row(vals, d=2):
    return "[" + ", ".join(n(v, d) for v in vals) + "]"


def _cell(v, d=2):
    return "?" if np.isnan(v) else n(v, d)


def _mtab(Y, rows, cols, d=1, extra=None):
    """A ratings matrix as an HTML table; NaN prints as '?'."""
    head = "".join("<th>%s</th>" % c for c in [""] + cols + ([extra[0]] if extra else []))
    body = ""
    for i, name in enumerate(rows):
        cells = "".join("<td>%s</td>" % _cell(v, d) for v in Y[i])
        if extra:
            cells += "<td><b>%s</b></td>" % extra[1][i]
        body += "<tr><td>%s</td>%s</tr>" % (name, cells)
    return "<table><thead><tr>%s</tr></thead><tbody>%s</tbody></table>" % (head, body)


def _pca(X):
    """Eigen-decomposition of the covariance of X, largest first. Each
    direction's sign is fixed so its largest-magnitude entry is positive --
    eigenvectors have no natural sign, and the text must not flip between runs."""
    Xc = X - X.mean(axis=0)
    C = Xc.T @ Xc / len(X)
    vals, vecs = np.linalg.eigh(C)
    order = np.argsort(vals)[::-1]
    vals, vecs = vals[order], vecs[:, order]
    for k in range(vecs.shape[1]):
        if vecs[np.argmax(np.abs(vecs[:, k])), k] < 0:
            vecs[:, k] = -vecs[:, k]
    return vals, vecs, C


def _std(X):
    return (X - X.mean(axis=0)) / X.std(axis=0)


def _deg(u):
    """Angle of a 2-D direction from the first axis, in degrees."""
    return np.degrees(np.arctan2(u[1], u[0]))


# ---------------------------------------------------------------- q01 what is learned
# one gradient-descent step on ONE rating: w, b and x all move
Y1, X1, W1, B1, AL1 = 4.0, np.array([1.0, 0.5]), np.array([1.0, 1.0]), 0.0, 0.1
F1 = W1 @ X1 + B1
E1 = F1 - Y1
W1n = W1 - AL1 * E1 * X1
B1n = B1 - AL1 * E1
X1n = X1 - AL1 * E1 * W1               # uses the OLD w: a simultaneous update
F1n = W1n @ X1n + B1n
# the spot: X never updated. A small ratings set with real structure.
_rng1 = np.random.default_rng(1)
NM1, NU1, NF1 = 8, 5, 2
_Xt1 = _rng1.normal(0, 1, (NM1, NF1))
_Wt1 = _rng1.normal(0, 1, (NU1, NF1))
_bt1 = _rng1.normal(0, 0.3, NU1)
Yq1 = np.clip(np.round(2 * (_Xt1 @ _Wt1.T + _bt1 + 3)) / 2, 0.5, 5.0)   # half-stars, 0.5 to 5
Rq1 = (_rng1.random(Yq1.shape) < 0.8).astype(float)
NR1 = int(Rq1.sum())


def _cofi(learn_x, steps=4000, a=0.05):
    r = np.random.default_rng(7)
    X = r.normal(0, 0.1, (NM1, NF1)); W = r.normal(0, 0.1, (NU1, NF1)); b = np.zeros(NU1)
    for _ in range(steps):
        E = (X @ W.T + b - Yq1) * Rq1
        dW, db, dX = E.T @ X, E.sum(axis=0), E @ W
        W = W - a * dW
        b = b - a * db
        if learn_x:
            X = X - a * dX
    E = (X @ W.T + b - Yq1) * Rq1
    return 0.5 * np.sum(E ** 2), np.sqrt(np.sum(E ** 2) / Rq1.sum())


J1_BOTH, RMS1_BOTH = _cofi(True)
J1_FROZEN, RMS1_FROZEN = _cofi(False)
# transfer: students x exam questions
NQ1, NS1, NK1, FILL1 = 400, 2000, 5, 0.06
PAR1 = NQ1 * NK1 + NS1 * (NK1 + 1)
OBS1 = NQ1 * NS1 * FILL1

# ---------------------------------------------------------------- q02 mean normalization
NAN = np.nan
Y2 = np.array([[5.0, 4.0, NAN, 3.0],
               [NAN, 2.0, 1.0, 3.0],
               [4.0, NAN, 5.0, NAN],
               [1.0, 1.0, NAN, 4.0]])
R2 = (~np.isnan(Y2)).astype(float)
Y2z = np.where(R2 == 1, Y2, 0.0)
MU2 = np.sum(Y2z, axis=1) / np.sum(R2, axis=1)
YN2 = Y2 - MU2.reshape(-1, 1)
BAD2 = np.mean(Y2z, axis=1)                   # the ? counted as 0
TOP2 = int(np.argmax(MU2))
TOPBAD2 = int(np.argmax(BAD2))
# transfer: a film rated once
Y2t = np.vstack([Y2, [[NAN, NAN, 5.0, NAN]]])
R2t = (~np.isnan(Y2t)).astype(float)
_Y2tz = np.where(R2t == 1, Y2t, 0.0)
SUM2t = np.sum(_Y2tz, axis=1)
CNT2t = np.sum(R2t, axis=1)
MU2t = SUM2t / CNT2t
G2 = np.sum(_Y2tz) / np.sum(R2t)
K2 = 3
SHR2 = (SUM2t + K2 * G2) / (CNT2t + K2)
TOPSHR2 = int(np.argmax(SHR2))

# ---------------------------------------------------------------- q03 cold start
# per-item features x = [romance, action]; users' learned w and b (lesson 2's setup)
W3 = np.array([[4.8, 0.2], [0.3, 4.6], [2.5, 2.4]])
B3 = np.array([0.1, 0.2, -0.1])
XNEW3 = np.array([0.9, 0.1])
P3 = W3 @ XNEW3 + B3
# collaborative filtering: no ratings, so no gradient ever reaches x_new; regularisation keeps it ~0
XCF3 = np.zeros(2)
PCF3 = W3 @ XCF3 + B3
# spot: the mean of an empty row
_Y3 = np.array([[NAN, NAN, NAN, NAN]])
_R3 = (~np.isnan(_Y3)).astype(float)
with np.errstate(invalid="ignore"):          # 0/0 on purpose: this IS the demonstration
    MU3 = (np.sum(np.where(_R3 == 1, _Y3, 0.0), axis=1) / np.sum(_R3, axis=1))[0]
NANP3 = MU3 + 0.0                             # nan + anything is nan

# ---------------------------------------------------------------- q04 two towers
VM4_RAW = np.array([[2.0, 1.0, 2.0], [0.0, 3.0, 4.0], [2.0, -1.0, 2.0], [4.0, 0.0, -3.0]])
VU4_RAW = np.array([2.0, 2.0, 1.0])
NORM4 = np.linalg.norm(VM4_RAW, axis=1)
VM4 = VM4_RAW / NORM4.reshape(-1, 1)
VU4 = VU4_RAW / np.linalg.norm(VU4_RAW)
S4 = VM4 @ VU4
BEST4 = int(np.argmax(S4))
NAMES4 = ["A", "B", "C", "D"]
# cost per request, counted in multiplications (weights only)
UT4 = (20, 256, 128, 32)            # user tower widths, input first
IT4 = (16, 256, 128, 32)            # item tower widths


def _mults(widths):
    t = 0
    for i in range(len(widths) - 1):
        t += widths[i] * widths[i + 1]
    return t


MU4, MI4 = _mults(UT4), _mults(IT4)
NIT4 = 1000000
REQ4 = MU4 + NIT4 * IT4[-1]                 # one user pass + a dot product per item
NAIVE4 = MU4 + NIT4 * (MI4 + IT4[-1])       # the item tower re-run for every item, every request
RATIO4 = NAIVE4 / REQ4
# transfer: the item tower is given the user's country
NC4, BYTES4 = 200, 4
STORE4 = NIT4 * IT4[-1] * BYTES4
STOREC4 = STORE4 * NC4

# ---------------------------------------------------------------- q05 retrieval and ranking
RULES5 = [("similar to the last films watched", [3, 7, 9, 2]),
          ("top films in the favourite genre", [7, 1, 4, 9]),
          ("top films in the user's country", [2, 5, 7, 11])]
WATCHED5 = [9, 5]
SCORE5 = np.array([0.31, 0.62, 0.55, 0.48, 0.71, 0.40, 0.12, 0.66, 0.93, 0.50, 0.28, 0.59])
_all5 = []
for _nm, _ids in RULES5:
    _all5 += _ids
RAW5 = len(_all5)
UNI5 = np.unique(np.array(_all5))
CAND5 = np.array([i for i in UNI5 if i not in WATCHED5])
_cs5 = SCORE5[CAND5]
_ord5 = np.argsort(_cs5)[::-1]
PICK5 = CAND5[_ord5[:3]]
_unw5 = np.array([i for i in range(len(SCORE5)) if i not in WATCHED5])
_uo5 = np.argsort(SCORE5[_unw5])[::-1]
TRUE5 = _unw5[_uo5[:3]]
HIT5 = len(set(TRUE5.tolist()) & set(CAND5.tolist()))
MISS5 = [int(i) for i in TRUE5 if i not in CAND5]
# spot: retrieval judged by precision. A noisy cheap score, an exact ranker.
_rng5 = np.random.default_rng(5)
N5, REPS5, TOP5 = 20000, 200, 10
KS5 = (50, 500)
REC5 = dict.fromkeys(KS5, 0.0)
for _r in range(REPS5):
    _s = _rng5.normal(0, 1, N5)
    _cheap = _s + _rng5.normal(0, 0.5, N5)
    _best = set(np.argsort(_s)[-TOP5:].tolist())
    _rank = np.argsort(_cheap)[::-1]
    for _k in KS5:
        REC5[_k] += len(_best & set(_rank[:_k].tolist())) / TOP5 / REPS5
PREC5 = {k: REC5[k] * TOP5 / k for k in KS5}
# transfer: a spelling corrector
DICT5, LM5_US, CHEAP5_US, CANDS5 = 500000, 200.0, 0.02, 30
ALL5_S = DICT5 * LM5_US / 1e6
TWO5_MS = (DICT5 * CHEAP5_US + CANDS5 * LM5_US) / 1e3

# ---------------------------------------------------------------- q06 related items
X6 = np.array([[1.0, 0.2], [0.8, 0.5], [-0.6, 0.9], [1.1, -0.1], [0.1, -1.0]])
D6 = np.sum((X6 - X6[0]) ** 2, axis=1)
_o6 = np.argsort(D6)
NEAR6 = [int(i) for i in _o6[1:3]]
# spot: average rating as similarity
X6s = np.array([[0.9, 0.1], [0.1, 0.9], [0.8, 0.2]])           # A romance, B action, C romance
Y6s = np.array([[5.0, 3.0, NAN, 4.0],
                [3.0, 5.0, 4.0, NAN],
                [4.0, NAN, 2.0, 3.0]])
_R6s = (~np.isnan(Y6s)).astype(float)
AVG6 = np.sum(np.where(_R6s == 1, Y6s, 0.0), axis=1) / np.sum(_R6s, axis=1)
DAB6 = np.sum((X6s[0] - X6s[1]) ** 2)
DAC6 = np.sum((X6s[0] - X6s[2]) ** 2)
# transfer: squared distance versus cosine
X6t = np.array([[2.0, 0.4], [0.5, 0.1], [0.4, 0.5]])           # strong romance, mild romance, mild mix


def _cos(a, b):
    return (a @ b) / (np.linalg.norm(a) * np.linalg.norm(b))


SQ6_12 = np.sum((X6t[1] - X6t[0]) ** 2)
SQ6_23 = np.sum((X6t[1] - X6t[2]) ** 2)
CS6_12 = _cos(X6t[1], X6t[0])
CS6_23 = _cos(X6t[1], X6t[2])

# ---------------------------------------------------------------- q07 what PCA does
X7 = np.array([[2.0, 1.0], [1.0, 2.0], [-1.0, -2.0], [-2.0, -1.0], [0.0, 0.0]])
EV7, U7, C7 = _pca(X7)
Z7 = (X7 - X7.mean(axis=0)) @ U7[:, 0]
KEEP7 = EV7[0] / EV7.sum()
# transfer: one outlier
X7o = np.vstack([X7, [[6.0, -2.0]]])
EV7o, U7o, _C7o = _pca(X7o)
ANG7, ANG7o = _deg(U7[:, 0]), _deg(U7o[:, 0])
KEEP7o = EV7o[0] / EV7o.sum()

# ---------------------------------------------------------------- q08 scaling before PCA
AGE8 = np.array([25.0, 32.0, 41.0, 47.0, 55.0, 60.0])
SAL8 = np.array([28000.0, 35000.0, 39000.0, 52000.0, 50000.0, 61000.0])
X8 = np.column_stack([AGE8, SAL8])
VAR8 = X8.var(axis=0)
EV8, U8, _ = _pca(X8)
KEEP8 = EV8[0] / EV8.sum()
EV8s, U8s, C8s = _pca(_std(X8))
R8 = C8s[0, 1]
KEEP8s = EV8s[0] / EV8s.sum()
# spot: the same salaries in thousands
X8k = np.column_stack([AGE8, SAL8 / 1000])
_, U8k, _ = _pca(X8k)
# transfer: three house features in three units
_rng8 = np.random.default_rng(8)
_size8 = np.clip(_rng8.normal(0, 1, 300), -2, 2)
AREA8 = 120 + 35 * _size8 + _rng8.normal(0, 8, 300)                    # square metres
ROOMS8 = np.clip(np.round(3.5 + 1.1 * _size8 + _rng8.normal(0, 0.5, 300)), 1, 8)
DIST8 = 1 + 25 * _rng8.random(300)                                     # km to the centre
H8 = np.column_stack([AREA8, ROOMS8, DIST8])
HSD8 = H8.std(axis=0)
EVH8, UH8, _ = _pca(H8)
EVH8s, UH8s, _ = _pca(_std(H8))
KEEPH8 = EVH8[0] / EVH8.sum()
KEEPH8s = EVH8s[0] / EVH8s.sum()

# ---------------------------------------------------------------- q09 explained variance
R9 = np.array([0.62, 0.19, 0.09, 0.06, 0.04])
CUM9 = np.cumsum(R9)


def _k_for(cum, target):
    """Smallest number of components whose running total reaches target."""
    return int(np.argmax(cum >= target - 1e-12)) + 1


K9 = {}
for _t in (0.80, 0.90, 0.95, 0.99):
    K9[_t] = _k_for(CUM9, _t)
IDX9 = int(np.argmax(CUM9 >= 0.90))          # the index, not the count
STRICT9 = int(np.argmax(CUM9 > 0.90)) + 1    # '>' instead of '>=': the total lands exactly on 0.9
# transfer: six sensors driven by two hidden causes
_rng9 = np.random.default_rng(9)
_f9 = _rng9.normal(0, 1, (1000, 2))
_mix9 = np.array([[1.0, 0.0], [0.9, 0.1], [0.8, -0.2], [0.0, 1.0], [0.2, 0.9], [0.1, -0.8]])
S9 = _f9 @ _mix9.T + _rng9.normal(0, 0.3, (1000, 6))
EV9, _U9, _ = _pca(_std(S9))
RAT9 = EV9 / EV9.sum()
CUMS9 = np.cumsum(RAT9)
K9t = _k_for(CUMS9, 0.95)
K9t90 = _k_for(CUMS9, 0.90)
ROWS9 = 1000000
BEFORE9 = ROWS9 * 6
AFTER9 = ROWS9 * K9t + K9t * 6 + 6

# ---------------------------------------------------------------- q10 feedback loops
# Two kinds of item. Users click the "provoking" kind slightly more often. Each
# round the system retrains on last round's clicks and shows each kind in
# proportion to the clicks it earned. A toy model -- it shows the mechanism, not
# the size of any real effect.
PC10, PP10 = 0.10, 0.12
ROUNDS10 = 20


def _step10(s, pc_=PC10, pp_=PP10):
    return s * pp_ / (s * pp_ + (1 - s) * pc_)


SH10 = [0.5]
for _ in range(ROUNDS10):
    SH10.append(_step10(SH10[-1]))
# spot: "more data will average it out" -- the same loop, simulated with clicks drawn at random
_rng10 = np.random.default_rng(10)


def _sim10(shown, rounds=ROUNDS10):
    s = 0.5
    for _r in range(rounds):
        k_p = int(round(shown * s))
        c_p = _rng10.binomial(k_p, PP10)
        c_c = _rng10.binomial(shown - k_p, PC10)
        s = c_p / (c_p + c_c)
    return s


SMALL10, LARGE10 = 1000, 100000
SIMS10 = 200
_fin_s = [_sim10(SMALL10) for _r in range(SIMS10)]
_fin_l = [_sim10(LARGE10) for _r in range(SIMS10)]
MEAN10_S, SD10_S = np.mean(_fin_s), np.std(_fin_s)
MEAN10_L, SD10_L = np.mean(_fin_l), np.std(_fin_l)
# transfer: established hits versus new artists, and a reserved exploration slice
PH10, PN10, EPS10, R10t = 0.11, 0.10, 0.10, 30
NEWS10, NEWE10 = [0.5], [0.5]
for _ in range(R10t):
    NEWS10.append(_step10(NEWS10[-1], PH10, PN10))
    NEWE10.append((1 - EPS10) * _step10(NEWE10[-1], PH10, PN10) + EPS10 * 0.5)
FLOOR10 = EPS10 * 0.5


DRILLS = [

# =================================================================== q01
D("c3w2-q01",
  recall=M("Everything collaborative filtering learns, from a blank page.",
    """<p>From memory, for <var>n</var><sub>m</sub> movies, <var>n</var><sub>u</sub> users and <var>n</var>
features per movie:</p>
<ol><li>List every set of numbers the algorithm learns. Which of them were <b>given</b> in the per-item
features lesson?</li>
<li>Write the two regularisation terms of the cost.</li>
<li>How many gradient-descent updates run on every step?</li></ol>""",
    """<ol><li><var>w</var><sup>(<var>j</var>)</sup> and <var>b</var><sup>(<var>j</var>)</sup> for every
user, <b>and</b> <var>x</var><sup>(<var>i</var>)</sup> for every movie. In the per-item features lesson
the <var>x</var><sup>(<var>i</var>)</sup> were written down by someone; here nobody supplies them.</li>
<li>(&lambda;/2) &sum;<sub><var>j</var></sub>&sum;<sub><var>k</var></sub>
(<var>w</var><sub><var>k</var></sub><sup>(<var>j</var>)</sup>)<sup>2</sup> + (&lambda;/2)
&sum;<sub><var>i</var></sub>&sum;<sub><var>k</var></sub>
(<var>x</var><sub><var>k</var></sub><sup>(<var>i</var>)</sup>)<sup>2</sup> &mdash; one for each side,
because both are now parameters.</li>
<li>Three, simultaneously: <var>w</var>, <var>b</var> <b>and</b> <var>x</var>. The third is the whole
idea.</li></ol>""",
    "Collaborative filtering learns the films' descriptions and the users' tastes together, from the ratings alone.",
    "Nobody tells the computer what any film is like or what anyone enjoys. It guesses both, checks the "
    "guesses against the stars people gave, and fixes both a little at a time until they agree.",
    [("parameter", "a number the algorithm learns rather than being told"),
     ("x<sup>(i)</sup>", "the learned description of film i"),
     ("w<sup>(j)</sup>, b<sup>(j)</sup>", "the learned taste of user j")]),

  work=M("One gradient step on one rating &mdash; and watch all three move.",
    """<p>One rating exists: <var>y</var> = %s. Right now <var>x</var><sup>(<var>i</var>)</sup> = %s,
<var>w</var><sup>(<var>j</var>)</sup> = %s, <var>b</var><sup>(<var>j</var>)</sup> = %s, &alpha; = %s and
&lambda; = 0.</p>
<ol><li>Compute the prediction and the error (prediction &minus; <var>y</var>).</li>
<li>Update <var>w</var>, <var>b</var> and <var>x</var> once. Use the <b>old</b> values on the right-hand
side of every update.</li>
<li>Compute the new prediction.</li></ol>""" % (
        n(Y1, 0), _row(X1, 1), _row(W1, 1), n(B1, 0), n(AL1, 1)),
    """<ol><li>%s&times;%s + %s&times;%s + %s = <b>%s</b>; error = <b>%s</b>.</li>
<li><var>w</var> := <var>w</var> &minus; &alpha;&middot;error&middot;<var>x</var> = <b>%s</b>;
<var>b</var> := <b>%s</b>; <var>x</var> := <var>x</var> &minus; &alpha;&middot;error&middot;<var>w</var>
= <b>%s</b>.</li>
<li>%s &mdash; from %s towards %s in one step, because <b>both</b> sides moved. Freeze <var>x</var> and
only <var>w</var> and <var>b</var> could close the gap.</li></ol>""" % (
        n(W1[0], 1), n(X1[0], 1), n(W1[1], 1), n(X1[1], 1), n(B1, 0), n(F1, 2), n(E1, 2),
        _row(W1n, 4), n(B1n, 4), _row(X1n, 4), n(F1n, 5), n(F1, 2), n(Y1, 0)),
    "The gradient of a rating's error reaches the user's numbers and the film's numbers alike.",
    "A guess was too low. The person's taste gets nudged up a bit and the film's description gets "
    "nudged up a bit too, so next time the guess is closer from both ends.",
    [("&alpha;", "the step size: how big each nudge is"),
     ("simultaneous update", "compute every new value from the old ones, then swap them in together")]),

  spot=M("A training loop that is one line short.",
    """<p>On a small ratings set (%d movies, %d users, %d of the %d cells rated, %d features) someone writes
the training loop:</p>%s
<p>It runs, and the cost falls. Which line is missing, and what does it cost them?</p>""" % (
        NM1, NU1, NR1, NM1 * NU1, NF1,
        code("for step in range(4000):\n"
             "    E = (X @ W.T + b - Y) * R\n"
             "    dW = E.T @ X\n"
             "    db = np.sum(E, axis=0)\n"
             "    dX = E @ W\n"
             "    W = W - alpha * dW\n"
             "    b = b - alpha * db")),
    """<p><b><code>X = X - alpha * dX</code> is missing.</b> <code>dX</code> is computed on line 5 and then
thrown away, so the movie features stay at their small random starting values for ever. That is
treating the features as given &mdash; content-based filtering with features nobody chose.</p>
<p>Both versions, run for real on the same data: with <var>X</var> learned the cost ends at
<b>%s</b> (typical error %s stars); with <var>X</var> frozen it stalls at <b>%s</b> (typical error %s
stars). The cost still falls in the frozen run, which is why the missing line is easy to miss.</p>""" % (
        n(J1_BOTH, 3), n(RMS1_BOTH, 2), n(J1_FROZEN, 2), n(RMS1_FROZEN, 2)),
    "If x is never updated, it is not collaborative filtering.",
    "It is like a team where only half the players are allowed to move. The score still changes, "
    "but they cannot win.",
    [("dX", "how the cost changes when each movie feature changes"),
     ("frozen", "left at its starting value, never learned")]),

  transfer=M("The same idea for students and exam questions.",
    """<p>A tutoring site has <b>%s questions</b> and <b>%s students</b>, and records a mark whenever a
student attempts a question &mdash; about %s of the pairs. Nobody has tagged the questions by topic.</p>
<ol><li>Map it onto collaborative filtering: what plays the movie, the user, <var>y</var>, and
<var>r</var>(<var>i</var>,<var>j</var>)?</li>
<li>With %d learned features, how many parameters are there, and how many marks to learn them from?</li>
<li>What could you do with the learned question features afterwards?</li></ol>""" % (
        big(NQ1), big(NS1), pc(FILL1, 0), NK1),
    """<ol><li>Question = movie, student = user, the mark = <var>y</var>, &ldquo;attempted&rdquo; =
<var>r</var>(<var>i</var>,<var>j</var>) = 1.</li>
<li>Questions: %s &times; %d; students: %s &times; (%d + 1). Total <b>%s</b>, from about <b>%s</b>
marks.</li>
<li>Questions with nearby learned features tend to be passed and failed by the same students &mdash; a
data-driven grouping, which you would still have to check by hand before calling it a
&ldquo;topic&rdquo;.</li></ol>""" % (
        big(NQ1), NK1, big(NS1), NK1, big(PAR1), big(OBS1)),
    "Any grid of people against things, mostly blank, can learn both sides at once.",
    "If the same children keep getting the same questions wrong, those questions probably test the same "
    "thing, even if nobody wrote that down.",
    [("feature", "a learned number describing a question, with no name attached"),
     ("tagged", "labelled by a person in advance")]),
),

# =================================================================== q02
D("c3w2-q02",
  recall=M("Mean normalization, both steps, and what it is for.",
    """<p>From memory: write how &mu;<sub><var>i</var></sub> is computed, what the model is trained on, and
what the prediction formula becomes. Then say what a brand-new user is predicted, with and without it.</p>""",
    """<p>&mu;<sub><var>i</var></sub> = the average of movie <var>i</var>'s <b>existing</b> ratings (the
cells with <var>r</var>(<var>i</var>,<var>j</var>) = 1). Train on <var>y</var><sup>(<var>i</var>,<var>j</var>)</sup>
&minus; &mu;<sub><var>i</var></sub>. Predict
<var>w</var><sup>(<var>j</var>)</sup>&middot;<var>x</var><sup>(<var>i</var>)</sup> +
<var>b</var><sup>(<var>j</var>)</sup> + &mu;<sub><var>i</var></sub>.</p>
<p>A new user's <var>w</var> and <var>b</var> are pushed to 0 by regularisation. Without normalization
they are predicted <b>0 stars for everything</b>; with it, <b>&mu;<sub><var>i</var></sub></b> &mdash;
each film's average.</p>""",
    "Subtract each film's average before training and add it back after, so knowing nothing predicts the average.",
    "If you meet someone new and know nothing about them, guessing they will like the films most people "
    "like is much better than guessing they hate everything.",
    [("&mu;<sub>i</sub>", "the average rating film i received"),
     ("cold start", "having no information yet about a new user or item")]),

  work=M("Centre a small ratings table, then serve a brand-new user.",
    """<p>Four movies, four users (? = not rated):</p>%s
<ol><li>Compute &mu;<sub><var>i</var></sub> for each movie.</li>
<li>Write movie 1's normalised row.</li>
<li>Eve signs up and has rated nothing. What is she predicted for each movie, with and without mean
normalization? What tops her list?</li></ol>""" % _mtab(
        Y2, ["movie 1", "movie 2", "movie 3", "movie 4"], ["user A", "user B", "user C", "user D"], 0),
    """<ol><li>&mu; = <b>%s</b> &mdash; each over the rated cells only (movie 3 has two ratings, so it is
(%s + %s)/2).</li>
<li>Movie 1 becomes <b>[%s]</b>: above or below that film's own reputation.</li>
<li>With it: <b>%s</b>, so movie %d tops her list. Without it: [0, 0, 0, 0] &mdash; a tie at the worst
possible score.</li></ol>""" % (
        _row(MU2, 2), n(Y2[2, 0], 0), n(Y2[2, 2], 0), ", ".join(_cell(v, 1) for v in YN2[0]),
        _row(MU2, 2), TOP2 + 1),
    "A new user's prediction is each movie's average, which is the sensible default.",
    "Before you know a new friend's taste, you recommend the films everybody already rates highly.",
    [("normalised row", "a film's ratings with its own average taken away"),
     ("?", "not rated &mdash; skipped, never counted as zero")]),

  spot=M("A mean that counts the blanks.",
    """<p>Using the same table, someone normalizes with:</p>%s
<p>Eve is then shown movie %d first. Which line is wrong, and what should she have been shown?</p>""" % (
        code("Y0 = np.where(R == 1, Y, 0)\n"
             "mu = np.mean(Y0, axis=1)\n"
             "Ynorm = (Y0 - mu.reshape(-1, 1)) * R"), TOPBAD2 + 1),
    """<p><b>Line 2.</b> <code>np.mean</code> divides by 4 for every row, so each <b>?</b> counts as a
zero-star rating. It gives &mu; = %s instead of <b>%s</b>. Movie 3, rated %s and %s, is dragged down to
%s.</p>
<p>Fix: <code>mu = np.sum(Y0, axis=1) / np.sum(R, axis=1)</code>. Eve's top film is then movie <b>%d</b>,
not movie %d.</p>""" % (
        _row(BAD2, 2), _row(MU2, 2), n(Y2[2, 0], 0), n(Y2[2, 2], 0), n(BAD2[2], 2), TOP2 + 1, TOPBAD2 + 1),
    "Average only over the ratings that exist.",
    "If two friends gave a film top marks and two never saw it, the film did not get two zeros.",
    [("np.mean", "adds a row and divides by its full length, blanks included"),
     ("r(i,j)", "1 if the rating exists, 0 if it does not")]),

  transfer=M("A film rated once, and five stars.",
    """<p>A fifth movie arrives and exactly one person rates it %s. Every other number in the table stays
the same.</p>
<ol><li>What is its &mu;, and what does Eve now see first?</li>
<li>One fix is to pretend each film also has %d extra ratings at the overall average of every rating in
the table. Compute that overall average and the adjusted &mu; for movies 3 and 5. Who is first now?</li></ol>""" % (
        n(Y2t[4, 2], 0), K2),
    """<ol><li>&mu; = %s, the highest in the table, so a film one stranger liked becomes <b>everyone's</b>
first recommendation.</li>
<li>Overall average = %s/%d = <b>%s</b>. Movie 5: (%s + %d&times;%s)/(1 + %d) = <b>%s</b>. Movie 3:
(%s + %d&times;%s)/(%d + %d) = <b>%s</b>. Movie %d is first again: a mean built on many ratings moves
less.</li></ol>
<p>The lesson's version is the plain mean. This shrinking is a common production tweak, not part of the
course algorithm.</p>""" % (
        n(MU2t[4], 2), n(np.sum(SUM2t), 0), int(np.sum(CNT2t)), n(G2, 3),
        n(SUM2t[4], 0), K2, n(G2, 3), K2, n(SHR2[4], 3),
        n(SUM2t[2], 0), K2, n(G2, 3), int(CNT2t[2]), K2, n(SHR2[2], 3), TOPSHR2 + 1),
    "An average of one rating is a guess, so a careful system leans it towards the overall average.",
    "One friend saying a film is amazing is not as convincing as twenty friends saying it is good.",
    [("overall average", "the mean of every rating in the table"),
     ("shrinking", "pulling a shaky average towards a safer one")]),
),

# =================================================================== q03
D("c3w2-q03",
  recall=M("Which approach can recommend a film nobody has rated?",
    """<p>From memory: a film was added this morning and has no ratings. Which approach can recommend it,
and why can the other not? Which approach finds links nobody thought to describe?</p>""",
    """<p><b>Content-based.</b> It uses the film's own features <var>x</var><sub><var>m</var></sub>
&mdash; genre, year, cast &mdash; which exist from day one.</p>
<p>Collaborative filtering learns <var>x</var><sup>(<var>i</var>)</sup> only from ratings, and the cost
sums only over cells with <var>r</var>(<var>i</var>,<var>j</var>) = 1. With none, nothing ever shapes
that film's features. In return, collaborative filtering finds patterns no feature list contains.
Real systems run both.</p>""",
    "Content-based filtering can rate what nobody has rated, because it looks at the thing itself.",
    "You can guess you will like a new book from its cover and its author before any friend has read it. "
    "Asking friends only works once some of them have.",
    [("content-based", "matching what an item is against what a person likes"),
     ("collaborative", "using who liked what, and nothing about the items")]),

  work=M("Score a brand-new film both ways.",
    """<p>Features are [romance, action]. Three users' learned parameters:</p>
<table><thead><tr><th>user</th><th><var>w</var><sup>(<var>j</var>)</sup></th><th><var>b</var><sup>(<var>j</var>)</sup></th></tr></thead>
<tbody>%s</tbody></table>
<ol><li>A new film has <var>x</var> = %s. Predict each user's rating. Who should be shown it?</li>
<li>In collaborative filtering the same film has no ratings, so the only thing acting on its
<var>x</var> is regularisation, which drives it to %s. What does each user get now?</li></ol>""" % (
        "".join("<tr><td>%d</td><td>%s</td><td>%s</td></tr>" % (j + 1, _row(W3[j], 1), n(B3[j], 1))
                for j in range(len(B3))), _row(XNEW3, 1), _row(XCF3, 0)),
    """<ol><li>Predictions <b>%s</b>. User 1 (the romance fan) gets it; user 2 should not.</li>
<li><var>w</var>&middot;0 + <var>b</var> = <b>%s</b>: each user's own offset and nothing about the
film. The same for every new film, so it cannot tell them apart.</li></ol>""" % (
        _row(P3, 2), _row(PCF3, 1)),
    "Known features give a new film a real score; learned features give it nothing until ratings arrive.",
    "If a new film comes with a label saying &ldquo;romance&rdquo;, the romance fan can be told about it "
    "today. If it has no label and no reviews, nobody knows who it is for.",
    [("x<sub>m</sub>", "an item's known features, such as genre"),
     ("regularisation", "a pull towards small numbers when nothing else pushes")]),

  spot=M("&ldquo;Mean normalization fixes new films too.&rdquo;",
    """<p>A classmate argues that collaborative filtering can recommend the new film:</p>
<ol><li>Compute its &mu;<sub><var>i</var></sub> as the sum of its ratings divided by how many there
are.</li>
<li>Predict <var>w</var>&middot;<var>x</var> + <var>b</var> + &mu;<sub><var>i</var></sub>, as for any
film.</li>
<li>So every user is predicted at least the film's average, and the best ones get shown it.</li></ol>
<p>Where does it break?</p>""",
    """<p><b>Line 1.</b> There are no ratings, so it is 0/0. NumPy returns <b>%s</b>, and line 2 inherits
it: <code>nan</code> + anything = <b>%s</b>. Every prediction for that film is undefined.</p>
<p>Mean normalization uses the <b>row</b> mean, so it rescues new <b>users</b>. A new <b>film</b> has no
row mean to fall back on; that needs content features.</p>""" % (
        "nan" if np.isnan(MU3) else n(MU3, 2), "nan" if np.isnan(NANP3) else n(NANP3, 2)),
    "A film with no ratings has no average, so mean normalization cannot help it.",
    "You cannot work out the average mark of a test nobody has taken yet.",
    [("nan", "&ldquo;not a number&rdquo;: what 0 divided by 0 gives"),
     ("row mean", "one film's average, which needs at least one rating")]),

  transfer=M("A podcast app with three awkward cases.",
    """<p>For each, say which approach can help and what it uses:</p>
<ol><li>An episode published an hour ago by a show that did not exist yesterday.</li>
<li>A user who installed the app a minute ago and ticked three topics on the welcome screen.</li>
<li>An old episode with a vague one-line description, whose listeners overlap heavily with a hit show.</li></ol>""",
    """<ol><li><b>Content-based</b>: its topic, length, language and description exist; no listens do.</li>
<li><b>Content-based</b> through user features (the ticked topics). Collaborative filtering with mean
normalization would give only the overall favourites.</li>
<li><b>Collaborative</b>: the description says too little, but the listening pattern places it next to
the hit show.</li></ol>
<p>Two of the three are cold starts, and they need different sides: one new item, one new user.</p>""",
    "Use what the thing is when there is no history, and who used it when there is.",
    "A brand-new shop is judged by its sign. An old shop with a faded sign is judged by who keeps going in.",
    [("user features", "facts about a person, such as topics they ticked"),
     ("hybrid", "a system that uses both approaches, each where it works")]),
),

# =================================================================== q04
D("c3w2-q04",
  recall=M("Two towers: what runs when.",
    """<p>From memory: what goes into each tower, what comes out, and how is the prediction made? Which
tower can run overnight, and why? What is the single shape constraint?</p>""",
    """<p>The user tower turns <var>x</var><sub><var>u</var></sub> into <var>v</var><sub><var>u</var></sub>;
the item tower turns <var>x</var><sub><var>m</var></sub> into <var>v</var><sub><var>m</var></sub>.
Prediction = <var>v</var><sub><var>u</var></sub>&middot;<var>v</var><sub><var>m</var></sub>.</p>
<p><var>v</var><sub><var>m</var></sub> depends <b>only on the item</b>, so every item's vector is
computed offline and stored. A request runs one small user-tower pass, then one dot product per item.
The constraint: both <b>output</b> layers must have the same width. The towers do not share weights.</p>""",
    "Item vectors are computed once in advance, so a request costs one user pass and a table of dot products.",
    "A shop writes a summary card for every product the night before. When a customer walks in, it "
    "describes the customer once and compares that with the cards. Nobody re-reads the products.",
    [("tower", "a neural network that turns one side's facts into a short vector"),
     ("offline", "done ahead of time, not while someone waits"),
     ("v<sub>m</sub>", "an item's stored vector")]),

  work=M("Serve one request from a precomputed table.",
    """<p>The item tower ran overnight and produced these raw outputs, which were scaled to length 1 and
stored:</p>
<table><thead><tr><th>item</th><th>raw output</th></tr></thead><tbody>%s</tbody></table>
<p>A user's tower outputs %s.</p>
<ol><li>Scale every vector to length 1, then compute all four scores. Which item is shown?</li>
<li>The user tower is %s wide and the item tower %s (input first). Counting weight multiplications,
what does one request cost over %s items?</li></ol>""" % (
        "".join("<tr><td>%s</td><td>%s</td></tr>" % (NAMES4[i], _row(VM4_RAW[i], 0)) for i in range(4)),
        _row(VU4_RAW, 0), " &rarr; ".join(str(v) for v in UT4), " &rarr; ".join(str(v) for v in IT4),
        big(NIT4)),
    """<ol><li>Lengths %s and %s for the user. Scores %s: item <b>%s</b>.</li>
<li>User tower: %s. Dot products: %s &times; %d. Total <b>%s</b> &mdash; the item tower does not run at
all.</li></ol>""" % (
        _row(NORM4, 0), n(np.linalg.norm(VU4_RAW), 0), _row(S4, 3), NAMES4[BEST4],
        big(MU4), big(NIT4), IT4[-1], big(REQ4)),
    "At request time it is one small network pass, then dot products.",
    "Comparing your wish list with a million summary cards is quick. Rewriting the million cards first "
    "would not be.",
    [("length 1", "scaled so only the direction counts"),
     ("dot product", "multiply matching entries and add")]),

  spot=M("A serving function that redoes last night's work on every request.",
    """<p>The serving code:</p>%s
<p>It returns exactly the right scores. Which line is the problem?</p>""" % code(
        "def recommend(x_u, X_items):\n"
        "    v_u = user_NN(x_u)\n"
        "    v_m = item_NN(X_items)\n"
        "    return v_m @ v_u"),
    """<p><b>Line 3.</b> It re-runs the item tower on every item, on every request, although no item changed
since last night. Load the stored <code>v_m</code> table instead.</p>
<p>With the towers above and %s items: <b>%s</b> multiplications per request this way, against
<b>%s</b> with a stored table &mdash; about <b>%s</b> times more. The answer is identical, which is why it
survives testing.</p>""" % (big(NIT4), big(NAIVE4), big(REQ4), big(RATIO4)),
    "Never recompute at request time what depends only on the item.",
    "Re-reading every book in the library each time someone asks for a recommendation, when the "
    "summaries were written last night.",
    [("serving", "answering a real request while someone waits"),
     ("latency", "how long one request takes")]),

  transfer=M("The item tower is given the user's country.",
    """<p>A product manager wants regional taste in the model and proposes feeding the user's country into
the <b>item</b> tower. There are %s items, %d countries, %d-number vectors and %d bytes per number.</p>
<ol><li>How much storage do the precomputed item vectors need now, and after the change?</li>
<li>Where should the country go instead?</li></ol>""" % (big(NIT4), NC4, IT4[-1], BYTES4),
    """<ol><li>Now: %s &times; %d &times; %d = <b>%s MB</b>. After: one table per country, %s MB &times; %d =
<b>%s GB</b> &mdash; and every new country adds another table.</li>
<li>Into the <b>user</b> tower. It describes the person, it runs per request anyway, and the item
vectors stay independent of who is looking.</li></ol>""" % (
        big(NIT4), IT4[-1], BYTES4, big(STORE4 / 1e6), big(STORE4 / 1e6), NC4, n(STOREC4 / 1e9, 1)),
    "Anything about the viewer belongs in the user tower, or the item table stops being precomputable.",
    "If every product's summary card had to be rewritten for each town, the shop would need a separate "
    "stack of cards for every town.",
    [("MB, GB", "millions and billions of bytes of storage"),
     ("independent", "not changing with who is asking")]),
),

# =================================================================== q05
D("c3w2-q05",
  recall=M("Retrieval, then ranking: what each stage is for.",
    """<p>From memory: what does each stage do, roughly how many items does each handle, and what is each
judged on? What can ranking never fix?</p>""",
    """<p><b>Retrieval</b>: cheap and approximate, millions down to a few hundred, judged on <b>recall</b>
&mdash; did the good items survive? <b>Ranking</b>: the full model on those few hundred, judged on getting
the order right.</p>
<p>Ranking only reorders what it is given. An item retrieval drops can never be recommended, however
good the ranker.</p>""",
    "A cheap filter that must not miss, then an expensive judge that must get the order right.",
    "To pick a present from a huge shop, you fill a trolley quickly with likely things, then choose "
    "carefully from the trolley. If the best toy never went in the trolley, you will never pick it.",
    [("retrieval", "quickly gathering a few hundred plausible candidates"),
     ("ranking", "scoring those candidates carefully and ordering them"),
     ("recall", "the share of the good items that made it through")]),

  work=M("Build a candidate list, rank it, and find what was lost.",
    """<p>A catalogue of %d films (0&ndash;%d). Three retrieval rules return:</p>
<ul>%s</ul>
<p>The user has already watched %s. The ranker's scores are %s (film 0 first).</p>
<ol><li>How many candidates reach the ranker?</li>
<li>Which three are shown?</li>
<li>Which three would the ranker have chosen from every unwatched film? What fraction did retrieval keep?</li></ol>""" % (
        len(SCORE5), len(SCORE5) - 1,
        "".join("<li>%s: %s</li>" % (nm, ", ".join(str(i) for i in ids)) for nm, ids in RULES5),
        " and ".join(str(i) for i in WATCHED5), _row(SCORE5, 2)),
    """<ol><li>%d IDs, %d distinct; remove the watched ones: <b>%d candidates</b> (%s).</li>
<li>Films <b>%s</b>.</li>
<li>Films %s; retrieval kept <b>%d of 3</b>. Film %d has the highest score in the catalogue and no rule
surfaced it, so the ranker never saw it.</li></ol>""" % (
        RAW5, len(UNI5), len(CAND5), ", ".join(str(i) for i in CAND5),
        ", ".join(str(i) for i in PICK5), ", ".join(str(i) for i in TRUE5), HIT5, MISS5[0]),
    "The ranker can only choose from what retrieval hands it.",
    "The judge of a baking contest can only taste the cakes that made it to the table.",
    [("candidate", "an item retrieval passes on to the ranker"),
     ("duplicate", "the same film found by two rules, kept once")]),

  spot=M("Retrieval tuned for precision.",
    """<p>A team's retrieval returns 500 candidates per request. Their review says:</p>
<ol><li>Only about %s of the 500 candidates are among the user's top 10.</li>
<li>That is poor precision, so retrieval is doing a bad job.</li>
<li>Cut the list to 50 candidates; precision rises to about %s.</li></ol>
<p>Simulated over %d users, %s items and a cheap score that is the true score plus noise, the change
does raise precision. Which line is the mistake, and what does the change cost?</p>""" % (
        pc(PREC5[500], 0), pc(PREC5[50], 0), REPS5, big(N5)),
    """<p><b>Line 2.</b> Retrieval is judged on <b>recall</b>; precision is the ranker's job.</p>
<p>In the same simulation, the share of each user's true top 10 that survives retrieval falls from
<b>%s</b> at 500 candidates to <b>%s</b> at 50: about %s of the best items are now invisible to the
ranker.</p>""" % (pc(REC5[500]), pc(REC5[50]), pc(1 - REC5[50], 0)),
    "Judge retrieval by what it keeps, not by how much junk it lets through.",
    "A net with big holes catches fewer weeds, and lets the fish go too.",
    [("precision", "the share of the candidates that are really good"),
     ("recall", "the share of the really good items that are candidates")]),

  transfer=M("A spelling corrector has the same shape.",
    """<p>A phone's spelling corrector has %s words. Its language model takes %s microseconds to score one
word in context. A cheap filter keeps only words within two typing slips of what was typed, at %s
microseconds per dictionary word, and passes about %d on.</p>
<ol><li>How long would scoring every word with the language model take? And filter-then-score?</li>
<li>Suppose the filter also insists on the same first letter. What happens when someone types
&ldquo;fone&rdquo;?</li></ol>""" % (big(DICT5), n(LM5_US, 0), n(CHEAP5_US, 2), CANDS5),
    """<ol><li>Every word: <b>%s seconds</b>. Filter then score: <b>%s ms</b>.</li>
<li>&ldquo;phone&rdquo; never reaches the language model, so no amount of model quality can suggest it.
That is a retrieval-recall failure, in a system with no users and no films.</li></ol>""" % (
        n(ALL5_S, 0), n(TWO5_MS, 0)),
    "Any cheap-filter-then-careful-judge system fails silently when the filter drops the right answer.",
    "If the guard at the door only lets in people whose names start with P, the friend called Phil "
    "who spells it Fil never gets in.",
    [("language model", "a model that scores how likely a word is in its sentence"),
     ("microsecond", "a millionth of a second")]),
),

# =================================================================== q06
D("c3w2-q06",
  recall=M("&ldquo;More like this&rdquo;, from a blank page.",
    """<p>From memory: to find the films most similar to film <var>i</var> with collaborative filtering,
what do you compute, and over what? Is any user involved? Why does it work when nobody knows what the
features mean?</p>""",
    """<p>The squared distance &Vert;<var>x</var><sup>(<var>k</var>)</sup> &minus;
<var>x</var><sup>(<var>i</var>)</sup>&Vert;<sup>2</sup> =
&sum;<sub><var>l</var></sub>(<var>x</var><sub><var>l</var></sub><sup>(<var>k</var>)</sup> &minus;
<var>x</var><sub><var>l</var></sub><sup>(<var>i</var>)</sup>)<sup>2</sup> to every other film's learned
features; keep the smallest few.</p>
<p>No user is involved, so it works for a logged-out visitor. Similar rating patterns produce similar
vectors, so the geometry carries meaning even though the axes have no names.</p>""",
    "Related items are the ones whose learned feature vectors sit closest.",
    "Every film gets a secret address. Films the same people liked end up living on the same street, "
    "so you find similar films by looking next door.",
    [("feature vector", "the short list of learned numbers for one film"),
     ("squared distance", "add up the squared gaps between two lists"),
     ("nearest neighbour", "the closest other item")]),

  work=M("Find film 1's two nearest neighbours by hand.",
    """<p>Learned features (<var>n</var> = 2):</p>
<table><thead><tr><th>film</th><th><var>x</var><sup>(<var>i</var>)</sup></th></tr></thead><tbody>%s</tbody></table>
<p>Compute the squared distance from film 1 to every other film. Which two are shown under &ldquo;because
you watched film 1&rdquo;?</p>""" % "".join(
        "<tr><td>%d</td><td>%s</td></tr>" % (i + 1, _row(X6[i], 1)) for i in range(len(X6))),
    """<p>Distances to films 2&ndash;5: <b>%s</b>. For film 2: (%s &minus; %s)<sup>2</sup> + (%s &minus;
%s)<sup>2</sup> = %s.</p>
<p>The two nearest are films <b>%d</b> and <b>%d</b>.</p>""" % (
        ", ".join(n(v, 2) for v in D6[1:]), n(X6[1, 0], 1), n(X6[0, 0], 1), n(X6[1, 1], 1),
        n(X6[0, 1], 1), n(D6[1], 2), NEAR6[0] + 1, NEAR6[1] + 1),
    "Square the gaps, add them, and the smallest totals win.",
    "Measure how far each film's address is from this one's, then point at the closest two houses.",
    [("x<sub>l</sub>", "the l-th learned number in a film's list")]),

  spot=M("Similar because the averages match.",
    """<p>Three films, their ratings (? = not rated) and their learned features:</p>%s
<p>A colleague writes: &ldquo;1. Film A averages %s and film B averages %s. 2. The difference is 0. 3. So
B is the most similar film to A.&rdquo; Where does this go wrong?</p>""" % (
        _mtab(Y6s, ["A, x = " + _row(X6s[0], 1), "B, x = " + _row(X6s[1], 1), "C, x = " + _row(X6s[2], 1)],
              ["user 1", "user 2", "user 3", "user 4"], 0, ("average", [n(v, 1) for v in AVG6])),
        n(AVG6[0], 1), n(AVG6[1], 1)),
    """<p><b>Line 3.</b> A matching average says how well liked two films are, not what they are like.
User 1 loves A and is lukewarm about B; user 2 is the reverse.</p>
<p>In feature space: A to B is <b>%s</b>, A to C is <b>%s</b>. C, with a lower average, is the real
neighbour.</p>""" % (n(DAB6, 2), n(DAC6, 2)),
    "Two films can be equally popular and nothing alike.",
    "A cake and a football can both get top marks from their fans. That does not make them similar.",
    [("average rating", "how well liked a film is overall"),
     ("feature space", "where each film sits according to its learned numbers")]),

  transfer=M("When squared distance and the angle disagree.",
    """<p>Three learned vectors: P = %s (strongly one kind), Q = %s (the same kind, weakly) and S = %s (a
mild mix). Which is Q's nearest neighbour by squared distance, and which by cosine similarity
(<var>a</var>&middot;<var>b</var> / (&Vert;<var>a</var>&Vert;&Vert;<var>b</var>&Vert;))?</p>""" % (
        _row(X6t[0], 1), _row(X6t[1], 1), _row(X6t[2], 1)),
    """<p>Squared distance: Q&ndash;P = %s, Q&ndash;S = %s, so <b>S</b>. Cosine: Q&ndash;P = <b>%s</b>,
Q&ndash;S = %s, so <b>P</b>.</p>
<p>P points exactly the same way as Q and is only longer. Cosine compares direction only, which is
often what you want when vector length mostly tracks how much data a film has.</p>""" % (
        n(SQ6_12, 2), n(SQ6_23, 2), n(CS6_12, 3), n(CS6_23, 3)),
    "Distance compares where two vectors end; cosine compares which way they point.",
    "Two arrows can point in exactly the same direction and still have their tips far apart if one "
    "is much longer.",
    [("cosine similarity", "how closely two arrows point the same way: 1 means exactly"),
     ("magnitude", "how long a vector is")]),
),

# =================================================================== q07
D("c3w2-q07",
  recall=M("What PCA does, and what it does not.",
    """<p>From memory: what does PCA find, what does it do with it, and what is <var>z</var>? Then say why
each of these is <b>not</b> PCA: picking the best original columns; grouping points; removing
outliers.</p>""",
    """<p>It finds the directions of <b>maximum variance</b> (each a weighted mix of the original
features), sorted by how much spread they carry, and projects onto the first few: <var>z</var> =
<var>x</var>&middot;<var>u</var>.</p>
<p>It makes <b>new</b> features, so it is not column selection. It does not group points; that is
clustering. Outliers are not removed &mdash; they pull the directions towards themselves.</p>""",
    "PCA builds new axes along which the data spreads most, and keeps the first few.",
    "Turn a crowd of toys until their shadows on the wall are as spread out as possible, then keep just "
    "the shadow.",
    [("principal component", "a new axis, mixed from the old ones"),
     ("projection z", "how far along the new axis a point sits"),
     ("variance", "how spread out the values are")]),

  work=M("PCA on five points, end to end.",
    """<p>Five points: %s.</p>
<ol><li>Find the mean and the covariance matrix (divide by <var>m</var> = %d).</li>
<li>Check that %s and %s are its eigenvectors, and find their eigenvalues.</li>
<li>Project every point onto the first component. What share of the variance is kept?</li></ol>""" % (
        ", ".join("(%s, %s)" % (n(p[0], 0), n(p[1], 0)) for p in X7), len(X7),
        _row(U7[:, 0], 3), _row(U7[:, 1], 3)),
    """<ol><li>The mean is (0, 0), so nothing to subtract. Covariance = <b>[%s, %s]</b>.</li>
<li>Eigenvalues <b>%s</b> and <b>%s</b>. For a matrix [<var>a</var>, <var>b</var>; <var>b</var>,
<var>a</var>] they are always <var>a</var> &plusmn; <var>b</var>, along the two diagonals.</li>
<li><var>z</var> = (<var>x</var><sub>1</sub> + <var>x</var><sub>2</sub>)/&radic;2 = <b>%s</b>. Kept:
%s/(%s + %s) = <b>%s</b>.</li></ol>""" % (
        _row(C7[0], 1), _row(C7[1], 1), n(EV7[0], 1), n(EV7[1], 1), _row(Z7, 3),
        n(EV7[0], 1), n(EV7[0], 1), n(EV7[1], 1), pc(KEEP7, 0)),
    "Centre, find the spread's main direction, and measure each point along it.",
    "Five dots lie roughly along a slanted line. Draw the line, and describe each dot by how far along "
    "it sits.",
    [("covariance matrix", "a table of how much each pair of features moves together"),
     ("eigenvalue", "how much spread lies along one direction")]),

  spot=M("&ldquo;PCA chose feature 1.&rdquo;",
    """<p>After reducing the five points above to one number each, someone reports:</p>
<ol><li>PCA kept one component.</li>
<li>That component is feature <var>x</var><sub>1</sub>, the more important column.</li>
<li>So for the point (%s, %s) the stored value is %s, and <var>x</var><sub>2</sub> can be deleted from the
database.</li></ol>
<p>Which line is wrong?</p>""" % (n(X7[0, 0], 0), n(X7[0, 1], 0), n(X7[0, 0], 0)),
    """<p><b>Line 2</b>, and line 3 follows from it. The component is %s: an equal mix of
<b>both</b> columns. The stored value for (%s, %s) is <var>z</var> = <b>%s</b>, neither %s nor %s.</p>
<p>Computing <var>z</var> for new data needs <var>x</var><sub>1</sub> and <var>x</var><sub>2</sub>, so
neither column can be deleted. Picking columns is feature selection, a different method.</p>""" % (
        _row(U7[:, 0], 3), n(X7[0, 0], 0), n(X7[0, 1], 0), n(Z7[0], 3), n(X7[0, 0], 0), n(X7[0, 1], 0)),
    "A principal component is a blend of every original feature, not one of them.",
    "A smoothie is not the banana. You still need the banana and the strawberry to make the next one.",
    [("feature selection", "keeping some original columns and dropping the rest"),
     ("loading", "how much of each original feature goes into a component")]),

  transfer=M("One outlier joins the five points.",
    """<p>A sixth point, (%s, %s), is added to the five points above &mdash; a typo in data entry, say. Before
computing, guess what happens to the first component. Then compare with the real result.</p>""" % (
        n(X7o[5, 0], 0), n(X7o[5, 1], 0)),
    """<p>The first component swings from <b>%s&deg;</b> to <b>%s&deg;</b> (now %s), and the share of
variance it keeps falls from %s to %s.</p>
<p>One point out of six re-aimed the whole axis, because a point far from the mean adds a lot of
variance in its own direction. Look at the data, and deal with bad points, before you trust a PCA.</p>""" % (
        n(ANG7, 0), n(ANG7o, 1), _row(U7o[:, 0], 3), pc(KEEP7, 0), pc(KEEP7o, 0)),
    "PCA chases variance, and one far-away point is a lot of variance.",
    "One child standing far off to the side of a class photo makes the photographer swing the "
    "camera round to fit them in.",
    [("outlier", "a point far from all the others"),
     ("degrees", "the angle of the new axis, measured from the first feature")]),
),

# =================================================================== q08
D("c3w2-q08",
  recall=M("Why PCA needs scaled features.",
    """<p>From memory: what two things must you do to the features before PCA, and why each? What does the
output look like if you skip scaling?</p>""",
    """<p><b>Mean-normalise</b>, because variance is measured about the mean. <b>Scale</b> to comparable
ranges, because PCA maximises variance and variance has units: change a column's units and its variance
changes with them.</p>
<p>Skip scaling and the first component points along whichever feature has the biggest numbers.
Nothing warns you; the output looks perfectly reasonable.</p>""",
    "Scale first, or the feature with the biggest numbers wins by its units alone.",
    "If one friend measures in millimetres and another in metres, the millimetre friend's numbers look "
    "huge. That is not because their thing is bigger.",
    [("scaling", "putting features on comparable ranges, e.g. mean 0 and spread 1"),
     ("units", "what a number is measured in: pounds, years, metres")]),

  work=M("Age and salary, before and after scaling.",
    """<p>Six people: ages %s, salaries in pounds %s.</p>
<ol><li>Compute each column's variance. Before doing any eigen-maths, predict the first component.</li>
<li>After standardising each column (mean 0, standard deviation 1), the covariance matrix is
[1, <var>r</var>; <var>r</var>, 1], where <var>r</var> is the correlation. What is <var>r</var>? (A matrix
[<var>a</var>, <var>b</var>; <var>b</var>, <var>a</var>] has eigenvalues <var>a</var> &plusmn; <var>b</var>
along the two diagonals.) Give the first component and its share.</li></ol>""" % (
        _row(AGE8, 0), ", ".join(big(v) for v in SAL8)),
    """<ol><li>Variances <b>%s</b> and <b>%s</b>. The first component is %s &mdash; salary alone, holding
%s of the variance. Age is invisible.</li>
<li><var>r</var> = <b>%s</b>. Eigenvalues 1 &plusmn; <var>r</var>; the first component is %s, an equal
mix, keeping (1 + <var>r</var>)/2 = <b>%s</b>.</li></ol>""" % (
        n(VAR8[0], 1), big(VAR8[1]), _row(U8[:, 0], 4), pc(KEEP8, 5), n(R8, 3), _row(U8s[:, 0], 3),
        pc(KEEP8s, 1)),
    "Unscaled, the first component is just the column with the biggest numbers.",
    "Two children's heights and pocket money can rise together, but if pocket money is counted in "
    "pennies it drowns out everything else.",
    [("standardise", "subtract the mean, divide by the standard deviation"),
     ("correlation r", "how closely two features rise and fall together, from &minus;1 to 1")]),

  spot=M("&ldquo;Changing units only relabels the axis.&rdquo;",
    """<p>Someone runs PCA on the age and salary data above, without scaling, then reasons:</p>
<ol><li>In pounds, the first component is %s.</li>
<li>Rewriting salary in thousands of pounds only relabels that axis.</li>
<li>So the first component is unchanged.</li></ol>
<p>Which line fails? Check by running the thousands version.</p>""" % _row(U8[:, 0], 4),
    """<p><b>Line 2.</b> Dividing a column by 1,000 divides its variance by 1,000,000. In thousands of
pounds the first component becomes <b>%s</b> &mdash; about %s&deg; from the age axis instead of %s&deg;.</p>
<p>Same people, same pattern, a different answer, decided by a unit. Standardising removes that choice,
which is why it is the default.</p>""" % (
        _row(U8k[:, 0], 3), n(_deg(U8k[:, 0]), 0), n(_deg(U8[:, 0]), 0)),
    "PCA is not scale-invariant: change a unit and the components change.",
    "Measuring a table in centimetres or in metres should not change which way it is long. Without "
    "scaling, for PCA it does.",
    [("scale-invariant", "giving the same answer whatever units you use"),
     ("&pound;k", "thousands of pounds")]),

  transfer=M("Three house features, three units.",
    """<p>%d houses: floor area in square metres, number of rooms, and distance to the centre in km. Their
standard deviations are %s, %s and %s.</p>
<ol><li>Without computing, which feature will dominate an unscaled first component?</li>
<li>Compare with the real results, unscaled and standardised.</li></ol>""" % (
        len(H8), n(HSD8[0], 1), n(HSD8[1], 1), n(HSD8[2], 1)),
    """<ol><li>Area, purely because its numbers spread the most.</li>
<li>Unscaled: first component %s (area, rooms, distance), holding %s. Standardised: %s, holding %s
&mdash; area and rooms together, a &ldquo;size&rdquo; direction. The second component is then %s, close
to distance alone: it is unrelated to size, so it gets an axis of its own.</li></ol>""" % (
        _row(UH8[:, 0], 3), pc(KEEPH8), _row(UH8s[:, 0], 3), pc(KEEPH8s), _row(UH8s[:, 1], 3)),
    "Look at each feature's spread before PCA; it predicts what an unscaled PCA will say.",
    "Put a giant and two children on a see-saw and you learn nothing about the children.",
    [("standard deviation", "a typical distance from the average"),
     ("size direction", "the component where area and rooms rise together")]),
),

# =================================================================== q09
D("c3w2-q09",
  recall=M("Reading explained_variance_ratio_.",
    """<p>From memory: what does each entry of <code>explained_variance_ratio_</code> mean, what do the
entries add up to, and how do you choose how many components to keep for a target such as 90%?</p>""",
    """<p>Entry <var>k</var> is the fraction of the total variance carried by component <var>k</var>, largest
first. Over all components they add up to 1.</p>
<p>Take the <b>running total</b> and keep the smallest number of components at which it reaches the
target. The cumulative sum is the number to read, not any single entry.</p>""",
    "Add the ratios up as you go and stop when the total reaches your target.",
    "You keep tipping cups of water into a jug, biggest cup first, until the jug is as full as you want.",
    [("explained variance ratio", "how much of the spread one component keeps"),
     ("cumulative sum", "a running total")]),

  work=M("How many components for each target?",
    """<p>A PCA reports %s. Write the running total. How many components are needed for
%s, %s, %s and %s?</p>""" % (
        _row(R9, 2), pc(0.80, 0), pc(0.90, 0), pc(0.95, 0), pc(0.99, 0)),
    """<p>Running total: <b>%s</b>.</p>
<p>%s</p>""" % (_row(CUM9, 2), "; ".join(
        "%s &rarr; <b>%d</b>" % (pc(t, 0), K9[t]) for t in (0.80, 0.90, 0.95, 0.99))),
    "Read off the first position where the running total reaches the target.",
    "Count how many cups it took before the jug reached the line.",
    [("target", "how much of the spread you decided to keep")]),

  spot=M("A count that comes out one short.",
    """<p>To keep %s of the variance:</p>%s
<p>With the ratios %s this prints %d. Which line is wrong?</p>""" % (
        pc(0.90, 0),
        code("ratios = np.array([0.62, 0.19, 0.09, 0.06, 0.04])\n"
             "total = np.cumsum(ratios)\n"
             "k = np.argmax(total >= 0.90)\n"
             "print(k)"), _row(R9, 2), IDX9),
    """<p><b>Line 3.</b> <code>np.argmax</code> returns the <b>index</b> of the first True, and indexes start
at 0. Index %d is the third component, so <code>k = np.argmax(total >= 0.90) + 1</code> = <b>%d</b>.</p>
<p>A second trap: the total lands <b>exactly</b> on 0.9, so writing <code>&gt;</code> instead of
<code>&gt;=</code> gives %d. Both slips are wrong answers on the quiz.</p>""" % (
        IDX9, IDX9 + 1, STRICT9),
    "An index counts from zero; a number of components counts from one.",
    "If the third child in a queue is called number 2 because counting started at 0, you still have "
    "three children.",
    [("np.argmax", "the position of the largest value, or of the first True"),
     ("index", "a position counted from 0")]),

  transfer=M("Six sensors, two hidden causes.",
    """<p>Six sensors on a machine are driven by two hidden causes (say, load and temperature) plus some
noise. After standardising, PCA reports %s.</p>
<ol><li>How many components for 90%% and for 95%%? What does the gap say?</li>
<li>Storing %s readings: how many numbers before, and after keeping the 95%% count (count the
components and the means too)?</li></ol>""" % (_row(RAT9, 3), big(ROWS9)),
    """<ol><li>Running total %s: <b>%d</b> for 90%%, <b>%d</b> for 95%%. Two components carry the two causes;
the third adds only %s and is mostly noise.</li>
<li>Before: <b>%s</b>. After: %s &times; %d + %d &times; 6 + 6 = <b>%s</b>.</li></ol>""" % (
        _row(CUMS9, 3), K9t90, K9t, pc(RAT9[K9t - 1]), big(BEFORE9), big(ROWS9), K9t, K9t, big(AFTER9)),
    "A sharp drop after a few components tells you how many real causes there are.",
    "Six thermometers in one room mostly tell you one thing. Two big readings and a lot of tiny wobble "
    "means two real causes.",
    [("hidden cause", "something not measured directly that moves several features together"),
     ("noise", "small random wobble carrying no pattern")]),
),

# =================================================================== q10
D("c3w2-q10",
  recall=M("The feedback loop, from a blank page.",
    """<p>From memory: draw the loop that makes a recommender different from every other model in the
specialization. Why is no bad intention needed? Name two technical mitigations. Why does more data not
fix it?</p>""",
    """<p><b>Shown &rarr; clicked &rarr; trained on &rarr; shown more.</b> The model's output becomes its
next training input.</p>
<p>Every step is a small, defensible response to clicks, so no one has to intend the result. Mitigations:
optimise a longer-horizon outcome; cap how often one kind of item is shown; reserve some slots for
exploration. More data gathered <b>through the same loop</b> feeds the loop.</p>""",
    "A recommender writes its own future training data, so small tilts grow.",
    "If a shop only restocks what sold yesterday, and only puts the restocked things in the window, the "
    "window slowly fills up with one kind of thing.",
    [("feedback loop", "an output that comes back as an input"),
     ("proxy", "something easy to measure that stands in for what you really want"),
     ("exploration", "showing some items on purpose to learn about them")]),

  work=M("Run the loop by hand.",
    """<p>A toy model, to see the mechanism, not to measure any real platform. There are two kinds of item.
Users click calm items %s of the time and provoking items %s of the time. Each round the system shows
each kind in proportion to the clicks it earned last round:</p>
<p><var>s</var><sub>new</sub> = <var>s</var>&times;%s / (<var>s</var>&times;%s +
(1 &minus; <var>s</var>)&times;%s), where <var>s</var> is the provoking share.</p>
<p>Start at <var>s</var> = %s. Compute two rounds.</p>""" % (
        pc(PC10, 0), pc(PP10, 0), n(PP10, 2), n(PP10, 2), n(PC10, 2), n(SH10[0], 1)),
    """<p>Round 1: %s&times;%s / (%s + %s) = <b>%s</b>. Round 2: <b>%s</b>.</p>
<p>Continuing: after 5 rounds %s, after 10 %s, after %d <b>%s</b>. Users prefer the provoking kind by only
%s percentage points, and nobody chose the outcome; the update rule did.</p>""" % (
        n(SH10[0], 1), n(PP10, 2), n(SH10[0] * PP10, 3), n((1 - SH10[0]) * PC10, 3), n(SH10[1], 3),
        n(SH10[2], 3), pc(SH10[5]), pc(SH10[10]), ROUNDS10, pc(SH10[ROUNDS10]), n(100 * (PP10 - PC10), 0)),
    "Retrain on your own output and a small preference compounds round after round.",
    "If a slightly louder friend gets a slightly bigger turn every time, soon nobody else gets a turn.",
    [("round", "one cycle of show, collect clicks, retrain"),
     ("share", "the fraction of what is shown that is of one kind")]),

  spot=M("&ldquo;With enough data it will average out.&rdquo;",
    """<p>An engineer reviewing the loop above writes:</p>
<ol><li>The drift comes from random noise in a small number of clicks.</li>
<li>Collecting %s times more impressions per round will average the noise away.</li>
<li>So at scale the shares stay near 50/50.</li></ol>
<p>The same loop, simulated %d times with clicks drawn at random, for %d rounds. Which line is the error?</p>""" % (
        big(LARGE10 / SMALL10), SIMS10, ROUNDS10),
    """<p><b>Line 1</b>, and the rest follows. With %s impressions per round the provoking share ends at
<b>%s</b> (spread %s). With %s it ends at <b>%s</b> (spread %s).</p>
<p>More data shrank the run-to-run spread about %s times and left the drift where it was. The drift comes from the
loop, not from noise, so collecting more data through the same loop only makes it more reliable.</p>""" % (
        big(SMALL10), pc(MEAN10_S), pc(SD10_S), big(LARGE10), pc(MEAN10_L), pc(SD10_L), n(SD10_S / SD10_L, 0)),
    "The narrowing is built into the loop; more data makes it more certain, not smaller.",
    "Asking more people the same leading question does not make the answers less one-sided.",
    [("impression", "one time an item is shown to someone"),
     ("spread", "how much the result varies between runs")]),

  transfer=M("New artists on a music app, with and without exploration.",
    """<p>Listeners click established hits %s of the time and tracks by new artists %s. The same update runs
every round, starting from a 50/50 split.</p>
<ol><li>What share do new artists have after %d rounds?</li>
<li>Now %s of slots are reserved for exploration and split evenly, whatever the clicks say. What share
do new artists settle at? What is the lowest it could ever fall to?</li></ol>""" % (
        pc(PH10, 0), pc(PN10, 0), R10t, pc(EPS10, 0)),
    """<ol><li><b>%s</b>, from %s. A %s-point difference in click rate nearly removed them.</li>
<li>About <b>%s</b>, and never below %s whatever happens. Exploration does not remove the tilt; it puts a
floor under it and keeps collecting evidence about the items the loop would otherwise stop showing.</li></ol>
<p>It costs some clicks, which is the trade the lesson asks you to make openly.</p>""" % (
        pc(NEWS10[R10t]), pc(NEWS10[0], 0), n(100 * (PH10 - PN10), 0), pc(NEWE10[R10t], 0), pc(FLOOR10, 0)),
    "Reserving a slice for exploration keeps new things visible and keeps the system learning about them.",
    "A radio station that keeps one song an hour for new bands stops only ever playing the same famous "
    "songs.",
    [("exploration slice", "slots kept for items the model would not choose"),
     ("floor", "a level the share can never fall below")]),
),
]
