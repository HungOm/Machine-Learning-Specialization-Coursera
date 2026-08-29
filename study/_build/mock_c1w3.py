# -*- coding: utf-8 -*-
"""Mock quiz — C1 W3."""
from mockkit import Q, O, SET

SET = SET("C1", 3, "Classification",
"""Logistic regression, the decision boundary, logistic loss and regularization. Watch the questions
that ask what a number <i>means</i> — that is where the graded quiz concentrates.""", [

Q("c1w3-q01",
  "<p>Why is linear regression a poor choice for a binary classification problem?</p>",
  [O("Its output is unbounded, so it predicts values outside 0 and 1", True,
     "A probability must live in [0, 1] and a straight line does not. It also means one distant point "
     "can rotate the line and change predictions for cases whose data did not change at all."),
   O("It cannot be trained with gradient descent", False,
     "It trains perfectly well. The problem is that what it converges to does not answer the "
     "question."),
   O("It is too slow on large datasets", False,
     "Speed is not the issue — logistic regression costs essentially the same to train."),
   O("It requires the features to be categorical", False,
     "Neither model requires that. It is the <em>target</em> that is categorical here, and that is "
     "precisely the mismatch.")],
  "c1/w3-01-motivations.html", tag="why not linear regression"),

Q("c1w3-q02",
  "<p>The sigmoid <span class=\"v\">g(z) = 1/(1 + e<sup>&minus;z</sup>)</span>. What is "
  "<span class=\"v\">g(0)</span>, and what happens as z becomes very large and negative?</p>",
  [O("g(0) = 0.5, and g approaches 0", True,
     "At z = 0 the exponential is 1, giving 1/2. As z &rarr; &minus;&infin; the exponential explodes, "
     "so the fraction goes to zero. z = 0 is exactly the decision boundary."),
   O("g(0) = 0, and g approaches &minus;1", False,
     "The sigmoid never leaves (0, 1) — it cannot be negative. You may be thinking of tanh, which "
     "ranges &minus;1 to 1."),
   O("g(0) = 1, and g approaches 0", False,
     "g(0) = 1/(1+1) = 0.5, not 1. The function reaches towards 1 only for large positive z."),
   O("g(0) = 0.5, and g approaches &minus;&infin;", False,
     "The output is a probability and is bounded below by 0. It is z, the input, that runs to "
     "&minus;&infin;.")],
  "c1/w3-02-logistic-regression.html", tag="sigmoid"),

Q("c1w3-q03",
  "<p>A logistic model outputs 0.3 for a patient. With the standard 0.5 threshold, which are "
  "true?</p>",
  [O("The predicted class is 0", True,
     "0.3 is below the threshold, so the model predicts the negative class."),
   O("The model estimates a 30% chance the label is 1", True,
     "That is what the output <em>is</em> — an estimated probability, which is more information than "
     "the class alone."),
   O("Lowering the threshold to 0.25 would change this prediction to 1", True,
     "0.3 is above 0.25. The threshold is a choice made after training, and moving it trades "
     "precision against recall — the subject of C2 W3."),
   O("The model is 30% confident in its prediction", False,
     "It is 70% confident in its prediction of class 0. The output is the probability of class 1, not "
     "a confidence in whatever it decided."),
   O("The prediction is wrong", False,
     "Nothing here says what the true label is. A probability is not right or wrong on a single "
     "case.")],
  "c1/w3-03-decision-boundary.html", tag="reading the output",
  note="The output is P(y = 1). The class is what you get after applying a threshold you chose."),

Q("c1w3-q04",
  "<p>Why is squared error not used as the cost for logistic regression?</p>",
  [O("With a sigmoid inside it, the cost surface is non-convex and gradient descent can get stuck",
     True,
     "That is the technical reason. The logistic loss is chosen specifically to restore convexity, so "
     "there is a single minimum and descent from anywhere reaches it."),
   O("It would give negative costs", False,
     "Squared error is a square — it cannot be negative. That is not the problem."),
   O("It cannot be differentiated", False,
     "It is perfectly differentiable. It simply has a bad shape."),
   O("It would be too slow to compute", False,
     "Computation cost is essentially identical. The issue is the geometry of the surface, not the "
     "arithmetic.")],
  "c1/w3-04-cost-function-for-logistic-regression.html", tag="logistic loss",
  note="Convexity is the property that makes &ldquo;descend from anywhere&rdquo; a safe strategy."),

Q("c1w3-q05",
  "<p>For a single example with <span class=\"v\">y = 1</span>, the loss is "
  "<span class=\"v\">&minus;log(f)</span>. What happens as f approaches 0?</p>",
  [O("The loss grows without bound", True,
     "&minus;log(f) &rarr; &infin;. Being confidently and completely wrong is infinitely expensive, "
     "and that is the whole design — it is what stops the model claiming certainty it has not "
     "earned."),
   O("The loss approaches 0", False,
     "That happens when f approaches 1 — the model was confident and right. You have the direction "
     "reversed."),
   O("The loss approaches 1", False,
     "The logistic loss is not bounded above. There is no ceiling to be approached."),
   O("The loss becomes negative", False,
     "log of a number below 1 is negative, and the leading minus sign flips it positive. The loss is "
     "always &ge; 0.")],
  "c1/w3-05-logistic-loss.html", tag="the loss curve",
  note="The infinity is real, which is why implementations clip f away from exactly 0 and 1."),

Q("c1w3-q06",
  "<p>Which of these describes <b>overfitting</b>?</p>",
  [O("Low error on the training set, much higher error on new data", True,
     "The model has fitted the noise in the examples it saw. That gap between training and unseen "
     "performance is the definition."),
   O("High error on both training and new data", False,
     "That is underfitting, or high bias — the model is not capable enough to capture the pattern in "
     "the first place."),
   O("Low error on both training and new data", False,
     "That is the goal. Nothing is wrong."),
   O("The cost function fails to converge", False,
     "That is an optimisation problem — usually the learning rate — and is unrelated to how well the "
     "fitted model generalises.")],
  "c1/w3-08-the-problem-of-overfitting.html", tag="overfitting"),

Q("c1w3-q07",
  "<p>You increase &lambda; substantially. What happens?</p>",
  [O("Training error rises, and variance falls", True,
     "A larger penalty shrinks the weights, making the model less flexible. It fits the training data "
     "less well by design, and generalises better up to a point — after which it underfits."),
   O("Training error falls and variance falls", False,
     "You cannot have both. Regularisation buys reduced variance by <em>giving up</em> training "
     "fit — that is the trade."),
   O("Both training and cross-validation error fall indefinitely", False,
     "Cross-validation error is U-shaped in &lambda;: it falls, reaches a minimum, then rises as the "
     "model becomes too rigid."),
   O("Nothing, unless the features are scaled", False,
     "Scaling affects how <em>evenly</em> the penalty is applied across features, but &lambda; has a "
     "strong effect either way.")],
  "c1/w3-10-cost-function-with-regularization.html", tag="regularization",
  note="The U-shaped CV curve against &lambda; is the picture to memorise. It reappears everywhere."),

Q("c1w3-q08",
  "<p>In the regularized gradient, why is <span class=\"v\">b</span> normally left out of the "
  "penalty?</p>",
  [O("b sets the overall level, not the sensitivity to any feature", True,
     "Shrinking b towards zero just biases every prediction downwards for no benefit. The penalty "
     "exists to stop individual features having outsized influence, and b is not attached to a "
     "feature."),
   O("Because b is always zero anyway", False,
     "b is generally non-zero and is genuinely needed — it is what lets the line sit at the right "
     "height."),
   O("Because regularizing b would make the cost non-convex", False,
     "It would remain convex. It would simply be a worse model."),
   O("Because b is not learned by gradient descent", False,
     "It is learned, with its own partial derivative, exactly like every weight.")],
  "c1/w3-11-regularized-gradient-descent.html", tag="what gets regularized"),

Q("c1w3-q09",
  "<p>Comparing the gradient descent update for logistic regression with the one for linear "
  "regression, what is true?</p>",
  [O("The expressions look identical; only the definition of f differs", True,
     "Both are (f &minus; y)x<sub>j</sub>, averaged. In one, f is a dot product; in the other, a "
     "sigmoid of a dot product. This is not a coincidence — it holds for any generalised linear model "
     "with its canonical link."),
   O("Logistic regression needs an extra term for the sigmoid derivative", False,
     "The sigmoid's derivative cancels exactly against the log in the loss. That cancellation is why "
     "the final expression is so clean."),
   O("Logistic regression cannot use a fixed learning rate", False,
     "It can, and the same diagnostics for choosing &alpha; apply unchanged."),
   O("They differ because logistic regression has no bias term", False,
     "It has a bias term, updated the same way.")],
  "c1/w3-07-gradient-descent-logistic.html", tag="the update rule",
  note="One implementation of the update serves both models. Only f changes."),

Q("c1w3-q10",
  "<p>Your model fits the training data almost perfectly but does badly on new data, and collecting "
  "more data is not possible this quarter. Which are reasonable next steps?</p>",
  [O("Increase &lambda;", True,
     "Directly targets variance by shrinking the weights, and keeps every feature. It is the usual "
     "first move for exactly this situation."),
   O("Remove some features", True,
     "Fewer parameters means less capacity to memorise. It works, and it discards information "
     "permanently — which is why regularisation is generally preferred."),
   O("Reduce the polynomial degree", True,
     "Same idea as removing features: a lower-degree model is less flexible and less able to chase "
     "noise."),
   O("Decrease &lambda;", False,
     "That increases flexibility and makes overfitting worse. It is the fix for the opposite "
     "problem."),
   O("Train for more iterations", False,
     "The model already fits the training data almost perfectly. More iterations move it further in "
     "the wrong direction.")],
  "c1/w3-09-addressing-overfitting.html", tag="fixing overfitting",
  note="Symptom first, then remedy. High variance and high bias take opposite actions."),
])
