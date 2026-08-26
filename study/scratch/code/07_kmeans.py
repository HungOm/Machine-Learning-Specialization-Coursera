"""k-means from scratch — C3 W1.

Run me:  python3 07_kmeans.py

Two functions, ten lines each. The interesting part is what the cost function
is for: it is how you choose between runs that disagree.
"""
import numpy as np

# %% SECTION: data
X = np.array([[1.0, 1.0], [1.5, 2.0], [3.0, 4.0],
              [5.0, 7.0], [3.5, 5.0], [4.5, 5.0]])
print("six points:\n", X)

# %% SECTION: assign
def assign(X, centroids):
    """Give each point the index of its nearest centroid.

    X[:, None, :] is (m, 1, n) and centroids[None] is (1, k, n); broadcasting
    them together gives every point-centroid difference at once, shape (m,k,n).
    """
    d = np.linalg.norm(X[:, None, :] - centroids[None, :, :], axis=2)   # (m, k)
    return d.argmin(axis=1)

# %% SECTION: move
def move(X, idx, k):
    """Each centroid becomes the mean of the points assigned to it.

    An empty cluster has no mean. Here we re-seed it at a random point, which
    keeps k intact; the alternative is to drop that centroid entirely.
    """
    out = np.zeros((k, X.shape[1]))
    for j in range(k):
        pts = X[idx == j]
        out[j] = pts.mean(axis=0) if len(pts) else X[np.random.randint(len(X))]
    return out

# %% SECTION: cost
def cost(X, idx, centroids):
    """Mean squared distance from each point to its own centroid."""
    return float(np.mean(np.sum((X - centroids[idx]) ** 2, axis=1)))

# %% SECTION: fit
def kmeans(X, k, init, iters=50):
    c = np.array(init, dtype=float)
    for _ in range(iters):
        idx = assign(X, c)
        new = move(X, idx, k)
        if np.allclose(new, c):
            break
        c = new
    idx = assign(X, c)
    return idx, c, cost(X, idx, c)

# %% SECTION: local_optima
print("\nsame data, same algorithm, two different starting points:")
for label, init in [("A: points 1 and 4", [X[0], X[3]]),
                    ("B: points 1 and 3", [X[0], X[2]])]:
    idx, c, J = kmeans(X, 2, init)
    print(f"  {label}  ->  clusters {idx}  J = {J:.4f}")
    print(f"      centroids {np.round(c, 3).tolist()}")
print("\nBoth are converged — neither can improve by another step. They are")
print("different LOCAL optima, and J is the only thing that tells them apart.")

# %% SECTION: restarts
def kmeans_best(X, k, n_restarts=50, seed=0):
    """The standard fix: many random starts, keep the lowest cost."""
    rng = np.random.default_rng(seed)
    best = None
    for _ in range(n_restarts):
        init = X[rng.choice(len(X), size=k, replace=False)]
        idx, c, J = kmeans(X, k, init)
        if best is None or J < best[2]:
            best = (idx, c, J)
    return best

idx, c, J = kmeans_best(X, 2)
print(f"\n50 random restarts -> best J = {J:.4f}, clusters {idx}")

# %% SECTION: elbow
rng = np.random.default_rng(4)
blobs = np.vstack([rng.normal(mu, 0.6, size=(40, 2))
                   for mu in [[0, 0], [5, 5], [10, 0]]])
print("\n120 points drawn from 3 real blobs — the elbow test:")
print(f"{'k':>3} {'J':>9}   {'drop':>8}")
prev = None
for k in range(1, 8):
    _, _, J = kmeans_best(blobs, k, n_restarts=25, seed=k)
    drop = "" if prev is None else f"{prev - J:8.3f}"
    print(f"{k:3d} {J:9.3f}   {drop}")
    prev = J
print("The drops collapse after k = 3, which is where the blobs actually are.")
print("Note J never rises with k: at k = m every point is its own cluster and")
print("J is exactly 0, so you can never pick k by minimising J.")
