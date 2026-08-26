"""Softmax and multi-class classification from scratch — C2 W2.

Run me:  python3 05_softmax.py

Includes the numerical-stability trick that `from_logits=True` uses, shown
by breaking the naive version first.
"""
import numpy as np

# %% SECTION: naive
def softmax_naive(z):
    e = np.exp(z)
    return e / e.sum()

print("softmax([2, 1, 0, 3]) =", np.round(softmax_naive(np.array([2., 1., 0., 3.])), 4))
print("sums to", softmax_naive(np.array([2., 1., 0., 3.])).sum())

# %% SECTION: overflow
# Now break it. Logits of a few hundred are entirely normal in a trained network.
with np.errstate(over="ignore", invalid="ignore"):
    bad = softmax_naive(np.array([1000., 999., 998.]))
print("\nnaive softmax on [1000, 999, 998]:", bad, " <- overflowed to nan")

# %% SECTION: stable
def softmax(z, axis=-1):
    """Subtract the max first. Algebraically identical, numerically safe.

    softmax(z + c) == softmax(z) for any constant c, because e^c cancels
    from the top and the bottom. Choosing c = -max(z) makes the largest
    exponent e^0 = 1, so nothing can overflow.
    """
    z = np.asarray(z, dtype=float)
    z = z - z.max(axis=axis, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=axis, keepdims=True)

print("stable softmax on [1000, 999, 998]:", np.round(softmax(np.array([1000., 999., 998.])), 4))
print("shift invariance:  softmax([2,1,0]) ==", np.round(softmax(np.array([2., 1., 0.])), 6))
print("                   softmax([12,11,10]) ==", np.round(softmax(np.array([12., 11., 10.])), 6))

# %% SECTION: logsoftmax
def log_softmax(z, axis=-1):
    """log(softmax(z)) without ever forming softmax(z).

    log(e^z_i / sum e^z_j) = z_i - log(sum e^z_j). Computing it this way never
    creates the tiny probability that log() would then have to rescue.
    """
    z = np.asarray(z, dtype=float)
    m = z.max(axis=axis, keepdims=True)
    return z - m - np.log(np.exp(z - m).sum(axis=axis, keepdims=True))

# A gap of ~750 in the logits is enough: e^-750 is below the smallest float64,
# so the probability underflows to exactly 0 and log(0) is -inf.
z = np.array([400., 0., -400.])
with np.errstate(divide="ignore"):
    p_first = softmax(z)
    naive_log = np.log(p_first)
print("\nsoftmax([400, 0, -400])   :", p_first, " <- the last one underflowed to 0")
print("then log of that          :", naive_log, " <- -inf, and no gradient")
print("direct log_softmax        :", np.round(log_softmax(z), 1), " <- still usable")
print("Same maths, different order of operations, and only one of them survives.")

# %% SECTION: loss
def cross_entropy(logits, y):
    """Mean loss over a batch. y holds integer class indices.

    Only the true class's log-probability enters the loss — that is the
    "pick one entry" that the -log(a_y) formula describes.
    """
    ls = log_softmax(logits, axis=1)
    return float(-ls[np.arange(len(y)), y].mean())

# %% SECTION: gradient
def grad_logits(logits, y):
    """dJ/dz for softmax + cross-entropy is (softmax(z) - onehot(y)) / m.

    Exactly the same shape of answer as sigmoid + log loss. The messy
    derivatives cancel, which is the real reason these pairs go together.
    """
    m = len(y)
    P = softmax(logits, axis=1)
    P[np.arange(m), y] -= 1.0
    return P / m

rng = np.random.default_rng(3)
logits = rng.normal(size=(5, 4))
yv = rng.integers(0, 4, size=5)
ana = grad_logits(logits.copy(), yv)
num = np.zeros_like(ana)
eps = 1e-6
for i in range(logits.size):
    up, dn = logits.copy(), logits.copy()
    up.reshape(-1)[i] += eps; dn.reshape(-1)[i] -= eps
    num.reshape(-1)[i] = (cross_entropy(up, yv) - cross_entropy(dn, yv)) / (2 * eps)
print(f"\ngradient check: max diff {np.max(np.abs(ana - num)):.3e}  "
      f"{'PASS' if np.max(np.abs(ana - num)) < 1e-7 else 'FAIL'}")

# %% SECTION: train
# Three blobs, one linear softmax classifier, trained by hand.
means = np.array([[0., 0.], [4., 4.], [8., 0.]])
X = np.vstack([rng.normal(mu, 1.1, size=(60, 2)) for mu in means])
y = np.repeat([0, 1, 2], 60)
Xs = (X - X.mean(0)) / X.std(0)
W, b = np.zeros((2, 3)), np.zeros(3)
print("\ntraining a 3-class softmax classifier:")
for it in range(3001):
    logits = Xs @ W + b
    if it % 750 == 0:
        acc = (logits.argmax(1) == y).mean()
        print(f"  iter {it:4d}  loss {cross_entropy(logits, y):.4f}  acc {acc:.3f}")
    dZ = grad_logits(logits, y)
    W -= 0.5 * (Xs.T @ dZ)
    b -= 0.5 * dZ.sum(0)
print(f"final accuracy: {(( Xs @ W + b).argmax(1) == y).mean():.4f}")

# %% SECTION: multilabel
# Multi-class vs multi-label: the difference in one comparison.
def sigmoid(z): return 1 / (1 + np.exp(-np.asarray(z, float)))
raw = np.array([3.0, 2.5, -1.0])            # car, bus, pedestrian
print("\nsame three logits, two different heads:")
print("  softmax (mutually exclusive):", np.round(softmax(raw), 4),
      " sum =", round(float(softmax(raw).sum()), 4))
print("  sigmoids (independent)      :", np.round(sigmoid(raw), 4),
      " sum =", round(float(sigmoid(raw).sum()), 4))
print("  A photo can hold a car AND a bus. Softmax cannot say that: raising")
print("  one probability must lower the others. Independent sigmoids can.")
