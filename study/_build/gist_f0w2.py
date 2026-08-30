# -*- coding: utf-8 -*-
"""The gist of F0 Week 2 — NumPy and pandas as one pipeline."""
from kit import key, trap
from gistkit import gistline, flow, carried, chain, bynumbers, retell, ladder, h2
from walkkit import cases, values, point, expr

GIST = dict(
    course="F0", week="2", title="Python, NumPy and pandas", mins=10,
    lede="Sixteen lessons that are really one pipeline: a file on disk becomes two arrays "
         "of the right shape, and every step has a way of going quietly wrong.",
    body="".join([
        gistline("""A CSV goes in and two NumPy arrays come out: <b>X</b> with one row per
example, and <b>y</b> with one number per example. Everything in this week is either a step
on that path or a way of checking you are still on it."""),

        h2("🖼", "The week in one picture"),
        flow([
            ("in", "A file on disk", "Rows, columns, headings, and probably a stray "
                                     "&ldquo;N/A&rdquo; somewhere."),
            ("arw", "read it, then LOOK at it"),
            ("op", "pandas DataFrame",
             "<code>head()</code>, <code>shape</code>, <code>info()</code>, "
             "<code>describe()</code>, <code>columns</code>. Twenty seconds that save hours."),
            ("arw", "pick the columns you want, by name"),
            ("op", "Select, then convert",
             "<code>df[['size','beds']].to_numpy()</code>. Names first, because after the "
             "conversion there are no names."),
            ("arw", "check the shapes before doing anything else"),
            ("op", "X is (m, n) and y is (m,)",
             "One bracket gives <b>(m,)</b>; two give <b>(m, 1)</b>. They print the same "
             "and are not the same."),
            ("arw", "now the maths, with no Python loops"),
            ("op", "Vectorised arithmetic",
             "<code>@</code> for dot products, broadcasting for biases, <code>axis</code> "
             "for per-column or per-row answers."),
            ("arw", "and when it breaks, which it will"),
            ("out", "Read the error from the bottom",
             "The last line names the problem. Print the shapes, print the types."),
        ], cap="""Nothing in this week is machine learning. It is the plumbing every later
week runs through, and plumbing failures are the single most common reason a lab does not
work."""),

        h2("🧱", "What this week rests on"),
        carried("""Week 1 gave you the maths. This week gives you the same ideas in the
notation you will actually type.""",
                [("The dot product", "F0 W1 · 10", "becomes <code>a @ b</code> — one "
                                                   "character"),
                 ("Matrices and shapes", "F0 W1 · 11–12", "becomes <code>.shape</code>, and "
                                                          "the error message when it is wrong"),
                 ("Transpose", "F0 W1 · 13", "becomes <code>.T</code>"),
                 ("Σ and the mean", "F0 W1 · 07, 17", "become <code>.sum(axis=)</code> and "
                                                      "<code>.mean(axis=)</code>"),
                 ("min, max, argmax", "F0 W1 · 19", "become <code>np.max</code> and "
                                                    "<code>np.argmax</code>")],
                head=("The idea", "Where you met it", "What you type instead")),

        h2("⚠️", "The five silent failures"),
        key("""<p>None of these raises an error. That is what makes them worth learning as a
list rather than meeting one at a time.</p>"""),
        values([("<code>[1,2,3] * 2</code>", "repeats the list",
                 "you wanted <code>np.array([1,2,3]) * 2</code>, which doubles"),
                ("<code>(3,1) + (1,3)</code>", "gives (3, 3)",
                 "broadcasting stretched <b>both</b>. Nine numbers where you wanted three"),
                ("<code>a * b</code> on square matrices", "runs, wrong answer",
                 "elementwise where you meant <code>@</code>. Same shape out, so nothing warns"),
                ("<code>df[['price']]</code>", "gives (m, 1)",
                 "one bracket gives (m,), which is what libraries want"),
                ("<code>reshape</code> instead of <code>.T</code>", "scrambles the data",
                 "same shape out, different numbers in it")],
               "five things that look right and are not"),

        h2("🔑", "The one rule that settles axis"),
        key("""<p><b>The axis you name is the one that disappears.</b></p>
<p>A <b>(3, 4)</b> table summed with <code>axis=0</code> loses the 3 and gives <b>(4,)</b>
— one answer per column. With <code>axis=1</code> it loses the 4 and gives <b>(3,)</b> —
one answer per row.</p>
<p>So do not try to remember which is which. Ask <b>what shape you want out</b>, then name
the number that has to go. One statistic per feature is <code>axis=0</code>; one prediction
per example is <code>axis=1</code>.</p>"""),

        h2("🩺", "How to debug anything in this week"),
        chain([
            dict(name="Read the last line first",
                 does="A traceback is read from the <b>bottom</b>. The final line names the "
                      "error in plain English, and that is the answer about 80% of the time.",
                 trap="The middle is library code you did not write and do not need to read. "
                      "A fifty-line traceback is not harder than a five-line one.",
                 feeds="you now know WHAT went wrong. Next: where."),
            dict(name="Print the shapes",
                 does="Two lines, above the line that failed.",
                 code="print(X.shape, y.shape)",
                 trap="Most errors here are shape errors wearing a different name — "
                      "<code>ValueError: shapes not aligned</code> is the honest one, but "
                      "broadcasting failures arrive disguised.",
                 feeds="if the shapes are right, it is a type problem."),
            dict(name="Print the types",
                 does="Is it a list where you expected an array? An object column where you "
                      "expected floats?",
                 code="print(type(X), X.dtype)",
                 trap="<code>dtype=object</code> on a numeric column means one stray "
                      "&ldquo;N/A&rdquo; turned the whole column into text. "
                      "<code>df.info()</code> catches this before you ever start.",
                 feeds=None),
        ]),

        h2("🚧", "What this week deliberately leaves out"),
        trap("""<p><b>No plotting.</b> matplotlib appears in the labs; this week is about
getting the data into the right shape first.</p>
<p><b>No scikit-learn.</b> Deliberately — Course 1 asks you to write gradient descent
yourself, and a library that does it for you would make that pointless.</p>
<p><b>No writing fast code.</b> Vectorisation here is about <b>correctness and readability</b>;
the speed argument comes in C1 W2, with numbers.</p>"""),

        h2("🗣", "Say the week back"),
        retell([
            "What a NumPy array can do that a Python list cannot, and one way that bites.",
            "Which elements <code>x[1:4]</code> gives, and how many.",
            "The one rule for <code>axis</code>, in a single sentence.",
            "The broadcasting rule, and the shape pair that silently gives you nine numbers.",
            "The difference between <code>*</code> and <code>@</code>, and why it is dangerous.",
            "Why <code>(preds == y).mean()</code> computes accuracy.",
            "How <code>reshape(3,2)</code> and <code>.T</code> differ on the same array.",
            "The five pandas calls to run on any new dataset, and which one catches the classic bug.",
            "Why you select columns before <code>to_numpy()</code>, not after.",
            "Which line of a traceback you read first, and what you print next.",
        ]),

        h2("🪜", "Where this week sits in the whole arc"),
        ladder("F0", """Week 1 was the notation; this week is the keyboard. From Course 1
onwards every idea arrives twice — once as a formula and once as a line of NumPy — and this
week is what makes the second version readable. It is also the week that decides whether the
labs are enjoyable or miserable, because almost every lab failure is a shape, a type or a
column name rather than a misunderstanding about machine learning."""),
    ]),
)
