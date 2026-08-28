/* ============================================================
   Tiny animation runtime for the study site.
   - No dependencies, works from file://
   - Widgets are registered with A.def(name, fn) and mounted on
     any element carrying   data-anim="name"
   - Re-renders automatically on resize + light/dark theme change
   ============================================================ */
(function (global) {
  'use strict';

  var A = {};
  A.widgets = {};
  A.def = function (name, fn) { A.widgets[name] = fn; };

  /* ---------- math helpers ---------- */
  A.clamp = function (v, a, b) { return v < a ? a : v > b ? b : v; };
  A.lerp = function (a, b, t) { return a + (b - a) * t; };
  A.map = function (v, a, b, c, d) { return c + (v - a) / (b - a) * (d - c); };
  A.ease = function (t) { return t < .5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2; };
  A.sig = function (z) { return 1 / (1 + Math.exp(-z)); };
  A.relu = function (z) { return z > 0 ? z : 0; };
  A.fmt = function (v, n) { n = n == null ? 2 : n; var s = v.toFixed(n); return s === '-0.00' ? '0.00' : s; };

  /* ---------- theme colours ---------- */
  var _cache = {};
  A.c = function (name) {
    if (_cache[name]) return _cache[name];
    var v = getComputedStyle(document.documentElement).getPropertyValue('--' + name).trim();
    _cache[name] = v || '#888';
    return _cache[name];
  };
  A.pal = function () {
    return {
      ink: A.c('ink'), soft: A.c('ink-soft'), faint: A.c('ink-faint'),
      line: A.c('line'), lineSoft: A.c('line-soft'),
      panel: A.c('bg-panel'), sunk: A.c('bg-sunk'), bg: A.c('bg'),
      a: A.c('accent'), aS: A.c('accent-soft'),
      b: A.c('blue'), bS: A.c('blue-soft'),
      g: A.c('green'), gS: A.c('green-soft'),
      p: A.c('purple'), pS: A.c('purple-soft'),
      m: A.c('amber'), mS: A.c('amber-soft'),
      r: A.c('red'), rS: A.c('red-soft')
    };
  };


  /* ---------- transport: play / pause / scrub -------------------
     Every auto-playing widget gets one. An animation you cannot stop
     is a thing that happens AT you; one you can scrub is a thing you
     can interrogate — step back to the frame that confused you and
     hold it there. ------------------------------------------------ */
  A.autoplay = function (root, c, render, opt) {
    opt = opt || {};
    var span = opt.span || 16;          /* seconds of timeline on the scrubber */
    var lt = 0, paused = false, lp = null;

    var bar = document.createElement('div');
    bar.className = 'transport';

    var btn = document.createElement('button');
    btn.className = 'btn tp';

    var inp = document.createElement('input');
    inp.type = 'range'; inp.min = 0; inp.max = span; inp.step = 0.02; inp.value = 0;
    inp.className = 'tp-scrub';
    inp.setAttribute('aria-label', 'scrub the animation');

    var tag = document.createElement('span');
    tag.className = 'tp-tag';

    function paint() { render(lt); }
    function setPaused(v) {
      paused = v;
      btn.textContent = v ? '\u25b6' : '\u275a\u275a';
      btn.setAttribute('aria-label', v ? 'play the animation' : 'pause the animation');
      btn.classList.toggle('primary', v);
      tag.textContent = v ? 'paused \u2014 drag to scrub' : 'playing';
      if (lp) lp.toggle(!v);
    }
    btn.addEventListener('click', function () { setPaused(!paused); });
    inp.addEventListener('input', function () {
      if (!paused) setPaused(true);
      lt = parseFloat(inp.value);
      paint();
    });

    bar.appendChild(btn); bar.appendChild(inp); bar.appendChild(tag);
    /* sit directly under the canvas, above any sliders and the readout */
    if (root.insertBefore && c.cv) root.insertBefore(bar, c.cv.nextSibling);
    else root.appendChild(bar);
    setPaused(false);

    A.bind(c, paint);
    lp = A.loop(c.cv, function (t) {
      if (paused) return;
      lt = t; inp.value = (t % span).toFixed(2); render(t);
    });
    return { paint: paint, pause: function () { setPaused(true); } };
  };


  /* ---------- log: a live numeric trace that replaces itself -----
     For widgets that actually run an algorithm (not just animate a
     diagram): a single line showing THIS step's real computed values.
     Each .set() call overwrites the line rather than appending, so a
     long-running loop never grows the page — it is a status line, not
     a scrollback. .set()'s second argument, if given, is shown as a
     tooltip on the line: the symbolic formula this step's numbers are
     an instance of. ------------------------------------------------ */
  A.log = function (root, opt) {
    opt = opt || {};
    var box = document.createElement('div');
    box.className = 'alglog';
    var line = document.createElement('span');
    line.className = 'alglog-line';
    box.appendChild(line);
    root.appendChild(box);
    return {
      el: box,
      set: function (html, formula) {
        line.innerHTML = html;
        box.title = formula || '';
        box.classList.toggle('has-formula', !!formula);
      }
    };
  };

  /* ---------- canvas ---------- */
  A.canvas = function (root, w, h) {
    var cv = document.createElement('canvas');
    cv.style.width = '100%';
    cv.style.aspectRatio = w + ' / ' + h;
    root.appendChild(cv);
    var o = { cv: cv, ctx: cv.getContext('2d'), W: w, H: h, dpr: 1 };
    o.fit = function () {
      var dpr = Math.min(global.devicePixelRatio || 1, 2);
      var cssW = cv.clientWidth || w;
      var scale = cssW / w;
      cv.width = Math.round(w * dpr * scale);
      cv.height = Math.round(h * dpr * scale);
      o.dpr = dpr * scale;
      o.ctx.setTransform(o.dpr, 0, 0, o.dpr, 0, 0);
    };
    o.clear = function (bg) {
      o.ctx.save(); o.ctx.setTransform(1, 0, 0, 1, 0, 0);
      o.ctx.clearRect(0, 0, cv.width, cv.height); o.ctx.restore();
      if (bg) { o.ctx.fillStyle = bg; o.ctx.fillRect(0, 0, w, h); }
    };
    /* pointer position in design coordinates */
    o.pt = function (ev) {
      var r = cv.getBoundingClientRect();
      var t = ev.touches ? ev.touches[0] : ev;
      return { x: (t.clientX - r.left) / r.width * w, y: (t.clientY - r.top) / r.height * h };
    };
    o.fit();
    return o;
  };

  /* ---------- drawing sugar ---------- */
  A.rr = function (ctx, x, y, w, h, r) {
    r = Math.min(r, Math.abs(w) / 2, Math.abs(h) / 2);
    ctx.beginPath();
    ctx.moveTo(x + r, y);
    ctx.arcTo(x + w, y, x + w, y + h, r);
    ctx.arcTo(x + w, y + h, x, y + h, r);
    ctx.arcTo(x, y + h, x, y, r);
    ctx.arcTo(x, y, x + w, y, r);
    ctx.closePath();
  };
  /* Canvas cannot fall back glyph-by-glyph the way HTML can: if the chosen
     font lacks a character, fillText draws a tofu box and there is no recovery.
     The two stacks we use have different gaps (checked with fontTools against
     the fonts macOS ships), so swap per-stack before drawing.

       both      U+20D7 x-vector arrow, U+27FA and U+21D4  — no font has these
       SF Pro    lacks U+2C7C subscript j
       Menlo     lacks U+2099 / U+2098 subscript n and m

     Use A.overArrow to draw a vector arrow properly. */
  var SAFE_BOTH = {
    '\u20d7': '',        /* x⃗  combining arrow — no font on macOS has it     */
    '\u27fa': '\u2194',  /* ⟺ -> ↔                                          */
    '\u21d4': '\u2194',  /* ⇔ -> ↔  (SF Pro lacks ⇔)                        */
    '\u27f9': '\u2192',  /* ⟹ -> →                                          */
    '\u21d2': '\u2192'   /* ⇒ -> →  (SF Pro lacks ⇒)                        */
  };
  var SAFE_SANS = { '\u2c7c': 'j' };                       /* SF Pro lacks ⱼ   */
  var SAFE_MONO = { '\u2099': 'n', '\u2098': 'm',          /* Menlo lacks ₙ ₘ  */
                    '\u2016': '||' };                      /* Menlo lacks ‖    */

  A.safe = function (s, mono) {
    s = String(s);
    var map = mono ? SAFE_MONO : SAFE_SANS, k;
    for (k in SAFE_BOTH) if (s.indexOf(k) >= 0) s = s.split(k).join(SAFE_BOTH[k]);
    for (k in map) if (s.indexOf(k) >= 0) s = s.split(k).join(map[k]);
    return s;
  };

  /* A short arrow drawn above a letter — the x⃗ mark, which no font provides. */
  A.overArrow = function (ctx, x, y, w, col) {
    w = w || 9;
    ctx.save();
    ctx.strokeStyle = col || A.c('ink');
    ctx.fillStyle = ctx.strokeStyle;
    ctx.lineWidth = 1.1;
    ctx.beginPath();
    ctx.moveTo(x, y); ctx.lineTo(x + w, y); ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(x + w, y); ctx.lineTo(x + w - 3, y - 2.2); ctx.lineTo(x + w - 3, y + 2.2);
    ctx.closePath(); ctx.fill();
    ctx.restore();
  };

  A.txt = function (ctx, s, x, y, opt) {
    opt = opt || {};
    s = A.safe(s, opt.mono);
    ctx.save();
    ctx.fillStyle = opt.fill || A.c('ink');
    ctx.font = (opt.w || 500) + ' ' + (opt.size || 13) + 'px ' + (opt.mono
      ? 'ui-monospace, Menlo, monospace'
      : '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif');
    ctx.textAlign = opt.align || 'left';
    ctx.textBaseline = opt.base || 'alphabetic';
    ctx.fillText(s, x, y);
    ctx.restore();
  };
  A.line = function (ctx, x1, y1, x2, y2, col, w, dash) {
    ctx.save();
    ctx.strokeStyle = col; ctx.lineWidth = w || 1;
    if (dash) ctx.setLineDash(dash);
    ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.stroke();
    ctx.restore();
  };
  A.dot = function (ctx, x, y, r, col) {
    ctx.save(); ctx.fillStyle = col; ctx.beginPath();
    ctx.arc(x, y, r, 0, 6.2832); ctx.fill(); ctx.restore();
  };
  A.arrow = function (ctx, x1, y1, x2, y2, col, w) {
    w = w || 1.6;
    var a = Math.atan2(y2 - y1, x2 - x1), hl = 7 + w;
    ctx.save(); ctx.strokeStyle = col; ctx.fillStyle = col; ctx.lineWidth = w;
    ctx.beginPath(); ctx.moveTo(x1, y1);
    ctx.lineTo(x2 - Math.cos(a) * hl * .8, y2 - Math.sin(a) * hl * .8); ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(x2, y2);
    ctx.lineTo(x2 - hl * Math.cos(a - .38), y2 - hl * Math.sin(a - .38));
    ctx.lineTo(x2 - hl * Math.cos(a + .38), y2 - hl * Math.sin(a + .38));
    ctx.closePath(); ctx.fill(); ctx.restore();
  };
  /* axes helper: returns scale functions */
  A.axes = function (ctx, box, xr, yr, opt) {
    opt = opt || {};
    var P = A.pal();
    var X = function (v) { return A.map(v, xr[0], xr[1], box.x, box.x + box.w); };
    var Y = function (v) { return A.map(v, yr[0], yr[1], box.y + box.h, box.y); };
    ctx.save();
    ctx.strokeStyle = P.lineSoft; ctx.lineWidth = 1;
    var i, xs = opt.xticks || 5, ys = opt.yticks || 4;
    for (i = 0; i <= xs; i++) {
      var xv = xr[0] + (xr[1] - xr[0]) * i / xs;
      A.line(ctx, X(xv), box.y, X(xv), box.y + box.h, P.lineSoft, 1);
      if (opt.xfmt) A.txt(ctx, opt.xfmt(xv), X(xv), box.y + box.h + 15,
        { align: 'center', size: 11, fill: P.faint });
    }
    for (i = 0; i <= ys; i++) {
      var yv = yr[0] + (yr[1] - yr[0]) * i / ys;
      A.line(ctx, box.x, Y(yv), box.x + box.w, Y(yv), P.lineSoft, 1);
      if (opt.yfmt) A.txt(ctx, opt.yfmt(yv), box.x - 7, Y(yv) + 4,
        { align: 'right', size: 11, fill: P.faint });
    }
    ctx.strokeStyle = P.line; ctx.lineWidth = 1.4;
    ctx.beginPath();
    ctx.moveTo(box.x, box.y); ctx.lineTo(box.x, box.y + box.h);
    ctx.lineTo(box.x + box.w, box.y + box.h); ctx.stroke();
    if (opt.xlab) A.txt(ctx, opt.xlab, box.x + box.w / 2, box.y + box.h + 33,
      { align: 'center', size: 12, w: 600, fill: P.soft });
    if (opt.ylab) {
      ctx.save(); ctx.translate(box.x - 40, box.y + box.h / 2); ctx.rotate(-Math.PI / 2);
      A.txt(ctx, opt.ylab, 0, 0, { align: 'center', size: 12, w: 600, fill: P.soft });
      ctx.restore();
    }
    ctx.restore();
    return { X: X, Y: Y };
  };
  /* plot a function y=f(x) */
  A.plot = function (ctx, S, xr, f, col, w, dash) {
    ctx.save(); ctx.strokeStyle = col; ctx.lineWidth = w || 2.2;
    if (dash) ctx.setLineDash(dash);
    ctx.beginPath();
    var n = 220, started = false;
    for (var i = 0; i <= n; i++) {
      var xv = xr[0] + (xr[1] - xr[0]) * i / n, yv = f(xv);
      if (!isFinite(yv)) { started = false; continue; }
      var px = S.X(xv), py = S.Y(yv);
      if (!started) { ctx.moveTo(px, py); started = true; } else ctx.lineTo(px, py);
    }
    ctx.stroke(); ctx.restore();
  };

  /* ---------- network / matrix drawing (shared by widget files) ---------- */
  A.col = function (x, n, top, bot, r) {
    var out = [], i;
    if (n === 1) return [{ x: x, y: (top + bot) / 2, r: r }];
    for (i = 0; i < n; i++) out.push({ x: x, y: top + (bot - top) * i / (n - 1), r: r });
    return out;
  };
  A.link = function (ctx, p, q, colr, w, alpha) {
    ctx.save(); ctx.globalAlpha = alpha == null ? 1 : alpha;
    ctx.strokeStyle = colr; ctx.lineWidth = w;
    ctx.beginPath(); ctx.moveTo(p.x + p.r, p.y); ctx.lineTo(q.x - q.r, q.y); ctx.stroke(); ctx.restore();
  };
  A.neuron = function (ctx, p, a, P, label, sub, ring) {
    ctx.save();
    ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, 6.2832); ctx.fillStyle = P.panel; ctx.fill();
    ctx.globalAlpha = .15 + .85 * A.clamp(a, 0, 1);
    ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, 6.2832); ctx.fillStyle = ring || P.a; ctx.fill();
    ctx.globalAlpha = 1; ctx.lineWidth = 1.6; ctx.strokeStyle = ring || P.a;
    ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, 6.2832); ctx.stroke(); ctx.restore();
    if (label != null) A.txt(ctx, label, p.x, p.y + 4,
      { align: 'center', size: 11.5, mono: true, w: 700, fill: a > .55 ? P.panel : P.ink });
    if (sub) A.txt(ctx, sub, p.x, p.y + p.r + 15, { align: 'center', size: 11, fill: P.faint });
  };
  A.pulse = function (ctx, p, q, t, colr, R) {
    var u = t % 1;
    A.dot(ctx, A.lerp(p.x + p.r, q.x - q.r, u), A.lerp(p.y, q.y, u), R || 3, colr);
  };
  A.matrix = function (ctx, x, y, rows, cols, cw, ch, P, get, opt) {
    opt = opt || {};
    var i, j;
    for (i = 0; i < rows; i++) for (j = 0; j < cols; j++) {
      var cx = x + j * cw, cy = y + i * ch;
      var st = opt.state ? opt.state(i, j) : 0;
      A.rr(ctx, cx, cy, cw - 3, ch - 3, 5);
      ctx.fillStyle = st === 1 ? P.aS : st === 2 ? P.bS : st === 3 ? P.gS : st === 4 ? P.rS : P.sunk;
      ctx.fill();
      ctx.strokeStyle = st === 1 ? P.a : st === 2 ? P.b : st === 3 ? P.g : st === 4 ? P.r : P.lineSoft;
      ctx.lineWidth = st ? 1.8 : 1; ctx.stroke();
      var v = get(i, j);
      if (v !== null && v !== undefined)
        A.txt(ctx, v, cx + (cw - 3) / 2, cy + (ch - 3) / 2 + 4,
          { align: 'center', size: opt.size || 12, mono: true, w: st ? 700 : 500,
            fill: st === 1 ? P.a : st === 2 ? P.b : st === 3 ? P.g : st === 4 ? P.r : P.soft });
    }
    var W = cols * cw - 3, H = rows * ch - 3;
    ctx.save(); ctx.strokeStyle = P.faint; ctx.lineWidth = 1.8; ctx.beginPath();
    ctx.moveTo(x - 7, y - 4); ctx.lineTo(x - 11, y - 4); ctx.lineTo(x - 11, y + H + 4); ctx.lineTo(x - 7, y + H + 4);
    ctx.moveTo(x + W + 7, y - 4); ctx.lineTo(x + W + 11, y - 4); ctx.lineTo(x + W + 11, y + H + 4); ctx.lineTo(x + W + 7, y + H + 4);
    ctx.stroke(); ctx.restore();
    if (opt.label) A.txt(ctx, opt.label, x + W / 2, y - 14, { align: 'center', size: 12, w: 700, fill: opt.labelColor || P.soft });
    if (opt.shape) A.txt(ctx, opt.shape, x + W / 2, y + H + 22, { align: 'center', size: 11, mono: true, fill: P.faint });
    return { w: W, h: H };
  };

  /* ---------- controls ---------- */
  A.ctrls = function (root) {
    var d = document.createElement('div'); d.className = 'ctrls';
    root.appendChild(d); return d;
  };
  A.slider = function (bar, opt) {
    var wrap = document.createElement('div'); wrap.className = 'ctrl';
    var lab = document.createElement('label'); lab.innerHTML = opt.label;
    var inp = document.createElement('input');
    inp.type = 'range'; inp.min = opt.min; inp.max = opt.max;
    inp.step = opt.step == null ? .01 : opt.step; inp.value = opt.value;
    var out = document.createElement('output');
    var fmt = opt.fmt || function (v) { return A.fmt(v, 2); };
    function sync() { out.textContent = fmt(parseFloat(inp.value)); }
    inp.addEventListener('input', function () { sync(); opt.on(parseFloat(inp.value)); });
    sync();
    wrap.appendChild(lab); wrap.appendChild(inp); wrap.appendChild(out);
    bar.appendChild(wrap);
    return { el: inp, set: function (v) { inp.value = v; sync(); }, get: function(){ return parseFloat(inp.value); } };
  };
  A.button = function (bar, label, on) {
    var b = document.createElement('button');
    b.className = 'btn'; b.textContent = label;
    b.addEventListener('click', function () { on(b); });
    bar.appendChild(b); return b;
  };
  A.toggle = function (bar, label, on, init) {
    var b = A.button(bar, label, function () {
      b.dataset.on = b.dataset.on === '1' ? '0' : '1';
      b.classList.toggle('primary', b.dataset.on === '1');
      on(b.dataset.on === '1');
    });
    b.dataset.on = init ? '1' : '0';
    b.classList.toggle('primary', !!init);
    return b;
  };
  A.readout = function (root) {
    var d = document.createElement('div'); d.className = 'readout';
    root.appendChild(d);
    return { el: d, set: function (h) { d.innerHTML = h; } };
  };
  A.legend = function (root, items) {
    var d = document.createElement('div'); d.className = 'legend';
    d.innerHTML = items.map(function (it) {
      return '<span><i style="background:' + it[0] + '"></i>' + it[1] + '</span>';
    }).join('');
    root.appendChild(d); return d;
  };

  /* ---------- render registry (resize + theme) ---------- */
  var renders = [];
  A.bind = function (obj, render) {
    renders.push({ o: obj, r: render });
    if (global.ResizeObserver && obj.cv) {
      var ro = new ResizeObserver(function () { obj.fit(); render(); });
      ro.observe(obj.cv);
    }
  };
  A.redrawAll = function () {
    _cache = {};
    renders.forEach(function (x) { if (x.o && x.o.fit) x.o.fit(); x.r(); });
  };
  if (global.matchMedia) {
    try {
      global.matchMedia('(prefers-color-scheme: dark)')
        .addEventListener('change', function () { setTimeout(A.redrawAll, 30); });
    } catch (e) { /* older Safari */ }
  }
  global.addEventListener('themechange', function () { setTimeout(A.redrawAll, 30); });

  /* ---------- animation loop (pauses when off-screen) ---------- */
  A.loop = function (el, fn) {
    var t0 = null, raf = null, visible = true, running = true;
    function step(ts) {
      if (t0 === null) t0 = ts;
      var t = (ts - t0) / 1000;
      fn(t);
      raf = requestAnimationFrame(step);
    }
    function start() { if (raf === null && running && visible) raf = requestAnimationFrame(step); }
    function stop() { if (raf !== null) { cancelAnimationFrame(raf); raf = null; } }
    if (global.IntersectionObserver && el) {
      new IntersectionObserver(function (es) {
        visible = es[0].isIntersecting;
        visible ? start() : stop();
      }, { threshold: .05 }).observe(el);
    }
    start();
    return {
      pause: function () { running = false; stop(); },
      play: function () { running = true; start(); },
      toggle: function (v) { v ? this.play() : this.pause(); },
      reset: function () { t0 = null; }
    };
  };

  /* ---------- mount ---------- */
  A.mount = function (scope) {
    (scope || document).querySelectorAll('[data-anim]').forEach(function (el) {
      if (el.dataset.mounted) return;
      var name = el.dataset.anim, fn = A.widgets[name];
      if (!fn) {
        el.innerHTML = '<div class="readout">Missing animation widget: <b>' + name + '</b></div>';
        return;
      }
      el.dataset.mounted = '1';
      var opts = {};
      Object.keys(el.dataset).forEach(function (k) {
        if (k !== 'anim' && k !== 'mounted') {
          var v = el.dataset[k];
          opts[k] = isNaN(parseFloat(v)) ? v : parseFloat(v);
        }
      });
      try { fn(el, opts); }
      catch (err) {
        el.innerHTML = '<div class="readout">Widget <b>' + name + '</b> failed: ' + err.message + '</div>';
        if (global.console) console.error(name, err);
      }
    });
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { A.mount(); });
  } else { A.mount(); }

  global.A = A;
})(window);
