# -*- coding: utf-8 -*-
"""C4 · Week 1 — Sequences, embeddings, and why the old answers failed."""
from kit import (kid, key, warn, trap, note, card, eq, eqp, decode, table, demo,
                 quiz, links, code, h2, grid2, grid3, pretest, explain, lenses)

L = []

# ============================================================ 1
L.append(dict(
    slug="01-why-order-matters", title="Why order matters", mins=12, tag="intuition",
    lede="Everything in Courses 1–3 treated an example as an unordered bag of features. Language is "
         "not a bag, and the whole of this course follows from that one fact.",
    body=(
        pretest("""<p>“The dog bit the man” and “the man bit the dog” use exactly the same words, the same number of times. <b>Guess what a model that only counts words would say about them</b> — and what it would have to be given instead.</p>""",
        """<p>Watch for the word <b>position</b>. Every mechanism in this course exists to put position back into a model that would otherwise not have it.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Every model you have built so far ate a <b>set</b> of numbers. Size, bedrooms, age —
shuffle those three columns and nothing changes as long as the weights shuffle too. Order carried no
meaning.</p>
<p>Now feed it a sentence. “The dog bit the man” and “the man bit the dog” contain identical words in
identical quantities. If your model only sees which words are present, those two sentences are
<b>literally the same input</b> — and one of them is a much worse day than the other.</p>""")

        + lenses(
            """<p>A recipe. Flour, water, yeast, salt, heat — the same five things in one order make
bread, and in another order make a burnt paste with raw dough in the middle.</p>
<p>No ingredient changed. What changed is <em>when</em> each one arrived. A cook who ignores order is
not making a variant of the dish; they are not making the dish at all.</p>""",

            """<p>If you have worked with time series, you have met this: shuffling the rows of a
sales table destroys the thing you were trying to model. Autocorrelation, lag, trend and seasonality
are all statements about order.</p>
<p>Everything in Courses 1–3 assumed rows were <b>exchangeable</b> — independent draws whose order
carried no information. That assumption is what breaks here, and it breaks completely rather than
partially.</p>""",

            """<p>A padlock with four dials.</p>
<p>The combination 1‑9‑8‑4 and the combination 4‑8‑9‑1 use the same four digits. One opens the lock.
A model that counted digits would call them identical, and would be wrong in the only way that
matters.</p>""",

            """<p>Early machine translation systems were built on word counts and produced exactly the
failure you would predict: correct vocabulary, incoherent meaning. Negation was the notorious case —
“the treatment is not effective” and “the treatment is effective, not” score identically on a bag of
words.</p>
<p>In a medical or legal document, that is not a quality issue. It is a safety issue, and it is why
sequence models were worth inventing.</p>""",

            """So everything that follows in this course is machinery for one purpose: letting a model
know not just <em>what</em> it was given, but <em>in what order</em>.""")

        + h2("🎬", "Watch it move")
        + demo("c4-orderbag", "The same words, two meanings",
               "the bag-of-words counter cannot tell these two sentences apart")

        + h2("🔢", "The maths, decoded")
        + """<p>An example is no longer one vector. It is a <b>sequence</b> of vectors, and its length
varies from example to example — which is itself new.</p>"""
        + eq("""<var>x</var> <span class="op">=</span> <span class="paren">(</span>
<var>x</var><sup>&lt;1&gt;</sup><span class="op">,</span> <var>x</var><sup>&lt;2&gt;</sup>
<span class="op">,</span> … <span class="op">,</span> <var>x</var><sup>&lt;T&gt;</sup>
<span class="paren">)</span>""", "one example — T items, in order")
        + decode([
            ("<var>x</var><sup>&lt;t&gt;</sup>", "“x at time t”", "The t-th item in <b>this one</b> example. Angle brackets are the course's marker for position within a sequence — a third bracket style, alongside (i) for example number and [l] for layer."),
            ("<var>T</var>", "“capital T”", "How long this particular sequence is. Unlike n (features) it is <b>not</b> the same for every example — one sentence is 5 words, the next is 40."),
            ("<var>x</var><sup>(<var>i</var>)&lt;<var>t</var>&gt;</sup>", "“example i, position t”", "Both markers at once: the t-th word of the i-th training example. You will meet this stacked notation constantly."),
        ])
        + note("""<p>Variable length is the quiet difficulty here. Every matrix shape you learned in
Course 2 assumed a fixed number of columns. A batch of sentences has no such number, which is why
real code pads short sequences and carries a <b>mask</b> saying which positions are real.</p>""",
               "The thing nobody warns you about")

        + h2("🕳", "Traps")
        + trap("""<p><b>Thinking a bag of words is merely less accurate.</b> It is not a weaker version
of a sequence model — for word-order questions it is structurally incapable, in the same way a
thermometer is incapable of telling the time.</p>""")
        + trap("""<p><b>Confusing the three superscript styles.</b> (i) is which example, [l] is which
layer, &lt;t&gt; is which position. This course uses all three, sometimes in one formula.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("Give two English sentences with identical word counts and opposite meanings.",
             "<p>Many possible. “The dog bit the man” / “the man bit the dog”. Or with negation: "
             "“profits rose, not fell” / “profits fell, not rose”. A bag-of-words model assigns both "
             "members of each pair the <b>identical</b> input vector.</p>"),
            ("Why is T not just another name for n, the number of features?",
             "<p>Because n is fixed for the whole dataset — every house has four columns. T varies "
             "per example, and that variation is what forces padding, masking, and eventually the "
             "attention mechanism.</p>"),
            ("A model predicts sentiment from a movie review. Give a case where word order flips the answer.",
             "<p>“I expected it to be terrible, and it was brilliant” versus “I expected it to be "
             "brilliant, and it was terrible”. Identical words; opposite sentiment.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("paper", "https://arxiv.org/abs/1706.03762",
             "Attention Is All You Need (2017)",
             "The paper this whole course is walking towards. Skim the abstract now; it will be readable by Week 3."),
            ("lesson", "c1/w2-01-multiple-features.html",
             "C1 W2 · Multiple features",
             "Where features were introduced as an unordered list — the assumption this lesson breaks."),
        ])
    )))

# ============================================================ 2
L.append(dict(
    slug="02-tokens", title="Tokens — what a model actually reads", mins=11, tag="core",
    lede="Before any maths happens, text has to become numbers. The choice of how to cut it up is "
         "quiet, consequential, and explains several things people find mysterious about LLMs.",
    body=(
        pretest("""<p>A model has to turn text into a fixed list of known items. <b>Guess the problem with using whole words</b> — think about someone typing a word the model has never seen.</p>""",
        """<p>Watch for the compromise between two bad extremes, and for why it makes models bad at spelling.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>A model cannot read letters. It can only look things up in a fixed list it was
built with — its <b>vocabulary</b>. So the first job is chopping text into pieces that are all on that
list.</p>
<p>Chop into whole words and you fail the first time someone writes “antidisestablishmentarianism”
or a typo. Chop into single letters and every sentence becomes hundreds of pieces with almost no
meaning each. So real models chop into <b>parts of words</b> — a compromise, and the reason a model
sees “unbelievable” as roughly three chunks rather than one word or twelve letters.</p>""")

        + lenses(
            """<p>A printer's tray of movable type.</p>
<p>You cannot have a block for every word that will ever be printed — the tray would be infinite. You
also do not want to set every page letter by letter. So you keep single letters <em>and</em> common
chunks: “ing”, “tion”, “the”. Frequent things get their own block; rare things get assembled.</p>
<p>That is precisely the trade a tokenizer makes, and it was solved in printing four centuries
before it was solved in software.</p>""",

            """<p>This is a compression problem, and the standard algorithm — <b>byte-pair
encoding</b> — was literally a compression algorithm first (Gage, 1994) before it was borrowed for
language models.</p>
<p>It starts from single characters and repeatedly merges whichever adjacent pair is most frequent,
until the vocabulary reaches the size you asked for. Common words end up as one token; rare ones stay
in pieces.</p>""",

            """<p>A word broken along dotted lines, like a chocolate bar.</p>
<p>“unbelievable” snaps into three pieces along lines the tokenizer decided in advance, based on what
was common in its training text. The model never sees the whole bar and never sees the individual
crumbs — only the pieces.</p>""",

            """<p>This explains two things people find odd about LLMs. <b>Spelling</b>: a model asked
to count the r's in a word is working from chunks, not letters, so the letters are genuinely not
directly visible to it. <b>Billing</b>: API pricing is per token, and English is roughly 0.75 words
per token while some other languages cost several tokens per word — a real and much-criticised cost
asymmetry.</p>""",

            """So when a formula below says “input length T”, T counts tokens — not words, and not
characters.""")

        + h2("🎬", "Watch it move")
        + demo("c4-tokens", "One sentence, three ways to cut it",
               "characters, words, and subword pieces — with the vocabulary cost of each")

        + h2("🧮", "The three options, counted")
        + table(["Scheme", "Vocabulary size", "Pieces in “unbelievable”", "The problem"],
                [["characters", "~100", "12", "sequences become very long, each piece nearly meaningless"],
                 ["whole words", "millions, and still incomplete", "1", "any unseen word is unrepresentable"],
                 ["<b>subword (BPE)</b>", "~30,000–100,000", "~3", "<b>the working compromise</b> — nothing is ever unrepresentable, because single characters remain in the vocabulary"]])
        + key("""<p>The vocabulary is fixed <b>before training</b> and never changes afterwards. A model
cannot learn a new token later — it can only learn new arrangements of the tokens it was born
with.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Assuming one token equals one word.</b> A useful rough figure for English is
about 0.75 words per token, but it varies by language and by how unusual your text is. Code and
proper nouns fragment heavily.</p>""")
        + trap("""<p><b>Comparing token counts across models.</b> Different models use different
tokenizers, so the same paragraph genuinely has different lengths for different models.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("Why does keeping single characters in the vocabulary matter, even though almost nothing is tokenized that way?",
             "<p>It guarantees <b>nothing is ever unrepresentable</b>. Any string at all, including "
             "typos, invented words and other alphabets, can be spelled out as a fallback. Without "
             "that, a model would have to emit an “unknown” token and lose the content entirely.</p>"),
            ("Why might a model struggle to reverse a word letter-by-letter?",
             "<p>Because it does not receive letters. It receives a few chunks, and the letter "
             "structure inside a chunk is something it must have learned indirectly rather than "
             "something it can read off.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("docs", "https://platform.openai.com/tokenizer",
             "An interactive tokenizer",
             "Paste text and watch it split. Try a long word, a typo, and a non-English sentence."),
        ])
    )))

# ============================================================ 3
L.append(dict(
    slug="03-one-hot-and-why-it-fails", title="One-hot vectors, and why they fail here", mins=11, tag="core",
    lede="You met one-hot encoding for decision trees. Applied to a 50,000-word vocabulary it breaks "
         "in two separate ways — and understanding both is what makes embeddings feel inevitable.",
    body=(
        pretest("""<p>One-hot encoding worked fine for three ear shapes in Course 2. <b>Guess what goes wrong when the categories are 50,000 words</b> — and there are two distinct problems, not one.</p>""",
        """<p>Watch for a size problem AND a meaning problem. The second is the one that actually matters.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>One-hot means: give every word its own slot, put a 1 in its slot and 0 everywhere
else. With three categories that is sensible. With 50,000 words each one becomes a list of 50,000
numbers, 49,999 of which are zero.</p>
<p>That is wasteful — but the real problem is worse. In that scheme <b>“cat” is exactly as similar to
“dog” as it is to “bulldozer”.</b> Every pair of different words is equally different. All the
meaning has been thrown away by the encoding itself, before the model sees anything.</p>""")

        + lenses(
            """<p>A hotel where every guest gets a room and no two rooms are adjacent.</p>
<p>Guest 12 and guest 13 are in rooms with consecutive numbers, but the numbers say nothing about the
guests — you cannot tell from the room number that two guests are family. The building has recorded
identity and destroyed every relationship.</p>""",

            """<p>Formally, one-hot vectors are mutually <b>orthogonal</b>: the dot product between any
two distinct words is exactly zero, and every pair is equidistant.</p>
<p>Since similarity in this course is measured by dot products, a representation where every dot
product is zero has pre-emptively deleted the only signal downstream maths can use. It is not a poor
encoding of meaning; it encodes no meaning at all.</p>""",

            """<p>A row of 50,000 light switches with exactly one on.</p>
<p>To say “cat” you flip switch 8,214. To say “dog” you flip 11,903. Nothing about the switchboard
records that those two switches belong together and switch 44,001 (“bulldozer”) does not.</p>""",

            """<p>The size problem is real too. A first layer taking 50,000 one-hot inputs into 512
units needs <b>25.6 million</b> parameters, almost all of them multiplying zeros.</p>
<p>Every early NLP system paid this cost, and it is why vocabulary size was a hard practical ceiling
for years — you were spending most of your model on an encoding that had already thrown the meaning
away.</p>""",

            """So the fix has to solve the meaning problem, not just the size problem — and the next
lesson is that fix.""")

        + h2("🎬", "Watch it move")
        + demo("c4-onehot", "Every word equally far from every other",
               "the dot product between any two distinct one-hot vectors is exactly zero")

        + h2("🔢", "The maths, decoded")
        + eq("""<var>cat</var> <span class="op">·</span> <var>dog</var> <span class="op">=</span> 0
&nbsp;&nbsp;&nbsp; <var>cat</var> <span class="op">·</span> <var>bulldozer</var> <span class="op">=</span> 0""",
             "every distinct pair, identically unrelated")
        + """<p>Both dot products are zero because the single 1 in each vector sits in a different
slot, so every product term is 1×0 or 0×1 or 0×0. There is no arrangement of a one-hot scheme in
which two different words are more alike than two others.</p>"""
        + table(["", "one-hot", "what we want"],
                [["length per word", "50,000", "a few hundred"],
                 ["cat · dog", "0", "high — related"],
                 ["cat · bulldozer", "0", "low — unrelated"],
                 ["params into a 512-unit layer", "25,600,000", "the same table, but it now <em>means</em> something"]])

        + h2("🕳", "Traps")
        + trap("""<p><b>Thinking the fix is “just use the word's index as a number”.</b> That is worse:
it invents an ordering that does not exist, claiming word 8,214 sits between 8,213 and 8,215 in some
meaningful way. Arbitrary structure is more damaging than none.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("One-hot works well for three ear shapes but not for 50,000 words. What actually changed?",
             "<p>Two things. Scale — 50,000 slots instead of 3. And, decisively, the fact that ear "
             "shapes genuinely <b>are</b> mutually unrelated categories, whereas words are not: "
             "throwing away the relationships between them throws away the entire signal.</p>"),
            ("Why is the dot product the right test to apply here?",
             "<p>Because it is how every model in this specialization measures agreement between two "
             "vectors. If the encoding makes all those dot products zero, no downstream layer can "
             "recover a similarity the encoding already destroyed.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("lesson", "c2/w4-06-one-hot-encoding.html",
             "C2 W4 · One-hot encoding",
             "Where one-hot was introduced, and where it genuinely was the right answer."),
        ])
    )))

# ============================================================ 4
L.append(dict(
    slug="04-embeddings", title="Embeddings — a learned lookup table", mins=13, tag="core",
    lede="The single idea that makes everything downstream possible, and it is far less exotic than "
         "its reputation: a table of numbers per word, learned by gradient descent like any other "
         "parameter.",
    body=(
        pretest("""<p>We need each word to become a short vector where similar words end up nearby. <b>Guess where those numbers could possibly come from</b> — nobody is going to hand-assign 50,000 of them.</p>""",
        """<p>Watch for the answer being something you already know how to do. There is no new algorithm in this lesson.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Give every word a short list of numbers — say 512 of them — and store all those
lists in one big table. To “embed” a word is simply to <b>look up its row</b>.</p>
<p>Where do the numbers come from? They start random and are <b>learned</b>, by exactly the gradient
descent you already know. The table is just another matrix of parameters. Because words used in
similar ways get pushed towards similar rows during training, meaning ends up encoded in geometry —
not because anyone designed it that way, but because that arrangement minimises the loss.</p>""")

        + lenses(
            """<p>A spice rack arranged by taste rather than alphabetically.</p>
<p>Cumin, coriander and paprika end up on one shelf; cinnamon, nutmeg and cloves on another. Nobody
wrote the rule — the cook shelved them by what gets used together, and over years the shelf became a
map of flavour. Reach blindly near the cumin and you get something plausible.</p>
<p>An embedding table is that rack, arranged by 512 kinds of “goes together” at once.</p>""",

            """<p>If you did Course 3's recommender week, you have already built this. Collaborative
filtering learned a feature vector per <em>movie</em> with nobody labelling genres — the features
emerged because they minimised prediction error.</p>
<p>An embedding table is the identical construction with words in place of films. Same idea, same
optimisation, and it is why that week is genuinely good preparation for this one.</p>""",

            """<p>A wall of pigeonholes, one per word, each holding 512 dials.</p>
<p>At the start every dial is set randomly. Training turns the dials. By the end, the pigeonholes for
“king” and “queen” have similar settings, and the one for “bulldozer” does not — and no human ever
touched a dial.</p>""",

            """<p>Embeddings power semantic search: instead of matching keywords, you embed the query
and the documents and find the nearest vectors. That is why a search for “how do I fix a puncture”
can return a page titled “repairing a flat tyre” with no shared words.</p>
<p>This is also the retrieval half of RAG — the standard way of grounding a language model in your
own documents — so this one table is the foundation of a large fraction of deployed LLM systems.</p>""",

            """So the lookup below is not a new kind of layer. It is a matrix of learned parameters,
indexed instead of multiplied.""")

        + h2("🎬", "Watch it move")
        + demo("c4-embed", "A lookup table, learning",
               "watch related words drift together as the loss falls")

        + h2("🔢", "The maths, decoded")
        + eq("""<var>E</var> <span class="op">∈</span> ℝ<sup><var>V</var> × <var>d</var></sup>
&nbsp;&nbsp;&nbsp; <var>e</var><sub><var>w</var></sub> <span class="op">=</span>
<var>E</var><span class="paren">[</span><var>w</var><span class="paren">]</span>""",
             "the table, and one lookup from it")
        + decode([
            ("<var>E</var>", "“the embedding matrix”", "One row per vocabulary item. Every entry is a learned parameter, updated by gradient descent like any weight."),
            ("<var>V</var>", "“the vocabulary size”", "How many distinct tokens exist. Typically 30,000–100,000."),
            ("<var>d</var>", "“the embedding dimension”", "How many numbers describe each token. 512 and 768 are common; larger models use more."),
            ("<var>e</var><sub><var>w</var></sub>", "“the embedding of w”", "One row — the vector that <em>is</em> this token, as far as the rest of the model is concerned."),
        ])
        + note("""<p>A lookup is mathematically identical to multiplying the one-hot vector by
<var>E</var> — the 1 selects exactly one row and the zeros delete the rest. So this is not a new
operation; it is the <em>same</em> matrix multiply, implemented as an index because multiplying by
49,999 zeros is a waste of a computer.</p>""", "Why this is not a new kind of layer")

        + h2("🧮", "Similarity, worked")
        + """<p>Take three deliberately tiny 3-dimensional embeddings and measure similarity with the
<b>cosine</b> — the dot product divided by both lengths, so only direction counts and magnitude does
not:</p>"""
        + table(["pair", "dot product", "lengths", "cosine similarity"],
                [["king [2,1,0] · queen [3,1,0]", "7", "2.236 × 3.162", "<b>0.990</b> — nearly the same direction"],
                 ["king [2,1,0] · banana [0,1,2]", "1", "2.236 × 2.236", "<b>0.200</b> — largely unrelated"]])
        + """<p>Check the first one by hand: 2(3) + 1(1) + 0(0) = 7, and 7 ÷ (2.236 × 3.162) = 0.990.
That single number is what every semantic search in the world is ranking on.</p>"""
        + explain("""<p>Cosine similarity divides away both vectors' lengths, keeping only the angle
between them. <b>Why is throwing away magnitude the right choice for comparing meaning?</b></p>""",
                  """<p>Because magnitude in an embedding table tracks things you do not want to
compare on — chiefly how often a token appeared in training. A common word and a rare synonym should
count as similar in <em>meaning</em> even if one vector is much longer than the other. Dividing both
lengths out asks the question you actually want: are these pointing the same way?</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Believing individual dimensions mean things.</b> Dimension 47 is not “royalty”.
The dimensions are an arbitrary basis chosen by optimisation; meaning lives in <em>directions and
distances</em>, not in single coordinates.</p>""")
        + trap("""<p><b>Expecting the famous king − man + woman ≈ queen result to be reliable.</b> It
works for some carefully chosen examples and fails on plenty of others. It is a real property, badly
oversold.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("A vocabulary of 50,000 tokens with d = 512. How many parameters is the embedding table?",
             "<p>50,000 × 512 = <b>25,600,000</b>. Comparable in size to an entire small network — and "
             "it is only the input layer.</p>"),
            ("Why can an embedding be described as “a matrix multiply implemented as an index”?",
             "<p>Multiplying a one-hot row vector by E selects exactly one row of E. The lookup does "
             "the same thing without computing the 49,999 multiplications by zero.</p>"),
            ("Where have you built this before?",
             "<p>Course 3 Week 2. Collaborative filtering learned a feature vector per movie with no "
             "genre labels, by gradient descent on prediction error. Same construction.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("lesson", "c3/w2-03-collaborative-filtering.html",
             "C3 W2 · Collaborative filtering",
             "Where you first learned features rather than being given them."),
            ("paper", "https://arxiv.org/abs/1301.3781",
             "word2vec (2013)",
             "The paper that made word embeddings famous. Short, readable, and now historical."),
        ])
    )))

# ============================================================ 5
L.append(dict(
    slug="05-rnn-idea", title="What RNNs tried", mins=12, tag="intuition",
    lede="The pre-2017 answer to sequences: read one item at a time and carry a running summary. "
         "Elegant, genuinely successful for a decade, and fatally limited in two ways.",
    body=(
        pretest("""<p>You must handle a sentence of any length with a fixed-size model. <b>Guess the obvious approach</b> — think about how you yourself read a long sentence.</p>""",
        """<p>Watch for what has to be carried from word to word, and how much can fit in it.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Read the sentence one word at a time, and keep a <b>running summary</b> in your
head. At each word, update the summary using the word you just read and the summary you already had.
At the end, the summary is your understanding of the sentence.</p>
<p>That is a recurrent neural network. The same small network is applied at every position — same
weights, reused — so a sentence of any length can be processed by a fixed-size model. For a decade
this was how machine translation, speech recognition and autocomplete worked.</p>""")

        + lenses(
            """<p>Someone taking a phone message with no paper.</p>
<p>They listen, holding a summary in their head, updating it word by word. Short message: perfect.
Long, detailed message: by the end they have the gist and the last sentence, and the phone number
from the beginning is gone.</p>
<p>Not because they were careless — because a running summary has a fixed capacity, and everything
new competes for it.</p>""",

            """<p>This is a state machine, or a discrete-time dynamical system: a hidden state
<var>h</var> updated by a transition function at each step.</p>
<p>If you have used a Kalman filter or any recursive estimator, the shape is identical — carry a
belief, update it with each new observation. The difference is that the transition function here is
learned rather than derived from physics.</p>""",

            """<p>A bucket chain passing water along a line of people.</p>
<p>Each person receives from the left, adds their own contribution, and passes right. The bucket at
position 40 contains something from position 1 — but heavily diluted by the 39 additions since, and
there is no way to reach back and ask position 1 directly.</p>""",

            """<p>RNNs and their LSTM refinement genuinely worked. Google Translate switched to a
neural sequence model in 2016 and the improvement was large enough to be newsworthy — it was the
first time machine translation stopped being a punchline.</p>
<p>So this is not a failed idea to skip past. It is the idea that proved sequence learning was
possible at all, and its <em>specific</em> limitations are what the next architecture was designed
against.</p>""",

            """So the recurrence below is worth understanding properly, because the whole of attention
is an answer to what it cannot do.""")

        + h2("🎬", "Watch it move")
        + demo("c4-rnn", "One summary, updated word by word",
               "watch the hidden state carry — and watch early information fade")

        + h2("🔢", "The maths, decoded")
        + eq("""<var>h</var><sup>&lt;t&gt;</sup> <span class="op">=</span> <var>g</var>
<span class="paren">(</span><var>W</var><sub><var>h</var></sub><var>h</var><sup>&lt;t−1&gt;</sup>
<span class="op">+</span> <var>W</var><sub><var>x</var></sub><var>x</var><sup>&lt;t&gt;</sup>
<span class="op">+</span> <var>b</var><span class="paren">)</span>""",
             "the new summary, from the old summary and the new word")
        + decode([
            ("<var>h</var><sup>&lt;t&gt;</sup>", "“h at time t”", "The running summary after reading t items. Also called the <b>hidden state</b>."),
            ("<var>h</var><sup>&lt;t−1&gt;</sup>", "“h at t minus one”", "The summary <em>before</em> this word. This is the recurrence — the output feeding back as input."),
            ("<var>W</var><sub><var>h</var></sub>, <var>W</var><sub><var>x</var></sub>", "“W-h and W-x”", "Two weight matrices, <b>the same at every position</b>. That reuse is what lets one model handle any length."),
        ])
        + key("""<p>The weights are shared across positions. A 5-word and a 500-word sentence use the
identical parameters — the network is applied 5 or 500 times. That is the elegant part, and it is
also why the next lesson's problem is unavoidable.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Picturing a very deep network with different layers.</b> It is <em>one</em>
small network applied repeatedly. Unrolled it looks deep, but every copy shares the same weights —
which matters enormously for how the gradients behave.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("Why can one RNN handle sentences of any length?",
             "<p>Because the weights are shared across positions. The model does not have a parameter "
             "per position — it has one small function applied as many times as needed.</p>"),
            ("What has to fit inside h?",
             "<p>Everything from the sequence so far that will matter later. Its size is fixed, so it "
             "is a bottleneck by construction — and that is the subject of the next two lessons.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("lesson", "c2/w1-06-forward-propagation.html",
             "C2 W1 · Forward propagation",
             "The same layer arithmetic, applied once per position instead of once per layer."),
        ])
    )))

# ============================================================ 6
L.append(dict(
    slug="06-why-rnns-failed", title="Why RNNs failed — the two limits", mins=13, tag="core",
    lede="Two independent problems, both fatal at scale, and both solved by the same later idea. "
         "This lesson is the argument for everything in Week 2.",
    body=(
        pretest("""<p>An RNN carries one fixed-size summary and processes words strictly one after another. <b>Guess two separate problems that causes</b> — one about memory, one about speed.</p>""",
        """<p>Watch for the fact that these are independent failures. Fixing one would not fix the other.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p><b>Problem one: it forgets.</b> Information from word 1 has to survive being
rewritten 40 times to reach word 41. In practice it does not — the signal fades. So a model cannot
connect “the keys” at the start of a paragraph with “them” at the end.</p>
<p><b>Problem two: it cannot be parallelised.</b> To compute the summary at word 41 you need word 40's
summary first. Every position waits for the one before it, so a 1,000-word document takes 1,000
sequential steps no matter how many processors you own.</p>""")

        + lenses(
            """<p>A message passed down a line of a hundred people, whispered.</p>
<p>By person eighty the beginning is unrecognisable — that is the forgetting. And the hundredth
person cannot start until the ninety-ninth has spoken, so a hundred people take a hundred turns
however big the room is. That is the speed limit.</p>
<p>Both failures come from the same design, and neither is fixed by trying harder.</p>""",

            """<p>The forgetting has a precise name and mechanism: the <b>vanishing gradient</b>, and
it is the identical arithmetic you met with deep sigmoid networks in C2 W2 — slopes below 1
multiplied together many times.</p>
<p>The speed problem is a dependency chain: the computation is inherently serial, so it cannot exploit
the parallel hardware that makes everything else in deep learning fast. Amdahl's law, applied to an
architecture.</p>""",

            """<p>A very long relay race with one baton.</p>
<p>The baton is the hidden state. Nothing can overtake it, nothing can be handed directly from runner
1 to runner 100, and if the baton is dropped or degraded en route there is no recovering what it
carried.</p>""",

            """<p>These two limits set the ceiling on what was buildable before 2017. Sequence models
were capped at modest context lengths and could not use large GPU clusters efficiently, because the
architecture refused to parallelise.</p>
<p>Removing the serial dependency is what made training on thousands of GPUs worthwhile, and that —
more than any single accuracy result — is why the transformer changed the economics of the field.</p>""",

            """So the two numbers below are the case for the whole of Week 2.""")

        + h2("🎬", "Watch it move")
        + demo("c4-vanish", "A signal fading across timesteps",
               "the same slope-multiplication problem as deep sigmoid networks, now across time")

        + h2("🧮", "How fast does it forget?")
        + """<p>Backpropagating through time multiplies a slope at every step. Sigmoid's slope tops out
at 0.25 and tanh's is realistically around 0.4. Multiply that over distance:</p>"""
        + table(["steps back", "at 0.25 per step", "at 0.4 per step"],
                [["5", "9.8 × 10⁻⁴", "0.010"],
                 ["10", "9.5 × 10⁻⁷", "1.0 × 10⁻⁴"],
                 ["20", "9.1 × 10⁻¹³", "1.1 × 10⁻⁸"],
                 ["50", "7.9 × 10⁻³¹", "1.3 × 10⁻²⁰"]])
        + """<p>Twenty words back, the gradient reaching that position is somewhere between a
hundred-millionth and a trillionth of the signal at the end. It is not that learning long-range
dependencies is hard — the update simply never arrives.</p>"""
        + note("""<p>LSTMs and GRUs, invented in 1997 and 2014, attack exactly this. They add gates
that let information pass through <em>unchanged</em> rather than being multiplied each step —
stretching usable memory from roughly 10 steps to perhaps 100. A real improvement, and still a
ceiling.</p>""", "What LSTMs actually fixed")

        + h2("🕳", "Traps")
        + trap("""<p><b>Thinking bigger hidden states fix the forgetting.</b> They help the capacity
problem slightly and do nothing about the vanishing gradient, which is caused by repeated
multiplication, not by size.</p>""")
        + trap("""<p><b>Assuming the speed problem is an implementation detail.</b> It is architectural.
No amount of engineering parallelises a computation whose step <var>t</var> genuinely requires step
<var>t</var>−1.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("Which of the two problems does an LSTM address, and which does it leave untouched?",
             "<p>It substantially mitigates <b>forgetting</b>, via gates that let information pass "
             "without repeated multiplication. It does nothing at all about the <b>serial</b> "
             "dependency — an LSTM is exactly as unparallelisable as a plain RNN.</p>"),
            ("Why is this the same problem as deep sigmoid networks in C2 W2?",
             "<p>Because both multiply many slopes below 1 together. There it was one factor per "
             "<em>layer</em>; here it is one per <em>timestep</em> — and sequences are much longer "
             "than networks are deep.</p>"),
            ("What would an architecture need in order to fix both at once?",
             "<p>A way for any position to reach any other position <b>directly</b> — one step, not "
             "forty — and a computation where positions do not have to wait for each other. That is "
             "precisely what attention provides.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("lesson", "c2/w2-03-sigmoid-alternatives.html",
             "C2 W2 · Alternatives to sigmoid",
             "The same vanishing-gradient arithmetic, across layers rather than across time."),
        ])
    )))

# ============================================================ 7
L.append(dict(
    slug="07-the-bottleneck", title="The bottleneck, and the first attention", mins=12, tag="core",
    lede="Before the transformer there was one more step: keeping every position's summary instead of "
         "just the last one, and letting the model choose which to look at. That is attention, and it "
         "arrived three years before the architecture named after it.",
    body=(
        pretest("""<p>A translation model reads a 40-word sentence into one summary vector, then writes the translation from it. <b>Guess the specific bottleneck</b> — and a fix that does not require discarding the RNN.</p>""",
        """<p>Watch for the move from <em>one</em> summary to <em>all</em> of them.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>The translation systems of 2014 read the whole source sentence into a single fixed
vector, then generated the translation from that vector alone. Everything the sentence meant had to
squeeze through one narrow pipe.</p>
<p>The fix was almost embarrassingly direct: <b>keep the summary from every position</b>, not just the
last one. Then, when generating each output word, let the model decide which input positions to look
at — and let it be a different mixture for every output word.</p>
<p>That decision, made by the model, is <b>attention</b>.</p>""")

        + lenses(
            """<p>A translator working from a document versus from memory.</p>
<p>Memorise a page, then recite the translation — that is the bottleneck, and it fails on long pages.
Keep the page in front of you and glance back at whichever line you are currently translating — that
is attention. Nobody would call the second approach clever; it is obviously what you would do.</p>""",

            """<p>This is soft, differentiable indexing. Rather than a hard lookup of one item, you take
a <b>weighted average of all items</b>, with weights that sum to 1 — which is exactly a softmax.</p>
<p>The reason it must be soft is that a hard argmax has no gradient. Making the selection continuous
is what allows the choosing itself to be trained by backpropagation.</p>""",

            """<p>A row of index cards, all face up, with a spotlight of adjustable width.</p>
<p>For one output word the spotlight is tight on card 3. For the next it is spread over cards 8, 9 and
10. Nothing is ever removed from the table; what changes is where the light falls, and the model
learns to aim it.</p>""",

            """<p>The 2014 paper that introduced this (Bahdanau et al.) measured the effect precisely:
without attention, translation quality <b>collapsed as sentences got longer</b>; with it, quality
stayed roughly flat with length.</p>
<p>That single chart is one of the more consequential results in the field. It says the bottleneck was
not a subtle inefficiency — it was the dominant failure mode, and removing it removed the length
limit.</p>""",

            """So the weighted average below is the whole mechanism, and Week 2 is what happens when
someone asks whether the RNN around it is needed at all.""")

        + h2("🎬", "Watch it move")
        + demo("c4-bottleneck", "One vector, versus all of them",
               "the same sentence encoded through a bottleneck and through attention")

        + h2("🔢", "The maths, decoded")
        + eqp([
            ('<var>c</var>', "attn-context", "the context vector"),
            ' <span class="op">=</span> ',
            ('<span class="big">Σ</span><sub><var>t</var></sub>', "sigma", "over every input position"),
            ('<var>α</var><sub><var>t</var></sub>', "attn-weight", "how much to look at position t"),
            ('<var>h</var><sup>&lt;t&gt;</sup>', "attn-value", "that position's summary"),
        ], "a weighted average of every position — hover or click any part")
        + decode([
            ("<var>α</var><sub><var>t</var></sub>", "“alpha t”", "The attention weight on position t. All of them are positive and they sum to 1 — because they come from a softmax."),
            ("<var>c</var>", "“the context vector”", "What the decoder actually reads. Recomputed <b>fresh for every output word</b>, which is the point."),
            ("<span class='big'>Σ</span>", "“sum over t”", "The same summation you have used since Foundations, now over sequence positions."),
        ])
        + key("""<p>Attention is a <b>weighted average</b>, and the weights come from a softmax. You
have known both halves since Course 2. Nothing mathematically new is introduced — only a new thing to
point them at.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Thinking attention replaced RNNs in 2014.</b> It did not — it was bolted onto
them and made them much better. The removal of the RNN came three years later, and that is Week
2's story.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("Why must the attention weights sum to 1?",
             "<p>Because the result is an <b>average</b> of the position summaries. If the weights did "
             "not sum to 1 the output's magnitude would drift with sequence length rather than "
             "reflecting content.</p>"),
            ("Why is a softmax used rather than simply picking the single best position?",
             "<p>Picking the maximum is not differentiable — there is no gradient to train the "
             "choosing. Softmax makes the selection soft and therefore learnable.</p>"),
            ("What does “recomputed for every output word” buy you?",
             "<p>Different output words need different parts of the input. A fixed context vector "
             "forces one compromise for the entire output; a per-word context lets the model look "
             "where it currently needs to.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("paper", "https://arxiv.org/abs/1409.0473",
             "Bahdanau et al. (2014) — attention, before transformers",
             "The paper that introduced attention as a fix for the bottleneck. Figure 2 is the length chart worth seeing."),
        ])
    )))

# ============================================================ 8
L.append(dict(
    slug="08-week-1-review", title="Where this leaves us", mins=9, tag="core",
    lede="Four facts to carry into Week 2, and the single question the transformer was invented to "
         "answer.",
    body=(
        pretest("""<p>You now know that RNNs forget and cannot parallelise, and that attention lets any output position read any input position directly. <b>Guess the obvious question somebody asked in 2017.</b></p>""",
        """<p>Watch for how radical the answer was — and how much simpler it made things.</p>""")
        + h2("🎈", "The idea, in plain words")
        + kid("""<p>Put the pieces together. Attention lets any position look at any other position in
<b>one step</b>, with no fading. The RNN around it is the part that forgets and the part that forces
everything to happen in order.</p>
<p>So: what if you removed the RNN and kept only the attention?</p>
<p>That question is the title of the 2017 paper — <em>Attention Is All You Need</em> — and the answer
turned out to be yes.</p>""")

        + h2("📋", "The four things to carry forward")
        + table(["", "the fact", "why it matters in Week 2"],
                [["1", "A sequence is ordered, and order is meaning", "attention alone is order-blind, so position has to be added back deliberately"],
                 ["2", "Tokens become vectors by <b>lookup</b> in a learned table", "the transformer's input is exactly this, unchanged"],
                 ["3", "RNNs forget, because slopes multiply across time", "attention's path from any position to any other is <b>one step</b>, so nothing multiplies"],
                 ["4", "RNNs are serial, so they cannot use parallel hardware", "attention computes all positions at once — this is the economic argument"]])

        + h2("🎬", "Watch it move")
        + demo("c4-w1recap", "Sequence in, embeddings, and the two failures",
               "the whole week in one diagram")

        + h2("🧮", "The question, stated precisely")
        + """<p>An RNN's path from position 1 to position 100 is <b>99 sequential steps</b>, each
multiplying the signal by something below 1. Attention's path from position 1 to position 100 is
<b>one</b> weighted average.</p>"""
        + table(["", "RNN", "attention"],
                [["steps between two positions", "their distance apart", "<b>1</b>, always"],
                 ["gradient over 20 positions", "~10⁻⁸ to 10⁻¹³", "undiminished"],
                 ["positions computable at once", "1", "<b>all of them</b>"],
                 ["parameters per position", "shared", "shared"]])
        + key("""<p>Everything in Week 2 follows from the middle two rows. One-step paths solve
forgetting; simultaneous computation solves speed. The cost — and there is one — is that attention
compares every position with every other, so the work grows with the <b>square</b> of the sequence
length. That trade is the subject of the whole architecture.</p>""")

        + h2("🕳", "Traps")
        + trap("""<p><b>Assuming the transformer is strictly better.</b> It is better at these two
things and pays for it quadratically in sequence length. That cost is why context windows are a
headline number and why so much research goes into making attention cheaper.</p>""")

        + h2("✅", "Check yourself")
        + quiz([
            ("State the two RNN problems and how attention addresses each.",
             "<p><b>Forgetting</b>: an RNN's signal is multiplied by a sub-1 slope at every step "
             "between two positions; attention connects them in a single step so nothing "
             "accumulates. <b>Serialisation</b>: an RNN's step t needs step t−1; attention computes "
             "every position simultaneously.</p>"),
            ("What does attention cost that an RNN does not?",
             "<p>Comparing every position to every other is O(T²) work and memory. An RNN is O(T). "
             "That is the whole reason long context windows are hard and expensive.</p>"),
            ("Why is an embedding table still needed in a transformer?",
             "<p>Because tokens still have to become vectors before anything else can happen. "
             "Nothing about attention changes the input representation — the lookup table survives "
             "unchanged.</p>"),
        ])

        + h2("🔗", "Go deeper")
        + links([
            ("paper", "https://arxiv.org/abs/1706.03762",
             "Attention Is All You Need (2017)",
             "Read the abstract and Figure 1 now. Both should be considerably less opaque than a week ago."),
        ])
    )))

WEEK = dict(course="C4", week=1, title="Sequences, Embeddings and the Old Answers", lessons=L)
