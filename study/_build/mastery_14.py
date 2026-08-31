# -*- coding: utf-8 -*-
"""Active Mastery for 14_mlops.py. Values read off the running file.

Depth note (brief §6): almost no equations here either. The weight is in
break/debug and wrong mental models, and the anchor is that recomputing the
scaling statistics at serve time costs 10.2 accuracy points and raises no
error at all.
"""
from masterykit import (section, prose, code, out, semantics, ledger, drill, peek,
                        predict, lab, breaks, invariant, wrong, reconstruct,
                        connections, recall, check)

AM = dict(
    lede="Eleven cards on the file that <b>starts</b> where every other one ends &mdash; with "
         "a model that already works.",
    sections=[

section("0", "&#129517;", "Before you run", "before", kind="orient",
    hook="0.8375 on held-out data. Every other file would stop here.",
    body=prose("""<p>A loan model, two features, <b>0.8375</b> on held-out data. Every other
file in this lane would be finished.</p>
<p>Everything below is a way a <b>working</b> model quietly stops working. <b>Not one of them
raises an error</b>, and that is precisely the difficulty.</p>
<p><b>Watch for three numbers.</b> Recomputing the scaling statistics at serve time costs
<b>10.2 accuracy points</b> silently. Input drift climbs by a factor of <b>400</b> while accuracy
never falls. And a 40-user canary reports <b>+0.1013</b> for a true effect of
<b>+0.0299</b>.</p>""")
    + connections([], [], "../gist/c33.html", "C3 Week 3 &mdash; the gist",
        extra=[("lab", "../scratch/02-logistic-regression.html", "File 02 first",
                "the model here is that logistic regression &mdash; nothing new is being learned")])),

section("1", "&#127991;&#65039;", "What every variable is", "vars", kind="semantics",
    hook="Eight variables, and the two that matter most are not the weights.",
    body=semantics([
        ("X_tr", "(4000, 2) float64", "the training applicants",
         "<b>One row = one loan applicant.</b> Column 0 is income, column 1 is years of "
         "employment.",
         "<b>$ thousands</b> and <b>years</b>",
         "<code>X_tr[0]</code> is one applicant's income and tenure. Income averages "
         "<b>49.85</b>, tenure <b>5.97</b> years.",
         "Real people, real units &mdash; which is why the fairness question in a real version "
         "of this file would not be optional."),
        ("y_tr", "(4000,) int64", "the outcomes",
         "<b>1 = approved, 0 = not.</b> The approval rate is 0.486, close to balanced.",
         "<i>class label</i>",
         "Because it is near 50/50, accuracy is a fair headline here &mdash; which is "
         "<b>not</b> generally true and is why the file says so.",
         "On a 5%-approval dataset every number in this file would need replacing with "
         "precision and recall."),
        ("CHAMP['w']", "(2,) float64", "the learned weights",
         "How much each feature pushes towards approval, in <b>scaled</b> space.",
         "<b>log-odds per standard deviation</b>",
         "<b>[2.3632, 2.2416]</b> &mdash; income and tenure matter almost equally, income "
         "about 5% more.",
         "Same units trap as files 01 and 02: divide by <code>sd</code> to get per-$1000 and "
         "per-year."),
        ("CHAMP['mu'] / ['sd']", "(2,) each", "the scaling statistics",
         "<b>The most important rows in this table.</b> <code>mu</code> = [49.8492, 5.9653], "
         "<code>sd</code> = [15.0456, 2.9750].",
         "<b>$ thousands</b> and <b>years</b>",
         "These are <b>part of the model</b>, not preprocessing. They are stored in "
         "<code>CHAMP</code> alongside w and b for exactly that reason.",
         "Recompute them at serve time instead of reusing these and you lose <b>10.2 accuracy "
         "points</b>, with no error and sensible-looking probabilities."),
        ("REG", "dict of 2", "the model registry",
         "<b>Which model produced which decision.</b> Each entry hashes the data, the weights "
         "and the scaler.",
         "<i>content hashes</i>",
         "<code>fe7074bb3f1f</code> is the champion; <code>0aeb5ebe5181</code> the challenger. "
         "A hash answers &ldquo;is this the same thing?&rdquo; <b>exactly</b>.",
         "&ldquo;Version 3&rdquo; is a label somebody types and can retype. A hash is computed "
         "from the content, so two artefacts with the same hash <b>are</b> the same artefact."),
        ("psi", "function &rarr; float", "population stability index",
         "<b>How far an input distribution has moved</b> from a reference window.",
         "<i>unitless</i>",
         "Conventional thresholds: 0.1 investigate, 0.25 act. In this file it reaches "
         "<b>1.6648</b> while accuracy <b>rises</b>.",
         "It measures the <b>inputs</b>, so it is a hypothesis that something might be wrong "
         "&mdash; never evidence that something is."),
        ("RULE", "float", "the concept-drift dial",
         "<b>How much the relationship between features and outcome has changed.</b> Not a "
         "model parameter &mdash; a property of the world.",
         "<i>unitless</i>",
         "<b>&minus;0.20</b> in the false-alarm experiment: tenure now matters far less. "
         "Accuracy falls to <b>0.5215</b> while every input monitor stays silent.",
         "This is the failure no amount of input monitoring can see, and the reason delayed "
         "labels are a problem rather than an inconvenience."),
        ("bootstrap_diff", "function &rarr; CI", "the canary's confidence interval",
         "<b>How much you are allowed to conclude</b> from a slice of traffic.",
         "<b>accuracy points</b>",
         "At 40 users it reports <b>+0.1013</b>, CI [+0.0000, +0.2250], for a true effect of "
         "<b>+0.0299</b> &mdash; more than three times the truth.",
         "A tiny canary does not give you a small amount of evidence. It gives you a "
         "<b>wildly wrong number</b> with total confidence."),
    ],
    """The rows to remember are <b>mu</b> and <b>sd</b>. They are stored inside
<code>CHAMP</code> deliberately, because they are <b>part of the model</b> &mdash; and treating
them as preprocessing is the most expensive mistake in the file."""),
    ),

section("2", "&#128302;", "Prediction checkpoints", "predict", kind="predict",
    hook="Four, and three of them go against the obvious answer.",
    body=predict([
        ("""Live traffic arrives where incomes run 12.6 higher than training. You could scale
it with the <b>training</b> statistics or recompute them on the live batch. <b>Predict which
is correct and what the other costs.</b>""",
         """<p>Use the <b>training</b> statistics: <b>0.8545</b>. Recomputing gives
<b>0.7530</b> &mdash; a loss of <b>10.2 accuracy points</b>.</p>
<p>Recomputing <i>looks</i> more correct: surely you should standardise against the data you
actually have? No. The weights were learned in a coordinate system defined by the training mu
and sd. <b>Change the coordinate system and the weights mean something else.</b></p>
<p>And it throws no error and returns sensible-looking probabilities. There is no symptom
&mdash; you find it by knowing the rule, or you find it in a quarterly review.</p>"""),
        ("""Over six months, income PSI climbs from 0.0041 to <b>1.6648</b> &mdash; a factor
of 400, far past every conventional threshold. <b>Predict what accuracy does.</b>""",
         """<p>It <b>never falls</b> &mdash; 0.8458, 0.8450, 0.8470, 0.8455, 0.8660, and
finally <b>0.8902</b>, four points <i>higher</i> than it started.</p>
<p>The standard thresholds (0.1 investigate, 0.25 act) would have had you retraining in month
3 and paging someone in month 4, for a model that was working perfectly.</p>
<p><b>Drift in the inputs is not damage.</b> It is a hypothesis, and it is worth exactly as
much as its false-alarm rate.</p>"""),
        ("""Two scenarios: (A) inputs move enormously, (B) inputs are identical but the
<b>rule</b> changes. <b>Predict which one your input monitors catch.</b>""",
         """<p>They catch <b>A</b>, which is fine: PSI <b>2.4719</b> and accuracy
<b>0.9137</b>, <i>up</i> from 0.8375. A loud alarm about a model that got better.</p>
<p>They are completely <b>silent</b> on B: PSI <b>0.0037</b> and accuracy <b>0.5215</b>
&mdash; barely better than a coin flip, on a model that looks perfectly healthy from
outside.</p>
<p>That is <b>concept drift</b>, and only <b>outcomes</b> reveal it. Which is a problem,
because outcomes take 90 days.</p>"""),
        ("""A challenger's true effect is <b>+0.0299</b>. <b>Predict what a 40-user canary
reports</b>, and whether a 200-user canary is enough to ship.""",
         """<p>The 40-user canary reports <b>+0.1013</b> &mdash; more than <b>three times</b>
the truth, with CI [+0.0000, +0.2250].</p>
<p>The 200-user canary gets the point estimate almost exactly right (<b>+0.0298</b>) and its
interval <b>still straddles zero</b>: [&minus;0.0050, +0.0650]. <b>Not enough to ship.</b></p>
<p>Being right by luck is not the same as having evidence. It takes <b>1,000 users</b> before
the interval excludes zero.</p>"""),
    ],
    """Every one of these punishes the intuitive answer. That is the file.""")),

section("3", "&#128295;", "Modify the copy", "lab", kind="lab",
    hook="Five, ending on the rollback that is one string.",
    body=lab([
        ("L1", "Change a value",
         "Shift live incomes by <b>+30</b> instead of +12.6 and re-run the skew comparison.",
         "X_new, y_new = make(4000, seed=9, income_shift=30.0)",
         """<p>The gap between correct and recomputed scaling <b>widens</b> &mdash; the further
serving data drifts from training, the more it costs to standardise against the wrong
statistics.</p>
<p>Now set the shift to <b>0.0</b>: the two approaches agree almost exactly. Which is the
trap. <b>The bug is invisible when your serving data resembles your training data</b>, so it
passes every test written before launch and appears months later.</p>"""),
        ("L2", "Change a parameter",
         "Set <code>RULE = 0.0</code> in the false-alarm experiment &mdash; no concept drift "
         "&mdash; and re-read scenario B.",
         "RULE = 0.0        # was -0.20",
         """<p>Scenario B's accuracy returns to about <b>0.84</b>, and the PSI stays near zero
as before.</p>
<p>So the <b>only</b> thing separating &ldquo;healthy&rdquo; from &ldquo;barely better than
chance&rdquo; is a change in the world that <b>no input monitor can observe</b>. The
observable side of the system is identical in both cases.</p>"""),
        ("L3", "Change the data",
         "Retrain the challenger on <b>only</b> the most recent traffic and compare it with "
         "the champion.",
         "CHALLENGER = fit(X_new[:3000], y_new[:3000])      # recent only, not stacked",
         """<p>It does better on recent traffic and <b>worse on the old distribution</b>
&mdash; you have traded generality for currency.</p>
<p>Whether that is right depends on a question the data cannot answer: <b>is the shift
permanent or seasonal?</b> Retraining on recent data only is correct for a permanent change
and a mistake for a temporary one, and you usually cannot tell which you are in for
months.</p>"""),
        ("L4", "Change an assumption",
         "Ship the challenger on the strength of the <b>200-user</b> canary, then check what "
         "you would have concluded.",
         "for frac in (0.025,):        # 200 users only",
         """<p>The 200-user reading is <b>+0.0298</b> against a true <b>+0.0299</b> &mdash;
almost exactly right, and its interval <b>[&minus;0.0050, +0.0650] includes zero</b>.</p>
<p>So shipping on it would have been <b>correct by luck</b>. Run the same canary on a
challenger that is genuinely neutral and the same interval width would have let you ship a
model with no effect at all.</p>
<p>The discipline: read the <b>interval</b>, not the point estimate. &ldquo;Keep
waiting&rdquo; is the correct reading of a CI that straddles zero, not a failure of the
test.</p>"""),
        ("L5", "Explain it",
         "Explain why a rollback is one string here, and what would have to be true for it not "
         "to be.",
         None,
         """<p>Because both versions are still <b>loadable</b> and each carries <b>its own
scaling statistics</b>. <code>serve(version, X)</code> takes a hash and looks the whole model
up, so changing the version is changing one identifier.</p>
<p>It would <b>not</b> be one string if the old weights were overwritten, if the scaler were
stored separately from the weights, or if the artefacts were not versioned at all &mdash; then
rolling back means <b>retraining</b>.</p>
<p>And loading old weights with the <i>new</i> scaler reproduces the skew bug while you
believe you have rolled back. <b>A rollback plan that requires retraining is not a rollback
plan.</b></p>"""),
    ],
    """L1 is the one to run twice. A bug that only appears when your data drifts is a bug that
passes every pre-launch test.""")),

section("4", "&#128165;", "Break it, then repair it", "break", kind="debug",
    hook="Five, and every single one of them is silent.",
    body=breaks([
        ("def predict(model, X):\n    Xs, _, _ = standardise(X)        # recompute, ignore the stored mu/sd",
         "Standardise at serve time instead of using the stored statistics. Predict the error "
         "message.",
         """<p>There <b>is no error message</b>. That is the entire point. Accuracy drops
<b>0.8545 &rarr; 0.7530</b> and every probability still looks perfectly reasonable.</p>
<p>The weights were learned in a coordinate system defined by the training mu and sd; change
that system and the weights mean something else. Nothing about the shapes or the types is
wrong.</p>
<p>The invariant: <b>the scaling statistics are part of the model.</b> They live in
<code>CHAMP</code> next to w and b, and <code>sklearn</code> splits <code>fit</code> from
<code>transform</code> precisely to make the correct thing the easy thing.</p>"""),
        ("REG[fingerprint(model['w'])] = {...}      # weights only, no data or scaler hash",
         "Register only the weights, dropping the data and scaler hashes. When does that hurt?",
         """<p>Months later, when you need to answer &ldquo;<b>what produced this
decision?</b>&rdquo; and can identify the weights but not the data they came from or the
scaler they were paired with.</p>
<p>Two models with identical weights and different scalers behave completely differently
&mdash; that is the skew bug &mdash; so the weight hash alone does not identify the system that
made a decision.</p>
<p>The invariant: <b>hash everything that affects the output.</b> The registry is boring
until it is the only thing standing between you and a five-hour incident.</p>"""),
        ("if psi(ref, live) > 0.25: retrain()      # input drift as the trigger",
         "Trigger retraining on input drift alone. Predict what happens in the file's five "
         "months and in scenario B.",
         """<p>You would retrain in <b>month 3</b> (PSI 0.1310) and again in month 4 (0.3193),
for a model whose accuracy never fell &mdash; and by month 6 (PSI 1.6648) accuracy is
<b>0.8902</b>, four points higher than it started.</p>
<p>And in <b>scenario B</b>, where accuracy collapses to <b>0.5215</b>, PSI is <b>0.0037</b>
and the trigger <b>never fires at all</b>.</p>
<p>The invariant: <b>input drift is a hypothesis, not damage.</b> An alarm that fires on
healthy models and stays silent on broken ones is worse than no alarm, because people learn to
ignore it.</p>"""),
        ("ship_if(diff > 0)        # point estimate, no interval",
         "Ship whenever the canary's point estimate is positive. What does that let through?",
         """<p>At 40 users the estimate is <b>+0.1013</b> &mdash; positive, and more than three
times the truth. You would ship on it every time.</p>
<p>And you would ship an entirely <b>neutral</b> challenger just as readily, because a 40-user
sample produces a positive estimate about half the time by chance.</p>
<p>The invariant: <b>ship on the interval, not the estimate.</b> A CI that straddles zero means
your sample cannot answer the question &mdash; which is information, not a failure.</p>"""),
        ("del REG[old_hash]        # tidy up after promoting the challenger",
         "Delete the previous version once the new one is live. Predict the cost.",
         """<p>Nothing breaks until you need to roll back &mdash; and then <b>you cannot</b>.
The one-string rollback becomes a retraining job, at exactly the moment you are least able to
wait for one.</p>
<p>It also destroys your ability to answer &ldquo;what produced this decision?&rdquo; for every
decision the old model made, which may be a regulatory question rather than an engineering
one.</p>
<p>The invariant: <b>a rollback plan that requires retraining is not a rollback plan</b>
&mdash; and it only stays true while the old artefacts remain loadable.</p>"""),
    ],
    """Five breaks, five silent failures. That ratio is the honest one for production ML, and
it is why this file exists.""")),

section("5", "&#9878;&#65039;", "The invariant", "invariant", kind="invariant",
    hook="One transform, stored with the weights — and an old version you can still load.",
    body=invariant("""<p><b>Serving must apply exactly the transform training used, with the
same stored statistics &mdash; and every version must remain loadable.</b></p>""",
    """<p>The first is worth <b>10.2 accuracy points</b> in this file, silently. The weights and
the scaler are a matched pair: <code>CHAMP</code> stores <code>w</code>, <code>b</code>,
<code>mu</code> and <code>sd</code> together for that reason, and separating them is how the
skew bug is introduced.</p>
<p>The second is what makes <code>serve(version, X)</code> a one-string rollback. The file
demonstrates it directly: the challenger returns <b>[0, 0, 0, 0, 0]</b> on five requests and
the champion returns <b>[1, 0, 1, 0, 0]</b> on the same five, and switching between them is
changing one identifier.</p>
<p>Both only hold because the registry hashes the <b>data, the weights and the scaler</b>. A
version identified by weights alone cannot guarantee either.</p>""",
    """assert set(CHAMP) >= {"w", "b", "mu", "sd"}          # scaler travels with weights
Xs_serve, _, _ = standardise(X_live, CHAMP["mu"], CHAMP["sd"])
assert np.allclose(Xs_serve.mean(0), (X_live.mean(0) - CHAMP["mu"]) / CHAMP["sd"])
for h in REG:
    assert serve(h, X_live[:1]) is not None          # every version still loads""")),

section("6", "&#129535;", "Wrong mental models", "wrong", kind="myths",
    hook="Five, and every one of them is a decision someone makes on a Monday.",
    body=wrong([
        ("Scaling is preprocessing, so recompute it on whatever data you have.",
         """<p>It is <b>part of the model</b>. Recomputing at serve time costs <b>10.2 accuracy
points</b> here, silently.</p>
<p>The weights were learned in a coordinate system defined by the training mu and sd. Change
the system and the weights mean something else. This is why <code>CHAMP</code> stores the
scaler <b>with</b> the weights, and why <code>sklearn</code> separates <code>fit</code> from
<code>transform</code>.</p>"""),
        ("Input drift means the model is degrading.",
         """<p>PSI climbs by a factor of <b>400</b> across six months and accuracy <b>rises</b>
to 0.8902. In scenario A, PSI hits <b>2.4719</b> and accuracy reaches <b>0.9137</b> &mdash; a
loud alarm about a model that got <i>better</i>.</p>
<p>Drift is a <b>hypothesis</b>, and it is worth exactly as much as its false-alarm rate.
Retraining on it alone means retraining healthy models on a schedule set by noise.</p>"""),
        ("If the inputs have not changed, the model is fine.",
         """<p>Scenario B is the counterexample: income PSI <b>0.0037</b>, tenure PSI
<b>0.0079</b>, accuracy <b>0.5215</b>. The inputs are identical and the model is barely better
than a coin flip.</p>
<p>The <b>relationship</b> between features and outcome changed. That is <b>concept drift</b>,
no input monitor can see it, and only outcomes reveal it &mdash; which is why delayed labels
are a real problem rather than a nuisance.</p>"""),
        ("A small canary gives you a small amount of evidence.",
         """<p>It gives you a <b>wildly wrong number</b>. The 40-user canary reports
<b>+0.1013</b> for a true effect of <b>+0.0299</b> &mdash; more than three times over, with
total confidence in the point estimate.</p>
<p>The 200-user canary is almost exactly right (+0.0298) and its interval <b>still includes
zero</b>. Both are being asked a question their sample cannot answer, and &ldquo;keep
waiting&rdquo; is the correct reading.</p>"""),
        ("We could roll back if we had to.",
         """<p>&ldquo;Could&rdquo; and &ldquo;have, recently, and it took under a minute&rdquo;
are very different claims, and only the second is a plan.</p>
<p>Here rolling back is one string &mdash; but <b>only</b> because both versions are still
loadable and each carries its own scaling statistics. Load old weights with the new scaler and
you have reproduced the skew bug while believing you rolled back.</p>"""),
    ])),

section("7", "&#127959;&#65039;", "Reconstruction challenge", "reconstruct", kind="rebuild",
    hook="Rebuild the registry first — everything else depends on it.",
    body=reconstruct([
        ("Explain", "In four sentences, say what this file adds to a model that already works.",
         """<p>A record of exactly what produced each decision, so you can answer questions
about the past. A serving path that applies the same transform training used, with the same
numbers. Monitoring that distinguishes inputs moving from the model breaking. And the ability
to put the previous version back in one step.</p>"""),
        ("Skeleton", "Write the signatures, and say which one makes rollback possible.",
         """<p><code>standardise(X, mu=None, sd=None)</code>, <code>fit(X, y, epochs, lr)</code>,
<code>predict(model, X, mu=None, sd=None)</code>, <code>fingerprint(a)</code>,
<code>register(model, X, y, note)</code>, <code>psi(expected, actual, bins)</code>,
<code>bootstrap_diff(a_correct, b_correct, n_boot, seed)</code>, and
<code>serve(version, X)</code>.</p>
<p><b><code>serve(version, X)</code></b> is the one. It takes a <b>version identifier</b>
rather than a model object, which is what makes switching versions a one-string change.</p>"""),
        ("Core", "Write standardise and predict from memory, so that skew is impossible.",
         """<p><code>standardise(X, mu=None, sd=None)</code> computes mu and sd <b>only when
they are not supplied</b>, and returns them. <code>predict</code> takes the model dict and
uses <code>model['mu']</code> and <code>model['sd']</code> &mdash; never recomputing.</p>
<p>The design point: make the correct call the <b>default</b> and the dangerous one require
you to pass something extra. An API where the easy path is the wrong path will be used wrongly,
however clearly it is documented.</p>"""),
        ("Minimal", "Build the smallest experiment that shows a monitor firing on a healthy "
         "model and staying silent on a broken one.",
         """<p>Two runs on the same trained model: one where you shift the inputs and one where
you change the label rule while leaving inputs alone. Report PSI and accuracy for both.</p>
<p>You should get a large PSI with unchanged-or-better accuracy, and a near-zero PSI with
collapsed accuracy &mdash; the file's <b>2.4719 / 0.9137</b> and <b>0.0037 / 0.5215</b>.</p>"""),
        ("Verify", "Check your rebuild without comparing to the original.",
         """<p>Three assertions: predicting with stored mu/sd differs from predicting with
recomputed ones on shifted data (proving your serving path is doing the right thing rather
than accidentally the same thing); every registered version still loads and serves; and a
canary interval on a <b>neutral</b> challenger includes zero.</p>
<p>That last one is the real test of your evaluation: if a no-effect challenger comes back
significant, your interval is too narrow.</p>"""),
    ],
    """Build the registry first. The skew fix, the rollback and the ability to answer
&ldquo;what produced this?&rdquo; all depend on it, and it is the least interesting part to
write.""")),

section("8", "&#128279;", "Connections", "conn", kind="links",
    hook="The end of the lane — and where every earlier file's model would live.",
    body=connections(
        [("lab", "../scratch/02-logistic-regression.html", "Back to 02",
          "the model here is that logistic regression, unchanged"),
         ("lab", "../scratch/01-linear-regression.html", "Back to 01",
          "where the scaling statistics first appear &mdash; and are first easy to lose"),
         ("lab", "../scratch/09-collaborative-filtering.html", "Back to 09",
          "a recommender's own output becomes next quarter's training data")],
        [("lab", "../scratch/13-agent-loop.html", "Alongside 13",
          "the other file about operating a system rather than training one")],
        "../gist/c33.html", "C3 Week 3 &mdash; the gist",
        extra=[("docs", "../reference.html", "Reference &mdash; C2 W3",
                "<code>c2w3-leakage</code> covers the split failures this file's registry "
                "would catch")])),

section("9", "&#9670;", "Recall sheet", "recall", kind="recall",
    hook="Six cards, all numbers you would have to defend in a review.",
    body=recall([
        ("Recomputing the scaling statistics at serve time: what does it cost, and what error "
         "do you get?",
         "<b>10.2 accuracy points</b> (0.8545 &rarr; 0.7530), and <b>no error at all</b>. The "
         "weights were learned in a coordinate system defined by the training mu/sd; change it "
         "and the weights mean something else."),
        ("Income PSI climbs 0.0041 &rarr; 1.6648 over six months. What does accuracy do?",
         "It <b>never falls</b> &mdash; and ends at 0.8902, four points higher than it started. "
         "Conventional thresholds would have triggered retraining in month 3 for a model that "
         "was fine."),
        ("Scenario B: inputs identical, rule changed. Give the two numbers.",
         "PSI <b>0.0037</b>, accuracy <b>0.5215</b> &mdash; barely better than a coin flip, "
         "with every input monitor silent. That is <b>concept drift</b>, and only outcomes "
         "reveal it."),
        ("True effect +0.0299. What does a 40-user canary report?",
         "<b>+0.1013</b> &mdash; more than three times over, CI [+0.0000, +0.2250]. A tiny "
         "canary does not give a little evidence; it gives a wildly wrong number confidently."),
        ("The 200-user canary reports +0.0298, almost exactly right. Ship?",
         "<b>No</b> &mdash; its interval [&minus;0.0050, +0.0650] <b>straddles zero</b>. Being "
         "right by luck is not evidence. It takes <b>1,000 users</b> before the interval "
         "excludes zero."),
        ("Why is rolling back one string, and what would break that?",
         "Both versions are still <b>loadable</b> and each carries <b>its own scaling "
         "statistics</b>. Deleting old artefacts, or storing the scaler apart from the weights, "
         "turns rollback into a retraining job."),
    ],
    """Cover and answer aloud.""")),

section("10", "&#9989;", "Mastery check", "check", kind="check",
    hook="Five, and none of them is a modelling question.",
    body=check([
        ("""Your model's live accuracy is 10 points below its test accuracy and nothing has
errored. Name the first thing you check.""",
         """<p>Whether the serving path uses the <b>stored</b> mu and sd or recomputes them. In
this file that exact mistake costs <b>10.2 points</b> silently, which matches the symptom
almost exactly.</p>
<p>Check it before you look at the model, the data or the features &mdash; it is one line and
it is the most common cause of this shape of gap.</p>"""),
        ("""Your input-drift monitor has fired four times this quarter and each investigation
found nothing. What do you change?""",
         """<p>Stop treating drift as damage. In this file PSI climbs 400&times; while accuracy
<b>improves</b> &mdash; conventional thresholds would fire in month 3 for a healthy model.</p>
<p>Pair it with an <b>outcome</b> metric, and be explicit that drift is a hypothesis. An alarm
that fires on healthy models and is silent on broken ones (PSI 0.0037 at accuracy 0.5215)
teaches people to ignore it, which is worse than no alarm.</p>"""),
        ("""Labels arrive 90 days late. Name what you watch in the meantime and what it cannot
tell you.""",
         """<p>Watch the <b>approval rate</b> and the score distribution &mdash; available
instantly. What they cannot tell you is whether those decisions were <b>right</b>.</p>
<p>A perfectly stable approval rate is entirely consistent with a model that has stopped
working: it still <i>decides</i> the same way. Watch what you can see, and be honest that it is
a proxy.</p>"""),
        ("""Your canary shows +8% on 50 users after two hours. Your manager wants to ship. What
do you say?""",
         """<p>That the number is almost certainly wrong. A 40-user canary in this file reports
<b>+0.1013</b> for a true <b>+0.0299</b> &mdash; the same shape of over-reading.</p>
<p>Ask for the <b>confidence interval</b>. If it includes zero, the sample cannot answer the
question yet, and &ldquo;keep waiting&rdquo; is the correct reading rather than a delay. It
took 1,000 users here.</p>"""),
        ("""Someone proposes deleting old model versions to save storage. Give two costs.""",
         """<p><b>Rollback becomes retraining</b> &mdash; at exactly the moment you can least
afford to wait. The one-string switch only works while both versions are loadable.</p>
<p>And you lose the ability to answer <b>&ldquo;what produced this decision?&rdquo;</b> for
every decision the old model made, which is often a regulatory question rather than an
engineering one.</p>"""),
    ],
    """None of these is a modelling question, and that is the lesson of the file: <b>after the
model works, almost nothing that goes wrong is the model's fault.</b>""")),
    ],
)
