# -*- coding: utf-8 -*-
"""Mock quiz — C3 W3."""
from mockkit import Q, O, SET

SET = SET("C3", 3, "Reinforcement Learning",
"""Return, policy, Q(s,a), Bellman and the three refinements. Work the six-square rover by hand
before sitting this — most of these are answerable from that strip.""", [

Q("c3w3-q01",
  "<p>With rewards 100 at state 1, 40 at state 6, zero elsewhere and &gamma; = 0.5, what is the "
  "return from state 4 if you always go left?</p>",
  [O("12.5", True,
     "Three steps to reach state 1: 0 + 0 + 0 + 0.5&sup3; &times; 100 = 0.125 &times; 100 = 12.5. "
     "The discount is applied once per step taken."),
   O("100", False,
     "That is the undiscounted reward. &gamma; &lt; 1 means a distant reward is worth less than a "
     "near one."),
   O("50", False,
     "That is one step of discounting, from state 2."),
   O("25", False,
     "That is two steps of discounting, from state 3.")],
  "c3/w3-03-the-return.html", tag="the return",
  note="At &gamma; = 0.5 a reward six steps away is worth about 1.6% of face value."),

Q("c3w3-q02",
  "<p>What is a <b>policy</b> in reinforcement learning?</p>",
  [O("A function from state to action — what to do in every state you might be in", True,
     "Not a plan or a sequence. A lookup that has an answer ready for whichever state you actually "
     "find yourself in, which is why RL survives surprises that break classical planning."),
   O("The sequence of actions that gives the highest reward", False,
     "That is a plan, and it falls apart the moment something unexpected happens."),
   O("The total reward the agent will collect", False,
     "That is the return."),
   O("The probability of moving between states", False,
     "That is the environment's transition dynamics, not the agent's policy.")],
  "c3/w3-04-policies.html", tag="policies"),

Q("c3w3-q03",
  "<p>What exactly does <span class=\"v\">Q(s, a)</span> mean?</p>",
  [O("Take action a in state s, then behave optimally for ever after", True,
     "The definition is deliberately strange — a may be foolish. That is what makes the comparison "
     "between two actions clean: any difference is caused by the first move alone."),
   O("The immediate reward for taking action a in state s", False,
     "That is R(s). Q looks at the whole discounted future, which is the entire point."),
   O("The probability of taking action a in state s", False,
     "That is a stochastic policy. Q is a value, not a probability."),
   O("Take action a and then act randomly afterwards", False,
     "Acting optimally afterwards is what makes Q comparable across actions.")],
  "c3/w3-06-state-action-value-function.html", tag="the Q function",
  note="Once Q exists, the policy is free: stand in a state, read the numbers, take the largest."),

Q("c3w3-q04",
  "<p>The Bellman equation says <span class=\"v\">Q(s,a) = R(s) + &gamma; max Q(s&prime;, "
  "a&prime;)</span>. Which are true?</p>",
  [O("It splits the problem into one step plus the same problem again", True,
     "What I get now, plus the discounted best I can do from where I land. That recursion is "
     "Bellman's principle of optimality."),
   O("It turns RL into a supervised learning problem", True,
     "The right-hand side becomes a training target and the network's output is the prediction. That "
     "reframing is the whole trick behind DQN."),
   O("The max is taken over the actions available in the <em>next</em> state", True,
     "s&prime; is where you land, and a&prime; ranges over what you could do there."),
   O("It requires knowing the entire sequence of future states in advance", False,
     "It needs only the next state. That locality is exactly why it is useful."),
   O("It only applies to deterministic environments", False,
     "For stochastic environments the right-hand side becomes an expectation. The structure is "
     "unchanged.")],
  "c3/w3-08-bellman-equation.html", tag="Bellman"),

Q("c3w3-q05",
  "<p>Why is an &epsilon;-greedy policy used during training?</p>",
  [O("Acting greedily on bad estimates is self-confirming — you never gather correcting evidence",
     True,
     "You never take the action you underrate, so you never learn that you underrated it. The error "
     "is stable, and a small amount of forced randomness is what breaks it."),
   O("It makes the algorithm converge faster", False,
     "It often converges more <em>slowly</em> in the short term, because some steps are deliberately "
     "wasted. It converges to something better."),
   O("It reduces the memory needed", False,
     "Memory is unaffected."),
   O("It prevents the Q values from becoming negative", False,
     "Negative Q values are perfectly normal when rewards are negative.")],
  "c3/w3-14-epsilon-greedy.html", tag="explore vs exploit",
  note="&epsilon; is normally decayed — near 1.0 early, about 0.01 later."),

Q("c3w3-q06",
  "<p>Why does moving from six discrete states to a continuous state space require a neural "
  "network?</p>",
  [O("There are infinitely many states, so a lookup table is impossible", True,
     "You need something that takes a state it has never seen and produces a value anyway — which is "
     "function approximation, and exactly what you spent two courses building."),
   O("Because neural networks are faster than tables", False,
     "A table lookup is far faster. The issue is that the table cannot exist."),
   O("Because continuous states have no rewards", False,
     "Rewards are defined the same way regardless of how states are represented."),
   O("Because the Bellman equation does not apply to continuous states", False,
     "It applies unchanged. Only how you store Q changes.")],
  "c3/w3-10-continuous-state-spaces.html", tag="function approximation",
  note="Tabular Q-learning provably converges. With a network it does not — hence the three refinements."),

Q("c3w3-q07",
  "<p>The improved DQN architecture outputs one Q value per action rather than taking the action as "
  "an input. Why?</p>",
  [O("You need every action's value to take the argmax, so one pass beats four", True,
     "A fourfold reduction in inference cost per decision, from a change to the last layer only — and "
     "training involves millions of decisions."),
   O("It makes the network more accurate", False,
     "Accuracy is not the motivation; efficiency is."),
   O("It allows continuous action spaces", False,
     "The opposite: this architecture <em>requires</em> a fixed, finite, discrete action set."),
   O("It removes the need for the Bellman equation", False,
     "Bellman still supplies the training targets.")],
  "c3/w3-13-improved-architecture.html", tag="DQN architecture"),

Q("c3w3-q08",
  "<p>What problem does the <b>soft update</b> of the target network solve?</p>",
  [O("The training targets move because they come from the network being trained", True,
     "Chasing a target that runs away is why naive deep Q-learning oscillates or diverges. Moving the "
     "target slowly — 0.01 new, 0.99 old — makes it nearly stationary."),
   O("It reduces the memory needed to store experiences", False,
     "That is what the replay buffer's size limit does."),
   O("It makes the network explore more", False,
     "Exploration is &epsilon;-greedy's job."),
   O("It removes the need for a learning rate", False,
     "Both exist and do different jobs — one governs the weight update, the other the target's "
     "drift.")],
  "c3/w3-15-minibatch-soft-updates.html", tag="soft updates"),

Q("c3w3-q09",
  "<p>Which are honest statements about the state of reinforcement learning?</p>",
  [O("It needs an enormous number of episodes, which is cheap in simulation and expensive on hardware",
     True,
     "Sample efficiency is the practical limitation, and it is why nearly every deployed success has "
     "either a simulator or a very cheap failure."),
   O("Designing the reward function is often the hardest engineering in the project", True,
     "Agents optimise exactly what you wrote, including the parts you did not mean. Reward hacking is "
     "the standard outcome of a sloppy specification."),
   O("RLHF for language models is a major current application", True,
     "The reward comes from human preference comparisons rather than a simulator — one answer to the "
     "sample-efficiency problem rather than an exception to it."),
   O("RL has largely replaced supervised learning in industry", False,
     "The overwhelming majority of deployed machine learning is supervised, and comfortably so."),
   O("RL works out of the box on physical robots", False,
     "This is the hardest setting, because failure is expensive and a policy tuned in simulation "
     "often does not transfer.")],
  "c3/w3-16-state-of-rl.html", tag="where RL actually works"),

Q("c3w3-q10",
  "<p>In a stochastic environment where the intended action succeeds 90% of the time, what changes?</p>",
  [O("You maximise the <em>expected</em> return rather than the return", True,
     "You no longer choose where you end up; you choose a distribution over where you might. Steer "
     "for the average outcome being good."),
   O("The Bellman equation no longer applies", False,
     "It applies with an expectation on the right-hand side. The structure is intact."),
   O("The optimal policy is always to take the safest action", False,
     "Sometimes, and not always — it depends on the rewards. A large reward can be worth a 10% risk "
     "of misstep."),
   O("&gamma; must be set to 1", False,
     "&gamma; is a separate modelling choice about how far-sighted the agent should be.")],
  "c3/w3-09-stochastic-environments.html", tag="stochastic environments"),
])
