# -*- coding: utf-8 -*-
"""The gist of F0 Week 3 — the maths behind the curtain."""
from kit import key, trap
from gistkit import gistline, flow, carried, retell, ladder, h2
from walkkit import cases, values, point, expr, chainset

GIST = dict(
    course="F0", week="3", title="The Maths Behind the Curtain", mins=9,
    lede="Five lessons that answer questions the courses raise and never return to. None of "
         "it is required. All of it turns a recipe into an explanation.",
    body="".join([
        gistline("""The specialization tells you <i>what</i> to do and, sensibly, skips
<i>why it is that and not something else</i>. This week answers five of those questions —
where loss functions come from, why PCA uses eigenvectors, and why the tidiest gradient in
deep learning is tidy."""),

        h2("🖼", "The week in one picture"),
        flow([
            ("note", "This week is not a pipeline",
             "The other sixteen weeks build one thing. These five lessons each answer a "
             "different unanswered question, so the picture is a map rather than a flow."),
            ("op", "Eigenvectors — the directions a matrix leaves alone",
             "<b>Av = λv</b>. Along these directions only, a whole matrix collapses to one "
             "number."),
            ("arw", "apply that to the covariance matrix"),
            ("op", "Why PCA works",
             "Each eigenvalue <b>is</b> the variance along its own eigenvector. So "
             "&ldquo;most spread out&rdquo; and &ldquo;largest eigenvector&rdquo; are the "
             "same instruction."),
            ("arw", "and generalise it to matrices that are not square"),
            ("op", "SVD — rotate, stretch, rotate",
             "Works on <b>any</b> matrix, and truncating it gives the provably best "
             "low-rank approximation."),
            ("note", "The other two answer a different question entirely", ""),
            ("op", "Maximum likelihood — where the losses came from",
             "Assume Gaussian noise, <b>derive</b> squared error. Assume a yes/no outcome, "
             "<b>derive</b> cross-entropy."),
            ("arw", "and then, how those losses are differentiated at scale"),
            ("op", "The Jacobian, and why softmax cancels",
             "The chain rule becomes matrix multiplication; and the softmax and "
             "cross-entropy derivatives annihilate, leaving <b>p − y</b>."),
        ], cap="""Two threads, not one. Lessons 1–2 are the linear algebra PCA leans on;
lessons 3–5 are where loss functions and their gradients come from."""),

        h2("❓", "The five questions this week answers"),
        carried("""Each of these is raised somewhere in the specialization and then left. If
none of them has bothered you, this week is genuinely optional.""",
                [("Why do the principal components come out as eigenvectors?", "01–02",
                  "because an eigenvalue <b>is</b> the variance along its eigenvector"),
                 ("Why does real PCA use SVD instead?", "02",
                  "because building the covariance matrix squares the numbers and loses "
                  "precision — and SVD works on non-square data"),
                 ("Why squared error for regression and log loss for classification?", "03",
                  "both are <b>derived</b> from maximum likelihood, under different "
                  "assumptions about the noise"),
                 ("What is a gradient when the output is a vector?", "04",
                  "a Jacobian — and the gradient you already use is one with a single row"),
                 ("Why is the softmax gradient just <b>p − y</b>?", "05",
                  "the softmax derivative carries p and the log contributes 1/p; they "
                  "cancel exactly")],
                head=("The question", "Lesson", "The short answer")),

        h2("🔑", "The one idea that carries the most weight"),
        key("""<p><b>Loss functions are not invented. They are derived.</b></p>
<p>Maximum likelihood says: choose the parameters that make the data you actually saw as
probable as possible. Assume the noise is Gaussian and squared error <b>falls out</b>.
Assume a yes/no outcome and cross-entropy <b>falls out</b>.</p>
<p>That reframes a whole course. The cost function stops being an arbitrary choice somebody
made and becomes <b>a consequence of what you assumed about your data</b>. And when a
standard loss does not suit your problem, you now know where to go looking for one that
does.</p>"""),

        h2("🔁", "The cancellation, in both places you meet it"),
        chainset([(["sigmoid + log loss", "gradient = f − y"], "Course 1 Week 3"),
                  (["softmax + cross-entropy", "gradient = p − y"], "Course 2 Week 2")],
                 "the same cancellation, twice"),
        key("""<p>Both pairs are <b>matched</b>. The squashing function's derivative carries
a factor that the logarithm's derivative exactly cancels, and what is left is the plain
error.</p>
<p>Which is why you never see sigmoid paired with squared error, or softmax paired with
anything but cross-entropy: pair either half with something else and the tidiness — and the
well-behaved gradient that comes with it — disappears.</p>"""),

        h2("🚧", "What to do with this week"),
        trap("""<p><b>It is genuinely optional.</b> You can complete the specialization,
pass every quiz and build working models without any of it.</p>
<p><b>Read it when a question nags.</b> The five above are the ones that nag. If you have
been through PCA and thought &ldquo;but why eigenvectors&rdquo;, lesson 2 is a twenty-minute
answer.</p>
<p><b>Do not read it first.</b> These are answers, and an answer to a question you have not
asked yet is just more notation to carry.</p>"""),

        h2("🗣", "Say the week back"),
        retell([
            "What makes a direction an <b>eigenvector</b> of a matrix.",
            "Why an eigenvalue of a covariance matrix is a <b>variance</b>.",
            "The three things SVD does to a space, in order.",
            "Two reasons SVD is preferred over eigendecomposition for PCA.",
            "The maximum likelihood principle, in one sentence.",
            "Which noise assumption gives you squared error, and which gives cross-entropy.",
            "What the rows and columns of a <b>Jacobian</b> are.",
            "Why the gradient you already use is a Jacobian with one row.",
            "Why <b>∂L/∂z = p − y</b> for softmax with cross-entropy.",
            "Why backprop multiplies right to left rather than left to right.",
        ]),

        h2("🪜", "Where this week sits in the whole arc"),
        ladder("F0", """This week does not unlock anything later — nothing in C1, C2 or C3
depends on it. What it changes is your relationship to the rest: after it, the loss
functions and the gradients stop being things you accept and start being things you can
<b>reconstruct</b>. That is the difference between following a recipe and knowing why the
recipe is that."""),
    ]),
)
