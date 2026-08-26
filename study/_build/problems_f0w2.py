# -*- coding: utf-8 -*-
"""F0 W2 — Python, NumPy and pandas. Predict the output, then check it."""
from problemkit import P, m, pre, cols

L = []
def add(*a, **k): L.append(P(*a, **k))

add("f0w2-p01", level=1, tag="shape",
    lesson="f0/w2-05-shape-and-axis.html",
    ask="Give the <code>.shape</code> of each:<br>"
        + pre("a = np.array([1, 2, 3])\nb = np.array([[1, 2, 3]])\nc = np.array([[1], [2], [3]])\nd = np.array([[1, 2], [3, 4], [5, 6]])"),
    hint="Count the brackets. One opening bracket at the start means 1-D; two means 2-D. "
         "Then read shape outside-in: (rows, columns).",
    steps=[("a — one pair of brackets, three numbers. 1-D, and the comma in the shape is not a typo",
            "(3,)"),
           ("b — brackets inside brackets: one row of three", "(1, 3)"),
           ("c — three rows of one", "(3, 1)"),
           ("d — three rows of two", "(3, 2)")],
    answer="%s, %s, %s, %s" % (m("(3,)"), m("(1, 3)"), m("(3, 1)"), m("(3, 2)")),
    why="(3,) and (3,1) behave completely differently under broadcasting. Almost every "
        "confusing NumPy result starts with someone assuming these are the same thing.")

add("f0w2-p02", level=2, tag="broadcasting",
    lesson="f0/w2-08-broadcasting.html",
    ask="What does this print, and what is the resulting shape?"
        + pre("A = np.array([[1, 2, 3],\n              [4, 5, 6]])\nb = np.array([10, 20, 30])\nprint(A + b)"),
    hint="Line the shapes up from the right. (2,3) and (3,). The missing dimension on the "
         "left is treated as 1, then stretched.",
    steps=[("Shapes right-aligned: (2, 3) and (3,) → (2, 3) and (1, 3)", "compatible"),
           ("b is stretched down to two identical rows", "[[10,20,30],[10,20,30]]"),
           ("Now add elementwise, row 1", "1+10, 2+20, 3+30 = 11, 22, 33"),
           ("Row 2", "4+10, 5+20, 6+30 = 14, 25, 36")],
    answer=pre("[[11 22 33]\n [14 25 36]]") + "shape %s" % m("(2, 3)"),
    why="This is exactly how a bias vector gets added to a whole batch at once. One row of "
        "biases, stretched silently over every example.")

add("f0w2-p03", level=2, tag="axis",
    lesson="f0/w2-10-aggregations.html",
    ask="With %s, what are<br>(a) <code>A.sum()</code> (b) <code>A.sum(axis=0)</code> "
        "(c) <code>A.sum(axis=1)</code> — and what shape is each?"
        % m("A = [[1, 2, 3], [4, 5, 6]]"),
    hint="axis=0 means “collapse the rows” — you end up with one number per column. "
         "The axis you name is the one that disappears.",
    steps=[("(a) no axis: collapse everything to one number", "1+2+3+4+5+6 = 21, shape ()"),
           ("(b) axis=0 collapses down the rows, leaving one entry per column",
            "[1+4, 2+5, 3+6] = [5, 7, 9], shape (3,)"),
           ("(c) axis=1 collapses across the columns, leaving one entry per row",
            "[1+2+3, 4+5+6] = [6, 15], shape (2,)")],
    answer="(a) %s &nbsp; (b) %s &nbsp; (c) %s" % (m("21"), m("[5, 7, 9]"), m("[6, 15]")),
    why="“Average the loss over the batch” is axis=0. “Sum the features for each example” "
        "is axis=1. Choosing the wrong one gives a number that looks plausible and is wrong.")

add("f0w2-p04", level=2, tag="dot product in code",
    lesson="f0/w2-09-dot-in-code.html",
    ask="Rewrite this loop as one line of NumPy, and say why the NumPy version is faster."
        + pre("total = 0\nfor i in range(len(w)):\n    total = total + w[i] * x[i]"),
    steps=[("The loop multiplies matching entries and adds them up — that is a dot product",
            "np.dot(w, x)"),
           ("Equivalent forms", "w @ x  &nbsp;or&nbsp; np.sum(w * x)"),
           ("Why faster: the loop runs in Python, one step at a time. np.dot hands the whole "
            "array to compiled C, which uses the CPU's vector instructions to do many "
            "multiplications per clock tick", "one call instead of len(w) interpreter steps")],
    answer=pre("total = np.dot(w, x)   # or  w @ x"),
    why="Vectorization is the difference between a model that trains in seconds and one "
        "that trains overnight. It is the same arithmetic, moved somewhere faster.")

add("f0w2-p05", level=1, tag="indexing",
    lesson="f0/w2-04-indexing-slicing.html",
    ask="With %s, give the value of:<br>"
        "(a) <code>x[0]</code> (b) <code>x[-1]</code> (c) <code>x[1:4]</code> "
        "(d) <code>x[:2]</code> (e) <code>x[::2]</code>"
        % m("x = np.array([10, 20, 30, 40, 50])"),
    hint="Counting starts at 0. A slice a:b includes a and excludes b.",
    steps=[("(a) position 0 is the first", "10"),
           ("(b) −1 counts back from the end", "50"),
           ("(c) positions 1, 2, 3 — stop before 4", "[20, 30, 40]"),
           ("(d) from the start, stop before 2", "[10, 20]"),
           ("(e) every second element from the start", "[10, 30, 50]")],
    answer="(a) %s (b) %s (c) %s (d) %s (e) %s"
           % (m("10"), m("50"), m("[20,30,40]"), m("[10,20]"), m("[10,30,50]")),
    why="Off-by-one on a slice silently drops your last training example. It never raises "
        "an error; it just quietly makes m smaller.")

add("f0w2-p06", level=2, tag="boolean masks",
    lesson="f0/w2-11-boolean-masks.html",
    ask="With %s, what do these give?<br>"
        "(a) <code>y &gt; 0.5</code> (b) <code>y[y &gt; 0.5]</code> "
        "(c) <code>(y &gt; 0.5).sum()</code> (d) <code>(y &gt; 0.5).astype(int)</code>"
        % m("y = np.array([0.2, 0.9, 0.5, 0.7])"),
    hint="A comparison on an array gives an array of True/False, the same shape. "
         "True counts as 1 when you add it up.",
    steps=[("(a) compare every element; note 0.5 > 0.5 is False",
            "[False, True, False, True]"),
           ("(b) the mask picks out only the True positions", "[0.9, 0.7]"),
           ("(c) True is 1, False is 0, so summing counts them", "0+1+0+1 = 2"),
           ("(d) same conversion, kept as an array", "[0, 1, 0, 1]")],
    answer="(a) %s (b) %s (c) %s (d) %s"
           % (m("[F, T, F, T]"), m("[0.9, 0.7]"), m("2"), m("[0, 1, 0, 1]")),
    why="(d) is exactly how you turn logistic-regression probabilities into 0/1 predictions. "
        "(c) is how you count how many you got right.")

add("f0w2-p07", level=3, tag="broadcasting trap",
    lesson="f0/w2-08-broadcasting.html",
    ask="One of these raises an error and one silently produces a 3×3 array. Which is which, "
        "and what is the 3×3 array?"
        + pre("a = np.array([1, 2, 3])        # shape (3,)\nb = np.array([[1], [2], [3]])  # shape (3, 1)\nc = np.array([1, 2, 3, 4])     # shape (4,)\n\nprint(a + b)\nprint(a + c)"),
    hint="Right-align the shapes. Two dimensions are compatible if they are equal, or if one "
         "of them is 1.",
    steps=[("a + b: shapes (3,) and (3,1) → right-align as (1,3) and (3,1)", "both stretch → (3, 3)"),
           ("Row i of the result is b[i] added to every element of a",
            "[[2,3,4],[3,4,5],[4,5,6]]"),
           ("a + c: shapes (3,) and (4,). 3 ≠ 4 and neither is 1",
            "ValueError: operands could not be broadcast together")],
    answer="%s is the silent 3×3 %s; %s raises %s."
           % (m("a + b"), m("[[2,3,4],[3,4,5],[4,5,6]]"), m("a + c"), m("ValueError")),
    why="The dangerous one is the case that works. A (3,) meeting a (3,1) gives you a matrix "
        "where you expected a vector, and the error only shows up three functions later.")

add("f0w2-p08", level=2, tag="reshape",
    lesson="f0/w2-12-reshape.html",
    ask="Starting from %s, write the code to make:<br>"
        "(a) a 2×3 array (b) a 3×2 array (c) a column vector, without counting the elements"
        % m("x = np.arange(6)"),
    hint="np.arange(6) is [0 1 2 3 4 5]. reshape(-1, 1) means “one column, and you work out "
         "how many rows”.",
    steps=[("(a) fill row by row", "x.reshape(2, 3) → [[0,1,2],[3,4,5]]"),
           ("(b) same numbers, different box", "x.reshape(3, 2) → [[0,1],[2,3],[4,5]]"),
           ("(c) −1 tells NumPy to infer that dimension", "x.reshape(-1, 1) → shape (6, 1)")],
    answer=pre("x.reshape(2, 3)\nx.reshape(3, 2)\nx.reshape(-1, 1)"),
    why="reshape(-1, 1) appears constantly in the labs, turning a flat (m,) of labels into "
        "the (m, 1) column that a matrix operation needs.")

add("f0w2-p09", level=2, tag="pandas",
    lesson="f0/w2-13-pandas-dataframes.html",
    ask="Given this DataFrame, write the code for each request."
        + pre("df = pd.DataFrame({\n    'size':  [850, 1200, 1500, 900],\n    'beds':  [2, 3, 3, 2],\n    'price': [200, 310, 400, 220],\n})")
        + "(a) just the price column (b) rows where beds is 3 (c) the mean price "
          "(d) the whole thing as a NumPy array",
    steps=[("(a) square brackets with the column name", "df['price']"),
           ("(b) a boolean mask, same idea as NumPy", "df[df['beds'] == 3]"),
           ("(c) pandas has the aggregations built in", "df['price'].mean() → 282.5"),
           ("(d) .to_numpy() drops the labels and hands you the raw grid",
            "df.to_numpy(), shape (4, 3)")],
    answer=pre("df['price']\ndf[df['beds'] == 3]\ndf['price'].mean()\ndf.to_numpy()"),
    why="Every lab starts in pandas (labelled, human-readable) and switches to NumPy (fast, "
        "anonymous) the moment maths begins. .to_numpy() is that border crossing.")

add("f0w2-p10", level=1, tag="lists vs arrays",
    lesson="f0/w2-03-lists-vs-arrays.html",
    ask="Predict both outputs and explain the difference."
        + pre("a = [1, 2, 3]\nb = np.array([1, 2, 3])\nprint(a * 2)\nprint(b * 2)"),
    steps=[("A Python list treats * as “repeat me”", "[1, 2, 3, 1, 2, 3]"),
           ("A NumPy array treats * as “multiply every element”", "[2, 4, 6]"),
           ("Same symbol, two completely different meanings, decided by the type",
            "list → concatenate · array → scale")],
    answer=pre("[1, 2, 3, 1, 2, 3]\n[2 4 6]"),
    why="This is the single most common beginner surprise in the labs. If a result is twice "
        "as long as it should be, you are holding a list where you thought you had an array.")

add("f0w2-p11", level=3, tag="reading errors",
    lesson="f0/w2-15-reading-errors.html",
    ask="You get this error. Say in one sentence what went wrong, and give a fix."
        + pre("ValueError: operands could not be broadcast together\n            with shapes (100,4) (3,)"),
    hint="Read the two shapes, right-aligned. Ignore everything else in the traceback first.",
    steps=[("Right-align them", "(100, 4)  and  (3,)  →  compare 4 against 3"),
           ("4 ≠ 3, and neither is 1, so there is no way to stretch them", "incompatible"),
           ("Meaning: you have 100 examples with 4 features each, but a weight vector of "
            "length 3", "one feature has no weight"),
           ("Fix: make w have one entry per column of X", "w = np.zeros(X.shape[1])")],
    answer="X has 4 features but w has only 3 weights. Build w from the data: "
           + pre("w = np.zeros(X.shape[1])   # never a hard-coded 3"),
    why="Shape errors are the most common failure in the assignments, and the two shapes in "
        "the message tell you the answer. Read those first, the stack trace second.")

add("f0w2-p12", level=2, tag="elementwise vs dot",
    lesson="f0/w2-07-elementwise.html",
    ask="With %s and %s, what is <code>w * x</code> and what is <code>w @ x</code>? "
        "Which one is a single number?" % (m("w = [1, 2, 3]"), m("x = [4, 5, 6]")),
    steps=[("* is elementwise: pair them up and multiply", "[1·4, 2·5, 3·6] = [4, 10, 18]"),
           ("@ is the dot product: multiply pairs, then add", "4 + 10 + 18 = 32"),
           ("So * keeps the shape and @ collapses it", "(3,) → (3,)  vs  (3,) → ()")],
    answer="%s and %s — only %s is a single number."
           % (m("w * x = [4, 10, 18]"), m("w @ x = 32"), m("w @ x")),
    why="np.sum(w * x) and w @ x give the same answer. Confusing * with @ is how a cost "
        "function ends up returning an array instead of a scalar.")

add("f0w2-p13", level=2, tag="creating arrays",
    lesson="f0/w2-06-creating-arrays.html",
    ask="Write one line for each: (a) a length-5 array of zeros (b) a 3×2 array of ones "
        "(c) the numbers 0 to 9 (d) five evenly spaced numbers from 0 to 1 inclusive.",
    steps=[("(a) zeros takes the shape", "np.zeros(5)"),
           ("(b) a tuple for a 2-D shape", "np.ones((3, 2))"),
           ("(c) arange stops *before* its argument", "np.arange(10)"),
           ("(d) linspace includes both ends and takes a count, not a step",
            "np.linspace(0, 1, 5) → [0, 0.25, 0.5, 0.75, 1]")],
    answer=pre("np.zeros(5)\nnp.ones((3, 2))\nnp.arange(10)\nnp.linspace(0, 1, 5)"),
    why="arange excludes the end, linspace includes it. Mixing them up is the reason a plot "
        "sometimes stops one tick short.")

add("f0w2-p14", level=3, tag="putting it together",
    lesson="f0/w2-16-functions.html",
    ask="Write a function <code>predict(X, w, b)</code> that takes %s, %s and a scalar %s "
        "and returns the %s predictions — no Python loop. Then say what shape it returns "
        "and why." % (m("X of shape (m, n)"), m("w of shape (n,)"), m("b"), m("m")),
    hint="Each prediction is one row of X dotted with w, plus b. Matrix multiplication does "
         "all m of them in a single operation.",
    steps=[("Shapes: (m, n) @ (n,) → the inner n's cancel", "result is (m,)"),
           ("Adding the scalar b broadcasts to every element", "still (m,)"),
           ("So the whole thing is one line", "return X @ w + b"),
           ("Sanity check with m=2, n=3: X is 2×3, w is (3,) → 2 predictions", "(2,)")],
    answer=pre("def predict(X, w, b):\n    return X @ w + b     # shape (m,)")
           + "It returns %s — one prediction per row of X." % m("(m,)"),
    why="This exact line is the forward pass for linear regression, and with a sigmoid "
        "wrapped round it, for logistic regression too. Everything else is finding good w and b.")

SET = dict(course="F0", week=2, title="Python, NumPy and pandas",
           lede="Predict the output before you run it. That is the whole skill — if you can "
                "say what a line will print, you can debug it; if you can only run it and "
                "look, you cannot.",
           problems=L)
