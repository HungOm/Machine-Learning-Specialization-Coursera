# -*- coding: utf-8 -*-
"""C2 W2 — training, activations, softmax and backprop."""
from problemkit import P, m, pre, cols

L = []
def add(*a, **k): L.append(P(*a, **k))

add("c2w2-p01", level=2, tag="softmax",
    lesson="c2/w2-07-softmax.html",
    ask="A softmax layer receives logits %s. Compute the four probabilities. "
        "Use %s, %s, %s, %s."
        % (m("z = [2, 1, 0, 3]"), m("e² ≈ 7.389"), m("e¹ ≈ 2.718"),
           m("e⁰ = 1"), m("e³ ≈ 20.086")),
    hint="Exponentiate every logit, add them up, then divide each by the total.",
    steps=[("Exponentiate", "7.389, 2.718, 1.000, 20.086"),
           ("Sum", "7.389 + 2.718 + 1.000 + 20.086 = 31.193"),
           ("Divide each by the sum", "7.389/31.193 = 0.237"),
           ("…and the rest", "2.718/31.193 = 0.087 · 1/31.193 = 0.032 · 20.086/31.193 = 0.644"),
           ("Check they add to 1", "0.237 + 0.087 + 0.032 + 0.644 = 1.000")],
    answer=m("[0.237, 0.087, 0.032, 0.644]") + " — they sum to 1, and the largest logit "
           "became the largest probability.",
    why="Softmax is “exponentiate then normalise”. Exponentiating is what makes it winner-"
        "favouring: a logit 1 bigger becomes e ≈ 2.7 times more probable.")

add("c2w2-p02", level=2, tag="softmax properties",
    lesson="c2/w2-07-softmax.html",
    ask="Show that adding the same constant to every logit does not change the softmax "
        "output. Use %s and %s to check numerically, then explain why this "
        "fact is used in real implementations."
        % (m("z = [2, 1, 0]"), m("z = [12, 11, 10]")),
    hint="Write out the fraction for one class and factor e^c out of the top and bottom.",
    steps=[("With logits z_k + c, the numerator is e^(z_i+c) = e^c · e^z_i",
            "and every denominator term picks up the same e^c"),
           ("The e^c cancels top and bottom", "softmax(z + c) = softmax(z)"),
           ("Numerically: e² + e¹ + e⁰ = 7.389 + 2.718 + 1 = 11.107",
            "→ [0.665, 0.245, 0.090]"),
           ("And e¹² + e¹¹ + e¹⁰ = 162754.8 + 59874.1 + 22026.5 = 244655.4",
            "→ [0.665, 0.245, 0.090] — identical"),
           ("Implementations subtract max(z) first, making the largest exponent e⁰ = 1",
            "prevents overflow on large logits")],
    answer="Both give %s. Libraries exploit this by subtracting "
           "%s before exponentiating, so nothing ever overflows."
           % (m("[0.665, 0.245, 0.090]"), m("max(z)")),
    why="This is the “numerical stability” that <code>from_logits=True</code> buys you in "
        "Keras — the same reason the course tells you to use a linear output layer.")

add("c2w2-p03", level=3, tag="from_logits",
    lesson="c2/w2-09-improved-softmax.html",
    ask="Why does the course recommend a <code>linear</code> output activation plus "
        "<code>SparseCategoricalCrossentropy(from_logits=True)</code> instead of a "
        "<code>softmax</code> output with the default loss? Give the numerical argument.",
    hint="Think about what happens to log(p) when p has already been rounded to a float.",
    steps=[("With softmax first, the model computes p = e^z/Σe^z, rounds it to float32, "
            "then the loss computes log(p)", "two lossy steps"),
           ("If p underflows to 0, log(0) is −inf", "NaN loss"),
           ("With from_logits=True, Keras keeps the raw z and computes log-softmax directly",
            "log(e^z_i/Σ) = z_i − log Σ e^z"),
           ("That form never forms the tiny probability at all, and the log-sum-exp is "
            "computed with the max subtracted", "no underflow, no overflow"),
           ("Cost: the model's output is now logits, so you must apply softmax yourself "
            "to read probabilities", "tf.nn.softmax(model(X))")],
    answer="Computing the softmax and then its log loses precision twice and can underflow to "
           "log(0) = −inf. <code>from_logits=True</code> lets Keras use the algebraically "
           "equivalent %s, which is stable. The trade-off is that "
           "the model now outputs logits, not probabilities."
           % m("z<sub>i</sub> − log Σ e<sup>z</sup>"),
    why="This is the one place in the course where a mathematically irrelevant rearrangement "
        "changes whether your training run survives. Worth remembering as a pattern.")

add("c2w2-p04", level=1, tag="activations",
    lesson="c2/w2-04-choosing-activations.html",
    ask="Choose the output activation for each task:<br>"
        "(a) predict house price<br>(b) is this email spam?<br>"
        "(c) which of 10 digits is this?<br>(d) predict tomorrow's temperature change, "
        "which can be negative<br>(e) does this photo contain a car, a bus, and/or a "
        "pedestrian?",
    steps=[("(a) a positive number", "ReLU (or linear)"),
           ("(b) one probability", "sigmoid"),
           ("(c) one of 10 mutually exclusive classes", "softmax with 10 units"),
           ("(d) a number that can be negative", "linear"),
           ("(e) three independent yes/no answers, not mutually exclusive",
            "3 sigmoid units — multi-label, not multi-class")],
    answer="(a) ReLU/linear (b) sigmoid (c) softmax (d) linear (e) three sigmoids",
    why="(c) versus (e) is the multi-class / multi-label distinction. Softmax forces the "
        "probabilities to compete and sum to 1; independent sigmoids do not.")

add("c2w2-p05", level=2, tag="ReLU",
    lesson="c2/w2-03-sigmoid-alternatives.html",
    ask="Compute %s for %s. Then explain, using the sigmoid's "
        "shape, why ReLU trains faster in hidden layers."
        % (m("ReLU(z) = max(0, z)"), m("z = −3, −0.1, 0, 2, 7")),
    steps=[("Anything negative becomes 0", "0, 0, 0"),
           ("Anything positive passes through unchanged", "2, 7"),
           ("Sigmoid flattens at both ends: for z = 7 its slope is about 0.0009",
            "gradients nearly vanish"),
           ("A vanishing gradient means the weight barely updates, however wrong it is",
            "learning stalls"),
           ("ReLU's slope is exactly 1 for all positive z", "gradient passes through undiminished")],
    answer="%s. ReLU trains faster because its gradient is 1 wherever it "
           "is active, while a sigmoid's gradient collapses towards zero at both ends and "
           "stops the weights updating." % m("[0, 0, 0, 2, 7]"),
    why="Sigmoid is flat in two places; ReLU is flat in one. Halving the number of dead zones "
        "was enough to make much deeper networks trainable.")

add("c2w2-p06", level=3, tag="derivatives",
    lesson="c2/w2-13-what-is-a-derivative.html",
    ask="Estimate %s at %s numerically by nudging w by "
        "%s, then compare with the exact answer from calculus."
        % (m("d/dw of J = w²"), m("w = 3"), m("ε = 0.001")),
    hint="The definition of a derivative is the rise over the run for a tiny run. Just "
         "compute both values and divide.",
    steps=[("J at w = 3", "3² = 9"),
           ("J at w = 3.001", "3.001² = 9.006001"),
           ("Rise ÷ run", "(9.006001 − 9) ÷ 0.001 = 0.006001 ÷ 0.001 = 6.001"),
           ("Exact answer: d/dw w² = 2w = 6", "the estimate is off by 0.001 = ε")],
    answer="Numerically %s, exactly %s. The error is about ε, which is why "
           "gradient checking uses a small ε — and a two-sided difference to do better."
           % (m("6.001"), m("6")),
    why="This is precisely what a gradient-checking routine does to verify hand-written "
        "backprop. If your analytic gradient and this number disagree, the analytic one is "
        "usually wrong.")

add("c2w2-p07", level=3, tag="computation graph",
    lesson="c2/w2-14-computation-graph.html",
    ask="For %s with %s, %s, %s, compute the forward value, then use the "
        "chain rule backwards to find %s, %s and %s."
        % (m("J = (a − y)²"), m("a = wx + b"), m("x = 2, y = 5"), m("w = 3, b = 1"),
           m("∂J/∂a"), m("∂J/∂w"), m("∂J/∂b")),
    hint="Forward: compute a, then J. Backward: ∂J/∂a first, then multiply by ∂a/∂w and "
         "∂a/∂b as you step back through the graph.",
    steps=[("Forward: a = 3×2 + 1", "a = 7"),
           ("Forward: J = (7 − 5)²", "J = 4"),
           ("Back one step: ∂J/∂a = 2(a − y)", "2(7 − 5) = 4"),
           ("∂a/∂w = x, so ∂J/∂w = ∂J/∂a × x", "4 × 2 = 8"),
           ("∂a/∂b = 1, so ∂J/∂b = ∂J/∂a × 1", "4"),
           ("Check ∂J/∂w numerically: w = 3.001 gives a = 7.002, J = 4.008004; "
            "(4.008004 − 4)/0.001 = 8.004", "matches 8")],
    answer="%s, %s, %s, %s" % (m("a = 7"), m("J = 4"), m("∂J/∂w = 8"), m("∂J/∂b = 4")),
    why="This is backpropagation in full, on the smallest possible network. Every real "
        "backprop is this same right-to-left multiplication, just with more nodes.")

add("c2w2-p08", level=2, tag="Adam",
    lesson="c2/w2-11-advanced-optimization.html",
    ask="What problem does Adam solve that plain gradient descent has, and what does it do "
        "differently? Say specifically what happens to a parameter whose gradient keeps "
        "pointing the same way, and one whose gradient keeps flipping sign.",
    steps=[("Plain gradient descent uses one α for every parameter and never changes it",
            "you must pick it perfectly"),
           ("Adam keeps a separate step size per parameter", "no single α to get right"),
           ("Gradient consistently the same sign → the parameter is far from its optimum",
            "Adam increases that parameter's step"),
           ("Gradient flipping sign → it is bouncing across a minimum",
            "Adam decreases that parameter's step")],
    answer="Adam gives every parameter its <b>own</b> learning rate and adapts it: growing the "
           "step when the gradient keeps pointing the same way, shrinking it when the "
           "gradient keeps reversing. Plain gradient descent uses one fixed α for everything.",
    why="This is why the labs pass a much larger initial learning rate to Adam than you would "
        "dare with plain gradient descent — Adam will correct it.")

add("c2w2-p09", level=2, tag="training steps",
    lesson="c2/w2-02-training-details.html",
    ask="Match the three lines of Keras code to the three steps of training you already know "
        "from logistic regression."
        + pre("model = Sequential([...])\nmodel.compile(loss=BinaryCrossentropy())\nmodel.fit(X, y, epochs=100)"),
    steps=[("Sequential([...]) defines f(x) — the model's shape",
            "step 1: define the model"),
           ("compile(loss=...) states how wrong a prediction is",
            "step 2: define the cost function"),
           ("fit(...) runs gradient descent to minimise that cost",
            "step 3: minimise the cost"),
           ("Exactly the same three steps as logistic regression, in three lines",
            "the algorithm never changed, only the model")],
    answer="1 = define the model · 2 = define the cost · 3 = minimise it with gradient "
           "descent. The same three steps as Course 1, wrapped in a library.",
    why="Keras hides gradient descent, not replaces it. Knowing which line is which is what "
        "lets you debug a training run that is not converging.")

add("c2w2-p10", level=3, tag="multi-class cost",
    lesson="c2/w2-08-softmax-output-layer.html",
    ask="For a 3-class softmax the loss is %s. If the true class is 2 "
        "and the model outputs %s, compute the loss. Then compute it if the "
        "model had output %s. Use %s, %s."
        % (m("−log(a<sub>y</sub>)"), m("a = [0.1, 0.8, 0.1]"), m("a = [0.4, 0.3, 0.3]"),
           m("log 0.8 ≈ −0.223"), m("log 0.3 ≈ −1.204")),
    hint="Only the probability assigned to the *true* class matters. Everything else in the "
         "vector is ignored by the loss.",
    steps=[("True class is 2, so pick out a₂", "a₂ = 0.8"),
           ("Loss", "−log(0.8) ≈ 0.223"),
           ("Second case: a₂ = 0.3", "−log(0.3) ≈ 1.204"),
           ("The other entries never appear in the formula",
            "but they do affect a₂ through the normalisation")],
    answer="%s and %s. Being right but unsure costs about 5× more than being right and confident."
           % (m("0.223"), m("1.204")),
    why="This is why softmax and cross-entropy are always used together: the loss only reads "
        "one entry, and softmax is what makes pushing that entry up require pushing the "
        "others down.")

add("c2w2-p11", level=2, tag="epochs and batches",
    lesson="c2/w2-01-tensorflow-training.html",
    ask="You have 10,000 training examples, a batch size of 32, and train for 20 epochs. "
        "How many gradient-descent steps does that take? Why not just use the whole dataset "
        "for every step?",
    steps=[("Batches per epoch", "10,000 ÷ 32 = 312.5 → 313 batches"),
           ("Steps over 20 epochs", "313 × 20 = 6,260 updates"),
           ("Full-batch would give 20 updates total — far too few to converge",
            "and every step would be expensive"),
           ("Small batches also add useful noise that helps escape poor regions",
            "faster and often better")],
    answer="About <b>6,260</b> updates (313 batches × 20 epochs). Full-batch training would "
           "give only 20 updates in the same time, each one no more accurate in direction "
           "than a good batch estimate.",
    why="An epoch is one pass over the data, not one update. Confusing the two makes "
        "training-time estimates wrong by a factor of hundreds.")

add("c2w2-p12", level=3, tag="why activations, again",
    lesson="c2/w2-05-why-activations.html",
    ask="A colleague uses ReLU in every hidden layer but <b>linear</b> in one hidden layer in "
        "the middle. Does that middle layer add anything? Explain.",
    hint="Ask what the linear layer can express that the layer before and after could not "
         "already do together.",
    steps=[("A linear layer computes W₂(ReLU output) + b₂", "no new non-linearity"),
           ("The layer after it computes ReLU(W₃(W₂a + b₂) + b₃)",
            "= ReLU((W₃W₂)a + (W₃b₂ + b₃))"),
           ("W₃W₂ is a single matrix, so the pair behaves as one layer",
            "the linear layer folds into its neighbour"),
           ("It can still change the *width*, which sometimes matters for parameter count",
            "but it adds no expressive power")],
    answer="No — it folds into the next layer's weights, since %s is just "
           "another matrix. It changes the parameter count but not what the network can "
           "represent." % m("W₃W₂"),
    why="This is the same collapse argument as C2 W1 problem 11, applied locally. Any two "
        "adjacent linear layers are one linear layer wearing a disguise.")

add("c2w2-p13", level=2, tag="multi-label vs multi-class",
    lesson="c2/w2-10-multi-label.html",
    ask="For a self-driving car detecting cars, buses and pedestrians in one image, why is a "
        "3-unit softmax wrong? What is right, and what loss goes with it?",
    steps=[("Softmax forces the three probabilities to sum to 1", "they compete"),
           ("But an image can contain a car AND a pedestrian", "both should be near 1"),
           ("Softmax cannot express that — raising one must lower the others",
            "structurally wrong"),
           ("Correct: three independent sigmoid units", "each answers its own yes/no"),
           ("Loss: binary cross-entropy, summed over the three outputs",
            "three separate binary problems sharing a body")],
    answer="Softmax makes the classes mutually exclusive, but an image can contain several at "
           "once. Use <b>three sigmoid units</b> with binary cross-entropy on each — one "
           "network body, three independent yes/no heads.",
    why="The give-away question is always: can two of these be true at the same time? Yes "
        "means sigmoids, no means softmax.")

SET = dict(course="C2", week=2, title="Training, activations and softmax",
           lede="This week is where the library starts doing the work for you, which makes it "
                "the week where it matters most that you know what the library is doing. "
                "Several of these problems are about exactly that gap.",
           problems=L)
