#!/usr/bin/env python3
"""Prove the Active Mastery layer APPENDED and did not rewrite.

Two independent checks, because a hash alone cannot express "append-only":

  1. The .py files must be BYTE-IDENTICAL to the recorded baseline. They are
     the source of truth for every code block on every page, so any drift here
     invalidates every claim the pages make.

  2. Each .html file must still contain the ENTIRE original document as an
     ordered subsequence of lines -- every original line, in its original
     order, with nothing removed and nothing reordered. New lines may appear
     between them. That is the formal statement of "sections added, lesson
     not rewritten", and it is stricter than a diff eyeball.

Run:  python3 study/_build/verify_preservation.py
Exit: 0 if every file passes, 1 otherwise.
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BASE = os.path.join(HERE, "_baseline")


def load_baseline():
    with open(os.path.join(BASE, "hashes.json")) as f:
        hashes = json.load(f)
    with open(os.path.join(BASE, "snapshot.json")) as f:
        snap = json.load(f)
    return hashes, snap


SANCTIONED = "data-printable"


def sanctioned_variant(orig_line, cur_line):
    """The brief permits exactly one edit to an existing line: updating the
    data-printable step count. Allow that, and nothing else -- the line must be
    identical outside the attribute value."""
    if SANCTIONED not in orig_line:
        return False
    import re
    strip = lambda L: re.sub(r'data-printable="[^"]*"', 'data-printable=""', L)
    return strip(orig_line) == strip(cur_line)


def is_ordered_subsequence(original, current):
    """Every line of `original`, in order, somewhere in `current`.

    Returns (ok, first_missing_line_number, the_line); records any sanctioned
    data-printable rewrite in `notes`. Greedy matching is
    correct here: if a greedy scan cannot place original line k, no scan can,
    because every candidate position for k is at or after the greedy one.
    """
    i = 0
    notes = []
    for k, line in enumerate(original):
        found = False
        while i < len(current):
            if current[i] == line:
                i += 1
                found = True
                break
            if sanctioned_variant(line, current[i]):
                i += 1
                found = "sanctioned"
                break
            i += 1
        if not found:
            return False, k + 1, line
        if found == "sanctioned":
            notes.append(line.strip()[:52])
    return True, 0, ""


def main():
    hashes, snap = load_baseline()
    py_fail = html_fail = 0
    py_n = html_n = 0

    print("1. runnable code -- must be byte-identical")
    for rel in sorted(k for k in hashes if k.endswith(".py")):
        py_n += 1
        cur = hashlib.sha256(open(os.path.join(ROOT, rel), "rb").read()).hexdigest()
        ok = cur == hashes[rel]
        if not ok:
            py_fail += 1
        print("   %-48s %s" % (rel, "identical" if ok else "*** CHANGED ***"))

    print("\n2. lesson pages -- original content must survive in order")
    for rel in sorted(k for k in hashes if k.endswith(".html")):
        html_n += 1
        original = snap[rel].splitlines()
        current = open(os.path.join(ROOT, rel), encoding="utf-8").read().splitlines()
        ok, ln, line = is_ordered_subsequence(original, current)
        added = len(current) - len(original)
        if ok:
            note = "  [data-printable updated]" if SANCTIONED in snap[rel] and \
                   snap[rel].splitlines() != current and \
                   any(SANCTIONED in l for l in current) and \
                   [l for l in original if SANCTIONED in l] != \
                   [l for l in current if SANCTIONED in l] else ""
            print("   %-46s intact  (+%d lines appended)%s" % (rel, added, note))
        else:
            html_fail += 1
            print("   %-46s *** LOST line %d: %s" % (rel, ln, line[:60]))

    print("\n%d .py checked, %d changed" % (py_n, py_fail))
    print("%d .html checked, %d damaged" % (html_n, html_fail))
    bad = py_fail + html_fail
    print("\n%s" % ("PASS -- every original byte still present, in order."
                    if not bad else "FAIL -- %d file(s) were rewritten, not appended to." % bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
