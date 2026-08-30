# -*- coding: utf-8 -*-
"""Quick-refresher badges for library calls, INSIDE code blocks.

content_f0ref.py and content_courseref.py badge prose — the explanatory text
around a formula or a concept. This module is for the other place notation
hides: the actual NumPy / TensorFlow / pandas / scikit-learn calls inside a
code() block, which the site's normal badge_terms() pass explicitly skips
(code should read as code, not get badges sprinkled through arbitrary
identifiers).

badge_api_calls() in build.py runs this same PATTERNS/TERMS machinery a
second time, scoped to just the inside of <code>...</code>, so hovering
np.dot in an actual snippet works the same way hovering "dot product" in a
paragraph does.

Coverage: every distinct NumPy, TensorFlow/Keras, pandas and scikit-learn
call that appears anywhere in a code() block on the site, audited against
the built pages rather than guessed. Every occurrence gets the badge, not
just the first per page — repetition is the point, not a cost, for a call
you are trying to make second nature.

Several entries deliberately cover more than one spelling of the same idea
(np.dot and np.matmul; Dense and tf.keras.layers.Dense; a bare .mean() call
on any array and the equivalent np.mean(x)) — the site teaches both forms
in different places, and they should open the identical explanation.
"""

ANCHOR = "apiref"

F0W1 = "f0/w1-%s.html"
F0W2 = "f0/w2-%s.html"
C1 = "c1/w%s-%s.html"
C2 = "c2/w%s-%s.html"
C3 = "c3/w%s-%s.html"

PATTERNS = [
    (r"np\.array\b", "nparray-api"),
    (r"np\.zeros\b|np\.ones\b|np\.full\b", "npcreate-api"),
    (r"np\.arange\b|np\.linspace\b", "nprange-api"),
    (r"np\.dot\b|np\.matmul\b|tf\.linalg\.matmul\b", "npdot-api"),
    (r"np\.sum\b|\.sum\(", "npsum-api"),
    (r"np\.log\b", "nplog-api"),
    (r"np\.exp\b", "npexp-api"),
    (r"np\.argmax\b|np\.argmin\b", "npargmax-api"),
    (r"model\.compile\b", "tfcompile-api"),
    (r"model\.fit\b", "tffit-api"),
    (r"model\.predict\b", "tfpredict-api"),
    (r"tf\.keras\.layers\.Dense\b|\bDense\b", "dense-api"),
    (r"tf\.keras\.models\.Sequential\b|\bSequential\b", "sequential-api"),
    (r"tf\.keras\.optimizers\.Adam\b|keras\.optimizers\.Adam\b|\bAdam\b", "adam-api"),
    (r"pd\.DataFrame\b", "pddataframe-api"),

    (r"np\.mean\b|\.mean\(", "npmean-api"),
    (r"np\.std\b|\.std\(", "npstd-api"),
    (r"np\.var\b|\.var\(", "npvar-api"),
    (r"\.reshape\(", "npreshape-api"),
    (r"np\.sqrt\b", "npsqrt-api"),
    (r"np\.log2\b", "nplog2-api"),
    (r"np\.log10\b", "nplog10-api"),
    (r"np\.prod\b", "npprod-api"),
    (r"np\.linalg\.norm\b", "npnorm-api"),
    (r"np\.max\b|np\.min\b|\.max\(|\.min\(", "npmaxmin-api"),
    (r"np\.random\.rand\b|np\.random\.choice\b|np\.random\.normal\b|np\.random\.permutation\b",
     "nprandom-api"),
    (r"np\.random\.seed\b", "npseed-api"),
    (r"np\.eye\b", "npeye-api"),
    (r"np\.c_\b", "npc-api"),
    (r"np\.polyfit\b", "nppolyfit-api"),
    (r"np\.gradient\b", "npgradient-api"),
    (r"np\.round\b", "npround-api"),

    (r"tf\.keras\.Input\b|tf\.keras\.layers\.Input\b|\bInput\(", "tfinput-api"),
    (r"tf\.GradientTape\b|\.gradient\(", "tftape-api"),
    (r"\.apply_gradients\(", "tfapplygrad-api"),
    (r"tf\.reduce_sum\b|tf\.reduce_max\b", "tfreduce-api"),
    (r"tf\.linalg\.l2_normalize\b", "tfl2norm-api"),
    (r"tf\.transpose\b", "tftranspose-api"),
    (r"\.numpy\(\)", "tfnumpy-api"),
    (r"\.set_weights\(", "tfsetweights-api"),
    (r"\.summary\(\)", "tfsummary-api"),
    (r"BinaryCrossentropy\b|SparseCategoricalCrossentropy\b|MeanSquaredError\b", "tflosses-api"),
    (r"tf\.keras\.regularizers\.l2\b|\bl2\(", "tfl2reg-api"),
    (r"tf\.keras\.Model\b", "tfmodel-api"),
    (r"tf\.keras\.layers\.Dot\b", "tfdot-api"),
    (r"tf\.keras\.layers\.GlobalAveragePooling2D\b", "tfgap-api"),
    (r"tf\.keras\.applications\.MobileNetV2\b", "tfmobilenet-api"),

    (r"pd\.read_csv\b", "pdreadcsv-api"),
    (r"pd\.get_dummies\b", "pdgetdummies-api"),
    (r"\.head\(\)|\.info\(\)|\.describe\(\)|\.isnull\(\)", "pdeda-api"),

    (r"train_test_split\b", "sklearntts-api"),
    (r"precision_recall_curve\b", "sklearnprc-api"),
    (r"\bPCA\(|\.fit_transform\(|\.inverse_transform\(", "sklearnpca-api"),
    (r"RandomForestClassifier\b|XGBClassifier\b|XGBRegressor\b", "sklearnforest-api"),
    (r"\.fit\(", "sklearnfit-api"),

    (r"\baxis\s*=(?!=)", "kwaxis-api"),
    (r"\bactivation\s*=(?!=)", "kwactivation-api"),
    (r"\bunits\s*=(?!=)", "kwunits-api"),
    (r"\bloss\s*=(?!=)", "kwloss-api"),
    (r"\bepochs\s*=(?!=)", "kwepochs-api"),
    (r"\bshape\s*=(?!=)", "kwshape-api"),
    (r"\bname\s*=(?!=)", "kwname-api"),
    (r"\bdtype\s*=(?!=)", "kwdtype-api"),
    (r"\boptimizer\s*=(?!=)", "kwoptimizer-api"),
    (r"\blearning_rate\s*=(?!=)", "kwlr-api"),
    (r"\bkernel_regularizer\s*=(?!=)", "kwkreg-api"),
    (r"\bfrom_logits\s*=(?!=)", "kwfromlogits-api"),
    (r"\btest_size\s*=(?!=)", "kwtestsize-api"),
    (r"\brandom_state\s*=(?!=)", "kwrandomstate-api"),
    (r"\bdegree\s*=(?!=)", "kwdegree-api"),
    (r"\bn_estimators\s*=(?!=)", "kwnestimators-api"),
    (r"\breplace\s*=(?!=)", "kwreplace-api"),
    (r"\bsize\s*=(?!=)", "kwsize-api"),
    (r"\bweights\s*=(?!=)", "kwweights-api"),
    (r"\bn_components\s*=(?!=)", "kwncomponents-api"),
    (r"\binput_shape\s*=(?!=)", "kwinputshape-api"),
    (r"\binclude_top\s*=(?!=)", "kwincludetop-api"),
    (r"\bcolumns\s*=(?!=)", "kwcolumns-api"),
    (r"\bcolor\s*=(?!=)|\blw\s*=(?!=)|\blabel\s*=(?!=)", "kwplotstyle-api"),
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

 dict(key="npcreate-api", label="np.zeros / np.ones / np.full", say="“numpy zeros”, “numpy ones”, “numpy full”",
      gist="Build a new array of a given <b>shape</b>, pre-filled with a constant — a starting "
           "point you then fill in, rather than typing every value by hand.",
      body="<div class='gq'>np.zeros(3) → [0., 0., 0.]  ·  np.full((2,2), 7) → every entry 7</div>"
           "<p>The argument is the <b>shape</b> you want, not the values. <code>np.zeros((2,3))</code> "
           "makes a 2×3 matrix of zeros, not a 2-element array. <code>np.full</code> is the same "
           "idea when the fill value is not 0 or 1.</p>",
      ml="The standard way to pre-allocate an output array before filling it in a loop — "
         "<code>compute_model_output</code> in C1 W1 does exactly this.",
      more_href=F0W2 % "06-creating-arrays", more_label="F0 W2 · Creating arrays"),

 dict(key="nprange-api", label="np.arange / np.linspace", say="“numpy a-range”",
      gist="Generate an evenly spaced array of numbers, without writing them out by hand.",
      body="<div class='gq'>np.arange(5) → [0, 1, 2, 3, 4]</div>"
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
           "the same operation: <code>A @ B</code> is <code>np.matmul(A, B)</code>. TensorFlow's "
           "own <code>tf.linalg.matmul</code> is the identical operation on a tensor.</p>"
           "<div class='gq'>np.dot([1,2,3], [4,5,6]) → 32</div><p>4 + 10 + 18. Same as <code>a @ b</code>. Note <code>a * b</code> gives <code>[4,10,18]</code> instead — the products without the summing.</p>",
      ml="This one operation underlies every layer in every neural network on this site.",
      more_href=F0W1 % "10-dot-product", more_label="F0 W1 · The dot product"),

 dict(key="npsum-api", label="np.sum(...) / x.sum()", say="“numpy sum”",
      gist="Adds up every element of an array — the code form of the Σ you keep seeing in a "
           "formula.",
      body="<div class='gq'>np.sum([1,2,3]) → 6  ·  X.sum(axis=0) → one total per column</div>"
           "<p>Callable two ways that mean the same thing: <code>np.sum(x)</code> and "
           "<code>x.sum()</code>. The <code>axis</code> argument is the one to watch — "
           "<code>axis=0</code> collapses the rows, leaving one number per column.</p>",
      ml="Every cost function on this site — mean squared error, cross-entropy, entropy itself — "
         "ends with a sum over examples, usually written this way.",
      more_href=F0W1 % "07-sigma-notation", more_label="F0 W1 · Sigma notation"),

 dict(key="nplog-api", label="np.log(...)", say="“numpy log”",
      gist="The <b>natural</b> logarithm — base e, not base 10.",
      body="<div class='gq'>np.log(1) → 0.0   np.log(np.e) → 1.0</div>"
           "<p>This is the log used in every cost function on this site (cross-entropy, log loss). "
           "<code>np.log2</code> and <code>np.log10</code> exist separately for the rarer cases "
           "that need a different base — entropy is the one place base 2 matters here.</p>",
      ml="If you ever see log(0) blow up to −∞ in your own code, that is why every loss function "
         "clips or guards against a probability of exactly 0.",
      more_href=F0W1 % "15-logarithms", more_label="F0 W1 · Logarithms"),

 dict(key="npexp-api", label="np.exp(...)", say="“numpy e-x-p”",
      gist="Raises e (≈2.718) to the power of every element — the building block of sigmoid, "
           "softmax and the Gaussian density.",
      body="<div class='gq'>np.exp(0) → 1.0   np.exp(1) → 2.718...</div>"
           "<p>Grows fast and is always positive, which is exactly why it appears in every "
           "function that needs to turn an unbounded score into something that behaves like a "
           "probability.</p>",
      ml="sigmoid, softmax and the Gaussian probability density are all built from this one call.",
      more_href=F0W1 % "14-exponentials", more_label="F0 W1 · Exponentials"),

 dict(key="npargmax-api", label="np.argmax / np.argmin", say="“arg-max”, “arg-min”",
      gist="Returns the <b>position</b> of the largest (or smallest) value — not the value "
           "itself.",
      body="<div class='gq'>x = [12, 31, 7]   np.argmax(x) → 1   (the value is x[1] = 31)</div>"
           "<p>Easy to confuse with <code>np.max</code>, which returns the value 31, not its "
           "index 1. Reading off a prediction from a softmax output is always argmax, never max.</p>",
      ml="How you turn a softmax's 10 probabilities into a single predicted digit: "
         "<code>np.argmax(probabilities)</code>.",
      more_href=F0W1 % "19-min-max-argmax", more_label="F0 W1 · Min, max, argmax"),

 dict(key="tfcompile-api", label="model.compile(...)", say="“compile”",
      gist="Tells Keras which loss function and optimizer to use — configuration, no data "
           "touched yet.",
      body="<div class='gq'>model.compile(loss=BinaryCrossentropy(), optimizer=Adam(1e-3))</div>"
           "<p>Nothing is computed here. This just wires up what <code>model.fit</code> will "
           "later use to measure error and to update the weights.</p>",
      ml="The loss you choose here is the single place a model's problem type (regression, "
         "binary, multiclass) gets encoded.",
      more_href=C2 % (2, "01-tensorflow-training"),
      more_label="C2 W2 · TensorFlow implementation of training"),

 dict(key="tffit-api", label="model.fit(...)", say="“fit”",
      gist="Runs gradient descent — the actual training. Everything before this line was setup.",
      body="<div class='gq'>model.fit(X, y, epochs=100)</div>"
           "<p><code>epochs</code> is how many times the whole training set is passed through. "
           "This one call replaces the gradient-descent loop you wrote by hand in Course 1.</p>",
      ml="This is where backpropagation actually runs — every derivative, computed automatically.",
      more_href=C2 % (2, "01-tensorflow-training"),
      more_label="C2 W2 · TensorFlow implementation of training"),

 dict(key="tfpredict-api", label="model.predict(...)", say="“predict”",
      gist="Runs the trained model forward on new data — inference, not training.",
      body="<p>No gradients, no learning, nothing changes about the model. Just: take these "
           "inputs, run forward propagation, return the outputs.</p>"
           "<div class='gq'>model.predict(X) → array of shape (m, 1)</div><p>One output per row you passed in. No gradients, no learning — the weights are untouched.</p>",
      ml="This is the “using” half of a model, as opposed to fit's “learning” half.",
      more_href=C2 % (2, "01-tensorflow-training"),
      more_label="C2 W2 · TensorFlow implementation of training"),

 dict(key="dense-api", label="Dense(...)", say="“dense layer”",
      gist="One fully-connected layer — every unit sees every input.",
      body="<div class='gq'>Dense(units=25, activation='relu')</div>"
           "<p>“Dense” is the contrast with layer types (like a convolution) where each unit only "
           "sees part of the input. Sometimes written out in full as "
           "<code>tf.keras.layers.Dense</code> — same call.</p>",
      ml="units is how many neurons are in the layer; activation is which non-linearity g each "
         "one applies.",
      more_href="c2/w1-09-building-a-network-sequential.html",
      more_label="C2 W1 · Building a neural network (Sequential)"),

 dict(key="sequential-api", label="Sequential([...])", say="“sequential”",
      gist="Stacks layers in a straight line — output of one layer feeds straight into the next.",
      body="<p>Covers the large majority of networks in this specialization. It cannot handle a "
           "network with more than one input, more than one output, or a layer that skips ahead — "
           "those need the more general functional API (<code>tf.keras.Model</code>). Sometimes "
           "written in full as <code>tf.keras.models.Sequential</code> — same call.</p>"
           "<div class='gq'>Sequential([Dense(25, 'relu'), Dense(15, 'relu'), Dense(1, 'sigmoid')])</div><p>Three layers, output straight into the next. That one call replaces writing forward propagation by hand.</p>",
      ml="This one call replaces writing out forward propagation by hand, layer by layer.",
      more_href="c2/w1-09-building-a-network-sequential.html",
      more_label="C2 W1 · Building a neural network (Sequential)"),

 dict(key="adam-api", label="Adam(...)", say="“Adam”",
      gist="An optimizer that gives every parameter its <b>own</b> effective learning rate, "
           "adjusted automatically as training goes.",
      body="<p>Short for Adaptive Moment estimation. Where plain gradient descent uses one α for "
           "every parameter, Adam speeds up parameters that keep moving the same direction and "
           "slows down ones that are oscillating. Sometimes written as "
           "<code>tf.keras.optimizers.Adam</code> — same call.</p>"
           "<div class='gq'>model.compile(optimizer=Adam(learning_rate=1e-3), loss=…)</div><p>The α you pass is a starting point, not a fixed step — Adam scales it per parameter as it goes.</p>",
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

 dict(key="npmean-api", label="np.mean(x) / x.mean()", say="“numpy mean”",
      gist="The average of every element — same call whether you write it as a function or a "
           "method.",
      body="<div class='gq'>np.mean([2,4,6]) → 4.0   ≡   np.array([2,4,6]).mean()</div>"
           "<p>With <code>axis=0</code> it averages down the columns — one mean per feature, "
           "which is exactly what feature scaling and anomaly detection's Gaussian both need.</p>",
      ml="mu = X.mean(axis=0) is the single most common line in every normalisation and anomaly-"
         "detection snippet on this site.",
      more_href=F0W1 % "17-mean-variance", more_label="F0 W1 · Mean and variance"),

 dict(key="npstd-api", label="np.std(x) / x.std()", say="“numpy standard deviation”",
      gist="How spread out the values are — the square root of the variance.",
      body="<div class='gq'>(X - X.mean()) / X.std()   # z-score</div>"
           "<p>Almost always seen paired with <code>.mean()</code> in exactly this pattern: "
           "subtract the mean, divide by the standard deviation.</p>",
      ml="This is the z-score / standardisation from feature scaling, written out in full.",
      more_href=F0W1 % "17-mean-variance", more_label="F0 W1 · Mean and variance"),

 dict(key="npvar-api", label="np.var(x) / x.var()", say="“numpy variance”",
      gist="The average <b>squared</b> distance from the mean — variance, not standard "
           "deviation (no square root taken).",
      body="<div class='gq'>var = std ** 2   (they are the same quantity, one square-rooted)</div>"
           "<p>Anomaly detection's Gaussian model is fitted with exactly two calls: "
           "<code>mu = X.mean(axis=0)</code>, <code>var = X.var(axis=0)</code>.</p>",
      ml="Regression trees use this same call to measure impurity for a numeric target, in place "
         "of entropy.",
      more_href=F0W1 % "17-mean-variance", more_label="F0 W1 · Mean and variance"),

 dict(key="npreshape-api", label="x.reshape(...)", say="“reshape”",
      gist="Rearranges the same numbers into a different shape — never changes the values or "
           "their order.",
      body="<div class='gq'>x.reshape(-1, 1)   # turn a flat list into a column</div>"
           "<p>The <code>-1</code> means “work this dimension out for me”. This exact call is "
           "how you turn one example into the 2-D shape <code>model.predict</code> always "
           "expects.</p>",
      ml="X[i].reshape(1, 400) is how a single digit image is fed to the Week 1 assignment's model.",
      more_href=F0W2 % "12-reshape", more_label="F0 W2 · Reshape"),

 dict(key="npsqrt-api", label="np.sqrt(...)", say="“numpy square root”",
      gist="The square root, applied elementwise.",
      body="<div class='gq'>np.sqrt(np.array([4, 9, 16])) → [2., 3., 4.]</div>"
           "<p>Appears constantly inside the Gaussian probability formula and inside Adam's "
           "update rule, both of which divide by a square root.</p>",
      ml="Standard deviation is literally <code>np.sqrt(variance)</code> — the two are the same "
         "idea, one is just rescaled to the original units."),

 dict(key="nplog2-api", label="np.log2(...)", say="“numpy log base 2”",
      gist="Logarithm base 2 — the one entropy is built from, so that its units come out in "
           "bits.",
      body="<div class='gq'>H(p) = -p*np.log2(p) - (1-p)*np.log2(1-p)</div>"
           "<p>Different from plain <code>np.log</code> (base e). The base only changes the "
           "units the answer comes out in, not what the formula means.</p>",
      ml="Every entropy and information-gain calculation in the decision-trees week uses base 2, "
         "specifically so a coin flip's entropy comes out to exactly 1.",
      more_href=C2 % (4, "03-measuring-purity"), more_label="C2 W4 · Measuring purity (entropy)"),

 dict(key="nplog10-api", label="np.log10(...)", say="“numpy log base 10”",
      gist="Logarithm base 10 — mostly useful for reading off orders of magnitude at a glance.",
      body="<div class='gq'>np.log10(1000) → 3.0</div>"
           "<p>Rare on this site; when it shows up it is almost always for a plot's axis, not "
           "for a cost function.</p>",
      ml="If a number's log10 is 3, the number itself is around a thousand — a quick sanity "
         "check when eyeballing a huge or tiny value."),

 dict(key="npprod-api", label="np.prod(...)", say="“numpy product”",
      gist="Multiplies every element together — the code form of the Π (capital pi) you see in "
           "a formula.",
      body="<div class='gq'>np.prod([2, 3, 4]) → 24</div>"
           "<p>With <code>axis=1</code> it multiplies across each row, collapsing several "
           "numbers into one per row.</p>",
      ml="Anomaly detection's p(x) multiplies one Gaussian probability per feature together with "
         "exactly this call: <code>np.prod(p, axis=1)</code>.",
      more_href=C3 % (1, "09-anomaly-detection-algorithm"),
      more_label="C3 W1 · The anomaly detection algorithm"),

 dict(key="npnorm-api", label="np.linalg.norm(...)", say="“numpy linear-algebra norm”",
      gist="The length of a vector — how far it is from the origin.",
      body="<div class='gq'>np.linalg.norm([3, 4]) → 5.0   (3² + 4² = 5²)</div>"
           "<p>Equivalent to <code>np.sqrt(np.sum(x**2))</code>, spelled out as one call. Used "
           "to compare two feature vectors by distance, e.g. finding related movies.</p>",
      ml="“Smallest squared distance wins” in the recommender system's related-items feature is "
         "exactly this call, squared.",
      more_href=F0W1 % "09-vectors", more_label="F0 W1 · Vectors"),

 dict(key="npmaxmin-api", label="np.max / np.min — x.max() / x.min()", say="“numpy max”, “numpy min”",
      gist="The largest or smallest <b>value</b> in an array — not its position (that is "
           "argmax/argmin).",
      body="<div class='gq'>np.max([12, 31, 7]) → 31     np.argmax(...) → 1</div>"
           "<p>Easy to reach for when you actually wanted the position — check which one a line "
           "of code needs before trusting it.</p>",
      ml="Used to normalise a value range for a plot, or to find the best score in a sweep like "
         "the ε threshold search in anomaly detection.",
      more_href=F0W1 % "19-min-max-argmax", more_label="F0 W1 · Min, max, argmax"),

 dict(key="nprandom-api", label="np.random.rand / .choice / .normal / .permutation",
      say="“numpy random”",
      gist="Generates random numbers — uniform, from a given list, from a bell curve, or a "
           "shuffled order, depending on which one you call.",
      body="<div class='gq'>np.random.permutation(m)[:K]   # K random rows, no repeats</div>"
           "<p>This exact pattern — permute, then take the first K — is how K-means picks its "
           "initial centroids, and how a train/test split is written by hand.</p>",
      ml="Every dataset generated for a demo on this site (the coffee-roasting data, the K-means "
         "blobs) starts from one of these calls."),

 dict(key="npseed-api", label="np.random.seed(...)", say="“numpy random seed”",
      gist="Makes “random” reproducible — same seed, same sequence of random numbers, every "
           "run.",
      body="<div class='gq'>np.random.seed(1)   # now every run of this notebook agrees</div>"
           "<p>Without it, re-running a cell that shuffles data or initialises random weights "
           "gives a different answer every time, which makes debugging much harder.</p>",
      ml="Every optional lab on this site fixes a seed for exactly this reason — so your output "
         "matches the lab's expected answer."),

 dict(key="npeye-api", label="np.eye(...)", say="“numpy eye”, as in “identity”",
      gist="Builds an identity matrix — 1s down the diagonal, 0s everywhere else.",
      body="<div class='gq'>np.eye(3) → [[1,0,0],[0,1,0],[0,0,1]]</div>"
           "<p>Multiplying anything by the identity matrix leaves it unchanged — the matrix "
           "equivalent of multiplying a number by 1.</p>",
      ml="Rare in this course's own code, but common enough elsewhere (regularisation terms, "
         "some solvers) that recognising it on sight is worth it.",
      more_href=F0W2 % "06-creating-arrays", more_label="F0 W2 · Creating arrays"),

 dict(key="npc-api", label="np.c_[...]", say="“numpy c underscore”",
      gist="Stacks arrays side by side as new <b>columns</b> — a shorthand for building a "
           "feature matrix.",
      body="<div class='gq'>np.c_[x, x**2, x**3]   # three columns instead of one</div>"
           "<p>Square brackets, not round ones — this is indexing syntax being reused as a "
           "shortcut, not a normal function call. It is exactly how a polynomial feature matrix "
           "is built by hand.</p>",
      ml="Feature engineering's “add x², x³ as new columns” is this one line.",
      more_href=C1 % (2, "08-feature-engineering"), more_label="C1 W2 · Feature engineering"),

 dict(key="nppolyfit-api", label="np.polyfit(...)", say="“numpy polynomial fit”",
      gist="Fits a polynomial curve to data points using the classical closed-form method — a "
           "quick one-line alternative to gradient descent, for polynomial curves specifically.",
      body="<div class='gq'>np.polyfit(x, y, deg=2)   # returns the 3 coefficients</div>"
           "<p>Handy for a quick reference curve on a plot; not how any model on this site is "
           "actually trained.</p>",
      ml="If you see a smooth reference line on a demo chart that was not produced by gradient "
         "descent, this is usually how it was drawn."),

 dict(key="npgradient-api", label="np.gradient(...)", say="“numpy gradient”",
      gist="A numerical <b>derivative</b> of a sequence of values — not to be confused with the "
           "gradient of a cost function used in gradient descent.",
      body="<div class='gq'>np.gradient([1, 4, 9, 16])   # approx. slope at each point</div>"
           "<p>Same word, different idea: this estimates a slope from data points; “the "
           "gradient” elsewhere on this site means the vector of partial derivatives of J.</p>",
      ml="Used only for illustration (e.g. drawing a tangent line on a demo curve), never inside "
         "an actual training loop."),

 dict(key="npround-api", label="np.round(...)", say="“numpy round”",
      gist="Rounds every element to a given number of decimal places.",
      body="<div class='gq'>np.round(3.14159, 2) → 3.14</div>"
           "<p>Purely cosmetic — used to tidy a printed number, never inside the maths of a "
           "model itself.</p>",
      ml="If you see a slightly different number on this site than in your own run, check "
         "whether one of you rounded and the other didn't."),

 dict(key="tfinput-api", label="Input(shape=...)", say="“input layer”",
      gist="Declares the shape of one example, before any layer sees it — lets Keras size every "
           "layer's weights immediately instead of waiting for data.",
      body="<div class='gq'>tf.keras.Input(shape=(400,))   # 400 pixels per example</div>"
           "<p>Optional in <code>Sequential</code> — Keras will size everything the first time "
           "you call <code>model.fit</code> if you skip it — but useful when you want to inspect "
           "a model's shapes before training.</p>",
      ml="Written either as <code>tf.keras.Input</code> or <code>tf.keras.layers.Input</code> — "
         "same call, and the shape you give here is what fixes n in the first layer's (n, units) "
         "weight matrix.",
      more_href=C2 % (1, "07-tensorflow-inference-code"),
      more_label="C2 W1 · Inference in code (TensorFlow)"),

 dict(key="tftape-api", label="tf.GradientTape() / tape.gradient(...)", say="“gradient tape”",
      gist="Records every operation as it runs, then replays them <b>backwards</b> to compute a "
           "derivative automatically — this is what backpropagation looks like in code.",
      body="<div class='gq'>with tf.GradientTape() as tape:\n    cost = (w*x - y)**2\n"
           "dJ_dw = tape.gradient(cost, w)</div>"
           "<p>Everything inside the <code>with</code> block is recorded. <code>tape.gradient"
           "(cost, w)</code> then walks that record backwards and returns exactly one number: "
           "how much <code>cost</code> would change per unit change in <code>w</code>.</p>",
      ml="model.fit does this same recording under the hood, every single step — GradientTape "
         "is what you reach for when your cost function is not one of Keras's built-in losses, "
         "e.g. collaborative filtering.",
      more_href=C3 % (2, "06-tensorflow-collaborative"),
      more_label="C3 W2 · TensorFlow implementation of collaborative filtering"),

 dict(key="tfapplygrad-api", label="optimizer.apply_gradients(...)", say="“apply gradients”",
      gist="The actual update step — takes the derivatives GradientTape computed and moves the "
           "parameters, exactly like a hand-written <code>w -= alpha * dJ_dw</code>.",
      body="<div class='gq'>optimizer.apply_gradients(zip(grads, [X, W, b]))</div>"
           "<p><code>zip</code> pairs each gradient with the variable it belongs to. This one "
           "line replaces writing out the gradient-descent (or Adam) update rule by hand.</p>",
      ml="Whatever optimizer you built with (plain SGD, Adam) decides <em>how</em> this step "
         "uses the gradient — the call itself stays the same.",
      more_href=C3 % (2, "06-tensorflow-collaborative"),
      more_label="C3 W2 · TensorFlow implementation of collaborative filtering"),

 dict(key="tfreduce-api", label="tf.reduce_sum / tf.reduce_max", say="“reduce sum”, “reduce max”",
      gist="TensorFlow's versions of summing or taking the max along an axis — the tensor "
           "equivalent of <code>np.sum</code> / <code>np.max</code>.",
      body="<div class='gq'>tf.reduce_max(q_values, axis=-1)   # best action's Q, per row</div>"
           "<p>“Reduce” means the named axis disappears from the result, same idea as NumPy's "
           "<code>axis=</code> argument.</p>",
      ml="max_a' Q(s', a') in the Bellman target is computed with exactly this call — one line, "
         "every action's value already computed by the network.",
      more_href=C3 % (3, "13-improved-architecture"),
      more_label="C3 W3 · Algorithm refinement: improved neural network architecture"),

 dict(key="tfl2norm-api", label="tf.linalg.l2_normalize(...)", say="“L2 normalise”",
      gist="Rescales a vector so its length becomes exactly 1, without changing the direction "
           "it points in.",
      body="<div class='gq'>[3, 4]  →  [0.6, 0.8]   (length 5 rescaled to length 1)</div>"
           "<p>Once both vectors being compared have length 1, their dot product is exactly the "
           "cosine of the angle between them — bounded between −1 and 1, so two comparisons are "
           "always on the same scale.</p>",
      ml="Both towers of the content-based recommender end with this call, precisely so their "
         "dot product is a fair, bounded comparison.",
      more_href=C3 % (2, "09-deep-content-based"),
      more_label="C3 W2 · Deep learning for content-based filtering"),

 dict(key="tftranspose-api", label="tf.transpose(...)", say="“transpose”",
      gist="Flips a matrix over its diagonal — rows become columns and columns become rows.",
      body="<div class='gq'>shape (3, 4)  →  tf.transpose(...)  →  shape (4, 3)</div>"
           "<p>Needed constantly to line up shapes for a matrix multiply — the same operation "
           "as NumPy's <code>.T</code>.</p>",
      ml="If a matmul is failing on a shape mismatch, transposing one side is very often the fix.",
      more_href=F0W1 % "13-transpose", more_label="F0 W1 · Transpose"),

 dict(key="tfnumpy-api", label=".numpy()", say="“dot numpy”",
      gist="Converts a TensorFlow tensor back into a plain NumPy array, so you can print it, "
           "plot it, or feed it to ordinary NumPy code.",
      body="<div class='gq'>a1 = layer(x)          # a tf.Tensor\na1.numpy()             # a plain ndarray</div>"
           "<p>TensorFlow and NumPy arrays look almost identical when printed; this call is the "
           "explicit crossing point between the two worlds.</p>",
      ml="Used whenever a TensorFlow layer's output needs to go into a NumPy-only function, "
         "like a plotting helper."),

 dict(key="tfsetweights-api", label=".set_weights([...])", say="“set weights”",
      gist="Manually installs a layer's weights, bypassing training entirely.",
      body="<div class='gq'>linear_layer.set_weights([np.array([[200]]), np.array([100])])</div>"
           "<p>Takes a list: the weight matrix first, then the bias. Used only for teaching — "
           "setting a neuron's weights to numbers you already solved for by hand, to prove the "
           "layer computes exactly what you expect.</p>",
      ml="This is how the very first neuron lab proves a Keras layer with no activation IS "
         "linear regression — same weights, same numbers, same answer.",
      more_href=C2 % (1, "04-neural-network-layer"),
      more_label="C2 W1 · Neural network layer"),

 dict(key="tfsummary-api", label="model.summary()", say="“summary”",
      gist="Prints every layer, its output shape, and its parameter count — a sanity check, not "
           "a training step.",
      body="<div class='gq'>Total params: 10,575</div>"
           "<p>The single fastest way to catch a layer sized wrong before wasting time training "
           "it — the printed parameter count should match what you'd compute by hand.</p>",
      ml="Comparing this printed total against your own by-hand count (inputs × units + units, "
         "per layer) is the standard way to check your understanding of a network's shape."),

 dict(key="tflosses-api", label="BinaryCrossentropy / SparseCategoricalCrossentropy / MeanSquaredError",
      say="“the loss classes”",
      gist="The three loss functions passed to <code>model.compile(loss=...)</code> on this "
           "site — which one you choose encodes what kind of problem the model is solving.",
      body="<div class='gq'>binary → BinaryCrossentropy   multiclass → SparseCategoricalCrossentropy(from_logits=True)   regression → MeanSquaredError</div>"
           "<p>“Sparse” means the labels are plain integers (3) rather than one-hot vectors; "
           "<code>from_logits=True</code> tells the preferred, numerically stable version that "
           "the last layer is linear, not already softmaxed.</p>",
      ml="Getting this one argument wrong (e.g. forgetting from_logits after making the last "
         "layer linear) is the single most common silent training bug on this site.",
      more_href=C2 % (2, "09-improved-softmax"),
      more_label="C2 W2 · Improved implementation of softmax"),

 dict(key="tfl2reg-api", label="tf.keras.regularizers.l2(...)", say="“L2 regulariser”",
      gist="Adds Course 1's regularisation penalty — λΣw² — to a layer's loss, discouraging "
           "large weights.",
      body="<div class='gq'>Dense(120, activation='relu', kernel_regularizer=l2(0.1))</div>"
           "<p>The number passed in is λ, exactly the same regularisation strength from Course "
           "1's cost function, just attached to one specific layer instead of the whole model.</p>",
      ml="The neural-network version of “build it too big, then regularise” — this is the line "
         "that does the regularising.",
      more_href=C2 % (3, "09-bias-variance-neural-networks"),
      more_label="C2 W3 · Bias / variance and neural networks"),

 dict(key="tfmodel-api", label="tf.keras.Model(...)", say="“the functional API”",
      gist="Builds a model from named inputs and outputs directly, instead of a straight "
           "<code>Sequential</code> stack — needed once a network has more than one input or "
           "output.",
      body="<div class='gq'>model = tf.keras.Model([input_user, input_item], output)</div>"
           "<p>Every layer is called like a function on the layer before it, and the model is "
           "then defined by which tensors are its inputs and its output.</p>",
      ml="The recommender system's two-tower network needs this — Sequential cannot express "
         "“two separate inputs meeting at one dot product”.",
      more_href=C3 % (2, "09-deep-content-based"),
      more_label="C3 W2 · Deep learning for content-based filtering"),

 dict(key="tfdot-api", label="tf.keras.layers.Dot(...)", say="“a Dot layer”",
      gist="Combines two vectors with a dot product, as a layer inside a model — the same "
           "operation as <code>np.dot</code>, wired into the network graph itself.",
      body="<div class='gq'>output = Dot(axes=1)([v_user, v_movie])</div>"
           "<p><code>axes=1</code> says which dimension of each input to multiply-and-sum along.</p>",
      ml="The point where the recommender's two towers finally meet and produce one predicted "
         "rating.",
      more_href=C3 % (2, "09-deep-content-based"),
      more_label="C3 W2 · Deep learning for content-based filtering"),

 dict(key="tfgap-api", label="GlobalAveragePooling2D()", say="“global average pooling”",
      gist="Collapses an entire image feature map down to one number per channel — a bridge "
           "layer used when reusing a pretrained image model.",
      body="<p>Turns a large grid of numbers into a short vector Dense layers can use, without "
           "adding any new parameters of its own.</p>",
      ml="Appears only where a pretrained network (like MobileNetV2) is being adapted — part of "
         "transfer learning's plumbing, not something you write from scratch.",
      more_href=C2 % (3, "13-transfer-learning"), more_label="C2 W3 · Transfer learning"),

 dict(key="tfmobilenet-api", label="tf.keras.applications.MobileNetV2(...)", say="“MobileNet V2”",
      gist="A neural network already trained on millions of images — the starting point for "
           "transfer learning rather than something trained from scratch here.",
      body="<p>Its early layers already recognise edges, textures and shapes; only the final "
           "layers get replaced and retrained for a new, specific task.</p>",
      ml="This is what makes transfer learning practical with a tiny dataset — you are reusing "
         "millions of images' worth of training you never had to do yourself.",
      more_href=C2 % (3, "13-transfer-learning"), more_label="C2 W3 · Transfer learning"),

 dict(key="pdreadcsv-api", label="pd.read_csv(...)", say="“read csv”",
      gist="Loads a CSV file straight into a pandas DataFrame.",
      body="<div class='gq'>df = pd.read_csv('houses.csv')</div>"
           "<p>The single most common way real data actually arrives in this course — as rows "
           "and named columns, not a NumPy array. It takes a URL as readily as a filename, so "
           "the <a href='../data.html'>datasets page</a> lets you run any of this without "
           "downloading anything.</p>",
      ml="Almost always the very first line of any real (non-synthetic) dataset on this site — "
         "and houses.csv is a real file in this repository, not a placeholder.",
      more_href=F0W2 % "13-pandas-dataframes", more_label="F0 W2 · pandas DataFrames"),

 dict(key="pdgetdummies-api", label="pd.get_dummies(...)", say="“get dummies”",
      gist="One-hot encodes every categorical column in a DataFrame automatically — pandas's "
           "version of the one-hot encoding decision trees rely on.",
      body="<div class='gq'>pd.get_dummies(df, columns=['ChestPainType'])</div>"
           "<p>Turns one column of category names into several 0/1 columns, one per category — "
           "exactly what a tree needs to split on.</p>",
      ml="The tree-ensemble lab's very first data-preparation step, before any model sees the "
         "data at all.",
      more_href=C2 % (4, "06-one-hot-encoding"),
      more_label="C2 W4 · Using one-hot encoding of categorical features"),

 dict(key="pdeda-api", label="df.head() / .info() / .describe() / .isnull()", say="“the first four you run”",
      gist="The four calls you run on any new DataFrame before doing anything else with it.",
      body="<div class='gq'>df.head()      # the first few rows, by eye\n"
           "df.info()      # column names, types, and how many are missing\n"
           "df.describe()  # mean, std, min, max per column\n"
           "df.isnull()    # exactly which cells are missing</div>"
           "<p>None of these change the data — they are how you get familiar with it before "
           "writing a single line of model code.</p>",
      ml="Skipping this step is the most common reason a beginner's model quietly trains on "
         "garbage — a missing value or a wrong dtype nobody noticed.",
      more_href=F0W2 % "13-pandas-dataframes", more_label="F0 W2 · pandas DataFrames"),

 dict(key="sklearntts-api", label="train_test_split(...)", say="“train test split”",
      gist="Randomly divides a dataset into separate pieces — train, cross-validation, test — "
           "so you always evaluate on data the model never learned from.",
      body="<div class='gq'>X_tr, X_, y_tr, y_ = train_test_split(X, y, test_size=0.40, random_state=1)</div>"
           "<p>Called twice in a row (as here) to get three splits instead of two: the leftover "
           "40% is split again into cross-validation and test.</p>",
      ml="random_state fixes the shuffle so the split is reproducible — same rows in train every "
         "time you rerun the notebook.",
      more_href=C2 % (3, "02-evaluating-a-model"), more_label="C2 W3 · Evaluating a model"),

 dict(key="sklearnprc-api", label="precision_recall_curve(...)", say="“precision recall curve”",
      gist="Sweeps every possible threshold and reports the precision and recall you would get "
           "at each one, in one call instead of a manual loop.",
      body="<div class='gq'>precision, recall, thresholds = precision_recall_curve(y_cv, probs)</div>"
           "<p>Three arrays come back, all the same length — read across them at the same index "
           "to see what precision and recall a given threshold buys you.</p>",
      ml="This is the tool for actually picking a threshold, rather than guessing 0.5 and hoping.",
      more_href=C2 % (3, "17-precision-recall-tradeoff"),
      more_label="C2 W3 · Trading off precision and recall"),

 dict(key="sklearnpca-api", label="PCA(...) / .fit_transform() / .inverse_transform()",
      say="“P-C-A”",
      gist="Finds the directions of greatest variance and projects the data onto the top few — "
           "scikit-learn's ready-made version of the PCA algorithm.",
      body="<div class='gq'>Z = PCA(n_components=2).fit_transform(X)   # compress\n"
           "X_hat = pca.inverse_transform(Z)                # approximately reconstruct</div>"
           "<p><code>fit_transform</code> both learns the axes and projects onto them in one "
           "call; <code>inverse_transform</code> goes the other way, approximately, since "
           "information was thrown away compressing.</p>",
      ml="n_components is the k you are choosing — how many numbers each example gets squashed "
         "down to.",
      more_href=C3 % (2, "15-pca-in-code"), more_label="C3 W2 · PCA in code"),

 dict(key="sklearnforest-api", label="RandomForestClassifier / XGBClassifier / XGBRegressor",
      say="“the ensemble classifiers”",
      gist="Ready-made tree ensembles — build and train dozens of decision trees and vote, in "
           "one class instead of writing bagging or boosting by hand.",
      body="<div class='gq'>RandomForestClassifier(n_estimators=100).fit(X_train, y_train)</div>"
           "<p>Same <code>.fit(X, y)</code> / <code>.predict(X)</code> shape as every other "
           "scikit-learn model — the ensemble machinery is entirely hidden inside the class.</p>",
      ml="XGBoost specifically is usually the strongest off-the-shelf choice for tabular "
         "(spreadsheet-shaped) data.",
      more_href=C2 % (4, "11-random-forest"), more_label="C2 W4 · Random forest algorithm"),

 dict(key="sklearnfit-api", label=".fit(X, y)", say="“fit”, the scikit-learn way",
      gist="Trains a scikit-learn model in one shot — no epochs, no learning rate to choose; it "
           "solves for the best parameters directly or runs its own internal loop.",
      body="<div class='gq'>clf = RandomForestClassifier().fit(X_train, y_train)</div>"
           "<p>Different from Keras's <code>model.fit</code>, which trains over a number of "
           "epochs you choose — scikit-learn's models return control once they consider "
           "themselves finished.</p>",
      ml="The same one-word method name across every scikit-learn model (trees, PCA, scalers) "
         "is deliberate — learn the pattern once, and it works everywhere in the library."),
dict(key="kwaxis-api", label="axis=", say="“axis”",
      gist="Which dimension an operation collapses along. <b>axis=0</b> collapses the rows, "
           "leaving one result per column; <b>axis=1</b> collapses the columns, one per row.",
      body="<div class='gq'>X.mean(axis=0)  # one mean per FEATURE (a column each)</div>"
           "<p>The rule of thumb: axis=0 is almost always what you want when rows are examples "
           "and columns are features, since it gives one number per feature.</p>",
      ml="The single most common source of a subtly-wrong result on this site — getting axis=0 "
         "and axis=1 backwards silently produces numbers of the wrong shape that still run.",
      more_href=F0W2 % "10-aggregations", more_label="F0 W2 · Aggregations"),

 dict(key="kwactivation-api", label="activation=", say="“activation”",
      gist="Which non-linearity g a layer applies after its weighted sum — 'relu', 'sigmoid', "
           "'softmax', or 'linear' for none at all.",
      body="<div class='gq'>Dense(25, activation='relu')</div>"
           "<p>This one string is the entire difference between a hidden layer and an output "
           "layer — the choice depends on the problem, not on taste.</p>",
      ml="Hidden layers: almost always relu. Output layer: sigmoid (binary), softmax "
         "(multiclass), or linear (regression).",
      more_href=C2 % (2, "04-choosing-activations"),
      more_label="C2 W2 · Choosing activation functions"),

 dict(key="kwunits-api", label="units=", say="“units”",
      gist="How many neurons are in this layer — not how many inputs it has.",
      body="<div class='gq'>Dense(units=25)   # 25 neurons, however many inputs arrive</div>"
           "<p>Keras works out the input size on its own from whatever feeds into the layer; "
           "units is the one number you must choose yourself.</p>",
      ml="A very common beginner mix-up: units is the layer's OUTPUT width, not its input width.",
      more_href="c2/w1-09-building-a-network-sequential.html",
      more_label="C2 W1 · Building a neural network (Sequential)"),

 dict(key="kwloss-api", label="loss=", say="“loss”",
      gist="Which cost function to minimise — the choice that encodes what kind of problem "
           "this is.",
      body="<div class='gq'>loss=BinaryCrossentropy()   # binary   |   loss=MeanSquaredError()   # regression</div>"
           "<p>Passed once, to <code>model.compile</code>, and used for every step of training "
           "afterwards.</p>",
      ml="Get this one argument wrong for the problem type and the model can still keep "
         "\u201ctraining\u201d — just towards the wrong thing.",
      more_href=C2 % (2, "01-tensorflow-training"),
      more_label="C2 W2 · TensorFlow implementation of training"),

 dict(key="kwepochs-api", label="epochs=", say="“epochs”",
      gist="How many times the WHOLE training set is passed through during training.",
      body="<div class='gq'>model.fit(X, y, epochs=100)   # 100 full passes over X</div>"
           "<p>Not the same as the number of gradient-descent steps — with batching, one epoch "
           "can be many steps.</p>",
      ml="Too few epochs and training stops before J has settled; too many can start to overfit "
         "on a small dataset.",
      more_href=C2 % (2, "01-tensorflow-training"),
      more_label="C2 W2 · TensorFlow implementation of training"),

 dict(key="kwshape-api", label="shape=", say="“shape”",
      gist="The size of each dimension of an array or tensor — how many rows, columns, etc.",
      body="<div class='gq'>Input(shape=(400,))   # each example is 400 numbers</div>"
           "<p>Declaring it up front lets Keras size a layer's weights immediately, instead of "
           "waiting to see actual data.</p>",
      ml="Reading shapes correctly (m, n) is the single most useful debugging skill in this "
         "whole specialization.",
      more_href=F0W2 % "05-shape-and-axis", more_label="F0 W2 · Shape and axis"),

 dict(key="kwname-api", label="name=", say="“name”",
      gist="A human-readable label for a layer or model — cosmetic, shows up in "
           "<code>model.summary()</code> and error messages, changes nothing about the maths.",
      body="<div class='gq'>Dense(25, activation='relu', name='layer1')</div>"
           "<p>Purely for your own benefit when reading a summary table or debugging which layer "
           "an error came from.</p>",
      ml="Handy once a network has more than two or three layers and 'dense_7' stops being "
         "informative."),

 dict(key="kwdtype-api", label="dtype=", say="“d-type”",
      gist="The single data type every element of an array is stored as — <code>float32</code>, "
           "<code>int64</code>, and so on.",
      body="<div class='gq'>np.array([1, 2, 3], dtype='float32')</div>"
           "<p>Every NumPy array has exactly one dtype for the whole array — you cannot mix "
           "types the way a Python list can.</p>",
      ml="TensorFlow defaults to float32; mixing it with a float64 NumPy array is a common "
         "source of a confusing dtype-mismatch error.",
      more_href=F0W2 % "02-types", more_label="F0 W2 · Types"),

 dict(key="kwoptimizer-api", label="optimizer=", say="“optimizer”",
      gist="Which update rule adjusts the weights each step — plain gradient descent, or "
           "(almost always in practice) Adam.",
      body="<div class='gq'>model.compile(optimizer=Adam(learning_rate=1e-3), loss=...)</div>"
           "<p>Passed once, alongside the loss, and used for every training step after that.</p>",
      ml="Adam is the default choice in real code; Course 1 teaches plain gradient descent by "
         "hand first so you understand what the optimizer is actually doing.",
      more_href=C2 % (2, "11-advanced-optimization"),
      more_label="C2 W2 · Advanced optimization (Adam)"),

 dict(key="kwlr-api", label="learning_rate=", say="“learning rate”",
      gist="The α you already know from Course 1, passed to an optimizer under its full name.",
      body="<div class='gq'>Adam(learning_rate=0.001)</div>"
           "<p>Same concept, same trade-off as everywhere else — too small crawls, too large "
           "overshoots — just spelled out in full rather than abbreviated to α.</p>",
      ml="If a Keras model trains oddly, this is one of the first two or three arguments worth "
         "sweeping.",
      more_href="c1/w1-11-learning-rate.html", more_label="C1 W1 · The learning rate"),

 dict(key="kwkreg-api", label="kernel_regularizer=", say="“kernel regularizer”",
      gist="Attaches Course 1's regularisation penalty to one specific layer's weights.",
      body="<div class='gq'>Dense(120, activation='relu', kernel_regularizer=l2(0.1))</div>"
           "<p>“Kernel” here just means “this layer's weight matrix” — nothing to do with the "
           "kernel trick from other ML contexts.</p>",
      ml="The line that actually does the regularising in \u201cbuild it too big, then regularise\u201d.",
      more_href=C2 % (3, "09-bias-variance-neural-networks"),
      more_label="C2 W3 · Bias / variance and neural networks"),

 dict(key="kwfromlogits-api", label="from_logits=", say="“from logits”",
      gist="Tells the loss function the model's last layer is <b>linear</b>, not already "
           "squashed by softmax — lets it compute the loss in a numerically safer way.",
      body="<div class='gq'>SparseCategoricalCrossentropy(from_logits=True)</div>"
           "<p>Pairs with a final <code>Dense(N, activation='linear')</code> layer. Forget this "
           "flag after making the last layer linear, and training silently learns the wrong "
           "thing.</p>",
      ml="The single most common silent bug in this course's multiclass code — right shapes, "
         "runs fine, wrong answer.",
      more_href=C2 % (2, "09-improved-softmax"),
      more_label="C2 W2 · Improved implementation of softmax"),

 dict(key="kwtestsize-api", label="test_size=", say="“test size”",
      gist="What fraction of the data goes into the held-out split — 0.40 means 40%.",
      body="<div class='gq'>train_test_split(X, y, test_size=0.40)   # 60% train, 40% held out</div>"
           "<p>Called twice in a row splits the held-out 40% again, e.g. into equal "
           "cross-validation and test halves.</p>",
      ml="Whatever fraction you choose, the point is that the model never trains on this "
         "portion.",
      more_href=C2 % (3, "02-evaluating-a-model"), more_label="C2 W3 · Evaluating a model"),

 dict(key="kwrandomstate-api", label="random_state=", say="“random state”",
      gist="Fixes the random shuffle so a split is reproducible — same rows in train every time "
           "you rerun it.",
      body="<div class='gq'>train_test_split(X, y, random_state=1)</div>"
           "<p>The number itself is arbitrary; what matters is using the SAME number every time "
           "you want the same split back.</p>",
      ml="Without it, comparing two models trained on \u201cthe same split\u201d across two runs is not "
         "actually a fair comparison."),

 dict(key="kwdegree-api", label="degree=", say="“degree”",
      gist="The highest power used when generating polynomial features — degree=3 adds x, x², "
           "and x³.",
      body="<div class='gq'>PolynomialFeatures(degree=3)</div>"
           "<p>Higher degree means a more flexible curve, and a bigger risk of overfitting.</p>",
      ml="Sweeping this argument and watching J_cv is exactly how Course 1 Week 2 picks a model "
         "complexity.",
      more_href=C1 % (2, "09-polynomial-regression"),
      more_label="C1 W2 · Polynomial regression"),

 dict(key="kwnestimators-api", label="n_estimators=", say="“n estimators”",
      gist="How many trees to build in a forest or boosted ensemble.",
      body="<div class='gq'>RandomForestClassifier(n_estimators=100)</div>"
           "<p>More trees generally help, up to a point of diminishing returns, at the cost of "
           "more compute.</p>",
      ml="B ≈ 100 is the usual rule of thumb — averaging more independent trees keeps shrinking "
         "the spread of the ensemble's answer, but slower and slower.",
      more_href=C2 % (4, "11-random-forest"), more_label="C2 W4 · Random forest algorithm"),

 dict(key="kwreplace-api", label="replace=", say="“replace”",
      gist="Whether a random draw can pick the SAME item more than once — True means sampling "
           "with replacement.",
      body="<div class='gq'>np.random.choice(m, size=m, replace=True)   # bootstrap sample</div>"
           "<p>This exact call, with replace=True, is what \u201cbagging\u201d means — some examples "
           "appear twice, some not at all.</p>",
      ml="Random forest and bagging both rely on replace=True; leaving it False would just give "
         "back a reshuffled copy of the original data.",
      more_href=C2 % (4, "10-sampling-with-replacement"),
      more_label="C2 W4 · Sampling with replacement"),

 dict(key="kwsize-api", label="size=", say="“size”",
      gist="How many random numbers to generate, and in what shape.",
      body="<div class='gq'>np.random.normal(5, 1.2, size=1000)   # 1000 draws</div>"
           "<p>Can be a single number (a flat array) or a tuple (a multi-dimensional array of "
           "random values).</p>",
      ml="Used to generate the synthetic datasets behind several demos on this site."),

 dict(key="kwweights-api", label="weights=", say="“weights”",
      gist="Which pretrained weights to load into a model, if any — <code>'imagenet'</code> "
           "loads weights already trained on a million labelled images.",
      body="<div class='gq'>MobileNetV2(weights='imagenet', include_top=False)</div>"
           "<p>This single argument is what makes a network transfer-learned rather than "
           "trained from scratch.</p>",
      ml="Skip this and you get the SAME architecture with random, untrained weights — all of "
         "transfer learning's benefit comes from this one argument.",
      more_href=C2 % (3, "13-transfer-learning"), more_label="C2 W3 · Transfer learning"),

 dict(key="kwncomponents-api", label="n_components=", say="“n components”",
      gist="How many numbers PCA should compress each example down to.",
      body="<div class='gq'>PCA(n_components=2)   # squash however many features into just 2</div>"
           "<p>Chosen by how much variance you are willing to give up in exchange for fewer "
           "numbers per example — often picked by plotting variance kept against this number.</p>",
      ml="n_components=2 or 3 specifically is what makes a high-dimensional dataset plottable "
         "by eye.",
      more_href=C3 % (2, "15-pca-in-code"), more_label="C3 W2 · PCA in code"),

 dict(key="kwinputshape-api", label="input_shape=", say="“input shape”",
      gist="An older, equivalent way of telling a layer the shape of one example — the same job "
           "as a separate Input(shape=...) layer.",
      body="<div class='gq'>Dense(25, activation='relu', input_shape=(400,))</div>"
           "<p>Only needs to be given to the very first layer — every later layer infers its "
           "input size from the layer before it.</p>",
      ml="You will see both spellings across real-world code; they do the same job."),

 dict(key="kwincludetop-api", label="include_top=", say="“include top”",
      gist="Whether to keep a pretrained model's final classification layer — False strips it "
           "off so you can attach your own.",
      body="<div class='gq'>MobileNetV2(include_top=False)   # keep the feature-extracting body only</div>"
           "<p>The \u201ctop\u201d was trained to recognise the ORIGINAL 1000 ImageNet categories — "
           "useless for a new task, which is why it gets removed and replaced.</p>",
      ml="Almost always False in transfer learning — you want the learned features, not "
         "someone else's output categories.",
      more_href=C2 % (3, "13-transfer-learning"), more_label="C2 W3 · Transfer learning"),

 dict(key="kwcolumns-api", label="columns=", say="“columns”",
      gist="Which column(s) of a DataFrame an operation should act on.",
      body="<div class='gq'>pd.get_dummies(df, columns=['ChestPainType'])</div>"
           "<p>Without naming a column, pandas would try to one-hot encode every "
           "categorical-looking column in the whole table.</p>",
      ml="Naming columns explicitly is what stops a numeric column from being accidentally "
         "treated as a category.",
      more_href=C2 % (4, "06-one-hot-encoding"),
      more_label="C2 W4 · Using one-hot encoding of categorical features"),

 dict(key="kwplotstyle-api", label="color= / lw= / label=", say="“plot styling”",
      gist="Purely cosmetic matplotlib arguments — line colour, line width, and the text shown "
           "in a legend. None of them change the data.",
      body="<div class='gq'>plt.plot(x, y, color='grey', lw=0.8, label='J_train')</div>"
           "<p>Safe to ignore when reading a snippet for the maths — these three only affect "
           "how the resulting picture looks.</p>",
      ml="label= is what makes plt.legend() able to say which line is which."),
]
