# -*- coding: utf-8 -*-
"""Mock quiz — C3 W1."""
from mockkit import Q, O, SET

SET = SET("C3", 1, "Unsupervised Learning",
"""K-means and anomaly detection. The split question and the &ldquo;which technique&rdquo; question
are the two the graded quiz always asks in some form.""", [

Q("c3w1-q01",
  "<p>What are the two steps k-means alternates between?</p>",
  [O("Assign each point to its nearest centroid; move each centroid to the mean of its points", True,
     "Two steps, repeated until nothing moves. Each one cannot increase the cost, which is why it "
     "terminates."),
   O("Assign points at random; then compute the cost", False,
     "Random assignment happens once at initialisation, not every round, and computing the cost is "
     "not one of the two update steps."),
   O("Compute the covariance; then take the top eigenvectors", False,
     "That is PCA, which appears in Week 2."),
   O("Split the largest cluster; then merge the two closest", False,
     "That describes hierarchical clustering, a different family entirely.")],
  "c3/w1-03-kmeans-algorithm.html", tag="the algorithm"),

Q("c3w1-q02",
  "<p>Why run k-means many times from different random initialisations?</p>",
  [O("It converges to a local optimum that depends on where the centroids started", True,
     "Two flags landing in the same corner give a genuinely worse clustering, and nothing in the "
     "algorithm can escape it. Run it 50&ndash;1000 times and keep the lowest cost."),
   O("Because the algorithm is stochastic at every step", False,
     "Once initialised, both steps are deterministic. Only the starting position is random."),
   O("To estimate the uncertainty in the cluster assignments", False,
     "That is a reasonable thing to want and is not why the restarts are prescribed here."),
   O("To choose the best value of k", False,
     "Restarts compare runs at a <em>fixed</em> k. The cost cannot be used to choose k because it "
     "falls automatically as k rises.")],
  "c3/w1-05-initializing-kmeans.html", tag="initialization",
  note="One run of k-means is a sample, not an answer."),

Q("c3w1-q03",
  "<p>Which are true of the k-means cost function J?</p>",
  [O("It is the average squared distance from each point to its own centroid", True,
     "Sometimes called inertia or distortion. It is the quantity both steps reduce."),
   O("It never increases from one iteration to the next", True,
     "Both steps can only reduce it, which proves the algorithm terminates — and makes a rising J a "
     "reliable assertion that you have a bug."),
   O("It cannot be used to choose k", True,
     "J falls automatically as k rises, reaching zero when every point is its own cluster. Choosing "
     "k needs the elbow, or a business reason."),
   O("It is convex, so there is only one minimum", False,
     "It is not convex in the assignments, which is exactly why local optima and restarts matter."),
   O("It is only defined once the algorithm has converged", False,
     "It can be computed at any iteration, which is what lets you plot it and check it is falling.")],
  "c3/w1-04-kmeans-cost.html", tag="the cost function"),

Q("c3w1-q04",
  "<p>Using the elbow method you plot J against k and get a smooth curve with no visible bend. What "
  "should you do?</p>",
  [O("Choose k by what the clusters are for", True,
     "Andrew is explicit that often no clear elbow exists. A t-shirt maker choosing between three "
     "sizes and five is weighing fit against inventory cost, and that decides it."),
   O("Pick the k with the lowest J", False,
     "That is always the largest k you tried, ending with one cluster per point."),
   O("Conclude the data cannot be clustered", False,
     "It clusters fine. The absence of an elbow says there is no single natural number of groups, not "
     "that grouping is impossible."),
   O("Increase the number of restarts until an elbow appears", False,
     "Restarts improve each run's quality; they do not create structure that is not there.")],
  "c3/w1-06-choosing-k.html", tag="choosing k"),

Q("c3w1-q05",
  "<p>For anomaly detection, how should you split 10,000 normal examples and 20 known anomalies?</p>",
  [O("All 10,000 normal in training; the 20 anomalies split between CV and test", True,
     "The model fits &mu; and &sigma; to describe <em>normal</em>. Contaminating training with "
     "anomalies widens the distribution until the anomalies look normal, so every one is spent on "
     "evaluation instead."),
   O("Split everything randomly 60/20/20", False,
     "That puts anomalies in the training set, which is precisely what you must not do."),
   O("All 20 anomalies in training so the model learns what they look like", False,
     "That would be supervised learning. This method never learns what an anomaly looks like — it "
     "learns what normal looks like and flags everything else."),
   O("Discard the anomalies; they are not needed", False,
     "They are the only way to choose &epsilon; and the only way to measure whether the system "
     "works.")],
  "c3/w1-10-developing-anomaly-detection.html", tag="the unusual split",
  note="Train on normal only. Spend every anomaly on evaluation."),

Q("c3w1-q06",
  "<p>You have 6,000 examples of fraud and expect future fraud to look like past fraud. Anomaly "
  "detection or supervised learning?</p>",
  [O("Supervised learning — many positives that resemble each other", True,
     "The deciding question is not how many positives you have but whether future ones will resemble "
     "past ones. Here they will, so a classifier can learn the pattern."),
   O("Anomaly detection — fraud is rare", False,
     "Rarity alone does not decide it. With 6,000 recognisable examples a classifier will do better "
     "than density estimation."),
   O("Anomaly detection — it needs no labels", False,
     "You have labels. Throwing away 6,000 of them to avoid using them is not an advantage."),
   O("Neither is appropriate for fraud", False,
     "Both are used for fraud in practice, often together — a classifier for the known, density "
     "estimation for the novel.")],
  "c3/w1-11-anomaly-vs-supervised.html", tag="which technique",
  note="Will future positives resemble past ones? Yes &rarr; classifier. No &rarr; anomaly detection."),

Q("c3w1-q07",
  "<p>A feature in your anomaly detector is heavily right-skewed. What should you do?</p>",
  [O("Transform it, e.g. log(x + 1), to make it roughly Gaussian", True,
     "The model assumes a Gaussian per feature. Making that assumption approximately true is usually "
     "the single highest-value step in the pipeline."),
   O("Remove it", False,
     "A skewed feature may be highly informative. Transform first, remove only if it earns nothing."),
   O("Nothing — the Gaussian model handles any distribution", False,
     "It does not. Fitting a Gaussian to a heavy-tailed feature mislabels ordinary large values as "
     "anomalies."),
   O("Scale it to the range 0&ndash;1", False,
     "Scaling shifts and stretches; it does not change the shape. A skewed feature is still skewed "
     "afterwards.")],
  "c3/w1-12-choosing-features.html", tag="feature transforms"),

Q("c3w1-q08",
  "<p>Why is accuracy the wrong metric for evaluating an anomaly detector?</p>",
  [O("With 0.2% anomalies, predicting &ldquo;normal&rdquo; always scores 99.8%", True,
     "The same skewed-data trap as C2 W3. Precision, recall and F1 on the anomaly class are the "
     "metrics that mean something."),
   O("Because anomaly detection is unsupervised and cannot be measured", False,
     "It can be measured — that is what the labelled anomalies in the CV and test sets are for."),
   O("Because &epsilon; changes the accuracy", False,
     "It does change it, and that is not the reason accuracy is misleading."),
   O("Because accuracy requires balanced classes to compute", False,
     "It computes fine. It is just uninformative here.")],
  "c3/w1-10-developing-anomaly-detection.html", tag="metrics"),

Q("c3w1-q09",
  "<p>A server has normal CPU and normal traffic individually, but high CPU <em>with</em> low traffic. "
  "Why might the independent-Gaussian model miss it?</p>",
  [O("It models each feature separately, so it cannot see the combination", True,
     "Each feature is individually unremarkable, and the product of two ordinary probabilities is "
     "ordinary. Catching this needs either the multivariate Gaussian or an engineered ratio "
     "feature."),
   O("Because CPU is not normally distributed", False,
     "Even with perfectly Gaussian features, the independence assumption is what loses the joint "
     "structure."),
   O("Because &epsilon; is too small", False,
     "Lowering &epsilon; flags more things overall, including many genuinely normal ones. It does not "
     "recover the specific joint signal."),
   O("Because the training set was too small", False,
     "More data does not create a dependency the model has no way to represent.")],
  "c3/w1-09-anomaly-detection-algorithm.html", tag="the independence assumption",
  note="The fix is a ratio feature — CPU divided by traffic — or a multivariate Gaussian."),

Q("c3w1-q10",
  "<p>For a Gaussian with &mu; = 50 and &sigma; = 5, roughly what fraction of values fall between 40 "
  "and 60?</p>",
  [O("About 95%", True,
     "40 and 60 are two standard deviations either side of the mean. The 68 / 95 / 99.7 rule is worth "
     "memorising — it converts a threshold into an expected false-alarm rate."),
   O("About 68%", False,
     "That is one standard deviation: 45 to 55."),
   O("About 99.7%", False,
     "That is three standard deviations: 35 to 65."),
   O("About 50%", False,
     "50% is the fraction below the mean, which is a different question.")],
  "c3/w1-08-gaussian-distribution.html", tag="the normal distribution"),
])
