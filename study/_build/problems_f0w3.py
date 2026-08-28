# -*- coding: utf-8 -*-
"""F0 W3 — the maths behind the curtain."""
from problemkit import P, m, pre, cols

L = []
def add(*a, **k): L.append(P(*a, **k))

add("f0w3-p01", level=1, tag="eigenvectors",
    lesson="f0/w3-01-eigenvectors.html",
    ask="Show that %s is an eigenvector of %s, and find its eigenvalue."
        % (m("v = [1, 1]"), m("A = [[2, 1], [1, 2]]")),
    gist="Multiply the matrix by the vector and see whether the answer points the same way.",
    steps=[("Row 1", "2(1) + 1(1) = 3"),
           ("Row 2", "1(1) + 2(1) = 3"),
           ("So Av =", "[3, 3]"),
           ("Is that a multiple of [1, 1]?", "yes — exactly 3 times it")],
    answer="%s, so v is an eigenvector with %s." % (m("Av = [3, 3] = 3v"), m("lambda = 3")),
    check="Try [1, −1] as well: Av = [1, −1], so that is the second eigenvector with λ = 1.",
    why="An eigenvector is a direction the matrix does not rotate. For those directions a whole "
        "matrix collapses into a single number — which is why they are worth finding.")

add("f0w3-p02", level=2, tag="PCA connection",
    lesson="f0/w3-01-eigenvectors.html",
    ask="A covariance matrix has eigenvalues %s. What fraction of the variance does the first "
        "principal component keep, and what does the second eigenvalue tell you?"
        % m("4.976 and 0.064"),
    steps=[("Total variance", "4.976 + 0.064 = 5.040"),
           ("First component's share", "4.976 ÷ 5.040"),
           ("As a percentage", "98.7%")],
    answer="The first component keeps %s of the variance. The second eigenvalue being tiny means "
           "the data is almost one-dimensional — it lies close to a straight line." % m("98.7%"),
    why="Each eigenvalue IS the variance along its own eigenvector. That is the fact that makes "
        "“direction of greatest variance” and “largest eigenvector of the covariance” the same "
        "instruction.")

add("f0w3-p03", level=2, tag="SVD",
    lesson="f0/w3-02-svd.html",
    ask="A centred 5 × 2 dataset has singular values %s. Show these carry the same information as "
        "the covariance eigenvalues from the previous problem." % m("4.988 and 0.567"),
    hint="Square them and divide by the number of examples.",
    steps=[("Square the first", "4.988² = 24.880"),
           ("Divide by n = 5", "24.880 ÷ 5 = 4.976"),
           ("Square the second", "0.567² = 0.321"),
           ("Divide by n", "0.321 ÷ 5 = 0.064")],
    answer="%s and %s — exactly the covariance eigenvalues. The two computations are the same "
           "thing." % (m("4.976"), m("0.064")),
    check="This is why real PCA implementations take the SVD of the centred data instead of "
          "eigendecomposing the covariance matrix — forming that matrix squares the data and "
          "loses precision.",
    why="One idea, two computational routes. Knowing they are the same turns two black boxes "
        "into one.")

add("f0w3-p04", level=2, tag="maximum likelihood",
    lesson="f0/w3-03-maximum-likelihood.html",
    ask="You flip a coin 10 times and get 7 heads. Write the likelihood as a function of the bias "
        "%s, evaluate it at 0.5 and 0.7, and say which the data prefers." % m("p"),
    steps=[("Likelihood", "L(p) = p⁷(1 − p)³"),
           ("At p = 0.5", "0.5⁷ × 0.5³ = 0.000977"),
           ("At p = 0.7", "0.7⁷ × 0.3³ = 0.002224"),
           ("Compare", "0.7 makes the observed data over twice as likely")],
    answer="%s. The data is more than twice as probable under p = 0.7, and that is the maximum "
           "likelihood estimate — which happens to equal 7/10." % m("L(p) = p^7 (1-p)^3"),
    check="The MLE for a coin is always k/n. Here that is 7/10 = 0.7, matching the peak.",
    why="Intuition would have said 0.7 anyway. The value of the derivation is that the same "
        "principle works where intuition has nothing to say — and it is where cross-entropy "
        "comes from.")

add("f0w3-p05", level=3, tag="deriving a loss",
    lesson="f0/w3-03-maximum-likelihood.html",
    ask="Assume a binary outcome where the model predicts probability %s. Write the probability of "
        "one observation %s, then take the negative log. What loss function have you derived?"
        % (m("f"), m("y")),
    hint="Write one expression that gives f when y = 1 and (1 − f) when y = 0.",
    steps=[("Probability of one observation", "f^y (1 − f)^(1−y)"),
           ("Check y = 1", "f¹(1−f)⁰ = f ✓"),
           ("Check y = 0", "f⁰(1−f)¹ = 1 − f ✓"),
           ("Negative log", "−[y log f + (1 − y) log(1 − f)]")],
    answer="%s — which is exactly the logistic loss from C1 W3, derived rather than asserted."
           % m("L = -y log f - (1-y) log(1-f)"),
    why="C1 W3 said this “comes from statistics” and moved on. This is the statistics: the log is "
        "there because the likelihood is a product, and logs turn products into sums.")

add("f0w3-p06", level=3, tag="softmax gradient",
    lesson="f0/w3-05-softmax-gradient.html",
    ask="Scores are %s and the true class is the first. Compute the softmax, then the gradient "
        "%s, and explain the sign of each entry." % (m("z = [2, 1, 0.5]"), m("dL/dz")),
    hint="The gradient of softmax with cross-entropy collapses to p − y.",
    steps=[("Exponentiate (subtracting the max first)", "e⁰ = 1, e⁻¹ = 0.368, e⁻¹·⁵ = 0.223"),
           ("Sum", "1.591"),
           ("Softmax", "[0.6285, 0.2312, 0.1402]"),
           ("One-hot y", "[1, 0, 0]"),
           ("Subtract", "[−0.3715, 0.2312, 0.1402]")],
    answer="%s. The true class is <b>negative</b> — gradient descent will push its score up. The "
           "other two are positive, so their scores get pushed down."
           % m("dL/dz = [-0.3715, 0.2312, 0.1402]"),
    check="Verified numerically by nudging each score by 1e-6: the measured derivative matches to "
          "four decimal places.",
    why="Two genuinely messy derivatives cancel to one subtraction. This is why softmax and "
        "cross-entropy are always specified together, and why from_logits=True exists.")

SET = dict(course="F0", week=3, title="The maths behind the curtain",
           lede="These answer questions the earlier courses raised and left open. Take them after "
                "Course 3 rather than before — each one lands much harder when you remember being "
                "asked to accept the thing it derives.",
           problems=L)
