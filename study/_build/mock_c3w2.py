# -*- coding: utf-8 -*-
"""Mock quiz — C3 W2."""
from mockkit import Q, O, SET

SET = SET("C3", 2, "Recommender Systems",
"""Collaborative filtering, content-based filtering, mean normalization and PCA. The
&ldquo;which one handles a brand-new item&rdquo; question comes up every time.""", [

Q("c3w2-q01",
  "<p>In collaborative filtering, what is learned?</p>",
  [O("Both the item features and the user parameters, at the same time", True,
     "That is what makes it collaborative — nobody supplies the item descriptions. The optimiser "
     "invents features that explain the ratings, and simultaneously the user weights that use them."),
   O("Only the user parameters; item features are given", False,
     "That is content-based filtering, where somebody has described each item in advance."),
   O("Only the item features; user parameters are given", False,
     "Neither side is given. Both are free parameters."),
   O("A single global set of weights shared by all users", False,
     "Each user has their own parameter vector — that is what makes the recommendations "
     "personalised.")],
  "c3/w2-03-collaborative-filtering.html", tag="what is learned"),

Q("c3w2-q02",
  "<p>Why apply mean normalization to the ratings matrix?</p>",
  [O("So a user with no ratings gets the average prediction rather than zero", True,
     "Without it, an empty parameter vector predicts 0 — the system decides a brand-new user hates "
     "everything, shows them nothing good, and they never rate anything. A two-line fix for the most "
     "expensive minute in the product."),
   O("To make the optimisation converge faster", False,
     "There is a small effect, and the cold-start behaviour is the reason it is prescribed."),
   O("To remove users who rate too few items", False,
     "Nothing is removed. Every row is centred."),
   O("To convert ratings into probabilities", False,
     "That is what a sigmoid does for binary labels, in a different lesson.")],
  "c3/w2-05-mean-normalization.html", tag="mean normalization",
  note="It turns &ldquo;I know nothing about you&rdquo; into &ldquo;I predict the average&rdquo;."),

Q("c3w2-q03",
  "<p>A brand-new film has just been added, with no ratings at all. Which approach can recommend it?</p>",
  [O("Content-based filtering", True,
     "It matches the film's <em>attributes</em> — genre, cast, year — against what a user has liked "
     "before. No ratings of that film are required."),
   O("Collaborative filtering", False,
     "It works entirely from the pattern of who rated what. With no ratings there is nothing to work "
     "from — this is the cold-start problem for items."),
   O("Neither can", False,
     "Content-based filtering exists largely for this case."),
   O("Both work equally well", False,
     "They have complementary blind spots, which is why real systems run both.")],
  "c3/w2-08-collaborative-vs-content.html", tag="cold start"),

Q("c3w2-q04",
  "<p>In the two-tower content-based architecture, why can it serve millions of items in "
  "milliseconds?</p>",
  [O("The item tower is precomputed offline; only the small user tower runs per request", True,
     "Items do not change, so their vectors are computed overnight and stored. At request time you "
     "run one small network and take dot products against a table."),
   O("Because the towers share weights", False,
     "They deliberately do not share weights — users and films are not the same kind of thing."),
   O("Because the network is very small", False,
     "The towers can be large. The asymmetry is what buys the latency, not the size."),
   O("Because the dot product is approximated", False,
     "Approximate nearest-neighbour search is used at the retrieval stage, which is a separate "
     "lesson. The dot product itself is exact.")],
  "c3/w2-09-deep-content-based.html", tag="two towers"),

Q("c3w2-q05",
  "<p>A large catalogue system uses retrieval then ranking. Which are true?</p>",
  [O("Retrieval is cheap and approximate; ranking is expensive and accurate", True,
     "Ten million down to about 500, then the full model on 500. The expensive judgement runs only on "
     "what survives."),
   O("An item never surfaced by retrieval can never be recommended", True,
     "No amount of ranking quality rescues it. This is why retrieval recall is measured separately, "
     "and it is usually the first thing to check when a good model underperforms."),
   O("The same two-stage shape appears in databases and graphics", True,
     "An index before a table scan; a bounding-box test before exact collision detection. Same "
     "economics every time."),
   O("Ranking runs on the entire catalogue", False,
     "That is exactly what the design avoids — it would be far too slow."),
   O("Retrieval must be exact for the system to work", False,
     "It is deliberately approximate. Slight inaccuracy is the price of speed, and it is worth it.")],
  "c3/w2-10-large-catalogues.html", tag="retrieval and ranking"),

Q("c3w2-q06",
  "<p>To find items similar to item <var>i</var> using collaborative filtering, what do you "
  "compute?</p>",
  [O("The distance between item <var>i</var>'s learned feature vector and every other item's", True,
     "Nearest-neighbour search in the learned space. No user is involved, which is why it works for a "
     "logged-out visitor on a page for a film they have never seen."),
   O("The correlation between the two items' user parameter vectors", False,
     "User parameters describe people, not items."),
   O("The number of users who rated both items", False,
     "A reasonable heuristic in its own right, and not what the learned features give you."),
   O("The difference in their average ratings", False,
     "Two films with the same average rating can be about entirely different things.")],
  "c3/w2-07-finding-related-items.html", tag="related items",
  note="A niche item with four ratings sits next to whatever those four people also rated — hence a minimum-ratings floor."),

Q("c3w2-q07",
  "<p>What does PCA do?</p>",
  [O("Finds the directions of maximum variance and projects the data onto the first few", True,
     "One good angle instead of a hundred pictures. It assumes variance carries the information, "
     "which is usually reasonable and occasionally catastrophic."),
   O("Selects the most predictive original features", False,
     "That is feature selection. PCA creates <em>new</em> features that are combinations of the "
     "originals."),
   O("Clusters the data into groups", False,
     "PCA reduces dimensions; it does not group points."),
   O("Removes outliers from the dataset", False,
     "Outliers strongly influence PCA, because they inflate variance in their direction.")],
  "c3/w2-13-reducing-features-pca.html", tag="what PCA does"),

Q("c3w2-q08",
  "<p>What must you do before running PCA, and why?</p>",
  [O("Scale the features, because PCA maximises variance and variance has units", True,
     "Leave salary in pounds beside age in years and the first component is &ldquo;salary&rdquo; every "
     "time, regardless of structure. Nothing warns you, and the output looks perfectly reasonable."),
   O("Remove correlated features, because PCA cannot handle them", False,
     "Correlated features are exactly what PCA exploits — that redundancy is what lets it compress."),
   O("Convert everything to categories", False,
     "PCA operates on continuous quantities. Categories need encoding, not conversion."),
   O("Nothing — PCA is scale-invariant", False,
     "It is emphatically not. This is the most common way PCA is misapplied.")],
  "c3/w2-14-pca-algorithm.html", tag="scaling before PCA"),

Q("c3w2-q09",
  "<p><code>explained_variance_ratio_</code> returns <code>[0.62, 0.19, 0.09, 0.06, 0.04]</code>. How "
  "many components do you need to keep 90% of the variance?</p>",
  [O("3", True,
     "Cumulative: 0.62, 0.81, 0.90. Three components reach exactly 90%."),
   O("2", False,
     "0.62 + 0.19 = 0.81, which is short of 90%."),
   O("4", False,
     "Four gives 96% — more than needed if your target is 90%."),
   O("1", False,
     "The first component alone carries 62%.")],
  "c3/w2-15-pca-in-code.html", tag="explained variance",
  note="Read the cumulative sum. That number tells you whether to trust everything downstream."),

Q("c3w2-q10",
  "<p>An engagement-optimised recommender gradually narrows what users see. Which statements are "
  "accurate?</p>",
  [O("The model's own output becomes its next training input", True,
     "Shown &rarr; clicked &rarr; trained on &rarr; shown more. Every other model in the "
     "specialization learns from data that existed before it; a recommender writes tomorrow's "
     "training data."),
   O("Optimising a measurable proxy can drift from the intended goal", True,
     "Engagement is measurable; whether time was well spent is not. Goodhart's law, with a fast and "
     "tireless optimiser."),
   O("Technical mitigations exist, such as optimising a longer-horizon outcome or capping exposure",
     True,
     "These are things you now know how to build, which is why the lesson sits in a technical course "
     "rather than a policy one."),
   O("It requires someone to have intended the outcome", False,
     "Every step can be a small, defensible response to what people actually clicked. No bad "
     "intention is needed."),
   O("The effect disappears with enough training data", False,
     "More data collected through the same loop reinforces it. Volume is not the fix.")],
  "c3/w2-11-ethics-recommenders.html", tag="feedback loops"),
])
