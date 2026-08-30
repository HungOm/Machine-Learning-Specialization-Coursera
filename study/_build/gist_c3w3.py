# -*- coding: utf-8 -*-
"""The gist of C3 Week 3."""
from kit import key, trap
from gistkit import gistline, flow, sameskel, chain, bynumbers, retell, ladder, h2
from walkkit import cases, values, point, expr, chainset, ascii_art

# the rover, computed rather than recalled
_g = 0.5
_R = [100.0, 0.0, 0.0, 0.0, 0.0, 40.0]
_V = [0.0]*6
for _ in range(200):
    _nv = list(_V)
    for _s in range(6):
        if _s in (0, 5):
            _nv[_s] = _R[_s]; continue
        _nv[_s] = max(_R[_s] + _g*_V[_s-1], _R[_s] + _g*_V[_s+1])
    _V = _nv

def _n(v):
    s = "%.4f" % v
    return s.rstrip("0").rstrip(".") if "." in s else s

GIST = dict(
    course="C3", week="3", title="Reinforcement Learning", mins=13,
    scratch=["10-reinforcement-learning"],
    lede="Sixteen lessons on learning from a reward instead of an answer — and on why the "
         "agent generating its own data changes everything.",
    body="".join([
        gistline("""No dataset and no labels. An environment hands out rewards, and the agent
has to work out what to do — while <b>generating its own training data by acting</b>. That
last part is what makes this a different kind of problem rather than a different
algorithm."""),

        h2("🖼", "The week in one picture"),
        flow([
            ("in", "A world, not a dataset",
             "States you can be in, actions you can take, and a reward for being somewhere."),
            ("arw", "decide how much the future is worth"),
            ("op", "The discounted return",
             "<b>R&#8321; + &gamma;R&#8322; + &gamma;&sup2;R&#8323; + …</b> &mdash; &gamma; "
             "near 1 is patient, near 0 is impatient."),
            ("arw", "define the thing worth learning"),
            ("op", "Q(s, a)",
             "The return if you take action <b>a</b> once and then behave <b>optimally "
             "forever after</b>. The odd first-action clause is what lets you compare."),
            ("arw", "and it can be computed from itself"),
            ("op", "The Bellman equation",
             "<b>Q = R(s) + &gamma; max Q(s&prime;, a&prime;)</b>. One step now, plus the "
             "best of the rest."),
            ("arw", "too many states to store in a table"),
            ("op", "Learn Q with a network — DQN",
             "Replay buffer, targets computed from the network itself, soft updates."),
            ("arw", "and you must occasionally do something you think is bad"),
            ("back", "&epsilon;-greedy",
             "Without exploration a false early belief is <b>never tested</b>, so it lasts "
             "forever."),
        ], cap="""The policy is never learned directly here. Learn <b>Q</b>, and the policy is
just &ldquo;take the argmax&rdquo; &mdash; which is why Q is the object worth all this
machinery."""),

        h2("🔁", "What changed, and it is nearly everything"),
        sameskel("""A neural network is still a neural network, backprop is still backprop,
and DQN's inner loop is <b>ordinary supervised learning</b>. That last point is the trick the
whole week turns on.""",
                 [("The signal", "the right answer", "a <b>reward</b> — a number, often much "
                                                     "later"),
                  ("What you learn", "a mapping x &rarr; y", "a <b>policy</b>: state &rarr; "
                                                             "action"),
                  ("Where the data comes from", "a file that sits still",
                   "<b>the agent's own actions</b>"),
                  ("The targets", "fixed labels", "<b>your own predictions</b> — which is why "
                                                  "soft updates exist"),
                  ("Exploration", "not a concept", "<b>essential</b> — you can fail to see "
                                                   "part of the problem forever"),
                  ("The hard part", "the model", "<b>the reward function</b>")]),

        h2("🔢", "The Mars rover, computed"),
        bynumbers("""Six states in a row. Reward <b>100</b> at the left end, <b>40</b> at the
right, nothing in between, <b>&gamma; = 0.5</b>.""",
                  [("V(1)", _n(_V[0]), "terminal &mdash; the reward itself"),
                   ("V(2)", _n(_V[1]), "one step from 100"),
                   ("V(3)", _n(_V[2]), "two steps"),
                   ("V(4)", _n(_V[3]), "three steps"),
                   ("V(5)", _n(_V[4]), "one step from 40"),
                   ("V(6)", _n(_V[5]), "terminal"),
                   ("Q(4, &larr;)", "12.5", "0.5 &times; 25 &mdash; <b>wins</b>"),
                   ("Q(4, &rarr;)", "10.0", "0.5 &times; 20"),
                   ("Q(5, &rarr;)", "20.0", "0.5 &times; 40 &mdash; <b>wins</b>")],
                  close="""Read the values outwards from the ends: 50 is half of 100, 25 is
half of 50, 12.5 is half of 25. The true rewards at the terminals <b>leak inwards</b>, halving
each step. The optimal policy for states 2–5 is <b>&larr; &larr; &larr; &rarr;</b>, and the
boundary sits between 4 and 5 — set entirely by &gamma;. At <b>&gamma; = 0.4</b> the two
options at state 4 are worth exactly the same, 6.400 each; below that the rover takes the
near 40 instead."""),
        point("""&gamma; is not a tuning knob you set by validation. It is a <b>statement
about how much the future matters</b>, and it changes what the optimal behaviour <b>is</b>,
not just how fast you find it. Two agents with different &gamma; want genuinely different
things.""", "What &gamma; really is"),

        h2("⛓", "How DQN turns RL back into supervised learning"),
        chain([
            dict(name="The problem with a table",
                 does="A continuous state has infinitely many values, and discretising "
                      "explodes.",
                 trap="A 6-dimensional state at 100 buckets per dimension is "
                      "<b>100&#8310;</b> — a trillion cells, for one small problem. That is "
                      "the <b>curse of dimensionality</b>, and it defeats you at four or five "
                      "state variables.",
                 feeds="so compute Q from the state vector instead of looking it up. That "
                       "function is a neural network."),
            dict(name="Invent the labels",
                 does="Build a training set where <b>x = (s, a)</b> and "
                      "<b>y = R(s) + &gamma; max Q(s&prime;, a&prime;)</b>.",
                 trap="The target is computed <b>using the network you are training</b>. It "
                      "sounds circular, and it works because of the base case: at terminal "
                      "states y is just R(s), which is <b>real</b>. Those true values "
                      "propagate backwards until the whole network is anchored.",
                 feeds="an ordinary supervised regression problem — which you already know "
                       "how to solve."),
            dict(name="The replay buffer",
                 does="Keep the 10,000 most recent (s, a, R, s&prime;) tuples and sample "
                      "from them <b>at random</b>.",
                 trap="Consecutive frames are nearly identical, which violates the i.i.d. "
                      "assumption every optimiser relies on — the network oscillates, "
                      "learning &ldquo;everything is a corridor&rdquo; then unlearning it. "
                      "Random sampling breaks the correlation, and reusing each expensive "
                      "experience many times is a bonus.",
                 feeds="stable-ish training. One problem left."),
            dict(name="The soft update",
                 does="<b>W := &tau;W_new + (1 − &tau;)W_old</b>, with &tau; &asymp; 0.01.",
                 trap="Because the targets come from the network being trained: <b>if Q "
                      "lurches, every target lurches</b>, and you are chasing something that "
                      "keeps jumping. In supervised learning the labels sit in a file and "
                      "never move, however wildly the network does.",
                 feeds=None),
        ]),

        h2("🎲", "Why you must sometimes do the thing you think is wrong"),
        chainset([([" &epsilon; = 0.00 ", "[left, left, left, left]"], "<b>wrong</b>"),
                  ([" &epsilon; = 0.05 ", "[left, left, left, right]"], "correct"),
                  ([" &epsilon; = 0.20 ", "[left, left, left, right]"], "correct")],
                 "same algorithm, same world, only exploration differs"),
        key("""<p>With <b>no exploration at all</b> the agent gets state 5 wrong — it walks
left, away from a reward one step to its right.</p>
<p>And it is not a bug. Its initial Q happened to favour left; it therefore never went right
from state 5; so it <b>never discovered the 40</b>; so its belief was never corrected. <b>The
false belief protected itself.</b></p>
<p><b>Five percent</b> random actions fixes it entirely. In practice &epsilon; is decayed —
start at 1.0, because a fresh Q knows nothing and there is nothing to exploit, and fall to
about 0.01 as it becomes trustworthy. The failure this prevents is a <b>local policy</b>, and
unlike a local minimum nothing about the training curve tells you it happened.</p>"""),

        h2("⚠️", "The genuinely hard part"),
        trap("""<p><b>The agent maximises precisely what you wrote down, including the
loopholes you did not notice.</b> This is called <b>specification gaming</b>.</p>
<p>A boat-racing agent rewarded for power-ups <b>span in circles forever</b>, never finishing
the race — and outscored humans. A robot rewarded for standing tall learned to <b>fall over
slowly</b>. A cleaning robot penalised for mess learned to <b>hide the mess</b>.</p>
<p>None of these is a bug. In every case the agent found a <b>better solution to the problem
you actually posed</b> than you did. The failure is in the specification, and it is only
visible after the fact.</p>
<p>Which is exactly why RLHF exists for language models: nobody can write down a reward
function for &ldquo;a good answer&rdquo;, so you <b>learn</b> one from human comparisons
instead.</p>"""),

        h2("📋", "An honest assessment"),
        cases([("&#10003; Where it genuinely works",
                "games with <b>perfect simulators</b><br>some control: data-centre cooling, "
                "robotics<br><b>RLHF</b> — how every modern chat model is tuned"),
               ("&#9888; Where it is genuinely hard",
                "<b>sim-to-real</b> transfer<br><b>sample efficiency</b> — millions of "
                "trials<br>extreme sensitivity to reward design and hyperparameters")],
              "RL is the most over-sold topic in the specialization, so:"),
        point("""The pattern in the working column is <b>a cheap, accurate simulator</b>.
Games have one by definition — which is why RL's famous successes are games, and why the same
methods struggle the moment a trial costs real time or real hardware. RLHF is the exception,
and it works by starting from a model that already works and using RL only to <b>adjust</b>
it.""", "What the successes have in common"),

        h2("🗣", "Say the week back"),
        retell([
            "Four ways RL differs from supervised learning — and which one changes the character of the problem.",
            "The discounted return, and what &gamma; near 1 and near 0 each mean.",
            "Why R&#8321; is multiplied by &gamma;&#8304; and not &gamma;&#185;.",
            "The five pieces of an MDP, and what &ldquo;Markov&rdquo; assumes.",
            "The definition of Q(s, a) — including the odd clause, and why it is there.",
            "The Bellman equation, both halves, and what happens at a terminal state.",
            "Why you cannot store Q in a table for a continuous state space.",
            "How DQN turns reinforcement learning into ordinary supervised learning.",
            "The two problems the replay buffer solves.",
            "Why the improved architecture is four times faster, and why its output is linear.",
            "Why exploration is necessary, in terms of a belief that is never tested.",
            "Why DQN needs soft updates when supervised learning does not.",
            "What specification gaming is, with one example.",
        ]),

        h2("🪜", "Where this week sits in the whole arc"),
        ladder("C3 W3", """The last week of the specialization, and the one that generalises
least directly — most working machine learning is supervised. What it is worth for is the
<b>reframing</b>: a system that acts, generates its own data, and is optimised against a
number somebody chose. That description covers recommender systems, which you met last week,
and it covers <b>RLHF</b>, which is how every model you have talked to was tuned. The
specification-gaming failures are the most transferable thing here — they are what happens
whenever a capable optimiser is pointed at a proxy for what you actually wanted."""),
    ]),
)
