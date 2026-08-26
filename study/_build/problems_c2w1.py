# -*- coding: utf-8 -*-
"""C2 W1 — neurons, layers and forward propagation."""
from problemkit import P, m, pre, cols

L = []
def add(*a, **k): L.append(P(*a, **k))

add("c2w1-p01", level=1, tag="one neuron",
    lesson="c2/w1-04-neural-network-layer.html",
    ask="A single sigmoid neuron has %s and %s. Compute its output for "
        "%s. Use %s."
        % (m("<b>w</b> = [2, −1]"), m("b = 0.5"), m("<b>x</b> = [1, 3]"), m("e<sup>0.5</sup> ≈ 1.6487")),
    hint="Two steps, always: z = w·x + b, then a = g(z). A neuron is a dot product wearing a "
         "squash function.",
    steps=[("Dot product", "2×1 + (−1)×3 = 2 − 3 = −1"),
           ("Add b", "z = −1 + 0.5 = −0.5"),
           ("Sigmoid", "a = 1/(1 + e^0.5) = 1/(1 + 1.6487) = 1/2.6487")],
    answer=m("a ≈ 0.378"),
    why="Every neuron in every network you will build is exactly this. A layer is just "
        "several of them side by side, fed the same input.")

add("c2w1-p02", level=2, tag="layer shapes",
    lesson="c2/w1-11-general-forward-prop.html",
    ask="A network takes 4 input features and has layers of 5, 3 and 1 units. Give the shape "
        "of every weight matrix and bias vector, and the total number of parameters.",
    hint="A weight matrix for a layer is (inputs to that layer) × (units in that layer). Each "
         "unit gets one bias.",
    steps=[("Layer 1: 4 inputs → 5 units", "W₁ is (4, 5), b₁ is (5,) → 20 + 5 = 25"),
           ("Layer 2: 5 inputs → 3 units", "W₂ is (5, 3), b₂ is (3,) → 15 + 3 = 18"),
           ("Layer 3: 3 inputs → 1 unit", "W₃ is (3, 1), b₃ is (1,) → 3 + 1 = 4"),
           ("Total", "25 + 18 + 4 = 47")],
    answer="%s %s %s — <b>47 parameters</b>."
           % (m("W₁ (4,5), b₁ (5,)"), m("W₂ (5,3), b₂ (3,)"), m("W₃ (3,1), b₃ (1,)")),
    why="The number of inputs to a layer is the number of units in the previous layer. Get "
        "this rule and you can size any network on the back of an envelope.")

add("c2w1-p03", level=2, tag="forward propagation",
    lesson="c2/w1-10-forward-prop-single-layer.html",
    ask="A layer has two units. Unit 1: %s. Unit 2: %s. "
        "Input %s. Compute %s, using sigmoid. "
        "%s, %s."
        % (m("w = [1, 1], b = −1"), m("w = [−1, 2], b = 0"), m("x = [1, 2]"),
           m("a<sup>[1]</sup>"), m("e<sup>−2</sup> ≈ 0.1353"), m("e<sup>−3</sup> ≈ 0.0498")),
    steps=[("Unit 1: z = 1×1 + 1×2 − 1", "z₁ = 2"),
           ("Unit 1: a = 1/(1 + e⁻²) = 1/1.1353", "a₁ ≈ 0.881"),
           ("Unit 2: z = (−1)×1 + 2×2 + 0", "z₂ = 3"),
           ("Unit 2: a = 1/(1 + e⁻³) = 1/1.0498", "a₂ ≈ 0.953")],
    answer=m("a<sup>[1]</sup> ≈ [0.881, 0.953]"),
    why="Both units see the same input and produce different numbers, because they have "
        "different weights. That difference is the only reason a layer is more useful than "
        "one neuron.")

add("c2w1-p04", level=3, tag="vectorized forward prop",
    lesson="c2/w1-16-matmul-code.html",
    ask="Write <code>dense(A_in, W, b, g)</code> for one layer using matrix multiplication, "
        "where %s holds a whole batch. State the shape at each line."
        % m("A_in is (m, n_in)"),
    hint="Stacking each unit's weights as a column of W lets one matmul do every unit for "
         "every example at once.",
    steps=[("W is (n_in, n_out) — one column per unit", "A_in @ W → (m, n_out)"),
           ("b is (n_out,) and broadcasts down every row of the batch", "still (m, n_out)"),
           ("Apply the activation elementwise", "(m, n_out)"),
           ("The whole layer, whole batch, one expression", "return g(A_in @ W + b)")],
    answer=pre("def dense(A_in, W, b, g):\n    Z = A_in @ W + b     # (m, n_in) @ (n_in, n_out) -> (m, n_out)\n    return g(Z)          # (m, n_out)"),
    why="Compare this with the loop version in the Coffee Roasting NumPy lab. Identical "
        "arithmetic, one line, and hundreds of times faster on a real batch.")

add("c2w1-p05", level=2, tag="matmul rules",
    lesson="c2/w1-15-matmul-rules.html",
    ask="Which of these are legal, and what shape does each result have?<br>"
        "(a) %s (b) %s (c) %s (d) %s"
        % (m("(3,4) @ (4,2)"), m("(3,4) @ (2,4)"), m("(1,5) @ (5,1)"), m("(5,1) @ (1,5)")),
    hint="The two inner numbers must match. The two outer numbers become the answer's shape.",
    steps=[("(a) inner 4 and 4 match", "legal → (3, 2)"),
           ("(b) inner 4 and 2 do not match", "illegal"),
           ("(c) inner 5 and 5 match", "legal → (1, 1), a single number in a box"),
           ("(d) inner 1 and 1 match", "legal → (5, 5)")],
    answer="(a) %s &nbsp;(b) <b>illegal</b> &nbsp;(c) %s &nbsp;(d) %s"
           % (m("(3,2)"), m("(1,1)"), m("(5,5)")),
    why="(c) and (d) use the same two matrices in opposite orders and give a scalar or a 5×5. "
        "Order is not a detail in matrix multiplication.")

add("c2w1-p06", level=2, tag="TensorFlow",
    lesson="c2/w1-09-building-a-network-sequential.html",
    ask="Write the Keras code for a network with 3 input features, a hidden layer of 4 "
        "sigmoid units, and a single sigmoid output. Then say how many parameters Keras will "
        "report.",
    steps=[("Sequential stacks layers in order", "tf.keras.Sequential([...])"),
           ("Dense means fully connected; units is the layer's width",
            "Dense(4, activation='sigmoid')"),
           ("Output layer is one unit", "Dense(1, activation='sigmoid')"),
           ("Parameters: (3×4 + 4) + (4×1 + 1)", "16 + 5 = 21")],
    answer=pre("model = tf.keras.Sequential([\n    tf.keras.layers.Dense(4, activation='sigmoid'),\n    tf.keras.layers.Dense(1, activation='sigmoid'),\n])")
           + "Keras reports <b>21</b> parameters.",
    why="Notice you never state the input size in Dense — Keras infers it the first time it "
        "sees data. That is also why model.summary() fails before the model has been built.")

add("c2w1-p07", level=3, tag="what layers learn",
    lesson="c2/w1-03-recognizing-images.html",
    ask="In a face-recognition network, the first hidden layer learns short edges, the second "
        "learns eyes and noses, the third learns whole faces. Explain in terms of the maths "
        "why depth produces this progression.",
    steps=[("Layer 1 sees raw pixels; a weighted sum of neighbouring pixels can detect a "
            "brightness change", "an edge detector"),
           ("Layer 2 sees layer 1's outputs — a weighted sum of edge detectors",
            "a combination of edges is a corner, a curve, an eye"),
           ("Layer 3 sees layer 2's outputs — a combination of parts",
            "parts in the right arrangement make a face"),
           ("Each layer can only combine what the previous layer offers",
            "so complexity grows one level at a time")],
    answer="Each layer computes weighted combinations of the previous layer's features, so "
           "the vocabulary available grows by one level of composition per layer: pixels → "
           "edges → parts → objects. Depth is what buys composition.",
    why="This also explains why the network must be trained end to end: nobody tells layer 2 "
        "to look for eyes. It discovers that eyes are a useful combination of edges because "
        "that helps the final answer.")

add("c2w1-p08", level=2, tag="notation",
    lesson="c2/w1-11-general-forward-prop.html",
    ask="Decode this notation: %s. What is each of the "
        "superscripts and subscripts, and what shape is each object?"
        % m("a<sub>2</sub><sup>[3]</sup> = g(<b>w</b><sub>2</sub><sup>[3]</sup> · <b>a</b><sup>[2]</sup> + b<sub>2</sub><sup>[3]</sup>)"),
    steps=[("[3] in square brackets — the layer number", "third layer"),
           ("subscript 2 — which unit within that layer", "second unit"),
           ("a⁽²⁾ with no subscript — the whole output vector of layer 2",
            "the input to this unit"),
           ("w₂⁽³⁾ — that one unit's weight vector, one weight per input",
            "shape = number of units in layer 2"),
           ("a₂⁽³⁾ and b₂⁽³⁾ are single numbers", "scalars")],
    answer="Square brackets = layer, subscript = unit inside the layer. The unit takes the "
           "<i>whole</i> previous layer's output vector, dots it with its own weight vector, "
           "adds its own scalar bias, and squashes.",
    why="Superscript in square brackets is the layer; superscript in round brackets is the "
        "training example. Both appear in the same formulas and mean completely different things.")

add("c2w1-p09", level=3, tag="counting operations",
    lesson="c2/w1-13-vectorization.html",
    ask="A layer maps 1000 inputs to 500 units, on a batch of 64 examples. How many "
        "multiply-adds does the forward pass need? Why is doing this as one matmul faster "
        "than 64 × 500 separate dot products, given the arithmetic is identical?",
    steps=[("One unit, one example", "1000 multiply-adds"),
           ("500 units", "500 × 1000 = 500,000"),
           ("64 examples", "64 × 500,000 = 32,000,000"),
           ("Same total either way — the win is not fewer operations",
            "it is memory and dispatch"),
           ("A single matmul loads each weight once and reuses it across all 64 examples, "
            "keeps data in cache, and issues SIMD instructions; 32,000 separate dot products "
            "pay Python and memory-traffic overhead each time",
            "same maths, far better use of the hardware")],
    answer="<b>32 million</b> multiply-adds either way. The matmul is faster because it "
           "reuses each weight across the whole batch while it is still in cache and issues "
           "vector instructions, instead of paying per-call overhead 32,000 times.",
    why="This is why batching exists at all. It is not a statistical trick — it is about "
        "keeping the arithmetic units fed.")

add("c2w1-p10", level=1, tag="data shapes in TensorFlow",
    lesson="c2/w1-08-data-in-tensorflow.html",
    ask="You have a single example with two features and want to predict on it. Why does "
        "%s fail where %s works?"
        % (m("x = np.array([200, 17])"), m("x = np.array([[200, 17]])")),
    steps=[("The first is shape (2,) — a flat vector", "TensorFlow reads it as 2 examples "
            "with 1 feature each"),
           ("The second is shape (1, 2) — one row, two columns", "1 example with 2 features"),
           ("TensorFlow always expects (batch, features), even for a batch of one",
            "the outer dimension is examples")],
    answer="%s is (1, 2): one example, two features. %s is (2,), which "
           "TensorFlow reads as two examples of one feature each — the wrong way round."
           % (m("[[200, 17]]"), m("[200, 17]")),
    why="The double brackets in the labs are not a typo. Anything you pass to a Keras model "
        "must carry a batch dimension.")

add("c2w1-p11", level=2, tag="activation choice",
    lesson="c2/w1-06-forward-propagation.html",
    ask="What would a network compute if every layer used <b>no</b> activation function — "
        "that is, %s? Show it for two layers and state the consequence."
        % m("a = z"),
    hint="Substitute the first layer's output into the second and simplify.",
    steps=[("Layer 1", "a⁽¹⁾ = W₁x + b₁"),
           ("Layer 2", "a⁽²⁾ = W₂(W₁x + b₁) + b₂"),
           ("Expand", "= (W₂W₁)x + (W₂b₁ + b₂)"),
           ("W₂W₁ is just another matrix, and the bracket is just another vector",
            "= W′x + b′ — a single linear layer")],
    answer="It collapses to %s: one linear layer, however deep you stack it. "
           "Without a non-linear activation, depth buys you nothing at all." % m("W′x + b′"),
    why="This is the mathematical reason activations exist. Not to squash, not for "
        "probabilities — to stop the whole network folding into a single matrix.")

add("c2w1-p12", level=3, tag="coffee roasting",
    lesson="c2/w1-02-demand-prediction.html",
    ask="The coffee-roasting example has two features (temperature, duration) and a hidden "
        "layer of three units. After training, the three hidden units have learned "
        "“too cool”, “too long” and “about right”. Explain how a single output unit can turn "
        "those three into a good/bad decision, and what its weights probably look like.",
    steps=[("Each hidden unit outputs a number near 1 when its condition holds",
            "three detectors"),
           ("The output unit computes w·a + b over those three", "a weighted vote"),
           ("Good coffee needs “about right” on and the two failure detectors off",
            "positive weight on the third, negative on the first two"),
           ("For example w ≈ [−4, −4, +5], b ≈ −2",
            "either failure firing drives z negative")],
    answer="The output unit takes a <b>weighted vote</b>: strongly negative weights on the two "
           "failure detectors and a positive weight on the “about right” detector, so any "
           "failure firing pushes z below zero and the sigmoid towards 0.",
    why="This is what “the network learns its own features” means concretely. Nobody defined "
        "“too cool” — it emerged because it was a useful intermediate for the final answer.")

SET = dict(course="C2", week=1, title="Neurons, layers and forward propagation",
           lede="A neuron is a dot product and a squash. A layer is several of those. A "
                "network is layers feeding layers. These problems keep the arithmetic small "
                "enough to do on paper, so the shapes stay visible.",
           problems=L)
