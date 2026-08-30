# -*- coding: utf-8 -*-
"""Walkthrough for 06_decision_tree.py."""
from walkkit import p, expr, chain, chainset, steps, cases, values, point, ascii_art

PICTURE = ([
    ("in", "Ten animals", "Three yes/no features each, and whether it is a cat."),
    ("arw", "measure the mess you are starting from"),
    ("op", "Entropy of the whole group",
     "5 cats out of 10 is maximum mess: <b>H = 1.0</b>, exactly one bit."),
    ("arw", "try every feature"),
    ("op", "Information gain, per feature",
     "How much mess does splitting on this feature remove? <b>Weighted</b> by how many "
     "examples go each way."),
    ("arw", "keep the best one"),
    ("back", "Split, and recurse",
     "Each half becomes a new problem. Repeat on it, with fewer examples."),
    ("arw", "pure enough, or too deep, or too few left"),
    ("out", "A tree of yes/no questions",
     "Follow it down and the leaf you land on is the answer."),
], "The whole program in one picture",
   "No gradients, no learning rate, no initialisation. Just counting, comparing and "
   "recursion &mdash; which is why it is the odd one out in this lane.")

WALK = {

"prelude": (
    p("""Everything else in this lane descends a gradient. This file does not. There is no
learning rate, no initialisation, nothing random, and no cost to minimise by stepping.""")
    + point("""A decision tree is <b>greedy search</b>: take the best split available right
now, recurse into both halves, stop when a rule says to. That is a genuinely different way
of learning, and it is why trees need no feature scaling.""")
),

"data": (
    p("""Ten animals, five of them cats. Three yes/no features: ear shape, face shape,
whiskers.""")
    + point("""Ten examples is far too few for anything real and exactly right for
<b>checking by hand</b>. Every number this file prints can be verified with a pencil, which
is the point.""")
),

"entropy": (
    p("""Entropy measures <b>mess</b>. Read the table and the shape of the function becomes
obvious.""")
    + values([("5/10 cats", "p = 0.5", "H = <b>1.0000</b> &mdash; maximum mess"),
              ("8/10 cats", "p = 0.8", "H = 0.7219"),
              ("10/10 cats", "p = 1.0", "H = <b>0.0000</b> &mdash; perfectly pure"),
              ("0/10 cats", "p = 0.0", "H = <b>0.0000</b> &mdash; also perfectly pure"),
              ("1/10 cats", "p = 0.1", "H = 0.4690")],
             "entropy at a few purities")
    + point("""Note that <b>p = 0 and p = 1 both give zero</b>. Entropy measures mess, not
cat-ness. All cats and no cats are equally tidy.""")
    + ascii_art("""  H
  1.0 |         ___
      |      __/   \\__
      |    _/         \\_
      |  _/             \\_
  0.0 |_/                 \\_
      +----------------------- p
      0        0.5         1""")
    + p("""Base <b>2</b> gives the answer in <b>bits</b>, which is why a 50/50 split comes
out at exactly 1 &mdash; one yes/no question's worth of uncertainty. The intuition:
<b>&ldquo;if I reach into this bag, how surprised will I be?&rdquo;</b>""")
),

"gain": (
    p("""Try every feature, and measure how much mess each one removes.""")
    + expr("gain = H(root) - ( w_left &middot; H(left) + w_right &middot; H(right) )",
           "the mess before, minus the WEIGHTED mess after")
    + values([("ear shape", "gain = 0.2781", "5 left (4 cats), 5 right (1 cat)"),
              ("face shape", "gain = 0.0349", "7 left (4 cats), 3 right (1 cat)"),
              ("whiskers", "gain = 0.1245", "4 left (3 cats), 6 right (2 cats)")],
             "root entropy is 1.0000. Here is what each split buys")
    + point("""<b>Ear shape wins</b>, by a factor of eight over face shape. Look at why: it
splits 5/5 and leaves each half at H = 0.7219, whereas face shape leaves 0.9852 and 0.9183
&mdash; barely less messy than where it started.""")
    + p("""The <b>weights</b> are the part people forget when implementing this, and dropping
them breaks the algorithm entirely. Without them, splitting a single example into its own
perfectly pure branch scores brilliantly every time, so the tree would learn to shave off
one example per split forever.""")
),

"build": (
    p("""Now recurse. Same procedure, on each half.""")
    + ascii_art("""  root: ear shape?   (n=10, gain=0.2781)
     |
     +-- yes: face shape?   (n=5, gain=0.7219)
     |        +-- yes: LEAF -> CAT      (4/4 cats)
     |        +-- no:  LEAF -> NOT CAT  (0/1 cats)
     |
     +-- no:  whiskers?     (n=5, gain=0.7219)""")
    + point("""Notice the gain <b>rises</b> as you go down &mdash; 0.2781 at the root,
0.7219 one level in. That is normal: the sub-groups are smaller and more homogeneous, so a
single question can settle far more of what is left.""")
    + p("""The recursion is the whole algorithm. &ldquo;Build a tree&rdquo; is: find the best
split, then <b>build a tree</b> on each half. It bottoms out when a stopping rule fires.""")
),

"predict": (
    p("""Run all ten training animals back through the finished tree.""")
    + values([("training accuracy", "1.00", "10 out of 10"),
              ("predicted", "[1,1,0,0,1,1,0,1,0,0]", ""),
              ("actual", "[1,1,0,0,1,1,0,1,0,0]", "identical")],
             "the result")
    + point("""<b>Perfect training accuracy should worry you, not please you.</b> The tree
was allowed to grow until every leaf was pure, so of course it reproduces the data it was
built from &mdash; that is what it was optimising.""")
    + p("""It tells you nothing about a new animal. The next two sections are about exactly
this problem.""")
),

"continuous": (
    p("""Trees split on yes/no questions. A continuous feature like weight has no natural
yes/no, so the tree invents one.""")
    + steps(["<b>Sort</b> the examples by weight.",
             "Consider each <b>midpoint</b> between consecutive distinct values &mdash; "
             "here, <b>9 candidates</b> for 10 animals.",
             "Compute the information gain for each.",
             "Keep the best. Here that is a threshold of <b>9.00 kg</b>, with gain "
             "<b>0.6100</b>."])
    + point("""0.6100 beats every yes/no feature in this dataset &mdash; more than double
ear shape's 0.2781. A well-chosen numeric threshold is often far more informative than a
categorical flag.""")
    + p("""And this is exactly why <b>trees need no feature scaling</b>. The algorithm only
ever asks &ldquo;is this above or below that?&rdquo; &mdash; a comparison, unchanged if you
multiply every weight by a thousand. Gradient descent cares about scale because it takes
<i>steps</i>; a tree never does.""")
),

"overfit": (
    p("""The last section is a warning, built out of <b>pure noise</b>. Forty examples, six
random binary features, and labels with <b>no relationship to them whatsoever</b>.""")
    + values([("max depth 1", "0.675", "already above 0.5"),
              ("max depth 2", "0.700", ""),
              ("max depth 3", "0.800", ""),
              ("max depth 6", "0.900", "<b>90% on data with no pattern in it</b>")],
             "training accuracy on random noise")
    + point("""There is <b>nothing to learn here</b> &mdash; the labels were generated
independently of the features. Every point of that 90% is memorisation.""")
    + p("""And notice how smoothly it climbs. Nothing warns you. The tree does not know it is
memorising, the training accuracy looks better at every depth, and on a real dataset this
curve looks exactly like progress.""")
    + point("""This is why every stopping rule in the algorithm exists, and why a single
tree is almost never used alone. It is also the clearest possible argument for a
<b>validation set</b>: training accuracy simply cannot distinguish these two situations.""")
),
}
