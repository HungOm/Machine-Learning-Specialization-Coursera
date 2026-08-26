"""Read the real .ipynb files and pull out their structure.

Nothing here invents anything: the outline, the functions and the exercise
markers are all read from the notebook on disk, so a companion page cannot
describe a lab that no longer looks like that.

Deliberate omission: for graded assignments the solution code is NOT extracted.
The point of an assignment is to write it.
"""
import json
import os
import re

EX = re.compile(r"UNQ_C(\d+)")
DEF = re.compile(r"^\s*def\s+(\w+)\s*\(([^)]*)\)", re.M)
GRADED_HINT = re.compile(r"UNQ_C\d+|### START CODE HERE|# UNIT TEST", re.I)


def _src(cell):
    s = cell.get("source", "")
    return s if isinstance(s, str) else "".join(s)


def read(path):
    """Structure of one notebook."""
    nb = json.load(open(path, encoding="utf-8"))
    cells = nb.get("cells", [])
    md = [c for c in cells if c.get("cell_type") == "markdown"]
    code = [c for c in cells if c.get("cell_type") == "code"]
    code_src = "\n".join(_src(c) for c in code)

    title = None
    outline = []
    for c in md:
        for line in _src(c).splitlines():
            m = re.match(r"^(#{1,4})\s+(.*)$", line.strip())
            if not m:
                continue
            level, text = len(m.group(1)), m.group(2).strip()
            text = re.sub(r"<[^>]+>", "", text).strip()
            if not text:
                continue
            if title is None:
                title = text
                continue
            outline.append((level, text))

    exercises = sorted({int(x) for x in EX.findall(code_src)})
    funcs = []
    for name, args in DEF.findall(code_src):
        if name.startswith("_") or name in ("main",):
            continue
        if name not in [f[0] for f in funcs]:
            funcs.append((name, args.strip()))

    imports = sorted({m for m in re.findall(r"^\s*import\s+(\w+)|^\s*from\s+(\w+)",
                                            code_src, re.M) for m in m if m})
    return {
        "path": path,
        "file": os.path.basename(path),
        "title": title or os.path.basename(path),
        "outline": outline,
        "n_cells": len(cells),
        "n_md": len(md),
        "n_code": len(code),
        "exercises": exercises,
        "functions": funcs,
        "imports": imports,
        "graded": bool(exercises) or bool(GRADED_HINT.search(code_src)),
    }


def scan(repo_root):
    out = []
    for dirpath, dirnames, filenames in os.walk(repo_root):
        dirnames[:] = [d for d in dirnames
                       if d not in (".ipynb_checkpoints", "archive", "study", ".git")]
        for f in sorted(filenames):
            if f.endswith(".ipynb"):
                out.append(read(os.path.join(dirpath, f)))
    return out
