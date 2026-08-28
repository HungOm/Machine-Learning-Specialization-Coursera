"""An agent loop from scratch -- tools, parsing, and the ways it goes wrong.

Run me:  python3 13_agent_loop.py

An "agent" is a loop. A model proposes an action, something runs it, the result
goes back into the prompt, repeat until done. That is the whole architecture,
and it is worth building once because almost everything that goes wrong lives
in the plumbing rather than in the model.

There is NO language model here. The planner in this file is a deterministic
stub so the file runs anywhere and gives the same answer twice. Every line
around it -- the tool schemas, the validation, the parser, the loop guards, the
budget -- is exactly what you would keep when you swapped the stub for a real
model. That plumbing is the part you have to get right.
"""
import ast
import re

# %% SECTION: tools
# A tool is three things: a name, a declared shape for its arguments, and a
# function. The declared shape is not paperwork -- it is the only thing
# standing between a wrong guess and a stack trace in production.
SAFE_NODES = (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Constant,
              ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.Mod,
              ast.USub, ast.UAdd)

def calc(expr):
    """Arithmetic only. Parse to a syntax tree and refuse any node not on the
    list -- never hand a string from a model straight to eval()."""
    tree = ast.parse(expr, mode="eval")
    for node in ast.walk(tree):
        if not isinstance(node, SAFE_NODES):
            raise ValueError("not allowed in an expression: %s" % type(node).__name__)
        if isinstance(node, ast.Constant) and not isinstance(node.value, (int, float)):
            raise ValueError("only numbers")
    return eval(compile(tree, "<calc>", "eval"), {"__builtins__": {}}, {})

UNITS = {("km", "m"): 1000.0, ("m", "cm"): 100.0, ("hour", "minute"): 60.0,
         ("day", "hour"): 24.0, ("kg", "g"): 1000.0}

def convert(value, frm, to):
    """One hop only, on purpose: a tool that quietly chains conversions is a
    tool whose errors are impossible to attribute."""
    if (frm, to) in UNITS:
        return value * UNITS[(frm, to)]
    if (to, frm) in UNITS:
        return value / UNITS[(to, frm)]
    raise ValueError("no conversion from %s to %s" % (frm, to))

FACTS = {
    "entropy": "a measure of impurity; 0 when a node is pure, highest when classes are even",
    "learning rate": "the size of each gradient descent step; too large and the cost diverges",
    "regularisation": "a penalty on large weights that trades training fit for generalisation",
    "attention": "a weighted average of value vectors, weighted by query-key similarity",
}

def lookup(topic):
    key = topic.lower().strip()
    for k in FACTS:
        if k in key or key in k:
            return FACTS[k]
    raise KeyError("nothing on file about %r" % topic)

TOOLS = {
    "calc":    {"fn": calc,    "args": {"expr": str},
                "help": "evaluate an arithmetic expression, e.g. calc(expr='3*(4+5)')"},
    "convert": {"fn": convert, "args": {"value": float, "frm": str, "to": str},
                "help": "convert one unit to another, e.g. convert(value=2, frm='km', to='m')"},
    "lookup":  {"fn": lookup,  "args": {"topic": str},
                "help": "look a term up in the notes, e.g. lookup(topic='entropy')"},
}
for name, t in TOOLS.items():
    print("%-8s %-38s args %s" % (name, t["help"][:38], list(t["args"])))

# %% SECTION: validate
def validate(name, kwargs):
    """Check the call BEFORE running it, and return a message a model can act on.

    'unknown argument radius' is a repairable error. A traceback is not.
    """
    if name not in TOOLS:
        return "no such tool %r; available: %s" % (name, ", ".join(TOOLS))
    spec = TOOLS[name]["args"]
    missing = [k for k in spec if k not in kwargs]
    extra = [k for k in kwargs if k not in spec]
    if missing:
        return "%s is missing argument(s): %s" % (name, ", ".join(missing))
    if extra:
        return "%s got unexpected argument(s): %s" % (name, ", ".join(extra))
    for k, want in spec.items():
        try:
            kwargs[k] = want(kwargs[k])
        except (TypeError, ValueError):
            return "%s: argument %s should be %s, got %r" % (name, k, want.__name__, kwargs[k])
    return None

for name, kw in [("calc", {"expr": "2+2"}), ("calc", {}),
                 ("convert", {"value": "two", "frm": "km", "to": "m"}),
                 ("lookup", {"topic": "entropy", "depth": 3}),
                 ("browse", {"url": "x"})]:
    print("%-8s %-42s -> %s" % (name, str(kw), validate(name, dict(kw)) or "ok"))

# %% SECTION: run_tool
def run_tool(name, kwargs):
    """Every failure comes back as a STRING, never as an exception.

    An agent that crashes on a bad tool call has one bad step. An agent that is
    told what went wrong has a chance to fix it on the next one.
    """
    kwargs = dict(kwargs)
    problem = validate(name, kwargs)
    if problem:
        return "ERROR: " + problem
    try:
        return str(TOOLS[name]["fn"](**kwargs))
    except Exception as e:
        return "ERROR: %s: %s" % (type(e).__name__, e)

for name, kw in [("calc", {"expr": "3*(4+5)"}), ("calc", {"expr": "__import__('os')"}),
                 ("calc", {"expr": "1/0"}), ("convert", {"value": 2.5, "frm": "km", "to": "m"}),
                 ("convert", {"value": 1, "frm": "km", "to": "kg"}),
                 ("lookup", {"topic": "entropy"}), ("lookup", {"topic": "the offside rule"})]:
    print("%-8s %-34s -> %s" % (name, str(kw)[:34], run_tool(name, kw)[:64]))

# %% SECTION: parse
ACTION = re.compile(r"^Action:\s*(\w+)\((.*)\)\s*$", re.M)
KWARG = re.compile(r"(\w+)\s*=\s*(?:'([^']*)'|\"([^\"]*)\"|([^,]+))")

def parse_action(text):
    """Pull a tool call out of free text. This is the fragile joint.

    A real model returns prose with a call somewhere inside it, and the format
    is a request, not a guarantee. Parse strictly and report the failure --
    guessing at a malformed call is how agents take actions nobody asked for.
    """
    m = ACTION.search(text)
    if not m:
        return None, "no Action: line found"
    name, argstr = m.group(1), m.group(2)
    kwargs = {}
    for km in KWARG.finditer(argstr):
        val = next(v for v in km.groups()[1:] if v is not None)
        kwargs[km.group(1)] = val.strip()
    if argstr.strip() and not kwargs:
        return None, "could not read the arguments: %r" % argstr
    return (name, kwargs), None

for text in ["Thought: I should multiply.\nAction: calc(expr='3*(4+5)')",
             "Action: convert(value=2.5, frm='km', to='m')",
             "I think the answer is 27.",
             "Action: calc(3*(4+5))",
             "Action: calc(expr='3*(4+5)'"]:
    got, err = parse_action(text)
    print("%-46s -> %s" % (repr(text.replace("\n", " | "))[:46], got or "FAILED: " + err))

# %% SECTION: policy
# The stand-in for the model. Deterministic, and it can only see the task text
# and the observations so far -- exactly what a real model would see.
NUM = r"[-+]?\d*\.?\d+"

def policy(task, observations):
    """Return the next line the 'model' would emit."""
    t = task.lower()
    if "in words" in t or "what does" in t or "what is the meaning" in t:
        if not observations:
            term = t.split("does")[-1].split("mean")[0].strip(" ?") if "does" in t else t
            return "Thought: this is a definition.\nAction: lookup(topic='%s')" % term
        return "Final: %s" % observations[-1]
    # The \b at each end is not decoration. Without it the alternation matches
    # the "m" at the start of "minute" and cheerfully converts km to m -- a
    # wrong answer, silently, from a parser that looked fine in testing.
    m = re.search(r"(%s)\s*\b(km|m|kg|day|hour)\b\s+(?:in|to|into)\s+"
                  r"\b(m|cm|g|hour|minute)\b" % NUM, t)
    if m and not observations:
        return ("Thought: convert first.\n"
                "Action: convert(value=%s, frm='%s', to='%s')" % m.groups())
    if m and observations and "then" not in t:
        return "Final: %s" % observations[-1]
    if m and observations and "then" in t:
        tail = t.split("then")[-1]
        op = re.search(r"(times|divided by|plus|minus)\s+(%s)" % NUM, tail)
        if op and len(observations) == 1:
            sym = {"times": "*", "divided by": "/", "plus": "+", "minus": "-"}[op.group(1)]
            return ("Thought: now use the conversion result.\n"
                    "Action: calc(expr='%s %s %s')" % (observations[-1], sym, op.group(2)))
        return "Final: %s" % observations[-1]
    if re.search(r"[-+*/()]", t) and not observations:
        expr = re.search(r"([-+*/()\d\s.]{3,})", task)
        if expr:
            return "Thought: arithmetic.\nAction: calc(expr='%s')" % expr.group(1).strip()
    if observations:
        return "Final: %s" % observations[-1]
    return "Final: I do not know."

# %% SECTION: loop
def agent(task, max_steps=4, feed_observations=True, verbose=False):
    """think -> act -> observe -> repeat. Everything else is a guard rail."""
    observations, transcript, seen = [], [], []
    for step in range(max_steps):
        msg = policy(task, observations if feed_observations else [])
        transcript.append(msg)
        if verbose:
            print("   step %d: %s" % (step + 1, msg.replace("\n", " | ")))
        if msg.startswith("Final:"):
            return msg[6:].strip(), transcript, "finished"
        action, err = parse_action(msg)
        if err:
            observations.append("ERROR: " + err)
            continue
        if action in seen:                      # the no-progress guard
            return None, transcript, "looped: repeated %s" % action[0]
        seen.append(action)
        obs = run_tool(*action)
        observations.append(obs)
        if verbose:
            print("      observation: %s" % obs[:70])
    return None, transcript, "out of steps"

for task in ["what is 3*(4+5)", "convert 2.5 km in m",
             "convert 3 day in hour then divided by 4", "what does entropy mean"]:
    print("\ntask:", task)
    answer, tr, why = agent(task, verbose=True)
    print("   -> %s   (%s, %d steps)" % (answer, why, len(tr)))

# %% SECTION: guards
# Three failures, each caught by a different guard.
print("1. a tool that errors -- the error is an observation, not a crash")
ans, tr, why = agent("convert 1 km in minute", verbose=True)
print("    -> %r  (%s)" % (ans, why))
print("2. a task the planner cannot make progress on")
ans, tr, why = agent("write me a poem about eigenvalues")
print("    -> %r  (%s)" % (ans, why))
print("3. a planner that repeats itself -- caught before it burns the budget")

def stuck_policy(task, obs):
    return "Action: lookup(topic='entropy')"

_real = policy
policy = stuck_policy
ans, tr, why = agent("anything", max_steps=20)
policy = _real
print("    -> %r  (%s after %d steps, not 20)" % (ans, why, len(tr)))
print("Without that guard this is the classic runaway agent: a model that keeps")
print("choosing the same action, each step costing a full call.")

# %% SECTION: budget
def agent_costed(task, max_steps=4, price_per_1k=0.003):
    """Rough token accounting. The loop re-sends the whole transcript every
    step, so cost grows with the SQUARE of the number of steps, not linearly.
    This surprises people the first time the bill arrives."""
    observations, tokens, sent = [], 0, 0
    for step in range(max_steps):
        prompt = task + " ".join(observations)
        sent += len(prompt.split())
        msg = policy(task, observations)
        tokens += len(msg.split())
        if msg.startswith("Final:"):
            break
        action, err = parse_action(msg)
        if err:
            observations.append("ERROR: " + err)
            continue
        observations.append(run_tool(*action))
    total = sent + tokens
    return step + 1, total, total / 1000.0 * price_per_1k

for task in ["what is 3*(4+5)", "convert 3 day in hour then divided by 4"]:
    steps, tok, cost = agent_costed(task)
    print("%-42s %d steps, ~%d tokens, ~$%.5f" % (task, steps, tok, cost))
print("Now imagine 30 steps and a 4000-token system prompt resent every time.")
print("Step count is the cost driver, which is why 'let it keep trying' is an")
print("expensive default.")

# %% SECTION: evaluate
# The last two are in here on purpose: the stub planner cannot do them.
# A suite that only contains what you know works measures nothing.
DECLINE = "I do not know."
SUITE = [("what is 3*(4+5)", "27"),
         ("what is 100/4", "25.0"),
         ("convert 2.5 km in m", "2500.0"),
         ("convert 3 day in hour", "72.0"),
         ("convert 3 day in hour then divided by 4", "18.0"),
         ("convert 2 hour in minute then times 3", "360.0"),
         ("what does entropy mean", FACTS["entropy"]),
         ("what does attention mean", FACTS["attention"]),
         ("convert 1 km in minute", "ERROR"),
         ("write me a poem about eigenvalues", DECLINE),
         ("remind me what entropy is", FACTS["entropy"]),
         ("take 3 days in hours and halve it", "36.0")]

def solved(task, want, feed=True):
    got = str(agent(task, feed_observations=feed)[0]).strip()
    return got.startswith("ERROR") if want == "ERROR" else got == want

full = sum(solved(t, w) for t, w in SUITE)
blind = sum(solved(t, w, feed=False) for t, w in SUITE)
print("solved %d of %d with observations fed back" % (full, len(SUITE)))
print("solved %d of %d WITHOUT feeding observations back" % (blind, len(SUITE)))
survivors = [t for t, w in SUITE if solved(t, w, feed=False)]
print("the only thing that still works blind: %s" % (survivors or "nothing"))
print("\nAnd it 'works' by declining. Nothing that needs a tool completes,")
print("multi-step or not: without the observation the planner cannot tell it has")
print("finished, so it proposes the same action again and the repeat guard stops")
print("it. The loop is not a refinement here -- it is the mechanism.")
print("\nWhat the stub could not do:")
for task, want in SUITE:
    if not solved(task, want):
        print("   %-42s wanted %r" % (task, want[:34]))
print("Both are phrasings, not new capabilities -- 'remind me what X is' and")
print("'halve it' need the same two tools as the tasks that pass. That gap is")
print("exactly what a real model buys you, and it is the ONLY thing it buys:")
print("every tool, guard, validator and budget above stays exactly as written.")
print("\nIt also brings a failure the stub cannot have -- proposing a call that")
print("is well-formed, plausible, and wrong. That is what the validator, the")
print("repeat guard and the step budget are really defending against.")
