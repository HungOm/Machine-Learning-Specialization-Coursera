# -*- coding: utf-8 -*-
"""C4 W3 — the transformer block, counted."""
from problemkit import P, m, pre, cols

L = []
def add(*a, **k): L.append(P(*a, **k))

add("c4w3-p01", level=1, tag="layer norm",
    lesson="c4/w3-03-layer-norm.html",
    ask="Apply layer normalization to one position's vector %s (ignore γ and β). Verify the "
        "result has mean 0 and standard deviation 1." % m("x = [1, 3, 5, 7]"),
    gist="Subtract the average, then divide by the spread. Exactly the z-score from Course 1.",
    steps=[("Mean", "(1 + 3 + 5 + 7) ÷ 4 = 4"),
           ("Deviations", "−3, −1, 1, 3"),
           ("Variance", "(9 + 1 + 1 + 9) ÷ 4 = 5"),
           ("Standard deviation", "√5 = 2.2361"),
           ("Divide each deviation", "−3/2.2361, −1/2.2361, 1/2.2361, 3/2.2361")],
    answer=m("[−1.342, −0.447, 0.447, 1.342]") + " — the values sum to 0, so the mean is 0, and "
           "their variance works out to exactly 1.",
    check="The result is symmetric because the input was evenly spaced. A quick sanity check: "
          "normalised values should mostly land between −2 and 2.",
    why="This is C1 W2's z-score with nothing added but two learned dials. The genuinely new part "
        "is <em>where</em> it happens — inside the network, at every layer.")

add("c4w3-p02", level=2, tag="residuals",
    lesson="c4/w3-02-residuals.html",
    ask="A 20-layer network has no residual connections and each layer multiplies the gradient by "
        "about 0.7. What fraction reaches layer 1? Then say what %s changes and why."
        % m("y = x + f(x)"),
    steps=[("Without residuals", "0.7²⁰"),
           ("Compute", "≈ 7.98 × 10⁻⁴"),
           ("With residuals, differentiate y = x + f(x)", "∂y/∂x = 1 + f′(x)"),
           ("The 1 is an identity path", "no chain of multiplications can shrink it below 1")],
    answer="About %s — under a thousandth. With residuals there is a route whose derivative is "
           "<b>1</b> at every layer, so the gradient reaches layer 1 undiminished at any depth."
           % m("8.0 × 10^-4"),
    why="Third appearance of the same enemy in this specialization: deep sigmoid networks, RNNs "
        "across time, and now depth. Recognising it on sight is worth more than any single fix.")

add("c4w3-p03", level=2, tag="block parameters",
    lesson="c4/w3-04-feed-forward.html",
    ask="For %s and %s, count the parameters in one transformer block: attention (four matrices), "
        "feed-forward (two), and the two layer norms. Which component is largest?"
        % (m("d = 256"), m("d_ff = 1024")),
    hint="Attention has W_Q, W_K, W_V and W_O, each d × d. Feed-forward has two matrices between "
         "d and d_ff. Each layer norm has a γ and a β, one per feature.",
    steps=[("Attention", "4 × 256 × 256 = 262,144"),
           ("Feed-forward", "2 × 256 × 1024 = 524,288"),
           ("Layer norms", "2 norms × 2 params × 256 = 1,024"),
           ("Total", "262,144 + 524,288 + 1,024")],
    answer="%s per block. The <b>feed-forward layer is largest</b> at 524,288 — exactly twice "
           "attention." % m("787,456"),
    check="It is always exactly twice: attention is 4d² and feed-forward is 2 × d × 4d = 8d².",
    why="The famous component is the smaller one. Two thirds of a transformer's block parameters "
        "sit in the plainest part of it.")

add("c4w3-p04", level=2, tag="whole model",
    lesson="c4/w3-08-counting-a-real-model.html",
    ask="Now build a whole small model: vocabulary 30,000, %s, context 512, and 6 blocks of the "
        "kind you just counted. What is the total, and what share is the embedding table?"
        % m("d = 256"),
    steps=[("Token embeddings", "30,000 × 256 = 7,680,000"),
           ("Positional embeddings", "512 × 256 = 131,072"),
           ("Six blocks", "6 × 787,456 = 4,724,736"),
           ("Total", "7,680,000 + 131,072 + 4,724,736")],
    answer="%s parameters, of which the token embedding table is %s — about <b>61%%</b>."
           % (m("12,535,808"), m("7,680,000")),
    check="In GPT-2 small the same table is 31.6%. The share falls as models get deeper, because "
          "the blocks grow while the vocabulary does not.",
    why="Worth noticing that at small scale the embedding table dominates. This is why tying the "
        "input and output embedding matrices is a common trick in small models.")

add("c4w3-p05", level=3, tag="positional encoding",
    lesson="c4/w3-01-positional-encoding.html",
    ask="Explain why every position's sinusoidal encoding has the <b>same magnitude</b>, and why "
        "several frequencies are used rather than one.",
    hint="Dimensions come in sin/cos pairs sharing a frequency. What is sin²θ + cos²θ?",
    steps=[("Each pair contributes", "sin²θ + cos²θ = 1, whatever θ is"),
           ("With d dimensions there are d/2 pairs", "squared length = d/2, for every position"),
           ("So the norm is √(d/2)", "identical at every position"),
           ("One frequency alone", "either repeats (distant positions collide) or moves too slowly "
            "to separate neighbours"),
           ("Several frequencies", "fast ones separate neighbours, slow ones separate distant "
            "positions")],
    answer="Every pair contributes exactly 1 to the squared length, so all positions have norm "
           "%s. Multiple frequencies are needed because a single one cannot both distinguish "
           "neighbours and stay unique over long distances." % m("√(d/2)"),
    check="For d = 8 the norm is √4 = 2 at every position — which is what the lesson's table shows.",
    why="Equal magnitude matters: if some positions had much larger encodings they would dominate "
        "the embedding they are added to, purely because of where the word happened to sit.")

add("c4w3-p06", level=3, tag="architecture",
    lesson="c4/w3-07-gpt-vs-bert.html",
    ask="You have a fixed budget and two tasks: (a) classify support tickets into eight "
        "categories, (b) draft replies to them. Which architecture family for each, and why?",
    steps=[("Task (a): the whole ticket is available", "nothing is being generated"),
           ("Bidirectional context helps", "words after a phrase inform its meaning"),
           ("Task (b): text is produced left to right", "each word conditioned on what came before"),
           ("That requires the causal mask", "and training on next-token prediction")],
    answer="(a) A <b>BERT-style encoder</b> — bidirectional context helps, and it is far cheaper "
           "to run for classification. (b) A <b>GPT-style decoder</b> — generation requires the "
           "causal mask and the next-token objective.",
    why="The instinct to reach for a generative model for everything is expensive and often worse. "
        "For pure classification an encoder is usually both more accurate and cheaper.")

SET = dict(course="C4", week=3, title="The transformer block",
           lede="Mostly counting. Being able to compute a model's parameters from its config is "
                "the difference between reading a model card and understanding one — and problems "
                "3 and 4 build to exactly that.",
           problems=L)
