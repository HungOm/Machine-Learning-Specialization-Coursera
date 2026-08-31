# -*- coding: utf-8 -*-
"""Active Mastery for 11_retrieval.py. Values read off the running file.

These four files have no SRS cards and no mock quiz, so the thing not to
duplicate is the line-by-line walkthrough already on the page. The
walkthrough explains what each block does; this asks the reader to run the
retrieval themselves and find where it fails.
"""
from masterykit import (section, prose, code, out, semantics, ledger, drill, peek,
                        predict, lab, breaks, invariant, wrong, reconstruct,
                        connections, recall, check)

AM = dict(
    lede="Eleven cards on the R in RAG &mdash; and on the query where a perfectly relevant "
         "document scores <b>exactly zero</b>.",
    sections=[

section("0", "&#129517;", "Before you run", "before", kind="orient",
    hook="Fourteen notes, 116 words, and one query that breaks lexical search.",
    body=prose("""<p>Retrieval decides <b>what the model is allowed to see</b>. It is also the
part that fails first, and this file builds it up until it breaks and then fixes it.</p>
<p><b>Watch for three numbers.</b> The count matrix is <b>89.8% zeros</b> on a corpus of
fourteen sentences. A synonym query scores <b>exactly 0.000</b> against relevant documents
&mdash; not low, invisible. And <b>20%</b> dense weighting fixes that without costing anything
on exact matches.</p>""")
    + connections([], [], "../gist/c32.html", "C3 Week 2 &mdash; the gist",
        extra=[("lab", "../scratch/08-pca.html", "File 08 first",
                "the SVD here is that SVD, pointed at text")])),

section("1", "&#127991;&#65039;", "What every variable is", "vars", kind="semantics",
    hook="Eight variables, and two of them have units nobody expects: log-documents.",
    body=semantics([
        ("DOCS", "list of 14 str", "the corpus",
         "<b>One entry = one note</b> about machine learning. This is the entire searchable "
         "world.",
         "<i>text</i>",
         "<code>DOCS[0]</code> begins &ldquo;gradient descent repeatedly nudges the weights "
         "downhill&hellip;&rdquo;.",
         "Fourteen notes is small enough to <b>read every result and check it by hand</b>, "
         "which is the only reason the failures below are visible."),
        ("VOCAB", "dict of 116", "word &rarr; column index",
         "<b>Every distinct word in the corpus</b>, mapped to a column number. This is what "
         "turns text into arithmetic.",
         "<i>index</i>",
         "116 distinct words from 179 total. <code>VOCAB['gradient']</code> is that word's "
         "column.",
         "A word not in VOCAB is <b>invisible</b> at query time &mdash; it cannot score "
         "against anything, which is the root of the mismatch failure below."),
        ("COUNTS", "(14, 116) float64", "the bag of words",
         "<b>One row per document, one column per word.</b> How many times each word appears.",
         "<b>counts</b>",
         "<b>89.8% of it is zeros</b> &mdash; and this is a tiny corpus. A real one is 99.99% "
         "zeros, which is what &ldquo;sparse&rdquo; means in practice.",
         "It throws away <b>word order</b>: &ldquo;the dog bit the man&rdquo; and &ldquo;the "
         "man bit the dog&rdquo; are the same row. It works anyway, which is either "
         "encouraging or depressing."),
        ("IDF", "(116,) float64", "inverse document frequency",
         "<b>How rare each word is</b>, so common words stop dominating. Computed as "
         "log(N / documents containing it).",
         "<b>log-documents</b> &mdash; genuinely a log of a count ratio",
         "It ranges <b>0.1542 to 2.6391</b>. The low end is &ldquo;the&rdquo;, in almost every "
         "document; the high end is a word in exactly one.",
         "Nobody wrote the stopword list <i>for this</i> &mdash; IDF discovers that "
         "&ldquo;the&rdquo; is uninformative by counting. But it measures <b>rarity, not "
         "meaning</b>, and on a small corpus those come apart."),
        ("STOP", "set of 43", "the stopword list",
         "Words silenced by hand, because IDF alone gets some of them wrong.",
         "<i>words</i>",
         "43 listed, of which <b>21</b> actually appear in this vocabulary and get zeroed.",
         "The file needs this because &ldquo;how&rdquo; appears in <b>1 of 14</b> documents "
         "and so earns a high IDF of <b>2.639</b> &mdash; as if it were a technical term. It "
         "is a question word that happens to be rare <i>here</i>."),
        ("IDF_S", "(116,) float64", "IDF after silencing",
         "The same weights with the stopwords set to <b>0</b>, so they contribute nothing to "
         "any score.",
         "<b>log-documents</b>",
         "<b>21</b> of its 116 entries are now exactly zero.",
         "Zeroing the weight is gentler than deleting the column: the matrix shape stays "
         "fixed, so every downstream index still lines up."),
        ("TFIDF", "(14, 116) float64", "the document vectors",
         "Counts weighted by rarity, then each row scaled to <b>length 1</b>.",
         "<i>unitless</i> after normalising",
         "Every row has norm exactly <b>1.0</b>. That is what makes a dot product a "
         "<b>cosine</b> &mdash; an angle, bounded in [&minus;1, 1].",
         "Skip the renormalising after dropping stopwords and longer documents score higher "
         "simply for being longer."),
        ("alpha", "float", "the hybrid weight",
         "How much of the <b>dense</b> score to mix in. <b>Not a property of the corpus</b> "
         "&mdash; a knob you choose.",
         "<i>unitless</i>, 0 to 1",
         "At <b>0.0</b> it is pure lexical and mean recall is 0.78. At <b>0.2</b> through "
         "<b>0.5</b> it is <b>1.00</b>.",
         "The flatness is the useful part: anything in that range works, so you do not have "
         "to tune it precisely to get both strengths."),
    ],
    """The row worth pausing on is <b>IDF</b>. Its units are genuinely <b>log-documents</b>, it
was never authored by anyone, and it measures <b>rarity rather than meaning</b> &mdash; which
is exactly why the file still needs a hand-written stopword list."""),
    ),

section("2", "&#128302;", "Prediction checkpoints", "predict", kind="predict",
    hook="Four, and the second is about a score that is exactly zero.",
    body=predict([
        ("""The corpus is 14 short sentences. <b>Predict what fraction of the count matrix is
zeros</b> before you look.""",
         """<p><b>89.8%</b> &mdash; and this is fourteen sentences sharing a topic.</p>
<p>Each document contains 11&ndash;14 words out of a 116-word vocabulary, so almost every cell
must be empty. A real corpus is <b>99.99%</b> zeros, and nobody stores that as a dense array
&mdash; you store only the positions that are not zero.</p>"""),
        ("""Query: <i>&ldquo;how do I make the loss smaller&rdquo;</i>. Two documents about
attention are genuinely irrelevant. <b>Predict their cosine score.</b>""",
         """<p><b>Exactly 0.000</b> &mdash; and so is every document sharing no words with the
query.</p>
<p>That is the important part: it is not <i>low</i>, it is <b>zero</b>. Cosine similarity
between vectors with no overlapping non-zero entries is 0 by construction. A perfectly
relevant document written in different vocabulary is <b>invisible</b>, not merely ranked
badly.</p>
<p>No amount of better weighting fixes that, because the information was never in the
representation.</p>"""),
        ("""The word <b>&ldquo;how&rdquo;</b> appears in 1 of 14 documents. <b>Predict its IDF
and whether that is desirable.</b>""",
         """<p><b>2.639</b> &mdash; the highest in the corpus, tied with genuine technical
terms like &ldquo;converge&rdquo; and &ldquo;regression&rdquo;.</p>
<p>Which is wrong, and the file says so. IDF measures <b>rarity</b>, and on a small corpus a
common question word can be rare by accident. That mismatch is exactly why a hand-written
stopword list still exists in 2024.</p>"""),
        ("""Dense retrieval fixes the synonym query. <b>Predict whether it also wins on
queries using the exact technical term.</b>""",
         """<p><b>No &mdash; it loses.</b> Lexical scores <b>1.00</b> on exact-match queries;
dense scores <b>0.78</b>.</p>
<p>Squashing 116 dimensions to 6 genuinely <b>lost</b> the precision that made an exact match
unambiguous. That column is the one people forget when they claim embeddings replaced
keyword search.</p>
<p>Which is the entire argument for hybrid: neither method dominates.</p>"""),
    ],
    """The second one is the point of the file. &ldquo;Zero&rdquo; and &ldquo;low&rdquo; are
different failures and need different fixes.""")),

section("3", "&#128295;", "Modify the copy", "lab", kind="lab",
    hook="Five, including the one that shows chunking is a real decision.",
    body=lab([
        ("L1", "Change a value",
         "Set <code>alpha = 1.0</code> &mdash; pure dense, no lexical &mdash; and re-read the "
         "three-column recall table.",
         "for alpha in [1.0]:",
         """<p>The <b>exact</b> column falls to about <b>0.78</b> while mismatch stays at
1.00. You have traded away precisely what lexical search was good at.</p>
<p>Compare that with alpha = 0.0, which is 1.00 on exact and 0.33 on mismatch. Neither
endpoint is good, and the middle is flat &mdash; which is why hybrid retrieval is the
practical default rather than a compromise.</p>"""),
        ("L2", "Change a parameter",
         "Chunk with <code>size=10, overlap=0</code> and then with <code>overlap=5</code>. "
         "Compare what happens to the sentence about the cost function.",
         "for c in chunk(text, size=10, overlap=5):",
         """<p>With no overlap that sentence is <b>sliced down the middle</b> &mdash; half in
one chunk, half in the next, and neither chunk answers the question on its own.</p>
<p>With overlap the sliding window means any given sentence appears <b>whole</b> in at least
one chunk, at the cost of storing some text twice.</p>
<p>Chunk size and overlap are a real trade: too small loses context, too large makes one
chunk an average of five topics that matches none of them well.</p>"""),
        ("L3", "Change the data",
         "Add a document that is a near-duplicate of <code>DOCS[0]</code> and re-run a query "
         "that matched it. What happens to the results?",
         "DOCS = DOCS + ['gradient descent repeatedly nudges the weights downhill to reduce the cost']",
         """<p>Both near-duplicates now occupy the <b>top two slots</b>, pushing a genuinely
different relevant document off the list.</p>
<p>And it damages IDF: the words in those documents now appear in 2 of 15 rather than 1 of 14,
so their weights <b>drop</b> &mdash; a duplicate makes its own vocabulary look more common and
therefore less informative.</p>
<p>Under a token budget this is expensive: you have spent half your context on the same
sentence twice. Real pipelines de-duplicate before indexing for exactly this reason.</p>"""),
        ("L4", "Change an assumption",
         "Skip <code>drop_stopwords</code> entirely and re-run the first query.",
         "TFIDF = weight(COUNTS, IDF)        # was IDF_S",
         """<p>Results get <b>noticeably worse</b>, and the reason is visible: the query
&ldquo;<b>how</b> does gradient descent choose its step&rdquo; now scores partly on
&ldquo;how&rdquo;, which carries IDF <b>2.639</b>.</p>
<p>So a document containing &ldquo;how&rdquo; for unrelated reasons gets a large boost from a
word that means nothing here.</p>
<p>The invariant: <b>IDF handles frequency, not function.</b> It cannot know that a rare word
is a question word rather than a technical term.</p>"""),
        ("L5", "Explain it",
         "Explain why the rows of <code>TFIDF</code> are normalised to length 1, and what "
         "would go wrong without it.",
         None,
         """<p>Because a dot product between unit vectors <b>is</b> the cosine of the angle
&mdash; direction only, bounded in [&minus;1, 1]. Without normalising, a longer document has a
longer vector and therefore a larger dot product with <b>everything</b>.</p>
<p>You would be ranking by <b>document length</b> as much as by relevance, and the bug would
look like &ldquo;our search prefers long documents&rdquo;, which is easy to observe and hard
to attribute.</p>
<p>Same reason the two-tower model in C3 W2 calls <code>tf.linalg.l2_normalize</code> before its dot
product.</p>"""),
    ],
    """L3 is the one that shows up in real systems. Everything else here is a tuning choice;
duplicate documents are a data problem that silently distorts the weights.""")),

section("4", "&#128165;", "Break it, then repair it", "break", kind="debug",
    hook="Four, and the first ranks by length while looking perfectly reasonable.",
    body=breaks([
        ("def weight(counts, idf):\n    return counts * idf        # no row normalisation",
         "Drop the row normalisation and re-run a query. Predict which documents rise.",
         """<p>The <b>longest</b> documents rise to the top, regardless of relevance &mdash;
more words means a longer vector means a larger dot product with everything.</p>
<p>Nothing errors, every score is a plausible positive number, and the ranking is
systematically biased. The tell is that your top results are all long.</p>
<p>The invariant: <b>every document vector must have norm 1</b>, so the dot product measures
<b>direction</b> and not magnitude. One assertion catches it.</p>"""),
        ("IDF_S = drop_stopwords(IDF, VOCAB, STOP)\nTFIDF = weight(COUNTS, IDF)   # forgot to use IDF_S",
         "Compute the silenced weights and then use the unsilenced ones anyway. How would you "
         "notice?",
         """<p>You would <b>not</b>, from the shapes or the scores &mdash; both are (116,) and
both give plausible rankings.</p>
<p>The only visible symptom is that queries containing common question words return slightly
odd results, which reads as &ldquo;retrieval is a bit noisy&rdquo; rather than as a bug.</p>
<p>The invariant that catches it in one line: after silencing, <b>exactly 21 entries of the
weight vector in use must be zero</b>. Assert on the array you actually pass forward, not the
one you computed.</p>"""),
        ("q = query_vector(text)\nscores = TFIDF @ q      # q was never normalised",
         "Normalise the documents but not the query. Does the ranking change?",
         """<p>The <b>ranking does not change at all</b> &mdash; the query's length is a
constant factor applied to every score equally, so the order is identical.</p>
<p>But the <b>values</b> are no longer cosines and no longer bounded by 1, which breaks any
<b>threshold</b> you set &mdash; including the abstain rule at the end of the file.</p>
<p>The invariant: <b>if you compare scores against a fixed number, both sides must be
normalised.</b> If you only ever rank, you can get away with it &mdash; which is why this bug
survives until someone adds a threshold.</p>"""),
        ("keep = [d for d in ranked if score(d) > 0]     # no budget check",
         "Assemble the context without a token budget. What breaks, and where?",
         """<p>Nothing breaks <b>here</b> &mdash; it breaks in the model call downstream, either
by truncation or by cost.</p>
<p>The file's own numbers make the point: at a 200-word budget all 5 notes fit in 89 words; at
40 words you keep <b>1 of 5</b> and use 35. Four fifths of the evidence is simply absent, and
the model answers confidently from what remains.</p>
<p>The invariant: <b>retrieval quality and budget interact.</b> Ranking the right passage
second instead of first is free at 200 words and fatal at 40.</p>"""),
    ],
    """The third is the subtle one: a bug that is invisible while you rank and appears the
moment you threshold.""")),

section("5", "&#9878;&#65039;", "The invariant", "invariant", kind="invariant",
    hook="Every row has length 1, so every score is an angle.",
    body=invariant("""<p><b>Every document vector has norm exactly 1, so every score is a
cosine bounded in [&minus;1, 1] &mdash; and a score of exactly 0 means no shared
vocabulary.</b></p>""",
    """<p>The file asserts the first by printing that every row still has length <b>1.0000</b>
after stopword removal. That is what makes the dot product an <b>angle</b> rather than a
quantity contaminated by document length.</p>
<p>The second half is the one worth internalising: <b>0.000 is structurally different from
0.05</b>. A low score means &ldquo;these overlap a little&rdquo;; an exact zero means
&ldquo;these share no words at all&rdquo;, which is why the mismatch query cannot be repaired
by re-ranking.</p>
<p>And it is what makes the abstain rule possible: &ldquo;what is the capital of
Norway&rdquo; scores exactly <b>0.000</b> against every note, so a threshold separates
&ldquo;nothing relevant&rdquo; from &ldquo;weakly relevant&rdquo; cleanly.</p>""",
    """assert np.allclose(np.linalg.norm(TFIDF, axis=1), 1.0)
assert (IDF_S == 0).sum() == 21              # the silenced stopwords
assert scores.max() <= 1.0 + 1e-9            # cosines, not raw dot products
assert scores_for_unrelated_query.max() == 0.0""")),

section("6", "&#129535;", "Wrong mental models", "wrong", kind="myths",
    hook="Five, and the first is why people over-trust embeddings.",
    body=wrong([
        ("Dense retrieval is strictly better than keyword search.",
         """<p>It is <b>worse on exact matches</b>. The file's own table: lexical scores
<b>1.00</b> on exact-term queries, dense scores <b>0.78</b>.</p>
<p>Squashing 116 dimensions to 6 loses the precision that made an exact technical term
unambiguous. Dense wins on <b>mismatch</b> (1.00 against 0.33) and loses on exact &mdash;
which is why hybrid at alpha 0.2&ndash;0.5 scores 1.00 on both.</p>"""),
        ("A low retrieval score means the document is only slightly relevant.",
         """<p>Sometimes. But <b>exactly 0.000</b> means something different: <b>no shared
vocabulary at all</b>, which is a structural property of the representation rather than a
judgement about relevance.</p>
<p>A genuinely relevant document written in different words is invisible, not
low-ranked. Re-ranking cannot recover it because it was never in the candidate set.</p>"""),
        ("IDF understands which words matter.",
         """<p>It counts. &ldquo;<b>how</b>&rdquo; appears in 1 of 14 documents and therefore
earns IDF <b>2.639</b> &mdash; the same as &ldquo;converge&rdquo; and
&ldquo;regression&rdquo;.</p>
<p>It measures <b>rarity</b>, and rarity approximates informativeness only on a large corpus.
That is precisely why a hand-written stopword list is still needed, and why the file has
one.</p>"""),
        ("The chunk size is an implementation detail.",
         """<p>It decides <b>what can be retrieved at all</b>. At <code>size=10,
overlap=0</code> the sentence about the cost function is cut in half, and neither half answers
the question.</p>
<p>Too large is equally bad: one chunk covering five topics has a vector that is an average of
five things and matches none of them well. There is no correct answer, only a trade you make
deliberately.</p>"""),
        ("If retrieval returns something, the system should answer.",
         """<p>The file's abstain block is the counter-argument. &ldquo;What is the capital of
Norway&rdquo; scores <b>0.000</b> against every note &mdash; unambiguously nothing.</p>
<p>Without an abstain rule the system hands the model its <b>least irrelevant</b> passages and
asks it to answer anyway. It obliges, because that is what it does, and you get a confident
answer grounded in something about gradient descent.</p>
<p><b>&ldquo;I do not have information about that&rdquo; is a correct answer</b>, and the
retrieval score is the cheapest way to know when to give it.</p>"""),
    ])),

section("7", "&#127959;&#65039;", "Reconstruction challenge", "reconstruct", kind="rebuild",
    hook="Rebuild it, then prove it fails on a synonym.",
    body=reconstruct([
        ("Explain", "In four sentences, describe the pipeline without the words <i>vector</i> "
         "or <i>cosine</i>.",
         """<p>Cut the documents into pieces small enough to be useful. Count which words each
piece contains, and weight each word by how rare it is across the whole collection. Do the
same to the question. Then score every piece by how much its weighted word profile overlaps
the question's, and return the best few.</p>"""),
        ("Skeleton", "Write the seven signatures from memory.",
         """<p><code>chunk(text, size, overlap)</code>, <code>tokenise(text)</code>,
<code>build_vocab(docs)</code>, <code>count_matrix(docs, vocab)</code>,
<code>idf_of(counts)</code>, <code>drop_stopwords(idf, vocab, stop)</code>, and
<code>weight(counts, idf)</code>.</p>
<p>Note that <code>drop_stopwords</code> operates on the <b>IDF vector</b>, not the vocabulary
or the counts &mdash; it zeroes weights rather than deleting columns, so every downstream
index still lines up.</p>"""),
        ("Core", "Write idf_of and weight from memory, normalisation included.",
         """<p><code>idf_of</code>: count how many documents contain each word (<code>counts >
0</code> summed down the rows), then <code>log(N / df)</code>.</p>
<p><code>weight</code>: multiply counts by idf, then <b>divide each row by its own
norm</b>. Forget that division and you rank by document length.</p>"""),
        ("Minimal", "Build the smallest query and corpus where lexical retrieval scores exactly "
         "zero on a relevant document.",
         """<p>Two documents and one query is enough: a document saying &ldquo;minimise the
loss&rdquo;, a query asking &ldquo;make the error smaller&rdquo;, and no shared content
words.</p>
<p>Every content word differs, so the vectors have no overlapping non-zero entries and the
cosine is <b>0</b> exactly. That is the whole vocabulary-mismatch problem in two
sentences.</p>"""),
        ("Verify", "Check your rebuild without comparing to the original.",
         """<p>Three assertions: every row of your weighted matrix has norm 1; the most common
word has the <b>lowest</b> IDF; and a query sharing no words with a document scores exactly
<b>0.0</b>.</p>
<p>Then the real test: confirm your synonym query <b>fails</b>. If it succeeds, your tokeniser
is doing stemming you did not intend, and you have accidentally solved a different
problem.</p>"""),
    ],
    """The verify stage asks you to confirm a <b>failure</b>, which is unusual and is the
point: lexical retrieval is supposed to miss synonyms.""")),

section("8", "&#128279;", "Connections", "conn", kind="links",
    hook="08's SVD, 09's learned space — pointed at text.",
    body=connections(
        [("lab", "../scratch/08-pca.html", "Back to 08",
          "the dense step is that SVD, applied to a 116-column word matrix"),
         ("lab", "../scratch/09-collaborative-filtering.html", "Back to 09",
          "near neighbours in a learned space &mdash; there for films, here for text")],
        [("lab", "../scratch/13-agent-loop.html", "On to 13",
          "what happens after retrieval hands its passages to a model"),
         ("lab", "../scratch/12-fine-tuning.html", "Alongside 12",
          "the other way to give a model knowledge it did not have")],
        "../gist/c32.html", "C3 Week 2 &mdash; the gist",
        extra=[("docs", "../reference.html", "Reference &mdash; F0 W3",
                "<code>f0-svd</code> covers the factorisation the dense step uses")])),

section("9", "&#9670;", "Recall sheet", "recall", kind="recall",
    hook="Six cards, all this file's own numbers.",
    body=recall([
        ("Fourteen short notes. What fraction of the count matrix is zeros, and what is a real "
         "corpus?",
         "<b>89.8%</b> here; a real corpus is about <b>99.99%</b> zeros. Nobody stores that "
         "densely &mdash; you store only the non-zero positions."),
        ("A relevant document scores <b>0.000</b> on a synonym query. Why exactly zero?",
         "Cosine between vectors with <b>no overlapping non-zero entries</b> is 0 by "
         "construction. The document is <b>invisible</b>, not low-ranked, so re-ranking cannot "
         "recover it."),
        ("&ldquo;how&rdquo; gets IDF <b>2.639</b>, the highest in the corpus. Is that right?",
         "No. It appears in 1 of 14 documents, so it is <b>rare</b> &mdash; but it is a "
         "question word, not a technical term. IDF measures rarity, not meaning, which is why "
         "a hand-written stopword list still exists."),
        ("Lexical vs dense on exact-term queries: which wins, and by how much?",
         "<b>Lexical</b>, 1.00 against <b>0.78</b>. Squashing 116 dimensions to 6 loses the "
         "precision that made an exact match unambiguous. Dense wins on mismatch: 1.00 against "
         "0.33."),
        ("What does alpha = 0.2 buy, and why does the flatness matter?",
         "Mean recall <b>1.00</b> across all three query types, against 0.78 for pure lexical. "
         "Anything from 0.2 to 0.5 works, so you do not have to tune it precisely to get both "
         "strengths."),
        ("At a 40-word budget, how many of 5 retrieved notes survive?",
         "<b>One</b>, using 35 words. Four fifths of the evidence is absent and the model "
         "answers confidently from what remains &mdash; which is why ranking the right passage "
         "second is free at 200 words and fatal at 40."),
    ],
    """Cover and answer aloud.""")),

section("10", "&#9989;", "Mastery check", "check", kind="check",
    hook="Five, all diagnostic.",
    body=check([
        ("""Your RAG system returns confident nonsense for questions outside its corpus. Name
the missing component and the number it would use.""",
         """<p>An <b>abstain rule</b>. The retrieval score already says the answer: &ldquo;what
is the capital of Norway&rdquo; scores <b>0.000</b> against every note, unambiguously.</p>
<p>Without it the system passes its <b>least irrelevant</b> passages to the model, which
answers from them. A threshold on the top score is the cheapest possible fix.</p>"""),
        ("""Your search consistently prefers long documents. Name the bug.""",
         """<p>The document vectors are <b>not normalised</b>. More words means a longer
vector means a larger dot product with everything, so you are ranking partly by length.</p>
<p>One assertion catches it: every row of the weighted matrix must have norm <b>1.0</b>.</p>"""),
        ("""A colleague replaces keyword search with embeddings and reports that exact
product-code lookups got worse. Explain why, without calling it a bug.""",
         """<p>Because it is not one. Dense retrieval <b>compresses</b>, and compression
discards exactly the precision that makes a rare exact token unambiguous &mdash; this file
measures it as 1.00 dropping to <b>0.78</b>.</p>
<p>The fix is hybrid: <b>20%</b> dense weighting recovers the synonym cases without giving up
anything on exact matches.</p>"""),
        ("""You add a threshold to your scores and it behaves inconsistently, though the
ranking looks right. What did you forget?""",
         """<p>To <b>normalise the query</b>. Ranking is unaffected &mdash; the query's length
scales every score equally &mdash; but the values are no longer cosines and no longer bounded
by 1, so a fixed threshold means different things for different queries.</p>
<p>This bug is invisible while you only rank, and appears the moment you compare against a
number.</p>"""),
        ("""Your corpus contains many near-duplicate documents. Name two separate harms.""",
         """<p>First, they <b>crowd the result list</b>, so duplicates occupy slots that a
genuinely different relevant document needed &mdash; expensive under a token budget.</p>
<p>Second, they <b>distort IDF</b>: words in a duplicated document now appear in more
documents, so their weights drop and the topic looks less distinctive than it is. A duplicate
makes its own vocabulary look common.</p>"""),
    ],
    """These four files have no mock quiz, so the thing not to repeat is the line-by-line
walkthrough above &mdash; which explains what each block does rather than asking you to find
where it fails.""")),
    ],
)
