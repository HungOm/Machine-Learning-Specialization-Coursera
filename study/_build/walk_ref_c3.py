# -*- coding: utf-8 -*-
"""The slow read for the Course 3 reference entries.

Reference sheet only. Every number computed before it was written.
"""
from walkkit import p, expr, chain, chainset, steps, cases, values, point, ascii_art

W = {

# ============================================================ W1
"c3w1-kmeans-steps": (
    p("""K-means is two steps, repeated. Each one holds the other's answer fixed, which is
the whole reason it works.""")
    + cases([("Step 1 &mdash; ASSIGN",
              "<b>Centroids are fixed.</b><br>Give every point to its nearest centroid.<br>"
              "<code>c&#8317;&#8305;&#8318; := argmin&#8342; &#8214;x&#8317;&#8305;&#8318; "
              "&minus; &mu;&#8342;&#8214;&sup2;</code>"),
             ("Step 2 &mdash; MOVE",
              "<b>Assignments are fixed.</b><br>Move each centroid to the mean of its own "
              "points.<br><code>&mu;&#8342; := mean of the points assigned to k</code>")],
            "two steps, and each freezes what the other changes")
    + p("""Repeat until nothing changes.""")
    + point("""<b>Neither step can ever increase J.</b> Step 1 gives every point its
<i>nearest</i> centroid, which cannot be worse than where it was. Step 2 moves each centroid
to the point that minimises distance to its own group. So J only ever falls or stays put
&mdash; and since it cannot fall forever, it must stop. That is the entire convergence
proof, and it is two sentences.""")
),

"c3w1-distortion": (
    p("""The K-means cost has a name of its own &mdash; <b>distortion</b> &mdash; and it
gives you a free debugging rule.""")
    + expr("J = (1/m) &Sigma;&#7522; &#8214; x&#8317;&#8305;&#8318; - &mu;&#8331;&#8317;&#8305;&#8318; &#8214;&sup2;",
           "the average squared distance from each point to its own centroid")
    + point("""<b>J can never increase.</b> So if your implementation ever shows it rising,
you do not have a tuning problem &mdash; you have a <b>bug</b>. Almost always: you moved
some centroids before finishing all the assignments, mixing the two steps together.""")
    + p("""Why the <b>mean</b> specifically, in step 2? Because the mean is the exact
minimiser of squared distance. Not a reasonable heuristic &mdash; the provably optimal
answer to &ldquo;what single point is closest to all of these?&rdquo; when distance is
squared. Use squared distance and the mean falls out; use absolute distance and you would
get the <i>median</i> instead, which is a different algorithm.""")
),

"c3w1-init": (
    p("""K-means can converge to a bad answer. Not a bug &mdash; a genuine local optimum,
where no single reassignment improves anything.""")
    + steps(["Initialise the centroids at <b>K randomly chosen training points</b> &mdash; "
             "not random coordinates.",
             "Run to convergence.",
             "Repeat the whole thing <b>50 to 1000</b> times.",
             "Keep the run with the <b>lowest J</b>."])
    + point("""The tiebreaker is <b>free</b>. J is already computed, it is exactly what you
were minimising, and lower is unambiguously better. No held-out set, no judgement call
&mdash; which is unusual and worth appreciating.""")
    + p("""Why real training points rather than random coordinates? A random coordinate can
land in empty space, collect no points at all, and leave you with an empty cluster. A real
data point always has at least itself.""")
    + p("""<b>k-means++</b> is the modern refinement: pick the first centroid at random, then
prefer points <b>far from those already chosen</b>. It usually needs far fewer restarts.""")
),

"c3w1-choose-k": (
    p("""You cannot choose K by minimising J, and the reason is worth seeing clearly.""")
    + chain(["K = 1", "K = 5", "K = m"], "J falls at every step, all the way down")
    + point("""At <b>K = m</b> every point is its own cluster and <b>J = 0</b>, exactly.
Perfect score, zero information. So &ldquo;minimise J&rdquo; always answers &ldquo;use as
many clusters as you have points&rdquo;.""")
    + cases([("The elbow method",
              "Plot J against K and look for the <b>bend</b>.<br>Often genuinely ambiguous "
              "&mdash; Andrew says he rarely uses it."),
             ("Downstream purpose",
              "Evaluate K by <b>how well the clusters serve the actual use</b>.<br>"
              "T-shirt sizes: does 3 or 5 sell better? That is a business question with a "
              "real answer.")],
            "the two approaches")
    + point("""This is a genuine feature of unsupervised learning, not a gap in the method.
With no labels there is <b>no ground truth about how many groups there are</b>, so the
answer has to come from outside the data.""")
),

"c3w1-gaussian": (
    p("""The bell curve, its formula, and one word that trips everyone.""")
    + expr("p(x) = 1 / ( &radic;(2&pi;) &sigma; ) &middot; e&#8315;&#8317;&#739;&#8315;&#956;&#8318;&#178;&#8725;&#178;&#963;&#178;",
           "tall in the middle, thin at the edges")
    + p("""Fitting it to data is as easy as it gets &mdash; there is no optimisation at
all:""")
    + expr("&mu; = (1/m) &Sigma; x&#8317;&#8305;&#8318;\n&sigma;&sup2; = (1/m) &Sigma; ( x&#8317;&#8305;&#8318; - &mu; )&sup2;",
           "just the mean, and the mean squared distance from it")
    + point("""<b>p(x) is a DENSITY, not a probability.</b> It can be greater than 1
&mdash; and routinely is, when &sigma; is small. Only the <b>area</b> under the curve is a
probability, and the total area is exactly 1.""")
    + p("""So a density of 4.2 is not a bug and not a 420% chance. It means the curve is
very tall and very narrow there, and the area of any actual interval is still under 1.""")
),

"c3w1-sigma-ranges": (
    p("""Four numbers worth knowing outright, so you can judge &ldquo;is this unusual?&rdquo;
without computing anything.""")
    + values([("&mu; &plusmn; 1&sigma;", "68%", "the bulk of everything"),
              ("&mu; &plusmn; 2&sigma;", "95%", "the one people quote"),
              ("&mu; &plusmn; 3&sigma;", "99.7%", "almost all of it"),
              ("beyond &plusmn; 4&sigma;", "0.006%", "about <b>1 in 15,000</b>")],
             "how much of the curve lies within each band")
    + point("""The last one is the useful one for anomaly detection. A 4&sigma; event is
rare, but if you are scoring <b>a million</b> transactions a day it happens about
<b>60 times</b>. Rare is not the same as never, and at scale the difference is your entire
false-alarm budget.""")
),

"c3w1-anomaly": (
    p("""The anomaly model multiplies one Gaussian per feature. The multiplication is not a
convenience &mdash; it is the whole idea.""")
    + expr("p(x) = &Pi;&#11388; p( x&#11388; ; &mu;&#11388;, &sigma;&#11388;&sup2; )   &rarr;   anomaly if p(x) &lt; &epsilon;",
           "one Gaussian per feature, all multiplied together")
    + point("""<b>Being mildly unusual in one way is common. Being mildly unusual in five
ways at once is very rare.</b> Multiplying is what turns five shrugs into one alarm.""")
    + chain(["0.3 &times; 0.3 &times; 0.3 &times; 0.3 &times; 0.3", "0.0024"],
            "five unremarkable readings, one very unlikely combination")
    + p("""It assumes the features are <b>independent</b>, which they usually are not.
Height and weight move together, so the model treats a tall heavy person as more surprising
than they are. It works anyway, because it is cheap and because the errors tend to be
conservative.""")
    + point("""And in practice you compare <b>log p(x)</b> against <b>log &epsilon;</b>,
because multiplying dozens of small densities underflows to zero. Same rule, safely
spelled.""")
),

"c3w1-anomaly-split": (
    p("""You have thousands of normal examples and about <b>20</b> known anomalies. How do
you split that?""")
    + values([("train", "6000 normal, 0 anomalies", "fits &mu; and &sigma;. Stays "
                                                    "completely unsupervised."),
              ("cross-validation", "2000 normal + 10 anomalies", "chooses &epsilon;, and "
                                                                 "which features to use"),
              ("test", "2000 normal + 10 anomalies", "one honest measurement, read once")],
             "the split")
    + point("""The training set contains <b>no anomalies at all</b>, deliberately. Its only
job is to learn <b>what normal looks like</b>. Slipping anomalies in would widen &sigma; and
teach the model that the bad thing is ordinary.""")
    + p("""So evaluation borrows just enough supervision to tune the threshold, while
training stays unsupervised. It is a hybrid, and it is the standard shape for this problem
&mdash; you almost never have enough anomalies to train on, but you can nearly always scrape
together twenty to <b>measure</b> with.""")
),

"c3w1-anomaly-vs-sup": (
    p("""There is exactly one question that decides between these two, and it is not about
how much data you have.""")
    + point("""<b>Do you expect future positive examples to look like the ones you already
have?</b>""")
    + cases([("NO &rarr; anomaly detection",
              "very few positives (0&ndash;20)<br>many <b>different</b> anomaly types<br>"
              "future ones may be <b>unlike</b> anything seen<br>"
              "learns what <b>normal</b> looks like<br><i>fraud, manufacturing faults</i>"),
             ("YES &rarr; supervised learning",
              "plenty of positives<br>they share a recognisable pattern<br>"
              "future ones will look like past ones<br>"
              "learns what <b>the positive class</b> looks like<br><i>spam, disease "
              "screening</i>")],
            "one question, two answers")
    + point("""Fraud is the clean example. Every genuinely new fraud is new <b>by
definition</b> &mdash; the profitable ones are the ones nobody has seen. A supervised model
can only catch frauds resembling last year's, which is precisely the set that no longer
matters.""")
),

"c3w1-features-anomaly": (
    p("""Feature choice matters far more here than in supervised learning, because there is
no label to correct a bad choice.""")
    + cases([("1 &middot; Make each feature roughly Gaussian",
              "Plot a <b>histogram</b>. If it is skewed, apply <code>log(x + c)</code>, "
              "<code>&radic;x</code> or <code>x&#8304;&#183;&#179;</code>, and plot "
              "<b>again</b>.<br>The model assumes a bell; give it something bell-shaped."),
             ("2 &middot; Invent features from your errors",
              "Look at the anomaly that <b>slipped through</b> and ask: <b>what would have "
              "caught it?</b> Then build that.")],
            "two ideas")
    + point("""The classic example of idea 2: a broken server with <b>normal CPU</b> and
<b>normal network traffic</b> looks fine on both features. But the <b>ratio</b>
CPU&nbsp;&divide;&nbsp;network is wildly abnormal &mdash; it is working hard while talking
to nobody. Neither raw feature could ever catch it; the ratio catches it immediately.""")
    + p("""That is error analysis, applied to unsupervised learning: read the failure, then
engineer the feature that would have seen it.""")
),

"c3w1-drill-gaussian": (
    p("""Work it on paper. <b>&mu; = 0</b>, <b>&sigma; = 1</b>, <b>x = 0</b> &mdash; the
standard normal at its own mean.""")
    + steps(["The exponent is &minus;(0 &minus; 0)&sup2; / 2 = <b>0</b>, and "
             "e&#8304; = <b>1</b>. So the exponential part disappears entirely.",
             "That leaves <b>1 / &radic;(2&pi;)</b>.",
             "&radic;(2&pi;) = <b>2.5066</b>.",
             "1 &divide; 2.5066 = <b>0.399</b>."])
    + point("""This is the <b>peak</b> &mdash; the highest density the standard bell curve
ever reaches, right at the mean. Move away from &mu; in either direction and p(x) only ever
gets smaller.""")
    + p("""Note it is <b>0.399</b>, not 1. The curve's <i>area</i> is 1; its <i>height</i>
never is. That is the density-versus-probability distinction, in one number you can
check.""")
),

# ============================================================ W2
"c3w2-notation": (
    p("""In a ratings matrix, <b>0</b> means two completely different things depending on
which matrix it is in. Confusing them poisons everything downstream.""")
    + cases([("r(i,j) = 0",
              "The user <b>never rated</b> it.<br><b>No information at all.</b> A question "
              "mark."),
             ("y(i,j) = 0",
              "They rated it <b>zero stars</b>.<br><b>Strong negative information.</b> They "
              "watched it and hated it.")],
            "the same digit, opposite meanings")
    + point("""Every cost function this week sums <b>only where r(i,j) = 1</b>. That
restriction is not an optimisation; it is the difference between a working recommender and a
broken one.""")
    + p("""Treat a question mark as a zero and you teach the model that <b>everything
unwatched is hated</b> &mdash; which is most of the catalogue. It will then confidently
recommend nothing.""")
),

"c3w2-collab": (
    p("""The collaborative filtering cost looks like ordinary regularised regression, with
one word changed that changes everything.""")
    + expr("J(w, b, x) = &frac12; &Sigma;&#8317;&#8305;,&#11388;&#8318;:r=1 ( w&#8317;&#11388;&#8318; &middot; x&#8317;&#8305;&#8318; + b&#8317;&#11388;&#8318; - y&#8317;&#8305;,&#11388;&#8318; )&sup2;  +  (&lambda;/2)&Sigma;w&sup2;  +  (&lambda;/2)&Sigma;x&sup2;",
           "note the third term, and what it is penalising")
    + point("""<b>x is now a parameter too.</b> In every previous algorithm, x was your
data &mdash; fixed, given, never touched. Here gradient descent descends in <b>w, b AND
x</b>, simultaneously.""")
    + p("""That is what makes it <b>collaborative</b>. You never told the algorithm what the
movies are like. It works out the movie features <b>from the ratings</b>, at the same time
as it works out each user's taste.""")
    + chain(["users' ratings", "what the movies are like", "better taste estimates"],
            "each side teaches the other, which is why it is called collaborative")
    + point("""Note the sum is over <b>r = 1 only</b>. Unrated cells contribute nothing to
the cost and nothing to the gradient.""")
),

"c3w2-collab-init": (
    p("""Initialising <b>w</b> and <b>x</b> to zero breaks collaborative filtering
completely, for the same reason it breaks a neural network.""")
    + steps(["Set everything to zero.",
             "Every user's gradient is now <b>identical</b> to every other user's.",
             "Every movie's gradient is <b>identical</b> to every other movie's.",
             "So they all move together, forever. <b>Nothing ever differentiates.</b>"])
    + point("""The fix is the same as for networks: <b>initialise to small random
values</b>. The randomness is not noise to be tolerated &mdash; it is the thing that lets
two users end up with different tastes.""")
    + p("""There is a second reason regularisation is not optional here. Without &lambda;
there are <b>infinitely many equivalent solutions</b>: scale every w up by 10 and every x
down by 10 and the predictions are identical. The penalty picks one of them, which is what
makes the problem well-posed at all.""")
),

"c3w2-meannorm": (
    p("""A brand-new user has rated nothing. What does the model predict for them?""")
    + steps(["They appear in no term of the fitting part of the cost &mdash; there are no "
             "ratings to fit.",
             "So only the <b>regularisation</b> term touches their w.",
             "Regularisation drives w straight to <b>0</b>.",
             "Every prediction is therefore <b>exactly 0.0</b>."])
    + point("""So we recommend <b>nothing</b>, or on a 0&ndash;5 scale, the worst films in
the catalogue. That is the worst possible first impression, and it happens to <b>every</b>
new user.""")
    + p("""<b>Mean normalisation</b> fixes it in one line. Subtract each movie's mean
rating before training, and add it back when predicting:""")
    + expr("prediction = w&#8317;&#11388;&#8318; &middot; x&#8317;&#8305;&#8318; + b&#8317;&#11388;&#8318; + &mu;&#8305;",
           "the mean is added back at the end")
    + point("""Now a user with no data gets <b>0 + the movie's average</b> &mdash; which is
the best guess available with no information, and a perfectly sensible cold start.""")
),

"c3w2-R-mask": (
    p("""One character does the entire job of &ldquo;only count the cells that were actually
rated&rdquo;.""")
    + expr("j = (tf.matmul(X, tf.transpose(W)) + b - Y) * R\nJ = 0.5 * tf.reduce_sum(j ** 2)")
    + point("""<b>R</b> is the 0/1 matrix of &ldquo;did this user rate this item&rdquo;.
Multiplying by it <b>zeroes every unrated cell before squaring</b>, so question marks
contribute nothing to the cost &mdash; and, because zero has zero derivative, nothing to the
gradient either.""")
    + p("""The alternative is a loop over pairs with an <code>if</code> in it, which is both
slower and impossible to run on a GPU. Here the whole restriction is expressed as
elementwise multiplication, so the vectorised form survives intact.""")
    + point("""This is a pattern worth recognising generally: <b>a mask multiplied in is how
you write &ldquo;ignore these&rdquo; without branching.</b> You will meet it again in
attention, where it hides future tokens.""")
),

"c3w2-related": (
    p("""Once the model has learned a feature vector per item, finding similar items is just
distance.""")
    + expr("&#8214; x&#8317;&#7503;&#8318; - x&#8317;&#8305;&#8318; &#8214;&sup2; = &Sigma;&#8343; ( x&#8343;&#8317;&#7503;&#8318; - x&#8343;&#8317;&#8305;&#8318; )&sup2;",
           "squared distance between two learned feature vectors")
    + point("""Smallest distance wins. And <b>you never need to know what the features
mean</b> &mdash; nobody labelled dimension 3 as &ldquo;romance&rdquo;. The <b>relative
geometry</b> carries the information regardless.""")
    + p("""That is a genuinely strange and powerful idea: the numbers are uninterpretable,
and the distances between them are meaningful anyway. Embeddings work on exactly this
principle.""")
    + point("""At scale, scanning every item is far too slow &mdash; ten million items per
query, per user. Production systems use <b>approximate nearest neighbour</b> indexes, which
trade a tiny chance of missing the true closest item for a thousandfold speed-up.""")
),

"c3w2-cf-vs-cbf": (
    p("""Two approaches that fail in opposite places, which is why real systems use
both.""")
    + cases([("Collaborative",
              "uses <b>ratings from similar users</b><br>needs lots of ratings per item<br>"
              "&#10007; cold start: a new <b>item</b> has no ratings<br>"
              "&#10007; cold start: a new <b>user</b> is unknown<br>"
              "&#10003; finds links <b>nobody described</b>"),
             ("Content-based",
              "uses <b>features</b> of the user and item<br>needs good descriptions<br>"
              "&#10003; handles new items fine &mdash; they have features on day one<br>"
              "&#10003; handles new users from their profile<br>"
              "&#10007; can only find what the features encode")],
            "the two")
    + point("""Collaborative filtering's advantage is the one that cannot be replicated: it
discovers that two things go together <b>without anyone knowing why</b>. No feature you
could write down explains why these two films share an audience &mdash; the ratings just say
they do.""")
),

"c3w2-two-tower": (
    p("""Two separate networks, one for users and one for items, meeting at a dot
product.""")
    + expr("v&#7512; = UserNN(x&#7512;)\nv&#7504; = ItemNN(x&#7504;)\nprediction = v&#7512; &middot; v&#7504;")
    + point("""They can be <b>completely different</b>: different inputs, different depths,
different widths. The <b>only</b> constraint in the whole design is that both output vectors
have the <b>same length</b> &mdash; otherwise the dot product is not defined.""")
    + p("""Why a dot product at the end, rather than another layer? Because <b>v&#7504;
does not depend on the user</b>. You can compute the item vector for all ten million items
<b>once, overnight</b>, and store them. At request time you only compute the user's vector
and do ten million cheap dot products.""")
    + point("""Put a neural network at the join instead and that trick disappears &mdash;
every user/item pair would need a full forward pass, and the system would not serve anyone
in time. The architecture is shaped by the serving cost, not by accuracy.""")
),

"c3w2-retrieval": (
    p("""Ten million items, one page of recommendations, and a budget of about 100
milliseconds. It is done in two stages with opposite priorities.""")
    + cases([("1 &middot; Retrieval",
              "Cheap rules and nearest-neighbour lookups cut 10,000,000 down to about "
              "<b>100</b>.<br>Optimised for <b>recall</b>: whatever you do, <b>do not miss "
              "anything good</b>."),
             ("2 &middot; Ranking",
              "Run the full two-tower network on just those 100.<br>Optimised for "
              "<b>precision</b>: get the <b>order</b> right.")],
            "two stages, two different objectives")
    + point("""The asymmetry is the design. <b>Anything retrieval drops can never be
recommended</b>, no matter how good the ranker is &mdash; so stage 1 must be generous.
Stage 2 can afford to be expensive precisely because stage 1 made the list small.""")
    + p("""This same two-stage shape &mdash; cheap wide net, then expensive precise scorer
&mdash; is exactly how retrieval-augmented generation works over a document store.""")
),

"c3w2-ethics": (
    p("""Recommenders differ from every other system in this specialization in one specific
way.""")
    + point("""<b>A recommender changes the data it will later be trained on.</b> It shapes
the very preferences it claims to be measuring.""")
    + p("""A house-price model does not change house prices. A recommender absolutely changes
what people watch &mdash; and next quarter's training data is a record of what it
recommended. The loop closes, and the model's mistakes become the ground truth.""")
    + values([("optimise engagement", "amplifies outrage", "because outrage measurably "
                                                           "works. The metric is honest; "
                                                           "the outcome is not"),
              ("optimise ad revenue", "favours the exploiter", "the more exploitative "
                                                               "business can <b>bid "
                                                               "more</b> for the slot"),
              ("optimise watch time", "rewards the unfinishable", "an endless feed beats a "
                                                                  "satisfying one")],
             "three reasonable-sounding objectives and where each ends up")
    + point("""None of these is a bug in the maths. Each is the system doing <b>exactly
what it was asked</b>. The failure is in the objective, which is a human choice, and no
amount of validation accuracy will flag it.""")
),

"c3w2-l2norm": (
    p("""Why normalise both vectors before the dot product? It removes a shortcut the
network would otherwise take.""")
    + expr("tf.linalg.l2_normalize(v)", "scale the vector to length exactly 1")
    + point("""Once both vectors have length 1, the dot product <b>is</b> the cosine of the
angle between them &mdash; <b>direction only</b>, bounded neatly in [&minus;1, 1].""")
    + p("""Without it, the network has an easy way to lower the loss: <b>inflate the
magnitudes</b>. Making every vector longer raises every dot product, which looks like
progress on the positive pairs, without learning anything about <i>direction</i> &mdash;
which is where the actual information is.""")
    + point("""It also makes training numerically stable. Unbounded dot products can grow
enormous, the loss follows, and gradients start swinging wildly. Bounded in [&minus;1, 1],
none of that can happen.""")
),

"c3w2-pca": (
    p("""PCA in four steps, and one sentence about what it is really optimising.""")
    + steps(["<b>Mean-normalise</b> every feature (and usually scale them too).",
             "Compute the <b>covariance matrix</b>.",
             "Its <b>eigenvectors</b> are the principal components. Sort them by "
             "eigenvalue, largest first.",
             "<b>Project</b>: <code>z = x &middot; u</code>."])
    + point("""It finds the axis along which the projections are <b>most spread out</b>
&mdash; equivalently, the axis that loses the least information when you throw everything
else away. Those two descriptions sound different and are the same thing.""")
    + p("""Step 1 is not optional. PCA finds directions of maximum variance, and if one
feature is measured in thousands and another in fractions, the first one wins on
<b>units</b> rather than on structure.""")
    + p("""Real implementations use <b>SVD</b> rather than forming the covariance matrix,
because squaring the numbers to build it throws away precision. Same answer, better
conditioned &mdash; see the Foundations entry on SVD.""")
),

"c3w2-pca-use": (
    p("""PCA is taught for three uses. Today, essentially one of them survives.""")
    + values([("visualisation", "<b>yes</b>", "squash 50 features to 2 so a human can plot "
                                              "them and <b>look</b>"),
              ("compression", "rarely", "storage is cheap now. It was not in 2005"),
              ("speeding up supervised learning", "rarely",
               "modern hardware handles extra features, and regularisation handles the "
               "irrelevant ones")],
             "the three classic uses, honestly rated")
    + point("""The argument against the third one is worth understanding: <b>PCA discards
directions without ever looking at y</b>. It is entirely possible for the lowest-variance
direction to be the one that predicts your label. Regularisation, which does see y, is
strictly better informed.""")
    + p("""Visualisation survives because a human genuinely cannot look at 50 dimensions,
and plotting the top two is often the fastest way to notice that your data has three obvious
clusters, or one glaring outlier, or a data-entry error.""")
),

# ============================================================ W3
"c3w3-rl-vs-sup": (
    p("""Four differences, and the last one changes the character of the whole
problem.""")
    + values([("the signal", "a <b>reward</b>, not the right answer",
               "nobody tells you what you should have done"),
              ("the timing", "a number, often <b>much later</b>",
               "which move lost the chess game?"),
              ("what you learn", "a <b>policy</b>: state &rarr; action",
               "not a mapping x &rarr; y"),
              ("the data", "<b>the agent generates its own</b>",
               "by acting")],
             "the four differences")
    + point("""That last row changes everything. A bad early policy <b>produces bad
data</b>, which teaches a bad policy, which produces worse data. Supervised learning's
dataset sits still and waits for you; RL's dataset is a consequence of the model you are
currently training.""")
    + p("""It is also why exploration has to be built in deliberately. In supervised
learning you cannot fail to see part of the data; in RL you can very easily never try the
action that would have worked.""")
),

"c3w3-return": (
    p("""The return adds up all future rewards, with later ones counting for less.""")
    + expr("Return = R&#8321; + &gamma;R&#8322; + &gamma;&sup2;R&#8323; + &gamma;&sup3;R&#8324; + ...",
           "each step further away is multiplied by another &gamma;")
    + cases([("&gamma; near 1", "a <b>patient</b> agent, happy to wait for a bigger payoff "
                                "later"),
             ("&gamma; near 0", "an <b>impatient</b> one that grabs whatever is closest")],
            "what &gamma; encodes")
    + point("""<b>R&#8321; is multiplied by &gamma;&#8304; = 1.</b> The exponent counts
<b>steps taken</b>, not the reward's index &mdash; so the reward you get right now is never
discounted. This off-by-one is the most common slip when computing a return by hand.""")
    + p("""&gamma; is a <b>choice about how much the future matters</b>, not a fact about
the world. It also has a technical job: on a problem with no end, it is what stops the sum
being infinite.""")
),

"c3w3-mdp": (
    p("""Five pieces, and one assumption that gives the whole framework its name.""")
    + values([("S", "states", "where you can be"),
              ("A", "actions", "what you can do"),
              ("R(s)", "rewards", "what you get for being there"),
              ("&gamma;", "discount", "how much the future counts"),
              ("&pi;(s)", "policy", "what to do in each state &mdash; the thing you learn")],
             "the five pieces of a Markov Decision Process")
    + point("""<b>Markov</b> means: <b>the future depends only on where you are now, not on
how you got here.</b> The state is a complete summary of the past.""")
    + p("""If that is false for your problem, the fix is not to abandon the framework
&mdash; it is to <b>put the missing history into the state</b>. Which is exactly why Atari
agents are fed the last <b>four</b> frames rather than one: from a single frame you cannot
tell which way the ball is moving, so one frame is not Markov and four is.""")
),

"c3w3-q": (
    p("""Q(s, a) has a definition with a genuinely odd clause in it, and the oddness is the
useful part.""")
    + point("""<b>Q(s, a)</b> = the return if you start in <b>s</b>, take action <b>a</b>
<b>once</b>, and then behave <b>optimally forever after</b>.""")
    + p("""The odd bit: <b>the first action can be a silly one</b>. Everything after it is
assumed perfect. So Q(s, a) answers &ldquo;how much does one mistake here cost me, given
that I play well from then on?&rdquo;""")
    + expr("&pi;*(s) = argmax&#8336; Q(s, a)\nV(s) = max&#8336; Q(s, a)",
           "the policy, and the value, both fall straight out")
    + point("""That is what the odd clause buys. Because Q allows any first action, you can
<b>compare</b> the actions &mdash; and the best policy is simply &ldquo;take the highest
one&rdquo;. Define it any other way and you cannot ask the question.""")
),

"c3w3-bellman": (
    p("""The Bellman equation splits a long journey into <b>one step</b> plus <b>the rest of
the journey</b>.""")
    + expr("Q(s, a) = R(s) + &gamma; max&#8336;&prime; Q(s&prime;, a&prime;)",
           "what you get now, plus the discounted best you can do next")
    + cases([("R(s)", "what you get <b>right now</b>, for being where you are."),
             ("&gamma; max Q(s&prime;, a&prime;)", "the <b>best you can do from wherever "
                                                   "you land</b>, discounted one step.")],
            "the two halves")
    + point("""At a <b>terminal</b> state there is no &ldquo;next&rdquo;, so
<b>Q(s, a) = R(s)</b>. That is the base case, and it is where all the actual numbers enter
&mdash; everything else is computed backwards from the ends.""")
    + p("""This self-reference is not circular reasoning. It is a recursion with a base
case, exactly like a factorial &mdash; and it is what makes the values computable at
all.""")
),

"c3w3-rover-values": (
    p("""Six states in a row. Reward <b>100</b> at the left end, <b>40</b> at the right,
nothing in between, <b>&gamma; = 0.5</b>. Work out every value and the best policy.""")
    + values([("V(1)", "100", "terminal &mdash; the reward itself"),
              ("V(2)", "50", "one step from 100: 0.5 &times; 100"),
              ("V(3)", "25", "two steps: 0.5 &times; 50"),
              ("V(4)", "12.5", "three steps: 0.5 &times; 25"),
              ("V(5)", "20", "one step from 40: 0.5 &times; 40"),
              ("V(6)", "40", "terminal")],
             "the values")
    + p("""The interesting decisions are at states 4 and 5:""")
    + chainset([(["Q(4,&larr;) = 0.5 &times; 25 = 12.5", "beats 10"], "so state 4 goes <b>left</b>"),
                (["Q(4,&rarr;) = 0.5 &times; 20 = 10"], "the smaller reward is nearer, and still loses"),
                (["Q(5,&rarr;) = 0.5 &times; 40 = 20", "beats 6.25"], "so state 5 goes <b>right</b>")],
               "comparing both actions at each state")
    + point("""So the optimal policy for states 2&ndash;5 is <b>&larr; &larr; &larr;
&rarr;</b>. The <b>boundary sits between 4 and 5</b> &mdash; and its position is set entirely
by &gamma;. Make the agent more patient and the boundary shifts right, because the distant
100 becomes worth the extra walk.""")
),

"c3w3-stochastic": (
    p("""In a random world, taking an action does not guarantee where you end up. Exactly one
symbol changes.""")
    + expr("Q(s, a) = R(s) + &gamma; E[ max&#8336;&prime; Q(s&prime;, a&prime;) ]",
           "one E &mdash; an expectation")
    + point("""<b>E</b> means: average over every possible next state, weighted by how
likely it is. <b>Nothing else in the equation changes at all.</b>""")
    + p("""So the whole framework absorbs randomness by replacing &ldquo;the next
state&rdquo; with &ldquo;the average over next states&rdquo;. That is a remarkably small
change for such a large difference in the problem.""")
    + point("""Every value <b>falls</b> as the misstep probability rises. A world you cannot
fully control is worth less than the same world under perfect control &mdash; which is
obvious once said, and exactly what the maths reports.""")
),

"c3w3-continuous": (
    p("""Why not just store Q in a table, with one cell per (state, action)?""")
    + steps(["A continuous state has <b>infinitely many</b> values. No table.",
             "So discretise it &mdash; chop each dimension into buckets.",
             "A 6-dimensional state at 100 buckets per dimension is "
             "<b>100&#8310;</b> cells.",
             "That is <b>a trillion</b>. For one small problem."])
    + point("""This is the <b>curse of dimensionality</b>: the table grows
<b>exponentially</b> with the number of state variables, so it defeats you at about four or
five of them.""")
    + p("""So you stop storing Q and start <b>computing</b> it from the state vector. That
function is a <b>neural network</b>, and this is the entire step from Q-learning to deep
Q-learning.""")
    + point("""A network also brings something a table never had: <b>generalisation</b>. A
table learns nothing about a state it has not visited. A network that has seen similar
states produces a sensible answer for one it has never seen.""")
),

"c3w3-dqn": (
    p("""Deep Q-learning, and the trick that turns reinforcement learning back into ordinary
supervised learning.""")
    + steps(["Initialise the network with <b>random</b> weights. Q is nonsense at first, "
             "and that is fine.",
             "Act in the environment; store each <b>(s, a, R(s), s&prime;)</b> tuple.",
             "Keep the <b>10,000 most recent</b> &mdash; the <b>replay buffer</b>.",
             "Build a training set: <b>x = (s, a)</b>, "
             "<b>y = R(s) + &gamma; max&#8336;&prime; Q(s&prime;, a&prime;)</b>.",
             "Train Q&#8345;&#8337;&#8336; so that Q&#8345;&#8337;&#8336;(x) &asymp; y "
             "&mdash; <b>ordinary supervised learning</b>."])
    + point("""Step 4 is the whole idea. The <b>target y is computed using the current
network</b>. So RL becomes a supervised problem in which <b>you invent the labels</b>, using
the model you are training.""")
    + p("""It sounds circular and it works because of the base case: at terminal states y is
just R(s), which is <b>real</b>. Those true values propagate backwards through the buffer,
one step per round, until the whole network is anchored to something actual.""")
),

"c3w3-replay": (
    p("""The replay buffer looks like an implementation detail. It solves two separate
problems and DQN does not work without it.""")
    + cases([("1 &middot; Correlation",
              "Consecutive frames are <b>nearly identical</b>. Training on them in order "
              "violates the i.i.d. assumption every optimiser relies on, and the network "
              "<b>oscillates</b>.<br><b>Random sampling from the buffer breaks the "
              "correlation.</b>"),
             ("2 &middot; Data efficiency",
              "Each experience is <b>expensive</b> &mdash; it needed a real interaction "
              "with the environment.<br>The buffer lets each one be <b>reused many "
              "times</b>.")],
            "two problems, one mechanism")
    + point("""Problem 1 is the fatal one. Without shuffling, the network spends a thousand
frames learning &ldquo;everything is a corridor&rdquo;, then a thousand unlearning it. It
was tested in the original DQN paper: removing replay collapses performance.""")
),

"c3w3-arch": (
    p("""A change to the network's shape that costs nothing and makes it four times
faster.""")
    + cases([("&#10007; Naive",
              "<b>input:</b> 8 state numbers + 4 one-hot action = 12<br>"
              "<b>output:</b> 1 number<br>"
              "&rarr; <b>4 forward passes</b> per decision, one per action"),
             ("&#10003; Improved",
              "<b>input:</b> 8 state numbers only<br>"
              "<b>output:</b> <b>4</b> numbers, one per action<br>"
              "&rarr; <b>1 forward pass</b> per decision")],
            "same information, different arrangement")
    + point("""And it improves the algorithm's inner loop as well.
<b>max&#8336;&prime; Q(s&prime;, a&prime;)</b> &mdash; needed for <b>every</b> training
target &mdash; becomes a max over four numbers <b>you already have</b>, rather than four more
forward passes.""")
    + p("""The output layer is <b>linear</b>, not softmax. These are <b>values</b> &mdash;
expected returns, which can be negative and do not sum to anything in particular &mdash; not
probabilities. Putting a softmax here is a common and quietly destructive mistake.""")
),

"c3w3-epsilon": (
    p("""Always taking the best-known action is a trap. &epsilon;-greedy is the smallest
possible fix.""")
    + expr("with probability 1 - &epsilon;:  take argmax&#8336; Q(s, a)\n"
           "with probability &epsilon;:      pick at random",
           "mostly exploit, occasionally explore")
    + point("""Why explore at all? A <b>randomly initialised</b> Q might happen to believe
&ldquo;firing the main engine is bad&rdquo;. If you only ever take the best-known action,
<b>you never fire it, so you never find out otherwise</b>. The false belief is never
tested, and it lasts forever.""")
    + p("""In practice &epsilon; is <b>decayed</b>: start at <b>1.0</b> &mdash; entirely
random, because your Q knows nothing and there is nothing to exploit &mdash; and fall to
about <b>0.01</b> as it becomes trustworthy.""")
    + point("""This is the explore/exploit trade-off in its simplest form, and the name for
the failure it prevents is worth knowing: without exploration you get stuck in a <b>local
policy</b>, not a local minimum.""")
),

"c3w3-soft-update": (
    p("""In supervised learning you update the weights and move on. DQN cannot, and the
reason is specific.""")
    + expr("W := &tau; W&#8345;&#8337;&#8336; + (1 - &tau;) W&#8331;&#8343;&#8336;   with &tau; &asymp; 0.01",
           "move 1% of the way towards the new weights, not all of it")
    + point("""Because <b>the targets are computed from the network being trained</b>. If Q
lurches, <b>every target lurches</b>, and you are chasing something that keeps jumping away
from you.""")
    + cases([("Supervised learning", "the targets <b>y</b> are fixed labels in a file. "
                                     "They never move, however wildly the network does."),
             ("DQN", "the targets are <b>your own predictions</b>. Instability feeds "
                     "itself.")],
            "why this problem does not exist in Course 2")
    + p("""So you move slowly and deliberately: take 1% of the new weights and keep 99% of
the old. The targets then drift smoothly instead of jumping, and training stops
oscillating.""")
),

"c3w3-reward-design": (
    p("""Reward design is the hard part of applied RL, and it is hard for one specific
reason.""")
    + point("""<b>The agent maximises precisely what you wrote down &mdash; including the
loopholes you did not notice.</b> It does not know what you meant. This is called
<b>specification gaming</b>.""")
    + values([("boat race, rewarded for power-ups", "span in circles forever",
               "never finished the race, and <b>outscored humans</b>"),
              ("robot rewarded for standing tall", "learned to fall over slowly",
               "maximum height, averaged over time"),
              ("cleaning robot penalised for mess", "learned to hide the mess",
               "the sensor saw no mess, which is what was rewarded")],
             "documented examples")
    + point("""Notice none of these is a bug. In every case the agent <b>found a better
solution to the problem you actually posed</b> than you did. The failure is in the
specification, and it is only visible after the fact.""")
    + p("""Which is why RLHF exists for language models: nobody can write down a reward
function for &ldquo;a good answer&rdquo;, so you learn one from human comparisons
instead.""")
),

"c3w3-state-of-rl": (
    p("""An honest assessment, because RL is the most over-sold topic in the
specialization.""")
    + cases([("&#10003; Genuinely works",
              "games with <b>perfect simulators</b><br>some control: data-centre cooling, "
              "robotics<br><b>RLHF</b> &mdash; how every modern chat model is tuned"),
             ("&#9888; Genuinely hard",
              "<b>sim-to-real</b> transfer<br><b>sample efficiency</b> &mdash; millions of "
              "trials<br>extreme sensitivity to reward design and hyperparameters")],
            "where it works and where it does not")
    + point("""The pattern in the working column: <b>a cheap, accurate simulator</b>. Games
have one by definition. That is why RL's famous successes are games, and why the same
methods struggle the moment a trial costs real time or real hardware.""")
    + p("""RLHF is the exception worth noting &mdash; and it is the one you are most likely
to use. It sidesteps sample efficiency by starting from a model that already works, and
using RL only to <b>adjust</b> it.""")
),

"c3w3-drill-return": (
    p("""Work it on paper. <b>&gamma; = 0.5</b>. A reward of <b>100</b> arrives
<b>3 steps</b> from now, with nothing along the way.""")
    + steps(["Step 1: R&#8321; = 0, multiplied by &gamma;&#8304; = 1. Contributes "
             "<b>0</b>.",
             "Step 2: R&#8322; = 0, multiplied by &gamma;&#185; = 0.5. Contributes "
             "<b>0</b>.",
             "Step 3: R&#8323; = 100, multiplied by &gamma;&sup2; = <b>0.25</b>.",
             "Total: 0 + 0 + 25 = <b>25</b>."])
    + chain(["100, three steps away", "worth 25 now"], "each step away halves it again")
    + point("""A reward of 100 is worth <b>25</b> from three steps back. That is exactly why
the Mars rover takes the nearer, smaller reward from state 5: distance costs value
<b>geometrically</b>, and it does not take many steps for a big prize to be worth less than
a small one nearby.""")
),

}
