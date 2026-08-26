"""Backpropagation from scratch — C2 W2, with no autodiff anywhere.

Run me:  python3 04_backprop.py

Every gradient here is derived by hand and then checked numerically. The
network learns XOR, which is the smallest problem a linear model cannot solve.
"""
import numpy as np

rng = np.random.default_rng(0)

def sigmoid(z):
    return np.where(z >= 0, 1 / (1 + np.exp(-np.abs(z))),
                    np.exp(-np.abs(z)) / (1 + np.exp(-np.abs(z))))

# %% SECTION: one_node
# Start with the smallest possible graph:  a = wx + b,  J = (a - y)^2
w, b, x, y = 3.0, 1.0, 2.0, 5.0
a = w * x + b
J = (a - y) ** 2
dJ_da = 2 * (a - y)          # derivative of the square
dJ_dw = dJ_da * x            # chain rule: da/dw = x
dJ_db = dJ_da * 1            # da/db = 1
print("forward :  a =", a, " J =", J)
print("backward:  dJ/da =", dJ_da, " dJ/dw =", dJ_dw, " dJ/db =", dJ_db)
eps = 1e-6
num = (((w + eps) * x + b - y) ** 2 - ((w - eps) * x + b - y) ** 2) / (2 * eps)
print("numeric dJ/dw =", round(num, 6), " -> matches:", abs(num - dJ_dw) < 1e-5)

# %% SECTION: derivatives
# The three derivatives every backward pass in this course is built from.
def d_sigmoid(a):
    """Given the OUTPUT a of a sigmoid, its derivative is a(1-a).

    Expressing it in terms of a rather than z is why the forward pass caches
    its activations: the backward pass reuses them instead of recomputing.
    """
    return a * (1 - a)

def d_relu(z):
    return (z > 0).astype(float)

for a in [0.1, 0.5, 0.9]:
    print(f"  sigmoid output {a}  ->  slope {d_sigmoid(a):.4f}")
print("  slope is largest at 0.5 and vanishes at both ends — that is the")
print("  saturation problem ReLU was introduced to avoid.")

# %% SECTION: forward
def forward(X, P):
    """Forward pass that CACHES everything the backward pass will need."""
    W1, b1, W2, b2 = P
    Z1 = X @ W1 + b1
    A1 = np.maximum(0.0, Z1)          # ReLU hidden layer
    Z2 = A1 @ W2 + b2
    A2 = sigmoid(Z2)                  # sigmoid output
    return A2, (X, Z1, A1, Z2, A2)

def cost(A2, y):
    eps = 1e-12
    f = np.clip(A2.ravel(), eps, 1 - eps)
    return float(-np.mean(y * np.log(f) + (1 - y) * np.log(1 - f)))

# %% SECTION: backward
def backward(cache, y, P):
    """Derived by hand, right to left.

    The one piece of magic: for a sigmoid output with log loss, dJ/dZ2
    simplifies all the way down to (A2 - y)/m. The sigmoid's derivative and
    the log's derivative cancel exactly. That cancellation is why this pair
    is always used together.
    """
    X, Z1, A1, Z2, A2 = cache
    W1, b1, W2, b2 = P
    m = X.shape[0]

    dZ2 = (A2 - y.reshape(-1, 1)) / m          # (m, 1)
    dW2 = A1.T @ dZ2                           # (h, m) @ (m, 1) -> (h, 1)
    db2 = dZ2.sum(axis=0)                      # (1,)

    dA1 = dZ2 @ W2.T                           # (m, 1) @ (1, h) -> (m, h)
    dZ1 = dA1 * d_relu(Z1)                     # ReLU passes gradient only where z > 0
    dW1 = X.T @ dZ1                            # (n, m) @ (m, h) -> (n, h)
    db1 = dZ1.sum(axis=0)                      # (h,)
    return [dW1, db1, dW2, db2]

# %% SECTION: gradcheck
X = np.array([[0., 0.], [0., 1.], [1., 0.], [1., 1.]])
y = np.array([0., 1., 1., 0.])                  # XOR
h = 8
def init(seed=2):
    """He initialisation: variance 2/fan_in keeps ReLU activations from dying.

    The biases are small random numbers, NOT zeros. With zero biases every
    hidden unit sees z = 0 for the input [0, 0], which is exactly the kink in
    ReLU — where the derivative does not exist and a numeric gradient check
    disagrees with the analytic one for a genuine mathematical reason.
    """
    r = np.random.default_rng(seed)
    return [r.normal(0, np.sqrt(2 / 2), (2, h)), r.normal(0, 0.1, h),
            r.normal(0, np.sqrt(2 / h), (h, 1)), r.normal(0, 0.1, 1)]

P = init()
A2, cache = forward(X, P)
grads = backward(cache, y, P)

def numeric_grads(P, i, eps=1e-6):
    g = np.zeros_like(P[i], dtype=float)
    flat = g.reshape(-1)
    for k in range(P[i].size):
        up = [p.copy() for p in P]; dn = [p.copy() for p in P]
        up[i].reshape(-1)[k] += eps
        dn[i].reshape(-1)[k] -= eps
        flat[k] = (cost(forward(X, up)[0], y) - cost(forward(X, dn)[0], y)) / (2 * eps)
    return g

print("\ngradient check — hand-derived vs numerical:")
for i, name in enumerate(["dW1", "db1", "dW2", "db2"]):
    n = numeric_grads(P, i)
    diff = np.max(np.abs(grads[i] - n))
    rel = diff / max(1e-12, np.max(np.abs(grads[i])) + np.max(np.abs(n)))
    print(f"  {name}: max abs diff {diff:.3e}   relative {rel:.3e}   "
          f"{'PASS' if rel < 1e-6 else 'FAIL'}")

# %% SECTION: relu_kink
# Now break it on purpose. Zero biases put every unit exactly on the ReLU kink
# for the input [0, 0], and the gradient check fails — correctly.
Pz = [P[0].copy(), np.zeros(h), P[2].copy(), np.zeros(1)]
_, cz = forward(X, Pz)
gz = backward(cz, y, Pz)
nz = numeric_grads(Pz, 1)
print("\nwith biases at exactly zero, db1 analytic vs numeric:")
print("  analytic:", np.round(gz[1], 6))
print("  numeric :", np.round(nz, 6))
print(f"  max diff: {np.max(np.abs(gz[1] - nz)):.3e}  <- a REAL disagreement")
print("  ReLU has no derivative at z = 0. The analytic version picks the flat")
print("  side; the numeric version averages across the kink. Neither is wrong.")
print("  This is why gradient checks on ReLU nets need biases off the kink.")

# %% SECTION: train
print("\ntraining on XOR:")
P = init(seed=2)
alpha = 1.0
for it in range(8001):
    A2, cache = forward(X, P)
    g = backward(cache, y, P)
    for k in range(4):
        P[k] = P[k] - alpha * g[k]
    if it % 2000 == 0:
        print(f"  iter {it:5d}  cost {cost(A2, y):.6f}")

A2, _ = forward(X, P)
print("\n  input    target   predicted")
for xi, yi, pi in zip(X, y, A2.ravel()):
    print(f"  {xi}   {yi:.0f}       {pi:.4f}   {'OK' if (pi >= .5) == (yi == 1) else 'WRONG'}")

# %% SECTION: why_hidden
# XOR is not linearly separable — prove a network with NO hidden layer fails.
print("\nsame problem with no hidden layer (plain logistic regression):")
w1, b1 = np.zeros(2), 0.0
for _ in range(20000):
    f = sigmoid(X @ w1 + b1)
    err = f - y
    w1 -= 1.0 * (X.T @ err) / len(y)
    b1 -= 1.0 * err.mean()
pred = sigmoid(X @ w1 + b1)
print("  predictions:", np.round(pred, 4), " -> all stuck near 0.5")
print(f"  accuracy {(((pred >= .5).astype(float)) == y).mean():.2f} — no better than guessing.")
print("  The hidden layer is not an optimisation. It is what makes XOR solvable.")
