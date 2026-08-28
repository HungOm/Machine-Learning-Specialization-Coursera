# -*- coding: utf-8 -*-
"""Review cards — Course 4, attention and transformers."""
from cardkit import C, deck, blk, steps, bullets, two, hint

W1 = deck("C4", 1, "Sequences, Embeddings and the Old Answers", [
    C("c4w1-order", "concept",
      "Why can a bag-of-words model never distinguish “the dog bit the man” from "
      "“the man bit the dog”?",
      "<p>Because it receives the same input for both: identical words, identical counts. Order is "
      "not <em>lost detail</em> — it was never encoded.</p>"
      + bullets(["everything in C1–C3 treated an example as an unordered set of features",
                 "a sequence is not a set: <var>x</var> = (x&lt;1&gt;, …, x&lt;T&gt;)",
                 "T varies per example, unlike n — which forces padding and masking"])
      + hint("Three superscript styles now: (i) = which example, [l] = which layer, &lt;t&gt; = which position."),
      "c4/w1-01-why-order-matters.html"),

    C("c4w1-tokens", "concept",
      "Why do models use <b>subword</b> tokens rather than words or characters?",
      two("<ul class='cbul'><li>whole words: vocabulary is unbounded and any unseen word is "
          "unrepresentable</li><li>characters: sequences become very long and each piece means "
          "almost nothing</li></ul>",
          "<ul class='cbul'><li>subword (BPE): ~30k–100k vocabulary</li><li>single characters stay "
          "in the vocabulary, so <b>nothing is ever unrepresentable</b></li></ul>",
          "the two extremes", "the compromise")
      + hint("~0.75 words per token in English. It is also why models are bad at spelling — they "
             "never see letters, only chunks."),
      "c4/w1-02-tokens.html"),

    C("c4w1-onehot", "trap",
      "One-hot encoding worked for decision trees. What are its <b>two</b> failures for a "
      "50,000-word vocabulary?",
      bullets(["<b>size</b> — 50,000 numbers per word, and 25.6 M parameters into a 512-unit layer, "
                 "almost all multiplying zeros",
                 "<b>meaning</b> — every pair of distinct words has dot product exactly <b>0</b>, so "
                 "“cat” is as similar to “dog” as to “bulldozer”"])
      + "<p>The second is the fatal one: the encoding destroys the only signal downstream dot "
        "products could use.</p>"
      + hint("Using the word's index as a number is worse — it invents an ordering that does not exist."),
      "c4/w1-03-one-hot-and-why-it-fails.html"),

    C("c4w1-embedding", "formula",
      "What <b>is</b> an embedding, mechanically?",
      blk("<var>E</var> ∈ ℝ<sup><var>V</var> × <var>d</var></sup> &nbsp;&nbsp; "
          "<var>e</var><sub><var>w</var></sub> = <var>E</var>[<var>w</var>]")
      + bullets(["a matrix of <b>learned parameters</b>, one row per token",
                 "“embedding a token” = looking up its row",
                 "mathematically identical to multiplying the one-hot vector by E — the 1 selects "
                 "one row and the zeros delete the rest"])
      + hint("You built this in C3 W2: collaborative filtering learned a feature vector per movie "
             "with no genre labels. Same construction, words instead of films."),
      "c4/w1-04-embeddings.html"),

    C("c4w1-cosine", "number",
      "king = [2,1,0], queen = [3,1,0]. Compute the cosine similarity.",
      blk("dot = 2(3) + 1(1) + 0(0) = <b>7</b>")
      + blk("‖king‖ = √5 = 2.236 &nbsp;&nbsp; ‖queen‖ = √10 = 3.162")
      + blk("cos = 7 ÷ (2.236 × 3.162) = <b>0.990</b>")
      + hint("Against banana = [0,1,2] it is 0.200. Cosine divides out both lengths so only "
             "direction counts — magnitude tracks training frequency, which is not what you want "
             "to compare meanings on."),
      "c4/w1-04-embeddings.html"),

    C("c4w1-rnn", "algorithm",
      "What does an RNN do, in one formula and one sentence?",
      blk("<var>h</var>&lt;t&gt; = <var>g</var>(<var>W<sub>h</sub>h</var>&lt;t−1&gt; + "
          "<var>W<sub>x</sub>x</var>&lt;t&gt; + <var>b</var>)")
      + "<p>Read one item at a time, carrying a running summary. Update the summary from the old "
        "summary plus the new item.</p>"
      + hint("The weights are <b>shared across positions</b> — that is why one fixed-size model "
             "handles any sequence length."),
      "c4/w1-05-rnn-idea.html"),

    C("c4w1-rnn-fails", "distinguish",
      "The <b>two</b> reasons RNNs were replaced — and which one an LSTM fixes.",
      two("<b>Forgetting</b><ul class='cbul'><li>slopes multiply once per timestep</li>"
          "<li>at 0.25/step, 20 steps back = 9.1 × 10⁻¹³</li>"
          "<li>LSTM <b>does</b> mitigate this — gates let information pass unmultiplied</li></ul>",
          "<b>Serial dependency</b><ul class='cbul'><li>step t needs step t−1</li>"
          "<li>cannot use parallel hardware at all</li>"
          "<li>LSTM does <b>nothing</b> for this — it is architectural</li></ul>",
          "problem 1", "problem 2")
      + hint("Same vanishing-gradient arithmetic as deep sigmoid nets in C2 W2 — one factor per "
             "timestep instead of per layer, and sequences are far longer than nets are deep."),
      "c4/w1-06-why-rnns-failed.html"),

    C("c4w1-attention-2014", "concept",
      "What did attention (2014) fix, and how?",
      "<p>The <b>bottleneck</b>: translation models compressed a whole sentence into one fixed "
      "vector before writing a single output word.</p>"
      + blk("<var>c</var> = Σ<sub><var>t</var></sub> <var>α</var><sub><var>t</var></sub> "
            "<var>h</var>&lt;t&gt;")
      + bullets(["keep <b>every</b> position's summary, not just the last",
                 "weights α come from a softmax, so they are positive and sum to 1",
                 "recomputed fresh for <b>every output word</b>"])
      + hint("Softmax rather than picking the best because argmax has no gradient — the choosing "
             "itself has to be trainable."),
      "c4/w1-07-the-bottleneck.html"),
])

W2 = deck("C4", 2, "Attention", [
    C("c4w2-formula", "formula",
      "The attention formula — write it out.",
      blk("Attention(<var>Q</var>, <var>K</var>, <var>V</var>) = softmax"
          "(<span class='fr'><span><var>QK</var><sup>T</sup></span>"
          "<span>√<var>d<sub>k</sub></var></span></span>) <var>V</var>")
      + "<p>Read it right to left: <b>score every pair, turn the scores into weights summing to 1, "
        "take a weighted average.</b></p>"
      + hint("Both halves are things you already knew — the dot product from F0 W1 and softmax from "
             "C2 W2. Nothing mathematically new is introduced."),
      "c4/w2-01-the-idea.html"),

    C("c4w2-qkv", "distinguish",
      "Query, key and value — what is each one, and where do they come from?",
      bullets(["<b>Q</b> — what am I looking for?",
               "<b>K</b> — what do I advertise about myself?",
               "<b>V</b> — what do I hand over if chosen?"])
      + blk("<var>Q</var> = <var>XW<sub>Q</sub></var> &nbsp; <var>K</var> = <var>XW<sub>K</sub></var> "
            "&nbsp; <var>V</var> = <var>XW<sub>V</sub></var>")
      + "<p>Three <b>learned projections of the same input</b>. Key and value are separate on "
        "purpose: what makes a word easy to find is not what makes it useful to read.</p>"
      + hint("A library: your request (Q), the catalogue card (K), the book (V)."),
      "c4/w2-02-query-key-value.html"),

    C("c4w2-shapes", "trap",
      "For T positions and query size d<sub>k</sub>, what shape is QK<sup>T</sup> — and what shape "
      "does attention output?",
      bullets(["<var>Q</var>, <var>K</var> are (T, d<sub>k</sub>)",
               "<var>QK</var><sup>T</sup> is <b>(T, T)</b> — d<sub>k</sub> is the inner dimension and vanishes",
               "output is (T, d<sub>v</sub>) — <b>one vector per input position</b>"])
      + hint("The output having the same number of rows as the input is what lets attention layers "
             "<b>stack</b>. A layer that changed the length could not be repeated."),
      "c4/w2-02-query-key-value.html"),

    C("c4w2-byhand", "number",
      "Q = K = [[1,0],[0,1],[1,1]], d<sub>k</sub> = 2. What are the attention weights in row 1, "
      "and what must they sum to?",
      blk("scores: [1, 0, 1] &nbsp;→&nbsp; ÷√2: [0.7071, 0, 0.7071]")
      + blk("softmax: <b>[0.4011, 0.1978, 0.4011]</b> &nbsp;&nbsp; sum = <b>1.0000</b>")
      + "<p>e<sup>0.7071</sup> = 2.028, e<sup>0</sup> = 1, total 5.056. 2.028 ÷ 5.056 = 0.4011.</p>"
      + hint("Rows sum to 1; columns do not. Softmaxing the wrong axis runs without error and "
             "produces meaningless output — the most common bug here."),
      "c4/w2-03-attention-by-hand.html"),

    C("c4w2-scale", "concept",
      "Why divide the scores by √d<sub>k</sub>?",
      "<p>Because a dot product of d<sub>k</sub> unit-variance components has standard deviation "
      "<b>√d<sub>k</sub></b>. Bigger vectors give bigger scores for no meaningful reason.</p>"
      + bullets(["measured at d<sub>k</sub> = 512: spread 22.591, and √512 = 22.627",
                 "oversized scores <b>saturate</b> the softmax into a near one-hot",
                 "a saturated softmax has ~zero gradient, so the layer stops learning"])
      + hint("Same instinct as feature scaling in C1 W2 — keep the numbers entering a nonlinearity "
             "in the range where it still responds."),
      "c4/w2-05-why-scale.html"),

    C("c4w2-multihead", "concept",
      "What does multi-head attention buy, and what does it cost?",
      "<p>Several attentions in parallel, each with its own W<sub>Q</sub>, W<sub>K</sub>, "
      "W<sub>V</sub>, concatenated and mixed by a final W<sub>O</sub>.</p>"
      + bullets(["a word relates to a sentence in several ways at once; one head computes one "
                 "weighted average and so can chase only one",
                 "cost: <b>nothing</b> — 8 heads of size 64 is the same parameter count as 1 head "
                 "of size 512",
                 "W<sub>O</sub> matters: without it the heads' outputs never interact"])
      + hint("Honest caveat: many heads can be pruned after training with little loss."),
      "c4/w2-06-multi-head.html"),

    C("c4w2-mask", "trap",
      "Why is the causal mask −∞ rather than 0?",
      "<p>Because masking happens <b>before</b> the softmax.</p>"
      + bullets(["score 0 → e<sup>0</sup> = 1 → an ordinary, unremarkable weight",
                 "score −∞ → e<sup>−∞</sup> = 0 → genuinely removed"])
      + "<p>In code it is <code>-1e9</code>, because arithmetic with true infinity produces NaN in "
        "some paths.</p>"
      + hint("This one triangle is the whole architectural difference between GPT (masked, can "
             "generate) and BERT (unmasked, better at understanding)."),
      "c4/w2-07-masking.html"),

    C("c4w2-cost", "number",
      "Context goes from 2,000 to 8,000 tokens. By what factor does attention work grow — and why "
      "did the transformer win anyway?",
      "<p>4× the length → <b>16×</b> the pairwise comparisons. O(T²).</p>"
      + "<p>It won because wall-clock time is operation count <em>divided by how many you can do at "
        "once</em>. An RNN's T steps are strictly serial; attention's T² operations are "
        "independent.</p>"
      + hint("It traded a quantity hardware could absorb (parallel work) for one it could not "
             "(serial dependency)."),
      "c4/w2-08-the-cost.html"),
])

W3 = deck("C4", 3, "The Transformer Block", [
    C("c4w3-posenc", "concept",
      "Why does a transformer need positional encoding at all?",
      "<p>Because attention is a weighted <b>average</b>, and an average is order-blind. Shuffle the "
      "inputs and the outputs shuffle identically — nothing else changes.</p>"
      + bullets(["a distinctive pattern is <b>added</b> to each embedding before attention runs",
                 "sinusoids at geometrically-spaced frequencies — fast dims separate neighbours, "
                 "slow dims separate distant positions",
                 "every position's encoding has the same magnitude, since sin² + cos² = 1"])
      + hint("Context-window extension is largely a positional-encoding problem — RoPE and ALiBi "
             "are schemes for exactly this."),
      "c4/w3-01-positional-encoding.html"),

    C("c4w3-residual", "formula",
      "Write the residual connection, differentiate it, and say why the result matters.",
      blk("<var>y</var> = <var>x</var> + Sublayer(<var>x</var>)")
      + blk("∂<var>y</var>/∂<var>x</var> = <b>1</b> + ∂Sublayer/∂<var>x</var>")
      + "<p>The <b>1</b> is an identity path that no chain of multiplications can shrink.</p>"
      + bullets(["without: 12 layers at 0.7 each → 0.7¹² = <b>0.014</b> of the gradient",
                 "with: the identity route delivers 1.0 at any depth"])
      + hint("Third appearance of the same enemy: deep sigmoid nets (C2 W2), RNNs across time "
             "(C4 W1), and now depth. Residuals are the cleanest answer."),
      "c4/w3-02-residuals.html"),

    C("c4w3-layernorm", "formula",
      "Layer normalization — the formula, and what it averages over.",
      blk("LN(<var>x</var>) = <var>γ</var> · "
          "<span class='fr'><span><var>x</var> − <var>μ</var></span><span><var>σ</var></span></span> + <var>β</var>")
      + bullets(["μ and σ are computed across <b>one position's d features</b> — not across the batch",
                 "γ and β are learned, so the layer can undo the normalisation if that helps",
                 "x = [2,8,4,6] → mean 5, sd 2.236 → [−1.342, 1.342, −0.447, 0.447]"])
      + hint("It is C1 W2's z-score applied inside the network. Not batch norm — which would make "
             "an example's output depend on which others share its batch."),
      "c4/w3-03-layer-norm.html"),

    C("c4w3-ffn", "trap",
      "Which holds more parameters — attention or the feed-forward layer? And why must the "
      "feed-forward layer exist at all?",
      "<p><b>Feed-forward, by two to one.</b> Attention is 4d²; feed-forward is 2 × d × 4d = 8d².</p>"
      + "<p>It must exist because attention is a weighted <b>average</b> — a linear operation. "
        "Stacking linear operations collapses to one, exactly the C2 W2 argument. The "
        "feed-forward layer supplies the non-linearity.</p>"
      + hint("It is also the only place NO information moves between positions. Attention is the "
             "only step where positions interact."),
      "c4/w3-04-feed-forward.html"),

    C("c4w3-block", "algorithm",
      "Write out one transformer block.",
      blk("x = x + attention(layer_norm(x))")
      + blk("x = x + feed_forward(layer_norm(x))")
      + bullets(["two sublayers, each wrapped identically",
                 "two residual connections, two layer norms",
                 "output shape = input shape, which is what lets blocks stack"])
      + hint("This is <b>pre-norm</b>, the modern arrangement. The 2017 paper used post-norm, which "
             "needs a carefully tuned warm-up to train stably at depth."),
      "c4/w3-05-the-block.html"),

    C("c4w3-gptbert", "distinguish",
      "GPT versus BERT — what single component differs?",
      two("<b>GPT — decoder-only</b><ul class='cbul'><li>causal mask</li>"
          "<li>predicts the next token</li><li><b>can generate</b></li>"
          "<li>writing, chat, completion</li></ul>",
          "<b>BERT — encoder-only</b><ul class='cbul'><li>no mask</li>"
          "<li>fills in hidden tokens</li><li>cannot generate left to right</li>"
          "<li>classification, search, extraction</li></ul>",
          "masked", "bidirectional")
      + hint("The block itself is identical. Decoder-only dominates public attention because "
             "generation is visible, not because it wins everywhere."),
      "c4/w3-07-gpt-vs-bert.html"),

    C("c4w3-count", "number",
      "GPT-2 small: 12 layers, d = 768, V = 50,257, context 1,024. Where do the parameters live?",
      bullets(["token embeddings: 50,257 × 768 = <b>38.6 M</b> (31.6%)",
               "attention, all layers: 4d² × 12 = 28.3 M (22.8%)",
               "<b>feed-forward, all layers: 8d² × 12 = 56.6 M (45.5%)</b>",
               "total ≈ <b>124.4 M</b>, against a published 124 M"])
      + hint("The feed-forward layers — the plainest component — are the largest share. The "
             "attention everyone talks about is under a quarter."),
      "c4/w3-08-counting-a-real-model.html"),
])

W4 = deck("C4", 4, "From Transformer to Language Model", [
    C("c4w4-objective", "formula",
      "The pretraining objective — and why it produces more than autocomplete.",
      blk("<var>L</var> = −Σ<sub><var>t</var></sub> log <var>P</var>(<var>x<sub>t</sub></var> | "
          "<var>x</var><sub>&lt;<var>t</var></sub>)")
      + "<p>Cross-entropy from C2 W2, over a 50,257-way softmax, at every position.</p>"
      + "<p>It produces knowledge because <b>predicting well requires it</b>: finishing “the capital "
        "of France is ___” with high probability means having stored the fact, so gradient descent "
        "stores it.</p>"
      + hint("Every position contributes a loss term simultaneously — a 1,000-token document is "
             "1,000 training signals in one forward pass."),
      "c4/w4-01-next-token.html"),

    C("c4w4-perplexity", "number",
      "A model assigns 0.10 to the correct token. What are the loss and the perplexity, and what "
      "does perplexity mean?",
      blk("loss = −log(0.10) = <b>2.303</b> &nbsp;&nbsp; perplexity = e<sup>2.303</sup> = <b>10.0</b>")
      + "<p>Perplexity reads as <b>how many options the model is effectively choosing between</b>. "
        "10 means it is about as uncertain as picking uniformly from 10 tokens.</p>"
      + hint("A uniform guess over 50,257 tokens has perplexity 50,257 and loss 10.825."),
      "c4/w4-01-next-token.html"),

    C("c4w4-temperature", "concept",
      "What does temperature do, and does it change the model?",
      blk("p = softmax(logits / <var>T</var>)")
      + bullets(["T &lt; 1 sharpens; T &gt; 1 flattens; T → 0 becomes argmax",
                 "applied to the <b>logits</b>, before the softmax — so it rescales probability "
                 "<em>ratios</em>",
                 "<b>not a single weight changes</b> — it sits entirely outside the model"])
      + "<p>Always taking the most likely token gives flat, repetitive text that loops, which is "
        "why real systems sample.</p>"
      + hint("Generating 1,000 tokens is 1,000 <b>sequential</b> forward passes — the parallelism "
             "that made training fast is gone."),
      "c4/w4-02-generation.html"),

    C("c4w4-rlhf", "algorithm",
      "The three training stages that turn a text predictor into an assistant.",
      steps(["<b>pretraining</b> — hundreds of billions of tokens; where essentially all capability "
             "comes from",
             "<b>supervised fine-tuning</b> — tens of thousands of demonstrations; teaches the "
             "<em>format</em> of a helpful answer",
             "<b>RLHF</b> — humans rank competing answers, a reward model learns those rankings, "
             "and the policy is optimised against it"])
      + "<p>Stage 1 gives capability; stages 2 and 3 give <b>behaviour</b>, and are cheap by "
        "comparison.</p>"
      + hint("This is C3 W3's reinforcement learning, and it is the largest deployed application of "
             "RL that exists. Caveat: RLHF optimises what people <em>rate highly</em>, which is not "
             "the same as true — hence sycophancy."),
      "c4/w4-04-rlhf.html"),

    C("c4w4-context", "distinguish",
      "A long context costs you two different things. What are they?",
      two("<b>Compute — O(T²)</b><ul class='cbul'><li>every pair of positions scored</li>"
          "<li>4k → 32k is 64× the work</li></ul>",
          "<b>Memory — O(T)</b><ul class='cbul'><li>the KV cache</li>"
          "<li>GPT-2 small: 38 MB at 1k, <b>4.7 GB</b> at 128k</li>"
          "<li>usually the binding constraint on serving</li></ul>",
          "attention", "the cache")
      + hint("The cache exists so generation does not recompute every previous token's keys and "
             "values each step — without it generation would be cubic in length."),
      "c4/w4-05-context-and-cost.html"),

    C("c4w4-limits", "trap",
      "Name three things a language model cannot reliably do — and the mechanism behind each.",
      bullets(["<b>hallucination</b> — the objective rewards <em>likely</em> continuations; nothing "
               "ever distinguished true from plausible",
               "<b>saying “I don't know”</b> — the softmax always yields a confident distribution "
               "and there is no abstain token; it has to be trained in during RLHF",
               "<b>counting letters</b> — the model receives subword chunks, never letters"])
      + hint("Scale reduces several of these and removes none. Hallucination follows from the "
             "objective, not from capacity."),
      "c4/w4-06-what-it-cannot-do.html"),

    C("c4w4-throughline", "concept",
      "What do all four courses share, and what did Course 4 actually change?",
      steps(["a <b>model</b> — what f is allowed to be",
             "a <b>cost</b> — one number for how wrong it is",
             "an <b>optimiser</b> — gradient descent, usually Adam"])
      + "<p>Course 4 changed <b>only the model</b>. The cost is still cross-entropy from C2 W2 and "
        "the optimiser is still Adam from C2 W2.</p>"
      + hint("Attention itself is the F0 W1 dot product plus the C2 W2 softmax. The genuinely new "
             "idea is letting every position read every other in one step."),
      "c4/w4-07-where-to-go-next.html"),
])

DECKS = [W1, W2, W3, W4]
