# -*- coding: utf-8 -*-
"""The plain, line-by-line walkthrough for 02_logistic_regression.py.

Kept in its own module because it is longer than everything else in
scratch_meta put together, and because it is a different KIND of writing: the
prose notes say why a block exists, this says what each line does. Every number
quoted here is one this file actually printed at build time.
"""
from walkkit import (p, expr, chain, chainset, steps, cases, values, point,
                     ascii_art)

PICTURE = ([
    ("in", "Eighty students",
     "Two exam scores each. Forty failed (label <b>0</b>), forty passed (label <b>1</b>). "
     "The two groups overlap on purpose, so no line can separate them perfectly."),
    ("arw", "start with every weight at zero"),
    ("loop", "repeat 5,000 times", [
        ("op", "Add up the scores, weighted",
         "<var>z</var> = exam1×<var>w</var><sub>1</sub> + exam2×<var>w</var><sub>2</sub> "
         "+ <var>b</var>. Any number at all comes out: −40, 0, +17."),
        ("arw", "but a probability has to sit between 0 and 1"),
        ("op", "Squash it — the sigmoid",
         "Turns any number into a probability. Very negative → near 0. Zero → exactly 0.5. "
         "Very positive → near 1."),
        ("arw", "compare that probability with what actually happened"),
        ("op", "Score the guess — the log loss",
         "Confident and right costs almost nothing. Unsure costs a bit. "
         "<b>Confident and wrong costs enormously.</b> That asymmetry is the whole point."),
        ("arw", "plus a fine for large weights (that is λ)"),
        ("op", "Which way is downhill",
         "One slope per weight — the identical formula to linear regression, with the "
         "sigmoid in place of the straight line."),
        ("back", "Nudge every weight",
         "Each weight steps a little way downhill. Repeat."),
    ]),
    ("arw", "the cost stops falling"),
    ("out", "A probability for any student",
     "Feed it two exam scores and it returns the chance of passing."),
    ("arw", "and only then, separately, choose a cut-off"),
    ("stop", "Pass or fail",
     "0.5 is the usual line, but it is a <b>decision you make</b>, not something the "
     "model learned. Move it and precision and recall move with it."),
], "The whole program in one picture",
   "Compare this with file 01. Every box is the same except two: a squash after the "
   "weighted sum, and a different way of scoring the guess. That is the entire "
   "difference between predicting a number and predicting a class.")

WALK = {

"prelude": """
<p>The file opens by importing NumPy and nothing else. No scikit-learn, no TensorFlow —
everything below is arithmetic you could do by hand if you had the patience.</p>
<p>Worth naming the goal before the code starts. File 01 answered <b>“how much?”</b>
&mdash; a house is worth $420,000. This file answers <b>“which of two?”</b> &mdash; this
student passes, that one does not. Everything that changes, changes because of that.</p>
""",

"data": """
<p><code>rng = np.random.default_rng(7)</code> makes a random-number generator. The
<b>7</b> is a seed: it means “use the same recipe for randomness every time”, so you and
this page get the identical eighty students on every run. Change the 7 and you get a
different class of students, and every number below shifts.</p>
<p><code>rng.normal([45, 50], 12, size=(40, 2))</code> invents forty students whose two
exam scores hover <b>around 45 and 50</b>, give or take about 12. These are the ones who
failed. The next line does the same around <b>70 and 72</b> for the forty who passed.</p>
<p><code>np.vstack</code> means <b>stack vertically</b> — put the failing forty on top of
the passing forty to make one table of eighty rows and two columns. <code>np.r_</code>
builds the answer column the same way: forty zeros, then forty ones.</p>
<p>So the shapes are <code>X</code> = (80, 2) and <code>y</code> = (80,), which is exactly
what <code>m = 80, n = 2</code> in the output means: <b>m</b> is how many students,
<b>n</b> is how many scores each one has.</p>
<p>The two clouds deliberately overlap. A neat, perfectly separable dataset would let the
weights grow forever and would hide everything this file is trying to show about λ.</p>
""",

"sigmoid": (
    p("""This is the one genuinely new idea in the file. The weighted sum can come out as
<b>any</b> number at all. A probability may not &mdash; it has to sit between 0 and 1. The
sigmoid is the funnel between them.""")
    + ascii_art("""  1.0 |                        _____----------
      |                  __--
      |               _--
  0.5 |- - - - - - - -*
      |            _--
      |       __---
  0.0 |------
      +----------------------------------------
           negative        0        positive
                        z""",
       "Very negative goes to 0, very positive goes to 1, and it passes through "
       "exactly 0.5 at z = 0.")
    + values([("sigmoid(&minus;2)", "0.1192", "well below the middle &mdash; probably no"),
              ("sigmoid(0)", "0.5", "exactly undecided"),
              ("sigmoid(2)", "0.8808", "well above &mdash; probably yes"),
              ("sigmoid(&minus;1000)", "0.0", "and no overflow warning, which is the point "
                                              "of the next bit")],
             "what this block actually printed")
    + p("""Notice it is symmetric: 0.1192 and 0.8808 add to exactly 1. That is the last
line of the output checking itself &mdash; the chance of passing at <b>z</b> and the chance
of failing at <b>&minus;z</b> are the same number.""")
    + p("""<b>Now, why is the function written in two halves?</b> The textbook formula is
one line:""")
    + expr("1 / (1 + exp(-z))", "the version in every textbook, and it breaks")
    + p("""Try it at <b>z = &minus;1000</b>. The machine has to work out
<code>exp(1000)</code> &mdash; a number with 435 digits. It does not fit in a float. It
overflows and warns, and you get nonsense.""")
    + cases([("When z is 0 or above",
              "<code>1 / (1 + exp(-z))</code><br>The exponent <b>&minus;z</b> is negative "
              "or zero, so <code>exp</code> stays small and safe."),
             ("When z is below 0",
              "<code>exp(z) / (1 + exp(z))</code><br>Now the exponent <b>z</b> is the "
              "negative one, so again <code>exp</code> stays small and safe.")],
            "so the code splits in two, and each half is safe where it is used")
    + point("""These are not two different formulas. Multiply the top and bottom of the
first by <code>exp(z)</code> and you get the second exactly. Same maths, rearranged so that
whichever side of zero you are on, <b>the thing being exponentiated is never
positive</b>.""")
    + p("""<b>You will meet a second spelling of this.</b> File 03 writes it as a single
<code>np.where</code>. It is not a different sigmoid &mdash; the two agree to the last bit
over 20,001 values from &minus;800 to +800, and at &plusmn;10,000 too.""")
    + p("""But it is safe for a different reason, and the difference is worth knowing.
<code>np.where</code> does <b>not</b> pick a branch and skip the other: it computes
<b>both</b> branches over the <b>whole</b> array, then chooses element by element. So
putting the obvious two formulas inside an <code>np.where</code> would still overflow
&mdash; the doomed half runs anyway. File 03 uses <code>-|z|</code> in <i>both</i>
branches, which is never positive whichever side you are on.""")
    + cases([("This page's version is safe because&hellip;",
              "each formula <b>only ever runs on the half of the data it suits</b>."),
             ("File 03's version is safe because&hellip;",
              "<b>neither formula can overflow in the first place</b>.")],
            "same answer, two different ways of avoiding the same cliff")
),

"cost": (
    p("""The cost answers one question: <b>how bad is this set of weights?</b> One number,
so that two candidate models can be compared.""")
    + p("""File 01 squared the miss. That will not do here. Suppose the model says
&ldquo;99% sure this student passed&rdquo; and the student <b>failed</b>. The plain error
is 0.99, which <i>sounds</i> small. It is a catastrophe, and the cost has to say so.""")
    + expr("loss = -( y * log(f) + (1 - y) * log(1 - f) )",
           "&ldquo;minus, y times log f, plus one minus y times log one minus f&rdquo;",
           "the log loss")
    + p("""It looks forbidding and it is really <b>two cases wearing one coat</b>. Because
<b>y is always 0 or 1</b>, one of the two halves is always multiplied by zero and
disappears.""")
    + cases([("If the student PASSED &nbsp;(y = 1)",
              "<code>1 - y</code> is 0, so the right half vanishes.<br>Only "
              "<code>-log(f)</code> is left."),
             ("If the student FAILED &nbsp;(y = 0)",
              "<code>y</code> is 0, so the left half vanishes.<br>Only "
              "<code>-log(1-f)</code> is left.")],
            "one of these two is always zero")
    + chainset([(["said 0.99", "cost 0.01"], "confident and right &mdash; almost free"),
                (["said 0.60", "cost 0.51"], "unsure &mdash; charged a little"),
                (["said 0.01", "cost 4.61"], "confident and <b>wrong</b> &mdash; 460&times; more")],
               "the student passed. What each guess costs")
    + point("""Right and confident is nearly free. Unsure costs a little. <b>Wrong and
confident costs enormously</b> &mdash; and the cost runs off towards infinity as the model
approaches total certainty about something false. That asymmetry is not a side effect. It
is the entire reason this cost exists instead of the squared error.""")
    + p("""Which is also why the next two lines are there:""")
    + expr("eps = 1e-12\nf = np.clip(f, eps, 1 - eps)", "keep f away from the cliff edges")
    + p("""<code>log(0)</code> is undefined &mdash; it heads for minus infinity &mdash; so a
probability that rounds all the way to 0 or 1 would poison the whole sum.
<code>np.clip</code> nudges them to 0.000000000001 and 0.999999999999: far enough from the
edge to be safe, close enough to change no answer you care about.""")
    + p("""The last term is the fine for large weights:""")
    + expr("(lam / (2 * len(y))) * np.sum(w ** 2)",
           "&lambda; times how big the weights have grown")
    + point("""Notice what is <b>not</b> in that term: <code>b</code>. The bias is never
penalised. Shrinking <b>w</b> flattens the model&rsquo;s confidence, which is the point;
shrinking <b>b</b> would only drag the boundary towards the origin, for no reason at
all.""")
),

"gradient": """
<p>Here is the payoff for all of file 01. Read these two lines next to the linear
regression ones and they are <b>character for character the same</b>:</p>
<p><code>err = sigmoid(X @ w + b) - y</code> — the only difference in the entire gradient
is that <code>sigmoid(...)</code> sits where the bare line used to be. That is not a
coincidence or a convenience; it falls out of the algebra, and it is why the log loss is
the “right” cost for a sigmoid rather than an arbitrary one.</p>
<p><code>X.T @ err</code> is the same weighted sum you met in file 01: each student's miss
multiplied by that student's scores, added up. <code>.T</code> is the transpose — it turns
the table on its side so the shapes line up: (2, 80) @ (80,) → (2,), one slope per
weight.</p>
<p><code>+ (lam / m) * w</code> is the penalty's own slope. A large weight gets a large
push back towards zero; a weight already near zero is barely touched.</p>
<p>And <code>dj_db</code> has no <code>lam</code> term at all, matching the cost: <b>b is
never regularized</b>.</p>
""",

"check_gradient": """
<p>This block is a test, and it is the reason to trust everything after it.</p>
<p>There are two ways to find a slope. You can <b>do the calculus</b> — that is
<code>compute_gradient</code>. Or you can <b>measure it</b>: nudge one weight up by a
hair, nudge it down by a hair, see how much the cost moved, and divide. That is
<code>numeric_gradient</code>, and <code>eps = 1e-6</code> is the size of the hair.</p>
<p>The measured version is far too slow to train with — it re-runs the whole cost twice
for every single weight — but it needs no calculus, so it cannot repeat a calculus
mistake. If the two agree, the derivative was differentiated correctly.</p>
<p>Look at the output. Both come out as <b>[-0.33510702, -0.36844957]</b> and the largest
disagreement is <b>6.785e-11</b> — a decimal point followed by ten zeros. That is the
noise floor of floating-point arithmetic, not an error.</p>
<p>This is a real professional habit, not a teaching exercise. A wrong gradient does not
crash. It trains happily and converges to the wrong answer, and this ten-line check is how
you find out.</p>
""",

"train": """
<p><code>w, b = np.zeros(X.shape[1]), 0.0</code> starts every weight at zero. Follow what
that means on the first iteration: <code>z</code> is 0 for every student, so
<code>sigmoid(0)</code> is 0.5, so the model's opening position is <b>“every student has a
50-50 chance”</b>. It knows nothing, and it says so.</p>
<p>Then the loop, three lines, repeated 5,000 times: work out which way is downhill, step
that way, repeat.</p>
<p><code>Xs = (X - X.mean(0)) / X.std(0)</code>, back in the check block, is why it works
at all. Raw exam scores run 20–100; after scaling they run about −2 to +2. Without that,
one weight needs a big step and the other a small one, and a single <code>alpha</code>
cannot suit both.</p>
<p>The printed cost tells the story: <b>0.568</b> at the start, <b>0.121</b> by iteration
1,000, and then 0.12139 forever. It has stopped improving by a fifth of the way in — the
remaining 4,000 iterations change nothing. The final weights are <b>w = [4.72, 2.85]</b>
and <b>b = −0.095</b>, meaning the first exam matters roughly 1.7 times as much as the
second.</p>
""",

"evaluate": """
<p>The model outputs probabilities. A decision needs a yes or a no, so
<code>(prob >= 0.5)</code> draws the line. The comment in the file — “the threshold is a
separate choice” — is the important part: <b>0.5 is not something the model learned</b>.
You chose it, and you may choose differently.</p>
<p><code>.astype(int)</code> just turns True/False into 1/0 so it can be compared with
<code>y</code>.</p>
<p>The four counts are the four things that can happen, and they are worth saying slowly.
Treating “passed” as the positive case:</p>
<ul>
<li><b>TP = 38</b> — said pass, did pass. Correct.</li>
<li><b>TN = 38</b> — said fail, did fail. Correct.</li>
<li><b>FP = 2</b> — said pass, actually failed. A <i>false alarm</i>.</li>
<li><b>FN = 2</b> — said fail, actually passed. A <i>miss</i>.</li>
</ul>
<p><b>Precision</b> = 38/(38+2) = <b>0.95</b>: when it says pass, how often is it right?
<b>Recall</b> = 38/(38+2) = <b>0.95</b>: of everyone who really passed, how many did it
find? They are equal here only because FP and FN happen to both be 2. <b>F1</b> combines
them into one number, and it is 0.95 too.</p>
<p>Accuracy is 0.95 as well — 76 right out of 80. It agrees with the others here because
the classes are balanced, forty and forty. On a lopsided problem it stops agreeing, and
that is precisely when precision and recall earn their keep.</p>
""",

"boundary": """
<p>Where exactly does the model change its mind? At the probability 0.5. And sigmoid gives
0.5 at exactly one input: <b>z = 0</b>.</p>
<p>So the dividing line is wherever <code>w₁x₁ + w₂x₂ + b = 0</code>. Rearranging for
<code>x₂</code> gives the line the code prints:
<code>x₂ = -(w₁x₁ + b) / w₂</code>.</p>
<p>Three points off that line appear in the output: at x₁ = −1 the boundary is at
x₂ = +1.690; at x₁ = 0 it is at +0.033; at x₁ = +1 it is at −1.623. Three points, dropping
steadily — it is a <b>straight line</b>, sloping down.</p>
<p>Which is the honest limit of this model. Everything on one side is called a pass,
everything on the other a fail, and the frontier between them is straight. It cannot curve
around an island of failing students sitting in the middle of the passing ones.</p>
<p>These numbers are in <b>scaled</b> space, because the model was trained on scaled data.
To draw the line on a chart of real exam marks you would have to undo the scaling
first.</p>
""",

"regularization": """
<p>This block runs the whole training four times with a bigger λ each time, and prints two
things: how big the weights got, and how accurate it was.</p>
<p><code>np.linalg.norm(wl)</code> is the length of the weight vector — roughly “how big
are all the weights together”. Read the column down:</p>
<ul>
<li>λ = 0 → <b>|w| = 5.52</b>, accuracy 0.950</li>
<li>λ = 1 → <b>|w| = 2.93</b>, accuracy 0.963</li>
<li>λ = 10 → <b>|w| = 1.28</b>, accuracy 0.963</li>
<li>λ = 100 → <b>|w| = 0.32</b>, accuracy 0.963</li>
</ul>
<p>The weights shrink by a factor of seventeen and the accuracy <b>goes up and stays
up</b>. That is the argument for regularization in four lines: the same decisions, made
with less confidence, and the confidence was never earned in the first place.</p>
<p>What is actually happening: with λ = 0 nothing stops the weights growing, so the model
pushes every probability towards 0.000 or 1.000 — it becomes certain. λ charges a fee for
that certainty. The boundary stays in nearly the same place; the model just stops shouting
about it.</p>
""",

"decay_limit": """
<p>The last block is the trap, and it is not in any lecture.</p>
<p>Look at what the regularized update does to <code>w</code> before the gradient is even
applied. Combining the two terms gives
<code>w := w(1 − αλ/m) − α × gradient</code>. So every step multiplies the weights by
<code>1 − αλ/m</code>. Call that the <b>shrink factor</b>.</p>
<ul>
<li>factor <b>0.9</b> → the weight gently shrinks: 10 → 9 → 8.1. Fine.</li>
<li>factor <b>−0.5</b> → the weight <b>flips sign</b> every step: 10 → −5 → 2.5. Ugly, but
still shrinking.</li>
<li>factor <b>−5.25</b> → it flips <b>and</b> grows every step. Gone.</li>
</ul>
<p>The output walks straight through those cases. α = 0.5 with λ = 100 gives a factor of
0.375 and settles at |w| = 0.32. Push λ to 320 and the factor hits exactly −1.000, which
is the knife edge: it does not blow up but it does not settle either, ending at
<b>|w| = 538</b>. At λ = 1000 the factor is −5.25 and it <b>diverges</b>.</p>
<p>Then the last line of the block fixes it without touching λ at all: keep λ = 1000 and
drop α to 0.05, and the factor is back to 0.375 and the weights land at 0.041.</p>
<p>So the rule: you are safe while <code>αλ/m &lt; 2</code>, that is
<code>α &lt; 2m/λ</code>. With m = 80 and λ = 1000 that means <b>α must be below
0.160</b>.</p>
<p>The lesson to carry: <b>α and λ are not independent knobs.</b> A λ that is perfectly
safe at one learning rate destroys the model at another, and the failure looks like
“training diverged”, which sends most people hunting for a bug in the gradient.</p>
""",
}
