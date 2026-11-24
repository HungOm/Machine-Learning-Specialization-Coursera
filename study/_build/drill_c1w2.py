# -*- coding: utf-8 -*-
"""Quiz drills — C1 W2. One concept per mock-quiz question, four methods each.

Every number below is COMPUTED here at import time and formatted into the text,
never typed. If a value is wrong, it is wrong in the arithmetic, where you can
see it, not in a sentence.
"""
import numpy as np
from drillkit import D, M
from masterykit import code, out


def n(x, d=2):
    """Format a number for prose: d decimals, trailing zeros trimmed."""
    s = ("%." + str(d) + "f") % x
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return "&minus;" + s[1:] if s.startswith("-") else s


# ---------------------------------------------------------------- q01 shapes
X1 = np.array([[2104., 5, 1, 45], [1416, 3, 2, 40], [852, 2, 1, 35]])
W1 = np.array([0.39133535, 18.75376741, -53.36032453, -26.42131618])
B1 = 785.1811367994083
F1 = X1[1] @ W1 + B1

# ---------------------------------------------------------------- q02 vectorization
W2 = np.array([1.5, -2.0, 0.5]); XV2 = np.array([4.0, 1.0, 6.0])
DOT2 = np.dot(W2, XV2)
try:
    np.dot(np.ones(4), np.ones((3, 4)))
    ERR2 = "no error"
except ValueError as e:
    ERR2 = str(e)

# ---------------------------------------------------------------- q03 scaling geometry
DW = 0.01
SIZE3, BED3 = 1500.0, 3.0
MOVE_SIZE, MOVE_BED = DW * SIZE3, DW * BED3
RATIO3 = MOVE_SIZE / MOVE_BED

# ---------------------------------------------------------------- q04 scaling arithmetic
V4 = np.array([300., 500, 800, 1200, 1700])
MU4, RNG4, SD4 = V4.mean(), V4.max() - V4.min(), V4.std()
X4 = 1200.0
MAX4, MEAN4, Z4 = X4 / V4.max(), (X4 - MU4) / RNG4, (X4 - MU4) / SD4
SPOT4_BAD, SPOT4_OK = (900 - 1000) / 1600, (900 - 1000) / 1200
INV4 = 1000 + (-1.5) * 250
FAR4 = (2400 - 1000) / 250

# ---------------------------------------------------------------- q05 feature engineering
F5 = np.array([10., 20, 30, 40, 15, 25]); D5 = np.array([30., 20, 40, 10, 50, 35])
Y5 = 0.5 * F5 * D5
A5 = np.column_stack([F5, D5, np.ones(6)])
C5 = np.linalg.lstsq(A5, Y5, rcond=None)[0]
RMS5_LIN = np.sqrt(np.mean((A5 @ C5 - Y5) ** 2))
A5b = np.column_stack([F5, D5, F5 * D5, np.ones(6)])
C5b = np.linalg.lstsq(A5b, Y5, rcond=None)[0]
RMS5_AREA = np.sqrt(np.mean((A5b @ C5b - Y5) ** 2))
# the trap: multiply AFTER scaling
FS5 = np.array([10., 20, 30, 40]); DS5 = np.array([20., 30, 40, 50])
ZF5 = (FS5 - FS5.mean()) / FS5.std(); ZD5 = (DS5 - DS5.mean()) / DS5.std()
ZP5 = ZF5 * ZD5
AR5 = FS5 * DS5

# ---------------------------------------------------------------- q06 polynomial
X6 = 10.0
F6 = 3 * X6 - 0.5 * X6 ** 2 + 0.02 * X6 ** 3 + 1
R6 = (1000.0, 1000.0 ** 2, 1000.0 ** 3)
X6b = 20.0
F6b = 3 * X6b - 0.5 * X6b ** 2 + 0.02 * X6b ** 3 + 1

# ---------------------------------------------------------------- q07 learning rate
def _steps(a, k=5):
    w, s = 1.0, []
    for _ in range(k):
        w = w - a * 2 * w
        s.append(w)
    return s


ST7 = {a: _steps(a) for a in (0.1, 0.9, 1.1)}
_rng = np.random.default_rng(0)
_xs = _rng.uniform(500, 2500, 40)
_ys = 0.12 * _xs + 50 + _rng.normal(0, 15, 40)
_z = (_xs - _xs.mean()) / _xs.std()
ALPHAS7 = (0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1.0, 3.0)
J7 = {}
for _a in ALPHAS7:
    _w = _b = 0.0
    with np.errstate(over="ignore", invalid="ignore"):
        for _ in range(100):
            _e = _w * _z + _b - _ys
            _w -= _a * np.mean(_e * _z)
            _b -= _a * np.mean(_e)
        J7[_a] = np.mean((_w * _z + _b - _ys) ** 2) / 2


def _j(v):
    if not np.isfinite(v) or v > 1e7:
        return "blows up (%s)" % ("inf" if not np.isfinite(v) else "%.1e" % v)
    return n(v, 2)


# ---------------------------------------------------------------- q08 scaling at serve time
TR8 = np.array([1100., 1300, 1500, 1700, 1900])
MU8, SD8 = TR8.mean(), TR8.std()
W8, B8 = 120.0, 340.0
NEW8 = 1900.0
Z8 = (NEW8 - MU8) / SD8
P8 = W8 * Z8 + B8
RAW8 = W8 * NEW8 + B8
BATCH8 = np.array([1900., 2000, 2100])
Z8b = (NEW8 - BATCH8.mean()) / BATCH8.std()
P8b = W8 * Z8b + B8

# ---------------------------------------------------------------- q09 vectorized gradient
X9 = np.array([[1., 2], [3, 1], [2, 2]]); Y9 = np.array([5., 6, 7])
W9 = np.array([1., 1]); B9 = 0.0
F9 = X9 @ W9 + B9
E9 = F9 - Y9
G9 = X9.T @ E9 / 3
GB9 = E9.mean()
XS9 = np.array([[1., 2], [3, 4]]); ES9 = np.array([1., -1])
RIGHT9, WRONG9 = XS9.T @ ES9 / 2, XS9 @ ES9 / 2

# ---------------------------------------------------------------- q10 normal equation
X10 = np.array([1., 2, 3]); Y10 = np.array([2., 4, 5])
A10 = np.column_stack([X10, np.ones(3)])
W10, B10 = np.linalg.solve(A10.T @ A10, A10.T @ Y10)
SD10 = X10.std()
Z10 = (X10 - X10.mean()) / SD10
_w = _b = 0.0
for _ in range(2000):
    _e = _w * Z10 + _b - Y10
    _w -= 0.1 * np.mean(_e * Z10)
    _b -= 0.1 * np.mean(_e)
WS10, BS10 = _w, _b


def _row(vals, d=3):
    return "[" + ", ".join(n(v, d) for v in vals) + "]"


DRILLS = [

# =================================================================== q01
D("c1w2-q01",
  recall=M("Four pieces of notation, from a blank page.",
    """<p>Without looking, write down what each of these means, in words:</p>
<ol><li><var>x</var><sup>(i)</sup></li><li><var>x</var><sub>j</sub></li>
<li><var>x</var><sub>j</sub><sup>(i)</sup></li><li><var>m</var> and <var>n</var></li></ol>
<p>Then: with <var>m</var> examples and <var>n</var> features, what shape is <code>X</code>, and
what shape is <var>w</var>?</p>""",
    """<ol><li><var>x</var><sup>(i)</sup> &mdash; the <b>whole i-th example</b>, a row of n numbers.</li>
<li><var>x</var><sub>j</sub> &mdash; the <b>j-th feature</b>, one column.</li>
<li><var>x</var><sub>j</sub><sup>(i)</sup> &mdash; <b>one cell</b>: feature j of example i.</li>
<li><var>m</var> counts examples (rows); <var>n</var> counts features (columns).</li></ol>
<p><code>X</code> is <b>m&times;n</b>. <var>w</var> has <b>n</b> numbers &mdash; one per feature,
never one per example. <var>b</var> is one number on its own.</p>""",
    "Superscript in brackets picks the row (which house); subscript picks the column (which measurement).",
    "Think of a class list. Each line is one kid; each column is something about them, like height or age. "
    "&ldquo;Kid number 3&rdquo; is a whole line. &ldquo;Age&rdquo; is a whole column. &ldquo;Kid 3's "
    "age&rdquo; is one box.",
    [("example", "one row &mdash; one house, one patient, one thing you measured"),
     ("feature", "one column &mdash; one kind of measurement, like size"),
     ("superscript (i)", "the little number up top, in brackets: which row"),
     ("subscript j", "the little number down low: which column"),
     ("shape m&times;n", "how many rows by how many columns")]),

  work=M("Read three cells off a real table and make one prediction.",
    """<p>Three houses (size in sq&nbsp;ft, bedrooms, floors, age in years):</p>
<table><thead><tr><th></th><th>size</th><th>bedrooms</th><th>floors</th><th>age</th></tr></thead><tbody>
<tr><td>house 1</td><td>2104</td><td>5</td><td>1</td><td>45</td></tr>
<tr><td>house 2</td><td>1416</td><td>3</td><td>2</td><td>40</td></tr>
<tr><td>house 3</td><td>852</td><td>2</td><td>1</td><td>35</td></tr></tbody></table>
<ol><li>What are <var>m</var>, <var>n</var> and the shape of <code>X</code>?</li>
<li>Write out <var>x</var><sup>(2)</sup>, and give <var>x</var><sub>3</sub><sup>(1)</sup> and
<var>x</var><sub>1</sub><sup>(3)</sup>.</li>
<li>With <var>w</var> = [%s] and <var>b</var> = %s, compute
<var>f</var>(<var>x</var><sup>(2)</sup>) = <var>w</var>&middot;<var>x</var><sup>(2)</sup> + <var>b</var>.
Price is in $1000s.</li></ol>""" % (", ".join(n(v, 2) for v in W1), n(B1, 2)),
    """<ol><li>m = 3, n = 4, <code>X</code> is <b>3&times;4</b>.</li>
<li><var>x</var><sup>(2)</sup> = [1416, 3, 2, 40]. <var>x</var><sub>3</sub><sup>(1)</sup> = 1
(floors of house 1). <var>x</var><sub>1</sub><sup>(3)</sup> = 852 (size of house 3).</li>
<li>Multiply pairwise and add: 1416&times;%s + 3&times;%s + 2&times;(%s) + 40&times;(%s) + %s
&asymp; <b>%s</b>, so about $%sk.</li></ol>
<p>Notice the <b>NumPy indices are one less</b>: <var>x</var><sub>3</sub><sup>(1)</sup> is
<code>X[0, 2]</code>.</p>""" % (n(W1[0], 2), n(W1[1], 2), n(W1[2], 2), n(W1[3], 2), n(B1, 2),
                                n(F1, 1), n(F1, 0)),
    "A prediction is one row multiplied against the weights, then plus b.",
    "Each fact about the house gets a score. You multiply each fact by how much it matters and add "
    "it all up, then add a starting amount. That total is your guess for the price.",
    [("w&middot;x (dot product)", "multiply matching pairs, then add them all up"),
     ("weight w<sub>j</sub>", "how much one feature pushes the price up or down"),
     ("bias b", "the starting amount before any feature is counted"),
     ("$1000s", "the price column is in thousands, so 232 means $232,000")]),

  spot=M("A classmate's notes on the same table. Two lines are wrong.",
    """<p>Using the three-house table above, a classmate wrote:</p>
<ol><li>&ldquo;<var>x</var><sup>(1)</sup> = 2104, the size of the first house.&rdquo;</li>
<li>&ldquo;<code>X.shape</code> is (4, 3) because there are 4 features.&rdquo;</li>
<li>&ldquo;<var>w</var> has 4 numbers.&rdquo;</li>
<li>&ldquo;<var>x</var><sub>2</sub><sup>(3)</sup> = 2.&rdquo;</li></ol>
<p>Which two are wrong, and what should they say?</p>""",
    """<p><b>Line 1 is wrong.</b> <var>x</var><sup>(1)</sup> is the whole row [2104, 5, 1, 45]. The size
of the first house is <var>x</var><sub>1</sub><sup>(1)</sup> = 2104 &mdash; it needs both indices.</p>
<p><b>Line 2 is wrong.</b> Rows are examples, so <code>X.shape</code> is <b>(3, 4)</b>. Swapping these is
the most common shape bug in the course.</p>
<p>Lines 3 and 4 are right: one weight per feature, and house 3 has 2 bedrooms.</p>""",
    "Naming one cell needs both a row number and a column number.",
    "If I say &ldquo;kid 1&rdquo;, I mean the whole kid, not just their height. To point to their "
    "height, I need to say both: kid 1 <i>and</i> height.",
    [("row vs column", "rows go across and are examples; columns go down and are features"),
     ("X.shape", "NumPy's way to ask &ldquo;how many rows, how many columns?&rdquo;"),
     ("(3, 4)", "3 rows, 4 columns &mdash; always rows first")]),

  transfer=M("A hospital dataset the lesson never mentioned.",
    """<p>A hospital records <b>12 measurements</b> for each of <b>500 patients</b> and wants to predict
length of stay with multiple linear regression.</p>
<ol><li>Shape of <code>X</code>? Length of <var>w</var>? How many numbers does the model learn in total?</li>
<li>In words, what is <var>x</var><sub>7</sub><sup>(42)</sup>, and what is it in NumPy?</li>
<li>They add a 13th measurement. Which of these change: m, n, the shape of <var>w</var>, the
number of rows?</li></ol>""",
    """<ol><li><code>X</code> is <b>500&times;12</b>; <var>w</var> has <b>12</b>; the model learns
<b>13</b> numbers (12 weights + b). The 500 patients are data, not parameters.</li>
<li>Measurement 7 of patient 42 &mdash; <code>X[41, 6]</code>.</li>
<li><b>n</b> goes to 13 and <var>w</var> grows to 13. m and the number of rows do not change.</li></ol>""",
    "More patients means more rows; more measurements means more weights.",
    "Getting more kids in the class makes the list longer, but you still only need one score per "
    "question. Adding a new question gives you one new score to learn.",
    [("parameter", "a number the model learns, like a weight or b"),
     ("data", "the numbers you were given, which the model does not change"),
     ("index 41", "NumPy counts from 0, so patient 42 lives at 41")]),
),

# =================================================================== q02
D("c1w2-q02",
  recall=M("Why the loop is slow, in four bullet points.",
    """<p>From memory, list <b>why</b> <code>np.dot(w, x)</code> beats a Python <code>for</code> loop
computing the same sum. Then list two things that are <b>not</b> the reason.</p>""",
    """<p><b>Why:</b></p><ul>
<li>The arithmetic is handed to compiled code that uses <b>SIMD</b> hardware &mdash; one instruction
on several numbers at once.</li>
<li>The loop pays the Python interpreter's overhead on <b>every single element</b>.</li></ul>
<p><b>Not why:</b> it does not use a cleverer formula (same multiplications, same additions), and it
does not approximate or skip anything.</p>""",
    "Same maths, faster road to the hardware.",
    "Imagine adding up a pile of coins. The loop hands you one coin, waits for you to say "
    "&ldquo;ok&rdquo;, then hands the next. Vectorizing tips the whole pile onto a machine that counts "
    "ten coins at a time.",
    [("vectorize", "do the whole list in one command instead of one item at a time"),
     ("SIMD", "Single Instruction, Multiple Data &mdash; the chip works on several numbers at once"),
     ("interpreter overhead", "the extra checking Python does every time a loop goes round")]),

  work=M("Do the dot product by hand, then count the work.",
    """<p><var>w</var> = [1.5, &minus;2, 0.5], <var>x</var> = [4, 1, 6].</p>
<ol><li>Compute <code>np.dot(w, x)</code> by hand.</li>
<li>For vectors of length n = 1,000,000, how many multiplications and how many additions does the
loop do? How many does <code>np.dot</code> do?</li></ol>""",
    """<ol><li>1.5&times;4 + (&minus;2)&times;1 + 0.5&times;6 = 6 &minus; 2 + 3 = <b>%s</b>.</li>
<li>Both: <b>1,000,000 multiplications and 999,999 additions</b>. The count is identical &mdash; the
speed-up is entirely in how they reach the processor.</li></ol>""" % n(DOT2, 2),
    "Vectorizing changes the speed, not the amount of arithmetic.",
    "Ten sums done one at a time or ten sums done together are still ten sums. Doing them together is "
    "just quicker.",
    [("dot product", "multiply pairs, then add"),
     ("n", "how many numbers are in each list")]),

  spot=M("Vectorized across houses, and it crashes.",
    """<p>Someone wants predictions for every house at once. <code>X</code> is (3, 4), <code>w</code> is (4,):</p>
%s
<p>What error do they get, and what is the fix?</p>""" % code("f = np.dot(w, X) + b"),
    """<p>NumPy refuses:</p>%s
<p>The inner sizes must match: (4,) against (3, <b>4</b>) lines up the 4 with the 3. Put the matrix
first: <code>np.dot(X, w) + b</code> &mdash; (3, <b>4</b>) by (<b>4</b>,) gives (3,), one prediction per
house. <code>X @ w + b</code> is the same thing.</p>""" % out(ERR2),
    "In a matrix-times-vector, the vector's length must match the matrix's columns.",
    "It is like plugging a plug into a socket. The four prongs have to meet four holes. Put it in "
    "the wrong way round and it simply will not go in.",
    [("shapes not aligned", "the two sizes that must be equal are not"),
     ("@", "NumPy's matrix-multiply sign, the same as np.dot here"),
     ("(3,)", "a flat list of 3 numbers &mdash; one prediction per house")]),

  transfer=M("Where vectorizing helps most, and where it hardly helps.",
    """<ol><li>A GPU has thousands of small cores. Why does the same rewrite (loop &rarr; one array
operation) pay off even more there?</li>
<li>Name a case where vectorizing gives almost no speed-up, and say why.</li></ol>""",
    """<ol><li>One array operation hands the GPU thousands of independent multiplications to spread across
its cores at once. A Python loop feeds them one by one, so the cores sit idle.</li>
<li>Tiny arrays &mdash; say three numbers. There is a fixed cost to calling into NumPy at all, and with
three elements that fixed cost is most of the time. The gain grows with n.</li></ol>""",
    "The bigger the array, the more vectorizing pays.",
    "A bus is great for carrying 50 people but not much faster than walking if only one person is going.",
    [("GPU", "a chip with thousands of simple workers, built for doing lots of sums at once"),
     ("fixed cost", "time you spend just getting started, however small the job")]),
),

# =================================================================== q03
D("c1w2-q03",
  recall=M("Draw the two contour plots from memory.",
    """<p>On paper, sketch the contours of <var>J</var>(<var>w</var><sub>1</sub>, <var>w</var><sub>2</sub>)
for size (0&ndash;2000) and bedrooms (1&ndash;5), <b>unscaled</b> and then <b>scaled</b>. Draw the path
gradient descent takes on each. Then write one sentence each for: what scaling changes, and what
it does not change.</p>""",
    """<p><b>Unscaled:</b> tall, thin ellipses &mdash; <b>narrow along <var>w</var><sub>1</sub></b> (the
size weight), because a tiny change in <var>w</var><sub>1</sub> moves J a lot, and long along
<var>w</var><sub>2</sub>. The
path zig-zags across the narrow valley.</p>
<p><b>Scaled:</b> near-circles; the path heads almost straight for the centre.</p>
<p><b>Changes:</b> how many steps it takes. <b>Does not change:</b> where the minimum is, in terms of
the predictions the model makes.</p>""",
    "Scaling reshapes the valley so gradient descent can walk straight down it.",
    "Picture rolling a marble into a long, skinny ditch. It bangs side to side for ages. In a round "
    "bowl it rolls straight to the bottom.",
    [("contour plot", "a map of the cost, where each ring joins points with the same cost"),
     ("feature range", "the smallest to the biggest value a feature takes"),
     ("converge", "settle at the bottom and stop moving")]),

  work=M("Nudge each weight by 0.01 and see what moves.",
    """<p>A house has size = %s and bedrooms = %s (unscaled). Increase <var>w</var><sub>1</sub>
(the size weight) by %s. How much does the prediction change? Now increase <var>w</var><sub>2</sub>
(bedrooms) by %s instead. Compare the two.</p>""" % (n(SIZE3, 0), n(BED3, 0), DW, DW),
    """<p>Size: %s &times; %s = <b>%s</b>. Bedrooms: %s &times; %s = <b>%s</b>.</p>
<p>The same nudge moves the prediction <b>%s times</b> more through size. That ratio is exactly how
stretched the contours are &mdash; and why one learning rate cannot suit both weights until the
features are on similar scales.</p>""" % (DW, n(SIZE3, 0), n(MOVE_SIZE, 2), DW, n(BED3, 0),
                                       n(MOVE_BED, 2), n(RATIO3, 0)),
    "A feature with big numbers makes its weight extra sensitive.",
    "If one knob is a tiny turn for a huge change and the other needs a big turn for a tiny change, "
    "it is hard to turn them both the right amount at the same time.",
    [("sensitivity", "how much the output moves when you nudge an input"),
     ("learning rate &alpha;", "how big a step gradient descent takes each time")]),

  spot=M("A wrong conclusion from a correct experiment.",
    """<p>&ldquo;Unscaled, my model needed 50,000 iterations to reach its lowest cost. Scaled, it needed
300. So the scaled model is the more <b>accurate</b> one and I should always report it.&rdquo;</p>
<p>The numbers are fine. Where is the reasoning wrong?</p>""",
    """<p><b>&ldquo;More accurate&rdquo;</b> is the error. Both runs head for the same minimum &mdash;
the same best fit, expressed in different units. Scaling bought <b>speed</b>, not accuracy. If both
were run to convergence, their predictions would match.</p>""",
    "Scaling makes training faster; it does not make the answer better.",
    "Taking the short path to the shop does not get you a better shop. Same shop, you just get there sooner.",
    [("accuracy", "how close the predictions are to the truth"),
     ("convergence speed", "how many steps it takes to get to the bottom")]),

  transfer=M("Three new features, one decision each.",
    """<p>A loan model has <b>age</b> (18&ndash;90), <b>income</b> ($20,000&ndash;$250,000) and
<b>has_mortgage</b> (0 or 1).</p>
<ol><li>Which features would you scale, and why?</li>
<li>If you solved it with the normal equation instead of gradient descent, would you still need to?</li></ol>""",
    """<ol><li>Certainly <b>income</b> &mdash; its range is thousands of times the others. Scaling age too is
sensible so all three sit near &minus;1&hellip;1. A 0/1 flag is already small; scaling it is
harmless but rarely needed.</li>
<li><b>No.</b> The normal equation solves in one step; there is no path, so the shape of the valley
does not matter. Scaling is for iterative methods.</li></ol>""",
    "Scale anything whose range dwarfs the others, when you train by taking steps.",
    "If one friend measures in centimetres and another in kilometres, you convert them to the same "
    "kind of size before comparing.",
    [("binary flag", "a feature that is only ever 0 or 1"),
     ("normal equation", "a formula that jumps straight to the answer without steps"),
     ("iterative", "getting there by many small steps")]),
),

# =================================================================== q04
D("c1w2-q04",
  recall=M("Three scaling formulas, and the range each gives.",
    """<p>Write the formula for <b>max scaling</b>, <b>mean normalization</b> and <b>z-score
normalization</b>, and the rough range of values each produces.</p>""",
    """<ul><li>Max scaling: <var>x</var> / max &rarr; about 0&hellip;1 (if values are positive).</li>
<li>Mean normalization: (<var>x</var> &minus; &mu;) / (max &minus; min) &rarr; about &minus;1&hellip;1,
centred on 0.</li>
<li>Z-score: (<var>x</var> &minus; &mu;) / &sigma; &rarr; mostly &minus;3&hellip;3, centred on 0 with
spread 1.</li></ul>""",
    "Subtract the middle, then divide by how spread out it is.",
    "It is like saying &ldquo;how far above or below average are you?&rdquo; and then measuring that in "
    "&ldquo;normal-sized steps&rdquo; instead of raw centimetres.",
    [("&mu; (mu)", "the mean &mdash; the average value"),
     ("&sigma; (sigma)", "the standard deviation &mdash; how far values typically sit from the average"),
     ("range", "max minus min"),
     ("normalize", "put on a standard scale")]),

  work=M("Scale one value three ways.",
    """<p>A feature takes the values [300, 500, 800, 1200, 1700].</p>
<ol><li>Compute &mu;, the range and &sigma; (population &sigma;, dividing by m).</li>
<li>Scale <var>x</var> = %s with all three methods.</li></ol>""" % n(X4, 0),
    """<ol><li>&mu; = %s, range = 1700 &minus; 300 = %s, &sigma; &asymp; %s.</li>
<li>Max: %s / 1700 &asymp; <b>%s</b>. Mean norm: (%s &minus; %s) / %s &asymp; <b>%s</b>.
Z-score: (%s &minus; %s) / %s &asymp; <b>%s</b>.</li></ol>
<p>Three different numbers for the same house &mdash; which is fine, as long as you use the <b>same</b>
method and the <b>same</b> statistics at prediction time.</p>""" % (
        n(MU4, 0), n(RNG4, 0), n(SD4, 1), n(X4, 0), n(MAX4, 3), n(X4, 0), n(MU4, 0), n(RNG4, 0),
        n(MEAN4, 3), n(X4, 0), n(MU4, 0), n(SD4, 1), n(Z4, 3)),
    "Each method gives a different number; what matters is using one consistently.",
    "Saying a temperature in Celsius or Fahrenheit gives different numbers for the same day. Either "
    "is fine as long as you do not mix them.",
    [("population &sigma;", "spread computed by dividing by m (NumPy's default std)"),
     ("scaled value", "the new number after the formula")]),

  spot=M("A worked mean-normalization with one slip.",
    """<p>A feature has mean 1000, min 400, max 1600. The working for <var>x</var> = 900:</p>
<p>(900 &minus; 1000) / 1600 = &minus;100 / 1600 = %s</p>
<p>Find the mistake and give the right value.</p>""" % n(SPOT4_BAD, 4),
    """<p>It divides by the <b>max</b> (1600) instead of the <b>range</b> (1600 &minus; 400 = 1200).
Correct: &minus;100 / 1200 &asymp; <b>%s</b>.</p>
<p>This is exactly the kind of near-miss a quiz distractor is built from.</p>""" % n(SPOT4_OK, 4),
    "Mean normalization divides by max minus min, not by max.",
    "If a ruler goes from 400 to 1600, it is 1200 long, not 1600. You measured from the wrong end.",
    [("range", "max minus min &mdash; how wide the spread is"),
     ("distractor", "a wrong answer in a quiz built to look right")]),

  transfer=M("Going backwards, and a value far outside.",
    """<p>A feature was z-scored with &mu; = 1000, &sigma; = 250.</p>
<ol><li>A scaled value is &minus;1.5. What was the raw value?</li>
<li>A new house arrives with raw value 2400. What is its z-score, and what should that make you
think?</li></ol>""",
    """<ol><li>Undo it: <var>x</var> = &mu; + <var>z</var>&sigma; = 1000 + (&minus;1.5)(250) =
<b>%s</b>.</li>
<li><var>z</var> = (2400 &minus; 1000) / 250 = <b>%s</b>. Almost six standard deviations out &mdash;
far outside anything the model trained on. The prediction is an <b>extrapolation</b>; trust it less.</li></ol>""" % (
        n(INV4, 0), n(FAR4, 1)),
    "A z-score tells you how unusual a value is, in standard-sized steps.",
    "If most kids in your class are between 1.3 and 1.5 metres and a new kid is 2.4 metres, your "
    "guesses about that kid are probably not very good.",
    [("z-score", "how many standard steps away from average"),
     ("extrapolation", "guessing outside the range you have seen")]),
),

# =================================================================== q05
D("c1w2-q05",
  recall=M("What feature engineering is, and why a model can't do it alone.",
    """<p>From memory: define feature engineering in one sentence. Say why a linear model cannot learn
<var>frontage</var> &times; <var>depth</var> on its own. Give two other engineered features from
any domain.</p>""",
    """<p>Feature engineering is <b>making new input columns</b> from the ones you have, using what you
know about the problem.</p>
<p>A linear model can only <b>add up scaled copies</b> of its inputs. No choice of weights turns
<var>w</var><sub>1</sub>&middot;frontage + <var>w</var><sub>2</sub>&middot;depth into a product.</p>
<p>Examples: price &divide; area (price per sq&nbsp;ft); log(income); day of week from a timestamp;
distance from two coordinates.</p>""",
    "You hand the model a column it could never build for itself.",
    "If you can only add, you can never make 5 &times; 6 out of a 5 and a 6. Someone has to give you "
    "the 30.",
    [("engineered feature", "a new column you built from other columns"),
     ("linear model", "a model that just multiplies each input by a number and adds them up"),
     ("representable", "something the model is able to express at all")]),

  work=M("Fit with and without the area column, and compare the error.",
    """<p>Six plots: frontage = [%s], depth = [%s], price = 0.5 &times; frontage &times; depth exactly.</p>
<p>Without computing, predict: can the best linear fit on <i>frontage</i> and <i>depth</i> get the
error to zero? Then check against the result of an actual least-squares fit (shown in the answer).
What happens when an <i>area</i> column is added?</p>""" % (
        ", ".join(n(v, 0) for v in F5), ", ".join(n(v, 0) for v in D5)),
    """<p>Frontage and depth only: best weights &asymp; %s, %s, intercept %s, and the
root-mean-square error is <b>%s</b> &mdash; it cannot get to zero.</p>
<p>Add area: the weight on area comes out at <b>%s</b> and the error drops to <b>%s</b> (zero, up to
rounding). The data were made from area, and now the model can see it.</p>""" % (
        n(C5[0], 2), n(C5[1], 2), n(C5[2], 1), n(RMS5_LIN, 2), n(C5b[2], 3), "%.0e" % RMS5_AREA),
    "The right engineered feature can turn an impossible fit into a perfect one.",
    "It is like trying to guess how much paint a wall needs from its width only, or its height only. "
    "Once you have width &times; height, you nail it.",
    [("least squares", "the fit that makes the total squared error as small as possible"),
     ("RMS error", "a typical size of the mistakes, in the same units as price"),
     ("intercept", "another word for b")]),

  spot=M("Area built from scaled columns. Something odd happens.",
    """<p>Someone scaled frontage [10, 20, 30, 40] and depth [20, 30, 40, 50] with z-scores
<b>first</b>, and then multiplied the scaled columns to make &ldquo;area&rdquo;. Their area column:</p>
<p>[%s]</p>
<p>The real areas are [%s]. What has gone wrong?</p>""" % (_row(ZP5, 2), _row(AR5, 0)),
    """<p>The smallest plot (200) and the largest plot (2000) both get <b>%s</b>. Two negatives
multiply to a positive, so &ldquo;small and small&rdquo; looks just like &ldquo;big and big&rdquo;.</p>
<p>Fix: <b>multiply the raw columns first, then scale the product</b>. Engineering comes before
scaling.</p>""" % n(ZP5[0], 2),
    "Build new features from raw values, then scale.",
    "Minus times minus is plus. So a tiny garden and a giant garden end up with the same number, "
    "which is silly.",
    [("z-scored", "turned into &ldquo;steps above or below average&rdquo;, so small things go negative"),
     ("order of operations", "which step you do first changes the answer")]),

  transfer=M("Taxi trips: invent the feature.",
    """<p>You predict taxi trip duration with a linear model. You have pickup and drop-off latitude and
longitude, and the pickup timestamp. Which two engineered features would you add, and why can't the
model build them itself?</p>""",
    """<p><b>Distance</b> between pickup and drop-off: it needs subtraction <i>and</i> squaring and a
square root of the coordinates &mdash; not a weighted sum of them.</p>
<p><b>Hour of day</b> (or rush-hour flag) from the timestamp: the raw timestamp is one ever-growing
number, and traffic depends on the time of day, which repeats.</p>""",
    "Ask what quantity actually drives the outcome, then hand it over as a column.",
    "A taxi takes longer when the trip is far and when the roads are busy. So tell the model "
    "&ldquo;how far&rdquo; and &ldquo;what time&rdquo;, not just a list of map numbers.",
    [("coordinates", "latitude and longitude &mdash; a place's position on the map"),
     ("timestamp", "the exact date and time something happened")]),
),

# =================================================================== q06
D("c1w2-q06",
  recall=M("Why a curve can still be linear regression.",
    """<p>From memory: what does &ldquo;linear&rdquo; refer to in polynomial regression? Write the
model for a cubic in one feature. Say why scaling becomes urgent.</p>""",
    """<p>&ldquo;Linear&rdquo; means <b>linear in the parameters</b> &mdash; each <var>w</var> just
multiplies a known number.</p>
<p><var>f</var> = <var>w</var><sub>1</sub><var>x</var> + <var>w</var><sub>2</sub><var>x</var>&sup2; +
<var>w</var><sub>3</sub><var>x</var>&sup3; + <var>b</var>.</p>
<p>The columns <var>x</var>, <var>x</var>&sup2;, <var>x</var>&sup3; have wildly different ranges, so
without scaling gradient descent crawls.</p>""",
    "The curve is in the features; the learning is still a weighted sum.",
    "You are still just adding up scores. Some of the scores happen to be &ldquo;the number "
    "squared&rdquo; or &ldquo;the number cubed&rdquo;.",
    [("polynomial", "a sum of powers like x, x&sup2;, x&sup3;"),
     ("linear in the parameters", "each weight only multiplies something, never gets squared itself"),
     ("cubic", "goes up to x&sup3;")]),

  work=M("Evaluate a cubic and size its columns.",
    """<p><var>f</var>(<var>x</var>) = 3<var>x</var> &minus; 0.5<var>x</var>&sup2; +
0.02<var>x</var>&sup3; + 1.</p>
<ol><li>Compute <var>f</var>(10) and <var>f</var>(20).</li>
<li>If <var>x</var> runs from 1 to 1000, what is the largest value of each column
<var>x</var>, <var>x</var>&sup2;, <var>x</var>&sup3;?</li></ol>""",
    """<ol><li><var>f</var>(10) = 30 &minus; 50 + 20 + 1 = <b>%s</b>. <var>f</var>(20) = 60 &minus; 200 +
160 + 1 = <b>%s</b>.</li>
<li>%s, %s and %s. The third column is a <b>million times</b> bigger than the first &mdash; which is why
scaling is not optional here.</li></ol>""" % (n(F6, 2), n(F6b, 2), "{:,.0f}".format(R6[0]),
                                              "{:,.0f}".format(R6[1]), "{:,.0f}".format(R6[2])),
    "Powers make the columns' ranges explode.",
    "Ten is small. Ten times ten times ten is a thousand. A thousand cubed is a billion. The "
    "numbers get huge really fast.",
    [("x&sup2; / x&sup3;", "x times itself, and x times itself times itself"),
     ("column range", "smallest to biggest value in that column")]),

  spot=M("&ldquo;Lower training cost, so it is the better model.&rdquo;",
    """<p>&ldquo;My straight-line fit has training cost 4.1. My cubic has training cost 0.2. So the cubic is
clearly the better model.&rdquo;</p>
<p>What is wrong with that argument?</p>""",
    """<p>A cubic <b>contains</b> the straight line (set <var>w</var><sub>2</sub> = <var>w</var><sub>3</sub> =
0), so its best training cost can never be worse. A lower training cost is guaranteed and proves
nothing about <b>new</b> data. You need a held-out set to compare them &mdash; that is week 3's
overfitting, and C2 W3's whole topic.</p>""",
    "Training cost always drops when you add features; judge models on data they have not seen.",
    "If you are allowed to draw a wiggly line, you can always pass closer to the dots. That does "
    "not mean you will guess the next dot better.",
    [("training cost", "the error on the data the model learned from"),
     ("held-out data", "data kept aside to test on"),
     ("overfitting", "fitting the training data so closely it does badly on new data")]),

  transfer=M("Diminishing returns, and what happens past the data.",
    """<ol><li>Price rises with size, but each extra square foot adds less. Which single engineered
feature captures that? Is the model still linear regression?</li>
<li>Your cubic fits sizes 500&ndash;3000 well. What do you expect at size 6000, and why?</li></ol>""",
    """<ol><li><b>&radic;size</b> (or log size): it grows, but more slowly. Still linear regression
&mdash; one weight times a known column.</li>
<li>The <var>x</var>&sup3; term dominates outside the data and drags the curve sharply up or down.
Polynomials <b>extrapolate badly</b>; the fit says nothing reliable beyond 3000.</li></ol>""",
    "Pick features whose shape matches the story, and do not trust them outside the data.",
    "The first slice of cake makes you very happy; the tenth, a little. A square root grows like "
    "that. And guessing far outside what you have seen is like guessing the weather next year.",
    [("diminishing returns", "each extra bit helps less than the one before"),
     ("&radic; (square root)", "the number that, times itself, gives this one"),
     ("extrapolate", "guess outside the range you have data for")]),
),

# =================================================================== q07
D("c1w2-q07",
  recall=M("Four learning curves, drawn from memory.",
    """<p>Sketch J against iteration for: &alpha; too small, &alpha; about right, &alpha; too large, and
a <b>bug</b>. Then write the ladder of &alpha; values the course suggests trying.</p>""",
    """<ul><li>Too small: falls slowly, still falling at the end.</li>
<li>About right: falls fast, then flattens.</li>
<li>Too large: zig-zags or climbs.</li>
<li>Bug: rises even with a tiny &alpha; (often a sign error in the update).</li></ul>
<p>Ladder: &hellip; 0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1 &hellip; &mdash; roughly &times;3 each time.</p>""",
    "Read the shape of the cost curve to choose the step size.",
    "If your steps are tiny you take forever to get downhill. If they are giant you jump over the "
    "bottom and land on the other side, higher up.",
    [("learning curve", "a graph of cost going down as training goes on"),
     ("iteration", "one step of gradient descent"),
     ("diverge", "the cost gets bigger and bigger instead of settling")]),

  work=M("Five steps on J = w&sup2; with three learning rates.",
    """<p>J(<var>w</var>) = <var>w</var>&sup2;, so the gradient is 2<var>w</var>. Start at
<var>w</var> = 1. The update is <var>w</var> &larr; <var>w</var> &minus; &alpha;&middot;2<var>w</var>.
Do five steps each for &alpha; = 0.1, 0.9 and 1.1.</p>""",
    """<ul><li>&alpha; = 0.1: %s &mdash; shrinks smoothly.</li>
<li>&alpha; = 0.9: %s &mdash; flips sign every step but still shrinks: it oscillates and converges.</li>
<li>&alpha; = 1.1: %s &mdash; flips <b>and grows</b>: divergence.</li></ul>
<p>Each step multiplies <var>w</var> by (1 &minus; 2&alpha;): 0.8, &minus;0.8, &minus;1.2. Bigger than
1 in size means it blows up.</p>""" % (_row(ST7[0.1], 4), _row(ST7[0.9], 4), _row(ST7[1.1], 4)),
    "A step that overshoots by more than it corrects makes things worse every time.",
    "Jumping across a stream: a small jump gets you closer; a jump that lands you further away on "
    "the other side each time means you never get across.",
    [("gradient", "the slope &mdash; which way is uphill and how steep"),
     ("oscillate", "swing back and forth"),
     ("&larr;", "&ldquo;becomes&rdquo; &mdash; replace the old value with the new one")]),

  spot=M("Cost rises, so they keep shrinking &alpha;.",
    """<p>&ldquo;My cost goes <b>up</b> every iteration. I tried &alpha; = 0.01, then 0.0001, then
0.000001. It still goes up every time, just more slowly. I'll try 1e-9 next.&rdquo;</p>
<p>What should they conclude instead?</p>""",
    """<p>With a small enough &alpha;, correct gradient descent <b>must</b> lower J each step. A cost that
rises at <i>every</i> &alpha; is not a learning-rate problem &mdash; it is a <b>bug</b>. The usual one
is a sign: <code>w = w + alpha * dj_dw</code> walks uphill. It should be <code>w - alpha * dj_dw</code>.</p>""",
    "If even a tiny step makes things worse, you are walking the wrong way.",
    "If every step you take, however tiny, takes you further from home, the problem is not your "
    "step size. You are facing the wrong way.",
    [("sign error", "a plus where there should be a minus"),
     ("dj_dw", "the code name for the slope of the cost with respect to w")]),

  transfer=M("A real sweep: choose &alpha; from the table.",
    """<p>A one-feature model (scaled) was trained for 100 iterations at each &alpha;. Final cost:</p>
<table><thead><tr><th>&alpha;</th><th>J after 100 iterations</th></tr></thead><tbody>%s</tbody></table>
<p>Which &alpha; would you pick? Why not the smallest &alpha;, and why not simply the largest one that
did not blow up?</p>""" % "".join("<tr><td>%s</td><td>%s</td></tr>" % (a, _j(J7[a])) for a in ALPHAS7),
    """<p>From 0.1 to 1 the cost reaches the same floor (%s): those have converged. 0.03 and below are
still falling. 3 blows up.</p>
<p>A sensible pick is <b>0.3</b>: it converges with room to spare below the value that diverges. 1
also works here but sits closer to the edge, and a tiny &alpha; wastes iterations without buying
anything.</p>""" % _j(J7[0.1]),
    "Choose a step size that converges, a safe distance below the one that blows up.",
    "Walk as fast as you can without tripping, and then a little slower, just to be safe.",
    [("sweep", "trying many values to see which works"),
     ("floor", "the lowest cost the model can reach")]),
),

# =================================================================== q08
D("c1w2-q08",
  recall=M("The three rules of scaling at prediction time.",
    """<p>From memory, write the three rules for scaling a new input at prediction time, and say what
must be saved from training.</p>""",
    """<ol><li><b>Save</b> &mu; and &sigma; (or min/max) computed on the <b>training</b> set.</li>
<li>Apply the <b>same</b> transformation to every new input, feature by feature.</li>
<li><b>Never</b> recompute the statistics from new data.</li></ol>""",
    "The model learned in scaled units, so every input must arrive in those same units.",
    "If you learned to bake using cups, someone giving you the recipe in spoons will ruin the cake. "
    "Always convert using the same cup you learned with.",
    [("training statistics", "the mean and spread worked out from the training data"),
     ("serving / prediction time", "when the finished model is used on new examples")]),

  work=M("One new house, three ways to scale it.",
    """<p>Training sizes were [%s] (so &mu; = %s, &sigma; &asymp; %s). The model learned
<var>w</var> = %s per &sigma; and <var>b</var> = %s (price in $1000s). A new house has size %s.</p>
<ol><li>Predict correctly.</li><li>Predict if you forgot to scale at all.</li>
<li>Predict if you scaled using a batch of three new houses [1900, 2000, 2100].</li></ol>""" % (
        ", ".join(n(v, 0) for v in TR8), n(MU8, 0), n(SD8, 1), n(W8, 0), n(B8, 0), n(NEW8, 0)),
    """<ol><li><var>z</var> = (%s &minus; %s) / %s &asymp; %s, so <var>f</var> &asymp; %s &times; %s + %s =
<b>%s</b>.</li>
<li>%s &times; %s + %s = <b>%s</b> &mdash; obviously absurd, so at least you would notice.</li>
<li>Batch &mu; = 2000, &sigma; &asymp; %s, so <var>z</var> &asymp; %s and <var>f</var> &asymp;
<b>%s</b>. Plausible-looking and <b>wrong</b> &mdash; the dangerous one, because nothing warns you.</li></ol>""" % (
        n(NEW8, 0), n(MU8, 0), n(SD8, 1), n(Z8, 3), n(W8, 0), n(Z8, 3), n(B8, 0), n(P8, 1),
        n(W8, 0), n(NEW8, 0), n(B8, 0), "{:,.0f}".format(RAW8), n(BATCH8.std(), 1), n(Z8b, 3), n(P8b, 1)),
    "The silent bug is the one that gives a believable wrong number.",
    "A broken clock that says 3 o'clock at night is easy to spot. A clock that is ten minutes wrong "
    "is the one that makes you late.",
    [("batch", "a group of new examples arriving together"),
     ("silent bug", "a mistake that gives no error message, just a wrong answer")]),

  spot=M("Scaling one new house with its own statistics.",
    """<p>Prediction code for a single new house:</p>%s<p>What happens, and what is the fix?</p>""" % code(
        "X_new = np.array([[1900, 3]])\n"
        "mu = X_new.mean(axis=0)\n"
        "sigma = X_new.std(axis=0)\n"
        "X_new_s = (X_new - mu) / sigma"),
    """<p>With one row, each column's mean is the value itself and its &sigma; is <b>0</b>. The code does
0 / 0 for every feature, so <code>X_new_s</code> is all <code>nan</code> (with a divide warning).</p>
<p>Fix: use the <code>mu</code> and <code>sigma</code> <b>saved from training</b>, never ones computed
from <code>X_new</code>.</p>""",
    "One house has no spread, so it cannot supply its own scaling.",
    "You cannot say if someone is tall by measuring only them. You need the rest of the class to "
    "compare against.",
    [("nan", "&ldquo;not a number&rdquo; &mdash; what you get from 0 divided by 0"),
     ("axis=0", "work down each column")]),

  transfer=M("The same rule in a new place: before or after the split?",
    """<p>You have 10,000 rows. You compute &mu; and &sigma; on <b>all</b> of them, scale, and only then
split into training and test sets. Is anything wrong? Where else in the course will this exact
rule come back?</p>""",
    """<p>Yes, a mild <b>leak</b>: the test rows helped choose the scaling, so the test set is not
completely unseen. Split first, fit &mu; and &sigma; on the training part, then apply them to the
test part.</p>
<p>The rule returns for <b>PCA</b> in C3 and for any preprocessing step: fit on training data, apply
everywhere.</p>""",
    "Fit every preprocessing step on training data only, then apply it everywhere else.",
    "If you peek at the test answers while studying, your test score no longer tells you how much "
    "you really know.",
    [("leak", "information from the test set sneaking into training"),
     ("test set", "data kept aside to check the model at the end"),
     ("PCA", "a C3 method that also needs statistics from training data")]),
),

# =================================================================== q09
D("c1w2-q09",
  recall=M("The vectorized gradient, with every shape.",
    """<p>From memory, write the vectorized gradient for multiple linear regression, for <var>w</var>
and for <var>b</var>, and the shape of every piece.</p>""",
    """<p>err = <code>X @ w + b - y</code> &mdash; shape (m,).</p>
<p>&part;J/&part;<var>w</var> = (1/m) <code>X.T @ err</code> &mdash; shape <b>(n,)</b>, one per weight.</p>
<p>&part;J/&part;<var>b</var> = mean(err) &mdash; one number.</p>""",
    "One slope per weight, each built from all m errors.",
    "Each knob gets its own instruction: turn me up a bit, or down a bit. To decide, it listens to "
    "every house's mistake.",
    [("&part;J/&part;w", "&ldquo;how much the cost changes when w changes&rdquo; &mdash; the slope"),
     ("X.T", "X flipped so rows become columns (the transpose)"),
     ("err", "prediction minus truth, for every example")]),

  work=M("One gradient by hand, on three examples.",
    """<p><code>X</code> = [[1, 2], [3, 1], [2, 2]], <var>y</var> = [5, 6, 7], <var>w</var> = [1, 1],
<var>b</var> = 0.</p>
<p>Compute the predictions, the errors, &part;J/&part;<var>w</var> and &part;J/&part;<var>b</var>.</p>""",
    """<p>Predictions = [%s]. Errors = [%s].</p>
<p>&part;J/&part;<var>w</var><sub>1</sub> = (1&times;(&minus;2) + 3&times;(&minus;2) + 2&times;(&minus;3)) / 3
= %s. &part;J/&part;<var>w</var><sub>2</sub> = (2&times;(&minus;2) + 1&times;(&minus;2) + 2&times;(&minus;3)) / 3
= %s. So the gradient is <b>[%s]</b> &mdash; length 2, one per weight, as it must be.</p>
<p>&part;J/&part;<var>b</var> = mean(errors) = <b>%s</b>.</p>""" % (
        ", ".join(n(v, 0) for v in F9), ", ".join(n(v, 0) for v in E9), n(G9[0], 3), n(G9[1], 3),
        ", ".join(n(v, 3) for v in G9), n(GB9, 3)),
    "Each weight's slope is the average of (error &times; that feature).",
    "If houses with a big feature also had big mistakes, that feature's knob needs turning the most.",
    [("partial derivative", "the slope in one direction only, holding the others still"),
     ("average", "add them up, divide by how many")]),

  spot=M("A transpose left out. Sometimes it crashes, sometimes it doesn't.",
    """<p>Someone writes the gradient as:</p>%s
<p>With <code>X</code> of shape (3, 2) this crashes. With a square (2, 2) <code>X</code> =
[[1, 2], [3, 4]] and <code>err</code> = [1, &minus;1], it runs. Is the square case right?</p>""" % code(
        "dj_dw = np.dot(X, err) / m"),
    """<p>No. It needs <code>X.T</code>. On the square case the right answer is <code>X.T @ err / 2</code>
= <b>[%s]</b>; the buggy line gives <b>[%s]</b>. It runs silently and is wrong.</p>
<p>The crash on (3, 2) was a gift. The square case is the dangerous one, because shapes happen to
line up.</p>""" % (", ".join(n(v, 1) for v in RIGHT9), ", ".join(n(v, 1) for v in WRONG9)),
    "Matching shapes do not prove the maths is right.",
    "A key that fits the lock is not always the right key. Sometimes it opens the wrong door.",
    [("transpose", "flip a table so its rows become columns"),
     ("square matrix", "same number of rows and columns")]),

  transfer=M("Scaling up: 50 features, and next week's model.",
    """<ol><li>With 50 features, how many numbers does one gradient-descent update change? Does the
vectorized code change if you add a 51st feature?</li>
<li>Next week, logistic regression uses <var>f</var> = sigmoid(<code>X @ w + b</code>). Guess what
its gradient formula looks like.</li></ol>""",
    """<ol><li><b>51</b> &mdash; 50 weights and <var>b</var>. The code does not change at all; only the
shapes grow. That is the point of vectorizing.</li>
<li>Exactly the same form: (1/m) <code>X.T @ err</code>, where err is now sigmoid(<code>X @ w + b</code>)
&minus; <var>y</var>. Only <var>f</var> changes.</li></ol>""",
    "Write it vectorized once and it works for any number of features.",
    "A recipe that says &ldquo;one spoon of sugar per guest&rdquo; works for 5 guests or 50. You do "
    "not rewrite it each time.",
    [("sigmoid", "a squashing function that turns any number into one between 0 and 1"),
     ("logistic regression", "next week's model, for yes/no answers")]),
),

# =================================================================== q10
D("c1w2-q10",
  recall=M("The normal equation: three strengths, three limits.",
    """<p>From memory: three things the normal equation does better than gradient descent, and three
reasons it is not used for the rest of the specialization.</p>""",
    """<p><b>Better:</b> one step, no &alpha; to choose, no iterations, no feature scaling needed.</p>
<p><b>Limits:</b> it costs roughly n&sup3; (inverting an n&times;n matrix), so it gets slow for large n;
it exists only for <b>linear</b> regression; it does not work for logistic regression or neural
networks.</p>""",
    "A shortcut that only exists for one kind of model.",
    "It is a secret tunnel that goes straight to the treasure &mdash; but only in this one castle. "
    "Every other castle, you have to climb the stairs.",
    [("closed form", "a formula that gives the answer straight away, no steps"),
     ("n&sup3;", "cost grows like n &times; n &times; n &mdash; ten times the features, a thousand "
      "times the work"),
     ("matrix inverse", "the &ldquo;undo&rdquo; of a matrix, which is expensive to compute")]),

  work=M("Solve a three-point line in one step.",
    """<p><var>x</var> = [1, 2, 3], <var>y</var> = [2, 4, 5]. Find the least-squares <var>w</var> and
<var>b</var> using the one-feature closed form: <var>w</var> = &Sigma;(<var>x</var>&minus;<span>x&#772;</span>)(<var>y</var>&minus;<span>y&#772;</span>)
/ &Sigma;(<var>x</var>&minus;<span>x&#772;</span>)&sup2;, then <var>b</var> = <span>y&#772;</span> &minus;
<var>w</var><span>x&#772;</span>.</p>""",
    """<p><span>x&#772;</span> = 2, <span>y&#772;</span> &asymp; 3.667. Top: (&minus;1)(&minus;1.667) + 0 +
(1)(1.333) = 3. Bottom: 1 + 0 + 1 = 2.</p>
<p><var>w</var> = 3 / 2 = <b>%s</b>, <var>b</var> = 3.667 &minus; 1.5&times;2 &asymp; <b>%s</b>.
The full normal equation gives the same: %s and %s.</p>""" % (
        n(W10, 3), n(B10, 3), n(W10, 4), n(B10, 4)),
    "For linear regression you can calculate the best line directly.",
    "Instead of trying lots of lines and shuffling closer, you use a formula that tells you the best "
    "line straight away.",
    [("x&#772; (x-bar)", "the average of x"),
     ("&Sigma; (sigma)", "add up all of these"),
     ("least-squares", "the line with the smallest total squared error")]),

  spot=M("&ldquo;The two methods disagree, so one is broken.&rdquo;",
    """<p>&ldquo;On the same data (<var>x</var> = [1, 2, 3], <var>y</var> = [2, 4, 5]), the normal
equation gave <var>w</var> = %s. Gradient descent on <b>z-scored</b> <var>x</var>, run to convergence,
gave <var>w</var> = %s. They disagree, so my gradient descent is wrong.&rdquo;</p>
<p>Is it?</p>""" % (n(W10, 4), n(WS10, 4)),
    """<p>No. They are the same line <b>in different units</b>. Gradient descent's weight is per
standard deviation of <var>x</var>; divide by &sigma; = %s and you get %s / %s = <b>%s</b>, matching
the normal equation.</p>
<p>Always convert back before comparing weights from scaled and unscaled models.</p>""" % (
        n(SD10, 4), n(WS10, 4), n(SD10, 4), n(WS10 / SD10, 4)),
    "Weights learned on scaled features are in scaled units.",
    "One friend says the table is 2 metres long, the other says 200 centimetres. They are not "
    "arguing; they are just using different rulers.",
    [("units", "what a number is counted in, like metres or centimetres"),
     ("per standard deviation", "how much y changes for one typical step of x, not one unit")]),

  transfer=M("Three projects: which solver?",
    """<p>Pick normal equation or gradient descent for each, with one reason:</p>
<ol><li>Linear regression, 8 features, 1,000,000 rows.</li>
<li>Linear regression, 50,000 features (word counts from text).</li>
<li>Logistic regression, 10 features.</li></ol>""",
    """<ol><li><b>Normal equation</b> is fine: n = 8 is tiny, so the n&sup3; part is trivial; building
X<sup>T</sup>X over a million rows is one pass.</li>
<li><b>Gradient descent</b>: 50,000&sup3; is over 10<sup>14</sup> operations for the inverse alone.</li>
<li><b>Gradient descent</b>: logistic regression has no closed form at all.</li></ol>""",
    "Use the shortcut when n is small and the model is linear; otherwise take steps.",
    "Take the secret tunnel when the castle is small and has one. Otherwise climb.",
    [("solver", "the method that finds the weights"),
     ("10<sup>14</sup>", "a 1 followed by 14 zeros &mdash; far too much work")]),
),
]
