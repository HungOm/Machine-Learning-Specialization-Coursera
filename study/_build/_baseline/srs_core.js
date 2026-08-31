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