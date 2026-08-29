/* Dashboard: what you've read, what's due, and what you keep getting wrong.
   Reads three localStorage keys and computes everything in the page —
   nothing is uploaded, and clearing your browser data clears all of it. */
(function () {
  'use strict';
  var PKEY = 'mls-study-progress-v1', SKEY = 'mls-srs-v1', QKEY = 'mls-quiz-v1', DAY = 86400000;

  function rd(k) { try { return JSON.parse(localStorage.getItem(k) || '{}'); } catch (e) { return {}; } }
  function iso(d) {
    return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') +
           '-' + String(d.getDate()).padStart(2, '0');
  }
  function today() { return iso(new Date()); }
  function addDays(n) { return iso(new Date(Date.now() + n * DAY)); }
  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }
  function el(id) { return document.getElementById(id); }

  var DECK = window.DECK || [], META = window.META || { lessons: [], weeks: [], cardsByLesson: {} };
  var done, S, Q;

  /* ---------------------------------------------------------- maturity */
  /* Anki's convention: an interval of 21 days or more means it has stuck. */
  function bucket(c) {
    if (!c || !c.reps) return 'new';
    if (c.ivl >= 21) return 'mature';
    return 'learning';
  }

  function stats() {
    var cards = S.cards || {}, b = { new: 0, learning: 0, mature: 0 }, due = 0, lapsed = 0;
    var t = today();
    DECK.forEach(function (c) {
      var st = cards[c.id];
      b[bucket(st)]++;
      if (st && st.due && st.due <= t && st.reps) due++;
      if (st && st.lapses >= 2) lapsed++;
    });
    /* Quiz answers and problem grades live in the same store but are different
       activities: a 3-line self-check is recognition, a problem is production.
       Counting them in one percentage hides exactly the gap that matters. */
    var qk = [], pk = [], right = 0, pright = 0;
    Object.keys(Q).forEach(function (k) {
      if (k.indexOf('P:') === 0) { pk.push(k); if (Q[k].r === 1) pright++; }
      else { qk.push(k); if (Q[k].r === 1) right++; }
    });
    return {
      lessonsDone: META.lessons.filter(function (L) { return done[L.s]; }).length,
      lessonsTotal: META.lessons.length,
      cards: b, cardsTotal: DECK.length, due: due, lapsed: lapsed,
      qAnswered: qk.length, qRight: right,
      pAnswered: pk.length, pRight: pright,
      pTotal: (META.problems || []).reduce(function (a, p) { return a + p.n; }, 0),
      qTotal: META.lessons.reduce(function (a, L) { return a + (L.q || 0); }, 0),
      streak: S.streak || 0,
      reviewsToday: (S.log || {})[t] || 0
    };
  }

  /* ---------------------------------------------------------- headline */
  function renderTop(x) {
    function pct(a, b) { return b ? Math.round(100 * a / b) : 0; }
    var acc = x.qAnswered ? Math.round(100 * x.qRight / x.qAnswered) : null;
    el('dash-top').innerHTML = [
      tile('lessons read', x.lessonsDone + ' / ' + x.lessonsTotal, pct(x.lessonsDone, x.lessonsTotal) + '% of the site', pct(x.lessonsDone, x.lessonsTotal)),
      tile('cards sticking', x.cards.mature + ' / ' + x.cardsTotal, 'interval ≥ 21 days', pct(x.cards.mature, x.cardsTotal)),
      tile('due right now', String(x.due), x.due ? 'go and clear them' : 'nothing waiting', null),
      tile('self-check score', acc === null ? '—' : acc + '%', x.qAnswered + ' of ' + x.qTotal + ' answered', acc),
      tile('problems solved', x.pAnswered ? x.pRight + ' / ' + x.pAnswered : '—',
           'unaided, of ' + x.pTotal + ' written', x.pAnswered ? pct(x.pRight, x.pAnswered) : null),
      tile('review streak', x.streak + (x.streak === 1 ? ' day' : ' days'), x.reviewsToday + ' reviews today', null)
    ].join('');
  }
  function tile(label, big, sub, pc) {
    return '<div class="tile"><span class="tl">' + label + '</span><b>' + big + '</b>' +
      '<span class="ts">' + sub + '</span>' +
      (pc === null ? '' : '<span class="tbar"><i style="width:' + Math.max(0, Math.min(100, pc)) + '%"></i></span>') +
      '</div>';
  }

  /* ---------------------------------------------------------- per week */
  function renderWeeks() {
    var cards = S.cards || {};
    var rows = META.weeks.map(function (w) {
      var ls = META.lessons.filter(function (L) { return L.c === w.c && L.w === w.w; });
      var nDone = ls.filter(function (L) { return done[L.s]; }).length;
      var files = {}; ls.forEach(function (L) { files[L.f] = 1; });
      var ids = [];
      Object.keys(META.cardsByLesson).forEach(function (f) {
        if (files[f]) ids = ids.concat(META.cardsByLesson[f]);
      });
      var mat = ids.filter(function (i) { return bucket(cards[i]) === 'mature'; }).length;
      var qa = 0, qr = 0;
      ls.forEach(function (L) {
        for (var i = 1; i <= (L.q || 0); i++) {
          var r = Q[L.s + '#' + i];
          if (r) { qa++; if (r.r === 1) qr++; }
        }
      });
      var p = function (a, b) { return b ? Math.round(100 * a / b) : 0; };
      return '<tr><td class="wk"><b>' + w.c + ' W' + w.w + '</b><span>' + esc(w.t) + '</span></td>' +
        '<td>' + minibar(p(nDone, ls.length)) + '<span class="mn">' + nDone + '/' + ls.length + '</span></td>' +
        '<td>' + minibar(p(mat, ids.length)) + '<span class="mn">' + mat + '/' + ids.length + '</span></td>' +
        '<td>' + (qa ? minibar(p(qr, qa), qr / qa < 0.7 ? 'bad' : '') + '<span class="mn">' + p(qr, qa) + '%</span>'
                     : '<span class="mn dim">not answered</span>') + '</td></tr>';
    });
    el('dash-weeks').innerHTML =
      '<table class="dashtab"><thead><tr><th>week</th><th>lessons read</th>' +
      '<th>cards sticking</th><th>self-check</th></tr></thead><tbody>' + rows.join('') + '</tbody></table>';
  }
  function minibar(p, cls) {
    return '<span class="mb ' + (cls || '') + '"><i style="width:' + p + '%"></i></span>';
  }

  /* ---------------------------------------------------------- forecast */
  function renderForecast() {
    var cards = S.cards || {}, days = [], max = 1;
    for (var i = 0; i < 21; i++) {
      var d = addDays(i), n = 0;
      DECK.forEach(function (c) {
        var st = cards[c.id];
        if (!st || !st.reps) return;
        if (i === 0 ? st.due <= d : st.due === d) n++;
      });
      days.push({ d: d, n: n });
      if (n > max) max = n;
    }
    el('dash-forecast').innerHTML = '<div class="fc">' + days.map(function (x, i) {
      var lab = i === 0 ? 'today' : (i === 1 ? 'tue' : '') ;
      return '<span class="fcb" title="' + x.d + ' — ' + x.n + ' cards">' +
        '<i style="height:' + Math.round(100 * x.n / max) + '%"></i>' +
        '<em>' + (i % 7 === 0 ? (i === 0 ? 'today' : '+' + i + 'd') : '') + '</em></span>';
    }).join('') + '</div>';
  }

  /* ---------------------------------------------------------- weak spots */
  function renderWeak() {
    var cards = S.cards || {}, byLesson = {};
    /* slug for every lesson file, so a problem can be traced back to its lesson */
    var slugOfFile = {};
    META.lessons.forEach(function (L) { slugOfFile[L.f] = L.s; });

    /* signal 1 — self-check questions you got wrong */
    /* signal 2 — problems you could not do unaided. These are keyed 'P:<pid>',
       so they have to be mapped through META.problemLesson; splitting on '#'
       the way a quiz id does would silently drop every one of them. */
    Object.keys(Q).forEach(function (qid) {
      if (Q[qid].r !== 0) return;
      var slug;
      if (qid.indexOf('M:') === 0) {
        var mfile = (META.mockLesson || {})[qid.slice(2)];
        slug = mfile && slugOfFile[mfile];
        if (!slug) return;
        byLesson[slug] = byLesson[slug] || { miss: 0, lapse: 0, prob: 0, mock: 0 };
        byLesson[slug].mock = (byLesson[slug].mock || 0) + 1;
        return;
      }
      if (qid.indexOf('P:') === 0) {
        var file = (META.problemLesson || {})[qid.slice(2)];
        slug = file && slugOfFile[file];
        if (!slug) return;
        byLesson[slug] = byLesson[slug] || { miss: 0, lapse: 0, prob: 0 };
        byLesson[slug].prob++;
        return;
      }
      slug = qid.split('#')[0];
      byLesson[slug] = byLesson[slug] || { miss: 0, lapse: 0, prob: 0 };
      byLesson[slug].miss++;
    });
    /* signal 2 — cards you have forgotten more than once */
    var lessonOf = {};
    Object.keys(META.cardsByLesson).forEach(function (f) {
      META.cardsByLesson[f].forEach(function (id) { lessonOf[id] = f; });
    });
    var slugOf = slugOfFile;
    DECK.forEach(function (c) {
      var st = cards[c.id];
      if (!st || st.lapses < 2) return;
      var slug = slugOf[lessonOf[c.id]];
      if (!slug) return;
      byLesson[slug] = byLesson[slug] || { miss: 0, lapse: 0, prob: 0 };
      byLesson[slug].lapse += st.lapses;
    });

    var meta = {};
    META.lessons.forEach(function (L) { meta[L.s] = L; });
    var out = Object.keys(byLesson).map(function (s) {
      var v = byLesson[s];
      return { s: s, L: meta[s],
               score: v.miss * 3 + v.lapse + (v.prob || 0) * 6 + (v.mock || 0) * 5,
               miss: v.miss, lapse: v.lapse, prob: v.prob || 0, mock: v.mock || 0 };
    }).filter(function (x) { return x.L; });
    out.sort(function (a, b) { return b.score - a.score; });

    if (!out.length) {
      el('dash-weak').innerHTML = '<p class="dim">Nothing flagged yet. Answer the self-check questions at the ' +
        'bottom of each lesson — miss one and it shows up here, and that lesson’s cards get pulled forward to tomorrow.</p>';
      return;
    }
    el('dash-weak').innerHTML = '<ol class="weaklist">' + out.slice(0, 15).map(function (x) {
      var why = [];
      if (x.mock) why.push(x.mock + ' mock-quiz miss' + (x.mock === 1 ? '' : 'es'));
      if (x.prob) why.push(x.prob + ' problem' + (x.prob === 1 ? '' : 's') + ' needed the solution');
      if (x.miss) why.push(x.miss + ' self-check miss' + (x.miss === 1 ? '' : 'es'));
      if (x.lapse) why.push(x.lapse + ' card lapse' + (x.lapse === 1 ? '' : 's'));
      return '<li><a href="' + x.L.f + '"><b>' + esc(x.L.t) + '</b>' +
        '<span class="wm">' + x.L.c + ' W' + x.L.w + ' · ' + why.join(' · ') + '</span></a></li>';
    }).join('') + '</ol>';
  }

  /* ---------------------------------------------------------- heatmap */
  function renderHeat() {
    var log = S.log || {}, cells = [], max = 1;
    for (var i = 83; i >= 0; i--) {
      var d = addDays(-i), n = log[d] || 0;
      cells.push({ d: d, n: n });
      if (n > max) max = n;
    }
    el('dash-heat').innerHTML = '<div class="heat">' + cells.map(function (c) {
      var lv = c.n === 0 ? 0 : c.n < max * .25 ? 1 : c.n < max * .5 ? 2 : c.n < max * .75 ? 3 : 4;
      return '<span class="hc l' + lv + '" title="' + c.d + ' — ' + c.n + ' reviews"></span>';
    }).join('') + '</div><p class="dim" style="margin-top:8px">Last 12 weeks of reviews. ' +
      'The nightly alarm fires at 22:00 — <code>study/_build/install-alarm.sh --status</code> to check it.</p>';
  }

  /* ---------------------------------------------------------- Anki export */
  function ankiTSV() {
    var lines = ['#separator:tab', '#html:true', '#notetype:Basic', '#deck:ML Specialization', '#tags column:3'];
    DECK.forEach(function (c) {
      var front = c.front, back = c.back + (c.plain || '') + (c.extra || '');
      var tags = ['MLspec', c.course, c.course + '_W' + c.weekNum, c.kind].join(' ');
      lines.push([clean(front), clean(back), tags].join('\t'));
    });
    return lines.join('\n');
  }
  function clean(h) {
    return String(h || '').replace(/[\t\r\n]+/g, ' ').replace(/\s{2,}/g, ' ').trim();
  }
  function download(name, text, mime) {
    var blob = new Blob([text], { type: mime || 'text/plain;charset=utf-8' });
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = name;
    document.body.appendChild(a); a.click();
    setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 1000);
  }

  /* ---------------------------------------------------------- boot */
  document.addEventListener('DOMContentLoaded', function () {
    done = rd(PKEY); S = rd(SKEY); Q = rd(QKEY);
    if (!S.cards) S.cards = {};
    var x = stats();
    renderTop(x); renderWeeks(); renderForecast(); renderWeak(); renderHeat();

    var a = el('anki-btn');
    if (a) a.addEventListener('click', function () {
      download('ml-specialization-anki.txt', ankiTSV(), 'text/tab-separated-values;charset=utf-8');
      el('anki-msg').textContent = '↓ saved — in Anki: File ▸ Import, pick this file, Basic note type.';
    });
    var j = el('json-btn');
    if (j) j.addEventListener('click', function () {
      download('ml-notes-backup.json', JSON.stringify({
        exported: new Date().toISOString(), progress: done, srs: S, quiz: Q
      }, null, 2), 'application/json');
      el('anki-msg').textContent = '↓ saved — that file restores your schedule if you clear this browser.';
    });
    var r = el('restore-inp');
    if (r) r.addEventListener('change', function () {
      var f = r.files && r.files[0]; if (!f) return;
      var fr = new FileReader();
      fr.onload = function () {
        try {
          var o = JSON.parse(fr.result);
          if (o.progress) localStorage.setItem(PKEY, JSON.stringify(o.progress));
          if (o.srs) localStorage.setItem(SKEY, JSON.stringify(o.srs));
          if (o.quiz) localStorage.setItem(QKEY, JSON.stringify(o.quiz));
          location.reload();
        } catch (e) { el('anki-msg').textContent = 'That file did not parse as a backup.'; }
      };
      fr.readAsText(f);
    });
  });
})();
