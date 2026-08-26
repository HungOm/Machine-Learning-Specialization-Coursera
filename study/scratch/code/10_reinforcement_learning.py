"""Reinforcement learning from scratch — C3 W3, on the Mars rover.

Run me:  python3 10_reinforcement_learning.py

Three algorithms on the same six-state world: value iteration (knows the
rules), Q-learning (does not), and epsilon-greedy exploration. Every number
matches the lectures, so you can check them against the slides.
"""
import numpy as np

# %% SECTION: world
# Six states in a line. State 0 pays 100, state 5 pays 40, both terminal.
N_STATES = 6
REWARD = np.array([100., 0., 0., 0., 0., 40.])
TERMINAL = {0, 5}
ACTIONS = {0: "left", 1: "right"}
GAMMA = 0.5

def step(s, a):
    """Take one action. Returns the next state."""
    return max(0, s - 1) if a == 0 else min(N_STATES - 1, s + 1)

print(f"{N_STATES} states, rewards {REWARD.tolist()}, gamma = {GAMMA}")

# %% SECTION: return_by_hand
def episode_return(start, policy, gamma=GAMMA, max_steps=20):
    """Sum of discounted rewards along one path: R0 + g*R1 + g^2*R2 + ..."""
    s, total, g = start, 0.0, 1.0
    path = [s]
    for _ in range(max_steps):
        total += g * REWARD[s]
        if s in TERMINAL:
            break
        s = step(s, policy(s))
        path.append(s)
        g *= gamma
    return total, path

for name, pol in [("always left", lambda s: 0), ("always right", lambda s: 1)]:
    r, path = episode_return(3, pol)
    print(f"\nfrom state 4, {name}: path {[p+1 for p in path]}  return {r}")

# %% SECTION: value_iteration
def value_iteration(gamma=GAMMA, tol=1e-12):
    """Sweep the Bellman equation until nothing changes.

    V*(s) = max_a [ R(s) + gamma * V*(s') ]
    """
    V = np.zeros(N_STATES)
    for sweep in range(1000):
        newV = V.copy()
        for s in range(N_STATES):
            if s in TERMINAL:
                newV[s] = REWARD[s]
            else:
                newV[s] = max(REWARD[s] + gamma * V[step(s, a)] for a in ACTIONS)
        if np.max(np.abs(newV - V)) < tol:
            V = newV
            break
        V = newV
    return V, sweep

V, sweeps = value_iteration()
print(f"\nvalue iteration converged in {sweeps} sweeps")
print("V* =", V.tolist())

# %% SECTION: q_and_policy
def q_from_v(V, gamma=GAMMA):
    Q = np.zeros((N_STATES, len(ACTIONS)))
    for s in range(N_STATES):
        for a in ACTIONS:
            Q[s, a] = REWARD[s] if s in TERMINAL else REWARD[s] + gamma * V[step(s, a)]
    return Q

Q = q_from_v(V)
print("\nstate   Q(left)   Q(right)   V*      policy")
for s in range(N_STATES):
    pol = "terminal" if s in TERMINAL else ACTIONS[int(Q[s].argmax())]
    print(f"{s+1:5d} {Q[s,0]:9.3f} {Q[s,1]:10.3f} {V[s]:7.2f}   {pol}")
print("\nOptimal policy: left, left, left, right for states 2-5.")
print("State 5 goes right because the 40 is one step away and the 100 is four.")

# %% SECTION: gamma_sweep
print("\nhow gamma changes the rover's mind at state 4:")
print(f"{'gamma':>7} {'left (100)':>12} {'right (40)':>12}   choice")
for g in [0.2, 0.3, 0.4, 0.5, 0.9]:
    left, right = 100 * g ** 3, 40 * g ** 2
    print(f"{g:7.2f} {left:12.3f} {right:12.3f}   {'left' if left > right else 'right' if right > left else 'tie'}")
print("The tie is at 100g^3 = 40g^2, i.e. g = 0.4 exactly.")

# %% SECTION: q_learning
def q_learning(episodes=6000, alpha=0.1, eps=0.2, gamma=GAMMA, seed=0):
    """Learn Q WITHOUT being told the rewards or the transitions.

    The agent only ever sees (state, action, reward, next state). Compare the
    result with value iteration, which was handed the whole model.
    """
    rng = np.random.default_rng(seed)
    Qh = np.zeros((N_STATES, len(ACTIONS)))
    for _ in range(episodes):
        s = int(rng.choice([1, 2, 3, 4]))          # start somewhere non-terminal
        for _ in range(30):
            a = int(rng.integers(2)) if rng.random() < eps else int(Qh[s].argmax())
            s2 = step(s, a)
            target = REWARD[s] + gamma * (REWARD[s2] if s2 in TERMINAL else Qh[s2].max())
            Qh[s, a] += alpha * (target - Qh[s, a])
            s = s2
            if s in TERMINAL:
                break
    return Qh

Qh = q_learning()
print("\nQ-learning (never told the model) vs value iteration (told everything):")
print(f"{'state':>6} {'learned L':>10} {'true L':>8} {'learned R':>10} {'true R':>8}")
for s in [1, 2, 3, 4]:
    print(f"{s+1:6d} {Qh[s,0]:10.3f} {Q[s,0]:8.3f} {Qh[s,1]:10.3f} {Q[s,1]:8.3f}")
learned_pol = [ACTIONS[int(Qh[s].argmax())] for s in [1, 2, 3, 4]]
true_pol = [ACTIONS[int(Q[s].argmax())] for s in [1, 2, 3, 4]]
print(f"\nlearned policy: {learned_pol}")
print(f"true policy   : {true_pol}")
print(f"match: {learned_pol == true_pol}")

# %% SECTION: exploration
print("\nwhy epsilon matters — same algorithm, different exploration:")
print(f"{'epsilon':>8} {'policy found':>34}  correct")
for eps in [0.0, 0.05, 0.2, 1.0]:
    qh = q_learning(episodes=3000, eps=eps, seed=1)
    pol = [ACTIONS[int(qh[s].argmax())] for s in [1, 2, 3, 4]]
    print(f"{eps:8.2f} {str(pol):>34}  {pol == true_pol}")
print("\nEpsilon = 0 is pure greed: whichever action looked good first is the")
print("only one ever tried again, so the other one keeps its initial estimate")
print("forever. Epsilon = 1 explores perfectly but never exploits what it learnt")
print("-- though for Q-learning that still finds the right Q, just inefficiently.")
