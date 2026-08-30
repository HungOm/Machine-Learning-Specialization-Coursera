# -*- coding: utf-8 -*-
"""Walkthrough for 10_reinforcement_learning.py."""
from walkkit import p, expr, chain, chainset, steps, cases, values, point, ascii_art

PICTURE = ([
    ("in", "A world, not a dataset",
     "Six states in a row. Reward <b>100</b> at the left end, <b>40</b> at the right, "
     "nothing in between."),
    ("arw", "no labels &mdash; nobody says which move was right"),
    ("op", "Guess a value for every state", "Start at zero. They are all wrong."),
    ("arw", "one step of lookahead"),
    ("loop", "sweep until nothing changes", [
        ("op", "Bellman update",
         "Each state's value = the reward here + &gamma; &times; the best you can do from "
         "wherever you land."),
        ("arw", "true values leak outwards from the ends"),
    ]),
    ("out", "A value for every state, and a policy",
     "The policy is just: from here, move towards the higher neighbour."),
], "The whole program in one picture",
   "The rewards at the two ends are the only real numbers in the system. Everything else "
   "is computed backwards from them.")

WALK = {

"prelude": (
    p("""No dataset. No labels. An <b>environment</b> that hands out rewards, and an agent
that has to work out what to do.""")
    + point("""And the agent <b>generates its own training data by acting</b>. That single
difference is what makes reinforcement learning a different kind of problem: a bad early
policy produces bad experience, which teaches a bad policy.""")
),

"world": (
    p("""Six states in a row, like squares on a board.""")
    + ascii_art("""   [1]---[2]---[3]---[4]---[5]---[6]
   100    0     0     0     0     40
    ^                              ^
  terminal                     terminal""")
    + values([("rewards", "[100, 0, 0, 0, 0, 40]", "only the two ends pay anything"),
              ("&gamma;", "0.5", "each step away halves the value"),
              ("actions", "left or right", "that is the whole action space")],
             "the world")
    + point("""&gamma; = 0.5 is <b>aggressive impatience</b>. It means a reward two steps
away is worth a quarter of one you can have now. Real problems use 0.9 to 0.99; 0.5 is
chosen here so the arithmetic stays checkable.""")
),

"return_by_hand": (
    p("""Before any algorithm, compute two returns by hand from state 4.""")
    + chainset([(["4 &rarr; 3 &rarr; 2 &rarr; 1", "return 12.5"],
                 "three steps to the <b>100</b>: 0.5&sup3; &times; 100"),
                (["4 &rarr; 5 &rarr; 6", "return 10.0"],
                 "two steps to the <b>40</b>: 0.5&sup2; &times; 40")],
               "from state 4, the two possible plans")
    + point("""So from state 4, walking <b>away</b> from the bigger prize is worse &mdash;
but only just, <b>12.5 against 10</b>. The 100 is two and a half times the 40 and it is one
step further, and the discount very nearly eats the whole advantage.""")
    + p("""That closeness is the point. Change &gamma; slightly and the answer flips, which
is exactly what the gamma sweep below demonstrates.""")
),

"value_iteration": (
    p("""Now compute every value at once, by repeatedly applying the Bellman equation.""")
    + expr("V(s) = max&#8336; [ R(s) + &gamma; V(s&prime;) ]",
           "the best of: what you get here, plus the discounted value of where you land")
    + values([("V*", "[100, 50, 25, 12.5, 20, 40]", "the converged values"),
              ("sweeps", "4", "that is all it took")],
             "value iteration")
    + point("""Read the values outwards from the ends. <b>50</b> is half of 100. <b>25</b> is
half of 50. <b>12.5</b> is half of 25. And on the right, <b>20</b> is half of 40. The true
rewards at the two terminals <b>leak inwards</b>, halving at each step.""")
    + p("""Four sweeps for six states is not a coincidence &mdash; information travels one
state per sweep, and the furthest any state is from a terminal is about four steps. That is
also why value iteration is slow on large problems.""")
),

"q_and_policy": (
    p("""Q separates &ldquo;how good is this state&rdquo; from &ldquo;how good is this
<b>action</b> in this state&rdquo;, which is what you actually need in order to decide.""")
    + values([("state 2", "Q(left) 50.000, Q(right) 12.500", "&rarr; <b>left</b>"),
              ("state 3", "Q(left) 25.000, Q(right) 6.250", "&rarr; <b>left</b>"),
              ("state 4", "Q(left) 12.500, Q(right) 10.000", "&rarr; <b>left</b>, narrowly"),
              ("state 5", "Q(left) 6.250, Q(right) 20.000", "&rarr; <b>right</b>")],
             "every action in every state")
    + point("""The policy is simply <b>argmax over each row</b>: &larr; &larr; &larr; &rarr;.
And <b>V(s) = max over the row</b>. Both fall straight out of Q, which is why Q is the thing
worth learning.""")
    + p("""The boundary sits between states <b>4 and 5</b>. State 4 still walks the long way
to the 100; state 5 gives up and takes the 40.""")
),

"gamma_sweep": (
    p("""Change nothing but &gamma;, and watch the rover change its mind at state 4.""")
    + values([("&gamma; = 0.20", "left 0.800 vs right 1.600", "&rarr; <b>right</b>"),
              ("&gamma; = 0.30", "left 2.700 vs right 3.600", "&rarr; <b>right</b>"),
              ("&gamma; = 0.40", "left 6.400 vs right 6.400", "&rarr; an exact <b>tie</b>"),
              ("&gamma; = 0.50", "left 12.500 vs right 10.000", "&rarr; <b>left</b>")],
             "the same state, four different discount rates")
    + point("""At <b>&gamma; = 0.4</b> the two options are worth <b>exactly the same</b>
&mdash; 6.400 each. Below it the agent grabs the near 40; above it the agent walks for the
distant 100.""")
    + p("""So &gamma; is not a tuning knob you set by validation. It is a <b>statement about
how much the future matters</b>, and it changes the optimal behaviour, not just how fast you
find it. Two agents with different &gamma; want genuinely different things.""")
),

"q_learning": (
    p("""Everything so far <b>knew the world</b> &mdash; the rewards, the transitions, all of
it. Q-learning knows none of that. It only gets to act and see what happens.""")
    + values([("state 2", "learned 50.000 / true 50.000", "and 12.500 / 12.500"),
              ("state 3", "learned 25.000 / true 25.000", "and 6.250 / 6.250"),
              ("state 4", "learned 12.500 / true 12.500", "and 10.000 / 10.000")],
             "Q-learning (told nothing) vs value iteration (told everything)")
    + point("""<b>Identical, to three decimal places.</b> One method was handed the complete
model of the world; the other worked it out by wandering around and remembering what
happened.""")
    + p("""This is the result that makes RL interesting. You do not need to <b>know</b> the
world to <b>act optimally</b> in it &mdash; and in most real problems you could never write
the world down anyway.""")
),

"exploration": (
    p("""The last section, and the one with the sharpest lesson. Same algorithm, only
&epsilon; changes.""")
    + values([("&epsilon; = 0.00", "[left, left, left, left]", "<b>WRONG</b>"),
              ("&epsilon; = 0.05", "[left, left, left, right]", "correct"),
              ("&epsilon; = 0.20", "[left, left, left, right]", "correct")],
             "the policy each run found")
    + point("""With <b>no exploration at all</b>, the agent gets state 5 wrong &mdash; it
walks left, away from a reward that is one step to its right.""")
    + p("""And it is not a bug. The agent's initial Q happened to favour left; it therefore
never went right from state 5; so it <b>never discovered the 40</b>; so its belief was never
corrected. The false belief protected itself.""")
    + point("""<b>Five percent</b> random actions is enough to fix it entirely. That is the
whole explore/exploit trade-off in three rows: without exploration you get stuck in a
<b>local policy</b> &mdash; and unlike a local minimum, nothing about the training curve tells
you it happened.""")
),
}
