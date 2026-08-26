# -*- coding: utf-8 -*-
"""C2 · Week 1 — Neural networks and forward propagation."""
from kit import (kid, key, warn, trap, note, card, eq, eqp, decode, table, demo,
                 quiz, links, code, h2, grid2, grid3, pretest)

L = []

# ============================================================ 1
L.append(dict(
    slug="01-neurons-and-the-brain", title="Neurons and the brain", mins=9, tag="intuition",
    lede="Where the name came from, why the brain analogy is much looser than the marketing suggests, "
         "and why a 1950s idea suddenly started working in 2012.",
    body=(
        pretest("""<p>An artificial neuron is often compared to a brain cell. <b>Guess how much of that comparison is real</b> — and what one artificial neuron actually computes, in two steps.</p>""",
        """<p>Watch for the two steps: a weighted sum, then a squash. Watch also for how loose the biological analogy really is.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Imagine a kid in a group project. Three friends shout opinions at her. She doesn’t
treat them equally: she <b>trusts</b> Ana a lot, trusts Ben a little, and actively distrusts Chris.
So she adds up their opinions with those trust levels, adds her own stubborn starting mood,
and if the total is convincing enough, she shouts <b>“yes!”</b> to the next kid along.</p>
<p>That’s a neuron. The trust levels are called <b>weights</b>. Her stubborn starting mood is called the
<b>bias</b>. Shouting “yes” more or less loudly is called the <b>activation</b>. A neural network is just
a whole classroom of these kids, arranged in rows, each row shouting to the next.</p>""")
        + """<p>The name is borrowed from biology, but it is borrowed <em>very</em> loosely. A real
neuron is a living cell with chemistry, timing, and thousands of connections that we still do not fully
understand. The artificial version is three lines of arithmetic. Andrew Ng is blunt about this in the
video, and it is worth taking seriously: <b>we are not simulating brains.</b> We took one cartoon of one
idea from neuroscience in the 1950s and it turned out to be a genuinely useful piece of maths.</p>"""

        + h2("🔢", "The maths, decoded")
        + """<p>One artificial neuron does exactly two things. Step one: a weighted sum. Step two: squash it.</p>"""
        + eq("""<var>z</var> <span class="op">=</span> <var class="hl-b">w</var><sub>1</sub><var>x</var><sub>1</sub>
<span class="op">+</span> <var class="hl-b">w</var><sub>2</sub><var>x</var><sub>2</sub>
<span class="op">+</span> <var class="hl-b">w</var><sub>3</sub><var>x</var><sub>3</sub>
<span class="op">+</span> <var class="hl-a">b</var>""", "step 1 — add up what you heard")
        + eqp([
            ('<var>a</var> <span class="op">=</span> <var class="hl-g">g</var><span class="paren">(</span><var>z</var><span class="paren">)</span> <span class="op">=</span> <span class="frac"><span>1</span><span>1 + <var>e</var><sup>−<var>z</var></sup></span></span>',
             "sigmoid-squash", "the squasher"),
        ], "step 2 — squash it into 0…1 — click it")
        + decode([
            ("<var>x</var>", "“the inputs”", "The numbers coming in — price, temperature, a pixel’s brightness. Whatever you measured."),
            ("<var>w</var>", "“the weights”", "How much this neuron trusts each input. Big positive = strong evidence for. Negative = evidence against. These are <b>learned</b>."),
            ("<var>b</var>", "“the bias”", "A constant added no matter what. It shifts how easily the neuron fires — its default mood. Also learned."),
            ("<var>z</var>", "“zee”", "The raw total. Any number at all: −57, 0.3, 900."),
            ("<var>g</var>", "“the activation function”", "The squasher. Here, sigmoid: it maps any number into the range 0 to 1."),
            ("<var>a</var>", "“the activation”", "What the neuron outputs and passes along. With sigmoid, you can read it as a probability."),
        ])
        + note("""<p>Compare that to Course 1. Logistic regression was <var>f</var>(<var>x</var>) =
<var>g</var>(<var>w</var>·<var>x</var> + <var>b</var>). <b>Identical.</b> One artificial neuron
<em>is</em> one logistic regression unit. A neural network is many of them wired together so that later
ones can use earlier ones’ answers as their inputs.</p>""", "You have already built one of these")

        + h2("🎬", "Watch it move")
        + demo("bio-vs-artificial", "Biological neuron vs. our maths copy",
               "signals arrive → get weighted → get summed → the neuron fires")

        + h2("🕰", "Why now, and not in 1985?")
        + """<p>The equations above are from 1958. Backpropagation, the training method, is from 1986.
Nothing about the maths changed. Three other things did:</p>"""
        + grid3(
            card("<h3>Data</h3><p>The internet gave us millions of labelled examples. In 1990 a big dataset "
                 "was a few thousand rows.</p>"),
            card("<h3>Compute</h3><p>GPUs made the matrix multiplications in Lesson 15 roughly a hundred "
                 "times cheaper.</p>"),
            card("<h3>Scale behaviour</h3><p>Classical algorithms flatten out as you add data. Big neural "
                 "networks keep improving. That was the surprise.</p>"))
        + """<p>The chart Andrew draws — performance versus amount of data, with traditional algorithms
plateauing and larger neural networks climbing past them — is the single most important business argument
in the course. It is why “just get more data and a bigger model” became a strategy.</p>"""

        + h2("🕳", "Traps")
        + trap("""<p><b>“It works like the brain.”</b> It doesn’t. It is inspired by a 1943 cartoon of a
brain cell. Saying this in an interview is a red flag; saying “it’s a stack of logistic regressions with
learned features” is a green one.</p>""")
        + trap("""<p><b>Confusing weights with inputs.</b> Inputs change with every example. Weights stay
put and change only during training. If you mix these up, nothing later in the course will make sense.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("A neuron has weights [2, −1] and bias 0.5. The input is [1, 3]. What is z, and roughly what is a?",
             "<p>z = 2(1) + (−1)(3) + 0.5 = <b>−0.5</b>. Sigmoid of −0.5 ≈ <b>0.38</b>. Below 0.5, so this "
             "neuron is leaning “no”.</p>"),
            ("Which of w, b, x change while the model is being trained?",
             "<p><b>w and b</b> change — they are the parameters the learning algorithm adjusts. "
             "<b>x</b> never changes; it is your data.</p>"),
            ("Why did neural networks take off in the 2010s rather than the 1990s?",
             "<p>Data and compute, not new maths. Plus the empirical finding that large networks keep "
             "getting better with more data while classical methods plateau.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("paper", "https://link.springer.com/article/10.1007/BF02478259",
             "McCulloch & Pitts (1943) — A logical calculus of the ideas immanent in nervous activity",
             "The original paper that modelled a neuron as a threshold unit. Dense, but this is where the idea starts."),
            ("paper", "https://psycnet.apa.org/record/1959-09865-001",
             "Rosenblatt (1958) — The Perceptron",
             "The first learning rule for these units, and the start of the first AI hype cycle."),
            ("paper", "https://www.nature.com/articles/323533a0",
             "Rumelhart, Hinton & Williams (1986) — Learning representations by back-propagating errors",
             "The training algorithm that made multi-layer networks possible. You’ll meet it properly in Week 2."),
            ("paper", "https://papers.nips.cc/paper/4824-imagenet-classification-with-deep-convolutional-neural-networks",
             "Krizhevsky, Sutskever & Hinton (2012) — AlexNet",
             "The result that convinced everyone. Same old maths, far more data and two GPUs."),
            ("video", "https://www.3blue1brown.com/lessons/neural-networks",
             "3Blue1Brown — But what is a neural network?",
             "Nineteen minutes. If you watch one extra thing this week, watch this."),
        ])
    )))

# ============================================================ 2
L.append(dict(
    slug="02-demand-prediction", title="Demand prediction", mins=11, tag="intuition",
    lede="The t-shirt example. This is the lesson where “hidden layer” stops being a scary phrase and "
         "starts meaning something concrete: features the network invents for itself.",
    body=(
        pretest("""<p>Price, shipping, marketing, material → will this T-shirt sell? <b>Guess why you would put a layer of neurons in the middle rather than going straight from the four inputs to the answer.</b></p>""",
        """<p>Watch for what the middle layer invents. Nobody tells it to compute “affordability” — it finds something like that because it helps.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>You want to guess if a t-shirt will be a hit. You could stare at the price, the postage,
the advert budget and the fabric all at once — messy. Instead you ask three simpler questions first:</p>
<ul><li>Can people <b>afford</b> it? (that’s mostly price + postage)</li>
<li>Have people <b>heard</b> of it? (that’s advertising)</li>
<li>Does it <b>feel</b> expensive-good? (that’s fabric, and oddly, price again)</li></ul>
<p>Answer those three little questions first, then answer the big question using only those three answers.
The three little questions are the <b>hidden layer</b>. The big question is the <b>output layer</b>.</p>""")
        + """<p>The important twist: <b>you never tell the network what the three questions are.</b> You
tell it “make three numbers”, and training decides what they should mean. “Affordability” is a story we
tell afterwards, because it makes the picture teachable. The real learned features are usually weirder and
harder to name — and that is fine.</p>"""

        + h2("🔢", "The maths, decoded")
        + """<p>Four inputs, three hidden units, one output. Every hidden unit sees <b>all four</b> inputs;
the output unit sees <b>all three</b> hidden activations.</p>"""
        + eqp([
            '<var class="hl-p">a</var><sup>[1]</sup> <span class="op">=</span> <span class="paren">[</span> <var>a</var><sub>1</sub><sup>[1]</sup>, <var>a</var><sub>2</sub><sup>[1]</sup>, <var>a</var><sub>3</sub><sup>[1]</sup> <span class="paren">]</span> <span class="op">where</span> <var>a</var><sub><var>j</var></sub><sup>[1]</sup> <span class="op">=</span> <var>g</var><span class="paren">(</span>',
            ('<var class="hl-b">w</var><sub><var>j</var></sub><sup>[1]</sup> · <var>x</var>', "dot-product-f0", "multiply matching entries, add them up"),
            ' <span class="op">+</span> <var class="hl-a">b</var><sub><var>j</var></sub><sup>[1]</sup><span class="paren">)</span>',
        ], "hidden layer — three little questions — click a part")
        + eqp([
            '<var class="hl-g">a</var><sup>[2]</sup> <span class="op">=</span> <var>g</var><span class="paren">(</span>',
            ('<var class="hl-b">w</var><sub>1</sub><sup>[2]</sup> · <var class="hl-p">a</var><sup>[1]</sup>', "dot-product-f0", "multiply matching entries, add them up"),
            ' <span class="op">+</span> <var class="hl-a">b</var><sub>1</sub><sup>[2]</sup><span class="paren">)</span>',
        ], "output layer — the big question, asked of the three answers — click it")
        + decode([
            ("<var>x</var>", "“the input vector”", "All four measured numbers in one list: [price, shipping, marketing, material]."),
            ("<sup>[1]</sup>", "“layer one”", "Square brackets on top always mean <b>which layer</b>. Never an exponent. Never a power."),
            ("<sub><var>j</var></sub>", "“unit j”", "Which neuron <em>inside</em> that layer. Unit 1, 2 or 3."),
            ("<var>w</var><sub><var>j</var></sub><sup>[1]</sup>", "“the weights of unit j in layer 1”", "A <b>vector</b> — one weight per incoming number. Here it has 4 entries because 4 inputs arrive."),
            ("<var>a</var><sup>[1]</sup>", "“a superscript one”", "The output of layer 1: a vector of 3 numbers, which becomes the input to layer 2."),
        ])
        + key("""<p>A layer’s output vector is the next layer’s input vector. That single sentence is the
entire architecture of a neural network. Everything else is choosing how many layers and how wide.</p>""")

        + h2("🎬", "Watch it move")
        + demo("demand", "T-shirt demand — drag the four inputs",
               "watch which hidden unit lights up, and how that moves the final probability")
        + """<p>Push the price to $400 and watch affordability collapse while perceived quality rises —
the same input pulling two learned features in opposite directions. That tug-of-war is exactly what the
hidden layer buys you, and it is why a single logistic regression on raw price would struggle here.</p>"""

        + h2("🧠", "Why bother with a middle layer at all?")
        + grid2(
            card("<h3>Without a hidden layer</h3><p>The model can only draw one straight boundary through "
                 "the raw inputs. “Expensive is bad” — full stop. It cannot express “expensive is bad for "
                 "affordability but good for perceived quality”.</p>"),
            card("<h3>With a hidden layer</h3><p>The network builds its own intermediate features first, "
                 "then draws a straight boundary <em>in that new space</em>. Straight there = curved back "
                 "in the original space. That is where the power comes from.</p>"))
        + note("""<p>In Course 1 you did feature engineering by hand: you invented x₁·x₂ or x², typed it in,
and hoped. A hidden layer does that automatically, and learns which invented features are worth keeping.
This is the actual selling point of deep learning: <b>learned features instead of hand-made ones</b>.</p>""",
               "The real upgrade over Course 1")

        + h2("🕳", "Traps")
        + trap("""<p><b>Thinking the hidden units really mean “affordability”.</b> They don’t, unless you
forced them to. They’re whatever combination happened to reduce the cost. Interpreting them is a research
field of its own.</p>""")
        + trap("""<p><b>Reading <sup>[2]</sup> as “squared”.</b> Square brackets = layer index. Round
brackets like <var>x</var><sup>(3)</sup> = the third <em>training example</em>. Plain superscripts are
powers. Three different meanings, three different bracket styles — the course is consistent about it.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("The hidden layer has 3 units and there are 4 inputs. How many weights and biases in that layer?",
             "<p>Each unit needs one weight per input: 4 weights each × 3 units = <b>12 weights</b>, "
             "plus <b>3 biases</b> (one per unit). 15 numbers to learn in layer 1 alone.</p>"),
            ("What is the shape of a<sup>[1]</sup>, and what does the output unit receive?",
             "<p>a<sup>[1]</sup> is a vector of <b>3 numbers</b>. The output unit receives exactly those "
             "3 numbers — it never sees the original price or fabric again.</p>"),
            ("Why is “affordability” a story rather than a fact?",
             "<p>Because nothing in the training procedure names the hidden units. They are initialised "
             "randomly and shaped only by whatever reduces the loss.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("docs", "https://developers.google.com/machine-learning/crash-course/neural-networks/nodes-hidden-layers",
             "Google ML Crash Course — hidden layers",
             "A second telling of exactly this idea, with a different worked example."),
            ("play", "https://playground.tensorflow.org/#activation=sigmoid&dataset=circle&hl=1",
             "Playground: try zero hidden layers on the circle dataset",
             "Watch it fail, then add one hidden layer and watch it succeed. Two minutes, very convincing."),
            ("paper", "https://link.springer.com/article/10.1007/BF02551274",
             "Cybenko (1989) — Approximation by superpositions of a sigmoidal function",
             "The universal approximation theorem: one hidden layer, enough units, and you can approximate "
             "any continuous function. (Says nothing about whether you can <em>learn</em> it.)"),
            ("lab", "../../C2%20-%20Advanced%20Learning%20Algorithms/week1/optional-labs/C2_W1_Lab01_Neurons_and_Layers.ipynb",
             "Optional lab: Neurons and Layers",
             "In this repo. Build a single neuron in TensorFlow and compare it to logistic regression."),
        ])
    )))

# ============================================================ 3
L.append(dict(
    slug="03-recognizing-images", title="Example: recognizing images", mins=9, tag="intuition",
    lede="What a picture looks like to a computer, and the famous result that early layers learn edges, "
         "middle layers learn parts, and late layers learn whole objects.",
    body=(
        pretest("""<p>A photo is a million brightness numbers. <b>Guess what the first layer of a face-recognition network learns to look for</b> — and what the last one does.</p>""",
        """<p>Watch for the staircase: edges, then parts, then whole faces. Nobody programmed that order.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>To a computer a photo is not a face. It is a huge list of brightness numbers — one per
tiny square. A 1000×1000 photo is a list of <b>a million</b> numbers.</p>
<p>So how do you get from a million numbers to “that’s Grandma”? In steps, like building with Lego.
First layer: find tiny straight lines and corners. Second layer: glue lines into eyes, noses, mouths.
Third layer: glue parts into whole faces. Last layer: which face is it?</p>
<p>Nobody programmed those steps. The network invented that staircase by itself, because it was the
cheapest way to get the answers right.</p>""")

        + h2("🔢", "The maths, decoded")
        + """<p>There is barely any new maths here — that is the point. The same
<var>a</var> = <var>g</var>(<var>w</var>·<var>x</var> + <var>b</var>) runs on pixels instead of prices.</p>"""
        + eqp([
            ('<var>x</var> <span class="op">=</span> <span class="paren">[</span><var>x</var><sub>1</sub>, <var>x</var><sub>2</sub>, …, <var>x</var><sub>1,000,000</sub><span class="paren">]</span>',
             "vector-f0", "one long list of numbers"),
            ' <span class="op">,</span> each <var>x</var><sub><var>i</var></sub> <span class="op">∈</span> <span class="paren">[</span>0, 255<span class="paren">]</span>',
        ], "a photo, flattened into one long vector — click it")
        + decode([
            ("<var>x</var><sub><var>i</var></sub>", "“pixel i”", "Brightness of one tiny square. 0 = black, 255 = white. Colour images use three such numbers per square (red, green, blue)."),
            ("flatten", "“unroll”", "Reading the 2-D grid row by row into one long 1-D list, so a plain Dense layer can accept it."),
            ("<var>a</var><sup>[1]</sup>", "“first layer’s activations”", "In an image network, each unit here reacts strongly to one small pattern — typically an edge at a particular angle."),
        ])
        + warn("""<p>Flattening throws away the fact that two pixels were next to each other. Fully-connected
networks then have to <em>re-learn</em> that neighbouring pixels are related, from scratch, for every
position in the image. Convolutional layers (Week 2, Lesson 12) fix precisely this. For now, flat is fine —
the assignment images are only 20×20.</p>""")

        + h2("🎬", "Watch it move")
        + demo("face-features", "What each layer looks for",
               "the picture → edges → parts → whole faces")

        + h2("🔬", "Is the edges-then-parts-then-faces story actually true?")
        + """<p>Broadly, yes, and it is one of the more beautiful empirical findings in the field. If you
train a network on faces and then visualise what makes each unit fire hardest, early units really do
respond to oriented edges, and later units really do respond to face-like blobs. Train the same
architecture on cars instead, and the middle layers become wheels and windscreens.</p>
<p>The nuance researchers add: it is not perfectly tidy. Many units are <em>polysemantic</em> — a single
unit responds to several unrelated things at once — and the clean hierarchy is clearest in convolutional
networks trained on natural images.</p>"""

        + h2("🕳", "Traps")
        + trap("""<p><b>Forgetting to scale pixels.</b> Feeding raw 0–255 values makes <var>z</var> enormous,
sigmoid saturates flat, gradients vanish and training stalls. Divide by 255 (or standardise). This bites
almost everyone once.</p>""")
        + trap("""<p><b>Assuming the layer roles are guaranteed.</b> “Layer 1 = edges” is a strong tendency,
not a law. It is what you observe after training, not something you can rely on before it.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("A 20×20 greyscale image goes into a Dense layer with 25 units. How many weights?",
             "<p>20×20 = 400 inputs. 400 × 25 = <b>10,000 weights</b>, plus 25 biases. This is exactly the "
             "shape you will see in the Week 1 assignment.</p>"),
            ("Why do later layers “see” bigger things?",
             "<p>Because each layer combines many outputs of the previous one. Combining several edge "
             "detectors gives you something that spans a larger region — and so on up the stack.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("paper", "https://arxiv.org/abs/1311.2901",
             "Zeiler & Fergus (2013) — Visualizing and Understanding Convolutional Networks",
             "The paper with the famous pictures of what each layer has learned. Skim the figures even if you skip the text."),
            ("paper", "https://distill.pub/2017/feature-visualization/",
             "Distill — Feature Visualization",
             "Interactive and gorgeous. How researchers generate images that maximally excite a chosen unit."),
            ("paper", "https://distill.pub/2020/circuits/zoom-in/",
             "Distill — Zoom In: An Introduction to Circuits",
             "The careful modern version of the edges→parts→objects story, including where it breaks down."),
            ("lab", "../../C2%20-%20Advanced%20Learning%20Algorithms/week1/C2W1A1/C2_W1_Assignment.ipynb",
             "Week 1 assignment: handwritten digit recognition",
             "In this repo. 20×20 images of 0s and 1s, flattened to 400 inputs — precisely this lesson."),
        ])
    )))

# ============================================================ 4
L.append(dict(
    slug="04-neural-network-layer", title="Neural network layer", mins=10, tag="core",
    lede="The unit of construction. A layer is several neurons reading the same inputs and each producing "
         "one number — and the notation that goes with it.",
    body=(
        pretest("""<p>A layer has 3 units and receives 2 numbers. <b>How many numbers come out — and how many parameters does that layer hold?</b> Commit to both.</p>""",
        """<p>Three out; 2×3 weights + 3 biases = 9. Watch for the rule, because you will be asked to count parameters constantly.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>One neuron gives you one opinion. A <b>layer</b> is a panel of judges: they all watch the
same performance, but each cares about different things — one watches the footwork, one the music, one the
smile. Each judge holds up one score card. The layer’s output is the row of score cards.</p>
<p>Then the next layer is another panel that only sees the score cards, not the original performance.</p>""")

        + h2("🔢", "The maths, decoded")
        + """<p>For a layer with three units, reading a two-number input:</p>"""
        + eq("""<var>a</var><sub>1</sub><sup>[1]</sup> <span class="op">=</span> <var>g</var>(<var>w</var><sub>1</sub><sup>[1]</sup>·<var>x</var> + <var>b</var><sub>1</sub><sup>[1]</sup>)<br>
<var>a</var><sub>2</sub><sup>[1]</sup> <span class="op">=</span> <var>g</var>(<var>w</var><sub>2</sub><sup>[1]</sup>·<var>x</var> + <var>b</var><sub>2</sub><sup>[1]</sup>)<br>
<var>a</var><sub>3</sub><sup>[1]</sup> <span class="op">=</span> <var>g</var>(<var>w</var><sub>3</sub><sup>[1]</sup>·<var>x</var> + <var>b</var><sub>3</sub><sup>[1]</sup>)""",
             "three units, three separate weight vectors, one shared input")
        + eqp([
            ('<var class="hl-p">a</var><sup>[1]</sup> <span class="op">=</span> <span class="paren">[</span> <var>a</var><sub>1</sub><sup>[1]</sup> &nbsp; <var>a</var><sub>2</sub><sup>[1]</sup> &nbsp; <var>a</var><sub>3</sub><sup>[1]</sup> <span class="paren">]</span>',
             "vector-f0", "the layer's whole output"),
        ], "collect them into one vector — this is what the layer outputs — click it")
        + decode([
            ("layer", "“a layer”", "A group of neurons that all receive the same input vector and each output one scalar."),
            ("<var>w</var><sub>2</sub><sup>[1]</sup>", "“w two, layer one”", "The weight <b>vector</b> of the second unit of layer 1. Same length as the input."),
            ("<var>a</var><sup>[1]</sup>", "“a one”", "The whole layer’s output, stacked: length = number of units in the layer."),
            ("units", "“units” / “neurons”", "Same thing. The Dense layer’s <code>units=3</code> argument literally means “three of these”."),
        ])
        + key("""<p>The number of units in a layer decides the <b>length of that layer’s output vector</b>.
Nothing else. Not the number of inputs, not the number of examples. Just the width of what comes out.</p>""")

        + h2("🎬", "Watch it move")
        + demo("layer", "One layer of three neurons",
               "drag x₁ and x₂ — each unit computes its own z, then its own a")
        + """<p>Notice unit 2 has weights (−1.8, 2.2): it wants x₂ high and x₁ low. Unit 1 wants the
opposite. Same inputs, opposite opinions — that variety is exactly what makes the next layer useful.</p>"""

        + h2("🧮", "Counting parameters, which you will be asked to do")
        + table(["Layer", "Inputs in", "Units", "Weights", "Biases", "Total"],
                [["hidden 1", 2, 3, "2 × 3 = 6", 3, "<b>9</b>"],
                 ["hidden 2", 3, 4, "3 × 4 = 12", 4, "<b>16</b>"],
                 ["output", 4, 1, "4 × 1 = 4", 1, "<b>5</b>"]])
        + """<p>Rule: <b>weights = (inputs in) × (units)</b>, <b>biases = units</b>. TensorFlow’s
<code>model.summary()</code> prints exactly these totals, and comparing it against your hand count is the
fastest way to catch a wiring mistake.</p>"""

        + h2("🕳", "Traps")
        + trap("""<p><b>Thinking neurons in the same layer talk to each other.</b> They don’t. Within a layer
they are completely independent — that independence is exactly what lets us compute them all at once as a
single matrix multiply in Lesson 15.</p>""")
        + trap("""<p><b>Mixing up the two subscripts.</b> <var>a</var><sub>2</sub><sup>[1]</sup> = unit 2 of
layer 1. <var>a</var><sup>[2]</sup> = the whole of layer 2. The position of the bracket carries the meaning.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("A layer has 5 units and receives a 10-dimensional input. What comes out, and how many parameters?",
             "<p>Out: a vector of <b>5</b> numbers. Parameters: 10×5 = 50 weights + 5 biases = <b>55</b>.</p>"),
            ("Does adding units to a layer change the number of inputs the layer accepts?",
             "<p>No. Units change the <em>output</em> width. The input width is fixed by whatever feeds it.</p>"),
            ("Why can the three units be computed in any order?",
             "<p>Because none of them depends on another’s output. They only depend on x. Independent work "
             "is parallelisable work.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("docs", "https://www.tensorflow.org/api_docs/python/tf/keras/layers/Dense",
             "tf.keras.layers.Dense",
             "“Dense” means every input connects to every unit. Read the <code>units</code> and "
             "<code>activation</code> arguments closely."),
            ("docs", "https://cs231n.github.io/neural-networks-1/#layers",
             "CS231n — Layer-wise organization",
             "Includes the parameter-counting worked through for realistic networks."),
            ("lab", "../../C2%20-%20Advanced%20Learning%20Algorithms/week1/optional-labs/C2_W1_Lab01_Neurons_and_Layers.ipynb",
             "Optional lab: Neurons and Layers",
             "Inspect <code>layer.get_weights()</code> and see the shapes for yourself."),
        ])
    )))

# ============================================================ 5
L.append(dict(
    slug="05-more-complex-networks", title="More complex neural networks", mins=9, tag="notation",
    lede="Four layers instead of two, and the one piece of notation you must be able to read fluently: "
         "a-superscript-square-bracket-l-subscript-j.",
    body=(
        pretest("""<p>To name one specific neuron you need two labels. <b>Guess what they are</b> — and what distinguishes a<sup>[2]</sup> from a<sub>2</sub>.</p>""",
        """<p>Watch for square brackets meaning layer and subscripts meaning unit. This notation looks frightening and is only a seat number and a row number.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>It’s the same panel-of-judges idea, but now there are four panels in a row. Panel 1
watches the performance. Panel 2 only sees panel 1’s score cards. Panel 3 only sees panel 2’s. The last
panel gives the final verdict.</p>
<p>To talk about one particular judge, you need two labels: <b>which panel</b> and <b>which seat</b>.
That’s all the scary notation is — a seat number and a panel number.</p>""")

        + h2("🔢", "The maths, decoded")
        + eqp([
            '<var class="hl-a">a</var><sub><var class="hl-b">j</var></sub><sup>[<var class="hl-p">l</var>]</sup> <span class="op">=</span> <var>g</var><span class="paren">(</span>',
            ('<var class="hl-b">w</var><sub><var class="hl-b">j</var></sub><sup>[<var class="hl-p">l</var>]</sup> <span class="op">·</span> <var>a</var><sup>[<var class="hl-p">l</var>−1]</sup>',
             "dot-product-f0", "multiply matching entries, add them up"),
            ' <span class="op">+</span> <var class="hl-a">b</var><sub><var class="hl-b">j</var></sub><sup>[<var class="hl-p">l</var>]</sup><span class="paren">)</span>',
        ], "the master equation of forward propagation — click it")
        + """<p>Every single computation in every neural network in this course is one instance of that
line. Memorise it. Say it out loud: “<em>the activation of unit j in layer l is g of: the weights of unit j
in layer l, dotted with the whole output of the previous layer, plus the bias of unit j in layer l</em>”.</p>"""
        + decode([
            ("<sup>[<var>l</var>]</sup>", "“layer L”", "Which layer. Square brackets, always."),
            ("<sub><var>j</var></sub>", "“unit J”", "Which neuron inside that layer."),
            ("<var>a</var><sup>[<var>l</var>−1]</sup>", "“a of layer L minus one”", "The <b>entire</b> previous layer’s output vector. Not one number — all of them."),
            ("<var>g</var>", "“g”", "The activation function of that layer. Different layers may use different ones (Week 2)."),
            ("<var>a</var><sup>[0]</sup>", "“a zero”", "A convenient alias for <var>x</var>, the input itself. It makes the formula work for layer 1 too."),
        ])
        + note("""<p>Setting <var>a</var><sup>[0]</sup> = <var>x</var> is not a deep insight — it is a
programmer’s trick so the loop <code>for l in range(1, L+1)</code> has no special case at the start. You
will write exactly that loop in Lesson 11.</p>""", "Why a<sup>[0]</sup> = x")

        + h2("🎬", "Watch it move")
        + demo("netnotation", "A tour of the notation",
               "the highlighted unit’s name is spelled out beneath the network")

        + h2("📏", "Counting layers, and the argument about it")
        + """<p>The course convention: a network with 4 hidden layers plus an output layer is called a
<b>5-layer network</b>. The input is layer 0 and is <em>not</em> counted, because it does no computation —
it is just the data sitting there.</p>"""
        + warn("""<p>Papers are not consistent about this. Some count the input layer, some count only
hidden layers. When someone says “a 3-layer network”, it is always worth asking which they mean before
you start reimplementing it.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Writing <var>w</var><sub>j</sub><sup>[l]</sup> · <var>a</var><sub>j</sub><sup>[l−1]</sup>.</b>
Wrong. The dot product is against the <em>whole</em> previous layer, not the matching-index unit. Unit 2 of
layer 3 reads every unit of layer 2, not just unit 2.</p>""")
        + trap("""<p><b>Assuming layers must get smaller.</b> They don’t have to. 25 → 15 → 1 is common, but
so is 64 → 128 → 64. Width is a design choice, not a rule.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("In a network with layers of size 4 → 5 → 3 → 1, what is the length of the vector that w<sub>2</sub><sup>[3]</sup> must have?",
             "<p>Layer 3 reads layer 2, which has <b>3</b> units. So w<sub>2</sub><sup>[3]</sup> is a "
             "vector of length <b>3</b>. Weight-vector length always equals the width of the previous layer.</p>"),
            ("How many layers does that network have, by the course’s convention?",
             "<p>Input 4 is layer 0 and does not count. So 5, 3, 1 → a <b>3-layer network</b> (2 hidden + 1 output).</p>"),
            ("What is a<sup>[0]</sup>?",
             "<p>x — the input. It is an alias so the general formula covers layer 1 without a special case.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("docs", "https://cs231n.github.io/neural-networks-1/#nn",
             "CS231n — notation and architectures",
             "Uses slightly different symbols. Reading a second notation is the fastest way to stop being scared of any notation."),
            ("video", "https://www.3blue1brown.com/lessons/gradient-descent",
             "3Blue1Brown — Gradient descent, how neural networks learn",
             "Chapter 2. Shows the same layered structure with the weights as a matrix picture."),
        ])
    )))

# ============================================================ 6
L.append(dict(
    slug="06-forward-propagation", title="Inference: making predictions (forward propagation)", mins=11, tag="core",
    lede="The complete prediction algorithm, start to finish. Handwritten digit recognition with a "
         "25 → 15 → 1 network — and the reason it is called “forward”.",
    body=(
        pretest("""<p>Input → layer 1 → layer 2 → layer 3 → answer. <b>Guess why it is called “forward”</b> — what would a backward version even mean?</p>""",
        """<p>Watch for the relay-race shape. Backward propagation exists too, and it is how the thing learns rather than predicts.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>It’s a relay race, and the baton is a list of numbers.</p>
<p>The picture hands its 64 numbers to the first panel of judges. That panel hands 25 score cards to the
second panel. The second hands 15 score cards to the last judge. The last judge hands you one number:
“I’m 93% sure this is a 1.”</p>
<p>The baton only ever moves <b>forwards</b>. Nobody runs backwards. That’s why it is called
<b>forward</b> propagation.</p>""")

        + h2("🔢", "The maths, decoded")
        + eqp([
            '<var class="hl-b">a</var><sup>[1]</sup> = <var>g</var>(',
            ('<var>W</var><sup>[1]</sup><var>x</var>', "matmul-f0", "whole layer, one multiply"),
            ' + <var>b</var><sup>[1]</sup>) &nbsp;→&nbsp; <var class="hl-p">a</var><sup>[2]</sup> = <var>g</var>(',
            ('<var>W</var><sup>[2]</sup><var class="hl-b">a</var><sup>[1]</sup>', "matmul-f0", "whole layer, one multiply"),
            ' + <var>b</var><sup>[2]</sup>) &nbsp;→&nbsp; <var class="hl-g">a</var><sup>[3]</sup> = <var>g</var>(',
            ('<var>W</var><sup>[3]</sup><var class="hl-p">a</var><sup>[2]</sup>', "matmul-f0", "whole layer, one multiply"),
            ' + <var>b</var><sup>[3]</sup>)',
        ], "three layers, in order — click a part")
        + eqp([
            ('<var>f</var>(<var>x</var>) = <var class="hl-g">a</var><sup>[3]</sup>', "func-f", "the model's output"),
            ' &nbsp;&nbsp;&nbsp; ŷ = <span class="paren">{</span> 1 if <var>a</var><sup>[3]</sup> ≥ 0.5, &nbsp; 0 otherwise',
        ], "and finally a decision — click it")
        + decode([
            ("forward", "“forward propagation”", "Computing layer 1, then 2, then 3, in that order. Also called <b>inference</b> — using a trained model rather than training one."),
            ("<var>f</var>(<var>x</var>)", "“f of x”", "The model’s output. For a binary classifier it is P(y = 1 | x), a probability."),
            ("ŷ", "“y hat”", "The final hard decision, 0 or 1, after thresholding the probability."),
            ("0.5", "“the threshold”", "A choice, not a law. Week 3 shows when you should move it (spoiler: whenever mistakes cost different amounts)."),
        ])
        + key("""<p>Forward propagation is a loop with three lines in the body. There is no cleverness in it
at all. All the difficulty in neural networks lives in <em>finding</em> W and b — never in using them.</p>""")

        + h2("🎬", "Watch it move")
        + demo("forward", "Draw a digit and watch it propagate",
               "click the squares — the hidden units and the output update instantly")
        + """<p>(The weights in that demo are hand-picked so it is readable, not trained — but the
arithmetic and the direction of flow are exactly right.)</p>"""

        + h2("💻", "In code")
        + code("""
# forward propagation, by hand, for a 3-layer network
a1 = sigmoid(np.matmul(x,  W1) + b1)   # (1,400) @ (400,25) -> (1,25)
a2 = sigmoid(np.matmul(a1, W2) + b2)   # (1,25)  @ (25,15)  -> (1,15)
a3 = sigmoid(np.matmul(a2, W3) + b3)   # (1,15)  @ (15,1)   -> (1,1)
yhat = 1 if a3[0, 0] >= 0.5 else 0
""")
        + """<p>Read the shape comments on the right. Each layer’s output shape becomes the next layer’s
input shape, and the “inner” numbers cancel: 400 meets 400, 25 meets 25, 15 meets 15. When your code
crashes in this course, it is almost always because two of those inner numbers didn’t match.</p>"""

        + h2("🕳", "Traps")
        + trap("""<p><b>Reusing a1 where you meant a2.</b> Copy-paste is the number one bug in hand-written
forward propagation. Name your variables after the layer, always.</p>""")
        + trap("""<p><b>Thresholding too early.</b> Keep the probability all the way to the end. Once you
round to 0/1 you have thrown away the confidence, and you cannot get it back — you need it for the
precision/recall work in Week 3.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("For a 400 → 25 → 15 → 1 network, what are the shapes of W1, W2, W3?",
             "<p>(400, 25), (25, 15), (15, 1) in the row-vector convention this course uses. Biases: "
             "(25,), (15,), (1,).</p>"),
            ("If a<sup>[3]</sup> = 0.49, what is ŷ at the default threshold? Is the model confident?",
             "<p>ŷ = <b>0</b>, because 0.49 &lt; 0.5. But it is barely confident at all — 0.49 vs 0.51 is a "
             "coin flip, and treating them as opposite certainties is a classic mistake.</p>"),
            ("Why is it called “inference” as well as “forward propagation”?",
             "<p>Because you are inferring an answer from a model you already have. Training is a separate "
             "activity that happens beforehand.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("video", "https://www.3blue1brown.com/lessons/neural-networks",
             "3Blue1Brown — chapter 1, the forward pass",
             "The animation of activations lighting up layer by layer is the same idea as the demo above, at higher production value."),
            ("docs", "https://numpy.org/doc/stable/reference/generated/numpy.matmul.html",
             "numpy.matmul",
             "The single function that does a whole layer. Note the shape rules at the bottom of the page."),
            ("lab", "../../C2%20-%20Advanced%20Learning%20Algorithms/week1/C2W1A1/C2_W1_Assignment.ipynb",
             "Week 1 assignment",
             "You implement exactly this, twice: once with loops, once vectorised."),
        ])
    )))

# ============================================================ 7
L.append(dict(
    slug="07-tensorflow-inference-code", title="Inference in code (TensorFlow)", mins=10, tag="code",
    lede="The coffee-roasting example: four lines of TensorFlow that do everything the last three lessons "
         "described by hand.",
    body=(
        pretest("""<p>You have built a network by hand. <b>Guess how many lines TensorFlow needs to do the same forward pass.</b></p>""",
        """<p>Watch for how little code it is, and for which line does the thing you spent a whole lesson computing by hand.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>You just learned to make bread by hand — grinding the flour, kneading, waiting. This
lesson is the bread machine. Same bread. Four buttons.</p>
<p>The catch is that a bread machine is only safe if you already know what the dough should look like.
That is why the by-hand lessons came first.</p>""")

        + h2("☕", "The example: roasting coffee")
        + """<p>Two inputs — temperature (°C) and duration (minutes). One output — was the roast good?
The good region is a slanted blob: too cool and it’s raw whatever you do; too hot and it burns; and the
right duration depends on the temperature. Two straight lines cannot carve that blob out, which is exactly
why it needs a hidden layer.</p>"""

        + h2("💻", "In code")
        + code("""
import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Dense

x = np.array([[200.0, 17.0]])          # ONE example, two features -> shape (1, 2)

layer_1 = Dense(units=3, activation='sigmoid')
a1 = layer_1(x)                        # -> tf.Tensor, shape (1, 3)

layer_2 = Dense(units=1, activation='sigmoid')
a2 = layer_2(a1)                       # -> tf.Tensor, shape (1, 1)

yhat = 1 if a2 >= 0.5 else 0
""")
        + decode([
            ("<code>Dense</code>", "“a dense layer”", "“Dense” = fully connected: every input reaches every unit. It is the layer type from Lesson 4."),
            ("<code>units=3</code>", "“three neurons”", "How many numbers this layer outputs."),
            ("<code>activation</code>", "“the squasher g”", "Which function to apply to z. <code>'sigmoid'</code> here; you’ll switch to <code>'relu'</code> in Week 2."),
            ("<code>layer_1(x)</code>", "“call the layer on x”", "In Keras a layer is a callable object. Calling it runs the forward computation."),
        ], head=("Piece", "Say it out loud", "What it does"))

        + h2("🎬", "Watch it move")
        + demo("codeflow", "Step through the code, line by line",
               "press ‘next step’ — the network lights up in time with the highlighted line")

        + h2("🧩", "Where did the weights come from?")
        + """<p>Nowhere — and that is the point of this lesson. <code>Dense</code> initialises W and b
<b>randomly</b> the first time it sees an input. This code therefore produces garbage predictions until
you train it. Lesson: <code>model.predict()</code> always returns <em>a</em> number; the number being
sensible is a separate question entirely.</p>"""
        + warn("""<p>TensorFlow returns <code>tf.Tensor</code> objects, not NumPy arrays. They print as
<code>tf.Tensor([[0.28]], shape=(1,1), dtype=float32)</code>. Call <code>.numpy()</code> when you want a
plain array back. Every learner trips over this once.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Passing a 1-D array.</b> <code>np.array([200.0, 17.0])</code> has shape (2,) and
Keras will complain or silently reinterpret it. It must be <code>[[200.0, 17.0]]</code> — double brackets.
That is the entire subject of the next lesson.</p>""")
        + trap("""<p><b>Forgetting normalisation.</b> Temperature ~200 and duration ~17 live on wildly
different scales. Real code puts a <code>Normalization</code> layer in front — the optional lab does exactly
this, and skipping it makes training crawl.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("What is the shape of a1 after <code>layer_1(x)</code> with units=3 and x of shape (1,2)?",
             "<p><b>(1, 3)</b> — one row because one example, three columns because three units.</p>"),
            ("If you ran this exact code twice in a fresh session, would you get the same a2?",
             "<p>No. The weights are randomly initialised each time. You’d get two different meaningless "
             "numbers.</p>"),
            ("Why does Dense not ask how many inputs there are?",
             "<p>It infers it from the first input it sees, then fixes W’s shape. That is why "
             "<code>model.summary()</code> before the first call can show “unbuilt”.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("docs", "https://www.tensorflow.org/guide/keras/sequential_model",
             "Keras — the Sequential model guide",
             "Official walkthrough of building, calling and inspecting layer stacks."),
            ("docs", "https://www.tensorflow.org/api_docs/python/tf/keras/layers/Normalization",
             "tf.keras.layers.Normalization",
             "The layer the coffee lab uses to fix the 200-vs-17 scale problem. Call <code>adapt()</code> on your data first."),
            ("lab", "../../C2%20-%20Advanced%20Learning%20Algorithms/week1/optional-labs/C2_W1_Lab02_CoffeeRoasting_TF.ipynb",
             "Optional lab: Coffee Roasting in TensorFlow",
             "In this repo. Run it, then change <code>units=3</code> to <code>units=1</code> and watch the decision boundary get worse."),
        ])
    )))

# ============================================================ 8
L.append(dict(
    slug="08-data-in-tensorflow", title="Data in TensorFlow", mins=9, tag="code",
    lede="Double brackets, single brackets, and why an afternoon of your life will otherwise be lost to "
         "shape errors.",
    body=(
        pretest("""<p>You pass <code>[200, 17]</code> to a model and it complains about shape. <b>Guess what TensorFlow wanted instead.</b></p>""",
        """<p>Watch for the extra pair of brackets. TensorFlow always expects a batch, even a batch of one.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Think of an egg box. A <b>matrix</b> is an egg box: it has rows and columns, and even a
box holding one single egg still has a row and a column.</p>
<p>A <b>1-D array</b> is eggs loose in a bag. Same eggs — but the bag doesn’t say which is a row and which
is a column. TensorFlow will not accept a bag. It wants the box.</p>""")

        + h2("🔢", "The three things that look alike")
        + table(["What you type", "Shape", "What it is", "Use it for"],
                [["<code>np.array([[200, 17]])</code>", "(1, 2)", "1 row × 2 cols — a matrix", "<b>one training example</b> with 2 features"],
                 ["<code>np.array([[200], [17]])</code>", "(2, 1)", "2 rows × 1 col — a matrix", "a column vector (rare in this course)"],
                 ["<code>np.array([200, 17])</code>", "(2,)", "1-D array — no rows or columns", "old Course 1 code; <b>not</b> what Keras wants"]])
        + key("""<p>The convention for the whole specialization: <b>rows = training examples, columns =
features</b>. A dataset of 3 examples with 2 features each is shape (3, 2). Learn to read a shape tuple as
“(how many examples, how many numbers per example)” and half your bugs vanish.</p>""")

        + h2("🎬", "Watch it move")
        + demo("shapes", "The same numbers, four different shapes",
               "click the shape buttons to see what the brackets actually build")

        + h2("🔬", "Tensors vs. arrays")
        + """<p>TensorFlow computes on <code>tf.Tensor</code>, which is its own matrix type — designed to be
shipped off to a GPU. NumPy computes on <code>ndarray</code>. They convert into each other constantly and
almost invisibly:</p>"""
        + code("""
a1 = layer_1(x)        # tf.Tensor([[0.2, 0.7, 0.5]], shape=(1, 3), dtype=float32)
a1.numpy()             # array([[0.2, 0.7, 0.5]], dtype=float32)   <- back to NumPy
""")
        + note("""<p>The word “tensor” sounds like physics but here it means nothing more exotic than
“an array with any number of dimensions”. A number is a 0-D tensor, a list is 1-D, a matrix is 2-D, a stack
of images is 4-D. That is the whole concept.</p>""", "“Tensor” demystified")

        + h2("🕳", "Traps")
        + trap("""<p><b>(2,) is not (1,2).</b> The trailing comma in <code>(2,)</code> means “one dimension,
of length two”. It is Python’s way of writing a one-element tuple, and it is the single most common source
of confusion in this week.</p>""")
        + trap("""<p><b>Silent broadcasting.</b> NumPy will sometimes cheerfully broadcast a wrong shape into
a valid-looking result instead of erroring. You get numbers, they’re just the wrong ones. Print
<code>.shape</code> after every step while you’re learning.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("You have 1000 images, each 20×20 greyscale, ready for a Dense layer. What shape is X?",
             "<p><b>(1000, 400)</b> — 1000 rows (examples) and 20×20 = 400 columns (features), after "
             "flattening each image.</p>"),
            ("<code>x = np.array([200, 17])</code> then <code>layer_1(x)</code>. What happens?",
             "<p>Keras either errors or reinterprets the (2,) array as two examples with one feature each — "
             "which is wrong. Write <code>np.array([[200, 17]])</code>.</p>"),
            ("What does <code>.numpy()</code> do and when do you need it?",
             "<p>Converts a tf.Tensor to a NumPy array. Needed when you want to index, plot or compare "
             "against NumPy results.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("docs", "https://numpy.org/doc/stable/user/basics.broadcasting.html",
             "NumPy broadcasting rules",
             "The precise rules for when shapes are compatible. Read once now, re-read when something breaks."),
            ("docs", "https://www.tensorflow.org/guide/tensor",
             "TensorFlow — Introduction to Tensors",
             "Ranks, shapes, dtypes, and how tensors differ from NumPy arrays."),
            ("docs", "https://numpy.org/doc/stable/user/absolute_beginners.html#how-to-convert-a-1d-array-into-a-2d-array",
             "NumPy — turning a 1-D array into a 2-D array",
             "<code>reshape(1, -1)</code> and <code>np.newaxis</code>, the two fixes you will use constantly."),
        ])
    )))

# ============================================================ 9
L.append(dict(
    slug="09-building-a-network-sequential", title="Building a neural network (Sequential)", mins=9, tag="code",
    lede="Stop calling layers by hand. Sequential wires them together, and three method calls — compile, "
         "fit, predict — do the rest.",
    body=(
        pretest("""<p><code>Sequential</code> stacks layers in a line. <b>Guess what kind of network it therefore cannot build.</b></p>""",
        """<p>Watch for what “sequential” rules out: more than one input, more than one output, or a layer that skips ahead.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Before: you carried the baton from runner to runner yourself. Now you hand the whole
team to a coach and say “run in this order”. The coach handles the handoffs.</p>
<p><code>Sequential</code> is that coach. You give it a list of layers, top to bottom, and it feeds each
one’s output into the next automatically.</p>""")

        + h2("💻", "In code")
        + code("""
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense

model = Sequential([
    Dense(units=3, activation='sigmoid'),   # layer 1
    Dense(units=1, activation='sigmoid'),   # layer 2 (output)
])

model.compile(loss='binary_crossentropy')   # what "wrong" means  (Week 2)
model.fit(X, Y, epochs=100)                 # learn W and b       (Week 2)
p = model.predict(X_new)                    # forward propagation, for every row of X_new
""")
        + decode([
            ("<code>Sequential</code>", "“a straight stack”", "Layers in a line, each feeding the next. No branches, no skips."),
            ("<code>compile</code>", "“set the rules”", "Tells the model what counts as a mistake (the loss) and how to fix it (the optimiser)."),
            ("<code>fit</code>", "“train”", "Runs gradient descent to find W and b. This is the only step that changes the parameters."),
            ("<code>predict</code>", "“infer”", "Forward propagation over a whole batch of examples at once. Returns an array with one row per input row."),
        ], head=("Piece", "Say it out loud", "What it does"))

        + h2("🎬", "Watch it move")
        + demo("sequential", "Stacking layers",
               "the layers drop into place, and the shape of what flows between them")

        + h2("🔬", "Two ways to write the same model")
        + grid2(
            card("<h3>List form</h3><pre style='margin:8px 0 0'><code>model = Sequential([\n"
                 "    Dense(3, activation='sigmoid'),\n    Dense(1, activation='sigmoid')\n])</code></pre>"
                 "<p style='margin-top:8px'>What the course uses. Compact and readable.</p>"),
            card("<h3>Add form</h3><pre style='margin:8px 0 0'><code>model = Sequential()\n"
                 "model.add(Dense(3, activation='sigmoid'))\nmodel.add(Dense(1, activation='sigmoid'))</code></pre>"
                 "<p style='margin-top:8px'>Identical result. Handy when layers are built in a loop.</p>"))
        + """<p>Add <code>model.summary()</code> after building and you get a table of every layer, its
output shape and its parameter count — the same numbers you hand-counted in Lesson 4. Get in the habit of
reading it before you train anything.</p>"""

        + h2("🕳", "Traps")
        + trap("""<p><b>Expecting <code>predict</code> to return 0s and 1s.</b> It returns probabilities.
Thresholding is your job: <code>(p >= 0.5).astype(int)</code>.</p>""")
        + trap("""<p><b>Calling <code>fit</code> twice by accident.</b> Keras <em>continues</em> training from
where it left off; it does not start over. Re-run the cell that builds the model if you want a clean start.</p>""")
        + warn("""<p><code>Sequential</code> can only express a straight line of layers. Anything with two
inputs, two outputs or a skip connection needs the <a href="https://www.tensorflow.org/guide/keras/functional_api"
target="_blank" rel="noopener">functional API</a>. Not needed for this course — worth knowing it exists.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("<code>model.predict(X)</code> with X of shape (500, 400) on a 400→25→15→1 network. Output shape?",
             "<p><b>(500, 1)</b> — one probability per input row. <code>predict</code> handles all 500 "
             "examples in one call.</p>"),
            ("Which of compile / fit / predict actually changes W and b?",
             "<p>Only <b>fit</b>. compile just records the settings; predict only reads.</p>"),
            ("Why does model.summary() sometimes report 0 parameters?",
             "<p>Because the model has not been built yet — Keras waits until it sees input data (or an "
             "explicit <code>input_shape</code>) to fix the weight shapes.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("docs", "https://www.tensorflow.org/guide/keras/sequential_model",
             "Keras — the Sequential model",
             "Including exactly when Sequential is the wrong choice."),
            ("docs", "https://keras.io/api/models/model_training_apis/",
             "Keras — compile / fit / evaluate / predict",
             "The full argument list for the three methods you will use every week from now on."),
            ("lab", "../../C2%20-%20Advanced%20Learning%20Algorithms/week1/optional-labs/C2_W1_Lab02_CoffeeRoasting_TF.ipynb",
             "Optional lab: Coffee Roasting in TensorFlow",
             "Builds this exact model, trains it, and plots the decision boundary the hidden units carve out."),
        ])
    )))

# ============================================================ 10
L.append(dict(
    slug="10-forward-prop-single-layer", title="Forward prop in a single layer (NumPy)", mins=10, tag="core",
    lede="Throw away the framework. Compute one layer with nothing but np.dot — because a black box you "
         "have opened once stops being a black box.",
    body=(
        pretest("""<p>You implement one layer in NumPy. The weight matrix W is 2×3. <b>Guess whether one neuron is a row or a column of W.</b></p>""",
        """<p>Commit before reading. Watch for <code>W[:, j]</code> — the slice that picks out one neuron.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>You have a big table of trust numbers, W. Each <b>column</b> of that table belongs to one
neuron — it is that neuron’s personal list of trust levels.</p>
<p>So to work out neuron 2’s answer: take column 2, pair it up with the incoming numbers, multiply each
pair, add them all up, add neuron 2’s bias, squash. Done. Now do the same with column 3.</p>""")

        + h2("🔢", "The maths, decoded")
        + eqp([
            ('<var>w</var><sub><var>j</var></sub> = <var>W</var><span class="paren">[</span>:, <var>j</var><span class="paren">]</span>', "indexing-f0", "all rows, column j"),
            ' &nbsp;&nbsp; <var>z</var><sub><var>j</var></sub> = ',
            ('<var>w</var><sub><var>j</var></sub> · <var>a</var><sub>in</sub>', "dot-product-f0", "multiply matching entries, add them up"),
            ' + <var>b</var><sub><var>j</var></sub> &nbsp;&nbsp; <var>a</var><sub>out</sub><span class="paren">[</span><var>j</var><span class="paren">]</span> = ',
            ('<var>g</var>(<var>z</var><sub><var>j</var></sub>)', "sigmoid-squash", "the squasher"),
        ], "one neuron = one column of W — click a part")
        + decode([
            ("<var>W</var>", "“capital W”", "The whole layer’s weights as one 2-D table. Rows = incoming features, columns = neurons."),
            ("<code>W[:, j]</code>", "“all rows, column j”", "NumPy slice notation: the colon means “everything”. This picks out neuron j’s weight vector."),
            ("<var>a</var><sub>in</sub>", "“a in”", "Whatever arrived from the previous layer (or the input x, for layer 1)."),
            ("<code>np.dot</code>", "“dot”", "Multiply matching entries and add them all up. Two lists in, one number out."),
        ])
        + key("""<p><b>Columns of W are neurons.</b> If you remember one thing from this lesson, remember
that. Rows of W are input features. This orientation is the one that makes the matrix version in Lesson 16
work without any transposes.</p>""")

        + h2("🎬", "Watch it move")
        + demo("densehand", "One column at a time",
               "the highlighted column of W is the neuron currently being computed")

        + h2("💻", "In code — the hard-coded version")
        + code("""
W = np.array([[ 1, -3,  5],      # row 0: weights that multiply a_in[0]
              [-2,  4, -6]])     # row 1: weights that multiply a_in[1]
b = np.array([-1,  1,  2])       # one bias per neuron
a_in = np.array([0.6, 0.9])

# neuron 1
w1 = W[:, 0]                     # -> [ 1, -2]
z1 = np.dot(w1, a_in) + b[0]     # 1(0.6) + (-2)(0.9) + (-1) = -2.2
a1 = sigmoid(z1)

# neuron 2
w2 = W[:, 1]                     # -> [-3,  4]
z2 = np.dot(w2, a_in) + b[1]     # -3(0.6) + 4(0.9) + 1 = 2.8
a2 = sigmoid(z2)

# neuron 3
w3 = W[:, 2]                     # -> [ 5, -6]
z3 = np.dot(w3, a_in) + b[2]     # 5(0.6) + (-6)(0.9) + 2 = -0.4
a3 = sigmoid(z3)

a_out = np.array([a1, a2, a3])   # [0.100, 0.943, 0.401]
""")
        + note("""<p>Do this arithmetic on paper once, right now, for neuron 2. −3(0.6) = −1.8. 4(0.9) = 3.6.
−1.8 + 3.6 + 1 = 2.8. sigmoid(2.8) = 0.943. Fifteen seconds of pencil work will do more for your
understanding than re-reading the page.</p>""", "Do it on paper")

        + h2("🕳", "Traps")
        + trap("""<p><b>Grabbing a row instead of a column.</b> <code>W[0]</code> is a row — the weights that
all three neurons apply to input 0. <code>W[:, 0]</code> is a column — everything neuron 0 uses. Different
things, both length-2 here, so NumPy will not save you.</p>""")
        + trap("""<p><b>Confusing <code>np.dot</code> with <code>*</code>.</b> <code>*</code> multiplies
element-wise and returns a <em>list</em>. <code>np.dot</code> also sums, returning a <em>number</em>. A
neuron needs the number.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("With the W above, what is W[:, 2] and what does it belong to?",
             "<p><b>[5, −6]</b> — the weight vector of the <b>third</b> neuron.</p>"),
            ("W has shape (2, 3). How many inputs and how many neurons?",
             "<p><b>2 inputs</b> (rows) and <b>3 neurons</b> (columns). Reading a weight-matrix shape as "
             "(in, out) is a habit worth building.</p>"),
            ("Compute z for neuron 1 by hand: w = [1, −2], a_in = [0.6, 0.9], b = −1.",
             "<p>1(0.6) + (−2)(0.9) + (−1) = 0.6 − 1.8 − 1 = <b>−2.2</b>. sigmoid(−2.2) ≈ 0.10, so this "
             "neuron is firmly saying “no”.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("docs", "https://numpy.org/doc/stable/user/basics.indexing.html",
             "NumPy indexing and slicing",
             "The colon syntax in full. Worth ten minutes — it is used in every ML codebase you will ever read."),
            ("lab", "../../C2%20-%20Advanced%20Learning%20Algorithms/week1/optional-labs/C2_W1_Lab03_CoffeeRoasting_Numpy.ipynb",
             "Optional lab: Coffee Roasting in NumPy",
             "The same model as the TensorFlow lab, written from scratch. Diff the two files — that comparison is the lesson."),
        ])
    )))

# ============================================================ 11
L.append(dict(
    slug="11-general-forward-prop", title="General implementation of forward propagation", mins=9, tag="core",
    lede="Replace the copy-pasted neurons with one loop, then stack the loops into a network. This is the "
         "code you will write in the assignment.",
    body=(
        pretest("""<p>You wrote a function for one layer. <b>Guess what has to change to make it work for a network of any depth.</b></p>""",
        """<p>Watch for how little does. The whole network is one function, called in a loop.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Last lesson you wrote out neuron 1, then neuron 2, then neuron 3 — three near-identical
paragraphs. That is silly. Whenever you catch yourself copying and pasting with one number changed, that
number wants to become a <b>loop counter</b>.</p>""")

        + h2("💻", "The dense() function")
        + code("""
def dense(a_in, W, b):
    units = W.shape[1]            # number of columns = number of neurons
    a_out = np.zeros(units)       # empty box to fill
    for j in range(units):        # one pass per neuron
        w = W[:, j]               # column j
        z = np.dot(w, a_in) + b[j]
        a_out[j] = sigmoid(z)
    return a_out
""")
        + decode([
            ("<code>W.shape[1]</code>", "“the number of columns”", "<code>shape</code> is (rows, cols). Index 1 is columns = the number of neurons. Never hard-code this."),
            ("<code>np.zeros(units)</code>", "“an empty box”", "Pre-allocate the answer so the loop can fill slots. Cheaper and clearer than appending."),
            ("<code>for j in range(units)</code>", "“for each neuron”", "j walks along the columns of W, left to right."),
            ("<code>a_out</code>", "“the layer’s output”", "One number per neuron, in order — exactly the vector a<sup>[l]</sup> from Lesson 5."),
        ], head=("Line", "Say it out loud", "Why it is there"))

        + h2("🎬", "Watch it move")
        + demo("denseloop", "The loop, running",
               "the highlighted column of W and the highlighted line of code stay in step")

        + h2("🔢", "And then the whole network")
        + code("""
def sequential(x):
    a1 = dense(x,  W1, b1)
    a2 = dense(a1, W2, b2)
    a3 = dense(a2, W3, b3)
    a4 = dense(a3, W4, b4)
    return a4                     # f(x)
""")
        + """<p>That is a complete neural network. Every framework in the world — TensorFlow, PyTorch, JAX —
is, at its computational core, this function plus a great deal of engineering for speed, autodiff and
hardware.</p>"""
        + note("""<p>Capital <code>W</code> for matrices, lowercase <code>b</code> and <code>w</code> for
vectors. This is standard maths convention and the course follows it exactly. It is a genuinely useful
reading aid: capital letter → expect two dimensions.</p>""", "Naming convention")

        + h2("🕳", "Traps")
        + trap("""<p><b>Using <code>W.shape[0]</code>.</b> That is the number of <em>inputs</em>, not the
number of neurons. If your a_out comes out the wrong length, this is the first thing to check.</p>""")
        + trap("""<p><b>Passing x into every layer.</b> Layer 2 takes <code>a1</code>, not <code>x</code>. It
is a one-character typo that produces perfectly valid-looking numbers and a completely broken network.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("W is (400, 25) and a_in is length 400. What does dense() return?",
             "<p>A vector of length <b>25</b>. The loop runs 25 times, once per column.</p>"),
            ("Why pre-allocate with np.zeros instead of building a list?",
             "<p>You know the size in advance, so allocation is cheaper than growing a list — and the "
             "result is already a NumPy array of the right dtype.</p>"),
            ("How would you change dense() to use ReLU instead of sigmoid?",
             "<p>Pass the activation function as an argument: <code>def dense(a_in, W, b, g)</code>, then "
             "<code>a_out[j] = g(z)</code>. That is exactly what Keras’ <code>activation=</code> does.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("docs", "https://numpy.org/doc/stable/reference/generated/numpy.zeros.html",
             "numpy.zeros",
             "Note the <code>dtype</code> argument — defaults to float64, which matters for memory on large models."),
            ("lab", "../../C2%20-%20Advanced%20Learning%20Algorithms/week1/C2W1A1/C2_W1_Assignment.ipynb",
             "Week 1 assignment — my_dense()",
             "You write this function for marks. Then you write the vectorised version from Lesson 16."),
        ])
    )))

# ============================================================ 12
L.append(dict(
    slug="12-path-to-agi", title="Is there a path to AGI?", mins=8, tag="optional",
    lede="An honest detour. The one-learning-algorithm hypothesis, the rewiring experiments behind it, "
         "and why Andrew Ng is careful not to over-promise.",
    body=(
        pretest("""<p>Neural networks were inspired by brains and now beat humans at many tasks. <b>Does that mean general intelligence is close?</b> Commit to a view before reading.</p>""",
        """<p>Watch for the honest assessment, including the “one learning algorithm” evidence that makes the question harder than it first looks.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Scientists once took a baby animal and plugged the wire from its <b>eye</b> into the part
of the brain that normally handles <b>hearing</b>. That patch of brain then learned to see.</p>
<p>Which raises a wild thought: maybe the brain isn’t a hundred different special machines. Maybe it’s a
hundred copies of <b>one</b> learning machine, and each copy becomes whatever its incoming wire feeds it.</p>
<p>If that’s true, and if we found that one algorithm, you could learn everything with it. That is the
dream. Nobody knows if it’s true.</p>""")

        + h2("🎬", "Watch it move")
        + demo("oneAlgo", "The rewiring experiment",
               "eye → visual cortex, then eye → auditory cortex, which learns to see")

        + h2("🧪", "The actual experiments")
        + """<p>These are real neuroscience results, not thought experiments:</p>
<ul>
<li><b>Neural rewiring in ferrets</b> (Sur and colleagues, 1980s–2000): visual input routed to the auditory
cortex produced orientation-selective cells there — the auditory tissue developed visual machinery.</li>
<li><b>Tactile-visual substitution</b> (Bach-y-Rita, from 1969): blind volunteers wearing a camera that
drives a grid of vibrating points on the tongue or back learn to perceive shape and depth.</li>
<li><b>Human echolocation</b>: some blind people learn to navigate by clicking, and brain imaging shows
visual areas becoming active.</li>
</ul>
<p>The shared punchline is that a piece of cortex is remarkably flexible about what kind of input it will
learn to process.</p>"""

        + h2("⚖️", "The honest scorecard")
        + grid2(
            card("<h3>Reasons for optimism</h3><ul>"
                 "<li>One architecture (the transformer) now handles text, images, audio and code.</li>"
                 "<li>Capabilities keep appearing from scale alone, without new algorithms.</li>"
                 "<li>The rewiring evidence really is suggestive.</li></ul>"),
            card("<h3>Reasons for caution</h3><ul>"
                 "<li>Cortex is flexible, but it is not blank — structure and wiring differ across regions.</li>"
                 "<li>Today’s systems need orders of magnitude more examples than a child does.</li>"
                 "<li>Nobody has a working definition of AGI that researchers agree on, which makes "
                 "“progress towards it” hard to measure.</li></ul>"))
        + warn("""<p>Andrew’s own framing in the video is worth copying: he is enthusiastic about the
hypothesis and openly unsure about the timeline. That combination — excited about the work, humble about
the extrapolation — is the professional norm. Be suspicious of anyone who has only one of the two.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("What is the one-learning-algorithm hypothesis in one sentence?",
             "<p>That much of the brain may run a single general learning procedure, and that regions "
             "specialise because of what they are wired to rather than because they are built differently.</p>"),
            ("Does the ferret rewiring result prove the hypothesis?",
             "<p>No. It shows cortex is unusually plastic. That is consistent with the hypothesis but a long "
             "way from proving one algorithm underlies everything.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("paper", "https://www.nature.com/articles/35009043",
             "Sharma, Angelucci & Sur (2000) — Induction of visual orientation modules in auditory cortex",
             "The rewiring result itself, in Nature."),
            ("paper", "https://www.nature.com/articles/221963a0",
             "Bach-y-Rita et al. (1969) — Vision substitution by tactile image projection",
             "The original sensory-substitution paper."),
            ("paper", "https://arxiv.org/abs/2001.08361",
             "Kaplan et al. (2020) — Scaling Laws for Neural Language Models",
             "The modern empirical basis for “just make it bigger”. Startlingly regular curves."),
            ("book", "https://www.deeplearningbook.org/contents/intro.html",
             "Deep Learning — chapter 1, historical trends",
             "A careful, non-hyped account of the field’s two previous boom-and-bust cycles."),
        ])
    )))

# ============================================================ 13
L.append(dict(
    slug="13-vectorization", title="How neural networks are implemented efficiently", mins=9, tag="core",
    lede="Why the for-loop version is fine for learning and useless in production, and what vectorisation "
         "actually buys you.",
    body=(
        pretest("""<p>A layer computes one dot product per neuron per example. With 1000 examples and 25 neurons that is 25,000 dot products. <b>Guess how many operations a computer should actually perform.</b></p>""",
        """<p>Watch for how all 25,000 collapse into a single matrix multiplication.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>You have 100 letters to stamp. You could pick up one letter, stamp it, put it down, pick
up the next… one hundred times. Or you could lay all 100 out on a big tray and bring down a giant stamp
<b>once</b>.</p>
<p>Same 100 stamps. Wildly different amount of time. Computers have that giant stamp — it is called
parallel hardware — but only if you hand them the whole tray instead of one letter at a time.</p>""")

        + h2("🎬", "Watch it move")
        + demo("vectorize", "One at a time vs. all at once",
               "the same 16 multiplications, two different ways of asking for them")

        + h2("🔢", "The two versions, side by side")
        + grid2(
            card("<h3>Looped</h3><pre style='margin:8px 0'><code>for j in range(units):\n"
                 "    w = W[:, j]\n    z = np.dot(w, a_in) + b[j]\n    a_out[j] = g(z)</code></pre>"
                 "<p>Python executes <code>units</code> separate iterations, each with interpreter overhead.</p>"),
            card("<h3>Vectorised</h3><pre style='margin:8px 0'><code>Z = np.matmul(A_in, W) + B\n"
                 "A_out = g(Z)</code></pre>"
                 "<p>One call into compiled, parallel, cache-friendly library code. Same answer.</p>"))
        + decode([
            ("vectorisation", "“doing it all at once”", "Expressing a computation as whole-array operations instead of element-by-element loops."),
            ("<code>np.matmul</code>", "“matrix multiply”", "The workhorse. Internally calls BLAS, a decades-old, viciously optimised library."),
            ("<code>A_in</code>", "“capital A in”", "Not one example — <b>all</b> the examples, stacked as rows. That is where the second speedup comes from."),
            ("GPU", "“graphics card”", "Thousands of small cores. Useless for one multiplication, extraordinary for a million at once."),
        ])
        + key("""<p>Vectorisation changes <em>nothing</em> about the maths and everything about the running
time. It is the reason deep learning became practical: the same equations, expressed so that hardware built
for video games could run them.</p>""")

        + h2("⏱", "Roughly how much faster?")
        + table(["Operation", "Loop in Python", "NumPy vectorised", "Typical speedup"],
                [["dot product of 10⁶ numbers", "~300 ms", "~1 ms", "~300×"],
                 ["(1000×400) @ (400×25) matmul", "minutes", "~10 ms", "thousands×"],
                 ["same matmul on a GPU", "—", "~0.1 ms", "another ~10–100×"]])
        + """<p>(Order-of-magnitude figures, hardware dependent — but the shape of the story is stable and
that shape is what matters.) The gap is not because NumPy is clever maths; it is because a Python loop pays
interpreter overhead per element, while NumPy hands a contiguous block of memory to compiled code that uses
SIMD instructions and multiple cores.</p>"""

        + h2("🕳", "Traps")
        + trap("""<p><b>Vectorising before it works.</b> Write the loop, check the numbers, <em>then</em>
vectorise and assert the two agree: <code>np.allclose(slow, fast)</code>. Debugging a wrong matmul with no
reference implementation is genuinely miserable.</p>""")
        + trap("""<p><b>Assuming a GPU always helps.</b> For small models the cost of shipping data to the
GPU exceeds the compute saved. GPUs win on <em>large</em> batches and <em>large</em> matrices.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("Does vectorising change the predictions?",
             "<p>No — up to tiny floating-point differences from a different summation order. Same maths, "
             "same answer.</p>"),
            ("Why can a layer’s neurons be computed in parallel but layer 2 cannot start before layer 1?",
             "<p>Within a layer, no neuron needs another neuron’s output — independent. Across layers, "
             "layer 2’s input <em>is</em> layer 1’s output — a strict dependency.</p>"),
            ("What does A_in contain in the vectorised version?",
             "<p>Every training example, one per row. So one matmul computes every neuron for every example "
             "simultaneously.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("docs", "https://numpy.org/doc/stable/user/basics.broadcasting.html",
             "NumPy — broadcasting",
             "How <code>+ b</code> quietly adds a length-3 vector to a (1000, 3) matrix. Essential to the vectorised form."),
            ("paper", "https://arxiv.org/abs/1404.5997",
             "Krizhevsky (2014) — One weird trick for parallelizing convolutional neural networks",
             "A readable look at how the parallelism is actually organised across GPUs."),
            ("docs", "https://developer.nvidia.com/blog/cuda-refresher-cuda-programming-model/",
             "NVIDIA — the CUDA programming model",
             "If you want to know what “thousands of cores” concretely means. Optional, and interesting."),
        ])
    )))

# ============================================================ 14
L.append(dict(
    slug="14-matrix-multiplication", title="Matrix multiplication", mins=10, tag="maths",
    lede="The dot product, slowly. Two lists in, one number out — and the reason it is exactly the "
         "operation a neuron needs.",
    body=(
        pretest("""<p>1 apple, 2 bananas, 3 cherries at £4, £5, £6. <b>Work out the bill</b>, then guess what changes if there are four different shops with four price lists.</p>""",
        """<p>£32 for one shop. Watch for how a grid of such bills is exactly a matrix multiplication.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>You have a shopping list: 1 apple, 2 bananas, 3 cherries. And a price list: apples £4,
bananas £5, cherries £6.</p>
<p>How much is the basket? Pair each item with its price, multiply, add it all up:
1×4 + 2×5 + 3×6 = 4 + 10 + 18 = <b>£32</b>.</p>
<p>That is a dot product. Two lists go in, one number comes out. And it is <em>exactly</em> what a neuron
does — inputs are the quantities, weights are the prices, z is the total bill.</p>""")

        + h2("🔢", "The maths, decoded")
        + eqp([
            ("<var>a</var> · <var>w</var>", "dot-product-f0", "multiply matching entries, add them up"),
            ' <span class="op">=</span> ',
            ('<span class="big">Σ</span><sub><var>i</var></sub> <var>a</var><sub><var>i</var></sub><var>w</var><sub><var>i</var></sub>',
             "sigma", "one term per pair"),
            ' <span class="op">=</span> <var>a</var><sub>1</sub><var>w</var><sub>1</sub> + <var>a</var><sub>2</sub><var>w</var><sub>2</sub> + … + <var>a</var><sub><var>n</var></sub><var>w</var><sub><var>n</var></sub>',
        ], "the dot product — click a part")
        + decode([
            ("·", "“dot”", "The dot product. Not ordinary multiplication — it includes the summing."),
            ("<span class='big'>Σ</span>", "“sum over i”", "A loop, written as a symbol. “Add up the following, for every i.”"),
            ("<var>a</var><sup>T</sup>", "“a transpose”", "Flipping a column vector into a row (or vice versa) so the shapes line up. a·w and a<sup>T</sup>w mean the same number."),
            ("length", "“they must match”", "Both lists must be the same length. Length 3 and length 4 cannot be paired up, and NumPy will refuse."),
        ])
        + key("""<p>A dot product collapses two lists into <b>one number</b>. That collapse is the whole
reason it fits a neuron: many inputs arrive, exactly one z must come out.</p>""")

        + h2("🎬", "Watch it move")
        + demo("dotprod", "Pair, multiply, add",
               "each element pairs with its partner, and the running total grows")

        + h2("🔬", "Transpose, and why it keeps appearing")
        + """<p>Transposing swaps rows and columns: <code>A.T</code> in NumPy, A<sup>T</sup> in maths.</p>"""
        + eqp([
            '<var>A</var> = <span class="paren">[</span> 1 &nbsp; 2 &nbsp; 3 <span class="paren">]</span> &nbsp;&nbsp;(1×3)&nbsp;&nbsp;→&nbsp;&nbsp; ',
            ('<var>A</var><sup>T</sup> = <span class="paren">[</span> 1 ; 2 ; 3 <span class="paren">]</span> &nbsp;&nbsp;(3×1)',
             "transpose-f0", "rows become columns"),
        ], "same three numbers, different orientation — click it", small=True)
        + """<p>It appears constantly because matrix multiplication only works when the inner dimensions
match. If you have a (3×1) and need a (1×3), transposing is how you get there. Nothing deeper is going on —
it is shape plumbing.</p>"""
        + note("""<p>Geometrically, a·w = |a||w|cos θ: it measures how much two vectors point the same way.
Positive means aligned, zero means perpendicular, negative means opposed. This is a lovely intuition for
what a neuron is doing — <b>asking how much the input resembles the pattern stored in its weights</b>.</p>""",
               "The geometric meaning (optional but beautiful)")

        + h2("🕳", "Traps")
        + trap("""<p><b><code>a * w</code> is not <code>np.dot(a, w)</code>.</b> The star multiplies
element-wise and gives you back a list of the same length. <code>np.dot</code> multiplies <em>and sums</em>,
giving one number.</p>""")
        + trap("""<p><b>Mismatched lengths.</b> <code>ValueError: shapes (3,) and (4,) not aligned</code> is
NumPy telling you there is nothing to pair the fourth element with.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("Compute [2, 0, −1] · [3, 5, 4].",
             "<p>2×3 + 0×5 + (−1)×4 = 6 + 0 − 4 = <b>2</b>.</p>"),
            ("Two vectors have a dot product of 0. What does that mean geometrically?",
             "<p>They are <b>perpendicular</b> — completely unrelated directions. A neuron whose weights are "
             "perpendicular to the input outputs z = b, ignoring the input entirely.</p>"),
            ("Why does a neuron need a dot product rather than element-wise multiplication?",
             "<p>Because a neuron must produce a single number z. Element-wise multiplication would leave "
             "you with a list.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("video", "https://www.3blue1brown.com/lessons/dot-products",
             "3Blue1Brown — Dot products and duality",
             "The geometric meaning, done properly. Fourteen minutes and genuinely worth it."),
            ("book", "http://immersivemath.com/ila/ch03_dotproduct/ch03.html",
             "Immersive Linear Algebra — chapter 3",
             "Free, fully interactive textbook. Drag the vectors and watch the dot product change."),
            ("docs", "https://numpy.org/doc/stable/reference/generated/numpy.dot.html",
             "numpy.dot",
             "Note how its behaviour changes with input dimensionality — a genuine source of bugs."),
        ])
    )))

# ============================================================ 15
L.append(dict(
    slug="15-matmul-rules", title="Matrix multiplication rules", mins=11, tag="maths",
    lede="From one dot product to a whole grid of them. The shape rule — (m×n)(n×p) = (m×p) — and how to "
         "never get it wrong again.",
    body=(
        pretest("""<p>A is (2×3), B is (3×4). <b>Which of A×B and B×A is legal, and what shape does the legal one give?</b></p>""",
        """<p>Watch the inner numbers. Watch also for why order matters here when it never did for ordinary multiplication.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>One dot product = one shopping basket priced up.</p>
<p>Now imagine <b>three</b> customers with three different baskets, and <b>four</b> shops with four
different price lists. How much does each customer pay at each shop? That’s 3 × 4 = 12 different totals,
and you can lay them out in a grid: customers down the side, shops across the top.</p>
<p>That grid is a matrix multiplication. Every cell of it is one ordinary dot product — a row meeting a
column.</p>""")

        + h2("🔢", "The maths, decoded")
        + eqp([
            '<var>Z</var><span class="paren">[</span><var>i</var>, <var>j</var><span class="paren">]</span> <span class="op">=</span> ',
            ('<span class="paren">(</span>row <var>i</var> of <var class="hl-a">A</var><span class="paren">)</span> <span class="op">·</span> <span class="paren">(</span>column <var>j</var> of <var class="hl-b">W</var><span class="paren">)</span>',
             "dot-product-f0", "multiply matching entries, add them up"),
        ], "every cell is a dot product — click it")
        + eqp([
            ('<span class="hl-a">(<var>m</var> × <var class="hl-p">n</var>)</span> <span class="op">×</span> <span class="hl-b">(<var class="hl-p">n</var> × <var>p</var>)</span> <span class="op">=</span> <span class="hl-g">(<var>m</var> × <var>p</var>)</span>',
             "matmul-f0", "inner numbers must match"),
        ], "the shape rule — the inner numbers must match, and they disappear — click it")
        + decode([
            ("<var>m</var>", "“rows of the first”", "Survives into the answer, as its rows."),
            ("<var class='hl-p'>n</var>", "“the inner dimension”", "Must be <b>identical</b> on both sides. It is what gets paired up and summed away — it never appears in the answer."),
            ("<var>p</var>", "“columns of the second”", "Survives into the answer, as its columns."),
            ("<code>@</code>", "“matmul”", "Python’s matrix-multiply operator. <code>A @ W</code> is <code>np.matmul(A, W)</code>."),
        ])
        + key("""<p>Write the two shapes next to each other: <b>(2×3)(3×4)</b>. If the middle two numbers
match, it is legal, and the answer is the outer two: <b>(2×4)</b>. This one trick prevents most shape errors
in the entire specialization.</p>""")

        + h2("🎬", "Watch it move")
        + demo("matmul", "Filling in the answer, one cell at a time",
               "watch which row and which column feed each cell of Z")

        + h2("⚠️", "Matrix multiplication is not commutative")
        + """<p><b>A × W and W × A are different</b>, and usually one of them is not even legal. If A is
(2×3) and W is (3×4), then A×W is fine (inner 3s match) but W×A needs 4 to equal 2 — it simply does not
exist. Order matters, always.</p>"""
        + table(["Expression", "Shapes", "Legal?", "Result"],
                [["A @ W", "(2×3)(3×4)", "✅ inner 3 = 3", "(2×4)"],
                 ["W @ A", "(3×4)(2×3)", "❌ 4 ≠ 2", "ValueError"],
                 ["A @ A", "(2×3)(2×3)", "❌ 3 ≠ 2", "ValueError"],
                 ["A @ A.T", "(2×3)(3×2)", "✅ inner 3 = 3", "(2×2)"]])

        + h2("🔬", "Why this is exactly a neural network layer")
        + """<p>Put your examples in the rows of A and your neurons in the columns of W:</p>"""
        + eqp([
            ('<span class="hl-a">A</span> <span class="paren">(</span><var>m</var> examples × <var>n</var> features<span class="paren">)</span>', "matrix-f0", "one row per example"),
            ' <span class="op">×</span> ',
            ('<span class="hl-b">W</span> <span class="paren">(</span><var>n</var> features × <var>p</var> neurons<span class="paren">)</span>', "matrix-f0", "one column per neuron"),
            ' <span class="op">=</span> <span class="hl-g">Z</span> <span class="paren">(</span><var>m</var> examples × <var>p</var> neurons<span class="paren">)</span>',
        ], "one multiply = every example through every neuron — click a part", small=True)
        + """<p>Cell Z[i, j] is “example i, as judged by neuron j”. The features dimension n is the thing
that gets summed away — which is precisely the weighted sum a neuron performs. The correspondence is not an
analogy; it is the same arithmetic written in a different notation.</p>"""

        + h2("🕳", "Traps")
        + trap("""<p><b>Multiplying in the wrong order to “fix” an error.</b> If the shapes do not match, one
of your matrices is probably built the wrong way round. Swapping the operands hides the problem instead of
fixing it — check what your rows and columns are supposed to <em>mean</em> first.</p>""")
        + trap("""<p><b><code>*</code> vs <code>@</code> in NumPy.</b> <code>A * W</code> is element-wise
(and will broadcast into something surprising). <code>A @ W</code> is matrix multiplication. This is a
silent, expensive bug.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("(64 × 400) @ (400 × 25) — legal? What shape comes out?",
             "<p>Legal (inner 400s match). Result <b>(64 × 25)</b>: 64 examples, 25 neurons.</p>"),
            ("You have X of shape (1000, 400) and W of shape (25, 400). How do you multiply them?",
             "<p><code>X @ W.T</code> → (1000,400)(400,25) = (1000, 25). W was stored transposed; "
             "<code>.T</code> fixes it.</p>"),
            ("What happened to the inner dimension n?",
             "<p>It was summed away. Each output cell is a sum over all n pairings — n disappears from the "
             "result shape by design.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("video", "https://www.3blue1brown.com/lessons/matrix-multiplication",
             "3Blue1Brown — Matrix multiplication as composition",
             "Matrix multiply as “do this transformation, then that one”. This is the intuition that makes it stop feeling arbitrary."),
            ("play", "http://matrixmultiplication.xyz/",
             "matrixmultiplication.xyz",
             "Type in two matrices and watch the rows slide across the columns. Silly and effective."),
            ("docs", "https://numpy.org/doc/stable/reference/generated/numpy.matmul.html",
             "numpy.matmul",
             "Including the broadcasting rules for stacks of matrices (3-D and beyond)."),
        ])
    )))

# ============================================================ 16
L.append(dict(
    slug="16-matmul-code", title="Matrix multiplication code", mins=9, tag="code",
    lede="The payoff: dense() with no loop at all. Two lines of NumPy that run a whole layer over a whole "
         "dataset.",
    body=(
        pretest("""<p><code>A * B</code> and <code>A @ B</code> in NumPy. <b>Guess whether they do the same thing.</b></p>""",
        """<p>They do not, and the wrong one often runs without error. Watch for which is which.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Everything you have learned this week collapses into two lines. One line does the
multiply-and-add for every neuron and every example at once. The other squashes the results.</p>
<p>That’s it. That’s a layer.</p>""")

        + h2("💻", "The vectorised dense()")
        + code("""
def dense(A_in, W, B):
    Z = np.matmul(A_in, W) + B     # (m,n) @ (n,units) -> (m,units)
    A_out = g(Z)                   # element-wise: same shape out
    return A_out
""")
        + """<p>Compare it to the looped version from Lesson 11. Same function, same output, no
<code>for</code>, no <code>W[:, j]</code>, no index arithmetic to get wrong.</p>"""
        + decode([
            ("<code>A_in</code>", "“all the inputs”", "(m × n): m examples in the rows, n features in the columns."),
            ("<code>W</code>", "“the weight matrix”", "(n × units): one <b>column</b> per neuron — the orientation from Lesson 10."),
            ("<code>B</code>", "“the bias row”", "Shape (1 × units). Broadcasting adds it to every row of Z automatically."),
            ("<code>Z</code>", "“capital Z”", "(m × units). Row i, column j = the z of neuron j for example i."),
            ("<code>g(Z)</code>", "“squash everything”", "Applied element-wise. sigmoid of a matrix is just sigmoid of every entry."),
        ], head=("Name", "Say it out loud", "Shape and meaning"))

        + h2("🎬", "Watch it move")
        + demo("matmulcode", "One line, one whole layer",
               "A_T @ W + b, with the shapes lined up")

        + h2("🔬", "Broadcasting, since it is doing real work here")
        + """<p><code>Z</code> is (m × units) but <code>B</code> is (1 × units). Adding them looks illegal,
and NumPy does it anyway: it <b>stretches</b> B down all m rows. That is broadcasting, and it saves you
writing a loop over examples just to add a bias.</p>"""
        + code("""
Z = np.array([[1., 2., 3.],
              [4., 5., 6.]])        # (2, 3)
B = np.array([[10., 20., 30.]])     # (1, 3)
Z + B
# array([[11., 22., 33.],
#        [14., 25., 36.]])          # B was reused for every row
""")
        + warn("""<p>Broadcasting is helpful right up until it isn’t. If B were shape (3, 1) instead of
(1, 3), NumPy would <em>still</em> produce an answer — a (2,3)+(3,1) → error here, but in many shape
combinations it silently produces a bigger, wrong matrix. Print shapes when results look odd.</p>""")

        + h2("🧾", "The whole week, in one box")
        + card("""<pre style="margin:0"><code>def dense(A_in, W, B):
    return g(np.matmul(A_in, W) + B)

def sequential(X):
    A1 = dense(X,  W1, B1)
    A2 = dense(A1, W2, B2)
    A3 = dense(A2, W3, B3)
    return A3</code></pre>
<p style="margin:12px 0 0">Six lines. That is a complete, working, fully vectorised neural network doing
forward propagation over an entire dataset. Everything else this course adds is about <em>finding</em> the
Ws and Bs.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Getting W the wrong way round.</b> If your W is stored as (units × n) — some texts do
— you need <code>np.matmul(A_in, W.T)</code>. Always check <code>W.shape</code> before assuming.</p>""")
        + trap("""<p><b>Using <code>np.dot</code> for matrices out of habit.</b> It works for 2-D, but its
behaviour for higher dimensions differs from <code>matmul</code>. Use <code>matmul</code> / <code>@</code>
for matrices and reserve <code>dot</code> for vectors.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("A_in is (1000, 400), W is (400, 25), B is (1, 25). What shape is A_out?",
             "<p><b>(1000, 25)</b>. One row per example, one column per neuron.</p>"),
            ("Rewrite the looped dense() as the vectorised one — what disappeared?",
             "<p>The <code>for</code> loop, the <code>W[:, j]</code> slicing, the <code>np.zeros</code> "
             "pre-allocation, and the per-neuron bias indexing. All of it is now implied by the shapes.</p>"),
            ("Why is g applied element-wise rather than to the whole matrix at once?",
             "<p>Because each neuron squashes its own z independently. Sigmoid of a matrix means sigmoid of "
             "every entry, separately — there is no mixing between entries.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("docs", "https://numpy.org/doc/stable/user/basics.broadcasting.html",
             "NumPy broadcasting — the rules in full",
             "Read the “General Broadcasting Rules” box until it is boring. It pays off all course."),
            ("lab", "../../C2%20-%20Advanced%20Learning%20Algorithms/week1/C2W1A1/C2_W1_Assignment.ipynb",
             "Week 1 assignment — my_dense_v (vectorised)",
             "The graded exercise is literally this function. You will also verify it matches your looped version."),
            ("lab", "../../C2%20-%20Advanced%20Learning%20Algorithms/week1/optional-labs/C2_W1_Lab03_CoffeeRoasting_Numpy.ipynb",
             "Optional lab: Coffee Roasting in NumPy",
             "End-to-end forward propagation with nothing but NumPy. The best possible end to this week."),
        ])
    )))

WEEK = dict(
    course="C2", week=1, title="Neural Networks",
    time="~6–8 h with labs",
    goal="Understand what a neuron computes, how layers stack, and how to run a network forwards — "
         "in TensorFlow, in NumPy loops, and vectorised.",
    lessons=L,
)
