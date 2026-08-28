# -*- coding: utf-8 -*-
"""The mastery plan — what "done" means for each week, and in what order.

The site had materials in six lanes and no statement of when a week was
finished. This supplies that: a fixed order to work in, a time budget, and a
set of conditions that the page evaluates against what you have actually done.

Nothing here is aspirational. Every condition is something the site can check.
"""

ORDER = """
<div class="callout key"><span class="tag">The order, and why it is this order</span>
<p>Within a week, always this sequence. It is not a menu &mdash; each step sets up the next,
and the two most commonly skipped are the two that do the most work.</p>
</div>
<ol class="masterorder">
<li><b>Read the lessons.</b> Once, at reading pace, with the animations. Do not take notes
&mdash; you will do something better than notes in step 2. <span class="mo-why">Getting the
shape of the week before trying to hold any of it.</span></li>
<li><b>Fill the week sheet from memory.</b> Blank paper, page shut. Then open it and correct
in a second colour. <span class="mo-why">This is the step people skip, and it is the one the
evidence is strongest for.</span></li>
<li><b>Work the problem set.</b> Solution shut, on paper. Grade yourself honestly &mdash; a
missed problem pulls that lesson's cards forward and shows up in weak spots.
<span class="mo-why">Recognition and production are different skills. Only this trains the
second one.</span></li>
<li><b>Do the lab.</b> Optional labs first if you want the practice, then the graded
assignment. Read the companion page before you open the notebook.
<span class="mo-why">This is the course's own checkpoint. Treat it as one.</span></li>
<li><b>Read the from-scratch file, then run it.</b> Where the week has one. Change a number
and predict what happens before you press enter. <span class="mo-why">Proves the library was
not doing anything you could not do yourself.</span></li>
<li><b>Let review handle the rest.</b> Ten minutes a day, every day, including the days you
are not studying. <span class="mo-why">Spacing is the one thing a study session cannot do
for itself.</span></li>
</ol>
"""

CRITERIA_NOTE = """
<p>A week is <b>done</b> when all five conditions below hold. Four of them the site checks for
you from what you have actually done; the fifth is the one only you can answer, and it is
deliberately the last one.</p>
<table class="data">
<thead><tr><th>condition</th><th>how it is checked</th></tr></thead>
<tbody>
<tr><td><b>Read</b> &mdash; every lesson marked done</td><td>the <i>mark done</i> button on each lesson</td></tr>
<tr><td><b>Produced</b> &mdash; at least 80% of the week's problems solved unaided</td><td>your own grading on the problem set</td></tr>
<tr><td><b>Practised</b> &mdash; the week's labs marked done</td><td>the <i>mark done</i> button on each lab companion</td></tr>
<tr><td><b>Stuck</b> &mdash; at least 70% of the week's cards at an interval of 21 days or more</td><td>the review trainer's own schedule</td></tr>
<tr><td><b>Explained</b> &mdash; you can fill the week sheet from a blank page and say the one-line version aloud</td><td><b>you</b>, honestly, with the page shut</td></tr>
</tbody></table>
<div class="callout trap"><span class="tag">The 21-day line, and why it is not arbitrary</span>
<p>An interval of 21 days is the usual dividing line between something you have recently seen
and something you actually know. A card at 21 days has survived several successful recalls
spread over weeks. A card you graded <i>Good</i> twice yesterday has survived nothing.</p>
<p>This is why a week cannot be finished in a day, however much you do. The card intervals
have to grow, and growing takes calendar time. That is not a limitation of the site; it is
what the word means.</p></div>
"""

# per-week guidance: what makes this week hard, and the one thing to get right
WEEKS = {
 "f01": dict(hard="Nothing here is difficult; there is just a lot of vocabulary at once.",
   one="Slope, derivative and Σ. Everything in all three courses is built from those three.",
   skip="Skip nothing. This is the week that decides whether the rest reads as maths or as noise."),
 "f02": dict(hard="Shapes. Almost every error you will hit later is a shape you did not check.",
   one="(m, n) for X, (n,) for w, (m,) for the predictions. Write those three down and keep them.",
   skip="If you have written Python before, skim lessons 1&ndash;3 but do <b>not</b> skim broadcasting."),
 "f03": dict(hard="This is the week that explains the things earlier weeks asked you to accept.",
   one="Maximum likelihood. Once you see squared error and cross-entropy fall out of it, loss functions stop being conventions.",
   skip="Take it after Course 3, not before &mdash; every lesson here answers a question an earlier course raised."),
 "c11": dict(hard="Gradient descent is four ideas at once: a model, a cost, a derivative, a step.",
   one="That J is a score for a <i>line</i>, not for the data. Once that clicks, the bowl makes sense.",
   skip="Nothing. This week is the spine of the entire specialization."),
 "c12": dict(hard="It stops being drawable. Two features you can picture; four you cannot.",
   one="Feature scaling. Not as tidiness &mdash; as the thing that makes α choosable at all.",
   skip="Nothing, but the sklearn lessons are quick."),
 "c13": dict(hard="Two new things at once: a squashed output, and a cost with a second job.",
   one="The boundary is where z = 0. You never compute a sigmoid to find it.",
   skip="Nothing. Six graded exercises here &mdash; the heaviest assignment in the specialization."),
 "c21": dict(hard="Notation. Square brackets, round brackets, subscripts, all in one formula.",
   one="A neuron is a dot product wearing a squash function. A layer is several of them.",
   skip="Lesson 12 (path to AGI) is interesting and not load-bearing."),
 "c22": dict(hard="Backprop, and the numerical-stability argument that looks like a detail.",
   one="The chain rule as multiplying the numbers along a path. Draw the path.",
   skip="Nothing, but the optional labs here are unusually good &mdash; do the backprop one."),
 "c23": dict(hard="It is not hard. It is <i>abstract</i>, and that makes it easy to nod along to.",
   one="The two comparisons, in order: J<sub>train</sub> against the baseline, then J<sub>cv</sub> against J<sub>train</sub>.",
   skip="Nothing. This is the most practically useful week in the three courses."),
 "c24": dict(hard="Nothing conceptually. The arithmetic is fiddly and easy to slip on.",
   one="The size weighting in information gain. Drop it and the tree chases tiny pure branches.",
   skip="XGBoost's internals are out of scope &mdash; know what it does, not how."),
 "c31": dict(hard="Two unrelated algorithms in one week. Do not let them blur together.",
   one="k-means finds a <b>local</b> optimum, and J is how you choose between runs.",
   skip="Nothing, but the two assignments are lighter than C1 W3."),
 "c32": dict(hard="Collaborative filtering learns two unknowns at once, which feels impossible.",
   one="Every rating constrains the <i>product</i> w &middot; x. Thousands of them pin down both.",
   skip="Lesson 11 (ethics) is short and worth reading properly, not skimming."),
 "c33": dict(hard="A new vocabulary and a moving target: the labels are made by the model itself.",
   one="The six-state rover. Get V* = [100, 50, 25, 12.5, 20, 40] solid and the rest follows.",
   skip="Nothing. The lunar lander takes real time to train &mdash; start it early."),
 "c41": dict(hard="Everything is a sequence now, and order carries meaning that a bag of numbers loses.",
   one="An embedding is a learned lookup table. Nothing more mystical than that.",
   skip="Skim the RNN history if you are impatient &mdash; but read <b>why</b> it failed."),
 "c42": dict(hard="Three names (query, key, value) for three uses of the same input. That is the whole hump.",
   one="Attention is a weighted average, and softmax picks the weights. You already know both halves.",
   skip="Nothing. This is the week the rest of modern AI is built on."),
 "c43": dict(hard="A lot of machinery arrives at once &mdash; residuals, norms, heads, positions.",
   one="Each piece fixes one specific failure. Learn the failure and the fix is obvious.",
   skip="The exact layer-norm formula. Know what it does and why it is there."),
 "c44": dict(hard="Scale changes behaviour in ways the small examples cannot show you.",
   one="A language model is next-token prediction. Everything else is layered on top of that one job.",
   skip="Nothing, but treat the numbers as illustrative &mdash; they date fast."),
}

BUDGET_NOTE = """
<p>Times are the site's own estimates: lessons are summed from their per-lesson figures and labs
from theirs. Problems assume about six minutes each including the working, and from-scratch pages
about twenty-five minutes including running the file and changing something.</p>
<p>Review is not in the table because it is not weekly &mdash; it is <b>ten minutes a day,
indefinitely</b>, and it is the only line here that continues after you finish the course.</p>
"""
