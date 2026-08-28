# -*- coding: utf-8 -*-
"""C4 · Week 3 — The transformer block."""
from kit import (kid, key, warn, trap, note, card, eq, eqp, decode, table, demo,
                 quiz, links, code, h2, grid2, grid3, pretest, explain, lenses)

L = []

# ============================================================ 1
L.append(dict(
    slug="01-positional-encoding", title="Positional encoding — putting order back", mins=13, tag="core",
    lede="Attention is order-blind by construction. Since Week 1 established that order is meaning, "
         "something has to put it back — and the fix is stranger and simpler than you would expect.",
    body=(
        pretest("""<p>Attention computes a weighted average over positions. <b>Guess what happens to the output if you shuffle the input words</b> — and whether attention can tell.</p>""",
        """<p>Watch for the fact that an average does not care about order. That is a problem, and the fix is added to the input rather than built into the mechanism.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Attention takes a weighted average. An average does not care what order things
arrived in — average 3, 7 and 5 in any order and you still get 5. So attention is <b>completely
blind to word order</b>, which after Week 1 should alarm you.</p>
<p>The fix does not change attention at all. Instead, before anything happens, a distinctive pattern
of numbers is <b>added to each embedding</b> depending on its position. Word 1 gets one pattern,
word 2 gets another. The word vector now carries a fingerprint of where it sat, and attention can
use that like any other information.</p>""")

        + lenses(
            """<p>Numbering the pages of a manuscript before dropping it.</p>
<p>The pages are now shuffle-proof — not because anything stops them scattering, but because each
one carries its own position with it. Reassembly becomes possible from the pages alone.</p>
<p>Positional encoding is stamping a page number onto every word before handing the pile to a
mechanism that will inevitably shuffle it.</p>""",

            """<p>Formally, attention is <b>permutation-equivariant</b>: permute the inputs and the
outputs permute identically, with no other change. That is exactly the wrong property for
language.</p>
<p>The standard fix uses sinusoids of geometrically-spaced frequencies — the same idea as a Fourier
basis. Low-frequency components change slowly across the sequence and encode coarse position;
high-frequency ones distinguish neighbours.</p>""",

            """<p>A set of clock hands spinning at different speeds.</p>
<p>One hand goes round once per sequence, another once every ten positions, another every two. Read
all of them together and the combination is unique to one position — the same reason a clock with
hour, minute and second hands can name an instant.</p>""",

            """<p>This choice has direct consequences you may have noticed. A model's <b>context
window</b> is partly a statement about which positions it has encodings for; feed it positions
beyond what it was trained on and quality degrades.</p>
<p>Making that extrapolate better is an active area — RoPE, ALiBi and their relatives are all
positional-encoding schemes, and “this model now supports 128k context” is usually a story about
exactly this component.</p>""",

            """So the sinusoids below are a fingerprint per position, added to the embedding before
attention ever sees it.""")

        + h2("🎬", "Watch it move")
        + demo("c4-posenc", "A fingerprint per position",
               "several waves at different frequencies — read together they name a position")

        + h2("🔢", "The maths, decoded")
        + eq("""PE<sub>(<var>pos</var>, 2<var>i</var>)</sub> <span class="op">=</span>
sin<span class="paren">(</span><span class="frac"><span><var>pos</var></span><span>10000<sup>2<var>i</var>/<var>d</var></sup></span></span><span class="paren">)</span>
&nbsp;&nbsp;&nbsp; PE<sub>(<var>pos</var>, 2<var>i</var>+1)</sub> <span class="op">=</span>
cos<span class="paren">(</span>same<span class="paren">)</span>""",
             "even dimensions get a sine, odd ones a cosine")
        + decode([
            ("<var>pos</var>", "“position”", "Which slot in the sequence — 0, 1, 2, and so on."),
            ("<var>i</var>", "“i”", "Which pair of dimensions. Each pair gets its own frequency."),
            ("10000<sup>2i/d</sup>", "“the wavelength”", "Grows geometrically with i, so early dimensions oscillate fast and later ones slowly. That spread is what makes the combination unique."),
            ("sin and cos together", "“a pair per frequency”", "Because sin² + cos² = 1, each pair contributes exactly 1 to the squared length — so every position's encoding has the <b>same magnitude</b>."),
        ])

        + h2("🧮", "Computed, for d = 8")
        + table(["position", "dim 0 (sin, fast)", "dim 1 (cos, fast)", "dim 4 (sin, slow)", "dim 5 (cos, slow)"],
                [["0", "0.000", "1.000", "0.000", "1.000"],
                 ["1", "0.841", "0.540", "0.010", "1.000"],
                 ["2", "0.909", "−0.416", "0.020", "1.000"],
                 ["3", "0.141", "−0.990", "0.030", "1.000"],
                 ["5", "−0.959", "0.284", "0.050", "0.999"]])
        + """<p>The fast dimensions change sharply between neighbouring positions — useful for “is this
the next word?”. The slow ones barely move over five positions but would distinguish position 5 from
position 500. Every row has the same length, exactly 2.000, for the sin²+cos² reason above.</p>"""
        + explain("""<p>The encoding is <b>added</b> to the embedding rather than concatenated onto
it. <b>Why is adding acceptable — does it not corrupt the word's meaning?</b></p>""",
                  """<p>It does perturb it, and that is tolerable because d is large. In 512
dimensions there is room for the positional pattern to occupy directions that the embedding space
does not heavily use, and the model — which learns the embeddings <em>knowing</em> the encoding will
be added — simply arranges them compatibly. Concatenating would be cleaner in principle but would
cost dimensions in every downstream layer, and the empirical answer was that adding works.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Thinking positional encoding is learned.</b> The original sinusoidal version is
<em>fixed</em> — computed from a formula, never trained. Learned positional embeddings also exist and
are common; they work about as well and extrapolate worse.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("Why does attention need this at all?",
             "<p>Because a weighted average is order-blind. Without a positional signal, attention "
             "would produce identical output for a sentence and any shuffling of it — the exact "
             "failure Week 1 lesson 1 was about.</p>"),
            ("Why several frequencies rather than one?",
             "<p>One frequency either repeats (so distant positions collide) or changes too slowly to "
             "distinguish neighbours. A spread of frequencies gives a combination that is unique "
             "across the whole range, like clock hands.</p>"),
            ("What does “context window” have to do with this lesson?",
             "<p>Positions beyond what the model saw in training have encodings it never learned to "
             "interpret. Extending context is largely a positional-encoding problem, which is why "
             "schemes like RoPE and ALiBi exist.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("lesson", "f0/w1-16-probability.html", "F0 W1 · Probability",
             "Not directly used here, but the same “fingerprint that identifies a case” instinct."),
        ])
    )))

# ============================================================ 2
L.append(dict(
    slug="02-residuals", title="Residual connections", mins=12, tag="core",
    lede="One line of arithmetic — add the input back to the output — and suddenly networks can be "
         "a hundred layers deep instead of twenty. The reason is the vanishing gradient, again.",
    body=(
        pretest("""<p>Deep networks train badly because gradients shrink as they pass back through layers. <b>Guess a way to give the gradient a shortcut</b> that does not require changing the layers themselves.</p>""",
        """<p>Watch for a path that multiplies by exactly 1.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Instead of <code>output = layer(x)</code>, write <code>output = x +
layer(x)</code>.</p>
<p>That is the whole trick. The layer now learns what to <b>change</b> about x rather than what x
should <b>become</b>. And critically, there is now a path from output back to input that passes
through no weights at all — so the gradient can travel it undiminished, however deep the stack.</p>""")

        + lenses(
            """<p>Editing a document with tracked changes rather than retyping it.</p>
<p>A copy editor does not rewrite the manuscript from scratch; they mark what should differ. If they
have nothing to say about a paragraph, it survives untouched. Retyping every page risks losing
something on every pass, however careful the typist.</p>
<p>A residual layer is tracked changes. Doing nothing is free and lossless.</p>""",

            """<p>The gradient argument is exact. Differentiating <var>y</var> = <var>x</var> +
<var>f</var>(<var>x</var>) gives ∂<var>y</var>/∂<var>x</var> = 1 + <var>f</var>′(<var>x</var>) — the
<b>1</b> is an identity path that no chain of multiplications can shrink.</p>
<p>Without it, 12 layers each attenuating by 0.7 leave you with 0.7¹² ≈ 0.014 of the signal. With
it, the identity route delivers 1.0 regardless of depth.</p>""",

            """<p>A motorway with exits, next to a road that goes through every village.</p>
<p>Information can take the slow road through every layer, or stay on the motorway and skip. Both
exist simultaneously, and the network learns per layer how much traffic to divert.</p>""",

            """<p>This is the idea (from ResNet, 2015) that made very deep networks trainable at all,
and it won ImageNet by a wide margin at 152 layers — at a time when 20 was considered deep.</p>
<p>Every transformer uses it twice per block. A 96-layer model without residuals would not train; the
gradient would vanish long before reaching the early layers.</p>""",

            """So the plus sign below is doing more work than any other symbol in the architecture.""")

        + h2("🎬", "Watch it move")
        + demo("c4-residual", "The gradient's two routes",
               "compare the signal reaching layer 1 with and without the identity path")

        + h2("🔢", "The maths, decoded")
        + eq("""<var>y</var> <span class="op">=</span> <var>x</var> <span class="op">+</span>
Sublayer<span class="paren">(</span><var>x</var><span class="paren">)</span>""",
             "the input survives, whatever the sublayer does")
        + """<p>Differentiate it:</p>"""
        + eq("""<span class="frac"><span>∂<var>y</var></span><span>∂<var>x</var></span></span>
<span class="op">=</span> 1 <span class="op">+</span>
<span class="frac"><span>∂ Sublayer</span><span>∂<var>x</var></span></span>""",
             "the 1 is the shortcut, and it cannot be multiplied away")
        + table(["depth", "gradient without residual (×0.7 per layer)", "with residual"],
                [["1 layer", "0.700", "≥ 1"],
                 ["6 layers", "0.118", "≥ 1"],
                 ["12 layers", "<b>0.014</b>", "<b>≥ 1</b>"],
                 ["48 layers", "1.9 × 10⁻⁸", "≥ 1"]])
        + key("""<p>Notice this is the third time the same enemy has appeared: deep sigmoid networks
(C2 W2), RNNs across time (C4 W1), and now depth again. Multiplying many numbers below 1 is <b>the</b>
recurring structural problem in deep learning, and residuals are the cleanest answer to it.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Thinking the sublayer output is discarded.</b> It is added, not replaced —
<code>x + f(x)</code>, not <code>x</code>. The layer still does its work; it just cannot destroy what
came in.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("Why does the 1 in ∂y/∂x = 1 + f′(x) matter so much?",
             "<p>Because backpropagation multiplies these terms together across layers. A chain of "
             "factors that are each at least 1 cannot vanish, no matter how many there are.</p>"),
            ("What does a residual layer learn, in words?",
             "<p>What to <b>change</b> about its input, rather than what its input should become. If "
             "no change is useful, it can output near-zero and the input passes through "
             "untouched.</p>"),
            ("Where have you met this enemy before?",
             "<p>Twice. Deep sigmoid networks in C2 W2, and RNNs across time in C4 W1. Same "
             "arithmetic every time: many factors below 1, multiplied.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("paper", "https://arxiv.org/abs/1512.03385", "Deep Residual Learning (2015)",
             "The paper. Figure 1 — training error getting WORSE with more layers — is the problem this solves."),
        ])
    )))

# ============================================================ 3
L.append(dict(
    slug="03-layer-norm", title="Layer normalization", mins=12, tag="core",
    lede="Feature scaling from Course 1, applied inside the network instead of to the input, and "
         "repeated at every layer. Same formula, same reason.",
    body=(
        pretest("""<p>You standardised features in C1 W2 by subtracting the mean and dividing by the standard deviation. <b>Guess why you would do that again in the middle of a network</b> — the inputs were already scaled.</p>""",
        """<p>Watch for what happens to the numbers <em>between</em> layers, not at the input.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>You scaled the inputs in Course 1 so gradient descent behaved. But a layer's
<em>output</em> is not scaled — it can drift to any magnitude, and the next layer receives whatever
it gets.</p>
<p>Layer normalization re-standardises at each step: take each position's vector, subtract its mean,
divide by its standard deviation. It is exactly the z-score you already know, applied inside the
network rather than at the door.</p>""")

        + lenses(
            """<p>Re-tuning an instrument between movements rather than only before the concert.</p>
<p>Strings drift under tension and temperature. Tuning once at the start is not enough for a long
piece — you check again partway through, because everything downstream depends on it.</p>""",

            """<p>It is the z-score, with two additions: a learned gain and bias
(<var>γ</var> and <var>β</var>) so the layer can undo the normalisation if that turns out to be
useful.</p>
<p>The <b>layer</b> in the name matters: it normalises across the features of one position, not
across the batch. That makes it independent of batch size and of other examples — which is why it
suits sequences, where batch statistics are unreliable.</p>""",

            """<p>A row of dials being reset to centre before each stage of a process.</p>
<p>Whatever drift accumulated is removed, so every stage starts from a known state. The learned gain
and bias are a technician's override, in case some drift was actually wanted.</p>""",

            """<p>Where the normalisation sits turned out to matter a great deal. The original 2017
design placed it <em>after</em> the residual add (“post-norm”); nearly every model since 2020 places
it <em>before</em> the sublayer (“pre-norm”), because post-norm requires a carefully tuned learning-rate
warm-up to train stably at depth and pre-norm largely does not.</p>
<p>A one-line change of ordering, and it is the difference between a model that trains and one that
needs babysitting.</p>""",

            """So the formula below is C1 W2's z-score, and the only genuinely new parts are the two
learned parameters at the end.""")

        + h2("🎬", "Watch it move")
        + demo("c4-layernorm", "Drift in, standard out",
               "watch an unbalanced vector come back to mean 0 and standard deviation 1")

        + h2("🔢", "The maths, decoded")
        + eq("""LN<span class="paren">(</span><var>x</var><span class="paren">)</span>
<span class="op">=</span> <var>γ</var> <span class="op">·</span>
<span class="frac"><span><var>x</var> <span class="op">−</span> <var>μ</var></span><span><var>σ</var></span></span>
<span class="op">+</span> <var>β</var>""", "z-score, plus a learned gain and shift")
        + decode([
            ("<var>μ</var>, <var>σ</var>", "“mu and sigma”", "The mean and standard deviation <b>of this one position's vector</b> — computed across its d features, not across the batch."),
            ("<var>γ</var>", "“gamma”, the gain", "A learned scale, one per feature. Lets the layer restore a spread if the normalisation removed something useful."),
            ("<var>β</var>", "“beta”, the shift", "A learned offset, one per feature. Together with γ, this means the layer can learn to undo the normalisation entirely."),
        ])

        + h2("🧮", "Worked")
        + """<p>Take one position's vector <var>x</var> = [2, 8, 4, 6]. Mean = 5, standard deviation =
2.2361.</p>"""
        + table(["", "before", "(x − 5) ÷ 2.2361", "after"],
                [["", "2", "(2−5)/2.2361", "<b>−1.342</b>"],
                 ["", "8", "(8−5)/2.2361", "<b>+1.342</b>"],
                 ["", "4", "(4−5)/2.2361", "<b>−0.447</b>"],
                 ["", "6", "(6−5)/2.2361", "<b>+0.447</b>"]])
        + """<p>The result has mean exactly 0 and standard deviation exactly 1 — check by adding the
four numbers. Then <var>γ</var> and <var>β</var> are applied, and they are learned.</p>"""

        + h2("🕳", "Traps")
        + trap("""<p><b>Confusing it with batch normalization.</b> Batch norm standardises each feature
across the <em>batch</em>; layer norm standardises each example across its <em>features</em>. Batch
norm makes an example's output depend on which other examples happen to be in the batch, which is
awkward for sequences and impossible at generation time.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("What exactly is averaged over?",
             "<p>The d features of a single position's vector. Not the batch, and not the sequence — "
             "which is what makes it independent of batch size.</p>"),
            ("Why include γ and β if the whole point is standardising?",
             "<p>So the layer is not <em>forced</em> to be standardised. If some other scale suits "
             "the next layer better, γ and β can produce it — including undoing the normalisation "
             "entirely. Constraining without the option to opt out would cost capacity.</p>"),
            ("Which is more common today, pre-norm or post-norm, and why?",
             "<p>Pre-norm. Post-norm (the 2017 original) needs a carefully tuned warm-up to train "
             "stably at depth; pre-norm largely does not.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("lesson", "c1/w2-05-feature-scaling.html", "C1 W2 · Feature scaling",
             "The identical formula, applied to the input instead of to a hidden layer."),
        ])
    )))

# ============================================================ 4
L.append(dict(
    slug="04-feed-forward", title="The feed-forward layer", mins=11, tag="core",
    lede="Two thirds of a transformer's parameters live here, and it is the plainest thing in the "
         "architecture — a two-layer network from Course 2, applied at each position separately.",
    body=(
        pretest("""<p>After attention has mixed information between positions, each position passes through a small two-layer network on its own. <b>Guess why that is needed</b> — attention already combined everything.</p>""",
        """<p>Watch for what attention <em>cannot</em> do: it averages, and an average is linear.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Attention gathers information from other positions. But gathering is all it does —
a weighted average is a <b>linear</b> operation, and Course 2 established that stacking linear
operations gets you nothing.</p>
<p>So after attention, each position goes through a small two-layer network by itself: expand to
about four times the width, apply a non-linearity, shrink back. Every position gets the same network,
applied independently — which is why it is called “position-wise”.</p>""")

        + lenses(
            """<p>A committee meeting, then everyone going away to write their own report.</p>
<p>The meeting is attention — information moves between people. The writing-up is the feed-forward
layer — each person processes what they heard, alone, with no further conferring. Both are needed:
a meeting with no write-up produces nothing, and a write-up with no meeting is uninformed.</p>""",

            """<p>It is a two-layer MLP with a hidden width of typically 4<var>d</var>, applied
identically at every position. Equivalently, a 1×1 convolution over the sequence.</p>
<p>The reason it must exist is the C2 W5 argument, unchanged: attention is a weighted <em>average</em>,
which is linear in the values. Without a non-linearity between attention layers, the whole stack
would collapse — exactly as a network of linear layers does.</p>""",

            """<p>An hourglass, on its side.</p>
<p>512 numbers in, widened to 2048, squeezed back to 512. The wide middle is where the non-linear
work happens; the narrow ends are so the block's output matches its input and can be stacked
again.</p>""",

            """<p>The parameter count is where this becomes surprising. In a standard block, attention
holds about 1.05 million parameters and the feed-forward layer holds about 2.10 million — <b>two
thirds of the block</b>.</p>
<p>The part everyone talks about is the smaller half. There is a real line of research suggesting
these layers act as a key–value memory storing factual associations, which would make them where a
model's knowledge largely lives.</p>""",

            """So the two matrices below are the biggest thing in the block, and their job is simply
to be non-linear.""")

        + h2("🎬", "Watch it move")
        + demo("c4-ffn", "Expand, activate, shrink",
               "the same network applied at every position, independently")

        + h2("🔢", "The maths, decoded")
        + eq("""FFN<span class="paren">(</span><var>x</var><span class="paren">)</span>
<span class="op">=</span> ReLU<span class="paren">(</span><var>xW</var><sub>1</sub>
<span class="op">+</span> <var>b</var><sub>1</sub><span class="paren">)</span><var>W</var><sub>2</sub>
<span class="op">+</span> <var>b</var><sub>2</sub>""",
             "a Course 2 two-layer network, unchanged")
        + decode([
            ("<var>W</var><sub>1</sub>", "“W one”", "(d, 4d) — widens each position's vector, typically 512 → 2048."),
            ("ReLU", "“rel-you”", "The non-linearity from C2 W2. Modern models often use GELU or SwiGLU instead; the role is identical."),
            ("<var>W</var><sub>2</sub>", "“W two”", "(4d, d) — narrows back, so the block's output can be added to its input and fed to the next block."),
            ("position-wise", "“position-wise”", "The SAME network is applied to every position separately. No information moves between positions here — that was attention's job."),
        ])
        + note("""<p>This is genuinely the network you built in Course 2 Week 1 — a Dense layer, an
activation, another Dense layer. Nothing about it is new. What is new is where it sits and how many
times it is repeated.</p>""", "You have built this before")

        + h2("🧮", "Where the parameters actually are")
        + table(["component", "parameters (d = 512, d_ff = 2048)", "share of block"],
                [["attention (W_Q, W_K, W_V, W_O)", "4 × 512 × 512 = 1,048,576", "33%"],
                 ["<b>feed-forward</b> (W₁, W₂)", "<b>2 × 512 × 2048 = 2,097,152</b>", "<b>67%</b>"],
                 ["layer norms", "2,048", "0.07%"],
                 ["one block", "<b>3,147,776</b>", "100%"]])

        + h2("🕳", "Traps")
        + trap("""<p><b>Thinking this layer mixes positions.</b> It does not — it is applied to each
position in isolation. Attention is the <em>only</em> place information moves between positions, and
keeping that clean separation in your head makes the whole block easy to reason about.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("Why can a transformer not be attention layers alone?",
             "<p>Because attention is a weighted average, which is linear in the values. Stacking "
             "linear operations collapses to a single linear operation — the exact C2 W2 argument. "
             "The feed-forward layer supplies the non-linearity.</p>"),
            ("Which holds more parameters, attention or the feed-forward layer?",
             "<p>Feed-forward, by roughly two to one — 2.10M against 1.05M in a standard block. The "
             "famous half is the smaller half.</p>"),
            ("Why widen to 4d and then narrow back?",
             "<p>The wide middle gives the non-linearity room to work. Narrowing back is required so "
             "the output matches the input width, which is what lets blocks stack.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("lesson", "c2/w2-05-why-activations.html", "C2 W2 · Why activation functions",
             "The argument for why this layer must exist, made in full."),
        ])
    )))

# ============================================================ 5
L.append(dict(
    slug="05-the-block", title="The block, assembled", mins=13, tag="core",
    lede="Five pieces, one diagram, and once you can draw it from memory you can read any transformer "
         "paper's architecture section.",
    body=(
        pretest("""<p>You now have attention, residuals, layer norm and a feed-forward layer. <b>Guess the order they go in</b> — and how many residual connections one block needs.</p>""",
        """<p>Watch for the two-sublayer pattern. Everything comes in pairs.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>A transformer block is two sublayers, each wrapped identically.</p>
<p><b>Sublayer one:</b> normalise, run attention, add the input back.<br>
<b>Sublayer two:</b> normalise, run the feed-forward network, add the input back.</p>
<p>That is the entire block. Everything else in a transformer is this, repeated — twelve times, or
ninety-six times.</p>""")

        + lenses(
            """<p>A production line station that does two operations and passes the piece on
unchanged in shape.</p>
<p>Because the piece comes out the same shape it went in, you can put fifty identical stations in a
row. That is the property being engineered for — not what each station does, but that its output can
be its own input.</p>""",

            """<p>The design is deliberately uniform: <code>x = x + Sublayer(LN(x))</code>, applied
twice with different sublayers.</p>
<p>That regularity is why transformers scale so predictably. There is one block design, repeated;
depth is a hyperparameter rather than an architectural decision, and a 96-layer model is the same code
as a 12-layer one with a different number.</p>""",

            """<p>A vertical strip you could draw on a napkin.</p>
<p>Input at the bottom. Two loops leaving the main line and rejoining it — one wrapping attention, one
wrapping the feed-forward. Output at the top, same width as the input. Draw it three times stacked and
you have drawn a transformer.</p>""",

            """<p>This uniformity is why scaling laws could be discovered at all. Because the only
things that vary are depth, width and data, researchers could measure how performance responds to each
— and the resulting curves are what justify spending nine figures on a training run.</p>
<p>An architecture that changed shape as it grew would not have permitted that.</p>""",

            """So the diagram below is the unit of modern AI, and it is five components you have now
met individually.""")

        + h2("🎬", "Watch it move")
        + demo("c4-block", "One block, piece by piece",
               "step through the two sublayers and their residual wrappers")

        + h2("🔢", "The block, written out")
        + code("""
# one transformer block  (pre-norm, the modern arrangement)
def block(x):
    x = x + attention(layer_norm(x))      # sublayer 1: mix between positions
    x = x + feed_forward(layer_norm(x))   # sublayer 2: process each position
    return x                              # same shape as the input
""")
        + table(["step", "what it does", "does information move between positions?"],
                [["layer norm", "re-standardise each position's vector", "no"],
                 ["attention", "gather from other positions", "<b>yes — the only place</b>"],
                 ["+ residual", "add the input back, protecting the gradient", "no"],
                 ["layer norm", "re-standardise again", "no"],
                 ["feed-forward", "non-linear processing, each position alone", "no"],
                 ["+ residual", "add the input back again", "no"]])
        + key("""<p>Attention is the <b>only</b> step where positions interact. Everything else operates
on one position at a time. Holding that fact makes the architecture far easier to reason about than
the diagrams suggest.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Reading old diagrams as current practice.</b> The 2017 paper's figure shows
post-norm — normalise <em>after</em> the residual add. Nearly everything since 2020 is pre-norm, as
written above. Both appear in the literature and they are not interchangeable.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("How many residual connections are in one block?",
             "<p>Two — one wrapping attention, one wrapping the feed-forward network.</p>"),
            ("Why must the block's output have the same shape as its input?",
             "<p>So blocks can stack. A block that changed the shape could not be repeated, and "
             "depth is where a transformer's power comes from.</p>"),
            ("Which single step lets information move between positions?",
             "<p>Attention, and only attention. Layer norm, the feed-forward layer and the residual "
             "adds all work position by position.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("paper", "https://arxiv.org/abs/1706.03762", "Attention Is All You Need — Figure 1",
             "The original diagram. You should now be able to name every box in it."),
        ])
    )))

# ============================================================ 6
L.append(dict(
    slug="06-stacking", title="Stacking blocks — what depth buys", mins=11, tag="intuition",
    lede="Twelve identical blocks, and something happens across them that no single block does. What "
         "we know about that, and how much is honestly still unclear.",
    body=(
        pretest("""<p>Every block is identical in structure and each has its own weights. <b>Guess what a twelve-block stack can do that one block cannot</b>.</p>""",
        """<p>Watch for the idea of information travelling further with each pass, and of later layers working on what earlier ones produced.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>One block lets every position gather from every other position, once. A second block
does it again — but now each position is gathering from positions that have <em>already</em>
gathered. Information compounds.</p>
<p>Roughly, and with real caveats: early layers appear to handle surface patterns — nearby words,
grammar. Middle layers appear to handle syntax and relationships. Later layers appear to handle more
abstract, task-relevant structure.</p>""")

        + lenses(
            """<p>Successive drafts of a document.</p>
<p>The first pass fixes spelling. The second fixes sentence structure. The third reconsiders the
argument. Each pass operates on the output of the last, and the third could not have been done first —
you cannot restructure an argument while still fixing typos.</p>""",

            """<p>This is representational hierarchy, and it is the same story as convolutional networks
for images: edges, then textures, then parts, then objects.</p>
<p>The honest caveat is that the evidence in language models is <b>correlational</b> — probing studies
find syntactic information is more decodable at middle layers, which is not the same as showing the
model uses it that way. Treat the layer story as a useful sketch, not an established mechanism.</p>""",

            """<p>Ripples spreading in a pond.</p>
<p>After one block, information has travelled one hop. After two, it has reached everything its
neighbours could reach. The effective receptive field grows with depth even though every block looks
identical.</p>""",

            """<p>Depth versus width is a real engineering decision with measured trade-offs. GPT-2
small is 12 layers at width 768; GPT-3 is 96 layers at width 12,288. Both directions were scaled
together, guided by the empirical scaling laws.</p>
<p>What is <em>not</em> true is that more layers is simply better — beyond a point, extra depth needs
proportionally more width and more data to pay for itself.</p>""",

            """So the stack below is repetition, not escalation: the same block, applied again to its
own output.""")

        + h2("🎬", "Watch it move")
        + demo("c4-stack", "Twelve identical blocks",
               "information reaching further with each pass through the stack")

        + h2("🧮", "Real configurations")
        + table(["model", "layers", "width d", "heads", "parameters"],
                [["GPT-2 small", "12", "768", "12", "124 M"],
                 ["GPT-2 medium", "24", "1024", "16", "355 M"],
                 ["GPT-2 large", "36", "1280", "20", "774 M"],
                 ["GPT-3", "96", "12288", "96", "175 B"]])
        + """<p>Note that depth, width and head count all grew together. Scaling one alone does not
work well, which is one of the more useful practical findings from the scaling-law literature.</p>"""

        + h2("🕳", "Traps")
        + trap("""<p><b>Believing the “early = syntax, late = semantics” story too literally.</b> It is
a reasonable summary of probing results and is often cited far more confidently than the evidence
supports. Layers are not modules with job titles.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("What can two blocks do that one cannot?",
             "<p>In the second block, each position gathers from positions that have already gathered "
             "from others — so information can travel two hops rather than one, and later processing "
             "operates on already-contextualised representations.</p>"),
            ("Why can blocks be stacked at all?",
             "<p>Because each block's output has exactly the same shape as its input. That is the "
             "property the whole design protects.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("paper", "https://arxiv.org/abs/2001.08361", "Scaling Laws for Neural Language Models (2020)",
             "The empirical study behind the depth/width/data trade-offs above."),
        ])
    )))

# ============================================================ 7
L.append(dict(
    slug="07-gpt-vs-bert", title="Two shapes: GPT and BERT", mins=11, tag="core",
    lede="The same block, arranged two ways, producing two families with completely different "
         "capabilities — and the difference is the mask from Week 2.",
    body=(
        pretest("""<p>One transformer family generates text left to right; another is better at understanding a whole sentence but cannot generate. <b>Guess which single component differs</b>.</p>""",
        """<p>You met it in Week 2 lesson 7.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Take the block you have just built. Mask it, so no position can see the future,
stack it, and train it to predict the next token. That is <b>GPT</b> — and it can generate, because
generating is exactly what it was trained to do.</p>
<p>Now remove the mask, so every position sees the whole sentence, and train it to fill in words you
deliberately hid. That is <b>BERT</b> — better at understanding, and unable to generate left to right,
because it never learned to predict something it could not see.</p>""")

        + lenses(
            """<p>Writing a letter, versus proofreading one.</p>
<p>The writer works forward and cannot see words not yet written. The proofreader has the whole page
and reads in any direction. Both are skilled; neither can do the other's job with the other's
constraints.</p>""",

            """<p>Two training objectives. GPT does <b>autoregressive</b> next-token prediction —
P(x<sub>t</sub> | x<sub>&lt;t</sub>). BERT does <b>masked language modelling</b> — hide roughly 15% of
tokens and predict them from both sides.</p>
<p>The architectural difference is only the mask; the capability difference follows from what each
objective is possible to train under.</p>""",

            """<p>The triangular weight matrix from Week 2, present or absent.</p>
<p>Present: a staircase, each row seeing only up to the diagonal. Absent: a full square. That is
genuinely the whole architectural difference between the two families.</p>""",

            """<p>The practical consequence is which one you reach for. Search ranking, classification
and named-entity extraction are BERT-family tasks — you have the whole text and want to understand it.
Chat, completion and summarisation are GPT-family tasks — you are producing text.</p>
<p>The reason “AI” now colloquially means the GPT family is that generation is the visible capability,
not that it is the better architecture.</p>""",

            """So the table below is one mask, two families, and everything else identical.""")

        + h2("🎬", "Watch it move")
        + demo("c4-gptbert", "One mask, two families",
               "toggle it and watch what each family can and cannot do")

        + h2("🧮", "Side by side")
        + table(["", "GPT (decoder-only)", "BERT (encoder-only)"],
                [["mask", "<b>causal</b> — cannot see the future", "<b>none</b> — sees everything"],
                 ["trained to", "predict the next token", "fill in deliberately hidden tokens"],
                 ["can generate text?", "<b>yes</b>, one token at a time", "no"],
                 ["good at", "writing, completion, chat", "classification, search, extraction"],
                 ["the block itself", "identical", "identical"]])
        + key("""<p>There is also an <b>encoder–decoder</b> arrangement (the original 2017 design, and
T5), which uses both — an unmasked encoder reading the input and a masked decoder writing the output,
joined by cross-attention. Translation is its natural home.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Assuming decoder-only is simply better because it is more famous.</b> For pure
classification a BERT-style encoder is often more accurate and far cheaper to run. The GPT family
dominates attention because generation is visible, not because it wins everywhere.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("What single component distinguishes the two families?",
             "<p>The causal mask. Present → GPT-style and able to generate. Absent → BERT-style and "
             "bidirectional. The block itself is the same.</p>"),
            ("Why can BERT not generate text left to right?",
             "<p>It was never trained to predict a token it could not see — its whole training assumed "
             "both sides were available. Asked to generate, it has no learned notion of “what comes "
             "next given only the past”.</p>"),
            ("Which family suits classifying support tickets?",
             "<p>BERT-style. You have the whole ticket and want to understand it, not continue it — "
             "and an encoder is cheaper to run for that.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("paper", "https://arxiv.org/abs/1810.04805", "BERT (2018)",
             "The other branch. Section 3.1 describes the masked-language-modelling objective."),
        ])
    )))

# ============================================================ 8
L.append(dict(
    slug="08-counting-a-real-model", title="Counting a real model", mins=12, tag="maths",
    lede="Add up GPT-2 small from first principles and land on 124 million. Being able to do this is "
         "the difference between reading a model card and understanding it.",
    body=(
        pretest("""<p>GPT-2 small is 12 layers, width 768, vocabulary 50,257, context 1,024. <b>Guess where most of its parameters are</b> — the embeddings, the attention, or the feed-forward layers.</p>""",
        """<p>Watch how large the embedding table is on its own.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Every number in the published specification of a model is something you can now
compute yourself. Not approximately — exactly.</p>
<p>Do it once for GPT-2 small and every model card you read afterwards becomes legible: you will know
what “12 layers, 768 hidden” actually buys, and why a bigger context window costs what it does.</p>""")

        + h2("🎬", "Watch it move")
        + demo("c4-count", "GPT-2 small, added up",
               "adjust the configuration and watch the parameter count move")

        + h2("🧮", "The whole calculation")
        + table(["component", "formula", "count"],
                [["token embeddings", "50,257 × 768", "38,597,376"],
                 ["positional embeddings", "1,024 × 768", "786,432"],
                 ["attention per block", "4 × 768 × 768", "2,359,296"],
                 ["feed-forward per block", "2 × 768 × 3,072", "4,718,592"],
                 ["layer norms per block", "4 × 768", "3,072"],
                 ["<b>one block</b>", "", "<b>7,080,960</b>"],
                 ["× 12 blocks", "", "84,971,520"],
                 ["<b>total</b>", "", "<b>124,355,328 ≈ 124 M</b>"]])
        + """<p>The published figure for GPT-2 small is 124 million. The arithmetic above lands on it —
which is worth doing yourself once, because it turns a model card from a specification into something
you can reason about.</p>"""
        + explain("""<p>The token embedding table alone is <b>38.6 million</b> parameters — about 31%
of the whole model, and larger than any three blocks put together. <b>Why is that not wasteful?</b></p>""",
                  """<p>Because it is doing a genuinely large job: it must give 50,257 distinct tokens
distinct, useful representations, and that irreducibly needs V × d numbers. It is also cheap at
<em>run time</em> in a way the blocks are not — a lookup touches one row, while every block does full
matrix multiplies over the whole sequence. Large in memory, nearly free in compute. Many models also
tie the input and output embedding matrices to avoid paying for it twice.</p>""")

        + h2("🧮", "Where the parameters live, as a share")
        + table(["", "share of GPT-2 small"],
                [["token + positional embeddings", "31.6%"],
                 ["attention (all 12 blocks)", "22.8%"],
                 ["<b>feed-forward (all 12 blocks)</b>", "<b>45.5%</b>"],
                 ["layer norms", "0.03%"]])
        + """<p>The feed-forward layers — the plainest component in the architecture — are the largest
single share. The attention everyone talks about is under a quarter.</p>"""

        + h2("🕳", "Traps")
        + trap("""<p><b>Confusing parameter count with memory needed to run.</b> Training needs several
times the parameter memory (gradients, optimiser state, activations). Inference needs roughly the
parameters plus a KV cache that grows with context length — which is another place the context window
costs you.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("Why is the feed-forward layer twice the size of attention in each block?",
             "<p>Attention is 4 matrices of d × d. Feed-forward is 2 matrices of d × 4d, which is "
             "8d² against attention's 4d² — exactly twice.</p>"),
            ("Doubling the context window from 1,024 to 2,048 — what happens to the parameter count?",
             "<p>Only the positional embeddings grow, by 786,432 — under 1% of the model. But the "
             "<b>compute</b> grows with the square of length, and the KV cache doubles. The "
             "parameter count is the wrong thing to watch here.</p>"),
            ("Where would you look first to make this model smaller?",
             "<p>The feed-forward layers, at 45.5%, or the embedding table at 31.6%. Attention is "
             "under a quarter of it — shrinking it would not achieve much.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("paper", "https://arxiv.org/abs/2005.14165", "Language Models are Few-Shot Learners (GPT-3, 2020)",
             "Table 2.1 lists the configurations. You can now compute every parameter count in it."),
        ])
    )))

WEEK = dict(course="C4", week=3, title="The Transformer Block", lessons=L)
