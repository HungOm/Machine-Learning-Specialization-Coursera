# -*- coding: utf-8 -*-
"""Reusable formula-PART explanations, for kit.eqp() (the colour-coded,
click-to-explain formula rendering).

Different in kind from content_f0ref / content_courseref / content_apiref:
those three are found automatically by scanning rendered text for a pattern.
These are never auto-badged — PATTERNS is empty on purpose — because a
fragment like "the error term" or "1/2m" is too generic and too structurally
different formula to formula to ever safely pattern-match in prose. Instead
an eqp() call in a lesson names one of these keys directly, once per
sub-expression, wherever that specific formula appears.

The point of keeping these keys SHARED rather than one-off per formula: the
error term in linear regression's cost function and logistic regression's
are the same underlying idea, so they should pop the same explanation and
feel like the same recurring concept, not two different write-ups a learner
has to reconcile.
"""

ANCHOR = "formulaparts"
PATTERNS = []  # never auto-badged — see module docstring

F0W1 = "f0/w1-%s.html"
C1 = "c1/w%s-%s.html"
C3 = "c3/w%s-%s.html"

TERMS = [
 dict(key="cost-j", label="J(w,b)", say="“the cost”",
      gist="One number saying how wrong the model currently is — smaller is better, and training "
           "means searching for the w and b that make this as small as possible.",
      body="<p>Every cost function in this specialization does the same job with a different "
           "formula underneath: turn “how good is this model” into one comparable number.</p>",
      ml="J for squared error (C1), log loss for classification (C1 W3), and the same shape of "
         "idea for a neural network, k-means, or PCA — always a single number, always smaller-is-better.",
      more_href=C1 % (1, "05-cost-function-formula"), more_label="C1 W1 · The cost function formula"),

 dict(key="avg-factor", label="1/m", say="“divide by m”, or “1/2m”",
      gist="Turns a sum over every training example into an <b>average</b>, so the cost doesn't "
           "simply grow the moment you collect more data.",
      body="<div class='gq'>total error &nbsp;÷&nbsp; m &nbsp;=&nbsp; average error</div>"
           "<p>Without this, a model scored on 10,000 examples would always look “worse” than the "
           "same model scored on 100 — not because it fits worse, just because there is more to "
           "add up. Sometimes written 1/2m instead of 1/m — see “squared” for why the 2 is there.</p>",
      ml="Every cost function in this specialization divides by m (or 2m) for exactly this reason.",
      more_href=C1 % (1, "05-cost-function-formula"), more_label="C1 W1 · The cost function formula"),

 dict(key="error-term", label="f(x) − y", say="“predicted minus actual”",
      gist="How wrong the model was on <b>one</b> example — positive if it guessed too high, "
           "negative if too low.",
      body="<div class='gq'>guess 250, actual 280 &nbsp;→&nbsp; 250 − 280 = −30 (too low)</div>"
           "<p>Every cost function in this specialization is built from exactly this difference, "
           "repeated once per training example and combined some way — squared, or fed through a "
           "log.</p>",
      ml="Same order every time: <b>prediction first, actual second</b>. Reverse it and every sign "
         "flips, which silently breaks which direction gradient descent steps.",
      more_href=C1 % (1, "05-cost-function-formula"), more_label="C1 W1 · The cost function formula"),

 dict(key="squared-term", label="( … )²", say="“squared”",
      gist="Makes every error positive, and makes big misses hurt disproportionately more than "
           "small ones.",
      body="<p>Being off by 10 counts a hundred times worse than being off by 1 — not ten times "
           "worse. Squaring is also what puts the 2 in 1/2m: differentiating a square brings down "
           "a factor of 2 that this cancels exactly, which is the entire reason the 2 is there.</p>",
      ml="Swap squared error for log loss (C1 W3) and this exact role — punish confident, "
         "wrong answers hard — is instead played by −log(f).",
      more_href=C1 % (1, "05-cost-function-formula"), more_label="C1 W1 · The cost function formula"),

 dict(key="assign-op", label=":=", say="“becomes”, not “equals”",
      gist="An instruction to overwrite a value, not a mathematical claim that two things are equal.",
      body="<p><code>w := w − 1</code> is perfectly sensible as an instruction — subtract 1 from "
           "w's current value — while <code>w = w − 1</code> is mathematically false for any w. "
           "Code just writes it as <code>=</code> and relies on you knowing which meaning is meant.</p>",
      ml="Every parameter update in this specialization — linear regression, logistic regression, "
         "every neural network — is this same kind of overwrite, not an equation to solve.",
      more_href=C1 % (1, "09-implementing-gradient-descent"),
      more_label="C1 W1 · Implementing gradient descent"),

 dict(key="alpha-lr", label="α", say="“alpha”, the learning rate",
      gist="How big a step to take — a hyperparameter you choose, not something gradient descent "
           "learns on its own.",
      body="<p>Too small and training crawls. Too large and it overshoots, oscillates, or diverges "
           "outright. There is no formula that hands you the right value — the standard approach "
           "is to try a ladder (0.001, 0.003, 0.01, 0.03, …) and watch what J does.</p>",
      ml="The single most-tuned hyperparameter in this specialization — identical role whether "
         "the model is linear regression or a deep network.",
      more_href=C1 % (1, "11-learning-rate"), more_label="C1 W1 · The learning rate"),

 dict(key="reg-penalty", label="λ Σ w²", say="“the regularization penalty”",
      gist="An extra cost for having <b>large</b> weights, added on top of the ordinary cost — the "
           "lever that discourages a model from overfitting.",
      body="<div class='gq'>J(w,b) + λ · (sum of the weights, squared)</div>"
           "<p>Turn λ up and the model is pushed towards smaller weights and a simpler fit; turn "
           "it up far enough and it can barely fit anything at all.</p>",
      ml="Identical formula, same λ, unchanged when the model becomes logistic regression or a "
         "neural network — only which weights get summed changes.",
      more_href=C1 % (3, "10-cost-function-with-regularization"),
      more_label="C1 W3 · The cost function with regularization"),

 dict(key="sigmoid-squash", label="g(z)", say="“the sigmoid”",
      gist="Squashes any real number into a probability between 0 and 1 — very negative in, "
           "near 0 out; very positive in, near 1 out.",
      body="<div class='gq'>g(z) = 1 / (1 + e<sup>−z</sup>)</div>"
           "<p>g(0) = 0.5 exactly — the undecided point. The bigger |z| gets, the closer g(z) sits "
           "to 0 or 1, but it never quite reaches either.</p>",
      ml="This one function is what turns linear regression into logistic regression, and it "
         "reappears as the standard activation for a single output unit throughout Course 2.",
      more_href=F0W1 % "14-exponentials", more_label="F0 W1 · Exponentials and e"),

 dict(key="times-xi", label="· x⁽ⁱ⁾", say="“times that example's x”",
      gist="The one piece that makes this the derivative <b>with respect to w</b> rather than b — "
           "b's derivative is identical except this factor is missing.",
      body="<p>A change in w affects a large-x example more than a small-x one — an x = 4 house "
           "responds four times as much as an x = 1 house — so large-x examples pull harder on "
           "w's gradient. b shifts every prediction by the same fixed amount, so every example "
           "gets an equal vote and no such factor appears.</p>",
      ml="The same asymmetry shows up every time a w-derivative and a b-derivative are compared "
         "side by side — logistic regression, a neural network layer, all of them.",
      more_href=C1 % (1, "12-gradient-descent-for-linear-regression"),
      more_label="C1 W1 · Gradient descent for linear regression"),

 dict(key="sq-distance", label="‖a − b‖²", say="“squared distance”",
      gist="How far apart two points are, squared — the same “punish big misses harder” shape as "
           "squared error, just measuring distance instead of prediction error.",
      body="<div class='gq'>‖a − b‖² = (a₁−b₁)² + (a₂−b₂)² + …</div>"
           "<p>Pythagoras with more terms. Squaring (rather than using plain distance) is what makes "
           "the point that minimises the total exactly the <b>mean</b> of a set of points.</p>",
      ml="K-means' cost and the “how far is this point from normal” score in anomaly detection are "
         "both built from this same shape.",
      more_href=F0W1 % "09-vectors", more_label="F0 W1 · Vectors"),

 dict(key="q-function", label="Q(s,a)", say="“the Q function”",
      gist="How good it is to take action <b>a</b> from state <b>s</b> — reward right now, plus the "
           "best you can still do afterwards.",
      body="<p>Every reinforcement learning algorithm on this site is, underneath, a strategy for "
           "getting an estimate of Q to satisfy the Bellman equation.</p>",
      ml="Once you have Q, the best policy is simple: from any state, take whichever action has the "
         "highest Q.",
      more_href=C3 % (3, "06-state-action-value-function"),
      more_label="C3 W3 · State-action value function"),

 dict(key="reward-r", label="R(s)", say="“the reward”",
      gist="What you collect immediately for being in this state — the one part of the equation "
           "that needs no lookahead at all.",
      body="<p>Purely local: R(s) depends only on the current state, never on what happens next.</p>",
      ml="Designing R is most of the actual work of setting up a reinforcement learning problem — "
         "get the rewards wrong and the agent optimises for the wrong thing.",
      more_href=C3 % (3, "08-bellman-equation"), more_label="C3 W3 · The Bellman equation"),

 dict(key="gamma-discount", label="γ", say="“gamma”, the discount factor",
      gist="How much a future reward is worth <b>today</b> — a number just under 1, so a reward "
           "later is worth slightly less than the same reward now.",
      body="<div class='gq'>γ = 0.9 &nbsp;→&nbsp; a reward 10 steps away is worth 0.9¹⁰ ≈ 35% of its full value</div>",
      ml="γ close to 1 makes the agent patient (values long-term reward); γ close to 0 makes it "
         "greedy for whatever is immediate.",
      more_href=C3 % (3, "08-bellman-equation"), more_label="C3 W3 · The Bellman equation"),

 dict(key="future-value", label="max Q(s′,a′)", say="“the best you can do from there”",
      gist="The value of the state you land in — assuming you play optimally from that point "
           "onward.",
      body="<p>This is exactly V(s′), written out. The whole Bellman equation is recursive because "
           "this piece is itself defined by the same equation, one step further along.</p>",
      ml="This is the piece every RL algorithm is really estimating — you never get to see it "
         "directly, only build up a better and better guess of it through experience.",
      more_href=C3 % (3, "08-bellman-equation"), more_label="C3 W3 · The Bellman equation"),

 dict(key="func-f", label="f(x)", say="“f of x”",
      gist="Put x into the machine named f, and read off what comes out. <b>Not</b> f multiplied by x.",
      body="<p>f(3) means “run the rule for f, using 3”, not “f times 3”. The brackets mean "
           "<b>applied to</b>, never multiplication — the single most common misreading of this "
           "notation.</p>",
      ml="Every model in this specialization — f(x) = wx+b, f(x) = g(w·x+b), a whole neural "
         "network — is this same idea: a name for a rule, with an input in brackets.",
      more_href=F0W1 % "01-what-is-a-function", more_label="F0 W1 · What a function is"),

 dict(key="adam-moments", label="m, v", say="“the running averages”",
      gist="Adam's memory of recent gradients — m tracks their average <b>direction</b>, v tracks "
           "their average <b>size</b>, both updated a little every step rather than recomputed from "
           "scratch.",
      body="<p>β₁ and β₂ (typically 0.9 and 0.999) decide how much of the old average survives each "
           "update versus how much the newest gradient counts.</p>",
      ml="v being large means this parameter's gradient has been erratic recently, which is exactly "
         "the signal Adam uses to shrink that parameter's effective step size.",
      more_href="c2/w2-11-advanced-optimization.html",
      more_label="C2 W2 · Advanced optimization (Adam)"),
]
