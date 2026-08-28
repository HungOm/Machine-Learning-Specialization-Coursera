# -*- coding: utf-8 -*-
"""C4 · Week 2 — Attention: queries, keys and values."""
from kit import (kid, key, warn, trap, note, card, eq, eqp, decode, table, demo,
                 quiz, links, code, h2, grid2, grid3, pretest, explain, lenses)

L = []

# ============================================================ 1
L.append(dict(
    slug="01-the-idea", title="Attention, in one sentence", mins=11, tag="intuition",
    lede="Every position looks at every other position and takes a weighted average of what it finds. "
         "That is the whole mechanism — the rest of the week is careful bookkeeping.",
    body=(
        pretest("""<p>Attention has to let position 7 gather information from positions 1–20, choosing how much to take from each. <b>Guess which two operations you already know could do that</b> — you have used both since Course 2.</p>""",
        """<p>Watch for “weighted average” and for what produces weights that are positive and sum to 1.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Each word asks the same question of every other word: <b>“how relevant are you to
me?”</b> The answers become weights. Then the word takes a weighted average of what all those words
are carrying, and that average is its new representation.</p>
<p>That is it. A relevance score for every pair, softmaxed into weights, used to average. Both halves
— dot products for scoring, softmax for turning scores into weights — you have used since Course
2.</p>""")

        + lenses(
            """<p>A newsroom where every journalist reads every other journalist's notes before writing
their paragraph.</p>
<p>The sports writer skims the politics notes and takes almost nothing; she reads the match report
closely. Nobody assigned those priorities — she judged relevance to her own paragraph. Everyone does
this simultaneously, and everyone's paragraph comes out informed by whichever notes mattered to
them.</p>""",

            """<p>This is a soft, content-addressed lookup — a dictionary where instead of one exact
key match you get a <b>similarity-weighted blend of every value</b>.</p>
<p>Database people will recognise it as a join whose match condition is continuous rather than
boolean. The softness is not a compromise; it is what makes the retrieval differentiable and hence
trainable.</p>""",

            """<p>A room of people, each holding a card, all looking at each other at once.</p>
<p>Every person decides how much attention to give each other person, then forms an opinion that is a
blend of all the cards, weighted by those decisions. Crucially <b>nobody waits their turn</b> —
everyone does it simultaneously, which is exactly what an RNN could not do.</p>""",

            """<p>This one mechanism is underneath essentially everything called AI in public
discussion today — GPT, Claude, Gemini, image transformers, protein-structure prediction, modern
recommenders.</p>
<p>It is worth registering how small the idea is relative to its consequences. Not a new kind of
maths: a dot product, a softmax, and an average, arranged so every position can reach every other in
one step.</p>""",

            """So the formula below has three named pieces, and the next lesson is entirely about why
the same input plays three different roles.""")

        + h2("🎬", "Watch it move")
        + demo("c4-attn-idea", "Every position looking at every other",
               "each row of weights sums to 1 — click a position to see what it attends to")

        + h2("🔢", "The maths, decoded")
        + eqp([
            'Attention',
            ('<span class="paren">(</span><var>Q</var>, <var>K</var>, <var>V</var><span class="paren">)</span>', "attn-qkv", "the three roles"),
            ' <span class="op">=</span> ',
            ('softmax', "softmax-fn", "turn scores into weights"),
            ('<span class="paren">(</span><span class="frac"><span><var>QK</var><sup>T</sup></span><span><span class="sqrt">√</span><var>d</var><sub><var>k</var></sub></span></span><span class="paren">)</span>', "attn-scores", "score every pair, then scale"),
            ('<var>V</var>', "attn-value", "average the content"),
        ], "the whole of attention — hover or click any part")
        + decode([
            ("<var>Q</var>", "“the queries”", "One per position: <em>what am I looking for?</em>"),
            ("<var>K</var>", "“the keys”", "One per position: <em>what do I offer?</em>"),
            ("<var>V</var>", "“the values”", "One per position: <em>what do I actually pass on if chosen?</em>"),
            ("<var>QK</var><sup>T</sup>", "“Q K transpose”", "Every query dotted with every key — a T × T grid of relevance scores. The transpose is only there to make the shapes meet."),
            ("<var>d</var><sub><var>k</var></sub>", "“d sub k”", "The length of one query/key vector. Dividing by its square root keeps the scores in a sane range — lesson 5 shows why."),
        ])
        + key("""<p>Read it right to left and it is a sentence you already know: <b>score every pair,
turn the scores into weights that sum to 1, take a weighted average.</b></p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Thinking Q, K and V are three different inputs.</b> In self-attention they are
three different <em>projections of the same input</em>. That is the next lesson, and it is the part
people find genuinely confusing.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("Which two operations from earlier courses is attention built from?",
             "<p>The <b>dot product</b> (C1 W2 / F0 W1), used to score how well a query matches a key; "
             "and <b>softmax</b> (C2 W2), used to turn those scores into weights that are positive and "
             "sum to 1.</p>"),
            ("Why must the weights sum to 1?",
             "<p>Because the result is an average of the value vectors. Weights that did not sum to 1 "
             "would make the output's magnitude depend on sequence length rather than on content.</p>"),
            ("What is the shape of QK<sup>T</sup> for a 100-token sequence?",
             "<p>100 × 100 — one score for every ordered pair of positions. That square is where "
             "attention's cost comes from, and it is the subject of lesson 8.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("lesson", "c2/w2-07-softmax.html", "C2 W2 · Softmax",
             "The exact function that turns attention scores into weights."),
            ("lesson", "f0/w1-10-dot-product.html", "F0 W1 · The dot product",
             "The other half. Worth rereading now that it has a second job."),
        ])
    )))

# ============================================================ 2
L.append(dict(
    slug="02-query-key-value", title="Query, key, value — three roles, one input", mins=13, tag="core",
    lede="The genuinely confusing part of the whole architecture, and it dissolves once you see that "
         "the three names are three learned projections of the same vectors.",
    body=(
        pretest("""<p>In self-attention, Q, K and V all come from the <b>same</b> sequence. <b>Guess why you would bother producing three versions of one thing</b> rather than just using it directly.</p>""",
        """<p>Watch for the difference between what a word is looking for and what a word offers.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Think about looking something up in a library.</p>
<p>Your <b>query</b> is what you want — “books about volcanoes”. Each book's <b>key</b> is what it
advertises about itself — the spine, the title, the catalogue entry. Its <b>value</b> is the actual
content you take away if you pick it.</p>
<p>The key and the value are different on purpose: what a thing advertises and what it contains are
not the same. A word being useful to find is a different property from a word being useful to
read.</p>""")

        + lenses(
            """<p>A dating agency's card index, in the days before apps.</p>
<p>Each member fills in two different things: what they are <b>looking for</b>, and what they
<b>offer</b>. The matching is done between one person's wants and another person's offers — never
wants against wants. And what you actually get on the date is a third thing again: the person, not
the card.</p>
<p>Query, key, value. Three roles, one member.</p>""",

            """<p>Formally these are three learned linear projections of the same input:
<var>Q</var> = <var>XW</var><sub><var>Q</var></sub>, <var>K</var> = <var>XW</var><sub><var>K</var></sub>,
<var>V</var> = <var>XW</var><sub><var>V</var></sub>.</p>
<p>Three separate weight matrices, all trained. The model is free to learn that the useful <em>index
of</em> a word differs from its useful <em>content</em> — and empirically it does learn exactly
that.</p>""",

            """<p>A library catalogue card and the book it points to.</p>
<p>The card is the key: short, designed for searching. The book is the value: long, and what you
actually leave with. Merging the two would force one representation to be good at both jobs, and it
would be mediocre at each.</p>""",

            """<p>This separation is why attention maps are interpretable enough to publish. Because
keys are a distinct learned thing, you can read off which positions a head found relevant — the
pictures showing a pronoun attending to the noun it refers to are literally plots of these
weights.</p>
<p>It is one of the few places in deep learning where a picture of the internals is genuinely
informative rather than decorative.</p>""",

            """So the three matrices below are the only new parameters attention introduces — and
everything after this is arithmetic you have already done.""")

        + h2("🎬", "Watch it move")
        + demo("c4-qkv", "One input, three projections",
               "the same X, multiplied by three different learned matrices")

        + h2("🔢", "The maths, decoded")
        + eq("""<var>Q</var> <span class="op">=</span> <var>XW</var><sub><var>Q</var></sub>
&nbsp;&nbsp; <var>K</var> <span class="op">=</span> <var>XW</var><sub><var>K</var></sub>
&nbsp;&nbsp; <var>V</var> <span class="op">=</span> <var>XW</var><sub><var>V</var></sub>""",
             "three projections of the same X")
        + decode([
            ("<var>X</var>", "“the input”", "The sequence, already embedded. Shape (T, d) — T positions, d numbers each."),
            ("<var>W</var><sub><var>Q</var></sub>", "“W-Q”", "A learned matrix turning each position into <em>what it is looking for</em>."),
            ("<var>W</var><sub><var>K</var></sub>", "“W-K”", "A learned matrix turning each position into <em>what it advertises</em>."),
            ("<var>W</var><sub><var>V</var></sub>", "“W-V”", "A learned matrix turning each position into <em>what it hands over</em> when attended to."),
            ("self-attention", "“self attention”", "The case where Q, K and V all come from the SAME sequence — a sentence attending to itself."),
        ])
        + note("""<p>When Q comes from one sequence and K, V from another, it is called
<b>cross-attention</b> — and that is exactly the 2014 translation setup from Week 1, where the output
being generated queried the input being translated. Self-attention is the newer idea: let a sequence
attend to <em>itself</em>.</p>""", "Self- versus cross-attention")

        + h2("🧮", "Shapes, which is where people get lost")
        + table(["", "shape", "read as"],
                [["<var>X</var>", "(T, d)", "T positions, d numbers each"],
                 ["<var>W</var><sub><var>Q</var></sub>, <var>W</var><sub><var>K</var></sub>", "(d, d<sub>k</sub>)", "project each position down to the query/key size"],
                 ["<var>W</var><sub><var>V</var></sub>", "(d, d<sub>v</sub>)", "project to the value size"],
                 ["<var>Q</var>, <var>K</var>", "(T, d<sub>k</sub>)", "one query and one key per position"],
                 ["<var>QK</var><sup>T</sup>", "<b>(T, T)</b>", "every position scored against every position"],
                 ["output", "(T, d<sub>v</sub>)", "one new vector per position — same length as the input sequence"]])
        + explain("""<p>The output has one vector per input position, exactly like the input.
<b>Why does that matter for building a deep model?</b></p>""",
                  """<p>Because it means attention layers <em>stack</em>. A layer that changed the
sequence length could not simply be repeated; one that preserves it can be applied over and over,
each pass letting information travel further and combine more. That shape-preserving property is
what makes a twelve-layer or ninety-six-layer transformer possible at all, and it is the same
argument that made <code>Sequential</code> work in Course 2.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Assuming K and V must be the same thing.</b> They are computed from the same
input but through different matrices, and the model uses that freedom. Tying them together is a
distinct, weaker architecture.</p>""")
        + trap("""<p><b>Losing track of which dimension is T and which is d.</b> Q is (T, d<sub>k</sub>);
QK<sup>T</sup> is (T, T). If your shapes come out as (d, d) somewhere, you have transposed
something.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("Why three projections rather than using X directly for all three roles?",
             "<p>Because “what I am looking for”, “what I advertise” and “what I hand over” are "
             "genuinely different properties. Three learned matrices let the model represent them "
             "separately; using X for all three forces one vector to do all three jobs.</p>"),
            ("What is the difference between self-attention and cross-attention?",
             "<p>In self-attention Q, K and V all come from the same sequence. In cross-attention Q "
             "comes from one sequence and K, V from another — which is the 2014 translation setup "
             "from Week 1.</p>"),
            ("For T = 50 and d<sub>k</sub> = 64, what shape is QK<sup>T</sup>?",
             "<p>(50, 50). Note d<sub>k</sub> vanishes — it was the inner dimension of the multiply. "
             "The result depends only on how many positions there are.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("lesson", "c2/w1-15-matmul-rules.html", "C2 W1 · Matrix multiplication rules",
             "The inner-numbers-must-match rule, which is all you need to follow every shape above."),
        ])
    )))

# ============================================================ 3
L.append(dict(
    slug="03-attention-by-hand", title="Attention, computed by hand", mins=15, tag="maths",
    lede="Three tokens, two dimensions, every number worked out. Do this once on paper and the "
         "mechanism stops being mysterious permanently.",
    body=(
        pretest("""<p>You are about to compute attention on a 3-token sequence with d<sub>k</sub> = 2. <b>Guess how many numbers are in the attention weight matrix</b>, and what each row of it must add up to.</p>""",
        """<p>Watch the row sums. They are the check that tells you whether you have done it right.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>We are going to do the whole thing with numbers small enough to check in your head.
Three tokens. Each query, key and value is just two numbers.</p>
<p>Four steps: score every pair, scale, softmax each row, then use each row as mixing proportions for
the values. Nothing else happens in an attention layer — everything else in a transformer is
around it, not inside it.</p>""")

        + h2("🎬", "Watch it move")
        + demo("c4-attn-hand", "The four steps, on three tokens",
               "step through score, scale, softmax and mix — every number is real")

        + h2("🧮", "Step 0 — the inputs")
        + """<p>Deliberately simple, so you can verify every product by eye:</p>"""
        + code("""
Q = [[1, 0],     K = [[1, 0],     V = [[10,  0],
     [0, 1],          [0, 1],          [ 0, 10],
     [1, 1]]          [1, 1]]          [ 5,  5]]
""")
        + """<p>Read the values as “token 1 carries 10 units of thing A, token 2 carries 10 units of
thing B, token 3 carries a bit of both”.</p>"""

        + h2("🧮", "Step 1 — score every pair")
        + """<p><var>QK</var><sup>T</sup>: each row of Q dotted with each row of K. Row 1 is
<var>q</var><sub>1</sub> = [1, 0] against all three keys:</p>"""
        + eq("""[1,0]·[1,0] = 1 &nbsp;&nbsp; [1,0]·[0,1] = 0 &nbsp;&nbsp; [1,0]·[1,1] = 1""",
             "the first row of scores, by hand")
        + table(["", "k₁", "k₂", "k₃"],
                [["q₁", "<b>1</b>", "0", "<b>1</b>"],
                 ["q₂", "0", "<b>1</b>", "<b>1</b>"],
                 ["q₃", "1", "1", "<b>2</b>"]])
        + """<p>Token 3's query matches token 3's key best (score 2) because [1,1]·[1,1] = 2 — a vector
agrees with itself more than with anything else. That diagonal dominance is normal and expected.</p>"""

        + h2("🧮", "Step 2 — scale by √d")
        + """<p><var>d</var><sub><var>k</var></sub> = 2, so divide everything by √2 = 1.4142:</p>"""
        + table(["", "k₁", "k₂", "k₃"],
                [["q₁", "0.7071", "0", "0.7071"],
                 ["q₂", "0", "0.7071", "0.7071"],
                 ["q₃", "0.7071", "0.7071", "1.4142"]])
        + """<p>Lesson 5 is entirely about why this division exists. For now: it stops the scores from
growing with <var>d</var><sub><var>k</var></sub>.</p>"""

        + h2("🧮", "Step 3 — softmax each row")
        + """<p>Row by row, independently. For row 1, scores [0.7071, 0, 0.7071]:</p>"""
        + eq("""<var>e</var><sup>0.7071</sup> = 2.028 &nbsp;&nbsp; <var>e</var><sup>0</sup> = 1
&nbsp;&nbsp; <var>e</var><sup>0.7071</sup> = 2.028 &nbsp;&nbsp;&nbsp; sum = 5.056""",
             "exponentiate, then divide by the total")
        + table(["", "→ k₁", "→ k₂", "→ k₃", "row sum"],
                [["from q₁", "<b>0.4011</b>", "0.1978", "<b>0.4011</b>", "1.000"],
                 ["from q₂", "0.1978", "<b>0.4011</b>", "<b>0.4011</b>", "1.000"],
                 ["from q₃", "0.2483", "0.2483", "<b>0.5035</b>", "1.000"]])
        + """<p>2.028 ÷ 5.056 = 0.4011 — check it. Every row sums to exactly 1, which is the property
that makes the next step an average rather than an arbitrary sum.</p>"""
        + key("""<p><b>Rows sum to 1; columns do not.</b> Each row is one position's own mixing recipe,
computed independently of the others. If your rows do not sum to 1, you have softmaxed the wrong
axis — the single most common implementation bug here.</p>""")

        + h2("🧮", "Step 4 — mix the values")
        + """<p>Each output row is its weight row applied to V. Output row 1:</p>"""
        + eq("""0.4011×[10,0] <span class="op">+</span> 0.1978×[0,10] <span class="op">+</span>
0.4011×[5,5] <span class="op">=</span> [6.017, 3.983]""", "one weighted average")
        + table(["output row", "value", "reading"],
                [["1", "[6.017, 3.983]", "mostly thing A — token 1 attended to itself and token 3"],
                 ["2", "[3.983, 6.017]", "mostly thing B — the mirror image"],
                 ["3", "[5.000, 5.000]", "an even blend — token 3 attended fairly evenly"]])
        + """<p>Check row 1's first component by hand: 0.4011(10) + 0.1978(0) + 0.4011(5) = 4.011 + 0 +
2.006 = 6.017. Every number on this page is reproducible with a calculator.</p>"""
        + explain("""<p>Row 3 came out as exactly [5, 5], a perfectly even blend.
<b>Why did that happen, given its weights were 0.248, 0.248 and 0.504 rather than equal?</b></p>""",
                  """<p>Because of what the values are, not what the weights are. Token 3's own value
is [5,5] — already the midpoint — and the other two, [10,0] and [0,10], are weighted equally at 0.2483
each, so they average to [5,5] between them. Two blends of [5,5] give [5,5]. It is a coincidence of
this hand-picked example, and worth noticing precisely so you do not read a rule into it.</p>""")

        + h2("💻", "In code")
        + code("""
import numpy as np

def softmax(x):
    e = np.exp(x - np.max(x, axis=-1, keepdims=True))   # the C2 W2 stability trick
    return e / np.sum(e, axis=-1, keepdims=True)

def attention(Q, K, V):
    d_k = Q.shape[-1]
    scores = Q @ K.T / np.sqrt(d_k)     # (T, T)
    weights = softmax(scores)           # rows sum to 1
    return weights @ V                  # (T, d_v)
""")
        + """<p>Five lines. That is the entire mechanism the last decade of AI is built on — and
<code>axis=-1</code> is doing the load-bearing work, because softmaxing the wrong axis is the bug
that silently produces plausible nonsense.</p>"""

        + h2("🕳", "Traps")
        + trap("""<p><b>Softmaxing the wrong axis.</b> It must be the last axis, so each <em>row</em> —
one position's weights over all positions — sums to 1. Softmaxing columns runs without error and
produces something meaningless.</p>""")
        + trap("""<p><b>Forgetting the scale.</b> With d<sub>k</sub> = 2 it barely matters. With
d<sub>k</sub> = 512 it is the difference between training and not training.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("For 3 tokens, what shape is the weights matrix, and what do its rows sum to?",
             "<p>3 × 3, and every row sums to exactly <b>1</b>. Columns do not, and are not supposed "
             "to — each row is one position's independent mixing recipe.</p>"),
            ("Compute the first component of output row 2 by hand.",
             "<p>0.1978(10) + 0.4011(0) + 0.4011(5) = 1.978 + 0 + 2.006 = <b>3.983</b>. ✓</p>"),
            ("Why does the diagonal of the score matrix tend to be largest?",
             "<p>Because a vector's dot product with itself is its squared length, which is at least "
             "as large as its dot product with anything of the same size. A position usually finds "
             "itself relevant — which is fine, and the model can learn to counteract it where it "
             "should not.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("lesson", "c2/w2-09-improved-softmax.html", "C2 W2 · Improved softmax",
             "The max-subtraction trick used in the code above, and why it is not optional."),
        ])
    )))

# ============================================================ 4
L.append(dict(
    slug="04-self-attention", title="Self-attention — a sentence reading itself", mins=12, tag="core",
    lede="What the mechanism is actually for: resolving what a word means from the other words around "
         "it, in one step, in both directions.",
    body=(
        pretest("""<p>“The animal didn’t cross the street because <b>it</b> was too tired.” <b>Guess what “it” refers to</b> — then guess what changes if the last word is “wide” instead of “tired”.</p>""",
        """<p>Watch how one word decides where to look based on the others. That decision is the whole job.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Words do not have fixed meanings. “Bank” means something different beside “river”
than beside “money”. To represent a word properly you have to look at its neighbours — and not just
the ones next to it, but whichever ones happen to matter.</p>
<p>Self-attention lets every word do exactly that, at once, in both directions. Each word ends up
represented not by itself but by <b>itself in context</b>.</p>""")

        + lenses(
            """<p>A jury deliberating.</p>
<p>Each juror arrives with an impression, then listens to all the others and updates. Nobody speaks in
turn down a line — everyone hears everyone. And a juror who cares about the forensic evidence weighs
the expert witness heavily and the character reference barely.</p>
<p>After one round everyone's view is a blend of the room. That round is one attention layer, and a
transformer runs a dozen of them.</p>""",

            """<p>Linguists call this <b>coreference resolution</b> and it was a hard, separate research
problem for decades — deciding which noun a pronoun refers to.</p>
<p>Self-attention does not solve it explicitly; it falls out. Some attention heads, examined after
training, are found to systematically connect pronouns to their referents even though nobody supplied
that objective.</p>""",

            """<p>A sentence with arrows drawn from every word to every other word, thicker where the
connection matters more.</p>
<p>For “it”, the thick arrow points at “animal”. Change the final adjective and the thick arrow swings
to “street”. The words did not change — the relevance did.</p>""",

            """<p>This is why models handle ambiguity that defeated earlier systems. The sentence pair
in the pretest — “because it was too tired” versus “because it was too wide” — is the classic
Winograd example, designed specifically to require world knowledge rather than grammar.</p>
<p>Attention is not what supplies the knowledge, but it is the mechanism that lets the knowledge be
applied to the right pair of words.</p>""",

            """So “self” in self-attention just means Q, K and V all come from the same sentence — and
that one change is what turned attention from a translation aid into an architecture.""")

        + h2("🎬", "Watch it move")
        + demo("c4-selfattn", "Which word does “it” look at?",
               "change the final adjective and watch the attention move")

        + h2("🔢", "What changes versus Week 1")
        + table(["", "cross-attention (2014)", "self-attention (2017)"],
                [["Q comes from", "the output being generated", "the same sequence"],
                 ["K, V come from", "the input being read", "the same sequence"],
                 ["used for", "translation, bolted onto an RNN", "representing a sequence at all"],
                 ["direction", "output → input", "every position ↔ every position"]])
        + key("""<p>Self-attention is not a different mechanism. It is the same arithmetic with the same
sequence in all three roles — and that is enough to replace the RNN entirely.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Expecting attention weights to be a clean explanation.</b> Some heads are
strikingly interpretable; many are not, and there is an active research literature on how much
attention weights actually explain a model's output. Treat the pretty pictures as suggestive, not
as proof.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("Why can a word not simply be represented by its embedding alone?",
             "<p>Because the embedding is fixed per token, and meaning depends on context. “Bank” has "
             "one embedding but at least two meanings, and only the surrounding words distinguish "
             "them.</p>"),
            ("In self-attention, how far apart can two positions be and still interact directly?",
             "<p>Any distance. Every pair is scored, so position 1 and position 500 interact in "
             "exactly one step — which is precisely what an RNN could not do.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("paper", "https://arxiv.org/abs/1706.03762", "Attention Is All You Need",
             "Section 3.2 is the mechanism you have now computed by hand. It should read as familiar."),
        ])
    )))

# ============================================================ 5
L.append(dict(
    slug="05-why-scale", title="Why divide by √d", mins=12, tag="maths",
    lede="A one-symbol detail with a real consequence, and a rare case where you can see exactly why "
         "a design choice was made — by measuring what happens without it.",
    body=(
        pretest("""<p>Attention divides its scores by √d<sub>k</sub> before the softmax. <b>Guess what goes wrong if you skip it</b>, remembering what softmax does when one input is much larger than the others.</p>""",
        """<p>Watch for the connection to vanishing gradients — the same enemy as Week 1, arriving by a different route.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>A dot product of two long vectors is a sum of many terms. The more terms, the bigger
the total tends to be — not because the vectors mean more, but simply because you added up more
numbers.</p>
<p>Feed unusually large numbers into a softmax and it saturates: one weight goes to essentially 1 and
the rest to essentially 0. At that point the gradient is nearly zero and the layer stops learning.
Dividing by √d<sub>k</sub> cancels the growth, keeping the scores in the range where softmax is still
responsive.</p>""")

        + lenses(
            """<p>Judges scoring a competition on a scale of 1–10 versus 1–1000.</p>
<p>On the wide scale, tiny differences in opinion produce enormous gaps, and the winner is decided by
one judge's outlier. Normalising the scale back to something sensible is not cosmetic — it changes
who wins.</p>""",

            """<p>Precisely: if the components of <var>q</var> and <var>k</var> are roughly independent
with variance 1, then <var>q</var>·<var>k</var> has variance <var>d</var><sub><var>k</var></sub> and
therefore standard deviation √<var>d</var><sub><var>k</var></sub>.</p>
<p>Dividing by exactly that returns the scores to unit variance. This is the same normalisation
instinct behind feature scaling in C1 W2 — keep the numbers entering a nonlinearity in the range
where it behaves.</p>""",

            """<p>The softmax curve, and where you are sitting on it.</p>
<p>Near the middle it is a gentle slope — nudge an input and the output moves, so there is gradient to
learn from. Far out it is flat as a table: one output is 1.0000, the rest are 0.0000, and nudging
changes nothing. Scaling is what keeps you on the slope.</p>""",

            """<p>Measured, by simulation: with <var>d</var><sub><var>k</var></sub> = 512, the standard
deviation of an unscaled dot product is about <b>22.6</b> — and √512 is 22.63, so the theory is
exact.</p>
<p>Scores of that size make softmax return a hard one-hot, so the attention layer produces a hard
selection with no usable gradient. The model does not train slowly; it does not train.</p>""",

            """So the √d below is the difference between a mechanism that learns and one that
silently locks up.""")

        + h2("🎬", "Watch it move")
        + demo("c4-scale", "Softmax, before and after scaling",
               "raise d and watch the weights collapse to one-hot without the divisor")

        + h2("🧮", "Measured, not asserted")
        + """<p>Twenty thousand random query/key pairs at each size, components drawn from a standard
normal:</p>"""
        + table(["d<sub>k</sub>", "std of q·k, measured", "√d<sub>k</sub>", "match?"],
                [["2", "1.419", "1.414", "✓"],
                 ["64", "8.041", "8.000", "✓"],
                 ["512", "22.591", "22.627", "✓"]])
        + """<p>The spread of the scores grows as the square root of the dimension, exactly as the
theory says. Dividing by √d<sub>k</sub> undoes it.</p>"""

        + h2("🧮", "And what saturation looks like")
        + """<p>Softmax of [s, 0, 0] as s grows:</p>"""
        + table(["scores", "softmax", "largest weight"],
                [["[1, 0, 0]", "[0.576, 0.212, 0.212]", "0.576 — soft, informative"],
                 ["[4, 0, 0]", "[0.965, 0.018, 0.018]", "0.965 — nearly hard"],
                 ["[16, 0, 0]", "[1.000, 0.000, 0.000]", "<b>1.000 — no gradient left</b>"]])
        + explain("""<p>A softmax that returns a confident 1.000 sounds like a model that has made up
its mind. <b>Why is it a problem during training rather than a success?</b></p>""",
                  """<p>Because confidence at this stage is arbitrary, not earned. Early in training the
projections are near-random, so which position wins is essentially noise — and once the softmax
saturates, the gradient through it is ~0, so that arbitrary choice can no longer be corrected. The
layer has committed to a random answer and lost the means to change its mind. Scaling keeps it
uncommitted long enough to learn.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Dividing by d<sub>k</sub> instead of √d<sub>k</sub>.</b> An easy slip, and it
over-corrects — scores become too small, softmax goes nearly uniform, and attention stops
distinguishing positions at all. The square root is the right amount, for the reason measured
above.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("Why √d<sub>k</sub> specifically, rather than any other constant?",
             "<p>Because the standard deviation of a dot product of d<sub>k</sub> independent unit-"
             "variance components is exactly √d<sub>k</sub>. Dividing by it restores unit variance — "
             "confirmed by the measurements above.</p>"),
            ("What is the failure mode without scaling, in one sentence?",
             "<p>Large scores saturate the softmax into a near one-hot, the gradient through it "
             "collapses to nearly zero, and the layer stops learning — a vanishing gradient reached "
             "by a different route than Week 1's.</p>"),
            ("Where have you seen this instinct before?",
             "<p>Feature scaling in C1 W2, and the softmax stability trick in C2 W2. All three are "
             "the same principle: keep the numbers entering a nonlinearity in the range where it "
             "still responds.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("lesson", "c1/w2-05-feature-scaling.html", "C1 W2 · Feature scaling",
             "The same normalisation instinct, applied to inputs rather than to attention scores."),
        ])
    )))

# ============================================================ 6
L.append(dict(
    slug="06-multi-head", title="Multi-head attention", mins=12, tag="core",
    lede="One attention layer can only compute one weighted average. Running several in parallel lets "
         "a model attend to several different kinds of relationship at once.",
    body=(
        pretest("""<p>One attention layer produces one set of weights per position. <b>Guess why that is limiting</b> — think about how many different relationships a single word has with the rest of a sentence.</p>""",
        """<p>Watch for the answer being “just run several, and concatenate”.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>A word relates to the rest of a sentence in several ways at once. “Bank” needs to
know its adjective, its verb, and whether “river” appears anywhere nearby — and those are different
questions with different answers.</p>
<p>One attention head produces one weighted average, so it can only chase one kind of relationship.
The fix is unglamorous: <b>run several heads in parallel</b>, each with its own
<var>W</var><sub><var>Q</var></sub>, <var>W</var><sub><var>K</var></sub>,
<var>W</var><sub><var>V</var></sub>, and glue their outputs together.</p>""")

        + lenses(
            """<p>A building being surveyed by several specialists on the same day.</p>
<p>The structural engineer, the electrician and the damp surveyor walk the same rooms and notice
completely different things. You do not want one generalist's averaged opinion — you want all three
reports, side by side.</p>
<p>Each attention head is one specialist, and concatenation is stapling the reports together.</p>""",

            """<p>This is an ensemble inside a layer, and it is closely analogous to having multiple
filters in a convolutional layer — each learns a different feature detector over the same input.</p>
<p>Note the budget: with <var>h</var> heads, each head's dimension is <var>d</var>/<var>h</var>, so
the total parameter count is roughly unchanged. You are not spending more; you are spending it on
diversity rather than on one wider view.</p>""",

            """<p>Several transparent overlays on one page of text.</p>
<p>One overlay draws arrows from verbs to their subjects. Another links pronouns to nouns. Another
tracks position. Stack them and you can see all the structures at once; use only one and you see
only one kind of relationship.</p>""",

            """<p>When researchers examined a trained model's heads, they found some had specialised
in recognisable ways — one tracking the direct object of a verb, another attending to the previous
token, another to sentence boundaries.</p>
<p>Nobody assigned those jobs. It is one of the more striking results in interpretability, and it is
also the honest caveat: plenty of other heads do nothing legible at all, and many can be pruned after
training with little loss.</p>""",

            """So the concatenation below is all “multi-head” means — several independent attentions,
stacked side by side and mixed once at the end.""")

        + h2("🎬", "Watch it move")
        + demo("c4-multihead", "Several heads, several patterns",
               "the same sentence, attended to in different ways at once")

        + h2("🔢", "The maths, decoded")
        + eq("""MultiHead <span class="op">=</span> Concat
<span class="paren">(</span>head<sub>1</sub>, …, head<sub><var>h</var></sub><span class="paren">)</span>
<var>W</var><sub><var>O</var></sub>""", "run them all, glue, then mix")
        + decode([
            ("head<sub><var>i</var></sub>", "“head i”", "One complete attention, with its own three projection matrices. Independent of every other head."),
            ("Concat", "“concatenate”", "Lay the outputs side by side. With h heads of size d/h, the result is back to width d."),
            ("<var>W</var><sub><var>O</var></sub>", "“W-O”, the output projection", "One final learned matrix that lets the heads' outputs be mixed rather than merely stacked."),
            ("<var>h</var>", "“the number of heads”", "8 or 12 are typical. Each head works in d/h dimensions, so the total stays roughly constant."),
        ])
        + note("""<p><var>W</var><sub><var>O</var></sub> is easy to overlook and it matters: without it
the heads' outputs would sit in separate slots, never interacting. It is what lets a later layer use
a combination of what several heads found.</p>""", "Why the final projection is there")

        + h2("🧮", "The budget, counted")
        + table(["", "1 head of size 512", "8 heads of size 64"],
                [["per-head Q/K/V params", "3 × 512 × 512", "3 × 512 × 64"],
                 ["× number of heads", "× 1", "× 8"],
                 ["total", "786,432", "<b>786,432</b>"],
                 ["different relationships representable", "1", "<b>8</b>"]])
        + """<p>Identical parameter count. The eight-head version simply spends it on eight narrower
views instead of one wide one — which turns out to be a much better use of the same budget.</p>"""

        + h2("🕳", "Traps")
        + trap("""<p><b>Thinking more heads is always better.</b> Each head gets narrower as you add
more, and past a point they have too few dimensions to represent anything useful. 8–16 is the usual
range for a reason.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("Why does splitting into 8 heads not cost 8× the parameters?",
             "<p>Because each head works in d/8 dimensions instead of d. Eight heads of size 64 is the "
             "same parameter budget as one head of size 512 — the budget is redistributed, not "
             "increased.</p>"),
            ("What does W<sub>O</sub> do that concatenation alone does not?",
             "<p>It lets the heads' outputs be <b>mixed</b>. Concatenation just places them side by "
             "side in separate dimensions; W<sub>O</sub> is a learned matrix that can combine "
             "information across heads.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("paper", "https://arxiv.org/abs/1905.10650", "Are Sixteen Heads Really Better than One? (2019)",
             "Finds that many heads can be pruned after training with little loss — the honest counterweight to the interpretability results."),
        ])
    )))

# ============================================================ 7
L.append(dict(
    slug="07-masking", title="Masking — stopping a model reading ahead", mins=11, tag="core",
    lede="A model trained to predict the next word must not be allowed to see it. One triangular "
         "matrix of −∞ enforces that, and it is the difference between GPT and BERT.",
    body=(
        pretest("""<p>A model is trained to predict the next word, and attention lets every position see every other position — including later ones. <b>Guess the problem</b>, and guess how you would stop it using only the softmax.</p>""",
        """<p>Watch for what softmax does with an input of −∞.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>To learn to predict the next word, a model must be tested on words it cannot see.
But plain self-attention lets every position look at every other — including the ones after it. A
model allowed to peek at the answer learns nothing except how to peek.</p>
<p>The fix is a <b>mask</b>: before the softmax, set every score for a future position to −∞.
Exponentiating −∞ gives 0, so those positions receive exactly zero weight. The model is now
structurally unable to look forward.</p>""")

        + lenses(
            """<p>An exam where the paper is revealed one question at a time and you cannot turn
back — or rather, cannot turn forward.</p>
<p>Not because you are trusted to be honest, but because the invigilator has physically covered the
rest of the page. It is a guarantee about what is possible, not a rule about what is permitted.</p>""",

            """<p>This is causality, in the signal-processing sense: an output may depend on the past
and the present, never on the future.</p>
<p>The same constraint appears in time-series forecasting, where using future information is called
<b>lookahead bias</b> and quietly invalidates a backtest. Financial modellers and language modellers
are guarding against precisely the same mistake.</p>""",

            """<p>A triangular sheet of paper laid over a square grid.</p>
<p>The upper-right triangle — every cell where the column is later than the row — is covered. Row 1
can see only column 1. Row 5 can see columns 1 through 5. The staircase edge is the “now” line moving
forward.</p>""",

            """<p>This single choice is the architectural difference between the two families of model
you have heard of. <b>Masked</b> (GPT and its descendants) can only look backwards, which is what
makes them able to generate text one token at a time. <b>Unmasked</b> (BERT) can see the whole
sentence at once, which makes it better at understanding and unable to generate.</p>
<p>Same mechanism, one triangle of −∞, two entirely different families of application.</p>""",

            """So the mask below is not a detail of implementation — it is the design decision that
determines what kind of model you have built.""")

        + h2("🎬", "Watch it move")
        + demo("c4-mask", "The triangle of −∞",
               "toggle the mask and watch the upper triangle of the weights vanish")

        + h2("🔢", "The maths, decoded")
        + eq("""scores<sub><var>ij</var></sub> <span class="op">=</span> −∞
&nbsp;&nbsp;for all <var>j</var> &gt; <var>i</var>""",
             "every position later than me becomes impossible")
        + """<p>Why −∞ rather than 0? Because the masking happens <b>before</b> the softmax. A score of
0 is not “ignore me” — it is a middling score, and after exponentiating it becomes
<var>e</var><sup>0</sup> = 1, a perfectly ordinary weight. Only −∞ exponentiates to exactly 0.</p>"""
        + table(["masked score", "e<sup>score</sup>", "resulting weight"],
                [["0", "1", "<b>ordinary</b> — not masked at all"],
                 ["−10", "0.0000454", "very small, but non-zero"],
                 ["<b>−∞</b>", "<b>0</b>", "<b>exactly zero — genuinely masked</b>"]])
        + key("""<p>In real code this is <code>-1e9</code> rather than true −∞, because arithmetic with
infinity produces NaN in some paths. A large negative number is close enough that the softmax weight
underflows to zero.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Masking after the softmax instead of before.</b> Zeroing weights afterwards
breaks the guarantee that they sum to 1, so the output is no longer an average. It must happen to the
scores.</p>""")
        + trap("""<p><b>Assuming masking is only for training.</b> A masked model is masked at
generation time too — it is how the architecture is defined, not a training-time restriction.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("Why −∞ and not 0?",
             "<p>Because masking happens before the softmax, and e<sup>0</sup> = 1 — a score of 0 is "
             "an ordinary, unremarkable score. Only e<sup>−∞</sup> = 0 removes the position "
             "entirely.</p>"),
            ("Which positions can position 4 attend to in a masked model?",
             "<p>Positions 1, 2, 3 and 4 — itself and everything before it. Never 5 onwards.</p>"),
            ("What kind of model do you get if you leave the mask out?",
             "<p>A bidirectional one, BERT-style: excellent at understanding a complete sentence, and "
             "incapable of generating text left to right, because it was never trained to predict "
             "something it could not see.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("paper", "https://arxiv.org/abs/1810.04805", "BERT (2018)",
             "The unmasked branch of the family tree, and what it is good at instead."),
        ])
    )))

# ============================================================ 8
L.append(dict(
    slug="08-the-cost", title="What attention costs", mins=11, tag="core",
    lede="Every pair of positions is compared, so the work grows with the square of the length. That "
         "one fact explains context-window pricing, and most of the research since 2020.",
    body=(
        pretest("""<p>Attention scores every position against every other. <b>Guess how the work grows as the sequence gets longer</b> — and what that implies for a model asked to read a whole book.</p>""",
        """<p>Watch the difference between doubling and squaring.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Attention compares every position with every other position. Ten tokens means a
10 × 10 grid — a hundred comparisons. A thousand tokens means a million. Ten thousand means a
hundred million.</p>
<p>Doubling the input does not double the work; it <b>quadruples</b> it. That single fact is why
context windows are a headline specification, why long inputs cost disproportionately more, and what a
large share of research since 2020 has been trying to fix.</p>""")

        + lenses(
            """<p>Handshakes at a party.</p>
<p>Ten people is 45 handshakes. Twenty people is 190 — not double, more than four times. Nobody shook
more hands than before; there are simply far more <em>pairs</em>. Attention is a room where everyone
must greet everyone.</p>""",

            """<p>This is O(T²) in both time and memory, and the memory is often the binding
constraint — the T × T score matrix has to exist, at least in tiles.</p>
<p>Compare an RNN at O(T): linear in length, but strictly serial. The transformer trades an
asymptotically worse cost for one that parallelises, and on real hardware that trade was worth
making — which is a useful reminder that asymptotic complexity is not the whole story.</p>""",

            """<p>A square grid that grows in both directions at once.</p>
<p>Add one token and you add a row <em>and</em> a column. The grid does not grow by one; it grows by
2T + 1. Watching the square fill in is watching the cost.</p>""",

            """<p>Counted: T = 1,000 is a million pairwise scores; T = 10,000 is a hundred million. At
a typical 0.75 words per token, a 100,000-token context is roughly a long novel — and ten billion
pairwise scores per layer, per head.</p>
<p>This is why long-context pricing is superlinear, why FlashAttention (a memory-efficient exact
implementation) was a significant result, and why approximate attention is an entire research
subfield.</p>""",

            """So the square below is the price of the one-step paths that made Week 1's problems go
away.""")

        + h2("🎬", "Watch it move")
        + demo("c4-cost", "The square, growing",
               "drag the sequence length and watch the comparison count")

        + h2("🧮", "Counted")
        + table(["sequence length T", "pairwise scores (T²)", "relative to T = 10"],
                [["10", "100", "1×"],
                 ["100", "10,000", "100×"],
                 ["1,000", "1,000,000", "10,000×"],
                 ["10,000", "100,000,000", "1,000,000×"]])
        + """<p>And that is per layer, per head. A 12-layer model with 8 heads multiplies every figure
in the middle column by 96.</p>"""
        + explain("""<p>An RNN is O(T) and attention is O(T²), yet the transformer won decisively.
<b>Why did the worse asymptotic cost not settle the argument?</b></p>""",
                  """<p>Because wall-clock time is not operation count — it is operation count divided
by how many you can do at once. An RNN's T steps are strictly sequential, so they cost T units of
<em>time</em> no matter what hardware you own. Attention's T² operations are independent, so on a
machine with thousands of parallel cores they cost far less time than the count suggests. The
transformer traded a quantity that hardware could absorb for one that it could not.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Assuming a longer context window is free once advertised.</b> Cost and latency
grow with the square, so filling a large window is materially more expensive than the token count
alone suggests.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("A model's context goes from 2,000 to 8,000 tokens. By what factor does attention work grow?",
             "<p>4× the length, so <b>16×</b> the pairwise comparisons. Not 4×.</p>"),
            ("Why is memory often the binding constraint rather than time?",
             "<p>Because the T × T score matrix must be held while the softmax runs. At T = 10,000 "
             "that is 100 million numbers per head per layer — which is why memory-efficient exact "
             "implementations were such a significant engineering result.</p>"),
            ("What did the field give up in exchange for this cost?",
             "<p>Nothing was given up — it was <b>bought</b>. One-step paths between any two positions "
             "(no forgetting) and full parallelism (no serial bottleneck). The square is the price of "
             "both.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("paper", "https://arxiv.org/abs/2205.14135", "FlashAttention (2022)",
             "Exact attention, reorganised so the T × T matrix never fully lands in slow memory. A rare case of a large practical win with no approximation."),
        ])
    )))

WEEK = dict(course="C4", week=2, title="Attention", lessons=L)
