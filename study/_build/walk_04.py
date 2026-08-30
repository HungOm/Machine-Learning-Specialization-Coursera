# -*- coding: utf-8 -*-
"""Line-by-line walkthrough for 04_backprop.py."""
from walkkit import p, expr, chain, chainset, steps, cases, values, point, ascii_art

PICTURE = ([
    ("in", "One batch of examples", "Together with the answers you want."),
    ("arw", "forward &mdash; and KEEP everything you compute"),
    ("op", "Forward pass",
     "Layer by layer to the output. Every intermediate value is stored, because the "
     "backward pass will need it."),
    ("arw", "compare with the truth"),
    ("op", "The cost", "One number."),
    ("arw", "now go backwards, starting from &part;J/&part;J = 1"),
    ("back", "Backward pass",
     "Walk the layers in <b>reverse</b>, multiplying by each one's local slope. Every "
     "weight's gradient falls out on the way."),
    ("arw", "one small step downhill"),
    ("back", "Update every weight", "And round again."),
    ("arw", "the cost stops falling"),
    ("out", "A trained network", "XOR, which no straight line can solve."),
], "The whole program in one picture",
   "File 03 was the forward arrow only. This file adds the backward one, and the backward "
   "arrow is the entire reason deep learning is possible.")

WALK = {

"prelude": (
    p("""Forward propagation asks: <b>what did the network predict?</b> Backpropagation asks
the other question: <b>which weight caused the mistake, and by how much?</b>""")
    + point("""This file derives every gradient <b>by hand</b>, checks each one numerically,
and then uses them to train a network on <b>XOR</b> &mdash; the smallest problem a straight
line cannot solve.""")
),

"one_node": (
    p("""Before touching a network, do the whole thing on <b>one node</b>, where you can
follow every number.""")
    + steps(["Forward: with the given w, b and x, the node outputs <b>a = 7.0</b>, and the "
             "cost comes out <b>J = 4.0</b>.",
             "Backward: <b>&part;J/&part;a = 4.0</b> &mdash; how much J moves if a moves.",
             "Then <b>&part;J/&part;w = 8.0</b> and <b>&part;J/&part;b = 4.0</b>, by "
             "multiplying along the path.",
             "Check it numerically: nudge w, measure. <b>8.0</b>. <b>Matches.</b>"])
    + point("""Notice the direction. The forward pass went <b>left to right</b> and produced
one number. The backward pass starts at that number and goes <b>right to left</b>, and each
step is just a multiplication by a local slope.""")
    + p("""Everything after this is the same four steps with more nodes. Nothing new is
introduced &mdash; only more of it.""")
),

"derivatives": (
    p("""Backprop needs the slope of every activation function. The sigmoid's has a
famously tidy form &mdash; and a famous problem.""")
    + expr("g'(z) = g(z) &middot; (1 - g(z))",
           "the slope, computed from the OUTPUT you already have")
    + values([("output 0.1", "slope 0.0900", "near the flat left end"),
              ("output 0.5", "slope 0.2500", "the steepest it ever gets"),
              ("output 0.9", "slope 0.0900", "near the flat right end")],
             "the sigmoid's slope at three points")
    + point("""Two things to take from those numbers. First, you never need z &mdash; the
slope is computable from the activation the forward pass already stored, which is why
forward values are kept.""")
    + p("""Second, and much more important: <b>the slope peaks at 0.25 and vanishes at both
ends</b>. Every layer multiplies the gradient by at most 0.25. Stack ten sigmoid layers and
the first one receives at most <b>0.25<sup>10</sup> &asymp; 0.00000095</b> of the
signal.""")
    + point("""That is the <b>saturation problem</b>, and it is exactly what ReLU was
introduced to avoid: ReLU's slope on the positive side is exactly <b>1</b>, so gradients
pass through undiminished however deep the stack.""")
),

"forward": (
    p("""The forward pass, written so that it <b>returns its intermediates</b> rather than
just the answer.""")
    + point("""That is the only difference from file 03. The backward pass needs every
value the forward pass computed, so the forward pass must hand them back rather than
throwing them away.""")
    + p("""This is also why <b>training uses far more memory than prediction</b>. A
prediction can discard each layer's output as soon as the next layer has consumed it;
training cannot discard anything until the backward pass has been all the way through. When
you run out of GPU memory, this is why, and halving the batch size is the first thing to
try.""")
),

"backward": (
    p("""The backward pass. Read it as the chain rule, walked from the end.""")
    + steps(["Start at the output with <b>&part;J/&part;J = 1</b>.",
             "At each layer, multiply by that layer's <b>local slope</b> &mdash; how much "
             "its output moves when its input moves.",
             "On the way past each weight, that running product <b>is</b> that weight's "
             "gradient.",
             "Pass what is left to the layer before, and repeat."])
    + point("""The key insight: <b>each node only needs to know its own little
multiplier</b>. No node knows anything about the network as a whole, and none of them needs
to. The chain rule assembles the global answer out of purely local facts.""")
    + p("""And this is why it is cheap. <b>One forward pass plus one backward pass</b> gives
you <b>every</b> gradient, no matter how many parameters there are. Nudging each parameter
separately would cost one forward pass <b>each</b> &mdash; a million passes for a million
parameters, instead of two.""")
),

"gradcheck": (
    p("""Every hand-derived gradient, checked against a numerical measurement. This is the
block that makes the rest trustworthy.""")
    + values([("dW1", "7.6e&minus;11", "PASS"),
              ("db1", "7.2e&minus;11", "PASS"),
              ("dW2", "8.1e&minus;11", "PASS"),
              ("db2", "3.2e&minus;11", "PASS")],
             "max absolute difference between hand-derived and numerical")
    + point("""<b>Eleven decimal places.</b> That is the noise floor of floating-point
arithmetic, not agreement-by-luck. The hand-derived calculus is right.""")
    + p("""Do this on any network you write by hand, once, before training. A wrong gradient
<b>does not crash</b> &mdash; it trains, converges to something, and quietly gives you a
worse model than you should have had. There is no other symptom.""")
    + point("""Turn it <b>off</b> before real training, though. The numerical version
re-runs the entire cost twice per parameter, which is exactly the cost backprop exists to
avoid.""")
),

"relu_kink": (
    p("""Now the interesting failure. This block deliberately sets the biases to exactly
zero and re-runs the check.""")
    + values([("analytic", "[0.117, 0, &minus;0.002, 0, 0.145, 0.126, &minus;0.001, &minus;0.011]", ""),
              ("numeric", "[0.086, 0.024, 0.062, &minus;0.051, 0.091, 0.079, 0.025, &minus;0.007]", ""),
              ("max difference", "6.4e&minus;02", "<b>a REAL disagreement</b>")],
             "the same check, now failing")
    + point("""This is not a bug in either version. <b>ReLU has no derivative at exactly
z = 0.</b> It is a kink: the slope is 0 on one side and 1 on the other, and at the point
itself there is no single answer.""")
    + cases([("The analytic version", "picks the <b>flat side</b> &mdash; it applies the "
                                      "rule <code>z &gt; 0</code>, so z = 0 counts as 0."),
             ("The numeric version", "<b>averages across the kink</b> &mdash; it steps to "
                                     "both sides and divides, landing somewhere in "
                                     "between.")],
            "two defensible answers to a question with no answer")
    + point("""<b>Neither is wrong.</b> And in practice it does not matter: hitting z
<i>exactly</i> zero has probability zero once weights are random, and the failure here had to
be engineered by setting every bias to 0 deliberately.""")
    + p("""It is worth seeing, though, because it is the one situation where a gradient
check <b>fails on correct code</b> &mdash; and knowing that saves you from hunting a bug
that is not there.""")
),

"train": (
    p("""Now train it, on <b>XOR</b>: output 1 when exactly one input is 1.""")
    + values([("iter 0", "cost 0.954843", "knows nothing"),
              ("iter 2000", "cost 0.000245", "essentially solved"),
              ("iter 4000", "cost 0.000109", ""),
              ("iter 8000", "cost 0.000049", "polishing")],
             "training")
    + point("""The cost falls by a factor of about <b>4,000</b> in the first 2,000
iterations. Everything after that is refinement &mdash; the same enormous-drop-then-flatten
shape as file 01, which is what a healthy run looks like at any scale.""")
    + p("""XOR is the classic choice here because it is the smallest problem that is
<b>provably impossible</b> for a single linear boundary. Solving it is a real
demonstration, not a formality.""")
),

"why_hidden": (
    p("""The control experiment, and the punchline of the file. Same problem, same training,
<b>no hidden layer</b> &mdash; which makes it plain logistic regression.""")
    + values([("predictions", "[0.5, 0.5, 0.5, 0.5]", "all four stuck at exactly 0.5"),
              ("accuracy", "0.50", "no better than a coin flip")],
             "logistic regression on XOR")
    + point("""It does not do <i>badly</i>. It does <b>nothing</b> &mdash; every prediction
is 0.5, which is the model announcing it has no idea. And it is not a training failure: no
straight line exists that separates XOR, so there is no better answer for it to find.""")
    + chainset([([" with a hidden layer ", "cost 0.00005"], "solved"),
                ([" without one ", "accuracy 0.50"], "impossible")],
               "the same problem, the same training loop")
    + point("""<b>The hidden layer is not an optimisation. It is what makes the problem
solvable at all.</b> That is the difference between Course 1 and Course 2, demonstrated in
four numbers.""")
),
}
