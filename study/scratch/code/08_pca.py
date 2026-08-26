"""PCA from scratch — C3 W2, via the covariance matrix and its eigenvectors.

Run me:  python3 08_pca.py

Also does it a second way (the SVD) and shows the two agree, because that is
what every library actually uses.
"""
import numpy as np

# %% SECTION: centre
def centre(X):
    """PCA is about variance, and variance is measured around the mean.

    Skipping this step makes the first component point at the mean instead of
    along the spread — a silent and very common error.
    """
    mu = X.mean(axis=0)
    return X - mu, mu

# %% SECTION: covariance
def covariance(Xc):
    """(1/m) Xc^T Xc — entry (i,j) is how features i and j vary together."""
    m = Xc.shape[0]
    return (Xc.T @ Xc) / m

X = np.array([[1., 2.], [2., 1.], [3., 5.], [4., 4.], [5., 3.]])
Xc, mu = centre(X)
C = covariance(Xc)
print("data:\n", X)
print("column means:", mu)
print("covariance:\n", C)
print("diagonal = each feature's variance; off-diagonal = how they move together")

# %% SECTION: eigen
def pca_eig(X, k):
    """Principal components are the eigenvectors of the covariance matrix.

    eigh is for symmetric matrices, which a covariance matrix always is. It
    returns eigenvalues in ASCENDING order, so we reverse them.
    """
    Xc, mu = centre(X)
    C = covariance(Xc)
    vals, vecs = np.linalg.eigh(C)
    order = np.argsort(vals)[::-1]
    vals, vecs = vals[order], vecs[:, order]
    return vecs[:, :k], vals, mu

W, vals, mu = pca_eig(X, 1)
print(f"\neigenvalues: {np.round(vals, 4)}   (variance along each direction)")
print(f"first principal component: {np.round(W[:, 0], 4)}")
print(f"variance explained by PC1: {vals[0] / vals.sum():.4f}")

# %% SECTION: project
def project(X, W, mu):
    """Squash each point onto the components: z = (x - mu) @ W."""
    return (X - mu) @ W

def reconstruct(Z, W, mu):
    """Come back out: x_approx = z @ W.T + mu. Not lossless unless k = n."""
    return Z @ W.T + mu

Z = project(X, W, mu)
Xr = reconstruct(Z, W, mu)
err = np.mean(np.sum((X - Xr) ** 2, axis=1))
print("\nprojected to 1-D:", np.round(Z.ravel(), 4))
print("reconstructed:\n", np.round(Xr, 3))
print(f"mean squared reconstruction error: {err:.4f}")
print(f"discarded eigenvalue was {vals[1]:.4f}  <- the error equals it")

# %% SECTION: svd
def pca_svd(X, k):
    """The way every library really does it: SVD, no covariance matrix formed.

    Forming X^T X squares the condition number, which loses precision. SVD
    works on X directly and is numerically better behaved.
    """
    Xc, mu = centre(X)
    U, S, Vt = np.linalg.svd(Xc, full_matrices=False)
    return Vt[:k].T, (S ** 2) / Xc.shape[0], mu

W2, vals2, _ = pca_svd(X, 1)
print("\nSVD route:")
print(f"  component  {np.round(W2[:, 0], 4)}")
print(f"  eigenvalues {np.round(vals2, 4)}")
# Components are only defined up to a sign — both directions span the same line.
same = np.allclose(np.abs(W[:, 0]), np.abs(W2[:, 0]))
print(f"  same direction as eigen route (up to sign): {same}")
print(f"  same eigenvalues: {np.allclose(np.sort(vals), np.sort(vals2))}")

# %% SECTION: perfect
# A perfectly correlated dataset — the second dimension carries nothing.
Xp = np.array([[1., 1.], [2., 2.], [3., 3.], [4., 4.], [5., 5.]])
Wp, valsp, mup = pca_eig(Xp, 1)
Zp = project(Xp, Wp, mup)
print("\nperfectly correlated data:")
print(f"  eigenvalues {np.round(valsp, 6)}  <- the second is exactly 0")
print(f"  variance explained by PC1: {valsp[0] / valsp.sum():.4f}")
print(f"  reconstruction error: "
      f"{np.mean(np.sum((Xp - reconstruct(Zp, Wp, mup))**2, axis=1)):.2e}  <- lossless")

# %% SECTION: higher_dim
# 50 features that secretly live in 3 dimensions.
rng = np.random.default_rng(0)
latent = rng.normal(size=(300, 3))
mixing = rng.normal(size=(3, 50))
Xh = latent @ mixing + rng.normal(0, 0.05, size=(300, 50))
_, vh, _ = pca_eig(Xh, 3)
cum = np.cumsum(vh) / vh.sum()
print("\n50 noisy features generated from 3 latent ones:")
for k in [1, 2, 3, 4, 10]:
    print(f"  first {k:2d} components explain {cum[k-1]:.4f} of the variance")
print("The cliff after 3 is PCA finding the true dimensionality on its own.")
