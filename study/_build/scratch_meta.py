# -*- coding: utf-8 -*-
"""Narrative for the from-scratch lane. Code comes from scratch/code/*.py."""

import walk_02

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
     },
     walk=walk_02.WALK,
     picture=walk_02.PICTURE),

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

dict(file="11_retrieval.py", slug="11-retrieval",
     title="Retrieval, the R in RAG",
     lede="Counting words, weighting them, cosine, then the SVD \u2014 built until "
          "lexical search fails on a synonym and dense search fails on a rare word, "
          "which is why every real system blends the two.",
     builds="chunking with overlap, a tf-idf index, cosine search, LSA embeddings, "
            "a hybrid ranker measured on three query sets, a prompt assembler with a "
            "token budget, and a threshold for saying nothing",
     primer="""
<p>This file leans on three ideas the three courses do not cover, so here they are, self-contained.</p>
<p><b>An embedding is a learned lookup table.</b> Give every word in your vocabulary a row of, say, 300
numbers. Nothing about those numbers is meaningful at first — they are random. They become meaningful
because they are adjusted, by ordinary gradient descent, until words used in similar contexts end up
with similar rows. That is the whole of it: a matrix with one row per word, trained like any other
parameters you met in C1.</p>
<p><b>The dot product is the similarity.</b> Two rows pointing the same way have a large dot product;
two pointing in unrelated directions have one near zero. Divide by both lengths and you have the
cosine, which is the same measurement with the magnitudes taken out — so a long document and a short
one can be compared on what they are about rather than on how much of it there is. This is the
F0 dot product doing exactly what it always did, on rows that happen to have been learned.</p>
<p><b>Context costs money and attention.</b> Whatever you retrieve has to be pasted into a fixed-size
prompt, and that budget is finite — a few thousand words in a small model. So retrieval is not
"find everything relevant". It is "rank, then fit as much as the budget allows, best first", and
knowing when to return <em>nothing</em> matters as much as ranking well.</p>""",
     lessons=[("f0/w1-10-dot-product.html", "The dot product"),
              ("c2/w1-06-forward-propagation.html", "Forward propagation"),
              ("c3/w2-07-finding-related-items.html", "Finding related items"),
              ("c3/w2-13-reducing-features-pca.html", "Reducing features with PCA")],
     prose={
"corpus": "<p>Fourteen sentences, and two of them are the experiment: some notes say "
          "<i>cost</i> and some say <i>loss</i> for the same idea. Every retrieval "
          "system you will ever build has this problem somewhere in it.</p>",
"chunk": "<p>Before anything can be searched it has to be cut up. Overlap is the "
         "only knob here and it buys exactly one thing \u2014 a fact that straddles a "
         "boundary stays findable. Look at what happens to <i>minimise the cost</i> "
         "at overlap 0: it is in neither chunk, and nothing warns you.</p>",
"vocab": "<p>A document becomes a row of counts. That is the entire representation, "
         "and the 89% of it that is zero is why nobody stores this as a dense array "
         "at real scale.</p>",
"tfidf": "<p>idf is supposed to silence the common words. Read the last four lines "
         "carefully: on this corpus <code>how</code> scores <b>higher</b> than "
         "<code>cost</code>, because it happens to appear in only one note. idf "
         "measures rarity, and in a small collection rarity and meaning come apart.</p>",
"stopwords": "<p>So every real search system ships a stop list. Not because the "
             "designers were lazy about idf \u2014 because of the measurement in the "
             "section directly above. Also note <code>contributions()</code>: a search "
             "you cannot explain is a search you cannot debug.</p>",
"retrieve": "<p>Cosine similarity is a dot product once both sides have length 1, "
            "which is the whole reason the rows were normalised. Each result prints "
            "the words that actually earned the score.</p>",
"mismatch": "<p>The failure. The query says <i>loss</i>; the notes that answer it say "
            "<i>cost</i>; they share no word, so they score exactly 0.000. This is not "
            "a tuning problem. tf-idf has no mechanism that could ever know those two "
            "words mean the same thing.</p>",
"dense": "<p>The SVD from file 08, pointed at a word matrix instead of a feature "
         "matrix. Words that keep the same company end up with similar coordinates, "
         "so a note can now score against a word it does not contain. The cost "
         "documents come back. This is 1990s technology and a modern embedding model "
         "does the same job far better \u2014 but it does <i>this</i> job.</p>",
"compare": "<p>Three query sets, kept apart on purpose. Dense wins on synonyms and "
           "<b>loses</b> on rare exact words, because compressing to six dimensions "
           "is precisely what blurs <code>gaussian</code> into its neighbours. Neither "
           "method dominates, which is the finding, not a disappointment.</p>",
"hybrid": "<p>So add the scores. The blend keeps the exact matches dense blurs and the "
          "synonyms lexical cannot see, for the price of one more dot product. Note "
          "the plateau: a broad range of alpha scores identically here, so anyone "
          "quoting a precise best alpha is quoting their corpus, not yours.</p>",
"assemble": "<p>Retrieval ends in a string. The budget is real \u2014 attention costs "
            "grow with the square of the context \u2014 so something gets dropped, and "
            "the ranker is what chooses. A bad ranker with a big budget just fails "
            "more expensively.</p>",
"abstain": "<p>The most under-built part of most systems. Without a floor the retriever "
           "always returns its top k however irrelevant, and a model handed irrelevant "
           "notes still answers, fluently. A good share of what gets called "
           "hallucination is retrieval that should have said nothing.</p>",
     }),

dict(file="12_fine_tuning.py", slug="12-fine-tuning",
     title="Fine-tuning: head, full, and LoRA",
     lede="Pretrain on 20000 examples, adapt to 60 three different ways, and measure "
          "what each one costs and what each one breaks \u2014 including the forgetting "
          "that freezing the body does not prevent.",
     builds="a pretrained network, a from-scratch baseline, head-only training, full "
            "fine-tuning, LoRA with its own gradients derived by hand, a rank sweep, "
            "and two sweeps that show what actually decides whether transfer works",
     primer="""
<p>One piece of arithmetic makes this whole file make sense: <b>how many numbers are actually in a
model</b>.</p>
<p>A layer that maps <var>d</var> inputs to <var>d</var> outputs holds <var>d</var>² weights. At
<var>d</var> = 768 that is 590,000 numbers — for one layer. Stack a few dozen of those and you are
into the hundreds of millions. Full fine-tuning means computing a gradient for every one of them and
storing an optimiser state alongside, which is where the memory actually goes: roughly four times the
parameter count, before you have loaded a single training example.</p>
<p><b>LoRA's arithmetic is the point of it.</b> Instead of updating the <var>d</var>×<var>d</var>
matrix, you freeze it and learn two thin matrices beside it — <var>d</var>×<var>r</var> and
<var>r</var>×<var>d</var>, with <var>r</var> perhaps 8. That is 2<var>dr</var> numbers instead of
<var>d</var>², which at <var>d</var> = 768 and <var>r</var> = 8 is 12,288 instead of 590,000: about
2% of the parameters, and the frozen matrix is never touched.</p>
<p>Everything else here you already have. Freezing early layers is transfer learning from C2 W3, the
optimiser is Adam from C2 W2, and the reason a small learning rate matters when unfreezing is the
same reason it always did.</p>""",
     lessons=[("c2/w3-13-transfer-learning.html", "Transfer learning"),
              ("c2/w2-11-advanced-optimization.html", "Advanced optimization"),
              ("c1/w3-10-cost-function-with-regularization.html", "Regularization"),
              ("c2/w3-09-bias-variance-neural-networks.html", "Bias and variance in networks")],
     prose={
"tasks": "<p>20000 examples of the task you do not care about, 60 of the task you do. "
         "That ratio is the entire situation and it is why any of this exists.</p>",
"model": "<p>Two ReLU layers and a linear head \u2014 file 03 and file 04 again. The one "
         "addition is the <code>delta</code> hook on W2, which is all LoRA will need.</p>",
"pretrain": "<p>0.90 on task A, and the same model gets 0.65 on task B. Related is "
            "not the same, and that gap is what the rest of the file tries to close.</p>",
"baseline": "<p>The number every fine-tuning result has to beat and the one most often "
            "left out of the comparison. Note the train accuracy: 1.0000. Memorising "
            "60 points is easy; generalising from them is not.</p>",
"head_only": "<p>Read the task A line twice. It got <b>worse</b>, even though the body "
             "never moved \u2014 because the head belongs to task A too, and you just "
             "retrained it on something else. Freezing the body is not the same as "
             "keeping the old behaviour, and almost every explanation of this implies "
             "that it is.</p>",
"full": "<p>The best task B number and a 19-point drop on task A. Nothing "
        "malfunctioned. You asked for the weights that fit 60 examples and you got "
        "them; catastrophic forgetting is that request being granted.</p>",
"lora": "<p>W + BA, with B starting at <b>zero</b> so the adapted model begins "
        "identical to the base \u2014 random B would start you somewhere worse than "
        "where you began. The gradients here are derived by hand from the chain rule "
        "through the product. Then the property no parameter count shows: detach the "
        "adapter and task A comes back at 0.8870, untouched.</p>",
"rank": "<p>The saving at this toy size is unimpressive, and the arithmetic printed "
        "underneath is why it matters on real models: the full matrix grows with d "
        "squared, the adapter only with d. At 4096 wide it is 0.39%. Rank r can only "
        "move the weights in r directions, so if the task needs more, it cannot follow.</p>",
"verdict": "<p>Four methods, two columns, no winner. Pick by what you are short of: "
           "data, compute, memory, or the need to keep the original behaviour.</p>",
"relatedness": "<p>The table that answers <i>will transfer work here</i>. Two different "
               "stories: using the base unchanged collapses from 0.89 to 0.47 as the "
               "task drifts, while fine-tuning holds up and still beats scratch even at "
               "drift 3.0, where the label rule has almost nothing to do with the "
               "original. What transfers is not the answers \u2014 it is the features.</p>",
"data_size": "<p>And the other axis. By 5000 examples every method lands within a point "
             "or two of every other. Fine-tuning pays in the middle band, where you "
             "have enough data to steer a model but not enough to raise one.</p>",
     }),

dict(file="13_agent_loop.py", slug="13-agent-loop",
     title="An agent loop, and how it breaks",
     lede="Tools, schemas, a strict parser, three guard rails and a budget \u2014 with a "
          "deterministic stub where the model goes, so that what is left on the page "
          "is exactly the part you have to get right yourself.",
     builds="a safe arithmetic tool, argument validation, a tool runner that never "
            "raises, an action parser, the think-act-observe loop, a repeat guard, "
            "token accounting, and an evaluation suite with deliberate failures in it",
     primer="""
<p>The model is a stub in this file, deliberately — so it is worth being precise about what the real
thing does, because every guard rail here exists because of one of these three facts.</p>
<p><b>It predicts one token at a time.</b> The model outputs a probability for every token in its
vocabulary, one is picked, it is appended to the input, and the whole thing runs again. Text comes out
left to right, and the model has no plan for the sentence it is part-way through. A temperature dial
controls how sharply the probabilities are peaked before sampling — low is repetitive, high is
erratic.</p>
<p><b>It has no separate store of facts.</b> There is no lookup table of true statements to consult, so
a plausible-sounding wrong answer is produced by exactly the same machinery as a right one, with the
same confidence. This is why the parser here is strict and why the tool runner never trusts the
model's arithmetic.</p>
<p><b>It was trained to be agreeable, not correct.</b> After pre-training, models are tuned on human
preference comparisons — people pick the better of two answers, and the model is optimised for what
gets picked. Helpful and confident is what wins those comparisons, which is precisely why an agent
loop needs a repeat guard, a step budget, and an evaluation suite with deliberate failures in it.</p>""",
     lessons=[("c3/w3-04-policies.html", "Policies"),
              ("c2/w3-11-error-analysis.html", "Error analysis"),
              ("c2/w3-17-precision-recall-tradeoff.html", "Precision and recall")],
     prose={
"tools": "<p>A tool is a name, a declared argument shape, and a function. The declared "
         "shape is not paperwork \u2014 it is the only thing between a wrong guess and a "
         "stack trace in production. Note that <code>calc</code> parses to a syntax "
         "tree and refuses anything not on a list; never hand a string from a model "
         "straight to <code>eval</code>.</p>",
"validate": "<p>Check before running, and return something the caller can act on. "
            "<i>unknown argument radius</i> is repairable. A traceback is not.</p>",
"run_tool": "<p>Every failure comes back as a string. An agent that crashes on a bad "
            "call has one bad step; an agent that is told what went wrong has a chance "
            "to fix it on the next one.</p>",
"parse": "<p>The fragile joint. A real model returns prose with a call somewhere "
         "inside, and the format is a request rather than a guarantee. Three of the "
         "five examples fail, and failing loudly is the correct behaviour \u2014 guessing "
         "at a malformed call is how agents take actions nobody asked for.</p>",
"policy": "<p>The stand-in for the model: deterministic, so this file gives the same "
          "answer twice and needs nothing installed. Look at the <code>\\b</code> "
          "boundaries in the regex. Without them the alternation matches the "
          "<i>m</i> at the start of <i>minute</i> and converts km to metres instead "
          "\u2014 a wrong answer, silently, from a parser that looked fine.</p>",
"loop": "<p>Think, act, observe, repeat. Four tasks, and the third one needs two "
        "tools where the second feeds the first. That is the whole architecture; "
        "everything else on this page is a guard rail.</p>",
"guards": "<p>Three failures, three different guards. The third is the classic runaway "
          "agent \u2014 a planner that keeps choosing the same action, each step costing "
          "a full model call \u2014 stopped after 2 steps instead of 20.</p>",
"budget": "<p>The loop re-sends the whole transcript every step, so cost grows with the "
          "<b>square</b> of the step count, not linearly. This is why <i>let it keep "
          "trying</i> is an expensive default.</p>",
"evaluate": "<p>Two deliberate failures in the suite, because a suite containing only "
            "what you know works measures nothing. Then the ablation: stop feeding "
            "observations back and the score goes to 1 of 12, and the one survivor "
            "<i>succeeds</i> by declining. Both missing tasks are phrasings, not new "
            "capabilities \u2014 which is precisely what a real model buys you, and the "
            "only thing it buys. Every tool, guard and validator above stays as "
            "written.</p>",
     }),

dict(file="14_mlops.py", slug="14-mlops",
     title="After the model works",
     lede="Versioning by hash, training/serving skew, drift that means nothing and "
          "damage that shows on no input monitor, delayed labels, and a canary big "
          "enough to actually decide something.",
     builds="a content-addressed model registry, a demonstration of skew costing real "
            "accuracy, PSI per feature, two cases that break naive drift monitoring, "
            "proxy metrics for the label-lag window, a bootstrap confidence interval "
            "for a canary, and a one-line rollback",
     lessons=[("c2/w3-14-full-cycle.html", "The full cycle"),
              ("c2/w3-10-iterative-loop.html", "The iterative loop"),
              ("c1/w2-05-feature-scaling.html", "Feature scaling"),
              ("c2/w3-16-skewed-datasets.html", "Skewed datasets")],
     prose={
"task": "<p>A loan-approval shape: two features, one decision. Small enough to see "
        "everything that follows.</p>",
"train": "<p><code>standardise</code> returns the statistics as well as the data, "
         "because <b>those statistics are part of the model</b>. They are the most "
         "commonly lost artefact in this entire file.</p>",
"registry": "<p>A version is not a number someone increments. It is a hash of "
            "everything that could change the answer: data, weights, scaler. Retrain "
            "on identical data and the version is identical; nudge one feature by "
            "0.001 and it is not. If a version can stay the same while the data "
            "changed, the version is decoration.</p>",
"skew": "<p>The most expensive bug here and the quietest. Recomputing the scaling "
        "statistics at serving time throws no error, returns sensible-looking "
        "probabilities, passes every shape test \u2014 and costs real accuracy, because "
        "the weights were learned in the training data's units. The only reliable "
        "defence is that one piece of code does the transform for both paths.</p>",
"drift": "<p>PSI, per feature, against a fixed reference. Income moves and years does "
         "not, and the table says which. <i>Something drifted</i> is not actionable; "
         "<i>income drifted</i> is.</p>",
"false_alarm": "<p>The two cases that make naive drift monitoring untrustworthy. In A "
               "the inputs move a long way and accuracy is <b>fine</b>. In B the "
               "inputs are identical, every monitor reads zero, and accuracy collapses "
               "to 0.52 because the rule changed. Drift tells you the world moved. "
               "Only labels tell you the model is wrong.</p>",
"delayed_labels": "<p>And labels are what arrives late. The approval rate holds near "
                  "0.50 across all five weeks while accuracy falls from 0.84 to 0.53. "
                  "Watch what you can see, and be honest about what it misses.</p>",
"canary": "<p>A real 3-point gain, read off five canaries of different sizes. The "
          "40-user row reports <b>+0.1013</b>, more than three times the truth \u2014 not "
          "a small error but a different conclusion, and nothing on that row says so. "
          "The interval is what says so. Work out the traffic you need before you "
          "start, from the smallest gain you would act on.</p>",
"rollback": "<p>Rolling back is changing one string \u2014 but only because both versions "
            "are still loadable and both carry their own scaling statistics. A "
            "rollback plan that requires retraining is not a rollback plan.</p>",
"checklist": "<p>Eight questions, none of them modelling questions. That is the "
             "lesson of the lane's last file: once the model works, almost nothing "
             "that goes wrong afterwards is the model's fault.</p>",
     }),
]
