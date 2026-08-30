# -*- coding: utf-8 -*-
"""The gist of C3 Week 2."""
from kit import key, trap
from gistkit import gistline, flow, sameskel, chain, bynumbers, retell, ladder, h2
from walkkit import cases, values, point, expr, chainset, ascii_art

GIST = dict(
    course="C3", week="2", title="Recommender Systems", mins=13,
    scratch=["09-collaborative-filtering", "08-pca"],
    lede="Fifteen lessons on filling in a mostly-empty table — and on the one algorithm here "
         "that learns its own features while it learns its own weights.",
    body="".join([
        gistline("""A ratings table with holes in it. The trick is that you can learn
<b>both sides at once</b>: what each film is like, and what each user wants, with nothing but
the ratings. Nobody describes the films to the algorithm, and it works out that some of them
are romances anyway."""),

        h2("🖼", "The week in one picture"),
        flow([
            ("in", "A ratings table, mostly empty",
             "A real one is <b>99.9%</b> empty. The gaps are what you are trying to fill."),
            ("arw", "subtract each item's mean rating"),
            ("op", "Mean normalisation",
             "So that a user who has rated nothing gets the item's average, rather than "
             "<b>0.0</b> for everything."),
            ("arw", "guess both sides, randomly"),
            ("loop", "repeat until the cost stops falling", [
                ("op", "Predict the RATED cells only",
                 "<b>w &middot; x + b</b>. Unrated cells are masked out — they contribute "
                 "nothing to the cost or the gradient."),
                ("arw", "two gradients, not one"),
                ("back", "Move w AND x",
                 "<b>x is a parameter here.</b> That is the unusual part, and it is what "
                 "&ldquo;collaborative&rdquo; means."),
            ]),
            ("arw", "add the means back on"),
            ("out", "Every empty cell, filled",
             "Plus, for free, which items are similar — from distance in the learned "
             "feature space."),
        ], cap="""PCA sits at the end of this week as a separate idea, and shares one theme:
learned dimensions that mean nothing individually and everything geometrically."""),

        h2("🔁", "The substitution that makes this week different"),
        sameskel("""Cost, gradient, descent, regularisation — all unchanged from Course 1.
The optimiser does not know anything special is happening.""",
                 [("What x is", "your <b>data</b> — fixed, never touched",
                   "a <b>parameter</b> — learned alongside w"),
                  ("Regularisation terms", "&lambda;&Sigma;w&sup2;", "&lambda;&Sigma;w&sup2; "
                                                                     "<b>and</b> &lambda;&Sigma;x&sup2;"),
                  ("Which cells count", "all of them", "<b>only where r(i,j) = 1</b>"),
                  ("Initialisation", "zeros are fine for C1", "<b>must be random</b> — zeros "
                                                              "never differentiate"),
                  ("Why &lambda; is needed", "to stop overfitting", "also to make the problem "
                                                                    "<b>well-posed</b> at all"),
                  ("What features mean", "you chose them", "<b>nothing</b> individually — "
                                                           "only the geometry matters")]),

        h2("🕳", "The distinction that breaks everything if you miss it"),
        key("""<p><b>r(i,j) = 0</b> means the user <b>never rated</b> it. No information.
A question mark.</p>
<p><b>y(i,j) = 0</b> means they rated it <b>zero stars</b>. Strong negative information. They
watched it and hated it.</p>
<p>Every cost function this week sums <b>only where r(i,j) = 1</b>. Treat a question mark as a
zero and you teach the model that <b>everything unwatched is hated</b> — which is most of the
catalogue. It will then confidently recommend nothing.</p>
<p>In the vectorised code that entire restriction is <b>one character</b>: multiply by the
0/1 matrix <b>R</b> before squaring. Zeroed cells contribute nothing to the cost and, having
zero derivative, nothing to the gradient either.</p>"""),

        h2("🔢", "What it learns without being told"),
        bynumbers("""Five films, four users, 15 of 20 cells rated. After training, the
learned feature space is asked which film is most like which.""",
                  [("Love at Last", "&rarr; Romance Forever", "d = 0.040"),
                   ("Romance Forever", "&rarr; Cute Puppies of Love", "d = 0.013"),
                   ("Nonstop Car Chases", "&rarr; Swords vs Karate", "d = 0.024"),
                   ("final cost", "9.503", "not near zero — that is &lambda; doing its job")],
                  close="""The romances found each other and the action films found each
other. <b>Nobody labelled a genre.</b> This came out of squared distance between vectors the
algorithm invented for itself — which is exactly the principle embeddings run on, and the
bridge from here to how retrieval works."""),

        h2("⛓", "The three problems, and their fixes"),
        chain([
            dict(name="A new user has rated nothing",
                 does="They appear in no fitting term, so only regularisation touches their "
                      "w — which drives it to <b>0</b>, so every prediction is exactly 0.0.",
                 trap="On a 0–5 scale that recommends the <b>worst films in the "
                      "catalogue</b>, to every new user.",
                 code="prediction = w[j] @ x[i] + b[j] + mu[i]",
                 feeds="mean normalisation fixes it in one line: they get the film's average, "
                       "which is the best guess available."),
            dict(name="A new item has no ratings",
                 does="Collaborative filtering cannot help at all — it only knows items "
                      "through ratings.",
                 trap="This is the <b>cold start</b> problem, and it is structural rather "
                      "than a tuning issue.",
                 feeds="content-based filtering, which uses item FEATURES rather than "
                       "ratings, and so handles a brand-new item on day one."),
            dict(name="Ten million items, 100 milliseconds",
                 does="Two stages with <b>opposite</b> priorities.",
                 trap="<b>Retrieval</b> cuts 10,000,000 to ~100 with cheap rules — optimised "
                      "for <b>recall</b>, because anything it drops can never be recommended. "
                      "<b>Ranking</b> runs the full model on those 100 — optimised for "
                      "<b>precision</b>.",
                 feeds=None),
        ]),

        h2("🏗", "The two-tower architecture"),
        expr("v&#7512; = UserNN(x&#7512;)\nv&#7504; = ItemNN(x&#7504;)\nprediction = v&#7512; &middot; v&#7504;",
             "two separate networks, meeting at a dot product"),
        key("""<p>They can be <b>completely different</b> — different inputs, depths, widths.
The <b>only</b> constraint in the whole design is that both output vectors have the same
length.</p>
<p>Why a dot product at the end rather than another layer? Because <b>v&#7504; does not depend
on the user</b>. You compute the item vector for all ten million items <b>once, overnight</b>,
and store them. At request time you compute one user vector and do ten million cheap dot
products.</p>
<p>Put a network at the join and that disappears — every user/item pair would need a full
forward pass, and nobody gets served in time. <b>The architecture is shaped by the serving
cost</b>, not by accuracy. And <code>l2_normalize</code> before the dot product turns it into
a cosine, so the network cannot cheat by inflating magnitudes instead of learning
directions.</p>"""),

        h2("🔻", "PCA, and what it is honestly for"),
        chain([
            dict(name="The algorithm",
                 does="Centre the features, compute the covariance matrix, take its "
                      "eigenvectors sorted by eigenvalue, project onto the top few.",
                 code="z = X_centred @ U[:, :k]",
                 trap="Centring is <b>not</b> tidying. PCA finds directions of greatest "
                      "spread <b>from the origin</b> — so uncentred data gives you a first "
                      "component pointing at where the data <i>is</i> rather than at its "
                      "shape.",
                 feeds="fewer columns, chosen to lose as little spread as possible."),
            dict(name="Why eigenvectors",
                 does="Because <b>each eigenvalue IS the variance along its own "
                      "eigenvector</b>.",
                 trap="So &ldquo;find the direction of greatest variance&rdquo; and "
                      "&ldquo;find the largest eigenvector of the covariance matrix&rdquo; are "
                      "the <b>same instruction</b>, not two steps.",
                 feeds="and real implementations use SVD instead, because forming the "
                       "covariance matrix squares the numbers and loses precision."),
            dict(name="What it is for, today",
                 does="<b>Visualisation.</b> Squash 50 features to 2 so a human can plot them "
                      "and look.",
                 trap="Compression is rarely worth it — storage is cheap now. And speeding up "
                      "supervised learning is a weak argument: <b>PCA discards directions "
                      "without ever looking at y</b>, so the direction it throws away may be "
                      "the one that predicts your label. Regularisation, which does see y, is "
                      "better informed.",
                 feeds=None),
        ]),

        h2("⚖️", "The one ethical property that is unique to this week"),
        trap("""<p><b>A recommender changes the data it will later be trained on.</b> It
shapes the very preferences it claims to be measuring.</p>
<p>A house-price model does not change house prices. A recommender absolutely changes what
people watch — and next quarter's training data is a record of what it recommended. The loop
closes, and the model's mistakes become the ground truth.</p>
<p>Optimise <b>engagement</b> and you amplify outrage, because outrage measurably works.
Optimise <b>ad revenue</b> and the more exploitative business can bid more for the slot. None
of these is a bug in the maths — each is the system doing <b>exactly what it was asked</b>.
The failure is in the objective, and no amount of validation accuracy will flag it.</p>"""),

        h2("🗣", "Say the week back"),
        retell([
            "The difference between r(i,j) = 0 and y(i,j) = 0, and what breaks if you confuse them.",
            "What makes collaborative filtering <b>collaborative</b>, in one sentence.",
            "Why w and x cannot both be initialised to zero.",
            "Why regularisation is needed here even ignoring overfitting.",
            "What a brand-new user is predicted to like, and the one-line fix.",
            "What <code>* R</code> does in the vectorised cost.",
            "How you find related items, and why you never need to know what the features mean.",
            "Collaborative vs content-based: which cold start each one survives.",
            "The single constraint in the two-tower design, and why the join is a dot product.",
            "Why retrieval optimises recall and ranking optimises precision.",
            "Why the principal components are the eigenvectors of the covariance matrix.",
            "What PCA is honestly for today, and the argument against using it to speed up training.",
        ]),

        h2("🪜", "Where this week sits in the whole arc"),
        ladder("C3 W2", """This is where <b>learned representations</b> arrive properly. The
film features here mean nothing individually and everything geometrically — and that is
exactly what an embedding is. The two-tower architecture, approximate nearest neighbour
lookup, and the retrieval-then-ranking split are the same three ideas that a
retrieval-augmented language system is built from; the build lane's retrieval file is this
week's ideas pointed at text instead of films. Week 3 then drops labels <i>and</i> the fixed
dataset, and learns from a reward."""),
    ]),
)
