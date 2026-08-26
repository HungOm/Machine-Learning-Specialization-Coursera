# -*- coding: utf-8 -*-
"""Quick-refresher badges for library calls, INSIDE code blocks.

content_f0ref.py and content_courseref.py badge prose — the explanatory text
around a formula or a concept. This module is for the other place notation
hides: the actual NumPy / TensorFlow calls inside a code() block, which the
site's normal badge_terms() pass explicitly skips (code should read as code,
not get badges sprinkled through arbitrary identifiers).

badge_api_calls() in build.py runs this same PATTERNS/TERMS machinery a
second time, scoped to just the inside of <code>...</code>, so hovering
np.dot in an actual snippet works the same way hovering "dot product" in a
paragraph does.

Coverage is deliberately narrow: every entry below was chosen because the
call appears at least half a dozen times across the lesson content (checked
against the built site, not guessed), so the badge earns its keep.
"""

ANCHOR = "apiref"

F0W1 = "f0/w1-%s.html"
F0W2 = "f0/w2-%s.html"
C2 = "c2/w%s-%s.html"

PATTERNS = [
    (r"np\.array\b", "nparray-api"),
    (r"np\.zeros\b|np\.ones\b", "npcreate-api"),
    (r"np\.arange\b|np\.linspace\b", "nprange-api"),
    (r"np\.dot\b|np\.matmul\b", "npdot-api"),
    (r"np\.sum\b", "npsum-api"),
    (r"np\.log\b", "nplog-api"),
    (r"np\.exp\b", "npexp-api"),
    (r"np\.argmax\b", "npargmax-api"),
    (r"model\.compile\b", "tfcompile-api"),
    (r"model\.fit\b", "tffit-api"),
    (r"model\.predict\b", "tfpredict-api"),
    (r"\bDense\b", "dense-api"),
    (r"\bSequential\b", "sequential-api"),
    (r"\bAdam\b", "adam-api"),
    (r"pd\.DataFrame\b", "pddataframe-api"),
]

TERMS = [
 dict(key="nparray-api", label="np.array(...)", say="“numpy dot array”",
      gist="Turns an ordinary Python list into a NumPy array — the type every other NumPy "
           "function expects.",
      body="<div class='gq'>np.array([1, 2, 3])</div>"
           "<p>Looks similar to a list but behaves completely differently: arithmetic runs "
           "elementwise, and every entry must be the same type.</p>",
      ml="Almost every code() block on this site starts by wrapping the data in np.array — it's "
         "the entry point into everything NumPy does.",
      more_href=F0W2 % "03-lists-vs-arrays", more_label="F0 W2 · Lists vs. NumPy arrays"),

 dict(key="npcreate-api", label="np.zeros / np.ones", say="“numpy zeros”, “numpy ones”",
      gist="Build a new array of a given <b>shape</b>, filled with 0s or 1s — a starting point "
           "you then fill in, rather than typing every value by hand.",
      body="<div class='gq'>np.zeros(3) &nbsp;→&nbsp; [0., 0., 0.]</div>"
           "<p>The argument is the <b>shape</b> you want, not the values. <code>np.zeros((2,3))</code> "
           "makes a 2×3 matrix of zeros, not a 2-element array.</p>",
      ml="The standard way to pre-allocate an output array before filling it in a loop — "
         "<code>compute_model_output</code> in C1 W1 does exactly this.",
      more_href=F0W2 % "06-creating-arrays", more_label="F0 W2 · Creating arrays"),

 dict(key="nprange-api", label="np.arange / np.linspace", say="“numpy a-range”",
      gist="Generate an evenly spaced array of numbers, without writing them out by hand.",
      body="<div class='gq'>np.arange(5) &nbsp;→&nbsp; [0, 1, 2, 3, 4]</div>"
           "<p><code>np.arange</code> steps by a fixed amount; <code>np.linspace</code> instead "
           "fixes how many points you want and spaces them evenly between two endpoints.</p>",
      ml="Used constantly to build the x-axis for a plot, or a sweep of test values for a "
         "parameter like α.",
      more_href=F0W2 % "06-creating-arrays", more_label="F0 W2 · Creating arrays"),

 dict(key="npdot-api", label="np.dot / np.matmul", say="“numpy dot”",
      gist="The code form of the dot product and matrix multiplication — one call instead of a "
           "loop.",
      body="<p><code>np.dot</code> handles both a plain vector·vector dot product and a full "
           "matrix multiply, depending on the shapes you give it. <code>@</code> is shorthand for "
           "the same operation: <code>A @ B</code> is <code>np.matmul(A, B)</code>.</p>",
      ml="This single call is what replaces the explicit for-loop version of a neural network "
         "layer — same maths, no Python loop.",
      more_href=F0W2 % "09-dot-in-code", more_label="F0 W2 · np.dot, matmul and @"),

 dict(key="npsum-api", label="np.sum(...)", say="“numpy sum”",
      gist="Adds up every entry of an array — the code form of Σ.",
      body="<div class='gq'>np.sum([1, 2, 3]) &nbsp;→&nbsp; 6</div>"
           "<p>Pass <code>axis=0</code> to sum down each column instead of collapsing the whole "
           "array to one number — the difference matters constantly once data is 2-D.</p>",
      ml="Every cost function on this site is, underneath, one np.sum call over the squared or "
         "logged errors.",
      more_href=F0W2 % "10-aggregations", more_label="F0 W2 · sum, mean, max — along an axis"),

 dict(key="nplog-api", label="np.log(...)", say="“numpy log”",
      gist="The natural logarithm, applied to every entry of an array at once.",
      body="<p>Same function as the log in a log-loss formula — <code>np.log</code> just runs it "
           "elementwise across a whole array instead of one number.</p>"
           "<div class='gq'>np.log(0) &nbsp;→&nbsp; -inf, with a RuntimeWarning</div>",
      ml="Feeding it exactly 0 is the single most common source of NaN in this course's loss "
         "computations — see the “log(0) in code” trap wherever log loss appears.",
      more_href=F0W1 % "15-logarithms", more_label="F0 W1 · Logarithms"),

 dict(key="npexp-api", label="np.exp(...)", say="“numpy exp”",
      gist="Raises e to the power of every entry of an array at once.",
      body="<div class='gq'>np.exp([0, 1]) &nbsp;→&nbsp; [1., 2.718...]</div>",
      ml="The sigmoid function is exactly <code>1 / (1 + np.exp(-z))</code> — this one call is "
         "the entire “squashing” step of logistic regression and every neural network activation.",
      more_href=F0W1 % "14-exponentials", more_label="F0 W1 · Exponentials and e"),

 dict(key="npargmax-api", label="np.argmax(...)", say="“numpy arg-max”",
      gist="Which position holds the largest value — not the value itself.",
      body="<div class='gq'>np.argmax([0.1, 0.7, 0.2]) &nbsp;→&nbsp; 1</div>"
           "<p>Pass <code>axis=1</code> on a 2-D array of predictions to get one winning class "
           "per row, instead of one number for the whole array.</p>",
      ml="Turning softmax's probabilities into an actual predicted class is exactly this one call.",
      more_href=F0W1 % "19-min-max-argmax", more_label="F0 W1 · min, max, argmin and argmax"),

 dict(key="tfcompile-api", label="model.compile(...)", say="“compile”",
      gist="Tells the model <b>how</b> to train — which loss function, which optimizer — before "
           "any training happens.",
      body="<p>Nothing is computed here. This just configures the training run that "
           "<code>model.fit</code> is about to do.</p>",
      ml="The loss you pass here (<code>BinaryCrossentropy</code>, "
         "<code>SparseCategoricalCrossentropy</code>...) is the actual cost function from the maths, "
         "by another name.",
      more_href=C2 % (2, "01-tensorflow-training"),
      more_label="C2 W2 · TensorFlow implementation of training"),

 dict(key="tffit-api", label="model.fit(...)", say="“fit”",
      gist="Runs gradient descent — this is the line that actually trains the model.",
      body="<div class='gq'>model.fit(X, Y, epochs=100)</div>"
           "<p>Everything Course 1 built by hand — the loop, the gradient, the update rule — "
           "happens inside this one call.</p>",
      ml="\"epochs\" is how many full passes over the training set to run; too few and it hasn't "
         "learned, too many and it starts memorising.",
      more_href=C2 % (2, "01-tensorflow-training"),
      more_label="C2 W2 · TensorFlow implementation of training"),

 dict(key="tfpredict-api", label="model.predict(...)", say="“predict”",
      gist="Runs the trained model forward on new data — inference, not training.",
      body="<p>No gradients, no learning, nothing changes about the model. Just: take these "
           "inputs, run forward propagation, return the outputs.</p>",
      ml="This is the “using” half of a model, as opposed to fit's “learning” half.",
      more_href=C2 % (2, "01-tensorflow-training"),
      more_label="C2 W2 · TensorFlow implementation of training"),

 dict(key="dense-api", label="Dense(...)", say="“dense layer”",
      gist="One fully-connected layer — every unit sees every input.",
      body="<div class='gq'>Dense(units=25, activation='relu')</div>"
           "<p>“Dense” is the contrast with layer types (like a convolution) where each unit only "
           "sees part of the input.</p>",
      ml="units is how many neurons are in the layer; activation is which non-linearity g each "
         "one applies.",
      more_href="c2/w1-09-building-a-network-sequential.html",
      more_label="C2 W1 · Building a neural network (Sequential)"),

 dict(key="sequential-api", label="Sequential([...])", say="“sequential”",
      gist="Stacks layers in a straight line — output of one layer feeds straight into the next.",
      body="<p>Covers the large majority of networks in this specialization. It cannot handle a "
           "network with more than one input, more than one output, or a layer that skips ahead — "
           "those need the more general functional API.</p>",
      ml="This one call replaces writing out forward propagation by hand, layer by layer.",
      more_href="c2/w1-09-building-a-network-sequential.html",
      more_label="C2 W1 · Building a neural network (Sequential)"),

 dict(key="adam-api", label="Adam(...)", say="“Adam”",
      gist="An optimizer that gives every parameter its <b>own</b> effective learning rate, "
           "adjusted automatically as training goes.",
      body="<p>Short for Adaptive Moment estimation. Where plain gradient descent uses one α for "
           "every parameter, Adam speeds up parameters that keep moving the same direction and "
           "slows down ones that are oscillating.</p>",
      ml="The default choice for training a neural network in practice — plain gradient descent "
         "is what Course 1 teaches by hand, Adam is what real code almost always uses.",
      more_href=C2 % (2, "11-advanced-optimization"),
      more_label="C2 W2 · Advanced optimization (Adam)"),

 dict(key="pddataframe-api", label="pd.DataFrame(...)", say="“pandas dataframe”",
      gist="A labelled table — rows and named columns — built on top of NumPy.",
      body="<div class='gq'>df['price'] &nbsp;→&nbsp; one named column, as a pandas Series</div>"
           "<p>Convenient for reading and inspecting data by column name. Convert to a plain "
           "NumPy array with <code>.to_numpy()</code> before doing maths on it.</p>",
      ml="Most real datasets arrive as a DataFrame (from a CSV); the model itself always still "
         "wants plain NumPy arrays.",
      more_href=F0W2 % "13-pandas-dataframes", more_label="F0 W2 · pandas DataFrames"),
]
