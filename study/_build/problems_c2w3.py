# -*- coding: utf-8 -*-
"""C2 W3 — diagnosing models: bias, variance, learning curves, skewed data."""
from problemkit import P, m, pre, cols

L = []
def add(*a, **k): L.append(P(*a, **k))

add("c2w3-p01", level=2, tag="bias vs variance",
    lesson="c2/w3-04-bias-and-variance.html",
    ask="Diagnose each model. Human-level performance on this task is about 10% error."
        + cols(["model", "J<sub>train</sub>", "J<sub>cv</sub>"],
               [["A", "11%", "12%"], ["B", "0.5%", "13%"], ["C", "18%", "19%"],
                ["D", "12%", "31%"]]),
    hint="Two comparisons, always in this order: J_train against the baseline (bias), then "
         "J_cv against J_train (variance).",
    steps=[("A: train 11% ≈ baseline 10%, and cv is close to train", "just right"),
           ("B: train 0.5% is far below baseline, cv is 13% — a 12.5 point gap",
            "high variance"),
           ("C: train 18% is well above baseline, and cv is close to it", "high bias"),
           ("D: train 12% is above baseline AND cv is 19 points higher",
            "high bias and high variance together")],
    answer="A = good · B = high variance · C = high bias · D = <b>both</b>",
    why="D is the case people forget exists. A model can underfit the patterns it does model "
        "while overfitting noise elsewhere — common with a badly chosen architecture.")

add("c2w3-p02", level=2, tag="what to try next",
    lesson="c2/w3-08-what-to-try-revisited.html",
    ask="Sort these six fixes into “helps high bias” and “helps high variance”:<br>"
        "(a) get more training examples (b) add more features (c) add polynomial features "
        "(d) decrease λ (e) increase λ (f) use a smaller set of features",
    steps=[("(a) more data gives the model more to generalise from — it cannot fix a model "
            "too simple to fit what it already has", "variance"),
           ("(b) more features give the model more to work with", "bias"),
           ("(c) polynomial features add flexibility", "bias"),
           ("(d) less regularization means more freedom", "bias"),
           ("(e) more regularization means more constraint", "variance"),
           ("(f) fewer features means less to overfit with", "variance")],
    answer="<b>High bias:</b> (b) more features, (c) polynomial features, (d) decrease λ.<br>"
           "<b>High variance:</b> (a) more data, (e) increase λ, (f) fewer features.",
    why="Note (a) is on the variance side only. Collecting more data is the most expensive "
        "thing on the list and it does nothing at all for a high-bias model — which is "
        "exactly why diagnosing first is worth the effort.")

add("c2w3-p03", level=3, tag="learning curves",
    lesson="c2/w3-07-learning-curves.html",
    ask="You plot %s and %s against training-set size and see them flatten out and "
        "<b>converge to nearly the same high value</b>. Will collecting ten times more data "
        "help? Explain using the shape of the curves."
        % (m("J<sub>train</sub>"), m("J<sub>cv</sub>")),
    hint="Ask what each curve is heading towards as m grows, and whether more m moves that "
         "destination.",
    steps=[("J_train rises with m — more examples are harder to fit perfectly",
            "it flattens at the model's best achievable error"),
           ("J_cv falls with m and approaches J_train from above", "the gap is the variance"),
           ("Here they have already met, and both are high", "the gap is gone; bias remains"),
           ("More data reduces the gap — but there is no gap left to reduce",
            "the curves are already flat")],
    answer="No. The two curves have already converged, so the variance is gone and only bias "
           "remains. More data just extends a flat line to the right. You need a "
           "<b>bigger model or better features</b>.",
    why="This is the single most valuable plot in the specialization: it can save you months "
        "of data collection that would provably have changed nothing.")

add("c2w3-p04", level=2, tag="data splits",
    lesson="c2/w3-03-model-selection.html",
    ask="Why is a two-way train/test split not enough once you start choosing between models? "
        "Describe what goes wrong and what the three-way split fixes.",
    steps=[("You train 10 polynomial degrees and pick the one with the lowest test error",
            "the test set chose the model"),
           ("That choice used the test set, so its error is now optimistic",
            "it is no longer an unseen estimate"),
           ("With 10 candidates, the winner is partly just lucky on that particular test set",
            "you have fitted the test set with one parameter — the degree"),
           ("Three-way split: train fits w and b, cross-validation picks the model, test is "
            "touched once at the very end", "an honest final number")],
    answer="Choosing a model by test error means the test set has been used for fitting — of "
           "one parameter, the choice itself. Its error is then optimistic. The "
           "<b>cross-validation set</b> does the choosing so the test set stays untouched "
           "and honest.",
    why="Typical split: 60/20/20. The discipline that matters is that the test set is looked "
        "at once, at the end, and never again.")

add("c2w3-p05", level=3, tag="precision and recall",
    lesson="c2/w2-06-multiclass.html" if False else "c2/w3-16-skewed-datasets.html",
    ask="A rare-disease classifier gives this confusion matrix on 1000 patients:"
        + cols(["", "predicted 1", "predicted 0"],
               [["actual 1", 8, 12], ["actual 0", 22, 958]])
        + "Compute accuracy, precision, recall and F1. Then explain why accuracy is "
          "misleading here.",
    hint="Precision: of those you flagged, how many really had it. Recall: of those who "
         "really had it, how many you caught.",
    steps=[("Accuracy = (8 + 958) ÷ 1000", "0.966 — 96.6%"),
           ("Precision = TP ÷ (TP + FP) = 8 ÷ (8 + 22)", "8 ÷ 30 ≈ 0.267"),
           ("Recall = TP ÷ (TP + FN) = 8 ÷ (8 + 12)", "8 ÷ 20 = 0.400"),
           ("F1 = 2PR ÷ (P + R) = 2(0.267)(0.400) ÷ 0.667", "0.2136 ÷ 0.667 ≈ 0.320"),
           ("A model that always predicts 0 would score 980 ÷ 1000",
            "98% accuracy, and catch nobody")],
    answer="Accuracy %s · precision %s · recall %s · F1 %s. Accuracy is "
           "misleading because always predicting “no disease” scores <b>98%%</b> while "
           "helping nobody." % (m("0.966"), m("0.267"), m("0.400"), m("0.320")),
    why="Whenever one class is rare, accuracy measures the base rate rather than the model. "
        "F1 is the single number to quote instead, because it collapses if either precision "
        "or recall collapses.")

add("c2w3-p06", level=2, tag="precision-recall trade-off",
    lesson="c2/w3-17-precision-recall-tradeoff.html",
    ask="Starting from the model in the previous problem, you lower the threshold from 0.5 to "
        "0.3 and the confusion matrix becomes:"
        + cols(["", "predicted 1", "predicted 0"],
               [["actual 1", 16, 4], ["actual 0", 90, 890]])
        + "Recompute precision and recall. Was this a good change?",
    steps=[("Precision = 16 ÷ (16 + 90)", "16 ÷ 106 ≈ 0.151"),
           ("Recall = 16 ÷ (16 + 4)", "16 ÷ 20 = 0.800"),
           ("Compare with before", "precision 0.267 → 0.151 · recall 0.400 → 0.800"),
           ("F1 = 2(0.151)(0.800) ÷ 0.951", "≈ 0.254 — lower than 0.320"),
           ("But F1 assumes the two errors matter equally, and for a disease they do not",
            "a missed case is far worse than a false alarm")],
    answer="Precision %s, recall %s. F1 <i>fell</i> to %s, but you now catch 16 of "
           "20 cases instead of 8. For a serious disease this is a <b>good</b> change — F1 is "
           "the wrong summary when the two errors have very different costs."
           % (m("0.151"), m("0.800"), m("0.254")),
    why="This is the honest limit of F1. It is a good default because it punishes collapse in "
        "either direction, but it silently assumes false positives and false negatives are "
        "equally bad.")

add("c2w3-p07", level=2, tag="baseline",
    lesson="c2/w3-06-baseline-performance.html",
    ask="A speech recogniser has %s and %s. "
        "Diagnose it (a) if human transcribers achieve 10.6%% error, and (b) if human "
        "transcribers achieve 0.5%% error."
        % (m("J<sub>train</sub> = 10.8%"), m("J<sub>cv</sub> = 14.8%")),
    steps=[("(a) baseline 10.6%: train is only 0.2 above it", "bias is fine"),
           ("(a) cv is 4.0 above train", "high variance — get more data or regularize"),
           ("(b) baseline 0.5%: train is 10.3 above it", "high bias — the model is too simple"),
           ("(b) the 4.0 gap is still there", "high variance too — both problems")],
    answer="(a) <b>high variance only</b> — the model matches human ability on the training "
           "data. (b) <b>high bias and high variance</b> — 10.8% is terrible when humans hit "
           "0.5%.",
    why="Identical numbers, opposite diagnoses. Without a baseline, J_train is uninterpretable "
        "— 10.8% error might be excellent or shameful and the number alone cannot say.")

add("c2w3-p08", level=3, tag="regularization and variance",
    lesson="c2/w3-05-regularization-bias-variance.html",
    ask="You sweep λ and record:"
        + cols(["λ", "J<sub>train</sub>", "J<sub>cv</sub>"],
               [["0", 0.02, 0.41], ["0.01", 0.05, 0.22], ["0.1", 0.09, 0.13],
                ["1", 0.19, 0.20], ["10", 0.38, 0.39]])
        + "Which λ do you pick, and describe the shape of each curve as λ grows.",
    steps=[("J_train rises steadily with λ", "more constraint means a worse fit to training data"),
           ("J_cv falls then rises — a U shape", "the sweet spot is the bottom of the U"),
           ("Minimum J_cv is 0.13 at λ = 0.1", "pick that"),
           ("λ = 0: gap of 0.39 — pure overfitting", "high variance"),
           ("λ = 10: both high and equal", "high bias")],
    answer="Pick %s. J<sub>train</sub> climbs monotonically with λ; J<sub>cv</sub> forms a "
           "<b>U</b>, high on the left from variance and high on the right from bias."
           % m("λ = 0.1"),
    why="The U shape is the whole bias–variance trade-off in one picture. λ slides you along "
        "it, and the bottom is the best compromise the current model can reach.")

add("c2w3-p09", level=2, tag="error analysis",
    lesson="c2/w3-11-error-analysis.html",
    ask="Your spam classifier misclassifies 1000 cross-validation emails. You hand-examine "
        "100 of them and tag each with any category that applies &mdash; <b>an email can carry "
        "more than one tag, and 31 fitted none of them</b>:"
        + cols(["category", "count in the 100"],
               [["pharmaceutical spam", 21], ["deliberate misspellings", 18],
                ["phishing", 18], ["unusual email routing", 7], ["image-only spam", 5],
                ["no clear pattern", 31]])
        + "Where should you spend the next month, and what does the sample of 100 tell you "
          "about the other 900?",
    steps=[("Sort by frequency. The tags overlap, so they do not add to 100",
            "pharma 21, misspellings 18, phishing 18, routing 7, image 5"),
           ("Solving image-only spam perfectly removes at most 5% of errors",
            "a ceiling on the payoff"),
           ("Pharma and phishing together are 39% of errors", "the highest ceiling"),
           ("The 100 is a random sample, so the proportions extrapolate — roughly 210 pharma "
            "errors in the full 1000", "but with sampling noise of a few percent"),
           ("Also weigh how hard each is to fix", "a 5% category with an easy fix may still win")],
    answer="Pharmaceutical spam and phishing — together about 39% of errors, so about 390 of "
           "the 1000. Image-only spam caps out at 5%, so even a perfect fix there is nearly "
           "invisible. The sample estimates each category's <b>ceiling on improvement</b>.",
    why="Error analysis is the cheapest step in the whole workflow and routinely redirects "
        "months of effort. An hour of reading actual mistakes beats a week of guessing.")

add("c2w3-p10", level=2, tag="transfer learning",
    lesson="c2/w3-13-transfer-learning.html",
    ask="You have 1000 labelled X-ray images and want a diagnosis model. Explain why "
        "starting from a network trained on a million photos of cats, cars and furniture "
        "helps, and describe both fine-tuning options.",
    steps=[("The early layers of the photo network learned edges, textures and shapes",
            "those are not cat-specific"),
           ("X-rays also contain edges, textures and shapes",
            "the early layers transfer"),
           ("Option 1: freeze all but the output layer, train only the new head",
            "for very small datasets — few parameters to fit"),
           ("Option 2: initialise from the pretrained weights and train everything at a low "
            "learning rate", "for larger datasets — more flexibility, more risk of overfitting"),
           ("Either way you replace the output layer, since the classes are different",
            "1000 photo classes → your diagnosis classes")],
    answer="Early layers learn generic visual features — edges, textures, shapes — which are "
           "the same in X-rays as in photos. <b>Option 1:</b> freeze everything, retrain only "
           "the output layer (best with very little data). <b>Option 2:</b> retrain all layers "
           "starting from the pretrained weights (better with more data).",
    why="With 1000 images, training from scratch would overfit hopelessly. Transfer learning "
        "is what makes small-data deep learning possible at all.")

add("c2w3-p11", level=3, tag="the iterative loop",
    lesson="c2/w3-10-iterative-loop.html",
    ask="Put these in the correct order and say what decision closes the loop back to the "
        "start:<br>(a) train the model (b) choose architecture and features "
        "(c) diagnose bias/variance and do error analysis (d) deploy",
    steps=[("Start by choosing the architecture, features and hyperparameters",
            "(b)"),
           ("Then train it", "(a)"),
           ("Then diagnose — bias/variance plus error analysis", "(c)"),
           ("The diagnosis tells you what to change, so you loop back to (b)",
            "b → a → c → b → a → c …"),
           ("Deploy only when the diagnosis says you have hit your target", "(d)")],
    answer="%s and repeat, only reaching %s when the diagnosis says you are good enough. "
           "The <b>diagnosis</b> is what closes the loop — it decides what to change next."
           % (m("b → a → c"), m("d")),
    why="The loop is the actual method of the whole specialization. Everything else — "
        "gradient descent, regularization, learning curves — is a tool used inside it.")

add("c2w3-p12", level=2, tag="model selection",
    lesson="c2/w3-03-model-selection.html",
    ask="You fit polynomial degrees 1 to 10 and record cross-validation error: "
        "%s. Which degree do you choose, and what error should you report as the model's "
        "expected performance?"
        % m("[0.42, 0.31, 0.19, 0.13, 0.11, 0.12, 0.16, 0.24, 0.38, 0.61]"),
    steps=[("Find the minimum J_cv", "0.11 at degree 5"),
           ("Degrees 1–4 are still falling", "underfitting"),
           ("Degrees 6–10 climb steeply", "overfitting"),
           ("Report the TEST error, not 0.11", "0.11 was used to make the choice")],
    answer="Choose <b>degree 5</b>. Report the error on the untouched <b>test set</b> — 0.11 "
           "is optimistic because that number is exactly what you selected on.",
    why="The U shape appears again, this time indexed by model complexity rather than λ. "
        "Same trade-off, different dial.")

add("c2w3-p13", level=3, tag="skewed data + threshold",
    lesson="c2/w3-16-skewed-datasets.html",
    ask="A fraud detector sees 0.2% fraud. Your model reports 99.8% accuracy. Before "
        "celebrating, what single question do you ask, and what two numbers do you demand "
        "instead?",
    steps=[("0.2% fraud means 99.8% of transactions are legitimate", "the base rate"),
           ("A model that predicts “legitimate” for everything scores exactly 99.8%",
            "the same as yours"),
           ("So the question is: does it beat always saying no?",
            "compare against the base rate, never against 0"),
           ("Demand precision and recall — or the confusion matrix itself",
            "those cannot be faked by a constant prediction")],
    answer="Ask <b>“what does a model that always predicts ‘not fraud’ score?”</b> — the "
           "answer is 99.8%, identical. Demand <b>precision and recall</b> (or the full "
           "confusion matrix), which a constant predictor cannot fake.",
    why="Any accuracy figure on skewed data must be quoted against the base rate. 99.8% "
        "sounds like a triumph and is, here, exactly worthless.")

SET = dict(course="C2", week=3, title="Diagnosing models",
           lede="This is the most practically useful week in the specialization: it turns "
                "“the model is bad” into a specific diagnosis with a specific fix. These "
                "problems are mostly diagnosis, which is a skill you can only build by doing "
                "it repeatedly.",
           problems=L)
