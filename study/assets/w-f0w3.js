/* Widgets for Foundations / Week 3 — the maths behind the curtain */
(function () {
  'use strict';

  /* ============================================================
     1. Eigenvectors — the directions that do not turn
     ============================================================ */
  A.def('f0-eigen', function (root) {
    var c = A.canvas(root, 760, 340), ctx = c.ctx;
    var ang = 0.6;
    var M = [[2, 1], [1, 2]];
    var bar = A.ctrls(root), log = A.log(root), ro = A.readout(root);
    A.slider(bar, { label: 'input direction', min: 0, max: 3.1416, step: .01, value: ang,
      fmt: function (v) { return (v * 180 / Math.PI).toFixed(0) + '°'; },
      on: function (v) { ang = v; render(); } });
    A.button(bar, 'snap to 45°', function () { ang = Math.PI / 4; render(); });
    A.button(bar, 'snap to 135°', function () { ang = 3 * Math.PI / 4; render(); });
    function mul(v) { return [M[0][0] * v[0] + M[0][1] * v[1], M[1][0] * v[0] + M[1][1] * v[1]]; }
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var box = { x: 70, y: 40, w: 300, h: 250 };
      var S = A.axes(ctx, box, [-4, 4], [-4, 4], {
        xticks: 4, yticks: 4, xfmt: function (v) { return v.toFixed(0); },
        yfmt: function (v) { return v.toFixed(0); }, xlab: 'x', ylab: 'y'
      });
      var v = [Math.cos(ang) * 1.6, Math.sin(ang) * 1.6];
      var Av = mul(v);
      /* the two eigen-directions, drawn faintly */
      [[1, 1, P.g, 'λ = 3'], [1, -1, P.b, 'λ = 1']].forEach(function (e) {
        var n = Math.sqrt(2);
        A.line(ctx, S.X(-3.6 * e[0] / n), S.Y(-3.6 * e[1] / n),
                    S.X(3.6 * e[0] / n), S.Y(3.6 * e[1] / n), e[2], 1.2, [4, 4]);
        A.txt(ctx, e[3], S.X(3.0 * e[0] / n) + 6, S.Y(3.0 * e[1] / n),
          { size: 11, w: 700, fill: e[2] });
      });
      A.arrow(ctx, S.X(0), S.Y(0), S.X(v[0]), S.Y(v[1]), P.b, 2.6);
      A.arrow(ctx, S.X(0), S.Y(0), S.X(Av[0]), S.Y(Av[1]), P.a, 2.6);
      A.txt(ctx, 'v', S.X(v[0]) + 8, S.Y(v[1]) - 4, { size: 13, w: 700, fill: P.b });
      A.txt(ctx, 'Av', S.X(Av[0]) + 8, S.Y(Av[1]) - 4, { size: 13, w: 700, fill: P.a });
      /* how far the output turned from the input */
      var a1 = Math.atan2(v[1], v[0]), a2 = Math.atan2(Av[1], Av[0]);
      var turn = Math.abs(((a2 - a1) * 180 / Math.PI + 540) % 360 - 180);
      var aligned = turn < 0.8;
      A.txt(ctx, 'A = [[2, 1], [1, 2]]', 420, 62, { size: 13, mono: true, w: 700, fill: P.soft });
      A.rr(ctx, 420, 84, 280, 60, 8);
      ctx.fillStyle = aligned ? P.gS : P.sunk; ctx.fill();
      ctx.strokeStyle = aligned ? P.g : P.lineSoft; ctx.lineWidth = aligned ? 2.2 : 1; ctx.stroke();
      A.txt(ctx, aligned ? 'no rotation — this IS an eigenvector'
                         : 'turned by ' + turn.toFixed(1) + '°',
        560, 120, { align: 'center', size: 13.5, w: 700, fill: aligned ? P.g : P.soft });
      A.txt(ctx, 'Almost every direction gets rotated. Two do not, and those two are a',
        420, 178, { size: 11.5, fill: P.faint });
      A.txt(ctx, 'property of the matrix — nothing you chose.', 420, 196,
        { size: 11.5, fill: P.faint });
      A.txt(ctx, 'A[1,1] = [3,3] = 3·[1,1]', 420, 228, { size: 12.5, mono: true, w: 700, fill: P.g });
      A.txt(ctx, 'A[1,−1] = [1,−1] = 1·[1,−1]', 420, 250, { size: 12.5, mono: true, w: 700, fill: P.b });
      A.txt(ctx, 'PCA: the covariance matrix’s eigenvectors are the natural axes of the data,',
        70, 314, { size: 12, fill: P.soft });
      A.txt(ctx, 'and each eigenvalue IS the variance along its own eigenvector.', 70, 334,
        { size: 12, w: 700, fill: P.a });
      log.set('input ' + (ang * 180 / Math.PI).toFixed(0) + '°  →  output turned ' +
        turn.toFixed(1) + '°' + (aligned ? '   ← eigenvector' : ''),
        'Av = λv  — for these directions a whole matrix collapses to one number');
      ro.set('Symmetric matrices — and every covariance matrix is symmetric — always have real ' +
        'eigenvalues and perpendicular eigenvectors.\nThat is why PCA is so well behaved.');
    }
    A.bind(c, render); render();
  });

  /* ============================================================
     2. SVD — rotate, stretch, rotate
     ============================================================ */
  A.def('f0-svd', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var keep = 2;
    var bar = A.ctrls(root), log = A.log(root), ro = A.readout(root);
    var SV = [4.988, 0.567];
    A.slider(bar, { label: 'singular values kept', min: 1, max: 2, step: 1, value: 2,
      fmt: function (v) { return v.toFixed(0); }, on: function (v) { keep = v; render(); } });
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var stages = [['V', 'rotate the input', P.b], ['Σ', 'stretch along the axes', P.a],
                    ['U', 'rotate the output', P.p]];
      A.txt(ctx, 'any matrix at all = rotate, stretch, rotate', 60, 44,
        { size: 13, w: 700, fill: P.soft });
      stages.forEach(function (s, i) {
        var x = 90 + i * 200;
        A.rr(ctx, x, 66, 150, 62, 9);
        ctx.fillStyle = i === 1 ? P.aS : i === 0 ? P.bS : P.pS; ctx.fill();
        ctx.strokeStyle = s[2]; ctx.lineWidth = 2; ctx.stroke();
        A.txt(ctx, s[0], x + 75, 100, { align: 'center', size: 22, w: 700, fill: s[2] });
        A.txt(ctx, s[1], x + 75, 120, { align: 'center', size: 10.5, fill: s[2] });
        if (i < 2) A.arrow(ctx, x + 156, 97, x + 184, 97, P.line, 1.8);
      });
      A.txt(ctx, 'the singular values, always sorted largest first', 60, 168,
        { size: 12.5, w: 700, fill: P.soft });
      var tot = SV[0] * SV[0] + SV[1] * SV[1];
      SV.forEach(function (s, i) {
        var y = 182 + i * 40, on = i < keep;
        A.rr(ctx, 90, y, Math.max(6, s * 110), 30, 5);
        ctx.fillStyle = on ? P.aS : P.sunk; ctx.fill();
        ctx.strokeStyle = on ? P.a : P.lineSoft; ctx.lineWidth = on ? 2 : 1; ctx.stroke();
        A.txt(ctx, s.toFixed(3), 100 + Math.max(6, s * 110), y + 21,
          { size: 12.5, mono: true, w: 700, fill: on ? P.a : P.faint });
        if (!on) A.txt(ctx, 'discarded', 180 + Math.max(6, s * 110), y + 21,
          { size: 11, fill: P.faint });
      });
      var kept = SV.slice(0, keep).reduce(function (a, s) { return a + s * s; }, 0) / tot;
      A.txt(ctx, 'keeping ' + keep + ': ' + (kept * 100).toFixed(1) + '% of the variance retained',
        60, 288, { size: 12.5, w: 700, fill: kept > 0.95 ? P.g : P.a });
      A.txt(ctx, 'Truncating to the top k is the PROVABLY best rank-k approximation (Eckart–Young).',
        60, 312, { size: 11.5, fill: P.faint });
      log.set('singular values ' + SV.map(function (s) { return s.toFixed(3); }).join(', ') +
        '  ·  squares ÷ n = 4.976, 0.064  ← the covariance eigenvalues',
        'A = U Σ Vᵀ    — and PCA is the SVD of the centred data');
      ro.set('Real PCA implementations use SVD rather than eigendecomposition, because forming the ' +
        'covariance matrix squares the data and loses precision.');
    }
    A.bind(c, render); render();
  });

  /* ============================================================
     3. Maximum likelihood
     ============================================================ */
  A.def('f0-mle', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var p = 0.5;
    var n = 10, k = 7;
    var bar = A.ctrls(root), log = A.log(root), ro = A.readout(root);
    A.slider(bar, { label: 'assumed bias p', min: 0.05, max: 0.95, step: .01, value: p,
      fmt: function (v) { return v.toFixed(2); }, on: function (v) { p = v; render(); } });
    A.button(bar, 'snap to the peak', function () { p = 0.7; render(); });
    function lik(q) { return Math.pow(q, k) * Math.pow(1 - q, n - k); }
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var box = { x: 70, y: 46, w: 620, h: 190 };
      var mx = lik(k / n) * 1.15;
      var S = A.axes(ctx, box, [0, 1], [0, mx], {
        xticks: 5, yticks: 4, xfmt: function (v) { return v.toFixed(1); },
        yfmt: function (v) { return v.toFixed(4); },
        xlab: 'assumed bias p', ylab: 'probability of the data'
      });
      A.plot(ctx, S, [0.02, 0.98], lik, P.a, 2.6);
      A.dot(ctx, S.X(k / n), S.Y(lik(k / n)), 6, P.g);
      A.txt(ctx, 'the peak — p = 0.7', S.X(k / n) + 10, S.Y(lik(k / n)) - 8,
        { size: 11.5, w: 700, fill: P.g });
      ctx.save(); ctx.strokeStyle = P.a; ctx.lineWidth = 1.6; ctx.setLineDash([4, 4]);
      ctx.beginPath(); ctx.moveTo(S.X(p), S.Y(0)); ctx.lineTo(S.X(p), S.Y(lik(p)));
      ctx.stroke(); ctx.restore();
      A.dot(ctx, S.X(p), S.Y(lik(p)), 5, P.a);
      A.txt(ctx, '10 flips, 7 heads. If the bias really were p, how likely was exactly that?',
        70, 268, { size: 12.5, w: 700, fill: P.soft });
      A.txt(ctx, 'Pick the p that makes the observed data most probable. That is the whole principle —',
        70, 292, { size: 12, fill: P.faint });
      A.txt(ctx, 'and squared error and cross-entropy both fall straight out of it.', 70, 312,
        { size: 12, w: 700, fill: P.a });
      log.set('p = ' + p.toFixed(2) + '  ·  L = ' + lik(p).toFixed(6) +
        '  ·  −log L = ' + (-Math.log(lik(p))).toFixed(4) +
        (Math.abs(p - 0.7) < 0.005 ? '   ← the maximum' : ''),
        'L(p) = p^7 (1−p)^3   — maximise it, or equivalently minimise −log L');
      ro.set('Gaussian noise → squared error. Bernoulli outcome → cross-entropy.\n' +
        'The loss function stops being a convention and becomes a consequence of what you assumed.');
    }
    A.bind(c, render); render();
  });

  /* ============================================================
     4. The Jacobian
     ============================================================ */
  A.def('f0-jacobian', function (root) {
    var c = A.canvas(root, 760, 320), ctx = c.ctx;
    var pick = 0;
    var bar = A.ctrls(root), ro = A.readout(root);
    ['nudge x₁', 'nudge x₂', 'nudge x₃'].forEach(function (n, i) {
      A.button(bar, n, function () { pick = i; sync(); render(); });
    });
    function sync() { bar.querySelectorAll('button').forEach(function (b, i) { b.classList.toggle('primary', i === pick); }); }
    function render() {
      var P = A.pal(); c.clear(P.panel);
      A.txt(ctx, 'a function taking 3 numbers to 2', 60, 44, { size: 12.5, w: 700, fill: P.soft });
      /* inputs */
      for (var j = 0; j < 3; j++) {
        var x = 70 + j * 90, on = j === pick;
        A.rr(ctx, x, 62, 76, 40, 6);
        ctx.fillStyle = on ? P.bS : P.sunk; ctx.fill();
        ctx.strokeStyle = on ? P.b : P.lineSoft; ctx.lineWidth = on ? 2.2 : 1; ctx.stroke();
        A.txt(ctx, 'x' + (j + 1), x + 38, 88, { align: 'center', size: 14, w: 700,
          fill: on ? P.b : P.soft });
      }
      /* outputs */
      for (var i = 0; i < 2; i++) {
        var y = 62 + i * 56;
        A.rr(ctx, 400, y, 76, 40, 6);
        ctx.fillStyle = P.aS; ctx.fill(); ctx.strokeStyle = P.a; ctx.lineWidth = 1.6; ctx.stroke();
        A.txt(ctx, 'f' + (i + 1), 438, y + 26, { align: 'center', size: 14, w: 700, fill: P.a });
        A.arrow(ctx, 70 + pick * 90 + 38, 104, 400, y + 20, P.b, 2);
      }
      /* the grid */
      A.matrix(ctx, 530, 62, 2, 3, 56, 46, P, function (r, cc) {
        return '∂f' + (r + 1) + '/∂x' + (cc + 1);
      }, { state: function (r, cc) { return cc === pick ? 1 : 0; }, size: 9.5,
           label: 'J — shape (2, 3)' });
      A.txt(ctx, 'One derivative per (output, input) pair. Rows are outputs, columns are inputs —',
        60, 190, { size: 12, fill: P.soft });
      A.txt(ctx, 'so the shape tells you the function’s signature.', 60, 210,
        { size: 12, w: 700, fill: P.a });
      A.rr(ctx, 60, 230, 640, 34, 6);
      ctx.fillStyle = P.gS; ctx.fill(); ctx.strokeStyle = P.g; ctx.lineWidth = 1.6; ctx.stroke();
      A.txt(ctx, 'the gradient you have used since Course 1 is a Jacobian with ONE row — ' +
        'because a cost has one output', 76, 252, { size: 12, w: 700, fill: P.g });
      A.txt(ctx, 'The chain rule becomes matrix multiplication, and backprop is that product ' +
        'evaluated right to left.', 60, 290, { size: 11.5, fill: P.faint });
      A.txt(ctx, 'Right to left keeps a row vector at every step. Left to right would build huge ' +
        'intermediate matrices.', 60, 310, { size: 11.5, fill: P.faint });
      ro.set('A 512→256 layer has a Jacobian of shape (256, 512) — 131,072 numbers.\n' +
        'Frameworks never build it: they compute Jacobian-<b>vector</b> products, because for a ' +
        'scalar loss you only ever need one row.');
    }
    sync(); A.bind(c, render); render();
  });

  /* ============================================================
     5. Softmax + cross-entropy gradient
     ============================================================ */
  A.def('f0-softmax-grad', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var z = [2.0, 1.0, 0.5];
    var bar = A.ctrls(root), log = A.log(root), ro = A.readout(root);
    z.forEach(function (v, i) {
      A.slider(bar, { label: 'z' + (i + 1), min: -3, max: 4, step: .1, value: v,
        fmt: function (q) { return q.toFixed(1); }, on: function (q) { z[i] = q; render(); } });
    });
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var m = Math.max.apply(null, z);
      var e = z.map(function (v) { return Math.exp(v - m); });
      var s = e.reduce(function (a, b) { return a + b; }, 0);
      var p = e.map(function (v) { return v / s; });
      var y = [1, 0, 0];
      A.txt(ctx, 'scores z (true class is the first)', 60, 44, { size: 12.5, w: 700, fill: P.soft });
      z.forEach(function (v, i) {
        var x = 60 + i * 220;
        A.rr(ctx, x, 58, 200, 34, 5);
        ctx.fillStyle = P.sunk; ctx.fill(); ctx.strokeStyle = P.lineSoft; ctx.stroke();
        A.txt(ctx, 'z' + (i + 1) + ' = ' + v.toFixed(1), x + 100, 81,
          { align: 'center', size: 12.5, mono: true, fill: P.soft });
      });
      A.txt(ctx, 'softmax p', 60, 124, { size: 12.5, w: 700, fill: P.b });
      p.forEach(function (v, i) {
        var x = 60 + i * 220;
        A.rr(ctx, x, 136, Math.max(6, v * 200), 28, 4);
        ctx.fillStyle = P.bS; ctx.fill(); ctx.strokeStyle = P.b; ctx.stroke();
        A.txt(ctx, v.toFixed(4), x + 8 + Math.max(6, v * 200), 156,
          { size: 12, mono: true, fill: P.b });
      });
      A.txt(ctx, 'gradient  ∂L/∂z  =  p − y', 60, 202, { size: 13, w: 700, fill: P.a });
      p.forEach(function (v, i) {
        var g = v - y[i], x = 60 + i * 220;
        A.rr(ctx, x, 214, 200, 34, 5);
        ctx.fillStyle = g < 0 ? P.gS : P.aS; ctx.fill();
        ctx.strokeStyle = g < 0 ? P.g : P.a; ctx.lineWidth = 1.8; ctx.stroke();
        A.txt(ctx, g.toFixed(4), x + 100, 237, { align: 'center', size: 13.5, mono: true, w: 700,
          fill: g < 0 ? P.g : P.a });
      });
      A.txt(ctx, 'Two messy derivatives — softmax’s full Jacobian and the log’s 1/p — cancel',
        60, 282, { size: 12, fill: P.soft });
      A.txt(ctx, 'exactly, leaving one subtraction. Verified numerically to four decimals.',
        60, 302, { size: 12, w: 700, fill: P.a });
      A.txt(ctx, 'The true class gets a negative gradient (push it up); the rest positive (push down).',
        60, 324, { size: 11.5, fill: P.faint });
      log.set('p = [' + p.map(function (v) { return v.toFixed(4); }).join(', ') +
        ']   →   ∂L/∂z = [' + p.map(function (v, i) { return (v - y[i]).toFixed(4); }).join(', ') + ']',
        '∂L/∂z = p − y   — for any number of classes, one subtraction');
      ro.set('Same cancellation as sigmoid + log loss in C1 W3, generalised from two classes to N.\n' +
        'It is why <code>from_logits=True</code> exists: the framework can use the cancelled form ' +
        'directly.');
    }
    A.bind(c, render); render();
  });

})();
