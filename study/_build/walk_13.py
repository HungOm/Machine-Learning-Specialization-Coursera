# -*- coding: utf-8 -*-
"""Walkthrough for 13_agent_loop.py."""
from walkkit import p, expr, chain, chainset, steps, cases, values, point, ascii_art

PICTURE = ([
    ("in", "A task, in words", "&ldquo;what is 3*(4+5)&rdquo;"),
    ("arw", "the model writes a line of text saying what it wants to do"),
    ("loop", "repeat, up to a step budget", [
        ("op", "Think, and name an action", "<code>Action: calc(expr='3*(4+5)')</code>"),
        ("arw", "parse it &mdash; and this is where most failures happen"),
        ("op", "Validate", "Does that tool exist? Are the arguments right? Reject before "
                           "running anything."),
        ("arw", "run it, inside a try/except"),
        ("op", "Observe", "The result &mdash; <b>or the error</b>. An error is an "
                          "observation, not a crash."),
        ("back", "Feed it back in", "and let the model decide the next step."),
    ]),
    ("arw", "the model says Final:, or the budget runs out"),
    ("out", "An answer, or an honest failure",
     "&ldquo;I could not do this&rdquo; is a valid outcome and must be reachable."),
], "The whole program in one picture",
   "The loop itself is about fifteen lines. Everything else in this file is the guard rails, "
   "which is roughly the ratio in a real agent too.")

WALK = {

"prelude": (
    p("""An agent is a loop: <b>think, act, observe, repeat</b>. The loop is trivial. What
makes an agent work or fail is everything around it.""")
    + point("""This file has no language model in it. The &ldquo;planner&rdquo; is a scripted
stand-in, so the loop, the parsing and the failure modes can be examined without any
randomness. The failures shown here are the real ones.""")
),

"tools": (
    p("""Three tools, each with a name, a description, and a declared list of
arguments.""")
    + values([("calc", "evaluate an arithmetic expression", "args: <code>expr</code>"),
              ("convert", "convert one unit to another", "args: <code>value, frm, to</code>"),
              ("lookup", "look a term up in the notes", "args: <code>topic</code>")],
             "the tool registry")
    + point("""The <b>declared argument list</b> is the important part. It is what the
description shown to the model is built from, and it is what makes validation possible before
anything runs.""")
),

"validate": (
    p("""Check the call <b>before</b> executing it. Five ways a call can be wrong, each
caught with a specific message.""")
    + values([("calc {'expr': '2+2'}", "ok", ""),
              ("calc {}", "rejected", "missing argument(s): expr"),
              ("convert {'value': 'two', ...}", "rejected", "value should be float"),
              ("lookup {'topic': 'x', 'depth': 3}", "rejected", "unexpected argument(s): depth"),
              ("browse {'url': 'x'}", "rejected", "no such tool; available: calc, convert, lookup")],
             "validation results")
    + point("""Every message says <b>what was wrong</b> and, for the unknown tool, <b>what
was available</b>. That is deliberate: the message goes back to the model as an observation,
so it is a <b>prompt</b>, not a log line.""")
    + p("""&ldquo;no such tool 'browse'&rdquo; on its own invites another guess.
&ldquo;available: calc, convert, lookup&rdquo; lets the model recover on the next step. Error
text is part of the interface.""")
),

"run_tool": (
    p("""Now run it &mdash; with everything wrapped so that <b>nothing a tool does can kill
the loop</b>.""")
    + values([("calc 3*(4+5)", "27", "fine"),
              ("calc __import__('os')", "ERROR", "<b>blocked</b>: not allowed in an expression"),
              ("calc 1/0", "ERROR", "ZeroDivisionError, caught"),
              ("convert 2.5 km to m", "2500.0", "fine"),
              ("convert 1 km to kg", "ERROR", "no conversion from km to kg")],
             "the tool runner")
    + point("""The second row is the one that matters. A calculator that evaluates arbitrary
text is a <b>remote code execution hole</b> &mdash; and the input comes from a model, which
takes its input from a user. The expression is checked against an allowlist before
evaluation.""")
    + p("""Every other error becomes a <b>string</b>. Division by zero does not crash the
agent; it becomes an observation the model can read and respond to. That is the design rule
for the whole loop.""")
),

"parse": (
    p("""Reading the model's intention out of free text. This is where real agents break most
often.""")
    + values([("Thought: ... | Action: calc(expr='3*(4+5)')", "parsed", "the happy path"),
              ("Action: convert(value=2.5, frm='km', to='m')", "parsed", "three arguments"),
              ("I think the answer is 27.", "FAILED", "no Action: line"),
              ("Action: calc(3*(4+5))", "FAILED", "positional, not named"),
              ("Action: calc(expr='3*(4+5)'", "FAILED", "unclosed bracket")],
             "five inputs, three of them failures")
    + point("""<b>Three of the five fail</b>, and none of them is exotic. A model that
answers in prose instead of calling a tool, forgets to name its arguments, or drops a
bracket &mdash; these are the everyday failures, not the edge cases.""")
    + p("""Which is why modern APIs offer <b>structured tool calling</b>: the model emits
JSON against a schema and the parsing problem largely disappears. This file parses text to
show you what that feature is <b>for</b>.""")
),

"policy": (
    p("""The planner &mdash; the piece a real system replaces with a language model. Here it
is scripted, so the loop's behaviour is completely reproducible and every failure below is
deliberate rather than lucky.""")
),

"loop": (
    p("""The loop itself. Note how short the trace is.""")
    + ascii_art("""  task: what is 3*(4+5)
     step 1: Action: calc(expr='3*(4+5)')
             observation: 27
     step 2: Final: 27
     -> 27   (finished, 2 steps)""")
    + point("""Think, act, observe, repeat, stop. The observation from step 1 is what lets
step 2 finish &mdash; the model does not compute anything itself, it <b>reads the result of
the tool</b>.""")
    + p("""That is the whole mechanism. Everything that makes agents hard is in the guards
around this, not in the loop.""")
),

"guards": (
    p("""Four things that must not kill the agent, each demonstrated.""")
    + cases([("1 &middot; A tool that errors",
              "The error becomes an <b>observation</b>, not a crash. The agent reports it "
              "and stops cleanly."),
             ("2 &middot; A task it cannot progress on",
              "It must <b>give up</b>, not loop forever. A step budget makes that "
              "guaranteed rather than hopeful.")],
            "the two shown in the output")
    + point("""&ldquo;<b>I could not do this</b>&rdquo; has to be a <b>reachable</b> outcome.
An agent with no way to fail does not succeed more often &mdash; it just fails in a more
expensive and less legible way, usually by looping.""")
    + p("""A repeated-action check matters too: if the agent proposes the <b>same call
twice</b> and got the same observation, it is stuck. Nothing about the next iteration will
differ, so stopping is correct.""")
),

"budget": (
    p("""Finally, count what it cost. This is the number that decides whether an agent is
viable in production.""")
    + chain(["what is 3*(4+5)", "2 steps", "~12 tokens", "~$0.00004"],
            "one simple task, fully costed")
    + point("""Fractions of a penny here &mdash; but the loop sends <b>the whole growing
transcript</b> on every step. Costs rise <b>quadratically</b> with steps, not linearly,
because step 10 re-sends everything from steps 1 to 9.""")
    + p("""So a ten-step agent is not five times a two-step agent. It is more like twenty-five
times. That is why step budgets are a <b>cost control</b> as much as a safety measure, and
why compacting the transcript is one of the first optimisations any real agent needs.""")
),

"evaluate": (
    p("""The last experiment, and it isolates what the loop is actually <b>for</b>. Twelve
tasks, run twice.""")
    + chainset([([" observations fed back ", "solved 10 of 12"], "the normal loop"),
                ([" observations NOT fed back ", "solved <b>1</b> of 12"], "the same planner, blind")],
               "the only difference is whether the tool result comes back in")
    + point("""And the single task that still &ldquo;works&rdquo; blind is <b>&ldquo;write me
a poem about eigenvalues&rdquo;</b> &mdash; which works by <b>declining</b>. It needs no
tool, so there is nothing to feed back.""")
    + p("""Nothing that requires a tool completes, multi-step or not. Without the observation
the planner cannot tell it has <b>finished</b>, so it proposes the same action again, and the
repeat guard stops it.""")
    + point("""<b>The loop is not a refinement. It is the mechanism.</b> An agent is not a
model that calls a tool &mdash; it is a model that <b>reads the result</b>.""")
    + p("""The two failures are worth naming too: <i>&ldquo;remind me what entropy is&rdquo;</i>
and <i>&ldquo;take 3 days in hours and halve it&rdquo;</i>. Both need exactly the same tools as
tasks that pass &mdash; they are <b>phrasings</b> the scripted stub cannot recognise, not new
capabilities.""")
    + point("""That gap is precisely what a real language model buys you, and it is the
<b>only</b> thing it buys. Every tool, guard, validator, parser and budget above stays exactly
as it is.""")
),
}
