# -*- coding: utf-8 -*-
"""Active Mastery for 12_fine_tuning.py. Values read off the running file.

The anchor: LoRA's task A accuracy WITHOUT the adapter is 0.8870 -- the
untouched original, exactly. That detachability is the property the
parameter count does not show, and it is the whole reason one base model
can serve many customers.
"""
from masterykit import (section, prose, code, out, semantics, ledger, drill, peek,
                        predict, lab, breaks, invariant, wrong, reconstruct,
                        connections, recall, check)

AM = dict(
    lede="Eleven cards on the file that measures what fine-tuning <b>destroys</b>, not just "
         "what it gains &mdash; which is the column papers do not print.",
    sections=[

section("0", "&#129517;", "Before you run", "before", kind="orient",
    hook="20,000 examples of one task, 60 of another. That ratio is the realistic part.",
    body=prose("""<p>Somebody else trained a model on <b>20,000</b> examples. You have
<b>60</b> for a related task. That is the shape of most modern machine learning, and this file
measures three ways of bridging the gap.</p>
<p><b>Watch the second column of every table.</b> Task B accuracy is what papers report; task
A accuracy <b>afterwards</b> is what it cost. Full fine-tuning wins on B at <b>0.7628</b> and
drops A from <b>0.8870</b> to <b>0.7025</b> &mdash; eighteen points, with a name:
catastrophic forgetting.</p>""")
    + connections([], [], "../gist/c22.html", "C2 Week 2 &mdash; the gist",
        extra=[("lab", "../scratch/04-backpropagation.html", "File 04 first",
                "this is that training loop, run on somebody else's weights")])),

section("1", "&#127991;&#65039;", "What every variable is", "vars", kind="semantics",
    hook="Nine variables, and none of them is physical. The honest table says so.",
    body=semantics([
        ("BASIS", "(6, 20) float64", "the shared latent structure",
         "<b>Six hidden directions in a 20-dimensional space</b> that <i>both</i> tasks are "
         "built from. This is what makes them &ldquo;related&rdquo; &mdash; made precise.",
         "<i>none &mdash; abstract</i>",
         "It has no physical meaning and inventing one would mislead. What matters is that "
         "<b>both tasks read the same six directions</b>.",
         "If the two tasks shared no basis, the pretrained weights would be worth nothing and "
         "training from scratch would do just as well. The relatedness sweep tests exactly "
         "that."),
        ("MIX_A / MIX_B", "(6, 4) float64", "how each task weights those directions",
         "<b>The only difference between the two tasks.</b> "
         "<code>MIX_B = MIX_A + 0.9 &times; noise</code> &mdash; related, not identical.",
         "<i>none</i>",
         "The <b>0.9</b> is the relatedness dial. Set it to 0 and the tasks are the same; "
         "raise it and they drift apart.",
         "This is the one knob that decides whether transfer helps at all, and the file sweeps "
         "it explicitly rather than assuming."),
        ("XA / XB", "(20000, 20) and (60, 20)", "the two datasets",
         "<b>One row = one example</b>, 20 abstract features. Task A is the big pretraining "
         "set; task B is your realistic 60.",
         "<i>none &mdash; abstract</i>",
         "<b>20,000 against 60</b> &mdash; a ratio of 333 to 1. That asymmetry is the entire "
         "situation being modelled.",
         "The <code>n_B</code> sweep at the end varies it from 20 to 5,000, and the "
         "conclusions change completely."),
        ("BASE", "dict of 6 arrays", "the pretrained model",
         "<b>W1 (20,64), b1 (64,), W2 (64,64), b2 (64,), W3 (64,4), b3 (4,)</b> &mdash; a "
         "three-layer network. The expensive thing you are trying not to repeat.",
         "<i>unitless</i>",
         "<code>n_params(BASE)</code> is <b>5,764</b>. Tiny &mdash; but the <b>ratios</b> "
         "between the methods hold at any scale.",
         "The last layer, <b>W3 (64,4)</b>, is only <b>260</b> parameters with b3. That is "
         "what &ldquo;train the head only&rdquo; means."),
        ("ACC_A", "float", "the number to protect",
         "<b>The pretrained model's accuracy on the task it was actually trained for.</b>",
         "<b>accuracy, 0&ndash;1</b>",
         "<b>0.8870</b>. Every method below is measured against how much of this it destroys.",
         "This is the column that fine-tuning papers omit. A method that gains 2 points on B "
         "and loses 18 on A has not obviously improved anything."),
        ("delta", "dict or None", "the LoRA adapter",
         "<b>A small correction applied alongside the frozen weights</b>, never merged into "
         "them.",
         "<i>unitless</i>",
         "At rank 4 it is <b>512</b> parameters &mdash; 8.9% of the model. Pass "
         "<code>delta=None</code> and you get the original network back <b>exactly</b>.",
         "That <code>None</code> is the whole point: the base weights were never modified, so "
         "the adapter can be <b>detached</b>. Full fine-tuning has no such option."),
        ("train", "tuple of str", "which parameters get gradients",
         "<b>The freeze switch.</b> <code>grads</code> and <code>sgd</code> take a tuple of "
         "names, and only those receive updates.",
         "<i>names</i>",
         "<code>train=(&quot;W3&quot;, &quot;b3&quot;)</code> is head-only. The default is all "
         "six.",
         "&ldquo;Freezing&rdquo; is not a special mode &mdash; it is <b>omitting names from a "
         "tuple</b>. Worth knowing, because it means you can freeze any subset, not just a "
         "prefix."),
        ("r", "int", "the LoRA rank",
         "How wide the adapter is. <b>A capacity choice</b>, not a property of the task.",
         "<i>unitless</i>",
         "r = 4 gives 512 parameters and 0.7435 on B. r = 16 gives 2,048 and <b>0.7532</b> "
         "&mdash; four times the parameters for 0.01 accuracy.",
         "The sweep is <b>not monotonic</b>: r = 8 scores 0.7368, <i>worse</i> than r = 4. "
         "With 60 examples the differences are mostly noise."),
        ("drift", "float", "how far task B moves from task A",
         "<b>A property of the experiment, not of any model.</b> The sweep parameter for "
         "relatedness.",
         "<i>unitless</i>",
         "At drift 0.0 the untouched base scores <b>0.8905</b> on task B; at drift 1.5 it "
         "scores <b>0.5605</b> &mdash; barely better than chance.",
         "Yet full fine-tuning stays around <b>0.81</b> the whole way. That gap is the "
         "evidence that pretraining contributes <i>two</i> different things."),
    ],
    """Nothing in this file is physical, and the table says so rather than inventing a story.
What <b>is</b> real is the structure: <code>BASIS</code> is shared, <code>MIX_B</code> differs
by a measurable amount, and every claim about transfer is checked against that dial."""),
    ),

section("2", "&#128302;", "Prediction checkpoints", "predict", kind="predict",
    hook="Four, and two of them go the way most people do not expect.",
    body=predict([
        ("""Head-only fine-tuning trains 260 of 5,764 parameters and leaves the body frozen.
<b>Predict task A's accuracy afterwards.</b>""",
         """<p>It <b>falls</b>, from 0.8870 to <b>0.6967</b> &mdash; even though the body never
moved.</p>
<p>Because <b>the head is part of task A's model too</b>. You froze the body and then
retrained the one layer task A also depended on. &ldquo;Freezing&rdquo; protects the weights
you froze, not the model as a whole.</p>
<p>Most people predict A is untouched. It is the cleanest surprise in the file.</p>"""),
        ("""Head-only trains fewer parameters and starts from a good model. <b>Predict whether
it beats training from scratch on the 60 examples.</b>""",
         """<p><b>No &mdash; it loses.</b> Head-only gets <b>0.7060</b>; from scratch gets
<b>0.7400</b>.</p>
<p>With 60 examples the frozen features were not quite right for task B, and only 260
parameters were free to compensate. Freezing is not automatically the safe choice; it is a
capacity restriction, and here it restricted too much.</p>"""),
        ("""LoRA at rank 4 reaches 0.7435 on task B. <b>Predict task A's accuracy with the
adapter removed.</b>""",
         """<p><b>0.8870 &mdash; exactly the original.</b> Not approximately.</p>
<p>The base weights were never modified, so detaching the adapter restores the pretrained
model bit for bit. That is the property the parameter count does not show, and it is why one
copy of an expensive base model can serve many customers, each with their own small adapter
swapped in per request.</p>
<p>Full fine-tuning cannot do this at any price &mdash; its forgetting is baked into the
weights.</p>"""),
        ("""The file sweeps task B's size from 20 to 5,000. <b>Predict whether fine-tuning's
advantage grows or shrinks.</b>""",
         """<p><b>Shrinks.</b> At n = 60 full fine-tuning beats scratch by <b>0.023</b>
(0.7628 vs 0.7400); at n = 5,000 by <b>0.008</b> (0.8790 vs 0.8708), which is inside the
noise.</p>
<p>That is the honest conclusion of the whole file: <b>fine-tuning is a fix for not having
much data.</b> With plenty of task B data, training from scratch catches up &mdash; and you
avoid the forgetting entirely.</p>
<p>At n = 20 nothing works: 0.6637, 0.6505, 0.6683, 0.6530. Too few examples for any method to
distinguish itself.</p>"""),
    ],
    """The first and third are the ones worth committing to in writing. Both are commonly
predicted wrong.""")),

section("3", "&#128295;", "Modify the copy", "lab", kind="lab",
    hook="Five, ending with the one-word change that reveals the whole point.",
    body=lab([
        ("L1", "Change a value",
         "Set the relatedness noise from 0.9 to <b>0.0</b> &mdash; the two tasks become "
         "identical &mdash; and compare the base model's task B accuracy.",
         "MIX_B = MIX_A + 0.0 * rng.normal(size=(6, N_CLASS))",
         """<p>The untouched base now scores about <b>0.89</b> on task B without any adaptation
at all, because task B <i>is</i> task A.</p>
<p>Which makes the ceiling visible: fine-tuning cannot beat the pretrained model when there is
nothing new to learn. Every gain in the main experiment is the model learning the part of task
B that <b>differs</b> from A.</p>"""),
        ("L2", "Change a parameter",
         "Freeze everything <b>except</b> the first layer &mdash; the opposite of head-only. "
         "Predict the result before running it.",
         'p2 = sgd(BASE, XB, yB, epochs=..., lr=..., bs=..., train=("W1", "b1"))',
         """<p>It does <b>worse</b> than head-only on task B. The first layer learns generic
low-level structure that both tasks share, so changing it damages what was useful while
leaving the task-specific head untouched.</p>
<p>This is the empirical basis for the standard advice: <b>replace the last layer, keep the
early ones</b>. The file lets you check it rather than take it on faith.</p>"""),
        ("L3", "Change the data",
         "Run the whole comparison with <code>n_B = 5000</code> and read the verdict table "
         "again.",
         "XB, yB, XB_te, yB_te = make_task(5000, MIX_B, ...)",
         """<p>The methods <b>converge</b>: scratch 0.8708, full 0.8790, LoRA 0.8620. The gaps
that looked decisive at 60 examples are now inside the noise.</p>
<p>And the strategic consequence: at this data volume, <b>training from scratch is the
sensible choice</b> &mdash; comparable accuracy, no forgetting, no dependency on somebody
else's weights.</p>
<p>&ldquo;Always fine-tune&rdquo; is advice for a data regime, not a law.</p>"""),
        ("L4", "Change an assumption",
         "After LoRA training, <b>merge</b> the adapter into the base weights and then measure "
         "task A.",
         "for k in ('W1','W2','W3'):\n    BASE[k] = BASE[k] + delta[k]      # merged, not detachable",
         """<p>Task A now reads <b>0.6655</b> &mdash; the with-adapter number &mdash; and
<b>you cannot get 0.8870 back</b>. The original weights are gone.</p>
<p>Merging is a real deployment choice: it removes the runtime cost of applying the adapter
separately, at the price of the one property that made LoRA attractive. You have converted it
into a full fine-tune with fewer training steps.</p>
<p>The lesson: <b>detachability is a property of how you deploy it</b>, not of the training
method.</p>"""),
        ("L5", "Explain it",
         "Explain why head-only fine-tuning damages task A when the body never changed.",
         None,
         """<p>Because task A's predictions also flow through <b>W3 and b3</b>. Freezing the
body protects the <b>features</b>, but the head is the part that turns features into task A's
four class scores, and you retrained it on a different labelling.</p>
<p>So &ldquo;freezing&rdquo; only ever protects the parameters you named. To keep task A
working you would need a <b>separate head per task</b> on a shared body &mdash; which is
exactly what multi-task architectures do, and why they exist.</p>"""),
    ],
    """L4 is the one to run. It shows that LoRA's headline advantage can be thrown away by a
deployment decision that looks like an optimisation.""")),

section("4", "&#128165;", "Break it, then repair it", "break", kind="debug",
    hook="Four, and three of them produce a better-looking number than the truth.",
    body=breaks([
        ("acc_B = accuracy(p, XB, yB)        # the TRAINING 60, not XB_te",
         "Measure task B accuracy on the 60 rows it was fine-tuned on, not the held-out ones. "
         "Predict what you would report.",
         """<p>Close to <b>1.00</b> for every method &mdash; the file already notes that
training from scratch reaches <b>1.0000</b> on its own 60 examples while managing 0.7400 on
new ones.</p>
<p>So every method would look excellent and <b>indistinguishable</b>, and the entire
comparison would collapse. Memorising 60 points is easy; generalising from them is not.</p>
<p>The invariant: <b>every number in the verdict table is on held-out data</b>. It is the one
thing that makes the table mean anything.</p>"""),
        ("acc_A_after = accuracy(p_lora, XA_te, yA_te, delta=delta)      # adapter left on",
         "Measure LoRA's task A accuracy <b>with</b> the adapter attached and report it as the "
         "forgetting number.",
         """<p>You get <b>0.6655</b> instead of <b>0.8870</b>, and you would conclude LoRA
forgets about as badly as full fine-tuning.</p>
<p>It does not. With the adapter <b>detached</b> the base is untouched &mdash; the two numbers
answer different questions: &ldquo;how does the adapted model do on A&rdquo; versus &ldquo;did
I damage the base model&rdquo;.</p>
<p>The invariant: <b>report LoRA's task A accuracy without the adapter</b>, because that is
the number that says whether the original still exists.</p>"""),
        ("p = sgd(BASE, XB, yB, ...)        # BASE is mutated in place",
         "Let training modify <code>BASE</code> in place rather than working on a copy. What "
         "breaks, and when?",
         """<p>Nothing breaks <b>during</b> that run. It breaks on the <b>next</b> one: the
&ldquo;pretrained&rdquo; model is now the fine-tuned one, so every subsequent method starts
from the wrong place.</p>
<p>The symptom is that results depend on <b>the order you ran the experiments in</b>, which is
maddening to debug and easy to mistake for randomness.</p>
<p>The invariant: <b>the base model must be immutable across the comparison.</b> Every method
starts from the same weights or none of the numbers are comparable.</p>"""),
        ("delta = {k: np.zeros_like(v) for k, v in BASE.items()}      # rank-full, zero-init",
         "Give the adapter the <b>full</b> shape of each weight matrix instead of a low-rank "
         "factorisation. Is it still LoRA?",
         """<p>It trains, and it is <b>not LoRA</b> &mdash; it is a full fine-tune wearing an
adapter's name. The parameter count goes from 512 to 5,764, and you have lost the only reason
to use the technique.</p>
<p>The <b>low rank</b> is the whole idea: r = 4 means the update is constrained to a 4-dimensional
subspace, which is both cheap and a regulariser. The file's rank sweep shows that r = 16 buys
almost nothing over r = 4 with 60 examples.</p>
<p>The invariant: <b>an adapter must be much smaller than what it adapts</b>, or it is not
buying anything.</p>"""),
    ],
    """Three of these four make your results look <b>better</b>, which is the dangerous
direction. A bug that flatters you is one nobody hunts for.""")),

section("5", "&#9878;&#65039;", "The invariant", "invariant", kind="invariant",
    hook="Detach the adapter and the original must return, exactly.",
    body=invariant("""<p><b>With the adapter detached, the model must reproduce the pretrained
accuracy exactly &mdash; and every reported number must come from held-out data.</b></p>""",
    """<p>The file checks the first by printing task A accuracy twice: <b>0.6655</b> with the
adapter and <b>0.8870</b> without. That second number is <b>bit-identical</b> to the
pretrained model's, because the base weights were never written to.</p>
<p>It is the strongest possible statement of what LoRA buys, and it is a property no parameter
count can express. Full fine-tuning trains the same 5,764 weights and has no equivalent
check, because there is nothing left to compare against.</p>
<p>The second invariant is duller and protects everything: the file's verdict table is
comparable <b>only</b> because every cell is held-out. Training from scratch scores
<b>1.0000</b> on its own 60 examples and <b>0.7400</b> on new ones.</p>""",
    """assert accuracy(BASE, XA_te, yA_te) == ACC_A          # base never mutated
assert accuracy(p_lora, XA_te, yA_te, delta=None) == ACC_A
assert n_params(delta) < 0.2 * n_params(BASE)         # it is an ADAPTER
assert acc_reported is measured_on(XB_te)             # never on XB""")),

section("6", "&#129535;", "Wrong mental models", "wrong", kind="myths",
    hook="Five, and the first is the one the whole file is built to correct.",
    body=wrong([
        ("Fine-tuning improves the model.",
         """<p>It produces a <b>different</b> model. Full fine-tuning gains 2 points on task B
(0.7400 &rarr; 0.7628) and loses <b>18</b> on task A (0.8870 &rarr; 0.7025).</p>
<p>Nothing went wrong: you asked gradient descent for the weights that fit 60 examples of task
B, and it gave you exactly that. It was never asked to preserve task A. If you need both, you
need <b>both sets of weights</b> &mdash; which for a large model means storing it twice.</p>"""),
        ("Freezing the body protects the pretrained model.",
         """<p>It protects the <b>body</b>. Head-only fine-tuning still drops task A from
0.8870 to <b>0.6967</b>, because the head is part of task A's model too.</p>
<p>Freezing only ever protects the parameters you named. To keep task A working you need a
<b>separate head</b> on a shared body, which is what multi-task architectures are for.</p>"""),
        ("A bigger LoRA rank is better.",
         """<p>The sweep is <b>not monotonic</b>: r = 4 gives 0.7435 and r = 8 gives
<b>0.7368</b> &mdash; worse with twice the parameters. r = 16 gives 0.7532, a gain of 0.01 for
four times the parameters.</p>
<p>With 60 examples there is not enough data to exploit a bigger adapter, and most of the
variation between rows is noise. Pick a small r and spend your attention elsewhere.</p>"""),
        ("If the tasks are unrelated, pretraining is worthless.",
         """<p>The drift sweep says otherwise. At drift 1.5 the untouched base scores
<b>0.5605</b> &mdash; barely better than chance &mdash; yet full fine-tuning from those same
weights still reaches <b>0.8115</b>, beating from-scratch's 0.7087 by <b>0.10</b>.</p>
<p>So pretraining contributes <b>two</b> things: task-specific knowledge, which drift destroys,
and <b>generally useful structure</b>, which survives. The second is why pretraining is worth
doing even for a distant task.</p>"""),
        ("Fine-tuning is how you add knowledge to a model.",
         """<p>It is how you adapt a model when you have <b>little data</b>. The n_B sweep is
the argument: the advantage over training from scratch shrinks from 0.023 at n = 60 to
<b>0.008</b> at n = 5,000, which is inside the noise.</p>
<p>And for knowledge that changes, retrieval is usually the better tool &mdash; file 11 adds
information without touching a single weight, and you can update it by editing a
document.</p>"""),
    ])),

section("7", "&#127959;&#65039;", "Reconstruction challenge", "reconstruct", kind="rebuild",
    hook="Rebuild the comparison, and make the base model immutable.",
    body=reconstruct([
        ("Explain", "In four sentences, describe the three methods and what each costs.",
         """<p>Train only the final layer, leaving the rest frozen &mdash; cheapest, least
capacity. Train everything from the pretrained starting point &mdash; best on the new task,
destroys the old one. Or add a small correction alongside the frozen weights and train only
that &mdash; nearly as good, and <b>removable</b>. All three are measured against simply
training from scratch, which is the number that decides whether any of it was worth it.</p>"""),
        ("Skeleton", "Write the signatures, and say which argument does the freezing.",
         """<p><code>init(seed)</code>, <code>forward(p, X, delta=None)</code>,
<code>grads(p, X, y, delta=None, train=(...))</code>,
<code>sgd(p, X, y, epochs, lr, bs, train=None)</code>, <code>n_params(p)</code>,
<code>accuracy(p, X, y, delta=None)</code>.</p>
<p>The freezing is the <b><code>train</code> tuple</b> &mdash; only the named parameters get
gradients. And <code>delta=None</code> is what makes the base recoverable.</p>"""),
        ("Core", "Write the LoRA forward pass from memory.",
         """<p>For each adapted weight: <code>W_effective = W + delta[k]</code>, where
<code>delta[k]</code> is the product of two thin matrices &mdash; <b>(n, r) @ (r, m)</b>
&mdash; so it has the shape of W but only <b>r(n + m)</b> free parameters.</p>
<p>Crucially the base <code>W</code> is <b>read, never written</b>. If your implementation
does <code>W += delta</code> anywhere, you have merged it and lost detachability.</p>"""),
        ("Minimal", "Build the smallest experiment that shows catastrophic forgetting.",
         """<p>Two tasks over the same inputs with different labels, one pretrained model, and
<b>two</b> accuracy measurements: task A before and after training on task B.</p>
<p>Reporting only the second is what hides forgetting, so the minimal experiment is really
about <b>which numbers you print</b>.</p>"""),
        ("Verify", "Check your rebuild without comparing to the original.",
         """<p>Three assertions: the base model's task A accuracy is <b>unchanged</b> after
every experiment (it must be immutable); LoRA with <code>delta=None</code> reproduces that
number exactly; and the adapter has far fewer parameters than the model.</p>
<p>The first one catches in-place mutation, which is the bug that makes results depend on the
order you ran things.</p>"""),
    ],
    """The immutability check is the one to write first. Without it every later number is
quietly contaminated by the experiment before.""")),

section("8", "&#128279;", "Connections", "conn", kind="links",
    hook="04's training loop, on somebody else's weights — and the alternative in 11.",
    body=connections(
        [("lab", "../scratch/04-backpropagation.html", "Back to 04",
          "the same training loop, started from pretrained weights instead of random ones"),
         ("lab", "../scratch/05-softmax.html", "Back to 05",
          "the 4-class head this file adapts")],
        [("lab", "../scratch/11-retrieval.html", "Alongside 11",
          "the other way to give a model knowledge &mdash; without touching a weight"),
         ("lab", "../scratch/14-mlops.html", "On to 14",
          "and how you would notice, in production, that the old task had degraded")],
        "../gist/c22.html", "C2 Week 2 &mdash; the gist",
        extra=[("docs", "../reference.html", "Reference &mdash; C2 W3",
                "<code>c2w3-transfer</code> covers freeze-vs-fine-tune and when each applies")])),

section("9", "&#9670;", "Recall sheet", "recall", kind="recall",
    hook="Six cards, all from the file's own tables.",
    body=recall([
        ("LoRA r=4: task A accuracy <b>with</b> and <b>without</b> the adapter?",
         "<b>0.6655</b> with, <b>0.8870</b> without &mdash; and 0.8870 is <b>exactly</b> the "
         "pretrained number. The base weights were never written to, so the adapter is "
         "detachable. That is the property the parameter count does not show."),
        ("Head-only freezes the body. What happens to task A, and why?",
         "It falls <b>0.8870 &rarr; 0.6967</b>. The <b>head is part of task A's model too</b> "
         "&mdash; you froze the body and retrained the layer task A also depended on."),
        ("Does head-only beat training from scratch on 60 examples?",
         "<b>No</b> &mdash; 0.7060 against <b>0.7400</b>. The frozen features were not quite "
         "right and only 260 parameters were free to compensate. Freezing is a capacity "
         "restriction, not a safe default."),
        ("Full fine-tuning's gain on task B, and its cost on task A?",
         "Gains <b>0.023</b> on B (0.7400 &rarr; 0.7628) and loses <b>0.18</b> on A (0.8870 "
         "&rarr; 0.7025). That drop is <b>catastrophic forgetting</b>, and nothing went "
         "wrong."),
        ("Is a bigger LoRA rank better? Give the numbers.",
         "Not reliably. r=4 &rarr; <b>0.7435</b>; r=8 &rarr; <b>0.7368</b> (worse, twice the "
         "parameters); r=16 &rarr; 0.7532. With 60 examples most of the variation is noise."),
        ("At n_B = 5,000, how does fine-tuning compare with training from scratch?",
         "<b>0.8790 against 0.8708</b> &mdash; a gap of 0.008, inside the noise. Fine-tuning "
         "is a fix for <b>not having much data</b>; with plenty, scratch catches up and avoids "
         "the forgetting."),
    ],
    """Cover and answer aloud.""")),

section("10", "&#9989;", "Mastery check", "check", kind="check",
    hook="Five, all about the column nobody prints.",
    body=check([
        ("""A paper reports that fine-tuning improved their model from 0.74 to 0.76. What is
the first thing you ask for?""",
         """<p><b>The accuracy on the original task afterwards.</b> This file's equivalent
numbers are 0.7400 &rarr; 0.7628 on task B, and <b>0.8870 &rarr; 0.7025</b> on task A.</p>
<p>A two-point gain that costs eighteen points elsewhere is a trade, not an improvement, and
the second number is routinely omitted.</p>"""),
        ("""Explain why head-only fine-tuning damaged the original task when the body was
frozen.""",
         """<p>Because the <b>head is part of the original task's model</b>. Freezing protects
the parameters you named &mdash; the features &mdash; but the head is what turns those
features into the original task's class scores, and you retrained it on different labels.</p>
<p>Keeping both working needs a <b>separate head per task</b> on a shared body.</p>"""),
        ("""Your colleague merges a LoRA adapter into the base weights to save inference cost.
What did they give up?""",
         """<p><b>Detachability</b> &mdash; and with it the ability to recover the original
model, which was 0.8870 on the old task. After merging, task A reads <b>0.6655</b> and there
is nothing to detach.</p>
<p>They have converted LoRA into a full fine-tune with fewer training steps, and lost the
ability to serve many customers from one base copy.</p>"""),
        ("""You have 5,000 examples for your new task. Argue against fine-tuning.""",
         """<p>At that volume the advantage is <b>0.008</b> (0.8790 against 0.8708) &mdash;
inside the noise. Training from scratch gives comparable accuracy, no catastrophic forgetting,
and <b>no dependency on somebody else's weights</b> or licence.</p>
<p>&ldquo;Always fine-tune&rdquo; is advice for the small-data regime, and this file measures
where that regime ends.</p>"""),
        ("""Your experiment results change depending on which order you ran the methods in.
Name the bug.""",
         """<p>The base model is being <b>mutated in place</b>. Each method starts from
whatever the previous one left behind, so the &ldquo;pretrained&rdquo; weights are not
pretrained by the second experiment.</p>
<p>It reads like randomness and is not. The fix is one assertion: the base model's original-task
accuracy must be <b>unchanged</b> after every run.</p>"""),
    ],
    """These four files have no mock quiz, so the thing not to repeat is the walkthrough
above &mdash; which explains what each block does, where this asks what you would report and
what you would refuse to.""")),
    ],
)
