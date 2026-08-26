#!/usr/bin/env python3
"""Check every character the site uses against the fonts it asks for.

Canvas cannot fall back glyph-by-glyph, and HTML falls back to whatever the OS
picks — which is fine but can silently change face mid-equation. A character
absent from every font in a stack renders as a tofu box.

Run:  python3 study/_build/glyphcheck.py
Needs fontTools. Emoji are skipped (they come from Apple Color Emoji).
"""
import glob
import os
import re
import sys
import unicodedata

try:
    from fontTools.ttLib import TTFont, TTCollection
except ImportError:
    sys.exit("needs fontTools:  pip3 install fonttools")

SUP = "/System/Library/Fonts/Supplemental/"
SYS = "/System/Library/Fonts/"

# the stacks declared in base.css / anim.js, in order
STACKS = {
    # HTML really does fall back across every installed font, so the honest
    # test for a page is "is this character in ANY of them?". The declared
    # stack still matters for consistency of face, reported separately.
    "serif (equations)": [SUP + "Iowan Old Style.ttc", SUP + "Palatino.ttc",
                          SUP + "Georgia.ttf", SUP + "Times New Roman.ttf",
                          SUP + "Arial Unicode.ttf", SYS + "Apple Symbols.ttf",
                          SYS + "SFNS.ttf", SYS + "Menlo.ttc",
                          SUP + "STIXGeneral.otf", SUP + "Symbol.ttf",
                          SYS + "AppleSDGothicNeo.ttc", SYS + "ZapfDingbats.ttf",
                          SUP + "Times New Roman.ttf"],
    "sans (body text)":  [SYS + "SFNS.ttf", SUP + "Arial.ttf", SUP + "Verdana.ttf"],
    "mono (code)":       [SYS + "Menlo.ttc", SUP + "Courier New.ttf"],
    "canvas sans":       [SYS + "SFNS.ttf"],
    "canvas mono":       [SYS + "Menlo.ttc"],
}


def cmap_of(path):
    if not os.path.exists(path):
        return None
    try:
        f = TTCollection(path).fonts[0] if path.endswith(".ttc") else TTFont(path, fontNumber=0)
        out = set()
        for t in f["cmap"].tables:
            out |= set(t.cmap.keys())
        return out
    except Exception:
        return None


def is_emoji(ch):
    """Emoji come from Apple Color Emoji, which is not in any text stack."""
    o = ord(ch)
    return ((0x1F000 <= o <= 0x1FAFF) or (0x2600 <= o <= 0x27BF)
            or (0x2190 <= o <= 0x21FF and ch in "\u2194\u2195")  # arrows w/ emoji forms
            or (0x231A <= o <= 0x23FF)                             # ⌚ ⌛ ⏱ ⏰ …
            or (0x2B00 <= o <= 0x2BFF) or (0xFE00 <= o <= 0xFE0F)
            or o in (0x200D, 0x20E3, 0x2122, 0x2139))


def canvas_swaps(root):
    """Read the A.safe() maps out of anim.js so this check cannot drift from it."""
    src = open(os.path.join(root, "assets", "anim.js"), encoding="utf-8").read()
    out = {"both": {}, "sans": {}, "mono": {}}
    for key, name in (("both", "SAFE_BOTH"), ("sans", "SAFE_SANS"), ("mono", "SAFE_MONO")):
        m = re.search(name + r"\s*=\s*\{(.*?)\}", src, re.S)
        if not m:
            continue
        for k, v in re.findall(r"'\\u([0-9a-fA-F]{4})'\s*:\s*'((?:\\u[0-9a-fA-F]{4}|[^'])*)'", m.group(1)):
            val = re.sub(r"\\u([0-9a-fA-F]{4})", lambda mm: chr(int(mm.group(1), 16)), v)
            out[key][chr(int(k, 16))] = val
    return out


def collect(root):
    """(chars in HTML, chars in canvas strings) — canvas is checked separately
    because A.txt draws literally, with no fallback."""
    html_chars, canvas_sans, canvas_mono = set(), set(), set()
    for p in glob.glob(os.path.join(root, "*.html")) + glob.glob(os.path.join(root, "*/*.html")):
        html_chars |= {c for c in open(p, encoding="utf-8").read() if ord(c) > 127}
    for p in glob.glob(os.path.join(root, "assets", "w-*.js")):
        src = open(p, encoding="utf-8").read()
        for m in re.finditer(r"A\.txt\(\s*ctx\s*,\s*(.{0,400}?)\)\s*;", src, re.S):
            chunk = m.group(1)
            target = canvas_mono if "mono: true" in chunk or "mono:true" in chunk else canvas_sans
            target |= {c for c in chunk if ord(c) > 127}
    return html_chars, canvas_sans, canvas_mono


def report(label, chars, stack_paths):
    cmaps = [(os.path.basename(p), cmap_of(p)) for p in stack_paths]
    cmaps = [(n, c) for n, c in cmaps if c]
    if not cmaps:
        print(f"  {label}: no fonts found, skipped")
        return []
    missing = []
    for ch in sorted(chars, key=ord):
        if is_emoji(ch) or unicodedata.category(ch) == "Zs":
            continue
        if not any(ord(ch) in c for _, c in cmaps):
            missing.append(ch)
    first = cmaps[0]
    fell_back = [ch for ch in sorted(chars, key=ord)
                 if not is_emoji(ch) and ord(ch) not in first[1]
                 and any(ord(ch) in c for _, c in cmaps[1:])]
    print(f"\n  {label}  ({', '.join(n for n, _ in cmaps)})")
    if missing:
        print(f"    MISSING FROM EVERY FONT — renders as a box:")
        for ch in missing:
            try:
                nm = unicodedata.name(ch)
            except ValueError:
                nm = "?"
            print(f"      U+{ord(ch):04X}  {ch}  {nm}")
    else:
        print("    every character resolves in this stack")
    if fell_back:
        print(f"    falls back past the first font ({first[0]}): "
              + " ".join(f"U+{ord(c):04X}" for c in fell_back[:14])
              + (" …" if len(fell_back) > 14 else ""))
    return missing


if __name__ == "__main__":
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    html_chars, cs, cm = collect(root)
    sw = canvas_swaps(root)
    # A.txt runs every string through A.safe() before drawing — apply the same
    # substitutions here, then check what is actually handed to fillText.
    def applied(chars, which):
        out = set()
        for ch in chars:
            rep = sw["both"].get(ch, sw[which].get(ch, ch))
            out |= set(rep) if rep else set()
        return out
    cs, cm = applied(cs, "sans"), applied(cm, "mono")
    print(f"  (A.safe rewrites {len(sw['both'])} chars in both canvas stacks, "
          f"{len(sw['sans'])} in sans, {len(sw['mono'])} in mono)")
    print(f"checking {len(html_chars)} distinct characters in HTML, "
          f"{len(cs)} in canvas sans, {len(cm)} in canvas mono")
    bad = []
    bad += report("HTML (any installed font may be used)", html_chars, STACKS["serif (equations)"])
    bad += report("canvas sans (A.txt)", cs, STACKS["canvas sans"])
    bad += report("canvas mono (A.txt mono:true)", cm, STACKS["canvas mono"])
    print()
    if bad:
        print(f"FAIL — {len(set(bad))} character(s) have no glyph anywhere they are used")
        sys.exit(1)
    print("PASS — every character used has a glyph in the stack that will draw it")
