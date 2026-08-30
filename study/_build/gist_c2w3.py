# -*- coding: utf-8 -*-
"""The gist of C2 Week 3."""
from kit import key, trap
from gistkit import gistline, flow, sameskel, chain, bynumbers, retell, ladder, h2
from walkkit import cases, values, point, expr, chainset, ascii_art, steps

_P, _R = 1.00, 0.01
_F1 = 2*_P*_R/(_P+_R)

GIST = dict(
    course="C2", week="3", title="Advice for Applying ML", mins=13,
    lede="Seventeen lessons and no new algorithm in any of them. This is the week about "
         "what to DO when the model is bad — and it is probably the most useful week here.",
    body="".join([
        gistline("""Every other week teaches you a model. This one teaches you the loop you
run <b>around</b> models: measure two numbers, read which of two problems you have, apply
one of two sets of fixes, repeat. Getting that diagnosis right is worth more than any
architecture choice."""),

        h2("🖼", "The week in one picture"),
        flow([
            ("in", "A model that is not good enough", "And a decision to make about what to "
                                                      "try next."),
            ("arw", "split the data three ways, not two"),
            ("op", "Train / CV / test",
             "60 / 20 / 20. <b>Train</b> fits the weights, <b>CV</b> chooses the model, "
             "<b>test</b> is read <b>once</b>."),
            ("arw", "measure two numbers"),
            ("op", "J_train and J_cv",
             "<b>J_train tells you about bias. The GAP tells you about variance.</b> One "
             "sentence, most of the week."),
            ("arw", "compare against a baseline, not against zero"),
            ("op", "Two gaps, not one",
             "baseline → J_train is <b>avoidable bias</b>. J_train → J_cv is <b>variance</b>."),
            ("arw", "now pick from the right list"),
            ("op", "Six fixes, split into two threes",
             "Every variance fix makes the model <b>less</b> flexible. Every bias fix makes "
             "it <b>more</b>."),
            ("arw", "then look at what it is actually getting wrong"),
            ("back", "Error analysis",
             "Read 100 misclassified examples. Count categories. Fix the biggest tractable "
             "one. Repeat."),
        ], cap="""The loop never ends in &ldquo;the model is bad&rdquo;. It ends in a
specific next action, chosen by evidence rather than by taste."""),

        h2("🎯", "The central diagnostic"),
        key("""<p><b>J<sub>train</sub> tells you about bias. The gap between J<sub>train</sub>
and J<sub>cv</sub> tells you about variance.</b></p>
<p>Both bad and close together → <b>underfitting</b>; the model is too simple. Training
excellent and the gap large → <b>overfitting</b>; the model memorised. Both can be true at
once, and then you need both fixes.</p>
<p>You <b>cannot</b> tell these apart from the training score alone — which is the entire
reason a validation set exists.</p>"""),
        values([("get more training examples", "variance", "the best fix, and the most expensive"),
                ("try a smaller set of features", "variance", "less flexible"),
                ("increase &lambda;", "variance", "less flexible"),
                ("get additional features", "bias", "more flexible"),
                ("add polynomial features", "bias", "more flexible"),
                ("decrease &lambda;", "bias", "more flexible")],
               "the six fixes, and which problem each one is for"),
        point("""Nothing here needs memorising. <b>Every variance fix makes the model less
flexible; every bias fix makes it more flexible.</b> Work out which direction you need and
the list sorts itself.""", "How to never get this backwards"),

        h2("💸", "The most expensive mistake in applied ML"),
        trap("""<p>&ldquo;Get more data&rdquo; appears on <b>one</b> of the two lists.</p>
<p>More data does <b>nothing</b> for high bias. If the model is too simple to capture the
pattern, ten times as many examples will be fitted equally badly. And it is the most
expensive item on either list — months and money, in a way that changing &lambda; is not.</p>
<p>Teams routinely spend a quarter collecting data for a model that was never going to
benefit, and a <b>learning curve</b> would have said so on day one:</p>"""),
        ascii_art("""  HIGH BIAS                      HIGH VARIANCE
  err                            err
   |  J_cv  ______                |  J_cv \\___
   |  J_tr  ______   both flat    |            \\___  still falling
   |                              |
   |........... baseline          |  J_tr ____/------
   +--------------- m             +--------------- m
   small gap, both high           big gap, cv still dropping
   -> more data will NOT help     -> more data WILL help""",
                   "And note J_train RISES with m. Fitting 1,000 points is harder than "
                   "fitting 10 — a climbing training error is healthy, not broken."),

        h2("📏", "Why one number is never enough"),
        bynumbers("""On a dataset that is <b>0.5% positive</b>, here is a model with no
inputs and no parameters at all.""",
                  [("<code>print(&quot;healthy&quot;)</code>", "99.5%", "accuracy"),
                   ("people it helps", "0", "it catches nobody"),
                   ("precision", "undefined", "it never predicts positive"),
                   ("recall", "0.00", "of everyone who was ill, it found none")],
                  close="""On skewed data, accuracy measures <b>how rare the positive class
is</b>, not how good your model is. Report precision, recall and F1 — and be most suspicious
when the headline number is most impressive."""),
        chainset([(["P = 1.00, R = 0.01", "F1 = %.4f" % _F1], "the harmonic mean — correctly damning"),
                  (["P = 1.00, R = 0.01", "ordinary mean = 0.505"], "which would look respectable")],
                 "why F1 uses the harmonic mean"),
        point("""A harmonic mean sits <b>close to the smaller of the two</b>. F1 refuses to
be impressed by a model that is excellent at one half and useless at the other — and an
ordinary average would call that model average.""", "The point of F1"),

        h2("🔍", "The unglamorous thing that is worth the most"),
        chain([
            dict(name="Error analysis",
                 does="Read the misclassified examples. Actually read them.",
                 code="wrong = X_cv[preds != y_cv]     # then sample ~100 and READ them",
                 trap="Let the categories <b>overlap</b> — one example can be in three. And "
                      "work on the biggest one that is also <b>tractable</b>: the largest "
                      "category is worthless if you have no idea how to fix it.",
                 feeds="a ranked list of what is actually wrong, rather than opinions."),
            dict(name="Data augmentation",
                 does="Make new training examples by distorting the ones you have.",
                 trap="One rule decides every case: <b>the distortion must be representative "
                      "of what really happens</b>. Caf&eacute; noise on speech, yes. Random "
                      "per-pixel noise on clean scans, no — a scanner never produces that. "
                      "Mirror-flipping handwritten digits, <b>no</b> — a mirrored 2 is not a 2, "
                      "and you are teaching it something false.",
                 feeds="more data, if you could not collect any."),
            dict(name="Transfer learning",
                 does="Start from somebody else's trained network instead of from random "
                      "numbers.",
                 trap="Replace <b>only the last layer</b> — everything before it learned "
                      "generic structure. Freeze the body for a tiny dataset; fine-tune "
                      "everything for a larger one, and <b>drop the learning rate</b> when "
                      "you unfreeze, or one large step destroys what somebody spent a "
                      "fortune learning.",
                 feeds=None),
        ]),

        h2("⚖️", "Two things the data cannot decide for you"),
        key("""<p><b>The threshold.</b> Raise it and precision rises while recall falls — use
that when a false alarm is expensive. Lower it and the reverse — use that when a miss is much
worse. <b>The right answer depends on what an action costs</b>, which is a question about the
world, not about the model.</p>
<p><b>Whether 92.4% is good.</b> Measure performance <b>per subgroup</b>. Aggregate accuracy
hides subgroup failure <b>by construction</b>: a group that is 6% of your data can be served
terribly and move the headline by under a point. And removing the sensitive attribute does not
fix it — the model finds proxies and reconstructs the group anyway.</p>"""),

        h2("🕳", "Three ways a split can silently lie"),
        trap("""<p><b>Splitting after sorting</b> — the halves are different populations.
Shuffle first, unless it is a time series, where you must split <b>by time</b>.</p>
<p><b>Duplicate entities</b> — the same house, patient or user in both sets. The model
recognises rather than generalises.</p>
<p><b>Scaling before splitting</b> — &mu; and &sigma; saw the test set.</p>
<p>What they share: your test score comes out <b>too good</b>, you ship confidently, and the
model underperforms in production for reasons nobody can reproduce. A suspiciously excellent
test score deserves suspicion, not celebration.</p>"""),

        h2("🗣", "Say the week back"),
        retell([
            "Which number tells you about bias and which about variance.",
            "Why three splits and not two, in one sentence about bias.",
            "The six fixes, and the rule that means you never have to memorise which is which.",
            "When more data does not help, and why that matters commercially.",
            "Why &ldquo;J_train = 10.8%&rdquo; is meaningless on its own, and the two gaps.",
            "How to read a learning curve — and why J_train rising is healthy.",
            "The two-question neural network recipe, and why &ldquo;go bigger&rdquo; is safe.",
            "The five steps of error analysis, and why categories should overlap.",
            "The one rule for data augmentation, and a case it rules out.",
            "Freeze vs fine-tune, and what decides between them.",
            "Precision vs recall — the trick with the denominators.",
            "Why accuracy is useless on a 0.5%-positive dataset.",
            "Why F1 uses the harmonic mean and not the ordinary one.",
        ]),

        h2("🪜", "Where this week sits in the whole arc"),
        ladder("C2 W3", """No new algorithm, and quite possibly the week with the highest
return per hour in the whole specialization. Every other week makes your models <b>better</b>;
this one makes your <b>decisions</b> better, and decisions compound. It is also the week that
transfers furthest outside this course: bias/variance, baselines, error analysis and leakage
apply identically to a decision tree, a transformer, or a fine-tuned language model."""),
    ]),
)
