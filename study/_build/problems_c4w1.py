# -*- coding: utf-8 -*-
"""C4 W1 — sequences, embeddings, and why the old answers failed."""
from problemkit import P, m, pre, cols

L = []
def add(*a, **k): L.append(P(*a, **k))

add("c4w1-p01", level=1, tag="order",
    lesson="c4/w1-01-why-order-matters.html",
    ask="Write down the bag-of-words representation of “the man bit the dog” and of "
        "“the dog bit the man”. What does this prove about what a bag-of-words model can do?",
    gist="Count how often each word appears in each sentence, then compare the two counts.",
    steps=[("Sentence 1 counts", "the × 2, man × 1, bit × 1, dog × 1"),
           ("Sentence 2 counts", "the × 2, dog × 1, bit × 1, man × 1"),
           ("Compare", "identical")],
    answer="Both give %s — the model receives literally the same input, so it cannot "
           "distinguish them by any amount of training." % m("{the: 2, bit: 1, dog: 1, man: 1}"),
    why="This is not a weakness that more data fixes. It is a structural impossibility, which is "
        "why sequences needed a different kind of model rather than a bigger one.")

add("c4w1-p02", level=1, tag="one-hot",
    lesson="c4/w1-03-one-hot-and-why-it-fails.html",
    ask="A vocabulary has 30,000 words. Using one-hot vectors, how many parameters does a first "
        "layer of 256 units need? And what is the dot product between the vectors for any two "
        "different words?",
    steps=[("Each one-hot vector is", "30,000 long"),
           ("Weights into 256 units", "30,000 × 256 = 7,680,000"),
           ("Plus biases", "+ 256"),
           ("Dot product of two distinct one-hots", "the single 1s are in different slots, so "
            "every term is 1×0 or 0×0 → 0")],
    answer="%s parameters, and the dot product between <b>any</b> two distinct words is exactly "
           "%s." % (m("7,680,256"), m("0")),
    check="7.68 million parameters, and almost every multiplication is by zero.",
    why="The size problem is annoying. The dot product being zero for every pair is fatal — it "
        "means the encoding has already deleted every relationship the model could have used.")

add("c4w1-p03", level=2, tag="embeddings",
    lesson="c4/w1-04-embeddings.html",
    ask="A model has a vocabulary of 30,000 tokens and an embedding dimension of 256. How many "
        "parameters is the embedding table, and how does looking up a token relate to matrix "
        "multiplication?",
    hint="The table has one row per vocabulary item. For the second part, think about what "
         "multiplying a one-hot row vector by a matrix actually selects.",
    steps=[("Table shape", "(30,000, 256)"),
           ("Parameters", "30,000 × 256 = 7,680,000"),
           ("One-hot times E", "the single 1 selects exactly one row; every 0 deletes its row"),
           ("So a lookup is", "the same operation, without computing 29,999 multiplications by zero")],
    answer="%s parameters. A lookup is <b>identical</b> to multiplying the one-hot vector by the "
           "embedding matrix — it is the same matrix multiply, implemented as an index."
           % m("7,680,000"),
    why="Same parameter count as the one-hot layer in the previous problem — but now the numbers "
        "carry meaning instead of being 99.99% zeros. That is the whole trade.")

add("c4w1-p04", level=2, tag="similarity",
    lesson="c4/w1-04-embeddings.html",
    ask="Two words have embeddings %s and %s. Compute their cosine similarity, and say what the "
        "answer means." % (m("a = [3, 4]"), m("b = [4, 3]")),
    hint="Cosine = (a · b) ÷ (‖a‖ ‖b‖). Both norms happen to be the same here.",
    steps=[("Dot product", "3(4) + 4(3) = 12 + 12 = 24"),
           ("‖a‖", "√(9 + 16) = √25 = 5"),
           ("‖b‖", "√(16 + 9) = √25 = 5"),
           ("Cosine", "24 ÷ (5 × 5) = 24 ÷ 25")],
    answer=m("cos = 0.96") + " — very similar in direction, so these two words are being treated "
           "as closely related.",
    check="Both vectors have the same length, so the whole answer comes from the angle between "
          "them. Perfectly aligned would be 1.0.",
    why="Cosine divides out both lengths deliberately: a vector's magnitude tracks how often the "
        "token appeared in training, which is not what you want to compare meanings on.")

add("c4w1-p05", level=2, tag="vanishing gradient",
    lesson="c4/w1-06-why-rnns-failed.html",
    ask="An RNN backpropagates through 15 timesteps, and each step multiplies the gradient by "
        "about 0.4. What fraction of the gradient reaches the earliest step? What does that mean "
        "in practice?",
    steps=[("One factor per timestep", "0.4 multiplied 15 times"),
           ("Compute", "0.4¹⁵"),
           ("Result", "1.07 × 10⁻⁶")],
    answer="About %s — roughly one millionth of the signal. In practice the update never arrives, "
           "so the model cannot learn a dependency that spans 15 words." % m("1.1 × 10⁻⁶"),
    check="At the sigmoid's best-case slope of 0.25 it is far worse: 0.25¹⁵ = 9.3 × 10⁻¹⁰.",
    why="This is exactly the C2 W2 arithmetic — many slopes below 1 multiplied together. The only "
        "difference is that here there is one factor per <em>word</em>, and sentences are much "
        "longer than networks are deep.")

add("c4w1-p06", level=3, tag="the two failures",
    lesson="c4/w1-06-why-rnns-failed.html",
    ask="An LSTM substantially fixes one of the RNN's two problems and does nothing for the other. "
        "Say which is which, and explain why the second one cannot be fixed by any better cell "
        "design.",
    hint="One problem is about information surviving; the other is about what has to happen before "
         "what.",
    steps=[("Problem 1 — forgetting", "gradients multiplied once per step, so they vanish"),
           ("LSTM's answer", "gates let information pass through unchanged rather than being "
            "multiplied — usable range goes from ~10 steps to perhaps 100"),
           ("Problem 2 — serial dependency", "computing h⟨t⟩ requires h⟨t−1⟩ to exist first"),
           ("Why no cell design helps", "it is a data dependency, not a numerical one — step t "
            "genuinely needs step t−1's output as its input")],
    answer="LSTMs mitigate <b>forgetting</b>. They do nothing at all for the <b>serial "
           "dependency</b>, because that is architectural: no amount of engineering parallelises "
           "a computation whose step t requires step t−1.",
    why="This is the more important of the two for why transformers won. Parallelism is what made "
        "training on thousands of GPUs worth doing, and no RNN variant can offer it.")

add("c4w1-p07", level=3, tag="attention, 2014",
    lesson="c4/w1-07-the-bottleneck.html",
    ask="In 2014-style attention the context vector is %s. Explain why the α values must sum to 1, "
        "and why a softmax is used rather than simply selecting the highest-scoring position."
        % m("c = Σ α_t h⟨t⟩"),
    steps=[("What c is", "a weighted average of the position summaries"),
           ("If the weights did not sum to 1", "the output's magnitude would grow or shrink with "
            "sequence length, rather than reflecting content"),
           ("Why not pick the maximum", "argmax is a step function — its derivative is zero "
            "everywhere it is defined"),
           ("Consequence", "there would be no gradient with which to learn <em>where to look</em>")],
    answer="Summing to 1 makes it a genuine <b>average</b> rather than a length-dependent sum. "
           "Softmax rather than argmax because the selection itself must be differentiable — "
           "otherwise the model could never learn what to attend to.",
    why="“Make the discrete choice soft so it can be trained” is one of the most reusable ideas in "
        "deep learning. It shows up far beyond attention.")

SET = dict(course="C4", week=1, title="Sequences and embeddings",
           lede="Small numbers, all checkable by hand. The point of these is to make the failures "
                "of the pre-2017 answers concrete — because every design decision in Week 2 is a "
                "response to one of them.",
           problems=L)
