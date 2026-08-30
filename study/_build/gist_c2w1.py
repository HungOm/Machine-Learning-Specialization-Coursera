# -*- coding: utf-8 -*-
"""The gist of C2 Week 1."""
import math
from kit import key, trap
from gistkit import gistline, flow, sameskel, chain, bynumbers, retell, ladder, h2
from walkkit import cases, values, point, expr, chainset

_sig = lambda z: 1 / (1 + math.exp(-z))
_z = 2*1 + (-1)*3 + 0.5

GIST = dict(
    course="C2", week="1", title="Neural Networks", mins=12,
    scratch=["03-forward-propagation"],
    lede="Sixteen lessons, and the unit at the centre of all of them is something you built "
         "in Course 1. What is new is the wiring.",
    body="".join([
        gistline("""One neuron is <b>exactly</b> one logistic regression unit — a dot
product, a bias, a squash. Stack a few side by side and you have a layer; stack layers and
the middle ones start inventing their own features. That invention is the entire reason
neural networks exist, and this week is about computing it, not learning it."""),

        h2("🖼", "The week in one picture"),
        flow([
            ("in", "A batch of examples", "<b>(m, n)</b> — rows are examples, columns are "
                                          "features. Same convention as always."),
            ("arw", "every example meets every neuron, in ONE matrix multiply"),
            ("op", "A layer",
             "<b>A @ W + b</b>, then squash. <b>W</b> is (inputs, units) — <b>columns are "
             "neurons</b>. Output is (m, units)."),
            ("arw", "the output of one layer is the input of the next"),
            ("op", "Another layer",
             "It reads the <b>hidden values</b>, not the original features. That is the "
             "whole point."),
            ("arw", "keep going, as deep as you like"),
            ("op", "The output layer",
             "Its activation is chosen by the task: sigmoid for yes/no, softmax for "
             "one-of-many, linear for a number."),
            ("out", "A prediction per example", "<b>(m, 1)</b>, or (m, classes)."),
        ], cap="""Nothing here learns. This week computes what a network with <b>given</b>
weights would output — that is <b>forward propagation</b>. Where the weights come from is
next week."""),

        h2("🔁", "Same skeleton, and what changed"),
        sameskel("""A neuron computes <b>z = w·x + b</b>, then <b>a = g(z)</b>. That is
Course 1 Week 3, unchanged, down to the letters. Feature scaling still matters, the shapes
still have to line up, and the dot product is still doing the work.""",
                 [("How many units", "one", "<b>many</b>, arranged in layers"),
                  ("Where features come from", "<b>you</b> engineered them", "the hidden "
                                                                             "layers "
                                                                             "<b>invent</b> them"),
                  ("The prediction", "<code>g(w·x + b)</code>", "the same, applied layer "
                                                                "after layer"),
                  ("The maths per unit", "a dot product and a squash", "<b>identical</b>"),
                  ("The notation", "x<sup>(i)</sup> for examples", "a<sup>[l]</sup> for "
                                                                   "<b>layers</b> — square "
                                                                   "brackets, never a power"),
                  ("The guarantee", "one bowl, one minimum", "<b>gone</b> — the cost "
                                                             "surface is lumpy now")]),

        h2("🔢", "One neuron, by hand"),
        bynumbers("""<b>w = [2, &minus;1]</b>, <b>b = 0.5</b>, <b>x = [1, 3]</b>. Two steps,
and they are the same two steps at every unit of every layer.""",
                  [("2 &times; 1", "2", "first feature times its weight"),
                   ("&minus;1 &times; 3", "&minus;3", "second feature times its weight"),
                   ("sum", "&minus;1", "the dot product"),
                   ("plus the bias", "&minus;0.5", "this is <b>z</b>"),
                   ("g(&minus;0.5)", "%.4f" % _sig(_z), "this is <b>a</b> — the activation")],
                  close="""0.378 is below 0.5, so this neuron is leaning &ldquo;no&rdquo;.
The negative weight on the second input did it. A network with a billion parameters is doing
exactly this, a billion times, and nothing else."""),

        h2("📐", "The shape bookkeeping, which is what actually breaks"),
        values([("input", "(4, 2)", "4 examples, 2 features"),
                ("layer 1", "(4,2) @ (2,3) &rarr; (4, 3)", "the <b>2</b>s must match; the "
                                                           "outers are the answer"),
                ("layer 2", "(4,3) @ (3,1) &rarr; (4, 1)", "the <b>3</b>s must match"),
                ("parameters", "9 + 4 = <b>13</b>", "2&times;3+3, then 3&times;1+1")],
               "a 2-3-1 network on a batch of four")
        + key("""<p>Read the journey as a sentence: <b>4 examples with 2 features become 4
examples with 3 hidden values, then 4 examples with 1 answer.</b> The <b>4</b> never changes,
because you always have four examples.</p>
<p>Two rules make every shape question answerable. <b>Columns of W are neurons</b>, so
<code>W.shape[1]</code> is the unit count. And a weight vector's length always equals
<b>the width of the previous layer</b> — never its own.</p>
<p>Count the parameters by hand once. 13 here; a large language model has hundreds of
billions arranged identically, and the difference is entirely scale.</p>"""),

        h2("⛓", "The pieces, in the order they hand to each other"),
        chain([
            dict(name="The neuron",
                 does="A dot product wearing a squash function. That is the whole of it.",
                 say="z equals w dot x plus b; a equals g of z.",
                 code="a = g(np.dot(w, x) + b)",
                 trap="It needs a <b>dot</b> product, not elementwise multiplication — a "
                      "neuron must produce a <b>single number</b>, and <code>*</code> leaves "
                      "you holding a list.",
                 feeds="one number. Now put several of them side by side."),
            dict(name="The layer",
                 does="Several neurons reading the same input. They never talk to each "
                      "other, which is exactly what lets them be computed together.",
                 code="A_out = g(A_in @ W + b)",
                 trap="<code>units=3</code> sets the <b>length of the output</b>. Not the "
                      "number of inputs, not the number of examples. And <b>b broadcasts</b> "
                      "down the rows: one bias per neuron, applied to every example.",
                 feeds="a vector of activations — which the next layer treats exactly like "
                       "input data."),
            dict(name="Forward propagation",
                 does="Run the layers in order, feeding each one's output into the next.",
                 code="for (W, b), g in zip(params, acts):\n    A = dense(A, W, b, g)",
                 trap="<b>a<sup>[0]</sup> = x.</b> The input is defined as layer 0's output, "
                      "so the formula needs no special case for the first layer.",
                 feeds="a prediction — computed, not learned. Learning is next week."),
        ]),

        h2("🧠", "What a hidden layer actually buys you"),
        key("""<p><b>Learned features.</b> In C1 W2 you invented <code>x&#8321;x&#8322;</code>
by hand, using what you knew about houses. A hidden layer invents its own intermediate
features and works out which are worth keeping.</p>
<p>The build lane's file 03 makes this concrete by building four detectors <b>by hand</b> —
&ldquo;too cool&rdquo;, &ldquo;too hot&rdquo;, &ldquo;too short&rdquo;, &ldquo;too long&rdquo;
— and then ANDing them in the output unit. You can look inside the layer and see the raw
input <code>[temperature, duration]</code> turned into
<code>[too cool?, too hot?, too short?, too long?]</code>, which is a far more useful
description of the same coffee.</p>
<p>One honest warning: the <b>names</b> are a story told afterwards. Nothing in training
assigns meanings, and the combinations a trained network finds are often not describable in
words at all.</p>"""),

        h2("🚧", "What this week deliberately cannot do yet"),
        trap("""<p><b>It cannot learn.</b> Every weight this week is either handed to you or
written down by hand. Backpropagation is Week 2, and it is the harder half.</p>
<p><b>It has lost Course 1's guarantee.</b> The cost surface of a network is lumpy, with many
local dips. Where you start now genuinely matters, which is why initialisation is random and
never zero.</p>
<p><b>It cannot yet pick more than one of many.</b> Sigmoid answers yes/no. Softmax, for
one-of-N, arrives next week.</p>"""),

        h2("🗣", "Say the week back"),
        retell([
            "What one neuron computes, and which Course 1 algorithm it is identical to.",
            "What a layer is, and what <code>units=3</code> does and does not control.",
            "Which way round the rows and columns of <b>W</b> go, and why that orientation.",
            "How long <b>w<sub>2</sub><sup>[3]</sup></b> is in a 4→5→3→1 network, and why.",
            "The difference between <b>(2,)</b> and <b>(1, 2)</b>, and which Keras wants.",
            "The matrix shape rule, and which pair gets summed away.",
            "Why a neuron needs a dot product rather than elementwise multiplication.",
            "How many parameters a layer with n inputs and p units has.",
            "What <b>a<sup>[2]</sup></b> means and what it definitely does not.",
            "What a hidden layer buys you over the feature engineering you did in C1 W2.",
            "The three things that changed in the 2010s, given that the maths is from 1958 and 1986.",
        ]),

        h2("🪜", "Where this week sits in the whole arc"),
        ladder("C2 W1", """This is the wiring diagram. You can now say exactly what a network
<b>computes</b> — every shape, every dot product, every activation — without yet knowing where
its weights come from. That split is deliberate and it is worth respecting: forward
propagation is bookkeeping you can fully verify by hand, and backpropagation is the part that
needs a gradient check. Get the shapes solid here and next week is one new idea rather than
two."""),
    ]),
)
