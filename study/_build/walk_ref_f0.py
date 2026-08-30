# -*- coding: utf-8 -*-
"""The slow read for the Foundations W1 reference entries.

Keyed on card id. These are NOT shown on the flashcards — a card you scroll is
a card you have stopped testing yourself with — only on reference.html, where
the job is to understand rather than to recall.

The card's own `plain` block is a gist: one analogy, a decode table, one line of
code, about thirty words. This is the other half: what it looks like with a
number in it, and why the idea is shaped the way it is.

Every number below was computed before it was written, never recalled.
"""
from walkkit import p, expr, chain, chainset, steps, cases, values, point, ascii_art

W = {

"f0-function": """
<p>Think of <b>f</b> as the name of a machine, the way <i>kettle</i> is the name of a
machine. <code>f(3)</code> means <b>put 3 into the machine called f</b> and see what falls
out. The brackets are a doorway, not a multiplication sign.</p>
<p>Say the machine is <b>f(x) = 3x − 4</b>. Then:</p>
<ul>
<li>put in <b>0</b> → 3×0 − 4 = <b>−4</b></li>
<li>put in <b>2</b> → 3×2 − 4 = <b>2</b></li>
<li>put in <b>−1</b> → 3×(−1) − 4 = <b>−7</b></li>
</ul>
<p>The one rule that makes it a function: <b>the same thing in always gives the same thing
out</b>. Put 2 in a hundred times and you get 2 back a hundred times.</p>
<p>Why this matters later: a trained model <i>is</i> one of these machines. Training never
changes the machine — it changes the numbers sitting inside it. That is what the little
<b>w, b</b> underneath in <b>f<sub>w,b</sub>(x)</b> is telling you: same machine, adjustable
parts.</p>
""",

"f0-superscripts": """
<p>Three little raised numbers that look almost identical and mean completely different
things. The <b>brackets around them are the only clue</b>, so read the brackets first.</p>
<ul>
<li><b>x<sup>(2)</sup></b>, round brackets → <b>the second example</b>. The second house,
the second student. Nothing is being multiplied.</li>
<li><b>x<sup>2</sup></b>, no brackets → <b>x times x</b>. An ordinary power.</li>
<li><b>a<sup>[2]</sup></b>, square brackets → <b>layer 2</b> of a neural network. This one
only turns up in Course 2.</li>
</ul>
<p>So <b>x<sub>3</sub><sup>(2)</sup></b> — which looks terrifying — is just: <b>the second
house, its third feature</b>. Superscript picks the row, subscript picks the column. It is
a spreadsheet address wearing formal clothes.</p>
<p>This specialization is consistent about it, so once you trust the brackets you can stop
worrying. The confusion is real but it is only ever notation, never maths.</p>
""",

"f0-slope": (
    p("""Slope is one number answering one question: <b>if I step one to the right, how far
up do I go?</b>""")
    + steps(["Pick two points on the line. Say <b>(2, 3)</b> and <b>(6, 11)</b>.",
             "How far <b>up</b>? 11 &minus; 3 = <b>8</b>. That is the <i>rise</i>.",
             "How far <b>across</b>? 6 &minus; 2 = <b>4</b>. That is the <i>run</i>.",
             "Divide: 8 &divide; 4 = <b>2</b>. That is the slope."],
            "worked all the way through")
    + point("""This line climbs <b>2 units up for every 1 across</b>. A slope of 0 is
flat. A negative slope goes downhill.""")
    + p("""The letters trip people up more than the idea does. At school it was probably
<b>m</b>. Here it is <b>w</b>, for weight &mdash; same number, different name, because
<b>w</b> is about to become a whole list of them.""")
    + p("""Everything in gradient descent is this one idea, asked about a hill instead of
a line.""")
),

"f0-derivative": (
    p("""A slope needs two points. A curve at a single spot only gives you one. So: take a
second point <b>very close by</b>, work out the slope between them, then slide the second
point closer and closer. The number it settles on is the <b>derivative</b>.""")
    + p("""Try it on <b>f(x) = x&sup2;</b> at <b>x = 3</b>, with the second point a
thousandth away.""")
    + values([("up a hair", "(3.001)&sup2; = 9.006001", "just to the right"),
              ("down a hair", "(2.999)&sup2; = 8.994001", "just to the left"),
              ("rise &divide; run", "0.012 &divide; 0.002 = 6.0", "the slope between them")],
             "measured, with a ruler")
    + p("""And the calculus rule says the derivative of x&sup2; is 2x, which at x = 3 is
<b>6</b>. The measurement and the rule agree.""")
    + point("""That agreement is not a coincidence and it is not just pretty &mdash; it is
exactly the check the from-scratch files run on every gradient they write. Calculus you did
by hand, against arithmetic that needs no calculus. If they match, the calculus was
right.""")
    + cases([("Its sign", "says which way is <b>uphill</b>."),
             ("Its size", "says <b>how steep</b> the hill is.")],
            "only three things about a derivative matter here: it is a slope, and then")
),

"f0-partial": """
<p>You are standing on a hillside. Someone asks “how steep is it?” — and the question is
incomplete, because it depends which way you face.</p>
<p>A <b>partial derivative</b> answers the fixed-up version: <b>pick one direction, hold
everything else still, and measure the steepness along that line only.</b></p>
<p>Take <b>f(x, y) = x²y</b> at the point <b>x = 2, y = 3</b>.</p>
<ul>
<li>Steepness in the <b>x</b> direction: pretend y is a frozen 3, differentiate x²·3 → 6x
→ at x = 2 that is <b>12</b>.</li>
<li>Steepness in the <b>y</b> direction: pretend x is a frozen 2, differentiate 4y → 4 →
that is <b>4</b>.</li>
</ul>
<p>Two numbers, one per direction. The curly <b>∂</b> — say it “partial dee” — is the only
thing announcing “there are other variables and I am holding them still”.</p>
<p>This is why gradient descent has one slope per weight. A model with a million weights is
standing on a hillside with a million directions, asking the same small question a million
times.</p>
""",

"f0-sigma": """
<p><b>Σ</b> is a capital Greek S and it stands for <b>Sum</b>. It is a <code>for</code>
loop that someone wrote down instead of typing.</p>
<p>Read it in three parts, bottom, top, right:</p>
<ul>
<li><b>bottom</b> — where the counter starts (<i>i</i> = 1)</li>
<li><b>top</b> — where it stops (<i>m</i>, and it <b>includes</b> m)</li>
<li><b>right</b> — the thing to work out each time round, then add on</li>
</ul>
<p>So with the list <b>[3, 1, 4]</b>: start at the first, take 3; next, add 1 to get 4;
next, add 4 to get <b>8</b>. Done.</p>
<p>In code that whole symbol is usually a single call: <code>np.sum(x)</code>, or
<code>x.sum()</code>. Cost functions look frightening mostly because they are a Σ wrapped
around something else — and the Σ is never the hard part. Cover it with your thumb, read
what is to the right of it, then remember it happens once per example and gets added
up.</p>
""",

"f0-pi": """
<p><b>Π</b> is a capital Greek P and it means <b>Product</b> — the same idea as Σ but with
multiplying instead of adding.</p>
<p>Now the practical problem. Multiply probabilities together and they collapse:
0.5 × 0.5 × 0.5 = <b>0.125</b>. Do that a thousand times and the answer is smaller than the
smallest number a computer can hold. It becomes 0, and everything after it is nonsense.
That failure has a name — <b>underflow</b>.</p>
<p>The escape is a logarithm, which turns multiplying into adding:</p>
<ul>
<li>log(0.125) = <b>−2.0794</b></li>
<li>log(0.5) + log(0.5) + log(0.5) = 3 × (−0.6931) = <b>−2.0794</b></li>
</ul>
<p>Same number, and the second route never made a tiny number along the way.</p>
<p>So Π appears in the maths and almost never in the code. Anywhere you would have
multiplied a long list of probabilities, real code adds their logs instead. That single
swap is why log-likelihood and log loss exist at all.</p>
""",

"f0-vector-length": """
<p>A <b>vector</b> is a list of numbers with an order: <code>[3, 4]</code>. You can picture
it as an arrow from the origin out to the point (3, 4).</p>
<p>Its <b>length</b> is measured with Pythagoras, which is the same rule you would use for
a ladder against a wall:</p>
<ul>
<li>square each number: 3² = 9, 4² = 16</li>
<li>add them: 9 + 16 = <b>25</b></li>
<li>square root: √25 = <b>5</b></li>
</ul>
<p>It works the same in any number of dimensions — just keep adding squares.
<code>[1, 2, 2]</code>: 1 + 4 + 4 = 9, so the length is <b>3</b>. You cannot picture
seven dimensions and you can still compute the length, which is the whole reason to trust
the algebra over the picture.</p>
<p>The double bars, <b>‖v‖</b>, are said “norm of v”. In code it is
<code>np.linalg.norm(v)</code>. When a lesson says a model's weights got “big”, this is the
number it means.</p>
""",

"f0-dot": (
    p("""The dot product takes two lists and gives back <b>one number</b>: multiply them
position by position, then add up the lot.""")
    + steps(["Pair them up by position: <b>a = [1, 2, 3]</b> with <b>b = [4, 5, 6]</b>.",
             "Multiply each pair: 1&times;4 = <b>4</b>, 2&times;5 = <b>10</b>, "
             "3&times;6 = <b>18</b>.",
             "Add them: 4 + 10 + 18 = <b>32</b>."])
    + chain(["[1, 2, 3] &middot; [4, 5, 6]", "32"], "two lists in, one number out")
    + p("""The lists must be the same length &mdash; there is nothing to pair a leftover
with.""")
    + cases([("It is the prediction step",
              "Features in one list, weights in the other. Dot them and you have the "
              "prediction. The whole loop is one character in code: <code>a @ b</code>."),
             ("It also measures agreement",
              "Geometrically it says how much two arrows point the <b>same way</b>. Zero "
              "means at right angles. That reading is the one PCA and attention use.")],
            "two things to take away")
),

"f0-shape-rule": (
    p("""Matrix multiplication is fussy about sizes, and one trick settles it every time.
<b>Write the two shapes side by side and look at the middle pair.</b>""")
    + ascii_art("""      (4, 2)  @  (2, 3)
          |         |
          +----+----+
               |
        these must MATCH

      (4, 2)  @  (2, 3)
       |                |
       +--------+-------+
                |
        these are the ANSWER  ->  (4, 3)""",
       "Inner pair must match. Outer pair is the result.")
    + p("""Read the answer as a sentence: <b>4 examples, each with 2 features, going into a
layer of 3 units, gives 4 examples each with 3 outputs.</b> The shapes are not bookkeeping
&mdash; they are the meaning.""")
    + point("""Get the inner pair wrong and NumPy stops with a shape error. That error is a
friend: almost every neural-network bug you will hit is a shape bug, and this trick finds
it before you run anything.""")
),

"f0-transpose": """
<p><b>Transpose</b> tips a table on its side: rows become columns, columns become rows. In
code it is one character, <code>M.T</code>.</p>
<p>Start with a 2-row, 3-column table:</p>
<ul>
<li><code>[[1, 2, 3], [4, 5, 6]]</code> — shape <b>(2, 3)</b></li>
<li>transposed: <code>[[1, 4], [2, 5], [3, 6]]</code> — shape <b>(3, 2)</b></li>
</ul>
<p>The first row, 1 2 3, has become the first <i>column</i>. Nothing was calculated;
nothing moved except the way you read it.</p>
<p>Why it keeps appearing: it is almost always there to make the shape rule work. You have
data as (examples, features) and you need (features, examples) so the inner numbers line
up. When you meet <code>X.T @ err</code> in a gradient, that is all the <code>.T</code> is
doing — turning the table so the multiplication is legal, and so the sum comes out
per-feature instead of per-example.</p>
""",

"f0-exp": """
<p><b>e</b> is just a number, <b>2.71828…</b>, the way π is just 3.14159… . Nothing mystical
about it; it is the number that makes one particular thing come out clean.</p>
<p>Two facts explain why it is everywhere here.</p>
<p><b>One: e<sup>x</sup> is its own slope.</b> The steepness of the curve at any point
equals its height at that point. No other function does this, and it makes the calculus of
anything built from e<sup>x</sup> unusually tidy — which is precisely why the sigmoid and
the softmax are built from it.</p>
<p><b>Two: it is always positive.</b> e<sup>0</sup> = <b>1</b>, e<sup>1</sup> =
<b>2.71828</b>, and e of a big negative number is a tiny sliver above zero but never zero
and never negative.</p>
<p>That second fact is doing real work. Probabilities may not be negative, so anything that
must come out as a probability gets pushed through an exponential first. The sigmoid and
the softmax are both that trick, and nothing more.</p>
""",

"f0-log": """
<p>A logarithm answers: <b>what power do I raise the base to, to get this?</b> It is the
undo button for an exponential. In machine learning it does exactly two jobs.</p>
<p><b>Job one: turn multiplying into adding.</b> Multiplying many probabilities together
collapses to zero and the computer loses it. Logs rescue that — log(0.125) is
<b>−2.0794</b>, and so is log(0.5) + log(0.5) + log(0.5). Same answer, no tiny numbers
along the way.</p>
<p><b>Job two: punish confident mistakes.</b> As a probability slides towards 0 its log
plunges towards minus infinity. So a model that was 99% sure and wrong is charged a huge
cost, while one that was merely unsure is charged a little. That asymmetry is not a
side effect — it <i>is</i> the log loss, and it is the reason classification does not use
squared error.</p>
<p>Note that “log” in this field almost always means <b>natural log</b>, base e, and
<code>np.log</code> is that one. Base 10 is <code>np.log10</code>.</p>
""",

"f0-prob-rules": """
<p>Four rules, and one of them quietly powers a whole algorithm.</p>
<ul>
<li>A probability lives between <b>0 and 1</b>. Nothing outside.</li>
<li>All the possibilities together add to <b>1</b>. Something must happen.</li>
<li><b>Not A</b> = 1 − P(A).</li>
<li><b>A and B, when they do not affect each other</b> = P(A) × P(B).</li>
</ul>
<p>That last one is the load-bearing rule. Anomaly detection assumes each feature is
independent of the others, so it takes the probability of each one on its own and
<b>multiplies them all together</b>. One feature being weird drags the whole product down,
and that is exactly the alarm you want.</p>
<p>It also explains a habit you will see everywhere in the code: because multiplying many
small probabilities underflows to zero, real implementations <b>add the logs</b> instead.
Same rule, safely spelled.</p>
<p>“Independent” is an assumption, not a fact, and it is usually a bit wrong. It survives
because it is cheap and it still works.</p>
""",

"f0-variance": (
    p("""Variance and standard deviation both answer <b>how spread out are these
numbers?</b> Take <b>[2, 4, 4, 4, 5, 5, 7, 9]</b>, whose mean is <b>5</b>.""")
    + steps(["Distance from the mean, for each one: "
             "<b>&minus;3, &minus;1, &minus;1, &minus;1, 0, 0, 2, 4</b>",
             "Add those up &mdash; you get <b>exactly 0</b>. You always will. So averaging "
             "the distances is useless: the answer is 0 for every dataset that has ever "
             "existed.",
             "So <b>square</b> them first: <b>9, 1, 1, 1, 0, 0, 4, 16</b>. Nothing is "
             "negative now, so nothing cancels.",
             "Average of those: <b>4</b>. That is the <b>variance</b>.",
             "Square root of that: <b>2</b>. That is the <b>standard deviation</b>."])
    + point("""The squaring is there to stop the cancellation. The square root is there to
undo the squaring, so the answer comes back in the original units. Variance is in
&ldquo;points squared&rdquo;, which means nothing to a human. A standard deviation of 2 is
in points, which means something.""")
    + p("""You meet this immediately as feature scaling:""")
    + expr("Xs = (X - X.mean(0)) / X.std(0)",
           "centre every column on 0, then squash it to a spread of 1")
),

"f0-normal": (
    p("""The bell curve turns up so often that three numbers about it are worth simply
knowing. Measured from the middle outwards:""")
    + values([("within 1 standard deviation", "68.27%", "roughly two thirds of everything"),
              ("within 2", "95.45%", "the one people quote as &ldquo;95%&rdquo;"),
              ("within 3", "99.73%", "almost all of it")],
             "how much of the curve sits how far out")
    + p("""People say 68, 95, 99.7 and that is close enough for any decision you will
make.""")
    + point("""Read the last one the useful way round: something more than 3 standard
deviations from the middle happens about <b>27 times in every 10,000</b>. Rare &mdash; but
not impossible. Seeing one is <b>not</b> proof that anything is broken.""")
    + p("""That is exactly the judgement anomaly detection asks of you. It flags points out
in that thin tail, and choosing where to cut is choosing how many false alarms you will put
up with. The curve does not choose for you.""")
),

"f0-argmax": (
    cases([("max asks&hellip;", "<b>&ldquo;what is the biggest value?&rdquo;</b>"),
           ("argmax asks&hellip;", "<b>&ldquo;where is it?&rdquo;</b> &mdash; the position, "
                                   "not the value.")],
          "two words that look alike and answer different questions")
    + chainset([([" [0.1, 0.7, 0.2] ", "max = 0.7"], "the value itself"),
                ([" [0.1, 0.7, 0.2] ", "argmax = 1"],
                 "its slot &mdash; counting from <b>0</b>")],
               "same list, two questions")
    + p("""You meet the difference in the same breath every time you classify something. A
softmax layer hands you one probability per class &mdash; say [0.1, 0.7, 0.2] for
<b>cat, dog, bird</b>.""")
    + cases([("argmax tells you the answer",
              "slot 1, so the model said <b>dog</b>. This is what you show a user."),
             ("max tells you the confidence",
              "<b>0.70</b>. This is what you use to decide whether to trust it.")])
    + point("""NumPy counts from 0, so <b>argmax = 1 means the second item</b>. That
off-by-one is the single most common slip with this pair.""")
),

"f0-drill-dotprod": (
    p("""Work it on paper before reading on.""")
    + steps(["Pair them by position: <b>a = [1, 2, 3]</b>, <b>b = [4, 5, 6]</b>.",
             "1 &times; 4 = <b>4</b>",
             "2 &times; 5 = <b>10</b>",
             "3 &times; 6 = <b>18</b>",
             "Add: 4 + 10 + 18 = <b>32</b>"])
    + cases([("Trap 1 &mdash; it is ONE number",
              "If you wrote <b>[4, 10, 18]</b> you did the <i>elementwise</i> product, "
              "which is <code>a * b</code>. That is a different operation, and NumPy will "
              "happily do it for you without complaining."),
             ("Trap 2 &mdash; pairing is by POSITION",
              "First with first, second with second. Never the first with all of them.")],
           "the two ways this goes wrong")
    + expr("a @ b\nnp.dot(a, b)", "both give 32")
    + point("""Being able to do this by hand is what lets you read a shape error later,
when a layer says it wanted 3 and got 4.""")
),
}
