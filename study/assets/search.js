/* Site-wide search over lessons, cards and symbols.
   Opens with "/" or the ⌕ button. The index is ~0.5 MB so it is injected
   lazily on first open — and injected as a <script>, not fetched, because
   fetch() is blocked on file:// and this site has to work offline. */
(function () {
  'use strict';
  var UP = '', loaded = false, loading = false, box, panel, list, results = [], sel = -1;

  function up() {
    var l = document.querySelector('link[href$="base.css"]');
    var h = l ? l.getAttribute('href') : 'assets/base.css';
    return h.slice(0, h.indexOf('assets/'));
  }

  function ensureIndex(cb) {
    if (window.SEARCH_INDEX) { loaded = true; return cb(); }   /* already on the page */
    if (loaded) return cb();
    if (loading) return;
    loading = true;
    var s = document.createElement('script');
    s.src = UP + 'assets/search-index.js';
    s.onload = function () { loaded = true; loading = false; cb(); };
    s.onerror = function () {
      loading = false;
      list.innerHTML = '<div class="sr-empty">Could not load the search index. ' +
        'Run <code>python3 study/_build/build.py</code> to generate it.</div>';
    };
    document.head.appendChild(s);
  }

  /* ---- scoring: every term must appear somewhere; earlier fields weigh more ---- */
  function score(rec, terms) {
    var ti = rec.ti.toLowerCase(), s = (rec.s || '').toLowerCase(),
        h = (rec.h || '').toLowerCase(), b = rec.b || '', tot = 0;
    for (var i = 0; i < terms.length; i++) {
      var t = terms[i], got = 0;
      if (ti.indexOf(t) === 0) got = 120;
      else if (ti.indexOf(t) >= 0) got = 80;
      else if (h.indexOf(t) >= 0) got = 30;
      else if (s.indexOf(t) >= 0) got = 22;
      else if (b.indexOf(t) >= 0) got = 8;
      if (!got) return 0;                       /* AND, not OR */
      tot += got;
    }
    if (rec.t === 'lesson') tot += 6;           /* prefer a whole lesson over a card */
    if (rec.t === 'symbol') tot += 3;
    if (rec.t === 'lab') tot += 2;
    return tot;
  }

  function run(q) {
    q = q.trim().toLowerCase();
    if (!q) { list.innerHTML = '<div class="sr-empty">Type to search lessons, problems, from-scratch code, lab companions, cards and symbols.</div>'; results = []; return; }
    var terms = q.split(/\s+/), out = [];
    for (var i = 0; i < window.SEARCH_INDEX.length; i++) {
      var sc = score(window.SEARCH_INDEX[i], terms);
      if (sc) out.push([sc, window.SEARCH_INDEX[i]]);
    }
    out.sort(function (a, b) { return b[0] - a[0]; });
    results = out.slice(0, 40).map(function (x) { return x[1]; });
    sel = results.length ? 0 : -1;
    render(terms);
  }

  function render(terms) {
    if (!results.length) {
      list.innerHTML = '<div class="sr-empty">Nothing matched. Try one word — “gradient”, “sigma”, “axis”.</div>';
      return;
    }
    list.innerHTML = results.map(function (r, i) {
      return '<a class="sr' + (i === sel ? ' on' : '') + '" href="' + UP + r.u + '" data-i="' + i + '">' +
        '<span class="sr-k k-' + r.t + '">' + r.t + '</span>' +
        '<span class="sr-main"><b>' + mark(r.ti, terms) + '</b>' +
        '<span class="sr-sub">' + mark(r.s || '', terms) + '</span></span>' +
        '<span class="sr-w">' + esc(r.w) + '</span></a>';
    }).join('');
    var on = list.querySelector('.sr.on');
    if (on && on.scrollIntoView) on.scrollIntoView({ block: 'nearest' });
  }

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }
  function mark(s, terms) {
    s = esc(s);
    terms.forEach(function (t) {
      if (t.length < 2) return;
      s = s.replace(new RegExp('(' + t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'ig'), '<em>$1</em>');
    });
    return s;
  }

  function open_() {
    panel.classList.add('on');
    document.body.classList.add('search-open');
    box.value = ''; box.focus();
    ensureIndex(function () { run(''); });
    run('');
  }
  function close_() { panel.classList.remove('on'); document.body.classList.remove('search-open'); }

  document.addEventListener('DOMContentLoaded', function () {
    UP = up();
    panel = document.createElement('div');
    panel.className = 'searchpanel';
    panel.innerHTML =
      '<div class="sp-box"><input type="search" id="sbox" autocomplete="off" spellcheck="false" ' +
      'placeholder="search lessons, cards and symbols…"><button class="btn" id="sclose">esc</button>' +
      '<div class="sp-list" id="slist"></div></div>';
    document.body.appendChild(panel);
    box = panel.querySelector('#sbox');
    list = panel.querySelector('#slist');

    panel.addEventListener('click', function (e) { if (e.target === panel) close_(); });
    panel.querySelector('#sclose').addEventListener('click', close_);
    box.addEventListener('input', function () { ensureIndex(function () { run(box.value); }); });

    box.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { close_(); return; }
      if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
        e.preventDefault();
        if (!results.length) return;
        sel = (sel + (e.key === 'ArrowDown' ? 1 : results.length - 1)) % results.length;
        render(box.value.trim().toLowerCase().split(/\s+/));
      }
      if (e.key === 'Enter' && sel >= 0 && results[sel]) location.href = UP + results[sel].u;
    });

    var sb = document.getElementById('search-btn');
    if (sb) sb.addEventListener('click', open_);

    document.addEventListener('keydown', function (e) {
      if (e.metaKey || e.ctrlKey || e.altKey) return;
      var tag = (e.target.tagName || '').toLowerCase();
      if (tag === 'input' || tag === 'textarea' || tag === 'select') return;
      if (e.key === '/') { e.preventDefault(); open_(); }
    });
  });
})();
