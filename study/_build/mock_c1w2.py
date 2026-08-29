# -*- coding: utf-8 -*-
"""Mock quiz — C1 W2."""
from mockkit import Q, O, SET

SET = SET("C1", 2, "Regression with Multiple Variables",
"""Many features, vectorisation, feature scaling and polynomial fits. The scaling questions are the
ones people lose marks on, because the reason it matters is geometric rather than numerical.""", [

Q("c1w2-q01",
  "<p>You have 4 features and 100 training examples. What is the shape of "
  "<span class=\"v\">X</span>, and what does <span class=\"v\">x<sup>(3)</sup></span> refer to?</p>",
  [O("X is 100&times;4; x<sup>(3)</sup> is the third training example, a vector of 4 numbers", True,
     "Rows are examples, columns are features. The superscript in parentheses indexes the row, so "
     "x<sup>(3)</sup> is one whole house, not one measurement."),
   O("X is 4&times;100; x<sup>(3)</sup> is the third feature across all examples", False,
     "This transposes the convention. It is a legitimate way to store data and it is not the one this "
     "course uses, and mixing the two is the most common source of shape bugs."),
   O("X is 100&times;4; x<sup>(3)</sup> is the third feature of the first example", False,
     "That would be x<sub>3</sub><sup>(1)</sup>. Subscript is the column, superscript-in-parentheses "
     "is the row — both are needed to name a single cell."),
   O("X is 100&times;5, because the bias needs a column of ones", False,
     "That trick belongs to the normal-equation formulation. In this course b is carried as a "
     "separate parameter, so no ones column is added.")],
  "c1/w2-01-multiple-features.html", tag="notation and shapes",
  note="Superscript in parentheses is the row; subscript is the column."),

Q("c1w2-q02",
  "<p>Why is <code>np.dot(w, x)</code> so much faster than a Python <code>for</code> loop computing "
  "the same sum?</p>",
  [O("It uses hardware instructions that handle several numbers at once", True,
     "SIMD — one instruction, multiple data. The loop is slow because every pass goes through the "
     "Python interpreter and never reaches those instructions, not because looping is inherently "
     "slow."),
   O("It uses a mathematically better algorithm", False,
     "The arithmetic is identical — the same multiplications and the same additions, in the same "
     "quantity. Only how they reach the processor differs."),
   O("It skips terms that are close to zero", False,
     "Nothing is skipped. The result is exactly the same number the loop would produce."),
   O("It approximates the answer to save time", False,
     "There is no approximation. You can check it: both give the same value to full precision.")],
  "c1/w2-03-why-vectorization-is-fast.html", tag="vectorization",
  note="This is also why GPUs help — they are built for exactly this shape of work."),

Q("c1w2-q03",
  "<p>Feature <span class=\"v\">x<sub>1</sub></span> ranges from 0&ndash;2000 and "
  "<span class=\"v\">x<sub>2</sub></span> from 1&ndash;5. Which are true?</p>",
  [O("The contours of J will be long thin ellipses", True,
     "Unequal feature ranges stretch the cost surface. A small change in the weight on the "
     "large-range feature moves J far more than the same change on the other."),
   O("Gradient descent will take many more iterations without scaling", True,
     "It bounces across the narrow valley instead of running down it, so it needs a small &alpha; "
     "and many steps to make progress along the long axis."),
   O("Scaling makes the contours rounder, so descent goes more directly to the minimum", True,
     "That is exactly the point of scaling — it is a geometric fix, not a numerical tidy-up."),
   O("Without scaling, gradient descent will converge to the wrong answer", False,
     "It converges to the same minimum, just far more slowly. Scaling changes the speed, not the "
     "destination."),
   O("Scaling changes which features are important", False,
     "It rescales the parameters correspondingly. A feature that mattered still matters — the weight "
     "attached to it is simply expressed in different units.")],
  "c1/w2-05-feature-scaling.html", tag="feature scaling",
  note="Scaling is about the shape of the contours, which is about how many steps you need."),

Q("c1w2-q04",
  "<p>Using mean normalization on a feature with mean 1000 and range 400&ndash;1600, what is the "
  "scaled value of <span class=\"v\">x = 1300</span>?</p>",
  [O("0.25", True,
     "(1300 &minus; 1000) / (1600 &minus; 400) = 300 / 1200 = 0.25. Subtract the mean, divide by the "
     "range."),
   O("0.8125", False,
     "This is 1300/1600 — dividing by the maximum without subtracting the mean. That is max scaling, "
     "which centres nothing."),
   O("300", False,
     "This is the numerator only. The division by the range is what puts the feature on a comparable "
     "scale to the others."),
   O("1.3", False,
     "This divides by the mean rather than subtracting it, which neither centres the feature nor "
     "controls its spread.")],
  "c1/w2-05-feature-scaling.html", tag="scaling arithmetic"),

Q("c1w2-q05",
  "<p>You have <span class=\"v\">frontage</span> and <span class=\"v\">depth</span> of a plot, and "
  "create <span class=\"v\">area = frontage &times; depth</span>. Why can this help so much?</p>",
  [O("A linear model cannot represent a product of two features, however long you train it", True,
     "That is the structural point. The new column changes what is <em>representable</em>, not merely "
     "what has been learned so far — and land sells by area, so the product is the meaningful "
     "quantity."),
   O("It reduces the number of features the model must handle", False,
     "It adds one. You may then choose to drop the originals, but that is a separate decision."),
   O("It makes gradient descent converge faster", False,
     "If anything it can slow convergence, since the product has a much larger range and now needs "
     "scaling."),
   O("It guarantees a lower cost on unseen data", False,
     "It guarantees nothing. A badly chosen engineered feature adds variance and can make unseen "
     "performance worse.")],
  "c1/w2-08-feature-engineering.html", tag="feature engineering",
  note="Feature engineering adds capability the optimiser could never have found on its own."),

Q("c1w2-q06",
  "<p>You fit <span class=\"v\">f = w<sub>1</sub>x + w<sub>2</sub>x&sup2; + w<sub>3</sub>x&sup3; + "
  "b</span>. Is this still linear regression?</p>",
  [O("Yes — it is linear in the parameters, which is what the name refers to", True,
     "The model is a weighted sum of known quantities. That the quantities happen to be powers of one "
     "another is irrelevant to the algorithm, which is why the same cost and the same gradient descent "
     "still apply unchanged."),
   O("No, because the fitted curve is not a straight line", False,
     "The shape of the curve in x is not what &ldquo;linear&rdquo; means here. Linear refers to how "
     "the parameters enter the model."),
   O("No — it needs a different cost function", False,
     "Squared error works exactly as before. Nothing about the training changes."),
   O("Only if you also scale the features", False,
     "Scaling is strongly advisable — x&sup3; can be a billion when x is a thousand — but it is a "
     "practical necessity, not part of the definition.")],
  "c1/w2-09-polynomial-regression.html", tag="polynomial regression",
  note="&ldquo;Linear&rdquo; describes the parameters. The curve is in the features you supply."),

Q("c1w2-q07",
  "<p>Your learning curve falls very slowly and is still clearly falling after 10,000 iterations. "
  "What should you try first?</p>",
  [O("Increase &alpha;", True,
     "Still-falling means each step is too small. Go up by roughly a factor of three — 0.001 to 0.003 "
     "to 0.01 — and watch the shape."),
   O("Decrease &alpha;", False,
     "That makes it slower still. You decrease &alpha; when the cost <em>rises</em> or oscillates."),
   O("Add more features", False,
     "This is an optimisation-speed symptom, not a model-capacity one. The cost is falling; it is "
     "simply not falling fast enough."),
   O("Stop — it has converged", False,
     "Converged means flat. A curve still descending at the right-hand edge has not finished.")],
  "c1/w2-07-choosing-the-learning-rate.html", tag="learning rate"),

Q("c1w2-q08",
  "<p>You scaled your features before training. At prediction time, for a new house, what must you "
  "do?</p>",
  [O("Apply the same scaling, using the mean and range from the training set", True,
     "The parameters were learned in scaled units, so the input must arrive in those same units — and "
     "critically, using the <em>training</em> statistics, not statistics recomputed from the new "
     "data."),
   O("Nothing — scaling is only needed during training", False,
     "This is the classic deployment bug. Feed raw values into a model trained on scaled ones and the "
     "predictions are silently, badly wrong."),
   O("Compute the mean and range of the new data and scale by those", False,
     "A single new house has no meaningful range, and even with a batch this shifts the scaling "
     "between training and serving. Store the training statistics and reuse them."),
   O("Scale only the features that were far from zero", False,
     "The transformation has to match what was applied in training, feature by feature, with no "
     "exceptions.")],
  "c1/w2-05-feature-scaling.html", tag="scaling at prediction time",
  note="Fit the scaler on train; apply it everywhere. The same rule returns for PCA in C3."),

Q("c1w2-q09",
  "<p>For multiple linear regression with n features, what is the shape of the gradient "
  "<span class=\"v\">&part;J/&part;w</span>?</p>",
  [O("A vector of length n — one partial derivative per feature", True,
     "Each weight has its own partial derivative, of exactly the form you derived for one feature. "
     "That vector is what the update subtracts, all at once."),
   O("A single number", False,
     "That is the case with one feature. With n weights there are n independent directions to "
     "consider."),
   O("An n&times;n matrix", False,
     "That would be the matrix of second derivatives — the Hessian — which Newton's method uses. "
     "Gradient descent needs only first derivatives."),
   O("A vector of length m, one per training example", False,
     "The per-example errors have length m, but they are summed as part of computing each partial "
     "derivative. The gradient's length matches the number of parameters.")],
  "c1/w2-04-gradient-descent-multiple-features.html", tag="vectorized gradient"),

Q("c1w2-q10",
  "<p>Which statement about the normal equation is correct?</p>",
  [O("It solves for w and b in one step, but only for linear regression and gets slow for large n",
     True,
     "It is a closed-form solution requiring a matrix inverse, which costs roughly O(n&sup3;). Fine at "
     "100 features, impractical at 10,000, and it does not generalise to logistic regression or "
     "neural networks."),
   O("It is always preferable to gradient descent", False,
     "Only for small linear-regression problems. It does not exist for the models in C2 and C3, which "
     "is why gradient descent is the method the whole specialization is built on."),
   O("It requires feature scaling to work", False,
     "It does not — that is one of its genuine advantages. Scaling matters for iterative methods."),
   O("It works for any model with a squared-error cost", False,
     "It needs the model to be linear in the parameters. A squared error around a neural network has "
     "no closed-form solution.")],
  "c1/w2-06-checking-convergence.html", tag="normal equation"),
])
