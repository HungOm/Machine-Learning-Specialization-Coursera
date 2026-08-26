# -*- coding: utf-8 -*-
"""Narrative for the from-scratch lane. Code comes from scratch/code/*.py."""

LANE = [
dict(file="01_linear_regression.py", slug="01-linear-regression",
     title="Linear regression",
     lede="Cost, gradient and gradient descent in about sixty lines, then checked "
          "twice — once against a numerical gradient, once against the closed-form "
          "least-squares solution.",
     builds="a working multi-feature linear regressor, z-score scaling, and a "
            "gradient checker you will reuse in every later file",
     lessons=[("c1/w1-05-cost-function-formula.html", "The cost function"),
              ("c1/w1-12-gradient-descent-for-linear-regression.html", "Gradient descent for linear regression"),
              ("c1/w2-05-feature-scaling.html", "Feature scaling"),
              ("f0/w2-09-dot-in-code.html", "The dot product in code")],
     prose={
"prelude": "<p>Eight houses, three features. Small enough that you can check any "
           "number by hand, which is the whole point of starting here.</p>",
"data": "<p><code>X</code> is <b>(m, n)</b> — one row per house, one column per "
        "feature — and <code>y</code> is <b>(m,)</b>. Every shape error you will ever "
        "hit in the assignments comes from losing track of those two lines.</p>",
"cost": "<p>Three lines. <code>X @ w</code> produces all eight predictions at once "
        "and <code>+ b</code> broadcasts the same number onto every one of them. "
        "There is no loop because there does not need to be one.</p>",
"gradient": "<p>The only part worth staring at is <code>X.T @ err</code>. The maths "
            "says <i>for each feature j, sum the error times that feature</i>. "
            "Transposing X makes each feature a row, so one matrix–vector product "
            "does every feature at once. Shapes: (n, m) @ (m,) → (n,).</p>",
"check_gradient": "<p>Before trusting a hand-derived gradient, check it. Nudge one "
                  "parameter by a tiny ε, see how much the cost moved, divide. If the "
                  "analytic and numerical answers disagree beyond about 1e-6, the "
                  "analytic one is wrong — this catches almost every derivative bug "
                  "you will ever write.</p>",
"scaling": "<p>Look at the ranges before and after. Age spans 32 while size spans "
           "1.73 — a factor of nearly twenty, which means their gradients differ by "
           "nearly twenty and no single α suits both. Note the function returns μ and "
           "σ as well: <b>those are part of the trained model</b> and you must keep "
           "them to predict on anything new.</p>",
"descent": "<p>The two updates both use the <i>old</i> w and b, because both gradients "
           "were computed before either changed. Doing it any other way is the classic "
           "simultaneous-update bug — and it usually still converges, which is why it "
           "survives in so much code.</p>",
"predict": "<p>Scaling at prediction time uses the <b>training</b> μ and σ. Recomputing "
           "them from new data changes the meaning of every weight and quietly ruins "
           "the model.</p>",
"compare": "<p>The real test. <code>np.linalg.lstsq</code> solves for w and b directly, "
           "with no learning rate and no iterations. Undo our scaling and the two "
           "answers agree to three decimal places — so the sixty lines above really do "
           "compute linear regression, and not merely something that looks like it.</p>",
     }),

dict(file="02_logistic_regression.py", slug="02-logistic-regression",
     title="Logistic regression and regularization",
     lede="The same skeleton as file 01 with three substitutions — a sigmoid, a log "
          "loss, and a λ term — plus a numerical trap that bites in real code.",
     builds="a regularized logistic classifier, an overflow-proof sigmoid, and a "
            "demonstration of the hidden constraint between α and λ",
     lessons=[("c1/w3-02-logistic-regression.html", "Logistic regression"),
              ("c1/w3-05-logistic-loss.html", "Logistic loss"),
              ("c1/w3-10-cost-function-with-regularization.html", "Cost with regularization"),
              ("c1/w3-11-regularized-gradient-descent.html", "Regularized gradient descent")],
     prose={
"prelude": "<p>Eighty students, two exam scores, pass or fail. Two overlapping blobs "
           "so the problem is not trivially separable.</p>",
"data": "<p>Forty of each class, deliberately overlapping — a perfectly separable "
        "dataset would let the weights grow without limit and hide what λ does.</p>",
"sigmoid": "<p>The textbook <code>1/(1+np.exp(-z))</code> overflows for very negative "
           "z, because <code>e^1000</code> does not fit in a float. The two branches "
           "here are algebraically identical and each avoids the overflow the other "
           "would hit. Libraries all do some version of this; it is worth seeing once.</p>",
"cost": "<p>Two details. <code>np.clip</code> keeps the log away from 0, where it "
        "would return −inf. And the penalty is on <code>w</code> only — <b>never on "
        "b</b>, because shrinking the model's baseline towards zero buys nothing.</p>",
"gradient": "<p>Compare this line with the linear-regression version: "
            "<code>(X.T @ err) / m</code>. Character for character the same. Only the "
            "definition of <code>err</code> changed, because a sigmoid's derivative and "
            "a log's derivative cancel exactly. That cancellation is the real reason "
            "these two are always paired.</p>",
"check_gradient": "<p>Same checker as file 01, now with λ switched on, so the "
                  "penalty's derivative <code>(λ/m)·w</code> is verified too.</p>",
"train": "<p>Nothing new — the loop is identical to linear regression.</p>",
"evaluate": "<p>The threshold at 0.5 is a <i>separate decision</i> made after training. "
            "The model outputs a probability; turning it into a label is your choice, "
            "and moving it trades precision against recall.</p>",
"boundary": "<p>The boundary is wherever z = 0, because g(0) = 0.5. You never compute "
            "a sigmoid to find it — solve the straight line instead.</p>",
"regularization": "<p>Watch ‖w‖ shrink as λ grows while accuracy holds or improves. "
                  "That is regularization doing its job: the same decisions, made with "
                  "less confidence, which generalises better.</p>",
"decay_limit": "<p>Now the trap. The regularized update is "
               "<code>w := w(1 − αλ/m) − α·gradient</code>, so it shrinks w by a factor "
               "before every step. If <code>αλ/m &gt; 2</code> that factor goes past "
               "−1 and the weights flip sign and grow every iteration. A λ that is "
               "perfectly safe at one α diverges at another — and this is not in any "
               "lecture.</p>",
     }),

dict(file="03_neural_net_forward.py", slug="03-forward-propagation",
     title="Forward propagation",
     lede="From one neuron to a whole network. The loop version and the matrix "
          "version, side by side, producing identical numbers — and a proof that "
          "without activations, depth buys nothing.",
     builds="a general forward pass for any depth, and a network you construct by "
            "hand whose behaviour you can predict exactly",
     lessons=[("c2/w1-04-neural-network-layer.html", "A neural network layer"),
              ("c2/w1-10-forward-prop-single-layer.html", "Forward prop in a single layer"),
              ("c2/w1-16-matmul-code.html", "Matrix multiplication in code"),
              ("c2/w2-05-why-activations.html", "Why we need activation functions")],
     prose={
"prelude": "<p>No training in this file — only the forward pass, so nothing is "
           "hidden behind an optimiser.</p>",
"one_neuron": "<p>A neuron is a dot product wearing a squash function. Once that "
              "sentence is genuinely obvious, the rest of neural networks is "
              "bookkeeping about shapes.</p>",
"layer_loop": "<p>The obvious version: walk the units one at a time. Note that "
              "<code>W</code> holds each unit's weights as a <i>column</i>. That "
              "convention is what makes the next version work.</p>",
"layer_matmul": "<p>The same layer as one matrix multiply. <code>A_in @ W</code> is "
                "(m, n_in) @ (n_in, n_out) → (m, n_out): every example against every "
                "unit, in one operation. The next block proves the two agree.</p>",
"network": "<p>A network is layers feeding layers, so the whole forward pass is a "
           "<code>for</code> loop over pairs of parameters. Four lines, any depth.</p>",
"shapes": "<p>The shape trace is the single most useful debugging habit in the "
          "labs. Print it once and every mismatch becomes obvious.</p>",
"linear_collapse": "<p>Here is why activations exist, demonstrated rather than "
                   "asserted. Run the same network with the identity as its "
                   "activation and it produces exactly the same numbers as a single "
                   "layer with <code>W1 @ W2</code>. Depth without non-linearity is "
                   "an elaborate way of writing one matrix.</p>",
"detectors": "<p>“Hidden units are feature detectors” is usually said and rarely "
             "shown. Here four units are built by hand — <i>too cool</i>, "
             "<i>too hot</i>, <i>too short</i>, <i>too long</i> — and the output "
             "unit is an AND gate with a large negative weight on each, so any "
             "detector firing vetoes the roast.</p>",
"detectors_inside": "<p>Print the hidden layer and read it directly: every row of "
                    "zeros is a good roast. A trained network's hidden layer holds "
                    "exactly this kind of thing, except nobody chose what the "
                    "detectors would detect.</p>",
     }),

dict(file="04_backprop.py", slug="04-backpropagation",
     title="Backpropagation",
     lede="Every gradient derived by hand and checked numerically, then used to "
          "train a network on XOR — the smallest problem a linear model cannot "
          "solve. No autodiff anywhere.",
     builds="a complete two-layer network with hand-derived gradients, a gradient "
            "checker that passes, and a demonstration of why it fails on a ReLU kink",
     lessons=[("c2/w2-13-what-is-a-derivative.html", "What is a derivative"),
              ("c2/w2-14-computation-graph.html", "The computation graph"),
              ("c2/w2-15-larger-network-example.html", "A larger network example"),
              ("c2/w2-03-sigmoid-alternatives.html", "Alternatives to the sigmoid")],
     prose={
"prelude": "<p>This is the file that turns backprop from a word into arithmetic. "
           "Nothing here calls a library that computes a derivative for you.</p>",
"one_node": "<p>Start with the smallest graph that has anything to say. Forward: "
            "compute a, then J. Backward: work out how much J changes per unit of a, "
            "then multiply by how much a changes per unit of w. That multiplication "
            "<i>is</i> the chain rule, and it is all backprop ever does.</p>",
"derivatives": "<p>A sigmoid's derivative written in terms of its own output, "
               "<code>a(1−a)</code>, is why the forward pass caches activations: the "
               "backward pass reuses them rather than recomputing. Note the slope "
               "collapses at both ends — that is saturation, and it is what ReLU "
               "was introduced to avoid.</p>",
"forward": "<p>Same forward pass as file 03, except it now returns a cache. Every "
           "value stored here is needed on the way back.</p>",
"backward": "<p>The whole algorithm, right to left. The one piece worth pausing on: "
            "<code>dZ2 = (A2 − y)/m</code>. For a sigmoid output with log loss, the "
            "sigmoid's derivative and the log's derivative cancel completely — the "
            "same cancellation you saw in logistic regression, and the reason that "
            "pairing is universal.</p>",
"gradcheck": "<p>Four gradients, four checks, all agreeing to about 1e-10. This is "
             "the test that tells you a hand-derived backward pass is right, and "
             "it is worth writing before you trust any network you built yourself.</p>",
"relu_kink": "<p>Now break it deliberately. With biases at exactly zero, every "
             "hidden unit sees z = 0 for the input [0, 0] — precisely the kink where "
             "ReLU has no derivative. The analytic gradient picks the flat side; the "
             "numerical one averages across the corner. Neither is wrong, and the "
             "check fails for an honest mathematical reason. This is why the "
             "initialiser puts the biases slightly off zero.</p>",
"train": "<p>Full training loop: forward, backward, step, repeat. The cost falls "
         "from 0.95 to about 5e-5.</p>",
"why_hidden": "<p>The control experiment. Train the same data with no hidden layer "
              "and it sticks at exactly 0.5 for all four inputs, forever, because "
              "XOR is not linearly separable. The hidden layer is not a performance "
              "tweak — it is the thing that makes the problem solvable at all.</p>",
     }),

dict(file="05_softmax.py", slug="05-softmax",
     title="Softmax and multi-class",
     lede="Including the numerical trap that <code>from_logits=True</code> exists "
          "to avoid, demonstrated by breaking the naive version first.",
     builds="a stable softmax, a log-softmax, cross-entropy with a verified "
            "gradient, and a trained three-class classifier",
     lessons=[("c2/w2-07-softmax.html", "Softmax"),
              ("c2/w2-09-improved-softmax.html", "Improved softmax implementation"),
              ("c2/w2-10-multi-label.html", "Multi-label classification"),
              ("f0/w1-14-exponentials.html", "Exponentials and e")],
     prose={
"naive": "<p>The definition, written exactly as the formula reads. It works, right "
         "up until it does not.</p>",
"overflow": "<p>Logits in the hundreds are entirely normal in a trained network, and "
            "<code>e^1000</code> is not a number a float can hold. The naive version "
            "returns nan and your training run is over.</p>",
"stable": "<p>The fix is one line, and it is free: softmax(z + c) = softmax(z) for "
          "any constant c, because e^c cancels top and bottom. Choose c = −max(z) and "
          "the largest exponent becomes e⁰ = 1, so nothing can overflow. The shift "
          "invariance is proved numerically two lines down.</p>",
"logsoftmax": "<p>Now the other half. Computing the probability and <i>then</i> its "
              "log loses precision twice, and once a probability underflows to zero "
              "the log is −inf and there is no gradient. Computing "
              "<code>z − log Σ e^z</code> directly never forms the tiny number at "
              "all. This is exactly what <code>from_logits=True</code> switches on.</p>",
"loss": "<p>Only the true class's log-probability enters the loss. That is the "
        "<code>−log(a_y)</code> formula, written with fancy indexing instead of a "
        "loop.</p>",
"gradient": "<p><code>softmax(z) − onehot(y)</code>, divided by m. Beautifully simple, "
            "and the same shape of answer as the sigmoid case for the same reason: "
            "the messy derivatives cancel. Verified numerically underneath.</p>",
"train": "<p>Three blobs, one linear softmax layer, trained by hand to 99.4%.</p>",
"multilabel": "<p>The distinction that matters in practice, in one comparison. The "
              "same three logits give a softmax that sums to 1 — the classes compete "
              "— or three independent sigmoids that do not. A photo can contain a car "
              "and a bus; softmax structurally cannot say so.</p>",
     }),

dict(file="06_decision_tree.py", slug="06-decision-tree",
     title="A decision tree",
     lede="No gradients, no learning rate, no initialisation. Just counting, "
          "comparing, and recursion — on the exact ten-animal dataset from the "
          "lectures, so every number can be checked against the slides.",
     builds="entropy, information gain, a recursive tree builder, continuous-feature "
            "thresholds, and a live demonstration of overfitting",
     lessons=[("c2/w4-03-measuring-purity.html", "Measuring purity"),
              ("c2/w4-04-information-gain.html", "Information gain"),
              ("c2/w4-05-putting-it-together.html", "Putting it together"),
              ("c2/w4-07-continuous-features.html", "Continuous features")],
     prose={
"data": "<p>The lecture's dataset exactly: ten animals, three binary features, five "
        "cats. Everything below can be checked against the course slides.</p>",
"entropy": "<p>Entropy is “how surprised would a random pick from this node make "
           "you”. Maximum at 50/50, zero when the node is pure. The 0·log 0 case has "
           "to be special-cased because the formula would otherwise be 0 × −∞.</p>",
"gain": "<p>The weighting by branch size is the part people drop. Without it the "
        "tree would adore a pure branch holding one example; with it, that branch "
        "contributes almost nothing to the average.</p>",
"build": "<p>Nine lines of recursion. Stop when the node is pure, when you run out "
         "of depth, when you run out of features, or when no split helps at all. "
         "Those four conditions are the entire difference between a tree that "
         "generalises and one that memorises.</p>",
"predict": "<p>Prediction is a walk from the root to a leaf. Note it reaches 100% "
           "training accuracy — hold that thought until the last block.</p>",
"continuous": "<p>A continuous feature is no harder: sort the values, try every "
              "midpoint between consecutive pairs, keep the best. That is m − 1 "
              "candidates per feature per node, which is why trees are slow to "
              "train and instant to use.</p>",
"overfit": "<p>The point of the file. Generate labels that are <b>pure noise</b> — "
           "there is nothing to learn — and watch training accuracy climb towards "
           "1.0 as depth increases. A tree can always memorise. 100% training "
           "accuracy from a tree is a warning, not a result.</p>",
     }),

dict(file="07_kmeans.py", slug="07-kmeans",
     title="k-means",
     lede="Two functions of about ten lines each. The interesting part is what the "
          "cost function is for — it is not optimised directly, it is how you "
          "choose between runs that disagree.",
     builds="assignment, centroid movement, the cost function, random restarts, and "
            "an elbow plot on data with a known answer",
     lessons=[("c3/w1-03-kmeans-algorithm.html", "The k-means algorithm"),
              ("c3/w1-04-kmeans-cost.html", "The k-means cost function"),
              ("c3/w1-05-initializing-kmeans.html", "Initializing k-means"),
              ("c3/w1-06-choosing-k.html", "Choosing the number of clusters")],
     prose={
"data": "<p>Six points, chosen so you can do the whole algorithm on paper and "
        "compare. These are the same six points as the C3 W1 problem set.</p>",
"assign": "<p>The broadcasting line is worth reading slowly. "
          "<code>X[:, None, :]</code> is (m, 1, n) and <code>centroids[None]</code> "
          "is (1, k, n); together they produce every point-to-centroid difference "
          "at once, shape (m, k, n). One expression, no loops.</p>",
"move": "<p>The empty-cluster case is real and has to be handled — the mean of no "
        "points is 0/0. Here it re-seeds at a random point, which keeps k intact; "
        "the alternative is to drop the centroid and accept k − 1.</p>",
"cost": "<p><code>centroids[idx]</code> is fancy indexing: it builds an array the "
        "same length as X holding each point's own centroid, so the whole cost is "
        "one vectorized expression.</p>",
"fit": "<p>Alternate the two steps until nothing moves. It always terminates, "
       "because both steps can only lower J and there are finitely many "
       "assignments.</p>",
"local_optima": "<p>The demonstration that matters. Same data, same algorithm, two "
                "starting points, two different converged answers — 1.778 and 1.313. "
                "Neither can improve by another step. k-means finds a <b>local</b> "
                "optimum, and J is the only thing that tells you which run was "
                "better.</p>",
"restarts": "<p>So the standard recipe is: run it many times from random starts and "
            "keep the lowest cost. That is what the cost function is <i>for</i> — "
            "it is a referee between runs, not something gradient descent minimises.</p>",
"elbow": "<p>120 points from three real blobs. The drops collapse after k = 3, which "
         "is the right answer. Note J never rises with k: at k = m every point is "
         "its own cluster and J is exactly zero, so you can never choose k by "
         "minimising J.</p>",
     }),

dict(file="08_pca.py", slug="08-pca",
     title="PCA",
     lede="Done twice — once through the covariance matrix and its eigenvectors, "
          "once through the SVD — and shown to agree, because the second is what "
          "every library actually uses.",
     builds="centring, covariance, eigendecomposition, projection and "
            "reconstruction, and PCA recovering a known true dimensionality",
     lessons=[("c3/w2-13-reducing-features-pca.html", "Reducing features with PCA"),
              ("c3/w2-14-pca-algorithm.html", "The PCA algorithm"),
              ("c3/w2-15-pca-in-code.html", "PCA in code"),
              ("f0/w1-17-mean-variance.html", "Mean and variance")],
     prose={
"centre": "<p>PCA is about variance, and variance is measured around the mean. Skip "
          "this and the first component points at the mean rather than along the "
          "spread — a silent error that produces plausible nonsense.</p>",
"covariance": "<p>The diagonal holds each feature's variance; the off-diagonal says "
              "how strongly the features move together. That single matrix is all "
              "PCA ever looks at — note it never sees <code>y</code>.</p>",
"eigen": "<p>The principal components are the eigenvectors of that matrix, and the "
         "eigenvalues are the variance along each one. <code>eigh</code> is the "
         "symmetric-matrix version, and it returns eigenvalues ascending, hence the "
         "reversal.</p>",
"project": "<p>Project down, then reconstruct back up, and measure what was lost. "
           "The reconstruction error comes out equal to the discarded eigenvalue — "
           "which is exactly what an eigenvalue means.</p>",
"svd": "<p>The way libraries really do it. Forming XᵀX squares the condition number "
       "and loses precision; the SVD works on X directly. The components agree up "
       "to a sign, because a direction and its opposite span the same line.</p>",
"perfect": "<p>Perfectly correlated data: the second eigenvalue is exactly zero, "
           "PC1 explains 100% of the variance, and the reconstruction is lossless to "
           "1e-32. The data was always one-dimensional; PCA just noticed.</p>",
"higher_dim": "<p>The realistic case. Fifty features generated from three hidden "
              "ones plus noise — and the cumulative variance jumps to 0.999 at "
              "exactly three components. PCA found the true dimensionality without "
              "being told it.</p>",
     }),

dict(file="09_collaborative_filtering.py", slug="09-collaborative-filtering",
     title="Collaborative filtering",
     lede="Learning the user preferences <i>and</i> the film features at the same "
          "time, from nothing but ratings. Includes the cold-start problem and its "
          "one-line fix.",
     builds="a masked cost function, gradients for both unknowns, mean "
            "normalisation, and a related-items lookup that falls out for free",
     lessons=[("c3/w2-03-collaborative-filtering.html", "Collaborative filtering"),
              ("c3/w2-05-mean-normalization.html", "Mean normalization"),
              ("c3/w2-07-finding-related-items.html", "Finding related items"),
              ("c3/w2-02-per-item-features.html", "Per-item features")],
     prose={
"data": "<p>The lecture's five films and four users. Note the <code>nan</code>s: "
        "most of a real ratings matrix is missing, and the entire algorithm is about "
        "respecting those gaps rather than reading them as zeros.</p>",
"normalise": "<p>Subtract each film's mean over the users who actually rated it. The "
             "reason will be obvious in the cold-start block at the bottom, but "
             "briefly: without it, a user who has rated nothing is predicted to hate "
             "everything.</p>",
"cost": "<p>Multiplying the error by <code>R</code> is the whole trick. It switches "
        "off every unrated cell, so “not rated” and “rated 0” stay different things. "
        "Without it the model would learn from 99% fake zeros.</p>",
"gradient": "<p>Two gradients, because there are two sets of unknowns. "
            "<code>X</code> is not data here — it is a parameter being optimised "
            "alongside <code>W</code>. That is what makes this collaborative rather "
            "than content-based.</p>",
"gradcheck": "<p>Both gradients checked numerically before any training. With two "
             "interacting unknowns this is not optional.</p>",
"train": "<p>Plain gradient descent on all three parameter sets at once.</p>",
"predict": "<p>The film means are added back at the end. Compare the predicted "
           "values with the bracketed real ones — and look at the blanks, which are "
           "the actual product.</p>",
"cold_start": "<p>Eve has rated nothing. Her <code>w</code> converges to exactly "
              "zero, because the only term in the cost that mentions it is the "
              "regularization penalty and nothing pushes back. Without mean "
              "normalisation she would be predicted 0.00 for every film; with it, "
              "she gets each film's average — a far better first guess.</p>",
"related": "<p>Similar films fall out for free, with no user involved: just compare "
           "the learned feature vectors. The three romances cluster and the two "
           "action films cluster, and nobody ever told the model what a genre is.</p>",
     }),

dict(file="10_reinforcement_learning.py", slug="10-reinforcement-learning",
     title="Reinforcement learning",
     lede="Three algorithms on the six-state Mars rover: value iteration, which "
          "knows the rules, and Q-learning, which does not — landing on identical "
          "answers.",
     builds="the discounted return, value iteration, Q-values, a policy, tabular "
            "Q-learning, and a demonstration of why ε-greedy exploration is required",
     lessons=[("c3/w3-03-the-return.html", "The return"),
              ("c3/w3-06-state-action-value-function.html", "The state-action value function"),
              ("c3/w3-08-bellman-equation.html", "The Bellman equation"),
              ("c3/w3-14-epsilon-greedy.html", "Epsilon-greedy policy")],
     prose={
"world": "<p>Six states in a line, 100 at the left end, 40 at the right. Small "
         "enough to solve on paper, which is exactly why the lectures use it.</p>",
"return_by_hand": "<p>The return is the discounted sum of rewards along a path. From "
                  "state 4, going left reaches the 100 in three steps and is worth "
                  "12.5; going right reaches the 40 in two and is worth 10. Left "
                  "wins — but only just, and that margin is the whole story.</p>",
"value_iteration": "<p>Sweep the Bellman equation until nothing changes. This is the "
                   "version that <i>knows the model</i> — it is handed the rewards "
                   "and the transitions. It converges to "
                   "V* = [100, 50, 25, 12.5, 20, 40], exactly the lecture's answer.</p>",
"q_and_policy": "<p>Q(s, a) answers “what if I take this action once, then behave "
                "optimally forever after”. The optimal policy is simply the argmax "
                "over Q, which is why Q is the more useful of the two functions.</p>",
"gamma_sweep": "<p>γ is not a nuisance hyperparameter — it decides what the agent "
               "wants. Sweep it and the rover changes its mind at exactly γ = 0.4, "
               "where 100γ³ = 40γ². Below that it takes the near reward; above it, "
               "the far one.</p>",
"q_learning": "<p>Now take the model away. This agent is never told the rewards or "
              "the transitions — it only ever sees (state, action, reward, next "
              "state) and updates towards the Bellman target. It recovers the same "
              "Q values to three decimal places.</p>",
"exploration": "<p>The last block is the argument for ε-greedy. With ε = 0 the agent "
               "never tries the action that looked worse first, so that action keeps "
               "its initial estimate forever and the policy comes out wrong. Any "
               "exploration at all fixes it.</p>",
     }),
]
