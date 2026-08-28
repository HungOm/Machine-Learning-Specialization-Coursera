# -*- coding: utf-8 -*-
"""C2 · Week 3 — Advice for applying machine learning."""
from kit import (kid, key, warn, trap, note, card, eq, eqp, decode, table, demo,
                 quiz, links, code, h2, grid2, grid3, pretest, explain, lenses)

SETUP = '<p class="tiny">The numbers on this page come from one reproducible experiment, used throughout the week: 60 points from <var>y</var> = 0.5<var>x</var>² − 2<var>x</var> + 3 plus Gaussian noise (σ = 1.5), split 36 train / 12 cross-validation / 12 test, fitted with polynomial features and ridge regression. The true function is a <b>quadratic</b> — remember that, because the sweep has to discover it.</p>'

L = []

# ============================================================ 1
L.append(dict(
    slug="01-deciding-what-to-try-next", title="Deciding what to try next", mins=8, tag="intuition",
    lede="The most valuable week of the course starts with an uncomfortable fact: most ML time is wasted "
         "on the wrong fix.",
    body=(
        pretest("""<p>Your model's predictions are bad. You could get more data, add features, remove features, change λ, or make the network bigger. <b>How would you decide which — without trying all five?</b></p>""",
        """<p>Watch for why guessing costs months. This whole chapter is about replacing the guess with a diagnosis.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Your bike won’t go. You could pump the tyres, oil the chain, tighten the brakes,
straighten the wheel, or buy a whole new bike. Each takes an afternoon.</p>
<p>A bad mechanic tries them in order until something works — five wasted afternoons.</p>
<p>A good mechanic <b>spins the wheel first and listens</b>. Ten seconds, and now they know it’s the
brake rubbing. That ten-second check is called a <b>diagnostic</b>, and this whole week is about the two
diagnostics that matter in machine learning.</p>""")

        + h2("😖", "The situation")
        + """<p>You built a regularised linear regression to predict house prices. It makes unacceptably
large errors on new data. Here is your menu:</p>"""
        + demo("whattotry", "Six things you could try — which half of the list is yours?",
               "each option fixes exactly one of the two problems")

        + h2("🔢", "Why guessing is so expensive")
        + table(["Option", "Typical cost", "Fixes"],
                [["Get more training examples", "weeks–months, sometimes money", "high variance only"],
                 ["Try a smaller set of features", "hours–days", "high variance only"],
                 ["Try getting additional features", "days–weeks", "high bias only"],
                 ["Try adding polynomial features", "hours", "high bias only"],
                 ["Try decreasing λ", "minutes", "high bias only"],
                 ["Try increasing λ", "minutes", "high variance only"]])
        + """<p>Notice the asymmetry: the most expensive item on the list — collecting more data — is
useless against high bias. Teams routinely spend a quarter collecting data for a model that was never
going to benefit from it.</p>"""
        + key("""<p>A diagnostic is a test you run to find out <b>what is actually wrong</b>, so you stop
choosing your next move by instinct. Diagnostics take time to implement, and they still pay for
themselves several times over.</p>""")

        + h2("🗺", "What this week gives you")
        + grid3(
            card("<h3>Lessons 2–9</h3><p>The bias/variance diagnostic. Two numbers tell you which half of "
                 "that list to look at.</p>"),
            card("<h3>Lessons 10–14</h3><p>The development loop, error analysis, and how to add data "
                 "cheaply when you do need more.</p>"),
            card("<h3>Lessons 15–17</h3><p>Fairness, and what to measure when 99% of your labels are the "
                 "same value.</p>"))

        + h2("🔤", "The words, decoded")
        + decode([
            ("diagnostic", "“a diagnostic”", "A test you run to find out <em>why</em> a model is bad, rather than guessing. This whole week is diagnostics."),
            ("bias", "“bias”, as in underfitting", "The model is too simple to fit even the training data. Nothing to do with fairness — different word, same spelling."),
            ("variance", "“variance”, as in overfitting", "The model fits the training data and not much else."),
            ("baseline", "“baseline”", "What a reasonable alternative achieves — usually a human. Without it, an error rate means nothing."),
        ])
        + h2("✅", "Check yourself")
        + quiz([
            ("Your model has 0.1% error on training data and 30% on new data. Is more data likely to help?",
             "<p><b>Yes</b> — that is the signature of high variance, and more data is a valid fix for it. "
             "(The next few lessons make this precise.)</p>"),
            ("Your model has 25% error on training data and 26% on new data. More data?",
             "<p><b>No.</b> It cannot even fit the data it already has. More of the same will not help. "
             "This is high bias.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("book", "https://info.deeplearning.ai/machine-learning-yearning-book",
             "Andrew Ng — Machine Learning Yearning",
             "Free. This week of the course, expanded into 100 short chapters. If you only read one ML book, read this one."),
            ("docs", "https://developers.google.com/machine-learning/guides/rules-of-ml",
             "Google — Rules of Machine Learning",
             "43 rules from production experience. Rules 1–15 are about exactly this problem."),
        ])
    )))

# ============================================================ 2
L.append(dict(
    slug="02-evaluating-a-model", title="Evaluating a model", mins=14, tag="core",
    lede="You cannot fix what you cannot measure. Split the data, and measure the error on the part the "
         "model has never seen.",
    body=(
        pretest("""<p>Your model scores brilliantly on the data it learned from. <b>Guess why that number is nearly worthless</b> — and what you would have to hold back to get an honest one.</p>""",
        """<p>Watch for the split, and for the one term that belongs in training but must never appear in the score you report.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Imagine studying for a test by memorising the answers to last year’s paper. Then you
mark yourself using last year’s paper. Amazing — 100%!</p>
<p>You have learned nothing about whether you can do <b>this</b> year’s paper.</p>
<p>So: hide some questions from yourself before you start studying. Study on the rest. Then mark yourself
on the hidden ones. That’s the train/test split, and it is the most important habit in all of applied
machine learning.</p>""")

        + h2("🔢", "The maths, decoded")
        + eqp([
            '<var>J</var><sub>train</sub> = ',
            ('<span class="frac"><span>1</span><span>2<var>m</var><sub>train</sub></span></span>', "avg-factor", "the average"),
            ('<span class="big">Σ</span> ( <var>f</var>(<var>x</var><sup>(<var>i</var>)</sup>) − <var>y</var><sup>(<var>i</var>)</sup> )<sup>2</sup>',
             "error-term", "predicted − actual, squared"),
        ], "error on the examples it learned from — hover or click a part", small=True)
        + eqp([
            '<var>J</var><sub>test</sub> = ',
            ('<span class="frac"><span>1</span><span>2<var>m</var><sub>test</sub></span></span>', "avg-factor", "the average"),
            ('<span class="big">Σ</span> ( <var>f</var>(<var>x</var><sup>(<var>i</var>)</sup>) − <var>y</var><sup>(<var>i</var>)</sup> )<sup>2</sup>',
             "error-term", "predicted − actual, squared"),
        ], "error on examples it has never seen — the honest one — hover or click a part", small=True)
        + decode([
            ("<var>J</var><sub>train</sub>", "“J train”", "How well it fits what it studied. Almost always optimistic."),
            ("<var>J</var><sub>test</sub>", "“J test”", "How well it does on fresh data. This is the number that matters."),
            ("70 / 30", "“the split”", "A common default. 80/20 is also fine. With millions of examples, 98/1/1 is normal — you only need enough test examples to measure precisely."),
            ("no λ term", "“regularisation is left out”", "λ‖w‖² is part of the <em>training objective</em>, not the evaluation. When you report error, you measure the mistakes only."),
        ])
        + warn("""<p>The regularisation term appears in the cost you minimise, but <b>not</b> in
J<sub>train</sub> or J<sub>test</sub> when you report them. It is a training aid, not part of the score.
The course is explicit about this and it is a common exam question.</p>""")

        + h2("🎬", "Watch it move")
        + demo("traintest", "Fit degree d, then measure on data it has never seen",
               "drag the degree up and watch the red test error diverge from the blue training error")

        + h2("🔠", "For classification, count mistakes instead")
        + eq("""<var>J</var><sub>test</sub> = <span class="frac"><span>number of misclassified test examples</span><span><var>m</var><sub>test</sub></span></span>""",
             "the fraction that is simply wrong", small=True)
        + """<p>You <em>can</em> report the cross-entropy loss on the test set, and sometimes should. But
“what fraction did it get wrong” is far easier to explain to a stakeholder, and for skewed data you will
want precision and recall instead — Lesson 16.</p>"""

        + h2("🧮", "One number is not enough — watch it fail")
        + """<p>Fit the same data twice, once with a degree-2 polynomial and once with degree 10, and
score both on the training set and on data neither has seen:</p>"""
        + table(["Model", "J<sub>train</sub>", "J<sub>test</sub>", "verdict"],
                [["degree 2", "0.665", "<b>0.909</b>", "close together — it generalises"],
                 ["degree 10", "<b>0.520</b>", "1.473", "far apart — it memorised"]])
        + """<p>Look only at the training column and degree 10 wins: 0.520 beats 0.665. It is the
better model by the only number you can compute without holding data back — and it is the worse
model. That gap is the entire reason this lesson exists.</p>""" + SETUP
        + explain("""<p>The degree-10 model’s training error is genuinely lower. <b>Why is that not
evidence that it fits the underlying pattern better?</b></p>""",
                  """<p>Because it has enough freedom to fit the <em>noise</em> as well as the
pattern, and noise is different in every sample. Extra parameters can only ever reduce training
error — a degree-10 curve can bend through points a degree-2 curve must miss — so J<sub>train</sub>
falls whether the extra bends are capturing something real or memorising this particular set of
random wobbles. Held-out data is the only place where the difference between those two shows
up.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Splitting after sorting.</b> If your data is ordered by price, date or class, the
first 70% and the last 30% are different populations. <b>Shuffle before splitting</b> — unless the data is
a time series, in which case you must split by time and never shuffle.</p>""")
        + trap("""<p><b>Leakage.</b> If the same house appears in both sets (duplicated rows, or two
photos of the same patient), your test score is fiction. De-duplicate by entity, not by row.</p>""")
        + trap("""<p><b>Scaling before splitting.</b> Computing the mean and standard deviation over the
whole dataset leaks test information into training. Fit the scaler on train only, then apply it to test.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("J_train = 0.02, J_test = 0.9. What is happening?",
             "<p>Severe <b>overfitting</b>. The model memorised the training set and learned nothing "
             "generalisable.</p>"),
            ("Why exclude the λ term when reporting J_test?",
             "<p>Because λ‖w‖² measures how big the weights are, not how wrong the predictions are. It "
             "belongs to the optimisation objective, not the evaluation.</p>"),
            ("You have 1,000,000 examples. Is a 70/30 split sensible?",
             "<p>Wasteful. 300,000 test examples measure the error far more precisely than you need. "
             "98/1/1 gives you 10,000 test examples — plenty — and 980,000 for training.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("docs", "https://scikit-learn.org/stable/modules/cross_validation.html",
             "scikit-learn — cross-validation and data splitting",
             "Including stratified splits (keep the class balance) and group splits (keep a patient in one set)."),
            ("docs", "https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets",
             "Google ML Crash Course — dividing datasets",
             "Short, with a good section on the ways a split can silently go wrong."),
            ("lab", "../../C2%20-%20Advanced%20Learning%20Algorithms/week3/C2W3A1/C2_W3_Assignment.ipynb",
             "Week 3 assignment",
             "In this repo. You will split data and plot exactly these curves."),
        ])
    )))

# ============================================================ 3
L.append(dict(
    slug="03-model-selection", title="Model selection and train / cross-validation / test", mins=20, tag="core",
    lede="Why two sets are not enough, and the discipline of keeping one set genuinely untouched until "
         "the very end.",
    body=(
        pretest("""<p>You try ten polynomial degrees and pick the one with the best test error. <b>Guess what is now wrong with that test error as an estimate of real performance.</b></p>""",
        """<p>Subtle and important. Watch for why choosing <em>using</em> a set spoils it, and for the third split that fixes it.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>You hid some questions to test yourself. Good. But then you tried <b>ten</b> different
study methods and picked whichever scored best on the hidden questions.</p>
<p>Now those hidden questions aren’t hidden any more — you used them to make a choice. Your score on them
is too flattering, because you picked the method that happened to suit them.</p>
<p>So hide <b>two</b> piles. Pile one picks the method. Pile two is opened once, at the end, and never
influences anything.</p>""")

        + h2("🔢", "The three sets")
        + table(["Set", "Typical size", "Used for", "How often you look"],
                [["<b>training</b>", "60%", "fitting w and b", "constantly"],
                 ["<b>cross-validation</b> (dev / validation)", "20%", "choosing the model: degree, λ, architecture, features", "every experiment"],
                 ["<b>test</b>", "20%", "one final honest estimate", "<b>once</b>"]])
        + decode([
            ("<var>J</var><sub>cv</sub>", "“J cee-vee”", "Error on the cross-validation set. Also written J<sub>dev</sub> or J<sub>val</sub> — three names for the same thing."),
            ("cross-validation", "“the dev set”", "Confusingly, this also names k-fold cross-validation, a different (related) technique. In this course it means the middle split."),
            ("model selection", "“choosing between candidates”", "Picking degree, λ, number of layers, feature set — any choice you make by looking at results."),
            ("generalisation error", "“the real error”", "How the model will do on genuinely new data. J<sub>test</sub> estimates it — but only if the test set stayed clean."),
        ])
        + key("""<p>Any number you use to <b>make a decision</b> becomes optimistically biased. That is why
the test set must be touched exactly once. The moment you say “hmm, let me try one more thing and check the
test set again”, you have converted your test set into a second cross-validation set.</p>""")

                + lenses(
            """<p>Hiring, with three stages: sift the CVs, interview a shortlist, then check references on the one
you want.</p>
<p>You do not use the interviews to also decide the reference check — that would be circular. Each
stage has one job, and the last one exists to give an honest answer about a decision already made.
Train, cross-validation and test are those three stages.</p>""",
            """<p>This is the multiple-comparisons problem wearing different clothes.</p>
<p>Try ten models against one held-out set and pick the best, and that best score is the maximum of ten
noisy draws — biased optimistically by construction. It is the same reason a p-value stops meaning
what you think it means after ten tests. The third split is the fix.</p>""",
            """<p>Three sealed envelopes.</p>
<p>You open the first as often as you like — that is the training set. You open the second to compare
your candidates. The third stays sealed until you have committed, and you open it exactly once. Open
it twice and it is no longer a test set; it is a second validation set.</p>""",
            """<p>This is the discipline behind every public ML leaderboard, and the reason serious competitions
keep a private test set nobody can query. Without it, teams optimise against the public score and the
winner is whoever overfitted the leaderboard hardest.</p>
<p>The same failure happens quietly inside companies whenever a team tunes for months against one
holdout and then reports that number to management as expected production performance.</p>""",
            """So the 60/20/20 split below is not a convention — each of the three has a distinct job that the
others cannot do.""")
        + h2("🎬", "Watch it move")
        + demo("splitcv", "Fit on train, choose on cross-validation, report on test",
               "each degree is fitted on TRAIN and scored on CV — the winner is only then measured on TEST")

        + h2("💻", "The procedure, in code")
        + code("""
from sklearn.model_selection import train_test_split

X_tr, X_, y_tr, y_ = train_test_split(X, y, test_size=0.40, random_state=1)
X_cv, X_te, y_cv, y_te = train_test_split(X_, y_, test_size=0.50, random_state=1)
#  -> 60% train, 20% cv, 20% test

best_d, best_j = None, float('inf')
for d in range(1, 11):
    model = fit_polynomial(X_tr, y_tr, degree=d)   # train ONLY on the training set
    j_cv = cost(model, X_cv, y_cv)                 # choose using cv
    if j_cv < best_j:
        best_d, best_j = d, j_cv

final = fit_polynomial(X_tr, y_tr, degree=best_d)
print('honest error:', cost(final, X_te, y_te))    # touch the test set ONCE
""")

        + h2("🧮", "The full sweep, measured")
        + """<p>Fit every degree from 1 to 10 and score each on train and on cross-validation:</p>"""
        + table(["degree", "J<sub>train</sub>", "J<sub>cv</sub>", ""],
                [["1", "3.876", "3.142", "underfitting — both high"],
                 ["<b>2</b>", "0.665", "<b>1.120</b>", "<b>lowest J<sub>cv</sub> — chosen</b>"],
                 ["3", "0.660", "1.149", ""],
                 ["4", "0.641", "1.223", ""],
                 ["5", "0.614", "1.475", "J<sub>cv</sub> now climbing"],
                 ["7", "0.601", "1.485", ""],
                 ["10", "<b>0.520</b>", "1.473", "best J<sub>train</sub>, and clearly overfitting"]])
        + """<p>Read the two columns against each other. <b>J<sub>train</sub> falls the whole way
down</b> — it never once gets worse, because more parameters can always fit the sample more closely.
<b>J<sub>cv</sub> makes a U</b>: down to degree 2, then up. The bottom of that U is the answer, and
the sweep found degree 2 — which is the degree the data was actually generated with.</p>
<p>Now the part that matters. Having <em>used</em> cross-validation to choose, its 1.120 is no longer
an honest estimate of future performance — it is the best of ten tries, and the best of ten tries is
optimistic. So you report the test set, untouched until this moment: <b>J<sub>test</sub> =
0.909</b>.</p>""" + SETUP
        + explain("""<p>You could have picked the degree with the lowest test error directly and
skipped cross-validation entirely. <b>What exactly would you have lost?</b></p>""",
                  """<p>The ability to say how good the model is. Choosing with a set turns that set’s
score into a best-of-ten, which is biased low for the same reason the highest of ten dice rolls
is not the expected roll. You would still get a reasonable degree — but you would have no untouched
data left, and no honest number to quote. The third split does not improve the model; it buys you
a trustworthy estimate of it.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Reporting J<sub>cv</sub> as your final number.</b> You optimised against it, so it
is biased low. The honest number is J<sub>test</sub>.</p>""")
        + trap("""<p><b>Peeking repeatedly.</b> Checking the test set after every experiment for “curiosity”
gradually leaks it. Kaggle competitions have public and private leaderboards for precisely this reason —
and people still overfit the public one.</p>""")
        + warn("""<p>With very little data (a few hundred rows), a single 20% cv split is noisy. That is when
you use <b>k-fold cross-validation</b>: split into k parts, train k times, average. Slower, much more
stable, and standard in scikit-learn.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("You try 100 architectures and report the best cross-validation error as your result. What is wrong?",
             "<p>With 100 tries, the best score is partly luck. Report the <b>test</b> error of the chosen "
             "model instead.</p>"),
            ("Why can J_cv be used for choosing λ but not for the final report?",
             "<p>Because choosing is what makes it biased. It is a fair comparison <em>between</em> "
             "candidates, and an unfair estimate <em>of</em> the winner.</p>"),
            ("Your test error is much worse than your cv error. What are the two likely causes?",
             "<p>(1) You over-selected on the cv set — too many candidates for too little cv data. "
             "(2) The splits are not from the same distribution (leakage, ordering, or drift).</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("docs", "https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html",
             "sklearn.model_selection.train_test_split",
             "Note <code>stratify=</code> — essential when classes are imbalanced."),
            ("docs", "https://scikit-learn.org/stable/modules/cross_validation.html#k-fold",
             "scikit-learn — k-fold cross-validation",
             "What to do when a single 20% split is too small to trust."),
            ("book", "https://hastie.su.domains/ElemStatLearn/",
             "Hastie, Tibshirani & Friedman — Elements of Statistical Learning, ch. 7",
             "Free PDF. The rigorous treatment of model assessment and selection."),
        ])
    )))

# ============================================================ 4
L.append(dict(
    slug="04-bias-and-variance", title="Diagnosing bias and variance", mins=20, tag="core",
    lede="The central diagnostic of the whole course. Two numbers, three possible verdicts, and a decision "
         "you no longer have to guess.",
    body=(
        pretest("""<p>Model A: 12% training error, 13% test. Model B: 0.5% training, 12% test. <b>Both are bad — but for opposite reasons. Name them.</b></p>""",
        """<p>Watch for the two labels, and for why the training error alone tells you which one you have.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Two ways to be a bad student.</p>
<p><b>Too simple (high bias):</b> you only ever learned “the answer is always 4”. You get last year’s paper
wrong <em>and</em> this year’s wrong. You’re not confused — you’re under-prepared.</p>
<p><b>Too clever (high variance):</b> you memorised last year’s paper word for word. Perfect on it,
hopeless on anything new. You didn’t learn the subject, you learned the paper.</p>
<p>You can tell which one you are by comparing two scores: how you do on what you studied, and how you do
on something fresh.</p>""")

        + h2("🔢", "The maths, decoded")
        + table(["Symptom", "J<sub>train</sub>", "J<sub>cv</sub>", "Verdict"],
                [["under-fitting", "<b>high</b>", "high (≈ J<sub>train</sub>)", "<b>high bias</b>"],
                 ["just right", "low", "low (≈ J<sub>train</sub>)", "good"],
                 ["over-fitting", "<b>low</b>", "<b>much higher</b>", "<b>high variance</b>"],
                 ["both at once", "high", "much higher still", "high bias <em>and</em> high variance"]])
        + decode([
            ("bias", "“under-fitting”", "The model is too simple to represent the pattern. It is wrong even on data it has seen. Named for a systematic, repeatable error."),
            ("variance", "“over-fitting”", "The model is so flexible it fits the noise. Re-train on a different sample and you get a wildly different model — hence “variance”."),
            ("J<sub>train</sub> high", "“can’t even fit what it saw”", "The tell-tale sign of bias. Nothing downstream will help until this is fixed."),
            ("J<sub>cv</sub> ≫ J<sub>train</sub>", "“the gap”", "The tell-tale sign of variance. The size of the gap is the size of the problem."),
        ])
        + key("""<p><b>J<sub>train</sub> tells you about bias. The gap between J<sub>train</sub> and
J<sub>cv</sub> tells you about variance.</b> One sentence, and it is most of the diagnostic value of this
entire week.</p>""")

                + lenses(
            """<p>Two apprentices failing at the same task, for opposite reasons.</p>
<p>One has not learned enough — he gets it wrong in the workshop and wrong on site, equally. The other
has learned the workshop <em>too</em> specifically: flawless on the bench he trained at, lost the
moment anything differs.</p>
<p>Both look like “bad apprentice”. Teaching them the same way would help one and harm the other,
which is exactly why naming the difference matters.</p>""",
            """<p>This is the bias–variance decomposition, and the diagnosis is mechanical: compare training error
to validation error, and compare training error to a baseline of what is achievable.</p>
<p>Two gaps, two diseases. Baseline-to-train is bias; train-to-validation is variance. Every remedy in
the table belongs to exactly one of those gaps, which is what turns an intuition into a procedure.</p>""",
            """<p>Two dartboards.</p>
<p>The first has a tight cluster in the wrong place — consistent and consistently wrong, high bias. The
second is scattered all over but averages to the bullseye — high variance. You fix a tight cluster by
aiming differently; you fix scatter by steadying the hand. Different problems, different actions.</p>""",
            """<p>This is the single most valuable week in the specialization for real work, because the wrong
diagnosis is expensive in a specific way: “get more data” is the costliest action available and it
does <b>nothing</b> for high bias.</p>
<p>Teams have spent months collecting data for models that were never data-limited. Two numbers, read
correctly, would have said so on day one.</p>""",
            """So the comparison below turns “the model is bad” into an instruction about what to do next.""")
        + h2("🎬", "Watch it move")
        + demo("biasvar", "Degree 1 to 10, with the diagnosis underneath",
               "left: the fit. right: J_train and J_cv against model complexity")
        + """<p>Watch the two curves on the right. J<sub>train</sub> falls forever — a more complex model
can always fit the training data better. J<sub>cv</sub> falls, bottoms out, then climbs. The bottom of the
J<sub>cv</sub> curve is the model you want, and it is nowhere near the bottom of the J<sub>train</sub>
curve.</p>"""

        + h2("🔬", "Why J_train can never tell you on its own")
        + """<p>Degree 10 has the lowest training error of any model on the demo. It is also the worst
model. If you selected by J<sub>train</sub> you would pick the most overfit candidate every single time —
which is precisely why the cross-validation set exists.</p>"""
        + note("""<p>The classical bias–variance <em>decomposition</em> splits expected test error into
bias² + variance + irreducible noise, and shows they genuinely trade off. Modern deep learning complicates
this — very large networks often improve past the point the classical curve says they should
(“double descent”). The practical diagnostic in this lesson still works; the tidy U-shaped story is
less universal than it looks.</p>""", "A note for the curious")

        + h2("🧮", "Both diseases, in one table")
        + """<p>Take three rows out of the degree sweep and read them as diagnoses:</p>"""
        + table(["", "J<sub>train</sub>", "J<sub>cv</sub>", "gap", "diagnosis"],
                [["degree 1", "3.876", "3.142", "≈ 0", "<b>high bias</b> — both bad, and equally bad"],
                 ["degree 2", "0.665", "1.120", "0.46", "healthy"],
                 ["degree 10", "0.520", "1.473", "<b>0.95</b>", "<b>high variance</b> — train fine, cv poor"]])
        + """<p>The signature of <b>high bias</b> is that the two numbers agree <em>and are both
high</em>. The model is not failing to generalise — it generalises its badness perfectly. Note that
J<sub>cv</sub> is even slightly <em>lower</em> than J<sub>train</sub> in that row, which surprises
people; with an underfitting model that is ordinary sampling noise, not a bug.</p>
<p>The signature of <b>high variance</b> is a wide gap with a low J<sub>train</sub>. Degree 10 fits
its own data better than degree 2 does, and does nearly a third worse on data it has not seen.</p>""" + SETUP
        + explain("""<p>Suppose someone reports J<sub>train</sub> = 0.52 and stops there.
<b>Why can that single number never distinguish these two diseases?</b></p>""",
                  """<p>Because it measures the model against the only data it was allowed to
optimise for, so it is a measure of <em>capacity</em>, not of correctness. A low J<sub>train</sub>
is consistent with a superb model and with pure memorisation, and a high one is consistent with
underfitting and with data that is simply noisy. The diagnosis lives entirely in the
<em>relationship</em> between two numbers — J<sub>train</sub> against J<sub>cv</sub> for variance,
and J<sub>train</sub> against a baseline for bias. One number carries no relationship, so it carries
no diagnosis.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Assuming it must be one or the other.</b> A model can have high bias and high
variance simultaneously — high J<sub>train</sub> <em>and</em> a big gap. It is rarer, and it means you have
two jobs, not one.</p>""")
        + trap("""<p><b>Calling 15% training error “high” without a reference.</b> High compared to what? If
humans score 14% on the same task, that is nearly perfect. Lesson 6 fixes this hole.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("J_train = 0.5%, J_cv = 12%. Diagnosis and first fix?",
             "<p><b>High variance.</b> Try: more data, more regularisation (larger λ), or fewer features.</p>"),
            ("J_train = 18%, J_cv = 19%. Diagnosis and first fix?",
             "<p><b>High bias.</b> Try: a bigger model, more features, polynomial features, or smaller λ. "
             "More data will not help.</p>"),
            ("J_train = 18%, J_cv = 32%. Diagnosis?",
             "<p><b>Both.</b> High J_train means bias; the 14-point gap means variance. Fix the bias first — "
             "a bigger model — then re-diagnose.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("docs", "https://scikit-learn.org/stable/auto_examples/model_selection/plot_underfitting_overfitting.html",
             "scikit-learn — underfitting vs overfitting, plotted",
             "Runnable code that draws the picture in the demo above."),
            ("paper", "https://www.pnas.org/doi/10.1073/pnas.1903070116",
             "Belkin et al. (2019) — Reconciling modern ML practice and the bias–variance trade-off",
             "The double-descent paper. Where the classical U-curve stops being the whole story."),
            ("video", "https://www.youtube.com/watch?v=EuBBz3bI-aA",
             "StatQuest — Bias and Variance",
             "Eight cheerful minutes. A good second telling if the terms still feel slippery."),
        ])
    )))

# ============================================================ 5
L.append(dict(
    slug="05-regularization-bias-variance", title="Regularization and bias/variance", mins=14, tag="core",
    lede="λ is the same dial as model complexity, turned the other way. Choose it exactly the way you "
         "chose the degree.",
    body=(
        pretest("""<p>λ = 0 and λ = enormous both give a bad model. <b>Guess which extreme gives which failure mode.</b></p>""",
        """<p>Watch for the U-shaped curve of cross-validation error against λ, and where the useful values live.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>λ is a stiffness dial on the model.</p>
<ul><li><b>λ = 0</b> — completely floppy. It will bend to touch every single training point, including
the wrong ones. Overfitting.</li>
<li><b>λ enormous</b> — rigid as a plank. It can barely bend at all, so it misses the real pattern too.
Underfitting.</li></ul>
<p>Somewhere in between is a model flexible enough to follow the trend and stiff enough to ignore the
noise. You find it by trying a ladder of values and keeping the one with the best cross-validation
score.</p>""")

        + h2("🔢", "The maths, decoded")
        + eqp([
            ("<var>J</var>(<var>w</var>,<var>b</var>)", "cost-j", "the cost"),
            ' = ',
            ('<span class="frac"><span>1</span><span>2<var>m</var></span></span>', "avg-factor", "the average"),
            ('<span class="big">Σ</span>(<var>f</var>(<var>x</var>) − <var>y</var>)<sup>2</sup>', "error-term", "predicted − actual, squared"),
            ' <span class="op">+</span> ',
            ('<span class="frac"><span><var class="hl-a">λ</var></span><span>2<var>m</var></span></span> <span class="big">Σ</span><var>w</var><sub><var>j</var></sub><sup>2</sup>',
             "reg-penalty", "the penalty term — keeps weights small"),
        ], "fit the data … and keep the weights small — hover or click a part")
        + decode([
            ("<var class='hl-a'>λ</var>", "“lambda”", "The regularisation strength. How much you care about small weights relative to fitting the data."),
            ("Σ<var>w</var><sub>j</sub>²", "“the size of the weights”", "Large weights = a wiggly, extreme function. Penalising them keeps the model smooth."),
            ("λ → 0", "“no penalty”", "Pure data fitting. Maximum flexibility → high variance."),
            ("λ → ∞", "“crush the weights”", "All w → 0, so f(x) → b, a flat line. Maximum stiffness → high bias."),
            ("b is not penalised", "“the bias term is exempt”", "Shrinking the intercept does not reduce wiggliness, only shifts the whole function. Conventionally left out."),
        ])
        + warn("""<p>Confusing vocabulary alert: the <b>bias term b</b> (the constant in w·x + b) and
<b>bias</b> as in underfitting are unrelated. English is doing two jobs with one word.</p>""")

        + h2("🎬", "Watch it move")
        + demo("lambdacurve", "The same picture as degree, mirrored",
               "λ from 0 to 100 on a degree-10 model — watch the curve stiffen")
        + """<p>Compare with the degree demo in Lesson 4. The J<sub>cv</sub> curve has the same U shape,
just flipped: small λ sits where high degree sat. The two dials do the same job from opposite directions.</p>"""

        + h2("💻", "How to pick λ")
        + code("""
lambdas = [0, 0.01, 0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 1.28, 2.56, 5.12, 10.24]

best = None
for lam in lambdas:
    model = train(X_train, y_train, lam)     # fit with this lambda
    j_cv  = cost(model, X_cv, y_cv)          # score on cross-validation
    if best is None or j_cv < best[1]:
        best = (lam, j_cv)

print('chosen lambda:', best[0])
# then report cost(retrained_model, X_test, y_test)
""")
        + """<p>The doubling ladder (0, 0.01, 0.02, 0.04, …) is Andrew’s suggestion and a good one: λ acts
multiplicatively, so equal <em>ratios</em> matter, not equal differences. Searching 0.1, 0.2, 0.3 wastes
almost all your tries in one narrow region.</p>"""

        + h2("🧮", "The λ sweep, measured")
        + """<p>Keep the degree fixed at 10 — deliberately far too flexible — and vary λ instead:</p>"""
        + table(["λ", "J<sub>train</sub>", "J<sub>cv</sub>", ""],
                [["0", "0.520", "1.473", "no regularisation — high variance"],
                 ["0.001", "0.595", "1.410", ""],
                 ["0.01", "0.625", "1.327", ""],
                 ["<b>0.1</b>", "0.650", "<b>1.230</b>", "<b>lowest J<sub>cv</sub> — chosen</b>"],
                 ["1", "0.762", "1.349", "starting to over-constrain"],
                 ["10", "1.477", "2.014", "high bias"],
                 ["100", "2.398", "2.634", "badly underfitting"]])
        + """<p>Compare this against the degree sweep and note that it is the <b>mirror image</b>. There,
J<sub>train</sub> fell as complexity rose. Here, J<sub>train</sub> <em>rises</em> the whole way down,
because λ is a penalty on fitting. Both times J<sub>cv</sub> makes a U and you take its bottom.</p>
<p>Worth seeing: a degree-10 model with λ = 0.1 reaches J<sub>cv</sub> = 1.230, close to the
degree-2 model’s 1.120 — the regularisation recovers most of what the excess flexibility cost.
That is why the neural-network recipe is “build it too big, then regularise” rather than “agonise
over the size”.</p>""" + SETUP
        + explain("""<p>Raising λ makes J<sub>train</sub> worse at every single step. <b>Why is
choosing a model with deliberately worse training error not self-defeating?</b></p>""",
                  """<p>Because J<sub>train</sub> is not the goal — it is the thing being sacrificed.
The λ term adds a cost for large weights, so the fit stops chasing the last few points and settles
for a smoother curve. Smoother means the model changes less when the sample changes, which is
precisely what lowers J<sub>cv</sub>. You are trading a quantity you do not care about for one you
do, and the U-shape shows exactly where that trade turns bad.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Tuning λ on the test set.</b> λ is a model choice like any other — it belongs to the
cross-validation set.</p>""")
        + trap("""<p><b>Regularising unscaled features.</b> λ penalises all weights equally, so a feature
measured in millions gets a tiny weight and is effectively exempt. <b>Always standardise features before
regularising.</b></p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("λ is very large. What does the model look like and which problem do you have?",
             "<p>All weights ≈ 0, so f(x) ≈ b — a horizontal line. Extreme <b>high bias</b>.</p>"),
            ("J_train = 0.01, J_cv = 0.40. Increase or decrease λ?",
             "<p><b>Increase</b> it. That gap is high variance, and more stiffness is one of the fixes.</p>"),
            ("Why is the λ curve a mirror image of the degree curve?",
             "<p>Because both control effective model complexity. High degree and low λ both mean “very "
             "flexible”; low degree and high λ both mean “very stiff”.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("docs", "https://scikit-learn.org/stable/modules/linear_model.html#ridge-regression",
             "scikit-learn — Ridge regression",
             "This exact penalty, with <code>RidgeCV</code> to select α (their name for λ) automatically."),
            ("paper", "https://jmlr.org/papers/v15/srivastava14a.html",
             "Srivastava et al. (2014) — Dropout",
             "A different way to regularise neural networks: randomly switch units off during training. Now standard."),
            ("lab", "../../C2%20-%20Advanced%20Learning%20Algorithms/week3/C2W3A1/C2_W3_Assignment.ipynb",
             "Week 3 assignment",
             "You sweep λ and plot exactly this curve."),
        ])
    )))

# ============================================================ 6
L.append(dict(
    slug="06-baseline-performance", title="Establishing a baseline level of performance", mins=9, tag="core",
    lede="“High” compared to what? Without a reference point, J_train is a number with no meaning.",
    body=(
        pretest("""<p>Your speech recogniser has 10.6% error. <b>Is that good?</b> Commit to yes or no before reading.</p>""",
        """<p>You cannot answer it yet — and that is the point. Watch for what you must compare against before 10.6% means anything.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>You got 89% on a test. Is that good?</p>
<p>You can’t possibly know yet. If everyone else got 98%, it’s bad. If the class average was 45%, it’s
brilliant. If the test contains three questions that are literally unanswerable, then 89% might be a
perfect score.</p>
<p>Same with models. 10.8% error sounds awful — until you learn that humans listening to the same crackly
audio get 10.6% wrong.</p>""")

        + h2("🎬", "Watch it move")
        + demo("baseline", "Three scenarios, identical-looking numbers",
               "click through: the same J_train means different things against different baselines")

        + h2("🔢", "The two gaps")
        + table(["Gap", "Measures", "Name"],
                [["baseline → J<sub>train</sub>", "how much worse than achievable you are on data you have seen", "<b>avoidable bias</b>"],
                 ["J<sub>train</sub> → J<sub>cv</sub>", "how much you lose on unseen data", "<b>variance</b>"]])
        + decode([
            ("baseline", "“what is achievable”", "The error rate you could reasonably hope for. Usually human performance, a competing system, or a previous version of your model."),
            ("avoidable bias", "“the part worth chasing”", "Only the gap to the baseline is worth attacking. Error below the baseline may simply be noise in the data."),
            ("Bayes error", "“the irreducible floor”", "The best any model could possibly do, given the information in the inputs. Unknowable exactly; human performance is a decent proxy for perception tasks."),
        ])
        + key("""<p>Compare J<sub>train</sub> against the <b>baseline</b>, not against zero. Chasing an
error rate below the noise floor of your own labels is a way to spend a year overfitting.</p>""")

        + h2("🔬", "Where to get a baseline")
        + grid3(
            card("<h3>Human performance</h3><p>Best for perception: vision, speech, reading. Have three "
                 "people label 100 examples and measure their disagreement.</p>"),
            card("<h3>A competing system</h3><p>The existing production model, an off-the-shelf API, or a "
                 "published result on the same benchmark.</p>"),
            card("<h3>Guessing well</h3><p>Always predict the most common class. Depressingly hard to beat "
                 "on skewed data — and a real check on whether ML is helping at all.</p>"))
        + warn("""<p>Human-level performance is a good baseline for tasks humans are good at. It is
<b>not</b> a sensible target for predicting stock prices, click-through rates or hardware failures — tasks
where humans are terrible and the irreducible noise is high. There, use a previous system or a simple
statistical model.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Assuming Bayes error is 0.</b> Some examples are genuinely ambiguous: audio nobody
can transcribe, an X-ray two radiologists disagree about. Insisting on 0% error means fitting label noise.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("Baseline 8%, J_train 8.2%, J_cv 15%. Diagnosis?",
             "<p>Avoidable bias 0.2% — essentially none. Variance 6.8% — the problem. <b>High variance.</b></p>"),
            ("Baseline 8%, J_train 15%, J_cv 15.5%. Diagnosis?",
             "<p>Avoidable bias 7% — large. Variance 0.5% — none. <b>High bias.</b></p>"),
            ("Your model scores 2% error; humans score 5%. Is something wrong?",
             "<p>Not necessarily — models beat humans on plenty of tasks. But check for leakage first: "
             "beating the baseline by a lot is more often a bug than a breakthrough.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("book", "https://info.deeplearning.ai/machine-learning-yearning-book",
             "Machine Learning Yearning — chapters on human-level performance",
             "Andrew’s longer treatment, including when human-level is the wrong target."),
            ("paper", "https://arxiv.org/abs/1706.06969",
             "Comparing deep neural networks against humans",
             "Careful measurement of human error rates on image tasks — a good illustration of how hard baselining is."),
        ])
    )))

# ============================================================ 7
L.append(dict(
    slug="07-learning-curves", title="Learning curves", mins=16, tag="core",
    lede="Plot error against training-set size and you get the definitive answer to the most expensive "
         "question in ML: will more data help?",
    body=(
        pretest("""<p>You plot error against training-set size. <b>Guess what the two curves do as data grows</b>, and whether they meet.</p>""",
        """<p>Watch for the gap between them, and for the case where adding data provably cannot help.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Fitting three points perfectly is easy. Fitting a thousand points perfectly is
impossible. So as you add examples, your score on the stuff you studied gets <b>worse</b>, and your score
on new stuff gets <b>better</b>. The two lines move towards each other.</p>
<p>Now: if they have already met and gone flat, adding more data changes nothing. Buying more books won’t
help someone who has stopped being able to learn from books. You need a different student.</p>""")

        + h2("🎬", "Watch it move")
        + demo("learncurve", "Error against training-set size",
               "toggle between the high-bias and high-variance shapes — they look completely different")

        + h2("🔢", "Reading the two shapes")
        + grid2(
            card("<h3>High bias</h3><ul>"
                 "<li>Both curves <b>flatten</b> early.</li>"
                 "<li>They flatten <b>well above</b> the baseline.</li>"
                 "<li>The gap between them is small.</li></ul>"
                 "<p><b>More data will not help.</b> The flat line is the model’s ceiling, and you are "
                 "already at it.</p>"),
            card("<h3>High variance</h3><ul>"
                 "<li>J<sub>train</sub> is <b>below</b> the baseline (a bad sign, not a good one).</li>"
                 "<li>A <b>large gap</b> to J<sub>cv</sub>.</li>"
                 "<li>J<sub>cv</sub> is still falling at the right-hand edge.</li></ul>"
                 "<p><b>More data will help</b>, and you can read roughly how much off the curve.</p>"))
        + decode([
            ("J<sub>train</sub> rising", "“harder to fit more”", "Not a bug. Fitting 1000 points is genuinely harder than fitting 3, so training error grows with m."),
            ("J<sub>cv</sub> falling", "“generalising better”", "More examples means less chance of memorising, so unseen-data error falls."),
            ("the gap", "“the variance”", "It closes as m grows — that is exactly why data fixes variance."),
            ("flat curves", "“a ceiling”", "Both curves plateau at the model’s intrinsic limit. Only a better model raises it."),
        ])
        + key("""<p>J<sub>train</sub> ending up <em>below</em> human-level performance is not something to
celebrate. It usually means the model is fitting noise that humans correctly ignore.</p>""")

        + h2("💻", "Plotting one yourself")
        + code("""
sizes = [50, 100, 200, 400, 800, 1600, 3200]
train_errs, cv_errs = [], []

for m in sizes:
    model = train(X_train[:m], y_train[:m])        # train on a SUBSET
    train_errs.append(cost(model, X_train[:m], y_train[:m]))
    cv_errs.append(cost(model, X_cv, y_cv))        # always the FULL cv set

plt.plot(sizes, train_errs, label='J_train')
plt.plot(sizes, cv_errs,    label='J_cv')
""")
        + warn("""<p>Two details that matter. The cross-validation set stays the <b>same size</b> throughout
— only the training subset grows. And with small m the curve is noisy, so average over several random
subsets if you can afford the compute.</p>""")

        + h2("🧮", "Two learning curves, measured")
        + """<p>Refit each model on the first 5, 10, 20 and 36 training points, scoring on the same
cross-validation set every time:</p>"""
        + table(["m", "degree 1 · J<sub>train</sub>", "degree 1 · J<sub>cv</sub>",
                 "degree 4 · J<sub>train</sub>", "degree 4 · J<sub>cv</sub>"],
                [["5", "7.098", "4.101", "<b>0.000</b>", "4.150"],
                 ["10", "4.774", "3.644", "0.398", "1.690"],
                 ["20", "2.993", "3.758", "0.569", "1.260"],
                 ["36", "3.876", "3.142", "0.641", "1.223"]])
        + """<p>Two completely different stories.</p>
<p><b>Degree 1 (high bias).</b> The curves come together and then both flatten around 3–4. Going
from 20 points to 36 moved J<sub>cv</sub> from 3.758 to 3.142. Doubling again would move it about as
little. <b>More data will not help</b>, and this table is how you know before you spend a month
collecting it.</p>
<p><b>Degree 4 (high variance).</b> J<sub>train</sub> starts at <b>0.000</b> — five points, and a
degree-4 curve passes through all of them exactly, which is memorisation with nothing left over.
J<sub>cv</sub> at that moment is 4.150, worse than the underfitting model. Then watch the gap close:
4.15 → 1.69 → 1.26 → 1.22 as data arrives. <b>More data is working</b>, though the returns are
already flattening by 36.</p>""" + SETUP
        + explain("""<p>At m = 5 the degree-4 model has a perfect training score and the
<em>worst</em> cross-validation score on the table. <b>Why do those two facts arrive
together?</b></p>""",
                  """<p>Because they are the same fact. Five points and five free coefficients means
the curve is fully determined — it must pass through every point, so the training error is zero by
construction and carries no information about whether the fit is sensible. Whatever it does between
and beyond those points is unconstrained, so it swings wildly, and the cross-validation set lands in
exactly that unconstrained territory. A training error of zero is not a strong result; it is a sign
that the data ran out before the parameters did.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Being surprised that J<sub>train</sub> goes up.</b> Everyone is, once. It is
correct and expected.</p>""")
        + trap("""<p><b>Extrapolating a flat curve optimistically.</b> If J<sub>cv</sub> has been flat for
the last three doublings of m, a fourth doubling will not rescue you. Learning curves are the cheapest way
to say no to a data-collection project.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("Both curves flat at 26% error, human level 3%. Should you collect more data?",
             "<p><b>No.</b> Classic high bias. Spend the money on a bigger model or better features "
             "instead.</p>"),
            ("J_train 1%, J_cv 15%, and J_cv is still falling steeply. More data?",
             "<p><b>Yes.</b> High variance, and the curve says the gap is still closing.</p>"),
            ("Why must the cv set stay the same size while the training subset grows?",
             "<p>So that J_cv values are comparable across the x-axis. Changing both at once confounds "
             "the measurement.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("docs", "https://scikit-learn.org/stable/modules/learning_curve.html",
             "scikit-learn — learning curves",
             "<code>learning_curve()</code> does the subsetting and averaging for you, with error bands."),
            ("paper", "https://arxiv.org/abs/1712.00409",
             "Hestness et al. (2017) — Deep Learning Scaling is Predictable, Empirically",
             "Learning curves measured over orders of magnitude of data. Remarkably regular power laws."),
        ])
    )))

# ============================================================ 8
L.append(dict(
    slug="08-what-to-try-revisited", title="Deciding what to try next, revisited", mins=12, tag="core",
    lede="Back to the six options from Lesson 1 — but now you know which half of the list to read.",
    body=(
        pretest("""<p>You now know whether you have high bias or high variance. <b>Sort these into two piles: more data, more features, fewer features, bigger network, larger λ, smaller λ.</b></p>""",
        """<p>Watch for how cleanly the six split. Getting the diagnosis right makes the fix obvious.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Remember the bike that wouldn’t go? You’ve now learned to spin the wheel and listen.
Here is the repair table that tells you what to do with what you heard.</p>""")

        + h2("🎬", "Watch it move")
        + demo("fixtable", "Symptom on the left, fix on the right",
               "the same six options from Lesson 1, now sorted")

        + h2("🔢", "The table to memorise")
        + table(["If you have…", "…try", "Because"],
                [["<b>high variance</b>", "get more training examples", "more data makes memorising harder"],
                 ["<b>high variance</b>", "try a smaller set of features", "fewer knobs to overfit with"],
                 ["<b>high variance</b>", "try increasing λ", "stiffer model, less wiggle"],
                 ["<b>high bias</b>", "try getting additional features", "give it more information to work with"],
                 ["<b>high bias</b>", "try adding polynomial features", "let it bend"],
                 ["<b>high bias</b>", "try decreasing λ", "loosen the stiffness"]])
        + key("""<p>Every high-variance fix makes the model <b>less</b> flexible. Every high-bias fix makes
it <b>more</b> flexible. That is the entire logic of the table, and you can regenerate it from that
sentence alone if you forget it.</p>""")

        + h2("🔬", "The order to do things in")
        + """<ol>
<li><b>Fix bias first.</b> If the model cannot fit the training set, nothing else matters. Make it bigger
until J<sub>train</sub> is close to the baseline.</li>
<li><b>Then fix variance.</b> Now add regularisation, or data, until J<sub>cv</sub> catches up.</li>
<li><b>Re-diagnose after every change.</b> Fixing bias often creates variance — that is expected, and it
means you are making progress, not going backwards.</li>
</ol>"""

        + h2("🧮", "The table, applied to three real cases")
        + """<p>The fix table is only useful if you can pick the row. Here are three measured
situations from this week’s experiment, and what each one actually calls for:</p>"""
        + table(["Measured", "Diagnosis", "Do this", "Do NOT do this"],
                [["J<sub>train</sub> 3.876, J<sub>cv</sub> 3.142",
                  "high bias",
                  "add features / raise the degree / lower λ",
                  "collect more data — the curve says it is already flat"],
                 ["J<sub>train</sub> 0.520, J<sub>cv</sub> 1.473",
                  "high variance",
                  "raise λ (0.1 took J<sub>cv</sub> to 1.230), or get more data",
                  "add more features — that widens the gap"],
                 ["J<sub>train</sub> 0.665, J<sub>cv</sub> 1.120",
                  "healthy",
                  "report J<sub>test</sub> and stop",
                  "keep tuning against the cv set — you will start fitting it"]])
        + """<p>Every row of the fix table sits on one side or the other, and half of them are
actively wrong for any given problem. Getting more data is the most expensive action available and
it is useless in row 1. That single distinction is what the week buys you.</p>""" + SETUP
        + explain("""<p>Row 2 offers two fixes — more regularisation or more data — and the learning
curve says both work. <b>How would you choose between them in practice?</b></p>""",
                  """<p>By cost, because the diagnosis has already told you both are on the right
side. Raising λ is a one-line change and a re-fit measured in seconds, so you try it first and read
the U-shape. More data is weeks of work, so you spend it only when the λ sweep has been done and the
learning curve shows J<sub>cv</sub> still falling at your current m. The order is not arbitrary:
cheap interventions also tell you <em>how much</em> the expensive one might buy.</p>""")

        + h2("🔤", "The words, decoded")
        + decode([
            ("high bias", "“underfitting”", "J_train is high, and J_cv is about the same. More data will not help."),
            ("high variance", "“overfitting”", "J_train is low and J_cv is much higher. More data probably will help."),
            ("regularisation parameter", "“lambda”", "Raise it to fight variance, lower it to fight bias. The two directions are opposite."),
            ("cross-validation set", "“the dev set”", "The split you tune against. Also called the validation set, or dev set — three names, one thing."),
        ])
        + h2("🕳", "Traps")
        + trap("""<p><b>Collecting data to fix high bias.</b> The single most expensive mistake in this
week. It is on the variance list <em>only</em>.</p>""")
        + trap("""<p><b>Changing two things at once.</b> If you add features and change λ together and the
score improves, you have learned nothing about which one helped.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("You increase λ and J_train goes up while J_cv goes down. Good or bad?",
             "<p><b>Good</b> — you traded a little bias for a lot less variance, and the number that "
             "matters (J_cv) improved.</p>"),
            ("You add 50 features and J_cv gets worse. What happened?",
             "<p>You fixed a bias problem you did not have and created a variance problem you did not "
             "need. Diagnose first.</p>"),
            ("Why fix bias before variance?",
             "<p>Because variance fixes (more data, more λ) all make the model less flexible — the "
             "opposite of what a high-bias model needs. You would be pulling in two directions.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("book", "https://info.deeplearning.ai/machine-learning-yearning-book",
             "Machine Learning Yearning — “Basic Error Analysis”",
             "The chapters on prioritising work. Short, and directly applicable."),
            ("docs", "https://developers.google.com/machine-learning/guides/rules-of-ml#ml_phase_ii_feature_engineering",
             "Google — Rules of ML, phase II",
             "What experienced teams actually do between “it works” and “it works well”."),
        ])
    )))

# ============================================================ 9
L.append(dict(
    slug="09-bias-variance-neural-networks", title="Bias / variance and neural networks", mins=10, tag="core",
    lede="The classical trade-off says you must choose. Large neural networks plus regularisation mostly "
         "let you refuse to.",
    body=(
        pretest("""<p>Classically, bigger models overfit. <b>Guess why modern practice often says “make it bigger” anyway.</b></p>""",
        """<p>Watch for the recipe, and for what regularisation lets you get away with.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>The old rule said: a simple model underfits, a complex model overfits, so hunt for the
perfect middle size. A tightrope.</p>
<p>Big neural networks changed the game. If your model is too simple — make it bigger. If it starts
memorising — don’t shrink it, just turn up the stiffness dial (λ) and get more data. A big, well-regularised
network is almost never worse than a small one.</p>
<p>The catch: “bigger” costs money and time, and “more data” isn’t always possible. The tightrope became a
budget question rather than a modelling question.</p>""")

        + h2("🎬", "Watch it move")
        + demo("nnrecipe", "The recipe, as a flowchart",
               "two questions, two fixes, and a loop")

        + h2("🔢", "The recipe in words")
        + """<ol>
<li>Train the model. Ask: <b>does it do well on the training set?</b> (compare J<sub>train</sub> to your
baseline)</li>
<li>If no → <b>bigger network</b>. More layers, more units. Go back to step 1.</li>
<li>If yes → ask: <b>does it do well on the cross-validation set?</b></li>
<li>If no → <b>more data</b> (or more regularisation). Go back to step 1.</li>
<li>If yes → <b>done</b>.</li>
</ol>"""
        + key("""<p>A larger neural network with appropriate regularisation will usually do <b>at least as
well as</b> a smaller one. So “too big” is a compute-cost problem, not an accuracy problem. That single
observation is why the field moved towards scale.</p>""")

        + h2("💻", "Regularising a neural network")
        + code("""
from tensorflow.keras.regularizers import l2

model = Sequential([
    Dense(25, activation='relu', kernel_regularizer=l2(0.01)),
    Dense(15, activation='relu', kernel_regularizer=l2(0.01)),
    Dense(1,  activation='sigmoid', kernel_regularizer=l2(0.01)),
])
""")
        + """<p><code>l2(0.01)</code> is λ = 0.01 applied to that layer’s weights. You can use a different
λ per layer; in practice one value everywhere is a fine starting point. <b>Dropout</b> and <b>early
stopping</b> are two other common regularisers you will meet later — dropout randomly switches units off
during training, early stopping just stops when J<sub>cv</sub> starts rising.</p>"""

        + h2("🔤", "The words, decoded")
        + decode([
            ("capacity", "“how flexible it is”", "How complicated a function the model can represent. Set by layers and units."),
            ("bias-variance tradeoff", "“the see-saw”", "The classical idea that reducing one raises the other. Large regularised networks largely break it."),
            ("kernel_regularizer", "“weight penalty”", "The Keras argument that adds λΣw² to the loss for that layer."),
            ("L2 regularisation", "“L-two”", "Penalising the sum of squared weights. The same λ term you met in Course 1."),
        ])
        + h2("🕳", "Traps")
        + trap("""<p><b>Making the network bigger without regularising.</b> Then you really will overfit.
The claim is “bigger <em>with</em> appropriate regularisation”, and the second half is doing work.</p>""")
        + trap("""<p><b>Ignoring the compute bill.</b> Doubling width roughly quadruples the multiply
count in that layer. Sometimes the honest answer is “a smaller model that we can actually afford to
serve”.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("Your network gets 20% training error against a 5% baseline. First move?",
             "<p><b>Bigger network.</b> That is high bias — more data or more λ would both make it worse.</p>"),
            ("Now J_train is 4% and J_cv is 16%. Next move?",
             "<p>High variance: <b>more data</b>, or increase λ, or add dropout. Do not shrink the "
             "network unless compute forces you to.</p>"),
            ("Why doesn't a bigger network automatically overfit?",
             "<p>Because regularisation constrains the <em>effective</em> capacity, not the parameter "
             "count. And empirically, large networks trained with gradient descent tend to find "
             "surprisingly generalisable solutions — an active research area.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("docs", "https://www.tensorflow.org/api_docs/python/tf/keras/regularizers/L2",
             "tf.keras.regularizers.L2",
             "The <code>kernel_regularizer</code> argument, documented."),
            ("paper", "https://arxiv.org/abs/1611.03530",
             "Zhang et al. (2016) — Understanding deep learning requires rethinking generalization",
             "Big networks can memorise pure random labels — and yet generalise on real ones. The paper that broke the classical story."),
            ("paper", "https://jmlr.org/papers/v15/srivastava14a.html",
             "Srivastava et al. (2014) — Dropout",
             "The other regulariser you will use constantly in practice."),
        ])
    )))

# ============================================================ 10
L.append(dict(
    slug="10-iterative-loop", title="The iterative loop of ML development", mins=7, tag="intuition",
    lede="Nobody gets it right on the first pass. The skill is making each pass short and each decision "
         "informed.",
    body=(
        pretest("""<p>You will not get an ML system right first time. <b>Guess the loop</b> — what are the repeating steps, and which one do people skip?</p>""",
        """<p>Watch for the step most teams skip, and for how much time skipping it costs.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Building a model is like making soup. You don’t compute the perfect recipe in advance —
you throw things in, <b>taste it</b>, and adjust. Then taste again.</p>
<p>The whole skill is in the tasting: knowing what to taste for, and how to change one thing at a time so
you learn something from each round.</p>""")

        + h2("🎬", "Watch it move")
        + demo("mlloop", "Choose → train → diagnose → choose again",
               "the loop you will run dozens of times on any real project")

        + h2("🔢", "The three stations")
        + table(["Stage", "What you decide", "How long it should take"],
                [["<b>choose architecture</b>", "which model, which features, which data", "hours"],
                 ["<b>train the model</b>", "nothing — you just run it", "minutes to days"],
                 ["<b>run diagnostics</b>", "bias/variance, learning curves, error analysis", "hours"]])
        + key("""<p>Optimise for <b>laps per week</b>, not for cleverness per lap. A team that can go round
this loop daily will beat a team that spends a month designing the perfect first model, every time.</p>""")

        + h2("🔬", "The spam classifier example")
        + """<p>Andrew’s running example for the rest of the week. Features: take the top 10,000 words in
your corpus, and for each email record whether that word appears. Then a neural network on top.</p>
<p>Your first version will be mediocre. The interesting question is what you do next, and the honest
answer is that you cannot know until you look at the failures — which is Lesson 11.</p>"""

        + h2("🔤", "The words, decoded")
        + decode([
            ("iterative loop", "“the loop”", "Choose an architecture, train, diagnose, repeat. Nobody gets it right the first time, and the loop is the job."),
            ("architecture", "“architecture”", "The structural choices — how many layers, which activations, which features. Everything you pick before training."),
            ("error analysis", "“error analysis”", "Reading misclassified examples by hand and sorting them into categories. Manual, unglamorous, and the highest-value hour you will spend."),
            ("deployment", "“shipping it”", "Putting the model where real users hit it. Where a new and different set of problems begins."),
        ])
        + h2("🕳", "Traps")
        + trap("""<p><b>Trying to design the perfect system up front.</b> You do not yet know what the hard
cases look like. Build the crude version, look at what it gets wrong, and let the data tell you.</p>""")
        + trap("""<p><b>Changing three things per lap.</b> Then you cannot attribute the improvement, and
your next decision is a guess again.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("Why build a quick, crude first model rather than a careful one?",
             "<p>Because it tells you where the real difficulty is. Effort spent before that is effort "
             "spent on a guess.</p>"),
            ("What makes a diagnostic worth building even though it takes time?",
             "<p>It converts an expensive guess into a cheap fact. One saved data-collection project pays "
             "for many diagnostics.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("docs", "https://developers.google.com/machine-learning/guides/rules-of-ml",
             "Google — Rules of Machine Learning",
             "Rule #1: don’t be afraid to launch a product without ML. Rule #4: keep the first model simple."),
            ("book", "https://info.deeplearning.ai/machine-learning-yearning-book",
             "Machine Learning Yearning",
             "The whole book is about running this loop well."),
        ])
    )))

# ============================================================ 11
L.append(dict(
    slug="11-error-analysis", title="Error analysis", mins=10, tag="core",
    lede="The second great diagnostic, and it needs no maths at all: read the mistakes, by hand, and count "
         "the categories.",
    body=(
        pretest("""<p>Your spam filter misclassifies 500 emails. <b>Guess what you would actually do with them</b> to decide what to fix next.</p>""",
        """<p>Watch for how manual and unglamorous the answer is — and how much better it works than intuition.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Your spam filter got 100 emails wrong. Instead of guessing why, <b>read them</b>. Put
them in piles: “these are all about pills”, “these are fake bank emails”, “these are weirdly spelled”.</p>
<p>Then count the piles. 21 pills, 18 fake banks, 3 weird spellings. Now you know exactly what to build
next — and, just as importantly, what <b>not</b> to build. Fixing the spelling problem could take a month
and would win you three emails.</p>""")

        + h2("🎬", "Watch it move")
        + demo("erroranalysis", "100 mistakes, sorted into piles",
               "the count per pile is the whole output of the technique")

        + h2("🔢", "How to actually do it")
        + """<ol>
<li>Take the misclassified <b>cross-validation</b> examples. If there are more than ~100, sample 100 at
random — that is enough to see the big categories.</li>
<li>Read them. Actually read them. Invent categories as you go; they will overlap, and that is fine.</li>
<li>Count each category.</li>
<li>Work on the biggest category that also looks tractable.</li>
</ol>"""
        + decode([
            ("100 examples", "“a sample is enough”", "You are estimating proportions, not being exhaustive. 100 is plenty to tell 20% from 3%."),
            ("overlapping categories", "“tags, not buckets”", "One email can be pharma AND phishing AND misspelled. Count it in all three."),
            ("tractable", "“can I even fix it?”", "A big category you have no idea how to attack is worth less than a medium one you can fix this week."),
        ])
        + key("""<p>Error analysis tells you what to work on. Bias/variance tells you what <em>kind</em> of
change to make. Together they cover almost every “what next?” decision you will face.</p>""")

        + h2("🔬", "Why it beats intuition")
        + """<p>The classic outcome: the team has been arguing for two weeks about deliberate misspellings
(w4tches, m0rtgage) because it is an interesting problem. Error analysis reveals it accounts for 3 of 100
errors. Even a perfect fix moves accuracy by 0.3 percentage points.</p>
<p>Meanwhile pharmaceutical spam is 21 of 100 and nobody was working on it. The technique is not clever —
it is just looking. And it is skipped constantly.</p>"""
        + warn("""<p>Error analysis is much harder for tasks humans cannot do. Reading a mislabelled email
is easy; understanding why a model mispredicted a click-through rate is not. It works best where you can
look at an example and tell what the right answer was.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Doing it on the test set.</b> You will start designing features around those
examples, and your final estimate is compromised. Use the cross-validation set.</p>""")
        + trap("""<p><b>Skipping it because it feels unscientific.</b> It is the highest-value hour in most
projects.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("1000 cv examples, 100 misclassified. Error analysis finds 30% are one category. If you fixed it perfectly, what happens to accuracy?",
             "<p>You would recover 30 of 1000 examples → accuracy improves by <b>3 percentage points</b> "
             "(90% → 93%). Worth knowing <em>before</em> you commit a month.</p>"),
            ("You have 5000 misclassified examples. Do you need to read all of them?",
             "<p>No. Sample 100. You are estimating proportions, and 100 is enough resolution to rank "
             "the categories.</p>"),
            ("Error analysis says a category is 40% of errors but you have no idea how to fix it. What now?",
             "<p>Note it, and work on the next biggest one you <em>can</em> fix. Impact matters, but so "
             "does tractability.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("book", "https://info.deeplearning.ai/machine-learning-yearning-book",
             "Machine Learning Yearning — “Basic Error Analysis”",
             "Chapters 10–19. The definitive treatment, with worked spreadsheets."),
            ("docs", "https://developers.google.com/machine-learning/guides/rules-of-ml#rule_23_you_are_not_a_typical_end_user",
             "Google — Rules of ML, rule 23",
             "“You are not a typical end user.” Look at real failures, not the ones you imagine."),
        ])
    )))

# ============================================================ 12
L.append(dict(
    slug="12-adding-data", title="Adding data", mins=10, tag="core",
    lede="When you do need more data, you rarely need more of everything. Targeted collection, "
         "augmentation, and synthesis — cheapest first.",
    body=(
        pretest("""<p>You need more data and labelling is expensive. <b>Guess two ways to get more without collecting any.</b></p>""",
        """<p>Watch for augmentation and synthesis, and for the rule about what a useful distortion looks like.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>You need more practice questions. Three ways to get them:</p>
<ol><li><b>Buy more</b> — but only of the type you keep getting wrong. (targeted collection)</li>
<li><b>Bend the ones you have</b> — turn the page sideways, photocopy it badly, read it in dim light.
Still the same question, still the same answer. (augmentation)</li>
<li><b>Make brand new ones from scratch</b> — write your own with a computer. (synthesis)</li></ol>""")

        + h2("🎬", "Watch it move")
        + demo("augment", "One letter becomes twelve",
               "rotate, stretch, shear, add noise — the label never changes")

        + h2("🔢", "The three strategies")
        + table(["Strategy", "What it is", "Cost", "Best for"],
                [["<b>targeted collection</b>", "get more of the category error analysis flagged", "medium — but focused", "when one category dominates your errors"],
                 ["<b>data augmentation</b>", "distort existing examples in realistic ways", "cheap", "images, audio — anything with natural variation"],
                 ["<b>data synthesis</b>", "generate brand-new examples artificially", "medium–high", "OCR (render text in many fonts), simulation, rare events"]])
        + key("""<p>The distortion must be <b>representative of what happens in the real world</b>. Adding
random per-pixel noise to clean scanned text teaches the model to solve a problem it will never
encounter — pure wasted capacity.</p>""")

        + h2("🔬", "Examples that work")
        + grid3(
            card("<h3>Images</h3><p>Rotate, crop, flip, scale, change brightness and contrast, add "
                 "realistic blur. Flipping is fine for cats; not for handwritten digits, where a mirrored "
                 "2 is not a 2.</p>"),
            card("<h3>Audio</h3><p>Add crowd noise, car noise, a poor phone line, slight speed changes. "
                 "One clip becomes a dozen realistic recordings.</p>"),
            card("<h3>Text (OCR)</h3><p>Render real words in thousands of fonts, sizes, colours and "
                 "backgrounds. Photorealistic synthesis is a huge win here.</p>"))

        + h2("📊", "The data-centric shift")
        + """<p>The classical approach fixes the data and iterates on the model. The <b>data-centric</b>
approach fixes the model and iterates on the data — usually by improving label quality and consistency
rather than adding volume.</p>
<p>On many practical problems, with a decent architecture already available, improving the data is the
higher-return activity. Andrew has spent much of the last few years arguing exactly this.</p>"""

        + h2("🔤", "The words, decoded")
        + decode([
            ("data augmentation", "“augmentation”", "Making new training examples by distorting existing ones. The distortion must resemble noise that actually occurs."),
            ("data synthesis", "“synthesis”", "Manufacturing examples from scratch — rendering text in many fonts, for instance."),
            ("data-centric", "“data-centric”", "Improving the data and holding the model fixed, rather than the reverse. Often the better return."),
            ("transfer learning", "“transfer learning”", "Starting from a model trained on someone else's much larger data set."),
        ])
        + h2("🕳", "Traps")
        + trap("""<p><b>Augmenting with distortions that never happen.</b> If your production images are
always upright, rotating them 90° adds noise, not signal.</p>""")
        + trap("""<p><b>Augmenting the cross-validation or test set.</b> Only augment the training set. Your
evaluation must reflect the real distribution.</p>""")
        + trap("""<p><b>Adding data to fix high bias.</b> Still doesn’t work. Check the diagnostic first.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("Speech recogniser struggles with car noise. Cheapest fix?",
             "<p><b>Augmentation</b>: overlay recorded car noise onto your existing clean clips. Far "
             "cheaper than recording thousands of new in-car samples.</p>"),
            ("You mirror-flip images of handwritten digits. What goes wrong?",
             "<p>A mirrored 2 is not a 2. The label is no longer correct, so you are training on wrong "
             "answers. Flipping is only valid where the class is genuinely symmetric.</p>"),
            ("When is targeted collection better than augmentation?",
             "<p>When error analysis shows one specific category dominating and you cannot realistically "
             "simulate it — for example, a rare defect type you have only five photos of.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("paper", "https://link.springer.com/article/10.1186/s40537-019-0197-0",
             "Shorten & Khoshgoftaar (2019) — A survey on image data augmentation",
             "Every technique, with measured effects. Free and readable."),
            ("docs", "https://www.tensorflow.org/tutorials/images/data_augmentation",
             "TensorFlow — data augmentation tutorial",
             "Keras preprocessing layers that augment inside the model, so it happens on the GPU."),
            ("video", "https://https-deeplearning-ai.github.io/data-centric-comp/",
             "The Data-Centric AI competition",
             "A competition where the model was fixed and only the data could change. The results are the argument."),
        ])
    )))

# ============================================================ 13
L.append(dict(
    slug="13-transfer-learning", title="Transfer learning", mins=10, tag="core",
    lede="Borrow someone else’s trained network, replace its last layer, and train on your fifty examples. "
         "It works absurdly well.",
    body=(
        pretest("""<p>You have 50 images of your product. A network trained on a million photos of other things exists. <b>Guess how the second helps with the first.</b></p>""",
        """<p>Watch for which layers you keep and which you replace, and for why early layers transfer at all.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Somebody spent a fortune teaching a computer to recognise a thousand everyday things:
cats, cars, chairs, coffee cups. Along the way it had to learn what an <b>edge</b> is, what a
<b>corner</b> is, what a <b>texture</b> is.</p>
<p>You want to spot tumours in X-rays and you only have fifty pictures. Fifty is nowhere near enough to
learn “what an edge is” from scratch.</p>
<p>So take their network, throw away only the <b>last</b> layer (the part that says “cat”), bolt on your
own last layer that says “tumour / no tumour”, and train just that. All the hard-won knowledge about edges
and textures comes along for free.</p>""")

        + h2("🎬", "Watch it move")
        + demo("transfer", "Pre-train on a million photos, then fine-tune on fifty X-rays",
               "the borrowed layers are frozen; only the new output layer is trained")

        + h2("🔢", "The two options")
        + table(["Option", "What you train", "When to use it"],
                [["<b>1 — freeze</b>", "only the new output layer’s parameters", "very small dataset (tens to hundreds of examples)"],
                 ["<b>2 — fine-tune</b>", "all parameters, starting from the borrowed values", "larger dataset (thousands+)"]])
        + decode([
            ("supervised pre-training", "“their expensive step”", "Training on a large, general dataset — ImageNet for vision, a huge text corpus for language."),
            ("fine-tuning", "“your cheap step”", "Continuing training on your small, specific dataset, starting from their weights instead of random ones."),
            ("freezing", "“don’t touch these”", "Marking layers as untrainable so gradient descent leaves them alone."),
            ("the last layer", "“the task-specific bit”", "The only part that genuinely depends on <em>your</em> classes. Everything before it is general-purpose feature extraction."),
        ])
        + key("""<p>Why it works: the early layers learn things that are true of <b>all</b> images — edges,
corners, textures, shapes. Those facts do not care whether the picture is a cat or a chest X-ray.</p>""")

        + warn("""<p>The input type must match. An image network transfers to other image tasks. It does
<b>not</b> transfer to audio or tabular data — the borrowed layers are detecting visual structure that
simply isn’t there.</p>""")

        + h2("💻", "In code")
        + code("""
base = tf.keras.applications.MobileNetV2(include_top=False, weights='imagenet')
base.trainable = False                       # option 1: freeze everything borrowed

model = Sequential([
    base,
    tf.keras.layers.GlobalAveragePooling2D(),
    Dense(1, activation='sigmoid'),          # your new output layer
])
model.compile(optimizer=Adam(1e-3), loss=BinaryCrossentropy())
model.fit(X_small, y_small, epochs=10)

# later, optionally: base.trainable = True and re-fit with a MUCH smaller learning rate
""")
        + """<p>That last comment matters. When you unfreeze for fine-tuning, drop the learning rate by a
factor of 10–100. A normal learning rate will destroy the pre-trained weights in the first few steps —
this is the most common way to make transfer learning worse than training from scratch.</p>"""

        + h2("🌍", "Why this is a big deal")
        + """<p>Transfer learning is the reason a small team with a few hundred labelled examples can build
something useful at all. It is also the foundation of the entire modern “foundation model” idea: pre-train
once at enormous cost, then adapt cheaply, thousands of times, to specific tasks.</p>
<p>When you fine-tune a language model on your company’s documents, or attach a small classifier head to a
vision model — this lesson is what you are doing.</p>"""

        + h2("🕳", "Traps")
        + trap("""<p><b>Forgetting to lower the learning rate when unfreezing.</b> Large gradients wipe out
the pre-trained features immediately.</p>""")
        + trap("""<p><b>Using the wrong preprocessing.</b> Pre-trained models expect their original input
scaling — some want [0,1], some [−1,1], some ImageNet mean-subtraction. Use the model’s own
<code>preprocess_input</code> function.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("You have 100 labelled X-rays. Freeze or fine-tune?",
             "<p><b>Freeze.</b> With 100 examples, training millions of parameters would overfit "
             "immediately. Train only the new output layer.</p>"),
            ("Can you transfer an image model to a speech task?",
             "<p><b>No</b> — different input type entirely. Transfer requires the same kind of input. "
             "(Spectrograms are a clever partial exception, treating audio as an image.)</p>"),
            ("Why is only the output layer replaced rather than the last three?",
             "<p>Because only the output layer is truly task-specific — its size is literally the number "
             "of classes. Layers before it hold general features worth keeping.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("docs", "https://www.tensorflow.org/tutorials/images/transfer_learning",
             "TensorFlow — transfer learning and fine-tuning",
             "The complete official walkthrough, including the learning-rate change when unfreezing."),
            ("paper", "https://arxiv.org/abs/1411.1792",
             "Yosinski et al. (2014) — How transferable are features in deep neural networks?",
             "Measures layer by layer how transferable each level of features is. The empirical basis for the whole technique."),
            ("paper", "https://arxiv.org/abs/1911.02685",
             "Zhuang et al. (2019) — A Comprehensive Survey on Transfer Learning",
             "If you need the taxonomy and the variants."),
            ("docs", "https://keras.io/api/applications/",
             "Keras Applications — the pre-trained model zoo",
             "MobileNet, ResNet, EfficientNet — one line each, weights downloaded for you."),
        ])
    )))

# ============================================================ 14
L.append(dict(
    slug="14-full-cycle", title="The full cycle of a machine learning project", mins=9, tag="intuition",
    lede="Modelling is maybe 20% of the work. Here is the other 80%, including the parts that only bite "
         "after launch.",
    body=(
        pretest("""<p>The model works in your notebook. <b>List everything still standing between that and users relying on it.</b></p>""",
        """<p>Watch for how much of the work sits after the modelling — and for the part that never ends.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Baking a cake isn’t just mixing. It’s deciding what cake to make, buying ingredients,
mixing, baking, <b>and</b> checking it hasn’t gone stale a week later.</p>
<p>Machine learning projects have the same shape, and the last part — the “is it still good?” part —
is the one people forget. A model that was excellent in March can be quietly useless by September, because
the world moved and the model didn’t.</p>""")

        + h2("🎬", "Watch it move")
        + demo("fullcycle", "Scope → data → train → deploy, with the arrows that go backwards",
               "the dashed purple arrows are where projects actually spend their time")

        + h2("🔢", "The four stages")
        + table(["Stage", "The real work", "Where it goes wrong"],
                [["<b>scope</b>", "define the problem, decide whether ML is even the answer", "solving a problem nobody has"],
                 ["<b>collect data</b>", "decide what to collect, then label it consistently", "inconsistent labels; not enough of the rare class"],
                 ["<b>train</b>", "train, error-analyse, and go back for more data", "skipping the diagnostics"],
                 ["<b>deploy</b>", "serve it, monitor it, maintain it, retrain it", "no monitoring, so nobody notices decay"]])
        + key("""<p>The arrows that go <b>backwards</b> are the ones that consume your quarter. Error
analysis sends you back to data collection. Production feedback sends you back to training. Plan for the
loop, not for a straight line.</p>""")

        + h2("🚀", "What deployment actually involves")
        + """<p>A typical setup: your model sits behind an inference server; the mobile app calls an API;
predictions come back. Then the parts nobody mentions in tutorials:</p>
<ul>
<li><b>Monitoring</b> — track the input distribution, not just uptime. A prediction service can be 100%
available and 100% wrong.</li>
<li><b>Data drift</b> — the world changes. New slang breaks a spam filter; a new phone camera breaks a
vision model.</li>
<li><b>Feedback loops</b> — your model influences the data it later trains on. A recommender that never
shows an item never learns whether people wanted it.</li>
<li><b>Rollback</b> — you will ship a bad model one day. Be able to undo it in minutes.</li>
</ul>
<p>The field name for this is <b>MLOps</b>. It is a whole discipline, and it is where most ML value is
actually won or lost.</p>"""

        + h2("🔤", "The words, decoded")
        + decode([
            ("scoping", "“scoping”", "Deciding what the project is for, before any data is collected. The stage most often skipped."),
            ("deployment", "“deployment”", "Serving the model to real traffic — an API, monitoring, and a rollback plan."),
            ("MLOps", "“em-el-ops”", "The engineering practice around deployed models: versioning, monitoring, retraining."),
            ("concept drift", "“drift”", "The world changes and the model silently gets worse. Why monitoring exists."),
        ])
        + h2("🕳", "Traps")
        + trap("""<p><b>Treating deployment as the finish line.</b> It is the start of the maintenance
phase, which lasts as long as the product does.</p>""")
        + trap("""<p><b>No monitoring of inputs.</b> Accuracy metrics need labels, which arrive late or
never. Watching the <em>input</em> distribution shift gives you an early warning that needs no labels at
all.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("Your deployed spam filter's accuracy drops over six months with no code change. Why?",
             "<p><b>Data drift.</b> Spammers changed tactics; the distribution moved away from your "
             "training data. The fix is retraining on recent data, and monitoring that would have caught "
             "it sooner.</p>"),
            ("Why monitor input distributions rather than just accuracy?",
             "<p>Because true labels in production are delayed or unavailable. Input drift is measurable "
             "immediately and predicts trouble before accuracy reports arrive.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("docs", "https://developers.google.com/machine-learning/guides/rules-of-ml",
             "Google — Rules of Machine Learning",
             "43 hard-won rules about the non-modelling 80%."),
            ("paper", "https://papers.nips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems.pdf",
             "Sculley et al. (2015) — Hidden Technical Debt in Machine Learning Systems",
             "The famous “the ML code is the small box” diagram. Essential and slightly terrifying."),
            ("docs", "https://ml-ops.org/",
             "MLOps.org — principles and practices",
             "A practical map of the tooling landscape around deployment and monitoring."),
        ])
    )))

# ============================================================ 15
L.append(dict(
    slug="15-fairness-bias-ethics", title="Fairness, bias, and ethics", mins=9, tag="core",
    lede="A model trained on the past will reproduce the past. This lesson is short, non-technical, and "
         "the one most likely to matter to somebody's life.",
    body=(
        pretest("""<p>Your model is accurate overall. <b>Guess how it could still be doing serious harm</b> — accuracy and fairness are not the same measurement.</p>""",
        """<p>Watch for who the average hides. Watch also for the concrete process suggested rather than good intentions.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>If you teach a computer by showing it what people did before, it learns to do what
people did before — including the unfair bits. It has no way to know which parts of history were a mistake.</p>
<p>And it will do it faster, cheaper and at bigger scale than any person could, while sounding perfectly
objective because it is “just maths”.</p>""")

        + h2("🎬", "Watch it move")
        + demo("fairness", "One accuracy number, four very different experiences",
               "press the button to break the average down by group")

        + h2("📋", "Documented cases worth knowing")
        + """<ul>
<li><b>Hiring.</b> A recruiting tool trained on ten years of past hires learned to down-rank CVs
containing the word “women’s”, because the historical hires it learned from were overwhelmingly male. The
project was scrapped.</li>
<li><b>Face recognition.</b> Buolamwini & Gebru measured commercial systems with error rates under 1% for
lighter-skinned men and over 30% for darker-skinned women — a 30× gap invisible in the headline accuracy.</li>
<li><b>Criminal risk scores.</b> ProPublica’s analysis of the COMPAS tool found different false-positive
rates across racial groups. The subsequent statistical debate is genuinely worth reading: several
reasonable definitions of “fair” are <em>mathematically incompatible</em>, so you must choose which one
you mean.</li>
<li><b>Medical devices.</b> Pulse oximeters and some diagnostic models perform measurably worse on darker
skin, because of who was in the calibration data.</li>
</ul>"""
        + key("""<p>Aggregate accuracy hides subgroup failure by construction. If a group is 6% of your
data, you can serve them terribly and still post a 92% headline number. <b>Always evaluate per
subgroup.</b></p>""")

        + h2("🛠", "What to actually do")
        + grid2(
            card("<h3>Before you build</h3><ul>"
                 "<li>Ask who could be harmed if it is wrong, and how badly.</li>"
                 "<li>Get a diverse team — homogeneous teams miss homogeneous blind spots.</li>"
                 "<li>Look for prior harms in your domain; someone has usually been here before.</li></ul>"),
            card("<h3>Before you ship</h3><ul>"
                 "<li>Measure performance <b>per subgroup</b>, not just overall.</li>"
                 "<li>Run an adversarial review: how would a bad actor use this?</li>"
                 "<li>Have a rollback plan and a way for users to appeal a decision.</li>"
                 "<li>Write a model card: intended use, known limits, evaluation by group.</li></ul>"))
        + warn("""<p>Removing the sensitive attribute from your features does <b>not</b> make a model fair.
Postcode, name, school and shopping history are all proxies. The model rediscovers the attribute; you just
lose the ability to measure the disparity.</p>""")

        + h2("🔤", "The words, decoded")
        + decode([
            ("bias", "“bias”, as in unfairness", "Systematically worse outcomes for a group. Unrelated to the bias/variance sense used elsewhere this week."),
            ("disparate impact", "“disparate impact”", "A system that harms one group more than another, whether or not anyone intended it."),
            ("adversarial attack", "“adversarial”", "A deliberately crafted input designed to fool the model."),
            ("audit", "“audit”", "Measuring performance separately per group <b>before</b> shipping. The single most useful concrete step."),
        ])
        + h2("✅", "Check yourself")
        + quiz([
            ("Your loan model is 94% accurate overall. What is the next thing to measure?",
             "<p>Accuracy — and false-positive and false-negative rates — <b>per subgroup</b>. The average "
             "cannot tell you whether one group is being systematically refused.</p>"),
            ("Does deleting the race field from your dataset make the model race-blind?",
             "<p><b>No.</b> Correlated features act as proxies. You lose the ability to audit for "
             "disparity without removing the disparity.</p>"),
            ("Why is “high accuracy” an insufficient standard for a medical model?",
             "<p>Because errors are not symmetric and not evenly distributed. A missed diagnosis costs far "
             "more than a false alarm, and a model can be accurate on average while failing an entire "
             "patient group.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("paper", "https://proceedings.mlr.press/v81/buolamwini18a.html",
             "Buolamwini & Gebru (2018) — Gender Shades",
             "The face-recognition audit. Careful, devastating, and the model for how to do this work."),
            ("paper", "https://arxiv.org/abs/1810.03993",
             "Mitchell et al. (2018) — Model Cards for Model Reporting",
             "A practical template for documenting intended use, limits and per-group evaluation."),
            ("book", "https://fairmlbook.org/",
             "Barocas, Hardt & Narayanan — Fairness and Machine Learning",
             "Free textbook. Chapter 2 explains why several definitions of fairness cannot all hold at once."),
            ("docs", "https://www.propublica.org/article/machine-bias-risk-assessments-in-criminal-sentencing",
             "ProPublica — Machine Bias",
             "The COMPAS investigation. Read the rebuttals too — the disagreement is the education."),
        ])
    )))

# ============================================================ 16
L.append(dict(
    slug="16-skewed-datasets", title="Error metrics for skewed datasets", mins=16, tag="core",
    lede="When 99.5% of your labels are the same value, accuracy becomes a liar. Precision and recall are "
         "the replacement.",
    body=(
        pretest("""<p>A disease affects 1 in 200. Here is my diagnostic program: <code>print("healthy")</code>. <b>What is its accuracy — and what is wrong with that number?</b></p>""",
        """<p>99.5%. Watch for the two questions that replace accuracy when one class is rare.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>A rare disease affects 1 in 200 people. I have written a diagnostic program. Here it
is, in full:</p>
<p style="text-align:center"><code>print("healthy")</code></p>
<p>It is <b>99.5% accurate</b>. It is also completely worthless — it has never found a single sick person
and never will.</p>
<p>So we need two better questions. Of everyone I <b>flagged</b>, how many were really ill? (precision)
And of everyone who was really ill, how many did I <b>catch</b>? (recall) My program scores zero on both,
which is the correct verdict.</p>""")

        + h2("🔢", "The maths, decoded")
        + eqp([
            ('precision <span class="op">=</span> <span class="frac"><span>true positives</span><span>true positives + <span class="hl-r">false</span> positives</span></span>',
             "precisionrecall-native", "of what I flagged, how much was right?"),
            '&nbsp;&nbsp;&nbsp;&nbsp;',
            ('recall <span class="op">=</span> <span class="frac"><span>true positives</span><span>true positives + <span class="hl-r">false</span> negatives</span></span>',
             "precisionrecall-native", "of what was true, how much did I catch?"),
        ], "both have TP on top — they differ in what goes wrong underneath — hover or click a part")
        + decode([
            ("true positive", "“caught it”", "Predicted 1, actually 1. What you want."),
            ("false positive", "“false alarm”", "Predicted 1, actually 0. Cost: wasted tests, annoyed customers, lost trust."),
            ("false negative", "“missed it”", "Predicted 0, actually 1. Cost: the disease goes untreated, the fraud goes through."),
            ("precision", "“when I shout, am I right?”", "Denominator = everything you flagged. Low precision = crying wolf."),
            ("recall", "“of the real ones, how many did I get?”", "Denominator = everything that was actually positive. Low recall = missing cases."),
        ])
        + key("""<p>Precision’s denominator is <b>what you predicted</b>. Recall’s denominator is <b>what
was true</b>. If you can hold on to that one difference, you will never mix them up again.</p>""")

                + lenses(
            """<p>A smoke alarm that never goes off is right 99.9% of the time.</p>
<p>Stated as accuracy that sounds excellent, and it is useless — because the thing it exists to detect
is rare, and it detects none of it. Any measure that lets “do nothing” score highly is measuring the
wrong thing.</p>""",
            """<p>This is class imbalance, and it breaks accuracy the way a heavily skewed distribution breaks the
mean.</p>
<p>The replacements are precision (of what you flagged, how much was real) and recall (of what was
real, how much you flagged). They pull against each other, and F1 is the harmonic mean — harmonic
specifically because it refuses to be rescued by one good half.</p>""",
            """<p>A two-by-two grid: predicted yes/no against actually yes/no.</p>
<p>Precision reads one <em>column</em>; recall reads one <em>row</em>. They share the true-positive
corner and differ in what they divide it by, which is the whole distinction and the reason the two
are so easily confused.</p>""",
            """<p>Cancer screening lives on this trade-off. Higher recall means fewer missed tumours and more
healthy people put through anxious follow-ups; higher precision means fewer false alarms and more
missed cases.</p>
<p>There is no mathematically correct answer — it is a judgement about which harm is worse, made by
clinicians and regulators, and then implemented as a threshold. The model supplies the probability;
people supply the ethics.</p>""",
            """So the two formulas below are worth memorising as “of what I flagged” and “of what was really
there”.""")
        + h2("🎬", "Watch it move")
        + demo("confusion", "The confusion matrix, live",
               "400 patients, 5% actually ill — drag the threshold and watch all four numbers move")

        + h2("🧮", "The worked example")
        + table(["", "Actually 1", "Actually 0"],
                [["<b>Predicted 1</b>", "TP = 15", "FP = 5"],
                 ["<b>Predicted 0</b>", "FN = 10", "TN = 70"]])
        + """<p>Precision = 15 / (15 + 5) = <b>0.75</b>. Three-quarters of your alarms were real.<br>
Recall = 15 / (15 + 10) = <b>0.60</b>. You caught 60% of the true cases.<br>
Accuracy = (15 + 70) / 100 = 0.85 — which sounds better than either, and tells you less than both.</p>"""
        + eqp([
            ('F<sub>1</sub> <span class="op">=</span> 2 <span class="op">·</span> <span class="frac"><span>P <span class="op">·</span> R</span><span>P + R</span></span>',
             "harmonic-mean", "leans toward whichever is worse"),
        ], "one number, when you need to rank models — hover or click it")
        + """<p>F1 is the <b>harmonic</b> mean, and that choice is deliberate: it sits close to the smaller
of the two numbers. Precision 1.0 with recall 0.01 gives F1 ≈ 0.02, not 0.5. It refuses to be impressed by
a model that is excellent at one half and useless at the other.</p>"""

        + explain("""<p><code>print("healthy")</code> scored 99.5%. <b>Why does accuracy fail here when it works elsewhere?</b></p>""",
            """<p>Because accuracy rewards getting the common case right, and here the common case is 199 of every 200. The metric is dominated by the class you do not care about, so it can be nearly perfect while the model never once does the thing it exists to do.</p>""")
        + h2("🕳", "Traps")
        + trap("""<p><b>Reporting accuracy on skewed data.</b> With 1 in 200 positives, accuracy is
essentially a measurement of how rare the positive class is.</p>""")
        + trap("""<p><b>Optimising recall alone.</b> Predict 1 for everybody and recall is a perfect 1.0.
Precision collapses. The pair only means something together.</p>""")
        + trap("""<p><b>Mixing up which is which under pressure.</b> Memorise the denominators: precision =
what I predicted, recall = what was true.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("TP=8, FP=2, FN=12, TN=978. Precision, recall, accuracy?",
             "<p>Precision = 8/10 = <b>0.80</b>. Recall = 8/20 = <b>0.40</b>. Accuracy = 986/1000 = "
             "<b>0.986</b> — which looks superb and hides the fact you missed 60% of the cases.</p>"),
            ("A model always predicts 0 on a 1%-positive dataset. Precision and recall?",
             "<p>Recall = <b>0</b> (caught nothing). Precision is 0/0 — undefined, conventionally reported "
             "as 0. Accuracy would be 99%.</p>"),
            ("Why the harmonic mean for F1 rather than the plain average?",
             "<p>Because the plain average of 1.0 and 0.01 is 0.505, which flatters a useless model. The "
             "harmonic mean gives 0.02 — it stays near the weaker number.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("docs", "https://scikit-learn.org/stable/modules/model_evaluation.html#precision-recall-f-measure-metrics",
             "scikit-learn — precision, recall and F-measure",
             "<code>classification_report()</code> prints all of it per class in one call."),
            ("docs", "https://developers.google.com/machine-learning/crash-course/classification/accuracy-precision-recall",
             "Google ML Crash Course — accuracy, precision, recall",
             "A second telling with a different worked example and interactive widgets."),
            ("paper", "https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0118432",
             "Saito & Rehmsmeier (2015) — The precision-recall plot is more informative than the ROC plot",
             "Why PR curves beat ROC curves specifically on imbalanced data."),
        ])
    )))

# ============================================================ 17
L.append(dict(
    slug="17-precision-recall-tradeoff", title="Trading off precision and recall", mins=15, tag="core",
    lede="You cannot have both. The threshold is the dial, and where you set it is a decision about "
         "consequences, not about statistics.",
    body=(
        pretest("""<p>Raise the threshold for calling something positive. <b>Guess what happens to precision, and what happens to recall.</b> They do not move together.</p>""",
        """<p>Watch for why you cannot maximise both, and for how to pick a point on the trade-off deliberately.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>You’re a lifeguard deciding when to blow the whistle.</p>
<ul><li><b>Only whistle when you’re certain someone is drowning.</b> You’ll almost never be wrong — but
you’ll miss the quiet ones. High precision, low recall.</li>
<li><b>Whistle at anything that might be trouble.</b> You’ll save everyone — and clear the pool six times
a day for nothing. High recall, low precision.</li></ul>
<p>There is no setting that is right for every beach. It depends on how bad a missed rescue is compared to
a false alarm — and that is a judgement about <em>consequences</em>, not about mathematics.</p>""")

        + h2("🎬", "Watch it move")
        + demo("prcurve", "The trade-off curve",
               "every point on the curve is one threshold — drag to move along it")

        + h2("🔢", "Which way to move the threshold")
        + table(["Threshold", "Effect", "Precision", "Recall", "Choose when"],
                [["<b>high</b> (0.9)", "predict 1 only when very confident", "↑ up", "↓ down", "a false alarm is expensive or harmful"],
                 ["<b>0.5</b>", "the default", "—", "—", "no reason to prefer either error"],
                 ["<b>low</b> (0.15)", "predict 1 on any suspicion", "↓ down", "↑ up", "a miss is much worse than a false alarm"]])
        + decode([
            ("threshold", "“how sure before I act”", "The probability above which you predict 1. Nothing forces it to be 0.5."),
            ("PR curve", "“the whole trade-off”", "Precision plotted against recall as the threshold sweeps. It summarises the model, not one operating point."),
            ("operating point", "“the setting you ship”", "The single threshold you actually deploy. A product decision, made with the people who own the consequences."),
        ])
        + key("""<p>The model gives you a probability. The threshold turns it into an action, and the right
threshold depends on what an action <em>costs</em>. That decision belongs to the doctor, the fraud team,
the product owner — not to the person who trained the model.</p>""")

        + h2("🌍", "Real trade-offs")
        + grid3(
            card("<h3>Cancer screening</h3><p>A missed tumour is catastrophic; an extra scan is an "
                 "inconvenience. <b>Favour recall</b> — set the threshold low.</p>"),
            card("<h3>Spam filtering</h3><p>A lost job offer in the spam folder is far worse than one "
                 "extra spam in the inbox. <b>Favour precision</b> — set it high.</p>"),
            card("<h3>Fraud blocking</h3><p>Blocking a genuine customer's card is expensive and infuriating; "
                 "so is fraud. Usually a middle threshold plus a human review queue.</p>"))

        + h2("💻", "Choosing the threshold in code")
        + code("""
from sklearn.metrics import precision_recall_curve

probs = model.predict(X_cv).ravel()
precision, recall, thresholds = precision_recall_curve(y_cv, probs)

# option A: the threshold with the best F1
f1 = 2 * precision * recall / (precision + recall + 1e-12)
best = thresholds[f1[:-1].argmax()]

# option B (usually better): the cheapest threshold that meets a required recall
required_recall = 0.95
ok = [t for t, r in zip(thresholds, recall[:-1]) if r >= required_recall]
chosen = max(ok) if ok else 0.0
""")
        + warn("""<p>Pick the threshold on the <b>cross-validation</b> set, never the test set. It is a
model choice like any other.</p>""")

        + h2("🧮", "The whole trade-off, one threshold at a time")
        + """<p>1,000 patients, 22 of them genuinely ill, and one model producing a probability for
each. Nothing about the model changes below — only the number you compare its output to:</p>"""
        + table(["threshold", "flagged", "TP", "FP", "FN", "precision", "recall", "F1"],
                [["0.2", "467", "22", "445", "0", "0.05", "<b>1.00</b>", "0.090"],
                 ["0.4", "112", "22", "90", "0", "0.20", "<b>1.00</b>", "0.328"],
                 ["0.5", "53", "20", "33", "2", "0.38", "0.91", "0.533"],
                 ["<b>0.6</b>", "20", "15", "5", "7", "0.75", "0.68", "<b>0.714</b>"],
                 ["0.7", "10", "10", "0", "12", "<b>1.00</b>", "0.45", "0.625"],
                 ["0.8", "4", "4", "0", "18", "<b>1.00</b>", "0.18", "0.308"]])
        + """<p>Read precision and recall moving in opposite directions, all the way down. At 0.2 the
model catches every ill patient — and flags 467 people to do it, so being flagged means almost
nothing. At 0.8 every flag is correct and it misses 18 of the 22.</p>
<p>F1 peaks in the middle, at 0.714. But notice what F1 is <em>not</em> doing: it does not know that
missing a sick patient is worse than a false alarm. If it is, 0.5 is the better threshold despite
its lower F1 — it catches 20 of 22 at the price of 33 unnecessary follow-ups. F1 compares
algorithms; consequences choose thresholds.</p>"""
        + explain("""<p>At threshold 0.7 precision is a perfect 1.00. <b>Why is that not the model
performing at its best?</b></p>""",
                  """<p>Because precision only asks about the cases the model chose to speak up on,
and at 0.7 it speaks up ten times out of a thousand. Being right about ten easy cases while staying
silent on twelve real ones is not accuracy, it is selectivity — and selectivity can always be made
perfect by refusing to answer. That is exactly why precision is never quoted alone: recall is the
number that counts what the silence cost.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Letting F1 make the decision for you.</b> F1 weights precision and recall equally,
which is almost never what the real cost structure looks like. It is a fine way to <em>rank models</em>,
and a poor way to <em>choose an operating point</em>.</p>""")
        + trap("""<p><b>Reporting the threshold-tuned score on the same data you tuned it on.</b> Same
optimistic-bias problem as everything else this week.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("Raise the threshold from 0.5 to 0.9. What happens to precision and recall?",
             "<p>Precision <b>rises</b> (you only flag the clear cases) and recall <b>falls</b> (you miss "
             "the borderline true positives).</p>"),
            ("Rare, treatable, aggressive cancer. Which do you favour?",
             "<p><b>Recall.</b> A missed case can be fatal; a false positive costs one further test. "
             "Set the threshold low and accept the false alarms.</p>"),
            ("Two models: A has P=0.9, R=0.1. B has P=0.6, R=0.6. Which is better?",
             "<p>Depends entirely on the application — but F1 says B (0.60 vs 0.18), and B is the safer "
             "default. Model A finds almost nothing, however confidently.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("docs", "https://scikit-learn.org/stable/auto_examples/model_selection/plot_precision_recall.html",
             "scikit-learn — plotting precision-recall curves",
             "Runnable code for the demo above, including average precision."),
            ("docs", "https://developers.google.com/machine-learning/crash-course/classification/roc-and-auc",
             "Google — ROC and AUC",
             "The other curve. Useful, but misleading on heavily imbalanced data — see the Saito paper in Lesson 16."),
            ("lab", "../../C2%20-%20Advanced%20Learning%20Algorithms/week3/C2W3A1/C2_W3_Assignment.ipynb",
             "Week 3 assignment",
             "In this repo. Bias/variance diagnostics end to end."),
        ])
    )))

WEEK = dict(
    course="C2", week=3, title="Advice for Applying ML",
    time="~6–8 h with labs",
    goal="Diagnose what is actually wrong with a model — bias, variance, or data — and choose the next "
         "experiment from evidence instead of instinct.",
    lessons=L,
)
