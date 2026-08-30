# -*- coding: utf-8 -*-
"""Walkthrough for 05_softmax.py."""
from walkkit import p, expr, chain, chainset, steps, cases, values, point, ascii_art

PICTURE = ([
    ("in", "One example", "It belongs to exactly one of three classes."),
    ("arw", "one weight vector per class"),
    ("op", "Three raw scores", "Called <b>logits</b>. Any numbers at all &mdash; "
                               "&minus;40, 0, +17. Not probabilities yet."),
    ("arw", "subtract the largest, then exponentiate &mdash; this order matters"),
    ("op", "Softmax",
     "Exponentiate to make everything positive, then divide by the total so they sum to "
     "exactly 1."),
    ("arw", "compare with the true class"),
    ("op", "Cross-entropy loss",
     "Only the <b>true</b> class's probability appears. Everything else is multiplied by "
     "zero."),
    ("arw", "and the gradient is startlingly simple"),
    ("back", "p &minus; y", "Predicted probabilities minus the one-hot truth. That is the "
                            "whole gradient."),
], "The whole program in one picture",
   "Compare with file 02. One sigmoid becomes three coupled outputs, and one log loss "
   "becomes cross-entropy. Everything else is untouched.")

WALK = {

"prelude": (
    p("""Binary classification asks &ldquo;yes or no&rdquo;. Multi-class asks &ldquo;which
one of these?&rdquo; This file builds that, and then spends most of its length on the
<b>numerical</b> problems softmax creates &mdash; because those are what
<code>from_logits=True</code> exists to solve.""")
),

"naive": (
    p("""Softmax written the obvious way, straight from the formula.""")
    + expr("e = np.exp(z)\nreturn e / e.sum()", "exponentiate, then normalise")
    + chain(["[2, 1, 0, 3]", "[0.237, 0.087, 0.032, 0.644]"], "and they sum to exactly 1.0")
    + point("""Two moves, each with one job. <b>exp</b> makes everything <b>positive</b>
&mdash; probabilities cannot be negative and raw scores routinely are. <b>Dividing by the
total</b> makes them <b>sum to 1</b>.""")
    + p("""Notice the exaggeration: a score of 3 is only 1.5&times; a score of 2, but its
probability is <b>2.7&times;</b> larger. Exponentiating widens every gap, which is what
makes softmax decisive.""")
),

"overflow": (
    p("""Now break it. Three scores that are perfectly ordinary as numbers.""")
    + chain(["[1000, 999, 998]", "[nan, nan, nan]"], "every answer destroyed")
    + point("""<code>exp(1000)</code> is a number with <b>435 digits</b>. It does not fit
in a float, so it becomes <code>inf</code>. Then <code>inf / inf</code> is <b>nan</b>
&mdash; not a number &mdash; and nan spreads through every subsequent calculation like
ink.""")
    + p("""The correct answer here is perfectly reasonable: [0.665, 0.245, 0.090]. Nothing
about the <b>maths</b> is extreme. Only the intermediate step was.""")
),

"stable": (
    p("""The fix is one subtraction, and it works because of a property worth
knowing.""")
    + expr("e = np.exp(z - np.max(z))\nreturn e / e.sum()", "subtract the largest first")
    + values([("softmax([2, 1, 0])", "[0.665241, 0.244728, 0.090031]", ""),
              ("softmax([12, 11, 10])", "[0.665241, 0.244728, 0.090031]", "<b>identical</b>")],
             "shift invariance, demonstrated")
    + point("""<b>Softmax depends only on the DIFFERENCES between the scores.</b> Adding a
constant to every score multiplies the top and the bottom by the same factor, which cancels
exactly.""")
    + p("""So subtracting the maximum is <b>free</b> &mdash; it cannot change the answer. And
afterwards the largest exponent is <code>exp(0) = 1</code> and everything else is smaller,
so <b>overflow is impossible</b>. Now [1000, 999, 998] returns [0.6652, 0.2447, 0.0900]
correctly.""")
    + point("""Every real softmax implementation does this. It is not an optimisation; it is
the difference between working and not.""")
),

"logsoftmax": (
    p("""A second, subtler failure &mdash; and this one the max-subtraction does not
fix.""")
    + steps(["<code>softmax([400, 0, -400])</code> gives "
             "<b>[1.0, 1.9e&minus;174, 0.0]</b>. The last one <b>underflowed to exactly "
             "zero</b>.",
             "Then take the log: <b>[0, &minus;400, &minus;inf]</b>.",
             "<b>&minus;inf</b>. And a gradient of inf is no gradient at all &mdash; "
             "training is over."])
    + p("""The fix is to never build the probability in the first place:""")
    + values([("softmax then log", "[0, &minus;400, &minus;inf]", "destroyed"),
              ("direct log_softmax", "[0, &minus;400, &minus;800]", "still usable")],
             "same maths, different order of operations")
    + point("""<b>Same maths, different order of operations, and only one of them
survives.</b> If the tiny number is never formed, it can never round to zero.""")
    + point("""This is exactly what <code>from_logits=True</code> does in Keras: it tells
the loss to take the <b>raw scores</b> and apply the rearranged formula itself, rather than
accepting probabilities that have already been damaged.""")
),

"loss": (
    p("""Cross-entropy, and why it is simpler than it looks.""")
    + expr("loss = -log( p[true_class] )", "only the true class appears")
    + point("""The full formula sums over all classes with a one-hot y &mdash; but y is
<b>0 everywhere except the true class</b>, so every other term is multiplied by zero and
vanishes. What is left is one logarithm.""")
    + p("""So the model is scored purely on <b>how much probability it gave to the right
answer</b>. Give it 0.99 and the loss is 0.01. Give it 0.01 and the loss is 4.61. It is the
same shape as the binary log loss in file 02, extended to more than two options.""")
),

"gradient": (
    p("""Two intimidating derivatives multiply together and almost everything
cancels.""")
    + expr("dz = p - y", "predicted probabilities minus the one-hot truth")
    + values([("gradient check", "2.805e&minus;10", "PASS")],
             "hand-derived against numerical")
    + point("""<b>That is the entire gradient.</b> No exponentials, no logs, no special
cases. The softmax derivative carries a factor of <b>p</b> and the log in cross-entropy
contributes <b>1/p</b>; they annihilate each other exactly.""")
    + p("""Read the signs. The <b>true</b> class gets a negative gradient &mdash; push its
score <b>up</b>. Every wrong class gets a positive one &mdash; push those <b>down</b>. The
size of each push is exactly how wrong that probability was.""")
    + point("""It is the same cancellation as sigmoid + log loss in file 02, which is why
these pairs are always used together. Pair either half with something else and you lose
this.""")
),

"train": (
    p("""Train it on three classes and watch two numbers at once.""")
    + values([("iter 0", "loss 1.0986, acc 0.333", "one in three &mdash; pure guessing"),
              ("iter 750", "loss 0.0297, acc 0.994", "essentially solved"),
              ("iter 3000", "loss 0.0183, acc 0.994", "polishing"),
              ("final", "accuracy 0.9944", "")],
             "training a 3-class classifier")
    + point("""<b>1.0986</b> at iteration 0 is not an arbitrary number. It is
<b>log(3)</b> &mdash; exactly the loss you get from assigning 1/3 to every class. A
3-class model that starts anywhere else has a bug in its initialisation.""")
    + p("""Notice accuracy reaches 0.994 by iteration 750 and then stops, while the loss
keeps falling. The model is no longer changing its <b>answers</b> &mdash; only becoming more
<b>confident</b> about the ones it already has.""")
),

"multilabel": (
    p("""The same three raw scores, sent through two different output heads. The answers are
completely different, and both are correct for their own question.""")
    + values([("softmax", "[0.615, 0.373, 0.011]", "sum = <b>1.0</b>"),
              ("three sigmoids", "[0.953, 0.924, 0.269]", "sum = <b>2.1457</b>")],
             "same logits, two heads")
    + cases([("Softmax &mdash; mutually exclusive",
              "The outputs are <b>coupled</b>. Raising one <b>must</b> lower the others, "
              "because they are forced to sum to 1."),
             ("Sigmoids &mdash; independent",
              "Each output decides on its own. They can all be high, or all low.")],
            "the structural difference")
    + point("""<b>A photo can contain a car AND a bus.</b> Softmax cannot say that &mdash;
it is built so the options compete. Independent sigmoids can.""")
    + p("""So the question that picks the head is not about accuracy: <b>can two answers be
true at once?</b> If yes, softmax is actively wrong, however good it looks.""")
),
}
