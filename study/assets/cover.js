/* Cover art — a neural network, drawn rather than illustrated.

   Layers of nodes with signals travelling the edges, coloured input → output.
   It is the subject of the book, so it earns its place as the cover; it is
   also generated, so it costs no image file and stays sharp at any size.
   Honours prefers-reduced-motion by drawing a single still frame. */
(function () {
  'use strict';
  document.addEventListener('DOMContentLoaded', function () {
    var cv = document.querySelector('canvas[data-cover]');
    if (!cv) return;
    var cx = null;
    try { cx = cv.getContext('2d'); } catch (e) { }
    if (!cx) return;                                  // no canvas: CSS bg stands alone

    var still = window.matchMedia &&
      window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var LAYERS = [5, 8, 8, 4], COL = ['#f0894c', '#e8b48a', '#8fbcf0', '#b697ef'];
    var nodes = [], edges = [], W = 0, H = 0, t0 = Date.now(), raf = 0;

    LAYERS.forEach(function (n, li) {
      for (var j = 0; j < n; j++) nodes.push({ l: li, j: j, n: n, ph: li * 7 + j * 3.1 });
    });
    nodes.forEach(function (a, ai) {
      nodes.forEach(function (b, bi) {
        if (b.l === a.l + 1) edges.push({ a: ai, b: bi, s: (ai * 13 + bi * 7) % 100 / 100 });
      });
    });

    function at(nd) {
      var padX = W * 0.17, spanX = W - padX * 2;
      var padY = H * 0.20, spanY = H - padY * 2;
      return {
        x: padX + (LAYERS.length === 1 ? .5 : nd.l / (LAYERS.length - 1)) * spanX,
        y: padY + (nd.n === 1 ? .5 : nd.j / (nd.n - 1)) * spanY
      };
    }

    function paint(t) {
      if (!W || !H) return;
      var g = cx.createLinearGradient(0, 0, W, H);
      g.addColorStop(0, '#14131a'); g.addColorStop(.5, '#191722'); g.addColorStop(1, '#101018');
      cx.fillStyle = g; cx.fillRect(0, 0, W, H);

      var rg = cx.createRadialGradient(W * .5, H * .46, 0, W * .5, H * .46, Math.max(W, H) * .62);
      rg.addColorStop(0, 'rgba(240,137,76,.15)'); rg.addColorStop(1, 'rgba(0,0,0,0)');
      cx.fillStyle = rg; cx.fillRect(0, 0, W, H);

      edges.forEach(function (e) {
        var a = at(nodes[e.a]), b = at(nodes[e.b]);
        cx.strokeStyle = 'rgba(200,190,225,.10)'; cx.lineWidth = 1;
        cx.beginPath(); cx.moveTo(a.x, a.y); cx.lineTo(b.x, b.y); cx.stroke();
        var p = ((t * 0.00013) + e.s) % 1;
        var px = a.x + (b.x - a.x) * p, py = a.y + (b.y - a.y) * p;
        var c = COL[nodes[e.b].l] || COL[0];
        var gd = cx.createRadialGradient(px, py, 0, px, py, 7);
        gd.addColorStop(0, c); gd.addColorStop(1, 'rgba(0,0,0,0)');
        cx.globalAlpha = .72; cx.fillStyle = gd;
        cx.beginPath(); cx.arc(px, py, 7, 0, 7); cx.fill(); cx.globalAlpha = 1;
      });

      nodes.forEach(function (nd) {
        var p = at(nd), c = COL[nd.l];
        var pulse = still ? 1 : (0.72 + 0.28 * Math.sin(t * 0.0016 + nd.ph));
        var glow = cx.createRadialGradient(p.x, p.y, 0, p.x, p.y, 17 * pulse);
        glow.addColorStop(0, c); glow.addColorStop(1, 'rgba(0,0,0,0)');
        cx.globalAlpha = .30 * pulse; cx.fillStyle = glow;
        cx.beginPath(); cx.arc(p.x, p.y, 17 * pulse, 0, 7); cx.fill();
        cx.globalAlpha = 1; cx.fillStyle = c;
        cx.beginPath(); cx.arc(p.x, p.y, 3.1, 0, 7); cx.fill();
      });

      var vg = cx.createRadialGradient(W * .5, H * .5, Math.min(W, H) * .30,
                                       W * .5, H * .5, Math.max(W, H) * .78);
      vg.addColorStop(0, 'rgba(0,0,0,0)'); vg.addColorStop(1, 'rgba(0,0,0,.62)');
      cx.fillStyle = vg; cx.fillRect(0, 0, W, H);
    }

    function size() {
      var d = window.devicePixelRatio || 1;
      W = cv.clientWidth; H = cv.clientHeight;
      if (!W || !H) return;
      cv.width = W * d; cv.height = H * d; cx.setTransform(d, 0, 0, d, 0, 0);
      if (still) paint(0);
    }

    function loop() { paint(Date.now() - t0); raf = requestAnimationFrame(loop); }

    /* ---- full screen ---- */
    var shell = cv.closest('.cover');
    var fsBtn = shell && shell.querySelector('[data-cover-fs]');
    function fsOn() { return document.fullscreenElement === shell; }
    function toggleFs() {
      if (!shell) return;
      try {
        if (fsOn()) (document.exitFullscreen || document.webkitExitFullscreen).call(document);
        else (shell.requestFullscreen || shell.webkitRequestFullscreen).call(shell);
      } catch (e) { }           /* iOS Safari refuses on non-video: leave as-is */
    }
    if (fsBtn) {
      /* hide the control outright where the API does not exist, rather than
         offering a button that silently does nothing */
      if (!(shell.requestFullscreen || shell.webkitRequestFullscreen)) fsBtn.style.display = 'none';
      else fsBtn.addEventListener('click', toggleFs);
    }
    document.addEventListener('fullscreenchange', function () {
      if (fsBtn) {
        fsBtn.innerHTML = fsOn() ? '&#10005;' : '&#9974;';
        fsBtn.setAttribute('aria-label', fsOn() ? 'Leave full screen' : 'Full screen');
      }
      size();
    });

    var nextBtn = shell && shell.querySelector('[data-cover-next]');
    if (nextBtn) nextBtn.addEventListener('click', function () {
      if (fsOn()) { toggleFs(); return; }
      var after = shell.nextElementSibling;
      if (after) after.scrollIntoView({ behavior: still ? 'auto' : 'smooth', block: 'start' });
    });

    document.addEventListener('keydown', function (e) {
      if (e.metaKey || e.ctrlKey || e.altKey) return;
      var tag = (e.target.tagName || '').toLowerCase();
      if (tag === 'input' || tag === 'textarea' || tag === 'select') return;
      if (e.key === 'f') { e.preventDefault(); toggleFs(); }
    });

    window.addEventListener('resize', size);
    size();
    if (still) return;                                  // one frame, no loop
    /* stop animating when the cover is off-screen — it sits at the top of a
       long page and there is no reason to burn a phone battery below the fold */
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es) {
        es.forEach(function (en) {
          if (en.isIntersecting && !raf) loop();
          else if (!en.isIntersecting && raf) { cancelAnimationFrame(raf); raf = 0; }
        });
      }, { threshold: 0.01 }).observe(cv);
    } else loop();
  });
})();
