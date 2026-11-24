# -*- coding: utf-8 -*-
"""Quiz drills — every concept a mock quiz tests, practised four ways.

The mock quiz asks you to RECOGNISE the right statement among four. That is the
weakest form of knowing. This layer takes each quiz question's concept and makes
you use it with the same fixed set of four methods, every time:

    recall    retrieval from a blank page      (Roediger & Karpicke 2006)
    work      produce the numbers by hand      (generation effect)
    spot      find the step that is wrong      (error detection)
    transfer  use it somewhere the lesson didn't go  (elaborative interrogation)

The drills are rendered INSIDE the lesson page the quiz question points to, after
the lesson. They reuse the Active Mastery card grid and am.js, so there is no
second design system: masterykit.section builds every card.

Every card also carries "Say it three ways": a one-line summary, the way a
ten-year-old would think about it, and the terms in simple words. It sits behind
its own <details>, AFTER the answer, so it never gives the answer away first.

Keys:
  * a concept is keyed by the quiz qid, which is permanent; a card's id is
    "<qid>-<method>", which keys the done-state in localStorage. Append only.
  * the build refuses a concept missing any of the four methods, and a qid that
    no mock quiz defines.
"""
from masterykit import section, _det

METHODS = ("recall", "work", "spot", "transfer")

META = {
    "recall":   dict(kind="recall", ico="&#129504;", label="Recall",
                     why="Close the lesson. Pulling it out of memory is what makes it stay; "
                         "re-reading only makes it feel familiar.",
                     reveal="I have written it down &mdash; check me"),
    "work":     dict(kind="work it", ico="&#9999;&#65039;", label="Work it",
                     why="Pen and paper, real numbers. You do not own a formula until you have "
                         "pushed numbers through it yourself.",
                     reveal="show the working"),
    "spot":     dict(kind="spot the error", ico="&#128269;", label="Spot the error",
                     why="This working looks right and is not. Find the exact line that fails "
                         "<b>before</b> you open the answer &mdash; this is the skill a quiz "
                         "distractor tests.",
                     reveal="show me where it breaks"),
    "transfer": dict(kind="transfer", ico="&#128256;", label="Transfer",
                     why="A situation the lesson never showed. If the idea only works on the "
                         "lesson's own example, you have memorised the example, not the idea.",
                     reveal="compare with my answer"),
}


def M(hook, ask, answer, summary, kid, words):
    """One method on one concept.

    hook    : one line on the card face — what you will do
    ask     : the task (HTML)
    answer  : the reveal (HTML), hidden until you commit
    summary : the whole point in one plain sentence
    kid     : how a ten-year-old would think about it — no notation at all
    words   : [(term, what it means in simple words), ...]
    """
    assert hook and ask and answer and summary and kid and words
    return dict(hook=hook, ask=ask, answer=answer, summary=summary, kid=kid, words=words)


def D(qid, recall, work, spot, transfer):
    return dict(qid=qid, recall=recall, work=work, spot=spot, transfer=transfer)


def _three_ways(m):
    words = "".join('<tr><td class="qd-term">%s</td><td>%s</td></tr>' % w for w in m["words"])
    body = ('<div class="qd-3">'
            '<div class="qd-3-row qd-sum"><span class="qd-3-l">In one line</span>'
            '<p>%s</p></div>'
            '<div class="qd-3-row qd-kid"><span class="qd-3-l">Like you are ten</span>'
            '<p>%s</p></div>'
            '<div class="qd-3-row qd-words"><span class="qd-3-l">The words, in simple words</span>'
            '<table class="qd-wtab"><tbody>%s</tbody></table></div>'
            '</div>' % (m["summary"], m["kid"], words))
    return _det("Say it three ways", body, cls="am-rev qd-3w")


def cards(concepts, quiz_href):
    """concepts: [(qid, tag, drill_dict)] in quiz order. Returns card markup."""
    out = []
    for ci, (qid, tag, d) in enumerate(concepts, 1):
        title = tag[:1].upper() + tag[1:]
        for mi, key in enumerate(METHODS, 1):
            m, meta = d[key], META[key]
            body = ('<div class="qd-card">'
                    '<p class="qd-src">From <a href="%s#q-%s">quiz question %s</a> '
                    '&middot; <b>%s</b></p>'
                    '<p class="qd-why"><span class="am-tag">%s</span>%s</p>'
                    '<div class="am-ask qd-ask">%s</div>%s%s</div>'
                    % (quiz_href, qid, qid.split("-q")[-1].lstrip("0"), tag,
                       meta["label"], meta["why"], m["ask"],
                       _det(meta["reveal"], m["answer"]), _three_ways(m)))
            # card face: method label on top, the concept as the title. The
            # method colour and label carry "which method"; no emoji, no repeat.
            out.append(section(meta["label"], "", title,
                               "%s-%s" % (qid, key), body,
                               kind=meta["kind"], hook=m["hook"]))
    return out


def legend():
    """The four method colours, named. Colour is never the only signal: every
    card also prints its method in words."""
    return ('<span class="qd-legend">%s</span>' % "".join(
        '<span class="qd-key" data-kind="%s">%s</span>' % (META[k]["kind"], META[k]["label"])
        for k in METHODS))


def lede(concepts, quiz_href, quiz_label):
    names = ", ".join("<b>%s</b>" % t for _, t, _ in concepts)
    n = len(concepts)
    return ("%s from the <a href=\"%s\">%s</a> %s on this lesson: %s. "
            "Each one four ways &mdash; recall it, work it, spot the error, carry it "
            "somewhere new.%s" % (
                "One concept" if n == 1 else "%d concepts" % n, quiz_href, quiz_label,
                "rests" if n == 1 else "rest", names, legend()))
