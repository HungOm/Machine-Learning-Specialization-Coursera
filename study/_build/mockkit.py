"""Helpers for the mock quizzes.

One mock quiz per week, in the shape the real graded quiz uses: single-answer
multiple choice and "select all that apply", marked in the browser, with a
rationale on EVERY option rather than only the right one. A distractor you
picked for a reason is worth more than the answer you got right, so the wrong
options carry the explanation of what they are actually describing.

Ids (`qid`) are permanent: they key your marks in localStorage, and a missed
question feeds the weak-spot list on the dashboard exactly as a missed problem
does. Append, never renumber.
"""
import html as _h  # noqa: F401


def O(text, correct, why):
    """One option: the text, whether it is right, and why — either way."""
    return dict(text=text, correct=bool(correct), why=why)


def Q(qid, ask, opts, lesson, tag="", note=None):
    """One quiz question.

    qid    : permanent id, e.g. "c2w3-q04"
    ask    : the question (HTML)
    opts   : [O(...), ...] — two or more; more than one correct makes it a
             "select all that apply", and the page says so
    lesson : the lesson file this tests, e.g. "c2/w3-04-bias-and-variance.html"
    tag    : short topic label, shown on the question
    note   : optional — one line after marking, about the idea rather than the
             option. Use it for the thing the question is really checking.
    """
    n_right = sum(1 for o in opts if o["correct"])
    assert n_right >= 1, "%s has no correct option" % qid
    assert len(opts) >= 2, "%s needs at least two options" % qid
    for o in opts:
        assert o["why"], "%s: every option needs a rationale" % qid
    return dict(qid=qid, ask=ask, opts=opts, lesson=lesson, tag=tag, note=note,
                multi=n_right > 1)


def SET(course, week, title, lede, questions):
    return dict(course=course, week=week, title=title, lede=lede,
                questions=questions)
