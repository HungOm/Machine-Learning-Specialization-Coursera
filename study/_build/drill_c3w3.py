# -*- coding: utf-8 -*-
"""Quiz drills — C3 W3. One concept per mock-quiz question, four methods each.

Every number below is COMPUTED here at import time and formatted into the text,
never typed. The Mars rover is solved for real: returns are summed along actual
paths, the Q table comes from value iteration on the six-square strip, policies
are evaluated by solving their linear equations, and the slippery rover is
solved with the expectation in the Bellman equation. Scenario inputs (rewards,
gamma, the assignment's hyper-parameters read from week3/C3W3A1) are stated
once as data; everything derived from them is computed.
"""
import numpy as np
from drillkit import D, M
from masterykit import code


def n(x, d=2):
    """Format a number for prose: d decimals, trailing zeros trimmed."""
    s = ("%." + str(d) + "f") % x
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    if s in ("-0", "&minus;0"):
        s = "0"
    return "&minus;" + s[1:] if s.startswith("-") else s


def pc(x, d=1):
    """A fraction as a percentage string, e.g. 0.125 -> '12.5%'."""
    return n(100 * x, d) + "%"


def big(x):
    return "{:,.0f}".format(x)


# ---------------------------------------------------------------- the rover
# States 1..6 are indices 0..5. Actions: 0 = left, 1 = right. The course's
# convention: R(s) is collected in the state you are leaving, a terminal state
# is worth exactly its own reward.
LEFT, RIGHT = 0, 1
ARR = ("&larr;", "&rarr;")
R1, R6, G = 100.0, 40.0, 0.5


def rewards(r1=R1, r6=R6, extra=None):
    R = np.zeros(6)
    R[0], R[5] = r1, r6
    for s, v in (extra or {}).items():
        R[s - 1] = v
    return R


def bellman(Q, R, gamma, p=0.0, slip="back", stay=False):
    """One sweep of Q(s,a) = R(s) + gamma * E[max_a' Q(s',a')]. p is the
    misstep probability: 'back' sends you the opposite way, 'stay' leaves you
    where you were. stay=True adds a third action, 'wait a turn'."""
    V = Q.max(axis=1)
    Qn = np.zeros_like(Q)
    for i in range(6):
        if i in (0, 5):
            Qn[i, :] = R[i]
            continue
        for a, j in ((LEFT, i - 1), (RIGHT, i + 1)):
            k = 2 * i - j if slip == "back" else i
            Qn[i, a] = R[i] + gamma * ((1 - p) * V[j] + p * V[k])
        if stay:
            Qn[i, 2] = R[i] + gamma * V[i]
    return Qn


def solve(R, gamma, p=0.0, slip="back", stay=False, iters=120):
    Q = np.zeros((6, 3 if stay else 2))
    for _ in range(iters):
        Q = bellman(Q, R, gamma, p, slip, stay)
    return Q


def walk(R, gamma, start, action):
    """Rewards collected by always taking one action, and their discounted sum."""
    s, rs = start - 1, []
    while True:
        rs.append(R[s])
        if s in (0, 5):
            break
        s = s - 1 if action == LEFT else s + 1
    rs = np.array(rs)
    return rs, float(np.sum(rs * gamma ** np.arange(len(rs))))


RW = rewards()
Q0 = solve(RW, G)
V0 = Q0.max(axis=1)
PI0 = Q0.argmax(axis=1)

# ---------------------------------------------------------------- q01 the return
WALK1 = [(s, walk(RW, G, s, LEFT)[1], walk(RW, G, s, RIGHT)[1]) for s in range(1, 7)]
RS1, RET1 = walk(RW, G, 4, LEFT)                       # the quiz question: 12.5
W1 = G ** np.arange(len(RS1))                          # 1, 0.5, 0.25, 0.125
BAD1 = float(np.sum(RS1 * G ** np.arange(1, len(RS1) + 1)))   # discounting the first reward too
SIXK1 = 6
SIX1 = G ** SIXK1
# transfer: steady small pay against one large late payment
STEADY1 = np.array([10.0, 10.0, 10.0, 10.0])
LATE1 = np.array([0.0, 0.0, 0.0, 0.0, 50.0])
GAMS1 = (0.5, 0.9, 0.95)


def _ret(rs, g):
    return float(np.sum(rs * g ** np.arange(len(rs))))


TR1 = [(g, _ret(STEADY1, g), _ret(LATE1, g)) for g in GAMS1]
_grid1 = np.linspace(0.5, 0.999, 49901)
_diff1 = np.array([_ret(LATE1, g) - _ret(STEADY1, g) for g in _grid1])
FLIP1 = _grid1[np.argmax(_diff1 > 0)]

# ---------------------------------------------------------------- q02 policies
def evaluate(pol, R=RW, gamma=G):
    """V under a fixed policy for states 2..5: solve (I - gamma P) V = R."""
    P = np.zeros((6, 6))
    for i, a in zip(range(1, 5), pol):
        P[i, i - 1 if a == LEFT else i + 1] = 1.0
    return np.linalg.solve(np.eye(6) - gamma * P, R)


NONTERM = 6 - 2
POLS2 = [tuple((c_ >> k) & 1 for k in range(NONTERM)) for c_ in range(2 ** NONTERM)]
VALS2 = [evaluate(p) for p in POLS2]
OPT2 = tuple(int(a) for a in PI0[1:5])
VOPT2 = evaluate(OPT2)
N_DOM2 = sum(1 for v in VALS2 if np.all(v >= VOPT2 - 1e-9))     # policies as good as optimal everywhere
N_WORSE2 = sum(1 for v in VALS2 if np.any(v < VOPT2 - 1e-9))
LOOP2 = (LEFT, RIGHT, LEFT, RIGHT)
VLOOP2 = evaluate(LOOP2)
# spot: a route stored as a list, then the rover slips once
ROUTE2_LEN = 3
SLIP2_LAND = 5
ROUTE2_END = SLIP2_LAND - (ROUTE2_LEN - 1)               # two more lefts from state 5
# transfer: a 4 x 4 grid, 2 terminal corners, 4 moves; and a 10 x 10 grid
GRID2a = 4 * 4 - 2
NPOL2a = 4 ** GRID2a
GRID2b = 10 * 10 - 2
NPOL2b = float(4) ** GRID2b

# ---------------------------------------------------------------- q03 the Q function
# spot: Q(2, right) computed as "go right and keep going right"
_rs3, KEEP3 = walk(RW, G, 2, RIGHT)
OK3 = Q0[1, RIGHT]
# work: the same strip with the right-hand rock worth 80
R3W = rewards(r6=80.0)
Q3W = solve(R3W, G)
# transfer: a third action, "wait a turn where you are"
Q3S = solve(RW, G, stay=True)
ARR3 = ("&larr;", "&rarr;", "wait")

# ---------------------------------------------------------------- q04 Bellman
SWEEPS4 = []
_Q4 = np.zeros((6, 2))
for _k in range(5):
    _Q4 = bellman(_Q4, RW, G)
    SWEEPS4.append((_Q4.max(axis=1).copy(), _Q4.argmax(axis=1).copy()))
RSWEEP4 = next(k for k, (_, p_) in enumerate(SWEEPS4) if p_[3] == RIGHT) + 1
FIRST4 = next(k for k, (v, _) in enumerate(SWEEPS4) if np.allclose(v, V0)) + 1
# spot: a mini-batch target with the max taken over the whole batch
QN4 = np.array([[3.0, 7.0], [12.0, 4.0], [0.5, 1.0]])
RB4 = np.array([0.0, 1.0, 0.0])
BAD4 = RB4 + G * np.max(QN4)
OK4 = RB4 + G * np.max(QN4, axis=1)
# transfer: a dust storm at state 3 costs 50 every time you pass through it
RSTORM4 = rewards(extra={3: -50.0})
QSTORM4 = solve(RSTORM4, G)
VSTORM4 = QSTORM4.max(axis=1)
PISTORM4 = QSTORM4.argmax(axis=1)

# ---------------------------------------------------------------- q05 epsilon-greedy
EPS5, NA5, T5 = 0.2, 4, 1000
QV5 = np.array([-1.3, 4.2, 6.8, 0.5])
PROB5 = np.full(NA5, EPS5 / NA5)
PROB5[np.argmax(QV5)] += 1 - EPS5
NONGREEDY5 = T5 * (1 - PROB5.max())
EACH5 = T5 * PROB5.min()
BADP5 = 1 - EPS5                                        # forgetting the random pick can land on the best
BADO5 = EPS5 / (NA5 - 1)
# decay, as in the assignment's utils.py: E_DECAY = 0.995, E_MIN = 0.01, once per episode
E0_5, EDEC5, EMIN5 = 1.0, 0.995, 0.01
FLOOR5 = int(np.ceil(np.log(EMIN5 / E0_5) / np.log(EDEC5)))
EPS_AT5 = [(k, max(EMIN5, E0_5 * EDEC5 ** k)) for k in (100, 300, 500)]
# transfer: two adverts, greedy versus epsilon-greedy, simulated
_rng5 = np.random.default_rng(5)
CTR5 = np.array([0.04, 0.06])
T5b, RUNS5, EPS5b = 10000, 200, 0.1
SIM5 = {}
for _eps in (0.0, EPS5b):
    _est = np.tile(np.array([1.0, 0.0]), (RUNS5, 1))     # A clicked on its first showing, B did not
    _cnt = np.ones((RUNS5, 2))
    _clk = np.zeros(RUNS5)
    _shB = np.zeros(RUNS5)
    _idx = np.arange(RUNS5)
    for _t in range(T5b):
        _a = np.where(_rng5.random(RUNS5) < _eps, _rng5.integers(0, 2, RUNS5), _est.argmax(axis=1))
        _c = (_rng5.random(RUNS5) < CTR5[_a]).astype(float)
        _cnt[_idx, _a] += 1
        _est[_idx, _a] += (_c - _est[_idx, _a]) / _cnt[_idx, _a]
        _clk += _c
        _shB += (_a == 1)
    SIM5[_eps] = (_clk.mean(), _shB.mean() / T5b, _est[:, 1].mean())
BEST5 = T5b * CTR5.max()

# ---------------------------------------------------------------- q06 function approximation
NS6, NACT6, H6 = 8, 4, 64                               # the assignment's network
REAL6, BIN6 = 6, 2                                      # 6 real numbers, 2 leg contacts (0 or 1)
BINS6 = 10
STATES6 = BINS6 ** REAL6 * 2 ** BIN6
CELLS6 = STATES6 * NACT6
NAIVE6 = BINS6 ** NS6 * NACT6                           # binning the legs as if they were real


def dense_params(sizes):
    return sum(a * b + b for a, b in zip(sizes[:-1], sizes[1:]))


NET6 = dense_params((NS6, H6, H6, NACT6))
RATIO6 = CELLS6 / NET6
STEPS6 = 1000000
FRAC6 = STEPS6 / CELLS6
# transfer: a cart and pole, 4 real numbers, 2 actions
CP_DIM6, CP_ACT6, CP_BINS6 = 4, 2, 20
CP_CELLS6 = CP_BINS6 ** CP_DIM6 * CP_ACT6
CP_NET6 = dense_params((CP_DIM6, H6, H6, CP_ACT6))
HELI_DIM6 = 12
HELI6 = float(BINS6) ** HELI_DIM6

# ---------------------------------------------------------------- q07 DQN architecture
# the assignment: update every 4 steps on a mini-batch of 64 (utils.py, the notebook)
STEPS7, EVERY7, MB7 = 1000, 4, 64
UPD7 = STEPS7 // EVERY7
NAIVE_ACT7, GOOD_ACT7 = STEPS7 * NACT6, STEPS7
NAIVE_TGT7, GOOD_TGT7 = UPD7 * MB7 * NACT6, UPD7 * MB7
NAIVE_TOT7, GOOD_TOT7 = NAIVE_ACT7 + NAIVE_TGT7, GOOD_ACT7 + GOOD_TGT7
NAIVE_P7 = dense_params((NS6 + NACT6, H6, H6, 1))
GOOD_P7 = dense_params((NS6, H6, H6, NACT6))
# spot: one output per torque, torque in [-2, 2] in steps of 0.01, for 1 and 3 joints
TQ7 = np.arange(-2.0, 2.0 + 1e-9, 0.01)
OUT7 = TQ7.size
OUT7_3 = OUT7 ** 3
# transfer: 18 actions, a 128-number state, mini-batch 32
NS7b, NA7b, MB7b = 128, 18, 32
NAIVE_IN7b = NS7b + NA7b
NAIVE_P7b = dense_params((NAIVE_IN7b, H6, H6, 1))
GOOD_P7b = dense_params((NS7b, H6, H6, NA7b))

# ---------------------------------------------------------------- q08 soft updates
TAU8 = 0.01
TAU8a = 1e-3                                            # utils.py in the assignment uses TAU = 1e-3
_w8 = 0.0
STEP8 = []
for _k in range(3):
    _w8 = TAU8 * 1.0 + (1 - TAU8) * _w8
    STEP8.append(_w8)
HALF8 = int(np.ceil(np.log(0.5) / np.log(1 - TAU8)))
NINETY5_8 = int(np.ceil(np.log(0.05) / np.log(1 - TAU8)))
HALF8a = int(np.ceil(np.log(0.5) / np.log(1 - TAU8a)))
# spot: tau on the wrong side
BADSTEP8 = (1 - TAU8) * 1.0 + TAU8 * 0.0
# transfer: hard copy every C steps with the same average age; and the wobble
_k8 = np.arange(20000)
_wts8 = TAU8 * (1 - TAU8) ** _k8
AGE8 = float(np.sum(_k8 * _wts8))
C8 = 2 * AGE8 + 1
WOB8 = np.sqrt(TAU8 / (2 - TAU8))
_rng8 = np.random.default_rng(8)
_on8 = _rng8.normal(0.0, 1.0, 100000)
_tg8 = np.zeros_like(_on8)
for _i in range(1, _on8.size):
    _tg8[_i] = TAU8 * _on8[_i] + (1 - TAU8) * _tg8[_i - 1]
WOBSIM8 = _tg8[5000:].std() / _on8.std()

# ---------------------------------------------------------------- q09 state of RL
EPIS9, MAXT9 = 2000, 1000                               # the assignment notebook
STEPS9 = EPIS9 * MAXT9
UPD9 = STEPS9 // EVERY7
SAMP9 = UPD9 * MB7


def qlearn(seed, Qtrue, p=0.0, alpha=1.0, tol=0.05, cap=100000):
    """Q-learning from experience on the rover, acting at random, until every
    Q(s,a) for states 2..5 is within tol of the true value. Returns steps."""
    rng = np.random.default_rng(seed)
    Q = np.zeros((6, 2))
    s, steps = int(rng.integers(1, 5)), 0
    for steps in range(1, cap + 1):
        a = int(rng.integers(0, 2))
        j = s - 1 if a == LEFT else s + 1
        if p > 0 and rng.random() < p:
            j = 2 * s - j
        nxt = RW[j] if j in (0, 5) else Q[j].max()
        Q[s, a] += alpha * (RW[s] + G * nxt - Q[s, a])
        s = j if j not in (0, 5) else int(rng.integers(1, 5))
        if np.all(np.abs(Q[1:5] - Qtrue[1:5]) <= tol * np.abs(Qtrue[1:5])):
            return steps
    return cap


P10 = 0.1
Q10 = solve(RW, G, P10)
SEEDS9 = 40
DET9 = np.median([qlearn(s, Q0) for s in range(SEEDS9)])
STO9 = np.median([qlearn(s, Q10, p=P10, alpha=0.05) for s in range(SEEDS9)])
# transfer: reward hacking. gamma 0.9, a bonus at state 3 for "making progress"
G9 = 0.9
BSTAR9 = R1 * (1 - G9 ** 2)                             # bonus at which circling 2-3 ties with the rock
HACK9 = []
for _b in (10.0, 20.0):
    _Q = solve(rewards(extra={3: _b}), G9, iters=400)
    HACK9.append((_b, _Q.max(axis=1), _Q.argmax(axis=1)))
LOOP9 = HACK9[1][0] / (1 - G9 ** 2)

# ---------------------------------------------------------------- q10 stochastic environments
V10 = Q10.max(axis=1)
PI10 = Q10.argmax(axis=1)
HAND10 = G * ((1 - P10) * V10[2] + P10 * V10[4])
# expected return, checked by simulation from state 4 under the optimal policy
_rng10 = np.random.default_rng(10)
EP10 = 20000
_pos = np.full(EP10, 3)
_g10 = np.zeros(EP10)
_live = np.ones(EP10, bool)
_t = 0
for _t in range(200):
    _done = (_pos == 0) | (_pos == 5)
    _g10 += np.where(_live & _done, RW[_pos] * G ** _t, 0.0)
    _live &= ~_done
    if not _live.any():
        break
    _step = np.where(PI10[_pos] == LEFT, -1, 1)
    _step = np.where(_rng10.random(EP10) < P10, -_step, _step)
    _pos = np.where(_live, _pos + _step, _pos)
MC10 = _g10.mean()
SHARE10 = np.mean(np.isclose(_g10, RET1))
LOW10 = np.mean(_g10 < RET1 - 1e-9)
# where pi*(4) flips from left to right as the misstep probability rises
def flip_p(slip):
    lo, hi = 0.0, 0.9
    for _ in range(40):
        mid = (lo + hi) / 2
        q = solve(RW, G, mid, slip=slip)
        if q[3, LEFT] >= q[3, RIGHT]:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


FLIP10 = flip_p("back")
# transfer: wheels that spin in place instead of slipping backwards
Q10s = solve(RW, G, P10, slip="stay")
V10s = Q10s.max(axis=1)
P10b = 0.3
Q10b = solve(RW, G, P10b)
Q10bs = solve(RW, G, P10b, slip="stay")
SPINFLIP10 = flip_p("stay")


def _qrow(Q, i, k=2):
    return "<tr><td>%d</td>%s<td>%s</td></tr>" % (
        i + 1, "".join("<td>%s</td>" % n(q, k) for q in Q[i]),
        ARR[int(Q[i].argmax())] if Q.shape[1] == 2 else ARR3[int(Q[i].argmax())])


def qtable(Q, k=2, cols=("Q(s, &larr;)", "Q(s, &rarr;)")):
    head = "<tr><th>s</th>%s<th>&pi;*(s)</th></tr>" % "".join("<th>%s</th>" % c for c in cols)
    return "<table><thead>%s</thead><tbody>%s</tbody></table>" % (
        head, "".join(_qrow(Q, i, k) for i in range(1, 5)))


DRILLS = [

# =================================================================== q01
D("c3w3-q01",
  recall=M("Write the return, and say what &gamma; does to it.",
    """<p>From memory: write the return for a sequence of rewards <var>R</var><sub>1</sub>,
<var>R</var><sub>2</sub>, <var>R</var><sub>3</sub>, &hellip; with discount &gamma;. Which reward is
<b>not</b> discounted at all? What is a reward <var>k</var> steps away multiplied by? What range must
&gamma; lie in?</p>""",
    """<p>Return = <var>R</var><sub>1</sub> + &gamma;<var>R</var><sub>2</sub> +
&gamma;&sup2;<var>R</var><sub>3</sub> + &hellip; &mdash; a reward <var>k</var> steps after the start is
multiplied by &gamma;<sup><var>k</var></sup>.</p>
<p>The first reward, the one collected in the state you start in, has &gamma;<sup>0</sup> = 1: it is not
discounted. &gamma; lies between 0 and 1. Near 0 the agent is impatient; near 1 it is patient.</p>
<p>At the rover's &gamma; = %s a reward %d steps away keeps only %s<sup>%d</sup> = <b>%s</b> of its face
value.</p>""" % (n(G), SIXK1, n(G), SIXK1, pc(SIX1, 2)),
    "The return adds up every reward, shrinking each one by &gamma; once for every step you wait.",
    "A sweet now is worth a whole sweet. A sweet tomorrow is worth a bit less, and a sweet next week "
    "much less, because waiting makes things feel smaller.",
    [("return", "all the rewards from here on, added up after shrinking the later ones"),
     ("discount factor &gamma;", "the number between 0 and 1 you multiply by for each step of waiting"),
     ("step", "one move from one square to the next")]),

  work=M("Returns from every square, going always left or always right.",
    """<p>The rover: rewards %s at state 1 and %s at state 6, zero elsewhere, &gamma; = %s. States 1 and 6
end the trip.</p>
<p>For each start state 1 to 6, compute the return if the rover <b>always goes left</b>, and if it
<b>always goes right</b>. Which start states prefer which direction?</p>""" % (n(R1, 0), n(R6, 0), n(G)),
    """<table><thead><tr><th>start</th><th>always &larr;</th><th>always &rarr;</th><th>better</th></tr></thead><tbody>%s</tbody></table>
<p>From state 4 going left: rewards %s, weights %s, so the return is %s &times; %s = <b>%s</b> &mdash; the
quiz's answer. Only state 5 prefers the right-hand rock: it sits next to the %s and far from the %s.
At a terminal state both columns agree, because the trip ends before any action matters.</p>""" % (
        "".join("<tr><td>%d</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (
            s_, n(l_), n(r_), "&mdash;" if s_ in (1, 6) else ("&larr;" if l_ > r_ else "&rarr;"))
            for s_, l_, r_ in WALK1),
        ", ".join(n(r, 0) for r in RS1), ", ".join(n(w, 3) for w in W1), n(W1[-1], 3), n(R1, 0),
        n(RET1), n(R6, 0), n(R1, 0)),
    "Count the steps to the reward, raise &gamma; to that power, multiply.",
    "Each square further from the rock shrinks what it is worth to you, so a big rock a few squares "
    "away is worth only a small slice of itself.",
    [("terminal state", "a square where the trip stops"),
     ("always left", "a rule that ignores where you are and just drives left")]),

  spot=M("&ldquo;Discount every reward once per step.&rdquo;",
    """<p>A learner computes the return from state 4, always going left, with &gamma; = %s:</p>
<ol><li>The path is 4 &rarr; 3 &rarr; 2 &rarr; 1 and the rewards are %s.</li>
<li>Each reward is discounted once for each step: return = &gamma;&middot;0 + &gamma;&sup2;&middot;0 +
&gamma;&sup3;&middot;0 + &gamma;<sup>4</sup>&middot;%s.</li>
<li>So the return is %s &times; %s = %s.</li></ol>
<p>Which line is wrong, and what is the right answer?</p>""" % (
        n(G), ", ".join(n(r, 0) for r in RS1), n(R1, 0), n(G ** 4, 4), n(R1, 0), n(BAD1)),
    """<p><b>Line 2.</b> The first reward is the one collected in state 4 itself, before any step is
taken, so its weight is &gamma;<sup>0</sup> = 1. The %s is reached after <b>%d</b> steps, so it is
multiplied by &gamma;&sup3; = %s, not &gamma;<sup>4</sup>.</p>
<p>Return = %s &times; %s = <b>%s</b>. Line 2's version carries one &gamma; too many. The quiz's wrong
options %s and %s make the opposite slip, counting too few steps.</p>""" % (
        n(R1, 0), len(RS1) - 1, n(G ** 3, 3), n(G ** 3, 3), n(R1, 0), n(RET1), n(G ** 2 * R1),
        n(G * R1)),
    "The exponent is the number of steps already taken, starting at zero.",
    "The sweet you hold right now isn't shrunk at all. Only sweets you have to walk to get smaller.",
    [("exponent", "the small raised number: how many times you multiply by &gamma;"),
     ("off by one", "counting one too many or one too few")]),

  transfer=M("Four small jobs now, or one big job later?",
    """<p>A delivery robot can take four short jobs that pay %s each, one per step, or drive to a far depot
that pays %s on its fifth step and nothing before. Compute both returns at &gamma; = %s, %s and %s.
Roughly where does the choice flip?</p>""" % (
        n(STEADY1[0], 0), n(LATE1[-1], 0), n(GAMS1[0]), n(GAMS1[1]), n(GAMS1[2])),
    """<table><thead><tr><th>&gamma;</th><th>four jobs</th><th>far depot</th></tr></thead><tbody>%s</tbody></table>
<p>The steady jobs win until &gamma; reaches about <b>%s</b>; above that the depot wins, although it pays
only %s in total against %s. Same rewards, different &gamma;, opposite decision &mdash; &gamma; is part
of the problem you set, not a detail of the solver.</p>""" % (
        "".join("<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (n(g_), n(a_, 3), n(b_, 3))
                for g_, a_, b_ in TR1),
        n(FLIP1, 3), n(LATE1.sum(), 0), n(STEADY1.sum(), 0)),
    "Which stream of rewards is better depends on &gamma; as much as on the rewards.",
    "If you are very hungry you take four small biscuits now. If you can wait, the big cake later "
    "looks better. How patient you are decides.",
    [("stream of rewards", "a list of payments, one per step"),
     ("patient", "&gamma; close to 1: later rewards still count nearly in full")]),
),

# =================================================================== q02
D("c3w3-q02",
  recall=M("Policy versus plan.",
    """<p>From memory: what is a policy, written as a function? How many entries does a policy for the
rover need? Why is a policy more useful than a fixed sequence of moves?</p>""",
    """<p>A policy is &pi;(<var>s</var>) = <var>a</var>: for <b>every</b> state, the action to take there.
For the rover it is a table with one entry for each non-terminal state &mdash; states 2 to 5,
so %d entries.</p>
<p>A sequence of moves assumes you end up where you planned. A policy has an answer ready for whichever
state you actually find yourself in, so a surprise (a slip, a gust) does not break it.</p>""" % NONTERM,
    "A policy is a rule that says what to do in every state, not a route.",
    "A route says &ldquo;turn left, then right, then left&rdquo;. A rule says &ldquo;wherever you are, "
    "here is what to do&rdquo;. If you get lost, only the rule still helps.",
    [("policy &pi;", "the rule that picks an action for each state"),
     ("plan", "a fixed list of moves worked out in advance")]),

  work=M("Evaluate a policy that goes round in circles.",
    """<p>The rover with &gamma; = %s. Policy A is &pi;(2) = &larr;, &pi;(3) = &rarr;, &pi;(4) = &larr;,
&pi;(5) = &rarr;. Compute the return from each of states 2 to 5 when following A. Compare with the
optimal policy &larr; &larr; &larr; &rarr;.</p>""" % n(G),
    """<table><thead><tr><th>state</th><th>policy A</th><th>optimal</th></tr></thead><tbody>%s</tbody></table>
<p>From 3, policy A sends you to 4, which sends you back to 3, for ever. You never reach a rock, so every
reward is 0 and the return is <b>0</b>. States 2 and 5 head straight for a rock and are unaffected.</p>
<p>All 2<sup>%d</sup> = %d policies of the rover were evaluated this way. Exactly <b>%d</b> of them is at
least as good as every other in every state, and the other %d are worse somewhere &mdash; one policy is
best everywhere at once, as the lesson promised.</p>""" % (
        "".join("<tr><td>%d</td><td>%s</td><td>%s</td></tr>" % (i + 1, n(VLOOP2[i]), n(VOPT2[i]))
                for i in range(1, 5)),
        NONTERM, len(POLS2), N_DOM2, N_WORSE2),
    "To score a policy, follow it from each state and add up the discounted rewards.",
    "If the rule for square 3 says &ldquo;go to 4&rdquo; and the rule for 4 says &ldquo;go to 3&rdquo;, "
    "you walk back and forth all day and never get a prize.",
    [("evaluate a policy", "work out how much each state is worth if you follow it"),
     ("optimal policy &pi;*", "the policy with the highest return from every state")]),

  spot=M("A plan stored as a list of moves.",
    """<p>A team writes down what their rover should do from state 4:</p>
<ol><li>The best route from 4 is left, left, left.</li>
<li>So we store the policy as the list [&larr;, &larr;, &larr;] and play it in order.</li>
<li>On the first move the wheels slip and the rover lands in state %d.</li>
<li>It plays the remaining two moves, &larr; &larr;, and stops in state %d.</li></ol>
<p>Which line is the mistake?</p>""" % (SLIP2_LAND, ROUTE2_END),
    """<p><b>Line 2.</b> A list is a plan, not a policy. After the slip it keeps replaying moves made for
states it is no longer in, and runs out of moves in state %d with no reward at all.</p>
<p>A policy is looked up from the state you are in. In state %d the optimal policy says &rarr;, worth
V(%d) = <b>%s</b>; it never needed the slip to be predicted.</p>""" % (
        ROUTE2_END, SLIP2_LAND, SLIP2_LAND, n(V0[SLIP2_LAND - 1])),
    "Store one action per state, so a surprise leaves you with an answer.",
    "Directions that only say &ldquo;left, left, left&rdquo; are useless once you take a wrong turn. "
    "A map that tells you what to do from every corner still works.",
    [("route", "a fixed order of moves"),
     ("look up", "find the answer in a table using where you are")]),

  transfer=M("How many policies does a small grid have?",
    """<p>A robot moves on a 4 &times; 4 grid with 4 moves (up, down, left, right). Two corner squares end
the episode. How many entries does a policy need, and how many different policies are there? Repeat for
a 10 &times; 10 grid. What does that tell you about finding the best policy?</p>""",
    """<p>4 &times; 4: %d non-terminal squares, so a policy is %d entries, and there are 4<sup>%d</sup> =
<b>%s</b> different policies. 10 &times; 10: %d entries and about <b>%s &times; 10<sup>%d</sup></b>
policies.</p>
<p>Nobody finds the best policy by trying them all. You compute Q (or estimate it with a network) and
read the policy off with an argmax, one state at a time. The rover's %d policies were small enough to
check by brute force; nothing real is.</p>""" % (
        GRID2a, GRID2a, GRID2a, big(NPOL2a), GRID2b,
        n(NPOL2b / 10 ** np.floor(np.log10(NPOL2b)), 1), int(np.floor(np.log10(NPOL2b))), len(POLS2)),
    "A policy is a small table, but the number of possible tables explodes.",
    "Choosing one of four arrows for each square is easy. Trying every way of choosing them would take "
    "longer than anyone could ever wait.",
    [("grid world", "a board of squares the robot moves around on"),
     ("brute force", "trying every possibility one by one")]),
),

# =================================================================== q03
D("c3w3-q03",
  recall=M("The definition of Q, word for word.",
    """<p>From memory: complete &ldquo;Q(<var>s</var>, <var>a</var>) is the return if you &hellip;&rdquo;.
Then write V(<var>s</var>) and &pi;*(<var>s</var>) in terms of Q.</p>""",
    """<p>Q(<var>s</var>, <var>a</var>) is the return if you <b>start in <var>s</var>, take action
<var>a</var> once, and then behave optimally</b> after that.</p>
<p>V(<var>s</var>) = max<sub><var>a</var></sub> Q(<var>s</var>, <var>a</var>), and &pi;*(<var>s</var>) =
arg max<sub><var>a</var></sub> Q(<var>s</var>, <var>a</var>). Because everything after the first move is
optimal, any difference between two Q values in the same state is caused by the first move alone.</p>""",
    "Q scores one first move followed by the best possible play.",
    "Q is like asking: if I take this one step first and then play perfectly, how well will I do? Ask it "
    "for each step you could take and pick the biggest answer.",
    [("Q(s, a)", "how good it is to do a in s, then play perfectly"),
     ("V(s)", "the best Q in state s: how good it is to be there"),
     ("arg max", "which choice gives the biggest number, not the number itself")]),

  work=M("Build the Q table for a richer right-hand rock.",
    """<p>Same rover, &gamma; = %s, but the right-hand rock is now worth %s (left still %s). Compute
Q(<var>s</var>, &larr;) and Q(<var>s</var>, &rarr;) for states 2 to 5, then read off &pi;* and V.</p>
<p>Work from the ends inwards: V(2) and V(5) first, because they are one step from a rock.</p>""" % (
        n(G), n(R3W[5], 0), n(R3W[0], 0)),
    """%s
<p>For example Q(4, &rarr;) = 0 + %s &times; V(5) = %s &times; %s = %s, and Q(4, &larr;) = %s &times; V(3) =
%s. The dividing line has moved: state 4 now goes right too. V(2), V(3), V(4), V(5) =
%s.</p>""" % (
        qtable(Q3W), n(G), n(G), n(Q3W[4].max()), n(Q3W[3, RIGHT]), n(G), n(Q3W[3, LEFT]),
        ", ".join(n(v) for v in Q3W.max(axis=1)[1:5])),
    "Fill Q from the rocks inwards; the policy is the bigger of each pair.",
    "Start next to the treasure, where the answer is easy, and walk backwards one square at a time, "
    "shrinking the value as you go.",
    [("Q table", "one number for every square and every move"),
     ("dividing line", "the place where the best direction switches")]),

  spot=M("&ldquo;Take &rarr;, then keep going &rarr;.&rdquo;",
    """<p>A learner computes Q(2, &rarr;) on the original rover (%s and %s, &gamma; = %s):</p>
<ol><li>Q(2, &rarr;) starts in state 2 and goes right.</li>
<li>It keeps going right: 2 &rarr; 3 &rarr; 4 &rarr; 5 &rarr; 6.</li>
<li>The rewards are %s, so Q(2, &rarr;) = %s.</li></ol>
<p>Where does it go wrong?</p>""" % (
        n(R1, 0), n(R6, 0), n(G), ", ".join(n(r, 0) for r in _rs3), n(KEEP3)),
    """<p><b>Line 2.</b> Only the <em>first</em> action is &rarr;. After it the rover is in state 3 and
behaves optimally, which from state 3 means going <b>left</b>, worth V(3) = %s.</p>
<p>Q(2, &rarr;) = 0 + %s &times; %s = <b>%s</b>, %s times line 3's answer. Q assumes good play after a
possibly foolish first move &mdash; that is the quiz's point.</p>""" % (
        n(V0[2]), n(G), n(V0[2]), n(OK3), n(OK3 / KEEP3, 1)),
    "After the first move, Q switches to the best play, whatever the first move was.",
    "One silly step to the right doesn't mean you must keep walking the wrong way. You turn round and "
    "head for the big prize.",
    [("first action", "the one move Q is asking about"),
     ("behave optimally", "from then on, always make the best move")]),

  transfer=M("Add a third action: wait a turn.",
    """<p>Give the rover a third action, <b>wait</b>: it stays where it is for one step. Using
Q(<var>s</var>, wait) = R(<var>s</var>) + &gamma;V(<var>s</var>) and &gamma; = %s, compute all three Q values
for states 2 to 5. Does the policy change?</p>""" % n(G),
    """%s
<p>Waiting is never best: with R(<var>s</var>) = 0, Q(<var>s</var>, wait) = %s &times; V(<var>s</var>), so it
is exactly &gamma; times the best value &mdash; one step of delay and nothing gained. The arg max still reads
the policy straight off the row, with three columns instead of two.</p>""" % (
        qtable(Q3S, cols=("&larr;", "&rarr;", "wait")), n(G)),
    "Q works for any number of actions; the policy is still the biggest number in each row.",
    "Standing still to think costs you a turn. If nothing good happens while you stand there, "
    "it is always better to just move towards the prize.",
    [("wait action", "stay on the same square for one step"),
     ("delay", "getting the same thing later, which &gamma; makes worth less")]),
),

# =================================================================== q04
D("c3w3-q04",
  recall=M("The Bellman equation and its two halves.",
    """<p>From memory: write the Bellman equation for Q. Name the two halves. What is it at a terminal
state? Over which actions is the max taken?</p>""",
    """<p>Q(<var>s</var>, <var>a</var>) = R(<var>s</var>) + &gamma; max<sub><var>a</var>&prime;</sub>
Q(<var>s</var>&prime;, <var>a</var>&prime;).</p>
<p><b>What you get now</b>, R(<var>s</var>), plus <b>the discounted best you can do from where you
land</b>. The max is over the actions <var>a</var>&prime; available in the <em>next</em> state
<var>s</var>&prime;. At a terminal state there is no next state, so Q(<var>s</var>, <var>a</var>) =
R(<var>s</var>).</p>
<p>It only needs the next state, and in DQN its right-hand side becomes the training target
<var>y</var>.</p>""",
    "Value now equals reward now plus the discounted best value from the next state.",
    "How good is this move? What I get right now, plus a little less than the best I can do from where "
    "I end up.",
    [("Bellman equation", "the rule linking a state's value to the next state's value"),
     ("s&prime;", "the next state, where the action takes you"),
     ("target y", "the number the network is trained to predict")]),

  work=M("Run value iteration by hand.",
    """<p>Start with every Q = 0 on the rover (&gamma; = %s). Apply the Bellman equation to every state at
once, using the previous sweep's values on the right-hand side, and record V = max Q after each sweep.
After how many sweeps does it stop changing?</p>""" % n(G),
    """<table><thead><tr><th>sweep</th>%s<th>&pi;(4)</th></tr></thead><tbody>%s</tbody></table>
<p>Sweep 1 only knows the rocks. Each sweep pushes real reward one more square inwards. At sweep %d,
state 4 can see the %s at state 6 but not yet the %s, so it briefly prefers &rarr; (V(4) = %s); one sweep
later the left-hand value arrives and it switches to &larr;. From sweep %d on nothing changes: that is
the solution, found using only one-step lookahead.</p>""" % (
        "".join("<th>V(%d)</th>" % k for k in range(1, 7)),
        "".join("<tr><td>%d</td>%s<td>%s</td></tr>" % (
            i + 1, "".join("<td>%s</td>" % n(v) for v in vv), ARR[int(pp[3])])
            for i, (vv, pp) in enumerate(SWEEPS4)),
        RSWEEP4, n(R6, 0), n(R1, 0), n(SWEEPS4[RSWEEP4 - 1][0][3]), FIRST4),
    "Apply Bellman repeatedly and the true values spread inwards from the rewards.",
    "Like news passing down a line of children: each round, every child hears what the child next to "
    "them knew last round.",
    [("sweep", "one pass applying the equation to every state"),
     ("value iteration", "repeating sweeps until the numbers stop changing")]),

  spot=M("A mini-batch of Bellman targets in NumPy.",
    """<p>Three stored experiences. <code>q_next</code> holds Q(<var>s</var>&prime;, <var>a</var>&prime;)
for both actions in each experience's next state:</p>%s
<p>The targets come out as [%s]. Which line is wrong, and what should the targets be?</p>""" % (
        code("q_next = np.array([[3.0, 7.0], [12.0, 4.0], [0.5, 1.0]])\n"
             "r = np.array([0.0, 1.0, 0.0])\n"
             "gamma = 0.5\n"
             "y = r + gamma * np.max(q_next)"),
        ", ".join(n(v) for v in BAD4)),
    """<p><b>The last line.</b> <code>np.max(q_next)</code> takes one max over the whole batch &mdash;
%s, from the second experience &mdash; and gives it to all three. The max must be over the actions of
<b>each</b> next state: <code>np.max(q_next, axis=1)</code> = [%s].</p>
<p>Correct targets: y = [<b>%s</b>]. The first and third experiences were being credited with a future
they will never see.</p>""" % (
        n(np.max(QN4)), ", ".join(n(v) for v in np.max(QN4, axis=1)), ", ".join(n(v) for v in OK4)),
    "The max in Bellman is over the next state's actions, one row at a time.",
    "Each child should get the best prize from their own lucky bag, not the best prize in anybody's bag.",
    [("mini-batch", "a handful of stored experiences trained on together"),
     ("axis=1", "work along each row separately")]),

  transfer=M("A dust storm in the middle of the strip.",
    """<p>Mission control adds a dust storm at state 3: every time the rover is in state 3 it collects
%s. Everything else is unchanged (&gamma; = %s). Use the Bellman equation to find V and &pi;* for states
2 to 5. Which state changes its mind?</p>""" % (n(RSTORM4[2], 0), n(G)),
    """%s
<p>V(2) is still %s: it is next to the big rock and never enters the storm. V(3) = %s +
%s &times; %s = <b>%s</b>. Crossing the storm now costs more than the %s is worth from state 4, so
<b>state 4 flips to &rarr;</b> and V(4) = %s. One negative reward in the middle and the equation reroutes
everything around it, with no new rule needed.</p>""" % (
        qtable(QSTORM4), n(VSTORM4[1]), n(RSTORM4[2], 0), n(G), n(VSTORM4[1]), n(VSTORM4[2]), n(R1, 0),
        n(VSTORM4[3])),
    "Bellman handles costs in the middle exactly as it handles prizes at the ends.",
    "If the shortcut goes through a puddle that soaks you, the longer dry way to the smaller prize can "
    "be the better walk.",
    [("negative reward", "a cost: a number taken off your score"),
     ("reroute", "pick a different way because one square got worse")]),
),

# =================================================================== q05
D("c3w3-q05",
  recall=M("The &epsilon;-greedy rule and why it exists.",
    """<p>From memory: state the &epsilon;-greedy rule. Why does an agent that always acts greedily on its
current Q estimates fail to correct them? How is &epsilon; normally scheduled over training?</p>""",
    """<p>With probability 1 &minus; &epsilon;, take arg max<sub><var>a</var></sub> Q(<var>s</var>,
<var>a</var>); with probability &epsilon;, pick an action uniformly at random.</p>
<p>A greedy agent only ever takes the action it rates highest, so it only gathers evidence about that
action. An action it underrates is never tried, so the underrating is never corrected &mdash; the error
confirms itself. Forced randomness breaks the loop.</p>
<p>&epsilon; starts near %s (Q is noise early on) and decays to a small floor such as %s, never to 0.</p>""" % (
        n(E0_5, 0), n(EMIN5)),
    "Sometimes act at random, or you never find out that your low ratings were wrong.",
    "If you never try the green ice cream because you think it's horrible, you'll never find out it is "
    "actually your favourite.",
    [("greedy", "always pick what currently looks best"),
     ("explore", "try something else on purpose, to learn about it"),
     ("decay", "shrink a little after each round")]),

  work=M("Action probabilities, and how fast &epsilon; decays.",
    """<p>A lander has %d actions with current Q = [%s] and &epsilon; = %s.</p>
<ol><li>What is the probability of each action being chosen?</li>
<li>Over %s steps, how many non-greedy actions do you expect?</li>
<li>The assignment starts at &epsilon; = %s and multiplies by %s after every episode, with a floor of %s.
What is &epsilon; after %s episodes? When does it reach the floor?</li></ol>""" % (
        NA5, ", ".join(n(q, 1) for q in QV5), n(EPS5), big(T5), n(E0_5, 1), n(EDEC5, 3), n(EMIN5),
        ", ".join(str(k) for k, _ in EPS_AT5)),
    """<ol><li>The random pick can also land on the best action, so the best action (Q = %s) gets
1 &minus; &epsilon; + &epsilon;/%d = <b>%s</b>, and each of the other %d gets &epsilon;/%d = <b>%s</b>.</li>
<li>%s &times; %s = <b>%s</b> non-greedy actions, about %s for each of the other %d.</li>
<li>%s. The floor is first reached after <b>%d</b> episodes.</li></ol>""" % (
        n(QV5.max(), 1), NA5, n(PROB5.max()), NA5 - 1, NA5, n(PROB5.min()), big(T5), n(1 - PROB5.max()),
        n(NONGREEDY5, 0), n(EACH5, 0), NA5 - 1,
        "; ".join("after %d: %s" % (k, n(e, 3)) for k, e in EPS_AT5), FLOOR5),
    "With probability &epsilon; you pick at random, which includes the best action too.",
    "Roll a dice before every move. Most of the time do your favourite thing; on an unlucky roll, "
    "pick anything at all, even your favourite again.",
    [("probability", "how often something happens, as a fraction of the time"),
     ("floor", "the smallest value &epsilon; is allowed to shrink to")]),

  spot=M("&ldquo;No exploration &mdash; training will fix the estimates.&rdquo;",
    """<p>A team's reasoning for setting &epsilon; = 0 from the first step:</p>
<ol><li>The new network rates &ldquo;fire main engine&rdquo; at Q = %s and &ldquo;do nothing&rdquo; at
%s.</li>
<li>Acting greedily wastes no steps on random actions.</li>
<li>Every step trains the network on real rewards, so its estimates keep getting better.</li>
<li>So the estimate for the main engine will be corrected too, given enough steps.</li></ol>
<p>Which line fails?</p>""" % (n(QV5.min(), 1), n(QV5.max(), 1)),
    """<p><b>Line 4.</b> Training only produces targets for actions that were actually taken. A greedy
agent never fires the main engine, so no experience ever says what firing it is worth, and its low
estimate stays low. Line 3 is true only for the actions it takes.</p>
<p>That is the self-confirming error the quiz asks about. Exploration is how the missing evidence gets
collected.</p>""",
    "You cannot learn the value of an action you never take.",
    "You can practise your favourite trick a thousand times and still know nothing about a trick you "
    "have never tried.",
    [("self-confirming", "a belief that stops you collecting the evidence that would change it"),
     ("evidence", "real results that show whether a guess was right")]),

  transfer=M("Choosing between two adverts.",
    """<p>A website shows one of two adverts per visit. Advert A is truly clicked %s of the time, advert B
%s. By luck, A's first showing got a click and B's did not, so the starting estimates are A = %s, B = %s.
Each estimate is then the running click rate of that advert.</p>
<p>Compare greedy (&epsilon; = 0) with &epsilon; = %s over %s visits. A simulation repeated %d times gives
the averages in the answer &mdash; predict them first.</p>""" % (
        pc(CTR5[0], 0), pc(CTR5[1], 0), n(1.0, 0), n(0.0, 0), n(EPS5b), big(T5b), RUNS5),
    """<table><thead><tr><th>&epsilon;</th><th>clicks</th><th>share of visits showing B</th><th>final
estimate of B</th></tr></thead><tbody>%s</tbody></table>
<p>Greedy never shows B: A's estimate falls towards %s but never below B's 0, so B's bad first impression
is never corrected. &epsilon;-greedy shows B by chance, learns its true rate, and switches. The best
possible is %s clicks; greedy gets about %s, &epsilon;-greedy about %s.</p>""" % (
        "".join("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (
            n(e_), n(SIM5[e_][0], 0), pc(SIM5[e_][1]), n(SIM5[e_][2], 3)) for e_ in (0.0, EPS5b)),
        pc(CTR5[0], 0), big(BEST5), n(SIM5[0.0][0], 0), n(SIM5[EPS5b][0], 0)),
    "One unlucky first try can hide the best option for ever unless you keep exploring.",
    "If the first time you tried a game it was boring, you might never play it again, even if it is "
    "the best game in the box.",
    [("advert", "a little message trying to get you to click"),
     ("click rate", "out of all showings, the fraction that got a click")]),
),

# =================================================================== q06
D("c3w3-q06",
  recall=M("Why the table has to go.",
    """<p>From memory: why can Q not be stored as a table once the state is a vector of real numbers?
What replaces the table, what goes in, what comes out? What does the replacement do that a table never
can?</p>""",
    """<p>Real-valued states mean infinitely many states, and you will almost never visit the same one
twice, so a table cannot exist. A neural network replaces it: the state vector goes in (%d numbers for
the lunar lander) and Q values come out.</p>
<p>The network <b>generalises</b>: two nearly identical states are nearly identical inputs, so they get
similar Q values, even if one was never seen. A table treats every row as unrelated. The Bellman equation
is unchanged; only how Q is stored changes.</p>""" % NS6,
    "With infinitely many states you must compute Q from the state, not look it up.",
    "You can't write down an answer for every possible position of a ball in the air, there are too "
    "many. So you learn a rule that works out the answer for any position.",
    [("continuous", "made of real numbers that can take any value, like 3.1416"),
     ("function approximation", "learning a formula that gives Q, instead of storing every Q"),
     ("generalise", "give sensible answers for cases you have never seen")]),

  work=M("Count a binned lunar-lander table against the network.",
    """<p>The lander's state is %d numbers: %d real ones and %d leg contacts that are only 0 or 1. Suppose
you chop each real number into %d bins and keep the legs as they are. How many states are there, and how
many Q entries with %d actions? Compare with the assignment's network, %d &rarr; %d &rarr; %d &rarr; %d.</p>""" % (
        NS6, REAL6, BIN6, BINS6, NACT6, NS6, H6, H6, NACT6),
    """<p>States: %d<sup>%d</sup> &times; 2<sup>%d</sup> = <b>%s</b>. Q entries: &times; %d = <b>%s</b>.</p>
<p>Network parameters: (%d&times;%d + %d) + (%d&times;%d + %d) + (%d&times;%d + %d) = <b>%s</b>, about
%s times fewer. (Binning the legs as if they were real too would give %s entries.)</p>
<p>And the table is the cruder of the two: %d bins cannot tell a small tilt from a large one, and each
of its cells has to be visited to be learned.</p>""" % (
        BINS6, REAL6, BIN6, big(STATES6), NACT6, big(CELLS6), NS6, H6, H6, H6, H6, H6, H6, NACT6, NACT6,
        big(NET6),
        big(RATIO6), big(NAIVE6), BINS6),
    "Even a crude table of the lander has millions of cells; the network has a few thousand weights.",
    "A list with a separate answer for every spot on a huge field would fill a library. A rule that "
    "works out the answer fits on a postcard.",
    [("bin", "a range of values treated as one, like 0&ndash;10 degrees"),
     ("parameter", "a number inside the network that training adjusts")]),

  spot=M("&ldquo;A million steps fills the table.&rdquo;",
    """<p>A team bins the lander as above (%s Q entries) and reasons:</p>
<ol><li>A table is simpler than a network and has no approximation error.</li>
<li>Our simulator runs %s steps overnight.</li>
<li>So by morning every cell will have been visited and learned.</li></ol>
<p>Which line fails, and by how much?</p>""" % (big(CELLS6), big(STEPS6)),
    """<p><b>Line 3.</b> Each step updates one cell. %s steps can touch at most %s / %s = <b>%s</b> of the
cells even once, and in practice far fewer, because the lander visits the same few situations again
and again. Each cell also needs many visits, not one.</p>
<p>Line 1 is shaky as well: binning <em>is</em> an approximation, a coarse one. The fix is a network
that learns from nearby states.</p>""" % (big(STEPS6), big(STEPS6), big(CELLS6), pc(FRAC6, 2)),
    "A table learns only the cells it visits; the network learns from neighbours too.",
    "If you had to taste every single sweet in a giant shop before knowing which you like, you'd never "
    "finish. You learn that sweets that look alike taste alike.",
    [("visit", "the agent actually being in that state and trying that action"),
     ("coarse", "rough: large steps that blur small differences")]),

  transfer=M("A pole balanced on a cart.",
    """<p>A cart-and-pole system has a %d-number state (cart position and speed, pole angle and spin) and
%d actions (push left, push right). With %d bins per number, how big is the table? What size is a
%d &rarr; %d &rarr; %d &rarr; %d network? Would a helicopter with %d numbers at %d bins be any
different?</p>""" % (CP_DIM6, CP_ACT6, CP_BINS6, CP_DIM6, H6, H6, CP_ACT6, HELI_DIM6, BINS6),
    """<p>Cart-pole table: %d<sup>%d</sup> &times; %d = <b>%s</b> entries; the network has <b>%s</b>
parameters. With only %d dimensions a binned table is just about possible, and people do solve
cart-pole that way.</p>
<p>The helicopter at %d bins needs %d<sup>%d</sup> = %s states. The exponent is what kills tables: each
extra state number multiplies the size. The network's input layer just grows by one.</p>""" % (
        CP_BINS6, CP_DIM6, CP_ACT6, big(CP_CELLS6), big(CP_NET6), CP_DIM6, BINS6, BINS6, HELI_DIM6,
        big(HELI6)),
    "Tables can survive a few dimensions; every added dimension multiplies their size.",
    "One more thing to keep track of makes a table ten times bigger, but only adds one more input to a "
    "network.",
    [("dimension", "one of the numbers that describe the state"),
     ("curse of dimensionality", "sizes that multiply with each extra number")]),
),

# =================================================================== q07
D("c3w3-q07",
  recall=M("Two designs, inputs and outputs.",
    """<p>From memory: describe the naive and the improved Q-network for the lunar lander &mdash; input
size, output size, and forward passes needed to choose one action. What must the action set be like for
the improved design to work? What activation goes on the output?</p>""",
    """<p><b>Naive:</b> input = %d state + %d one-hot action = %d; output = 1 number; %d passes to compare all
actions. <b>Improved:</b> input = %d state; output = %d numbers, one Q per action; <b>1</b> pass.</p>
<p>The action set must be fixed, finite and discrete. The output is <b>linear</b>, because Q values are
unbounded and must not be squashed.</p>""" % (NS6, NACT6, NS6 + NACT6, NACT6, NS6, NACT6),
    "Put the actions on the output side and one pass gives every Q you need for the max.",
    "Instead of asking a friend four questions, one for each choice, ask once: &ldquo;score all four "
    "for me&rdquo;.",
    [("forward pass", "running the network once from input to output"),
     ("one-hot", "a list of zeros with a single 1 marking the chosen action"),
     ("linear output", "the raw number, not squashed into 0 to 1")]),

  work=M("Count forward passes for %s steps of training." % big(STEPS7),
    """<p>The assignment trains every %d steps on a mini-batch of %d experiences. Each step chooses an
action (needs all %d Q values) and each experience's target needs max<sub><var>a</var>&prime;</sub>
Q(<var>s</var>&prime;, <var>a</var>&prime;). Count forward passes over %s steps for both designs. Then count
each network's parameters with hidden layers of %d and %d.</p>""" % (
        EVERY7, MB7, NACT6, big(STEPS7), H6, H6),
    """<table><thead><tr><th></th><th>naive</th><th>improved</th></tr></thead><tbody>
<tr><td>choosing actions</td><td>%s &times; %d = %s</td><td>%s</td></tr>
<tr><td>targets (%d updates &times; %d)</td><td>%s</td><td>%s</td></tr>
<tr><td><b>total passes</b></td><td><b>%s</b></td><td><b>%s</b></td></tr>
<tr><td>parameters</td><td>%s</td><td>%s</td></tr></tbody></table>
<p>A factor of %d in passes, and the improved network even has %d fewer parameters: its first layer
shrinks from %d inputs to %d, which saves more than the wider output layer costs.</p>""" % (
        big(STEPS7), NACT6, big(NAIVE_ACT7), big(GOOD_ACT7), UPD7, MB7, big(NAIVE_TGT7), big(GOOD_TGT7),
        big(NAIVE_TOT7), big(GOOD_TOT7), big(NAIVE_P7), big(GOOD_P7), NAIVE_TOT7 // GOOD_TOT7,
        NAIVE_P7 - GOOD_P7, NS6 + NACT6, NS6),
    "Every max over actions costs one pass instead of four.",
    "Four trips to the shop for four things, or one trip with a list. Same shopping, a quarter of the "
    "walking.",
    [("mini-batch", "a handful of saved experiences used for one training update"),
     ("max over actions", "the biggest of the Q values for a state")]),

  spot=M("One output per torque.",
    """<p>A team adapts DQN to a robot arm whose joint takes any torque between %s and %s:</p>
<ol><li>The state is the arm's angles and speeds.</li>
<li>Give the network one output unit per possible torque.</li>
<li>Pick the torque whose output is largest.</li></ol>
<p>Which line breaks, and what happens if they patch it by allowing only torques in steps of %s?</p>""" % (
        n(TQ7[0]), n(TQ7[-1]), n(TQ7[1] - TQ7[0])),
    """<p><b>Line 2.</b> A continuous torque has infinitely many values, so there is no finite list of
outputs. The one-output-per-action design <em>requires</em> a fixed, finite, discrete action set &mdash;
the opposite of the quiz's distractor.</p>
<p>The %s patch gives %s outputs for one joint, and for three joints %s<sup>3</sup> = <b>%s</b>
combinations. Continuous control uses a different family of methods.</p>""" % (
        n(TQ7[1] - TQ7[0]), big(OUT7), big(OUT7), big(OUT7_3)),
    "One output per action only works when actions can be listed.",
    "You can have one button for each of four choices. You can't have a button for every possible "
    "speed of a car.",
    [("torque", "a twisting push, here how hard the joint turns"),
     ("discrete", "separate choices you can count")]),

  transfer=M("A game with %d joystick actions." % NA7b,
    """<p>A game has a %d-number state and %d joystick actions. For both designs (hidden layers %d, %d),
give the input size, output size, passes per decision and passes to build targets for a mini-batch of
%d. Does the saving grow or shrink with more actions?</p>""" % (NS7b, NA7b, H6, H6, MB7b),
    """<table><thead><tr><th></th><th>naive</th><th>improved</th></tr></thead><tbody>
<tr><td>input</td><td>%d + %d = %d</td><td>%d</td></tr>
<tr><td>output</td><td>1</td><td>%d</td></tr>
<tr><td>passes per decision</td><td>%d</td><td>1</td></tr>
<tr><td>passes for %d targets</td><td>%s</td><td>%d</td></tr>
<tr><td>parameters</td><td>%s</td><td>%s</td></tr></tbody></table>
<p>The saving is a factor equal to the number of actions, so it <b>grows</b>: %d&times; here against
%d&times; for the lander.</p>""" % (
        NS7b, NA7b, NAIVE_IN7b, NS7b, NA7b, NA7b, MB7b, big(MB7b * NA7b), MB7b, big(NAIVE_P7b),
        big(GOOD_P7b), NA7b, NACT6),
    "The more actions there are, the more the one-pass design saves.",
    "Asking once for all the scores saves more the more choices there are to score.",
    [("joystick action", "one of the button and direction combinations a player can press"),
     ("factor", "how many times bigger one number is than another")]),
),

# =================================================================== q08
D("c3w3-q08",
  recall=M("The soft update and the problem it solves.",
    """<p>From memory: write the soft update with &tau;. What does &tau; = 1 mean? Why does deep Q-learning
need this when ordinary supervised learning does not?</p>""",
    """<p>W<sub>target</sub> := &tau; W + (1 &minus; &tau;) W<sub>target</sub>, typically &tau; = %s:
%s new, %s old. &tau; = 1 is a hard update: replace the target outright.</p>
<p>In supervised learning the labels <var>y</var> are fixed data. In DQN the targets
<var>y</var> = R + &gamma; max Q&#770;(<var>s</var>&prime;, <var>a</var>&prime;) come from a network, so
when that network jumps, every target jumps. Moving the target network slowly keeps the targets nearly
still while the main network chases them.</p>""" % (n(TAU8), pc(TAU8, 0), pc(1 - TAU8, 0)),
    "Blend the target network towards the trained one slowly, so the targets stop running away.",
    "It is hard to hit a target that jumps every time you throw. Make it slide slowly and you can aim.",
    [("target network", "a slow-moving copy of the network, used only to make targets"),
     ("&tau; (tau)", "how much of the new weights to mix in each update"),
     ("hard update", "copying the weights over completely in one go")]),

  work=M("How fast does the target catch up?",
    """<p>A weight in the main network jumps from 0 to 1 and stays there. The target copy starts at 0 and
is soft-updated every step with &tau; = %s.</p>
<ol><li>Compute the target weight after steps 1, 2 and 3 by hand.</li>
<li>How many steps until it is halfway? Until it is within 5%%?</li>
<li>The assignment's <code>utils.py</code> uses &tau; = %s. How many steps to halfway there?</li></ol>""" % (
        n(TAU8), n(TAU8a, 3)),
    """<ol><li>%s.</li>
<li>After <var>k</var> steps the target is 1 &minus; (1 &minus; &tau;)<sup><var>k</var></sup>. Halfway
first at step <b>%d</b>; within 5%% at step <b>%d</b>.</li>
<li>&tau; = %s: halfway at step <b>%s</b>, ten times slower.</li></ol>
<p>With &tau; = 1 the target would be at 1 after a single step &mdash; and would jump again the moment
the main network did.</p>""" % (
        ", ".join(n(w, 6) for w in STEP8), HALF8, NINETY5_8, n(TAU8a, 3), big(HALF8a)),
    "With &tau; = %s the target closes %s of the remaining gap each step." % (n(TAU8), pc(TAU8, 0)),
    "Like pouring a cup of hot water into a cold bath every minute: the bath warms up, but slowly and "
    "smoothly.",
    [("halfway", "the point where the target has covered half the jump"),
     ("gap", "how far the target still is from the main network")]),

  spot=M("&tau; on the wrong side.",
    """<p>The soft update, written for one weight array:</p>%s
<p>The author expected the target to move 1%% per update. After one update from
<code>w_target = 0</code> towards <code>w = 1</code>, how far has it moved, and which line is wrong?</p>""" % code(
        "tau = 0.01\n"
        "w_target = tau * w_target + (1 - tau) * w"),
    """<p><b>The second line.</b> &tau; multiplies the <em>old</em> target and 1 &minus; &tau; the new
weights, so the target moves <b>%s</b> of the way in one step: almost a hard update, and the targets run
away again.</p>
<p>The rule is W<sub>target</sub> := &tau; W + (1 &minus; &tau;) W<sub>target</sub>:
<code>w_target = tau * w + (1 - tau) * w_target</code>.</p>""" % pc(BADSTEP8, 0),
    "&tau; goes with the new weights; 1 &minus; &tau; keeps the old target.",
    "Mixing paint: you wanted a drop of red in a pot of white. Swap them and you get a pot of red.",
    [("weight array", "the network's numbers for one layer, stored together"),
     ("swap", "put each thing where the other should be")]),

  transfer=M("Soft updates against a copy every C steps.",
    """<p>The original DQN paper instead copied the weights outright every <var>C</var> steps. With
&tau; = %s, the weights in the soft target are on average how many steps old? What <var>C</var> gives the
same average age? And if the main network's weights jitter randomly from step to step, how much of that
jitter reaches the soft target?</p>""" % n(TAU8),
    """<p>A weight from <var>k</var> steps ago carries &tau;(1 &minus; &tau;)<sup><var>k</var></sup> of the
target, so the average age is (1 &minus; &tau;) / &tau; = <b>%s</b> steps. A copy every <var>C</var> steps
has an average age of (<var>C</var> &minus; 1) / 2, which matches at <var>C</var> = <b>%s</b>.</p>
<p>The jitter that gets through is &radic;(&tau; / (2 &minus; &tau;)) = <b>%s</b> of the original; a
simulation of %s steps measured %s. Same lag on average, but the soft target moves smoothly instead
of in jumps, and filters out most of the noise.</p>""" % (
        n(AGE8, 0), n(C8, 0), pc(WOB8), big(_on8.size), pc(WOBSIM8)),
    "A soft update is a smoothed copy: the same lag as copying now and then, without the jumps.",
    "One way is to update the scoreboard only every few minutes; the other is to nudge it a tiny bit "
    "every second. The nudged board is never far behind and never jumps.",
    [("average age", "how long ago, on average, the numbers in the target were learned"),
     ("jitter", "small random wobbles from one step to the next")]),
),

# =================================================================== q09
D("c3w3-q09",
  recall=M("What is real, and what is hard.",
    """<p>From memory: name two places reinforcement learning genuinely works today, and three reasons it
is hard to use elsewhere. Why does a simulator matter so much?</p>""",
    """<p><b>Real:</b> games and control problems with good simulators; RLHF, where the reward comes from
human preference comparisons, used to tune language models.</p>
<p><b>Hard:</b> it needs an enormous number of episodes (sample efficiency); the reward function is hard
to design and agents exploit its loopholes; a policy trained in simulation often fails on real hardware.
Deployed RL is still far less common than supervised learning.</p>
<p>A simulator makes failure free and fast, and RL learns by failing many times.</p>""",
    "RL works where failure is cheap; elsewhere sample cost and reward design make it hard.",
    "Learning to ride a bike by falling a million times is fine in a video game, and not fine on a real "
    "road.",
    [("sample efficiency", "how much experience it takes to learn"),
     ("simulator", "a computer copy of the world where mistakes cost nothing"),
     ("RLHF", "training a language model with rewards from people's preferences")]),

  work=M("The assignment's experience budget.",
    """<p>The lunar-lander assignment allows %s episodes of up to %s steps, and trains every %d steps on a
mini-batch of %d. In the worst case, how many steps of flying is that, how many training updates, and how
many sampled experiences?</p>""" % (big(EPIS9), big(MAXT9), EVERY7, MB7),
    """<p>Steps: %s &times; %s = <b>%s</b>. Updates: %s / %d = <b>%s</b>. Sampled experiences: &times; %d =
<b>%s</b>.</p>
<p>Even the six-square rover needs experience. Learning Q from random moves rather than solving it,
in this module's simulation the median over %d runs to get every Q within 5%% was <b>%s</b> steps when
moves are reliable, and <b>%s</b> when they slip %s of the time. Noise in the world multiplies the
experience you need; a simulator is what makes that affordable.</p>""" % (
        big(EPIS9), big(MAXT9), big(STEPS9), big(STEPS9), EVERY7, big(UPD9), MB7, big(SAMP9),
        SEEDS9, big(DET9), big(STO9), pc(P10, 0)),
    "RL's appetite for experience is cheap only in simulation.",
    "If learning a game takes millions of tries, you can do that on a computer, but not with a real "
    "spaceship.",
    [("episode", "one attempt, from start to crash or landing"),
     ("budget", "the most you are allowed to spend")]),

  spot=M("A pitch that overclaims.",
    """<p>A slide in a project proposal:</p>
<ol><li>RL has produced superhuman play in games with perfect simulators.</li>
<li>RLHF, with rewards from human preference comparisons, is used to tune language models.</li>
<li>RL has largely replaced supervised learning in industry, so we should use it for our sales
forecasts.</li>
<li>Reward design will need careful work, because agents optimise exactly what we write.</li></ol>
<p>Which line would you strike?</p>""",
    """<p><b>Line 3.</b> The overwhelming majority of deployed machine learning is supervised. A sales
forecast has a label &mdash; the actual sales &mdash; so it is a supervised problem, and RL would add
reward design and exploration costs for nothing.</p>
<p>Lines 1, 2 and 4 are honest. Line 4 is the most useful sentence on the slide.</p>""",
    "Claim what RL has done; don't claim it has replaced supervised learning.",
    "Saying &ldquo;everyone uses a hammer now&rdquo; is wrong, and you don't need a hammer to cut paper.",
    [("supervised learning", "learning from examples that come with the right answer"),
     ("overclaim", "say something is bigger or truer than it is")]),

  transfer=M("A progress bonus that teaches the rover to circle.",
    """<p>To &ldquo;encourage progress&rdquo;, an engineer gives the rover a bonus every time it is in
state 3, with &gamma; = %s and the usual rocks. Compute V and &pi;* for bonuses of %s and %s. Above what
bonus does the agent stop going to the rock?</p>""" % (n(G9), n(HACK9[0][0], 0), n(HACK9[1][0], 0)),
    """<table><thead><tr><th>bonus</th>%s<th>&pi;*(2)</th></tr></thead><tbody>%s</tbody></table>
<p>With %s, state 2 &mdash; one step from the %s rock &mdash; turns <b>right</b>. Circling 2 &harr; 3
collects the bonus every other step for ever, worth b / (1 &minus; &gamma;&sup2;) = %s from state 3,
which beats the rock. It starts as soon as the bonus passes %s(1 &minus; &gamma;&sup2;) = <b>%s</b>.</p>
<p>The agent did exactly what the reward said. That is reward hacking, and why reward design is the
hardest engineering in the project.</p>""" % (
        "".join("<th>V(%d)</th>" % k for k in range(2, 6)),
        "".join("<tr><td>%s</td>%s<td>%s</td></tr>" % (
            n(b_, 0), "".join("<td>%s</td>" % n(v, 2) for v in vv[1:5]), ARR[int(pp[1])])
            for b_, vv, pp in HACK9),
        n(HACK9[1][0], 0), n(R1, 0), n(LOOP9), n(R1, 0), n(BSTAR9, 0)),
    "An agent maximises the reward you wrote, loopholes included.",
    "If you give a dog a treat every time it walks past the door, it may just walk back and forth "
    "past the door all day instead of going for its walk.",
    [("reward hacking", "scoring well in a way the designer never meant"),
     ("bonus", "an extra reward added to steer behaviour")]),
),

# =================================================================== q10
D("c3w3-q10",
  recall=M("What changes when the world is random.",
    """<p>From memory: if the intended move succeeds only %s of the time, what does the agent now maximise?
Write the Bellman equation for that case. Does the policy have to become random?</p>""" % pc(1 - P10, 0),
    """<p>It maximises the <b>expected</b> return &mdash; the average over all the ways things could turn
out, weighted by their probabilities.</p>
<p>Q(<var>s</var>, <var>a</var>) = R(<var>s</var>) + &gamma; E[max<sub><var>a</var>&prime;</sub>
Q(<var>s</var>&prime;, <var>a</var>&prime;)]. The only change is the expectation; &gamma;, the max and the
policy carry over. The policy can stay deterministic: the randomness is in the world, not the agent's
choice.</p>""",
    "In a random world you maximise the average return; Bellman gains an expectation and nothing else.",
    "When the floor is slippery you can't be sure where you'll end up, so you choose the move that "
    "works out best on average.",
    [("stochastic", "random: the same action can lead to different places"),
     ("expected value", "the average you would get over very many tries"),
     ("misstep", "the rover going the wrong way by accident")]),

  work=M("One Bellman step with an expectation.",
    """<p>The rover slips the opposite way with probability %s (&gamma; = %s). Solving the strip gives
V(3) = %s and V(5) = %s. By hand, compute Q(4, &larr;): left reaches state 3 with probability %s and
state 5 with probability %s.</p>""" % (
        n(P10), n(G), n(V10[2], 4), n(V10[4], 4), n(1 - P10), n(P10)),
    """<p>Q(4, &larr;) = 0 + %s &times; (%s &times; %s + %s &times; %s) = <b>%s</b>, matching the solved table:</p>%s
<p>Down from %s with perfect control. Simulating %s trips from state 4 with this policy: %s of them
return exactly %s (no slip), %s return less, and the average is <b>%s</b> &mdash; the expected return.
No single trip is worth %s; the average is.</p>""" % (
        n(G), n(1 - P10), n(V10[2], 4), n(P10), n(V10[4], 4), n(HAND10, 4), qtable(Q10),
        n(V0[3]), big(EP10), pc(SHARE10), n(RET1), pc(LOW10), n(MC10, 3), n(V10[3], 2)),
    "Weight each possible next state by its probability, then discount.",
    "If you usually land on a good square and now and then on a worse one, your move is worth the "
    "average of the two, counting the usual one more, then shrunk a little for the step.",
    [("probability", "how often each landing spot happens"),
     ("weighted average", "an average where likelier outcomes count more")]),

  spot=M("&ldquo;Slipping means play safe.&rdquo;",
    """<p>A team's reasoning for the slippery rover (misstep %s, &gamma; = %s):</p>
<ol><li>The Bellman equation still applies, with an expectation over where the rover lands.</li>
<li>From state 4, the left rock is %d steps away and the right rock only %d.</li>
<li>A slippery world rewards caution, so &pi;*(4) becomes &rarr;, the nearer rock.</li></ol>
<p>Which line fails?</p>""" % (pc(P10, 0), n(G), 4 - 1, 6 - 4),
    """<p><b>Line 3.</b> Solving the equation gives Q(4, &larr;) = %s and Q(4, &rarr;) = %s, so &pi;*(4) is
still <b>&larr;</b>. Slipping lowers every value, but the bigger rock is still worth the risk.</p>
<p>Whether caution wins depends on the numbers: here &pi;*(4) only flips once the misstep probability
passes about <b>%s</b>. &ldquo;Always take the safest action&rdquo; is the quiz's distractor.</p>""" % (
        n(Q10[3, LEFT]), n(Q10[3, RIGHT]), pc(FLIP10)),
    "Randomness changes the values; whether it changes the policy has to be computed.",
    "A slippery path to a big prize can still beat a short path to a small one. It only stops being "
    "worth it when you slip a lot.",
    [("safe", "less likely to go wrong, but maybe less rewarding"),
     ("risk", "the chance of things not going as planned")]),

  transfer=M("Wheels that spin instead of slipping back.",
    """<p>A different rover: %s of the time its wheels <b>spin in place</b> and it stays where it is,
instead of going the wrong way. Solve the strip (&gamma; = %s) and compare V(4) with the slip-back rover.
Then repeat both at a misstep probability of %s. Which kind of failure is worse, and does either change
&pi;*(4)?</p>""" % (pc(P10, 0), n(G), pc(P10b, 0)),
    """<table><thead><tr><th>misstep</th><th>kind</th><th>Q(4, &larr;)</th><th>Q(4, &rarr;)</th><th>&pi;*(4)</th></tr></thead><tbody>%s</tbody></table>
<p>Spinning only wastes a step, so it costs less than being thrown backwards: V(4) = %s against %s at
%s. At %s the slip-back rover has already flipped to &rarr;, while the spinning rover still goes
&larr;; it flips only past about <b>%s</b>, against <b>%s</b> for slipping back.</p>
<p>Same expected-value machinery, different transition probabilities, different answer. The model of
<em>how</em> things go wrong matters as much as how often.</p>""" % (
        "".join("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (
            pc(p_, 0), k_, n(q_[3, 0]), n(q_[3, 1]), ARR[int(q_[3].argmax())])
            for p_, k_, q_ in ((P10, "slip back", Q10), (P10, "spin", Q10s),
                               (P10b, "slip back", Q10b), (P10b, "spin", Q10bs))),
        n(V10s[3]), n(V10[3]), pc(P10, 0), pc(P10b, 0), pc(SPINFLIP10), pc(FLIP10)),
    "The expected return depends on where a failure sends you, not only how often it happens.",
    "Tripping and standing still is annoying; tripping and sliding backwards is worse. You'd risk the "
    "long way more often if you only ever stood still.",
    [("transition probabilities", "the chances of landing in each next square"),
     ("spin in place", "the wheels turn but the rover doesn't move")]),
),
]
