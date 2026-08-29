# -*- coding: utf-8 -*-
"""Mock quiz — C2 W4."""
from mockkit import Q, O, SET

SET = SET("C2", 4, "Decision Trees",
"""Entropy, information gain, the greedy split, and the two ways of combining trees. The entropy
arithmetic is worth doing on paper once before you sit this.""", [

Q("c2w4-q01",
  "<p>A node contains 6 cats and 0 dogs. What is its entropy?</p>",
  [O("0", True,
     "A pure node. p = 1, and H(1) = 0 — there is no uncertainty at all, so reaching in blind tells "
     "you nothing you did not know."),
   O("1", False,
     "H = 1 is the <em>maximum</em>, reached at exactly 50/50. This node is the opposite of that."),
   O("0.5", False,
     "Entropy is not the fraction. H(0.5) = 1, and H at p = 1 is 0."),
   O("6", False,
     "Entropy does not count examples — it measures the mix, and is between 0 and 1 for two "
     "classes.")],
  "c2/w4-03-measuring-purity.html", tag="entropy"),

Q("c2w4-q02",
  "<p>Why is information gain weighted by the number of examples in each child node?</p>",
  [O("So that a pure but tiny child does not outweigh a large impure one", True,
     "Without the weight, isolating 2 fraudulent transactions out of 100,000 into a perfect leaf "
     "scores spectacularly and is noise. The weighting makes gain mean &ldquo;tidier on "
     "average&rdquo;."),
   O("To keep the result between 0 and 1", False,
     "Gain is naturally bounded by the parent's entropy. The weighting is about meaning, not range."),
   O("To make the computation faster", False,
     "It costs a multiplication. Speed is not the reason."),
   O("Because entropy is undefined for small nodes", False,
     "Entropy is perfectly well defined for a node of size 1 — it is 0.")],
  "c2/w4-04-information-gain.html", tag="information gain",
  note="Dropping the weight is a real, silent bug: it trains, it scores well, it fails in production."),

Q("c2w4-q03",
  "<p>Which are true of the tree-building algorithm as taught?</p>",
  [O("It is greedy — it takes the best split now and never reconsiders", True,
     "Locally best at each node, with no lookahead. Cheap, usually good, and provably not optimal."),
   O("Finding the smallest tree that fits the data exactly is computationally hard", True,
     "NP-hard, which is why nobody does it and why greedy is the practical choice."),
   O("Adding one training example can change the entire tree", True,
     "If it changes the root split, everything beneath is rebuilt. This instability is real, expected, "
     "and a large part of why ensembles took over."),
   O("It considers all possible trees and picks the best", False,
     "That is the exhaustive search the greedy approach exists to avoid."),
   O("It always produces the tree with the fewest nodes", False,
     "Greedy gives no such guarantee. It gives a good tree quickly.")],
  "c2/w4-02-learning-process.html", tag="greedy splitting"),

Q("c2w4-q04",
  "<p>What must change to make a decision tree do <b>regression</b> rather than classification?</p>",
  [O("Split on variance reduction instead of entropy, and predict the mean at each leaf", True,
     "The algorithm is identical; only the measure of &ldquo;tidy&rdquo; changes, and the leaf holds "
     "an average instead of a majority vote."),
   O("Nothing — trees handle both without modification", False,
     "Entropy is defined over class proportions and has no meaning for a continuous target."),
   O("You must one-hot encode the target", False,
     "The target is a number. One-hot encoding applies to categorical <em>features</em>."),
   O("You must use a neural network for the leaves", False,
     "That is a model-tree variant and not what this course means by a regression tree.")],
  "c2/w4-08-regression-trees.html", tag="regression trees"),

Q("c2w4-q05",
  "<p>A house-price regression tree was trained on homes up to 400 m². What does it predict for a "
  "2,000 m² house?</p>",
  [O("The same value as for a 400 m² house", True,
     "Trees are piecewise-constant. There is no step beyond the last one, so it returns the value of "
     "the final region — for ever. Trees cannot extrapolate."),
   O("A proportionally higher price", False,
     "That is what a linear model would do. A tree has no notion of a trend to continue."),
   O("An error, since the value is out of range", False,
     "It predicts happily. It simply predicts the edge value."),
   O("Zero", False,
     "The leaf holds the mean of its training examples, which is not zero.")],
  "c2/w4-08-regression-trees.html", tag="extrapolation",
  note="Refusing to guess beyond what it has seen is sometimes the safest possible behaviour."),

Q("c2w4-q06",
  "<p>What does sampling <b>with replacement</b> mean when building a bagged ensemble?</p>",
  [O("Each draw returns an example to the pool, so a training set can contain duplicates", True,
     "Draw ten times from ten with replacement and you get ten entries, some repeated, some missing "
     "— on average about 63% of the originals appear at least once."),
   O("Each example appears exactly once in each new training set", False,
     "That would be a permutation, and every tree would see identical data — so every tree would be "
     "identical."),
   O("Examples are replaced with synthetic versions", False,
     "No new examples are created. The originals are drawn repeatedly."),
   O("The test set is replaced each round", False,
     "The test set is untouched. Resampling applies to training data only.")],
  "c2/w4-10-sampling-with-replacement.html", tag="the bootstrap",
  note="The ~37% left out each round are the out-of-bag sample — a free validation estimate."),

Q("c2w4-q07",
  "<p>What distinguishes a <b>random forest</b> from plain bagged trees?</p>",
  [O("At every split, only a random subset of features is available to choose from", True,
     "And crucially at <em>every node</em>, not once per tree. Without it, one dominant feature "
     "becomes the root split in all 500 trees and they average to roughly one tree."),
   O("Trees are built sequentially rather than in parallel", False,
     "That describes boosting. A forest builds independently, which is why it parallelises so well."),
   O("Each tree is trained on a different set of features only", False,
     "Rows are bootstrapped too. Both sources of variation are used."),
   O("Trees are pruned rather than depth-limited", False,
     "Forests typically grow trees deep and rely on averaging to control variance.")],
  "c2/w4-11-random-forest.html", tag="random forests"),

Q("c2w4-q08",
  "<p>How does boosting differ from a random forest?</p>",
  [O("Each tree is fitted to the errors the previous trees left behind", True,
     "Sequential rather than parallel. Every tree exists because of what the earlier ones got wrong, "
     "and the prediction is the running sum."),
   O("Boosting uses deeper trees", False,
     "Boosting typically uses <em>shallower</em> trees — often just a few levels — because each one "
     "only has to fix a little."),
   O("Boosting does not use a learning rate", False,
     "It does, and it matters: sequential fitting will keep chasing noise, so the learning rate exists "
     "to slow it deliberately."),
   O("Boosting cannot overfit", False,
     "It overfits more readily than a forest, for exactly the reason above.")],
  "c2/w4-12-xgboost.html", tag="boosting"),

Q("c2w4-q09",
  "<p>You have a spreadsheet of 40,000 customer records with mixed numeric and categorical columns "
  "and some missing values. Which model would you reach for first?</p>",
  [O("Gradient-boosted trees", True,
     "This is exactly the shape of data trees dominate — and they handle mixed types and missing "
     "values with far less preprocessing than a network needs."),
   O("A deep convolutional network", False,
     "Convolution assumes locality and translation invariance, which are properties of images. In a "
     "spreadsheet the column order is arbitrary, so the assumption encodes a relationship that does "
     "not exist."),
   O("A large transformer", False,
     "Enormously more expensive to train and serve, and on tabular data it routinely loses to "
     "boosting."),
   O("Linear regression with no feature engineering", False,
     "A reasonable baseline, and it cannot capture interactions between columns without you supplying "
     "them by hand.")],
  "c2/w4-13-trees-vs-neural-networks.html", tag="choosing a model",
  note="Decide by the shape of the data, not by fashion. It is a GPU-bill-sized decision."),

Q("c2w4-q10",
  "<p>Why should you avoid feeding a customer-ID column to a decision tree?</p>",
  [O("It gives perfect purity and enormous gain while being useless on new customers", True,
     "Every ID is unique, so splitting on it separates the training set perfectly. The tree memorises "
     "and learns nothing that transfers — a new customer has an ID the tree has never seen."),
   O("Trees cannot handle numeric columns", False,
     "They handle continuous features by choosing thresholds, which is a whole lesson of this week."),
   O("It would make training too slow", False,
     "Slower, yes; the fatal problem is that the result is worthless."),
   O("IDs must be one-hot encoded first", False,
     "One-hot encoding a high-cardinality ID column makes it worse — millions of columns, same "
     "memorisation.")],
  "c2/w4-06-one-hot-encoding.html", tag="high-cardinality features"),
])
