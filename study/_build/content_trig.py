# -*- coding: utf-8 -*-
"""Trigonometry refresher.

The specialization never asks you to *do* trigonometry, but it quietly uses it:
cos θ sits in the geometric form of the dot product, cosine similarity is how
recommenders compare items, "tangent" turns up in every explanation of a
derivative, and the lunar lander reports its tilt in radians. None of that is
explained anywhere in the course.

TERMS feeds the little badges that appear beside the first mention of a term on
a page. PANEL is the fuller refresher that sits at the end of the reference
sheet and the symbol glossary.
"""

ANCHOR = "trig"
TOPIC = "trigonometry"

# what to badge on a page, longest first (the builder sorts by length too)
PATTERNS = [
    (r"cosine similarity", "cosine-similarity"),
    (r"Pythagoras", "pythagoras"),
    (r"hypotenuse", "hypotenuse"),
    (r"perpendicular", "perpendicular"),
    (r"orthogonal", "perpendicular"),
    (r"radians?", "radian"),
    (r"tangent", "tan"),
    (r"cos\s*&theta;|cos\s*\u03b8|\bcos\b", "cos"),
    (r"\bsin\b", "sin"),
    (r"\btan\b", "tan"),
    (r"\u03b8", "theta"),
]

# key, label shown in the badge popover, how to say it, the refresher itself
TERMS = [
 dict(key="cos", label="cos θ", say="“coz theta”",
      gist="How much two directions <b>point the same way</b>, as a number between "
           "−1 and 1.",
      body="<p>Draw a right-angled triangle. <b>cos</b> of an angle is the side "
           "<i>next to</i> the angle divided by the longest side:</p>"
           "<div class='gq'>cos θ = adjacent ÷ hypotenuse</div>"
           "<p>The only three values worth memorising:</p>"
           "<table class='gtab'><tr><td>cos 0°</td><td>= 1</td><td>same direction</td></tr>"
           "<tr><td>cos 90°</td><td>= 0</td><td>at right angles</td></tr>"
           "<tr><td>cos 180°</td><td>= −1</td><td>opposite directions</td></tr></table>",
      ml="This is why <b>a · b = ‖a‖‖b‖ cos θ</b> tells you about direction: the "
         "lengths are fixed, so the sign of the dot product is the sign of cos θ."),

 dict(key="sin", label="sin θ", say="“sine theta”",
      gist="The other ratio in a right-angled triangle — the side <b>across from</b> "
           "the angle over the longest side.",
      body="<div class='gq'>sin θ = opposite ÷ hypotenuse</div>"
           "<table class='gtab'><tr><td>sin 0°</td><td>= 0</td></tr>"
           "<tr><td>sin 90°</td><td>= 1</td></tr>"
           "<tr><td>sin 180°</td><td>= 0</td></tr></table>"
           "<p>sin and cos are the same wave, shifted: <b>sin θ = cos(90° − θ)</b>.</p>",
      ml="Rare in this course. It appears if you ever plot a circle or generate "
         "wave-shaped test data."),

 dict(key="tan", label="tan θ", say="“tan theta”",
      gist="The <b>slope</b> of a line, expressed as an angle.",
      body="<div class='gq'>tan θ = opposite ÷ adjacent = sin θ ÷ cos θ</div>"
           "<p>A line that rises 1 for every 1 across sits at 45°, and "
           "<b>tan 45° = 1</b>. So a slope of 1 <i>is</i> an angle of 45°.</p>",
      ml="Careful: a <b>tangent line</b> and the function <b>tan</b> are different "
         "things that share a name. In this course “tangent” almost always means "
         "the straight line that just touches a curve — the thing whose slope is "
         "the derivative."),

 dict(key="theta", label="θ", say="“theta”",
      gist="A Greek letter. In geometry it means <b>an angle</b>; in machine "
           "learning papers it usually means <b>all the parameters at once</b>.",
      body="<p>Two completely different jobs for one letter, and which one is "
           "meant is decided entirely by context:</p>"
           "<table class='gtab'>"
           "<tr><td>cos θ</td><td>θ is an <b>angle</b></td></tr>"
           "<tr><td>∇<sub>θ</sub>J(θ)</td><td>θ is <b>w and b bundled together</b></td></tr>"
           "<tr><td>θ, θ̇ (lunar lander)</td><td>tilt <b>angle</b>, and how fast it is changing</td></tr>"
           "</table>",
      ml="If θ sits next to cos, sin or tan it is an angle. Anywhere else in this "
         "specialization it is the parameters."),

 dict(key="radian", label="radians", say="“ray-dee-ans”",
      gist="Another way of measuring angles. Maths and code use them; degrees are "
           "for humans.",
      body="<div class='gq'>π radians = 180°&nbsp;&nbsp;·&nbsp;&nbsp;1 radian ≈ 57.3°</div>"
           "<table class='gtab'>"
           "<tr><td>0</td><td>= 0°</td></tr>"
           "<tr><td>π/2 ≈ 1.571</td><td>= 90°</td></tr>"
           "<tr><td>π ≈ 3.142</td><td>= 180°</td></tr>"
           "<tr><td>2π ≈ 6.283</td><td>= 360°, all the way round</td></tr></table>"
           "<p>Why they exist: in radians the maths of derivatives comes out clean, "
           "with no stray conversion factor.</p>",
      ml="<code>np.cos</code> and friends take <b>radians</b>, not degrees. Feeding "
         "them 90 gives you cos(90 radians), which is −0.448 and not what you meant. "
         "Convert with <code>np.deg2rad</code>."),

 dict(key="pythagoras", label="Pythagoras", say="“pie-THAG-or-as”",
      gist="In a right-angled triangle, the two short sides squared add up to the "
           "long side squared.",
      body="<div class='gq'>a² + b² = c²</div>"
           "<p>3 across and 4 up gives 3² + 4² = 9 + 16 = 25, and √25 = <b>5</b>.</p>",
      ml="This <i>is</i> the length of a vector, just written differently: "
         "<b>‖x‖ = √(x₁² + x₂² + …)</b>. Pythagoras with more terms."),

 dict(key="hypotenuse", label="hypotenuse", say="“hy-POT-en-use”",
      gist="The longest side of a right-angled triangle — the slanted one, opposite "
           "the square corner.",
      body="<p>The other two sides are named relative to whichever angle you are "
           "looking at: <b>opposite</b> (across from it) and <b>adjacent</b> "
           "(next to it).</p>",
      ml="A vector drawn as an arrow is the hypotenuse of a triangle made from its "
         "components, which is why its length uses Pythagoras."),

 dict(key="perpendicular", label="perpendicular", say="“per-pen-DIC-you-lar”",
      gist="At right angles — a perfect corner, 90°. <b>Orthogonal</b> is the same "
           "word, used when there are more than two dimensions.",
      body="<p>Because cos 90° = 0, two perpendicular vectors have a dot product of "
           "exactly <b>zero</b>:</p>"
           "<div class='gq'>a · b = ‖a‖‖b‖ × 0 = 0</div>"
           "<p>So “their dot product is 0” and “they are at right angles” are the "
           "same statement.</p>",
      ml="PCA's components are chosen to be perpendicular to each other, which is "
         "what makes each one carry information the others do not."),

 dict(key="cosine-similarity", label="cosine similarity", say="“co-sine similarity”",
      gist="A score from −1 to 1 for <b>how alike two things are in direction</b>, "
           "ignoring how big they are.",
      body="<div class='gq'>cos θ = (a · b) ÷ (‖a‖ ‖b‖)</div>"
           "<p>Dividing by both lengths cancels size out, leaving only direction.</p>"
           "<table class='gtab'><tr><td>1</td><td>identical taste</td></tr>"
           "<tr><td>0</td><td>unrelated</td></tr>"
           "<tr><td>−1</td><td>opposite taste</td></tr></table>",
      ml="Used to find related films from learned features. Preferred over plain "
         "distance because a user who rates everything highly should still count as "
         "similar to one who rates everything low — same direction, different size."),
]

# ---------------------------------------------------------------- bonus panel
SVG_TRI = """
<svg viewBox="0 0 260 150" class="gsvg" role="img" aria-label="a right-angled triangle with sides labelled">
  <polygon points="30,120 210,120 210,30" fill="var(--blue-soft)" stroke="var(--blue)" stroke-width="2"/>
  <path d="M198,120 L198,108 L210,108" fill="none" stroke="var(--blue)" stroke-width="1.6"/>
  <path d="M30,120 a26,26 0 0 1 26,-13" fill="none" stroke="var(--accent)" stroke-width="1.8"/>
  <text x="60" y="115" class="gs-a">θ</text>
  <text x="120" y="138" class="gs-l">adjacent</text>
  <text x="216" y="78" class="gs-l">opposite</text>
  <text x="100" y="66" class="gs-l" transform="rotate(-27 100 66)">hypotenuse</text>
</svg>"""

SVG_CIRCLE = """
<svg viewBox="0 0 200 200" class="gsvg" role="img" aria-label="the unit circle, showing cosine as the across distance and sine as the up distance">
  <circle cx="100" cy="100" r="70" fill="none" stroke="var(--line)" stroke-width="1.5"/>
  <line x1="20" y1="100" x2="180" y2="100" stroke="var(--line)" stroke-width="1"/>
  <line x1="100" y1="20" x2="100" y2="180" stroke="var(--line)" stroke-width="1"/>
  <line x1="100" y1="100" x2="149.5" y2="50.5" stroke="var(--accent)" stroke-width="2.4"/>
  <line x1="100" y1="100" x2="149.5" y2="100" stroke="var(--blue)" stroke-width="3"/>
  <line x1="149.5" y1="100" x2="149.5" y2="50.5" stroke="var(--green)" stroke-width="3"/>
  <circle cx="149.5" cy="50.5" r="4" fill="var(--accent)"/>
  <path d="M124,100 a24,24 0 0 0 7,-17" fill="none" stroke="var(--accent)" stroke-width="1.6"/>
  <text x="132" y="96" class="gs-a">θ</text>
  <text x="112" y="116" class="gs-b">cos θ</text>
  <text x="155" y="78" class="gs-g">sin θ</text>
</svg>"""

PANEL = """
<section class="bonus" id="trig">
<header><span class="bonus-badge">bonus</span>
<h3>The trigonometry you actually need</h3>
<span class="n">9 terms</span></header>
<p class="bonus-lede">This specialization never asks you to <i>do</i> trigonometry. It just
uses four or five facts and assumes you have them. Here they are, and nothing beyond them
is needed anywhere in the three courses.</p>

<div class="bonus-grid">
  <div class="bonus-fig">%s
    <p class="cap">Every trig word is a side of this triangle. The angle <b>θ</b> decides
    which side is called which: <b>opposite</b> is across from it, <b>adjacent</b> is
    beside it, and the <b>hypotenuse</b> is always the slanted one.</p>
  </div>
  <div class="bonus-fig">%s
    <p class="cap">The same three ratios on a circle of radius 1. Walk round the edge and
    <b>cos θ</b> is how far across you are, <b>sin θ</b> is how far up. That is the whole
    reason both stay between −1 and 1.</p>
  </div>
</div>

<table class="gbig">
<thead><tr><th>term</th><th>say it</th><th>the formula</th><th>what it gives you</th></tr></thead>
<tbody>
<tr><td>sin θ</td><td>sine theta</td><td class="f">opposite ÷ hypotenuse</td><td>how far <b>up</b></td></tr>
<tr><td>cos θ</td><td>coz theta</td><td class="f">adjacent ÷ hypotenuse</td><td>how far <b>across</b></td></tr>
<tr><td>tan θ</td><td>tan theta</td><td class="f">opposite ÷ adjacent = sin θ ÷ cos θ</td><td>the <b>slope</b></td></tr>
<tr><td>Pythagoras</td><td>pie-THAG-or-as</td><td class="f">a² + b² = c²</td><td>the <b>length</b> of the slanted side</td></tr>
<tr><td>radians</td><td>ray-dee-ans</td><td class="f">π radians = 180°</td><td>the units code expects</td></tr>
</tbody></table>

<div class="bonus-cols">
<div>
<h4>The five values worth knowing by heart</h4>
<table class="gbig small"><tbody>
<tr><td>cos 0°</td><td class="f">1</td><td>pointing the same way</td></tr>
<tr><td>cos 90°</td><td class="f">0</td><td>at right angles &mdash; <b>dot product is 0</b></td></tr>
<tr><td>cos 180°</td><td class="f">&minus;1</td><td>pointing opposite ways</td></tr>
<tr><td>sin 0°</td><td class="f">0</td><td>flat</td></tr>
<tr><td>tan 45°</td><td class="f">1</td><td>a slope of 1 is a 45&deg; line</td></tr>
</tbody></table>
</div>
<div>
<h4>Where it actually shows up</h4>
<ul class="bonus-list">
<li><b>The dot product.</b> <span class="f">a &middot; b = &#8214;a&#8214;&#8214;b&#8214; cos&nbsp;&theta;</span> &mdash;
the lengths are fixed, so the <i>sign</i> of the answer is the sign of cos&nbsp;&theta;.
Positive means roughly the same direction, zero means perpendicular, negative means opposed.</li>
<li><b>Cosine similarity</b> (C3 W2). <span class="f">(a &middot; b) &divide; (&#8214;a&#8214;&#8214;b&#8214;)</span>.
Dividing by both lengths cancels size out, so only direction is compared. That is why a user
who rates everything 5 still counts as similar to one who rates everything 2.</li>
<li><b>PCA</b> (C3 W2). Components are chosen <b>perpendicular</b> to each other, so each one
carries something the others do not.</li>
<li><b>Vector length.</b> Pythagoras with more terms:
<span class="f">&#8214;x&#8214; = &radic;(x&#8321;&sup2; + x&#8322;&sup2; + &hellip;)</span>.</li>
<li><b>The lunar lander</b> (C3 W3). Its tilt <span class="f">&theta;</span> and spin
<span class="f">&theta;&#775;</span> are reported in <b>radians</b>.</li>
</ul>
</div>
</div>

<div class="bonus-trap"><span class="tag">Two traps</span>
<p><b>“Tangent” means two different things.</b> The function <b>tan</b> is a ratio. A
<b>tangent line</b> is the straight line that just touches a curve &mdash; and that is what
the word means every time this course uses it, when explaining a derivative. They are
unrelated in practice.</p>
<p><b>NumPy works in radians.</b> <code>np.cos(90)</code> is not cos&nbsp;90&deg; &mdash; it is
cos of 90 <i>radians</i>, which is &minus;0.448. Use <code>np.cos(np.deg2rad(90))</code>,
which gives 0 as intended.</p>
</div>
<div class="scribble"><span class="lbl">&#9998; on paper</span>Draw one right-angled triangle. Label the angle &theta;, then name the three sides from <i>its</i> point of view. Write cos&nbsp;&theta; and sin&nbsp;&theta; as fractions of those sides. Then a circle of radius 1 with a point on it, and drop the two dashed lines to the axes &mdash; those two lengths are cos and sin. Finally write cos&nbsp;0&deg;, cos&nbsp;90&deg; and cos&nbsp;180&deg; with their values.</div>
</section>
""" % (SVG_TRI, SVG_CIRCLE)
