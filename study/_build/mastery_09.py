# -*- coding: utf-8 -*-
"""Active Mastery for 09_collaborative_filtering.py.

The anchor is that this file holds the SAME fact in three representations:
Y uses nan for unrated, Yf uses 0.0, and R is the 0/1 mask. Confusing them
is the bug that breaks recommenders, and the file makes all three visible.

Non-duplication: the c3w2 deck already covers r(i,j) vs y(i,j), the cost,
zero-initialisation, mean normalisation, the R mask and related items; the
mock quiz covers what is learned, why mean-normalise, cold start and
similar items. None of that is repeated here.
"""
from masterykit import (section, prose, code, out, semantics, ledger, drill, peek,
                        predict, lab, breaks, invariant, wrong, reconstruct,
                        connections, recall, check)

AM = dict(
    lede="Eleven cards on the file where <b>x is a parameter</b> &mdash; and where the same "
         "fact is stored three different ways, one of which will bite you.",
    sections=[

section("0", "&#129517;", "Before you run", "before", kind="orient",
    hook="Five films, four users, and five holes to fill.",
    body=prose("""<p>A ratings table with <b>15 of 20</b> cells filled. The five holes are the
whole problem &mdash; and the algorithm fills them by learning <b>what the films are like</b>
at the same time as <b>what each user wants</b>, from nothing but the ratings.</p>
<p><b>Watch for:</b> the training cost settling at <b>9.503</b> rather than near zero; both
gradients agreeing with a numerical check to nine decimal places; and the learned film
features placing the romances next to each other without anyone naming a genre.</p>""")
    + connections([], [], "../gist/c32.html", "C3 Week 2 &mdash; the gist",
        extra=[("lab", "../scratch/08-pca.html", "Alongside 08",
                "learned dimensions that mean nothing individually &mdash; same idea, different use")])),

section("1", "&#127991;&#65039;", "What every variable is", "vars", kind="semantics",
    hook="Three variables hold the same fact in three encodings. That is the trap.",
    body=semantics([
        ("Y", "(5, 4) float64", "the ratings, with holes",
         "<b>One row = one film, one column = one user.</b> Unrated cells are <b>nan</b>.",
         "<b>stars, 0&ndash;5</b>",
         "<code>Y[1, 1]</code> is <b>nan</b> &mdash; Bob never rated <i>Romance Forever</i>. "
         "<code>Y[0, 2]</code> is <b>0.0</b> &mdash; Carol watched <i>Love at Last</i> and "
         "gave it nothing.",
         "Those two cells look similar and mean opposite things. nan is <b>no information</b>; "
         "0.0 is <b>strong negative information</b>."),
        ("R", "(5, 4) float64", "the mask",
         "<b>1 where a rating exists, 0 where it does not.</b> Built as "
         "<code>(~np.isnan(Y))</code>, so it is exactly the nan pattern inverted.",
         "<b>0 / 1 flag</b>",
         "<code>R.sum()</code> is <b>15</b> of 20 cells &mdash; 75% dense. A real ratings "
         "matrix is about 99.9% <i>empty</i>.",
         "Every sum in the cost is multiplied by this. Set a cell to 1 that should be 0 and "
         "you train the model to predict a rating nobody gave."),
        ("Yf", "(5, 4) float64", "the nan-free copy",
         "<b>The same table with nan replaced by 0.0</b>, so arithmetic does not propagate "
         "nan through everything.",
         "<b>stars</b>",
         "<code>Yf[1, 1]</code> is <b>0.0</b> &mdash; and so is <code>Yf[0, 2]</code>. The "
         "two cells are now <b>indistinguishable</b>, which is exactly why R has to exist.",
         "This is the single most dangerous variable in the file. It looks like the data and "
         "it has silently destroyed the distinction between &ldquo;unrated&rdquo; and "
         "&ldquo;hated&rdquo;. Only R remembers."),
        ("mu", "(5,) float64", "per-film mean rating",
         "The average rating each film received, <b>over its rated cells only</b>.",
         "<b>stars</b>",
         "<code>mu</code> is [2.5, 2.5, 2.0, 2.25, <b>1.6667</b>]. The last is 5/3 &mdash; "
         "<i>Swords vs Karate</i> has only <b>three</b> ratings, so its mean is over three "
         "cells, not four.",
         "Compute it over all four and every mean drifts towards zero, because the unrated "
         "cell contributes a 0 that was never a rating."),
        ("X", "(5, 3) float64", "the learned film features",
         "<b>Three numbers per film that nobody supplied.</b> This is a <b>parameter</b>, not "
         "data &mdash; the unusual thing about this file.",
         "<i>none &mdash; a learned coordinate</i>",
         "<code>X[0]</code> is three numbers describing <i>Love at Last</i>. None of them "
         "means anything on its own; only the <b>distances</b> between rows do.",
         "The <b>3</b> is a choice (<code>k=3</code>), not a fact about films. More "
         "dimensions can fit better and overfit faster."),
        ("W", "(4, 3) float64", "the learned user tastes",
         "<b>One row per user</b>, in the <b>same three dimensions</b> as X &mdash; which is "
         "what makes the dot product meaningful.",
         "<i>none &mdash; a learned coordinate</i>",
         "<code>W[0] @ X[0]</code> is Alice's predicted score for <i>Love at Last</i>. Both "
         "sides were invented by the same optimisation.",
         "X and W must share k. That is the only structural constraint in the whole model, "
         "and it is the same one the two-tower architecture has."),
        ("b", "(4,) float64", "per-user bias",
         "How generous each user is overall &mdash; one number per <b>user</b>, not per film.",
         "<b>stars</b>",
         "Shape <b>(4,)</b>, so it broadcasts across films. A user who rates everything highly "
         "gets a high b and the features stop having to explain it.",
         "The film-side equivalent is <code>mu</code>, added back at prediction time. Between "
         "them they absorb the &ldquo;overall level&rdquo; so X and W can carry only "
         "<i>differences</i>."),
        ("lam", "float", "the regularisation strength",
         "The fine for large parameters &mdash; on <b>both</b> X and W, which is unusual.",
         "<i>unitless</i>",
         "It is why the training cost settles at <b>9.503</b> rather than approaching zero. "
         "That floor is the penalty, not a failure to converge.",
         "Without it the problem is <b>ill-posed</b>: scale W up by 10 and X down by 10 and "
         "every prediction is identical, so there are infinitely many equally good answers."),
    ],
    """Rows one, two and three are the point. <b>Y, Yf and R hold the same fact in three
encodings</b>, and only R survives the conversion intact. Any bug in this family produces a
model that confidently recommends nothing."""),
    ),

section("2", "&#128302;", "Prediction checkpoints", "predict", kind="predict",
    hook="Four, including one about a cost that stops at nine.",
    body=predict([
        ("""Training goes 44.357 &rarr; 9.505 &rarr; 9.503 and stops. <b>Predict why it does
not approach zero</b>, and say whether that is a problem.""",
         """<p>It is the <b>regularisation floor</b>, and it is not a problem.</p>
<p>The cost is fit error <b>plus</b> &lambda; times the size of X and W. Even a perfect fit
pays the penalty, so the total can never reach zero while &lambda; &gt; 0.</p>
<p>The useful inversion: a collaborative-filtering cost that <b>does</b> reach ~0 has
&lambda; = 0 and is almost certainly overfitting &mdash; it has memorised 15 ratings with
27 free parameters.</p>"""),
        ("""<code>mu</code> is [2.5, 2.5, 2.0, 2.25, 1.6667]. <b>Predict why the last one is
not a round number</b> like the others.""",
         """<p>Because <i>Swords vs Karate</i> has only <b>three</b> ratings, not four. Its
mean is 5/3 = <b>1.6667</b>.</p>
<p>The means are computed over <b>rated cells only</b>. Average over all four and you would be
including a cell that is not a rating &mdash; every mean would drift towards zero, and the
worst-affected films would be the ones with the fewest ratings, which are exactly the ones
that need the most help.</p>"""),
        ("""The gradient check reports <b>dX 5.56e&minus;09</b> and <b>dW 5.11e&minus;09</b>.
Why check <b>two</b> gradients here when files 01 and 02 checked one?""",
         """<p>Because there are <b>two sets of parameters</b>. X is not data in this file
&mdash; it is learned alongside W, so it has its own gradient and its own opportunity to be
wrong.</p>
<p>They are also computed <b>from each other</b>, which makes a sign or index error easy and
its symptom invisible: the cost would still fall, just to a worse answer. Two coupled
gradients is exactly the situation where a numerical check earns its keep.</p>"""),
        ("""The learned features are asked which film is most like which. <b>Predict whether
the romances find each other</b>, given nobody supplied a genre.""",
         """<p>They do. <i>Love at Last</i> &rarr; <i>Romance Forever</i> at distance
<b>0.040</b>; <i>Nonstop Car Chases</i> &rarr; <i>Swords vs Karate</i> at <b>0.024</b>.</p>
<p>Nothing in the data says &ldquo;romance&rdquo;. The only input was <b>who rated what</b>,
and films rated similarly by the same people end up near each other in the learned space.</p>
<p>That is the whole idea behind embeddings, and it is why the individual dimensions being
meaningless does not matter.</p>"""),
    ],
    """The first is the one people misread as a failure to converge.""")),

section("3", "&#128295;", "Modify the copy", "lab", kind="lab",
    hook="Five, ending with the edit that silently destroys the model.",
    body=lab([
        ("L1", "Change a value",
         "Change <code>k</code> from 3 to <b>1</b> &mdash; one learned feature per film "
         "&mdash; and compare the final cost.",
         "X, W, b, hist = fit(Yn, R, k=1)",
         """<p>The cost settles <b>higher</b>. With one dimension the model can only place
films on a single line, so it cannot express &ldquo;likes romance but dislikes slow
films&rdquo; as two separate things.</p>
<p>Then try <code>k=10</code>: the cost falls <b>lower</b> than k=3, and that is not good news
&mdash; with 15 ratings and 90 parameters it is memorising. <b>k is a capacity dial</b>, and
the training cost cannot tell you where to set it.</p>"""),
        ("L2", "Change a parameter",
         "Set <code>lam = 0</code> and watch both the cost and <code>np.abs(X).max()</code>.",
         "X, W, b, hist = fit(Yn, R, lam=0.0)",
         """<p>The cost falls much closer to zero and the parameter magnitudes <b>grow</b>.</p>
<p>Worse, the answer is no longer unique: scale every W up by 10 and every X down by 10 and
<b>every prediction is identical</b>. With &lambda; = 0 there are infinitely many equally
optimal solutions, so what you get depends entirely on where the optimiser stopped.</p>
<p>&lambda; is what makes the problem <b>well-posed</b>, not merely better-behaved.</p>"""),
        ("L3", "Change the data",
         "Add a sixth film that <b>nobody has rated</b> &mdash; a whole row of nan &mdash; "
         "and predict what the model says about it.",
         "Y = np.vstack([Y, [np.nan, np.nan, np.nan, np.nan]])\n"
         "FILMS = FILMS + ['Brand New Release']",
         """<p>Its row of <code>R</code> is all zeros, so it appears in <b>no</b> term of the
fit. Only regularisation touches its features, driving them to <b>0</b>.</p>
<p>And <code>mu</code> for that film is the mean of an <b>empty</b> set &mdash; nan &mdash;
which then propagates into every prediction for it.</p>
<p>This is the <b>item</b> cold start, and it is structural: collaborative filtering knows
items <i>only</i> through ratings, so an item with none is invisible. No amount of training
helps; you need content-based features.</p>"""),
        ("L4", "Change an assumption",
         "Give the model <code>Yf</code> instead of <code>Yn</code> &mdash; the raw table with "
         "nan replaced by 0 &mdash; and keep R as it is.",
         "X, W, b, hist = fit(Yf, R, k=3)      # was Yn, the mean-normalised version",
         """<p>It trains fine and the predictions get <b>worse</b>, especially for users with
few ratings.</p>
<p>Without mean-normalisation the model must explain each film's overall level using the
learned features, which uses up capacity that should be describing <i>differences between
users</i>. A new user still ends up at 0, which on a 0&ndash;5 scale is the worst possible
recommendation.</p>
<p>Nothing errors, and the cost curve looks entirely normal.</p>"""),
        ("L5", "Explain it",
         "Explain why <code>R</code> cannot simply be replaced by <code>Yf != 0</code>.",
         None,
         """<p>Because a genuine rating of <b>zero stars</b> would then be treated as
<i>unrated</i>. <code>Y[0, 2]</code> is a real 0.0 &mdash; Carol watched <i>Love at Last</i>
and hated it &mdash; and that is <b>strong negative information</b> the model needs.</p>
<p><code>Yf != 0</code> would throw it away, and the model would lose exactly the examples
that teach it what Carol dislikes.</p>
<p>This is why R is built from <code>~np.isnan(Y)</code> <b>before</b> the nan are filled.
Once <code>Yf</code> exists the distinction is gone forever, and R is the only record of
it.</p>"""),
    ],
    """L5 is the one to be able to answer without running anything. It is the difference
between a working recommender and one that recommends nothing.""")),

section("4", "&#128165;", "Break it, then repair it", "break", kind="debug",
    hook="Four, and three of them train happily to a wrong answer.",
    body=breaks([
        ("R = (Yf != 0).astype(float)      # was (~np.isnan(Y))",
         "Build the mask from the filled table instead of the nan pattern. Predict which cells "
         "change and what the model then learns.",
         """<p>Two cells flip from 1 to 0 &mdash; the <b>genuine zero ratings</b>, including
Carol's 0.0 for <i>Love at Last</i>.</p>
<p>The model now never sees the examples that teach it what Carol <b>dislikes</b>, so it has
only positive evidence about her and predicts blandly high scores for everything.</p>
<p>The invariant: <b>R must be built from the nan pattern, before the fill.</b> Nothing errors,
the cost falls, and the recommendations are quietly worse for exactly the users who told you
the most.</p>"""),
        ("j = (X @ W.T + b - Yn)            # the * R is gone\nJ = 0.5 * np.sum(j ** 2)",
         "Drop the mask from the cost and re-run. Predict what the model is now being asked "
         "to do.",
         """<p>It now tries to make every <b>unrated</b> cell equal <b>0</b> as well &mdash;
because after mean-normalisation the filled value is 0, and the cost now counts it.</p>
<p>Since 15 of 20 cells are rated and 5 are not, a quarter of the objective is now
&ldquo;predict zero for things nobody watched&rdquo;. The model dutifully learns to predict
low scores everywhere, which is the classic broken recommender.</p>
<p>The invariant: <b>the sum runs over rated cells only</b>, and <code>* R</code> is the
entire mechanism. One character, and it is load-bearing.</p>"""),
        ("mu = np.nanmean(Yf, axis=1)       # Yf has no nan left",
         "Compute the film means from the <b>filled</b> table. Predict which film is worst "
         "affected.",
         """<p><code>np.nanmean</code> on a table with no nan is just <code>mean</code>, so
every unrated cell contributes a <b>0</b> that was never a rating.</p>
<p><i>Swords vs Karate</i> is worst hit: its true mean is 5/3 = <b>1.6667</b> over three
ratings, and this gives <b>1.25</b> over four. The films with the <b>fewest ratings</b> are
distorted most &mdash; and those are exactly the ones relying on their mean for a sensible
cold-start prediction.</p>
<p>The invariant: <b>every average in this file is over rated cells only.</b></p>"""),
        ("P = X @ W.T + b                   # mu is never added back",
         "Predict without restoring the film means. What do the numbers look like?",
         """<p>Every prediction is shifted down by that film's mean, so a good film comes back
as roughly <b>0</b> and a bad one as <b>negative</b> &mdash; on a scale that only runs
0&ndash;5.</p>
<p>The <b>ranking within a film</b> is still correct, so a top-N list per film would look
fine, and the bug hides. It shows up the moment anyone displays a predicted star rating.</p>
<p>The invariant: <b>subtract mu going in, add it back coming out</b> &mdash; the same matched
pair as centring in PCA and the scaling statistics in files 01 and 14.</p>"""),
    ],
    """Three of these four produce a model that trains, converges, and is wrong. That ratio is
the honest one for recommenders.""")),

section("5", "&#9878;&#65039;", "The invariant", "invariant", kind="invariant",
    hook="Both gradients must be checkable, and the mask must match the nan pattern.",
    body=invariant("""<p><b>R must equal the nan pattern of Y exactly, and both gradients must
match a numerical estimate.</b></p>""",
    """<p>The first is cheap and catches the whole family of bugs above:
<code>R.sum()</code> is <b>15</b>, and every cell where R is 0 must be a cell where Y is nan.
Once <code>Yf</code> exists, R is the <b>only</b> record that the distinction ever existed.</p>
<p>The second matters more here than in earlier files because there are <b>two coupled</b>
gradients, each computed from the other's parameters. The file reports <b>dX 5.56e&minus;09</b>
and <b>dW 5.11e&minus;09</b> &mdash; nine decimal places on both.</p>
<p>A wrong gradient in either does not crash. The cost still falls, the training curve looks
healthy, and the recommendations are quietly worse.</p>""",
    """assert np.array_equal(R == 0, np.isnan(Y))
assert R.sum() == np.count_nonzero(~np.isnan(Y))
assert np.max(np.abs(dX - num_grad(X, "X"))) < 1e-6
assert np.max(np.abs(dW - num_grad(W, "W"))) < 1e-6""")),

section("6", "&#129535;", "Wrong mental models", "wrong", kind="myths",
    hook="Five, and the first is why the cost never reaching zero looks like a bug.",
    body=wrong([
        ("The cost stalling at 9.503 means it has not converged.",
         """<p>It has converged. The cost is fit error <b>plus</b> the &lambda; penalty on X
and W, and the penalty never goes away &mdash; so the total has a <b>floor</b> above
zero.</p>
<p>Read it the other way round: a collaborative-filtering cost that <i>does</i> approach zero
has &lambda; = 0, and with 15 ratings and 27 parameters that means memorisation.</p>"""),
        ("The learned features are latent genres.",
         """<p>They are <b>three numbers with no individual meaning</b>. Nobody labelled a
dimension, and no dimension is &ldquo;romance&rdquo;.</p>
<p>What is real is the <b>geometry</b>: <i>Love at Last</i> and <i>Romance Forever</i> sit
0.040 apart, the action films 0.024 apart. The distances carry the information while the
coordinates carry none &mdash; the same property as PCA components in file 08.</p>"""),
        ("Filling nan with 0 is a harmless implementation detail.",
         """<p>It <b>destroys</b> the distinction between &ldquo;never rated&rdquo; and
&ldquo;rated zero stars&rdquo;. <code>Yf[1,1]</code> and <code>Yf[0,2]</code> are both 0.0
and mean opposite things.</p>
<p>It is safe <b>only</b> because R was built from <code>~np.isnan(Y)</code> first. Build R
from <code>Yf != 0</code> instead and you silently discard every genuine zero rating &mdash;
the strongest negative signal you have.</p>"""),
        ("k is a property of the films.",
         """<p><code>k=3</code> is <b>your choice</b>, like the number of clusters in k-means.
There is no true number of dimensions a film has.</p>
<p>Raise it and the training cost falls, always &mdash; more capacity fits better. So the
training cost cannot choose k for you, and with 15 ratings even k=3 is already 27
parameters.</p>"""),
        ("Because it learns x, this is basically unsupervised.",
         """<p>It has labels &mdash; the 15 real ratings &mdash; and the cost is a supervised
squared error over exactly those cells.</p>
<p>What is unusual is that <b>x is a parameter rather than data</b>, which is a statement
about which things get gradients, not about supervision. Compare file 07, which genuinely has
no y at all.</p>"""),
    ])),

section("7", "&#127959;&#65039;", "Reconstruction challenge", "reconstruct", kind="rebuild",
    hook="Rebuild it, and prove the mask is right before anything else.",
    body=reconstruct([
        ("Explain", "In three sentences, say what is being learned and what makes it unusual.",
         """<p>A short list of numbers for every film and a matching list for every user, such
that their dot product reproduces the ratings that exist. Neither list was supplied &mdash;
both are invented by the optimisation. That is what makes it unusual: the <b>features
themselves</b> are parameters, not data.</p>"""),
        ("Skeleton", "Write the five signatures from memory.",
         """<p><code>mean_normalise(Y, R)</code>, <code>cost(X, W, b, Yn, R, lam)</code>,
<code>gradients(X, W, b, Yn, R, lam)</code>,
<code>fit(Yn, R, k=3, lam=1.0, alpha=0.02, iters=3000, seed=1)</code>, and
<code>num_grad(mat, which)</code> for the check.</p>
<p>Note that <code>cost</code> and <code>gradients</code> take <b>both</b> R and Yn &mdash;
the mask is not optional and not derivable from Yn once the nan are gone.</p>"""),
        ("Core", "Write the cost and both gradients, vectorised, with no loop over cells.",
         """<p><code>err = (X @ W.T + b - Yn) * R</code>, then
<code>J = 0.5*np.sum(err**2) + (lam/2)*(np.sum(X**2) + np.sum(W**2))</code>.</p>
<p><code>dX = err @ W + lam*X</code>; <code>dW = err.T @ X + lam*W</code>;
<code>db = err.sum(axis=0)</code>.</p>
<p>The <code>* R</code> must be applied <b>before</b> squaring. Apply it after and the unrated
cells still contribute.</p>"""),
        ("Minimal", "Build the smallest ratings matrix where a user's prediction is entirely "
         "determined by mean normalisation.",
         """<p>Any user who has rated <b>nothing</b>. Their W row appears in no fit term, so
regularisation drives it to 0, and their prediction is <code>0 + b + mu</code> &mdash; which
after normalisation is exactly the film's average.</p>
<p>Two films and two users is enough: leave one user's column entirely nan.</p>"""),
        ("Verify", "Check your rebuild without comparing to the original.",
         """<p>Assert <code>R == 0</code> exactly where <code>Y</code> is nan; assert both
gradients match a numerical estimate to ~1e&minus;6; and assert that a user with no ratings
gets each film's mean back.</p>
<p>That third check is the one that catches a missing mu, a missing mask, and a broken
normalisation all at once.</p>"""),
    ],
    """Do the mask assertion first. Everything downstream is meaningless if R is wrong, and it
is one line.""")),

section("8", "&#128279;", "Connections", "conn", kind="links",
    hook="Learned coordinates, like 08 — and the retrieval problem 11 solves.",
    body=connections(
        [("lab", "../scratch/08-pca.html", "Alongside 08",
          "dimensions that mean nothing individually and everything geometrically"),
         ("lab", "../scratch/01-linear-regression.html", "Back to 01",
          "the same squared error and gradient descent &mdash; with x now learned too")],
        [("lab", "../scratch/11-retrieval.html", "On to 11",
          "finding near neighbours in a learned space, at a scale where scanning is too slow"),
         ("lab", "../scratch/14-mlops.html", "On to 14",
          "and what happens when a recommender's own output becomes next quarter's data")],
        "../gist/c32.html", "C3 Week 2 &mdash; the gist",
        extra=[("docs", "../reference.html", "Reference &mdash; C3 W2",
                "<code>c3w2-notation</code> and <code>c3w2-R-mask</code> carry the "
                "distinction this file makes concrete")])),

section("9", "&#9670;", "Recall sheet", "recall", kind="recall",
    hook="Six cards, all about this file's own numbers and encodings.",
    body=recall([
        ("<code>Y</code>, <code>Yf</code> and <code>R</code> all describe the same table. What "
         "does each encode, and which one survives?",
         "<b>Y</b> marks unrated with <b>nan</b>; <b>Yf</b> replaces nan with <b>0.0</b>; "
         "<b>R</b> is 1 where a rating exists. Only <b>R</b> preserves the distinction once "
         "Yf exists &mdash; in Yf, &ldquo;unrated&rdquo; and &ldquo;zero stars&rdquo; are "
         "identical."),
        ("Why is <code>mu[4] = 1.6667</code> rather than a round number?",
         "<i>Swords vs Karate</i> has only <b>three</b> ratings, so its mean is 5/3. Means are "
         "over <b>rated cells only</b>; averaging over all four would give 1.25 and would "
         "distort the sparsest films most."),
        ("Training stops at cost <b>9.503</b>, not near zero. Bug or expected?",
         "<b>Expected.</b> The cost includes the &lambda; penalty on X and W, which never goes "
         "away, so there is a floor. A cost that <i>does</i> reach zero means &lambda; = 0 and "
         "probable memorisation."),
        ("Why does this file check <b>two</b> gradients when file 01 checks one?",
         "Because <b>X is a parameter too</b>, learned alongside W. They are computed from each "
         "other, so an error in either is easy to make and invisible &mdash; the cost still "
         "falls. Reported at <b>5.56e&minus;09</b> and <b>5.11e&minus;09</b>."),
        ("What is <code>k=3</code>, and can the training cost help you choose it?",
         "The number of learned dimensions per film &mdash; <b>your choice</b>, not a property "
         "of films. The training cost <b>always</b> falls as k rises, so it cannot choose k. "
         "With 15 ratings, k=3 is already 27 parameters."),
        ("You build <code>R</code> as <code>Yf != 0</code>. Which cells are wrong and what "
         "does the model lose?",
         "The <b>genuine zero ratings</b> &mdash; such as Carol's 0.0 for <i>Love at Last</i> "
         "&mdash; get marked unrated. The model loses its <b>strongest negative evidence</b> "
         "and predicts blandly high scores."),
    ],
    """Cover and answer aloud.""")),

section("10", "&#9989;", "Mastery check", "check", kind="check",
    hook="Five, none in the C3 W2 quiz.",
    body=check([
        ("""Point at two cells of <code>Y</code> that look the same in <code>Yf</code> and mean
opposite things. Say what each one tells the model.""",
         """<p><code>Y[1,1]</code> is <b>nan</b> &mdash; Bob never rated <i>Romance Forever</i>,
so it carries <b>no information</b>. <code>Y[0,2]</code> is <b>0.0</b> &mdash; Carol watched
<i>Love at Last</i> and hated it, which is <b>strong negative information</b>.</p>
<p>In <code>Yf</code> both are 0.0. If you cannot name this pair you will eventually build the
recommender that suggests nothing.</p>"""),
        ("""Your recommender predicts low scores for almost everything and you have not changed
the model. Name the two most likely bugs.""",
         """<p>Either the <code>* R</code> is missing from the cost &mdash; so the model is
being trained to predict <b>0 for every unrated cell</b>, which is a quarter of the table
&mdash; or <code>mu</code> was never added back at prediction time, so every score is shifted
down by the film's mean.</p>
<p>Both train cleanly, both produce a normal-looking cost curve, and both are one line.</p>"""),
        ("""A new film is added with no ratings at all. Trace what happens to its features, its
mean, and its predictions.""",
         """<p>Its row of R is all zeros, so it appears in <b>no fit term</b>; only
regularisation touches its features, driving them to <b>0</b>. Its <code>mu</code> is the mean
of an empty set &mdash; <b>nan</b> &mdash; which propagates into every prediction for it.</p>
<p>This is the <b>item</b> cold start and it is structural: collaborative filtering knows items
only through ratings. The fix is not more training, it is content-based features.</p>"""),
        ("""Explain why the training cost cannot tell you whether <code>k=3</code> is the right
number of dimensions.""",
         """<p>Because raising k <b>always</b> lowers the training cost &mdash; more parameters
fit the same 15 ratings better, all the way to memorising them. It is the same shape of
argument as choosing K in k-means by minimising J.</p>
<p>You need held-out ratings, or a downstream measure of whether the recommendations are
actually better.</p>"""),
        ("""Someone proposes dropping <code>lam</code> to zero &ldquo;since we have plenty of
data&rdquo;. Give the argument against that is <b>not</b> about overfitting.""",
         """<p>Without &lambda; the problem is <b>ill-posed</b>: scale every W up by 10 and
every X down by 10 and <b>every prediction is identical</b>. There are infinitely many equally
optimal solutions, so which one you get depends entirely on where the optimiser happened to
stop.</p>
<p>&lambda; picks one. That is a well-posedness argument, and it holds however much data you
have.</p>"""),
    ],
    """None of these appears in the <a href="../quiz/c32.html">C3 W2 mock quiz</a>, which
covers what is learned, why mean-normalise, cold start, two-tower serving and retrieval.""")),
    ],
)
