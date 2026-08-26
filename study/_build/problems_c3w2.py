# -*- coding: utf-8 -*-
"""C3 W2 — recommender systems and PCA."""
from problemkit import P, m, pre, cols

L = []
def add(*a, **k): L.append(P(*a, **k))

add("c3w2-p01", level=1, tag="content-based prediction",
    lesson="c3/w2-02-per-item-features.html",
    ask="A film has features %s (romance, action). Alice's "
        "parameters are %s, %s; Bob's are %s, %s. "
        "Predict each rating and say what the numbers reveal about their taste."
        % (m("x = [0.9, 0.1]"), m("w = [5, 0]"), m("b = 0"), m("w = [0, 5]"), m("b = 0")),
    steps=[("Alice", "5(0.9) + 0(0.1) + 0 = 4.5"),
           ("Bob", "0(0.9) + 5(0.1) + 0 = 0.5"),
           ("Alice's weight vector is all on romance", "she rates by romance alone"),
           ("Bob's is all on action", "he rates by action alone")],
    answer="Alice %s, Bob %s. The weight vector <i>is</i> the taste profile: "
           "whichever feature carries the weight is what that person cares about."
           % (m("4.5"), m("0.5")),
    why="A recommender is just linear regression run once per user, with each user getting "
        "their own w and b but sharing the item features x.")

add("c3w2-p02", level=3, tag="collaborative filtering",
    lesson="c3/w2-03-collaborative-filtering.html",
    ask="In content-based filtering you know %s and learn %s. In collaborative filtering you "
        "know <b>neither</b> and learn both at once. Explain how learning both from ratings "
        "alone is even possible, and what the learned %s means."
        % (m("x"), m("w"), m("x")),
    hint="Think about what constraint a single rating places on the pair (w, x) jointly.",
    steps=[("Each rating gives one equation: w·x + b ≈ y", "one constraint on the product"),
           ("With many users rating many films, you get thousands of such equations",
            "a large system in both unknowns"),
           ("Gradient descent minimises the total squared error over w, b AND x together",
            "differentiate with respect to all of them"),
           ("If two users agree on many films, the fit pushes their w vectors together",
            "and films they both like get similar x"),
           ("The learned x is a set of latent features nobody named",
            "dimension 3 might be “slow-paced” — or nothing describable")],
    answer="Every rating constrains the <i>product</i> %s, and thousands of ratings from "
           "overlapping users pin down both factors up to a rotation. The learned %s is a "
           "vector of <b>latent features</b> — real, useful, and usually not interpretable."
           % (m("w·x"), m("x")),
    why="“Collaborative” means the users do the feature engineering for each other, without "
        "anyone ever describing a film. That is why it works for domains nobody can "
        "characterise by hand.")

add("c3w2-p03", level=3, tag="mean normalization",
    lesson="c3/w2-05-mean-normalization.html",
    ask="A new user Eve has rated nothing. With the standard regularized cost, what will "
        "gradient descent learn for her %s and %s, what will she be predicted to rate "
        "everything, and how does mean normalization fix it?"
        % (m("w"), m("b")),
    hint="If a user has no ratings, which terms of the cost mention their parameters at all?",
    steps=[("The squared-error term sums only over films the user actually rated",
            "for Eve, that sum is empty"),
           ("So the only term mentioning her w is the regularization term (λ/2)‖w‖²",
            "minimised at w = 0"),
           ("Her b has no term at all and stays at its initial 0", "b = 0"),
           ("Prediction: w·x + b = 0 for every film", "she is predicted to hate everything"),
           ("Mean normalization: subtract each film's mean rating before training, and add it "
            "back when predicting", "Eve's prediction becomes 0 + μ_film = the film's average")],
    answer="She learns %s, so every prediction is <b>0</b> — the worst possible rating for "
           "everything. Mean normalization subtracts each film's average rating during "
           "training and adds it back at prediction time, so a new user is predicted the "
           "<b>film's average</b> instead." % m("w = 0, b = 0"),
    why="This is the cold-start problem in its purest form, and the fix is one line of "
        "preprocessing. The average rating is a much better first guess than zero.")

add("c3w2-p04", level=2, tag="mean normalization by hand",
    lesson="c3/w2-05-mean-normalization.html",
    ask="Ratings (blank = not rated). Compute each film's mean over the ratings that exist, "
        "then normalise the first row."
        + cols(["film", "Alice", "Bob", "Carol", "Dave"],
               [["Love at Last", 5, 5, 0, 0],
                ["Romance Forever", 5, "—", "—", 0],
                ["Cute Puppies", "—", 4, 0, "—"],
                ["Swords vs Karate", 0, 0, 5, 4],
                ["Nonstop Chases", 0, 0, 5, "—"]]),
    hint="Divide by how many ratings actually exist for that film, not by 4.",
    steps=[("Love at Last: (5+5+0+0) ÷ 4", "μ = 2.5"),
           ("Romance Forever: (5+0) ÷ 2", "μ = 2.5"),
           ("Cute Puppies: (4+0) ÷ 2", "μ = 2.0"),
           ("Swords vs Karate: (0+0+5+4) ÷ 4", "μ = 2.25"),
           ("Nonstop Chases: (0+0+5) ÷ 3", "μ ≈ 1.667"),
           ("Row 1 normalised: subtract 2.5 from each existing rating",
            "[2.5, 2.5, −2.5, −2.5]")],
    answer="Means %s; row 1 becomes %s."
           % (m("[2.5, 2.5, 2.0, 2.25, 1.667]"), m("[2.5, 2.5, −2.5, −2.5]")),
    why="Note the normalised values are now centred on zero, so “predicting 0” means "
        "“predicting average” instead of “predicting terrible”.")

add("c3w2-p05", level=2, tag="finding related items",
    lesson="c3/w2-07-finding-related-items.html",
    ask="Film A has learned features %s. Three candidates have "
        "%s, %s, %s. Which is most similar to A, using squared "
        "distance %s?"
        % (m("x<sup>(A)</sup> = [0.9, 0.1, 0.5]"), m("[0.8, 0.2, 0.5]"),
           m("[0.1, 0.9, 0.5]"), m("[0.9, 0.1, 0.9]"),
           m("‖x<sup>(k)</sup> − x<sup>(A)</sup>‖²")),
    steps=[("Candidate 1", "(0.1)² + (0.1)² + 0² = 0.01 + 0.01 = 0.02"),
           ("Candidate 2", "(0.8)² + (0.8)² + 0² = 0.64 + 0.64 = 1.28"),
           ("Candidate 3", "0² + 0² + (0.4)² = 0.16"),
           ("Smallest wins", "0.02 < 0.16 < 1.28")],
    answer="<b>Candidate 1</b> (distance %s), then candidate 3 (%s), then candidate 2 (%s)."
           % (m("0.02"), m("0.16"), m("1.28")),
    why="“Related items” needs no user at all — it is pure geometry in the learned feature "
        "space. This is how “because you watched…” rows are built.")

add("c3w2-p06", level=3, tag="binary labels",
    lesson="c3/w2-04-binary-labels.html",
    ask="Netflix has no star ratings, only “did the user finish it”. What two changes convert "
        "the collaborative filtering model to this case? Be specific about the prediction "
        "and the cost.",
    steps=[("Prediction was w·x + b, a number that could be any size",
            "now it must be a probability"),
           ("Change 1: wrap it in a sigmoid", "g(w·x + b)"),
           ("Cost was squared error", "wrong for probabilities — non-convex, and unbounded"),
           ("Change 2: use binary cross-entropy", "−y log(f) − (1−y) log(1−f)"),
           ("Everything else — the joint learning of w, b and x — is unchanged",
            "same algorithm, new head")],
    answer="(1) Wrap the prediction in a <b>sigmoid</b>: %s. "
           "(2) Replace squared error with <b>binary cross-entropy</b>. Nothing else changes."
           % m("f = g(w·x + b)"),
    why="This is exactly the linear → logistic regression change from C1 W3, applied to a "
        "recommender. The same two substitutions appear every time an output becomes a "
        "yes/no.")

add("c3w2-p07", level=2, tag="PCA",
    lesson="c3/w2-14-pca-algorithm.html",
    ask="Data %s. (a) Centre it. (b) Its "
        "covariance matrix is %s — what does the off-diagonal 2 tell you? "
        "(c) The eigenvalues are 4 and 0. What does the zero mean?"
        % (m("[[1,1],[2,2],[3,3],[4,4],[5,5]]"), m("[[2, 2], [2, 2]]")),
    steps=[("(a) Column means are both 3", "centred: [−2,−2], [−1,−1], [0,0], [1,1], [2,2]"),
           ("(b) The off-diagonal is the covariance between the two features",
            "positive and equal to both variances → perfectly correlated"),
           ("(c) Eigenvalues are the variance along each principal direction",
            "4 along one direction, 0 along the other"),
           ("Zero variance in the second direction means every point already lies on a line",
            "the second dimension carries no information"),
           ("So one number per point suffices", "2-D → 1-D with zero loss")],
    answer="(a) %s etc. (b) The two features are perfectly "
           "correlated. (c) The second direction has <b>zero variance</b> — the data already "
           "lies on a line, so it can be reduced to 1-D losing <b>nothing</b>."
           % m("[−2, −2]"),
    why="PCA finds directions of maximum variance. A direction with zero variance is a "
        "dimension the data never actually uses.")

add("c3w2-p08", level=3, tag="PCA variance explained",
    lesson="c3/w2-13-reducing-features-pca.html",
    ask="A second dataset has covariance %s with eigenvalues 3 and 1. "
        "(a) What fraction of the variance does the first principal component explain? "
        "(b) The first component is %s — describe that direction in words. "
        "(c) Would you reduce to 1-D here?"
        % (m("[[2, 1], [1, 2]]"), m("[0.707, 0.707]")),
    steps=[("(a) total variance = 3 + 1 = 4", "3 ÷ 4 = 0.75"),
           ("(b) equal components in both features", "the 45° diagonal, x₁ = x₂"),
           ("(c) dropping to 1-D discards the second component's variance", "loses 25%"),
           ("Whether that is acceptable depends on the use — for visualisation, yes; for a "
            "model that needs the detail, probably not", "a judgement call, not a rule")],
    answer="(a) <b>75%</b>. (b) The <b>45° diagonal</b> — the direction along which both "
           "features rise together. (c) Only if losing 25% of the variance is acceptable; "
           "for a 2-D plot it usually is.",
    why="“Variance explained” is the number to quote when you reduce dimensions. 75% from one "
        "of two components is weak; 95% from 2 of 50 is the case PCA is really for.")

add("c3w2-p09", level=2, tag="what PCA is for",
    lesson="c3/w2-15-pca-in-code.html",
    ask="Andrew Ng says PCA is mostly used for <b>visualisation</b> today, and warns against "
        "two older uses. Name them and say why they fell out of favour.",
    steps=[("Old use 1: compress data to save disk or memory",
            "storage got cheap; the compression rarely pays"),
           ("Old use 2: reduce features to speed up supervised learning",
            "modern optimisers handle many features fine"),
           ("Worse, using PCA to fight overfitting throws away information blindly",
            "regularization does the same job while keeping every feature"),
           ("PCA never looks at y, so it can happily discard the very direction that "
            "predicts your label", "a real failure mode"),
           ("What survives: projecting to 2-D or 3-D so a human can look at the data",
            "still genuinely useful")],
    answer="(1) <b>Compression</b> to save space and (2) <b>speeding up supervised learning</b> "
           "/ fighting overfitting. Both are obsolete: storage and compute are cheap, and "
           "regularization handles overfitting without discarding information. PCA is blind "
           "to y, so it can delete exactly the direction that predicted your label.",
    why="Worth remembering as a general lesson: an unsupervised preprocessing step has no way "
        "of knowing what you were going to predict.")

add("c3w2-p10", level=3, tag="cost function",
    lesson="c3/w2-03-collaborative-filtering.html",
    ask="The collaborative filtering cost sums over %s — only the (i, j) pairs where "
        "user j actually rated film i. What would go wrong if you summed over all pairs and "
        "treated missing ratings as 0?" % m("r(i,j) = 1"),
    steps=[("A missing rating would become a 0 rating", "“not seen” read as “hated it”"),
           ("Most of the matrix is missing — often over 99% of it",
            "so the cost would be dominated by fake zeros"),
           ("The model would learn to predict ≈0 everywhere", "minimising mostly-fake error"),
           ("Genuine ratings would be swamped", "the real signal is a rounding error"),
           ("Hence the r(i,j) indicator, which switches off every unrated pair",
            "the same multiply-by-zero trick as the softmax loss")],
    answer="Missing would be read as <b>hated it</b>. Since the matrix is usually over 99% "
           "empty, the cost would be almost entirely fake zeros and the model would learn to "
           "predict 0 for everything, drowning the genuine ratings.",
    why="%s is doing real work in that formula. It is the difference between "
        "“no data” and “bad rating”, which are not remotely the same thing." % m("r(i,j)"))

add("c3w2-p11", level=2, tag="deep content-based",
    lesson="c3/w2-09-deep-content-based.html",
    ask="A deep content-based recommender puts users through one network and items through "
        "another, then takes the dot product of the two outputs. Why two separate networks "
        "rather than one network taking both at once, and what must be true of the two output "
        "vectors?",
    steps=[("User features and item features are completely different in kind",
            "age and genre have nothing in common"),
           ("Two towers let each learn its own representation", "then meet at the end"),
           ("The outputs must have the SAME length", "or the dot product is undefined"),
           ("Crucially, item vectors can be computed once and stored",
            "they do not depend on the user"),
           ("At serve time you compute one user vector and do fast dot products against "
            "millions of stored item vectors", "this is what makes it scale")],
    answer="Separate towers let each side learn its own representation from very different "
           "raw inputs, and the two outputs must be the <b>same dimension</b> so the dot "
           "product works. The real payoff is that item vectors can be <b>precomputed and "
           "cached</b> — only the user vector is computed at request time.",
    why="This “two-tower” design is the standard architecture for industrial retrieval. The "
        "precomputation is not an optimisation detail; it is the reason the approach is "
        "usable at all.")

add("c3w2-p12", level=3, tag="large catalogues",
    lesson="c3/w2-10-large-catalogues.html",
    ask="You have 10 million items and must respond in 100 milliseconds. Scoring every item "
        "is impossible. Describe the two-stage solution and what each stage optimises for.",
    steps=[("Stage 1 — retrieval: generate a few hundred plausible candidates fast",
            "from cached lists: similar to recent views, top in favourite genres, popular locally"),
           ("This stage optimises for recall and speed", "cheap, approximate, no misses that matter"),
           ("Stage 2 — ranking: run the full model on those few hundred only",
            "expensive but on a tiny set"),
           ("This stage optimises for precision of the ordering", "the quality you actually show"),
           ("Trade-off: retrieving more candidates gives better final results and a slower "
            "response", "tune the number offline against measured quality")],
    answer="<b>Retrieval</b> then <b>ranking</b>. Retrieval cheaply produces a few hundred "
           "candidates from precomputed lists, optimising for speed and not missing good "
           "items. Ranking runs the full model on just those, optimising the order shown. "
           "The number of candidates is the dial between quality and latency.",
    why="Almost every large recommender and search system in production has this shape. It is "
        "the standard answer to “the model is too slow to run on everything”.")

SET = dict(course="C3", week=2, title="Recommenders and PCA",
           lede="Recommenders are the most commercially deployed thing in this "
                "specialization, and the maths turns out to be linear regression with both "
                "sides unknown. PCA closes the week with a different idea entirely: finding "
                "the directions your data actually uses.",
           problems=L)
