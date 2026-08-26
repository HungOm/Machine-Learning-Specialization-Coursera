# -*- coding: utf-8 -*-
"""C2 W4 — decision trees, entropy, information gain and ensembles."""
from problemkit import P, m, pre, cols

L = []
def add(*a, **k): L.append(P(*a, **k))

CATS = cols(["#", "ear shape", "face shape", "whiskers", "cat?"],
            [[1, "pointy", "round", "present", 1],
             [2, "floppy", "not round", "present", 1],
             [3, "floppy", "round", "absent", 0],
             [4, "pointy", "not round", "present", 0],
             [5, "pointy", "round", "present", 1],
             [6, "pointy", "round", "absent", 1],
             [7, "floppy", "not round", "absent", 0],
             [8, "pointy", "round", "absent", 1],
             [9, "floppy", "round", "absent", 0],
             [10, "floppy", "round", "absent", 0]])

add("c2w4-p01", level=1, tag="entropy",
    lesson="c2/w4-03-measuring-purity.html",
    ask="Compute the entropy %s for a node containing "
        "(a) 5 cats and 5 dogs (b) 8 cats and 2 dogs (c) 6 cats and 0 dogs. "
        "Use %s, %s."
        % (m("H(p) = −p log₂ p − (1−p) log₂(1−p)"),
           m("log₂ 0.8 ≈ −0.322"), m("log₂ 0.2 ≈ −2.322")),
    hint="p is the fraction of one class. Entropy is highest at p = 0.5 and zero at p = 0 or 1.",
    steps=[("(a) p = 0.5", "−0.5(−1) − 0.5(−1) = 0.5 + 0.5 = 1.0"),
           ("(b) p = 0.8", "−0.8(−0.322) − 0.2(−2.322) = 0.258 + 0.464"),
           ("(c) p = 1 — the log of 1 is 0, and 0·log 0 is defined as 0", "0")],
    answer="(a) %s (b) %s (c) %s" % (m("H = 1.0"), m("H ≈ 0.722"), m("H = 0")),
    why="Entropy is “how surprised would you be by a random pick from this node”. A 50/50 "
        "node is maximally surprising; a pure node is not surprising at all.")

add("c2w4-p02", level=3, tag="information gain",
    lesson="c2/w4-04-information-gain.html",
    ask="Using the ten-animal dataset, compute the information gain from splitting on "
        "<b>ear shape</b>." + CATS
        + "Take %s and %s." % (m("H(0.8) ≈ 0.722"), m("H(0.2) ≈ 0.722")),
    hint="Three numbers: the root's entropy, then each child's entropy, then a weighted "
         "average of the children subtracted from the root.",
    steps=[("Root: 5 cats out of 10", "p = 0.5 → H = 1.0"),
           ("Pointy branch: examples 1, 4, 5, 6, 8 → cats 1, 5, 6, 8",
            "4 of 5 → p = 0.8 → H = 0.722"),
           ("Floppy branch: examples 2, 3, 7, 9, 10 → cat only 2",
            "1 of 5 → p = 0.2 → H = 0.722"),
           ("Weighted average of the children", "(5/10)(0.722) + (5/10)(0.722) = 0.722"),
           ("Gain = root − weighted children", "1.0 − 0.722")],
    answer=m("information gain ≈ 0.278"),
    why="The weighting by branch size is what stops the tree loving tiny pure branches. A "
        "pure leaf holding one example contributes almost nothing to the average.")

add("c2w4-p03", level=3, tag="choosing the split",
    lesson="c2/w4-05-putting-it-together.html",
    ask="For the same dataset, the gains are: ear shape %s, face shape %s, "
        "whiskers %s. (a) Which feature is the root? (b) After that split, what "
        "should the pointy branch split on, and why does that produce two leaves?"
        % (m("0.278"), m("0.035"), m("0.125")),
    steps=[("(a) pick the largest gain", "ear shape, 0.278"),
           ("(b) pointy branch holds examples 1, 4, 5, 6, 8 with labels 1,0,1,1,1",
            "entropy 0.722"),
           ("Split it on face shape: round → examples 1, 5, 6, 8, all cats",
            "4 of 4 → pure, H = 0"),
           ("not round → example 4 only, not a cat", "0 of 1 → pure, H = 0"),
           ("Gain = 0.722 − 0 = 0.722, the maximum possible",
            "both children are pure, so both become leaves")],
    answer="(a) <b>ear shape</b>. (b) Split on <b>face shape</b>: it separates the pointy "
           "branch perfectly into 4 cats and 1 non-cat, both pure, so recursion stops — "
           "gain %s." % m("0.722"),
    why="The tree stops when a node is pure because there is nothing left to gain. That is "
        "also the mechanism that lets trees overfit: keep splitting and every leaf becomes "
        "pure, including on noise.")

add("c2w4-p04", level=2, tag="one-hot encoding",
    lesson="c2/w4-06-one-hot-encoding.html",
    ask="Ear shape can be pointy, floppy or oval. Show the one-hot encoding, and explain why "
        "coding it as %s instead would be wrong.",
    steps=[("Three categories become three binary columns",
            "pointy → [1,0,0] · floppy → [0,1,0] · oval → [0,0,1]"),
           ("Exactly one column is 1, hence “one-hot”", "each row sums to 1"),
           ("Coding 1/2/3 asserts an ordering: oval > floppy > pointy", "which is meaningless"),
           ("It also asserts spacing: oval − floppy = floppy − pointy",
            "a split at 'ear > 1.5' would be arbitrary")],
    answer=cols(["ear shape", "is pointy", "is floppy", "is oval"],
                [["pointy", 1, 0, 0], ["floppy", 0, 1, 0], ["oval", 0, 0, 1]])
           + "Coding 1/2/3 invents an order and a spacing between categories that do not exist.",
    why="One-hot also makes every feature binary, which is exactly what the simple split rule "
        "needs. The same encoding lets you feed categorical data to a neural network.")

add("c2w4-p05", level=3, tag="continuous features",
    lesson="c2/w4-07-continuous-features.html",
    ask="Weight is a continuous feature. Describe precisely how a decision tree chooses a "
        "threshold for it, and how many candidate thresholds it must test for %s "
        "examples with distinct weights." % m("m"),
    steps=[("Sort the examples by weight", "w₍₁₎ < w₍₂₎ < … < w₍<sub>m</sub>₎"),
           ("A useful threshold must lie between two adjacent values — anywhere else gives "
            "the same split", "midpoints between consecutive pairs"),
           ("That is m − 1 candidates", "one per gap"),
           ("For each candidate, compute the information gain of that binary split",
            "then keep the best"),
           ("The same procedure is then repeated at every node, on every feature",
            "which is why trees are slow to train and fast to use")],
    answer="Sort by the value, try each <b>midpoint between consecutive values</b>, compute "
           "the information gain of each resulting binary split, and keep the best. That is "
           "%s candidates." % m("m − 1"),
    why="This is why a continuous feature is no harder in principle than a categorical one — "
        "the tree simply converts it into the best available yes/no question.")

add("c2w4-p06", level=2, tag="regression trees",
    lesson="c2/w4-08-regression-trees.html",
    ask="A regression tree predicts weight instead of a class. What replaces entropy as the "
        "measure of a node's quality, and what does a leaf predict? A leaf holds weights "
        "%s — what does it output?" % m("[7.2, 8.8, 7.6, 10.2]"),
    steps=[("Entropy measures disagreement about a label", "for numbers, use variance"),
           ("A split is scored by the weighted reduction in variance",
            "same formula, different impurity measure"),
           ("A leaf predicts the mean of its examples", "(7.2 + 8.8 + 7.6 + 10.2) ÷ 4"),
           ("Compute", "33.8 ÷ 4 = 8.45")],
    answer="<b>Variance</b> replaces entropy, and a leaf predicts the <b>mean</b> of its "
           "examples: %s." % m("8.45"),
    why="Everything else about the algorithm is unchanged. Swapping the impurity measure is "
        "the whole difference between a classification and a regression tree.")

add("c2w4-p07", level=2, tag="sampling with replacement",
    lesson="c2/w4-10-sampling-with-replacement.html",
    ask="You build a bagged ensemble from 10 training examples by sampling 10 examples "
        "<b>with replacement</b>. (a) Can an example appear twice? (b) Can one be missing "
        "entirely? (c) Roughly what fraction of the original examples appears in a given "
        "sample?",
    hint="For (c), the chance one specific example is missed on one draw is 9/10, and the "
         "draws are independent.",
    steps=[("(a) with replacement means it goes back in the pot", "yes, several times even"),
           ("(b) if one is drawn twice, another must be absent", "yes"),
           ("(c) P(a given example missed by all 10 draws) = (9/10)¹⁰",
            "≈ 0.349"),
           ("So the expected fraction present", "1 − 0.349 ≈ 0.651 — about 65%"),
           ("As m grows this tends to 1 − 1/e ≈ 0.632", "the classic bagging number")],
    answer="(a) yes (b) yes (c) about <b>65%%</b>, tending to %s as the "
           "dataset grows." % m("1 − 1/e ≈ 63.2%"),
    why="That variation is the entire point. Identical training sets would give identical "
        "trees, and averaging identical trees achieves nothing.")

add("c2w4-p08", level=3, tag="random forest",
    lesson="c2/w4-11-random-forest.html",
    ask="Bagged trees still tend to look alike — they usually all pick the same strong "
        "feature at the root. What extra randomisation does a random forest add, what is the "
        "usual amount, and why does it help?",
    steps=[("At each node, choose from a random subset of k of the n features",
            "not all n"),
           ("Typical choice", "k = √n"),
           ("Now a tree sometimes cannot use the dominant feature at the root",
            "it is forced to find a different structure"),
           ("More varied trees make more independent errors", "averaging cancels more of them"),
           ("With n = 100 features", "k = 10 considered at each node")],
    answer="At every node it considers only a <b>random subset of %s features</b> "
           "instead of all of them. This stops every tree from choosing the same root, so "
           "the trees decorrelate and averaging cancels more error." % m("k ≈ √n"),
    why="The key word is <i>decorrelate</i>. Averaging helps in proportion to how independent "
        "the errors are; identical trees average to exactly one tree.")

add("c2w4-p09", level=3, tag="boosting",
    lesson="c2/w4-12-xgboost.html",
    ask="Explain the one sentence that separates boosting from bagging, and say what "
        "consequence it has for whether the trees can be built in parallel.",
    steps=[("Bagging: each tree gets an independent random sample", "trees are independent"),
           ("Boosting: each new tree is trained with more weight on the examples the "
            "existing ensemble gets wrong", "trees are sequential"),
           ("So tree 2 cannot start until tree 1 has been evaluated",
            "no parallelism across trees"),
           ("Bagging can build all trees at once", "trivially parallel"),
           ("Boosting usually wins on accuracy for tabular data, at the cost of that "
            "sequential dependency", "the trade")],
    answer="Boosting trains each tree on the <b>mistakes of the ones before it</b>, whereas "
           "bagging trains each on an independent sample. That makes boosting inherently "
           "<b>sequential</b> — trees cannot be built in parallel — while bagging can build "
           "all of them at once.",
    why="It also explains why boosting overfits more readily: it deliberately chases the hard "
        "examples, and some hard examples are just mislabelled.")

add("c2w4-p10", level=2, tag="trees vs neural networks",
    lesson="c2/w4-13-trees-vs-neural-networks.html",
    ask="Choose trees or a neural network for each, and give the reason:<br>"
        "(a) a 40-column spreadsheet of loan applications<br>(b) classifying photographs<br>"
        "(c) a model a regulator must be able to audit<br>(d) a task where you want to reuse "
        "a pretrained model",
    steps=[("(a) tabular, mixed types, modest size", "trees — usually better and far faster"),
           ("(b) pixels, where structure and locality matter", "neural network"),
           ("(c) a single small tree is readable as a flowchart",
            "trees, though a forest is much less so"),
           ("(d) transfer learning is a neural-network property; trees have no equivalent",
            "neural network")],
    answer="(a) trees (b) neural network (c) trees (d) neural network",
    why="The honest summary: trees for tables, networks for unstructured data (images, audio, "
        "text) and for anything where you want to transfer learning.")

add("c2w4-p11", level=2, tag="overfitting trees",
    lesson="c2/w4-02-learning-process.html",
    ask="A tree grown with no depth limit reaches 100% training accuracy on any dataset with "
        "no contradictory rows. Explain why, and name three ways to stop it.",
    steps=[("Keep splitting and every leaf eventually holds one example", "trivially pure"),
           ("A leaf with one example predicts that example perfectly",
            "training accuracy 100%"),
           ("But those deep leaves encode noise, not pattern", "terrible on new data"),
           ("Stop 1: maximum depth", "limit how many questions deep it can go"),
           ("Stop 2: minimum examples per leaf", "refuse to split a node that is already small"),
           ("Stop 3: minimum information gain", "refuse a split that barely helps")],
    answer="Because splitting can continue until every leaf holds a single example, which is "
           "pure by definition. Stop it with a <b>maximum depth</b>, a <b>minimum number of "
           "examples per leaf</b>, or a <b>minimum information gain</b> per split.",
    why="100% training accuracy from a tree is a red flag, not a result. It is the tree "
        "equivalent of J_train ≈ 0 with a large gap to J_cv.")

add("c2w4-p12", level=3, tag="ensembles and variance",
    lesson="c2/w4-09-using-multiple-trees.html",
    ask="A single decision tree is famously unstable: change one training example and the "
        "whole tree can change shape. Explain why, and why that instability is exactly what "
        "makes ensembles work so well for trees.",
    hint="Think about what happens at the root when two features have gains of 0.281 and "
         "0.278.",
    steps=[("The root split is chosen by whichever gain is highest", "a hard argmax"),
           ("If two features are nearly tied, one changed example can flip the winner",
            "0.281 vs 0.278 → swap"),
           ("Flipping the root changes every subsequent split", "the entire tree differs"),
           ("So trees are high variance — very sensitive to the exact training sample",
            "unstable"),
           ("Averaging many high-variance, low-bias models cancels the variance while "
            "keeping the low bias", "exactly what bagging is for")],
    answer="Because each split is a hard <b>argmax</b> over gains, a near-tie can be flipped "
           "by one example, and flipping the root changes everything below it. That high "
           "variance is precisely what averaging removes — which is why ensembles help trees "
           "far more than they help most other models.",
    why="Averaging reduces variance and leaves bias alone. That is only a good trade for a "
        "model whose problem is variance — and a deep tree's problem is always variance.")

add("c2w4-p13", level=1, tag="reading a tree",
    lesson="c2/w4-01-decision-tree-model.html",
    ask="Trace this tree for an animal with <b>floppy</b> ears, a <b>round</b> face and "
        "<b>absent</b> whiskers."
        + pre("ear shape?\n├─ pointy  -> face shape?\n│                ├─ round     -> CAT\n│                └─ not round -> NOT CAT\n└─ floppy  -> whiskers?\n                 ├─ present -> CAT\n                 └─ absent  -> NOT CAT"),
    steps=[("Start at the root: ear shape?", "floppy → take the lower branch"),
           ("Next question on that branch: whiskers?", "absent → lower branch"),
           ("That is a leaf", "NOT CAT"),
           ("Note face shape was never consulted",
            "different paths ask different questions")],
    answer="<b>NOT CAT</b> — and notice the face-shape question was never reached.",
    why="This is why trees are readable: a prediction is a short path you can print out and "
        "hand to someone. It is also why a forest of 100 trees loses that property entirely.")

SET = dict(course="C2", week=4, title="Decision trees and ensembles",
           lede="Trees are the one algorithm here with no gradients and no learning rate. "
                "Everything is counting and comparing, which makes them ideal for doing on "
                "paper — and the arithmetic below is the actual lecture dataset.",
           problems=L)
