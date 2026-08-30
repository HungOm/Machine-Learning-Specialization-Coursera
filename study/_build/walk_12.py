# -*- coding: utf-8 -*-
"""Walkthrough for 12_fine_tuning.py."""
from walkkit import p, expr, chain, chainset, steps, cases, values, point, ascii_art

PICTURE = ([
    ("in", "A model that already knows a lot",
     "Pretrained on <b>20,000</b> examples of task A. Scores 0.8870 on it."),
    ("arw", "and now a new task, with only 60 examples"),
    ("op", "Three ways to adapt it",
     "Train the <b>head</b> only, train <b>everything</b>, or bolt on a small "
     "<b>adapter</b> and train that."),
    ("arw", "each one costs something different"),
    ("op", "Measure BOTH tasks",
     "Not just the new one. What the model <b>forgot</b> is the number nobody reports."),
    ("arw", "and compare against the honest baseline"),
    ("out", "A verdict table",
     "How many parameters moved, what you gained on B, and what you lost on A."),
], "The whole program in one picture",
   "The point of this file is the second column of that final table. Fine-tuning papers "
   "report task B; the cost is always paid on task A.")

WALK = {

"prelude": (
    p("""This is the practical shape of most modern machine learning: somebody else trained
a large model, and you have a small amount of data for a related task.""")
    + point("""The file measures <b>three</b> ways of adapting it, and &mdash; crucially
&mdash; measures what each one <b>destroys</b> as well as what it gains.""")
),

"tasks": (
    p("""Two tasks, deliberately <b>related</b>.""")
    + values([("task A (pretrain)", "20,000 train", "the big one somebody else paid for"),
              ("task B (downstream)", "<b>60</b> train", "yours. This is the realistic part")],
             "the setup")
    + point("""Both label rules read the <b>same 6 latent directions</b>, weighted
differently. That is what &ldquo;a related task&rdquo; means, made precise &mdash; and it is
the whole reason transfer can work at all.""")
    + p("""If the two tasks shared no structure, the pretrained weights would be worth
nothing and starting from scratch would be just as good. The <b>relatedness sweep</b> later
in this file tests exactly that.""")
),

"model": (
    p("""A small network, so every experiment runs in seconds.""")
    + values([("W1 (20, 64)", "1,280", ""),
              ("b1 (64,)", "64", ""),
              ("W2 (64, 64)", "4,096", ""),
              ("b2 (64,)", "64", ""),
              ("total", "<b>5,764</b>", "")],
             "parameters")
    + point("""5,764 parameters is tiny, and the <b>proportions</b> are what matter. A real
model has billions arranged the same way, and the ratios between the three methods below
hold up at that scale.""")
),

"pretrain": (
    p("""Train on task A's 20,000 examples. This is the expensive step you are trying to
avoid repeating.""")
    + chain(["20,000 examples", "0.8870 on task A"], "the model you are starting from")
    + p("""Note the loss wobbles &mdash; 0.2382, 0.2026, 0.2176, then <b>0.7154</b>. That is
mini-batch noise, not divergence: each epoch sees different batches, and small batches give
noisy estimates. Only the trend matters.""")
),

"baseline": (
    p("""The honest comparison: <b>ignore the pretrained model entirely</b> and train from
scratch on the 60 examples.""")
    + values([("test accuracy", "0.7400", "on unseen task B data"),
              ("train accuracy", "<b>1.0000</b>", "on those same 60 examples")],
             "trained from scratch on 60 examples")
    + point("""<b>Memorising 60 points is easy. Generalising from them is not.</b> Perfect
training accuracy and 0.74 on new data is textbook overfitting, and with 60 examples and
5,764 parameters it is unavoidable.""")
    + p("""0.7400 is the number every other method has to beat. Without it, &ldquo;fine-tuning
got 0.76&rdquo; means nothing at all.""")
),

"head_only": (
    p("""Method one: <b>freeze the body</b>, train only the final layer.""")
    + values([("trained", "260 of 5,764", "<b>4.5%</b>"),
              ("task B", "0.7060", "<b>worse</b> than from scratch (0.7400)"),
              ("task A", "0.6967", "was 0.8870")],
             "head-only fine-tuning")
    + point("""It <b>lost</b> to training from scratch. With 60 examples the frozen features
were not quite right for task B, and only 260 parameters were free to compensate.""")
    + p("""And now the genuinely surprising row: <b>task A got worse too</b> &mdash; from
0.8870 down to 0.6967 &mdash; <b>even though the body never moved</b>.""")
    + point("""Why? Because <b>the head is part of task A's model too</b>. You froze the
body and then retrained the one layer task A also depended on. &ldquo;Freezing&rdquo;
protects the weights you froze, not the model as a whole.""")
),

"full": (
    p("""Method two: <b>train everything</b>, starting from the pretrained weights.""")
    + values([("trained", "5,764 of 5,764", "all of them"),
              ("task B", "<b>0.7628</b>", "the best result so far"),
              ("task A", "0.7025", "was 0.8870 &mdash; a drop of <b>0.18</b>")],
             "full fine-tuning")
    + point("""Best on task B, and it destroyed <b>18 accuracy points</b> on task A. That
drop has a name: <b>catastrophic forgetting</b>.""")
    + p("""And nothing went wrong. You asked gradient descent for the weights that fit 60
examples of task B, and it gave you exactly that. It was never asked to preserve task A, so
it did not.""")
    + point("""This is why a fine-tuned model is a <b>different model</b>, not an upgraded
one. If you need both tasks, you need both sets of weights &mdash; which for a large model
means storing the whole thing twice.""")
),

"lora": (
    p("""Method three: leave the base weights <b>untouched</b> and add a small trainable
adapter alongside them.""")
    + values([("trained", "512 of 5,764", "<b>8.9%</b>"),
              ("task B", "0.7435", "beats from-scratch, beats head-only"),
              ("task A with the adapter", "0.6655", ""),
              ("task A <b>without</b> it", "<b>0.8870</b>", "<b>exactly the original</b>")],
             "LoRA, rank 4")
    + point("""That last row is the whole point. <b>0.8870 &mdash; the original number,
unchanged.</b> The base weights were never modified, so removing the adapter restores the
original model <b>exactly</b>. Not approximately.""")
    + p("""<b>You can detach it.</b> That is the property the parameter count does not show,
and it is the reason one base model can serve many customers at once: one copy of the
expensive weights, plus a small adapter per customer, swapped in per request.""")
    + point("""Full fine-tuning cannot do this at any price. Its forgetting is baked into
the weights.""")
),

"rank": (
    p("""LoRA's rank <b>r</b> controls how big the adapter is. Sweep it.""")
    + values([("r = 1", "128 params", "task B 0.7183"),
              ("r = 2", "256 params", "task B 0.7370"),
              ("r = 4", "512 params", "task B 0.7435"),
              ("r = 8", "1,024 params", "task B 0.7368"),
              ("r = 16", "2,048 params", "task B 0.7532")],
             "rank against accuracy")
    + point("""The curve is <b>flat and noisy</b>. Sixteen times the parameters buys about
<b>0.035</b> accuracy, and it is not even monotonic &mdash; r = 8 scores worse than r = 4.""")
    + p("""So the honest reading: with 60 examples, <b>rank barely matters</b>. There is not
enough data to exploit a bigger adapter, and the variation between rows is mostly noise. Pick
a small r and spend your attention elsewhere.""")
),

"verdict": (
    p("""Everything in one table &mdash; and read the <b>last</b> column, which papers rarely
print.""")
    + values([("from scratch", "5,764 trained", "B <b>0.7400</b> &middot; A after 0.6358"),
              ("head only", "260 trained", "B 0.7060 &middot; A after 0.6967"),
              ("full fine-tune", "5,764 trained", "B <b>0.7628</b> &middot; A after 0.7025"),
              ("LoRA r=4", "512 trained", "B 0.7435 &middot; A after 0.6655"),
              ("base, untouched", "0 trained", "B 0.6500 &middot; A <b>0.8870</b>")],
             "trained parameters, task B accuracy, task A afterwards")
    + point("""The bottom row is the reference point. The untouched base model already scores
<b>0.65</b> on a task it was never trained for &mdash; that is transfer happening for free,
before you do anything.""")
    + p("""Full fine-tuning wins on B by about <b>2 points</b> over LoRA, and trains
<b>11&times;</b> as many parameters to get them. Whether that is worth it depends entirely on
whether you still need task A.""")
),

"relatedness": (
    p("""Transfer works because the tasks are related. So how related do they have to be?
This sweeps a <b>drift</b> parameter that pulls task B away from task A.""")
    + values([("drift 0.0", "base 0.8905", "scratch 0.7250 &middot; full 0.8417 &middot; LoRA 0.8150"),
              ("drift 0.3", "base 0.8095", "scratch 0.7228 &middot; full 0.8360"),
              ("drift 0.6", "base 0.7218", "scratch 0.7205 &middot; full 0.7920"),
              ("drift 0.9", "base 0.6525", "scratch 0.7103 &middot; full 0.8023"),
              ("drift 1.5", "base <b>0.5605</b>", "scratch 0.7087 &middot; full <b>0.8115</b>")],
             "as task B drifts away from task A")
    + point("""Watch the <b>base as-is</b> column collapse: 0.89 &rarr; 0.56, until it is
barely better than a coin flip. That is transfer failing, exactly as you would expect.""")
    + p("""But look at <b>full fine-tune</b>: it stays around <b>0.80&ndash;0.84 the whole
way</b>, and at drift 1.5 it beats from-scratch by <b>0.10</b>. Even when the tasks have
almost nothing in common, starting from pretrained weights <b>still helps</b>.""")
    + point("""So the pretrained model contributes two different things: <b>task-specific
knowledge</b>, which drift destroys, and <b>generally useful structure</b>, which survives.
The second is why pretraining is worth doing even for a distant task.""")
),

"data_size": (
    p("""The last question, and the one that decides which method you should use: <b>how much
task B data do you have?</b>""")
    + values([("n = 20", "scratch 0.6637", "full 0.6683 &middot; LoRA 0.6530 &mdash; all equally bad"),
              ("n = 60", "scratch 0.7400", "full <b>0.7628</b> &middot; LoRA 0.7435"),
              ("n = 200", "scratch 0.8195", "full 0.8247 &middot; LoRA 0.7815"),
              ("n = 1000", "scratch 0.8452", "full 0.8655 &middot; LoRA <b>0.8690</b>"),
              ("n = 5000", "scratch <b>0.8708</b>", "full 0.8790 &middot; LoRA 0.8620")],
             "accuracy against how much task B data you have")
    + point("""The gap <b>closes</b>. At n = 60 fine-tuning beats scratch by 0.023; at
n = 5000 it beats it by <b>0.008</b>, which is inside the noise.""")
    + p("""That is the honest conclusion of the whole file: <b>fine-tuning is a fix for not
having much data.</b> With plenty of task B data, training from scratch catches up &mdash;
and you avoid the forgetting entirely.""")
    + point("""It also explains why n = 20 shows nothing. Twenty examples is too few for
<b>any</b> method to learn from; the differences between clever adaptation strategies only
appear once there is something to adapt <b>to</b>.""")
),
}
