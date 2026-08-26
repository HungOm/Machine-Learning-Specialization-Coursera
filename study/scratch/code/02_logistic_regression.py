"""Logistic regression from scratch — C1 W3 in NumPy.

Run me:  python3 02_logistic_regression.py

Same skeleton as linear regression. Three things change: a sigmoid on the
output, log loss instead of squared error, and a lambda term on w.
"""
import numpy as np

# %% SECTION: data
rng = np.random.default_rng(7)
# Two blobs: exam scores of students who passed (1) and failed (0)
neg = rng.normal([45, 50], 12, size=(40, 2))
pos = rng.normal([70, 72], 12, size=(40, 2))
X = np.vstack([neg, pos])
y = np.r_[np.zeros(40), np.ones(40)]
m, n = X.shape
print(f"m = {m}, n = {n}, positives = {int(y.sum())}")

# %% SECTION: sigmoid
def sigmoid(z):
    """1 / (1 + e^-z), written so it never overflows.

    For very negative z, e^-z is astronomically large and np.exp warns.
    The two branches are algebraically identical; each avoids the overflow
    the other would hit.
    """
    z = np.asarray(z, dtype=float)
    out = np.empty_like(z)
    pos = z >= 0
    out[pos] = 1.0 / (1.0 + np.exp(-z[pos]))
    ez = np.exp(z[~pos])
    out[~pos] = ez / (1.0 + ez)
    return out

print("sigmoid(-1000) =", sigmoid(-1000.0), " (no overflow warning)")
print("sigmoid([-2, 0, 2]) =", np.round(sigmoid([-2, 0, 2]), 4))
print("g(-z) == 1 - g(z):", np.allclose(sigmoid(-3.7), 1 - sigmoid(3.7)))

# %% SECTION: cost
def compute_cost(X, y, w, b, lam=0.0):
    """Average log loss, plus the regularization term on w only (never b)."""
    f = sigmoid(X @ w + b)
    eps = 1e-12                                  # keeps log() away from 0
    f = np.clip(f, eps, 1 - eps)
    loss = -(y * np.log(f) + (1 - y) * np.log(1 - f))
    return float(loss.mean() + (lam / (2 * len(y))) * np.sum(w ** 2))

# %% SECTION: gradient
def compute_gradient(X, y, w, b, lam=0.0):
    """Character for character the same as linear regression, except f."""
    m = len(y)
    err = sigmoid(X @ w + b) - y
    dj_dw = (X.T @ err) / m + (lam / m) * w      # penalty derivative is (lam/m)w
    dj_db = float(err.sum() / m)                 # b is NOT regularized
    return dj_dw, dj_db

# %% SECTION: check_gradient
def numeric_gradient(f, theta, eps=1e-6):
    g = np.zeros_like(theta, dtype=float)
    for i in range(theta.size):
        up, dn = theta.astype(float).copy(), theta.astype(float).copy()
        up[i] += eps; dn[i] -= eps
        g[i] = (f(up) - f(dn)) / (2 * eps)
    return g

Xs = (X - X.mean(0)) / X.std(0)                  # scale, as always
w0, b0, lam = np.array([0.3, -0.2]), 0.1, 1.5
ana, _ = compute_gradient(Xs, y, w0, b0, lam)
num = numeric_gradient(lambda w: compute_cost(Xs, y, w, b0, lam), w0)
print("\nanalytic dj_dw:", np.round(ana, 8))
print("numeric  dj_dw:", np.round(num, 8))
print("max difference:", f"{np.max(np.abs(ana - num)):.3e}")

# %% SECTION: train
def gradient_descent(X, y, alpha, iters, lam=0.0):
    w, b = np.zeros(X.shape[1]), 0.0
    for i in range(iters):
        dw, db = compute_gradient(X, y, w, b, lam)
        w, b = w - alpha * dw, b - alpha * db
        if i % (iters // 5) == 0:
            print(f"  iter {i:5d}  cost {compute_cost(X, y, w, b, lam):.5f}")
    return w, b

print("\ntraining (lambda = 0):")
w, b = gradient_descent(Xs, y, alpha=0.5, iters=5000)
print(f"learned w = {np.round(w, 4)}  b = {b:.4f}")

# %% SECTION: evaluate
prob = sigmoid(Xs @ w + b)
pred = (prob >= 0.5).astype(int)                 # the threshold is a separate choice
acc = (pred == y).mean()
tp = int(((pred == 1) & (y == 1)).sum()); fp = int(((pred == 1) & (y == 0)).sum())
fn = int(((pred == 0) & (y == 1)).sum()); tn = int(((pred == 0) & (y == 0)).sum())
prec = tp / (tp + fp); rec = tp / (tp + fn)
print(f"\naccuracy {acc:.3f}   TP {tp}  FP {fp}  FN {fn}  TN {tn}")
print(f"precision {prec:.3f}   recall {rec:.3f}   F1 {2*prec*rec/(prec+rec):.3f}")

# %% SECTION: boundary
# The boundary is where z = 0, i.e. w1*x1 + w2*x2 + b = 0.
# Solve for x2:  x2 = -(w1*x1 + b) / w2
print("\ndecision boundary in scaled space:")
for x1 in [-1.0, 0.0, 1.0]:
    print(f"  x1 = {x1:+.1f}  ->  x2 = {-(w[0]*x1 + b)/w[1]:+.3f}")

# %% SECTION: regularization
print("\nwhat lambda does to the weights:")
print(f"{'lambda':>8}  {'|w|':>8}  {'train acc':>9}")
for lam in [0.0, 1.0, 10.0, 100.0]:
    wl, bl = np.zeros(n), 0.0
    for _ in range(3000):
        dw, db = compute_gradient(Xs, y, wl, bl, lam)
        wl, bl = wl - 0.5 * dw, bl - 0.5 * db
    a = ((sigmoid(Xs @ wl + bl) >= 0.5).astype(int) == y).mean()
    print(f"{lam:8.0f}  {np.linalg.norm(wl):8.4f}  {a:9.3f}")
print("\nbigger lambda -> smaller weights -> a flatter, more cautious model.")

# %% SECTION: decay_limit
# Regularized descent shrinks w by (1 - alpha*lam/m) before every gradient step.
# If that factor goes negative, w flips sign and grows every iteration. This is
# a real trap: a lambda that is fine at one alpha diverges at another.
print("\nthe hidden constraint between alpha and lambda:")
print(f"{'alpha':>7} {'lambda':>7} {'1-a*l/m':>9}   outcome")
for alpha, lam in [(0.5, 100.0), (0.5, 320.0), (0.5, 1000.0), (0.05, 1000.0)]:
    factor = 1 - alpha * lam / m
    wl, bl = np.zeros(n), 0.0
    with np.errstate(over="ignore", invalid="ignore"):   # divergence is the point here
        for _ in range(2000):
            dw, db = compute_gradient(Xs, y, wl, bl, lam)
            wl, bl = wl - alpha * dw, bl - alpha * db
        norm = np.linalg.norm(wl)
    state = "diverged" if not np.isfinite(norm) else f"|w| = {norm:.4f}"
    print(f"{alpha:7.2f} {lam:7.0f} {factor:9.3f}   {state}")
print("\nStable only while alpha*lambda/m < 2, i.e. alpha < 2m/lambda.")
print(f"With m = {m} and lambda = 1000 that means alpha < {2*m/1000:.3f}.")
