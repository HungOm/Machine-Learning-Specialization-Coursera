# -*- coding: utf-8 -*-
"""The datasets the lessons actually name — generated, and committed.

Every code block on this site that says `pd.read_csv('houses.csv')` now has a
real houses.csv to read. The files live in study/data/ so they are served by
the site itself and fetchable by raw URL, which means a lesson can be run
without downloading anything at all:

    df = pd.read_csv(DATA + 'houses.csv')

Two kinds of file live here:

  generated  — built by the make_* functions below from a seeded RNG, so the
               shapes in the lessons ((1000, 5), (200, 3)) are true by
               construction and rerunning this file reproduces them byte for
               byte.
  course     — real data that already ships with the Coursera notebooks in this
               repository, copied to one clean path (and, for the recommender,
               reshaped from a dense 8 MB matrix into a tidy 25k-row table).

Run:  python3 study/_build/datakit.py
"""
import csv
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                       # study/
REPO = os.path.dirname(ROOT)
OUT = os.path.join(ROOT, "data")

RAW = ("https://raw.githubusercontent.com/HungOm/"
       "Machine-Learning-Specialization-Coursera/main/study/data/")


# ---------------------------------------------------------------- generated
def make_houses():
    """1000 houses, five columns — the file F0 W2 lessons 13 and 14 read.

    Calibrated against the real 99-house dataset in C1 W2's optional lab
    (size 788-3194 sqft, price 158-718 thousand), so the numbers feel like that
    data rather than like noise. Price is a genuine linear function of the four
    features plus noise, which matters: gradient descent run on this file
    converges to weights close to the ones written below, and the wildly
    different column scales are what makes the feature-scaling lesson bite.
    """
    rng = np.random.default_rng(11)
    m = 1000

    size = np.clip(rng.lognormal(np.log(1350), 0.34, m), 720, 3400).round()
    # bedrooms track size, loosely — bigger house, more rooms, but not exactly
    beds = np.clip(np.round(size / 620 + rng.normal(0, 0.55, m)), 1, 5)
    floors = np.where(size > 1500 + rng.normal(0, 400, m), 2.0, 1.0)
    age = np.clip(rng.gamma(2.6, 15.0, m), 1, 100).round()

    price = (0.182 * size + 11.5 * beds + 14.0 * floors - 1.05 * age
             + 88.0 + rng.normal(0, 24.0, m))
    price = np.clip(price, 95, None).round(1)

    rows = [("size", "beds", "floors", "age", "price")]
    for s, b, f, a, p in zip(size, beds, floors, age, price):
        rows.append((int(s), int(b), int(f), int(a), p))
    return rows


def make_houses_messy(clean):
    """The same 1000 houses, with this lesson's three traps actually present.

    The traps section of F0 W2 lesson 13 warns about a KeyError from a
    mis-cased column, a numeric column that arrived as text, and missing
    values. Reading about them does nothing; hitting them does. So:

      * 'price' is spelled 'Price'  -> df['price'] raises KeyError
      * 'beds ' carries a trailing space -> so does df['beds']
      * 'size' holds four non-numeric strings -> the column is dtype object
      * 41 cells in floors and age are empty -> df.isnull().sum() is non-zero

    The four bad size values are deliberately NOT "N/A": pandas reads that as a
    missing value, which would quietly give you a clean float column and hide
    the trap the lesson is about. "1,240" (a thousands separator, the single
    most common way a real spreadsheet export poisons a numeric column) and
    "unknown" are not in read_csv's na_values list, so the column really does
    arrive as text.

    Everything else is identical to houses.csv, so a learner can fix the file
    and diff it against the clean one.
    """
    rng = np.random.default_rng(12)
    body = [list(r) for r in clean[1:]]
    m = len(body)

    bad = rng.choice(m, 4, replace=False)
    for i in bad[:2]:
        body[i][0] = "{:,}".format(body[i][0])      # 1,240 — a spreadsheet export
    for i in bad[2:]:
        body[i][0] = "unknown"
    for i in rng.choice(m, 18, replace=False):
        body[i][2] = ""
    for i in rng.choice(m, 23, replace=False):
        body[i][3] = ""

    return [("size", "beds ", "floors", "age", "Price")] + [tuple(r) for r in body]


def make_coffee():
    """200 roasts — the C2 W1 example, reproduced from the lab's own generator.

    This is load_coffee_data() from C2_W1_Lab02, not an imitation of it: same
    rule, same ranges, so the decision boundary the lesson draws is the
    boundary in this file. Temperature is in degrees Celsius and duration in
    minutes, and the 200-vs-17 scale gap between them is exactly why that
    lesson reaches for a Normalization layer.
    """
    rng = np.random.default_rng(2)
    X = rng.random(400).reshape(-1, 2)
    X[:, 1] = X[:, 1] * 4 + 11.5                 # duration, minutes
    X[:, 0] = X[:, 0] * (285 - 150) + 150        # temperature, celsius

    rows = [("temperature", "duration", "good_roast")]
    for t, d in X:
        y = -3.0 / (260 - 175) * t + 21
        good = int(175 < t < 260 and 12 < d < 15 and d <= y)
        rows.append((round(t, 2), round(d, 2), good))
    return rows


# ---------------------------------------------------------------- from the repo
def read_course(rel):
    return list(csv.reader(open(os.path.join(REPO, rel), encoding="utf-8")))


def make_houses_lab():
    """The real 99 houses from C1 W2's optional lab, given a header row.

    houses.txt on disk is headerless and written in scientific notation, which
    is why nobody opens it. Same numbers, readable."""
    src = read_course("C1 - Supervised Machine Learning - Regression and "
                      "Classification/week2/Optional Labs/data/houses.txt")
    rows = [("size", "beds", "floors", "age", "price")]
    for r in src:
        s, b, f, a, p = (float(v) for v in r)
        rows.append((int(s), int(b), int(f), int(a), round(p, 1)))
    return rows


def make_heart():
    """918 patients, 12 columns — the tree-ensemble lab's data, unchanged.

    Copied verbatim so `pd.get_dummies(df, columns=['ChestPainType'])` from the
    one-hot lesson has something to run on."""
    return [tuple(r) for r in
            read_course("C2 - Advanced Learning Algorithms/week4/optional labs/heart.csv")]


def make_movies():
    """The C3 W2 MovieLens slice, turned from two dense matrices into one
    tidy table of the ratings that actually exist.

    The lesson makes a point of it: 4,778 films x 443 users is 2.1 million
    cells and almost all of them are empty. The lab stores that as an 8.5 MB
    grid of zeros. Stored the way the point describes it — one row per rating
    that was actually given — the same data is a twentieth of the size, and the
    sparsity stops being a claim you have to take on trust.

    Returns (movies_rows, ratings_rows).
    """
    Y = np.loadtxt(os.path.join(
        REPO, "C3 - Unsupervised Learning, Recommenders, Reinforcement Learning/"
              "week2/C3W2/C3W2A1/data/small_movies_Y.csv"), delimiter=",")
    R = np.loadtxt(os.path.join(
        REPO, "C3 - Unsupervised Learning, Recommenders, Reinforcement Learning/"
              "week2/C3W2/C3W2A1/data/small_movies_R.csv"), delimiter=",")
    lst = read_course("C3 - Unsupervised Learning, Recommenders, Reinforcement "
                      "Learning/week2/C3W2/C3W2A1/data/small_movie_list.csv")[1:]

    movies = [("movieId", "title", "mean_rating", "n_ratings")]
    for mid, mean, n, title in lst:
        movies.append((int(mid), title, float(mean), int(n)))

    ratings = [("userId", "movieId", "rating")]
    mi, ui = np.nonzero(R)
    for i, u in zip(mi, ui):
        ratings.append((int(u), int(i), round(float(Y[i, u]), 1)))

    # The tidy table is only worth having if it is lossless. Pivot it straight
    # back and compare against the lab's own dense matrix: if this ever fails,
    # the small file is not the same data and should not be published as if it
    # were. Cheap insurance, and it runs every time the file is regenerated.
    back = np.zeros_like(Y)
    for u, i, r in ratings[1:]:
        back[i, u] = r
    assert np.allclose(back, Y), "ratings.csv does not round-trip to small_movies_Y.csv"

    return movies, ratings


# ---------------------------------------------------------------- the registry
# Everything the data page renders comes from here: nothing about a dataset is
# written twice, so the shape shown on the page is the shape of the file.
C = lambda name, kind, unit, what: dict(name=name, kind=kind, unit=unit, what=what)

DATASETS = [
    dict(
        file="houses.csv", origin="generated",
        title="Houses",
        blurb="Four things about a house and what it sold for. The file every "
              "<code>pd.read_csv('houses.csv')</code> on this site is reading — the "
              "one dataset you meet before you have met a model.",
        why="Price really is a linear function of the four features plus noise, so "
            "gradient descent on it converges to something sensible rather than to "
            "mush — and <code>size</code> runs in the thousands while <code>beds</code> "
            "runs 1&ndash;5, which is the whole argument for feature scaling sitting "
            "in one file.",
        columns=[
            C("size", "int", "square feet", "floor area — 720 to 3,400"),
            C("beds", "int", "count", "bedrooms, 1 to 5 — tracks size, loosely"),
            C("floors", "int", "count", "1 or 2"),
            C("age", "int", "years", "1 to 100"),
            C("price", "float", "$ thousands", "what it sold for — this is <b>y</b>"),
        ],
        snippet="""
import pandas as pd

df = pd.read_csv('houses.csv')

df.shape        # (1000, 5)
df.head()
df.describe()

X = df[['size', 'beds', 'floors', 'age']].to_numpy()   # (1000, 4)
y = df['price'].to_numpy()                             # (1000,)
""",
        used=[("f0/w2-13-pandas-dataframes.html", "F0 W2 · pandas DataFrames"),
              ("f0/w2-14-pandas-to-numpy.html", "F0 W2 · From pandas to NumPy"),
              ("c1/w2-05-feature-scaling.html", "C1 W2 · Feature scaling")],
    ),
    dict(
        file="houses_messy.csv", origin="generated",
        title="Houses, as it would really arrive",
        blurb="The same 1,000 houses with the three traps from the pandas lesson "
              "actually in the file, so you hit them instead of reading about them.",
        why="<code>df['price']</code> raises <code>KeyError</code> — the column is "
            "spelled <code>Price</code>. <code>df['beds']</code> raises it too — that "
            "one has a trailing space. <code>size</code> comes back as dtype "
            "<code>object</code> — four cells hold text, two of them numbers a "
            "spreadsheet helpfully wrote as <code>1,240</code> — so <code>.mean()</code> "
            "fails outright. And 41 cells are simply empty. "
            "<code>df.columns</code>, <code>df.info()</code> and "
            "<code>df.isnull().sum()</code> find all four in about ten seconds; the "
            "point of the file is to make that ten seconds a habit.",
        columns=[
            C("size", "object ⚠", "square feet",
              "4 cells are text: two written <code>1,240</code>, two <code>unknown</code>"),
            C("beds&nbsp;", "int", "count", "note the <b>trailing space</b> in the name"),
            C("floors", "float ⚠", "count", "18 missing"),
            C("age", "float ⚠", "years", "23 missing"),
            C("Price", "float", "$ thousands", "note the <b>capital P</b>"),
        ],
        snippet="""
df = pd.read_csv('houses_messy.csv')

df.columns          # look here first — the names are not what you assumed
df.info()           # size is 'object', not int64. Why?
df.isnull().sum()   # floors 18, age 23

# the fix, once you have seen what is wrong
df.columns = df.columns.str.strip().str.lower()
df['size'] = pd.to_numeric(df['size'], errors='coerce')
df = df.dropna()
df.shape            # (956, 5)
""",
        used=[("f0/w2-13-pandas-dataframes.html", "F0 W2 · pandas DataFrames"),
              ("f0/w2-15-reading-errors.html", "F0 W2 · Reading errors")],
    ),
    dict(
        file="coffee.csv", origin="generated",
        title="Coffee roasting",
        blurb="Temperature, duration, and whether the roast came out good — the "
              "running example for the whole of C2 W1.",
        why="Two features, one binary label, and a decision boundary that no straight "
            "line can draw: good roasts sit inside a triangle, which is why this is "
            "the example a network is introduced on. It is also the scale problem in "
            "miniature — 150&ndash;285 against 11.5&ndash;15.5, which is what the "
            "<code>Normalization</code> layer in that lab is there to fix.",
        columns=[
            C("temperature", "float", "°C", "150 to 285"),
            C("duration", "float", "minutes", "11.5 to 15.5"),
            C("good_roast", "int", "0 or 1", "the label — this is <b>y</b>"),
        ],
        snippet="""
df = pd.read_csv('coffee.csv')

X = df[['temperature', 'duration']].to_numpy()   # (200, 2)
y = df['good_roast'].to_numpy()                  # (200,)

y.mean()        # about 0.21 — good roasts are the minority
""",
        used=[("c2/w1-09-building-a-network-sequential.html", "C2 W1 · Building a network with Sequential"),
              ("c2/w1-04-neural-network-layer.html", "C2 W1 · The neural network layer")],
    ),
    dict(
        file="houses_lab.csv", origin="course",
        title="Houses (the real 99)",
        blurb="The actual dataset behind C1 W2's optional labs, with a header row "
              "added and the scientific notation unwound.",
        why="Same five columns as <code>houses.csv</code>, one twentieth the size, and "
            "real. Worth running the same code on both: the fitted weights land in the "
            "same place, and the noisier picture on 99 rows is what a small dataset "
            "looks like.",
        columns=[
            C("size", "int", "square feet", "788 to 3,194"),
            C("beds", "int", "count", "0 to 4"),
            C("floors", "int", "count", "1 or 2"),
            C("age", "int", "years", "12 to 107"),
            C("price", "float", "$ thousands", "158 to 718"),
        ],
        snippet="""
df = pd.read_csv('houses_lab.csv')
df.shape        # (100, 5)
""",
        used=[("c1/w2-05-feature-scaling.html", "C1 W2 · Feature scaling"),
              ("c1/w2-08-feature-engineering.html", "C1 W2 · Feature engineering")],
    ),
    dict(
        file="heart.csv", origin="course",
        title="Heart failure",
        blurb="918 patients, eleven measurements and one diagnosis — the dataset the "
              "decision tree and tree-ensemble labs use.",
        why="The first dataset here with <b>categorical</b> columns "
            "(<code>ChestPainType</code>, <code>ST_Slope</code>, "
            "<code>RestingECG</code>), which is what makes the one-hot encoding lesson "
            "necessary. It is also the one where a tree beats a neural network, which "
            "is the point C2 W4 closes on.",
        columns=[
            C("Age", "int", "years", ""),
            C("Sex", "text", "M / F", "categorical"),
            C("ChestPainType", "text", "ATA / NAP / ASY / TA", "categorical — four values"),
            C("RestingBP", "int", "mm Hg", "resting blood pressure"),
            C("Cholesterol", "int", "mm/dl", ""),
            C("FastingBS", "int", "0 or 1", "fasting blood sugar &gt; 120 mg/dl"),
            C("RestingECG", "text", "Normal / ST / LVH", "categorical"),
            C("MaxHR", "int", "bpm", "maximum heart rate reached"),
            C("ExerciseAngina", "text", "Y / N", "categorical"),
            C("Oldpeak", "float", "—", "ST depression"),
            C("ST_Slope", "text", "Up / Flat / Down", "categorical"),
            C("HeartDisease", "int", "0 or 1", "the label — this is <b>y</b>"),
        ],
        snippet="""
df = pd.read_csv('heart.csv')
df.shape        # (918, 12)

cat = ['Sex', 'ChestPainType', 'RestingECG', 'ExerciseAngina', 'ST_Slope']
df = pd.get_dummies(df, columns=cat)
df.shape        # (918, 21) -- one column per category value
""",
        used=[("c2/w4-06-one-hot-encoding.html", "C2 W4 · One-hot encoding"),
              ("c2/w4-12-xgboost.html", "C2 W4 · XGBoost")],
    ),
    dict(
        file="ratings.csv", origin="course",
        title="MovieLens ratings",
        blurb="Every rating that was actually given — one row each, instead of a "
              "4,778 × 443 grid that is 98.1% zeros.",
        why="The recommender lessons keep saying that 2.1 million cells hold only about "
            "thirty-nine thousand ratings. The lab stores that as an 8.5 MB dense "
            "matrix; here it is the shape the sentence describes, at a twentieth of "
            "the size. Pivot it back with one line when you need the matrix.",
        columns=[
            C("userId", "int", "0–442", "who rated"),
            C("movieId", "int", "0–4777", "joins to <code>movies.csv</code>"),
            C("rating", "float", "0.5–5.0", "in half-star steps"),
        ],
        snippet="""
ratings = pd.read_csv('ratings.csv')
movies  = pd.read_csv('movies.csv')

ratings.shape                       # (39253, 3) -- the ratings that exist

# back to the dense Y and R the lab uses, in two lines
Y = ratings.pivot(index='movieId', columns='userId',
                  values='rating').reindex(range(4778)).fillna(0).to_numpy()
R = (Y > 0).astype(int)
Y.shape, R.mean()                   # ((4778, 443), 0.0185)
""",
        used=[("c3/w2-03-collaborative-filtering.html", "C3 W2 · Collaborative filtering"),
              ("c3/w2-05-mean-normalization.html", "C3 W2 · Mean normalization")],
    ),
    dict(
        file="movies.csv", origin="course",
        title="MovieLens titles",
        blurb="The 4,778 films, so a recommendation comes back as a name rather than "
              "as row 2,143.",
        why="Joins to <code>ratings.csv</code> on <code>movieId</code>. Keep it to hand "
            "while training the recommender — reading your own predictions as titles is "
            "the fastest sanity check there is on whether it learned anything.",
        columns=[
            C("movieId", "int", "0–4777", "the join key"),
            C("title", "text", "", "with the year, e.g. <code>Toy Story (1995)</code>"),
            C("mean_rating", "float", "0.5–5.0", "average across users who rated it"),
            C("n_ratings", "int", "count", "how many rated it — as few as 1"),
        ],
        snippet="""
movies = pd.read_csv('movies.csv')

# the 10 best-rated films with a decent number of ratings behind them
(movies[movies.n_ratings > 20]
       .sort_values('mean_rating', ascending=False)
       .head(10))
""",
        used=[("c3/w2-03-collaborative-filtering.html", "C3 W2 · Collaborative filtering")],
    ),
]

BY_FILE = {d["file"]: d for d in DATASETS}


# ---------------------------------------------------------------- writing
def write(name, rows):
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8", newline="") as f:
        csv.writer(f, lineterminator="\n").writerows(rows)
    return path


def build():
    os.makedirs(OUT, exist_ok=True)
    houses = make_houses()
    movies, ratings = make_movies()
    made = [
        ("houses.csv", houses),
        ("houses_messy.csv", make_houses_messy(houses)),
        ("coffee.csv", make_coffee()),
        ("houses_lab.csv", make_houses_lab()),
        ("heart.csv", make_heart()),
        ("ratings.csv", ratings),
        ("movies.csv", movies),
    ]
    total = 0
    for name, rows in made:
        path = write(name, rows)
        d = BY_FILE[name]
        d["rows"] = len(rows) - 1
        d["cols"] = len(rows[0])
        d["bytes"] = os.path.getsize(path)
        total += d["bytes"]
        print("  %-18s %6d x %-3d %8.1f KB" % (name, d["rows"], d["cols"], d["bytes"] / 1024))
    print("  %d files, %.1f KB total -> study/data/" % (len(made), total / 1024))
    return DATASETS


def measure():
    """Shapes and sizes read back off disk — what the data page renders.

    Read rather than remembered, so the page cannot claim a shape the file does
    not have."""
    for d in DATASETS:
        path = os.path.join(OUT, d["file"])
        if not os.path.exists(path):
            d["rows"], d["cols"], d["bytes"] = 0, 0, 0
            continue
        with open(path, encoding="utf-8", newline="") as f:
            r = csv.reader(f)
            d["cols"] = len(next(r))
            d["rows"] = sum(1 for _ in r)
        d["bytes"] = os.path.getsize(path)
    return DATASETS


def check():
    """Execute every snippet the data page shows, against the files on disk.

    The page promises that its code runs as written. That is only worth
    printing if something checks it, so:  python3 study/_build/datakit.py check
    """
    import traceback
    import pandas as pd  # noqa: F401  (the snippets use it)

    cwd = os.getcwd()
    os.chdir(OUT)
    bad = 0
    try:
        for d in DATASETS:
            src = d["snippet"].strip()
            try:
                exec(compile(src, d["file"], "exec"), {"pd": pd, "np": np})
                print("  ok    %-18s (%d lines)" % (d["file"], len(src.splitlines())))
            except Exception:
                bad += 1
                print("  FAIL  %s" % d["file"])
                traceback.print_exc(limit=2)
    finally:
        os.chdir(cwd)
    print("  %d/%d snippets run against the real files"
          % (len(DATASETS) - bad, len(DATASETS)))
    return bad


if __name__ == "__main__":
    import sys
    if "check" in sys.argv[1:]:
        raise SystemExit(1 if check() else 0)
    build()
