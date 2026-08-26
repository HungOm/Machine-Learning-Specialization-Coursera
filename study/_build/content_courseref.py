# -*- coding: utf-8 -*-
"""Quick-refresher badges for vocabulary the COURSE itself defines.

content_f0ref.py cross-references pure notation taught in Foundations. This
module is its sibling for the other half of the problem: terms C1-C3 coin and
explain once, then reuse without re-explaining for the rest of the
specialization — "training example", "hyperparameter", "convergence",
"one-hot", "epoch", "regularisation", "softmax", "cross-entropy",
"precision"/"recall". By lesson 80 the definition from lesson 9 is a long
scroll away; the badge is the shortcut back to it.

Some patterns here are deliberately longer/more specific than a same-word
pattern in content_f0ref.py, so they win the alternation and route to the
right sense of an overloaded word — e.g. "log loss" and "high variance" are
checked before the bare "log" / "variance" they contain.
"""

ANCHOR = "courseref"

C1 = "c1/w%s-%s.html"
C2 = "c2/w%s-%s.html"

PATTERNS = [
    (r"\bReLU\b", "relu-native"),
    (r"\bhigh variance\b|\bhigh bias\b|\bbias[/\s-]variance\b", "bias-variance-native"),
    (r"\blog loss\b", "logloss-native"),
    (r"cross-entropy", "crossentropy-native"),
    (r"one-hot(?:\s*encod\w*)?", "onehot-native"),
    (r"regulari[sz]ation", "regularization-native"),
    (r"\boverfitting\b|\boverfit\b", "overfitting-native"),
    (r"\bhyperparameters?\b", "hyperparameter-native"),
    (r"\bconvergence\b|\bconverges?\b|\bconverged\b|\bconverging\b", "convergence-native"),
    (r"\btraining examples?\b", "trainingexample-native"),
    (r"\bmini-batch(?:es)?\b", "minibatch-native"),
    (r"\bsoftmax\b", "softmax-native"),
    (r"\bepochs?\b", "epoch-native"),
    (r"\bprecision\b|\brecall\b", "precisionrecall-native"),
]

TERMS = [
 dict(key="trainingexample-native", label="x⁽ⁱ⁾", say="“x superscript i, in round brackets”",
      gist="One row of the training set — the i-th example. The round brackets are the tell: they "
           "always mean “which example”, never a power.",
      body="<div class='gq'>x⁽²⁾ = the 2nd training example &nbsp;·&nbsp; x² = x squared</div>"
           "<p>Same-looking superscript, two completely different jobs. Round brackets = which "
           "example. No brackets = an actual power. Square brackets (seen from Course 2 on) = which "
           "layer.</p>",
      ml="Every Σ in this specialization loops i from 1 to m over exactly these — one pass per "
         "training example.",
      more_href=C1 % (1, "04-linear-regression-model"),
      more_label="C1 W1 · The linear regression model"),

 dict(key="hyperparameter-native", label="hyperparameter", say="“hyper-parameter”",
      gist="A setting <b>you</b> choose before training starts — not something gradient descent learns.",
      body="<p>w and b are parameters: the data determines them. The learning rate α is a "
           "hyperparameter: you pick it, and a bad choice is a you-problem, not a data problem.</p>",
      ml="Every knob you turn without running gradient descent on it — α, the number of layers, "
         "λ, k in k-means — is a hyperparameter.",
      more_href=C1 % (1, "11-learning-rate"), more_label="C1 W1 · The learning rate"),

 dict(key="convergence-native", label="converged", say="“con-verged”",
      gist="Training has stopped making meaningful progress — J has flattened out.",
      body="<p>Not the same as “finished successfully”. A run can converge to a mediocre answer just "
           "as easily as a good one; convergence only says the numbers stopped moving, not that "
           "they stopped somewhere good.</p>",
      ml="The plot-J-against-iterations habit exists specifically to let you see convergence happen, "
         "rather than guessing at how many iterations are “enough”.",
      more_href=C1 % (1, "09-implementing-gradient-descent"),
      more_label="C1 W1 · Implementing gradient descent"),

 dict(key="minibatch-native", label="mini-batch", say="“mini-batch”",
      gist="A small, random slice of the training set — the practical middle ground between using "
           "all m examples per step and using just one.",
      body="<div class='gq'>batch: all m &nbsp;·&nbsp; mini-batch: ~32&ndash;512 &nbsp;·&nbsp; stochastic: 1</div>"
           "<p>More examples per step means a smoother, more reliable gradient but a slower step. "
           "Mini-batch trades a little noise for a lot of speed.</p>",
      ml="Effectively all deep learning trains this way — including every neural network built later "
         "in this specialization.",
      more_href=C1 % (1, "13-running-gradient-descent"),
      more_label="C1 W1 · Running gradient descent"),

 dict(key="overfitting-native", label="overfitting", say="“over-fitting”",
      gist="A model that has memorised the noise in the training data rather than the pattern "
           "underneath it — great on the data it has seen, bad on data it hasn't.",
      body="<p>The tell: training performance is excellent and performance on new examples is not. "
           "A model too simple to capture the pattern at all is the opposite problem, "
           "<b>underfitting</b>.</p>",
      ml="Regularisation, more data, and simpler models are the three standard fixes — Course 2 "
         "Week 3 turns diagnosing which one you need into a repeatable procedure.",
      more_href=C1 % (3, "08-the-problem-of-overfitting"),
      more_label="C1 W3 · The problem of overfitting"),

 dict(key="regularization-native", label="regularisation", say="“reg-you-lar-eye-zay-shun”",
      gist="Discouraging large weights during training, so the model can't lean too hard on any one "
           "feature — a direct lever against overfitting.",
      body="<div class='gq'>J(w,b) + &lambda;·(sum of the weights squared)</div>"
           "<p>Adds a penalty for big weights to the ordinary cost. Turn &lambda; up and the model is "
           "pushed towards simpler, smaller-weight solutions; turn it up too far and it can't fit "
           "anything at all.</p>",
      ml="The exact same idea, same &lambda;, reappears unchanged for logistic regression and every "
         "neural network in Course 2.",
      more_href=C1 % (3, "10-cost-function-with-regularization"),
      more_label="C1 W3 · The cost function with regularization"),

 dict(key="onehot-native", label="one-hot", say="“one-hot”",
      gist="Turning a category into several 0/1 columns — one column per possible value, exactly "
           "one of them set to 1.",
      body="<div class='gq'>colour ∈ {red, green, blue} &nbsp;→&nbsp; [1,0,0], [0,1,0], [0,0,1]</div>"
           "<p>Fixes the mistake of encoding categories as 1, 2, 3, which would falsely tell the "
           "model that blue is “between” red and green.</p>",
      ml="Standard prep step before feeding a categorical feature into linear regression, logistic "
         "regression, or a neural network — none of which can read a raw category.",
      more_href=C2 % (4, "06-one-hot-encoding"),
      more_label="C2 W4 · Using one-hot encoding of categorical features"),

 dict(key="softmax-native", label="softmax", say="“soft-max”",
      gist="Turns a list of raw scores into a list of probabilities that add up to exactly 1 — the "
           "multi-class version of the sigmoid.",
      body="<div class='gq'>softmax(z)ᵢ = eᶻⁱ ÷ Σ eᶻʲ</div>"
           "<p>Every output is positive and the whole list sums to 1, so each entry can be read "
           "directly as “the model's probability this is class i”.</p>",
      ml="The output layer for any neural network choosing between more than two classes — "
         "handwritten digits, this course's own worked example, uses 10 softmax outputs.",
      more_href=C2 % (2, "07-softmax"), more_label="C2 W2 · Softmax"),

 dict(key="logloss-native", label="log loss", say="“log loss”",
      gist="The cost function for classification — a large penalty for a confident wrong answer, "
           "almost no penalty for a confident right one.",
      body="<div class='gq'>y = 1: −log(f) &nbsp;&nbsp;·&nbsp;&nbsp; y = 0: −log(1 − f)</div>"
           "<p>Predict 0.99 for the true class and the penalty is tiny. Predict 0.01 for the true "
           "class and it is enormous — that asymmetry is the entire point.</p>",
      ml="Same formula as binary cross-entropy — two names for one thing, used interchangeably "
         "from here on.",
      more_href=C1 % (3, "05-logistic-loss"), more_label="C1 W3 · The logistic loss, in detail"),

 dict(key="crossentropy-native", label="cross-entropy", say="“cross-entropy”",
      gist="The general name for log loss — “binary” cross-entropy for two classes, plain "
           "cross-entropy for more.",
      body="<p>Same idea as log loss, extended: penalise the model in proportion to how far its "
           "predicted probability was from being confidently correct, for whichever class the "
           "example actually belongs to.</p>",
      ml="TensorFlow's <code>BinaryCrossentropy</code> and <code>SparseCategoricalCrossentropy</code> "
         "loss functions are exactly this, by name.",
      more_href=C2 % (2, "07-softmax"), more_label="C2 W2 · Softmax"),

 dict(key="epoch-native", label="epoch", say="“epoch”",
      gist="One full pass of gradient descent over the <b>entire</b> training set.",
      body="<div class='gq'>model.fit(X, Y, epochs=100)</div>"
           "<p>100 epochs does not mean 100 gradient descent steps if you're using mini-batches — it "
           "means 100 full sweeps, each made of several smaller steps.</p>",
      ml="Too few epochs and training stops before it's learned; too many and it starts memorising "
         "the training set — the same overfitting trade-off, on a different dial.",
      more_href=C2 % (2, "01-tensorflow-training"),
      more_label="C2 W2 · TensorFlow implementation of training"),

 dict(key="precisionrecall-native", label="precision / recall", say="“precision”, “recall”",
      gist="Two different questions about a classifier's mistakes on a skewed dataset, where plain "
           "accuracy can lie.",
      body="<div class='gq'>precision: of what I flagged, how much was right?</div>"
           "<div class='gq'>recall: of what was actually true, how much did I catch?</div>"
           "<p>A model that never flags anything scores well on accuracy (if the condition is rare) "
           "and zero on recall — which is why precision/recall exist.</p>",
      ml="F1 combines both into one number when you need a single score to compare models by.",
      more_href=C2 % (3, "16-skewed-datasets"),
      more_label="C2 W3 · Error metrics for skewed datasets"),

 dict(key="bias-variance-native", label="bias / variance", say="“bias”, “variance”",
      gist="Two different failure modes for a model, borrowing (loosely) the language of statistical "
           "variance — <b>not</b> the same calculation as σ².",
      body="<p><b>High bias</b> (underfitting): too simple to capture the pattern, wrong even on "
           "training data.</p><p><b>High variance</b> (overfitting): so flexible it fits the "
           "training data's noise, and would fit a different sample completely differently — "
           "\"sensitive to which examples you happened to train on\" is the sense of \"variance\" "
           "meant here, not the spread-around-a-mean formula.</p>",
      ml="Diagnosing which one you have decides the fix: high bias wants a bigger model or more "
         "features; high variance wants more data, regularisation, or a simpler model.",
      more_href=C2 % (3, "04-bias-and-variance"),
      more_label="C2 W3 · Bias and variance"),

 dict(key="relu-native", label="ReLU(z)", say="“ray-luh”",
      gist="Below zero, output exactly 0. Above zero, output the input unchanged. That's the "
           "whole function.",
      body="<div class='gq'>ReLU(z) = max(0, z)</div>"
           "<p>No exponentials, no division — just a single comparison — which is part of why it "
           "trains faster than sigmoid.</p>",
      ml="The default activation for hidden layers in this specialization. Sigmoid is mostly "
         "reserved for a binary output layer now.",
      more_href=C2 % (2, "03-sigmoid-alternatives"),
      more_label="C2 W2 · Alternatives to the sigmoid activation"),
]
