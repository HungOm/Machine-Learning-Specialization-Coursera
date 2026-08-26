# -*- coding: utf-8 -*-
"""The symbol glossary: every symbol, how to say it, what it means, and its code equivalent."""

# (symbol, say it, what it means, code equivalent, where you meet it)
GROUPS = [

("Greek letters", [
 ("α", "alpha", "learning rate — the step size for gradient descent", "alpha = 0.01", "C1 W1 · everywhere"),
 ("β₁, β₂", "beta one, beta two", "decay rates inside Adam. 0.9 and 0.999", "Adam(beta_1=0.9)", "C2 W2"),
 ("γ", "gamma", "discount factor — how much a future reward is worth now", "gamma = 0.99", "C3 W3"),
 ("ε", "epsilon", "a tiny number: a threshold, or a guard against dividing by zero", "eps = 1e-8", "C3 W1, W3"),
 ("θ", "theta", "parameters — another name for the collection of w and b", "theta", "papers, not this course"),
 ("λ", "lambda", "regularisation strength — how hard weights are pushed towards zero", "lambda_ = 1.0", "C1 W3 · C2 W3"),
 ("μ", "mu", "the mean — the plain average", "x.mean()", "C1 W2 · C3 W1"),
 ("π", "pi (lowercase)", "in RL, a <b>policy</b>: state in, action out. Not 3.14159 there", "policy", "C3 W3"),
 ("σ", "sigma", "standard deviation — how spread out something is", "x.std()", "C1 W2 · C3 W1"),
 ("σ²", "sigma squared", "variance — the average squared distance from the mean", "x.var()", "C3 W1 · C2 W4"),
 ("σ(z)", "sigma of z", "confusingly, also used for the <b>sigmoid</b> function", "1/(1+np.exp(-z))", "papers"),
 ("τ", "tau", "soft-update rate — how much of a new network to blend in", "tau = 0.01", "C3 W3"),
 ("Σ", "capital sigma", "<b>add all of these up</b>. A for loop", "np.sum(x)", "everywhere"),
 ("Π", "capital pi", "<b>multiply all of these together</b>", "np.prod(p)", "C3 W1"),
 ("∇", "nabla / del", "the gradient — every partial derivative collected into one list", "grads", "C1 W1 · C2 W2"),
 ("∂", "partial / curly dee", "rate of change of, with the other variables held still", "—", "C1 W1 onward"),
 ("Δ", "delta", "“the change in”", "y2 - y1", "C1 W1"),
]),

("Model and data", [
 ("x", "ex", "an input — one feature value", "x", "C1 W1"),
 ("x⃗ or <b>x</b>", "x vector", "a whole example — a list of feature values", "x = np.array([...])", "C1 W2"),
 ("x<sub>j</sub>", "x sub j", "feature j — which <b>column</b>", "X[:, j]", "C1 W2"),
 ("x<sup>(i)</sup>", "x, example i", "training example i — which <b>row</b>", "X[i]", "C1 W1"),
 ("x<sub>j</sub><sup>(i)</sup>", "x sub j, example i", "feature j of example i — one number", "X[i, j]", "C1 W2"),
 ("y", "why", "the true answer — the target or label", "y", "C1 W1"),
 ("ŷ", "y hat", "the <b>prediction</b>. The hat always means “estimated”", "y_pred", "C1 W1"),
 ("m", "em", "the number of training <b>examples</b> (rows)", "X.shape[0]", "everywhere"),
 ("n", "en", "the number of <b>features</b> (columns)", "X.shape[1]", "C1 W2"),
 ("w", "double-you", "a weight — the slope. What the model learns", "w", "C1 W1"),
 ("b", "bee", "the bias or intercept. Also learned", "b", "C1 W1"),
 ("f(x)", "f of x", "the model's output for input x", "model(x)", "C1 W1"),
 ("X", "capital X", "the whole feature matrix, shape (m, n)", "X", "C1 W2"),
]),

("Cost, loss and training", [
 ("J", "jay", "the <b>cost</b> — average loss over all examples. What you minimise", "compute_cost(...)", "C1 W1"),
 ("L", "ell", "the <b>loss</b> — the error on <b>one</b> example", "—", "C1 W3"),
 (":=", "becomes", "assignment, not equality. “Replace the old value with this”", "w = w - ...", "C1 W1"),
 ("J<sub>train</sub>", "J train", "error on the data the model learned from", "cost(X_train, y_train)", "C2 W3"),
 ("J<sub>cv</sub>", "J see-vee", "error on held-out data used to <b>choose</b> the model", "cost(X_cv, y_cv)", "C2 W3"),
 ("J<sub>test</sub>", "J test", "error on data touched exactly <b>once</b>, at the end", "cost(X_test, y_test)", "C2 W3"),
 ("g(z)", "g of z", "the activation function — the squasher", "sigmoid(z), relu(z)", "C1 W3 · C2 W1"),
 ("z", "zee", "the raw weighted sum, before squashing. Also called a <b>logit</b>", "X @ w + b", "C1 W3"),
 ("a", "a (activation)", "what a neuron outputs after squashing", "a1 = g(z1)", "C2 W1"),
 ("a<sup>[l]</sup>", "a, layer l", "the whole output of layer l", "a2", "C2 W1"),
 ("W<sup>[l]</sup>", "capital W, layer l", "the weight <b>matrix</b> of layer l. Columns are neurons", "W2", "C2 W1"),
]),

("Maths operations", [
 ("·", "dot", "the dot product: multiply the pairs <b>and add them up</b>", "a @ b", "C1 W2"),
 ("×", "times", "ordinary multiplication", "a * b", "everywhere"),
 ("A<sup>T</sup>", "A transpose", "rows and columns swapped", "A.T", "C1 W2 · C2 W1"),
 ("‖x‖", "the norm of x", "the <b>length</b> of a vector. Double bars", "np.linalg.norm(x)", "C3 W1"),
 ("|x|", "absolute value", "distance from zero, for a single number. Single bars", "abs(x)", "—"),
 ("√", "square root", "the number that, times itself, gives this one. √9 = 3",
  "np.sqrt(x)", "C1 W2"),
 ("e<sup>z</sup>", "e to the z", "exponential. Always positive, grows fast", "np.exp(z)", "C1 W3 · C2 W2"),
 ("log", "log", "natural log (base e) unless stated. Turns tiny into huge", "np.log(x)", "C1 W3"),
 ("log₂", "log base two", "used for entropy, so answers come out in bits", "np.log2(x)", "C2 W4"),
 ("max / min", "max / min", "the biggest / smallest <b>value</b>", "np.max(x)", "everywhere"),
 ("argmax", "arg max", "the <b>position</b> that gives the biggest value", "np.argmax(x, axis=1)", "C2 W2 · C3 W3"),
 ("argmin", "arg min", "the position that gives the smallest", "np.argmin(x)", "C3 W1"),
 ("∈", "is an element of", "“is one of”. y ∈ {0, 1} means y is 0 or 1", "in", "C2 W2"),
 ("≈", "approximately equals", "close enough — usually because the number was rounded",
  "np.allclose(a, b)", "—"),
  ("≠", "not equal to", "these two are different — the shape rule uses it a lot",
  "a != b", "C1 W2 · C2 W1"),
 ("≥", "greater than or equal to", "at least this much. “≤” is at most",
  "x >= 3", "C1 W3"),
 ("δ", "delta", "a small change in something; also the error term inside backprop",
  "delta", "C2 W2"),
 ("η", "eta", "another letter for the learning rate — papers use it where this course uses α",
  "lr", "papers"),
 ("ρ", "rho", "a correlation, or a decay rate, depending on context",
  "rho", "papers"),
 ("∞", "infinity", "endlessly large", "np.inf", "C1 W3"),
 ("Σ x²", "sum of x squared", "square <b>each</b>, then add. Not add then square", "np.sum(x**2)", "C1 W1"),

 ("X<sup>-1</sup>", "X inverse", "the matrix that undoes X. Finding one costs about "
  "n&sup3;, which is why the normal equation stops scaling", "np.linalg.inv(X)", "C1 W2"),
]),

("Probability and statistics", [
 ("P(A)", "P of A", "the probability of A. Always between 0 and 1", "—", "C1 W3"),
 ("P(y=1 | x)", "P of y equals 1, <b>given</b> x", "the bar means “given”. What every classifier outputs", "model.predict(x)", "C1 W3"),
 ("E[…]", "the expected value of", "the average over everything that could happen", "—", "C3 W3"),
 ("~ N(μ, σ²)", "is distributed normally with…", "follows a bell curve with that middle and spread", "np.random.normal(mu, sigma)", "C3 W1"),
 ("H(p)", "H of p", "entropy — how mixed up a group is. 0 = pure, 1 = 50/50", "—", "C2 W4"),
 ("x̄", "x bar", "the sample mean. Another way of writing μ", "x.mean()", "—"),

 ("E[X]", "the expected value of X", "the average outcome, weighted by how likely each one is",
  "(p * x).sum()", "C3 W3"),
 ("P(A | B)", "probability of A given B", "how likely A is once you already know B happened",
  "&mdash;", "C2 W2"),
 ("random variable", "random variable", "a quantity whose value depends on chance &mdash; the "
  "return of an episode, before you have run it", "rng.normal()", "C3 W3"),
]),

("Reinforcement learning", [
 ("s", "ess", "a state — the situation you are in", "state", "C3 W3"),
 ("a", "ay", "an action — what you do", "action", "C3 W3"),
 ("s′", "s prime", "the <b>next</b> state. Prime always means “next”", "next_state", "C3 W3"),
 ("R(s)", "R of s", "the reward for being in state s", "reward", "C3 W3"),
 ("Q(s, a)", "Q of s a", "the return from doing a in s, then playing perfectly", "q_values[s, a]", "C3 W3"),
 ("V(s)", "V of s", "the value of state s — the best Q available there", "np.max(q[s])", "C3 W3"),
 ("π(s)", "pi of s", "the policy: given state s, take this action", "policy[s]", "C3 W3"),
 ("π*", "pi star", "the <b>optimal</b> policy. A star always means “best”", "—", "C3 W3"),

 ("1 + &gamma; + &gamma;&sup2; + &hellip;", "geometric series", "a sum where each term is a fixed "
  "fraction of the last. Adds up to 1 &divide; (1 &minus; &gamma;) when &gamma; &lt; 1, which is why "
  "an endless run still has a finite return", "1/(1-g)", "C3 W3"),
]),
("Trigonometry — the little the courses assume", [
 ("sin &theta;", "sine theta", "opposite &divide; hypotenuse &mdash; how far <b>up</b>",
  "np.sin(np.deg2rad(d))", "C3 W2"),
 ("cos &theta;", "coz theta", "adjacent &divide; hypotenuse &mdash; how far <b>across</b>. "
  "1 = same direction, 0 = right angles, &minus;1 = opposite",
  "np.cos(np.deg2rad(d))", "F0 W1 &middot; C3 W2"),
 ("tan &theta;", "tan theta", "opposite &divide; adjacent &mdash; the <b>slope</b>. "
  "Not the same as a <i>tangent line</i>", "np.tan(...)", "F0 W1"),
 ("&theta;", "theta", "an <b>angle</b> when it sits beside sin, cos or tan &mdash; "
  "everywhere else in this course it means the parameters",
  "theta", "F0 W1 &middot; C3 W3"),
 ("radian", "ray-dee-an", "the angle unit code uses. &pi; radians = 180&deg;, "
  "1 radian &asymp; 57.3&deg;", "np.deg2rad(90)", "C3 W3"),
 ("a&sup2; + b&sup2; = c&sup2;", "Pythagoras", "the two short sides squared add to the long "
  "side squared. This is vector length with more terms", "np.hypot(a, b)", "F0 W1"),
 ("cosine similarity", "co-sine similarity", "(a &middot; b) &divide; (&#8214;a&#8214;&#8214;b&#8214;) "
  "&mdash; likeness of <b>direction</b>, ignoring size", "cosine_similarity(a, b)", "C3 W2"),
 ("&#8869;", "perpendicular / orthogonal", "at right angles. Their dot product is exactly <b>0</b>, "
  "because cos 90&deg; = 0", "np.dot(a, b) == 0", "C3 W2"),
]),
]
