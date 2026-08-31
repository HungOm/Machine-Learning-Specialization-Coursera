# -*- coding: utf-8 -*-
"""Active Mastery for 10_reinforcement_learning.py.

Non-duplication forced the shape of this one. The c3w3 deck already covers
RL-vs-supervised, the return, MDPs, Q, Bellman, the rover values, stochastic
environments, continuous states, DQN, replay, architecture, epsilon, soft
updates, reward design and the state of RL -- sixteen cards -- and the mock
quiz covers most of the same ground.

So this layer is weighted almost entirely to the file's EXPERIMENTS: the
gamma sweep where both actions tie at exactly 6.400, the told-nothing vs
told-everything comparison, and the exploration run that gets state 5 wrong
forever. Those are computed results, not concepts, and none of them is in
the deck.
"""
from masterykit import (section, prose, code, out, semantics, ledger, drill, peek,
                        predict, lab, breaks, invariant, wrong, reconstruct,
                        connections, recall, check)

AM = dict(
    lede="Eleven cards built almost entirely from this file's <b>experiments</b> &mdash; the "
         "exact tie at &gamma; = 0.4, and the run that is wrong forever because it never "
         "looked.",
    sections=[

section("0", "&#129517;", "Before you run", "before", kind="orient",
    hook="Six squares in a row. Every number in the file is checkable by hand.",
    body=prose("""<p>Six states, rewards <b>100</b> at the left end and <b>40</b> at the right,
nothing in between, <b>&gamma; = 0.5</b>. Small enough that you can verify every value the
file prints with a pencil.</p>
<p><b>Three experiments to watch</b>, and they are the point of the file rather than the
theory. A <b>&gamma; sweep</b> where the two actions at state 4 come out worth <i>exactly</i>
the same. A comparison between an algorithm <b>told the whole world</b> and one <b>told
nothing</b>. And an exploration run that gets a state wrong <b>permanently</b>, for a reason
that is not a bug.</p>""")
    + connections([], [], "../gist/c33.html", "C3 Week 3 &mdash; the gist",
        extra=[("lab", "../scratch/07-kmeans.html", "Contrast with 07",
                "that one has no labels; this one has no fixed dataset at all")])),

section("1", "&#127991;&#65039;", "What every variable is", "vars", kind="semantics",
    hook="Seven variables. Two are the world, three are beliefs about it, and one is a choice.",
    body=semantics([
        ("REWARD", "(6,) float64", "the reward for each state",
         "<b>The only real numbers in the system.</b> <code>[100, 0, 0, 0, 0, 40]</code> "
         "&mdash; everything else is computed backwards from these two.",
         "<i>reward units</i> &mdash; arbitrary but consistent",
         "<code>REWARD[5]</code> is 40 &mdash; the smaller prize, at the right-hand end.",
         "Change 40 to 60 and the whole policy can flip. These two numbers <b>are</b> the "
         "problem definition."),
        ("TERMINAL", "set {0, 5}", "the two end states",
         "Where an episode <b>stops</b>. The base case that makes the recursion computable.",
         "<i>state indices</i>",
         "States 0 and 5 &mdash; the two rewarded squares. Reaching one ends the run.",
         "Without terminals the Bellman recursion has no anchor and the values are defined "
         "only by each other."),
        ("GAMMA", "float", "the discount",
         "<b>Not a property of the world.</b> A statement about <b>how much the future "
         "matters to you</b>, which is a choice.",
         "<i>unitless</i>, 0 to 1",
         "0.5 means a reward one step away is worth <b>half</b> as much. Aggressive "
         "impatience &mdash; real problems use 0.9&ndash;0.99.",
         "It changes what the <b>optimal behaviour is</b>, not just how fast you find it. Two "
         "agents with different &gamma; want genuinely different things."),
        ("V", "(6,) float64", "the state values",
         "<b>What each square is worth</b> if you play optimally from there.",
         "<b>same units as REWARD</b>",
         "<code>V</code> is [100, <b>50</b>, 25, 12.5, 20, 40]. Read it outwards: 50 is half "
         "of 100, 25 is half of 50 &mdash; the terminal rewards <b>leak inwards</b>, halving "
         "each step.",
         "Every value is a <b>belief</b>, not a measurement. Before value iteration runs they "
         "are all zero and all wrong."),
        ("Q", "(6, 2) float64", "the action values",
         "<b>What each action is worth from each square</b> &mdash; which is what you actually "
         "need in order to decide.",
         "<b>same units as REWARD</b>",
         "<code>Q[3]</code> is <b>[12.5, 10.0]</b>: from state 4, going left is worth 12.5 and "
         "right 10.0. <b>Narrowly</b> left.",
         "V is <code>max</code> over each row and the policy is <code>argmax</code>. That is "
         "why Q is the thing worth learning &mdash; V alone cannot tell you what to do."),
        ("ACTIONS", "dict {0:'left', 1:'right'}", "the action names",
         "The whole action space. Column 0 of Q is left, column 1 is right.",
         "<i>names</i>",
         "Purely so the printed policy reads as words. The algorithm only ever sees 0 and 1.",
         "Note the <b>column order is a convention</b> &mdash; swap the dict and every printed "
         "policy inverts while every number stays identical."),
        ("Qh", "(6, 2) float64", "the LEARNED action values",
         "<b>Q-learning's own estimate</b>, built by wandering around rather than by being "
         "told the world.",
         "<b>same units as REWARD</b>",
         "It matches <code>Q</code> to three decimals &mdash; 50.000, 25.000, 12.500, 10.000 "
         "&mdash; despite never being given <code>REWARD</code> or <code>step</code>.",
         "That agreement is the file's headline result: <b>you do not need to know the world "
         "to act optimally in it.</b>"),
    ],
    """The split worth holding: <b>REWARD, TERMINAL and the transition rule are the world</b>;
<b>V, Q and Qh are beliefs about it</b>; and <b>GAMMA is a choice you make</b>. Only the first
group is given &mdash; and Q-learning does not even get that."""),
    ),

section("2", "&#128302;", "Prediction checkpoints", "predict", kind="predict",
    hook="Four, and the second is an exact tie you can compute in your head.",
    body=predict([
        ("""From state 4, walking left reaches the 100 in three steps; walking right reaches
the 40 in two. With &gamma; = 0.5, <b>compute both returns before reading the output.</b>""",
         """<p>Left: 0.5&sup3; &times; 100 = <b>12.5</b>. Right: 0.5&sup2; &times; 40 =
<b>10.0</b>.</p>
<p>So left wins &mdash; but <b>only just</b>. The 100 is two and a half times the 40 and one
step further away, and the discount very nearly eats the whole advantage.</p>
<p>That narrowness is the setup for the next question.</p>"""),
        ("""The file sweeps &gamma; and finds one value where state 4's two actions are worth
<b>exactly the same</b>. <b>Solve for it</b> before looking: when does
&gamma;&sup3;&times;100 equal &gamma;&sup2;&times;40?""",
         """<p>Divide both sides by &gamma;&sup2;: <b>100&gamma; = 40</b>, so
<b>&gamma; = 0.4</b>.</p>
<p>And the file confirms it &mdash; at &gamma; = 0.40 both come out at <b>6.400</b>. Below it
the agent grabs the near 40; above it, it walks for the distant 100.</p>
<p>So &gamma; is not a tuning knob you find by validation. It is a <b>statement about
patience</b>, and there is a sharp value at which the optimal behaviour changes.</p>"""),
        ("""Value iteration converges in <b>4 sweeps</b>. Predict <i>why</i> four, and what
would change it.""",
         """<p>Because information travels <b>one state per sweep</b>, and the furthest any
state sits from a terminal is about four steps. State 4 cannot know about the 100 until the
news has propagated 3&rarr;2&rarr;1.</p>
<p>Widen the corridor to twelve states and it needs roughly twelve sweeps. That linear growth
is exactly why value iteration does not scale, and why file 10's later sections move to
learning Q instead of computing it.</p>"""),
        ("""Q-learning is given <b>no</b> access to <code>REWARD</code> or <code>step</code>
&mdash; it only acts and observes. Predict how close it gets to the true Q.""",
         """<p><b>Three decimal places.</b> 50.000, 25.000, 12.500, 10.000 &mdash; identical to
value iteration's answers.</p>
<p>One method was handed a complete model of the world; the other worked it out by wandering
around and remembering what happened. That is the result that makes RL interesting, because in
most real problems you could never write the world down.</p>"""),
    ],
    """The second one is worth doing algebraically. It is the only place in the lane where you
can <b>solve for</b> the exact point at which an optimal policy changes.""")),

section("3", "&#128295;", "Modify the copy", "lab", kind="lab",
    hook="Five, including the one that makes the agent permanently wrong.",
    body=lab([
        ("L1", "Change a value",
         "Raise the right-hand reward from 40 to <b>60</b> and re-run value iteration. Predict "
         "the new policy first.",
         "REWARD = np.array([100., 0., 0., 0., 0., 60.])",
         """<p>The boundary <b>moves left</b>. From state 4, right is now worth
0.5&sup2;&times;60 = <b>15</b> against left's 12.5, so state 4 flips to <b>right</b>.</p>
<p>The policy becomes &larr; &larr; &rarr; &rarr;. One number in the world definition, and a
quarter of the policy changes &mdash; which is the same sensitivity that makes reward design
the hard part of applied RL.</p>"""),
        ("L2", "Change a parameter",
         "Set <code>GAMMA = 0.9</code> &mdash; a patient agent &mdash; and re-read the whole "
         "policy.",
         "GAMMA = 0.9        # was 0.5",
         """<p>Every state now walks <b>left</b>, towards the 100. From state 5, left is worth
0.9&#8308;&times;100 = <b>65.6</b> against right's 0.9&times;40 = <b>36</b>.</p>
<p>The distant prize is now worth the walk from everywhere, so the boundary disappears off the
end of the corridor. Same world, same rewards, <b>completely different behaviour</b> &mdash;
because &gamma; changed what the agent <i>wants</i>.</p>"""),
        ("L3", "Change the data",
         "Extend the corridor to <b>10</b> states, keeping the rewards at the two ends, and "
         "count the sweeps to convergence.",
         "N_STATES = 10\nREWARD = np.array([100.] + [0.]*8 + [40.])\nTERMINAL = {0, 9}",
         """<p>It needs roughly <b>8 sweeps</b> instead of 4 &mdash; information still travels
one state per sweep, and the corridor is longer.</p>
<p>Also worth reading: with &gamma; = 0.5 the far end is now 0.5&#8311;&times;100 &asymp;
<b>0.78</b> from state 8, so the 100 is effectively invisible from there and the whole right
half walks right. <b>Discounting creates a horizon</b>, and past it the big reward may as well
not exist.</p>"""),
        ("L4", "Change an assumption",
         "Run Q-learning with <code>eps = 0.0</code> &mdash; no exploration at all &mdash; and "
         "read the policy it finds.",
         "Qh, pol = q_learning(eps=0.0)",
         """<p>It returns <b>['left', 'left', 'left', 'left']</b>, which is <b>wrong at state
5</b>: it walks left, away from a reward one step to its right.</p>
<p>And it is <b>not a bug</b>. The initial Q happened to favour left; the agent therefore
never went right from state 5; so it <b>never discovered the 40</b>; so its belief was never
corrected. <b>The false belief protected itself.</b></p>
<p>Set <code>eps = 0.05</code> and it is fixed. Five percent random actions is enough.</p>"""),
        ("L5", "Explain it",
         "Explain why value iteration needs <code>REWARD</code> and <code>step</code> but "
         "Q-learning does not &mdash; and what Q-learning pays for that.",
         None,
         """<p>Value iteration computes <b>expectations over known transitions</b>, so it must
be able to ask &ldquo;if I do this, where do I land and what do I get?&rdquo; before acting.
Q-learning instead <b>samples</b>: it takes the action, observes the outcome, and nudges its
estimate towards what it saw.</p>
<p>What it pays is <b>experience</b>. Value iteration converges in 4 sweeps of arithmetic;
Q-learning here needs <b>6,000 episodes</b> of wandering. That is the sample-efficiency
problem, and it is why RL's successes are in domains with cheap simulators.</p>"""),
    ],
    """L4 is the one to run. &ldquo;Explore a little&rdquo; sounds like a hyperparameter until
you watch an agent be permanently wrong about a state it never visited.""")),

section("4", "&#128165;", "Break it, then repair it", "break", kind="debug",
    hook="Four, and two of them converge confidently to the wrong answer.",
    body=breaks([
        ("V[s] = max(REWARD[s] + GAMMA * V[s-1],\n            REWARD[s] + GAMMA * V[s+1])\n"
         "# terminal states are no longer special-cased",
         "Let value iteration update the <b>terminal</b> states too. Predict what happens to "
         "V[0].",
         """<p>V[0] <b>grows without bound</b>. State 0 looks at its neighbour, adds its own
100, and each sweep inflates it further &mdash; there is no longer anything anchoring the
recursion.</p>
<p>The invariant: <b>at a terminal state, V(s) = R(s), full stop.</b> That is the base case,
and it is where all the real numbers enter the system. Every other value is computed backwards
from it.</p>
<p>A recursion without a base case does not error &mdash; it just produces increasing
nonsense.</p>"""),
        ("Q[s, a] = REWARD[s] + GAMMA * V[s_next]\n# ...but V was computed with a different gamma",
         "Compute V with &gamma; = 0.5, then derive Q with &gamma; = 0.9. Predict whether the "
         "policy changes.",
         """<p>The numbers all change and the <b>policy at state 4 flips</b> &mdash; because
the comparison is now between values built on <b>two different discount rates</b>.</p>
<p>Nothing errors, every number is finite and plausible, and the resulting policy is
internally inconsistent: it prefers a future it valued at one rate using a present it valued
at another.</p>
<p>The invariant: <b>one &gamma; per problem</b>. It is a property of the objective, not of a
function, so passing it as a default in three places is exactly how this bug arises.</p>"""),
        ("if np.max(np.abs(V - V_old)) < 1e-12: break      # replaced with:\nfor _ in range(2): ...",
         "Cap value iteration at <b>2</b> sweeps instead of running to convergence. Predict "
         "which states are wrong.",
         """<p>States <b>3 and 4</b> are wrong &mdash; the ones furthest from a terminal.</p>
<p>After two sweeps the news from the 100 has reached state 2 but not state 3, so V[3] is
still under-estimated and the policy derived from it can point the wrong way.</p>
<p>The invariant: <b>information travels one state per sweep</b>, so you need at least as many
sweeps as the longest distance to a terminal. Stopping early does not give you a slightly
worse answer &mdash; it gives you a <b>locally</b> wrong one, and the error is concentrated
exactly where the problem is hardest.</p>"""),
        ("Qh[s, a] += alpha * (r + gamma * Qh[s2].max() - Qh[s, a])\n"
         "# ...with s2 terminal, Qh[s2] is still being updated",
         "Let Q-learning bootstrap from a terminal state's Q instead of stopping there. What "
         "does it learn?",
         """<p>It <b>double-counts the terminal reward</b>: the agent collects 100 for arriving
<i>and</i> adds the discounted value of a state it has already finished in.</p>
<p>Values inflate steadily. The <b>policy often stays correct</b> &mdash; because everything
inflates together &mdash; so the bug hides behind a right answer, and only shows up when you
compare Qh against the true Q.</p>
<p>The invariant: <b>at a terminal, the target is just r</b> &mdash; there is no next state to
bootstrap from. That single conditional is the most commonly omitted line in a DQN
implementation.</p>"""),
    ],
    """The last two are the instructive pair: one is wrong in a way that changes the policy, the
other is wrong in a way that does not &mdash; and the second is harder to find.""")),

section("5", "&#9878;&#65039;", "The invariant", "invariant", kind="invariant",
    hook="Told everything and told nothing must agree.",
    body=invariant("""<p><b>Q-learning, given no model of the world, must converge to the same
Q that value iteration computes from a complete one &mdash; and V must equal the row-wise max
of Q.</b></p>""",
    """<p>The file checks the first by printing both side by side, and they agree to three
decimals: <b>50.000, 25.000, 12.500, 10.000</b>. One algorithm was handed <code>REWARD</code>,
<code>step</code> and <code>TERMINAL</code>; the other was handed nothing and had to wander.
Two unrelated routes to one answer is the strongest check available.</p>
<p>The second is free and catches most indexing bugs: <b>V = Q.max(axis=1)</b> and
<b>&pi; = Q.argmax(axis=1)</b>, by definition. If your V and your Q disagree, one of them was
built with the wrong neighbour.</p>
<p>And the base case: at a <b>terminal</b>, Q(s, a) = R(s) for every a &mdash; which is why
<code>Q[0]</code> is <b>[100, 100]</b> and <code>Q[5]</code> is <b>[40, 40]</b>. Both actions
are worth the same because neither happens.</p>""",
    """assert np.allclose(V, Q.max(axis=1))
assert np.allclose(Q[0], REWARD[0]) and np.allclose(Q[5], REWARD[5])
assert np.allclose(Qh[1:5], Q[1:5], atol=1e-2)      # learned vs computed
assert learned_pol == true_pol""")),

section("6", "&#129535;", "Wrong mental models", "wrong", kind="myths",
    hook="Five, and the first is why people tune gamma like a learning rate.",
    body=wrong([
        ("&gamma; is a hyperparameter you tune for performance.",
         """<p>It <b>defines the objective</b>. At &gamma; = 0.5 state 4 walks left; at
&gamma; = 0.3 it walks right; and at exactly <b>&gamma; = 0.4</b> the two are worth
<b>6.400</b> each.</p>
<p>You are not finding a better solution to the same problem &mdash; you are asking a
<b>different question</b> about how much the future is worth. Two agents with different
&gamma; want different things, and neither is more correct.</p>"""),
        ("If the agent converged, it found the best policy.",
         """<p>With <code>eps = 0.0</code> Q-learning converges perfectly and returns
<b>['left', 'left', 'left', 'left']</b> &mdash; wrong at state 5, where the reward is one step
to the right.</p>
<p>It converged to a <b>local policy</b>: its initial Q favoured left, so it never went right
from state 5, so it never saw the 40, so nothing ever corrected it. Convergence means the
updates stopped changing anything, not that the answer is right.</p>"""),
        ("Q(s,a) is how good action a is.",
         """<p>It is the return if you take a <b>once</b> and then behave <b>optimally
forever after</b>. The first action can be a silly one; everything after it is assumed
perfect.</p>
<p>That odd clause is what makes the actions <b>comparable</b> &mdash; every column of the row
shares the same &ldquo;and then play well&rdquo; assumption, so their difference is purely the
cost of that one move. Define it any other way and argmax stops meaning anything.</p>"""),
        ("More episodes always means a better policy.",
         """<p>Not without exploration. With <code>eps = 0.0</code> you can run <b>six
million</b> episodes and state 5 stays wrong, because the agent never takes the action that
would teach it.</p>
<p>Experience only helps where it is <b>gathered</b>, and a greedy policy gathers experience
only where it already believes the reward is.</p>"""),
        ("Value iteration is just a slower Q-learning.",
         """<p>They solve different problems. Value iteration <b>requires a model</b> &mdash;
it must know the rewards and transitions to compute expectations &mdash; and converges here in
<b>4 sweeps</b> of arithmetic.</p>
<p>Q-learning requires <b>no model</b> and pays for it in <b>experience</b>: 6,000 episodes of
wandering to reach the same numbers. If you have the model, computing is enormously cheaper.
Real problems usually do not, which is the entire reason Q-learning exists.</p>"""),
    ])),

section("7", "&#127959;&#65039;", "Reconstruction challenge", "reconstruct", kind="rebuild",
    hook="Rebuild both algorithms and check them against each other.",
    body=reconstruct([
        ("Explain", "In three sentences, say what value iteration does and where its numbers "
         "come from.",
         """<p>Start with a guess of zero for every state. Repeatedly replace each state's
value with the best available &ldquo;reward here plus discounted value of where I would
land&rdquo;. The only real numbers enter at the <b>terminals</b>, where the value is just the
reward, and they spread outwards one state per sweep.</p>"""),
        ("Skeleton", "Write the five signatures from memory.",
         """<p><code>step(s, a)</code>,
<code>episode_return(start, policy, gamma=GAMMA, max_steps=20)</code>,
<code>value_iteration(gamma=GAMMA, tol=1e-12)</code>,
<code>q_from_v(V, gamma=GAMMA)</code>, and
<code>q_learning(episodes=6000, alpha=0.1, eps=0.2, gamma=GAMMA, seed=0)</code>.</p>
<p>Note that <code>q_learning</code> takes <b>no reward table</b> &mdash; it only calls
<code>step</code>. That absence is the whole point.</p>"""),
        ("Core", "Write the value-iteration sweep from memory, terminal handling included.",
         """<p>For each non-terminal s: <code>V[s] = max over a of (REWARD[s] + gamma *
V[step(s,a)])</code>. For each <b>terminal</b> s: <code>V[s] = REWARD[s]</code>, and never
update it again.</p>
<p>The terminal case is the base of the recursion. Omit it and the values grow without
bound &mdash; not an error, just increasing nonsense.</p>"""),
        ("Minimal", "Build the smallest world where &gamma; changes the optimal policy, and "
         "solve for the &gamma; at which it flips.",
         """<p>Three states is enough: a big reward two steps one way and a small one one step
the other. The flip is where <b>&gamma;&sup2;&times;big = &gamma;&times;small</b>, so
<b>&gamma; = small / big</b>.</p>
<p>In this file's corridor that is 40/100 = <b>0.4</b>, and the sweep confirms both actions
worth <b>6.400</b> there.</p>"""),
        ("Verify", "Check your rebuild without comparing to the original.",
         """<p>Three self-contained checks: <code>V == Q.max(axis=1)</code>; terminal Q rows
equal the terminal reward in every column; and <b>Q-learning's answer matches value
iteration's</b> to about two decimals.</p>
<p>That last one is the real test, because the two share no code &mdash; one computes from a
model, the other samples from experience.</p>"""),
    ],
    """Building both and making them agree is the whole exercise. Either alone is easy to get
subtly wrong.""")),

section("8", "&#128279;", "Connections", "conn", kind="links",
    hook="The last file with an exact answer to check against.",
    body=connections(
        [("lab", "../scratch/07-kmeans.html", "Contrast with 07",
          "no labels there; here there is no fixed dataset at all"),
         ("lab", "../scratch/04-backpropagation.html", "Back to 04",
          "the network that replaces this Q table once the states go continuous")],
        [("lab", "../scratch/13-agent-loop.html", "On to 13",
          "another act-observe-repeat loop &mdash; with a language model choosing the action"),
         ("lab", "../scratch/14-mlops.html", "On to 14",
          "and what happens when a deployed policy changes the data it is judged on")],
        "../gist/c33.html", "C3 Week 3 &mdash; the gist",
        extra=[("docs", "../reference.html", "Reference &mdash; C3 W3",
                "<code>c3w3-rover-values</code> works the same corridor by hand")])),

section("9", "&#9670;", "Recall sheet", "recall", kind="recall",
    hook="Six cards, all computed results from this file.",
    body=recall([
        ("Solve for the &gamma; at which state 4's two actions are worth the same.",
         "&gamma;&sup3;&times;100 = &gamma;&sup2;&times;40, so 100&gamma; = 40 and "
         "<b>&gamma; = 0.4</b>. The sweep confirms both at <b>6.400</b>. Below it the agent "
         "takes the near 40; above it, the far 100."),
        ("Value iteration converges in <b>4</b> sweeps. Why four?",
         "Information travels <b>one state per sweep</b>, and the furthest state sits about "
         "four steps from a terminal. Widen the corridor and the sweep count grows with it "
         "&mdash; which is why it does not scale."),
        ("Q-learning is given no rewards and no transition function. How close does it get?",
         "<b>Three decimal places</b> &mdash; 50.000, 25.000, 12.500, 10.000, identical to "
         "value iteration. You do not need to know the world to act optimally in it."),
        ("With <code>eps = 0.0</code>, what policy does Q-learning find, and why is it not a "
         "bug?",
         "<b>['left','left','left','left']</b> &mdash; wrong at state 5. Its initial Q favoured "
         "left, so it never went right, so it never saw the 40, so nothing corrected it. "
         "<b>The false belief protected itself.</b> eps = 0.05 fixes it."),
        ("<code>Q[0]</code> is [100, 100] and <code>Q[5]</code> is [40, 40]. Why are both "
         "columns equal?",
         "They are <b>terminal</b> states, so Q(s,a) = R(s) for every a &mdash; the action "
         "never happens. That base case is where all the real numbers enter; every other value "
         "is computed backwards from it."),
        ("What are the two free checks relating V, Q and the policy?",
         "<b>V = Q.max(axis=1)</b> and <b>&pi; = Q.argmax(axis=1)</b>, by definition. If V and "
         "Q disagree, one was built with the wrong neighbour."),
    ],
    """Cover and answer aloud.""")),

section("10", "&#9989;", "Mastery check", "check", kind="check",
    hook="Five, none in the C3 W3 quiz.",
    body=check([
        ("""Solve algebraically for the &gamma; at which this corridor's optimal policy changes
at state 4, then say what that means about &gamma;.""",
         """<p>&gamma;&sup3;&times;100 = &gamma;&sup2;&times;40 gives <b>&gamma; = 0.4</b>,
where both actions are worth <b>6.400</b>.</p>
<p>It means &gamma; is <b>not</b> a performance dial. There is a sharp value at which the
optimal behaviour changes, so choosing &gamma; is choosing <b>which problem you are
solving</b> &mdash; and no amount of validation data can pick it for you.</p>"""),
        ("""Your Q-learning agent converges and its policy is stable across 10,000 more
episodes. What have you established?""",
         """<p>That the <b>updates stopped changing things</b> &mdash; nothing more.</p>
<p>With eps = 0.0 this file's agent converges stably to a policy that is <b>wrong at state
5</b>, because it never takes the action that would teach it otherwise. Stability under a
greedy policy is self-confirming: it only samples where it already believes.</p>"""),
        ("""You extend the corridor to 20 states and value iteration is slow. Explain why, and
say whether Q-learning would help.""",
         """<p>Information travels <b>one state per sweep</b>, so you need roughly 20 sweeps
rather than 4 &mdash; it grows with the diameter of the state space.</p>
<p>Q-learning would <b>not</b> help here: it needs thousands of episodes to match what value
iteration computes in a handful of sweeps. It is the right tool when you <b>lack a model</b>,
not when the model is merely large. For a large known model you want better sweeps, not
sampling.</p>"""),
        ("""Your DQN's values grow steadily larger over training but the policy looks correct.
Name the likely bug.""",
         """<p>You are <b>bootstrapping from terminal states</b> &mdash; adding
<code>gamma * max Q(s')</code> when there is no next state, so the terminal reward gets counted
twice and compounds.</p>
<p>The policy stays right because <b>everything inflates together</b>, which is exactly what
makes it hard to find. The fix is one conditional: at a terminal, the target is just
<code>r</code>.</p>"""),
        ("""Someone changes the right-hand reward from 40 to 60 and reports that &ldquo;the
model got worse&rdquo;. Correct them.""",
         """<p>The model did not get worse &mdash; <b>the problem changed</b>. At 60 the state-4
comparison becomes 12.5 against <b>15</b>, so right genuinely wins and the optimal policy is
now &larr; &larr; &rarr; &rarr;.</p>
<p>The agent is solving the world it was given, correctly. Reward numbers are the
<b>specification</b>, not hyperparameters, and this sensitivity is why reward design is the
hard part of applied RL.</p>"""),
    ],
    """None of these appears in the <a href="../quiz/c33.html">C3 W3 mock quiz</a>, which
covers the rover values, policies, Q, Bellman, &epsilon;-greedy, continuous states, the
improved architecture and soft updates.""")),
    ],
)
