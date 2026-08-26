"""Linear regression from scratch — no scikit-learn, no TensorFlow.

Run me:  python3 01_linear_regression.py

Everything here is C1 W1-W2 in about 60 lines of NumPy. The last section
checks the answer against scikit-learn, so you can see it really is the same.
"""
import numpy as np

# %% SECTION: data
# A tiny house dataset: size (1000 sq ft), bedrooms, age (years) -> price ($1000s)
X = np.array([
    [2.10, 3, 20], [1.60, 3, 15], [2.40, 3, 18], [1.42, 2, 30],
    [3.00, 4, 8],  [1.99, 3, 25], [1.27, 2, 40], [2.65, 4, 12],
], dtype=float)
y = np.array([400., 330., 369., 232., 540., 400., 200., 480.])
m, n = X.shape
print(f"m = {m} examples, n = {n} features")

# %% SECTION: cost
def compute_cost(X, y, w, b):
    """J(w,b) = (1/2m) sum (f - y)^2.

    X is (m, n), w is (n,), b is a scalar. X @ w is (m,) — one prediction per
    row — and + b broadcasts the same number onto all of them.
    """
    f = X @ w + b                    # (m,)
    err = f - y                      # (m,)
    return float(np.sum(err ** 2) / (2 * len(y)))

# %% SECTION: gradient
def compute_gradient(X, y, w, b):
    """The two partial derivatives, vectorized.

    dj_dw[j] = (1/m) sum (f - y) * x_j   ->  that is column j of X dotted with
    the error vector, for every j at once, which is exactly X.T @ err.
    """
    m = len(y)
    err = (X @ w + b) - y            # (m,)
    dj_dw = (X.T @ err) / m          # (n, m) @ (m,) -> (n,)
    dj_db = float(np.sum(err) / m)   # scalar
    return dj_dw, dj_db

# %% SECTION: check_gradient
def numeric_gradient(f, theta, eps=1e-6):
    """Central difference. Used only to prove the analytic gradient is right."""
    g = np.zeros_like(theta, dtype=float)
    for i in range(theta.size):
        up, dn = theta.astype(float).copy(), theta.astype(float).copy()
        up[i] += eps
        dn[i] -= eps
        g[i] = (f(up) - f(dn)) / (2 * eps)
    return g

w0, b0 = np.array([0.2, -1.0, 0.5]), 3.0
ana_w, ana_b = compute_gradient(X, y, w0, b0)
num_w = numeric_gradient(lambda w: compute_cost(X, y, w, b0), w0)
num_b = numeric_gradient(lambda bb: compute_cost(X, y, w0, bb[0]), np.array([b0]))[0]
print("analytic dj_dw:", np.round(ana_w, 6))
print("numeric  dj_dw:", np.round(num_w, 6))
print("max difference:", f"{np.max(np.abs(ana_w - num_w)):.3e}",
      "| db diff:", f"{abs(ana_b - num_b):.3e}")

# %% SECTION: scaling
def zscore(X):
    """Return scaled X plus the mu and sigma you must keep for prediction."""
    mu = X.mean(axis=0)
    sigma = X.std(axis=0)
    return (X - mu) / sigma, mu, sigma

Xs, mu, sigma = zscore(X)
print("\nbefore scaling, column ranges:", np.round(X.max(0) - X.min(0), 2))
print("after  scaling, column ranges:", np.round(Xs.max(0) - Xs.min(0), 2))

# %% SECTION: descent
def gradient_descent(X, y, alpha, iters):
    w = np.zeros(X.shape[1])
    b = 0.0
    history = []
    for i in range(iters):
        dj_dw, dj_db = compute_gradient(X, y, w, b)
        w = w - alpha * dj_dw        # both updates use the OLD w and b,
        b = b - alpha * dj_db        # because both gradients were computed above
        if i % (iters // 10) == 0 or i == iters - 1:
            history.append((i, compute_cost(X, y, w, b)))
    return w, b, history

w, b, hist = gradient_descent(Xs, y, alpha=0.1, iters=2000)
print("\niteration      cost")
for i, c in hist:
    print(f"{i:9d}  {c:9.4f}")
print(f"\nlearned w = {np.round(w, 3)}   b = {b:.3f}")

# %% SECTION: predict
def predict(x_raw, w, b, mu, sigma):
    """Scale with the TRAINING mu and sigma, never with new data's own."""
    return float(((x_raw - mu) / sigma) @ w + b)

house = np.array([2.0, 3, 22])
print(f"\n2000 sq ft, 3 bed, 22 yrs -> ${predict(house, w, b, mu, sigma):.1f}k")
print("training predictions:", np.round(Xs @ w + b, 1))
print("actual prices:       ", y)

# %% SECTION: compare
# The closed-form solution (the "normal equation") for comparison.
Xb = np.c_[np.ones(m), X]                       # add a column of 1s for b
theta = np.linalg.lstsq(Xb, y, rcond=None)[0]   # least squares, solved directly
print("\nnormal equation  b, w:", np.round(theta, 3))
# Undo the scaling on our gradient-descent answer so the two are comparable
w_unscaled = w / sigma
b_unscaled = b - float(w @ (mu / sigma))
print("gradient descent b, w:", np.round(np.r_[b_unscaled, w_unscaled], 3))
print("agree to 3 dp:", np.allclose(theta, np.r_[b_unscaled, w_unscaled], atol=1e-3))
