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
  var LEECH_LAPSES = 3;   /* forgotten this many times -> flagged as stuck, not just scheduled */

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
  function stripTags(h) { return String(h).replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim(); }
  var reduce = window.matchMedia &&
               window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- filter chips ---------- */
  function renderChips() {
    var courses = [], weeks = [], kinds = [];
    DECK.forEach(function (c) {
      if (courses.indexOf(c.course) < 0) courses.push(c.course);
      if (c.course === filter.course || filter.course === 'all') {
        var wk = c.course + ' W' + c.week;
        if (weeks.indexOf(wk) < 0) weeks.push(wk);
      }
      if (kinds.indexOf(c.kind) < 0) kinds.push(c.kind);
    });
    function row(host, items, key, labels) {
      var h = $(host);
      if (!h) return;
      h.innerHTML = '';
      items.forEach(function (v) {
        var b = el('button', 'chip' + (filter[key] === v ? ' on' : ''), labels ? labels(v) : v);
        b.type = 'button';
        b.addEventListener('click', function () {
          filter[key] = v;
          if (key === 'course') filter.week = 'all';
          startSession();
        });
        h.appendChild(b);
      });
    }
    row('#f-course', ['all'].concat(courses), 'course');
    row('#f-week', ['all'].concat(weeks), 'week');
    row('#f-kind', ['all'].concat(kinds), 'kind');
  }

  /* ---------- stuck cards: forgotten LEECH_LAPSES+ times ----------
     Surfaced rather than merely rescheduled: a card you have forgotten three
     times is not a scheduling problem, it is a comprehension problem, and the
     fix is re-reading the lesson rather than drilling it again. */
  function renderStuck() {
    var host = $('#srs-stuck');
    if (!host) return;
    var stuck = DECK.map(function (c) {
      var s = S.cards[c.id];
      return s && s.lapses >= LEECH_LAPSES ? { c: c, lapses: s.lapses, ef: s.ef } : null;
    }).filter(Boolean).sort(function (a, b) { return b.lapses - a.lapses; });
    if (!stuck.length) { host.innerHTML = ''; return; }
    host.innerHTML =
      '<div class="stuck-h"><span class="stuck-n">' + stuck.length + '</span>' +
      '<div><b>Stuck cards</b><span>Forgotten ' + LEECH_LAPSES + '+ times each &mdash; ' +
      'rescheduling alone is not working. Re-read the lesson.</span></div></div>' +
      '<ul class="stuck-l">' + stuck.slice(0, 8).map(function (s) {
        return '<li><a href="' + s.c.lesson + '"><span class="stuck-q">' +
          stripTags(s.c.front).slice(0, 78) + '</span>' +
          '<span class="stuck-m">' + s.lapses + ' lapses &middot; ease ' +
          s.ef.toFixed(2) + '</span></a></li>';
      }).join('') + '</ul>';
  }

  /* ---------- dashboard ---------- */
  function renderCounts() {
    var c = counts();
    var map = { '#c-due': c.due, '#c-new': c.nw, '#c-later': c.later,
                '#c-done': S.log[today()] || 0, '#c-streak': S.streak };
    Object.keys(map).forEach(function (k) { var n = $(k); if (n) n.textContent = map[k]; });
    var start = $('#srs-start');
    if (start) {
      var n = c.due + Math.min(c.nw, S.settings.newPerDay);
      start.querySelector('.start-n').textContent = n;
      start.disabled = false;
      start.querySelector('.start-l').textContent =
        n ? (c.due ? 'cards ready now' : 'new cards to learn') : 'study ahead anyway';
    }
    var ring = $('#srs-ring-fg');
    if (ring) {
      var total = c.due + c.nw + c.later || 1;
      var seen = c.later;                       /* scheduled = already learned */
      var C = 2 * Math.PI * 34;
      ring.style.strokeDasharray = C;
      ring.style.strokeDashoffset = C * (1 - seen / total);
      var pc = $('#srs-ring-pc');
      if (pc) pc.textContent = Math.round(100 * seen / total) + '%';
    }
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
          '<i style="height:' + Math.max(2, n / mx * 100) + '%"></i>' +
          '<em>' + (i === 0 ? 'now' : i % 7 === 0 ? i + 'd' : '') + '</em></span>';
      }).join('') + '</div>';
  }

  /* ---------- full-screen study mode ----------
     One card, nothing else on screen. That is not decoration: the whole method
     depends on an honest self-report, and anything else visible is something to
     compare yourself against instead of answering. */
  var stage = null, undoSnapshot = null;

  function buildStage() {
    stage = el('div', 'sx-stage');
    stage.hidden = true;
    stage.setAttribute('role', 'dialog');
    stage.setAttribute('aria-modal', 'true');
    stage.setAttribute('aria-label', 'review session');
    stage.innerHTML =
      '<div class="sx-glow" aria-hidden="true"></div>' +
      '<header class="sx-top">' +
        '<button type="button" class="sx-x" aria-label="end session">' +
          '<svg viewBox="0 0 24 24" width="18" height="18"><path d="M6 6l12 12M18 6L6 18"' +
          ' fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg>' +
        '</button>' +
        '<div class="sx-bar"><i></i></div>' +
        '<span class="sx-count"><b>0</b><span>done</span></span>' +
      '</header>' +
      '<div class="sx-body"><div class="sx-scroll"></div></div>' +
      '<footer class="sx-foot"></footer>';
    document.body.appendChild(stage);
    stage.querySelector('.sx-x').addEventListener('click', endSession);
    return stage;
  }

  function openStage() {
    if (!stage) buildStage();
    stage.hidden = false;
    document.body.classList.add('sx-open');
    renderCard();
  }
  function endSession() {
    if (stage) stage.hidden = true;
    document.body.classList.remove('sx-open');
    current = null;
    renderCounts(); renderForecast(); renderStuck();
    var s = $('#srs-start');
    if (s) s.focus();
  }

  function renderCard() {
    if (!stage || stage.hidden) return;
    var scroll = stage.querySelector('.sx-scroll');
    var foot = stage.querySelector('.sx-foot');
    var bar = stage.querySelector('.sx-bar i');
    var cnt = stage.querySelector('.sx-count b');
    scroll.innerHTML = ''; foot.innerHTML = '';
    cnt.textContent = doneThisSession;
    var totalKnown = doneThisSession + queue.length + (current ? 1 : 0);
    bar.style.width = (100 * doneThisSession / Math.max(1, totalKnown)) + '%';

    if (!current) {
      var c = counts();
      var done = el('div', 'sx-done');
      done.innerHTML =
        '<div class="sx-done-ring"><svg viewBox="0 0 96 96"><circle cx="48" cy="48" r="40"/>' +
        '<circle class="fg" cx="48" cy="48" r="40"/></svg><span>&#10003;</span></div>' +
        '<h3>' + (doneThisSession ? 'Session finished' : 'Nothing due right now') + '</h3>' +
        '<p>' + (doneThisSession
          ? 'You reviewed <b>' + doneThisSession + '</b> card' + (doneThisSession === 1 ? '' : 's') +
            '. ' + (c.later ? c.later + ' scheduled for later.' : '')
          : 'Every card in this filter is scheduled for a future day.') + '</p>';
      var row = el('div', 'sx-done-btns');
      var ahead = el('button', 'sx-btn ghost', 'Study ahead');
      ahead.type = 'button';
      ahead.addEventListener('click', function () {
        var p = pool().slice().sort(function (a, b) {
          return (S.cards[a.id] ? S.cards[a.id].due : '9999') <
                 (S.cards[b.id] ? S.cards[b.id].due : '9999') ? -1 : 1;
        });
        queue = p.slice(0, 20); next();
      });
      var close = el('button', 'sx-btn primary', 'Done');
      close.type = 'button';
      close.addEventListener('click', endSession);
      row.appendChild(ahead); row.appendChild(close);
      done.appendChild(row);
      scroll.appendChild(done);
      return;
    }

    var s = st(current.id);
    var card = el('article', 'sx-card' + (revealed ? ' is-open' : ''));
    var status = s.seen === 0 ? 'new' : (s.reps === 0 ? 'relearning' : s.ivl + 'd interval');
    card.innerHTML =
      '<div class="sx-meta"><span class="srs-kind k-' + current.kind + '">' + current.kind +
      '</span><span class="sx-week">' + current.course + ' &middot; W' + current.weekNum +
      ' &middot; ' + current.weekTitle +
      '</span><span class="sx-status">' + status + '</span></div>' +
      '<div class="sx-front">' + current.front + '</div>';
    if (revealed) {
      var back = el('div', 'sx-answer');
      back.innerHTML = '<div class="sx-rule"><span>answer</span></div>' +
        '<div class="srs-back">' + current.back + '</div>' +
        (current.plain ? '<div class="srs-plain-wrap">' + current.plain + '</div>' : '') +
        (current.extra ? '<div class="srs-extra">' + current.extra + '</div>' : '') +
        '<a class="srs-lesson" href="' + current.lesson + '">&#8599; read the full lesson</a>';
      card.appendChild(back);
    }
    scroll.appendChild(card);
    scroll.scrollTop = 0;

    if (!revealed) {
      var show = el('button', 'sx-btn primary big', 'Show answer <kbd>space</kbd>');
      show.type = 'button';
      show.addEventListener('click', reveal);
      foot.appendChild(show);
      foot.appendChild(el('p', 'sx-tip',
        'Answer it <b>out loud</b> before you reveal. Recognising an answer is not recalling it.'));
    } else {
      var grades = el('div', 'sx-grades');
      [['Again', 0, 'g-again'], ['Hard', 1, 'g-hard'],
       ['Good', 2, 'g-good'], ['Easy', 3, 'g-easy']].forEach(function (g, i) {
        var ivl = nextInterval(s, g[1]);
        var b = el('button', 'sx-g ' + g[2],
          '<span class="g-n">' + g[0] + '</span>' +
          '<span class="g-i">' + (g[1] === 0 ? 'now' : ivl + (ivl === 1 ? ' day' : ' days')) + '</span>' +
          '<kbd>' + (i + 1) + '</kbd>');
        b.type = 'button';
        b.addEventListener('click', function () { answer(g[1]); });
        grades.appendChild(b);
      });
      foot.appendChild(grades);
    }
    /* Undo lives outside the reveal branch on purpose: you usually notice a
       misgrade on the NEXT card, not on the one you just graded. */
    if (undoSnapshot) {
      var u = el('button', 'sx-undo', '&#8630; undo last grade <kbd>u</kbd>');
      u.type = 'button';
      u.addEventListener('click', undo);
      foot.appendChild(u);
    }
  }

  /* ---------- flow ---------- */
  function reveal() {
    if (current && !revealed) {
      revealed = true;
      renderCard();
      if (!reduce && stage) {
        var c = stage.querySelector('.sx-card');
        if (c) { c.classList.remove('sx-flip'); void c.offsetWidth; c.classList.add('sx-flip'); }
      }
    }
  }
  /* Undo restores the scheduling state exactly as it was before the last grade.
     It is a UI affordance only: it replays a snapshot into the same schema the
     scheduler already writes, and never invents a value. */
  function undo() {
    if (!undoSnapshot) return;
    S.cards = JSON.parse(undoSnapshot.cards);
    S.log = JSON.parse(undoSnapshot.log);
    S.streak = undoSnapshot.streak;
    S.lastDay = undoSnapshot.lastDay;
    save();
    queue.unshift(current);
    current = undoSnapshot.card;
    doneThisSession = Math.max(0, doneThisSession - 1);
    revealed = true;
    undoSnapshot = null;
    renderCard(); renderCounts(); renderForecast(); renderStuck();
  }
  function answer(g) {
    if (!current) return;
    undoSnapshot = { cards: JSON.stringify(S.cards), log: JSON.stringify(S.log),
                     streak: S.streak, lastDay: S.lastDay, card: current };
    grade(current.id, g);
    doneThisSession++;
    if (g === 0) queue.push(current);          /* see it again this session */
    if (stage && !reduce) {
      stage.classList.remove('sx-g0','sx-g1','sx-g2','sx-g3');
      void stage.offsetWidth;
      stage.classList.add('sx-g' + g);
    }
    next();
    renderCounts(); renderForecast(); renderStuck();
  }
  function next() {
    current = queue.shift() || null;
    revealed = false;
    renderCard();
  }
  function startSession() {
    doneThisSession = 0;
    undoSnapshot = null;
    buildQueue();
    renderChips();
    renderCounts();
    renderForecast();
    renderStuck();
    next();
  }
  function beginStudy() {
    startSession();
    if (!current) { buildQueue(); next(); }
    openStage();
  }

  /* ---------- tools ---------- */
  function wireTools() {
    var np = $('#srs-newperday');
    if (np) {
      np.value = S.settings.newPerDay;
      np.addEventListener('change', function () {
        S.settings.newPerDay = Math.max(0, Math.min(60, parseInt(np.value, 10) || 0));
        np.value = S.settings.newPerDay;
        save(); startSession();
      });
    }
    var ex = $('#srs-export');
    if (ex) ex.addEventListener('click', function () {
      var blob = new Blob([JSON.stringify(S, null, 1)], { type: 'application/json' });
      var a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = 'ml-review-progress-' + today() + '.json';
      a.click();
      setTimeout(function () { URL.revokeObjectURL(a.href); }, 1000);
    });
    var im = $('#srs-import');
    if (im) im.addEventListener('change', function () {
      var f = im.files && im.files[0];
      if (!f) return;
      var r = new FileReader();
      r.onload = function () {
        try {
          var p = JSON.parse(r.result);
          S.cards = p.cards || {}; S.log = p.log || {};
          S.settings = Object.assign({ newPerDay: 12 }, p.settings || {});
          S.streak = p.streak || 0; S.lastDay = p.lastDay || null;
          save(); startSession();
        } catch (e) { alert('That file is not a progress export.'); }
      };
      r.readAsText(f);
    });
    var rs = $('#srs-reset');
    if (rs) rs.addEventListener('click', function () {
      if (confirm('Erase all review progress on this device? ' +
                  'Tip: export first if you might want it back.')) {
        S.cards = {}; S.log = {}; S.streak = 0; S.lastDay = null;
        save(); startSession();
      }
    });
    var go = $('#srs-start');
    if (go) go.addEventListener('click', beginStudy);
  }

  document.addEventListener('keydown', function (e) {
    if (!stage || stage.hidden) return;
    /* e.target is the document when nothing is focused, and document has no
       .matches -- calling it there throws and kills every shortcut. */
    var t = e.target;
    if (t && t.nodeType === 1 && t.closest && t.closest('input, textarea, select')) return;
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    if (e.key === 'Escape') { endSession(); return; }
    if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); reveal(); return; }
    if (revealed && e.key >= '1' && e.key <= '4') {
      e.preventDefault();
      answer(parseInt(e.key, 10) - 1);
    }
    if (e.key === 'u' || e.key === 'z') { e.preventDefault(); undo(); }
  });

  document.addEventListener('DOMContentLoaded', function () {
    load();
    wireTools();
    startSession();
  });
})();
