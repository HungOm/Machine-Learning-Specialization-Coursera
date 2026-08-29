# -*- coding: utf-8 -*-
"""C3 · Week 2 — Recommender systems and PCA."""
from kit import (kid, key, warn, trap, note, card, eq, eqp, decode, table, demo,
                 quiz, links, code, h2, grid2, grid3, pretest, explain, lenses)

REPO = "../../C3%20-%20Unsupervised%20Learning,%20Recommenders,%20Reinforcement%20Learning"
L = []

# ============================================================ 1
L.append(dict(
    slug="01-making-recommendations", title="Making recommendations", mins=13, tag="intuition",
    lede="Probably the most commercially valuable algorithm in this specialization, and it starts with a "
         "table full of question marks.",
    body=(
        pretest("""<p>1000 users, 10000 films, and most of the grid is blank. <b>Guess what you are actually trying to predict</b> — and why the blanks are the whole problem.</p>""",
        """<p>Watch for the notation for “did this user rate this film”, separate from what the rating was.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Four friends, five films. Some of them have given star ratings. Most of the squares are
empty, because nobody watches everything.</p>
<p>Your job: <b>fill in an empty square.</b> Would Bob like “Romance Forever”? If you can guess that well,
you can guess it for every empty square — and then recommend each person whichever film you predicted
highest for them.</p>
<p>That is the whole business. Netflix, Spotify, Amazon, YouTube, every app store.</p>""")

        + lenses(
            """<p>A second-hand bookshop with one very good owner. You have bought from her eleven times. You walk
in, and before you have taken your coat off she has a book on the counter for you.</p>
<p>She has never read your mind. She has a shelf of books, a memory of what <em>you</em> took and what
you brought back, and a memory of what everyone else took. The whole business of recommendation is
those two memories, and this week is about writing them down as a table.</p>""",
            """<p>If you have worked with a sparse matrix, or a survey where most respondents skipped most
questions, you already know the central difficulty here.</p>
<p>It is not that the maths is hard. It is that <b>almost every cell is empty</b>. A cinema with
50,000 films and 10 million users has 500 billion cells and perhaps 0.01% of them filled. Every
technique in this week is a way of being useful about the 99.99% you cannot see.</p>""",
            """<p>A grid. Films down the side, people across the top, a rating written in a cell when that person
rated that film, and a blank when they did not.</p>
<p>That grid is the entire problem statement. Every algorithm this week does exactly one thing to it:
<b>fill in a blank</b>. Not “understand taste” — fill in a blank with a number.</p>""",
            """<p>Roughly a third of what people buy on large retail sites, and the large majority of what gets
watched on streaming services, comes from a recommender rather than a search.</p>
<p>That makes the blank-filling worth an enormous amount of money, and it also means these systems
shape what a culture sees. The lesson on ethics later this week is not an afterthought bolted on: it
is a direct consequence of the sums being this large.</p>""",
            """So the notation below — <var>n</var><sub>u</sub>, <var>n</var><sub>m</sub>, <var>r</var>(i,j),
<var>y</var>(i,j) — is just names for the parts of that grid.""")

        + h2("🎬", "Watch it move")
        + demo("ratingsmatrix", "Four users, five movies, and a lot of question marks",
               "the highlighted cell is the one being predicted")

        + h2("🔢", "The notation")
        + decode([
            ("<var>n</var><sub><var>u</var></sub>", "“n sub u”", "The number of users. 4 here; hundreds of millions in production."),
            ("<var>n</var><sub><var>m</var></sub>", "“n sub m”", "The number of movies (or items)."),
            ("<var>r</var>(<var>i</var>, <var>j</var>)", "“r of i j”", "1 if user j has rated movie i, 0 otherwise. It records <b>whether</b>, not what."),
            ("<var>y</var><sup>(<var>i</var>, <var>j</var>)</sup>", "“y i j”", "The rating user j gave movie i. Only defined where r(i, j) = 1."),
            ("<var>m</var><sup>(<var>j</var>)</sup>", "“m j”", "How many movies user j has rated."),
        ])
        + key("""<p>Every cost function this week sums <b>only over the entries where r(i, j) = 1</b>. You
are never penalised for a rating that does not exist — the question marks contribute nothing. Forgetting
this is the single most common bug in the assignment.</p>""")

        + h2("📏", "The scale of the real problem")
        + """<p>The example has 4 × 5 = 20 cells with 6 question marks. A real system has perhaps
100,000,000 users and 50,000 items — five trillion cells, of which maybe 0.01% are filled.</p>
<p>That extreme sparsity is not an obstacle to the method; it is the reason the method exists. If the
matrix were full there would be nothing to predict.</p>"""

        + h2("🧮", "How empty is the matrix, really?")
        + """<p>The assignment’s MovieLens slice, counted:</p>"""
        + table(["", "value"],
                [["movies (n<sub>m</sub>)", "4,778"],
                 ["users (n<sub>u</sub>)", "443"],
                 ["cells in the matrix", "2,116,654"],
                 ["cells that contain a rating", "<b>39,253</b>"],
                 ["fraction filled", "<b>1.85%</b> — so 98.15% is empty"]])
        + """<p>That is the problem in one number. You are asked to predict two million values from
thirty-nine thousand, and the thirty-nine thousand are not spread evenly:</p>"""
        + table(["", "min", "median", "max"],
                [["ratings per user", "1", "31", "1,270"],
                 ["ratings per movie", "1", "<b>2</b>", "198"]])
        + """<p>The <em>median movie has two ratings</em>. Half the catalogue is known through one or
two opinions. Any method that needs a decent sample per item is dead on arrival here, which is
exactly why the algorithm has to borrow strength across users rather than treat each movie
separately.</p>"""
        + explain("""<p>98% of the matrix is missing, and the missing cells are not missing at
random — people watch what they expect to like. <b>Why does that make “unrated” a bad substitute for
“rated zero”?</b></p>""",
                  """<p>Because a blank does not mean disliked, it overwhelmingly means unseen. If
you filled the blanks with zeros you would be asserting two million strong negative opinions that
nobody expressed, and since those fabricated cells outnumber the real ones fifty to one, they would
dominate the cost function completely — the model would learn to predict “everyone hates
everything”. That is why every formula this week carries the condition r(i,j) = 1, and why the
vectorised version multiplies by R.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Treating a question mark as a 0.</b> “Has not watched it” is not the same as “rated
it zero”. Conflating them teaches the model that everything unwatched is bad — and unwatched is almost
everything.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("What is the difference between r(i,j) = 0 and y(i,j) = 0?",
             "<p><b>r = 0</b> means the user never rated it — no information. <b>y = 0</b> means they "
             "rated it zero stars — strong negative information. Completely different.</p>"),
            ("Why is a 99.99% empty matrix normal rather than a data-quality problem?",
             "<p>Because nobody watches 50,000 films. Sparsity is the natural state, and predicting the "
             "empty cells is the entire task.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("paper", "https://ieeexplore.ieee.org/document/5197422",
             "Koren, Bell & Volinsky (2009) — Matrix Factorization Techniques for Recommender Systems",
             "Written by the team that won the Netflix Prize. The clearest single paper on this topic."),
            ("docs", "https://developers.google.com/machine-learning/recommendation",
             "Google — Recommendation Systems course",
             "A free short course covering everything in this week, with a different worked example."),
            ("lab", REPO + "/week2/C3W2/C3W2A1/C3_W2_Collaborative_RecSys_Assignment.ipynb",
             "Week 2 assignment 1: collaborative filtering",
             "In this repo. The real MovieLens dataset."),
        ])
    )))

# ============================================================ 2
L.append(dict(
    slug="02-per-item-features", title="Using per-item features", mins=10, tag="core",
    lede="If somebody has already labelled every film as romantic or action-y, recommendation collapses "
         "into linear regression — one per user.",
    body=(
        pretest("""<p>You know each film's romance and action scores. <b>Guess how you would learn one person's taste</b> — and what familiar algorithm that turns out to be.</p>""",
        """<p>Watch for it being ordinary linear regression, run once per user.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Suppose someone has gone through and scored every film: how romantic is it (0 to 1), and
how much action does it have (0 to 1).</p>
<p>Now look at Alice’s ratings. She gave 5 stars to the romantic films and 0 to the action ones. So Alice’s
personal formula is roughly “5 × romance + 0 × action”. Learn that formula for her, and you can score any
film she has not seen.</p>
<p>Then do it again for Bob. And again for Carol. One little formula each.</p>""")

        + lenses(
            """<p>A video shop where every case has two numbers pencilled on the spine by the owner: <b>how much
romance</b>, and <b>how much action</b>, each out of ten.</p>
<p>You tell her you liked a 9-romance, 1-action film and hated a 0-romance, 10-action one. She now has
enough to guess at any other film on the shelf without knowing anything else about you — because the
films were described first, and your taste is read off the descriptions.</p>""",
            """<p>This is ordinary <b>linear regression, one model per person</b>.</p>
<p>If you have fitted a separate regression for each store, each patient or each region, you have done
exactly this: the same feature columns, a different coefficient vector each time, fitted on that
unit's own rows. The only novelty is that a “unit” is a user and the rows are their ratings.</p>""",
            """<p>One person's rating history, written as a little table: the film's two feature numbers on the
left, the rating they gave on the right. Four or five rows.</p>
<p>Fitting <var>w</var> for that person means finding the two weights that best turn the left columns
into the right one. Then you do it again for the next person, from scratch. That stack of tiny
regressions is the whole algorithm.</p>""",
            """<p>The catch is what the pencilled numbers cost. Somebody has to decide how much romance is in every
one of 50,000 films, and keep doing it as the catalogue grows.</p>
<p>Studios and streaming services really did employ people to tag content this way — Netflix's
micro-genre tagging is the famous example — and it does not scale to user-generated catalogues at
all. That expense is precisely what the next lesson removes.</p>""",
            """So the cost function below is the familiar squared error, with one crucial change: it sums only over
the films that person actually rated.""")

        + h2("🎬", "Watch it move")
        + demo("peritemfeatures", "One user at a time — click through the four",
               "the shading is what that user’s learned formula predicts everywhere in feature space")

        + h2("🔢", "The maths, decoded")
        + eqp([
            'predicted rating <span class="op">=</span> ',
            ('<var class="hl-b">w</var><sup>(<var>j</var>)</sup> <span class="op">·</span> <var class="hl-a">x</var><sup>(<var>i</var>)</sup>', "dot-product-f0", "multiply matching entries, add them up"),
            ' <span class="op">+</span> <var class="hl-b">b</var><sup>(<var>j</var>)</sup>',
        ], "user j’s taste, dotted with movie i’s features — hover or click it")
        + eqp([
            'min <span class="frac"><span>1</span><span>2</span></span> ',
            ('<span class="big">Σ</span><sub><var>i</var> : <var>r</var>(<var>i</var>,<var>j</var>)=1</sub>', "sigma", "for every movie user j rated"),
            (' ( <var>w</var><sup>(<var>j</var>)</sup>·<var>x</var><sup>(<var>i</var>)</sup> + <var>b</var><sup>(<var>j</var>)</sup> − <var>y</var><sup>(<var>i</var>,<var>j</var>)</sup> )',
             "error-term", "predicted rating − actual rating"),
            ('<sup>2</sup>', "squared-term", "squared"),
            ' <span class="op">+</span> ',
            ('<span class="frac"><span>λ</span><span>2</span></span> <span class="big">Σ</span>( <var>w</var><sub><var>k</var></sub><sup>(<var>j</var>)</sup> )<sup>2</sup>',
             "reg-penalty", "keeps this user's weights small"),
        ], "the cost for ONE user — this is just regularised linear regression — hover or click a part")
        + decode([
            ("<var class='hl-a'>x</var><sup>(<var>i</var>)</sup>", "“the features of movie i”", "Given to you in this lesson. A vector like [0.9, 0.0] meaning “very romantic, no action”."),
            ("<var class='hl-b'>w</var><sup>(<var>j</var>)</sup>", "“user j’s parameters”", "Learned. A vector the same length as x, saying how much this user cares about each feature."),
            ("<var>i</var> : <var>r</var>(<var>i</var>,<var>j</var>)=1", "“only the movies they rated”", "The sum skips every question mark. This is the piece of notation to get right."),
            ("λ", "“the usual regulariser”", "Same job as in Course 2: keep w small so a user with three ratings does not get wild parameters."),
        ])
        + key("""<p>There is nothing new here. It is <b>Course 1 linear regression, run n<sub>u</sub> times
— once per user</b>, each on that user’s own handful of ratings.</p>""")

        + h2("🚧", "And here is the problem")
        + """<p>Where did x come from? Somebody watched every film and scored its romance and action levels
by hand. For five films that is an afternoon. For fifty thousand films with twenty features each, it is a
million judgement calls — and two people would disagree about half of them.</p>
<p>Worse, the features you can easily label (genre, year, length) are often not the ones that predict
taste. Whatever it is that makes people who liked <i>Arrival</i> also like <i>Prisoners</i>, nobody has a
column for it.</p>"""

        + h2("✅", "Check yourself")
        + quiz([
            ("Alice rates romantic films 5 and action films 0. Roughly what is her w?",
             "<p>About <b>[5, 0]</b> with b ≈ 0 — strongly positive on romance, indifferent or negative "
             "on action.</p>"),
            ("Why does the sum only run over movies where r(i,j) = 1?",
             "<p>Because you have no target y for the others. Including them would mean inventing a "
             "target, and any value you invent is wrong.</p>"),
            ("Ten users, two features. How many parameters?",
             "<p>10 × (2 weights + 1 bias) = <b>30</b>. Each user has their own w and b; nothing is "
             "shared.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("docs", "https://developers.google.com/machine-learning/recommendation/content-based/basics",
             "Google — content-based filtering basics",
             "The same idea, framed as a feature-matching problem."),
        ])
    )))

# ============================================================ 3
L.append(dict(
    slug="03-collaborative-filtering", title="The collaborative filtering algorithm", mins=20, tag="core",
    lede="The central idea of the week: if you do not have features, learn them. From the ratings. At the "
         "same time as everything else.",
    body=(
        pretest("""<p>Last lesson assumed you know what each film is like. <b>You do not. Guess how you could learn the films' features and everyone's taste at the same time</b>, from ratings alone.</p>""",
        """<p>Watch for the bootstrap: each side helps pin down the other. That mutual help is why it is called collaborative.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Last lesson: “if I know what the films are like, I can work out what each person likes.”</p>
<p>Turn it round: “if I know what each person likes, I can work out what the films are like.” Alice loves
this film and hates that one, and Alice is a romance person — so this film is probably romantic.</p>
<p>Now the magic: <b>do both at once.</b> Start with random guesses for everything. Nudge the people
formulas to fit the ratings. Nudge the film features to fit the ratings. Repeat. Both get better together
— each one bootstrapping the other.</p>
<p>That is why it is called <em>collaborative</em>: the users collaborate, without ever meeting, to tell
the algorithm what the films are like.</p>""")

                + lenses(
            """<p>Two regulars at a bookshop who keep buying the same novels.</p>
<p>The bookseller has never read any of them and could not tell you what genre they are. But she knows
that when one of them likes something, the other usually does too — so when a new title lands well with
the first, she puts it aside for the second.</p>
<p>She is recommending without understanding the books at all. That is the whole trick.</p>""",
            """<p>This is matrix factorisation: approximate a mostly-empty ratings matrix as the product of two
much smaller ones — a taste vector per user and a feature vector per item.</p>
<p>What makes it unusual is that <b>both</b> factors are unknown and learned simultaneously. In Courses
1 and 2 the features were given and only the weights were learned; here the features are themselves
parameters.</p>""",
            """<p>A grid with 98% of the cells blank.</p>
<p>Films down the side, people across the top, a handful of scattered ratings. The task is to fill in
every blank from the few that are filled — and the only structure available is that similar people
rate similar films similarly.</p>""",
            """<p>On this course’s own MovieLens slice: 4,778 films × 443 users is 2.1 million cells, of which
<b>39,253</b> are filled. That is 1.85%. The median film has been rated <b>twice</b>.</p>
<p>Any method needing a decent sample per item is dead on arrival at those numbers, which is exactly why
borrowing strength across users is not a clever optimisation but the only thing that works.</p>""",
            """So the cost function below sums only over cells that actually contain a rating — and that one
condition is the heart of it.""")
        + h2("🎬", "Watch it move")
        + demo("collabfilter", "Real gradient descent, running live",
               "orange cells are the model's predictions; the vectors on the right are features nobody labelled")
        + """<p>Watch the learned feature vectors settle. The three romantic films end up with similar
numbers, and the two action films end up with similar numbers of the opposite sign — <b>nobody told it
about romance or action</b>. It discovered that the ratings split that way.</p>"""

        + h2("🔢", "The maths, decoded")
        + eqp([
            ("<var>J</var>(<var>w</var>, <var>b</var>, <var class=\"hl-a\">x</var>)", "cost-j", "the cost"),
            ' <span class="op">=</span> <span class="frac"><span>1</span><span>2</span></span> ',
            ('<span class="big">Σ</span><sub>(<var>i</var>,<var>j</var>) : <var>r</var>(<var>i</var>,<var>j</var>)=1</sub>',
             "sigma", "for every rating that actually exists"),
            (' ( <var>w</var><sup>(<var>j</var>)</sup>·<var class="hl-a">x</var><sup>(<var>i</var>)</sup> + <var>b</var><sup>(<var>j</var>)</sup> − <var>y</var><sup>(<var>i</var>,<var>j</var>)</sup> )',
             "error-term", "predicted rating − actual rating"),
            ('<sup>2</sup>', "squared-term", "squared"),
        ], "sum over every rating that actually exists — hover or click a part")
        + eqp([
            ' <span class="op">+</span> ',
            ('<span class="frac"><span>λ</span><span>2</span></span> <span class="big">Σ</span><sub><var>j</var></sub><span class="big">Σ</span><sub><var>k</var></sub>(<var>w</var><sub><var>k</var></sub><sup>(<var>j</var>)</sup>)<sup>2</sup>',
             "reg-penalty", "keeps every user's weights small"),
            ' <span class="op">+</span> ',
            ('<span class="frac"><span>λ</span><span>2</span></span> <span class="big">Σ</span><sub><var>i</var></sub><span class="big">Σ</span><sub><var>k</var></sub>(<var class="hl-a">x</var><sub><var>k</var></sub><sup>(<var>i</var>)</sup>)<sup>2</sup>',
             "reg-penalty", "keeps every movie's features small"),
        ], "…regularise the user parameters AND the movie features — hover or click a part")
        + decode([
            ("<var class='hl-a'>x</var> as a parameter", "“the features are learned too”", "The one change from last lesson, and the whole idea. x is no longer given — it is optimised."),
            ("the double sum", "“every existing rating, once”", "Summing over both i and j where r = 1 is the same as summing over every filled-in cell."),
            ("two regularisation terms", "“keep both small”", "One for w, one for x. Symmetric, because both are now parameters."),
            ("collaborative", "“users help each other”", "Bob’s ratings help pin down what a film is like, which helps predict Carol’s rating of it."),
        ])
        + eqp([
            ('<var>w</var><sub><var>k</var></sub><sup>(<var>j</var>)</sup> :=', "assign-op", "becomes, not equals"),
            ' <var>w</var><sub><var>k</var></sub><sup>(<var>j</var>)</sup> − ',
            ('α', "alpha-lr", "the learning rate"),
            ' ∂J/∂<var>w</var><sub><var>k</var></sub><sup>(<var>j</var>)</sup> &nbsp;&nbsp; <var>b</var><sup>(<var>j</var>)</sup> := <var>b</var><sup>(<var>j</var>)</sup> − α ∂J/∂<var>b</var><sup>(<var>j</var>)</sup> &nbsp;&nbsp; ',
            ('<var class="hl-a">x</var><sub><var>k</var></sub><sup>(<var>i</var>)</sup> :=', "assign-op", "becomes, not equals"),
            ' <var class="hl-a">x</var><sub><var>k</var></sub><sup>(<var>i</var>)</sup> − α ∂J/∂<var class="hl-a">x</var><sub><var>k</var></sub><sup>(<var>i</var>)</sup>',
        ], "gradient descent updates all three, simultaneously — hover or click a part", small=True)
        + key("""<p>The third update is the new one. Gradient descent is now descending in <b>w, b and
x</b> together. Nothing else about the machinery changes.</p>""")

        + h2("🔬", "Why does this not just produce nonsense?")
        + """<p>A fair worry: you are fitting two unknowns against each other with no ground truth for
either. Two reasons it works:</p>
<ul>
<li><b>Every rating constrains many parameters at once.</b> One rating touches one user vector and one
movie vector. With thousands of ratings, the constraints overlap heavily and only a consistent solution
survives.</li>
<li><b>Regularisation breaks ties.</b> Without λ there are infinitely many equivalent solutions (scale w
up and x down by the same factor and every prediction is unchanged). λ picks the smallest one.</li>
</ul>
<p>What you do <em>not</em> get is interpretability. The learned x₁ is not “romance” — it is whatever
direction happened to explain the most variation. It is only meaningful up to rotation.</p>"""

        + h2("🧮", "The cost function, evaluated")
        + """<p>The lab gives you a small corner of the data — 5 movies, 4 users, 3 features — with
known-good <var>X</var>, <var>W</var> and <var>b</var>, so you can check your implementation against
a number rather than a feeling:</p>"""
        + table(["λ", "J", "what it contains"],
                [["0", "<b>13.67</b>", "squared error over rated cells only"],
                 ["1.5", "<b>28.09</b>", "the same, plus (λ/2)(Σw² + Σx²)"]])
        + """<p>Get 13.67 and your masking is right. Get 28.09 and your regularisation is right. If
the first is wrong the second cannot be diagnosed, so fix them in that order.</p>
<p>The most common wrong answer is larger than 13.67, and it means the sum ran over every cell
instead of only the rated ones — the model being charged for failing to predict ratings nobody
gave.</p>"""
        + note("""<p>Notice that regularisation more than doubles the cost here. That is not a sign
λ is too big; it is a sign the corner is tiny — 5 × 3 + 4 × 3 = 27 parameters against only a handful
of ratings, so the penalty term is large relative to the error term. On the full 4,778 × 443
problem the balance is completely different.</p>""")
        + explain("""<p>The regularisation penalises <var>x</var> and <var>w</var> together, in one
sum. <b>Why is it not a problem that a single λ controls both?</b></p>""",
                  """<p>Because they enter the prediction symmetrically — it is
<var>w</var>·<var>x</var>, and scaling <var>x</var> up while scaling <var>w</var> down by the same
factor leaves every prediction identical. Without a penalty that symmetry is a free direction the
optimiser can wander along forever; penalising both ends pins it down, and pinning it down is all
one λ needs to do. Separate λs would let the same wandering resume at a different ratio.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Initialising everything to zero.</b> Then all gradients are symmetric and nothing
ever differentiates. Initialise w and x to <b>small random values</b>, exactly as with neural
networks.</p>""")
        + trap("""<p><b>Summing over all cells instead of the rated ones.</b> Your model learns that every
unwatched film deserves a 0. Predictions collapse.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("Why is it called “collaborative” filtering?",
             "<p>Because users collectively supply the information that defines the items. Bob's ratings "
             "shape the movie features that improve Carol's predictions, even though they never interact.</p>"),
            ("100 users, 50 movies, 3 features. How many parameters?",
             "<p>Users: 100 × (3 + 1) = 400. Movies: 50 × 3 = 150. <b>550 total</b>, learned from however "
             "many ratings exist.</p>"),
            ("Does the learned x₁ mean “romance”?",
             "<p>No. It is whatever direction best explains the ratings. It may correlate with romance, "
             "and it has no guaranteed interpretation — the solution is only defined up to rotation.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("paper", "https://ieeexplore.ieee.org/document/5197422",
             "Koren, Bell & Volinsky (2009) — Matrix Factorization Techniques",
             "This algorithm is matrix factorisation: you are factorising Y ≈ X·Wᵀ. The paper explains the connection properly."),
            ("paper", "https://dl.acm.org/doi/10.1145/1401890.1401944",
             "Koren (2008) — Factorization meets the neighborhood",
             "How the Netflix Prize was actually won: blending this with neighbourhood methods."),
            ("lab", REPO + "/week2/C3W2/C3W2A1/C3_W2_Collaborative_RecSys_Assignment.ipynb",
             "Week 2 assignment 1",
             "In this repo. You write the vectorised cost function and train it on real MovieLens data."),
        ])
    )))

# ============================================================ 4
L.append(dict(
    slug="04-binary-labels", title="Binary labels: favs, likes and clicks", mins=9, tag="core",
    lede="Almost nobody gives star ratings. Everybody clicks. The same algorithm, with the linear-to-"
         "logistic swap you already know.",
    body=(
        pretest("""<p>Instead of 1–5 stars you only have clicked / did not click. <b>Guess which Course 1 idea you would borrow</b> to handle a 0-or-1 label.</p>""",
        """<p>Watch for the sigmoid and the log loss reappearing, unchanged, in a completely different setting.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Real apps rarely ask you to rate things out of five. They just watch what you do.
Did you click it? Did you watch past 30 seconds? Did you buy it?</p>
<p>So the table stops holding 0–5 and starts holding 1 (yes) and 0 (no). Everything else works the same —
you just swap the prediction formula and the loss, exactly like going from linear regression to logistic
regression in Course 1.</p>""")

        + lenses(
            """<p>The shop owner stops asking customers for marks out of five, because almost nobody gave her one.
Instead she just watches: <b>did they pick it up, and did they take it home?</b></p>
<p>She loses the fine detail — she can no longer tell a four from a five — and she gains a hundred
times more evidence, because every customer generates it without being asked. That trade is worth
making, and it is the trade the whole modern industry has made.</p>""",
            """<p>You have seen this move before: it is the switch from <b>linear regression to logistic
regression</b>, and it is the same switch for the same reason.</p>
<p>Squared error on a 0/1 target is badly behaved; the logistic loss is not. Everything you learned in
C1 W3 transfers wholesale — sigmoid on the output, binary cross-entropy instead of squared error, and
the rest of the algorithm untouched.</p>""",
            """<p>The same grid as before, with the numbers replaced by 1, 0 or blank.</p>
<p>And the essential distinction, which is easy to skate over: <b>0 is not blank</b>. A 0 means shown
and not clicked — real negative evidence. A blank means never shown at all. Confusing the two is the
single most common mistake in applied recommenders.</p>""",
            """<p>Implicit feedback — clicks, watch time, skips — is what every large recommender actually runs on,
because explicit ratings are rare, biased towards extremes, and given by the wrong people.</p>
<p>It also brings a bias that explicit ratings do not: you only observe clicks on things the system
chose to show, so the model is trained on its own past decisions. Whole subfields exist to correct
for that feedback loop.</p>""",
            """So the change below is one line — swap the squared error for the logistic loss — and it is the line
that made recommenders practical.""")

        + h2("🎬", "Watch it move")
        + demo("binarylabels", "Ones, zeros, and question marks",
               "note that 0 and ? mean completely different things")

        + h2("🔢", "The two swaps")
        + table(["", "Ratings (continuous)", "Clicks (binary)"],
                [["Prediction", "w·x + b", "<b>g(w·x + b)</b> — sigmoid"],
                 ["Loss", "(prediction − y)²", "<b>−y log(f) − (1−y) log(1−f)</b>"],
                 ["Output means", "predicted stars", "<b>P(y = 1)</b>, the chance they engage"]])
        + decode([
            ("<var>y</var> = 1", "“engaged”", "Clicked, watched past a threshold, liked, bought, favourited."),
            ("<var>y</var> = 0", "“shown it, and did not engage”", "Real negative evidence — they saw it and passed."),
            ("<var>y</var> = ?", "“never shown it”", "No information at all. Must not be treated as 0."),
            ("g(z)", "“sigmoid”", "Squashes the prediction into 0…1 so it can be read as a probability."),
        ])
        + key("""<p>The 0 versus ? distinction is where real systems go wrong. If you log “not clicked” for
every item on the page but only ever show 20 items out of 50,000, then 49,980 items are <b>?</b> — and
recording them as 0 poisons the model.</p>""")

        + h2("🌍", "What counts as y = 1")
        + grid3(
            card("<h3>Did they click?</h3><p>Cheap and plentiful, and easily gamed by clickbait. Optimising "
                 "purely for this is Lesson 11’s cautionary tale.</p>"),
            card("<h3>Did they finish it?</h3><p>Much stronger evidence of genuine value, and much rarer.</p>"),
            card("<h3>Did they come back?</h3><p>The strongest signal, and the slowest to collect. Long-term "
                 "metrics are the hardest to optimise and the most worth optimising.</p>"))

        + h2("✅", "Check yourself")
        + quiz([
            ("Why not just record every unshown item as y = 0?",
             "<p>Because you would be teaching the model that the user rejected 50,000 items they were "
             "never offered. The model learns that almost everything is unwanted.</p>"),
            ("What does the model output now, and how do you use it?",
             "<p>P(y = 1) — the probability of engagement. Rank items by it and show the top few. You "
             "usually never threshold it at all.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("paper", "https://dl.acm.org/doi/10.1109/ICDM.2008.22",
             "Hu, Koren & Volinsky (2008) — Collaborative Filtering for Implicit Feedback Datasets",
             "The standard reference for clicks-instead-of-ratings, including how to weight confidence in a 0."),
            ("docs", "https://developers.google.com/machine-learning/recommendation/dnn/training",
             "Google — implicit vs explicit feedback",
             "Practical notes on negative sampling, which is how the ? problem is handled at scale."),
        ])
    )))

# ============================================================ 5
L.append(dict(
    slug="05-mean-normalization", title="Mean normalization", mins=14, tag="core",
    lede="A brand-new user with zero ratings gets zero for everything — which is both useless and slightly "
         "insulting. One subtraction fixes it.",
    body=(
        pretest("""<p>A brand-new user has rated nothing. <b>Guess what the algorithm predicts for them</b>, and why that is unhelpful.</p>""",
        """<p>Watch for what subtracting each film's average rating fixes, and what the new user gets predicted instead.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Eve just signed up. She has rated nothing.</p>
<p>The maths says: keep her formula small, so w = 0. Which means every prediction for Eve is exactly 0.
Zero stars for everything. We would either recommend her nothing, or recommend the films the algorithm
thinks are worst.</p>
<p>Fix: before training, subtract each film’s average rating from its row. Now “zero” means “average”
instead of “terrible”. Add the average back when predicting, and Eve gets sensible starting
recommendations — the generally well-liked films.</p>""")

        + lenses(
            """<p>Two judges at a village show. One gives 7s and 8s to everything he mildly likes; the other gives
2s to anything short of perfection. Neither is wrong, and comparing their raw numbers is
meaningless.</p>
<p>So the show secretary does what secretaries have always done: she subtracts each judge's own
average before comparing. Now a 2 from the harsh judge and an 8 from the generous one can sit in the
same column and mean the same thing.</p>""",
            """<p>This is <b>centring</b>, the same operation you apply before a PCA or when computing a
correlation, and it does the same job here: it removes a per-unit offset that is not the signal you
care about.</p>
<p>The wrinkle specific to recommenders is what it does for a user with <em>no</em> ratings at all.
Centring quietly turns “I know nothing about you” into “I predict the average”, which is the correct
and sane default, and you get it for free rather than special-casing it.</p>""",
            """<p>A row of ratings, and the same row with that row's mean subtracted from every entry.</p>
<p>Do it once on paper with [5, 5, 0, 0, blank] and you will see the whole point: the mean is 2.5, the
row becomes [2.5, 2.5, −2.5, −2.5, blank], and a brand-new user with an empty row now predicts 2.5
instead of 0.</p>""",
            """<p>Without this, a new user is predicted to hate everything, so the system shows them nothing good,
so they never rate anything, so they stay new. That is the <b>cold-start</b> problem doing real
commercial damage in the first thirty seconds of a customer's life.</p>
<p>Mean normalization is a two-line fix for the most expensive minute in the product.</p>""",
            """So the step below — subtract the row mean, add it back at prediction time — is worth far more than
its size suggests.""")

        + h2("🎬", "Watch it move")
        + demo("meannorm", "Press the button and watch Eve’s column change meaning",
               "same maths, different baseline")

        + h2("🔢", "The maths, decoded")
        + eqp([
            ('<var>μ</var><sub><var>i</var></sub> <span class="op">=</span> average rating of movie <var>i</var>', "avg-factor", "the average"),
            ' &nbsp;&nbsp;→&nbsp;&nbsp; train on ( <var>y</var><sup>(<var>i</var>,<var>j</var>)</sup> <span class="op">−</span> <var>μ</var><sub><var>i</var></sub> )',
        ], "step 1 — centre each row — hover or click it", small=True)
        + eqp([
            'prediction <span class="op">=</span> ',
            ('<var>w</var><sup>(<var>j</var>)</sup>·<var>x</var><sup>(<var>i</var>)</sup>', "dot-product-f0", "multiply matching entries, add them up"),
            ' <span class="op">+</span> <var>b</var><sup>(<var>j</var>)</sup> <span class="op">+</span> <var class="hl-a">μ</var><sub><var>i</var></sub>',
        ], "step 2 — add the mean back when predicting — hover or click it")
        + decode([
            ("μ<sub>i</sub>", "“the mean for movie i”", "Averaged over the users who <em>did</em> rate it — the question marks are skipped."),
            ("by row, not by column", "“per movie”", "Row normalisation helps new <b>users</b>. Column normalisation would help new <b>movies</b>, which is a different (and harder) problem."),
            ("cold start", "“the new-user problem”", "The general name for “I know nothing about this user or item yet”. Mean normalisation is the cheapest partial answer."),
        ])
        + key("""<p>With w = 0 and b = 0, the prediction is now μ<sub>i</sub> — the average rating of that
film. A new user is shown the generally-liked films, which is exactly the right default.</p>""")

        + h2("🔬", "The second benefit")
        + """<p>Centring the data also speeds up gradient descent, for the same reason feature scaling did
in Course 1: the cost surface becomes rounder and less elongated, so gradient descent takes a more direct
path. This is a smaller effect than the cold-start fix, but it is free.</p>"""

        + h2("🧮", "Worked on four real movies")
        + """<p>Four of the most-rated films, three users who rated them, and a fourth user who has
rated none of them:</p>"""
        + table(["", "user A", "user B", "user C", "user D (new)", "movie mean"],
                [["movie 1", "5.0", "3.5", "4.0", "—", "<b>4.167</b>"],
                 ["movie 2", "5.0", "3.5", "3.5", "—", "<b>4.000</b>"],
                 ["movie 3", "5.0", "3.5", "4.0", "—", "<b>4.167</b>"],
                 ["movie 4", "5.0", "4.0", "5.0", "—", "<b>4.667</b>"]])
        + """<p>Subtract each row’s mean from its rated cells and you get <var>Y</var><sub>norm</sub>:</p>"""
        + table(["", "user A", "user B", "user C"],
                [["movie 1", "+0.833", "−0.667", "−0.167"],
                 ["movie 2", "+1.000", "−0.500", "−0.500"],
                 ["movie 3", "+0.833", "−0.667", "−0.167"],
                 ["movie 4", "+0.333", "−0.667", "+0.333"]])
        + """<p>The numbers now say something better than “how many stars”: they say <em>how much
above or below this film’s reputation</em>. User A is consistently generous, user B consistently
harsh, and the model no longer has to spend parameters rediscovering that.</p>
<p>Now user D. Every term for them is skipped, so regularisation drives their
<var>w</var> and <var>b</var> to <b>0</b>, and the prediction is 0 + the movie mean:
<b>4.167, 4.000, 4.167, 4.667</b>. Without normalisation the same reasoning gives 0 stars for
everything — the worst possible first impression. With it, a brand-new user is shown the
best-reviewed films, which is exactly right when you know nothing about them.</p>"""
        + explain("""<p>The normalisation is per <em>movie</em> (each row), not per user. <b>Given
that the problem being solved is a new user, why is the row the right choice?</b></p>""",
                  """<p>Because the fallback has to be computable without any information about the
person. A movie’s mean exists as soon as anyone has rated it, so it is available for a user who has
done nothing — which is precisely the case that needs rescuing. A user’s mean requires that user to
have rated something, so for the new user it does not exist at all, and normalising by it would
solve every case except the one that was broken. (Per-user normalisation is a real technique — it
handles harsh and generous raters — but it is a different problem.)</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Forgetting to add μ<sub>i</sub> back at prediction time.</b> Every prediction comes
out centred around zero, and your top recommendations are meaningless.</p>""")
        + trap("""<p><b>Including question marks in the mean.</b> Only average over the ratings that
exist.</p>""")
        + warn("""<p>Mean normalisation solves the new-<b>user</b> problem. It does <em>not</em> solve the
new-<b>movie</b> problem — a film with no ratings has no meaningful μ<sub>i</sub> either. That needs
content-based features, which is Lesson 8 onward.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("A movie has ratings 5, 4, and ? and ?. What is μ for that row?",
             "<p>(5 + 4) / 2 = <b>4.5</b>. The two question marks are skipped, not counted as zeros.</p>"),
            ("Why normalise by row rather than by column?",
             "<p>Because the goal is a sensible default for new <em>users</em>. Row (per-movie) means "
             "give a new user the average rating of each film.</p>"),
            ("Does this fix the cold start for new movies?",
             "<p>No. A film nobody has rated has no μ either. That needs content features — see Lesson 8.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("docs", "https://developers.google.com/machine-learning/recommendation/collaborative/summary",
             "Google — collaborative filtering, pros and cons",
             "The cold-start section is exactly this problem, with the standard mitigations listed."),
        ])
    )))

# ============================================================ 6
L.append(dict(
    slug="06-tensorflow-collaborative", title="TensorFlow implementation of collaborative filtering",
    mins=14, tag="code",
    lede="Why you write the training loop by hand here, and how GradientTape does the calculus for a cost "
         "function Keras has never heard of.",
    body=(
        pretest("""<p>This cost function has no standard layer type. <b>Guess how you would still use TensorFlow to minimise it.</b></p>""",
        """<p>Watch for auto-differentiation as a general tool, not a neural-network feature — you write the cost, it finds the gradient.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Usually you hand TensorFlow a stack of layers and say “train it”. But collaborative
filtering isn’t a stack of layers — it’s a strange sum over a sparse set of (user, movie) pairs.</p>
<p>So you write the loop yourself. The good news: you still don’t have to do any calculus. TensorFlow
<b>records</b> everything you compute on a “tape”, then plays it backwards to get the derivatives.</p>""")

        + lenses(
            """<p>A joiner who has always cut mortises by hand buys a machine. The machine does not know what a
mortise is. It knows how to move a chisel exactly where he tells it, very fast, without tiring.</p>
<p>His job changes from cutting to <b>describing the cut</b>. Get the description right and the machine
is unstoppable; get it wrong and it will make the same mistake ten thousand times without
complaining.</p>""",
            """<p>Automatic differentiation is the idea, and it is far older and far simpler than deep learning
makes it sound.</p>
<p>If you have used a solver in a spreadsheet, or <code>scipy.optimize.minimize</code> with a
numerically estimated gradient, you have used the same division of labour: you supply the objective,
the tool supplies the derivative. TensorFlow's <code>GradientTape</code> just does it exactly rather
than approximately.</p>""",
            """<p>A tape recorder that is running while you compute the cost.</p>
<p>Every operation you perform inside the <code>with tf.GradientTape()</code> block is written onto the
tape in order. When you ask for the gradient, the tape is played <em>backwards</em>, applying the
chain rule at each step. That is the entire mechanism, and it is why the block has to wrap the
forward computation.</p>""",
            """<p>This lesson is where the course quietly stops being about recommenders and starts being about a
general tool.</p>
<p>Collaborative filtering is not a <code>Sequential</code> model — you are optimising two parameter
matrices in a custom cost — so this is the first time you meet the escape hatch that every non-standard
model in industry is built through. Anything you invent later gets trained exactly this way.</p>""",
            """So the code below is not recommender code. It is the general pattern: define the cost, tape it,
apply the gradients.""")

        + h2("🎬", "Watch it move")
        + demo("tfcollab", "The tape, recording and replaying",
               "step through — watch what lands on the tape and what comes back off it")

        + h2("💻", "The real thing")
        + code("""
optimizer = keras.optimizers.Adam(learning_rate=1e-1)

for iter in range(200):
    with tf.GradientTape() as tape:
        cost_value = cofi_cost_func_v(X, W, b, Ynorm, R, lambda_)

    grads = tape.gradient(cost_value, [X, W, b])      # all three at once
    optimizer.apply_gradients(zip(grads, [X, W, b]))
""")
        + decode([
            ("<code>tf.Variable</code>", "“a trainable thing”", "X, W and b must be Variables, not plain tensors, or the tape will not track them."),
            ("<code>GradientTape</code>", "“the recorder”", "Everything computed inside the <code>with</code> block is remembered so it can be differentiated."),
            ("<code>tape.gradient(cost, [X, W, b])</code>", "“all the derivatives”", "One backward pass returns ∂J/∂X, ∂J/∂W and ∂J/∂b together."),
            ("<code>apply_gradients</code>", "“take the step”", "Adam handles the per-parameter learning rates (C2 W2 L11)."),
        ], head=("Piece", "Say it out loud", "What it does"))

        + h2("🔢", "The vectorised cost")
        + code("""
def cofi_cost_func_v(X, W, b, Y, R, lambda_):
    j = (tf.linalg.matmul(X, tf.transpose(W)) + b - Y) * R    # <- R zeroes the '?' entries
    J = 0.5 * tf.reduce_sum(j ** 2)
    J += (lambda_ / 2) * (tf.reduce_sum(X ** 2) + tf.reduce_sum(W ** 2))
    return J
""")
        + key("""<p><code>* R</code> is the whole trick. Multiplying elementwise by the 0/1 matrix R
zeroes out every unrated cell <b>before</b> squaring, so the question marks contribute exactly nothing to
the cost or to the gradient. One character does the job of the “sum only where r(i,j)=1” notation.</p>""")

        + h2("🧮", "The real training run")
        + """<p>4,778 movies × 443 users, 10 features, λ = 1, 200 Adam steps on the mean-normalised
ratings:</p>"""
        + table(["iteration", "J"],
                [["0", "14,647.8"],
                 ["20", "5,826.0"],
                 ["40", "5,073.2"],
                 ["100", "4,748.4"],
                 ["160", "4,701.1"],
                 ["199", "<b>4,687.7</b>"]])
        + """<p>Most of the work happens in the first twenty steps — the cost falls by 60% before
iteration 20 and by another 4% over the remaining 180. That shape is typical of Adam and is why
200 iterations is enough here.</p>
<p>The end result, in units you can feel: the model’s predictions on the 39,253 <em>known</em>
ratings are off by <b>0.292 stars</b> on average.</p>"""
        + warn("""<p>Which is a training-set number, and Course 2 Week 3 applies here in full. It
tells you the optimiser worked. It does not tell you the recommendations are good — for that you
would hold out ratings and predict them.</p>""")
        + explain("""<p>Every other model this course has trained used <code>model.fit</code>. This
one needs a hand-written loop with <code>GradientTape</code>. <b>What about collaborative filtering
rules out the standard path?</b></p>""",
                  """<p>That there is no input flowing through layers. <code>fit</code> assumes a
model that maps X to y, so it can push examples forward and errors backward. Here
<em>both</em> operands of the prediction are unknowns being learned simultaneously, and the “input”
X is itself a parameter — there is nothing to feed in. <code>GradientTape</code> drops that
assumption: it records whatever arithmetic you write and differentiates it with respect to whatever
variables you name. Which means the same three lines will optimise any cost function you can express
in code — a genuinely general tool that <code>fit</code> is a convenience wrapper around.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Computing the cost outside the <code>with</code> block.</b> Nothing is recorded, and
<code>tape.gradient</code> returns <code>None</code>. A silent, confusing failure.</p>""")
        + trap("""<p><b>Using plain tensors instead of <code>tf.Variable</code>.</b> Same symptom: gradients
come back as None.</p>""")
        + trap("""<p><b>Applying <code>* R</code> after squaring.</b> Works out the same numerically here,
but do it before and the intent is clearer — and with other losses the order genuinely matters.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("Why can't you use model.compile() and model.fit() for this?",
             "<p>Because the cost is not a standard per-example loss over a fixed input tensor — it is a "
             "sum over a sparse set of (i, j) pairs with two sets of parameters being learned "
             "simultaneously. Keras has no built-in for it.</p>"),
            ("What does tape.gradient return for [X, W, b]?",
             "<p>A list of three tensors, ∂J/∂X, ∂J/∂W and ∂J/∂b, each the same shape as its parameter.</p>"),
            ("What does multiplying by R accomplish?",
             "<p>It zeroes the error for every unrated cell, so unrated entries contribute nothing to J "
             "or its gradient — the vectorised equivalent of “sum only where r(i,j) = 1”.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("docs", "https://www.tensorflow.org/guide/autodiff",
             "TensorFlow — automatic differentiation and GradientTape",
             "Every gotcha, including why gradients come back None."),
            ("docs", "https://www.tensorflow.org/guide/basic_training_loops",
             "TensorFlow — writing a custom training loop",
             "The pattern used here, explained from first principles."),
            ("lab", REPO + "/week2/C3W2/C3W2A1/C3_W2_Collaborative_RecSys_Assignment.ipynb",
             "Week 2 assignment 1",
             "You write cofi_cost_func, first with loops and then vectorised."),
        ])
    )))

# ============================================================ 7
L.append(dict(
    slug="07-finding-related-items", title="Finding related items", mins=8, tag="core",
    lede="“Because you watched X…” — and it is one line of maths on features nobody ever labelled.",
    body=(
        pretest("""<p>The learned features have no names — nobody knows what x₃ means. <b>Guess how you would still find films similar to a given one.</b></p>""",
        """<p>Watch for distance doing the work without interpretation. You never need to know what the numbers mean.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Every film ended up with a little list of numbers. You have no idea what the numbers
mean — but films that got <b>similar</b> numbers turn out to be similar films.</p>
<p>So to find films like this one: measure the distance between number lists and pick the closest few.
That is the entire “because you watched…” row.</p>""")

        + lenses(
            """<p>A record shop with the stock arranged not by genre but by <em>how it sounds</em>. Two albums end
up next to each other because the same people kept buying both, and nobody at the shop can quite
articulate why they go together.</p>
<p>“Customers who liked this also liked…” is that shelf. The similarity was never described in words.
It was learned from behaviour and then measured with a ruler.</p>""",
            """<p>This is nearest-neighbour search in a learned vector space, and the distance is the squared
Euclidean one you already know.</p>
<p>If you have done any clustering or used cosine similarity on documents, the move is familiar: turn
each object into a vector, then let geometry stand in for meaning. What is new is that nobody chose
the axes — the optimiser did, and it will not tell you what they represent.</p>""",
            """<p>The feature vector <var>x</var><sup>(i)</sup> that collaborative filtering learned for one film,
sitting as a point in space, with the handful of other points nearest to it circled.</p>
<p>Those circled points are the recommendation. No user is involved in this computation at all —
which is exactly why it works on a page for a film you have never seen, for a visitor who is not
logged in.</p>""",
            """<p>This is the workhorse of “more like this”, and it is what fills the page when a system knows
nothing about you.</p>
<p>It is also where the failure modes show up first: a niche film with four ratings sits next to
whatever those four people also happened to rate, and the result is confidently absurd. Production
systems put a minimum-ratings floor on this for exactly that reason.</p>""",
            """So the distance formula below is doing something modest and useful: measuring how close two learned
descriptions turned out to be.""")

        + h2("🎬", "Watch it move")
        + demo("relateditems", "Pick a film, get its nearest neighbours",
               "the green lines are the two closest in learned-feature space")

        + h2("🔢", "The maths, decoded")
        + eqp([
            'similarity(<var>k</var>, <var>i</var>) <span class="op">=</span> ',
            ('‖ <var>x</var><sup>(<var>k</var>)</sup> <span class="op">−</span> <var>x</var><sup>(<var>i</var>)</sup> ‖<sup>2</sup>', "sq-distance", "how far apart, in feature space"),
            ' <span class="op">=</span> ',
            ('<span class="big">Σ</span><sub><var>l</var></sub> ( <var>x</var><sub><var>l</var></sub><sup>(<var>k</var>)</sup> <span class="op">−</span> <var>x</var><sub><var>l</var></sub><sup>(<var>i</var>)</sup> )<sup>2</sup>',
             "sigma", "add up every feature's contribution"),
        ], "squared distance between two feature vectors — smallest wins — hover or click a part")
        + decode([
            ("‖ · ‖²", "“squared distance”", "The same formula as in K-means. Distance in feature space is doing all the work again."),
            ("cosine similarity", "“the angle version”", "x·z / (‖x‖‖z‖). Often preferred, because it ignores magnitude and compares direction only."),
            ("k-nearest neighbours", "“the top few”", "Sort by distance, take the closest 5 or 10."),
        ])
        + key("""<p>You never need to know what x₁ and x₂ <em>mean</em>. Distance works regardless of
interpretation — which is fortunate, because the learned features have no interpretation.</p>""")

        + h2("🚧", "The scaling problem")
        + """<p>Comparing one item against 50,000 others is 50,000 distance computations, per request. That
is fine offline and far too slow for a page load.</p>
<p>Production systems precompute the neighbour lists in a batch job overnight, or use an <b>approximate
nearest neighbour</b> index — FAISS, ScaNN, HNSW — which trades a tiny amount of accuracy for
millisecond lookups over millions of items. This is also exactly how vector databases for LLM retrieval
work; the technique is the same one.</p>"""

        + h2("🕳", "Traps")
        + trap("""<p><b>Cold start again.</b> A brand-new film has a random x, so its “related items” are
nonsense until it accumulates ratings. Fall back to content features for new items.</p>""")
        + trap("""<p><b>Recommending things that are <em>too</em> similar.</b> Five sequels of the same film
is technically correct and a bad user experience. Real systems add an explicit diversity penalty.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("x⁽¹⁾ = [0.9, 0.1] and x⁽²⁾ = [0.8, 0.2]. Squared distance?",
             "<p>(0.9−0.8)² + (0.1−0.2)² = 0.01 + 0.01 = <b>0.02</b>. Very close — these two films are "
             "near-neighbours.</p>"),
            ("Why does this work when the features are uninterpretable?",
             "<p>Because similar ratings patterns produce similar vectors. The <em>relative</em> geometry "
             "is meaningful even though the axes are not.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("docs", "https://github.com/facebookresearch/faiss",
             "FAISS — Facebook AI Similarity Search",
             "The standard library for fast approximate nearest-neighbour search over millions of vectors."),
            ("paper", "https://arxiv.org/abs/1603.09320",
             "Malkov & Yashunin (2016) — HNSW",
             "The graph-based index behind most modern vector databases. Elegant, and readable."),
        ])
    )))

# ============================================================ 8
L.append(dict(
    slug="08-collaborative-vs-content", title="Collaborative filtering vs content-based filtering",
    mins=9, tag="core",
    lede="Two philosophies. One learns from who else liked it; the other learns from what it is. Real "
         "systems use both.",
    body=(
        pretest("""<p>Collaborative filtering uses only who-rated-what. <b>Guess what it cannot do</b> that a method using actual user and item attributes could.</p>""",
        """<p>Watch for the cold-start problem, and for what each approach is genuinely better at.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p><b>Collaborative:</b> “people who liked what you liked also liked this.” It knows
nothing about the film itself — only about the pattern of who rated what.</p>
<p><b>Content-based:</b> “you are 27, you like sci-fi, and this is a 2019 sci-fi film with actors you have
watched before.” It looks at the actual properties of you and of the item.</p>
<p>Collaborative can find surprising links nobody would have described. Content-based can handle a film
released this morning that nobody has rated yet. You want both.</p>""")

        + lenses(
            """<p>Two ways to be recommended a builder. The first: <b>“three people on this street used him and
were happy.”</b> Nothing about the builder is described — only the pattern of who was pleased.</p>
<p>The second: <b>“he is a roofer, he is certified, he works in your postcode, and you need a
roof.”</b> Nobody's experience is involved. The two answers can disagree, and knowing which one you
are getting matters enormously.</p>""",
            """<p>This is the same axis as memory-based versus model-based reasoning, or case-based versus
rule-based systems.</p>
<p>And it has the same well-known weakness on each side: the behaviour-based one cannot say anything
about a thing nobody has used yet, and the description-based one cannot discover anything its
descriptions failed to capture.</p>""",
            """<p>Two arrows pointing at the same empty cell in the grid.</p>
<p>One arrow comes along the <em>column</em> — other people's ratings of this film. The other comes
along the <em>row</em> — this film's attributes matched against your stated preferences. Same blank,
two entirely different routes to a number.</p>""",
            """<p>Every real system runs both, because each covers the other's blind spot. A brand-new film has no
ratings, so content-based carries it until it has some; an obscure film with no useful metadata is
found only by behaviour.</p>
<p>The switchover is a genuine engineering decision with revenue attached, and “hybrid recommender”
is simply the industry's name for having made it.</p>""",
            """So the comparison below is not a ranking. It is a description of two different blind spots.""")

        + h2("🎬", "Watch it move")
        + demo("cfvscbf", "Five deciding factors, side by side",
               "note that both cold-start rows favour content-based")

        + h2("🔢", "What content-based needs")
        + grid2(
            card("<h3>User features x<sub>u</sub></h3><ul><li>age, gender, country</li>"
                 "<li>average rating given per genre</li><li>how long they have been a member</li>"
                 "<li>device, time of day</li></ul>"),
            card("<h3>Item features x<sub>m</sub></h3><ul><li>year, genre(s), runtime</li>"
                 "<li>average rating received</li><li>cast, director, studio</li>"
                 "<li>the poster and the description text</li></ul>"))
        + decode([
            ("<var>x</var><sub><var>u</var></sub><sup>(<var>j</var>)</sup>", "“user j’s features”", "Known facts about the person. Given, not learned."),
            ("<var>x</var><sub><var>m</var></sub><sup>(<var>i</var>)</sup>", "“item i’s features”", "Known facts about the item. Also given."),
            ("<var>v</var><sub><var>u</var></sub>, <var>v</var><sub><var>m</var></sub>", "“the learned vectors”", "What the two networks produce from those raw features. These <em>are</em> learned — see the next lesson."),
            ("cold start", "“nothing known yet”", "The failure mode collaborative filtering cannot escape, and content-based can."),
        ])
        + key("""<p>The two feature lists can be <b>completely different lengths and completely different
kinds of thing</b>. That is fine — the next lesson shows how they get mapped into a shared space where
they can be compared.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Assuming content-based is safer because it uses “real” information.</b> It can only
express what its features encode. If the thing that actually drives taste is not in your feature list, it
is invisible — and collaborative filtering would have found it.</p>""")
        + trap("""<p><b>Filter bubbles.</b> Content-based recommends more of what you already engage with,
by construction. Deliberate diversity injection is a design decision, not an emergent property.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("A film released this morning with zero ratings. Which approach can recommend it?",
             "<p><b>Content-based.</b> Its genre, cast and year exist from day one. Collaborative "
             "filtering has literally nothing to work with.</p>"),
            ("What can collaborative filtering find that content-based cannot?",
             "<p>Patterns nobody thought to encode as a feature — the hard-to-name quality shared by two "
             "films in different genres that the same people happen to love.</p>"),
            ("Must the user and item feature vectors be the same length?",
             "<p><b>No.</b> The two networks in the next lesson map them into vectors of the same length, "
             "and that is the only place the lengths must match.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("docs", "https://developers.google.com/machine-learning/recommendation/content-based/summary",
             "Google — content-based filtering, pros and cons",
             "A concise table of exactly this trade-off."),
            ("paper", "https://dl.acm.org/doi/10.1145/2843948",
             "Gomez-Uribe & Hunt (2015) — The Netflix Recommender System",
             "How a real production system blends both approaches, and what it is worth commercially. Unusually candid."),
        ])
    )))

# ============================================================ 9
L.append(dict(
    slug="09-deep-content-based", title="Deep learning for content-based filtering", mins=16, tag="core",
    lede="Two neural networks, two very different inputs, one shared output space — and a dot product at "
         "the end. This is the architecture behind modern recommenders and modern search alike.",
    body=(
        pretest("""<p>Users have attributes; films have different attributes; the two lists are not even the same length. <b>Guess how you would still compare them.</b></p>""",
        """<p>Watch for two networks meeting at a dot product, and for the single constraint on their output layers.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>You know a lot about the person: age, country, what genres they usually like. You know a
lot about the film: year, genre, cast. These are completely different kinds of information, so you cannot
compare them directly.</p>
<p>So build <b>two</b> machines. One turns everything about a person into 32 numbers. The other turns
everything about a film into 32 numbers. Neither machine knows what the other is doing.</p>
<p>Now both are lists of 32 numbers — so you can compare them. Multiply them together and add up. Big
number, good match.</p>""")

        + lenses(
            """<p>The video-shop owner stops pencilling two numbers on the spine and starts writing a paragraph:
cast, director, decade, mood, pace, budget, where it was shot.</p>
<p>She cannot compare paragraphs by eye any more. So she hires someone whose only job is to read a
paragraph and boil it down to <b>thirty-two numbers</b>, doing it the same way every time. The
paragraphs are rich; the thirty-two numbers are comparable. That reader is the network.</p>""",
            """<p>This is the <b>two-tower</b> architecture, and it is one of the most widely deployed shapes in
industry.</p>
<p>If you know Siamese networks from signature verification or face matching, it is the same idea:
two separate networks, no shared weights, trained jointly so that their outputs land in one shared
space where a dot product means something.</p>""",
            """<p>Two funnels pointing at each other.</p>
<p>Into the left funnel goes everything you know about the user — age band, watch history, country —
and out comes a vector of 32 numbers. Into the right goes everything about the film, and out comes
another 32. The prediction is the dot product of the two outputs. Nothing else.</p>""",
            """<p>The two towers are why this scales. The film tower can be run <b>overnight</b>, once per film,
and the results stored — films do not change.</p>
<p>At request time you run only the small user tower and take dot products against a precomputed
table. That asymmetry is what lets a system respond in 20 milliseconds over a catalogue of
millions, and it is the whole reason the architecture is shaped this way.</p>""",
            """So the two networks below are not one model split in half. They are two encoders that were taught
to agree on a meeting place.""")

        + h2("🎬", "Watch it move")
        + demo("deepcbf", "Two towers meeting at a dot product",
               "the towers have different inputs and different shapes — only the output length must match")

        + h2("🔢", "The maths, decoded")
        + eqp([
            '<var class="hl-b">v</var><sub><var>u</var></sub> <span class="op">=</span> UserNN(<var>x</var><sub><var>u</var></sub>) &nbsp;&nbsp;&nbsp; <var class="hl-a">v</var><sub><var>m</var></sub> <span class="op">=</span> ItemNN(<var>x</var><sub><var>m</var></sub>) &nbsp;&nbsp;&nbsp; prediction <span class="op">=</span> ',
            ('<var class="hl-b">v</var><sub><var>u</var></sub> <span class="op">·</span> <var class="hl-a">v</var><sub><var>m</var></sub>',
             "dot-product-f0", "how well the two embeddings match"),
        ], "two networks, one dot product — hover or click it")
        + decode([
            ("<var>x</var><sub><var>u</var></sub>", "“raw user features”", "Whatever you know: age, country, average rating per genre. Could be 50 numbers."),
            ("<var>v</var><sub><var>u</var></sub>", "“the user embedding”", "The network’s 32-number summary of that user. Learned."),
            ("<var>v</var><sub><var>m</var></sub>", "“the item embedding”", "The 32-number summary of the item. Also learned."),
            ("the dot product", "“how well they match”", "One number. Large when the two vectors point the same way."),
            ("two towers", "“the architecture’s name”", "Also called a dual-encoder. The same design underlies modern semantic search and retrieval-augmented generation."),
        ])
        + key("""<p>The two networks can have <b>completely different architectures and completely
different input sizes</b>. The only constraint in the entire design is that their <em>output layers</em>
have the same number of units, so the dot product is defined.</p>""")

        + h2("🔢", "The cost")
        + eqp([
            ("<var>J</var>", "cost-j", "the cost"),
            ' <span class="op">=</span> ',
            ('<span class="big">Σ</span><sub>(<var>i</var>,<var>j</var>) : <var>r</var>(<var>i</var>,<var>j</var>)=1</sub>', "sigma", "for every rating that actually exists"),
            (' ( <var>v</var><sub><var>u</var></sub><sup>(<var>j</var>)</sup> · <var>v</var><sub><var>m</var></sub><sup>(<var>i</var>)</sup> <span class="op">−</span> <var>y</var><sup>(<var>i</var>,<var>j</var>)</sup> )',
             "error-term", "predicted rating − actual rating"),
            ('<sup>2</sup>', "squared-term", "squared"),
            ' <span class="op">+</span> regularisation',
        ], "the same shape of cost as before — and both networks are trained by it at once — hover or click a part", small=True)
        + """<p>Both towers are trained together, end to end, with one gradient. This is the “neural
networks compose” advantage from C2 W4 L13 being cashed in: you could never do this with two decision
trees.</p>"""

        + h2("💰", "Why the dot product is the point")
        + """<p>The architecture looks like an aesthetic choice. It is an engineering one.</p>
<p>Because the item tower only depends on the item, you can compute <b>every</b> v<sub>m</sub> once,
overnight, and store them. At request time you run the user tower once and do 50,000 dot products — which
is one matrix multiply, and fast. If instead the model took (user, item) jointly and mixed them in the
hidden layers, you would have to run a full forward pass per candidate item, which is hopeless at scale.</p>
<p>Everything in the next lesson depends on this property.</p>"""

        + h2("🧮", "Why both towers must end at the same width")
        + """<p>Each tower ends with <code>tf.linalg.l2_normalize</code>, which rescales a vector to
length 1. Take two 4-dimensional outputs (the real ones are 32-dimensional; the arithmetic is
identical):</p>"""
        + table(["", "raw output", "length", "after l2_normalize"],
                [["<var>v</var><sub>u</sub> (a user)", "[1, 2, 2, 0]", "3.000", "[0.333, 0.667, 0.667, 0]"],
                 ["<var>v</var><sub>m</sub> (film A)", "[2, 1, 2, 0]", "3.000", "[0.667, 0.333, 0.667, 0]"],
                 ["<var>v</var><sub>m</sub> (film B)", "[0, 0, 1, 2]", "2.236", "[0, 0, 0.447, 0.894]"]])
        + """<p>Now the predictions, which are just dot products:</p>"""
        + table(["Pair", "dot product", "reading"],
                [["user · film A", "<b>0.889</b>", "strong match"],
                 ["user · film B", "0.298", "weak match"]])
        + """<p>Because both vectors have length 1, the dot product is exactly the cosine of the angle
between them, so it is pinned to the range −1 … +1 no matter what the towers output. That is what
makes the two scores comparable — and it is why normalising matters: without it, a tower could
inflate its outputs and win every comparison by being loud rather than by being right.</p>
<p>The shared width is not a convention. A dot product pairs element 1 with element 1, element 2
with element 2, and so on — it is undefined the moment the lengths differ. The two towers may take
completely different inputs and have completely different hidden sizes, but their <em>final</em>
layers must match, and mismatching them is the assignment’s most common error.</p>"""
        + explain("""<p>The towers are trained jointly, from one prediction error, even though
neither ever sees the other’s input. <b>How does the user tower learn anything about films?</b></p>""",
                  """<p>Through the dot product, which is the only place the two ever meet. The error
at the output is a single number, and the gradient of that number with respect to
<var>v</var><sub>u</sub> depends on <var>v</var><sub>m</sub> — literally, the derivative of
<var>v</var><sub>u</sub>·<var>v</var><sub>m</sub> with respect to <var>v</var><sub>u</sub>
<em>is</em> <var>v</var><sub>m</sub>. So the film vector is exactly the message the user tower
receives about films, and vice versa. The two towers negotiate a shared 32-dimensional language in
which “what this person wants” and “what this film is” can be compared.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Mismatched output sizes.</b> A 32-unit user tower and a 64-unit item tower cannot
be dotted. It is the one hard constraint, and it produces a shape error rather than a silent bug —
mercifully.</p>""")
        + trap("""<p><b>Forgetting to normalise the raw features.</b> Age in years (0–100) and “average
rating per genre” (0–5) on very different scales, straight into a network — the C2 W1 lesson applies here
too.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("User tower outputs 32 numbers, item tower outputs 32. What does the dot product give?",
             "<p>A single number — the predicted rating, or a logit to pass through a sigmoid for a "
             "binary label.</p>"),
            ("Can the user tower have 4 layers and the item tower 6?",
             "<p><b>Yes.</b> Different depths, widths and even different input sizes are all fine. Only "
             "the final layer widths must agree.</p>"),
            ("Why is it valuable that v_m depends only on the item?",
             "<p>Because you can precompute all of them offline. Serving then becomes one user-tower pass "
             "plus a big matrix multiply — which is what makes the next lesson possible.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("paper", "https://dl.acm.org/doi/10.1145/2959100.2959190",
             "Covington, Adams & Sargin (2016) — Deep Neural Networks for YouTube Recommendations",
             "This exact architecture, in production, at YouTube scale. One of the most useful applied ML papers there is."),
            ("paper", "https://arxiv.org/abs/1606.07792",
             "Cheng et al. (2016) — Wide & Deep Learning for Recommender Systems",
             "Google Play’s recommender. Combines memorisation and generalisation in one model."),
            ("lab", REPO + "/week2/C3W2/C3W2A2/C3_W2_RecSysNN_Assignment.ipynb",
             "Week 2 assignment 2: content-based filtering with a neural network",
             "In this repo. You build both towers in Keras."),
        ])
    )))

# ============================================================ 10
L.append(dict(
    slug="10-large-catalogues", title="Recommending from a large catalogue", mins=14, tag="core",
    lede="You cannot run a neural network on ten million items while somebody waits for a page to load. "
         "The answer is two stages: cheap and rough, then slow and accurate.",
    body=(
        pretest("""<p>10 million films and a user waiting. You cannot score them all. <b>Guess the two-stage shape of a practical answer.</b></p>""",
        """<p>Watch for retrieval then ranking — cheap and rough first, expensive and careful on the survivors.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>You are picking a birthday present from a shop with ten million things in it. You do not
examine all ten million.</p>
<p>First you grab a trolley-full of <b>plausible</b> things — quickly, roughly, using easy rules like “toys,
about the right age, popular this year”. Maybe a hundred items.</p>
<p>Then you look at those hundred <b>properly</b> and pick the best few.</p>
<p>Fast filter, then careful ranking. Every large recommender works this way.</p>""")

        + lenses(
            """<p>A librarian asked for a book like the one you just finished, in a library of ten million.</p>
<p>She does not consider ten million books. She walks to two or three <em>shelves</em> that are
obviously relevant, pulls perhaps a hundred, and only then reads the blurbs properly to pick five.
Fast and rough, then slow and careful — and never slow and careful on everything.</p>""",
            """<p><b>Retrieval then ranking</b>, and the shape is everywhere: a database index before a full table
scan, a cheap bounding-box test before exact collision detection, triage before diagnosis.</p>
<p>The economics are always the same. A cheap filter you can afford to run on everything, then an
expensive judgement you can only afford on what survives.</p>""",
            """<p>A funnel with two stages written on it: <b>10,000,000 → 500 → 10</b>.</p>
<p>The first arrow is approximate nearest-neighbour lookup, milliseconds, slightly wrong. The second
is the full model on 500 candidates, and it is allowed to be slow because 500 is a small number. The
whole system's latency budget lives in the shape of that funnel.</p>""",
            """<p>Getting the funnel wrong is one of the most common causes of a recommender that is excellent
offline and disappointing in production.</p>
<p>If retrieval never surfaces an item, no amount of ranking quality can rescue it — your beautifully
tuned model simply never sees it. Teams measure <b>retrieval recall</b> separately for this reason,
and it is usually the first thing to check when a good model underperforms.</p>""",
            """So the two-stage design below is not an optimisation bolted on afterwards. It is the only reason
the thing runs at all.""")

        + h2("🎬", "Watch it move")
        + demo("retrieval", "The funnel — and the trade-off in how wide you open it",
               "drag the candidate count and watch the quality-versus-cost balance shift")

        + h2("🔢", "The two stages")
        + table(["", "Retrieval", "Ranking"],
                [["Goal", "generate plausible candidates", "score them accurately"],
                 ["How many items", "10,000,000 → ~100", "~100 → 10"],
                 ["Method", "precomputed lists, nearest-neighbour lookup, simple rules", "the full two-tower network"],
                 ["Speed", "milliseconds", "affordable for 100 items"],
                 ["Optimised for", "<b>recall</b> — do not miss anything good", "<b>precision</b> — get the order right"]])
        + """<p>Typical retrieval rules, straight from the lecture:</p>
<ul>
<li>For each of the last 10 films the user watched, find the 10 most similar items.</li>
<li>For each of the user’s top 3 genres, take the top 10 films.</li>
<li>The top 20 films in the user’s country.</li>
</ul>
<p>Then combine, remove duplicates and anything already watched, and pass the survivors to ranking.</p>"""
        + key("""<p>Retrieval is allowed to be crude, because ranking will fix the ordering. What retrieval
must <b>not</b> do is miss something good — anything it drops can never be recommended, no matter how good
the ranker is.</p>""")

        + h2("⚖️", "Choosing the candidate count")
        + """<p>More candidates → better final recommendations, and more compute per request. Andrew’s
advice is refreshingly concrete: run an offline experiment. Increase the candidate count and measure
whether the final recommendations actually improve. When they stop improving, stop paying.</p>"""
        + note("""<p>Because v<sub>m</sub> depends only on the item, all item embeddings can be computed
overnight and stored in an approximate nearest-neighbour index. Retrieval then becomes a single index
lookup rather than a model call. This is the payoff for the two-tower design in Lesson 9.</p>""",
               "Why the architecture made this possible")

        + h2("🧮", "The arithmetic that forces two stages")
        + """<p>Scoring every item for one user, on this course’s data set and at industrial scale:</p>"""
        + table(["Catalogue", "network passes to score everything", "feasible in ~100 ms?"],
                [["this assignment — 4,778 films", "4,778", "yes, comfortably"],
                 ["a streaming service — 10⁵ titles", "100,000", "borderline"],
                 ["a large marketplace — 10⁸ items", "100,000,000", "<b>no, by several orders</b>"]])
        + """<p>And that is <em>per user, per page load</em>. The bottom row is not a tuning problem;
no amount of hardware makes a hundred million forward passes fit in a page load.</p>
<p>So the work is split. <b>Retrieval</b> assembles a few hundred plausible candidates using cheap
lookups — items similar to the last few watched, the top items in each favourite genre, what is
popular in the user’s country. No network runs. <b>Ranking</b> then runs the expensive model on
those candidates only, perhaps 200 forward passes instead of 10⁸.</p>
<p>The saving that makes it work: <var>v</var><sub>m</sub> for every item depends only on the item,
so all 10⁸ of them are computed <em>offline</em> and cached. At request time the item tower does not
run at all — only the user tower, once, followed by a few hundred dot products.</p>"""
        + explain("""<p>Retrieval uses crude heuristics that the ranking model would easily beat.
<b>Why is it not better to make retrieval smarter?</b></p>""",
                  """<p>Because the two stages are judged on different things. Retrieval only has to
avoid <em>missing</em> good items — anything it passes through gets properly evaluated a moment
later, so its precision barely matters and its recall is everything. That job is well served by
cheap, broad, diverse heuristics. Making retrieval smarter means making it slower, which forces it
to consider fewer candidates, which costs recall — the one thing it exists to protect. The right
tuning knob is the number of candidates, and you find it by measuring whether more candidates still
improve the final recommendations.</p>""")

        + h2("🔤", "The words, decoded")
        + decode([
            ("retrieval", "“retrieval”", "Cheaply assembling a few hundred plausible candidates. Judged on recall, not precision."),
            ("ranking", "“ranking”", "Running the expensive model on those candidates only, to order them."),
            ("candidate generation", "“candidates”", "Another name for retrieval. The list handed to the ranker."),
            ("precomputed embedding", "“cached vector”", "An item's v_m, computed offline because it does not depend on who is looking. What makes serving feasible."),
            ("latency", "“latency”", "How long a request takes. The hard budget everything here is designed around."),
        ])
        + h2("🕳", "Traps")
        + trap("""<p><b>Judging retrieval by precision.</b> Retrieval should be judged on <em>recall</em> —
did the good items survive? Precision is the ranker’s job.</p>""")
        + trap("""<p><b>Forgetting to filter.</b> Already-watched, out-of-stock, region-blocked and
age-inappropriate items must be removed. Usually after retrieval, before ranking.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("Why not just run the full model on all 10 million items?",
             "<p>10 million forward passes per request. Even at a microsecond each that is 10 seconds — "
             "and you have milliseconds.</p>"),
            ("Retrieval returns 100 candidates and the best possible item is not among them. Can ranking recover?",
             "<p><b>No.</b> Ranking only reorders what it is given. This is why retrieval optimises "
             "recall.</p>"),
            ("How do you decide between 100 and 500 candidates?",
             "<p>Offline experiment: raise the number, measure whether the final recommendations improve. "
             "When the improvement flattens, the extra compute is wasted.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("paper", "https://dl.acm.org/doi/10.1145/2959100.2959190",
             "Covington et al. (2016) — YouTube recommendations",
             "Section 4 is candidate generation and ranking, described exactly as in this lesson."),
            ("docs", "https://github.com/google-research/google-research/tree/master/scann",
             "ScaNN — Google’s approximate nearest-neighbour library",
             "What retrieval is actually built on at scale."),
        ])
    )))

# ============================================================ 11
L.append(dict(
    slug="11-ethics-recommenders", title="Ethical use of recommender systems", mins=9, tag="core",
    lede="A recommender changes the data it will later be trained on. That single property is what makes "
         "this the most consequential ethics lesson in the specialization.",
    body=(
        pretest("""<p>A recommender maximising watch time will find <em>something</em> that works. <b>Guess what it might land on that you would not want it to.</b></p>""",
        """<p>Watch for the gap between the metric you optimise and the outcome you actually want.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Imagine you told a robot: “make people watch as long as possible.” Not “make people
happy”. Not “show people useful things”. Just: <b>keep them watching</b>.</p>
<p>The robot will work out — correctly, and without any malice — that angry, shocking and frightening
things keep people watching longest. So it shows more of them. People watch longer. The robot learns it was
right, and shows even more.</p>
<p>Nobody decided to do this. It is simply what the instruction meant when taken literally.</p>""")

        + lenses(
            """<p>A newsagent who notices that the shocking paper sells better, so he moves it to the front. It
sells more, so he orders more. Within a year the quiet local paper is gone from the shop, and no
individual decision he made was wrong.</p>
<p>Nobody set out to narrow what the street reads. Every step was a small, defensible response to what
people actually picked up. That is the whole mechanism, and it does not require anybody's bad
intentions.</p>""",
            """<p>This is a <b>feedback loop</b> with a badly chosen objective, and if you have worked with control
systems, KPIs, or Goodhart's law, you know the failure exactly.</p>
<p>The system optimises what it can measure. Engagement is measurable; whether the time was well spent
is not. So the measurable proxy silently becomes the goal, and it drifts away from the thing it was
standing in for.</p>""",
            """<p>A circle, not a line: <b>shown → clicked → trained on → shown more</b>.</p>
<p>The crucial property is that the model's own output becomes its next training input. Every other
model in this specialization learns from data that was there before it existed. A recommender writes
the data it will be trained on tomorrow.</p>""",
            """<p>This is the loop behind engagement-optimised feeds amplifying outrage, behind recommendation
systems steering viewers towards more extreme content, and behind pricing systems that quietly learn
which customers will tolerate more.</p>
<p>The technical fixes — optimising for a longer-horizon outcome, injecting exploration, capping how
often one item can be shown — are all things you now know how to build, which is the reason this
lesson sits in a technical course rather than a policy one.</p>""",
            """So the questions below are engineering questions. What is being maximised, and who benefits when it
is.""")

        + h2("🎬", "Watch it move")
        + demo("ethicsrec", "The same loop, two different objectives",
               "press the buttons to switch what the system is being told to maximise")

        + h2("🔢", "The problem cases from the lecture")
        + table(["Case", "What the system optimises", "What it amplifies"],
                [["Movie recommendation", "watch time", "usually fine — this one is mostly benign"],
                 ["Social media feed", "engagement", "<b>outrage, conspiracy, and content that provokes</b>"],
                 ["Ad targeting", "click-through, or bid amount", "<b>exploitative businesses that can afford to bid more</b>"],
                 ["News ranking", "clicks", "<b>clickbait headlines over accurate ones</b>"]])
        + """<p>The ad case is the sharpest, and Andrew’s framing is worth quoting in structure: a payday
loan company charging exploitative rates makes more money per customer, so it can afford to bid more for
ad slots, so an ad system that maximises revenue shows it to more people. <b>The more harmful business
outbids the less harmful one, systematically.</b> That is not a bug in the algorithm; it is the algorithm
working exactly as specified.</p>"""
        + key("""<p>The recommender is unusual among ML systems: it <b>changes the data it will later be
trained on</b>. It shapes the very preferences it claims to be measuring. Ordinary supervised models
predict a world they do not affect; this one does not have that luxury.</p>""")

        + h2("🛠", "What can actually be done")
        + grid2(
            card("<h3>Change the objective</h3><ul>"
                 "<li>Optimise for “would you say this was worth your time?”, asked afterwards.</li>"
                 "<li>Weight long-term retention over next-session engagement.</li>"
                 "<li>Filter exploitative categories out on purpose, before ranking.</li></ul>"),
            card("<h3>Change the process</h3><ul>"
                 "<li>Be transparent about what is being optimised.</li>"
                 "<li>Measure harm per subgroup, not just the average (C2 W3 L15).</li>"
                 "<li>Give users real control over their own feed.</li>"
                 "<li>Be willing to lose engagement — and say so out loud.</li></ul>"))
        + warn("""<p>Andrew’s honest note in this lecture: these problems are not solved, and some of the
mitigations cost real money. The recommendation is not “here is the fix” — it is “know what you are
building, and be transparent about the trade you are making”.</p>""")

        + h2("🔤", "The words, decoded")
        + decode([
            ("engagement optimisation", "“maximising watch time”", "Training on time spent rather than on whether the recommendation was good. The root of most of the harm."),
            ("filter bubble", "“the bubble”", "Being shown steadily narrower content because that is what you clicked."),
            ("amplification", "“amplification”", "The system making an existing tendency stronger, rather than merely reflecting it."),
            ("transparency", "“transparency”", "Telling people why they were shown something, and letting them change it."),
        ])
        + h2("✅", "Check yourself")
        + quiz([
            ("Why does optimising for engagement tend to amplify outrage?",
             "<p>Because outrage measurably produces engagement. The system has no notion of “good” — it "
             "has a number, and outrage raises the number.</p>"),
            ("Why is a recommender different from a normal supervised model, ethically?",
             "<p>Because it changes the world it is measuring. Its recommendations shape future "
             "behaviour, which becomes future training data — a feedback loop no static classifier has.</p>"),
            ("What makes ad auctions structurally favour exploitative businesses?",
             "<p>They extract more per customer, so they can bid more per click, so a revenue-maximising "
             "system shows them more. The harm is a direct consequence of the objective.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("paper", "https://arxiv.org/abs/2107.10939",
             "Stray et al. (2021) — What are you optimizing for? Aligning Recommender Systems with Human Values",
             "The most useful practical treatment of this problem, written by people who have shipped these systems."),
            ("paper", "https://arxiv.org/abs/1908.08313",
             "Ribeiro et al. (2019) — Auditing Radicalization Pathways on YouTube",
             "A large empirical study of where recommendation actually leads people. Evidence rather than anecdote."),
            ("book", "https://fairmlbook.org/",
             "Fairness and Machine Learning",
             "Free textbook. Chapter 1 covers feedback loops directly."),
        ])
    )))

# ============================================================ 12
L.append(dict(
    slug="12-tensorflow-content-based", title="TensorFlow implementation of content-based filtering",
    mins=9, tag="code",
    lede="The two-tower model in about eight lines of Keras — plus the one line most people leave out.",
    body=(
        pretest("""<p>Two towers, one dot product. <b>Guess how you would express that in Keras</b> when it is not a simple stack of layers.</p>""",
        """<p>Watch for why <code>Sequential</code> cannot do it, and what replaces it.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Two separate machines. One reads everything you know about a <b>person</b>
— age bracket, what they have watched, how they tend to rate things — and boils it down
to a short list of numbers. The other reads everything you know about a <b>film</b> and boils that
down to a list of numbers of the same length.</p>
<p>Then you compare the two lists. If they point the same way, it is a good match.</p>
<p>The useful part: the film side never changes when a different person arrives, so you can work
out every film's list once, store it, and only ever compute the person's list live. That is what
makes it fast enough to run for millions of items.</p>""")

        + lenses(
            """<p>The joiner's machine again, but now cutting two matching pieces at once. The joint only works if
the tenon and the mortise are cut to the <em>same</em> reference, so both cutters move together and
are adjusted together.</p>
<p>Cut them independently, each perfect against its own reference, and the joint will not close.
Training the two towers jointly is that: two cuts, one reference.</p>""",
            """<p>The Keras functional API is what you reach for the moment a model stops being a straight line of
layers.</p>
<p>If you have built any DAG-shaped computation — a build graph, a dataflow pipeline — the idea is
familiar: name the inputs, wire the operations, then declare which nodes are the model's ends.
<code>Sequential</code> is the special case where the graph is a path.</p>""",
            """<p>Two <code>Sequential</code> stacks drawn side by side, their outputs joined by a single dot
product, and one loss hanging off the bottom.</p>
<p>The gradient flows back from that one loss into <em>both</em> towers. That is the whole reason the
two encoders learn to agree: they are punished together for disagreeing.</p>""",
            """<p>Two details in this code carry disproportionate weight in production: <b>L2-normalising</b> each
tower's output, which turns the dot product into a cosine and stops one tower winning by shouting, and
the fact that the towers do <em>not</em> share weights, because users and films are not the same kind
of thing.</p>
<p>Both are one-line decisions, and both are the sort of thing that silently costs a few percent for
months if you get them wrong.</p>""",
            """So the code below is the two-tower diagram, transcribed almost line for line.""")

        +h2("🎬", "Watch it move")
        + demo("tfcbf", "Step through the code, watch the towers build",
               "the dot at the end is the only place the two sides meet")

        + h2("💻", "The model")
        + code("""
num_outputs = 32

user_NN = tf.keras.models.Sequential([
    tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(num_outputs),          # no activation on the last layer
])
item_NN = tf.keras.models.Sequential([
    tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(num_outputs),
])

input_user = tf.keras.layers.Input(shape=(num_user_features,))
vu = user_NN(input_user)
vu = tf.linalg.l2_normalize(vu, axis=1)          # <- the line people forget

input_item = tf.keras.layers.Input(shape=(num_item_features,))
vm = item_NN(input_item)
vm = tf.linalg.l2_normalize(vm, axis=1)

output = tf.keras.layers.Dot(axes=1)([vu, vm])

model = tf.keras.Model([input_user, input_item], output)
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.01),
              loss=tf.keras.losses.MeanSquaredError())
""")
        + decode([
            ("<code>Input(shape=…)</code>", "“a named entry point”", "Needed because this model has TWO inputs — Sequential cannot express that, so this is the functional API."),
            ("<code>l2_normalize</code>", "“scale to length 1”", "Divides each vector by its own magnitude. The dot product then measures direction only — a cosine similarity."),
            ("<code>Dot(axes=1)</code>", "“multiply and sum”", "Row-wise dot product of the two 32-vectors."),
            ("<code>Model([a, b], out)</code>", "“the functional API”", "Two inputs, one output, one gradient. Both towers train together."),
            ("last layer has no activation", "“linear output”", "The embedding should be free to take any value; squashing it would throw information away."),
        ], head=("Piece", "Say it out loud", "Why it is there"))
        + key("""<p><b>l2_normalize is not optional in practice.</b> Without it, the network can lower the
loss by inflating vector magnitudes rather than by learning better directions, and training becomes
unstable. Normalising removes that degree of freedom.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Using <code>Sequential</code>.</b> It cannot express two inputs meeting at a dot
product. You need the functional API here — this is the standard first reason to reach for it.</p>""")
        + trap("""<p><b>Different <code>num_outputs</code> for the two towers.</b> The Dot layer will
error. Define it once as a variable, as above.</p>""")
        + trap("""<p><b>Forgetting <code>axis=1</code> in l2_normalize.</b> Normalising the wrong axis
scales across the batch instead of within each example — a quiet, wrong result.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("Why the functional API instead of Sequential?",
             "<p>Because the model has two separate inputs that meet in the middle. Sequential only "
             "expresses a single straight chain.</p>"),
            ("What does l2_normalize change about the dot product?",
             "<p>It turns it into a cosine similarity, bounded in [−1, 1] and depending only on direction. "
             "Magnitude can no longer be used to cheat the loss down.</p>"),
            ("Both towers are trained by one loss. Do they share weights?",
             "<p>No. They are separate networks with separate parameters, trained together by one "
             "gradient — which is not the same as sharing.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("docs", "https://www.tensorflow.org/guide/keras/functional",
             "Keras — the functional API",
             "Multiple inputs, multiple outputs, shared layers, skip connections. Worth reading properly once."),
            ("docs", "https://www.tensorflow.org/recommenders",
             "TensorFlow Recommenders (TFRS)",
             "A library that packages this whole two-tower pattern, including retrieval indexes."),
            ("lab", REPO + "/week2/C3W2/C3W2A2/C3_W2_RecSysNN_Assignment.ipynb",
             "Week 2 assignment 2",
             "In this repo. You build exactly this and train it on MovieLens."),
        ])
    )))

# ============================================================ 13
L.append(dict(
    slug="13-reducing-features-pca", title="Reducing the number of features (PCA)", mins=9, tag="optional",
    lede="Start of the optional PCA section. Squash many features into two or three so a human can plot "
         "them and actually look.",
    body=(
        pretest("""<p>Fifty features, and you want to plot the data. <b>Guess how you would get from 50 dimensions to 2</b> without simply throwing 48 away.</p>""",
        """<p>Watch for the idea of a new axis that is a blend of old ones, chosen to keep as much spread as possible.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>You measured every car’s length in centimetres <b>and</b> in inches. Two columns — but
really one fact. If you know one, you know the other.</p>
<p>Now a subtler one: length and width. Not identical, but they move together — big cars are big in both
directions. So most of what those two numbers tell you is really just <b>“how big is this car?”</b>, which
is one number, plus a little bit left over.</p>
<p>PCA finds that one number. It draws a new axis in the direction the data actually spreads, and measures
everything along it.</p>""")

        + lenses(
            """<p>Photographing a chair for a catalogue. You could take a hundred pictures from a hundred angles,
and most of them would tell the buyer nothing new.</p>
<p>One good angle — usually three-quarters from the front — shows the arms, the back and the legs at
once. You have thrown away two of the three dimensions and lost almost nothing that mattered.
Choosing that angle is the entire idea of PCA.</p>""",
            """<p>You may know this as factor analysis, as the SVD, or as the thing that produces a scree plot.</p>
<p>The framing that transfers best: PCA finds the directions of <b>maximum variance</b>, and it assumes
variance is what carries the information. That assumption is usually reasonable and occasionally
catastrophic — a rare but decisive signal has, by definition, low variance.</p>""",
            """<p>A cloud of points on a page that is long and thin, tilted at 30°, with one arrow drawn along its
length.</p>
<p>That arrow is the first principal component. Projecting every point onto it replaces two numbers
with one, and the cloud's shape is why so little is lost. Draw the cloud, draw the arrow, and the
maths afterwards is bookkeeping.</p>""",
            """<p>The honest industrial use of PCA today is mostly <b>visualisation and compression</b>, not
accuracy. It is how you look at a 300-column dataset before modelling it, and how you shrink a
feature store.</p>
<p>Andrew is explicit that using it to prevent overfitting is a mistake people used to make;
regularisation does that job better, and PCA throws away information without ever consulting the
labels.</p>""",
            """So the algorithm below is a way of asking: which single direction, if I could keep only one, would I
keep?""")

        + h2("🎬", "Watch it move")
        + demo("pcaintro", "Two correlated features collapsing onto one axis",
               "the dashed lines show each point dropping onto the new axis")

        + h2("🔢", "The vocabulary")
        + decode([
            ("dimensionality reduction", "“fewer numbers per example”", "Replace n features with k < n new ones that keep most of the information."),
            ("principal component", "“a new axis”", "A direction in the original feature space, built as a weighted combination of the original features."),
            ("PC1", "“the first one”", "The direction in which the data spreads out the most."),
            ("z", "“the projected value”", "How far along the new axis a point sits. One number replacing the original n."),
            ("unsupervised", "“no y anywhere”", "PCA only looks at x. It has no idea what you plan to predict."),
        ])
        + key("""<p>The main use today is <b>visualisation</b>. A dataset with 50 features cannot be
plotted; the same data reduced to 2 components can, and a human can then see the clusters, the outliers
and the structure. That is genuinely valuable and hard to get any other way.</p>""")

        + h2("🌍", "The country example from the lecture")
        + """<p>Andrew’s example: a table of countries with GDP, population, GDP per person, life
expectancy, human development index — dozens of columns. Nobody can look at that.</p>
<p>Run PCA down to two components and plot it, and you get a map where the horizontal axis turns out to
correspond roughly to “size of the economy” and the vertical to “GDP per person”. Countries cluster
visibly. Nobody defined those axes — they fell out of the data.</p>"""
        + warn("""<p>Note the hedge: the axes “turn out to correspond roughly to”. PCA gives you directions,
not names. Interpreting them is your judgement, and it is easy to over-read.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("You have length in cm and length in inches. How many principal components carry real information?",
             "<p><b>One.</b> The second direction contains only floating-point noise — the two features "
             "are the same fact twice.</p>"),
            ("Why is PCA unsupervised?",
             "<p>Because it uses only x. It finds directions of spread without any knowledge of what you "
             "want to predict — which is also its main weakness for supervised tasks.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("docs", "https://setosa.io/ev/principal-component-analysis/",
             "Explained Visually — Principal Component Analysis",
             "Interactive, and the single best explanation of PCA on the internet. Drag the 3-D data around."),
            ("video", "https://www.youtube.com/watch?v=FgakZw6K1QQ",
             "StatQuest — PCA, step by step",
             "Twenty minutes, and the eigenvector part finally makes sense."),
        ])
    )))

# ============================================================ 14
L.append(dict(
    slug="14-pca-algorithm", title="The PCA algorithm", mins=16, tag="optional",
    lede="Pick the axis that keeps the most spread. That single sentence defines it — and it is not the "
         "same thing as linear regression.",
    body=(
        pretest("""<p>You may rotate the axis to any angle. <b>Guess what makes one angle better than another</b>, if the goal is to lose as little information as possible.</p>""",
        """<p>Watch for spread meaning information, and for why PCA is not the same as linear regression.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Shine a torch at a crowd of people and look at their shadows on the wall.</p>
<p>From one angle, everyone’s shadow lands on top of everyone else’s — you have lost all the information
about who is where.</p>
<p>From another angle, the shadows are nicely spread out and you can still tell people apart.</p>
<p>PCA rotates the torch until the shadows are <b>as spread out as possible</b>. Spread means information
kept.</p>""")

        + lenses(
            """<p>Turning a wire sculpture in your hand until it shows its widest face, then tracing its shadow on
the wall.</p>
<p>Two steps, in order, and they cannot be swapped. First find the best angle. Then flatten. The
shadow is smaller than the sculpture and still recognisable, precisely because you turned it
first.</p>""",
            """<p>Formally: the principal components are the eigenvectors of the covariance matrix, ordered by
eigenvalue, and in practice everyone computes them with an SVD instead because it is numerically
better behaved.</p>
<p>If you met eigenvectors as “the directions a matrix does not rotate”, this is the payoff — the
covariance matrix's own directions are the axes the data was secretly using all along.</p>""",
            """<p>An arrow, and a point dropping perpendicularly onto it.</p>
<p>The projection is one number: how far along the arrow the foot of that perpendicular lands. It is
a dot product, and if the arrow has unit length it is <em>only</em> a dot product. Everything else in
the algorithm is choosing which arrow.</p>""",
            """<p>The mandatory step is the one people skip: <b>scale the features first</b>. PCA maximises
variance, and variance has units.</p>
<p>Leave a salary column in pounds next to an age column in years and the first component will be
“salary”, every time, regardless of structure. Nothing warns you. The output looks perfectly
reasonable and is worthless.</p>""",
            """So the three steps below — normalise, find the directions, project — are the sculpture, the turn and
the shadow.""")

        + h2("🎬", "Watch it move")
        + demo("pcaalgo", "Rotate the axis and watch the variance",
               "the curve on the right is variance-kept against angle — PCA finds its maximum")

        + h2("🔢", "The steps")
        + """<ol>
<li><b>Mean-normalise</b> every feature (subtract its mean), and usually scale them to comparable ranges.</li>
<li>Compute the <b>covariance matrix</b> of the data.</li>
<li>Its <b>eigenvectors</b> are the principal components; their <b>eigenvalues</b> say how much variance
each one captures. Sort by eigenvalue, largest first.</li>
<li><b>Project</b>: z = x · u, for each component u you decided to keep.</li>
</ol>"""
        + decode([
            ("mean normalisation", "“centre it first”", "Mandatory. PCA measures spread <em>about the mean</em>; without centring, the first component just points at where the data happens to sit."),
            ("feature scaling", "“comparable ranges”", "Also usually necessary. A feature in dollars will otherwise dominate one in years purely by unit choice."),
            ("eigenvector", "“a direction the data likes”", "A direction that the covariance matrix stretches without rotating. Do not worry if that is opaque — the demo shows what it means."),
            ("eigenvalue", "“how much spread that direction has”", "The variance captured by that component. This is what gets sorted."),
            ("projection", "“the shadow”", "z = x · u. The distance along the new axis. This is your new, shorter feature vector."),
            ("reconstruction", "“the approximate x back”", "x̂ = z · u. It will not be exactly x — the discarded components are gone for good."),
        ])
        + key("""<p>PCA is often confused with linear regression. They are genuinely different: <b>linear
regression minimises vertical distance to a label y; PCA minimises perpendicular distance and has no
label at all.</b> Different error, different problem, different answer.</p>""")

        + h2("🔬", "Two ways to say the same thing")
        + grid2(
            card("<h3>Maximise the variance kept</h3><p>Find the direction along which the projected points "
                 "are most spread out. Spread = information retained.</p>"),
            card("<h3>Minimise the reconstruction error</h3><p>Find the direction that loses the least when "
                 "you squash onto it and try to rebuild.</p>"))
        + """<p>These are the same optimisation problem written two ways — total variance is fixed, so
whatever is not kept is exactly what is lost. Different textbooks lead with different halves.</p>"""

        + h2("🧮", "PCA on two correlated features")
        + """<p>Take two standardised features from the anomaly data set that correlate at
<b>0.90</b> — they largely say the same thing. Compute the covariance matrix and its eigenvalues:</p>"""
        + table(["Component", "eigenvalue", "variance explained"],
                [["first", "<b>1.921</b>", "<b>95.1%</b>"],
                 ["second", "0.099", "4.9%"]])
        + """<p>The first axis comes out as <b>[0.704, 0.711]</b> — very nearly the 45° diagonal,
which is exactly where you would draw a line through a cloud of points that rises at 45°. Project
onto that one axis and you keep 95.1% of the variance while halving the number of features. The
discarded direction is the perpendicular scatter about the diagonal, which was mostly noise.</p>"""
        + warn("""<p>Now the honest counterexample. Run the same procedure on all 11 features of that
data set and the variance explained comes out as 0.121, 0.113, 0.103, 0.100, 0.094 … — almost
perfectly flat, needing <b>all 11</b> components to reach 95%. PCA compresses <em>correlated</em>
features. When features are already independent there is no redundancy to remove, and PCA correctly
tells you so by refusing to concentrate the variance anywhere.</p>""")
        + explain("""<p>The first component landed on the diagonal rather than on either original
axis. <b>Why is the direction of greatest variance the right thing to keep?</b></p>""",
                  """<p>Because variance is where the differences between examples live. A direction
along which every point has nearly the same value distinguishes nothing — drop it and you lose
almost no ability to tell examples apart. The diagonal is where these points actually spread out,
so a single number measuring position along it recovers most of what the two original numbers told
you. “Greatest variance” and “most information about which point is which” are the same criterion,
which is why the eigenvector of the largest eigenvalue is the axis to keep.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Skipping mean normalisation.</b> The first component then points from the origin
towards the data cloud, which tells you nothing you did not already know.</p>""")
        + trap("""<p><b>Skipping feature scaling.</b> Whichever feature has the biggest numeric range wins,
purely because of its units. Salary in dollars will always beat age in years.</p>""")
        + trap("""<p><b>Reading meaning into the components.</b> They are directions of maximum variance,
not concepts. Any interpretation is your inference, not the algorithm’s output.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("What is the difference between PCA and linear regression?",
             "<p>Linear regression minimises <b>vertical</b> distance to a target y. PCA minimises "
             "<b>perpendicular</b> distance and has no y at all. They produce different lines on the "
             "same data.</p>"),
            ("Why must you mean-normalise before PCA?",
             "<p>Because variance is measured about the mean. Uncentred, the largest component simply "
             "points at the data's location rather than its spread.</p>"),
            ("Data spreads mostly along a 45° diagonal. What is PC1?",
             "<p>Roughly the unit vector at 45°, i.e. [0.707, 0.707]. PC2 is perpendicular to it — "
             "components are always mutually orthogonal.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("docs", "https://setosa.io/ev/principal-component-analysis/",
             "Explained Visually — PCA",
             "Interactive. Rotate the axes yourself and watch the variance move."),
            ("book", "https://web.stanford.edu/~boyd/vmls/",
             "Boyd & Vandenberghe — Introduction to Applied Linear Algebra",
             "Free. Chapter 5 covers the linear algebra that makes eigenvectors feel obvious rather than magical."),
            ("paper", "https://arxiv.org/abs/1404.1100",
             "Shlens (2014) — A Tutorial on Principal Component Analysis",
             "The clearest derivation there is. Twelve pages, and it builds it twice — via variance and via SVD."),
        ])
    )))

# ============================================================ 15
L.append(dict(
    slug="15-pca-in-code", title="PCA in code", mins=8, tag="optional",
    lede="Four lines of scikit-learn — plus the honest modern assessment of when PCA is worth using at all.",
    body=(
        pretest("""<p>scikit-learn does PCA in three lines. <b>Guess what you must do to the data first</b>, and why skipping it silently ruins the result.</p>""",
        """<p>Watch for the mandatory centring step, and for what the explained-variance ratio tells you.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Four lines. One to say how many directions you want to keep, one to look at the
data and find them, one to squash the data down onto them, and one to ask how much you lost.</p>
<p>The interesting part of this lesson is not the code — it is the last section, which argues
that two of the three classic reasons for using PCA no longer hold. Read the code, then read that.</p>""")

        + lenses(
            """<p>Reading the label on a tin before you eat what is in it. The interesting number here is not the
output of the transform — it is <b>how much you threw away</b>.</p>
<p>Two components that keep 95% of the variation are a good trade. Two that keep 34% mean you have
flattened something that genuinely needed three dimensions, and everything downstream is now working
from a bad photograph.</p>""",
            """<p><code>explained_variance_ratio_</code> is a scree plot in an array, and the elbow you look for is
the same elbow you learned to look for when choosing <var>k</var> in k-means last week.</p>
<p>Same judgement, same picture, different algorithm — which is worth noticing, because it is one of
the few genuinely reusable habits in unsupervised learning.</p>""",
            """<p>An array of numbers that sums to 1: <code>[0.71, 0.24, 0.03, 0.02]</code>.</p>
<p>Read it as “the first direction carries 71% of the variation”. Add them up as you go and stop when
the running total is high enough. That cumulative sum is the only number in this lesson worth
memorising how to read.</p>""",
            """<p>The failure that costs real money is fitting the transform on the <em>whole</em> dataset before
splitting into train and test.</p>
<p>It leaks test-set structure into the training features, the validation score comes out flattering,
and the model disappoints in production. Fit on train, apply to test — the same discipline as feature
scaling in C1, and broken just as often.</p>""",
            """So the three lines below are ordinary. The fourth line, the one that prints the explained variance,
is the one that tells you whether to trust the other three.""")

        +h2("💻", "In code")
        + code("""
from sklearn.decomposition import PCA

pca = PCA(n_components=2)             # how many components to keep
X_reduced = pca.fit_transform(X)      # fit AND project, in one call

print(pca.explained_variance_ratio_)  # e.g. [0.62, 0.21] -> 83% of the spread kept
X_approx = pca.inverse_transform(X_reduced)   # an approximate reconstruction
""")
        + decode([
            ("<code>fit_transform</code>", "“learn the axes and project”", "<code>fit</code> finds the components; <code>transform</code> projects. Combined for convenience."),
            ("<code>explained_variance_ratio_</code>", "“how much each component keeps”", "A list summing to at most 1. The single most useful diagnostic PCA gives you."),
            ("<code>inverse_transform</code>", "“undo it, approximately”", "Maps back to the original space. The discarded components are gone, so it is not exact."),
            ("<code>n_components=0.95</code>", "“keep 95% of the variance”", "sklearn also accepts a fraction, and picks the number of components for you."),
        ], head=("Call", "Say it out loud", "What it does"))
        + warn("""<p>Fit the PCA on the <b>training set only</b>, then <code>transform</code> the
cross-validation and test sets with the same fitted object. Fitting on everything leaks test information
into training — exactly the same rule as feature scaling.</p>""")

        + h2("🎬", "Watch it move")
        + demo("pcacode", "Explained variance, and how many components to keep",
               "the cumulative percentage is what decides where you stop")

        + h2("🔢", "How many components?")
        + table(["Purpose", "How many", "Why"],
                [["<b>visualisation</b>", "2, or 3", "because that is what you can plot"],
                 ["<b>compression</b>", "enough for 90–99% of the variance", "a defensible amount of information kept"],
                 ["<b>speeding up a model</b>", "—", "rarely worth it now (see below)"]])

        + h2("🕰", "The honest modern assessment")
        + """<p>PCA used to be routinely recommended for two things beyond visualisation: compressing data
to save storage, and reducing features to speed up supervised learning. Andrew is explicit in this lecture
that <b>both uses have faded</b>.</p>
<ul>
<li><b>Compression:</b> storage is cheap now. It was a real concern when disks were measured in megabytes.</li>
<li><b>Speeding up training:</b> modern hardware and good regularisation handle high-dimensional inputs
well. Deep learning in particular does its own feature reduction internally, and usually does it better
than PCA — because PCA has never seen your labels and cannot know which directions actually matter for
prediction.</li>
</ul>
<p>Visualisation, on the other hand, remains genuinely useful and has no good substitute.</p>"""
        + note("""<p>For 2-D visualisation specifically, <b>t-SNE</b> and <b>UMAP</b> usually produce much
more legible cluster structure than PCA. They are non-linear, slower, and their distances between clusters
should not be over-interpreted — but for “show me the shape of this data”, they are the modern default.
PCA remains the right choice when you need a fast, linear, invertible transform.</p>""",
               "What people use instead, for plotting")

        + h2("✅", "Check yourself")
        + quiz([
            ("explained_variance_ratio_ is [0.5, 0.3, 0.1, 0.05]. How many components for 90%?",
             "<p>0.5 + 0.3 + 0.1 = 0.9, so <b>3 components</b>.</p>"),
            ("Why fit PCA on the training set only?",
             "<p>Because fitting uses the data's covariance. Including test data leaks information about "
             "it into the transform — the same rule as for scalers.</p>"),
            ("Why has PCA fallen out of favour for speeding up supervised learning?",
             "<p>Compute got cheap, regularisation handles extra features well, and PCA discards "
             "directions using no knowledge of y — so it can throw away exactly the low-variance "
             "direction that predicts your label.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("docs", "https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html",
             "sklearn.decomposition.PCA",
             "Including <code>n_components</code> as a fraction, and <code>svd_solver</code> for large data."),
            ("docs", "https://umap-learn.readthedocs.io/en/latest/",
             "UMAP — Uniform Manifold Approximation and Projection",
             "The modern default for 2-D visualisation of high-dimensional data. Read the “how to use” caveats."),
            ("paper", "https://distill.pub/2016/misread-tsne/",
             "Distill — How to Use t-SNE Effectively",
             "Interactive, and essential if you ever plot with t-SNE. Cluster sizes and distances mean much less than they appear to."),
        ])
    )))

WEEK = dict(
    course="C3", week=2, title="Recommender Systems",
    time="~7–9 h with labs",
    goal="Build collaborative filtering from scratch, extend it to binary labels and content features, "
         "scale it to large catalogues with a two-tower network — and reduce dimensions with PCA.",
    lessons=L,
)
