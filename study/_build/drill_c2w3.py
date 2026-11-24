# -*- coding: utf-8 -*-
"""Quiz drills — C2 W3. One concept per mock-quiz question, four methods each.

Every number below is COMPUTED here at import time and formatted into the text,
never typed. If a value is wrong, it is wrong in the arithmetic, where you can
see it, not in a sentence. Scenario inputs (the error rates a team reports, the
counts in a confusion matrix) are stated once as data; everything derived from
them is computed.
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


def pc(x, d=1):
    """A fraction as a percentage string, e.g. 0.125 -> '12.5%'."""
    return n(100 * x, d) + "%"


def pts(x, d=1):
    """A gap in percentage points."""
    return n(x, d)


def _prf(tp, fp, fn):
    p = tp / (tp + fp) if (tp + fp) else float("nan")
    r = tp / (tp + fn)
    f = 2 * p * r / (p + r) if (p + r) else 0.0
    return p, r, f


# ---------------------------------------------------------------- q01 diagnosing bias
# (baseline, J_train, J_cv) in percent error
SC1 = [("A", 2.0, 2.5, 9.0), ("B", 1.0, 8.0, 8.6), ("C", 4.0, 9.5, 15.0)]
GAPS1 = [(name, tr - bl, cv - tr) for name, bl, tr, cv in SC1]
SPOT1_BL, SPOT1_TR, SPOT1_CV = 7.0, 7.4, 8.1
SPOT1_BIAS0 = SPOT1_TR - 0.0
SPOT1_BIAS, SPOT1_VAR = SPOT1_TR - SPOT1_BL, SPOT1_CV - SPOT1_TR
TR1_BL, TR1_TR, TR1_CV = 18.0, 15.0, 21.0
TR1_BIAS, TR1_VAR = TR1_TR - TR1_BL, TR1_CV - TR1_TR

# ---------------------------------------------------------------- q02 data splits
_rng2 = np.random.default_rng(2)
M2, TRUE2, K2, REPS2 = 200, 0.10, 20, 5000
_err2 = _rng2.binomial(M2, TRUE2, size=(REPS2, K2)) / M2
ONE2 = _err2[:, 0].mean()
BEST2 = _err2.min(axis=1).mean()
OPT2 = TRUE2 - BEST2
_rng2b = np.random.default_rng(22)
M2b, TRUE2b, K2b = 1000, 0.85, 50
_acc2b = _rng2b.binomial(M2b, TRUE2b, size=(REPS2, K2b)) / M2b
BEST2b = _acc2b.max(axis=1).mean()

# ---------------------------------------------------------------- q03 learning curves
_rng3 = np.random.default_rng(3)
_xtr3 = _rng3.uniform(0, 3, 160); _ytr3 = _xtr3 ** 2 + _rng3.normal(0, 0.5, 160)
_xcv3 = _rng3.uniform(0, 3, 400); _ycv3 = _xcv3 ** 2 + _rng3.normal(0, 0.5, 400)
MS3 = (5, 10, 20, 40, 80, 160)
LC3 = []
for _m in MS3:
    _p = np.polyfit(_xtr3[:_m], _ytr3[:_m], 1)
    _jt = np.mean((np.polyval(_p, _xtr3[:_m]) - _ytr3[:_m]) ** 2) / 2
    _jc = np.mean((np.polyval(_p, _xcv3) - _ycv3) ** 2) / 2
    LC3.append((_m, _jt, _jc))
_p2 = np.polyfit(_xtr3, _ytr3, 2)
JCV3_QUAD = np.mean((np.polyval(_p2, _xcv3) - _ycv3) ** 2) / 2
NOISE3 = 0.5 ** 2 / 2
CVS3 = (14.0, 12.2, 11.0)
GAIN3 = (CVS3[0] - CVS3[1], CVS3[1] - CVS3[2])
RATIO3 = GAIN3[1] / GAIN3[0]
NEXT3 = CVS3[2] - GAIN3[1] * RATIO3

# ---------------------------------------------------------------- q04 skewed data
TP4, FP4, FN4, TN4 = 15, 15, 5, 965
N4 = TP4 + FP4 + FN4 + TN4
ACC4 = (TP4 + TN4) / N4
P4, R4, F4 = _prf(TP4, FP4, FN4)
ACC4_NULL = (FP4 + TN4) / N4
STP4, SFP4, SFN4 = 12, 8, 28
SBAD4 = STP4 / (STP4 + SFP4)
SOK4 = STP4 / (STP4 + SFN4)
MODELS4 = [("A", 0.9, 0.1), ("B", 0.5, 0.5), ("C", 0.7, 0.6)]
SCORES4 = [(k, p, r, (p + r) / 2, 2 * p * r / (p + r)) for k, p, r in MODELS4]

# ---------------------------------------------------------------- q05 threshold
P5 = np.array([0.95, 0.85, 0.78, 0.66, 0.58, 0.52, 0.41, 0.33, 0.22, 0.08])
Y5 = np.array([1, 1, 0, 1, 1, 0, 1, 0, 0, 0])
TH5 = (0.3, 0.5, 0.7)
PR5 = []
for _t in TH5:
    _pred = P5 >= _t
    _tp = np.sum(_pred & (Y5 == 1)); _fp = np.sum(_pred & (Y5 == 0)); _fn = np.sum(~_pred & (Y5 == 1))
    _pp, _rr, _ff = _prf(_tp, _fp, _fn)
    PR5.append((_t, int(_tp), int(_fp), int(_fn), _pp, _rr))
G5_07 = 1 / (1 + np.exp(-0.7))
Z5_07 = np.log(0.7 / 0.3)
_rng5 = np.random.default_rng(5)
_p5 = _rng5.beta(1, 8, 4000)
_y5 = _rng5.random(4000) < _p5
CFN5, CFP5 = 50.0, 2.0
GRID5 = (0.02, 0.04, 0.1, 0.2, 0.3, 0.5)
COST5 = []
for _t in GRID5:
    _pr = _p5 >= _t
    _c = CFN5 * np.sum(~_pr & _y5) + CFP5 * np.sum(_pr & ~_y5)
    COST5.append((_t, _c))
BEST5 = COST5[0]
for _tc in COST5:
    if _tc[1] < BEST5[1]:
        BEST5 = _tc
TSTAR5 = CFP5 / (CFP5 + CFN5)

# ---------------------------------------------------------------- q06 error analysis
NCV6, NWRONG6, NSAMP6 = 5000, 400, 100
ERR6 = NWRONG6 / NCV6
TALLY6 = [("blurry photo", 31), ("small object", 22), ("glare", 12), ("mislabelled", 9)]
EST6 = [(name, k, k / NSAMP6 * NWRONG6, ERR6 * k / NSAMP6) for name, k in TALLY6]
SPOT6 = [("pharmaceutical", 43), ("fake bank login", 30), ("image-only", 38)]
SPOT6_SUM = sum(k for _, k in SPOT6)
SPOT6_NORM = [(nm, k / SPOT6_SUM) for nm, k in SPOT6]
P6T, N6T = 0.20, 100
SE6 = np.sqrt(P6T * (1 - P6T) / N6T)
LO6, HI6 = P6T - 1.96 * SE6, P6T + 1.96 * SE6

# ---------------------------------------------------------------- q07 augmentation
IMG7, ROT7, BRI7, FLIP7 = 2000, 5, 3, 2
PER7 = ROT7 * BRI7 * FLIP7
TOT7 = IMG7 * PER7
PER7_DIG = ROT7 * BRI7
TOT7_DIG = IMG7 * PER7_DIG

# ---------------------------------------------------------------- q08 transfer learning
L8 = (2048, 1024, 512)
BODY8 = L8[0] * L8[1] + L8[1] + L8[1] * L8[2] + L8[2]
OLDHEAD8 = L8[2] * 1000 + 1000
NEWHEAD8 = L8[2] * 3 + 3
TOTAL8 = BODY8 + NEWHEAD8
FRAC8 = NEWHEAD8 / TOTAL8
PER_EX8 = TOTAL8 / 300

# ---------------------------------------------------------------- q09 the NN recipe
BL9 = 1.0
RUNS9 = [("1", "small network", 6.0, 6.8), ("2", "4&times; wider", 1.4, 5.2),
         ("3", "same network, 3&times; data", 1.6, 2.3)]
G9 = [(k, what, tr, cv, tr - BL9, cv - tr) for k, what, tr, cv in RUNS9]
S9_BL, S9_TR, S9_CV = 1.0, 1.2, 7.9
S9_BIAS, S9_VAR = S9_TR - S9_BL, S9_CV - S9_TR

# ---------------------------------------------------------------- q10 fairness
# group: (TP, FN, FP, TN)
GA10 = (180, 20, 30, 570)
GB10 = (30, 20, 2, 148)


def _grp(t):
    tp, fn, fp, tn = t
    nn_ = tp + fn + fp + tn
    return nn_, (tp + tn) / nn_, fn / (tp + fn)


NA10, ACCA10, FNRA10 = _grp(GA10)
NB10, ACCB10, FNRB10 = _grp(GB10)
ACC10 = (GA10[0] + GA10[3] + GB10[0] + GB10[3]) / (NA10 + NB10)
FNR10 = (GA10[1] + GB10[1]) / (GA10[0] + GA10[1] + GB10[0] + GB10[1])
WITH10, WITHB10 = 250, 230
SHARE10 = WITHB10 / WITH10
NG10, PG10 = 60, 0.15
SEG10 = np.sqrt(PG10 * (1 - PG10) / NG10)


DRILLS = [

# =================================================================== q01
D("c2w3-q01",
  recall=M("The two gaps, and the fix for each.",
    """<p>From memory: given a baseline, a training error and a cross-validation error, which
<b>two differences</b> do you compute, what does each one name, and what are two fixes for each?</p>""",
    """<p><b>Baseline &rarr; training</b> is <b>avoidable bias</b>. Fixes: a bigger network, more or
better features, less regularisation (smaller &lambda;), training longer.</p>
<p><b>Training &rarr; cross-validation</b> is <b>variance</b>. Fixes: more training data, more
regularisation (larger &lambda;), fewer features.</p>
<p>Read the gaps, never the raw numbers. A 10% error can be excellent or terrible depending on the
baseline.</p>""",
    "Bias is the gap to the baseline; variance is the gap from training to new data.",
    "If the best players in your class score 9 out of 10 and you score 6 on practice, you need to "
    "get better at the game. If you score 9 on practice but 5 in the real match, you only learned the "
    "practice questions.",
    [("baseline", "the error you could realistically hope for, often what humans get"),
     ("avoidable bias", "how far your training error sits above that baseline"),
     ("variance", "how much worse you do on new data than on data you trained on")]),

  work=M("Diagnose three teams from their three numbers.",
    """<p>Three projects report error rates (all in %%):</p>
<table><thead><tr><th>project</th><th>baseline</th><th>training</th><th>cross-validation</th></tr></thead><tbody>%s</tbody></table>
<p>Compute both gaps for each and name the main problem.</p>""" % "".join(
        "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (nm, n(bl, 1), n(tr, 1), n(cv, 1))
        for nm, bl, tr, cv in SC1),
    """<table><thead><tr><th>project</th><th>bias gap</th><th>variance gap</th><th>diagnosis</th></tr></thead><tbody>
<tr><td>A</td><td>%s</td><td>%s</td><td><b>high variance</b> &mdash; get more data or regularise</td></tr>
<tr><td>B</td><td>%s</td><td>%s</td><td><b>high bias</b> &mdash; bigger model or better features</td></tr>
<tr><td>C</td><td>%s</td><td>%s</td><td><b>both</b> &mdash; fix bias first, then re-measure</td></tr>
</tbody></table>
<p>B and C have similar training errors, but C's baseline is higher, so its bias gap is smaller than it
looks &mdash; and C's variance gap is large as well.</p>""" % (
        pts(GAPS1[0][1]), pts(GAPS1[0][2]), pts(GAPS1[1][1]), pts(GAPS1[1][2]),
        pts(GAPS1[2][1]), pts(GAPS1[2][2])),
    "Subtract twice, then fix whichever gap is bigger.",
    "Two measuring sticks: one from &ldquo;as good as possible&rdquo; to your practice score, one from "
    "your practice score to your real score. The longer stick is the problem to fix.",
    [("gap", "one error rate minus another, in percentage points"),
     ("percentage point", "the plain difference between two percentages, like 9% minus 2% = 7")]),

  spot=M("&ldquo;7.4 points of bias &mdash; build a bigger network.&rdquo;",
    """<p>A team's audio classifier has training error %s%% and cross-validation error %s%%. Their note:</p>
<p>&ldquo;Training error is %s points above zero, so bias is our big problem. Plan: double the
network.&rdquo;</p>
<p>Three annotators, labelling the same clips, disagree with the true label %s%% of the time. Where does the
reasoning break?</p>""" % (n(SPOT1_TR, 1), n(SPOT1_CV, 1), n(SPOT1_BIAS0, 1), n(SPOT1_BL, 1)),
    """<p>They compared training error with <b>zero</b> instead of with the <b>baseline</b>. Against the
%s%% human baseline the avoidable bias is only <b>%s points</b>, and the variance gap is <b>%s points</b>.
Neither is large; this model is close to the noise floor of its own labels.</p>
<p>Doubling the network chases error that is mostly noise in the audio.</p>""" % (
        n(SPOT1_BL, 1), pts(SPOT1_BIAS), pts(SPOT1_VAR)),
    "Measure bias against what is achievable, never against perfection.",
    "If even the teachers get 7 questions wrong on a really blurry test, scoring 7.4 wrong isn't "
    "a disaster. You can't beat a test that is partly impossible.",
    [("noise floor", "error no model can remove, because the information isn't in the input"),
     ("annotator", "a person who writes the correct answers for the data")]),

  transfer=M("A weather model that beats its baseline on training.",
    """<p>A rain forecaster is compared with the simple rule &ldquo;tomorrow is like today&rdquo;, which is wrong
%s%% of the time. Your model: training error %s%%, cross-validation error %s%%. Compute the gaps. What
does a <b>negative</b> bias gap mean, and what should you work on?</p>""" % (
        n(TR1_BL, 0), n(TR1_TR, 0), n(TR1_CV, 0)),
    """<p>Bias gap: %s &minus; %s = <b>%s</b> points. Variance gap: %s &minus; %s = <b>%s</b> points.</p>
<p>A negative bias gap means the training error is already <b>below</b> the baseline. Here that just
says the baseline is a weak rule rather than a floor &mdash; it is not human-level performance. The
clear problem is the <b>%s-point variance gap</b>: on new days the model does worse than the simple
rule. Work on more data or regularisation.</p>""" % (
        n(TR1_TR, 0), n(TR1_BL, 0), pts(TR1_BIAS, 0), n(TR1_CV, 0), n(TR1_TR, 0), pts(TR1_VAR, 0),
        pts(TR1_VAR, 0)),
    "A baseline is any honest yardstick; the gap pattern still tells you what to fix.",
    "Beating a simple guess while practising, then losing to it in the real game, means you "
    "memorised your practice days instead of learning the weather.",
    [("persistence rule", "forecasting that tomorrow will look like today"),
     ("yardstick", "something simple you compare against")]),
),

# =================================================================== q02
D("c2w3-q02",
  recall=M("Three sets, three jobs.",
    """<p>From memory: what is each of the training, cross-validation and test sets used for? Which one may
you look at only once, and why?</p>""",
    """<ul><li><b>Training</b>: fit the parameters <var>w</var>, <var>b</var>.</li>
<li><b>Cross-validation</b>: choose between models &mdash; degree, architecture, &lambda;.</li>
<li><b>Test</b>: report the final error of the one chosen model, once.</li></ul>
<p>The test set must not influence any decision. Every choice made using a set makes that set's error
look better than new data will, so it stops being an honest estimate.</p>""",
    "Fit on train, choose on cross-validation, report on test exactly once.",
    "Practise with homework, pick your best method using a practice quiz, and only then sit the real "
    "exam. If you peeked at the exam to choose your method, your exam score would flatter you.",
    [("cross-validation set", "data kept apart to choose between models (also: dev or validation set)"),
     ("unbiased estimate", "a number that is not tilted by having been used to make choices")]),

  work=M("Measure the optimism of picking the best of twenty.",
    """<p>Twenty models are <b>all truly %s accurate &mdash; error %s on new data</b>. Each is scored on the
same %s-example test set, and the lowest test error is reported. A simulation repeats this %s times.
Before reading on, guess: what is the average reported error?</p>""" % (
        pc(1 - TRUE2, 0), pc(TRUE2, 0), M2, "{:,}".format(REPS2)),
    """<p>One model on its own averages <b>%s</b> on the test set &mdash; honest. The best of twenty averages
<b>%s</b>: about <b>%s points</b> too optimistic, though no model is better than any other.</p>
<p>The winner won partly by luck on those %s examples. Choose on cross-validation, then report the
winner on a test set it has never influenced, and the number goes back to the truth.</p>""" % (
        pc(ONE2, 2), pc(BEST2, 2), n(100 * OPT2, 1), M2),
    "Picking the best score on a set makes that score too good to trust.",
    "If twenty kids flip a coin ten times, someone will get eight heads. That kid is not a better "
    "flipper; they got lucky, and the record makes them look skilled.",
    [("simulation", "running a random experiment many times on a computer to see the average"),
     ("optimistic", "looks better than it really is")]),

  spot=M("A report that chose its model on the test set.",
    """<p>A project write-up:</p>
<ol><li>Split the data 60 / 20 / 20 into train, cross-validation and test.</li>
<li>Trained polynomial models of degree 1 to 10 on the training set.</li>
<li>Picked degree 6 because it had the lowest <b>test</b> error.</li>
<li>Reported that test error as the expected error on new data.</li></ol>
<p>Which line breaks the method?</p>""",
    """<p><b>Line 3.</b> The degree was chosen on the test set, so the reported test error in line 4 is
optimistic. The cross-validation set exists for exactly this choice and was never used.</p>
<p>Fix: choose the degree by cross-validation error, then report the test error of that single model.</p>""",
    "Any set used to choose a model can no longer grade it honestly.",
    "Choosing which answer to keep by checking the answer sheet, and then saying you scored well, "
    "doesn't count.",
    [("degree", "the highest power of x in a polynomial model"),
     ("write-up", "the report of what was done and what was found")]),

  transfer=M("A competition leaderboard is the same trap.",
    """<p>A data competition scores submissions on a public set of %s examples and ranks entrants by their
best public score. A team submits <b>%s</b> slightly different models, all truly %s accurate, and keeps
the best public score. What do they see, and what happens on the hidden final set?</p>""" % (
        "{:,}".format(M2b), K2b, pc(TRUE2b, 0)),
    """<p>Simulated, the best of %s public scores averages <b>%s</b> &mdash; above the true %s. On the hidden
set, used once, the chosen model scores about %s again.</p>
<p>That drop is the same optimism as choosing on a test set. The public leaderboard has quietly
become a cross-validation set; only the hidden set is a test set.</p>""" % (
        K2b, pc(BEST2b, 2), pc(TRUE2b, 0), pc(TRUE2b, 0)),
    "Many looks at one scoreboard turn it into a selection set.",
    "If you can retake a quiz fifty times and only your best try counts, your best score says more "
    "about your luck than your knowledge.",
    [("leaderboard", "a ranking of submissions by score"),
     ("hidden set", "data nobody can score against until the very end")]),
),

# =================================================================== q03
D("c2w3-q03",
  recall=M("Sketch both learning-curve shapes.",
    """<p>On paper, draw J<sub>train</sub> and J<sub>cv</sub> against training-set size <var>m</var> for a
<b>high-bias</b> model and for a <b>high-variance</b> model, with a dashed baseline line. Label which one
more data would help.</p>""",
    """<p><b>High bias:</b> J<sub>train</sub> rises, J<sub>cv</sub> falls, they meet early and go flat
<b>well above</b> the baseline. Small gap. More data does <b>not</b> help.</p>
<p><b>High variance:</b> J<sub>train</sub> stays low (often below the baseline), J<sub>cv</sub> is much
higher and still falling at the right edge. Large gap. More data <b>does</b> help.</p>""",
    "Flat and close together means the model is the limit; a falling gap means data is the limit.",
    "If two runners' times stop changing and they are both slow, more practice laps won't help; they "
    "need better legs. If one is still getting faster every week, keep the practice coming.",
    [("learning curve", "error plotted against how many training examples were used"),
     ("plateau", "where a curve goes flat and stops improving")]),

  work=M("Build a real learning curve for a straight line on curved data.",
    """<p>The data follow <var>y</var> = <var>x</var>&sup2; plus noise. A straight line is fitted on the first
<var>m</var> training examples and scored on %s cross-validation examples (cost = mean squared error / 2):</p>
<table><thead><tr><th>m</th><th>J<sub>train</sub></th><th>J<sub>cv</sub></th></tr></thead><tbody>%s</tbody></table>
<p>Describe the shape and say whether more data would help.</p>""" % (
        len(_xcv3), "".join("<tr><td>%d</td><td>%s</td><td>%s</td></tr>" % (m_, n(jt, 3), n(jc, 3))
                            for m_, jt, jc in LC3)),
    """<p>Training cost climbs from %s and cross-validation cost drops from %s until both settle together,
at %s and %s by <var>m</var> = %d. Both are far above the noise level of about %s. That is <b>high
bias</b>: a straight line cannot bend, and more examples just pin down the same wrong line.</p>
<p>Fitting a quadratic instead on the same %d examples gives J<sub>cv</sub> = <b>%s</b> &mdash; close to the
noise. The fix was model capacity, not data.</p>""" % (
        n(LC3[0][1], 3), n(LC3[0][2], 3), n(LC3[-1][1], 3), n(LC3[-1][2], 3), LC3[-1][0], n(NOISE3, 3),
        LC3[-1][0], n(JCV3_QUAD, 3)),
    "When the curves have met high and flat, change the model, not the data.",
    "A ruler can't trace a smile however many dots you give it. A bendy line can.",
    [("noise level", "the error left over even with the perfect curve"),
     ("quadratic", "a curve using x and x&sup2;")]),

  spot=M("A plan to label 20,000 more examples.",
    """<p>&ldquo;Our learning curves at <var>m</var> = 2,000: training error 15%, cross-validation error 16%,
both flat since <var>m</var> = 800. Human error is 4%. Plan: label 20,000 more examples to bring the error
down.&rdquo;</p>
<p>Where does the plan go wrong?</p>""",
    """<p>The curves have <b>already met and flattened</b> far above the 4% baseline: a 1-point gap and an
11-point bias gap. That is high bias, and more data cannot help a model that is already at its own
ceiling. The 20,000 labels would be money burnt.</p>
<p>Fix: a bigger network, better features or less regularisation first.</p>""",
    "Flat, close curves above the baseline mean more data is wasted.",
    "If you already know every answer in the textbook and still fail, buying a second copy of the "
    "same textbook won't help.",
    [("labelling", "having people write the correct answer for each example"),
     ("ceiling", "the best a model can do, whatever data you give it")]),

  transfer=M("Use the curve to decide a data budget.",
    """<p>A high-variance model's cross-validation error at 1,000, 2,000 and 4,000 examples is %s%%, %s%% and
%s%%. Each doubling of labelled data costs the same. Estimate the next doubling's gain and decide
whether it is worth buying.</p>""" % (n(CVS3[0], 1), n(CVS3[1], 1), n(CVS3[2], 1)),
    """<p>Gains per doubling: <b>%s</b> then <b>%s</b> points, so each doubling gives about %s of the one
before. The next would give roughly %s points, bringing cross-validation error near <b>%s%%</b>.</p>
<p>The curve is still falling, so data helps &mdash; but with shrinking returns. Whether another doubling
is worth it depends on what %s points are worth to you, and the curve has priced it for you. This is a
rough extrapolation, not a guarantee.</p>""" % (
        pts(GAIN3[0]), pts(GAIN3[1]), n(RATIO3, 2), pts(GAIN3[1] * RATIO3), n(NEXT3, 1),
        pts(GAIN3[1] * RATIO3)),
    "A still-falling curve prices the next batch of data before you pay for it.",
    "If each new box of puzzles makes you a bit less better than the last box did, you can guess how "
    "much the next box will help before you buy it.",
    [("doubling", "twice as many examples as before"),
     ("diminishing returns", "each extra step helps less than the one before"),
     ("extrapolate", "guess past the end of what you have measured")]),
),

# =================================================================== q04
D("c2w3-q04",
  recall=M("Precision and recall, by their denominators.",
    """<p>From memory: write precision and recall in terms of true positives, false positives and false
negatives. Say in words what each one's denominator is. Then write F1.</p>""",
    """<p>Precision = TP / (TP + FP) &mdash; denominator: <b>everything you flagged</b>.</p>
<p>Recall = TP / (TP + FN) &mdash; denominator: <b>everything that was really positive</b>.</p>
<p>F1 = 2&middot;P&middot;R / (P + R), the harmonic mean, which stays low if either one is low.</p>""",
    "Precision divides by what you flagged; recall divides by what was really there.",
    "Precision: when you shout &ldquo;found one!&rdquo;, how often are you right? Recall: of all the "
    "hidden eggs, how many did you find?",
    [("true positive (TP)", "said yes, and it was yes"),
     ("false positive (FP)", "said yes, but it was no &mdash; a false alarm"),
     ("false negative (FN)", "said no, but it was yes &mdash; a miss")]),

  work=M("A fraud model that ties with doing nothing.",
    """<p>Of %s transactions, %d are fraud. A model flags %d, of which %d are fraud. Fill in the confusion
matrix and compute accuracy, precision, recall and F1. Then compute the accuracy of a model that
says &ldquo;not fraud&rdquo; every time.</p>""" % ("{:,}".format(N4), TP4 + FN4, TP4 + FP4, TP4),
    """<p>TP = %d, FP = %d, FN = %d, TN = %d.</p>
<p>Accuracy = (%d + %d) / %s = <b>%s</b>. Precision = %d / %d = <b>%s</b>. Recall = %d / %d =
<b>%s</b>. F1 = <b>%s</b>.</p>
<p>The do-nothing model's accuracy is %d / %s = <b>%s</b> &mdash; exactly the same. Accuracy cannot tell a
working fraud detector from one that catches nothing; precision and recall can.</p>""" % (
        TP4, FP4, FN4, TN4, TP4, TN4, "{:,}".format(N4), pc(ACC4), TP4, TP4 + FP4, n(P4, 2),
        TP4, TP4 + FN4, n(R4, 2), n(F4, 2), FP4 + TN4, "{:,}".format(N4), pc(ACC4_NULL)),
    "On rare classes, accuracy can't tell a useful model from a useless one.",
    "If only 2 kids in 100 are hiding, guessing &ldquo;nobody is hiding&rdquo; is right 98 times. "
    "That's a great score and a terrible seeker.",
    [("confusion matrix", "a 2-by-2 table of what was predicted against what was true"),
     ("accuracy", "the fraction of all predictions that were right"),
     ("F1", "one score that combines precision and recall and punishes either being low")]),

  spot=M("Recall computed with the wrong denominator.",
    """<p>A fraud model has TP = %d, FP = %d, FN = %d. The report says:</p>
<p>&ldquo;Recall = %d / (%d + %d) = %s, so we catch %s of all fraud.&rdquo;</p>
<p>Find the slip and the right figure.</p>""" % (
        STP4, SFP4, SFN4, STP4, STP4, SFP4, n(SBAD4, 2), pc(SBAD4, 0)),
    """<p>That is <b>precision</b>: it divides by what was flagged (TP + FP). Recall divides by what was
really fraud (TP + FN): %d / (%d + %d) = <b>%s</b>. They catch only <b>%s</b> of the fraud &mdash; half
what the report claims.</p>""" % (STP4, STP4, SFN4, n(SOK4, 2), pc(SOK4, 0)),
    "Recall's denominator is the real positives, including the ones you missed.",
    "&ldquo;How many eggs did I find?&rdquo; must count the eggs you never found, not the stones you "
    "thought were eggs.",
    [("denominator", "the number on the bottom of a fraction"),
     ("report", "the written results someone else will read")]),

  transfer=M("Rank three models by F1, not by the plain average.",
    """<p>Three models for flagging dangerous messages:</p>
<table><thead><tr><th>model</th><th>precision</th><th>recall</th></tr></thead><tbody>%s</tbody></table>
<p>Compute the plain average and F1 for each. Which ranking would you trust, and why?</p>""" % "".join(
        "<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (k, n(p, 1), n(r, 1)) for k, p, r in MODELS4),
    """<table><thead><tr><th>model</th><th>average</th><th>F1</th></tr></thead><tbody>%s</tbody></table>
<p>The average ranks A level with B, though A misses nine dangerous messages in ten. F1 gives A
only <b>%s</b>, because a harmonic mean refuses to be rescued by one strong half. C wins on F1.</p>""" % (
        "".join("<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (k, n(a, 2), n(f, 2))
                for k, p, r, a, f in SCORES4), n(SCORES4[0][4], 2)),
    "F1 drops sharply if either precision or recall is low.",
    "A team where one player is brilliant and one never shows up isn't a good team. F1 notices the "
    "missing player.",
    [("harmonic mean", "an average that is pulled hard towards the smaller number"),
     ("ranking", "putting things in order from best to worst")]),
),

# =================================================================== q05
D("c2w3-q05",
  recall=M("What moving the threshold does, and what it doesn't.",
    """<p>From memory: what happens to precision and recall when you <b>raise</b> the threshold? When you
<b>lower</b> it? Does the model change? Who decides where it goes?</p>""",
    """<p>Raise it: fewer, surer positive predictions &rarr; precision usually <b>up</b>, recall
<b>down</b>. Lower it: more positives &rarr; recall up, precision down.</p>
<p>The model's weights do <b>not</b> change; the threshold is applied to its output after training. Where
to put it is a decision about which mistake costs more.</p>""",
    "One trained model, many thresholds: you choose the trade-off, not the weights.",
    "A smoke alarm with a sensitivity dial. Turn it up and it catches every fire but also beeps at "
    "toast. Turn it down and it stops beeping at toast but might miss a small fire. Same alarm.",
    [("threshold", "the cut-off probability above which you say yes"),
     ("operating point", "the precision and recall you get at one chosen threshold")]),

  work=M("Ten predictions, three thresholds.",
    """<p>Ten examples with the model's probability and the true label:</p>
<table><thead><tr><th>probability</th>%s</tr><tr><th>label</th>%s</tr></thead></table>
<p>Compute precision and recall at thresholds 0.3, 0.5 and 0.7.</p>""" % (
        "".join("<td>%s</td>" % n(p, 2) for p in P5), "".join("<td>%d</td>" % y for y in Y5)),
    """<table><thead><tr><th>threshold</th><th>TP</th><th>FP</th><th>FN</th><th>precision</th><th>recall</th></tr></thead><tbody>%s</tbody></table>
<p>As the threshold rises, recall falls steadily; precision rises, then holds. Precision is not
guaranteed to rise at every step &mdash; it depends on which examples cross the line &mdash; but recall
can only fall. Nothing about the model changed between rows.</p>""" % "".join(
        "<tr><td>%s</td><td>%d</td><td>%d</td><td>%d</td><td>%s</td><td>%s</td></tr>"
        % (n(t, 1), tp, fp, fn, n(p, 2), n(r, 2)) for t, tp, fp, fn, p, r in PR5),
    "Higher threshold, fewer yeses: more of them right, more true cases missed.",
    "If you only put your hand up when you are really sure, you're right more often when you do, but "
    "you miss questions you actually knew.",
    [("TP / FP / FN", "caught it / false alarm / missed it"),
     ("threshold", "the probability you must reach before the model says yes")]),

  spot=M("A threshold applied to the wrong number.",
    """<p>The team wants to flag cases with probability at least 0.7. The code:</p>%s
<p>What threshold are they really using?</p>""" % code(
        "z = np.dot(X, w) + b\n"
        "flag = z >= 0.7"),
    """<p><code>z</code> is the input to the sigmoid, not the probability. <code>z &ge; 0.7</code> means
probability &ge; g(0.7) = <b>%s</b>, not 0.7. The threshold is silently lower than intended, so recall
is higher and precision lower than they think.</p>
<p>Fix: compare <code>1 / (1 + np.exp(-z))</code> with 0.7, or equivalently compare <code>z</code> with
ln(0.7 / 0.3) = <b>%s</b>.</p>""" % (n(G5_07, 3), n(Z5_07, 3)),
    "Apply a probability threshold to the probability, after the sigmoid.",
    "Saying &ldquo;only keep apples heavier than 0.7&rdquo; but weighing them in the wrong units keeps "
    "the wrong apples.",
    [("z", "the score before it is squashed into a probability"),
     ("sigmoid", "the function that turns z into a number between 0 and 1")]),

  transfer=M("Choose the threshold from the cost of each mistake.",
    """<p>A screening model: a missed case (false negative) costs %s, a false alarm (false positive) costs
%s. On %s cases, the total cost at each threshold is:</p>
<table><thead><tr><th>threshold</th><th>total cost</th></tr></thead><tbody>%s</tbody></table>
<p>Which threshold would you pick, and why is it so far below 0.5?</p>""" % (
        n(CFN5, 0), n(CFP5, 0), "{:,}".format(len(_p5)),
        "".join("<tr><td>%s</td><td>%s</td></tr>" % (n(t, 2), "{:,.0f}".format(c)) for t, c in COST5)),
    """<p>Pick <b>%s</b>, the lowest total cost. It is low because a miss costs %s times a false alarm,
so it pays to flag generously.</p>
<p>If the probabilities are well calibrated, theory puts the best threshold at cost<sub>FP</sub> /
(cost<sub>FP</sub> + cost<sub>FN</sub>) = <b>%s</b>, which agrees. 0.5 is only right when both mistakes
cost the same.</p>""" % (n(BEST5[0], 2), n(CFN5 / CFP5, 0), n(TSTAR5, 3)),
    "Put the threshold where the cheaper mistake absorbs the risk.",
    "If forgetting your umbrella ruins your day but carrying it is only a little annoying, you take it "
    "even when rain is unlikely.",
    [("calibrated", "a 0.2 from the model really means about a 1-in-5 chance"),
     ("total cost", "the price of all the mistakes added up")]),
),

# =================================================================== q06
D("c2w3-q06",
  recall=M("The error-analysis procedure, step by step.",
    """<p>From memory: list the steps of error analysis. What do you do if there are thousands of
misclassified examples? Can one example belong to two categories?</p>""",
    """<ol><li>Take the misclassified <b>cross-validation</b> examples (a random sample of about 100 if there
are many).</li>
<li>Read each one and tag it with every category that applies &mdash; categories may <b>overlap</b>.</li>
<li>Count each category and rank them.</li>
<li>Work on the biggest categories first. A category's share is the <b>most</b> you could gain by fixing
it completely.</li></ol>""",
    "Read the mistakes, tag them, count them, fix the biggest pile first.",
    "Before tidying your room, sort the mess into piles: clothes, books, toys. Tidy the biggest pile "
    "first and the room looks better fastest.",
    [("category", "a kind of mistake, like &ldquo;blurry photo&rdquo;"),
     ("overlap", "one example can fall into more than one pile")]),

  work=M("From a 100-example tally to a ceiling on each fix.",
    """<p>A photo classifier gets %d of %s cross-validation examples wrong. You read a random %d of the
mistakes and tag them:</p>
<table><thead><tr><th>category</th><th>count in sample</th></tr></thead><tbody>%s</tbody></table>
<p>Estimate how many of all %d mistakes fall in each category, and the most each fix could lower the
%s error rate.</p>""" % (
        NWRONG6, "{:,}".format(NCV6), NSAMP6,
        "".join("<tr><td>%s</td><td>%d</td></tr>" % (nm, k) for nm, k in TALLY6), NWRONG6,
        pc(ERR6, 0)),
    """<table><thead><tr><th>category</th><th>estimated count</th><th>error rate if fixed perfectly</th></tr></thead><tbody>%s</tbody></table>
<p>Fixing every blurry case could take the error from %s to about %s; fixing every mislabelled case,
only to about %s. These are <b>ceilings</b>: real fixes recover part of each pile.</p>""" % (
        "".join("<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (nm, n(est, 0), pc(ERR6 - drop, 2))
                for nm, k, est, drop in EST6),
        pc(ERR6, 0), pc(ERR6 - EST6[0][3], 2), pc(ERR6 - EST6[3][3], 2)),
    "A category's share of the errors caps what fixing it can win.",
    "If a third of your spelling mistakes are one word, learning that word fixes at most a third of "
    "your mistakes.",
    [("sample", "a random handful taken to stand for the whole"),
     ("ceiling", "the most you could gain, if the fix were perfect")]),

  spot=M("A tally that &ldquo;doesn't add up&rdquo;.",
    """<p>An error analysis of 100 misclassified emails found: %s. A reviewer writes:</p>
<p>&ldquo;These sum to %d, which is impossible for 100 emails. I have renormalised them to %s so they add
to 100%%.&rdquo;</p>
<p>What did the reviewer get wrong?</p>""" % (
        ", ".join("%s %d" % (nm, k) for nm, k in SPOT6), SPOT6_SUM,
        ", ".join("%s %s" % (nm, pc(f, 0)) for nm, f in SPOT6_NORM)),
    """<p>Categories in error analysis <b>overlap</b>: an image-only pharmaceutical email is tagged twice.
A sum above 100 is expected, not an error.</p>
<p>Renormalising understates every category &mdash; pharmaceutical really touches <b>%s</b> of the errors,
not %s &mdash; and so understates the ceiling on each fix. Keep the raw counts.</p>""" % (
        pc(SPOT6[0][1] / 100, 0), pc(SPOT6_NORM[0][1], 0)),
    "Overlapping categories can sum past 100; each count still stands on its own.",
    "A kid can be in the choir and on the football team. Counting both clubs counts that kid twice, "
    "and that's fine.",
    [("renormalise", "rescale numbers so they add up to 100%"),
     ("tag", "a label you attach to an example")]),

  transfer=M("How sure is a tally from only 100 examples?",
    """<p>A speech system has 5,000 mistakes. You listen to a random 100 and %d of them have heavy car noise.
How precise is &ldquo;%s of mistakes are car noise&rdquo;? Give a rough 95%% range.</p>""" % (
        int(P6T * N6T), pc(P6T, 0)),
    """<p>The standard error of a proportion is &radic;(p(1&minus;p)/n) = &radic;(%s &times; %s / %d) =
<b>%s</b>. A rough 95%% range is %s &plusmn; 1.96 &times; %s, about <b>%s to %s</b>.</p>
<p>That is precise enough to rank a 20%% category above a 5%% one, but not to separate 20%% from
18%%. If two piles are close, read more examples before betting on one.</p>""" % (
        n(P6T, 2), n(1 - P6T, 2), N6T, n(SE6, 3), n(P6T, 2), n(SE6, 3), pc(LO6, 0), pc(HI6, 0)),
    "A 100-example sample ranks big piles reliably but can't split close ones.",
    "Tasting one spoonful tells you the soup is salty, but not exactly how salty.",
    [("standard error", "how much an estimate would wobble if you took a different sample"),
     ("proportion", "a fraction of the whole, like 20 out of 100")]),
),

# =================================================================== q07
D("c2w3-q07",
  recall=M("The one rule for a good augmentation.",
    """<p>From memory: state the rule that decides whether a distortion is a good augmentation. Give two
good and two bad examples for photos, and one domain where mirroring breaks the label.</p>""",
    """<p>The distortion must be one that <b>plausibly happens in deployment</b>, and it must <b>not change
the label</b>.</p>
<p>Good for photos: small rotations, brightness or contrast changes, realistic blur, crops. Bad: uniform
random pixel noise that never occurs in real photos; any change that alters the class.</p>
<p>Mirroring breaks handwritten digits and letters, where a mirrored 2 is not a 2.</p>""",
    "Only add changes the real world would make, and that leave the answer the same.",
    "If you're learning to spot cats, practising on cats in dim light or tilted photos helps. "
    "Practising on cats covered in rainbow static doesn't, because you'll never see that.",
    [("augmentation", "making new training examples by changing old ones"),
     ("deployment", "when the model is used on real data")]),

  work=M("Count the augmented set, and what it is worth.",
    """<p>You have %s photos. Each is rotated to %d angles, given %d brightness levels, and mirrored or
not. How many training examples is that? How many for handwritten digits, where mirroring is not
allowed?</p>""" % ("{:,}".format(IMG7), ROT7, BRI7),
    """<p>Photos: %d &times; %d &times; %d = <b>%d</b> versions per image, so <b>%s</b> examples.</p>
<p>Digits, without mirroring: %d &times; %d = <b>%d</b> per image, so <b>%s</b>.</p>
<p>These are not %s independent new examples: they are variations on %s originals. Augmentation
teaches the model what should <b>not</b> matter, which helps, but it does not add new kinds of
content.</p>""" % (
        ROT7, BRI7, FLIP7, PER7, "{:,}".format(TOT7), ROT7, BRI7, PER7_DIG, "{:,}".format(TOT7_DIG),
        "{:,}".format(TOT7), "{:,}".format(IMG7)),
    "Augmentation multiplies examples, not information.",
    "Looking at the same dog from five angles helps you know it's the same dog. It doesn't teach "
    "you about any other dog.",
    [("variant", "one changed copy of an example"),
     ("independent", "genuinely new, not a copy of something you already have")]),

  spot=M("An augmentation pipeline for traffic signs.",
    """<p>A team trains a traffic-sign classifier. Their augmentation step, applied to every training
image:</p>
<ol><li>Rotate by a random angle up to 10&deg;.</li>
<li>Change brightness by up to 30%.</li>
<li>Mirror left-to-right with probability one half, keeping the label.</li>
<li>Add a small amount of motion blur.</li></ol>
<p>Which step corrupts the data?</p>""",
    """<p><b>Step 3.</b> A mirrored &ldquo;turn left&rdquo; sign looks like &ldquo;turn right&rdquo;, but
keeps the &ldquo;turn left&rdquo; label. The model is now trained on wrong answers for every
directional sign.</p>
<p>Steps 1, 2 and 4 are realistic: signs are seen tilted, in different light, from a moving car.</p>""",
    "If a change can alter the true answer, it is not augmentation; it is mislabelling.",
    "Looking at a &ldquo;left&rdquo; arrow in a mirror makes it point right. Calling it &ldquo;left&rdquo; "
    "anyway teaches the wrong thing.",
    [("pipeline", "the list of steps applied to each example, in order"),
     ("label", "the correct answer attached to an example")]),

  transfer=M("Augmenting audio for a wake word.",
    """<p>You are training a model to hear the wake word &ldquo;hey lamp&rdquo; on a kitchen speaker. Which of
these would you use, and why?</p>
<ol><li>Mixing in recorded kitchen noise.</li><li>Speeding the clip up or down by 10%.</li>
<li>Playing the clip backwards.</li><li>Adding a little random hiss.</li></ol>""",
    """<p><b>Use 1, 2 and 4.</b> Kitchens are noisy, people speak at different speeds, and cheap microphones
hiss. All happen in deployment and none changes what was said.</p>
<p><b>Not 3.</b> Reversed speech is no longer &ldquo;hey lamp&rdquo;. Notice that random noise is fine
here, unlike pixel noise on photos: the rule is not &ldquo;never add noise&rdquo;, it is &ldquo;only add
what the real world adds&rdquo;.</p>""",
    "The same rule in every domain: copy the real world's distortions, keep the answer intact.",
    "Practising listening in a noisy room helps you hear a friend at a party. Practising with the "
    "words said backwards doesn't.",
    [("wake word", "a phrase that switches a device on"),
     ("hiss", "faint background noise from a microphone")]),
),

# =================================================================== q08
D("c2w3-q08",
  recall=M("Transfer learning: the two steps and the two options.",
    """<p>From memory: name the two steps of transfer learning, the two options for the second step, and
when to use each. Why do the early layers carry over to a new task?</p>""",
    """<p><b>Step 1, pre-training:</b> someone trains a large network on a huge dataset of the same input
type. <b>Step 2, fine-tuning:</b> replace the output layer and train on your data.</p>
<p><b>Option 1:</b> freeze the borrowed layers and train only the new output layer &mdash; for very small
datasets. <b>Option 2:</b> train all layers starting from the borrowed values, at a low learning rate
&mdash; when you have more data.</p>
<p>Early layers detect generic things like edges and textures, which are useful for any image task.</p>""",
    "Borrow the parts that learned general patterns; retrain only what is specific to your task.",
    "Someone who already knows how to read can learn a new subject much faster than someone learning "
    "letters at the same time.",
    [("pre-training", "the first, expensive training on a huge dataset"),
     ("freeze", "keep some weights fixed so training can't change them"),
     ("output layer", "the last layer, which gives the final answer")]),

  work=M("Count what you train in option 1.",
    """<p>A borrowed network has dense layers of %s &rarr; %s &rarr; %s units and an output layer for 1,000
classes. You replace the output with one for 3 classes and use option 1 on 300 labelled images. How
many parameters does the new head have, how many are frozen, and what fraction do you train?</p>""" % (
        "{:,}".format(L8[0]), "{:,}".format(L8[1]), "{:,}".format(L8[2])),
    """<p>Frozen body: %s&times;%s + %s + %s&times;%s + %s = <b>%s</b> parameters. The old 1,000-class head
had %s; the new head has %s&times;3 + 3 = <b>%s</b>.</p>
<p>You train <b>%s</b> of the network &mdash; about %s parameters per image if you trained everything, but
only the head's %s with option 1. That is why option 1 is safe with 300 images.</p>""" % (
        "{:,}".format(L8[0]), "{:,}".format(L8[1]), "{:,}".format(L8[1]), "{:,}".format(L8[1]),
        "{:,}".format(L8[2]), "{:,}".format(L8[2]), "{:,}".format(BODY8), "{:,}".format(OLDHEAD8),
        "{:,}".format(L8[2]), "{:,}".format(NEWHEAD8), pc(FRAC8, 2), "{:,.0f}".format(PER_EX8),
        "{:,}".format(NEWHEAD8)),
    "With little data, train few parameters; borrow the rest.",
    "You don't rebuild a whole bike to change its bell. You keep the bike and fit a new bell.",
    [("parameter", "one number the network learns, like a weight"),
     ("head", "the new output layer you add on top")]),

  spot=M("Fine-tuning everything, too fast, on too little.",
    """<p>A team has 300 labelled X-rays and a network pre-trained on photos. Their plan:</p>
<ol><li>Replace the 1,000-class output layer with a 2-class one.</li>
<li>Unfreeze every layer.</li>
<li>Train at the same learning rate used for pre-training.</li>
<li>Stop when validation accuracy stops improving.</li></ol>
<p>Which steps are risky, and what should they do instead?</p>""",
    """<p><b>Steps 2 and 3 together.</b> With 300 examples, updating millions of borrowed weights at a full
pre-training learning rate quickly overwrites the general features that made the network worth
borrowing.</p>
<p>Instead: freeze the body and train only the new head (option 1). If more data arrives later,
unfreeze and fine-tune with a <b>much smaller</b> learning rate.</p>""",
    "With little data, freeze; when you unfreeze, go slow.",
    "If you borrow a friend's perfect drawing to finish yours, you add a little colour carefully. "
    "You don't scribble all over it.",
    [("unfreeze", "let training change weights that were fixed"),
     ("learning rate", "how big each training step is")]),

  transfer=M("Transfer learning for text.",
    """<p>A company has 400 labelled support tickets in five categories and access to a language model
pre-trained on billions of sentences. Describe how transfer learning applies here, and the one
condition that must hold for it to work.</p>""",
    """<p>Keep the pre-trained model's body, which already represents words and sentences, add a new
five-way output layer, and train only that head on the 400 tickets (option 1). With thousands of
tickets, fine-tune more layers at a low learning rate.</p>
<p>The condition: <b>same input type</b>. A text model transfers to text; it would not help with
images or sensor readings.</p>""",
    "Transfer works across tasks, as long as the input type stays the same.",
    "Knowing English helps you learn to sort English letters into piles quickly. It doesn't help "
    "you sort photos.",
    [("language model", "a network trained on lots of text to understand sentences"),
     ("input type", "what kind of data goes in: pictures, sound, text")]),
),

# =================================================================== q09
D("c2w3-q09",
  recall=M("The two questions of the NN recipe.",
    """<p>From memory: write the recipe for improving a neural network as two questions and their actions.
Why does &ldquo;make it bigger&rdquo; work for neural networks when it didn't classically? What are its
costs?</p>""",
    """<ol><li>Does it do well on the <b>training</b> set (compared with the baseline)? No &rarr; bigger
network, then ask again.</li>
<li>Does it do well on the <b>cross-validation</b> set? No &rarr; more data (and regularisation), then go
back to question 1.</li></ol>
<p>A large network with suitable regularisation usually does as well or better than a small one, so
bias can be fixed without automatically paying in variance. The costs are compute and the need for
more data.</p>""",
    "Not fitting training data? Grow the network. Not fitting new data? Get more data.",
    "If you can't lift the box, get stronger. If you can lift it at home but drop it at school, "
    "practise in more places.",
    [("regularisation", "a penalty that stops weights growing too big"),
     ("compute", "the computer time and power needed to train")]),

  work=M("Apply the recipe to a real experiment log.",
    """<p>Baseline error %s%%. An experiment log (errors in %%):</p>
<table><thead><tr><th>run</th><th>change</th><th>training</th><th>cross-validation</th></tr></thead><tbody>%s</tbody></table>
<p>For each run, compute both gaps and say what the recipe tells you to do next.</p>""" % (
        n(BL9, 1), "".join("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (k, w_, n(tr, 1), n(cv, 1))
                            for k, w_, tr, cv in RUNS9)),
    """<table><thead><tr><th>run</th><th>bias gap</th><th>variance gap</th><th>next step</th></tr></thead><tbody>
<tr><td>1</td><td>%s</td><td>%s</td><td>fails question 1 &rarr; bigger network</td></tr>
<tr><td>2</td><td>%s</td><td>%s</td><td>passes 1, fails 2 &rarr; more data</td></tr>
<tr><td>3</td><td>%s</td><td>%s</td><td>both small &rarr; good enough, or start error analysis</td></tr>
</tbody></table>""" % (
        pts(G9[0][4]), pts(G9[0][5]), pts(G9[1][4]), pts(G9[1][5]), pts(G9[2][4]), pts(G9[2][5])),
    "Each run answers one question; the answer picks the next move.",
    "Fix the biggest problem, check again, fix the next one. Like tightening bolts one by one.",
    [("experiment log", "a list of what you tried and what happened"),
     ("loop", "repeat the same steps until you are done")]),

  spot=M("&ldquo;It's overfitting, so we shrank the network.&rdquo;",
    """<p>Baseline %s%%, training error %s%%, cross-validation error %s%%. The team writes: &ldquo;Classic
overfitting. We halved the number of units in every layer.&rdquo;</p>
<p>What does the recipe say instead?</p>""" % (n(S9_BL, 1), n(S9_TR, 1), n(S9_CV, 1)),
    """<p>The diagnosis is right: bias gap %s, variance gap <b>%s</b>. The action is the classical one, not
the recipe's. Shrinking trades variance for bias and may bring the bias back.</p>
<p>The recipe keeps the network and attacks variance with <b>more data</b> and <b>more
regularisation</b>; a large, well-regularised network rarely does worse than a smaller one.</p>""" % (
        pts(S9_BIAS), pts(S9_VAR)),
    "For a neural network with high variance, add data or regularisation before shrinking it.",
    "If a strong kid keeps showing off and messing up, you don't make them weaker. You give them "
    "more practice and a few rules.",
    [("overfitting", "learning the training data too closely to handle new data"),
     ("units", "the neurons in a layer")]),

  transfer=M("When the recipe's assumptions fail.",
    """<p>The recipe assumes you can grow the network and get more data. Name what you would do instead
for (a) a model that must run on a cheap phone, and (b) a rare disease with 200 labelled scans in the
world.</p>""",
    """<p>(a) Size is capped, so &ldquo;bigger&rdquo; is off the table: look for better features or
architectures, or train a big model and shrink it carefully afterwards &mdash; and accept a higher bias
floor.</p>
<p>(b) More data is off the table: use <b>data augmentation</b>, <b>transfer learning</b> from a model
pre-trained on other scans or images, and stronger regularisation.</p>""",
    "Know the recipe's two levers, and reach for substitutes when one is missing.",
    "If you can't get a bigger toolbox, pick smarter tools. If you can't get more puzzles, learn from "
    "puzzles somebody else already solved.",
    [("constraint", "a limit you can't change"),
     ("substitute", "something that does a similar job when the usual thing isn't available")]),
),

# =================================================================== q10
D("c2w3-q10",
  recall=M("Three facts about fairness, and the one technique.",
    """<p>From memory: why can overall accuracy hide a problem? Why does deleting the protected attribute
often not fix it? Where else can bias enter? What is the basic technique for finding it?</p>""",
    """<ul><li>One accuracy figure averages all groups together, so a small group's errors barely move
it.</li>
<li>Other features often <b>correlate</b> with the protected attribute and carry the same
information.</li>
<li>Historical <b>labels</b> can encode past human decisions, which the model learns to repeat.</li></ul>
<p>Technique: compute every metric &mdash; accuracy, false-negative rate, false-positive rate &mdash;
<b>separately for each group</b>.</p>""",
    "Split every metric by group; one average can hide a group the model fails.",
    "A class average of 90% can hide that one table of kids is getting half their answers marked "
    "wrong. You only see it if you check each table.",
    [("protected attribute", "a characteristic like sex or ethnicity that the law protects"),
     ("proxy", "another feature that carries the same information"),
     ("subgroup", "one group within the whole population")]),

  work=M("One model, two groups, two very different miss rates.",
    """<p>A screening model's results, split by group (TP, FN, FP, TN):</p>
<table><thead><tr><th>group</th><th>TP</th><th>FN</th><th>FP</th><th>TN</th></tr></thead><tbody>
<tr><td>A</td><td>%d</td><td>%d</td><td>%d</td><td>%d</td></tr>
<tr><td>B</td><td>%d</td><td>%d</td><td>%d</td><td>%d</td></tr></tbody></table>
<p>Compute overall accuracy, each group's accuracy, and each group's false-negative rate.</p>""" % (
        GA10 + GB10),
    """<p>Overall accuracy: <b>%s</b>. Group A: %s; group B: %s &mdash; a gap of %s points.</p>
<p>False-negative rate: group A <b>%s</b>, group B <b>%s</b> &mdash; qualified people in group B are
missed <b>%s times</b> as often. Group B is only %s of the data, so the overall false-negative rate of
%s says nothing about group B's %s.</p>""" % (
        pc(ACC10), pc(ACCA10, 2), pc(ACCB10, 1), n(100 * (ACCA10 - ACCB10), 2), pc(FNRA10, 0),
        pc(FNRB10, 0), n(FNRB10 / FNRA10, 0), pc(NB10 / (NA10 + NB10), 0), pc(FNR10, 0),
        pc(FNRB10, 0)),
    "A modest accuracy gap can hide a large gap in who gets missed.",
    "If a teacher marks 1 in 10 right answers wrong for most kids but 4 in 10 for one small group, "
    "the class average barely changes. That group still loses.",
    [("false-negative rate", "of the real yeses, the fraction the model said no to"),
     ("aggregate", "one number for everyone together")]),

  spot=M("&ldquo;We dropped the column, so no audit is needed.&rdquo;",
    """<p>&ldquo;Our model no longer sees the group column, so it cannot treat groups differently. A
per-group audit is unnecessary.&rdquo;</p>
<p>In the training data, %d applicants list a particular club membership, and %d of them are in group B.
What is wrong with the claim?</p>""" % (WITH10, WITHB10),
    """<p>%d / %d = <b>%s</b> of that feature's holders are in group B, so the feature is a strong
<b>proxy</b> for the deleted column. The model can still separate the groups through it.</p>
<p>Removing the attribute is not evidence of fairness; only measuring each group's error rates is.
Keep the audit.</p>""" % (WITHB10, WITH10, pc(SHARE10, 0)),
    "Deleting a column doesn't delete the information; measure the outcome per group.",
    "Hiding someone's name tag doesn't hide who they are if their team shirt is still on.",
    [("audit", "a check of results, here split by group"),
     ("correlated", "tends to go up and down together")]),

  transfer=M("Checking a voice assistant across accents.",
    """<p>A voice assistant's wake-word error rate is measured per accent. One accent has only %d test
recordings and %s errors. Estimate how uncertain that figure is, and say what you would do before
drawing a conclusion.</p>""" % (NG10, pc(PG10, 0)),
    """<p>Standard error &asymp; &radic;(%s &times; %s / %d) = <b>%s</b>, so the true rate could plausibly be
anywhere from about %s to %s.</p>
<p>Before concluding the accent is served worse, collect more recordings for that group so the estimate
is tight enough to compare. Small subgroups are exactly where problems hide and where estimates are
weakest.</p>""" % (
        n(PG10, 2), n(1 - PG10, 2), NG10, n(SEG10, 3), pc(max(PG10 - 1.96 * SEG10, 0), 0),
        pc(PG10 + 1.96 * SEG10, 0)),
    "Per-group checks need enough examples per group to mean something.",
    "If you only asked three kids whether they liked lunch, you wouldn't know much about the whole "
    "class. Ask more before deciding.",
    [("standard error", "how much an estimate would wobble with a different sample"),
     ("accent", "the way a group of people pronounce words")]),
),
]
