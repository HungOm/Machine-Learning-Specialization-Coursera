# -*- coding: utf-8 -*-
"""Walkthrough for 14_mlops.py."""
from walkkit import p, expr, chain, chainset, steps, cases, values, point, ascii_art

PICTURE = ([
    ("in", "A model that works", "0.8375 on held-out test data. This is where courses stop."),
    ("arw", "write down exactly what produced it"),
    ("op", "Registry", "Hash the data, the weights and the scaler. A version you can "
                       "<b>return to</b>."),
    ("arw", "serve it &mdash; and now the ways to be wrong are different"),
    ("op", "Training / serving skew",
     "Scale live traffic with the <b>training</b> statistics. Recomputing them costs 10 "
     "accuracy points and raises no error."),
    ("arw", "watch it over months"),
    ("op", "Drift &mdash; and false alarms",
     "Inputs can move a long way and be fine. Inputs can be identical and the model be "
     "broken."),
    ("arw", "ship the replacement carefully"),
    ("op", "Canary", "A small slice, and a confidence interval that says whether you can "
                     "read anything from it yet."),
    ("out", "A rollback that is one string",
     "Which only works because of the registry, four steps earlier."),
], "The whole program in one picture",
   "Every box after the first is a way a working model quietly stops working. None of them "
   "raises an exception.")

WALK = {

"prelude": (
    p("""Every other file in this lane ends when the model works. This one <b>starts</b>
there.""")
    + point("""Everything below is a way a working model quietly stops working. Not one of
them raises an error, and that is precisely the difficulty.""")
),

"task": (
    p("""A loan-approval model. Two features, and a roughly balanced outcome.""")
    + values([("income", "mean 49.8", ""),
              ("years", "mean 6.0", ""),
              ("approval rate", "0.486", "close to half, so accuracy is a fair measure here")],
             "the training data")
),

"train": (
    p("""Train it. Nothing new &mdash; this is file 02's logistic regression.""")
    + values([("weights", "[2.3632, 2.2416]", ""),
              ("bias", "&minus;0.1357", ""),
              ("scaling &mu;", "[49.849, 5.965]", "<b>remember these two rows</b>"),
              ("scaling &sigma;", "[15.046, 2.975]", ""),
              ("test accuracy", "<b>0.8375</b>", "")],
             "the trained model")
    + point("""The <b>scaling statistics are part of the model</b>. Not a preprocessing
detail, not something you recompute later &mdash; they are as much a learned parameter as the
weights, and the next-but-one section shows what happens when you forget that.""")
),

"registry": (
    p("""Write down exactly what produced this model, by <b>hashing</b> each piece.""")
    + values([("data", "1f5e44413023", "which rows it was trained on"),
              ("weights", "e37aae5b5b41", "the parameters themselves"),
              ("scaler", "52135bcb4e84", "the &mu; and &sigma;"),
              ("n_train", "4000", ""),
              ("note", "champion", "the one currently serving traffic")],
             "the registry entry")
    + point("""A hash gives you an <b>exact</b> answer to &ldquo;is this the same
thing?&rdquo; &mdash; a question you cannot answer by eye and will need urgently at 3am.""")
    + p("""&ldquo;Version 3&rdquo; is a label somebody types and can retype. A hash is
computed from the content, so two artefacts with the same hash <b>are</b> the same
artefact.""")
    + point("""This section looks like bureaucracy. The <b>rollback</b> section at the end of
this file is what it buys, and it is the difference between a five-second fix and a
five-hour one.""")
),

"skew": (
    p("""The most expensive mistake in this file, and it produces no error at all.""")
    + p("""Live traffic arrives where incomes run <b>12.6 higher</b> than in training &mdash;
a perfectly ordinary shift.""")
    + cases([("Scale with the TRAINING &mu;/&sigma;",
              "accuracy <b>0.8545</b><br><b>Correct.</b> The model sees the same "
              "distribution it learned on."),
             ("Recompute &mu;/&sigma; at serve time",
              "accuracy <b>0.7530</b><br><b>Wrong</b>, by <b>10.2 accuracy points</b>.")],
            "the same traffic, the same model, two ways of scaling it")
    + point("""Recomputing looks <b>more</b> correct &mdash; surely you should standardise
against the data you actually have? No. The weights were learned in a coordinate system
defined by the training &mu; and &sigma;. Change the coordinate system and the weights mean
something else.""")
    + p("""And the second version <b>throws no error and returns sensible-looking
probabilities</b>. There is no symptom. You find it by knowing the rule, or you find it in a
quarterly review months later.""")
    + point("""This is <b>training/serving skew</b>, and it is the reason
<code>sklearn</code> splits <code>fit</code> from <code>transform</code>: to make the correct
thing the easy thing.""")
),

"drift": (
    p("""Watch the inputs drift over five months, with <b>PSI</b> &mdash; a standard measure
of how far a distribution has moved.""")
    + values([("month 1", "income PSI 0.0041", "accuracy 0.8458"),
              ("month 3", "income PSI 0.1310", "accuracy 0.8470"),
              ("month 4", "income PSI 0.3193", "accuracy 0.8455"),
              ("month 5", "income PSI <b>0.8660</b>", "accuracy <b>0.8660</b>")],
             "input drift against actual accuracy")
    + point("""PSI climbs by a factor of <b>200</b>. Accuracy does <b>not move</b> &mdash; in
fact it ends slightly higher than it started.""")
    + p("""The conventional PSI thresholds (0.1 = investigate, 0.25 = act) would have had you
retraining in month 3 and paging someone in month 4, for a model that was working
perfectly.""")
    + point("""Drift in the <b>inputs</b> is not damage. It is a <b>hypothesis</b> that
something might be wrong, and it is worth exactly as much as its false-alarm rate &mdash;
which the next section measures.""")
),

"false_alarm": (
    p("""Two scenarios, side by side. They are the reason input monitoring alone is not
enough.""")
    + cases([("A &mdash; the inputs move a long way",
              "income PSI <b>2.4719</b><br>accuracy <b>0.9137</b>, up from 0.8375<br>"
              "<b>A loud alarm about a model that got better.</b>"),
             ("B &mdash; the inputs are identical, the RULE changed",
              "income PSI <b>0.0037</b><br>accuracy <b>0.5215</b>, down from 0.8375<br>"
              "<b>Real damage, and every input monitor is silent.</b>")],
            "the two cases that matter")
    + point("""Scenario B is the one that should frighten you. The relationship between
features and outcome changed &mdash; years of employment now matters far less &mdash; and
<b>nothing on the input side can see that</b>, because the inputs are unchanged.""")
    + p("""Accuracy fell to <b>0.52</b>: barely better than a coin flip, on a model that
looks completely healthy from the outside. This is <b>concept drift</b>, and only
<b>outcomes</b> reveal it.""")
),

"delayed_labels": (
    p("""So watch outcomes. Except you usually cannot, for months.""")
    + point("""On a loan model the <b>approval rate is available instantly</b>. Whether those
loans were repaid is available in <b>90 days</b>.""")
    + p("""So the metric you can see is a <b>proxy</b>, and it is important to be honest
about that: a perfectly stable approval rate is entirely consistent with a model that has
quietly stopped working. It says the model still <i>decides</i> the same way, not that it
decides <i>well</i>.""")
    + point("""<b>Watch what you can see, and be honest that it is a proxy.</b> That is the
whole discipline: not pretending the fast number answers the slow question.""")
),

"canary": (
    p("""A challenger model, and the question of how much traffic you need before you can
believe a result.""")
    + p("""The true effect, measured on all 8,000 users, is <b>+0.0299</b>. Now pretend you
do not know that and read it off a canary.""")
    + values([("0.5% &mdash; 40 users", "+0.1013", "CI [+0.0000, +0.2250] &rarr; <b>keep waiting</b>"),
              ("2.5% &mdash; 200 users", "+0.0298", "CI [&minus;0.0050, +0.0650] &rarr; <b>keep waiting</b>"),
              ("12.5% &mdash; 1000 users", "+0.0271", "CI [+0.0140, +0.0410] &rarr; <b>ship</b>"),
              ("50% &mdash; 4000 users", "+0.0267", "CI [+0.0198, +0.0335] &rarr; <b>ship</b>")],
             "one challenger, one true effect, five readings")
    + point("""Look at the <b>40-user</b> row: it reports <b>+0.1013</b> &mdash; more than
three times the truth. A tiny canary does not give you a small amount of evidence; it gives
you a <b>wildly wrong number</b> with total confidence.""")
    + p("""The 200-user row has the point estimate almost exactly right (+0.0298 against
+0.0299) and its interval <b>still straddles zero</b>. Being right by luck is not the same as
having evidence.""")
    + point("""<b>The small canaries are not wrong about the data they saw.</b> They are being
asked a question their sample cannot answer, and &ldquo;keep waiting&rdquo; is the correct
reading of an interval that includes zero &mdash; not a failure of the test.""")
),

"rollback": (
    p("""The last section, and the payoff for the registry at the top.""")
    + values([("fe7074bb3f1f", "n_train=4000", "champion"),
              ("0aeb5ebe5181", "n_train=6000", "challenger, retrained on recent traffic")],
             "the registry now holds two versions")
    + chainset([([" serve with 0aeb5ebe ", "[0, 0, 0, 0, 0]"], "the challenger rejects everyone"),
                ([" serve with fe7074bb ", "[1, 0, 1, 0, 0]"], "the champion, restored")],
               "the same five requests")
    + point("""<b>Rolling back is: change one string.</b> Not retrain, not rebuild, not
find the notebook. One identifier.""")
    + p("""And that is <b>only</b> true because both versions are still <b>loadable</b> and
each carries <b>its own scaling statistics</b>. Load the old weights with the new scaler and
you have reproduced the skew bug from earlier in this file, while believing you rolled
back.""")
    + point("""<b>A rollback plan that requires retraining is not a rollback plan.</b> The
registry section at the top of this file is what buys you this line at the bottom &mdash;
which is the argument for doing the boring part first.""")
),

"checklist": (
    p("""Everything above, turned into questions you can actually answer before shipping.""")
    + steps(["Can you name the <b>exact</b> data, weights and preprocessing behind any past "
             "decision?",
             "Does <b>one</b> piece of code do the feature transform for both training and "
             "serving?",
             "Are the scaling statistics <b>stored with the weights</b>, not recomputed?",
             "Is drift measured <b>per feature</b>, against a <b>fixed</b> reference window?",
             "Do you know which of your monitors would catch a change in <b>P(y|x)</b>?",
             "What do you watch in the gap <b>before labels arrive</b>, and what does it "
             "miss?",
             "Is your canary <b>big enough</b> for its confidence interval to exclude zero?",
             "Can you <b>roll back without retraining</b> &mdash; and has anyone tried it "
             "recently?"])
    + point("""<b>None of these is a modelling question.</b> Not one mentions architecture,
loss functions, learning rates or accuracy.""")
    + p("""That is the lesson of the whole file, and the reason it exists at the end of this
lane: <b>after the model works, almost nothing that goes wrong is the model's fault</b>.""")
    + point("""Question 8 is the one people answer wrongly most often. &ldquo;We could roll
back&rdquo; and &ldquo;we have rolled back, recently, and it took under a minute&rdquo; are
very different claims, and only the second one is a plan.""")
),
}
