# -*- coding: utf-8 -*-
"""C1 · Week 1 — Introduction, linear regression, gradient descent."""
from kit import (kid, key, warn, trap, note, card, eq, eqp, decode, table, demo,
                 quiz, links, code, h2, grid2, grid3, pretest)

REPO = "../../C1%20-%20Supervised%20Machine%20Learning%20-%20Regression%20and%20Classification"
L = []

# ============================================================ 1
L.append(dict(
    slug="01-what-is-machine-learning", title="What is machine learning?", mins=8, tag="intuition",
    lede="The definition, the one big split that organises everything that follows, and why this is worth "
         "three courses of your time.",
    body=(
        pretest("""<p>You want a program that decides whether a photo shows your grandmother. Try, right now, to write down the <b>rule</b> it should follow — in words, precisely enough that someone could code it.</p>""",
                """<p>If you got stuck, that is the point. Watch for <b>why the stuckness matters</b>: this lesson argues the whole field exists because some rules cannot be written down, only demonstrated with examples.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Normally you tell a computer <b>exactly</b> what to do: “if the price is over £50, add a
delivery charge.” Every rule, written out by a person.</p>
<p>Machine learning is different. You show it <b>examples</b> — a thousand houses and what each one sold
for — and it works out the rule itself.</p>
<p>That matters for problems where nobody can write the rule down. Nobody can explain, step by step, how
they recognise their grandmother’s face. But everyone can supply examples.</p>""")

        + h2("🎬", "Watch it move")
        + demo("whatisml", "The definition, and the two branches",
               "supervised on one side, unsupervised on the other — that split organises the whole specialization")

        + h2("🔢", "Two definitions worth knowing")
        + """<p><b>Arthur Samuel, 1959:</b> “the field of study that gives computers the ability to learn
without being explicitly programmed.” Samuel wrote a checkers program that played itself tens of thousands
of times, learned which board positions tended to lead to wins, and ended up beating him.</p>
<p>The interesting question that raises: if he had let it play only ten games instead of ten thousand,
would it have been better or worse? Worse — and that intuition, that more experience helps, is the
foundation of everything here.</p>"""
        + decode([
            ("supervised learning", "“learning from answers”", "You are given examples with the right answer attached. x → y. Courses 1 and 2, and by far the most used in practice."),
            ("unsupervised learning", "“learning without answers”", "You get x only, and must find structure yourself. Course 3."),
            ("training set", "“the examples”", "The data the algorithm learns from."),
            ("model", "“the learned rule”", "The function the algorithm produces, which you then use to make predictions."),
        ])
        + key("""<p>Almost all the economic value of machine learning today comes from <b>supervised
learning</b>. That is why two of the three courses are about it, and why Course 1 spends its whole length
on two supervised algorithms.</p>""")

        + h2("🧰", "A note on tools")
        + """<p>Andrew makes a point in this week that is worth taking seriously: the algorithms are not
enough. Plenty of teams have a good algorithm and still fail, because they apply it badly — wrong data,
wrong metric, wrong problem.</p>
<p>The analogy he uses: giving someone the world’s best set of tools does not make them a good carpenter.
Course 2 Week 3 is the part of this specialization that teaches the carpentry, and it is the part
practitioners come back to most.</p>"""

        + h2("✅", "Check yourself")
        + quiz([
            ("You have 10,000 emails, each labelled spam or not spam. Supervised or unsupervised?",
             "<p><b>Supervised</b> — every example comes with its answer. Specifically it is "
             "classification, since the answer is one of two categories.</p>"),
            ("You have 10,000 news articles and want to group them by topic, with no labels. Which?",
             "<p><b>Unsupervised</b> — there is no y. This is clustering, covered in Course 3 Week 1.</p>"),
            ("Why does “without being explicitly programmed” matter?",
             "<p>Because for many valuable problems nobody can write the rules. You cannot enumerate what "
             "makes a face a face, but you can supply a million labelled photographs.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("docs", "https://developers.google.com/machine-learning/crash-course",
             "Google — Machine Learning Crash Course",
             "Free, and a good second telling of everything in Course 1. Useful when an explanation here does not land."),
            ("paper", "https://ieeexplore.ieee.org/document/5392560",
             "Samuel (1959) — Some Studies in Machine Learning Using the Game of Checkers",
             "The paper the definition comes from. Genuinely readable, and startlingly modern in places."),
            ("lab", REPO + "/week1/Optional%20Labs/C1_W1_Lab01_Python_Jupyter_Soln.ipynb",
             "Optional lab: Python and Jupyter",
             "In this repo. Ten minutes of tooling, so the notebooks later do not get in your way."),
        ])
    )))

# ============================================================ 2
L.append(dict(
    slug="02-supervised-learning", title="Supervised learning", mins=9, tag="intuition",
    lede="Learning x → y from examples with the answers attached — and the one distinction that decides "
         "everything downstream: regression or classification.",
    body=(
        pretest("""<p>Two jobs: (a) predict tomorrow's rainfall in millimetres, (b) predict whether it rains tomorrow. Same weather, same data. <b>Guess why a machine-learning person would treat these as different kinds of problem.</b></p>""",
                """<p>Watch for the word that names the split. The difference is not the subject matter — it is what <em>shape</em> the answer takes, and that single choice decides the model, the cost function and how you score it.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Imagine learning about dogs by being shown a hundred photos, each one with someone
saying “dog” or “not a dog”. After enough of them you can label a photo you have never seen.</p>
<p>That is supervised learning. Every training example arrives with its right answer, and the algorithm
learns the pattern that connects the two.</p>""")

        + h2("🎬", "Watch it move")
        + demo("supervised", "The two kinds — click between them",
               "regression predicts a number; classification predicts a category")

        + h2("🔢", "Regression vs classification")
        + table(["", "Regression", "Classification"],
                [["Predicts", "a <b>number</b>", "a <b>category</b>"],
                 ["How many possible answers", "infinitely many", "a small, finite set"],
                 ["Examples", "house price, temperature, delivery time", "spam / not spam, benign / malignant, which of 10 digits"],
                 ["Covered in", "C1 W1–2", "C1 W3"]])
        + decode([
            ("supervised", "“with answers”", "The training set contains (x, y) pairs — input and correct output."),
            ("x", "“the input / the feature”", "What you measure. House size, tumour diameter, email text."),
            ("y", "“the output / the target / the label”", "The right answer for that example."),
            ("regression", "“predict a number”", "Confusingly, “logistic regression” is a classification algorithm. Historical accident; everyone lives with it."),
            ("classification", "“predict a category”", "The categories need not be numbers. 0 and 1 are just convenient names."),
        ])
        + key("""<p>“Is my output a number or a category?” is the first question to ask about any new
problem. It decides the model, the cost function, the metric, and how you evaluate success. Getting it
wrong is not a small mistake.</p>""")

        + h2("🌍", "What this is actually used for")
        + grid3(
            card("<h3>Spam filtering</h3><p>email → spam or not. Classification, and one of the earliest "
                 "commercially successful applications.</p>"),
            card("<h3>Speech recognition</h3><p>audio → text. Technically classification, over an enormous "
                 "number of possible outputs.</p>"),
            card("<h3>Online advertising</h3><p>ad + user → will they click? Classification, and quietly "
                 "the most lucrative application of ML ever built.</p>"))

        + h2("🕳", "Traps")
        + trap("""<p><b>Encoding a category as a number and using regression.</b> Predicting “cat = 1,
dog = 2, horse = 3” with regression tells the model that a dog is between a cat and a horse. It is not.
Week 3 shows what to do instead.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("Predicting tomorrow's rainfall in millimetres. Which?",
             "<p><b>Regression</b> — the answer is a number with infinitely many possible values.</p>"),
            ("Predicting whether it will rain tomorrow. Which?",
             "<p><b>Classification</b> — two categories. Note that the same underlying situation gives "
             "different problem types depending on how you phrase the question.</p>"),
            ("Predicting which of 5 defect types a part has. Which?",
             "<p><b>Classification</b>, with five classes. Course 2 Week 2 covers the multi-class case "
             "properly.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("docs", "https://scikit-learn.org/stable/supervised_learning.html",
             "scikit-learn — supervised learning",
             "Every supervised algorithm in one place. Worth skimming the contents page to see how much sits under this one heading."),
            ("docs", "https://developers.google.com/machine-learning/crash-course/linear-regression",
             "Google Crash Course — framing supervised problems",
             "A short, careful treatment of labels, features and examples."),
        ])
    )))

# ============================================================ 3
L.append(dict(
    slug="03-unsupervised-learning", title="Unsupervised learning", mins=8, tag="intuition",
    lede="The other half of the map. No answers, no marking, just “is there structure in here?”",
    body=(
        pretest("""<p>Someone hands you 10,000 news articles with no labels of any kind and asks you to “find the stories”. <b>Before reading: how would you even check whether your answer was right?</b></p>""",
                """<p>Sit with the discomfort — there genuinely is no answer key. Watch for what replaces “correct” when there is nothing to compare against.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Someone hands you a box of mixed Lego and says nothing at all. No instructions, no
picture on the lid.</p>
<p>You still start sorting: reds here, wheels there, the long flat pieces in their own pile. Nobody told
you those were the right piles. You just noticed that some pieces belong together.</p>
<p>That is unsupervised learning. Data with no answers, and the job is to find whatever structure is
there.</p>""")

        + h2("🎬", "Watch it move")
        + demo("unsupervised", "The three kinds",
               "clustering, anomaly detection, dimensionality reduction")

        + h2("🔢", "The three families")
        + table(["Type", "The question", "Example", "Where in the specialization"],
                [["<b>clustering</b>", "which of these belong together?", "Google News grouping the same story from 20 outlets", "C3 W1"],
                 ["<b>anomaly detection</b>", "which of these is weird?", "a fraudulent transaction; a failing engine", "C3 W1"],
                 ["<b>dimensionality reduction</b>", "can I compress this without losing much?", "50 features squashed to 2 so a human can plot them", "C3 W2"]])
        + decode([
            ("unsupervised", "“no answer key”", "The dataset has only x. There is no y column at all."),
            ("structure", "“patterns in x”", "Groups, outliers, redundancy — whatever is there to be found."),
            ("no marking", "“you cannot score it”", "With no y, there is nothing to compare a prediction against. This is genuinely uncomfortable at first."),
        ])
        + key("""<p>Because there is no right answer, two different clusterings of the same data can both be
defensible. Unsupervised results are judged by whether they are <b>useful</b>, not by whether they are
correct.</p>""")

        + h2("🌍", "The DNA example")
        + """<p>Andrew’s example in the video: a genetic microarray, where each column is a person and each
row is a gene. Nobody has labelled these people as belonging to type 1, 2 or 3. The clustering algorithm
finds that they fall into groups anyway — and those groups turn out to be biologically meaningful.</p>
<p>That is the appeal of unsupervised learning: it can tell you something you did not know to ask
about.</p>"""

        + h2("✅", "Check yourself")
        + quiz([
            ("Given a large set of news articles with no labels, group them by story. Which type?",
             "<p><b>Clustering.</b> No labels, and the goal is to find groups.</p>"),
            ("You have server logs and want to find the machine behaving strangely. Which type?",
             "<p><b>Anomaly detection.</b> You are not classifying against known failure types — you are "
             "looking for the odd one out.</p>"),
            ("Why can't you compute an accuracy score for a clustering?",
             "<p>There is no y to compare against. Internal measures exist (silhouette, distortion) but "
             "they measure tightness, not correctness.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("docs", "https://scikit-learn.org/stable/unsupervised_learning.html",
             "scikit-learn — unsupervised learning",
             "The full catalogue: clustering, decomposition, outlier detection, manifold learning."),
            ("docs", "https://scikit-learn.org/stable/auto_examples/cluster/plot_cluster_comparison.html",
             "Comparing clustering algorithms",
             "One figure showing where K-means works and where it does not. Thirty seconds well spent."),
        ])
    )))

# ============================================================ 4
L.append(dict(
    slug="04-linear-regression-model", title="The linear regression model", mins=10, tag="core",
    lede="The first algorithm, and the simplest useful one there is: draw a straight line through the data.",
    body=(
        pretest("""<p>Dots on a graph: house size across, price up. You want to draw one straight line through them. <b>How many numbers do you need to pin down exactly which line it is?</b> Commit to a number.</p>""",
                """<p>Watch for what each of those numbers <em>means</em> in house terms — one of them has a physical reading (dollars per square foot) and the other is famously meaningless on its own.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>You have dots on a graph: house size across the bottom, price up the side. Bigger houses
cost more, roughly.</p>
<p>Draw a straight line through the middle of the dots. Now for any size you like, look up the line and
read off the price.</p>
<p>A line needs exactly two numbers to describe it: <b>how steep it is</b> and <b>where it starts</b>.
Those two numbers are the entire model.</p>""")

        + h2("🎬", "Watch it move")
        + demo("linreg", "Drag w and b until the line fits",
               "the red dashes are the errors — try to make them all small at once")

        + h2("🔢", "The maths, decoded")
        + eqp([
            ('<var>f</var><sub><var>w</var>,<var>b</var></sub>(<var>x</var>)', "func-f", "apply the model to x"),
            ' <span class="op">=</span> <var class="hl-a">w</var><var>x</var> <span class="op">+</span> <var class="hl-b">b</var>',
        ], "the model — a straight line — click it")
        + decode([
            ("<var>f</var>", "“f of x”", "The model. Give it an x, it returns a prediction. Sometimes written h (for hypothesis) in older material."),
            ("<var class='hl-a'>w</var>", "“w”, the weight or slope", "How much y goes up for each unit of x. Here: dollars per square foot."),
            ("<var class='hl-b'>b</var>", "“b”, the bias or intercept", "Where the line crosses the y-axis. The prediction when x = 0."),
            ("<var>x</var><sup>(<var>i</var>)</sup>", "“x superscript i”", "The i-th training example. <b>Round brackets always mean “which example”</b> — never a power."),
            ("ŷ", "“y hat”", "The prediction. Plain y is the true value from the data; ŷ is what the model guesses."),
            ("<var>m</var>", "“m”", "The number of training examples."),
        ])
        + warn("""<p>Three different superscripts appear in this specialization and they mean three
different things. <var>x</var><sup>(2)</sup> = training example 2. <var>x</var><sup>2</sup> = x squared.
<var>a</var><sup>[2]</sup> = layer 2 (Course 2). The bracket style carries the meaning, and the course is
consistent about it.</p>""")

        + h2("🔬", "Why start with something this simple?")
        + """<p>Two reasons, and both are good ones.</p>
<p>First, every concept in the specialization is easier to see here. Cost functions, gradient descent,
overfitting, regularisation — all of them appear in Course 1 in a setting simple enough to draw on paper.
A neural network is doing the same things with more moving parts.</p>
<p>Second, linear regression is genuinely useful. It is fast, interpretable — you can read w and say “each
extra square foot is worth $100” — and on many real problems it is difficult to beat by enough to justify
anything more complicated.</p>"""

        + h2("💻", "In code")
        + code("""
import numpy as np

x_train = np.array([1.0, 2.0])      # size in 1000 sqft
y_train = np.array([300.0, 500.0])  # price in $1000s

w = 200
b = 100

def compute_model_output(x, w, b):
    m = x.shape[0]
    f_wb = np.zeros(m)
    for i in range(m):
        f_wb[i] = w * x[i] + b
    return f_wb
""")
        + """<p>That loop is the honest, slow version. Week 2 replaces it with a single vectorised line —
but it is worth writing this one once so the loop version is what you picture when you read the fast
one.</p>"""

        + h2("✅", "Check yourself")
        + quiz([
            ("w = 200, b = 100, x = 1.2. What is the prediction?",
             "<p>200(1.2) + 100 = <b>340</b>. In the housing units, $340,000.</p>"),
            ("What does b represent physically here?",
             "<p>The predicted price of a house of size zero — $100,000. Physically meaningless, and "
             "mathematically necessary: without it the line is forced through the origin.</p>"),
            ("How many parameters does this model have, and how many does a training set of 10,000 houses have?",
             "<p>The model has <b>two</b> parameters, w and b, regardless of the data size. 10,000 "
             "examples do not add parameters — they constrain the two you have.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("lab", REPO + "/week1/Optional%20Labs/C1_W1_Lab03_Model_Representation_Soln.ipynb",
             "Optional lab: Model Representation",
             "In this repo. Plot the line, drag w and b, and see the notation in code."),
            ("docs", "https://scikit-learn.org/stable/modules/linear_model.html#ordinary-least-squares",
             "scikit-learn — ordinary least squares",
             "The production version. <code>LinearRegression().fit(X, y)</code> does everything in this week in one line — which is exactly why it is worth understanding first."),
        ])
    )))

# ============================================================ 5
L.append(dict(
    slug="05-cost-function-formula", title="The cost function formula", mins=11, tag="maths",
    lede="One number that says how badly the current line fits. Everything from here is about making that "
         "number small.",
    body=(
        pretest("""<p>Your model is wrong on three houses by 30, 20 and 10. A rival is wrong on one house by 30 and perfect on the rest. <b>Which model is worse — and does your answer change if you square each miss before adding?</b></p>""",
                """<p>Do the squaring by hand before reading: 900+400+100 against 900. Watch for <em>why</em> the formula squares at all — it is a deliberate choice about which kind of wrongness to punish.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>You drew a line. Is it a good line?</p>
<p>Measure, for each dot, how far the line missed it. Then <b>square</b> each of those misses and add them
all up.</p>
<p>Why square? Two reasons. It makes everything positive, so being too high on one dot cannot cancel out
being too low on another. And it makes a big miss hurt much more than a small one — being off by 10 is a
hundred times worse than being off by 1, not ten times worse.</p>""")

        + h2("🎬", "Watch it move")
        + demo("costformula", "The squared error, drawn as an actual square",
               "each example is highlighted in turn and its contribution computed")

        + h2("🔢", "The maths, decoded")
        + eqp([
            ("<var>J</var>(<var>w</var>, <var>b</var>)", "cost-j", "the cost"),
            ' <span class="op">=</span> ',
            ('<span class="frac"><span>1</span><span>2<var>m</var></span></span>', "avg-factor", "the average"),
            ('<span class="big">Σ</span><sub><var>i</var>=1</sub><sup><var>m</var></sup>', "sigma", "for every example"),
            ('<span class="paren">(</span> <var>f</var><sub><var>w</var>,<var>b</var></sub>(<var>x</var><sup>(<var>i</var>)</sup>)'
             ' <span class="op">−</span> <var>y</var><sup>(<var>i</var>)</sup> <span class="paren">)</span>',
             "error-term", "predicted − actual"),
            ("<sup>2</sup>", "squared-term", "squared"),
        ], "the squared error cost function — click any part")
        + decode([
            ("<var>J</var>(<var>w</var>, <var>b</var>)", "“J of w and b”", "The cost. One number saying how wrong the whole line is. Written as a function of w and b because those are what you can change."),
            ("<span class='big'>Σ</span>", "“sum over i”", "A loop, written as a symbol: do the following for every training example and add up the results."),
            ("<var>f</var>(<var>x</var><sup>(i)</sup>) − <var>y</var><sup>(i)</sup>", "“the error”", "Predicted minus actual, for example i. Positive if the line is above the point."),
            ("( … )²", "“squared”", "Makes it positive, and punishes big misses disproportionately."),
            ("1/<var>m</var>", "“the average”", "So that J does not simply grow as you collect more data. Without it, more examples always means a bigger number."),
            ("the 2 in 1/2<var>m</var>", "“a convenience”", "Pure tidiness. Differentiating a square brings down a factor of 2, which cancels this one. It changes nothing about where the minimum is."),
        ])
        + key("""<p><b>Small J = good fit.</b> Training a model means: find the w and b that make J as small
as possible. That single sentence is what the rest of Week 1 is about.</p>""")

        + h2("🧮", "A worked example")
        + """<p>Three points: (1, 1), (2, 2), (3, 3). Try w = 1, b = 0:</p>
<ul>
<li>Predictions: 1, 2, 3. Errors: 0, 0, 0. Squared: 0, 0, 0.</li>
<li>J = (1 / 2×3) × 0 = <b>0</b>. A perfect fit.</li>
</ul>
<p>Now try w = 0.5, b = 0:</p>
<ul>
<li>Predictions: 0.5, 1, 1.5. Errors: −0.5, −1, −1.5. Squared: 0.25, 1, 2.25.</li>
<li>J = (1/6) × 3.5 = <b>0.583</b>.</li>
</ul>
<p>Worse line, bigger number. That is all J is doing.</p>"""

        + h2("🕳", "Traps")
        + trap("""<p><b>Forgetting to square.</b> Without the square, an error of +10 and one of −10
cancel to zero, and a terrible line scores perfectly.</p>""")
        + trap("""<p><b>Thinking the 2 matters.</b> It does not affect which (w, b) minimises J — only the
number J reports. Some textbooks omit it. Both are correct.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("Two points (1, 2) and (2, 4), with w = 2, b = 0. What is J?",
             "<p>Predictions 2 and 4; errors 0 and 0. <b>J = 0</b> — the line passes exactly through both "
             "points.</p>"),
            ("Same points, w = 1, b = 0. What is J?",
             "<p>Predictions 1 and 2; errors −1 and −2; squared 1 and 4. J = (1/4)(5) = <b>1.25</b>.</p>"),
            ("Why divide by m rather than just summing?",
             "<p>So that J is comparable across datasets of different sizes. Without it, a model on "
             "10,000 examples would always look worse than the same model on 100.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("lab", REPO + "/week1/Optional%20Labs/C1_W1_Lab04_Cost_function_Soln.ipynb",
             "Optional lab: Cost Function",
             "In this repo. Interactive plots of J against w — the same picture as the next lesson, in code you can change."),
            ("docs", "https://developers.google.com/machine-learning/crash-course/linear-regression/loss",
             "Google Crash Course — loss",
             "Includes L1 (absolute error) as a contrast, and why squared error is the usual default."),
        ])
    )))

# ============================================================ 6
L.append(dict(
    slug="06-cost-function-intuition", title="Cost function intuition", mins=10, tag="maths",
    lede="Two graphs that are easy to confuse and essential to keep apart: the model, and the cost.",
    body=(
        pretest("""<p>You will meet two graphs in this lesson. One has house size along the bottom; the other has <b>w</b> along the bottom. <b>Guess what a single dot on the second graph represents.</b></p>""",
                """<p>This is the most common confusion in Course 1. Watch for the sentence that says what one point on the second graph <em>is</em> — it is not a house.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>There are two completely different pictures here and mixing them up is the single most
common confusion in Course 1.</p>
<p><b>Picture 1</b> is the data: dots, and a line through them. The horizontal axis is <b>x</b> (house
size).</p>
<p><b>Picture 2</b> is the score: how good each possible line is. The horizontal axis is <b>w</b> (the
slope you chose).</p>
<p>Every <em>line</em> in picture 1 becomes a single <em>dot</em> in picture 2.</p>""")

        + h2("🎬", "Watch it move")
        + demo("costintuition", "Drag w and watch both pictures respond",
               "left: the model in data-space. right: the cost in parameter-space")

        + h2("🔢", "The simplification")
        + """<p>To make this drawable, set b = 0. The model becomes f(x) = wx — a line through the origin
with only <b>one</b> parameter. Now J depends on one number, so J(w) is a curve you can plot.</p>
<p>With the data (1,1), (2,2), (3,3):</p>"""
        + table(["w", "the fit", "J(w)"],
                [["1.0", "passes exactly through every point", "<b>0</b>"],
                 ["0.5", "too shallow", "0.58"],
                 ["0.0", "flat along the x-axis", "2.33"],
                 ["1.5", "too steep", "0.58"]])
        + """<p>Notice the symmetry: 0.5 and 1.5 are both 0.5 away from the best value, and both score
0.58. Plot enough of these and you get a <b>parabola</b> — a U-shape with exactly one lowest point.</p>"""
        + key("""<p>Left picture: the world of the <b>data</b>. Right picture: the world of the
<b>parameters</b>. Training happens entirely in the right-hand picture — you are searching for its lowest
point.</p>""")

        + h2("🔬", "Why a parabola, exactly?")
        + """<p>Because J is a sum of squared terms, and each term is a quadratic in w. Add up quadratics
and you get a quadratic. A quadratic with a positive leading coefficient is a U.</p>
<p>This is a much bigger deal than it looks. A U-shape has <b>exactly one</b> minimum. There is no risk of
getting stuck in a wrong valley, no dependence on where you start. Gradient descent on this shape simply
cannot fail. You will lose that guarantee in Week 3, and lose it thoroughly in Course 2.</p>"""

        + h2("🕳", "Traps")
        + trap("""<p><b>Reading the right-hand graph as if it were data.</b> The x-axis is w, not house
size. The curve is not a prediction — it is a score for each possible model.</p>""")
        + trap("""<p><b>Expecting J to reach zero.</b> It does here only because the toy data lies exactly
on a line. Real data has noise, and the minimum of J sits well above zero. That is not a failure.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("On the J(w) curve, what does a single point represent?",
             "<p>One complete choice of model — one specific line — and how badly it fits. Its height is "
             "the cost of that line.</p>"),
            ("Why is J(w) a parabola rather than some other shape?",
             "<p>Because it is a sum of squared linear terms, which is a quadratic in w. Quadratics with "
             "a positive leading coefficient are U-shaped.</p>"),
            ("If real data never lies exactly on a line, what does the minimum of J represent?",
             "<p>The best line available — not a perfect one. J at the minimum measures the irreducible "
             "scatter in the data, which no straight line could ever capture.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("lab", REPO + "/week1/Optional%20Labs/C1_W1_Lab04_Cost_function_Soln.ipynb",
             "Optional lab: Cost Function",
             "In this repo. Both pictures side by side, with sliders."),
        ])
    )))

# ============================================================ 7
L.append(dict(
    slug="07-visualizing-the-cost-function", title="Visualizing the cost function", mins=10, tag="maths",
    lede="Put b back in and J becomes a bowl in three dimensions. Seen from above, it becomes a contour "
         "map — and that map is the background of every picture for the rest of the course.",
    body=(
        pretest("""<p>With one parameter the cost was a U-shaped curve. Now there are two, <b>w</b> and <b>b</b>. <b>What shape does the cost become — and how would you draw a 3-D shape on flat paper?</b></p>""",
                """<p>Hikers and geologists solved the drawing problem centuries ago. Watch for the borrowed technique, and for what it means when the rings sit close together.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>With one parameter, J was a U-shaped curve. With two — w <em>and</em> b — it becomes a
<b>bowl</b>: a 3-D surface, with w one way, b the other, and J as the height.</p>
<p>A 3-D picture is awkward on a flat page. So do what map-makers do: look at it from <b>directly
above</b> and draw a ring around all the points at the same height. Rings close together mean steep; rings
far apart mean flat. The bullseye in the middle is the bottom of the bowl — the best line.</p>""")

        + h2("🎬", "Watch it move")
        + demo("costcontour", "Drag inside the right-hand panel",
               "each position is a (w, b) pair; the left panel shows the line that pair produces")
        + """<p>Move to the outer rings and the line is obviously wrong. Move towards the bullseye and it
settles onto the data. Every ring is a set of (w, b) pairs that are all <b>equally bad</b>.</p>"""

        + h2("🔢", "Reading a contour plot")
        + decode([
            ("contour plot", "“a height map”", "The 3-D bowl seen from above. Each closed curve joins points of equal J."),
            ("a ring", "“an iso-cost line”", "Every (w, b) on this ring gives a different line, all of which fit exactly as badly as each other."),
            ("rings close together", "“steep”", "J changes fast here. Gradient descent will take large steps."),
            ("the bullseye", "“the minimum”", "The best possible w and b for this data."),
            ("elongated rings", "“an awkward valley”", "The bowl is much steeper one way than the other. Week 2 shows why this is a problem and how feature scaling fixes it."),
        ])
        + key("""<p>Every gradient-descent picture in this specialization is a <b>path across this
map</b>, starting somewhere on an outer ring and walking to the bullseye. Getting comfortable reading it
now pays off for the next two courses.</p>""")

        + h2("🔬", "Why the rings are ellipses")
        + """<p>J is a quadratic in w and b, so its level sets are exact ellipses — not roughly, exactly.
Their shape is set by the data: the more the feature values vary, the steeper J is in the w direction and
the more squashed the ellipse becomes.</p>
<p>That connection matters. The elongation of these rings is a direct consequence of your feature scaling,
which is why Week 2 spends a whole lesson on it.</p>"""

        + h2("✅", "Check yourself")
        + quiz([
            ("Two different (w, b) points sit on the same contour ring. What does that tell you?",
             "<p>They produce two <b>different lines</b> that fit the data <b>equally badly</b>. Same J, "
             "different model.</p>"),
            ("The rings are very tightly packed in one direction. What does that mean for gradient descent?",
             "<p>J changes steeply in that direction, so gradient descent takes big steps there and small "
             "ones along the flat direction — the zig-zagging behaviour that feature scaling cures.</p>"),
            ("What is at the centre of the smallest ring?",
             "<p>The (w, b) that minimises J — the best-fitting line. Finding it is the whole job.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("lab", REPO + "/week1/Optional%20Labs/C1_W1_Lab04_Cost_function_Soln.ipynb",
             "Optional lab: Cost Function",
             "In this repo. Includes the 3-D surface and the contour plot, both interactive."),
            ("docs", "https://matplotlib.org/stable/gallery/images_contours_and_fields/contour_demo.html",
             "matplotlib — contour plots",
             "How to draw these yourself. <code>plt.contour</code> is three lines and worth knowing."),
        ])
    )))

# ============================================================ 8
L.append(dict(
    slug="08-gradient-descent", title="Gradient descent", mins=9, tag="core",
    lede="The algorithm that finds the bottom of the bowl — and, with almost no changes, trains every "
         "model in this specialization including the neural networks.",
    body=(
        pretest("""<p>You are on a hillside in fog thick enough to see one metre. You want the bottom of the valley. <b>Write down the procedure you would actually follow.</b> No map allowed.</p>""",
                """<p>Whatever you wrote is probably the algorithm. Watch for the one thing it never needs to know — and for the catch that comes with only ever looking one metre ahead.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>You are standing somewhere on a hilly landscape in thick fog. You want to get to the
bottom of a valley, and you can see about a metre in any direction.</p>
<p>What do you do? Spin around slowly, work out which way is <b>most steeply downhill</b>, take one small
step that way. Then do it again. And again.</p>
<p>You never need a map. Just the ground under your feet.</p>""")

        + h2("🎬", "Watch it move")
        + demo("gradientdescent", "Two walkers, two starting points",
               "each finds a valley — and they are not the same valley")

        + h2("🔢", "Why this is a big deal")
        + """<p>Gradient descent does not need to know where the minimum is. It only needs the <b>local
slope</b>. That is what makes it work in a million dimensions where you could never look at the surface at
all — which is precisely the situation for a neural network.</p>
<p>It is used for essentially every model in this specialization: linear regression, logistic regression,
neural networks, collaborative filtering, deep Q-networks. Learn it properly once.</p>"""
        + decode([
            ("gradient", "“the direction of steepest uphill”", "In one dimension it is just the derivative. In many, it is the vector of all the partial derivatives."),
            ("descent", "“go the other way”", "You want to go down, so you step in the <em>opposite</em> direction to the gradient. That is the minus sign in the update rule."),
            ("local minimum", "“a valley that may not be the deepest”", "A point where every direction is uphill. There may be a better one elsewhere and you would never know."),
            ("convex", "“a single bowl”", "A shape with exactly one minimum. Squared-error linear regression is convex, which is why the fog problem never bites here."),
        ])
        + key("""<p>Where you end up can depend on where you start. For <b>linear regression with squared
error</b> this never happens — the cost is a single smooth bowl, so every starting point leads to the same
answer. For neural networks it very much does happen, and people mostly stopped worrying about it.</p>""")

        + h2("🔬", "The honest caveat about local minima")
        + """<p>The fog picture makes local minima look like a serious threat. In modern practice they turn
out to be much less of a problem than expected.</p>
<p>In very high dimensions, a genuine local minimum requires the surface to curve upwards in <em>every
single one</em> of thousands of directions simultaneously, which is rare. Most flat points are saddle
points — up in some directions, down in others — and gradient descent slides off them eventually.</p>
<p>Worth knowing, so the picture in this lesson does not leave you more worried than the field is.</p>"""

        + h2("✅", "Check yourself")
        + quiz([
            ("Why does gradient descent not need to know where the minimum is?",
             "<p>Because it only ever uses the local slope. Repeatedly stepping downhill gets you there "
             "without ever seeing the whole landscape.</p>"),
            ("Two starting points give two different answers. What kind of cost function is this?",
             "<p>A <b>non-convex</b> one, with multiple local minima. Linear regression's squared-error "
             "cost is not like this; neural network costs are.</p>"),
            ("Is gradient descent only for linear regression?",
             "<p>No — it is the general workhorse. Nearly every model in these three courses is trained "
             "with it or a close variant.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("video", "https://www.3blue1brown.com/lessons/gradient-descent",
             "3Blue1Brown — Gradient descent, how neural networks learn",
             "The best visual account there is. Framed around neural networks, and everything in it applies here."),
            ("paper", "https://distill.pub/2017/momentum/",
             "Distill — Why Momentum Really Works",
             "Interactive. Shows exactly why an elongated valley is hard, which is the picture behind Week 2's feature scaling."),
        ])
    )))

# ============================================================ 9
L.append(dict(
    slug="09-implementing-gradient-descent", title="Implementing gradient descent", mins=10, tag="core",
    lede="The update rule, and the one implementation detail that is easy to get wrong and hard to notice: "
         "simultaneous update.",
    body=(
        pretest("""<p>Two dials, w and b, both to be adjusted. You work out w's new value, set it, <b>then</b> work out b's. <b>Guess what goes wrong — and whether you would notice.</b></p>""",
                """<p>Watch for why this bug is dangerous rather than fatal: it often still reduces the cost, which is precisely why it survives in people's code for months.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>You and a friend both have to take one step, and you both have to decide based on where
you are <b>right now</b>.</p>
<p>If you step first and then your friend looks around, they are deciding from a different position than
you did. You have taken half a step of one kind and half of another, and it is not the step either of you
meant to take.</p>
<p>So: both of you work out your step first. <b>Then</b> both of you move.</p>""")

        + h2("🎬", "Watch it move")
        + demo("gdsteps", "The correct order, and the wrong one",
               "the numbers at the bottom show they genuinely differ")

        + h2("🔢", "The maths, decoded")
        + eqp([
            ('<var>w</var> <span class="op">=</span>', "assign-op", "becomes, not equals"),
            ' <var>w</var> <span class="op">−</span> ',
            ('<var class="hl-a">α</var>', "alpha-lr", "the learning rate"),
            (' <span class="frac"><span>∂<var>J</var>(<var>w</var>,<var>b</var>)</span><span>∂<var>w</var></span></span>',
             "partial-f0", "the slope, at w"),
            '&nbsp;&nbsp;&nbsp;&nbsp;',
            ('<var>b</var> <span class="op">=</span>', "assign-op", "becomes, not equals"),
            ' <var>b</var> <span class="op">−</span> ',
            ('<var class="hl-a">α</var>', "alpha-lr", "the learning rate"),
            (' <span class="frac"><span>∂<var>J</var>(<var>w</var>,<var>b</var>)</span><span>∂<var>b</var></span></span>',
             "partial-f0", "the slope, at b"),
        ], "repeat until convergence — updating both simultaneously — click any part")
        + decode([
            ("=", "“becomes”, not “equals”", "This is assignment. In maths a = a − 1 is false; in code it is an instruction. Andrew writes := to be explicit."),
            ("<var class='hl-a'>α</var>", "“alpha”, the learning rate", "How big a step to take. A small positive number, usually between 0.001 and 1."),
            ("∂<var>J</var>/∂<var>w</var>", "“the partial derivative with respect to w”", "The slope of J in the w direction, holding b still."),
            ("the minus", "“go downhill”", "Subtracting the slope moves you against the uphill direction — this is the whole trick."),
            ("convergence", "“nothing is changing any more”", "When w and b stop moving appreciably between iterations, you are at (or very near) a minimum."),
        ])
        + key("""<p><b>Both parameters must be computed from the same old values.</b> Calculate both changes
first, then assign both. The sequential version is a different algorithm that happens to often still work
— which is exactly what makes the bug so hard to spot.</p>""")

        + h2("💻", "In code")
        + code("""
def gradient_descent(x, y, w, b, alpha, num_iters):
    for i in range(num_iters):
        dj_dw, dj_db = compute_gradient(x, y, w, b)   # compute BOTH first

        w = w - alpha * dj_dw                          # then assign BOTH
        b = b - alpha * dj_db
    return w, b
""")
        + """<p>In Python this happens to be safe because <code>dj_dw</code> and <code>dj_db</code> are
both computed before either assignment. The bug appears when people restructure the loop and compute the
gradients inside it, one at a time.</p>"""

        + h2("🕳", "Traps")
        + trap("""<p><b>Updating w, then recomputing the gradient before updating b.</b> Not gradient
descent. It may still reduce J, which is precisely why nobody notices.</p>""")
        + trap("""<p><b>Reading = as mathematical equality.</b> <code>w = w − α·∂J/∂w</code> is an
instruction, not a claim.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("w = 5, ∂J/∂w = 2, α = 0.1. What is the new w?",
             "<p>5 − 0.1(2) = <b>4.8</b>. The positive slope means uphill is to the right, so w moves "
             "left.</p>"),
            ("Why must the updates be simultaneous?",
             "<p>Because the gradient is defined at a specific point (w, b). Updating w first moves you "
             "to a different point, so b's step is computed from the wrong place.</p>"),
            ("What happens if α is negative?",
             "<p>You would climb <em>uphill</em> and J would grow. α is always positive; the minus sign "
             "in the formula is what makes it descent.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("lab", REPO + "/week1/Optional%20Labs/C1_W1_Lab05_Gradient_Descent_Soln.ipynb",
             "Optional lab: Gradient Descent",
             "In this repo. Implements this loop and plots the path across the contour map."),
        ])
    )))

# ============================================================ 10
L.append(dict(
    slug="10-gradient-descent-intuition", title="Gradient descent intuition", mins=9, tag="maths",
    lede="Why subtracting the derivative always sends you the right way — whichever side of the minimum "
         "you start on.",
    body=(
        pretest("""<p>The rule is <code>w = w − α × slope</code>. On the left-hand side of a valley the slope is negative. <b>Subtracting a negative number — which way does w move, and is that the right way?</b></p>""",
                """<p>Work the sign through by hand for both sides of the valley. Watch for why the formula never needs to know which side you started on.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>The derivative is just the <b>steepness</b> of the curve where you are standing, with a
sign attached.</p>
<ul>
<li>Standing on the right-hand slope of a valley, the ground rises to the right. Positive slope. Subtract
it and you move <b>left</b> — downhill. ✓</li>
<li>Standing on the left-hand slope, the ground falls to the right. Negative slope. Subtracting a negative
adds, so you move <b>right</b> — downhill. ✓</li>
</ul>
<p>Either way you head for the bottom, and the formula never has to know which side you are on.</p>""")

        + h2("🎬", "Watch it move")
        + demo("gdintuition", "Drag w and watch the tangent line",
               "the green arrow is the step gradient descent would take from there")

        + h2("🔢", "What a derivative is, if that word is new")
        + """<p>Draw the tangent line — the straight line that just touches the curve at your point without
crossing it. The derivative is that line’s <b>slope</b>: rise over run.</p>
<p>You do not need to be able to compute derivatives by hand to finish this course. You need to know that
the derivative is a number, that its <b>sign</b> tells you which way is uphill, and that its <b>size</b>
tells you how steep.</p>"""
        + decode([
            ("derivative", "“the slope right here”", "How much J changes for a tiny change in w. Positive = uphill to the right."),
            ("tangent line", "“the local straight-line approximation”", "Touching the curve at one point. Its slope is the derivative."),
            ("at the minimum", "“slope zero”", "The tangent is horizontal, so the update subtracts nothing and gradient descent stops on its own."),
        ])
        + key("""<p>Notice something the demo shows nicely: even with α <b>fixed</b>, the steps automatically
get smaller as you approach the minimum — because the slope gets smaller. You never have to shrink α by
hand.</p>""")

        + h2("🔬", "What happens exactly at the minimum")
        + """<p>The slope is zero, so w := w − α(0) = w. Nothing moves. Gradient descent has converged and
stays put — which is the behaviour you want.</p>
<p>This is also why a flat spot anywhere else is dangerous: if you land on a plateau or a saddle point, the
gradient is near zero and progress stalls even though you are not at a good solution. It does not arise for
linear regression, and it very much arises for deep networks.</p>"""

        + h2("✅", "Check yourself")
        + quiz([
            ("J(w) = w². At w = −3, what is the derivative, and which way does w move?",
             "<p>dJ/dw = 2w = <b>−6</b>. Negative, so w := −3 − α(−6) = −3 + 6α — w moves <b>right</b>, "
             "towards zero. ✓</p>"),
            ("Why do the steps shrink near the minimum even with α constant?",
             "<p>Because the step size is α × slope, and the slope approaches zero. The algorithm slows "
             "down automatically as it arrives.</p>"),
            ("What if you land exactly on a flat point that is not the minimum?",
             "<p>The gradient is zero, so you stop — even though a better solution exists. This is the "
             "plateau/saddle problem. It does not occur for linear regression's convex cost.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("video", "https://www.3blue1brown.com/topics/calculus",
             "3Blue1Brown — Essence of Calculus",
             "Chapters 1–3 cover everything you need about derivatives. If calculus never clicked at school, this is the fix."),
            ("docs", "https://www.khanacademy.org/math/differential-calculus",
             "Khan Academy — Differential Calculus",
             "Free, with practice problems, if you want mechanical fluency rather than just intuition."),
        ])
    )))

# ============================================================ 11
L.append(dict(
    slug="11-learning-rate", title="The learning rate", mins=11, tag="core",
    lede="The one hyperparameter in this week, and the one you will spend the most time on. Too small "
         "wastes days; too large produces NaN.",
    body=(
        pretest("""<p>α sets your step size. You try α = 0.0001 and it barely moves; you try α = 10 and the cost prints 12, 45, 380, <code>NaN</code>. <b>What is physically happening on the hillside at α = 10?</b></p>""",
                """<p>Picture the stride, not the number. Watch for the one-line debugging rule this gives you — it stays true for every model in all three courses.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>α decides how big a step you take.</p>
<ul>
<li><b>Tiny steps.</b> You will get there. Possibly next Tuesday.</li>
<li><b>Sensible steps.</b> Down the hill briskly, slowing naturally as it flattens.</li>
<li><b>Enormous steps.</b> You stride straight over the valley and land higher up the other side. Next
step, higher still. You are now climbing out of the valley backwards, faster and faster.</li>
</ul>""")

        + h2("🎬", "Watch it move")
        + demo("learningrate", "Drag α across three orders of magnitude",
               "watch the steps go from crawling, to smooth, to oscillating, to diverging")

        + h2("🔢", "The four regimes")
        + table(["α", "What happens", "What you see in J"],
                [["far too small", "converges, extremely slowly", "falls smoothly, and barely"],
                 ["about right", "converges briskly", "falls fast, then flattens"],
                 ["too large", "overshoots and oscillates", "bounces up and down"],
                 ["far too large", "<b>diverges</b>", "grows without limit, then <code>NaN</code>"]])
        + decode([
            ("α", "“alpha”, the learning rate", "A hyperparameter — you choose it, the algorithm does not learn it."),
            ("overshoot", "“stepping past the bottom”", "The step is longer than the distance to the minimum, so you land on the far side."),
            ("diverge", "“it explodes”", "Each overshoot is bigger than the last. J grows towards infinity, and floating point gives up with NaN."),
            ("hyperparameter", "“a setting, not a parameter”", "w and b are learned from data. α is chosen by you, before training starts."),
        ])
        + key("""<p><b>If J ever increases between iterations, α is too large.</b> That is the single most
useful debugging rule in this course, and it stays true for every model in all three courses.</p>""")

        + h2("🔬", "The debugging trick worth remembering")
        + """<p>Your model is not learning and you do not know whether it is α or a bug in the gradient.</p>
<p>Set α to something absurdly small — 0.0001. With a tiny enough step, J is guaranteed to decrease on
every single iteration <em>if the gradient is correct</em>. So:</p>
<ul>
<li>J now decreases → the gradient is fine, and your original α was too large.</li>
<li>J still does not decrease → it is not α. There is a bug, most often a sign error in the gradient.</li>
</ul>
<p>This is a genuinely useful separation of concerns, and it takes one line to try.</p>"""

        + h2("🕳", "Traps")
        + trap("""<p><b>Assuming a small α is the safe choice.</b> It is safe and it may take a hundred
thousand iterations. Andrew’s advice is to find the largest α that still converges smoothly, then perhaps
back off one notch.</p>""")
        + trap("""<p><b>Not scaling your features first.</b> The best α depends enormously on feature
scale. Week 2 covers this, and it is the most common reason a “reasonable” α refuses to work.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("Your J values are 12, 45, 380, NaN. What is wrong?",
             "<p>α is far too large — it is diverging. Reduce it by a factor of ten and try again.</p>"),
            ("Your J values are 12.0, 11.98, 11.96, 11.94. What is wrong?",
             "<p>Nothing is <em>wrong</em> — it is converging, glacially. α is too small. Increase it by "
             "a factor of three or ten.</p>"),
            ("You set α = 0.0001 and J still does not decrease. What does that tell you?",
             "<p>It is not the learning rate. There is a bug in the gradient computation — most often a "
             "sign error or a wrong index.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("lab", REPO + "/week2/Optional%20Labs/C1_W2_Lab03_Feature_Scaling_and_Learning_Rate_Soln.ipynb",
             "Optional lab: Feature Scaling and Learning Rate",
             "In this repo. Runs several α values and plots each J curve — exactly the experiment described here."),
            ("paper", "https://arxiv.org/abs/1506.01186",
             "Smith (2015) — Cyclical Learning Rates for Training Neural Networks",
             "The “LR range test”: sweep α upwards during a short run and read the best value off the curve. Standard practice now."),
        ])
    )))

# ============================================================ 12
L.append(dict(
    slug="12-gradient-descent-for-linear-regression", title="Gradient descent for linear regression",
    mins=10, tag="maths",
    lede="Putting the two halves together — the actual derivatives, and the guarantee that makes this "
         "combination unusually well behaved.",
    body=(
        pretest("""<p>The w-update and the b-update turn out to be almost identical, except one has an extra <b>× x⁽ⁱ⁾</b> on the end. <b>Guess which one, and why that example's own x would matter to it.</b></p>""",
                """<p>Think about what w multiplies in the model and what b does not. Watch for the sentence that explains why big houses pull harder on w than small ones do.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>You have a way to score a line (the cost function) and a way to walk downhill (gradient
descent). Now bolt them together.</p>
<p>And there is a piece of good luck here. The bowl for linear regression has <b>exactly one</b> bottom —
no side valleys, no traps. Whichever fog-bound spot you start from, you always end up in the same place.</p>""")

        + h2("🎬", "Watch it move")
        + demo("gdlinreg", "One bowl versus many valleys",
               "the derivatives, and the property that makes linear regression easy")

        + h2("🔢", "The derivatives")
        + eqp([
            ('<span class="frac"><span>∂<var>J</var></span><span>∂<var>w</var></span></span>', "partial-f0", "the slope, at w"),
            ' <span class="op">=</span> ',
            ('<span class="frac"><span>1</span><span><var>m</var></span></span>', "avg-factor", "the average"),
            ('<span class="big">Σ</span>', "sigma", "for every example"),
            (' <span class="paren">(</span> <var>f</var>(<var>x</var><sup>(<var>i</var>)</sup>) <span class="op">−</span> <var>y</var><sup>(<var>i</var>)</sup> <span class="paren">)</span>',
             "error-term", "predicted − actual"),
            ('<var class="hl-a">· <var>x</var><sup>(<var>i</var>)</sup></var>', "times-xi", "only in the w-derivative"),
        ], "the w derivative — click any part", small=True)
        + eqp([
            ('<span class="frac"><span>∂<var>J</var></span><span>∂<var>b</var></span></span>', "partial-f0", "the slope, at b"),
            ' <span class="op">=</span> ',
            ('<span class="frac"><span>1</span><span><var>m</var></span></span>', "avg-factor", "the average"),
            ('<span class="big">Σ</span>', "sigma", "for every example"),
            (' <span class="paren">(</span> <var>f</var>(<var>x</var><sup>(<var>i</var>)</sup>) <span class="op">−</span> <var>y</var><sup>(<var>i</var>)</sup> <span class="paren">)</span>',
             "error-term", "predicted − actual"),
        ], "the b derivative — identical, minus the x — click any part", small=True)
        + """<p>The only difference is the <b>· x<sup>(i)</sup></b> on the end of the first one. That makes
intuitive sense: a change in w affects a house with x = 4 four times as much as one with x = 1, so large-x
examples pull harder on w. Changing b shifts every prediction by the same amount, so every example gets an
equal vote.</p>"""
        + decode([
            ("∂<var>J</var>/∂<var>w</var>", "“the slope of J in the w direction”", "Decoded fully in the previous lesson — the same object, just written out for this specific model."),
            ("<span class='big'>Σ</span> ( … )", "“add this up over every example”", "Do the calculation inside the brackets once per training example, then add the m results together."),
            ("<var>f</var>(<var>x</var><sup>(i)</sup>) <span class='op'>−</span> <var>y</var><sup>(i)</sup>", "“the error, again”", "Same error term as the cost function — prediction minus actual, for example i."),
            ("<var class='hl-a'>· <var>x</var><sup>(i)</sup></var>", "“times that example's x”", "The one piece that is new here. It is what makes this the w-derivative rather than the b-derivative — see the paragraph below."),
        ])
        + note("""<p>Here is where that 2 in 1/2m goes. Differentiating (…)² brings down a factor of 2 by
the chain rule, which cancels the 2 in the denominator, leaving a clean 1/m. That is the entire reason the
2 was put there — someone worked out the derivative first and then wrote the cost function to make it
tidy.</p>""", "The 2 finally pays off")

        + h2("🔬", "Convexity, and why it matters here")
        + """<p>The squared-error cost for linear regression is <b>convex</b>: a single smooth bowl. This
has a real, provable consequence — gradient descent with a sufficiently small α will <em>always</em> reach
the global minimum, from any starting point.</p>
<p>That is a stronger guarantee than almost anything else in machine learning offers. You lose it the
moment you build a neural network in Course 2, and the field carries on regardless because in practice
local minima turn out to be far less troublesome than the theory feared.</p>"""

        + h2("💻", "In code")
        + code("""
def compute_gradient(x, y, w, b):
    m = x.shape[0]
    dj_dw = 0
    dj_db = 0
    for i in range(m):
        f_wb = w * x[i] + b
        dj_dw += (f_wb - y[i]) * x[i]      # note the * x[i]
        dj_db += (f_wb - y[i])             # and note that it is absent here
    return dj_dw / m, dj_db / m
""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Forgetting the <code>* x[i]</code> in dj_dw, or adding it to dj_db.</b> The most
common bug in the Week 2 assignment. The symptom is that training converges to something confidently
wrong.</p>""")
        + trap("""<p><b>Dividing by m in the wrong place.</b> Divide once, after the loop. Dividing inside
gives m² in the denominator.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("Why does the w derivative have an extra x<sup>(i)</sup> but the b derivative does not?",
             "<p>Because w is multiplied by x in the model, so an example with a large x is more sensitive "
             "to a change in w. b is added to every prediction equally, so every example weighs the "
             "same.</p>"),
            ("What does “convex” guarantee, precisely?",
             "<p>That there is exactly one minimum, so gradient descent with a small enough α reaches the "
             "global optimum from any starting point.</p>"),
            ("Does this convexity guarantee survive into Course 2?",
             "<p>No. Neural network cost functions are non-convex with many local minima. In practice "
             "this matters much less than the theory suggests, but the guarantee is genuinely gone.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("book", "https://web.stanford.edu/~boyd/cvxbook/",
             "Boyd & Vandenberghe — Convex Optimization",
             "Free PDF, and the standard reference for what convexity buys you. Heavy going, and chapter 1 is readable."),
            ("lab", REPO + "/week1/Optional%20Labs/C1_W1_Lab05_Gradient_Descent_Soln.ipynb",
             "Optional lab: Gradient Descent",
             "In this repo. Implements compute_gradient and plots the descent path."),
        ])
    )))

# ============================================================ 13
L.append(dict(
    slug="13-running-gradient-descent", title="Running gradient descent", mins=9, tag="core",
    lede="Watching it actually work — the path across the contour map, the falling cost curve, and what "
         "“batch” means.",
    body=(
        pretest("""<p>Watching it train, the path takes big confident strides at first, then crawls slowly for a long time. <b>Guess what about the data — not the algorithm — causes the crawl.</b></p>""",
                """<p>Watch for the shape of the bowl seen from above, and for which of next week's lessons is the fix.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Press go and watch three things happen at once.</p>
<p>The line on the left swings around and settles onto the data. The dot on the right walks steadily from
an outer ring to the bullseye. And the cost curve underneath falls and flattens.</p>
<p>They are three views of the same event.</p>""")

        + h2("🎬", "Watch it move")
        + demo("gdrunning", "All three views at once — and try changing α",
               "the fit, the path across the cost map, and J against iterations")
        + """<p>Look at the shape of the path. Big confident strides down the steep sides of the valley,
then a long slow crawl along the flat floor towards the centre. That elongated valley is a direct
consequence of the features not being scaled — which is the first thing Week 2 fixes.</p>"""

        + h2("🔢", "What “batch” means")
        + decode([
            ("batch gradient descent", "“use every example, every step”", "Each single update looks at all m training examples. What this course uses throughout Course 1."),
            ("stochastic gradient descent", "“one example at a time”", "Each update uses a single example. Noisier per step, and far more steps per second."),
            ("mini-batch", "“a handful at a time”", "The practical compromise — typically 32 to 512 examples per step. What essentially all deep learning uses."),
        ])
        + """<p>The name “batch” is why you will see the term <em>mini</em>-batch later: it is a smaller
batch. Course 3 Week 3 revisits this properly. For Course 1, batch is simple and fast enough.</p>"""

        + h2("📈", "The one plot to always make")
        + key("""<p>Plot J against iteration number. Every time. It costs three lines of matplotlib and it
tells you immediately whether α is sensible, whether it has converged, and whether something is broken.
Skipping it is how people spend two days on a problem that a glance would have diagnosed.</p>""")
        + code("""
w, b, J_history = gradient_descent(x, y, w_init, b_init, alpha, iters)

plt.plot(J_history)
plt.xlabel('iteration')
plt.ylabel('J(w, b)')
""")

        + h2("✅", "Check yourself")
        + quiz([
            ("Why does the path bend sharply and then crawl?",
             "<p>Because the cost bowl is elongated. Gradient descent moves fast down the steep direction "
             "and slowly along the shallow one. Feature scaling (Week 2) makes the bowl rounder and the "
             "path direct.</p>"),
            ("What does “batch” gradient descent mean?",
             "<p>Every update uses all m training examples. The alternatives are stochastic (one at a "
             "time) and mini-batch (a small subset).</p>"),
            ("You plot J and it decreases for 100 iterations then flattens completely. What now?",
             "<p>It has converged. Running longer will not help. If the fit is still poor, the problem is "
             "the model or the features — not the optimisation.</p>"),
        ])

        + h2("🎓", "That is Week 1")
        + """<p>You now have a complete, working machine learning algorithm: a model (f = wx + b), a way to
score it (J), and a way to improve it (gradient descent). Everything in the remaining six weeks of Courses
1 and 2 is a variation on those three pieces.</p>
<p>Week 2 scales it up to many features and makes it fast. Week 3 changes the model and the cost so it can
do classification. Course 2 makes the model a neural network. The three-part structure never changes.</p>"""

        + h2("🔗", "Go deeper")
        + links([
            ("lab", REPO + "/week1/Optional%20Labs/C1_W1_Lab05_Gradient_Descent_Soln.ipynb",
             "Optional lab: Gradient Descent",
             "In this repo. Includes the contour path animation and the J curve."),
            ("lab", REPO + "/week2/C1W2A1/C1_W2_Linear_Regression.ipynb",
             "Week 2 assignment: Linear Regression",
             "In this repo. The graded exercise — you implement compute_cost and compute_gradient yourself."),
        ])
    )))

WEEK = dict(
    course="C1", week=1, title="Introduction to Machine Learning",
    time="~5–6 h with labs",
    goal="Understand what supervised learning is, build linear regression, define a cost function, and "
         "train it with gradient descent — the three pieces every later algorithm reuses.",
    lessons=L,
)
