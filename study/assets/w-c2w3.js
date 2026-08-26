/* Widgets for Course 2 / Week 3 — advice for applying machine learning */
(function () {
  'use strict';

  /* ---------- a tiny deterministic dataset + real polynomial fitting ---------- */
  function rnd(i) { var v = Math.sin(i * 12.9898 + 78.233) * 43758.5453; return v - Math.floor(v); }
  function truth(x) { return 0.55 * Math.sin(x * 1.5) + 0.28 * x - 0.1 * x * x; }
  var DATA = (function () {
    var a = [];
    for (var i = 0; i < 60; i++) {
      var x = -3 + 6 * rnd(i * 3 + 1);
      a.push({ x: x, y: truth(x) + (rnd(i * 7 + 5) - .5) * 0.8 });
    }
    a.sort(function (p, q) { return p.x - q.x; });
    return a;
  })();
  /* fixed shuffle → train 60 / cv 20 / test 20 */
  var ORDER = DATA.map(function (d, i) { return i; })
    .sort(function (a, b) { return rnd(a * 5 + 2) - rnd(b * 5 + 2); });
  var TRAIN = ORDER.slice(0, 30).map(function (i) { return DATA[i]; });
  var CV = ORDER.slice(30, 45).map(function (i) { return DATA[i]; });
  var TEST = ORDER.slice(45).map(function (i) { return DATA[i]; });

  function solve(Amat, bvec) {                     /* gaussian elimination */
    var n = bvec.length, i, j, k;
    var M = Amat.map(function (r, ri) { return r.slice().concat([bvec[ri]]); });
    for (i = 0; i < n; i++) {
      var p = i;
      for (j = i + 1; j < n; j++) if (Math.abs(M[j][i]) > Math.abs(M[p][i])) p = j;
      var tmp = M[i]; M[i] = M[p]; M[p] = tmp;
      if (Math.abs(M[i][i]) < 1e-12) M[i][i] = 1e-12;
      for (j = i + 1; j < n; j++) {
        var f = M[j][i] / M[i][i];
        for (k = i; k <= n; k++) M[j][k] -= f * M[i][k];
      }
    }
    var x = new Array(n);
    for (i = n - 1; i >= 0; i--) {
      var s = M[i][n];
      for (j = i + 1; j < n; j++) s -= M[i][j] * x[j];
      x[i] = s / M[i][i];
    }
    return x;
  }
  var SC = 3;                                    /* scale x into [-1,1] for conditioning */
  function polyfit(pts, deg, lam) {
    lam = lam || 0;
    var n = deg + 1, A = [], b = [], i, j, k;
    for (i = 0; i < n; i++) {
      A.push(new Array(n).fill(0)); b.push(0);
      for (j = 0; j < n; j++)
        for (k = 0; k < pts.length; k++) A[i][j] += Math.pow(pts[k].x / SC, i + j);
      if (i > 0) A[i][i] += lam;                 /* don't regularise the intercept */
      for (k = 0; k < pts.length; k++) b[i] += Math.pow(pts[k].x / SC, i) * pts[k].y;
    }
    return solve(A, b);
  }
  function ev(w, x) { var s = 0; for (var i = 0; i < w.length; i++) s += w[i] * Math.pow(x / SC, i); return s; }
  function cost(w, pts) {
    var s = 0; pts.forEach(function (p) { var d = ev(w, p.x) - p.y; s += d * d; });
    return s / (2 * pts.length);
  }
  /* cache of fits by "deg|lam|set" */
  var FITC = {};
  function fit(pts, deg, lam, tag) {
    var k = tag + '|' + deg + '|' + lam;
    if (!FITC[k]) FITC[k] = polyfit(pts, deg, lam);
    return FITC[k];
  }
  function scatter(ctx, S, pts, colr, r) {
    pts.forEach(function (p) { A.dot(ctx, S.X(p.x), S.Y(p.y), r || 3.6, colr); });
  }

  /* ============================================================
     1. Deciding what to try next
     ============================================================ */
  A.def('whattotry', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var opts = [
      ['get more training examples', 'variance'],
      ['try a smaller set of features', 'variance'],
      ['try getting additional features', 'bias'],
      ['try adding polynomial features', 'bias'],
      ['try decreasing λ', 'bias'],
      ['try increasing λ', 'variance']
    ];
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var hot = Math.floor((t * .6) % 6);
      A.txt(ctx, 'Your model makes unacceptably large errors. Six things you could try:', 40, 38,
        { size: 13, w: 700, fill: P.soft });
      opts.forEach(function (o, i) {
        var y = 60 + i * 40, on = i === hot;
        A.rr(ctx, 40, y, 380, 32, 8);
        ctx.fillStyle = on ? P.aS : P.sunk; ctx.fill();
        ctx.strokeStyle = on ? P.a : P.lineSoft; ctx.lineWidth = on ? 2 : 1; ctx.stroke();
        A.txt(ctx, o[0], 56, y + 21, { size: 12.5, w: on ? 700 : 500, fill: on ? P.a : P.soft });
        if (on) {
          A.arrow(ctx, 430, y + 16, 500, o[1] === 'bias' ? 130 : 230, P.a, 2);
        }
      });
      [['fixes HIGH BIAS', 'underfitting — the model is too simple', 110, P.b],
       ['fixes HIGH VARIANCE', 'overfitting — the model memorised the data', 210, P.p]
      ].forEach(function (bx) {
        A.rr(ctx, 505, bx[2] - 26, 220, 62, 10);
        ctx.fillStyle = bx[3] === P.b ? P.bS : P.pS; ctx.fill();
        ctx.strokeStyle = bx[3]; ctx.lineWidth = 1.8; ctx.stroke();
        A.txt(ctx, bx[0], 615, bx[2] - 4, { align: 'center', size: 13, w: 700, fill: bx[3] });
        A.txt(ctx, bx[1], 615, bx[2] + 16, { align: 'center', size: 10.5, fill: bx[3] });
      });
      A.txt(ctx, 'Each of these costs weeks. Picking by instinct is a coin flip.', 40, 306,
        { size: 12, fill: P.faint });
      A.txt(ctx, 'A diagnostic tells you WHICH half of the list to look at — that is the whole point of this week.',
        40, 324, { size: 12, w: 700, fill: P.a });
    }
    A.bind(c, function () { render(lt); });
    var lt = 0; A.loop(c.cv, function (t) { lt = t; render(t); });
  });

  /* ============================================================
     2. Train / test split
     ============================================================ */
  A.def('traintest', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var deg = 1;
    var bar = A.ctrls(root), ro = A.readout(root);
    A.slider(bar, { label: 'polynomial degree d =', min: 1, max: 10, step: 1, value: deg,
      fmt: function (v) { return v.toFixed(0); }, on: function (v) { deg = v; render(); } });
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var TR = TRAIN, TE = TEST;
      var w = fit(TR, deg, 0, 'tt');
      var jtr = cost(w, TR), jte = cost(w, TE);
      var box = { x: 70, y: 34, w: 430, h: 220 };
      var S = A.axes(ctx, box, [-3.2, 3.2], [-2.6, 2.2], {
        xticks: 4, yticks: 4, xfmt: function (v) { return v.toFixed(0); },
        yfmt: function (v) { return v.toFixed(0); }, xlab: 'x', ylab: 'y'
      });
      A.plot(ctx, S, [-3.2, 3.2], function (x) { return A.clamp(ev(w, x), -3, 3); }, P.a, 2.6);
      scatter(ctx, S, TR, P.b, 3.6);
      scatter(ctx, S, TE, P.r, 5);
      A.txt(ctx, 'degree ' + deg, box.x + 12, box.y + 20, { size: 14, w: 700, fill: P.a });
      /* the two costs as bars */
      var bx = 560, maxJ = 0.45;
      [['J train', jtr, P.b], ['J test', jte, P.r]].forEach(function (r, i) {
        var y = 70 + i * 78;
        A.txt(ctx, r[0], bx, y - 8, { size: 12.5, w: 700, fill: r[2] });
        A.rr(ctx, bx, y, 150, 26, 5); ctx.fillStyle = P.sunk; ctx.fill();
        A.rr(ctx, bx, y, Math.max(3, 150 * A.clamp(r[1] / maxJ, 0, 1)), 26, 5);
        ctx.fillStyle = r[2]; ctx.globalAlpha = .8; ctx.fill(); ctx.globalAlpha = 1;
        A.txt(ctx, r[1].toFixed(3), bx + 158, y + 18, { size: 12.5, mono: true, w: 700, fill: P.ink });
      });
      var verdict = deg <= 2 ? 'both errors high → UNDERFIT'
        : jte > jtr * 2.5 ? 'train tiny, test large → OVERFIT'
        : 'both low and close → looks good';
      A.txt(ctx, verdict, bx, 245, { size: 13, w: 700,
        fill: deg <= 2 ? P.b : jte > jtr * 2.5 ? P.r : P.g });
      A.legend(root, [[P.b, 'training examples (⅔)'], [P.r, 'test examples (⅓) — never trained on'],
        [P.a, 'the fitted curve']]);
      A.txt(ctx, 'Push the degree to 12: the curve threads every blue point and the red error explodes.',
        70, 296, { size: 12, fill: P.faint });
      A.txt(ctx, 'That gap between J_train and J_test IS overfitting, measured.', 70, 316,
        { size: 12, w: 700, fill: P.soft });
      ro.set('J<sub>train</sub> = <b>' + jtr.toFixed(4) + '</b>   J<sub>test</sub> = <b>' + jte.toFixed(4) +
        '</b>   ratio = <b>' + (jte / jtr).toFixed(1) + '×</b>' +
        '\nJ = (1/2m) Σ (f(x⁽ⁱ⁾) − y⁽ⁱ⁾)²  — the same formula, computed on two different sets of examples.');
    }
    A.bind(c, render); render();
  });

  /* ============================================================
     3. Train / cross-validation / test
     ============================================================ */
  A.def('splitcv', function (root) {
    var c = A.canvas(root, 760, 340), ctx = c.ctx;
    var ro = A.readout(root);
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      /* the split bar */
      var segs = [['training set', 60, P.b, '60%'], ['cross-validation', 20, P.a, '20%'], ['test', 20, P.g, '20%']];
      var x = 60;
      segs.forEach(function (s) {
        var w = 6.4 * s[1];
        A.rr(ctx, x, 44, w - 4, 46, 8); ctx.fillStyle = s[2]; ctx.globalAlpha = .22; ctx.fill();
        ctx.globalAlpha = 1; ctx.strokeStyle = s[2]; ctx.lineWidth = 1.8; ctx.stroke();
        A.txt(ctx, s[0], x + w / 2 - 2, 66, { align: 'center', size: 12.5, w: 700, fill: s[2] });
        A.txt(ctx, s[3], x + w / 2 - 2, 82, { align: 'center', size: 11, fill: s[2] });
        x += w;
      });
      A.txt(ctx, 'all your data', 60, 34, { size: 12, fill: P.faint });
      /* degree table */
      var degs = [1, 2, 3, 4, 5, 6, 7, 8];
      var jcv = degs.map(function (d) { return cost(fit(TRAIN, d, 0, 'cv'), CV); });
      var jtr = degs.map(function (d) { return cost(fit(TRAIN, d, 0, 'cv'), TRAIN); });
      var best = 0; jcv.forEach(function (v, i) { if (v < jcv[best]) best = i; });
      var reveal = Math.min(degs.length, Math.floor((t * 1.1) % (degs.length + 5)));
      A.txt(ctx, 'fit each degree on TRAIN, score it on CROSS-VALIDATION', 60, 124,
        { size: 12.5, w: 700, fill: P.soft });
      degs.forEach(function (d, i) {
        var bx = 60 + i * 84, on = (reveal > degs.length && i === best);
        A.rr(ctx, bx, 140, 76, 96, 8);
        ctx.fillStyle = on ? P.aS : P.sunk; ctx.fill();
        ctx.strokeStyle = on ? P.a : P.lineSoft; ctx.lineWidth = on ? 2.2 : 1; ctx.stroke();
        A.txt(ctx, 'd = ' + d, bx + 38, 160, { align: 'center', size: 12.5, w: 700, fill: on ? P.a : P.soft });
        if (i < reveal) {
          A.txt(ctx, 'train', bx + 38, 182, { align: 'center', size: 10, fill: P.faint });
          A.txt(ctx, jtr[i].toFixed(3), bx + 38, 196, { align: 'center', size: 11.5, mono: true, fill: P.b });
          A.txt(ctx, 'cv', bx + 38, 212, { align: 'center', size: 10, fill: P.faint });
          A.txt(ctx, jcv[i].toFixed(3), bx + 38, 226, { align: 'center', size: 12, mono: true, w: 700,
            fill: on ? P.a : P.soft });
        } else {
          A.txt(ctx, '…', bx + 38, 200, { align: 'center', size: 16, fill: P.faint });
        }
      });
      if (reveal > degs.length) {
        A.txt(ctx, 'winner: degree ' + degs[best] + ' — lowest cross-validation error', 60, 262,
          { size: 13, w: 700, fill: P.a });
        A.txt(ctx, 'ONLY NOW do you touch the test set — once — to report an honest error.', 60, 284,
          { size: 12.5, w: 700, fill: P.g });
        A.txt(ctx, 'J_test = ' + cost(fit(TRAIN, degs[best], 0, 'cv'), TEST).toFixed(4), 60, 306,
          { size: 12.5, mono: true, fill: P.g });
      } else {
        A.txt(ctx, 'trying each candidate…', 60, 262, { size: 13, fill: P.faint });
      }
      ro.set('If you pick the degree using the TEST set, the test error is no longer an honest estimate — ' +
        'you fitted a choice to it.\nThat is why there are three sets: <b>train</b> fits the parameters, ' +
        '<b>cross-validation</b> picks the model, <b>test</b> is only ever read at the very end.');
    }
    A.bind(c, function () { render(lt); });
    var lt = 0; A.loop(c.cv, function (t) { lt = t; render(t); });
  });

  /* ============================================================
     4. Bias and variance vs model complexity
     ============================================================ */
  A.def('biasvar', function (root) {
    var c = A.canvas(root, 760, 340), ctx = c.ctx;
    var deg = 2;
    var bar = A.ctrls(root), ro = A.readout(root);
    A.slider(bar, { label: 'degree d =', min: 1, max: 10, step: 1, value: deg,
      fmt: function (v) { return v.toFixed(0); }, on: function (v) { deg = v; render(); } });
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var w = fit(TRAIN, deg, 0, 'bv');
      var jt = cost(w, TRAIN), jc = cost(w, CV);
      var b1 = { x: 60, y: 40, w: 300, h: 210 };
      var S = A.axes(ctx, b1, [-3.2, 3.2], [-2.6, 2.2], { xticks: 4, yticks: 4, xlab: 'x', ylab: 'y' });
      A.plot(ctx, S, [-3.2, 3.2], function (x) { return A.clamp(ev(w, x), -3, 3); }, P.a, 2.6);
      scatter(ctx, S, TRAIN, P.b, 3.4); scatter(ctx, S, CV, P.p, 4.4);
      A.txt(ctx, 'degree ' + deg, b1.x + 10, b1.y + 20, { size: 14, w: 700, fill: P.a });
      /* the curves */
      var b2 = { x: 460, y: 40, w: 250, h: 210 };
      var degs = [], jts = [], jcs = [], i;
      for (i = 1; i <= 10; i++) { var ww = fit(TRAIN, i, 0, 'bv'); degs.push(i); jts.push(cost(ww, TRAIN)); jcs.push(cost(ww, CV)); }
      var top = 0.5;
      var S2 = A.axes(ctx, b2, [1, 10], [0, top], {
        xticks: 4, yticks: 4, xfmt: function (v) { return v.toFixed(0); },
        yfmt: function (v) { return v.toFixed(1); }, xlab: 'degree of polynomial', ylab: 'error'
      });
      function poly(arr, colr) {
        ctx.save(); ctx.strokeStyle = colr; ctx.lineWidth = 2.4; ctx.beginPath();
        arr.forEach(function (v, k) {
          var px = S2.X(k + 1), py = S2.Y(Math.min(v, top));
          k === 0 ? ctx.moveTo(px, py) : ctx.lineTo(px, py);
        });
        ctx.stroke(); ctx.restore();
      }
      poly(jts, P.b); poly(jcs, P.p);
      A.dot(ctx, S2.X(deg), S2.Y(Math.min(jts[deg - 1], top)), 6, P.b);
      A.dot(ctx, S2.X(deg), S2.Y(Math.min(jcs[deg - 1], top)), 6, P.p);
      A.line(ctx, S2.X(deg), b2.y, S2.X(deg), b2.y + b2.h, P.a, 1.4, [4, 3]);
      A.txt(ctx, 'J_cv', S2.X(8.6), S2.Y(.44), { size: 12, w: 700, fill: P.p });
      A.txt(ctx, 'J_train', S2.X(7.6), S2.Y(.06), { size: 12, w: 700, fill: P.b });
      A.txt(ctx, 'high bias', S2.X(1.3), S2.Y(.46), { size: 11, fill: P.faint });
      A.txt(ctx, 'high variance', S2.X(6.6), S2.Y(.48), { size: 11, fill: P.faint });
      var diag = (jt > .07) ? ['HIGH BIAS — underfitting', P.b,
          'J_train is high, and J_cv is about the same. The model is too simple for the data.']
        : (jc > jt * 2.2) ? ['HIGH VARIANCE — overfitting', P.p,
          'J_train is low but J_cv is much higher. The model memorised the training set.']
        : ['JUST RIGHT', P.g, 'Both errors are low and close together.'];
      A.txt(ctx, diag[0], 60, 282, { size: 15, w: 700, fill: diag[1] });
      A.txt(ctx, diag[2], 60, 304, { size: 12, fill: P.soft });
      A.txt(ctx, 'J_train = ' + jt.toFixed(3) + '    J_cv = ' + jc.toFixed(3), 60, 326,
        { size: 12.5, mono: true, fill: P.faint });
      ro.set('<b>High bias:</b> J<sub>train</sub> is high  (and J<sub>cv</sub> ≈ J<sub>train</sub>)' +
        '\n<b>High variance:</b> J<sub>cv</sub> ≫ J<sub>train</sub>' +
        '\nYou can have both at once — high J<sub>train</sub> AND an even higher J<sub>cv</sub>.');
    }
    A.bind(c, render); render();
  });

  /* ============================================================
     5. Regularisation and bias / variance
     ============================================================ */
  A.def('lambdacurve', function (root) {
    var c = A.canvas(root, 760, 340), ctx = c.ctx;
    var li = 0;
    var lams = [0, 0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1, 3, 10, 100];
    var bar = A.ctrls(root), ro = A.readout(root);
    A.slider(bar, { label: 'λ =', min: 0, max: 10, step: 1, value: li,
      fmt: function (v) { return String(lams[v]); }, on: function (v) { li = v; render(); } });
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var D = 10;
      var w = fit(TRAIN, D, lams[li], 'lam');
      var jt = cost(w, TRAIN), jc = cost(w, CV);
      var b1 = { x: 60, y: 40, w: 300, h: 210 };
      var S = A.axes(ctx, b1, [-3.2, 3.2], [-2.6, 2.2], { xticks: 4, yticks: 4, xlab: 'x', ylab: 'y' });
      A.plot(ctx, S, [-3.2, 3.2], function (x) { return A.clamp(ev(w, x), -3, 3); }, P.a, 2.6);
      scatter(ctx, S, TRAIN, P.b, 3.4); scatter(ctx, S, CV, P.p, 4.4);
      A.txt(ctx, 'degree 10, λ = ' + lams[li], b1.x + 10, b1.y + 20, { size: 13.5, w: 700, fill: P.a });
      var b2 = { x: 460, y: 40, w: 250, h: 210 };
      var jts = [], jcs = [], i;
      for (i = 0; i < lams.length; i++) {
        var ww = fit(TRAIN, D, lams[i], 'lam');
        jts.push(cost(ww, TRAIN)); jcs.push(cost(ww, CV));
      }
      var top = 0.5;
      var S2 = A.axes(ctx, b2, [0, lams.length - 1], [0, top], {
        xticks: 5, yticks: 4, xfmt: function (v) { return ['0', '', '0.01', '', '0.3', '', '3', '', '100'][Math.round(v / 1.25)] || ''; },
        yfmt: function (v) { return v.toFixed(1); }, xlab: 'λ  (small → large)', ylab: 'error'
      });
      function poly(arr, colr) {
        ctx.save(); ctx.strokeStyle = colr; ctx.lineWidth = 2.4; ctx.beginPath();
        arr.forEach(function (v, k) {
          var px = S2.X(k), py = S2.Y(Math.min(v, top));
          k === 0 ? ctx.moveTo(px, py) : ctx.lineTo(px, py);
        });
        ctx.stroke(); ctx.restore();
      }
      poly(jts, P.b); poly(jcs, P.p);
      A.line(ctx, S2.X(li), b2.y, S2.X(li), b2.y + b2.h, P.a, 1.4, [4, 3]);
      A.dot(ctx, S2.X(li), S2.Y(Math.min(jts[li], top)), 6, P.b);
      A.dot(ctx, S2.X(li), S2.Y(Math.min(jcs[li], top)), 6, P.p);
      A.txt(ctx, 'J_cv', S2.X(7.6), S2.Y(.2), { size: 12, w: 700, fill: P.p });
      A.txt(ctx, 'J_train', S2.X(4.0), S2.Y(.06), { size: 12, w: 700, fill: P.b });
      A.txt(ctx, 'overfit', S2.X(0.2), S2.Y(.46), { size: 11, fill: P.faint });
      A.txt(ctx, 'underfit', S2.X(8.2), S2.Y(.46), { size: 11, fill: P.faint });
      var msg = lams[li] <= 0.003 ? ['λ too SMALL → high variance', P.p, 'the wiggly curve is free to chase noise']
        : lams[li] >= 1 ? ['λ too LARGE → high bias', P.b, 'the weights are crushed towards 0; it can barely bend']
        : ['λ about right', P.g, 'flexible enough to follow the pattern, stiff enough to ignore the noise'];
      A.txt(ctx, msg[0], 60, 284, { size: 15, w: 700, fill: msg[1] });
      A.txt(ctx, msg[2], 60, 306, { size: 12, fill: P.soft });
      A.txt(ctx, 'J_train = ' + jt.toFixed(3) + '    J_cv = ' + jc.toFixed(3), 60, 328,
        { size: 12.5, mono: true, fill: P.faint });
      ro.set('This picture is the DEGREE picture, mirrored. Small λ behaves like a high degree (overfit); ' +
        'large λ behaves like a low degree (underfit).\nPick λ the same way you picked the degree: try a ' +
        'ladder of values, keep the one with the lowest J<sub>cv</sub>.');
    }
    A.bind(c, render); render();
  });

  /* ============================================================
     6. Baseline level of performance
     ============================================================ */
  A.def('baseline', function (root) {
    var c = A.canvas(root, 760, 300), ctx = c.ctx;
    var scen = 0;
    var scenarios = [
      { n: 'clean audio', base: 10.6, tr: 10.8, cv: 14.8, verdict: 'HIGH VARIANCE', why: 'gap to baseline 0.2%, gap train→cv 4.0%' },
      { n: 'noisy audio', base: 10.6, tr: 15.0, cv: 15.5, verdict: 'HIGH BIAS', why: 'gap to baseline 4.4%, gap train→cv 0.5%' },
      { n: 'both problems', base: 10.6, tr: 15.0, cv: 19.7, verdict: 'HIGH BIAS *AND* HIGH VARIANCE', why: 'gap to baseline 4.4%, gap train→cv 4.7%' }
    ];
    var bar = A.ctrls(root);
    scenarios.forEach(function (s, i) { A.button(bar, s.n, function () { scen = i; sync(); render(); }); });
    function sync() { bar.querySelectorAll('button').forEach(function (b, i) { b.classList.toggle('primary', i === scen); }); }
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var s = scenarios[scen], mx = 24;
      var bars = [['human / baseline', s.base, P.g], ['J train', s.tr, P.b], ['J cv', s.cv, P.p]];
      bars.forEach(function (r, i) {
        var y = 70 + i * 62;
        A.txt(ctx, r[0], 190, y + 22, { align: 'right', size: 12.5, w: 700, fill: r[2] });
        A.rr(ctx, 205, y, 440, 32, 6); ctx.fillStyle = P.sunk; ctx.fill();
        A.rr(ctx, 205, y, 440 * (r[1] / mx), 32, 6);
        ctx.fillStyle = r[2]; ctx.globalAlpha = .8; ctx.fill(); ctx.globalAlpha = 1;
        A.txt(ctx, r[1].toFixed(1) + '%', 205 + 440 * (r[1] / mx) + 10, y + 22,
          { size: 13, mono: true, w: 700, fill: P.ink });
      });
      /* gap annotations */
      var xb = 205 + 440 * (s.base / mx), xt = 205 + 440 * (s.tr / mx), xc = 205 + 440 * (s.cv / mx);
      A.line(ctx, xb, 102, xt, 102, P.a, 1.6, [3, 3]);
      A.txt(ctx, 'bias gap ' + (s.tr - s.base).toFixed(1) + '%', (xb + xt) / 2, 96,
        { align: 'center', size: 11, w: 700, fill: P.a });
      A.line(ctx, xt, 164, xc, 164, P.a, 1.6, [3, 3]);
      A.txt(ctx, 'variance gap ' + (s.cv - s.tr).toFixed(1) + '%', (xt + xc) / 2, 158,
        { align: 'center', size: 11, w: 700, fill: P.a });
      A.txt(ctx, s.verdict, 380, 262, { align: 'center', size: 16, w: 700, fill: P.a });
      A.txt(ctx, s.why, 380, 284, { align: 'center', size: 12, fill: P.faint });
      A.txt(ctx, '10.8% training error sounds terrible — until you learn humans get 10.6% on the same audio.',
        60, 40, { size: 12.5, w: 600, fill: P.soft });
    }
    sync(); A.bind(c, render); render();
  });

  /* ============================================================
     7. Learning curves
     ============================================================ */
  A.def('learncurve', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var mode = 0;
    var bar = A.ctrls(root), ro = A.readout(root);
    ['high bias (too simple)', 'high variance (too complex)'].forEach(function (n, i) {
      A.button(bar, n, function () { mode = i; sync(); render(); });
    });
    function sync() { bar.querySelectorAll('button').forEach(function (b, i) { b.classList.toggle('primary', i === mode); }); }
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var box = { x: 80, y: 40, w: 600, h: 210 };
      var S = A.axes(ctx, box, [1, 100], [0, 1], {
        xticks: 5, yticks: 4, xfmt: function (v) { return v.toFixed(0); },
        yfmt: function (v) { return v.toFixed(1); },
        xlab: 'm — number of training examples', ylab: 'error'
      });
      var base = mode === 0 ? 0.52 : 0.08;
      var jtr = function (m) { return base * (1 - Math.exp(-m / 14)) * (mode === 0 ? 1 : 1.0) + (mode === 0 ? 0.06 : 0.01); };
      var jcv = function (m) { return base + (mode === 0 ? 0.10 : 0.62) * Math.exp(-m / (mode === 0 ? 16 : 45)) + 0.05; };
      A.plot(ctx, S, [1, 100], jtr, P.b, 2.8);
      A.plot(ctx, S, [1, 100], jcv, P.p, 2.8);
      /* the baseline */
      var hb = mode === 0 ? 0.12 : 0.12;
      A.line(ctx, box.x, S.Y(hb), box.x + box.w, S.Y(hb), P.g, 2, [6, 4]);
      A.txt(ctx, 'human-level performance', box.x + box.w - 6, S.Y(hb) - 8,
        { align: 'right', size: 11.5, w: 700, fill: P.g });
      A.txt(ctx, 'J_cv', S.X(88), S.Y(jcv(88)) - 12, { size: 12.5, w: 700, fill: P.p });
      A.txt(ctx, 'J_train', S.X(88), S.Y(jtr(88)) + 18, { size: 12.5, w: 700, fill: P.b });
      if (mode === 0) {
        ctx.save(); ctx.fillStyle = P.b; ctx.globalAlpha = .1;
        ctx.fillRect(S.X(45), S.Y(jcv(45)), S.X(100) - S.X(45), S.Y(hb) - S.Y(jcv(45)));
        ctx.restore();
        A.txt(ctx, 'both curves have FLATTENED, well above human level', 90, 282,
          { size: 13.5, w: 700, fill: P.b });
        A.txt(ctx, '→ more data will NOT help. The model itself is too simple. Add features, add capacity, lower λ.',
          90, 304, { size: 12.5, fill: P.soft });
      } else {
        A.arrow(ctx, S.X(70), S.Y(jcv(70)) - 6, S.X(95), S.Y(jcv(95)) - 6, P.a, 2);
        A.txt(ctx, 'big gap, and J_cv is still coming down', 90, 282, { size: 13.5, w: 700, fill: P.p });
        A.txt(ctx, '→ more data WILL help. The gap closes as m grows. Also try more λ or fewer features.',
          90, 304, { size: 12.5, fill: P.soft });
      }
      ro.set('J<sub>train</sub> <b>rises</b> with m (harder to fit 100 points perfectly than 3) and ' +
        'J<sub>cv</sub> <b>falls</b> with m.\nIf they have already met and flattened, buying more data buys you nothing.');
    }
    sync(); A.bind(c, render); render();
  });

  /* ============================================================
     8. Symptom → fix
     ============================================================ */
  A.def('fixtable', function (root) {
    var c = A.canvas(root, 760, 320), ctx = c.ctx;
    var rows = [
      ['get more training examples', 1], ['try a smaller set of features', 1],
      ['try increasing λ', 1], ['try getting additional features', 0],
      ['try adding polynomial features', 0], ['try decreasing λ', 0]
    ];
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var hot = Math.floor((t * .55) % 6);
      A.txt(ctx, 'Once you know WHICH problem you have, the list stops being a guess:', 40, 36,
        { size: 13, w: 700, fill: P.soft });
      A.rr(ctx, 40, 56, 340, 120, 10); ctx.fillStyle = P.pS; ctx.fill();
      ctx.strokeStyle = P.p; ctx.lineWidth = 1.8; ctx.stroke();
      A.txt(ctx, 'HIGH VARIANCE (overfitting)', 210, 78, { align: 'center', size: 13, w: 700, fill: P.p });
      A.rr(ctx, 400, 56, 320, 120, 10); ctx.fillStyle = P.bS; ctx.fill();
      ctx.strokeStyle = P.b; ctx.lineWidth = 1.8; ctx.stroke();
      A.txt(ctx, 'HIGH BIAS (underfitting)', 560, 78, { align: 'center', size: 13, w: 700, fill: P.b });
      rows.forEach(function (r, i) {
        var isVar = r[1] === 1;
        var k = isVar ? i : i - 3;
        var x = isVar ? 56 : 416, y = 96 + k * 26;
        var on = i === hot;
        A.txt(ctx, (on ? '▸ ' : '· ') + r[0], x, y + 12,
          { size: 12, w: on ? 700 : 500, fill: on ? (isVar ? P.p : P.b) : P.soft });
      });
      A.txt(ctx, 'Why these and not the others?', 40, 210, { size: 12.5, w: 700, fill: P.soft });
      var why = rows[hot][1] === 1
        ? 'More data, fewer features and a bigger λ all make the model LESS able to memorise noise.'
        : 'More features, polynomial terms and a smaller λ all make the model MORE able to bend.';
      A.txt(ctx, why, 40, 234, { size: 12.5, fill: rows[hot][1] === 1 ? P.p : P.b });
      A.txt(ctx, 'Notice: “get more data” only appears on the variance side. It is the most expensive item on',
        40, 268, { size: 12, fill: P.faint });
      A.txt(ctx, 'the list and it is useless against high bias — which is why the diagnostic pays for itself.',
        40, 286, { size: 12, fill: P.faint });
    }
    A.bind(c, function () { render(lt); });
    var lt = 0; A.loop(c.cv, function (t) { lt = t; render(t); });
  });

  /* ============================================================
     9. The neural-network recipe
     ============================================================ */
  A.def('nnrecipe', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var step = Math.floor((t * .5) % 5);
      var boxes = [
        { x: 300, y: 40, w: 200, h: 44, t: 'train the network', c: P.soft },
        { x: 260, y: 106, w: 280, h: 48, t: 'does it do well on the TRAINING set?', c: P.b },
        { x: 60, y: 180, w: 200, h: 48, t: 'bigger network', s: 'more layers / more units', c: P.b },
        { x: 260, y: 186, w: 280, h: 48, t: 'does it do well on the CV set?', c: P.p },
        { x: 560, y: 260, w: 160, h: 48, t: 'more data', s: 'or regularise', c: P.p },
        { x: 260, y: 266, w: 200, h: 44, t: '✓ done', c: P.g }
      ];
      var lit = [0, 1, 2, 3, 5];
      boxes.forEach(function (b, i) {
        var on = lit.indexOf(i) === step || (step >= 2 && i === 2 && step === 2) ;
        on = (step === 0 && i === 0) || (step === 1 && i === 1) || (step === 2 && i === 2) ||
             (step === 3 && i === 3) || (step === 4 && i === 5);
        A.rr(ctx, b.x, b.y, b.w, b.h, 9);
        ctx.fillStyle = on ? P.aS : P.sunk; ctx.fill();
        ctx.strokeStyle = on ? P.a : (b.c === P.g ? P.g : P.lineSoft); ctx.lineWidth = on ? 2.2 : 1.2; ctx.stroke();
        A.txt(ctx, b.t, b.x + b.w / 2, b.y + (b.s ? 22 : 27), { align: 'center', size: 12.5, w: 700,
          fill: on ? P.a : b.c });
        if (b.s) A.txt(ctx, b.s, b.x + b.w / 2, b.y + 38, { align: 'center', size: 10.5, fill: P.faint });
      });
      A.arrow(ctx, 400, 84, 400, 104, P.line, 1.8);
      A.arrow(ctx, 260, 130, 162, 178, P.line, 1.8);
      A.txt(ctx, 'no', 200, 148, { size: 11.5, w: 700, fill: P.b });
      A.arrow(ctx, 400, 154, 400, 184, P.line, 1.8);
      A.txt(ctx, 'yes', 410, 172, { size: 11.5, w: 700, fill: P.g });
      A.arrow(ctx, 540, 210, 620, 258, P.line, 1.8);
      A.txt(ctx, 'no', 590, 228, { size: 11.5, w: 700, fill: P.p });
      A.arrow(ctx, 380, 234, 370, 264, P.line, 1.8);
      A.txt(ctx, 'yes', 388, 254, { size: 11.5, w: 700, fill: P.g });
      /* loops back */
      ctx.save(); ctx.strokeStyle = P.lineSoft; ctx.lineWidth = 1.6; ctx.setLineDash([4, 4]);
      ctx.beginPath(); ctx.moveTo(160, 180); ctx.bezierCurveTo(60, 120, 120, 40, 296, 60); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(720, 284); ctx.bezierCurveTo(748, 160, 640, 40, 504, 60); ctx.stroke();
      ctx.restore();
      A.txt(ctx, 'A large neural network with proper regularisation is almost always at least as good',
        40, 306, { size: 12, fill: P.faint });
      A.txt(ctx, 'as a smaller one — so “too big” is a compute problem, not an accuracy problem.',
        40, 322, { size: 12, fill: P.faint });
    }
    A.bind(c, function () { render(lt); });
    var lt = 0; A.loop(c.cv, function (t) { lt = t; render(t); });
  });

})();

/* ---------- part 2 : the development loop, data, metrics ---------- */
(function () {
  'use strict';

  function rnd(i) { var v = Math.sin(i * 45.164 + 12.771) * 24634.6345; return v - Math.floor(v); }

  /* a deliberately skewed, scored test set: 400 examples, 5% positive */
  var SCORED = (function () {
    var a = [], i;
    for (i = 0; i < 400; i++) {
      var pos = rnd(i * 3 + 7) < 0.05;
      var r1 = rnd(i * 11 + 3), r2 = rnd(i * 17 + 5);
      var g = Math.sqrt(-2 * Math.log(r1 + 1e-9)) * Math.cos(6.2832 * r2);  /* box-muller */
      var s = A.sig((pos ? 1.9 : -1.6) + g * 1.15);
      a.push({ y: pos ? 1 : 0, s: s });
    }
    return a;
  })();
  function confuse(th) {
    var tp = 0, fp = 0, fn = 0, tn = 0;
    SCORED.forEach(function (e) {
      var p = e.s >= th ? 1 : 0;
      if (e.y === 1 && p === 1) tp++;
      else if (e.y === 0 && p === 1) fp++;
      else if (e.y === 1 && p === 0) fn++;
      else tn++;
    });
    var prec = tp + fp ? tp / (tp + fp) : 1;
    var rec = tp + fn ? tp / (tp + fn) : 0;
    var f1 = prec + rec ? 2 * prec * rec / (prec + rec) : 0;
    return { tp: tp, fp: fp, fn: fn, tn: tn, prec: prec, rec: rec, f1: f1,
             acc: (tp + tn) / SCORED.length };
  }

  /* ============================================================
     10. The iterative loop of ML development
     ============================================================ */
  A.def('mlloop', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var steps = [
      { t: 'choose architecture', s: 'model, data, features', a: -Math.PI / 2 },
      { t: 'train the model', s: 'and it will not work the first time', a: Math.PI / 6 },
      { t: 'run diagnostics', s: 'bias / variance / error analysis', a: Math.PI * 5 / 6 }
    ];
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var cx = 300, cy = 170, R = 105;
      var cur = Math.floor((t * .45) % 3);
      ctx.save(); ctx.strokeStyle = P.lineSoft; ctx.lineWidth = 26;
      ctx.beginPath(); ctx.arc(cx, cy, R, 0, 6.2832); ctx.stroke(); ctx.restore();
      /* moving highlight arc */
      var a0 = steps[cur].a - .55, a1 = steps[cur].a + .55;
      ctx.save(); ctx.strokeStyle = P.a; ctx.lineWidth = 26; ctx.globalAlpha = .28;
      ctx.beginPath(); ctx.arc(cx, cy, R, a0, a1); ctx.stroke(); ctx.restore();
      steps.forEach(function (s, i) {
        var x = cx + Math.cos(s.a) * R, y = cy + Math.sin(s.a) * R;
        var on = i === cur;
        A.dot(ctx, x, y, on ? 15 : 11, on ? P.a : P.line);
        A.dot(ctx, x, y, on ? 9 : 6, P.panel);
        var lx = cx + Math.cos(s.a) * (R + 40), ly = cy + Math.sin(s.a) * (R + 40);
        var al = Math.abs(Math.cos(s.a)) < .3 ? 'center' : (Math.cos(s.a) > 0 ? 'left' : 'right');
        A.txt(ctx, s.t, lx, ly, { align: al, size: 13, w: 700, fill: on ? P.a : P.soft });
        A.txt(ctx, s.s, lx, ly + 16, { align: al, size: 11, fill: P.faint });
      });
      /* the spinning arrow */
      var ang = (t * .8) % 6.2832;
      A.dot(ctx, cx + Math.cos(ang) * R, cy + Math.sin(ang) * R, 5, P.a);
      A.txt(ctx, 'round and round', cx, cy - 6, { align: 'center', size: 12.5, w: 700, fill: P.faint });
      A.txt(ctx, 'until it is good enough', cx, cy + 12, { align: 'center', size: 12.5, fill: P.faint });
      A.rr(ctx, 500, 60, 230, 210, 10); ctx.fillStyle = P.sunk; ctx.fill();
      ctx.strokeStyle = P.lineSoft; ctx.stroke();
      A.txt(ctx, 'Nobody gets it right first time', 615, 88, { align: 'center', size: 12.5, w: 700, fill: P.soft });
      ['Your first model will be bad.', 'That is not failure — that is', 'the first lap of the loop.', '',
       'The skill being taught here is', 'how to make each lap SHORT', 'and each decision INFORMED.'
      ].forEach(function (ln, i) {
        A.txt(ctx, ln, 615, 116 + i * 20, { align: 'center', size: 11.5, fill: P.faint });
      });
      A.txt(ctx, 'Speed round the loop matters more than cleverness on any single lap.', 60, 312,
        { size: 12, w: 700, fill: P.soft });
    }
    A.bind(c, function () { render(lt); });
    var lt = 0; A.loop(c.cv, function (t) { lt = t; render(t); });
  });

  /* ============================================================
     11. Error analysis
     ============================================================ */
  A.def('erroranalysis', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var bins = [
      { n: 'pharmaceutical spam', k: 21, fix: 'add drug-name features' },
      { n: 'deliberate misspellings', k: 3, fix: 'not worth it — only 3 emails' },
      { n: 'unusual email routing', k: 7, fix: 'parse headers' },
      { n: 'phishing / stolen passwords', k: 18, fix: 'add URL features' },
      { n: 'spam in embedded images', k: 5, fix: 'hard, and rare' },
      { n: 'other', k: 46, fix: 'look again, more carefully' }
    ];
    var N = 100;
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var phase = A.clamp(((t * .35) % 3) - .2, 0, 1);
      var cols = [P.a, P.faint, P.b, P.p, P.faint, P.line];
      A.txt(ctx, '100 misclassified emails, read by hand', 40, 36, { size: 13, w: 700, fill: P.soft });
      var idx = 0;
      bins.forEach(function (b, bi) {
        for (var k = 0; k < b.k; k++) {
          var i = idx++;
          var sx = 44 + (i % 20) * 17, sy = 56 + Math.floor(i / 20) * 17;
          var tx = 300 + (k % 8) * 13, ty = 168 + bi * 26 + Math.floor(k / 8) * 0;
          var x = A.lerp(sx, tx, A.ease(phase)), y = A.lerp(sy, ty, A.ease(phase));
          A.dot(ctx, x, y, 4.6, phase > .5 ? cols[bi] : P.faint);
        }
      });
      if (phase > .6) {
        bins.forEach(function (b, bi) {
          var y = 172 + bi * 26;
          A.txt(ctx, b.n, 290, y + 4, { align: 'right', size: 12, w: b.k > 15 ? 700 : 500,
            fill: b.k > 15 ? cols[bi] : P.faint });
          A.txt(ctx, b.k, 420, y + 4, { size: 12.5, mono: true, w: 700, fill: b.k > 15 ? cols[bi] : P.faint });
          A.txt(ctx, '→ ' + b.fix, 450, y + 4, { size: 11.5, fill: b.k > 15 ? P.soft : P.faint });
        });
        A.txt(ctx, 'Fix pharma + phishing first: that is 39 of the 100. Misspellings is 3 — ignore it.',
          40, 320, { size: 12.5, w: 700, fill: P.a });
      } else {
        A.txt(ctx, 'sorting them into piles…', 300, 200, { size: 13, fill: P.faint });
      }
      A.txt(ctx, 'categories can overlap — one email can be both pharma and phishing', 40, 148,
        { size: 11.5, fill: P.faint });
    }
    A.bind(c, function () { render(lt); });
    var lt = 0; A.loop(c.cv, function (t) { lt = t; render(t); });
  });

  /* ============================================================
     12. Adding data — augmentation
     ============================================================ */
  A.def('augment', function (root) {
    var c = A.canvas(root, 760, 300), ctx = c.ctx;
    function letterA(x, y, s, rot, warp, P, colr) {
      ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s);
      ctx.transform(1, warp, warp * .6, 1, 0, 0);
      ctx.strokeStyle = colr; ctx.lineWidth = 7 / s; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
      ctx.beginPath();
      ctx.moveTo(-18, 24); ctx.lineTo(0, -24); ctx.lineTo(18, 24);
      ctx.moveTo(-10, 6); ctx.lineTo(10, 6);
      ctx.stroke(); ctx.restore();
    }
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      A.txt(ctx, 'one letter you have', 100, 40, { align: 'center', size: 12.5, w: 700, fill: P.soft });
      A.rr(ctx, 40, 54, 120, 120, 10); ctx.fillStyle = P.sunk; ctx.fill();
      ctx.strokeStyle = P.line; ctx.lineWidth = 1.6; ctx.stroke();
      letterA(100, 114, 1.5, 0, 0, P, P.ink);
      A.arrow(ctx, 176, 114, 214, 114, P.line, 2);
      A.txt(ctx, 'twelve you can make from it, for free', 470, 40,
        { align: 'center', size: 12.5, w: 700, fill: P.a });
      for (var i = 0; i < 12; i++) {
        var gx = 250 + (i % 6) * 78, gy = 54 + Math.floor(i / 6) * 66;
        A.rr(ctx, gx, gy, 70, 58, 8); ctx.fillStyle = P.sunk; ctx.fill();
        ctx.strokeStyle = P.lineSoft; ctx.stroke();
        var ph = t * .5 + i * 1.7;
        var rot = Math.sin(ph) * .38, warp = Math.cos(ph * .8) * .22, sc = .78 + Math.sin(ph * .6) * .16;
        ctx.save(); ctx.beginPath(); A.rr(ctx, gx, gy, 70, 58, 8); ctx.clip();
        letterA(gx + 35, gy + 29, sc, rot, warp, P, P.a);
        if (i % 4 === 3) {                                     /* speckle noise */
          for (var k = 0; k < 22; k++) {
            var rx = gx + ((k * 37 + i * 13) % 66) + 2, ry = gy + ((k * 53 + i * 29) % 54) + 2;
            A.dot(ctx, rx, ry, 1.3, P.faint);
          }
        }
        ctx.restore();
      }
      A.txt(ctx, 'rotate · stretch · shear · add noise — the label stays "A" through all of it',
        250, 208, { size: 12, fill: P.faint });
      A.txt(ctx, 'The distortion must be one that happens in REAL data. Random pixel noise on clean',
        40, 250, { size: 12, fill: P.soft });
      A.txt(ctx, 'scanned documents teaches your model to handle a problem it will never meet.',
        40, 268, { size: 12, fill: P.soft });
      A.txt(ctx, 'For speech: add café noise, car noise, a bad phone line. Same idea.', 40, 290,
        { size: 12, w: 700, fill: P.a });
    }
    A.bind(c, function () { render(lt); });
    var lt = 0; A.loop(c.cv, function (t) { lt = t; render(t); });
  });

  /* ============================================================
     13. Transfer learning
     ============================================================ */
  A.def('transfer', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var phase = ((t * .3) % 2) < 1 ? 0 : 1;
      A.txt(ctx, phase === 0 ? 'STEP 1 — supervised pre-training' : 'STEP 2 — fine-tuning',
        380, 34, { align: 'center', size: 15, w: 700, fill: phase === 0 ? P.b : P.a });
      A.txt(ctx, phase === 0 ? 'someone else trains on a million photos of 1000 everyday objects'
        : 'you keep their layers, swap the last one, and train on your 50 X-rays',
        380, 56, { align: 'center', size: 12, fill: P.faint });
      var sizes = [5, 4, 4, 3], cols = sizes.map(function (n, i) { return A.col(150 + i * 130, n, 110, 250, 16); });
      var out = A.col(670, phase === 0 ? 4 : 2, phase === 0 ? 110 : 150, phase === 0 ? 250 : 210, 16);
      var all = cols.concat([out]);
      var li, i, j;
      for (li = 1; li < all.length; li++)
        for (i = 0; i < all[li - 1].length; i++)
          for (j = 0; j < all[li].length; j++) {
            var isLast = li === all.length - 1;
            A.link(ctx, all[li - 1][i], all[li][j],
              isLast ? (phase === 1 ? P.a : P.b) : P.line, isLast ? 1.6 : .8, isLast ? .8 : .3);
          }
      for (li = 0; li < cols.length; li++)
        for (j = 0; j < cols[li].length; j++)
          A.neuron(ctx, cols[li][j], .7, P, null, null, phase === 1 ? P.faint : P.b);
      for (j = 0; j < out.length; j++)
        A.neuron(ctx, out[j], .8, P, null, null, phase === 1 ? P.a : P.b);
      if (phase === 1) {
        ctx.save(); ctx.setLineDash([5, 4]); ctx.strokeStyle = P.faint; ctx.lineWidth = 1.8;
        A.rr(ctx, 120, 90, 470, 180, 12); ctx.stroke(); ctx.restore();
        A.txt(ctx, '🔒 frozen (or gently fine-tuned)', 355, 84, { align: 'center', size: 12, w: 700, fill: P.faint });
        ctx.save(); ctx.setLineDash([5, 4]); ctx.strokeStyle = P.a; ctx.lineWidth = 2.2;
        A.rr(ctx, 638, 130, 64, 100, 12); ctx.stroke(); ctx.restore();
        A.txt(ctx, 'NEW', 670, 122, { align: 'center', size: 12, w: 700, fill: P.a });
      }
      A.txt(ctx, phase === 0 ? '1000 outputs: cat, car, chair…' : '2 outputs: tumour / no tumour',
        670, 282, { align: 'center', size: 11.5, fill: phase === 0 ? P.b : P.a });
      A.txt(ctx, 'Edges and shapes are edges and shapes whether the picture is a cat or a chest X-ray.',
        60, 306, { size: 12.5, w: 700, fill: P.soft });
      A.txt(ctx, 'That is why the borrowed layers transfer — but only if the INPUT TYPE matches. Image → image, audio → audio.',
        60, 324, { size: 11.5, fill: P.faint });
    }
    A.bind(c, function () { render(lt); });
    var lt = 0; A.loop(c.cv, function (t) { lt = t; render(t); });
  });

  /* ============================================================
     14. The full cycle of an ML project
     ============================================================ */
  A.def('fullcycle', function (root) {
    var c = A.canvas(root, 760, 300), ctx = c.ctx;
    var stages = [
      { t: 'scope the project', s: 'what problem, and is ML even right?' },
      { t: 'collect the data', s: 'and label it, which costs more than you think' },
      { t: 'train the model', s: 'error analysis → back to data (a lot)' },
      { t: 'deploy in production', s: 'monitor, maintain, retrain' }
    ];
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var cur = Math.floor((t * .4) % 4);
      stages.forEach(function (s, i) {
        var x = 40 + i * 180, on = i === cur;
        A.rr(ctx, x, 80, 150, 78, 10);
        ctx.fillStyle = on ? P.aS : P.sunk; ctx.fill();
        ctx.strokeStyle = on ? P.a : P.lineSoft; ctx.lineWidth = on ? 2.2 : 1.2; ctx.stroke();
        A.txt(ctx, s.t, x + 75, 108, { align: 'center', size: 12.5, w: 700, fill: on ? P.a : P.soft });
        var words = s.s.split(' '), line = '', ln = 0;
        words.forEach(function (w) {
          if ((line + w).length > 22) { A.txt(ctx, line, x + 75, 126 + ln * 13, { align: 'center', size: 10, fill: P.faint }); line = w + ' '; ln++; }
          else line += w + ' ';
        });
        A.txt(ctx, line, x + 75, 126 + ln * 13, { align: 'center', size: 10, fill: P.faint });
        if (i < 3) A.arrow(ctx, x + 152, 119, x + 176, 119, cur > i ? P.a : P.line, 2);
      });
      /* the back-arrows nobody warns you about */
      ctx.save(); ctx.strokeStyle = P.p; ctx.lineWidth = 1.8; ctx.setLineDash([5, 4]);
      ctx.beginPath(); ctx.moveTo(475, 76); ctx.bezierCurveTo(430, 30, 300, 30, 260, 76); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(655, 164); ctx.bezierCurveTo(600, 218, 300, 218, 260, 172); ctx.stroke();
      ctx.restore();
      A.txt(ctx, 'need more / better data', 368, 24, { align: 'center', size: 11, w: 700, fill: P.p });
      A.txt(ctx, 'production data looks different from your test set', 450, 234,
        { align: 'center', size: 11, w: 700, fill: P.p });
      A.txt(ctx, 'The arrows that go BACKWARDS are the ones that eat your quarter.', 40, 268,
        { size: 12.5, w: 700, fill: P.soft });
      A.txt(ctx, 'Deployment is not the end: models decay as the world drifts away from the data they were trained on.',
        40, 288, { size: 11.5, fill: P.faint });
    }
    A.bind(c, function () { render(lt); });
    var lt = 0; A.loop(c.cv, function (t) { lt = t; render(t); });
  });

  /* ============================================================
     15. Fairness — the average hides the problem
     ============================================================ */
  A.def('fairness', function (root) {
    var c = A.canvas(root, 760, 300), ctx = c.ctx;
    var split = false;
    var bar = A.ctrls(root);
    A.toggle(bar, 'break it down by group', function (v) { split = v; render(); }, false);
    var groups = [['group A', 96, 0.62], ['group B', 94, 0.20], ['group C', 71, 0.12], ['group D', 63, 0.06]];
    function render() {
      var P = A.pal(); c.clear(P.panel);
      if (!split) {
        A.txt(ctx, 'overall accuracy', 380, 70, { align: 'center', size: 13, w: 700, fill: P.soft });
        A.txt(ctx, '92.4%', 380, 136, { align: 'center', size: 56, w: 700, fill: P.g });
        A.txt(ctx, 'Ship it? 🎉', 380, 176, { align: 'center', size: 14, fill: P.faint });
        A.txt(ctx, 'One number over the whole test set. Everything looks fine.', 380, 236,
          { align: 'center', size: 12.5, fill: P.soft });
        A.txt(ctx, 'Now press the button.', 380, 258, { align: 'center', size: 12.5, w: 700, fill: P.a });
      } else {
        A.txt(ctx, 'the same model, scored separately per group', 380, 42,
          { align: 'center', size: 13, w: 700, fill: P.soft });
        groups.forEach(function (g, i) {
          var y = 66 + i * 46;
          var bad = g[1] < 80;
          A.txt(ctx, g[0], 150, y + 22, { align: 'right', size: 12.5, w: 700, fill: bad ? P.r : P.soft });
          A.txt(ctx, '(' + Math.round(g[2] * 100) + '% of data)', 150, y + 36,
            { align: 'right', size: 10, fill: P.faint });
          A.rr(ctx, 165, y, 460, 30, 5); ctx.fillStyle = P.sunk; ctx.fill();
          A.rr(ctx, 165, y, 460 * g[1] / 100, 30, 5);
          ctx.fillStyle = bad ? P.r : P.g; ctx.globalAlpha = .82; ctx.fill(); ctx.globalAlpha = 1;
          A.txt(ctx, g[1] + '%', 636, y + 21, { size: 13, mono: true, w: 700, fill: bad ? P.r : P.ink });
        });
        A.line(ctx, 165 + 460 * .924, 60, 165 + 460 * .924, 252, P.faint, 1.6, [4, 3]);
        A.txt(ctx, 'the 92.4% average', 165 + 460 * .924 + 6, 268, { size: 11, fill: P.faint });
        A.txt(ctx, 'Groups C and D are 30 points worse — and they are small, so they barely move the average.',
          40, 282, { size: 12.5, w: 700, fill: P.r });
      }
    }
    A.bind(c, render); render();
  });

  /* ============================================================
     16. Confusion matrix, precision and recall
     ============================================================ */
  A.def('confusion', function (root) {
    var c = A.canvas(root, 760, 340), ctx = c.ctx;
    var th = 0.5;
    var bar = A.ctrls(root), ro = A.readout(root);
    A.slider(bar, { label: 'threshold', min: .02, max: .98, step: .01, value: th,
      on: function (v) { th = v; render(); } });
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var r = confuse(th);
      var x0 = 190, y0 = 84, cw = 130, ch = 74;
      A.txt(ctx, 'actual class', x0 + cw, 44, { align: 'center', size: 12, w: 700, fill: P.faint });
      A.txt(ctx, '1  (rare disease)', x0 + cw / 2, 66, { align: 'center', size: 11.5, fill: P.faint });
      A.txt(ctx, '0  (healthy)', x0 + cw * 1.5, 66, { align: 'center', size: 11.5, fill: P.faint });
      ctx.save(); ctx.translate(x0 - 84, y0 + ch); ctx.rotate(-Math.PI / 2);
      A.txt(ctx, 'predicted', 0, 0, { align: 'center', size: 12, w: 700, fill: P.faint }); ctx.restore();
      A.txt(ctx, 'predicted 1', x0 - 10, y0 + 42, { align: 'right', size: 11.5, fill: P.faint });
      A.txt(ctx, 'predicted 0', x0 - 10, y0 + ch + 42, { align: 'right', size: 11.5, fill: P.faint });
      var cells = [
        [0, 0, 'true pos', r.tp, P.g], [1, 0, 'false pos', r.fp, P.r],
        [0, 1, 'false neg', r.fn, P.r], [1, 1, 'true neg', r.tn, P.g]
      ];
      cells.forEach(function (cl) {
        var x = x0 + cl[0] * cw, y = y0 + cl[1] * ch;
        A.rr(ctx, x, y, cw - 4, ch - 4, 8);
        ctx.fillStyle = cl[4] === P.g ? P.gS : P.rS; ctx.fill();
        ctx.strokeStyle = cl[4]; ctx.lineWidth = 1.6; ctx.stroke();
        A.txt(ctx, cl[2], x + cw / 2 - 2, y + 22, { align: 'center', size: 11, fill: cl[4] });
        A.txt(ctx, String(cl[3]), x + cw / 2 - 2, y + 52, { align: 'center', size: 24, mono: true, w: 700, fill: cl[4] });
      });
      /* metrics */
      var mx = 490;
      [['precision', r.prec, 'of those we FLAGGED, how many really had it?', 'TP / (TP + FP)'],
       ['recall', r.rec, 'of those who really had it, how many did we CATCH?', 'TP / (TP + FN)'],
       ['F1 score', r.f1, 'a single number that punishes a bad half', '2PR / (P + R)'],
       ['accuracy', r.acc, 'the misleading one — see below', '(TP + TN) / all']
      ].forEach(function (m, i) {
        var y = 76 + i * 56;
        A.txt(ctx, m[0], mx, y, { size: 12.5, w: 700, fill: i === 3 ? P.faint : P.a });
        A.txt(ctx, m[3], mx + 190, y, { align: 'right', size: 10, mono: true, fill: P.faint });
        A.rr(ctx, mx, y + 6, 190, 14, 4); ctx.fillStyle = P.sunk; ctx.fill();
        A.rr(ctx, mx, y + 6, Math.max(2, 190 * m[1]), 14, 4);
        ctx.fillStyle = i === 3 ? P.faint : P.a; ctx.globalAlpha = .8; ctx.fill(); ctx.globalAlpha = 1;
        A.txt(ctx, (m[1] * 100).toFixed(1) + '%', mx + 190, y + 36, { align: 'right', size: 12, mono: true, w: 700, fill: P.ink });
        A.txt(ctx, m[2], mx, y + 36, { size: 10.5, fill: P.faint });
      });
      A.txt(ctx, 'Only 5% of these 400 patients are actually ill. A model that always says "healthy"', 40, 268,
        { size: 12, fill: P.soft });
      A.txt(ctx, 'scores 95% accuracy — and catches nobody. Precision and recall refuse to be fooled like that.',
        40, 286, { size: 12, w: 700, fill: P.a });
      A.txt(ctx, 'threshold = ' + th.toFixed(2), 40, 320, { size: 13, mono: true, w: 700, fill: P.soft });
      ro.set('Raise the threshold → fewer flags → <b>precision up, recall down</b> (you only shout when very sure).' +
        '\nLower it → more flags → <b>recall up, precision down</b> (you catch more, and cry wolf more).');
    }
    A.bind(c, render); render();
  });

  /* ============================================================
     17. The precision / recall trade-off curve
     ============================================================ */
  A.def('prcurve', function (root) {
    var c = A.canvas(root, 760, 340), ctx = c.ctx;
    var th = 0.5;
    var bar = A.ctrls(root), ro = A.readout(root);
    A.slider(bar, { label: 'threshold', min: .02, max: .98, step: .01, value: th,
      on: function (v) { th = v; render(); } });
    var curve = (function () {
      var a = [];
      for (var t = .02; t <= .985; t += .01) { var r = confuse(t); a.push({ t: t, p: r.prec, r: r.rec, f: r.f1 }); }
      return a;
    })();
    var bestF = curve.reduce(function (a, b) { return b.f > a.f ? b : a; }, curve[0]);
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var box = { x: 80, y: 34, w: 330, h: 230 };
      var S = A.axes(ctx, box, [0, 1], [0, 1], {
        xticks: 5, yticks: 5, xfmt: function (v) { return v.toFixed(1); },
        yfmt: function (v) { return v.toFixed(1); }, xlab: 'recall — how many we caught', ylab: 'precision'
      });
      ctx.save(); ctx.strokeStyle = P.a; ctx.lineWidth = 2.6; ctx.beginPath();
      curve.forEach(function (pt, i) {
        var px = S.X(pt.r), py = S.Y(pt.p);
        i === 0 ? ctx.moveTo(px, py) : ctx.lineTo(px, py);
      });
      ctx.stroke(); ctx.restore();
      var cur = confuse(th);
      A.dot(ctx, S.X(cur.r), S.Y(cur.p), 7, P.b);
      A.dot(ctx, S.X(bestF.r), S.Y(bestF.p), 5, P.g);
      A.txt(ctx, 'best F1', S.X(bestF.r) + 8, S.Y(bestF.p) + 14, { size: 11, w: 700, fill: P.g });
      A.txt(ctx, 'high threshold', S.X(.06), S.Y(.96), { size: 11, fill: P.faint });
      A.txt(ctx, 'low threshold', S.X(.62), S.Y(.08), { size: 11, fill: P.faint });
      /* threshold ladder */
      var mx = 460;
      A.txt(ctx, 'moving the threshold', mx, 50, { size: 13, w: 700, fill: P.soft });
      [[.9, 'only flag if almost certain'], [.5, 'the default'], [.15, 'flag anything suspicious']]
        .forEach(function (row, i) {
          var r = confuse(row[0]), y = 74 + i * 66, on = Math.abs(th - row[0]) < .06;
          A.rr(ctx, mx, y, 250, 56, 8);
          ctx.fillStyle = on ? P.aS : P.sunk; ctx.fill();
          ctx.strokeStyle = on ? P.a : P.lineSoft; ctx.lineWidth = on ? 2 : 1; ctx.stroke();
          A.txt(ctx, 'threshold ' + row[0].toFixed(2), mx + 12, y + 20, { size: 12, w: 700, fill: on ? P.a : P.soft });
          A.txt(ctx, row[1], mx + 12, y + 35, { size: 10.5, fill: P.faint });
          A.txt(ctx, 'P ' + (r.prec * 100).toFixed(0) + '%  R ' + (r.rec * 100).toFixed(0) + '%',
            mx + 238, y + 26, { align: 'right', size: 12.5, mono: true, w: 700, fill: on ? P.a : P.soft });
        });
      A.txt(ctx, 'now: precision ' + (cur.prec * 100).toFixed(1) + '%   recall ' + (cur.rec * 100).toFixed(1) +
        '%   F1 ' + (cur.f1 * 100).toFixed(1) + '%', 80, 296, { size: 13, mono: true, w: 700, fill: P.b });
      A.txt(ctx, 'F1 is the harmonic mean: it is close to the SMALLER of the two, so 100% recall with 5% precision scores badly.',
        80, 320, { size: 11.5, fill: P.faint });
      ro.set('There is no “correct” threshold — it depends on what a mistake costs.' +
        '\nMissing a treatable cancer is far worse than an extra test → favour <b>recall</b>. ' +
        'Wrongly accusing a customer of fraud is expensive → favour <b>precision</b>.');
    }
    A.bind(c, render); render();
  });

})();
