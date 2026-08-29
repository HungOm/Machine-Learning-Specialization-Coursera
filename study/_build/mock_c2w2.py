# -*- coding: utf-8 -*-
"""Mock quiz — C2 W2."""
from mockkit import Q, O, SET

SET = SET("C2", 2, "Neural Network Training",
"""Training in TensorFlow, activation functions, softmax and the numerical-stability flag. The
activation questions separate the output layer from the hidden layers — so does the real quiz.""", [

Q("c2w2-q01",
  "<p>What do the three steps <code>Sequential</code>, <code>compile</code> and <code>fit</code> "
  "correspond to?</p>",
  [O("The model, the cost function, and gradient descent", True,
     "Exactly the three objects you built by hand in C1. Every training script you write is these "
     "three, elaborated."),
   O("The data, the model, and the prediction", False,
     "Data is passed <em>to</em> fit; prediction is a separate call afterwards."),
   O("Forward propagation, backpropagation, and evaluation", False,
     "Forward and backward passes both happen inside <code>fit</code>. They are not separate API "
     "steps."),
   O("Initialisation, regularisation, and optimisation", False,
     "Initialisation is automatic and regularisation is an argument to a layer, not one of the three "
     "calls.")],
  "c2/w2-02-training-details.html", tag="the three steps",
  note="Model, loss, optimiser is the organising structure of every deep learning framework."),

Q("c2w2-q02",
  "<p>Which activation should you use in the <b>hidden</b> layers of most networks, and why?</p>",
  [O("ReLU, because its gradient does not vanish for positive inputs", True,
     "The derivative is exactly 1 on the positive side, so gradients survive many layers of the chain "
     "rule. The sigmoid's derivative peaks at 0.25 and multiplying ten of those leaves almost "
     "nothing."),
   O("Sigmoid, because it produces probabilities", False,
     "Probabilities are wanted at the <em>output</em>, not internally — and the sigmoid is exactly "
     "the function that causes vanishing gradients in hidden layers."),
   O("Linear, because it keeps the maths simple", False,
     "A stack of linear layers collapses to a single linear layer, so the network gains nothing from "
     "depth. This is the point of the &ldquo;why do we need activations?&rdquo; lesson."),
   O("Softmax, because it normalises the outputs", False,
     "Softmax couples all units in a layer and is for a multiclass output. Using it internally makes "
     "no sense.")],
  "c2/w2-03-sigmoid-alternatives.html", tag="hidden activations"),

Q("c2w2-q03",
  "<p>Match the output activation to the task. Which pairings are correct?</p>",
  [O("Binary classification &rarr; sigmoid", True,
     "One output, squashed to (0, 1) — a probability for the positive class."),
   O("Regression, any real value &rarr; linear", True,
     "No activation at all. Anything else caps the range, which is why a sigmoid on a price model "
     "silently prevents predictions above 1."),
   O("Multiclass, exactly one correct &rarr; softmax", True,
     "Softmax couples the outputs so they sum to 1, which is what &ldquo;exactly one&rdquo; means."),
   O("Multi-label, several can be true &rarr; softmax", False,
     "This is the architecture bug the multi-label lesson warns about. Softmax forces the outputs to "
     "compete; use independent sigmoids instead."),
   O("Regression, output must be positive &rarr; sigmoid", False,
     "Sigmoid caps at 1. ReLU is the right choice for a non-negative unbounded quantity.")],
  "c2/w2-04-choosing-activations.html", tag="output activations",
  note="The output activation follows from the range of y. The hidden one is ReLU by default."),

Q("c2w2-q04",
  "<p>What does <code>from_logits=True</code> do, and why does it matter?</p>",
  [O("It hands raw scores to the loss, which computes softmax and log together more stably", True,
     "Computing the probability and then its log loses precision. Done together, the intermediate "
     "never has to exist — which is what prevents exp overflow and log(0) producing NaN."),
   O("It converts the labels to one-hot vectors", False,
     "Label encoding is handled by which loss you choose — sparse or otherwise — not by this flag."),
   O("It makes training faster by skipping the activation", False,
     "The softmax still happens; it happens <em>inside</em> the loss. The gain is numerical, not "
     "speed."),
   O("It applies regularization to the output layer", False,
     "Regularization is set on layers via kernel_regularizer, and is unrelated.")],
  "c2/w2-09-improved-softmax.html", tag="numerical stability",
  note="If your loss goes to NaN a few hundred steps in, this is the first thing to check."),

Q("c2w2-q05",
  "<p>Softmax outputs for a 4-class problem are <span class=\"v\">[0.1, 0.6, 0.25, 0.05]</span>. "
  "Which are true?</p>",
  [O("They sum to 1", True,
     "Softmax always normalises, which is what makes the outputs a distribution over the classes."),
   O("The predicted class is the second one", True,
     "The argmax. 0.6 is the largest."),
   O("Raising the second logit would lower all the others", True,
     "Softmax is a function of all logits at once. The outputs are coupled — which is exactly why it "
     "is wrong for multi-label problems."),
   O("The model is 60% accurate", False,
     "Accuracy is measured over a dataset. This is one prediction's confidence, not a performance "
     "metric."),
   O("Each output can be interpreted independently of the others", False,
     "They cannot. That independence is what sigmoid outputs have and softmax outputs do not.")],
  "c2/w2-07-softmax.html", tag="softmax outputs"),

Q("c2w2-q06",
  "<p>Why does a network need non-linear activation functions at all?</p>",
  [O("Without them, any stack of layers collapses into a single linear model", True,
     "A composition of linear functions is linear. Ten layers with no activation have exactly the "
     "expressive power of one, and all the depth is wasted."),
   O("Without them the gradients vanish", False,
     "Vanishing gradients are caused <em>by</em> certain activations, notably the sigmoid. Removing "
     "activations does not cause them."),
   O("Because TensorFlow requires one", False,
     "It does not — <code>activation=None</code> is legal, and used deliberately for a linear output "
     "layer."),
   O("To keep the outputs between 0 and 1", False,
     "Some activations do that; ReLU does not, and it is the standard hidden choice.")],
  "c2/w2-05-why-activations.html", tag="why non-linearity"),

Q("c2w2-q07",
  "<p>What does the Adam optimiser do that plain gradient descent does not?</p>",
  [O("It adapts a separate learning rate for each parameter as training proceeds", True,
     "Parameters with consistently small gradients get larger effective steps and vice versa, so you "
     "spend far less time hand-tuning a single global &alpha;."),
   O("It guarantees finding the global minimum", False,
     "No optimiser guarantees that on a non-convex surface. Adam converges faster and more reliably; "
     "it does not change what minima exist."),
   O("It removes the need for a learning rate entirely", False,
     "You still supply an initial learning rate. Adam adapts around it."),
   O("It computes exact second derivatives", False,
     "It uses running averages of the gradient and its square — cheap first-order statistics, not a "
     "true Hessian.")],
  "c2/w2-11-advanced-optimization.html", tag="Adam"),

Q("c2w2-q08",
  "<p>You are classifying images that may contain a car, a bus and a pedestrian, any combination. "
  "What should the output layer be?</p>",
  [O("3 units with sigmoid activations, and a binary cross-entropy loss on each", True,
     "Three independent yes/no questions. The outputs need not sum to 1, and each can be read on its "
     "own."),
   O("3 units with a softmax activation", False,
     "Softmax forces exactly one answer. The model would never report a car and a pedestrian "
     "together, no matter how much data you gave it — the architecture forbids it."),
   O("1 unit with a sigmoid activation", False,
     "One unit answers one question. You have three."),
   O("8 units with softmax, one per combination", False,
     "This technically works and scales terribly — 2<sup>n</sup> classes — and it cannot share "
     "evidence between combinations that contain the same object.")],
  "c2/w2-10-multi-label.html", tag="multi-label vs multiclass",
  note="Can two answers be true at once? Yes &rarr; sigmoids. No &rarr; softmax."),

Q("c2w2-q09",
  "<p>What is a <b>derivative</b>, in the sense used by gradient descent?</p>",
  [O("How much the output changes when you nudge the input by a tiny amount", True,
     "A rate of change — the slope of the tangent at that point. Steep slope, big step; flat slope, "
     "small step, which is why descent slows near a minimum without being told to."),
   O("The value of the function at that point", False,
     "That is the function itself. The derivative describes how it is <em>changing</em> there."),
   O("The area under the curve", False,
     "That is the integral — the opposite operation."),
   O("The difference between the prediction and the label", False,
     "That is the error. The derivative of the cost happens to involve it, but they are not the same "
     "thing.")],
  "c2/w2-13-what-is-a-derivative.html", tag="derivatives"),

Q("c2w2-q10",
  "<p>What does backpropagation on a computation graph actually do?</p>",
  [O("Applies the chain rule backwards, computing each node's effect on the final loss", True,
     "One backward walk over the same graph the forward pass built, attributing the loss one link at "
     "a time. It costs about the same as the forward pass, which is what makes training large "
     "networks affordable."),
   O("Re-runs the forward pass many times with slightly different weights", False,
     "That is numerical differentiation. It is far more expensive and is used only to check an "
     "implementation."),
   O("Updates the weights directly", False,
     "It computes gradients. The optimiser then uses them to update — two separate steps."),
   O("Searches for the best network architecture", False,
     "The architecture is fixed before training. Searching over architectures is a different activity "
     "entirely.")],
  "c2/w2-14-computation-graph.html", tag="backpropagation"),
])
