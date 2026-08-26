#!/usr/bin/env python3
"""Check the reference snippets stay inside the vocabulary the site teaches.

A snippet is only useful if the reader can read it. The Foundations Python track
(F0 W2) teaches arrays, shapes, indexing, slicing, broadcasting, @, axis=,
boolean masks, reshape, aggregations, pandas and def. Anything beyond that is a
thing the reader has to look up, which defeats the purpose.

This walks the AST rather than matching text, so the word "try" in a comment or
"lambda" in prose cannot trigger it.

Run:  python3 study/_build/vocabcheck.py
"""
import ast
import sys

BANNED_NODES = {
    ast.Lambda: "lambda (use def — that is what F0 W2 teaches)",
    ast.ListComp: "list comprehension",
    ast.SetComp: "set comprehension",
    ast.DictComp: "dict comprehension",
    ast.GeneratorExp: "generator expression",
    ast.IfExp: "ternary if/else",
    ast.Try: "try/except",
    ast.While: "while loop",
    ast.ClassDef: "class definition",
    ast.JoinedStr: "f-string",
}

# np.<name> that the Foundations track never introduces
BANNED_NP = {
    "c_", "r_", "eye", "sign", "meshgrid", "fliplr", "flipud", "diff", "sort",
    "argsort", "allclose", "isclose", "newaxis", "vectorize", "einsum",
    "apply_along_axis", "vstack", "hstack", "column_stack", "tile", "repeat",
}
BANNED_CALLS = {"float": "float() cast — codekit already tidies the printed value",
                "int": "int() cast — codekit already tidies the printed value",
                "sorted": "sorted() with a key",
                "map": "map()", "filter": "filter()", "zip": "zip()", "enumerate": "enumerate()"}
# np.linalg.<name>: only norm is taught (F0 W1, the vector-length lesson)
ALLOWED_LINALG = {"norm"}


def offences(src):
    out = []
    try:
        tree = ast.parse(src)
    except SyntaxError as e:
        return ["SyntaxError: %s" % e]
    for node in ast.walk(tree):
        for cls, label in BANNED_NODES.items():
            if isinstance(node, cls):
                out.append(label)
        if isinstance(node, ast.Attribute):
            # np.linalg.<x>
            if (isinstance(node.value, ast.Attribute) and node.value.attr == "linalg"
                    and node.attr not in ALLOWED_LINALG):
                out.append("np.linalg.%s" % node.attr)
            if (isinstance(node.value, ast.Name) and node.value.id == "np"
                    and node.attr in BANNED_NP):
                out.append("np.%s" % node.attr)
            if node.attr == "default_rng":
                out.append("np.random.default_rng")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in BANNED_CALLS:
                out.append(BANNED_CALLS[node.func.id])
        # x[:, None] — a None inside a subscript is np.newaxis
        if isinstance(node, ast.Subscript):
            for sub in ast.walk(node.slice):
                if isinstance(sub, ast.Constant) and sub.value is None:
                    out.append("[:, None] (np.newaxis)")
    return sorted(set(out))


def main():
    import content_code
    bad = {}
    for cid, src in content_code.CODE.items():
        o = offences(src)
        if o:
            bad[cid] = o
    print("%d snippets checked" % len(content_code.CODE))
    if not bad:
        print("PASS — every snippet stays inside what the Foundations track teaches")
        return 0
    print("FAIL — %d snippet(s) use something the reader has not been taught:" % len(bad))
    for cid, o in bad.items():
        print("   %-24s %s" % (cid, ", ".join(o)))
    return 1


if __name__ == "__main__":
    sys.exit(main())
