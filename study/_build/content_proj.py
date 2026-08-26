# -*- coding: utf-8 -*-
"""Projection — the idea PCA is built on and never explains.

C3 W2 says "Project: z = x · u" and moves on. Projecting is the one genuinely
visual idea in PCA: it is the shadow a point casts on a line. Without it, PCA is
a recipe you follow rather than a thing you understand.
"""

ANCHOR = "projection"
TOPIC = "projection and PCA"

PATTERNS = [
    (r"orthonormal", "orthonormal"),
    (r"unit vector", "unit-vector"),
    (r"projections?\b", "projection"),
    (r"\bproject(?:ing|ed|s)?\b(?=[^<]{0,26}\bonto\b)", "projection"),
    (r"\bbasis\b", "orthonormal"),
]

TERMS = [
 dict(key="projection", label="projection", say="“pro-JEC-shun”",
      gist="The <b>shadow</b> a point casts on a line. One number: how far along "
           "that line the shadow falls.",
      body="<p>Shine a light straight down onto a line. Where the point's shadow "
           "lands is its projection, and how far along the line that is, is the "
           "only number you keep:</p>"
           "<div class='gq'>z = x · u</div>"
           "<p>That is why the dot product turns up: dotting with a direction "
           "<b>u</b> measures how far along <b>u</b> you are. Everything "
           "perpendicular to <b>u</b> is thrown away — which is exactly what "
           "“reducing to one dimension” means.</p>",
      ml="This <i>is</i> PCA's last step. 50 features become 2 numbers because "
         "each point is projected onto 2 chosen directions."),

 dict(key="unit-vector", label="unit vector", say="“unit vector”",
      gist="An arrow of length exactly <b>1</b>. It carries a direction and no "
           "size.",
      body="<div class='gq'>‖u‖ = 1</div>"
           "<p>Make one by dividing any vector by its own length: "
           "<b>u = v ÷ ‖v‖</b>.</p>"
           "<p>Why it matters here: <b>x · u</b> only equals the projection "
           "distance when u has length 1. If u were twice as long, every answer "
           "would come out twice too big — the number would measure the "
           "direction's size as well as the point's position.</p>",
      ml="Principal components are always returned as unit vectors, which is why "
         "you can dot with them directly and read the answer as a distance."),

 dict(key="orthonormal", label="orthonormal", say="“or-tho-NORM-al”",
      gist="A set of directions that are all at <b>right angles</b> to each other "
           "and all of <b>length 1</b>. Two words squashed together: "
           "<i>ortho</i>gonal + <i>norm</i>alised.",
      body="<p>A <b>basis</b> is just a set of directions you measure everything "
           "against — north and east, say. An orthonormal basis is one where the "
           "directions do not overlap at all and each is one unit long.</p>"
           "<p>Because they are perpendicular, each direction measures something "
           "the others cannot see. No double counting.</p>"
           "<div class='gq'>e₁ = [1, 0], e₂ = [0, 1] → e₁ · e₂ = 0, ‖e₁‖ = 1</div><p>At right angles, and each of length 1. That is the whole definition, and it is why dotting with one gives a distance directly.</p>",
      ml="PCA returns an orthonormal basis. That is why the second component adds "
         "genuinely new information rather than repeating the first."),
]

SVG_PROJ = """
<svg viewBox="0 0 270 170" class="gsvg" role="img" aria-label="a point projected onto a direction line">
  <line x1="20" y1="140" x2="245" y2="40" stroke="var(--ink-faint)" stroke-width="1.6"/>
  <text x="228" y="34" class="gs-l">the direction u</text>
  <line x1="20" y1="140" x2="72" y2="117" stroke="var(--accent)" stroke-width="4"/>
  <polygon points="72,117 64,113 66,122" fill="var(--accent)"/>
  <text x="26" y="112" class="gs-a">u</text>
  <line x1="20" y1="140" x2="150" y2="35" stroke="var(--blue)" stroke-width="2.4"/>
  <circle cx="150" cy="35" r="5" fill="var(--blue)"/>
  <text x="156" y="30" class="gs-b">x</text>
  <line x1="150" y1="35" x2="121.5" y2="94.9" stroke="var(--ink-faint)" stroke-width="1.4" stroke-dasharray="4 3"/>
  <path d="M116,88 L110,91 L113,97" fill="none" stroke="var(--ink-faint)" stroke-width="1.3"/>
  <circle cx="121.5" cy="94.9" r="5" fill="var(--green)"/>
  <line x1="20" y1="140" x2="121.5" y2="94.9" stroke="var(--green)" stroke-width="3.4"/>
  <text x="52" y="136" class="gs-g">z = x · u</text>
</svg>"""

SVG_PCA = """
<svg viewBox="0 0 240 170" class="gsvg" role="img" aria-label="a tilted cloud of points with its two principal directions">
  <g fill="var(--blue)" opacity=".62">
    <circle cx="62" cy="118" r="3.4"/><circle cx="80" cy="108" r="3.4"/><circle cx="94" cy="104" r="3.4"/>
    <circle cx="108" cy="92" r="3.4"/><circle cx="120" cy="88" r="3.4"/><circle cx="134" cy="78" r="3.4"/>
    <circle cx="148" cy="72" r="3.4"/><circle cx="162" cy="60" r="3.4"/><circle cx="76" cy="122" r="3.4"/>
    <circle cx="100" cy="112" r="3.4"/><circle cx="126" cy="98" r="3.4"/><circle cx="152" cy="84" r="3.4"/>
    <circle cx="88" cy="96" r="3.4"/><circle cx="114" cy="80" r="3.4"/><circle cx="140" cy="66" r="3.4"/>
  </g>
  <line x1="52" y1="126" x2="176" y2="54" stroke="var(--accent)" stroke-width="3"/>
  <text x="150" y="46" class="gs-a">PC1 — most spread</text>
  <line x1="100" y1="76" x2="128" y2="124" stroke="var(--green)" stroke-width="2.4"/>
  <text x="112" y="140" class="gs-g">PC2</text>
  <path d="M104,84 L110,80 L114,87" fill="none" stroke="var(--ink-faint)" stroke-width="1.3"/>
</svg>"""

PANEL = """
<section class="bonus" id="projection">
<header><span class="bonus-badge">bonus</span>
<h3>Projection &mdash; the idea PCA rests on</h3>
<span class="n">3 terms</span></header>
<p class="bonus-lede">The PCA lesson says &ldquo;<b>project: z = x &middot; u</b>&rdquo; and moves on.
That one word is doing all the work, and it is the most visual idea in the whole course.</p>

<div class="bonus-grid">
  <div class="bonus-fig">%s
    <p class="cap">Shine a light straight down onto the line. The <b>shadow</b> of the point
    <b>x</b> is its projection, and the single number <b>z</b> is how far along the line that
    shadow falls. Everything at right angles to the line is discarded &mdash; and discarding
    it is the entire point.</p>
  </div>
  <div class="bonus-fig">%s
    <p class="cap">PCA picks the line to project onto: the direction the cloud is most spread
    along. <b>PC2</b> is chosen at right angles to <b>PC1</b>, so it measures something PC1
    cannot see. Keep PC1 only, and every point becomes one number.</p>
  </div>
</div>

<table class="gbig">
<thead><tr><th>term</th><th>say it</th><th>the formula</th><th>what it gives you</th></tr></thead>
<tbody>
<tr><td>projection</td><td>pro-JEC-shun</td><td class="f">z = x &middot; u</td><td>one number &mdash; how far along <b>u</b></td></tr>
<tr><td>unit vector</td><td>unit vector</td><td class="f">&#8214;u&#8214; = 1, &nbsp; u = v &divide; &#8214;v&#8214;</td><td>a direction with no size attached</td></tr>
<tr><td>reconstruct</td><td>&mdash;</td><td class="f">x &asymp; z &middot; u</td><td>back out again &mdash; not exact unless you kept every direction</td></tr>
<tr><td>orthonormal</td><td>or-tho-NORM-al</td><td class="f">u&#7522; &middot; u&#11388; = 0, &nbsp; &#8214;u&#7522;&#8214; = 1</td><td>directions that do not double-count</td></tr>
</tbody></table>

<div class="bonus-cols">
<div>
<h4>Why the dot product measures a shadow</h4>
<p style="font-size:13.5px">The geometric dot product is
<span class="f">x &middot; u = &#8214;x&#8214; &#8214;u&#8214; cos&nbsp;&theta;</span>. Make <b>u</b> a unit
vector and <span class="f">&#8214;u&#8214;</span> becomes 1, leaving
<span class="f">&#8214;x&#8214; cos&nbsp;&theta;</span> &mdash; which is exactly the adjacent side of
the right-angled triangle formed by dropping a perpendicular. The shadow.</p>
<p style="font-size:13.5px">So &ldquo;dot with a unit vector&rdquo; and &ldquo;measure the shadow&rdquo;
are the same instruction.</p>
</div>
<div>
<h4>Where it actually shows up</h4>
<ul class="bonus-list">
<li><b>PCA</b> (C3 W2). <span class="f">z = x &middot; u</span> for each component you keep.
50 features become 2 numbers you can plot.</li>
<li><b>Reconstruction error.</b> Project down and back up; what does not survive the round
trip is what you threw away.</li>
<li><b>Every neuron.</b> <span class="f">w &middot; x</span> is a projection too &mdash; it asks
&ldquo;how much of this input points along the direction I care about?&rdquo;</li>
</ul>
</div>
</div>

<div class="bonus-trap"><span class="tag">The trap</span>
<p><b>The direction must have length 1.</b> <span class="f">x &middot; u</span> is only a distance
when <span class="f">&#8214;u&#8214; = 1</span>. Use a direction of length 2 and every projection comes
out twice too large &mdash; the number would then be measuring the arrow you chose as well as the
point you are looking at. Libraries always hand back unit vectors, which is why this rarely
bites in practice and is baffling when it does.</p>
</div>
<div class="scribble"><span class="lbl">&#9998; on paper</span>Draw a line and a point off it. Drop a perpendicular from the point onto the line and mark the right angle. Thicken the bit of line from the origin to where it landed, and label it z. Write z&nbsp;=&nbsp;x&nbsp;&middot;&nbsp;u along it. Then write &#8214;u&#8214;&nbsp;=&nbsp;1 and circle it &mdash; that is the condition the whole thing depends on.</div>
</section>
""" % (SVG_PROJ, SVG_PCA)
