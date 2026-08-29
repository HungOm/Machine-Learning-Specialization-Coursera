# -*- coding: utf-8 -*-
"""Mock quiz — C1 W1. Written from the lessons, not copied from Coursera."""
from mockkit import Q, O, SET

SET = SET("C1", 1, "Introduction to Machine Learning",
"""Regression, the cost function and gradient descent. If you can do these ten closed-book you are
ready for the graded quiz; if you cannot, the misses will tell you which lesson to re-read.""", [

Q("c1w1-q01",
  "<p>A hospital wants to predict, from a patient's records, <b>how many days</b> they will stay. "
  "Which best describes this problem?</p>",
  [O("Supervised learning, regression", True,
     "Past patients come with their actual length of stay — that is the label — and the answer is a "
     "number on a continuous scale. Both halves of the definition are satisfied."),
   O("Supervised learning, classification", False,
     "Classification predicts one of a small set of categories. &ldquo;Number of days&rdquo; is a "
     "quantity, and treating 3 days and 4 days as unrelated categories throws away the ordering."),
   O("Unsupervised learning, clustering", False,
     "Clustering has no labels at all. Here the historical records <em>do</em> carry the right "
     "answer, so using an unsupervised method would discard the most valuable column you have."),
   O("Unsupervised learning, anomaly detection", False,
     "Anomaly detection asks &ldquo;is this unusual?&rdquo;, not &ldquo;how many days?&rdquo; It is "
     "the right tool when you have almost no labelled examples of what you are looking for.")],
  "c1/w1-02-supervised-learning.html", tag="supervised vs unsupervised",
  note="Two questions, in order: are there labels, and is the answer a number or a category?"),

Q("c1w1-q02",
  "<p>For <span class=\"v\">f(x) = 0.3x + 12</span>, what is the predicted value at "
  "<span class=\"v\">x = 40</span>?</p>",
  [O("24", True, "0.3 &times; 40 = 12, and 12 + 12 = 24. Multiply before you add."),
   O("12.3", False,
     "This adds w and b and ignores x entirely. Check that x actually appears in your arithmetic."),
   O("52", False,
     "This is 40 + 12 — it uses x but drops the weight. w is a rate: it says how much f changes per "
     "unit of x, so it must multiply x rather than be added to it."),
   O("36", False,
     "This is 0.3 &times; (40 + 12) & mdash; the bias added inside rather than outside. b shifts the "
     "whole line up, so it is added last.".replace("& mdash;", "&mdash;"))],
  "c1/w1-04-linear-regression-model.html", tag="the model"),

Q("c1w1-q03",
  "<p>Which of the following are true of the squared error cost "
  "<span class=\"v\">J(w, b)</span> for linear regression?</p>",
  [O("It is always greater than or equal to zero", True,
     "Every term is a square, and a sum of squares cannot be negative. J = 0 exactly when the line "
     "passes through every point."),
   O("Its minimum is the best line under this definition of &ldquo;best&rdquo;", True,
     "That is what the cost function is for: it converts &ldquo;which line?&rdquo; into &ldquo;which "
     "(w, b) makes this number smallest?&rdquo;"),
   O("For linear regression it has exactly one minimum", True,
     "Squared error in a linear model is convex — a bowl. There are no local minima to get trapped "
     "in, which is why gradient descent is safe here and not in a neural network."),
   O("It measures the error of a single training example", False,
     "That is one term inside the sum. J averages over <em>all</em> m examples — a cost for the whole "
     "dataset, not for one point."),
   O("Making J smaller always makes predictions on new data better", False,
     "This is exactly the overfitting trap you meet in Week 3. J is measured on the training set, and "
     "driving it to zero can make new predictions worse.")],
  "c1/w1-05-cost-function-formula.html", tag="cost function",
  note="J scores a whole line with one number. The division by 2m is convention, not meaning."),

Q("c1w1-q04",
  "<p>Gradient descent is at a point where the derivative "
  "<span class=\"v\">&part;J/&part;w</span> is <b>negative</b>. What happens to w on the next step?</p>",
  [O("w increases", True,
     "The update subtracts &alpha; times the derivative. Subtracting a negative number increases w — "
     "and a negative slope means J falls as w rises, so increasing w is downhill. Correct."),
   O("w decreases", False,
     "This is the trap. The rule is subtract &alpha;&part;J/&part;w, and the derivative is negative, "
     "so the subtraction adds. Substitute a number: w &minus; 0.1 &times; (&minus;4) = w + 0.4."),
   O("w does not change", False,
     "w is unchanged only when the derivative is exactly zero, which is the definition of being at a "
     "minimum (or a flat point)."),
   O("It depends on the sign of b", False,
     "The two parameters are updated independently, each from its own partial derivative. b's value "
     "does not enter w's update rule.")],
  "c1/w1-10-gradient-descent-intuition.html", tag="gradient descent",
  note="One rule handles both directions because the sign is carried by the derivative."),

Q("c1w1-q05",
  "<p>Your cost <span class=\"v\">J</span> <b>increases</b> on almost every iteration of gradient "
  "descent. What is the most likely cause?</p>",
  [O("The learning rate &alpha; is too large", True,
     "The classic symptom. Each step overshoots the minimum and lands somewhere the slope is even "
     "steeper, so the next step is worse again. Try &alpha; ten times smaller."),
   O("The learning rate &alpha; is too small", False,
     "A too-small &alpha; makes J fall very <em>slowly</em>. It still falls — it never rises."),
   O("You need more training data", False,
     "More data changes what the minimum is, not whether the algorithm can walk downhill. A rising "
     "cost is an optimisation failure, not a data problem."),
   O("The cost function is not convex", False,
     "For linear regression with squared error it always is. A non-convex surface would cause you to "
     "land in a poor local minimum, not to climb.")],
  "c1/w1-11-learning-rate.html", tag="learning rate",
  note="A rising cost is almost always &alpha;. Set it absurdly small to confirm the gradient itself is right."),

Q("c1w1-q06",
  "<p>On a contour plot of <span class=\"v\">J(w, b)</span>, what do the points on a single contour "
  "line have in common?</p>",
  [O("They all give exactly the same cost", True,
     "A contour is a level set — every (w, b) on that ring produces the identical value of J, in the "
     "same way every point on one elevation line of a map is at the same height."),
   O("They all give the same prediction for a given x", False,
     "Different (w, b) pairs on the same contour are different lines, and they generally predict "
     "different values. They merely happen to be equally wrong overall."),
   O("They are all the same distance from the minimum", False,
     "Only if the contours were perfect circles. Elongated ellipses — which is the usual case with "
     "unscaled features — have points on one ring at very different distances from the centre."),
   O("They all have zero gradient", False,
     "The gradient is zero only at the centre. Along a contour the gradient is non-zero and points "
     "perpendicular to the line.")],
  "c1/w1-07-visualizing-the-cost-function.html", tag="contour plots"),

Q("c1w1-q07",
  "<p>Which of these is an <b>unsupervised</b> learning problem?</p>",
  [O("Grouping news articles by topic, with no topics defined in advance", True,
     "No labels exist and none are supplied — the groups are discovered from the data. That is "
     "clustering, and it is unsupervised."),
   O("Predicting tomorrow's temperature from the last 30 days", False,
     "Every historical day comes with the temperature that actually followed. Those are labels, so "
     "this is supervised regression."),
   O("Deciding whether an email is spam, using 10,000 labelled emails", False,
     "The word &ldquo;labelled&rdquo; settles it. This is supervised classification."),
   O("Predicting house price from floor area and age", False,
     "The historical sale prices are the labels. Supervised regression.")],
  "c1/w1-03-unsupervised-learning.html", tag="unsupervised learning",
  note="One test: does the training data contain the answer you want to predict?"),

Q("c1w1-q08",
  "<p>Why must <span class=\"v\">w</span> and <span class=\"v\">b</span> be updated "
  "<b>simultaneously</b>?</p>",
  [O("Both gradients must be computed from the same, old parameter values", True,
     "The gradient describes the slope of J at the point you are currently standing on. Update w "
     "first, and b's gradient is then computed on a surface at a different point — you are descending "
     "a hill you have already partly moved down."),
   O("Otherwise the algorithm will crash", False,
     "It will not crash. That is what makes this bug dangerous: it runs, it usually still converges, "
     "and it converges to something slightly wrong."),
   O("Because w and b must always be equal", False,
     "They are independent parameters with entirely different meanings — a slope and an intercept."),
   O("So that the learning rate stays constant", False,
     "&alpha; is a fixed number you chose. Nothing about the update order changes it.")],
  "c1/w1-09-implementing-gradient-descent.html", tag="simultaneous update",
  note="A bug that still converges — to the wrong place — is worse than one that crashes."),

Q("c1w1-q09",
  "<p>You plot <span class=\"v\">J</span> against iteration number and the curve falls steeply, then "
  "flattens completely for the last 200 iterations. What does this tell you?</p>",
  [O("Gradient descent has converged", True,
     "A flat tail means the parameters have stopped changing meaningfully. Running longer will not "
     "improve the fit — whether the fit is <em>good</em> is a separate question this plot cannot "
     "answer."),
   O("The learning rate is too small", False,
     "A too-small &alpha; gives a curve that is <em>still falling</em> at the right-hand edge. This "
     "one has flattened, which is the opposite diagnosis."),
   O("The model has overfitted", False,
     "This plot only shows training cost against iterations. Overfitting is a gap between training "
     "and unseen data, and nothing here measures unseen data."),
   O("You should increase the number of features", False,
     "Convergence says the optimiser finished. It says nothing about whether the model is powerful "
     "enough — for that you would compare J to a baseline.")],
  "c1/w1-13-running-gradient-descent.html", tag="convergence"),

Q("c1w1-q10",
  "<p>In <span class=\"v\">f(x) = wx + b</span> for house prices in thousands, with x in square "
  "feet, what does <span class=\"v\">w</span> mean?</p>",
  [O("The change in price for one extra square foot", True,
     "w is a rate: the change in output per unit change in input. If w = 0.2 and price is in "
     "thousands, each extra square foot adds &pound;200."),
   O("The price of a house of average size", False,
     "That would be the model's output at the mean x, which is w&#772;x + b — it involves both "
     "parameters, not w alone."),
   O("The price of a zero-square-foot house", False,
     "That is b, the intercept — the value of f when x = 0. It is often physically meaningless and "
     "still necessary, because it sets the line's height."),
   O("How accurate the model is", False,
     "Accuracy is measured by the cost J, or by error on unseen data. A large w means a steep line, "
     "not a good one.")],
  "c1/w1-04-linear-regression-model.html", tag="interpreting parameters",
  note="w is a rate, b is an offset. Every model in the specialization has this pair."),
])
