#!/usr/bin/env python3
"""Static builder for the ML Specialization study site.

Content lives in content_<course><week>.py modules, each exporting WEEK.
Run:  python3 study/_build/build.py
"""
import glob
import html
import importlib
import kit
import json
import os
import re
import sys
from urllib.parse import quote as urlquote

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                      # study/
sys.path.insert(0, HERE)

# order matters: it defines the pagination chain
CARD_MODULES = ["cards_f0", "cards_c1", "cards_c2", "cards_c3"]
PLAIN_MODULES = ["cards_plain_f0", "cards_plain_c1", "cards_plain_c2", "cards_plain_c3"]

PROBLEM_MODULES = [
    "problems_f0w1", "problems_f0w2",
    "problems_c1w1", "problems_c1w2", "problems_c1w3",
    "problems_c2w1", "problems_c2w2", "problems_c2w3", "problems_c2w4",
    "problems_c3w1", "problems_c3w2", "problems_c3w3",
]

MODULES = [
    "content_f0w1", "content_f0w2",
    "content_c1w1", "content_c1w2", "content_c1w3",
    "content_c2w1", "content_c2w2", "content_c2w3", "content_c2w4",
    "content_c3w1", "content_c3w2", "content_c3w3",
]

COURSE_TITLE = {
    "F0": "Foundations",
    "C2": "Advanced Learning Algorithms",
    "C3": "Unsupervised Learning, Recommenders, RL",
    "C1": "Supervised Machine Learning",
}


# ---------------------------------------------------------------- glyph repair
# Some characters have no glyph in ANY font macOS ships, so they render as tofu
# boxes. Checked with fontTools against Iowan Old Style, Palatino, Georgia,
# Times New Roman, SF Pro and Menlo:
#
#   U+20D7  COMBINING RIGHT ARROW ABOVE  (the x-vector arrow)   missing in all 6
#   U+27FA  LONG LEFT RIGHT DOUBLE ARROW (also U+21D4 ⇔)        missing in all 6
#
# The combining circumflex, dot-above and macron ARE present everywhere, so
# ŷ, θ̇ and x̄ are left exactly as authored. Sources keep the readable character
# and it is translated here, at the moment the HTML is written — doing it in the
# sources would collide with Python's own string quoting.
MARKS = [
    ("\u20d7", "vec"),   # x⃗  vector
]
MARK_RE = re.compile("([A-Za-z])(" + "|".join(m for m, _ in MARKS) + ")")
_MARK_CLASS = {m: c for m, c in MARKS}


def fixmarks(text):
    """Replace unrenderable combining marks with CSS-drawn equivalents."""
    def sub(m):
        return '<span class="ov %s">%s</span>' % (_MARK_CLASS[m.group(2)], m.group(1))
    text = MARK_RE.sub(sub, text)
    # a <var> that now wraps only a span: collapse it so styling still applies
    text = re.sub(r'<var><span class="ov (\w+)">([A-Za-z])</span></var>',
                  r'<var class="ov \1">\2</var>', text)
    text = text.replace("\u27fa", "\u2194").replace("\u21d4", "\u2194")
    return text


def wr(path, text):
    """Every HTML page in this site is written through here."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(badge_api_calls(badge_terms(fixmarks(text))))


# ------------------------------------------------------------ refresher badges
# Things the specialization uses but never teaches. Each module exports
# TERMS (the floating notes), PATTERNS (what to badge) and PANEL (the bonus
# section). The first mention on a page gets a badge; the panels sit at the end
# of reference.html and symbols.html.
#
# content_f0ref and content_courseref are different in kind: their terms ARE
# taught on this site (F0, and C1-C3 itself respectively), so their badges
# link back to the specific lesson instead of a reference.html panel.
REFRESHER_MODULES = ["content_trig", "content_proj", "content_growth", "content_means",
                      "content_f0ref", "content_courseref"]

# content_apiref badges library CALLS (np.dot, model.fit, Dense(...)) rather
# than prose — it runs through badge_api_calls() below, scoped to the inside
# of <code> blocks, instead of through badge_terms(). Kept as its own list so
# the two passes can never accidentally badge each other's territory.
API_MODULES = ["content_apiref"]

# content_formulaparts is never auto-badged (empty PATTERNS) — its keys are
# only ever reached by an explicit eqp() call in a lesson, naming a part of
# ITS OWN formula. Still needs to land in window.GLOSS, hence its own list.
FORMULA_PART_MODULES = ["content_formulaparts"]


def _load_modules(names):
    mods = []
    for name in names:
        try:
            m = importlib.import_module(name)
        except ModuleNotFoundError:
            continue
        importlib.reload(m)
        mods.append(m)
    return mods


def _refreshers():
    return _load_modules(REFRESHER_MODULES)


def _build_patterns(mods):
    """[(compiled alternation, [keys])] — longest patterns first so
    "cosine similarity" beats "cos" and "weighted average" beats "average"."""
    pats = []
    for m in mods:
        pats.extend(getattr(m, "PATTERNS", []))
    pats.sort(key=lambda pk: -len(pk[0]))
    rx = re.compile("|".join("(?P<g%d>%s)" % (i, p) for i, (p, _k) in enumerate(pats)))
    return rx, [k for _p, k in pats]


def _patterns():
    return _build_patterns(_refreshers())


_TRIG_RE = None
_TRIG_KEY = None
# never badge inside these, and never inside a tag. aside is the lesson
# sidebar: every page's nav list of lesson titles (some of which literally
# contain "Σ" or "Π") would otherwise claim the page's one first-mention slot
# before the article body ever gets a look-in. "a" is any link: a badge
# nested inside link text fights the link's own click behaviour (the badge's
# click handler stops the click from bubbling, but never calls
# preventDefault, so a click there both opens the popup AND navigates).
SKIP_EL = re.compile(r"</?(code|pre|script|style|title|h1|option|textarea|aside|a)\b", re.I)


def badge_terms(html_text):
    """Wrap the first mention of each refresher term in a badge.

    Works on text between tags only, tracks whether we are inside an element
    where a badge would be wrong (code, headings, the bonus panel itself, or
    an eqp() formula's own part labels — those already carry their own
    gterm badges, authored directly by the formula, and re-scanning their
    text would double-badge it), and fires once per key per page so the
    result is a hint, not a rash.

    IMPORTANT history note: this used to bail out for the WHOLE page the
    moment any "gterm" string appeared anywhere in it — which meant any page
    using even one eqp() formula (99 of 172 lesson pages) got zero prose
    refresher badges at all, since eqp() emits its own gterm spans directly.
    Replaced with the depth-tracked "faneq" skip below, which excludes only
    the formula block itself and leaves the surrounding prose to be scanned
    normally.
    """
    global _TRIG_RE, _TRIG_KEY
    if _TRIG_RE is None:
        _TRIG_RE, _TRIG_KEY = _patterns()
    if not _TRIG_KEY:
        return html_text
    seen = set()
    depth = {"skip": 0, "bonus": 0, "topbar": 0, "faneq": 0}
    out = []
    pos = 0
    for m in re.finditer(r"<[^>]+>", html_text):
        text = html_text[pos:m.start()]
        tag = m.group(0)
        if text:
            if depth["skip"] or depth["bonus"] or depth["topbar"] or depth["faneq"] or len(seen) == len(set(_TRIG_KEY)):
                out.append(text)
            else:
                out.append(_badge_text(text, seen))
        out.append(tag)
        pos = m.end()
        low = tag.lower()
        if SKIP_EL.match(low):
            depth["skip"] += -1 if low.startswith("</") else 1
            depth["skip"] = max(0, depth["skip"])
        if 'class="bonus"' in low or "gpop" in low:
            depth["bonus"] += 1
        elif depth["bonus"] and low.startswith("</section"):
            depth["bonus"] = max(0, depth["bonus"] - 1)
        # the topbar crumb repeats the CURRENT page's own title on every page
        # (e.g. "Diagnosing bias and variance") — badging it would both steal
        # the first-mention slot and, worse, sometimes badge the wrong sense
        # of a word (ML "variance" in bias/variance vs. statistical variance).
        if 'class="topbar"' in low:
            depth["topbar"] += 1
        elif depth["topbar"] and low.startswith("</header"):
            depth["topbar"] = max(0, depth["topbar"] - 1)
        # an eqp() block is a <div class="fanat-eq..."> containing exactly one
        # nested <div class="fanat-row">...</div> (everything inside that is
        # spans). Track div depth from the moment we see the outer div so we
        # correctly exit after the one level of nesting, however it's spaced.
        if 'class="fanat-eq' in low:
            depth["faneq"] += 1
        elif depth["faneq"] and low.startswith("<div"):
            depth["faneq"] += 1
        elif depth["faneq"] and low.startswith("</div"):
            depth["faneq"] = max(0, depth["faneq"] - 1)
    tail = html_text[pos:]
    out.append(tail if (depth["skip"] or depth["bonus"] or depth["topbar"] or depth["faneq"]) else _badge_text(tail, seen))
    return "".join(out)


def _badge_text(text, seen):
    def sub(m):
        idx = next(i for i, g in enumerate(m.groups()) if g is not None)
        key = _TRIG_KEY[idx]
        if key in seen:
            return m.group(0)
        seen.add(key)
        return '<span class="gterm" data-g="%s">%s</span>' % (key, m.group(0))
    return _TRIG_RE.sub(sub, text)


_API_RE = None
_API_KEY = None
CODE_INNER = re.compile(r"(<code>)(.*?)(</code>)", re.S)


def badge_api_calls(html_text):
    """Wrap EVERY mention of a known library call — the mirror image of
    badge_terms(): this one works ONLY inside <code>...</code>, prose is left
    alone. Reuses the exact same .gterm/.gpop machinery, just a second,
    separately-scoped pass with its own pattern list (content_apiref.py).

    Unlike badge_terms()'s prose pass, this badges every occurrence, not just
    the first per page: a method you are trying to make second nature is
    worth re-explaining on hover at every encounter, and gloss.js attaches an
    independent listener per element, so repeated badges of the same key cost
    nothing and never conflict."""
    global _API_RE, _API_KEY
    if _API_RE is None:
        _API_RE, _API_KEY = _build_patterns(_load_modules(API_MODULES))
    if not _API_KEY or "<code>" not in html_text:
        return html_text

    def sub_text(text):
        def sub(m):
            idx = next(i for i, g in enumerate(m.groups()) if g is not None)
            key = _API_KEY[idx]
            return '<span class="gterm" data-g="%s">%s</span>' % (key, m.group(0))
        return _API_RE.sub(sub, text)

    def repl(m):
        out, pos = [], 0
        inner = m.group(2)
        for tm in re.finditer(r"<[^>]+>", inner):
            chunk = inner[pos:tm.start()]
            if chunk:
                out.append(sub_text(chunk))
            out.append(tm.group(0))
            pos = tm.end()
        out.append(sub_text(inner[pos:]))
        return m.group(1) + "".join(out) + m.group(3)

    return CODE_INNER.sub(repl, html_text)


MAPPAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Concept map</title>
<link rel="stylesheet" href="assets/base.css">
<link rel="stylesheet" href="assets/print.css" media="print">
<script src="assets/site.js"></script>
<script src="assets/search.js"></script>
<script>window.GLOSS_UP="";</script>
<script src="assets/gloss-data.js"></script>
<script src="assets/gloss.js"></script>
<script src="assets/meta.js"></script>
</head>
<body data-slug="__map__">
<header class="topbar">
  <button class="btn" id="menu-toggle" aria-label="menu">&#9776;</button>
  <a class="brand" href="index.html">ML<span>&#183;</span>notes</a>
  <span class="crumb">Concept map &#183; <b>what leans on what</b></span>
  <span class="spacer"></span>
  <button class="btn" id="search-btn" title="search  (/)">&#8981;</button>
  <button class="btn" id="theme-btn" title="theme">&#9689;</button>
</header>
<div class="layout">
<aside class="sidebar">
{sidebar}
</aside>
<main>
<p class="runhead"><span class="part">Apparatus</span><span class="d">&#183;</span><span class="ch">Concept map</span><span class="right">{n} lessons &#183; {e} links</span></p>
<h1>What leans on what</h1>
<p class="lede">Every lesson in the book, and every place one leans on another. The links are
not drawn by hand &mdash; a lesson that uses a cross-referenced term is joined to whichever lesson
<b>teaches</b> that term, so this map is generated from the text and cannot drift from it.</p>

<div class="mapwrap">
  <div class="maphead">
    <b>Drag to pan &#183; click a lesson</b>
    <span class="maplegend">
      <span><i data-p="I"></i>Foundations</span>
      <span><i data-p="II"></i>Supervised</span>
      <span><i data-p="III"></i>Neural nets</span>
      <span><i data-p="IV"></i>Unsup &#183; RL</span>
    </span>
    <span class="maplegend" id="map-prog-legend">
      <span><i class="pr-dim"></i>not yet read</span>
      <span><i class="pr-flat"></i>read</span>
      <span><i class="pr-ring"></i>mastered</span>
    </span>
    <button class="btn primary" id="map-progress" title="show what you have actually read and mastered" aria-pressed="true">my progress</button>
    <button class="btn" id="map-reset" title="reset view">reset</button>
  </div>
  <canvas id="conceptmap"></canvas>
  <div class="mapfoot" id="mapfoot">Reading order runs left to right. Bigger dots are leaned on
    by more lessons &mdash; those are the ones worth over-learning.</div>
</div>

<h2><span class="ico">&#128207;</span>The load-bearing lessons</h2>
<p>Counted, not guessed: these are the lessons the most other lessons depend on.</p>
<ol class="loadbearing" id="loadbearing"></ol>

<h2><span class="ico">&#129504;</span>Why a map at all</h2>
<p>A book is a line; understanding is not. Concept and knowledge maps are the one
well-evidenced study technique this site did not have &mdash; a meta-analysis in
<i>Review of Educational Research</i> found learners who work with them retain and transfer
more than those who read the equivalent text (Nesbit &amp; Adesope, 2006).</p>
<p>It answers what the linear book cannot: <b>everything &#931; touches</b>; <b>what has to be
solid before chapter 7</b>; <b>which ideas are load-bearing</b>. Click any lesson to see what it
leans on and what leans on it.</p>
<footer class="sitefoot">Study notes for the ML Specialization <span class="sep">&#183;</span> Hung Om</footer>
</main>
</div>
<script src="assets/mapdata.js"></script>
<script src="assets/map.js"></script>
</body>
</html>
"""


_CHAPTERS = None


def _chapters():
    """Chapter openers/closers, keyed by chapter number. Data lives beside the
    generator so it can be edited without touching build.py."""
    global _CHAPTERS
    if _CHAPTERS is None:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "content_chapters.json")
        try:
            _CHAPTERS = json.load(open(path, encoding="utf-8"))
        except Exception:
            _CHAPTERS = {}
    return _CHAPTERS


IDXPAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Index</title>
<link rel="stylesheet" href="assets/base.css">
<link rel="stylesheet" href="assets/print.css" media="print">
<script src="assets/site.js"></script>
<script src="assets/search.js"></script>
<script>window.GLOSS_UP="";</script>
<script src="assets/gloss-data.js"></script>
<script src="assets/gloss.js"></script>
</head>
<body data-slug="__bookindex__">
<header class="topbar">
  <button class="btn" id="menu-toggle" aria-label="menu">&#9776;</button>
  <a class="brand" href="index.html">ML<span>&#183;</span>notes</a>
  <span class="crumb">Index &#183; <b>every concept, and where it appears</b></span>
  <span class="spacer"></span>
  <button class="btn" id="search-btn" title="search  (/)">&#8981;</button>
  <button class="btn" id="theme-btn" title="theme">&#9689;</button>
</header>
<div class="layout">
<aside class="sidebar">
{sidebar}
</aside>
<main>
<p class="runhead"><span class="part">Apparatus</span><span class="d">&#183;</span><span class="ch">Index</span><span class="right">{n} entries</span></p>
<h1>Index</h1>
<p class="lede">Every cross-referenced concept and the sections it turns up in, the way a book's
back matter works. Generated from where the terms actually appear &mdash; so it records the text
rather than a list kept by hand. The <b>bold</b> section is where the idea is taught.</p>
<div class="bookidx">{body}</div>
<footer class="sitefoot">Study notes for the ML Specialization <span class="sep">&#183;</span> Hung Om</footer>
</main>
</div>
</body>
</html>
"""


def build_index_terms(weeks, flat):
    """The back-of-book index: concept -> the sections it appears in.

    Generated from where the cross-reference badges actually land, so it is a
    record of the text rather than a list someone maintained separately. A term
    that stops being used stops being indexed.
    """
    file_of = {rec["file"]: rec for rec in flat}
    labels, teaches = {}, {}
    for mod in _refreshers() + _load_modules(API_MODULES) + _load_modules(FORMULA_PART_MODULES):
        for t in getattr(mod, "TERMS", []):
            labels[t["key"]] = t["label"]
            href = (t.get("more_href") or "").split("#")[0]
            if href in file_of:
                teaches[t["key"]] = href

    where = {}
    for rec in flat:
        path = os.path.join(ROOT, rec["file"])
        if not os.path.exists(path):
            continue
        h = open(path, encoding="utf-8").read()
        body = h[h.find("<main"):]
        for key in set(re.findall(r'data-g="([a-zA-Z0-9-]+)"', body)):
            where.setdefault(key, []).append(rec)

    rows = []
    for key, recs in where.items():
        label = labels.get(key)
        if not label:
            continue
        recs = sorted(recs, key=lambda r: r["idx"])
        plain = re.sub(r"<[^>]+>", "", label).strip()
        # Group A-Z, and everything else — Greek, operators, np.* — under one
        # "Symbols" heading at the end. Python's isalpha() is True for Greek,
        # so Σ and λ would otherwise each get a heading of their own, and
        # symbols sorting either side of the ASCII letters produced THREE
        # separate "Symbols" groups.
        head = plain.lstrip("(").strip()[:1].upper()
        is_az = "A" <= head <= "Z"
        rows.append(((0 if is_az else 1, plain.lower()),
                     plain, key, recs, head if is_az else "Symbols"))
    rows.sort(key=lambda r: r[0])

    parts, letter = [], None
    for sort_key, plain, key, recs, first in rows:
        if first != letter:
            letter = first
            parts.append('<div class="ixletter">%s</div>' % html.escape(letter))
        home = teaches.get(key)
        secs = []
        for r in recs[:8]:
            bold = ' class="ix-home"' if r["file"] == home else ""
            secs.append('<a%s href="%s">%s</a>' % (bold, r["file"], r["sec"]))
        more = " …" if len(recs) > 8 else ""
        parts.append('<div class="ix"><span class="t">%s</span><span class="d"></span>'
                     '<span class="p">%s%s</span></div>'
                     % (html.escape(plain), ", ".join(secs), more))

    wr(os.path.join(ROOT, "book-index.html"),
       IDXPAGE.format(sidebar=sidebar(weeks, flat, "__bookindex__", 0),
                      n=len(rows), body="".join(parts)))
    return len(rows)


def build_map(weeks, flat):
    """The concept map: which lesson leans on which.

    Built from the cross-reference data the site already carries, not from a
    hand-drawn diagram — a lesson that badges a term gets an edge to whichever
    lesson TEACHES that term. So the graph cannot drift from the text: add a
    badge and the edge appears, remove one and it goes.

    Concept maps are the one well-evidenced technique this site was missing
    (Nesbit & Adesope 2006). The value is showing what a linear book cannot:
    which ideas are load-bearing, and what has to be solid before chapter N.
    """
    import content_f0ref, content_courseref, content_apiref, content_formulaparts
    file_of = {rec["file"]: rec for rec in flat}

    # term -> the lesson that teaches it
    teaches = {}
    for mod in _refreshers() + _load_modules(API_MODULES) + _load_modules(FORMULA_PART_MODULES):
        for t in getattr(mod, "TERMS", []):
            href = (t.get("more_href") or "").split("#")[0]
            if href in file_of:                      # lessons only, not reference.html
                teaches[t["key"]] = href

    nodes, index = [], {}
    for rec in flat:
        index[rec["file"]] = len(nodes)
        nodes.append({
            "f": rec["file"], "t": rec["L"]["title"], "sec": rec["sec"],
            "ch": rec["chapter"], "part": rec["part"],
        })

    seen, edges = set(), []
    for rec in flat:
        path = os.path.join(ROOT, rec["file"])
        if not os.path.exists(path):
            continue
        html_text = open(path, encoding="utf-8").read()
        body = html_text[html_text.find("<main"):]
        for key in sorted(set(re.findall(r'data-g="([a-zA-Z0-9-]+)"', body))):
            tgt = teaches.get(key)
            if not tgt or tgt == rec["file"]:
                continue
            pair = (index[rec["file"]], index[tgt])
            if pair not in seen:
                seen.add(pair)
                edges.append(list(pair))

    for a, b in edges:                                # how load-bearing each is
        nodes[b]["d"] = nodes[b].get("d", 0) + 1
    for n in nodes:
        n.setdefault("d", 0)

    with open(os.path.join(ROOT, "assets", "mapdata.js"), "w", encoding="utf-8") as f:
        f.write("/* generated by build.py — see build_map() */\n"
                "window.MAP = " + json.dumps({"nodes": nodes, "edges": edges},
                                             ensure_ascii=False, separators=(",", ":")) + ";\n")
    wr(os.path.join(ROOT, "map.html"),
       MAPPAGE.format(sidebar=sidebar(weeks, flat, "__map__", 0),
                      n=len(nodes), e=len(edges)))
    return len(nodes), len(edges)


def build_gloss():
    """window.GLOSS for the floating refresher cards."""
    data = {}
    for m in _refreshers() + _load_modules(API_MODULES) + _load_modules(FORMULA_PART_MODULES):
        anchor = getattr(m, "ANCHOR", "")
        for t in getattr(m, "TERMS", []):
            more_href = t.get("more_href") or ("reference.html#%s" % anchor)
            more_label = t.get("more_label") or "the whole refresher"
            data[t["key"]] = {"label": t["label"], "say": t["say"], "gist": t["gist"],
                              "body": t["body"], "ml": t["ml"],
                              "moreHref": more_href, "moreLabel": more_label}
    if not data:
        return 0
    with open(os.path.join(ROOT, "assets", "gloss-data.js"), "w", encoding="utf-8") as f:
        f.write("/* generated by build.py from _build/content_trig.py */\n"
                "window.GLOSS = " + json.dumps(data, ensure_ascii=False) + ";\n")
    return len(data)


def load_weeks():
    weeks = []
    for m in MODULES:
        try:
            mod = importlib.import_module(m)
        except ModuleNotFoundError:
            print("  (skipping %s — not written yet)" % m)
            continue
        importlib.reload(mod)
        weeks.append(mod.WEEK)
    return weeks


# ---------------------------------------------------------------- the book
# The book structure was always latent in the content — one part per course,
# one chapter per week, one numbered section per lesson. Naming it gives every
# lesson a stable address (§ 8.4) and a position in the whole (97 of 172),
# which a per-week "Lesson 4 of 17" cannot express.
PARTS = [
    ("F0", "I",   "Foundations"),
    ("C1", "II",  "Supervised Learning"),
    ("C2", "III", "Neural Networks & Practice"),
    ("C3", "IV",  "Unsupervised, Recommenders, RL"),
]
PART_OF = {c: (roman, title) for c, roman, title in PARTS}


def flatten(weeks):
    """Return a flat, ordered list of lesson records, numbered as a book."""
    flat = []
    chapter = 0
    for w in weeks:
        chapter += 1
        roman, part_title = PART_OF.get(w["course"], ("", ""))
        for i, L in enumerate(w["lessons"]):
            slug = "%s%s-%s" % (w["course"].lower(), w["week"], L["slug"])
            flat.append({
                "slug": slug,
                "file": "%s/w%s-%s.html" % (w["course"].lower(), w["week"], L["slug"]),
                "n": i + 1,
                "week": w,
                "L": L,
                # book coordinates
                "part": roman,
                "part_title": part_title,
                "chapter": chapter,
                "sec": "%d.%d" % (chapter, i + 1),
            })
    for k, rec in enumerate(flat):          # position in the whole book
        rec["idx"] = k + 1
        rec["of"] = len(flat)
    return flat


def sidebar(weeks, flat, current_slug, depth):
    up = "../" * depth
    out = []
    out.append('<a href="%sindex.html" style="font-weight:700">← Study plan</a>' % up)
    out.append('<a href="%smastery.html" style="font-weight:700">✓ Mastery plan</a>' % up)
    out.append('<a href="%sreview.html" style="font-weight:700">◆ Review (SRS)</a>' % up)
    out.append('<a href="%sproblems.html" style="font-weight:700">✎ Problem sets</a>' % up)
    out.append('<a href="%spaper.html" style="font-weight:700">✐ On paper</a>' % up)
    out.append('<a href="%sscratch.html" style="font-weight:700">⚙ From scratch</a>' % up)
    out.append('<a href="%slabs.html" style="font-weight:700;margin-bottom:10px">⌨ Lab companions</a>' % up)
    out.append('<a href="%sprogress.html" style="font-weight:700">▲ Progress</a>' % up)
    out.append('<a href="%sreference.html" style="font-weight:700">☰ Reference sheet</a>' % up)
    out.append('<a href="%ssymbols.html" style="font-weight:700">∑ Symbol glossary</a>' % up)
    out.append('<a href="%smap.html" style="font-weight:700">◈ Concept map</a>' % up)
    out.append('<a href="%sbook-index.html" style="font-weight:700;margin-bottom:10px">⌥ Index</a>' % up)
    for w in weeks:
        out.append('<h4>%s · W%s — %s</h4>' % (w["course"], w["week"], html.escape(w["title"])))
        for rec in flat:
            if rec["week"] is not w:
                continue
            cls = "here" if rec["slug"] == current_slug else ""
            out.append(
                '<a class="%s" data-slug-link="%s" href="%s%s"><span class="n">%02d</span>%s</a>'
                % (cls, rec["slug"], up, rec["file"], rec["n"], html.escape(rec["L"]["title"]))
            )
    return "\n".join(out)


PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · {course} W{week}</title>
<link rel="stylesheet" href="{up}assets/base.css">
<link rel="stylesheet" href="{up}assets/print.css" media="print">
<script src="{up}assets/site.js"></script>
<script src="{up}assets/search.js"></script>
<script>window.GLOSS_UP="{up}";</script>
<script src="{up}assets/gloss-data.js"></script>
<script src="{up}assets/gloss.js"></script>
<script src="{up}assets/reader.js"></script>
</head>
<body data-slug="{slug}">
<header class="topbar">
  <button class="btn" id="menu-toggle" aria-label="menu">☰</button>
  <a class="brand" href="{up}index.html">ML<span>·</span>notes</a>
  <span class="crumb">{course} · Week {week} · <b>{nav_title}</b></span>
  <span class="spacer"></span>
  <button class="btn" id="done-btn">mark done</button>
  <button class="btn" id="search-btn" title="search  (/)">&#8981;</button>
  <button class="btn" id="theme-btn" title="theme">◐</button>
</header>
<div class="layout">
<aside class="sidebar">
{sidebar}
</aside>
<main>
<p class="runhead"><span class="part">Part {part}</span><span class="d">·</span><span class="ch">Chapter {chapter} — {week_title}</span><span class="right">§&nbsp;{sec}{mins}</span></p>
<h1><span class="secno">{sec}</span>{title}</h1>
<p class="lede">{lede}</p>
<div class="bookrail" title="Lesson {idx} of {of_book} in the book"><i style="width:{pct}%"></i></div>
<p class="bookrail-cap"><span>{course} · Week {week} · lesson {n} of {of}</span><span class="r">{idx} of {of_book} · {pct}% of the book</span></p>
{body}
<nav class="pager">
{prev}
{next}
</nav>
<footer class="sitefoot">Study notes for the ML Specialization <span class="sep">·</span> Hung Om</footer>
</main>
</div>
<script src="{up}assets/meta.js"></script>
<script src="{up}assets/quiz.js"></script>
<script src="{up}assets/anim.js"></script>
<script src="{up}assets/{widgets}"></script>
</body>
</html>
"""

INDEX = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ML Specialization — study plan &amp; notes</title>
<link rel="stylesheet" href="assets/base.css">
<link rel="stylesheet" href="assets/print.css" media="print">
<script src="assets/site.js"></script>
<script src="assets/search.js"></script>
<script>window.GLOSS_UP="";</script>
<script src="assets/gloss-data.js"></script>
<script src="assets/gloss.js"></script>
</head>
<body data-slug="__index__">
<header class="topbar">
  <a class="brand" href="index.html">ML<span>·</span>notes</a>
  <span class="crumb">Study plan &amp; animated notes</span>
  <span class="spacer"></span>
  <button class="btn" id="reset-btn">reset progress</button>
  <button class="btn" id="search-btn" title="search  (/)">&#8981;</button>
  <button class="btn" id="theme-btn" title="theme">◐</button>
</header>
<div class="layout">
<aside class="sidebar">
{sidebar}
</aside>
<main>
{body}
<footer class="sitefoot">Study notes for the ML Specialization <span class="sep">·</span> Hung Om</footer>
</main>
</div>
<script src="assets/anim.js"></script>
<script src="assets/cover.js"></script>
</body>
</html>
"""



REVIEW = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Review — spaced repetition</title>
<link rel="stylesheet" href="assets/base.css">
<link rel="stylesheet" href="assets/print.css" media="print">
<script src="assets/site.js"></script>
<script src="assets/search.js"></script>
<script>window.GLOSS_UP="";</script>
<script src="assets/gloss-data.js"></script>
<script src="assets/gloss.js"></script>
</head>
<body data-slug="__review__">
<header class="topbar">
  <button class="btn" id="menu-toggle" aria-label="menu">&#9776;</button>
  <a class="brand" href="index.html">ML<span>&#183;</span>notes</a>
  <span class="crumb">Review &#183; <b>spaced repetition</b></span>
  <span class="spacer"></span>
  <a class="btn" href="reference.html">reference sheet</a>
  <button class="btn" id="search-btn" title="search  (/)">&#8981;</button>
  <button class="btn" id="theme-btn" title="theme">&#9689;</button>
</header>
<div class="layout">
<aside class="sidebar">
{sidebar}
</aside>
<main>
<p class="kicker">Spaced repetition &#183; {n} cards</p>
<h1>Review</h1>
<p class="lede">The notes are for understanding something the first time. This is for still knowing it in
six months. Cards you find easy come back rarely; cards you fumble come back tomorrow.</p>

<div class="srs-top">
  <div class="srs-stat due"><div class="k">due now</div><div class="v" id="c-due">0</div></div>
  <div class="srs-stat new"><div class="k">new</div><div class="v" id="c-new">0</div></div>
  <div class="srs-stat"><div class="k">scheduled</div><div class="v" id="c-later">0</div></div>
  <div class="srs-stat done"><div class="k">done today</div><div class="v" id="c-done">0</div></div>
  <div class="srs-stat"><div class="k">day streak</div><div class="v" id="c-streak">0</div></div>
</div>

<div class="filters">
  <div class="filter-row" id="f-course"></div>
  <div class="filter-row" id="f-week"></div>
  <div class="filter-row" id="f-kind"></div>
</div>

<div id="card-area"></div>
<div id="forecast"></div>
<div id="srs-stuck"></div>

<div class="srs-tools">
  <label>new cards per day <input type="number" id="srs-newperday" min="0" max="60" step="1"></label>
  <span class="spacer" style="flex:1"></span>
  <button class="btn" id="srs-export">export progress</button>
  <label class="btn" style="cursor:pointer">import<input type="file" id="srs-import" accept="application/json" hidden></label>
  <button class="btn" id="srs-reset">reset</button>
</div>

<h2><span class="ico">&#128276;</span>The 10 pm reminder</h2>
<p>A nightly alarm can be installed on this Mac so the review does not depend on remembering. It plays a
sound at 22:00, posts a notification, and opens this page.</p>
<pre><code>bash study/_build/install-alarm.sh          # install
bash study/_build/install-alarm.sh --status # check it
bash study/_build/install-alarm.sh --remove # uninstall</code></pre>

<h2><span class="ico">&#129504;</span>How the scheduling works</h2>
<p>An SM-2 variant, the same family of algorithm behind Anki. Each card carries an <b>interval</b>, an
<b>ease factor</b> and a <b>due date</b>.</p>
<ul>
<li><b>Again</b> — you had no idea. The card resets and comes back later in this same session.</li>
<li><b>Hard</b> — you got there, painfully. Short interval, and the ease factor drops.</li>
<li><b>Good</b> — normal recall. The interval multiplies by the ease factor (1 day, then 6, then ~15, ~38 &#8230;).</li>
<li><b>Easy</b> — instant. A longer jump, and the ease factor rises.</li>
</ul>
<p>Grade honestly. Marking a card Easy when you actually hesitated is the one way to make this stop
working &#8212; the whole method rests on the interval matching your real forgetting curve.</p>
<p style="color:var(--ink-faint);font-size:13.5px">Progress is stored in this browser only
(<code>localStorage</code>), never uploaded. Use <b>export</b> before clearing site data or switching
machines. Keyboard: <code>space</code> reveals, <code>1</code>&#8211;<code>4</code> grade.</p>
<footer class="sitefoot">Study notes for the ML Specialization <span class="sep">·</span> Hung Om</footer>
</main>
</div>
<script src="assets/deck.js"></script>
<script src="assets/srs.js"></script>
</body>
</html>
"""

REFERENCE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Reference sheet — every formula and algorithm</title>
<link rel="stylesheet" href="assets/base.css">
<link rel="stylesheet" href="assets/print.css" media="print">
<script src="assets/site.js"></script>
<script src="assets/search.js"></script>
<script>window.GLOSS_UP="";</script>
<script src="assets/gloss-data.js"></script>
<script src="assets/gloss.js"></script>
<script src="assets/print.js"></script>
</head>
<body data-slug="__reference__" data-printable="Reference sheet &#183; ML Specialization|{n} entries">
<header class="topbar">
  <button class="btn" id="menu-toggle" aria-label="menu">&#9776;</button>
  <a class="brand" href="index.html">ML<span>&#183;</span>notes</a>
  <span class="crumb">Reference &#183; <b>every formula and algorithm</b></span>
  <span class="spacer"></span>
  <a class="btn primary" href="review.html">review these</a>
  <button class="btn" id="search-btn" title="search  (/)">&#8981;</button>
  <button class="btn" id="theme-btn" title="theme">&#9689;</button>
</header>
<div class="layout">
<aside class="sidebar">
{sidebar}
</aside>
<main>
<p class="kicker">All three courses &#183; {n} entries</p>
<h1>Reference sheet</h1>
<div class="modebar" id="modebar">
  <span class="pl">Show</span>
  <button class="btn" data-mode="all">everything</button>
  <button class="btn" data-mode="plain">plain English only</button>
  <button class="btn" data-mode="formal">formulas only</button>
  <span class="ph">every symbol on this page is decoded in the entry that uses it</span>
</div>
<p class="lede">Every formula, algorithm and load-bearing concept from the whole specialization, grouped by
week, with both sides showing. This is the page to scan before an exam or an interview; the
<a href="review.html">review trainer</a> is the same material with the answers hidden and a schedule
attached.</p>
{body}
{bonus}
<script>
(function () {{
  var KEY = 'mls-ref-mode-v1', bar = document.getElementById('modebar');
  function set(m) {{
    document.body.classList.remove('refmode-plain', 'refmode-formal');
    if (m !== 'all') document.body.classList.add('refmode-' + m);
    bar.querySelectorAll('[data-mode]').forEach(function (b) {{
      b.classList.toggle('on', b.dataset.mode === m);
    }});
    try {{ localStorage.setItem(KEY, m); }} catch (e) {{ }}
  }}
  bar.addEventListener('click', function (e) {{
    var b = e.target.closest('[data-mode]');
    if (b) set(b.dataset.mode);
  }});
  var m = 'all';
  try {{ m = localStorage.getItem(KEY) || 'all'; }} catch (e) {{ }}
  set(m);
}})();
</script>
<hr>
<p style="color:var(--ink-faint);font-size:14px">Each entry links to the lesson it came from. Same content
as the spaced-repetition deck &#8212; if you fix a mistake here, fix it in
<code>study/_build/cards_c*.py</code> and rebuild.</p>
<footer class="sitefoot">Study notes for the ML Specialization <span class="sep">·</span> Hung Om</footer>
</main>
</div>
</body>
</html>
"""


def load_plain():
    """id -> beginner-friendly decode block."""
    p = {}
    for m in PLAIN_MODULES:
        try:
            mod = importlib.import_module(m)
        except ModuleNotFoundError:
            continue
        importlib.reload(mod)
        p.update(mod.P)
    return p


def load_cards():
    """Flatten all card decks, tagging each card with its course/week."""
    plains = load_plain()
    out = []
    for m in CARD_MODULES:
        try:
            mod = importlib.import_module(m)
        except ModuleNotFoundError:
            print("  (skipping %s — not written yet)" % m)
            continue
        importlib.reload(mod)
        for d in mod.DECKS:
            for c in d["cards"]:
                rec = dict(c)
                rec["course"] = d["course"]
                rec["week"] = "%sw%s" % (d["course"].lower(), d["week"])
                rec["weekNum"] = d["week"]
                rec["weekTitle"] = d["title"]
                rec["plain"] = plains.get(c["id"], "")
                for k in ("front", "back", "extra", "plain"):
                    rec[k] = fixmarks(rec.get(k) or "")
                out.append(rec)
    ids = [c["id"] for c in out]
    dupes = set(i for i in ids if ids.count(i) > 1)
    assert not dupes, "duplicate card ids: %s" % dupes
    gloss = _glossary()
    added = sum(enrich_plain(c, gloss) for c in out)
    if added:
        print("       (auto-decoded %d symbol(s) that a card used without explaining)" % added)
    nop = [c["id"] for c in out if not c["plain"]]
    if nop:
        print("  WARNING: %d card(s) have no plain-English block: %s"
              % (len(nop), ", ".join(nop[:8])))
    return out


# ---------------------------------------------------------- decode completeness
# A card that prints σ and never says what σ is has failed the one job this deck
# has for someone without a maths background. These are the symbols a beginner
# cannot guess; '·' and '×' are excluded because they read as "times" already.
OPAQUE = {
    "Σ": "sum of", "Π": "product of", "∂": "partial", "∇": "gradient",
    "√": "square root", "‖": "norm", "∈": "element of", "∞": "infinity",
    "≈": "approximately", "≤": "less than or equal", "≥": "greater than or equal",
    "≠": "not equal", "α": "alpha", "β": "beta", "γ": "gamma", "δ": "delta",
    "ε": "epsilon", "η": "eta", "θ": "theta", "λ": "lambda", "μ": "mu",
    "ρ": "rho", "σ": "sigma", "τ": "tau", "φ": "phi", "ω": "omega",
    "Δ": "delta", "Θ": "theta", "Λ": "lambda", "Φ": "phi", "Ω": "omega",
}
CODE_RE = re.compile(r"<code>.*?</code>", re.S)
ROW_RE = re.compile(r"<tbody>(.*?)</tbody>", re.S)


def _glossary():
    """symbol -> (how you say it, what it means), read from content_symbols."""
    import content_symbols
    importlib.reload(content_symbols)
    out = {}
    for _title, rows in content_symbols.GROUPS:
        for sym, say, mean, _code, _where in rows:
            key = strip_tags(sym)
            if key and key not in out:
                out[key] = (strip_tags(say), mean)
    return out


def enrich_plain(card, gloss):
    """Append a decode row for every opaque symbol the card uses but never explains.

    Returns the number of rows added. Code samples are ignored — `>=` inside a
    line of Python is not a symbol anyone needs decoding.
    """
    body = CODE_RE.sub(" ", (card.get("front") or "") + " " +
                            (card.get("back") or "") + " " + (card.get("extra") or ""))
    body = strip_tags(body)
    plain = card.get("plain") or ""
    plain_txt = strip_tags(plain)
    missing = []
    for sym, name in OPAQUE.items():
        if sym not in body:
            continue
        if sym in plain_txt or name in plain_txt.lower():
            continue
        entry = gloss.get(sym)
        if not entry:                       # try the fuller glossary form, e.g. ‖x‖
            for k, v in gloss.items():
                if sym in k:
                    entry = v
                    break
        if entry:
            missing.append((sym, entry[0], entry[1]))
    if not missing:
        return 0

    rows = "".join('<tr><td class="sy">%s</td><td class="sa">%s</td><td>%s</td></tr>'
                   % (sym, say, mean) for sym, say, mean in missing)
    if '<table class="cdec">' in plain:
        card["plain"] = ROW_RE.sub(lambda m: "<tbody>" + m.group(1) + rows + "</tbody>",
                                   plain, count=1)
    else:
        table = ('<table class="cdec"><thead><tr><th>symbol</th><th>say it</th>'
                 '<th>what it means</th></tr></thead><tbody>%s</tbody></table>' % rows)
        if plain:
            card["plain"] = plain.replace("</div>", table + "</div>", 1) if plain.endswith("</div>") \
                else plain + table
        else:
            card["plain"] = ('<div class="cplain">'
                             '<span class="cplain-tag">In plain English</span>%s</div>' % table)
    return len(missing)


def build_review(weeks, flat, cards):
    with open(os.path.join(ROOT, "assets", "deck.js"), "w", encoding="utf-8") as f:
        f.write("/* generated by build.py — edit cards in _build/cards_c*.py */\n")
        f.write("window.DECK = " + json.dumps(cards, ensure_ascii=False) + ";\n")
    wr(os.path.join(ROOT, "review.html"),
       REVIEW.format(sidebar=sidebar(weeks, flat, "__review__", 0), n=len(cards)))


def build_reference(weeks, flat, cards):
    by_week = []
    for c in cards:
        if not by_week or by_week[-1][0] != c["week"]:
            by_week.append((c["week"], c["course"], c["weekNum"], c["weekTitle"], []))
        by_week[-1][4].append(c)
    parts = []
    for wk, course, num, title, items in by_week:
        rows = []
        for c in items:
            rows.append(
                '<div class="ref-item"><div class="q">'
                '<span class="srs-kind k-%s">%s</span><span>%s</span></div>'
                '<div class="a"><div class="formal">%s%s</div>%s%s'
                '<a class="srs-lesson" href="%s">&#8599; lesson</a></div></div>'
                % (c["kind"], c["kind"], c["front"], c["back"], c["extra"],
                   c["plain"],
                   code_for(c) +
                   (('<div class="scribble"><span class="lbl">&#9998; on paper</span>%s</div>'
                     % scribble_for(c)) if scribble_for(c) else ""),
                   c["lesson"]))
        parts.append(
            '<section class="ref-week"><header><h3>%s &#183; Week %s &mdash; %s</h3>'
            '<span class="n">%d entries</span></header>%s</section>'
            % (course, num, html.escape(title), len(items), "".join(rows)))
    bonus = "".join(getattr(m, "PANEL", "") for m in _refreshers())
    wr(os.path.join(ROOT, "reference.html"),
       REFERENCE.format(sidebar=sidebar(weeks, flat, "__reference__", 0),
                        n=len(cards), body="\n".join(parts), bonus=bonus))



SYMBOLS = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Symbol glossary</title>
<link rel="stylesheet" href="assets/base.css">
<link rel="stylesheet" href="assets/print.css" media="print">
<script src="assets/site.js"></script>
<script src="assets/search.js"></script>
<script>window.GLOSS_UP="";</script>
<script src="assets/gloss-data.js"></script>
<script src="assets/gloss.js"></script>
<script src="assets/print.js"></script>
</head>
<body data-slug="__symbols__" data-printable="Symbol glossary &#183; ML Specialization|{n} symbols">
<header class="topbar">
  <button class="btn" id="menu-toggle" aria-label="menu">&#9776;</button>
  <a class="brand" href="index.html">ML<span>&#183;</span>notes</a>
  <span class="crumb">Glossary &#183; <b>every symbol, and its code equivalent</b></span>
  <span class="spacer"></span>
  <a class="btn" href="reference.html">reference sheet</a>
  <button class="btn" id="search-btn" title="search  (/)">&#8981;</button>
  <button class="btn" id="theme-btn" title="theme">&#9689;</button>
</header>
<div class="layout">
<aside class="sidebar">
{sidebar}
</aside>
<main>
<p class="kicker">{n} symbols and terms</p>
<h1>Symbol glossary</h1>
<p class="lede">Every symbol you will meet across the three courses, with how to <b>say it out loud</b>,
what it actually means, and the <b>NumPy equivalent</b>. Most of what makes maths feel impenetrable is not
knowing how to pronounce it &#8212; so that column is not a joke.</p>
<p class="sym-filter"><input type="search" id="symfilter" placeholder="filter — try “sigma”, “axis”, “gradient”…"
   style="width:100%;padding:10px 14px;font:inherit;border:1px solid var(--line);
          border-radius:var(--radius-sm);background:var(--bg-panel);color:var(--ink)"></p>
{body}
{bonus}
<hr>
<p style="color:var(--ink-faint);font-size:14px">If a symbol here is still opaque, the
<a href="f0/w1-03-greek-letters.html">Foundations lesson on Greek letters</a> says each one out loud, and
the <a href="f0/w1-01-what-is-a-function.html">maths lane</a> works through the ideas behind them.</p>
<footer class="sitefoot">Study notes for the ML Specialization <span class="sep">·</span> Hung Om</footer>
</main>
</div>
<script>
(function () {{
  var box = document.getElementById('symfilter');
  if (!box) return;
  box.addEventListener('input', function () {{
    var q = box.value.trim().toLowerCase();
    document.querySelectorAll('tr[data-row]').forEach(function (tr) {{
      tr.style.display = (!q || tr.dataset.row.indexOf(q) >= 0) ? '' : 'none';
    }});
    document.querySelectorAll('section[data-grp]').forEach(function (sec) {{
      var any = Array.prototype.some.call(sec.querySelectorAll('tr[data-row]'),
        function (tr) {{ return tr.style.display !== 'none'; }});
      sec.style.display = any ? '' : 'none';
    }});
  }});
}})();
</script>
</body>
</html>
"""


def build_symbols(weeks, flat):
    import content_symbols
    importlib.reload(content_symbols)
    parts, n = [], 0
    for title, rows in content_symbols.GROUPS:
        body = []
        for sym, say, mean, codev, where in rows:
            n += 1
            # the filter key must hold real characters, not entity text, or
            # typing the symbol itself would never match
            key = html.unescape(" ".join([sym, say, mean, codev, where])).lower()
            key = re.sub(r"<[^>]+>", " ", key)
            # combining marks (e.g. x + U+20D7) get turned into a <span> by
            # fixmarks() later on every page — including inside this attribute,
            # which would tear it open. Strip them here; the plain letter still
            # matches a search for "vector".
            for mark, _cls in MARKS:
                key = key.replace(mark, "")
            body.append(
                '<tr data-row="%s"><td class="sy">%s</td><td class="sa">%s</td><td>%s</td>'
                '<td><code>%s</code></td><td class="wh">%s</td></tr>'
                % (html.escape(key, quote=True), sym, say, mean, html.escape(codev), where))
        parts.append(
            '<section class="ref-week" data-grp="1"><header><h3>%s</h3>'
            '<span class="n">%d</span></header>'
            '<table class="symtab"><thead><tr><th>symbol</th><th>say it</th>'
            '<th>what it means</th><th>in code</th><th>where</th></tr></thead>'
            '<tbody>%s</tbody></table></section>' % (html.escape(title), len(rows), "".join(body)))
    bonus = "".join(getattr(m, "PANEL", "") for m in _refreshers())
    wr(os.path.join(ROOT, "symbols.html"),
       SYMBOLS.format(sidebar=sidebar(weeks, flat, "__symbols__", 0),
                      n=n, body="\n".join(parts), bonus=bonus))
    return n


TAGRE = re.compile(r"<[^>]+>")
WSRE = re.compile(r"\s+")


def strip_tags(h):
    """Plain text for the search index.

    Combining marks are dropped rather than converted: this text is rendered
    through esc(), so a <span> would be escaped and shown as literal markup.
    Searching for "x" still finds the vector.
    """
    h = re.sub(r"<(script|style|canvas)[^>]*>.*?</\1>", " ", h, flags=re.S | re.I)
    t = html.unescape(TAGRE.sub(" ", h))
    t = t.replace("\u20d7", "").replace("\u27fa", "\u2194").replace("\u21d4", "\u2194")
    return WSRE.sub(" ", t).strip()


def tag_quiz(body, slug):
    """Give every <details class="q"> a stable id: <slug>#<n>.
    Ids are positional, so inserting a question mid-lesson renumbers the ones
    after it — append new questions at the end of a quiz() block."""
    n = [0]

    def sub(m):
        n[0] += 1
        return '<details class="q" data-qid="%s#%d">' % (slug, n[0])
    out = re.sub(r'<details class="q">', sub, body)
    return out, n[0]


def build_meta(weeks, flat, cards, qcount):
    """Everything the client-side pages need to know about the site.

    This carries all SIX lanes, not just lessons — the dashboard and the mastery
    checklist both need to say what has been finished in each of them, and a
    problem's grade has to be traceable back to the lesson it came from.
    """
    by_lesson = {}
    for c in cards:
        by_lesson.setdefault(c["lesson"], []).append(c["id"])

    # problems: the pid -> lesson map is what lets a missed problem reach the
    # weak-spot list, and the week map is what lets mastery count them
    problems, problem_lesson, problems_by_week = [], {}, {}
    for mname in PROBLEM_MODULES:
        try:
            mod = importlib.import_module(mname)
        except ModuleNotFoundError:
            continue
        S = mod.SET
        key = "%s%s" % (S["course"].lower(), S["week"])
        problems.append({"s": "prob-" + key, "f": "problems/%s.html" % key,
                         "c": S["course"], "w": S["week"], "t": S["title"],
                         "n": len(S["problems"])})
        problems_by_week[key] = [p["pid"] for p in S["problems"]]
        for pr in S["problems"]:
            problem_lesson[pr["pid"]] = pr["lesson"]

    scratch = []
    try:
        import scratch_meta
        importlib.reload(scratch_meta)
        for i, d in enumerate(scratch_meta.LANE, 1):
            scratch.append({"s": "scratch-" + d["slug"], "f": "scratch/%s.html" % d["slug"],
                            "t": d["title"], "n": i})
    except ModuleNotFoundError:
        pass

    labs = []
    try:
        import labkit
        import lab_meta
        importlib.reload(labkit); importlib.reload(lab_meta)
        for nb in labkit.scan(os.path.dirname(ROOT)):
            a = lab_meta.LABS.get(nb["file"])
            if not a:
                continue
            slug = re.sub(r"[^a-z0-9]+", "-", os.path.splitext(nb["file"])[0].lower()).strip("-")
            labs.append({"s": "lab-" + slug, "f": "labs/%s.html" % slug,
                         "c": a["course"], "w": a["week"], "t": nb["title"][:70],
                         "k": a["kind"], "m": a["mins"]})
    except ModuleNotFoundError:
        pass

    meta = {
        "lessons": [{
            "f": r["file"], "s": r["slug"], "t": r["L"]["title"],
            "c": r["week"]["course"], "w": r["week"]["week"], "n": r["n"],
            "g": r["L"].get("tag", ""), "q": qcount.get(r["slug"], 0),
            "m": r["L"].get("mins", 10),
        } for r in flat],
        "weeks": [{"c": w["course"], "w": w["week"], "t": w["title"],
                   "n": len(w["lessons"])} for w in weeks],
        "cardsByLesson": by_lesson,
        "courseTitle": COURSE_TITLE,
        "problems": problems,
        "problemLesson": problem_lesson,
        "problemsByWeek": problems_by_week,
        "scratch": scratch,
        "labs": labs,
    }
    with open(os.path.join(ROOT, "assets", "meta.js"), "w", encoding="utf-8") as f:
        f.write("/* generated by build.py */\nwindow.META = "
                + json.dumps(meta, ensure_ascii=False, separators=(",", ":")) + ";\n")
    return sum(qcount.values())



PROGRESS = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Progress &#8212; what you know and what you don&#8217;t</title>
<link rel="stylesheet" href="assets/base.css">
<link rel="stylesheet" href="assets/print.css" media="print">
<script src="assets/site.js"></script>
<script src="assets/search.js"></script>
<script>window.GLOSS_UP="";</script>
<script src="assets/gloss-data.js"></script>
<script src="assets/gloss.js"></script>
</head>
<body data-slug="__progress__">
<header class="topbar">
  <button class="btn" id="menu-toggle" aria-label="menu">&#9776;</button>
  <a class="brand" href="index.html">ML<span>&#183;</span>notes</a>
  <span class="crumb">Progress &#183; <b>what you know and what you don&#8217;t</b></span>
  <span class="spacer"></span>
  <a class="btn primary" href="review.html">review now</a>
  <button class="btn" id="search-btn" title="search  (/)">&#8981;</button>
  <button class="btn" id="theme-btn" title="theme">&#9689;</button>
</header>
<div class="layout">
<aside class="sidebar">
{sidebar}
</aside>
<main>
<p class="kicker">{nl} lessons &#183; {nc} cards &#183; {nq} self-check questions</p>
<h1>Progress</h1>
<p class="lede">Everything here is computed in this browser from what you have actually done &#8212; lessons
marked done, cards graded, self-check questions answered. Nothing is uploaded anywhere. The section
that matters most is <a href="#weak">weak spots</a>: it is the one part of this site that tells you
something you did not already know about yourself.</p>

<div id="dash-top" class="tiles"></div>

<h2 id="byweek"><span class="ico">&#128202;</span>Week by week</h2>
<p>Three independent signals. <b>Lessons read</b> is just the &#8220;mark done&#8221; button. <b>Cards
sticking</b> counts cards whose review interval has reached 21 days &#8212; the usual line for
&#8220;this has moved into long-term memory&#8221;. <b>Self-check</b> is how you graded yourself on the
questions at the bottom of each lesson.</p>
<div id="dash-weeks"></div>

<h2 id="due"><span class="ico">&#128197;</span>What is coming</h2>
<p>Cards due over the next three weeks. Tall bars mean a heavy day &#8212; if one looks brutal, do a few
early rather than skipping the day.</p>
<div id="dash-forecast"></div>

<h2 id="weak"><span class="ico">&#127919;</span>Weak spots</h2>
<p>Ranked by two signals: self-check questions you marked <em>missed</em>, and cards you have forgotten
twice or more. Missing a question also pulls that lesson&#8217;s cards forward to tomorrow, so the
schedule reacts on its own.</p>
<div id="dash-weak"></div>

<h2 id="activity"><span class="ico">&#128293;</span>Review activity</h2>
<div id="dash-heat"></div>

<h2 id="export"><span class="ico">&#128190;</span>Take it with you</h2>
<div class="card">
<p><b>Anki export</b> &#8212; the whole deck as a tab-separated file, plain-English blocks included, tagged by
course and week. Review on your phone; the schedule there is Anki&#8217;s own, separate from this site&#8217;s.</p>
<p><b>Backup</b> &#8212; your schedule and progress live only in this browser&#8217;s storage. Clearing site data
wipes them. The JSON backup restores everything.</p>
<p style="display:flex;gap:8px;flex-wrap:wrap;align-items:center">
  <button class="btn primary" id="anki-btn">export for Anki</button>
  <button class="btn" id="json-btn">back up progress</button>
  <label class="btn" style="cursor:pointer">restore backup&#8230;
    <input type="file" id="restore-inp" accept="application/json,.json" style="display:none"></label>
  <span id="anki-msg" style="font-size:12.5px;color:var(--ink-faint)"></span>
</p>
</div>
<footer class="sitefoot">Study notes for the ML Specialization <span class="sep">·</span> Hung Om</footer>
</main>
</div>
<script src="assets/deck.js"></script>
<script src="assets/meta.js"></script>
<script src="assets/dash.js"></script>
</body>
</html>
"""


def build_progress(weeks, flat, cards, n_q):
    wr(os.path.join(ROOT, "progress.html"),
       PROGRESS.format(sidebar=sidebar(weeks, flat, "__progress__", 0),
                       nl=len(flat), nc=len(cards), nq=n_q))


PROBSET = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Problems &#183; {course} W{week}</title>
<link rel="stylesheet" href="../assets/base.css">
<link rel="stylesheet" href="../assets/print.css" media="print">
<script src="../assets/site.js"></script>
<script src="../assets/search.js"></script>
<script>window.GLOSS_UP="../";</script>
<script src="../assets/gloss-data.js"></script>
<script src="../assets/gloss.js"></script>
</head>
<body data-slug="prob-{course_l}{week}" data-printable="Problems &#183; {course} Week {week}|{n} problems">
<header class="topbar">
  <button class="btn" id="menu-toggle" aria-label="menu">&#9776;</button>
  <a class="brand" href="../index.html">ML<span>&#183;</span>notes</a>
  <span class="crumb">Problems &#183; {course} W{week} &#183; <b>{title}</b></span>
  <span class="spacer"></span>
  <button class="btn" id="done-btn">mark done</button>
  <button class="btn" id="search-btn" title="search  (/)">&#8981;</button>
  <button class="btn" id="theme-btn" title="theme">&#9689;</button>
</header>
<div class="layout">
<aside class="sidebar">
{sidebar}
</aside>
<main>
<p class="kicker">{course} &#183; Week {week} &#183; {n} problems &#183; {n1} warm-up &#183; {n2} core &#183; {n3} stretch</p>
<h1>Problems &mdash; {title}</h1>
<p class="lede">{lede}</p>
<div class="callout key"><span class="tag">How to use this page</span>
<p>Work each one on <b>paper, with the solution shut</b>. Open the hint only after you are
genuinely stuck, and the solution only after you have written something down &#8212; even a wrong
something. Reading a worked solution you have not attempted feels like learning and is not.</p>
<p>Then grade yourself honestly. A <b>missed</b> problem pulls that lesson&#8217;s review cards
forward to tomorrow and shows up in <a href="../progress.html">weak spots</a>.</p></div>
{body}
<nav class="pager">
{prev}
{next}
</nav>
<footer class="sitefoot">Study notes for the ML Specialization <span class="sep">·</span> Hung Om</footer>
</main>
</div>
<script src="../assets/meta.js"></script>
<script src="../assets/quiz.js"></script>
</body>
</html>
"""

PROBINDEX = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Problem sets</title>
<link rel="stylesheet" href="assets/base.css">
<link rel="stylesheet" href="assets/print.css" media="print">
<script src="assets/site.js"></script>
<script src="assets/search.js"></script>
<script>window.GLOSS_UP="";</script>
<script src="assets/gloss-data.js"></script>
<script src="assets/gloss.js"></script>
</head>
<body data-slug="__problems__">
<header class="topbar">
  <button class="btn" id="menu-toggle" aria-label="menu">&#9776;</button>
  <a class="brand" href="index.html">ML<span>&#183;</span>notes</a>
  <span class="crumb">Problems &#183; <b>{n} problems with full worked solutions</b></span>
  <span class="spacer"></span>
  <button class="btn" id="search-btn" title="search  (/)">&#8981;</button>
  <button class="btn" id="theme-btn" title="theme">&#9689;</button>
</header>
<div class="layout">
<aside class="sidebar">
{sidebar}
</aside>
<main>
<p class="kicker">{nw} sets &#183; {n} problems</p>
<h1>Problem sets</h1>
<p class="lede">Reading the notes trains recognition. These train production &#8212; a blank page
and a question. Every problem shows <b>every line of the working</b>, not just the answer, so a
solution you have to read is still a lesson.</p>
<div class="callout kid"><span class="tag">Why the problems are shuffled</span>
<p>Within a set the topics are mixed up rather than grouped. Practising one topic in a block
feels much better than it works: you stop having to decide <i>what kind of problem is this?</i>,
which is the part you must actually do when it counts. Mixed practice feels harder and sticks
better. That is not a mistake in the ordering.</p></div>
{body}
<footer class="sitefoot">Study notes for the ML Specialization <span class="sep">·</span> Hung Om</footer>
</main>
</div>
</body>
</html>
"""


def build_problems(weeks, flat):
    import problemkit
    importlib.reload(problemkit)
    sets = []
    for mname in PROBLEM_MODULES:
        try:
            mod = importlib.import_module(mname)
        except ModuleNotFoundError:
            continue
        importlib.reload(mod)
        sets.append(mod.SET)
    if not sets:
        return 0, 0

    files = ["problems/%s%s.html" % (S["course"].lower(), S["week"]) for S in sets]
    for i, S in enumerate(sets):
        body = "\n".join(problemkit.render(p, j + 1) for j, p in enumerate(S["problems"]))
        lv = [p["level"] for p in S["problems"]]
        prev = ('<a class="prev" href="../%s"><span class="dir">&#8249; previous</span>'
                '<span class="ttl">%s W%s problems</span></a>'
                % (files[i - 1], sets[i - 1]["course"], sets[i - 1]["week"])) if i else '<span class="ghost"></span>'
        nxt = ('<a class="next" href="../%s"><span class="dir">next &#8250;</span>'
               '<span class="ttl">%s W%s problems</span></a>'
               % (files[i + 1], sets[i + 1]["course"], sets[i + 1]["week"])) if i < len(sets) - 1 else '<span class="ghost"></span>'
        page = PROBSET.format(
            course=S["course"], course_l=S["course"].lower(), week=S["week"],
            title=html.escape(S["title"]), lede=S["lede"], n=len(S["problems"]),
            n1=lv.count(1), n2=lv.count(2), n3=lv.count(3),
            sidebar=sidebar(weeks, flat, "prob-%s%s" % (S["course"].lower(), S["week"]), 1),
            body=body, prev=prev, next=nxt)
        wr(os.path.join(ROOT, files[i]), page)

    total = sum(len(S["problems"]) for S in sets)
    rows = []
    for i, S in enumerate(sets):
        lv = [p["level"] for p in S["problems"]]
        tags = []
        for p in S["problems"]:
            if p["tag"] and p["tag"] not in tags:
                tags.append(p["tag"])
        rows.append(
            '<li><a data-slug-link="prob-%s%s" href="%s"><span class="n">%s W%s</span>'
            '<span class="pt"><b>%s</b><span class="pgs">%s</span></span>'
            '<span class="tag2">%d problems</span></a></li>'
            % (S["course"].lower(), S["week"], files[i], S["course"], S["week"],
               html.escape(S["title"]), html.escape(" · ".join(tags)), len(S["problems"])))
    body = ('<h2><span class="ico">&#9999;&#65039;</span>Every set, in course order</h2>'
            '<ol class="problist">%s</ol>' % "".join(rows))
    wr(os.path.join(ROOT, "problems.html"),
       PROBINDEX.format(sidebar=sidebar(weeks, flat, "__problems__", 0),
                        n=total, nw=len(sets), body=body))
    return len(sets), total


SCRATCHPAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>From scratch &#183; {title}</title>
<link rel="stylesheet" href="../assets/base.css">
<link rel="stylesheet" href="../assets/print.css" media="print">
<script src="../assets/site.js"></script>
<script src="../assets/search.js"></script>
<script>window.GLOSS_UP="../";</script>
<script src="../assets/gloss-data.js"></script>
<script src="../assets/gloss.js"></script>
</head>
<body data-slug="scratch-{slug}" data-printable="From scratch &#183; {title}|{nsec} steps">
<header class="topbar">
  <button class="btn" id="menu-toggle" aria-label="menu">&#9776;</button>
  <a class="brand" href="../index.html">ML<span>&#183;</span>notes</a>
  <span class="crumb">From scratch &#183; <b>{title}</b></span>
  <span class="spacer"></span>
  <button class="btn" id="done-btn">mark done</button>
  <button class="btn" id="search-btn" title="search  (/)">&#8981;</button>
  <button class="btn" id="theme-btn" title="theme">&#9689;</button>
</header>
<div class="layout">
<aside class="sidebar">
{sidebar}
</aside>
<main>
<p class="kicker">From scratch &#183; file {num} of {total} &#183; {nlines} lines of NumPy</p>
<h1>{title}</h1>
<p class="lede">{lede}</p>

<div class="runbox">
  <div class="rb-l">Run it yourself</div>
  <pre><code>cd study/scratch/code
python3 {file}</code></pre>
  <p>Pure NumPy &#8212; no scikit-learn, no TensorFlow. <b>Every code block below is read
  straight out of that file, and the output under it is what that exact block printed
  when this page was built.</b> They cannot drift apart.</p>
  <p class="rb-b">By the end you will have built {builds}.</p>
</div>

{body}

<h2><span class="ico">&#128218;</span>The lessons this rests on</h2>
{lessons}

<nav class="pager">
{prev}
{next}
</nav>
<footer class="sitefoot">Study notes for the ML Specialization <span class="sep">·</span> Hung Om</footer>
</main>
</div>
</body>
</html>
"""

SCRATCHINDEX = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Build it from scratch</title>
<link rel="stylesheet" href="assets/base.css">
<link rel="stylesheet" href="assets/print.css" media="print">
<script src="assets/site.js"></script>
<script src="assets/search.js"></script>
<script>window.GLOSS_UP="";</script>
<script src="assets/gloss-data.js"></script>
<script src="assets/gloss.js"></script>
</head>
<body data-slug="__scratch__">
<header class="topbar">
  <button class="btn" id="menu-toggle" aria-label="menu">&#9776;</button>
  <a class="brand" href="index.html">ML<span>&#183;</span>notes</a>
  <span class="crumb">From scratch &#183; <b>{total} algorithms in pure NumPy</b></span>
  <span class="spacer"></span>
  <button class="btn" id="search-btn" title="search  (/)">&#8981;</button>
  <button class="btn" id="theme-btn" title="theme">&#9689;</button>
</header>
<div class="layout">
<aside class="sidebar">
{sidebar}
</aside>
<main>
<p class="kicker">{total} runnable files &#183; {nlines} lines &#183; {nsec} annotated steps</p>
<h1>Build it from scratch</h1>
<p class="lede">Every algorithm in the specialization, implemented in pure NumPy with no
scikit-learn and no TensorFlow, then checked against something independent &#8212; a numerical
gradient, a closed-form solution, or the library's own answer. You do not really know
backpropagation until you have written the four lines that do it and watched the numbers match.</p>
<div class="callout key"><span class="tag">These files really run</span>
<p>They live in <code>study/scratch/code/</code> and you can run any of them right now with
<code>python3 &lt;file&gt;</code>. The code on each page is <b>read out of the file at build time</b>
and the output shown beneath each block is <b>what that block actually printed</b>. If a file
broke, the page would show the error instead.</p></div>
{body}
<footer class="sitefoot">Study notes for the ML Specialization <span class="sep">·</span> Hung Om</footer>
</main>
</div>
</body>
</html>
"""


def build_scratch(weeks, flat):
    try:
        import scratchkit
        import scratch_meta
    except ModuleNotFoundError:
        return 0, 0, 0
    importlib.reload(scratchkit)
    importlib.reload(scratch_meta)
    lane = scratch_meta.LANE
    code_dir = os.path.join(ROOT, "scratch", "code")
    files = ["scratch/%s.html" % d["slug"] for d in lane]
    total_lines = 0
    total_sec = 0
    failures = []

    for i, d in enumerate(lane):
        path = os.path.join(code_dir, d["file"])
        src_lines = len(open(path, encoding="utf-8").read().splitlines())
        total_lines += src_lines
        sections = scratchkit.run_sections(path)
        total_sec += len(sections)
        body = []
        for name, code, out, err in sections:
            if err:
                failures.append((d["file"], name, err))
            body.append(scratchkit.render_section(
                name, code, out, err, d["prose"].get(name, "")))
        lessons = "".join(
            '<li><a href="../%s">%s</a></li>' % (href, html.escape(t))
            for href, t in d["lessons"])
        prev = ('<a class="prev" href="../%s"><span class="dir">&#8249; previous</span>'
                '<span class="ttl">%s</span></a>' % (files[i - 1], html.escape(lane[i - 1]["title"]))
                ) if i else '<span class="ghost"></span>'
        nxt = ('<a class="next" href="../%s"><span class="dir">next &#8250;</span>'
               '<span class="ttl">%s</span></a>' % (files[i + 1], html.escape(lane[i + 1]["title"]))
               ) if i < len(lane) - 1 else '<span class="ghost"></span>'
        page = SCRATCHPAGE.format(
            title=html.escape(d["title"]), slug=d["slug"], lede=d["lede"],
            file=d["file"], builds=d["builds"], nlines=src_lines,
            num=i + 1, total=len(lane), nsec=len(sections),
            sidebar=sidebar(weeks, flat, "scratch-%s" % d["slug"], 1),
            body="\n".join(body),
            lessons='<ul class="links plain">%s</ul>' % lessons,
            prev=prev, next=nxt)
        wr(os.path.join(ROOT, files[i]), page)

    rows = []
    for i, d in enumerate(lane):
        rows.append(
            '<li><a data-slug-link="scratch-%s" href="%s"><span class="n">%02d</span>'
            '<span class="pt"><b>%s</b><span class="pgs">%s</span></span>'
            '<span class="tag2">%s</span></a></li>'
            % (d["slug"], files[i], i + 1, html.escape(d["title"]),
               html.escape(d["lede"][:118].rsplit(" ", 1)[0] + "\u2026"), d["file"]))
    body = ('<h2><span class="ico">&#128295;</span>The lane, in order</h2>'
            '<ol class="problist">%s</ol>' % "".join(rows))
    wr(os.path.join(ROOT, "scratch.html"),
       SCRATCHINDEX.format(sidebar=sidebar(weeks, flat, "__scratch__", 0),
                                    total=len(lane), nlines=total_lines,
                                    nsec=total_sec, body=body))
    if failures:
        print("  !! scratch code raised:")
        for fn, sec, e in failures:
            print("     %s [%s] %s" % (fn, sec, e))
    return len(lane), total_lines, total_sec


LABPAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Lab companion &#183; {title}</title>
<link rel="stylesheet" href="../assets/base.css">
<link rel="stylesheet" href="../assets/print.css" media="print">
<script src="../assets/site.js"></script>
<script src="../assets/search.js"></script>
<script>window.GLOSS_UP="../";</script>
<script src="../assets/gloss-data.js"></script>
<script src="../assets/gloss.js"></script>
</head>
<body data-slug="lab-{slug}" data-printable="Lab companion &#183; {title}|{course} Week {week}">
<header class="topbar">
  <button class="btn" id="menu-toggle" aria-label="menu">&#9776;</button>
  <a class="brand" href="../index.html">ML<span>&#183;</span>notes</a>
  <span class="crumb">Lab &#183; {course} W{week} &#183; <b>{title}</b></span>
  <span class="spacer"></span>
  <button class="btn" id="done-btn">mark done</button>
  <button class="btn" id="search-btn" title="search  (/)">&#8981;</button>
  <button class="btn" id="theme-btn" title="theme">&#9689;</button>
</header>
<div class="layout">
<aside class="sidebar">
{sidebar}
</aside>
<main>
<p class="kicker">{course} &#183; Week {week} &#183; <span class="labkind {kind}">{kind}</span> &#183; about {mins}</p>
<h1>{title}</h1>
<p class="lede">{blurb}</p>

<div class="runbox lab">
  <div class="rb-l">Open the notebook</div>
  <p><a href="{nbhref}"><code>{nbpath}</code></a></p>
  <p>{cells} cells &#8212; {ncode} code, {nmd} markdown.{exline}</p>
</div>

{watch}
{exercises}
<h2><span class="ico">&#128203;</span>What is in it, in order</h2>
<p>Read straight out of the notebook, so it is what you will actually see.</p>
{outline}
{funcs}
<h2><span class="ico">&#128218;</span>The lessons behind it</h2>
{lessons}

<nav class="pager">
{prev}
{next}
</nav>
<footer class="sitefoot">Study notes for the ML Specialization <span class="sep">·</span> Hung Om</footer>
</main>
</div>
</body>
</html>
"""

LABINDEX = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Lab companions</title>
<link rel="stylesheet" href="assets/base.css">
<link rel="stylesheet" href="assets/print.css" media="print">
<script src="assets/site.js"></script>
<script src="assets/search.js"></script>
<script>window.GLOSS_UP="";</script>
<script src="assets/gloss-data.js"></script>
<script src="assets/gloss.js"></script>
</head>
<body data-slug="__labs__">
<header class="topbar">
  <button class="btn" id="menu-toggle" aria-label="menu">&#9776;</button>
  <a class="brand" href="index.html">ML<span>&#183;</span>notes</a>
  <span class="crumb">Labs &#183; <b>all {n} notebooks in this repo</b></span>
  <span class="spacer"></span>
  <button class="btn" id="search-btn" title="search  (/)">&#8981;</button>
  <button class="btn" id="theme-btn" title="theme">&#9689;</button>
</header>
<div class="layout">
<aside class="sidebar">
{sidebar}
</aside>
<main>
<p class="kicker">{n} notebooks &#183; {g} graded &#183; {o} optional &#183; {ex} exercises</p>
<h1>Lab companions</h1>
<p class="lede">A companion page for every notebook in this repository: what it is really for,
which lessons it leans on, the one thing to watch, and &#8212; for graded assignments &#8212;
what each exercise asks, the maths behind it, the shapes involved and how it usually goes wrong.</p>
<div class="callout key"><span class="tag">No solutions here</span>
<p>The outline and the function list on each page are read out of the real <code>.ipynb</code>
at build time, so they cannot drift. But <b>the solution code for graded exercises is
deliberately never reproduced</b> &#8212; writing it is the entire point of the assignment.
What you get instead is the specification: what to return, in what shape, and which mistake
to expect.</p></div>
{body}
<footer class="sitefoot">Study notes for the ML Specialization <span class="sep">·</span> Hung Om</footer>
</main>
</div>
</body>
</html>
"""


def build_labs(weeks, flat):
    try:
        import labkit
        import lab_meta
    except ModuleNotFoundError:
        return 0, 0, 0
    importlib.reload(labkit)
    importlib.reload(lab_meta)
    repo = os.path.dirname(ROOT)
    found = labkit.scan(repo)
    ann = lab_meta.LABS
    labs = []
    for nb in found:
        a = ann.get(nb["file"])
        if not a:
            print("  (lab with no annotation: %s)" % nb["file"])
            continue
        rec = dict(nb)
        rec.update(a)
        rec["slug"] = re.sub(r"[^a-z0-9]+", "-",
                             os.path.splitext(nb["file"])[0].lower()).strip("-")
        rec["rel"] = os.path.relpath(nb["path"], repo)
        labs.append(rec)
    order = {"C1": 1, "C2": 2, "C3": 3}
    labs.sort(key=lambda r: (order.get(r["course"], 9), r["week"],
                             0 if r["kind"] == "graded" else 1, r["file"]))
    files = ["labs/%s.html" % r["slug"] for r in labs]

    n_ex = 0
    for i, r in enumerate(labs):
        n_ex += len(r.get("exercises", []))
        # outline, straight from the notebook
        if r["outline"]:
            items = []
            for level, text in r["outline"]:
                items.append('<li class="l%d">%s</li>' % (min(level, 4), html.escape(text)))
            outline = '<ul class="nboutline">%s</ul>' % "".join(items)
        else:
            outline = ('<p style="color:var(--ink-faint)">This notebook has no markdown '
                       'headings &#8212; it is short enough not to need them.</p>')
        if r["functions"]:
            fl = "".join('<li><code>%s(%s)</code></li>'
                         % (html.escape(n), html.escape(a)) for n, a in r["functions"][:14])
            funcs = ('<h2><span class="ico">&#128295;</span>Functions it defines</h2>'
                     '<ul class="nbfuncs">%s</ul>' % fl)
        else:
            funcs = ""
        watch = ('<div class="callout warn"><span class="tag">The one thing to watch</span>'
                 '<p>%s</p></div>' % r["watch"]) if r.get("watch") else ""

        exs = ""
        if r.get("exercises"):
            cards = []
            for e in r["exercises"]:
                cards.append(
                    '<article class="exc"><header><span class="en">Exercise %d</span>'
                    '<code>%s</code></header>'
                    '<dl><dt>What it asks</dt><dd>%s</dd>'
                    '<dt>The maths</dt><dd class="mth">%s</dd>'
                    '<dt>Shapes</dt><dd><code>%s</code></dd>'
                    '<dt>How it usually goes wrong</dt><dd class="trp">%s</dd></dl>'
                    '</article>' % (e["n"], html.escape(e["fn"]), e["asks"],
                                    e["maths"], html.escape(e["shape"]), e["trap"]))
            exs = ('<h2><span class="ico">&#9999;&#65039;</span>The %d exercises</h2>'
                   '<p>The specification only &#8212; no solution code. If you want to see a '
                   'working implementation of the same idea, the '
                   '<a href="../scratch.html">from-scratch lane</a> has one you can run.</p>'
                   '%s' % (len(r["exercises"]), "".join(cards)))

        lessons = "".join('<li><a href="../%s">%s</a></li>' % (href, html.escape(t))
                          for href, t in r["lessons"])
        exline = ("" if not r["exercises"]
                  else " <b>%d graded exercises</b> (UNQ_C%s)."
                       % (len(r["exercises"]),
                          ", UNQ_C".join(str(x) for x in r["exercises"])))
        prev = ('<a class="prev" href="../%s"><span class="dir">&#8249; previous</span>'
                '<span class="ttl">%s</span></a>' % (files[i - 1], html.escape(labs[i - 1]["title"][:52]))
                ) if i else '<span class="ghost"></span>'
        nxt = ('<a class="next" href="../%s"><span class="dir">next &#8250;</span>'
               '<span class="ttl">%s</span></a>' % (files[i + 1], html.escape(labs[i + 1]["title"][:52]))
               ) if i < len(labs) - 1 else '<span class="ghost"></span>'

        page = LABPAGE.format(
            title=html.escape(r["title"]), slug=r["slug"], course=r["course"],
            week=r["week"], kind=r["kind"], mins="%d min" % r["mins"] if r["mins"] < 60
            else "%.1f h" % (r["mins"] / 60), blurb=r["blurb"],
            nbhref="../../" + urlquote(r["rel"]), nbpath=html.escape(r["rel"]),
            cells=r["n_cells"], ncode=r["n_code"], nmd=r["n_md"], exline=exline,
            watch=watch, exercises=exs, outline=outline, funcs=funcs,
            lessons='<ul class="links plain">%s</ul>' % lessons,
            sidebar=sidebar(weeks, flat, "lab-%s" % r["slug"], 1),
            prev=prev, next=nxt)
        wr(os.path.join(ROOT, files[i]), page)

    groups = []
    for r, fn in zip(labs, files):
        key = (r["course"], r["week"])
        if not groups or groups[-1][0] != key:
            groups.append((key, []))
        groups[-1][1].append((r, fn))
    parts = []
    for (course, week), items in groups:
        rows = []
        for r, fn in items:
            badge = ('<span class="labkind graded">graded</span>' if r["kind"] == "graded"
                     else '<span class="labkind optional">optional</span>')
            rows.append(
                '<li><a data-slug-link="lab-%s" href="%s">%s'
                '<span class="pt"><b>%s</b><span class="pgs">%s</span></span>'
                '<span class="tag2">%d min</span></a></li>'
                % (r["slug"], fn, badge, html.escape(r["title"][:64]),
                   html.escape(r["blurb"][:104].rsplit(" ", 1)[0] + "\u2026"), r["mins"]))
        parts.append('<section class="plan-week"><header><h3>%s &#183; Week %s</h3>'
                     '<span class="meta">%d notebooks</span></header>'
                     '<ol class="problist labs">%s</ol></section>'
                     % (course, week, len(items), "".join(rows)))
    g = sum(1 for r in labs if r["kind"] == "graded")
    wr(os.path.join(ROOT, "labs.html"),
       LABINDEX.format(sidebar=sidebar(weeks, flat, "__labs__", 0),
                                n=len(labs), g=g, o=len(labs) - g, ex=n_ex,
                                body="\n".join(parts)))
    return len(labs), g, n_ex


PAPER = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Working it on paper</title>
<link rel="stylesheet" href="assets/base.css">
<link rel="stylesheet" href="assets/print.css" media="print">
<script src="assets/site.js"></script>
<script src="assets/search.js"></script>
<script>window.GLOSS_UP="";</script>
<script src="assets/gloss-data.js"></script>
<script src="assets/gloss.js"></script>
</head>
<body data-slug="__paper__" data-printable="Working it on paper|12 sheets, one per week">
<header class="topbar">
  <button class="btn" id="menu-toggle" aria-label="menu">&#9776;</button>
  <a class="brand" href="index.html">ML<span>&#183;</span>notes</a>
  <span class="crumb">Paper &#183; <b>what to scribble, and why it works</b></span>
  <span class="spacer"></span>
  <button class="btn" id="search-btn" title="search  (/)">&#8981;</button>
  <button class="btn" id="theme-btn" title="theme">&#9689;</button>
</header>
<div class="layout">
<aside class="sidebar">
{sidebar}
</aside>
<main>
<p class="kicker">12 sheets &#183; one per week &#183; {nitems} things to reproduce from memory</p>
<h1>Working it on paper</h1>
<p class="lede">You remember by drawing, so this page is the one that turns the rest of the
site into something your hand has done rather than something your eyes have passed over.
Every claim below is sourced, and the sources were checked before they were quoted.</p>
{method}

<h2><span class="ico">&#128196;</span>One sheet per week</h2>
<p>Each of these is a single page you should be able to fill from memory by the end of that
week. Not a summary to copy &mdash; a <b>target</b>. Draw the picture first, then hang
everything else off it.</p>
{sheets}

<h2><span class="ico">&#128218;</span>Where this comes from</h2>
<p>Study advice is mostly folklore. These are the results the advice above is actually
built on, with the papers, so you can check any of it.</p>
{refs}
<hr>
<p style="color:var(--ink-faint);font-size:14px">Every entry on the
<a href="reference.html">reference sheet</a> carries a <b>&#9998; on paper</b> line saying what to
draw for that one thing. The <a href="review.html">review trainer</a> handles the spacing between
sessions, which is the one part a study session cannot do for itself.</p>
<footer class="sitefoot">Study notes for the ML Specialization <span class="sep">·</span> Hung Om</footer>
</main>
</div>
</body>
</html>
"""


def build_paper(weeks, flat):
    try:
        import content_paper
    except ModuleNotFoundError:
        return 0
    importlib.reload(content_paper)
    sheets = []
    for sh in content_paper.SHEETS:
        items = "".join("<li>%s</li>" % i for i in sh["items"])
        sheets.append(
            '<section class="sheet"><header><span class="sh-n">%s W%s</span>'
            '<h3>%s</h3><span class="sh-c">%d things</span></header>'
            '<div class="sh-draw"><span class="lbl">draw this first</span>%s</div>'
            '<ul class="sh-list">%s</ul>'
            '<div class="sh-test"><span class="lbl">then close it and answer</span>%s</div>'
            '</section>'
            % (sh["c"], sh["w"], html.escape(sh["title"]), len(sh["items"]),
               sh["draw"], items, sh["test"]))
    refs = "".join(
        '<li><span class="rf-a">%s</span> <a href="%s" target="_blank" rel="noopener">%s</a>'
        '<span class="rf-d">%s</span></li>' % (a, url, t, d)
        for a, t, url, d in content_paper.REFS)
    wr(os.path.join(ROOT, "paper.html"),
       PAPER.format(sidebar=sidebar(weeks, flat, "__paper__", 0),
                    method=content_paper.METHOD,
                    sheets="\n".join(sheets),
                    refs='<ul class="reflist">%s</ul>' % refs,
                    nitems=sum(len(s["items"]) for s in content_paper.SHEETS)))
    return len(content_paper.SHEETS)


_CODE_CACHE = {}


def code_for(card):
    """The NumPy snippet for one entry, run at build time so the result shown
    is the result it produced. Cached — a snippet is executed once per build."""
    if not _CODE_CACHE:
        try:
            import codekit
            import content_code
            importlib.reload(codekit)
            importlib.reload(content_code)
        except ModuleNotFoundError:
            _CODE_CACHE["__none__"] = True
            return ""
        from kit import highlight
        fails = []
        for cid, src in content_code.CODE.items():
            src, out, err = codekit.run(src)
            if err:
                fails.append((cid, err))
            _CODE_CACHE[cid] = codekit.render(src, out, err, highlight)
        try:
            import vocabcheck
            importlib.reload(vocabcheck)
            outside = {cid: vocabcheck.offences(src)
                       for cid, src in content_code.CODE.items()
                       if vocabcheck.offences(src)}
            if outside:
                print("  !! %d snippet(s) use something the Foundations track never "
                      "teaches:" % len(outside))
                for cid, o in list(outside.items())[:6]:
                    print("     %s  %s" % (cid, ", ".join(o)))
        except ModuleNotFoundError:
            pass
        _CODE_CACHE["__fails__"] = fails
        if fails:
            print("  !! %d reference snippet(s) raised:" % len(fails))
            for cid, e in fails[:6]:
                print("     %s  %s" % (cid, e))
    return _CODE_CACHE.get(card["id"], "")


def scribble_for(card):
    """The '&#9998; on paper' line for one reference entry."""
    try:
        import content_paper
    except ModuleNotFoundError:
        return ""
    bespoke = content_paper.SCRIBBLE.get(card["id"])
    if bespoke:
        return bespoke
    return content_paper.BY_KIND.get(card["kind"], "")


MASTERY = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Mastery plan &#8212; what &#8220;done&#8221; means</title>
<link rel="stylesheet" href="assets/base.css">
<link rel="stylesheet" href="assets/print.css" media="print">
<script src="assets/site.js"></script>
<script src="assets/search.js"></script>
<script>window.GLOSS_UP="";</script>
<script src="assets/gloss-data.js"></script>
<script src="assets/gloss.js"></script>
</head>
<body data-slug="__mastery__" data-printable="Mastery plan|12 weeks, five conditions each">
<header class="topbar">
  <button class="btn" id="menu-toggle" aria-label="menu">&#9776;</button>
  <a class="brand" href="index.html">ML<span>&#183;</span>notes</a>
  <span class="crumb">Mastery &#183; <b>what &#8220;done&#8221; actually means</b></span>
  <span class="spacer"></span>
  <a class="btn" href="progress.html">progress</a>
  <button class="btn" id="search-btn" title="search  (/)">&#8981;</button>
  <button class="btn" id="theme-btn" title="theme">&#9689;</button>
</header>
<div class="layout">
<aside class="sidebar">
{sidebar}
</aside>
<main>
<p class="kicker">12 weeks &#183; five conditions each &#183; four of them checked for you</p>
<h1>Mastery plan</h1>
<p class="lede">The site had six lanes of material and no statement of when a week was finished.
This is that statement. Every condition below is something the site can measure from what you
have actually done &#8212; except the last one on each week, which is the one only you can
answer, and is deliberately last.</p>
<div id="mastery-head"></div>

<h2><span class="ico">&#128260;</span>The order to work in</h2>
{order}

<h2><span class="ico">&#9989;</span>What counts as done</h2>
{criteria}

<h2><span class="ico">&#9201;</span>What it costs</h2>
{budget}
{budget_table}

<h2><span class="ico">&#128202;</span>Week by week</h2>
<p>Ticks fill in as you work. Nothing here is stored anywhere but this browser.</p>
<div id="mastery-weeks"></div>
<hr>
<p style="color:var(--ink-faint);font-size:14px">The four measurable conditions come from your
own marking &#8212; they are as honest as you are. The
<a href="progress.html">progress dashboard</a> shows the same data from the other direction:
what you are getting wrong rather than what you have finished.</p>
<footer class="sitefoot">Study notes for the ML Specialization <span class="sep">·</span> Hung Om</footer>
</main>
</div>
<script src="assets/meta.js"></script>
<script>window.MASTERY_WEEKS = {weekdata};</script>
<script src="assets/mastery.js"></script>
</body>
</html>
"""


def build_mastery(weeks, flat, cards):
    try:
        import content_mastery
    except ModuleNotFoundError:
        return 0
    importlib.reload(content_mastery)

    # ---- the time budget, summed from the site's own per-item estimates ----
    lab_min = {}
    try:
        import labkit, lab_meta
        for nb in labkit.scan(os.path.dirname(ROOT)):
            a = lab_meta.LABS.get(nb["file"])
            if a:
                lab_min.setdefault("%s%s" % (a["course"].lower(), a["week"]), 0)
                lab_min["%s%s" % (a["course"].lower(), a["week"])] += a["mins"]
    except ModuleNotFoundError:
        pass
    prob_n = {}
    for mname in PROBLEM_MODULES:
        try:
            mod = importlib.import_module(mname)
        except ModuleNotFoundError:
            continue
        prob_n["%s%s" % (mod.SET["course"].lower(), mod.SET["week"])] = len(mod.SET["problems"])

    rows, tot = [], [0, 0, 0, 0]
    for w in weeks:
        key = "%s%s" % (w["course"].lower(), w["week"])
        read = sum(L.get("mins", 10) for L in w["lessons"])
        prob = prob_n.get(key, 0) * 6
        lab = lab_min.get(key, 0)
        scr = 25 if key in ("f02", "c11", "c12", "c13", "c21", "c22", "c24", "c31", "c32", "c33") else 0
        tot[0] += read; tot[1] += prob; tot[2] += lab; tot[3] += scr
        rows.append('<tr><td><b>%s W%s</b> %s</td><td class="num">%d</td><td class="num">%d</td>'
                    '<td class="num">%d</td><td class="num">%s</td><td class="num"><b>%.1f h</b></td></tr>'
                    % (w["course"], w["week"], html.escape(w["title"]), read, prob, lab,
                       scr or "&mdash;", (read + prob + lab + scr) / 60))
    grand = sum(tot)
    table = ('<table class="data"><thead><tr><th>week</th><th>read</th><th>problems</th>'
             '<th>labs</th><th>build</th><th>total</th></tr></thead><tbody>%s'
             '<tr class="tot"><td><b>everything</b></td><td class="num">%d</td>'
             '<td class="num">%d</td><td class="num">%d</td><td class="num">%d</td>'
             '<td class="num"><b>%.0f h</b></td></tr></tbody></table>'
             % ("".join(rows), tot[0], tot[1], tot[2], tot[3], grand / 60))

    wr(os.path.join(ROOT, "mastery.html"),
       MASTERY.format(sidebar=sidebar(weeks, flat, "__mastery__", 0),
                      order=content_mastery.ORDER,
                      criteria=content_mastery.CRITERIA_NOTE,
                      budget=content_mastery.BUDGET_NOTE,
                      budget_table=table,
                      weekdata=json.dumps(content_mastery.WEEKS, ensure_ascii=False)))
    return round(grand / 60)


def build_search(weeks, flat, cards):
    """One flat index over lessons, cards and symbols. Written as JS so it
    loads from file:// without fetch()."""
    import content_symbols
    idx = []
    for rec in flat:
        w, L = rec["week"], rec["L"]
        heads = [strip_tags(m) for m in re.findall(r"<h2[^>]*>(.*?)</h2>", L["body"], re.S)]
        text = strip_tags(L["body"])
        idx.append({
            "t": "lesson",
            "u": rec["file"],
            "ti": L["title"],
            "w": "%s W%s" % (w["course"], w["week"]),
            "s": strip_tags(L["lede"])[:190],
            "h": " · ".join(heads)[:260],
            "b": text[:1500].lower(),
        })
    for c in cards:
        idx.append({
            "t": "card",
            "u": "review.html",
            "ti": strip_tags(c["front"])[:120],
            "w": "%s W%s" % (c["course"], c["weekNum"]),
            "s": strip_tags(c["back"])[:190],
            "h": c["kind"],
            "b": strip_tags(c["back"] + " " + c["plain"])[:700].lower(),
        })
    for title, rows in content_symbols.GROUPS:
        for sym, say, mean, codev, where in rows:
            idx.append({
                "t": "symbol",
                "u": "symbols.html",
                "ti": strip_tags(sym) + "  —  " + strip_tags(say),
                "w": where,
                "s": strip_tags(mean)[:190],
                "h": codev,
                "b": (" ".join([strip_tags(sym), strip_tags(say), strip_tags(mean), codev])).lower(),
            })
    # problem sets
    for mname in PROBLEM_MODULES:
        try:
            mod = importlib.import_module(mname)
        except ModuleNotFoundError:
            continue
        S = mod.SET
        u = "problems/%s%s.html" % (S["course"].lower(), S["week"])
        for pr in S["problems"]:
            idx.append({
                "t": "problem", "u": u + "#" + pr["pid"],
                "ti": strip_tags(pr["ask"])[:110],
                "w": "%s W%s" % (S["course"], S["week"]),
                "s": strip_tags(pr["answer"])[:190],
                "h": pr["tag"],
                "b": strip_tags(" ".join([pr["ask"], pr["answer"], pr.get("why") or ""]))[:800].lower(),
            })
    # from-scratch sections
    try:
        import scratch_meta
        for d in scratch_meta.LANE:
            for sec, prose in d["prose"].items():
                idx.append({
                    "t": "scratch", "u": "scratch/%s.html#sx-%s" % (d["slug"], sec),
                    "ti": "%s — %s" % (d["title"], sec.replace("_", " ")),
                    "w": d["file"], "s": strip_tags(prose)[:190], "h": "numpy",
                    "b": strip_tags(d["lede"] + " " + prose)[:700].lower(),
                })
    except ModuleNotFoundError:
        pass
    # the refresher panels
    for _m in _refreshers():
        for t in getattr(_m, "TERMS", []):
            idx.append({
                "t": "refresher", "u": "reference.html#" + getattr(_m, "ANCHOR", "trig"),
                "ti": "%s — %s" % (t["label"], strip_tags(t["say"]).strip("“”")),
                "w": "bonus · " + getattr(_m, "TOPIC", "refresher"),
                "s": strip_tags(t["gist"])[:190],
                "h": "refresher",
                "b": strip_tags(" ".join([t["gist"], t["body"], t["ml"]]))[:800].lower(),
            })

    # lab companions
    try:
        import labkit
        import lab_meta
        repo = os.path.dirname(ROOT)
        for nb in labkit.scan(repo):
            a = lab_meta.LABS.get(nb["file"])
            if not a:
                continue
            slug = re.sub(r"[^a-z0-9]+", "-", os.path.splitext(nb["file"])[0].lower()).strip("-")
            idx.append({
                "t": "lab", "u": "labs/%s.html" % slug,
                "ti": nb["title"][:110],
                "w": "%s W%s · %s" % (a["course"], a["week"], a["kind"]),
                "s": strip_tags(a["blurb"])[:190],
                "h": " · ".join(n for n, _ in nb["functions"][:6]),
                "b": strip_tags(" ".join(
                    [a["blurb"], a.get("watch") or "", nb["file"]]
                    + ["unq_c%d" % e["n"] for e in a.get("exercises", [])]
                    + [t for _, t in nb["outline"]]
                    + [e["fn"] + " " + e["asks"] for e in a.get("exercises", [])]))[:1100].lower(),
            })
    except ModuleNotFoundError:
        pass

    out = os.path.join(ROOT, "assets", "search-index.js")
    with open(out, "w", encoding="utf-8") as f:
        f.write("/* generated by build.py */\nwindow.SEARCH_INDEX = "
                + json.dumps(idx, ensure_ascii=False, separators=(",", ":")) + ";\n")
    return len(idx), os.path.getsize(out)


def pager_link(rec, depth, direction):
    if rec is None:
        return '<span class="ghost"></span>'
    up = "../" * depth
    return ('<a class="%s" href="%s%s"><span class="dir">%s</span>'
            '<span class="ttl">%s</span></a>'
            % (direction, up, rec["file"],
               "‹ previous" if direction == "prev" else "next ›",
               html.escape(rec["L"]["title"])))


CODE_BLOCK = re.compile(r"<code>(.*?)</code>", re.S)
TORN = re.compile(r'<span <span|class="tok-[a-z]"&gt;|&lt;span class="tok-')


def check_code_blocks():
    """Fail loudly if syntax highlighting has torn its own markup open.

    This exact bug shipped once — 1,404 broken spans across 87 pages — because
    the highlighter ran several re.sub passes and a later one matched inside an
    earlier one's output. Cheap to check, so it is checked every build.
    """
    bad = []
    for path in sorted(glob.glob(os.path.join(ROOT, "*.html")) +
                       glob.glob(os.path.join(ROOT, "*", "*.html"))):
        h = open(path, encoding="utf-8").read()
        for m in CODE_BLOCK.finditer(h):
            if TORN.search(m.group(1)):
                bad.append(os.path.relpath(path, ROOT))
                break
    return bad


def build():
    weeks = load_weeks()
    flat = flatten(weeks)
    n_pages = 0
    qcount = {}
    for i, rec in enumerate(flat):
        w, L = rec["week"], rec["L"]
        depth = 1  # every lesson lives one directory deep
        up = "../" * depth
        prev = flat[i - 1] if i > 0 else None
        nxt = flat[i + 1] if i < len(flat) - 1 else None
        week_len = len(w["lessons"])
        mins = " · %s min read" % L["mins"] if L.get("mins") else ""
        body_html = L["body"]
        if w["course"] == "F0":
            try:
                import content_paper as _cp
                prompt = _cp.FOUNDATION.get(L["slug"])
            except ModuleNotFoundError:
                prompt = None
            if prompt:
                body_html += (
                    '<h2 id="on-paper"><span class="ico">&#9998;</span>Put it on paper</h2>'
                    '<p>You remember this by drawing it, not by reading it. Shut this page '
                    'first, try it from memory, and only then look back and fix what is wrong '
                    '&mdash; the correcting is the part that sticks. '
                    '<a href="../paper.html">Why this works &#8594;</a></p>'
                    '<div class="scribble"><span class="lbl">&#9998; on paper</span>%s</div>'
                    % prompt)
        # chapter openers and closers — the joins between chapters, which are
        # otherwise silent because every lesson is self-contained
        ch = _chapters().get(str(rec["chapter"]))
        if ch:
            if rec["n"] == 1:
                body_html = (kit.chapter_open(ch["rests"], ch["able"], ch["leads"], ch["hook"])
                             + body_html)
            if rec["n"] == week_len:
                body_html += kit.chapter_close(ch["q"])
        body_html, nq = tag_quiz(body_html, rec["slug"])
        qcount[rec["slug"]] = nq
        page = PAGE.format(
            title=html.escape(L["title"]),
            nav_title=html.escape(L["title"]),
            course=w["course"], week=w["week"], slug=rec["slug"],
            n=rec["n"], of=week_len, mins=mins,
            part=rec["part"], chapter=rec["chapter"], sec=rec["sec"],
            week_title=html.escape(w["title"]),
            idx=rec["idx"], of_book=rec["of"],
            pct=round(rec["idx"] / rec["of"] * 100),
            lede=L["lede"], body=body_html,
            sidebar=sidebar(weeks, flat, rec["slug"], depth),
            prev=pager_link(prev, depth, "prev"),
            next=pager_link(nxt, depth, "next"),
            up=up,
            widgets="w-%s%s.js" % (w["course"].lower(), "w%s" % w["week"]),
        )
        wr(os.path.join(ROOT, rec["file"]), page)
        n_pages += 1

    # ---- review + reference ----
    cards = load_cards()
    build_review(weeks, flat, cards)
    build_reference(weeks, flat, cards)
    n_sym = build_symbols(weeks, flat)
    n_mn, n_me = build_map(weeks, flat)
    n_ix = build_index_terms(weeks, flat)
    if _CODE_CACHE and not _CODE_CACHE.get("__none__"):
        print("       + %d NumPy snippets on the reference sheet (all executed)"
              % sum(1 for k in _CODE_CACHE if not k.startswith("__")))
    n_gloss = build_gloss()
    n_paper = build_paper(weeks, flat)
    n_sets, n_prob = build_problems(weeks, flat)
    n_sc, n_sl, n_ss = build_scratch(weeks, flat)
    n_lab, n_grad, n_ex = build_labs(weeks, flat)
    n_q = build_meta(weeks, flat, cards, qcount)
    build_progress(weeks, flat, cards, n_q)
    n_hours = build_mastery(weeks, flat, cards)
    n_idx, idx_bytes = build_search(weeks, flat, cards)

    # ---- index ----
    body = build_index_body(weeks, flat)
    wr(os.path.join(ROOT, "index.html"),
       INDEX.format(sidebar=sidebar(weeks, flat, "__index__", 0), body=body))
    torn = check_code_blocks()
    if torn:
        print("  !! BROKEN SYNTAX HIGHLIGHTING in %d page(s): %s"
              % (len(torn), ", ".join(torn[:6])))
    print("built %d lesson pages + index + review + reference  (%d weeks, %d cards)"
          % (n_pages, len(weeks), len(cards)))
    print("       + symbols.html (%d symbols)" % n_sym)
    print("       + search index (%d entries, %d KB)" % (n_idx, idx_bytes // 1024))
    print("       + meta.js (%d quiz questions tagged)" % n_q)
    if n_gloss:
        print("       + %d refresher terms with floating notes" % n_gloss)
    if n_paper:
        print("       + paper.html (%d week sheets)" % n_paper)
    if n_hours:
        print("       + mastery.html (12 weeks, ~%d h budgeted)" % n_hours)
    if n_sets:
        print("       + %d problem sets (%d problems)" % (n_sets, n_prob))
    if n_sc:
        print("       + %d from-scratch pages (%d lines run, %d sections)" % (n_sc, n_sl, n_ss))
    if n_lab:
        print("       + %d lab companions (%d graded, %d exercises)" % (n_lab, n_grad, n_ex))


def build_index_body(weeks, flat):
    import content_plan
    importlib.reload(content_plan)
    total = len(flat)
    total_min = sum(r["L"].get("mins", 10) for r in flat)
    parts = []
    parts.append(content_plan.HERO.format(total=total, hours=round(total_min / 60 + 0.4)))
    parts.append('<div class="card" style="display:flex;gap:16px;align-items:center;flex-wrap:wrap">'
                 '<div style="flex:1;min-width:200px"><div class="progressbar" id="pbar" data-total="%d"><i></i></div></div>'
                 '<b id="pcount" style="font-variant-numeric:tabular-nums">0 / %d</b>'
                 '<span style="color:var(--ink-faint);font-size:13px">lessons marked done (saved in this browser)</span>'
                 '</div>' % (total, total))
    parts.append(content_plan.PLAN)
    parts.append('<h2 id="lessons"><span class="ico">📚</span>Every lesson, in order</h2>')
    for w in weeks:
        rows = []
        for rec in flat:
            if rec["week"] is not w:
                continue
            L = rec["L"]
            rows.append(
                '<li><a data-slug-link="%s" href="%s"><span class="n">%02d</span>'
                '<span>%s</span><span class="tag2">%s</span></a></li>'
                % (rec["slug"], rec["file"], rec["n"], html.escape(L["title"]),
                   html.escape(L.get("tag", ""))))
        parts.append(
            '<section class="plan-week"><header><h3>%s · Week %s — %s</h3>'
            '<span class="meta">%d lessons · %s</span></header><ol>%s</ol></section>'
            % (w["course"], w["week"], html.escape(w["title"]), len(w["lessons"]),
               html.escape(w.get("time", "")), "".join(rows)))
    parts.append(content_plan.FOOT)
    return "\n".join(parts)


if __name__ == "__main__":
    build()
