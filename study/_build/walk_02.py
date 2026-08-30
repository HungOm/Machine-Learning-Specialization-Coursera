# -*- coding: utf-8 -*-
"""The plain, line-by-line walkthrough for 02_logistic_regression.py.

Kept in its own module because it is longer than everything else in
scratch_meta put together, and because it is a different KIND of writing: the
prose notes say why a block exists, this says what each line does. Every number
quoted here is one this file actually printed at build time.
"""

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

"sigmoid": """
<p>This is the one genuinely new idea in the file. The weighted sum can come out as any
number at all — −40, 0, +17. A probability may not. The sigmoid is the funnel between
them:</p>
<ul>
<li>a big negative number → almost <b>0</b></li>
<li>exactly zero → exactly <b>0.5</b></li>
<li>a big positive number → almost <b>1</b></li>
</ul>
<p>You can read that straight off the output: <code>sigmoid([-2, 0, 2])</code> gives
<b>0.1192, 0.5, 0.8808</b>. Symmetric around the middle, and it never quite reaches either
end.</p>
<p><b>Why the function is written in two halves.</b> The textbook formula is
<code>1 / (1 + exp(-z))</code>. Try it at z = −1000 and the machine has to work out
<code>exp(1000)</code>, a number with 435 digits, which does not fit in a float. It
overflows and warns.</p>
<p>So the code splits: for <code>z ≥ 0</code> it uses <code>1/(1+exp(-z))</code>, and for
<code>z &lt; 0</code> it uses <code>exp(z)/(1+exp(z))</code>. Multiply the top and bottom
of the first by <code>exp(z)</code> and you get the second — they are the <b>same
formula rearranged</b>. Each half is chosen so the exponent it feeds to <code>exp</code>
is never positive, and <code>exp</code> of a negative number is a safe little value
between 0 and 1.</p>
<p>Hence the first output line: <code>sigmoid(-1000) = 0.0</code>, no warning.</p>
<p><b>You will meet a second spelling of this.</b> File 03 writes the same function as a
single <code>np.where(z >= 0, 1/(1+exp(-|z|)), exp(-|z|)/(1+exp(-|z|)))</code>. It is not
a different sigmoid &mdash; the two agree to the last bit over 20,001 values from −800 to
+800 and at ±10,000 as well.</p>
<p>But the reason it is safe is subtly different, and worth knowing.
<code>np.where</code> does <b>not</b> pick a branch and skip the other: it computes
<b>both</b> branches over the <b>whole</b> array and then chooses element by element. So
writing the obvious two formulas inside an <code>np.where</code> would still overflow —
the doomed half gets evaluated anyway. Both branches there use <code>-|z|</code>, which is
never positive whichever side you are on, and that is what makes it safe.</p>
<p>So: the version on this page is safe because each formula <b>only ever runs on the half
of the data it suits</b>. File 03's is safe because <b>neither formula can overflow in the
first place</b>. Same answer, two different ways of avoiding the same cliff.</p>
<p>The last line, <code>g(-z) == 1 - g(z)</code>, checks the symmetry: the chance of
passing at z and the chance of failing at −z are the same number. It prints
<b>True</b>.</p>
""",

"cost": """
<p>The cost answers one question: <b>how bad is this set of weights?</b> One number, so
two candidate models can be compared.</p>
<p>File 01 squared the miss. That will not do here. Suppose the model says “99% sure this
student passed” and the student failed. The plain error is 0.99 — which sounds small, and
it is not small at all. It is a catastrophe.</p>
<p><code>loss = -(y*log(f) + (1-y)*log(1-f))</code> looks forbidding and is really two
cases wearing one coat, because <b>y is always 0 or 1</b>, so one of the two terms is
always multiplied by zero and vanishes:</p>
<ul>
<li>The student <b>passed</b> (y = 1) → only <code>-log(f)</code> survives. Predict 0.99
and the cost is 0.01. Predict 0.01 and the cost is <b>4.6</b>.</li>
<li>The student <b>failed</b> (y = 0) → only <code>-log(1-f)</code> survives, and it
punishes confidence the other way.</li>
</ul>
<p>That is the whole design: right and confident is nearly free, unsure costs a little,
<b>wrong and confident costs enormously</b> — and it heads for infinity as the model
approaches total certainty about something false.</p>
<p><code>eps = 1e-12</code> and the <code>np.clip</code> line exist because of that
infinity. <code>log(0)</code> is undefined, so a probability that rounds to exactly 0 or 1
would crash the sum. Clipping nudges them to 0.000000000001 and 0.999999999999 — far
enough from the edge to be safe, close enough to change no answer.</p>
<p>The final term, <code>(lam / (2*len(y))) * np.sum(w**2)</code>, is the fine for large
weights. Note what is <b>not</b> in it: <code>b</code>. The bias is never penalised,
because it only shifts the boundary rather than steepening it.</p>
""",

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
