# -*- coding: utf-8 -*-
"""The three averages the courses use without distinguishing them.

Weighted averaging is what makes information gain correct — dropping the weights
flatters a tiny pure branch by nearly five times. The harmonic mean is why F1
refuses to be impressed by a lopsided model. Both are used and neither is
compared to the ordinary average anywhere.

Every number below was computed before it was written.
"""

ANCHOR = "means"
TOPIC = "averages"

PATTERNS = [
    (r"weighted (?:average|mean|sum)", "weighted-mean"),
    (r"harmonic mean", "harmonic-mean"),
    (r"\barithmetic mean\b", "arithmetic-mean"),
]

TERMS = [
 dict(key="arithmetic-mean", label="arithmetic mean", say="“the ordinary average”",
      gist="Add them up, divide by how many there are. The one everyone means by "
           "“average”.",
      body="<div class='gq'>(a + b) ÷ 2</div>"
           "<p>It treats every value as equally important, and it sits exactly "
           "halfway between them. That is usually what you want — and twice in "
           "this course it is not.</p>",
      ml="μ in feature scaling, the mean squared error, the mean of a cluster in "
         "k-means."),

 dict(key="weighted-mean", label="weighted average", say="“weighted average”",
      gist="An average where some values count for more than others, because they "
           "represent more.",
      body="<div class='gq'>(w₁a + w₂b) ÷ (w₁ + w₂)</div>"
           "<p>Used whenever the things you are averaging are not the same size. "
           "Averaging the entropy of a branch holding 9 examples and one holding "
           "1 example as though they were equal is simply wrong — the big branch "
           "is nine times as much of the problem.</p>",
      ml="This is the part of information gain that people drop. Without the "
         "size weighting, a branch containing a single pure example looks "
         "wonderful, and the tree chases it."),

 dict(key="harmonic-mean", label="harmonic mean", say="“har-MON-ic mean”",
      gist="An average that leans hard towards the <b>smaller</b> of the two "
           "numbers. It refuses to be impressed by one good score.",
      body="<div class='gq'>2ab ÷ (a + b)</div>"
           "<table class='gtab'>"
           "<tr><td>0.6 and 0.5</td><td>0.55 vs <b>0.545</b></td><td>barely differs</td></tr>"
           "<tr><td>0.9 and 0.1</td><td>0.5 vs <b>0.18</b></td><td>collapses</td></tr>"
           "<tr><td>1.0 and 0.01</td><td>0.505 vs <b>0.0198</b></td><td>collapses hard</td></tr>"
           "</table>"
           "<p>When the two numbers are close it behaves like the ordinary "
           "average. When one is much smaller it follows the small one down.</p>",
      ml="F1 = 2PR ÷ (P + R). A model with precision 1.0 and recall 0.01 scores "
         "0.0198, not 0.505 — which is the honest answer, because it finds almost "
         "nothing."),
]

SVG_BARS = """
<svg viewBox="0 0 260 170" class="gsvg" role="img" aria-label="the same two numbers averaged three ways">
  <line x1="34" y1="140" x2="250" y2="140" stroke="var(--line)" stroke-width="1.4"/>
  <rect x="44" y="34"  width="30" height="106" fill="var(--blue)" opacity=".55"/>
  <rect x="80" y="129" width="30" height="11"  fill="var(--blue)" opacity=".55"/>
  <text x="59" y="28"  class="gs-b" text-anchor="middle">0.9</text>
  <text x="95" y="123" class="gs-b" text-anchor="middle">0.1</text>
  <text x="77" y="156" class="gs-l" text-anchor="middle">the two numbers</text>
  <line x1="126" y1="20" x2="126" y2="146" stroke="var(--line)" stroke-width="1"/>
  <rect x="146" y="81"  width="34" height="59" fill="var(--green)"/>
  <text x="163" y="75"  class="gs-g" text-anchor="middle">0.50</text>
  <text x="163" y="156" class="gs-l" text-anchor="middle">arithmetic</text>
  <rect x="200" y="119" width="34" height="21" fill="var(--accent)"/>
  <text x="217" y="113" class="gs-a" text-anchor="middle">0.18</text>
  <text x="217" y="156" class="gs-l" text-anchor="middle">harmonic</text>
</svg>"""

SVG_WEIGHT = """
<svg viewBox="0 0 260 170" class="gsvg" role="img" aria-label="a lopsided split, weighted against unweighted">
  <rect x="30" y="30" width="126" height="34" fill="var(--blue-soft)" stroke="var(--blue)" stroke-width="1.6"/>
  <text x="93" y="52" class="gs-b" text-anchor="middle">9 examples, mixed</text>
  <rect x="164" y="30" width="24" height="34" fill="var(--green-soft)" stroke="var(--green)" stroke-width="1.6"/>
  <text x="176" y="52" class="gs-g" text-anchor="middle">1</text>
  <text x="206" y="52" class="gs-l">pure</text>
  <text x="30" y="92" class="gs-l">weighted, correct</text>
  <rect x="30" y="98" width="34" height="13" fill="var(--green)"/>
  <text x="70" y="109" class="gs-g">gain 0.108</text>
  <text x="30" y="130" class="gs-l">unweighted, wrong</text>
  <rect x="30" y="136" width="159" height="13" fill="var(--red)"/>
  <text x="195" y="147" class="gs-a" fill="var(--red)">gain 0.505</text>
</svg>"""

PANEL = """
<section class="bonus" id="means">
<header><span class="bonus-badge">bonus</span>
<h3>Three kinds of average, and when each is wrong</h3>
<span class="n">3 terms</span></header>
<p class="bonus-lede">&ldquo;Average&rdquo; is used loosely across the courses for three different
calculations. Twice it matters a great deal which one is meant, and in one of those cases
using the wrong one silently breaks a decision tree.</p>

<div class="bonus-grid">
  <div class="bonus-fig">%s
    <p class="cap">The same two numbers, <b>0.9</b> and <b>0.1</b>, averaged two ways. The
    ordinary average says 0.50 &mdash; respectable. The harmonic mean says <b>0.18</b>, because
    one of the two is nearly zero and pretending otherwise would be dishonest.</p>
  </div>
  <div class="bonus-fig">%s
    <p class="cap">A lopsided split: nine mixed examples and one pure one. Weighting by branch
    size gives a gain of <b>0.108</b>. Forgetting the weights gives <b>0.505</b> &mdash; nearly
    five times too flattering, and the tree takes the useless split.</p>
  </div>
</div>

<table class="gbig">
<thead><tr><th>average</th><th>formula</th><th>0.9 and 0.1</th><th>use it when</th></tr></thead>
<tbody>
<tr><td>arithmetic</td><td class="f">(a + b) &divide; 2</td><td class="f">0.500</td><td>the values count equally</td></tr>
<tr><td>weighted</td><td class="f">(w&#8321;a + w&#8322;b) &divide; (w&#8321; + w&#8322;)</td><td class="f">depends on w</td><td>some values represent more than others</td></tr>
<tr><td>harmonic</td><td class="f">2ab &divide; (a + b)</td><td class="f">0.180</td><td>a single bad score should sink the result</td></tr>
</tbody></table>

<div class="bonus-cols">
<div>
<h4>Where each one is load-bearing</h4>
<ul class="bonus-list">
<li><b>Information gain</b> (C2 W4) &mdash; <b>weighted</b>. The children's entropies are
averaged <i>by branch size</i>. Drop the weights and a branch holding one pure example looks
like a triumph.</li>
<li><b>F1</b> (C2 W3) &mdash; <b>harmonic</b>. Chosen precisely so that precision 1.0 with
recall 0.01 scores <span class="f">0.0198</span> rather than 0.505.</li>
<li><b>Cost functions</b> (everywhere) &mdash; <b>arithmetic</b>. Every example counts once.</li>
<li><b>Ensembles</b> (C2 W4) &mdash; boosting uses a <b>weighted</b> vote; bagging uses a plain
one.</li>
</ul>
</div>
<div>
<h4>An honest caveat</h4>
<p style="font-size:13.5px">When the branches happen to be the <b>same size</b>, weighting
changes nothing. The lecture's cat dataset splits 5 and 5 on ear shape, so its weighted and
unweighted answers are identical &mdash; both <span class="f">0.7219</span>.</p>
<p style="font-size:13.5px">That is exactly why the mistake survives: it agrees with the
correct answer on the worked example everybody checks against, and only diverges on the
lopsided splits that occur deeper in a real tree.</p>
</div>
</div>

<div class="bonus-trap"><span class="tag">The trap</span>
<p><b>The harmonic mean is not &ldquo;a stricter average&rdquo;.</b> It is close to the ordinary
average when the two numbers are close &mdash; 0.6 and 0.5 give 0.55 and 0.545, a difference of
half a percent. It only diverges when they are far apart, and then it follows the smaller one.
That is the entire behaviour, and it is why F1 is safe to quote without also quoting precision
and recall &mdash; though you should quote them anyway.</p>
</div>
<div class="scribble"><span class="lbl">&#9998; on paper</span>Write 0.9 and 0.1 at the top. Underneath draw three bars: the two numbers, then their ordinary average at 0.5, then the harmonic at 0.18. Then draw a lopsided split &mdash; nine boxes and one box &mdash; and write both gains, 0.108 and 0.505. Ring the wrong one.</div>
</section>
""" % (SVG_BARS, SVG_WEIGHT)
