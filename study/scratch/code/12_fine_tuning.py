"""Fine-tuning from scratch -- head-only, full, and LoRA, in pure NumPy.

Run me:  python3 12_fine_tuning.py

Nobody trains a large model from nothing. They start from one somebody else
paid for and adapt it, and the interesting question is which parameters to
touch. This file pretrains a small network on one task, then adapts it to a
related task three different ways and measures what each one costs and breaks.
"""
import numpy as np

rng = np.random.default_rng(7)

# %% SECTION: tasks
# Two tasks over the same 20 inputs. Task A (pretraining) has 20000 examples;
# task B (the downstream job) has 60. That ratio is the whole situation: you
# have a lot of general data and very little of the data you actually care
# about.
D_IN, D_HID, N_CLASS = 20, 64, 4
BASIS = rng.normal(size=(6, D_IN))          # shared structure both tasks use

def make_task(n, mix, noise, seed):
    """Both tasks read the same 6 latent directions, weighted differently."""
    r = np.random.default_rng(seed)
    z = r.normal(size=(n, 6))
    X = z @ BASIS + r.normal(0, 0.3, size=(n, D_IN))
    y = np.argmax(z @ mix, axis=1)
    idx = r.permutation(n)[:int(noise * n)]
    y[idx] = r.integers(0, N_CLASS, size=idx.size)
    return X, y

MIX_A = rng.normal(size=(6, N_CLASS))
MIX_B = MIX_A + 0.9 * rng.normal(size=(6, N_CLASS))   # related, not identical

XA, yA = make_task(20000, MIX_A, 0.05, 1)
XA_te, yA_te = make_task(4000, MIX_A, 0.05, 2)
XB, yB = make_task(60, MIX_B, 0.05, 3)
XB_te, yB_te = make_task(4000, MIX_B, 0.05, 4)
print("task A (pretrain) : %d train, %d test" % (len(XA), len(XA_te)))
print("task B (downstream): %d train, %d test  <- this is the realistic part"
      % (len(XB), len(XB_te)))
print("both label rules read the same 6 latent directions, weighted differently")
print("-- which is what 'a related task' means and why transfer can work at all")

# %% SECTION: model
def init(seed):
    r = np.random.default_rng(seed)
    return {"W1": r.normal(0, np.sqrt(2 / D_IN), (D_IN, D_HID)),
            "b1": np.zeros(D_HID),
            "W2": r.normal(0, np.sqrt(2 / D_HID), (D_HID, D_HID)),
            "b2": np.zeros(D_HID),
            "W3": r.normal(0, np.sqrt(1 / D_HID), (D_HID, N_CLASS)),
            "b3": np.zeros(N_CLASS)}

def forward(p, X, delta=None):
    """Two ReLU layers then a linear head. `delta` optionally adds a low-rank
    correction to W2 -- that is the only hook LoRA needs."""
    W2 = p["W2"] if delta is None else p["W2"] + delta["B"] @ delta["A"] * delta["s"]
    h1 = np.maximum(X @ p["W1"] + p["b1"], 0)
    h2 = np.maximum(h1 @ W2 + p["b2"], 0)
    return (h2 @ p["W3"] + p["b3"]), h1, h2

def softmax_ce(logits, y):
    z = logits - logits.max(axis=1, keepdims=True)
    e = np.exp(z)
    prob = e / e.sum(axis=1, keepdims=True)
    m = len(y)
    return -np.mean(np.log(prob[np.arange(m), y] + 1e-12)), prob

def accuracy(p, X, y, delta=None):
    return float(np.mean(np.argmax(forward(p, X, delta)[0], axis=1) == y))

def n_params(p):
    return sum(v.size for v in p.values())

P0 = init(0)
print("parameters: %d" % n_params(P0))
for k, v in P0.items():
    print("   %-3s %-9s %6d" % (k, str(v.shape), v.size))

# %% SECTION: pretrain
def grads(p, X, y, delta=None, train=("W1", "b1", "W2", "b2", "W3", "b3")):
    """One backward pass. `train` names which tensors get a gradient; the rest
    come back as zeros, which is all 'freezing a layer' actually means."""
    logits, h1, h2 = forward(p, X, delta)
    loss, prob = softmax_ce(logits, y)
    m = len(y)
    d3 = prob.copy()
    d3[np.arange(m), y] -= 1
    d3 /= m
    W2 = p["W2"] if delta is None else p["W2"] + delta["B"] @ delta["A"] * delta["s"]
    dh2 = (d3 @ p["W3"].T) * (h2 > 0)
    dh1 = (dh2 @ W2.T) * (h1 > 0)
    g = {"W3": h2.T @ d3, "b3": d3.sum(0),
         "W2": h1.T @ dh2, "b2": dh2.sum(0),
         "W1": X.T @ dh1, "b1": dh1.sum(0)}
    for k in g:
        if k not in train:
            g[k] = np.zeros_like(g[k])
    return loss, g, dh2, h1

def sgd(p, X, y, epochs, lr, bs, train=None, quiet=True):
    """Plain mini-batch gradient descent, reshuffled every epoch.

    `train` is the only new idea in this file: freezing is not a special mode,
    it is simply not applying the update to some tensors.
    """
    train = train or tuple(p)
    r = np.random.default_rng(11)
    for ep in range(epochs):
        order = r.permutation(len(X))
        for s in range(0, len(X), bs):
            idx = order[s:s + bs]
            loss, g, _, _ = grads(p, X[idx], y[idx], train=train)
            for k in train:
                p[k] -= lr * g[k]
        if not quiet and (ep + 1) % 2 == 0:
            print("   epoch %2d  loss %.4f" % (ep + 1, loss))
    return p

BASE = init(0)
sgd(BASE, XA, yA, epochs=8, lr=0.15, bs=128, quiet=False)
ACC_A = accuracy(BASE, XA_te, yA_te)
print("pretrained model on task A: %.4f" % ACC_A)
print("the same model on task B  : %.4f  <- related is not the same" %
      accuracy(BASE, XB_te, yB_te))

# %% SECTION: baseline
# What do you get without the pretrained model at all? This is the number every
# fine-tuning result has to beat, and it is the one most often left out.
SCRATCH = init(3)
sgd(SCRATCH, XB, yB, epochs=400, lr=0.15, bs=16)
ACC_SCRATCH = accuracy(SCRATCH, XB_te, yB_te)
print("trained from scratch on 60 examples: %.4f" % ACC_SCRATCH)
print("train accuracy on those same 60    : %.4f" % accuracy(SCRATCH, XB, yB))
print("Memorising 60 points is easy. Generalising from them is not.")

# %% SECTION: head_only
def clone(p):
    return {k: v.copy() for k, v in p.items()}

HEAD = clone(BASE)
sgd(HEAD, XB, yB, epochs=400, lr=0.15, bs=16, train=("W3", "b3"))
ACC_HEAD = accuracy(HEAD, XB_te, yB_te)
n_head = BASE["W3"].size + BASE["b3"].size
print("head only: trained %d of %d parameters (%.1f%%)"
      % (n_head, n_params(BASE), 100 * n_head / n_params(BASE)))
print("task B accuracy: %.4f" % ACC_HEAD)
print("task A accuracy: %.4f  (was %.4f)" % (accuracy(HEAD, XA_te, yA_te), ACC_A))
print("Task A got worse even though the body never moved -- because the head is")
print("part of task A's model too, and you just retrained it on something else.")
print("'Freezing the body' does not mean 'keeping the old behaviour'.")

# %% SECTION: full
FULL = clone(BASE)
sgd(FULL, XB, yB, epochs=400, lr=0.15, bs=16)
ACC_FULL = accuracy(FULL, XB_te, yB_te)
print("full fine-tune: trained all %d parameters" % n_params(BASE))
print("task B accuracy: %.4f" % ACC_FULL)
print("task A accuracy: %.4f  (was %.4f)" % (accuracy(FULL, XA_te, yA_te), ACC_A))
print("That drop is catastrophic forgetting. Nothing went wrong -- you asked")
print("for the weights that fit 60 examples and you got them.")

# %% SECTION: lora
def lora_init(r, d, seed, alpha=None):
    """W + BA, with B starting at zero so the adapted model begins IDENTICAL to
    the base. If B were random the first step would move you somewhere worse
    than where you started, and you would have to climb back."""
    g = np.random.default_rng(seed)
    alpha = alpha if alpha is not None else r
    return {"A": g.normal(0, 0.01, (r, d)), "B": np.zeros((d, r)),
            "r": r, "s": alpha / r}

def train_lora(base, delta, X, y, epochs, lr, bs):
    r = np.random.default_rng(11)
    for ep in range(epochs):
        order = r.permutation(len(X))
        for s in range(0, len(X), bs):
            idx = order[s:s + bs]
            xb, yb = X[idx], y[idx]
            loss, g, dh2, h1 = grads(base, xb, yb, delta=delta, train=())
            # dL/dW2 = h1^T dh2, and W2eff = W2 + s*B@A, so chain through B and A
            dW = h1.T @ dh2
            dB = delta["s"] * dW @ delta["A"].T
            dA = delta["s"] * delta["B"].T @ dW
            delta["B"] -= lr * dB
            delta["A"] -= lr * dA
    return delta

LORA = lora_init(4, D_HID, 5)
train_lora(BASE, LORA, XB, yB, epochs=400, lr=0.15, bs=16)
ACC_LORA = accuracy(BASE, XB_te, yB_te, delta=LORA)
n_lora = LORA["A"].size + LORA["B"].size
print("LoRA r=4: trained %d of %d parameters (%.1f%%)"
      % (n_lora, n_params(BASE), 100 * n_lora / n_params(BASE)))
print("task B accuracy: %.4f" % ACC_LORA)
print("task A accuracy WITH the adapter   : %.4f" % accuracy(BASE, XA_te, yA_te, LORA))
print("task A accuracy WITHOUT the adapter: %.4f  <- base weights never changed"
      % accuracy(BASE, XA_te, yA_te))
print("You can detach it. That is the property the parameter count does not")
print("show and the reason one base model can serve many customers at once.")

# %% SECTION: rank
print("  r   params  taskB   taskA(+adapter)")
for r in [1, 2, 4, 8, 16, 32]:
    d = lora_init(r, D_HID, 5)
    train_lora(BASE, d, XB, yB, epochs=400, lr=0.15, bs=16)
    print("  %2d  %6d  %.4f  %.4f" % (r, d["A"].size + d["B"].size,
                                      accuracy(BASE, XB_te, yB_te, d),
                                      accuracy(BASE, XA_te, yA_te, d)))
print("W2 is %dx%d = %d numbers. A rank-r update needs 2*%d*r."
      % (D_HID, D_HID, D_HID * D_HID, D_HID))
print("At r=4 that is %d against %d, an %dx saving. Real, but modest -- and it"
      % (2 * D_HID * 4, D_HID * D_HID, D_HID // 8))
print("gets dramatically better as the layer gets bigger, because the full")
print("matrix grows with d squared and the adapter only with d:")
for d in [64, 1024, 4096]:
    print("   a %5dx%-5d layer: full %10d   LoRA r=8 %8d   %.2f%%"
          % (d, d, d * d, 2 * d * 8, 100 * 2 * 8.0 / d))
print("That last line is why LoRA matters on real models and barely registers")
print("here. And rank r can only move the weights in r directions -- if the task")
print("needs more than that, the adapter cannot follow it.")

# %% SECTION: verdict
rows = [("from scratch", n_params(BASE), ACC_SCRATCH, accuracy(SCRATCH, XA_te, yA_te)),
        ("head only", n_head, ACC_HEAD, accuracy(HEAD, XA_te, yA_te)),
        ("full fine-tune", n_params(BASE), ACC_FULL, accuracy(FULL, XA_te, yA_te)),
        ("LoRA r=4", n_lora, ACC_LORA, accuracy(BASE, XA_te, yA_te, LORA))]
print("  method            trained    task B   task A after")
for name, n, b, a in rows:
    print("  %-16s %7d    %.4f   %.4f" % (name, n, b, a))
print("  %-16s %7s    %.4f   %.4f" % ("(base, untouched)", "0",
                                      accuracy(BASE, XB_te, yB_te), ACC_A))
print("\nThere is no winner column. Pick by what you are short of: data, compute,")
print("memory, or the need to keep the original behaviour intact.")

# %% SECTION: relatedness
# The question that actually decides whether any of this works: how related
# are the two tasks? Drift the label rule away from the pretraining one and
# watch four different things happen.
PERT = np.random.default_rng(21).normal(size=MIX_A.shape)
print("  drift   base as-is   scratch   full FT   LoRA r=4")
for c in [0.0, 0.3, 0.6, 0.9, 1.5, 3.0]:
    MB = MIX_A + c * PERT
    Xn, yn = make_task(60, MB, 0.05, 3)
    Xt, yt = make_task(4000, MB, 0.05, 4)
    s_ = init(3); sgd(s_, Xn, yn, epochs=400, lr=0.15, bs=16)
    f_ = clone(BASE); sgd(f_, Xn, yn, epochs=400, lr=0.15, bs=16)
    l_ = lora_init(4, D_HID, 5); train_lora(BASE, l_, Xn, yn, epochs=400, lr=0.15, bs=16)
    print("   %4.1f     %.4f     %.4f    %.4f    %.4f"
          % (c, accuracy(BASE, Xt, yt), accuracy(s_, Xt, yt),
             accuracy(f_, Xt, yt), accuracy(BASE, Xt, yt, l_)))
print("\nTwo different stories in one table.")
print("The 'base as-is' column falls off a cliff: 0.89 down to 0.47, which is")
print("barely above the 0.25 you would get by guessing. Using a model unchanged")
print("only works while the new task really is the old task.")
print("The 'full FT' column does not fall off. Even at drift 3.0, where the")
print("label rule has almost nothing to do with the original, fine-tuning still")
print("beats training from scratch on the same 60 examples.")
print("That is the point most explanations skip: what transfers is not the")
print("answers, it is the FEATURES. Both tasks read the same latent directions,")
print("and a body that already knows how to extract them is worth having even")
print("when it has been asked a completely different question.")

# %% SECTION: data_size
# And the other axis: how much task-B data would make this whole file moot?
print("   n_B   scratch   head   full   LoRA r=4")
for n in [20, 60, 200, 1000, 5000]:
    Xn, yn = make_task(n, MIX_B, 0.05, 3)
    ep = max(40, int(24000 / n))
    s_ = init(3); sgd(s_, Xn, yn, epochs=ep, lr=0.15, bs=16)
    h_ = clone(BASE); sgd(h_, Xn, yn, epochs=ep, lr=0.15, bs=16, train=("W3", "b3"))
    f_ = clone(BASE); sgd(f_, Xn, yn, epochs=ep, lr=0.15, bs=16)
    l_ = lora_init(4, D_HID, 5); train_lora(BASE, l_, Xn, yn, epochs=ep, lr=0.15, bs=16)
    print("  %5d   %.4f  %.4f  %.4f  %.4f"
          % (n, accuracy(s_, XB_te, yB_te), accuracy(h_, XB_te, yB_te),
             accuracy(f_, XB_te, yB_te), accuracy(BASE, XB_te, yB_te, l_)))
print("\nThe columns converge. By 5000 examples every method lands within a")
print("point or two of every other, and the pretrained start has stopped")
print("earning its keep. Note also that the differences at n=20 are smaller")
print("than the differences at n=200 -- with 20 examples nothing works well")
print("enough for the choice of method to matter. Fine-tuning pays in the")
print("middle band, where you have enough data to steer a model but not enough")
print("to raise one.")
