# -*- coding: utf-8 -*-
"""Active Mastery for 08_pca.py.

Depth note (brief §6): the variable table carries most of the weight here,
because "what IS a principal component" is the honest hard question. The
anchor is that [3,5] and [5,3] project to the SAME z -- mirror pairs about
the 45-degree line collapse, so you can point at exactly what PCA discarded.

Non-duplication: the c3w2 deck already covers the PCA algorithm, what PCA is
for, and what to do before it; the mock quiz covers explained_variance_ratio.
None of that is repeated here.
"""
from masterykit import (section, prose, code, out, semantics, ledger, drill, peek,
                        predict, lab, breaks, invariant, wrong, reconstruct,
                        connections, recall, check)

AM = dict(
    lede="Eleven cards on the file where you can point at <b>exactly which information was "
         "thrown away</b> &mdash; because two of its five points come back identical.",
    sections=[

section("0", "&#129517;", "Before you run", "before", kind="orient",
    hook="Five points chosen so the answer is checkable by hand.",
    body=prose("""<p>Five 2-D points, a covariance matrix you can compute in your head, and
eigenvalues that come out as exactly <b>3</b> and <b>1</b>. Nothing here is approximate.</p>
<p><b>Watch for three things.</b> The first component comes out as <b>[0.7071, 0.7071]</b>,
which is 1/&radic;2 &mdash; exactly 45&deg;. The reconstruction turns <b>five distinct
points into two</b>. And the same answer arrives twice, by eigendecomposition and by SVD,
agreeing &ldquo;up to sign&rdquo; &mdash; a phrase worth understanding before you meet it in
someone else's output.</p>""")
    + connections([], [], "../gist/c32.html", "C3 Week 2 &mdash; the gist",
        extra=[("lab", "../scratch/07-kmeans.html", "File 07 first",
                "the other unsupervised file &mdash; that one has no exact answer, this one does")])),

section("1", "&#127991;&#65039;", "What every variable is", "vars", kind="semantics",
    hook="Eight variables, and the honest answer to “what is a component” is in row four.",
    body=semantics([
        ("X", "(5, 2) float64", "the raw points",
         "<b>One row = one point in a plane.</b> Abstract coordinates &mdash; the file gives "
         "them no real-world meaning, and inventing one would add nothing.",
         "<i>arbitrary length units</i>",
         "<code>X[2]</code> is [3.0, 5.0]. Its mirror, <code>X[4]</code>, is [5.0, 3.0] "
         "&mdash; remember that pair.",
         "Both columns span 1&ndash;5, so no scaling step appears. Give one column a 1000&times; "
         "range and it would dominate the covariance entirely."),
        ("mu", "(2,) float64", "the column means",
         "The centre of the cloud: <b>[3.0, 3.0]</b> exactly, because the points were chosen "
         "symmetrically.",
         "<b>same units as X</b>",
         "<code>mu</code> is the point PCA measures everything <i>from</i>. It is not a data "
         "point and need not be near one.",
         "Skip the centring and the first component points at <b>where the data is</b> rather "
         "than at its shape &mdash; which is a different question with a different answer."),
        ("Xc", "(5, 2) float64", "the centred points",
         "The same five points, restated as offsets from the middle. Every column now sums "
         "to zero.",
         "<b>same units as X</b>",
         "<code>Xc[2]</code> is [0, 2] &mdash; point 3 sits two units above the centre in y "
         "and exactly on it in x.",
         "This is what the covariance is computed from. Everything downstream is about "
         "<b>offsets</b>, never absolute positions."),
        ("C", "(2, 2) float64", "the covariance matrix",
         "<b>How the two columns vary together.</b> Here <code>[[2, 1], [1, 2]]</code> "
         "&mdash; each column has variance 2, and they co-vary by 1.",
         "<b>(length units)&sup2;</b>",
         "<code>C[0,1]</code> is 1.0, and it equals <code>C[1,0]</code>. Covariance matrices "
         "are <b>symmetric by construction</b>.",
         "That symmetry is not cosmetic: it guarantees the eigenvalues are <b>real</b> and "
         "the eigenvectors <b>perpendicular</b>, which is why PCA is well behaved rather "
         "than merely plausible."),
        ("vals", "(2,) float64", "the eigenvalues",
         "<b>The variance along each component.</b> This is the honest definition &mdash; an "
         "eigenvalue is not an abstract scalar here, it is a spread.",
         "<b>(length units)&sup2;</b>",
         "<code>vals</code> is <b>[3.0, 1.0]</b>. So 3 units of variance lie along the first "
         "direction and 1 along the second, and 3/(3+1) = <b>0.75</b>.",
         "They sum to <b>4</b>, which is the total variance &mdash; the same 2 + 2 on C's "
         "diagonal. Rotating the axes moves variance around; it never creates or destroys "
         "any."),
        ("W", "(2, 1) float64", "the principal component",
         "<b>A direction, not a quantity.</b> A unit-length arrow saying which way the data "
         "spreads most. It has no individual meaning &mdash; only the geometry does.",
         "<i>unitless</i> (a unit vector)",
         "<code>W</code> is <b>[0.7071, 0.7071]</b>, which is <b>1/&radic;2</b> in both "
         "entries &mdash; exactly <b>45&deg;</b>, equal parts of both columns.",
         "Its <b>length is 1</b>, which is what makes <code>Xc @ W</code> a distance "
         "rather than a distance times something. And it is only defined <b>up to sign</b>: "
         "[&minus;0.707, &minus;0.707] is the same axis."),
        ("Z", "(5, 1) float64", "the projections",
         "<b>How far along the component each point's shadow falls.</b> Two numbers per "
         "point become one.",
         "<b>same units as X</b>",
         "<code>Z</code> is [&minus;2.1213, &minus;2.1213, 1.4142, 1.4142, 1.4142] &mdash; "
         "note that <b>two points share the first value and three share the second</b>.",
         "That collapse is not a bug. It is precisely the information PCA decided to lose, "
         "and section 2 makes you name it."),
        ("Xr", "(5, 2) float64", "the reconstruction",
         "The projections pushed back into the original 2-D space &mdash; what survives a "
         "round trip.",
         "<b>same units as X</b>",
         "<code>Xr</code> holds only <b>two distinct points</b>: [1.5, 1.5] twice and "
         "[4.0, 4.0] three times. Five points went in.",
         "The gap between <code>X</code> and <code>Xr</code> <b>is</b> the cost of the "
         "compression, and here you can read it off point by point."),
    ],
    """The row that matters is <b>W</b>. A principal component is a <b>direction</b>, not a
feature and not a measurement &mdash; nobody labelled it, it has no units, and its individual
numbers mean nothing. Only the geometry it defines carries information, which is exactly the
property embeddings run on."""),
    ),

section("2", "&#128302;", "Prediction checkpoints", "predict", kind="predict",
    hook="Four, and the second asks you to name what was destroyed.",
    body=predict([
        ("""The covariance matrix is <code>[[2, 1], [1, 2]]</code>. <b>Predict its two
eigenvalues before running anything</b> &mdash; this one is doable in your head.""",
         """<p><b>3 and 1.</b></p>
<p>For a symmetric matrix <code>[[a, b], [b, a]]</code> the eigenvectors are always
<b>[1, 1]</b> and <b>[1, &minus;1]</b>, with eigenvalues <b>a + b</b> and <b>a &minus;
b</b>. Here 2 + 1 = 3 and 2 &minus; 1 = 1.</p>
<p>Which also tells you the component before you compute it: [1, 1] normalised is
<b>[0.7071, 0.7071]</b>, exactly 45&deg;.</p>"""),
        ("""<code>Z</code> comes out as [&minus;2.1213, &minus;2.1213, 1.4142, 1.4142,
1.4142] &mdash; only <b>two distinct values</b> for five points. <b>Name the pairs that
collapsed, and say what they have in common.</b>""",
         """<p><b>[1,2] with [2,1]</b>, and <b>[3,5] with [5,3]</b> &mdash; each pair is a
<b>mirror image about the line y = x</b>.</p>
<p>The component points along y = x, so a point and its mirror have <b>identical shadows</b>
on it. What distinguishes them lives entirely in the perpendicular direction, and that is the
direction PCA discarded.</p>
<p>So you can say exactly what was lost: <b>which side of the 45&deg; line a point was
on.</b> Not &ldquo;some information&rdquo; &mdash; that specific fact.</p>"""),
        ("""The SVD route prints &ldquo;same direction as eigen route (<b>up to sign</b>):
True&rdquo;. Why is that qualifier there, and is it a defect?""",
         """<p>Not a defect. An eigenvector describes a <b>line</b>, and a line has <b>two</b>
directions: <b>[0.707, 0.707]</b> and <b>[&minus;0.707, &minus;0.707]</b> describe the same
axis.</p>
<p>Nothing in the definition picks between them, so different implementations &mdash; and
different runs of the same one &mdash; can return either. Sign flips between LAPACK versions
are normal and mean nothing.</p>
<p>The practical consequence: never compare components with <code>==</code>. Compare
<code>abs(a &middot; b)</code> against 1, or fix a convention such as &ldquo;largest component
positive&rdquo;.</p>"""),
        ("""50 noisy features are generated from just <b>3</b> underlying ones. Predict how
much variance the first 3 components explain, and how much the 4th adds.""",
         """<p>The first three explain <b>0.9991</b>; the fourth adds <b>0.0001</b>.</p>
<p>PCA <b>found the 3</b>. It was never told there were three latent factors or that 50
columns were redundant &mdash; it read it off the eigenvalues.</p>
<p>The curve shape is what you look for in practice: a steep climb (0.3848, 0.7353,
<b>0.9991</b>), then a cliff. Where it flattens is how many components are worth keeping.</p>"""),
    ],
    """The second one is the point of the file. Commit to naming the pairs before you
look.""")),

section("3", "&#128295;", "Modify the copy", "lab", kind="lab",
    hook="Five, including one that makes the second eigenvalue exactly zero.",
    body=lab([
        ("L1", "Change a value",
         "Move <code>X[4]</code> from [5, 3] to [5, 5] and re-run. Predict what happens to "
         "<code>Z</code> before you look.",
         "X = np.array([[1., 2.], [2., 1.], [3., 5.], [4., 4.], [5., 5.]])",
         """<p>The mirror symmetry breaks, so <code>Z</code> now has <b>more distinct
values</b> &mdash; [3,5] and [5,5] are no longer reflections, so they no longer share a
shadow.</p>
<p>The eigenvalues shift too: the cloud is no longer balanced about y = x, so the first
component rotates away from exactly 45&deg; and 0.7071 stops being exact.</p>
<p>The lesson: the clean numbers in this file are a <b>property of the chosen data</b>, not
of PCA. Real data gives you 0.6834 and 0.7300, and nothing is checkable by hand.</p>"""),
        ("L2", "Change a parameter",
         "Ask for <code>k = 2</code> instead of 1 &mdash; keep <b>both</b> components &mdash; "
         "then reconstruct and compare with X.",
         "W, vals = pca_eig(X, k=2)",
         """<p>The reconstruction is <b>exact</b>, to floating-point noise. Nothing is
lost.</p>
<p>Which makes the point that PCA with <b>k = n</b> is not compression at all &mdash; it is a
pure <b>rotation</b>. All the information is still there, just expressed along different axes.
Compression only begins when you <b>truncate</b>.</p>
<p>So PCA is two separate ideas: rotate so the interesting direction comes first, then decide
how many to keep. Only the second one loses anything.</p>"""),
        ("L3", "Change the data",
         "Make the second column an exact copy of the first, then look at the eigenvalues.",
         "X = np.array([[1., 1.], [2., 2.], [3., 3.], [4., 4.], [5., 5.]])",
         """<p>The eigenvalues come out <b>[4.0, 0.0]</b> &mdash; the second is <b>exactly
zero</b> &mdash; and the reconstruction error is <b>7.89e&minus;32</b>, which is lossless at
the limit of float64.</p>
<p>A zero eigenvalue means there is <b>no spread at all</b> in that direction. The second
column carried nothing the first did not already have, so discarding it costs literally
nothing.</p>
<p>This is the clean version of what PCA does on real data, where columns are <i>partly</i>
redundant so eigenvalues are small rather than zero.</p>"""),
        ("L4", "Change an assumption",
         "Skip the centring &mdash; pass <code>X</code> straight to <code>covariance</code> "
         "&mdash; and compare the first component.",
         "C = covariance(X)          # was covariance(Xc)",
         """<p>The component swings towards <b>[0.707, 0.707]</b>&hellip; which looks
unchanged, because this cloud happens to sit at [3, 3], <b>along the same 45&deg;
line</b>.</p>
<p>So the bug hides here. Shift the data to <code>X + [10, 0]</code> and re-run: now the
uncentred version points at <b>where the data is</b> rather than at how it is shaped, and the
answer is completely wrong.</p>
<p>The invariant: <b>PCA measures spread from the origin</b>, so the origin has to be the
middle. A test that passes on symmetric data proves nothing.</p>"""),
        ("L5", "Explain it",
         "Explain why <code>W</code> must have length exactly 1, and what would go wrong if it "
         "were twice as long.",
         None,
         """<p>Because <code>Z = Xc @ W</code> only gives the <b>distance along
W</b> when W is a unit vector. Double W's length and every projection doubles &mdash; the
number would then measure the <i>direction's size</i> as well as the point's position.</p>
<p>The reconstruction would break too: <code>Xr = Z @ W.T + mu</code> assumes the same unit
scale on the way back, so a non-unit W would over-shoot by that factor squared.</p>
<p>This is why principal components are always returned normalised, and why you can dot with
them directly and read the answer as a distance.</p>"""),
    ],
    """L4 is the one to run twice &mdash; once as written, where the bug is invisible, and once
on shifted data, where it is obvious.""")),

section("4", "&#128165;", "Break it, then repair it", "break", kind="debug",
    hook="Four, and two of them return a perfectly plausible wrong answer.",
    body=breaks([
        ("order = np.argsort(vals)          # ascending, not descending",
         "Sort the eigenvalues the wrong way and keep the &ldquo;first&rdquo; component. "
         "Predict the variance explained.",
         """<p>You keep the <b>smallest</b> direction: variance explained becomes
<b>0.25</b> instead of 0.75, and the projection captures the least interesting axis.</p>
<p>Nothing errors, the shapes are right, and a reconstruction still comes back. On this data
you would notice because 0.25 is obviously wrong &mdash; on 50 features you would not.</p>
<p>The invariant: <b>eigenvalues must come back sorted largest-first</b>, and
<code>np.linalg.eigh</code> returns them <b>ascending</b>. That off-by-a-reversal is the most
common PCA bug there is.</p>"""),
        ("Z = Xc @ W\nXr = Z @ W.T                 # the mu is never added back",
         "Forget to add <code>mu</code> back during reconstruction. Predict what "
         "<code>Xr</code> looks like.",
         """<p>Every reconstructed point is shifted by <b>&minus;[3, 3]</b> &mdash; the
<b>shape</b> is perfect and the <b>position</b> is wrong. <code>Xr[0]</code> comes back as
[&minus;1.5, &minus;1.5] instead of [1.5, 1.5].</p>
<p>If you only ever plot the reconstruction it looks completely correct, because a scatter
plot of a shifted cloud looks like the cloud. It fails the moment you compute an error against
the original.</p>
<p>The invariant: <b>centring and reconstruction are a matched pair.</b> Subtract mu going in,
add it back coming out &mdash; the same discipline as the scaling statistics in files 01 and
14.</p>"""),
        ("W = W / np.linalg.norm(W) * 2      # deliberately not unit length",
         "Scale the component to length 2. Predict whether the reconstruction still works.",
         """<p>The projections <b>double</b> and the reconstruction <b>overshoots by a factor
of 4</b> &mdash; because the error is applied once on the way out and once on the way
back.</p>
<p>No error is raised. You get a reconstruction that is systematically wrong by a constant
factor, which looks like a scaling bug in your data pipeline rather than in your PCA.</p>
<p>The invariant: <b>&#8214;W&#8214; = 1</b>, and it is worth asserting rather than
assuming.</p>"""),
        ("Xc, mu = centre(X)\nC = Xc.T @ Xc                # the / (m-1) is gone",
         "Drop the normalisation from the covariance. What changes, and what does not?",
         """<p>The <b>eigenvalues scale by (m&minus;1) = 4</b> &mdash; [12, 4] instead of
[3, 1] &mdash; but the <b>eigenvectors are identical</b>, so the component and the projections
are unchanged.</p>
<p>And variance <i>explained</i> is unchanged too: 12/(12+4) is still <b>0.75</b>, because the
ratio cancels the factor.</p>
<p>The invariant worth taking: <b>scaling a matrix scales its eigenvalues and leaves its
eigenvectors alone.</b> So this bug is invisible in every relative measure and only shows up
if you quote an eigenvalue as a variance &mdash; which the semantics table says you
should.</p>"""),
    ],
    """The last one is unusually instructive: a real bug that changes an absolute number,
leaves every ratio correct, and therefore survives most tests.""")),

section("5", "&#9878;&#65039;", "The invariant", "invariant", kind="invariant",
    hook="Two routes, one answer — and the eigenvalues must sum to the total variance.",
    body=invariant("""<p><b>Eigendecomposition and SVD must agree up to sign, the components
must be unit-length and perpendicular, and the eigenvalues must sum to the total variance in
the data.</b></p>""",
    """<p>The file checks the first directly and prints <code>same direction as eigen route
(up to sign): True</code> and <code>same eigenvalues: True</code>. Two genuinely different
algorithms reaching one answer is the strongest evidence available that the implementation is
right.</p>
<p>The third is the one people never check and it is free: here <code>vals</code> is
<b>[3, 1]</b> summing to <b>4</b>, and the diagonal of <code>C</code> is <b>2 + 2 = 4</b>.
Rotating the axes <b>moves variance around; it never creates or destroys any</b>. If your
eigenvalues do not sum to the trace, your covariance or your sort is wrong.</p>""",
    """assert np.allclose(np.linalg.norm(W, axis=0), 1.0)          # unit length
assert np.allclose(W.T @ W, np.eye(W.shape[1]), atol=1e-12)  # perpendicular
assert np.isclose(vals.sum(), np.trace(C))                   # variance conserved
assert np.allclose(np.abs(W_eig.T @ W_svd), 1.0)             # agree, up to sign""")),

section("6", "&#129535;", "Wrong mental models", "wrong", kind="myths",
    hook="Five, and the first is the one that makes people over-claim in reports.",
    body=wrong([
        ("A principal component is a meaningful feature you can name.",
         """<p>It is a <b>direction</b> with no individual meaning. <code>W</code> here is
[0.7071, 0.7071] &mdash; equal parts of both columns, and nobody labelled it.</p>
<p>People routinely write &ldquo;PC1 represents overall size&rdquo; in reports. Sometimes a
component <i>is</i> interpretable, but that is a happy accident of the data, never something
PCA provides. The numbers are uninterpretable and the <b>distances between them</b> are
meaningful anyway &mdash; the same property embeddings run on.</p>"""),
        ("PCA loses a little of everything, evenly.",
         """<p>It loses <b>specific</b> things completely and keeps others perfectly. Here
<b>[3,5] and [5,3] become the same point</b>, and so do [1,2] and [2,1].</p>
<p>What was destroyed is nameable: <b>which side of the 45&deg; line a point was on</b>.
Everything along that line survived exactly. Compression by projection is not lossy in a
diffuse way &mdash; it is lossy in one precise direction.</p>"""),
        ("A sign flip in the components means something went wrong.",
         """<p>An eigenvector describes a <b>line</b>, and a line has two directions.
[0.707, 0.707] and [&minus;0.707, &minus;0.707] are the <b>same axis</b>.</p>
<p>Nothing in the definition picks between them, so implementations differ and even library
versions differ. Compare with <code>abs(a &middot; b) &asymp; 1</code>, never with
<code>==</code>.</p>"""),
        ("The eigenvalues are abstract scalars.",
         """<p>They are <b>variances</b>, in the squared units of your data. <code>vals</code>
= [3, 1] means <b>3 units of spread along the first direction and 1 along the second</b>.</p>
<p>That is why they sum to the total variance (the trace of C, here 4) and why the ratio
3/(3+1) = <b>0.75</b> is a meaningful &ldquo;fraction explained&rdquo;. Treating them as
dimensionless is what makes people forget that <b>scaling the matrix scales them</b>.</p>"""),
        ("Eigendecomposition and SVD are interchangeable, so use whichever.",
         """<p>They agree <b>here</b>, on a square symmetric covariance matrix &mdash; and the
file proves it.</p>
<p>But eigendecomposition <b>requires</b> a square matrix, so it can only ever be applied to
the covariance, and forming that covariance means <b>squaring your numbers</b>, which throws
away precision you cannot get back. SVD works on the data matrix directly, whatever its shape.
That is why real implementations use SVD, and it is a numerical argument rather than a
mathematical one.</p>"""),
    ])),

section("7", "&#127959;&#65039;", "Reconstruction challenge", "reconstruct", kind="rebuild",
    hook="Rebuild it, then prove it with the trace identity.",
    body=reconstruct([
        ("Explain", "In three sentences, describe PCA without the words <i>eigenvector</i> or "
         "<i>variance</i>.",
         """<p>Find the direction in which the cloud of points is most stretched out. Measure
how far along that direction each point sits, and keep only that number. Repeat with the next
most stretched direction that is at right angles to the first, for as many as you want to
keep.</p>"""),
        ("Skeleton", "Write the five signatures from memory.",
         """<p><code>centre(X)</code> returning <b>(Xc, mu)</b>, <code>covariance(Xc)</code>,
<code>pca_eig(X, k)</code> returning <b>(W, vals)</b>, <code>project(X, W, mu)</code> and
<code>reconstruct(Z, W, mu)</code>.</p>
<p>The detail people miss: <code>centre</code> returns <b>two</b> things, because
<code>mu</code> has to survive until reconstruction. Throw it away and you cannot come
back.</p>"""),
        ("Core", "Write pca_eig from memory, sorting included.",
         """<p>Centre, compute the covariance, call <code>np.linalg.eigh</code>, then
<b>reverse</b> &mdash; <code>eigh</code> returns eigenvalues <b>ascending</b> and you want the
largest first. Slice the top k columns.</p>
<p>Use <code>eigh</code> and not <code>eig</code>: the covariance is symmetric, and
<code>eigh</code> exploits that to return real, sorted, orthogonal results. <code>eig</code>
can hand you complex numbers with tiny imaginary parts for a matrix that is symmetric in
exact arithmetic.</p>"""),
        ("Minimal", "Build the smallest dataset where the second eigenvalue is exactly zero, "
         "and one where both are equal.",
         """<p><b>Zero:</b> any dataset where one column is an exact function of the other
&mdash; [[1,1],[2,2],[3,3]&hellip;] gives [4, 0].</p>
<p><b>Equal:</b> a symmetric cloud with no preferred direction, such as the four points
(&plusmn;1, 0) and (0, &plusmn;1). Both eigenvalues match, so <b>no direction is
&ldquo;first&rdquo;</b> and the component you get back is arbitrary &mdash; a real degenerate
case worth having met.</p>"""),
        ("Verify", "Check your rebuild without comparing to the original.",
         """<p>Four assertions, all self-contained: components are unit length; components are
mutually perpendicular (<code>W.T @ W</code> is the identity); <b>eigenvalues sum to the trace
of C</b>; and reconstruction with <b>k = n</b> is exact.</p>
<p>The trace check is the one that catches a wrong covariance or a missing normalisation, and
it costs one line.</p>"""),
    ],
    """The trace identity is the most under-used check in PCA and it fully constrains the
eigenvalues.""")),

section("8", "&#128279;", "Connections", "conn", kind="links",
    hook="Unsupervised like 07, exact unlike 07 — and the same SVD that 11 uses.",
    body=connections(
        [("lab", "../scratch/07-kmeans.html", "Contrast with 07",
          "also unsupervised, but non-deterministic with no exact answer"),
         ("lab", "../scratch/09-collaborative-filtering.html", "Alongside 09",
          "learned dimensions that mean nothing individually &mdash; the same idea")],
        [("lab", "../scratch/11-retrieval.html", "On to 11",
          "this exact SVD, pointed at text: 116 sparse dimensions down to 6")],
        "../gist/c32.html", "C3 Week 2 &mdash; the gist",
        extra=[("docs", "../reference.html", "Reference &mdash; F0 W3",
                "<code>f0-eigen</code> and <code>f0-svd</code> carry the linear algebra "
                "this file applies")])),

section("9", "&#9670;", "Recall sheet", "recall", kind="recall",
    hook="Six cards, all about this file's numbers.",
    body=recall([
        ("<code>C = [[2, 1], [1, 2]]</code>. Give both eigenvalues and the first component, "
         "in your head.",
         "For <code>[[a,b],[b,a]]</code> the eigenvalues are <b>a+b</b> and <b>a&minus;b</b> "
         "&mdash; so <b>3</b> and <b>1</b> &mdash; with eigenvectors [1,1] and [1,&minus;1]. "
         "Normalised, the first is <b>[0.7071, 0.7071]</b>, exactly 45&deg;."),
        ("Five points project to only <b>two</b> distinct values. Which pairs collapsed, and "
         "what did PCA discard?",
         "<b>[1,2] with [2,1]</b> and <b>[3,5] with [5,3]</b> &mdash; mirror images about "
         "y = x. What was thrown away is precisely <b>which side of the 45&deg; line a point "
         "was on</b>."),
        ("What does &ldquo;the components agree <b>up to sign</b>&rdquo; mean, and why is it "
         "not a defect?",
         "An eigenvector describes a <b>line</b>, which has two directions. [0.707, 0.707] and "
         "[&minus;0.707, &minus;0.707] are the same axis. Compare with "
         "<code>abs(a&middot;b) &asymp; 1</code>, never <code>==</code>."),
        ("Eigenvalues [3, 1]. What must they sum to, and why is that worth checking?",
         "The <b>total variance</b> &mdash; the trace of C, here 2 + 2 = <b>4</b>. Rotation "
         "moves variance around and never creates or destroys it, so a mismatch means a wrong "
         "covariance or a missing normalisation."),
        ("You drop the <code>/(m-1)</code> from the covariance. What changes?",
         "The eigenvalues scale by 4 &mdash; [12, 4] &mdash; and the <b>eigenvectors and "
         "projections are unchanged</b>. Variance explained is still 0.75, because the ratio "
         "cancels. Invisible in every relative measure."),
        ("50 noisy features from 3 latent ones. What do the first 3 and 4 components explain?",
         "<b>0.9991</b> and <b>0.9992</b> &mdash; the 4th adds 0.0001. PCA found the 3 without "
         "being told they existed."),
    ],
    """Cover and answer aloud.""")),

section("10", "&#9989;", "Mastery check", "check", kind="check",
    hook="Five, none of them in the C3 W2 quiz.",
    body=check([
        ("""Point at two rows of <code>X</code> that PCA made indistinguishable, and say in
one sentence what property they share.""",
         """<p><b>[3, 5] and [5, 3]</b> &mdash; or equally [1, 2] and [2, 1]. They are
<b>mirror images about the line y = x</b>, which is the direction the component points along,
so their shadows on it are identical.</p>
<p>If you cannot name the discarded quantity, you cannot honestly report what a compression
cost.</p>"""),
        ("""Your colleague's PCA returns components with the opposite signs to yours on the
same data. Who is wrong?""",
         """<p><b>Neither.</b> An eigenvector defines a line, and both signs describe the same
axis. Different LAPACK builds return different conventions.</p>
<p>What <b>would</b> be a real disagreement is different <i>directions</i> &mdash; check
<code>abs(a &middot; b)</code>, which should be 1 for the same axis and less for a different
one.</p>"""),
        ("""You run PCA and the first component explains 0.25 of the variance on data you
expected to be strongly correlated. Name the bug.""",
         """<p>The eigenvalues are sorted the <b>wrong way round</b>. <code>np.linalg.eigh</code>
returns them <b>ascending</b>, so a missing reverse gives you the <b>smallest</b>
direction.</p>
<p>0.25 and 0.75 are complements here, which is the tell: you are not getting noise, you are
getting the other component.</p>"""),
        ("""Explain why real implementations use SVD rather than eigendecomposition, in terms
of precision rather than mathematics.""",
         """<p>Eigendecomposition needs a <b>square</b> matrix, so you must first form the
covariance &mdash; and forming it means <b>squaring your numbers</b>, which squares the
condition number and throws away precision you cannot recover.</p>
<p>SVD works on the data matrix directly, of any shape. Both are mathematically correct here;
only one is numerically sound at scale.</p>"""),
        ("""Someone reports &ldquo;PC1 captures overall customer value&rdquo;. What is your
response?""",
         """<p>That it might be true and PCA did not say so. A component is a <b>direction</b>
&mdash; here [0.7071, 0.7071], equal parts of two columns nobody named.</p>
<p>Interpretability is a property of the <b>data</b>, not an output of the method. The honest
version is &ldquo;PC1 loads roughly equally on spend and frequency, which is consistent with
an overall-value reading&rdquo; &mdash; a hypothesis, not a finding.</p>"""),
    ],
    """None of these appears in the <a href="../quiz/c32.html">C3 W2 mock quiz</a>, which
covers what PCA does, what to do before it, and how to read
the explained-variance ratio.""")),
    ],
)
