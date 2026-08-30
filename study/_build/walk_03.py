# -*- coding: utf-8 -*-
"""Line-by-line walkthrough for 03_neural_net_forward.py."""
from walkkit import p, expr, chain, chainset, steps, cases, values, point, ascii_art

PICTURE = ([
    ("in", "A batch of examples", "Four examples, two numbers each. Shape <b>(4, 2)</b>."),
    ("arw", "every example meets every neuron, in one matrix multiply"),
    ("op", "Hidden layer &mdash; 3 units",
     "<b>(4,2) @ (2,3) &rarr; (4,3)</b>. Each unit computes its own weighted sum, adds its "
     "own bias, and squashes."),
    ("arw", "ReLU: keep the positives, zero the negatives"),
    ("op", "Output layer &mdash; 1 unit",
     "<b>(4,3) @ (3,1) &rarr; (4,1)</b>. It reads the three hidden numbers, not the "
     "original two."),
    ("arw", "sigmoid, to make it a probability"),
    ("out", "One number per example", "Four answers, between 0 and 1."),
], "The whole program in one picture",
   "Nothing here learns. This file only computes what a network with GIVEN weights would "
   "output; file 04 works out how to change those weights.")

WALK = {

"prelude": (
    p("""One import and one function. The <b>sigmoid</b> here is written to be
overflow-proof &mdash; see file 02's sigmoid section for why, and for why this file spells
it differently.""")
    + point("""Nothing in this file <b>learns</b>. Every weight is either written down by
hand or chosen to make a point. This is <b>forward propagation</b> alone: given the weights,
what does the network compute? File 04 answers the other half.""")
),

"one_neuron": (
    p("""A neuron, in one line of code and three of arithmetic.""")
    + expr("z = np.dot(w, x) + b\nreturn g(z)", "dot, add the bias, squash")
    + p("""With <b>w = [2, &minus;1]</b>, <b>b = 0.5</b>, <b>x = [1, 3]</b>:""")
    + steps(["2 &times; 1 = <b>2</b>",
             "&minus;1 &times; 3 = <b>&minus;3</b>",
             "2 + (&minus;3) = <b>&minus;1</b>",
             "&minus;1 + 0.5 = <b>&minus;0.5</b>. That is <b>z</b>.",
             "g(&minus;0.5) = <b>0.377541</b>. That is <b>a</b>."])
    + point("""The docstring puts it best: <b>a neuron is a dot product wearing a squash
function.</b> That is the whole of it. A network with a billion parameters is doing exactly
this, a billion times.""")
    + p("""0.377 is below 0.5, so this neuron is leaning &ldquo;no&rdquo;. The negative
weight on the second input is what did it: a large x&#8322; actively pushes this neuron
<b>down</b>.""")
),

"layer_loop": (
    p("""A whole layer, written the obvious way &mdash; one neuron at a time.""")
    + expr("for j in range(units):\n    w = W[:, j]\n    a_out[j] = g(np.dot(w, a_in) + b[j])")
    + point("""<code>W[:, j]</code> means <b>all rows, column j</b>. So <b>columns are
neurons</b> &mdash; column j holds neuron j's personal weight vector.""")
    + p("""<code>W.shape[1]</code> is the number of <b>columns</b>, which is the number of
neurons. Using <code>[0]</code> instead gives the number of <b>inputs</b>, and if the two
happen to be equal &mdash; a square W &mdash; the loop runs and silently does the wrong
thing.""")
    + point("""This version is correct and it will never run on a GPU. The next section
fixes that without changing a single number.""")
),

"layer_matmul": (
    p("""The same layer, for a whole batch, with no loop at all.""")
    + expr("return g(A_in @ W + b)", "every example against every neuron, in one operation")
    + values([("loop version", "[0.952574, 0.993307, 0.022977]", ""),
              ("matmul version", "[0.952574, 0.993307, 0.022977]", ""),
              ("identical", "True", "not approximately &mdash; the same numbers")],
             "the check this block prints")
    + point("""<b>A_in @ W</b> is <b>(m, n_in) @ (n_in, n_out)</b>. The inner dimension
&mdash; the input size &mdash; is summed away, which is precisely the dot product each
neuron needed. The loop was never doing anything the matrix multiply cannot.""")
    + p("""<b>b</b> is <code>(n_out,)</code> and <b>broadcasts down the rows</b>: one bias
per neuron, applied to every example, without writing that loop either.""")
    + point("""This is the version that runs on a GPU, and it is the entire reason the
2010s happened. Same maths, same answer, a hundred times the throughput.""")
),

"network": (
    p("""Two layers, stacked, and a batch of four examples pushed through.""")
    + expr("for (W, b), g in zip(params, activations):\n    A = dense(A, W, b, g)",
           "the output of one layer becomes the input of the next")
    + point("""That loop <b>is</b> forward propagation. Three lines. Everything else in this
file is either building the pieces it calls or examining what came out.""")
    + values([("[1, 3]", "0.006693", "confidently no"),
              ("[0, 0]", "0.679179", "leaning yes"),
              ("[&minus;2, 1]", "0.000553", "very confidently no"),
              ("[4, &minus;1]", "0.999290", "very confidently yes")],
             "four examples through a 2-3-1 network")
    + p("""The network uses <b>ReLU</b> in the hidden layer and <b>sigmoid</b> at the
output. That is the standard arrangement: ReLU everywhere inside, and the output activation
chosen by what the task needs &mdash; here, a probability.""")
),

"shapes": (
    p("""Shape bookkeeping. This section exists because <b>shape errors are the thing that
actually breaks</b>, far more often than the maths.""")
    + ascii_art("""  input          (4, 2)
                    |
  layer 1:  (4,2) @ (2,3) + (3,)  ->  (4, 3)
                    |
  layer 2:  (4,3) @ (3,1) + (1,)  ->  (4, 1)
                    |
  output         (4, 1)""")
    + point("""Read the middle numbers: <b>2 meets 2</b>, then <b>3 meets 3</b>. Those are
the pairs that must match. The outer numbers &mdash; 4 and 3, then 4 and 1 &mdash; are the
answer.""")
    + p("""And read the whole journey as a sentence: <b>4 examples with 2 features become 4
examples with 3 hidden values, and then 4 examples with 1 answer.</b> The <b>4</b> never
changes, because you always have four examples.""")
    + values([("layer 1", "2&times;3 + 3", "6 weights, 3 biases = <b>9</b>"),
              ("layer 2", "3&times;1 + 1", "3 weights, 1 bias = <b>4</b>"),
              ("total", "13", "the whole network's learnable numbers")],
             "counting the parameters by hand")
    + point("""<b>13 parameters.</b> A large language model has hundreds of billions,
arranged exactly like this. The difference is entirely one of scale, and this is a genuinely
useful thing to have counted once by hand.""")
),

"linear_collapse": (
    p("""The most important experiment in the file: <b>what happens if you remove the
activations?</b>""")
    + expr("identity = lambda z: z", "an activation that does nothing at all")
    + values([("two linear layers", "[&minus;8.75, &minus;0.75, &minus;12.75, 19.25]", ""),
              ("one equivalent layer", "[&minus;8.75, &minus;0.75, &minus;12.75, 19.25]", ""),
              ("identical", "True", "")],
             "the network, against a SINGLE matrix computed from its weights")
    + point("""<b>Two linear layers are exactly one linear layer.</b> Not similar &mdash;
identical, to the last decimal, and the code proves it by building the equivalent single
matrix with <code>W1 @ W2</code>.""")
    + p("""So a 100-layer linear network has <b>exactly the same expressive power</b> as a
1-layer one, and costs a hundred times as much to run. Depth without non-linearity buys
nothing whatsoever.""")
    + point("""This is why activation functions exist. Not to squash, not to normalise
&mdash; <b>to stop the layers from collapsing into each other</b>. Each ReLU adds a kink,
and no amount of matrix multiplication can flatten a kink out.""")
),

"detectors": (
    p("""What does &ldquo;hidden units are feature detectors&rdquo; actually mean? This
section makes it concrete by <b>building four detectors by hand</b>.""")
    + p("""The rule to reproduce: a roast is good if the temperature is between <b>180 and
260</b> AND the duration is between <b>12 and 15</b> minutes.""")
    + cases([("Unit 1 &mdash; too cool?", "fires when <b>T &lt; 180</b>"),
             ("Unit 2 &mdash; too hot?", "fires when <b>T &gt; 260</b>"),
             ("Unit 3 &mdash; too short?", "fires when <b>D &lt; 12</b>"),
             ("Unit 4 &mdash; too long?", "fires when <b>D &gt; 15</b>")],
            "four hand-built detectors in the hidden layer")
    + p("""The output unit gives each detector a weight of <b>&minus;60</b> and itself a
bias of <b>+30</b>. So with nothing firing it outputs sigmoid(30) &asymp; 1, and <b>any
single detector firing</b> drags it to sigmoid(&minus;30) &asymp; 0.""")
    + point("""That is an <b>AND gate</b>, built out of neurons: good roast = NOT too cool
AND NOT too hot AND NOT too short AND NOT too long. Any one veto is enough.""")
    + values([("200 C, 13.9 min", "1.0000", "good &mdash; correct"),
              ("200 C, 17.0 min", "0.0000", "too long &mdash; correct"),
              ("285 C, 12.5 min", "0.0000", "too hot &mdash; correct"),
              ("175 C, 13.0 min", "0.0000", "too cool &mdash; correct"),
              ("220 C, 12.5 min", "1.0000", "good &mdash; correct"),
              ("259.9 C, 14.9 min", "0.0000", "<b>WRONG</b> &mdash; it wanted good")],
             "the hand-built network against six test roasts")
    + point("""The last row is the interesting one and it is <b>not a bug</b>. That roast
sits 0.1&deg; from one boundary and 0.1 min from another. A sigmoid boundary is <b>soft</b>:
near the edge a detector outputs something between 0 and 1, so the AND gate is genuinely
undecided. The next section shows this happening.""")
),

"detectors_inside": (
    p("""Open the hidden layer up and look at what it is actually producing. These four
numbers <b>are</b> the detectors.""")
    + values([("200 C, 13.9 min", "[0, 0, 0.001, 0.012]", "nothing firing &mdash; a good roast"),
              ("200 C, 17.0 min", "[0, 0, 0, 1]", "&ldquo;too long&rdquo; is fully on"),
              ("285 C, 12.5 min", "[0, 1, 0.119, 0]", "&ldquo;too hot&rdquo; is fully on"),
              ("175 C, 13.0 min", "[0.993, 0, 0.018, 0]", "&ldquo;too cool&rdquo;"),
              ("259.9 C, 14.9 min", "[0, 0.475, 0, 0.401]", "<b>two half-firing</b>")],
             "[too cool, too hot, too short, too long]")
    + point("""<b>Every row of zeros is a good roast.</b> The raw input was
<code>[temperature, duration]</code>; the hidden layer has transformed it into
<code>[too cool?, too hot?, too short?, too long?]</code> &mdash; which is a far more useful
description of the same coffee.""")
    + p("""That transformation is what <b>learned features</b> means. Here they were built
by hand so you can see them; in a trained network the same kind of thing emerges from
gradient descent, without anyone naming it.""")
    + point("""And the last row explains the WRONG answer above: <b>0.475 and 0.401</b>
&mdash; two detectors each about half-firing. Together they add up to enough veto to tip the
output past 0.5, even though neither alone would have. The grid sweep that follows shows
that sharpening the weights <b>shrinks</b> this uncertain band but can never remove it
&mdash; which is exactly what lets a network say &ldquo;probably good&rdquo; instead of only
&ldquo;good&rdquo; or &ldquo;bad&rdquo;.""")
),
}
