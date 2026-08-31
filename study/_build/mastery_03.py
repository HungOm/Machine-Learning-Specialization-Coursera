# -*- coding: utf-8 -*-
"""Active Mastery for 03_neural_net_forward.py.

Every shape, dtype and value quoted below was read off the running file by
introspection, not inferred from a name. Two of them matter especially:

  * `batch` is [[1,3],[0,0],[-2,1],[4,-1]] and has NO physical meaning. This
    file's first network is a shape demo. Saying "one row is a house" here
    would be an invention, so the table says so plainly instead.
  * `tests` IS physical: degrees Celsius and minutes. The detector layer `h`
    is the anchor for this file, exactly as the roast experiment intends.

Nothing here duplicates the C2 W1 mock quiz (which already asks parameter
counting, the shape rule, [[200,17]] vs [200,17], what a unit computes, and
forward-prop truths) or the c2w1-* SRS cards.
"""
from masterykit import (section, prose, code, out, semantics, ledger, drill, peek,
                        predict, lab, breaks, invariant, wrong, reconstruct,
                        connections, recall, check, render)

AM = dict(
    lede="Eleven sections that ask you to <b>use</b> this file rather than read it again. "
         "Everything references real names in <code>03_neural_net_forward.py</code> and "
         "real numbers it actually printed.",
    sections=[

# ---------------------------------------------------------------- 0
section("0", "&#129517;", "Before you run", "before", 
    prose("""<p>This file has <b>two networks in it</b>, and they are doing completely
different jobs. Knowing which one you are looking at is most of the battle.</p>
<ul>
<li>The <b>2&ndash;3&ndash;1 demo network</b> (<code>W1, b1, W2, b2, batch, out</code>)
exists to show <b>shapes and mechanics</b>. Its inputs are made-up numbers with no meaning.</li>
<li>The <b>coffee roast checker</b> (<code>Wd, bd, Wout, bout, tests, h, probs</code>) exists
to show what <b>hidden units are for</b>. Its inputs are real: degrees Celsius and minutes.</li>
</ul>
<p><b>Three things to watch as you read:</b> that <code>loop_out</code> and
<code>mat_out</code> come out <i>identical</i>; that removing the activations collapses two
layers into one matrix; and that one test roast comes out <b>WRONG</b> on purpose.</p>""")
    + connections([], [],
                  "../gist/c21.html", "C2 Week 1 &mdash; the gist",
                  extra=[("lab", "../scratch/02-logistic-regression.html",
                          "File 02 first, if you have not",
                          "one neuron is exactly the logistic unit built there")])),

# ---------------------------------------------------------------- 1  THE HEADLINE
section("1", "&#127991;&#65039;", "What every variable is", "vars",
    semantics([
        ("x", "(2,) float64", "the single-neuron demo input",
         "<b>Nothing.</b> Two made-up numbers used to show the arithmetic of one unit.",
         "<i>none</i>", "<code>x[1]</code> is 3.0, and 3.0 of nothing in particular.",
         "The answer changes; no claim about the world changes."),
        ("batch", "(4, 2) float64", "four examples fed through the demo net",
         "<b>Still nothing.</b> <code>[[1,3],[0,0],[-2,1],[4,-1]]</code> was chosen to "
         "exercise positive, zero and negative inputs &mdash; not to represent anything.",
         "<i>none</i>",
         "<code>batch[2,0]</code> is &minus;2.0. There is no quantity in the world that "
         "this is &minus;2 <i>of</i>.",
         "Nothing, in world terms. This is the honest reading, and the as-if reading "
         "(&ldquo;pretend it is two sensor readings&rdquo;) is a crutch that will mislead "
         "you the moment you meet a file where the numbers <b>do</b> mean something."),
        ("W1", "(2, 3) float64", "first layer weights",
         "How much each of the two inputs matters to each of the three units. "
         "<b>Column j is unit j&rsquo;s own weight vector.</b>",
         "<i>unitless</i> (output per input)",
         "<code>W1[1,2]</code> is &minus;1.5: unit 3 is pushed <b>down</b> by a large "
         "second input.",
         "Flip its sign and unit 3 changes from a detector of &ldquo;low x&#8322;&rdquo; to "
         "one of &ldquo;high x&#8322;&rdquo;."),
        ("b1", "(3,) float64", "first layer biases",
         "Each unit&rsquo;s <b>default mood</b> &mdash; how strongly it fires with zero "
         "input.",
         "<i>same units as z</i>",
         "<code>b1[0]</code> is &minus;1.0, so unit 1 starts reluctant: it needs positive "
         "evidence before it fires at all.",
         "Raise it and that unit fires more easily for every input, without any input "
         "mattering more."),
        ("out", "(4, 1) float64", "the demo network&rsquo;s output",
         "A number between 0 and 1 per example. Because the inputs mean nothing, "
         "<b>this probability is a probability of nothing</b>.",
         "probability, 0&ndash;1",
         "<code>out[3,0]</code> is 0.99929 &mdash; the network is very confident about an "
         "example that represents nothing.",
         "Confidence here is a property of the weights somebody wrote down, not evidence "
         "about any world."),
        ("total", "int", "parameter count",
         "How many numbers this network could learn, if it were learning &mdash; which in "
         "this file it is not.",
         "a count",
         "13: nine in layer 1 (2&times;3 + 3) and four in layer 2 (3&times;1 + 1).",
         "More parameters means more capacity to fit, and more to get wrong."),
        ("tests", "(6, 2) float64", "six roasts to check",
         "<b>Here the numbers mean something.</b> One row = one roast. Column 0 is "
         "temperature, column 1 is duration.",
         "&deg;C, and minutes",
         "<code>tests[2,0]</code> is 285.0 &mdash; roast #3 was run at 285&nbsp;&deg;C, "
         "which is 25&nbsp;&deg;C above the good band.",
         "Raise a temperature past 260 and the &ldquo;too hot&rdquo; detector should switch "
         "on. That is a testable claim about this file."),
        ("Wd", "(2, 4) float64", "detector weights, built by hand",
         "Which measurement each detector reads, and in which direction. Column 0 reads "
         "temperature negatively; column 3 reads duration positively.",
         "<i>unitless</i>, but see the 4",
         "<code>Wd[1,2]</code> is &minus;4.0. The <b>4</b> is a deliberate scale factor: "
         "minutes span a much narrower range than degrees, so duration is amplified to "
         "make the two detectors comparably sharp.",
         "Halve it and the duration detectors become blunter than the temperature ones, so "
         "borderline-duration roasts get judged less confidently than borderline-temperature "
         "ones."),
        ("bd", "(4,) float64", "detector biases",
         "<b>Literally the thresholds.</b> <code>[180, &minus;260, 48, &minus;60]</code> are "
         "the boundaries of the good band, written into the biases.",
         "&deg;C and (4 &times; minutes)",
         "<code>bd[0]</code> is 180: unit 1 computes &minus;T + 180, which is positive "
         "exactly when <b>T &lt; 180&nbsp;&deg;C</b>.",
         "Change 180 to 190 and you have moved the &ldquo;too cool&rdquo; line, and the "
         "network now rejects roasts it used to accept &mdash; with no retraining, because "
         "nothing here was trained."),
        ("h", "(6, 4) float64", "the hidden layer&rsquo;s output",
         "<b>Four alarms, one per row of <code>tests</code>.</b> "
         "<code>[too cool?, too hot?, too short?, too long?]</code> &mdash; and this is the "
         "variable worth understanding in the whole file.",
         "unitless, 0&ndash;1 (an alarm&rsquo;s confidence)",
         "<code>h[3,0]</code> is <b>0.993</b>: roast #4 was 175&nbsp;&deg;C, and the "
         "&ldquo;too cool&rdquo; alarm is almost fully on.",
         "A row of four zeros means <b>no alarm fired</b>, which is what a good roast looks "
         "like from inside the network."),
        ("probs", "(6,) float64", "final good/bad score",
         "The output unit&rsquo;s answer: the chance this roast is good.",
         "probability, 0&ndash;1",
         "<code>probs[5]</code> is about 1.6e&minus;10 for a roast the rule calls "
         "<b>good</b>. That row is wrong, deliberately.",
         "It is not a bug &mdash; see section 4."),
        ("K", "float", "detector sharpness",
         "How abruptly each alarm switches. <b>Not a property of coffee at all</b> &mdash; "
         "it is a modelling choice, the same kind of quantity as a learning rate.",
         "<i>unitless</i>",
         "60.0. Large enough that the output unit behaves almost like a hard AND gate.",
         "Lower it and the boundaries blur; raise it and they sharpen but never become "
         "perfectly hard. This is the parameter / hyperparameter line, drawn in units."),
    ],
    """Read down the <b>in the world</b> and <b>units</b> columns. Two of these variables
have genuine physical referents and most do not, and being able to say which is which is the
skill this section is for. Where a quantity means nothing, this table says so rather than
inventing a story for it.""")

    + ledger([
        ("x", "(2,)", "one example, two features &mdash; no batch dimension"),
        ("batch", "(4, 2)", "<b>m=4</b> examples &times; <b>n=2</b> features"),
        ("W1", "(2, 3)", "n=2 inputs &times; 3 units. <b>Columns are neurons</b>"),
        ("b1", "(3,)", "one per unit; broadcasts down all m rows"),
        ("A after layer 1", "(4, 3)", "m=4 still; n has become <b>3</b>"),
        ("W2", "(3, 1)", "3 inputs (the previous layer&rsquo;s width) &times; 1 unit"),
        ("out", "(4, 1)", "m=4 unchanged, one answer each"),
        ("tests", "(6, 2)", "<b>m=6</b> roasts &times; n=2 measurements"),
        ("Wd", "(2, 4)", "n=2 &times; 4 detectors"),
        ("h", "(6, 4)", "m=6 roasts &times; 4 alarms"),
        ("grid", "(2501, 2)", "the sweep: 61 &times; 41 points, flattened"),
    ],
    """<b>m never changes inside a forward pass.</b> Four examples go in and four answers come
out; six roasts go in and six verdicts come out. It is <b>n</b> that changes &mdash; 2 becomes
3 becomes 1 &mdash; and every weight matrix's first dimension is the <b>previous</b> layer's
width. If you can predict that column, you can predict every shape error in the file.""")

    + drill("""<p>Do not look anything up. In <code>h</code>, point at <b><code>h[3, 0]</code></b>
and say out loud, in a full sentence, what that number is <b>about a roast</b>. Then do the
same for <b><code>h[5, 1]</code></b> and <b><code>h[0, 3]</code></b>.</p>
<p>A correct answer names the roast, the measurement, and the alarm.</p>""",
    """<p><code>h[3, 0] = <b>0.993</b></code> &mdash; roast #4 was run at
<b>175&nbsp;&deg;C</b>, and the <b>&ldquo;too cool&rdquo;</b> alarm is almost fully on,
because 175 is below the 180 threshold.</p>
<p><code>h[5, 1] = <b>0.475</b></code> &mdash; roast #6 was <b>259.9&nbsp;&deg;C</b>, a tenth
of a degree under the &ldquo;too hot&rdquo; line, so that alarm is <b>half on</b>. Not off.
Half.</p>
<p><code>h[0, 3] = <b>0.012</b></code> &mdash; roast #1 ran <b>13.9 minutes</b>, comfortably
inside the 12&ndash;15 band, so the &ldquo;too long&rdquo; alarm is essentially silent.</p>
<p>If you said &ldquo;0.993 is a high activation&rdquo; you described the number, not the
roast. That is exactly the gap this section exists to close.</p>""")

    + peek("""You cannot narrate a variable you have never printed. Here is a helper that
prints the four things worth knowing about any array.""",
"""import numpy as np

def peek(name, arr):
    a = np.asarray(arr)
    first = a[0] if a.ndim > 1 else a
    print(f"{name:8s} shape={str(a.shape):7s} dtype={a.dtype}  "
          f"min={a.min():.4g}  max={a.max():.4g}")
    print(f"         first row: {np.round(np.atleast_1d(first)[:6], 4).tolist()}")""",
    [("peek(&quot;mat_out&quot;, mat_out)", "just after <code>mat_out</code> is computed, in the <code>layer_matmul</code> section"),
     ("peek(&quot;batch&quot;, batch); peek(&quot;out&quot;, out)", "just after <code>out = forward(batch, net, acts)</code>"),
     ("peek(&quot;tests&quot;, tests); peek(&quot;h&quot;, h); peek(&quot;probs&quot;, probs)", "just after <code>h = dense(tests, Wd, bd, sigmoid)</code>")],
    out("""--- point 1  after dense() in layer_matmul ---
mat_out  shape=(3,)    dtype=float64  min=0.02298  max=0.9933
         first row: [0.9526, 0.9933, 0.023]
--- point 2  after forward(batch, net, acts) ---
batch    shape=(4, 2)  dtype=float64  min=-2  max=4
         first row: [1.0, 3.0]
out      shape=(4, 1)  dtype=float64  min=0.0005528  max=0.9993
         first row: [0.0067]
--- point 3  after h = dense(tests, Wd, bd, sigmoid) ---
tests    shape=(6, 2)  dtype=float64  min=12.5  max=285
         first row: [200.0, 13.9]
h        shape=(6, 4)  dtype=float64  min=2.507e-46  max=1
         first row: [0.0, 0.0, 0.0005, 0.0121]
probs    shape=(6,)    dtype=float64  min=7.309e-17  max=1
         first row: [1.0, 0.0, 0.0, 0.0, 1.0, 0.0]""")
    + prose("""<p>Two things in that output are worth stopping on. <code>h</code>'s minimum is
<b>2.5e&minus;46</b> &mdash; a sigmoid output that has saturated so hard it is numerically
zero. And <code>probs</code> is exactly <b>[1, 0, 0, 0, 1, 0]</b> to four decimal places: the
network is not hedging on five of the six roasts, and the one it hedges on is the one it gets
wrong.</p>"""))),

# ---------------------------------------------------------------- 2
section("2", "&#128302;", "Prediction checkpoints", "predict",
    predict([
        ("""Before scrolling to the output: <b>write down</b> whether
<code>loop_out</code> and <code>mat_out</code> will be <i>exactly</i> equal, or equal to
within floating-point noise. Commit to one.""",
         """<p><b>Exactly equal</b> &mdash; <code>np.allclose</code> prints
<code>True</code>, and in fact they are bit-identical here.</p>
<p>People expect noise because the two routines look different. They are not different: the
loop computes each <code>np.dot(w, a_in)</code> separately and the matmul computes the same
products in the same order per column. There is no reassociation, so there is nothing to
round differently.</p>"""),
        ("""The demo net returns <code>out[1] = 0.679</code> for the input
<code>[0, 0]</code>. Before checking: with an input of all zeros, <b>where can a non-zero
output possibly come from?</b>""",
         """<p>From the <b>biases</b>, and only the biases. With <code>x = [0,0]</code> the
first layer computes <code>relu(b1) = relu([-1, 0, 0.25]) = [0, 0, 0.25]</code>. Then layer 2
gives <code>0.25 &times; 1.0 + 0.5 = 0.75</code>, and <code>sigmoid(0.75) = 0.679</code>.</p>
<p>This is the cleanest demonstration in the file that <b>b is not decoration</b>. Remove the
biases and a zero input can only ever produce sigmoid(0) = 0.5.</p>"""),
        ("""Roast #6 is <b>259.9&nbsp;&deg;C for 14.9 minutes</b>. The rule says good is
180&ndash;260&nbsp;&deg;C and 12&ndash;15 minutes, so it <b>is</b> good, with 0.1 to spare on
each. Predict <code>probs[5]</code>: above 0.5, or below?""",
         """<p><b>Below</b> &mdash; about <b>1.6e&minus;10</b>. The network calls a good roast
bad.</p>
<p>Look at <code>h[5] = [0, 0.475, 0, 0.401]</code>. Neither alarm is on, but <b>both are
about half on</b>, and the output unit subtracts 60 for each. Two half-alarms add up to
roughly a whole veto.</p>
<p>The lesson is not &ldquo;the network is broken&rdquo;. It is that <b>a sigmoid boundary is
soft</b>, and softness accumulates when several detectors are near their edges at once.</p>"""),
        ("""If you set every activation to the identity, the two-layer network becomes
equivalent to a single layer. Before running it: <b>what shape</b> is the single equivalent
weight matrix, and roughly what is in it?""",
         """<p><code>W_eq = W1 @ W2</code> has shape <b>(2, 1)</b> &mdash; two inputs straight
to one output, with the hidden layer gone entirely.</p>
<p>Its value is <b>[[4.0], [&minus;4.0]]</b> and <code>b_eq</code> is <b>[&minus;0.75]</b>.
Three units of hidden layer reduced to two numbers.</p>"""),
    ],
    """Write each answer down <b>before</b> opening the reveal. An answer you thought is not
an answer you committed to, and the whole value of this section is finding out which of your
beliefs were wrong.""")),

# ---------------------------------------------------------------- 3
section("3", "&#128295;", "Modify the copy", "lab",
    lab([
        ("L1", "Change a value",
         "Set <code>bd[0]</code> from 180 to 190, re-run, and read the new <code>h</code> "
         "column 0. Which roasts changed, and by how much?",
         "bd = np.array([ 190.0,   -260.0,      48.0,      -60.0 ])",
         """<p>Roast #4 (175&nbsp;&deg;C) was already flagged at 0.993 and now goes to
essentially 1.0. But watch roast #1 and #5, both at 200&nbsp;&deg;C: still 0, because 200 is
comfortably above 190 too.</p>
<p>You moved a threshold by 10&nbsp;&deg;C and only the roast <i>near</i> that threshold
noticed. That is what a steep sigmoid buys you.</p>"""),
        ("L2", "Change a parameter",
         "Set <code>K = 3.0</code> instead of 60.0 and re-run the roast checker. Does roast "
         "#6 &mdash; the one it currently gets wrong &mdash; get fixed?",
         "K = 3.0                      # was 60.0",
         """<p>No, it gets <b>worse everywhere</b>. <code>K</code> only scales the output
unit's veto strength, so lowering it makes every verdict mushy: good roasts stop reaching
1.0 and bad ones stop reaching 0.</p>
<p>The important distinction: the file's own sweep sharpens the <b>detectors</b>
(<code>Wd * sharp, bd * sharp</code>), not the output. Sharpening the wrong layer cannot fix
a boundary problem in the layer before it.</p>"""),
        ("L3", "Change the data",
         "Add a seventh roast at <b>exactly</b> 260.0&nbsp;&deg;C for 13.0 minutes &mdash; "
         "right on the boundary, in the middle of the duration band. Predict "
         "<code>h[6,1]</code> before you run it.",
         "tests = np.array([[200., 13.9], [200., 17.0], [285., 12.5],\n"
         "                  [175., 13.0], [220., 12.5], [259.9, 14.9],\n"
         "                  [260.0, 13.0]])",
         """<p><code>h[6,1]</code> is <b>exactly 0.5</b>. The detector computes
<code>T &minus; 260 = 0</code>, and <code>sigmoid(0) = 0.5</code> by definition.</p>
<p>So the network is <b>perfectly undecided</b> &mdash; and the output still comes out bad,
because half of a 60-point veto is still 30 points of veto. A point exactly on the boundary
is not a coin flip in this architecture; it is a rejection.</p>"""),
        ("L4", "Change an assumption",
         "The output unit assumes <b>any one alarm should veto</b>. Change it to require "
         "<b>two</b> alarms before rejecting, by halving each weight and keeping the bias. "
         "Does roast #6 now pass? Does anything else break?",
         "Wout = np.array([[-30.], [-30.], [-30.], [-30.]])   # was -60 each\n"
         "bout = np.array([30.])                              # unchanged",
         """<p>Roast #6 now <b>passes</b>: 0.475 and 0.401 half-alarms at &minus;30 each sum
to about &minus;26, against a bias of +30, so the output stays positive.</p>
<p>But you have broken the rule you were implementing. Roast #2 (200&nbsp;&deg;C,
<b>17 minutes</b>) has a single fully-on alarm worth &minus;30 against +30 &mdash; a dead
heat, output 0.5. A genuinely over-long roast is now judged a coin flip.</p>
<p>That is the real trade: you cannot loosen the AND gate to forgive borderline cases without
also loosening it for clear violations. The fix has to happen in the detectors, not the
gate.</p>"""),
        ("L5", "Explain it",
         "Without looking: write three sentences explaining why <code>h</code> has four "
         "columns when <code>tests</code> has two. Then explain what would have to change "
         "for it to have five.",
         None,
         """<p><code>h</code>'s column count is set by <b><code>Wd.shape[1]</code></b> &mdash;
the number of <b>units</b> in the layer &mdash; and has nothing to do with how many
measurements come in. Two measurements feed <b>all four</b> detectors; each detector reads
both and cares about one.</p>
<p>For five columns you would add a fifth column to <code>Wd</code> (shape becomes
<code>(2, 5)</code>), a fifth entry to <code>bd</code>, and a fifth row to <code>Wout</code>
(shape <code>(5, 1)</code>). Miss the last one and you get a shape error &mdash; which is the
system telling you a detector exists that nothing listens to.</p>"""),
    ],
    """Work on <b>a copy</b> of <code>03_neural_net_forward.py</code>, not the original. Each
level changes something one step further from the surface, and each asks for a prediction
before the edit.""")),

# ---------------------------------------------------------------- 4
section("4", "&#128165;", "Break it, then repair it", "break",
    breaks([
        ("W1 = np.array([[1.0, -1.0, 0.5],\n                [1.0,  2.0, -1.5],\n                [0.0,  0.0,  0.0]])   # a third row",
         "You have given <code>W1</code> a third input row while <code>batch</code> still "
         "has two columns. <b>Predict the exact error message and which line raises it</b>, "
         "then run it.",
         """<p><code>ValueError: matmul: Input operand 1 has a mismatch in its core dimension
0</code>, raised inside <code>dense</code> at <code>A_in @ W</code>.</p>
<p>The invariant it is protecting: <b>a weight matrix's first dimension must equal the
previous layer's width</b>. <code>(4,2) @ (3,3)</code> has inner dimensions 2 and 3, and
there is no sensible answer.</p>
<p>Notice what the error is <b>not</b> telling you: it does not say &ldquo;you added a row&rdquo;.
It says the shapes disagree, and locating <i>which</i> of the two you got wrong is your job.
That is why the shape ledger in section 1 is worth keeping.</p>"""),
        ("acts = [sigmoid, sigmoid]        # was [relu, sigmoid]",
         "Swap ReLU for sigmoid in the hidden layer and re-run the <b>demo net</b>. The "
         "outputs will change. <b>Is the network now wrong?</b>",
         """<p>No &mdash; it is a <b>different network</b>, not a broken one. Nothing here is
trained, so there is no correct answer to be further from.</p>
<p>What is worth noticing is the direction: outputs move towards the middle. The zero input,
which gave 0.679 with ReLU, now passes <code>sigmoid([-1, 0, 0.25])</code> forward as
<code>[0.269, 0.5, 0.562]</code> instead of <code>[0, 0, 0.25]</code> &mdash; so the second
layer receives three non-zero signals where before it received one.</p>
<p>The invariant: <b>ReLU passes zero through as zero; sigmoid never outputs zero.</b> That
single difference is why ReLU produces sparse activations and sigmoid does not.</p>"""),
        ("h = dense(tests, Wd.T, bd, sigmoid)      # note the .T",
         "Transpose <code>Wd</code> and run. This one is nastier: <b>predict whether it "
         "errors or silently returns something</b>.",
         """<p>It <b>errors</b> &mdash; <code>(6,2) @ (4,2)</code> is not legal.</p>
<p>But that is luck. If the layer had happened to be <b>square</b> &mdash; two inputs and two
detectors &mdash; the transpose would have run cleanly and returned confident, meaningless
numbers, with no warning at any point.</p>
<p>The invariant worth taking from this: <b>a shape check that passes is not a correctness
check.</b> The only real defence is knowing what each axis <i>means</i>, which is section 1's
whole job.</p>"""),
        ("bout = np.array([0.0])           # was 30.0",
         "Zero the output bias and re-run the roast checker. Predict what "
         "<code>probs</code> becomes for a <b>good</b> roast.",
         """<p><b>0.5</b>, for every good roast &mdash; and still ~0 for every bad one.</p>
<p>With no alarms firing the output unit computes exactly 0, and
<code>sigmoid(0) = 0.5</code>. The network can still say &ldquo;definitely bad&rdquo; but has
lost all ability to say &ldquo;good&rdquo;.</p>
<p>The invariant: in an AND gate built this way, <b>the bias is what &ldquo;nothing is
wrong&rdquo; is worth</b>. The weights supply the vetoes; the bias supplies the case for the
defence.</p>"""),
    ],
    """Each of these breaks something on purpose. In every case <b>predict the failure before
you run it</b> &mdash; including whether it fails loudly or quietly, which is the more
important half.""")),

# ---------------------------------------------------------------- 5
section("5", "&#9878;&#65039;", "The invariant", "invariant",
    invariant("""<p><b>The loop and the matrix multiply must produce identical numbers, and
two linear layers must collapse to exactly one.</b></p>""",
    """<p>These are the two claims this file exists to prove, and both are checked in the
file itself rather than asserted. The first says the vectorised form is not an approximation
of the loop &mdash; it <i>is</i> the loop. The second says depth without non-linearity is
worth nothing at all: <code>W1 @ W2</code> is a single (2,1) matrix that reproduces the
network's output to the last decimal.</p>
<p>If you ever modify <code>dense</code>, this is the check that tells you whether you broke
it. It needs no training, no data and no judgement &mdash; just equality.</p>""",
    """assert np.allclose(dense_loop(x, W1, b1), dense(x.reshape(1, -1), W1, b1)[0])
assert np.allclose(forward(batch, net, [identity, identity]),
                   batch @ (W1 @ W2) + (b1 @ W2 + b2))""")),

# ---------------------------------------------------------------- 6
section("6", "&#129535;", "Wrong mental models", "wrong",
    wrong([
        ("The hidden units learn what they detect &mdash; that is why they have names.",
         """<p>In <b>this</b> file nothing is learned. Every detector was written by hand:
<code>Wd</code> and <code>bd</code> encode the thresholds 180, 260, 12 and 15 directly.</p>
<p>The names are a story <i>we</i> attached to columns we designed. In a trained network the
units do organise into something useful, but nothing assigns them meanings, and the
combinations found are often not describable in words at all. The file makes this checkable
precisely because the meanings here are real &mdash; and hand-installed.</p>"""),
        ("A sigmoid detector is basically a threshold, so it is on or off.",
         """<p><code>h[5] = [0, <b>0.475</b>, 0, <b>0.401</b>]</code> is the counterexample,
and it is why roast #6 fails.</p>
<p>Near a boundary a sigmoid is genuinely <b>partly on</b>, and several partly-on detectors
combine. The file's grid sweep shows that steeper weights <b>shrink</b> that band and never
remove it &mdash; which is not a defect. It is exactly what lets a network express
&ldquo;probably good&rdquo; instead of only &ldquo;good&rdquo; or &ldquo;bad&rdquo;.</p>"""),
        ("More layers means more expressive power.",
         """<p>Only with a non-linearity between them. The <code>linear_collapse</code>
section runs the two-layer network with identity activations and gets
<code>[&minus;8.75, &minus;0.75, &minus;12.75, 19.25]</code> &mdash; and a single matrix
<code>W_eq = W1 @ W2</code> reproduces it exactly.</p>
<p>So a 100-layer linear network is algebraically identical to one layer and costs a hundred
times as much. <b>Depth is not the source of power; the kinks between the layers are.</b></p>"""),
        ("<code>units</code> has to relate somehow to the number of inputs.",
         """<p>It does not. <code>Wd</code> is <code>(2, 4)</code>: two measurements feeding
<b>four</b> detectors, and every detector reads <b>both</b> measurements.</p>
<p><code>units</code> sets the <b>width of the output</b> and nothing else. The input width
is fixed by whatever came before, and the two numbers are free to differ in either
direction.</p>"""),
        ("The network gets roast #6 wrong, so the weights are miscalibrated.",
         """<p>The weights implement the stated rule <b>exactly</b>. The disagreement is not
between the network and the rule &mdash; it is between a <b>hard</b> rule and a <b>soft</b>
implementation of it, evaluated 0.1 units from two boundaries at once.</p>
<p>No choice of finite weights removes that band. You can shrink it towards zero by
sharpening, and the file measures exactly that. Believing this is a calibration bug will send
you tuning numbers that were never wrong.</p>"""),
    ])),

# ---------------------------------------------------------------- 7
section("7", "&#127959;&#65039;", "Reconstruction challenge", "reconstruct",
    reconstruct([
        ("Explain",
         "Close the file. In four sentences, say what forward propagation does, without "
         "using the words <i>matrix</i> or <i>multiply</i>.",
         """<p>A good answer says roughly: each unit takes every number from the layer
before, weighs each one by how much it cares about it, adds its own default, and squashes the
result into a bounded range. All units in a layer do this at once and independently. Their
answers become the inputs of the next layer. Repeat until the last layer, whose output is the
prediction.</p>"""),
        ("Skeleton",
         "From memory, write the signature and docstring of <code>dense</code> and "
         "<code>forward</code> &mdash; no bodies. Get the argument order right.",
         """<p><code>dense(A_in, W, b, g=sigmoid)</code> and
<code>forward(X, params, activations)</code>, where <code>params</code> is a list of
<code>(W, b)</code> pairs.</p>
<p>The detail worth getting right: <code>forward</code> takes activations as a
<b>separate list</b>, parallel to params. That is what lets the same network be run with
<code>[relu, sigmoid]</code> and then with <code>[identity, identity]</code> for the collapse
demonstration, without rebuilding it.</p>"""),
        ("Core",
         "Write <code>dense</code> from scratch, vectorised, in one line of body. Then write "
         "<code>dense_loop</code> and assert they agree.",
         """<p><code>return g(A_in @ W + b)</code> is the whole body.</p>
<p>The loop version must slice <b>columns</b>: <code>w = W[:, j]</code>, and iterate
<code>range(W.shape[1])</code>. Using <code>W.shape[0]</code> is the classic slip &mdash; it
loops over inputs instead of units, and on a square W it runs without complaint.</p>"""),
        ("Minimal",
         "Build the smallest network that cannot be collapsed into one layer, and prove it "
         "cannot.",
         """<p>Two layers with <b>any</b> non-linearity between them &mdash; for instance
2&rarr;2&rarr;1 with ReLU. Prove it by computing <code>W1 @ W2</code> and showing that
<code>batch @ W_eq + b_eq</code> does <b>not</b> match the network's output, which is exactly
the comparison the <code>linear_collapse</code> section makes in reverse.</p>"""),
        ("Verify",
         "Rebuild the roast checker's four detectors from the rule alone &mdash; good is "
         "180&ndash;260&nbsp;&deg;C and 12&ndash;15 minutes &mdash; without looking at "
         "<code>Wd</code> or <code>bd</code>. Then compare.",
         """<p>Each detector needs to be positive exactly when its violation holds. For
&ldquo;too cool&rdquo;, you want positive when T &lt; 180, so the weight on temperature is
<b>&minus;1</b> and the bias is <b>+180</b>. For &ldquo;too hot&rdquo;, positive when
T &gt; 260, so weight <b>+1</b> and bias <b>&minus;260</b>.</p>
<p>The duration pair is the same with a scale factor of 4: <b>&minus;4</b> and <b>+48</b>,
then <b>+4</b> and <b>&minus;60</b>. If you derived &minus;1 and +12 instead, you have the
right boundary and a blunter detector &mdash; compare your <code>h</code> against the file's
and you will see your duration alarms respond more gradually.</p>"""),
    ],
    """Work down the list in order. Each stage is harder and each one has a way to check
yourself that does not require reading the answer first.""")),

# ---------------------------------------------------------------- 8
section("8", "&#128279;", "Connections", "conn",
    connections(
        [("lab", "../scratch/02-logistic-regression.html", "Back to 02 &mdash; logistic regression",
          "one neuron is <b>exactly</b> the unit built there: dot, bias, squash"),
         ("lab", "../scratch/01-linear-regression.html", "Back to 01 &mdash; linear regression",
          "the dot product inside every unit, and the shapes it needs")],
        [("lab", "../scratch/04-backpropagation.html", "On to 04 &mdash; backpropagation",
          "this file computes the forward arrow; 04 adds the backward one"),
         ("lab", "../scratch/05-softmax.html", "On to 05 &mdash; softmax",
          "replaces the single sigmoid output with N coupled ones")],
        "../gist/c21.html", "C2 Week 1 &mdash; the gist",
        extra=[("docs", "../reference.html", "Reference &mdash; the C2 W1 entries",
                "<code>c2w1-dense-cols</code>, <code>c2w1-shapes</code> and "
                "<code>c2w1-master-eq</code> cover the notation this file assumes"),
               ("play", "../map.html", "Concept map",
                "where forward propagation sits among the 82 cross-referenced terms")])),

# ---------------------------------------------------------------- 9
section("9", "&#9670;", "Recall sheet", "recall",
    recall([
        ("In this file, what is <code>h[3, 0] = 0.993</code> about a roast?",
         "Roast #4 ran at <b>175&nbsp;&deg;C</b>, and the <b>&ldquo;too cool&rdquo;</b> "
         "alarm is almost fully on &mdash; 175 is below the 180 threshold."),
        ("Which variable holds the roast checker&rsquo;s <b>thresholds</b>, and in what form?",
         "<code>bd = [180, &minus;260, 48, &minus;60]</code>. The biases <b>are</b> the "
         "boundaries: unit 1 computes &minus;T + 180, positive exactly when T &lt; 180."),
        ("Why is there a factor of <b>4</b> in <code>Wd</code>&rsquo;s duration row?",
         "Minutes span a far narrower range than degrees, so duration is amplified to make "
         "the two pairs of detectors comparably sharp. It is a scaling choice, not a fact "
         "about coffee."),
        ("What does <code>W_eq = W1 @ W2</code> equal, and what does that prove?",
         "<b>[[4.0], [&minus;4.0]]</b>, with <code>b_eq = [&minus;0.75]</code>. It proves "
         "two <b>linear</b> layers are exactly one linear layer &mdash; depth without a "
         "non-linearity buys nothing."),
        ("The demo net outputs <b>0.679</b> for the input <code>[0, 0]</code>. Where does a "
         "non-zero answer come from with a zero input?",
         "Entirely from the <b>biases</b>: <code>relu(b1) = [0, 0, 0.25]</code>, then "
         "<code>0.25 &times; 1.0 + 0.5 = 0.75</code>, and <code>sigmoid(0.75) = 0.679</code>."),
        ("Why does roast #6 (259.9&nbsp;&deg;C, 14.9 min) come out <b>bad</b> when the rule "
         "says good?",
         "<code>h[5] = [0, 0.475, 0, 0.401]</code> &mdash; <b>two half-fired alarms</b>. "
         "Neither is on, but at &minus;60 each they add up to enough veto. A sigmoid "
         "boundary is soft, and softness accumulates."),
        ("What sets the number of columns in <code>h</code>?",
         "<code>Wd.shape[1]</code> &mdash; the number of <b>units</b>. Nothing to do with "
         "how many measurements come in; all four detectors read both."),
    ],
    """Cover the answers. Say each one out loud <b>before</b> revealing &mdash; producing an
answer from memory is what makes it stick, and re-reading one does not.""")),

# ---------------------------------------------------------------- 10
section("10", "&#9989;", "Mastery check", "check",
    check([
        ("""Point at any element of <code>h</code> and state, in one sentence, what it is
about a specific roast &mdash; naming the roast, the measurement and the alarm.""",
         """<p>If you cannot do this without scrolling up, section 1 is the one to redo. This
is the single skill this page exists for: <b>never pass a variable whose real-world meaning
you cannot state out loud</b>.</p>"""),
        ("""Name the two variables in this file that have <b>no physical meaning at all</b>,
and say why pretending otherwise would cost you something.""",
         """<p><code>batch</code> and <code>x</code> &mdash; and by extension <code>out</code>,
which is a probability of nothing. Inventing an as-if reading for them trains a habit that
breaks the moment you meet a file where the numbers <b>do</b> mean something and your
invented story quietly disagrees with the real one.</p>"""),
        ("""Without running anything: a layer receives <code>(6, 4)</code> and its weight
matrix is <code>(4, 1)</code>. State the output shape and what each axis is.""",
         """<p><code>(6, 1)</code> &mdash; still <b>six roasts</b>, now <b>one verdict</b>
each. The 4 was summed away because it was the inner dimension.</p>
<p>This is exactly the <code>Wout</code> step, and being able to name the axes rather than
just the numbers is the difference between reading a shape and understanding it.</p>"""),
        ("""Explain why sharpening the <b>detectors</b> shrinks the band of disagreement but
sharpening the <b>output unit</b> does not.""",
         """<p>The uncertainty originates in the detectors: near a boundary they output
values between 0 and 1, and that is what the output unit receives. Sharpening the output unit
only makes it more decisive about the mushy input it was given &mdash; it cannot recover
information that was already lost.</p>
<p>The file demonstrates this by sweeping <code>Wd * sharp, bd * sharp</code> and watching the
disagreement band shrink, which is a different edit from changing <code>K</code>.</p>"""),
        ("""You add a fifth detector to <code>Wd</code> and the program crashes. Name the
<b>other two</b> things you forgot to change.""",
         """<p><code>bd</code> needs a fifth entry, and <code>Wout</code> needs a fifth row
&mdash; shape <code>(5, 1)</code>.</p>
<p>The crash is the system telling you a detector exists that nothing listens to. Worth
noticing that this is a <b>helpful</b> failure: the shape rule caught a genuine modelling
mistake, which it will not always do.</p>"""),
    ],
    """These do not repeat the <a href="../quiz/c21.html">C2 W1 mock quiz</a>, which already
covers parameter counting, the shape rule and the <code>[[200, 17]]</code> convention. Every
question here needs something you can only get from <b>this file</b>.""")),
    ],
)
