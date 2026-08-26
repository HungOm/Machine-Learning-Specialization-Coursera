# -*- coding: utf-8 -*-
"""Hand-written orientation for each notebook in the repo.

Structure (outline, functions, exercise markers) is read from the .ipynb by
labkit. This file supplies only the judgement: what the lab is really for,
which lessons it leans on, and — for graded assignments — what each exercise
is asking and how it goes wrong.

Solution code is deliberately never reproduced for graded exercises.
"""

E = lambda n, fn, asks, maths, shape, trap: dict(
    n=n, fn=fn, asks=asks, maths=maths, shape=shape, trap=trap)

LABS = {

# ============================================================ C1 W1
"C1_W1_Lab01_Python_Jupyter_Soln.ipynb": dict(
    course="C1", week=1, kind="optional", mins=15,
    blurb="Fifteen minutes on how a notebook works — markdown cells versus code cells, "
          "and Shift+Enter. Skip it only if you have used Jupyter before.",
    lessons=[("f0/w2-01-jupyter.html", "Jupyter and notebooks")],
    watch="Cells share one memory. Running them out of order is the single most "
          "common cause of a lab that “was working a minute ago”."),

"C1_W1_Lab03_Model_Representation_Soln.ipynb": dict(
    course="C1", week=1, kind="optional", mins=25,
    blurb="Two houses, one straight line. You set w and b by hand and watch the line "
          "move, which is the cheapest possible way to make f(x) = wx + b concrete.",
    lessons=[("c1/w1-04-linear-regression-model.html", "The linear regression model"),
             ("f0/w1-04-slope.html", "Slope")],
    watch="The notation table near the top is worth copying out. x<sup>(i)</sup> is the i-th "
          "example, not x to the power i, and that confusion breaks everything after it."),

"C1_W1_Lab04_Cost_function_Soln.ipynb": dict(
    course="C1", week=1, kind="optional", mins=30,
    blurb="An interactive plot of J(w) as you drag w. This is the lab that makes the "
          "word “bowl” mean something.",
    lessons=[("c1/w1-05-cost-function-formula.html", "The cost function formula"),
             ("c1/w1-06-cost-function-intuition.html", "Cost function intuition")],
    watch="Watch the cost fall to exactly zero when the line passes through every "
          "point, and note that this is only possible because the data is synthetic."),

"C1_W1_Lab05_Gradient_Descent_Soln.ipynb": dict(
    course="C1", week=1, kind="optional", mins=40,
    blurb="The full loop, plotted: cost against iteration, and the path across the "
          "contour plot. Try breaking it by raising alpha — the divergence is the lesson.",
    lessons=[("c1/w1-09-implementing-gradient-descent.html", "Implementing gradient descent"),
             ("c1/w1-11-learning-rate.html", "The learning rate"),
             ("c1/w1-13-running-gradient-descent.html", "Running gradient descent")],
    watch="The steps get shorter as it approaches the minimum without alpha changing. "
          "That is the gradient shrinking on its own, and it is why a fixed alpha works."),

# ============================================================ C1 W2
"C1_W2_Lab01_Python_Numpy_Vectorization_Soln.ipynb": dict(
    course="C1", week=2, kind="optional", mins=45,
    blurb="The most useful optional lab in Course 1. It times a loop against np.dot "
          "on a million elements and the gap is not subtle.",
    lessons=[("c1/w2-02-vectorization.html", "Vectorization"),
             ("c1/w2-03-why-vectorization-is-fast.html", "Why vectorization is fast"),
             ("f0/w2-09-dot-in-code.html", "The dot product in code")],
    watch="Note the timing difference and then note that the arithmetic is identical. "
          "Vectorization does not compute less; it computes in a better place."),

"C1_W2_Lab02_Multiple_Variable_Soln.ipynb": dict(
    course="C1", week=2, kind="optional", mins=35,
    blurb="Linear regression with four features instead of one. Almost nothing in the "
          "code changes, which is the point.",
    lessons=[("c1/w2-01-multiple-features.html", "Multiple features"),
             ("c1/w2-04-gradient-descent-multiple-features.html", "Gradient descent with multiple features")],
    watch="Track the shapes: X is (m, n), w is (n,), and X @ w is (m,). Write those "
          "three down before reading the code."),

"C1_W2_Lab03_Feature_Scaling_and_Learning_Rate_Soln.ipynb": dict(
    course="C1", week=2, kind="optional", mins=45,
    blurb="Runs gradient descent at several learning rates on unscaled data — watch it "
          "diverge — then scales the features and watches the same alpha work.",
    lessons=[("c1/w2-05-feature-scaling.html", "Feature scaling"),
             ("c1/w2-07-choosing-the-learning-rate.html", "Choosing the learning rate"),
             ("f0/w1-17-mean-variance.html", "Mean and variance")],
    watch="The contour plots before and after scaling. A long thin valley becomes a "
          "round bowl, and the zig-zag path becomes a straight one."),

"C1_W2_Lab04_FeatEng_PolyReg_Soln.ipynb": dict(
    course="C1", week=2, kind="optional", mins=30,
    blurb="Fits a curve with a straight-line model by inventing x², x³ features. Shows "
          "that “linear regression” means linear in the parameters, not in x.",
    lessons=[("c1/w2-08-feature-engineering.html", "Feature engineering"),
             ("c1/w2-09-polynomial-regression.html", "Polynomial regression")],
    watch="Look at the feature ranges once x³ exists. Polynomial features make scaling "
          "compulsory, not optional."),

"C1_W2_Lab05_Sklearn_GD_Soln.ipynb": dict(
    course="C1", week=2, kind="optional", mins=15,
    blurb="The same problem in four lines of scikit-learn. Worth doing straight after "
          "writing it yourself, so you can see what the library is hiding.",
    lessons=[("c1/w2-04-gradient-descent-multiple-features.html", "Gradient descent with multiple features")],
    watch="SGDRegressor still needs scaled features. The library did not remove that "
          "requirement, it just stopped telling you about it."),

"C1_W2_Lab06_Sklearn_Normal_Soln.ipynb": dict(
    course="C1", week=2, kind="optional", mins=15,
    blurb="LinearRegression solves for w and b in closed form — no alpha, no iterations, "
          "no scaling needed. Then ask why the course still teaches gradient descent.",
    lessons=[("c1/w2-04-gradient-descent-multiple-features.html", "Gradient descent with multiple features")],
    watch="The answer to “why bother with gradient descent”: this method needs a matrix "
          "inverse, and it exists only for linear regression."),

"C1_W2_Linear_Regression.ipynb": dict(
    course="C1", week=2, kind="graded", mins=120,
    blurb="The first graded assignment: predict restaurant profit from city population. "
          "Two functions, and they are the two you will rewrite in every later course.",
    lessons=[("c1/w1-05-cost-function-formula.html", "The cost function formula"),
             ("c1/w1-12-gradient-descent-for-linear-regression.html", "Gradient descent for linear regression"),
             ("f0/w1-07-sigma-notation.html", "Sigma notation")],
    watch="Single-feature, so x is (m,) not (m, n). The shapes are simpler here than "
          "anywhere later — enjoy it.",
    exercises=[
      E(1, "compute_cost(x, y, w, b)",
        "Return J(w,b) — the average squared error, halved.",
        "J = (1/2m) Σ (f(x<sup>(i)</sup>) − y<sup>(i)</sup>)²",
        "x is (m,), returns a single float",
        "Dividing by m instead of 2m. The grader checks an exact value, so the ½ matters."),
      E(2, "compute_gradient(x, y, w, b)",
        "Return dj_dw and dj_db.",
        "dj_dw = (1/m) Σ (f−y)·x<sup>(i)</sup> &nbsp;·&nbsp; dj_db = (1/m) Σ (f−y)",
        "both are floats here, because there is only one feature",
        "Forgetting the extra x<sup>(i)</sup> in dj_dw. The two formulas differ by exactly that."),
    ]),

# ============================================================ C1 W3
"C1_W3_Lab01_Classification_Soln.ipynb": dict(
    course="C1", week=3, kind="optional", mins=15,
    blurb="Fits a straight line to 0/1 labels, then adds one far-away point and watches "
          "the decision boundary move. Two minutes that justify the whole sigmoid.",
    lessons=[("c1/w3-01-motivations.html", "Motivations")],
    watch="The single added point does not change where the classes actually separate, "
          "yet it moves the linear boundary. That is the failure the sigmoid fixes."),

"C1_W3_Lab02_Sigmoid_function_Soln.ipynb": dict(
    course="C1", week=3, kind="optional", mins=20,
    blurb="Plots g(z) and confirms g(0) = 0.5. Short, and worth it for that one fact.",
    lessons=[("c1/w3-02-logistic-regression.html", "Logistic regression"),
             ("f0/w1-14-exponentials.html", "Exponentials and e")],
    watch="Where the curve is steepest is where the model learns fastest. At the flat "
          "ends the gradient nearly vanishes — remember this when ReLU appears."),

"C1_W3_Lab03_Decision_Boundary_Soln.ipynb": dict(
    course="C1", week=3, kind="optional", mins=25,
    blurb="Draws the boundary for a two-feature classifier, then adds polynomial "
          "features and draws a circular one.",
    lessons=[("c1/w3-03-decision-boundary.html", "The decision boundary")],
    watch="The boundary is always where z = 0. Curved boundaries come from curved "
          "features, never from a curved sigmoid."),

"C1_W3_Lab04_LogisticLoss_Soln.ipynb": dict(
    course="C1", week=3, kind="optional", mins=25,
    blurb="Plots squared error on a sigmoid — visibly lumpy — next to logistic loss, "
          "which is a clean bowl. This is the “why this formula” lab.",
    lessons=[("c1/w3-05-logistic-loss.html", "Logistic loss"),
             ("f0/w1-15-logarithms.html", "Logarithms")],
    watch="The lumpy surface is what non-convex means. Gradient descent on it ends "
          "wherever it happened to start."),

"C1_W3_Lab05_Cost_Function_Soln.ipynb": dict(
    course="C1", week=3, kind="optional", mins=20,
    blurb="The combined cost, and a check that it collapses correctly for y = 0 and y = 1.",
    lessons=[("c1/w3-06-simplified-cost-function.html", "The simplified cost function")],
    watch="The multiply-by-zero trick that switches off one term. You will see it again "
          "in softmax and in collaborative filtering."),

"C1_W3_Lab06_Gradient_Descent_Soln.ipynb": dict(
    course="C1", week=3, kind="optional", mins=30,
    blurb="Gradient descent for logistic regression. Put this side by side with the "
          "Week 1 version and look for the difference.",
    lessons=[("c1/w3-07-gradient-descent-logistic.html", "Gradient descent for logistic regression")],
    watch="The gradient code is identical to linear regression. Only f changed. That "
          "is not a coincidence — it falls out of both losses' derivatives."),

"C1_W3_Lab07_Scikit_Learn_Soln.ipynb": dict(
    course="C1", week=3, kind="optional", mins=10,
    blurb="LogisticRegression in three lines.",
    lessons=[("c1/w3-02-logistic-regression.html", "Logistic regression")],
    watch="sklearn regularizes by default (C = 1.0). Your hand-written version does not, "
          "so the two will not give identical weights unless you say so."),

"C1_W3_Lab08_Overfitting_Soln.ipynb": dict(
    course="C1", week=3, kind="optional", mins=25,
    blurb="An interactive widget: add polynomial degrees and watch the fit go from "
          "sensible to absurd, then turn lambda up and watch it come back.",
    lessons=[("c1/w3-08-the-problem-of-overfitting.html", "The problem of overfitting"),
             ("c1/w3-09-addressing-overfitting.html", "Addressing overfitting")],
    watch="The overfitted curve passes through every training point perfectly. Perfect "
          "training accuracy is the symptom, not the goal."),

"C1_W3_Lab09_Regularization_Soln.ipynb": dict(
    course="C1", week=3, kind="optional", mins=30,
    blurb="Regularized cost and gradient for both linear and logistic regression, side "
          "by side.",
    lessons=[("c1/w3-10-cost-function-with-regularization.html", "Cost function with regularization"),
             ("c1/w3-11-regularized-gradient-descent.html", "Regularized gradient descent")],
    watch="b never appears in the penalty. Check that in the code — it is one line and "
          "easy to get wrong in your own implementation."),

"C1_W3_Logistic_Regression.ipynb": dict(
    course="C1", week=3, kind="graded", mins=180,
    blurb="Six exercises, the most in the specialization: sigmoid, cost, gradient, "
          "predict, and then the regularized versions of the last two. Budget real time.",
    lessons=[("c1/w3-02-logistic-regression.html", "Logistic regression"),
             ("c1/w3-06-simplified-cost-function.html", "The simplified cost function"),
             ("c1/w3-07-gradient-descent-logistic.html", "Gradient descent for logistic regression"),
             ("c1/w3-11-regularized-gradient-descent.html", "Regularized gradient descent")],
    watch="Exercises 5 and 6 are exercises 2 and 3 plus one extra term each. Write them "
          "by copying your own earlier answer and adding the penalty.",
    exercises=[
      E(1, "sigmoid(z)",
        "Return g(z), working for a scalar, a vector or a matrix.",
        "g(z) = 1 / (1 + e^(−z))",
        "same shape as the input — do not reshape anything",
        "Using math.exp, which only accepts scalars. Use np.exp."),
      E(2, "compute_cost(X, y, w, b, lambda_=1)",
        "Average logistic loss. lambda_ is accepted but unused at this stage.",
        "J = (1/m) Σ [ −y log(f) − (1−y) log(1−f) ]",
        "X is (m,n), w is (n,); returns a float",
        "log(0) when a prediction saturates. Also: the parameter is lambda_ with a "
        "trailing underscore, because lambda is a Python keyword."),
      E(3, "compute_gradient(X, y, w, b, lambda_=None)",
        "Return dj_db then dj_dw — note that order, it is the reverse of Week 2.",
        "dj_dw = (1/m) Σ (f−y)x &nbsp;·&nbsp; dj_db = (1/m) Σ (f−y)",
        "dj_dw is (n,), dj_db is a float",
        "Returning them the wrong way round. The signature here is (dj_db, dj_dw)."),
      E(4, "predict(X, w, b)",
        "Return 0/1 labels, not probabilities.",
        "predict 1 when g(w·x + b) ≥ 0.5",
        "returns (m,) of 0s and 1s",
        "Returning probabilities. The grader wants hard labels."),
      E(5, "compute_cost_reg(X, y, w, b, lambda_=1)",
        "Exercise 2 plus the penalty.",
        "J + (λ/2m) Σ w<sub>j</sub>²",
        "still a float",
        "Including b in the penalty. Only w is regularized."),
      E(6, "compute_gradient_reg(X, y, w, b, lambda_=1)",
        "Exercise 3 plus the penalty's derivative.",
        "dj_dw += (λ/m) w<sub>j</sub> &nbsp;·&nbsp; dj_db unchanged",
        "dj_dw is (n,), dj_db is a float",
        "Adding the penalty term to dj_db as well. It must not be there."),
    ]),

# ============================================================ C2 W1
"C2_W1_Lab01_Neurons_and_Layers.ipynb": dict(
    course="C2", week=1, kind="optional", mins=30,
    blurb="Shows that a single neuron with a linear activation IS linear regression, and "
          "one with a sigmoid IS logistic regression. The best bridge between the courses.",
    lessons=[("c2/w1-04-neural-network-layer.html", "A neural network layer"),
             ("c2/w1-01-neurons-and-the-brain.html", "Neurons and the brain")],
    watch="It sets the neuron's weights to the ones you fitted in Course 1 and gets "
          "identical predictions. Nothing new was invented — it was renamed."),

"C2_W1_Lab02_CoffeeRoasting_TF.ipynb": dict(
    course="C2", week=1, kind="optional", mins=35,
    blurb="A two-layer network in Keras on the coffee-roasting data, including the "
          "Normalization layer that people forget to reuse at prediction time.",
    lessons=[("c2/w1-09-building-a-network-sequential.html", "Building a network with Sequential"),
             ("c2/w1-08-data-in-tensorflow.html", "Data in TensorFlow")],
    watch="The Normalization layer is adapted on the training data and then must be "
          "applied to anything new. It is part of the model, exactly like mu and sigma."),

"C2_W1_Lab03_CoffeeRoasting_Numpy.ipynb": dict(
    course="C2", week=1, kind="optional", mins=40,
    blurb="The same network in raw NumPy — the lab that shows Keras is not doing anything "
          "mysterious. Pair it with the from-scratch forward-propagation page.",
    lessons=[("c2/w1-10-forward-prop-single-layer.html", "Forward prop in a single layer"),
             ("c2/w1-16-matmul-code.html", "Matrix multiplication in code"),
             ("scratch/03-forward-propagation.html", "From scratch: forward propagation")],
    watch="The hidden units really do become “too cool”, “too long” and “about right” "
          "detectors. Print the hidden layer's output and read it."),

"C2_W1_Assignment.ipynb": dict(
    course="C2", week=1, kind="graded", mins=120,
    blurb="Handwritten digit recognition, 0 versus 1. You build the same layer three "
          "times: in Keras, as a NumPy loop, and as a matrix multiply.",
    lessons=[("c2/w1-09-building-a-network-sequential.html", "Building a network with Sequential"),
             ("c2/w1-10-forward-prop-single-layer.html", "Forward prop in a single layer"),
             ("c2/w1-16-matmul-code.html", "Matrix multiplication in code")],
    watch="Exercises 2 and 3 must produce identical numbers. If they do not, the "
          "difference tells you exactly which index you have transposed.",
    exercises=[
      E(1, "model = Sequential([...])",
        "Build a 25-15-1 network with sigmoid activations.",
        "each Dense layer computes g(a·W + b)",
        "input is 400 pixels (a flattened 20×20 image)",
        "Forgetting the activation argument, which silently gives you a linear layer."),
      E(2, "my_dense(a_in, W, b, g)",
        "One layer, one example, written as a loop over units.",
        "a<sub>j</sub> = g(w<sub>j</sub> · a_in + b<sub>j</sub>)",
        "a_in is (n_in,), W is (n_in, n_out), returns (n_out,)",
        "W[:, j] is unit j's weights — a column, not a row. Getting this backwards "
        "gives a shape error if the layer is not square, and silent nonsense if it is."),
      E(3, "my_dense_v(A_in, W, b, g)",
        "The same layer for a whole batch, with no loop.",
        "A_out = g(A_in @ W + b)",
        "A_in is (m, n_in), returns (m, n_out)",
        "This is one line. If yours is longer, you are probably looping over examples."),
    ]),

# ============================================================ C2 W2
"C2_W2_Relu.ipynb": dict(
    course="C2", week=2, kind="optional", mins=15,
    blurb="Short and genuinely illuminating: shows how ReLU units switch on at different "
          "points to build a piecewise-linear function of any shape.",
    lessons=[("c2/w2-03-sigmoid-alternatives.html", "Alternatives to the sigmoid"),
             ("c2/w2-05-why-activations.html", "Why we need activation functions")],
    watch="Each unit contributes nothing until its own threshold, then a straight line. "
          "Stacking those gives you any curve you like."),

"C2_W2_SoftMax.ipynb": dict(
    course="C2", week=2, kind="optional", mins=25,
    blurb="Softmax, and the numerically better way to compute it. This is where "
          "from_logits=True is explained.",
    lessons=[("c2/w2-07-softmax.html", "Softmax"),
             ("c2/w2-09-improved-softmax.html", "Improved softmax implementation"),
             ("scratch/05-softmax.html", "From scratch: softmax")],
    watch="The roundoff demonstration is real, not academic. Large logits are ordinary "
          "in a trained network."),

"C2_W2_Multiclass_TF.ipynb": dict(
    course="C2", week=2, kind="optional", mins=25,
    blurb="Four blobs, four classes, and a plot of the decision regions each hidden unit "
          "carves out.",
    lessons=[("c2/w2-06-multiclass.html", "Multiclass classification"),
             ("c2/w2-08-softmax-output-layer.html", "The softmax output layer")],
    watch="The hidden layer's boundaries are straight lines; the final regions are not. "
          "That composition is what depth buys."),

"C2_W2_Derivatives.ipynb": dict(
    course="C2", week=2, kind="optional", mins=25,
    blurb="Uses SymPy to compute derivatives symbolically, so you can check the rules "
          "rather than take them on faith.",
    lessons=[("c2/w2-13-what-is-a-derivative.html", "What is a derivative"),
             ("f0/w1-05-derivatives.html", "Derivatives")],
    watch="Try the “nudge by epsilon” calculation by hand first, then let SymPy confirm "
          "it. Doing it in that order is the whole value of the lab."),

"C2_W2_Backprop.ipynb": dict(
    course="C2", week=2, kind="optional", mins=45,
    blurb="Computation graphs drawn out node by node, with the backward pass filled in "
          "one arrow at a time. The clearest treatment of backprop in the course.",
    lessons=[("c2/w2-14-computation-graph.html", "The computation graph"),
             ("c2/w2-15-larger-network-example.html", "A larger network example"),
             ("scratch/04-backpropagation.html", "From scratch: backpropagation")],
    watch="Backprop is right-to-left because that is the direction in which each "
          "quantity is already known. Forward computes values; backward computes "
          "sensitivities."),

"C2_W2_Assignment.ipynb": dict(
    course="C2", week=2, kind="graded", mins=120,
    blurb="Handwritten digits, all ten this time. Two exercises: write softmax yourself, "
          "then build the network the recommended way.",
    lessons=[("c2/w2-07-softmax.html", "Softmax"),
             ("c2/w2-09-improved-softmax.html", "Improved softmax implementation"),
             ("c2/w2-11-advanced-optimization.html", "Advanced optimization")],
    watch="The output layer is linear, not softmax. That is deliberate, and the loss "
          "argument from_logits=True is what completes it.",
    exercises=[
      E(1, "my_softmax(z)",
        "Softmax over a 1-D vector of logits.",
        "a_j = e^(z_j) / Σ_k e^(z_k)",
        "z is (n,), returns (n,) summing to 1",
        "Not subtracting max(z) first. It passes the grader on small inputs and "
        "overflows on real ones."),
      E(2, "model = Sequential([...])",
        "A 25-15-10 network with a LINEAR output layer.",
        "the softmax lives inside the loss, not the model",
        "input 400 features, output 10 logits",
        "Using activation='softmax' on the output. Then from_logits=True applies "
        "softmax twice and the model trains badly but not obviously so."),
    ]),

# ============================================================ C2 W3
"C2_W3_Assignment.ipynb": dict(
    course="C2", week=3, kind="graded", mins=150,
    blurb="The diagnosis assignment: build the error metrics, then use them to compare "
          "models of different complexity and pick lambda.",
    lessons=[("c2/w3-02-evaluating-a-model.html", "Evaluating a model"),
             ("c2/w3-03-model-selection.html", "Model selection"),
             ("c2/w3-04-bias-and-variance.html", "Bias and variance"),
             ("c2/w3-05-regularization-bias-variance.html", "Regularization and bias/variance")],
    watch="The whole assignment is one loop: train, measure on cross-validation, "
          "compare. The final number you report must come from the test set.",
    exercises=[
      E(1, "eval_mse(y, yhat)",
        "Mean squared error for regression.",
        "J = (1/2m) Σ (yhat − y)²",
        "both are (m,); returns a float",
        "The ½. This version halves it, matching the course's convention."),
      E(2, "eval_cat_err(y, yhat)",
        "Fraction of categorical predictions that are wrong.",
        "error = (number wrong) / m",
        "returns a float in [0, 1]",
        "Returning accuracy instead of error. This wants the fraction WRONG."),
      E(3, "model = Sequential([...])",
        "A deliberately complex model, to produce overfitting you can see.",
        "more units and layers means more variance",
        "linear output, from_logits in the loss",
        "Making it too small to overfit, which defeats the demonstration."),
      E(4, "model_s = Sequential([...])",
        "A deliberately simple model, to produce underfitting.",
        "fewer units means more bias",
        "same input and output sizes",
        "Comparing against the complex model on the training set only. The gap "
        "between train and cv is the whole point."),
      E(5, "model_r = Sequential([..., kernel_regularizer=...])",
        "The complex model again, with L2 regularization added.",
        "cost += λ Σ w²",
        "regularize the hidden layers, not the output",
        "Sweeping lambda and then reporting the best cross-validation error as the "
        "final result. That number chose lambda, so it is optimistic."),
    ]),

# ============================================================ C2 W4
"C2_W4_Lab_01_Decision_Trees.ipynb": dict(
    course="C2", week=4, kind="optional", mins=25,
    blurb="Builds the cat/not-cat tree from the lectures step by step, printing the "
          "entropy and gain at each split.",
    lessons=[("c2/w4-04-information-gain.html", "Information gain"),
             ("c2/w4-05-putting-it-together.html", "Putting it together"),
             ("scratch/06-decision-tree.html", "From scratch: a decision tree")],
    watch="Check the printed gains against 0.2781, 0.0349 and 0.1245. Those are the "
          "lecture's numbers and they should match exactly."),

"C2_W4_Lab_02_Tree_Ensemble.ipynb": dict(
    course="C2", week=4, kind="optional", mins=35,
    blurb="Random forests and XGBoost on a heart-disease dataset, with plots of "
          "performance against the number of trees.",
    lessons=[("c2/w4-11-random-forest.html", "Random forest"),
             ("c2/w4-12-xgboost.html", "XGBoost")],
    watch="Adding trees to a forest improves it and then flattens — it does not start "
          "overfitting. That is the property that makes forests forgiving."),

"C2_W4_Decision_Tree_with_Markdown.ipynb": dict(
    course="C2", week=4, kind="graded", mins=120,
    blurb="Build a decision tree from nothing: entropy, splitting, information gain, and "
          "choosing the best feature. No gradients anywhere.",
    lessons=[("c2/w4-03-measuring-purity.html", "Measuring purity"),
             ("c2/w4-04-information-gain.html", "Information gain"),
             ("c2/w4-05-putting-it-together.html", "Putting it together"),
             ("scratch/06-decision-tree.html", "From scratch: a decision tree")],
    watch="The four exercises are a chain: each one uses the last. Get exercise 1 exactly "
          "right before starting exercise 3, or you will debug the wrong function.",
    exercises=[
      E(1, "compute_entropy(y)",
        "Entropy of a set of 0/1 labels.",
        "H(p) = −p log₂ p − (1−p) log₂(1−p)",
        "y is (n,); returns a float",
        "An empty node, and p = 0 or 1. All three must return 0, and log₂(0) is −inf "
        "if you do not special-case them."),
      E(2, "split_dataset(X, node_indices, feature)",
        "Split a node's indices into left (feature == 1) and right (feature == 0).",
        "no maths — pure bookkeeping",
        "returns two lists of INDICES, not two arrays of data",
        "Returning rows of X instead of indices. Everything downstream expects indices."),
      E(3, "compute_information_gain(X, y, node_indices, feature)",
        "Gain from splitting this node on this feature.",
        "H(node) − [ w_left·H(left) + w_right·H(right) ]",
        "returns a float",
        "Forgetting the size weights. Unweighted entropy makes tiny pure branches "
        "look wonderful."),
      E(4, "get_best_split(X, y, node_indices)",
        "The feature with the highest information gain.",
        "argmax over features of the gain",
        "returns an int feature index, or −1 if no split helps",
        "Returning the gain instead of the index."),
    ]),

# ============================================================ C3 W1
"C3_W1_KMeans_Assignment.ipynb": dict(
    course="C3", week=1, kind="graded", mins=120,
    blurb="k-means, then used to compress an image down to 16 colours — the most "
          "visually satisfying result in the specialization.",
    lessons=[("c3/w1-03-kmeans-algorithm.html", "The k-means algorithm"),
             ("c3/w1-04-kmeans-cost.html", "The k-means cost function"),
             ("scratch/07-kmeans.html", "From scratch: k-means")],
    watch="The image compression at the end treats every pixel as a point in 3-D colour "
          "space. Nothing about the algorithm changes; only the interpretation does.",
    exercises=[
      E(1, "find_closest_centroids(X, centroids)",
        "Assign each example to its nearest centroid.",
        "idx<sup>(i)</sup> = argmin_k ‖x<sup>(i)</sup> − μ_k‖²",
        "X is (m,n), centroids is (K,n); returns (m,) of ints",
        "Returning the distance instead of the index. You can also skip the square "
        "root entirely — it does not change which is smallest."),
      E(2, "compute_centroids(X, idx, K)",
        "Move each centroid to the mean of its assigned points.",
        "μ_k = (1/|C_k|) Σ x<sup>(i)</sup> for i in cluster k",
        "returns (K, n)",
        "An empty cluster gives 0/0 and a nan that then poisons every later "
        "assignment."),
    ]),

"C3_W1_Anomaly_Detection.ipynb": dict(
    course="C3", week=1, kind="graded", mins=120,
    blurb="Fit a Gaussian per feature, then choose the threshold epsilon by maximising "
          "F1 on a cross-validation set that contains the known anomalies.",
    lessons=[("c3/w1-08-gaussian-distribution.html", "The Gaussian distribution"),
             ("c3/w1-09-anomaly-detection-algorithm.html", "The anomaly detection algorithm"),
             ("c3/w1-10-developing-anomaly-detection.html", "Developing an anomaly detection system")],
    watch="F1, not accuracy. With anomalies at well under 1%, accuracy is a measure of "
          "the base rate and nothing else.",
    exercises=[
      E(1, "estimate_gaussian(X)",
        "Mean and variance of every feature.",
        "μ_j = (1/m) Σ x_j &nbsp;·&nbsp; σ²_j = (1/m) Σ (x_j − μ_j)²",
        "X is (m,n); returns two (n,) arrays",
        "Using np.var's default, which divides by m. That is what this wants — but "
        "check, because some libraries default to m−1."),
      E(2, "select_threshold(y_val, p_val)",
        "Sweep epsilon and return the one with the best F1.",
        "prec = tp/(tp+fp) · rec = tp/(tp+fn) · F1 = 2·prec·rec/(prec+rec)",
        "returns (best_epsilon, best_F1)",
        "Division by zero when an epsilon flags nothing at all, making tp + fp = 0."),
    ]),

# ============================================================ C3 W2
"C3_W2_Collaborative_RecSys_Assignment.ipynb": dict(
    course="C3", week=2, kind="graded", mins=120,
    blurb="Collaborative filtering on the MovieLens data. One exercise, but it is the "
          "cost function for two sets of unknowns at once.",
    lessons=[("c3/w2-03-collaborative-filtering.html", "Collaborative filtering"),
             ("c3/w2-05-mean-normalization.html", "Mean normalization"),
             ("scratch/09-collaborative-filtering.html", "From scratch: collaborative filtering")],
    watch="Write the loop version first and get it passing, then vectorize it. The lab "
          "explicitly supports doing it in that order, and the speed difference at the "
          "end is worth seeing.",
    exercises=[
      E(1, "cofi_cost_func(X, W, b, Y, R, lambda_)",
        "Squared error over rated cells only, plus regularization on both X and W.",
        "J = ½ Σ_(i,j):r=1 (w<sup>(j)</sup>·x<sup>(i)</sup> + b<sup>(j)</sup> − y⁽<sup>i</sup>'<sup>j</sup>⁾)² + (λ/2)(Σw² + Σx²)",
        "X is (n_m, n), W is (n_u, n), Y and R are (n_m, n_u)",
        "Forgetting to multiply by R. Without it, every unrated cell is treated as a "
        "rating of zero, and the model learns to predict zero for everything."),
    ]),

"C3_W2_RecSysNN_Assignment.ipynb": dict(
    course="C3", week=2, kind="graded", mins=120,
    blurb="Content-based filtering with two neural networks — one for users, one for "
          "items — meeting at a dot product.",
    lessons=[("c3/w2-09-deep-content-based.html", "Deep learning for content-based filtering"),
             ("c3/w2-07-finding-related-items.html", "Finding related items"),
             ("c3/w2-08-collaborative-vs-content.html", "Collaborative vs content-based")],
    watch="The two towers must output vectors of the same length, or the dot product at "
          "the end is undefined.",
    exercises=[
      E(1, "user_NN / item_NN",
        "Build the two towers.",
        "each is a small Sequential ending in a linear layer of size num_outputs",
        "both must end at the SAME width",
        "Different output widths. The error appears at the dot product, several "
        "layers away from the mistake."),
      E(2, "sq_dist(a, b)",
        "Squared distance between two feature vectors, for finding similar items.",
        "‖a − b‖² = Σ (aᵢ − bᵢ)²",
        "a and b are (n,); returns a float",
        "Returning the distance rather than its square. The lab wants the square, and "
        "the ordering is the same either way."),
    ]),

# ============================================================ C3 W3
"State-action value function example.ipynb": dict(
    course="C3", week=3, kind="optional", mins=20,
    blurb="A slider over the six-state Mars rover: change gamma or the rewards and watch "
          "Q and the optimal policy update live.",
    lessons=[("c3/w3-07-state-action-value-example.html", "State-action value function example"),
             ("c3/w3-08-bellman-equation.html", "The Bellman equation"),
             ("scratch/10-reinforcement-learning.html", "From scratch: reinforcement learning")],
    watch="Drag gamma down through 0.4 and watch state 4 flip from left to right. That "
          "is the exact point where 100γ³ = 40γ²."),

"C3_W3_A1_Assignment.ipynb": dict(
    course="C3", week=3, kind="graded", mins=180,
    blurb="Deep Q-learning on the lunar lander. The longest assignment, and the only one "
          "where you watch the thing learn to do something physical.",
    lessons=[("c3/w3-11-lunar-lander.html", "The lunar lander"),
             ("c3/w3-12-learning-the-state-value-function.html", "Learning the state-value function"),
             ("c3/w3-15-minibatch-soft-updates.html", "Mini-batches and soft updates")],
    watch="Training takes real time — tens of minutes. Do not conclude it is broken "
          "because nothing has happened after 200 episodes.",
    exercises=[
      E(1, "q_network / target_q_network",
        "Two identical networks: 64-64-num_actions, ReLU hidden, linear output.",
        "Q(s,a) is a value, so the output must be linear",
        "input is the 8-dimensional state, output is one value per action",
        "A softmax or sigmoid output. Q values are unbounded — they are not "
        "probabilities."),
      E(2, "compute_loss(experiences, gamma, q_network, target_q_network)",
        "The mean squared error between the network's Q and the Bellman target.",
        "y = R if terminal, else R + γ max_a′ Q_target(s′, a′)",
        "returns a scalar loss",
        "Using q_network instead of target_q_network for the target. That is the "
        "moving-target instability the whole two-network design exists to prevent — "
        "and it trains, badly, without ever erroring."),
    ]),
}
