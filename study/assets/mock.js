/* Mock quizzes — marked in the browser.

   Same storage as the self-check questions and the problem sets
   (mls-quiz-v1), keyed 'M:<qid>' so the dashboard's weak-spot list can trace a
   missed question back to its lesson through META.mockLesson — exactly the way
   'P:<pid>' is traced through META.problemLesson.

   A missed question also pulls that lesson's cards forward to tomorrow, which
   is the same nudge quiz.js applies. Nothing is ever pushed further out. */
(function () {
  'use strict';
  var QKEY = 'mls-quiz-v1', SKEY = 'mls-srs-v1', MKEY = 'mls-mock-v1', DAY = 86400000;

  function rd(k) { try { return JSON.parse(localStorage.getItem(k) || '{}'); } catch (e) { return {}; } }
  function wr(k, o) { try { localStorage.setItem(k, JSON.stringify(o)); } catch (e) { } }

  function iso(d) {
    return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') +
           '-' + String(d.getDate()).padStart(2, '0');
  }
  var TOMORROW = iso(new Date(Date.now() + DAY));

  /* pull one lesson's cards forward; mirrors quiz.js nudge() */
  function nudge(file) {
    if (!window.META || !window.META.cardsByLesson) return 0;
    var ids = window.META.cardsByLesson[file] || [];
    if (!ids.length) return 0;
    var S;
    try { S = JSON.parse(localStorage.getItem(SKEY) || 'null'); } catch (e) { return 0; }
    if (!S || !S.cards) return 0;
    var moved = 0;
    ids.forEach(function (id) {
      var c = S.cards[id];
      if (!c || !c.reps) return;
      if (c.due > TOMORROW) { c.due = TOMORROW; c.nudged = true; moved++; }
    });
    if (moved) wr(SKEY, S);
    return moved;
  }

  function selected(li) {
    return Array.prototype.filter.call(
      li.querySelectorAll('ul.mq-opts input'), function (i) { return i.checked; });
  }

  document.addEventListener('DOMContentLoaded', function () {
    var list = document.querySelector('ol.mqlist');
    if (!list) return;
    var qs = Array.prototype.slice.call(list.querySelectorAll('li.mq'));
    var submit = document.getElementById('mq-submit');
    var retry = document.getElementById('mq-retry');
    var msg = document.getElementById('mq-msg');
    var scoreEl = document.getElementById('mq-score');
    var setId = list.dataset.set || '';

    function mark() {
      var unanswered = qs.filter(function (li) { return !selected(li).length; });
      if (unanswered.length) {
        msg.innerHTML = '<span class="mq-unanswered">' + unanswered.length +
          ' question' + (unanswered.length === 1 ? '' : 's') +
          ' still unanswered.</span> Answer every one — a guess you commit to is worth ' +
          'more than a blank, and the rationale will tell you why it was wrong.';
        unanswered[0].scrollIntoView({ behavior: 'smooth', block: 'center' });
        return;
      }

      var Q = rd(QKEY), right = 0, nudged = 0;
      qs.forEach(function (li) {
        var opts = Array.prototype.slice.call(li.querySelectorAll('ul.mq-opts > li'));
        var ok = true;
        opts.forEach(function (o) {
          var input = o.querySelector('input');
          var isRight = o.dataset.c === '1';
          o.classList.remove('ok', 'bad');
          if (isRight) o.classList.add('ok');
          if (input.checked && !isRight) { o.classList.add('bad'); ok = false; }
          if (!input.checked && isRight) ok = false;
          input.disabled = true;
        });
        li.classList.add('marked');
        li.classList.add(ok ? 'right' : 'wrong');
        if (ok) right++;
        Q['M:' + li.dataset.qid] = { r: ok ? 1 : 0, t: Date.now() };
        if (!ok && li.dataset.lesson) nudged += nudge(li.dataset.lesson);
      });
      wr(QKEY, Q);

      var pct = Math.round(right / qs.length * 100);
      scoreEl.textContent = right + ' / ' + qs.length;
      scoreEl.className = 'mq-score ' + (pct >= 80 ? 'pass' : 'fail');

      var M = rd(MKEY);
      M[setId] = { r: right, n: qs.length, t: Date.now() };
      wr(MKEY, M);

      var out = pct >= 80
        ? '<b>' + pct + '%.</b> That is a pass on the real thing (80% is the usual bar). '
        : '<b>' + pct + '%.</b> The real quiz needs 80%. ';
      out += 'Read the rationale under every option, including the ones you got right.';
      if (nudged) out += ' ' + nudged + ' card' + (nudged === 1 ? '' : 's') +
        ' pulled forward to tomorrow, and the misses are now on your dashboard.';
      msg.innerHTML = out;
      submit.hidden = true;
      retry.hidden = false;
    }

    function reset() {
      qs.forEach(function (li) {
        li.classList.remove('marked', 'right', 'wrong');
        Array.prototype.forEach.call(li.querySelectorAll('ul.mq-opts > li'), function (o) {
          o.classList.remove('ok', 'bad');
          var i = o.querySelector('input');
          i.disabled = false; i.checked = false;
        });
      });
      scoreEl.textContent = '—';
      scoreEl.className = 'mq-score';
      msg.textContent = '';
      submit.hidden = false;
      retry.hidden = true;
      list.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    submit.addEventListener('click', mark);
    retry.addEventListener('click', reset);

    /* show the last score for this set, if there is one */
    var prev = rd(MKEY)[setId];
    if (prev && msg) {
      msg.innerHTML = 'Last attempt: <b>' + prev.r + ' / ' + prev.n + '</b>. ' +
        'Answers are not kept — the questions start blank every time, on purpose.';
    }
  });
}());
