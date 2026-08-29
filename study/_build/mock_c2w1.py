# -*- coding: utf-8 -*-
"""Mock quiz — C2 W1."""
from mockkit import Q, O, SET

SET = SET("C2", 1, "Neural Networks",
"""Layers, forward propagation, TensorFlow shapes and matrix multiplication. Half the marks on the
real quiz for this week are shape questions, so most of these are too.""", [

Q("c2w1-q01",
  "<p>A hidden layer has 4 inputs and 3 units. How many parameters does it have?</p>",
  [O("15", True,
     "12 weights (4 inputs &times; 3 units) plus 3 biases, one per unit. Weights are inputs &times; "
     "units; biases match the unit count."),
   O("12", False,
     "This counts the weights and forgets the biases. Every unit has its own bias."),
   O("7", False,
     "This adds inputs and units rather than multiplying. Each unit needs a weight for <em>every</em> "
     "input."),
   O("21", False,
     "This looks like 4&times;3 plus 3&times;3. Only one weight matrix is involved in one layer.")],
  "c2/w1-04-neural-network-layer.html", tag="counting parameters"),

Q("c2w1-q02",
  "<p>What does a single unit in a hidden layer compute?</p>",
  [O("A weighted sum of its inputs, plus a bias, passed through an activation function", True,
     "Exactly logistic regression, if the activation is a sigmoid. A layer is several of these run "
     "side by side on the same inputs — no new idea, just repetition."),
   O("The average of its inputs", False,
     "An average is a weighted sum with all weights equal to 1/n. A unit learns its weights, and they "
     "are rarely equal."),
   O("The largest of its inputs", False,
     "That is a max-pooling operation, which appears in convolutional networks and is not what a "
     "dense unit does."),
   O("A probability distribution over its inputs", False,
     "That describes softmax, which acts on a whole layer's outputs at once. A single unit produces "
     "one number.")],
  "c2/w1-04-neural-network-layer.html", tag="what a unit does"),

Q("c2w1-q03",
  "<p>In TensorFlow, why must a single example be written <code>[[200, 17]]</code> rather than "
  "<code>[200, 17]</code>?</p>",
  [O("The first dimension is always the batch, even when the batch is one", True,
     "The library expects a 2-D array of rows. One example is a table with one row — slightly absurd "
     "for a single case, and the reason nothing has to change for a million."),
   O("Because there are two features", False,
     "The number of features is the <em>second</em> dimension. The extra bracket is about rows, not "
     "columns."),
   O("Because TensorFlow requires integers in a nested list", False,
     "The dtype is unrelated. The requirement is about rank — how many dimensions the array has."),
   O("It is only needed during training, not inference", False,
     "It is needed for both. This is one of the most common first-day errors, and it appears at "
     "prediction time as often as in training.")],
  "c2/w1-08-data-in-tensorflow.html", tag="TensorFlow shapes"),

Q("c2w1-q04",
  "<p>What is the result shape of multiplying a <span class=\"v\">(3&times;2)</span> matrix by a "
  "<span class=\"v\">(2&times;4)</span> matrix?</p>",
  [O("3&times;4", True,
     "Write the shapes side by side, check the touching pair agrees (2 and 2), and cross them out. "
     "What remains — 3 and 4 — is the answer."),
   O("2&times;2", False,
     "This keeps the inner dimensions, which are exactly the ones that cancel."),
   O("4&times;3", False,
     "The right shape, transposed. Order matters: the first matrix supplies the rows."),
   O("The multiplication is not defined", False,
     "It is defined precisely because the inner dimensions match. It would be undefined if they "
     "did not.")],
  "c2/w1-15-matmul-rules.html", tag="matrix shapes",
  note="Check the shapes on paper before writing the code. It removes most shape bugs in advance."),

Q("c2w1-q05",
  "<p>Which are true of forward propagation?</p>",
  [O("It computes the prediction, layer by layer, from input to output", True,
     "One direction, one pass. Each layer's output becomes the next layer's input."),
   O("Each layer's computation uses only the previous layer's output and its own parameters", True,
     "A layer knows nothing about the layers beyond it, or about the loss. That locality is what "
     "makes stacking work."),
   O("It is used at both training and prediction time", True,
     "Training runs it and then computes gradients; prediction runs it and stops. It is the same "
     "computation."),
   O("It adjusts the weights to reduce the cost", False,
     "That is the backward pass and the optimiser. Forward propagation only evaluates — it changes "
     "nothing."),
   O("It requires the labels y", False,
     "No labels are involved. That is why it works at prediction time, where no label exists.")],
  "c2/w1-06-forward-propagation.html", tag="forward propagation"),

Q("c2w1-q06",
  "<p>A network is described as having 4 layers. By the usual convention, what does this mean?</p>",
  [O("3 hidden layers plus the output layer", True,
     "Hidden layers plus the output layer are counted; the input is not a layer because it computes "
     "nothing — it is just the data."),
   O("4 hidden layers plus an input and an output layer", False,
     "That would be a 5-layer network by the standard count."),
   O("The input, 2 hidden layers, and the output", False,
     "This counts the input layer, which the convention excludes."),
   O("4 units in a single layer", False,
     "Layers and units are different things. A layer's width is its unit count.")],
  "c2/w1-05-more-complex-networks.html", tag="counting layers"),

Q("c2w1-q07",
  "<p>What does <code>Dense(units=3, activation='sigmoid')</code> create?</p>",
  [O("A layer with 3 units, each with its own weights, bias and sigmoid", True,
     "That one line is W, b and the activation, all three. The input width is inferred from whatever "
     "you feed it."),
   O("A layer with 3 inputs", False,
     "<code>units</code> is the number of <em>outputs</em>. The input count comes from the previous "
     "layer."),
   O("Three separate layers", False,
     "One layer, three units within it. Stacking layers is what the list in "
     "<code>Sequential</code> does."),
   O("A layer with 3 weights", False,
     "Each of the 3 units has a full weight vector, so with 4 inputs there are 12 weights and 3 "
     "biases.")],
  "c2/w1-07-tensorflow-inference-code.html", tag="the Dense layer"),

Q("c2w1-q08",
  "<p>In NumPy, what is the difference between <code>A @ B</code> and <code>A * B</code>?</p>",
  [O("<code>@</code> is matrix multiplication; <code>*</code> multiplies elementwise", True,
     "Two characters apart, entirely different operations — and both will run silently on compatible "
     "shapes, which is what makes the confusion dangerous."),
   O("They are the same, and <code>@</code> is newer syntax", False,
     "They compute different things. <code>@</code> is newer syntax for <code>np.matmul</code>, not "
     "for <code>*</code>."),
   O("<code>*</code> is matrix multiplication; <code>@</code> is elementwise", False,
     "Reversed. In MATLAB <code>*</code> is matrix multiply, which is a common source of this "
     "mix-up."),
   O("<code>@</code> only works on square matrices", False,
     "It works on any pair whose inner dimensions agree.")],
  "c2/w1-16-matmul-code.html", tag="NumPy operators"),

Q("c2w1-q09",
  "<p>You write your own layer and store <span class=\"v\">W</span> so that each unit's weights are "
  "a <b>column</b>. Why does the convention matter?</p>",
  [O("Getting it backwards can still run without error while learning nothing", True,
     "If the dimensions happen to be compatible, the arithmetic proceeds and the numbers are "
     "meaningless. Nothing raises, which makes it the classic silent failure of a hand-written "
     "layer."),
   O("Because NumPy requires columns", False,
     "NumPy has no opinion. It is a convention you must apply consistently, and this course uses "
     "columns for units."),
   O("Because it makes the code faster", False,
     "Memory layout has some effect at very large scale, but that is not why the convention matters "
     "here."),
   O("Because biases must be rows", False,
     "The bias is a vector added by broadcasting; its orientation follows from the output shape.")],
  "c2/w1-10-forward-prop-single-layer.html", tag="weight layout"),

Q("c2w1-q10",
  "<p>Which statement about the relationship between neural networks and the brain is most "
  "accurate?</p>",
  [O("The name was borrowed as a loose analogy; the models are not descriptions of biology", True,
     "A unit here is a weighted sum and a nonlinearity. A real neuron has thousands of synapses, its "
     "own chemistry, and timing that carries information. The metaphor was fruitful and it is not a "
     "description."),
   O("Neural networks simulate biological neurons accurately", False,
     "They do not, and no one working on them claims otherwise. Computational neuroscience uses "
     "quite different models."),
   O("Deep networks are known to reach general intelligence by scaling", False,
     "This is exactly the extrapolation the AGI lesson warns against. Rapid progress on narrow tasks "
     "is not evidence about a different category of capability."),
   O("The analogy is useless and should be discarded", False,
     "Too strong. It motivated the architecture and still supplies useful intuition — it simply must "
     "not be mistaken for a claim about biology.")],
  "c2/w1-12-path-to-agi.html", tag="the brain analogy"),
])
