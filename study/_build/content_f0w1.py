# -*- coding: utf-8 -*-
"""Foundations · Week 1 — The maths you actually need."""
from kit import (kid, key, warn, trap, note, card, eq, eqp, decode, table, demo,
                 quiz, links, code, h2, grid2, grid3, pretest)

L = []

def lesson(slug, title, mins, lede, body):
    L.append(dict(slug=slug, title=title, mins=mins, tag="foundations", lede=lede, body=body))


# ============================================================ 1
lesson("01-what-is-a-function", "What a function is", 8,
    "The single most important idea in the whole specialization, and the one nobody stops to explain. "
    "A machine: number in, number out.",
    pretest("""<p>A machine takes a number, doubles it, and adds one. You feed in <b>3</b> and get <b>7</b>. You feed in 3 again tomorrow. <b>What comes out — and how sure are you?</b></p>""",
        """<p>Your certainty is the whole idea. Watch for the word that names “same input, same output, always” — it is the property everything else in this course is built on.</p>""")
    + h2("🎈", "The idea, in plain words")
    + kid("""<p>A vending machine. You put a coin in one slot, and a chocolate bar comes out the other.
Same coin, same chocolate bar, every time.</p>
<p>A function is exactly that, with numbers. Put 3 in, get 7 out. Put 3 in again, get 7 again — always.</p>
<p>That is genuinely the whole idea. Everything else in this course is built on top of it.</p><p>Try the actual rule this lesson uses later: “double it, then add one”. Feed in 3 and the machine does 2×3 + 1 and hands back 7. Feed in 3 again next week and it still hands back 7 — that reliability, not the arithmetic, is what makes it a function.</p>""")

    + h2("🔤", "The symbol, and how to say it")
    + eqp([
        ("<var>f</var>(<var>x</var>)", "func-f", "apply f to x"),
        ' <span class="op">=</span> 2<var>x</var> <span class="op">+</span> 1',
    ], "read as: “f of x equals two x plus one” — click f(x)")
    + decode([
        ("<var>f</var>", "“eff”", "the machine's <b>name</b>. Could equally be g, h, J or σ — they are all just names."),
        ("<var>x</var>", "“ex”", "whatever you put in. Also called the <b>input</b>, or the <b>argument</b>."),
        ("<var>f</var>(<var>x</var>)", "“f of x”", "what comes out. <b>Not</b> f multiplied by x — the brackets mean “applied to”."),
        ("=", "“is”", "the two sides are the same thing, written differently."),
        ("<var>f</var>(3)", "“f of three”", "put 3 in. The answer is 2(3) + 1 = 7."),
    ])
    + warn("""<p><b>f(3) does not mean f × 3.</b> This trips up almost everybody once. In maths, brackets
directly after a letter usually mean multiplication — but after a <em>function name</em> they mean “feed
this in”. You tell them apart by knowing f is a function, which you only know from context.</p>""")

    + h2("🧮", "Worked by hand")
    + table(["Put in (x)", "The working", "Get out f(x)"],
            [["0", "2(0) + 1", "<b>1</b>"],
             ["1", "2(1) + 1", "<b>3</b>"],
             ["3", "2(3) + 1", "<b>7</b>"],
             ["−2", "2(−2) + 1", "<b>−3</b>"],
             ["0.5", "2(0.5) + 1", "<b>2</b>"]])

    + h2("🎬", "Watch it move")
    + demo("ffnmachine", "Drop a number in one end",
           "change x, change the machine, watch what falls out")

    + h2("💻", "In NumPy")
    + code("""
def f(x):
    return 2 * x + 1

f(3)                       # 7  -- one number in, one out

import numpy as np
xs = np.array([0, 1, 3, -2, 0.5])
f(xs)                      # array([ 1.,  3.,  7., -3.,  2.])
""")
    + """<p>That last line is worth staring at. You wrote the function for <b>one</b> number, and it
worked on <b>five at once</b>, with no loop. That is NumPy doing the work — and it is why almost no
machine learning code contains a loop over examples.</p>"""

    + h2("🔬", "What is actually happening")
    + """<p>“Function” means something slightly stricter than “rule”. It means: <b>one input can never
give two different outputs</b>. Feed in 3 and you get 7, today and forever.</p>
<p>Why that matters here: a machine learning model <em>is</em> a function. Its input is your data, its
output is a prediction. Training does not change the function — it changes some numbers <em>inside</em>
it (w and b), which is the same as swapping the vending machine for a slightly different one.</p>
<p>So when you read <b>f<sub>w,b</sub>(x)</b> later, the little subscript is saying: “this is the machine
set up with these particular dials”.</p>"""

    + h2("🕳", "Traps")
    + trap("""<p><b>Reading f(x) as multiplication.</b> If you see <code>f(x + 1)</code>, it means “put
x + 1 into the machine” — not “f times x plus f”.</p>""")
    + trap("""<p><b>Assuming f always means the same thing.</b> Different chapters reuse f, g and h freely.
Check what has just been defined.</p>""")

    + h2("✅", "Check yourself")
    + quiz([
        ("f(x) = 3x − 4. What is f(2)?",
         "<p>3(2) − 4 = 6 − 4 = <b>2</b>.</p>"),
        ("f(x) = x². What is f(−3)?",
         "<p>(−3) × (−3) = <b>9</b>. A negative times a negative is positive.</p>"),
        ("Can a function give two different answers for the same input?",
         "<p><b>No</b> — that is precisely what would stop it being a function. Same input, same output, "
         "always.</p>"),
    ])

    + h2("🔗", "Go deeper")
    + links([
        ("video", "https://www.khanacademy.org/math/algebra/x2f8bb11595b61c86:functions",
         "Khan Academy — Functions",
         "Free, from the very beginning, with practice problems. If this lesson felt fast, start here."),
        ("play", "https://www.desmos.com/calculator",
         "Desmos graphing calculator",
         "Type <code>y = 2x + 1</code> and drag things. Ten minutes here builds more intuition than an hour of reading."),
    ]))

# ============================================================ 2
lesson("02-reading-a-graph", "Reading a graph", 7,
    "A graph is a picture of a function. Learning to read one — across, then up, then across — makes "
    "every diagram in the specialization legible.",
    pretest("""<p>Someone says “the line goes up steeply from left to right”. <b>Without any formula: what two things must you know about the picture before that sentence means anything at all?</b></p>""",
        """<p>Watch for the two labels that turn a squiggle into information. Most confusion later is not about maths — it is about not checking these first.</p>""")
    + h2("🎈", "The idea, in plain words")
    + kid("""<p>A graph is a map of a function. Every dot on the line is one question and its answer,
side by side.</p>
<p>To use it: go <b>across</b> the bottom to your question, then <b>up</b> until you hit the line, then
<b>left</b> to read off the answer. Always that order.</p><p>Say the graph tracks a plant’s height by day. Find 4 along the bottom, go up until you hit the line, then look across — land on 12 and you have just read “12&nbsp;cm tall on day&nbsp;4” straight off the picture, with no formula involved at all.</p>""")

    + h2("🔤", "The symbol, and how to say it")
    + decode([
        ("<var>x</var>-axis", "“the ex axis”", "the line along the bottom. Your input."),
        ("<var>y</var>-axis", "“the why axis”", "the line up the side. The output."),
        ("origin", "“the origin”", "where the two cross: the point (0, 0)."),
        ("(3, 7)", "“the point three, seven”", "<b>across 3, up 7</b>. Across always comes first."),
        ("<var>y</var> = <var>f</var>(<var>x</var>)", "“y equals f of x”", "just says the height of the line is whatever the function gives."),
    ])

    + h2("🎬", "Watch it move")
    + demo("freadgraph", "Slide along the bottom and read off the answer",
           "the blue dashes go up, the green dashes go across")

    + h2("💻", "In NumPy")
    + code("""
import numpy as np
import matplotlib.pyplot as plt

xs = np.linspace(-3, 5, 200)      # 200 evenly spaced x values
ys = 0.6 * xs**2 - 1.2 * xs + 1.5 # the y value at each one

plt.plot(xs, ys)
plt.xlabel('x'); plt.ylabel('y')
plt.axhline(0, color='grey', lw=0.8)   # draw the axes
plt.axvline(0, color='grey', lw=0.8)
""")
    + """<p>A curve on a screen is not really a curve — it is a few hundred straight lines joining a few
hundred dots. <code>linspace</code> makes the dots; more dots means a smoother-looking curve.</p>"""

    + h2("🔬", "What is actually happening")
    + """<p>The computer never draws a curve. It evaluates the function at 200 x values, gets 200 y values,
and joins the dots with straight segments. At 200 points your eye cannot see the joins.</p>
<p>This matters practically: if a plot looks suspiciously angular, the fix is usually more points, not a
different plotting command.</p>
<p>It also explains a phrase you will meet — a <b>“decision boundary”</b> is drawn the same way: evaluate
the model on a grid of points, and colour each one by what it predicts.</p>"""

    + h2("🕳", "Traps")
    + trap("""<p><b>Reading (3, 7) as up 3, across 7.</b> It is always <b>across first</b>. The mnemonic
people use: “along the corridor, then up the stairs”.</p>""")
    + trap("""<p><b>Assuming the axes start at zero.</b> Plotting libraries often crop to the data. Always
glance at the numbers on the axes before believing a shape.</p>""")

    + h2("✅", "Check yourself")
    + quiz([
        ("A point is at (−2, 5). Where is it?",
         "<p>Two to the <b>left</b> of the origin, and five <b>up</b>.</p>"),
        ("A line passes through (0, 4). What does that tell you?",
         "<p>That when x = 0, y = 4 — so it crosses the y-axis at 4. In <code>y = wx + b</code> that "
         "means <b>b = 4</b>.</p>"),
    ])

    + h2("🔗", "Go deeper")
    + links([
        ("play", "https://www.desmos.com/calculator",
         "Desmos", "Type a formula, see the picture instantly. The fastest way to build graph intuition."),
        ("docs", "https://matplotlib.org/stable/tutorials/pyplot.html",
         "matplotlib — pyplot tutorial",
         "The plotting library every notebook in this course uses."),
    ]))

# ============================================================ 3
lesson("03-greek-letters", "Greek letters and other symbols", 7,
    "Not maths — vocabulary. A page you can come back to whenever a formula throws a symbol at you.",
    pretest("""<p>You meet <b>α</b>, <b>Σ</b> and <b>μ</b> in a formula. <b>Guess whether these are three quantities you must calculate, or something else entirely.</b></p>""",
        """<p>Watch for what a symbol actually <em>is</em>. They are not maths — they are vocabulary, and the only hard part is that nobody says them out loud for you.</p>""")
    + h2("🎈", "The idea, in plain words")
    + kid("""<p>Maths ran out of letters. So it borrowed the Greek alphabet.</p>
<p>There is nothing clever going on: α is just a letter, like calling a variable <code>a</code>. The only
reason symbols feel hard is that nobody ever says them out loud, so you cannot hold them in your head.</p>
<p>Say each one aloud once. That is the entire lesson.</p><p>Think of it the way a new job has jargon on day one — “standup”, “sprint”, “blocker” — words that sound intimidating for about a week, until somebody simply tells you what they mean once. α, β and the rest are exactly that: ordinary words, borrowed from Greek, that this field happens to use instead of English ones.</p>""")

    + h2("🎬", "Watch it move")
    + demo("fgreek", "Every symbol you will meet in these three courses",
           "say the highlighted one out loud — that is genuinely the exercise")

    + h2("🔤", "The ones that carry meaning")
    + """<p>Most Greek letters are just names. A few have a <b>conventional</b> meaning that holds across
the whole field — worth knowing, because seeing them tells you what kind of thing you are looking at.</p>"""
    + decode([
        ("<var>α</var>", "“alpha”", "the <b>learning rate</b> — how big a step gradient descent takes."),
        ("<var>λ</var>", "“lambda”", "<b>regularisation strength</b> — how hard you push weights towards zero."),
        ("<var>μ</var>", "“mu”, rhymes with “few”", "the <b>mean</b> — the plain average."),
        ("<var>σ</var>", "“sigma”", "the <b>standard deviation</b> — how spread out something is."),
        ("<var>σ</var><sup>2</sup>", "“sigma squared”", "the <b>variance</b>. Sigma is its square root."),
        ("<var>ε</var>", "“epsilon”", "something <b>tiny</b> — a threshold, or a guard against dividing by zero."),
        ("<var>γ</var>", "“gamma”", "the <b>discount factor</b> in reinforcement learning."),
        ("<var>θ</var>", "“theta”", "<b>parameters</b> — another name for the collection of w and b."),
    ])
    + note("""<p><b>Capital letters are different symbols, not loud versions.</b> Lowercase σ is a standard
deviation; capital <b>Σ</b> means “add these up”. Lowercase π is 3.14159; capital <b>Π</b> means “multiply
these together”. They are unrelated, and the courses use all four.</p>""", "Capitals matter")

    + h2("🔬", "What is actually happening")
    + """<p>There is a genuine reason conventions exist. When a paper writes <b>α</b> without explanation,
every reader in the field already knows it is a learning rate. The symbol is compressing a whole sentence.</p>
<p>The flip side: conventions clash. <b>π</b> is 3.14159 everywhere in mathematics and a <em>policy</em> in
reinforcement learning. <b>σ</b> is a standard deviation in statistics and the <em>sigmoid function</em> in
deep learning. Context, not the symbol, tells you which — and if a paper is confusing, this is often why.</p>"""

    + h2("🕳", "Traps")
    + trap("""<p><b>Assuming a symbol means what it meant last chapter.</b> Always check what has just been
defined. Authors redefine freely.</p>""")

    + h2("✅", "Check yourself")
    + quiz([
        ("You see “α = 0.01” in some code. What is it, most likely?",
         "<p>The <b>learning rate</b> — the step size for gradient descent. 0.01 is a very typical value.</p>"),
        ("What is the difference between σ and Σ?",
         "<p>Lowercase <b>σ</b> is the standard deviation (a number). Capital <b>Σ</b> is an instruction: "
         "“add all of these up”. Completely unrelated.</p>"),
        ("A reinforcement learning paper uses π. Is it 3.14159?",
         "<p>Almost certainly not — in RL, π is the <b>policy</b>, the rule mapping states to actions.</p>"),
    ])

    + h2("🔗", "Go deeper")
    + links([
        ("docs", "https://en.wikipedia.org/wiki/Greek_alphabet",
         "The Greek alphabet",
         "All 24 letters with pronunciations, if you want the complete set."),
        ("docs", "https://en.wikipedia.org/wiki/Glossary_of_mathematical_symbols",
         "Glossary of mathematical symbols",
         "A lookup table for anything this page missed."),
    ]))

# ============================================================ 4
lesson("04-slope", "Slope — rise over run", 8,
    "The steepness of a line, as a single number. Get this and gradient descent stops being mysterious, "
    "because gradient descent is entirely about slopes.",
    pretest("""<p>Two hills. On the first you walk 2 steps forward and rise 6. On the second, 2 steps forward and rise 2. <b>How many times steeper is the first — and what single number would you use to say so?</b></p>""",
        """<p>Do 6÷2 and 2÷2 before reading. Watch for the name of that division, and for what a <em>negative</em> answer would mean.</p>""")
    + h2("🎈", "The idea, in plain words")
    + kid("""<p>Slope answers one question: <b>if I take one step to the right, how far up do I go?</b></p>
<p>A gentle ramp has a small slope. A steep hill has a big one. Walking downhill gives a negative one.
Flat ground gives zero.</p><p>Two hikers climb for 2 steps. One rises 6 inches; the other rises only 2. The first hill is steeper — three times as steep, in fact, since 6 ÷ 2 is three times 2 ÷ 2. That ratio, rise divided by run, is the whole of slope.</p>""")

    + h2("🔤", "The symbol, and how to say it")
    + eqp([
        ("slope <span class=\"op\">=</span> <span class=\"frac\"><span>rise</span><span>run</span></span>", "slope-f0", "rise over run"),
        ' <span class="op">=</span> <span class="frac"><span>how far UP</span><span>how far ACROSS</span></span>',
    ], "“rise over run” — click it")
    + decode([
        ("rise", "“the rise”", "the change in y — how much it went up. Negative if it went down."),
        ("run", "“the run”", "the change in x — how far you moved across."),
        ("<var>m</var>", "“em”", "the usual letter for slope in school maths."),
        ("<var>w</var>", "“double-you”", "the <b>same thing</b>, in machine learning. A weight <em>is</em> a slope."),
        ("Δ", "“delta”", "“the change in”. Δy / Δx is another way of writing rise over run."),
    ])
    + key("""<p>School writes a line as <b>y = mx + c</b>. This course writes it as <b>f(x) = wx + b</b>.
Identical. m and w are both the slope; c and b are both where it crosses. Only the letters changed.</p>""")

    + h2("🧮", "Worked by hand")
    + """<p>A line goes through (1, 3) and (3, 9).</p>
<ul>
<li>rise = 9 − 3 = <b>6</b> (how much y changed)</li>
<li>run = 3 − 1 = <b>2</b> (how much x changed)</li>
<li>slope = 6 / 2 = <b>3</b></li>
</ul>
<p>So every step right, the line climbs 3. Sanity check: from (1, 3), stepping one right should reach
(2, 6). Does the line pass through there? Yes.</p>"""

    + h2("🎬", "Watch it move")
    + demo("fslope", "Drag the slope and the starting height",
           "the blue and green sides of the triangle are the run and the rise")

    + h2("💻", "In NumPy")
    + code("""
import numpy as np

x = np.array([1, 3])
y = np.array([3, 9])

rise = y[1] - y[0]        # 6
run  = x[1] - x[0]        # 2
slope = rise / run        # 3.0

# NumPy can also fit the best straight line through many points:
xs = np.array([1, 2, 3, 4])
ys = np.array([3, 5, 7, 9])
w, b = np.polyfit(xs, ys, 1)     # 1 means "a straight line"
print(w, b)                      # 2.0  1.0   ->  y = 2x + 1
""")

    + h2("🔬", "What is actually happening")
    + """<p>Slope is a <b>rate</b>. That word connects it to everything else you will meet.</p>
<ul>
<li>Distance against time → the slope is <b>speed</b>.</li>
<li>Cost against a weight → the slope is <b>how much the cost changes per unit of weight</b>. That is
exactly the number gradient descent uses.</li>
</ul>
<p>Notice also that a straight line has the <em>same</em> slope everywhere. That is what makes it straight.
A curve has a different slope at every point — which is why curves need the next lesson.</p>"""

    + h2("🕳", "Traps")
    + trap("""<p><b>Getting rise and run the wrong way up.</b> Rise is on top. If you compute run/rise you
get the reciprocal, and the answer will look plausible and be wrong.</p>""")
    + trap("""<p><b>Subtracting the points in a different order on top and bottom.</b> If rise is
y₂ − y₁, then run must be x₂ − x₁. Mixing the order flips the sign.</p>""")

    + h2("✅", "Check yourself")
    + quiz([
        ("A line goes through (2, 5) and (6, 13). What is the slope?",
         "<p>rise = 13 − 5 = 8. run = 6 − 2 = 4. slope = 8/4 = <b>2</b>.</p>"),
        ("A line has slope −3. What happens as you move right?",
         "<p>It goes <b>down</b> by 3 for every 1 across. Negative slope means downhill.</p>"),
        ("In f(x) = wx + b, which letter is the slope?",
         "<p><b>w</b>. And b is where the line crosses the y-axis — the value when x = 0.</p>"),
    ])

    + h2("🔗", "Go deeper")
    + links([
        ("video", "https://www.khanacademy.org/math/algebra/x2f8bb11595b61c86:linear-equations-graphs",
         "Khan Academy — slope and linear equations",
         "With practice problems. Worth an evening if lines are new to you."),
    ]))

# ============================================================ 5
lesson("05-derivatives", "What a derivative actually is", 10,
    "The slope of a curve at one exact point. This is the single piece of calculus the whole "
    "specialization runs on — and you need the meaning, not the rules.",
    pretest("""<p>Slope needs two points. A curve's steepness changes everywhere, and you only have <b>one</b> point. <b>How would you cheat?</b></p>""",
        """<p>Whatever trick you invented is probably the real one. Watch for what happens as the second point slides closer and closer — and for the word that names where it settles.</p>""")
    + h2("🎈", "The idea, in plain words")
    + kid("""<p>A straight line has one slope everywhere. A curve is steeper in some places than others —
so “the slope of a curve” only makes sense if you say <b>where</b>.</p>
<p>But slope needs <em>two</em> points, and you only have one. So cheat: take a second point very close by,
work out rise over run, then slide it closer. And closer. The number it settles on is the slope at your
point.</p>
<p>That settled number is the derivative.</p><p>A speedometer does this trick continuously. It cannot watch you drive for a whole minute and report one speed, because your speed might change within that minute — so instead it compares where you are now against where you were a tiny fraction of a second ago, and reports that ratio. Shrink the fraction small enough and you get your speed at this <em>exact</em> instant, which is exactly what a derivative does to a curve.</p>""")

    + h2("🔤", "The symbol, and how to say it")
    + eqp([
        ("<var>f</var>′(<var>x</var>) <span class=\"op\">=</span> <span class=\"frac\"><span><var>d</var><var>f</var></span><span><var>d</var><var>x</var></span></span>",
         "derivative-f0", "the slope, at x"),
        ' <span class="op">=</span> lim<sub><var>h</var>→0</sub> <span class="frac"><span><var>f</var>(<var>x</var>+<var>h</var>) − <var>f</var>(<var>x</var>)</span><span><var>h</var></span></span>',
    ], "three ways to write the same thing — click the first")
    + decode([
        ("<var>f</var>′(<var>x</var>)", "“f prime of x”", "the derivative. The little dash is all it is."),
        ("<var>df</var>/<var>dx</var>", "“dee f by dee x”", "the same thing. Reads as “the rate of change of f with respect to x”."),
        ("<var>h</var>", "“aitch”", "the tiny gap to the second point. Sometimes written Δx."),
        ("lim<sub><var>h</var>→0</sub>", "“the limit as h goes to zero”", "“keep shrinking the gap and see what number it approaches”."),
        ("<var>∂f</var>/<var>∂x</var>", "“partial dee f by dee x”", "the curly version, used when there is more than one variable. Next lesson."),
    ])
    + key("""<p>You do <b>not</b> need to be able to differentiate by hand to finish this specialization.
You need three things: a derivative is a <b>slope</b>; its <b>sign</b> says which way is uphill; its
<b>size</b> says how steep. TensorFlow computes the actual numbers.</p>""")

    + h2("🧮", "Worked by hand")
    + """<p>Take f(x) = x², at the point x = 3. Try shrinking gaps:</p>"""
    + table(["gap h", "f(3+h)", "rise", "rise / run", "getting close to…"],
            [["1", "16", "16 − 9 = 7", "7 / 1 = <b>7</b>", ""],
             ["0.5", "12.25", "3.25", "<b>6.5</b>", ""],
             ["0.1", "9.61", "0.61", "<b>6.1</b>", ""],
             ["0.01", "9.0601", "0.0601", "<b>6.01</b>", "…6"],
             ["→ 0", "", "", "<b>6</b>", "the derivative"]])
    + """<p>So the slope of x² at x = 3 is <b>6</b>. And the general rule — which you can now believe
rather than memorise — is that the derivative of x² is <b>2x</b>. At x = 3: 2(3) = 6. ✓</p>"""

    + h2("🎬", "Watch it move")
    + demo("fderiv", "Shrink the gap and watch the two lines merge",
           "orange is the line through two points; green dashes are the true slope at the point")

    + h2("💻", "In NumPy")
    + code("""
import numpy as np

def f(x):
    return x ** 2

# the definition, done numerically
def derivative(f, x, h=1e-5):
    return (f(x + h) - f(x)) / h

derivative(f, 3.0)        # 6.00001...   ~ the exact answer is 6

# NumPy can also do it across a whole array of points
xs = np.linspace(-3, 3, 7)
np.gradient(f(xs), xs)    # slopes at each point: [-6, -4, -2, 0, 2, 4, 6]
""")
    + warn("""<p>Do not make <code>h</code> too small. At h = 1e-15 the two f values round to the same
number, the top becomes exactly 0, and your answer is garbage. The sweet spot is around 1e-5 to 1e-7 — the
same floating-point limitation you meet again in Course 2, Week 2.</p>""")

    + h2("🔬", "What is actually happening")
    + """<p>Three rules cover almost everything in these courses, and they are worth <em>recognising</em>
even if you never apply them:</p>"""
    + table(["Function", "Derivative", "In words"],
            [["x²", "2x", "the power comes down in front, and drops by one"],
             ["x³", "3x²", "same rule again"],
             ["3x", "3", "a straight line has the same slope everywhere"],
             ["7 (a constant)", "0", "flat — nudging x changes nothing"]])
    + """<p>The deeper point: a derivative turns a <b>function</b> into another <b>function</b>. f(x) = x²
tells you the height at each x. f′(x) = 2x tells you the <em>steepness</em> at each x. Two different
questions about the same curve.</p>
<p>And notice from the animation: the closer the two points get, the more the chord lies on top of the
tangent. “Zoom in far enough and any smooth curve looks straight” is the whole idea of calculus in one
sentence.</p>"""

    + h2("🕳", "Traps")
    + trap("""<p><b>Thinking the derivative is a number.</b> f′(x) is a whole function — it has a different
value at every x. f′(3) is a number.</p>""")
    + trap("""<p><b>Confusing f′(x) with f(x).</b> One is the height, the other is the steepness. At x = 0
on the curve x², the height is 0 and the slope is also 0 — coincidence, not a rule.</p>""")

    + h2("✅", "Check yourself")
    + quiz([
        ("f(x) = x². What is the slope at x = −2?",
         "<p>2x = 2(−2) = <b>−4</b>. Negative, so the curve is heading downhill there.</p>"),
        ("The derivative at some point is 0. What does that mean?",
         "<p>The curve is <b>flat</b> there — the tangent is horizontal. Usually a peak, a valley bottom, "
         "or a plateau. Gradient descent stops dead at such a point.</p>"),
        ("Why does gradient descent need derivatives at all?",
         "<p>Because the <b>sign</b> tells it which way is downhill and the <b>size</b> tells it how far "
         "it can safely step. It never needs to know where the minimum is.</p>"),
    ])

    + h2("🔗", "Go deeper")
    + links([
        ("video", "https://www.3blue1brown.com/topics/calculus",
         "3Blue1Brown — Essence of Calculus",
         "Chapters 1–3 cover everything you need. If calculus never clicked at school, this is the single best fix available."),
        ("docs", "https://www.khanacademy.org/math/differential-calculus",
         "Khan Academy — Differential Calculus",
         "Free, with practice, if you want to be able to actually compute them."),
    ]))

# ============================================================ 6
lesson("06-partial-derivatives", "Partial derivatives", 10,
    "What to do when a function has several inputs. Freeze all but one, and you are back to an ordinary "
    "slope.",
    pretest("""<p>You are standing on a hillside with <b>two</b> dials, and the height depends on both. <b>How could you talk about “the steepness” at all, when steepness depends on which way you walk?</b></p>""",
        """<p>Watch for the trick: freeze one dial, wiggle the other. The curly ∂ is just notation for “I froze the rest”.</p>""")
    + h2("🎈", "The idea, in plain words")
    + kid("""<p>Picture a landscape with two directions you can walk: call one <b>w</b> (east–west) and
the other <b>b</b> (north–south). At every spot (w, b) the ground has a height, and that height is
<b>J</b>. So J is a machine that takes a spot and hands back a height:</p>
<p style="text-align:center"><var>J</var>(<var>w</var>, <var>b</var>) = your height, given where you
are standing</p>
<p>“How steep is it?” is not yet a complete question — steep walking <b>which way</b>? East might be a
cliff while north is flat. So you have to ask two separate, narrower questions: “if I walk exactly
east, how steep is it?” and “if I walk exactly north, how steep is it?”</p>
<p>Each of those is a question about walking along a single straight line — and a line has an ordinary
slope you already know how to find. That is the entire idea. A partial derivative freezes every
direction except one, and a hillside becomes a curve.</p><p>Picture a video-game character standing on this hillside with two joysticks in hand: one moves w, the other moves b. Push only the w joystick a little and the height changes one way; push only the b joystick and it changes a different way. A partial derivative is simply “how much did pushing this <em>one</em> joystick change the height”.</p>""")

    + h2("🧭", "Meet the letters before the symbol")
    + """<p>Before the ∂ shows up, it is worth being completely sure what each letter in
<var>J</var>(<var>w</var>, <var>b</var>) is standing for — both in the hillside picture and in the
machine-learning problem it represents.</p>"""
    + decode([
        ("<var>w</var>", "“double-u”", "your east–west position on the hillside. In a real model, one of the <b>parameters</b> being learned."),
        ("<var>b</var>", "“bee”", "your north–south position. In a real model, another <b>parameter</b> — often literally called the bias."),
        ("<var>J</var>", "“jay”", "your height — a single number the spot produces. In a real model, the <b>cost</b>: how wrong the current parameters are."),
    ])
    + """<p>So “find the slope of the mountain” is really “find out how the <b>cost</b> changes when one
<b>parameter</b> moves” — the hillside is just a picture of the cost function, drawn so you can see it.</p>"""

    + h2("🔤", "The symbol, and how to say it")
    + eqp([
        ('<span class="frac"><span>∂<var>J</var></span><span>∂<var>w</var></span></span>', "partial-f0", "the slope, at w"),
    ], "“partial dee J by dee w”, or just “dee J dee w” — click it")
    + decode([
        ("∂", "“partial” or “curly dee”", "a curly d. Its <b>only</b> job is to say “there are other variables, and they are being held still”."),
        ("<var>d</var> (straight)", "“dee”", "used when there is only one variable in the whole problem — the ordinary derivative from the last lesson."),
        ("∂<var>J</var>/∂<var>w</var>", "—", "how much J changes when you nudge <b>w</b> alone, with b frozen."),
        ("∂<var>J</var>/∂<var>b</var>", "—", "how much J changes when you nudge <b>b</b> alone, with w frozen."),
        ("∇<var>J</var>", "“grad J” or “del J”", "the <b>gradient</b>: all the partial derivatives, collected into one list."),
    ])

    + h2("🧮", "Worked by hand")
    + """<p>Take J(w, b) = w² + 2b².</p>
<p><b>∂J/∂w</b>: freeze b — pretend it is a fixed number, say 7. Then 2b² becomes a plain constant, and
constants differentiate to 0. All that is left to differentiate is w², which gives <b>2w</b>.</p>
<p><b>∂J/∂b</b>: freeze w instead. w² vanishes as a constant, and 2b² differentiates to <b>4b</b>.</p>
<p>Now put in actual numbers: w = 3, b = 1.</p>
<p>∂J/∂w = 2w = 2(3) = <b>6</b>. &nbsp;∂J/∂b = 4b = 4(1) = <b>4</b>. So the gradient at this spot is
<b>∇J = [6, 4]</b>.</p>
<p>Those two numbers are directly comparable, and that is the point of computing both: nudge w by a
tiny amount and J moves about <b>6</b> units for every one unit w moved; nudge b the same tiny amount
and J only moves about <b>4</b>. This particular hillside is steeper in the w direction than in the b
direction — and the gradient is precisely how you read that off.</p>"""

    + h2("🎬", "Watch it move")
    + demo("fpartial", "Freeze one, wiggle the other",
           "the left panel is the whole landscape; the right is the single slice you are walking along")

    + h2("💻", "In NumPy")
    + code("""
import numpy as np

def J(w, b):
    return w**2 + 2*b**2

def partial(f, w, b, wrt='w', h=1e-5):
    if wrt == 'w':
        return (f(w + h, b) - f(w, b)) / h      # b stays put
    else:
        return (f(w, b + h) - f(w, b)) / h      # w stays put

partial(J, 3.0, 1.0, 'w')     # 6.00001   -> 2w
partial(J, 3.0, 1.0, 'b')     # 4.00002   -> 4b
""")
    + """<p>Look at what “freeze the other one” means in code: it is literally that you do not add h to
it. There is nothing more to the concept than that.</p>"""

    + h2("🔬", "What is actually happening")
    + """<p>The <b>sign</b> of a partial derivative is an instruction, and it is worth reading one out
loud. Say a tiny model has just two parameters and a cost of 10, and you compute:</p>
<p>∂J/∂w₁ = <b>5</b> &nbsp;(positive) &nbsp;·&nbsp; ∂J/∂w₂ = <b>−3</b> &nbsp;(negative)</p>
<p>The positive 5 says “increasing w₁ makes the cost <i>worse</i>” — so to improve, w₁ should go
<b>down</b>. The negative −3 says the opposite: increasing w₂ makes the cost <i>better</i>, so w₂
should go <b>up</b>. Two parameters, two completely different instructions, read straight off the
sign — and neither one required looking at the other.</p>
<p>Collecting all of them into one list is the <b>gradient</b> ∇J, and it has a lovely property: it
points in the direction of <b>steepest uphill</b>. Which is exactly why gradient descent subtracts
it — going the opposite way is the fastest way down.</p>
<p>Scale is the only thing that changes for a real network: it has hundreds of thousands of
parameters, not two, so the gradient is a list hundreds of thousands of numbers long — one sign,
one instruction, per parameter. You could never compute those one at a time by nudging each one and
re-running the model, which is precisely the problem <b>backpropagation</b> solves (Course 2, Week
2). It gets every single one of them in about two passes over the network.</p>"""

    + key("""<p>The ladder, if you want the whole lesson in one line each:</p>
<p><b>Derivative</b> — one input, one slope. <b>Partial derivative</b> — several inputs; freeze all
but one and you are back to an ordinary slope. <b>Gradient</b> — every partial derivative, collected
into one list; it points steepest uphill. <b>Gradient descent</b> — step in the <i>opposite</i>
direction to the gradient, because opposite-of-uphill is downhill.</p>""",
      "The ladder")

    + h2("🕳", "Traps")
    + trap("""<p><b>Forgetting that the other variables are constants.</b> When differentiating with
respect to w, a term like 2b² is a <em>number</em>, and numbers differentiate to zero. It vanishes entirely.</p>""")
    + trap("""<p><b>Reading ∂ as a different operation from d.</b> It is the same operation. The curl is
purely a notice to the reader.</p>""")

    + h2("✅", "Check yourself")
    + quiz([
        ("J(w, b) = 3w + 5b. What is ∂J/∂w?",
         "<p><b>3</b>. The 5b term is constant with respect to w, so it disappears.</p>"),
        ("J(w, b) = w·b. What is ∂J/∂w?",
         "<p><b>b</b>. Treat b as a fixed number — then w·b is just “that number times w”, whose slope "
         "is that number.</p>"),
        ("A parameter's partial derivative comes out negative. Should gradient descent increase it or decrease it?",
         "<p><b>Increase it.</b> A negative partial means increasing that parameter makes the cost go "
         "<i>down</i> — and going down is the whole goal.</p>"),
        ("Why does gradient descent subtract the gradient rather than add it?",
         "<p>Because the gradient points <b>uphill</b>, and you want to go down. The minus sign is the "
         "whole trick.</p>"),
    ])

    + h2("🔗", "Go deeper")
    + links([
        ("video", "https://www.3blue1brown.com/lessons/gradient-descent",
         "3Blue1Brown — Gradient descent",
         "Shows the gradient as an arrow on a landscape. Once you have seen it, ∇ stops being frightening."),
        ("docs", "https://www.khanacademy.org/math/multivariable-calculus/multivariable-derivatives",
         "Khan Academy — multivariable derivatives",
         "The formal treatment, free, if you want more than the intuition."),
    ]))

# ============================================================ 7
lesson("07-sigma-notation", "Σ — summation notation", 9,
    "The scariest-looking symbol in the course, and it is a for loop. Once you can read it, half the "
    "formulas in the specialization become ordinary.",
    pretest("""<p>A formula says <b>Σ</b> with <b>i=1</b> underneath and <b>m</b> on top. <b>Guess what it is telling a computer to do</b> — you have almost certainly written this in code without knowing the symbol.</p>""",
        """<p>Watch for the three questions every Σ answers: where to start, where to stop, and what to do each time. It is a <code>for</code> loop wearing a hat.</p>""")
    + h2("🎈", "The idea, in plain words")
    + kid("""<p>You want to say “add up all of these”. Writing x₁ + x₂ + x₃ + … + x₁₀₀₀ is silly.</p>
<p>So maths has a shorthand: a big Σ, with “where to start” underneath, “where to stop” on top, and “the
thing to add up” beside it.</p>
<p>It is a for loop. That is not an analogy — it is the same instruction, written differently.</p>
<p>Picture a robot on an assembly line: it starts at position 1, picks up item x₁, adds it to a running total, steps to position 2, picks up x₂, adds that in too — and keeps going until it passes position m, at which point it hands you the final total. Σ is the instruction card taped to that robot.</p>""")

    + h2("🔤", "The symbol, and how to say it")
    + eqp([
        ('<span class="big">Σ</span><sub><var>i</var>=1</sub><sup><var>m</var></sup> <var>x</var><sub><var>i</var></sub>',
         "sigma", "add up every xᵢ"),
    ], "“the sum, from i equals 1 to m, of x sub i” — click it")
    + decode([
        ("<span class='big'>Σ</span>", "“sum” (capital sigma)", "the instruction: <b>add up what follows</b>."),
        ("<var>i</var> = 1", "“i starts at one”", "the counter, and where it begins. Underneath."),
        ("<var>m</var>", "“up to m”", "where it stops. On top. Usually the number of examples."),
        ("<var>x<sub>i</sub></var>", "“x sub i”", "the thing being added. The i changes each time round."),
        ("<var>i</var>", "“the index”", "just a counter. j, k and n are equally common — the letter means nothing."),
    ])
    + key("""<p>When you meet Σ in a formula, read it as: <b>“now do this for every training example, and
add up the results.”</b> That single translation unlocks the cost functions in all three courses.</p>""")

    + note("""<p>Every Σ you will ever meet answers the same three questions, in the same three places.
Once you can point to all three, you can unroll it — however unfamiliar what comes after it looks.</p>
<ol style="margin:6px 0 0"><li><b>Where does it start?</b> — look <b>underneath</b> Σ.</li>
<li><b>Where does it stop?</b> — look <b>on top</b> of Σ.</li>
<li><b>What do I do to each one?</b> — look <b>beside</b> Σ, to the right.</li></ol>""",
      "The three questions every Σ answers")

    + h2("🧮", "Worked by hand")
    + """<p>With x = [3, 1, 4, 1, 5]:</p>
<p style="text-align:center"><b>Σ<sub>i=1</sub><sup>5</sup> x<sub>i</sub></b> = 3 + 1 + 4 + 1 + 5 = <b>14</b></p>
<p>And a slightly harder one — the thing after Σ can be any expression:</p>
<p style="text-align:center"><b>Σ<sub>i=1</sub><sup>3</sup> x<sub>i</sub>²</b> = 3² + 1² + 4² = 9 + 1 + 16 = <b>26</b></p>
<p>Notice you square <em>each one first</em>, then add. Not add then square — that would be 8² = 64.</p>"""

    + h2("🎬", "Watch it move")
    + demo("fsigma", "The symbol unrolling into a loop",
           "watch the running total build up one term at a time")

    + h2("💻", "In NumPy")
    + code("""
import numpy as np
x = np.array([3, 1, 4, 1, 5])

# the literal translation
total = 0
for i in range(len(x)):
    total = total + x[i]          # 14

# what you actually write
np.sum(x)                         # 14
x.sum()                           # 14  -- same thing

# Σ x²  -- square each, then add
np.sum(x ** 2)                    # 52

# the machine learning shape: Σ (prediction - truth)²
errors = predictions - y
np.sum(errors ** 2)
""")

    + h2("🔬", "What is actually happening")
    + """<p>Now look at a real cost function and see how little is left once Σ is decoded:</p>"""
    + eqp([
        ('<var>J</var>', "cost-j", "the cost"),
        ' <span class="op">=</span> ',
        ('<span class="frac"><span>1</span><span>2<var>m</var></span></span>', "avg-factor", "the average"),
        ('<span class="big">Σ</span><sub><var>i</var>=1</sub><sup><var>m</var></sup>', "sigma", "for every example"),
        ('( <var>f</var>(<var>x</var><sup>(<var>i</var>)</sup>) − <var>y</var><sup>(<var>i</var>)</sup> )', "error-term", "predicted − actual"),
        ('<sup>2</sup>', "squared-term", "squared"),
    ], "click any part", small=True)
    + """<p>Only one piece of that has not been pulled apart yet: <b>f(x<sup>(i)</sup>) − y<sup>(i)</sup></b>.
That is not a special notation — it is exactly the f(x) from Lesson 1, applied once per example, minus
the correct answer for that same example.</p>"""
    + decode([
        ("<var>x</var><sup>(<var>i</var>)</sup>", "“x superscript i”", "the input for training example number i — one house, one email."),
        ("<var>f</var>(<var>x</var><sup>(<var>i</var>)</sup>)", "“f of x superscript i”", "the model's <b>guess</b> for that example. A number it produced."),
        ("<var>y</var><sup>(<var>i</var>)</sup>", "“y superscript i”", "the <b>correct answer</b> for that example, taken from the data — never guessed."),
        ("<var>f</var>(<var>x</var><sup>(<var>i</var>)</sup>) − <var>y</var><sup>(<var>i</var>)</sup>", "—", "guess minus truth: the <b>error</b> on that one example."),
    ])
    + """<p>Put a number through it. Say a model predicts a house is worth 250 (thousand) and it actually
sold for 280:</p>"""
    + table(["guess f(x⁽ⁱ⁾)", "truth y⁽ⁱ⁾", "f(x⁽ⁱ⁾) − y⁽ⁱ⁾", "what the sign means"],
            [["250", "280", "<b>−30</b>", "negative → guessed too <b>low</b>"],
             ["280", "280", "<b>0</b>", "exactly right"],
             ["300", "280", "<b>+20</b>", "positive → guessed too <b>high</b>"]])
    + """<p>Squaring throws the sign away on purpose — being 30 too low and 30 too high are equally wrong,
and a cost function should not care which direction the mistake went, only how big it was.</p>
<p>Read the whole formula left to right: “take one over two-m, times the sum, for every example from 1 to
m, of (the guess minus the truth) squared”. Which is: <b>for each example work out how wrong you were,
square it, add them all up, and take the average.</b></p>
<p>That is a sentence you could have understood before this lesson. The symbol was the only obstacle.</p>"""
    + note("""<p>Σ has one genuinely useful property: you can pull constants out.
Σ(3x<sub>i</sub>) = 3 Σx<sub>i</sub>. This is why the 1/2m sits <em>outside</em> the sum rather than
inside — same answer, fewer multiplications.</p>""", "One handy rule")

    + h2("🕳", "Traps")
    + trap("""<p><b>Applying an operation after the sum instead of inside it.</b> Σ(x²) squares each term
then adds. (Σx)² adds first then squares. For [1, 2] those are 5 and 9.</p>""")
    + trap("""<p><b>Off-by-one between maths and code.</b> Maths says i = 1 to m. Python says
<code>range(m)</code>, which is 0 to m−1. Same m items, different labels.</p>""")

    + h2("✅", "Check yourself")
    + quiz([
        ("x = [2, 4, 6]. What is Σ x_i?",
         "<p>2 + 4 + 6 = <b>12</b>.</p>"),
        ("Same x. What is Σ (x_i / 2)?",
         "<p>1 + 2 + 3 = <b>6</b>. Halve each one, then add.</p>"),
        ("A model predicts 12 and the true answer is 9. Is f(x) − y positive or negative, and what does that mean?",
         "<p><b>Positive</b> (12 − 9 = 3) — the model guessed too <b>high</b>. A negative result would "
         "mean the opposite: the guess was too low.</p>"),
        ("Translate into English: (1/m) Σ (f(xᵢ) − yᵢ)²",
         "<p>“For every example, take the guess minus the truth, square it, add them all up, and divide "
         "by how many there were.” — the average squared error.</p>"),
    ])

    + h2("🔗", "Go deeper")
    + links([
        ("docs", "https://numpy.org/doc/stable/reference/generated/numpy.sum.html",
         "numpy.sum", "Note the <code>axis</code> argument — you will need it once your data is 2-D."),
    ]))

# ============================================================ 8
lesson("08-pi-notation", "Π — multiplying them all", 6,
    "Sigma's sibling. Same shape, one different instruction — and it explains why anomaly detection works.",
    pretest("""<p>Σ adds things up. <b>Π</b> does the same thing with a different operation. <b>Guess which — and what its running total must start at</b> (Σ starts at 0; starting Π at 0 would be a disaster).</p>""",
        """<p>Ask yourself what ×0 does to any total. Watch for why five mild oddities multiply into one very unlikely event — that is anomaly detection, three courses away.</p>""")
    + h2("🎈", "The idea, in plain words")
    + kid("""<p>Σ says “add them all up”. Π says “<b>multiply</b> them all together”.</p>
<p>That is the entire difference. Same layout, same counter, same start and stop.</p>
<p>Same robot as Σ, but this one’s instruction card says <b>multiply</b> instead of add — and it starts its running total at <b>1</b>, not 0, because multiplying anything by 0 would wipe the whole calculation out before it began.</p>""")

    + h2("🔤", "The symbol, and how to say it")
    + eqp([
        ('<span class="big">Π</span><sub><var>j</var>=1</sub><sup><var>n</var></sup> <var>p</var><sub><var>j</var></sub>',
         "pi-notation", "multiply every pⱼ"),
    ], "“the product, from j equals 1 to n, of p sub j” — click it")
    + decode([
        ("<span class='big'>Π</span>", "“product” (capital pi)", "multiply them all together."),
        ("lowercase <var>π</var>", "“pi”", "the <b>completely different</b> thing: 3.14159. Capital and lowercase are unrelated."),
        ("<var>p<sub>j</sub></var>", "“p sub j”", "the thing being multiplied — usually a probability."),
    ])
    + """<p>Same three questions as Σ, same three places: <b>underneath</b> is where it starts,
<b>on top</b> is where it stops, <b>beside</b> it is what you do to each one — multiply, this time,
instead of add.</p>"""

    + h2("🧮", "Worked by hand")
    + """<p>With p = [0.5, 0.4, 0.6, 0.3]:</p>
<p style="text-align:center">0.5 × 0.4 × 0.6 × 0.3 = <b>0.036</b></p>
<p>Look at what happened. Four perfectly ordinary-looking numbers multiplied down to something under 4%.
Numbers below 1 shrink fast when you multiply them.</p>"""

    + h2("🎬", "Watch it move")
    + demo("fpi", "The running product falling away",
           "four ordinary numbers becoming one small one")

    + h2("💻", "In NumPy")
    + code("""
import numpy as np
p = np.array([0.5, 0.4, 0.6, 0.3])

np.prod(p)              # 0.036

# with many features this UNDERFLOWS to exactly 0.0:
big = np.full(400, 0.5)
np.prod(big)            # 0.0   -- the true answer is about 1e-121

# so real code adds logs instead:
np.sum(np.log(big))     # -277.2   -- perfectly fine
""")

    + h2("🔬", "What is actually happening")
    + """<p>The shrinking is not a nuisance — it is the <b>point</b>, and it is the engine behind anomaly
detection (Course 3, Week 1).</p>
<p>Being slightly unusual on one measurement is common. Being slightly unusual on five measurements
<em>at once</em> is genuinely rare, and multiplying is what turns “five mild oddities” into one very small
number you can threshold on.</p>
<p>The practical catch is in the code above. Multiply enough small numbers and floating point gives up and
returns exactly zero. The standard fix uses a property of logarithms:</p>"""
    + eqp([
        ('log(<var>a</var> × <var>b</var>) = log(<var>a</var>) + log(<var>b</var>)', "logarithm-f0", "turns × into +"),
    ], "so a product of many things becomes a sum of many things — click it", small=True)
    + """<p>Sums do not underflow. This is why you will see <code>np.sum(np.log(...))</code> all over real
machine learning code where the formula on the page says Π.</p>"""

    + h2("🕳", "Traps")
    + trap("""<p><b>Confusing Π with π.</b> Capital = multiply. Lowercase = 3.14159 (or a policy, in
reinforcement learning). Three different meanings, one alphabet.</p>""")

    + h2("✅", "Check yourself")
    + quiz([
        ("p = [0.2, 0.5]. What is Π p_j?",
         "<p>0.2 × 0.5 = <b>0.1</b>.</p>"),
        ("Why does real code compute Σ log(p) instead of Π p?",
         "<p>Because multiplying many small numbers underflows to exactly zero in floating point. Logs "
         "turn the product into a sum, which does not.</p>"),
    ])

    + h2("🔗", "Go deeper")
    + links([
        ("docs", "https://numpy.org/doc/stable/reference/generated/numpy.prod.html",
         "numpy.prod", "And note <code>np.log</code> next to it — you will use them together."),
    ]))

# ============================================================ 9
lesson("09-vectors", "Vectors", 8,
    "A list of numbers. That is it — and almost every object in machine learning is one.",
    pretest("""<p>A house: 1400 sq ft, 3 beds, 2 floors, 18 years old. <b>Is [1400, 3, 2, 18] the same thing as [18, 2, 3, 1400]?</b> Commit to yes or no, and why.</p>""",
        """<p>Watch for the word “ordered”. It sounds trivial and it is the entire difference between a vector and a bag of numbers.</p>""")
    + h2("🎈", "The idea, in plain words")
    + kid("""<p>A vector is a list of numbers kept in order. [3, 2] is a vector. So is [2104, 5, 1, 45] —
the size, bedrooms, floors and age of a house.</p>
<p>With two numbers you can draw it as an arrow: 3 across, 2 up. With four hundred numbers you cannot draw
it at all — and every single formula still works identically.</p><p>A recipe is a vector in disguise: “2 cups flour, 1 egg, 0.5 cups sugar” is just the list [2, 1, 0.5] with labels attached. Swap the order of those three numbers and you have changed the recipe, even though it is the “same” three numbers — which is exactly why a vector’s entries must always stay in a fixed, agreed order.</p>""")

    + h2("🔤", "The symbol, and how to say it")
    + decode([
        ("<var>x⃗</var>", "“x vector”", "the little arrow means “this is a list, not a single number”."),
        ("<b>x</b>", "“bold x”", "the same thing. Printed books use bold; handwriting uses the arrow."),
        ("<var>x</var><sub>2</sub>", "“x sub two”", "the second entry <b>inside</b> the vector — a single number."),
        ("‖<var>x⃗</var>‖", "“the norm of x”", "its <b>length</b>. Double bars, not single."),
        ("scalar", "“SCAY-lar”", "the word for an ordinary single number, as opposed to a vector."),
        ("dimension", "“dimension”", "how many entries it has. A 4-feature house is a 4-dimensional vector."),
    ])
    + key("""<p>In this specialization a vector is almost always <b>one row of your spreadsheet</b> — one
house, one email, one patient. And a <b>matrix</b> is the whole spreadsheet.</p>""")

    + h2("🧮", "Worked by hand")
    + """<p>x⃗ = [3, 4]. Its length is found with Pythagoras — because the arrow is the hypotenuse of a
triangle 3 across and 4 up:</p>
<p style="text-align:center">‖x⃗‖ = √(3² + 4²) = √(9 + 16) = √25 = <b>5</b></p>
<p>The same formula works with four hundred entries; you just square more things before adding them.</p>"""

    + h2("🎬", "Watch it move")
    + demo("fvector", "Two numbers, drawn as an arrow",
           "drag them and watch the components and the length")

    + h2("💻", "In NumPy")
    + code("""
import numpy as np

x = np.array([3, 4])

x.shape              # (2,)      -- 2 entries, one dimension
len(x)               # 2
x[0]                 # 3         -- counting starts at zero
x[-1]                # 4         -- last one

np.linalg.norm(x)    # 5.0       -- the length
x + np.array([1, 1]) # array([4, 5])   -- elementwise
2 * x                # array([6, 8])   -- scales the arrow, same direction
""")

    + h2("🔬", "What is actually happening")
    + """<p>Two operations on vectors matter, and they mean genuinely different things:</p>
<ul>
<li><b>Adding</b> two vectors joins the arrows nose to tail. [3,4] + [1,1] = [4,5].</li>
<li><b>Scaling</b> by a number stretches the arrow without turning it. 2 × [3,4] = [6,8] points exactly
the same way, twice as far.</li>
</ul>
<p>Why the geometry is worth keeping in mind even at 400 dimensions: when Course 3 says two films are
“similar”, it means their vectors point in a similar direction. When Course 2 says a neuron
“detects a pattern”, it means the input vector points the same way as the weight vector. The picture keeps
working long after you can no longer draw it.</p>"""

    + h2("🕳", "Traps")
    + trap("""<p><b>Confusing shape (2,) with (1, 2).</b> The first is a plain list of two numbers; the
second is a matrix with one row. NumPy treats them differently and TensorFlow cares. Covered properly in
the Python lane.</p>""")
    + trap("""<p><b>Using single bars for length.</b> |x| is absolute value (for one number). ‖x‖ with
double bars is the length of a vector.</p>""")

    + h2("✅", "Check yourself")
    + quiz([
        ("What is the length of [6, 8]?",
         "<p>√(36 + 64) = √100 = <b>10</b>.</p>"),
        ("x⃗ = [1, 2, 3]. What is x₂, and what is the dimension?",
         "<p>x₂ = <b>2</b> (the second entry, counting from 1 as maths does). The vector is "
         "<b>3-dimensional</b>.</p>"),
        ("A house has 12 features. What shape is one house as a vector?",
         "<p>A <b>12-dimensional</b> vector — shape <code>(12,)</code>. Impossible to draw, perfectly "
         "ordinary to compute with.</p>"),
    ])

    + h2("🔗", "Go deeper")
    + links([
        ("video", "https://www.3blue1brown.com/lessons/vectors",
         "3Blue1Brown — Vectors, what even are they?",
         "Ten minutes, and the best possible introduction. Watch this one."),
        ("book", "http://immersivemath.com/ila/",
         "Immersive Linear Algebra",
         "Free and fully interactive — drag the vectors around in the diagrams."),
    ]))

# ============================================================ 10
lesson("10-dot-product", "The dot product", 9,
    "Two lists in, one number out. It is what a neuron computes, what a recommender uses to match you to "
    "a film, and what matrix multiplication is made of.",
    pretest("""<p>Shopping list: 1 apple, 2 bananas, 3 cherries. Prices: £4, £5, £6. <b>Work out the bill.</b> Then: how many separate <em>kinds</em> of operation did you just perform?</p>""",
        """<p>You should get £32. Watch for why maths bothers to give that two-step pattern a single name — it turns out to be what every neuron in Course 2 computes.</p>""")
    + h2("🎈", "The idea, in plain words")
    + kid("""<p>A shopping list: 1 apple, 2 bananas, 3 cherries. A price list: apples £4, bananas £5,
cherries £6.</p>
<p>The total bill? Pair each item with its price, multiply, add it all up:
1×4 + 2×5 + 3×6 = 4 + 10 + 18 = <b>£32</b>.</p>
<p>That is a dot product. Two lists go in; one number comes out.</p>
<p>Notice you just did two different things back to back — multiplying, then adding — and gave that whole two-step combination a single name, “dot”. Whenever maths bothers to name a repeated pattern of steps, it is because that exact pattern turns out to matter enormously later. This one does, everywhere in the specialization.</p>""")

    + h2("🔤", "The symbol, and how to say it")
    + eqp([
        ('<var>a⃗</var> <span class="op">·</span> <var>b⃗</var>', "dot-product-f0", "multiply matching entries, add them up"),
        ' <span class="op">=</span> ',
        ('<span class="big">Σ</span><sub><var>i</var></sub> <var>a<sub>i</sub>b<sub>i</sub></var>', "sigma", "one term per pair"),
        ' <span class="op">=</span> <var>a</var><sub>1</sub><var>b</var><sub>1</sub> + <var>a</var><sub>2</sub><var>b</var><sub>2</sub> + … + <var>a<sub>n</sub>b<sub>n</sub></var>',
    ], "“a dot b” — click a part")
    + decode([
        ("·", "“dot”", "the dot product. <b>Not</b> ordinary multiplication — it includes the adding up."),
        ("<var>a</var><sup>T</sup><var>b</var>", "“a transpose b”", "the same thing, written the matrix way. You will see both."),
        ("⟨<var>a</var>, <var>b</var>⟩", "“the inner product”", "again the same thing, in more mathematical writing."),
        ("|<var>a</var>||<var>b</var>| cos θ", "“a b cos theta”", "the geometric form — length times length times how aligned they are."),
    ])
    + key("""<p>A dot product <b>collapses</b> two lists into a single number. That collapse is exactly why
a neuron uses one: many inputs arrive, and exactly one number must come out.</p>""")

    + h2("🧮", "Worked by hand")
    + table(["step", "working", "running total"],
            [["pair 1", "1 × 4 = 4", "4"],
             ["pair 2", "2 × 5 = 10", "14"],
             ["pair 3", "3 × 6 = 18", "<b>32</b>"]])
    + """<p>Both lists must be the <b>same length</b>, or there is nothing to pair the leftovers with.
That is not a convention — it is the reason NumPy raises an error.</p>"""

    + h2("🎬", "Watch it move")
    + demo("fdot", "Pair, multiply, add — and what the answer means geometrically",
           "drag the angle and watch the sign of the answer flip")

    + h2("💻", "In NumPy")
    + code("""
import numpy as np
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

np.dot(a, b)        # 32
a @ b               # 32   -- the modern shorthand, preferred
(a * b).sum()       # 32   -- the long way, showing what it does

a * b               # array([ 4, 10, 18])   <- NOT a dot product!
""")
    + warn("""<p>That last line is the mistake to watch for. <code>a * b</code> multiplies elementwise and
gives you back a <b>list</b>. <code>a @ b</code> multiplies <em>and adds</em> and gives you a
<b>number</b>. Both run without error; only one is what the formula meant.</p>""")

    + h2("🔬", "What is actually happening")
    + """<p>The geometric form is where the intuition lives:</p>"""
    + eqp([
        ('<var>a⃗</var> · <var>b⃗</var>', "dot-product-f0", "multiply matching entries, add them up"),
        ' = |<var>a⃗</var>| |<var>b⃗</var>| ',
        ('cos <var>θ</var>', "cos", "how aligned the two directions are"),
    ], "click a part", small=True)
    + table(["The two arrows", "cos θ", "The dot product"],
            [["point the same way", "1", "<b>large positive</b>"],
             ["at a slight angle", "0.7", "smaller positive"],
             ["at right angles", "0", "<b>exactly zero</b>"],
             ["point opposite ways", "−1", "<b>large negative</b>"]])
    + """<p>So a dot product measures <b>how much two things agree</b>. Read a neuron's z = w⃗·x⃗ + b that
way and it stops being arithmetic: the neuron is asking “how much does this input look like the pattern
stored in my weights?”</p>
<p>The same reading explains Course 3's recommender: v<sub>u</sub>·v<sub>m</sub> is asking how much your
taste vector agrees with the film's vector. Big number, good match.</p>"""

    + h2("🕳", "Traps")
    + trap("""<p><b>Different lengths.</b> <code>ValueError: shapes (3,) and (4,) not aligned</code> is
NumPy saying there is nothing to pair the fourth element with.</p>""")
    + trap("""<p><b>Using np.dot on 2-D arrays and expecting matrix multiply.</b> It works for 2-D, but
behaves differently in higher dimensions. Use <code>@</code> or <code>np.matmul</code> for matrices and
keep <code>np.dot</code> for vectors.</p>""")

    + h2("✅", "Check yourself")
    + quiz([
        ("Compute [2, 0, −1] · [3, 5, 4].",
         "<p>2×3 + 0×5 + (−1)×4 = 6 + 0 − 4 = <b>2</b>.</p>"),
        ("Two vectors have a dot product of 0. What does that mean geometrically?",
         "<p>They are at <b>right angles</b> — completely unrelated directions. A neuron whose weights "
         "are perpendicular to its input outputs just z = b, ignoring the input entirely.</p>"),
        ("Why does a neuron need a dot product rather than a * b?",
         "<p>Because it must produce one number, z. Elementwise multiplication would leave a whole list.</p>"),
    ])

    + h2("🔗", "Go deeper")
    + links([
        ("video", "https://www.3blue1brown.com/lessons/dot-products",
         "3Blue1Brown — Dot products and duality",
         "The geometric meaning done properly. Genuinely worth fourteen minutes."),
    ]))

# ============================================================ 11
lesson("11-matrices", "Matrices and shapes", 8,
    "A grid of numbers — and the shape tuple that causes more beginner errors than anything else in "
    "machine learning.",
    pretest("""<p>You have 100 houses, each with 4 measurements. <b>Someone says “the shape is (100, 4)”. Which number is which — and how would you know if you had it backwards?</b></p>""",
        """<p>Watch for the convention: rows first, always. Getting this backwards is the single most common source of errors in the labs.</p>""")
    + h2("🎈", "The idea, in plain words")
    + kid("""<p>A matrix is a spreadsheet. Rows going across, columns going down, numbers in the boxes.</p>
<p>Its <b>shape</b> is how many rows and how many columns — written (rows, columns), in that order,
always.</p>
<p>Say row 3 of the sheet is one house: 1500 (square feet), 3 (bedrooms), 2 (floors). Column 2 running down the whole sheet is every house’s bedroom count at once. “Row 3, column 2” — a single cell — is just that one house’s bedroom count: 3.</p>""")

    + h2("🔤", "The symbol, and how to say it")
    + decode([
        ("<var>M</var>", "“capital M”", "matrices get capital letters. Vectors get lowercase. A useful reading aid."),
        ("(3, 4)", "“three by four”", "3 rows, 4 columns. <b>Rows first.</b>"),
        ("<var>M</var><sub><var>ij</var></sub>", "“M i j”", "the entry in row i, column j. Row first again."),
        ("<var>M</var>[1, 2]", "“M one two”", "the code version — and it counts from <b>zero</b>."),
        ("<var>M</var>[:, 2]", "“M, all rows, column two”", "the colon means “everything in this direction”."),
    ])
    + key("""<p>In machine learning, almost always: <b>rows are your examples, columns are your
features</b>. So a (1000, 4) matrix is 1000 houses, each described by 4 numbers.</p>""")

    + h2("🧮", "Worked by hand")
    + """<p>M = [[11, 12, 13, 14], [21, 22, 23, 24], [31, 32, 33, 34]]</p>
<ul>
<li>Shape: <b>(3, 4)</b> — three rows, four columns.</li>
<li>M[0, 0] = <b>11</b> (top-left).</li>
<li>M[2, 1] = <b>32</b> (third row, second column — counting from zero).</li>
<li>M[1] = <b>[21, 22, 23, 24]</b> — a whole row.</li>
<li>M[:, 1] = <b>[12, 22, 32]</b> — a whole column.</li>
</ul>"""

    + h2("🎬", "Watch it move")
    + demo("fmatrix", "Change the shape, watch the indices",
           "the highlighted cell shows its own address")

    + h2("💻", "In NumPy")
    + code("""
import numpy as np
M = np.array([[11, 12, 13, 14],
              [21, 22, 23, 24],
              [31, 32, 33, 34]])

M.shape          # (3, 4)
M.shape[0]       # 3   -- rows     (often m, the number of examples)
M.shape[1]       # 4   -- columns  (often n, the number of features)
M.ndim           # 2   -- it is 2-dimensional
M.size           # 12  -- total numbers

M[2, 1]          # 32
M[1]             # array([21, 22, 23, 24])   a row
M[:, 1]          # array([12, 22, 32])       a column
""")

    + h2("🔬", "What is actually happening")
    + """<p>A matrix is not really a grid in memory — it is one long line of 12 numbers, plus a note saying
“read this as 3 rows of 4”. That note is the shape.</p>
<p>This explains two things that otherwise look like magic. <b>reshape</b> is nearly free, because nothing
moves — only the note changes. And <b>transpose</b> can also be free, because NumPy can just record “read
this the other way round” instead of copying anything.</p>
<p>It also explains why shape errors are so common: the numbers are fine, the note is wrong, and nothing
looks visibly broken until an operation refuses to line up.</p>"""
    + note("""<p><b>Print <code>.shape</code> constantly while you are learning.</b> It is free, it takes
one line, and it answers most of the questions you will actually have.</p>""", "The single best habit")

    + h2("🕳", "Traps")
    + trap("""<p><b>Reading shape as (columns, rows).</b> It is always rows first. A (2, 5) matrix is short
and wide, not tall and thin.</p>""")
    + trap("""<p><b>Maths counts from 1, code counts from 0.</b> M<sub>11</sub> in a textbook is
<code>M[0, 0]</code> in NumPy. Both conventions appear in this specialization.</p>""")

    + h2("✅", "Check yourself")
    + quiz([
        ("You have 500 emails, each described by 10,000 word counts. What shape is X?",
         "<p><b>(500, 10000)</b> — 500 rows (examples) by 10,000 columns (features).</p>"),
        ("What does M[:, 0] give you?",
         "<p>The <b>first column</b>, as a 1-D array. The colon means “all rows”.</p>"),
        ("M.shape is (3, 4). What is M.shape[1]?",
         "<p><b>4</b> — the number of columns. shape[0] would be 3, the rows.</p>"),
    ])

    + h2("🔗", "Go deeper")
    + links([
        ("docs", "https://numpy.org/doc/stable/user/basics.indexing.html",
         "NumPy — indexing basics",
         "The colon syntax in full. Ten minutes here pays off in every notebook you will ever open."),
    ]))

# ============================================================ 12
lesson("12-matrix-multiplication", "Matrix multiplication", 10,
    "A whole grid of dot products, computed at once. And the shape rule that tells you instantly whether "
    "two matrices can meet.",
    pretest("""<p>You multiply a (2×3) by a (3×4). <b>Guess the shape of the answer — and guess what happens if you try (2×3) times (2×3).</b></p>""",
        """<p>Watch the two inner numbers. Watch for what they do — they must match, and then they vanish.</p>""")
    + h2("🎈", "The idea, in plain words")
    + kid("""<p>One dot product prices up one shopping basket.</p>
<p>Now imagine <b>three</b> customers with three baskets, and <b>four</b> shops with four price lists.
How much does each customer pay at each shop? That is 3 × 4 = 12 totals, and you can lay them out in a
grid.</p>
<p>That grid is a matrix multiplication. Every cell in it is one ordinary dot product — one row meeting
one column.</p>
<p>Nobody needs a new kind of arithmetic for those twelve totals. Each one is just an ordinary “multiply and add” shopping bill, done twelve times and arranged in a grid. Matrix multiplication does not introduce new arithmetic — it only organises arithmetic you already know.</p>""")

    + h2("🔤", "The symbol, and how to say it")
    + eqp([
        ('(<var>m</var> × <var class="hl-a"><var>n</var></var>) × (<var class="hl-a"><var>n</var></var> × <var>p</var>)',
         "matmul-f0", "inner numbers must match"),
        ' <span class="op">=</span> (<var>m</var> × <var>p</var>)',
    ], "the shape rule — the inner numbers must match, and they vanish — click it")
    + decode([
        ("<var>A</var><var>B</var>", "“A B”", "matrix multiplication. Often written with no symbol at all between them."),
        ("<var>A</var> @ <var>B</var>", "“A at B”", "the Python operator for it."),
        ("the inner numbers", "—", "the two in the middle. They must be <b>equal</b>, and they get summed away."),
        ("the outer numbers", "—", "the two on the ends. They become the shape of your answer."),
    ])
    + key("""<p><b>The trick:</b> write the shapes side by side — (3×<b>2</b>)(<b>2</b>×4). Middles match →
legal. The answer is the outer two → (3×4). This one habit prevents most shape errors in the whole
specialization.</p>""")

    + h2("🧮", "Worked by hand")
    + """<p>A is (3×2), B is (2×3). The cell in row 1, column 1 of the answer is row 1 of A dotted with
column 1 of B:</p>
<p style="text-align:center">[1, 2] · [7, 10] = 1×7 + 2×10 = <b>27</b></p>
<p>Then row 1 with column 2, row 1 with column 3, then move to row 2. Nine cells, nine dot products.</p>"""
    + table(["Expression", "Shapes", "Legal?", "Result"],
            [["A @ B", "(3×2)(2×3)", "✅ inner 2 = 2", "(3×3)"],
             ["B @ A", "(2×3)(3×2)", "✅ inner 3 = 3", "(2×2) — a <b>different</b> answer"],
             ["A @ A", "(3×2)(3×2)", "❌ 2 ≠ 3", "ValueError"],
             ["A @ A.T", "(3×2)(2×3)", "✅ inner 2 = 2", "(3×3)"]])

    + h2("🎬", "Watch it move")
    + demo("fmatmul", "The answer filling in, one cell at a time",
           "watch which row and which column feed each cell")

    + h2("💻", "In NumPy")
    + code("""
import numpy as np
A = np.array([[1, 2], [3, 4], [5, 6]])       # (3, 2)
B = np.array([[7, 8, 9], [10, 11, 12]])      # (2, 3)

A @ B                # (3, 3)  -- the preferred spelling
np.matmul(A, B)      # identical

A * B                # ValueError -- elementwise needs matching shapes
B @ A                # (2, 2)  -- legal, and a completely different answer
""")
    + warn("""<p><code>*</code> is elementwise; <code>@</code> is matrix multiplication. When the shapes
happen to allow both, <code>*</code> will run silently and give you numbers that are wrong. This is one of
the most expensive typos in machine learning.</p>""")

    + h2("🔬", "What is actually happening")
    + """<p>Put your examples in the rows of A and your neurons in the columns of W, and look at what one
multiplication does:</p>"""
    + eqp([
        ('<var>A</var> (<var>m</var> examples × <var>n</var> features)', "matrix-f0", "one row per example"),
        ' × ',
        ('<var>W</var> (<var>n</var> features × <var>p</var> neurons)', "matrix-f0", "one column per neuron"),
        ' = <var>Z</var> (<var>m</var> examples × <var>p</var> neurons)',
    ], "click a part", small=True)
    + """<p>Cell Z[i, j] is “example i, as judged by neuron j”. The features dimension n gets summed away —
which is exactly the weighted sum a neuron performs.</p>
<p>So one matrix multiply runs <b>every example through every neuron simultaneously</b>. That is not an
analogy for what a neural network layer does; it <em>is</em> what a layer does. Course 2, Week 1 arrives at
this equation and it will already be familiar.</p>
<p>Order matters and is not negotiable: AB and BA are different operations, and usually only one is even
defined. Matrix multiplication is <b>not commutative</b>.</p>"""

    + h2("🕳", "Traps")
    + trap("""<p><b>Swapping the operands to “fix” a shape error.</b> If the shapes do not match, one of
your matrices is probably built the wrong way round. Swapping hides the problem rather than fixing it —
check what your rows and columns are supposed to <em>mean</em> first.</p>""")

    + h2("✅", "Check yourself")
    + quiz([
        ("(64 × 400) @ (400 × 25) — legal? What comes out?",
         "<p>Legal, inner 400s match. Result <b>(64 × 25)</b>: 64 examples, 25 neurons.</p>"),
        ("X is (1000, 400) and W is (25, 400). How do you multiply them?",
         "<p><code>X @ W.T</code> → (1000,400)(400,25) = <b>(1000, 25)</b>. W was stored transposed.</p>"),
        ("What happened to the inner dimension?",
         "<p>It was <b>summed away</b>. Each output cell is a sum over all n pairings, so n never appears "
         "in the result shape.</p>"),
    ])

    + h2("🔗", "Go deeper")
    + links([
        ("video", "https://www.3blue1brown.com/lessons/matrix-multiplication",
         "3Blue1Brown — Matrix multiplication as composition",
         "Matrix multiply as “do this transformation, then that one”. This is what stops it feeling arbitrary."),
        ("play", "http://matrixmultiplication.xyz/",
         "matrixmultiplication.xyz",
         "Type in two matrices and watch the rows slide across the columns. Silly, and effective."),
    ]))

# ============================================================ 13
lesson("13-transpose", "Transpose", 6,
    "Tipping a matrix on its side. Not a deep idea — but you will reach for it constantly, and knowing "
    "why saves a lot of confusion.",
    pretest("""<p>A table has students down the side and exams across the top. Your code needs it the other way round. <b>Has any information changed?</b></p>""",
        """<p>Watch for how little is really happening. It is shape plumbing, not mathematics — but you will type <code>.T</code> constantly, so it is worth being bored by it now.</p>""")
    + h2("🎈", "The idea, in plain words")
    + kid("""<p>Take your spreadsheet and tip it over. What were rows are now columns; what were columns
are now rows.</p>
<p>The numbers do not change. Nothing is calculated. Only where each number <em>sits</em> changes.</p>
<p>Say row 2 of the sheet held Bob’s exam scores, 70 and 85, before tipping it over. After tipping, those same two numbers, in the same order, become column 2 instead — running downward now rather than across.</p>""")

    + h2("🔤", "The symbol, and how to say it")
    + decode([
        ("<var>M</var><sup>T</sup>", "“M transpose”", "the maths notation — a raised capital T."),
        ("<code>M.T</code>", "“M dot tee”", "the NumPy version. Identical meaning."),
        ("(2, 3) → (3, 2)", "—", "transposing always swaps the shape numbers round."),
        ("<var>a</var><sup>T</sup><var>b</var>", "“a transpose b”", "a dot product, written the matrix way — you saw this two lessons ago."),
    ])

    + h2("🧮", "Worked by hand")
    + """<p>M = [[1, 2, 3], [4, 5, 6]] with shape (2, 3).</p>
<p>M<sup>T</sup> = [[1, 4], [2, 5], [3, 6]] with shape (3, 2).</p>
<p>Follow one number: the 6 was at row 1, column 2. It is now at row 2, column 1. Every entry does the
same swap — M<sup>T</sup>[j, i] = M[i, j].</p>"""

    + h2("🎬", "Watch it move")
    + demo("ftranspose", "The grid tipping over",
           "watch each number travel to its mirrored position")

    + h2("💻", "In NumPy")
    + code("""
import numpy as np
M = np.array([[1, 2, 3], [4, 5, 6]])

M.shape        # (2, 3)
M.T            # array([[1, 4], [2, 5], [3, 6]])
M.T.shape      # (3, 2)
M.T.T          # back to M -- transposing twice does nothing

# the usual reason you need it:
X = np.random.rand(100, 4)     # 100 examples, 4 features
W = np.random.rand(25, 4)      # 25 neurons, 4 weights each
X @ W       # ValueError: 4 and 25 do not match
X @ W.T     # (100, 4) @ (4, 25) -> (100, 25)   works
""")

    + h2("🔬", "What is actually happening")
    + """<p>Nothing moves in memory. NumPy stores one long line of numbers plus a note saying how to walk
through them; transposing just changes the walking instructions. This is why <code>.T</code> is instant
even on a huge array — it is a <b>view</b>, not a copy.</p>
<p>Practically, transpose exists in your code for one boring reason: <b>making shapes line up</b>. You have
a (2,3) and you need a (3,2) so a multiplication is defined. That is nearly always the entire story.</p>
<p>The one thing worth internalising: transpose is <b>not</b> the same as reshape. Reshape re-cuts the
same sequence of numbers into a different grid. Transpose genuinely mirrors positions. For a (2,3) both
give you something of shape (3,2) — and the two results are different.</p>"""

    + h2("🕳", "Traps")
    + trap("""<p><b>Using transpose when you meant reshape, or the reverse.</b> They can produce the same
shape and different numbers, so nothing errors and the answer is quietly wrong.</p>""")
    + trap("""<p><b>Transposing a 1-D array.</b> <code>np.array([1,2,3]).T</code> does <em>nothing</em> —
a (3,) has no second dimension to swap with. You need <code>.reshape(-1, 1)</code> to get a column.</p>""")

    + h2("✅", "Check yourself")
    + quiz([
        ("A is (5, 3). What shape is A.T?",
         "<p><b>(3, 5)</b>. Transposing always swaps the two numbers.</p>"),
        ("X is (100, 4), W is (25, 4). Write the multiplication that works.",
         "<p><code>X @ W.T</code> — (100,4) meeting (4,25) gives <b>(100, 25)</b>.</p>"),
        ("What does M.T.T give you?",
         "<p><b>M</b> again. Transposing twice returns you to where you started.</p>"),
    ])

    + h2("🔗", "Go deeper")
    + links([
        ("docs", "https://numpy.org/doc/stable/reference/generated/numpy.transpose.html",
         "numpy.transpose", "Including what it does for arrays with more than two dimensions."),
    ]))

# ============================================================ 14
lesson("14-exponentials", "Exponentials and e", 8,
    "Why a number beginning 2.718 turns up in the sigmoid, in softmax, and in every probability formula "
    "in the specialization.",
    pretest("""<p>A rumour doubles every hour. After 10 hours, <b>roughly how many people know it if one person started?</b> Guess before calculating — most people guess far too low.</p>""",
        """<p>The answer is 1024. Watch for the shape of the curve that produces it, and for why this specific behaviour is what the sigmoid is built from.</p>""")
    + h2("🎈", "The idea, in plain words")
    + kid("""<p>e is just a number, like π. It is about <b>2.718</b>. Nobody is asking you to work it out.</p>
<p>“e to the power of z”, written e<sup>z</sup>, does two useful things: it is <b>always positive</b>, no
matter what z is, and it <b>grows very fast</b> as z gets bigger.</p>
<p>Those two properties are the entire reason it appears everywhere in this course.</p><p>Bacteria in a dish do this: each one splits into two, then each of <em>those</em> splits into two, and so on. The population does not creep up steadily — it explodes, doubling and doubling again. e<sup>z</sup> is the smooth, continuous version of exactly that runaway growth.</p>""")

    + h2("🔤", "The symbol, and how to say it")
    + decode([
        ("<var>e</var>", "“ee”", "a fixed number ≈ 2.71828. Sometimes called Euler's number."),
        ("<var>e</var><sup><var>z</var></sup>", "“e to the z”", "e multiplied by itself z times. Also written exp(z)."),
        ("exp(<var>z</var>)", "“exp of z”", "the same thing. What code calls it, because superscripts are hard to type."),
        ("<var>e</var><sup>0</sup>", "“e to the zero”", "<b>= 1</b>. Anything to the power zero is 1."),
        ("<var>e</var><sup>−<var>z</var></sup>", "“e to the minus z”", "= 1 / e<sup>z</sup>. Tiny when z is big."),
    ])

    + h2("🧮", "Worked by hand")
    + table(["z", "e^z", "what to notice"],
            [["−10", "0.000045", "very negative → almost zero, but never quite"],
             ["−1", "0.368", ""],
             ["0", "<b>1</b>", "always, for any base"],
             ["1", "2.718", "e itself"],
             ["10", "22,026", "very positive → enormous"]])
    + """<p>Never zero, never negative, and it climbs faster than anything polynomial. Those are the facts
that matter.</p>"""

    + h2("🎬", "Watch it move")
    + demo("fexp", "The curve, and the numbers at each point",
           "notice it never touches the bottom, however far left you go")

    + h2("💻", "In NumPy")
    + code("""
import numpy as np

np.exp(0)          # 1.0
np.exp(1)          # 2.718281828...
np.e               # 2.718281828...   the constant itself

z = np.array([-2, 0, 2])
np.exp(z)          # array([0.135, 1.   , 7.389])   -- works on whole arrays

# the sigmoid, which is just this:
def sigmoid(z):
    return 1 / (1 + np.exp(-z))
""")
    + warn("""<p><code>np.exp(1000)</code> gives <code>inf</code> — the answer is too big for the computer
to hold. This is <b>overflow</b>, and it is exactly the problem that softmax has to work around in Course
2, Week 2 by subtracting the largest value first.</p>""")

    + h2("🔬", "What is actually happening")
    + """<p>Two questions worth answering.</p>
<p><b>Why exponentials in softmax?</b> Because you need to turn scores that might be negative into
positive numbers before you can call them probabilities. e<sup>z</sup> is always positive, and it preserves
the ordering — bigger score in, bigger number out. Nothing else needs to be true.</p>
<p><b>Why e specifically, and not 2 or 10?</b> Because e is the one base whose curve has slope exactly
equal to its own height. The derivative of e<sup>x</sup> is e<sup>x</sup> — itself. That single property
makes every derivative in this specialization come out clean instead of dragging an awkward constant
along. It is a convenience, chosen once, everywhere.</p>"""

    + h2("🕳", "Traps")
    + trap("""<p><b>Confusing e<sup>x</sup> with x<sup>e</sup>.</b> The first has the variable in the
exponent and explodes. The second is an ordinary power.</p>""")
    + trap("""<p><b>Overflow.</b> exp of anything past about 700 is <code>inf</code> in float64, and past
about 88 in float32. Real libraries subtract the maximum first to avoid it.</p>""")

    + h2("✅", "Check yourself")
    + quiz([
        ("What is e^0?",
         "<p><b>1</b>. Anything raised to the power zero is 1 — which is why sigmoid(0) = 1/(1+1) = 0.5.</p>"),
        ("Can e^z ever be negative?",
         "<p><b>No</b>, never. It approaches zero for very negative z but never reaches or crosses it. "
         "That is exactly why softmax uses it.</p>"),
        ("Why is e used rather than 10?",
         "<p>Because the derivative of e^x is e^x itself. Any other base drags an extra constant through "
         "every calculation.</p>"),
    ])

    + h2("🔗", "Go deeper")
    + links([
        ("video", "https://www.3blue1brown.com/lessons/eulers-number",
         "3Blue1Brown — What's so special about e?",
         "Answers the “why e” question properly and visually."),
    ]))

# ============================================================ 15
lesson("15-logarithms", "Logarithms", 8,
    "The undo button for exponentials — and the reason a confidently wrong prediction costs a model so "
    "much.",
    pretest("""<p>Exponentials ask “what does this power give me?”. <b>Guess the opposite question</b> — and what it would be useful for if a probability came out as 0.001.</p>""",
        """<p>log(0.001) is about −6.9. Watch for why turning a tiny fiddly number into a comfortable large one is exactly what a loss function needs.</p>""")
    + h2("🎈", "The idea, in plain words")
    + kid("""<p>Exponentials ask: “I have e, raised to the power 3 — what number is that?”</p>
<p>Logarithms ask the <b>opposite</b>: “I have the number 20 — what power did I raise e to, to get it?”</p>
<p>They undo each other, the way ÷2 undoes ×2.</p><p>Say a rumour doubles the number of people who have heard it every hour. Ask “how many people have heard it now” and exponentials answer that. Ask the opposite — “it has reached this many people, so how many hours has it been spreading?” — and you need the undo-button question a logarithm asks: doubling this many times gets me to that number; how many times was it?</p>""")

    + h2("🔤", "The symbol, and how to say it")
    + eqp([
        ('<var>e</var><sup><var>x</var></sup> = <var>y</var>', "exponential-f0", "raise e to a power"),
        ' &nbsp;&nbsp;↔&nbsp;&nbsp; ',
        ('log(<var>y</var>) = <var>x</var>', "logarithm-f0", "the undo button"),
    ], "these two say exactly the same thing — click either")
    + decode([
        ("log", "“log”", "in machine learning, <b>always the natural log</b> (base e) unless it says otherwise."),
        ("ln", "“ell-en” or “natural log”", "the same thing. Older texts and calculators use ln."),
        ("log<sub>2</sub>", "“log base two”", "used for entropy, so the answer comes out in “bits”."),
        ("log<sub>10</sub>", "“log base ten”", "used for decibels and pH. Rare here."),
        ("−log(<var>p</var>)", "“minus log p”", "the shape used for loss: small p → big penalty."),
    ])

    + h2("🧮", "Worked by hand")
    + table(["p", "−log(p)", "read as"],
            [["1.0", "<b>0</b>", "certain and right → no penalty at all"],
             ["0.5", "0.69", "a coin flip → a moderate penalty"],
             ["0.1", "2.30", "wrong → expensive"],
             ["0.01", "4.61", "confidently wrong → very expensive"],
             ["0.001", "6.91", "and it keeps climbing"],
             ["→ 0", "→ ∞", "certain and wrong → infinite penalty"]])
    + """<p>That table <em>is</em> the logistic loss from Course 1, Week 3. Nothing else is going on.</p>"""

    + h2("🎬", "Watch it move")
    + demo("flog", "Drag p towards zero and watch the penalty climb",
           "the curve is the whole of cross-entropy loss")

    + h2("💻", "In NumPy")
    + code("""
import numpy as np

np.log(1)          # 0.0
np.log(np.e)       # 1.0
np.log(0.5)        # -0.693
-np.log(0.5)       # 0.693     <- the loss for a coin-flip prediction

np.log2(8)         # 3.0       base 2  (entropy uses this)
np.log10(1000)     # 3.0       base 10

np.log(0)          # -inf  + a RuntimeWarning
""")
    + warn("""<p><code>np.log(0)</code> is <code>-inf</code>, and it will poison every number downstream.
This is exactly why Course 2 Week 2 introduces <code>from_logits=True</code> — it rearranges the formula so
a probability of zero is never actually built.</p>""")

    + h2("🔬", "What is actually happening")
    + """<p>Logs do two distinct jobs in this specialization, and it is worth separating them.</p>
<p><b>Job one: turn tiny into huge.</b> A probability of 0.001 is hard to reason about; −log of it is 6.9,
a comfortable number that grows steadily as things get worse. This is what makes cross-entropy a usable
loss function.</p>
<p><b>Job two: turn multiplying into adding.</b></p>"""
    + eqp([
        ('log(<var>a</var> × <var>b</var>) = log(<var>a</var>) + log(<var>b</var>)', "logarithm-f0", "turns × into +"),
    ], "click it", small=True)
    + """<p>Multiply four hundred probabilities together and floating point gives you zero. Add four hundred
logs and you get a perfectly ordinary number. This is why anomaly detection code computes
<code>np.sum(np.log(p))</code> where the formula on the page shows a Π.</p>
<p>Both jobs come from the same fact: logs compress enormous ranges into manageable ones.</p>"""

    + h2("🕳", "Traps")
    + trap("""<p><b>Assuming log means base 10.</b> Calculators and school maths often do. Machine learning
almost always means base e. Check when it matters — for entropy it very much does.</p>""")
    + trap("""<p><b>log of zero or a negative number.</b> Undefined. Real code clips probabilities into
something like [1e−15, 1 − 1e−15] first.</p>""")

    + h2("✅", "Check yourself")
    + quiz([
        ("What is log(1), and why does that matter for loss functions?",
         "<p><b>0</b>. So a perfectly confident, correct prediction costs exactly nothing — which is "
         "precisely the behaviour you want.</p>"),
        ("Why does anomaly detection code add logs instead of multiplying probabilities?",
         "<p>Because multiplying hundreds of small numbers underflows to exactly 0. log turns the product "
         "into a sum, which is numerically safe.</p>"),
        ("−log(0.01) ≈ 4.6 and −log(0.1) ≈ 2.3. What does that pattern tell you?",
         "<p>Each tenfold drop in probability adds about 2.3 to the penalty. The cost of being wrong "
         "grows steadily rather than exploding all at once — until you get very close to zero.</p>"),
    ])

    + h2("🔗", "Go deeper")
    + links([
        ("video", "https://www.khanacademy.org/math/algebra2/x2ec2f6f830c9fb89:logs",
         "Khan Academy — Logarithms",
         "From the beginning, with practice. Worth an hour if logs are genuinely new."),
    ]))

# ============================================================ 16
lesson("16-probability", "Probability basics", 8,
    "Four rules. They cover every probability statement in the specialization, including the one that "
    "makes anomaly detection work.",
    pretest("""<p>A model outputs <b>0.7</b> for “this email is spam”. <b>What must the other possibility be — and what does that tell you about how all the outputs relate?</b></p>""",
        """<p>Watch for the rule about what everything must add to. It is one sentence and it constrains every classifier you will build.</p>""")
    + h2("🎈", "The idea, in plain words")
    + kid("""<p>A probability is a number between <b>0</b> (never happens) and <b>1</b> (always happens).
0.5 means a coin flip.</p>
<p>Three balls out of ten are red, so the chance of pulling a red one is 3/10 = 0.3. That is the whole
definition: how many ways it can happen, divided by how many things could happen.</p>
<p>Every probability question, however it is dressed up, is secretly this same question: out of everything that could happen, what fraction of it is the thing being asked about?</p>""")

    + h2("🔤", "The symbol, and how to say it")
    + decode([
        ("<var>P</var>(<var>A</var>)", "“P of A”", "the probability that A happens. Always between 0 and 1."),
        ("<var>P</var>(not <var>A</var>)", "“P of not A”", "= 1 − P(A). The two must add to 1."),
        ("<var>P</var>(<var>A</var> and <var>B</var>)", "“A and B”", "both happen. For independent things, <b>multiply</b>."),
        ("<var>P</var>(<var>A</var> or <var>B</var>)", "“A or B”", "either happens. For things that cannot both occur, <b>add</b>."),
        ("<var>P</var>(<var>y</var>=1 | <var>x</var>)", "“P of y equals 1, <b>given</b> x”", "the vertical bar means “given that we saw”. Conditional probability."),
        ("independent", "“in-de-PEN-dent”", "one does not affect the other. Two coin flips are; two cards from one deck are not."),
    ])
    + key("""<p><b>AND → multiply. OR → add.</b> That single line covers most of what you need, and the
multiplying one is doing the real work in this specialization.</p>""")

    + h2("🧮", "Worked by hand")
    + """<p>A bag of 10 balls, 3 red and 7 blue.</p>
<ul>
<li>P(red) = 3/10 = <b>0.3</b></li>
<li>P(not red) = 1 − 0.3 = <b>0.7</b> — they must add to 1</li>
<li>P(red, then red again with replacement) = 0.3 × 0.3 = <b>0.09</b></li>
<li>P(red or blue) = 0.3 + 0.7 = <b>1.0</b> — it must be one of them</li>
</ul>
<p>Now notice the third one. Two events that each looked reasonably likely combine into something under
10%. Multiply five such things and you are at 0.00243.</p>"""

    + h2("🎬", "Watch it move")
    + demo("fprob", "A bag of ten, and the four rules",
           "change how many are red and watch every number update")

    + h2("💻", "In NumPy")
    + code("""
import numpy as np

# probability estimated from data = just a mean of True/False
y = np.array([1, 0, 1, 1, 0, 0, 0, 1, 0, 0])
p = y.mean()                    # 0.4  -- 4 out of 10 are 1

# independent events: multiply
np.prod([0.3, 0.3])             # 0.09

# a model's output IS a probability
probs = model.predict(X)        # e.g. array([0.92, 0.13, 0.68])
preds = (probs >= 0.5).astype(int)   # turn chances into decisions
""")

    + h2("🔬", "What is actually happening")
    + """<p>Two things worth carrying forward.</p>
<p><b>The multiplying rule is why anomaly detection works.</b> Course 3 computes p(x) as a product across
every feature. A server that is mildly unusual on CPU <em>and</em> mildly unusual on memory <em>and</em>
mildly unusual on disk multiplies out to something genuinely rare — even though no single measurement
looked alarming. The multiplication is doing the detecting.</p>
<p><b>The vertical bar is everywhere.</b> P(y = 1 | x) — “the chance of a yes, <em>given</em> this input” —
is what every classifier in these courses actually outputs. When logistic regression returns 0.7, that is
what the 0.7 means. Not “70% of the time this happens”, but “given what I can see about this particular
example, 70%”.</p>
<p>One honest caveat: the multiplying rule needs the events to be <b>independent</b>, and real features
rarely are. CPU and network traffic move together. Anomaly detection assumes independence anyway and works
well regardless — a recurring theme in applied machine learning.</p>"""

    + h2("🕳", "Traps")
    + trap("""<p><b>Multiplying things that are not independent.</b> P(rain today) × P(rain tomorrow) is
wrong — weather is correlated. The rule needs independence to be exactly right.</p>""")
    + trap("""<p><b>Reading a model output of 0.7 as “70% of these are positive”.</b> It is a statement
about <em>this</em> example given its features, not about a population.</p>""")

    + h2("✅", "Check yourself")
    + quiz([
        ("P(spam) = 0.2. What is P(not spam)?",
         "<p>1 − 0.2 = <b>0.8</b>. They must add to 1.</p>"),
        ("Three independent features each have probability 0.2 for this example. What is p(x)?",
         "<p>0.2 × 0.2 × 0.2 = <b>0.008</b>. Three mild oddities become one rare event.</p>"),
        ("What does the bar in P(y = 1 | x) mean?",
         "<p>“<b>Given</b>” — the probability of y being 1, given that we have observed this particular x. "
         "It is what every classifier in this specialization outputs.</p>"),
    ])

    + h2("🔗", "Go deeper")
    + links([
        ("play", "https://seeing-theory.brown.edu/basic-probability/index.html",
         "Seeing Theory — Basic Probability",
         "Interactive and beautiful. Drag things and watch the probabilities respond."),
    ]))

# ============================================================ 17
lesson("17-mean-variance", "Mean, variance and standard deviation", 9,
    "Where the middle is, and how spread out things are. Five steps, in order — and the reason step three "
    "squares everything.",
    pretest("""<p>Two classrooms both average 10 out of 20. In one, everyone scored 10. In the other, scores ran 0 to 20. <b>The average cannot tell them apart — what second number would?</b></p>""",
        """<p>Watch for the name of that second number, and for why it squares the distances rather than just adding them up.</p>""")
    + h2("🎈", "The idea, in plain words")
    + kid("""<p>Two questions you can ask about any pile of numbers.</p>
<p><b>Where is the middle?</b> Add them all up, divide by how many. That is the mean.</p>
<p><b>How spread out are they?</b> Measure how far each one sits from the middle, and take a typical
distance. That is the standard deviation.</p>
<p>[9, 10, 11] and [1, 10, 19] have the same middle and are nothing alike. The spread is what tells them
apart.</p>
<p>Two classrooms could both average exactly 70% on a test — one because nearly every student scored close to 70, the other because half the class scored 40 and half scored 100. The average alone cannot tell those two classrooms apart. The spread is what does.</p>""")

    + h2("🔤", "The symbol, and how to say it")
    + decode([
        ("<var>μ</var>", "“mu”", "the mean. Sometimes written x̄ (“x bar”)."),
        ("<var>σ</var>", "“sigma”", "the standard deviation. In the same units as your data."),
        ("<var>σ</var><sup>2</sup>", "“sigma squared”", "the variance. σ is its square root."),
        ("<var>x</var><sup>(<var>i</var>)</sup> − <var>μ</var>", "“the deviation”", "how far one value sits from the middle. Can be negative."),
        ("<var>m</var>", "“em”", "how many values you have."),
    ])
    + eqp([
        ('<var>μ</var> = <span class="frac"><span>1</span><span><var>m</var></span></span>', "avg-factor", "the average"),
        (' <span class="big">Σ</span> <var>x</var><sup>(<var>i</var>)</sup>', "sigma", "add up every point"),
        '&nbsp;&nbsp;&nbsp;&nbsp;',
        ('<var>σ</var><sup>2</sup> = <span class="frac"><span>1</span><span><var>m</var></span></span> <span class="big">Σ</span> ( <var>x</var><sup>(<var>i</var>)</sup> − <var>μ</var> )<sup>2</sup>',
         "variance-f0", "average squared distance from μ"),
    ], "you can now read both of these — Σ is the loop, μ is the mean — click a part", small=True)

    + h2("🧮", "Worked by hand")
    + """<p>Take [2, 4, 4, 4, 5, 5, 7, 9]. Eight numbers.</p>
<ol>
<li><b>Mean:</b> (2+4+4+4+5+5+7+9) / 8 = 40 / 8 = <b>5</b></li>
<li><b>Deviations:</b> −3, −1, −1, −1, 0, 0, 2, 4</li>
<li><b>Square them:</b> 9, 1, 1, 1, 0, 0, 4, 16</li>
<li><b>Variance:</b> (9+1+1+1+0+0+4+16) / 8 = 32 / 8 = <b>4</b></li>
<li><b>Standard deviation:</b> √4 = <b>2</b></li>
</ol>
<p>So the typical distance from the middle is 2. Sanity check against the data: most values sit within 2
of 5, and that is exactly what you see.</p>"""

    + h2("🎬", "Watch it move")
    + demo("fstats", "Spread the points out and watch σ grow",
           "the shaded band is one standard deviation either side of the mean")

    + h2("💻", "In NumPy")
    + code("""
import numpy as np
x = np.array([2, 4, 4, 4, 5, 5, 7, 9])

x.mean()      # 5.0
x.var()       # 4.0
x.std()       # 2.0

# on a 2-D array, one answer per column:
X = np.random.rand(100, 4)
X.mean(axis=0)    # shape (4,)  -- the mean of each feature
X.std(axis=0)     # shape (4,)

# which is exactly feature scaling:
X_scaled = (X - X.mean(axis=0)) / X.std(axis=0)
""")
    + """<p>That last line is the whole of z-score normalisation from Course 1, Week 2. Now you can read
it: subtract each column's mean, divide by each column's spread.</p>"""

    + h2("🔬", "What is actually happening")
    + """<p><b>Why square in step three?</b> Because the raw deviations always add to exactly zero — the
ones above the mean cancel the ones below. That is not a coincidence; it is what “mean” means. Squaring
makes every deviation count positively.</p>
<p><b>Why take the square root at the end?</b> Because squaring changed the units. If your data is in
pounds, the variance is in pounds-squared, which is meaningless to a human. σ puts it back into pounds so
you can say “typically about 2 pounds away”.</p>
<p><b>Where you will meet these:</b> feature scaling (Course 1), the Gaussian in anomaly detection (Course
3), and variance reduction in regression trees (Course 2). Same two numbers, three different jobs.</p>"""
    + note("""<p>Statistics courses divide by (m−1) rather than m, to correct a small bias when you are
estimating from a sample. Andrew uses m and notes the difference is negligible with any reasonable amount
of data. NumPy defaults to m; pandas defaults to m−1. Worth knowing, not worth losing time over.</p>""",
           "m or m−1?")

    + h2("🕳", "Traps")
    + trap("""<p><b>Confusing variance and standard deviation.</b> Variance is the squared one. If someone
says “σ = 2”, the variance is 4.</p>""")
    + trap("""<p><b>Computing the scaling numbers on all your data.</b> μ and σ must come from the
<em>training set only</em>, then be applied everywhere else. Otherwise test information leaks in.</p>""")

    + h2("✅", "Check yourself")
    + quiz([
        ("What is the mean of [10, 20, 30]?",
         "<p>60 / 3 = <b>20</b>.</p>"),
        ("Same numbers. What is the standard deviation?",
         "<p>Deviations: −10, 0, 10. Squared: 100, 0, 100. Variance = 200/3 ≈ 66.7. "
         "σ = √66.7 ≈ <b>8.16</b>.</p>"),
        ("Why square the deviations instead of just adding them up?",
         "<p>Because the plain deviations always sum to <b>zero</b> — the positives cancel the negatives. "
         "Squaring makes them all count.</p>"),
    ])

    + h2("🔗", "Go deeper")
    + links([
        ("video", "https://www.youtube.com/watch?v=SzZ6GpcfoQY",
         "StatQuest — Standard Deviation, clearly explained",
         "Short and genuinely clear, if the squaring still feels arbitrary."),
    ]))

# ============================================================ 18
lesson("18-normal-distribution", "The normal distribution", 8,
    "The bell curve. Two numbers describe it completely — and it is the entire model behind anomaly "
    "detection.",
    pretest("""<p>Measure a thousand adults' heights and draw a bar per height. <b>Sketch the shape you expect</b>, then guess how many numbers it would take to describe that shape exactly.</p>""",
        """<p>Watch for the answer being <em>two</em>. Watch also for why this particular hill shape turns up in so many unrelated places.</p>""")
    + h2("🎈", "The idea, in plain words")
    + kid("""<p>Measure a thousand people's heights and draw a bar for each. You get a hill: lots of people
near the middle, fewer as you go out, almost nobody at the extremes.</p>
<p>That hill shape turns up everywhere in nature. And it takes exactly <b>two</b> numbers to describe:
where the top is (μ) and how wide it is (σ).</p><p>Most adults sit close to the average height, a few are notably short or tall, and almost nobody is seven feet or two feet tall — that tapering-off-at-the-extremes shape appears again and again because a huge number of small, independent effects (genes, nutrition, and so on) are all pulling the outcome in different directions and, on average, cancelling out.</p>""")

    + h2("🔤", "The symbol, and how to say it")
    + eqp([
        '<var>p</var>(<var>x</var>) <span class="op">=</span> ',
        ('<span class="frac"><span>1</span><span>√<span class="sqrt">2π</span> <var>σ</var></span></span>',
         "normal-dist-f0", "scales the curve to sum to 1"),
        ('<var>e</var><sup>−<span class="frac"><span>(<var>x</var> − <var>μ</var>)<sup>2</sup></span><span>2<var>σ</var><sup>2</sup></span></span></sup>',
         "exponential-f0", "falls off fast, away from μ"),
    ], "the formula — recognise the parts, do not memorise it — click one")
    + decode([
        ("(<var>x</var> − <var>μ</var>)<sup>2</sup>", "“distance from the middle, squared”", "the <b>only</b> place x appears. Symmetric, so ±2 away are equally likely."),
        ("<var>e</var><sup>−(…)</sup>", "“e to the minus”", "makes it fall away fast as you move out. This is the bell shape."),
        ("2<var>σ</var><sup>2</sup>", "“two sigma squared”", "controls how fast it falls — the width."),
        ("1/(√2π σ)", "“the normalising constant”", "nothing conceptual. It scales the curve so the area comes to exactly 1."),
        ("<var>p</var>(<var>x</var>)", "“p of x”", "a <b>density</b>, not a probability. It can exceed 1."),
        ("~ <var>N</var>(<var>μ</var>, <var>σ</var><sup>2</sup>)", "“is distributed normally with…”", "shorthand for “this follows a bell curve with this middle and this spread”."),
    ])

    + h2("🧮", "The numbers worth memorising")
    + table(["Range", "Fraction inside", "In anomaly terms"],
            [["μ ± 1σ", "68%", "completely ordinary"],
             ["μ ± 2σ", "95%", "still normal"],
             ["μ ± 3σ", "99.7%", "getting unusual"],
             ["beyond μ ± 4σ", "0.006%", "about 1 in 15,000 — worth investigating"]])
    + """<p>This is where the phrase “a three-sigma event” comes from: something in the outer 0.3%.</p>"""

    + h2("🎬", "Watch it move")
    + demo("fnormal", "Drag μ and σ",
           "the shaded bands are one, two and three standard deviations")

    + h2("💻", "In NumPy")
    + code("""
import numpy as np

# fitting one to data is just two lines
x = np.random.normal(5, 1.2, size=1000)   # generate some
mu    = x.mean()      # ~5.0
sigma = x.std()       # ~1.2

# evaluating the density at a point
def gaussian(x, mu, sigma):
    return np.exp(-(x - mu)**2 / (2 * sigma**2)) / (np.sqrt(2*np.pi) * sigma)

gaussian(5.0, mu, sigma)    # tallest, at the middle
gaussian(9.0, mu, sigma)    # tiny -- more than 3 sigma out
""")
    + """<p>Notice how short “fitting a Gaussian” is: compute a mean, compute a standard deviation, done.
There is no training loop. That is why anomaly detection is so cheap to run.</p>"""

    + h2("🔬", "What is actually happening")
    + """<p><b>Density is not probability.</b> p(x) can be bigger than 1 when σ is small — the curve gets
tall and narrow. Only the <em>area</em> under a stretch of curve is a probability, and the total area is
always exactly 1. That is what the constant out front is for.</p>
<p><b>Small σ makes a suspicious model.</b> A narrow spike means the model has seen very consistent data,
so anything even slightly off-centre gets a very low p(x). A wide flat hill means almost nothing looks
strange. This is the dial that decides how twitchy your anomaly detector is.</p>
<p><b>And the honest caveat:</b> plenty of real features are not bell-shaped at all. Incomes, response
times and file sizes are all heavily skewed. That is exactly why Course 3, Week 1 has a whole lesson on
transforming features with log(x + c) until the histogram looks like a hill.</p>"""

    + h2("🕳", "Traps")
    + trap("""<p><b>Assuming your data is normal.</b> Plot a histogram first. It takes one line and it is
frequently a surprise.</p>""")
    + trap("""<p><b>Reading p(x) as a probability.</b> It is a density. p(x) = 4 is perfectly legal and
does not mean 400%.</p>""")

    + h2("✅", "Check yourself")
    + quiz([
        ("μ = 100, σ = 15. Is 145 unusual?",
         "<p>It is 3σ above the mean. Only about 0.15% of values sit that far above — <b>unusual</b>, "
         "though not extraordinary.</p>"),
        ("What happens to the peak height as σ shrinks?",
         "<p>It <b>rises</b> — the same total area squeezed into a narrower curve. With σ = 0.1 the peak "
         "is about 4. Densities are allowed to exceed 1.</p>"),
        ("You fit a Gaussian and get σ = 0. What does that mean?",
         "<p>Every training value was identical. The curve collapses to a spike and any different value "
         "gets p ≈ 0 — the feature is useless, and numerically dangerous.</p>"),
    ])

    + h2("🔗", "Go deeper")
    + links([
        ("play", "https://seeing-theory.brown.edu/probability-distributions/index.html",
         "Seeing Theory — Probability Distributions",
         "Interactive. Drag μ and σ and watch the curve respond."),
        ("video", "https://www.youtube.com/watch?v=rzFX5NWojp0",
         "StatQuest — The Normal Distribution",
         "Five minutes, and it sticks."),
    ]))

# ============================================================ 19
lesson("19-min-max-argmax", "min, max, argmin and argmax", 6,
    "Four words that appear in almost every algorithm in the specialization. The “arg” prefix is the "
    "only thing to learn.",
    pretest("""<p>Scores [0.1, 0.7, 0.2]. One question asks “how good was the best?”, another asks “which one was best?”. <b>Give both answers</b> — they are different numbers.</p>""",
        """<p>0.7 and position 1. Watch for the two names, and for which one turns a neural network's output into an actual prediction.</p>""")
    + h2("🎈", "The idea, in plain words")
    + kid("""<p>You have a row of scores: 12, 31, 7, 24, 19.</p>
<p><b>max</b> asks “what is the biggest score?” — the answer is 31.</p>
<p><b>argmax</b> asks “<b>where</b> is the biggest score?” — the answer is position 1.</p>
<p>One gives you the value. The other gives you the place. That is the entire difference, and it matters
enormously.</p>
<p>A talent-show judge does this instinctively: “the highest score was a 9.8” is max; “contestant number 4 got that score” is argmax. Everyone already keeps both pieces of information straight in ordinary life, without ever needing a maths class to do it.</p>""")

    + h2("🔤", "The symbol, and how to say it")
    + decode([
        ("max", "“max”", "the biggest <b>value</b>."),
        ("argmax", "“arg max”", "the <b>position</b> (or the thing) that produces the biggest value."),
        ("min / argmin", "“min” / “arg min”", "the same pair, for smallest."),
        ("argmax<sub><var>a</var></sub>", "“arg max over a”", "the subscript says <em>what you are choosing between</em> — here, actions."),
        ("arg", "“argument”", "in maths, “the input”. So argmax = “the input that maximises it”."),
    ])
    + key("""<p>“arg” means “the input that does it”. Once you know that, <b>argmax<sub>a</sub> Q(s,a)</b>
reads straightforwardly: “the action a that makes Q biggest” — the action, not the score.</p>""")

    + h2("🧮", "Worked by hand")
    + """<p>x = [12, 31, 7, 24, 19], with positions 0, 1, 2, 3, 4.</p>
<ul>
<li>max(x) = <b>31</b> · argmax(x) = <b>1</b></li>
<li>min(x) = <b>7</b> · argmin(x) = <b>2</b></li>
</ul>"""

    + h2("🎬", "Watch it move")
    + demo("fargmax", "The four in turn",
           "watch whether the highlight lands on the value or on the index")

    + h2("💻", "In NumPy")
    + code("""
import numpy as np
x = np.array([12, 31, 7, 24, 19])

np.max(x)        # 31
np.argmax(x)     # 1
np.min(x)        # 7
np.argmin(x)     # 2

# the classic use: turning 10 class probabilities into a predicted digit
probs = model.predict(X)      # shape (m, 10)
preds = np.argmax(probs, axis=1)    # shape (m,)  -- which class won, per row
""")
    + warn("""<p><code>axis=1</code> takes the max across each <b>row</b> — one answer per example, which is
what you want. <code>axis=0</code> goes down the columns and asks a completely different, useless question.
Getting this wrong produces an answer of the wrong length, which at least fails loudly.</p>""")

    + h2("🔬", "What is actually happening")
    + """<p>Where these appear in the three courses:</p>
<ul>
<li><b>Classification</b> (C2 W2): the network gives 10 probabilities; <code>argmax</code> turns them into
a predicted digit. You want the <em>which</em>, not the score.</li>
<li><b>K-means</b> (C3 W1): <code>argmin</code> over distances assigns each point to its nearest centroid.
Again the index, not the distance.</li>
<li><b>Reinforcement learning</b> (C3 W3): π*(s) = argmax<sub>a</sub> Q(s,a) — the optimal policy is
literally “take whichever action scores highest”.</li>
<li><b>Decision trees</b> (C2 W4): pick the feature with the highest information gain.</li>
</ul>
<p>In every case the pattern is the same: score all the options, then pick the winner by position. That is
why these four words are worth five minutes.</p>"""

    + h2("🕳", "Traps")
    + trap("""<p><b>Using max where you meant argmax.</b> You get the score instead of the choice. Often
this is a number in a plausible range, so nothing errors and the behaviour is just wrong.</p>""")
    + trap("""<p><b>Ties.</b> If two entries are equally largest, <code>argmax</code> returns the
<em>first</em>. Rarely matters; occasionally it does.</p>""")

    + h2("✅", "Check yourself")
    + quiz([
        ("x = [5, 2, 9, 1]. What are max(x) and argmax(x)?",
         "<p>max = <b>9</b>, argmax = <b>2</b> (counting from zero).</p>"),
        ("A model outputs [0.1, 0.7, 0.2] for three classes. Which does it predict?",
         "<p>argmax = <b>1</b> — class 1, the middle one. The value 0.7 is its confidence, not the answer.</p>"),
        ("What does argmax_a Q(s, a) mean in reinforcement learning?",
         "<p>“The <b>action</b> a that makes Q(s, a) biggest.” The action itself, not its value. That is "
         "the optimal policy.</p>"),
    ])

    + h2("🔗", "Go deeper")
    + links([
        ("docs", "https://numpy.org/doc/stable/reference/generated/numpy.argmax.html",
         "numpy.argmax", "Note the <code>axis</code> argument, and what it does to the output shape."),
    ]))

WEEK = dict(
    course="F0", week=1, title="The Maths You Actually Need",
    time="~4–5 h",
    goal="Every symbol, formula and mathematical idea the three courses assume you already know — "
         "explained plainly, worked by hand, with its NumPy equivalent.",
    lessons=L,
)
