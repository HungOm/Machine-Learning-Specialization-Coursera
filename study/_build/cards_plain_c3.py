# -*- coding: utf-8 -*-
"""Beginner-friendly decode for every Course 3 card, keyed by card id."""
from cardkit import plain

P = {

"c3w1-kmeans-steps": plain(
  "Drop a few flags on the playground. Everyone runs to their nearest flag. Each flag then moves to "
  "the middle of its own crowd. Repeat until nobody moves.",
  [("K", "“kay”", "how many groups you want. YOU choose this in advance"),
   ("centroid", "“SEN-troid”", "the middle of a group. Drawn as an ✕"),
   ("μ_k", "“mew kay”", "the position of centroid number k"),
   ("c<sup>(i)</sup>", "“c, example i”", "which group example i currently belongs to"),
   ("argmin", "“arg min”", "“whichever gives the smallest” — the INDEX, not the value"),
   ("‖ ‖²", "“squared distance”", "how far apart, squared. Squaring avoids a square root")],
  "Neither step can ever make things worse, which is why it always settles down."),

"c3w1-distortion": plain(
  "One score for how tight your groups are: the average squared distance from each point to its own "
  "flag. Smaller is tighter.",
  [("J", "“jay”", "the distortion — total tightness score"),
   ("distortion", "“dis-TOR-shun”", "just the name for this score"),
   ("μ_c<sup>(i)</sup>", "“the centroid that point i belongs to”", "read it inside out: c<sup>(i)</sup> says which, μ says where"),
   ("mean", "—", "the plain average. Exactly the point that minimises squared distance")],
  "If your code ever shows J going UP, you have a bug — usually moving flags before finishing the "
  "assignments."),

"c3w1-init": plain(
  "Where you drop the flags decides where you end up. So drop them somewhere else and try again, "
  "fifty times, then keep whichever attempt scored best.",
  [("local optimum", "“OP-ti-mum”", "a settled answer that isn't the best possible one"),
   ("initialisation", "“in-ish-al-eye-ZAY-shun”", "where you start the flags"),
   ("training points", "—", "start ON real data points, not at random empty coordinates"),
   ("k-means++", "“k means plus plus”", "a smarter way of seeding that spreads the flags out")],
  "You already have the tiebreaker for free — just keep the run with the lowest J."),

"c3w1-choose-k": plain(
  "You cannot pick the number of groups by minimising the score, because more groups ALWAYS scores "
  "better. With one group per point the score is zero.",
  [("elbow method", "—", "plot the score against K and look for a bend. Often there isn't one"),
   ("downstream purpose", "—", "judge K by what you'll actually DO with the groups"),
   ("K = m", "—", "one group per example. Score zero, information zero")],
  "T-shirts: 3 sizes is cheaper to make, 5 fits better. The data cannot decide that for you."),

"c3w1-gaussian": plain(
  "The bell curve. Measure a thousand people's heights and you get a hill: lots in the middle, few at "
  "the edges. Two numbers describe it completely.",
  [("μ", "“mew”", "the mean — where the top of the hill sits"),
   ("σ", "“sigma”", "standard deviation — how WIDE the hill is"),
   ("σ²", "“sigma squared”", "the variance. Sigma is its square root"),
   ("p(x)", "“p of x”", "how likely that value is. A density, not a probability"),
   ("e^−(…)", "—", "makes the curve drop off fast as you move away from the middle"),
   ("1/(√2π σ)", "—", "just scales it so the total area is exactly 1")],
  "Small σ = a tall narrow spike, so anything off-centre looks instantly suspicious."),

"c3w1-sigma-ranges": plain(
  "Rules of thumb for how much of a bell curve sits within so many steps of the middle. Worth "
  "memorising — they come up constantly.",
  [("1σ", "“one sigma”", "one standard deviation from the middle → 68% of everything"),
   ("2σ", "—", "95%. Still counts as normal"),
   ("3σ", "—", "99.7%. Now it's getting unusual"),
   ("4σ", "—", "about 1 in 15,000. Worth a look")],
  "A “3-sigma event” means something in the outer 0.3% — that's where the phrase comes from."),

"c3w1-anomaly": plain(
  "Check each measurement separately, then MULTIPLY the results together. Being slightly odd in one "
  "way is common; being slightly odd in five ways at once is very rare.",
  [("Π", "“product of”", "like Σ but multiplying instead of adding. Capital pi"),
   ("p(x)", "—", "the overall “how normal is this?” score"),
   ("ε", "“epsilon”", "the cutoff. Below this and you flag it"),
   ("independent", "—", "the assumption that the features don't affect each other"),
   ("underflow", "“UNDER-flow”", "so many small numbers multiplied that the answer rounds to zero")],
  "0.3 × 0.3 × 0.3 × 0.3 × 0.3 is tiny — even though no single 0.3 looked alarming."),

"c3w1-anomaly-split": plain(
  "You have thousands of normal examples and maybe twenty broken ones. Not enough to learn from — "
  "but plenty to TEST with.",
  [("training set", "—", "normal examples only. This is where μ and σ come from"),
   ("cross-validation", "—", "normal plus a few anomalies. Used to pick ε"),
   ("test set", "—", "normal plus a few anomalies. Used once, at the end"),
   ("skewed", "“skyood”", "one class is far rarer than the other")],
  "Put an anomaly in the training set and the model learns it's normal — which defeats the point."),

"c3w1-anomaly-vs-sup": plain(
  "Two approaches that look interchangeable, decided by a single question: will tomorrow's problems "
  "look like yesterday's?",
  [("anomaly detection", "—", "learn what NORMAL looks like, flag anything else"),
   ("supervised learning", "—", "learn what each specific class looks like"),
   ("novel failure mode", "—", "a way of breaking nobody has ever seen before")],
  "Spam looks like past spam → supervised. Aircraft engines fail in brand-new ways → anomaly "
  "detection. Fraudsters actively change tactics, which is why fraud sits on the anomaly side."),

"c3w1-features-anomaly": plain(
  "Feature choice matters far more here than in supervised learning, because there's no answer key "
  "telling the algorithm which columns to ignore.",
  [("Gaussian", "“GOW-see-an”", "bell-shaped. What the algorithm assumes each column looks like"),
   ("skewed", "—", "lopsided — a long tail off to one side"),
   ("log(x + c)", "“log of x plus c”", "a transform that pulls a long tail back into a hill shape"),
   ("ratio", "—", "one column divided by another. Often far more revealing than either alone")],
  "The classic: a server with normal CPU and normal network traffic, but a wildly unusual RATIO "
  "between them. Neither column alone would ever catch it."),

"c3w2-notation": plain(
  "A blank square in a ratings table means “we don't know”, not “they hated it”. Confusing those two "
  "wrecks the model.",
  [("r(i,j)", "“r of i j”", "1 if this person rated this film at all, 0 if they never did"),
   ("y(i,j)", "“y of i j”", "the actual rating they gave. Only exists where r = 1"),
   ("i", "—", "which film (row)"),
   ("j", "—", "which person (column)"),
   ("sparse", "“sparce”", "mostly empty. A real ratings table is 99.99% blank")],
  "Treat blanks as zeros and you teach the model that every unwatched film is terrible — and "
  "unwatched is nearly everything."),

"c3w2-collab": plain(
  "Two chicken-and-egg problems solved at once. If I knew what the films were like, I could work out "
  "what you like. If I knew what you like, I could work out what the films are like. So guess both, "
  "then improve both together.",
  [("w<sup>(j)</sup>", "“w for person j”", "that person's taste dials"),
   ("x<sup>(i)</sup>", "“x for film i”", "that film's hidden qualities. NOW ALSO LEARNED"),
   ("b<sup>(j)</sup>", "—", "that person's general generosity with stars"),
   ("r=1", "—", "only sum over squares that actually have a rating in them"),
   ("λ", "“lambda”", "keeps all the numbers from getting silly"),
   ("collaborative", "“col-LAB-or-ative”", "everyone's ratings help everyone else's predictions")],
  "Nobody labelled any film as romantic or action. The algorithm works it out from who liked what."),

"c3w2-collab-init": plain(
  "Start everything at zero and nothing can ever tell itself apart — every dial gets the identical "
  "nudge, forever.",
  [("initialise", "—", "the values you start with, before any learning"),
   ("symmetric", "“sim-ET-ric”", "identical, so they all move together and never differentiate"),
   ("small random values", "—", "the fix. Tiny differences let them specialise")],
  "Also: without λ there are infinitely many equally good answers (scale w up, scale x down). "
  "Regularisation is what picks one."),

"c3w2-meannorm": plain(
  "A brand-new user has rated nothing, so the maths keeps their dials at zero, so every prediction "
  "is zero stars. Fix it by making “zero” mean “average” instead of “terrible”.",
  [("μᵢ", "“mew i”", "the average rating of film i, across everyone who rated it"),
   ("mean normalisation", "—", "subtract that average before training, add it back when predicting"),
   ("cold start", "—", "the problem of knowing nothing about a new user or item"),
   ("by row", "—", "per FILM. This helps new users. By column would help new films")],
  "Now a new user is shown the generally well-liked films, which is exactly the right default."),

"c3w2-R-mask": plain(
  "A one-character trick that does the job of “only count the squares that have a rating in them”.",
  [("R", "“capital R”", "a table of 1s and 0s: 1 where a rating exists"),
   ("* R", "“times R”", "multiply elementwise — zeroes out every blank square"),
   ("elementwise", "—", "pair up matching positions and multiply each pair"),
   ("before squaring", "—", "zero it first, so blanks contribute nothing to the score OR the slope")],
  "Anything multiplied by zero is zero, so the blanks quietly disappear from the sum."),

"c3w2-related": plain(
  "The algorithm gave each film a little list of numbers. You have no idea what they mean — and it "
  "doesn't matter. Films with SIMILAR lists turn out to be similar films.",
  [("‖ ‖²", "“squared distance”", "how far apart two lists of numbers are"),
   ("nearest neighbour", "—", "the closest few"),
   ("l", "“ell”", "which position in the list you're comparing"),
   ("FAISS / HNSW", "“face” / “aitch-en-ess-double-you”", "libraries that find nearest neighbours "
    "among millions in milliseconds")],
  "This is the same technique that powers “vector search” for AI chatbots."),

"c3w2-cf-vs-cbf": plain(
  "Two philosophies. One learns from who else liked it; the other from what the thing actually IS. "
  "Each fails exactly where the other works.",
  [("collaborative", "—", "“people like you also liked…”. Knows nothing about the film itself"),
   ("content-based", "—", "“you're 27 and like sci-fi, and this is sci-fi”"),
   ("cold start", "—", "a brand-new user or item, with no history at all"),
   ("features", "—", "known facts: age, genre, year, cast")],
  "Real systems run both: content-based covers the newcomers, collaborative catches the patterns "
  "nobody thought to write down."),

"c3w2-two-tower": plain(
  "Build two separate machines. One turns everything about a person into 32 numbers; the other turns "
  "everything about a film into 32 numbers. Now they're comparable, so multiply and add.",
  [("tower", "—", "one of the two networks"),
   ("v_u", "“v sub u”", "the user's 32-number summary"),
   ("v_m", "“v sub m”", "the film's 32-number summary"),
   ("embedding", "“em-BED-ing”", "the posh word for “a summary as a list of numbers”"),
   ("dot product", "—", "multiply the pairs and add. Big number = good match")],
  "The two towers can have totally different shapes and inputs. Only their OUTPUT lengths must match."),

"c3w2-retrieval": plain(
  "You're choosing a present from a shop with ten million things. You don't examine all ten million — "
  "you grab a trolley of plausible ones quickly, then look at those properly.",
  [("retrieval", "“ri-TREE-val”", "the fast, rough shortlist step"),
   ("ranking", "—", "the slow, accurate scoring step"),
   ("candidates", "—", "the shortlist. Usually around 100"),
   ("recall", "—", "did I keep all the good ones? Retrieval's job"),
   ("precision", "—", "did I get the ORDER right? Ranking's job")],
  "Anything retrieval throws away can never be recommended, however clever the ranker is."),

"c3w2-ethics": plain(
  "Most models predict a world they don't affect. A recommender changes what people watch — and then "
  "trains on what they watched.",
  [("feedback loop", "—", "the output changes the input, round and round"),
   ("engagement", "—", "clicks and watch time. Easy to measure, easy to game"),
   ("amplify", "“AM-pli-fy”", "make more of something appear"),
   ("proxy metric", "—", "an easy number you measure instead of the thing you actually want")],
  "Tell a system “maximise watch time” and it will find that outrage works — without any malice. "
  "It's simply what the instruction meant, taken literally."),

"c3w2-l2norm": plain(
  "Scale both summaries to the same length before comparing, so you're comparing DIRECTION rather "
  "than size.",
  [("l2_normalize", "“ell two normalise”", "divide a list by its own length, so its length becomes 1"),
   ("cosine similarity", "“CO-sine”", "how much two arrows point the same way. Between −1 and 1"),
   ("magnitude", "“MAG-ni-tude”", "how long the arrow is"),
   ("functional API", "—", "the Keras style you need when a model has two separate inputs")],
  "Without it the network can cheat: instead of learning better directions, it just makes the arrows "
  "longer."),

"c3w2-pca": plain(
  "Shine a torch at a crowd and look at the shadows on the wall. From one angle everyone overlaps; "
  "from another they're nicely spread out. PCA finds the angle that spreads them out most.",
  [("PCA", "“pee-see-ay”", "Principal Component Analysis"),
   ("principal component", "—", "one of the new axes it finds"),
   ("covariance matrix", "“co-VAIR-ee-ance”", "a table of how the columns move together"),
   ("eigenvector", "“EYE-gen-vector”", "a direction the data naturally stretches along"),
   ("eigenvalue", "—", "how MUCH it stretches in that direction. Sort by this"),
   ("project", "—", "drop each point onto the new axis and record how far along it lands")],
  "Spread = information kept. Not the same as linear regression: that measures vertical distance to "
  "an answer; PCA measures perpendicular distance and has no answer at all."),

"c3w2-pca-use": plain(
  "Honest answer about what this is actually good for these days.",
  [("visualisation", "—", "squash 50 columns to 2 so a human can draw it and look"),
   ("compression", "—", "storage is cheap now. This mattered more in 1998"),
   ("t-SNE / UMAP", "“tee-snee” / “YOU-map”", "newer methods that usually make prettier 2-D pictures")],
  "PCA never sees your answers, so it can happily throw away the one small direction that actually "
  "predicts what you care about."),

"c3w3-rl-vs-sup": plain(
  "How you train a dog. You never show it a thousand photos labelled “correct sitting posture”. You "
  "say sit, and when something roughly right happens, it gets a treat.",
  [("reinforcement learning", "“ree-in-FORCE-ment”", "learning from rewards instead of answers"),
   ("reward", "—", "a number the world hands back. Positive good, negative bad"),
   ("policy", "“POL-i-see”", "the rule being learned: what to do in each situation"),
   ("agent", "—", "the thing making decisions. Your program"),
   ("environment", "—", "everything else — the world it acts in")],
  "The hard part is the delay: the treat comes after the sit, but WHICH of the last twenty things "
  "earned it?"),

"c3w3-return": plain(
  "£100 today or £100 next year? Today. £100 today or £110 next year? Now it depends how patient you "
  "are. γ is the dial for exactly that.",
  [("return", "—", "the total reward, counting the future as worth slightly less"),
   ("γ", "“gamma”", "the discount. A number between 0 and 1"),
   ("γ²", "“gamma squared”", "two steps away, so discounted twice"),
   ("R₁, R₂", "—", "the reward at step 1, step 2, and so on"),
   ("γ⁰ = 1", "—", "the first reward isn't discounted at all")],
  "γ near 1 = patient, happy to wait. γ near 0 = grabs whatever's closest. It's a choice you make, "
  "not a fact about the world."),

"c3w3-mdp": plain(
  "The formal name for this whole setup, and the one assumption hiding inside it.",
  [("MDP", "“em-dee-pee”", "Markov Decision Process. Just a name for the S/A/R/γ/π setup"),
   ("S", "—", "all the situations you could be in"),
   ("A", "—", "all the things you could do"),
   ("R(s)", "—", "what each situation is worth"),
   ("π(s)", "“pi of s”", "your plan: given this situation, do that. Nothing to do with 3.14"),
   ("Markov", "“MAR-koff”", "the future depends only on where you are NOW, not how you got here")],
  "If that assumption is false, put the missing history INTO the state — which is exactly why game-"
  "playing AIs stack four consecutive video frames."),

"c3w3-q": plain(
  "Q answers one very specific question: “if I'm here, and I do this ONE thing, and then play "
  "perfectly forever after — how much do I get in total?”",
  [("Q(s,a)", "“Q of s a”", "the value of doing action a in situation s"),
   ("s", "—", "the situation you're in"),
   ("a", "—", "the action you're considering"),
   ("π*", "“pi star”", "the BEST possible plan. The star means optimal"),
   ("argmax_a", "—", "whichever ACTION gives the biggest Q"),
   ("V(s)", "“V of s”", "the value of being in situation s at all — the best Q available there")],
  "The odd shape (one free action, then perfect play) is what makes choosing trivial: work out two "
  "numbers, take the bigger."),

"c3w3-bellman": plain(
  "Every long journey splits into two bits: what you get right now, and how good tomorrow will be. "
  "One line, and every reinforcement learning algorithm ever written is built on it.",
  [("R(s)", "—", "what you collect immediately. The “now” half"),
   ("γ", "—", "discount the future half slightly"),
   ("s′", "“s prime”", "the situation you land in next. Prime always means “next”"),
   ("a′", "“a prime”", "the action you'd take from there"),
   ("max_a′", "—", "assume you'd pick the best one available")],
  "Q appears on both sides — it defines itself. That sounds circular, but there's exactly one set of "
  "numbers that works, and you can find it by repeatedly applying the equation."),

"c3w3-rover-values": plain(
  "The little six-square example, worked all the way through. Worth being able to reproduce on paper "
  "— everything else in the week is this, scaled up.",
  [("V(s)", "—", "how much each square is worth"),
   ("terminal", "—", "reaching square 1 or 6 ends the trip"),
   ("← ← ← →", "—", "the best plan: squares 2, 3, 4 go left; square 5 goes right"),
   ("0.5 × 25", "—", "one step away from something worth 25, discounted by γ = 0.5")],
  "Square 5 goes right because 40 is one step away, while 100 is four steps away — and with γ = 0.5, "
  "four steps costs you a lot."),

"c3w3-stochastic": plain(
  "What if you say “go left” and the ground is icy, so 10% of the time you slide right instead? You "
  "stop asking “what will I get” and start asking “what will I get ON AVERAGE”.",
  [("stochastic", "“sto-KAS-tik”", "random. Just a scary word for “sometimes it goes wrong”"),
   ("E[…]", "“the expected value of”", "the average over everything that could happen, weighted by "
    "how likely each is"),
   ("expected return", "—", "not what happens once — what happens on average over many tries")],
  "Every value drops when the world is unreliable. That's correct: a world you can't control is "
  "genuinely worth less to be in."),

"c3w3-continuous": plain(
  "Six squares you can write on a piece of paper. A truck's position, speed and angle — you could "
  "never list them all, because there are infinitely many.",
  [("continuous", "“con-TIN-you-us”", "made of real numbers, not a short list of options"),
   ("ℝ<sup>n</sup>", "“R to the n”", "a list of n real numbers. Just means “n measurements”"),
   ("curse of dimensionality", "—", "chop each of 6 measurements into 100 buckets and you need a "
    "trillion boxes"),
   ("function approximation", "—", "COMPUTE the value instead of looking it up in a table"),
   ("generalise", "—", "guess sensibly about situations you've never actually been in")],
  "A table has no idea that 12.34 metres and 12.35 metres are nearly the same thing. A network does."),

"c3w3-dqn": plain(
  "The trick that makes it work: you have no correct answers, so you INVENT them — using the network "
  "you're currently training.",
  [("DQN", "“dee-cue-en”", "Deep Q-Network"),
   ("(s, a, R, s′)", "—", "one memory: where I was, what I did, what I got, where I ended up"),
   ("replay buffer", "—", "the last 10,000 memories, kept and reused"),
   ("target y", "—", "the made-up “right answer” you train towards"),
   ("bootstrapping", "“BOOT-strapping”", "improving a guess using another of your own guesses")],
  "It doesn't spiral into nonsense because R is REAL. Every made-up target contains one genuine "
  "measured reward, and that truth spreads outwards."),

"c3w3-replay": plain(
  "Why keeping a pile of old memories matters more than it looks.",
  [("correlated", "“COR-e-lay-ted”", "very similar to each other. Consecutive video frames nearly "
    "are"),
   ("i.i.d.", "“eye-eye-dee”", "independent and identically distributed — the “examples should be "
    "unrelated” assumption all supervised learning rests on"),
   ("random sampling", "—", "pulling memories out in a jumbled order, which breaks the correlation"),
   ("data efficiency", "—", "reusing each hard-won experience many times")],
  "It was tested without the buffer in the original paper and performance collapsed. It's holding "
  "the roof up, not decorating it."),

"c3w3-arch": plain(
  "A design change that costs nothing and saves three quarters of the work. Move the actions from "
  "the input side to the output side.",
  [("one-hot action", "—", "encoding “which action” as four columns of 0s and one 1"),
   ("forward pass", "—", "running the network once to get an answer"),
   ("4 outputs", "—", "one Q value per action, all in one go"),
   ("linear output", "—", "no squashing. Q values can be −200 or +140, so squashing would ruin them")],
  "Picking an action happens millions of times during training, so a 4× saving on that is enormous."),

"c3w3-epsilon": plain(
  "You always order the same dish because you know it's good. But there are forty others and one "
  "might be better — and you'll never find out.",
  [("ε", "“epsilon”", "how often you deliberately ignore your own advice. Usually small"),
   ("greedy", "“GREE-dee”", "taking the best option you currently know about"),
   ("exploration", "—", "trying something random, just to see"),
   ("exploitation", "“ex-ploy-TAY-shun”", "using what you already know"),
   ("decay", "—", "start at ε = 1 (all random), shrink towards 0.01 as your knowledge improves")],
  "A randomly-started network might believe “firing the engine is bad”. If it never tries, it never "
  "learns otherwise."),

"c3w3-soft-update": plain(
  "Don't throw the old network away and swap in the new one. Blend them — keep 99% of the old and "
  "mix in 1% of the new.",
  [("τ", "“tau”", "how much of the new network to mix in. About 0.01"),
   ("soft update", "—", "blending rather than replacing"),
   ("target", "—", "the made-up right answer you're training towards"),
   ("W", "—", "the network's weights")],
  "The targets are computed FROM the network being trained. If the network jumps, every target "
  "jumps, and you're chasing something that keeps moving."),

"c3w3-reward-design": plain(
  "The agent maximises exactly what you wrote down — including the loopholes you didn't spot. This "
  "has a name and a long history of funny, expensive failures.",
  [("reward function", "—", "the rules you wrote saying what's worth points"),
   ("specification gaming", "“spess-if-i-KAY-shun”", "finding a loophole in the rules rather than "
    "doing what you meant"),
   ("reward shaping", "—", "designing rewards to encourage the behaviour you want"),
   ("proxy", "—", "an easy-to-measure stand-in for what you actually care about")],
  "A boat-racing AI rewarded for collecting power-ups learned to spin in circles forever, never "
  "finishing the race — and outscored every human."),

"c3w3-state-of-rl": plain(
  "An honest scorecard, because the hype around this exceeds what is actually deployed.",
  [("simulator", "—", "a computer model of the world. Trials are free and instant"),
   ("sim-to-real", "—", "the gap between the simulator and actual reality. Usually painful"),
   ("sample efficiency", "—", "how many tries you need. RL needs millions"),
   ("RLHF", "“are-ell-aitch-eff”", "RL from Human Feedback — how chat models are tuned. Quietly the "
    "biggest real use of RL there is")],
  "Superhuman in video games. Fragile and expensive on real robots. Worth knowing; rarely the first "
  "tool to reach for."),


"c3w1-drill-gaussian": plain(
  "The bell curve's height at its own centre \u2014 the single most likely value it will ever hand "
  "back. Move away from the centre in either direction and the height only ever drops.",
  [("&mu;", "“mew”", "the centre of the bell curve, its average"),
   ("&sigma;", "“sigma”", "how wide the bell curve is"),
   ("p(x)", "“p of x”", "how likely a value near x is \u2014 the bell's height there")],
  "Standing exactly at the middle of a hill is the highest point you can be \u2014 walk any "
  "direction and you go downhill from there. 0.399 is that hilltop height."),

"c3w3-drill-return": plain(
  "Add up every future reward, but shrink each one the further away it is \u2014 a reward three "
  "steps from now is worth less than the same reward arriving right now.",
  [("&gamma;", "“gamma”", "the discount \u2014 how much patience the agent has, between 0 and 1"),
   ("R\u2081, R\u2082, R\u2083", "“R one, R two, R three”", "the reward received at each future step")],
  "Like preferring \u00a3100 today over \u00a3100 in three years \u2014 the further away a reward "
  "is, the less it counts right now."),

}
