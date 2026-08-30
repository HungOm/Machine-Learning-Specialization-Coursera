# -*- coding: utf-8 -*-
"""The gist of F0 Week 1 — the maths, as one connected toolkit."""
from kit import decode, key, trap
from gistkit import gistline, flow, carried, chain, bynumbers, retell, ladder, h2
from walkkit import cases, values, point

X = [1.0, 2.0, 3.0]
Y = [3.0, 5.0, 8.0]
_m = len(X)
_mean_x = sum(X) / _m
_mean_y = sum(Y) / _m
_sxy = sum((x - _mean_x) * (y - _mean_y) for x, y in zip(X, Y))
_sxx = sum((x - _mean_x) ** 2 for x in X)
_var = sum((y - _mean_y) ** 2 for y in Y) / _m
_sd = _var ** 0.5

def _n(v, p=4):
    s = "%.*f" % (p, v)
    return s.rstrip("0").rstrip(".") if "." in s else s

GIST = dict(
    course="F0", week="1", title="The Maths You Actually Need", mins=11,
    lede="Nineteen lessons, and every one of them is a part of the same machine. This page "
         "shows the machine.",
    body="".join([
        gistline("""Nineteen separate-looking topics, and they are not nineteen topics. They
are the parts of one sentence: <b>add up how wrong you are, work out which way is downhill,
and step that way.</b> Every symbol in this week appears somewhere in that sentence."""),

        h2("🖼", "The week in one picture"),
        flow([
            ("in", "A table of numbers",
             "Rows are things, columns are facts about them. A <b>vector</b> is one row; a "
             "<b>matrix</b> is the whole table."),
            ("arw", "combine each row with a set of weights"),
            ("op", "The dot product",
             "Multiply position by position, add it all up. <b>One number out.</b> This is "
             "a prediction."),
            ("arw", "compare with the truth, for every row"),
            ("op", "Σ, and the mean",
             "<b>Σ</b> adds over all the rows; dividing by <b>m</b> makes it an average so "
             "a bigger table does not look worse."),
            ("arw", "now: which way should the weights move?"),
            ("op", "The derivative",
             "The slope. Its <b>sign</b> says which way is uphill; its <b>size</b> says how "
             "steep."),
            ("arw", "there is more than one weight"),
            ("op", "The partial derivative",
             "One slope per weight, each measured with the others held still. The curly "
             "<b>∂</b> is the only thing announcing that."),
            ("back", "Step, and repeat",
             "Subtract a little of each slope from its weight. That is learning."),
        ], cap="""Exponentials, logarithms and probability sit slightly to one side of this
loop — they are what you need once the prediction has to be a <b>probability</b> rather than
a number, which is Course 1 Week 3. Everything else in the week is on the path above."""),

        h2("🧰", "What each tool is FOR"),
        carried("""It is worth seeing the whole toolkit at once, with the job each piece
does. Nothing here is learned for its own sake.""",
                [("Function notation", "01", "names the machine, so you can talk about "
                                             "changing what is inside it"),
                 ("Slope", "04", "the whole idea of gradient descent, in its simplest form"),
                 ("Derivative", "05", "a slope for a curve, at one exact point"),
                 ("Partial derivative", "06", "one slope per weight — because models have "
                                              "more than one"),
                 ("Σ, summation", "07", "adds the error over every training example"),
                 ("Vectors, dot product", "09–10", "one row of data meets one set of "
                                                   "weights, giving one prediction"),
                 ("Matrices, shapes", "11–13", "all the rows and all the weights at once"),
                 ("e and logarithms", "14–15", "turn any number into a probability, and "
                                               "turn multiplying into adding"),
                 ("Probability, mean, variance", "16–17", "feature scaling, and anomaly "
                                                          "detection"),
                 ("The normal distribution", "18", "what &ldquo;unusual&rdquo; means, "
                                                   "numerically"),
                 ("min, max, argmax", "19", "the value, versus <b>where</b> the value is — "
                                            "which is how a classifier answers")]),

        h2("🔢", "The whole toolkit, on three numbers"),
        bynumbers("""Three points: <b>x = %s</b>, <b>y = %s</b>. Watch how many of the
week's tools it takes to fit a line through them — and notice that it is all of the ones on
the path above."""
                  % (", ".join(_n(v,1) for v in X), ", ".join(_n(v,1) for v in Y)),
                  [("the mean of x", _n(_mean_x, 4), "lesson 17 — and it is what centring uses"),
                   ("the mean of y", _n(_mean_y, 4), "same tool, other column"),
                   ("Σ (x−x̄)(y−ȳ)", _n(_sxy, 4), "lesson 07 does the adding; this is how "
                                                   "x and y move together"),
                   ("Σ (x−x̄)²", _n(_sxx, 4), "the same sum, with x against itself"),
                   ("the best slope", _n(_sxy / _sxx, 4), "divide one by the other — "
                                                           "lesson 04, rise over run"),
                   ("the best intercept", _n(_mean_y - (_sxy/_sxx)*_mean_x, 4),
                    "so the line passes through the middle of the data"),
                   ("variance of y", _n(_var, 4), "lesson 17"),
                   ("standard deviation", _n(_sd, 4), "the square root, so it is back in "
                                                      "the original units")],
                  close="""Six of the nineteen lessons, used together, to fit a line by
hand. Course 1 Week 1 does exactly this and calls it linear regression."""),

        h2("🗣", "The three symbols people stall on"),
        key("""<p>If any of the notation is still opaque, it is almost always one of these
three, and each has a one-line fix.</p>
<p><b>Σ</b> is a <code>for</code> loop somebody wrote down. Cover it with your thumb, read
what is to the right, then remember it happens once per example and gets added up.</p>
<p><b>∂</b> is a <code>d</code> that is announcing &ldquo;there are other variables and I
am holding them still&rdquo;. It is not a different kind of derivative.</p>
<p><b>x<sup>(i)</sup></b> with round brackets is <b>example i</b>, never a power. The
bracket style carries the meaning, every time, throughout the specialization.</p>"""),

        h2("🚧", "What this week deliberately leaves out"),
        trap("""<p><b>No proofs.</b> You are learning to <i>read and use</i> this notation,
not to derive it. That is the right trade for what comes next.</p>
<p><b>No integration.</b> Calculus here is one-directional: derivatives only. You will not
need the other half.</p>
<p><b>No linear algebra beyond shapes.</b> Eigenvectors and SVD wait for Week 3, and only
because PCA needs them.</p>
<p><b>Nothing about learning yet.</b> This week has no model, no cost and no data. It is the
alphabet, not the language.</p>"""),

        h2("🗣", "Say the week back"),
        retell([
            "What makes something a <b>function</b>, in one sentence.",
            "What a <b>slope</b> is, without using the word derivative.",
            "What a <b>derivative</b> adds to that, and why a curve needs it.",
            "Why more than one weight forces you into <b>partial</b> derivatives.",
            "What <b>Σ</b> does, and where the counter starts and stops.",
            "What a <b>dot product</b> takes in, and what comes out.",
            "The shape rule for multiplying two matrices, and which pair must match.",
            "Why <b>e</b> turns up wherever a probability is needed.",
            "The two jobs a <b>logarithm</b> does in machine learning.",
            "Why you square the deviations when computing a <b>variance</b>.",
            "The difference between <b>max</b> and <b>argmax</b>, and where you meet it.",
        ]),

        h2("🪜", "Where this week sits in the whole arc"),
        ladder("F0", """This is the notation everything else is written in, and it is the
only week whose <b>content</b> you will never be tested on directly. You will use every
piece of it, constantly, without it ever being the subject again. Time spent here is
repaid in every later week, and skipped time here shows up as every later week feeling
harder than it is."""),
    ]),
)
