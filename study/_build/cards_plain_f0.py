# -*- coding: utf-8 -*-
"""Beginner decode for the Foundations cards — here the emphasis is the NumPy equivalent."""
from cardkit import plain

P = {
"f0-function": plain(
  "A vending machine for numbers. Put a coin in, get a chocolate bar out — same coin, same bar, every time.",
  [("f", "“eff”", "the machine's name. Could be g, h, J, σ — all just names"),
   ("f(x)", "“f of x”", "what comes out. The brackets mean “applied to”, never “times”"),
   ("f(3)", "“f of three”", "put 3 in. If f(x) = 2x+1 the answer is 7")],
  "In code: <code>def f(x): return 2*x + 1</code>"),

"f0-superscripts": plain(
  "Little raised numbers mean three different things, and the brackets around them are the only clue.",
  [("x⁽²⁾", "“x, example two”", "the SECOND house in your data"),
   ("x²", "“x squared”", "x times itself"),
   ("a[²]", "“a, layer two”", "belonging to layer 2 of a network")],
  "Like a shirt label: “size 10” and “10 in the pack” are both 10 and mean nothing alike."),

"f0-slope": plain(
  "How steep a line is, as one number: step one to the right, how far up do you go?",
  [("rise", "“the rise”", "how much it went UP. Negative if it went down"),
   ("run", "“the run”", "how far you went ACROSS"),
   ("m", "“em”", "the school-maths letter for slope"),
   ("w", "“double-you”", "the SAME thing, in machine learning")],
  "y = mx + c at school is f(x) = wx + b here. Identical; only the letters changed."),

"f0-derivative": plain(
  "Slope needs two points and a curve gives you one. So take a second point very close by, then slide it "
  "closer and closer. The number it settles on is the derivative.",
  [("f′(x)", "“f prime of x”", "the derivative. The little dash is all it is"),
   ("df/dx", "“dee f by dee x”", "the same thing, written differently"),
   ("h", "“aitch”", "the tiny gap to the second point"),
   ("lim h→0", "“as h goes to zero”", "“keep shrinking the gap and see what it approaches”")],
  "In code: <code>(f(x+h) - f(x)) / h</code> with h about 1e-5. Any smaller and rounding ruins it."),

"f0-partial": plain(
  "You are on a hillside. “How steep?” is incomplete — steep in which direction? Pick one direction, walk "
  "only along that line, and you are back to an ordinary slope.",
  [("∂", "“partial” or “curly dee”", "a curly d. It only means “other variables are being held still”"),
   ("∂J/∂w", "“dee J dee w”", "how much J changes if you nudge w alone"),
   ("∇J", "“grad J”", "all the partials collected into one list — the gradient")],
  "In code, “held still” literally means you do not add h to it."),

"f0-sigma": plain(
  "Writing x₁ + x₂ + … + x₁₀₀₀ is silly, so maths has a shorthand. It is a for loop wearing a hat.",
  [("Σ", "“sum of” (capital sigma)", "add up what follows"),
   ("i = 1", "“i starts at one”", "the counter and where it begins — underneath"),
   ("m", "“up to m”", "where it stops — on top. Usually the number of examples"),
   ("xᵢ", "“x sub i”", "the thing being added; i changes each time round")],
  "In code: <code>np.sum(x)</code>, or <code>np.sum(x ** 2)</code> for Σx²."),

"f0-pi": plain(
  "Sigma's sibling. Same layout, one different instruction: multiply instead of add.",
  [("Π", "“product of” (capital pi)", "multiply them all together"),
   ("π", "“pi” (lowercase)", "the COMPLETELY different thing: 3.14159"),
   ("underflow", "“UNDER-flow”", "so many small numbers multiplied that the answer rounds to zero")],
  "In code: <code>np.prod(p)</code> — but real code writes <code>np.sum(np.log(p))</code> to stay safe."),

"f0-vector-length": plain(
  "A list of numbers kept in order. Two numbers you can draw as an arrow; four hundred you cannot, and "
  "every formula works identically.",
  [("x⃗", "“x vector”", "the little arrow means “this is a list, not one number”"),
   ("‖x‖", "“the norm of x”", "its LENGTH. Double bars"),
   ("|x|", "“absolute value”", "single bars — a different thing, for single numbers"),
   ("scalar", "“SCAY-lar”", "the word for an ordinary single number")],
  "In code: <code>np.linalg.norm(x)</code>. It is just Pythagoras with more terms."),

"f0-dot": plain(
  "A shopping list and a price list. Pair each item with its price, multiply, add it all up. One number "
  "comes out: the total bill.",
  [("·", "“dot”", "the dot product — includes the adding, unlike ordinary ×"),
   ("aᵀb", "“a transpose b”", "the same thing, written the matrix way"),
   ("cos θ", "“cos theta”", "how much two arrows point the same way")],
  "In code: <code>a @ b</code> gives 32. <code>a * b</code> gives [4, 10, 18] — a list, not a total."),

"f0-shape-rule": plain(
  "A test you can do in your head before writing any code: can these two tables be multiplied, and what "
  "size will the answer be?",
  [("(m × n)", "“m by n”", "m rows, n columns. Rows always first"),
   ("inner numbers", "—", "the two in the middle. They MUST match"),
   ("outer numbers", "—", "the two on the ends. They become the answer's shape")],
  "In code: <code>A @ B</code>. Write (3×2)(2×4) — middles match, answer is (3×4)."),

"f0-transpose": plain(
  "Tip the spreadsheet on its side. Rows become columns. No number changes value; they just move.",
  [("Mᵀ", "“M transpose”", "the maths notation — a raised capital T"),
   ("M.T", "“M dot tee”", "the NumPy version. Same thing"),
   ("view", "“a view”", "NumPy does not copy anything — it just changes how it walks the numbers")],
  "You reach for it when shapes refuse to match: <code>X @ W.T</code>."),

"f0-exp": plain(
  "e is a fixed number, about 2.718, like π. “e to the power z” is always positive and grows very fast — "
  "and those two facts are the whole reason it appears everywhere.",
  [("e", "“ee”", "≈ 2.71828. Nothing to solve"),
   ("e^z", "“e to the z”", "also written exp(z), because superscripts are hard to type"),
   ("e^0", "“e to the zero”", "= 1. Always"),
   ("overflow", "“OH-ver-flow”", "e^1000 is too big to store → the computer returns infinity")],
  "In code: <code>np.exp(z)</code>. And the sigmoid is just <code>1 / (1 + np.exp(-z))</code>."),

"f0-log": plain(
  "The undo button for exponentials. “What power did I raise e to, to get this number?”",
  [("log", "“log”", "in ML always the natural log, base e, unless it says otherwise"),
   ("ln", "“ell-en”", "the same thing. Older books and calculators use this"),
   ("log₂", "“log base two”", "used for entropy, so answers come out in “bits”"),
   ("−log(p)", "“minus log p”", "small p → big penalty. This IS the loss function")],
  "In code: <code>np.log(p)</code>. −log(1) = 0 and −log(0.01) = 4.6."),

"f0-prob-rules": plain(
  "A probability is between 0 (never) and 1 (certain). Three balls out of ten are red, so P(red) = 0.3.",
  [("P(A)", "“P of A”", "the probability that A happens"),
   ("|", "“given”", "the vertical bar. P(y=1 | x) = “given that we saw x”"),
   ("independent", "“in-de-PEN-dent”", "one does not affect the other. Two coin flips are")],
  "In code, a probability estimated from data is just a mean: <code>y.mean()</code>."),

"f0-variance": plain(
  "Two questions about any pile of numbers: where is the middle, and how spread out are they? "
  "[9,10,11] and [1,10,19] have the same middle and are nothing alike.",
  [("μ", "“mu”, rhymes with few", "the mean — the plain average"),
   ("σ", "“sigma”", "the standard deviation — the typical distance from the middle"),
   ("σ²", "“sigma squared”", "the variance. Sigma is its square root"),
   ("deviation", "—", "how far one value sits from the mean. Can be negative")],
  "In code: <code>x.mean()</code>, <code>x.var()</code>, <code>x.std()</code>."),

"f0-normal": plain(
  "Measure a thousand people's heights and you get a hill: lots in the middle, few at the edges. Two "
  "numbers describe it completely.",
  [("μ", "“mu”", "where the top of the hill sits"),
   ("σ", "“sigma”", "how wide the hill is"),
   ("density", "“DEN-sity”", "the height of the curve. NOT a probability — it can exceed 1"),
   ("3-sigma event", "—", "something in the outer 0.3%. That is where the phrase comes from")],
  "In code: <code>np.random.normal(mu, sigma, size)</code> draws samples from it."),

"f0-argmax": plain(
  "Scores: 12, 31, 7. “max” asks what the biggest score is — 31. “argmax” asks where it is — position 1. "
  "One gives the value, the other the place.",
  [("max", "“max”", "the biggest VALUE"),
   ("argmax", "“arg max”", "the POSITION of the biggest"),
   ("arg", "“argument”", "in maths, “the input”. So argmax = “the input that maximises it”")],
  "In code: <code>np.argmax(probs, axis=1)</code> — which class won, for each row."),

"f0-list-vs-array": plain(
  "Both use square brackets. A list is a general container (so + means “join”); an array is a maths object "
  "(so + means “add the numbers”). Python warns you about neither.",
  [("list", "“a Python list”", "[1,2,3]. Can hold anything. * repeats it"),
   ("array", "“a NumPy array”", "np.array([1,2,3]). All one type. * doubles each"),
   ("np.array(x)", "—", "the conversion. The fix for the whole category of confusion")],
  "The difference is memory: a list holds pointers to scattered objects; an array holds raw numbers in one "
  "solid block. That layout is where the speed comes from."),

"f0-slicing": plain(
  "Square brackets ask for an address. The first thing lives at 0, not 1 — that feels wrong for about a "
  "week and then becomes invisible.",
  [("x[0]", "“x sub zero”", "the FIRST one"),
   ("x[-1]", "“x minus one”", "the LAST one. Minus counts back from the end"),
   ("x[1:4]", "“one to four”", "positions 1, 2, 3. STOPS BEFORE 4"),
   (":", "“colon”", "alone it means “everything in this direction”"),
   ("M[:, 2]", "“all rows, column two”", "the 2-D version. Used constantly in Course 2")],
  "In Course 2 you will write <code>W[:, j]</code> to grab neuron j's weights — a dense layer stores one "
  "neuron per column."),

"f0-axis": plain(
  "Which direction to work in. Axis 0 goes down the rows; axis 1 goes across the columns.",
  [("axis=0", "“axis zero”", "collapse DOWN → one answer per COLUMN"),
   ("axis=1", "“axis one”", "collapse ACROSS → one answer per ROW"),
   ("no axis", "—", "collapse everything to a single number"),
   ("shape", "—", "(rows, columns). The named axis vanishes from it")],
  "Say the sentence out loud: “one number per feature” → axis=0. “One per example” → axis=1."),

"f0-broadcast": plain(
  "You have a table with 1000 rows and one row of numbers to add to all of them. The shapes do not match "
  "and NumPy does it anyway, by stretching the smaller one.",
  [("broadcasting", "“BROAD-casting”", "quietly stretching a smaller array to fit a bigger one"),
   ("from the right", "—", "how the shapes are lined up. Not from the left"),
   ("one of them is 1", "—", "the condition for stretching to be allowed")],
  "Nothing is really copied in memory, which is why it is free. In code this is why "
  "<code>np.matmul(A, W) + b</code> works with b as a single row."),

"f0-star-vs-at": plain(
  "Two things both called “multiply”. One keeps the numbers separate; the other adds them all up at the end.",
  [("*", "“star”", "elementwise. Pairs them up, keeps them separate → a LIST"),
   ("@", "“at”", "dot / matrix multiply. Pairs, multiplies AND adds → collapses"),
   ("np.dot", "“numpy dot”", "same as @ for vectors; behaves oddly past 2-D. Prefer @")],
  "Dangerous because on two square matrices both run, both give the same shape, and only one is correct."),

"f0-mask": plain(
  "Ask a question of a whole array — “which are bigger than 25?” — and get back a whole array of yes/no "
  "answers. Put that in the brackets and you keep only the yesses.",
  [("mask", "“a mask”", "an array of True/False, same length as your data"),
   ("True = 1", "—", "which is why .sum() counts and .mean() gives a fraction"),
   ("&", "“and”", "combine masks. NOT the word 'and' — that fails on arrays"),
   ("|", "“or”", "the other combiner. Each condition needs its own brackets")],
  "<code>(preds == y).mean()</code> is accuracy in one line."),

"f0-reshape": plain(
  "Twelve numbers can be read as 3 rows of 4, or 4 rows of 3, or one long row. The numbers never move; "
  "only how you read them changes.",
  [("reshape(3,4)", "“reshape three by four”", "re-cut into that grid. Must total the same"),
   ("-1", "“minus one”", "“work this dimension out for me”"),
   ("flatten()", "“flatten”", "squash everything back to 1-D"),
   (".T", "“transpose”", "a DIFFERENT thing — mirrors positions rather than re-cutting")],
  "<code>reshape(1, -1)</code> is the fix when Keras complains that it wants 2-D."),

"f0-pandas-five": plain(
  "pandas knows about column NAMES; NumPy knows about positions. pandas is for loading and tidying; NumPy "
  "is for the maths.",
  [("DataFrame", "“data frame”", "a spreadsheet: named columns, an indexed set of rows"),
   ("Series", "“series”", "one column on its own, with its index attached"),
   ("df.info()", "—", "types and missing values. The one that catches the classic bug"),
   ("dtype object", "—", "means TEXT. A numeric column that arrived as strings")],
  "Run head(), info() and describe() on every dataset before modelling anything."),

"f0-to-numpy": plain(
  "The one line that crosses from “loading data” to “doing maths”. You lose the column names, so pick your "
  "columns before crossing.",
  [(".to_numpy()", "“to numpy”", "the modern spelling"),
   (".values", "“values”", "the older spelling you will see in old notebooks. Same thing"),
   ("X", "“capital X”", "conventionally your features — 2-D, shape (m, n)"),
   ("y", "“lowercase y”", "conventionally your target — 1-D, shape (m,)")],
  "Single brackets give (m,); double brackets give (m,1). Libraries want y as (m,)."),

"f0-traceback": plain(
  "A wall of red text where almost nothing matters. The last line is a plain English sentence naming the "
  "actual problem.",
  [("traceback", "“TRACE-back”", "the chain of function calls that led to the failure"),
   ("the last line", "—", "the error type and what went wrong. Read this FIRST"),
   ("the middle lines", "—", "just how the code got there. Ignorable at first"),
   ("bisecting", "—", "splitting a long line in half and printing, to find where it breaks")],
  "Two habits fix most errors: print the shapes, and print the types."),

"f0-five-errors": plain(
  "The same handful of errors will account for nearly everything that goes wrong in the labs. Recognising "
  "them on sight saves hours.",
  [("ValueError", "“value error”", "usually shapes that do not line up"),
   ("IndexError", "“index error”", "you asked for a position that does not exist"),
   ("TypeError", "“type error”", "an operation that does not make sense for that kind of thing"),
   ("NameError", "“name error”", "a typo, or an import cell you never ran"),
   ("KeyError", "“key error”", "a column name that is not in the DataFrame")],
  "Each one names the problem precisely. Read it before searching the internet."),

"f0-function-read": plain(
  "A recipe with a name. You give it ingredients, it does some steps, and it hands you back a result.",
  [("def", "“def”", "“I am defining a function”"),
   ("parameters", "“pa-RAM-eters”", "what it needs, in the brackets. Matched IN ORDER"),
   (":", "“colon”", "starts the body. The indent below is what belongs to it"),
   ("return", "“return”", "hands one value back. Without it you get None"),
   ("indentation", "—", "not decoration — it is what defines the body in Python")],
  "Every graded exercise is “fill in the body of this function”, so reading a signature is the core skill."),

"f0-drill-dotprod": plain(
  "Two lists of the same length. Pair up the numbers in the same position, multiply each pair, "
  "then add all the answers together. One number comes out the other end.",
  [("a·b", "“a dot b”", "the dot product — pair, multiply, add"),
   ("4, 10, 18", "—", "the three pairwise products, before adding")],
  "Like a receipt: 4 apples at £1 each, plus 5 pears at £2 each — you add the LINE TOTALS, not the "
  "quantities or the prices alone."),

"f0-eigen": plain(
  "Multiplying by a matrix usually turns a vector AND stretches it. A few special directions do not "
  "get turned at all — they only get longer or shorter. Those are the eigenvectors.",
  [("A", "“the matrix”", "the transformation being applied"),
   ("v", "“an eigenvector”", "a direction the matrix leaves pointing the same way"),
   ("λ", "“lambda”", "the eigenvalue — how much that direction gets stretched")],
  "Like stretching a rubber sheet: most arrows drawn on it swing round, but the ones along the pull do not."),

"f0-pca-why": plain(
  "PCA wants the direction the data spreads out most along. That is exactly what the biggest "
  "eigenvector of the covariance matrix is — the eigenvalue IS the spread along it.",
  [("covariance matrix", "—", "a small grid describing how the data is spread out"),
   ("principal component", "—", "one of those special directions, biggest first"),
   ("98.7%", "—", "4.976 ÷ (4.976 + 0.064) — how much spread the first one keeps")],
  "This is the sentence Course 3 asked you to accept without explanation."),

"f0-svd": plain(
  "Any grid of numbers at all can be pulled apart into three simple steps: turn, stretch, turn. The "
  "stretches come out sorted biggest first, so you can drop the small ones to compress it.",
  [("U, V", "“U and V”", "the two turning steps"),
   ("Σ", "“sigma”", "the stretching amounts, always sorted largest first"),
   ("rank-k", "“rank k”", "keeping only the k biggest stretches")],
  "A stack of transparencies ordered by importance: keep the first few, discard the rest."),

"f0-mle": plain(
  "Instead of asking “how wrong is my model”, ask “if my model were right, how likely was the data I "
  "actually saw?” Then pick whatever makes the data most likely.",
  [("likelihood", "“likelihood”", "how probable the observed data is, for a given guess"),
   ("−log", "“negative log”", "makes multiplying into adding, and stops tiny numbers vanishing"),
   ("MLE", "“M-L-E”", "maximum likelihood estimate — the guess at the peak")],
  "A detective asking which suspect makes the evidence least surprising, rather than who looks guilty."),

"f0-jacobian": plain(
  "With one input and one output a derivative is one number. With several of each you need one number "
  "per pair — arranged in a grid, with outputs down the side and inputs across the top.",
  [("J", "“the Jacobian”", "the grid of all the partial derivatives"),
   ("∂fᵢ/∂xⱼ", "“partial f-i by partial x-j”", "how much output i moves when input j is nudged"),
   ("(m, n)", "—", "m outputs, n inputs — the shape tells you the function's signature")],
  "A mixing desk: three sliders, two speakers, six answers, laid out as a table."),

"f0-softmax-grad": plain(
  "Softmax has an awkward derivative and the log has another. Put them together and both messes "
  "cancel exactly, leaving “what you predicted minus what was true”. One subtraction.",
  [("p", "“p”", "the predicted probabilities, from softmax"),
   ("y", "“y”", "the true answer, as a 1 in the right slot and 0s elsewhere"),
   ("p − y", "—", "the whole gradient. Negative for the true class, positive for the rest")],
  "Two awkward gear ratios that happen to be reciprocals — in series they turn cleanly 1:1."),
}
