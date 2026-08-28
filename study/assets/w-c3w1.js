/* Widgets for Course 3 / Week 1 — clustering and anomaly detection */
(function () {
  'use strict';

  function rnd(i) { var v = Math.sin(i * 12.9898 + 78.233) * 43758.5453; return v - Math.floor(v); }
  function gauss(i) {
    var r1 = rnd(i * 2 + 1), r2 = rnd(i * 2 + 2);
    return Math.sqrt(-2 * Math.log(r1 + 1e-9)) * Math.cos(6.2832 * r2);
  }
  /* three blobs, deterministic */
  var BLOBS = (function () {
    var cen = [[-1.7, 1.3], [1.8, 1.5], [0.2, -1.6]], a = [], i, k;
    for (k = 0; k < 3; k++)
      for (i = 0; i < 22; i++) {
        var s = k * 100 + i;
        a.push({ x: cen[k][0] + gauss(s * 3 + 1) * .62, y: cen[k][1] + gauss(s * 3 + 2) * .58, t: k });
      }
    return a;
  })();
  var COLS = function (P) { return [P.a, P.b, P.g, P.p, P.m]; };

  function dist2(p, c) { var dx = p.x - c.x, dy = p.y - c.y; return dx * dx + dy * dy; }
  function assign(pts, cents) {
    return pts.map(function (p) {
      var best = 0, bd = 1e9;
      cents.forEach(function (c, i) { var d = dist2(p, c); if (d < bd) { bd = d; best = i; } });
      return best;
    });
  }
  function move(pts, idx, K) {
    var out = [];
    for (var k = 0; k < K; k++) {
      var sel = pts.filter(function (p, i) { return idx[i] === k; });
      if (!sel.length) { out.push(null); continue; }
      out.push({ x: sel.reduce(function (s, p) { return s + p.x; }, 0) / sel.length,
                 y: sel.reduce(function (s, p) { return s + p.y; }, 0) / sel.length });
    }
    return out;
  }
  function distortion(pts, idx, cents) {
    var s = 0, n = 0;
    pts.forEach(function (p, i) { if (cents[idx[i]]) { s += dist2(p, cents[idx[i]]); n++; } });
    return n ? s / n : 0;
  }
  function initCents(K, seed) {
    /* pick K distinct training points as the starting centroids */
    var used = {}, out = [], salt = 0;
    for (var k = 0; k < K; k++) {
      var j, tries = 0;
      do {
        j = Math.floor(rnd(seed * 37 + k * 11 + (++salt) * 7 + 5) * BLOBS.length) % BLOBS.length;
        tries++;
      } while (used[j] && tries < 80);          /* bounded: never spins forever */
      used[j] = 1;
      out.push({ x: BLOBS[j].x, y: BLOBS[j].y });
    }
    return out;
  }

  /* ============================================================
     1. Supervised vs unsupervised
     ============================================================ */
  A.def('whatisclustering', function (root) {
    var c = A.canvas(root, 760, 320), ctx = c.ctx;
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var cols = COLS(P);
      var found = ((t * .3) % 2) > 1;
      [{ x: 40, sup: true }, { x: 400, sup: false }].forEach(function (pan) {
        var box = { x: pan.x + 30, y: 60, w: 300, h: 200 };
        var S = A.axes(ctx, box, [-3.2, 3.2], [-3, 3], { xticks: 4, yticks: 4, xlab: 'x₁', ylab: pan.sup ? 'x₂' : '' });
        A.txt(ctx, pan.sup ? 'SUPERVISED — you were given labels' : 'UNSUPERVISED — no labels at all',
          box.x + box.w / 2, 40, { align: 'center', size: 13, w: 700, fill: pan.sup ? P.b : P.a });
        BLOBS.forEach(function (p) {
          var showCol = pan.sup ? p.t : (found ? p.t : -1);
          A.dot(ctx, S.X(p.x), S.Y(p.y), 4, showCol < 0 ? P.faint : cols[showCol]);
        });
        if (pan.sup) {
          A.txt(ctx, 'y is given: ● class 0  ● class 1  ● class 2', box.x + 6, box.y + box.h + 34,
            { size: 11, fill: P.faint });
        } else {
          A.txt(ctx, found ? 'the algorithm FOUND three groups' : 'just x — the data comes with no y',
            box.x + 6, box.y + box.h + 34, { size: 11, w: 700, fill: found ? P.a : P.faint });
        }
      });
      A.txt(ctx, 'Clustering asks: “are there natural groups in here?” Nobody tells it the answer, and nobody can mark it right or wrong.',
        40, 306, { size: 12, w: 600, fill: P.soft });
    }
    A.autoplay(root, c, render);
  });

  /* ============================================================
     2. K-means intuition — the two repeating steps
     ============================================================ */
  A.def('kmeansintuition', function (root) {
    var c = A.canvas(root, 760, 340), ctx = c.ctx;
    var K = 3, seed = 3, step = 0, playing = true;
    var cents = initCents(K, seed), idx = assign(BLOBS, cents), prev = cents.map(function (o) { return { x: o.x, y: o.y }; });
    var ro = A.readout(root);
    function doStep() {
      if (step % 2 === 0) { idx = assign(BLOBS, cents); }
      else { prev = cents.map(function (o) { return { x: o.x, y: o.y }; });
             var nc = move(BLOBS, idx, K);
             cents = nc.map(function (v, i) { return v || cents[i]; }); }
      step++;
    }
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var cols = COLS(P);
      var box = { x: 70, y: 44, w: 400, h: 240 };
      var S = A.axes(ctx, box, [-3.2, 3.2], [-3, 3], { xticks: 4, yticks: 4, xlab: 'x₁', ylab: 'x₂' });
      var assigning = step % 2 === 1;
      BLOBS.forEach(function (p, i) {
        var k = idx[i];
        A.dot(ctx, S.X(p.x), S.Y(p.y), 4, cols[k]);
        if (assigning) A.line(ctx, S.X(p.x), S.Y(p.y), S.X(cents[k].x), S.Y(cents[k].y), cols[k], .5);
      });
      cents.forEach(function (cc, k) {
        var x = S.X(cc.x), y = S.Y(cc.y);
        ctx.save(); ctx.strokeStyle = cols[k]; ctx.lineWidth = 3;
        ctx.beginPath(); ctx.moveTo(x - 9, y - 9); ctx.lineTo(x + 9, y + 9);
        ctx.moveTo(x + 9, y - 9); ctx.lineTo(x - 9, y + 9); ctx.stroke(); ctx.restore();
        if (!assigning && prev[k]) A.arrow(ctx, S.X(prev[k].x), S.Y(prev[k].y), x, y, cols[k], 1.6);
      });
      /* the two steps, described */
      [['1 · ASSIGN', 'every point joins its nearest ✕', assigning],
       ['2 · MOVE', 'every ✕ hops to the middle of its own points', !assigning]
      ].forEach(function (s, i) {
        var y = 70 + i * 90;
        A.rr(ctx, 510, y, 210, 74, 10);
        ctx.fillStyle = s[2] ? P.aS : P.sunk; ctx.fill();
        ctx.strokeStyle = s[2] ? P.a : P.lineSoft; ctx.lineWidth = s[2] ? 2.2 : 1.2; ctx.stroke();
        A.txt(ctx, s[0], 615, y + 26, { align: 'center', size: 14, w: 700, fill: s[2] ? P.a : P.faint });
        A.txt(ctx, s[1], 615, y + 48, { align: 'center', size: 10.5, fill: P.faint });
      });
      A.arrow(ctx, 725, 100, 735, 190, P.line, 1.6);
      A.arrow(ctx, 505, 190, 495, 100, P.line, 1.6);
      A.txt(ctx, 'repeat until nothing moves', 615, 262, { align: 'center', size: 11.5, w: 700, fill: P.soft });
      A.txt(ctx, 'iteration ' + Math.floor(step / 2) + ' · distortion J = ' +
        distortion(BLOBS, idx, cents).toFixed(4), 70, 312, { size: 12.5, mono: true, fill: P.soft });
      ro.set('Two steps, alternating forever: <b>assign</b> each point to the closest centroid, then ' +
        '<b>move</b> each centroid to the average of its points.\nNeither step can ever increase J — which ' +
        'is why K-means always converges.');
    }
    var bar = A.ctrls(root);
    A.toggle(bar, 'auto', function (on) { playing = on; }, true);
    A.button(bar, 'step ›', function () { playing = false; doStep(); render(lt); });
    A.button(bar, 'restart', function () {
      seed++; cents = initCents(K, seed); idx = assign(BLOBS, cents); step = 0; render(lt);
    });
    A.bind(c, function () { render(lt); });
    var lt = 0, acc = 0;
    A.loop(c.cv, function (t) {
      lt = t;
      if (playing && t - acc > 1.1) { acc = t; if (step > 11) { seed++; cents = initCents(K, seed); idx = assign(BLOBS, cents); step = 0; } else doStep(); }
      render(t);
    });
  });

  /* ============================================================
     3. The K-means algorithm, with K you choose
     ============================================================ */
  A.def('kmeansalgo', function (root) {
    var c = A.canvas(root, 760, 340), ctx = c.ctx;
    var K = 3, seed = 1, cents = initCents(K, seed), idx = assign(BLOBS, cents), it = 0, done = false;
    var bar = A.ctrls(root), ro = A.readout(root);
    A.slider(bar, { label: 'K =', min: 1, max: 5, step: 1, value: K,
      fmt: function (v) { return v.toFixed(0); }, on: function (v) { K = v; reset(); } });
    A.button(bar, 'new random start', function () { seed++; reset(); });
    function reset() { cents = initCents(K, seed); idx = assign(BLOBS, cents); it = 0; done = false; }
    function iterate() {
      var old = JSON.stringify(cents);
      idx = assign(BLOBS, cents);
      var nc = move(BLOBS, idx, K);
      cents = nc.map(function (v, i) { return v || cents[i]; });
      it++;
      if (JSON.stringify(cents) === old) done = true;
    }
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var cols = COLS(P);
      var box = { x: 70, y: 40, w: 620, h: 230 };
      var S = A.axes(ctx, box, [-3.4, 3.4], [-3, 3], { xticks: 6, yticks: 4, xlab: 'x₁', ylab: 'x₂' });
      /* faint voronoi-ish shading by sampling */
      ctx.save(); ctx.globalAlpha = .07;
      for (var gx = 0; gx < 62; gx++) for (var gy = 0; gy < 23; gy++) {
        var px = -3.4 + 6.8 * gx / 61, py = -3 + 6 * gy / 22;
        var bi = 0, bd = 1e9;
        cents.forEach(function (cc, i) { var d = dist2({ x: px, y: py }, cc); if (d < bd) { bd = d; bi = i; } });
        ctx.fillStyle = cols[bi];
        ctx.fillRect(S.X(px) - 6, S.Y(py) - 6, 12, 12);
      }
      ctx.restore();
      BLOBS.forEach(function (p, i) { A.dot(ctx, S.X(p.x), S.Y(p.y), 4, cols[idx[i]]); });
      cents.forEach(function (cc, k) {
        var x = S.X(cc.x), y = S.Y(cc.y);
        ctx.save(); ctx.strokeStyle = P.panel; ctx.lineWidth = 5;
        ctx.beginPath(); ctx.moveTo(x - 9, y - 9); ctx.lineTo(x + 9, y + 9);
        ctx.moveTo(x + 9, y - 9); ctx.lineTo(x - 9, y + 9); ctx.stroke();
        ctx.strokeStyle = cols[k]; ctx.lineWidth = 3;
        ctx.beginPath(); ctx.moveTo(x - 9, y - 9); ctx.lineTo(x + 9, y + 9);
        ctx.moveTo(x + 9, y - 9); ctx.lineTo(x - 9, y + 9); ctx.stroke(); ctx.restore();
      });
      A.txt(ctx, 'iteration ' + it + (done ? '  ·  converged, nothing moved' : ''), 70, 300,
        { size: 12.5, mono: true, w: 700, fill: done ? P.g : P.soft });
      A.txt(ctx, 'J = ' + distortion(BLOBS, idx, cents).toFixed(4), 70, 322,
        { size: 12.5, mono: true, fill: P.faint });
      A.txt(ctx, 'shaded regions show which centroid owns which patch of space', 380, 322,
        { size: 11.5, fill: P.faint });
      ro.set('repeat until convergence:\n' +
        '  <b>for i = 1..m</b>:  c<sup>(i)</sup> := index of the centroid closest to x<sup>(i)</sup>\n' +
        '  <b>for k = 1..K</b>:  μ<sub>k</sub> := average of all points assigned to k');
    }
    A.bind(c, function () { render(lt); });
    var lt = 0, acc = 0;
    A.loop(c.cv, function (t) {
      lt = t;
      if (t - acc > 1.0) { acc = t; if (done) { seed++; reset(); } else iterate(); }
      render(t);
    });
  });

  /* ============================================================
     4. The cost function (distortion) only ever goes down
     ============================================================ */
  A.def('kmeanscost', function (root) {
    var c = A.canvas(root, 760, 320), ctx = c.ctx;
    var hist = (function () {
      var K = 3, cents = initCents(K, 9), h = [], idx;
      for (var s = 0; s < 12; s++) {
        idx = assign(BLOBS, cents);
        h.push({ J: distortion(BLOBS, idx, cents), what: 'assign' });
        var nc = move(BLOBS, idx, K);
        cents = nc.map(function (v, i) { return v || cents[i]; });
        h.push({ J: distortion(BLOBS, idx, cents), what: 'move' });
      }
      return h;
    })();
    var ro = A.readout(root);
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var n = Math.min(hist.length, 2 + Math.floor((t * 1.6) % (hist.length + 4)));
      var box = { x: 80, y: 40, w: 620, h: 200 };
      var top = hist[0].J * 1.12;
      var S = A.axes(ctx, box, [0, hist.length - 1], [0, top], {
        xticks: 6, yticks: 4, xfmt: function (v) { return (v / 2).toFixed(0); },
        yfmt: function (v) { return v.toFixed(1); },
        xlab: 'iteration (each has an assign step and a move step)', ylab: 'J — distortion'
      });
      ctx.save(); ctx.strokeStyle = P.a; ctx.lineWidth = 2.4; ctx.beginPath();
      for (var i = 0; i < n; i++) {
        var px = S.X(i), py = S.Y(hist[i].J);
        i === 0 ? ctx.moveTo(px, py) : ctx.lineTo(px, py);
      }
      ctx.stroke(); ctx.restore();
      for (i = 0; i < n; i++)
        A.dot(ctx, S.X(i), S.Y(hist[i].J), 4, hist[i].what === 'assign' ? P.b : P.g);
      A.legend(root, [[P.b, 'after the assign step'], [P.g, 'after the move step']]);
      A.txt(ctx, 'J = ' + hist[Math.max(0, n - 1)].J.toFixed(4), 80, 268,
        { size: 13, mono: true, w: 700, fill: P.a });
      A.txt(ctx, 'It never goes up. Not once. If your implementation ever increases J, you have a bug.',
        80, 292, { size: 12.5, w: 700, fill: P.soft });
      A.txt(ctx, 'Both steps are minimising the SAME quantity — that is the whole proof of convergence.',
        80, 312, { size: 11.5, fill: P.faint });
      ro.set('J(c<sup>(1)</sup>…c<sup>(m)</sup>, μ<sub>1</sub>…μ<sub>K</sub>) = (1/m) Σ ‖ x<sup>(i)</sup> − μ<sub>c<sup>(i)</sup></sub> ‖²' +
        '\n<b>assign</b> minimises J over the assignments c, holding μ fixed. ' +
        '<b>move</b> minimises J over the centroids μ, holding c fixed.');
    }
    A.autoplay(root, c, render);
  });

  /* ============================================================
     5. Random initialisation and local optima
     ============================================================ */
  A.def('kmeansinit', function (root) {
    var c = A.canvas(root, 760, 320), ctx = c.ctx;
    var runs = [4, 17, 23].map(function (sd) {
      var K = 3, cents = initCents(K, sd), idx;
      for (var s = 0; s < 25; s++) {
        idx = assign(BLOBS, cents);
        var nc = move(BLOBS, idx, K);
        cents = nc.map(function (v, i) { return v || cents[i]; });
      }
      idx = assign(BLOBS, cents);
      return { cents: cents, idx: idx, J: distortion(BLOBS, idx, cents) };
    });
    /* force one visibly worse local optimum */
    (function () {
      var K = 3, cents = [{ x: -1.9, y: 1.5 }, { x: -1.4, y: 1.0 }, { x: 1.0, y: 0 }], idx;
      for (var s = 0; s < 25; s++) {
        idx = assign(BLOBS, cents);
        var nc = move(BLOBS, idx, K);
        cents = nc.map(function (v, i) { return v || cents[i]; });
      }
      idx = assign(BLOBS, cents);
      runs[1] = { cents: cents, idx: idx, J: distortion(BLOBS, idx, cents) };
    })();
    var best = 0; runs.forEach(function (r, i) { if (r.J < runs[best].J) best = i; });
    var ro = A.readout(root);
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var cols = COLS(P);
      var reveal = ((t * .35) % 2) > 1;
      runs.forEach(function (r, ri) {
        var bx = 40 + ri * 240;
        var box = { x: bx + 20, y: 66, w: 190, h: 150 };
        var S = A.axes(ctx, box, [-3.2, 3.2], [-3, 3], { xticks: 2, yticks: 2 });
        var win = reveal && ri === best;
        A.rr(ctx, bx, 46, 230, 200, 10);
        ctx.strokeStyle = win ? P.a : P.lineSoft; ctx.lineWidth = win ? 2.4 : 1; ctx.stroke();
        BLOBS.forEach(function (p, i) { A.dot(ctx, S.X(p.x), S.Y(p.y), 3, cols[r.idx[i]]); });
        r.cents.forEach(function (cc, k) {
          var x = S.X(cc.x), y = S.Y(cc.y);
          ctx.save(); ctx.strokeStyle = cols[k]; ctx.lineWidth = 2.6;
          ctx.beginPath(); ctx.moveTo(x - 7, y - 7); ctx.lineTo(x + 7, y + 7);
          ctx.moveTo(x + 7, y - 7); ctx.lineTo(x - 7, y + 7); ctx.stroke(); ctx.restore();
        });
        A.txt(ctx, 'random start ' + (ri + 1), bx + 115, 40, { align: 'center', size: 12, w: 700,
          fill: win ? P.a : P.faint });
        A.txt(ctx, 'J = ' + r.J.toFixed(4), bx + 115, 264, { align: 'center', size: 13, mono: true,
          w: 700, fill: win ? P.a : P.soft });
        if (win) A.txt(ctx, '← keep this one', bx + 115, 284, { align: 'center', size: 11.5, w: 700, fill: P.a });
      });
      A.txt(ctx, 'Same data, same algorithm, three different answers — because the starting positions differed.',
        40, 24, { size: 12.5, w: 700, fill: P.soft });
      A.txt(ctx, 'The fix is embarrassingly simple: run it 50–1000 times and keep whichever run got the lowest J.',
        40, 308, { size: 12, fill: P.faint });
    }
    A.autoplay(root, c, render);
  });

  /* ============================================================
     6. Choosing K
     ============================================================ */
  A.def('elbow', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var Js = [];
    (function () {
      for (var K = 1; K <= 8; K++) {
        var bestJ = 1e9;
        for (var trial = 0; trial < 12; trial++) {
          var cents = initCents(K, trial * 13 + K), idx;
          for (var s = 0; s < 20; s++) {
            idx = assign(BLOBS, cents);
            var nc = move(BLOBS, idx, K);
            cents = nc.map(function (v, i) { return v || cents[i]; });
          }
          idx = assign(BLOBS, cents);
          bestJ = Math.min(bestJ, distortion(BLOBS, idx, cents));
        }
        Js.push(bestJ);
      }
    })();
    var sel = 3;
    var bar = A.ctrls(root), ro = A.readout(root);
    A.slider(bar, { label: 'K =', min: 1, max: 8, step: 1, value: sel,
      fmt: function (v) { return v.toFixed(0); }, on: function (v) { sel = v; render(); } });
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var box = { x: 70, y: 46, w: 320, h: 200 };
      var S = A.axes(ctx, box, [1, 8], [0, Js[0] * 1.1], {
        xticks: 7, yticks: 4, xfmt: function (v) { return v.toFixed(0); },
        yfmt: function (v) { return v.toFixed(1); }, xlab: 'K — number of clusters', ylab: 'J'
      });
      ctx.save(); ctx.strokeStyle = P.a; ctx.lineWidth = 2.6; ctx.beginPath();
      Js.forEach(function (j, i) { var px = S.X(i + 1), py = S.Y(j); i === 0 ? ctx.moveTo(px, py) : ctx.lineTo(px, py); });
      ctx.stroke(); ctx.restore();
      Js.forEach(function (j, i) { A.dot(ctx, S.X(i + 1), S.Y(j), 4.5, i === sel - 1 ? P.g : P.a); });
      A.dot(ctx, S.X(sel), S.Y(Js[sel - 1]), 9, P.g);
      var gain = sel > 1 ? Js[sel - 2] - Js[sel - 1] : null;
      A.txt(ctx, 'K = ' + sel, S.X(sel) + 12, S.Y(Js[sel - 1]) - 10, { size: 12, w: 700, fill: P.g });
      A.txt(ctx, gain === null ? 'one cluster — nothing to compare against'
              : 'this step bought ' + gain.toFixed(2) + ' of J',
        S.X(sel) + 12, S.Y(Js[sel - 1]) + 8, { size: 10.5, fill: gain !== null && gain < 0.25 ? P.faint : P.g });
      A.txt(ctx, 'J always falls as K grows — more centroids can only fit tighter.', 70, 274,
        { size: 11.5, fill: P.faint });
      A.txt(ctx, 'So you can never pick K by minimising J. K = m would give J = 0.', 70, 292,
        { size: 11.5, w: 700, fill: P.r });
      /* the honest answer */
      A.rr(ctx, 430, 46, 290, 200, 10); ctx.fillStyle = P.sunk; ctx.fill();
      ctx.strokeStyle = P.lineSoft; ctx.stroke();
      A.txt(ctx, 'the answer that actually works', 575, 72, { align: 'center', size: 12.5, w: 700, fill: P.soft });
      A.txt(ctx, 'choose K by what you will DO with it', 575, 96, { align: 'center', size: 12, fill: P.a, w: 700 });
      [['T-shirt sizes:', 'K = 3 → S, M, L'], ['', 'K = 5 → XS, S, M, L, XL'],
       ['', ''], ['Better fit per shirt (K = 5)', 'vs cheaper manufacturing (K = 3)'],
       ['', ''], ['That is a business decision,', 'not a maths one.']
      ].forEach(function (r, i) {
        A.txt(ctx, r[0], 450, 126 + i * 20, { size: 11.5, w: 600, fill: P.soft });
        A.txt(ctx, r[1], 700, 126 + i * 20, { align: 'right', size: 11.5, fill: P.faint });
      });
      A.txt(ctx, 'The elbow is worth a glance. It is often ambiguous, and Andrew explicitly says he does not use it much.',
        70, 316, { size: 12, w: 700, fill: P.soft });
      ro.set('Elbow method: plot J against K and look for the bend. Honest caveat — on real data the curve ' +
        'is usually a smooth slope with no obvious elbow at all.\nDownstream method: evaluate K by how well ' +
        'the clusters serve the actual purpose. This is the one to reach for.');
    }
    A.bind(c, render); render();
  });

})();

/* ---------- part 2 : anomaly detection ---------- */
(function () {
  'use strict';

  function rnd(i) { var v = Math.sin(i * 45.164 + 12.771) * 24634.6345; return v - Math.floor(v); }
  function gauss(i) {
    var r1 = rnd(i * 2 + 1), r2 = rnd(i * 2 + 2);
    return Math.sqrt(-2 * Math.log(r1 + 1e-9)) * Math.cos(6.2832 * r2);
  }
  function npdf(x, mu, sig) {
    return Math.exp(-(x - mu) * (x - mu) / (2 * sig * sig)) / (Math.sqrt(6.2832) * sig);
  }
  /* aircraft engines: x1 = heat, x2 = vibration */
  var ENG = (function () {
    var a = [], i;
    for (i = 0; i < 80; i++) a.push({ x: 5 + gauss(i * 5 + 1) * 1.05, y: 5 + gauss(i * 5 + 3) * 1.15, bad: 0 });
    /* a handful of genuine anomalies */
    [[1.6, 8.4], [8.9, 1.9], [9.4, 9.0], [1.3, 1.6], [8.6, 5.1]].forEach(function (p) {
      a.push({ x: p[0], y: p[1], bad: 1 });
    });
    return a;
  })();
  function fitParams(pts) {
    var mx = pts.reduce(function (s, p) { return s + p.x; }, 0) / pts.length;
    var my = pts.reduce(function (s, p) { return s + p.y; }, 0) / pts.length;
    var sx = Math.sqrt(pts.reduce(function (s, p) { return s + (p.x - mx) * (p.x - mx); }, 0) / pts.length);
    var sy = Math.sqrt(pts.reduce(function (s, p) { return s + (p.y - my) * (p.y - my); }, 0) / pts.length);
    return { mx: mx, my: my, sx: sx, sy: sy };
  }
  var PAR = fitParams(ENG.filter(function (p) { return !p.bad; }));
  function px2(p) { return npdf(p.x, PAR.mx, PAR.sx) * npdf(p.y, PAR.my, PAR.sy); }

  /* ============================================================
     7. Finding unusual events
     ============================================================ */
  A.def('anomalyintro', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var tx = 8.6, ty = 4.6;
    var bar = A.ctrls(root), ro = A.readout(root);
    A.slider(bar, { label: 'test engine — heat', min: 1, max: 10, value: tx,
      fmt: function (v) { return v.toFixed(1); }, on: function (v) { tx = v; render(); } });
    A.slider(bar, { label: 'vibration', min: 1, max: 10, value: ty,
      fmt: function (v) { return v.toFixed(1); }, on: function (v) { ty = v; render(); } });
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var box = { x: 80, y: 40, w: 380, h: 230 };
      var S = A.axes(ctx, box, [0, 11], [0, 11], {
        xticks: 5, yticks: 5, xfmt: function (v) { return v.toFixed(0); },
        yfmt: function (v) { return v.toFixed(0); },
        xlab: 'x₁ — heat generated', ylab: 'x₂ — vibration intensity'
      });
      ENG.forEach(function (p) { if (!p.bad) A.dot(ctx, S.X(p.x), S.Y(p.y), 3.6, P.b); });
      var p = px2({ x: tx, y: ty });
      var pMid = px2({ x: PAR.mx, y: PAR.my });
      var odd = p < pMid * 0.02;
      A.dot(ctx, S.X(tx), S.Y(ty), 9, odd ? P.r : P.g);
      ctx.save(); ctx.strokeStyle = odd ? P.r : P.g; ctx.lineWidth = 2; ctx.setLineDash([4, 3]);
      ctx.beginPath(); ctx.arc(S.X(tx), S.Y(ty), 15, 0, 6.2832); ctx.stroke(); ctx.restore();
      A.txt(ctx, 'every engine we have ever tested (all fine)', box.x + 6, 32, { size: 11.5, fill: P.faint });
      /* verdict panel */
      A.rr(ctx, 510, 60, 210, 130, 10);
      ctx.fillStyle = odd ? P.rS : P.gS; ctx.fill();
      ctx.strokeStyle = odd ? P.r : P.g; ctx.lineWidth = 2; ctx.stroke();
      A.txt(ctx, odd ? '⚠ ANOMALY' : '✓ looks normal', 615, 100,
        { align: 'center', size: 17, w: 700, fill: odd ? P.r : P.g });
      A.txt(ctx, odd ? 'send it for inspection' : 'ship it', 615, 124,
        { align: 'center', size: 12, fill: odd ? P.r : P.g });
      A.txt(ctx, 'p(x) = ' + p.toExponential(2), 615, 152, { align: 'center', size: 12, mono: true, fill: P.soft });
      A.txt(ctx, 'vs ' + pMid.toExponential(2) + ' at the centre', 615, 170,
        { align: 'center', size: 10.5, mono: true, fill: P.faint });
      A.txt(ctx, 'You have never seen a broken engine. All you have is a pile of normal ones —', 80, 296,
        { size: 12, fill: P.soft });
      A.txt(ctx, 'so the question becomes “is this one WEIRD?”, not “is this one broken?”.', 80, 316,
        { size: 12, w: 700, fill: P.a });
      ro.set('Anomaly detection is trained on <b>normal examples only</b>. It learns what normal looks like, ' +
        'then flags anything improbable.\nThat is why it can catch failure modes nobody has ever seen — ' +
        'which supervised learning fundamentally cannot.');
    }
    A.bind(c, render); render();
  });

  /* ============================================================
     8. The Gaussian distribution
     ============================================================ */
  A.def('gaussian', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var mu = 5, sig = 1.2;
    var bar = A.ctrls(root), ro = A.readout(root);
    A.slider(bar, { label: 'μ (mean)', min: 1, max: 9, value: mu,
      fmt: function (v) { return v.toFixed(2); }, on: function (v) { mu = v; render(); } });
    A.slider(bar, { label: 'σ (spread)', min: .3, max: 3, value: sig,
      fmt: function (v) { return v.toFixed(2); }, on: function (v) { sig = v; render(); } });
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var box = { x: 70, y: 40, w: 620, h: 210 };
      var S = A.axes(ctx, box, [0, 11], [0, 1.4], {
        xticks: 5, yticks: 4, xfmt: function (v) { return v.toFixed(0); },
        yfmt: function (v) { return v.toFixed(1); }, xlab: 'x', ylab: 'p(x)'
      });
      /* the data it is being fitted to */
      var xs = ENG.filter(function (p) { return !p.bad; }).map(function (p) { return p.x; });
      xs.forEach(function (v) { A.dot(ctx, S.X(v), S.Y(0.04), 3, P.faint); });
      /* the shaded ±2σ region */
      ctx.save(); ctx.fillStyle = P.a; ctx.globalAlpha = .12; ctx.beginPath();
      ctx.moveTo(S.X(mu - 2 * sig), S.Y(0));
      for (var v2 = mu - 2 * sig; v2 <= mu + 2 * sig; v2 += .04) ctx.lineTo(S.X(v2), S.Y(npdf(v2, mu, sig)));
      ctx.lineTo(S.X(mu + 2 * sig), S.Y(0)); ctx.closePath(); ctx.fill(); ctx.restore();
      A.plot(ctx, S, [0, 11], function (v) { return npdf(v, mu, sig); }, P.a, 2.8);
      A.line(ctx, S.X(mu), box.y, S.X(mu), S.Y(0), P.a, 1.4, [4, 3]);
      A.txt(ctx, 'μ', S.X(mu), box.y + 14, { align: 'center', size: 14, w: 700, fill: P.a });
      A.line(ctx, S.X(mu - sig), S.Y(npdf(mu - sig, mu, sig)), S.X(mu + sig), S.Y(npdf(mu - sig, mu, sig)), P.b, 2);
      A.txt(ctx, '2σ wide here', S.X(mu), S.Y(npdf(mu - sig, mu, sig)) - 8,
        { align: 'center', size: 11, w: 700, fill: P.b });
      A.txt(ctx, 'the shaded part holds about 95% of everything', 80, 270, { size: 12, fill: P.faint });
      A.txt(ctx, 'Small σ → a tall narrow spike: the model is confident, and anything off-centre is instantly suspicious.',
        70, 296, { size: 12, fill: P.soft });
      A.txt(ctx, 'Large σ → a wide flat hill: almost nothing looks strange. The area under the curve is always exactly 1.',
        70, 316, { size: 12, fill: P.soft });
      ro.set('p(x) = (1 / (√(2π)·σ)) · e<sup>−(x−μ)² / (2σ²)</sup>' +
        '\nFitted from data: μ = (1/m)Σx<sup>(i)</sup> = <b>' + PAR.mx.toFixed(3) +
        '</b>,  σ² = (1/m)Σ(x<sup>(i)</sup>−μ)² = <b>' + (PAR.sx * PAR.sx).toFixed(3) + '</b>');
    }
    A.bind(c, render); render();
  });

  /* ============================================================
     9. The anomaly detection algorithm
     ============================================================ */
  A.def('anomalyalgo', function (root) {
    var c = A.canvas(root, 760, 340), ctx = c.ctx;
    var epsExp = -4;
    var bar = A.ctrls(root), ro = A.readout(root);
    A.slider(bar, { label: 'ε = 10^', min: -7, max: -1.2, step: .1, value: epsExp,
      fmt: function (v) { return '1e' + v.toFixed(1); }, on: function (v) { epsExp = v; render(); } });
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var eps = Math.pow(10, epsExp);
      var box = { x: 70, y: 40, w: 350, h: 240 };
      var S = A.axes(ctx, box, [0, 11], [0, 11], {
        xticks: 5, yticks: 5, xfmt: function (v) { return v.toFixed(0); },
        yfmt: function (v) { return v.toFixed(0); }, xlab: 'x₁ — heat', ylab: 'x₂ — vibration'
      });
      /* contours of p(x) */
      [0.5, 0.2, 0.06, 0.015, 0.003].forEach(function (lvl) {
        var pk = npdf(PAR.mx, PAR.mx, PAR.sx) * npdf(PAR.my, PAR.my, PAR.sy);
        var target = pk * lvl;
        var r = Math.sqrt(-2 * Math.log(lvl));
        ctx.save(); ctx.strokeStyle = P.lineSoft; ctx.lineWidth = 1.2; ctx.beginPath();
        for (var th = 0; th <= 6.3; th += .06) {
          var xx = PAR.mx + PAR.sx * r * Math.cos(th), yy = PAR.my + PAR.sy * r * Math.sin(th);
          th === 0 ? ctx.moveTo(S.X(xx), S.Y(yy)) : ctx.lineTo(S.X(xx), S.Y(yy));
        }
        ctx.closePath(); ctx.stroke(); ctx.restore();
      });
      var flagged = 0, caught = 0, falseAl = 0;
      ENG.forEach(function (p) {
        var an = px2(p) < eps;
        if (an) { flagged++; if (p.bad) caught++; else falseAl++; }
        A.dot(ctx, S.X(p.x), S.Y(p.y), an ? 5.5 : 3.6, an ? P.r : (p.bad ? P.m : P.b));
        if (an) {
          ctx.save(); ctx.strokeStyle = P.r; ctx.lineWidth = 1.4;
          ctx.beginPath(); ctx.arc(S.X(p.x), S.Y(p.y), 9, 0, 6.2832); ctx.stroke(); ctx.restore();
        }
      });
      var nBad = ENG.filter(function (p) { return p.bad; }).length;
      /* the algorithm, written out */
      var lines = [
        ['1. pick features x₁ … xₙ you think might expose an anomaly', P.soft],
        ['2. fit each one separately:', P.soft],
        ['     μⱼ = mean of xⱼ    σⱼ² = variance of xⱼ', P.faint],
        ['3. for a new x, multiply the per-feature probabilities:', P.soft],
        ['     p(x) = p(x₁;μ₁,σ₁²) × p(x₂;μ₂,σ₂²) × … × p(xₙ;μₙ,σₙ²)', P.a],
        ['4. flag it if p(x) < ε', P.a]
      ];
      lines.forEach(function (l, i) {
        A.txt(ctx, l[0], 450, 66 + i * 26, { size: 11.5, w: l[1] === P.a ? 700 : 500, mono: i === 2, fill: l[1] });
      });
      A.txt(ctx, 'ε = ' + eps.toExponential(1), 450, 244, { size: 14, mono: true, w: 700, fill: P.a });
      A.txt(ctx, 'flagged ' + flagged + '  ·  ' + caught + ' of ' + nBad + ' real anomalies caught  ·  ' +
        falseAl + ' false alarms', 450, 268, { size: 11.5, mono: true, fill: P.soft });
      A.legend(root, [[P.b, 'normal engines'], [P.m, 'genuinely faulty (not used in training)'], [P.r, 'flagged by the model']]);
      A.txt(ctx, 'Multiplying is the key move: a value only mildly odd on TWO features multiplies into something very small.',
        70, 314, { size: 12, w: 700, fill: P.soft });
      ro.set('p(x) = <b>Π</b><sub>j=1..n</sub> p(x<sub>j</sub>; μ<sub>j</sub>, σ<sub>j</sub>²)   —   ' +
        'anomaly if p(x) &lt; ε' +
        '\nThis assumes the features are independent. They usually are not, and it works well anyway — ' +
        'which is a recurring theme in applied ML.');
    }
    A.bind(c, render); render();
  });

  /* ============================================================
     10. Evaluating an anomaly detector, and choosing ε
     ============================================================ */
  A.def('anomalyeval', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var epsExp = -4;
    var bar = A.ctrls(root), ro = A.readout(root);
    A.slider(bar, { label: 'ε = 10^', min: -7, max: -1.2, step: .05, value: epsExp,
      fmt: function (v) { return '1e' + v.toFixed(1); }, on: function (v) { epsExp = v; render(); } });
    function score(eps) {
      var tp = 0, fp = 0, fn = 0, tn = 0;
      ENG.forEach(function (p) {
        var flag = px2(p) < eps;
        if (p.bad && flag) tp++; else if (!p.bad && flag) fp++;
        else if (p.bad && !flag) fn++; else tn++;
      });
      var prec = tp + fp ? tp / (tp + fp) : 1, rec = tp + fn ? tp / (tp + fn) : 0;
      return { tp: tp, fp: fp, fn: fn, tn: tn, prec: prec, rec: rec,
               f1: prec + rec ? 2 * prec * rec / (prec + rec) : 0 };
    }
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var eps = Math.pow(10, epsExp), r = score(eps);
      var box = { x: 70, y: 46, w: 380, h: 190 };
      var S = A.axes(ctx, box, [-7, -1.2], [0, 1], {
        xticks: 5, yticks: 4, xfmt: function (v) { return '1e' + v.toFixed(0); },
        yfmt: function (v) { return v.toFixed(1); }, xlab: 'ε (log scale)', ylab: 'score'
      });
      A.plot(ctx, S, [-7, -1.2], function (e) { return score(Math.pow(10, e)).prec; }, P.b, 2.2);
      A.plot(ctx, S, [-7, -1.2], function (e) { return score(Math.pow(10, e)).rec; }, P.g, 2.2);
      A.plot(ctx, S, [-7, -1.2], function (e) { return score(Math.pow(10, e)).f1; }, P.a, 2.8);
      var bestE = -7, bestF = 0;
      for (var e = -7; e <= -1.2; e += .05) { var f = score(Math.pow(10, e)).f1; if (f > bestF) { bestF = f; bestE = e; } }
      A.dot(ctx, S.X(bestE), S.Y(bestF), 6, P.a);
      A.txt(ctx, 'best F1', S.X(bestE) + 8, S.Y(bestF) - 8, { size: 11, w: 700, fill: P.a });
      A.line(ctx, S.X(epsExp), box.y, S.X(epsExp), box.y + box.h, P.faint, 1.4, [4, 3]);
      A.legend(root, [[P.b, 'precision'], [P.g, 'recall'], [P.a, 'F1']]);
      /* the split recipe */
      A.txt(ctx, 'how you split the data', 480, 40, { size: 12.5, w: 700, fill: P.soft });
      [['training set', '6000 normal, 0 anomalies', 'fit μ and σ here — normal only', P.b],
       ['cross-validation', '2000 normal, 10 anomalies', 'choose ε and the features here', P.a],
       ['test set', '2000 normal, 10 anomalies', 'measure once, at the end', P.g]
      ].forEach(function (row, i) {
        var y = 56 + i * 62;
        A.rr(ctx, 470, y, 250, 54, 8); ctx.fillStyle = P.sunk; ctx.fill();
        ctx.strokeStyle = row[3]; ctx.lineWidth = 1.4; ctx.stroke();
        A.txt(ctx, row[0], 484, y + 20, { size: 12, w: 700, fill: row[3] });
        A.txt(ctx, row[1], 484, y + 35, { size: 10.5, mono: true, fill: P.faint });
        A.txt(ctx, row[2], 484, y + 48, { size: 10, fill: P.faint });
      });
      A.txt(ctx, 'precision ' + (r.prec * 100).toFixed(0) + '%  ·  recall ' + (r.rec * 100).toFixed(0) +
        '%  ·  F1 ' + (r.f1 * 100).toFixed(0) + '%', 70, 262, { size: 13, mono: true, w: 700, fill: P.a });
      A.txt(ctx, 'Anomalies are rare, so accuracy is useless here — a detector that flags nothing scores 94%.',
        70, 288, { size: 12, fill: P.soft });
      A.txt(ctx, 'This is exactly the skewed-dataset problem from Course 2, Week 3.', 70, 308,
        { size: 12, w: 700, fill: P.a });
      ro.set('The trick that makes evaluation possible: put your <b>few known anomalies into the ' +
        'cross-validation and test sets</b>, never into training.\nTraining stays unsupervised; ' +
        'evaluation borrows just enough supervision to tune ε.');
    }
    A.bind(c, render); render();
  });

  /* ============================================================
     11. Anomaly detection vs supervised learning
     ============================================================ */
  A.def('anomalyvssupervised', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var rows = [
      ['very few positives (0–20), many negatives', 1, 'many positives AND negatives'],
      ['many different types of anomaly — future ones may look nothing like past ones', 1,
       'enough examples of each type; future ones look like past ones'],
      ['fraud, manufacturing defects, machine monitoring, hacking', 1,
       'spam, weather, disease from symptoms, product defects you keep seeing'],
      ['learns what NORMAL looks like', 1, 'learns what each CLASS looks like'],
      ['can catch a failure mode never seen before', 1, 'can only recognise what it was shown']
    ];
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var hot = Math.floor((t * .5) % rows.length);
      A.txt(ctx, 'ANOMALY DETECTION', 200, 40, { align: 'center', size: 14, w: 700, fill: P.a });
      A.txt(ctx, 'SUPERVISED LEARNING', 570, 40, { align: 'center', size: 14, w: 700, fill: P.b });
      A.line(ctx, 380, 50, 380, 288, P.lineSoft, 1.4, [4, 4]);
      rows.forEach(function (r, i) {
        var y = 56 + i * 48, on = i === hot;
        [[40, r[0], P.a], [392, r[2], P.b]].forEach(function (side) {
          A.rr(ctx, side[0], y, 328, 42, 7);
          ctx.fillStyle = on ? (side[2] === P.a ? P.aS : P.bS) : P.sunk; ctx.fill();
          ctx.strokeStyle = on ? side[2] : P.lineSoft; ctx.lineWidth = on ? 1.8 : 1; ctx.stroke();
          var words = side[1].split(' '), line = '', ln = 0;
          words.forEach(function (w) {
            if ((line + w).length > 44) {
              A.txt(ctx, line, side[0] + 12, y + 17 + ln * 14, { size: 10.5, w: on ? 700 : 500,
                fill: on ? side[2] : P.soft });
              line = w + ' '; ln++;
            } else line += w + ' ';
          });
          A.txt(ctx, line, side[0] + 12, y + 17 + ln * 14, { size: 10.5, w: on ? 700 : 500,
            fill: on ? side[2] : P.soft });
        });
      });
      A.txt(ctx, 'The deciding question: do you expect future positives to LOOK LIKE the ones you have already seen?',
        40, 310, { size: 12, w: 700, fill: P.soft });
      A.txt(ctx, 'Yes → supervised.   No → anomaly detection.', 40, 328, { size: 12, w: 700, fill: P.a });
    }
    A.autoplay(root, c, render);
  });

  /* ============================================================
     12. Choosing features — make them Gaussian
     ============================================================ */
  A.def('featurechoice', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var cc = 0;
    var bar = A.ctrls(root), ro = A.readout(root);
    A.slider(bar, { label: 'transform: log(x + c), c =', min: 0, max: 3, step: .05, value: cc,
      fmt: function (v) { return v.toFixed(2); }, on: function (v) { cc = v; render(); } });
    /* a heavily right-skewed feature */
    var RAW = (function () {
      var a = [];
      for (var i = 0; i < 400; i++) {
        var u = rnd(i * 9 + 4);
        a.push(Math.pow(-Math.log(u + 1e-9), 2.1) * .8 + .05);
      }
      return a;
    })();
    function hist(vals, lo, hi, nb) {
      var h = new Array(nb).fill(0);
      vals.forEach(function (v) {
        var b = Math.floor((v - lo) / (hi - lo) * nb);
        if (b >= 0 && b < nb) h[b]++;
      });
      return h;
    }
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var vals = cc > 0.001 ? RAW.map(function (v) { return Math.log(v + cc); }) : RAW.slice();
      var lo = Math.min.apply(null, vals), hi = Math.max.apply(null, vals);
      var nb = 34, h = hist(vals, lo, hi, nb), mx = Math.max.apply(null, h);
      var box = { x: 70, y: 50, w: 620, h: 180 };
      var S = A.axes(ctx, box, [lo, hi], [0, mx * 1.1], {
        xticks: 5, yticks: 3, xfmt: function (v) { return v.toFixed(1); },
        yfmt: function (v) { return v.toFixed(0); },
        xlab: cc > 0.001 ? 'log(x + ' + cc.toFixed(2) + ')' : 'x — raw feature', ylab: 'count'
      });
      var bw = box.w / nb;
      h.forEach(function (n, i) {
        var x = box.x + i * bw, y = S.Y(n);
        A.rr(ctx, x + 1, y, bw - 2, box.y + box.h - y, 3);
        ctx.fillStyle = P.a; ctx.globalAlpha = .55; ctx.fill(); ctx.globalAlpha = 1;
      });
      /* overlay the Gaussian this feature would be fitted with */
      var m = vals.reduce(function (s, v) { return s + v; }, 0) / vals.length;
      var sd = Math.sqrt(vals.reduce(function (s, v) { return s + (v - m) * (v - m); }, 0) / vals.length);
      A.plot(ctx, S, [lo, hi], function (v) {
        return npdf(v, m, sd) * vals.length * (hi - lo) / nb;
      }, P.b, 2.6);
      var skew = vals.reduce(function (s, v) { return s + Math.pow((v - m) / sd, 3); }, 0) / vals.length;
      var good = Math.abs(skew) < 0.42;
      A.txt(ctx, good ? '✓ close enough to a bell curve' : '✗ badly skewed — the Gaussian fits poorly',
        70, 262, { size: 13.5, w: 700, fill: good ? P.g : P.r });
      A.txt(ctx, 'skewness = ' + skew.toFixed(2) + '  (0 would be a perfect bell)', 70, 284,
        { size: 12, mono: true, fill: P.faint });
      A.txt(ctx, 'The algorithm assumes each feature is roughly Gaussian. When it is not, transform it until it is —',
        70, 308, { size: 12, fill: P.soft });
      A.txt(ctx, 'log(x + c), √x, x^0.4 … whatever makes the histogram look like a hill.', 70, 326,
        { size: 12, w: 700, fill: P.a });
      A.txt(ctx, 'blue curve = the Gaussian that would be fitted to this feature', 380, 38,
        { align: 'center', size: 11.5, fill: P.b });
      ro.set('Second idea in this lesson: when a real anomaly slips through with a high p(x), <b>look at that ' +
        'example by hand</b> and invent a feature that makes it stand out.\nThe classic: a server with normal ' +
        'CPU and normal network traffic, but a very unusual <b>ratio</b> of the two. x<sub>new</sub> = CPU / network.');
    }
    A.bind(c, render); render();
  });

})();
