# -*- coding: utf-8 -*-
"""Active Mastery for 04_backprop.py.

Per the brief's depth rule, this file gets the deepest debug section in the
lane: gradient checking IS its invariant, and it is the one file where a
correct implementation makes the check legitimately FAIL (the ReLU kink).
The XOR inputs are genuinely abstract -- the semantics table says so rather
than inventing a story. Hidden layer is 8 units, read off P: (2,8),(8,),(8,1),(1,).
"""
from masterykit import (section, prose, code, out, semantics, ledger, drill, peek,
                        predict, lab, breaks, invariant, wrong, reconstruct,
                        connections, recall, check)

AM = dict(
    lede="Eleven cards on the backward arrow &mdash; the half that makes deep learning "
         "possible, and the one file where a <b>correct</b> gradient check can fail.",
    sections=[

section("0", "&#129517;", "Before you run", "before", kind="orient",
    hook="XOR: the smallest problem a straight line cannot solve.",
    body=prose("""<p>File 03 asked <i>what did the network predict?</i> This one asks the
other question: <b>which weight caused the mistake, and by how much?</b></p>
<p>The data is <b>XOR</b> &mdash; four points, output 1 when exactly one input is 1. It is
chosen because it is <b>provably impossible</b> for a single linear boundary, so solving it
is a real demonstration rather than a formality.</p>
<p><b>Three things to watch.</b> All four gradients agree with a numerical measurement to
about 1e&minus;11. Then the file deliberately makes that same check <b>fail</b> at
6.4e&minus;02 &mdash; and neither side is wrong. And at the end, the same problem without a
hidden layer predicts 0.5 four times.</p>""")
    + connections([], [], "../gist/c22.html", "C2 Week 2 &mdash; the gist",
        extra=[("lab", "../scratch/03-forward-propagation.html", "File 03 first",
                "the forward arrow, which this file keeps and reverses")])),

section("1", "&#127991;&#65039;", "What every variable is", "vars", kind="semantics",
    hook="An honest table: XOR has no physical meaning, and saying so is the lesson.",
    body=semantics([
        ("X", "(4, 2) float64", "the four XOR inputs",
         "<b>Nothing physical.</b> [[0,0],[0,1],[1,0],[1,1]] &mdash; the four combinations of "
         "two bits, chosen because no straight line separates their labels.",
         "<i>none &mdash; abstract bits</i>",
         "<code>X[2]</code> is [1, 0]. It is not 1 metre of anything; it is the pattern "
         "&ldquo;first bit on, second off&rdquo;.",
         "There is no as-if reading worth having here. Inventing one (&ldquo;two "
         "switches&rdquo;) adds nothing the pattern does not already say, and would mislead "
         "you the moment a file has real units."),
        ("y", "(4,) float64", "the XOR answers",
         "[0, 1, 1, 0] &mdash; true when <b>exactly one</b> input is on.",
         "<i>class label</i>",
         "<code>y[1]</code> is 1.0: input [0,1] has exactly one bit on.",
         "Change it to AND ([0,0,0,1]) and a network with <b>no</b> hidden layer solves it "
         "immediately &mdash; AND <i>is</i> linearly separable. That single swap is the "
         "cleanest way to see what XOR is testing."),
        ("P", "list of 4 arrays", "the parameters",
         "<b>W1 (2,8), b1 (8,), W2 (8,1), b2 (1,)</b> &mdash; a 2&ndash;8&ndash;1 network. "
         "Eight hidden units for a four-point problem.",
         "<i>unitless</i>",
         "<code>P[0].shape</code> is (2, 8): two inputs feeding eight units, "
         "<b>columns are units</b>.",
         "Eight is generous on purpose. Drop to two and it still solves XOR but needs a lucky "
         "initialisation; drop to one and it cannot, ever."),
        ("A2", "(4, 1) float64", "the network's output",
         "<b>P(this input is a XOR-true case)</b>, one per input row.",
         "<b>probability, 0&ndash;1</b>",
         "After training: <b>[0.0001, 1.0, 1.0, 0.0]</b> &mdash; essentially exact on all "
         "four.",
         "Getting to 0.0001 rather than 0.05 is the log loss doing its job: it keeps paying "
         "the model to become more certain, long after the decisions stopped changing."),
        ("grads", "list of 4 arrays", "the gradients",
         "One array <b>per parameter array</b>, each exactly the same shape as the thing it "
         "corrects.",
         "cost per unit of that weight",
         "<code>grads[0].shape</code> is (2, 8) &mdash; identical to <code>P[0]</code>. That "
         "shape match is the first thing to check in any backprop implementation.",
         "Its <b>sign</b> is the message: negative means that weight is too small. Its "
         "magnitude says how urgently."),
        ("g'(z) for sigmoid", "derived", "the local slope",
         "How much a unit's output moves when its input moves &mdash; computable from the "
         "output alone, as <code>a(1&minus;a)</code>.",
         "<i>unitless</i>",
         "output 0.5 &rarr; slope <b>0.25</b>, the largest it ever gets. Output 0.1 or 0.9 "
         "&rarr; <b>0.09</b>.",
         "This is why the forward values are kept: the backward pass needs them. It is also "
         "why sigmoid stacks badly &mdash; 0.25<sup>10</sup> &asymp; <b>9.5e&minus;07</b> "
         "reaches the first layer."),
        ("eps", "float", "the nudge size",
         "How far to move a weight when <b>measuring</b> a slope rather than deriving it. A "
         "property of the <b>check</b>, not of the network.",
         "<i>unitless</i>",
         "Too large and you measure a chord instead of a tangent; too small and floating-point "
         "cancellation eats the difference. There is a sweet spot around 1e&minus;6.",
         "It never appears in training. Remove the check and the model is identical."),
    ],
    """This is the honest case the brief demands. <b>X and y here mean nothing physical</b>
&mdash; XOR is a structural test, not a measurement of anything &mdash; and pretending
otherwise would teach a habit that breaks on the next file with real units.""")
    + ledger([
        ("X", "(4, 2)", "<b>m=4</b> examples &times; <b>n=2</b> inputs"),
        ("W1", "(2, 8)", "n=2 in &times; <b>8 units</b>. Columns are units"),
        ("A1", "(4, 8)", "m=4 still; width has become 8"),
        ("W2", "(8, 1)", "8 in (the previous width) &times; 1 out"),
        ("A2", "(4, 1)", "m=4, one answer each"),
        ("dW1", "(2, 8)", "<b>identical to W1</b>. Always."),
        ("dW2", "(8, 1)", "<b>identical to W2</b>. Always."),
    ],
    """The rule that catches most backprop bugs before you run anything: <b>every gradient
has exactly the shape of the parameter it corrects.</b> If <code>dW1.shape != W1.shape</code>
you have a bug, and you knew it without computing a single number.""")
    + drill("""<p>Without looking: a sigmoid unit outputs <b>0.98</b>. Say out loud what its
local slope is, and what that means for the weight feeding it.</p>""",
    """<p>0.98 &times; (1 &minus; 0.98) = <b>0.0196</b> &mdash; almost flat.</p>
<p>So the gradient reaching that weight is multiplied by about <b>0.02</b>: the unit is
<b>saturated</b> and barely learns, however wrong it is. Nudging its input changes its output
almost not at all, so the chain rule passes almost nothing back.</p>
<p>That is the vanishing gradient in one number, and it is exactly why ReLU &mdash; slope
exactly <b>1</b> on the positive side &mdash; replaced sigmoid in hidden layers.</p>""")
    + peek("""Print the shapes and the slopes that the backward pass depends on.""",
"""import numpy as np

def peek(name, arr):
    a = np.asarray(arr)
    first = a[0] if a.ndim > 1 else a
    print(f"{name:8s} shape={str(a.shape):7s} dtype={a.dtype}  "
          f"min={a.min():.4g}  max={a.max():.4g}")
    print(f"         first row: {np.round(np.atleast_1d(first)[:6], 4).tolist()}")""",
    [("for i, p in enumerate(P): peek(f&quot;P[{i}]&quot;, p)", "just after the parameters are built"),
     ("for i, g in enumerate(grads): peek(f&quot;grads[{i}]&quot;, g)", "just after the backward pass in <code>gradcheck</code>"),
     ("peek(&quot;A2&quot;, A2)", "after training, in the <code>train</code> section")],
    prose("""<p>Line the two loops up. <code>P[i]</code> and <code>grads[i]</code> must
report <b>the same shape on every row</b> &mdash; (2,8), (8,), (8,1), (1,). If any pair
disagrees, stop and fix that before reading a single number.</p>
<p>And <code>A2</code> after training reads <b>[0.0001, 1.0, 1.0, 0.0]</b> &mdash; not
[0.05, 0.95, ...]. The log loss keeps rewarding confidence long after the four decisions
have stopped changing.</p>"""))),

section("2", "&#128302;", "Prediction checkpoints", "predict", kind="predict",
    hook="Four, and one asks you to predict a failure that is not a bug.",
    body=predict([
        ("""The gradient check passes at about 1e&minus;11. Then the file zeroes every bias
and runs the <b>same</b> check. Predict: does it still pass?""",
         """<p><b>No</b> &mdash; it fails at <b>6.4e&minus;02</b>, a real disagreement, six
orders of magnitude worse.</p>
<p>And <b>neither side is wrong.</b> ReLU has no derivative at exactly z = 0: the slope is 0
on one side and 1 on the other. The analytic version applies <code>z &gt; 0</code> and picks
the flat side; the numeric version steps both ways and <b>averages across the kink</b>.</p>
<p>This is the one situation in the whole lane where a gradient check fails on <b>correct
code</b>, and knowing it exists saves you from hunting a bug that is not there.</p>"""),
        ("""Before reading the training column: how many iterations does XOR need before the
cost is essentially zero?""",
         """<p>About <b>2,000</b>. The cost goes <b>0.954843</b> at iteration 0 to
<b>0.000245</b> at 2,000 &mdash; a factor of roughly 4,000.</p>
<p>Everything after that is polish: 0.000109 at 4,000, 0.000049 at 8,000. The same
enormous-drop-then-flatten shape as file 01, at a completely different scale.</p>"""),
        ("""The control experiment removes the hidden layer entirely. Predict the four
predictions, not just the accuracy.""",
         """<p><b>[0.5, 0.5, 0.5, 0.5]</b> &mdash; all four identical, and accuracy
<b>0.50</b>.</p>
<p>It does not do <i>badly</i>; it does <b>nothing</b>. Every prediction is exactly the
model announcing it has no idea. And it is not a training failure &mdash; no straight line
separates XOR, so there is no better answer to find. The weights converge to zero because
every direction is equally useless.</p>"""),
        ("""How many forward passes would it cost to get all the gradients by nudging each
parameter one at a time? Count the parameters first.""",
         """<p>Parameters: 2&times;8 + 8 + 8&times;1 + 1 = <b>33</b>. A central-difference
nudge needs <b>two</b> cost evaluations each, so about <b>66</b> forward passes.</p>
<p>Backprop gets all 33 in <b>one forward plus one backward</b>. At 33 parameters that is a
33&times; saving; at a million parameters it is the difference between two passes and two
million &mdash; a different complexity class, and the reason deep learning exists at
all.</p>"""),
    ],
    """The first one is the most valuable prediction in the lane: a check that fails on
correct code.""")),

section("3", "&#128295;", "Modify the copy", "lab", kind="lab",
    hook="Five edits, from the harmless to the one that makes XOR unsolvable.",
    body=lab([
        ("L1", "Change a value",
         "Set <code>eps</code> to <code>1e-2</code> and re-run the gradient check. Predict "
         "whether it gets better or worse.",
         "def numeric_gradient(f, theta, eps=1e-2):     # was 1e-6",
         """<p><b>Worse</b> &mdash; the agreement degrades from ~1e&minus;11 to roughly
1e&minus;04.</p>
<p>A large nudge measures a <b>chord</b> rather than a tangent, and the curvature between the
two points shows up as error. Now try <code>1e-12</code>: it gets worse <i>again</i>, because
subtracting two nearly-identical costs destroys the significant digits.</p>
<p>The lesson: <code>eps</code> has a sweet spot around 1e&minus;6, and it is a property of
the <b>measurement</b>, not of the network.</p>"""),
        ("L2", "Change a parameter",
         "Shrink the hidden layer from 8 units to <b>2</b>. Re-run training a few times and "
         "watch the final cost.",
         "P = init(2, 2, 1, rng)        # was init(2, 8, 1, rng)",
         """<p>It usually still solves XOR &mdash; two hidden units are the theoretical
minimum &mdash; but <b>not every run</b>. Some initialisations get stuck with the cost
plateauing well above zero.</p>
<p>Eight units is not eight times more capacity than needed; it is <b>insurance against a bad
start</b>. That is the practical argument for over-parameterising slightly, and it is the
same reason C2 W3 says a bigger network with proper regularisation is almost never
worse.</p>"""),
        ("L3", "Change the data",
         "Change y from XOR to <b>AND</b>. Then remove the hidden layer as well. Predict "
         "whether it can still learn.",
         "y = np.array([0., 0., 0., 1.])     # AND, not XOR",
         """<p>With AND it learns perfectly <b>even with no hidden layer</b>, because AND
<b>is</b> linearly separable &mdash; a single line with the right slope divides [1,1] from
the other three.</p>
<p>This is the sharpest possible statement of what the hidden layer is for. Same network,
same code, same training loop: the only thing that changed is whether the problem needs a
bend in the boundary.</p>"""),
        ("L4", "Change an assumption",
         "Initialise <b>every</b> weight to zero instead of randomly. Predict what the eight "
         "hidden units learn.",
         "P = [np.zeros((2, 8)), np.zeros(8), np.zeros((8, 1)), np.zeros(1)]",
         """<p>Nothing. The cost barely moves, and all eight hidden units stay
<b>identical</b> forever.</p>
<p>With identical weights every unit computes the same output, so every unit receives the
same gradient, so every unit takes the same step. There is nothing to <b>break the
symmetry</b>, and eight identical units have exactly the capacity of one.</p>
<p>This is why initialisation is random &mdash; not for luck, but because the randomness
<i>is</i> the mechanism that lets units specialise. Same failure as file 09's collaborative
filtering, for the same reason.</p>"""),
        ("L5", "Explain it",
         "Explain why the forward pass has to <b>return</b> its intermediate values here when "
         "file 03's did not.",
         None,
         """<p>Because the backward pass needs them. Each local slope depends on what that
node <b>saw on the way in</b> &mdash; a sigmoid's slope is <code>a(1&minus;a)</code>, so you
need <code>a</code>; a ReLU's slope depends on the sign of <code>z</code>.</p>
<p>File 03 only predicts, so it can discard each layer's output as soon as the next has
consumed it. Training cannot discard anything until the backward pass has been all the way
through &mdash; which is precisely why <b>training uses far more memory than
prediction</b>, and why halving the batch size is the first thing to try when you run
out.</p>"""),
    ],
    """L4 is the one to actually run. &ldquo;Initialise randomly&rdquo; sounds like
superstition until you watch eight units refuse to differentiate.""")),

section("4", "&#128165;", "Break it, then repair it", "break", kind="debug",
    hook="Five breaks. This is the deepest debug section in the lane, and the file earns it.",
    body=breaks([
        ("dA1 = dZ2 @ W2.T\ndZ1 = dA1 * d_relu(Z1)      # <- delete this factor:\ndZ1 = dA1",
         "Drop the activation's local slope from the backward pass. <b>Predict whether the "
         "gradient check catches it</b>, and whether training still appears to work.",
         """<p>The gradient check catches it <b>immediately and loudly</b> &mdash; dW1 and db1
disagree with the numerical estimate by orders of magnitude, while dW2 and db2 still
pass.</p>
<p>That split is the diagnostic: <b>the layer whose check fails is downstream of the
mistake</b>. dW2 is computed before the missing factor is needed, so it survives.</p>
<p>Without the check, training would still <i>run</i> and the cost would still <i>fall</i>
&mdash; just to a worse answer, slowly, with no symptom whatsoever. This is the single best
argument in the lane for gradient checking.</p>"""),
        ("dZ2 = (A2 - y.reshape(-1, 1))        # the / m is gone",
         "Forget to divide one gradient by m. Predict the symptom.",
         """<p>The check fails on <b>dW1 and db1 by a factor of exactly 4</b> &mdash; which is
m. Not noise, not a sign error: a clean integer ratio.</p>
<p>The invariant worth learning: <b>a gradient check that fails by a round number is a
scaling bug, not a calculus bug.</b> A factor of m, or 2, or 0.5 tells you where to look
immediately. A factor of 1.0003 is something else entirely.</p>"""),
        ("dZ2 = (A2 - y) / m               # the .reshape(-1, 1) is gone",
         "Subtract a flat <code>y</code> from a column <code>A2</code>. <b>Predict whether "
         "anything errors.</b>",
         """<p><b>Nothing errors.</b> <code>(4,1) - (4,)</code> broadcasts to <b>(4,4)</b>
&mdash; every output against every label.</p>
<p>From there the shapes cascade wrongly but often stay <i>legal</i>, so you get a trained
model built on a 4&times;4 matrix that should have been a 4&times;1 vector. The cost is a
number, it goes down, and everything is wrong.</p>
<p>The defence is the shape ledger, not more staring: <b>dz2 must be (4,1)</b>, and one
<code>print(dz2.shape)</code> settles it.</p>"""),
        ("A1 = sigmoid(Z1)                 # was np.maximum(0.0, Z1)",
         "Replace the hidden ReLU with a sigmoid inside <code>forward</code>. Does XOR still get solved, and how fast?",
         """<p>It still solves it, but <b>noticeably slower</b> &mdash; the cost falls less
steeply in the early iterations.</p>
<p>With only two layers the vanishing gradient is mild: one factor of at most 0.25. Stack ten
sigmoid layers and the first receives at most <b>0.25<sup>10</sup> &asymp; 9.5e&minus;07</b>
of the signal, and it stops learning entirely.</p>
<p>The invariant: <b>ReLU's slope is exactly 1 on the positive side, so gradients pass
through undiminished at any depth.</b> That is the whole reason it replaced sigmoid in hidden
layers &mdash; not expressiveness.</p>"""),
        ("for _ in range(10000):\n    ...\n    P = [p - 0.5 * g for p, g in zip(P, grads)]",
         "Raise the learning rate from its default to 0.5. Predict what the cost column does.",
         """<p>It <b>oscillates</b>, and at higher rates diverges to <code>nan</code>.</p>
<p>Same rule as file 01, unchanged by the extra layer: <b>if the cost ever rises between two
iterations, the step is too large</b>. Backprop changed how the gradient is <i>computed</i>;
it changed nothing about how it is <i>used</i>.</p>
<p>Worth noticing that this is the one break here that is a <b>tuning</b> problem rather than
a bug &mdash; and the way to tell is the &alpha;-shrink test from file 02.</p>"""),
    ],
    """Predict the failure <b>mode</b> each time: loud, quiet, or silent-and-plausible. Two of
these five are silent, and those are the ones that cost days.""")),

section("5", "&#9878;&#65039;", "The invariant", "invariant", kind="invariant",
    hook="Hand-derived against measured &mdash; and the one place it legitimately fails.",
    body=invariant("""<p><b>Every hand-derived gradient must match a numerical measurement
&mdash; except exactly at a ReLU kink, where neither answer is wrong.</b></p>""",
    """<p>The file checks all four parameter arrays and prints the worst disagreement for
each: <b>7.6e&minus;11</b>, <b>7.2e&minus;11</b>, <b>8.1e&minus;11</b>,
<b>3.2e&minus;11</b>. Eleven decimal places is the floating-point noise floor, not luck.</p>
<p>Then it sets every bias to exactly zero and re-runs, and the check <b>fails</b> at
<b>6.4e&minus;02</b>. ReLU has no derivative at z = 0 &mdash; slope 0 on one side, 1 on the
other &mdash; so the analytic version picks the flat side and the numeric version averages
across the kink. Both are defensible answers to a question with no answer.</p>
<p>In practice it never matters: hitting z <i>exactly</i> zero has probability zero once the
weights are random, and the failure here had to be <b>engineered</b> by zeroing every bias
deliberately. But it is worth seeing once, because it is the only case in the lane where
correct code fails its own test.</p>""",
    """for name, g_analytic, g_numeric in checks:
    denom = np.maximum(1e-12, np.abs(g_analytic) + np.abs(g_numeric))
    rel = np.max(np.abs(g_analytic - g_numeric) / denom)
    assert rel < 1e-7, f"{name} disagrees: {rel:.3e}"

# and the shape invariant, which costs nothing and catches more:
for p, g in zip(P, grads):
    assert p.shape == g.shape""")),

section("6", "&#129535;", "Wrong mental models", "wrong", kind="myths",
    hook="Five, including the one about what backprop actually is.",
    body=wrong([
        ("Backpropagation is just the chain rule.",
         """<p>The chain rule is the <b>maths</b>. Backprop is a specific <b>order of
evaluation</b> of it, and the order is the entire contribution.</p>
<p>Evaluating the same chain left-to-right (forward-mode) costs one sweep <b>per
parameter</b>. Right-to-left keeps a single row vector at every step and gets all of them in
<b>one</b> sweep. For 33 parameters that is 33&times;; for a million it is the difference
between possible and impossible.</p>
<p>Everyone knew the chain rule in 1960. The ordering is what 1986 contributed.</p>"""),
        ("A gradient check that fails means my calculus is wrong.",
         """<p>Usually &mdash; but this file contains a counterexample it built on purpose. At
a <b>ReLU kink</b> the analytic and numeric answers legitimately differ (6.4e&minus;02),
because the derivative does not exist there.</p>
<p>And the other common cause is not calculus either: <b>eps too large or too small</b>. Too
large measures a chord; too small loses the difference to floating-point cancellation. Check
your eps before you check your derivation.</p>"""),
        ("Random initialisation is a small detail.",
         """<p>Set every weight to zero and the network learns <b>nothing</b> &mdash; not
&ldquo;learns slowly&rdquo;. All eight hidden units compute the same value, receive the same
gradient, and take the same step, forever.</p>
<p>The randomness is not luck, it is the <b>symmetry-breaking mechanism</b>. Eight identical
units have exactly the capacity of one, which for XOR is zero.</p>"""),
        ("The hidden layer makes the network better at XOR.",
         """<p>It makes XOR <b>possible</b>. Without it the network predicts <b>0.5 four
times</b> and scores 0.50 &mdash; not a poor result, the complete absence of one.</p>
<p>No straight line separates XOR, so there is no better answer for a linear model to find.
The difference between 0.50 and 0.00005 is not a difference of degree.</p>"""),
        ("Training and prediction cost about the same.",
         """<p>Prediction discards each layer's output as soon as the next consumes it.
Training <b>cannot discard anything</b> until the backward pass has been all the way through,
because every local slope depends on the forward value.</p>
<p>That is why training memory scales with depth <b>and</b> batch size, why you run out of
GPU memory training but not serving, and why halving the batch is the first fix.</p>"""),
    ])),

section("7", "&#127959;&#65039;", "Reconstruction challenge", "reconstruct", kind="rebuild",
    hook="Rebuild backprop, and check it the way the file does.",
    body=reconstruct([
        ("Explain", "In four sentences, explain backprop without the words <i>chain rule</i>.",
         """<p>Roughly: run the network forward and keep every intermediate value. Start at the
output with the question &ldquo;how much does the cost move if this moves?&rdquo;, which is 1
for the cost itself. Walk backwards through the layers, and at each step multiply by how much
that step's output moves when its input moves. Whenever you pass a weight, the running product
<b>is</b> that weight's gradient.</p>"""),
        ("Skeleton", "Write the signatures of the forward and backward passes, and say what "
         "each returns.",
         """<p>Forward returns the output <b>and the cache</b> of intermediates &mdash; that
is the difference from file 03. Backward takes that cache plus the true labels and returns a
list of gradients, <b>one per parameter array, each the same shape as its parameter</b>.</p>"""),
        ("Core", "Write the two-layer backward pass from memory: dz2, dW2, db2, dz1, dW1, db1.",
         """<p><code>dZ2 = (A2 - y.reshape(-1,1)) / m</code>; <code>dW2 = A1.T @ dZ2</code>;
<code>db2 = dZ2.sum(axis=0)</code>; <code>dZ1 = (dZ2 @ W2.T) * d_relu(Z1)</code>;
<code>dW1 = X.T @ dZ1</code>; <code>db1 = dZ1.sum(axis=0)</code>.</p>
<p>Two things people drop: the <b>/ m</b>, and the <b>relu_grad</b> factor. The first fails
the check by exactly m; the second fails only the first layer.</p>"""),
        ("Minimal", "Build the smallest network that solves XOR, and the smallest that "
         "provably cannot.",
         """<p><b>2&ndash;2&ndash;1 with a non-linearity</b> can, though not from every
initialisation. <b>2&ndash;1</b> &mdash; no hidden layer &mdash; cannot, and the file proves
it: four predictions of 0.5.</p>
<p>Also worth building: <b>2&ndash;8&ndash;1 with identity activations</b>. It cannot solve
XOR either, because it collapses to a single linear layer &mdash; which is file 03's
result.</p>"""),
        ("Verify", "Check your rebuild without looking at the original.",
         """<p>Three self-contained checks. Every <code>grad.shape == param.shape</code>.
Every gradient within ~1e&minus;7 relative of a central-difference estimate at
eps = 1e&minus;6. And the cost falls monotonically for a small enough step.</p>
<p>If the check fails by a <b>round factor</b> it is a scaling bug; if it fails on the first
layer only, you dropped an activation's local slope.</p>"""),
    ],
    """The verify stage is the real content here. Once you can check a gradient you can write
any network with confidence; without it you cannot trust one you did not copy.""")),

section("8", "&#128279;", "Connections", "conn", kind="links",
    hook="03 gave the forward arrow; this is the other one. 05 reuses both.",
    body=connections(
        [("lab", "../scratch/03-forward-propagation.html", "Back to 03",
          "the forward pass this file keeps and then reverses"),
         ("lab", "../scratch/01-linear-regression.html", "Back to 01",
          "the gradient check first appears there, on four parameters instead of 33")],
        [("lab", "../scratch/05-softmax.html", "On to 05",
          "the same backward pass with a coupled N-class output"),
         ("lab", "../scratch/12-fine-tuning.html", "On to 12",
          "this training loop, run on somebody else's pretrained weights")],
        "../gist/c22.html", "C2 Week 2 &mdash; the gist",
        extra=[("docs", "../reference.html", "Reference &mdash; C2 W2",
                "<code>c2w2-backprop-cost</code> and <code>c2w2-chain-rule</code> carry the "
                "cost argument this file demonstrates")])),

section("9", "&#9670;", "Recall sheet", "recall", kind="recall",
    hook="Seven cards, weighted towards the debugging.",
    body=recall([
        ("What must be true of <code>grads[i].shape</code>, always?",
         "It must <b>equal <code>P[i].shape</code></b> &mdash; (2,8), (8,), (8,1), (1,). A "
         "gradient corrects a parameter, so it has the parameter's shape. Checking this costs "
         "nothing and catches a lot."),
        ("The gradient check fails by a factor of exactly <b>4</b>, with m = 4. What kind of "
         "bug is it?",
         "A <b>scaling</b> bug, not a calculus one &mdash; a missing <code>/ m</code>. A "
         "round-number ratio always means scaling; 1.0003 means something else."),
        ("The check fails on dW1 and db1 but <b>passes</b> on dW2 and db2. Where is the bug?",
         "Downstream of layer 2 in the backward walk &mdash; almost always the missing "
         "<code>d_relu(Z1)</code> factor in <code>dZ1</code>. dW2 is computed before that "
         "factor is needed, so it survives."),
        ("Name the one case where a gradient check fails on <b>correct</b> code.",
         "At a <b>ReLU kink</b> (z exactly 0), where the derivative does not exist. The file "
         "engineers it by zeroing every bias, and gets <b>6.4e&minus;02</b>. Analytic picks "
         "the flat side; numeric averages across."),
        ("Why is <code>eps = 1e-6</code> and not 1e&minus;2 or 1e&minus;12?",
         "Too <b>large</b> measures a chord instead of a tangent (curvature error); too "
         "<b>small</b> loses the difference to floating-point cancellation. 1e&minus;6 is the "
         "sweet spot."),
        ("Backprop costs about two passes. What is the alternative, and what does it cost?",
         "Nudging each parameter separately: <b>~2 forward passes per parameter</b>. Here 33 "
         "parameters &rarr; ~66 passes. At a million parameters it is two passes against two "
         "million."),
        ("Every weight initialised to zero. What do the eight hidden units learn?",
         "<b>Nothing, identically.</b> Same output &rarr; same gradient &rarr; same step, "
         "forever. Randomness is the <b>symmetry-breaking mechanism</b>, not luck."),
    ],
    """Cover them and answer aloud.""")),

section("10", "&#9989;", "Mastery check", "check", kind="check",
    hook="Five, and three of them are diagnostic rather than factual.",
    body=check([
        ("""Your gradient check fails on <b>every</b> parameter by the same factor of 4.
Name the bug without looking at your code.""",
         """<p>A missing <b><code>/ m</code></b>, with m = 4. A uniform round-number ratio is
always a scaling bug &mdash; and because it is uniform, it is applied at a point every
gradient passes through, most likely on <code>dZ2</code>.</p>"""),
        ("""Your check passes on dW2/db2 and fails on dW1/db1. What did you get wrong, and
why does that split localise it?""",
         """<p>You dropped the activation's local slope &mdash; the
<code>* d_relu(Z1)</code> in <code>dZ1</code>.</p>
<p>The split localises it because the backward pass computes <b>dW2 before it needs that
factor</b>. Anything downstream of the mistake in the walk is unaffected; everything upstream
is wrong. Reading which layers fail tells you where to look.</p>"""),
        ("""State, in one sentence, why the forward pass here must return its intermediates
when file 03's did not.""",
         """<p>Because every local slope in the backward pass depends on what that node saw on
the way in &mdash; a sigmoid's slope is <code>a(1&minus;a)</code>, a ReLU's depends on the
sign of z. Prediction can discard as it goes; training cannot, and that is why training uses
far more memory.</p>"""),
        ("""Someone reports a gradient check failing at 6e&minus;02 and asks you to find the
bug. What do you ask them first?""",
         """<p>Whether any <code>z</code> is <b>exactly zero</b> &mdash; and whether they
zeroed the biases or used an all-zero input. At a ReLU kink the check fails on correct
code.</p>
<p>Then: what <code>eps</code> are they using? Those two account for most gradient-check
failures that are not real bugs, and both are faster to rule out than re-deriving the
maths.</p>"""),
        ("""The no-hidden-layer control predicts 0.5 four times. Explain why that is
<b>not</b> a training failure.""",
         """<p>Because no straight line separates XOR, so there is no better answer available
to a linear model. The optimiser converged correctly to the best a linear boundary can do,
which is to give up equally on all four points.</p>
<p>The distinction matters: a training failure is fixed by tuning, and this is fixed only by
changing the <b>model class</b>. Reading 0.50 as &ldquo;needs more iterations&rdquo; would
waste an afternoon.</p>"""),
    ],
    """None of these appears in the <a href="../quiz/c22.html">C2 W2 mock quiz</a>, which
covers ReLU, softmax, Adam and the backprop cost argument. These are all things you only
learn by breaking this file.""")),
    ],
)
