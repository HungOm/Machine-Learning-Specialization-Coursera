"""A decision tree from scratch — C2 W4, no gradients anywhere.

Run me:  python3 06_decision_tree.py

Uses the exact ten-animal dataset from the lectures, so every number printed
below can be checked against the slides.
"""
import numpy as np

# %% SECTION: data
# ear shape (1 = pointy), face shape (1 = round), whiskers (1 = present)
FEATURES = ["ear shape", "face shape", "whiskers"]
X = np.array([
    [1, 1, 1], [0, 0, 1], [0, 1, 0], [1, 0, 1], [1, 1, 1],
    [1, 1, 0], [0, 0, 0], [1, 1, 0], [0, 1, 0], [0, 1, 0],
])
y = np.array([1, 1, 0, 0, 1, 1, 0, 1, 0, 0])
print(f"{len(y)} animals, {int(y.sum())} of them cats")

# %% SECTION: entropy
def entropy(y):
    """H(p) = -p log2 p - (1-p) log2 (1-p), with 0 log 0 taken as 0."""
    if len(y) == 0:
        return 0.0
    p = float(np.mean(y))
    if p in (0.0, 1.0):
        return 0.0
    return float(-p * np.log2(p) - (1 - p) * np.log2(1 - p))

print("\nentropy at a few purities:")
for cats, total in [(5, 10), (8, 10), (10, 10), (0, 10), (1, 10)]:
    yy = np.r_[np.ones(cats), np.zeros(total - cats)]
    print(f"  {cats}/{total} cats  p = {cats/total:.1f}  H = {entropy(yy):.4f}")

# %% SECTION: gain
def information_gain(X, y, feature):
    """Root entropy minus the SIZE-WEIGHTED average of the children's.

    The weighting is what stops the tree loving a tiny pure branch.
    """
    left = y[X[:, feature] == 1]
    right = y[X[:, feature] == 0]
    w_left = len(left) / len(y)
    w_right = len(right) / len(y)
    return entropy(y) - (w_left * entropy(left) + w_right * entropy(right))

print(f"\nroot entropy: {entropy(y):.4f}")
print("information gain per feature:")
for j, name in enumerate(FEATURES):
    left, right = y[X[:, j] == 1], y[X[:, j] == 0]
    print(f"  {name:11s} left {len(left)} ({int(left.sum())} cats, H={entropy(left):.4f})"
          f"  right {len(right)} ({int(right.sum())} cats, H={entropy(right):.4f})"
          f"  gain = {information_gain(X, y, j):.4f}")
best = max(range(3), key=lambda j: information_gain(X, y, j))
print(f"-> split on {FEATURES[best]}")

# %% SECTION: build
def build(X, y, depth=0, max_depth=3, min_samples=1, used=()):
    """Recursively split until pure, out of features, or out of depth."""
    if entropy(y) == 0 or depth >= max_depth or len(y) <= min_samples:
        return {"leaf": True, "predict": int(round(float(np.mean(y)))),
                "n": len(y), "cats": int(y.sum())}
    candidates = [j for j in range(X.shape[1]) if j not in used]
    if not candidates:
        return {"leaf": True, "predict": int(round(float(np.mean(y)))),
                "n": len(y), "cats": int(y.sum())}
    j = max(candidates, key=lambda k: information_gain(X, y, k))
    gain = information_gain(X, y, j)
    if gain <= 1e-12:                       # no split helps: stop
        return {"leaf": True, "predict": int(round(float(np.mean(y)))),
                "n": len(y), "cats": int(y.sum())}
    mask = X[:, j] == 1
    return {
        "leaf": False, "feature": j, "gain": gain, "n": len(y),
        "yes": build(X[mask], y[mask], depth + 1, max_depth, min_samples, used + (j,)),
        "no":  build(X[~mask], y[~mask], depth + 1, max_depth, min_samples, used + (j,)),
    }

def show(node, indent="", label="root"):
    if node["leaf"]:
        print(f"{indent}{label}: LEAF -> {'CAT' if node['predict'] else 'NOT CAT'} "
              f"({node['cats']}/{node['n']} cats)")
    else:
        print(f"{indent}{label}: {FEATURES[node['feature']]}?  "
              f"(n={node['n']}, gain={node['gain']:.4f})")
        show(node["yes"], indent + "    ", "yes")
        show(node["no"], indent + "    ", "no")

tree = build(X, y)
print("\nthe tree:")
show(tree)

# %% SECTION: predict
def predict_one(node, x):
    while not node["leaf"]:
        node = node["yes"] if x[node["feature"]] == 1 else node["no"]
    return node["predict"]

def predict(node, X):
    return np.array([predict_one(node, x) for x in X])

pred = predict(tree, X)
print(f"\ntraining accuracy: {(pred == y).mean():.2f}  ({(pred == y).sum()}/{len(y)})")
print("predictions:", pred)
print("actual     :", y)

# %% SECTION: continuous
def best_threshold(values, y):
    """For a continuous feature, try every midpoint between sorted values."""
    order = np.argsort(values)
    v, yy = values[order], y[order]
    best_gain, best_t = -1.0, None
    for i in range(len(v) - 1):
        if v[i] == v[i + 1]:
            continue
        t = (v[i] + v[i + 1]) / 2
        left, right = yy[v <= t], yy[v > t]
        g = entropy(yy) - (len(left) / len(yy) * entropy(left)
                           + len(right) / len(yy) * entropy(right))
        if g > best_gain:
            best_gain, best_t = g, t
    return best_t, best_gain

weight = np.array([7.2, 8.8, 15.0, 9.2, 8.4, 7.6, 11.0, 10.2, 18.0, 20.0])
t, g = best_threshold(weight, y)
print(f"\ncontinuous feature (weight): best threshold {t:.2f} kg, gain {g:.4f}")
print(f"  tried {len(np.unique(weight)) - 1} candidate midpoints")

# %% SECTION: overfit
# Grow it without limits on noisy data and watch training accuracy hit 1.0
rng = np.random.default_rng(1)
Xn = rng.integers(0, 2, size=(40, 6))
yn = rng.integers(0, 2, size=40)                  # labels are pure noise
print("\npure-noise data, 40 examples, 6 binary features:")
print(f"{'max depth':>10} {'train acc':>10}")
for d in [1, 2, 3, 6]:
    t2 = build(Xn, yn, max_depth=d, used=())
    print(f"{d:10d} {(predict(t2, Xn) == yn).mean():10.3f}")
print("Training accuracy climbs towards 1.0 on data with no signal at all.")
print("That is overfitting in its purest form — and why depth limits exist.")
