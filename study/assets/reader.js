/* Reader mode — the book shell.

   Turns a lesson page into viewport-sized pages you turn, instead of one long
   scroll. The unit is the authored <h2> section, never a pixel measurement:
   splitting by height would cut a code block or a canvas widget in half, and
   every lesson already has 5–11 sections written as natural boundaries.

   Nothing is removed or rebuilt — sections are shown and hidden in place, so
   every widget, term popup, quiz and cross-reference keeps working untouched.
   If anything here fails the page is left exactly as it was: a normal scroll. */
(function () {
  'use strict';
  var KEY = 'mls-reader-v1';       // on/off
  var POSKEY = 'mls-readpos-v1';   // {slug: sectionIndex}

  function on() { try { return localStorage.getItem(KEY) !== '0'; } catch (e) { return true; } }
  function setOn(v) { try { localStorage.setItem(KEY, v ? '1' : '0'); } catch (e) { } }
  function readPos() { try { return JSON.parse(localStorage.getItem(POSKEY) || '{}'); } catch (e) { return {}; } }
  function savePos(slug, i) {
    if (!slug) return;
    try { var o = readPos(); o[slug] = i; localStorage.setItem(POSKEY, JSON.stringify(o)); } catch (e) { }
  }

  document.addEventListener('DOMContentLoaded', function () {
    var main = document.querySelector('main');
    if (!main || !document.body.dataset.slug) return;       // lessons only
    var h2s = [].slice.call(main.querySelectorAll(':scope > h2'));
    if (h2s.length < 3) return;                             // not a lesson shape

    var slug = document.body.dataset.slug;
    var head = [], leaves = [], pager = main.querySelector('.pager');
    var foot = main.querySelector('.sitefoot');

    /* everything before the first h2 is the title block; keep it on every page */
    var node = main.firstElementChild;
    while (node && node !== h2s[0]) { head.push(node); node = node.nextElementSibling; }

    /* group each h2 with the nodes that follow it, into one leaf per section */
    h2s.forEach(function (h, i) {
      var wrap = document.createElement('section');
      wrap.className = 'rd-leaf';
      var stop = h2s[i + 1] || pager || foot;
      var n = h, next;
      var members = [];
      while (n && n !== stop) { members.push(n); n = n.nextElementSibling; }
      h.parentNode.insertBefore(wrap, members[0]);
      members.forEach(function (m) { wrap.appendChild(m); });
      leaves.push(wrap);
    });
    if (!leaves.length) return;

    /* ---- chrome ---- */
    var bar = document.createElement('div');
    bar.className = 'rd-bar';
    bar.innerHTML =
      '<button class="rd-nav" data-rd="prev" aria-label="Previous section">‹</button>' +
      '<div class="rd-track"><i></i></div>' +
      '<span class="rd-cnt" aria-live="polite"></span>' +
      '<button class="rd-nav" data-rd="next" aria-label="Next section">›</button>' +
      '<button class="rd-nav rd-x" data-rd="off" title="Leave reader mode (r)">≡</button>';
    document.body.appendChild(bar);

    var fill = bar.querySelector('.rd-track i'), cnt = bar.querySelector('.rd-cnt');
    var bPrev = bar.querySelector('[data-rd="prev"]'), bNext = bar.querySelector('[data-rd="next"]');
    var zoneL = document.createElement('div'), zoneR = document.createElement('div');
    zoneL.className = 'rd-zone l'; zoneR.className = 'rd-zone r';
    zoneL.setAttribute('aria-hidden', 'true'); zoneR.setAttribute('aria-hidden', 'true');
    document.body.appendChild(zoneL); document.body.appendChild(zoneR);

    var at = 0, live = false;

    function label(i) {
      var h = leaves[i].querySelector('h2');
      if (!h) return 'Section ' + (i + 1);
      /* the heading is <span class="ico">EMOJI</span>Watch it move — take the
         text after the icon span, not textContent, which has no separator and
         would swallow the first real word along with the emoji */
      var t = '';
      [].forEach.call(h.childNodes, function (n) {
        if (n.nodeType === 1 && n.classList && n.classList.contains('ico')) return;
        t += n.textContent || '';
      });
      return t.trim() || ('Section ' + (i + 1));
    }

    function go(i, remember) {
      at = Math.max(0, Math.min(leaves.length - 1, i));
      leaves.forEach(function (l, k) { l.classList.toggle('on', k === at); });
      fill.style.width = ((at + 1) / leaves.length * 100) + '%';
      cnt.textContent = (at + 1) + ' / ' + leaves.length + '  ·  ' + label(at);
      bPrev.disabled = at === 0;
      bNext.disabled = at === leaves.length - 1;
      if (pager) pager.classList.toggle('rd-show', at === leaves.length - 1);
      window.scrollTo(0, 0);
      if (remember !== false) savePos(slug, at);
      /* canvas widgets size themselves from clientWidth — nudge the one now visible */
      window.dispatchEvent(new Event('resize'));
    }

    function enable(startAt) {
      document.body.classList.add('rd-on');
      live = true;
      go(typeof startAt === 'number' ? startAt : (readPos()[slug] || 0), false);
    }
    function disable() {
      document.body.classList.remove('rd-on');
      live = false;
      leaves.forEach(function (l) { l.classList.remove('on'); });
      if (pager) pager.classList.remove('rd-show');
      setOn(false);
    }

    bar.addEventListener('click', function (e) {
      var b = e.target.closest('[data-rd]'); if (!b) return;
      if (b.dataset.rd === 'prev') go(at - 1);
      if (b.dataset.rd === 'next') go(at + 1);
      if (b.dataset.rd === 'off') disable();
    });
    zoneL.addEventListener('click', function () { go(at - 1); });
    zoneR.addEventListener('click', function () { go(at + 1); });

    document.addEventListener('keydown', function (e) {
      if (e.metaKey || e.ctrlKey || e.altKey) return;
      var tag = (e.target.tagName || '').toLowerCase();
      if (tag === 'input' || tag === 'textarea' || tag === 'select') return;
      if (e.key === 'r') { live ? disable() : (setOn(true), enable()); return; }
      if (!live) return;
      /* inside reader mode the arrows turn sections; site.js paging still runs
         at the ends, which is what carries you into the next lesson */
      if (e.key === 'ArrowRight' && at < leaves.length - 1) { e.stopPropagation(); e.preventDefault(); go(at + 1); }
      if (e.key === 'ArrowLeft' && at > 0) { e.stopPropagation(); e.preventDefault(); go(at - 1); }
    }, true);

    var sx = 0, sy = 0;
    document.addEventListener('touchstart', function (e) {
      sx = e.touches[0].clientX; sy = e.touches[0].clientY;
    }, { passive: true });
    document.addEventListener('touchend', function (e) {
      if (!live) return;
      var dx = e.changedTouches[0].clientX - sx, dy = e.changedTouches[0].clientY - sy;
      if (Math.abs(dx) > 55 && Math.abs(dx) > Math.abs(dy) * 1.6) go(at + (dx < 0 ? 1 : -1));
    }, { passive: true });

    if (on()) enable();
  });
})();
