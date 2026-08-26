/* Little refresher notes.
   A term that the course uses but never explains (cos, radians, Pythagoras…),
   or a symbol that Foundations taught a while back (Σ, ∂J/∂w, a dot product…),
   gets a small badge beside its first mention on a page. On a real mouse it
   opens the moment you hover; on touch or keyboard, a tap or Enter does it.

   Data comes from assets/gloss-data.js, generated from every REFRESHER_MODULES
   entry in _build/build.py (content_trig, content_f0ref, …). */
(function () {
  'use strict';
  var pop = null, open = null;
  var showTimer = null, hideTimer = null;
  var HOVER_SHOW = 80, HOVER_HIDE = 220;
  var CAN_HOVER = window.matchMedia && window.matchMedia('(hover: hover) and (pointer: fine)').matches;

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }

  function build() {
    pop = document.createElement('div');
    pop.className = 'gpop';
    pop.setAttribute('role', 'dialog');
    pop.setAttribute('aria-modal', 'false');
    pop.innerHTML = '<button class="gpop-x" aria-label="close">&times;</button><div class="gpop-b"></div>';
    document.body.appendChild(pop);
    pop.querySelector('.gpop-x').addEventListener('click', close);
    pop.addEventListener('click', function (e) { e.stopPropagation(); });
    if (CAN_HOVER) {
      pop.addEventListener('mouseenter', cancelHide);
      pop.addEventListener('mouseleave', scheduleHide);
    }
  }

  function cancelHide() {
    if (hideTimer) { clearTimeout(hideTimer); hideTimer = null; }
  }

  function scheduleHide() {
    cancelHide();
    hideTimer = setTimeout(close, HOVER_HIDE);
  }

  function close() {
    if (showTimer) { clearTimeout(showTimer); showTimer = null; }
    cancelHide();
    if (!pop) return;
    pop.classList.remove('on');
    document.body.classList.remove('gpop-open');
    if (open) { open.setAttribute('aria-expanded', 'false'); open = null; }
  }

  function place(el) {
    /* Below the term if it fits, above if it does not. On a narrow screen the
       CSS turns this into a sheet pinned to the bottom, so skip positioning. */
    if (window.matchMedia('(max-width: 640px)').matches) {
      pop.style.left = ''; pop.style.top = '';
      return;
    }
    var r = el.getBoundingClientRect();
    var w = pop.offsetWidth, h = pop.offsetHeight;
    var left = r.left + window.scrollX + r.width / 2 - w / 2;
    left = Math.max(12, Math.min(left, window.innerWidth - w - 12));
    var below = r.bottom + window.scrollY + 10;
    var above = r.top + window.scrollY - h - 10;
    var fitsBelow = r.bottom + h + 20 < window.innerHeight;
    pop.style.left = left + 'px';
    pop.style.top = (fitsBelow || above < window.scrollY ? below : above) + 'px';
    pop.classList.toggle('above', !fitsBelow && above >= window.scrollY);
  }

  function show(el) {
    var g = (window.GLOSS || {})[el.dataset.g];
    if (!g) return;
    if (!pop) build();
    if (open && open !== el) open.setAttribute('aria-expanded', 'false');
    pop.querySelector('.gpop-b').innerHTML =
      '<div class="gpop-h"><b>' + esc(g.label) + '</b><i>' + esc(g.say) + '</i></div>' +
      '<p class="gpop-gist">' + g.gist + '</p>' +
      g.body +
      (g.ml ? '<p class="gpop-ml"><span>where it turns up</span>' + g.ml + '</p>' : '') +
      '<a class="gpop-more" href="' + (window.GLOSS_UP || '') + (g.moreHref || 'reference.html#trig') + '">' +
      esc(g.moreLabel || 'the whole refresher') + ' &#8594;</a>';
    pop.classList.add('on');
    document.body.classList.add('gpop-open');
    open = el;
    el.setAttribute('aria-expanded', 'true');
    place(el);
  }

  function toggle(el) {
    if (open === el) { close(); return; }
    show(el);
  }

  document.addEventListener('DOMContentLoaded', function () {
    var terms = document.querySelectorAll('.gterm[data-g]');
    if (!terms.length) return;
    terms.forEach(function (el) {
      el.setAttribute('tabindex', '0');
      el.setAttribute('role', 'button');
      el.setAttribute('aria-expanded', 'false');
      el.addEventListener('click', function (e) { e.stopPropagation(); toggle(el); });
      el.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggle(el); }
      });
      if (CAN_HOVER) {
        el.addEventListener('mouseenter', function () {
          cancelHide();
          if (showTimer) clearTimeout(showTimer);
          showTimer = setTimeout(function () { showTimer = null; show(el); }, HOVER_SHOW);
        });
        el.addEventListener('mouseleave', function () {
          if (showTimer) { clearTimeout(showTimer); showTimer = null; }
          if (open === el) scheduleHide();
        });
      }
    });
    document.addEventListener('click', close);
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
    window.addEventListener('resize', close);
  });
})();
