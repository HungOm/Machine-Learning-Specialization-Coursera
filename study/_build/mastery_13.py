# -*- coding: utf-8 -*-
"""Active Mastery for 13_agent_loop.py.

Depth note (brief §6): this file has almost no equations and NO arrays --
the state is three dicts and some strings. Its variable table is therefore
genuinely short, and says so rather than padding. The weight is in break /
debug and wrong mental models, exactly as the brief predicts.
"""
from masterykit import (section, prose, code, out, semantics, ledger, drill, peek,
                        predict, lab, breaks, invariant, wrong, reconstruct,
                        connections, recall, check)

AM = dict(
    lede="Eleven cards on the loop that is fifteen lines &mdash; and on the guard rails that "
         "are everything else.",
    sections=[

section("0", "&#129517;", "Before you run", "before", kind="orient",
    hook="No model, no randomness. Every failure here is deliberate.",
    body=prose("""<p>An agent is a loop: <b>think, act, observe, repeat</b>. The loop is
trivial. What makes an agent work or fail is everything around it.</p>
<p>There is <b>no language model in this file</b>. The planner is a scripted stand-in, so the
loop, the parsing and the failure modes can be examined without any randomness. Every failure
below is reproducible.</p>
<p><b>Watch for:</b> three of five parse attempts failing on entirely ordinary input; a
calculator that must refuse <code>__import__</code>; and the final experiment, which solves
<b>10 of 12</b> tasks with observations fed back and <b>1 of 12</b> without.</p>""")
    + connections([], [], "../gist/c33.html", "C3 Week 3 &mdash; the gist",
        extra=[("lab", "../scratch/11-retrieval.html", "File 11 first",
                "what feeds an agent its context, and what happens when it retrieves nothing")])),

section("1", "&#127991;&#65039;", "What every variable is", "vars", kind="semantics",
    hook="Five variables, no arrays, and no units anywhere. Honestly the thinnest table in the lane.",
    body=prose("""<p><b>This file has no numerical state.</b> There is no matrix, no vector and
no learned parameter &mdash; the entire model is three dictionaries and some regular
expressions. Padding this section with invented quantities would be worse than admitting
that, so here is the short honest version.</p>""")
    + semantics([
        ("TOOLS", "dict of 3", "the tool registry",
         "<b>Everything the agent can do.</b> Each entry is "
         "<code>{fn, args, help}</code> &mdash; the function, its declared argument names, and "
         "the description shown to the model.",
         "<i>none</i>",
         "<code>TOOLS['calc']['args']</code> is <code>['expr']</code>. That declared list is "
         "what makes validation possible <b>before</b> anything runs.",
         "Add a tool and the model can suddenly do a new thing &mdash; and can suddenly get a "
         "new thing wrong. The <code>help</code> string is a prompt, not documentation."),
        ("UNITS", "dict of 5", "the conversion table",
         "The pairs <code>convert</code> knows: km&rarr;m, m&rarr;cm, hour&rarr;minute and two "
         "more.",
         "<b>conversion factors</b>",
         "<code>UNITS[('km','m')]</code> is 1000.0. A pair not in the dict is an <b>error</b>, "
         "not a guess.",
         "This is the only place in the file with anything like a real unit &mdash; and the "
         "important behaviour is what happens for a pair it does <b>not</b> have."),
        ("FACTS", "dict of 4", "the tiny knowledge base",
         "What <code>lookup</code> can find: entropy, learning rate, regularisation, "
         "attention.",
         "<i>none</i>",
         "Four entries. A question about anything else returns a miss, which the agent must "
         "then <b>handle rather than crash on</b>.",
         "This is file 11's retrieval, reduced to a dict so the agent loop can be studied "
         "without it."),
        ("SAFE_NODES", "tuple of AST types", "the calculator's allowlist",
         "<b>Which Python syntax <code>calc</code> will evaluate.</b> Numbers, arithmetic, "
         "brackets &mdash; and nothing else.",
         "<i>none</i>",
         "It exists because the expression comes from a <b>model</b>, which takes its input "
         "from a <b>user</b>. <code>eval</code> on that path is a remote code execution hole.",
         "Widen it carelessly and you have built the vulnerability. This is the one place in "
         "the lane where a design choice is a security boundary."),
        ("SUITE", "list of 12", "the evaluation tasks",
         "Twelve tasks used to measure the loop, including two the scripted planner cannot "
         "phrase its way through.",
         "<i>none</i>",
         "10 of 12 solved with observations fed back; <b>1 of 12</b> without.",
         "That gap is the file's headline result and the reason the loop exists at all."),
    ],
    """Five entries, no shapes, no units. A file whose state is dictionaries genuinely has less
to say here than one whose state is a matrix, and the useful content has moved to sections 4
and 6."""),
    ),

section("2", "&#128302;", "Prediction checkpoints", "predict", kind="predict",
    hook="Four, and the first is about how often ordinary input fails to parse.",
    body=predict([
        ("""Five model outputs are fed to <code>parse_action</code>. <b>Predict how many
fail</b>, and whether the failures look exotic.""",
         """<p><b>Three of five fail</b>, and none of them is exotic.</p>
<p>A model answering in <b>prose</b> instead of calling a tool; one using a <b>positional</b>
argument (<code>calc(3*(4+5))</code>) instead of a named one; and one dropping a <b>closing
bracket</b>. These are the everyday failures, not the edge cases.</p>
<p>Which is exactly why modern APIs offer <b>structured tool calling</b> &mdash; the model
emits JSON against a schema and the parsing problem largely disappears. This file parses text
to show you what that feature is <i>for</i>.</p>"""),
        ("""<code>calc</code> is asked to evaluate <code>__import__('os')</code>. <b>Predict
what it returns</b> &mdash; a result, an error, or a crash.""",
         """<p>An <b>error string</b>: <code>ValueError: not allowed in an expression</code>,
caught and returned as an observation.</p>
<p>Not a crash, and certainly not a result. The expression came from a model, which takes its
input from a user, so a bare <code>eval</code> here is a remote code execution hole. The
allowlist is the boundary.</p>
<p>Note the <b>shape</b> of the answer: even a security refusal is returned as an observation
the loop can carry on from.</p>"""),
        ("""A tool raises <code>ZeroDivisionError</code> mid-run. <b>Predict what the loop
does.</b>""",
         """<p>It <b>continues</b>. The error becomes a string observation &mdash;
<code>ERROR: ZeroDivisionError: division by zero</code> &mdash; and the planner gets to read
it and decide what to do next.</p>
<p>That is the design rule for the whole file: <b>nothing a tool does may kill the loop.</b>
An agent that crashes on a bad tool call cannot recover from anything, and bad tool calls are
the normal case.</p>"""),
        ("""The final experiment runs 12 tasks twice: once with observations fed back, once
without. <b>Predict both scores.</b>""",
         """<p><b>10 of 12</b> with, <b>1 of 12</b> without.</p>
<p>And the single task that still &ldquo;works&rdquo; blind is <i>&ldquo;write me a poem about
eigenvalues&rdquo;</i> &mdash; which works by <b>declining</b>. It needs no tool, so there is
nothing to feed back.</p>
<p>Nothing requiring a tool completes. Without the observation the planner cannot tell it has
<b>finished</b>, so it proposes the same action again and the repeat guard stops it.</p>"""),
    ],
    """The last one is the file's whole argument: the loop is not a refinement, it is the
mechanism.""")),

section("3", "&#128295;", "Modify the copy", "lab", kind="lab",
    hook="Five, including the one that turns a helpful message into a useless one.",
    body=lab([
        ("L1", "Change a value",
         "Remove <code>'available: ...'</code> from the unknown-tool error and re-run the "
         "validation block.",
         'return f"no such tool {name!r}"        # was: ...; available: {", ".join(TOOLS)}',
         """<p>The message still tells you what went wrong and <b>no longer tells the model how
to recover</b>. &ldquo;no such tool 'browse'&rdquo; invites another guess; the original also
lists <code>calc, convert, lookup</code>.</p>
<p>The point: in an agent, <b>error text is a prompt, not a log line</b>. It goes back into the
model's context, so it is part of the interface and should be written for a reader who can act
on it.</p>"""),
        ("L2", "Change a parameter",
         "Cut the step budget to <b>1</b> and run the arithmetic task.",
         "run(task, max_steps=1)",
         """<p>It fails &mdash; the task needs <b>two</b> steps: one to call <code>calc</code>
and one to read the observation and answer.</p>
<p>Worth noticing that it fails <b>cleanly</b>, reporting that it ran out of steps rather than
hanging or inventing an answer. A budget is a correctness feature as much as a cost one: it
converts &ldquo;might loop forever&rdquo; into a guaranteed, legible outcome.</p>"""),
        ("L3", "Change the data",
         "Add a fifth entry to <code>UNITS</code> for <code>('minute','second')</code> and ask "
         "for a two-hop conversion: hours to seconds.",
         "UNITS[('minute', 'second')] = 60.0",
         """<p>It still <b>fails</b>. <code>convert</code> looks up a single pair; there is no
chaining, so <code>('hour','second')</code> is simply absent.</p>
<p>Which is the interesting part: adding data did not add a capability. The agent can now do
minutes&rarr;seconds, but multi-hop conversion needs either a new entry or a <b>planner that
calls convert twice</b> &mdash; and whether it does is a property of the model, not of the
tool.</p>"""),
        ("L4", "Change an assumption",
         "Remove the repeated-action guard and run the task the planner cannot make progress "
         "on.",
         "# if action == last_action and obs == last_obs: stop",
         """<p>It loops until the step budget stops it, <b>re-sending the whole transcript
every time</b>.</p>
<p>So the failure is not just slow &mdash; it is <b>quadratically expensive</b>, because step
10 re-sends everything from steps 1&ndash;9. Without a budget it would run until something
else stopped it.</p>
<p>The invariant: <b>if the same action returns the same observation, nothing about the next
iteration will differ.</b> Stopping is correct, and detecting it is two variables.</p>"""),
        ("L5", "Explain it",
         "Explain why validation happens <b>before</b> <code>run_tool</code> rather than "
         "catching the error afterwards.",
         None,
         """<p>Because some failures should never execute. <code>calc</code> with a malicious
expression, or a tool name that does not exist, should be refused <b>without running
anything</b> &mdash; the allowlist is a boundary, not an error handler.</p>
<p>And the messages differ in kind: validation can say <b>exactly what was wrong</b> with the
call (&ldquo;missing argument: expr&rdquo;, &ldquo;value should be float&rdquo;), whereas a
caught exception can only report what the tool happened to raise.</p>
<p>Validate what you can check <b>statically</b>; catch what you cannot.</p>"""),
    ],
    """L3 is the one that changes how you think about tools: adding data is not the same as
adding a capability.""")),

section("4", "&#128165;", "Break it, then repair it", "break", kind="debug",
    hook="Five, and this is where this file's weight is.",
    body=breaks([
        ("SAFE_NODES = SAFE_NODES + (ast.Call, ast.Name, ast.Attribute)",
         "Widen the calculator's allowlist to permit function calls. <b>Predict what "
         "<code>__import__('os').system('...')</code> now does.</b>",
         """<p>It <b>executes</b>. You have built a remote code execution vulnerability, in one
line that looks like a feature request (&ldquo;let users call sqrt&rdquo;).</p>
<p>The path is worth stating plainly: a <b>user</b> writes a prompt, a <b>model</b> emits an
expression, and your code <b>evaluates</b> it. Every link in that chain is untrusted.</p>
<p>The invariant: <b>an allowlist must enumerate what is permitted, never what is
forbidden.</b> If you need sqrt, add a <code>sqrt</code> <b>tool</b> &mdash; do not widen the
evaluator.</p>"""),
        ("def run_tool(name, kwargs):\n    return TOOLS[name]['fn'](**kwargs)      # no try/except",
         "Remove the exception handling from the tool runner and ask for an impossible "
         "conversion.",
         """<p>The <code>ValueError</code> propagates out of the loop and <b>kills the
agent</b>. One bad tool call ends the session.</p>
<p>Which is fatal in practice, because bad tool calls are the <b>normal case</b> &mdash; the
model guesses arguments, mistypes units and asks for things that do not exist, constantly.</p>
<p>The invariant: <b>every tool error must become an observation.</b> The agent's ability to
recover depends entirely on the error reaching the planner as text rather than reaching the
process as an exception.</p>"""),
        ("ACTION = re.compile(r'Action:\\s*(\\w+)\\((.*)\\)')      # the ^...$ and re.M are gone",
         "Loosen the action regex so it matches anywhere in the text. Predict what breaks.",
         """<p>It now matches inside the model's <b>reasoning</b> &mdash; a line like
&ldquo;I could use Action: calc(...) but instead&hellip;&rdquo; is parsed as a real tool
call.</p>
<p>The agent executes something the model was only <b>considering</b>. No error, plausible
behaviour, and a genuinely wrong action taken.</p>
<p>The invariant: <b>the action must be anchored to its own line</b>. The distinction between
&ldquo;thinking about doing X&rdquo; and &ldquo;doing X&rdquo; is carried entirely by that
anchor.</p>"""),
        ("obs = run_tool(name, kwargs)\n# transcript.append(obs)   <- never fed back",
         "Run the tool but do not put the observation into the transcript. Predict the "
         "success rate.",
         """<p><b>1 of 12</b>, down from 10 &mdash; and the one that survives does so by
<b>declining</b> a task that needed no tool.</p>
<p>Nothing that requires a tool completes, multi-step or not. Without the observation the
planner cannot tell it has <b>finished</b>, so it proposes the same action again and the
repeat guard stops it.</p>
<p>The invariant, and it is the file's whole thesis: <b>an agent is not a model that calls a
tool. It is a model that reads the result.</b></p>"""),
        ("kwargs = {k: v for k, v in raw.items()}        # every value stays a string",
         "Skip the type coercion in <code>validate</code> and call "
         "<code>convert(value='2.5', ...)</code>.",
         """<p><code>'2.5' * 1000.0</code> raises a <code>TypeError</code> inside the tool
&mdash; which the try/except catches, so the agent survives and reports a confusing message
about types.</p>
<p>The model then has to guess what it did wrong from an error about Python types rather than
about its call. It usually retries identically.</p>
<p>The invariant: <b>coerce and validate at the boundary</b>, where you can say
&ldquo;argument <code>value</code> should be a float&rdquo;. An error from deep inside a tool
is far less actionable than one from the validator.</p>"""),
    ],
    """Five breaks, and the first is a security bug. This is the file where a careless
&ldquo;small improvement&rdquo; is genuinely dangerous.""")),

section("5", "&#9878;&#65039;", "The invariant", "invariant", kind="invariant",
    hook="Nothing a tool does may kill the loop — and the loop must be able to give up.",
    body=invariant("""<p><b>Every tool failure becomes an observation, every action is
validated before it runs, and the loop always terminates.</b></p>""",
    """<p>The three together are what make an agent operable. A tool that raises kills the
session; an action that runs before validation can execute something dangerous; and a loop
without a budget can run until your bill stops it.</p>
<p>The termination clause deserves the most attention, because &ldquo;<b>I could not do
this</b>&rdquo; has to be a <b>reachable outcome</b>. An agent with no way to fail does not
succeed more often &mdash; it fails more expensively, usually by looping while re-sending its
whole transcript.</p>
<p>Which is also why the cost is quadratic rather than linear in steps: step 10 re-sends
everything from steps 1&ndash;9. A ten-step agent is not five times a two-step agent, it is
nearer twenty-five.</p>""",
    """for name, kwargs in every_proposed_call:
    err = validate(name, kwargs)
    assert err is None or isinstance(err, str)      # refuse, never raise
    if err is None:
        obs = run_tool(name, kwargs)
        assert isinstance(obs, str)                 # even failures are text
assert steps <= max_steps                           # always terminates""")),

section("6", "&#129535;", "Wrong mental models", "wrong", kind="myths",
    hook="Five, and the first is what people mean when they say “agent”.",
    body=wrong([
        ("An agent is a model that can call tools.",
         """<p>It is a model that <b>reads the result</b>. The file measures exactly this:
<b>10 of 12</b> tasks solved with observations fed back, <b>1 of 12</b> without &mdash; and
that one works by declining.</p>
<p>Calling a tool and never seeing its output is not a degraded agent, it is not an agent. The
loop is the mechanism, not a refinement.</p>"""),
        ("Error messages are for the logs.",
         """<p>They go back into the model's <b>context</b>, so they are prompts. &ldquo;no such
tool 'browse'&rdquo; invites another guess; &ldquo;no such tool 'browse'; available: calc,
convert, lookup&rdquo; lets the model recover on the next step.</p>
<p>Error text in an agent is part of the interface and should be written for a reader who can
act on it.</p>"""),
        ("Parsing failures are edge cases.",
         """<p><b>Three of five</b> ordinary model outputs fail to parse in this file: prose
instead of a call, a positional argument, a missing bracket.</p>
<p>That is the everyday case, and it is why structured tool calling exists. If you are parsing
free text, budget for it failing most of the time.</p>"""),
        ("A step budget is a cost control.",
         """<p>It is also a <b>correctness</b> feature. Without it, a task the planner cannot
progress on loops indefinitely, and the loop re-sends the entire transcript each time &mdash;
so cost grows <b>quadratically</b> with steps, not linearly.</p>
<p>The budget converts &ldquo;might run forever&rdquo; into a legible, bounded failure that
the caller can handle.</p>"""),
        ("Swapping in a real language model would fix the two failing tasks.",
         """<p>It would &mdash; and that is <b>all</b> it would change. The two failures are
<i>&ldquo;remind me what entropy is&rdquo;</i> and <i>&ldquo;take 3 days in hours and halve
it&rdquo;</i>, and both need <b>exactly the same tools</b> as tasks that already pass. They are
<b>phrasings</b> the scripted planner cannot recognise, not missing capabilities.</p>
<p>Every tool, guard, validator, parser and budget in this file stays exactly as it is. The
model replaces one function.</p>"""),
    ])),

section("7", "&#127959;&#65039;", "Reconstruction challenge", "reconstruct", kind="rebuild",
    hook="Rebuild the loop, then prove it survives a hostile tool.",
    body=reconstruct([
        ("Explain", "In four sentences, describe the loop and name the four things that can "
         "stop it.",
         """<p>Ask the planner what to do; parse a tool name and arguments from its reply;
validate and run that tool; put the result back into the transcript and ask again.</p>
<p>It stops when the planner says it is finished, when the step budget runs out, when the same
action returns the same observation twice, or when parsing fails and cannot be
recovered.</p>"""),
        ("Skeleton", "Write the five signatures from memory.",
         """<p><code>calc(expr)</code>, <code>convert(value, frm, to)</code>,
<code>lookup(topic)</code>, <code>validate(name, kwargs)</code> returning an error string or
None, <code>run_tool(name, kwargs)</code>, and <code>parse_action(text)</code>.</p>
<p>The important shape: <code>validate</code> <b>returns</b> an error rather than raising one,
because that error is destined for the model's context.</p>"""),
        ("Core", "Write validate from memory. Five distinct failures.",
         """<p>Unknown tool &mdash; and <b>list the available ones</b>. Missing required
argument, named. Unexpected argument, named. Wrong type, saying which argument and what type
was wanted. And a value that fails a domain check, such as an unknown unit pair.</p>
<p>Each message must say what was wrong <b>and</b> what would be right. That is the difference
between a message and a prompt.</p>"""),
        ("Minimal", "Build the smallest agent that can fail safely: one tool, one guard.",
         """<p>One tool that raises, a try/except turning that into a string, and a step
budget. That is enough to demonstrate the whole discipline &mdash; the agent survives the
error, reports it, and stops.</p>
<p>Then check the thing people forget: does your loop have a way to return <b>&ldquo;I could
not do this&rdquo;</b>? If not, it cannot fail, which means it will loop.</p>"""),
        ("Verify", "Check your rebuild without comparing to the original.",
         """<p>Three assertions: a tool that raises never propagates out of the loop; an
invalid call is refused <b>without executing</b>; and the step count never exceeds the
budget.</p>
<p>Then the real test &mdash; run your suite <b>without feeding observations back</b>. If the
success rate does not collapse, your tasks are not actually using the tools, and your
evaluation is measuring nothing.</p>"""),
    ],
    """That last verification is the one worth stealing: the no-feedback run is a control that
tells you whether your agent evaluation has any content.""")),

section("8", "&#128279;", "Connections", "conn", kind="links",
    hook="Retrieval feeds it, RL shares its shape, MLOps deploys it.",
    body=connections(
        [("lab", "../scratch/11-retrieval.html", "Back to 11",
          "what fills an agent's context &mdash; and the abstain rule it needs"),
         ("lab", "../scratch/10-reinforcement-learning.html", "Back to 10",
          "the same act-observe-repeat shape, with a value function choosing instead of a model")],
        [("lab", "../scratch/14-mlops.html", "On to 14",
          "what it takes to run any of this in production and notice when it breaks")],
        "../gist/c33.html", "C3 Week 3 &mdash; the gist",
        extra=[("docs", "../reference.html", "Reference sheet",
                "the retrieval and RL entries this file sits between")])),

section("9", "&#9670;", "Recall sheet", "recall", kind="recall",
    hook="Six cards, all measured results.",
    body=recall([
        ("Observations fed back vs not: what are the two scores?",
         "<b>10 of 12</b> and <b>1 of 12</b>. The one that survives works by <b>declining</b> "
         "a task needing no tool. An agent is a model that <b>reads the result</b>, not one "
         "that calls a tool."),
        ("Of five ordinary model outputs, how many fail to parse, and how?",
         "<b>Three</b>: prose instead of a call, a <b>positional</b> argument, and a missing "
         "bracket. All everyday, which is why structured tool calling exists."),
        ("Why must <code>calc</code> use an allowlist rather than blocking dangerous strings?",
         "Because the expression comes from a <b>model</b>, which takes input from a "
         "<b>user</b>. An allowlist enumerates what is <b>permitted</b>; a blocklist can always "
         "be worked around. Widening it to allow calls is a remote code execution hole."),
        ("What must happen to a tool that raises an exception?",
         "It becomes an <b>observation</b> &mdash; a string the planner reads &mdash; never an "
         "exception that escapes the loop. Bad tool calls are the normal case, so an agent "
         "that crashes on one cannot recover from anything."),
        ("Why does agent cost grow <b>quadratically</b> with steps?",
         "Because the loop re-sends the <b>whole growing transcript</b> every step &mdash; step "
         "10 re-sends steps 1&ndash;9. A ten-step agent is nearer twenty-five times a two-step "
         "one, not five."),
        ("The two tasks the stub cannot do. What would a real model change?",
         "Only those two. Both need <b>the same tools</b> as tasks that pass &mdash; they are "
         "<b>phrasings</b>, not missing capabilities. Every tool, guard, validator and budget "
         "stays exactly as it is."),
    ],
    """Cover and answer aloud.""")),

section("10", "&#9989;", "Mastery check", "check", kind="check",
    hook="Five, and the first is a security question.",
    body=check([
        ("""A teammate wants users to be able to call <code>sqrt</code> in the calculator and
proposes adding <code>ast.Call</code> to the allowlist. Respond.""",
         """<p><b>No.</b> Permitting calls permits <code>__import__('os').system(...)</code>,
and the expression arrives from a model that takes its input from a user. That one line is a
remote code execution hole dressed as a feature.</p>
<p>The right fix is a <b>sqrt tool</b>, validated like every other. An allowlist enumerates
what is permitted; widening it to cover a use case is how these vulnerabilities are actually
introduced.</p>"""),
        ("""Your agent hangs on some tasks and your bill is far higher than expected. Name the
two missing guards and why the cost is worse than linear.""",
         """<p>A <b>step budget</b> and a <b>repeated-action check</b>. Without them, a task
the planner cannot progress on loops indefinitely.</p>
<p>Cost is <b>quadratic</b> because the transcript is re-sent every step &mdash; step 10
includes steps 1&ndash;9. So a runaway loop does not cost linearly more, it compounds.</p>"""),
        ("""Your agent's success rate is 85%. Describe the one control run that tells you
whether that number means anything.""",
         """<p>Run the same suite <b>without feeding observations back</b>. If the score barely
moves, your tasks are not actually using the tools and the evaluation is measuring the
planner's priors, not the agent.</p>
<p>This file's control drops from <b>10/12 to 1/12</b>, which is what a meaningful agent
benchmark looks like.</p>"""),
        ("""Rewrite this error to be useful to a model: <code>"invalid input"</code>.""",
         """<p>Something like: <b>&ldquo;convert: argument <code>value</code> should be a
number, got '2.5' as text. Expected: convert(value=float, frm=str, to=str). Known unit pairs:
km&rarr;m, m&rarr;cm, hour&rarr;minute&hellip;&rdquo;</b></p>
<p>Name <b>which</b> argument, <b>what</b> was wrong, and <b>what would be right</b>. The
message goes back into the context, so it is a prompt &mdash; and &ldquo;invalid input&rdquo;
gives the model nothing to act on, so it retries identically.</p>"""),
        ("""Someone says swapping in GPT would make this a real agent. What is right and wrong
about that?""",
         """<p><b>Right</b> that it fixes the two failing tasks, which are phrasing problems
rather than capability gaps. <b>Wrong</b> that it changes anything else.</p>
<p>The tools, the validator, the parser, the try/except, the repeat guard and the step budget
all stay exactly as they are &mdash; and they are the parts that decide whether the thing is
operable. The model replaces one function.</p>"""),
    ],
    """These four files have no mock quiz. The thing not to repeat is the walkthrough above,
which explains what each block does &mdash; where this asks you to break it and say what the
failure teaches.""")),
    ],
)
