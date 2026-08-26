"""A neural network's forward pass from scratch — C2 W1 in NumPy.

Run me:  python3 03_neural_net_forward.py

Builds up from one neuron to a whole network, then shows the loop version and
the matrix version giving identical numbers.
"""
import numpy as np

def sigmoid(z):
    z = np.asarray(z, dtype=float)
    return np.where(z >= 0, 1 / (1 + np.exp(-np.abs(z))),
                    np.exp(-np.abs(z)) / (1 + np.exp(-np.abs(z))))

# %% SECTION: one_neuron
def neuron(x, w, b, g=sigmoid):
    """A neuron is a dot product wearing a squash function. That is all."""
    z = np.dot(w, x) + b
    return g(z)

x = np.array([1.0, 3.0])
print("one neuron, w=[2,-1], b=0.5, x=[1,3]")
print("  z =", np.dot([2.0, -1.0], x) + 0.5)
print("  a =", round(float(neuron(x, np.array([2.0, -1.0]), 0.5)), 6))

# %% SECTION: layer_loop
def dense_loop(a_in, W, b, g=sigmoid):
    """One layer, written the obvious way: one unit at a time.

    W is (n_in, n_out) — column j holds unit j's weights.
    """
    units = W.shape[1]
    a_out = np.zeros(units)
    for j in range(units):
        w = W[:, j]                       # this unit's weight vector
        a_out[j] = g(np.dot(w, a_in) + b[j])
    return a_out

# %% SECTION: layer_matmul
def dense(A_in, W, b, g=sigmoid):
    """The same layer for a whole batch at once.

    A_in is (m, n_in). A_in @ W is (m, n_out): every example against every
    unit, in one operation. b is (n_out,) and broadcasts down the rows.
    """
    return g(A_in @ W + b)

W1 = np.array([[1.0, -1.0, 0.5],
               [1.0,  2.0, -1.5]])       # 2 inputs -> 3 units
b1 = np.array([-1.0, 0.0, 0.25])
loop_out = dense_loop(x, W1, b1)
mat_out = dense(x.reshape(1, -1), W1, b1)[0]
print("\nloop version  :", np.round(loop_out, 6))
print("matmul version:", np.round(mat_out, 6))
print("identical:", np.allclose(loop_out, mat_out))

# %% SECTION: network
def forward(X, params, activations):
    """Run a whole network. params is [(W1,b1), (W2,b2), ...]."""
    A = X
    for (W, b), g in zip(params, activations):
        A = dense(A, W, b, g)
    return A

relu = lambda z: np.maximum(0.0, z)
W2 = np.array([[1.5], [-2.0], [1.0]])     # 3 units -> 1 output
b2 = np.array([0.5])
net = [(W1, b1), (W2, b2)]
acts = [relu, sigmoid]

batch = np.array([[1.0, 3.0], [0.0, 0.0], [-2.0, 1.0], [4.0, -1.0]])
out = forward(batch, net, acts)
print("\nbatch of 4 through a 2-3-1 network:")
for xi, oi in zip(batch, out.ravel()):
    print(f"  x = {xi}  ->  {oi:.6f}")

# %% SECTION: shapes
print("\nshape bookkeeping (the thing that actually breaks):")
A = batch
print(f"  input           {A.shape}")
for i, ((W, b), g) in enumerate(zip(net, acts), 1):
    print(f"  layer {i}: {A.shape} @ {W.shape} + {b.shape}", end="")
    A = dense(A, W, b, g)
    print(f"  ->  {A.shape}")
total = sum(W.size + b.size for W, b in net)
print(f"  total parameters: {total}")

# %% SECTION: linear_collapse
# Why activations exist: without them, depth buys nothing.
identity = lambda z: z
lin = forward(batch, net, [identity, identity])
W_eq = W1 @ W2                      # one matrix does the whole network
b_eq = b1 @ W2 + b2
collapsed = batch @ W_eq + b_eq
print("\ntwo linear layers   :", np.round(lin.ravel(), 6))
print("one equivalent layer:", np.round(collapsed.ravel(), 6))
print("identical:", np.allclose(lin, collapsed))
print("-> stacking linear layers is pointless; the non-linearity is the point.")

# %% SECTION: detectors
# What "hidden units are feature detectors" means, made concrete.
# Good roast = temperature in [180, 260] AND duration in [12, 15].
# Build four detectors by hand, then AND them in the output unit.
K = 60.0                      # how sharp each detector's step is
Wd = np.array([
    #  too cool   too hot   too short   too long
    [   -1.0,       1.0,      0.0,        0.0   ],   # temperature feeds units 1-2
    [    0.0,       0.0,     -4.0,        4.0   ],   # duration feeds units 3-4
])
bd = np.array([ 180.0,    -260.0,      48.0,      -60.0 ])
# unit 1 fires when -T + 180 > 0, i.e. T < 180.  unit 2 when T > 260.
# unit 3 when -4D + 48 > 0, i.e. D < 12.          unit 4 when D > 15.
Wout = np.array([[-K], [-K], [-K], [-K]])   # any detector firing vetoes the roast
bout = np.array([K / 2])                    # nothing firing -> sigmoid(K/2) = 1

coffee = [(Wd, bd), (Wout, bout)]
tests = np.array([[200., 13.9], [200., 17.0], [285., 12.5],
                  [175., 13.0], [220., 12.5], [259.9, 14.9]])
probs = forward(tests, coffee, [sigmoid, sigmoid]).ravel()
print("\nhand-built roast checker  (temp C, minutes) -> P(good)")
for (t, d), pr in zip(tests, probs):
    want = "good" if (180 <= t <= 260 and 12 <= d <= 15) else "bad"
    got = "good" if pr >= 0.5 else "bad"
    print(f"  {t:5.0f} C for {d:4.1f} min  ->  {pr:.4f}  {got:4s} (want {want}) "
          f"{'OK' if got == want else 'WRONG'}")

# %% SECTION: detectors_inside
# Look at what the hidden layer actually outputs — these are the detectors.
h = dense(tests, Wd, bd, sigmoid)
print("\ninside the hidden layer  [too cool, too hot, too short, too long]")
for (t, d), row in zip(tests, h):
    print(f"  {t:5.0f} C, {d:4.1f} min -> {np.round(row, 3)}")
print("\nEvery row of zeros is a good roast. The output unit is just an AND gate:")
print("it adds -60 for every detector that fires, so one firing is enough to veto.")

# Sweep a grid and see how faithfully the network reproduces the rule.
# The grid is deliberately offset so no point lands exactly on a boundary,
# where a sigmoid is genuinely 0.5 and the answer is a coin flip.
T, D = np.meshgrid(np.linspace(150.7, 300.7, 61), np.linspace(10.13, 18.13, 41))
grid = np.c_[T.ravel(), D.ravel()]
want = ((grid[:, 0] >= 180) & (grid[:, 0] <= 260) &
        (grid[:, 1] >= 12) & (grid[:, 1] <= 15))
# distance to the nearest boundary, in the units each detector actually sees
edge = np.minimum(np.minimum(np.abs(grid[:, 0] - 180), np.abs(grid[:, 0] - 260)),
                  4.0 * np.minimum(np.abs(grid[:, 1] - 12), np.abs(grid[:, 1] - 15)))

print(f"\nswept {len(grid)} grid points. Sharpening the DETECTORS (not the output):")
print(f"{'sharpness':>10} {'match':>8}   widest disagreement from the boundary")
for sharp in [1.0, 3.0, 10.0]:
    c2 = [(Wd * sharp, bd * sharp), (Wout, bout)]
    got = forward(grid, c2, [sigmoid, sigmoid]).ravel() >= 0.5
    agree = got == want
    band = edge[~agree].max() if (~agree).any() else 0.0
    print(f"{sharp:10.0f} {100 * agree.mean():7.2f}%   {band:.3f}")
print("\nA sigmoid boundary is SOFT: near the edge the unit outputs something")
print("between 0 and 1, so the AND gate is undecided. Steeper weights shrink")
print("that band but never remove it — which is exactly why the network can")
print("express 'probably good' instead of only 'good' or 'bad'.")
