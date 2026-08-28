"""What happens after the model works -- versioning, skew, drift, rollout.

Run me:  python3 14_mlops.py

Everything in files 01 to 13 ends the moment the model is good. That is roughly
the halfway point. This file is about the other half: knowing exactly what you
shipped, noticing when the world moves underneath it, and changing it without
breaking anything. None of it is clever. All of it is the part that fails.
"""
import hashlib
import json

import numpy as np

rng = np.random.default_rng(3)

# %% SECTION: task
# A loan-approval-shaped problem: two features, one binary decision. Small
# enough to see everything, structured enough that the failures below are real.
def make(n, seed, income_shift=0.0, rule_shift=0.0):
    r = np.random.default_rng(seed)
    income = r.normal(50 + income_shift, 15, n)
    years = r.normal(6, 3, n)
    score = 0.06 * (income - 50) + (0.30 + rule_shift) * (years - 6)
    y = (score + r.normal(0, 0.7, n) > 0).astype(int)
    return np.column_stack([income, years]), y

X_tr, y_tr = make(4000, 1)
X_te, y_te = make(4000, 2)
print("features: income (mean %.1f) and years (mean %.1f)"
      % (X_tr[:, 0].mean(), X_tr[:, 1].mean()))
print("approval rate in training data: %.3f" % y_tr.mean())

# %% SECTION: train
def standardise(X, mu=None, sd=None):
    """Returns the stats as well as the data. Those stats are PART OF THE MODEL
    and the single most commonly lost artefact in this whole file."""
    if mu is None:
        mu, sd = X.mean(0), X.std(0)
    return (X - mu) / sd, mu, sd

def fit(X, y, epochs=400, lr=0.5):
    Xs, mu, sd = standardise(X)
    w, b = np.zeros(Xs.shape[1]), 0.0
    for _ in range(epochs):
        p = 1 / (1 + np.exp(-(Xs @ w + b)))
        w -= lr * (Xs.T @ (p - y)) / len(y)
        b -= lr * float(np.mean(p - y))
    return {"w": w, "b": b, "mu": mu, "sd": sd}

def predict(model, X, mu=None, sd=None):
    """mu/sd default to the model's own. Passing different ones is the bug
    demonstrated two sections down, and it is deliberately made possible here."""
    mu = model["mu"] if mu is None else mu
    sd = model["sd"] if sd is None else sd
    Xs = (X - mu) / sd
    return (1 / (1 + np.exp(-(Xs @ model["w"] + model["b"]))) >= 0.5).astype(int)

CHAMP = fit(X_tr, y_tr)
BASE_ACC = float(np.mean(predict(CHAMP, X_te) == y_te))
print("weights %s  bias %.4f" % (np.round(CHAMP["w"], 4), CHAMP["b"]))
print("scaling stats mu=%s sd=%s" % (np.round(CHAMP["mu"], 3), np.round(CHAMP["sd"], 3)))
print("test accuracy: %.4f" % BASE_ACC)

# %% SECTION: registry
def fingerprint(a):
    """A stable hash of an array. Same numbers in, same 12 characters out."""
    return hashlib.sha256(np.ascontiguousarray(a, dtype=np.float64).tobytes()
                          ).hexdigest()[:12]

def register(model, X, y, note):
    """A version is not a number someone increments. It is a hash of everything
    that could change the answer: the data, the weights, the scaling stats.

    'Which model made this decision' has to be answerable months later, from a
    log line, with no access to whoever trained it.
    """
    manifest = {
        "data": fingerprint(np.column_stack([X, y])),
        "weights": fingerprint(np.concatenate([model["w"], [model["b"]]])),
        "scaler": fingerprint(np.concatenate([model["mu"], model["sd"]])),
        "n_train": int(len(X)), "note": note,
    }
    manifest["version"] = hashlib.sha256(
        json.dumps(manifest, sort_keys=True).encode()).hexdigest()[:12]
    return manifest

REG = {}
m1 = register(CHAMP, X_tr, y_tr, "champion")
REG[m1["version"]] = (m1, CHAMP)
print(json.dumps(m1, indent=2))
again = register(fit(X_tr, y_tr), X_tr, y_tr, "champion")
print("\nretrained on identical data -> version %s  (same: %s)"
      % (again["version"], again["version"] == m1["version"]))
X2 = X_tr.copy(); X2[0, 0] += 0.001
changed = register(fit(X2, y_tr), X2, y_tr, "champion")
print("one feature nudged by 0.001 -> version %s  (same: %s)"
      % (changed["version"], changed["version"] == m1["version"]))
print("That sensitivity is the point. If a version can stay the same while the")
print("data changed, the version is decoration.")

# %% SECTION: skew
# The most expensive bug in this file, and the quietest.
serve_X, serve_y = make(4000, 5, income_shift=12.0)
right = float(np.mean(predict(CHAMP, serve_X) == serve_y))
mu_s, sd_s = serve_X.mean(0), serve_X.std(0)
wrong = float(np.mean(predict(CHAMP, serve_X, mu=mu_s, sd=sd_s) == serve_y))
print("serving traffic where incomes run %.1f higher than training"
      % (serve_X[:, 0].mean() - X_tr[:, 0].mean()))
print("  scaled with the TRAINING mu/sd (correct): %.4f" % right)
print("  scaled with stats recomputed at serve time: %.4f" % wrong)
print("  difference: %.1f accuracy points" % (100 * (right - wrong)))
print("\nThe second version throws no error, returns sensible-looking")
print("probabilities and passes every unit test that checks output shape. The")
print("weights were learned in the training data's units; recomputing mu and sd")
print("silently changes what every weight means. This is training/serving skew,")
print("and the only reliable defence is that ONE piece of code does the")
print("transform for both paths.")

# %% SECTION: drift
def psi(expected, actual, bins=10):
    """Population Stability Index: how far a distribution has moved.

    Bin the reference sample, count both samples into those bins, and sum
    (a-e)*log(a/e). The rules of thumb everyone uses: under 0.1 nothing,
    0.1-0.25 worth a look, above 0.25 investigate. They are conventions, not
    theorems -- calibrate them against your own history before trusting them.
    """
    edges = np.quantile(expected, np.linspace(0, 1, bins + 1))
    edges[0], edges[-1] = -np.inf, np.inf
    e = np.histogram(expected, edges)[0] / len(expected)
    a = np.histogram(actual, edges)[0] / len(actual)
    e, a = np.maximum(e, 1e-6), np.maximum(a, 1e-6)
    return float(np.sum((a - e) * np.log(a / e)))

print("  month  income PSI  years PSI   accuracy")
for month, shift in enumerate([0, 2, 5, 9, 14, 20], start=1):
    Xm, ym = make(4000, 100 + month, income_shift=shift)
    print("   %2d      %.4f     %.4f     %.4f"
          % (month, psi(X_tr[:, 0], Xm[:, 0]), psi(X_tr[:, 1], Xm[:, 1]),
             float(np.mean(predict(CHAMP, Xm) == ym))))
print("Income moves, years does not, and PSI says so per feature. Per-feature")
print("is the useful granularity: 'something drifted' is not actionable.")

# %% SECTION: false_alarm
# Now the two cases that make naive drift monitoring untrustworthy.
X_alarm, y_alarm = make(4000, 41, income_shift=25.0)
X_quiet, y_quiet = make(4000, 42, rule_shift=-0.55)
print("A. inputs move a long way:")
print("     income PSI %.4f, years PSI %.4f, accuracy %.4f (was %.4f)"
      % (psi(X_tr[:, 0], X_alarm[:, 0]), psi(X_tr[:, 1], X_alarm[:, 1]),
         float(np.mean(predict(CHAMP, X_alarm) == y_alarm)), BASE_ACC))
print("B. inputs identical, the RULE changes -- years now matters far less:")
print("     income PSI %.4f, years PSI %.4f, accuracy %.4f (was %.4f)"
      % (psi(X_tr[:, 0], X_quiet[:, 0]), psi(X_tr[:, 1], X_quiet[:, 1]),
         float(np.mean(predict(CHAMP, X_quiet) == y_quiet)), BASE_ACC))
print("\nA is a loud alarm about a model that is still fine. B is real damage")
print("with every input monitor reading zero. Input drift is a proxy for the")
print("thing you care about, and a weak one in both directions.")
print("Drift detection tells you the world moved. Only labels tell you the")
print("model is wrong, and labels are exactly what arrives late.")

# %% SECTION: delayed_labels
# Loans do not default the same afternoon. What can you watch meanwhile?
print("  week  approval rate  mean score  accuracy (known 90 days later)")
for week, rs in enumerate([0.0, -0.15, -0.30, -0.45, -0.55], start=1):
    Xw, yw = make(4000, 200 + week, rule_shift=rs)
    Xs = (Xw - CHAMP["mu"]) / CHAMP["sd"]
    prob = 1 / (1 + np.exp(-(Xs @ CHAMP["w"] + CHAMP["b"])))
    print("   %2d       %.4f        %.4f       %.4f"
          % (week, float((prob >= 0.5).mean()), float(prob.mean()),
             float(np.mean(predict(CHAMP, Xw) == yw))))
print("The approval rate is available the instant you make a prediction; the")
print("accuracy is not available for three months. Watch what you can see, and")
print("be honest that it is a proxy: a stable approval rate is consistent with")
print("a model that has quietly stopped working.")

# %% SECTION: canary
def bootstrap_diff(a_correct, b_correct, n_boot=2000, seed=0):
    """Is the challenger really better, or did it get a lucky slice of traffic?

    Resample the same users repeatedly and look at the spread of the
    difference. If the interval straddles zero, you have not measured anything.
    """
    r = np.random.default_rng(seed)
    n = len(a_correct)
    idx = r.integers(0, n, size=(n_boot, n))
    diffs = b_correct[idx].mean(1) - a_correct[idx].mean(1)
    return float(diffs.mean()), float(np.quantile(diffs, 0.025)), float(np.quantile(diffs, 0.975))

# The world has changed the way section B changed it -- the rule moved, not the
# inputs -- so retraining on recent traffic really should help. The question is
# whether you can PROVE it before you ship it.
RULE = -0.20
X_new, y_new = make(6000, 77, rule_shift=RULE)
CHALLENGER = fit(np.vstack([X_tr, X_new[:3000]]), np.concatenate([y_tr, y_new[:3000]]))
m2 = register(CHALLENGER, X_new, y_new, "challenger: retrained on recent traffic")
REG[m2["version"]] = (m2, CHALLENGER)

live_X, live_y = make(8000, 88, rule_shift=RULE)
a_ok = (predict(CHAMP, live_X) == live_y).astype(float)
b_ok = (predict(CHALLENGER, live_X) == live_y).astype(float)
truth = float(b_ok.mean() - a_ok.mean())
print("champion %.4f, challenger %.4f on all %d live users -> true gain %+.4f"
      % (a_ok.mean(), b_ok.mean(), len(live_y), truth))
print("Now pretend you do not know that number, and read it off a canary:")
for frac in [0.005, 0.025, 0.125, 0.5, 1.00]:
    n = int(frac * len(live_y))
    d, lo, hi = bootstrap_diff(a_ok[:n], b_ok[:n])
    ship = "ship" if lo > 0 else ("roll back" if hi < 0 else "keep waiting")
    print("  %5.1f%% of traffic (%4d users): %+.4f  95%% CI [%+.4f, %+.4f]  -> %s"
          % (100 * frac, n, d, lo, hi, ship))
print("\nOne challenger, one true effect of %+.4f, and the answer changes with"
      % truth)
print("The small ones are not wrong about the")
print("data they saw -- they are being asked a question their sample cannot")
print("answer, and 'keep waiting' is the correct reading of a CI that straddles")
print("zero. Deciding on a point estimate instead would have shipped or blocked")
print("this model on a coin flip.")
print("Work out the traffic you need BEFORE the canary, from the smallest gain")
print("you would actually act on. A canary that cannot resolve that gain is not")
print("a safety measure, it is a delay.")

# %% SECTION: rollback
def serve(version, X):
    manifest, model = REG[version]
    return predict(model, X), manifest["version"]

print("registry holds %d versions:" % len(REG))
for v, (man, _) in REG.items():
    print("   %s  n_train=%-5d %s" % (v, man["n_train"], man["note"]))
preds, used = serve(m2["version"], live_X[:5])
print("\nserved 5 requests with %s -> %s" % (used, preds))
print("rolling back is: change one string.")
preds, used = serve(m1["version"], live_X[:5])
print("served the same 5 with %s -> %s" % (used, preds))
print("\nThat is only true because both versions are still loadable and both")
print("carry their own scaling stats. A rollback plan that requires retraining")
print("is not a rollback plan. The registry section at the top of this file is")
print("what buys you this line at the bottom.")

# %% SECTION: checklist
print("Everything above, as questions you can answer before shipping:")
for i, q in enumerate([
        "Can you name the exact data, weights and preprocessing behind any past decision?",
        "Does ONE piece of code do the feature transform for training and serving?",
        "Are the scaling statistics stored with the weights, not recomputed?",
        "Is drift measured per feature, against a fixed reference window?",
        "Do you know which of your monitors would have caught a change in P(y|x)?",
        "What do you watch in the gap before labels arrive, and what does it miss?",
        "Is your canary big enough for its confidence interval to exclude zero?",
        "Can you roll back without retraining, and has anyone tried it recently?"], 1):
    print("  %d. %s" % (i, q))
print("\nNone of these are modelling questions. That is the lesson: after the")
print("model works, almost nothing that goes wrong is the model's fault.")
