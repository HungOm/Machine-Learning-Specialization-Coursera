# -*- coding: utf-8 -*-
"""Walkthrough for 11_retrieval.py."""
from walkkit import p, expr, chain, chainset, steps, cases, values, point, ascii_art

PICTURE = ([
    ("in", "A pile of documents", "14 notes here. A real system has millions."),
    ("arw", "cut into pieces small enough to be useful"),
    ("op", "Chunk", "Overlapping windows, so a sentence split down the middle still "
                    "appears whole somewhere."),
    ("arw", "count words, then weight them by how rare they are"),
    ("op", "TF-IDF vectors", "One number per vocabulary word. Mostly zeros."),
    ("arw", "the query becomes a vector the same way"),
    ("op", "Cosine similarity", "Which document points most nearly the same way as the "
                                "question?"),
    ("arw", "and when the words simply do not match, this fails"),
    ("op", "Dense vectors, via SVD", "Squash the sparse space so related words end up "
                                     "near each other."),
    ("arw", "combine both scores"),
    ("out", "A handful of passages", "Trimmed to a token budget, or nothing at all if "
                                     "nothing is relevant."),
], "The whole program in one picture",
   "This is the R in RAG. Everything here is retrieval; the generation step is somebody "
   "else's problem, and it can only ever be as good as this.")

WALK = {

"prelude": (
    p("""Retrieval is the part of RAG that decides <b>what the model gets to see</b>. It is
also the part that fails first, and this file builds it up until it breaks and then fixes
it.""")
),

"corpus": (
    p("""Fourteen short notes, 179 words in total.""")
    + point("""Small enough that you can read every document and check every result by hand.
That is the whole reason for the size &mdash; on a real corpus you cannot tell a good
retrieval from a lucky one.""")
),

"chunk": (
    p("""Documents get cut into pieces. The size and the <b>overlap</b> are both real
decisions.""")
    + p("""With <code>size=10, overlap=0</code>, one sentence about the cost function gets
sliced straight down the middle &mdash; half of it in one chunk, half in the next, and
neither chunk answers the question on its own.""")
    + point("""That is why chunks <b>overlap</b> in practice. A window that slides rather
than jumps means any given sentence appears <b>whole</b> in at least one chunk, at the cost
of storing some text twice.""")
    + p("""Too small and you lose context; too large and one chunk covers five topics, so
its vector is an average of five things and matches none of them well. There is no correct
answer, only a trade you make deliberately.""")
),

"vocab": (
    p("""Turn text into numbers by counting words.""")
    + values([("vocabulary", "116 distinct words", "from 179 total words"),
              ("count matrix", "(14, 116)", "one row per document, one column per word"),
              ("zeros", "89.8%", "and this is a <b>tiny</b> corpus")],
             "the bag-of-words matrix")
    + point("""<b>89.8% zeros</b> here; a real corpus is <b>99.99%</b> zeros. Every document
contains almost none of the vocabulary. That is what &ldquo;sparse&rdquo; means in practice,
and nobody stores this as a dense array &mdash; you store only the positions that are not
zero.""")
    + p("""Note what this representation throws away: <b>word order</b>. &ldquo;the dog bit
the man&rdquo; and &ldquo;the man bit the dog&rdquo; are the same vector. It works anyway,
which is either encouraging or depressing depending on your mood.""")
),

"tfidf": (
    p("""Raw counts are dominated by words that appear everywhere and mean nothing. IDF
fixes that by weighting each word by <b>how rare</b> it is.""")
    + values([("lowest idf", "the, and, a, is, one, on", "everywhere &mdash; worth almost nothing"),
              ("highest idf", "converge, scaling, regression, error", "rare &mdash; worth a lot")],
             "IDF sorts the vocabulary by informativeness, automatically")
    + point("""Nobody wrote that list. <b>&ldquo;the&rdquo; is uninformative because it is in
everything</b>, and the maths discovers that by counting. IDF is
<code>log(N / documents containing the word)</code> and nothing more.""")
    + p("""But the block also prints a warning case: <b>&ldquo;how&rdquo;</b> appears in
<b>1 of 14</b> documents, so it gets a high IDF of <b>2.639</b> &mdash; as if it were a
technical term. It is a question word that happens to be rare <i>in this corpus</i>. IDF
measures rarity, not meaning, and on a small corpus those come apart.""")
),

"stopwords": (
    p("""So silence the obvious offenders by hand.""")
    + values([("silenced", "21 of 116", "vocabulary entries zeroed"),
              ("row length", "1.0000", "still exactly 1 after re-normalising")],
             "stopword removal")
    + point("""Renormalising afterwards matters. Removing words shortens every vector, and
cosine similarity is about <b>direction</b> &mdash; so you scale each row back to length 1
and the comparison stays fair.""")
),

"retrieve": (
    p("""Score every document against a query by <b>cosine similarity</b>: the angle between
the two vectors.""")
    + values([("0.275", "the elbow of the distortion curve&hellip;", "<b>wrong document</b>"),
              ("0.232", "gradient descent repeatedly nudges the weights&hellip;", "correct"),
              ("0.191", "a large learning rate makes gradient descent overshoot&hellip;", "correct")],
             "query: &ldquo;how does gradient descent choose its step&rdquo;")
    + point("""The <b>top hit is wrong</b>, and you can see why: that document contains
&ldquo;<b>choose</b>&rdquo; and &ldquo;<b>one</b>&rdquo;, which the query also has. It shares
words without sharing meaning.""")
    + p("""This is lexical search being exactly what it is: a word-overlap counter. It has no
idea that &ldquo;step&rdquo; and &ldquo;learning rate&rdquo; are related, or that
&ldquo;elbow&rdquo; belongs to a different topic entirely.""")
),

"mismatch": (
    p("""Now the failure that motivates everything after it. Same corpus, a query using
<b>synonyms</b>.""")
    + values([("0.327", "we minimise the loss by taking the derivative&hellip;", "correct"),
              ("0.316", "the loss for one training example is squared error&hellip;", "correct"),
              ("<b>0.000</b>", "the query key and value vectors&hellip;", "<b>exactly zero</b>"),
              ("<b>0.000</b>", "attention lets every token look at&hellip;", "<b>exactly zero</b>")],
             "query: &ldquo;how do I make the loss smaller&rdquo;")
    + point("""<b>Exactly zero</b>, not merely low. If a document shares <b>no words</b> with
the query, cosine similarity is 0 &mdash; and a perfectly relevant document written in
different vocabulary is <b>invisible</b>, not merely ranked badly.""")
    + p("""This is the <b>vocabulary mismatch</b> problem, and it is the reason dense
retrieval exists. No amount of better weighting fixes it, because the information was never
in the representation.""")
),

"dense": (
    p("""The fix: squash the sparse space down so that words which <b>appear in the same
documents</b> end up pointing in similar directions.""")
    + chain(["116 sparse dimensions", "6 dense ones"], "via SVD &mdash; the same SVD as file 08")
    + values([("+0.968", "we minimise the loss by taking the derivative&hellip;", "was 0.327"),
              ("+0.940", "the loss for one training example&hellip;", "was 0.316")],
             "the same synonym query, now")
    + point("""The scores are far higher <b>and</b> the previously invisible documents now
score above zero. Because &ldquo;minimise&rdquo; and &ldquo;smaller&rdquo; co-occur with the
same other words across the corpus, SVD places them near each other &mdash; so a query using
one partially matches a document using the other.""")
    + p("""This is the same machinery as PCA, pointed at text. Real systems use trained
embedding models instead of SVD, but the idea being exploited is identical: <b>related things
should be near each other in the space</b>.""")
),

"compare": (
    p("""Measure both methods honestly, on three kinds of query.""")
    + values([("lexical recall@1", "1.00 / 0.00 / 1.00", "plain / mismatch / exact"),
              ("lexical recall@3", "1.00 / 0.33 / 1.00", ""),
              ("dense recall@1", "1.00 / 0.00 / 0.78", ""),
              ("dense recall@3", "1.00 / <b>1.00</b> / 0.78", "")],
             "recall at 1 and 3, by query type")
    + point("""Read the columns. On <b>mismatch</b> queries, dense wins outright &mdash;
1.00 against 0.33 at rank 3. On <b>exact</b> queries, lexical wins &mdash; 1.00 against
0.78.""")
    + p("""That second column is the one people forget. Dense retrieval is <b>worse</b> when
the user typed the exact technical term, because squashing to 6 dimensions genuinely
<b>lost</b> the precision that made an exact match unambiguous.""")
    + point("""So neither method dominates. Which is the entire argument for the next
section.""")
),

"hybrid": (
    p("""Combine the two scores with a weight &alpha;, and sweep it.""")
    + values([("&alpha; = 0.0", "1.00 / 0.33 / 1.00", "mean <b>0.78</b> &mdash; pure lexical"),
              ("&alpha; = 0.2", "1.00 / 1.00 / 1.00", "mean <b>1.00</b>"),
              ("&alpha; = 0.4", "1.00 / 1.00 / 1.00", "mean <b>1.00</b>"),
              ("&alpha; = 0.5", "1.00 / 1.00 / 1.00", "mean <b>1.00</b>")],
             "plain / mismatch / exact, and the mean")
    + point("""<b>Twenty percent</b> of the dense score is enough to fix the mismatch column
completely <b>without giving up anything</b> on the exact column. Perfect on all three.""")
    + p("""And it is not a knife edge &mdash; anything from 0.2 to 0.5 works. That flatness is
what makes hybrid retrieval the practical default: you get both strengths, and you do not
have to tune it precisely to get them.""")
),

"assemble": (
    p("""Retrieved passages have to fit in a <b>token budget</b>, because the model's context
window is finite and you are paying per token.""")
    + values([("budget 200 words", "kept 5 of 5", "used 89 words &mdash; everything fits"),
              ("budget 40 words", "kept <b>1</b> of 5", "used 35 words")],
             "the same five notes, two budgets")
    + point("""At 40 words you keep <b>one</b> passage. Not a slightly worse answer &mdash;
four fifths of the evidence is simply not there, and the model will answer confidently from
what remains.""")
    + p("""This is why retrieval quality matters more than it looks. Rank the right passage
second instead of first and, on a tight budget, it never reaches the model at all.""")
),

"abstain": (
    p("""The last and most under-appreciated piece: knowing when to return <b>nothing</b>.""")
    + values([("what is entropy", "0.644", "answer it"),
              ("how does k means pick centroids", "0.684", "answer it"),
              ("what is the capital of Norway", "<b>0.000</b>", "<b>abstain</b>"),
              ("how do I renew a passport", "<b>0.000</b>", "<b>abstain</b>")],
             "best score per query")
    + point("""The corpus contains nothing about Norway or passports, and the scores say so
<b>unambiguously</b> &mdash; exactly 0, not merely low. A threshold separates these cleanly.""")
    + p("""Without an abstain rule, a RAG system hands the model its <b>least irrelevant</b>
passages and asks it to answer anyway. The model obliges, because that is what it does, and
you get a confident answer grounded in something about gradient descent.""")
    + point("""<b>&ldquo;I do not have information about that&rdquo; is a correct answer</b>,
and the retrieval score is the cheapest possible way to know when to give it.""")
),
}
