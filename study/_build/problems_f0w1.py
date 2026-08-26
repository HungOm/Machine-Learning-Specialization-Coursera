# -*- coding: utf-8 -*-
"""F0 W1 — the maths, mixed up on purpose."""
from problemkit import P, m, frac, cols, pre

L = []
def add(*a, **k): L.append(P(*a, **k))

# ---------------------------------------------------------------- 01
add("f0w1-p01", level=1, tag="functions",
    lesson="f0/w1-01-what-is-a-function.html",
    ask="A function is defined as %s. Work out %s, %s and %s."
        % (m("f(x) = 3x − 4"), m("f(0)"), m("f(2)"), m("f(−1)")),
    steps=[("Put 0 where every x is", "f(0) = 3·0 − 4 = 0 − 4"),
           ("Put 2 where every x is", "f(2) = 3·2 − 4 = 6 − 4"),
           ("Put −1 where every x is. Watch the sign: 3 × (−1) = −3",
            "f(−1) = 3·(−1) − 4 = −3 − 4")],
    answer="%s, %s, %s" % (m("f(0) = −4"), m("f(2) = 2"), m("f(−1) = −7")),
    gist="A function is a rule: whatever number you feed it, the rule does the exact same thing to it, ""every time. Here the rule is “triple it, then take away 4”.",
    check="Read f(0) off a graph of y = 3x − 4 instead of computing it: it is exactly where the line ""crosses the vertical axis. Same answer, no arithmetic.",
    why="A function is a machine, and the letter in the brackets is whatever you feed it. "
        "Everything later — the model, the cost, the sigmoid — is this one move repeated.")

# ---------------------------------------------------------------- 02
add("f0w1-p02", level=1, tag="slope",
    lesson="f0/w1-04-slope.html",
    ask="A straight line passes through %s and %s. Find its slope, then say what the "
        "slope means in words." % (m("(1, 7)"), m("(5, 19)")),
    hint="Slope is rise over run: how much y changed, divided by how much x changed.",
    steps=[("Rise — how far up", "19 − 7 = 12"),
           ("Run — how far across", "5 − 1 = 4"),
           ("Divide", "12 ÷ 4 = 3")],
    answer="%s. In words: <b>every time x goes up by 1, y goes up by 3.</b>" % m("slope = 3"),
    gist="You are asking how steep a line is: compare how far up two points are apart against how far ""across they are apart.",
    check="Test a third point the slope predicts. From (1, 7), stepping 2 more to the right should add ""2 × 3 = 6 to y, landing at (3, 13). Check that point is on the line and you have confirmed ""the slope independently, with no division involved.",
    why="In ML the slope of the cost curve is the gradient, and the gradient is the whole "
        "of gradient descent. If you can read a slope you can read a gradient.")

# ---------------------------------------------------------------- 03
add("f0w1-p03", level=2, tag="sigma",
    lesson="f0/w1-07-sigma-notation.html",
    ask="Given %s, evaluate %s."
        % (m("x = [4, 1, 6, 9]"), m("Σ<sub>i=1</sub><sup>4</sup> (x<sub>i</sub> − 5)<sup>2</sup>")),
    hint="Σ says: do the thing inside once for every i, then add up the results. "
         "Subtract first, square second, add last.",
    steps=[("i = 1", "(4 − 5)² = (−1)² = 1"),
           ("i = 2", "(1 − 5)² = (−4)² = 16"),
           ("i = 3", "(6 − 5)² = (1)² = 1"),
           ("i = 4", "(9 − 5)² = (4)² = 16"),
           ("Now add the four results", "1 + 16 + 1 + 16")],
    answer=m("34"),
    gist="Σ means “do this to every number in the list, then add up the results”. Here ""“this” is: subtract 5, then square.",
    check="5 is exactly the mean of [4, 1, 6, 9] (4+1+6+9 = 20, ÷ 4 = 5) — so this sum is exactly ""the numerator of the variance from the Mean and Variance lesson. Divide your answer by 4 and ""you get the variance of this list: 34 ÷ 4 = 8.5.",
    why="This is the squared-error cost with the 5 playing the part of the prediction. "
        "You have just computed the numerator of J(w,b) by hand.")

# ---------------------------------------------------------------- 04
add("f0w1-p04", level=2, tag="derivatives",
    lesson="f0/w1-05-derivatives.html",
    ask="Differentiate each one with respect to %s:<br>"
        "(a) %s &nbsp; (b) %s &nbsp; (c) %s &nbsp; (d) %s"
        % (m("x"), m("f(x) = x<sup>2</sup>"), m("f(x) = 5x"),
           m("f(x) = 7"), m("f(x) = 3x<sup>2</sup> − 4x + 9")),
    hint="One rule does all four: the derivative of x<sup>n</sup> is n·x<sup>n</sup>⁻¹. A plain number has "
         "derivative 0, because a flat line has no slope.",
    steps=[("(a) power rule: bring the 2 down, drop the power by one", "2x<sup>1</sup> = 2x"),
           ("(b) 5x is 5·x¹ → bring down the 1", "5·1·x<sup>0</sup> = 5"),
           ("(c) a constant never changes, so its slope is flat", "0"),
           ("(d) differentiate term by term",
            "3·2x − 4·1 + 0 = 6x − 4")],
    answer="(a) %s &nbsp; (b) %s &nbsp; (c) %s &nbsp; (d) %s"
           % (m("2x"), m("5"), m("0"), m("6x − 4")),
    gist="Differentiating asks: nudge x by a tiny amount right now — how much does the output change, ""per unit of nudge? The one rule covers all four: bring the power down as a multiplier, then ""drop the power by one.",
    check="Check (a) the numerical way from Lesson 5: nudge x = 3 by h = 0.001. ""((3.001)² − 3²) ÷ 0.001 = 6.001 — matching 2x = 2(3) = 6 with no ""differentiation rule needed at all.",
    why="Every gradient in this specialization is one of these three rules applied to a "
        "slightly longer expression. Nothing harder ever appears.")

# ---------------------------------------------------------------- 05
add("f0w1-p05", level=2, tag="dot product",
    lesson="f0/w1-10-dot-product.html",
    ask="With %s and %s, compute %s. Then compute %s and say what you notice."
        % (m("<b>a</b> = [2, 0, 3]"), m("<b>b</b> = [1, 5, −2]"),
           m("<b>a</b> · <b>b</b>"), m("<b>b</b> · <b>a</b>")),
    steps=[("Multiply matching positions", "2×1 = 2 &nbsp;·&nbsp; 0×5 = 0 &nbsp;·&nbsp; 3×(−2) = −6"),
           ("Add the three products", "2 + 0 + (−6)"),
           ("Now the other way round", "1×2 + 5×0 + (−2)×3 = 2 + 0 − 6")],
    answer="%s and %s — <b>the dot product does not care about the order.</b>"
           % (m("<b>a</b> · <b>b</b> = −4"), m("<b>b</b> · <b>a</b> = −4")),
    gist="A dot product pairs two lists position by position, multiplies each pair, and adds everything ""into one number.",
    check="Notice both directions multiplied the exact same three pairs of numbers, just written in a ""different order — multiplication does not care which factor comes first, so adding those ""same three products twice was always going to give the same total.",
    why="The dot product turns two lists into one number. That is exactly what a neuron "
        "does to its inputs and weights before it adds b.")

# ---------------------------------------------------------------- 06
add("f0w1-p06", level=1, tag="logarithms",
    lesson="f0/w1-15-logarithms.html",
    ask="Without a calculator: (a) %s &nbsp; (b) %s &nbsp; (c) %s &nbsp; (d) %s"
        % (m("log<sub>10</sub>(1000)"), m("log<sub>2</sub>(8)"),
           m("ln(1)"), m("log(0.001)  [base 10]")),
    hint="Read log as a question: “what power do I raise the base to, to get this?”",
    steps=[("(a) 10 to what power is 1000? 10³ = 1000", "3"),
           ("(b) 2 to what power is 8? 2³ = 8", "3"),
           ("(c) e to what power is 1? Anything to the power 0 is 1", "0"),
           ("(d) 0.001 = 10⁻³", "−3")],
    answer="(a) %s &nbsp; (b) %s &nbsp; (c) %s &nbsp; (d) %s" % (m("3"), m("3"), m("0"), m("−3")),
    gist="A logarithm asks a “what power” question. log₁₀(1000) is asking: 10 to what ""power gives 1000?",
    check="Check (d) a different way: 0.001 = 1÷1000, and log of a reciprocal is always minus the log ""of the original — so log(0.001) = −log(1000) = −3, matching part (a) with the ""sign flipped.",
    why="Logistic loss is built out of logs. The one fact that matters there: log of "
        "something near 1 is near 0, and log of something near 0 is a huge negative number.")

# ---------------------------------------------------------------- 07
add("f0w1-p07", level=2, tag="matrix multiplication",
    lesson="f0/w1-12-matrix-multiplication.html",
    ask="Multiply %s by %s. Before you compute anything, write down the shape of the answer."
        % (m("A = [[1, 2], [3, 4]]"), m("B = [[5, 6], [7, 8]]")),
    hint="Shape first: (2×2) times (2×2) gives (2×2). Each output cell is a row of A "
         "dotted with a column of B.",
    steps=[("Shapes: (2×2)·(2×2). The inner 2s match, so it is legal; the outer 2s give the answer shape",
            "result is 2×2"),
           ("Row 1 of A · column 1 of B", "1×5 + 2×7 = 5 + 14 = 19"),
           ("Row 1 of A · column 2 of B", "1×6 + 2×8 = 6 + 16 = 22"),
           ("Row 2 of A · column 1 of B", "3×5 + 4×7 = 15 + 28 = 43"),
           ("Row 2 of A · column 2 of B", "3×6 + 4×8 = 18 + 32 = 50")],
    answer=m("AB = [[19, 22], [43, 50]]"),
    gist="Each cell of the answer is one ordinary dot product: one row of the first matrix paired ""against one column of the second.",
    check="Read the first cell through the Dot Product lesson’s shopping-list picture: row 1 of A is ""[1, 2], column 1 of B is [5, 7] — a 2-item basket priced at [5, 7], total bill ""1×5 + 2×7 = 19. Same arithmetic, a completely different way of seeing it.",
    why="Every forward pass through a layer is this. Get the shape rule into your fingers "
        "and half of all neural-network bugs disappear.")

# ---------------------------------------------------------------- 08
add("f0w1-p08", level=2, tag="mean & variance",
    lesson="f0/w1-17-mean-variance.html",
    ask="For the data %s find the mean, then the variance (divide by %s), then the "
        "standard deviation." % (m("[2, 4, 4, 4, 5, 5, 7, 9]"), m("n")),
    steps=[("Add them up", "2+4+4+4+5+5+7+9 = 40"),
           ("Divide by n = 8", "μ = 40 ÷ 8 = 5"),
           ("Distance from the mean, each one squared",
            "9, 1, 1, 1, 0, 0, 4, 16"),
           ("Add those and divide by 8", "32 ÷ 8 = 4"),
           ("Standard deviation is the square root of the variance", "√4 = 2")],
    answer="%s, %s, %s" % (m("μ = 5"), m("σ² = 4"), m("σ = 2")),
    gist="Mean is just “add them all up, divide by how many there are” — the ordinary ""average. Variance measures how spread out the numbers are around that average.",
    check="Before squaring, check the deviations themselves: −3, −1, −1, −1, 0, 0, 2, ""4 add up to exactly zero. Deviations from the true mean <b>always</b> cancel — if yours ""had not summed to zero, that would be the moment to go back and check the mean.",
    why="Feature scaling is exactly this, done to a column and then used to rewrite it. "
        "Z-score scaling is (x − μ) ÷ σ and nothing else.")

# ---------------------------------------------------------------- 09
add("f0w1-p09", level=3, tag="partial derivatives",
    lesson="f0/w1-06-partial-derivatives.html",
    ask="For %s, find %s and %s, then evaluate both at %s."
        % (m("f(w, b) = w<sup>2</sup>b + 3b"), m("∂f/∂w"), m("∂f/∂b"), m("(w, b) = (2, 5)")),
    hint="For ∂/∂w, freeze b — treat it as if it were the number 5 the whole way through. "
         "For ∂/∂b, freeze w.",
    steps=[("∂/∂w: b is frozen, so w²b is “a constant times w²”, and 3b is just a constant",
            "∂f/∂w = 2wb + 0 = 2wb"),
           ("∂/∂b: w is frozen, so w²b is “a constant times b”, and 3b differentiates to 3",
            "∂f/∂b = w² + 3"),
           ("Evaluate the first at w = 2, b = 5", "2·2·5 = 20"),
           ("Evaluate the second at w = 2", "2² + 3 = 4 + 3 = 7")],
    answer="%s and %s; at (2, 5) they are %s and %s."
           % (m("∂f/∂w = 2wb"), m("∂f/∂b = w² + 3"), m("20"), m("7")),
    gist="Finding ∂f/∂w means: pretend b is frozen at some fixed number, then differentiate as ""if w were the only thing that could ever move.",
    check="Land on ∂f/∂b = 7 a different way: freeze w at its actual value, 2, <b>before</b> ""differentiating. f(2, b) = 2²b + 3b = 4b + 3b = 7b — an ordinary one-variable function ""whose derivative is just 7. No partial notation required at all.",
    why="Gradient descent updates w and b at the same time using exactly this pair of "
        "numbers. The freezing move is the whole idea of a partial derivative.")

# ---------------------------------------------------------------- 10
add("f0w1-p10", level=2, tag="probability",
    lesson="f0/w1-16-probability.html",
    ask="A model says an email is spam with probability %s. "
        "(a) What is the probability it is not spam? "
        "(b) If you classify anything above 0.5 as spam, what does this model say? "
        "(c) Two independent emails both get 0.8 — what is the chance both are spam?"
        % m("P = 0.8"),
    steps=[("(a) Probabilities of all the outcomes add to 1", "1 − 0.8 = 0.2"),
           ("(b) 0.8 is above the 0.5 threshold", "predict spam"),
           ("(c) Independent events multiply", "0.8 × 0.8 = 0.64")],
    answer="(a) %s &nbsp; (b) %s &nbsp; (c) %s" % (m("0.2"), "spam", m("0.64")),
    gist="All the possible outcomes must add up to 1, and independent events multiply rather than add.",
    check="0.8 × 0.8 asks: what fraction of the time would <b>both</b> of two independent, ""80%-likely events happen? Multiplying two numbers under 1 always shrinks the answer — so ""0.64 being smaller than 0.8 is exactly what should happen, not a mistake.",
    why="Logistic regression outputs a probability, not a label. The threshold is a "
        "separate decision you make afterwards — and you are allowed to move it.")

# ---------------------------------------------------------------- 11
add("f0w1-p11", level=1, tag="transpose",
    lesson="f0/w1-13-transpose.html",
    ask="Write down %s where %s. What shape is %s, and what shape is %s?"
        % (m("A<sup>T</sup>"), m("A = [[1, 2, 3], [4, 5, 6]]"), m("A"), m("A<sup>T</sup>")),
    steps=[("A has 2 rows and 3 columns", "A is 2×3"),
           ("Transposing swaps rows and columns: row 1 of A becomes column 1 of Aᵀ",
            "[1, 2, 3] → first column"),
           ("Row 2 of A becomes column 2 of Aᵀ", "[4, 5, 6] → second column")],
    answer="%s &nbsp;— %s is %s and %s is %s."
           % (m("A<sup>T</sup> = [[1, 4], [2, 5], [3, 6]]"), m("A"), m("2×3"),
              m("A<sup>T</sup>"), m("3×2")),
    gist="Transposing tips the grid on its side: whatever sat in row i, column j moves to row j, ""column i. Nothing is calculated — only where each number sits changes.",
    check="Confirm the shape with no grid-drawing at all: A is (2 rows, 3 columns), and transposing ""always swaps the two numbers round, so A" + m("<sup>T</sup>") + " must be (3 rows, 2 columns) ""— you know the shape of the answer before moving a single number.",
    why="Transpose exists almost entirely to make shapes line up so a multiplication is "
        "legal. When NumPy shouts about shapes, a transpose is usually the fix.")

# ---------------------------------------------------------------- 12
add("f0w1-p12", level=2, tag="exponentials",
    lesson="f0/w1-14-exponentials.html",
    ask="The sigmoid is %s. Compute %s, %s, and %s. "
        "Use %s and %s."
        % (m("g(z) = 1 / (1 + e<sup>−z</sup>)"), m("g(0)"), m("g(2)"), m("g(−2)"),
           m("e<sup>−2</sup> ≈ 0.135"), m("e<sup>2</sup> ≈ 7.389")),
    hint="Do the exponent first, then the 1 +, then the division. Nothing else.",
    steps=[("z = 0: e⁰ = 1", "g(0) = 1 / (1 + 1) = 1/2 = 0.5"),
           ("z = 2: the exponent is −2, so e⁻² ≈ 0.135",
            "g(2) = 1 / (1 + 0.135) = 1 / 1.135 ≈ 0.881"),
           ("z = −2: the exponent is +2, so e² ≈ 7.389",
            "g(−2) = 1 / (1 + 7.389) = 1 / 8.389 ≈ 0.119"),
           ("Notice the pair", "0.881 + 0.119 = 1.000")],
    answer="%s, %s, %s. And %s — sigmoid is symmetric about 0.5."
           % (m("g(0) = 0.5"), m("g(2) ≈ 0.881"), m("g(−2) ≈ 0.119"), m("g(−z) = 1 − g(z)")),
    gist="The sigmoid squashes any number into somewhere between 0 and 1: work out the exponent first, ""add 1, then divide 1 by that.",
    check="Get g(−2) with no exponentials at all: g(−z) = 1 − g(z) is always true, so once ""g(2) ≈ 0.881 is known, g(−2) must be 1 − 0.881 = 0.119 — the pairing rule does ""the work.",
    why="You will meet g(z) hundreds of times. Knowing g(0) = 0.5 by heart tells you the "
        "decision boundary sits where z = 0, which is where wx + b = 0.")

# ---------------------------------------------------------------- 13
add("f0w1-p13", level=3, tag="argmax",
    lesson="f0/w1-19-min-max-argmax.html",
    ask="A softmax layer outputs %s for classes %s.<br>"
        "(a) What is %s? (b) What is %s? (c) Why does the difference matter?"
        % (m("[0.1, 0.6, 0.05, 0.25]"), m("[cat, dog, bird, fox]"),
           m("max"), m("argmax")),
    steps=[("max asks “what is the biggest value?”", "0.6"),
           ("argmax asks “at which position?” Counting from 0", "index 1"),
           ("Index 1 in the class list", "dog")],
    answer="(a) %s &nbsp; (b) %s, i.e. <b>dog</b> &nbsp; (c) max is the "
           "<i>confidence</i>; argmax is the <i>prediction</i>. You report the label from "
           "argmax and the confidence from max." % (m("0.6"), m("1")),
    gist="max picks out the biggest number in the list. argmax picks out <b>where</b> that number sits ""— its position, not its value.",
    check="A fast way to catch the classic mix-up: if an answer to argmax looks like a probability ""(somewhere between 0 and 1), max was accidentally computed instead — argmax must always ""be a whole-number position.",
    why="Mixing these up is a real and common bug: printing 0.6 where the class name was "
        "wanted, or comparing an index against a probability.")

# ---------------------------------------------------------------- 14
add("f0w1-p14", level=2, tag="vectors",
    lesson="f0/w1-09-vectors.html",
    ask="With %s and %s, compute %s, %s, and the length %s."
        % (m("<b>u</b> = [3, 4]"), m("<b>v</b> = [1, 2]"),
           m("<b>u</b> + <b>v</b>"), m("2<b>u</b>"), m("‖<b>u</b>‖")),
    steps=[("Adding is position by position", "[3+1, 4+2] = [4, 6]"),
           ("Multiplying by a number stretches every entry", "[2·3, 2·4] = [6, 8]"),
           ("Length is Pythagoras", "√(3² + 4²) = √(9 + 16) = √25")],
    answer="%s, %s, %s" % (m("[4, 6]"), m("[6, 8]"), m("‖<b>u</b>‖ = 5")),
    gist="Adding vectors combines them position by position. Multiplying by a plain number stretches ""every entry by that much. Length is Pythagoras, with more terms if the vector is longer.",
    check="[3, 4] is the well-known 3–4–5 triangle, so ‖u‖ = 5 should look immediately ""familiar — no calculator required for this particular pair of numbers.",
    why="‖w‖² is the thing regularization shrinks. A vector's length is a single number "
        "measuring “how big are these weights, overall”.")

# ---------------------------------------------------------------- 15
add("f0w1-p15", level=3, tag="normal distribution",
    lesson="f0/w1-18-normal-distribution.html",
    ask="Exam marks are normally distributed with %s and %s. "
        "(a) Between which two marks do about 68%% of students fall? "
        "(b) About 95%%? (c) A student scores 85 — how many standard deviations above the mean is that?"
        % (m("μ = 70"), m("σ = 10")),
    hint="The 68–95–99.7 rule: one σ either side holds ~68%, two σ holds ~95%.",
    steps=[("(a) one σ either side of the mean", "70 − 10 = 60 and 70 + 10 = 80"),
           ("(b) two σ either side", "70 − 20 = 50 and 70 + 20 = 90"),
           ("(c) that is the z-score: (x − μ) ÷ σ", "(85 − 70) ÷ 10 = 15 ÷ 10")],
    answer="(a) %s &nbsp; (b) %s &nbsp; (c) %s"
           % (m("60 to 80"), m("50 to 90"), m("z = 1.5")),
    gist="μ is where the middle of the bell sits. σ is roughly how far a typical value strays ""from it. The 68–95–99.7 rule says what fraction of everything falls within 1, 2 or 3 ""of those typical distances.",
    check="Check part (c) against (a) and (b) rather than trusting the arithmetic alone: a score of 85 ""sits at z = 1.5, which is between the 68% boundary (z = 1, up to 80) and the 95% boundary ""(z = 2, up to 90) — so 85 should feel somewhat unusual but nowhere near extreme, exactly ""where 1.5 sits between 1 and 2.",
    why="Anomaly detection in Course 3 flags points with a very low probability under a "
        "fitted Gaussian. The z-score is how you say “how unusual is this” in one number.")

# ---------------------------------------------------------------- 16
add("f0w1-p16", level=3, tag="Σ + slope together",
    lesson="f0/w1-07-sigma-notation.html",
    ask="A model predicts %s. The training data is %s. "
        "Compute the cost %s."
        % (m("f(x) = 2x + 1"), m("(1, 3), (2, 5), (3, 8)"),
           m("J = (1/2m) Σ (f(x<sup>(i)</sup>) − y<sup>(i)</sup>)<sup>2</sup>")),
    hint="Three columns on paper: prediction, error, error squared. Then sum, then divide "
         "by 2m where m = 3.",
    steps=[("Predictions", "f(1) = 3, f(2) = 5, f(3) = 7"),
           ("Errors, prediction minus actual", "3−3 = 0, &nbsp; 5−5 = 0, &nbsp; 7−8 = −1"),
           ("Square them", "0, 0, 1"),
           ("Sum", "0 + 0 + 1 = 1"),
           ("Divide by 2m, with m = 3", "1 ÷ 6")],
    answer="%s (about %s)" % (m("J = 1/6"), m("0.167")),
    gist="This is the Course 1 cost function, run on three real houses: for each one, see how wrong ""the line’s guess was, square that error, add the three up, then average.",
    check="The line predicted the first two houses exactly right — both errors were 0. The entire ""cost of 1/6 came from missing the <b>third</b> house alone by 1. A perfect model here would ""have scored J = 0 exactly.",
    why="This is the whole of Course 1 Week 1 in one calculation. If you can do this on "
        "paper you can read every cost-function plot in the course.")

SET = dict(course="F0", week=1, title="The Maths You Actually Need",
           lede="Sixteen problems, deliberately shuffled so you have to work out what kind "
                "of problem each one is before you can solve it. Paper and pencil — the "
                "point is to produce the maths, not recognise it.",
           problems=L)
