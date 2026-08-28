# -*- coding: utf-8 -*-
"""Review cards — Course 3."""
from cardkit import C, deck, blk, steps, bullets, two, hint

W1 = deck("C3", 1, "Unsupervised Learning", [
    C("c3w1-kmeans-steps", "algorithm",
      "The <b>K-means</b> algorithm — two steps, and what each holds fixed.",
      steps(["<b>assign</b>: c<sup>(i)</sup> := argmin<sub>k</sub> ‖x<sup>(i)</sup> − μ<sub>k</sub>‖² "
             "&nbsp;(centroids fixed)",
             "<b>move</b>: μ<sub>k</sub> := the mean of the points assigned to k &nbsp;(assignments fixed)"])
      + "<p>Repeat until nothing changes.</p>"
      + hint("Neither step can ever <em>increase</em> J. That is the whole proof of convergence — it is "
             "coordinate descent on one cost."),
      "c3/w1-03-kmeans-algorithm.html"),

    C("c3w1-distortion", "formula",
      "The K-means <b>cost</b> (distortion) — and the debugging rule it gives you.",
      blk("<var>J</var> = <span class='fr'><span>1</span><span><var>m</var></span></span> <span class='sum'>Σ</span><sub><var>i</var></sub> "
          "‖ <var>x</var><sup>(<var>i</var>)</sup> − <var>μ</var><sub><var>c</var><sup>(<var>i</var>)</sup></sub> ‖<sup>2</sup>")
      + "<p><b>J can never increase.</b> If your implementation ever shows it rising, you have a bug — "
        "usually updating centroids before finishing the assignments.</p>"
      + hint("Why the mean specifically? Because the mean is the <em>exact</em> minimiser of a sum of "
             "squared distances. Squared distance and “move to the mean” are two halves of one decision."),
      "c3/w1-04-kmeans-cost.html"),

    C("c3w1-init", "algorithm",
      "K-means can land in a <b>local optimum</b>. What is the fix?",
      steps(["initialise centroids at K randomly chosen <b>training points</b> (not random coordinates)",
             "run to convergence",
             "repeat 50–1000 times",
             "keep the run with the <b>lowest J</b>"])
      + hint("You already have the tiebreaker for free — no held-out set, no judgement call. "
             "k-means++ is the smarter seeding everyone actually uses."),
      "c3/w1-05-initializing-kmeans.html"),

    C("c3w1-choose-k", "concept",
      "Why can you not choose <b>K</b> by minimising J, and what do you do instead?",
      "<p>J <b>always</b> falls as K rises. At K = m every point is its own cluster and J = 0.</p>"
      + bullets(["<b>elbow method</b> — plot J vs K, look for the bend. Often ambiguous; Andrew says he "
                 "rarely uses it",
                 "<b>downstream purpose</b> — evaluate K by how well the clusters serve the actual use"])
      + hint("T-shirt sizes: K = 3 (S/M/L) is cheaper to manufacture; K = 5 fits better. That is a "
             "business decision the data cannot make."),
      "c3/w1-06-choosing-k.html"),

    C("c3w1-gaussian", "formula",
      "The <b>Gaussian</b>, and how you fit it to data.",
      blk("<var>p</var>(<var>x</var>) = <span class='fr'><span>1</span><span>√(2π) <var>σ</var></span></span> "
          "<var>e</var><sup>−(<var>x</var>−<var>μ</var>)<sup>2</sup> / 2<var>σ</var><sup>2</sup></sup>")
      + blk("<var>μ</var> = (1/<var>m</var>)<span class='sum'>Σ</span><var>x</var><sup>(<var>i</var>)</sup> &nbsp;·&nbsp; "
            "<var>σ</var><sup>2</sup> = (1/<var>m</var>)<span class='sum'>Σ</span>(<var>x</var><sup>(<var>i</var>)</sup> − <var>μ</var>)<sup>2</sup>", "fitting")
      + hint("p(x) is a <b>density</b>, not a probability — it can exceed 1 when σ is small. Only the "
             "<em>area</em> is a probability, and it totals 1."),
      "c3/w1-08-gaussian-distribution.html"),

    C("c3w1-sigma-ranges", "number",
      "What fraction of a Gaussian lies within μ ± 1σ, ± 2σ, ± 3σ?",
      bullets(["μ ± 1σ → <b>68%</b>", "μ ± 2σ → <b>95%</b>", "μ ± 3σ → <b>99.7%</b>",
               "beyond ± 4σ → 0.006%, about 1 in 15,000"]),
      "c3/w1-08-gaussian-distribution.html"),

    C("c3w1-anomaly", "formula",
      "The <b>anomaly detection</b> model, and why the multiplication is the point.",
      blk("<var>p</var>(<var>x</var>) = <span class='sum'>Π</span><sub><var>j</var>=1</sub><sup><var>n</var></sup> "
          "<var>p</var>(<var>x<sub>j</sub></var>; <var>μ<sub>j</sub></var>, <var>σ<sub>j</sub></var><sup>2</sup>) "
          "&nbsp;→&nbsp; anomaly if <var>p</var>(<var>x</var>) &lt; <var>ε</var>")
      + "<p>Being mildly unusual in one way is common. Being mildly unusual in <b>five ways at once</b> "
        "multiplies into something very rare.</p>"
      + hint("It assumes the features are independent. They usually are not, and it works well anyway. "
             "With many features, use <b>log p = Σ log p<sub>j</sub></b> to avoid underflow."),
      "c3/w1-09-anomaly-detection-algorithm.html"),

    C("c3w1-anomaly-split", "concept",
      "How do you split the data for anomaly detection when you have only ~20 known anomalies?",
      bullets(["<b>train</b>: 6000 normal, <b>0 anomalies</b> — fits μ and σ",
               "<b>cross-validation</b>: 2000 normal + 10 anomalies — chooses ε and the features",
               "<b>test</b>: 2000 normal + 10 anomalies — one honest measurement"])
      + "<p>Training stays unsupervised; evaluation borrows just enough supervision to tune ε.</p>"
      + hint("Put an anomaly in the training set and the model learns it is normal. Report precision, "
             "recall, F1 — never accuracy."),
      "c3/w1-10-developing-anomaly-detection.html"),

    C("c3w1-anomaly-vs-sup", "distinguish",
      "<b>Anomaly detection</b> vs <b>supervised learning</b> — the one deciding question.",
      "<p><b>Do you expect future positive examples to look like the ones you already have?</b></p>"
      + two(bullets(["very few positives (0–20)", "many different anomaly types",
                     "future ones may be unlike past ones", "learns what <b>normal</b> looks like",
                     "fraud, manufacturing faults, intrusions"]),
            bullets(["many positives (100s+)", "enough examples of each type",
                     "future looks like past", "learns what each <b>class</b> looks like",
                     "spam, weather, known defects"]),
            "No → anomaly detection", "Yes → supervised")
      + hint("Fraud is on the anomaly side because fraudsters actively change tactics to evade whatever "
             "you deployed last month."),
      "c3/w1-11-anomaly-vs-supervised.html"),

    C("c3w1-features-anomaly", "concept",
      "Two ideas for choosing features in anomaly detection.",
      steps(["<b>make each feature roughly Gaussian</b> — plot a histogram, apply log(x + c), √x or "
             "x<sup>0.3</sup>, plot again",
             "<b>invent features from your errors</b> — look at the anomaly that slipped through and ask "
             "what would have caught it"])
      + "<p>The classic: a server with normal CPU <b>and</b> normal network traffic, but an unusual "
        "<b>ratio</b>. Add x₃ = CPU / network.</p>"
      + hint("Feature choice matters far more here than in supervised learning, because there is no y to "
             "tell the algorithm which features to ignore."),
      "c3/w1-12-choosing-features.html"),
    C("c3w1-drill-gaussian", "drill",
      "&mu; = 0, &sigma; = 1, x = 0. Compute p(x) — the standard normal density at its own mean.",
      blk("<var>p</var>(0) = 1 / &radic;(2&pi;) &middot; <var>e</var><sup>0</sup> = 1 / 2.507 = <b>0.399</b>")
      + hint("This is the PEAK of the standard bell curve — the highest density it ever reaches, right "
             "at the mean. Move away from &mu; and p(x) only ever gets smaller."),
      "c3/w1-08-gaussian-distribution.html"),
])

W2 = deck("C3", 2, "Recommender Systems", [
    C("c3w2-notation", "concept",
      "In a ratings matrix, what is the difference between <b>r(i,j) = 0</b> and <b>y(i,j) = 0</b>?",
      bullets(["<b>r(i,j) = 0</b> — the user never rated it. <b>No information.</b>",
               "<b>y(i,j) = 0</b> — they rated it zero stars. <b>Strong negative information.</b>"])
      + "<p>Every cost function this week sums <b>only where r(i,j) = 1</b>.</p>"
      + hint("Treating a question mark as a 0 teaches the model that everything unwatched is bad — and "
             "unwatched is 99.99% of the matrix."),
      "c3/w2-01-making-recommendations.html"),

    C("c3w2-collab", "formula",
      "The <b>collaborative filtering</b> cost — and the one thing that makes it collaborative.",
      blk("<var>J</var>(<var>w</var>,<var>b</var>,<b><var>x</var></b>) = ½ <span class='sum'>Σ</span><sub>(<var>i</var>,<var>j</var>):<var>r</var>=1</sub> "
          "(<var>w</var><sup>(<var>j</var>)</sup>·<var>x</var><sup>(<var>i</var>)</sup> + <var>b</var><sup>(<var>j</var>)</sup> − <var>y</var><sup>(<var>i,j</var>)</sup>)<sup>2</sup> "
          "+ <span class='fr'><span><var>λ</var></span><span>2</span></span><span class='sum'>Σ</span><var>w</var><sup>2</sup> "
          "+ <span class='fr'><span><var>λ</var></span><span>2</span></span><span class='sum'>Σ</span><b><var>x</var></b><sup>2</sup>")
      + "<p><b>x is now a parameter too.</b> Gradient descent descends in w, b <em>and</em> x "
        "simultaneously.</p>"
      + hint("The users teach the algorithm what the movies are like, and the movies teach it what the "
             "users are like. Neither was labelled."),
      "c3/w2-03-collaborative-filtering.html"),

    C("c3w2-collab-init", "trap",
      "Why can't you initialise w and x to <b>zero</b> in collaborative filtering?",
      "<p>All the gradients would be symmetric and nothing would ever differentiate. Initialise to "
      "<b>small random values</b> — exactly as with neural networks.</p>"
      + hint("Also: without λ there are infinitely many equivalent solutions (scale w up and x down). "
             "Regularisation is what breaks the tie."),
      "c3/w2-03-collaborative-filtering.html"),

    C("c3w2-meannorm", "concept",
      "A new user has rated nothing. What does the model predict, and what is the fix?",
      "<p>Regularisation drives their w to 0, so every prediction is exactly <b>0.0</b> — we recommend "
      "nothing, or the worst films.</p>"
      + "<p><b>Mean normalisation:</b> subtract each movie's mean rating before training, add it back "
        "when predicting.</p>"
      + blk("prediction = <var>w</var><sup>(<var>j</var>)</sup>·<var>x</var><sup>(<var>i</var>)</sup> + <var>b</var><sup>(<var>j</var>)</sup> + <b><var>μ<sub>i</sub></var></b>")
      + hint("Normalise by <b>row</b> (per movie) — the goal is helping new <em>users</em>. It does not "
             "fix the new-<em>movie</em> problem."),
      "c3/w2-05-mean-normalization.html"),

    C("c3w2-R-mask", "code",
      "In the vectorised collaborative filtering cost, what does <code>* R</code> do?",
      "<pre><code>j = (tf.matmul(X, tf.transpose(W)) + b - Y) * R\nJ = 0.5 * tf.reduce_sum(j ** 2)</code></pre>"
      + "<p>R is the 0/1 matrix. Multiplying by it <b>zeroes every unrated cell before squaring</b>, so "
        "question marks contribute nothing to the cost or the gradient.</p>"
      + hint("One character does the job of the “sum only where r(i,j) = 1” notation."),
      "c3/w2-06-tensorflow-collaborative.html"),

    C("c3w2-related", "formula",
      "How do you find <b>related items</b> from learned features?",
      blk("‖ <var>x</var><sup>(<var>k</var>)</sup> − <var>x</var><sup>(<var>i</var>)</sup> ‖<sup>2</sup> = "
          "<span class='sum'>Σ</span><sub><var>l</var></sub> ( <var>x<sub>l</sub></var><sup>(<var>k</var>)</sup> − <var>x<sub>l</sub></var><sup>(<var>i</var>)</sup> )<sup>2</sup>")
      + "<p>Smallest distance wins. You <b>never need to know what the features mean</b> — the relative "
        "geometry is what carries the information.</p>"
      + hint("At scale, scanning every item is too slow: production uses approximate nearest-neighbour "
             "indexes (FAISS, ScaNN, HNSW). Same technique as vector databases for LLM retrieval."),
      "c3/w2-07-finding-related-items.html"),

    C("c3w2-cf-vs-cbf", "distinguish",
      "<b>Collaborative</b> vs <b>content-based</b> filtering.",
      two(bullets(["uses <b>ratings from similar users</b>", "needs lots of ratings per item",
                   "✗ cold start: new item has no ratings", "✗ cold start: new user is unknown",
                   "✓ finds links nobody described"]),
          bullets(["uses <b>features of the user and item</b>", "needs good descriptions",
                   "✓ new item has features from day one", "✓ new user has age, location, sign-up survey",
                   "✗ limited to what the features encode"]),
          "Collaborative", "Content-based")
      + hint("Real systems use both: content-based to cover cold start, collaborative to catch the "
             "patterns nobody thought to describe."),
      "c3/w2-08-collaborative-vs-content.html"),

    C("c3w2-two-tower", "concept",
      "The <b>two-tower</b> architecture — and the one constraint in the whole design.",
      blk("<var>v<sub>u</sub></var> = UserNN(<var>x<sub>u</sub></var>) &nbsp;·&nbsp; "
          "<var>v<sub>m</sub></var> = ItemNN(<var>x<sub>m</sub></var>) &nbsp;→&nbsp; prediction = <b><var>v<sub>u</sub></var> · <var>v<sub>m</sub></var></b>")
      + "<p>Different inputs, different depths, different widths. The <b>only</b> constraint is that both "
        "output vectors have the <b>same length</b>.</p>"
      + hint("Why the dot product matters: v<sub>m</sub> depends only on the item, so you can precompute "
             "every one overnight. Serving becomes one user-tower pass plus a matrix multiply."),
      "c3/w2-09-deep-content-based.html"),

    C("c3w2-retrieval", "algorithm",
      "How do you recommend from a catalogue of <b>10 million</b> items?",
      steps(["<b>retrieval</b> — cheap rules and nearest-neighbour lookups cut it to ~100 candidates. "
             "Optimised for <b>recall</b>: do not miss anything good",
             "<b>ranking</b> — run the full two-tower network on just those 100. Optimised for "
             "<b>precision</b>: get the order right"])
      + hint("Anything retrieval drops can never be recommended, however good the ranker is. Choose the "
             "candidate count by an offline experiment: raise it until the recommendations stop improving."),
      "c3/w2-10-large-catalogues.html"),

    C("c3w2-ethics", "concept",
      "What makes a recommender different from every other ML system, ethically?",
      "<p>It <b>changes the data it will later be trained on</b>. It shapes the very preferences it "
      "claims to be measuring.</p>"
      + bullets(["optimise engagement → amplifies outrage, because outrage measurably works",
                 "optimise ad revenue → the <b>more exploitative business can bid more</b>, so it gets "
                 "shown more"])
      + hint("The maths is neutral. What you point it at is not. Ask what the system is <em>really</em> "
             "optimising."),
      "c3/w2-11-ethics-recommenders.html"),

    C("c3w2-l2norm", "code",
      "Why does the two-tower model call <code>tf.linalg.l2_normalize</code> before the dot product?",
      "<p>It scales each vector to length 1, turning the dot product into a <b>cosine similarity</b> — "
      "direction only, bounded in [−1, 1].</p>"
      + "<p>Without it the network can lower the loss by <b>inflating magnitudes</b> rather than learning "
        "better directions, and training becomes unstable.</p>"
      + hint("Also: this needs the <b>functional API</b>, not Sequential — two inputs meeting in the "
             "middle."),
      "c3/w2-12-tensorflow-content-based.html"),

    C("c3w2-pca", "algorithm",
      "The <b>PCA</b> algorithm, and what it is optimising.",
      steps(["<b>mean-normalise</b> every feature (and usually scale them)",
             "compute the <b>covariance matrix</b>",
             "its <b>eigenvectors</b> are the principal components; sort by eigenvalue",
             "project: z = x · u"])
      + "<p>It finds the axis along which the projections are <b>most spread out</b> — equivalently, the "
        "one that loses the least when you squash onto it.</p>"
      + hint("<b>Not</b> linear regression: that minimises <em>vertical</em> distance to a label y. PCA "
             "minimises <em>perpendicular</em> distance and has no label at all."),
      "c3/w2-14-pca-algorithm.html"),

    C("c3w2-pca-use", "concept",
      "What is PCA actually <b>for</b>, today?",
      "<p><b>Visualisation.</b> Squash 50 features to 2 so a human can plot them and look.</p>"
      + bullets(["compression — storage is cheap now",
                 "speeding up supervised learning — modern hardware and regularisation handle extra "
                 "features well, and PCA discards directions <b>without ever seeing y</b>"])
      + hint("For 2-D plotting specifically, t-SNE and UMAP usually produce more legible structure. PCA "
             "stays the choice when you need a fast, linear, invertible transform."),
      "c3/w2-15-pca-in-code.html"),
])

W3 = deck("C3", 3, "Reinforcement Learning", [
    C("c3w3-rl-vs-sup", "distinguish",
      "How does reinforcement learning differ from supervised learning?",
      bullets(["you get a <b>reward signal</b>, not the right answer",
               "feedback is <b>a number, often much later</b>",
               "you learn a <b>policy</b> (state → action), not a mapping x → y",
               "<b>the agent generates its own training data by acting</b>"])
      + hint("That last row changes everything: a bad early policy produces bad data, which makes "
             "learning harder. It is the core difficulty of the field."),
      "c3/w3-01-what-is-rl.html"),

    C("c3w3-return", "formula",
      "The <b>discounted return</b>, and what γ encodes.",
      blk("Return = <var>R</var><sub>1</sub> + <var>γR</var><sub>2</sub> + <var>γ</var><sup>2</sup><var>R</var><sub>3</sub> + <var>γ</var><sup>3</sup><var>R</var><sub>4</sub> + …")
      + bullets(["γ near 1 → a <b>patient</b> agent, happy to wait for a bigger payoff",
                 "γ near 0 → an <b>impatient</b> one that grabs whatever is closest",
                 "R₁ is multiplied by γ⁰ = 1 — the exponent counts <b>steps taken</b>"])
      + hint("γ is a choice about how much you care about the future, not a fact about the world. "
             "Real problems use 0.9–0.999; this course uses 0.5 to keep the arithmetic readable."),
      "c3/w3-03-the-return.html"),

    C("c3w3-mdp", "concept",
      "What are the five pieces of an <b>MDP</b>, and what does “Markov” assume?",
      bullets(["<b>S</b> states · <b>A</b> actions · <b>R(s)</b> rewards · <b>γ</b> discount · "
               "<b>π(s)</b> policy"])
      + "<p><b>Markov:</b> the future depends only on <b>where you are now</b>, not on how you got here.</p>"
      + hint("If that is false for your problem, put the missing history <b>into the state</b> — which is "
             "exactly why Atari agents stack four consecutive frames."),
      "c3/w3-05-review-of-key-concepts.html"),

    C("c3w3-q", "concept",
      "Define <b>Q(s, a)</b> precisely — including the odd bit.",
      "<p>The return if you start in s, take action a <b>once</b>, and then <b>behave optimally forever "
      "after</b>.</p>"
      + blk("<var>π</var>*(<var>s</var>) = argmax<sub><var>a</var></sub> <var>Q</var>(<var>s</var>, <var>a</var>) "
            "&nbsp;·&nbsp; <var>V</var>(<var>s</var>) = max<sub><var>a</var></sub> <var>Q</var>(<var>s</var>, <var>a</var>)")
      + hint("The first action can be a silly one; everything after is assumed optimal. That odd shape is "
             "what makes choosing trivial: compare two numbers, take the bigger."),
      "c3/w3-06-state-action-value-function.html"),

    C("c3w3-bellman", "formula",
      "The <b>Bellman equation</b> — and what each half means.",
      blk("<var>Q</var>(<var>s</var>, <var>a</var>) = <b><var>R</var>(<var>s</var>)</b> + "
          "<b><var>γ</var></b> max<sub><var>a</var>′</sub> <var>Q</var>(<var>s</var>′, <var>a</var>′)")
      + bullets(["<b>R(s)</b> — what you get <b>right now</b>",
                 "<b>γ max Q(s′, a′)</b> — the best you can do from wherever you land, discounted"])
      + "<p>At a terminal state there is no “next”, so Q(s, a) = R(s). That is the base case.</p>"
      + hint("Every long journey splits into “this step” plus “the rest”. Every RL algorithm ever written "
             "is built on this."),
      "c3/w3-08-bellman-equation.html"),

    C("c3w3-rover-values", "number",
      "Mars rover, rewards 100 and 40, γ = 0.5. What are V(1)…V(6) and the optimal policy?",
      blk("V = [ <b>100, 50, 25, 12.5, 20, 40</b> ]")
      + "<p>Optimal policy for states 2–5: <b>← ← ← →</b></p>"
      + bullets(["Q(4,←) = 0 + 0.5 × V(3) = 0.5 × 25 = <b>12.5</b>",
                 "Q(4,→) = 0 + 0.5 × V(5) = 0.5 × 20 = <b>10</b> → so state 4 goes left",
                 "Q(5,→) = 0 + 0.5 × 40 = <b>20</b> beats Q(5,←) = 6.25 → state 5 goes right"])
      + hint("The split at states 4/5 is the interesting part — and moving γ moves the dividing line."),
      "c3/w3-06-state-action-value-function.html"),

    C("c3w3-stochastic", "formula",
      "What changes in the Bellman equation for a <b>random</b> environment?",
      blk("<var>Q</var>(<var>s</var>, <var>a</var>) = <var>R</var>(<var>s</var>) + <var>γ</var> "
          "<b>E</b>[ max<sub><var>a</var>′</sub> <var>Q</var>(<var>s</var>′, <var>a</var>′) ]")
      + "<p>One <b>E</b> — an expectation, averaging over every possible next state weighted by its "
        "probability. Nothing else changes.</p>"
      + hint("Every value falls as the misstep probability rises: a world you cannot fully control is "
             "genuinely worth less to be in."),
      "c3/w3-09-stochastic-environments.html"),

    C("c3w3-continuous", "concept",
      "Why can't you store Q in a <b>table</b> for a continuous state space?",
      "<p>Infinitely many states. Discretised, a 6-D state at 100 buckets per dimension is 100⁶ = a "
      "trillion cells — the <b>curse of dimensionality</b>.</p>"
      + "<p>So you <b>compute</b> Q from a vector of numbers instead. That function is a neural network.</p>"
      + hint("A network also <b>generalises</b>: it learns that nearby states have similar Q. A table has "
             "no notion of “nearby”."),
      "c3/w3-10-continuous-state-spaces.html"),

    C("c3w3-dqn", "algorithm",
      "The <b>deep Q-learning</b> (DQN) algorithm.",
      steps(["initialise the network with <b>random</b> weights",
             "act in the environment; store each <b>(s, a, R(s), s′)</b> tuple",
             "keep the 10,000 most recent — the <b>replay buffer</b>",
             "build a training set: <b>x = (s, a)</b>, <b>y = R(s) + γ max<sub>a′</sub> Q(s′, a′)</b>",
             "train Q<sub>new</sub> so Q<sub>new</sub>(x) ≈ y — ordinary supervised learning",
             "set Q = Q<sub>new</sub>, and repeat"])
      + hint("Why it converges rather than spiralling: <b>R(s) is real</b>. Every target contains one "
             "genuine measured reward, and that truth propagates outwards."),
      "c3/w3-12-learning-the-state-value-function.html"),

    C("c3w3-replay", "concept",
      "What two problems does the <b>replay buffer</b> solve?",
      bullets(["<b>correlation</b> — consecutive frames are nearly identical, which violates the i.i.d. "
               "assumption and makes the network oscillate. Random sampling breaks it",
               "<b>data efficiency</b> — each expensive experience is reused many times"])
      + hint("Removing it was tested in the original DQN paper and performance collapses. It is "
             "load-bearing, not an optimisation."),
      "c3/w3-12-learning-the-state-value-function.html"),

    C("c3w3-arch", "concept",
      "What is the <b>improved DQN architecture</b>, and why does it matter?",
      two("input: 8 state + 4 one-hot action = 12<br>output: <b>1</b> number<br>→ <b>4</b> forward passes "
          "per decision",
          "input: <b>8 state only</b><br>output: <b>4</b> numbers, one per action<br>→ <b>1</b> forward pass",
          "✗ naive", "✓ improved")
      + "<p>max<sub>a′</sub> Q(s′, a′) becomes a max over four numbers you already have.</p>"
      + hint("Output activation must be <b>linear</b> — Q values are unbounded reals, not probabilities."),
      "c3/w3-13-improved-architecture.html"),

    C("c3w3-epsilon", "formula",
      "The <b>ε-greedy</b> policy, and why explore at all?",
      blk("with prob 1 − <var>ε</var>: take argmax<sub><var>a</var></sub> <var>Q</var>(<var>s</var>,<var>a</var>) "
          "&nbsp;·&nbsp; with prob <var>ε</var>: pick at <b>random</b>")
      + "<p>A randomly-initialised Q might permanently believe “firing the main engine is bad”. If you "
        "never try it, you never find out otherwise.</p>"
      + hint("Start at ε = 1.0 (all random) and decay towards 0.01. Never to exactly 0 — there may still "
             "be states you have not visited."),
      "c3/w3-14-epsilon-greedy.html"),

    C("c3w3-soft-update", "formula",
      "The <b>soft update</b>, and why DQN needs it when supervised learning does not.",
      blk("<var>W</var> := <var>τ</var> <var>W</var><sub>new</sub> + (1 − <var>τ</var>) <var>W</var><sub>old</sub> "
          "&nbsp;&nbsp; with <var>τ</var> ≈ 0.01")
      + "<p>Because the <b>targets are computed from the network being trained</b>. If Q lurches, every "
        "target lurches, and you are chasing something that keeps jumping.</p>"
      + hint("In supervised learning the targets y are fixed data. Here they are not — which is the whole "
             "reason this refinement exists."),
      "c3/w3-15-minibatch-soft-updates.html"),

    C("c3w3-reward-design", "trap",
      "Why is <b>reward design</b> considered the hard part of applied RL?",
      "<p>The agent maximises precisely what you wrote down, <b>including loopholes you did not "
      "notice</b>. This is called <b>specification gaming</b>.</p>"
      + bullets(["a boat-racing agent rewarded for power-ups span in circles forever, never finishing — "
                 "and outscored humans",
                 "robots rewarded for “distance travelled” learn to fall over in the right direction"])
      + hint("The behaviour you get is a consequence of the reward function, not of your intentions."),
      "c3/w3-07-state-action-value-example.html"),

    C("c3w3-state-of-rl", "concept",
      "Honest assessment: where does RL actually work, and where does it not?",
      two(bullets(["games with perfect simulators", "some control: data-centre cooling, robotics",
                   "<b>RLHF</b> — how every modern chat model is tuned"]),
          bullets(["sim-to-real transfer", "sample efficiency — millions of trials",
                   "extreme sensitivity to reward design and hyperparameters",
                   "far fewer production applications than supervised learning"]),
          "✓ works", "⚠ hard")
      + hint("The hype exceeds the deployed reality — and the ideas still matter, because RLHF is "
             "quietly the biggest deployed application of RL that exists."),
      "c3/w3-16-state-of-rl.html"),
    C("c3w3-drill-return", "drill",
      "&gamma; = 0.5. A reward of 100 arrives 3 steps from now, with 0 reward along the way. Compute the return.",
      blk("Return = <var>R</var>&#8321; + &gamma;<var>R</var>&#8322; + &gamma;&sup2;<var>R</var>&#8323; "
          "= 0 + 0 + (0.5)&sup2;(100)")
      + blk("= 0.25 &times; 100 = <b>25</b>")
      + hint("Each extra step away halves the value again — this is exactly why the Mars rover chooses the "
             "closer, smaller reward once the discount has eaten enough of the far one."),
      "c3/w3-03-the-return.html"),
])

DECKS = [W1, W2, W3]
