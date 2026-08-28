# -*- coding: utf-8 -*-
"""C4 · Week 4 — From transformer to a language model."""
from kit import (kid, key, warn, trap, note, card, eq, eqp, decode, table, demo,
                 quiz, links, code, h2, grid2, grid3, pretest, explain, lenses)

L = []

# ============================================================ 1
L.append(dict(
    slug="01-next-token", title="The one job: predict the next token", mins=12, tag="core",
    lede="Every capability people find remarkable about language models comes out of a training "
         "objective that sounds far too simple to produce them.",
    body=(
        pretest("""<p>A model is trained on a very large amount of text with one objective. <b>Guess what it is</b> — and then guess whether that objective could plausibly produce a system that answers questions.</p>""",
        """<p>Watch for how much has to be learned in order to do the simple thing well.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Show the model some text, hide what comes next, ask it to predict. Compare with the
truth, adjust the weights, repeat — a few hundred billion times.</p>
<p>That is the whole of pretraining. No question-answering objective, no reasoning objective, no
instructions. Just: <b>what token comes next?</b></p>
<p>The reason this produces more than autocomplete is that predicting well <em>requires</em> more. To
finish “the capital of France is ___” you must have stored a fact. To finish “2 + 2 = ___” you must
have picked up arithmetic. The objective is simple; satisfying it is not.</p>""")

        + lenses(
            """<p>An apprentice who has spent ten years finishing their master's sentences.</p>
<p>They were never taught the trade explicitly. But to reliably guess what the master says next about
a joint, a timber, a customer — they had to absorb how the master thinks. The guessing was the
exercise; the understanding was the side effect.</p>""",

            """<p>Formally this is maximum likelihood estimation over sequences, factorised by the
chain rule: P(<var>x</var>) = ∏<sub><var>t</var></sub> P(<var>x</var><sub><var>t</var></sub> |
<var>x</var><sub>&lt;<var>t</var></sub>).</p>
<p>The loss is cross-entropy — the identical function from C2 W2, now over a 50,000-way softmax at
every position. Nothing about the objective is novel; the scale is what is novel.</p>""",

            """<p>A cloze test on an unimaginable scale.</p>
<p>“The Eiffel Tower is in ___.” Fill it in. Now do that for every position in 300 billion tokens —
roughly 225 billion words, or something like two million books' worth of text.</p>""",

            """<p>This is why the capabilities are <b>emergent</b> rather than designed, and why they
are hard to predict or guarantee. Nobody wrote a module for arithmetic; it appeared because it helped
predict tokens.</p>
<p>It is also why models hallucinate. A confident, fluent, false continuation is a <em>good</em>
next-token prediction in the sense the objective measures — the training signal never distinguished
plausible from true.</p>""",

            """So the loss below is C2 W2's cross-entropy, unchanged, and everything surprising comes
from what satisfying it demands.""")

        + h2("🎬", "Watch it move")
        + demo("c4-nexttoken", "Predict, compare, adjust",
               "one training step on one position — the same loop as C2 W2")

        + h2("🔢", "The maths, decoded")
        + eq("""<var>L</var> <span class="op">=</span> <span class="op">−</span>
<span class="big">Σ</span><sub><var>t</var></sub> log <var>P</var>
<span class="paren">(</span><var>x</var><sub><var>t</var></sub> <span class="op">|</span>
<var>x</var><sub>&lt;<var>t</var></sub><span class="paren">)</span>""",
             "cross-entropy, summed over every position")
        + decode([
            ("<var>x</var><sub>&lt;<var>t</var></sub>", "“x before t”", "Everything up to but not including position t. The causal mask is what guarantees the model only sees this."),
            ("<var>P</var>(<var>x</var><sub><var>t</var></sub> | …)", "“probability of x-t given …”", "The softmax output at position t, read off at the index of the token that actually came next."),
            ("−log", "“negative log”", "The logistic loss from C1 W3 and C2 W2. Confidently right costs almost nothing; confidently wrong costs enormously."),
        ])
        + note("""<p>Every position in the sequence contributes a loss term <em>simultaneously</em>.
A 1,000-token document supplies 1,000 training signals in one forward pass — which is a large part of
why this objective is so efficient at scale.</p>""", "Why this trains so efficiently")

        + h2("🧮", "Perplexity — the number papers quote")
        + """<p>Perplexity is <var>e</var> raised to the loss, and it has a genuinely useful reading:
<b>how many options the model is effectively choosing between</b>.</p>"""
        + table(["P(correct token)", "loss", "perplexity", "reading"],
                [["1/50257 (uniform)", "10.825", "50,257", "no idea at all — guessing uniformly"],
                 ["0.10", "2.303", "10.0", "effectively narrowed to 10 options"],
                 ["0.25", "1.386", "4.0", "narrowed to 4"],
                 ["0.50", "0.693", "2.0", "down to a coin flip"],
                 ["0.90", "0.105", "1.11", "almost certain"]])
        + """<p>A perplexity of 20 means the model is about as uncertain as if it were picking uniformly
from 20 possibilities — a far more intuitive figure than a loss of 3.0.</p>"""

        + h2("🕳", "Traps")
        + trap("""<p><b>Assuming the model has any notion of truth.</b> It was trained to predict likely
continuations, and “likely” and “true” coincide often but not always. This is the mechanism behind
hallucination, and it is not a bug that can be patched away — it is what the objective optimises.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("Why does a next-token objective produce factual knowledge?",
             "<p>Because storing the fact is <b>necessary</b> to predict well. Finishing “the capital "
             "of France is ___” with high probability requires having stored it — so gradient descent "
             "stores it.</p>"),
            ("What does a perplexity of 20 mean?",
             "<p>The model is about as uncertain as if it were choosing uniformly among 20 tokens. "
             "Lower is better; 1.0 would be perfect certainty and is never reached.</p>"),
            ("Why is hallucination a predictable consequence rather than a bug?",
             "<p>The objective rewards <b>likely</b> continuations. A fluent, confident, false "
             "statement can be a perfectly good prediction by that measure — nothing in the training "
             "signal distinguished plausible from true.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("lesson", "c2/w2-07-softmax.html", "C2 W2 · Softmax",
             "The output layer, now 50,257 wide and applied at every position."),
        ])
    )))

# ============================================================ 2
L.append(dict(
    slug="02-generation", title="How text actually comes out", mins=12, tag="core",
    lede="A model produces one probability distribution. Turning that into a paragraph requires a "
         "separate set of choices that are not part of the model at all — and they matter more than "
         "people expect.",
    body=(
        pretest("""<p>The model outputs a probability for each of 50,257 possible next tokens. <b>Guess what happens if you always pick the single most likely one</b>.</p>""",
        """<p>Watch for why the obvious answer produces bad writing.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>The model gives you a probability distribution over the next token. To produce text
you must <b>choose</b> one, append it, and run the model again on the longer sequence. Repeat.</p>
<p>Always picking the single highest-probability token sounds right and produces flat, repetitive
text that loops. So real systems <b>sample</b> — pick randomly, weighted by the probabilities — with
knobs controlling how adventurous that sampling is.</p>""")

        + lenses(
            """<p>A jazz musician who only ever plays the most expected note.</p>
<p>Every note is defensible; the solo is dead. Playing purely at random is noise. The skill is
sampling from what fits — mostly expected, occasionally not — and that is a dial, not a rule.</p>""",

            """<p>This is a sampling strategy over a categorical distribution, and it is entirely
separate from the model. <b>Temperature</b> divides the logits before the softmax: below 1 sharpens,
above 1 flattens. <b>Top-k</b> keeps only the k most likely; <b>top-p</b> (nucleus) keeps the smallest
set whose probabilities sum to p.</p>
<p>None of these change a single weight. Two systems with identical models can behave very
differently.</p>""",

            """<p>A dial from “boring” to “unhinged”.</p>
<p>At temperature 0.1 the model says the same thing every time. At 1.0 it follows its own
distribution honestly. At 2.0 it reaches for options it thinks are unlikely — which is sometimes
creative and more often incoherent.</p>""",

            """<p>Generation is <b>sequential</b> and this is the dominant cost of running a model.
Producing 1,000 tokens takes 1,000 forward passes, one after another — the training-time parallelism
across positions is gone entirely.</p>
<p>It is why responses stream in rather than appearing at once, why output tokens are priced higher
than input tokens, and why speeding up generation is such an intense engineering focus.</p>""",

            """So the temperature table below is a setting you control, sitting outside a model you
do not change.""")

        + h2("🎬", "Watch it move")
        + demo("c4-generate", "Temperature, and what it does",
               "the same distribution, sampled at different temperatures")

        + h2("🧮", "Temperature, computed")
        + """<p>Take four candidate tokens with raw scores [3.0, 2.0, 1.0, 0.5]. Divide by the
temperature, then softmax:</p>"""
        + table(["T", "cat", "dog", "car", "the", "behaviour"],
                [["0.1", "<b>1.000</b>", "0.000", "0.000", "0.000", "deterministic — same output every time"],
                 ["0.5", "0.862", "0.117", "0.016", "0.006", "focused"],
                 ["1.0", "0.631", "0.232", "0.085", "0.052", "the model's honest distribution"],
                 ["2.0", "0.442", "0.268", "0.163", "0.127", "flattened — reaching for unlikely options"]])
        + """<p>Note the model produced <em>one</em> set of scores. Everything in this table is what
happened afterwards, outside it.</p>"""
        + explain("""<p>Temperature divides the logits <em>before</em> the softmax rather than
adjusting the probabilities afterwards. <b>Why does that ordering matter?</b></p>""",
                  """<p>Because softmax is exponential, so dividing the scores rescales the
<em>ratios</em> between probabilities rather than shifting them uniformly. Halving the logits square-roots
every probability ratio, which is a smooth, principled sharpening that keeps the ordering intact and
keeps the result a valid distribution. Rescaling the probabilities directly would need renormalising
and would not have that clean interpretation — and at T → 0 the logit version limits neatly to
argmax.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Expecting deterministic output at default settings.</b> Sampling is random, so
the same prompt legitimately gives different answers. Temperature 0 makes it near-deterministic, at
the cost of flat, repetitive text.</p>""")
        + trap("""<p><b>Thinking a bad answer means a bad model.</b> It may be the sampling settings.
The same weights at T = 0.2 and T = 1.5 can look like two different systems.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("Why not always take the most likely token?",
             "<p>It produces flat, repetitive text that often falls into loops. Human language is not "
             "the most-likely continuation at every step, and greedy decoding sounds like it.</p>"),
            ("Does temperature change the model?",
             "<p>No. Not a single weight. It rescales the scores before the softmax, entirely outside "
             "the model — which is why it can be set per request.</p>"),
            ("Why does generating 1,000 tokens cost so much more than reading 1,000?",
             "<p>Reading is one parallel forward pass over all positions. Generating is 1,000 "
             "sequential passes, each one waiting for the last — the parallelism that made training "
             "fast is unavailable.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("paper", "https://arxiv.org/abs/1904.09751", "The Curious Case of Neural Text Degeneration (2019)",
             "Why greedy and beam search produce bland, repetitive text — the paper that introduced nucleus sampling."),
        ])
    )))

# ============================================================ 3
L.append(dict(
    slug="03-scale", title="What scale actually did", mins=12, tag="intuition",
    lede="The architecture barely changed between 2018 and 2023. Almost everything that changed was "
         "size — and the honest version of that story is more interesting than the headline.",
    body=(
        pretest("""<p>GPT-2 (2019) and GPT-3 (2020) use essentially the same architecture. <b>Guess what changed between them</b>, and by roughly what factor.</p>""",
        """<p>Watch for how little the design changed relative to the numbers.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>You have now built, conceptually, the entire architecture behind GPT. The block you
drew in Week 3 is the block in these models. What separates GPT-2 from GPT-3 is not a new idea — it
is roughly 1,400 times more parameters and vastly more data.</p>
<p>The uncomfortable finding of the last few years is how far that goes. Capabilities that looked
like they would need new architecture — arithmetic, translation, following instructions — largely
arrived by making the same thing bigger.</p>""")

        + lenses(
            """<p>The same recipe, cooked for a thousand times as many people.</p>
<p>Nothing about the method changed. But at that scale you need industrial ovens, a supply chain and
a team — the engineering is entirely different even though the recipe card is identical. Most of what
distinguishes a frontier lab is that engineering, not a secret recipe.</p>""",

            """<p>This is the empirical <b>scaling laws</b> literature: loss falls as a smooth power
law in parameters, data and compute, over many orders of magnitude.</p>
<p>The practical consequence is that performance became <em>predictable in advance</em> — you can
extrapolate from small runs to decide whether a large one is worth funding. That predictability, more
than any single result, is what made nine-figure training runs a rational decision.</p>""",

            """<p>A straight line on a log-log plot.</p>
<p>Loss against compute, over six orders of magnitude, remarkably straight. That line is the entire
economic argument for the last five years of the field.</p>""",

            """<p>The honest caveats matter here. Scaling laws describe <em>loss</em>, and loss is not
capability — the relationship between them is much less well understood. “Emergent” capabilities that
appear suddenly at scale have been shown in some cases to be artefacts of how the capability was
measured rather than genuine phase changes.</p>
<p>And the curves flatten. Diminishing returns are built into a power law, which is why data quality,
architecture efficiency and post-training have become the active frontiers rather than raw size.</p>""",

            """So the numbers below are the story, and the design column is the part worth noticing.""")

        + h2("🎬", "Watch it move")
        + demo("c4-scale-story", "Four years of scale",
               "the same architecture, three orders of magnitude apart")

        + h2("🧮", "The numbers")
        + table(["", "GPT-2 (2019)", "GPT-3 (2020)", "factor"],
                [["parameters", "1.5 B", "175 B", "×117"],
                 ["layers", "48", "96", "×2"],
                 ["width", "1,600", "12,288", "×7.7"],
                 ["context", "1,024", "2,048", "×2"],
                 ["training tokens", "~10 B", "~300 B", "×30"],
                 ["<b>architecture</b>", "transformer decoder", "transformer decoder", "<b>unchanged</b>"]])
        + """<p>300 billion tokens is roughly 225 billion words — on the order of two million books.
The last row is the one worth sitting with.</p>"""

        + h2("🕳", "Traps")
        + trap("""<p><b>Concluding that scale is all that matters.</b> Data quality, the mix of training
sources, and post-training (the next lesson) all move results substantially at fixed size. The scaling
story is real and is routinely over-told.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("What is the main architectural difference between GPT-2 and GPT-3?",
             "<p>Essentially none. Same transformer decoder block. The differences are parameter "
             "count, data, context length and the engineering to train at that scale.</p>"),
            ("Why do scaling laws matter commercially, not just scientifically?",
             "<p>Because they make performance predictable before you spend the money. You can "
             "extrapolate from cheap small runs to decide whether an expensive large one is "
             "justified.</p>"),
            ("Give one honest limitation of the scaling story.",
             "<p>Scaling laws describe loss, not capability, and the link between them is poorly "
             "understood. Some “emergent” jumps have turned out to be artefacts of the metric rather "
             "than real phase changes.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("paper", "https://arxiv.org/abs/2206.07682", "Emergent Abilities of Large Language Models (2022)",
             "The claim that some capabilities appear suddenly with scale."),
            ("paper", "https://arxiv.org/abs/2304.15004", "Are Emergent Abilities a Mirage? (2023)",
             "The rebuttal, arguing several of those jumps are artefacts of discontinuous metrics. Read both."),
        ])
    )))

# ============================================================ 4
L.append(dict(
    slug="04-rlhf", title="RLHF — from text predictor to assistant", mins=13, tag="core",
    lede="A pretrained model completes text. It does not answer questions, follow instructions or "
         "decline anything. Turning it into something useful is a second training stage — and it is "
         "reinforcement learning, which you already know.",
    body=(
        pretest("""<p>A raw pretrained model is asked “What is the capital of France?”. <b>Guess what it might do</b> — remembering its only skill is continuing text plausibly.</p>""",
        """<p>Watch for the gap between “likely continuation” and “helpful answer”.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Ask a raw pretrained model “What is the capital of France?” and a perfectly good
continuation is “What is the capital of Germany? What is the capital of Spain?” — because in its
training data, questions are often followed by more questions.</p>
<p>It is not being unhelpful. It has no concept of helpful. It completes text.</p>
<p>Turning it into an assistant takes a second stage: show it examples of good answers, then have
people rank competing answers, train a model to predict those rankings, and use that as a
<b>reward</b> to fine-tune the original. That last part is reinforcement learning — which you learned
in Course 3.</p>""")

        + lenses(
            """<p>Someone who has read every cookbook ever written but never cooked for a guest.</p>
<p>They know everything about food and nothing about what <em>you</em> wanted for dinner. Making them
useful is not more reading — it is service, feedback, and being told “less salt next time” by real
people, repeatedly.</p>""",

            """<p>Three stages. <b>Supervised fine-tuning</b> on demonstration data teaches the format
of an answer. A <b>reward model</b> is trained on human preference comparisons — which of these two
answers is better. Then <b>policy optimisation</b> (PPO, or increasingly simpler alternatives like
DPO) fine-tunes the model against that reward.</p>
<p>The reward model exists because human judgement is too slow and too expensive to be in the loop
for every gradient step. It is a learned stand-in for a person.</p>""",

            """<p>Two answers side by side and a human clicking the better one.</p>
<p>That click, repeated tens of thousands of times, is the entire training signal for the reward
model. Everything about a model's tone, helpfulness and willingness to refuse traces back to those
clicks and to whoever was clicking.</p>""",

            """<p>This is the single biggest deployed application of reinforcement learning that
exists — which is worth noting given Course 3's honest caveat that RL rarely ships. It shipped here,
at enormous scale.</p>
<p>It is also where a system's values come from, and that is not a neutral technical detail. Who wrote
the guidelines, who was hired to do the ranking, and what they were told to prefer are all decisions
that end up encoded in the model's behaviour.</p>""",

            """So the reward below is C3 W3's reward, and the policy being optimised is a language
model.""")

        + h2("🎬", "Watch it move")
        + demo("c4-rlhf", "Three stages, one assistant",
               "pretrain, demonstrate, then optimise against human preference")

        + h2("🧮", "The three stages")
        + table(["stage", "data", "what it teaches", "cost"],
                [["1 · pretraining", "hundreds of billions of tokens of text", "language, facts, reasoning patterns", "enormous — months of compute"],
                 ["2 · supervised fine-tuning", "tens of thousands of written demonstrations", "the <b>format</b> of a helpful answer", "modest"],
                 ["3 · RLHF", "human rankings of competing answers", "which answers people actually prefer, and what to decline", "modest"]])
        + """<p>Note the asymmetry: stage 1 is where essentially all the capability comes from, and
stages 2 and 3 are where the <b>behaviour</b> comes from. They are cheap by comparison and they change
the experience of using the model completely.</p>"""
        + key("""<p>Course 3 Week 3 taught reward, policy and the idea of optimising behaviour with no
labelled correct answer. That is exactly this — the policy is a language model and the reward is a
learned model of human preference. The RL week was not a detour.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Assuming RLHF makes a model truthful.</b> It makes it produce answers people
<em>rate highly</em>, which correlates with truthfulness and is not the same thing. A confident,
well-formatted wrong answer can be rated above a hedged correct one — a known failure mode called
sycophancy.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("Why does a raw pretrained model not answer questions?",
             "<p>Because it was only ever trained to continue text plausibly, and in its training "
             "data a question is often followed by more questions. Answering is a behaviour that has "
             "to be taught separately.</p>"),
            ("Why is a reward model needed rather than asking humans directly?",
             "<p>Because RL needs a reward at every step, and humans are far too slow and expensive "
             "for that. The reward model is a learned stand-in trained on human comparisons.</p>"),
            ("Where does a model's willingness to decline a request come from?",
             "<p>Stages 2 and 3 — demonstrations and human preference rankings, shaped by whatever "
             "guidelines the people doing the ranking were given. It is a trained behaviour, not an "
             "architectural property.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("lesson", "c3/w3-01-what-is-rl.html", "C3 W3 · What is reinforcement learning",
             "The foundation this is built on. Worth rereading now that you know where it ends up."),
            ("paper", "https://arxiv.org/abs/2203.02155", "Training language models to follow instructions (InstructGPT, 2022)",
             "The paper describing the three-stage recipe above."),
        ])
    )))

# ============================================================ 5
L.append(dict(
    slug="05-context-and-cost", title="Context windows and what they cost", mins=11, tag="core",
    lede="Why the headline number in every model announcement is a context length, and what it "
         "actually costs to use it.",
    body=(
        pretest("""<p>Attention is O(T²) and generation is sequential. <b>Guess what a very long context costs</b> — in compute, and in memory that has to be held during generation.</p>""",
        """<p>Watch for a cost that grows even when the model itself does not.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>The context window is how many tokens the model can attend to at once. It is the
model's entire working memory: anything outside it does not exist.</p>
<p>Two things make it expensive. Attention is quadratic, so doubling the context quadruples the
comparison work. And during generation the model caches the keys and values for every previous token
so it does not recompute them — that cache grows linearly with context and has to live in fast
memory.</p>""")

        + lenses(
            """<p>A desk you can spread papers on.</p>
<p>A bigger desk lets you work with more documents at once. It does not make you cleverer, and finding
things on it takes longer. Papers that fall off the edge are simply gone — the model has no memory
whatsoever outside its window.</p>""",

            """<p>Two distinct costs. <b>Compute</b> scales as O(T²) for attention. <b>Memory</b>
scales as O(T) for the KV cache, and that one is usually the binding constraint on how many
simultaneous users a machine can serve.</p>
<p>Almost every serving optimisation you read about — paged attention, multi-query and grouped-query
attention, quantised caches — is aimed at that cache rather than at the model weights.</p>""",

            """<p>A conveyor belt of fixed length.</p>
<p>New tokens arrive at one end; once the belt is full, the oldest fall off the other. There is no
storage under the belt. A conversation that scrolls past the window is not summarised or remembered —
it is gone.</p>""",

            """<p>Computed for GPT-2 small: at its native 1,024-token context the KV cache is about
<b>38 MB</b> per sequence. Give the same model a 128k context and that cache becomes about
<b>4.7 GB</b> — for one conversation.</p>
<p>Multiply by the number of concurrent users and it is clear why long context is priced the way it
is, and why it is a serving problem before it is a modelling one.</p>""",

            """So the numbers below explain both the pricing page and why “just make the window
bigger” is not free.""")

        + h2("🎬", "Watch it move")
        + demo("c4-context", "The window, and what falls off",
               "the KV cache growing as the conversation gets longer")

        + h2("🧮", "Counted")
        + table(["context length", "attention comparisons", "KV cache (GPT-2 small, fp16)"],
                [["1,024", "1.0 M", "38 MB"],
                 ["8,192", "67 M", "302 MB"],
                 ["32,768", "1.07 B", "1.2 GB"],
                 ["128,000", "16.4 B", "<b>4.7 GB</b>"]])
        + """<p>And that is for a 124-million-parameter model. The cache for a frontier-scale model at
long context is substantially larger than the entire GPT-2 small network.</p>"""
        + explain("""<p>The KV cache exists to avoid recomputing keys and values for tokens already
processed. <b>Why is that trade — memory for compute — worth making?</b></p>""",
                  """<p>Because without it, generating token <var>n</var> would mean recomputing the
whole sequence's keys and values from scratch, making generation O(T²) <em>per token</em> and O(T³)
overall. The cache turns that into O(T) per token. It is the difference between generation being
feasible and not — which is why the memory cost is accepted and then attacked with every trick
available.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Treating a large advertised context as usable end to end.</b> Retrieval quality
often degrades in the middle of long contexts — the “lost in the middle” effect — so a model may
attend well to the start and end and poorly to the centre.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("Why does the KV cache exist?",
             "<p>To avoid recomputing keys and values for every previous token at every generation "
             "step. Without it generation would be cubic in length rather than quadratic.</p>"),
            ("A context goes from 4k to 32k. What happens to attention work and to cache size?",
             "<p>Attention work: ×64 (8² ). Cache: ×8, linear. Different scaling, and the cache is "
             "usually the binding constraint on serving.</p>"),
            ("What happens to a conversation that exceeds the window?",
             "<p>The oldest tokens fall out and are simply gone — there is no memory outside the "
             "window. Any apparent longer-term memory is an application feature (summarising, or "
             "retrieval) built on top.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("paper", "https://arxiv.org/abs/2307.03172", "Lost in the Middle (2023)",
             "Measures how retrieval accuracy varies with where the relevant information sits in a long context."),
        ])
    )))

# ============================================================ 6
L.append(dict(
    slug="06-what-it-cannot-do", title="What these models cannot reliably do", mins=13, tag="core",
    lede="Knowing the failure modes, and why each one follows from the architecture, is as much a "
         "mark of understanding as knowing the capabilities.",
    body=(
        pretest("""<p>You now know the objective is next-token prediction and the architecture is attention over a fixed window. <b>Guess three things that will therefore be unreliable</b>.</p>""",
        """<p>Watch for failures that follow from the design rather than from insufficient training.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Every limitation below follows from something you have already learned. None of
them are mysteries, and none are obviously fixable by training harder.</p>
<p>Being able to predict where a system will fail — from how it was built — is a large part of what
it means to actually understand it.</p>""")

        + lenses(
            """<p>A brilliant improviser who has never been told they are allowed to say “I don't
know”.</p>
<p>Asked something outside their knowledge, they produce something fluent and plausible, because
that is what the job has always rewarded. The failure is not dishonesty; nothing in the training ever
distinguished confident invention from confident recall.</p>""",

            """<p>Each failure traces to a specific mechanism. <b>Hallucination</b>: the objective
rewards likely, not true. <b>No calibrated uncertainty</b>: the softmax always produces a confident
distribution; there is no “abstain” token. <b>Arithmetic</b>: learned as token patterns rather than
as an algorithm, so it degrades on unfamiliar magnitudes. <b>Character-level tasks</b>: the model sees
subword chunks, not letters.</p>""",

            """<p>A map with no edges marked.</p>
<p>Inside the well-travelled region it is excellent. Outside, it does not go blank — it keeps drawing
coastlines with the same confidence. There is no boundary line saying “beyond here I am guessing”.</p>""",

            """<p>This matters most in exactly the settings where these systems are being deployed —
medical, legal, financial summarisation. The failure mode is not obviously-wrong output; it is
<b>plausible</b> wrong output delivered in the same confident register as correct output.</p>
<p>Which is precisely why the practical guidance is verification and retrieval-grounding rather than
trust, and why knowing these limits is a professional skill rather than a caveat.</p>""",

            """So the table below is not a list of complaints — it is a set of predictions you can now
make from first principles.""")

        + h2("🎬", "Watch it move")
        + demo("c4-limits", "Five failures, five causes",
               "each one traced back to a mechanism you have already learned")

        + h2("🧮", "The failures, and their causes")
        + table(["failure", "why, mechanically", "from which lesson"],
                [["hallucination — confident falsehoods", "the objective rewards <b>likely</b> continuations; nothing distinguished true from plausible", "W4 L1"],
                 ["poor calibration — no “I don't know”", "the softmax always yields a confident distribution; there is no abstain option", "C2 W2"],
                 ["arithmetic on unfamiliar numbers", "learned as token patterns, not as an algorithm", "W4 L1"],
                 ["counting letters in a word", "the model receives subword chunks, never letters", "W1 L2"],
                 ["forgetting earlier conversation", "anything outside the context window does not exist", "W4 L5"],
                 ["inconsistency between runs", "generation samples randomly from a distribution", "W4 L2"]])
        + key("""<p>Every row's cause is something you learned in this course. That is the point of the
table — not that these systems are unreliable, but that <b>where</b> they are unreliable is
predictable from how they work.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Assuming a bigger model fixes these.</b> Scale reduces the frequency of several
of them and removes none. Hallucination in particular follows from the objective, not from
capacity.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("Why is a model bad at counting the letters in a word?",
             "<p>Because it never receives letters. Tokenization gives it subword chunks, so letter "
             "structure inside a chunk is something it must have inferred indirectly rather than "
             "something it can read.</p>"),
            ("Why does a model rarely say “I don't know”?",
             "<p>The softmax always produces a distribution over real tokens, and there is no abstain "
             "option in the vocabulary. Saying so has to be <b>trained in</b> during RLHF; it is not "
             "a natural output of the architecture.</p>"),
            ("Name one failure that scale genuinely does reduce, and one it does not.",
             "<p>Reduces: arithmetic on common magnitudes, and factual recall of well-represented "
             "facts. Does not remove: hallucination, which follows from what the objective rewards "
             "rather than from how much capacity the model has.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("paper", "https://arxiv.org/abs/2311.05232", "A Survey of Hallucination in LLMs (2023)",
             "A structured taxonomy of the failure and the current mitigations."),
        ])
    )))

# ============================================================ 7
L.append(dict(
    slug="07-where-to-go-next", title="Where to go from here", mins=10, tag="core",
    lede="What you now know, what you do not, and the honest map of what is worth learning next.",
    body=(
        pretest("""<p>You have now traced the path from a dot product to a working language model. <b>Guess what is still missing</b> before you could build or deploy one.</p>""",
        """<p>Watch for the difference between understanding a mechanism and being able to ship it.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>You can now read the architecture section of most modern papers, compute a model's
parameter count from its config, and explain why it fails where it does.</p>
<p>What you cannot yet do is build one that works at scale, or deploy one responsibly. Those are
different skills, and it is worth being clear about which is which.</p>""")

        + h2("📋", "What you can now do")
        + table(["", "you can"],
                [["1", "read <i>Attention Is All You Need</i> and follow every component"],
                 ["2", "compute attention by hand, and any model's parameter count from its config"],
                 ["3", "explain why context windows are expensive, and why in two distinct ways"],
                 ["4", "predict where a language model will fail, from how it works"],
                 ["5", "distinguish the GPT and BERT families and say which suits a task"]])

        + h2("🧭", "What is genuinely still missing")
        + table(["area", "what it covers", "why it matters"],
                [["<b>CNNs and vision</b>", "convolution, pooling, image models", "the other major architecture family; also how vision-language models work"],
                 ["<b>Training at scale</b>", "distributed training, mixed precision, data pipelines", "the gap between understanding a model and producing one"],
                 ["<b>Practitioner LLM skills</b>", "prompting, RAG, embeddings and vector search, LoRA fine-tuning, agents", "what most people building on LLMs actually do day to day"],
                 ["<b>Deeper maths</b>", "eigenvectors and SVD, maximum likelihood, matrix calculus", "lets you read <em>method</em> sections rather than skipping to results"],
                 ["<b>MLOps</b>", "monitoring, drift, evaluation, rollback", "the difference between a notebook and a system"],
                 ["<b>Safety and interpretability</b>", "alignment, evaluations, mechanistic interpretability", "increasingly the most interesting open problems"]])
        + note("""<p>If you want one next step: the practitioner LLM skills are the most immediately
useful, and mechanistic interpretability is the most intellectually interesting given what you now
know. Both build directly on this course.</p>""", "If you only pick one")

        + h2("🎬", "Watch it move")
        + demo("c4-roadmap", "The whole path, and what comes next",
               "from a dot product to a language model, and the roads leading out")

        + h2("🧮", "The whole specialization, in one line")
        + table(["", "the one idea"],
                [["Foundations", "a function is a machine; a derivative is its speedometer"],
                 ["Course 1", "model + cost + gradient descent"],
                 ["Course 2", "stack the model; diagnose it before you change it"],
                 ["Course 3", "learn without labels; learn from reward"],
                 ["<b>Course 4</b>", "<b>let every position read every other, in one step</b>"]])
        + key("""<p>Every course is the same three parts — a model, a cost, an optimiser. Course 4
changed only the model. The cost is still cross-entropy from Course 2, and the optimiser is still Adam
from Course 2. That continuity is real, and it is the most useful thing to carry forward.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("What are the three parts every algorithm in all four courses shares?",
             "<p>A <b>model</b> (what f is allowed to be), a <b>cost</b> (one number for how wrong it "
             "is), and an <b>optimiser</b> (gradient descent, usually Adam). Course 4 changed only "
             "the first.</p>"),
            ("Someone says an LLM “understands” a document. What is the precise version of that claim?",
             "<p>It computes representations of each token that are contextualised by every other "
             "token in the window, in a way that supports accurate next-token prediction. Whether "
             "that constitutes understanding is a genuinely open question, and the mechanism is what "
             "you can state confidently.</p>"),
            ("Why is the RL week of Course 3 more relevant than it first appeared?",
             "<p>Because RLHF — the stage that turns a text predictor into an assistant — is "
             "reinforcement learning, and it is the largest deployed application of RL that "
             "exists.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("paper", "https://arxiv.org/abs/1706.03762", "Attention Is All You Need",
             "Read it end to end now. It should be almost entirely legible."),
            ("video", "https://www.youtube.com/watch?v=kCc8FmEb1nY",
             "Karpathy — building GPT from scratch",
             "Two hours, in code, assuming exactly what you now know. The natural next thing to do."),
        ])
    )))

WEEK = dict(course="C4", week=4, title="From Transformer to Language Model", lessons=L)
