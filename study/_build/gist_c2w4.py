# -*- coding: utf-8 -*-
"""The gist of C2 Week 4."""
import math
from kit import key, trap
from gistkit import gistline, flow, sameskel, chain, bynumbers, retell, ladder, h2
from walkkit import cases, values, point, expr, chainset, ascii_art

def _H(p):
    if p in (0, 1): return 0.0
    return -p*math.log2(p) - (1-p)*math.log2(1-p)

GIST = dict(
    course="C2", week="4", title="Decision Trees", mins=12,
    scratch=["06-decision-tree"],
    lede="A completely different way of learning — no gradients, no learning rate, nothing "
         "random. And on tabular data it is still the thing to beat.",
    body="".join([
        gistline("""Everything so far descended a gradient. A tree does not. It asks
&ldquo;which question splits this group most cleanly?&rdquo;, splits, and asks again on each
half. That is the whole algorithm — and the interesting part of the week is why one tree is
never enough."""),

        h2("🖼", "The week in one picture"),
        flow([
            ("in", "A table with a label column", "No scaling needed. None."),
            ("arw", "measure the mess you are starting from"),
            ("op", "Entropy",
             "<b>H = 1</b> at a 50/50 split — maximum mess. <b>H = 0</b> when a group is all "
             "one class."),
            ("arw", "try every feature, and every threshold for numeric ones"),
            ("op", "Information gain",
             "Mess before, minus the <b>weighted</b> mess after. The weights are the part "
             "everyone forgets."),
            ("arw", "keep the best split and recurse into both halves"),
            ("back", "Repeat on each half",
             "Until pure, too deep, too few examples, or the gain is too small."),
            ("arw", "and now the problem: ONE tree is unstable"),
            ("op", "Build many, and disagree on purpose",
             "<b>Bootstrap</b> the rows, and at every node choose from a <b>random subset</b> "
             "of features."),
            ("out", "A forest, or a boosted ensemble",
             "Vote for classification, average for regression."),
        ], cap="""Every stopping rule exists for one reason: <b>keeping the tree small</b>. A
tree allowed to grow until every leaf is pure memorises perfectly and generalises terribly."""),

        h2("🔁", "Same goal, completely different machinery"),
        sameskel("""The <b>job</b> is the same as everything before: read a row of features,
predict a label, and generalise to rows you have not seen. Bias and variance still apply, and
so does everything from Week 3.""",
                 [("How it learns", "gradient descent", "<b>greedy search</b> — best split "
                                                        "now, then recurse"),
                  ("Learning rate", "essential", "<b>none</b>"),
                  ("Initialisation", "random, and it matters", "<b>none</b> — fully "
                                                               "deterministic"),
                  ("Feature scaling", "essential", "<b>irrelevant</b> — it only ever compares"),
                  ("What it optimises", "a differentiable cost", "<b>purity</b>, one split "
                                                                 "at a time"),
                  ("Main weakness", "local minima", "<b>high variance</b> — a tiny data "
                                                    "change rebuilds the whole tree")]),

        h2("🔢", "Entropy and information gain, by hand"),
        bynumbers("""Ten animals, five of them cats. Root entropy is <b>1.0</b> — maximum
mess. Here is what each feature buys.""",
                  [("H(0.5)", "%.4f" % _H(0.5), "the root: 5 cats out of 10"),
                   ("H(0.8)", "%.4f" % _H(0.8), "and H(0.2) is <b>the same</b> — entropy is symmetric"),
                   ("H(1.0)", "%.4f" % _H(1.0), "perfectly pure"),
                   ("ear shape", "gain = 0.2781", "splits 5/5, both halves at H = 0.7219"),
                   ("whiskers", "gain = 0.1245", "splits 4/6"),
                   ("face shape", "gain = 0.0349", "leaves both halves at 0.98 and 0.92 — "
                                                   "barely tidier"),
                   ("&rarr; split on", "ear shape", "eight times better than face shape")],
                  close="""The <b>weights</b> in the gain formula are load-bearing. Without
them, splitting a single example into its own perfectly pure branch scores brilliantly every
time — so the tree would learn to shave off one example per split, forever. This is the most
common bug when implementing a tree from scratch."""),

        h2("⚠️", "The demonstration that should change how you read a training score"),
        trap("""<p>The build lane's file 06 runs this tree on <b>pure noise</b>: 40 examples,
6 random binary features, labels generated with <b>no relationship to them whatsoever</b>.</p>
<p>Depth 1 → <b>0.675</b>. Depth 2 → <b>0.700</b>. Depth 3 → <b>0.800</b>. Depth 6 →
<b>0.900</b>.</p>
<p><b>Ninety percent training accuracy on data with no pattern in it</b>, climbing smoothly
the whole way, with nothing to warn you. On a real dataset that curve looks exactly like
progress.</p>
<p>This is the clearest possible argument for a validation set, and the reason every stopping
rule in the algorithm exists.</p>"""),

        h2("⛓", "Why one tree is never enough"),
        chain([
            dict(name="The instability",
                 does="The root split is a single argmax over feature scores.",
                 trap="Suppose two features score <b>0.281</b> and <b>0.278</b>. Change a "
                      "handful of examples and they swap — a <b>different root</b> is chosen, "
                      "and <b>everything below it</b> is built on a different foundation.",
                 feeds="so averaging many trees should help — but only if they make DIFFERENT "
                       "mistakes."),
            dict(name="Bootstrapping",
                 does="Draw m examples from m, <b>with replacement</b>, for each tree.",
                 code="idx = rng.integers(0, m, size=m)   # replace=True is the whole trick",
                 trap="About <b>63.2%</b> of the originals appear — the limit is "
                      "<b>1 − 1/e</b>. The missing 37% are <b>out-of-bag</b> and make a free "
                      "validation set. Without <code>replace=True</code> you get a "
                      "permutation, every tree is identical, and averaging achieves nothing.",
                 feeds="trees that saw different rows. Not yet different enough."),
            dict(name="Feature subsampling",
                 does="At <b>every node</b>, choose the split from a random subset of "
                      "k &asymp; &radic;n features.",
                 trap="This is what makes a random forest more than bagging. Without it a "
                      "<b>dominant feature wins the root in every tree</b>, and all B trees "
                      "come out nearly identical — exactly what averaging cannot fix.",
                 feeds="trees that genuinely disagree. Now the average is worth more than "
                       "the parts."),
            dict(name="Boosting",
                 does="Build trees <b>sequentially</b>, each one focusing on what the last "
                      "got wrong.",
                 trap="Trees are kept <b>shallow</b> (depth 3–6) because each only needs to "
                      "make a <b>small correction</b> — the ensemble supplies the power. And "
                      "boosting cannot parallelise across trees: tree b needs the errors of "
                      "trees 1…b−1.",
                 feeds=None),
        ]),

        h2("🌳", "Random forest vs boosting"),
        cases([("Random forest",
                "trees built <b>independently</b>, in parallel<br>sampling is uniformly "
                "random<br><b>deep</b>, fully grown trees<br>rarely overfits<br>almost no "
                "tuning"),
               ("Boosting / XGBoost",
                "trees built <b>sequentially</b>, each fixing the last<br>sampling focuses "
                "on current errors<br><b>shallow</b> trees, depth 3–6<br>can overfit<br>"
                "needs tuning")],
              "the dividing line is independent vs sequential; everything else follows"),

        h2("🆚", "Trees or neural networks?"),
        key("""<p><b>Tabular data</b> → trees first, XGBoost specifically. Fast, no scaling
needed, readable, and still the thing to beat on most spreadsheet-shaped problems.</p>
<p><b>Images, audio, text</b> → neural networks, no contest. A tree has no way to exploit the
fact that adjacent pixels are related.</p>
<p>The neural network's decisive long-term advantage is <b>composability</b>. Everything is
differentiable, so you can chain several networks and train the whole chain <b>end to end</b>
with one loss. A tree cannot pass a gradient back to whatever produced its inputs — which is
why every large modern system is a stack of networks, and why transfer learning and
fine-tuning are possible at all.</p>"""),

        h2("🗣", "Say the week back"),
        retell([
            "The two decisions that define tree learning, and why every stopping rule exists.",
            "What entropy measures, and what H(0) and H(1) both are.",
            "Why H(0.8) and H(0.2) are equal.",
            "The information gain formula — including the part everyone forgets, and what breaks without it.",
            "Why a customer-ID feature scores perfectly and is useless.",
            "How a tree splits on a continuous feature, and why that means no scaling is needed.",
            "The single substitution that turns a classification tree into a regression tree.",
            "Why one-hot rather than 0/1/2 — and the case where ordinal is <b>better</b>.",
            "Why a single tree is high variance, in terms of the root split.",
            "What fraction of originals a bootstrap sample contains, and what the rest are for.",
            "What random forests add to bagging, and why it is necessary.",
            "Why boosted trees are shallow, and why boosting cannot parallelise across trees.",
        ]),

        h2("🪜", "Where this week sits in the whole arc"),
        ladder("C2 W4", """This is the week that stops neural networks looking like the
answer to everything. Trees learn by a completely different mechanism, need none of the
preparation, and win on most tabular problems — which is most business problems. Course 2 ends
with two families rather than one, and the useful skill is knowing which shape of data you are
holding. Course 3 then changes the question entirely: no labels at all."""),
    ]),
)
