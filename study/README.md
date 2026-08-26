# Study notes — animated, one page per lesson

A self-contained static site of study notes for the Machine Learning Specialization.
No build tools, no CDN, no internet needed to read it. Just open `index.html`.

```
open study/index.html          # macOS
```

## What's here

| | |
|---|---|
| `index.html` | The study plan: how to use it, week-by-week schedules, prerequisites, reference shelf |
| `review.html` | Spaced-repetition trainer — 132 cards, SM-2 scheduling, progress in `localStorage` |
| `reference.html` | The same 132 entries with both sides showing, grouped by week |
| `f0/…` | **Foundations** — the maths and Python the courses assume you know |
| `problems/…` | 12 problem sets, 156 problems with full worked solutions |
| `scratch/…` | 10 algorithms in pure NumPy · `scratch/code/*.py` really run |
| `labs/…` | A companion page for every one of the 41 notebooks in this repo |
| `progress.html` | Dashboard: weak spots, forecast, Anki export, backup |
| `c1/…`, `c2/…`, `c3/…` | One page per lesson (`w<N>-<nn>-<slug>.html`), paginated with prev / next |
| `symbols.html` | Filterable glossary: 71 symbols, how to say them, NumPy equivalents |
| `assets/base.css` | All styling, light + dark |
| `assets/anim.js` | ~300-line animation runtime (canvas, sliders, theme-aware redraw) |
| `assets/w-c<C>w<N>.js` | The interactive widgets for that course-week |
| `assets/site.js` | Theme toggle, progress tracking, keyboard paging |
| `assets/srs.js` | The spaced-repetition scheduler and review UI |
| `assets/deck.js` | Generated — the card deck as JSON |
| `_build/cards_c*.py` | Card content, one module per course |
| `_build/cards_plain_c*.py` | The plain-English decode for each card, keyed by card id |
| `_build/install-alarm.sh` | Install / test / remove the nightly 22:00 alarm |
| `_build/` | The generator and all lesson content |

**Coverage:** a Foundations track plus the whole specialization — **172 lessons, 172 interactive
animations, 156 problems with worked solutions, 10 algorithms implemented from scratch in NumPy,
41 lab companions, 492 self-check questions, 161 spaced-repetition cards, 71 glossary symbols,
252 links** to papers and documentation. 243 pages in total.

## The five lanes

Reading is one of them and on its own the weakest — recognising an idea and producing it from
nothing are different skills.

| Lane | What it is | Where |
|---|---|---|
| **Read** | 172 lessons, one per page, each with an animation | `index.html` |
| **Do** | 156 problems, every line of working shown, topics interleaved | `problems.html` |
| **Build** | 10 algorithms in pure NumPy, each checked against something independent | `scratch.html` |
| **Practise** | 41 lab companions — what each notebook is for, and what its exercises ask | `labs.html` |
| **Remember** | 161 SRS cards + a dashboard that finds your weak spots | `review.html`, `progress.html` |
| **Scribble** | 12 from-memory sheets, and a paper prompt on every reference entry | `paper.html` |

**When is a week done?** `mastery.html` answers it: five conditions per week, four checked
against what you have marked, graded and reviewed (`_build/content_mastery.py` +
`assets/mastery.js`). It also fixes the working order and budgets ~84 h across the twelve weeks.

| Course | Weeks | Lessons | Topics |
|---|---|---|---|
| **F0 — Foundations** | 1–2 | **35** | functions, graphs, Greek letters, slope, derivatives, Σ/Π, vectors, matrices, exp/log, probability, statistics · then Jupyter, NumPy, shapes, broadcasting, masks, pandas, errors |
| C1 — Supervised ML: Regression and Classification | 1–3 | 33 | linear regression, cost functions, gradient descent, vectorisation, scaling, logistic regression, regularisation |
| C2 — Advanced Learning Algorithms | 1–4 | 61 | neural networks, training, bias/variance, decision trees |
| C3 — Unsupervised, Recommenders, RL | 1–3 | 43 | clustering, anomaly detection, recommenders, PCA, reinforcement learning |

## Reading it

Every lesson page has the same shape:

1. **The idea, for a ten-year-old** — the concept with no notation at all
2. **The maths, decoded** — the formula, with every symbol explained in a table
3. **Watch it move** — an interactive animation of that specific idea
4. **In code** — the NumPy / TensorFlow / sklearn version
5. **Traps** — the mistakes people actually make
6. **Check yourself** — questions with click-to-reveal answers
7. **Go deeper** — original papers, docs, and the labs in this repository

Keyboard: <kbd>←</kbd> / <kbd>→</kbd> move between lessons. "mark done" tracks progress in
`localStorage` (nothing is uploaded anywhere; "reset progress" on the index clears it).

## The Foundations track

`f0/` is 35 lessons covering what the three courses silently assume: the maths lane (19 lessons —
functions through argmax) and the Python lane (16 — Jupyter through reading a traceback).

Every Foundations lesson has the same six parts, which is the shape to keep if you add more:

1. **The idea, for a ten-year-old** — no notation at all
2. **The symbol, and how to say it** — a decoder table with pronunciations
3. **Worked by hand** — tiny numbers, done on paper
4. **Watch it move** — the animation
5. **In NumPy** — the code equivalent, with pandas where relevant
6. **What is actually happening** — the mechanism underneath

`symbols.html` is the companion: 71 symbols in one filterable table, each with pronunciation, meaning,
NumPy equivalent, and which week you meet it. Edit it in `_build/content_symbols.py`.

## Problem sets

`problems/` holds one set per week, 12 sets and 156 problems. Each problem carries a permanent
`pid`, a difficulty (warm-up / core / stretch), a hint on the harder ones, a solution showing
**every intermediate step**, and a note on what it is really testing.

Problems within a set are **interleaved on purpose** — mixed rather than grouped by lesson.
Blocked practice feels better and works worse: it removes the step where you decide what kind of
problem you are looking at, which is the part that matters under exam conditions.

Author them in `_build/problems_<course>w<N>.py` using `problemkit.P(...)`. Every numeric answer in
the existing sets was verified against NumPy before it shipped; keep doing that.

## The from-scratch lane

`scratch/code/*.py` are **real, runnable files** — `python3 07_kmeans.py` works right now. The HTML
pages are generated by executing each file one `# %% SECTION:` block at a time and capturing what
that block printed, so:

- the code on the page is read out of the file that runs, and
- the output under it is what that code actually produced.

Neither can drift from the other, and if a file broke, its page would show the error instead of
output. Narrative lives in `_build/scratch_meta.py`, keyed by section name.

Each file checks itself against something independent: a numerical gradient, a closed-form
solution, or the library's own answer.

## Lab companions

`labs/` has one page per notebook, all 41 of them. The outline, the function list and the exercise
markers are **read out of the real `.ipynb` at build time** (`_build/labkit.py`), so a companion
cannot describe a lab that has changed. The judgement — what the lab is for, which lessons it leans
on, the one thing to watch, and for the 11 graded assignments what each of the 31 exercises asks —
is hand-written in `_build/lab_meta.py`.

**Solution code for graded exercises is deliberately never extracted.** Each exercise card gives the
specification instead: what to return, in what shape, the maths, and the mistake to expect.

## Reviewing (spaced repetition)

`review.html` is a flashcard trainer over 132 cards covering every formula, algorithm and
load-bearing concept in the three courses. The scheduler is an SM-2 variant:

| Grade | Effect |
|---|---|
| **Again** | resets the card; it returns later in the same session |
| **Hard** | short interval, ease factor drops |
| **Good** | 1 day → 6 → 15 → 38 → 95 → 238 → 595 … |
| **Easy** | 3 days → 8 → 28 → 102 → 385 … , ease factor rises |

Progress lives in `localStorage` under `mls-srs-v1`. **Export it** before clearing site data —
there is a button on the page. Keyboard: `space` reveals, `1`–`4` grade.

Every card carries a second answer written for a beginner: a jargon-free restatement plus a
symbol-by-symbol table (*what it looks like · how you say it · what it actually means*). 656 symbols
and terms are decoded across the deck, 2–7 per card. These live in `_build/cards_plain_c*.py`, keyed
by card id — the build warns if any card is missing one.

Card content is in `_build/cards_f0.py`, `cards_c1.py`, `cards_c2.py`, `cards_c3.py`. A card's `cid` is its
permanent identity — the learner's schedule is keyed on it, so **renaming a cid silently resets
that card's progress**. Treat them as append-only.

### NumPy snippets on every reference entry

All 161 entries carry a short, runnable NumPy snippet. They live in
`_build/content_code.py` keyed by card id, and `_build/codekit.py` **executes every one at
build time** — the result shown beside a snippet is the value it produced, and a snippet that
raises is reported by the build rather than shipped.

**Two rules, both machine-enforced by `_build/vocabcheck.py`:**

1. **NumPy, always.** Never a pure-Python loop over data. Every lab, assignment and
   from-scratch file is NumPy, and writing Σ as a `for` loop would model the exact habit
   Course 1 spends a week arguing against.
2. **Nothing the Foundations Python track does not teach.** No `lambda`, no comprehensions,
   no ternaries, no `np.c_` / `meshgrid` / `eye` / `[:, None]`, no `float()` or `int()` casts
   added just to tidy the printed value. A reader who has finished F0 W2 must be able to read
   every line without looking anything up — otherwise the snippet is not helping.

`vocabcheck.py` walks the **AST**, not the text, so the word "try" in a comment or "lambda" in
prose cannot trigger it. The build runs it and reports any snippet that drifts outside.

This was not the case when the snippets first shipped: 47 of 161 used something Foundations
never teaches, `lambda` in 22 of them and pointless `float()` casts in 29. Keep them under
three lines — the point is to show the concept in code you could type.

### Every symbol gets decoded, automatically

A card that prints σ and never says what σ is has failed the only job this deck has for
someone without a maths background. `build.py` enforces that: after the cards load, it
scans each one for symbols a beginner cannot guess (Greek letters, Σ ∂ √ ‖ ∈ ≈ ≥ ≠ …,
ignoring anything inside `<code>`), and any that the card's own decode table misses get a
row appended from the glossary in `_build/content_symbols.py`. The build prints how many
it filled in. Currently 37, and **0 cards are left using a symbol they never explain**.

So the glossary is load-bearing, not decoration: if a symbol is missing there, the
auto-fill cannot rescue a card that uses it. Keep it complete, and never leave a
`what it means` field empty.

### Reading level

The plain-English blocks measure at **Flesch-Kincaid grade 5.5** (reading ease 76) against
**7.7** for the formal answers — checked over all 161 cards. If you add cards, keep the
plain layer under roughly grade 7: short sentences, no unexplained noun phrases, and
concrete before abstract.

The reference sheet has three reading modes — *everything*, *plain English only*,
*formulas only* — so the whole sheet can be read at either level. The choice is remembered.

### Refresher panels

The courses lean on maths they never teach. Four panels cover it, listed in
`REFRESHER_MODULES` in `build.py`:

| Module | Anchor | Covers | Because |
|---|---|---|---|
| `content_trig.py` | `#trig` | cos, sin, tan, θ, radians, Pythagoras, perpendicular, cosine similarity | `a · b = ‖a‖‖b‖ cos θ` and C3 W2's cosine similarity |
| `content_proj.py` | `#projection` | projection, unit vector, orthonormal | C3 W2 says "project: z = x · u" and never defines projecting |
| `content_growth.py` | `#growth` | O(n), n³ | "does not scale" is asserted 13 times and never shown |
| `content_means.py` | `#means` | arithmetic, weighted, harmonic | dropping the weights in information gain overstates a gain 4.7× |

Each module exports **`TERMS`** (the floating notes), **`PATTERNS`** (what to badge),
**`PANEL`** (the bonus section), plus `ANCHOR` and `TOPIC`. The build wraps the **first
mention on each page** in a small badge that opens a floating note — 63 badges across 35
pages, never twice for the same term on one page, never inside code, a heading or a link.
The panels sit at the end of `reference.html` and `symbols.html`.

To add a fifth: write the module, add it to `REFRESHER_MODULES`, and add glossary rows so
site search finds it. Everything else — badges, popovers, search, print rules — follows.

**How the list was chosen.** All 30 maths ideas the courses use were checked against the
19 Foundations lessons, 869 decode rows and the glossary. Most were already covered — including
several that looked like gaps (convexity has a "bumpy versus bowl" animation; the chain rule is
taught with gear multipliers). Eight terms were used but defined nowhere; three warranted a
visual, five needed only a glossary row. Only **L1 vs L2** is deliberately left out: this
specialization only ever uses L2.

### Working it on paper

`paper.html` is the method page: four moves in order (copy once → draw the thing → fill a
blank sheet → explain it), what a good page looks like, a twenty-minute session, and **12
week sheets** — one page per week you should be able to fill from memory, each with a
picture to draw first, 5–7 things to recall, and a closing question.

Every claim is sourced to a paper, and **the DOIs were checked against Crossref before they
were written** — one I reached for from memory turned out to be Kirschner/Sweller/Clark
rather than Mayer, which is exactly why the check exists.

Paper prompts live in `_build/content_paper.py`:

- `SHEETS` — the 12 week targets
- `SCRIBBLE` — 45 bespoke per-card prompts, keyed by card id
- `BY_KIND` — the fallback for the other 116, one template per card kind
- `FOUNDATION` — one prompt per Foundations lesson, keyed by lesson slug

That yields 52 distinct prompts across the 161 reference entries. If you add a card, it
picks up a kind template automatically; add a `SCRIBBLE` entry when a specific drawing is
obviously right.

### What the dashboard reads

`meta.js` carries **all six lanes**, not just lessons — `problems`, `scratch`, `labs`,
`problemLesson` and `problemsByWeek`. That last pair matters: problem grades are stored as
`P:<pid>`, so without a pid→lesson map a missed problem cannot be traced back to a lesson and
is silently discarded. That was a real bug — 156 problems produced zero weak-spot entries.

Two related rules for anything added later:

- **If a page has a `mark done` button, something must read that flag.** 63 pages once wrote a
  completion flag nothing displayed.
- **Quiz answers and problem grades are different activities.** They share one localStorage key
  but must never be summed into one percentage — recognition and production are the two things
  the dashboard exists to tell apart.

## The nightly alarm

A macOS LaunchAgent that plays a real sound at 22:00 every day.

```
bash study/_build/install-alarm.sh            # install (or reinstall)
bash study/_build/install-alarm.sh --test     # fire it right now
bash study/_build/install-alarm.sh --status   # is it loaded?
bash study/_build/install-alarm.sh --time 21 30   # different time
bash study/_build/install-alarm.sh --remove   # uninstall
```

It plays `/System/Library/Sounds/Submarine.aiff` three times and posts a notification.
Log: `~/Library/Logs/mlnotes-review.log`. Plist: `~/Library/LaunchAgents/com.mlnotes.review.plist`.

Environment overrides (set them in the plist or the script):
`MLNOTES_SOUND`, `MLNOTES_REPEATS`, `MLNOTES_OPEN=1` (also open `review.html`).

If the Mac is asleep at 22:00, launchd fires the job when it next wakes.

## Rebuilding / extending

Content lives in Python modules, one per week. To edit a lesson, change the text in
`_build/content_c2w<N>.py` and run:

```
python3 study/_build/build.py
```

To add a week:

1. Write `_build/content_c<C>w<N>.py` exporting `WEEK = dict(course=..., week=..., lessons=[...])`
2. Add its module name to `MODULES` in `_build/build.py` (list order defines the pagination chain)
3. Add the widgets to `assets/w-c<C>w<N>.js` (registered with `A.def('name', fn)`)
4. Rebuild

The builder handles pagination, the sidebar, the index and the per-page widget script tag.

## Checking your work

Five checks, each of which has caught a real bug:

```bash
# 1. every widget executes headlessly
node study/_build/smoke.js study/assets anim.js \
    w-f0w1.js w-f0w2.js w-c1w1.js w-c1w2.js w-c1w3.js \
    w-c2w1.js w-c2w2.js w-c2w3.js w-c2w4.js w-c3w1.js w-c3w2.js w-c3w3.js

# 2. every from-scratch file still runs standalone
cd study/scratch/code && for f in *.py; do python3 "$f" >/dev/null || echo "FAIL $f"; done

# 3. rebuild — a broken scratch section prints its error, and a lab with no
#    annotation is named
python3 study/_build/build.py
```

4. **Page behaviour** — the jsdom suites load the real built pages and run the real
   scripts against them (search, print modes, quiz→SRS nudging, the dashboard,
   problem grading, lab pages). Use `pagetest.js` as the harness.

5. **Citations** — check every cited paper's *title* against the arXiv or Crossref API,
   not just its HTTP status. Five citations once pointed at real pages that were the
   wrong paper.

6. **Syntax highlighting** — the build fails loudly if a `<code>` block contains torn span
   markup. Highlighting is **one left-to-right pass** (`kit.highlight`), shared by lessons and
   the from-scratch lane. It used to be a series of `re.sub` calls, and a later pass matched
   the `class=` attribute of spans an earlier pass had inserted — `class` is a Python keyword.
   That shipped: 1,404 broken spans across 87 pages. A single alternation cannot do it, because
   `re.sub` never rescans its own replacement.

7. **Fonts** — `python3 study/_build/glyphcheck.py` tests every character the site uses
   against the fonts each stack actually asks for. This is not paranoia: the vector
   arrow `x⃗` (U+20D7) has **no glyph in any font macOS ships** and rendered as a box
   everywhere it appeared. Canvas is the strict case — `fillText` cannot fall back
   glyph-by-glyph, so `A.safe()` in `anim.js` rewrites what the chosen stack lacks, and
   `glyphcheck.py` reads those maps so the two cannot drift.

Also worth repeating: resolve every `../` link from the page's own directory (pages one
level deep need `../..` to reach the repo root), and verify problem-set arithmetic
against NumPy rather than by eye.

### Writing maths

Use the helpers in `kit.py` rather than typing the character:

| Want | Write | Not |
|---|---|---|
| a vector | `vec("x")` | `x⃗` — U+20D7 exists in no font |
| an estimate | `hat("y")` | (the combining circumflex is fine, but be consistent) |
| a square root | `sqrt("x<sup>2</sup> + y<sup>2</sup>")` | `<span class="sqrt">√…</span>` — the bar goes over the **radicand**, not the sign |
| sub/superscript letters | `<sub>j</sub>`, `<sup>(i)</sup>` | `ⱼ`, `⁽ⁱ⁾` — missing from the serif stack |

`build.py` translates `x⃗` in the sources into the CSS form at write time, so authoring it
by hand still works — but the helper is clearer. Never put `class="..."` inside a
double-quoted Python string in the content modules; the quotes collide.
