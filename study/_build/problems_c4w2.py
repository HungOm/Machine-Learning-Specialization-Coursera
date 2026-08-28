# -*- coding: utf-8 -*-
"""C4 W2 — attention, computed by hand."""
from problemkit import P, m, pre, cols

L = []
def add(*a, **k): L.append(P(*a, **k))

TWO = ("Use this two-token example throughout: %s, %s, %s, and %s."
       % (m("Q = [[1,1],[2,0]]"), m("K = [[1,1],[0,2]]"), m("V = [[4,0],[0,8]]"), m("d_k = 2")))

add("c4w2-p01", level=1, tag="scores",
    lesson="c4/w2-03-attention-by-hand.html",
    ask=TWO + "<br>Compute %s — the raw score matrix." % m("QK^T"),
    gist="Dot each row of Q with each row of K. Four dot products, four numbers.",
    steps=[("q₁ · k₁", "[1,1]·[1,1] = 1 + 1 = 2"),
           ("q₁ · k₂", "[1,1]·[0,2] = 0 + 2 = 2"),
           ("q₂ · k₁", "[2,0]·[1,1] = 2 + 0 = 2"),
           ("q₂ · k₂", "[2,0]·[0,2] = 0 + 0 = 0")],
    answer=m("QK^T = [[2, 2], [2, 0]]"),
    why="Rows are queries (who is asking), columns are keys (who is offering). Keeping that "
        "straight is most of what it takes to read attention code.")

add("c4w2-p02", level=2, tag="scale and softmax",
    lesson="c4/w2-03-attention-by-hand.html",
    ask=TWO + "<br>Scale those scores by %s and softmax each row. Verify each row sums to 1."
        % m("√d_k"),
    hint="√2 = 1.4142. Softmax each row on its own — never down a column.",
    steps=[("Scale row 1", "[2, 2] ÷ 1.4142 = [1.4142, 1.4142]"),
           ("Softmax row 1", "both equal, so the weights split evenly → [0.5, 0.5]"),
           ("Scale row 2", "[2, 0] ÷ 1.4142 = [1.4142, 0]"),
           ("Exponentiate", "e^1.4142 = 4.1133, e^0 = 1, sum = 5.1133"),
           ("Divide", "4.1133/5.1133 = 0.8044, 1/5.1133 = 0.1956")],
    answer="Row 1: %s. Row 2: %s. Both sum to exactly 1."
           % (m("[0.5000, 0.5000]"), m("[0.8044, 0.1956]")),
    check="Row 1's two scores were equal, so an even split is the only sensible answer — a good "
          "sanity check that you softmaxed the right axis.",
    why="Rows summing to 1 is the check that catches the single most common attention bug. "
        "Softmaxing columns runs without error and produces meaningless output.")

add("c4w2-p03", level=2, tag="the output",
    lesson="c4/w2-03-attention-by-hand.html",
    ask=TWO + "<br>Using the weights from the previous problem, compute the final output.",
    steps=[("Output row 1", "0.5×[4,0] + 0.5×[0,8]"),
           ("", "= [2, 0] + [0, 4] = [2, 4]"),
           ("Output row 2", "0.8044×[4,0] + 0.1956×[0,8]"),
           ("", "= [3.2177, 0] + [0, 1.5646] = [3.2177, 1.5646]")],
    answer=m("output = [[2.000, 4.000], [3.218, 1.565]]"),
    check="Position 1 split its attention evenly and got an even blend of the two values. "
          "Position 2 leaned on the first value and its output reflects that.",
    why="Note the output has two rows — the same as the input. That shape preservation is exactly "
        "what lets attention layers stack twelve deep.")

add("c4w2-p04", level=2, tag="shapes",
    lesson="c4/w2-02-query-key-value.html",
    ask="A sequence has 64 positions, model width %s, and %s. What are the shapes of Q, of "
        "%s, and of the attention output? Which dimension disappears, and why?"
        % (m("d = 512"), m("d_k = d_v = 64"), m("QK^T")),
    steps=[("Q = XW_Q, where X is (64, 512) and W_Q is (512, 64)", "Q is (64, 64)"),
           ("QK^T: (64, 64) @ (64, 64)^T", "the inner 64 (d_k) meets and vanishes → (64, 64)"),
           ("Output: weights @ V, (64, 64) @ (64, 64)", "(64, 64)")],
    answer="Q is %s, %s is %s, output is %s. The dimension that disappears is %s — it was the "
           "inner dimension of the multiply, so the score grid depends only on how many "
           "<b>positions</b> there are."
           % (m("(64, 64)"), m("QK^T"), m("(64, 64)"), m("(64, 64)"), m("d_k")),
    why="It is a coincidence here that T and d_k are both 64. Redo it with T = 100 and d_k = 64 "
        "and you get a (100, 100) score grid — the shape rule is what tells you that.")

add("c4w2-p05", level=2, tag="scaling",
    lesson="c4/w2-05-why-scale.html",
    ask="Query and key components are roughly independent with variance 1. Explain why the "
        "standard deviation of their dot product is %s, and what goes wrong at %s if you skip "
        "the division." % (m("√d_k"), m("d_k = 512")),
    hint="A dot product is a sum of d_k terms. Variances of independent terms add.",
    steps=[("Each term q_i k_i has variance", "1 (product of two independent unit-variance values)"),
           ("Summing d_k independent terms", "variances add → total variance = d_k"),
           ("Standard deviation", "√d_k"),
           ("At d_k = 512", "√512 = 22.6 — measured empirically as 22.591"),
           ("Softmax of scores spread over ±22", "one weight → 1.0000, the rest → 0.0000")],
    answer="Variances of independent terms add, so summing %s of them gives variance %s and "
           "standard deviation %s. At that spread the softmax <b>saturates</b> into a hard "
           "one-hot, its gradient collapses to ~0, and the layer stops learning."
           % (m("d_k"), m("d_k"), m("√d_k")),
    why="Note it fails by <em>not training at all</em>, not by training badly. And early in "
        "training the position it commits to is essentially random, since the projections are "
        "still near-random.")

add("c4w2-p06", level=2, tag="multi-head budget",
    lesson="c4/w2-06-multi-head.html",
    ask="Compare the parameter count of one attention head of size 512 against eight heads of "
        "size 64. Count only the Q, K and V projections.",
    steps=[("One head of 512", "3 matrices of 512 × 512 = 3 × 262,144"),
           ("", "= 786,432"),
           ("One head of 64", "3 matrices of 512 × 64 = 3 × 32,768 = 98,304"),
           ("Eight of those", "8 × 98,304 = 786,432")],
    answer="Both are %s. Splitting into heads costs <b>nothing</b> — the budget is redistributed, "
           "not increased." % m("786,432"),
    check="Each head works in d/h dimensions, so h heads of size d/h is always the same total as "
          "one head of size d.",
    why="This is why multi-head is close to a free win, and why 8–16 heads is standard. Push it "
        "much further and each head has too few dimensions left to represent anything useful.")

add("c4w2-p07", level=3, tag="the cost",
    lesson="c4/w2-08-the-cost.html",
    ask="A model's context grows from 512 to 4,096 tokens. By what factor does the attention work "
        "grow? Then explain why the transformer beat the RNN despite being O(T²) against O(T).",
    steps=[("Length factor", "4096 ÷ 512 = 8"),
           ("Work factor", "8² = 64"),
           ("RNN cost", "O(T) operations, but strictly <b>serial</b>"),
           ("Attention cost", "O(T²) operations, but all <b>independent</b>"),
           ("On parallel hardware", "wall-clock time is operations ÷ how many run at once")],
    answer="<b>64×</b> the work. The transformer won because operation count is not wall-clock "
           "time: an RNN's T steps cost T units of <em>time</em> whatever hardware you own, while "
           "attention's T² operations run simultaneously.",
    why="A genuinely useful lesson beyond this course: asymptotic complexity assumes a sequential "
        "machine. When the hardware is massively parallel, the constant factors and the "
        "parallelisability can matter more than the exponent.")

SET = dict(course="C4", week=2, title="Attention",
           lede="Almost all of these use one two-token example, small enough to check on paper. "
                "Work through the first three in order — they are one calculation split into "
                "three, and doing it by hand once is worth more than reading it five times.",
           problems=L)
