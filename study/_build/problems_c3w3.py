# -*- coding: utf-8 -*-
"""C3 W3 — reinforcement learning, on the Mars rover."""
from problemkit import P, m, pre, cols

L = []
def add(*a, **k): L.append(P(*a, **k))

ROVER = ("The Mars rover lives on six states in a line. State 1 has reward "
         "<b>100</b>, state 6 has reward <b>40</b>, states 2–5 have reward <b>0</b>. "
         "States 1 and 6 are terminal. The discount is %s." % m("γ = 0.5"))

add("c3w3-p01", level=2, tag="the return",
    lesson="c3/w3-03-the-return.html",
    ask=ROVER + "<br>The rover starts in state 4 and always goes <b>left</b>. Write out the "
        "reward at each step and compute the return.",
    hint="The return is R₁ + γR₂ + γ²R₃ + … The reward is collected on arrival, so the first "
         "term is the reward of the state you start in.",
    steps=[("Path: 4 → 3 → 2 → 1", "rewards 0, 0, 0, 100"),
           ("Discount factors", "γ⁰ = 1, γ¹ = 0.5, γ² = 0.25, γ³ = 0.125"),
           ("Multiply and add", "0(1) + 0(0.5) + 0(0.25) + 100(0.125)"),
           ("Result", "12.5")],
    answer=m("return = 12.5"),
    why="Discounting is impatience made precise. That 100 is worth only 12.5 because it takes "
        "three steps to reach — and 0.5 is a very impatient discount.")

add("c3w3-p02", level=2, tag="comparing actions",
    lesson="c3/w3-04-policies.html",
    ask=ROVER + "<br>From state 4, compute the return for going <b>right</b> as well, and say "
        "which action the rover should take.",
    steps=[("Right: path 4 → 5 → 6", "rewards 0, 0, 40"),
           ("Discounts", "γ⁰ = 1, γ¹ = 0.5, γ² = 0.25"),
           ("Return", "0 + 0 + 40(0.25) = 10.0"),
           ("Compare with going left", "12.5 versus 10.0")],
    answer="Right gives %s, left gives %s — so the rover should go <b>left</b>, "
           "even though the 100 is further away." % (m("10.0"), m("12.5")),
    why="This is the whole trade-off in one comparison: a bigger reward further away versus a "
        "smaller one nearby. γ decides which wins, and it is a modelling choice you make.")

add("c3w3-p03", level=3, tag="how gamma changes the answer",
    lesson="c3/w3-03-the-return.html",
    ask="Redo the previous comparison with %s and with %s. At which γ does the "
        "rover change its mind, and what does a small γ mean about the agent's character?"
        % (m("γ = 0.9"), m("γ = 0.3")),
    hint="Left is worth 100γ³ and right is worth 40γ². Set them equal and solve for γ.",
    steps=[("γ = 0.9: left = 100(0.9)³ = 100(0.729) = 72.9", "right = 40(0.81) = 32.4 → left"),
           ("γ = 0.3: left = 100(0.027) = 2.7", "right = 40(0.09) = 3.6 → right"),
           ("Set them equal: 100γ³ = 40γ²", "divide by γ²: 100γ = 40"),
           ("Solve", "γ = 0.4"),
           ("Below γ = 0.4 the rover prefers the near reward", "above it, the far one")],
    answer="γ = 0.9 → left (72.9 vs 32.4); γ = 0.3 → right (2.7 vs 3.6). It switches at exactly "
           "%s. A small γ makes the agent <b>short-sighted</b>: it will take a small reward "
           "now over a large one later." % m("γ = 0.4"),
    why="γ is not a nuisance hyperparameter — it defines what the agent is trying to achieve. "
        "Change γ and you have changed the problem, not just the solution.")

add("c3w3-p04", level=3, tag="state-action value",
    lesson="c3/w3-06-state-action-value-function.html",
    ask=ROVER + "<br>The optimal values are %s. "
        "Compute %s and %s using %s, and state the optimal action in state 4."
        % (m("V* = [100, 50, 25, 12.5, 20, 40]"), m("Q(4, ←)"), m("Q(4, →)"),
           m("Q(s,a) = R(s) + γ max<sub>a′</sub> Q(s′, a′)")),
    hint="R(s) is the reward of the state you are leaving, which is 0 for state 4. Then add γ "
         "times the value of the state you land in.",
    steps=[("Q(4, ←) = R(4) + γV*(3)", "0 + 0.5(25) = 12.5"),
           ("Q(4, →) = R(4) + γV*(5)", "0 + 0.5(20) = 10.0"),
           ("V*(4) = max of the two", "max(12.5, 10.0) = 12.5  ✓ consistent"),
           ("The optimal action is the argmax", "left")],
    answer="%s, %s, and the optimal action is <b>left</b>."
           % (m("Q(4,←) = 12.5"), m("Q(4,→) = 10.0")),
    why="Q is the answer to “what if I take this action once, then behave optimally forever "
        "after”. That is why the greedy policy — argmax over Q — is optimal.")

add("c3w3-p05", level=3, tag="Bellman equation",
    lesson="c3/w3-08-bellman-equation.html",
    ask="Verify the Bellman equation %s at states 2, 3 and 5, "
        "given %s."
        % (m("V*(s) = max<sub>a</sub> [ R(s) + γ V*(s′) ]"),
           m("V* = [100, 50, 25, 12.5, 20, 40]")),
    steps=[("State 2: left → V*(1) = 100, right → V*(3) = 25",
            "max(0 + 0.5(100), 0 + 0.5(25)) = max(50, 12.5) = 50  ✓"),
           ("State 3: left → V*(2) = 50, right → V*(4) = 12.5",
            "max(0.5(50), 0.5(12.5)) = max(25, 6.25) = 25  ✓"),
           ("State 5: left → V*(4) = 12.5, right → V*(6) = 40",
            "max(0.5(12.5), 0.5(40)) = max(6.25, 20) = 20  ✓"),
           ("Every state agrees with the given V*", "the values are self-consistent")],
    answer="All three check out: %s, %s, %s. The optimal policy is "
           "%s — left everywhere except state 5."
           % (m("V*(2) = 50"), m("V*(3) = 25"), m("V*(5) = 20"), m("← ← ← →")),
    why="Bellman says a value equals one step of reward plus a discounted value. That single "
        "recursive fact is what lets you solve for all the values at once, and it is what "
        "the DQN loss is built from.")

add("c3w3-p06", level=2, tag="policy",
    lesson="c3/w3-04-policies.html",
    ask="Given %s and %s, write out the optimal "
        "policy %s for states 2–5, and explain why state 5 differs from its neighbours."
        % (m("V* = [100, 50, 25, 12.5, 20, 40]"), m("γ = 0.5"), m("π(s)")),
    steps=[("State 2: 0.5(100) = 50 vs 0.5(25) = 12.5", "←"),
           ("State 3: 0.5(50) = 25 vs 0.5(12.5) = 6.25", "←"),
           ("State 4: 0.5(25) = 12.5 vs 0.5(20) = 10", "← (only just)"),
           ("State 5: 0.5(12.5) = 6.25 vs 0.5(40) = 20", "→"),
           ("State 5 is one step from the 40 but four steps from the 100",
            "with γ = 0.5, distance dominates size")],
    answer="%s. State 5 goes right because the 40 is one step away while the 100 is four — "
           "and γ = 0.5 halves the value at every step." % m("π = [←, ←, ←, →] for states 2–5"),
    why="State 4 is the interesting one: 12.5 versus 10 is a narrow margin. That is the exact "
        "point where the two rewards balance, which is why it flipped at γ = 0.4 in problem 3.")

add("c3w3-p07", level=2, tag="stochastic environments",
    lesson="c3/w3-09-stochastic-environments.html",
    ask="The rover's wheels slip: it goes the commanded way with probability 0.9 and the "
        "opposite way with probability 0.1. What changes in the definition of the return, and "
        "what does the agent now maximise?",
    steps=[("With slipping, the same action from the same state gives different paths",
            "the return is a random variable"),
           ("You cannot maximise a random number", "you maximise its average"),
           ("So the objective becomes the EXPECTED return",
            "E[R₁ + γR₂ + γ²R₃ + …]"),
           ("Bellman gains an expectation over where you land",
            "Q(s,a) = R(s) + γ E[max Q(s′,a′)]"),
           ("Everything else — policies, value iteration, DQN — is unchanged in structure",
            "just averaged")],
    answer="The return becomes a <b>random variable</b>, so the agent maximises the "
           "<b>expected</b> return %s. Bellman gains an "
           "expectation over the landing state." % m("E[R₁ + γR₂ + γ²R₃ + …]"),
    why="Every real environment is stochastic. Adding the expectation is a small change on "
        "paper and the reason you must average over many episodes to evaluate a policy.")

add("c3w3-p08", level=3, tag="training a DQN",
    lesson="c3/w3-12-learning-the-state-value-function.html",
    ask="A DQN learns %s with a neural network. Describe what %s and %s are for a "
        "single training example, and identify the strange thing about this supervised "
        "learning problem." % (m("Q(s,a)"), m("x"), m("y")),
    hint="You are creating your own training targets out of the network's current guesses.",
    steps=[("x is the state and action together", "x = (s, a)"),
           ("y is what Bellman says Q should be", "y = R(s) + γ max_{a′} Q(s′, a′)"),
           ("But Q on the right is the network's own current estimate",
            "the target depends on the model being trained"),
           ("So the targets move as training proceeds", "a moving target"),
           ("Mitigations: a separate frozen target network, and soft updates",
            "the target changes slowly enough to be learnable")],
    answer="%s and %s. The strange part: the "
           "<b>label is produced by the network being trained</b>, so the targets move as "
           "learning proceeds — which is why DQN needs a frozen target network and soft "
           "updates to be stable."
           % (m("x = (s, a)"), m("y = R(s) + γ max<sub>a′</sub> Q(s′, a′)")),
    why="This is the single biggest difference from supervised learning in Courses 1 and 2. "
        "There, y was given and fixed. Here you manufacture it, and it changes underneath you.")

add("c3w3-p09", level=2, tag="epsilon-greedy",
    lesson="c3/w3-14-epsilon-greedy.html",
    ask="With %s, an agent picks a random action 5%% of the time. "
        "(a) Why not always pick the best known action? (b) Why not always act randomly? "
        "(c) Why does ε usually start high and decrease?" % m("ε = 0.05"),
    steps=[("(a) early Q estimates are nearly random guesses",
            "always-greedy locks onto whichever bad action was overestimated first"),
           ("An action never tried keeps its initial estimate forever", "never corrected"),
           ("(b) always random never exploits what it has learnt", "no improvement in behaviour"),
           ("(c) early on, the estimates are worthless so exploring is cheap",
            "start with ε near 1"),
           ("Later the estimates are good, so exploiting is worth more",
            "decay ε to about 0.01")],
    answer="(a) Early Q values are almost random, so greedy behaviour locks onto an "
           "overestimated bad action and never revisits it. (b) Pure randomness never uses "
           "what it has learnt. (c) Start high because early estimates are worthless, and "
           "decay because later estimates are worth exploiting.",
    why="This is the explore/exploit trade-off, and it has no equivalent anywhere in Courses "
        "1 and 2 — because there, the data arrived without the model's help.")

add("c3w3-p10", level=2, tag="continuous states",
    lesson="c3/w3-10-continuous-state-spaces.html",
    ask="The lunar lander's state is %s — position, velocity, angle, angular "
        "velocity, and two leg contacts. Why can you not use a table of Q values here, and "
        "what replaces it?" % m("[x, y, ẋ, ẏ, θ, θ̇, l, r]"),
    steps=[("Six of the eight numbers are continuous", "infinitely many states"),
           ("Even discretising each into just 100 buckets", "100⁶ = 10¹² entries"),
           ("And you would need to visit each one many times to estimate it",
            "impossible"),
           ("Replace the table with a function approximator", "a neural network"),
           ("The network generalises: states it has never seen but that resemble ones it has "
            "get sensible values", "which a table can never do")],
    answer="Continuous states mean infinitely many entries — discretising six dimensions into "
           "100 buckets each already gives %s cells. A <b>neural network</b> replaces the "
           "table and, crucially, <b>generalises</b> to states never visited."
           % m("10<sup>12</sup>"),
    why="Generalisation is the real reason, not just size. A table has no opinion about a "
        "state it has never seen; a network interpolates.")

add("c3w3-p11", level=3, tag="reward design",
    lesson="c3/w3-11-lunar-lander.html",
    ask="The lunar lander's reward includes a large bonus for landing on the pad, a penalty "
        "for crashing, a small penalty for firing thrusters, and a small shaping term for "
        "moving towards the pad. Explain what each is for, and what would go wrong if you "
        "gave <b>only</b> the landing bonus.",
    steps=[("Landing bonus defines the actual goal", "what success means"),
           ("Crash penalty rules out the fast wrong solution", "otherwise crashing is neutral"),
           ("Fuel penalty encourages efficiency", "and stops endless hovering"),
           ("Shaping term gives feedback on the way", "progress is rewarded, not just arrival"),
           ("With only the landing bonus, a random agent almost never lands",
            "so it almost never sees a non-zero reward"),
           ("No signal means no gradient to learn from", "training stalls entirely")],
    answer="Bonus = the goal · crash penalty = rule out the wrong solution · fuel penalty = "
           "efficiency · shaping = feedback along the way. With <b>only</b> the landing bonus "
           "the reward is almost always zero, because a random agent essentially never lands "
           "by accident — so there is nothing to learn from.",
    why="This is the <b>sparse reward problem</b>, and reward design is most of the practical "
        "difficulty in real RL. A badly shaped reward produces an agent that games it "
        "perfectly and does the wrong thing.")

add("c3w3-p12", level=1, tag="RL vs supervised",
    lesson="c3/w3-01-what-is-rl.html",
    ask="Give three concrete ways reinforcement learning differs from the supervised learning "
        "of Courses 1 and 2.",
    steps=[("1. No labelled correct action is ever provided",
            "only a reward signal, often delayed"),
           ("2. The agent's own actions determine what data it sees",
            "supervised data is fixed and independent of the model"),
           ("3. Rewards can arrive many steps after the action that earned them",
            "credit assignment across time"),
           ("A fourth: the agent must explore, deliberately taking actions it believes are "
            "worse", "no supervised analogue")],
    answer="(1) There is no correct answer per example, only a reward. (2) The agent's "
           "actions decide what data it collects. (3) Rewards are <b>delayed</b>, so credit "
           "must be assigned back across many steps.",
    why="Point (2) is why RL is so much harder in practice: a bad policy collects bad data, "
        "which trains a bad policy. Supervised learning has no such feedback loop.")

SET = dict(course="C3", week=3, title="Reinforcement learning",
           lede="Every number below comes from the six-state Mars rover in the lectures, so "
                "you can check any of them by hand. Get that tiny example completely solid "
                "and the lunar lander is the same ideas with a neural network bolted on.",
           problems=L)
