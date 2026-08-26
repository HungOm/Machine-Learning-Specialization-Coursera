/* ============================================================
   Spaced repetition trainer.
   - Deck comes from window.DECK (generated into assets/deck.js)
   - Scheduling state lives in localStorage; nothing is uploaded
   - Scheduler is an SM-2 variant with four grades
   ============================================================ */
(function () {
  'use strict';

  var KEY = 'mls-srs-v1';
  var DAY = 86400000;

  /* ---------- dates, as local YYYY-MM-DD ---------- */
  function iso(d) {
    return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') +
           '-' + String(d.getDate()).padStart(2, '0');
  }
  function today() { return iso(new Date()); }
  function addDays(n) { return iso(new Date(Date.now() + n * DAY)); }
  function daysUntil(s) {
    var a = new Date(s + 'T00:00:00'), b = new Date(today() + 'T00:00:00');
    return Math.round((a - b) / DAY);
  }

  /* ---------- persistence ---------- */
  var S = { cards: {}, log: {}, settings: { newPerDay: 12 }, streak: 0, lastDay: null };
  function load() {
    try {
      var raw = localStorage.getItem(KEY);
      if (raw) {
        var p = JSON.parse(raw);
        S.cards = p.cards || {};
        S.log = p.log || {};
        S.settings = Object.assign({ newPerDay: 12 }, p.settings || {});
        S.streak = p.streak || 0;
        S.lastDay = p.lastDay || null;
      }
    } catch (e) { /* private window, cleared storage — carry on with defaults */ }
  }
  function save() {
    try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) { }
  }
  function st(id) {
    if (!S.cards[id]) S.cards[id] = { ef: 2.5, reps: 0, ivl: 0, due: today(), lapses: 0, seen: 0 };
    return S.cards[id];
  }

  /* ---------- the scheduler ---------- */
  /* grade: 0 again · 1 hard · 2 good · 3 easy */
  function nextInterval(c, grade) {
    if (grade === 0) return 0;
    if (c.reps === 0) return grade === 3 ? 3 : grade === 1 ? 1 : 1;
    if (c.reps === 1) return grade === 3 ? 8 : grade === 1 ? 3 : 6;
    var mult = grade === 1 ? 0.6 : grade === 3 ? 1.3 : 1.0;
    return Math.max(1, Math.round(c.ivl * c.ef * mult));
  }
  function grade(id, g) {
    var c = st(id), q = [0, 3, 4, 5][g];
    c.seen++;
    if (g === 0) {
      c.lapses++; c.reps = 0; c.ivl = 0; c.due = today();
    } else {
      c.ivl = nextInterval(c, g);
      c.reps++;
      c.due = addDays(c.ivl);
    }
    c.ef = Math.max(1.3, Math.min(3.2, c.ef + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))));
    var d = today();
    S.log[d] = (S.log[d] || 0) + 1;
    if (S.lastDay !== d) {
      S.streak = (S.lastDay === addDays(-1)) ? S.streak + 1 : 1;
      S.lastDay = d;
    }
    save();
  }

  /* ---------- deck filtering ---------- */
  var DECK = window.DECK || [];
  var filter = { course: 'all', week: 'all', kind: 'all' };
  function pass(c) {
    return (filter.course === 'all' || c.course === filter.course) &&
           (filter.week === 'all' || c.week === filter.week) &&
           (filter.kind === 'all' || c.kind === filter.kind);
  }
  function pool() { return DECK.filter(pass); }
  function counts() {
    var p = pool(), t = today(), due = 0, nw = 0, later = 0;
    p.forEach(function (c) {
      var s = S.cards[c.id];
      if (!s || s.reps === 0 && s.seen === 0) nw++;
      else if (s.due <= t) due++;
      else later++;
    });
    return { due: due, nw: nw, later: later, total: p.length };
  }

  /* ---------- the session queue ---------- */
  var queue = [], current = null, revealed = false, doneThisSession = 0;
  function buildQueue() {
    var p = pool(), t = today();
    var dueCards = [], newCards = [];
    p.forEach(function (c) {
      var s = S.cards[c.id];
      if (!s || (s.reps === 0 && s.seen === 0)) newCards.push(c);
      else if (s.due <= t) dueCards.push(c);
    });
    /* oldest-due first, then a capped number of new cards, lightly shuffled */
    dueCards.sort(function (a, b) { return (S.cards[a.id].due < S.cards[b.id].due) ? -1 : 1; });
    var introduced = 0;
    Object.keys(S.log).length;                      /* touch, keeps linters quiet */
    var cap = S.settings.newPerDay;
    var takeNew = newCards.slice(0, Math.max(0, cap - introduced));
    queue = dueCards.concat(takeNew);
    /* interleave a little so it is not all reviews then all new */
    for (var i = queue.length - 1; i > 0; i--) {
      if (Math.random() < 0.35) {
        var j = Math.floor(Math.random() * (i + 1));
        var tmp = queue[i]; queue[i] = queue[j]; queue[j] = tmp;
      }
    }
  }

  /* ---------- rendering ---------- */
  function $(sel) { return document.querySelector(sel); }
  function el(tag, cls, html) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html != null) e.innerHTML = html;
    return e;
  }

  function renderChips() {
    var courses = ['all'], weeks = [], kinds = ['all'];
    DECK.forEach(function (c) {
      if (courses.indexOf(c.course) < 0) courses.push(c.course);
      if (kinds.indexOf(c.kind) < 0) kinds.push(c.kind);
    });
    DECK.forEach(function (c) {
      if (filter.course !== 'all' && c.course !== filter.course) return;
      if (weeks.indexOf(c.week) < 0) weeks.push(c.week);
    });
    weeks.sort();
    function chipRow(host, items, key, label) {
      host.innerHTML = '';
      host.appendChild(el('span', 'chip-label', label));
      items.forEach(function (v) {
        var b = el('button', 'chip' + (filter[key] === v ? ' on' : ''),
          v === 'all' ? 'all' : (key === 'week' ? v.toUpperCase().replace('W', ' W') : v));
        b.addEventListener('click', function () {
          filter[key] = v;
          if (key === 'course') filter.week = 'all';
          startSession();
        });
        host.appendChild(b);
      });
    }
    chipRow($('#f-course'), courses, 'course', 'course');
    chipRow($('#f-week'), ['all'].concat(weeks), 'week', 'week');
    chipRow($('#f-kind'), kinds, 'kind', 'type');
  }

  function renderCounts() {
    var c = counts();
    $('#c-due').textContent = c.due;
    $('#c-new').textContent = c.nw;
    $('#c-later').textContent = c.later;
    $('#c-done').textContent = S.log[today()] || 0;
    $('#c-streak').textContent = S.streak;
  }

  function renderCard() {
    var host = $('#card-area');
    host.innerHTML = '';
    if (!current) {
      var c = counts();
      var box = el('div', 'srs-done');
      box.appendChild(el('div', 'srs-done-mark', '✓'));
      box.appendChild(el('h3', null, doneThisSession ? 'Session finished' : 'Nothing due right now'));
      box.appendChild(el('p', null, doneThisSession
        ? 'You reviewed <b>' + doneThisSession + '</b> card' + (doneThisSession === 1 ? '' : 's') + '. '
          + (c.later ? c.later + ' card' + (c.later === 1 ? ' is' : 's are') + ' scheduled for later.' : '')
        : 'Every card in this filter is either scheduled for a future day, or you have not enabled any new ones.'));
      var ahead = el('button', 'btn primary', 'Study ahead anyway');
      ahead.addEventListener('click', function () {
        var p = pool().slice().sort(function (a, b) {
          return (S.cards[a.id] ? S.cards[a.id].due : '9999') < (S.cards[b.id] ? S.cards[b.id].due : '9999') ? -1 : 1;
        });
        queue = p.slice(0, 20);
        next();
      });
      box.appendChild(ahead);
      host.appendChild(box);
      renderForecast();
      return;
    }
    var s = st(current.id);
    var wrap = el('div', 'srs-card');
    var meta = el('div', 'srs-meta');
    meta.appendChild(el('span', 'srs-kind k-' + current.kind, current.kind));
    meta.appendChild(el('span', 'srs-week', current.course + ' · Week ' + current.week + ' — ' + current.weekTitle));
    var status = s.seen === 0 ? 'new' : (s.reps === 0 ? 'relearning' : 'review · ' + s.ivl + 'd');
    meta.appendChild(el('span', 'srs-status', status));
    wrap.appendChild(meta);
    wrap.appendChild(el('div', 'srs-front', current.front));
    if (revealed) {
      wrap.appendChild(el('hr', 'srs-rule'));
      wrap.appendChild(el('div', 'srs-back', current.back));
      if (current.plain) wrap.appendChild(el('div', 'srs-plain-wrap', current.plain));
      if (current.extra) wrap.appendChild(el('div', 'srs-extra', current.extra));
      var link = el('a', 'srs-lesson', '↗ read the full lesson');
      link.href = current.lesson;
      wrap.appendChild(link);
    }
    host.appendChild(wrap);

    var bar = el('div', 'srs-actions');
    if (!revealed) {
      var show = el('button', 'btn primary big', 'Show answer');
      show.addEventListener('click', reveal);
      bar.appendChild(show);
      bar.appendChild(el('span', 'srs-hint', 'space'));
    } else {
      [['Again', 0, 'g-again'], ['Hard', 1, 'g-hard'], ['Good', 2, 'g-good'], ['Easy', 3, 'g-easy']]
        .forEach(function (g) {
          var ivl = nextInterval(s, g[1]);
          var b = el('button', 'btn grade ' + g[2],
            g[0] + '<small>' + (g[1] === 0 ? 'now' : ivl + ' day' + (ivl === 1 ? '' : 's')) + '</small>');
          b.addEventListener('click', function () { answer(g[1]); });
          bar.appendChild(b);
        });
      bar.appendChild(el('span', 'srs-hint', '1 · 2 · 3 · 4'));
    }
    host.appendChild(bar);
    var prog = el('div', 'srs-prog');
    prog.innerHTML = '<i style="width:' +
      (100 * doneThisSession / Math.max(1, doneThisSession + queue.length + 1)) + '%"></i>';
    host.appendChild(prog);
  }

  function renderForecast() {
    var host = $('#forecast');
    if (!host) return;
    var buckets = new Array(15).fill(0), t = today();
    pool().forEach(function (c) {
      var s = S.cards[c.id];
      if (!s || s.seen === 0) return;
      var d = daysUntil(s.due);
      if (d < 0) d = 0;
      if (d < 15) buckets[d]++;
    });
    var mx = Math.max.apply(null, buckets.concat([1]));
    host.innerHTML = '<div class="fc-title">upcoming reviews</div><div class="fc-bars">' +
      buckets.map(function (n, i) {
        return '<span class="fc-bar" title="' + n + ' on day ' + i + '">' +
          '<i style="height:' + (n / mx * 100) + '%"></i>' +
          '<em>' + (i === 0 ? 'now' : i % 7 === 0 ? i + 'd' : '') + '</em></span>';
      }).join('') + '</div>';
  }

  /* ---------- flow ---------- */
  function reveal() { if (current && !revealed) { revealed = true; renderCard(); } }
  function answer(g) {
    if (!current) return;
    grade(current.id, g);
    doneThisSession++;
    if (g === 0) queue.push(current);          /* see it again this session */
    next();
    renderCounts();
    renderForecast();
  }
  function next() {
    current = queue.shift() || null;
    revealed = false;
    renderCard();
  }
  function startSession() {
    doneThisSession = 0;
    buildQueue();
    renderChips();
    renderCounts();
    next();
    renderForecast();
  }

  /* ---------- export / import / reset ---------- */
  function wireTools() {
    var ex = $('#srs-export');
    if (ex) ex.addEventListener('click', function () {
      var blob = new Blob([JSON.stringify(S, null, 2)], { type: 'application/json' });
      var a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = 'ml-srs-progress-' + today() + '.json';
      document.body.appendChild(a); a.click(); a.remove();
    });
    var im = $('#srs-import');
    if (im) im.addEventListener('change', function (e) {
      var f = e.target.files[0];
      if (!f) return;
      var r = new FileReader();
      r.onload = function () {
        try {
          var p = JSON.parse(r.result);
          S.cards = p.cards || {}; S.log = p.log || {};
          S.settings = p.settings || S.settings; S.streak = p.streak || 0; S.lastDay = p.lastDay || null;
          save(); startSession();
          alert('Progress restored.');
        } catch (err) { alert('That file could not be read as SRS progress.'); }
      };
      r.readAsText(f);
    });
    var rs = $('#srs-reset');
    if (rs) rs.addEventListener('click', function () {
      if (confirm('Reset ALL spaced-repetition progress? This cannot be undone.\n\n' +
                  'Tip: export first if you might want it back.')) {
        S = { cards: {}, log: {}, settings: { newPerDay: 12 }, streak: 0, lastDay: null };
        save(); startSession();
      }
    });
    var np = $('#srs-newperday');
    if (np) {
      np.value = S.settings.newPerDay;
      np.addEventListener('change', function () {
        S.settings.newPerDay = Math.max(0, parseInt(np.value, 10) || 0);
        save(); startSession();
      });
    }
  }

  document.addEventListener('keydown', function (e) {
    var tag = (e.target.tagName || '').toLowerCase();
    if (tag === 'input' || tag === 'textarea' || e.metaKey || e.ctrlKey) return;
    if (!current) return;
    if (!revealed && (e.key === ' ' || e.key === 'Enter')) { e.preventDefault(); reveal(); }
    else if (revealed && ['1', '2', '3', '4'].indexOf(e.key) >= 0) {
      e.preventDefault(); answer(parseInt(e.key, 10) - 1);
    }
  });

  document.addEventListener('DOMContentLoaded', function () {
    load();
    if (!document.getElementById('card-area')) return;
    wireTools();
    startSession();
  });
})();
