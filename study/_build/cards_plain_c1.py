# -*- coding: utf-8 -*-
"""Beginner-friendly decode for every Course 1 card, keyed by card id."""
from cardkit import plain

P = {

"c1w1-model": plain(
  "A straight line drawn through your dots. To describe a line you only ever need two numbers: how "
  "steep it is, and how high it starts. That is the whole model.",
  [("f(x)", "“f of x”", "the machine: put a number in, get a guess out"),
   ("w", "“double-you”", "steepness. Bigger w = the line climbs faster"),
   ("x", "“ex”", "what you measured — the house size"),
   ("b", "“bee”", "where the line starts when x is zero"),
   ("=", "“is”", "just says the left side and right side are the same")],
  "Like working out a taxi fare: £2 to get in (that is b), plus £3 per mile (that is w)."),

"c1w1-notation": plain(
  "Little numbers floating next to a letter can mean three totally different things, and the "
  "<em>brackets</em> tell you which. Getting this wrong makes formulas look impossible.",
  [("x⁽²⁾", "“x, example two”", "the SECOND house in your list"),
   ("x²", "“x squared”", "x times itself"),
   ("a[²]", "“a, layer two”", "something belonging to layer 2 of a network"),
   ("( )", "round brackets", "→ which example"),
   ("[ ]", "square brackets", "→ which layer")],
  "Same as a shirt label: “size 10” and “10 in the pack” are both 10 and mean nothing alike."),

"c1w1-cost": plain(
  "One score for how badly your line fits. For every dot, measure how far off you were, square that "
  "number, add them all up, then divide to get an average. Low score = good line.",
  [("J", "“jay”", "the badness score. Small is good"),
   ("Σ", "“sum of”", "add up the following for every dot"),
   ("i = 1 to m", "“for each example”", "go through dot 1, dot 2, … dot m"),
   ("m", "“em”", "how many dots (training examples) you have"),
   ("( f − y )", "“guess minus truth”", "how far off you were on that dot"),
   ("( … )²", "“squared”", "multiply it by itself, so misses can't cancel out"),
   ("1/2m", "“divided by two-m”", "take the average; the 2 is just for tidiness later")],
  "Like a golf score: every stroke you waste adds up, and lower is better."),

"c1w1-cost-shape": plain(
  "If you draw the badness score for every possible line, you get a smooth bowl shape — like the "
  "inside of a salad bowl. A bowl has exactly one lowest point, so you can never get lost.",
  [("convex", "“con-vex”", "bowl-shaped: one bottom, no side dips"),
   ("parabola", "“pa-RAB-o-la”", "the U-shape you get from squaring things"),
   ("minimum", "“minimum”", "the lowest point — the best line")],
  "Drop a marble anywhere in a salad bowl and it always rolls to the same spot. That is what "
  "“convex” buys you."),

"c1w1-contour": plain(
  "The bowl seen from directly above, like a map of a hill. Each ring joins up all the points at the "
  "same height — so every line on one ring is equally bad.",
  [("contour", "“con-tour”", "a ring joining equal heights, like on a walking map"),
   ("w axis", "“the w direction”", "how steep the line is"),
   ("b axis", "“the b direction”", "how high the line starts"),
   ("bullseye", "“the centre”", "the best possible line")],
  "Rings squeezed close together = a steep cliff. Rings spread wide = flat ground."),

"c1w1-gd-update": plain(
  "Take one small step downhill, over and over. The formula says: look at which way is uphill, then "
  "move a little bit the OTHER way.",
  [(":=", "“becomes”", "not “equals” — it means “replace the old value with this”"),
   ("α", "“alpha”", "step size. How big a stride you take"),
   ("∂J/∂w", "“the slope in the w direction”", "which way is uphill, and how steep"),
   ("−", "“minus”", "the whole trick: go the OPPOSITE way to uphill")],
  "Simultaneous update means: both feet decide where to step BEFORE either one moves. Otherwise you "
  "trip."),

"c1w1-gd-sign": plain(
  "The slope has a sign — plus or minus — and that sign alone tells you which way to walk. You never "
  "need to know where the bottom is.",
  [("positive slope", "“going up to the right”", "so step LEFT to go down"),
   ("negative slope", "“going down to the right”", "so step RIGHT to go down"),
   ("slope = 0", "“flat”", "you are at the bottom; stop")],
  "Standing on a hill in fog: you can't see the valley, but you can always feel which way your feet "
  "tilt."),

"c1w1-alpha": plain(
  "α is your stride length. Too tiny and you shuffle forever. Too huge and you leap right over the "
  "valley and land higher up the other side — then leap even further next time.",
  [("α", "“alpha”", "how far you move each step"),
   ("diverge", "“di-VERGE”", "fly off to infinity instead of settling down"),
   ("NaN", "“nan”", "“Not a Number” — the computer's way of saying the maths broke"),
   ("oscillate", "“OSS-il-ate”", "bounce back and forth without settling")],
  "Stepping stones across a river: too small and you never cross, too big and you land in the water."),

"c1w1-alpha-debug": plain(
  "A trick to tell two different problems apart. Make the steps ridiculously tiny. If the score still "
  "won't come down, the problem isn't your step size — something in your code is wrong.",
  [("0.0001", "“a really tiny step”", "so small it CANNOT overshoot"),
   ("gradient", "“GRAY-dee-ent”", "the slope your code calculated"),
   ("sign error", "“a plus where a minus should be”", "the most common bug of all")],
  "Like testing whether a car won't start because of the fuel or the battery — change one thing "
  "only."),

"c1w1-derivatives": plain(
  "These two formulas answer: “if I nudge w a tiny bit, how much does the badness change?” and the "
  "same for b. They are what tells gradient descent which way to walk.",
  [("∂", "“partial dee”", "a fancy d. It means “rate of change of”"),
   ("∂J/∂w", "“dee J by dee w”", "how much the score changes when w changes"),
   ("· x<sup>(i)</sup>", "“times x”", "big houses push harder on w than small ones do"),
   ("(no x on b)", "—", "b shifts every guess equally, so every dot gets an equal vote")],
  "Think of w and b as two taps. These formulas say how much the water level moves per turn of each "
  "tap."),

"c1w1-batch": plain(
  "How many examples you look at before taking one step. Look at all of them, one of them, or a "
  "handful.",
  [("batch", "“batch”", "use ALL your examples for every single step"),
   ("stochastic", "“sto-KAS-tik”", "just a scary word for “random” — use one example at a time"),
   ("mini-batch", "“mini-batch”", "a small handful, usually 32 to 512. What everyone actually uses")],
  "Batch = read the whole book before deciding. Mini-batch = read a chapter. Stochastic = read one "
  "sentence."),

"c1w1-three-parts": plain(
  "Every single algorithm in all three courses is built from the same three pieces. Once you spot "
  "them, nothing later is really new.",
  [("model", "“the guesser”", "the shape of the guess it is allowed to make"),
   ("cost function", "“the scorer”", "one number saying how wrong the guesses are"),
   ("optimiser", "“the fixer”", "the thing that makes that number smaller")],
  "Like darts: how you throw (model), how far off you landed (cost), and adjusting your aim "
  "(optimiser)."),

"c1w2-multi-model": plain(
  "Before, one thing decided the price. Now several do — size, bedrooms, floors, age. Each gets its "
  "own dial saying how much it matters.",
  [("w₁, w₂, w₃", "“w one, w two…”", "one dial per thing you measured"),
   ("x₁, x₂, x₃", "“x one, x two…”", "the actual measurements"),
   ("w⃗", "“w vector”", "the little arrow means “this is a whole list of numbers, not one”"),
   ("·", "“dot”", "multiply each pair and add them all up"),
   ("n", "“en”", "how many features (columns) you have"),
   ("m", "“em”", "how many examples (rows) you have")],
  "A shopping bill: quantity of each item × its price, all added together."),

"c1w2-subscripts": plain(
  "Two little numbers pin down one single value in a table: which column, and which row.",
  [("subscript ₂", "“sub two”", "which FEATURE — which column"),
   ("superscript ⁽³⁾", "“example three”", "which EXAMPLE — which row"),
   ("x₂⁽³⁾", "“x two, example three”", "the bedrooms of the third house")],
  "Exactly like a spreadsheet cell: column B, row 3."),

"c1w2-dot-vs-star": plain(
  "Two ways to multiply lists that look almost the same and do very different things. One gives you "
  "a list back; the other gives you a single number.",
  [("*", "“star” / “times”", "multiply each pair, keep them separate → a LIST"),
   ("np.dot", "“numpy dot”", "multiply each pair AND add them up → ONE number"),
   ("list", "“a Python list”", "[1,2,3]. Times 2 makes it longer!"),
   ("array", "“a NumPy array”", "np.array([1,2,3]). Times 2 doubles each number")],
  "Star = the price of each item. Dot = the total bill."),

"c1w2-why-fast": plain(
  "Your computer can multiply many pairs of numbers at the exact same instant. A slow loop hands it "
  "one pair at a time, so nearly all that power sits idle.",
  [("loop", "“a for loop”", "do it one at a time, in order"),
   ("vectorised", "“VEK-tor-ised”", "hand over the whole list at once"),
   ("SIMD", "“sim-dee”", "hardware that multiplies many pairs in one go"),
   ("BLAS", "“blass”", "an old, extremely fast maths library NumPy secretly uses"),
   ("interpreter overhead", "—", "the time Python wastes just deciding what to do next")],
  "One cashier serving a queue, versus twenty tills open at once."),

"c1w2-scaling-why": plain(
  "If one column counts to 2000 and another only to 5, the bowl gets squashed into a long thin "
  "canyon. Walking down a canyon by always heading straight downhill means bouncing off the walls.",
  [("scaling", "“scaling”", "shrinking all columns to roughly the same size"),
   ("canyon", "—", "a bowl that is much steeper one way than the other"),
   ("zig-zag", "—", "bouncing side to side instead of walking forward")],
  "Rescaling turns the canyon back into a round bowl, and then straight downhill really does point "
  "at the bottom."),

"c1w2-scaling-how": plain(
  "Three recipes for shrinking every column to about the same size. The third is what nearly "
  "everybody uses.",
  [("μ", "“mew”", "the mean — the plain average of that column"),
   ("σ", "“sigma”", "the standard deviation — how spread out that column is"),
   ("x − μ", "“minus the average”", "slides the numbers so they sit around zero"),
   ("÷ σ", "“divided by sigma”", "squeezes them so the spread is about 1"),
   ("z-score", "“zee score”", "the name for doing both of those together")],
  "Like converting prices from yen and pounds into one shared currency before comparing."),

"c1w2-scaling-trap": plain(
  "Two mistakes that give you a model that looks fine and is quietly broken.",
  [("leak", "“leakage”", "letting the model peek at the test data by accident"),
   ("fit the scaler", "—", "work out μ and σ. Do this on TRAINING data only"),
   ("apply the scaler", "—", "use those SAME numbers on everything else, forever")],
  "Like marking your own exam using next year's answer sheet — the score means nothing."),

"c1w2-convergence": plain(
  "Draw a graph of “how wrong am I” against “how many steps have I taken”. The shape of that line "
  "tells you everything.",
  [("converged", "“con-VERGED”", "it stopped improving — it has finished"),
   ("plateau", "“pla-TOE”", "gone flat"),
   ("oscillating", "—", "wobbling up and down, so your steps are too big"),
   ("iteration", "“it-er-AY-shun”", "one single step")],
  "Like watching a kettle: still rising, or has it settled?"),

"c1w2-alpha-ladder": plain(
  "There is no formula for the right step size. You try a few, look at the graphs, and keep the "
  "biggest one that still behaves.",
  [("×3 apart", "—", "0.001, 0.003, 0.01… because step size acts by multiplying, not adding"),
   ("smooth decrease", "—", "the graph goes down cleanly with no wobbles"),
   ("hyperparameter", "“hyper-parameter”", "a setting YOU pick, not one the computer learns")],
  "Trying shoe sizes: you jump 6, 7, 8 — not 7.01, 7.02, 7.03."),

"c1w2-feateng": plain(
  "The model can only ADD things up. It cannot multiply two of your columns together. So if what "
  "really matters is width × depth, you have to work that out yourself and hand it over.",
  [("feature", "“FEE-cher”", "one column of your data — one thing you measured"),
   ("feature engineering", "—", "inventing a useful new column yourself"),
   ("interaction", "—", "a new column made by multiplying two others together")],
  "The model is a calculator stuck on the + key. If you need ×, you press it before handing over "
  "the number."),

"c1w2-polyreg": plain(
  "A straight line can't follow a curve. So you secretly hand the model x-squared as an extra "
  "column — and adding up straight things that include a squared thing gives you a curve.",
  [("polynomial", "“poly-NOH-mee-al”", "a formula with powers in it: x², x³"),
   ("linear in the parameters", "—", "“linear” describes the w's, NOT the x's"),
   ("x³", "“x cubed”", "x × x × x")],
  "You didn't change the machine. You changed what you fed it."),

"c1w3-why-not-linreg": plain(
  "Using a straight line to answer yes/no questions breaks in two ways: it gives answers like −0.4, "
  "and one extreme-but-obvious example drags the whole line sideways.",
  [("classification", "—", "sorting things into groups (yes/no) rather than guessing a number"),
   ("outlier", "“OUT-lie-er”", "a point sitting far away from all the others"),
   ("decision boundary", "—", "the dividing line between “yes” and “no”"),
   ("unbounded", "—", "can be any number at all, including silly ones")],
  "Like letting one very tall person shift where you draw the line between “tall” and “short”."),

"c1w3-sigmoid": plain(
  "A squasher. Feed it any number at all — minus a million, plus a million — and it hands back "
  "something between 0 and 1, which you can read as a chance.",
  [("g(z)", "“g of z”", "the squasher function"),
   ("z", "“zee”", "the plain old straight-line answer, before squashing"),
   ("e", "“ee”", "a fixed number, about 2.718. It just happens to make the maths tidy"),
   ("e^−z", "“e to the minus z”", "gets tiny when z is big, huge when z is very negative"),
   ("1/(1+…)", "—", "the shape that forces the answer between 0 and 1"),
   ("P(y=1|x)", "“probability y is 1, given x”", "the chance of a yes")],
  "Like a volume knob that physically cannot go below 0 or above 10, however hard you turn it."),

"c1w3-sigmoid-values": plain(
  "Worth memorising a few points on the S-curve so you can sanity-check numbers in your head.",
  [("g(0) = 0.5", "—", "dead centre: completely undecided"),
   ("g(2) ≈ 0.88", "—", "fairly confident yes"),
   ("g(5) ≈ 0.993", "—", "almost certain yes"),
   ("saturated", "“SAT-you-ray-ted”", "so far along the curve it has flattened out and stopped "
    "responding")],
  "Past about ±5 the curve is basically flat — pushing further changes nothing. That is exactly why "
  "extreme examples stop dragging the line."),

"c1w3-boundary": plain(
  "The line where the model stops saying “no” and starts saying “yes”. It sits wherever the "
  "unsquashed answer is exactly zero, because that is where the squasher gives 0.5.",
  [("z = 0", "“z is zero”", "the exact tipping point"),
   ("↔", "“if and only if”", "these two statements always agree with each other"),
   ("boundary", "—", "the dividing line on your chart"),
   ("threshold", "“THRESH-old”", "the cutoff you chose — usually 0.5, but you may move it")],
  "The features you hand over decide the SHAPE of that line: a straight line, or a circle, or "
  "something wigglier."),

"c1w3-why-not-sq-error": plain(
  "The old scoring method now makes a lumpy landscape full of little dips instead of one clean bowl. "
  "Walk downhill and you get stuck in the nearest dip, thinking you're done.",
  [("non-convex", "“non-CON-vex”", "lumpy: many dips, not one bowl"),
   ("local minimum", "—", "a dip that is not the deepest one"),
   ("squared error", "—", "the Course 1 scoring method: (guess − truth)²")],
  "A golf course full of small hollows, versus one big funnel."),

"c1w3-logloss": plain(
  "A scoring rule with an opinion: being confidently wrong should hurt enormously; being confidently "
  "right should cost nearly nothing.",
  [("L", "“ell”", "the loss — badness for ONE example"),
   ("log", "“log”", "a function that turns very small numbers into very big penalties"),
   ("−log(f)", "“minus log f”", "used when the true answer is yes"),
   ("−log(1−f)", "—", "used when the true answer is no"),
   ("y", "“why”", "the true answer: 1 for yes, 0 for no"),
   ("f", "“eff”", "what the model guessed, between 0 and 1")],
  "Because y is only ever 0 or 1, one of the two halves is multiplied by zero and vanishes."),

"c1w3-logloss-shape": plain(
  "The penalty doesn't rise gently — it accelerates. Going from “fairly sure” to “very sure” about "
  "something false costs far more than the first mistake did.",
  [("0.69", "—", "the score for a pure coin flip (guessing 50/50)"),
   ("→ ∞", "“goes to infinity”", "grows without limit as you get more confidently wrong"),
   ("confident", "—", "a guess close to 0 or close to 1")],
  "Like a bet: shrugging costs you little, betting your house on a lie costs you the house."),

"c1w3-why-log": plain(
  "Two good reasons the logarithm shows up here, and neither is “someone made it up”.",
  [("convex", "—", "makes the landscape a clean bowl again"),
   ("likelihood", "“LIKE-lee-hood”", "how probable your actual data is, under this model"),
   ("negative log-likelihood", "—", "picking the settings that make what you SAW most believable")],
  "It isn't a trick — it falls straight out of statistics."),

"c1w3-gd-logistic": plain(
  "The step you take is written in exactly the same letters as before. Only the meaning of one "
  "symbol changed.",
  [("f", "“eff”", "before: the straight line. Now: the SQUASHED straight line"),
   ("everything else", "—", "genuinely unchanged, letter for letter"),
   ("g′(z)", "“g prime of z”", "the slope of the squasher — it cancels out neatly")],
  "Same recipe, one swapped ingredient."),

"c1w3-overfit": plain(
  "Two opposite ways to be bad at this, and they need opposite cures — so naming them correctly "
  "matters.",
  [("underfit / high bias", "“BY-ass”", "too simple. Wrong even on stuff it has already seen"),
   ("overfit / high variance", "“VAIR-ee-ance”", "memorised the answers. Great on old stuff, useless "
    "on new"),
   ("generalise", "“JEN-er-al-ise”", "do well on things it has never seen — the only thing that "
    "counts")],
  "Underfit = the student who learned one fact. Overfit = the student who memorised last year's "
  "exam paper."),

"c1w3-address-overfit": plain(
  "Three ways to stop a model memorising. The third keeps all your information, which is why people "
  "reach for it first.",
  [("more data", "—", "with enough examples there is no room left to memorise"),
   ("fewer features", "—", "fewer dials to fiddle with"),
   ("regularisation", "“REG-you-lar-eye-zay-shun”", "keep every dial, but don't let any turn too far")],
  "Option 2 throws a tool out of the box. Option 3 just stops you swinging it too hard."),

"c1w3-regcost": plain(
  "You now tell the model two things at once: “match the data” AND “keep your numbers small”. It has "
  "to balance them, so it only uses a big number when a big number really earns its place.",
  [("λ", "“lambda”", "how loudly you say the second thing"),
   ("Σ w²", "“sum of w squared”", "how big the dials are overall"),
   ("λ = 0", "—", "second rule switched off → memorises"),
   ("λ huge", "—", "second rule shouts → everything flattens to a straight line"),
   ("j = 1", "“starting at one”", "deliberately skips b — b is left alone")],
  "Like a budget: you can spend, but every pound has to be justified."),

"c1w3-weight-decay": plain(
  "Rearranged, the update says: shrink every dial by a hair FIRST, then take your normal step. Do "
  "that thousands of times and dials only stay big if the data keeps pushing them back up.",
  [("(1 − αλ/m)", "“one minus alpha lambda over m”", "a number just under 1, like 0.9998"),
   ("decay", "“de-KAY”", "fade away slowly"),
   ("weight decay", "—", "the name for this, used in every modern ML library")],
  "Like a slow puncture: constant tiny leak, so you only stay inflated if you keep pumping."),

}
