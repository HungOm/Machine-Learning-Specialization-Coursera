# -*- coding: utf-8 -*-
"""Working it on paper — what to scribble, and why it works.

The learner remembers by drawing. Every claim on this page is sourced; the DOIs
were checked against Crossref before they were written down.
"""

REFS = [
 ("Slamecka &amp; Graf (1978)", "The generation effect: delineation of a phenomenon",
  "https://doi.org/10.1037/0278-7393.4.6.592",
  "Producing an answer yourself is remembered better than reading the same answer. "
  "This is the whole argument for a blank page."),
 ("Roediger &amp; Karpicke (2006)", "Test-enhanced learning",
  "https://doi.org/10.1111/j.1467-9280.2006.01693.x",
  "Being tested beats re-reading, and the gap grows the longer you wait before "
  "the real test. Re-reading feels better and works worse."),
 ("Karpicke &amp; Blunt (2011)", "Retrieval practice produces more learning than "
  "elaborative studying with concept mapping",
  "https://doi.org/10.1126/science.1199327",
  "Recalling from an empty page beat drawing an elaborate concept map — while "
  "students predicted the opposite. Trust the result, not the feeling."),
 ("Wammes, Meade &amp; Fernandes (2016)", "The drawing effect: evidence for reliable "
  "and robust memory benefits in free recall",
  "https://doi.org/10.1080/17470218.2015.1094494",
  "Drawing a thing beat writing its name repeatedly, across seven experiments. "
  "Quality of the drawing did not matter — bad drawings worked too."),
 ("Paivio (1991)", "Dual coding theory: retrospect and current status",
  "https://doi.org/10.1037/h0084295",
  "A picture and words are stored twice, in two systems. Two routes back to the "
  "same idea is why a diagram plus a caption beats either alone."),
 ("Fiorella &amp; Mayer (2015)", "Eight ways to promote generative learning",
  "https://doi.org/10.1007/s10648-015-9348-9",
  "Drawing, self-explaining and teaching are three of the eight. All three are "
  "things you do with a pen, not things you do with your eyes."),
 ("Sweller &amp; Cooper (1985)", "The use of worked examples as a substitute for "
  "problem solving in learning algebra",
  "https://doi.org/10.1207/s1532690xci0201_3",
  "When a topic is brand new, studying a worked example beats struggling. Copy "
  "first, then close the book. The order matters."),
 ("Bjork &amp; Kroll (2015)", "Desirable difficulties in vocabulary learning",
  "https://doi.org/10.5406/amerjpsyc.128.2.0241",
  "Practice that feels harder often teaches more. If scribbling from memory "
  "feels uncomfortable, that is the mechanism working, not a sign to stop."),
]

METHOD = """
<div class="callout key"><span class="tag">The whole method in one line</span>
<p>Shut the page. Fill a sheet from memory. Open the page. Fix what is wrong in a
different colour. <b>The mistakes you make and correct are the part that sticks.</b></p></div>

<h2><span class="ico">&#9999;&#65039;</span>Four moves, in this order</h2>
<p>These are not four options to pick from. They are a sequence, and the order is the
part people get wrong &mdash; most jump straight to move 3 and wonder why nothing sticks.</p>

<div class="grid2">
<div class="card"><h3>1 &middot; Copy it once</h3>
<p>Only for something genuinely new. Copy the formula out by hand, with the page open,
saying each symbol aloud as you write it.</p>
<p>This is the one time reading beats struggling &mdash; with no foothold at all, floundering
just loads you up with nothing to hold. One copy, then stop.</p>
<p class="dim" style="font-size:12.5px">Sweller &amp; Cooper (1985)</p></div>

<div class="card"><h3>2 &middot; Draw the thing</h3>
<p>Not the formula &mdash; <b>the thing the formula is about</b>. A bowl. An arrow. A tilted
cloud of dots. A tree with two branches.</p>
<p>Drawing beat writing across seven experiments, and the drawings did not have to be
good. Yours will be bad. That is fine and does not reduce the effect.</p>
<p class="dim" style="font-size:12.5px">Wammes, Meade &amp; Fernandes (2016)</p></div>
</div>

<div class="grid2">
<div class="card"><h3>3 &middot; Fill a blank sheet</h3>
<p>Close everything. Write down everything you can remember about the topic, in any
order, badly. Then look, and correct in a second colour.</p>
<p>This beat elaborate concept-mapping in a controlled comparison &mdash; and the students
in that study predicted the opposite result. It will feel unproductive. It is not.</p>
<p class="dim" style="font-size:12.5px">Karpicke &amp; Blunt (2011)</p></div>

<div class="card"><h3>4 &middot; Explain it to the paper</h3>
<p>Write the sentence you would say to somebody else. Out loud, then written down.
&ldquo;This bowl is every possible line, and the bottom is the best one.&rdquo;</p>
<p>If the sentence will not come, you have found the gap &mdash; and finding it is the
result you came for.</p>
<p class="dim" style="font-size:12.5px">Fiorella &amp; Mayer (2015)</p></div>
</div>

<h2><span class="ico">&#128209;</span>What a good page looks like</h2>
<p>One sheet, landscape, one topic. It should be crowded and a bit ugly. A page that
looks like a textbook is a page you copied.</p>
<ul>
<li><b>Middle:</b> the picture. The bowl, the arrow, the triangle. No words yet.</li>
<li><b>Around it:</b> the formula, written from memory, with a line from each symbol out
to a word saying what that symbol does.</li>
<li><b>One corner:</b> the smallest worked example you can do &mdash; two data points, not
twenty.</li>
<li><b>Another corner:</b> the trap. Write the wrong version <i>and</i> the right version,
and circle the difference.</li>
<li><b>Second colour, added after checking:</b> everything you got wrong. This is the
most valuable ink on the page.</li>
</ul>

<div class="callout trap"><span class="tag">Three things not to do</span>
<p><b>Do not copy the notes onto paper.</b> Copying is move 1, used once, for something
brand new. Past that it is transcription with the feeling of work attached.</p>
<p><b>Do not make it neat.</b> Time spent on presentation is time not spent retrieving.
Ugly and from memory beats beautiful and copied, every time.</p>
<p><b>Do not check as you go.</b> Peeking mid-recall converts the exercise back into
reading. Write everything you have first, wrong bits included, and only then look.</p></div>

<h2><span class="ico">&#128337;</span>A twenty-minute session</h2>
<table class="data">
<thead><tr><th>time</th><th>do</th><th>why</th></tr></thead>
<tbody>
<tr><td class="num">2 min</td><td>Blank sheet. Write down everything you remember about
today's topic before opening anything.</td><td>Retrieval first, while it is hardest</td></tr>
<tr><td class="num">5 min</td><td>Open the lesson. Correct your sheet in a second colour.
Add what you missed.</td><td>The errors are the lesson</td></tr>
<tr><td class="num">8 min</td><td>Work one problem from that week's set, by hand, solution
shut.</td><td>Production, not recognition</td></tr>
<tr><td class="num">5 min</td><td>Turn the sheet over. Redraw the single most important
picture from memory. Say the one-sentence version aloud.</td><td>Second retrieval, spaced
by a few minutes</td></tr>
</tbody></table>
<p>Then let the <a href="review.html">review trainer</a> handle the spacing. It will bring
each idea back at increasing intervals, which is the part a study session cannot do for
itself.</p>
"""

# ---------------------------------------------------------------- week sheets
# "If you can fill this page from memory, you know the week."
SHEETS = [
 dict(c="F0", w=1, title="The maths you actually need",
      draw="A number line, an x&ndash;y grid with one straight line on it, and a right-angled "
           "triangle with sides 3 and 4.",
      items=["f(x) = wx + b &mdash; label w as the steepness and b as the starting height",
             "slope = rise &divide; run, with an actual rise and run marked on your line",
             "the derivative as the slope of the tangent at one point &mdash; draw the tangent",
             "&Sigma; written out longhand: &Sigma;&#8321;&#8308; x&#7522; = x&#8321; + x&#8322; + x&#8323; + x&#8324;",
             "a vector as an arrow from the origin, and &#8214;x&#8214; = &radic;(3&sup2; + 4&sup2;) = 5",
             "a 2&times;3 matrix, with the shape written under it as (2, 3)",
             "the bell curve, with &mu; at the peak and &sigma; marked either side"],
      test="Cover it. Can you say what the derivative of x&sup2; is, and <i>why</i> the answer "
           "is a formula rather than a number?"),
 dict(c="F0", w=2, title="Python, NumPy and pandas",
      draw="A grid of boxes labelled (m, n), with an arrow down the columns marked "
           "<b>axis=0</b> and an arrow across the rows marked <b>axis=1</b>.",
      items=["the four shapes: (3,) &nbsp; (1, 3) &nbsp; (3, 1) &nbsp; (3, 2) &mdash; and a sketch of each",
             "broadcasting: (2, 3) + (3,) drawn as the small one stretched down",
             "A @ w + b with the shapes written above each part",
             "a list times 2 next to an array times 2, and the two different answers",
             "the axis rule: <i>the axis you name is the one that disappears</i>"],
      test="Predict, without running it: <code>np.array([[1,2],[3,4]]).sum(axis=0)</code>."),
 dict(c="C1", w=1, title="Regression, cost and gradient descent",
      draw="Two pictures side by side: scattered dots with a line through them, and a "
           "<b>bowl</b> with a ball part-way down one side.",
      items=["f(x) = wx + b on the dots picture",
             "J(w, b) = (1/2m) &Sigma; (f &minus; y)&sup2; on the bowl picture",
             "the update rule, twice: w := w &minus; &alpha;&thinsp;&part;J/&part;w and the same for b",
             "the word <b>simultaneously</b>, circled",
             "three arrows on the bowl: too small &alpha;, right &alpha;, too big &alpha; overshooting"],
      test="Why does the step get smaller near the bottom when &alpha; never changed?"),
 dict(c="C1", w=2, title="Many features, scaling and curves",
      draw="Two contour plots: one a long thin valley, one round. Label them "
           "<b>before scaling</b> and <b>after scaling</b>.",
      items=["X (m, n) &middot; w (n,) &middot; b scalar &middot; predictions (m,) &mdash; the five shapes",
             "z-score: x&prime; = (x &minus; &mu;) &divide; &sigma;",
             "the zig-zag path across the thin valley, and the straight path across the round one",
             "&part;J/&part;w&#11388; = (1/m) &Sigma; (f &minus; y) x&#11388; &mdash; ring the x&#11388; and note it is why scaling matters",
             "a J-against-iteration curve for each: falling, flat, rising, zig-zag"],
      test="&mu; and &sigma; came from training. What must you do with them at prediction time, "
           "and what happens if you don't?"),
 dict(c="C1", w=3, title="Classification, loss and regularization",
      draw="The <b>S-curve</b> of the sigmoid, with 0.5 marked on the y-axis and a dashed "
           "line down to z = 0.",
      items=["g(z) = 1 &divide; (1 + e^&minus;z), and g(0) = 0.5",
             "the boundary is where <b>z = 0</b>, not where x = 0",
             "the two loss curves: &minus;log(f) for y = 1, and &minus;log(1 &minus; f) for y = 0",
             "a lumpy surface next to a bowl &mdash; squared error vs log loss",
             "the penalty (&lambda;/2m) &Sigma; w&#11388;&sup2;, with a note that <b>b is not in it</b>",
             "the decay form: w := w(1 &minus; &alpha;&lambda;/m) &minus; &alpha;&thinsp;&middot;&thinsp;gradient"],
      test="Draw an overfitted boundary and a regularized one on the same scattered dots."),
 dict(c="C2", w=1, title="Neurons, layers and forward propagation",
      draw="Four circles in a column, three in the next, one at the end, with every "
           "circle joined to every circle in the next column.",
      items=["one neuron: a = g(w &middot; x + b), written inside a circle",
             "the shapes above each gap: (4, 5) then (5, 3) then (3, 1)",
             "the parameter count under each: 4&times;5+5, 5&times;3+3, 3&times;1+1",
             "A_in @ W + b for a whole batch, with (m, n_in) @ (n_in, n_out)",
             "the collapse: two linear layers = W&#8322;W&#8321;x + &hellip; = one layer"],
      test="Why does removing every activation function make depth worthless? Write the "
           "two lines of algebra."),
 dict(c="C2", w=2, title="Training, activations and softmax",
      draw="A small computation graph &mdash; four boxes joined by arrows &mdash; with a number "
           "on each arrow, and the numbers multiplied along the path.",
      items=["the three Keras lines, and which of the three steps each one is",
             "ReLU drawn: flat, then a 45&deg; line",
             "the sigmoid drawn beside it, flat at <b>both</b> ends &mdash; ring both flat parts",
             "softmax: e^z divided by the sum of e^z, summing to 1",
             "the chain rule as a product of the numbers on your arrows",
             "&part;J/&part;z&#8322; = (a &minus; y)/m &mdash; and the note that the ugly parts cancelled"],
      test="Why does a linear output layer plus <code>from_logits=True</code> beat a softmax "
           "output layer?"),
 dict(c="C2", w=3, title="Diagnosing models",
      draw="Two curves converging as the training set grows, and a <b>U</b> shape with "
           "&lambda; along the bottom.",
      items=["J<sub>train</sub> and J<sub>cv</sub> on the learning curve, with the gap labelled <b>variance</b>",
             "the distance from J<sub>train</sub> down to the baseline, labelled <b>bias</b>",
             "the U: high on the left from variance, high on the right from bias",
             "the six fixes sorted into two columns, bias and variance",
             "a 2&times;2 confusion matrix with precision and recall written as arrows across it",
             "F1 = 2PR &divide; (P + R)"],
      test="Both curves flat and close, both high. Does more data help? Say why in one "
           "sentence."),
 dict(c="C2", w=4, title="Decision trees and ensembles",
      draw="The cat tree: <b>ear shape?</b> at the top, two branches, then a question on "
           "each, then four leaves.",
      items=["H(p) sketched as a hill, peaking at p = 0.5 and zero at both ends",
             "gain = H(parent) &minus; [ w&#8343;H(left) + w&#8341;H(right) ], with the weights ringed",
             "the three gains: 0.28, 0.03, 0.12 &mdash; and which one wins",
             "the four leaves with their counts: 4/4, 0/1, 1/1, 0/4",
             "bagging as many trees voting; boosting as trees in a row, each fixing the last"],
      test="What stops a tree splitting forever, and what happens if nothing does?"),
 dict(c="C3", w=1, title="Clustering and anomaly detection",
      draw="Six dots with two crosses among them, and arrows from each dot to its "
           "nearer cross.",
      items=["the two steps, as a cycle with two arrows: <b>assign</b> then <b>move</b>",
             "J as the mean squared distance to your own centroid",
             "two different converged answers on the same dots &mdash; label them 1.78 and 1.31",
             "the bell curve with &mu; and &sigma;&sup2; fitted to a column of numbers",
             "p(x) = p&#8321; &times; p&#8322; &times; &hellip; and the threshold &epsilon; drawn as a cut-off"],
      test="Why can you never choose k by making J as small as possible?"),
 dict(c="C3", w=2, title="Recommenders and PCA",
      draw="A grid of films by users, most cells empty, and beside it a tilted cloud of "
           "dots with one line drawn through its long axis.",
      items=["prediction = w&#8317;&#690;&#8318; &middot; x&#8317;&#8305;&#8318; + b&#8317;&#690;&#8318;, with a note that <b>both</b> w and x are learned",
             "r(i,j) drawn as a mask over the grid &mdash; and why 'not rated' &ne; 'rated 0'",
             "mean normalisation: subtract the row mean, add it back at prediction",
             "a new user with no ratings, predicted the film average rather than zero",
             "z = x &middot; u drawn as a shadow dropping onto the line"],
      test="Eve has rated nothing. What does she learn for w, and why does mean "
           "normalisation rescue her?"),
 dict(c="C3", w=3, title="Reinforcement learning",
      draw="Six boxes in a row, 100 at the left end and 40 at the right, with an arrow "
           "under each showing which way to go.",
      items=["the return: R&#8321; + &gamma;R&#8322; + &gamma;&sup2;R&#8323; + &hellip;, with &gamma; = 0.5 filled in",
             "from state 4: left = 100&gamma;&sup3; = 12.5 against right = 40&gamma;&sup2; = 10",
             "V* = [100, 50, 25, 12.5, 20, 40] written under your six boxes",
             "the policy arrows: &larr; &larr; &larr; &rarr;",
             "Bellman: Q(s,a) = R(s) + &gamma; max Q(s&prime;, a&prime;)",
             "&epsilon;-greedy as a coin flip before each move"],
      test="At which &gamma; does state 4 change its mind, and why is that the answer?"),

 dict(c="C4", w=1, title="Sequences and embeddings",
      draw="Two rows of word-boxes for the two sentences, and under both the SAME bag of counts.",
      items=["the bag: {the: 2, bit: 1, dog: 1, man: 1} &mdash; written once, for both sentences",
             "one-hot: a row of 0s with one 1, and <i>every pair dots to 0</i> beside it",
             "the embedding table E, V rows by d columns, with one row ringed as a lookup",
             "cos = a&middot;b / (&#8214;a&#8214;&#8214;b&#8214;), and [3,4]&middot;[4,3] = 24/25 = 0.96",
             "the RNN loop: h&lt;t&gt; = g(W&#8341;h&lt;t&minus;1&gt; + W&#8339;x&lt;t&gt; + b)",
             "0.4&#185;&#8309; = 1.1 &times; 10&#8315;&#8310; under an arrow spanning 15 steps"],
      test="Name the two RNN failures, and say which one an LSTM fixes and which it cannot."),

 dict(c="C4", w=2, title="Attention",
      draw="A 3&times;3 grid, rows labelled q&#8321;q&#8322;q&#8323;, columns k&#8321;k&#8322;k&#8323;, "
           "with an arrow off each row marked <i>sums to 1</i>.",
      items=["softmax(QK&#7488; / &#8730;d&#8342;)V &mdash; written out once from memory",
             "Q = XW&#7476;, K = XW&#7472;, V = XW&#7515; &mdash; three roles, one input",
             "the four steps down the page: score &rarr; scale &rarr; softmax &rarr; mix",
             "row 1 of the worked example: [0.4011, 0.1978, 0.4011]",
             "&#8730;512 = 22.6 beside the words <i>why we divide</i>",
             "the causal mask: a triangle of &minus;&infin; in the upper right"],
      test="Why must the softmax be applied along rows, and what happens silently if it is not?"),

 dict(c="C4", w=3, title="The transformer block",
      draw="A vertical strip: two boxes on a line, each with a curved arrow leaving before it and "
           "rejoining after it.",
      items=["x = x + attention(layer_norm(x))",
             "x = x + feed_forward(layer_norm(x))",
             "&part;y/&part;x = 1 + f&prime;(x), with the 1 ringed",
             "LN: (x &minus; &mu;)/&sigma;, and [1,3,5,7] &rarr; [&minus;1.34, &minus;0.45, 0.45, 1.34]",
             "block params: attention 4d&sup2;, feed-forward 8d&sup2; &mdash; <i>twice</i>",
             "GPT-2 small: 124 M, added up in four lines"],
      test="Which single step in the block lets information move between positions?"),

 dict(c="C4", w=4, title="Language models",
      draw="A sentence with the last word covered, an arrow to a bar chart of candidate tokens, "
           "and a dial marked T beside it.",
      items=["L = &minus;&Sigma; log P(x&#8348; | x&#8249;&#8348;) &mdash; cross-entropy, again",
             "perplexity = e to the loss, and p = 0.2 &rarr; ppl 5",
             "p = softmax(logits / T), with T = 0.5 and T = 2 side by side",
             "the three stages: pretrain &rarr; SFT &rarr; RLHF",
             "two costs: compute O(T&sup2;), KV cache O(T)",
             "three failures and their causes, in two columns"],
      test="Give the mechanical account of what a model computes &mdash; and say where it stops."),

 dict(c="F0", w=3, title="The maths behind the curtain",
      draw="A vector and its image under a matrix, with the two directions that do not turn drawn "
           "as dashed lines through the origin.",
      items=["Av = &lambda;v, and A[1,1] = [3,3] worked underneath it",
             "the covariance eigenvalues 4.976 and 0.064, with 98.7% ringed",
             "A = U&Sigma;V&#7488; &mdash; rotate, stretch, rotate",
             "L(p) = p&#8311;(1&minus;p)&sup3; with a curve peaking at 0.7",
             "&minus;log of it &rarr; &minus;y log f &minus; (1&minus;y) log(1&minus;f)",
             "&part;L/&part;z = p &minus; y, with [0.6285, 0.2312, 0.1402] &minus; [1,0,0] under it"],
      test="Which noise assumption gives you squared error, and which gives cross-entropy?"),
]

# ---------------------------------------------------------- per-card prompts
# what to put on paper, by the kind of thing the card is
BY_KIND = {
 "formula":    "Write it from memory, then draw a line from every symbol out to a word "
               "saying what that symbol does. Then sketch the shape it makes.",
 "algorithm":  "Draw it as a cycle: boxes for the steps, arrows for the order, and mark "
               "where it stops. Then run it once on two data points.",
 "concept":    "One picture, no words. Then add labels. Then write the single sentence you "
               "would say to explain it to someone else.",
 "distinguish":"Two columns, side by side. One line in each. Then write underneath the "
               "<b>question</b> that tells you which one you are looking at.",
 "trap":       "Write the wrong version and the right version one above the other, and "
               "circle the difference. Add a note saying what it costs you.",
 "number":     "Write the number big in the middle of a space, and draw three arrows out "
               "to what it lets you conclude.",
 "code":       "Write the line out, then put the <b>shape</b> above every array in it. "
               "Then say aloud what each line does before you read the next.",
}


# Bespoke prompts for the cards where one particular drawing is obviously the
# right one. Everything else falls back to BY_KIND above.
SCRIBBLE = {
 # ---- Foundations
 "f0-slope": "Draw one line on a grid. Mark an actual rise and an actual run on it with two "
             "little brackets, and write the division. Then draw a second line twice as steep.",
 "f0-derivative": "Draw a curve. Touch a straight line against it at one point. That line's "
                  "slope is the derivative there &mdash; write it next to the touch point. Move "
                  "the touch point and draw a second, flatter one.",
 "f0-partial": "Draw a hill in 3-D, badly. Slice it once north&ndash;south and once east&ndash;west. "
               "Each slice is a partial: label which letter you froze for each.",
 "f0-sigma": "Write &Sigma; once, then immediately write the same thing longhand with plus "
             "signs. Do it for four terms. The longhand version is the one to remember.",
 "f0-vector-length": "Draw the arrow to (3, 4). Complete the right-angled triangle underneath "
                     "it. Write 3&sup2; + 4&sup2; = 25 along the sides and &radic;25 = 5 on the arrow.",
 "f0-dot": "Draw two arrows from the same origin, once nearly aligned and once at right "
           "angles. Write the sign of the dot product beside each. Then a third pair pointing "
           "apart, and write a negative sign.",
 "f0-shape-rule": "Write (2,&nbsp;3) and (3,&nbsp;4) side by side. Ring the two inner numbers "
                  "and join them with a line saying <i>must match</i>. Ring the outer two and "
                  "write the answer's shape.",
 "f0-transpose": "Draw a 2&times;3 grid of boxes with numbers in. Draw it again tipped on its "
                 "side. Write (2, 3) under the first and (3, 2) under the second.",
 "f0-exp": "Draw e^x rising off the top of the page and e^&minus;x falling towards zero without "
           "touching it. Mark the point where both pass through 1.",
 "f0-log": "Draw log(x). Mark that it is 0 at x = 1 and plunges as x nears 0. Write beside "
           "the plunge: <i>this is what punishes a confident wrong answer</i>.",
 "f0-broadcast": "Draw a (2,&nbsp;3) block and a (3,) strip. Draw the strip copied down to "
                 "make a second row. Then draw (3,) meeting (3,&nbsp;1) and the 3&times;3 that "
                 "silently appears.",
 "f0-axis": "Draw a grid. One arrow down through the rows labelled axis=0, one across labelled "
            "axis=1. Write beside each: <i>the axis you name disappears</i>.",
 "f0-normal": "Draw the bell. Mark &mu; at the peak. Mark &mu;&nbsp;&plusmn;&nbsp;&sigma; and shade "
              "it 68%. Mark &plusmn;2&sigma; and shade 95%.",

 # ---- C1
 "c1w1-model": "Draw the dots and one line through them. Write f(x) = wx + b on the line, with "
               "an arrow from w to the steepness and from b to where the line crosses.",
 "c1w1-cost": "Draw the dots and the line, then draw a short vertical stick from each dot to "
              "the line. Write: <i>square each stick, add them, halve the average</i>.",
 "c1w1-cost-shape": "Draw the bowl. Put a ball on the side. Write J up the vertical axis and w "
                    "along the bottom. Mark the single bottom point and label it <i>the best w</i>.",
 "c1w1-contour": "Draw three nested rings. Write <i>same cost everywhere on one ring</i> beside "
                 "them. Put a dot outside and an arrow from it heading straight across the rings.",
 "c1w1-gd-update": "Write both update lines one under the other. Draw a box around them both "
                   "and write <b>simultaneously</b> across the box.",
 "c1w1-alpha": "Draw four little J-against-iteration curves in a row: smooth fall, slow crawl, "
               "zig-zag, and one shooting upward. Label each with what to do about it.",
 "c1w2-scaling-why": "Draw a long thin valley of contours with a zig-zag path across it. Beside "
                     "it draw round contours with a straight path. Label them before and after.",
 "c1w2-scaling-how": "Three short rows: max scaling, mean normalisation, z-score. Write each as "
                     "<i>subtract something, divide by something</i>, and fill in the somethings.",
 "c1w3-sigmoid": "Draw the S. Mark 0.5 where it crosses the vertical axis. Drop a dashed line to "
                 "z = 0 and write <i>the boundary lives here</i>.",
 "c1w3-logloss": "Draw two curves: &minus;log(f) plunging from the right, and &minus;log(1&nbsp;&minus;&nbsp;f) "
                 "plunging from the left. Mark that both go to infinity at the wrong end.",
 "c1w3-boundary": "Draw scattered dots of two colours with a straight line between them. Write "
                  "z = 0 along the line, not on the axes.",
 "c1w3-regcost": "Write the cost in two halves with a big <b>+</b> between them. Label the left "
                 "<i>fit the data</i> and the right <i>stay small</i>. Ring the &lambda; and draw "
                 "arrows for what happens as it grows and shrinks.",
 "c1w3-weight-decay": "Write w := 0.9999&nbsp;w &minus; &alpha;(gradient). Ring the 0.9999 and write "
                      "<i>shrink first, then step</i> beside it.",

 # ---- C2
 "c2w1-neuron": "Draw a circle. Arrows in from three inputs, one arrow out. Write w&nbsp;&middot;&nbsp;x&nbsp;+&nbsp;b "
                "inside it and g( ) wrapped round the outside.",
 "c2w1-master-eq": "Draw two columns of circles joined by every possible line. Write the equation "
                   "under it, then draw an arrow from each superscript and subscript to what it "
                   "points at in the picture.",
 "c2w1-params": "Draw a layer with n arrows in and p circles. Write n&times;p for the lines and "
                "+p for the circles, then add them.",
 "c2w1-matmul-rule": "Write the two shapes with the inner pair ringed and joined. Do it three "
                     "times with different numbers, one of them illegal.",
 "c2w2-softmax": "Write four logits in a row. Under each write e^z. Draw a bracket under all "
                 "four to the sum, then arrows back up showing each divided by it.",
 "c2w2-relu": "Draw ReLU: flat, then a 45&deg; line. Beside it draw the sigmoid, and shade the "
              "two flat ends. Write <i>no gradient here</i> in both shaded parts.",
 "c2w2-chain-rule": "Draw four boxes in a row with an arrow between each. Put a number on every "
               "arrow. Multiply them along the row and ring the answer.",
 "c2w3-diagnostic": "Draw two curves converging as the training set grows. Mark the gap "
                       "between them <b>variance</b> and the drop from the lower one to the "
                       "baseline <b>bias</b>.",
 "c2w3-fix-table": "Two columns headed <i>high bias</i> and <i>high variance</i>. Write the "
                   "six fixes into them from memory. Then draw the U underneath with &lambda; "
                   "along the bottom and mark which wall each column belongs to.",
 "c2w3-f1": "Draw two bars, 0.9 and 0.1. Beside them draw the arithmetic mean at 0.5 and the "
            "harmonic at 0.18. Write <i>it follows the smaller one</i>.",
 "c2w4-entropy": "Draw H(p) as a hill: zero at 0, peak at 0.5, zero at 1. Mark where a pure "
                 "node sits and where a 50/50 node sits.",
 "c2w4-infogain": "Draw the parent node with its entropy, two children with theirs, and write "
                  "the branch sizes as fractions in front of each child. Ring the fractions.",
 "c2w4-tree-decisions": "Draw the cat tree: ear shape at the top, two branches, a question on each, four "
              "leaves with their counts.",

 # ---- C3
 "c3w1-kmeans-steps": "Draw six dots and two crosses. Arrow from each dot to its nearer cross. Then "
                "draw the crosses moved to the middle of their group. Two steps, two pictures.",
 "c3w1-anomaly": "Draw two bell curves, one per feature, with a point marked on each. Multiply "
                 "the two heights and compare the result against a line marked &epsilon;.",
 "c3w2-collab": "Draw the film-by-user grid with most cells empty. Write w&nbsp;&middot;&nbsp;x in one "
                "filled cell, and ring both w and x with a note: <i>both of these are unknown</i>.",
 "c3w2-pca": "Draw a tilted cloud of dots. Draw the long axis through it. Drop one dot's "
             "perpendicular onto that axis and mark the distance along it as z.",
 "c3w3-return": "Draw six boxes with 100 at one end and 40 at the other. Write the discounted "
                "sum under a path going each way and ring the bigger one.",
 "c3w3-bellman": "Write Q(s,a) = R(s) + &gamma;&thinsp;max&thinsp;Q(s&prime;,a&prime;). Draw an arrow from "
                 "R(s) to <i>now</i> and from the max to <i>everything after</i>.",
}


# ---------------------------------------------------- Foundations, per lesson
# One thing to put on paper for each Foundations concept, keyed by lesson slug.
FOUNDATION = {
 # --- W1, the maths
 "01-what-is-a-function": "Draw a box with an arrow in and an arrow out. Write x on the way "
   "in, f(x) on the way out, and the rule inside the box. Feed it three different numbers "
   "and write all three answers.",
 "02-reading-a-graph": "Draw the axes and label what each one measures &mdash; in words, not "
   "letters. Put one point on it and write its two coordinates in brackets beside it.",
 "03-greek-letters": "Write out the eight you will actually meet, one per line: &alpha; &beta; "
   "&gamma; &epsilon; &theta; &lambda; &mu; &sigma;. Beside each write how you <b>say</b> it, then "
   "what it usually means here. Say them aloud as you write.",
 "04-slope": "Draw one line. Mark a rise and a run on it with brackets and divide. Then draw a "
   "steeper line and a downhill line beside it, and write the sign of each slope.",
 "05-derivatives": "Draw a curve. Rest a straight line against it at one point. Write the slope "
   "of that line beside the touch point. Slide the touch point and draw a second one, flatter.",
 "06-partial-derivatives": "Draw a hill. Slice it one way, then the other. Label each slice with "
   "the letter you held still. Write &part;f/&part;w beside the slice where b was frozen.",
 "07-sigma-notation": "Write &Sigma;&#8321;&#8308;&nbsp;x&#7522; on one line and x&#8321;&nbsp;+&nbsp;x&#8322;&nbsp;+&nbsp;x&#8323;&nbsp;+&nbsp;x&#8324; "
   "directly underneath. Join them with an equals sign. Do it once more with a squared term inside.",
 "08-pi-notation": "Write &Pi; with four terms and the multiplication written out underneath. "
   "Then write log of the same product turning into a sum, which is why code prefers logs.",
 "09-vectors": "Draw the arrow to (3,&nbsp;4) from the origin. Complete the right-angled triangle. "
   "Write 3&sup2;&nbsp;+&nbsp;4&sup2;&nbsp;=&nbsp;25 along the sides and 5 on the arrow itself.",
 "10-dot-product": "Two arrows from one origin: nearly aligned, then square, then opposed. Write "
   "the sign of the dot product under each of the three.",
 "11-matrices": "Draw a grid of empty boxes, 2 by 3. Write (2,&nbsp;3) underneath it. Then draw "
   "(3,&nbsp;2) beside it so the difference is in front of you.",
 "12-matrix-multiplication": "Write the two shapes with the inner numbers ringed and joined by a "
   "line. Then do one 2&times;2 by hand, drawing an arrow from the row and the column into each answer cell.",
 "13-transpose": "Draw a 2&times;3 grid with numbers in. Draw it tipped on its side. Trace one "
   "number from its old position to its new one with an arrow.",
 "14-exponentials": "Draw e^x shooting up and e^&minus;x falling towards zero without touching. "
   "Mark where both cross 1. Beside it write e&nbsp;&asymp;&nbsp;2.718.",
 "15-logarithms": "Draw log(x): zero at 1, plunging as x approaches 0. Write beside the plunge "
   "<i>this is the punishment for being confidently wrong</i>.",
 "16-probability": "Draw a box split into two parts, 0.8 and 0.2, and write that they add to 1. "
   "Beside it write 0.8&nbsp;&times;&nbsp;0.8 for two independent events, and the answer.",
 "17-mean-variance": "Write eight numbers in a row. Mark the mean with a vertical line. Draw a "
   "bracket from each number to that line, square them, average them. That is the variance.",
 "18-normal-distribution": "Draw the bell. Mark &mu; at the peak, shade &plusmn;1&sigma; and write "
   "68%, then &plusmn;2&sigma; and write 95%. Put one point far out and write <i>unlikely</i>.",
 "19-min-max-argmax": "Write four numbers in a row with their positions 0, 1, 2, 3 underneath. "
   "Ring the biggest <b>value</b> and label it max. Ring its <b>position</b> and label it argmax.",
 # --- W2, Python
 "01-jupyter": "Draw two stacked cells, one markdown and one code, with an arrow marked "
   "Shift+Enter. Write beside it: <i>they share one memory, so order matters</i>.",
 "02-types": "Write the four types down the page with one example each. Beside each write what "
   "breaks if you get it wrong.",
 "03-lists-vs-arrays": "Write <code>[1,2,3] * 2</code> and <code>np.array([1,2,3]) * 2</code> one "
   "above the other, and their two different answers beside them. Ring the difference.",
 "04-indexing-slicing": "Draw five boxes with the numbers in and the indices 0&ndash;4 underneath. "
   "Then bracket x[1:4] and shade exactly which boxes it takes.",
 "05-shape-and-axis": "Draw a grid. Arrow down through the rows marked axis=0, arrow across "
   "marked axis=1. Write <i>the axis you name disappears</i> beneath both.",
 "06-creating-arrays": "Four short lines: zeros, ones, arange, linspace. Beside arange and "
   "linspace write which one includes its endpoint.",
 "07-elementwise": "Two rows of boxes stacked, with a line joining each pair and the operation "
   "between. Write <i>same shape in, same shape out</i>.",
 "08-broadcasting": "Draw (2,&nbsp;3) and (3,) right-aligned, with the strip copied down to make "
   "the second row. Then draw (3,) meeting (3,&nbsp;1) and the surprise 3&times;3 it makes.",
 "09-dot-in-code": "Write <code>w * x</code> and <code>w @ x</code> one above the other with "
   "their answers. Ring which one is a single number.",
 "10-aggregations": "One small grid, three answers around it: no axis, axis=0, axis=1. Write the "
   "shape of each answer beside it.",
 "11-boolean-masks": "Write four numbers, then True/False under each, then 1/0 under those. "
   "Draw an arrow to the sum and write <i>this is how you count correct predictions</i>.",
 "12-reshape": "Write 0&ndash;5 in a row, then boxed as 2&times;3, then as 3&times;2, then as a "
   "column. Write reshape(-1,&nbsp;1) beside the column and <i>you work out the rows</i>.",
 "13-pandas-dataframes": "Draw a small table with column names along the top and a row index "
   "down the side. Ring the labels and write <i>this is what NumPy does not have</i>.",
 "14-pandas-to-numpy": "Draw the labelled table, an arrow marked .to_numpy(), and the bare grid "
   "it becomes. Write <i>the labels are gone from here on</i>.",
 "15-reading-errors": "Write a shape error out by hand: (100,&nbsp;4) and (3,). Right-align them, "
   "ring 4 and 3, and write the fix &mdash; <code>w = np.zeros(X.shape[1])</code> &mdash; underneath.",
 "16-functions": "Write <code>def predict(X, w, b):</code> and the one line inside it. Put the "
   "shape above every name in that line, and the returned shape at the end.",
}
