# -*- coding: utf-8 -*-
"""Walkthrough for 08_pca.py."""
from walkkit import p, expr, chain, chainset, steps, cases, values, point, ascii_art

PICTURE = ([
    ("in", "Data with many columns", "Some of them saying much the same thing as others."),
    ("arw", "subtract each column's mean &mdash; this is not optional"),
    ("op", "Centre it", "Every column now has mean 0, so &ldquo;spread&rdquo; is measured "
                        "from the origin."),
    ("arw", "how does each column vary WITH each other column?"),
    ("op", "Covariance matrix", "A square grid of how the features move together."),
    ("arw", "find the directions this matrix does not rotate"),
    ("op", "Eigenvectors", "The principal components. Their eigenvalues ARE the variance "
                           "along each one."),
    ("arw", "keep the biggest few, throw the rest away"),
    ("out", "Fewer numbers per point",
     "50 columns become 2, chosen to lose as little spread as possible."),
], "The whole program in one picture",
   "PCA is a rotation followed by a truncation. Turn the data so the most interesting "
   "direction is first, then stop keeping the boring ones.")

WALK = {

"prelude": (
    p("""PCA reduces the number of columns while throwing away as little information as
possible. This file builds it twice &mdash; once through eigenvectors, once through SVD
&mdash; and shows they agree.""")
),

"centre": (
    p("""Subtract each column's mean. Every column now has mean <b>0</b>.""")
    + point("""This is not tidying. PCA looks for <b>directions of greatest spread measured
from the origin</b> &mdash; so if the data sits far from the origin, the first component
just points at the data's location rather than at its shape.""")
    + p("""Scaling is usually done too. Otherwise a column measured in thousands dominates
one measured in fractions, and PCA reports which column has the biggest <b>units</b> rather
than which carries the most structure.""")
),

"covariance": (
    p("""Five points, two columns, and column means of exactly <b>[3, 3]</b> &mdash; chosen
so the arithmetic stays checkable.""")
    + p("""The covariance matrix answers: <b>how does each column vary with each other
column?</b> Its diagonal holds each column's own variance; the off-diagonal holds how much
they move <b>together</b>.""")
    + point("""It is <b>symmetric</b> by construction &mdash; how x varies with y is the same
as how y varies with x. That symmetry is what makes PCA well behaved, and the next section
is where it pays off.""")
),

"eigen": (
    p("""The eigenvectors of the covariance matrix are the principal components.""")
    + values([("eigenvalues", "[3.0, 1.0]", "the variance along each direction"),
              ("first component", "[0.7071, 0.7071]", "a 45&deg; diagonal"),
              ("variance explained by PC1", "0.7500", "3 out of 3+1")],
             "what this block printed")
    + point("""<b>Each eigenvalue IS the variance along its own eigenvector.</b> That single
fact is why &ldquo;find the direction of greatest spread&rdquo; and &ldquo;find the largest
eigenvector of the covariance matrix&rdquo; are the same instruction.""")
    + p("""0.7071 is <b>1/&radic;2</b>, so the first component points at exactly 45&deg;
&mdash; equal parts of both columns. And it has length 1, which is what makes
<code>z = x &middot; u</code> a distance rather than a distance times something.""")
    + point("""Because covariance matrices are symmetric, the eigenvalues are guaranteed
<b>real</b> and the eigenvectors guaranteed <b>perpendicular</b>. Perpendicular means the
second component measures something the first one <b>cannot see</b> &mdash; no double
counting.""")
),

"project": (
    p("""Project onto the first component: two numbers per point become one.""")
    + expr("z = x &middot; u", "how far along u this point's shadow falls")
    + values([("projected", "[&minus;2.121, &minus;2.121, 1.414, 1.414, 1.414]", "one number per point"),
              ("reconstructed", "[1.5, 1.5], [1.5, 1.5], [4, 4] &hellip;", "back to two, approximately")],
             "down to 1-D, then back again")
    + point("""The reconstruction is <b>not exact</b>, and that is the whole trade. The first
two points both come back as [1.5, 1.5] &mdash; they were different, and after squashing to
one dimension they are the same point. That difference lived entirely in the direction you
threw away.""")
    + p("""What survives is everything along the 45&deg; line; what is lost is everything
perpendicular to it. PCA chose that line precisely because losing it costs the least.""")
),

"svd": (
    p("""The same answer by a completely different route.""")
    + values([("component", "[0.7071, 0.7071]", "same direction"),
              ("eigenvalues", "[3.0, 1.0]", "same values"),
              ("same up to sign", "True", ""),
              ("same eigenvalues", "True", "")],
             "SVD against the eigenvector route")
    + point("""&ldquo;<b>Up to sign</b>&rdquo; matters. An eigenvector points along a line,
and a line has <b>two</b> directions &mdash; [0.707, 0.707] and [&minus;0.707, &minus;0.707]
describe the same axis. Sign flips between implementations are normal and mean nothing.""")
    + p("""Real PCA uses <b>SVD</b>, not the covariance route. Forming the covariance matrix
means <b>squaring</b> the numbers, which throws away precision you cannot get back. SVD works
on the data directly. Same answer, better conditioned &mdash; and it works on non-square data
too.""")
),

"perfect": (
    p("""A deliberately extreme case: data where the second column is a perfect function of
the first.""")
    + values([("eigenvalues", "[4.0, 0.0]", "the second is <b>exactly</b> zero"),
              ("variance explained by PC1", "1.0000", "all of it"),
              ("reconstruction error", "7.89e&minus;32", "<b>lossless</b>")],
             "perfectly correlated data")
    + point("""A <b>zero</b> eigenvalue means there is <b>no spread at all</b> in that
direction. The second column carried no information the first did not already have, so
discarding it costs literally nothing &mdash; and the error confirms it, at the limit of
floating point.""")
    + p("""This is the clean version of what PCA does on real data. Real columns are
partially redundant, so eigenvalues are small rather than zero, and discarding them costs a
little rather than nothing.""")
),

"higher_dim": (
    p("""The realistic case: <b>50</b> noisy features, all generated from just <b>3</b>
underlying ones.""")
    + values([("first 1 component", "0.3848", "of the variance"),
              ("first 2", "0.7353", ""),
              ("first 3", "<b>0.9991</b>", "essentially everything"),
              ("first 4", "0.9992", "the 4th buys <b>0.0001</b>")],
             "cumulative variance explained")
    + point("""PCA <b>found the 3</b>. It was never told there were three latent factors, or
that 50 columns were redundant. It read it off the eigenvalues.""")
    + p("""And the shape of the curve is what you look for in practice: a steep climb, then a
sharp flattening. The place it flattens is how many components are worth keeping &mdash; the
same elbow logic as choosing K in k-means, and rather more reliable here.""")
    + point("""So 50 columns become 3, losing <b>0.09%</b> of the variance. That is the case
PCA was built for, and it is why the honest modern use is <b>visualisation</b>: squash to 2
and you can actually look at your data.""")
),
}
