/* The mastery checklist.
   Evaluates each week's five conditions against what you have actually done —
   lessons marked read, problems graded, labs marked done, card intervals — so
   "done" is a measurement rather than a feeling. */
(function () {
  'use strict';
  var PKEY = 'mls-study-progress-v1', SKEY = 'mls-srs-v1', QKEY = 'mls-quiz-v1';
  var MATURE = 21, PROB_BAR = 0.8, CARD_BAR = 0.7;

  function rd(k) { try { return JSON.parse(localStorage.getItem(k) || '{}'); } catch (e) { return {}; } }
  function pct(a, b) { return b ? Math.round(100 * a / b) : 0; }

  function weekKey(c, w) { return c.toLowerCase() + w; }

  function evaluate(wk, done, S, Q) {
    var M = window.META, cards = S.cards || {};
    var key = weekKey(wk.c, wk.w);

    var lessons = M.lessons.filter(function (L) { return L.c === wk.c && L.w === wk.w; });
    var readN = lessons.filter(function (L) { return done[L.s]; }).length;

    var pids = (M.problemsByWeek || {})[key] || [];
    var graded = pids.filter(function (p) { return Q['P:' + p]; });
    var solved = pids.filter(function (p) { return Q['P:' + p] && Q['P:' + p].r === 1; });

    var labs = (M.labs || []).filter(function (l) { return l.c === wk.c && l.w === wk.w; });
    var labsDone = labs.filter(function (l) { return done[l.s]; }).length;

    var files = {};
    lessons.forEach(function (L) { files[L.f] = 1; });
    var ids = [];
    Object.keys(M.cardsByLesson).forEach(function (f) {
      if (files[f]) ids = ids.concat(M.cardsByLesson[f]);
    });
    var mature = ids.filter(function (i) {
      var c = cards[i]; return c && c.reps && c.ivl >= MATURE;
    }).length;

    var probSet = (M.problems || []).filter(function (p) { return p.c === wk.c && p.w === wk.w; });
    var scratchDone = (M.scratch || []).filter(function (s) { return done[s.s]; }).length;

    return {
      key: key,
      read:   { got: readN, need: lessons.length, ok: lessons.length > 0 && readN === lessons.length },
      probs:  { got: solved.length, need: pids.length, graded: graded.length,
                ok: pids.length > 0 && solved.length >= Math.ceil(pids.length * PROB_BAR) },
      labs:   { got: labsDone, need: labs.length, ok: labs.length === 0 || labsDone === labs.length },
      cards:  { got: mature, need: ids.length,
                ok: ids.length === 0 || mature >= Math.ceil(ids.length * CARD_BAR) },
      probSet: probSet[0] || null,
      scratchDone: scratchDone
    };
  }

  function bar(got, need, ok) {
    return '<span class="mb ' + (ok ? '' : 'bad') + '"><i style="width:' + pct(got, need) + '%"></i></span>' +
           '<span class="mn">' + got + '/' + need + '</span>';
  }

  function row(label, r, hint) {
    return '<tr class="' + (r.ok ? 'met' : '') + '"><td class="mk">' + (r.ok ? '&#10003;' : '&#9675;') +
      '</td><td>' + label + '</td><td>' + bar(r.got, r.need, r.ok) + '</td>' +
      '<td class="mh">' + (r.ok ? 'met' : hint) + '</td></tr>';
  }

  document.addEventListener('DOMContentLoaded', function () {
    var host = document.getElementById('mastery-weeks');
    if (!host || !window.META) return;
    var done = rd(PKEY), S = rd(SKEY), Q = rd(QKEY);
    var out = [], metCount = 0;

    window.META.weeks.forEach(function (wk) {
      var e = evaluate(wk, done, S, Q);
      var four = [e.read.ok, e.probs.ok, e.labs.ok, e.cards.ok];
      var n = four.filter(Boolean).length;
      if (n === 4) metCount++;
      var g = (window.MASTERY_WEEKS || {})[e.key] || {};
      out.push(
        '<section class="mweek' + (n === 4 ? ' all' : '') + '">' +
        '<header><span class="mw-n">' + wk.c + ' W' + wk.w + '</span>' +
        '<h3>' + wk.t + '</h3>' +
        '<span class="mw-c">' + n + ' of 4 checked</span></header>' +
        '<div class="mw-guide">' +
          '<p><span class="lbl">what makes it hard</span>' + (g.hard || '') + '</p>' +
          '<p><span class="lbl">the one thing to get right</span>' + (g.one || '') + '</p>' +
          '<p><span class="lbl">what you can skim</span>' + (g.skip || '') + '</p>' +
        '</div>' +
        '<table class="mtab"><tbody>' +
          row('Read every lesson', e.read, 'mark them done as you finish') +
          row('Solve 80% of the problems unaided', e.probs,
              e.probs.graded ? 'keep going — ' + e.probs.graded + ' graded so far'
                             : 'not started' + (e.probSet ? '' : ' (no set for this week)')) +
          row('Finish the labs', e.labs, e.labs.need ? 'open the companion first' : 'none this week') +
          row('70% of the cards at 21 days or more', e.cards,
              'this one needs calendar time, not effort') +
        '</tbody></table>' +
        '<div class="mw-last"><span class="lbl">&#9998; and then, only you can check</span>' +
        'Fill the <a href="paper.html#sheets">' + wk.c + ' W' + wk.w + ' sheet</a> from a blank page, ' +
        'and say the one-line version of this week out loud without looking.</div>' +
        '</section>');
    });
    host.innerHTML = out.join('');

    var head = document.getElementById('mastery-head');
    if (head) {
      head.innerHTML =
        '<div class="tiles">' +
        '<div class="tile"><span class="tl">weeks fully checked</span><b>' + metCount + ' / 12</b>' +
        '<span class="ts">all four measurable conditions met</span>' +
        '<span class="tbar"><i style="width:' + pct(metCount, 12) + '%"></i></span></div>' +
        '</div>';
    }
  });
})();
