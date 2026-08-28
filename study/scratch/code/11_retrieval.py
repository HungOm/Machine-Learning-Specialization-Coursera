"""Retrieval from scratch -- the R in RAG, built with nothing but NumPy.

Run me:  python3 11_retrieval.py

A language model knows only what was in its training data and what you put in
the prompt. Retrieval decides what goes in the prompt. There is no model in
this file at all, because retrieval is a separate problem and it is ordinary
linear algebra you have already met: counting, weighting, cosine, SVD.
"""
import re

import numpy as np

# %% SECTION: corpus
# Fourteen short notes. Deliberately written so that some say "cost" and some
# say "loss" for the same idea, because that mismatch is the whole lesson.
DOCS = [
    "gradient descent repeatedly nudges the weights downhill to minimise the cost",
    "the cost function measures how wrong the model is averaged over the training set",
    "a large learning rate makes gradient descent overshoot and the cost goes up",
    "we minimise the loss by taking the derivative and stepping against it",
    "the loss for one training example is squared error for regression",
    "feature scaling makes gradient descent converge faster on data with wide ranges",
    "regularisation adds a penalty on the weights so the model generalises better",
    "a decision tree splits on the feature that gives the largest information gain",
    "entropy measures impurity and information gain is the drop in entropy after a split",
    "k means alternates assigning points to centroids and moving centroids to the mean",
    "the elbow of the distortion curve is one way people choose k for clustering",
    "an anomaly is a point with very low probability under the fitted gaussian",
    "attention lets every token look at every other token and weigh what matters",
    "the query key and value vectors are three different linear views of one token",
]

print("%d documents, %d words total" % (len(DOCS), sum(len(d.split()) for d in DOCS)))
print("shortest %d words, longest %d words"
      % (min(len(d.split()) for d in DOCS), max(len(d.split()) for d in DOCS)))

# %% SECTION: chunk
def chunk(text, size, overlap):
    """Cut a long text into overlapping windows of `size` words.

    Overlap exists because a fact can straddle a boundary. With no overlap a
    sentence cut in half is retrievable by neither of its halves, and you never
    find out -- the search simply returns something else.
    """
    words = text.split()
    step = size - overlap
    if step <= 0:
        raise ValueError("overlap must be smaller than size")
    out = []
    for start in range(0, max(len(words) - overlap, 1), step):
        piece = words[start:start + size]
        if piece:
            out.append(" ".join(piece))
        if start + size >= len(words):
            break
    return out

long_note = " ".join(DOCS[:3])
for size, ov in [(10, 0), (10, 4)]:
    pieces = chunk(long_note, size, ov)
    print("\nsize=%d overlap=%d -> %d chunks" % (size, ov, len(pieces)))
    for p in pieces:
        print("   |", p)
print("\nAt overlap 0 the phrase 'minimise the cost' is split between chunks 1")
print("and 2, so no single chunk contains it. At overlap 4 one chunk does.")
print("Overlap costs storage and buys recall. That is the entire trade.")

# %% SECTION: vocab
def tokenise(text):
    """Lowercase and keep runs of letters. Crude on purpose and easy to inspect."""
    return re.findall(r"[a-z]+", text.lower())

def build_vocab(docs):
    """word -> column index, in first-seen order so the output is stable."""
    vocab = {}
    for d in docs:
        for w in tokenise(d):
            if w not in vocab:
                vocab[w] = len(vocab)
    return vocab

def count_matrix(docs, vocab):
    """(n_docs, n_words). Entry (i, j) is how often word j occurs in doc i."""
    C = np.zeros((len(docs), len(vocab)))
    for i, d in enumerate(docs):
        for w in tokenise(d):
            if w in vocab:
                C[i, vocab[w]] += 1
    return C

VOCAB = build_vocab(DOCS)
COUNTS = count_matrix(DOCS, VOCAB)
INV = {j: w for w, j in VOCAB.items()}
print("vocabulary: %d distinct words" % len(VOCAB))
print("count matrix:", COUNTS.shape, "-> one row per document, one column per word")
print("%.1f%% of it is zeros, which is what 'sparse' means in practice"
      % (100.0 * (COUNTS == 0).mean()))
print("A real corpus is 99.99%% zeros. Nobody stores this as a dense array.")

# %% SECTION: tfidf
def idf_of(counts):
    """log(n_docs / n_docs_containing_word).

    A word in every document scores 0 and drops out; a word in one document
    scores highest. The intent is that 'the' cannot dominate a search.
    """
    n = counts.shape[0]
    df = (counts > 0).sum(axis=0)
    return np.log(n / np.maximum(df, 1)), df

def weight(counts, idf):
    """Scale by idf, then set every row to length 1.

    Normalising is why a long document is not automatically closer to
    everything than a short one: only direction survives, not magnitude.
    """
    W = counts * idf
    norms = np.linalg.norm(W, axis=1, keepdims=True)
    return W / np.maximum(norms, 1e-12)

IDF, DF = idf_of(COUNTS)
order = np.argsort(IDF)
print("lowest idf :", [INV[j] for j in order[:6]])
print("highest idf:", [INV[j] for j in order[-6:]])
print("\nBut look at these two:")
for w in ["how", "cost", "loss", "the"]:
    print("   %-6s appears in %2d of %d docs, idf %.3f"
          % (w, DF[VOCAB[w]], len(DOCS), IDF[VOCAB[w]]))
print("'how' scores higher than 'cost'. idf is a statistic OF THIS CORPUS, and")
print("in a small one a rare function word looks exactly like a rare technical")
print("word. idf alone does not identify meaning; it identifies rarity.")

# %% SECTION: stopwords
# This is why every real search system ships an explicit list. It is not
# inelegance, it is the fix for the problem measured directly above.
STOP = set("""a an and are as at be by for from how i in is it its of on or so
that the their them then there these this to under we what when where which
with do does did make made you your""".split())

def drop_stopwords(idf, vocab, stop):
    """Zero the columns of the stop words. Everything downstream is unchanged."""
    idf = idf.copy()
    for w in stop:
        if w in vocab:
            idf[vocab[w]] = 0.0
    return idf

IDF_S = drop_stopwords(IDF, VOCAB, STOP)
TFIDF = weight(COUNTS, IDF_S)
killed = sum(1 for w in VOCAB if IDF_S[VOCAB[w]] == 0)
print("silenced %d of %d vocabulary entries" % (killed, len(VOCAB)))
print("every document row still has length %.4f" % np.linalg.norm(TFIDF[0]))

def contributions(q, doc_i, vocab, idf, mat, top=4):
    """Which words actually produced this score? A search you cannot explain is
    a search you cannot debug."""
    qv = embed_query(q, vocab, idf)
    per = mat[doc_i] * qv
    idx = np.argsort(per)[::-1][:top]
    return [(INV[j], float(per[j])) for j in idx if per[j] > 0]

# %% SECTION: retrieve
def embed_query(q, vocab, idf):
    """Put the query through exactly the same pipeline as the documents.

    Processing query and document differently is the most common retrieval bug
    there is, and it fails quietly -- you get results, just worse ones.
    """
    c = count_matrix([q], vocab)[0]
    v = c * idf
    return v / max(np.linalg.norm(v), 1e-12)

def search(q, docs, mat, vocab, idf, k=3):
    """Cosine similarity is a plain dot product once both sides have length 1."""
    qv = embed_query(q, vocab, idf)
    scores = mat @ qv
    top = np.argsort(scores)[::-1][:k]
    return [(int(i), float(scores[i]), docs[i]) for i in top]

for q in ["how does gradient descent choose its step",
          "what is information gain"]:
    print("\nquery:", q)
    for i, s, d in search(q, DOCS, TFIDF, VOCAB, IDF_S):
        print("   %.3f  [%2d]  %s" % (s, i, d))
    top = search(q, DOCS, TFIDF, VOCAB, IDF_S, k=1)[0][0]
    print("   won on:", contributions(q, top, VOCAB, IDF_S, TFIDF))
print("\nScores are cosines: 1.0 is the same direction, 0.0 shares no word.")

# %% SECTION: mismatch
# Now a query that means the same thing but reaches for the other word.
q = "how do I make the loss smaller"
print("query:", q)
hits = search(q, DOCS, TFIDF, VOCAB, IDF_S, k=4)
for i, s, d in hits:
    print("   %.3f  [%2d]  %s" % (s, i, d))
COST_DOCS = {0, 1, 2}
found = sorted(COST_DOCS & {i for i, s, d in hits})
print("\nDocuments 0, 1 and 2 answer this question, using the word 'cost'.")
print("Retrieved from that set: %s" % (found if found else "none"))
print("They contain no query word at all, so they score exactly 0.000. Matching")
print("letters is not matching meaning, and no tuning of tf-idf repairs it,")
print("because tf-idf never sees that 'cost' and 'loss' are the same thing.")

# %% SECTION: dense
def lsa(mat, k):
    """Compress the sparse rows to k dense dimensions with the SVD -- the same
    machinery as file 08, pointed at a word matrix instead of a feature matrix.

    Vt's rows are directions in word space. Two words that keep the same
    company get similar coordinates, so a document can now score against a word
    it does not literally contain. That is the whole trick, and it is 1990
    technology; a modern embedding model does the same job far better.
    """
    U, S, Vt = np.linalg.svd(mat, full_matrices=False)
    doc_vecs = U[:, :k] * S[:k]
    doc_vecs /= np.maximum(np.linalg.norm(doc_vecs, axis=1, keepdims=True), 1e-12)
    return doc_vecs, Vt[:k]

def dense_search(q, docs, doc_vecs, comps, vocab, idf, k=3):
    qv = embed_query(q, vocab, idf) @ comps.T
    qv /= max(np.linalg.norm(qv), 1e-12)
    scores = doc_vecs @ qv
    top = np.argsort(scores)[::-1][:k]
    return [(int(i), float(scores[i]), docs[i]) for i in top]

DIM = 6
DENSE, COMPS = lsa(TFIDF, DIM)
print("compressed %d sparse dimensions down to %d dense ones" % (TFIDF.shape[1], DIM))
print("\nsame query:", q)
for i, s, d in dense_search(q, DOCS, DENSE, COMPS, VOCAB, IDF_S, k=4):
    print("   %+.3f  [%2d]  %s" % (s, i, d))
dfound = sorted(COST_DOCS & {i for i, s, d in
                             dense_search(q, DOCS, DENSE, COMPS, VOCAB, IDF_S, k=4)})
print("\nCost documents now retrieved: %s" % (dfound if dfound else "none"))

# %% SECTION: compare
# Two query sets, kept separate on purpose. The first shares words with its
# answers; the second deliberately does not. Averaging them together would
# hide the only difference that matters.
PLAIN = [("what is information gain", {7, 8}),
         ("how do centroids move", {9}),
         ("what do query and key vectors do", {12, 13}),
         ("choosing k for clustering", {10})]
MISMATCH = [("how do I make the loss smaller", {0, 1, 2}),
            ("what pushes the cost upward", {2}),
            ("a rule for splitting on impurity", {7})]
# And a third set: rare exact terms, the case lexical search is best at.
EXACT = [("gaussian", {11}), ("distortion", {10}), ("overshoot", {2}),
         ("impurity", {8}), ("anomaly", {11}), ("scaling", {5}),
         ("penalty", {6}), ("derivative", {3}), ("squared error", {4})]

def recall_at(fn, qs, k):
    return float(np.mean([len({i for i, s, d in fn(q, k)} & gold) > 0 for q, gold in qs]))

lex = lambda q, k: search(q, DOCS, TFIDF, VOCAB, IDF_S, k=k)
den = lambda q, k: dense_search(q, DOCS, DENSE, COMPS, VOCAB, IDF_S, k=k)
print("                      plain  mismatch  exact")
for name, f in [("lexical", lex), ("dense  ", den)]:
    for k in [1, 3]:
        print("  %s recall@%d :   %.2f     %.2f    %.2f"
              % (name, k, recall_at(f, PLAIN, k), recall_at(f, MISMATCH, k),
                 recall_at(f, EXACT, k)))
print("\nRead the last column. Dense retrieval WINS on synonyms and LOSES on")
print("rare exact words -- compressing to 6 dimensions is exactly what blurs")
print("'gaussian' into its neighbours. Neither method dominates.")
print("\nHow many dimensions to keep is a real knob, not a formality:")
for k in [2, 4, 6, 8, 12, 14]:
    dv, cp = lsa(TFIDF, k)
    f = lambda q, kk, dv=dv, cp=cp: dense_search(q, DOCS, dv, cp, VOCAB, IDF_S, k=kk)
    print("   k=%2d  plain@3 %.2f   mismatch@3 %.2f   exact@3 %.2f"
          % (k, recall_at(f, PLAIN, 3), recall_at(f, MISMATCH, 3),
             recall_at(f, EXACT, 3)))
print("Too few dimensions and unrelated notes collapse together -- and notice the")
print("exact column climbing back to 1.00 by k=8, because rare words stop being")
print("blurred once there is room to keep them apart. The top of the")
print("range does not misbehave here, and it cannot: this matrix has rank 14, so")
print("k=14 is the original data back. On a real corpus of millions of documents")
print("that ceiling is thousands of times further away, and the curve keeps")
print("mattering all the way up.")

# %% SECTION: hybrid
# Nobody in production picks one. They add the two scores, because the failures
# are not the same failures.
def hybrid(q, alpha, k=3):
    ql = embed_query(q, VOCAB, IDF_S)
    qd = ql @ COMPS.T
    qd /= max(np.linalg.norm(qd), 1e-12)
    scores = (1 - alpha) * (TFIDF @ ql) + alpha * (DENSE @ qd)
    top = np.argsort(scores)[::-1][:k]
    return [(int(i), float(scores[i]), DOCS[i]) for i in top]

print("           plain  mismatch  exact   mean")
best = (None, -1.0)
for a in [0.0, 0.2, 0.4, 0.5, 0.6, 0.8, 1.0]:
    f = lambda q, k, a=a: hybrid(q, a, k)
    r = [recall_at(f, PLAIN, 3), recall_at(f, MISMATCH, 3), recall_at(f, EXACT, 3)]
    mean = float(np.mean(r))
    if mean > best[1]:
        best = (a, mean)
    print("  alpha=%.1f  %.2f    %.2f     %.2f   %.2f" % (a, r[0], r[1], r[2], mean))
ties = [a for a in [0.0, 0.2, 0.4, 0.5, 0.6, 0.8, 1.0]
        if abs(np.mean([recall_at(lambda q, k, a=a: hybrid(q, a, k), qs, 3)
                        for qs in (PLAIN, MISMATCH, EXACT)]) - best[1]) < 1e-9]
print("\nalpha 0.0 is pure lexical, 1.0 is pure dense. Everything from %.1f to %.1f"
      % (min(ties), max(ties)))
print("scores the same here -- a broad plateau, not a sharp optimum.")
print("Both ends give up something. The blend keeps the exact matches that dense")
print("blurs and the synonyms that lexical cannot see, and it costs one extra")
print("dot product. Where the best alpha sits depends entirely on your corpus")
print("and your queries, so measure it -- this number is not transferable.")

# %% SECTION: assemble
def build_prompt(question, hits, budget_words):
    """Retrieval ends here: a string. Everything above exists to fill this in.

    The budget is real. Attention costs grow with the square of the context
    (C4 W2 'the cost'), so something has to be dropped -- and ranking is what
    chooses. A bad ranker with a big budget just fails more expensively.
    """
    header = "Answer using only the notes below. If they do not contain the answer, say so."
    used, kept = len(header.split()) + len(question.split()), []
    for i, s, d in hits:
        if used + len(d.split()) > budget_words:
            break
        kept.append((i, s, d))
        used += len(d.split())
    notes = "\n".join("[%d] %s" % (i, d) for i, s, d in kept)
    return "%s\n\n%s\n\nQuestion: %s" % (header, notes, question), used, len(kept)

question = "why does a big learning rate hurt"
hits = search(question, DOCS, TFIDF, VOCAB, IDF_S, k=5)
for budget in [200, 40]:
    prompt, used, n = build_prompt(question, hits, budget)
    print("\nbudget %d words -> kept %d of %d notes, used %d words"
          % (budget, n, len(hits), used))
    if budget == 40:
        print("---")
        print(prompt)
        print("---")

# %% SECTION: abstain
def answerable(q, mat, vocab, idf, floor):
    """Refuse when nothing scores above a floor.

    Without this a retriever always returns its top k however irrelevant, and a
    model handed irrelevant notes will still answer, fluently. A good share of
    what gets called hallucination is retrieval that should have said nothing.
    """
    best = float(np.max(mat @ embed_query(q, vocab, idf)))
    return best >= floor, best

probes = ["what is entropy", "how does k means pick centroids",
          "what is the capital of Norway", "how do I renew a passport"]
print("           query                          best score")
for q in probes:
    _, best = answerable(q, TFIDF, VOCAB, IDF_S, 0.0)
    print("   %-38s %.3f" % (q, best))
in_scope = [answerable(q, TFIDF, VOCAB, IDF_S, 0)[1] for q in probes[:2]]
out_scope = [answerable(q, TFIDF, VOCAB, IDF_S, 0)[1] for q in probes[2:]]
floor = (min(in_scope) + max(out_scope)) / 2
print("\nlowest in-scope score %.3f, highest out-of-scope score %.3f"
      % (min(in_scope), max(out_scope)))
print("a floor of %.3f separates them on these four" % floor)
for q in probes:
    ok, best = answerable(q, TFIDF, VOCAB, IDF_S, floor)
    print("   %-38s -> %s" % (q, "answer" if ok else "say you do not know"))
print("\nFour probes is not a calibration. The method is right and the sample is")
print("far too small: collect the queries you actually get, score them, and put")
print("the floor where the two groups stop overlapping -- if they ever do.")
