# -*- coding: utf-8 -*-
"""Walkthrough for 09_collaborative_filtering.py."""
from walkkit import p, expr, chain, chainset, steps, cases, values, point, ascii_art

PICTURE = ([
    ("in", "A ratings table, mostly empty",
     "5 films, 4 users, and only <b>15 of the 20</b> cells filled in. The gaps are the "
     "whole problem."),
    ("arw", "subtract each film's mean rating"),
    ("op", "Guess BOTH sides at once",
     "Invent a feature vector <b>x</b> for every film and a taste vector <b>w</b> for "
     "every user. Both start as small random numbers."),
    ("arw", "predict only the cells that were actually rated"),
    ("loop", "repeat until the cost stops falling", [
        ("op", "Score the guesses", "Squared error on the rated cells only, plus a penalty "
                                    "on both w and x."),
        ("arw", "one gradient for w, one for x"),
        ("back", "Move BOTH", "This is the unusual part: <b>x is a parameter too</b>."),
    ]),
    ("arw", "add each film's mean back on"),
    ("out", "Every empty cell, filled in", "And, for free, which films are similar."),
], "The whole program in one picture",
   "Every other file in this lane treats x as fixed data. Here the algorithm invents the "
   "features as it goes, which is what 'collaborative' means.")

WALK = {

"prelude": (
    p("""In every previous file, <b>x was your data</b> &mdash; fixed, given, never touched.
Here it is a <b>parameter</b>. The algorithm works out what the films are like at the same
time as it works out what each user wants.""")
    + point("""That is what <b>collaborative</b> means: the users teach the algorithm what
the films are, and the films teach it what the users like. Neither was described to it.""")
),

"data": (
    p("""Five films, four users, and a table with holes in it.""")
    + values([("cells", "20", "5 films &times; 4 users"),
              ("rated", "15", "75% dense"),
              ("empty", "5", "the cells you are trying to predict")],
             "the ratings matrix")
    + point("""A real ratings matrix is <b>99.9% empty</b>, not 25%. This one is dense enough
to print and check by hand, which is the only reason it looks manageable.""")
    + p("""The critical distinction: an empty cell means <b>&ldquo;not rated&rdquo;</b>, not
&ldquo;rated zero&rdquo;. Treat a question mark as a 0 and you teach the model that everything
unwatched is hated &mdash; which is most of the catalogue.""")
),

"normalise": (
    p("""Subtract each film's own mean rating before training.""")
    + values([("Love at Last", "2.500", ""),
              ("Romance Forever", "2.500", ""),
              ("Cute Puppies of Love", "2.000", ""),
              ("Nonstop Car Chases", "2.250", ""),
              ("Swords vs Karate", "1.667", "averaged over its rated cells only")],
             "per-film mean rating")
    + point("""This is the <b>cold start</b> fix. A brand-new user appears in no fitting term
&mdash; they have rated nothing &mdash; so only regularisation touches their <b>w</b>, which
drives it to <b>0</b>, and every prediction becomes exactly 0.""")
    + p("""With mean normalisation, that user gets <b>0 + the film's average</b> instead
&mdash; which is the best available guess with no information, and a perfectly sensible
first impression.""")
    + point("""Note the means are computed over <b>rated cells only</b>. Including the empty
ones would drag every average towards zero, which is the same bug in a different
place.""")
),

"cost": (
    p("""The cost has three parts, and the third one is the tell.""")
    + expr("J = &frac12; &Sigma;&#8331;&#8336;&#8348;&#8337;&#8340; (w&middot;x + b - y)&sup2;  +  (&lambda;/2)&Sigma;w&sup2;  +  (&lambda;/2)&Sigma;x&sup2;",
           "fit the rated cells, and keep BOTH sets of parameters small")
    + point("""The <b>&Sigma;x&sup2;</b> term is the giveaway that <b>x is being learned</b>.
You do not regularise your data.""")
    + p("""And the fitting sum runs over <b>rated cells only</b>. In the vectorised code that
restriction is a single multiplication by <b>R</b>, the 0/1 mask &mdash; which zeroes every
unrated cell <b>before squaring</b>, so it contributes nothing to the cost and, having zero
derivative, nothing to the gradient either.""")
    + point("""Regularisation is not optional here for a second reason. Without &lambda;
there are <b>infinitely many equivalent solutions</b>: scale every w up by 10 and every x
down by 10 and every prediction is identical. The penalty picks one.""")
),

"gradient": (
    p("""Two gradients instead of one, because there are two sets of parameters to
move.""")
    + cases([("dJ/dW", "how each user's taste should change, given the current guess at "
                       "what the films are"),
             ("dJ/dX", "how each film's features should change, given the current guess at "
                       "what the users like")],
            "and they are computed from each other")
    + point("""They are updated <b>simultaneously</b>, from the same old values &mdash; the
same rule as w and b in Course 1, for the same reason. Update X first and the W gradient is
computed against films that no longer exist.""")
),

"gradcheck": (
    p("""Both gradients, checked against a numerical measurement.""")
    + values([("dX", "5.56e&minus;09", "PASS"),
              ("dW", "5.11e&minus;09", "PASS")],
             "hand-derived against numerical")
    + point("""Nine decimal places on <b>both</b>. Worth doing here more than anywhere:
there are two coupled gradients, it is easy to get a sign or an index wrong in one of them,
and a wrong gradient does not crash &mdash; it just trains to a worse answer.""")
),

"train": (
    p("""Learning X and W together, from small random starting values.""")
    + values([("iter 0", "cost 44.357", "random features, random tastes"),
              ("iter 600", "cost 9.505", "essentially converged"),
              ("iter 1800", "cost 9.503", "polishing")],
             "training")
    + point("""It settles at <b>9.5</b>, not near zero. That is <b>regularisation</b> doing
its job &mdash; the penalty terms never go away, so the cost has a floor well above zero. A
collaborative filtering cost that reaches zero has &lambda; = 0 and is overfitting.""")
    + p("""Both sets of parameters must start <b>random</b>. Initialise everything to zero
and all the gradients are symmetric, so nothing ever differentiates &mdash; every user ends
up with identical taste. Same failure as a neural network, same fix.""")
),

"predict": (
    p("""Now fill in the gaps. Existing ratings are shown in brackets for comparison.""")
    + values([("Love at Last / Alice", "4.88 [5]", "close"),
              ("Romance Forever / Bob", "4.44", "<b>never rated it</b> &mdash; predicted"),
              ("Cute Puppies / Alice", "3.93", "<b>never rated it</b> &mdash; predicted"),
              ("Love at Last / Dave", "0.10 [0]", "close")],
             "predicted ratings")
    + point("""Look at the pattern rather than the numbers. Alice and Bob both score the
romances high and the action films low; Carol and Dave do the opposite. <b>Nobody told the
algorithm that some of these films are romances.</b>""")
    + p("""It worked that out from ratings alone, and the film features it invented encode
it &mdash; even though no dimension is labelled &ldquo;romance&rdquo; and none of them means
anything on its own.""")
),

"cold_start": (
    p("""A user who has rated nothing, run through the same training.""")
    + point("""The cost converges to <b>9.50309</b> &mdash; effectively the same as without
them. A user with no ratings contributes <b>nothing</b> to the fitting term, so they cannot
change what the model learns about anyone else.""")
    + p("""And thanks to mean normalisation, they still get sensible recommendations: each
film's average, which is the best guess available. Without it they would get <b>0.0</b> for
everything and be shown the worst films in the catalogue.""")
),

"related": (
    p("""One more thing falls out for free, without any extra training.""")
    + values([("Love at Last", "&rarr; Romance Forever", "d = 0.040"),
              ("Romance Forever", "&rarr; Cute Puppies of Love", "d = 0.013"),
              ("Nonstop Car Chases", "&rarr; Swords vs Karate", "d = 0.024")],
             "nearest neighbour in the learned feature space")
    + point("""The romances found each other. The action films found each other. This came
out of <b>squared distance between learned vectors</b> &mdash; and nobody ever labelled a
genre.""")
    + p("""You never need to know what the features <b>mean</b>. The numbers are
uninterpretable and the <b>distances between them</b> are meaningful anyway. That is exactly
the principle embeddings run on, and it is the bridge from here to how retrieval works.""")
    + point("""At scale, comparing every item to every other is far too slow &mdash; ten
million items per query. Production systems use <b>approximate nearest neighbour</b>
indexes, trading a small chance of missing the true closest item for a thousandfold
speed-up.""")
),
}
