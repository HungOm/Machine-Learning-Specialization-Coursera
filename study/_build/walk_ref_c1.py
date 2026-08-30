# -*- coding: utf-8 -*-
"""The slow read for the Course 1 reference entries.

Reference sheet only — see build.walk_for(). Every number below was computed
before it was written.
"""
from walkkit import p, expr, chain, chainset, steps, cases, values, point, ascii_art

W = {

# ============================================================ W1
"c1w1-model": (
    p("""The whole model, and there is genuinely nothing hidden in it.""")
    + expr("f(x) = wx + b", "&ldquo;f of x equals w times x, plus b&rdquo;")
    + cases([("w &mdash; the weight",
              "How steep the line is. In houses: <b>how many dollars per square foot</b>. "
              "Turn it up and the line tilts."),
             ("b &mdash; the bias",
              "Where the line crosses the vertical axis &mdash; the prediction when x is "
              "0. Turn it up and the whole line slides upward.")],
            "two numbers, and that is the entire model")
    + point("""<b>w and b are learned. x is your data.</b> That split is the thing to hold
on to: training never touches x, it only ever hunts for better w and b.""")
    + p("""Every model in the rest of the specialization is this with more knobs. A neural
network has millions of them, arranged in layers, and each one is still just a number
being nudged.""")
),

"c1w1-notation": (
    p("""Three little raised numbers that look nearly identical. <b>Read the brackets
first</b> &mdash; the bracket style carries the whole meaning.""")
    + values([("x<sup>(2)</sup>", "round brackets", "training example number <b>2</b>. "
                                                    "Nothing is multiplied."),
              ("x<sup>2</sup>", "no brackets", "x <b>squared</b>. An ordinary power."),
              ("a<sup>[2]</sup>", "square brackets", "<b>layer 2</b> of a network. Course 2 "
                                                     "only.")],
             "the three, side by side")
    + point("""So <b>x<sub>3</sub><sup>(2)</sup></b>, which looks like the hardest thing on
the page, means <b>the second example, its third feature</b>. Superscript picks the row,
subscript picks the column. It is a spreadsheet address.""")
    + p("""The course is consistent about this, so once you trust the brackets you can stop
worrying about it. The confusion is real but it is only ever notation.""")
),

"c1w1-cost": (
    p("""The cost squashes every miss into <b>one number</b>, so that two candidate lines
can be compared.""")
    + expr("J(w,b) = (1 / 2m) &Sigma; ( f(x&#8317;&#8305;&#8318;) - y&#8317;&#8305;&#8318; )&sup2;",
           "&ldquo;J of w and b equals one over two m, times the sum over every example of "
           "the miss squared&rdquo;")
    + steps(["For each example, work out the <b>miss</b>: prediction minus truth.",
             "<b>Square</b> it. Now a miss of &minus;5 and a miss of +5 both count as 25, "
             "so they cannot cancel out.",
             "<b>Add</b> them all up.",
             "<b>Divide by m</b>, so the number is an average rather than a total.",
             "There is a <b>2</b> in the denominator as well. That one is pure "
             "convenience."])
    + cases([("Why square?",
              "It makes every miss positive, so overshooting and undershooting do not "
              "cancel. It also punishes <b>big</b> misses disproportionately &mdash; one "
              "miss of 10 costs as much as a hundred misses of 1."),
             ("Why the 2?",
              "Differentiating a square brings a 2 down in front. Putting a 2 underneath "
              "in advance means it <b>cancels</b>, and the gradient comes out clean. It "
              "changes nothing about where the minimum is.")],
            "the two bits that look arbitrary and are not")
),

"c1w1-cost-shape": (
    p("""The shape of J is not a detail. It is the reason gradient descent is guaranteed to
work here, and the reason that guarantee disappears in Course 2.""")
    + p("""With one parameter, J is a <b>parabola</b>. With two, it is a <b>bowl</b>.""")
    + ascii_art("""   J
   |  \\                    /
   |   \\                  /
   |    \\                /
   |     \\_            _/
   |       \\__      __/
   |          \\____/
   +---------------------------- w
                 ^
            one lowest point,
            and nowhere else to get stuck""")
    + steps(["J is a sum of <b>squared linear</b> terms.",
             "That makes it a <b>quadratic</b>.",
             "A quadratic bowl is <b>convex</b> &mdash; it curves the same way everywhere.",
             "A convex surface has <b>exactly one</b> minimum.",
             "So gradient descent finds the <b>global</b> best, from any starting point."])
    + point("""You lose this entirely once you build a neural network. Its cost surface is
lumpy, with many local dips, and where you start genuinely matters. Enjoy the guarantee
while Course 1 lasts &mdash; and know that it was a property of the <b>model</b>, never of
gradient descent.""")
),

"c1w1-contour": (
    p("""A contour plot is the bowl seen from directly above, the way a map draws a hill.
Each ring joins up points at the <b>same height</b>.""")
    + point("""So one ring is a set of <b>(w, b) pairs that all fit equally badly</b>.
Different lines, same cost. That is a genuinely surprising idea the first time: there is
not one second-best model, there is a whole ring of them.""")
    + values([("rings close together", "steep", "J changes fast here &mdash; a small move "
                                                "in w matters a lot"),
              ("rings far apart", "flat", "you can move a long way and barely change the "
                                          "cost"),
              ("the bullseye", "the answer", "the best possible w and b"),
              ("long stretched rings", "trouble", "an awkward narrow valley &mdash; and "
                                                  "exactly what feature scaling cures")],
             "how to read one")
),

"c1w1-gd-update": (
    p("""The whole of gradient descent, in two lines.""")
    + expr("w := w - &alpha; &part;J/&part;w\nb := b - &alpha; &part;J/&part;b",
           "&ldquo;w becomes w minus alpha times the slope in the w direction&rdquo;")
    + p("""<code>:=</code> is said &ldquo;<b>becomes</b>&rdquo;. It is an instruction to
replace, not a claim that the two sides are equal.""")
    + point("""The detail that is easy to get wrong: this is a <b>simultaneous</b> update.
Compute <b>both</b> slopes from the <b>old</b> w and b first, and only then assign both.""")
    + cases([("Right",
              "<code>dw, db = grads(w, b)</code><br><code>w = w - a*dw</code><br>"
              "<code>b = b - a*db</code>"),
             ("Wrong &mdash; and it will not crash",
              "<code>w = w - a*dw(w, b)</code><br><code>b = b - a*db(w, b)</code><br>"
              "The second line now uses the <b>new</b> w.")],
            "the classic Week 1 bug")
    + p("""The sequential version often still reduces J, which is exactly why the bug is
hard to spot. It just converges to something slightly wrong, quietly.""")
),

"c1w1-gd-sign": (
    p("""Why does <b>subtracting</b> the slope always walk you downhill? Check both cases
and you will never doubt it again.""")
    + cases([("The slope is POSITIVE",
              "Uphill is to the <b>right</b>.<br>Subtracting a positive number moves w "
              "<b>left</b>.<br>Left is downhill. &#10003;"),
             ("The slope is NEGATIVE",
              "Uphill is to the <b>left</b>.<br>Subtracting a negative number moves w "
              "<b>right</b>.<br>Right is downhill. &#10003;")],
            "both cases, worked")
    + point("""And at the minimum the slope is <b>exactly 0</b>, so nothing moves. Gradient
descent stops on its own. Nobody has to tell it when to stop.""")
    + p("""There is a bonus that is easy to miss: the steps <b>shrink automatically</b> as
you approach the bottom, because the slope itself is shrinking. You take big strides while
you are far away and small careful ones near the answer &mdash; without ever changing
&alpha;.""")
),

"c1w1-alpha": (
    p("""&alpha; (&ldquo;alpha&rdquo;), the learning rate, is how big a step to take. There
are four regimes and you can identify all of them from one plot of J.""")
    + values([("far too small", "converges &mdash; glacially",
               "J falls, but you will run out of patience first"),
              ("about right", "falls fast, then flattens", "what you want"),
              ("too large", "J oscillates", "it overshoots the bottom and bounces"),
              ("far too large", "J grows, then NaN", "diverged. Gone.")],
             "the four shapes of a J-against-iterations plot")
    + point("""<b>If J ever increases between two iterations, &alpha; is too large.</b>
That single rule is the most useful piece of debugging in the whole specialization, and it
costs three lines of matplotlib to check.""")
),

"c1w1-alpha-debug": (
    p("""Your model will not learn. Is it &alpha;, or is it a bug in the gradient? There is
a clean test that separates them.""")
    + expr("alpha = 0.0001", "absurdly small, on purpose")
    + cases([("J now decreases",
              "The gradient is <b>fine</b>. Your &alpha; was simply too large. Raise it "
              "gradually from here."),
             ("J still does not decrease",
              "It is <b>not</b> &alpha;. There is a <b>bug</b> &mdash; almost always a "
              "sign error, or the wrong index in the gradient.")],
            "run a few iterations and look")
    + point("""The reason this works is a guarantee, not a heuristic: with a small enough
step, J is <b>mathematically certain</b> to fall &mdash; provided the gradient is
correct. So if it does not fall, the gradient is what is wrong.""")
),

"c1w1-derivatives": (
    p("""The two slopes gradient descent needs. They are the same sum twice, with one small
difference.""")
    + expr("&part;J/&part;w = (1/m) &Sigma; ( f(x&#8317;&#8305;&#8318;) - y&#8317;&#8305;&#8318; ) &middot; x&#8317;&#8305;&#8318;\n"
           "&part;J/&part;b = (1/m) &Sigma; ( f(x&#8317;&#8305;&#8318;) - y&#8317;&#8305;&#8318; )",
           "identical, except the w version carries an extra x")
    + point("""That extra <b>&middot; x</b> is not decoration. It says: a miss on an example
with a <b>large x</b> is stronger evidence that the <b>slope</b> is wrong. A miss on a tiny
house tells you almost nothing about dollars-per-square-foot. The bias has no such factor,
because <b>b affects every example equally</b>.""")
    + p("""And this is where the mysterious <b>2</b> from <code>1/2m</code> went:
differentiating the square brings a 2 down in front, and it cancels the one you put
underneath. That is the entire reason it was there.""")
),

"c1w1-batch": (
    p("""&ldquo;Batch&rdquo; describes <b>how many examples each update looks at</b>. There
are three choices and the naming is genuinely confusing.""")
    + values([("batch", "all m", "every update reads the whole dataset. What Course 1 "
                                 "uses."),
              ("stochastic", "1", "one example per update. Noisy, but enormously more "
                                  "updates per second."),
              ("mini-batch", "32&ndash;512", "a subset. The practical compromise, and what "
                                             "all deep learning actually uses.")],
             "how many examples per step")
    + point("""So &ldquo;batch&rdquo; already meant <b>all of them</b> &mdash; which is why
the compromise had to be called <b>mini</b>-batch. The name is backwards from what most
people first assume.""")
),

"c1w1-three-parts": (
    p("""This is the most useful sentence in Course 1, and it holds for every algorithm
that follows.""")
    + steps(["A <b>model</b> &mdash; what f(x) is allowed to look like.",
             "A <b>cost function</b> &mdash; one number saying how wrong it is.",
             "An <b>optimiser</b> &mdash; gradient descent, which makes that number "
             "smaller."])
    + cases([("Course 2 changes part 1",
              "The model becomes a neural network. Cost and optimiser barely move."),
             ("Course 3 changes part 2",
              "The cost becomes a clustering objective, or a reward. The structure is "
              "untouched.")],
            "and then, for the rest of the specialization")
    + point("""When a new algorithm looks overwhelming, ask the three questions: <b>what is
the model, what is the cost, what is the optimiser?</b> Most of the apparent novelty is one
of the three having changed while the other two stayed put.""")
),

"c1w1-drill-cost": (
    p("""Work it on paper first.""")
    + p("""<b>x = [1, 2]</b>, <b>y = [300, 500]</b>, <b>w = 100</b>, <b>b = 100</b>.""")
    + steps(["Predict: f(1) = 100&times;1 + 100 = <b>200</b>, and "
             "f(2) = 100&times;2 + 100 = <b>300</b>.",
             "Misses: 200 &minus; 300 = <b>&minus;100</b>, and 300 &minus; 500 = "
             "<b>&minus;200</b>.",
             "Square them: <b>10,000</b> and <b>40,000</b>. Sum: <b>50,000</b>.",
             "Divide by 2m, which is 2&times;2 = 4: 50,000 &divide; 4 = <b>12,500</b>."])
    + point("""For comparison, the perfect fit here is <b>w = 200, b = 100</b>, which gives
<b>J = 0</b> exactly. So 12,500 is what &ldquo;visibly close but wrong&rdquo; costs &mdash;
useful for calibrating what a cost number is telling you.""")
),

# ============================================================ W2
"c1w2-multi-model": (
    p("""Same model, more columns. Written out in full, and then written properly.""")
    + expr("f(x) = w&#8321;x&#8321; + w&#8322;x&#8322; + ... + w&#8345;x&#8345; + b",
           "one weight per feature, plus one bias")
    + expr("f(x) = w &middot; x + b", "the same thing, using a dot product")
    + point("""The second form is not a shorthand or an approximation. <b>It is exactly the
first one</b> &mdash; a dot product multiplies position by position and adds, which is
precisely what the long version does.""")
    + cases([("n &mdash; features", "how many <b>columns</b>: size, bedrooms, age. One "
                                    "weight each."),
             ("m &mdash; examples", "how many <b>rows</b>: how many houses you have.")],
            "keep these two straight; almost every shape bug is confusing them")
),

"c1w2-subscripts": (
    p("""Read it as a spreadsheet address and it stops being frightening.""")
    + expr("x&#8322;&#8317;&#179;&#8318;", "&ldquo;x sub 2, superscript 3&rdquo;")
    + cases([("subscript 2", "<b>which feature</b> &mdash; which <b>column</b>."),
             ("superscript (3)", "<b>which example</b> &mdash; which <b>row</b>.")])
    + point("""So it is <b>feature 2 of training example 3</b>: one single number, one cell
of the table. Not a vector, not a matrix. One number.""")
    + p("""The round brackets on the superscript are doing real work &mdash; without them
it would read as <i>x&#8322; cubed</i>.""")
),

"c1w2-dot-vs-star": (
    p("""One is elementwise, one adds up. A neuron always wants the one that adds up.""")
    + cases([("w * x",
              "<code>[1,2,3] * [10,20,30]</code><br>gives <b>[10, 40, 90]</b><br>"
              "An <b>array</b> the same length. Nothing summed."),
             ("np.dot(w, x)",
              "<code>[1,2,3] &middot; [10,20,30]</code><br>gives <b>140</b><br>"
              "A single <b>number</b>. Multiplied <i>and</i> added.")],
            "note 10 + 40 + 90 = 140 &mdash; dot is star with a sum on the end")
    + point("""A prediction is one number, so a neuron needs the dot. If your prediction
comes out as a list, this is why.""")
    + p("""A related trap in the same family: a plain Python <b>list</b> times 2 gives you
<b>two copies of the list</b>; a NumPy <b>array</b> times 2 <b>doubles every number</b>.
Neither raises an error.""")
),

"c1w2-why-fast": (
    p("""&ldquo;NumPy is faster&rdquo; is true and useless. Here is the actual mechanism, in
three parts.""")
    + steps(["A Python <b>loop</b> pays interpreter overhead <b>per element</b> &mdash; "
             "check the type, find the method, box the result &mdash; a thousand times "
             "for a thousand numbers.",
             "<code>np.dot</code> hands one <b>contiguous block of memory</b> to compiled "
             "library code (BLAS) and pays that overhead <b>once</b>.",
             "That code uses <b>SIMD</b>: one CPU instruction that multiplies several "
             "pairs of numbers <i>at the same time</i>. Often across several cores too."])
    + point("""Same maths, same answer, <b>10&ndash;100&times;</b> the speed. Nothing
clever happened to the arithmetic; the overhead was removed and the work was done in
parallel.""")
    + p("""This is also, in one sentence, why GPUs matter for deep learning. A GPU is that
last step taken to an extreme: thousands of small units doing the same multiply-and-add at
once. Vectorising your code is what makes that possible.""")
),

"c1w2-scaling-why": (
    p("""Feature scaling looks like tidying. It is not &mdash; it changes the <b>shape of
the cost surface</b>, and that changes how fast gradient descent can move.""")
    + p("""If one feature runs 0&ndash;5 and another runs 0&ndash;2000, the bowl is not a
bowl. It is a <b>long thin canyon</b>.""")
    + ascii_art("""  unscaled: a canyon            scaled: a bowl
  +----------------------+      +----------------+
  |  ((((((((((((((()))  |      |     (( ))      |
  |  ->zig  zag<-        |      |      \\ /       |
  |  ((((((((((((((()))  |      |       *        |
  +----------------------+      +----------------+
   steps bounce across it        steps head straight in""")
    + steps(["A gradient step goes <b>perpendicular to the contour</b> it is standing on.",
             "In a narrow canyon, perpendicular points <b>across</b> the valley, not "
             "along it.",
             "So the path <b>zig-zags</b>, making progress towards the bottom very "
             "slowly.",
             "And you must keep &alpha; <b>small</b> to stop it bouncing out of the "
             "canyon &mdash; which makes the crawl slower still."])
    + point("""Scaled features give near-circular contours, so perpendicular points
<b>straight at the middle</b>, and a larger &alpha; is safe. You get a better direction and
a bigger step, from a one-line change.""")
),

"c1w2-scaling-how": (
    p("""Three ways to do it. You will use the third.""")
    + values([("divide by max", "x / max", "lands in 0&hellip;1"),
              ("mean normalisation", "(x &minus; &mu;) / (max &minus; min)",
               "roughly &minus;0.5&hellip;0.5"),
              ("z-score", "(x &minus; &mu;) / &sigma;",
               "mean 0, spread 1. <b>The usual choice.</b>")],
             "the three methods")
    + point("""Aim for roughly <b>&minus;1 to 1</b>. Andrew's rules of thumb:
&minus;3&hellip;3 is fine, &minus;0.3&hellip;0.3 is fine. But <b>0&hellip;0.001</b> or
<b>&minus;100&hellip;100</b> needs rescaling.""")
    + p("""The z-score is the default because it does not care about outliers the way
&ldquo;divide by max&rdquo; does &mdash; one freak value sets the maximum and squashes
everything else into a corner.""")
),

"c1w2-scaling-trap": (
    p("""Two mistakes, both silent, both very common.""")
    + cases([("1. Scaling before splitting",
              "You compute &mu; and &sigma; on the <b>whole</b> dataset, then split into "
              "train and test.<br>Those numbers now carry information about the test set. "
              "That is <b>leakage</b>: your test score is optimistic and you will not "
              "know."),
             ("2. Forgetting to scale at prediction time",
              "The model was trained on standardised inputs. Feed it a raw <b>2000</b> "
              "and it returns nonsense &mdash; without any error, because 2000 is a "
              "perfectly valid number.")],
            "the two classic feature-scaling bugs")
    + point("""The rule that prevents both: <b>fit the scaler on the training set only</b>,
then apply those <i>same</i> &mu; and &sigma; everywhere else &mdash; validation, test, and
every future prediction. <code>sklearn</code>'s <code>fit</code> / <code>transform</code>
split exists precisely to make this hard to get wrong.""")
),

"c1w2-convergence": (
    p("""Plot J against iteration number. It is three lines of matplotlib and it is the
cheapest diagnostic in machine learning.""")
    + values([("falls, then flattens", "healthy, done", "it has converged. Stop."),
              ("falls, still falling", "healthy, not done", "run it longer."),
              ("oscillates up and down", "&alpha; too large", "reduce it."),
              ("increases steadily", "&alpha; far too large, or a bug",
               "if shrinking &alpha; does not fix it, it is a bug")],
             "the four shapes and what each means")
    + point("""Notice that three of the four are diagnosed <b>by eye, in seconds</b>. Not
plotting this is the most common reason people spend an afternoon on something a glance
would have told them.""")
),

"c1w2-alpha-ladder": (
    p("""There is no formula for &alpha;. There is a procedure, and it takes about two
minutes.""")
    + steps(["Try a ladder roughly <b>&times;3</b> apart: "
             "<b>0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1</b>.",
             "<b>Plot J against iterations</b> for each one.",
             "Keep the <b>largest</b> &alpha; that still decreases <b>smoothly</b>.",
             "Optionally back off one notch, for safety on data you have not seen."])
    + point("""Why <b>&times;3</b> rather than <b>+0.1</b>? Because &alpha; acts
<b>multiplicatively</b> on the step size. Going from 0.001 to 0.1 is a hundredfold change;
going from 0.9 to 1.0 is almost nothing. <b>Equal ratios</b> matter, not equal
differences.""")
),

"c1w2-feateng": (
    p("""A linear model cannot learn that <b>area = frontage &times; depth</b> matters.
Not &ldquo;finds it difficult&rdquo; &mdash; <b>cannot</b>, at all, ever.""")
    + expr("f = w&#8321;x&#8321; + w&#8322;x&#8322; + b",
           "a weighted SUM. There is no multiplication of features anywhere in it")
    + point("""There is no choice of w&#8321; and w&#8322; that produces a <b>product</b>.
It is outside what the model can represent, so no amount of training or data will find
it.""")
    + p("""So you compute it yourself and hand it over:""")
    + expr("x&#8323; = x&#8321; * x&#8322;", "now the model has a column for area")
    + point("""That is <b>feature engineering</b>, and it is where domain knowledge enters a
machine-learning system. Knowing that estate agents price by area, not by frontage, is
worth more here than any amount of tuning. It is also exactly the job neural networks
eventually take over &mdash; which is the entire pitch of Course 2.""")
),

"c1w2-polyreg": (
    p("""Fitting a curve, still using linear regression, and the name is not a mistake.""")
    + expr("f = w&#8321;x + w&#8322;x&sup2; + w&#8323;x&sup3; + b", "a curve &mdash; and still linear regression")
    + point("""<b>&ldquo;Linear&rdquo; refers to being linear in the parameters w, not in
x.</b> The formula is still a plain weighted sum; the fact that the features happen to be
powers of x changes nothing whatsoever about the algorithm.""")
    + p("""So you can fit curves, wiggles and arcs without leaving Course 1. You are not
using a fancier model &mdash; you are feeding the same model cleverer columns.""")
    + point("""One consequence is <b>not</b> optional. If x runs 1&ndash;1000, then
x&sup3; runs 1&ndash;1,000,000,000. Those two columns cannot share a learning rate, so
<b>feature scaling becomes mandatory</b> the moment you add a power.""")
),

"c1w2-drill-zscore": (
    p("""Work it on paper first. &mu; = <b>218.67</b>, &sigma; = <b>39.96</b>, and this
house has x = <b>200</b>.""")
    + steps(["Subtract the mean: 200 &minus; 218.67 = <b>&minus;18.67</b>.",
             "Divide by the standard deviation: &minus;18.67 &divide; 39.96 = "
             "<b>&minus;0.47</b>."])
    + chain(["x = 200", "z = &minus;0.47"], "about half a standard deviation below average")
    + point("""The <b>sign</b> is the readable part: negative means <b>below average</b>.
And the <b>size</b> is in units of &ldquo;typical spread&rdquo;, so &minus;0.47 says this
house is smaller than usual but entirely unremarkable. A z of &minus;3 would be a genuinely
odd house.""")
),

# ============================================================ W3
"c1w3-why-not-linreg": (
    p("""Two separate reasons, and the second one is the one people underrate.""")
    + cases([("1. The output is unbounded",
              "A straight line will happily predict <b>&minus;0.4</b> or <b>1.8</b>. "
              "Neither can be read as a class, and neither can be a probability."),
             ("2. Outliers drag the boundary",
              "Squared error punishes the line for being <b>far</b> from a point &mdash; "
              "even a point that is unambiguously in its own class. So one clear-cut "
              "example, far out, pulls the whole decision boundary towards itself.")],
            "why linear regression fails at classification")
    + point("""Reason 2 is the worse one, because reason 1 you would <b>notice</b>. A
prediction of 1.8 is visibly wrong. A boundary quietly dragged three units to the left
looks like a working model that is simply not very good.""")
    + p("""The sigmoid fixes both at once. It bounds the output, and because it
<b>saturates</b>, a point far out on the correct side contributes almost nothing &mdash; so
it cannot pull anything.""")
),

"c1w3-sigmoid": (
    p("""The one new piece of machinery in Week 3.""")
    + expr("g(z) = 1 / (1 + e&#8315;&#7859;)",
           "&ldquo;g of z equals one over one plus e to the minus z&rdquo;")
    + steps(["Compute <b>z = w &middot; x + b</b> &mdash; exactly as in linear regression.",
             "Push z through <b>g</b>, which squashes it into 0&hellip;1.",
             "Read the result as <b>P(y = 1)</b> &mdash; the chance this example is a "
             "positive."])
    + values([("always strictly between 0 and 1", "never 0, never 1",
               "so it can always be a probability"),
              ("g(0) = 0.5", "exactly", "because e&#8304; = 1, so it is 1/(1+1)"),
              ("symmetric", "g(&minus;z) = 1 &minus; g(z)",
               "the chance of yes at z equals the chance of no at &minus;z")],
             "three properties worth knowing")
    + point("""The model is unchanged underneath. Logistic regression is linear regression
with a squash on the end &mdash; which is why almost every formula from Weeks 1 and 2
carries over untouched.""")
),

"c1w3-sigmoid-values": (
    p("""A handful of values worth simply knowing, so you can sanity-check an output at a
glance.""")
    + values([("g(&minus;5)", "0.007", "confidently no"),
              ("g(&minus;2)", "0.12", "probably no"),
              ("g(0)", "0.50", "exactly undecided"),
              ("g(2)", "0.88", "probably yes"),
              ("g(5)", "0.993", "confidently yes")],
             "the sigmoid at five points")
    + point("""Past about <b>&plusmn;5</b> the sigmoid has <b>saturated</b>: extra distance
changes the answer almost not at all. g(5) is 0.993 and g(50) is 0.9999999&hellip; &mdash;
practically the same.""")
    + p("""That saturation is exactly why outliers stop dragging the boundary. A point
sitting way out at z = 40, on the correct side, is <b>already</b> as right as it can be, so
it contributes essentially no gradient. Squared error had no such mercy.""")
),

"c1w3-boundary": (
    p("""Where does the model change its mind? At <b>P = 0.5</b> &mdash; and the sigmoid
gives 0.5 at exactly one input.""")
    + chain(["g(z) = 0.5", "z = 0", "w &middot; x + b = 0"],
            "so the boundary is wherever z is zero")
    + point("""The shape of that boundary is a property of <b>the features you supply</b>,
not of logistic regression.""")
    + cases([("Features x&#8321;, x&#8322;",
              "<b>w&#8321;x&#8321; + w&#8322;x&#8322; + b = 0</b><br>That is the equation "
              "of a <b>straight line</b>."),
             ("Features x&#8321;&sup2;, x&#8322;&sup2;",
              "<b>w&#8321;x&#8321;&sup2; + w&#8322;x&#8322;&sup2; + b = 0</b><br>That is "
              "the equation of a <b>circle</b>.")],
            "same model, same algorithm, different columns")
    + point("""The model is <b>always linear in z</b>. A curved boundary does not make it a
neural network &mdash; it just means you fed it curved features. This is the same idea as
polynomial regression, wearing different clothes.""")
),

"c1w3-why-not-sq-error": (
    p("""Two reasons, and both matter.""")
    + cases([("1. The surface stops being a bowl",
              "f now has a <b>sigmoid inside it</b>. Squaring the error of a squashed "
              "function gives a <b>non-convex</b> surface &mdash; many local dips instead "
              "of one bowl. Gradient descent can now get stuck."),
             ("2. Learning stalls exactly when it matters",
              "The gradient would pick up a <b>g&prime;(z)</b> factor, and g&prime; is "
              "<b>near zero</b> when the model is confident. So a confidently <b>wrong</b> "
              "prediction produces a tiny gradient. It learns slowest precisely where it "
              "is most wrong.")],
            "why squared error is the wrong cost here")
    + point("""Reason 2 is the one that would actually ruin your training run. It is also
exactly what the log loss fixes: the <code>1/f</code> from the logarithm cancels the
<code>g&prime;</code>, so a confident mistake gives a <b>large</b> gradient, as it
should.""")
),

"c1w3-logloss": (
    p("""Written as two cases, then folded into one line.""")
    + cases([("If y = 1", "loss = <b>&minus;log(f)</b><br>Reward a high f."),
             ("If y = 0", "loss = <b>&minus;log(1 &minus; f)</b><br>Reward a low f.")],
            "the two cases")
    + expr("L(f, y) = -y log(f) - (1 - y) log(1 - f)", "the same thing in one line")
    + point("""It folds because <b>y is only ever 0 or 1</b>. Whichever it is, one of the
two terms is multiplied by zero and vanishes. Nothing clever is happening &mdash; it is a
switch written as arithmetic.""")
    + p("""This is <b>binary cross-entropy</b>, and you will use it for every binary
classifier you ever build, including the output layer of a neural network. It is worth
knowing both forms: the two-case version is what it <i>means</i>, the one-line version is
what you <i>type</i>.""")
),

"c1w3-logloss-shape": (
    p("""The point of this loss is what it does to a <b>confidently wrong</b> answer.""")
    + chainset([(["y = 1, f = 0.99", "loss 0.01"], "confident and right &mdash; nearly free"),
                (["y = 1, f = 0.50", "loss 0.69"], "hedging &mdash; a moderate charge"),
                (["y = 1, f = 0.01", "loss 4.61"], "confidently <b>wrong</b> &mdash; "
                                                   "460&times; the first")],
               "the true answer is 1. What each prediction costs")
    + point("""The penalty heads for <b>infinity</b> as f approaches 0. There is no ceiling
on being confidently wrong, which is exactly the incentive you want.""")
    + p("""<b>&minus;log(0.5) = 0.693</b> is the reference point worth memorising: it is
what a model scores by refusing to commit at all. A classifier averaging <b>below</b> 0.693
is beating a coin flip. Above it, it is worse than useless &mdash; and that single number
will tell you so in one glance.""")
),

"c1w3-why-log": (
    p("""Two reasons, and neither is &ldquo;because it works&rdquo;.""")
    + cases([("1. It makes the cost convex again",
              "One bowl, one minimum. Gradient descent gets its guarantee back &mdash; "
              "the same guarantee the sigmoid had just taken away."),
             ("2. It is the negative log-likelihood",
              "It is <b>derived</b>: the w and b that minimise it are exactly the ones "
              "that make the data you actually observed <b>most probable</b>.")],
            "why a logarithm")
    + point("""So the log loss is not a trick someone found. It falls out of statistics
&mdash; assume a yes/no outcome, apply maximum likelihood, take the negative log, and this
is what you get. See the Foundations entry on maximum likelihood for that derivation.""")
    + p("""The sigmoid and the log loss are a <b>matched pair</b>. The tidiness &mdash; the
clean <code>(f &minus; y)</code> gradient &mdash; disappears the moment you pair either of
them with something else.""")
),

"c1w3-gd-logistic": (
    p("""The gradient for logistic regression, and the most satisfying line in Course 1.""")
    + expr("w&#11388; := w&#11388; - &alpha; (1/m) &Sigma; ( f(x&#8317;&#8305;&#8318;) - y&#8317;&#8305;&#8318; ) x&#11388;&#8317;&#8305;&#8318;",
           "compare it, character by character, with linear regression")
    + point("""It is <b>identical</b>. The only difference is what <b>f</b> means:
<b>g(w&middot;x + b)</b> instead of <b>w&middot;x + b</b>. Two completely different
algorithms, one gradient formula.""")
    + p("""And it is not a coincidence or a happy accident. The derivative of the sigmoid is
<b>g&prime;(z) = g(z)(1 &minus; g(z))</b>, and the derivative of the logarithm contributes
a <b>1/f</b>. They cancel <b>exactly</b>, leaving the plain error term behind.""")
    + point("""Which is why swapping in a different loss, or a different squashing function,
loses the tidiness. The pair was chosen so that this cancellation happens.""")
),

"c1w3-overfit": (
    p("""Two failures that both look like &ldquo;the model is bad&rdquo; and need
<b>opposite</b> fixes. That is why naming them matters.""")
    + cases([("Underfitting  (high bias)",
              "<b>Poor</b> on training data.<br><b>Poor</b> on new data.<br>"
              "The model is <b>too simple</b> to capture the pattern.<br>"
              "&rarr; add features, add capacity, reduce &lambda;."),
             ("Overfitting  (high variance)",
              "<b>Excellent</b> on training data.<br><b>Poor</b> on new data.<br>"
              "The model is <b>too flexible</b> and memorised the noise.<br>"
              "&rarr; more data, fewer features, raise &lambda;.")],
            "the two, side by side")
    + point("""The <b>gap</b> between training and new-data performance is the diagnostic.
Both bad and close together means underfitting. Training excellent and the gap large means
overfitting. You cannot tell them apart from the training score alone &mdash; which is the
entire reason a validation set exists.""")
),

"c1w3-address-overfit": (
    p("""Three ways to fix overfitting, in the order they are usually reached for.""")
    + values([("more data", "the best fix", "and often impossible, or expensive"),
              ("fewer features", "works", "but you may throw away one that mattered"),
              ("regularisation", "usually first", "keep every feature, shrink the weights")],
             "three options")
    + point("""Regularisation beats feature selection because it does <b>not force a binary
choice</b>. Dropping a feature says &ldquo;this is worth exactly nothing&rdquo;. Shrinking
its weight says &ldquo;this is worth a little&rdquo; &mdash; which is usually closer to the
truth, and the data decides how much.""")
),

"c1w3-regcost": (
    p("""One cost, two jobs, pulling against each other.""")
    + expr("J = (1/2m) &Sigma; ( f - y )&sup2;  +  (&lambda;/2m) &Sigma; w&#11388;&sup2;",
           "fit the data &hellip; and keep the weights small")
    + cases([("First term", "<b>Fit the data.</b> Pushes the weights wherever they need "
                            "to go to reduce the misses."),
             ("Second term", "<b>Keep the weights small.</b> Pushes every weight back "
                             "towards zero, in proportion to how big it already is.")],
            "the tug of war")
    + values([("&lambda; = 0", "no penalty", "the original cost. Overfits."),
              ("&lambda; just right", "balanced", "fits the shape, ignores the noise"),
              ("&lambda; enormous", "all w &asymp; 0", "f &asymp; b, a flat line. Underfits.")],
             "what &lambda; does at the extremes")
    + point("""Note the sum starts at <b>j = 1</b>: <b>b is not regularised</b>. Shrinking b
only slides the whole curve up and down &mdash; it does nothing about wiggliness, which is
the thing you were trying to control.""")
),

"c1w3-weight-decay": (
    p("""Take the regularised update and gather the w terms together. A second name for the
same thing falls out.""")
    + expr("w&#11388; := (1 - &alpha;&lambda;/m) w&#11388;  -  &alpha; (1/m) &Sigma; ( f - y ) x&#11388;",
           "shrink first, then take the ordinary step")
    + point("""So every single iteration <b>multiplies w by a number just below 1</b> before
doing anything else. The weights leak away steadily unless the data keeps pushing them back
up. That is why it is called <b>weight decay</b>.""")
    + values([("&alpha; = 0.01, &lambda; = 1, m = 100", "&times; 0.9999", "a very gentle leak"),
              ("&alpha; = 0.1, &lambda; = 10, m = 100", "&times; 0.99",
               "1% of every weight, every iteration")],
             "the shrink factor, worked")
    + point("""This is the <code>weight_decay</code> argument in every modern optimiser
&mdash; AdamW, <code>kernel_regularizer=l2(0.01)</code>, all of it. You have already met the
thing; only the name changes.""")
    + p("""One warning that file 02 in the build lane demonstrates: if
<b>&alpha;&lambda;/m</b> exceeds 2, that factor goes past &minus;1, and the weights flip
sign and <b>grow</b> every step. &alpha; and &lambda; are not independent knobs.""")
),

"c1w3-drill-sigmoid": (
    p("""Work it on paper first. <b>w = 1</b>, <b>b = 0</b>, <b>x = 1.5</b>.""")
    + steps(["<b>z</b> = 1 &times; 1.5 + 0 = <b>1.5</b>",
             "<b>e<sup>&minus;1.5</sup></b> = <b>0.2231</b>",
             "<b>1 + 0.2231</b> = <b>1.2231</b>",
             "<b>1 &divide; 1.2231</b> = <b>0.818</b>"])
    + chain(["x = 1.5", "z = 1.5", "g(z) = 0.818"], "an 82% chance of being class 1")
    + point("""0.818 is above 0.5, so this example is classified <b>&#375; = 1</b> &mdash;
and fairly confidently. Note the two separate steps: the model produced a <b>probability</b>
of 0.818, and then a <b>threshold</b> of 0.5 turned it into a decision. The threshold was
your choice, not the model's.""")
),

}
