# -*- coding: utf-8 -*-
"""The slow read for the Course 2 reference entries.

Reference sheet only. Every number computed before it was written.
"""
from walkkit import p, expr, chain, chainset, steps, cases, values, point, ascii_art

W = {

# ============================================================ W1  neural networks
"c2w1-neuron": (
    p("""One artificial neuron. If Week 3 of Course 1 made sense, you already know this
&mdash; it is the same thing with a new name.""")
    + expr("z = w &middot; x + b\na = g(z)", "dot, add the bias, squash")
    + point("""<b>One neuron IS one logistic regression unit.</b> Not similar to, not
inspired by &mdash; the same two lines of arithmetic. A neural network is many of these
wired together.""")
    + values([("w", "learned", "how much this neuron <b>trusts each input</b>"),
              ("b", "learned", "its <b>default mood</b> &mdash; how easily it fires "
                               "with no input at all"),
              ("a", "computed", "the <b>activation</b>: the one number it passes on")],
             "the three letters")
    + p("""Everything else in Course 2 is bookkeeping about how to arrange thousands of
these and how to work out all their gradients at once.""")
),

"c2w1-hidden-layer": (
    p("""What does a hidden layer actually buy you over plain logistic regression? One
thing, and it is a big one.""")
    + point("""<b>Learned features.</b> In Course 1 you invented <code>x&#8321;x&#8322;</code>
or <code>x&sup2;</code> by hand, using what you knew about houses. A hidden layer invents
its own intermediate features and learns which ones are worth keeping.""")
    + chain(["raw inputs", "hidden layer", "useful features", "decision"],
            "the layer in the middle is doing the feature engineering for you")
    + p("""So the work you did by hand in C1 W2 &mdash; deciding that
<i>frontage &times; depth</i> matters &mdash; is the work the hidden layer now does
automatically. That is the whole pitch.""")
    + point("""One honest warning. The names people give hidden units &mdash;
&ldquo;affordability&rdquo;, &ldquo;brand awareness&rdquo; &mdash; are a <b>story told
afterwards</b>. Nothing in training assigns meanings. The units find whatever combinations
reduce the cost, and those are often not describable in words at all.""")
),

"c2w1-layer": (
    p("""A <b>layer</b> is several neurons that all read the <b>same</b> input vector and
each produce one number.""")
    + ascii_art("""                 +--> neuron 1 --> a1
   x  ---------> +--> neuron 2 --> a2      units=3
                 +--> neuron 3 --> a3

   every neuron sees ALL of x.
   no neuron sees any other neuron.""")
    + point("""<code>units=3</code> sets the <b>length of that layer's output vector</b>.
Nothing else. Not the number of inputs, not the number of examples, not the number of
layers. Just how many numbers come out.""")
    + p("""And neurons within a layer <b>never talk to each other</b>. That independence is
exactly what lets the whole layer be computed as one matrix multiply &mdash; there is
nothing sequential to wait for.""")
),

"c2w1-params": (
    p("""Counting parameters is worth doing by hand once, because it is the fastest way to
catch a wiring mistake.""")
    + expr("weights = n &times; p\nbiases  = p", "n inputs, p units")
    + steps(["Every one of the <b>p</b> neurons needs one weight per input, so that is "
             "<b>n &times; p</b> weights.",
             "Every neuron also gets <b>one</b> bias of its own, so that is <b>p</b> more.",
             "Total: <b>np + p</b>."])
    + values([("400 inputs, 25 units", "10,000 weights", "400 &times; 25"),
              ("plus biases", "25", "one per unit"),
              ("total", "10,025", "for a single layer")],
             "worked, on a realistic layer")
    + point("""<code>model.summary()</code> prints exactly these totals. Comparing it
against a hand count takes ten seconds and catches transposed dimensions before you spend
an hour training something wired wrongly.""")
),

"c2w1-master-eq": (
    p("""One equation describes every unit in every layer of every network in Course 2.""")
    + expr("a&#11388;&#8317;&#737;&#8318; = g( w&#11388;&#8317;&#737;&#8318; &middot; a&#8317;&#737;&#8315;&#185;&#8318; + b&#11388;&#8317;&#737;&#8318; )",
           "&ldquo;the activation of unit j in layer l is g of: unit j's weights in layer "
           "l, dotted with the whole output of the previous layer, plus its bias&rdquo;")
    + steps(["Take <b>a&#8317;&#737;&#8315;&#185;&#8318;</b> &mdash; everything the "
             "<b>previous</b> layer produced.",
             "Dot it with <b>this</b> unit's own weight vector.",
             "Add <b>this</b> unit's own bias.",
             "Squash with <b>g</b>. That is one number, and it goes into the next layer."])
    + point("""The tidy part: <b>a&#8317;&#8304;&#8318; = x</b>. The input is defined to be
&ldquo;layer 0's output&rdquo;, so the formula works for layer 1 with no special case. The
first layer is not different; it just reads a layer that happens to be your data.""")
),

"c2w1-brackets": (
    p("""The single most common notation error in Course 2, and it is entirely avoidable.""")
    + values([("a<sup>[2]</sup>", "square brackets", "<b>layer 2</b>. Never a power."),
              ("x<sup>(2)</sup>", "round brackets", "training <b>example</b> 2"),
              ("x<sup>2</sup>", "bare", "x <b>squared</b>")],
             "the three, again, because this one bites in Course 2")
    + point("""Reading <b>a<sup>[2]</sup></b> as &ldquo;a squared&rdquo; makes the whole
of forward propagation incomprehensible &mdash; and it is a very easy slip, because square
brackets look like an afterthought rather than notation.""")
),

"c2w1-weight-vec-len": (
    p("""A network is <b>4 &rarr; 5 &rarr; 3 &rarr; 1</b>. How long is
<b>w&#8322;<sup>[3]</sup></b> &mdash; the weight vector of unit 2 in layer 3?""")
    + steps(["Layer 3 reads whatever <b>layer 2</b> produced.",
             "Layer 2 has <b>3</b> units, so it produces <b>3</b> numbers.",
             "Unit 2 of layer 3 needs one weight for each of those. So the answer is "
             "<b>3</b>."])
    + point("""The rule, permanently: <b>a weight vector's length always equals the width
of the PREVIOUS layer.</b> Never its own layer, never the input size.""")
    + p("""And a trap hidden in the naming: unit <b>2</b> of layer 3 reads <b>every</b>
unit of layer 2, not just unit 2. The subscript names <i>which neuron this is</i>, not
<i>which input it looks at</i>. In a dense layer everything is connected to everything.""")
),

"c2w1-dense-cols": (
    p("""In <b>W</b> for a dense layer, which way round are the rows and columns? Get this
wrong and everything transposes.""")
    + cases([("Columns are NEURONS",
              "<code>W[:, j]</code> is neuron j's personal weight vector."),
             ("Rows are INPUT FEATURES",
              "One row per number arriving from the previous layer.")])
    + expr("W.shape == (2, 3)", "2 inputs, 3 neurons")
    + point("""This orientation is not arbitrary &mdash; it is chosen so the vectorised
version works with <b>no transposes</b>: <code>A_in @ W</code> is
<code>(m, 2) @ (2, 3) &rarr; (m, 3)</code>, every example against every neuron, in one
operation.""")
    + p("""If you find yourself sprinkling <code>.T</code> through a forward pass to make
the shapes agree, this convention is usually the thing you got backwards.""")
),

"c2w1-shapes": (
    p("""<b>(2,)</b> and <b>(1, 2)</b> hold the same two numbers and are not the same
thing. Keras will accept one and refuse the other.""")
    + cases([("np.array([200, 17]) &rarr; (2,)",
              "A <b>1-D</b> array. No rows, no columns &mdash; just two numbers in a row. "
              "Course 1 style. <b>Keras will not take it.</b>"),
             ("np.array([[200, 17]]) &rarr; (1, 2)",
              "A <b>matrix</b>: 1 row &times; 2 columns. One training example that has two "
              "features. This is what Course 2 wants.")],
            "count the brackets")
    + point("""The convention for the whole specialization from here on: <b>rows are
examples, columns are features.</b> Even one example is a table with one row. It feels like
pedantry until the first shape error, and then it is the only thing that matters.""")
),

"c2w1-dense-code": (
    p("""One layer, written the obvious way: one neuron at a time.""")
    + expr("def dense(a_in, W, b):\n"
           "    units = W.shape[1]\n"
           "    a_out = np.zeros(units)\n"
           "    for j in range(units):\n"
           "        w = W[:, j]\n"
           "        z = np.dot(w, a_in) + b[j]\n"
           "        a_out[j] = g(z)\n"
           "    return a_out")
    + steps(["<code>W.shape[1]</code> &mdash; how many <b>columns</b>, which is how many "
             "<b>neurons</b>.",
             "<code>W[:, j]</code> &mdash; all rows, column j. That is neuron j's own "
             "weights.",
             "<code>np.dot(w, a_in) + b[j]</code> &mdash; the z for that one neuron.",
             "<code>g(z)</code> &mdash; squash it, and store it in slot j."])
    + point("""<code>W.shape[1]</code>, <b>not</b> <code>[0]</code>. Position 0 is the
number of <b>inputs</b>. Using it loops the wrong number of times, and if the two happen to
be equal &mdash; a square W &mdash; it will run and silently do the wrong thing.""")
),

"c2w1-dense-vec": (
    p("""The same layer, for the whole batch, with no loop at all.""")
    + expr("def dense(A_in, W, B):\n"
           "    Z = np.matmul(A_in, W) + B\n"
           "    return g(Z)",
           "(m, n) @ (n, units) -> (m, units)")
    + point("""No loop, no slicing, no index arithmetic. <b>Every example against every
neuron, in one operation.</b> This is the version that runs on a GPU; the looped one never
will.""")
    + p("""<b>B</b> is <code>(1, units)</code> and broadcasting adds it to <b>every
row</b> &mdash; one bias per neuron, applied to all m examples, without writing that loop
either. This is the broadcasting rule from Foundations doing real work.""")
),

"c2w1-matmul-rule": (
    p("""The rule that decides whether a matrix multiplication is legal, and what comes
out.""")
    + expr("( m &times; n ) &times; ( n &times; p ) = ( m &times; p )",
           "the inner pair must match; the outer pair is the answer")
    + steps(["Write the two shapes side by side.",
             "Look at the <b>inner</b> two. If they match, it is legal.",
             "The <b>outer</b> two are the shape of the result.",
             "The inner dimension gets <b>summed away</b> &mdash; it never appears in the "
             "answer."])
    + point("""And <b>A@W is not W@A</b>. Usually one of the two is not even legal, which
is a mercy &mdash; when both are legal, you get a wrong answer with no complaint.""")
),

"c2w1-dotprod": (
    p("""Why must a neuron use a dot product rather than elementwise multiplication? There
is a practical answer and a nicer one.""")
    + cases([("The practical answer",
              "A neuron must produce a <b>single number</b> z. Elementwise multiplication "
              "leaves you holding a <b>list</b>, and there is nothing to squash."),
             ("The interesting answer",
              "<b>a &middot; w = |a||w| cos&theta;</b>. The dot product measures <b>how "
              "much the input resembles the pattern stored in the weights</b>.")],
            "two ways to see it")
    + point("""So a neuron is a <b>pattern detector</b>. Its weights are a template; the
dot product scores how well the incoming activation matches that template; the bias sets
how good a match has to be before it fires. That reading carries all the way to
attention.""")
),

"c2w1-vectorization": (
    p("""The maths of neural networks is from <b>1958</b> (the perceptron) and <b>1986</b>
(backpropagation). Nothing about it changed. Three other things did.""")
    + steps(["<b>Data.</b> The internet supplied millions of labelled examples, which "
             "had simply never existed before.",
             "<b>Compute.</b> GPUs made the matrix multiplies roughly <b>100&times;</b> "
             "cheaper &mdash; and matrix multiplies are almost all of the work.",
             "<b>Scale behaviour.</b> Classical algorithms <b>plateau</b> as you add data. "
             "Large networks keep improving."])
    + point("""That third point is the one that changed strategy rather than just speed.
If more data keeps helping, then collecting data becomes a <b>reliable</b> way to buy
performance &mdash; which is not true of most algorithms, and is why the last decade looked
the way it did.""")
),

"c2w1-drill-forwardprop": (
    p("""Work it on paper. One neuron: <b>w = [2, &minus;1]</b>, <b>b = 0.5</b>,
<b>x = [1, 3]</b>.""")
    + steps(["Multiply position by position: 2&times;1 = <b>2</b>, and "
             "&minus;1&times;3 = <b>&minus;3</b>.",
             "Add them: 2 + (&minus;3) = <b>&minus;1</b>.",
             "Add the bias: &minus;1 + 0.5 = <b>&minus;0.5</b>. That is <b>z</b>.",
             "Squash: g(&minus;0.5) = 1 / (1 + e<sup>0.5</sup>) = <b>0.378</b>."])
    + chain(["x = [1, 3]", "z = &minus;0.5", "a = 0.378"], "below 0.5 &mdash; this neuron does not fire")
    + point("""That two-step recipe &mdash; <b>dot-and-add, then squash</b> &mdash; is
identical at every unit of every layer. A network with a million parameters is doing
exactly this, a million times, and nothing else.""")
),

# ============================================================ W2  training
"c2w2-three-steps": (
    p("""Training in TensorFlow is three lines, and each one is something you already built
by hand in Course 1.""")
    + values([("Sequential([...])", "define the model", "&larr; what f(x) is allowed to be"),
              ("model.compile(loss=...)", "say what wrong means", "&larr; the cost function"),
              ("model.fit(X, y, epochs=)", "minimise it", "&larr; gradient descent")],
             "the three steps, and their Course 1 twins")
    + point("""Only <code>fit</code> changes the weights. <code>compile</code> just
<b>records settings</b> &mdash; it does no work at all. People lose hours to this: they
change the loss, re-run <code>compile</code>, and wonder why nothing moved.""")
),

"c2w2-bce": (
    p("""The same loss as Course 1 Week 3, and a distinction in vocabulary that is worth
getting right.""")
    + expr("L(f, y) = -y log(f) - (1 - y) log(1 - f)", "binary cross-entropy")
    + cases([("loss &mdash; L", "the error on <b>one</b> example."),
             ("cost &mdash; J", "the <b>average</b> loss over all m examples: "
                                "<b>J = (1/m) &Sigma; L</b>.")],
            "loss is per-example; cost is the average")
    + point("""It sounds like pedantry and it is not: the whole of Course 2 Week 3 talks
about <b>J<sub>train</sub></b> versus <b>J<sub>cv</sub></b>, which are costs over different
sets. Confusing the two makes that week much harder than it is.""")
),

"c2w2-relu": (
    p("""ReLU is the simplest function in the course and it is why deep networks train at
all.""")
    + expr("g(z) = max(0, z)", "negative becomes 0; positive is left alone")
    + ascii_art("""     g(z)
      |        /
      |       /
      |      /
      |     /
  ----+----*--------- z
      |    0
   flat here    slope exactly 1 here""")
    + cases([("The slope is exactly 1 on the positive side",
              "So gradients pass through <b>undiminished</b>. Stack fifty layers and a "
              "gradient still arrives at the first one."),
             ("One max, no exp",
              "<code>max(0, z)</code> is a comparison. <code>e&#8315;&#7859;</code> is a "
              "transcendental function. Meaningfully faster, over billions of calls.")],
            "two reasons it replaced the sigmoid in hidden layers")
    + point("""The sigmoid's slope <b>peaks at 0.25</b> and is smaller nearly everywhere.
Stack ten sigmoid layers and the gradient reaching the first one is multiplied by at most
<b>0.25<sup>10</sup> &asymp; 0.00000095</b>. The early layers receive essentially nothing.
That is the vanishing gradient problem, and ReLU simply does not have it.""")
),

"c2w2-dying-relu": (
    p("""ReLU has one failure mode, and it is permanent.""")
    + steps(["A unit's <b>z is negative for every single training example</b>.",
             "So its output is always 0.",
             "So its gradient is always <b>0</b>.",
             "So its weights <b>never update</b>.",
             "So its z never changes. It is dead, for the rest of training."])
    + point("""Notice the loop closes on itself. There is no path back &mdash; nothing that
happens later can revive it, because the only thing that could change its weights is a
gradient, and its gradient is structurally zero.""")
    + p("""Two fixes. A <b>lower learning rate</b> stops the huge early step that knocked it
there in the first place. Or <b>Leaky ReLU</b>, which returns <code>0.01z</code> instead of
<code>0</code> on the negative side &mdash; a tiny slope, but not zero, so a dead unit can
still crawl back.""")
),

"c2w2-activation-choice": (
    p("""Choosing activations is almost mechanical once you know the four output cases.""")
    + values([("binary classification", "sigmoid", "one probability, 0 to 1"),
              ("regression, can go negative", "linear", "no squash at all"),
              ("regression, never negative", "ReLU", "prices, counts, durations"),
              ("multiclass, pick one", "softmax", "probabilities that sum to 1")],
             "the OUTPUT layer &mdash; decided by the task")
    + point("""For <b>every hidden layer</b>: <b>ReLU</b>, almost always. This is not a
close call any more, and it is the one place in machine learning where the default is
genuinely just the right answer.""")
    + p("""One vocabulary trap: &ldquo;<b>linear activation</b>&rdquo; means <b>no</b>
activation &mdash; <code>g(z) = z</code>. It sounds like a thing being applied and it is
the absence of one.""")
),

"c2w2-why-nonlinear": (
    p("""Without non-linear activations, depth buys you <b>nothing at all</b>. Not a little
&mdash; nothing. Here is the proof, and it is two lines.""")
    + expr("a&#8317;&#178;&#8318; = W&#8317;&#178;&#8318;( W&#8317;&#185;&#8318;x + b&#8317;&#185;&#8318; ) + b&#8317;&#178;&#8318;\n"
           "     = ( W&#8317;&#178;&#8318;W&#8317;&#185;&#8318; ) x + ( ... )\n"
           "     = W&prime;x + b&prime;",
           "two layers collapse into one")
    + point("""Two matrices multiplied together are <b>just another matrix</b>. So a
100-layer linear network is algebraically identical to a <b>single</b> layer &mdash; exactly
zero extra expressive power, and a hundred times the compute.""")
    + p("""Each ReLU adds a <b>kink</b>, and kinks cannot be flattened out by multiplying
matrices. That is the entire reason activations exist: not to squash, not to normalise, but
to stop the layers from collapsing. The build lane's file 03 demonstrates this collapse
numerically, if you want to see it happen.""")
),

"c2w2-softmax": (
    p("""Softmax turns a list of arbitrary scores into a list of probabilities. Two moves,
each doing one job.""")
    + expr("a&#11388; = e&#7859;&#11388; / &Sigma;&#8342; e&#7859;&#8342;", "= P(y = j | x)")
    + cases([("exp", "makes everything <b>positive</b>. Probabilities cannot be negative, "
                     "and raw scores routinely are."),
             ("&divide; by the total", "makes them <b>sum to exactly 1</b>. Now it is a "
                                       "distribution.")],
            "the two moves")
    + point("""Softmax is the <b>only</b> activation where each output depends on <b>all
the others</b> &mdash; the denominator contains every score. That coupling is precisely
what forces the sum to 1, and it is why you cannot compute one softmax output on its
own.""")
),

"c2w2-softmax-shift": (
    p("""Do <b>z = [10, 1, 1]</b> and <b>z = [110, 101, 101]</b> give the same softmax
output? Every score is a hundred larger.""")
    + point("""<b>Yes &mdash; identical.</b> Softmax depends only on the <b>differences</b>
between the scores. Adding the same constant to every z changes nothing at all, because it
multiplies the top and the bottom by the same factor, which cancels.""")
    + chain(["[10, 1, 1]", "[0.99975, 0.00012, 0.00012]"], "and [110, 101, 101] gives exactly the same")
    + p("""This is not a curiosity. It is the basis of the standard numerical fix:""")
    + expr("exp(z - np.max(z))", "subtract the largest score first")
    + point("""Now the largest exponent is <b>e&#8304; = 1</b> and everything else is
smaller, so <b>overflow is impossible</b> &mdash; and because shifting changes nothing, the
answer is exactly the same. Every real softmax implementation does this.""")
),

"c2w2-from-logits": (
    p("""<code>from_logits=True</code> is a small argument that fixes a real numerical
problem.""")
    + steps(["It tells Keras the output layer is <b>linear</b> &mdash; it hands over raw "
             "scores, not probabilities.",
             "The <b>loss</b> then applies the sigmoid or softmax itself.",
             "And it uses an <b>algebraically rearranged</b> formula that never builds the "
             "intermediate probability at all."])
    + point("""Which matters because a probability can round to exactly <b>0</b> or
<b>1</b> in floating point, and then <code>log</code> of it is infinite. If the number is
never formed, it can never round.""")
    + expr("-log( 1 / (1 + e&#8315;&#7859;) )  =  log(1 + e&#8315;&#7859;)",
           "same maths, and the right-hand side never divides by anything")
    + point("""The catch: your output layer must actually be <b>linear</b>. Leave a sigmoid
on it <i>and</i> pass <code>from_logits=True</code> and the squash is applied <b>twice</b>.
It trains, badly, and nothing warns you.""")
),

"c2w2-multiclass-vs-label": (
    p("""Two words one letter apart, describing genuinely different problems.""")
    + cases([("Multi-CLASS &mdash; exactly one is right",
              "&ldquo;Which digit is this?&rdquo;<br>y is an <b>integer</b>, e.g. 7<br>"
              "<code>Dense(N, 'softmax')</code><br>outputs <b>sum to 1</b><br>"
              "outputs are <b>coupled</b>"),
             ("Multi-LABEL &mdash; several can be true",
              "&ldquo;Is there a car? a bus? a person?&rdquo;<br>y is a <b>vector</b>, "
              "e.g. [1, 0, 1]<br><code>Dense(N, 'sigmoid')</code><br>outputs sum to "
              "<b>anything</b><br>outputs are <b>independent</b>")],
            "the two, side by side")
    + point("""The tell is the question &ldquo;<b>can two answers be true at once?</b>&rdquo;
If yes, softmax is actively wrong &mdash; it is built to make the options compete, and here
they should not.""")
),

"c2w2-adam": (
    p("""Plain gradient descent uses <b>one</b> &alpha; for every parameter, forever. Adam
keeps a separate one for <b>each</b> parameter and adapts it as it goes.""")
    + cases([("Gradient keeps pointing the same way",
              "You are on a long steady slope. <b>Increase</b> that parameter's step "
              "&mdash; you are being too timid."),
             ("Gradient keeps flip-flopping",
              "You are bouncing across a valley. <b>Decrease</b> it &mdash; you are "
              "overshooting.")],
            "the two adaptations, and they are common sense")
    + expr("w &larr; w - &alpha; &middot; m&#770; / ( &radic;v&#770; + &epsilon; )")
    + values([("m", "running mean of the gradient", "momentum &mdash; which way it has been going"),
              ("v", "running mean of the gradient squared", "how <b>volatile</b> it has been"),
              ("&epsilon;", "a tiny number", "so you never divide by zero")],
             "what the letters hold")
    + point("""Read the fraction: divide by how volatile this parameter has been. Noisy
parameters get small steps; steady ones get large steps. That is the whole idea, and it is
why Adam is the default in practice.""")
),

"c2w2-conv": (
    p("""A convolutional layer differs from a dense one in exactly two ways, and both are
<b>restrictions</b>.""")
    + cases([("Each unit sees only a small window",
              "Not the whole input &mdash; just a patch, say 3&times;3 pixels."),
             ("All units share the same weights",
              "There is <b>one</b> kernel, slid across the whole image. Not one set of "
              "weights per position.")],
            "two restrictions")
    + point("""Both are restrictions, and both are the <b>point</b>. Far fewer parameters,
faster training, less overfitting &mdash; and a detector learned in one corner of the image
<b>works everywhere</b>, because it is literally the same weights being reused.""")
    + p("""That last property has a name: <b>translation equivariance</b>. A dense layer
would have to learn &ldquo;edge in the top-left&rdquo; and &ldquo;edge in the
bottom-right&rdquo; as two completely separate things.""")
),

"c2w2-backprop-cost": (
    p("""Backpropagation is not a clever way to do calculus. It is a clever way to do
calculus <b>cheaply</b>, and the cost is the entire reason deep learning exists.""")
    + values([("nudge each parameter separately", "N forward passes",
               "the obvious method. Hopeless."),
              ("forward-mode autodiff", "still N sweeps", "better bookkeeping, same cost"),
              ("backprop", "1 forward + 1 backward",
               "<b>about two passes, regardless of N</b>")],
             "how much it costs to get all N derivatives")
    + point("""For a million parameters that is <b>two</b> passes instead of a
<b>million</b>. Not a speed-up you optimise your way to &mdash; a different complexity
class, and the difference between training a network and never training one.""")
),

"c2w2-chain-rule": (
    p("""The chain rule is how a slope travels backwards through a chain of operations.""")
    + expr("&part;J/&part;w = (&part;J/&part;d)(&part;d/&part;a)(&part;a/&part;c)(&part;c/&part;w)",
           "multiply the local slopes along the path")
    + point("""Each node only ever needs to know <b>its own little multiplier</b> &mdash;
how much its output moves when its input moves. It knows nothing about the network as a
whole, and it does not need to.""")
    + steps(["Start at the end, with <b>&part;J/&part;J = 1</b>.",
             "Walk <b>right to left</b>, multiplying by each node's local slope as you "
             "pass it.",
             "By the time you reach a weight, you have its gradient."])
    + p("""One practical consequence: the <b>forward values must be kept</b>, because each
local slope depends on what that node saw on the way in. This is why training uses far more
memory than prediction does &mdash; and why halving the batch size is the first thing to try
when you run out of it.""")
),

"c2w2-mse-vs-bce": (
    p("""Mean squared error on a classification problem <b>runs</b>. It just trains
badly.""")
    + point("""The gradient is <b>tiny exactly where the model is confidently wrong</b>
&mdash; which is precisely where you most need a large correction.""")
    + p("""The mechanism: the gradient of squared error picks up a <b>g&prime;(z)</b>
factor, and the sigmoid's slope is nearly zero once it has saturated. So a model that is
99% confident and completely wrong produces almost no gradient and barely
learns.""")
    + point("""Cross-entropy fixes it because the <b>1/f</b> from the logarithm
<b>cancels</b> the g&prime;. Same reason as Course 1 Week 3: the sigmoid and the log loss
are a matched pair whose derivatives were designed to annihilate each other.""")
),

"c2w2-drill-softmax": (
    p("""Work it on paper. <b>z = [1, 2, 3, 4]</b>. What is the softmax for the largest
score?""")
    + steps(["Exponentiate each: <b>2.72, 7.39, 20.09, 54.60</b>.",
             "Add them: <b>84.79</b>.",
             "Divide the one you want: 54.60 &divide; 84.79 = <b>0.644</b>."])
    + values([("a&#8321;", "0.032", "from z = 1"),
              ("a&#8322;", "0.087", "from z = 2"),
              ("a&#8323;", "0.237", "from z = 3"),
              ("a&#8324;", "0.644", "from z = 4"),
              ("total", "1.000", "as it must")],
             "all four")
    + point("""Look at the exaggeration. z = 4 is only <b>4&times;</b> z = 1, but its
probability comes out <b>20&times;</b> larger. Exponentiating widens every gap &mdash; which
is what makes softmax decisive, and also why a slightly wrong score can produce a very
confident wrong answer.""")
),

}

W.update({

# ============================================================ W3  advice
"c2w3-diagnostic": (
    p("""This is the most valuable sentence in Course 2, and it is two numbers.""")
    + cases([("J_train is high", "&rarr; <b>high bias</b>. Underfitting. It cannot even "
                                 "fit the data it was shown."),
             ("J_cv is much bigger than J_train", "&rarr; <b>high variance</b>. "
                                                  "Overfitting. It memorised rather than "
                                                  "learned.")],
            "two numbers, two diagnoses")
    + point("""<b>J<sub>train</sub> tells you about bias. The GAP tells you about
variance.</b> One sentence, and it is most of the diagnostic value of the entire week.""")
    + p("""Both can be true at once &mdash; a model that fits the training set poorly
<i>and</i> generalises even worse. That is not a contradiction, it is a model that is
simultaneously too simple in some ways and too flexible in others, and it needs both fixes.""")
),

"c2w3-three-sets": (
    p("""Why three splits and not two? Because of one uncomfortable fact about
measurement.""")
    + values([("train", "60%", "fits <b>w</b> and <b>b</b>"),
              ("cross-validation", "20%", "chooses the <b>model</b>: degree, &lambda;, "
                                          "architecture, features"),
              ("test", "20%", "read <b>once</b>, at the very end")],
             "the three sets and their jobs")
    + point("""<b>Any number you use to make a decision becomes optimistically
biased.</b> Try twelve polynomial degrees and pick the best, and that best score is partly
luck &mdash; you selected for it.""")
    + p("""So selecting on the test set quietly converts it into <b>another training
set</b>, and the final number you report is no longer an estimate of anything. The
cross-validation set exists to absorb that bias so the test set can stay clean.""")
    + point("""&ldquo;Read once&rdquo; is meant literally. Looking at the test score,
changing something, and looking again has already spent it.""")
),

"c2w3-fix-table": (
    p("""Six things to try. Three make the model <b>less</b> flexible, three make it
<b>more</b>. Applying the wrong three makes everything worse.""")
    + cases([("Fix high VARIANCE  (overfitting)",
              "&bull; get more training examples<br>&bull; try a <b>smaller</b> set of "
              "features<br>&bull; <b>increase</b> &lambda;"),
             ("Fix high BIAS  (underfitting)",
              "&bull; get <b>additional</b> features<br>&bull; add polynomial features<br>"
              "&bull; <b>decrease</b> &lambda;")],
            "the six, sorted")
    + point("""There is no memorisation needed here: <b>every variance fix makes the model
less flexible, and every bias fix makes it more flexible.</b> Work out which way you need to
go, and the list sorts itself.""")
),

"c2w3-more-data": (
    p("""&ldquo;Get more data&rdquo; is the standard advice and it is on <b>one</b> of the
two lists only.""")
    + point("""More data does <b>nothing</b> for high bias. If the model is too simple to
capture the pattern, showing it ten times as many examples of that pattern will not help
&mdash; it will fit them all equally badly.""")
    + p("""It is also the <b>most expensive</b> item on either list. Collecting and
labelling data costs money and months, in a way that changing &lambda; does not.""")
    + point("""Which is exactly why the diagnostic is worth the ten minutes it takes.
Teams routinely spend a quarter collecting data for a model that was never going to benefit
from it &mdash; and a learning curve would have said so on day one.""")
),

"c2w3-baseline": (
    p("""&ldquo;J<sub>train</sub> = 10.8%&rdquo; is meaningless on its own. High compared
to <b>what</b>?""")
    + cases([("If humans score 0.5% on this audio",
              "then 10.8% is <b>terrible</b>. There is a huge amount of avoidable error."),
             ("If humans score 10.6% on this audio",
              "then 10.8% is <b>nearly perfect</b>. The audio is simply that noisy.")],
            "the same number, two opposite conclusions")
    + point("""So you need a <b>baseline</b> &mdash; human performance, a competitor, or a
previous system &mdash; and then there are <b>two gaps</b>, not one.""")
    + values([("baseline &rarr; J_train", "avoidable bias", "how much of your error is "
                                                            "actually fixable"),
              ("J_train &rarr; J_cv", "variance", "how much you are overfitting")],
             "the two gaps")
    + point("""Chasing error below the noise floor of your own labels is a way to spend a
year overfitting to label mistakes. The baseline tells you when to stop.""")
),

"c2w3-learning-curves": (
    p("""A learning curve plots error against <b>how much training data you used</b>. It
answers the expensive question: <b>will more data help?</b>""")
    + ascii_art("""  HIGH BIAS                     HIGH VARIANCE
  err                           err
   |  J_cv  ______                |  J_cv \\___
   |  J_tr  ______  <- both flat  |            \\___   still falling
   |                              |
   |........... baseline          |  J_tr ____/------
   +--------------- m             +--------------- m
   small gap, both high           big gap, cv still dropping
   -> more data will NOT help     -> more data WILL help""")
    + cases([("High bias",
              "Both curves <b>flatten early</b>, well above the baseline, with a "
              "<b>small gap</b>.<br>&rarr; more data will <b>not</b> help."),
             ("High variance",
              "J_train sits <b>below</b> the baseline, the gap is <b>large</b>, and J_cv "
              "is <b>still falling</b> at the right edge.<br>&rarr; more data <b>will</b> "
              "help.")],
            "which shape are you looking at")
    + point("""One counter-intuitive detail: <b>J<sub>train</sub> RISES with m</b>. Fitting
1,000 points well is genuinely harder than fitting 10. A training error that climbs is
healthy, not broken.""")
),

"c2w3-nn-recipe": (
    p("""Two questions, two fixes, and a loop. This is the whole development process for a
neural network.""")
    + steps(["<b>Does it do well on the TRAINING set</b> (compared to the baseline)?<br>"
             "<b>No</b> &rarr; use a <b>bigger network</b>. Go back to 1.",
             "<b>Yes</b> &rarr; does it do well on the <b>CV set</b>?<br>"
             "<b>No</b> &rarr; get <b>more data</b> (or more regularisation). Go back to 1.",
             "<b>Yes</b> &rarr; <b>done</b>."])
    + point("""What makes this work is a fact peculiar to neural networks: <b>a larger
network with proper regularisation is almost never worse</b> than a smaller one. So &ldquo;go
bigger&rdquo; is a safe move, and the loop always has somewhere to go.""")
    + p("""The costs are compute and time, not accuracy. That is a very different trade from
the one classical models offer, where a bigger model genuinely does risk being worse.""")
),

"c2w3-error-analysis": (
    p("""Error analysis is unglamorous, manual, and routinely worth more than any
architecture change.""")
    + steps(["Take the <b>misclassified</b> cross-validation examples.",
             "If there are more than about <b>100</b>, sample 100. That is enough.",
             "<b>Read them.</b> Invent categories as you go &mdash; and let them "
             "<b>overlap</b>; one example can be in three.",
             "<b>Count</b> each category.",
             "Work on the <b>biggest</b> one that is also <b>tractable</b>."])
    + point("""The classic outcome: the team has argued for two weeks about a category that
turns out to be <b>3</b> of the 100, while the real problem &mdash; 43 of them &mdash; is
something nobody had named. An afternoon of reading settles arguments that months of
opinion cannot.""")
    + p("""&ldquo;Biggest <b>and</b> tractable&rdquo; matters. The largest category is
worthless if you have no idea how to fix it; take the second largest that you can actually
attack.""")
),

"c2w3-augmentation": (
    p("""Data augmentation makes new training examples by distorting the ones you have.
There is exactly one rule.""")
    + point("""<b>The distortion must be representative of what actually happens in real
data.</b> That is the whole rule, and it decides every case.""")
    + values([("speech &rarr; add caf&eacute; noise, car noise, a bad line", "&#10003;",
               "your users really will call from cars"),
              ("clean scanned text &rarr; random per-pixel noise", "&#10007;",
               "a scanner will never produce that. You are teaching it about nothing"),
              ("handwritten digits &rarr; mirror flipping", "&#10007;",
               "a mirrored <b>2</b> is not a 2. You are teaching it something false")],
             "three cases, decided by the one rule")
    + point("""The failure mode is subtle: bad augmentation does not throw an error, it
just spends your compute teaching the model about a world that does not exist &mdash; and
in the mirror case, actively teaches it something wrong.""")
),

"c2w3-transfer": (
    p("""Transfer learning starts from somebody else's trained network instead of from
random numbers. Two options, chosen by how much data you have.""")
    + cases([("1 &middot; Freeze",
              "Train <b>only the new output layer</b>. Everything else is held fixed.<br>"
              "For a <b>very small</b> dataset &mdash; tens to hundreds of examples."),
             ("2 &middot; Fine-tune",
              "Train <b>all</b> parameters, but starting from theirs rather than from "
              "random.<br>For a <b>larger</b> dataset &mdash; thousands or more.")],
            "the two options")
    + point("""Replace <b>only the last layer</b>. Everything before it learned generic
things &mdash; edges, textures, shapes, or for language, grammar and word relationships.
The final layer is the only genuinely task-specific part.""")
    + p("""When you unfreeze, <b>drop the learning rate</b> substantially. Those weights are
already good; a large step will destroy in one iteration what somebody spent a fortune in
compute learning.""")
),

"c2w3-precision-recall": (
    p("""Two numbers that are constantly confused. There is a trick that makes it
permanent.""")
    + expr("precision = TP / (TP + FP)\nrecall    = TP / (TP + FN)",
           "same top, different bottom")
    + cases([("Precision asks", "of those we <b>flagged</b>, how many were <b>real</b>?"),
             ("Recall asks", "of those that were <b>real</b>, how many did we <b>catch</b>?")])
    + point("""The trick: <b>precision's denominator is what you PREDICTED. Recall's is
what was TRUE.</b> Everything else follows from that, including which one a false positive
hurts.""")
    + p("""Hold onto the pair with a scenario. A cancer screen with high recall and low
precision <b>frightens healthy people</b>. One with high precision and low recall <b>misses
sick ones</b>. Both are bad; which is worse is a question about the world, not the
model.""")
),

"c2w3-accuracy-trap": (
    p("""On a dataset that is 0.5% positive, accuracy is worse than useless.""")
    + expr('print("healthy")', "a model with no inputs and no parameters")
    + point("""This scores <b>99.5% accuracy</b> and catches <b>nobody</b>. It is not a bad
model; it is not a model at all, and accuracy cannot tell the difference.""")
    + p("""On skewed data, accuracy is essentially a measurement of <b>how rare the positive
class is</b>. It tells you about your dataset, not your model.""")
    + point("""So report <b>precision, recall and F1</b>. Never accuracy alone &mdash; and
be suspicious of anyone who does, especially when the number is impressively high.""")
),

"c2w4-drill-entropy": (
    p("""Work it on paper. A node has <b>10 examples, 8 of one class</b>.""")
    + steps(["p = 8/10 = <b>0.8</b>",
             "&minus;0.8 &times; log&#8322;(0.8) = <b>0.258</b>",
             "&minus;0.2 &times; log&#8322;(0.2) = <b>0.464</b>",
             "Add them: <b>0.722</b>"])
    + values([("H(0.5)", "1.000", "maximally mixed &mdash; a coin flip"),
              ("H(0.8)", "0.722", "<b>this node</b> &mdash; fairly pure"),
              ("H(1.0)", "0.000", "completely pure &mdash; no surprise at all")],
             "for comparison")
    + point("""Notice the smaller group contributes <b>more</b> (0.464 against 0.258)
despite being only a fifth of the examples. Rare things are surprising, and entropy is
measuring surprise.""")
),

"c2w3-f1": (
    p("""F1 combines precision and recall into one number, and the choice of <b>harmonic</b>
mean is doing real work.""")
    + expr("F1 = 2 &middot; P &middot; R / ( P + R )", "the harmonic mean of the two")
    + point("""A harmonic mean sits <b>close to the smaller of the two</b>. That is the
entire reason it was chosen.""")
    + chainset([(["P = 1.00, R = 0.01", "F1 = 0.02"], "harmonic &mdash; correctly damning"),
                (["P = 1.00, R = 0.01", "ordinary mean = 0.505"], "which would look fine")],
               "a model that flags one thing, correctly, and misses everything else")
    + point("""F1 <b>refuses to be impressed</b> by a model that is excellent at one half
and useless at the other. An ordinary average would call that model average; F1 calls it
what it is.""")
),

"c2w3-threshold": (
    p("""The model gives you a probability. <b>You</b> turn it into an action, and which way
you lean is not a modelling question.""")
    + cases([("Raise it &mdash; say 0.9",
              "precision <b>&uarr;</b>, recall <b>&darr;</b><br>Use when a <b>false alarm "
              "is expensive</b> &mdash; you only act when very sure."),
             ("Lower it &mdash; say 0.15",
              "recall <b>&uarr;</b>, precision <b>&darr;</b><br>Use when a <b>miss is much "
              "worse</b> &mdash; screening for a treatable disease.")],
            "which way, and when")
    + point("""<b>The right threshold depends on what an action costs, and that is a
question about the world.</b> No amount of validation data can answer it, because the data
does not know that a missed tumour is worse than a needless scan.""")
),

"c2w3-fairness": (
    p("""Your model is <b>92.4%</b> accurate overall. That number is the beginning of the
investigation, not the end of it.""")
    + point("""The next thing to measure is <b>performance per subgroup</b> &mdash;
accuracy, false positives and false negatives, broken down.""")
    + p("""Aggregate accuracy hides subgroup failure <b>by construction</b>. A group that is
6% of your data can be served terribly and move the headline number by less than a
percentage point. The average is not lying; it is just answering a question you did not
mean to ask.""")
    + point("""And removing the sensitive attribute does <b>not</b> fix it. The model finds
proxies &mdash; postcode, name, purchase history &mdash; and reconstructs the group anyway.
You cannot audit for a bias you have made yourself blind to, which is why you measure the
breakdown rather than deleting the column.""")
),

"c2w3-leakage": (
    p("""Three ways a train/test split can lie to you, and none of them raises an error.""")
    + values([("splitting after sorting", "different populations",
               "the halves are not the same kind of data. <b>Shuffle first</b> &mdash; "
               "unless it is a time series, where you must split <b>by time</b>"),
              ("duplicate entities", "the same thing in both sets",
               "the same house, patient or user in train and test. The model recognises "
               "it rather than generalising"),
              ("scaling before splitting", "&mu; and &sigma; saw everything",
               "test information leaked into training through the scaler")],
             "the three")
    + point("""What they share: your test score comes out <b>too good</b>, you ship with
confidence, and the model underperforms in production for reasons nobody can reproduce. A
suspiciously excellent test score deserves suspicion, not celebration.""")
),

# ============================================================ W4  trees
"c2w4-tree-decisions": (
    p("""A whole tree-learning algorithm is two decisions, repeated.""")
    + cases([("Which feature to split on?",
              "The one that makes the two resulting groups <b>purest</b> &mdash; maximum "
              "<b>information gain</b>."),
             ("When to stop?",
              "&bull; node is 100% one class<br>&bull; max depth reached<br>"
              "&bull; gain too small<br>&bull; too few examples left")],
            "the two decisions")
    + point("""Every stopping rule exists for <b>one</b> reason: <b>keeping the tree
small</b>. A tree that is allowed to grow until every leaf is pure will memorise the
training set perfectly and generalise terribly.""")
    + p("""So a decision tree has no learning rate, no gradient and no cost function to
minimise by descent. It is greedy search &mdash; take the best split available right now,
recurse, stop early. That difference is why it needs no feature scaling.""")
),

"c2w4-entropy": (
    p("""Entropy measures <b>mess</b>. One formula, and two endpoints worth knowing by
heart.""")
    + expr("H(p) = -p log&#8322;(p) - (1-p) log&#8322;(1-p)", "for a two-class node")
    + values([("H = 0", "completely pure", "p = 0 or p = 1. Everything is one class."),
              ("H = 1", "maximum mess", "p = 0.5. Exactly one bit of uncertainty."),
              ("H(0.8) = H(0.2)", "0.722", "<b>symmetric</b> &mdash; 80/20 and 20/80 are "
                                           "equally messy")],
             "the landmarks")
    + point("""The intuition in one sentence: <b>&ldquo;if I reach into this bag, how
surprised will I be?&rdquo;</b> All one colour, no surprise, H = 0. Fifty-fifty, maximum
surprise, H = 1.""")
    + p("""Base <b>2</b> gives the answer in <b>bits</b>, which is why a 50/50 bag comes out
at exactly 1 &mdash; one yes/no question's worth of uncertainty. That is the whole reason
the base is 2 rather than e.""")
),

"c2w4-infogain": (
    p("""Information gain is how much mess a split removes. There is one part everybody
forgets, and forgetting it breaks the algorithm completely.""")
    + expr("gain = H(root) - ( w_left &middot; H(left) + w_right &middot; H(right) )",
           "the mess before, minus the WEIGHTED mess after")
    + point("""The <b>weights</b> are the fraction of examples going each way, and they are
the part people drop.""")
    + p("""Without them: split off a <b>single</b> example into its own branch. That branch
is perfectly pure, H = 0, so the average of the two entropies looks fantastic. Every time.
The tree would learn to shave off one example per split, forever.""")
    + point("""With the weights, that pure branch is multiplied by <b>1/m</b> and counts for
almost nothing &mdash; which is right, because it explains almost nothing. This is the most
common bug when implementing a tree from scratch.""")
),

"c2w4-id-column": (
    p("""A customer-ID column would score a <b>perfect</b> information gain. That is not a
triumph; it is the algorithm failing loudly.""")
    + steps(["Split on ID and every leaf holds <b>exactly one</b> example.",
             "Every leaf is therefore <b>perfectly pure</b>, H = 0.",
             "So the gain is <b>maximal</b> &mdash; better than any real feature."])
    + point("""But the rule &ldquo;<b>if ID = 4471 then cat</b>&rdquo; tells you
<b>nothing</b> about a new customer, who has an ID the tree has never seen. It is pure
memorisation with a perfect training score.""")
    + p("""C4.5 addresses this properly with <b>gain ratio</b>, which penalises features
with very many distinct values. The practical fix is simpler: <b>never feed an ID column to
a tree.</b> Any high-cardinality identifier &mdash; order number, timestamp, email &mdash;
has the same problem.""")
),

"c2w4-continuous": (
    p("""Trees split on yes/no questions. A continuous feature like weight has no natural
yes/no, so the tree invents one.""")
    + steps(["<b>Sort</b> the examples by that feature.",
             "Consider each <b>midpoint</b> between consecutive distinct values &mdash; "
             "that is <b>m &minus; 1</b> candidate thresholds.",
             "Compute the <b>information gain</b> for each one.",
             "Keep the best. That threshold, and that gain, become the feature's score."])
    + point("""This is also exactly why <b>trees need no feature scaling</b>. The algorithm
only ever asks &ldquo;is this value above or below that one?&rdquo; &mdash; a comparison,
which is unchanged by multiplying every value by a thousand. Gradient descent cares about
scale because it takes <i>steps</i>; a tree never does.""")
),

"c2w4-regtree": (
    p("""One substitution turns a classification tree into a regression tree. Everything
else is untouched.""")
    + cases([("Classification",
              "measure mess with <b>entropy</b><br>split by <b>information gain</b><br>"
              "leaf predicts the <b>majority class</b>"),
             ("Regression",
              "measure mess with <b>variance</b><br>split by <b>variance reduction</b><br>"
              "leaf predicts the <b>mean</b>")],
            "swap the impurity measure, and that is all")
    + point("""Recursion, stopping rules, one-hot encoding, continuous thresholds &mdash;
all identical. The tree never knew what it was predicting; it only ever knew how to measure
mess.""")
    + p("""One property worth noticing: a regression tree's output is a <b>staircase</b>,
not a curve. It predicts one constant per leaf, so it cannot extrapolate beyond the range it
was trained on at all. Feed it a house bigger than any it has seen and it returns the mean
of its biggest leaf.""")
),

"c2w4-onehot": (
    p("""Why not just map {red, green, blue} to {0, 1, 2}? It is shorter and it is
wrong.""")
    + point("""Because <b>ordinal encoding tells the model that blue is bigger than
red</b>, and twice green. For unordered categories that is simply a lie, and the model will
act on it &mdash; a threshold like &ldquo;colour &gt; 1.5&rdquo; is meaningless but perfectly
learnable.""")
    + cases([("Unordered &mdash; red / green / blue",
              "<b>one-hot</b>. Three columns, one of them 1. No false ordering."),
             ("Genuinely ordered &mdash; S &lt; M &lt; L",
              "<b>ordinal is correct, and better</b>. One-hot would throw the order away, "
              "and the order is real information.")],
            "the choice depends on whether the order is real")
    + point("""So this is not &ldquo;always one-hot&rdquo;. It is: <b>encode the structure
that actually exists</b>, and no more.""")
),

"c2w4-why-ensemble": (
    p("""A single decision tree is <b>high variance</b>, and the reason is startlingly
small.""")
    + steps(["The root split is chosen by a single <b>argmax</b> over feature scores.",
             "Suppose two features score <b>0.281</b> and <b>0.278</b>.",
             "Change a handful of training examples and those two swap order.",
             "A <b>different root</b> is chosen &mdash; and <b>everything below it</b> is "
             "now built on a different foundation."])
    + point("""So a tiny change in the data produces a completely different tree. That
instability is what &ldquo;high variance&rdquo; means, and it is why trees are almost never
used one at a time.""")
    + p("""Averaging fixes it &mdash; but only if the models make <b>different</b> mistakes.
Three identical trees average to exactly one tree. That single requirement is what the next
two entries are about: bootstrapping and feature subsampling exist purely to force the trees
apart.""")
),

"c2w4-bootstrap": (
    p("""Draw m examples from m, <b>with replacement</b>. How many of the originals turn
up?""")
    + expr("1 - (1 - 1/m)&#7504;   &rarr;   1 - 1/e   &asymp;   0.632",
           "as m gets large, it converges")
    + values([("m = 10", "0.651", "already close"),
              ("m = 100", "0.634", "closer"),
              ("m = 1000", "0.632", "there"),
              ("the limit", "0.6321", "1 &minus; 1/e, exactly")],
             "the fraction of distinct originals that appear")
    + point("""So about <b>63%</b> appear, and the other <b>37%</b> do not. Those missing
ones are called <b>out-of-bag</b>, and they are a <b>free validation set</b> for that
particular tree &mdash; data it genuinely never saw, at no cost.""")
    + p("""<code>replace=True</code> is the whole trick. Without it you get a
<b>permutation</b> of the same data, every tree sees exactly the same examples, and every
tree comes out identical &mdash; which averages to nothing.""")
),

"c2w4-random-forest": (
    p("""A random forest is bagging plus <b>one</b> extra idea, and the extra idea is what
makes it work.""")
    + steps(["For b = 1&hellip;B: draw a <b>bootstrap sample</b>.",
             "Train a tree on it &mdash; <b>but at every node</b>, choose the split from a "
             "<b>random subset of k &asymp; &radic;n features</b>.",
             "Predict by <b>majority vote</b> (or the average, for regression)."])
    + point("""Step 2 is the addition. Without feature subsampling, a single dominant
feature wins the root split in <b>every</b> tree, and all B trees end up nearly identical
&mdash; which is exactly the thing averaging cannot fix.""")
    + p("""Forcing each node to choose from a random handful means the dominant feature is
<b>absent</b> from roughly half the choices, so other features get to lead sometimes. The
trees genuinely disagree, and only then is the average worth more than the parts.""")
),

"c2w4-boosting": (
    p("""Two ensembles that sound similar and are opposites in almost every respect.""")
    + cases([("Random forest",
              "trees built <b>independently</b>, in parallel<br>"
              "sampling is <b>uniformly random</b><br>"
              "<b>deep</b>, fully grown trees<br>"
              "rarely overfits<br>almost no tuning"),
             ("Boosting / XGBoost",
              "trees built <b>sequentially</b>, each fixing the last<br>"
              "sampling <b>focuses on current errors</b><br>"
              "<b>shallow</b> trees, depth 3&ndash;6<br>"
              "can overfit<br>needs tuning")],
            "the two, side by side")
    + point("""The dividing line is <b>independent versus sequential</b>, and everything
else follows from it. Independent trees can be built in parallel and cannot compound each
other's mistakes. Sequential trees are more accurate and must be built one at a time.""")
),

"c2w4-boost-shallow": (
    p("""Boosted trees are kept deliberately shallow &mdash; depth 3 to 6, when a lone tree
might go to 30.""")
    + point("""Because each tree only needs to make a <b>small correction</b>. <b>The
ensemble supplies the power</b>, not the individual tree.""")
    + p("""A deep tree would fit its own residuals almost perfectly &mdash; and since those
residuals are largely noise by that point, it would be memorising noise. The sequential
process then <b>amplifies</b> that: the next tree fits the errors of a tree that was already
overfitting.""")
    + point("""It is also why boosting <b>cannot parallelise across trees</b>: tree b needs
the errors of trees 1&hellip;b&minus;1, which do not exist until they are built. XGBoost is
fast because it parallelises <b>within</b> each tree's split search instead.""")
),

"c2w4-tree-vs-nn": (
    p("""Which model, for which data? On this one the answer is unusually clear-cut.""")
    + cases([("Tabular / spreadsheet data",
              "<b>Trees first</b> &mdash; XGBoost. Fast, no scaling needed, readable, and "
              "still the thing to beat on most tabular problems."),
             ("Images, audio, text",
              "<b>Neural networks</b>, no contest. Trees have no way to exploit the fact "
              "that adjacent pixels are related.")],
            "the split")
    + point("""The neural network's decisive long-term advantage is <b>composability</b>.
Everything is differentiable, so you can chain several networks together and train the whole
chain <b>end to end</b> with one loss.""")
    + p("""You cannot do that with trees. A tree is not differentiable, so it cannot pass a
gradient back to whatever produced its inputs. That single property is why every large modern
system &mdash; vision, speech, language &mdash; is a stack of networks, and it is what makes
transfer learning and fine-tuning possible at all.""")
),

})
