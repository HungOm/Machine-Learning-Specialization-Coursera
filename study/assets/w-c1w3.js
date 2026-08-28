/* Widgets for Course 1 / Week 3 — classification, logistic regression, regularisation */
(function () {
  'use strict';

  function rnd(i) { var v = Math.sin(i * 21.71 + 5.13) * 31417.77; return v - Math.floor(v); }

  /* ============================================================
     1. Why linear regression fails at classification
     ============================================================ */
  A.def('classmotivation', function (root) {
    var c = A.canvas(root, 760, 340), ctx = c.ctx;
    var outlier = false;
    var bar = A.ctrls(root), ro = A.readout(root);
    A.toggle(bar, 'add one very large tumour (still malignant)', function (v) { outlier = v; render(); }, false);
    var BASE = [[0.5,0],[0.8,0],[1.1,0],[1.5,0],[1.9,0],[2.6,1],[3.0,1],[3.4,1],[3.9,1],[4.3,1]];
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var D = BASE.map(function (p) { return { x: p[0], y: p[1] }; });
      if (outlier) D.push({ x: 9.4, y: 1 });
      var sx=0, sy=0, sxx=0, sxy=0;
      D.forEach(function (p) { sx+=p.x; sy+=p.y; sxx+=p.x*p.x; sxy+=p.x*p.y; });
      var m = D.length;
      var w = (m*sxy - sx*sy) / (m*sxx - sx*sx), b = (sy - w*sx)/m;
      var thresh = (0.5 - b) / w;
      var box = { x: 80, y: 56, w: 600, h: 190 };
      var S = A.axes(ctx, box, [0, 10.4], [-0.4, 1.5], {
        xticks: 5, yticks: 3, xfmt: function (v) { return v.toFixed(0); },
        yfmt: function (v) { return v.toFixed(1); },
        xlab: 'tumour size (cm)', ylab: 'malignant?'
      });
      A.plot(ctx, S, [0, 10.4], function (x) { return w * x + b; }, P.a, 2.6);
      A.line(ctx, box.x, S.Y(0.5), box.x + box.w, S.Y(0.5), P.faint, 1.4, [5, 4]);
      A.txt(ctx, 'threshold 0.5', box.x + 8, S.Y(0.5) - 8, { size: 10.5, fill: P.faint });
      A.line(ctx, S.X(thresh), box.y, S.X(thresh), box.y + box.h, P.g, 2.2, [4, 3]);
      A.txt(ctx, 'boundary', S.X(thresh) + 8, box.y + 16, { size: 11, w: 700, fill: P.g });
      D.forEach(function (p, i) {
        var isOut = outlier && i === D.length - 1;
        A.dot(ctx, S.X(p.x), S.Y(p.y), isOut ? 8 : 5.5, p.y ? P.r : P.b);
        if (isOut) {
          ctx.save(); ctx.strokeStyle = P.r; ctx.lineWidth = 2; ctx.setLineDash([3, 3]);
          ctx.beginPath(); ctx.arc(S.X(p.x), S.Y(p.y), 13, 0, 6.2832); ctx.stroke(); ctx.restore();
        }
      });
      /* count the mistakes */
      var wrong = 0;
      D.forEach(function (p) { if (((w * p.x + b) >= .5 ? 1 : 0) !== p.y) wrong++; });
      A.txt(ctx, 'boundary moved to ' + thresh.toFixed(2) + ' cm   ·   ' + wrong + ' example' +
        (wrong === 1 ? '' : 's') + ' now misclassified', 80, 278,
        { size: 13, mono: true, w: 700, fill: wrong ? P.r : P.g });
      A.txt(ctx, outlier
        ? 'One extra point — which everybody would agree is malignant — dragged the line down and moved the boundary.'
        : 'Looks fine. Now press the button and add one large tumour on the right.',
        80, 304, { size: 12, w: 700, fill: outlier ? P.r : P.soft });
      A.txt(ctx, outlier
        ? 'Nothing about the underlying problem changed. Linear regression is simply the wrong shape of model for this.'
        : 'It is still obviously malignant, so a good model should not change its mind about anything.',
        80, 326, { size: 11.5, fill: P.faint });
      ro.set('Two problems with using linear regression for classification:' +
        '\n<b>1.</b> Its output is unbounded — it will happily predict −0.4 or 1.8, which cannot be read ' +
        'as “is it malignant?”.' +
        '\n<b>2.</b> A far-away example that is <em>clearly</em> in one class still drags the fitted line, ' +
        'and moves the decision boundary. That is exactly backwards.');
    }
    A.bind(c, render); render();
  });

  /* ============================================================
     2. Logistic regression and the sigmoid
     ============================================================ */
  A.def('logistic', function (root) {
    var c = A.canvas(root, 760, 340), ctx = c.ctx;
    var w = 1.6, b = -4.2;
    var bar = A.ctrls(root), ro = A.readout(root);
    A.slider(bar, { label: 'w', min: 0.2, max: 5, step: .05, value: w,
      fmt: function (v) { return v.toFixed(2); }, on: function (v) { w = v; render(); } });
    A.slider(bar, { label: 'b', min: -12, max: 2, step: .1, value: b,
      fmt: function (v) { return v.toFixed(1); }, on: function (v) { b = v; render(); } });
    var D = [[0.5,0],[0.8,0],[1.1,0],[1.5,0],[1.9,0],[2.6,1],[3.0,1],[3.4,1],[3.9,1],[4.3,1]];
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      /* left: the z number line */
      var b1 = { x: 60, y: 56, w: 260, h: 190 };
      var S1 = A.axes(ctx, b1, [-6, 6], [-0.1, 1.1], {
        xticks: 4, yticks: 3, xfmt: function (v) { return v.toFixed(0); },
        yfmt: function (v) { return v.toFixed(1); }, xlab: 'z', ylab: 'g(z)'
      });
      A.txt(ctx, 'the sigmoid — the squasher', b1.x + b1.w / 2, 42,
        { align: 'center', size: 12, w: 700, fill: P.soft });
      A.plot(ctx, S1, [-6, 6], A.sig, P.p, 2.8);
      A.line(ctx, b1.x, S1.Y(.5), b1.x + b1.w, S1.Y(.5), P.faint, 1.2, [4, 3]);
      var zq = Math.sin(t * .6) * 4.4;
      A.dot(ctx, S1.X(zq), S1.Y(A.sig(zq)), 6, P.a);
      A.txt(ctx, 'g(0) = 0.5', S1.X(0) + 8, S1.Y(.5) - 8, { size: 10.5, fill: P.faint });
      A.txt(ctx, 'always between 0 and 1', b1.x + b1.w / 2, b1.y + b1.h + 44,
        { align: 'center', size: 11, fill: P.faint });
      /* right: applied to the tumour data */
      var b2 = { x: 410, y: 56, w: 300, h: 190 };
      var S2 = A.axes(ctx, b2, [0, 5.4], [-0.1, 1.1], {
        xticks: 4, yticks: 3, xfmt: function (v) { return v.toFixed(0); },
        yfmt: function (v) { return v.toFixed(1); }, xlab: 'tumour size', ylab: 'P(y = 1)'
      });
      A.txt(ctx, 'the model  f(x) = g(wx + b)', b2.x + b2.w / 2, 42,
        { align: 'center', size: 12, w: 700, fill: P.soft });
      A.plot(ctx, S2, [0, 5.4], function (x) { return A.sig(w * x + b); }, P.a, 2.8);
      A.line(ctx, b2.x, S2.Y(.5), b2.x + b2.w, S2.Y(.5), P.faint, 1.2, [4, 3]);
      D.forEach(function (p) { A.dot(ctx, S2.X(p[0]), S2.Y(p[1]), 5, p[1] ? P.r : P.b); });
      var bx = -b / w;
      if (bx > 0 && bx < 5.4) {
        A.line(ctx, S2.X(bx), b2.y, S2.X(bx), b2.y + b2.h, P.g, 2, [4, 3]);
        A.txt(ctx, 'boundary ' + bx.toFixed(2), S2.X(bx) + 6, b2.y + 16, { size: 10.5, w: 700, fill: P.g });
      }
      var qx = 3.0, pq = A.sig(w * qx + b);
      A.dot(ctx, S2.X(qx), S2.Y(pq), 7, P.a);
      A.txt(ctx, 'a 3 cm tumour → P(malignant) = ' + (pq * 100).toFixed(0) + '%', 60, 282,
        { size: 13.5, mono: true, w: 700, fill: P.a });
      A.txt(ctx, 'The output is now a PROBABILITY, so it can never be −0.4 or 1.8.', 60, 306,
        { size: 12, fill: P.soft });
      A.txt(ctx, 'And a tumour far to the right barely moves the curve — sigmoid has already saturated there.',
        60, 326, { size: 12, w: 700, fill: P.g });
      ro.set('z = w·x + b  (a number, anything at all)   →   f(x) = g(z) = <b>1 / (1 + e<sup>−z</sup>)</b>  (a probability)' +
        '\nRead it as P(y = 1 | x; w, b): “the chance that y is 1, given this x and these parameters”.' +
        '\nThe name is historical — it is called logistic <em>regression</em> and it is a classification algorithm.');
    }
    A.autoplay(root, c, render);
  });

  /* ============================================================
     3. The decision boundary
     ============================================================ */
  A.def('decisionboundary', function (root) {
    var c = A.canvas(root, 760, 340), ctx = c.ctx;
    var mode = 0;
    var bar = A.ctrls(root), ro = A.readout(root);
    ['linear features', 'polynomial features'].forEach(function (n, i) {
      A.button(bar, n, function () { mode = i; sync(); render(); });
    });
    function sync() { bar.querySelectorAll('button').forEach(function (b, i) { b.classList.toggle('primary', i === mode); }); }
    var LIN = [], CIRC = [];
    (function () {
      for (var i = 0; i < 40; i++) {
        var x = -2.6 + rnd(i * 3 + 1) * 5.2, y = -2.6 + rnd(i * 3 + 2) * 5.2;
        LIN.push({ x: x, y: y, c: (x + y > 0.2) ? 1 : 0 });
        CIRC.push({ x: x, y: y, c: (x * x + y * y < 2.4) ? 0 : 1 });
      }
    })();
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var D = mode === 0 ? LIN : CIRC;
      var box = { x: 90, y: 44, w: 250, h: 230 };
      var S = A.axes(ctx, box, [-3, 3], [-3, 3], { xticks: 4, yticks: 4, xlab: 'x₁', ylab: 'x₂' });
      function z(x, y) { return mode === 0 ? (x + y - 0.2) * 2.2 : (2.4 - x * x - y * y) * -1.6; }
      ctx.save(); ctx.globalAlpha = .12;
      for (var gx = 0; gx <= 26; gx++) for (var gy = 0; gy <= 24; gy++) {
        var px = -3 + 6 * gx / 26, py = -3 + 6 * gy / 24;
        ctx.fillStyle = z(px, py) > 0 ? P.r : P.b;
        ctx.fillRect(S.X(px) - 6, S.Y(py) - 6, 12, 12);
      }
      ctx.restore();
      if (mode === 0) {
        A.line(ctx, S.X(-3), S.Y(3.2), S.X(3), S.Y(-2.8), P.a, 2.8);
      } else {
        ctx.save(); ctx.strokeStyle = P.a; ctx.lineWidth = 2.8; ctx.beginPath();
        for (var th = 0; th <= 6.3; th += .04) {
          var r = Math.sqrt(2.4);
          var qx = S.X(r * Math.cos(th)), qy = S.Y(r * Math.sin(th));
          th === 0 ? ctx.moveTo(qx, qy) : ctx.lineTo(qx, qy);
        }
        ctx.closePath(); ctx.stroke(); ctx.restore();
      }
      D.forEach(function (p) { A.dot(ctx, S.X(p.x), S.Y(p.y), 4.6, p.c ? P.r : P.b); });
      /* the maths */
      A.txt(ctx, 'the boundary is where z = 0', 400, 66, { size: 13, w: 700, fill: P.soft });
      A.txt(ctx, 'because g(0) = 0.5 exactly', 400, 86, { size: 11, fill: P.faint });
      A.txt(ctx, mode === 0 ? 'z = w₁x₁ + w₂x₂ + b' : 'z = w₁x₁² + w₂x₂² + b',
        400, 122, { size: 15, mono: true, w: 700, fill: P.a });
      A.txt(ctx, mode === 0 ? 'z = 0  →  a straight LINE' : 'z = 0  →  a CIRCLE',
        400, 150, { size: 13, mono: true, w: 700, fill: P.g });
      [['f ≥ 0.5', 'z ≥ 0', 'predict ŷ = 1', P.r],
       ['f < 0.5', 'z < 0', 'predict ŷ = 0', P.b]
      ].forEach(function (r, i) {
        var y = 184 + i * 44;
        A.rr(ctx, 400, y, 300, 36, 7);
        ctx.fillStyle = r[3] === P.r ? P.rS : P.bS; ctx.fill();
        ctx.strokeStyle = r[3]; ctx.lineWidth = 1.4; ctx.stroke();
        A.txt(ctx, r[0] + '   ↔   ' + r[1] + '   ⟹   ' + r[2], 414, y + 23,
          { size: 12, mono: true, w: 700, fill: r[3] });
      });
      A.txt(ctx, mode === 0
        ? 'With only x₁ and x₂ available, the boundary can only ever be a straight line.'
        : 'Feed it x₁² and x₂² as features and the boundary can be a circle — or, with more terms, almost any shape.',
        90, 302, { size: 12, w: 700, fill: P.soft });
      A.txt(ctx, 'The boundary is a property of the FEATURES you supply, not of logistic regression itself.',
        90, 324, { size: 11.5, fill: P.faint });
      ro.set('The decision boundary is the set of x where <b>z = w·x + b = 0</b>.' +
        '\nThe model is always “linear in z”. What that looks like in x-space depends entirely on which ' +
        'features you gave it — the same feature-engineering idea as Week 2, doing much more visible work.');
    }
    sync(); A.bind(c, render); render();
  });

  /* ============================================================
     4. Why squared error does not work here
     ============================================================ */
  A.def('logcost', function (root) {
    var c = A.canvas(root, 760, 372), ctx = c.ctx;
    var bar = A.ctrls(root), ro = A.readout(root);
    var X = [0, 1, 2, 3, 4, 5], Y = [0, 0, 0, 1, 1, 1];
    var w0 = -5, b0 = 10, N = 300;

    /* gradient descent, actually run, on both cost functions */
    function run(kind) {
      var w = w0, b = b0, acc = [], a = 1;
      for (var it = 0; it <= N; it++) {
        var gw = 0, gb = 0, right = 0;
        for (var i = 0; i < X.length; i++) {
          var z = w * X[i] + b, f = A.sig(z), e = f - Y[i];
          /* squared error drags an extra g'(z) = f(1-f) along; log loss does not */
          var m = kind === 'sq' ? e * f * (1 - f) : e;
          gw += m * X[i]; gb += m;
          if ((f >= .5 ? 1 : 0) === Y[i]) right++;
        }
        acc.push(right / X.length);
        w -= a * gw / X.length; b -= a * gb / X.length;
      }
      return { acc: acc, w: w, b: b, end: acc[acc.length - 1] };
    }

    A.slider(bar, { label: 'start w =', min: -8, max: 8, step: .5, value: w0,
      fmt: function (v) { return v.toFixed(1); }, on: function (v) { w0 = v; render(); } });
    A.slider(bar, { label: 'start b =', min: -20, max: 20, step: 1, value: b0,
      fmt: function (v) { return v.toFixed(0); }, on: function (v) { b0 = v; render(); } });

    function render() {
      var P = A.pal(); c.clear(P.panel);
      var sq = run('sq'), lg = run('log');

      var box = { x: 62, y: 56, w: 380, h: 190 };
      var S = A.axes(ctx, box, [0, N], [0, 1.05], {
        xticks: 3, yticks: 4,
        xfmt: function (v) { return v.toFixed(0); },
        yfmt: function (v) { return v.toFixed(2); },
        xlab: 'gradient descent steps', ylab: 'accuracy'
      });
      A.plot(ctx, S, [0, N], function (x) { return sq.acc[A.clamp(Math.round(x), 0, N)]; }, P.r, 2.6);
      A.plot(ctx, S, [0, N], function (x) { return lg.acc[A.clamp(Math.round(x), 0, N)]; }, P.g, 2.6);
      A.txt(ctx, 'squared error → ' + sq.end.toFixed(2), 74, 76, { size: 12, w: 700, fill: P.r });
      A.txt(ctx, 'log loss → ' + lg.end.toFixed(2), 74, 96, { size: 12, w: 700, fill: P.g });

      var box2 = { x: 520, y: 56, w: 200, h: 190 };
      var S2 = A.axes(ctx, box2, [-8, 8], [0, .28], {
        xticks: 4, yticks: 3,
        xfmt: function (v) { return v.toFixed(0); },
        yfmt: function (v) { return v.toFixed(2); },
        xlab: 'z', ylab: 'g′(z)'
      });
      A.plot(ctx, S2, [-8, 8], function (z) { var g = A.sig(z); return g * (1 - g); }, P.r, 2.4);
      var z0 = w0 * 3 + b0, g0 = A.sig(z0) * (1 - A.sig(z0));
      A.dot(ctx, S2.X(A.clamp(z0, -8, 8)), S2.Y(g0), 5, P.a);
      A.txt(ctx, 'g′(z) at your start = ' + g0.toFixed(4), 620, 268,
        { align: 'center', size: 11, mono: true, fill: g0 < .02 ? P.r : P.soft });

      A.txt(ctx, 'Squared error multiplies every gradient by g′(z) = g(1−g), which peaks at 0.25 and',
        40, 296, { size: 12.5, fill: P.soft });
      A.txt(ctx, 'collapses to nearly nothing once the sigmoid saturates — exactly where a badly placed',
        40, 316, { size: 12.5, fill: P.soft });
      A.txt(ctx, 'model sits. Log loss is built so that factor cancels, so its gradient stays alive.',
        40, 336, { size: 12.5, w: 700, fill: P.a });
      A.txt(ctx, 'Drag to a confident-but-wrong start and watch the red line flatline.',
        40, 358, { size: 11.5, fill: P.faint });

      ro.set('From w = ' + w0.toFixed(1) + ', b = ' + b0.toFixed(0) + ' after ' + N + ' steps: ' +
        '<b>squared error</b> ends at w = ' + sq.w.toFixed(2) + ', accuracy <b>' + sq.end.toFixed(2) + '</b>. ' +
        '<b>Log loss</b> ends at w = ' + lg.w.toFixed(2) + ', accuracy <b>' + lg.end.toFixed(2) + '</b>.' +
        '\nBoth run the identical algorithm on the identical data. Only the cost function differs.' +
        '\nThis is a real optimisation, run in your browser — not a drawing of one.');
    }
    A.bind(c, render);
    render();
  });

  /* ============================================================
     5. The logistic loss
     ============================================================ */
  A.def('logloss', function (root) {
    var c = A.canvas(root, 760, 340), ctx = c.ctx;
    var f = 0.7, y = 1;
    var bar = A.ctrls(root), ro = A.readout(root);
    A.slider(bar, { label: 'the model predicts f =', min: .01, max: .99, step: .01, value: f,
      on: function (v) { f = v; render(); } });
    A.button(bar, 'truth: y = 1', function () { y = 1; sync(); render(); });
    A.button(bar, 'truth: y = 0', function () { y = 0; sync(); render(); });
    function sync() {
      var bs = bar.querySelectorAll('button');
      bs[0].classList.toggle('primary', y === 1); bs[1].classList.toggle('primary', y === 0);
    }
    function loss(fv) { return y === 1 ? -Math.log(fv) : -Math.log(1 - fv); }
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var box = { x: 80, y: 46, w: 590, h: 200 };
      var S = A.axes(ctx, box, [0, 1], [0, 5], {
        xticks: 5, yticks: 5, xfmt: function (v) { return v.toFixed(1); },
        yfmt: function (v) { return v.toFixed(0); },
        xlab: 'f(x) — the predicted probability', ylab: 'loss'
      });
      A.plot(ctx, S, [.005, .995], function (v) { return Math.min(5, -Math.log(v)); },
        y === 1 ? P.g : P.lineSoft, y === 1 ? 2.8 : 1.6);
      A.plot(ctx, S, [.005, .995], function (v) { return Math.min(5, -Math.log(1 - v)); },
        y === 0 ? P.r : P.lineSoft, y === 0 ? 2.8 : 1.6);
      A.txt(ctx, 'if y = 1:  −log(f)', S.X(.10), S.Y(4.2), { size: 12, w: 700, fill: y === 1 ? P.g : P.faint });
      A.txt(ctx, 'if y = 0:  −log(1 − f)', S.X(.60), S.Y(4.2), { size: 12, w: 700, fill: y === 0 ? P.r : P.faint });
      var Lv = Math.min(loss(f), 5);
      A.line(ctx, S.X(f), box.y, S.X(f), S.Y(0), P.a, 1.4, [4, 3]);
      A.dot(ctx, S.X(f), S.Y(Lv), 7, P.a);
      A.txt(ctx, 'loss = ' + loss(f).toFixed(3), S.X(f) + 12, S.Y(Lv) - 10,
        { size: 13.5, mono: true, w: 700, fill: P.a });
      var verdict = (y === 1 && f > .8) || (y === 0 && f < .2) ? ['confident and right — almost no penalty', P.g]
        : (y === 1 && f < .2) || (y === 0 && f > .8) ? ['confident and WRONG — the penalty explodes', P.r]
        : ['hedging — a moderate penalty either way', P.m];
      A.txt(ctx, verdict[0], 80, 276, { size: 14, w: 700, fill: verdict[1] });
      A.txt(ctx, 'The loss is built so that being sure of something false costs you enormously. Drag f towards',
        80, 300, { size: 11.5, fill: P.soft });
      A.txt(ctx, '0.01 with y = 1 and watch it climb — as f → 0 the loss goes to infinity.', 80, 320,
        { size: 11.5, fill: P.soft });
      ro.set('L(f, y) = <b>−log(f)</b> if y = 1,   <b>−log(1 − f)</b> if y = 0.' +
        '\nWhy a logarithm? Because it produces a <b>convex</b> overall cost, and because it is the ' +
        'negative log-likelihood — the choice of w and b that makes the observed data most probable.' +
        '\nThe cost J is the average of this loss over all m examples.');
    }
    sync(); A.bind(c, render); render();
  });

  /* ============================================================
     6. The simplified (combined) cost
     ============================================================ */
  A.def('simplifiedcost', function (root) {
    var c = A.canvas(root, 760, 320), ctx = c.ctx;
    var ro = A.readout(root);
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var y = Math.floor((t * .4) % 2);
      A.txt(ctx, 'the two-case version', 40, 44, { size: 12.5, w: 700, fill: P.soft });
      [[0, '−log(1 − f)   if y = 0'], [1, '−log(f)         if y = 1']].forEach(function (r, i) {
        var on = r[0] === y;
        A.rr(ctx, 40, 62 + i * 46, 300, 38, 7);
        ctx.fillStyle = on ? P.aS : P.sunk; ctx.fill();
        ctx.strokeStyle = on ? P.a : P.lineSoft; ctx.lineWidth = on ? 2 : 1; ctx.stroke();
        A.txt(ctx, r[1], 56, 86 + i * 46, { size: 13, mono: true, w: on ? 700 : 500,
          fill: on ? P.a : P.soft });
      });
      A.arrow(ctx, 350, 100, 396, 100, P.line, 2);
      A.txt(ctx, 'the one-line version', 420, 44, { size: 12.5, w: 700, fill: P.soft });
      A.rr(ctx, 420, 62, 300, 84, 9);
      ctx.fillStyle = P.gS; ctx.fill(); ctx.strokeStyle = P.g; ctx.lineWidth = 2; ctx.stroke();
      A.txt(ctx, 'L = −y·log(f)', 570, 92, { align: 'center', size: 14, mono: true, w: 700, fill: P.g });
      A.txt(ctx, '     − (1 − y)·log(1 − f)', 570, 118, { align: 'center', size: 14, mono: true, w: 700, fill: P.g });
      /* the cancellation */
      A.txt(ctx, 'why it works — y is only ever 0 or 1', 40, 178, { size: 12.5, w: 700, fill: P.soft });
      var lines = y === 1
        ? ['y = 1:', '  −1·log(f) − (1 − 1)·log(1 − f)', '  = −log(f) − 0·log(1 − f)', '  = −log(f)   ✓']
        : ['y = 0:', '  −0·log(f) − (1 − 0)·log(1 − f)', '  = 0 − log(1 − f)', '  = −log(1 − f)   ✓'];
      lines.forEach(function (l, i) {
        A.txt(ctx, l, 40, 202 + i * 22, { size: 12.5, mono: true,
          w: i === 3 ? 700 : 500, fill: i === 3 ? P.g : i === 0 ? P.a : P.soft });
      });
      A.txt(ctx, 'one of the two terms is always multiplied by zero', 420, 190,
        { size: 11.5, w: 700, fill: P.faint });
      A.txt(ctx, 'and quietly disappears. Nothing has changed —', 420, 210, { size: 11.5, fill: P.faint });
      A.txt(ctx, 'it is the same loss, written without an if.', 420, 230, { size: 11.5, fill: P.faint });
      A.txt(ctx, 'This is called binary cross-entropy, and it is the loss you will use for every binary',
        420, 260, { size: 11, fill: P.soft });
      A.txt(ctx, 'classifier in Course 2 as well.', 420, 278, { size: 11, w: 700, fill: P.a });
      A.txt(ctx, 'J(w, b) = (1/m) Σ L( f(x⁽ⁱ⁾), y⁽ⁱ⁾ )', 40, 300,
        { size: 14, mono: true, w: 700, fill: P.a });
      ro.set('L(f, y) = <b>−y·log(f) − (1 − y)·log(1 − f)</b>' +
        '\nNote there is no 1/2 here — that only existed in the squared-error cost to cancel the 2 from ' +
        'differentiating a square. There is no square to differentiate now.');
    }
    A.autoplay(root, c, render);
  });

  /* ============================================================
     7. Gradient descent for logistic regression
     ============================================================ */
  A.def('gdlogistic', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var ro = A.readout(root);
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var flip = ((t * .35) % 2) < 1;
      A.txt(ctx, 'the update rule', 380, 44, { align: 'center', size: 13.5, w: 700, fill: P.soft });
      A.rr(ctx, 110, 62, 540, 44, 9);
      ctx.fillStyle = P.aS; ctx.fill(); ctx.strokeStyle = P.a; ctx.lineWidth = 2; ctx.stroke();
      A.txt(ctx, 'wⱼ := wⱼ − α · (1/m) Σ ( f(x⁽ⁱ⁾) − y⁽ⁱ⁾ ) · xⱼ⁽ⁱ⁾', 380, 90,
        { align: 'center', size: 15, mono: true, w: 700, fill: P.a });
      A.txt(ctx, 'looks IDENTICAL to linear regression…', 380, 130,
        { align: 'center', size: 12.5, w: 700, fill: P.faint });
      /* the one difference */
      [[190, 'linear regression', 'f(x) = w·x + b', P.b, !flip],
       [570, 'logistic regression', 'f(x) = g(w·x + b)', P.a, flip]
      ].forEach(function (pn) {
        A.rr(ctx, pn[0] - 150, 152, 300, 76, 9);
        ctx.fillStyle = pn[4] ? (pn[3] === P.b ? P.bS : P.aS) : P.sunk; ctx.fill();
        ctx.strokeStyle = pn[4] ? pn[3] : P.lineSoft; ctx.lineWidth = pn[4] ? 2.4 : 1.2; ctx.stroke();
        A.txt(ctx, pn[1], pn[0], 178, { align: 'center', size: 12.5, w: 700, fill: pn[3] });
        A.txt(ctx, pn[2], pn[0], 208, { align: 'center', size: 16, mono: true, w: 700, fill: pn[3] });
      });
      A.txt(ctx, '…but f means something completely different. That is the whole difference.', 380, 254,
        { align: 'center', size: 13, w: 700, fill: P.g });
      A.txt(ctx, 'Everything else carries straight over: simultaneous updates, feature scaling, plotting J against',
        40, 288, { size: 11.5, fill: P.soft });
      A.txt(ctx, 'iterations, choosing α by trying a ladder of values. All of Week 1 and Week 2 still applies.',
        40, 308, { size: 11.5, fill: P.soft });
      ro.set('The derivative of the logistic cost with respect to w<sub>j</sub> comes out to exactly the ' +
        'same expression as for squared error — a genuinely surprising and convenient piece of algebra.' +
        '\nIt is not a coincidence: it is a property of pairing the sigmoid with the log loss. Pair them ' +
        'wrongly and the tidiness disappears.');
    }
    A.autoplay(root, c, render);
  });

  /* ============================================================
     8. The problem of overfitting
     ============================================================ */
  A.def('overfitting', function (root) {
    var c = A.canvas(root, 760, 340), ctx = c.ctx;
    var which = 1, task = 0;
    var bar = A.ctrls(root), ro = A.readout(root);
    ['regression', 'classification'].forEach(function (n, i) {
      A.button(bar, n, function () { task = i; sync(); render(); });
    });
    var D = [];
    (function () {
      for (var i = 0; i < 12; i++) {
        var x = .3 + i * .33;
        D.push({ x: x, y: 1.1 * Math.sqrt(x * 1.6) + .5 + (rnd(i * 7 + 3) - .5) * .42 });
      }
    })();
    function sync() { bar.querySelectorAll('button').forEach(function (b, i) { b.classList.toggle('primary', i === task); }); }
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var titles = [
        ['UNDERFIT', 'high bias', 'too simple — it does not even fit the training data', P.b],
        ['JUST RIGHT', 'generalises well', 'fits the training data, and will fit new data too', P.g],
        ['OVERFIT', 'high variance', 'passes through every point, and will fail on anything new', P.r]
      ];
      titles.forEach(function (ti, k) {
        var x0 = 30 + k * 245;
        var box = { x: x0 + 20, y: 74, w: 200, h: 150 };
        var S = A.axes(ctx, box, [0, 4.4], [0, 3.4], { xticks: 2, yticks: 2 });
        A.rr(ctx, x0, 56, 230, 186, 9);
        ctx.strokeStyle = ti[3]; ctx.lineWidth = 1.6; ctx.stroke();
        A.txt(ctx, ti[0], x0 + 115, 44, { align: 'center', size: 13, w: 700, fill: ti[3] });
        if (task === 0) {
          var f = k === 0 ? function (x) { return .55 * x + .9; }
            : k === 1 ? function (x) { return 1.1 * Math.sqrt(x * 1.6) + .5; }
            : function (x) {
                var s = 1.1 * Math.sqrt(x * 1.6) + .5;
                return s + .55 * Math.sin(x * 7.4) * Math.exp(-Math.pow((x - 2.2) / 3.4, 2));
              };
          A.plot(ctx, S, [0.05, 4.35], function (x) { return A.clamp(f(x), 0, 3.4); }, ti[3], 2.4);
          D.forEach(function (p) { A.dot(ctx, S.X(p.x), S.Y(p.y), 3.6, P.faint); });
        } else {
          for (var i = 0; i < 26; i++) {
            var px = .3 + rnd(i * 5 + 2) * 3.8, py = .3 + rnd(i * 5 + 4) * 2.8;
            var cl = (py > .55 * px + .9 + (rnd(i * 9 + 1) - .5) * .5) ? 1 : 0;
            A.dot(ctx, S.X(px), S.Y(py), 3.6, cl ? P.r : P.b);
          }
          ctx.save(); ctx.strokeStyle = ti[3]; ctx.lineWidth = 2.4; ctx.beginPath();
          for (var q = 0; q <= 60; q++) {
            var xx = .1 + q / 60 * 4.2;
            var yy = k === 0 ? .35 * xx + 1.35
              : k === 1 ? .55 * xx + .9
              : .55 * xx + .9 + .5 * Math.sin(xx * 6.2);
            var sx = S.X(xx), sy = S.Y(A.clamp(yy, 0, 3.4));
            q === 0 ? ctx.moveTo(sx, sy) : ctx.lineTo(sx, sy);
          }
          ctx.stroke(); ctx.restore();
        }
        A.txt(ctx, ti[1], x0 + 115, 258, { align: 'center', size: 11.5, w: 700, fill: ti[3] });
        var words = ti[2].split(' '), line = '', ln = 0;
        words.forEach(function (wd) {
          if ((line + wd).length > 30) {
            A.txt(ctx, line, x0 + 115, 276 + ln * 14, { align: 'center', size: 9.5, fill: P.faint });
            line = wd + ' '; ln++;
          } else line += wd + ' ';
        });
        A.txt(ctx, line, x0 + 115, 276 + ln * 14, { align: 'center', size: 9.5, fill: P.faint });
      });
      A.txt(ctx, 'Both failures look like a bad fit, and they need opposite fixes. That is why naming them matters.',
        30, 322, { size: 12, w: 700, fill: P.soft });
      ro.set('<b>Underfit / high bias</b>: the model has a strong preconception that the data cannot ' +
        'change — a straight line no matter what you show it.' +
        '\n<b>Overfit / high variance</b>: it fits the training data perfectly, so perfectly that a ' +
        'slightly different training set would produce a wildly different model.' +
        '\nCourse 2 Week 3 turns this picture into two numbers you can measure.');
    }
    sync();
    A.autoplay(root, c, render);
  });

  /* ============================================================
     9. Addressing overfitting
     ============================================================ */
  A.def('addressing', function (root) {
    var c = A.canvas(root, 760, 320), ctx = c.ctx;
    var opts = [
      ['1 · collect more data', 'the best fix when you can get it',
       'with enough examples even a flexible model cannot wiggle — there is no room left',
       'often expensive, slow, or simply impossible'],
      ['2 · use fewer features', 'feature selection',
       'fewer parameters means less capacity to memorise noise',
       'you may throw away a feature that genuinely mattered'],
      ['3 · regularisation', 'keep every feature, but shrink the weights',
       'lets you keep all the information while limiting how extreme the model can get',
       'the one to reach for first — and the subject of the rest of this week']
    ];
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var hot = Math.floor((t * .45) % 3);
      A.txt(ctx, 'three ways to stop a model memorising its training data', 40, 40,
        { size: 13, w: 700, fill: P.soft });
      opts.forEach(function (o, i) {
        var y = 58 + i * 78, on = i === hot;
        A.rr(ctx, 40, y, 680, 68, 9);
        ctx.fillStyle = on ? (i === 2 ? P.gS : P.aS) : P.sunk; ctx.fill();
        ctx.strokeStyle = on ? (i === 2 ? P.g : P.a) : P.lineSoft; ctx.lineWidth = on ? 2.2 : 1.2; ctx.stroke();
        var col = on ? (i === 2 ? P.g : P.a) : P.soft;
        A.txt(ctx, o[0], 58, y + 24, { size: 13.5, w: 700, fill: col });
        A.txt(ctx, o[1], 58, y + 42, { size: 11, fill: P.faint });
        A.txt(ctx, '+ ' + o[2], 300, y + 26, { size: 10.5, fill: on ? P.soft : P.faint });
        A.txt(ctx, '− ' + o[3], 300, y + 46, { size: 10.5, fill: P.faint });
      });
      A.txt(ctx, 'Regularisation shrinks weights towards zero without forcing them there — a soft version of',
        40, 296, { size: 11.5, fill: P.soft });
      A.txt(ctx, 'deleting a feature. It is why option 3 usually beats option 2.', 40, 314,
        { size: 11.5, w: 700, fill: P.g });
    }
    A.autoplay(root, c, render);
  });

  /* ============================================================
     10. The cost function with regularisation
     ============================================================ */
  A.def('regcost', function (root) {
    var c = A.canvas(root, 760, 350), ctx = c.ctx;
    var li = 3;
    var lams = [0, 0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000, 10000];
    var bar = A.ctrls(root), ro = A.readout(root);
    A.slider(bar, { label: 'λ =', min: 0, max: 9, step: 1, value: li,
      fmt: function () { return String(lams[li]); }, on: function (v) { li = v; render(); } });
    var D = [];
    (function () {
      for (var i = 0; i < 11; i++) {
        var x = -2.4 + i * .48;
        D.push({ x: x, y: .42 * x + .9 + (rnd(i * 11 + 5) - .5) * .8 });
      }
    })();
    var DEG = 8, SC = 2.6;
    function fit(lam) {
      var n = DEG + 1, A2 = [], b2 = [], i, j, q;
      for (i = 0; i < n; i++) {
        A2.push(new Array(n).fill(0)); b2.push(0);
        for (j = 0; j < n; j++) for (q = 0; q < D.length; q++)
          A2[i][j] += Math.pow(D[q].x / SC, i + j);
        if (i > 0) A2[i][i] += lam;
        for (q = 0; q < D.length; q++) b2[i] += Math.pow(D[q].x / SC, i) * D[q].y;
      }
      var Mx = A2.map(function (r, ri) { return r.slice().concat([b2[ri]]); });
      for (i = 0; i < n; i++) {
        var p = i;
        for (j = i + 1; j < n; j++) if (Math.abs(Mx[j][i]) > Math.abs(Mx[p][i])) p = j;
        var tm = Mx[i]; Mx[i] = Mx[p]; Mx[p] = tm;
        if (Math.abs(Mx[i][i]) < 1e-12) Mx[i][i] = 1e-12;
        for (j = i + 1; j < n; j++) {
          var f2 = Mx[j][i] / Mx[i][i];
          for (q = i; q <= n; q++) Mx[j][q] -= f2 * Mx[i][q];
        }
      }
      var sol = new Array(n);
      for (i = n - 1; i >= 0; i--) {
        var s = Mx[i][n];
        for (j = i + 1; j < n; j++) s -= Mx[i][j] * sol[j];
        sol[i] = s / Mx[i][i];
      }
      return sol;
    }
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var co = fit(lams[li]);
      function f(x) { var s = 0; for (var i = 0; i < co.length; i++) s += co[i] * Math.pow(x / SC, i); return s; }
      var box = { x: 70, y: 46, w: 320, h: 210 };
      var S = A.axes(ctx, box, [-2.7, 2.7], [-1.2, 3], {
        xticks: 4, yticks: 4, xfmt: function (v) { return v.toFixed(0); },
        yfmt: function (v) { return v.toFixed(0); }, xlab: 'x', ylab: 'y'
      });
      A.plot(ctx, S, [-2.7, 2.7], function (x) { return A.clamp(f(x), -2, 4); }, P.a, 2.8);
      D.forEach(function (p) { A.dot(ctx, S.X(p.x), S.Y(p.y), 4.8, P.b); });
      A.txt(ctx, 'a degree-8 polynomial, λ = ' + lams[li], box.x + box.w / 2, 36,
        { align: 'center', size: 12, w: 700, fill: P.a });
      /* the weights, as bars */
      A.txt(ctx, 'the size of the weights', 560, 46, { align: 'center', size: 12, w: 700, fill: P.soft });
      var mxw = Math.max.apply(null, co.map(Math.abs));
      co.forEach(function (v, j) {
        var y = 62 + j * 22;
        A.txt(ctx, 'w' + j, 432, y + 12, { align: 'right', size: 10.5, mono: true, fill: P.faint });
        A.line(ctx, 560, y, 560, y + 16, P.lineSoft, 1);
        var wdt = 118 * A.clamp(Math.abs(v) / (mxw || 1), 0, 1);
        A.rr(ctx, v >= 0 ? 560 : 560 - wdt, y + 2, Math.max(2, wdt), 12, 3);
        ctx.fillStyle = P.a; ctx.globalAlpha = .8; ctx.fill(); ctx.globalAlpha = 1;
        A.txt(ctx, v.toFixed(2), 700, y + 12, { align: 'right', size: 9.5, mono: true, fill: P.faint });
      });
      var msg = lams[li] === 0 ? ['λ = 0 — no penalty at all', P.r, 'huge weights, and a wildly wiggly curve. Textbook overfitting.']
        : lams[li] >= 1000 ? ['λ enormous — everything crushed', P.b, 'all weights ≈ 0, so f(x) ≈ b. A flat line. Textbook underfitting.']
        : ['λ in a sensible range', P.g, 'the weights are small but not zero — the curve follows the trend and ignores the noise.'];
      A.txt(ctx, msg[0], 70, 288, { size: 14, w: 700, fill: msg[1] });
      A.txt(ctx, msg[2], 70, 310, { size: 11.5, fill: P.soft });
      A.txt(ctx, 'The 1/(2m) on the penalty means λ does not need re-tuning when m changes.', 70, 334,
        { size: 11, fill: P.faint });
      ro.set('J(w, b) = <b>(1/2m) Σ ( f(x⁽ⁱ⁾) − y⁽ⁱ⁾ )²</b>  +  <b>(λ/2m) Σ<sub>j=1..n</sub> w<sub>j</sub>²</b>' +
        '\nThe first term says “fit the data”. The second says “keep the weights small”. λ decides which ' +
        'one wins, and the whole art is in balancing them.' +
        '\nNote the sum starts at j = 1: <b>b is not regularised</b>. Shrinking the intercept only slides ' +
        'the curve up and down; it does nothing about wiggliness.');
    }
    A.bind(c, render); render();
  });

  /* ============================================================
     11. The regularised update rule
     ============================================================ */
  A.def('reglinlog', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var alpha = 0.01, lam = 1, m = 50;
    var bar = A.ctrls(root), ro = A.readout(root);
    A.slider(bar, { label: 'α', min: .001, max: .1, step: .001, value: alpha,
      fmt: function (v) { return v.toFixed(3); }, on: function (v) { alpha = v; render(); } });
    A.slider(bar, { label: 'λ', min: 0, max: 20, step: .5, value: lam,
      fmt: function (v) { return v.toFixed(1); }, on: function (v) { lam = v; render(); } });
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var shrink = 1 - alpha * lam / m;
      A.txt(ctx, 'the regularised update, rearranged', 40, 42, { size: 13, w: 700, fill: P.soft });
      A.rr(ctx, 40, 58, 680, 44, 9);
      ctx.fillStyle = P.sunk; ctx.fill(); ctx.strokeStyle = P.lineSoft; ctx.stroke();
      A.txt(ctx, 'wⱼ := wⱼ − α [ (1/m) Σ ( f(x⁽ⁱ⁾) − y⁽ⁱ⁾ ) xⱼ⁽ⁱ⁾  +  (λ/m) wⱼ ]', 380, 86,
        { align: 'center', size: 14, mono: true, w: 700, fill: P.soft });
      A.arrow(ctx, 380, 108, 380, 124, P.line, 1.8);
      A.rr(ctx, 40, 130, 680, 44, 9);
      ctx.fillStyle = P.aS; ctx.fill(); ctx.strokeStyle = P.a; ctx.lineWidth = 2; ctx.stroke();
      A.txt(ctx, 'wⱼ := ' + shrink.toFixed(5) + ' · wⱼ  −  α (1/m) Σ ( f(x⁽ⁱ⁾) − y⁽ⁱ⁾ ) xⱼ⁽ⁱ⁾', 380, 158,
        { align: 'center', size: 14, mono: true, w: 700, fill: P.a });
      A.txt(ctx, '↑ (1 − αλ/m)', 168, 190, { align: 'center', size: 11, mono: true, fill: P.a });
      A.txt(ctx, 'shrink w a little', 168, 208, { align: 'center', size: 11, w: 700, fill: P.a });
      A.txt(ctx, '↑ the ordinary gradient step', 500, 190, { align: 'center', size: 11, fill: P.faint });
      A.txt(ctx, 'then move downhill as usual', 500, 208, { align: 'center', size: 11, w: 700, fill: P.faint });
      /* the decay picture */
      var w0 = 1, ws = [w0];
      for (var i = 0; i < 60; i++) ws.push(ws[ws.length - 1] * shrink);
      var box = { x: 60, y: 226, w: 300, h: 58 };
      ctx.save(); ctx.strokeStyle = P.a; ctx.lineWidth = 2; ctx.beginPath();
      ws.forEach(function (v, i) {
        var px = box.x + box.w * i / (ws.length - 1);
        var py = box.y + box.h - box.h * A.clamp(v, 0, 1);
        i === 0 ? ctx.moveTo(px, py) : ctx.lineTo(px, py);
      });
      ctx.stroke(); ctx.restore();
      A.line(ctx, box.x, box.y + box.h, box.x + box.w, box.y + box.h, P.line, 1);
      A.txt(ctx, 'a weight left alone for 60 steps shrinks to ' + (ws[60]).toFixed(3),
        box.x, box.y + box.h + 18, { size: 11, fill: P.faint });
      A.txt(ctx, 'Every single iteration multiplies every weight by a number just below 1 before doing anything else.',
        400, 240, { size: 11.5, fill: P.soft });
      A.txt(ctx, 'That is “weight decay”, and it is exactly what the name says.', 400, 260,
        { size: 11.5, w: 700, fill: P.a });
      A.txt(ctx, 'The b update is unchanged — b is never regularised.', 400, 284,
        { size: 11.5, fill: P.faint });
      A.txt(ctx, 'For logistic regression the formula is character-for-character identical. Only f changes: g(w·x + b).',
        40, 316, { size: 11.5, w: 700, fill: P.g });
      ro.set('(1 − αλ/m) with α = ' + alpha.toFixed(3) + ', λ = ' + lam + ', m = ' + m +
        ' gives <b>' + shrink.toFixed(5) + '</b>.' +
        '\nIf λ = 0 the factor is exactly 1 and you are back to ordinary gradient descent. ' +
        'Larger λ shrinks harder. This is the same mechanism as <code>weight_decay</code> in every ' +
        'modern deep-learning optimiser.');
    }
    A.autoplay(root, c, render);
  });

})();
