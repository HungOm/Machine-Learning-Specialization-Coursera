/* Site chrome: theme, progress tracking, sidebar, keyboard paging */
(function () {
  'use strict';
  var KEY = 'mls-study-progress-v1', TKEY = 'mls-study-theme-v1';

  function read() {
    try { return JSON.parse(localStorage.getItem(KEY) || '{}'); } catch (e) { return {}; }
  }
  function write(o) { try { localStorage.setItem(KEY, JSON.stringify(o)); } catch (e) { } }

  /* ---- theme ---- */
  function applyTheme(v) {
    if (v === 'light' || v === 'dark') document.documentElement.setAttribute('data-theme', v);
    else document.documentElement.removeAttribute('data-theme');
    var b = document.getElementById('theme-btn');
    if (b) b.textContent = v === 'dark' ? '☾' : v === 'light' ? '☀' : '◐';
    window.dispatchEvent(new Event('themechange'));
  }
  var theme = 'auto';
  try { theme = localStorage.getItem(TKEY) || 'auto'; } catch (e) { }
  applyTheme(theme);

  document.addEventListener('DOMContentLoaded', function () {
    var tb = document.getElementById('theme-btn');
    if (tb) tb.addEventListener('click', function () {
      theme = theme === 'auto' ? 'light' : theme === 'light' ? 'dark' : 'auto';
      try { localStorage.setItem(TKEY, theme); } catch (e) { }
      applyTheme(theme);
    });

    /* ---- sidebar (mobile) ---- */
    var mt = document.getElementById('menu-toggle');
    if (mt) mt.addEventListener('click', function () { document.body.classList.toggle('nav-open'); });
    document.querySelectorAll('.sidebar a').forEach(function (a) {
      a.addEventListener('click', function () { document.body.classList.remove('nav-open'); });
    });

    /* ---- progress ---- */
    var done = read();
    var slug = document.body.dataset.slug;
    document.querySelectorAll('[data-slug-link]').forEach(function (a) {
      if (done[a.dataset.slugLink]) a.classList.add('seen');
    });

    /* Remember the last lesson opened, so the cover can offer "continue".
       Guard on .runhead, not on data-slug: the index, problem, scratch and lab
       pages all carry sentinel slugs like "__index__", and keying off the slug
       alone recorded the index itself as the last lesson read — storing the
       cover's own title as the thing to continue from. */
    var runhead = document.querySelector('main .runhead');
    if (slug && slug.indexOf('__') !== 0 && runhead) {
      try {
        var h1 = document.querySelector('main h1');
        var t = '';
        if (h1) [].forEach.call(h1.childNodes, function (n) {
          /* skip the § number, keep the title */
          if (n.nodeType === 1 && n.classList && n.classList.contains('secno')) return;
          t += n.textContent || '';
        });
        var run = runhead.querySelector('.ch');
        var right = runhead.querySelector('.right');
        localStorage.setItem('mls-last-v1', JSON.stringify({
          href: location.pathname.split('/').slice(-2).join('/'),
          title: t.trim() || slug,
          slug: slug,
          sec: right ? right.textContent.trim() : '',
          chapter: run ? run.textContent.trim() : ''
        }));
      } catch (e) { }
    }
    var btn = document.getElementById('done-btn');
    function syncBtn() {
      if (!btn) return;
      var on = !!done[slug];
      btn.classList.toggle('done', on);
      btn.textContent = on ? '✓ done' : 'mark done';
    }
    if (btn && slug) {
      syncBtn();
      btn.addEventListener('click', function () {
        done = read();
        if (done[slug]) delete done[slug]; else done[slug] = Date.now();
        write(done); syncBtn();
        document.querySelectorAll('[data-slug-link="' + slug + '"]').forEach(function (a) {
          a.classList.toggle('seen', !!done[slug]);
        });
      });
    }
    /* index page totals */
    var pb = document.getElementById('pbar');
    if (pb) {
      var total = +pb.dataset.total, n = 0;
      Object.keys(done).forEach(function (k) { n++; });
      pb.querySelector('i').style.width = (100 * n / total) + '%';
      var lbl = document.getElementById('pcount');
      if (lbl) lbl.textContent = n + ' / ' + total;
    }
    var reset = document.getElementById('reset-btn');
    if (reset) reset.addEventListener('click', function () {
      if (confirm('Clear all lesson progress?')) { write({}); location.reload(); }
    });

    /* ---- keyboard paging ---- */
    document.addEventListener('keydown', function (e) {
      if (e.metaKey || e.ctrlKey || e.altKey) return;
      var tag = (e.target.tagName || '').toLowerCase();
      if (tag === 'input' || tag === 'textarea' || tag === 'select') return;
      var p = document.querySelector('.pager a.prev'), n = document.querySelector('.pager a.next');
      if (e.key === 'ArrowLeft' && p) location.href = p.href;
      if (e.key === 'ArrowRight' && n) location.href = n.href;
    });

    /* scroll the sidebar so the current lesson is visible */
    var here = document.querySelector('.sidebar a.here');
    if (here) {
      var sb = document.querySelector('.sidebar');
      if (sb && here.offsetTop > sb.clientHeight - 80) sb.scrollTop = here.offsetTop - sb.clientHeight / 2;
    }

    /* Notebook links, when this is served from GitHub Pages.
       The lab links are relative (../../C1 - .../foo.ipynb) so they work
       offline from file:// — which is the primary way this site is used.
       But Pages serves a .ipynb as a raw file, so the browser downloads it
       instead of showing it. On github.io only, point those links at the
       repo's blob view instead, which renders notebooks properly. */
    var host = location.hostname || '';
    var m = host.match(/^([^.]+)\.github\.io$/);
    if (m && location.pathname.indexOf('/study/') !== -1) {
      var user = m[1];
      var repo = location.pathname.split('/')[1];
      if (repo) {
        var base = 'https://github.com/' + user + '/' + repo + '/blob/main/';
        var links = document.querySelectorAll('a[href$=".ipynb"]');
        Array.prototype.forEach.call(links, function (a) {
          var raw = a.getAttribute('href');
          if (!raw || /^https?:/i.test(raw)) return;
          /* resolve the relative href, then re-root it onto the blob view */
          var abs = new URL(raw, location.href).pathname;
          var prefix = '/' + repo + '/';
          if (abs.indexOf(prefix) === 0) abs = abs.slice(prefix.length);
          a.setAttribute('href', base + abs);
          a.setAttribute('target', '_blank');
          a.setAttribute('rel', 'noopener');
        });
      }
    }
  });
})();
