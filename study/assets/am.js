/* Active Mastery — turns the server-rendered card grid into an app.

   PROGRESSIVE ENHANCEMENT. Every card's content is already in the DOM and
   visible before this file runs. All this does is hide the bodies, wire the
   grid, and move a body into a modal when you open it. With JS off you get a
   readable stack of sections and working <details>. Nothing here is the only
   copy of anything.

   State is per page, in localStorage under mls-am-<slug>. It records which
   cards you marked done — nothing else, and never anything you typed. */
(function () {
  'use strict';
  var root = document.getElementById('active-mastery');
  if (!root) return;

  var slug = (document.body.getAttribute('data-slug') || 'am');
  var KEY = 'mls-am-' + slug;
  var cards = [].slice.call(root.querySelectorAll('.am-card'));
  var total = cards.length;
  var reduce = window.matchMedia &&
               window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------------------------------------------------------- state */
  function load() {
    try { return JSON.parse(localStorage.getItem(KEY) || '[]') || []; }
    catch (e) { return []; }
  }
  function save(list) {
    try { localStorage.setItem(KEY, JSON.stringify(list)); } catch (e) {}
  }
  var done = load();
  function isDone(id) { return done.indexOf(id) >= 0; }
  function setDone(id, on) {
    var i = done.indexOf(id);
    if (on && i < 0) done.push(id);
    if (!on && i >= 0) done.splice(i, 1);
    save(done); paint();
  }

  /* ---------------------------------------------------------- progress */
  var ring = root.querySelector('.am-ring-fg');
  var nEl = root.querySelector('.am-done-n');
  var bar = root.querySelector('.am-bar-fill');
  var C = 2 * Math.PI * 31;
  if (ring) { ring.style.strokeDasharray = C; ring.style.strokeDashoffset = C; }

  function paint() {
    var n = 0;
    cards.forEach(function (c) {
      var on = isDone(c.getAttribute('data-am'));
      c.classList.toggle('is-done', on);
      var btn = c.querySelector('.am-card-btn');
      if (btn) btn.setAttribute('aria-pressed', on ? 'true' : 'false');
      if (on) n++;
    });
    if (nEl) nEl.textContent = n;
    var pct = total ? n / total : 0;
    if (ring) ring.style.strokeDashoffset = C * (1 - pct);
    if (bar) bar.style.width = (pct * 100) + '%';
    root.classList.toggle('is-complete', n === total && total > 0);
    var rst = root.querySelector('.am-reset');
    if (rst) rst.hidden = n === 0;
  }

  /* ---------------------------------------------------------- modal */
  var modal = document.createElement('div');
  modal.className = 'am-modal';   /* carries the --am-* tokens: content is
                                     MOVED here, so it leaves .am-root */
  modal.setAttribute('role', 'dialog');
  modal.setAttribute('aria-modal', 'true');
  modal.hidden = true;
  modal.innerHTML =
    '<div class="am-back" data-close></div>' +
    '<div class="am-sheet" role="document">' +
      '<header class="am-sheet-h">' +
        '<span class="am-sheet-ico"></span>' +
        '<div class="am-sheet-t"><span class="am-sheet-kind"></span>' +
        '<h3 class="am-sheet-title" id="am-modal-title"></h3></div>' +
        '<button type="button" class="am-x" data-close aria-label="close">' +
        '<svg viewBox="0 0 24 24" width="17" height="17"><path d="M6 6l12 12M18 6L6 18"' +
        ' fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/>' +
        '</svg></button>' +
      '</header>' +
      '<div class="am-sheet-b" tabindex="-1"></div>' +
      '<footer class="am-sheet-f">' +
        '<button type="button" class="am-nav am-prev">&#8592; Previous</button>' +
        '<button type="button" class="am-mark"><span class="am-mark-i">' +
        '<svg viewBox="0 0 24 24" width="14" height="14"><path d="M4 12.5l5.5 5.5L20 7"' +
        ' fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round"' +
        ' stroke-linejoin="round"/></svg></span><span class="am-mark-t">Mark done</span>' +
        '</button>' +
        '<button type="button" class="am-nav am-next">Next &#8594;</button>' +
      '</footer>' +
    '</div>';
  modal.setAttribute('aria-labelledby', 'am-modal-title');
  document.body.appendChild(modal);

  var sheet = modal.querySelector('.am-sheet');
  var sBody = modal.querySelector('.am-sheet-b');
  var sTitle = modal.querySelector('.am-sheet-title');
  var sKind = modal.querySelector('.am-sheet-kind');
  var sIco = modal.querySelector('.am-sheet-ico');
  var markBtn = modal.querySelector('.am-mark');
  var current = -1, lastFocus = null, host = null;

  function open(i, dir) {
    if (i < 0 || i >= total) return;
    if (current >= 0) stow();
    current = i;
    var card = cards[i];
    var body = card.querySelector('.am-card-body');
    host = card;
    sTitle.textContent = body.getAttribute('data-title') || '';
    sKind.textContent = card.getAttribute('data-kind') || '';
    sIco.innerHTML = body.getAttribute('data-ico') || '';
    sBody.appendChild(body);              /* move, so <details> state persists */
    body.hidden = false;
    modal.hidden = false;
    document.body.classList.add('am-open');
    sheet.setAttribute('data-dir', dir || '');
    if (!reduce) { sheet.classList.remove('am-in'); void sheet.offsetWidth;
                   sheet.classList.add('am-in'); }
    modal.querySelector('.am-prev').disabled = i === 0;
    modal.querySelector('.am-next').disabled = i === total - 1;
    syncMark();
    sBody.scrollTop = 0;
    sBody.focus();
  }

  function stow() {
    if (host) {
      var body = sBody.querySelector('.am-card-body');
      if (body) { body.hidden = true; host.appendChild(body); }
    }
    host = null;
  }

  function close() {
    stow();
    modal.hidden = true;
    current = -1;
    document.body.classList.remove('am-open');
    if (lastFocus) lastFocus.focus();
  }

  function syncMark() {
    var on = isDone(cards[current].getAttribute('data-am'));
    markBtn.classList.toggle('is-on', on);
    markBtn.setAttribute('aria-pressed', on ? 'true' : 'false');
    markBtn.querySelector('.am-mark-t').textContent = on ? 'Done' : 'Mark done';
  }

  markBtn.addEventListener('click', function () {
    if (current < 0) return;
    var id = cards[current].getAttribute('data-am');
    var now = !isDone(id);
    setDone(id, now);
    syncMark();
    if (now && !reduce) {
      markBtn.classList.remove('am-pop'); void markBtn.offsetWidth;
      markBtn.classList.add('am-pop');
    }
  });
  modal.querySelector('.am-prev').addEventListener('click', function () { open(current - 1, 'b'); });
  modal.querySelector('.am-next').addEventListener('click', function () { open(current + 1, 'f'); });

  modal.addEventListener('click', function (e) {
    if (e.target.closest('[data-close]')) close();
  });
  document.addEventListener('keydown', function (e) {
    if (modal.hidden) return;
    if (e.key === 'Escape') { close(); return; }
    if (e.key === 'ArrowRight' && !e.target.closest('.am-sheet-b')) open(current + 1, 'f');
    if (e.key === 'ArrowLeft' && !e.target.closest('.am-sheet-b')) open(current - 1, 'b');
    if (e.key === 'Tab') {                       /* focus trap */
      var f = sheet.querySelectorAll('button:not([disabled]), a[href], summary,' +
                                     ' [tabindex]:not([tabindex="-1"])');
      if (!f.length) return;
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
  });

  /* ---------------------------------------------------------- wire the grid */
  root.classList.add('am-js');            /* CSS hides the inline bodies now */
  cards.forEach(function (card, i) {
    card.querySelector('.am-card-body').hidden = true;
    card.querySelector('.am-card-btn').addEventListener('click', function () {
      lastFocus = this;
      open(i, '');
    });
  });

  var reset = root.querySelector('.am-reset');
  if (reset) reset.addEventListener('click', function () {
    done = []; save(done); paint();
  });

  /* Entrance animation lives entirely in CSS (see am-enter). Nothing here
     gates visibility on a callback, deliberately. */

  paint();
})();
