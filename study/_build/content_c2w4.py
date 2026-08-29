# -*- coding: utf-8 -*-
"""C2 · Week 4 — Decision trees and tree ensembles."""
from kit import (kid, key, warn, trap, note, card, eq, eqp, decode, table, demo,
                 quiz, links, code, h2, grid2, grid3, pretest, explain, lenses)

L = []

CAT_TABLE = table(
    ["#", "Ear shape", "Face shape", "Whiskers", "Cat?"],
    [["1", "pointy", "round", "present", "<b>yes</b>"],
     ["2", "pointy", "round", "present", "<b>yes</b>"],
     ["3", "pointy", "round", "absent", "<b>yes</b>"],
     ["4", "pointy", "round", "absent", "<b>yes</b>"],
     ["5", "pointy", "not round", "present", "no"],
     ["6", "floppy", "not round", "present", "<b>yes</b>"],
     ["7", "floppy", "round", "absent", "no"],
     ["8", "floppy", "round", "absent", "no"],
     ["9", "floppy", "round", "absent", "no"],
     ["10", "floppy", "not round", "absent", "no"]])

# ============================================================ 1
L.append(dict(
    slug="01-decision-tree-model", title="Decision tree model", mins=9, tag="intuition",
    lede="A completely different kind of model: no weights, no gradient descent, no calculus. Just a "
         "flowchart of yes/no questions — and on spreadsheet data it often wins.",
    body=(
        pretest("""<p>Is it a cat? You may ask about ear shape, face shape and whiskers. <b>Write down the questions you would ask, in order</b> — and notice you just built the model.</p>""",
        """<p>Watch for the vocabulary: root, node, leaf. You already understand the structure; this is naming it.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>You know that game where you guess an animal by asking questions? “Does it have pointy
ears?” Yes → “Is its face round?” Yes → “It’s a cat!”</p>
<p>That’s the entire model. A list of questions arranged in a tree, where the answer to each question tells
you which question to ask next, until you reach the bottom and give your answer.</p>
<p>No maths at all when you <em>use</em> it. All the cleverness is in choosing which questions to ask —
which is the next few lessons.</p>""")

        + lenses(
            """<p>A triage nurse in a busy A&amp;E. Someone walks in. <b>“Chest pain?”</b> No — and she points
down a different corridor entirely. Yes — and the next question is <b>“how long?”</b> Under an
hour sends you one way, since yesterday sends you another.</p>
<p>She never weighs everything she knows about you at once. She asks <em>one</em> question, and your
answer decides which question comes next. By the fourth question you are in a room. A decision tree
is that corridor, written down.</p>""",
            """<p>If you have ever written a nested <code>IF</code> in a spreadsheet, or drawn a flowchart for an
approval process, you have already built a decision tree by hand.</p>
<p>The only thing that changes here is <b>who chooses the questions</b>. You chose yours from
experience, and put the most useful one first because you knew it was the most useful. The algorithm
has no experience, so it has to measure which question is most useful — and that measurement is
the whole of the next three lessons.</p>""",
            """<p>An upside-down tree drawn on paper: one box at the top, two arrows leaving it, more boxes below,
and along the bottom a row of labels.</p>
<p>To make a prediction you put a finger on the top box and slide it down one arrow at a time until
you run out of arrows. <b>That path is the prediction</b> — not the whole tree, just the one
route your animal took through it. Most of the tree is irrelevant to any single prediction, and that
is not a flaw.</p>""",
            """<p>Banks adjudicating loans and hospitals writing clinical decision rules reach for trees over
networks constantly, and usually not for accuracy. They reach for them because <b>the path is the
explanation</b>.</p>
<p>Under EU credit law a rejected applicant can demand the reason for the decision. “The fourth layer
had a high activation” is not a reason. “Your debt-to-income was above 0.43 <em>and</em> your account
was under six months old” is a reason, it is auditable, and you can read it straight off the path.</p>""",
            """So when the formal version below says a tree is decision nodes and leaf nodes, it is saying something
very plain: the questions, and the answers you land on.""")

        + h2("🐱", "The data")
        + """<p>Ten animals, three features, one label. This is the running example for the whole week and
it is worth glancing back at.</p>"""
        + CAT_TABLE
        + """<p>Every feature here takes one of two values, which keeps the arithmetic clean. Lessons 6 and
7 remove that restriction.</p>"""

        + h2("🎬", "Watch it move")
        + demo("treeplay", "Toggle the features and watch the path light up",
               "the orange path is the only part of the tree that gets used")

        + h2("🔢", "The vocabulary")
        + decode([
            ("root node", "“the top”", "The first question, asked of every example. Drawn at the top; trees in ML grow downwards."),
            ("decision node", "“an internal question”", "Any node that asks about a feature and branches. Also called a split."),
            ("leaf node", "“the answer”", "A node with no children. It makes the prediction — no more questions asked."),
            ("branch", "“an answer arrow”", "The path taken for one value of the feature."),
            ("depth", "“how many questions deep”", "The number of decisions from root to leaf. The main knob for controlling overfitting."),
        ], head=("Term", "Say it out loud", "What it is"))
        + key("""<p>There are <b>many</b> possible trees for the same data. The learning algorithm’s job is
to pick one that is accurate on the training set <em>and</em> small enough to generalise. Small matters:
a tree deep enough to give every example its own leaf is a perfect memoriser.</p>""")

        + h2("🔬", "How this differs from everything so far")
        + table(["", "Neural network", "Decision tree"],
                [["Parameters", "weights and biases — millions", "the questions and the tree shape"],
                 ["Trained by", "gradient descent", "greedy search over splits"],
                 ["Needs calculus", "yes", "<b>no</b>"],
                 ["Needs feature scaling", "yes", "<b>no</b> — only order matters"],
                 ["Handles categories", "needs one-hot", "natively"],
                 ["Readable by a human", "essentially no", "<b>yes</b>, if it is small"]])

        + h2("🕳", "Traps")
        + trap("""<p><b>Thinking every feature is used for every prediction.</b> Only the features on the
path are consulted. If the ears are pointy, this tree never looks at the whiskers at all.</p>""")

        + explain("""<p>The comparison table says a tree needs no feature scaling. <b>Say why not, when every model in
C1 and C2 so far did.</b></p>""",
                  """<p>Because a tree only ever asks <b>&ldquo;is this value above that threshold?&rdquo;</b>, and the
answer to that question is unchanged by any monotonic rescaling. Multiply every salary by 1000 and
every split still separates exactly the same examples.</p>
<p>Gradient-based models care because scaling changes the <em>shape of the cost surface</em>. A tree
has no cost surface and takes no steps — it only compares. Same data, completely different reason to
care or not.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("A floppy-eared animal with whiskers. What does the tree in the demo say, and which features did it use?",
             "<p><b>Cat.</b> It used ear shape and whiskers. Face shape was never examined.</p>"),
            ("Why is a very deep tree a bad idea even though it fits the training data perfectly?",
             "<p>Because it can give every training example its own leaf — pure memorisation, and no "
             "generalisation. Depth is the tree’s equivalent of polynomial degree.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("docs", "https://scikit-learn.org/stable/modules/tree.html",
             "scikit-learn — Decision Trees",
             "Including <code>plot_tree()</code>, which draws the real thing for you."),
            ("paper", "https://link.springer.com/article/10.1007/BF00116251",
             "Quinlan (1986) — Induction of Decision Trees",
             "The ID3 algorithm — this exact entropy-based procedure, from the paper that started it."),
            ("lab", "../../C2%20-%20Advanced%20Learning%20Algorithms/week4/optional%20labs/C2_W4_Lab_01_Decision_Trees.ipynb",
             "Optional lab: Decision Trees",
             "In this repo. Builds the cat tree by hand, split by split."),
        ])
    )))

# ============================================================ 2
L.append(dict(
    slug="02-learning-process", title="The learning process", mins=9, tag="core",
    lede="Two decisions define the entire algorithm: which feature to split on, and when to stop.",
    body=(
        pretest("""<p>Building a tree means choosing which question to ask first. <b>Guess what makes one question better than another.</b></p>""",
        """<p>Watch for the goal: after the split, each group should be more <em>uniform</em> than before. The next lesson makes that measurable.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Building the tree is like sorting a messy box of Lego. You pick a rule — “red on the
left, everything else on the right” — and the box splits into two smaller, tidier boxes. Then you do the
same thing to each smaller box.</p>
<p>Two questions come up every time. <b>Which rule do I use?</b> (the one that tidies the most) and
<b>when do I stop?</b> (when a box is already all one colour, or when it’s too small to bother with).</p>""")

        + lenses(
            """<p>A sorting office in the week before Christmas. Someone tips a sack onto a table and splits it by
the single biggest thing that separates: <b>overseas or domestic</b>. Two smaller piles.</p>
<p>Someone else takes each pile and splits <em>that</em> by the next most useful thing — region.
Then postcode. Then street. Nobody planned the sequence in advance, and nobody is holding the whole
sorting scheme in their head. At each table you look at the pile in front of you and pick the one
split that tidies it most.</p>""",
            """<p>This is a <b>greedy</b> algorithm in the exact technical sense, and if you have met stepwise
regression, nearest-neighbour route building, or Huffman coding, you know the shape: take the locally
best move, commit to it, never reconsider.</p>
<p>You also know the price. Greedy is cheap and usually good, and it is <em>provably not optimal</em>
— finding the smallest tree that fits the data exactly is NP-hard, which is why nobody does it.</p>""",
            """<p>One pile of ten animals becoming two piles of five, then four piles of two or three. Draw it as
actual piles on a table, not as a diagram.</p>
<p>At every pile the algorithm asks one question and one only: <b>which single feature, split right
now, leaves the two children tidiest?</b> Then it walks away and lets someone else worry about the
children.</p>""",
            """<p>The greediness is why adding a single row to your training data can change the top split, and
changing the top split rewrites <em>every</em> tree beneath it.</p>
<p>Teams running trees in production watch for exactly this: a model that reshuffles dramatically
between retrains on almost identical data. It looks like a bug and it is not one — it is the
algorithm being what it is, and it is a large part of why single trees gave way to forests.</p>""",
            """So the formal statement — pick the split with the highest information gain, recurse, stop on a
criterion — is that sorting office written in three lines.""")

        + h2("🎬", "Watch it move")
        + demo("treeprocess", "The two decisions, and the four ways to stop",
               "decision 1 is lessons 3–4; decision 2 is where overfitting is controlled")

        + h2("🔢", "Decision 1 — which feature?")
        + """<p>Try every feature. For each one, ask: how <b>pure</b> are the two groups it creates? Keep
the feature that produces the purest split. “Pure” means “as close as possible to all-one-class”, and
Lesson 3 makes it a number.</p>
<p>This is a <b>greedy</b> algorithm: it takes the best split available <em>right now</em>, without
checking whether a slightly worse split now would allow a much better one later. Finding the globally
optimal tree is NP-hard, so every practical implementation is greedy.</p>"""

        + h2("🔢", "Decision 2 — when to stop?")
        + table(["Stop when…", "Why", "Typical setting"],
                [["a node is 100% one class", "there is nothing left to separate", "always"],
                 ["splitting would exceed max depth", "smaller trees generalise better", "depth 3–10"],
                 ["the information gain is below a threshold", "not worth the complexity", "problem-specific"],
                 ["a node has too few examples", "a split decided by 2 examples is noise", "5–20 examples"]])
        + key("""<p>Every stopping rule exists for the same reason: <b>keeping the tree small</b>. A deeper
tree always fits the training data better and generalises worse. This is exactly the bias/variance dial
from Week 3, wearing a different hat.</p>""")
        + note("""<p>The alternative to stopping early is <b>pruning</b>: grow the tree fully, then cut
branches back that do not help on a validation set. It often works better than early stopping, because a
split that looks useless can enable a great one below it. scikit-learn offers it as
<code>ccp_alpha</code>.</p>""", "The other approach: prune afterwards")

        + h2("🔤", "The words, decoded")
        + decode([
            ("node", "“node”, or “a split”", "A point in the tree where a question is asked."),
            ("root node", "“the root”", "The very first question, at the top, seen by every example."),
            ("leaf node", "“a leaf”", "A node that asks nothing and makes a prediction instead."),
            ("purity", "“how mixed it is”", "How close a group is to being all one class. Entropy is one way to measure it."),
            ("stopping criterion", "“when to stop”", "The rule that ends the recursion — max depth, minimum examples, or too little gain."),
        ])
        + h2("🕳", "Traps")
        + trap("""<p><b>Assuming the greedy tree is the best tree.</b> It usually isn’t. It is a good tree
found quickly, and that trade is why the algorithm is practical.</p>""")
        + trap("""<p><b>Leaving max_depth unset.</b> scikit-learn will happily grow until every leaf is
pure — a perfectly overfit tree. Always set <code>max_depth</code> or <code>min_samples_leaf</code>.</p>""")

        + explain("""<p>Left alone, scikit-learn grows a tree until every leaf is pure — 100% training accuracy. <b>Say
why that is a warning rather than an achievement.</b></p>""",
                  """<p>Because on any dataset with no duplicate rows it is <em>always</em> achievable, for any data,
including pure noise. A result you can get regardless of whether there is a pattern tells you nothing
about whether there is one.</p>
<p>What it has done is memorise: one path per training example. Every stopping rule —
<code>max_depth</code>, <code>min_samples_leaf</code> — exists to stop it, and they are the reason the
tree has to generalise instead of remembering.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("Why is choosing the best split greedy rather than exhaustive?",
             "<p>Because the number of possible trees is astronomical — finding the optimal one is NP-hard. "
             "Greedy is fast and works well in practice.</p>"),
            ("A node has 3 examples: 2 cats, 1 not. Should you split it?",
             "<p>Probably not. A rule learned from 3 examples is almost certainly noise. Make it a leaf "
             "predicting “cat”, and accept the one error.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("docs", "https://scikit-learn.org/stable/modules/tree.html#tree-algorithms-id3-c4-5-c5-0-and-cart",
             "scikit-learn — ID3, C4.5, CART compared",
             "The families of tree algorithms and how they differ. CART is what sklearn implements."),
            ("docs", "https://scikit-learn.org/stable/auto_examples/tree/plot_cost_complexity_pruning.html",
             "scikit-learn — cost-complexity pruning",
             "The grow-then-prune alternative, with the validation curve."),
        ])
    )))

# ============================================================ 3
L.append(dict(
    slug="03-measuring-purity", title="Measuring purity (entropy)", mins=15, tag="maths",
    lede="Turning “how mixed up is this group?” into a single number between 0 and 1. The one genuinely "
         "new piece of maths this week.",
    body=(
        pretest("""<p>A bag of 6 cats and 0 dogs versus 3 cats and 3 dogs. <b>Which is messier — and can you put a number on the mess?</b></p>""",
        """<p>Watch for the number being 0 and 1 at the two extremes, and for why all-dogs is just as tidy as all-cats.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>A bag of 6 cats and 0 dogs: reach in, and you already know what you’ll get. Zero
surprise. Zero mess. Call it <b>0</b>.</p>
<p>A bag of 3 cats and 3 dogs: you have no idea what’s coming out. Maximum surprise. Maximum mess.
Call it <b>1</b>.</p>
<p>Entropy is the number that measures exactly this: <b>how surprised will I be by the next thing I pull
out?</b> And notice it is symmetric — all cats and all dogs are both perfectly tidy.</p>""")

        + h2("🔢", "The maths, decoded")
        + eqp([
            '<var>H</var>(<var>p</var>) <span class="op">=</span> ',
            ('<span class="op">−</span><var>p</var> log<sub>2</sub>(<var>p</var>)', "logarithm-f0", "log, base 2 → bits"),
            ' <span class="op">−</span> ',
            ('(1 <span class="op">−</span> <var>p</var>) log<sub>2</sub>(1 <span class="op">−</span> <var>p</var>)', "logarithm-f0", "the other class, same idea"),
        ], "entropy — impurity of a group — hover or click a part")
        + decode([
            ("<var>p</var>", "“p one”", "The fraction of the group that is the positive class. 4 cats out of 5 → p = 0.8."),
            ("log<sub>2</sub>", "“log base two”", "Base 2 makes H come out in <b>bits</b>, so a 50/50 group is exactly 1 — one coin flip of uncertainty."),
            ("the minus signs", "“flip it positive”", "log of a number below 1 is negative. The minus makes H positive, so bigger = messier."),
            ("H = 0", "“pure”", "Everything is the same class. Happens at p = 0 and at p = 1."),
            ("H = 1", "“total mess”", "Exactly half and half. p = 0.5."),
            ("0 log 0", "“defined as 0”", "Mathematically it is a limit; in code you must special-case it or you get NaN."),
        ])

                + lenses(
            """<p>Sorting a drawer of mixed screws.</p>
<p>A drawer that is all one size needs no thought — reach in blind and you have the right screw. A
drawer half wood-screws and half machine-screws makes you look every time. Entropy is a number for
exactly that: how much looking a group forces on you.</p>""",
            """<p>This is Shannon entropy, from information theory, and it measures <b>surprise</b> — the average
number of bits needed to convey which class an item is.</p>
<p>All-one-class costs zero bits: you never need to be told. A fifty-fifty split costs exactly one bit
per item, which is why the maximum is 1 and why the logarithm is base 2. The units are literally
bits.</p>""",
            """<p>An arch, upside down.</p>
<p>Zero at both ends — all one class, or all the other — and peaking dead centre at a 50/50 mix. Note
that H(0.8) and H(0.2) are identical: entropy measures how mixed, not which side wins.</p>""",
            """<p>The same formula compresses your files. ZIP and JPEG work by spending fewer bits on predictable
data and more on surprising data — which is Shannon’s result applied to storage rather than to
splitting.</p>
<p>A decision tree asking “which question most reduces entropy?” is asking “which question compresses
my uncertainty most?”. The two fields are the same mathematics with different goals.</p>""",
            """So the formula below is measuring surprise in bits, and the tree simply hunts for whichever question
removes the most of it.""")
        + h2("🎬", "Watch it move")
        + demo("entropy", "A bag of twelve animals",
               "drag the mix and watch the curve — it peaks at 50/50 and is symmetric")

        + h2("🧮", "Values worth memorising")
        + table(["Mix", "p", "H(p)", "Read as"],
                [["5/5 cats", "1.00", "<b>0.00</b>", "perfectly pure"],
                 ["4/5 cats", "0.80", "<b>0.72</b>", "mostly cats"],
                 ["3/5 cats", "0.60", "<b>0.97</b>", "nearly a mess"],
                 ["1/2 cats", "0.50", "<b>1.00</b>", "maximum mess"],
                 ["1/5 cats", "0.20", "<b>0.72</b>", "mostly not cats — same as 4/5!"],
                 ["0/5 cats", "0.00", "<b>0.00</b>", "perfectly pure"]])
        + """<p>The symmetry is worth pausing on: H(0.8) = H(0.2). Entropy does not care <em>which</em>
class dominates, only how lopsided the mix is. That is exactly what you want from a purity measure.</p>"""
        + note("""<p>Many libraries default to the <b>Gini impurity</b>, 2p(1−p), instead. It is cheaper to
compute (no logarithm), has almost the same shape, and gives nearly identical trees. Entropy is taught
because it has a clean information-theoretic meaning; Gini is used because it is fast.</p>""",
               "Gini vs entropy")

        + h2("🕳", "Traps")
        + trap("""<p><b>log(0) in code.</b> <code>0 * log(0)</code> is mathematically 0 but numerically NaN.
Guard it: <code>if p == 0 or p == 1: return 0</code>.</p>""")
        + trap("""<p><b>Using the wrong log base.</b> Base 2 gives bits and a maximum of 1. Natural log gives
nats and a maximum of 0.693. Splits come out identical either way — only the numbers on the page change.</p>""")

        + explain("""<p>Base 2 gives a maximum entropy of 1 and natural log gives 0.693, and the splits chosen come out
identical. <b>Say why the base cannot change which split wins.</b></p>""",
                  """<p>Changing the base multiplies every entropy by the same constant. Information gain is a difference
of entropies, so it is scaled by that same constant too — and scaling every candidate's score by one
positive number cannot change which is largest.</p>
<p>So the base is a choice of <em>units</em>, exactly like measuring in metres or feet. Bits are
conventional because they carry the clean information-theoretic reading: a 50/50 group costs one coin
flip of uncertainty.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("A node has 6 cats and 2 not-cats. What is p, and roughly what is H?",
             "<p>p = 6/8 = 0.75. H(0.75) = −0.75log₂0.75 − 0.25log₂0.25 ≈ <b>0.811</b>.</p>"),
            ("Why is H(0.8) equal to H(0.2)?",
             "<p>Because the formula is symmetric about p = 0.5. Impurity depends on how lopsided the "
             "mix is, not which class is on top.</p>"),
            ("Group A: 100 examples, all cats. Group B: 2 examples, both cats. Same entropy?",
             "<p>Yes — both are <b>0</b>. Entropy measures purity, not size. That is why information gain "
             "weights each branch by how many examples it holds.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("paper", "https://ieeexplore.ieee.org/document/6773024",
             "Shannon (1948) — A Mathematical Theory of Communication",
             "Where entropy comes from. One of the great scientific papers of the 20th century, and surprisingly readable."),
            ("video", "https://www.youtube.com/watch?v=YtebGVx-Fxw",
             "StatQuest — Entropy (for data science), clearly explained",
             "Entropy as “expected number of yes/no questions to identify the answer”, which is the deepest intuition for it."),
            ("docs", "https://scikit-learn.org/stable/modules/tree.html#mathematical-formulation",
             "scikit-learn — impurity criteria",
             "Gini, entropy and log-loss, side by side with the formulas."),
        ])
    )))

# ============================================================ 4
L.append(dict(
    slug="04-information-gain", title="Choosing a split: information gain", mins=12, tag="maths",
    lede="How much mess did this question remove? Compute it for every feature, take the biggest. That is "
         "the whole learning algorithm.",
    body=(
        pretest("""<p>A split leaves one branch with 9 examples and another with 1. <b>Guess why you cannot simply average the two branches' messiness.</b></p>""",
        """<p>Watch for the weighting by branch size. Dropping it makes a tiny pure branch look wonderful, and the tree chases it.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>You have a messy bag: 5 cats, 5 dogs. Mess level 1.0 — as bad as it gets.</p>
<p>You ask “pointy ears?” and now you have two bags: one with 4 cats and 1 dog (fairly tidy), one with
1 cat and 4 dogs (also fairly tidy). Total mess is now about 0.72.</p>
<p>You removed <b>0.28</b> of mess. That’s the information gain. Try all three questions, and keep whichever
removed the most.</p>
<p>One subtlety: a bag of 1 that’s perfectly tidy isn’t worth as much as a bag of 9 that’s perfectly tidy.
So you weight each bag by how many animals are in it.</p>""")

        + lenses(
            """<p>Twenty questions, and you get to ask one. You want to learn as much as you possibly can from
the answer.</p>
<p><b>“Is it alive?”</b> cuts the world roughly in half whichever way it goes. A brilliant question.
<b>“Is it a left-handed banjo?”</b> gets “no” essentially every time and leaves you exactly where you
started. Information gain is just the score that says the first question is worth asking and the
second is not — and it says it in a number, so a machine can compare them.</p>""",
            """<p>Statisticians know this quantity as the <b>reduction in entropy</b>, and it is identical to the
mutual information between the feature and the label.</p>
<p>If you have run a chi-square test to ask “is this variable associated with the outcome?”, you were
asking the same question with a different yardstick. The advantage of this one is that it is directly
comparable across features of completely different kinds — a yes/no and a 12-way category score
on the same scale, in bits.</p>""",
            """<p>Three numbers on a page. The entropy <b>before</b> the split. The two entropies <b>after</b>.
Gain is the first, minus the other two <em>weighted by how many examples fell each way</em>.</p>
<p>That subtraction is the entire criterion. One number per candidate feature, computed the same way
every time, and the algorithm keeps the biggest. There is nothing else in the box.</p>""",
            """<p>The weighting is the part that earns its money in production. A split that isolates 2 fraudulent
transactions out of 100,000 into a perfectly pure leaf looks spectacular if you ignore group size,
and it is noise.</p>
<p>Weighting by how many examples landed in each child is what stops a fraud model chasing single
transactions into leaves of their own. Dropping that weight is a genuine, common, and quiet bug: the
model still trains, still scores well on the data it memorised, and falls over in production.</p>""",
            """So the weighted sum in the formula below is not bookkeeping. It is what makes gain mean “tidier on
average” rather than “tidier somewhere”.""")

        + h2("🔢", "The maths, decoded")
        + eqp([
            'gain <span class="op">=</span> <var>H</var>(<var>p</var><sub>root</sub>) <span class="op">−</span> ',
            ('<span class="paren">(</span> <var class="hl-b">w</var><sup>left</sup><var>H</var>(<var>p</var><sup>left</sup>) <span class="op">+</span> <var class="hl-b">w</var><sup>right</sup><var>H</var>(<var>p</var><sup>right</sup>) <span class="paren">)</span>',
             "weighted-mean", "sized by how many examples went each way"),
        ], "mess before, minus weighted mess after — hover or click it")
        + decode([
            ("<var>H</var>(<var>p</var><sub>root</sub>)", "“mess before”", "Entropy of the node you are about to split."),
            ("<var class='hl-b'>w</var><sup>left</sup>", "“the weight of the left branch”", "Fraction of the examples that go left. 4 of 10 → 0.4. <b>This is the bit people forget.</b>"),
            ("the bracket", "“weighted mess after”", "The average entropy of the two children, weighted by size."),
            ("gain", "“mess removed”", "Always ≥ 0. Bigger is better. Measured in bits."),
        ])
        + key("""<p>Without the size weighting, splitting off a single example into its own perfectly pure
branch would look like a fantastic idea every time. The weights are what stop the tree from doing exactly
that.</p>""")

        + h2("🎬", "Watch it move")
        + demo("infogain", "All three candidate splits, scored",
               "each one is computed in full, then the winner is chosen")

        + h2("🧮", "The full calculation for ear shape")
        + """<p>Root: 5 cats, 5 not. p = 0.5, so H = <b>1.00</b>.</p>
<p>Split on ear shape:</p>
<ul>
<li><b>pointy</b>: 5 examples, 4 cats. p = 0.8, H = 0.7219. Weight = 5/10 = 0.5.</li>
<li><b>floppy</b>: 5 examples, 1 cat. p = 0.2, H = 0.7219. Weight = 5/10 = 0.5.</li>
</ul>
<p>Weighted entropy after = 0.5(0.7219) + 0.5(0.7219) = 0.7219.<br>
Gain = 1.00 − 0.7219 = <b>0.2781</b>.</p>"""
        + table(["Split on", "Left branch", "Right branch", "Weighted H", "Gain"],
                [["<b>ear shape</b>", "pointy: 4/5 cats", "floppy: 1/5 cats", "0.7219", "<b>0.28</b> ← winner"],
                 ["face shape", "round: 4/7 cats", "not round: 1/3 cats", "0.9651", "0.03"],
                 ["whiskers", "present: 3/4 cats", "absent: 2/6 cats", "0.8755", "0.12"]])

        + h2("💻", "In code")
        + code("""
import numpy as np

def entropy(y):
    if len(y) == 0:
        return 0.0
    p = np.mean(y)
    if p == 0 or p == 1:
        return 0.0                       # log(0) guard
    return -p * np.log2(p) - (1 - p) * np.log2(1 - p)

def information_gain(X, y, feature):
    left  = y[X[:, feature] == 1]
    right = y[X[:, feature] == 0]
    w_left  = len(left) / len(y)
    w_right = len(right) / len(y)
    return entropy(y) - (w_left * entropy(left) + w_right * entropy(right))

best = max(range(X.shape[1]), key=lambda f: information_gain(X, y, f))
""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Forgetting the weights.</b> Averaging the two entropies unweighted makes tiny pure
branches look wonderful. This is the single most common implementation bug in the assignment.</p>""")
        + trap("""<p><b>Bias towards many-valued features.</b> A feature with a unique value per example
(an ID column!) gives perfect purity and enormous gain, while being completely useless. C4.5 fixes this
with <em>gain ratio</em>; the practical fix is: never feed an ID column to a tree.</p>""")

        + explain("""<p>An ID column gives perfect purity and enormous information gain. <b>Say why gain — a correct
formula, correctly computed — recommends something useless.</b></p>""",
                  """<p>Because gain measures purity on the <b>training set only</b>, and it has no way to ask whether a
split will ever apply again. Every ID is unique, so splitting on it separates the data perfectly and
scores brilliantly.</p>
<p>A new customer arrives with an ID the tree has never seen, and the split is meaningless. The
formula is not wrong; it is answering &ldquo;does this tidy the data in front of me?&rdquo; when you
wanted &ldquo;will this generalise?&rdquo; — which is the whole reason held-out evaluation exists.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("A split gives left: 2 cats 0 not (weight 0.2), right: 3 cats 5 not (weight 0.8). Gain from H_root = 0.954?",
             "<p>H(left) = 0. H(right) = H(3/8) = 0.954. Weighted = 0.2(0) + 0.8(0.954) = 0.763. "
             "Gain = 0.954 − 0.763 = <b>0.191</b>.</p>"),
            ("Can information gain be negative?",
             "<p>No. Splitting can never increase weighted entropy — at worst the gain is 0, when the "
             "split separates nothing.</p>"),
            ("Why would a customer-ID feature score a perfect gain and still be useless?",
             "<p>Every leaf would hold one example and be perfectly pure, so the gain is maximal. But the "
             "rule “if ID = 4471 then cat” tells you nothing about a new customer. Pure memorisation.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("paper", "https://link.springer.com/article/10.1007/BF00116251",
             "Quinlan (1986) — Induction of Decision Trees",
             "ID3 in the original. The information-gain criterion, exactly as taught here."),
            ("book", "https://hastie.su.domains/ElemStatLearn/",
             "Elements of Statistical Learning, chapter 9",
             "The rigorous treatment of CART, including why the greedy criterion works as well as it does."),
            ("lab", "../../C2%20-%20Advanced%20Learning%20Algorithms/week4/C2W4A1/C2_W4_Decision_Tree_with_Markdown.ipynb",
             "Week 4 assignment",
             "In this repo. You implement entropy, split, and information gain from scratch."),
        ])
    )))

# ============================================================ 5
L.append(dict(
    slug="05-putting-it-together", title="Putting it together", mins=14, tag="core",
    lede="The full algorithm, which turns out to be four lines — because it calls itself.",
    body=(
        pretest("""<p>You can pick the best split. <b>Guess how the whole tree gets built from that</b> — and what tells you to stop.</p>""",
        """<p>Watch for the word recursion, and for the stopping rules that keep the tree from memorising.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>You split the messy box into two tidier boxes. Now here’s the trick: <b>each of those
boxes is just a smaller version of the same problem.</b> So you run exactly the same procedure on it.</p>
<p>That’s recursion — a set of instructions that includes “now do these instructions again, on a smaller
pile”. It stops when a pile is already tidy, or too small to be worth splitting.</p>""")

        + lenses(
            """<p>Dividing an estate. You split the whole into two shares. Now you treat each share as a brand-new
problem and divide it by the same rule.</p>
<p>The rule applied to a share is the <em>identical</em> rule you applied to the whole estate. Nothing
about it knows or cares whether it is running at the top or four levels down. That is the only idea
in this lesson, and everything else is bookkeeping.</p>""",
            """<p>This is recursion in its purest textbook form. If you have written a quicksort, walked a
directory tree, or parsed nested JSON, you have written this exact control flow: do one thing, call
yourself on each piece, stop at a base case.</p>
<p>Which means the interesting question is the one recursion always raises — <b>what is the base
case?</b> Here it is not a detail. It is every hyperparameter you will ever tune.</p>""",
            """<p>One function, drawn as a box, with two arrows leaving it that point back into copies of itself.</p>
<p>The tree on the page is <em>not</em> built by a loop that fills in level 1, then level 2. It is built
by one short function that calls itself twice and stops when told to. Picture the box, and the two
arrows curving back into it.</p>""",
            """<p><code>max_depth</code>, <code>min_samples_leaf</code>, <code>min_impurity_decrease</code> —
every one of these is the stopping condition of this recursion, wearing a different name.</p>
<p>They are also the entire difference between a model that generalises and one that has memorised
each customer individually. A tree left to recurse until every leaf is pure will hit 100% training
accuracy on any dataset with no duplicate rows, every time, and tell you nothing.</p>""",
            """So the algorithm below is four lines long only because recursion lets every level treat the other
levels as somebody else's problem.""")

        + h2("🎬", "Watch it move")
        + demo("treebuild", "The tree building itself, one level at a time",
               "the root split, then each branch treated as a brand-new problem")

        + h2("💻", "The algorithm")
        + code("""
def build_tree(examples, depth):
    # --- stopping criteria ---
    if all_same_class(examples):          return Leaf(examples[0].label)
    if depth >= MAX_DEPTH:                return Leaf(majority_class(examples))
    if len(examples) < MIN_SAMPLES:       return Leaf(majority_class(examples))

    # --- decision 1: which feature? ---
    feature = argmax(information_gain(examples, f) for f in features)
    if information_gain(examples, feature) < MIN_GAIN:
        return Leaf(majority_class(examples))

    # --- split and recurse ---
    left, right = split_on(examples, feature)
    return Node(feature,
                build_tree(left,  depth + 1),      # <- itself
                build_tree(right, depth + 1))      # <- itself
""")
        + decode([
            ("<code>build_tree</code> calling itself", "“recursion”", "The procedure for a branch is the same procedure as for the whole tree, on fewer examples."),
            ("<code>depth + 1</code>", "“one level deeper”", "How the recursion knows when to give up. Without it, it might never stop."),
            ("<code>Leaf(...)</code>", "“the base case”", "Every recursion needs a way to end. These three checks are it."),
            ("<code>majority_class</code>", "“best guess”", "When you stop early, predict whichever class is more common in the node."),
        ], head=("Piece", "Say it out loud", "What it does"))
        + key("""<p>Recursion is the natural shape here because a decision tree <b>is</b> recursive: every
subtree is itself a complete decision tree over a subset of the data.</p>""")

        + h2("🧮", "Following our example through")
        + """<ol>
<li>All 10 examples: 5 cats, 5 not. Best split = ear shape (gain 0.28).</li>
<li><b>Pointy</b> (5 examples, 4 cats). Best split = face shape → round: 4 cats, 0 not — <b>pure, leaf</b>;
not round: 0 cats, 1 not — <b>pure, leaf</b>.</li>
<li><b>Floppy</b> (5 examples, 1 cat). Best split = whiskers → present: 1 cat, 0 not — <b>pure, leaf</b>;
absent: 0 cats, 4 not — <b>pure, leaf</b>.</li>
<li>Every branch is pure. Done. Depth 2.</li>
</ol>
<p>On this toy dataset every leaf comes out pure, which is tidy but unusual. On real data you will hit a
depth or purity limit long before that.</p>"""

        + h2("🧮", "The second level, computed")
        + """<p>Ear shape won the root with a gain of 0.2781. Now <b>throw away everything else</b>
and treat the left branch as a brand-new problem: the five pointy-eared animals, four of which are
cats.</p>"""
        + table(["", "value"],
                [["examples at this node", "5 (indices 0, 3, 4, 5, 7)"],
                 ["p₁ at this node", "4/5 = 0.8"],
                 ["H at this node", "0.7219 — no longer 1.0, because the root split already tidied it"]])
        + """<p>Two features are left. Score them <em>on these five animals only</em>:</p>"""
        + table(["Split on", "left branch", "right branch", "gain"],
                [["<b>face shape</b>", "4 of 4 are cats — <b>pure</b>", "0 of 1 is a cat — <b>pure</b>",
                  "<b>0.7219</b> ← winner"],
                 ["whiskers", "2 of 3 are cats", "2 of 2 are cats", "0.1710"]])
        + """<p>Face shape removes <em>all</em> the remaining entropy — 0.7219 of it, leaving 0.0000 —
so both children are perfectly pure and become leaves. That branch of the tree is finished after two
questions.</p>
<p>Notice what changed: at the root, face shape was the <b>worst</b> feature, scoring 0.0349. Five
animals later it is the best, scoring 0.7219. A feature is not good or bad in itself — it is good or
bad <em>at a particular node</em>, given what the splits above it have already separated. That is
why the algorithm re-scores every feature at every node instead of ranking them once.</p>"""
        + explain("""<p>Face shape went from the worst split available (0.0349) to the best (0.7219)
without a single one of its own values changing. <b>Why?</b></p>""",
                  """<p>Because entropy is a property of the <em>group</em>, not of the feature. At the
root, face shape cut across a 50/50 mix and produced two branches that were still nearly 50/50 —
it separated nothing. After the ear split, the five remaining animals are already 80% cats, and
within that smaller, more homogeneous group, face shape happens to align exactly with the one
non-cat. The feature did not improve; the question it was being asked to answer got easier, because
another feature had already removed the confusion it could not.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Recursing on the wrong subset.</b> The left branch must recurse on the left
examples only. Passing the full set is an easy typo and produces infinite recursion.</p>""")
        + trap("""<p><b>No depth limit.</b> Guaranteed overfitting, and on adversarial data, a stack
overflow.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("Why is the algorithm naturally recursive?",
             "<p>Because each branch is a smaller instance of the identical problem: a set of examples "
             "needing a tree.</p>"),
            ("A node has 4 cats and 4 not, and every possible split gives gain 0. What now?",
             "<p>Make it a leaf. No split separates anything, so predict the majority — here a tie, so "
             "either class, and accept 50% error on that node.</p>"),
            ("With max_depth = 1, what can the tree learn?",
             "<p>A single question. That is a “decision stump” — high bias, but it is exactly what "
             "boosting uses as its building block.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("docs", "https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html",
             "sklearn.tree.DecisionTreeClassifier",
             "The production version. Read <code>max_depth</code>, <code>min_samples_leaf</code>, <code>criterion</code>."),
            ("lab", "../../C2%20-%20Advanced%20Learning%20Algorithms/week4/C2W4A1/C2_W4_Decision_Tree_with_Markdown.ipynb",
             "Week 4 assignment",
             "You write build_tree yourself, recursion and all."),
        ])
    )))

# ============================================================ 6
L.append(dict(
    slug="06-one-hot-encoding", title="Using one-hot encoding of categorical features", mins=12, tag="core",
    lede="What to do when a feature has three values instead of two — and why this trick matters for "
         "neural networks too.",
    body=(
        pretest("""<p>Ear shape is pointy, floppy or oval. You encode them as 1, 2, 3. <b>Guess what you have accidentally told the model.</b></p>""",
        """<p>Watch for the false ordering, and for the encoding that avoids it by using three columns instead of one.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>So far every question had two answers: pointy or floppy. Easy — two branches.</p>
<p>But what if ears can be pointy, floppy <b>or</b> oval? You could make three branches. Or you can play a
trick: replace the one question with <b>three yes/no questions</b>.</p>
<p>“Pointy? yes/no.” “Floppy? yes/no.” “Oval? yes/no.” Exactly one of them is yes for every animal. Now
everything is back to two branches and nothing else has to change.</p>""")

        + lenses(
            """<p>A form asks for your country and gives you one box to write a <em>number</em> in. So someone
draws up a list: Albania 1, Brazil 2, and on to Zimbabwe at 195.</p>
<p>The form now quietly believes Zimbabwe is 195 times Albania, and that Brazil sits neatly between
them. Nothing whatsoever about those countries says that — the ordering came from the alphabet.
Replace the one box with 195 tick-boxes, tick exactly one, and the invented arithmetic vanishes.</p>""",
            """<p>Econometricians have called these <b>dummy variables</b> for a century; survey researchers call it
indicator coding. Same object.</p>
<p>One difference is worth carrying across, because it trips people up: in a linear regression you
<em>drop</em> one level, or the columns are perfectly collinear and the fit has no unique solution.
For trees and neural networks you normally keep all of them, because neither cares.</p>""",
            """<p>One column of words becoming <var>k</var> columns of 0s and 1s, with exactly one 1 in every row.</p>
<p>Lay the two side by side on paper. Identical information; no invented ordering. The name is a
literal description of what you are looking at — one bit hot, the rest cold.</p>""",
            """<p>This is where high-cardinality columns quietly destroy models. One-hot a UK postcode column and
you have roughly 1.7 million new columns.</p>
<p>The tree then splits on “is the postcode exactly SW1A 1AA”, memorises the training set, and scores
beautifully in validation <em>if the same postcodes appear there</em>. Every serious feature pipeline
has an explicit cardinality rule for this reason, and target- or hash-encoding exists because of
it.</p>""",
            """So one-hot is not a trick to memorise. It is what you do when a column's numbers were never
quantities in the first place.""")

        + h2("🎬", "Watch it move")
        + demo("onehot", "One column with three values becomes three columns of 0/1",
               "exactly one column is “hot” in every row")

        + h2("🔢", "The maths, decoded")
        + decode([
            ("one-hot", "“exactly one is on”", "A vector of k values where one entry is 1 and the rest are 0. “Hot” means on, as in electronics."),
            ("k values → k columns", "“one column per category”", "Three ear shapes become three binary features."),
            ("why not just 0, 1, 2?", "“ordinal encoding”", "Because that tells the model oval (2) is “more” than pointy (0), and twice floppy (1). For unordered categories that is a lie."),
            ("dummy variables", "“the statistics name”", "The same thing. Statisticians often drop one column (k−1) to avoid collinearity; for trees and networks, keep all k."),
        ])
        + key("""<p>One-hot encoding is not a tree technique — it is how you feed <b>any</b> categorical
feature into <b>any</b> algorithm that expects numbers. You will use it for neural networks constantly.</p>""")

        + h2("💻", "In code")
        + code("""
import pandas as pd

df = pd.DataFrame({'ear': ['pointy', 'floppy', 'oval', 'pointy']})
pd.get_dummies(df, columns=['ear'], dtype=int)
#    ear_floppy  ear_oval  ear_pointy
# 0           0         0           1
# 1           1         0           0
# 2           0         1           0
# 3           0         0           1
""")

        + h2("🧮", "Encoded, and scored")
        + """<p>Suppose ear shape has three values, not two: pointy, floppy, oval. One-hot turns one
column into three 0/1 columns, exactly one of which is 1 per row. Score each:</p>"""
        + table(["Encoded feature", "left branch (=1)", "right branch (=0)", "gain"],
                [["is_pointy", "4 of 5 cats", "1 of 5 cats", "<b>0.2781</b>"],
                 ["is_floppy", "1 of 3 cats", "4 of 7 cats", "0.0349"],
                 ["is_oval", "<b>0 of 2 cats</b> — pure", "5 of 8 cats", "0.2365"]])
        + """<p>The tree now has three ordinary binary questions to choose from and picks
<code>is_pointy</code>. Nothing else about the algorithm changes — which is the entire point of
one-hot encoding.</p>"""
        + warn("""<p>An honest wrinkle. Splitting three ways <em>at once</em> — one branch per value —
scores a gain of <b>0.3635</b>, higher than any of the three binary splits. Multi-way splits almost
always score higher, because more branches means smaller, purer groups. That is not the tree finding
something better; it is the bias towards many-valued features. Keeping every split binary is what
stops that bias from running away, and a two-level binary tree can reach the same partition
anyway.</p>""")
        + explain("""<p>One-hot on a 3-value feature produces three columns, but you could identify
all three values with two columns (00, 01, 10). <b>Why use the redundant third?</b></p>""",
                  """<p>Because with two columns the tree can only ask “is bit 1 set?” — a question
about an arbitrary encoding, not about the data. “Is it oval?” would no longer be a single available
split; it would have to be reconstructed from a combination the tree may never find. The redundancy
is the point: one-hot guarantees every <em>category</em> gets its own directly askable question, and
for trees that matters more than the wasted column. (In linear models, where the redundancy causes
collinearity, you do drop one.)</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Ordinal encoding unordered categories.</b> Mapping {red, green, blue} → {0,1,2}
tells the model blue is bigger than red. For genuinely ordered categories (small &lt; medium &lt; large)
ordinal encoding is correct and better.</p>""")
        + trap("""<p><b>High-cardinality explosion.</b> A postcode feature with 10,000 values becomes
10,000 columns. Use target encoding, hashing, or embeddings instead.</p>""")
        + trap("""<p><b>Fitting the encoder on train and test together.</b> If a category appears only in
test, your encoder must already know how to handle it (<code>handle_unknown='ignore'</code>).</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("A colour feature with 4 values. How many columns after one-hot?",
             "<p><b>4</b> columns, exactly one of which is 1 per row. (Statisticians often use 3 to avoid "
             "perfect collinearity; for trees and neural networks, 4 is standard.)</p>"),
            ("Why is one-hot needed for neural networks and not just trees?",
             "<p>Because a network computes w·x + b — it must have numbers, and it would treat an ordinal "
             "code as a quantity with an order and a magnitude.</p>"),
            ("T-shirt sizes S, M, L. One-hot or ordinal?",
             "<p><b>Ordinal</b> (1, 2, 3) is fine and often better here — the order is real and "
             "meaningful. One-hot throws that information away.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("docs", "https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OneHotEncoder.html",
             "sklearn.preprocessing.OneHotEncoder",
             "The production tool. Note <code>handle_unknown</code> and <code>drop</code>."),
            ("docs", "https://pandas.pydata.org/docs/reference/api/pandas.get_dummies.html",
             "pandas.get_dummies",
             "The quick version for exploration."),
            ("docs", "https://scikit-learn.org/stable/modules/preprocessing.html#encoding-categorical-features",
             "scikit-learn — encoding categorical features",
             "Including ordinal and target encoding, and when each is right."),
        ])
    )))

# ============================================================ 7
L.append(dict(
    slug="07-continuous-features", title="Continuous valued features", mins=14, tag="core",
    lede="Weight in pounds is not a category. The fix: turn “which value?” into “is it above a threshold?” "
         "and try every threshold.",
    body=(
        pretest("""<p>Weight is a number, not a category — there are infinitely many possible splits. <b>Guess how the algorithm picks one.</b></p>""",
        """<p>Watch for how few candidate thresholds actually need testing.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Weight isn’t pointy-or-floppy. It’s 7.2, or 8.4, or 20 — endless possibilities.</p>
<p>So you don’t ask “what does it weigh?”. You ask “<b>does it weigh less than 10 pounds?</b>” — which is
back to yes/no.</p>
<p>But where do you put the line? You try every sensible place, score each one with information gain, and
keep the best. The computer doesn’t mind; there are only a handful of places worth trying.</p>""")

        + lenses(
            """<p>A market inspector grading melons, with nothing but a two-pan balance and a box of standard
weights. She cannot ask “how heavy is this?” — the balance does not tell her that. She can only
ask <b>“is it heavier than this weight?”</b></p>
<p>So she tries the 1 kg, the 1.5, the 2, and keeps whichever one best separates the ripe from the
unripe. The continuous quantity never becomes a number she reads off. It becomes a <em>threshold she
tests</em>.</p>""",
            """<p>If you have ever set a clinical cut-off — troponin above 14 ng/L means investigate —
you have chosen a threshold on a continuous variable to force a binary decision.</p>
<p>Two things differ here. The algorithm chooses the cut-off rather than a committee, and it chooses
it with the <em>same</em> criterion it uses for everything else. No new machinery arrives for
continuous features; only a longer list of candidate questions.</p>""",
            """<p>Sort the examples by that one feature and lay them in a row, with their labels written
underneath.</p>
<p>Every gap between two neighbouring values is a candidate threshold. Walk along the row, score each
gap with the gain you already know, keep the best. That row of sorted values <em>is</em> the whole
procedure — there is no formula to learn here, only a loop.</p>""",
            """<p>This step is why fitting a tree costs O(<var>n</var> log <var>n</var>) per feature rather than
O(<var>n</var>) — the sort dominates.</p>
<p>It is also, almost single-handedly, why LightGBM is fast: at a billion rows you stop considering
every gap and bucket the values into a histogram of 255 bins instead. The speed difference that made
gradient boosting practical on large data is this one decision, taken differently.</p>""",
            """So “try every midpoint and take the best gain” is that inspector, working patiently through her box
of weights.""")

        + h2("🎬", "Watch it move")
        + demo("contsplit", "Slide the threshold and watch the information gain",
               "the curve underneath is the gain at every possible threshold")

        + h2("🔢", "The maths, decoded")
        + eqp([
            'split condition: ',
            ('<var>x</var><sub>weight</sub>', "func-f", "the continuous feature, as it arrives"),
            ' <span class="op">≤</span> ',
            ('<var class="hl-a">t</var>', "sq-distance", "the threshold the algorithm chooses"),
        ], "one threshold turns a number into a yes/no question — hover or click a part", small=True)
        + decode([
            ("<var class='hl-a'>t</var>", "“the threshold”", "The cut point. Chosen by the algorithm, not by you."),
            ("m − 1 candidates", "“the thresholds worth trying”", "Sort the values; the only useful cut points are midway between consecutive distinct values. 10 examples → at most 9 candidates."),
            ("re-used features", "“a feature can appear twice”", "Unlike a binary feature, weight can be split at 10 lb near the top and again at 15 lb further down."),
            ("no scaling needed", "“only the order matters”", "Trees compare values; they never add them. Converting pounds to kilograms changes nothing about the tree."),
        ])
        + key("""<p>This is why trees need <b>no feature scaling at all</b> — a genuine practical advantage
over neural networks, and one of the reasons they are so easy to use on messy real-world tables.</p>""")

        + h2("🧮", "The procedure")
        + """<ol>
<li>Sort the examples by that feature.</li>
<li>Consider each midpoint between consecutive distinct values as a candidate threshold.</li>
<li>For each candidate, split and compute the information gain, exactly as before.</li>
<li>Keep the best threshold, and its gain, as this feature’s score.</li>
<li>Then compare that score against every other feature, as usual.</li>
</ol>
<p>A continuous feature therefore costs more to evaluate (m−1 gain calculations instead of 1) but is
otherwise treated identically. Nothing about the rest of the algorithm changes.</p>"""

        + h2("🧮", "The threshold sweep, in full")
        + """<p>Give the same ten animals a weight in pounds and the tree cannot ask “is weight = 1?”
— it has to find a cut. So it sorts the values, tries the midpoint between each neighbouring pair,
and scores every one:</p>"""
        + table(["threshold", "left (≤)", "right (>)", "gain"],
                [["w ≤ 7.40", "1 of 1 cats", "4 of 9 cats", "0.1080"],
                 ["w ≤ 8.00", "2 of 2 cats", "3 of 8 cats", "0.2365"],
                 ["w ≤ 8.60", "3 of 3 cats", "2 of 7 cats", "0.3958"],
                 ["<b>w ≤ 9.00</b>", "<b>4 of 4 cats</b>", "1 of 6 cats", "<b>0.6100</b> ← best"],
                 ["w ≤ 9.70", "4 of 5 cats", "1 of 5 cats", "0.2781"],
                 ["w ≤ 10.60", "5 of 6 cats", "<b>0 of 4 cats</b>", "<b>0.6100</b> ← ties"],
                 ["w ≤ 13.00", "5 of 7 cats", "0 of 3 cats", "0.3958"],
                 ["w ≤ 16.50", "5 of 8 cats", "0 of 2 cats", "0.2365"],
                 ["w ≤ 19.00", "5 of 9 cats", "0 of 1 cats", "0.1080"]])
        + """<p>Two things worth noticing. First, the winning threshold scores <b>0.6100</b> — more
than twice ear shape’s 0.2781. A well-chosen continuous cut can easily beat every categorical
feature, which is why you never bucket a continuous variable by hand before giving it to a tree.</p>
<p>Second, w ≤ 9.00 and w ≤ 10.60 tie exactly. One isolates a pure group of cats, the other a pure
group of non-cats, and entropy does not care which class a pure branch is pure in. Implementations
break the tie by taking whichever comes first.</p>
<p>The cost: with <var>m</var> examples there are up to <var>m</var> − 1 thresholds to score per
feature, so this step is the reason tree training is dominated by sorting.</p>"""
        + explain("""<p>The gains rise to a peak and fall away symmetrically — 0.108, 0.237, 0.396,
0.610, then back down through 0.396, 0.237, 0.108. <b>Why that shape?</b></p>""",
                  """<p>Because the weights happen to separate the classes almost perfectly, so a
threshold’s gain depends mostly on how <em>far it is from the true dividing line</em>. Cut far to
one side and you peel off a tiny pure sliver — pure, but weighted by almost nothing, so the gain is
small. Move towards the boundary and each cut peels off more while staying pure, so the gain grows.
Past the boundary the same thing happens in reverse. The peak sits where the split matches the
structure actually in the data — which is exactly what you want a gain to measure.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Trying every real number.</b> Pointless — the gain only changes when the threshold
crosses a data point. Sorting and using midpoints reduces infinity to m−1 candidates.</p>""")
        + trap("""<p><b>Assuming a single threshold captures the feature.</b> If cats are <em>medium</em>
weight — heavier than kittens, lighter than dogs — one cut cannot express that. Two splits at different
depths can.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("You have 100 examples with 100 distinct weights. How many thresholds are worth testing?",
             "<p><b>99</b> — one between each pair of consecutive sorted values.</p>"),
            ("Why do trees not need feature scaling?",
             "<p>Because they only ever <em>compare</em> feature values against a threshold. Scaling "
             "preserves order, so it preserves every split the tree could make.</p>"),
            ("Cats weigh 8–12 lb; everything else is under 6 or over 15. Can one threshold separate them?",
             "<p>No. You need two: “> 6 lb?” and then “≤ 12 lb?”. Trees express intervals by stacking "
             "splits on the same feature at different depths.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("docs", "https://scikit-learn.org/stable/modules/tree.html#mathematical-formulation",
             "scikit-learn — how splits are chosen",
             "The exact candidate-threshold procedure, in the docs."),
            ("paper", "https://arxiv.org/abs/cs/9603103",
             "Quinlan (1996) — Improved Use of Continuous Attributes in C4.5",
             "The refinement that made continuous features work well in practice."),
        ])
    )))

# ============================================================ 8
L.append(dict(
    slug="08-regression-trees", title="Regression trees", mins=10, tag="core",
    lede="Predicting a number instead of a class. One substitution — variance for entropy — and everything "
         "else is unchanged.",
    body=(
        pretest("""<p>Instead of “is it a cat?”, predict how much it weighs. <b>Guess what a leaf should predict, and what replaces “are these the same class?” when choosing splits.</b></p>""",
        """<p>Watch for the mean at the leaves and variance as the impurity measure. One substitution converts the whole algorithm.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Same tree, different question. Instead of “is it a cat?”, you want “how much does it
weigh?”.</p>
<p>Two changes. At the bottom, instead of naming a class, you say the <b>average weight</b> of everything
that landed there. And when choosing a split, instead of asking “are these all the same class?” you ask
“are these weights all <b>close to each other</b>?”.</p>
<p>“All close together” has a name: low variance. That’s the only new word.</p>""")

        + lenses(
            """<p>An auction valuer, asked what your chair is worth. She does not compute anything. She puts it in
a group — <b>Victorian, mahogany, damaged, no provenance</b> — and quotes what that group
of chairs has been fetching. “Two to three hundred.”</p>
<p>The number comes from the group, not from your chair. Two chairs in the same group get the same
estimate even if one is visibly nicer, and the only way to get a different number is to land in a
different group.</p>""",
            """<p>Formally this is a <b>piecewise-constant</b> fit, or a step function.</p>
<p>Anyone who has used banded rates — income tax brackets, postage by weight class, insurance
age bands — has used exactly this model daily without calling it one. The tree's only extra
trick is that it <em>chooses</em> where the bands go instead of taking them from legislation.</p>""",
            """<p>A scatter plot with a <b>staircase</b> drawn through it instead of a line. Flat within each
region, jumping at the boundaries.</p>
<p>The tree decides where the jumps go. The height of each step is nothing cleverer than the average
of the points sitting underneath it. Picture the staircase, and you have the model.</p>""",
            """<p>The staircase is exactly why trees <b>cannot extrapolate</b>. A house-price tree trained on homes
up to 400 m² will quote the 400 m² price for a 2,000 m² mansion, for ever, because no step exists
beyond the last one.</p>
<p>A linear model would happily extrapolate — often to something absurd, like a negative price.
Which behaviour you want is a real engineering decision, and in safety-critical settings “refuses to
guess outside what it has seen” is sometimes the feature rather than the bug.</p>""",
            """So swapping entropy for variance below does not change the algorithm at all. It changes what the
word “tidy” measures.""")

        + h2("🎬", "Watch it move")
        + demo("regtree", "Predicting weight — click the three candidate splits",
               "variance reduction replaces information gain, and leaves predict the mean")

        + h2("🔢", "The maths, decoded")
        + eqp([
            ('variance <span class="op">=</span> <span class="frac"><span>1</span><span><var>m</var></span></span> <span class="big">Σ</span> ( <var>y</var><sup>(<var>i</var>)</sup> <span class="op">−</span> <var>ȳ</var> )<sup>2</sup>',
             "variance-f0", "average squared distance from the mean"),
        ], "how spread out the numbers in this node are — hover or click it", small=True)
        + eqp([
            'reduction <span class="op">=</span> var(root) <span class="op">−</span> ',
            ('<span class="paren">(</span> <var>w</var><sup>left</sup>var(left) <span class="op">+</span> <var>w</var><sup>right</sup>var(right) <span class="paren">)</span>',
             "weighted-mean", "sized by how many examples went each way"),
        ], "exactly the information-gain formula, with variance swapped in — hover or click it")
        + decode([
            ("<var>ȳ</var>", "“y bar”", "The mean of all the y-values in this node — plain average, the bar just marks “the average of”."),
            ("(<var>y</var><sup>(i)</sup> − <var>ȳ</var>)²", "“squared distance from the mean”", "Same shape as the cost function from Course 1: how far each value sits from the average, squared so far-out values count more."),
            ("<var>w</var><sup>left</sup>, <var>w</var><sup>right</sup>", "“the fraction of examples on each side”", "Not the model's weights — just what share of the node's examples went left vs. right. Same w<sup>left</sup>/w<sup>right</sup> weighting used for entropy two lessons ago."),
        ])
        + table(["", "Classification tree", "Regression tree"],
                [["Label is", "a class (cat / not cat)", "a number (weight)"],
                 ["Impurity measure", "entropy H(p)", "<b>variance</b>"],
                 ["Split criterion", "information gain", "<b>variance reduction</b>"],
                 ["Leaf predicts", "the majority class", "<b>the mean</b> of the examples there"],
                 ["Everything else", "recursion, stopping, one-hot, thresholds", "identical"]])
        + key("""<p>Entropy measures “are these all the same <em>label</em>?”. Variance measures “are these
all the same <em>number</em>?”. Same job, different data type — and that single substitution converts the
whole algorithm.</p>""")

        + h2("🧮", "Worked, on the ten animals")
        + """<p>All ten weights: mean 11.54 lb, variance 18.46.</p>
<ul>
<li><b>Split on ear shape</b> → pointy {7.2, 8.8, 9.2, 8.4, 7.6} mean 8.24, variance 0.55; floppy
{10.2, 15, 18, 11, 20} mean 14.84, variance 14.58.<br>
Weighted variance = 0.5(0.55) + 0.5(14.58) = 7.57. Reduction = 18.46 − 7.57 = <b>10.89</b>.</li>
</ul>
<p>The demo computes the other two features live. Ear shape wins here as well — the light animals really
do have pointy ears in this toy dataset.</p>"""
        + code("""
weights = np.array([7.2, 8.8, 9.2, 8.4, 7.6, 10.2, 15, 18, 11, 20])
pointy  = np.array([7.2, 8.8, 9.2, 8.4, 7.6])
floppy  = np.array([10.2, 15, 18, 11, 20])

def variance(y):
    return np.sum((y - np.mean(y))**2) / len(y)

root = variance(weights)
split = (len(pointy)/len(weights)) * variance(pointy) + (len(floppy)/len(weights)) * variance(floppy)
reduction = root - split
np.round([root, split, reduction], 2)   # [18.46, 7.57, 10.89] -- matches the hand-worked numbers above
""")
        + note("""<p>A regression tree predicts a <b>step function</b>: constant within each leaf, jumping
at the split boundaries. It cannot extrapolate beyond the range of the training data — ask it about a
50 lb animal and it will confidently return the mean of the heaviest leaf it has. Neural networks and
linear models extrapolate (often badly, but they do).</p>""", "What a regression tree can’t do")

        + explain("""<p>Entropy was replaced by variance and everything else stayed. <b>Why does that one substitution convert the whole algorithm?</b></p>""",
            """<p>Because the tree only ever asked one question of a split: are the groups more uniform afterwards? Entropy answers that for labels, variance answers it for numbers. Swap the measure of uniformity and every other part — recursion, weighting, stopping — is untouched.</p>""")
        + h2("🕳", "Traps")
        + trap("""<p><b>Expecting smooth predictions.</b> The output is piecewise constant. If you need a
smooth curve, a tree is the wrong shape of model — or you need an ensemble, which averages many step
functions into something much smoother.</p>""")
        + trap("""<p><b>Extrapolating.</b> Outside the training range, a tree returns a constant. This
matters for time-series and price prediction, where tomorrow is often outside yesterday’s range.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("A leaf holds weights [10, 12, 14]. What does it predict, and what is its variance?",
             "<p>Predicts the mean, <b>12</b>. Variance = ((−2)² + 0² + 2²)/3 = <b>2.67</b>.</p>"),
            ("Why variance rather than entropy for regression?",
             "<p>Entropy needs discrete classes to count. Variance measures the spread of continuous "
             "values — the natural analogue of “how mixed up is this group?”.</p>"),
            ("Your regression tree predicts the same number for every input in a wide range. Bug?",
             "<p>No — that is exactly how a tree behaves. It is a step function, constant within each "
             "leaf. If the steps are too coarse, allow more depth or use an ensemble.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("docs", "https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeRegressor.html",
             "sklearn.tree.DecisionTreeRegressor",
             "Note <code>criterion='squared_error'</code> — that is variance reduction under another name."),
            ("docs", "https://scikit-learn.org/stable/auto_examples/tree/plot_tree_regression.html",
             "scikit-learn — decision tree regression, plotted",
             "The step-function shape, drawn. One picture and the whole lesson lands."),
        ])
    )))

# ============================================================ 9
L.append(dict(
    slug="09-using-multiple-trees", title="Using multiple decision trees", mins=13, tag="intuition",
    lede="A single tree is fragile: change one example and the whole thing can rearrange. The fix is not a "
         "better tree — it is more trees.",
    body=(
        pretest("""<p>Change one training example and a decision tree can come out completely different. <b>Guess how you would turn that fragility into an advantage.</b></p>""",
        """<p>Watch for the idea of a vote, and for why many unstable trees beat one careful one.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>One judge can have a bad day. Ask three judges and take the majority, and one bad day
doesn’t decide the contest.</p>
<p>Decision trees have a lot of bad days. Swap a single animal in the training set and the root question
can change from “pointy ears?” to “whiskers?” — and because every question below the root depends on the
root, the whole tree rearranges.</p>
<p>So: build lots of trees, all slightly different, and let them vote.</p>""")

        + lenses(
            """<p>There is a rattle in your car. One mechanic listens and says wheel bearing. You are not
convinced.</p>
<p>So you take it to three more, separately, and crucially <b>without telling any of them what the
first one said</b>. Three say bearing, one says exhaust bracket. You replace the bearing. No
individual mechanic became more skilled — you exploited the fact that their mistakes were
<em>different</em> mistakes.</p>""",
            """<p>You may know this as the wisdom-of-crowds effect, or from averaging forecasts, or from Galton's
ox at the county fair.</p>
<p>And you probably know the condition everyone forgets when they repeat the story: the errors have
to be <b>uncorrelated</b>. Four mechanics trained in the same garage by the same man are not four
mechanics. They are one mechanic, consulted four times, and averaging them buys you nothing.</p>""",
            """<p>Ten small trees drawn side by side, the same new animal fed into each one, each shouting a label,
and a tally box underneath.</p>
<p>The tally is the prediction. That is the entire ensemble — no weighting, no cleverness, just
a vote. Everything in the next three lessons is about making those ten trees disagree honestly.</p>""",
            """<p>Nearly every winning entry on a tabular Kaggle problem, and a very large share of credit scoring
and insurance pricing in production, is an ensemble rather than a single tree.</p>
<p>The reason is economic as much as statistical: the accuracy you gain by averaging is usually
larger, and always cheaper, than the accuracy you gain by tuning any one model harder. That is why
“start with gradient boosting” is genuinely good first advice for anything shaped like a
spreadsheet.</p>""",
            """So the rest of the week answers exactly one question: how do you build trees that get
<em>different</em> things wrong?""")

        + h2("🎬", "Watch it move")
        + demo("ensemble", "Three trees, one vote",
               "press the button: one changed example flips a whole tree, and the ensemble shrugs")

        + h2("🔢", "Why trees are high variance")
        + """<p>The root split is chosen by a single argmax over information gains. If two features score
0.281 and 0.278, a tiny change in the data flips which one wins — and everything below the root is then
built on a different foundation.</p>
<p>In Week 3’s vocabulary: a deep decision tree is a <b>low bias, high variance</b> model. It can fit
almost anything, and it is unstable. Week 3 also told you what fixes variance: more data, or averaging.
Ensembles are averaging.</p>"""
        + decode([
            ("ensemble", "“a committee”", "Several models whose predictions are combined."),
            ("majority vote", "“most trees win”", "For classification. For regression, take the average of the predictions."),
            ("variance reduction", "“errors cancel”", "If trees make <em>independent</em> errors, averaging B of them cuts the error variance by roughly a factor of B."),
            ("independence", "“the catch”", "Trees trained on the same data are highly correlated. Lessons 10–11 are entirely about forcing them to differ."),
        ])
        + key("""<p>Averaging only helps if the models make <b>different</b> mistakes. Three identical trees
vote identically and you have gained nothing. That is why the next two lessons are about deliberately
injecting randomness.</p>""")

        + h2("🧮", "How unstable is one tree? Change a single label")
        + """<p>This is worth doing rather than believing. Take the ten animals, flip <b>one</b>
label, and recompute the root split:</p>"""
        + table(["Dataset", "ear shape", "face shape", "whiskers", "root becomes"],
                [["original", "<b>0.278</b>", "0.035", "0.125", "<b>ear shape</b>"],
                 ["flip example 5", "0.125", "0.006", "<b>0.256</b>", "<b>whiskers</b>"],
                 ["flip example 7", "0.125", "0.006", "<b>0.256</b>", "<b>whiskers</b>"]])
        + """<p>One label out of ten — a single animal relabelled — and the tree asks a completely
different first question. Everything below the root is then built on a different foundation, so the
entire tree changes shape.</p>
<p>That is what “high variance” means, made concrete. It is not that trees are inaccurate; the
original tree fits its data perfectly. It is that the tree you get is a fact about <em>this
sample</em> rather than about cats, and a slightly different sample would have produced a
substantially different model. Averaging many trees built on many resamples is the direct answer to
exactly this problem.</p>"""
        + explain("""<p>A change at the root propagates through the whole tree, but a change deep in
one branch usually does not. <b>Why is a tree so much more fragile at the top?</b></p>""",
                  """<p>Because the algorithm is <em>greedy and sequential</em>: every node is chosen
given the split above it, and never revisited. A different root sends different subsets down each
side, so every subsequent question is being asked of a different group — the damage compounds with
depth. A change deep down only affects the handful of examples that reached that node. This is also
why trees cannot recover from a bad early split: nothing in the algorithm ever goes back and
reconsiders it.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("Why is one deep decision tree high variance?",
             "<p>Because every split depends on the ones above it, so a small change near the root "
             "cascades through the whole tree.</p>"),
            ("You train 100 trees on identical data with an identical algorithm. How much does the ensemble help?",
             "<p><b>Not at all.</b> They are identical, so they vote identically. You need a source of "
             "difference — which is the next lesson.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("paper", "https://link.springer.com/article/10.1007/BF00058655",
             "Breiman (1996) — Bagging Predictors",
             "The paper that introduced the whole idea. Short, clear, and the experiments are convincing."),
            ("docs", "https://scikit-learn.org/stable/modules/ensemble.html",
             "scikit-learn — ensemble methods",
             "The full map: bagging, forests, boosting, stacking, voting."),
        ])
    )))

# ============================================================ 10
L.append(dict(
    slug="10-sampling-with-replacement", title="Sampling with replacement", mins=13, tag="maths",
    lede="The trick that manufactures many different training sets out of the one you have.",
    body=(
        pretest("""<p>You have 10 examples and want many different training sets from them. <b>Guess how, without collecting more data.</b></p>""",
        """<p>Watch for putting each drawn example back. Watch also for roughly what fraction of the originals each new bag ends up containing.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Put ten marbles in a bag. Pull one out, write down its colour, and <b>put it back</b>.
Do that ten times.</p>
<p>You now have a list of ten marbles — but not the same ten. Some appear twice or three times. Some never
came out at all. It’s the same bag, and it is a genuinely different list.</p>
<p>Do the whole thing again and you get another different list. That is how you turn one training set into
a hundred slightly different training sets — without collecting any new data.</p>""")

        + lenses(
            """<p>A cook tasting a pot of stew. She takes a spoonful, tastes it, and <b>tips it back in</b>. Then
another spoonful — which may well catch the same piece of carrot again.</p>
<p>Ten spoonfuls, each judged on its own, tell her far more about the pot than one careful spoonful
would. And the tipping-back is what keeps it the same pot every time: she is not slowly eating her
way through the evidence.</p>""",
            """<p>This is <b>the bootstrap</b>, Efron 1979, borrowed wholesale.</p>
<p>If you have ever put a confidence interval on a statistic with no clean formula — a median, a
ratio of two means, an AUC — you resampled with replacement for precisely this reason. The
trees are new; the resampling is a forty-year-old idea from statistics doing its usual job.</p>""",
            """<p>A bag of ten numbered marbles. Draw one, write the number down, <b>put it back</b>. Do that ten
times.</p>
<p>Your list has ten entries. Some numbers appear twice, some not at all — and on average about
<b>63%</b> of the original marbles show up at least once. That list is one training set. Do it again
and you get a different one, from the same bag.</p>""",
            """<p>The ~37% left out of each draw are not waste. They are the <b>out-of-bag</b> sample, and a random
forest scores each tree on exactly the examples that tree never saw.</p>
<p>That gives you a validation estimate for free, with no held-out set at all. On a clinical study
with 300 patients, where surrendering 60 of them to a test set genuinely hurts, that free estimate is
worth more than any accuracy gain the forest brings.</p>""",
            """So “with replacement” is not a technicality to skim. It is the only reason the ten datasets differ
at all.""")

        + h2("🎬", "Watch it move")
        + demo("bagging", "Draw a new bag, and see who got duplicated and who got left out",
               "press the button a few times — the composition changes every time")

        + h2("🔢", "The maths, decoded")
        + eqp([
            ('P(a given example is never picked)', "probability-f0", "a number from 0 to 1"),
            ' <span class="op">=</span> <span class="paren">(</span>1 <span class="op">−</span> <span class="frac"><span>1</span><span><var>m</var></span></span><span class="paren">)</span><sup><var>m</var></sup> <span class="op">→</span> ',
            ('<span class="frac"><span>1</span><span><var>e</var></span></span>', "exponential-f0", "the limit, as m grows"),
            ' <span class="op">≈</span> 0.368',
        ], "as m grows, about 37% of examples are left out of each bag — hover or click a part")
        + decode([
            ("with replacement", "“put it back”", "The example can be drawn again. Without replacement you would just get a shuffle of the same set — useless here."),
            ("bootstrap sample", "“one new bag”", "A sample of size m drawn with replacement from a dataset of size m. Always the same size as the original."),
            ("~63%", "“distinct examples per bag”", "1 − 1/e ≈ 0.632. Each bag contains about 63% of the distinct originals, with the rest duplicated."),
            ("out-of-bag", "“the ~37% left out”", "A free validation set for that tree — you can score it on the examples it never saw, with no separate split."),
            ("bagging", "“bootstrap aggregating”", "Bootstrap sample + aggregate the predictions. That is the whole method."),
        ])
        + key("""<p>Sampling <b>with</b> replacement is what makes each bag genuinely different. Without
replacement you would draw all m examples every time and get the identical dataset back, in a different
order — and identical trees.</p>""")

        + h2("💻", "In code")
        + code("""
import numpy as np

def bootstrap(X, y):
    m = len(y)
    idx = np.random.choice(m, size=m, replace=True)    # <- replace=True is the whole trick
    return X[idx], y[idx]

trees = []
for b in range(100):
    Xb, yb = bootstrap(X, y)
    trees.append(train_tree(Xb, yb))
""")

        + h2("🧮", "How much of the data does each tree actually see?")
        + """<p>Draw 10 examples with replacement from a set of 10. One such draw:</p>"""
        + code("""
[8, 0, 1, 2, 1, 8, 8, 5, 0, 0]        # 10 draws
unique -> 5 of the 10 original examples
# example 8 appears 3 times, example 0 appears 3 times, and 3, 4, 6, 7, 9 never appear
""")
        + """<p>Half the data set is missing from that tree, and two examples are triple-weighted.
That is not a flaw — it is the mechanism. Every tree gets a different distortion of the data, so
every tree is a different model, and different models are what makes averaging worth anything.</p>
<p>How much is missing on average? The chance a particular example survives one draw is
(1 − 1/<var>m</var>), and there are <var>m</var> draws:</p>"""
        + table(["m", "P(a given example is never drawn) = (1 − 1/m)<sup>m</sup>"],
                [["10", "0.3487"],
                 ["100", "0.3660"],
                 ["1,000", "0.3677"],
                 ["10,000", "0.3679"],
                 ["→ ∞", "<b>1/e = 0.3679</b>"]])
        + """<p>So for any reasonably sized data set, each bagged tree trains on about <b>63.2%</b>
of the unique examples and never sees the other 36.8%. Those left-out examples have a name —
<em>out-of-bag</em> — and because each is unseen by roughly a third of the trees, they provide a
free validation estimate with no separate holdout set at all.</p>"""
        + explain("""<p>The fraction left out converges to 1/e — the same constant as in compound
interest and in <var>e</var><sup><var>x</var></sup>. <b>Why does it appear here?</b></p>""",
                  """<p>Because (1 − 1/<var>m</var>)<sup><var>m</var></sup> <em>is</em> the definition
of 1/<var>e</var> in the limit — the same expression that defines <var>e</var> as
(1 + 1/<var>m</var>)<sup><var>m</var></sup>, with the sign flipped. Each of the <var>m</var> draws
independently spares an example with probability (1 − 1/<var>m</var>), and multiplying <var>m</var>
of those together is exactly that limit. It is not a coincidence about trees; it is what happens
whenever you take <var>m</var> independent chances each of size 1/<var>m</var>.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b><code>replace=False</code>.</b> You get a permutation of the original data, every
tree is identical, and the ensemble does nothing.</p>""")
        + trap("""<p><b>Sampling fewer than m.</b> Allowed (“subagging”), and it changes the bias/variance
balance. The standard method draws exactly m.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("You bootstrap from 1000 examples. Roughly how many distinct examples are in one bag?",
             "<p>About <b>632</b> — 63.2%. The other ~368 are duplicates of those already drawn.</p>"),
            ("What are out-of-bag examples good for?",
             "<p>Free validation. Each tree can be scored on the examples it never saw, giving an "
             "out-of-bag error estimate with no held-out set at all.</p>"),
            ("Why must the bag be the same size as the original?",
             "<p>So each tree sees a comparable amount of data. Smaller bags mean weaker trees; the "
             "standard bootstrap keeps size m and gets its variety purely from the duplication.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("paper", "https://projecteuclid.org/journals/annals-of-statistics/volume-7/issue-1/Bootstrap-Methods-Another-Look-at-the-Jackknife/10.1214/aos/1176344552.full",
             "Efron (1979) — Bootstrap Methods: Another Look at the Jackknife",
             "The original bootstrap paper. A statistical idea that predates its use in ML by seventeen years."),
            ("docs", "https://scikit-learn.org/stable/modules/ensemble.html#bagging",
             "scikit-learn — Bagging meta-estimator",
             "<code>BaggingClassifier</code> wraps <em>any</em> model, not just trees."),
        ])
    )))

# ============================================================ 11
L.append(dict(
    slug="11-random-forest", title="Random forest algorithm", mins=13, tag="core",
    lede="Bagging, plus one extra sprinkle of randomness that stops all the trees from making the same "
         "first move.",
    body=(
        pretest("""<p>Bagging gives many trees from one dataset — but they still all pick the same obvious first split. <b>Guess the extra randomisation that fixes it.</b></p>""",
        """<p>Watch for restricting which features each split may even consider.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>You built a hundred trees from a hundred different bags. Problem: if one feature is
clearly the best, <b>every</b> tree picks it as its first question anyway. The trees end up looking
suspiciously similar, and a hundred near-identical judges is barely better than one.</p>
<p>So add a rule: at every question, each tree may only choose from a <b>random handful</b> of the
features. Sometimes the star feature isn’t even on the menu, and the tree is forced to find a different
route.</p>
<p>Forcing disagreement makes the vote worth taking.</p>""")

        + lenses(
            """<p>A panel tasting wine. Sit them round one table and the loudest taster anchors the room —
you get one opinion in four voices.</p>
<p>So you seat them apart. And then the real trick: you give each of them only <b>part</b> of the
information. One gets the nose and the colour, another the finish and the acidity. Now their mistakes
genuinely differ, and the average is better than any single palate.</p>""",
            """<p>If you know that averaging <var>n</var> independent estimates shrinks the standard error by
1/√<var>n</var>, you already know why bagging helps — and you know precisely why it stops
helping.</p>
<p>That formula assumes independence. Real bagged trees are heavily correlated, so the variance
reduction stalls well short of what the formula promises. Feature subsampling is a direct, deliberate
attack on the correlation term that bagging alone leaves untouched.</p>""",
            """<p>At every split, in every tree, a hand covering most of the feature columns and leaving only a
random handful visible. The tree must choose its split from what it can see.</p>
<p>The essential detail: that hand moves <b>at every node</b>, not once per tree. A fresh random
handful at every single split. That, and nothing else, is the difference between a random forest and
plain bagging.</p>""",
            """<p>Without it, one dominant feature — “has previously defaulted”, say — is chosen as the
root split by all 500 trees, and 500 nearly identical trees average to approximately one tree.</p>
<p>Practitioners meet this constantly: bagging alone gives a disappointing bump, and feature
subsampling unlocks the rest. √<var>p</var> features per split is the usual classification
default, and it is a default worth understanding rather than inheriting.</p>""",
            """So the algorithm below is two lines — bootstrap the rows, subsample the columns at every node
— and both lines exist for one purpose: to manufacture disagreement.""")

        + h2("🎬", "Watch it move")
        + demo("forest", "B trees, each voting",
               "drag the number of trees and watch the vote stabilise")

        + h2("🔢", "The algorithm, in full")
        + """<ol>
<li>For b = 1 to B:
  <ul><li>Draw a bootstrap sample of size m (Lesson 10).</li>
  <li>Train a decision tree on it — but at <b>every node</b>, choose the split from a random subset of
  k features rather than all n.</li></ul></li>
<li>To predict: <b>majority vote</b> (classification) or <b>average</b> (regression) over all B trees.</li>
</ol>"""
        + decode([
            ("B", "“the number of trees”", "64, 100, 128 are typical. More never hurts accuracy — only compute. Past ~100 the gains flatten."),
            ("k", "“features per split”", "Usually k = √n for classification, n/3 for regression. This is the one genuinely new hyperparameter."),
            ("feature bagging", "“the extra randomness”", "The difference between bagged trees and a random forest. Bagging randomises the rows; the forest also randomises the columns."),
            ("out-of-bag score", "“free validation”", "<code>oob_score=True</code> gives you a validation estimate without holding anything out."),
        ])
        + key("""<p>Random forests are <b>hard to break</b>. They need almost no tuning, do not need feature
scaling, handle mixed data types, tolerate missing values reasonably, and rarely overfit badly. That is why
they are the standard first thing to try on a table of data.</p>""")

        + h2("💻", "In code")
        + code("""
from sklearn.ensemble import RandomForestClassifier

clf = RandomForestClassifier(
    n_estimators=100,      # B — number of trees
    max_features='sqrt',   # k — features considered per split
    oob_score=True,        # free validation from the left-out examples
    random_state=1,
)
clf.fit(X_train, y_train)
print('out-of-bag accuracy:', clf.oob_score_)
print('feature importances:', clf.feature_importances_)
""")
        + note("""<p><code>feature_importances_</code> is a genuinely useful by-product: how much each
feature reduced impurity across the whole forest. Treat it as a hint rather than a truth — it is biased
towards high-cardinality features. <b>Permutation importance</b> is the more trustworthy version.</p>""",
               "A useful side effect")

        + h2("🧮", "How many features does each node get to see?")
        + """<p>Random forest adds one restriction to bagging: at every node, choose from a random
subset of <var>k</var> features rather than all <var>n</var>. The usual choice is
<var>k</var> = √<var>n</var>:</p>"""
        + table(["features n", "k = √n", "fraction of features visible at a node"],
                [["3", "1", "33%"],
                 ["9", "3", "33%"],
                 ["16", "4", "25%"],
                 ["100", "10", "10%"],
                 ["400", "20", "5%"]])
        + """<p>With 100 features, each node sees ten. Nine times out of ten, the single strongest
feature is <b>not available</b> — and that is deliberate.</p>
<p>Recall from two lessons ago that ear shape wins the root by 0.278 against 0.125 and 0.035. Bagging
alone resamples the rows, but ear shape is strong enough that it would still win the root in most
resamples, so the trees would come out looking alike — and averaging near-identical models buys
nothing. Forcing each node to ignore most features means some trees are <em>compelled</em> to build
around whiskers instead, and discover whatever whiskers can contribute. Diversity is not a side
effect here; it is the thing being manufactured.</p>"""
        + explain("""<p>Hiding the best feature from most nodes makes every individual tree
<em>worse</em>. <b>Why does the forest get better?</b></p>""",
                  """<p>Because averaging only cancels errors that differ. If every tree makes the
same mistake, the average makes it too, no matter how many trees you add — so the quantity that
matters is not each tree’s accuracy but how <em>uncorrelated</em> their errors are. Trading a little
individual accuracy for a lot of decorrelation is a good trade, and the arithmetic in the next
lesson shows why: the spread of an average falls with the number of <em>independent</em> members,
and near-duplicates do not count as members.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Setting <code>max_features</code> to all features.</b> Then it is plain bagging, the
trees correlate, and you lose most of the benefit.</p>""")
        + trap("""<p><b>Too few trees.</b> With B = 5 the vote is noisy. Use at least 50; 100 is a fine
default and the cost is linear.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("You have 16 features. What is a typical k for classification?",
             "<p>√16 = <b>4</b> features considered at each split.</p>"),
            ("Why sample features as well as rows?",
             "<p>Because bootstrap sampling alone leaves the trees highly correlated — a dominant feature "
             "wins the root in nearly every bag. Feature sampling forces genuine diversity.</p>"),
            ("Does raising B from 100 to 1000 risk overfitting?",
             "<p>Essentially no. More trees reduce variance and converge; they do not add capacity. You "
             "pay in compute, not in generalisation.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("paper", "https://link.springer.com/article/10.1023/A:1010933404324",
             "Breiman (2001) — Random Forests",
             "The paper. Includes the out-of-bag idea and the proof that the error converges as B grows."),
            ("docs", "https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html",
             "sklearn.ensemble.RandomForestClassifier",
             "Every argument, with sensible defaults already set."),
            ("docs", "https://scikit-learn.org/stable/modules/permutation_importance.html",
             "scikit-learn — permutation importance",
             "The more trustworthy way to ask which features matter."),
            ("lab", "../../C2%20-%20Advanced%20Learning%20Algorithms/week4/optional%20labs/C2_W4_Lab_02_Tree_Ensemble.ipynb",
             "Optional lab: Tree Ensembles",
             "In this repo. Random forest and XGBoost on the heart-disease dataset."),
        ])
    )))

# ============================================================ 12
L.append(dict(
    slug="12-xgboost", title="XGBoost", mins=15, tag="core",
    lede="Instead of making every tree from a random sample, make each new tree focus on what the previous "
         "ones got wrong. This is the algorithm that wins competitions.",
    body=(
        pretest("""<p>Random forest builds trees independently. <b>Guess what you could do instead if each new tree were allowed to see where the previous ones went wrong.</b></p>""",
        """<p>Watch for boosting, and for why it dominates competitions on tabular data.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Random forest is a hundred students each revising from a random chunk of the textbook.</p>
<p>Boosting is <b>one</b> student who takes a practice test, marks it, and then revises <b>only the
questions they got wrong</b>. Then tests again. Then revises the ones still wrong.</p>
<p>It’s a much more efficient use of effort — and it is why boosted trees usually beat random forests on
the same data.</p>""")

        + lenses(
            """<p>A tailor fitting a suit. The first cut is rough and close. He puts it on you, chalks the places
where it pulls at the shoulder, and the second pass works <b>only on the chalk marks</b>.</p>
<p>Then a third pass, on whatever is still wrong. Nobody re-cuts the whole suit each time. Each pass
is small, and aimed squarely at the error the previous passes left behind.</p>""",
            """<p>If you have used Newton's method, successive approximation, or a PID controller, this is that:
each step works on the residual left by the steps before it.</p>
<p>The contrast with a forest is worth stating precisely. A forest builds its trees <b>in parallel</b>
and averages them — the trees never learn of each other's existence. Boosting builds
<b>in sequence</b>, and every tree exists only because of what the previous ones got wrong.</p>""",
            """<p>A column of <b>residuals</b>, shrinking.</p>
<p>Fit tree 1 to the labels. Subtract its predictions and you are left with a column of what remains.
Fit tree 2 to <em>that column</em>. Subtract again. The final prediction is the running sum of every
tree. Picture the column of leftovers getting smaller down the page.</p>""",
            """<p>XGBoost and its descendants — LightGBM, CatBoost — are the default model for tabular
data across pricing, risk, ranking and ad click-through, and they beat neural networks on structured
data more often than not.</p>
<p>They are also markedly easier to overfit than a forest, because sequential fitting will
enthusiastically keep chasing noise once the signal is gone. The learning rate exists to slow it
down on purpose, which is why boosting has more knobs and demands more care than a forest.</p>""",
            """So “boosting” names the mechanism exactly: each tree boosts the examples the previous one got
wrong.""")

        + h2("🎬", "Watch it move")
        + demo("boosting", "Four rounds, each focusing on the remaining mistakes",
               "the misclassified animals grow — that is their weight increasing")

        + h2("🔢", "The idea, decoded")
        + """<p>The version Andrew describes: like bagging, but when drawing the sample for tree b, make
examples that the previous b−1 trees got <b>wrong</b> more likely to be picked. Each new tree therefore
specialises in the hard cases.</p>"""
        + decode([
            ("boosting", "“focus on the hard ones”", "Trees are built <b>sequentially</b>, each one correcting the ensemble so far."),
            ("deliberate sampling", "“the opposite of random”", "Random forest samples uniformly. Boosting samples the current mistakes preferentially."),
            ("gradient boosting", "“the real formulation”", "Each tree is fitted to the <em>residual errors</em> — the gradient of the loss — rather than to a re-weighted sample. Same intuition, cleaner maths."),
            ("XGBoost", "“eXtreme Gradient Boosting”", "A specific, very fast implementation with built-in regularisation, clever split-finding, missing-value handling and parallelism."),
        ])
        + warn("""<p>The one real downside: because trees are built <b>in sequence</b>, boosting cannot
parallelise across trees the way a random forest can. XGBoost gets its speed from parallelising <em>inside</em>
each tree instead.</p>""")

        + h2("💻", "In code — it really is this short")
        + code("""
from xgboost import XGBClassifier

model = XGBClassifier(
    n_estimators=100,        # number of boosting rounds
    learning_rate=0.1,       # how much each tree is allowed to contribute
    max_depth=4,             # boosted trees are SHALLOW on purpose
    early_stopping_rounds=10,
)
model.fit(X_train, y_train, eval_set=[(X_cv, y_cv)])
y_pred = model.predict(X_test)

# regression is the same object with a different name:
# from xgboost import XGBRegressor
""")
        + """<p><code>max_depth=4</code> is not a typo. Boosting deliberately uses <b>weak</b> trees — often
depth 3 to 6 — because the ensemble supplies the power and shallow trees keep each correction small and
safe. A boosted forest of depth-20 trees usually overfits badly.</p>"""

        + h2("⚖️", "Random forest vs boosting")
        + table(["", "Random forest", "Boosting / XGBoost"],
                [["Trees built", "independently, in parallel", "sequentially, each fixing the last"],
                 ["Sampling", "uniformly random", "focused on current errors"],
                 ["Tree depth", "deep, fully grown", "<b>shallow</b> (3–6)"],
                 ["Overfits?", "rarely", "<b>yes, if you let it</b> — needs early stopping"],
                 ["Tuning needed", "almost none", "some — learning rate matters"],
                 ["Typical accuracy", "very good", "<b>usually better</b>"]])
        + key("""<p>On a table of numbers and categories, gradient-boosted trees are still the thing to
beat. They win the large majority of tabular competitions on Kaggle, and neural networks have repeatedly
failed to displace them on structured data.</p>""")

        + h2("🧮", "Why averaging works at all — measured")
        + """<p>Before boosting, the arithmetic that makes any ensemble worth building. Take
<var>B</var> predictors whose errors are independent with a spread of 1.0, average them, and measure
the spread of that average over 20,000 trials:</p>"""
        + table(["B (predictors averaged)", "spread of the average", "1/√B"],
                [["1", "1.0073", "1.0000"],
                 ["5", "0.4443", "0.4472"],
                 ["25", "0.2000", "0.2000"],
                 ["100", "0.1007", "0.1000"]])
        + """<p>The measurement tracks 1/√<var>B</var> exactly. Averaging 100 noisy models gives you
a model ten times steadier than any one of them — from models that are individually no better.</p>
<p>Two consequences follow directly from that square root. First, it is why <b>B ≈ 100</b> is the
usual advice: going from 1 to 25 cuts the spread by 5×, while going from 100 to 400 buys only
another 2× for four times the compute. Second, it is why the previous lesson works so hard on
decorrelation — the <var>B</var> in that formula counts <em>independent</em> members, so a hundred
near-identical trees behave like far fewer.</p>
<p>Boosting then changes what the members are. Instead of resampling uniformly, each new tree is
trained with more weight on the examples the previous trees got wrong — deliberate practice on the
weak spots rather than more repetitions of the whole exam.</p>"""
        + explain("""<p>Bagging’s trees can all be built at the same time; boosting’s cannot.
<b>Why does the difference in <em>how</em> they choose examples force that?</b></p>""",
                  """<p>Because boosting’s next tree is defined by the current ensemble’s mistakes,
which do not exist until the previous trees are trained. Each round’s weights depend on the last
round’s errors, so the sequence is inherently serial. Bagging draws every bootstrap sample straight
from the original data, independently of any tree, so all <var>B</var> trees can train in parallel.
That is a real practical trade: random forests parallelise almost perfectly, and boosting buys its
usually-higher accuracy with a serial dependency.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>No early stopping.</b> Unlike a random forest, more boosting rounds <em>can</em>
overfit. <code>early_stopping_rounds</code> with a validation set is not optional.</p>""")
        + trap("""<p><b>Learning rate and n_estimators tuned separately.</b> They trade off directly: halve
the learning rate, roughly double the trees. Tune them together, or fix the rate at 0.05–0.1 and let early
stopping choose the count.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("Why are boosted trees kept shallow?",
             "<p>Each tree only needs to make a small correction. Deep trees would overfit their "
             "residuals, and the sequential process would amplify that.</p>"),
            ("Can boosting be parallelised across trees like a random forest?",
             "<p>No — tree b needs the errors of trees 1…b−1. XGBoost parallelises the split-finding "
             "<em>within</em> each tree instead.</p>"),
            ("Random forest with 1000 trees does not overfit. Boosting with 1000 rounds might. Why?",
             "<p>Forest trees are independent, so averaging only reduces variance. Boosting rounds are "
             "cumulative — each adds capacity aimed at the remaining errors, including noise.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("paper", "https://arxiv.org/abs/1603.02754",
             "Chen & Guestrin (2016) — XGBoost: A Scalable Tree Boosting System",
             "The paper. Sections 2–3 explain the regularised objective and the split-finding algorithm."),
            ("paper", "https://projecteuclid.org/journals/annals-of-statistics/volume-29/issue-5/Greedy-function-approximation-A-gradient-boosting-machine/10.1214/aos/1013203451.full",
             "Friedman (2001) — Greedy Function Approximation: A Gradient Boosting Machine",
             "Where gradient boosting comes from. Dense, and the source of the whole family."),
            ("docs", "https://xgboost.readthedocs.io/en/stable/tutorials/model.html",
             "XGBoost — “Introduction to Boosted Trees”",
             "The official tutorial. Genuinely one of the better pieces of ML documentation."),
            ("paper", "https://arxiv.org/abs/2207.08815",
             "Grinsztajn et al. (2022) — Why do tree-based models still outperform deep learning on tabular data?",
             "A careful benchmark. The answer to “should I use a neural network on my spreadsheet?”"),
        ])
    )))

# ============================================================ 13
L.append(dict(
    slug="13-trees-vs-neural-networks", title="When to use decision trees", mins=9, tag="core",
    lede="The practical decision rule, and the end of Course 2. Spreadsheet? Try trees first. Pixels, "
         "sound or words? Neural network.",
    body=(
        pretest("""<p>Both work. <b>Guess which you would choose for a spreadsheet of house prices, and which for photographs</b> — and what the deciding factor is.</p>""",
        """<p>Watch for the data-type rule, and for the one property neural networks have that trees do not: they compose.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>A hammer and a screwdriver are both good tools. You just need to know which is holding
your thing together.</p>
<p><b>Neat rows and columns</b> — ages, prices, categories, counts — that’s tree country. Fast, accurate,
and you can read the answer.</p>
<p><b>Pictures, sound, or words</b> — that’s neural network country, and it isn’t close.</p>""")

        + lenses(
            """<p>Choosing between a socket set and a lathe.</p>
<p>The socket set is fast, everyone in the shop can already use it, and it handles nine jobs in ten on
the vehicles that actually come through the door. The lathe can make a part that does not exist yet,
takes far longer to set up, and rewards a skilled operator. Neither is the better tool. The only
question is what is on the bench.</p>""",
            """<p>If you have ever chosen between a decision rule and a fitted model — an actuarial table
versus a survival model, a triage scoring sheet versus a clinician's judgement — you have made
this trade before.</p>
<p>It is the same axis every time: transparency and speed on one side, flexibility and the ability to
absorb inputs that do not fit in columns on the other.</p>""",
            """<p>Two things on a page, side by side. On the left, a spreadsheet — rows, named columns, mixed
types, missing values, one column called <code>customer_age</code>.</p>
<p>On the right, a photograph, a waveform, a sentence. The left is where trees win. The right is where
networks win. Almost the whole decision is working out which of those two objects you are actually
holding.</p>""",
            """<p>This choice costs real money. Neural networks on tabular data routinely lose to gradient
boosting while costing far more to train, tune and serve — and on images, a transfer-learned
network is the only sane option there has ever been.</p>
<p>Teams that choose by fashion rather than by the shape of their data pay for it twice: once in GPU
bills, and again in the weeks spent tuning something that was never going to win.</p>""",
            """So the comparison table below is not a list of opinions. It is a list of what each of those two
objects makes cheap.""")

        + h2("🎬", "Watch it move")
        + demo("treevsnn", "The comparison, line by line",
               "each row highlights which side wins and why")

        + h2("🔢", "The scorecard")
        + grid2(
            card("<h3>🌳 Decision trees & ensembles</h3><ul>"
                 "<li>Excellent on <b>tabular / structured</b> data.</li>"
                 "<li><b>Fast</b> to train — often seconds to minutes.</li>"
                 "<li>Handle categorical features natively; <b>no scaling needed</b>.</li>"
                 "<li>A small tree is <b>human-readable</b>.</li>"
                 "<li>✗ Not for images, audio or text.</li>"
                 "<li>✗ No transfer learning; cannot be chained into a bigger differentiable system.</li></ul>"),
            card("<h3>🧠 Neural networks</h3><ul>"
                 "<li>Work on <b>everything</b> — tabular, images, audio, text, video.</li>"
                 "<li><b>Transfer learning</b>: start from someone else’s pre-trained model.</li>"
                 "<li>Multiple networks can be <b>chained and trained together</b> end to end.</li>"
                 "<li>✗ Slower to train.</li>"
                 "<li>✗ Need scaling, tuning, and more care.</li>"
                 "<li>✗ Much harder to interpret.</li></ul>"))
        + key("""<p>The decisive advantage of neural networks is <b>composability</b>: because everything is
differentiable, you can bolt several networks together and train the whole stack with one gradient. You
cannot do that with trees — and that single property is why deep learning scaled.</p>""")

        + h2("🎓", "You have finished Course 2")
        + """<p>Look back at what you can now do:</p>
<ul>
<li><b>Week 1</b> — build a neural network and run it forwards, in TensorFlow, in NumPy loops, and
vectorised with matrix multiplication.</li>
<li><b>Week 2</b> — train one: cross-entropy loss, ReLU, softmax, numerically stable implementations,
Adam, and what backpropagation actually computes.</li>
<li><b>Week 3</b> — diagnose one: train/cv/test, bias vs variance, learning curves, error analysis,
precision and recall.</li>
<li><b>Week 4</b> — a completely different model family: trees, entropy, information gain, random forests
and XGBoost.</li>
</ul>
<p>Course 3 goes to unsupervised learning (clustering, anomaly detection), recommender systems, and
reinforcement learning. The habits from Week 3 carry into all of it.</p>"""

        + h2("🔤", "The words, decoded")
        + decode([
            ("structured data", "“tabular data”", "Rows and columns, like a spreadsheet. Trees are excellent here."),
            ("unstructured data", "“images, audio, text”", "No natural columns. Neural networks, essentially always."),
            ("interpretability", "“can you explain it”", "Whether a human can follow why the model decided what it did. A small tree is readable; a network is not."),
            ("end-to-end", "“end to end”", "Training several stacked models together as one. Networks allow it; trees do not."),
        ])
        + h2("🕳", "Traps")
        + trap("""<p><b>Reaching for a neural network on a 5,000-row spreadsheet.</b> XGBoost will very
likely beat it, train in seconds and need no tuning. Try the cheap thing first.</p>""")
        + trap("""<p><b>Reaching for a tree on raw pixels.</b> A tree has no notion of “nearby pixels”, so
it must learn every position independently. It will not work.</p>""")

        + explain("""<p>A tree on raw pixels &ldquo;will not work&rdquo;. <b>Say what a tree lacks that a convolutional
network has.</b></p>""",
                  """<p>Any notion that pixel 4,001 is <em>next to</em> pixel 4,002. To a tree the input is an unordered
list of numbers, so a cat one pixel to the left is an entirely unrelated set of thresholds and must be
learned from scratch.</p>
<p>A convolution builds locality and translation invariance in as a structural assumption — the same
filter slides everywhere. That prior is true of images and false of spreadsheets, which is precisely
why the two model families swap places depending on the data.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("A 50,000-row spreadsheet of customer data, predicting churn. What first?",
             "<p><b>XGBoost.</b> Tabular, moderate size, mixed types, and you get feature importances for "
             "free. Try a network afterwards if you want, but expect it to lose.</p>"),
            ("Classifying skin lesions from photographs. What first?",
             "<p><b>A pre-trained convolutional neural network</b>, fine-tuned (Week 3, Lesson 13). "
             "Trees cannot use pixel structure.</p>"),
            ("Why can several neural networks be trained together but not several trees?",
             "<p>Because networks are differentiable end to end — one gradient flows through the whole "
             "stack. Tree splits are discrete decisions with no useful derivative.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("paper", "https://arxiv.org/abs/2207.08815",
             "Grinsztajn et al. (2022) — Why do tree-based models still outperform deep learning on tabular data?",
             "A careful, honest benchmark. The best available answer to this lesson’s question."),
            ("paper", "https://arxiv.org/abs/2106.11959",
             "Gorishniy et al. (2021) — Revisiting Deep Learning Models for Tabular Data",
             "The other side of the argument, with strong neural baselines. Read both."),
            ("lab", "../../C2%20-%20Advanced%20Learning%20Algorithms/week4/optional%20labs/C2_W4_Lab_02_Tree_Ensemble.ipynb",
             "Optional lab: Tree Ensembles",
             "In this repo. Compare a single tree, a random forest and XGBoost on the same data."),
            ("docs", "https://www.coursera.org/learn/unsupervised-learning-recommenders-reinforcement-learning",
             "Course 3 — Unsupervised Learning, Recommenders, Reinforcement Learning",
             "Where to go next. The C3 folder in this repository has the labs waiting."),
        ])
    )))

WEEK = dict(
    course="C2", week=4, title="Decision Trees",
    time="~5–7 h with labs",
    goal="Build decision trees from entropy and information gain, extend them to categorical, continuous "
         "and regression targets, and combine them into random forests and XGBoost.",
    lessons=L,
)
