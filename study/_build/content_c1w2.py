# -*- coding: utf-8 -*-
"""C1 · Week 2 — Regression with multiple input variables."""
from kit import (kid, key, warn, trap, note, card, eq, eqp, decode, table, demo,
                 quiz, links, code, h2, grid2, grid3, pretest, explain, lenses)

REPO = "../../C1%20-%20Supervised%20Machine%20Learning%20-%20Regression%20and%20Classification"
L = []

# ============================================================ 1
L.append(dict(
    slug="01-multiple-features", title="Multiple features", mins=14, tag="core",
    lede="Houses have more than a size. Four features instead of one, and the notation that keeps track "
         "of which is which.",
    body=(
        pretest("""<p>Last week: price from size alone. Now you also know bedrooms, floors and age. <b>Guess how the formula changes — and how many numbers the model now has to learn.</b></p>""",
        """<p>Watch for the subscript that appears, and for the rule about which superscript means “which example” versus “which feature”.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Last week you guessed the price of a house from one thing: how big it is. But you know
more than that — how many bedrooms, how many floors, how old it is.</p>
<p>So give each one its own dial. Turn up the bedroom dial if bedrooms matter a lot; turn the age dial
negative because older houses are usually worth less.</p>
<p>Four dials instead of one. Same idea, more of it.</p>""")

        + lenses(
            """<p>Valuing a house on floor area alone gets you close. Everyone knows the other things that matter —
bedrooms, age, whether it is on a main road — and each one adds a correction.</p>
<p>An estate agent does not have a formula. She has a starting figure and a list of adjustments, and that
list is what a multi-feature model is.</p>""",
            """<p>This is multiple linear regression, and if you have run one in R, Stata or a spreadsheet, the model
is identical.</p>
<p>The coefficient interpretation carries across exactly: <var>w</var><sub>j</sub> is the change in
<var>y</var> per unit change in <var>x</var><sub>j</sub>, <b>holding the others fixed</b> — and that last
clause is the part people forget when features are correlated.</p>""",
            """<p>The spreadsheet gains columns. One row is still one house; there are now four numbers to the left of
the price instead of one.</p>
<p>The notation follows the picture: <var>x</var><sup>(i)</sup> is a whole <b>row</b>,
<var>x</var><sub>j</sub><sup>(i)</sup> is one <b>cell</b>. Superscript is the row, subscript the
column.</p>""",
            """<p>Real models have hundreds of columns, and the geometry stops being drawable at three. This is where
you have to start trusting the algebra over the picture.</p>
<p>The good news is that nothing in the maths changes — the dot product handles four features exactly as
it handles four hundred, which is why the vector notation is worth adopting now rather than later.</p>""",
            """So the notation below is bookkeeping for a wider table, and the model is the same line it always
was.""")

        + h2("🎬", "Watch it move")
        + demo("multifeatures", "The table, and what each subscript means",
               "watch the highlighted cell and read its name underneath")

        + h2("🔢", "The maths, decoded")
        + eqp([
            ('<var>f</var>(<var>x</var>)', "func-f", "apply the model to x"),
            ' <span class="op">=</span> <var>w</var><sub>1</sub><var>x</var><sub>1</sub> <span class="op">+</span> <var>w</var><sub>2</sub><var>x</var><sub>2</sub> <span class="op">+</span> <var>w</var><sub>3</sub><var>x</var><sub>3</sub> <span class="op">+</span> <var>w</var><sub>4</sub><var>x</var><sub>4</sub> <span class="op">+</span> <var>b</var>',
        ], "one weight per feature, plus one bias — hover or click it")
        + eqp([
            '<var>f</var>(<var>x</var>) <span class="op">=</span> ',
            ('<var class="hl-a">w⃗</var> <span class="op">·</span> <var class="hl-b">x⃗</var>',
             "dot-product-f0", "multiply matching entries, add them up"),
            ' <span class="op">+</span> <var>b</var>',
        ], "…written compactly as a dot product — hover or click it")
        + decode([
            ("<var>n</var>", "“n”", "The number of <b>features</b>. Four here. (m is still the number of examples.)"),
            ("<var>x</var><sub><var>j</var></sub>", "“x sub j”", "Feature j. x₁ = size, x₂ = bedrooms, and so on."),
            ("<var>x⃗</var><sup>(<var>i</var>)</sup>", "“x vector, example i”", "The whole row for house i — a vector of n numbers. The little arrow means “this is a vector”."),
            ("<var>x</var><sub><var>j</var></sub><sup>(<var>i</var>)</sup>", "“x sub j, superscript i”", "Feature j of example i. One single number. Subscript = which column, superscript = which row."),
            ("<var>w⃗</var>", "“w vector”", "All n weights in one list. b stays a single number."),
            ("·", "“dot”", "The dot product: multiply matching entries, add them all up."),
        ])
        + key("""<p><b>Subscript = which feature. Superscript in round brackets = which example.</b>
x₂<sup>(3)</sup> is the number of bedrooms of the third house. Get this straight now — it is used
constantly for the rest of the specialization.</p>""")

        + h2("🔬", "Reading the weights")
        + """<p>With w = [0.1, 4, 10, −2] and b = 80, in units of $1000s:</p>
<ul>
<li>w₁ = 0.1 → each extra square foot adds $100.</li>
<li>w₂ = 4 → each extra bedroom adds $4,000.</li>
<li>w₃ = 10 → each extra floor adds $10,000.</li>
<li>w₄ = −2 → each extra year of age <em>subtracts</em> $2,000.</li>
<li>b = 80 → a base price of $80,000 before any feature is considered.</li>
</ul>
<p>That readability is a genuine advantage of linear models, and it is the first thing you lose when you
move to a neural network.</p>"""
        + warn("""<p>Be careful about causal language. w₂ = 4 does <b>not</b> mean “adding a bedroom to your
house raises its value by $4,000”. It means “among houses in this dataset, holding the other features
fixed, an extra bedroom is <em>associated</em> with $4,000 more”. Correlation, not intervention.</p>""")

        + h2("🧮", "Four features, one real prediction")
        + """<p>The optional lab’s three-house data set, with four features each — size, bedrooms,
floors, age — and the fitted parameters it hands you:</p>"""
        + code("""
X_train = np.array([[2104, 5, 1, 45],
                    [1416, 3, 2, 40],
                    [ 852, 2, 1, 35]])
y_train = np.array([460., 232., 178.])

w = np.array([0.39133535, 18.75376741, -53.36032453, -26.42131618])
b = 785.1811367994083
""")
        + """<p>Predict the first house — a dot product plus b:</p>"""
        + table(["term", "value"],
                [["0.39133535 × 2104", "+823.37"],
                 ["18.75376741 × 5", "+93.77"],
                 ["−53.36032453 × 1", "−53.36"],
                 ["−26.42131618 × 45", "−1188.96"],
                 ["+ b", "+785.18"],
                 ["<b>prediction</b>", "<b>460.00000</b>"]])
        + """<p>Against an actual price of 460.0 — correct to five decimal places, and the other two
houses match exactly too. Those weights were fitted to these three points, so this is a check that
the arithmetic is right, not evidence the model is good.</p>"""
        + warn("""<p>Do not read the weights as importance. Floors gets −53.36 and size gets 0.391,
which does <em>not</em> mean floors matter 136 times more — the weights carry the features’ units.
Size is measured in thousands of square feet worth of digits, floors in ones. Comparing weights is
only meaningful after scaling, which is the next lesson but one.</p>""")
        + explain("""<p>Age has weight −26.42, so older houses are predicted cheaper. <b>Why can you
not conclude that ageing a house reduces its value by $26,420 a year?</b></p>""",
                  """<p>Because the weight is a fit to three data points with four features — the
model has more freedom than data, so it can fit any values whatsoever and the individual weights are
not identified. More generally, even with plenty of data, a regression weight is a
<em>partial association</em> given the other features in the model, not a causal effect. Older
houses here also differ in size and floors, and the weights split the credit between correlated
features in ways that need not correspond to anything you could change.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("What is x₃⁽²⁾ in the table?",
             "<p>Feature 3 (floors) of example 2 — the second house. In the demo's table that is <b>2</b>.</p>"),
            ("You have 1000 houses and 12 features. What are m and n?",
             "<p>m = <b>1000</b> examples, n = <b>12</b> features. How many parameters? 12 weights plus "
             "one b = <b>13</b>.</p>"),
            ("Why is b not written as w₀ with a feature x₀?",
             "<p>It sometimes is — the trick is to define x₀ = 1 always, so w₀x₀ = w₀ = b. It makes the "
             "formulas tidier and this course keeps b separate for clarity.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("lab", REPO + "/week2/Optional%20Labs/C1_W2_Lab02_Multiple_Variable_Soln.ipynb",
             "Optional lab: Multiple Variable Linear Regression",
             "In this repo. The full multi-feature implementation, with all the shapes printed out."),
        ])
    )))

# ============================================================ 2
L.append(dict(
    slug="02-vectorization", title="Vectorization", mins=14, tag="code",
    lede="Replace a loop with one function call. Shorter to write, faster to run, and the standard way "
         "every real ML codebase is written.",
    body=(
        pretest("""<p>You could add up 100,000 products with a Python <code>for</code> loop, or one NumPy call. <b>Guess how much faster the second is — and why, given both do the same multiplications.</b></p>""",
        """<p>Watch for where the speed actually comes from. It is not that NumPy loops faster; it is that it does not loop in Python at all.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>You have to multiply 100 pairs of numbers and add up the results.</p>
<p>You could do it one pair at a time, writing each answer down. Or you could hand the whole list to a
machine built for exactly this job and get the total back in one go.</p>
<p>Same answer. Far less typing, and far less waiting.</p>""")

                + lenses(
            """<p>Paying a hundred builders. You could hand each one a numbered envelope of cash, one at a time,
walking the site all afternoon. Or you could send a single instruction to the bank and have all
hundred paid at once.</p>
<p>Identical money, identical people. The difference is entirely in how many separate trips someone
had to make — and that is the whole of vectorisation.</p>""",
            """<p>If you have written SQL, you already have the instinct: you do not fetch a million rows and loop
over them in your application; you push the operation down to the engine and let it do the whole set
at once.</p>
<p><code>np.dot</code> is that same move. The loop still happens — but it happens in compiled code
that was written for exactly this, instead of in the Python interpreter.</p>""",
            """<p>A supermarket with one till open, versus twenty.</p>
<p>The same customers, the same items scanned, the same total takings. What collapses is the queue.
A CPU with SIMD instructions is a shop that can scan several items in one motion; a GPU is a shop
with thousands of tills.</p>""",
            """<p>This is not a micro-optimisation — it is the reason modern AI is economically possible at all.
Training a large model with Python loops would take longer than the age of the universe. Training it
with vectorised operations on a GPU takes weeks.</p>
<p>The gap between those two facts is the entire hardware industry that grew up around machine
learning.</p>""",
            """So the timing comparison below is the difference between a technique that works and one that
merely exists on paper.""")
        + h2("🎬", "Watch it move")
        + demo("vectorization", "The dot product forming, and the three ways to write it",
               "only the third one is worth writing")

        + h2("💻", "The three versions")
        + code("""
# 1. no vectorisation — unreadable, and hopeless when n = 100
f = w[0]*x[0] + w[1]*x[1] + w[2]*x[2] + b

# 2. a for loop — readable, and slow
f = 0
for j in range(n):
    f = f + w[j] * x[j]
f = f + b

# 3. vectorised — short AND fast
f = np.dot(w, x) + b
""")
        + decode([
            ("<code>np.dot(w, x)</code>", "“the dot product”", "Multiplies matching entries and sums them. Two arrays in, one number out."),
            ("<code>np.array</code>", "“a NumPy array”", "Not a Python list. Arrays support elementwise arithmetic; lists do not."),
            ("vectorisation", "“whole-array operations”", "Expressing a computation over entire arrays instead of element by element."),
            ("0-indexing", "“the off-by-one tax”", "The maths writes w₁ … w<sub>n</sub>; NumPy writes w[0] … w[n−1]. Same numbers, shifted names."),
        ], head=("Piece", "Say it out loud", "What it is"))
        + key("""<p>Two separate wins, and they compound: the code is <b>shorter</b> (fewer places to make
a mistake) and it <b>runs faster</b> (next lesson explains why). This is why you will almost never see an
explicit loop over features in real ML code.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Using a Python list instead of a NumPy array.</b> <code>[1,2,3] * 2</code> gives
<code>[1,2,3,1,2,3]</code>. <code>np.array([1,2,3]) * 2</code> gives <code>[2,4,6]</code>. Completely
different behaviour, no error message.</p>""")
        + trap("""<p><b>Mixing up <code>*</code> and <code>np.dot</code>.</b> The star multiplies
elementwise and returns an <em>array</em>. <code>np.dot</code> multiplies <em>and sums</em>, returning a
<em>number</em>. The model needs the number.</p>""")
        + trap("""<p><b>Off-by-one between maths and code.</b> w₁ in a formula is <code>w[0]</code> in
NumPy. Be deliberate about it, especially when translating a formula from a lecture.</p>""")

        + explain("""<p><code>[1,2,3] * 2</code> gives <code>[1,2,3,1,2,3]</code> and <code>np.array([1,2,3]) * 2</code>
gives <code>[2,4,6]</code>. <b>Say why Python is right in both cases, and why that makes the bug so
dangerous.</b></p>""",
                  """<p>For a <em>list</em>, <code>*</code> means repeat — the same meaning it has for strings. For an
<em>array</em>, it means multiply each element. Both are correct behaviour for their own type, so
neither raises.</p>
<p>That is exactly what makes it dangerous: your gradient is silently six numbers long instead of
three, the shapes may still be compatible downstream, and the model trains to something confidently
wrong. A bug that errors is cheap; this one costs you an afternoon.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("w = [1, 2, 3], x = [10, 20, 30], b = 5. What is np.dot(w, x) + b?",
             "<p>1(10) + 2(20) + 3(30) = 10 + 40 + 90 = 140, plus 5 = <b>145</b>.</p>"),
            ("What does w * x give instead, for those same arrays?",
             "<p><code>[10, 40, 90]</code> — an array, not a number. Elementwise multiplication with no "
             "summing.</p>"),
            ("Which index in code corresponds to w₃ in the maths?",
             "<p><code>w[2]</code>. Maths counts from 1; NumPy counts from 0.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("lab", REPO + "/week2/Optional%20Labs/C1_W2_Lab01_Python_Numpy_Vectorization_Soln.ipynb",
             "Optional lab: Python, NumPy and Vectorization",
             "In this repo. The most useful optional lab in Course 1 — it also times the loop against np.dot so you see the difference."),
            ("docs", "https://numpy.org/doc/stable/user/absolute_beginners.html",
             "NumPy — the absolute beginner’s guide",
             "If NumPy is new, read this once. It pays for itself within a week."),
            ("docs", "https://numpy.org/doc/stable/reference/generated/numpy.dot.html",
             "numpy.dot",
             "Note how its behaviour changes with input dimensionality — a genuine source of confusion later."),
        ])
    )))

# ============================================================ 3
L.append(dict(
    slug="03-why-vectorization-is-fast", title="Why vectorization is fast", mins=13, tag="core",
    lede="Not because NumPy is clever maths. Because it hands the whole array to hardware that can do "
         "many multiplications at the same instant.",
    body=(
        pretest("""<p>Both versions do exactly the same arithmetic. <b>So where could the time possibly be going in the slow one?</b></p>""",
        """<p>Watch for what the hardware can do with many numbers at once, and for what Python costs you on every single step of a loop.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>A for loop is one person doing sums on a piece of paper: first pair, write it down,
second pair, write it down.</p>
<p><code>np.dot</code> is handing the whole sheet to a room of a hundred people who all do their sum at
once, then a machine that adds up all hundred answers in one go.</p>
<p>Your computer really does have that room. A Python loop simply never asks it to help.</p>""")

        + lenses(
            """<p>Twelve people carrying one sack each in a single trip, versus one person making twelve trips.</p>
<p>Same twelve sacks. The first finishes in a twelfth of the time, and not because anyone is walking
faster — because twelve things happened at once.</p>""",
            """<p>The mechanism is <b>SIMD</b>: one instruction applied to several numbers simultaneously, built into
the processor.</p>
<p>If you have been told to avoid loops in R or pandas, this is the reason. The loop is not slow because
looping is slow; it is slow because each pass goes through the Python interpreter and never reaches the
instructions that handle sixteen floats at once.</p>""",
            """<p>Two blocks of code side by side computing the identical result: a <code>for</code> loop over 100,000
elements, and <code>np.dot(w, x)</code>.</p>
<p>Time them. The factor is typically 50 to 200, and seeing the number yourself is what makes the habit
stick.</p>""",
            """<p>The consequence scales all the way up: this is why GPUs matter, because a GPU is thousands of small
cores that are useful only if handed thousands of independent multiplications at once.</p>
<p>Training a large model is possible because its core operation happens to be exactly the operation this
hardware is best at.</p>""",
            """So <code>np.dot</code> below is not shorter code. It is different code, reaching parts of the machine
a loop never touches.""")

        + h2("🎬", "Watch it move")
        + demo("vectorfast", "The loop, tick by tick, and the vectorised version in one",
               "same 16 multiplications, very different amounts of waiting")

        + h2("🔢", "What is actually happening")
        + table(["", "The for loop", "np.dot"],
                [["Executed by", "the Python interpreter", "compiled, optimised library code (BLAS)"],
                 ["Per-element overhead", "large — type checks, object handling", "essentially none"],
                 ["Uses SIMD instructions", "no", "<b>yes</b> — many multiplies per instruction"],
                 ["Uses multiple cores", "no", "usually yes"],
                 ["Typical speedup", "—", "<b>10× to 100×</b>, more on large arrays"]])
        + decode([
            ("SIMD", "“single instruction, multiple data”", "One CPU instruction that multiplies several pairs of numbers simultaneously. Standard on every modern processor."),
            ("BLAS", "“Basic Linear Algebra Subprograms”", "A decades-old, viciously optimised library that NumPy calls underneath. You are standing on a lot of work."),
            ("GPU", "“graphics card”", "Thousands of small cores. Useless for one multiplication; extraordinary for a million at once. This is why deep learning runs on them."),
        ])
        + key("""<p>The maths is <b>identical</b>. Vectorisation changes nothing about the answer and
everything about how long you wait. On a large dataset this is the difference between a model that trains
overnight and one that trains over a fortnight.</p>""")

        + h2("🔬", "Scaling up gradient descent")
        + """<p>The same idea applies to the update step. With 16 features, the non-vectorised version is:</p>"""
        + code("""
for j in range(16):
    w[j] = w[j] - 0.1 * d[j]
""")
        + """<p>and the vectorised version is one line that does all sixteen at the same moment:</p>"""
        + code("""
w = w - 0.1 * d
""")
        + """<p>With 16 parameters this hardly matters. With 100,000 — an entirely ordinary size for a
neural network — it is the difference between practical and impossible.</p>"""

        + h2("🧮", "Timed on ten million numbers")
        + """<p>Two vectors of 10,000,000 elements, dot-producted both ways, measured on this
machine:</p>"""
        + table(["Version", "time", "relative"],
                [["<code>for i in range(n): s += a[i]*b[i]</code>", "≈ 2,154 ms", "1×"],
                 ["<code>np.dot(a, b)</code>", "<b>11.4 ms</b>", "<b>≈ 189× faster</b>"]])
        + """<p>Two seconds against one hundredth of a second, for identical arithmetic — the same ten
million multiplications and ten million additions happen either way.</p>
<p>The difference is where the work is done. The loop runs in the Python interpreter, which for every
single element re-checks types, looks up methods and builds a temporary object. <code>np.dot</code>
hands the whole array to compiled code that pays none of that per element, reads memory in a
cache-friendly order, and uses SIMD instructions that perform several multiplications per clock
cycle.</p>
<p>Now scale it up. A single gradient-descent step is a dot product; a real run is thousands of
steps. At 189×, two seconds per step becomes eleven milliseconds — the difference between a model
you can iterate on and one you cannot.</p>"""
        + explain("""<p>The speedup comes from removing the loop, not from doing less arithmetic.
<b>So why is <code>np.dot</code> on a 10-element array barely faster than a Python loop?</b></p>""",
                  """<p>Because there is a fixed cost to entering NumPy at all — checking shapes and
dtypes, and dispatching into the compiled routine — and it is paid once per call regardless of size.
On 10 elements that overhead dominates and the loop is competitive. On 10 million it is invisible,
amortised over every element. The lesson is that vectorisation pays in proportion to how much work
each call does, which is why the goal is few large array operations rather than many small
ones.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("Does vectorisation change the answer your model produces?",
             "<p>No — up to tiny floating-point differences from a different summation order. Same maths, "
             "same result.</p>"),
            ("Why is it faster, in one sentence?",
             "<p>Because it hands the whole array to compiled code that uses parallel hardware, instead "
             "of paying Python interpreter overhead once per element.</p>"),
            ("Would a GPU speed up np.dot on two 3-element arrays?",
             "<p>No — the cost of shipping data to the GPU would dwarf the work. GPUs win on <em>large</em> "
             "arrays and large batches.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("lab", REPO + "/week2/Optional%20Labs/C1_W2_Lab01_Python_Numpy_Vectorization_Soln.ipynb",
             "Optional lab: Vectorization",
             "In this repo. Times a loop against np.dot on 10 million elements. The number is startling."),
            ("docs", "https://numpy.org/doc/stable/user/whatisnumpy.html#why-is-numpy-fast",
             "NumPy — why is NumPy fast?",
             "The official answer: vectorisation and broadcasting, explained by the people who wrote it."),
        ])
    )))

# ============================================================ 4
L.append(dict(
    slug="04-gradient-descent-multiple-features", title="Gradient descent for multiple linear regression",
    mins=9, tag="core",
    lede="The same update rule, once per parameter — plus the one alternative method that exists only for "
         "linear regression.",
    body=(
        pretest("""<p>Two parameters needed two update lines. Now there are twelve features. <b>Guess how many update lines you need — and what must be true about when they happen.</b></p>""",
        """<p>Watch for the simultaneity rule you met last week, and for why it now matters across thirteen values instead of two.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>You had two dials to tune. Now you have five. Nothing else changes: work out which way
each dial should move, then move them all at the same moment.</p>""")

        + lenses(
            """<p>Adjusting four guy ropes instead of one. Same procedure at every rope: feel which way it wants to
go, move a little, come back round.</p>
<p>No new skill is required. There are simply more ropes, and you adjust them all before walking round
again.</p>""",
            """<p>The gradient is now a <b>vector</b>, one partial derivative per parameter, and every component has
exactly the form you derived last week.</p>
<p>If you have done multivariable calculus, this is the gradient of a scalar field, and gradient descent
is following it downhill in <var>n</var> dimensions. The formula per component is unchanged.</p>""",
            """<p><var>n</var> update lines instead of two, computed together and applied together.</p>
<p><code>w = w - alpha * dj_dw</code>, where both <code>w</code> and <code>dj_dw</code> are arrays of
length <var>n</var>. One line of NumPy is <var>n</var> simultaneous updates, which is the vectorisation
lesson paying off immediately.</p>""",
            """<p>Simultaneous update matters more here than it did with two parameters, because there are more chances
to get it wrong.</p>
<p>Compute the entire gradient vector from the current parameters, <em>then</em> assign. Updating in place
inside a loop over features is a real bug that still converges to something slightly wrong, which is the
worst kind.</p>""",
            """So the vector update below is last week's algorithm with the ropes counted.""")

        + h2("🎬", "Watch it move")
        + demo("gdmulti", "n + 1 update lines, all almost identical",
               "the only thing that differs between them is which x is on the end")

        + h2("🔢", "The maths, decoded")
        + eqp([
            ('<var>w</var><sub><var>j</var></sub> <span class="op">:=</span>', "assign-op", "becomes, not equals"),
            ' <var>w</var><sub><var>j</var></sub> <span class="op">−</span> ',
            ('<var>α</var>', "alpha-lr", "the learning rate"),
            ' ',
            ('<span class="frac"><span>1</span><span><var>m</var></span></span>', "avg-factor", "the average"),
            ('<span class="big">Σ</span>', "sigma", "for every example"),
            (' <span class="paren">(</span> <var>f</var>(<var>x⃗</var><sup>(<var>i</var>)</sup>) <span class="op">−</span> <var>y</var><sup>(<var>i</var>)</sup> <span class="paren">)</span>',
             "error-term", "predicted − actual"),
            ('<var>x</var><sub><var>j</var></sub><sup>(<var>i</var>)</sup>', "times-xi", "only in the wⱼ-derivative"),
        ], "for j = 1 … n, all simultaneously — hover or click any part")
        + eqp([
            ('<var>b</var> <span class="op">:=</span>', "assign-op", "becomes, not equals"),
            ' <var>b</var> <span class="op">−</span> ',
            ('<var>α</var>', "alpha-lr", "the learning rate"),
            ' ',
            ('<span class="frac"><span>1</span><span><var>m</var></span></span>', "avg-factor", "the average"),
            ('<span class="big">Σ</span>', "sigma", "for every example"),
            (' <span class="paren">(</span> <var>f</var>(<var>x⃗</var><sup>(<var>i</var>)</sup>) <span class="op">−</span> <var>y</var><sup>(<var>i</var>)</sup> <span class="paren">)</span>',
             "error-term", "predicted − actual"),
        ], "…and b, which has no x on the end", small=True)
        + decode([
            ("<var>w</var><sub><var>j</var></sub>", "“w sub j”", "The weight belonging to feature j. Not one number any more — n of them, j = 1 … n."),
            ("<var>x⃗</var><sup>(i)</sup>", "“x vector, example i”", "The little arrow means “this is the whole row of features for example i”, not a single number — the arrow is the only thing that changed from Week 1's f(x⁽ⁱ⁾)."),
            ("<var>x</var><sub><var>j</var></sub><sup>(i)</sup>", "“x sub j, example i”", "One specific number: feature j, from example i. Two subscripts because you now need to say both which example and which feature."),
            ("<var>n</var>", "“n”", "The number of features. Not to be confused with m, the number of examples — n columns, m rows."),
        ])
        + """<p>Compare with Week 1. It is the same formula, with a subscript j added and the update
repeated for every feature. Simultaneous update still applies — and now it means all n + 1 parameters, not
just two.</p>"""

        + h2("💻", "Vectorised")
        + code("""
def compute_gradient(X, y, w, b):
    m = X.shape[0]
    err = (X @ w + b) - y            # (m,) — every prediction's error at once
    dj_dw = (X.T @ err) / m          # (n,) — one derivative per feature
    dj_db = np.sum(err) / m          # a scalar
    return dj_dw, dj_db

w = w - alpha * dj_dw                # all n weights updated in one line
b = b - alpha * dj_db
""")
        + key("""<p>No loop over features anywhere. <code>X.T @ err</code> computes all n derivatives in a
single matrix operation — and it is exactly the “multiply by x<sub>j</sub> and sum over i” from the
formula, done for every j at once.</p>""")

        + h2("🔬", "The normal equation")
        + """<p>There is an alternative that exists for linear regression and nothing else: solve for w and
b directly, in one shot, with an explicit formula. No iterations, no α, no convergence to check.</p>"""
        + table(["", "Gradient descent", "Normal equation"],
                [["Iterations", "many", "<b>none</b>"],
                 ["Need to choose α", "yes", "<b>no</b>"],
                 ["Works when n is large", "yes", "no — roughly n³ cost, slow past ~10,000 features"],
                 ["Works for other algorithms", "<b>yes, all of them</b>", "no — linear regression only"]])
        + """<p>Some scikit-learn implementations use it internally without telling you. Worth knowing it
exists so the term is not a surprise; not worth reaching for, because it generalises to nothing.</p>"""

        + explain("""<p>The normal equation needs no &alpha;, no iterations and no convergence check. <b>Say why the
whole specialization is nevertheless built on gradient descent.</b></p>""",
                  """<p>Because it <b>generalises to nothing else</b>. It is a closed-form solution that exists only
because linear regression with squared error happens to have one. Logistic regression does not,
neural networks do not, recommenders do not.</p>
<p>It also costs roughly O(<var>n</var>&sup3;) for the matrix inverse, so it is impractical past
about 10,000 features. Gradient descent is slower on the one problem where both work, and it is the
only method that survives Course 2 and Course 3.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("With 12 features, how many update equations run per iteration?",
             "<p><b>13</b> — one per weight plus one for b. All executed simultaneously.</p>"),
            ("Why does the b update have no x on the end?",
             "<p>Because b is added to every prediction equally, so ∂f/∂b = 1 for every example. "
             "(Equivalently: think of b as w₀ with x₀ = 1 always.)</p>"),
            ("When might the normal equation be preferable?",
             "<p>Small n (a few thousand features at most) and linear regression specifically. Never for "
             "logistic regression or neural networks — it simply does not apply.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("lab", REPO + "/week2/Optional%20Labs/C1_W2_Lab06_Sklearn_Normal_Soln.ipynb",
             "Optional lab: scikit-learn, normal equation",
             "In this repo. <code>LinearRegression</code> solves it in closed form — compare its answer to your gradient descent."),
            ("docs", "https://scikit-learn.org/stable/modules/linear_model.html#ordinary-least-squares",
             "scikit-learn — ordinary least squares",
             "Including the note that it uses an SVD-based solver rather than the naive normal equation, for numerical stability."),
        ])
    )))

# ============================================================ 5
L.append(dict(
    slug="05-feature-scaling", title="Feature scaling", mins=20, tag="core",
    lede="A feature ranging 300–2000 next to one ranging 0–5 turns the cost bowl into a canyon. One "
         "division fixes it, and it is the highest-value line in this week.",
    body=(
        pretest("""<p>Size runs 300–2000. Bedrooms run 1–5. Both get a weight. <b>Guess what that 400× difference in range does to gradient descent.</b></p>""",
        """<p>Picture the bowl from Week 1, stretched long and thin. Watch for why the path zig-zags, and how one rescaling fixes it.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Imagine a see-saw where one child weighs 2000 kg and the other weighs 5 kg. Every tiny
movement by the heavy child sends the light one flying, and the light child can barely move the see-saw at
all.</p>
<p>Features are like that. If house size goes up to 2000 and bedrooms only up to 5, then a small change in
the size weight has an enormous effect while the bedroom weight barely matters — and gradient descent
spends its time bouncing across the canyon instead of walking down it.</p>
<p>Fix: make everyone roughly the same size before you start.</p>""")

                + lenses(
            """<p>A recipe calling for 2 kilos of flour and 3 grams of salt. Both numbers matter enormously, but
a 10% error in the salt is invisible while a 10% error in the flour ruins the loaf — <em>because of
the units they happen to be written in</em>, not because of what they do.</p>
<p>A baker fixes this by measuring proportionally: baker’s percentages, everything expressed relative
to the flour. Scaling features is the same move — put every ingredient on a comparable scale before
you start reasoning about them.</p>""",
            """<p>This is standardisation, and if you have computed a z-score you have done it: subtract the mean,
divide by the standard deviation.</p>
<p>The reason it matters computationally, though, is not statistical — it is geometric. Unequal
feature scales stretch the cost surface into a long thin valley, and gradient descent handles valleys
badly. Same arithmetic you know, deployed for a different reason.</p>""",
            """<p>A canyon versus a bowl, seen from above as contour rings.</p>
<p>Gradient descent always steps perpendicular to the contour it stands on. In a round bowl that
points at the centre. In a long thin canyon it points across the narrow direction, so you zig-zag
between the walls while barely advancing along the floor. Scaling turns the canyon back into a
bowl.</p>""",
            """<p>Measured on this site’s own data: the largest learning rate that does not diverge is
<b>9.4 × 10⁻⁷</b> unscaled and <b>0.97</b> after standardising. A factor of a million, from four lines
of arithmetic.</p>
<p>That is not a tuning nicety. Without scaling, a model with a size feature in the thousands and a
bedroom count in single digits is effectively untrainable by gradient descent.</p>""",
            """So the three methods below all do the same job — make the features comparable — and the z-score is
the default for the reason above.""")
        + h2("🎬", "Watch it move")
        + demo("featurescaling", "Turn scaling on and watch the bowl round out",
               "unscaled: a long thin canyon and a zig-zagging path. scaled: a circle and a direct walk")

        + h2("🔢", "The three methods")
        + table(["Method", "Formula", "Result", "When"],
                [["divide by max", "x₁ := x₁ / max", "0 … 1", "quick and crude"],
                 ["mean normalisation", "x₁ := (x₁ − μ₁) / (max − min)", "roughly −0.5 … 0.5, centred on 0", "when centring matters"],
                 ["<b>z-score</b>", "x₁ := (x₁ − μ₁) / σ₁", "mean 0, standard deviation 1", "<b>the usual choice</b>"]])
        + decode([
            ("μ<sub>j</sub>", "“mu j”", "The mean of feature j across the training set."),
            ("σ<sub>j</sub>", "“sigma j”", "The standard deviation of feature j — how spread out it is."),
            ("z-score", "“standardisation”", "The default in practice, and what <code>StandardScaler</code> does."),
            ("normalisation", "“a slippery word”", "Sometimes means min-max to 0…1, sometimes means z-score. Always check which one someone means."),
        ])
        + key("""<p>Aim for every feature to land roughly in <b>−1 to 1</b>. Andrew’s rules of thumb: −3 to 3
is fine, −0.3 to 0.3 is fine. Something ranging 0 to 0.001, or −100 to 100, wants rescaling.</p>""")

        + h2("💻", "In code")
        + code("""
mu    = X_train.mean(axis=0)      # one mean per feature      -> shape (n,)
sigma = X_train.std(axis=0)       # one std dev per feature    -> shape (n,)

X_train_scaled = (X_train - mu) / sigma
X_test_scaled  = (X_test  - mu) / sigma      # SAME mu and sigma — not recomputed

# and at prediction time, for a single new house:
x_new_scaled = (x_new - mu) / sigma
""")
        + warn("""<p>Compute μ and σ on the <b>training set only</b>, then apply those same numbers
everywhere — test set, cross-validation set, and every future prediction. Recomputing them on the test set
leaks information; forgetting to scale a new input at prediction time silently produces nonsense. Both are
extremely common production bugs.</p>""")

        + h2("🔬", "What it does to the picture")
        + """<p>Unscaled, the contours of J are long thin ellipses. Gradient descent’s step is perpendicular
to the contour it is standing on, which in a narrow canyon points mostly <em>across</em> the valley rather
than along it. So it zig-zags, and you must use a small α to stop it bouncing out — making the crawl along
the valley floor slower still.</p>
<p>Scaled, the contours are near-circles. Perpendicular now points almost straight at the centre, and a
much larger α is safe. Both effects pull in the same direction, which is why the speedup is often an order
of magnitude rather than a few percent.</p>"""

        + h2("🧮", "What scaling is worth — measured")
        + """<p>The lab’s <code>houses.txt</code>: 100 houses, four features, wildly different
ranges.</p>"""
        + table(["feature", "raw range", "mean", "sd"],
                [["size (sqft)", "788 … 3,194", "1,413.71", "412.17"],
                 ["bedrooms", "0 … 4", "2.71", "0.65"],
                 ["floors", "1 … 2", "1.38", "0.49"],
                 ["age", "12 … 107", "38.65", "25.79"]])
        + """<p>Size spans 2,406 units; floors spans 1. The cost bowl is therefore enormously
stretched, and here is what that costs you — the largest learning rate that does not diverge, found
by bisection:</p>"""
        + table(["", "largest usable α", ""],
                [["raw features", "<b>9.4 × 10⁻⁷</b>", "set by the size feature"],
                 ["after z-score scaling", "<b>0.966</b>", "about a million times larger"]])
        + """<p>A factor of a million. And with 100 iterations each: the unscaled run gets J from
71,024 down to 1,565; the scaled run reaches <b>222</b> — seven times lower, in the same number of
steps.</p>
<p>The reason is that α must be small enough for the <em>steepest</em> direction or the whole thing
diverges, and that one direction then dictates the pace for every other. Scaling makes all directions
comparably steep, so a single α suits them all. (This is the same argument that Adam solves
automatically in Course 2 Week 2.)</p>"""
        + explain("""<p>Scaling does not change the data’s information content, the best-fit line, or
the minimum cost achievable. <b>So what exactly does it change?</b></p>""",
                  """<p>The shape of the path to that minimum, and therefore how many steps it takes.
The optimum is the same point; the bowl around it is what gets reshaped, from a long thin canyon into
something round. Gradient descent always steps perpendicular to the contours, and in a canyon that
means bouncing across the narrow direction while creeping along the long one. Round contours point
straight at the centre. You are not helping the model — you are helping the optimiser find
it.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Scaling before splitting your data.</b> Computing μ over the whole dataset leaks
test information into training. Split first, then fit the scaler on the training half.</p>""")
        + trap("""<p><b>Forgetting to scale at prediction time.</b> The model was trained on standardised
inputs; feeding it a raw 2000 produces a wild answer. Keep the scaler and the model together — this is
what <code>sklearn.pipeline.Pipeline</code> is for.</p>""")
        + trap("""<p><b>Scaling the target y.</b> Usually unnecessary, and if you do it, remember to
un-scale the predictions before reporting them.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("A feature ranges 300–2000 with mean 1150 and σ 400. Z-score a house of 1800.",
             "<p>(1800 − 1150) / 400 = <b>1.625</b>. Comfortably inside a sensible range.</p>"),
            ("Which features need rescaling: 0–1, −100–100, 0.0001–0.001, 1–3?",
             "<p><b>−100 to 100</b> and <b>0.0001 to 0.001</b>. The other two are already in a workable "
             "range.</p>"),
            ("Why not recompute μ and σ on the test set?",
             "<p>Because it leaks information about the test set into your pipeline, and because the "
             "model was trained expecting one specific transform. Use the training values everywhere.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("lab", REPO + "/week2/Optional%20Labs/C1_W2_Lab03_Feature_Scaling_and_Learning_Rate_Soln.ipynb",
             "Optional lab: Feature Scaling and Learning Rate",
             "In this repo. Shows the contour shape before and after, and how much larger α can safely become."),
            ("docs", "https://scikit-learn.org/stable/modules/preprocessing.html#standardization-or-mean-removal-and-variance-scaling",
             "scikit-learn — StandardScaler",
             "The production tool. Note <code>fit_transform</code> on train, <code>transform</code> on test — the rule from this lesson, enforced by the API."),
            ("docs", "https://scikit-learn.org/stable/modules/compose.html#pipeline",
             "scikit-learn — Pipeline",
             "Bundles the scaler and the model into one object so you cannot forget to scale at prediction time."),
        ])
    )))

# ============================================================ 6
L.append(dict(
    slug="06-checking-convergence", title="Checking gradient descent for convergence", mins=12, tag="core",
    lede="One plot, three lines of code, and it tells you whether your model is training, stuck, or broken.",
    body=(
        pretest("""<p>Your model has been training for ten minutes. <b>How would you know whether to stop, keep going, or that something is broken?</b></p>""",
        """<p>Watch for the one plot that answers all three questions at once, and costs three lines to make.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>How do you know when to stop? Draw a graph of “how wrong am I?” against “how many steps
have I taken”.</p>
<p>If the line is falling, keep going. If it has gone flat, you are done. If it is going <b>up</b>,
something is wrong — and you have just saved yourself a day.</p>""")

                + lenses(
            """<p>Roasting a joint of meat. You do not open the oven every ten seconds, and you do not walk away
for three hours either. You check at sensible intervals and watch the temperature <em>trend</em> —
rising steadily, good; stalled, something is wrong.</p>
<p>The learning curve is that thermometer. One glance tells you whether to keep going, adjust, or
stop.</p>""",
            """<p>Any iterative solver you have used — Newton–Raphson, a numerical optimiser, even Excel’s Goal
Seek — has a convergence criterion, and it is always the same shape: stop when the change per step
falls below some ε.</p>
<p>The value of ε is a judgement, not a fact. Too tight and you burn compute for invisible gains; too
loose and you stop while the model is still improving.</p>""",
            """<p>One line falling from top-left to bottom-right, then flattening.</p>
<p>That shape is “healthy and finished”. Still descending at the right-hand edge means “not
finished”. Sawtoothing up and down means α is too large. Climbing off the top means α is far too
large, or the gradient is wrong. Four shapes, four diagnoses.</p>""",
            """<p>Training runs cost real money by the hour. Teams that do not plot this curve routinely do one of
two expensive things: stop early and ship an undertrained model, or run for hours after the loss
stopped moving.</p>
<p>It is three lines of matplotlib and it is the cheapest diagnostic in the entire field.</p>""",
            """So the plot below is the one output you should generate for every training run you ever do.""")
        + h2("🎬", "Watch it move")
        + demo("convergence", "Three learning curves — click between them",
               "one healthy, two broken in different ways")

        + h2("🔢", "How to read the curve")
        + table(["What you see", "What it means", "What to do"],
                [["falls smoothly, then flattens", "healthy, and converged", "stop — more iterations will not help"],
                 ["falls smoothly, still falling at the end", "healthy, not finished", "run for more iterations"],
                 ["oscillates up and down", "α is too large", "reduce α, typically by ×3 or ×10"],
                 ["increases steadily", "α far too large, or a bug", "try α = 0.0001. Still rising? It is a bug."]])
        + key("""<p><b>J must decrease on every single iteration.</b> If it ever goes up, either α is too
large or the gradient is wrong. There is no third option, and that makes the diagnosis fast.</p>""")

        + h2("💻", "In code")
        + code("""
w, b, J_history = gradient_descent(X, y, w_init, b_init, alpha, num_iters)

plt.plot(J_history)
plt.xlabel('iteration')
plt.ylabel('J(w, b)')
plt.title('learning curve')
""")
        + """<p>Have <code>gradient_descent</code> append <code>compute_cost(...)</code> to a list every
iteration (or every 10, for long runs) and return it. It costs almost nothing and you will look at this
plot more than any other in the course.</p>"""

        + h2("🔬", "The automatic convergence test")
        + """<p>You can automate it: declare convergence when J decreases by less than some small ε — say
0.001 — in a single iteration.</p>
<p>Andrew’s honest note is that choosing ε is genuinely hard. Its right value depends on the scale of J,
which depends on your data. He says he prefers looking at the graph, and that is reasonable advice: the
graph tells you <em>why</em> it stopped, and a threshold only tells you <em>that</em> it did.</p>"""

        + h2("🔤", "The words, decoded")
        + decode([
            ("convergence", "“settling down”", "J has stopped changing meaningfully. Not zero — just flat."),
            ("learning curve", "“learning curve”", "J plotted against iteration number. The one plot you should always make."),
            ("epsilon (ε)", "“epsilon”", "A tiny threshold, e.g. 0.001. Declare convergence when J falls by less than ε in one step."),
            ("iteration", "“iteration”", "One full update of every parameter. In batch gradient descent, one pass over all the data."),
        ])
        + h2("🕳", "Traps")
        + trap("""<p><b>Not recording J at all.</b> Then a failing model is a mystery instead of a
five-second diagnosis. Always keep the history.</p>""")
        + trap("""<p><b>Expecting a fixed number of iterations to work.</b> Different problems need 30,
1,000 or 100,000. There is no universal number — which is exactly why you plot it.</p>""")

        + explain("""<p>Two problems converge in 30 iterations and 100,000 iterations respectively, with the same code.
<b>Say why no universal iteration count exists, and what you should do instead.</b></p>""",
                  """<p>How many steps you need depends on the shape of the cost surface — how elongated the contours
are, which depends on your features and your scaling — and on &alpha;. Those change with every
dataset, so any fixed number is right by accident.</p>
<p>So you plot <var>J</var> against iteration and read the shape: falling and flat means converged,
still falling means keep going or raise &alpha;, rising means lower it. That is why recording the
history is non-negotiable — without it, a failing model is a mystery instead of a five-second
diagnosis.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("J goes 100, 40, 22, 21.8, 21.7, 21.7. What now?",
             "<p>Converged. Running longer gains nothing. If 21.7 is too high, the problem is the model "
             "or the features — not the optimisation.</p>"),
            ("J goes 100, 130, 90, 160, 70, 210. What now?",
             "<p>Oscillating and growing — α is too large. Cut it by a factor of ten.</p>"),
            ("J is flat from the very first iteration. What are the two possibilities?",
             "<p>Either α is so small that nothing moves, or the gradient is computing zero — often "
             "because of a bug or because all the weights are stuck.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("lab", REPO + "/week2/Optional%20Labs/C1_W2_Lab03_Feature_Scaling_and_Learning_Rate_Soln.ipynb",
             "Optional lab: Feature Scaling and Learning Rate",
             "In this repo. Plots several learning curves side by side."),
        ])
    )))

# ============================================================ 7
L.append(dict(
    slug="07-choosing-the-learning-rate", title="Choosing the learning rate", mins=8, tag="core",
    lede="Try a ladder of values, plot each one, keep the largest that still behaves. That is the whole "
         "method, and it is genuinely how people do it.",
    body=(
        pretest("""<p>You must pick α with no formula to tell you the right value. <b>Guess a systematic way to search</b> — better than trying random numbers.</p>""",
        """<p>Watch for the ladder, and for the rule about what J doing anything other than falling tells you immediately.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>There is no formula for α. You try a few and look.</p>
<p>The values people try go up by roughly ×3 each time — 0.001, 0.003, 0.01, 0.03, 0.1 — because α acts
multiplicatively, so equal <em>ratios</em> matter rather than equal differences. Trying 0.1, 0.2, 0.3
wastes all your attempts in one narrow region.</p>""")

        + lenses(
            """<p>Turning a tap to fill a glass. Too gentle and you stand there all day. Too hard and it splashes
everywhere and the glass ends up emptier than when you started.</p>
<p>Nobody computes the right pressure. You turn it, look, and adjust — and that is genuinely the accepted
professional method here.</p>""",
            """<p>This is a step-size choice, and the honest position is that there is <b>no formula</b>.</p>
<p>The recommended procedure is a logarithmic sweep: 0.001, 0.003, 0.01, 0.03, 0.1 — roughly threefold
steps, because you are looking for the right order of magnitude, not the third decimal place.</p>""",
            """<p>Three cost curves on one pair of axes.</p>
<p>One falls smoothly and flattens — good. One falls very slowly and is still falling at the right-hand
edge — α too small. One rises or oscillates — α too large. Learn those three shapes and you can diagnose
any training run at a glance.</p>""",
            """<p>A diverging cost is nearly always the learning rate, and it is the first thing to check before
suspecting anything more interesting.</p>
<p>The useful debugging trick is to set α absurdly small — 0.0001 — and confirm the cost decreases at all.
If it does not, the bug is in the gradient, not the rate, and you have just halved your search
space.</p>""",
            """So the sweep below is the actual professional practice, and the three curve shapes are how you read
it.""")

        + h2("🎬", "Watch it move")
        + demo("alphachoice", "Five values, five learning curves",
               "the largest one that still falls smoothly is the one you want")

        + h2("🔢", "The procedure")
        + """<ol>
<li>Try α = 0.001. Run for a few hundred iterations, plot J.</li>
<li>Multiply by 3: 0.003, 0.01, 0.03, 0.1, 0.3, 1. Plot each.</li>
<li>Find the largest α whose curve <b>decreases smoothly</b>.</li>
<li>Use that, or one notch below it for safety.</li>
</ol>"""
        + key("""<p>You do not need to be precise. There is usually a comfortable range of a factor of ten
that works fine — which is fortunate, because tuning α to three decimal places would be a poor use of an
afternoon.</p>""")

        + h2("🔬", "The bug-versus-α test, once more")
        + """<p>It is worth repeating from Week 1 because this is where you will need it.</p>
<p>Set α to something absurdly small — 0.0001. With a small enough step, J is <em>mathematically
guaranteed</em> to decrease every iteration, provided the gradient is correct.</p>
<ul>
<li>J now decreases → the gradient is right, α was too big.</li>
<li>J still does not decrease → it is not α. Go and look at <code>compute_gradient</code>.</li>
</ul>
<p>One line, and it separates two completely different problems.</p>"""
        + warn("""<p>The best α depends heavily on whether you scaled your features. Scale first, then tune
α — doing it the other way round means redoing the tuning.</p>""")

        + h2("🔤", "The words, decoded")
        + decode([
            ("learning rate (α)", "“alpha”", "How far to step, per unit of gradient. The single most important number you choose by hand."),
            ("hyperparameter", "“hyper-parameter”", "A number you set, not one the model learns. α, λ, the number of layers."),
            ("diverge", "“blow up”", "J grows instead of shrinking, usually to infinity. Always means α is too large — or the derivative is wrong."),
            ("oscillate", "“bounce”", "J goes down, up, down, up. Overshooting the valley. Halve α."),
        ])
        + explain("""<p>&alpha; and &lambda; are both called hyperparameters, and <var>w</var> and <var>b</var> are
not. <b>Say what the distinction actually is.</b></p>""",
                  """<p>Parameters are the numbers the algorithm <em>learns from the data</em> by minimising the cost.
Hyperparameters are the numbers you fix before the learning starts, and gradient descent never
touches them.</p>
<p>Which is why they need a completely different search method — a sweep and a plot rather than a
gradient — and why choosing them well is a manual skill rather than an automatic one. Everything in
C2 Week 3 is, in one way or another, about choosing hyperparameters honestly.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("Why go up by ×3 rather than adding a fixed amount?",
             "<p>Because α acts multiplicatively — the difference between 0.001 and 0.002 is huge, and "
             "between 0.501 and 0.502 is nothing. Equal ratios cover the useful range efficiently.</p>"),
            ("α = 0.01 works and α = 0.03 also works. Which do you pick?",
             "<p><b>0.03</b> — the larger of the two that still converges smoothly. It gets there in "
             "fewer iterations. Some people back off to 0.01 for safety margin; both are defensible.</p>"),
            ("You scaled your features and now your old α diverges. Why?",
             "<p>Because scaling changed the shape of the cost surface. Larger α values are usually safe "
             "<em>after</em> scaling, so this direction is unusual — check the scaler was applied "
             "consistently.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("paper", "https://arxiv.org/abs/1506.01186",
             "Smith (2015) — Cyclical Learning Rates",
             "Introduces the “LR range test”: increase α during one short run and read the best value off the resulting curve. Now standard in deep learning."),
            ("lab", REPO + "/week2/Optional%20Labs/C1_W2_Lab03_Feature_Scaling_and_Learning_Rate_Soln.ipynb",
             "Optional lab: Learning Rate",
             "In this repo. Runs the ladder for you."),
        ])
    )))

# ============================================================ 8
L.append(dict(
    slug="08-feature-engineering", title="Feature engineering", mins=9, tag="core",
    lede="The model can only combine features the way its formula allows. Anything else you want it to "
         "use, you have to hand it directly — and that is where domain knowledge enters.",
    body=(
        pretest("""<p>You have a plot's frontage and its depth. The price really depends on <b>area</b>. <b>Can a linear model work that out for itself?</b> Commit to yes or no.</p>""",
        """<p>Watch for why the answer is no, and for what one extra column fixes. This is the lesson that makes linear models far more powerful than they look.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>You are predicting the price of a plot of land. You have the frontage (how wide it is)
and the depth (how far back it goes).</p>
<p>But what actually matters is the <b>area</b> — width × depth. And your model can only add things
together. It literally cannot multiply two features, no matter how many iterations you run.</p>
<p>So multiply them yourself and hand the result over as a third feature. Now it can use the area.</p>""")

        + lenses(
            """<p>A surveyor given the length and width of a plot, asked what it is worth. He multiplies them
together, because <b>land sells by area</b>.</p>
<p>Nobody handed him the area. He knew something about the trade that the two raw numbers did not say on
their own, and creating that third number is worth more than any amount of adjusting the first two.</p>""",
            """<p>This is domain knowledge entering the model as a new column, and it is consistently the highest-value
activity in applied machine learning on tabular data.</p>
<p>The reason is structural: a linear model cannot represent <var>x</var><sub>1</sub> ×
<var>x</var><sub>2</sub> however long you train it. Handing it the product changes what is
<em>representable</em>, not merely what is learned.</p>""",
            """<p>A new column appearing in the spreadsheet, computed from two existing ones.</p>
<p><code>area = frontage * depth</code>. One column, added by a person who knows what the rows mean. That
is feature engineering entirely.</p>""",
            """<p>Before deep learning, this was most of the job — teams of people inventing columns. It remains most
of the job for tabular data, which is nearly all business data.</p>
<p>Deep learning's claim is that networks learn features themselves, and that is broadly true for images,
audio and text and much less true for spreadsheets. Knowing which regime you are in tells you where to
spend your week.</p>""",
            """So the new column below carries something no amount of training could have recovered from the old
ones.""")

        + h2("🎬", "Watch it move")
        + demo("featureeng", "Two features becoming three",
               "the model could never have found area on its own")

        + h2("🔢", "What it is")
        + eqp([
            '<var>x</var><sub>3</sub> <span class="op">=</span> <var>x</var><sub>1</sub> <span class="op">×</span> <var>x</var><sub>2</sub> &nbsp;&nbsp;→&nbsp;&nbsp; ',
            ('<var>f</var>(<var>x</var>)', "func-f", "apply the model to x"),
            ' <span class="op">=</span> <var>w</var><sub>1</sub><var>x</var><sub>1</sub> <span class="op">+</span> <var>w</var><sub>2</sub><var>x</var><sub>2</sub> <span class="op">+</span> <var class="hl-a"><var>w</var><sub>3</sub><var>x</var><sub>3</sub></var> <span class="op">+</span> <var>b</var>',
        ], "invent a feature, then let the model weigh it — hover or click it", small=True)
        + decode([
            ("feature engineering", "“inventing better inputs”", "Using knowledge of the problem to construct features that make the pattern easy to express."),
            ("interaction term", "“a product of two features”", "x₁ × x₂. Captures “these two matter together”, which a sum cannot."),
            ("domain knowledge", "“knowing the subject”", "Knowing that area matters for land is not a machine learning skill. It is why ML teams need people who understand the problem."),
        ])
        + key("""<p>A linear model can only <b>add up weighted features</b>. If the real pattern involves a
product, a ratio, a threshold or a curve, you must build that structure into the features yourself —
otherwise it is simply unavailable to the model.</p>""")

        + h2("🔬", "Features worth trying")
        + grid3(
            card("<h3>Products</h3><p>width × depth = area. price × quantity = revenue. Captures “these "
                 "matter together”.</p>"),
            card("<h3>Ratios</h3><p>price per square foot. CPU per network packet. Often far more "
                 "informative than either number alone.</p>"),
            card("<h3>Transforms</h3><p>log(income), √(area), age². Change the <em>shape</em> of the "
                 "relationship the model can express.</p>"))
        + note("""<p>Feature engineering was the single biggest lever in classical machine learning — most
of a data scientist’s week went into it. Neural networks reduce the need for it substantially, because
hidden layers learn their own intermediate features (Course 2, Week 1). They do not remove it: on tabular
data, well-engineered features still routinely beat a deeper network.</p>""",
               "How much this still matters")

        + h2("🕳", "Traps")
        + trap("""<p><b>Creating features that leak the answer.</b> If you are predicting whether a
customer churns and you engineer “days since they cancelled”, your model will be perfect on paper and
useless in production. Ask whether the feature would exist at prediction time.</p>""")
        + trap("""<p><b>Forgetting to scale engineered features.</b> If x₁ is 0–2000 then x₁² is
0–4,000,000. Rescale after engineering, not before.</p>""")

        + explain("""<p>You are predicting customer churn and engineer a feature called <i>days since they cancelled</i>.
It gives a near-perfect model. <b>Say what has gone wrong.</b></p>""",
                  """<p>The feature <b>cannot exist at prediction time</b>. You are trying to predict whether someone
will cancel, and the feature already knows that they did — so the model has been handed the answer
in the input.</p>
<p>This is data leakage, and its signature is exactly this: implausibly good validation numbers and
a useless model in production. The test to apply to every engineered feature is one question — would
this value be available, with this meaning, at the moment I need the prediction?</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("Predicting fuel cost from distance and fuel price. What feature would you engineer?",
             "<p>distance × price. The cost is fundamentally a product, and a model that can only add "
             "them cannot express it.</p>"),
            ("Why can't the model learn to multiply x₁ by x₂ on its own?",
             "<p>Because its formula is w₁x₁ + w₂x₂ + b. There is no arrangement of w₁ and w₂ that "
             "produces a product. It is outside what the model can represent.</p>"),
            ("You engineer “average purchase value” for churn prediction. What must you check?",
             "<p>That it is computed only from data available <em>before</em> the prediction point. "
             "Including post-churn behaviour is leakage.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("lab", REPO + "/week2/Optional%20Labs/C1_W2_Lab04_FeatEng_PolyReg_Soln.ipynb",
             "Optional lab: Feature Engineering and Polynomial Regression",
             "In this repo. Shows the fit before and after adding engineered features."),
            ("book", "http://www.feat.engineering/",
             "Kuhn & Johnson — Feature Engineering and Selection",
             "Free online. The standard practical reference, if this becomes your day job."),
        ])
    )))

# ============================================================ 9
L.append(dict(
    slug="09-polynomial-regression", title="Polynomial regression", mins=14, tag="core",
    lede="Feature engineering’s most useful special case: hand the model x², x³ or √x and a straight-line "
         "algorithm starts drawing curves.",
    body=(
        pretest("""<p>Your data curves. Your model draws straight lines. <b>Guess how you could fit a curve without abandoning linear regression.</b></p>""",
        """<p>Watch for what stays linear even when the curve does not. The trick is in what you feed it, not what it is.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Your data curves, and a straight line cannot follow a curve. So bend the line.</p>
<p>Except you do not bend the line — you cannot, the model only adds things up. Instead you hand it
<b>x squared</b> as an extra feature. Now “add up weighted features” includes an x² term, and the result
is a curve.</p>
<p>Same algorithm. Different ingredients.</p>""")

        + lenses(
            """<p>Bending a flexible ruler to follow a curved line instead of laying a straight one against it.</p>
<p>The ruler is still a ruler and you are still fitting it, but it can now follow a shape a straight edge
never could. Bend it too eagerly and it follows every wobble, including the ones that were mistakes in
the drawing.</p>""",
            """<p>The point that surprises people: adding <var>x</var>², <var>x</var>³ as columns keeps the model
<b>linear in the parameters</b>, which is what “linear regression” actually means.</p>
<p>Everything you know still applies — same cost, same gradient descent, same guarantees. The curve is in
the features, not in the model.</p>""",
            """<p>A spreadsheet with three columns computed from one: <var>x</var>, <var>x</var>², <var>x</var>³.</p>
<p>Feed those to the same linear regression and you get a cubic fit. Nothing about the algorithm knows or
cares that the columns are related.</p>""",
            """<p>Feature scaling becomes urgent rather than helpful here, and it is worth seeing the numbers: if
<var>x</var> runs to 1,000 then <var>x</var>³ runs to 1,000,000,000.</p>
<p>Those columns are nine orders of magnitude apart, the contours become extraordinarily elongated, and
gradient descent will not converge in any reasonable time without scaling.</p>""",
            """So the powers below are new columns, and the model fitting them is exactly the one you already
have.""")

        + h2("🎬", "Watch it move")
        + demo("polyreg", "Four models on the same curved data",
               "click through: straight line, quadratic, cubic, square root")

        + h2("🔢", "The options")
        + table(["Model", "Features you supply", "Shape it can make"],
                [["f = w₁x + b", "x", "a straight line"],
                 ["f = w₁x + w₂x² + b", "x, x²", "a parabola — which eventually turns back down"],
                 ["f = w₁x + w₂x² + w₃x³ + b", "x, x², x³", "an S-curve that keeps rising"],
                 ["f = w₁√x + b", "√x", "rises fast, then flattens"]])
        + """<p>For house prices, the parabola is a poor choice despite fitting well in the middle: it
predicts that beyond some size, bigger houses get <em>cheaper</em>. The square root is often the most
natural shape here — prices rise with size but with diminishing returns.</p>"""
        + key("""<p>It is <b>still linear regression</b>. “Linear” refers to being linear in the
<em>parameters</em> w, not in x. You have not changed the algorithm at all — only what you feed it.</p>""")

        + h2("⚠️", "Scaling becomes essential")
        + warn("""<p>If x ranges from 1 to 1000, then x² ranges to 1,000,000 and x³ to 1,000,000,000. Those
three features are on wildly different scales, and gradient descent will be hopeless without rescaling.
<b>Polynomial features make feature scaling mandatory rather than merely helpful.</b></p>""")

        + h2("💻", "In code")
        + code("""
X = np.c_[x, x**2, x**3]          # three columns instead of one

mu, sigma = X.mean(axis=0), X.std(axis=0)
X = (X - mu) / sigma              # now essential, not optional

w, b, _ = gradient_descent(X, y, ...)
""")
        + """<p>scikit-learn does the first line for you with
<code>PolynomialFeatures(degree=3)</code>, which also generates the interaction terms (x₁x₂ and so on) when
you have several features.</p>"""

        + h2("🤔", "Which degree, though?")
        + """<p>This lesson gives you the mechanism and deliberately not the answer. Choosing the degree is
a real decision with a real trade-off: too low and the model cannot follow the pattern, too high and it
starts fitting the noise.</p>
<p>You will meet the honest way to choose in <b>Week 3</b> (overfitting, and what to do about it) and the
rigorous way in <b>Course 2 Week 3</b> (a cross-validation set, and the bias/variance diagnostic). For
now: try a few, and look at the fit.</p>"""

        + h2("🧮", "Why scaling stops being optional")
        + """<p>Polynomial regression is ordinary linear regression on engineered features — you add
<var>x</var>², <var>x</var>³ and let the same algorithm fit them. But look at what that does to the
ranges. For a size feature running to about 3,000:</p>"""
        + table(["feature", "typical magnitude"],
                [["<var>x</var>", "10³"],
                 ["<var>x</var>²", "10⁷"],
                 ["<var>x</var>³", "<b>10¹⁰</b>"]])
        + """<p>Ten orders of magnitude between the first feature and the third. From the previous
lesson, the largest usable α is set by the steepest direction — so <var>x</var>³ would force α down
to something around 10⁻²⁰, at which point <var>x</var> would never move at all.</p>
<p>So: with polynomial features, <b>scaling is not an optimisation, it is a precondition</b>. Without
it gradient descent does not converge slowly, it does not converge.</p>
<p>Which degree to pick is a question this course cannot yet answer honestly — the fit always
improves on the training data as the degree rises. Course 2 Week 3 answers it with a
cross-validation set.</p>"""
        + explain("""<p>Adding <var>x</var>² and <var>x</var>³ lets the model draw curves, yet it is
still called <em>linear</em> regression. <b>Linear in what?</b></p>""",
                  """<p>In the <em>parameters</em>, not in <var>x</var>. The model is
<var>w</var><sub>1</sub><var>x</var> + <var>w</var><sub>2</sub><var>x</var>² +
<var>w</var><sub>3</sub><var>x</var>³ + <var>b</var> — every <var>w</var> appears to the first power
and is multiplied by something known. That is the property the maths actually depends on: it makes
the cost a bowl with one minimum, and the derivatives stay the same simple form. Once you accept
that, <var>x</var>² is just another column of numbers and nothing in the algorithm needs to change —
which is exactly the trick.</p>""")

        + h2("🔤", "The words, decoded")
        + decode([
            ("polynomial", "“polynomial”", "A sum of powers: x, x², x³. Degree = the highest power."),
            ("feature engineering", "“feature engineering”", "Creating new input columns from the ones you have, using what you know about the problem."),
            ("linear in the parameters", "“linear in w”", "Every w appears to the first power. That — not the shape of the curve — is what makes it linear regression."),
            ("degree", "“degree”", "The highest power used. Higher degree = more flexible = easier to overfit."),
        ])
        + h2("✅", "Check yourself")
        + quiz([
            ("Why is polynomial regression still called linear regression?",
             "<p>Because it is linear in the <b>parameters</b>. f = w₁x + w₂x² + b is a weighted sum of "
             "features; that the features happen to be powers of x changes nothing about the algorithm.</p>"),
            ("Why is a parabola a poor model for house prices?",
             "<p>Because it turns downwards eventually, predicting that very large houses are cheap. "
             "The shape must make sense beyond your data, not just inside it.</p>"),
            ("x ranges 1–1000. What is the range of x³, and what does that imply?",
             "<p>1 to 1,000,000,000. Feature scaling is now mandatory — gradient descent will not "
             "converge otherwise.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("lab", REPO + "/week2/Optional%20Labs/C1_W2_Lab04_FeatEng_PolyReg_Soln.ipynb",
             "Optional lab: Polynomial Regression",
             "In this repo. Fits several degrees and plots them together."),
            ("docs", "https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.PolynomialFeatures.html",
             "sklearn.preprocessing.PolynomialFeatures",
             "Generates powers and interaction terms automatically. Note how fast the column count grows with degree."),
            ("docs", "https://scikit-learn.org/stable/auto_examples/model_selection/plot_underfitting_overfitting.html",
             "scikit-learn — underfitting vs overfitting",
             "The same polynomial-degree question, with the answer Week 3 is about to give you."),
        ])
    )))

WEEK = dict(
    course="C1", week=2, title="Regression with Multiple Variables",
    time="~6–7 h with labs",
    goal="Scale linear regression to many features, make it fast with vectorisation, and make gradient "
         "descent behave with feature scaling and a well-chosen learning rate.",
    lessons=L,
)
