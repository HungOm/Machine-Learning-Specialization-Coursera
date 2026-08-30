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

# ---------------------------------------------------------------- W2, NumPy and pandas
W.update({

"f0-list-vs-array": (
    p("""Two things that look identical and behave completely differently. Neither errors,
which is what makes it a trap rather than a bug you would notice.""")
    + cases([("x is a LIST",
              "<code>[1, 2, 3] * 2</code><br>gives <b>[1, 2, 3, 1, 2, 3]</b><br>"
              "It <b>repeated the list</b>. To Python, <code>*</code> on a list means "
              "&ldquo;give me two of these&rdquo;."),
             ("x is a NumPy ARRAY",
              "<code>np.array([1,2,3]) * 2</code><br>gives <b>[2, 4, 6]</b><br>"
              "It <b>doubled each number</b>, which is what you meant.")],
            "the same three characters, two different answers")
    + point("""So: <b>always <code>np.array(my_list)</code> before doing maths.</b> If a
result is suddenly twice as long as it should be, this is why.""")
    + p("""The reason underneath is memory. A Python list holds <i>pointers</i> to objects
that could each be anything &mdash; a number, a string, another list &mdash; scattered
around. A NumPy array holds <b>raw numbers of one type in a solid block</b>. That layout is
where the speed comes from, and it is why an array will not let you mix types.""")
),

"f0-slicing": (
    p("""A slice takes a run of elements. The rule everybody gets wrong is the second
number.""")
    + expr("x[1:4]", "&ldquo;from 1, stop before 4&rdquo; &mdash; positions 1, 2 and 3")
    + p("""With <code>x = [0,1,2,3,4,5,6,7,8,9]</code>, <code>x[1:4]</code> gives
<b>[1, 2, 3]</b>. Three elements, not four. The end is <b>excluded</b>.""")
    + point("""The handy consequence: the number of elements is just
<b>end &minus; start</b>. 4 &minus; 1 = 3. You never have to count.""")
    + values([("x[0]", "first", "counting starts at zero"),
              ("x[-1]", "last", "negative counts back from the end"),
              ("x[:3]", "from the start", "a missing number means &ldquo;all the way&rdquo;"),
              ("x[3:]", "to the end", "same rule, other side"),
              ("M[:, 2]", "all rows, column 2", "comma separates the dimensions")],
             "the whole vocabulary")
    + point("""One more, and it bites: a slice is a <b>view</b>, not a copy. Change the
slice and you have changed the original array. Use <code>.copy()</code> when you mean a
copy.""")
),

"f0-axis": (
    p("""<code>axis</code> is the single most confusing argument in NumPy, and there is one
rule that makes it permanent.""")
    + point("""<b>The axis you name is the one that disappears.</b>""")
    + p("""Take a table of shape <b>(3, 4)</b> &mdash; 3 rows, 4 columns.""")
    + cases([("axis=0",
              "The <b>3</b> disappears.<br>Result shape <b>(4,)</b><br>"
              "One answer <b>per column</b> &mdash; it went down the rows."),
             ("axis=1",
              "The <b>4</b> disappears.<br>Result shape <b>(3,)</b><br>"
              "One answer <b>per row</b> &mdash; it went across the columns.")],
            "(3, 4) with a sum applied")
    + p("""So do not try to remember which is which. Ask: <b>what shape do I want out?</b>
Then name the number that has to go.""")
    + cases([("One statistic per feature", "&rarr; <code>axis=0</code>. The mean of each "
                                           "column, for scaling."),
             ("One prediction per example", "&rarr; <code>axis=1</code>. The argmax across "
                                            "the classes, for classifying.")],
            "the two you will actually use")
),

"f0-broadcast": (
    p("""Broadcasting lets NumPy add a small array to a big one by silently stretching the
small one. It is enormously useful and it is the source of the nastiest silent bug in
NumPy.""")
    + steps(["<b>Line the two shapes up from the RIGHT.</b>",
             "They are compatible at a position if the numbers are <b>equal</b>, or if one "
             "of them is <b>1</b>.",
             "A dimension of 1 gets <b>stretched</b> to match the other."])
    + cases([("The one you want",
              "<code>(1000, 4) + (4,)</code> &rarr; <b>(1000, 4)</b><br>"
              "One bias per feature, added to all 1000 examples. Exactly right."),
             ("The one that ruins your day",
              "<code>(3, 1) + (1, 3)</code> &rarr; <b>(3, 3)</b><br>"
              "<b>Both</b> stretched. You wanted three numbers and got nine, and "
              "<b>nothing warned you</b>.")],
            "the same rule, two very different outcomes")
    + point("""When a result has a surprising shape, broadcasting is almost always what
happened. The fix is a habit, not a cleverness: <b>print the shapes</b> either side of the
line that surprised you.""")
),

"f0-star-vs-at": (
    p("""One character apart, and they do genuinely different things.""")
    + cases([("a * b &mdash; elementwise",
              "<code>[1,2,3] * [4,5,6]</code><br>gives <b>[4, 10, 18]</b><br>"
              "Same length in, same length out. Nothing is added up."),
             ("a @ b &mdash; dot / matmul",
              "<code>[1,2,3] @ [4,5,6]</code><br>gives <b>32</b><br>"
              "It multiplies <i>and then adds</i>. Collapses to one number.")],
            "note that 4 + 10 + 18 = 32 &mdash; @ is * with a sum on the end")
    + point("""Here is why it is dangerous rather than merely different: on two <b>square</b>
matrices, both operations run and both return the <b>same shape</b>. Only one of them is
the one you meant, and nothing warns you. The model just trains badly.""")
    + p("""Prefer <code>@</code> to <code>np.dot</code>. They agree on 1-D and 2-D, and
<code>np.dot</code> starts doing something different once you go past two dimensions
&mdash; which you will, the moment you touch batches.""")
),

"f0-mask": (
    p("""This one line computes accuracy, and it works because of a small piece of Python
that is easy to miss.""")
    + expr("(preds == y).mean()", "the fraction that match")
    + steps(["<code>preds == y</code> compares the two arrays position by position. It "
             "gives back an array of <b>True/False</b> &mdash; a <i>mask</i>.",
             "In arithmetic, <b>True counts as 1</b> and <b>False counts as 0</b>.",
             "So the <b>mean</b> of that array is exactly the fraction that are True."])
    + chain(["[T, F, T, T]", "[1, 0, 1, 1]", "mean = 0.75"],
            "three right out of four")
    + point("""Combining conditions: use <code>&amp;</code> and <code>|</code>, <b>not</b>
<code>and</code> / <code>or</code>. And give every condition its own brackets &mdash;
<code>(a &gt; 1) &amp; (b &lt; 2)</code>. Without the brackets Python reads the operators in
the wrong order and the error message will not tell you that.""")
),

"f0-reshape": (
    p("""Both turn a <b>(2, 3)</b> into a <b>(3, 2)</b>. They do not give the same numbers,
and confusing them silently scrambles your data.""")
    + p("""Start from <code>[[1, 2, 3], [4, 5, 6]]</code>.""")
    + cases([("reshape(3, 2)",
              "<b>[[1, 2], [3, 4], [5, 6]]</b><br>It read the numbers out in order "
              "&mdash; 1,2,3,4,5,6 &mdash; and <b>re-cut</b> them into rows of two."),
             (".T  (transpose)",
              "<b>[[1, 4], [2, 5], [3, 6]]</b><br>It <b>mirrored</b> the positions. The "
              "first row became the first column.")],
            "same shape out, different numbers in it")
    + point("""<code>reshape</code> re-cuts a sequence. <code>.T</code> tips the table on
its side. If your model suddenly learns nothing, check you did not reshape where you meant
to transpose.""")
    + values([("reshape(1, -1)", "one row", "the fix when a library insists on 2-D; "
                                            "<b>&minus;1</b> means &ldquo;work it out&rdquo;"),
              (".T on a 1-D array", "nothing", "no second dimension to swap with. A real "
                                               "and very common surprise")])
),

"f0-pandas-five": (
    p("""Five calls, in this order, on every dataset before you model anything. It takes
about twenty seconds and it saves hours.""")
    + steps(["<code>df.head()</code> &mdash; <b>look at it</b>. Actually look. Half the "
             "problems are visible here.",
             "<code>df.shape</code> &mdash; how much data is there? (rows, columns).",
             "<code>df.info()</code> &mdash; the <b>types</b> of each column, and how many "
             "values are missing.",
             "<code>df.describe()</code> &mdash; min, max, mean per column. Tells you "
             "whether you need feature scaling.",
             "<code>df.columns</code> &mdash; the <b>exact spelling</b> of the names, "
             "including capitals and stray spaces."])
    + point("""Step 3 is the one that earns its keep. <code>info()</code> catches the
classic bug: a column of numbers that arrived as <b>text</b> because one row contains
&ldquo;N/A&rdquo;. Everything downstream then behaves bizarrely and the error surfaces
somewhere far away.""")
),

"f0-to-numpy": (
    p("""Getting <b>X</b> and <b>y</b> out of a DataFrame, and the shape trap waiting at the
end of it.""")
    + expr("X = df[['size', 'beds']].to_numpy()   # (m, 2)\ny = df['price'].to_numpy()            # (m,)",
           "pick the columns first, then convert")
    + point("""Select the columns <b>before</b> converting. Afterwards the names are gone
&mdash; a NumPy array has no column headings, only positions.""")
    + cases([("df['price']  &mdash; one bracket",
              "gives shape <b>(m,)</b><br>A flat list of m numbers. <b>This is what you "
              "want for y.</b>"),
             ("df[['price']]  &mdash; two brackets",
              "gives shape <b>(m, 1)</b><br>A table with one column. Looks the same when "
              "printed. Is not.")],
            "one bracket versus two")
    + point("""If you end up with <b>(m, 1)</b> where a library wanted <b>(m,)</b>, the fix
is <code>y.ravel()</code>. The symptom is usually a broadcasting surprise several lines
later, not an error here.""")
),

"f0-traceback": (
    p("""A traceback looks like a wall of unfamiliar file paths. Almost none of it is yours,
and you read it <b>from the bottom</b>.""")
    + steps(["<b>Read the LAST line first.</b> It names the error and describes it in "
             "plain English. This is the answer about 80% of the time.",
             "<b>Then the frame just above it</b> &mdash; that is the line of your code "
             "where it broke.",
             "<b>Only then</b> work upwards, and only if you still need to know how you "
             "got there."])
    + point("""The middle is just the chain of calls that led in &mdash; mostly library
files you did not write and do not need to read. Length is not difficulty: a fifty-line
traceback and a five-line one are usually equally easy.""")
    + p("""Two habits fix most of what you will hit here:""")
    + expr("print(X.shape, y.shape)\nprint(type(X), X.dtype)",
           "print the shapes, print the types")
),

"f0-five-errors": (
    p("""These five account for nearly everything you will hit in the labs.""")
    + values([("ValueError: shapes not aligned", "shape bug",
               "print both shapes; one probably needs <code>.T</code>"),
              ("IndexError: out of bounds", "counting",
               "positions start at <b>0</b>; the last is <code>x[-1]</code>"),
              ("TypeError: can only concatenate list", "list, not array",
               "wrap it: <code>np.array(my_list)</code>"),
              ("NameError: not defined", "typo, or unrun cell",
               "in Jupyter, usually an import cell you never ran"),
              ("KeyError: 'Price'", "wrong column name",
               "<code>print(df.columns)</code> &mdash; it is probably lowercase")],
             "the error, what it really means, and the fix")
    + point("""Notice that four of the five are <b>not</b> mistakes about machine learning.
They are mistakes about shapes, types and spelling. That ratio holds up in real work
too.""")
),

"f0-function-read": (
    p("""You will constantly meet functions you have never seen. You almost never need to
read the body. Three things tell you nearly everything.""")
    + steps(["<b>Its name.</b> Decent code names things honestly: "
             "<code>compute_cost</code> computes the cost.",
             "<b>Its parameters</b> &mdash; what it needs from you, matched <b>in order</b> "
             "unless you name them.",
             "<b>What it returns</b> &mdash; one value, or a tuple of several."])
    + point("""That is enough to <i>use</i> it, which is exactly what every graded exercise
asks of you. The exercises hand you the signature and the docstring precisely because
reading the body is not the skill being tested.""")
    + p("""One trap: a function with <b>no</b> <code>return</code> hands back
<code>None</code>. Nothing complains at the time; you get a confusing failure several lines
later when something tries to do arithmetic on <code>None</code>.""")
),

})

# ---------------------------------------------------------------- W3, behind the curtain
W.update({

"f0-eigen": (
    p("""Most directions get rotated when you multiply them by a matrix. A few special ones
do not &mdash; they only get longer or shorter, and keep pointing the same way. Those are
the <b>eigenvectors</b>.""")
    + expr("A v = &lambda; v",
           "&ldquo;A times v equals lambda times v&rdquo; &mdash; a whole matrix acting "
           "like a single number")
    + p("""Try it on <b>A = [[2, 1], [1, 2]]</b>.""")
    + cases([("Direction [1, 1]",
              "A &times; [1, 1] = <b>[3, 3]</b><br>Same direction, <b>3&times;</b> as long. "
              "So &lambda; = <b>3</b>."),
             ("Direction [1, &minus;1]",
              "A &times; [1, &minus;1] = <b>[1, &minus;1]</b><br>Unchanged. So &lambda; = "
              "<b>1</b>.")],
            "two directions this matrix does not rotate")
    + point("""That is the whole appeal. Along those directions only, a matrix &mdash; a
grid of numbers doing something complicated &mdash; collapses to <b>one number</b>. Find
them and you have found the axes the matrix is really working in.""")
),

"f0-pca-why": (
    p("""PCA says &ldquo;find the direction of greatest variance&rdquo;. Linear algebra says
&ldquo;find the largest eigenvector of the covariance matrix&rdquo;. Those sound like two
different instructions and they are the same one.""")
    + point("""The link is one sentence: <b>each eigenvalue IS the variance along its own
eigenvector.</b> So sorting eigenvalues largest-first <i>is</i> sorting directions by how
much the data spreads along them.""")
    + p("""Covariance matrices are also <b>symmetric</b>, which buys two guarantees that
make PCA well behaved rather than merely plausible:""")
    + cases([("The eigenvalues are real",
              "No imaginary numbers turn up in the middle of your variances, which for a "
              "general matrix they can."),
             ("The eigenvectors are perpendicular",
              "So the second component measures something the first one <b>cannot see</b>. "
              "No double counting.")],
            "why symmetry matters here")
),

"f0-svd": (
    p("""Every matrix, without exception, is three simple things done in a row.""")
    + expr("A = U &Sigma; V&#7488;", "&ldquo;U sigma V transpose&rdquo;")
    + steps(["<b>V&#7488;</b> &mdash; a <b>rotation</b>. Turn the space.",
             "<b>&Sigma;</b> &mdash; a <b>stretch</b>. Scale each axis, by the singular "
             "values.",
             "<b>U</b> &mdash; another <b>rotation</b>. Turn it again."])
    + point("""Rotate, stretch, rotate. That is all any matrix ever does, however
complicated it looks.""")
    + cases([("Why it beats eigendecomposition",
              "Eigendecomposition needs a <b>square</b> matrix. SVD works on <b>any</b> "
              "matrix &mdash; and your data table is 1000&times;4, not square."),
             ("Why truncating it is safe",
              "&Sigma; comes back <b>sorted, largest first</b>. Keep the top k and you have "
              "the <b>provably best</b> rank-k approximation. Not a heuristic &mdash; a "
              "theorem.")],
            "two reasons it is the factorisation worth knowing")
    + p("""And the bridge back to PCA: a singular value <b>squared, divided by n</b>, is
exactly a covariance eigenvalue. Real PCA implementations use SVD, because building the
covariance matrix first squares the numbers and throws away precision you did not have to
lose.""")
),

"f0-mle": (
    p("""Where do loss functions come from? They are not invented. They are derived, from
one principle.""")
    + point("""<b>Choose the parameters that make the data you actually saw as probable as
possible.</b> That is maximum likelihood, in full.""")
    + p("""Work it on ten coin flips that came up <b>7 heads</b>. If the coin lands heads
with probability p, the chance of seeing exactly that is:""")
    + expr("L(p) = p&#8311; (1 - p)&sup3;", "how likely this exact result was, for each p")
    + chain(["p = 0.5 &rarr; 0.00098", "p = 0.7 &rarr; 0.00222", "p = 0.9 &rarr; 0.00048"],
            "the peak is at p = 0.7 &mdash; which is just 7 out of 10")
    + p("""The answer is the obvious one, which is the point: the principle agrees with
common sense on an easy case, and then keeps working on hard ones.""")
    + cases([("Assume Gaussian noise", "&rarr; you <b>derive</b> squared error."),
             ("Assume a yes/no outcome", "&rarr; you <b>derive</b> cross-entropy.")],
            "and here is what it gives you")
    + point("""So the loss function stops being an arbitrary choice someone made and becomes
a <b>consequence of what you assumed about the noise</b>. Take the negative log of it and
products become sums, and nothing underflows &mdash; which is exactly why every loss you
meet has a log in it.""")
),

"f0-jacobian": (
    p("""A gradient is what you get when a function has <b>one</b> output. A Jacobian is
what you get when it has several.""")
    + expr("J&#7522;&#11388; = &part;f&#7522; / &part;x&#11388;",
           "row i, column j: how much output i moves when input j moves")
    + cases([("Rows are OUTPUTS", "one row per thing the function returns."),
             ("Columns are INPUTS", "one column per thing you could change.")],
            "the only thing to remember about the layout")
    + p("""So a function taking <b>n</b> numbers in and giving <b>m</b> out has an
<b>m &times; n</b> grid of slopes.""")
    + point("""And the gradient you already use is just <b>a Jacobian with one row</b>
&mdash; because a cost function has exactly one output. It was never a different object.""")
    + p("""This is also what backpropagation <i>is</i>. The chain rule, in many dimensions,
becomes matrix multiplication; backprop evaluates that product <b>right to left</b>, which
keeps a single row vector at every step instead of ever building the enormous square
matrices in the middle. That ordering is the entire trick.""")
),

"f0-softmax-grad": (
    p("""Two intimidating pieces of calculus &mdash; the derivative of softmax, and the
derivative of cross-entropy &mdash; multiply together and almost everything cancels.""")
    + expr("&part;L / &part;z = p - y",
           "predicted probabilities minus the true one-hot answer")
    + p("""Work it on <b>z = [2, 1, 0.5]</b> where the <b>first</b> class is the true
one.""")
    + values([("softmax(z)", "[0.6285, 0.2312, 0.1402]", "the predicted probabilities"),
              ("y, one-hot", "[1, 0, 0]", "the truth: it really was class one"),
              ("p &minus; y", "[&minus;0.3715, 0.2312, 0.1402]", "and that is the gradient")],
             "no calculus required at the point of use")
    + point("""Read the signs. The <b>true</b> class has a negative gradient &mdash; push
its score <b>up</b>. Every wrong class has a positive one &mdash; push those <b>down</b>.
The size of each push is exactly how wrong that probability was.""")
    + p("""<b>Why it cancels:</b> softmax's derivative carries a factor of
<b>p&#7527;</b>, and the log inside cross-entropy contributes <b>1 / p&#7527;</b>. They
annihilate. It is the same cancellation that makes the sigmoid and log loss pair up in
C1 W3, and it is why these two are always used together &mdash; pair either with something
else and you lose the clean gradient.""")
),

})
