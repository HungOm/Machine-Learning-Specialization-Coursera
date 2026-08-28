# -*- coding: utf-8 -*-
"""Beginner-friendly decode for every Course 2 card, keyed by card id."""
from cardkit import plain

P = {

"c2w1-neuron": plain(
  "A neuron is a kid who listens to a few friends, trusts each one a different amount, adds it all "
  "up, and then shouts an answer between 0 and 1. That is genuinely all it does.",
  [("w⃗", "“w vector”", "the trust levels — one per friend"),
   ("x⃗", "“x vector”", "what the friends said — the inputs"),
   ("·", "“dot”", "multiply each pair and add them up"),
   ("b", "“bee”", "the kid's own stubborn starting mood"),
   ("z", "“zee”", "the raw total, before squashing. Any number at all"),
   ("g", "“g”", "the squasher"),
   ("a", "“a” (activation)", "what it finally shouts out and passes on")],
  "This is exactly logistic regression from Course 1. One neuron IS one logistic regression."),

"c2w1-hidden-layer": plain(
  "In Course 1 you invented useful new columns by hand. A hidden layer invents its own — and works "
  "out which of its inventions are worth keeping.",
  [("hidden layer", "—", "a middle row of neurons you never see the output of directly"),
   ("learned features", "—", "new columns the network made up for itself"),
   ("hidden unit", "—", "one neuron in that middle row")],
  "The names people give hidden units (“affordability”, “awareness”) are a story told afterwards. "
  "Nothing in training assigns them meaning."),

"c2w1-layer": plain(
  "A layer is a panel of judges. They all watch the same performance, each holds up one score card, "
  "and the row of score cards is what gets passed on.",
  [("layer", "—", "a group of neurons that all read the same input"),
   ("units", "“units” / “neurons”", "the same thing. How many judges are on the panel"),
   ("units=3", "—", "three judges, so three numbers come out")],
  "The judges never talk to each other — which is exactly why a computer can work them all out at "
  "the same instant."),

"c2w1-params": plain(
  "Counting the knobs the network has to learn. Every input connects to every neuron, so you "
  "multiply — then add one extra knob per neuron for its mood.",
  [("parameter", "“pa-RAM-eter”", "a number the network learns for itself"),
   ("n", "“en”", "how many numbers come IN"),
   ("p", "“pee”", "how many neurons are in this layer"),
   ("n × p", "—", "one wire from each input to each neuron"),
   ("+ p", "—", "one bias per neuron")],
  "Like plugging every one of 400 cables into each of 25 sockets: 10,000 connections."),

"c2w1-master-eq": plain(
  "One line that describes every single calculation in every network in this course. It looks scary "
  "and it is only saying: “this neuron listens to the whole row before it, then shouts.”",
  [("a", "—", "what a neuron shouts out"),
   ("subscript j", "“unit j”", "WHICH neuron in the row"),
   ("[l]", "“layer l”", "WHICH row it is in"),
   ("[l−1]", "“the row before”", "the previous layer — it listens to ALL of that row"),
   ("w, b", "—", "that particular neuron's trust levels and mood"),
   ("g", "—", "the squasher")],
  "Say it out loud: “what neuron j in row l shouts is the squash of — its own trust levels, dotted "
  "with everything the previous row said, plus its own mood.”"),

"c2w1-brackets": plain(
  "The same tiny raised number means three different things depending on the brackets around it. "
  "Mixing these up is the number one way formulas become unreadable.",
  [("a[²]", "“a, layer two”", "square brackets → which LAYER"),
   ("x⁽²⁾", "“x, example two”", "round brackets → which EXAMPLE"),
   ("x²", "“x squared”", "no brackets → a genuine power")],
  "Reading a[²] as “a squared” is the single most common mistake in Course 2."),

"c2w1-weight-vec-len": plain(
  "How many trust levels does one neuron need? Exactly as many as there are things talking to it.",
  [("w₂[³]", "“w two, layer three”", "the trust levels of neuron 2 in row 3"),
   ("previous layer width", "—", "how many neurons are in the row before"),
   ("4 → 5 → 3 → 1", "—", "a network with rows of those sizes")],
  "Careful: neuron 2 of row 3 listens to EVERY neuron in row 2 — not just neuron 2."),

"c2w1-dense-cols": plain(
  "W is a table of trust levels. Reading it the right way round is what makes everything else work.",
  [("W", "“capital double-you”", "the whole layer's trust levels as one table"),
   ("columns", "—", "one column per NEURON"),
   ("rows", "—", "one row per INPUT"),
   ("W[:, j]", "“all rows, column j”", "the colon means “everything”. Grabs neuron j's own column"),
   ("shape (2,3)", "—", "2 inputs, 3 neurons")],
  "Careful: W[0] grabs a ROW, not a column. Different thing entirely, and NumPy won't warn you."),

"c2w1-shapes": plain(
  "Two things that look almost identical to a human and completely different to the computer. The "
  "extra pair of brackets is doing real work.",
  [("(2,)", "“shape two comma”", "a plain list of 2 numbers. No rows, no columns"),
   ("(1, 2)", "“shape one by two”", "a proper table: 1 row, 2 columns"),
   ("the trailing comma", "—", "Python's way of writing a one-item tuple. It is not a typo"),
   ("rows / columns", "—", "rows = examples, columns = features. Always")],
  "A bag of eggs versus an egg box. Same eggs; only the box says which is a row."),

"c2w1-dense-code": plain(
  "The slow, honest version. Walk along the columns of the trust table, one neuron at a time, and "
  "fill in its answer.",
  [("W.shape[1]", "“shape, index one”", "the number of COLUMNS = number of neurons"),
   ("W.shape[0]", "—", "the number of ROWS = number of inputs. NOT what you want here"),
   ("np.zeros(units)", "—", "an empty box with a slot for each answer"),
   ("for j in range(units)", "—", "do this once per neuron"),
   ("np.dot(w, a_in)", "—", "multiply the pairs and add them up")],
  "Using shape[0] instead of shape[1] gives you an answer of the wrong length — a very common bug."),

"c2w1-dense-vec": plain(
  "The same thing with the loop deleted. One instruction now does every neuron for every example at "
  "the same instant.",
  [("A_in", "“capital A in”", "ALL your examples stacked up, one per row"),
   ("np.matmul", "“mat-mul”", "matrix multiply — a whole grid of dot products at once"),
   ("@", "“at”", "shorthand for np.matmul"),
   ("B", "“capital B”", "the biases, one row"),
   ("broadcasting", "—", "NumPy quietly copying that one row down every row for you")],
  "Six lines like this, stacked, is a complete working neural network."),

"c2w1-matmul-rule": plain(
  "A test you can do in your head to check whether two tables can be multiplied, and what size the "
  "answer will be.",
  [("(m × n)", "“m by n”", "a table with m rows and n columns"),
   ("inner numbers", "—", "the two in the middle. They MUST match"),
   ("outer numbers", "—", "the two on the ends. They become your answer's size"),
   ("the inner number", "—", "gets added away and vanishes from the result")],
  "Write the two shapes side by side: (2×3)(3×4). Middles match → legal. Answer is (2×4)."),

"c2w1-dotprod": plain(
  "A neuron has to end up with ONE number. Multiplying lists item by item leaves you with a list, "
  "which is no use.",
  [("dot product", "—", "multiply the pairs AND add them up → one number"),
   ("elementwise", "—", "multiply the pairs and stop → still a list"),
   ("cos θ", "“cos theta”", "how much two arrows point the same way")],
  "A shopping list × a price list. Elementwise gives you each item's cost; the dot product gives you "
  "the total bill."),

"c2w1-vectorization": plain(
  "The maths behind neural networks is from 1958 and 1986. Three other things changed, and that is "
  "why they suddenly started working.",
  [("data", "—", "the internet supplied millions of labelled examples"),
   ("compute", "—", "graphics cards made the maths about 100× cheaper"),
   ("GPU", "“gee-pee-you”", "a graphics card: thousands of tiny calculators working at once"),
   ("scale behaviour", "—", "old methods stop improving with more data; big networks keep going")],
  "Nobody invented better maths. They got more examples and faster chips."),

"c2w2-three-steps": plain(
  "Training anything, in three moves — and they are the same three from Course 1, wearing "
  "TensorFlow's clothes.",
  [("Sequential", "“se-QUEN-shal”", "stack these layers, feed each into the next"),
   ("compile", "“com-PILE”", "write down the rules. Changes nothing yet"),
   ("loss=", "—", "which scoring rule to use"),
   ("fit", "“fit”", "actually train. The ONLY step that changes the numbers"),
   ("epochs", "“EP-ocks”", "how many times to go through the whole dataset")],
  "Like teaching a dog: name the trick, define what “wrong” means, then practise."),

"c2w2-bce": plain(
  "The scoring rule for yes/no answers, and a word distinction people get tested on.",
  [("L", "“ell” (loss)", "how wrong you were on ONE example"),
   ("J", "“jay” (cost)", "the AVERAGE loss over all your examples"),
   ("cross-entropy", "“cross-EN-tro-pee”", "the official name for this scoring rule"),
   ("log", "—", "turns a tiny probability into a huge penalty"),
   ("y", "—", "the true answer: 1 or 0")],
  "Loss = one exam question. Cost = your overall mark."),

"c2w2-relu": plain(
  "The simplest useful squasher there is: if the number is negative, say zero; otherwise pass it "
  "straight through. Two words of logic, and it beat the elegant S-curve.",
  [("ReLU", "“RAY-loo”", "Rectified Linear Unit. A blunt but very effective squasher"),
   ("max(0, z)", "“max of zero and z”", "whichever is bigger"),
   ("slope", "—", "how steep the squasher is. Learning needs slope"),
   ("saturate", "“SAT-you-rate”", "go flat, so it stops responding to anything"),
   ("vanishing gradient", "—", "the learning signal fading to nothing through deep stacks")],
  "Sigmoid's slope maxes out at 0.25. Multiply that through ten layers and you get 0.0000001 — "
  "the early layers hear nothing at all."),

"c2w2-dying-relu": plain(
  "ReLU's one weakness. A neuron that outputs zero for every single example gets no learning signal, "
  "so it can never fix itself. It's stuck forever.",
  [("dying ReLU", "—", "a neuron permanently stuck at zero"),
   ("gradient = 0", "—", "no learning signal, so the dials never move"),
   ("Leaky ReLU", "—", "a version with a tiny slope on the negative side, so it can recover")],
  "A light switch jammed off — and the only thing that could unjam it is the light being on."),

"c2w2-activation-choice": plain(
  "The last layer is the one that talks to you, so it has to speak the right language. The middle "
  "layers talk only to each other, so they don't need to be polite.",
  [("activation", "—", "the squasher applied at the end of a layer"),
   ("sigmoid", "“SIG-moid”", "answers between 0 and 1 → a chance"),
   ("linear", "“LIN-ee-ar”", "no squashing at all. Any number, positive or negative"),
   ("softmax", "“soft max”", "several chances that add up to 1"),
   ("ReLU", "—", "zero or positive. Also the default for every hidden layer")],
  "“Linear activation” and “no activation” are the same sentence."),

"c2w2-why-nonlinear": plain(
  "Tape two straight sticks together in a line and you get… a longer straight stick. Do it a hundred "
  "times and it's still straight. Something has to be allowed to bend.",
  [("W[¹], W[²]", "—", "the trust tables of two layers"),
   ("collapse", "—", "several layers turning out to be the same as one"),
   ("W′", "“W prime”", "the single table the two multiply out into"),
   ("non-linear", "—", "not a straight line. What lets the network bend")],
  "A hundred linear layers has exactly as much power as one. Not less accuracy — literally none extra."),

"c2w2-softmax": plain(
  "Ten judges shout scores; some are negative, some huge. Two moves turn them into “what share of "
  "the vote did each get”.",
  [("softmax", "—", "a gentle way of picking the biggest, letting the others keep a share"),
   ("e^z", "“e to the z”", "makes every score positive, and stretches the gaps"),
   ("Σ", "“sum of”", "add all of them up"),
   ("÷ Σ", "—", "divide by the total, so the shares add to exactly 1"),
   ("a_j", "—", "class j's share — its probability")],
  "The only squasher where each output depends on all the others. Push one up and the rest must "
  "come down — they share a fixed budget of 100%."),

"c2w2-softmax-shift": plain(
  "Softmax only cares about the GAPS between scores, not the scores themselves. Add the same amount "
  "to every score and nothing changes at all.",
  [("differences", "—", "the gaps between the z's. This is all softmax sees"),
   ("overflow", "“OH-ver-flow”", "a number too big for the computer to hold → infinity"),
   ("exp(z − max z)", "—", "subtract the biggest first, so nothing ever explodes")],
  "Like a race: adding 10 seconds to everyone's time changes nobody's position."),

"c2w2-from-logits": plain(
  "Computers store numbers with limited precision. Squash first and then take a log, and the answer "
  "can round away to nothing. Rearranging the sum avoids ever building the dangerous middle number.",
  [("logits", "“LOW-jits”", "the raw scores BEFORE any squashing"),
   ("from_logits=True", "—", "“I'll hand you raw scores, you do the squashing safely”"),
   ("float32", "—", "the computer's number format: about 7 useful digits"),
   ("rounds to 1.0", "—", "0.999999998 becomes exactly 1, and then log(1) = 0 — the error vanishes")],
  "The catch: predict() now hands back raw scores, not chances. Run tf.nn.softmax on them yourself."),

"c2w2-multiclass-vs-label": plain(
  "Two questions that look the same and are not: “which ONE is it?” versus “which of these are "
  "present?”",
  [("multi-class", "—", "exactly one answer is right. Cat OR dog OR horse"),
   ("multi-label", "—", "several can be right at once. Car AND bus AND person"),
   ("mutually exclusive", "“mew-chew-ally ex-CLOO-siv”", "only one can be true"),
   ("softmax", "—", "forces the answers to compete for one shared 100%"),
   ("sigmoid ×N", "—", "gives each question its own separate 100%")],
  "Use softmax for multi-label and the model literally cannot say “both”, however clear the photo."),

"c2w2-adam": plain(
  "Plain gradient descent uses one stride length for every dial. Adam gives each dial its own, and "
  "adjusts it as it goes: bigger strides where progress is steady, smaller where it keeps flip-flopping.",
  [("Adam", "“Adam”", "ADAptive Moment estimation. Not a person's name"),
   ("m", "“momentum”", "a running average of recent slopes. Steady direction → bigger steps"),
   ("v", "—", "a running average of SQUARED slopes: how bumpy this dial has been"),
   ("√v on the bottom", "—", "bumpier dial → smaller steps"),
   ("β₁, β₂", "“beta one, beta two”", "how much history to keep. 0.9 and 0.999. Rarely worth changing"),
   ("ε", "“epsilon”", "a tiny number, only there to avoid dividing by zero")],
  "Walking down a long narrow valley: long strides along the floor, tiny careful ones across it."),

"c2w2-conv": plain(
  "A dense neuron reads the entire picture. A convolutional one peeks through a small window — and "
  "every window uses the SAME set of trust levels.",
  [("convolutional", "“con-vo-LOO-shun-al”", "sliding a small detector across the input"),
   ("kernel / filter", "—", "the little detector. Just a few numbers, reused everywhere"),
   ("window", "—", "the small patch one neuron can see"),
   ("weight sharing", "—", "all the neurons use one shared detector. The key idea"),
   ("receptive field", "—", "how much of the original input one neuron ends up depending on")],
  "Learn “what an edge looks like” once, and you can spot edges anywhere in the picture for free."),

"c2w2-backprop-cost": plain(
  "The surprising fact that makes training possible at all: you can find out how ALL million dials "
  "affect the final answer in about two passes, not a million.",
  [("backpropagation", "“back-prop-a-GAY-shun”", "walking backwards through the network to get all "
    "the slopes at once"),
   ("forward pass", "—", "numbers flowing left to right, making a prediction"),
   ("backward pass", "—", "slopes flowing right to left"),
   ("N", "—", "how many parameters the network has")],
  "Testing each dial one at a time would need a million experiments. Backprop needs two."),

"c2w2-chain-rule": plain(
  "A chain of gears. Turn the first one and you want to know how far the last one moves. You don't "
  "need to understand the whole machine — just each pair, multiplied together.",
  [("chain rule", "—", "multiply the slopes along the path"),
   ("∂J/∂d", "“dee J by dee d”", "how much the score changes when d changes"),
   ("local slope", "—", "one node's own little multiplier"),
   ("∂J/∂J = 1", "—", "where the backward walk starts")],
  "A→B is ×2, B→C is ×3, C→D is ×0.5. So A→D is 2×3×0.5 = 3. That's the whole idea."),

"c2w2-mse-vs-bce": plain(
  "Using the Course 1 scoring rule here doesn't crash — it just trains badly, and for a sneaky "
  "reason: the learning signal goes quiet exactly where you need it loudest.",
  [("MSE", "“em-ess-ee”", "Mean Squared Error — the Course 1 scoring rule"),
   ("gradient", "—", "the learning signal"),
   ("confidently wrong", "—", "very sure, and very mistaken. Where the biggest fix is needed")],
  "The sigmoid and the log loss are a matched pair. Split them up and the tidiness disappears."),

"c2w3-diagnostic": plain(
  "Two numbers, and each one points at a different disease. Reading them correctly is most of what "
  "this week is worth.",
  [("J_train", "“J train”", "how wrong it is on the examples it has already studied"),
   ("J_cv", "“J see-vee”", "how wrong it is on examples it has never seen"),
   ("bias", "“BY-ass”", "too simple. Wrong even on the studied examples"),
   ("variance", "“VAIR-ee-ance”", "memorised. Fine on studied ones, bad on new ones"),
   ("the gap", "—", "J_cv minus J_train")],
  "J_train tells you about bias. The GAP tells you about variance. That one sentence is the whole "
  "diagnostic."),

"c2w3-three-sets": plain(
  "Split your data three ways, not two. The reason is subtle: the moment you use a number to make a "
  "CHOICE, that number stops being an honest measurement.",
  [("training set", "—", "used to set the dials"),
   ("cross-validation set", "“cross-val-i-DAY-shun”", "used to CHOOSE between models. Also called "
    "the dev set"),
   ("test set", "—", "opened once, at the very end, and never again"),
   ("biased", "—", "flattering, because you picked whatever happened to suit it")],
  "Study from a textbook, practise on mock papers, sit the real exam once. Marking yourself on the "
  "mocks and calling it your grade would be cheating."),

"c2w3-fix-table": plain(
  "Six things people try when a model is bad. Three help one disease and three help the other — and "
  "trying the wrong three wastes weeks.",
  [("high variance fixes", "—", "all make the model LESS flexible"),
   ("high bias fixes", "—", "all make the model MORE flexible"),
   ("λ", "“lambda”", "the stiffness dial. Up = stiffer, down = floppier"),
   ("polynomial features", "—", "adding x², x³ so the model can bend")],
  "You never have to memorise which is which. Ask: does this make the model bendier or stiffer?"),

"c2w3-more-data": plain(
  "The most expensive thing on the list, and it only cures one of the two diseases. Teams routinely "
  "spend months collecting data for a model that was never going to benefit.",
  [("high bias", "—", "cannot even fit what it already has. More of the same changes nothing"),
   ("high variance", "—", "memorising. More data leaves no room to memorise")],
  "Buying more textbooks doesn't help a student who has stopped being able to learn from books."),

"c2w3-baseline": plain(
  "“10.8% error” means nothing on its own. High compared to what? If people get 10.6% on the same "
  "task, you are nearly perfect.",
  [("baseline", "“BASE-line”", "what is realistically achievable — often human performance"),
   ("avoidable bias", "—", "the gap between the baseline and your training score. Worth chasing"),
   ("variance", "—", "the gap between your training score and your unseen score"),
   ("Bayes error", "“BAYZ error”", "the best ANY model could ever do. Some examples are just ambiguous")],
  "Getting 89% on a test is brilliant or terrible depending entirely on what everyone else got."),

"c2w3-learning-curves": plain(
  "Draw how wrong you are against how many examples you have. The SHAPE of those two lines tells you "
  "whether buying more data is worth it.",
  [("learning curve", "—", "error plotted against dataset size"),
   ("plateau", "“pla-TOE”", "gone flat and stopped improving"),
   ("the gap", "—", "distance between the two curves"),
   ("J_train rising", "—", "normal! Fitting 1000 points is harder than fitting 3")],
  "If both lines have already met and flattened, more data changes nothing. That is a very cheap way "
  "to say no to an expensive project."),

"c2w3-nn-recipe": plain(
  "A flowchart with two questions in it. Ask them in order and it tells you what to do next, every "
  "time.",
  [("does well on training?", "—", "if no, it is too small. Make it bigger"),
   ("does well on cv?", "—", "if no, it is memorising. Get more data or more stiffness"),
   ("regularisation", "—", "the stiffness setting that stops a big network memorising")],
  "A bigger network with proper stiffness is almost never worse than a small one — so “too big” is "
  "a bill, not a mistake."),

"c2w3-error-analysis": plain(
  "The highest-value hour in most projects, and it involves no maths at all. Read the mistakes. "
  "Sort them into piles. Count the piles.",
  [("error analysis", "—", "reading your model's mistakes by hand"),
   ("misclassified", "—", "the ones it got wrong"),
   ("cross-validation set", "—", "use these, NOT the test set"),
   ("~100 examples", "—", "enough to tell 20% from 3%. You are estimating, not auditing")],
  "The usual outcome: the thing everyone has been arguing about turns out to be 3 mistakes out of "
  "100, while a 21-out-of-100 pile had nobody working on it."),

"c2w3-augmentation": plain(
  "Turning one example into ten by bending it — but only in ways that could genuinely happen in real "
  "life.",
  [("augmentation", "“aug-men-TAY-shun”", "making new examples by distorting the ones you have"),
   ("representative", "—", "the distortion must be something the real world actually does"),
   ("training set only", "—", "never augment the data you score yourself on")],
  "Adding café noise to speech makes sense — you will meet noisy cafés. Adding random static to "
  "clean scans does not — you never will."),

"c2w3-transfer": plain(
  "Borrow a network somebody else spent a fortune training. Keep everything except the last layer, "
  "bolt your own last layer on, and train just that on your 50 examples.",
  [("transfer learning", "—", "reusing someone else's trained network for your own task"),
   ("pre-training", "—", "their expensive step, on a million general images"),
   ("fine-tuning", "—", "your cheap step, on your small specific set"),
   ("freeze", "—", "mark layers as “don't change these”"),
   ("output layer", "—", "the only part that genuinely depends on YOUR classes")],
  "Early layers learn what edges and textures are — and edges are edges whether the photo is a cat "
  "or a chest X-ray."),

"c2w3-precision-recall": plain(
  "Two different questions about the same mistakes, and everyone mixes them up. The trick is to "
  "remember what is on the BOTTOM of each fraction.",
  [("TP", "“true positive”", "you said yes and you were right"),
   ("FP", "“false positive”", "you said yes and you were wrong — a false alarm"),
   ("FN", "“false negative”", "you said no and you were wrong — you missed one"),
   ("precision", "“pre-SI-zhun”", "of everything you FLAGGED, how much was real?"),
   ("recall", "“re-CALL”", "of everything that WAS real, how much did you catch?")],
  "Precision's bottom is what you predicted. Recall's bottom is what was true. Hold onto that one "
  "difference and you'll never mix them up."),

"c2w3-accuracy-trap": plain(
  "When almost everything is “no”, a model that always says “no” scores brilliantly and is completely "
  "useless.",
  [("accuracy", "—", "the fraction you got right overall"),
   ("skewed", "“skyood”", "one class is much rarer than the other"),
   ("99.5% accurate", "—", "exactly what you get by never flagging anything, if 0.5% are positive")],
  "On rare-event problems, accuracy is basically measuring how rare the event is."),

"c2w3-f1": plain(
  "One number combining precision and recall — but NOT a plain average, because a plain average lets "
  "a useless model look decent.",
  [("F1", "“eff one”", "a single combined score"),
   ("harmonic mean", "“har-MON-ic”", "an average that leans hard towards the SMALLER number"),
   ("P, R", "—", "precision and recall")],
  "Precision 1.0 and recall 0.01: a plain average says 0.505, which flatters it. F1 says 0.02, which "
  "is the truth."),

"c2w3-threshold": plain(
  "The model hands you a chance. YOU decide what chance is high enough to act on — and that depends "
  "on what acting wrongly costs.",
  [("threshold", "“THRESH-old”", "the cutoff for saying yes. 0.5 is only a default"),
   ("raise it", "—", "only shout when very sure → fewer false alarms, more misses"),
   ("lower it", "—", "shout at anything suspicious → fewer misses, more false alarms")],
  "A missed cancer versus one extra scan is not the same trade as blocking a real customer's card. "
  "That is a business decision, not a maths one."),

"c2w3-fairness": plain(
  "One overall score can hide a group being served terribly, purely because that group is small.",
  [("subgroup", "—", "a slice of your users: by age, region, skin tone, language"),
   ("aggregate", "“AG-ri-git”", "the single overall number"),
   ("disparity", "“dis-PARR-ity”", "one group doing much worse than another"),
   ("proxy", "“PROX-ee”", "a feature that secretly stands in for another — postcode for income")],
  "If a group is 6% of your data you can fail them completely and the headline number barely twitches."),

"c2w3-leakage": plain(
  "Three ways your test score can be a lie, all of which leave you feeling great until you deploy.",
  [("leakage", "“LEEK-ij”", "test information sneaking into training"),
   ("shuffle", "—", "mix the rows before splitting, so both halves look alike"),
   ("time series", "—", "data in time order. Here you must NOT shuffle — split by date"),
   ("de-duplicate", "—", "make sure the same house/patient isn't in both halves")],
  "Like revising from a paper that turns out to contain the exam questions — the mark tells you "
  "nothing."),

"c2w4-tree-decisions": plain(
  "Building a tree needs only two answers, over and over: what question to ask next, and when to "
  "stop asking.",
  [("split", "—", "asking a question and dividing the examples into two groups"),
   ("pure", "—", "a group that is all one class"),
   ("max depth", "—", "how many questions deep you allow the tree to go"),
   ("leaf", "—", "a node that stops asking and just gives an answer")],
  "Every stopping rule exists for one reason: keeping the tree small. Depth is the tree's version of "
  "polynomial degree."),

"c2w4-entropy": plain(
  "A number for “how mixed up is this pile?”. All one thing → 0. Half and half → 1. And it doesn't "
  "care WHICH thing dominates.",
  [("entropy", "“EN-tro-pee”", "how messy or surprising a group is"),
   ("H(p)", "“H of p”", "the messiness score"),
   ("p", "—", "the fraction of the group that is the positive class"),
   ("log₂", "“log base two”", "base 2 means the answer comes out in “bits” — coin flips of surprise"),
   ("H = 0", "—", "perfectly pure. No surprise at all"),
   ("H = 1", "—", "exactly 50/50. Maximum surprise")],
  "H(0.8) and H(0.2) are both 0.72 — it only measures how lopsided the mix is, not which way."),

"c2w4-infogain": plain(
  "How much mess did this question clear up? Messiness before, minus messiness after — but weighted "
  "by how many examples went each way.",
  [("information gain", "—", "how much messiness the question removed"),
   ("H(root)", "—", "the mess before you asked"),
   ("w_left, w_right", "—", "the FRACTION of examples going each way. The bit people forget"),
   ("weighted", "—", "a tidy pile of 1 is worth less than a tidy pile of 9")],
  "Without the weights, splitting off one lonely example into its own perfect pile looks like a "
  "brilliant move every time."),

"c2w4-id-column": plain(
  "A column with a unique value per row scores a perfect result and teaches the model absolutely "
  "nothing.",
  [("cardinality", "“car-di-NAL-ity”", "how many different values a column has"),
   ("perfect purity", "—", "every leaf holds one example, so every leaf is “pure”"),
   ("memorisation", "—", "learning the answers rather than the pattern")],
  "“If the customer ID is 4471, it's a cat.” Perfectly true, and useless for customer 4472."),

"c2w4-continuous": plain(
  "Weight isn't “pointy or floppy” — it's a number. So the question becomes “is it under some "
  "cutoff?”, and the algorithm just tries every sensible cutoff.",
  [("continuous", "“con-TIN-you-us”", "a number that can take any value, not a category"),
   ("threshold", "—", "the cutoff point for the question"),
   ("midpoint", "—", "halfway between two neighbouring values. The only cutoffs worth trying"),
   ("m − 1", "—", "with m examples there are only that many useful cutoffs")],
  "This is also why trees never need feature scaling: they only ever COMPARE numbers, never add them."),

"c2w4-regtree": plain(
  "Same tree, different question: predict a number instead of a category. One word gets swapped and "
  "everything else stays.",
  [("regression tree", "—", "a tree that predicts a number"),
   ("variance", "“VAIR-ee-ance”", "how spread out a group of numbers is"),
   ("variance reduction", "—", "the number version of information gain"),
   ("mean", "—", "the plain average. What each leaf predicts"),
   ("step function", "—", "flat within each leaf, jumping at the boundaries")],
  "Entropy asks “are these all the same LABEL?”. Variance asks “are these all the same NUMBER?”. "
  "Same job, different data type."),

"c2w4-onehot": plain(
  "You cannot number unordered categories, because numbering implies an order that isn't there. So "
  "give each category its own yes/no column instead.",
  [("one-hot", "—", "exactly ONE column is 1 (“hot”), the rest are 0"),
   ("categorical", "“cat-e-GOR-ic-al”", "a column of labels, not numbers"),
   ("ordinal", "“OR-din-al”", "categories that DO have an order — small, medium, large"),
   ("dummy variables", "—", "the statisticians' name for the same trick")],
  "Coding red=0, green=1, blue=2 tells the model blue is bigger than red and twice green. It is not."),

"c2w4-why-ensemble": plain(
  "One tree is fragile. The very first question is picked by a razor-thin margin, and if it flips, "
  "every question underneath it changes too.",
  [("high variance", "—", "swap one example and you get a very different model"),
   ("root split", "—", "the first question. Everything below depends on it"),
   ("argmax", "“arg max”", "“whichever scores highest” — even by 0.003"),
   ("ensemble", "“on-SOM-bull”", "several models voting together")],
  "Averaging only helps if the models make DIFFERENT mistakes. Three identical trees vote identically."),

"c2w4-bootstrap": plain(
  "Put ten marbles in a bag. Draw one, write it down, PUT IT BACK, repeat ten times. You get ten "
  "marbles — but not the same ten. Some appear twice; some never come out.",
  [("bootstrap", "—", "sampling with replacement to fake a fresh dataset"),
   ("with replacement", "—", "put it back each time, so it can be drawn again"),
   ("63%", "—", "roughly how many of the originals show up in one bag"),
   ("out-of-bag", "—", "the ~37% left out. A free test set for that tree"),
   ("bagging", "—", "Bootstrap AGGregating: do this many times and combine")],
  "Without putting it back, you'd just draw all ten every time and every tree would be identical."),

"c2w4-random-forest": plain(
  "Many trees, each grown on its own bag of data AND allowed to consider only a random handful of "
  "questions at each step. That second restriction is what makes it work.",
  [("random forest", "—", "many trees, voting"),
   ("B", "—", "how many trees. 100 is a fine default"),
   ("k ≈ √n", "“square root of n”", "how many features each split may choose from"),
   ("feature bagging", "—", "randomising the COLUMNS as well as the rows"),
   ("majority vote", "—", "whichever answer most trees gave")],
  "Without the feature restriction, one strong column wins the first question in nearly every tree "
  "and they all end up alike."),

"c2w4-boosting": plain(
  "Random forest: a hundred students each revising a random chunk. Boosting: one student who marks "
  "their own test and revises only the questions they got wrong.",
  [("boosting", "—", "trees built one after another, each fixing the last one's mistakes"),
   ("sequential", "“se-QUEN-shal”", "in order, one at a time. Cannot be done in parallel"),
   ("XGBoost", "“ex-gee-boost”", "eXtreme Gradient Boosting — a very fast implementation"),
   ("early stopping", "—", "stop adding trees when the validation score stops improving")],
  "It's a far more efficient use of effort, and it's why boosted trees usually win on spreadsheets."),

"c2w4-boost-shallow": plain(
  "Each tree in a boosted model only has to nudge things slightly. The power comes from having many "
  "of them, not from any one being clever.",
  [("shallow", "—", "only 3 to 6 questions deep"),
   ("residual", "“re-ZID-you-al”", "what's left over — the error still remaining"),
   ("weak learner", "—", "a deliberately simple model. The building block of boosting")],
  "Deep trees would overfit their leftovers, and the sequential process would amplify that mistake "
  "with every round."),

"c2w4-tree-vs-nn": plain(
  "Different tools for different shapes of data — and one property that only neural networks have.",
  [("tabular", "“TAB-you-lar”", "spreadsheet data: rows and columns of numbers and categories"),
   ("composability", "“com-POSE-ability”", "being able to bolt models together and train them as one"),
   ("differentiable", "“diff-er-EN-shable”", "you can compute slopes through it, so gradients flow")],
  "Tree splits are yes/no decisions with no useful slope, so you cannot chain trees the way you "
  "chain networks. That single property is why deep learning scaled."),


"c2w1-drill-forwardprop": plain(
  "A neuron weighs each input by how much it trusts it, adds a starting bias, and squashes the total "
  "into 0\u20261 with the sigmoid curve. Two inputs, two weights, one bias, one squash.",
  [("w", "“double-you”", "how much this neuron trusts each input"),
   ("b", "“bee”", "the neuron's default mood before seeing any input"),
   ("z", "“zee”", "the raw weighted total, before squashing"),
   ("a", "“ay”", "the squashed output \u2014 what the neuron actually passes on")],
  "z came out negative, so after squashing a landed below 0.5 \u2014 this neuron stays quiet."),

"c2w2-drill-softmax": plain(
  "Turn four raw scores into four probabilities that add up to 1. Bigger raw scores get "
  "disproportionately bigger shares \u2014 exponentiating stretches the gaps apart before sharing "
  "out the total.",
  [("e", "“e”", "Euler's number, about 2.718 \u2014 the base every score gets raised to"),
   ("a\u2084", "“a four”", "the share of probability given to the 4th, largest score")],
  "Score 4 was only 4 times bigger than score 1, but ends up with about 20 times more of the "
  "probability \u2014 softmax rewards the leader more than it looks like it should."),

"c2w4-drill-entropy": plain(
  "Ask: how mixed is this group? All-one-class is perfectly tidy (entropy 0). A dead-even 50/50 mix "
  "is the messiest it can be (entropy 1). 8 cats out of 10 sits closer to tidy than messy.",
  [("p", "“pee”", "the fraction belonging to one class \u2014 here, 0.8 are cats"),
   ("H", "“aitch”", "the entropy \u2014 the messiness score, from 0 to 1"),
   ("log\u2082", "“log base two”", "a log using 2 instead of 10 \u2014 keeps the answer between 0 and 1")],
  "Think of it as a measure of surprise: guessing the class of a random animal from this group is "
  "fairly easy (low surprise), because most of them are cats."),

}
