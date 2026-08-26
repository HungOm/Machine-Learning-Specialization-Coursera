# -*- coding: utf-8 -*-
"""Index page: the study plan itself."""
from kit import kid, key, warn, card, links, h2, grid2, grid3, note, table

HERO = """
<section class="cover">
  <canvas class="cover-cv" data-cover="1" aria-hidden="true"></canvas>
  <button class="cover-fs" data-cover-fs type="button"
          title="Full screen (f)" aria-label="Full screen">&#9974;</button>
  <div class="cover-in">
    <p class="cover-eyebrow">A study companion</p>
    <h1 class="cover-title">Machine<span>Learning</span></h1>
    <div class="cover-rule"></div>
    <p class="cover-sub">The maths you actually need, then the whole specialization &mdash;
      one page per idea, with everything that connects them.</p>
    <div class="cover-stat">
      <div><b>4</b>parts</div><div><b>12</b>chapters</div>
      <div><b>{total}</b>lessons</div><div><b>156</b>problems</div>
    </div>
    <nav class="cover-nav" aria-label="Start reading">
      <a class="cv-btn primary" data-cover-resume href="f0/w1-01-what-is-a-function.html">
        <b>Start reading</b><i>&sect;&nbsp;1.1 &middot; What a function is</i></a>
      <a class="cv-btn" data-cover-contents href="#lessons"><b>Contents</b><i>12 chapters</i></a>
      <a class="cv-btn" href="review.html"><b>Review</b><i>due today</i></a>
    </nav>
    <p class="cover-by">Hung Om</p>
  </div>
  <button class="cover-next" data-cover-next type="button">
    <span>Begin</span><span class="chev">&#8595;</span></button>
</section>
<div class="hero">
<p class="kicker">Machine Learning Specialization · DeepLearning.AI + Stanford</p>
<h1>Every lesson, one page, with the maths pulled apart and animated.</h1>
<p class="lede">This is a companion to the course videos — not a replacement for them. Each page takes
<b>one</b> lesson, tells the idea in plain words, then shows the same idea as maths with every
symbol decoded, then lets you play with a live animation of it, then gives you the code and the papers.
Starting from <b>no maths and no programming background</b>: a Foundations track that teaches every
symbol and every line of Python the courses assume, then the whole specialization — Course 1
(regression, classification, gradient descent), Course 2 (neural networks, diagnostics, decision trees)
and Course 3 (clustering, recommenders, reinforcement learning). <b>{total} lessons</b>, about
{hours} hours of reading plus the labs.</p>
</div>
<div class="statgrid">
  <div class="stat"><div class="k">Lessons</div><div class="v">{total}</div></div>
  <div class="stat"><div class="k">Problems</div><div class="v"><a href="problems.html">156</a></div></div>
  <div class="stat"><div class="k">From scratch</div><div class="v"><a href="scratch.html">10</a></div></div>
  <div class="stat"><div class="k">Lab guides</div><div class="v"><a href="labs.html">41</a></div></div>
  <div class="stat"><div class="k">Review cards</div><div class="v"><a href="review.html">161</a></div></div>
  <div class="stat"><div class="k">Paper sheets</div><div class="v"><a href="paper.html">12</a></div></div>
  <div class="stat"><div class="k">Weeks mastered</div><div class="v"><a href="mastery.html">0&#8202;/&#8202;12</a></div></div>
</div>
"""

PLAN = (
  h2("🎒", "Start here — the Foundations track", "foundations")
  + """<p>These courses quietly assume you already know what ∂J/∂w means and what
<code>W[:, j]</code> does. If you don't, the lectures wash over you and it feels like a maths problem
when it is really a <b>vocabulary</b> problem.</p>
<p>So there is a track before the courses: <b>35 lessons</b> covering every symbol, formula and line of
Python the specialization takes for granted. Nothing more — this is not a maths degree, it is the
specific, surprisingly small set of things you actually need.</p>"""
  + grid2(
      card('<h3><a href="f0/w1-01-what-is-a-function.html">∑ The maths you actually need</a></h3>'
           '<p>19 lessons. Functions · graphs · Greek letters · slope · derivatives · partial derivatives · '
           'Σ and Π · vectors · dot products · matrices · matrix multiplication · transpose · exponentials · '
           'logarithms · probability · mean and variance · the bell curve · argmax.</p>'
           '<p style="margin-bottom:0"><a class="btn primary" href="f0/w1-01-what-is-a-function.html">start the maths lane</a></p>'),
      card('<h3><a href="f0/w2-01-jupyter.html">🐍 Python, NumPy and pandas</a></h3>'
           '<p>16 lessons. Jupyter · types · lists vs arrays · slicing · shape and axis · creating arrays · '
           'elementwise maths · broadcasting · dot in code · aggregations · boolean masks · reshape · '
           'DataFrames · pandas→NumPy · reading errors · functions.</p>'
           '<p style="margin-bottom:0"><a class="btn" href="f0/w2-01-jupyter.html">start the Python lane</a></p>'))
  + note("""<p>Every Foundations lesson has the same six parts: the idea told plainly, <b>the symbol and
how to say it out loud</b>, the maths worked by hand on tiny numbers, an animation, <b>the NumPy or pandas
equivalent</b>, and what is actually happening underneath.</p>
<p>There is also a <a href="symbols.html">symbol glossary</a> — all 71 symbols in one filterable table,
each with its pronunciation and its code equivalent. Keep it open in a tab while you watch lectures.</p>""",
         "What each Foundations lesson gives you")

  + h2("◆", "Review — the part that makes it stick", "review")
  + """<p>Reading a lesson once is not learning it. Within a month most of it is gone unless something
brings it back. So alongside the notes there is a <b>spaced-repetition deck</b>: 161 cards covering every
symbol, formula, algorithm and load-bearing idea — Foundations included.</p>"""
  + grid2(
      card('<h3><a href="review.html">◆ Review trainer</a></h3>'
           '<p>Cards with the answer hidden and a schedule attached. Grade yourself honestly and each card '
           'comes back exactly when you are about to forget it — tomorrow if you fumbled, in eight months '
           'if it is solid.</p>'
           '<p style="margin-bottom:0"><a class="btn primary" href="review.html">start reviewing</a></p>'),
      card('<h3><a href="reference.html">☰ Reference sheet</a></h3>'
           '<p>The same 161 entries with both sides showing, grouped by week. This is the page to scan '
           'before an exam or an interview, or when you half-remember a formula and need it now.</p>'
           '<p style="margin-bottom:0"><a class="btn" href="reference.html">open the sheet</a></p>'))
  + note("""<p>A nightly alarm can be installed so this does not depend on remembering. It plays a sound
on this Mac at 22:00 every day:</p>
<pre style="margin:10px 0 0"><code>bash study/_build/install-alarm.sh          # install
bash study/_build/install-alarm.sh --test   # hear it now
bash study/_build/install-alarm.sh --remove # uninstall</code></pre>""", "The 10 pm reminder")

  + h2("🧭", "How to use this", "how")
  + """<p>The order matters more than the speed. Do this loop for every single lesson — it takes
about 25–35 minutes and it is the difference between “I watched a video” and “I can rebuild it”.</p>"""
  + grid3(
      card('<h3>1 · Watch</h3><p>Watch the Coursera video first, at 1× speed, without pausing. '
           'Do not take notes. Just get the shape of the idea.</p>'),
      card('<h3>2 · Read + play</h3><p>Open that lesson\'s page here. Read the plain-words opening, '
           'then the decoded maths, then <b>drag the sliders</b> until the animation stops surprising you.</p>'),
      card('<h3>3 · Rebuild</h3><p>Close everything. On paper, write the formula from memory and '
           'compute one tiny example by hand. Then open the notebook lab and make it run.</p>'))
  + kid("""<p>Think of a video like watching someone ride a bike. The animation on each page is you
holding the handlebars while someone steadies the seat. The lab is you riding it alone. You cannot skip
straight from watching to riding — everybody falls off.</p>""")
  + key("""<p>If you can’t explain a formula out loud, in plain words, <em>without</em> looking at it,
you don’t know it yet. That is the bar every page here is written to.</p>""")

  + h2("📅", "A three-week plan for Course 1", "plan1")
  + """<p>Start here if you are new. Course 1 is where every idea in the specialization is introduced in
its simplest possible form — one feature, one straight line, a cost you can draw on paper. Everything
later is a variation on it.</p>"""
  + table(
      ["Week", "Mon–Tue", "Wed–Thu", "Fri", "Weekend"],
      [["<b>1</b><br><span style='color:var(--ink-faint)'>Linear regression</span>",
        "Lessons 1–4: what ML is, supervised vs unsupervised, the model f = wx + b",
        "Lessons 5–7: the cost function, and the contour plot of J(w, b)",
        "Lessons 8–11: gradient descent, and the learning rate",
        "Lessons 12–13 + the optional labs on cost and gradient descent"],
       ["<b>2</b><br><span style='color:var(--ink-faint)'>Many features</span>",
        "Lessons 1–3: multiple features and vectorisation",
        "Lessons 4–6: gradient descent at scale, feature scaling, convergence",
        "Lessons 7–9: choosing α, feature engineering, polynomial regression",
        "The W2 assignment, plus the NumPy vectorisation lab"],
       ["<b>3</b><br><span style='color:var(--ink-faint)'>Classification</span>",
        "Lessons 1–3: why linear regression fails, the sigmoid, the decision boundary",
        "Lessons 4–7: the logistic cost, and gradient descent for it",
        "Lessons 8–9: overfitting, and the three ways to address it",
        "Lessons 10–11 (regularisation) + the W3 assignment"]])
  + note("""<p>The single most important idea in Course 1 is the <b>three-part structure</b>: a model, a
cost function that scores it, and gradient descent that improves it. Every algorithm in Courses 2 and 3 is
those same three parts with different pieces slotted in. If you can state them for linear regression, you
can follow anything that comes later.</p>""", "What Course 1 is really teaching")

  + h2("📅", "A four-week plan for Course 2", "plan")
  + """<p>Five days on, two days off. Each “day” is roughly 70–90 minutes. If you only have 40 minutes,
do half a day and let the plan stretch to 8 weeks — spacing it out actually helps memory, it does not hurt it.</p>"""
  + table(
      ["Week", "Mon–Tue", "Wed–Thu", "Fri", "Weekend"],
      [["<b>1</b><br><span style='color:var(--ink-faint)'>Neural networks</span>",
        "Lessons 1–6: what a neuron is, layers, forward propagation",
        "Lessons 7–12: TensorFlow, data shapes, NumPy by hand",
        "Lessons 13–16: vectorisation + matrix multiplication",
        "Lab: <i>Neurons and Layers</i>, <i>Coffee Roasting</i> ×2, then the W1 assignment"],
       ["<b>2</b><br><span style='color:var(--ink-faint)'>Training</span>",
        "Lessons 1–5: the loss, gradient descent, activation functions",
        "Lessons 6–10: softmax and multiclass",
        "Lessons 11–12: Adam, convolutional layers",
        "Optional lessons 13–15 (back-prop) + the W2 assignment"],
       ["<b>3</b><br><span style='color:var(--ink-faint)'>Advice that actually works</span>",
        "Lessons 1–5: train/cv/test, bias vs variance",
        "Lessons 6–9: baselines, learning curves, NNs and regularisation",
        "Lessons 10–13: the dev loop, error analysis, more data",
        "Lessons 14–17: ethics, precision/recall + the W3 assignment"],
       ["<b>4</b><br><span style='color:var(--ink-faint)'>Trees</span>",
        "Lessons 1–5: trees, entropy, information gain",
        "Lessons 6–8: one-hot, continuous splits, regression trees",
        "Lessons 9–13: bagging, random forests, XGBoost",
        "The W4 assignment, then re-read your own notes from week 3"]])
  + warn("""<p>Do not skip Week 3. It is the least mathematical week and by far the most useful one at work.
Almost every real ML failure is a week-3 failure (wrong split, wrong baseline, wrong metric), not a
week-1 failure.</p>""")

  + h2("📅", "A three-week plan for Course 3", "plan3")
  + """<p>Course 3 is shorter and broader. Three weeks at the same pace, and week 3 is the one that will
take longest — reinforcement learning has more genuinely new vocabulary than anything else in the
specialization.</p>"""
  + table(
      ["Week", "Mon–Tue", "Wed–Thu", "Fri", "Weekend"],
      [["<b>1</b><br><span style='color:var(--ink-faint)'>Unsupervised</span>",
        "Lessons 1–6: clustering and K-means, start to finish",
        "Lessons 7–9: anomaly detection and the Gaussian",
        "Lessons 10–12: evaluating it, and choosing features",
        "Both W1 assignments: K-means (with image compression) and anomaly detection"],
       ["<b>2</b><br><span style='color:var(--ink-faint)'>Recommenders</span>",
        "Lessons 1–5: the ratings matrix through mean normalisation",
        "Lessons 6–10: TensorFlow, related items, two-tower networks, scale",
        "Lessons 11–12: ethics, and the Keras implementation",
        "Both W2 assignments, then optional lessons 13–15 on PCA"],
       ["<b>3</b><br><span style='color:var(--ink-faint)'>Reinforcement learning</span>",
        "Lessons 1–5: rover, returns, policies, MDPs",
        "Lessons 6–9: Q(s,a) and the Bellman equation — the hardest two days of the course",
        "Lessons 10–13: continuous states, lunar lander, deep Q-learning",
        "Lessons 14–16 + the lunar lander assignment"]])
  + note("""<p>Week 3 of Course 3 is where people stall. The reason is almost always Q(s, a): it is defined
in terms of behaving optimally afterwards, which sounds circular until the Bellman equation resolves it.
Spend a whole session on lessons 6–8 and compute the rover’s Q values on paper. Everything after that is
comparatively mechanical.</p>""", "The one place to slow down")

  + h2("🎒", "What you need before starting", "prereq")
  + """<p>Very little. Course 1 assumes:</p>
<ul>
<li><b>Basic Python.</b> Loops, functions, lists. You do not need to be fluent — the first optional lab is
a refresher, and NumPy is taught as you go.</li>
<li><b>High-school algebra.</b> What a straight line is, what a slope is, how to read y = mx + c.</li>
<li><b>Willingness to see a derivative</b> without needing to compute one. Every formula that involves
calculus is decoded symbol by symbol on the page it appears; you are never asked to differentiate anything
by hand.</li>
</ul>
<p>That is genuinely all. If any of it feels shaky, the “Go deeper” links on each page include free
refreshers.</p>"""
  + kid("""<p>If a formula looks frightening, read its decoder table first. Every symbol in this site is
explained in a table right underneath the equation — what it is called, how to say it out loud, and what it
actually <em>is</em>. The maths stops being scary once you can pronounce it.</p>""", "One piece of advice")

  + h2("🗺", "The shape of the three courses", "map")
  + grid2(
      card("<h3>C1 W1–2 — the foundation</h3><p>A model, a cost function, and gradient descent, on the "
           "simplest possible example. Then many features, vectorisation and scaling. Everything later "
           "reuses these three pieces.</p>"),
      card("<h3>C1 W3 — classification</h3><p>The sigmoid, a cost function that had to be redesigned, "
           "and the first appearance of overfitting and regularisation — the two ideas that never stop "
           "mattering.</p>"))
  + grid2(
      card("<h3>C2 W1–2 — the machine</h3><p><b>How</b> a neural network computes and how it learns. "
           "Forward propagation, activation functions, softmax, Adam. This is the engineering.</p>"),
      card("<h3>C2 W3–4 — the judgement</h3><p><b>Whether</b> your model is any good and what to do when it "
           "isn't. Bias/variance, error analysis, metrics — plus decision trees, which often beat neural "
           "networks on tabular data.</p>"))
  + grid2(
      card("<h3>C3 W1–2 — learning without labels</h3><p>Finding structure when there is no y: clustering, "
           "anomaly detection, PCA. Then recommender systems, which learn the features and the "
           "preferences at the same time.</p>"),
      card("<h3>C3 W3 — learning from consequences</h3><p>No labels and no fixed dataset — the agent "
           "generates its own data by acting. The Bellman equation, then a deep Q-network that lands a "
           "lunar lander.</p>"))

  + h2("🔗", "Reference shelf", "shelf")
  + links([
      ("docs", "symbols.html",
       "The symbol glossary (in this site)",
       "All 71 symbols with pronunciations and NumPy equivalents, filterable. The page to keep open while watching lectures."),
      ("play", "https://playground.tensorflow.org",
       "TensorFlow Playground",
       "Train a tiny neural network in your browser and watch the decision boundary bend. Ten minutes here is worth an hour of reading."),
      ("video", "https://www.3blue1brown.com/topics/neural-networks",
       "3Blue1Brown — Neural Networks",
       "The best visual explanation of forward and backward propagation ever made. Watch chapters 1–4 alongside week 1–2."),
      ("book", "https://www.deeplearningbook.org/",
       "Goodfellow, Bengio & Courville — Deep Learning",
       "The standard graduate text, free online. Chapter 6 covers everything in Course 2 Weeks 1–2 properly."),
      ("book", "https://info.deeplearning.ai/machine-learning-yearning-book",
       "Andrew Ng — Machine Learning Yearning",
       "Free book. It is essentially Week 3 of this course, expanded — how to decide what to try next."),
      ("docs", "https://cs231n.github.io/neural-networks-1/",
       "Stanford CS231n course notes",
       "Denser than the videos but excellent on activation functions, initialisation and practical training."),
      ("docs", "https://www.tensorflow.org/api_docs/python/tf/keras/layers/Dense",
       "tf.keras Dense layer — official docs",
       "The exact object you use all course. Worth reading the argument list once, slowly."),
      ("docs", "https://numpy.org/doc/stable/user/basics.broadcasting.html",
       "NumPy broadcasting rules",
       "Half of all beginner bugs in this course are shape bugs. This page is the cure."),
      ("book", "http://incompleteideas.net/book/the-book-2nd.html",
       "Sutton & Barto — Reinforcement Learning: An Introduction",
       "Free PDF, and the definitive text for Course 3 week 3. Chapters 1, 3 and 6 cover that whole week properly."),
      ("play", "https://setosa.io/ev/principal-component-analysis/",
       "Explained Visually — Principal Component Analysis",
       "Interactive 3-D PCA. The best single explanation of it anywhere; useful for C3 week 2."),
      ("docs", "https://gymnasium.farama.org/",
       "Gymnasium — the standard RL environment library",
       "<code>LunarLander-v2</code> is the C3 week 3 assignment. Worth installing and playing with."),
      ("lab", "../C2%20-%20Advanced%20Learning%20Algorithms",
       "Course 2 notebooks in this repository",
       "Optional labs and assignments for every week, sitting right next to these notes."),
      ("lab", "../C3%20-%20Unsupervised%20Learning,%20Recommenders,%20Reinforcement%20Learning",
       "Course 3 notebooks in this repository",
       "K-means, anomaly detection, both recommender assignments, and the lunar lander."),
  ])
  + h2("🧭", "The six ways to use this site", "lanes")
  + """<p>Reading is only one of them, and on its own it is the weakest. The other four exist because
recognising an idea on a page and being able to produce it from nothing are completely different
skills, and only the second one survives contact with an assignment.</p>"""
  + grid2(
      card('<h3><a href="index.html#lessons">📚 Read — 172 lessons</a></h3>'
           '<p>One lesson per page, each with a live animation, every symbol decoded, and links to '
           'the papers. This is the lane to follow alongside the videos.</p>'
           '<p style="margin-bottom:0"><a class="btn" href="#foundations">start at Foundations</a></p>'),
      card('<h3><a href="problems.html">✎ Do — 156 problems</a></h3>'
           '<p>Paper-and-pencil problems with <b>every line of the working</b> shown, deliberately '
           'shuffled so you have to work out what kind of problem each one is. Grade yourself and a '
           'missed problem pulls that lesson\'s cards forward.</p>'
           '<p style="margin-bottom:0"><a class="btn primary" href="problems.html">open the problem sets</a></p>'))
  + grid2(
      card('<h3><a href="scratch.html">⚙ Build — 10 algorithms in NumPy</a></h3>'
           '<p>Linear and logistic regression, forward prop, backprop, softmax, decision trees, '
           'k-means, PCA, collaborative filtering and Q-learning &mdash; in pure NumPy, each checked '
           'against a numerical gradient or a library answer. The files really run.</p>'
           '<p style="margin-bottom:0"><a class="btn" href="scratch.html">open the build lane</a></p>'),
      card('<h3><a href="labs.html">⌨ Practise — 41 lab guides</a></h3>'
           '<p>A companion for every notebook in this repository: what it is for, which lessons it '
           'uses, the one thing to watch, and for the 11 graded assignments, what each of the 31 '
           'exercises asks and how it usually goes wrong. No solutions.</p>'
           '<p style="margin-bottom:0"><a class="btn" href="labs.html">open the lab guides</a></p>'))
  + grid3(
      card('<h3><a href="review.html">◆ Remember — 161 cards</a></h3>'
           '<p>Spaced repetition over every formula and algorithm, each with a plain-English '
           'explanation next to the formal one. A nightly alarm at 22:00 if you install it.</p>'
           '<p style="margin-bottom:0"><a class="btn" href="review.html">review now</a> '
           '<a class="btn" href="progress.html">see progress</a></p>'),
      card('<h3><a href="paper.html">✐ Scribble — 12 sheets from memory</a></h3>'
           '<p>You remember by drawing. Every reference entry carries a line saying what to '
           'put on paper for it, every Foundations lesson ends with one, and there is a page '
           'per week you should be able to fill from memory. The method is sourced, not folklore.</p>'
           '<p style="margin-bottom:0"><a class="btn" href="paper.html">open the paper sheets</a></p>'),
      card('<h3><a href="progress.html">▲ Diagnose — what you don\'t know</a></h3>'
           '<p>The dashboard computes your weak spots from two signals: self-check questions you '
           'marked missed, and cards you have forgotten twice. It also exports the deck to Anki and '
           'backs up your schedule.</p>'
           '<p style="margin-bottom:0"><a class="btn" href="progress.html">open the dashboard</a> '
           '<a class="btn" href="symbols.html">∑ symbol glossary</a></p>'))
)

FOOT = """
<hr>
<p style="color:var(--ink-faint);font-size:14px">Progress is stored only in this browser (localStorage) —
nothing is uploaded anywhere. Keyboard: <code>←</code> and <code>→</code> move between lessons.</p>

<section class="about">
<h2>About</h2>
<p>Study notes built while working through the <b>Machine Learning Specialization</b> — structured
and edited by <b>Hung Om</b>, with the lesson text drafted using Claude. The Foundations track, the
five-lane structure and the choice of what to cover are the parts worth judging; the prose is a
means to them.</p>
<p class="credits">
Course material by Andrew Ng —
<a href="https://www.coursera.org/specializations/machine-learning-introduction" target="_blank" rel="noopener">DeepLearning.AI &amp; Stanford Online</a>,
on Coursera. These notes are an independent study companion, not affiliated with or endorsed by
either.<br>
Assignment notebooks in this repository come from
<a href="https://github.com/greyhatguy007/Machine-Learning-Specialization-Coursera" target="_blank" rel="noopener">greyhatguy007/Machine-Learning-Specialization-Coursera</a>,
which this is forked from.
</p>
</section>
"""
