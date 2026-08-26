# -*- coding: utf-8 -*-
"""Review cards — Course 2."""
from cardkit import C, deck, blk, steps, bullets, two, hint

W1 = deck("C2", 1, "Neural Networks", [
    C("c2w1-neuron", "formula",
      "What does <b>one artificial neuron</b> compute?",
      blk("<var>z</var> = <b>w⃗·x⃗</b> + <var>b</var> &nbsp;→&nbsp; <var>a</var> = <var>g</var>(<var>z</var>)")
      + "<p>Identical to logistic regression. <b>One neuron <em>is</em> one logistic regression unit.</b></p>"
      + bullets(["w — how much this neuron trusts each input (learned)",
                 "b — its default mood (learned)",
                 "a — the activation it passes on"]),
      "c2/w1-01-neurons-and-the-brain.html"),

    C("c2w1-hidden-layer", "concept",
      "What does a <b>hidden layer</b> actually buy you over plain logistic regression?",
      "<p><b>Learned features.</b> In Course 1 you invented x₁x₂ or x² by hand. A hidden layer invents "
      "its own intermediate features and learns which are worth keeping.</p>"
      + hint("The names we give hidden units (“affordability”, “awareness”) are a story we tell afterwards. "
             "Nothing in training assigns them meaning."),
      "c2/w1-02-demand-prediction.html"),

    C("c2w1-layer", "concept",
      "What is a <b>layer</b>, and what does <code>units=3</code> control?",
      "<p>Several neurons that all read the <b>same input vector</b> and each output <b>one</b> number.</p>"
      + "<p><code>units</code> sets the <b>length of that layer's output vector</b>. Nothing else — not "
        "the number of inputs, not the number of examples.</p>"
      + hint("Neurons within a layer never talk to each other. That independence is exactly what lets them "
             "be computed as one matrix multiply."),
      "c2/w1-04-neural-network-layer.html"),

    C("c2w1-params", "formula",
      "How many <b>parameters</b> in a layer with n inputs and p units?",
      blk("weights = <var>n</var> × <var>p</var> &nbsp;&nbsp;·&nbsp;&nbsp; biases = <var>p</var>")
      + "<p>e.g. 400 inputs → 25 units: 400×25 = <b>10,000</b> weights + <b>25</b> biases.</p>"
      + hint("<code>model.summary()</code> prints exactly these totals. Comparing them against a hand "
             "count is the fastest way to catch a wiring mistake."),
      "c2/w1-04-neural-network-layer.html"),

    C("c2w1-master-eq", "formula",
      "The <b>master equation</b> of forward propagation.",
      blk("<var>a</var><sub><var>j</var></sub><sup>[<var>l</var>]</sup> = <var>g</var>( <b>w</b><sub><var>j</var></sub><sup>[<var>l</var>]</sup> · <b>a</b><sup>[<var>l</var>−1]</sup> + <var>b</var><sub><var>j</var></sub><sup>[<var>l</var>]</sup> )")
      + "<p>“The activation of unit <b>j</b> in layer <b>l</b> is g of: the weights of unit j in layer l, "
        "dotted with the <b>whole</b> output of the previous layer, plus its bias.”</p>"
      + hint("a<sup>[0]</sup> = x, so the formula works for layer 1 with no special case."),
      "c2/w1-05-more-complex-networks.html"),

    C("c2w1-brackets", "trap",
      "In a neural network, what does a <b>square-bracket superscript</b> mean, and what does it never mean?",
      bullets(["<b>a<sup>[2]</sup></b> — layer 2. <b>Never</b> a power.",
               "<b>x<sup>(2)</sup></b> — training example 2",
               "<b>x<sup>2</sup></b> — x squared"])
      + hint("Reading <sup>[2]</sup> as “squared” is the single most common notation error in Course 2."),
      "c2/w1-05-more-complex-networks.html"),

    C("c2w1-weight-vec-len", "concept",
      "A network is 4 → 5 → 3 → 1. How long is the weight vector <b>w<sub>2</sub><sup>[3]</sup></b>?",
      "<p><b>3.</b> Layer 3 reads layer 2, which has 3 units.</p>"
      + hint("Weight-vector length always equals the <b>width of the previous layer</b>. And unit 2 of "
             "layer 3 reads <em>every</em> unit of layer 2, not just unit 2."),
      "c2/w1-05-more-complex-networks.html"),

    C("c2w1-dense-cols", "concept",
      "In <code>W</code> for a dense layer, what do the <b>rows</b> and <b>columns</b> mean?",
      "<p><b>Columns are neurons. Rows are input features.</b></p>"
      + "<p><code>W[:, j]</code> is neuron j's personal weight vector. W of shape (2, 3) = 2 inputs, "
        "3 neurons.</p>"
      + hint("This orientation is what makes the vectorised version work with no transposes."),
      "c2/w1-10-forward-prop-single-layer.html"),

    C("c2w1-shapes", "trap",
      "What is the difference between <code>(2,)</code> and <code>(1, 2)</code> in NumPy?",
      two("a <b>1-D array</b> — no rows or columns at all. Old Course 1 style; Keras will not accept it.",
          "a <b>matrix</b>: 1 row × 2 columns. One training example with two features.",
          "np.array([200, 17]) → (2,)", "np.array([[200, 17]]) → (1,2)")
      + hint("Convention for the whole specialization: <b>rows = examples, columns = features</b>."),
      "c2/w1-08-data-in-tensorflow.html"),

    C("c2w1-dense-code", "code",
      "Write <code>dense()</code> — the looped version.",
      "<pre><code>def dense(a_in, W, b):\n"
      "    units = W.shape[1]        # columns = neurons\n"
      "    a_out = np.zeros(units)\n"
      "    for j in range(units):\n"
      "        w = W[:, j]           # column j\n"
      "        z = np.dot(w, a_in) + b[j]\n"
      "        a_out[j] = g(z)\n"
      "    return a_out</code></pre>"
      + hint("<code>W.shape[1]</code>, not <code>[0]</code> — [0] is the number of <em>inputs</em>."),
      "c2/w1-11-general-forward-prop.html"),

    C("c2w1-dense-vec", "code",
      "Write <code>dense()</code> — the <b>vectorised</b> version.",
      "<pre><code>def dense(A_in, W, B):\n"
      "    Z = np.matmul(A_in, W) + B   # (m,n)@(n,units) -> (m,units)\n"
      "    return g(Z)</code></pre>"
      + "<p>No loop, no slicing, no index arithmetic. <code>B</code> is (1, units) and broadcasting "
        "adds it to every row.</p>",
      "c2/w1-16-matmul-code.html"),

    C("c2w1-matmul-rule", "formula",
      "The <b>matrix multiplication shape rule</b>.",
      blk("(<var>m</var> × <b><var>n</var></b>) × (<b><var>n</var></b> × <var>p</var>) = (<var>m</var> × <var>p</var>)")
      + "<p>Write the two shapes side by side. If the <b>inner</b> numbers match it is legal, and the "
        "answer is the <b>outer</b> two.</p>"
      + hint("The inner dimension gets summed away — it never appears in the result. And A@W ≠ W@A; "
             "usually one of them is not even legal."),
      "c2/w1-15-matmul-rules.html"),

    C("c2w1-dotprod", "concept",
      "Why does a neuron need a <b>dot product</b> rather than elementwise multiplication?",
      "<p>Because a neuron must produce a <b>single number</b> z. Elementwise multiplication leaves you "
      "with a list.</p>"
      + hint("Geometrically a·w = |a||w|cos θ — it measures how much the input <em>resembles the pattern "
             "stored in the weights</em>."),
      "c2/w1-14-matrix-multiplication.html"),

    C("c2w1-vectorization", "concept",
      "Why did neural networks become practical in the 2010s?",
      bullets(["<b>data</b> — the internet supplied millions of labelled examples",
               "<b>compute</b> — GPUs made the matrix multiplies ~100× cheaper",
               "<b>scale behaviour</b> — classical algorithms plateau with more data; large networks "
               "keep improving"])
      + hint("The maths is from 1958 and 1986. Nothing about it changed."),
      "c2/w1-13-vectorization.html"),
])

W2 = deck("C2", 2, "Neural Network Training", [
    C("c2w2-three-steps", "algorithm",
      "The <b>three steps</b> of training in TensorFlow, and their Course 1 twins.",
      steps(["<b>define the model</b> — <code>Sequential([...])</code> ← what f(x) is",
             "<b>say what wrong means</b> — <code>model.compile(loss=...)</code> ← the cost function",
             "<b>minimise it</b> — <code>model.fit(X, Y, epochs=...)</code> ← gradient descent"])
      + hint("Only <code>fit</code> changes the weights. <code>compile</code> just records settings."),
      "c2/w2-01-tensorflow-training.html"),

    C("c2w2-bce", "formula",
      "<b>Binary cross-entropy</b> — and the difference between loss and cost.",
      blk("<var>L</var>(<var>f</var>, <var>y</var>) = −<var>y</var> log(<var>f</var>) − (1 − <var>y</var>) log(1 − <var>f</var>)")
      + bullets(["<b>loss</b> L — the error on <b>one</b> example",
                 "<b>cost</b> J — the <b>average</b> loss over all m examples: J = (1/m)ΣL"])
      + hint("The distinction is asked about in interviews and relied on throughout Course 2."),
      "c2/w2-02-training-details.html"),

    C("c2w2-relu", "formula",
      "<b>ReLU</b>, and why it replaced sigmoid in hidden layers.",
      blk("<var>g</var>(<var>z</var>) = max(0, <var>z</var>)")
      + bullets(["<b>slope is exactly 1</b> on the positive side → gradients survive deep stacks",
                 "one <code>max</code>, no <code>exp</code> → meaningfully faster",
                 "sigmoid's slope peaks at 0.25; stack ten layers and 0.25¹⁰ ≈ 10⁻⁶ — the early layers "
                 "receive nothing"]),
      "c2/w2-03-sigmoid-alternatives.html"),

    C("c2w2-dying-relu", "trap",
      "What is a <b>dying ReLU</b>, and why is it permanent?",
      "<p>A unit whose z is negative for <b>every</b> training example. Its gradient is 0 always, so its "
      "weights never update, so its z never changes.</p>"
      + hint("A lower learning rate, or Leaky ReLU, avoids it."),
      "c2/w2-03-sigmoid-alternatives.html"),

    C("c2w2-activation-choice", "concept",
      "Which <b>output activation</b> for each task? And for hidden layers?",
      bullets(["binary classification → <b>sigmoid</b>",
               "regression, can be negative → <b>linear</b>",
               "regression, never negative → <b>ReLU</b>",
               "multiclass, pick one → <b>softmax</b>",
               "<b>every hidden layer → ReLU</b>, almost always"])
      + hint("“Linear activation” means <em>no</em> activation: g(z) = z."),
      "c2/w2-04-choosing-activations.html"),

    C("c2w2-why-nonlinear", "concept",
      "Prove that a network with <b>linear activations everywhere</b> is pointless.",
      blk("<var>a</var><sup>[2]</sup> = <var>W</var><sup>[2]</sup>(<var>W</var><sup>[1]</sup><var>x</var> + <var>b</var><sup>[1]</sup>) + <var>b</var><sup>[2]</sup> "
          "= <b>(<var>W</var><sup>[2]</sup><var>W</var><sup>[1]</sup>)</b><var>x</var> + <b>(…)</b> = <var>W′x</var> + <var>b′</var>")
      + "<p>Two matrices multiplied together are just another matrix. A 100-layer linear network is "
        "<b>algebraically identical to one layer</b> — exactly zero extra expressive power.</p>"
      + hint("Each ReLU unit adds exactly one “kink”. Enough kinks and you can trace any curve."),
      "c2/w2-05-why-activations.html"),

    C("c2w2-softmax", "formula",
      "<b>Softmax</b> — the formula and what the two moves do.",
      blk("<var>a<sub>j</sub></var> = <span class='fr'><span><var>e</var><sup><var>z<sub>j</sub></var></sup></span>"
          "<span><span class='sum'>Σ</span><sub><var>k</var></sub> <var>e</var><sup><var>z<sub>k</sub></var></sup></span></span> = <var>P</var>(<var>y</var> = <var>j</var> | <var>x</var>)")
      + bullets(["<b>exp</b> → makes everything positive",
                 "<b>÷ by the total</b> → makes them sum to exactly 1"])
      + hint("The <b>only</b> activation where each output depends on all the others. That coupling is "
             "what forces the sum to 1."),
      "c2/w2-07-softmax.html"),

    C("c2w2-softmax-shift", "concept",
      "z = [10, 1, 1] and z = [110, 101, 101]. Do these give the same softmax output?",
      "<p><b>Yes — identical.</b> Softmax depends only on the <b>differences</b> between the z's. Adding "
      "a constant to every z changes nothing.</p>"
      + hint("This fact is the basis of the numerical fix: compute <code>exp(z − max(z))</code>, so the "
             "largest exponent is exp(0) = 1 and overflow is impossible."),
      "c2/w2-07-softmax.html"),

    C("c2w2-from-logits", "concept",
      "What does <code>from_logits=True</code> do, and what is the catch?",
      "<p>It tells Keras the output layer is <code>linear</code> and the loss should apply the "
      "sigmoid/softmax itself — using an algebraically rearranged formula that never builds the "
      "intermediate probability, so nothing rounds to 0 or 1.</p>"
      + blk("−log( 1/(1+<var>e</var><sup>−z</sup>) ) = log(1 + <var>e</var><sup>−<var>z</var></sup>)", "same maths, safer")
      + "<p><b>The catch:</b> <code>predict</code> now returns raw logits, not probabilities. Apply "
        "<code>tf.nn.softmax()</code> yourself.</p>"
      + hint("At z = 20, sigmoid rounds to exactly 1.0 in float32, so −log(1) = 0 — the model is told it "
             "made no error and learning stops."),
      "c2/w2-09-improved-softmax.html"),

    C("c2w2-multiclass-vs-label", "distinguish",
      "<b>Multi-class</b> vs <b>multi-label</b>.",
      two(bullets(["exactly <b>one</b> answer is correct", "y is an integer, e.g. 7",
                   "<code>Dense(N, 'softmax')</code>", "outputs sum to <b>1</b>", "outputs are coupled"]),
          bullets(["<b>several</b> can be true at once", "y is a vector, e.g. [1, 0, 1]",
                   "<code>Dense(N, 'sigmoid')</code>", "outputs sum to anything", "outputs are independent"]),
          "Multi-class", "Multi-label")
      + hint("Using softmax for multi-label structurally prevents the model from saying “both” — it can "
             "never be right about a photo containing a car and a bus."),
      "c2/w2-10-multi-label.html"),

    C("c2w2-adam", "concept",
      "What does <b>Adam</b> do that plain gradient descent does not?",
      "<p>It keeps a <b>separate learning rate for every parameter</b> and adapts each one:</p>"
      + bullets(["gradient consistently the same direction → <b>increase</b> the step",
                 "gradient keeps flip-flopping → <b>decrease</b> the step"])
      + blk("<var>w</var> ← <var>w</var> − <span class='fr'><span><var>α m̂</var></span><span>√<var>v̂</var> + <var>ε</var></span></span>")
      + hint("m = running mean of the gradient (momentum). v = running mean of the <em>squared</em> "
             "gradient (bumpiness). ADAptive Moment estimation — not a person's name."),
      "c2/w2-11-advanced-optimization.html"),

    C("c2w2-conv", "concept",
      "What makes a <b>convolutional</b> layer different from a dense layer?",
      bullets(["each unit sees only a <b>small window</b>, not every input",
               "all units <b>share the same weights</b> (one kernel, slid along)"])
      + "<p>Result: far fewer parameters, faster training, less overfitting — and a detector learned in "
        "one place works everywhere.</p>"
      + hint("The restriction <em>is</em> the benefit: it encodes the true fact that nearby pixels are "
             "related and position should not change what a thing is."),
      "c2/w2-12-additional-layer-types.html"),

    C("c2w2-backprop-cost", "concept",
      "Why is <b>backpropagation</b> the reason deep learning is possible at all?",
      "<p>It computes <b>all N derivatives in about two forward passes</b>, regardless of N.</p>"
      + bullets(["nudging each parameter separately → N forward passes",
                 "forward-mode autodiff → still N sweeps",
                 "<b>backprop → 1 forward + 1 backward</b>"])
      + hint("For a million parameters that is 2 passes instead of a million. Reverse-mode autodiff is "
             "efficient exactly when you have many inputs and one output — the shape of a loss function."),
      "c2/w2-15-larger-network-example.html"),

    C("c2w2-chain-rule", "formula",
      "The <b>chain rule</b>, as backprop uses it.",
      blk("<span class='fr'><span>∂<var>J</var></span><span>∂<var>w</var></span></span> = "
          "<span class='fr'><span>∂<var>J</var></span><span>∂<var>d</var></span></span> · "
          "<span class='fr'><span>∂<var>d</var></span><span>∂<var>a</var></span></span> · "
          "<span class='fr'><span>∂<var>a</var></span><span>∂<var>c</var></span></span> · "
          "<span class='fr'><span>∂<var>c</var></span><span>∂<var>w</var></span></span>")
      + "<p>Multiply the <b>local slopes</b> along the path. Each node only needs to know its own little "
        "multiplier.</p>"
      + hint("Start at ∂J/∂J = 1 and work right to left. The forward values must be kept — which is why "
             "training uses far more memory than inference."),
      "c2/w2-14-computation-graph.html"),

    C("c2w2-mse-vs-bce", "trap",
      "Why not use <b>mean squared error</b> for classification?",
      "<p>It runs, and it trains badly. The gradient is <b>tiny exactly where the model is confidently "
      "wrong</b> — which is where you most need a big correction.</p>"
      + hint("Same reason as Course 1 Week 3: the sigmoid and the log loss are a matched pair whose "
             "derivatives cancel cleanly."),
      "c2/w2-02-training-details.html"),
])

W3 = deck("C2", 3, "Advice for Applying ML", [
    C("c2w3-diagnostic", "formula",
      "The <b>central diagnostic</b>: which number tells you about bias, and which about variance?",
      bullets(["<b>J<sub>train</sub> high</b> → <b>high bias</b> (underfitting)",
               "<b>J<sub>cv</sub> ≫ J<sub>train</sub></b> → <b>high variance</b> (overfitting)",
               "both can be true at once"])
      + hint("<b>J<sub>train</sub> tells you about bias. The gap tells you about variance.</b> One "
             "sentence, and it is most of the diagnostic value of the whole week."),
      "c2/w3-04-bias-and-variance.html"),

    C("c2w3-three-sets", "concept",
      "Why <b>three</b> data splits and not two?",
      bullets(["<b>train (60%)</b> — fits w and b",
               "<b>cross-validation (20%)</b> — chooses the model: degree, λ, architecture, features",
               "<b>test (20%)</b> — read <b>once</b>, at the very end"])
      + "<p>Any number you use to <b>make a decision</b> becomes optimistically biased. Selecting on the "
        "test set converts it into a second cv set.</p>"
      + hint("Report J<sub>test</sub>, never J<sub>cv</sub>, as your final number."),
      "c2/w3-03-model-selection.html"),

    C("c2w3-fix-table", "algorithm",
      "Six things to try. Which fix <b>high variance</b> and which fix <b>high bias</b>?",
      two(bullets(["get more training examples", "try a smaller set of features", "try increasing λ"]),
          bullets(["try getting additional features", "try adding polynomial features", "try decreasing λ"]),
          "High variance", "High bias")
      + hint("Every variance fix makes the model <b>less</b> flexible; every bias fix makes it <b>more</b> "
             "flexible. You can regenerate the table from that sentence alone."),
      "c2/w3-08-what-to-try-revisited.html"),

    C("c2w3-more-data", "trap",
      "When does <b>collecting more data</b> not help?",
      "<p>When you have <b>high bias</b>. More data is on the variance list <em>only</em>.</p>"
      + hint("It is also the most expensive item on the list. Teams routinely spend a quarter collecting "
             "data for a model that was never going to benefit — which is what the diagnostic prevents."),
      "c2/w3-08-what-to-try-revisited.html"),

    C("c2w3-baseline", "concept",
      "Why is “J<sub>train</sub> = 10.8%” meaningless on its own, and what are the <b>two gaps</b>?",
      "<p>High compared to what? If humans score 10.6% on the same audio, 10.8% is nearly perfect.</p>"
      + bullets(["<b>baseline → J<sub>train</sub></b> = <b>avoidable bias</b>",
                 "<b>J<sub>train</sub> → J<sub>cv</sub></b> = <b>variance</b>"])
      + hint("Chasing error below the noise floor of your own labels is a way to spend a year overfitting."),
      "c2/w3-06-baseline-performance.html"),

    C("c2w3-learning-curves", "concept",
      "How do you read a <b>learning curve</b> to decide whether more data will help?",
      two(bullets(["both curves <b>flatten early</b>", "well above the baseline", "small gap",
                   "→ more data will <b>not</b> help"]),
          bullets(["J<sub>train</sub> below the baseline", "<b>large gap</b>",
                   "J<sub>cv</sub> still falling at the right edge", "→ more data <b>will</b> help"]),
          "High bias", "High variance")
      + hint("J<sub>train</sub> <b>rises</b> with m — fitting 1000 points is harder than fitting 3. "
             "That is expected, not a bug."),
      "c2/w3-07-learning-curves.html"),

    C("c2w3-nn-recipe", "algorithm",
      "The <b>neural network recipe</b> — two questions, two fixes.",
      steps(["Does it do well on the <b>training</b> set? (vs the baseline)",
             "No → <b>bigger network</b>. Go back to 1.",
             "Yes → does it do well on the <b>cv</b> set?",
             "No → <b>more data</b> (or more regularisation). Go back to 1.",
             "Yes → done."])
      + hint("A larger network with proper regularisation is almost never worse than a smaller one. "
             "So “too big” is a compute problem, not an accuracy problem."),
      "c2/w3-09-bias-variance-neural-networks.html"),

    C("c2w3-error-analysis", "algorithm",
      "How do you actually do <b>error analysis</b>?",
      steps(["take the <b>misclassified cross-validation</b> examples",
             "sample ~100 if there are more",
             "read them, inventing overlapping categories as you go",
             "<b>count</b> each category",
             "work on the biggest one that is also tractable"])
      + hint("The classic outcome: the team has argued for two weeks about a category that turns out to "
             "be 3 of 100. Meanwhile a 21-of-100 category had nobody on it."),
      "c2/w3-11-error-analysis.html"),

    C("c2w3-augmentation", "concept",
      "What is the one rule for <b>data augmentation</b>?",
      "<p>The distortion must be <b>representative of what actually happens in real data</b>.</p>"
      + bullets(["speech → add café noise, car noise, a bad phone line ✓",
                 "clean scanned text → random per-pixel noise ✗ — it will never meet that",
                 "handwritten digits → mirror flipping ✗ — a mirrored 2 is not a 2"])
      + hint("Augment the <b>training set only</b>. Never the cv or test set."),
      "c2/w3-12-adding-data.html"),

    C("c2w3-transfer", "algorithm",
      "<b>Transfer learning</b> — the two options and when to use each.",
      two("train <b>only the new output layer</b><br>very small dataset (tens–hundreds)",
          "train <b>all</b> parameters, starting from theirs<br>larger dataset (thousands+)",
          "1 · Freeze", "2 · Fine-tune")
      + "<p>Replace only the <b>last</b> layer — it is the only genuinely task-specific part.</p>"
      + hint("When you unfreeze, drop the learning rate by 10–100×. A normal α destroys the pre-trained "
             "weights in the first few steps. Also: the <b>input type must match</b>."),
      "c2/w3-13-transfer-learning.html"),

    C("c2w3-precision-recall", "formula",
      "<b>Precision</b> and <b>recall</b> — and the trick for never mixing them up.",
      blk("precision = <span class='fr'><span>TP</span><span>TP + FP</span></span> &nbsp;&nbsp;·&nbsp;&nbsp; "
          "recall = <span class='fr'><span>TP</span><span>TP + FN</span></span>")
      + bullets(["<b>precision</b> — of those we <b>flagged</b>, how many were real?",
                 "<b>recall</b> — of those that were <b>real</b>, how many did we catch?"])
      + hint("<b>Precision's denominator is what you predicted. Recall's is what was true.</b> Hold onto "
             "that one difference."),
      "c2/w3-16-skewed-datasets.html"),

    C("c2w3-accuracy-trap", "trap",
      "Why is <b>accuracy</b> useless on a 0.5%-positive dataset?",
      "<p><code>print(\"healthy\")</code> scores <b>99.5% accuracy</b> and catches nobody.</p>"
      + "<p>On skewed data, accuracy is essentially a measurement of how rare the positive class is.</p>"
      + hint("Report precision, recall and F1. Never accuracy alone."),
      "c2/w3-16-skewed-datasets.html"),

    C("c2w3-f1", "formula",
      "<b>F1</b> — the formula, and why the <em>harmonic</em> mean specifically.",
      blk("F<sub>1</sub> = 2 · <span class='fr'><span>P · R</span><span>P + R</span></span>")
      + "<p>Because it sits close to the <b>smaller</b> of the two. P = 1.0 with R = 0.01 gives F1 ≈ 0.02, "
        "not 0.5.</p>"
      + hint("It refuses to be impressed by a model that is excellent at one half and useless at the other."),
      "c2/w3-16-skewed-datasets.html"),

    C("c2w3-threshold", "concept",
      "Which way do you move the <b>threshold</b>, and who decides?",
      bullets(["<b>raise it</b> (0.9) → precision ↑, recall ↓ — when a false alarm is expensive",
               "<b>lower it</b> (0.15) → recall ↑, precision ↓ — when a miss is much worse"])
      + "<p>The model gives a probability. The threshold turns it into an <b>action</b>, and the right "
        "one depends on what an action <b>costs</b>.</p>"
      + hint("That is a product decision, not a modelling one — and F1 is a poor way to make it, because "
             "it weights the two errors equally."),
      "c2/w3-17-precision-recall-tradeoff.html"),

    C("c2w3-fairness", "concept",
      "Your model is 92.4% accurate overall. What is the next thing to measure?",
      "<p>Performance <b>per subgroup</b> — accuracy, false positives and false negatives, broken down.</p>"
      + "<p>Aggregate accuracy hides subgroup failure <b>by construction</b>: a group that is 6% of your "
        "data can be served terribly with no visible effect on the headline.</p>"
      + hint("Removing the sensitive attribute does <b>not</b> make a model fair — postcode, name and "
             "purchase history are proxies. You just lose the ability to measure the disparity."),
      "c2/w3-15-fairness-bias-ethics.html"),

    C("c2w3-leakage", "trap",
      "Three ways a <b>train/test split</b> can silently lie to you.",
      bullets(["<b>splitting after sorting</b> — the halves are different populations. Shuffle first "
               "(unless it is a time series, where you must split by time)",
               "<b>duplicate entities</b> — the same house or patient in both sets",
               "<b>scaling before splitting</b> — μ and σ computed over everything leaks test info"]),
      "c2/w3-02-evaluating-a-model.html"),
])

W4 = deck("C2", 4, "Decision Trees", [
    C("c2w4-tree-decisions", "concept",
      "What are the <b>two decisions</b> that define the tree-learning algorithm?",
      steps(["<b>which feature to split on?</b> → the one that makes the two groups purest "
             "(maximum information gain)",
             "<b>when to stop?</b> → node is 100% one class · max depth reached · gain too small · "
             "too few examples"])
      + hint("Every stopping rule exists for one reason: keeping the tree <b>small</b>. Depth is the "
             "tree's equivalent of polynomial degree."),
      "c2/w4-02-learning-process.html"),

    C("c2w4-entropy", "formula",
      "<b>Entropy</b> — the formula and the two endpoints.",
      blk("<var>H</var>(<var>p</var>) = −<var>p</var> log<sub>2</sub>(<var>p</var>) − (1 − <var>p</var>) log<sub>2</sub>(1 − <var>p</var>)")
      + bullets(["<b>H = 0</b> — completely pure (p = 0 or p = 1)",
                 "<b>H = 1</b> — maximum mess (p = 0.5), exactly one bit",
                 "<b>symmetric</b>: H(0.8) = H(0.2) = 0.72"])
      + hint("“If I reach into this bag, how surprised will I be?” Base 2 gives bits, so a 50/50 bag is "
             "one coin flip of uncertainty."),
      "c2/w4-03-measuring-purity.html"),

    C("c2w4-infogain", "formula",
      "<b>Information gain</b> — and the part everyone forgets.",
      blk("gain = <var>H</var>(<var>p</var><sub>root</sub>) − ( <b><var>w</var><sup>left</sup></b><var>H</var>(<var>p</var><sup>left</sup>) + <b><var>w</var><sup>right</sup></b><var>H</var>(<var>p</var><sup>right</sup>) )")
      + "<p>The <b>weights</b> are the fraction of examples going each way.</p>"
      + hint("Without them, splitting off a single example into its own perfectly pure branch looks "
             "fantastic every time. This is the most common bug in the assignment."),
      "c2/w4-04-information-gain.html"),

    C("c2w4-id-column", "trap",
      "A customer-ID feature would score a <b>perfect</b> information gain. Why is that a problem?",
      "<p>Every leaf holds one example and is perfectly pure — maximum gain. But the rule “if ID = 4471 "
      "then cat” tells you nothing about a new customer. Pure memorisation.</p>"
      + hint("C4.5 fixes this with <em>gain ratio</em>. The practical fix: never feed an ID column to a "
             "tree."),
      "c2/w4-04-information-gain.html"),

    C("c2w4-continuous", "algorithm",
      "How does a tree split on a <b>continuous</b> feature like weight?",
      steps(["sort the examples by that feature",
             "consider each midpoint between consecutive distinct values (<b>m − 1</b> candidates)",
             "compute the information gain for each",
             "keep the best threshold, and let that be the feature's score"])
      + hint("This is also why trees need <b>no feature scaling</b> — they only ever <em>compare</em> "
             "values, never add them."),
      "c2/w4-07-continuous-features.html"),

    C("c2w4-regtree", "concept",
      "What single substitution turns a classification tree into a <b>regression</b> tree?",
      two("entropy → split by <b>information gain</b><br>leaf predicts the <b>majority class</b>",
          "<b>variance</b> → split by <b>variance reduction</b><br>leaf predicts the <b>mean</b>",
          "Classification", "Regression")
      + hint("Everything else — recursion, stopping rules, one-hot, thresholds — is identical. "
             "Note a regression tree predicts a <b>step function</b> and cannot extrapolate."),
      "c2/w4-08-regression-trees.html"),

    C("c2w4-onehot", "concept",
      "Why <b>one-hot encode</b> instead of mapping {red, green, blue} to {0, 1, 2}?",
      "<p>Because ordinal encoding tells the model blue is <b>bigger</b> than red, and twice green. For "
      "unordered categories that is a lie.</p>"
      + hint("For genuinely <em>ordered</em> categories (S &lt; M &lt; L) ordinal encoding is correct and "
             "better — one-hot throws the order away."),
      "c2/w4-06-one-hot-encoding.html"),

    C("c2w4-why-ensemble", "concept",
      "Why is a single decision tree <b>high variance</b>?",
      "<p>The root split is a single argmax. If two features score 0.281 and 0.278, a tiny change in the "
      "data flips which wins — and <b>everything below the root</b> is then built on a different "
      "foundation.</p>"
      + hint("Averaging only helps if the models make <b>different</b> mistakes. Three identical trees "
             "vote identically and gain you nothing."),
      "c2/w4-09-using-multiple-trees.html"),

    C("c2w4-bootstrap", "number",
      "In a <b>bootstrap sample</b> of size m drawn with replacement, what fraction of the distinct "
      "originals appears?",
      blk("1 − (1 − 1/<var>m</var>)<sup><var>m</var></sup> → 1 − 1/<var>e</var> ≈ <b>0.632</b>")
      + "<p>About <b>63%</b> appear; the other ~37% are “<b>out-of-bag</b>” and make a free validation "
        "set for that tree.</p>"
      + hint("<code>replace=True</code> is the whole trick. Without it you get a permutation of the same "
             "data and every tree is identical."),
      "c2/w4-10-sampling-with-replacement.html"),

    C("c2w4-random-forest", "algorithm",
      "The <b>random forest</b> algorithm — and the one thing that makes it more than bagging.",
      steps(["for b = 1…B: draw a bootstrap sample",
             "train a tree on it — but at <b>every node</b>, choose the split from a random subset of "
             "<b>k ≈ √n</b> features",
             "predict by majority vote (or average, for regression)"])
      + "<p>The feature subsampling is the addition. Without it a dominant feature wins the root in nearly "
        "every bag and the trees correlate.</p>"
      + hint("More trees never hurts accuracy — only compute. Past ~100 the gains flatten."),
      "c2/w4-11-random-forest.html"),

    C("c2w4-boosting", "distinguish",
      "<b>Random forest</b> vs <b>boosting</b>.",
      two(bullets(["trees built <b>independently</b>, in parallel", "sampling is <b>uniformly random</b>",
                   "deep, fully grown trees", "rarely overfits", "almost no tuning"]),
          bullets(["trees built <b>sequentially</b>, each fixing the last", "sampling <b>focuses on "
                   "current errors</b>", "<b>shallow</b> trees (depth 3–6)", "<b>can</b> overfit — needs "
                   "early stopping", "learning rate matters"]),
          "Random forest", "Boosting / XGBoost")
      + hint("Boosting is one student re-doing only the questions they got wrong. It usually wins."),
      "c2/w4-12-xgboost.html"),

    C("c2w4-boost-shallow", "concept",
      "Why are boosted trees kept <b>shallow</b> (depth 3–6)?",
      "<p>Each tree only needs to make a <b>small correction</b>. The ensemble supplies the power. Deep "
      "trees would overfit their residuals, and the sequential process amplifies that.</p>"
      + hint("Also why boosting cannot parallelise across trees: tree b needs the errors of trees 1…b−1. "
             "XGBoost parallelises <em>within</em> each tree instead."),
      "c2/w4-12-xgboost.html"),

    C("c2w4-tree-vs-nn", "concept",
      "Tabular data vs images — which model, and what is the neural network's decisive advantage?",
      bullets(["<b>tabular / spreadsheet</b> → <b>trees (XGBoost) first</b>. Fast, no scaling needed, "
               "readable, still the thing to beat",
               "<b>images, audio, text</b> → <b>neural networks</b>, no contest"])
      + "<p>The decisive NN advantage: <b>composability</b>. Everything is differentiable, so you can "
        "chain several networks and train the whole stack with one gradient. You cannot do that with "
        "trees.</p>",
      "c2/w4-13-trees-vs-neural-networks.html"),
])

DECKS = [W1, W2, W3, W4]
