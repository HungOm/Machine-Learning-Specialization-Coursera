# -*- coding: utf-8 -*-
"""Beginner-friendly decode for every Course 4 card, keyed by card id."""
from cardkit import plain

P = {

"c4w1-order": plain(
  "Shuffle the words of a sentence and the meaning changes completely — but a model that only counts "
  "how often each word appears sees no difference at all. Order has to be put back in deliberately.",
  [("x⟨t⟩", "“x at time t”", "the t-th word of this sentence"),
   ("T", "“capital T”", "how many words this particular sentence has — different for every one"),
   ("⟨ ⟩", "angle brackets", "→ which POSITION (round = which example, square = which layer)")],
  "Like a recipe: same ingredients, different order, and you get bread or a burnt mess."),

"c4w1-tokens": plain(
  "A model can only look words up in a fixed list it was built with. Whole words make the list "
  "impossibly long; single letters make it meaningless. So it uses chunks of words — a compromise.",
  [("token", "“token”", "one chunk of text — usually part of a word"),
   ("vocabulary", "“vocab”", "the fixed list of chunks the model knows. It never grows"),
   ("BPE", "“byte-pair encoding”", "the method for choosing the chunks — a compression algorithm")],
  "Like a printer's tray of type: single letters AND common chunks like “ing”, so anything can be set."),

"c4w1-onehot": plain(
  "Giving every word its own slot with a 1 in it wastes enormous space — but worse, it makes every "
  "word exactly as different from every other. “Cat” ends up as unrelated to “dog” as to “bulldozer”.",
  [("one-hot", "“one hot”", "a long list of 0s with a single 1 marking which item this is"),
   ("dot product", "“dot product”", "the site's way of measuring similarity. Here it is always 0")],
  "Like hotel room numbers: they identify each guest and say nothing about who is family."),

"c4w1-embedding": plain(
  "Give every word a short list of numbers, stored in one big table. Look up the row to “embed” a "
  "word. The numbers start random and are learned by ordinary gradient descent, like any weight.",
  [("E", "“the embedding matrix”", "the table: one row per word"),
   ("V", "“vocab size”", "how many words — typically 30,000 to 100,000"),
   ("d", "“the dimension”", "how many numbers describe each word — often 512"),
   ("ℝ", "“the real numbers”", "just means “ordinary decimal numbers go here”")],
  "You built this in Course 3 for movies. Words instead of films; identical machinery."),

"c4w1-cosine": plain(
  "To ask how similar two words are, multiply their number-lists together pairwise and add up — then "
  "divide by both lengths so only the DIRECTION counts, not how big the numbers happen to be.",
  [("cos", "“cosine”", "a similarity score from −1 to 1. Near 1 = very alike"),
   ("‖x‖", "“the norm of x”, or “length”", "how long the arrow is: √(sum of squares)"),
   ("·", "“dot”", "multiply matching entries, then add them all up")],
  "Dividing by the lengths matters because long vectors just mean “this word was common in training”."),

"c4w1-rnn": plain(
  "Read the sentence one word at a time, keeping a running summary in your head. Each new word "
  "updates the summary. At the end, the summary is your understanding.",
  [("h⟨t⟩", "“h at time t”", "the running summary after t words. Also called the hidden state"),
   ("h⟨t−1⟩", "“h at t minus one”", "the summary BEFORE this word — this is the loop"),
   ("g", "“the activation function”", "the squashing step, same as every neuron in Course 2")],
  "Like taking a phone message with no paper: fine for short ones, hopeless for long ones."),

"c4w1-rnn-fails": plain(
  "Two separate problems, both fatal. It forgets things from the start of long text. And it has to "
  "process words strictly one after another, so it cannot use fast parallel hardware.",
  [("vanishing gradient", "“the signal fades”", "many numbers below 1 multiplied together → almost zero"),
   ("LSTM", "“L-S-T-M”", "a smarter RNN. Fixes forgetting somewhat; fixes the speed problem not at all"),
   ("serial", "“one after another”", "step 41 cannot start until step 40 finishes")],
  "A whispered message down a line of a hundred people: it gets garbled, AND it takes a hundred turns."),

"c4w1-attention-2014": plain(
  "Instead of squeezing a whole sentence into one summary, keep the summary from every position and "
  "let the model choose which ones to look at — a different choice for every word it writes.",
  [("c", "“the context vector”", "what the model actually reads — a blend of every position"),
   ("α", "“alpha”", "how much to take from each position. They all add up to 1"),
   ("Σ", "“sum over t”", "add up across every position")],
  "A translator with the page in front of them, glancing back — rather than one working from memory."),

"c4w2-formula": plain(
  "Score how relevant every word is to every other word, turn those scores into proportions that add "
  "to 1, then take a weighted average. That is the whole of attention.",
  [("Q, K, V", "“queries, keys, values”", "three versions of the same input — see the next card"),
   ("QKᵀ", "“Q K transpose”", "every query matched against every key. The T just flips it to line the shapes up"),
   ("√dₖ", "“root d k”", "shrinks the scores so they do not get huge. Card 5 explains why"),
   ("softmax", "“soft max”", "turns any scores into positive numbers adding to exactly 1")],
  "Read it right to left and it is one sentence: score, weight, average."),

"c4w2-qkv": plain(
  "Every word produces three different versions of itself: what it is looking for, what it advertises "
  "to others, and what it actually hands over if chosen. Three learned tables, one input.",
  [("W_Q, W_K, W_V", "“W-Q, W-K, W-V”", "three learned matrices, one per role"),
   ("X", "“the input”", "the sentence, already turned into numbers"),
   ("projection", "“projection”", "just means “multiplied by a matrix to get a new version”")],
  "A library: your request, the catalogue card, and the book itself. Three different things."),

"c4w2-shapes": plain(
  "Shapes are how you check attention code is right. T positions in, T positions out — and the score "
  "grid is always T by T, one number for every pair.",
  [("(T, dₖ)", "“T by d-k”", "T rows (one per word), each dₖ numbers long"),
   ("(T, T)", "“T by T”", "the score grid: every word against every word")],
  "Same number of rows in as out is what lets you stack these layers twelve deep."),

"c4w2-byhand": plain(
  "Work it through with tiny numbers once and it stops being mysterious. Score the pairs, shrink them, "
  "softmax each row, and check the row adds to 1.",
  [("0.4011", "—", "e^0.7071 ÷ (sum of all three exponentials) = 2.028 ÷ 5.056"),
   ("row sums to 1", "—", "the check that tells you you did it right")],
  "If your rows do not add to 1, you softmaxed the wrong direction — and nothing will error."),

"c4w2-scale": plain(
  "Longer number-lists give bigger dot products just because you added up more terms. Big scores make "
  "the softmax pick one winner absolutely, and once it does that there is nothing left to learn from.",
  [("dₖ", "“d k”", "how long each query and key is — often 512"),
   ("√", "“square root”", "the amount the spread grows by, so dividing by it cancels it out"),
   ("saturate", "“saturate”", "the softmax goes to 1.0000 and 0.0000 — no gradient left")],
  "Same instinct as feature scaling in Course 1: keep numbers in the range where things still respond."),

"c4w2-multihead": plain(
  "One attention can chase one kind of relationship. Run eight side by side, each with its own tables, "
  "and glue the answers together — for the same total number of parameters.",
  [("head", "“a head”", "one complete attention, with its own three matrices"),
   ("concat", "“concatenate”", "lay the outputs side by side"),
   ("W_O", "“W-O”", "a final matrix that lets the heads' answers actually mix together")],
  "Three specialists surveying one building — you want all three reports, not one averaged opinion."),

"c4w2-mask": plain(
  "A model learning to predict the next word must not be able to see it. Setting future scores to "
  "minus infinity before the softmax makes their weight exactly zero.",
  [("−∞", "“minus infinity”", "e to the power of it is 0, so the position vanishes completely"),
   ("causal", "“causal”", "can depend on the past and present, never the future"),
   ("-1e9", "“minus one e nine”", "what code actually uses — real infinity causes NaN errors")],
  "An exam where the invigilator physically covers the rest of the page."),

"c4w2-cost": plain(
  "Comparing every word with every other means the work grows with the SQUARE of the length. Double "
  "the text and you quadruple the work.",
  [("O(T²)", "“order T squared”", "work grows as length × length"),
   ("O(T)", "“order T”", "work grows in step with length — what an RNN costs")],
  "Handshakes at a party: 10 people is 45, but 20 people is 190 — not double, over four times."),

"c4w3-posenc": plain(
  "Averaging does not care what order things came in, so attention is blind to word order. The fix is "
  "to stamp a distinctive pattern onto each word saying where it sat, before attention runs.",
  [("PE", "“positional encoding”", "the pattern added to each word based on its position"),
   ("sin, cos", "“sine and cosine”", "waves. Several at different speeds, read together"),
   ("pos", "“position”", "which slot in the sentence — 0, 1, 2…")],
  "Numbering the pages before you drop the manuscript."),

"c4w3-residual": plain(
  "Instead of “output = layer(x)”, write “output = x + layer(x)”. The layer now learns what to CHANGE, "
  "and the gradient gets a route home that passes through no weights at all.",
  [("∂y/∂x", "“dee y by dee x”", "how much y changes when x is nudged — a derivative"),
   ("the 1", "—", "the shortcut. No chain of multiplications can shrink it"),
   ("residual", "“residual”", "the leftover — what the layer adds on top of the input")],
  "Tracked changes on a document, rather than retyping every page and risking a new typo each time."),

"c4w3-layernorm": plain(
  "Take one word's numbers, subtract their average, divide by their spread. Now they are centred and "
  "sensibly sized for the next layer — the same z-score you did in Course 1.",
  [("μ", "“mew”", "the average of this one word's numbers"),
   ("σ", "“sigma”", "the spread — how far they typically sit from that average"),
   ("γ, β", "“gamma and beta”", "learned dials so the layer can undo this if it prefers")],
  "Retuning the instrument between movements, not only before the concert."),

"c4w3-ffn": plain(
  "After attention has mixed information between words, each word goes through a small two-layer "
  "network on its own. It exists because averaging is linear, and stacking linear things gets nothing.",
  [("FFN", "“feed-forward network”", "the two-layer network from Course 2, unchanged"),
   ("d_ff", "“d f f”", "the wide middle — usually 4 times the normal width"),
   ("position-wise", "“position-wise”", "applied to each word separately. No mixing happens here")],
  "Attention is the meeting; this is everyone going away to write their own report."),

"c4w3-block": plain(
  "Two steps, each wrapped the same way: normalise, do the thing, add the input back. Do that with "
  "attention, then with the small network. That is one block — and a transformer is this repeated.",
  [("sublayer", "“sublayer”", "one of the two steps inside a block"),
   ("pre-norm", "“pre-norm”", "normalise BEFORE the step. The modern arrangement")],
  "A production-line station whose output is the same shape as its input, so you can put fifty in a row."),

"c4w3-gptbert": plain(
  "One triangle of blocked-out scores is the whole difference between the two famous families. Block "
  "the future and you can generate text; leave it open and you understand better but cannot write.",
  [("decoder-only", "“decoder only”", "GPT-style: masked, generates"),
   ("encoder-only", "“encoder only”", "BERT-style: unmasked, understands"),
   ("bidirectional", "“both directions”", "can see words before AND after")],
  "Writing a letter versus proofreading one. Both skilled; neither can do the other's job."),

"c4w3-count": plain(
  "Every number on a model's spec sheet is something you can add up yourself. Do it once and model "
  "cards stop being marketing and start being information.",
  [("124 M", "“124 million”", "how many numbers this model stores and learns"),
   ("d", "“the width”", "how many numbers represent each word inside the model"),
   ("V × d", "—", "the embedding table: one row of d numbers per vocabulary item")],
  "The plain feed-forward layers are the biggest part. The famous attention is under a quarter."),

"c4w4-objective": plain(
  "Show it text, hide the next word, ask it to guess, correct it. A few hundred billion times. That is "
  "all pretraining is — and facts get stored because storing them is the only way to guess well.",
  [("P(x_t | x_<t)", "“probability of x-t given everything before”", "how likely this word is, given the text so far"),
   ("−log", "“negative log”", "the loss from Course 1 and 2. Confidently wrong costs enormously"),
   ("Σ", "“sum over t”", "add up the loss at every position in the text")],
  "An apprentice who spent ten years finishing their master's sentences, and absorbed the trade doing it."),

"c4w4-perplexity": plain(
  "Perplexity turns the loss into something you can picture: roughly how many options the model is "
  "torn between. Lower is better; 1 would be perfect certainty.",
  [("perplexity", "“perplexity”", "e raised to the loss"),
   ("e", "“e”", "about 2.718 — the same constant from Foundations")],
  "Perplexity 10 means it is about as unsure as if it were picking at random from ten words."),

"c4w4-temperature": plain(
  "The model gives probabilities; something else has to actually pick a word. Temperature is the dial "
  "controlling how adventurous that picking is — and it changes nothing inside the model.",
  [("T", "“temperature”", "divides the scores before softmaxing. Low = safe, high = wild"),
   ("logits", "“logits”", "the raw scores, before they are turned into probabilities"),
   ("argmax", "“arg max”", "always taking the single highest. Sounds right, produces flat repetitive text")],
  "A musician who only ever plays the most expected note. Every note defensible, the solo dead."),

"c4w4-rlhf": plain(
  "A freshly trained model just continues text — ask it a question and it might reply with more "
  "questions. Turning it into an assistant takes two more, much cheaper, training stages.",
  [("SFT", "“supervised fine-tuning”", "showing it written examples of good answers"),
   ("RLHF", "“R-L-H-F”", "reinforcement learning from human feedback"),
   ("reward model", "“reward model”", "a stand-in for a human, trained on which answer people preferred")],
  "Someone who has read every cookbook but never cooked for a guest. What they need is feedback, not more reading."),

"c4w4-context": plain(
  "The context window is the model's entire working memory — anything outside it simply does not "
  "exist. Making it bigger costs you in two different ways at once.",
  [("context window", "“the window”", "how many tokens it can attend to at once"),
   ("KV cache", "“K-V cache”", "saved keys and values so generation does not redo old work"),
   ("O(T²) vs O(T)", "—", "compute grows with the square; memory grows in step with length")],
  "A desk you can spread papers on. Bigger desk, more documents — and papers off the edge are gone."),

"c4w4-limits": plain(
  "Every well-known failure of these systems follows from something you now understand. Being able to "
  "predict where one will fail is as much a mark of understanding as knowing what it can do.",
  [("hallucination", "“hallucination”", "confident, fluent, false. The objective rewarded likely, not true"),
   ("calibration", "“calibration”", "whether stated confidence matches actual accuracy")],
  "A brilliant improviser who was never told they are allowed to say “I don't know”."),

"c4w4-throughline": plain(
  "Four courses, one shape. Choose what the model may look like, define one number for how wrong it "
  "is, and roll downhill. Course 4 only changed the first of those three.",
  [("model", "—", "what f is allowed to be"),
   ("cost", "—", "one number saying how wrong it is"),
   ("optimiser", "—", "gradient descent, usually Adam")],
  "Attention itself is the Foundations dot product plus the Course 2 softmax. The new idea is what they point at."),
}
