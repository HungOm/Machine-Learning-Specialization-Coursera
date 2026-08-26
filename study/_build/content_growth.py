# -*- coding: utf-8 -*-
"""Growth rates — why some algorithms stop working.

"n³", "O(n)" and "does not scale" are used across all three courses to justify
why the normal equation dies on large problems and why vectorization matters.
The claim is always asserted and never shown. One chart settles it.

Every number in the panel is arithmetic, checked before it was written.
"""

ANCHOR = "growth"
TOPIC = "growth rates"

PATTERNS = [
    (r"O\(n(?:\s*log\s*n|\^?[23]|&sup[23];|²|³)?\)", "bigo"),
    (r"\bbig-?O\b", "bigo"),
    (r"n³|n\^3", "cubic"),
    (r"\bquadratic(?:ally)?\b", "cubic"),
    (r"\bdoes ?n[o']t scale\b|\bscales? poorly\b", "bigo"),
]

TERMS = [
 dict(key="bigo", label="O(n)", say="“big oh of n”",
      gist="Shorthand for <b>how the work grows</b> as the problem gets bigger — "
           "not how long it takes.",
      body="<p>Read <b>O(n²)</b> as “double the input and the work goes up "
           "four-fold”. It deliberately ignores constants, because those stop "
           "mattering once n is large:</p>"
           "<table class='gtab'>"
           "<tr><td>O(n)</td><td>double n → double the work</td></tr>"
           "<tr><td>O(n²)</td><td>double n → <b>4×</b> the work</td></tr>"
           "<tr><td>O(n³)</td><td>double n → <b>8×</b> the work</td></tr></table>"
           "<p>So an O(n³) method that is fast on 100 features can be unusable on "
           "1,000 — the same code, nothing wrong with it.</p>",
      ml="This is the whole argument against the normal equation: it inverts an "
         "n×n matrix, which is about n³ work. Gradient descent is roughly O(n) "
         "per step, which is why it survives where the closed form does not."),

 dict(key="cubic", label="n³", say="“n cubed”",
      gist="n multiplied by itself three times. The growth rate that makes "
           "matrix inversion impractical.",
      body="<table class='gtab'>"
           "<tr><td>n = 10</td><td>1,000</td></tr>"
           "<tr><td>n = 100</td><td>1,000,000</td></tr>"
           "<tr><td>n = 1,000</td><td>1,000,000,000</td></tr>"
           "<tr><td>n = 10,000</td><td>1,000,000,000,000</td></tr></table>"
           "<p>At roughly a billion operations a second, the last row is about "
           "<b>17 minutes</b> and the row above it is about <b>one second</b>. "
           "Ten times the features, a thousand times the wait.</p>",
      ml="A matrix multiply of (m,n) by (n,k) costs about m·n·k. That is why "
         "the shape of your data, not just its size, decides what is affordable."),
]

SVG_CURVES = """
<svg viewBox="0 0 260 170" class="gsvg" role="img" aria-label="curves showing linear, quadratic and cubic growth">
  <line x1="34" y1="140" x2="246" y2="140" stroke="var(--line)" stroke-width="1.4"/>
  <line x1="34" y1="140" x2="34" y2="18" stroke="var(--line)" stroke-width="1.4"/>
  <text x="240" y="156" class="gs-l" text-anchor="end">problem size n</text>
  <text x="30" y="16" class="gs-l" text-anchor="end">work</text>
  <path d="M34,140 L246,116" fill="none" stroke="var(--green)" stroke-width="2.6"/>
  <text x="212" y="112" class="gs-g">O(n)</text>
  <path d="M34,140 Q160,136 246,62" fill="none" stroke="var(--blue)" stroke-width="2.6"/>
  <text x="216" y="58" class="gs-b">O(n²)</text>
  <path d="M34,140 Q186,138 224,20" fill="none" stroke="var(--accent)" stroke-width="2.8"/>
  <text x="196" y="26" class="gs-a">O(n³)</text>
</svg>"""

SVG_BARS = """
<svg viewBox="0 0 260 170" class="gsvg" role="img" aria-label="bars comparing the cost of n cubed at four problem sizes">
  <line x1="40" y1="140" x2="250" y2="140" stroke="var(--line)" stroke-width="1.4"/>
  <rect x="52"  y="137" width="26" height="3"   fill="var(--green)"/>
  <rect x="102" y="128" width="26" height="12"  fill="var(--blue)"/>
  <rect x="152" y="92"  width="26" height="48"  fill="var(--amber)"/>
  <rect x="202" y="24"  width="26" height="116" fill="var(--accent)"/>
  <text x="65"  y="154" class="gs-l" text-anchor="middle">10</text>
  <text x="115" y="154" class="gs-l" text-anchor="middle">100</text>
  <text x="165" y="154" class="gs-l" text-anchor="middle">1,000</text>
  <text x="215" y="154" class="gs-l" text-anchor="middle">10,000</text>
  <text x="65"  y="131" class="gs-l" text-anchor="middle">1 µs</text>
  <text x="115" y="122" class="gs-l" text-anchor="middle">1 ms</text>
  <text x="165" y="86"  class="gs-l" text-anchor="middle">1 s</text>
  <text x="215" y="18"  class="gs-a" text-anchor="middle">17 min</text>
</svg>"""

PANEL = """
<section class="bonus" id="growth">
<header><span class="bonus-badge">bonus</span>
<h3>Growth rates &mdash; why some methods stop working</h3>
<span class="n">2 terms</span></header>
<p class="bonus-lede">All three courses say things like &ldquo;that does not scale&rdquo; and
&ldquo;about n&sup3;&rdquo; without ever showing what that means. It is not about speed. It is
about <b>shape</b>: how fast the work grows when the problem grows.</p>

<div class="bonus-grid">
  <div class="bonus-fig">%s
    <p class="cap">All three start in the same corner. That is the trap &mdash; on small data
    every method looks fine, and the difference only appears once the problem is big enough
    to matter.</p>
  </div>
  <div class="bonus-fig">%s
    <p class="cap">The same n&sup3; method at four sizes, at roughly a billion operations a
    second. Ten times the features is a <b>thousand</b> times the wait: one second becomes
    seventeen minutes.</p>
  </div>
</div>

<table class="gbig">
<thead><tr><th>growth</th><th>double the input and&hellip;</th><th>n = 1,000 costs</th><th>where it appears</th></tr></thead>
<tbody>
<tr><td class="f">O(1)</td><td>nothing changes</td><td class="f">1</td><td>looking up one array element</td></tr>
<tr><td class="f">O(n)</td><td>work doubles</td><td class="f">1,000</td><td>one pass over the data &mdash; a gradient descent step</td></tr>
<tr><td class="f">O(n&sup2;)</td><td>work &times; 4</td><td class="f">1,000,000</td><td>comparing every pair &mdash; distances between all points</td></tr>
<tr><td class="f">O(n&sup3;)</td><td>work &times; 8</td><td class="f">1,000,000,000</td><td>inverting a matrix &mdash; the normal equation</td></tr>
</tbody></table>

<div class="bonus-cols">
<div>
<h4>The two claims this explains</h4>
<ul class="bonus-list">
<li><b>&ldquo;Use gradient descent, not the closed form.&rdquo;</b> (C1 W2)
The normal equation inverts an n&times;n matrix &mdash; about <span class="f">n&sup3;</span> work in the
number of <i>features</i>. At 10,000 features that is roughly 17 minutes for one fit.
Gradient descent is about <span class="f">O(n)</span> per step.</li>
<li><b>&ldquo;Vectorize.&rdquo;</b> (C1 W2) This one is different, and worth being precise about:
vectorization does <b>not</b> change the growth rate. The loop and <code>np.dot</code> do the
same number of multiplications. It is a <b>constant-factor</b> win &mdash; often 10&ndash;100&times;
&mdash; from using the hardware properly. Both lines on the chart have the same shape; one is
simply far lower.</li>
</ul>
</div>
<div>
<h4>The shape of your data decides the cost</h4>
<p style="font-size:13.5px">A matrix multiply of <span class="f">(m, n)</span> by
<span class="f">(n, k)</span> costs about <span class="f">m &middot; n &middot; k</span>
multiply-adds. So a batch of 64 examples through a 1,000&rarr;500 layer is
<span class="f">64 &times; 1,000 &times; 500 = 32 million</span>.</p>
<p style="font-size:13.5px">That is why doubling the batch size doubles the cost, but doubling
the <i>width</i> of two adjacent layers quadruples it.</p>
</div>
</div>

<div class="bonus-trap"><span class="tag">The trap</span>
<p><b>Big-O throws away the constants, and sometimes the constants are what you care about.</b>
An O(n) method with a huge constant can lose to an O(n&nbsp;log&nbsp;n) method on every size you
will ever run. Big-O tells you what happens <i>eventually</i>; it does not tell you what is
faster today. Use it to spot the method that will fall off a cliff, then measure.</p>
</div>
<div class="scribble"><span class="lbl">&#9998; on paper</span>Draw axes and three curves from the same corner: nearly flat, bending up, and shooting off the page. Label them O(n), O(n&sup2;), O(n&sup3;). Then write four rows down the side &mdash; 10, 100, 1000, 10000 &mdash; and the n&sup3; value beside each. Ring the last one and write <i>17 minutes</i>.</div>
</section>
""" % (SVG_CURVES, SVG_BARS)
