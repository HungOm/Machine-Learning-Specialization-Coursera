# -*- coding: utf-8 -*-
"""The gist of C2 Week 2."""
import math
import numpy as np
from kit import key, trap
from gistkit import gistline, flow, sameskel, chain, bynumbers, retell, ladder, h2
from walkkit import cases, values, point, expr, chainset

_z = np.array([1., 2, 3, 4]); _e = np.exp(_z); _p = _e / _e.sum()

def _n(v, p=4):
    s = "%.*f" % (p, v)
    return s.rstrip("0").rstrip(".") if "." in s else s

GIST = dict(
    course="C2", week="2", title="Neural Network Training", mins=13,
    scratch=["04-backpropagation", "05-softmax"],
    lede="The other half. Fifteen lessons on where the weights come from, which activation "
         "to use where, and how to answer a question with more than two options.",
    body="".join([
        gistline("""Last week computed what a network outputs. This week works out
<b>which weight caused the mistake</b> — and the answer, backpropagation, costs about two
passes no matter how many parameters there are. That cost is the entire reason deep learning
is possible."""),

        h2("🖼", "The week in one picture"),
        flow([
            ("in", "A batch, and the answers you want", ""),
            ("arw", "forward &mdash; and KEEP every intermediate value"),
            ("op", "Forward pass",
             "Layer by layer to the output. Everything computed is stored, because the "
             "backward pass will need it."),
            ("arw", "score it"),
            ("op", "The loss",
             "Binary cross-entropy for yes/no, <b>softmax + cross-entropy</b> for "
             "one-of-many."),
            ("arw", "now go backwards, starting from &part;J/&part;J = 1"),
            ("back", "Backward pass",
             "Walk the layers in <b>reverse</b>, multiplying by each one's local slope. "
             "Every weight's gradient falls out on the way."),
            ("arw", "and take the step cleverly, not plainly"),
            ("back", "Adam",
             "A separate, adapting learning rate for <b>every</b> parameter."),
            ("arw", "repeat"),
            ("out", "A trained network", ""),
        ], cap="""The three lines of TensorFlow map exactly onto Course 1:
<code>Sequential</code> is the model, <code>compile(loss=)</code> is the cost,
<code>fit</code> is gradient descent. Only <code>fit</code> changes any weights."""),

        h2("🔁", "Same skeleton, and what changed"),
        sameskel("""<b>Predict → measure the miss → find the slopes → step downhill →
repeat.</b> Still true, at every scale. What changes is <i>how</i> the slopes are found and
<i>how</i> the step is taken.""",
                 [("Finding the gradient", "one formula, differentiated by hand",
                   "<b>backpropagation</b> — the chain rule, walked backwards"),
                  ("Cost of the gradient", "trivial", "1 forward + 1 backward pass, "
                                                      "<b>regardless of parameter count</b>"),
                  ("Hidden activation", "&mdash;", "<b>ReLU</b>, almost always"),
                  ("Output for one-of-N", "&mdash;", "<b>softmax</b> — coupled outputs "
                                                     "summing to 1"),
                  ("The step", "w &minus; &alpha;&middot;grad", "<b>Adam</b> — a per-parameter, "
                                                                "adapting &alpha;"),
                  ("Memory used", "negligible", "<b>large</b> — every forward value is kept")]),

        h2("⛓", "The pieces, in the order they hand to each other"),
        chain([
            dict(name="Backpropagation",
                 does="Compute every gradient by walking the chain rule from the output "
                      "backwards, multiplying local slopes as you go.",
                 say="d J by d w equals the product of the local slopes along the path.",
                 code="dz2 = a2 - y\ndW2 = a1.T @ dz2 / m\ndz1 = (dz2 @ W2.T) * relu_grad(z1)",
                 trap="Each node only needs <b>its own little multiplier</b> — it knows "
                      "nothing about the network as a whole. And the forward values must be "
                      "kept, which is why <b>training uses far more memory than "
                      "prediction</b>, and why halving the batch size is the first fix when "
                      "you run out.",
                 feeds="every gradient, for about the price of two forward passes."),
            dict(name="ReLU",
                 does="max(0, z). Keeps positives, zeroes negatives.",
                 code="a = np.maximum(0, z)",
                 trap="A unit whose z is negative for <b>every</b> example has gradient 0 "
                      "forever, so its weights never update, so its z never changes. That is "
                      "a <b>dying ReLU</b>, and it is permanent. Lower the learning rate, or "
                      "use Leaky ReLU.",
                 feeds="gradients that survive depth — which sigmoid's do not."),
            dict(name="Softmax",
                 does="Turns a list of raw scores into probabilities that sum to exactly 1.",
                 say="a sub j equals e to the z j, over the sum of e to the z k.",
                 code="e = np.exp(z - np.max(z))\np = e / e.sum()",
                 trap="Subtracting the max is <b>not optional</b>. Softmax depends only on "
                      "the <b>differences</b> between scores, so subtracting a constant "
                      "changes nothing — and it makes overflow impossible. Without it, "
                      "[1000, 999, 998] returns <b>nan</b>.",
                 feeds="a probability per class — and a gradient that is startlingly simple."),
            dict(name="Adam",
                 does="A separate learning rate per parameter, raised when the gradient is "
                      "consistent and lowered when it flip-flops.",
                 code="model.compile(optimizer=Adam(learning_rate=1e-3), ...)",
                 trap="It is not magic — it is common sense automated. Noisy parameters get "
                      "small steps; steady ones get large steps.",
                 feeds=None),
        ]),

        h2("🔢", "Softmax, by hand"),
        bynumbers("""<b>z = [1, 2, 3, 4]</b>. Exponentiate, add, divide.""",
                  [("e&#185;, e&sup2;, e&sup3;, e&#8308;",
                    ", ".join("%.2f" % v for v in _e), "exponentiate each"),
                   ("their total", "%.2f" % _e.sum(), "the denominator"),
                   ("a&#8321;", "%.3f" % _p[0], "from z = 1"),
                   ("a&#8322;", "%.3f" % _p[1], ""),
                   ("a&#8323;", "%.3f" % _p[2], ""),
                   ("a&#8324;", "%.3f" % _p[3], "from z = 4"),
                   ("total", "%.1f" % _p.sum(), "as it must be")],
                  close="""Look at the exaggeration: z = 4 is only <b>4&times;</b> z = 1, but
its probability is <b>20&times;</b> larger. Exponentiating widens every gap, which is what
makes softmax decisive — and why a slightly wrong score can produce a very confident wrong
answer."""),

        h2("✨", "The two results worth carrying forward"),
        key("""<p><b>1. Without non-linear activations, depth buys nothing.</b> Two linear
layers multiply out to <b>W&#8322;W&#8321;</b>, which is just another matrix. A 100-layer
linear network is algebraically <b>identical</b> to one layer, and costs a hundred times as
much. Each ReLU adds a kink, and no amount of matrix multiplication flattens a kink out. The
build lane's file 03 shows the collapse numerically.</p>
<p><b>2. The gradient of softmax with cross-entropy is <code>p − y</code>.</b> No
exponentials, no logs. The softmax derivative carries a factor of <b>p</b> and the logarithm
contributes <b>1/p</b>; they annihilate. Same cancellation as sigmoid + log loss in C1 W3 —
which is why these are always used in matched pairs.</p>"""),

        h2("⚠️", "Where sigmoid fails, in one number"),
        chainset([(["sigmoid slope peaks at", "0.25"], "and is smaller nearly everywhere"),
                  (["stack 10 layers", "0.25&#185;&#8304; &asymp; 0.00000095"],
                   "what reaches the first layer"),
                  (["ReLU slope on the positive side", "exactly 1"],
                   "gradients pass through undiminished")],
                 "the vanishing gradient problem, quantified"),
        trap("""<p>That is why ReLU replaced sigmoid <b>in hidden layers</b> — not because it
is more expressive, but because gradients survive depth. Sigmoid is still correct at the
<b>output</b> of a binary classifier, where there is only one layer of it and it is producing
a probability rather than passing a gradient on.</p>
<p>The related trap is <code>from_logits=True</code>: it tells the loss to take <b>raw
scores</b> and apply the squash itself, using a rearranged formula that never builds the
intermediate probability — so nothing can round to 0 or 1 and produce an infinite log. But
your output layer must then actually be <b>linear</b>. Leave a sigmoid on it as well and the
squash is applied twice. It trains, badly, and nothing warns you.</p>"""),

        h2("🗣", "Say the week back"),
        retell([
            "The three TensorFlow steps and their Course 1 twins — and which one changes the weights.",
            "The difference between <b>loss</b> and <b>cost</b>.",
            "Why backprop costs about two passes regardless of parameter count.",
            "Why the forward values have to be kept, and what that costs you.",
            "Two reasons ReLU replaced sigmoid in hidden layers.",
            "What a dying ReLU is, and why it is permanent.",
            "Which output activation goes with which task — all four.",
            "Why a network with linear activations everywhere has no more power than one layer.",
            "What the two moves in softmax each accomplish.",
            "Why <code>exp(z - max(z))</code> cannot change the answer.",
            "Multi-class vs multi-label: the tell, and which head each needs.",
            "What Adam does that plain gradient descent does not.",
        ]),

        h2("🪜", "Where this week sits in the whole arc"),
        ladder("C2 W2", """You can now build and <b>train</b> a network of any shape, on any
of the four standard output types. Everything after this is either <b>how to tell whether it
is working</b> (Week 3), <b>a different family of model</b> (Week 4), or <b>a different kind
of problem</b> (Course 3). Backpropagation in particular does not appear again as a topic —
it becomes the thing every framework does for you, and this is the one week where you see
what it is doing."""),
    ]),
)
