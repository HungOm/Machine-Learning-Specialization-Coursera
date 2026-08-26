/* Self-check questions feed the review schedule.
   Miss a question and every card belonging to that lesson gets pulled forward
   to tomorrow — so the system finds your weak spots instead of you having to.
   Nothing is ever pushed further out from here; only pulled in. */
(function () {
  'use strict';
  var QKEY = 'mls-quiz-v1', SKEY = 'mls-srs-v1', DAY = 86400000;

  function readQ() { try { return JSON.parse(localStorage.getItem(QKEY) || '{}'); } catch (e) { return {}; } }
  function writeQ(o) { try { localStorage.setItem(QKEY, JSON.stringify(o)); } catch (e) { } }

  function iso(d) {
    return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') +
           '-' + String(d.getDate()).padStart(2, '0');
  }
  var TOMORROW = iso(new Date(Date.now() + DAY));

  /* pull this lesson's cards forward; returns how many actually moved */
  function nudge(file) {
    if (!window.META || !window.META.cardsByLesson) return 0;
    var ids = window.META.cardsByLesson[file] || [];
    if (!ids.length) return 0;
    var S;
    try { S = JSON.parse(localStorage.getItem(SKEY) || 'null'); } catch (e) { return 0; }
    if (!S || !S.cards) return 0;               /* deck never started — nothing to reschedule */
    var moved = 0;
    ids.forEach(function (id) {
      var c = S.cards[id];
      if (!c || !c.reps) return;                /* untouched card: leave it to the new-card queue */
      if (c.due > TOMORROW) { c.due = TOMORROW; c.nudged = true; moved++; }
    });
    if (moved) { try { localStorage.setItem(SKEY, JSON.stringify(S)); } catch (e) { } }
    return moved;
  }

  document.addEventListener('DOMContentLoaded', function () {
    wireQuiz();
    wireProblems();
  });

  /* ---------------- problem sets: same grading, one bar per problem ------- */
  function wireProblems() {
    var probs = document.querySelectorAll('article.prob[data-pid]');
    if (!probs.length) return;
    var store = readQ();
    var lessonOf = {};
    (window.META && window.META.lessons || []).forEach(function (L) { lessonOf[L.f] = L; });

    probs.forEach(function (art) {
      var pid = 'P:' + art.dataset.pid;
      var lessonHref = (art.querySelector('a.pl') || {}).getAttribute
        ? art.querySelector('a.pl').getAttribute('href').replace(/^\.\.\//, '') : null;
      var sol = art.querySelector('details.psol');
      if (!sol) return;
      var bar = document.createElement('div');
      bar.className = 'qgrade';
      bar.innerHTML =
        '<span class="ql">how did you do?</span>' +
        '<button class="qb ok" data-r="1">✓ got it unaided</button>' +
        '<button class="qb no" data-r="0">✗ needed the solution</button>' +
        '<span class="qmsg"></span>';
      sol.querySelector('.psol-b').appendChild(bar);
      var msg = bar.querySelector('.qmsg');

      function paint() {
        var rec = store[pid];
        bar.querySelectorAll('.qb').forEach(function (b) {
          b.classList.toggle('on', !!rec && String(rec.r) === b.dataset.r);
        });
        art.classList.toggle('solved', !!rec && rec.r === 1);
        art.classList.toggle('shaky', !!rec && rec.r === 0);
      }
      paint();

      bar.querySelectorAll('.qb').forEach(function (b) {
        b.addEventListener('click', function () {
          var r = +b.dataset.r;
          store = readQ();
          var prev = store[pid] || { n: 0 };
          store[pid] = { r: r, t: Date.now(), n: prev.n + 1 };
          writeQ(store);
          paint();
          if (r === 0 && lessonHref) {
            var moved = nudge(lessonHref);
            msg.textContent = moved
              ? '→ ' + moved + ' card' + (moved === 1 ? '' : 's') + ' from that lesson pulled forward to tomorrow'
              : '→ re-read the lesson linked at the top right';
          } else {
            msg.textContent = r ? 'noted' : '';
          }
        });
      });
    });
  }

  function wireQuiz() {
    var qs = document.querySelectorAll('details.q[data-qid]');
    if (!qs.length) return;

    var slug = document.body.dataset.slug, file = null;
    if (window.META) {
      (window.META.lessons || []).forEach(function (L) { if (L.s === slug) file = L.f; });
    }
    var store = readQ();
    var nCards = (window.META && file && (window.META.cardsByLesson[file] || []).length) || 0;

    qs.forEach(function (d) {
      var qid = d.dataset.qid, a = d.querySelector('.a');
      if (!a) return;
      var bar = document.createElement('div');
      bar.className = 'qgrade';
      bar.innerHTML =
        '<span class="ql">did you get it?</span>' +
        '<button class="qb ok" data-r="1">✓ got it</button>' +
        '<button class="qb no" data-r="0">✗ missed it</button>' +
        '<span class="qmsg"></span>';
      a.appendChild(bar);

      var msg = bar.querySelector('.qmsg');
      function paint() {
        var rec = store[qid];
        bar.querySelectorAll('.qb').forEach(function (b) {
          b.classList.toggle('on', !!rec && String(rec.r) === b.dataset.r);
        });
        if (rec && rec.n > 1) msg.textContent = rec.n + ' attempts';
      }
      paint();

      bar.querySelectorAll('.qb').forEach(function (b) {
        b.addEventListener('click', function () {
          var r = +b.dataset.r;
          store = readQ();
          var prev = store[qid] || { n: 0 };
          store[qid] = { r: r, t: Date.now(), n: prev.n + 1 };
          writeQ(store);
          paint();
          if (r === 0) {
            var moved = nudge(file);
            msg.textContent = moved
              ? '→ ' + moved + ' card' + (moved === 1 ? '' : 's') + ' from this lesson pulled forward to tomorrow'
              : (nCards ? '→ this lesson’s ' + nCards + ' card' + (nCards === 1 ? '' : 's') + ' are already due or unstarted'
                        : '→ no cards attached to this lesson');
          } else {
            msg.textContent = 'noted';
          }
        });
      });
    });
  }
})();
