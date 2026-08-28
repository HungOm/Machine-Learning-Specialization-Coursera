# -*- coding: utf-8 -*-
"""C4 W4 — language models, generation and cost."""
from problemkit import P, m, pre, cols

L = []
def add(*a, **k): L.append(P(*a, **k))

add("c4w4-p01", level=1, tag="loss and perplexity",
    lesson="c4/w4-01-next-token.html",
    ask="A model assigns probability %s to the token that actually came next. Compute the loss "
        "and the perplexity, and say what the perplexity means in words." % m("0.20"),
    gist="Take the negative log of the probability, then raise e to that answer.",
    steps=[("Loss", "−log(0.20) = 1.6094"),
           ("Perplexity", "e^1.6094 = 5.0"),
           ("Note", "perplexity = 1 ÷ probability, when it is a single token")],
    answer="Loss %s, perplexity %s — the model is about as uncertain as if it were picking "
           "uniformly among <b>five</b> tokens." % (m("1.609"), m("5.0")),
    check="A uniform guess over a 50,257-token vocabulary would give perplexity 50,257 and loss "
          "10.825.",
    why="Perplexity is quoted in papers precisely because “effectively choosing between 5 options” "
        "is far more interpretable than “loss 1.6”.")

add("c4w4-p02", level=2, tag="temperature",
    lesson="c4/w4-02-generation.html",
    ask="Three tokens have scores %s. Compute the sampling probabilities at %s and at %s, and "
        "describe the difference." % (m("[2, 1, 0]"), m("T = 0.5"), m("T = 2.0")),
    hint="Divide the scores by T first, then softmax.",
    steps=[("T = 0.5: divide", "[4, 2, 0]"),
           ("Exponentiate", "54.60, 7.39, 1.00 → sum 62.99"),
           ("Softmax", "[0.867, 0.117, 0.016]"),
           ("T = 2.0: divide", "[1, 0.5, 0]"),
           ("Exponentiate", "2.718, 1.649, 1.00 → sum 5.367"),
           ("Softmax", "[0.507, 0.307, 0.186]")],
    answer="At T = 0.5: %s — sharply focused. At T = 2.0: %s — much flatter, so unlikely tokens "
           "get picked far more often." % (m("[0.867, 0.117, 0.016]"), m("[0.507, 0.307, 0.186]")),
    check="The <b>ordering</b> never changes — only how sharply the leader is favoured. That is "
          "why T → 0 becomes argmax.",
    why="Not a single model weight differs between these two columns. Temperature is a serving "
        "setting, which is why the same model can feel like two different systems.")

add("c4w4-p03", level=2, tag="context cost",
    lesson="c4/w4-05-context-and-cost.html",
    ask="A model has 6 layers and %s. Compute its KV cache at a context of 2,048 tokens, in fp16 "
        "(2 bytes per number). Then say how the cache and the attention work each scale with "
        "length." % m("d = 256"),
    hint="The cache stores both a key and a value per layer per token.",
    steps=[("Numbers cached per token per layer", "2 (one key, one value) × 256 = 512"),
           ("Across 6 layers", "6 × 512 = 3,072 numbers per token"),
           ("Across 2,048 tokens", "3,072 × 2,048 = 6,291,456 numbers"),
           ("At 2 bytes each", "12,582,912 bytes")],
    answer="About %s per sequence. The cache grows <b>linearly</b> with length; attention work "
           "grows with the <b>square</b>." % m("12.6 MB"),
    check="Double the context to 4,096 and the cache doubles to 25 MB while the attention work "
          "quadruples.",
    why="Two different scaling laws in one system. Memory is usually what limits how many "
        "simultaneous users a machine can serve, which is why so much serving research targets "
        "this cache specifically.")

add("c4w4-p04", level=2, tag="failure modes",
    lesson="c4/w4-06-what-it-cannot-do.html",
    ask="For each failure, name the mechanism that causes it: (a) confidently stating a false "
        "fact, (b) miscounting the letters in a word, (c) losing track of something said earlier "
        "in a long conversation.",
    steps=[("(a) hallucination", "the training objective rewards LIKELY continuations; nothing in "
            "it ever distinguished true from plausible"),
           ("(b) letter counting", "tokenization — the model receives subword chunks and never "
            "sees individual letters"),
           ("(c) forgetting", "the context window — anything outside it does not exist at all")],
    answer="(a) the next-token objective rewards plausibility, not truth; (b) tokenization hides "
           "letters; (c) the fixed context window, beyond which there is simply no memory.",
    why="Every one of these follows from the design rather than from insufficient training — which "
        "is why they are predictable, and why scale reduces some of them and removes none.")

add("c4w4-p05", level=3, tag="RLHF",
    lesson="c4/w4-04-rlhf.html",
    ask="A freshly pretrained model is asked “What is the capital of France?” and replies “What is "
        "the capital of Germany? What is the capital of Spain?”. Explain why this is a reasonable "
        "output, and what the two additional training stages each fix.",
    steps=[("What the model was trained to do", "continue text plausibly"),
           ("In its training data", "a question is frequently followed by more questions — a list, "
            "a quiz, an exercise sheet"),
           ("So the continuation is genuinely likely", "the model is succeeding at its objective"),
           ("Stage 2 — supervised fine-tuning", "demonstrations teach the FORMAT of an answer"),
           ("Stage 3 — RLHF", "human rankings teach which answers people actually prefer")],
    answer="It is a perfectly good next-token prediction — questions often precede more questions "
           "in real text. Stage 2 teaches the <b>format</b> of answering; stage 3 teaches "
           "<b>which answers people prefer</b>, including when to decline.",
    check="Stage 1 supplies essentially all the capability. Stages 2 and 3 are cheap by comparison "
          "and change the entire experience of using the model.",
    why="Stage 3 is reinforcement learning — the reward is a learned model of human preference and "
        "the policy is the language model. Course 3 Week 3 was not a detour.")

add("c4w4-p06", level=3, tag="synthesis",
    lesson="c4/w4-07-where-to-go-next.html",
    ask="Someone claims a language model “understands” the document you gave it. Write the "
        "precise, mechanical version of that claim — what is actually computed — and say what "
        "part of the claim remains genuinely open.",
    steps=[("Each token becomes a vector", "by embedding lookup, plus a positional encoding"),
           ("Each block", "lets every position read every other, weighted by learned relevance"),
           ("After 12 or 96 blocks", "each position's vector is contextualised by the whole window"),
           ("Those representations support", "accurate prediction of what comes next"),
           ("What is not established", "whether that constitutes understanding in any sense beyond "
            "the predictive one")],
    answer="Mechanically: the model computes, for every token, a representation shaped by every "
           "other token in the window, in a way that supports accurate next-token prediction. "
           "Whether that amounts to <b>understanding</b> is an open question — the mechanism is "
           "what you can state with confidence.",
    why="Being able to give the mechanical account, and to mark clearly where it stops, is a large "
        "part of what it means to actually understand these systems rather than to have opinions "
        "about them.")

SET = dict(course="C4", week=4, title="Language models",
           lede="The last set in the specialization. These are less about arithmetic and more "
                "about being able to explain a real system precisely — which is the skill that "
                "actually transfers.",
           problems=L)
