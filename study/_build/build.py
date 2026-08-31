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

# ---------------------------------------------------------------- hidden courses
# C4 (attention and transformers) was written alongside the specialization but
# is not part of it. Naming a course here drops it from every generated page —
# lessons, the plan, problems, cards, paper sheets, mastery rows, and the
# cross-links pointing into it — without touching a single source file. Empty
# the set and the whole course is back on the next build.
HIDDEN_COURSES = {"C4"}
_HIDDEN_DIRS = tuple("%s/" % c.lower() for c in sorted(HIDDEN_COURSES))


def shown(course):
    """False for a course this build is hiding."""
    return str(course).upper() not in HIDDEN_COURSES


def _shown_modules(names):
    """Drop content/card/problem modules belonging to a hidden course."""
    tags = tuple("_%s" % c.lower() for c in sorted(HIDDEN_COURSES))
    return [n for n in names if not any(t in n for t in tags)]


def shown_href(href):
    """False for a cross-link pointing into a hidden course's pages."""
    return not href.lstrip("./").startswith(_HIDDEN_DIRS)


# order matters: it defines the pagination chain
CARD_MODULES = _shown_modules(["cards_f0", "cards_c1", "cards_c2", "cards_c3", "cards_c4"])
PLAIN_MODULES = _shown_modules(["cards_plain_f0", "cards_plain_c1", "cards_plain_c2",
                                "cards_plain_c3", "cards_plain_c4"])

PROBLEM_MODULES = _shown_modules([
    "problems_f0w1", "problems_f0w2", "problems_f0w3",
    "problems_c1w1", "problems_c1w2", "problems_c1w3",
    "problems_c2w1", "problems_c2w2", "problems_c2w3", "problems_c2w4",
    "problems_c3w1", "problems_c3w2", "problems_c3w3",
    "problems_c4w1", "problems_c4w2", "problems_c4w3", "problems_c4w4",
])

# one mock quiz per graded week — C1-C3 only, since F0 has no official quiz
MOCK_MODULES = _shown_modules([
    "mock_c1w1", "mock_c1w2", "mock_c1w3",
    "mock_c2w1", "mock_c2w2", "mock_c2w3", "mock_c2w4",
    "mock_c3w1", "mock_c3w2", "mock_c3w3",
])

# one gist page per week — the whole week as a single connected picture. Same
# order as MODULES, and a week without a module here simply has no gist page yet.
GIST_MODULES = _shown_modules([
    "gist_f0w1", "gist_f0w2", "gist_f0w3",
    "gist_c1w1", "gist_c1w2", "gist_c1w3",
    "gist_c2w1", "gist_c2w2", "gist_c2w3", "gist_c2w4",
    "gist_c3w1", "gist_c3w2", "gist_c3w3",
    "gist_c4w1", "gist_c4w2", "gist_c4w3", "gist_c4w4",
])

MODULES = _shown_modules([
    "content_f0w1", "content_f0w2", "content_f0w3",
    "content_c1w1", "content_c1w2", "content_c1w3",
    "content_c2w1", "content_c2w2", "content_c2w3", "content_c2w4",
    "content_c3w1", "content_c3w2", "content_c3w3",
    "content_c4w1", "content_c4w2", "content_c4w3", "content_c4w4",
])

COURSE_TITLE = {
    "F0": "Foundations",
    "C4": "Attention and Transformers",
    "C2": "Advanced Learning Algorithms",
    "C3": "Unsupervised Learning, Recommenders, RL",
    "C1": "Supervised Machine Learning",
}
COURSE_TITLE = {c: t for c, t in COURSE_TITLE.items() if shown(c)}


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
# `button` joins this list for the same reason `option`, `textarea` and `a` are on
# it: a refresher badge inside a CONTROL is clickable and fights the control. The
# Active Mastery card headers are buttons, and a badge landed inside one.
SKIP_EL = re.compile(r"</?(code|pre|script|style|title|h1|option|textarea|aside|a|button)\b", re.I)


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
      <span><i data-p="V"></i>Transformers</span>
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
            more_href = t.get("more_href") or ""
            if not more_href or not shown_href(more_href):
                more_href = "reference.html#%s" % anchor
                more_label = "the whole refresher"
            else:
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
    ("C4", "V",   "Attention & Transformers"),
]
PARTS = [p for p in PARTS if shown(p[0])]
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
    out.append('<a href="%sgist.html" style="font-weight:700">◉ Week gists</a>' % up)
    out.append('<a href="%smastery.html" style="font-weight:700">✓ Mastery plan</a>' % up)
    out.append('<a href="%sreview.html" style="font-weight:700">◆ Review (SRS)</a>' % up)
    out.append('<a href="%sproblems.html" style="font-weight:700">✎ Problem sets</a>' % up)
    out.append('<a href="%squizzes.html" style="font-weight:700">◎ Mock quizzes</a>' % up)
    out.append('<a href="%spaper.html" style="font-weight:700">✐ On paper</a>' % up)
    out.append('<a href="%sscratch.html" style="font-weight:700">⚙ From scratch</a>' % up)
    out.append('<a href="%slabs.html" style="font-weight:700">⌨ Lab companions</a>' % up)
    out.append('<a href="%sdata.html" style="font-weight:700;margin-bottom:10px">⬇ Datasets</a>' % up)
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
<div class="rv-hero">
  <div class="rv-glow" aria-hidden="true"></div>
  <div class="rv-hero-in">
    <div class="rv-hero-txt">
      <span class="rv-kicker">Spaced repetition &#183; {n} cards</span>
      <h1 class="rv-title">Review</h1>
      <p class="rv-lede">The notes are for understanding something the first time. This is for
      still knowing it in six months. Cards you find easy come back rarely; cards you fumble
      come back tomorrow.</p>
      <button type="button" class="rv-start" id="srs-start">
        <span class="start-go">Start reviewing</span>
        <span class="start-badge"><b class="start-n">0</b><small class="start-l">cards ready now</small></span>
      </button>
    </div>
    <div class="rv-ring" role="img" aria-label="how much of this deck is scheduled rather than new">
      <svg viewBox="0 0 80 80" aria-hidden="true">
        <circle class="bg" cx="40" cy="40" r="34"/>
        <circle class="fg" id="srs-ring-fg" cx="40" cy="40" r="34"/>
      </svg>
      <span class="rv-ring-pc" id="srs-ring-pc">0%</span>
      <span class="rv-ring-l">learned</span>
    </div>
  </div>
</div>

<div class="rv-stats">
  <div class="rv-stat due"><span class="v" id="c-due">0</span><span class="k">due now</span></div>
  <div class="rv-stat new"><span class="v" id="c-new">0</span><span class="k">new</span></div>
  <div class="rv-stat"><span class="v" id="c-later">0</span><span class="k">scheduled</span></div>
  <div class="rv-stat done"><span class="v" id="c-done">0</span><span class="k">done today</span></div>
  <div class="rv-stat streak"><span class="v" id="c-streak">0</span><span class="k">day streak</span></div>
</div>

<details class="rv-filters">
  <summary><span>Filter the deck</span><span class="rv-fhint">course &middot; week &middot; kind</span></summary>
  <div class="filters">
    <div class="filter-row" id="f-course"></div>
    <div class="filter-row" id="f-week"></div>
    <div class="filter-row" id="f-kind"></div>
  </div>
</details>

<div id="srs-stuck"></div>
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
                   c["plain"] + walk_for(c),
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


def mock_lesson_map():
    """qid -> lesson file, for the dashboard's weak-spot list."""
    m = {}
    for mname in MOCK_MODULES:
        try:
            mod = importlib.import_module(mname)
        except ModuleNotFoundError:
            continue
        for q in mod.SET["questions"]:
            m[q["qid"]] = q["lesson"]
    return m


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
        "mockLesson": mock_lesson_map(),
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


GISTPAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The gist &#183; {course} W{week}</title>
<link rel="stylesheet" href="../assets/base.css">
<link rel="stylesheet" href="../assets/print.css" media="print">
<script src="../assets/site.js"></script>
<script src="../assets/search.js"></script>
<script>window.GLOSS_UP="../";</script>
<script src="../assets/gloss-data.js"></script>
<script src="../assets/gloss.js"></script>
<script src="../assets/reader.js"></script>
</head>
<body data-slug="gist-{course_l}{week}" data-printable="The gist &#183; {course} Week {week}|{title}">
<header class="topbar">
  <button class="btn" id="menu-toggle" aria-label="menu">&#9776;</button>
  <a class="brand" href="../index.html">ML<span>&#183;</span>notes</a>
  <span class="crumb">The gist &#183; {course} W{week} &#183; <b>{title}</b></span>
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
<p class="kicker">{course} &#183; Week {week} &#183; the whole week at once &#183; {mins} min</p>
<h1>The gist &mdash; {title}</h1>
<p class="lede">{lede}</p>
<div class="callout kid"><span class="tag">What this page is for</span>
<p>The {n} lesson pages for this week each teach <b>one</b> idea properly. That is the right shape
for meeting an idea and the wrong shape for seeing how the ideas join &mdash; so this page is only
the joins. Nothing here is new: if a claim on this page is not already in one of those lessons, it
is a bug.</p>
<p>Read it <b>after</b> the week for consolidation, or <b>before</b> it as a map you will
recognise on the way through. Both work; reading it <i>instead</i> of the week does not.</p></div>
{body}
{compresses}
<nav class="pager">
{prev}
{next}
</nav>
<footer class="sitefoot">Study notes for the ML Specialization <span class="sep">&#183;</span> Hung Om</footer>
</main>
</div>
<script src="../assets/meta.js"></script>
<script src="../assets/quiz.js"></script>
</body>
</html>
"""

GISTINDEX = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Week gists</title>
<link rel="stylesheet" href="assets/base.css">
<link rel="stylesheet" href="assets/print.css" media="print">
<script src="assets/site.js"></script>
<script src="assets/search.js"></script>
<script>window.GLOSS_UP="";</script>
<script src="assets/gloss-data.js"></script>
<script src="assets/gloss.js"></script>
</head>
<body data-slug="__gist__">
<header class="topbar">
  <button class="btn" id="menu-toggle" aria-label="menu">&#9776;</button>
  <a class="brand" href="index.html">ML<span>&#183;</span>notes</a>
  <span class="crumb">Week gists &#183; <b>one page per week, the whole thing at once</b></span>
  <span class="spacer"></span>
  <button class="btn" id="search-btn" title="search  (/)">&#8981;</button>
  <button class="btn" id="theme-btn" title="theme">&#9689;</button>
</header>
<div class="layout">
<aside class="sidebar">
{sidebar}
</aside>
<main>
<p class="kicker">{n} of {nw} weeks</p>
<h1>Week gists</h1>
<p class="lede">Each lesson in this site is self-contained, which is what makes it readable and
also what makes the <b>joins</b> invisible. One gist page per week draws the joins: the week as a
single picture, what carried over from last week, the pieces in the order they hand to each other,
and the same algorithm on numbers small enough to check by hand.</p>
<div class="callout key"><span class="tag">These add nothing new</span>
<p>A gist page is a compression of lessons you already have, not a replacement for them. It exists
because <b>knowing the shape of a week is a different skill from knowing its parts</b>, and the
lesson pages can only teach the parts.</p></div>
{body}
<footer class="sitefoot">Study notes for the ML Specialization <span class="sep">&#183;</span> Hung Om</footer>
</main>
</div>
</body>
</html>
"""


def _gists():
    """[GIST] for every week that has a gist module, in course order."""
    out = []
    for mname in GIST_MODULES:
        try:
            mod = importlib.import_module(mname)
        except ModuleNotFoundError:
            continue
        importlib.reload(mod)
        out.append(mod.GIST)
    return out


def build_gist(weeks, flat):
    """One page per week: the week as a single connected picture.

    The page body is authored; the closing "what this compresses" block is
    DERIVED from the week's own lesson records, so a renamed or reordered
    lesson cannot leave a stale link behind on the gist page.
    """
    import scratchkit  # noqa: F401  (only to fail early if the lane is broken)
    gists = _gists()
    if not gists:
        return 0

    try:
        import scratch_meta
        scratch_title = {d["slug"]: d["title"] for d in scratch_meta.LANE}
    except ModuleNotFoundError:
        scratch_title = {}

    files = ["gist/%s%s.html" % (G["course"].lower(), G["week"]) for G in gists]
    for i, G in enumerate(gists):
        recs = [r for r in flat
                if r["week"]["course"] == G["course"] and str(r["week"]["week"]) == str(G["week"])]
        lis = "".join(
            '<li><a data-slug-link="%s" href="../%s"><span class="n">%02d</span>%s</a></li>'
            % (r["slug"], r["file"], r["n"], html.escape(r["L"]["title"])) for r in recs)
        extra = []
        pf = os.path.join(ROOT, "problems", "%s%s.html" % (G["course"].lower(), G["week"]))
        if os.path.exists(pf):
            extra.append('<a href="../problems/%s%s.html">&#9998; the problem set</a>'
                         % (G["course"].lower(), G["week"]))
        qf = os.path.join(ROOT, "quiz", "%s%s.html" % (G["course"].lower(), G["week"]))
        if os.path.exists(qf):
            extra.append('<a href="../quiz/%s%s.html">&#9678; the mock quiz</a>'
                         % (G["course"].lower(), G["week"]))
        for sl in G.get("scratch", []):
            if sl in scratch_title:
                extra.append('<a href="../scratch/%s.html">&#9881; run it from scratch: %s</a>'
                             % (sl, html.escape(scratch_title[sl])))
        extra.append('<a href="../review.html">&#9670; the cards for this week</a>')
        compresses = (
            '<h2 id="compresses"><span class="ico">&#128218;</span>What this page compresses</h2>'
            '<p>Every claim above is taught in full in one of these. If a line here went past too '
            'quickly, the lesson is where it slows down.</p>'
            '<ol class="gistsrc">%s</ol>'
            '<p class="gistalso">%s</p>' % (lis, ' <span class="sep">&#183;</span> '.join(extra)))

        prev = ('<a class="prev" href="../%s"><span class="dir">&#8249; previous</span>'
                '<span class="ttl">%s W%s gist</span></a>'
                % (files[i - 1], gists[i - 1]["course"], gists[i - 1]["week"])) if i else '<span class="ghost"></span>'
        nxt = ('<a class="next" href="../%s"><span class="dir">next &#8250;</span>'
               '<span class="ttl">%s W%s gist</span></a>'
               % (files[i + 1], gists[i + 1]["course"], gists[i + 1]["week"])) if i < len(gists) - 1 else '<span class="ghost"></span>'

        page = GISTPAGE.format(
            course=G["course"], course_l=G["course"].lower(), week=G["week"],
            title=html.escape(G["title"]), lede=G["lede"], mins=G.get("mins", 10),
            n=len(recs), body=G["body"], compresses=compresses,
            sidebar=sidebar(weeks, flat, "gist-%s%s" % (G["course"].lower(), G["week"]), 1),
            prev=prev, next=nxt)
        wr(os.path.join(ROOT, files[i]), page)

    have = {"%s%s" % (G["course"].lower(), G["week"]) for G in gists}
    rows = []
    for w in weeks:
        k = "%s%s" % (w["course"].lower(), w["week"])
        if k in have:
            G = next(g for g in gists if "%s%s" % (g["course"].lower(), g["week"]) == k)
            rows.append(
                '<li><a data-slug-link="gist-%s" href="gist/%s.html">'
                '<span class="n">%s W%s</span><span class="pt"><b>%s</b>'
                '<span class="pgs">%s</span></span>'
                '<span class="tag2">%s min</span></a></li>'
                % (k, k, w["course"], w["week"], html.escape(G["title"]),
                   strip_tags(G["lede"])[:150], G.get("mins", 10)))
        else:
            rows.append(
                '<li class="soon"><span class="n">%s W%s</span>'
                '<span class="pt"><b>%s</b><span class="pgs">gist not written yet</span></span>'
                '<span class="tag2">&mdash;</span></li>'
                % (w["course"], w["week"], html.escape(w["title"])))
    body = ('<h2><span class="ico">&#9673;</span>Every week, in course order</h2>'
            '<ol class="problist gistlist">%s</ol>' % "".join(rows))
    wr(os.path.join(ROOT, "gist.html"),
       GISTINDEX.format(sidebar=sidebar(weeks, flat, "__gist__", 0),
                        n=len(gists), nw=len(weeks), body=body))
    return len(gists)


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


MOCKPAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Mock quiz &#183; {course} W{week}</title>
<link rel="stylesheet" href="../assets/base.css">
<link rel="stylesheet" href="../assets/print.css" media="print">
<script src="../assets/site.js"></script>
<script src="../assets/search.js"></script>
<script>window.GLOSS_UP="../";</script>
<script src="../assets/gloss-data.js"></script>
<script src="../assets/gloss.js"></script>
</head>
<body data-slug="{slug}" data-printable="Mock quiz &#183; {course} Week {week}|{n} questions">
<header class="topbar">
  <button class="btn" id="menu-toggle" aria-label="menu">&#9776;</button>
  <a class="brand" href="../index.html">ML<span>&#183;</span>notes</a>
  <span class="crumb">Mock quiz &#183; {course} W{week} &#183; <b>{title}</b></span>
  <span class="spacer"></span>
  <button class="btn" id="search-btn" title="search  (/)">&#8981;</button>
  <button class="btn" id="theme-btn" title="theme">&#9689;</button>
</header>
<div class="layout">
<aside class="sidebar">
{sidebar}
</aside>
<main>
<p class="kicker">{course} &#183; Week {week} &#183; {n} questions &#183; pass mark 80%</p>
<h1>{title}</h1>
<p class="lede">{lede}</p>

<div class="mq-head">
  <div><b>Closed book.</b> No notes, no scrolling back &mdash; that is the condition the real
  one is sat under.</div>
  <span class="mq-score" id="mq-score">&mdash;</span>
</div>

<ol class="mqlist" data-set="{slug}">
{questions}
</ol>

<div class="mq-acts">
  <button class="btn primary" id="mq-submit">Submit answers</button>
  <button class="btn" id="mq-retry" hidden>Clear and try again</button>
  <span class="msg" id="mq-msg"></span>
</div>

<nav class="pager">
{prev}
{next}
</nav>
<footer class="sitefoot">Study notes for the ML Specialization <span class="sep">&#183;</span> Hung Om</footer>
</main>
</div>
<script src="../assets/meta.js"></script>
<script src="../assets/mock.js"></script>
</body>
</html>
"""

MOCKINDEX = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Mock quizzes</title>
<link rel="stylesheet" href="assets/base.css">
<link rel="stylesheet" href="assets/print.css" media="print">
<script src="assets/site.js"></script>
<script src="assets/search.js"></script>
<script>window.GLOSS_UP="";</script>
<script src="assets/gloss-data.js"></script>
<script src="assets/gloss.js"></script>
</head>
<body data-slug="__quizzes__">
<header class="topbar">
  <button class="btn" id="menu-toggle" aria-label="menu">&#9776;</button>
  <a class="brand" href="index.html">ML<span>&#183;</span>notes</a>
  <span class="crumb">Mock quizzes &#183; <b>{n} questions in the graded-quiz format</b></span>
  <span class="spacer"></span>
  <button class="btn" id="search-btn" title="search  (/)">&#8981;</button>
  <button class="btn" id="theme-btn" title="theme">&#9689;</button>
</header>
<div class="layout">
<aside class="sidebar">
{sidebar}
</aside>
<main>
<p class="kicker">{nw} quizzes &#183; {n} questions</p>
<h1>Mock quizzes</h1>
<p class="lede">One per graded week, written the way the real quiz asks: single-answer multiple
choice and &ldquo;select all that apply&rdquo;, marked in this browser, 80% to pass. The point is
not the score. It is the <b>rationale on every option</b>, including the ones you did not pick.</p>
<div class="callout kid"><span class="tag">Why every wrong answer is explained</span>
<p>A distractor you chose for a reason is more informative than the answer you got right. Each wrong
option here is a real misunderstanding &mdash; usually a true statement about the <i>wrong</i> thing
&mdash; and the rationale names which one, so a miss tells you what to re-read rather than just
costing you a mark.</p></div>
<div class="callout trap"><span class="tag">These are not the real questions</span>
<p>Nothing here is copied from Coursera. These are written from the same lessons the graded quizzes
are drawn from, in the same format and at the same difficulty, so that sitting one tells you
something true about whether you are ready.</p></div>
{body}
<footer class="sitefoot">Study notes for the ML Specialization <span class="sep">&#183;</span> Hung Om</footer>
</main>
</div>
</body>
</html>
"""


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
<script src="../assets/gloss.js"></script>{am_js}
</head>
<body data-slug="scratch-{slug}" data-printable="From scratch &#183; {title}|{steps}">
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
  <p class="rb-b">By the end you will have built {builds}.</p>{am_anchor}
</div>
{picture}
{body}{mastery}
{primer}
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


def build_mock(weeks, flat):
    """One graded-format quiz per week, marked in the browser.

    The lessons train recognition and the problem sets train production; this
    trains the specific thing the graded quiz asks for, which is neither —
    picking the right statement out of four plausible ones under time.
    """
    sets = []
    for mname in MOCK_MODULES:
        try:
            mod = importlib.import_module(mname)
        except ModuleNotFoundError:
            continue
        importlib.reload(mod)
        sets.append(mod.SET)
    if not sets:
        return 0, 0

    files = ["quiz/%s%s.html" % (S["course"].lower(), S["week"]) for S in sets]
    total_q = sum(len(S["questions"]) for S in sets)

    for i, S in enumerate(sets):
        slug = "%s%s" % (S["course"].lower(), S["week"])
        qs = []
        for q in S["questions"]:
            opts = []
            for o in q["opts"]:
                opts.append(
                    '<li class="mq-opt" data-c="%d">'
                    '<label><input type="%s" name="%s"><span class="mq-t">%s</span></label>'
                    '<p class="mq-why">%s</p></li>'
                    % (1 if o["correct"] else 0,
                       "checkbox" if q["multi"] else "radio",
                       q["qid"], o["text"], o["why"]))
            multi = ('<span class="mq-multi">select all that apply</span>'
                     if q["multi"] else "")
            tag = ('<span class="mq-tag">%s</span>' % html.escape(q["tag"])) if q["tag"] else ""
            note = ('<p class="mq-note"><span class="lbl">What this is really testing</span>%s</p>'
                    % q["note"]) if q["note"] else ""
            qs.append(
                '<li class="mq" data-qid="%s" data-lesson="%s">'
                '<p class="mq-n">%s%s</p><div class="mq-ask">%s</div>'
                '<ul class="mq-opts">%s</ul>%s</li>'
                % (q["qid"], q["lesson"], tag, multi, q["ask"], "".join(opts), note))

        prev = ('<a class="prev" href="../%s"><span class="dir">&#8249; previous</span>'
                '<span class="ttl">%s W%s quiz</span></a>'
                % (files[i - 1], sets[i - 1]["course"], sets[i - 1]["week"])
                ) if i else '<span class="ghost"></span>'
        nxt = ('<a class="next" href="../%s"><span class="dir">next &#8250;</span>'
               '<span class="ttl">%s W%s quiz</span></a>'
               % (files[i + 1], sets[i + 1]["course"], sets[i + 1]["week"])
               ) if i < len(sets) - 1 else '<span class="ghost"></span>'

        wr(os.path.join(ROOT, files[i]),
           MOCKPAGE.format(course=S["course"], week=S["week"],
                           title=html.escape(S["title"]), lede=S["lede"],
                           slug="mock-" + slug, n=len(S["questions"]),
                           sidebar=sidebar(weeks, flat, "mock-" + slug, 1),
                           questions="\n".join(qs), prev=prev, next=nxt))

    rows = []
    for i, S in enumerate(sets):
        topics = " &middot; ".join(q["tag"] for q in S["questions"] if q["tag"])
        rows.append(
            '<li><a data-slug-link="mock-%s%s" href="%s"><span class="n">%s W%s</span>'
            '<span class="pt"><b>%s</b><span class="pgs">%s</span></span>'
            '<span class="tag2">%d questions</span></a></li>'
            % (S["course"].lower(), S["week"], files[i], S["course"], S["week"],
               html.escape(S["title"]), topics, len(S["questions"])))
    body = ('<h2><span class="ico">&#9678;</span>One per graded week</h2>'
            '<ol class="problist">%s</ol>' % "".join(rows))
    wr(os.path.join(ROOT, "quizzes.html"),
       MOCKINDEX.format(sidebar=sidebar(weeks, flat, "__quizzes__", 0),
                        n=total_q, nw=len(sets), body=body))
    return len(sets), total_q


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
                name, code, out, err, d["prose"].get(name, ""),
                d.get("walk", {}).get(name)))
        lessons = "".join(
            '<li><a href="../%s">%s</a></li>' % (href, html.escape(t))
            for href, t in d["lessons"] if shown_href(href))
        prev = ('<a class="prev" href="../%s"><span class="dir">&#8249; previous</span>'
                '<span class="ttl">%s</span></a>' % (files[i - 1], html.escape(lane[i - 1]["title"]))
                ) if i else '<span class="ghost"></span>'
        nxt = ('<a class="next" href="../%s"><span class="dir">next &#8250;</span>'
               '<span class="ttl">%s</span></a>' % (files[i + 1], html.escape(lane[i + 1]["title"]))
               ) if i < len(lane) - 1 else '<span class="ghost"></span>'
        # Some builds go past the three courses and used to lean on C4 for their
        # theory. A primer carries that ground themselves, so the file stands up
        # whether or not C4 is a hidden course.
        primer = ('<h2><span class="ico">&#129504;</span>What you need that the courses '
                  'do not cover</h2>\n<div class="callout key"><span class="tag">Enough '
                  'theory to read this file</span>%s</div>' % d["primer"]
                  ) if d.get("primer") else ""
        # The whole program as one picture, before any of it is read in pieces.
        # A file of 150 lines in eleven blocks is a list until you can see the
        # shape it makes; the shape is what the blocks are FOR.
        pic = ""
        if d.get("picture"):
            import gistkit
            importlib.reload(gistkit)
            pic = ('<h2><span class="ico">&#128444;&#65039;</span>The whole program in '
                   'one picture</h2>' + gistkit.flow(d["picture"][0],
                                                     tag=d["picture"][1],
                                                     cap=d["picture"][2]))
        # ---- Active Mastery: APPENDED after the lesson, never woven into it.
        # The lesson body above is byte-for-byte what it was before this layer
        # existed; verify_preservation.py proves that on every build.
        am_html, am_anchor, am_js, n_am = "", "", "", 0
        if d.get("mastery"):
            import masterykit
            importlib.reload(masterykit)
            am = d["mastery"]
            n_am = len(am["sections"])
            am_html = "\n" + masterykit.render(am)
            am_js = '\n<script src="../assets/am.js" defer></script>' 
            am_anchor = ('\n  <p class="rb-am"><a class="am-jump" href="#active-mastery">'
                         '&#127919; Active Mastery &#8595;</a> '
                         '<span class="d">%d exercises that use this file rather than '
                         'explain it again</span></p>' % n_am)
        steps = "%d steps" % len(sections)
        if n_am:
            steps += " + %d mastery" % n_am

        page = SCRATCHPAGE.format(
            picture=pic,
            mastery=am_html,
            am_js=am_js,
            am_anchor=am_anchor,
            steps=steps,
            primer=primer,
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
                          for href, t in r["lessons"] if shown_href(href))
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
    paper_sheets = [sh for sh in content_paper.SHEETS if shown(sh["c"])]
    for sh in paper_sheets:
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
                    nitems=sum(len(sh["items"]) for sh in paper_sheets)))
    return len(paper_sheets)


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


WALK_MODULES = ["walk_ref_f0", "walk_ref_c1", "walk_ref_c2", "walk_ref_c3", "walk_ref_c4"]
_WALK = None


def walk_for(card):
    """The long, worked, plain-words note for one reference entry.

    The card's `plain` block is a GIST — one analogy, a decode table, one line
    of code, and it is deliberately short because the same block is shown on a
    flashcard. This is the other thing a reference sheet is for: the slow read,
    with a number small enough to check by hand.

    Reference sheet only. Putting it on the review card would defeat the card:
    a flashcard you scroll is a flashcard you are no longer testing yourself on.
    """
    global _WALK
    if _WALK is None:
        _WALK = {}
        for name in _shown_modules(WALK_MODULES):
            try:
                mod = importlib.import_module(name)
            except ModuleNotFoundError:
                continue
            importlib.reload(mod)
            _WALK.update(getattr(mod, "W", {}))
    body = _WALK.get(card["id"])
    if not body:
        return ""
    return ('<div class="cwalk"><span class="cwalk-tag">Walk me through it</span>'
            '%s</div>' % body)


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
                      weekdata=json.dumps(
                          {k: v for k, v in content_mastery.WEEKS.items()
                           if shown(k[:2])}, ensure_ascii=False)))
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
    # week gists — the whole-week pages
    for G in _gists():
        u = "gist/%s%s.html" % (G["course"].lower(), G["week"])
        heads = [strip_tags(m) for m in re.findall(r"<h2[^>]*>(.*?)</h2>", G["body"], re.S)]
        idx.append({
            "t": "gist", "u": u,
            "ti": "The gist — %s" % G["title"],
            "w": "%s W%s" % (G["course"], G["week"]),
            "s": strip_tags(G["lede"])[:190],
            "h": " · ".join(heads)[:260],
            "b": strip_tags(G["body"])[:1500].lower(),
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


DATAPAGE = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Datasets</title>
<link rel="stylesheet" href="assets/base.css">
<link rel="stylesheet" href="assets/print.css" media="print">
<script src="assets/site.js"></script>
<script src="assets/search.js"></script>
<script>window.GLOSS_UP="";</script>
<script src="assets/gloss-data.js"></script>
<script src="assets/gloss.js"></script>
</head>
<body data-slug="__data__" data-printable="Datasets &#183; ML Specialization|{n} files">
<header class="topbar">
  <button class="btn" id="menu-toggle" aria-label="menu">&#9776;</button>
  <a class="brand" href="index.html">ML<span>&#183;</span>notes</a>
  <span class="crumb">Data &#183; <b>the files the lessons actually read</b></span>
  <span class="spacer"></span>
  <a class="btn" href="labs.html">lab companions</a>
  <button class="btn" id="search-btn" title="search  (/)">&#8981;</button>
  <button class="btn" id="theme-btn" title="theme">&#9689;</button>
</header>
<div class="layout">
<aside class="sidebar">
{sidebar}
</aside>
<main>
<p class="kicker">{n} files &#183; {rows} rows &#183; {kb} KB</p>
<h1>Datasets</h1>
<p class="lede">Every lesson on this site that says <code>pd.read_csv('houses.csv')</code> is reading
a real file, and this is where it lives. Download it, or skip the download entirely &#8212; pandas
reads a URL as happily as a path, so a one-line change makes any lesson runnable from a cold
notebook.</p>

<div class="callout key"><span class="tag">The one line that saves you the download</span>
<p>Paste this at the top of a notebook and every snippet on this page runs, with nothing on
disk:</p>
<pre><code>{urlsnip}</code></pre>
<p style="margin-bottom:0">Then <code>pd.read_csv(DATA + 'houses.csv')</code> anywhere a lesson
says <code>pd.read_csv('houses.csv')</code>.</p></div>

<p>The shapes below are <b>measured off the files at build time</b>, not written down &#8212; so a
column table on this page cannot describe a file that no longer looks like that. Four of the
seven are generated by <a href="https://github.com/HungOm/Machine-Learning-Specialization-Coursera/blob/main/study/_build/datakit.py"><code>datakit.py</code></a>
from a fixed seed, which is what lets the lessons quote an exact shape; the other three are the
real Coursera data already in this repository, moved to one clean path.</p>

{body}

<h2 id="how"><span class="ico">&#128295;</span>Rebuilding them</h2>
<p>The generated files are reproducible byte for byte &#8212; every generator draws from a seeded
<code>default_rng</code>, so there is no reason to be precious about the copies in git:</p>
<pre><code>{rebuild}</code></pre>
<p>The three course files are copied and reshaped from the notebooks in this repository rather
than invented. The MovieLens pair is worth a note: pivoting <code>ratings.csv</code> back into a
dense matrix reproduces the lab's own <code>small_movies_Y.csv</code> <b>exactly</b> &#8212;
<code>datakit.py</code> asserts it every time the file is regenerated, so nothing is lost by
keeping the twenty-times-smaller version.</p>

<footer class="sitefoot">Study notes for the ML Specialization <span class="sep">&#183;</span> Hung Om</footer>
</main>
</div>
</body>
</html>
'''


def build_data(weeks, flat):
    """study/data.html — one card per dataset, shapes read off the files.

    Nothing here is written twice: the blurbs and column tables come from
    datakit's registry, and the shape, column count and file size are measured
    from the file on disk. A dataset that stops matching its description is a
    build-time failure, not a page that quietly lies.
    """
    try:
        import datakit
    except ModuleNotFoundError:
        return 0, 0
    importlib.reload(datakit)
    sets = datakit.measure()

    missing = [d["file"] for d in sets if not d["rows"]]
    if missing:
        print("  !! datasets missing from study/data/: %s" % ", ".join(missing))
        print("     run: python3 study/_build/datakit.py")
    dead = [h for d in sets for h, _ in d["used"]
            if shown_href(h) and not os.path.exists(os.path.join(ROOT, h))]
    if dead:
        print("  !! datakit points at lessons that do not exist: %s" % ", ".join(dead))

    cards, total_rows, total_bytes = [], 0, 0
    for d in sets:
        total_rows += d["rows"]
        total_bytes += d["bytes"]
        cols = "".join(
            '<tr><td><code>%s</code></td><td class="ty">%s</td><td>%s</td><td>%s</td></tr>'
            % (c["name"], c["kind"], c["unit"] or "&#8212;", c["what"] or "&#8212;")
            for c in d["columns"])
        lessons = "".join(
            '<li><a href="%s">%s</a></li>' % (h, html.escape(t))
            for h, t in d["used"] if shown_href(h))
        origin = ("generated" if d["origin"] == "generated" else "from the course")
        size = ("%.1f KB" % (d["bytes"] / 1024) if d["bytes"] < 1024 * 1024
                else "%.1f MB" % (d["bytes"] / 1024 / 1024))
        cards.append(
            '<section class="dset" id="%s">'
            '<header><h3><code>%s</code></h3>'
            '<span class="shape">%s &#215; %d</span>'
            '<span class="orig %s">%s</span>'
            '<span class="sz">%s</span></header>'
            '<p class="blurb">%s</p>'
            '<div class="dl">'
            '<a class="btn primary" href="data/%s" download>&#8595; download</a>'
            '<a class="btn" href="%s%s">raw URL</a>'
            '<a class="btn" href="data/%s">view</a></div>'
            '<h4>Columns</h4>'
            '<table class="data dcols"><thead><tr><th>column</th><th>type</th>'
            '<th>unit</th><th>what it is</th></tr></thead><tbody>%s</tbody></table>'
            '<h4>Reading it</h4><pre><code>%s</code></pre>'
            '<div class="callout note"><span class="tag">Why this file</span><p>%s</p></div>'
            '<h4>Used by</h4><ul class="dused">%s</ul>'
            '</section>'
            % (d["file"].replace(".", "-"), html.escape(d["file"]),
               "{:,}".format(d["rows"]), d["cols"],
               d["origin"], origin, size,
               d["blurb"], d["file"], datakit.RAW, d["file"], d["file"],
               cols, kit.highlight(d["snippet"].strip("\n")), d["why"], lessons))

    urlsnip = kit.highlight(
        "import pandas as pd\n\n"
        "DATA = '%s'\n\n"
        "df = pd.read_csv(DATA + 'houses.csv')\n"
        "df.shape        # (1000, 5)" % datakit.RAW)
    rebuild = kit.highlight("python3 study/_build/datakit.py\npython3 study/_build/build.py")

    wr(os.path.join(ROOT, "data.html"),
       DATAPAGE.format(sidebar=sidebar(weeks, flat, "__data__", 0),
                       n=len(sets), rows="{:,}".format(total_rows),
                       kb=round(total_bytes / 1024),
                       urlsnip=urlsnip, rebuild=rebuild,
                       body="\n".join(cards)))
    return len(sets), total_rows


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
    n_gist = build_gist(weeks, flat)
    n_mock, n_mq = build_mock(weeks, flat)
    n_sc, n_sl, n_ss = build_scratch(weeks, flat)
    n_lab, n_grad, n_ex = build_labs(weeks, flat)
    n_data, n_drows = build_data(weeks, flat)
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
        print("       + mastery.html (%d weeks, ~%d h budgeted)" % (len(weeks), n_hours))
    if n_sets:
        print("       + %d problem sets (%d problems)" % (n_sets, n_prob))
    if n_gist:
        print("       + %d week gists (gist.html)" % n_gist)
    if n_mock:
        print("       + %d mock quizzes (%d questions, graded in browser)" % (n_mock, n_mq))
    if n_sc:
        print("       + %d from-scratch pages (%d lines run, %d sections)" % (n_sc, n_sl, n_ss))
    if n_lab:
        print("       + %d lab companions (%d graded, %d exercises)" % (n_lab, n_grad, n_ex))
    if n_data:
        print("       + data.html (%d datasets, %d rows, shapes measured off disk)"
              % (n_data, n_drows))


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
