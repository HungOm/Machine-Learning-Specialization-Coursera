# -*- coding: utf-8 -*-
"""Mock quiz — C2 W3."""
from mockkit import Q, O, SET

SET = SET("C2", 3, "Advice for Applying ML",
"""Bias, variance, baselines, learning curves and error metrics. This is the week the graded quiz
leans on hardest, because every question is a diagnosis rather than a fact.""", [

Q("c2w3-q01",
  "<p>Training error 12%, cross-validation error 13%, human-level performance 3%. What is the "
  "problem, and what should you do?</p>",
  [O("High bias — try a bigger network or more features", True,
     "The gap that matters is baseline&rarr;training: 9 points. Training&rarr;CV is only 1 point, so "
     "variance is not the issue. The model is not capable enough."),
   O("High variance — collect more training data", False,
     "More data closes a training&rarr;CV gap, and that gap is 1 point. You would be spending months "
     "fixing a problem you do not have."),
   O("High variance — increase &lambda;", False,
     "Increasing &lambda; makes the model <em>less</em> flexible, which worsens a bias problem."),
   O("The model is performing well; ship it", False,
     "12% against a human baseline of 3% is a four-fold error rate. There is substantial headroom.")],
  "c2/w3-06-baseline-performance.html", tag="diagnosing bias",
  note="Read the two gaps, not the three numbers: baseline&rarr;training is bias, training&rarr;CV is variance."),

Q("c2w3-q02",
  "<p>Why is a three-way train / cross-validation / test split preferred over just train / test?</p>",
  [O("Choosing a model on the test set makes the test score optimistic", True,
     "Try twenty models and report the best test score, and you have fitted the test set with twenty "
     "attempts. The number is no longer an unbiased estimate of new-data performance."),
   O("Because two splits do not provide enough training data", False,
     "Three splits give you <em>less</em> training data, not more. The reason is about honesty of the "
     "estimate."),
   O("Because the test set must be larger than the training set", False,
     "It is normally much smaller — often 20% or less."),
   O("Because cross-validation is required for gradient descent to converge", False,
     "Convergence is entirely unrelated to how you split the data.")],
  "c2/w3-03-model-selection.html", tag="data splits",
  note="Every decision you make on a set costs you the right to use it as an unbiased estimate."),

Q("c2w3-q03",
  "<p>Your learning curves show training and cross-validation error close together, both flat and "
  "both high, at the right-hand edge. Which are true?</p>",
  [O("This is high bias", True,
     "Both errors are high and the gap is small. The model is not capable enough to fit the pattern."),
   O("Collecting more data will not help", True,
     "The curves have already met and flattened. More data closes a gap, and there is no gap to "
     "close — this is the single most valuable thing a learning curve tells you."),
   O("A more flexible model might help", True,
     "More features, a higher polynomial degree, a bigger network, or less regularisation are the "
     "bias fixes."),
   O("You should increase &lambda;", False,
     "That reduces flexibility further, making a bias problem worse."),
   O("The model has overfitted", False,
     "Overfitting shows as a large persistent <em>gap</em>. Here there is barely any.")],
  "c2/w3-07-learning-curves.html", tag="reading learning curves"),

Q("c2w3-q04",
  "<p>A dataset is 99.5% negative. Your model predicts &ldquo;negative&rdquo; for everything. What "
  "are its accuracy, precision and recall?</p>",
  [O("Accuracy 99.5%, recall 0%, precision undefined", True,
     "It gets every negative right and every positive wrong. Recall is 0/all-positives = 0. Precision "
     "is 0/0 — it never made a positive prediction — which is why accuracy is useless on skewed "
     "data."),
   O("Accuracy 99.5%, recall 100%, precision 99.5%", False,
     "Recall counts the positives it found, and it found none."),
   O("Accuracy 50%, recall 0%, precision 0%", False,
     "Accuracy is the fraction of all predictions that are right, and 99.5% of them are."),
   O("All three are 99.5%", False,
     "This is the trap the whole lesson exists to prevent. Only accuracy is high, and it is high for "
     "a worthless model.")],
  "c2/w3-16-skewed-datasets.html", tag="skewed data",
  note="On skewed data, always report precision and recall. Accuracy hides a useless model."),

Q("c2w3-q05",
  "<p>You raise the classification threshold from 0.5 to 0.8. What happens?</p>",
  [O("Precision rises and recall falls", True,
     "You make fewer positive predictions and are more sure of each, so a higher share are correct — "
     "and you miss more of the true positives."),
   O("Precision falls and recall rises", False,
     "That is what <em>lowering</em> the threshold does."),
   O("Both rise", False,
     "They move in opposite directions. If a change improved both, you would have a better model, not "
     "a different operating point."),
   O("The model is retrained with different weights", False,
     "The model does not change at all. The threshold is applied to its output after training, which "
     "is why one trained model gives you a whole curve of operating points.")],
  "c2/w3-17-precision-recall-tradeoff.html", tag="threshold",
  note="Which way you move it is a business decision about which error costs more."),

Q("c2w3-q06",
  "<p>You have 100 misclassified emails. Error analysis shows 43 are pharmaceutical spam and 5 use "
  "deliberate misspellings. What follows?</p>",
  [O("Work on pharmaceutical spam first — it is 43% of your errors", True,
     "Fixing the misspelling category perfectly buys 5% of your errors. Fixing the pharmaceutical "
     "category buys 43%. Same effort, eight times the return."),
   O("Work on misspellings first — they are harder and more interesting", False,
     "This is the most common way strong engineers waste time: solving the most interesting failure "
     "rather than the most common one."),
   O("Collect more training data before analysing further", False,
     "Error analysis is an afternoon and tells you <em>which</em> data to collect. Doing it first is "
     "what makes the collection targeted."),
   O("Both categories deserve equal effort", False,
     "The whole point of counting is that they do not. A tally exists to rank the work.")],
  "c2/w3-11-error-analysis.html", tag="error analysis",
  note="Manual, unglamorous, no library for it — and it routinely beats a week of tuning."),

Q("c2w3-q07",
  "<p>Which of these are valid data augmentations for a photo classifier?</p>",
  [O("Rotating the image by 15 degrees", True,
     "A plausible thing that happens to real photographs, so it teaches the model something true "
     "about deployment."),
   O("Changing the brightness or contrast", True,
     "Lighting genuinely varies. This is one of the most effective augmentations in practice."),
   O("Adding realistic blur", True,
     "Real cameras produce blurred photographs, especially handheld ones."),
   O("Adding uniform random noise to every pixel", False,
     "This distortion does not occur in deployment, and augmentations that do not reflect reality "
     "reliably fail to help. The test is always: would this really happen?"),
   O("Mirroring handwritten digits left-to-right", False,
     "A mirrored 2 is not a 2. Mirroring is fine for cats and catastrophic here, which shows how "
     "domain-specific the choice is.")],
  "c2/w3-12-adding-data.html", tag="data augmentation"),

Q("c2w3-q08",
  "<p>You have 500 labelled medical scans and want to use a network pre-trained on ImageNet. What is "
  "the sensible approach?</p>",
  [O("Replace the output layer, freeze the early layers, and train only the new head", True,
     "With very little data, unfreezing everything destroys the pre-trained weights. The early layers "
     "learned edges and textures, which are as true of scans as of photographs."),
   O("Train the whole network from random initialisation", False,
     "500 examples is nowhere near enough. This discards the most valuable thing you have — someone "
     "else's 14 million images."),
   O("Unfreeze everything and fine-tune at a high learning rate", False,
     "A high learning rate on 500 examples will wreck the pre-trained features in a few steps. This "
     "is the most common way transfer learning is misapplied."),
   O("Use the pre-trained network's predictions directly with no training", False,
     "Its output layer predicts ImageNet categories — dogs, boats. It has no notion of your "
     "classes.")],
  "c2/w3-13-transfer-learning.html", tag="transfer learning"),

Q("c2w3-q09",
  "<p>What is the recommended loop for a neural network when you have adequate compute and can obtain "
  "data?</p>",
  [O("Does it do well on training? No &rarr; bigger network. Yes, but not on CV? &rarr; more data. "
     "Repeat.", True,
     "Two questions and a loop. It works because a large, well-regularised network rarely does worse "
     "than a small one — which broke the classical bias&ndash;variance trade-off."),
   O("Always start with the largest possible network", False,
     "The loop starts small and grows. Starting enormous wastes compute and slows every iteration of "
     "the diagnosis."),
   O("Tune &lambda; first, then decide on the architecture", False,
     "Architecture comes first; &lambda; is tuned once a model is big enough to overfit."),
   O("Collect data until training error reaches zero", False,
     "More data does not reduce training error — it usually increases it, because there is more to "
     "fit.")],
  "c2/w3-09-bias-variance-neural-networks.html", tag="the NN recipe"),

Q("c2w3-q10",
  "<p>A hiring model shows equal overall accuracy but a much higher false-negative rate for one "
  "group. Which are true?</p>",
  [O("Aggregate accuracy can hide this entirely", True,
     "One number over the whole population averages the groups together. The gap is invisible unless "
     "you split the metric, which is the entire technique."),
   O("Removing the protected attribute may not fix it", True,
     "Correlated features carry the same information. This is why simply dropping the column is not a "
     "solution, and why people who propose it are usually surprised."),
   O("Historical labels can encode past human bias", True,
     "The model learns the distribution of its training labels, including whatever produced them. If "
     "past decisions were biased, it reproduces the bias while looking objective."),
   O("This is unavoidable if the data is imbalanced", False,
     "Imbalance is a reason to check, not an excuse. Threshold adjustment, reweighting and "
     "constrained training all exist."),
   O("The model is fine because overall accuracy is equal", False,
     "Equal aggregate accuracy with unequal error rates means the harms fall unevenly, which is "
     "exactly the failure being measured.")],
  "c2/w3-15-fairness-bias-ethics.html", tag="fairness",
  note="Split every metric by group. It is one line of code and it is the whole defence."),
])
