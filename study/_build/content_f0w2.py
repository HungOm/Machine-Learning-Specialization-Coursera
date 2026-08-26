# -*- coding: utf-8 -*-
"""Foundations · Week 2 — Python, NumPy and pandas."""
from kit import (kid, key, warn, trap, note, card, eq, decode, table, demo,
                 quiz, links, code, h2, grid2, grid3)

L = []

def lesson(slug, title, mins, lede, body):
    L.append(dict(slug=slug, title=title, mins=mins, tag="foundations", lede=lede, body=body))


# ============================================================ 1
lesson("01-jupyter", "Jupyter notebooks", 6,
    "Every lab in this specialization is a notebook. Five minutes here and they stop being intimidating.",
    h2("🎈", "The idea, in plain words")
    + kid("""<p>A notebook is a stack of little boxes called <b>cells</b>. You type code in a box, press a
key, and the answer appears underneath it.</p>
<p>Each box remembers what the boxes before it did. So you build things up gradually instead of writing a
whole program at once.</p>""")

    + h2("🔤", "The vocabulary")
    + decode([
        ("cell", "“cell”", "one box. Either code, or text (called markdown)."),
        ("<b>Shift + Enter</b>", "—", "run this cell and move to the next. <b>95% of using Jupyter.</b>"),
        ("In [3]", "“in three”", "this was the <b>3rd cell you ran</b> — not the 3rd on the page."),
        ("In [*]", "“in star”", "still running. If it stays like this, something is stuck."),
        ("Out[3]", "“out three”", "what that cell produced."),
        ("kernel", "“KER-nel”", "the Python process doing the work. Restarting it forgets everything."),
    ], head=("Thing", "Say it", "What it means"))

    + h2("🎬", "Watch it move")
    + demo("fjupyter", "Cells running one after another",
           "note that only the LAST line of a cell prints automatically")

    + h2("💻", "The four things you will actually do")
    + code("""
# 1. run a cell:            Shift + Enter
# 2. see a value:           put it on the last line, or use print()
x = 5
x + 3                       # shows 8

# 3. see several values:    print() each one
print(x)
print(x * 2)

# 4. import a library:      once, at the top
import numpy as np
import pandas as pd
""")

    + h2("🔬", "What is actually happening")
    + """<p>The number in <code>In [3]</code> is the order you <b>ran</b> things, not their position on the
page. That has one important consequence: if you run cell 5, then go back and change cell 2, the notebook
still holds the results from the <em>old</em> cell 2. Everything below can now be quietly wrong.</p>
<p>This is the single most common source of “but it worked a minute ago” in notebooks. The cure is
<b>Kernel → Restart &amp; Run All</b>, which throws away everything and runs the page top to bottom in
order. Do that before you trust any result.</p>"""
    + note("""<p>Two shortcuts worth having: <b>Esc</b> then <b>A</b> inserts a cell above, <b>Esc</b> then
<b>B</b> below. And <code>shift + tab</code> with your cursor inside a function's brackets pops up its
documentation — genuinely useful when you cannot remember an argument.</p>""", "Worth knowing")

    + h2("🕳", "Traps")
    + trap("""<p><b>Running cells out of order.</b> The notebook does not care, and your results will be
built on stale values. Restart &amp; Run All before believing anything.</p>""")
    + trap("""<p><b>Forgetting to run the import cell.</b> Then everything below fails with
<code>NameError: name 'np' is not defined</code>. It is almost always this.</p>""")

    + h2("✅", "Check yourself")
    + quiz([
        ("A cell shows In [*] and nothing happens. What does that mean?",
         "<p>It is still <b>running</b>. Either it is slow, or it is stuck — perhaps waiting for input, "
         "or in an infinite loop. Interrupt the kernel (the ■ button) to stop it.</p>"),
        ("You changed a cell near the top. What should you do?",
         "<p><b>Restart &amp; Run All.</b> Otherwise everything below is still using the old value.</p>"),
        ("Why does x + 3 print something but x = 5 not?",
         "<p>Jupyter shows the value of the last <b>expression</b> in a cell. <code>x = 5</code> is an "
         "assignment, which has no value to show. Use <code>print()</code> if you want it anyway.</p>"),
    ])

    + h2("🔗", "Go deeper")
    + links([
        ("docs", "https://jupyter-notebook.readthedocs.io/en/stable/notebook.html",
         "Jupyter — the official notebook guide", "Skim it once; the keyboard shortcut list is the useful part."),
        ("lab", "../../C1%20-%20Supervised%20Machine%20Learning%20-%20Regression%20and%20Classification/week1/Optional%20Labs/C1_W1_Lab01_Python_Jupyter_Soln.ipynb",
         "Optional lab: Python and Jupyter",
         "In this repo. The course's own ten-minute tour — a good first thing to actually run."),
    ]))

# ============================================================ 2
lesson("02-types", "Values and types", 6,
    "Six kinds of thing, and why mixing two of them up produces an error message that looks nothing like "
    "the actual problem.",
    h2("🎈", "The idea, in plain words")
    + kid("""<p>Every value in Python is a <b>kind</b> of thing, and the kind decides what you can do
with it.</p>
<p>The number 5 and the text "5" look identical on screen. Add 5 + 5 and you get 10. Add "5" + "5" and you
get "55" — because gluing text together is what + means for text.</p>""")

    + h2("🔤", "The six you will meet")
    + decode([
        ("<code>5</code>", "“int”", "a whole number."),
        ("<code>5.0</code>", "“float”", "a decimal. <b>What machine learning uses everywhere</b> — note the .0"),
        ("<code>\"cat\"</code>", "“string” / “str”", "text, in quotes. Single or double, they are the same."),
        ("<code>True</code>", "“bool”", "yes or no. <b>Capital T</b>, capital F — Python is fussy."),
        ("<code>[1, 2, 3]</code>", "“list”", "several things in order, in square brackets."),
        ("<code>None</code>", "“None”", "deliberately nothing. Not zero, not empty text — nothing."),
    ], head=("Value", "Type", "What it is"))

    + h2("🎬", "Watch it move")
    + demo("ftypes", "The six types",
           "the type is what decides how an operator behaves")

    + h2("💻", "In code")
    + code("""
type(5)         # <class 'int'>
type(5.0)       # <class 'float'>
type("5")       # <class 'str'>
type([1,2,3])   # <class 'list'>

5 + 5           # 10
"5" + "5"       # '55'      <- + means "glue" for text
5 + "5"         # TypeError: unsupported operand type(s)

int("5")        # 5     convert text to a number
float(5)        # 5.0   convert int to float
str(5)          # '5'   convert number to text
""")

    + h2("🔬", "What is actually happening")
    + """<p>Python is <b>dynamically typed</b>: a variable does not have a type, the <em>value</em> does,
and a variable can point at different types at different moments. That flexibility is why Python is
pleasant to learn and why type errors show up at run time rather than being caught in advance.</p>
<p>For this specialization, one type matters more than the rest: <b>float</b>. Neural network weights,
gradients and probabilities are all floats. You will see <code>float32</code> and <code>float64</code> —
these are how many digits of precision the computer keeps, and that limit is exactly the reason Course 2,
Week 2 has a whole lesson on numerical stability.</p>"""

    + h2("🕳", "Traps")
    + trap("""<p><b>Numbers read from a file arrive as text.</b> A CSV column looks numeric and comes in as
strings, so sums silently concatenate. <code>df.dtypes</code> tells you what you actually have.</p>""")
    + trap("""<p><b><code>true</code> instead of <code>True</code>.</b> Python needs the capital. Lowercase
gives <code>NameError</code>.</p>""")

    + h2("✅", "Check yourself")
    + quiz([
        ("What does \"3\" + \"4\" give?",
         "<p><b>'34'</b> — text glued together, not 7. Use <code>int()</code> first if you wanted "
         "arithmetic.</p>"),
        ("Why is 5.0 different from 5?",
         "<p>5 is an <b>int</b>, 5.0 is a <b>float</b>. They compare as equal, but they are stored "
         "differently — and ML libraries want floats.</p>"),
        ("Your sums are producing nonsense on data from a CSV. What is the first thing to check?",
         "<p><code>df.dtypes</code> — a column you assume is numeric is probably <code>object</code>, "
         "meaning text.</p>"),
    ])

    + h2("🔗", "Go deeper")
    + links([
        ("docs", "https://docs.python.org/3/tutorial/introduction.html",
         "The official Python tutorial", "Sections 3.1 and 3.2 cover numbers and strings properly."),
    ]))

# ============================================================ 3
lesson("03-lists-vs-arrays", "Lists vs NumPy arrays", 8,
    "They look identical and behave nothing alike. This one distinction causes more beginner confusion "
    "than anything else in scientific Python.",
    h2("🎈", "The idea, in plain words")
    + kid("""<p>A <b>list</b> is a general container. It can hold anything — numbers, text, other lists.
Because it might hold text, <code>+</code> means “join these together”.</p>
<p>A NumPy <b>array</b> is a maths object. Everything in it is the same kind of number, so <code>+</code>
can safely mean “add the numbers”.</p>
<p>Same square brackets on screen. Completely different behaviour, and no warning.</p>""")

    + h2("🧮", "The three that catch everyone")
    + table(["You write", "A list gives", "An array gives"],
            [["<code>x * 2</code>", "<code>[1,2,3,1,2,3]</code> — repeats it", "<code>[2,4,6]</code> — doubles each"],
             ["<code>x + 10</code>", "<b>TypeError</b>", "<code>[11,12,13]</code> — adds to each"],
             ["<code>x + y</code>", "<code>[1,2,3,4,5,6]</code> — glued", "<code>[5,7,9]</code> — added pairwise"]])

    + h2("🎬", "Watch it move")
    + demo("flistarray", "The same operation, both ways",
           "click through — the list column is almost never what you wanted")

    + h2("💻", "In NumPy")
    + code("""
import numpy as np

my_list = [1, 2, 3]
arr = np.array(my_list)      # convert -- this is the fix

my_list * 2      # [1, 2, 3, 1, 2, 3]
arr * 2          # array([2, 4, 6])

# always convert before doing maths:
X = np.array(rows_from_a_file)

# things arrays can do that lists cannot:
arr.mean()       # 2.0
arr.shape        # (3,)
arr[arr > 1]     # array([2, 3])
""")

    + h2("🔬", "What is actually happening")
    + """<p>The difference is in memory. A Python list holds <b>pointers</b> to objects scattered around
memory, and each object carries its own type information. NumPy stores the raw numbers in one solid block,
all the same type.</p>
<p>That is why arrays are fast: the numbers sit next to each other, so the processor can load and multiply
several at once. A list forces the interpreter to chase a pointer, check a type, and unbox a value — for
every single element.</p>
<p>It is also why an array cannot mix types. <code>np.array([1, "cat"])</code> silently converts everything
to text, which is a genuinely nasty surprise. The rigidity is the price of the speed.</p>"""
    + key("""<p><b>For any maths, convert to an array first.</b> <code>np.array(my_list)</code>. One line,
and the whole category of confusion goes away.</p>""")

    + h2("🕳", "Traps")
    + trap("""<p><b><code>my_list * 2</code> silently doing the wrong thing.</b> No error. You just get six
elements where you expected three doubled ones.</p>""")
    + trap("""<p><b>Appending to an array in a loop.</b> Arrays are fixed-size; <code>np.append</code>
copies the whole thing each time, which is very slow. Build a list, then convert once at the end.</p>""")

    + h2("✅", "Check yourself")
    + quiz([
        ("x = [1,2,3]. What does x * 3 give?",
         "<p><code>[1,2,3,1,2,3,1,2,3]</code> — nine elements. For <code>[3,6,9]</code> you need "
         "<code>np.array(x) * 3</code>.</p>"),
        ("Why can't a NumPy array mix numbers and text?",
         "<p>Because it stores raw values of one fixed type in a solid block — that layout is where the "
         "speed comes from. Mixing forces everything to become text.</p>"),
        ("You need to collect results in a loop. List or array?",
         "<p>Build a <b>list</b> (appending is cheap), then <code>np.array(results)</code> once at the "
         "end. Appending to an array copies it every time.</p>"),
    ])

    + h2("🔗", "Go deeper")
    + links([
        ("docs", "https://numpy.org/doc/stable/user/absolute_beginners.html",
         "NumPy — the absolute beginner's guide",
         "If NumPy is new, read this once. It pays for itself within a week."),
        ("lab", "../../C1%20-%20Supervised%20Machine%20Learning%20-%20Regression%20and%20Classification/week2/Optional%20Labs/C1_W2_Lab01_Python_Numpy_Vectorization_Soln.ipynb",
         "Optional lab: Python, NumPy and Vectorization",
         "In this repo. The most useful optional lab in Course 1."),
    ]))

# ============================================================ 4
lesson("04-indexing-slicing", "Indexing and slicing", 9,
    "How to grab one thing, or a run of things. The colon, and the off-by-one rule that catches "
    "absolutely everybody.",
    h2("🎈", "The idea, in plain words")
    + kid("""<p>Numbers in an array have addresses, and <b>the first one lives at 0</b>, not 1. That feels
wrong for about a week and then becomes invisible.</p>
<p>Square brackets are how you ask for an address. <code>x[0]</code> is the first, <code>x[2]</code> is the
third, and <code>x[-1]</code> is the last — counting backwards.</p>""")

    + h2("🔤", "The syntax")
    + decode([
        ("<code>x[0]</code>", "“x sub zero”", "the <b>first</b> element."),
        ("<code>x[-1]</code>", "“x minus one”", "the <b>last</b>. Negative counts back from the end."),
        ("<code>x[1:4]</code>", "“x, one to four”", "positions 1, 2, 3. <b>Stops BEFORE 4.</b>"),
        ("<code>x[:3]</code>", "“x, up to three”", "from the start. Same as x[0:3]."),
        ("<code>x[3:]</code>", "“x, from three”", "to the end."),
        ("<code>x[:]</code>", "“x, everything”", "the whole thing. The bare colon means “all”."),
        ("<code>M[:, 2]</code>", "“all rows, column two”", "for 2-D. This is the one you meet in Course 2."),
    ], head=("Written", "Say it", "What you get"))
    + key("""<p><b>x[1:4] gives you 1, 2, 3 — it stops before 4.</b> Everybody gets this wrong once. The
upside: the count you get is simply (end − start), which is often exactly what you want.</p>""")

    + h2("🎬", "Watch it move")
    + demo("fslice", "Click each form and watch what lights up",
           "the two rows of small numbers are the forward and backward addresses")

    + h2("💻", "In NumPy")
    + code("""
import numpy as np
x = np.array([10, 20, 30, 40, 50, 60])

x[0]       # 10        first
x[-1]      # 60        last
x[1:4]     # [20 30 40]     stops before index 4
x[:3]      # [10 20 30]
x[3:]      # [40 50 60]
x[::2]     # [10 30 50]     every second one

M = np.array([[1, 2, 3],
              [4, 5, 6]])
M[0, 1]    # 2         row 0, column 1
M[1]       # [4 5 6]   a whole row
M[:, 1]    # [2 5]     a whole COLUMN  <- the Course 2 one
""")

    + h2("🔬", "What is actually happening")
    + """<p><code>M[:, j]</code> is worth pausing on, because it appears constantly in Course 2. Read the
comma as separating the dimensions: <b>rows first, then columns</b>. The colon means “everything in this
one”. So <code>M[:, 1]</code> is “every row, column 1” — a whole column.</p>
<p>In Course 2 you will write <code>W[:, j]</code> to grab neuron j's weights, because a dense layer stores
one neuron per <em>column</em>. Knowing this notation is the difference between that line being obvious and
being magic.</p>
<p>One efficiency note: a basic slice is a <b>view</b>, not a copy — it points at the same memory. So
changing a slice changes the original. If you need an independent copy, say <code>x[1:4].copy()</code>.</p>"""

    + h2("🕳", "Traps")
    + trap("""<p><b>Expecting x[1:4] to include position 4.</b> It does not. Four positions would be
x[1:5].</p>""")
    + trap("""<p><b>Confusing M[0] with M[:, 0].</b> The first is a <em>row</em>; the second is a
<em>column</em>. On a square matrix both work and give different answers.</p>""")
    + trap("""<p><b>Modifying a slice and being surprised the original changed.</b> Slices are views. Use
<code>.copy()</code> when you need independence.</p>""")

    + h2("✅", "Check yourself")
    + quiz([
        ("x = [10,20,30,40,50]. What is x[1:3]?",
         "<p><code>[20, 30]</code> — positions 1 and 2. It stops before 3.</p>"),
        ("How do you get the last element without knowing the length?",
         "<p><code>x[-1]</code>. And <code>x[-2]</code> is second to last.</p>"),
        ("M is (400, 25). What does M[:, 7] give, and what shape?",
         "<p>Column 7 — all 400 rows of it. Shape <b>(400,)</b>. In Course 2 that is neuron 7's weights.</p>"),
    ])

    + h2("🔗", "Go deeper")
    + links([
        ("docs", "https://numpy.org/doc/stable/user/basics.indexing.html",
         "NumPy — indexing on ndarrays",
         "The complete rules. Ten minutes here saves hours later."),
    ]))

# ============================================================ 5
lesson("05-shape-and-axis", "Shape and axis", 9,
    "Most NumPy confusion is shape confusion. And `axis` has one rule that makes it click permanently.",
    h2("🎈", "The idea, in plain words")
    + kid("""<p><b>Shape</b> says how the numbers are arranged: (3, 4) means 3 rows and 4 columns.</p>
<p><b>Axis</b> says which direction to work in. Axis 0 goes <b>down</b> the rows; axis 1 goes
<b>across</b> the columns.</p>
<p>The rule that makes it stick: <b>the axis you name is the one that disappears.</b></p>""")

    + h2("🔤", "The syntax")
    + decode([
        ("<code>M.shape</code>", "“shape”", "a tuple: (rows, columns). Rows always first."),
        ("<code>M.shape[0]</code>", "—", "the number of rows. Often <b>m</b>, your examples."),
        ("<code>M.shape[1]</code>", "—", "the number of columns. Often <b>n</b>, your features."),
        ("<code>M.ndim</code>", "“n dim”", "how many dimensions. 1 for a vector, 2 for a matrix."),
        ("<code>axis=0</code>", "“axis zero”", "work <b>down the rows</b> → one answer per column."),
        ("<code>axis=1</code>", "“axis one”", "work <b>across the columns</b> → one answer per row."),
        ("<code>(3,)</code>", "“shape three comma”", "1-D, three entries. The comma is not a typo."),
    ], head=("Written", "Say it", "What it means"))

    + h2("🧮", "Worked by hand")
    + """<p>M = [[1,2,3,4], [5,6,7,8], [9,10,11,12]], shape (3, 4).</p>
<ul>
<li><code>M.sum(axis=0)</code> → [15, 18, 21, 24]. Four answers — one per column. The <b>rows</b>
collapsed. Shape (3,4) became (4,).</li>
<li><code>M.sum(axis=1)</code> → [10, 26, 42]. Three answers — one per row. The <b>columns</b> collapsed.
Shape (3,4) became (3,).</li>
<li><code>M.sum()</code> → 78. Everything collapsed to one number.</li>
</ul>"""

    + h2("🎬", "Watch it move")
    + demo("fshape", "The two axes, and which one vanishes",
           "watch the output shape in each case")

    + h2("💻", "In NumPy")
    + code("""
import numpy as np
M = np.arange(1, 13).reshape(3, 4)

M.shape            # (3, 4)
M.sum(axis=0)      # array([15, 18, 21, 24])   shape (4,)
M.sum(axis=1)      # array([10, 26, 42])       shape (3,)
M.sum()            # 78

# the ML pattern -- one statistic per FEATURE, so axis=0:
X.mean(axis=0)     # the mean of each column
X.std(axis=0)      # the spread of each column

# one prediction per EXAMPLE, so axis=1:
np.argmax(probs, axis=1)    # which class won, per row
""")

    + h2("🔬", "What is actually happening")
    + """<p>“The named axis disappears” is not a mnemonic — it is literally what happens to the shape.
(3, 4) with <code>axis=0</code> gives (4,): position 0 of the shape tuple is gone. With
<code>axis=1</code> you get (3,): position 1 is gone.</p>
<p>Once you see it that way, <code>axis</code> stops needing to be memorised. Ask “which number in the
shape do I want to get rid of?” and that is your axis.</p>
<p>The one that catches people is that <b>axis=0 gives per-column answers</b>, which feels backwards until
you think of it as “collapse downwards, squashing all the rows into one”.</p>"""
    + key("""<p><b>Print <code>.shape</code> constantly while learning.</b> It costs one line and it
answers most of the questions you will actually have. When something behaves strangely, print the shape of
every array involved — the wrong one is usually obvious immediately.</p>""")

    + h2("🕳", "Traps")
    + trap("""<p><b>(3,) is not (3, 1).</b> The first is a flat list of three; the second is a column
matrix. NumPy broadcasts them differently and TensorFlow cares. <code>reshape(-1, 1)</code> converts.</p>""")
    + trap("""<p><b>Guessing the axis.</b> Do not — work it out from which shape number you want gone. It
takes two seconds and is always right.</p>""")

    + h2("✅", "Check yourself")
    + quiz([
        ("X is (1000, 4). What shape is X.mean(axis=0), and what does it mean?",
         "<p><b>(4,)</b> — the mean of each of the 4 features, across all 1000 examples. The rows "
         "collapsed.</p>"),
        ("You want the total for each example. Which axis?",
         "<p><b>axis=1</b> — collapse across the columns, leaving one number per row.</p>"),
        ("What is the difference between shape (5,) and (5, 1)?",
         "<p>(5,) is 1-D — a flat list. (5,1) is 2-D — five rows, one column. They look the same when "
         "printed and behave differently.</p>"),
    ])

    + h2("🔗", "Go deeper")
    + links([
        ("docs", "https://numpy.org/doc/stable/user/basics.broadcasting.html",
         "NumPy — broadcasting", "The next lesson, and the other half of shape understanding."),
    ]))

# ============================================================ 6
lesson("06-creating-arrays", "Creating arrays", 7,
    "Six ways to conjure numbers out of nothing, and the two whose end-points differ in a way nobody "
    "ever remembers.",
    h2("🎈", "The idea, in plain words")
    + kid("""<p>Sometimes you need an array before you have any data — an empty box to fill in, or a row of
evenly spaced numbers to draw a graph with.</p>""")

    + h2("🔤", "The six")
    + table(["Call", "Gives", "Used for"],
            [["<code>np.zeros(5)</code>", "[0, 0, 0, 0, 0]", "an empty box to fill in a loop"],
             ["<code>np.ones(5)</code>", "[1, 1, 1, 1, 1]", "a bias column, or a starting point"],
             ["<code>np.arange(5)</code>", "[0, 1, 2, 3, 4]", "counting. <b>Stops before 5</b>"],
             ["<code>np.linspace(0, 1, 5)</code>", "[0, 0.25, 0.5, 0.75, 1]", "graph x-values. <b>Includes both ends</b>"],
             ["<code>np.zeros((2, 3))</code>", "a 2×3 grid of zeros", "note the <b>double brackets</b>"],
             ["<code>np.random.rand(3)</code>", "3 random numbers in 0…1", "initialising weights"]])

    + h2("🎬", "Watch it move")
    + demo("fcreate", "Click each one and see what comes out",
           "watch the shape line underneath")

    + h2("💻", "In NumPy")
    + code("""
import numpy as np

np.zeros(5)             # array([0., 0., 0., 0., 0.])
np.zeros((2, 3))        # a 2x3 grid -- the shape is ONE argument, hence ((  ))
np.arange(2, 10, 2)     # array([2, 4, 6, 8])   start, stop, step
np.linspace(0, 1, 5)    # array([0., 0.25, 0.5, 0.75, 1.])
np.full((2, 2), 7)      # every entry 7
np.eye(3)               # identity matrix: 1s on the diagonal

np.random.seed(1)       # <- makes "random" repeatable
np.random.rand(3)       # same three numbers every run now
""")
    + warn("""<p><code>np.zeros(2, 3)</code> is an error — it reads 3 as a different argument. The shape
must be a single tuple: <code>np.zeros((2, 3))</code>. Those double brackets look like a typo and are
required.</p>""")

    + h2("🔬", "What is actually happening")
    + """<p><b>arange vs linspace</b> is worth getting straight because they answer different questions.
<code>arange</code> takes a <em>step size</em> and stops before the end. <code>linspace</code> takes a
<em>count</em> and includes both ends. For plotting you almost always want linspace, because you asked for
200 points and you want exactly 200.</p>
<p><b>Why <code>np.random.seed</code> matters more than it looks.</b> Computer randomness is not random —
it is a fixed sequence started from a seed. Setting the seed means your "random" weights are the same every
run, so a result you got yesterday can be reproduced today. Every serious experiment sets one. It is also
why the labs give identical answers on your machine and everyone else's.</p>"""

    + h2("🕳", "Traps")
    + trap("""<p><b>Forgetting the tuple.</b> <code>np.zeros((2,3))</code>, not <code>np.zeros(2,3)</code>.
The same applies to <code>ones</code>, <code>full</code> and <code>random.rand</code>'s cousins.</p>""")
    + trap("""<p><b>Assuming arange includes the end.</b> <code>np.arange(0, 1, 0.1)</code> stops at 0.9.
And with decimal steps it can occasionally give an unexpected number of elements — floating point again.
linspace avoids that.</p>""")

    + h2("✅", "Check yourself")
    + quiz([
        ("What does np.arange(3) give?",
         "<p><code>array([0, 1, 2])</code> — three numbers, starting at 0, stopping before 3.</p>"),
        ("You want 100 evenly spaced x values from −5 to 5 for a plot. Which call?",
         "<p><code>np.linspace(-5, 5, 100)</code> — and both −5 and 5 are included.</p>"),
        ("Why set np.random.seed(1)?",
         "<p>So the “random” numbers are the same every run, making your results reproducible. Essential "
         "for any experiment you might need to explain or repeat.</p>"),
    ])

    + h2("🔗", "Go deeper")
    + links([
        ("docs", "https://numpy.org/doc/stable/reference/routines.array-creation.html",
         "NumPy — array creation routines", "The full catalogue, for when you need something unusual."),
    ]))

# ============================================================ 7
lesson("07-elementwise", "Elementwise arithmetic", 7,
    "Do a sum to every number at once, with no loop. This is the habit that makes machine learning code "
    "short.",
    h2("🎈", "The idea, in plain words")
    + kid("""<p>Write <code>a + b</code> with two arrays and NumPy lines them up and adds each pair. Write
<code>a ** 2</code> and it squares every single one.</p>
<p>No loop. You write the sum once and it happens everywhere.</p>""")

    + h2("🧮", "Worked by hand")
    + """<p>a = [1, 2, 3, 4], b = [10, 20, 30, 40].</p>
<ul>
<li><code>a + b</code> → [11, 22, 33, 44]</li>
<li><code>a * b</code> → [10, 40, 90, 160]</li>
<li><code>a ** 2</code> → [1, 4, 9, 16]</li>
<li><code>np.sqrt(a)</code> → [1, 1.41, 1.73, 2]</li>
</ul>
<p>Every result is the <b>same length</b> as what went in. Nothing is added up or collapsed — that is the
defining feature.</p>"""

    + h2("🎬", "Watch it move")
    + demo("felementwise", "Six operations, position by position",
           "notice the answer is always the same length as the input")

    + h2("💻", "In NumPy")
    + code("""
import numpy as np
a = np.array([1, 2, 3, 4])
b = np.array([10, 20, 30, 40])

a + b            # array([11, 22, 33, 44])
a * b            # array([ 10,  40,  90, 160])
a ** 2           # array([ 1,  4,  9, 16])
np.sqrt(a)       # array([1.  , 1.414, 1.732, 2.  ])
np.exp(a)        # e to each one
np.log(a)        # log of each one

# which is why the sigmoid works on a whole matrix with no loop:
def sigmoid(Z):
    return 1 / (1 + np.exp(-Z))
""")

    + h2("🔬", "What is actually happening")
    + """<p>Look at that sigmoid again. <code>Z</code> might be a (1000, 25) matrix — 25,000 numbers. The
function has no loop in it at all, because every operation inside is elementwise: <code>-Z</code> negates
all 25,000, <code>np.exp</code> exponentiates all 25,000, the division divides all 25,000.</p>
<p>This is why real machine learning code is so much shorter than you would expect. The loops are still
happening — they are just happening inside compiled C code rather than in Python.</p>
<p>The important contrast to hold onto: elementwise operations <b>preserve the shape</b>. Dot products and
matrix multiplication <b>collapse</b> a dimension. When you are reading code and wondering what shape
something is, that distinction answers it.</p>"""

    + h2("🕳", "Traps")
    + trap("""<p><b>Mismatched shapes.</b> <code>a + b</code> with lengths 3 and 4 is a ValueError — there
is nothing to pair the fourth with. Unless broadcasting applies, which is the next lesson.</p>""")
    + trap("""<p><b>Using <code>*</code> when you meant <code>@</code>.</b> Elementwise instead of matrix
multiply. Runs happily, gives wrong numbers.</p>""")

    + h2("✅", "Check yourself")
    + quiz([
        ("a = [2, 4], b = [3, 5]. What is a * b?",
         "<p><code>[6, 20]</code> — elementwise. For the dot product (26) you would need "
         "<code>a @ b</code>.</p>"),
        ("np.exp(Z) where Z is (100, 25). What shape comes back?",
         "<p><b>(100, 25)</b> — unchanged. Elementwise operations never change the shape.</p>"),
        ("Why does the sigmoid function need no loop?",
         "<p>Because every operation in it (<code>-</code>, <code>np.exp</code>, <code>+</code>, "
         "<code>/</code>) is elementwise and applies to all the numbers at once.</p>"),
    ])

    + h2("🔗", "Go deeper")
    + links([
        ("docs", "https://numpy.org/doc/stable/reference/ufuncs.html",
         "NumPy — universal functions (ufuncs)",
         "The formal name for these. The list of available ones is worth a skim."),
    ]))

# ============================================================ 8
lesson("08-broadcasting", "Broadcasting", 9,
    "How NumPy adds a (1,3) to a (2,3) without complaining. Enormously useful, and the source of some "
    "very quiet bugs.",
    h2("🎈", "The idea, in plain words")
    + kid("""<p>You have a table with 2 rows, and a single row of numbers you want to add to <b>both</b>
rows.</p>
<p>Strictly the shapes do not match. NumPy does it anyway — it quietly <b>stretches</b> the single row
down to cover both, and then adds.</p>
<p>That stretching is called broadcasting.</p>""")

    + h2("🔤", "The rule")
    + """<p>Line the shapes up <b>from the right</b>. Two dimensions are compatible if they are
<b>equal</b>, or if <b>one of them is 1</b>.</p>"""
    + table(["Shapes", "Compatible?", "Result"],
            [["(2, 3) and (1, 3)", "✅ 3=3, then 2 vs 1 — the 1 stretches", "(2, 3)"],
             ["(2, 3) and (3,)", "✅ the (3,) is treated as (1,3)", "(2, 3)"],
             ["(2, 3) and (2, 1)", "✅ the 1 stretches across", "(2, 3)"],
             ["(2, 3) and (2, 3)", "✅ identical", "(2, 3)"],
             ["(2, 3) and (3, 2)", "❌ 3≠2 and neither is 1", "ValueError"],
             ["(3, 1) and (1, 3)", "⚠️ both stretch", "<b>(3, 3)</b> — probably not what you wanted"]])

    + h2("🎬", "Watch it move")
    + demo("fbroadcast", "The single row being copied down",
           "nothing is really copied in memory — but this is what it computes")

    + h2("💻", "In NumPy")
    + code("""
import numpy as np
Z = np.array([[1, 2, 3],
              [4, 5, 6]])          # (2, 3)
b = np.array([10, 20, 30])         # (3,)

Z + b        # array([[11, 22, 33],
             #        [14, 25, 36]])     b added to EVERY row

# this is exactly the neural network layer from Course 2:
#   Z = np.matmul(A_in, W) + B
# where B is one row of biases, added to every example automatically

# feature scaling, same idea:
X_scaled = (X - X.mean(axis=0)) / X.std(axis=0)
#           (1000,4)  (4,)          (4,)    -> both broadcast down all 1000 rows
""")

    + h2("🔬", "What is actually happening")
    + """<p>Nothing is actually copied. NumPy computes as if the smaller array had been stretched, but it
never allocates the memory — it just reuses the same values. So broadcasting is free, which is why library
code leans on it so heavily.</p>
<p>Now the dangerous case, the last row of the table. A (3,1) and a (1,3) are <b>both</b> compatible under
the rule, so NumPy stretches both and hands you a (3,3). You expected three numbers and got nine, with no
error at all.</p>
<p>This is the classic silent bug. It usually happens when something you thought was a row is actually a
column — often the result of a <code>df['col']</code> versus <code>df[['col']]</code> mix-up, or a
forgotten <code>reshape</code>.</p>"""
    + key("""<p>When a result has a <b>surprising shape</b>, broadcasting is almost always what happened.
Print the shapes of both operands and the culprit is immediately obvious.</p>""")

    + h2("🕳", "Traps")
    + trap("""<p><b>(3,1) + (1,3) giving a (3,3).</b> No error, nine numbers where you wanted three. The
most common quiet bug in NumPy.</p>""")
    + trap("""<p><b>Assuming it aligns from the left.</b> It aligns from the <b>right</b>. That is why a
(3,) matches the columns of a (2,3), not the rows.</p>""")

    + h2("✅", "Check yourself")
    + quiz([
        ("(1000, 4) + (4,). Does it work, and what comes out?",
         "<p>Yes — the (4,) is added to every row. Result <b>(1000, 4)</b>. This is exactly how a bias "
         "vector is applied.</p>"),
        ("(5, 3) + (5,). Does it work?",
         "<p><b>No.</b> Aligning from the right, 3 vs 5 do not match and neither is 1. You would need "
         "<code>(5,1)</code> — try <code>b.reshape(-1, 1)</code>.</p>"),
        ("Your result is (100, 100) and you expected (100,). What happened?",
         "<p>You almost certainly added a (100,1) to a (1,100). Both broadcast, producing a square. Check "
         "the shapes of both operands.</p>"),
    ])

    + h2("🔗", "Go deeper")
    + links([
        ("docs", "https://numpy.org/doc/stable/user/basics.broadcasting.html",
         "NumPy — broadcasting rules",
         "Read the “General Broadcasting Rules” box until it is boring. It pays off all specialization."),
    ]))

# ============================================================ 9
lesson("09-dot-in-code", "np.dot, matmul and @", 8,
    "Four ways to multiply arrays, two of which collapse and two of which do not. Choosing wrong is a "
    "silent bug.",
    h2("🎈", "The idea, in plain words")
    + kid("""<p>There are two completely different things called “multiply” here.</p>
<p><code>*</code> pairs the numbers up and multiplies them, keeping them separate. You get a list back.</p>
<p><code>@</code> pairs them up, multiplies, <b>and adds everything together</b>. You get one number back.</p>
<p>Both run. Only one is what a formula usually means.</p>""")

    + h2("🔤", "The four spellings")
    + table(["Written", "Does", "a=[1,2,3], b=[4,5,6] gives", "Collapses?"],
            [["<code>a * b</code>", "elementwise", "<code>[4, 10, 18]</code>", "no"],
             ["<code>(a * b).sum()</code>", "elementwise, then add", "<code>32</code>", "yes"],
             ["<code>np.dot(a, b)</code>", "dot product", "<code>32</code>", "yes"],
             ["<code>a @ b</code>", "the modern operator", "<code>32</code>", "yes"]])

    + h2("🎬", "Watch it move")
    + demo("fdotcode", "Click each spelling and watch what comes out",
           "the “one number out?” panel is the thing to watch")

    + h2("💻", "In NumPy")
    + code("""
import numpy as np
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

a @ b            # 32     -- preferred for vectors
np.dot(a, b)     # 32     -- same thing
a * b            # [4 10 18]   -- NOT a dot product

A = np.random.rand(3, 2)
B = np.random.rand(2, 4)
A @ B            # (3, 4)  -- preferred for matrices
np.matmul(A, B)  # identical
A * B            # ValueError -- shapes do not match elementwise
""")
    + key("""<p><b>Use <code>@</code>.</b> It works for vectors and matrices, it reads clearly, and it does
not have <code>np.dot</code>'s surprising behaviour once you go past two dimensions.</p>""")

    + h2("🔬", "What is actually happening")
    + """<p>Why does <code>np.dot</code> have a caveat? Because it tries to be clever. For 1-D it does a dot
product; for 2-D it does matrix multiplication; for 3-D and above it does something else entirely (a sum
over particular axes) that is almost never what you meant.</p>
<p><code>np.matmul</code> and <code>@</code> behave consistently: they always treat the last two dimensions
as a matrix. When you meet batched operations in deep learning — where you have a stack of matrices —
that consistency matters.</p>
<p>The genuinely dangerous case is when shapes happen to allow both <code>*</code> and <code>@</code>. Two
(3,3) matrices, for instance. Both run, both give a (3,3), and only one is correct. Nothing warns you.</p>"""

    + h2("🕳", "Traps")
    + trap("""<p><b><code>*</code> where you meant <code>@</code>.</b> On square matrices both work and give
different answers. This is the expensive one.</p>""")
    + trap("""<p><b><code>np.dot</code> on 3-D arrays.</b> Does not do what you expect. Use
<code>@</code>.</p>""")

    + h2("✅", "Check yourself")
    + quiz([
        ("a = [1,2], b = [3,4]. What do a*b and a@b give?",
         "<p><code>a*b</code> → <code>[3, 8]</code> (a list). <code>a@b</code> → <code>11</code> "
         "(one number, 3 + 8).</p>"),
        ("X is (100, 4), W is (4, 25). Which operator, and what shape?",
         "<p><code>X @ W</code> → <b>(100, 25)</b>. The inner 4s match and vanish.</p>"),
        ("Why prefer @ over np.dot?",
         "<p>Because <code>np.dot</code> changes behaviour for arrays with more than 2 dimensions. "
         "<code>@</code> is consistent, and reads more clearly.</p>"),
    ])

    + h2("🔗", "Go deeper")
    + links([
        ("docs", "https://numpy.org/doc/stable/reference/generated/numpy.matmul.html",
         "numpy.matmul", "Read the note about how it differs from np.dot."),
    ]))

# ============================================================ 10
lesson("10-aggregations", "sum, mean, max — along an axis", 7,
    "Collapsing a lot of numbers into fewer. The same axis rule from lesson 5, now doing real work.",
    h2("🎈", "The idea, in plain words")
    + kid("""<p>You have a table of numbers and want a summary. Total? Average? Biggest?</p>
<p>The only question is <b>which direction</b> to summarise in — down the columns, across the rows, or
everything at once.</p>""")

    + h2("🔤", "The family")
    + decode([
        ("<code>.sum()</code>", "“sum”", "add them up."),
        ("<code>.mean()</code>", "“mean”", "the average."),
        ("<code>.std()</code>", "“standard deviation”", "the spread."),
        ("<code>.max()</code> / <code>.min()</code>", "—", "biggest / smallest value."),
        ("<code>.argmax()</code>", "“arg max”", "the <b>position</b> of the biggest."),
        ("<code>axis=0</code>", "—", "collapse the rows → one answer per <b>column</b>."),
        ("<code>axis=1</code>", "—", "collapse the columns → one answer per <b>row</b>."),
        ("no axis", "—", "collapse everything → a single number."),
    ], head=("Method", "Say it", "What it does"))

    + h2("🎬", "Watch it move")
    + demo("faxis", "Pick a function and an axis",
           "watch the shape of the answer change")

    + h2("💻", "In NumPy")
    + code("""
import numpy as np
M = np.arange(1, 13).reshape(3, 4)

M.sum()            # 78          everything
M.sum(axis=0)      # [15 18 21 24]   per column, shape (4,)
M.sum(axis=1)      # [10 26 42]      per row,    shape (3,)

# the two patterns you will use constantly:
X.mean(axis=0)                 # a statistic per FEATURE  -> feature scaling
np.argmax(probs, axis=1)       # a prediction per EXAMPLE -> classification

# and accuracy in one line, using a mask:
(preds == y).mean()            # fraction correct
""")

    + h2("🔬", "What is actually happening")
    + """<p>Two mental hooks, and after these <code>axis</code> stops being guesswork.</p>
<p><b>One: the named axis disappears from the shape.</b> (3,4) with axis=0 gives (4,). Want a result with
one number per feature? You want the examples gone, so collapse axis 0.</p>
<p><b>Two: think about what you want one of.</b> One number <em>per feature</em> → axis=0. One number
<em>per example</em> → axis=1. Say the sentence out loud and the axis follows.</p>
<p>There is a third useful trick above: <code>(preds == y).mean()</code>. The comparison makes an array of
True/False, and True counts as 1 — so the mean of that array is the fraction that are True. That is
accuracy, in one line, with no counting.</p>"""

    + h2("🕳", "Traps")
    + trap("""<p><b>Guessing the axis and getting a plausible answer.</b> If X is square, both axes give a
result of the same shape and you will not notice. Work it out rather than guessing.</p>""")
    + trap("""<p><b>Using <code>max</code> when you wanted <code>argmax</code>.</b> The score instead of
the choice.</p>""")

    + h2("✅", "Check yourself")
    + quiz([
        ("X is (500, 8). You want the average of each feature. Which call?",
         "<p><code>X.mean(axis=0)</code> → shape <b>(8,)</b>. The 500 examples collapse.</p>"),
        ("probs is (500, 10). How do you get the predicted class for each example?",
         "<p><code>np.argmax(probs, axis=1)</code> → shape <b>(500,)</b>. One prediction per row.</p>"),
        ("What does (preds == y).mean() compute?",
         "<p><b>Accuracy.</b> The comparison gives True/False, True counts as 1, so the mean is the "
         "fraction correct.</p>"),
    ])

    + h2("🔗", "Go deeper")
    + links([
        ("docs", "https://numpy.org/doc/stable/reference/routines.statistics.html",
         "NumPy — statistics routines", "The full list, all taking the same <code>axis</code> argument."),
    ]))

# ============================================================ 11
lesson("11-boolean-masks", "Boolean masks", 8,
    "Comparing an array gives you an array of True/False — and putting that in brackets filters your data. "
    "One of the most useful things in NumPy.",
    h2("🎈", "The idea, in plain words")
    + kid("""<p>Ask a question of a whole array — “which of these are bigger than 25?” — and you get back
a whole array of <b>yes/no</b> answers, one per position.</p>
<p>Then put that yes/no array inside the square brackets, and you keep only the yesses.</p>""")

    + h2("🧮", "Worked by hand")
    + """<p>x = [12, 31, 7, 44, 19, 28]</p>
<ul>
<li><code>x > 25</code> → [False, True, False, True, False, True] — a <b>mask</b>, same length</li>
<li><code>x[x > 25]</code> → [31, 44, 28] — only the ones where the mask was True</li>
<li><code>(x > 25).sum()</code> → 3 — because True counts as 1</li>
</ul>"""

    + h2("🎬", "Watch it move")
    + demo("fmask", "Slide the threshold and watch the mask and the filter",
           "the mask is always the same length as the data; the filtered result is not")

    + h2("💻", "In NumPy")
    + code("""
import numpy as np
x = np.array([12, 31, 7, 44, 19, 28])

x > 25              # array([False, True, False, True, False, True])
x[x > 25]           # array([31, 44, 28])
(x > 25).sum()      # 3      -- True counts as 1
(x > 25).mean()     # 0.5    -- half of them

# combining conditions -- EACH NEEDS ITS OWN BRACKETS
x[(x > 10) & (x < 40)]     # and
x[(x < 10) | (x > 40)]     # or

# selecting rows of a 2-D array by a condition on one column
X[y == 1]           # only the examples labelled 1
""")
    + warn("""<p>Use <code>&amp;</code> and <code>|</code>, <b>not</b> <code>and</code> and <code>or</code>.
Python's <code>and</code> tries to reduce a whole array to a single True/False and raises “truth value of
an array is ambiguous”. And each condition needs its own brackets, because <code>&amp;</code> binds more
tightly than <code>&gt;</code>.</p>""")

    + h2("🔬", "What is actually happening")
    + """<p>The comparison is elementwise, exactly like arithmetic — it just produces booleans instead of
numbers. And because True is 1 and False is 0, you get two very useful shortcuts for free:</p>
<ul>
<li><code>mask.sum()</code> <b>counts</b> how many passed.</li>
<li><code>mask.mean()</code> gives the <b>fraction</b> that passed.</li>
</ul>
<p>Which is where the one-line accuracy from the last lesson comes from: <code>(preds == y).mean()</code>.
And it is how the confusion-matrix counts in Course 2 are computed —
<code>np.sum((preds == 1) &amp; (y == 1))</code> is the number of true positives.</p>
<p>Note that unlike slicing, boolean indexing returns a <b>copy</b>, not a view. Modifying the result does
not touch the original.</p>"""

    + h2("🕳", "Traps")
    + trap("""<p><b><code>and</code> instead of <code>&amp;</code>.</b> Gives “The truth value of an array
with more than one element is ambiguous” — a confusing message for a simple cause.</p>""")
    + trap("""<p><b>Missing brackets.</b> <code>x &gt; 10 &amp; x &lt; 40</code> is parsed wrongly. Write
<code>(x &gt; 10) &amp; (x &lt; 40)</code>.</p>""")

    + h2("✅", "Check yourself")
    + quiz([
        ("x = [1, 5, 10, 15]. What is x[x > 5]?",
         "<p><code>[10, 15]</code>. The mask is [F, F, T, T].</p>"),
        ("How do you count how many predictions were correct?",
         "<p><code>(preds == y).sum()</code>. Or <code>.mean()</code> for the fraction — which is "
         "accuracy.</p>"),
        ("Why does x[(x>2) and (x<8)] fail?",
         "<p>Python's <code>and</code> wants a single True/False, not an array. Use <code>&amp;</code>, "
         "with brackets around each condition.</p>"),
    ])

    + h2("🔗", "Go deeper")
    + links([
        ("docs", "https://numpy.org/doc/stable/user/basics.indexing.html#boolean-array-indexing",
         "NumPy — boolean array indexing", "Including np.where, which is the “if/else for arrays”."),
    ]))

# ============================================================ 12
lesson("12-reshape", "reshape, flatten and T", 7,
    "Rearranging the same numbers into a different grid — and the difference from transpose, which is not "
    "the same thing.",
    h2("🎈", "The idea, in plain words")
    + kid("""<p>You have twelve numbers in a row. You can arrange them as 3 rows of 4, or 4 rows of 3, or
2 rows of 6.</p>
<p>The numbers do not change and never move. Only how you <b>read</b> them changes.</p>""")

    + h2("🔤", "The syntax")
    + decode([
        ("<code>x.reshape(3, 4)</code>", "“reshape three by four”", "re-cut into 3 rows of 4. Must total 12."),
        ("<code>x.reshape(-1, 4)</code>", "“minus one”", "“4 columns, and work out the rows for me”."),
        ("<code>x.reshape(1, -1)</code>", "—", "make it one row. <b>The fix for “Keras wants 2-D”.</b>"),
        ("<code>x.flatten()</code>", "“flatten”", "squash everything back to 1-D."),
        ("<code>x.T</code>", "“transpose”", "<b>a different thing</b> — mirror rows and columns."),
    ], head=("Written", "Say it", "What it does"))

    + h2("🎬", "Watch it move")
    + demo("freshape", "The same twelve numbers, several ways",
           "read the numbers in order — they never change position in the sequence")

    + h2("💻", "In NumPy")
    + code("""
import numpy as np
x = np.arange(12)         # [0 1 2 ... 11], shape (12,)

x.reshape(3, 4)           # 3 rows of 4
x.reshape(-1, 4)          # same -- NumPy works out that -1 means 3
x.reshape(1, -1)          # shape (1, 12)  one row
x.reshape(-1, 1)          # shape (12, 1)  one column
x.reshape(3, 4).flatten() # back to (12,)

# the classic fix, when a library insists on 2-D:
single = np.array([200.0, 17.0])     # (2,)   -- Keras complains
single.reshape(1, -1)                # (1,2)  -- happy
""")

    + h2("🔬", "What is actually happening")
    + """<p>Reshape is essentially free. The twelve numbers stay exactly where they are in memory; NumPy
just changes the note saying how to walk through them. That is why you can reshape a huge array instantly.</p>
<p><b>reshape is not transpose</b>, and this is worth being clear about. Take [1,2,3,4,5,6] as a (2,3):</p>"""
    + table(["", "Result", "Reading order"],
            [["<code>.reshape(3, 2)</code>", "[[1,2],[3,4],[5,6]]", "re-cuts the same sequence"],
             ["<code>.T</code>", "[[1,4],[2,5],[3,6]]", "mirrors positions"]])
    + """<p>Both are (3,2). The numbers are in different places. Using one where you meant the other gives
no error and wrong answers — one of the harder bugs to spot, because the shape looks right.</p>"""

    + h2("🕳", "Traps")
    + trap("""<p><b>reshape when you meant transpose.</b> Same shape, different numbers, no error.</p>""")
    + trap("""<p><b>Wrong total.</b> <code>reshape(5, 3)</code> on 12 numbers is an error — 15 ≠ 12. The
new shape must multiply to the same count.</p>""")
    + trap("""<p><b><code>.T</code> on a 1-D array does nothing.</b> A (3,) has no second dimension to
swap. Use <code>reshape(-1, 1)</code> to get a column.</p>""")

    + h2("✅", "Check yourself")
    + quiz([
        ("x has 20 elements. What does x.reshape(-1, 5) give?",
         "<p><b>(4, 5)</b> — you asked for 5 columns, and −1 works out that 4 rows are needed.</p>"),
        ("Keras rejects your single example of shape (2,). What do you do?",
         "<p><code>x.reshape(1, -1)</code> → shape (1, 2). One row, two features.</p>"),
        ("Is reshape(3,2) the same as .T on a (2,3) array?",
         "<p><b>No.</b> Both give shape (3,2) and the numbers land in different places. reshape re-cuts "
         "the sequence; transpose mirrors it.</p>"),
    ])

    + h2("🔗", "Go deeper")
    + links([
        ("docs", "https://numpy.org/doc/stable/reference/generated/numpy.reshape.html",
         "numpy.reshape", "Including the <code>order</code> argument, if you ever need column-major."),
    ]))

# ============================================================ 13
lesson("13-pandas-dataframes", "pandas DataFrames", 9,
    "A spreadsheet with column names. This is how data gets into your notebook, and five methods cover "
    "nearly everything.",
    h2("🎈", "The idea, in plain words")
    + kid("""<p>NumPy knows about <b>positions</b>: column 2, row 7. pandas knows about <b>names</b>: the
“price” column, the row with index 7.</p>
<p>That is the whole difference. pandas is for loading messy real files and tidying them up. NumPy is for
doing the maths afterwards. You use both, in that order.</p>""")

    + h2("🔤", "The five that matter")
    + decode([
        ("<code>pd.read_csv(f)</code>", "“read c-s-v”", "load a file into a DataFrame. Where everything starts."),
        ("<code>df.head()</code>", "“head”", "the first 5 rows. <b>Always your first move.</b>"),
        ("<code>df.shape</code>", "“shape”", "(rows, columns) — same as NumPy."),
        ("<code>df.info()</code>", "“info”", "column names, types, and how many values are missing."),
        ("<code>df.describe()</code>", "“describe”", "count, mean, std, min, max for every numeric column."),
    ], head=("Call", "Say it", "What it gives you"))

    + h2("🧮", "Selecting things")
    + table(["Written", "Gives", "Note"],
            [["<code>df['price']</code>", "one column", "a <b>Series</b>, shape (m,)"],
             ["<code>df[['price']]</code>", "one column", "a <b>DataFrame</b>, shape (m,1) — double brackets"],
             ["<code>df[['size','beds']]</code>", "two columns", "a list of names inside the brackets"],
             ["<code>df.head(3)</code>", "first 3 rows", ""],
             ["<code>df[df['beds'] > 2]</code>", "matching rows", "a boolean mask, just like NumPy"],
             ["<code>df.iloc[1, 0]</code>", "one cell", "by <b>position</b>, like NumPy"],
             ["<code>df.loc[1, 'size']</code>", "one cell", "by <b>label</b>"]])

    + h2("🎬", "Watch it move")
    + demo("fdataframe", "Click each selection and watch what lights up",
           "note how the row index and the column names are both labels")

    + h2("💻", "In pandas")
    + code("""
import pandas as pd

df = pd.read_csv('houses.csv')

df.head()            # look at it FIRST, every time
df.shape             # (1000, 5)
df.info()            # types, and missing values
df.describe()        # summary statistics
df.columns           # the column names -- check the spelling

df['price'].mean()          # aggregations work like NumPy
df[df['beds'] > 2].shape    # how many have more than 2 bedrooms
df.isnull().sum()           # missing values per column
""")

    + h2("🔬", "What is actually happening")
    + """<p>A DataFrame is really a collection of columns, each of which is a <b>Series</b> — a 1-D array
with an index attached. That is why <code>df['price']</code> gives you something slightly different from
<code>df[['price']]</code>: the first is one Series, the second is a DataFrame that happens to have one
column.</p>
<p>Most of the time it does not matter. It matters when you hand the result to something that insists on
2-D, which is exactly the <code>(m,)</code> versus <code>(m,1)</code> distinction from the shape lesson,
wearing pandas clothing.</p>
<p><b>The habit worth forming:</b> run <code>head()</code>, <code>info()</code> and <code>describe()</code>
on every dataset before you model anything. <code>info()</code> tells you about missing values and about
columns that arrived as text when you assumed they were numbers. <code>describe()</code> tells you the
scale of each feature — which is your first hint about whether you need feature scaling.</p>"""

    + h2("🕳", "Traps")
    + trap("""<p><b><code>KeyError: 'Price'</code>.</b> Column names are case-sensitive and often have
stray spaces. <code>print(df.columns)</code> shows exactly what they are.</p>""")
    + trap("""<p><b>Numbers that arrived as text.</b> A column with one stray “N/A” becomes type
<code>object</code> and every sum misbehaves. <code>df.info()</code> reveals it instantly.</p>""")
    + trap("""<p><b>SettingWithCopyWarning.</b> pandas warning you that you may be modifying a copy rather
than the original. Use <code>.loc</code> for assignments and it goes away.</p>""")

    + h2("✅", "Check yourself")
    + quiz([
        ("What is the difference between df['price'] and df[['price']]?",
         "<p>The first is a <b>Series</b>, shape (m,). The second is a <b>DataFrame</b>, shape (m,1). "
         "Same numbers, different container.</p>"),
        ("You get KeyError: 'Price'. What is the first thing to run?",
         "<p><code>print(df.columns)</code>. It is almost certainly <code>'price'</code>, or has a "
         "trailing space.</p>"),
        ("Which three calls should you run on every new dataset?",
         "<p><code>head()</code>, <code>info()</code>, <code>describe()</code>. Shape, types, missing "
         "values, and the scale of each feature.</p>"),
    ])

    + h2("🔗", "Go deeper")
    + links([
        ("docs", "https://pandas.pydata.org/docs/user_guide/10min.html",
         "pandas — 10 minutes to pandas",
         "The official quick tour. Genuinely about ten minutes, and worth all of them."),
        ("docs", "https://pandas.pydata.org/docs/user_guide/indexing.html",
         "pandas — indexing and selecting",
         "The <code>.loc</code> vs <code>.iloc</code> distinction, properly explained."),
    ]))

# ============================================================ 14
lesson("14-pandas-to-numpy", "From pandas to NumPy", 6,
    "The one line that crosses from “loading data” to “doing maths” — and the shape trap waiting there.",
    h2("🎈", "The idea, in plain words")
    + kid("""<p>You loaded a file with pandas and tidied it up. Now you want to do maths, which means
NumPy.</p>
<p>One method crosses over. You lose the column names — so pick your columns <b>before</b> you cross, not
after.</p>""")

    + h2("🔤", "The crossing")
    + decode([
        ("<code>.to_numpy()</code>", "“to numpy”", "the modern spelling. Returns a plain array."),
        ("<code>.values</code>", "“values”", "the older spelling. You will see it in older notebooks. Same thing."),
        ("<code>X</code>", "“capital X”", "conventionally your <b>features</b> — a 2-D array."),
        ("<code>y</code>", "“lowercase y”", "conventionally your <b>target</b> — a 1-D array."),
    ], head=("Written", "Say it", "What it is"))

    + h2("🎬", "Watch it move")
    + demo("fpandasnumpy", "The names falling away",
           "after crossing you have positions, not labels")

    + h2("💻", "The standard pattern")
    + code("""
import pandas as pd
import numpy as np

df = pd.read_csv('houses.csv')

# select the columns you want FIRST, while you still have names
X = df[['size', 'beds', 'floors', 'age']].to_numpy()    # (1000, 4)
y = df['price'].to_numpy()                              # (1000,)

X.shape, y.shape          # ((1000, 4), (1000,))

# now everything from the NumPy lessons applies:
X = (X - X.mean(axis=0)) / X.std(axis=0)                # feature scaling
""")
    + warn("""<p>Note the shapes. <code>df[['price']]</code> would give <b>(1000, 1)</b>, while
<code>df['price']</code> gives <b>(1000,)</b>. Most scikit-learn and TensorFlow code wants y as
<code>(m,)</code> and X as <code>(m, n)</code>. Getting y as (m,1) produces confusing broadcasting bugs
later rather than an immediate error.</p>""")

    + h2("🔬", "What is actually happening")
    + """<p>Why cross over at all, rather than doing everything in pandas? Because pandas carries the index
and column labels around with every operation, which is useful for bookkeeping and pure overhead for
arithmetic. NumPy drops all of that and just computes.</p>
<p>The division of labour that experienced people settle on:</p>
<ul>
<li><b>pandas</b> — load the file, inspect it, handle missing values, engineer features by name, filter rows.</li>
<li><b>cross over once</b>, deliberately, with <code>.to_numpy()</code>.</li>
<li><b>NumPy</b> — scaling, matrix multiplication, training, everything numeric.</li>
</ul>
<p>Crossing back and forth repeatedly is a sign something is being done the hard way.</p>"""

    + h2("🕳", "Traps")
    + trap("""<p><b>Converting first, then trying to select columns by name.</b> The names are gone. Select
first.</p>""")
    + trap("""<p><b>y ending up as (m, 1) instead of (m,).</b> Use single brackets for the target column.
If you already have a (m,1), fix it with <code>y.ravel()</code>.</p>""")

    + h2("✅", "Check yourself")
    + quiz([
        ("Write the two lines to get X and y from a DataFrame with columns size, beds, price.",
         "<p><code>X = df[['size','beds']].to_numpy()</code> → (m, 2)<br>"
         "<code>y = df['price'].to_numpy()</code> → (m,)</p>"),
        ("Why select columns before converting?",
         "<p>Because <code>.to_numpy()</code> discards the column names. Afterwards you only have "
         "positions.</p>"),
        ("Your y has shape (1000, 1) and something is broadcasting oddly. What do you do?",
         "<p><code>y = y.ravel()</code> (or use single brackets when selecting) to get (1000,).</p>"),
    ])

    + h2("🔗", "Go deeper")
    + links([
        ("docs", "https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_numpy.html",
         "pandas — DataFrame.to_numpy", "Note what happens to mixed-type columns."),
    ]))

# ============================================================ 15
lesson("15-reading-errors", "Reading an error message", 8,
    "Tracebacks look terrifying and are mostly noise. Read the last line, and know the five errors you "
    "will actually hit.",
    h2("🎈", "The idea, in plain words")
    + kid("""<p>When Python fails it prints a wall of red text. Almost none of it matters.</p>
<p><b>Read the last line.</b> It is a plain English sentence that names the actual problem. The lines above
it just show how the code got there.</p>""")

    + h2("🔤", "The five you will meet")
    + table(["Error", "What it means", "What to do"],
            [["<code>ValueError: shapes not aligned</code>", "a matmul whose inner numbers do not match",
              "print both <code>.shape</code>s; transpose one"],
             ["<code>IndexError: out of bounds</code>", "you asked for a position that does not exist",
              "counting starts at 0; the last is <code>x[-1]</code>"],
             ["<code>TypeError: can only concatenate list</code>", "you did maths on a list, not an array",
              "<code>np.array(my_list)</code>"],
             ["<code>NameError: not defined</code>", "a typo, or you never ran the import cell",
              "check spelling, then run the imports"],
             ["<code>KeyError: 'Price'</code>", "that column name is not in the DataFrame",
              "<code>print(df.columns)</code>"]])

    + h2("🎬", "Watch it move")
    + demo("ftraceback", "A real traceback, annotated",
           "click each error type for what it means and what to do")

    + h2("💻", "The two habits that fix most of them")
    + code("""
# 1. print shapes -- solves nearly every ValueError
print(X.shape, W.shape, b.shape)

# 2. print types -- solves nearly every TypeError
print(type(x), x.dtype if hasattr(x, 'dtype') else '')

# and when you are stuck, cut the line in half:
tmp = X @ W          # does this alone work?
print(tmp.shape)
tmp2 = tmp + b       # or is it this bit?
""")

    + h2("🔬", "What is actually happening")
    + """<p>A traceback is a <b>stack</b> — the chain of function calls that led to the failure, oldest
first. So the last frame is where it actually broke, and the very last line is Python's summary of why.</p>
<p>Reading order: <b>last line first</b> (what went wrong), then the frame just above it (where), then work
upwards only if you still need to know how you got there.</p>
<p>The other habit worth building is <b>bisecting</b>. When a long expression fails, split it into pieces
and print after each one. It takes thirty seconds and converts “something is wrong somewhere” into “line 2
produces a (4,25) and I expected (25,4)”.</p>"""
    + key("""<p>Error messages are not obstacles — they are the most specific help you will get all day.
A <code>ValueError</code> naming two shapes has told you exactly what is wrong. Read it before searching
the internet.</p>""")

    + h2("🕳", "Traps")
    + trap("""<p><b>Reading the traceback from the top.</b> The top is the outermost call and rarely the
problem. Start at the bottom.</p>""")
    + trap("""<p><b>Pasting the whole traceback into a search engine.</b> Paste just the last line, and
strip out your own file paths and variable names.</p>""")

    + h2("✅", "Check yourself")
    + quiz([
        ("ValueError: shapes (100,4) and (25,4) not aligned. What is wrong and how do you fix it?",
         "<p>The inner numbers, 4 and 25, do not match. Transpose the second: <code>X @ W.T</code> gives "
         "(100,4)@(4,25) → (100,25).</p>"),
        ("NameError: name 'np' is not defined. What happened?",
         "<p>You did not run the <code>import numpy as np</code> cell — or the kernel was restarted "
         "since you did.</p>"),
        ("Where in a traceback is the useful information?",
         "<p>The <b>last line</b>. It names the error type and describes the problem in plain English.</p>"),
    ])

    + h2("🔗", "Go deeper")
    + links([
        ("docs", "https://docs.python.org/3/tutorial/errors.html",
         "Python — errors and exceptions", "What each built-in error type actually means."),
    ]))

# ============================================================ 16
lesson("16-functions", "Writing and reading functions", 8,
    "Every graded exercise in this specialization is “fill in the body of this function”. So it is worth "
    "being able to read one at a glance.",
    h2("🎈", "The idea, in plain words")
    + kid("""<p>A function is a recipe with a name. You give it ingredients, it does some steps, and it
hands you back a result.</p>
<p>Writing one means saying: what it is called, what it needs, and what it gives back.</p>""")

    + h2("🔤", "The anatomy")
    + code("""
def compute_cost(X, y, w, b):
    m = X.shape[0]
    err = (X @ w + b) - y
    return np.sum(err ** 2) / (2 * m)
""")
    + decode([
        ("<code>def</code>", "“def”", "“I am defining a function”."),
        ("<code>compute_cost</code>", "—", "the <b>name</b> you will call it by."),
        ("<code>(X, y, w, b)</code>", "“the parameters”", "what it needs. Matched <b>in order</b> when you call it."),
        ("<code>:</code>", "“colon”", "starts the body. Everything indented below belongs to the function."),
        ("indentation", "—", "not decoration — it is <b>what defines the body</b> in Python."),
        ("<code>return</code>", "“return”", "hands one value back. Without it you get <code>None</code>."),
    ], head=("Piece", "Say it", "What it does"))

    + h2("🎬", "Watch it move")
    + demo("ffunction", "The parts of a function, one at a time",
           "and how the values you pass in line up with the parameters")

    + h2("💻", "Calling it")
    + code("""
J = compute_cost(X_train, y_train, w, b)
#                   |        |     |  |
#                   X        y     w  b     -- matched IN ORDER

# or by name, which is clearer and order-independent:
J = compute_cost(X=X_train, y=y_train, w=w, b=b)

# default values -- callers can leave these out
def gradient_descent(X, y, w, b, alpha=0.01, iters=1000):
    ...

gradient_descent(X, y, w, b)                 # uses the defaults
gradient_descent(X, y, w, b, alpha=0.1)      # overrides just one
""")

    + h2("🔬", "What is actually happening")
    + """<p>When you read a function you have never seen, three things tell you almost everything:</p>
<ol>
<li><b>The name.</b> Good code names things honestly — <code>compute_cost</code> computes a cost.</li>
<li><b>The parameters.</b> What does it need? <code>(X, y, w, b)</code> tells you it works on a whole
dataset with a set of parameters.</li>
<li><b>The return.</b> What does it hand back? One number, or a tuple of several?</li>
</ol>
<p>That is enough to <em>use</em> a function without reading its body — which is exactly the skill the
assignments need, because they hand you a signature and a docstring and ask you to fill in the middle.</p>
<p>One Python quirk worth knowing: a function can return several things at once, as a tuple.
<code>return dj_dw, dj_db</code> is unpacked by <code>dj_dw, dj_db = compute_gradient(...)</code>. You will
see this constantly.</p>"""

    + h2("🕳", "Traps")
    + trap("""<p><b>Forgetting <code>return</code>.</b> The function runs, does the work, and hands back
<code>None</code>. Then something downstream fails with a confusing message about NoneType.</p>""")
    + trap("""<p><b>Inconsistent indentation.</b> Python is strict. Mixing tabs and spaces gives
<code>IndentationError</code>; most editors can be set to convert tabs to spaces.</p>""")
    + trap("""<p><b>Assuming the parameter names mean anything to the caller.</b> They are matched by
<b>position</b> unless you name them. Swapping two arguments of the same type is a silent bug.</p>""")

    + h2("✅", "Check yourself")
    + quiz([
        ("A function ends without a return statement. What do you get back?",
         "<p><code>None</code>. Which usually causes a confusing error further down rather than "
         "where the real problem is.</p>"),
        ("def f(a, b, c=10). How many arguments must you pass?",
         "<p>At least <b>two</b> — a and b. c has a default and is optional.</p>"),
        ("What does dj_dw, dj_db = compute_gradient(X, y, w, b) mean?",
         "<p>The function returns <b>two</b> values as a tuple, and they are unpacked into two variables "
         "in order.</p>"),
    ])

    + h2("🎓", "That is the Foundations track")
    + """<p>You now have the maths vocabulary and the Python vocabulary that all three courses assume. Not
mastery — but enough that a formula on a lecture slide has no symbol in it you cannot name, and a line in a
notebook has no syntax in it you cannot read.</p>
<p>That is the point at which Course 1 stops washing over you and starts making sense. Go there next.</p>"""

    + h2("🔗", "Go deeper")
    + links([
        ("docs", "https://docs.python.org/3/tutorial/controlflow.html#defining-functions",
         "Python — defining functions", "The official treatment, including keyword and default arguments."),
        ("lab", "../../C1%20-%20Supervised%20Machine%20Learning%20-%20Regression%20and%20Classification/week2/C1W2A1/C1_W2_Linear_Regression.ipynb",
         "Course 1, Week 2 assignment",
         "In this repo. Fill in the bodies of two functions whose signatures are already written. You are ready for it."),
    ]))

WEEK = dict(
    course="F0", week=2, title="Python, NumPy and pandas",
    time="~4–5 h",
    goal="Enough Python to read and write every line in the labs: arrays, shapes, slicing, broadcasting, "
         "DataFrames, and how to read an error message.",
    lessons=L,
)
