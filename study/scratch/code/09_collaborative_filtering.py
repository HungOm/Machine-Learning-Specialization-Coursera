"""Collaborative filtering from scratch — C3 W2.

Run me:  python3 09_collaborative_filtering.py

Learns BOTH the user preferences and the movie features at the same time,
from nothing but the ratings. Uses the lecture's five-film dataset.
"""
import numpy as np

# %% SECTION: data
# nan = not rated. The whole algorithm is about respecting those gaps.
FILMS = ["Love at Last", "Romance Forever", "Cute Puppies of Love",
         "Nonstop Car Chases", "Swords vs Karate"]
USERS = ["Alice", "Bob", "Carol", "Dave"]
Y = np.array([
    [5., 5., 0., 0.],
    [5., np.nan, np.nan, 0.],
    [np.nan, 4., 0., np.nan],
    [0., 0., 5., 4.],
    [0., 0., 5., np.nan],
])
R = (~np.isnan(Y)).astype(float)          # 1 where a rating exists
Yf = np.nan_to_num(Y)                      # zeros where it does not (masked out below)
n_m, n_u = Y.shape
print(f"{n_m} films, {n_u} users, {int(R.sum())} of {n_m*n_u} cells rated "
      f"({100*R.mean():.0f}% dense)")

# %% SECTION: normalise
def mean_normalise(Y, R):
    """Subtract each film's mean over the users who actually rated it.

    Without this, a user with no ratings learns w = 0 (regularization pulls it
    there and nothing pushes back) and is predicted to rate everything 0.
    After it, that same user is predicted the film's average.
    """
    counts = R.sum(axis=1)
    mu = np.where(counts > 0, (Y * R).sum(axis=1) / np.maximum(counts, 1), 0.0)
    return (Y - mu[:, None]) * R, mu

Yn, mu = mean_normalise(Yf, R)
print("\nper-film mean rating:", np.round(mu, 3))

# %% SECTION: cost
def cost(X, W, b, Yn, R, lam):
    """Squared error over RATED cells only, plus regularization on X and W.

    Multiplying by R is what makes "not rated" different from "rated 0".
    Without it the model would learn that every gap means "hated it".
    """
    err = (X @ W.T + b) - Yn
    J = 0.5 * np.sum((err * R) ** 2)
    J += (lam / 2) * (np.sum(X ** 2) + np.sum(W ** 2))
    return float(J)

# %% SECTION: gradient
def gradients(X, W, b, Yn, R, lam):
    """Derivatives with respect to the film features AND the user weights.

    That is the whole trick: X is an unknown being optimised, not data.
    """
    err = ((X @ W.T + b) - Yn) * R          # masked error, (n_m, n_u)
    dX = err @ W + lam * X                  # (n_m,n_u)@(n_u,k) -> (n_m,k)
    dW = err.T @ X + lam * W                # (n_u,n_m)@(n_m,k) -> (n_u,k)
    db = err.sum(axis=0)                    # (n_u,)
    return dX, dW, db

# %% SECTION: gradcheck
rng = np.random.default_rng(1)
k = 3
X = rng.normal(0, .5, (n_m, k)); W = rng.normal(0, .5, (n_u, k)); b = np.zeros(n_u)
lam = 1.0
dX, dW, db = gradients(X, W, b, Yn, R, lam)
def num_grad(mat, which):
    g = np.zeros_like(mat)
    for i in range(mat.size):
        up, dn = mat.copy(), mat.copy()
        up.reshape(-1)[i] += 1e-6; dn.reshape(-1)[i] -= 1e-6
        a = cost(up, W, b, Yn, R, lam) if which == "X" else cost(X, up, b, Yn, R, lam)
        c = cost(dn, W, b, Yn, R, lam) if which == "X" else cost(X, dn, b, Yn, R, lam)
        g.reshape(-1)[i] = (a - c) / 2e-6
    return g
print(f"\ngradient check  dX: {np.max(np.abs(dX - num_grad(X, 'X'))):.2e}   "
      f"dW: {np.max(np.abs(dW - num_grad(W, 'W'))):.2e}")

# %% SECTION: train
def fit(Yn, R, k=3, lam=1.0, alpha=0.02, iters=3000, seed=1):
    rng = np.random.default_rng(seed)
    n_m, n_u = Yn.shape
    X = rng.normal(0, .5, (n_m, k))
    W = rng.normal(0, .5, (n_u, k))
    b = np.zeros(n_u)
    for i in range(iters):
        dX, dW, db = gradients(X, W, b, Yn, R, lam)
        X -= alpha * dX; W -= alpha * dW; b -= alpha * db
        if i % (iters // 5) == 0:
            print(f"  iter {i:5d}  cost {cost(X, W, b, Yn, R, lam):9.5f}")
    return X, W, b

print("\ntraining (learning X and W together):")
X, W, b = fit(Yn, R)

# %% SECTION: predict
P = X @ W.T + b + mu[:, None]              # add the film means back
print("\npredicted ratings (existing ratings in brackets):")
print(f"{'':24s}" + "".join(f"{u:>10s}" for u in USERS))
for i, f in enumerate(FILMS):
    row = "".join(
        f"{P[i,j]:>7.2f}" + (f"[{Y[i,j]:.0f}]" if R[i, j] else "   ")
        for j in range(n_u))
    print(f"{f:24s}{row}")

rated = R.astype(bool)
print(f"\nerror on the ratings it was shown: "
      f"{np.sqrt(np.mean((P[rated] - Yf[rated])**2)):.4f} RMSE")

# %% SECTION: cold_start
# A brand-new user who has rated nothing at all.
Y2 = np.c_[Yf, np.zeros(n_m)]
R2 = np.c_[R, np.zeros(n_m)]
Yn2, mu2 = mean_normalise(Y2, R2)
X2, W2, b2 = fit(Yn2, R2, iters=3000)
P2 = X2 @ W2.T + b2 + mu2[:, None]
print("\ncold start — a new user, Eve, who has rated nothing:")
print(f"  her learned w = {np.round(W2[-1], 6)}  (regularization pulled it to 0)")
print(f"  her learned b = {b2[-1]:.6f}")
print("  film                      predicted   film average")
for i, f in enumerate(FILMS):
    print(f"  {f:24s} {P2[i,-1]:9.3f} {mu2[i]:14.3f}")
print("  Without mean normalisation she would be predicted 0.00 for everything.")

# %% SECTION: related
# Similar films fall out for free: compare the learned feature vectors.
print("\nmost similar film to each (squared distance in learned feature space):")
for i, f in enumerate(FILMS):
    d = np.sum((X - X[i]) ** 2, axis=1)
    d[i] = np.inf
    j = int(d.argmin())
    print(f"  {f:24s} -> {FILMS[j]:24s} (d = {d[j]:.3f})")
