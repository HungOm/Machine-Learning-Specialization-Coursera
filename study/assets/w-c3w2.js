/* Widgets for Course 3 / Week 2 — recommender systems and PCA */
(function () {
  'use strict';

  var USERS = ['Alice', 'Bob', 'Carol', 'Dave'];
  var MOVIES = ['Love at Last', 'Romance Forever', 'Cute Puppies of Love',
                'Nonstop Car Chases', 'Swords vs. Karate'];
  /* ratings, null = not rated.  rows = movies, cols = users */
  var R = [
    [5, 5, 0, 0],
    [5, null, null, 0],
    [null, 4, 0, null],
    [0, 0, 5, 4],
    [0, 0, 5, null]
  ];
  /* the hand-made content features used in "using per-item features" */
  var XF = [[0.90, 0.00], [1.00, 0.01], [0.99, 0.00], [0.10, 1.00], [0.00, 0.90]];

  function solve(Am, bv) {
    var n = bv.length, i, j, k;
    var M = Am.map(function (r, ri) { return r.slice().concat([bv[ri]]); });
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
  /* least squares fit of w (2 features + bias) for one user, using XF */
  function fitUser(u, lam) {
    lam = lam == null ? 0.02 : lam;
    var A = [[0, 0, 0], [0, 0, 0], [0, 0, 0]], bv = [0, 0, 0];
    for (var i = 0; i < 5; i++) {
      if (R[i][u] === null) continue;
      var f = [XF[i][0], XF[i][1], 1];
      for (var a = 0; a < 3; a++) {
        for (var b2 = 0; b2 < 3; b2++) A[a][b2] += f[a] * f[b2];
        bv[a] += f[a] * R[i][u];
      }
    }
    for (var d = 0; d < 2; d++) A[d][d] += lam;
    return solve(A, bv);
  }

  /* ============================================================
     1. The ratings matrix
     ============================================================ */
  A.def('ratingsmatrix', function (root) {
    var c = A.canvas(root, 760, 320), ctx = c.ctx;
    var ro = A.readout(root);
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var qs = [];
      for (var i = 0; i < 5; i++) for (var j = 0; j < 4; j++) if (R[i][j] === null) qs.push([i, j]);
      var hot = qs[Math.floor((t * .6) % qs.length)];
      var x0 = 250, y0 = 74, cw = 96, ch = 42;
      USERS.forEach(function (u, j) {
        A.txt(ctx, u, x0 + j * cw + 46, y0 - 12, { align: 'center', size: 12.5, w: 700,
          fill: hot[1] === j ? P.a : P.soft });
      });
      MOVIES.forEach(function (m, i) {
        A.txt(ctx, m, x0 - 14, y0 + i * ch + 27, { align: 'right', size: 11.5, w: 700,
          fill: hot[0] === i ? P.a : P.soft });
      });
      A.matrix(ctx, x0, y0, 5, 4, cw, ch, P,
        function (i, j) { return R[i][j] === null ? '?' : String(R[i][j]); },
        { state: function (i, j) {
            if (R[i][j] === null) return (i === hot[0] && j === hot[1]) ? 1 : 4;
            return R[i][j] >= 4 ? 3 : 0;
          }, size: 15 });
      A.txt(ctx, 'ratings 0–5, and a lot of question marks', 250, 44, { size: 13, w: 700, fill: P.soft });
      var mTitle = MOVIES[hot[0]];
      if (mTitle.length > 16) mTitle = mTitle.slice(0, 15) + '…';
      A.txt(ctx, 'Would ' + USERS[hot[1]] + ' like', 40, 122, { size: 13.5, w: 700, fill: P.a });
      A.txt(ctx, '“' + mTitle + '”?', 40, 142, { size: 13.5, w: 700, fill: P.a });
      A.txt(ctx, 'That single question is the', 40, 172, { size: 12, fill: P.faint });
      A.txt(ctx, 'whole of recommender systems.', 40, 190, { size: 12, fill: P.faint });
      A.txt(ctx, 'n_u = ' + USERS.length + ' users', 40, 210, { size: 12, mono: true, fill: P.soft });
      A.txt(ctx, 'n_m = ' + MOVIES.length + ' movies', 40, 228, { size: 12, mono: true, fill: P.soft });
      A.txt(ctx, 'r(i,j) = 1 if rated', 40, 252, { size: 12, mono: true, fill: P.soft });
      A.txt(ctx, 'y(i,j) = the rating', 40, 270, { size: 12, mono: true, fill: P.soft });
      A.txt(ctx, 'Real matrices are 99.9% question marks: a million users, ten thousand films, and most people have rated twenty.',
        40, 306, { size: 11.5, fill: P.faint });
      ro.set('r(i, j) = 1 if user j has rated movie i, otherwise 0.   y(i, j) = the rating, defined only where r = 1.' +
        '\nEvery cost function this week sums <b>only over the entries where r(i, j) = 1</b> — you can never be ' +
        'penalised for a rating that does not exist.');
    }
    A.autoplay(root, c, render);
  });

  /* ============================================================
     2. Using per-item features
     ============================================================ */
  A.def('peritemfeatures', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var u = 0;
    var bar = A.ctrls(root), ro = A.readout(root);
    USERS.forEach(function (n, i) { A.button(bar, n, function () { u = i; sync(); render(); }); });
    function sync() { bar.querySelectorAll('button').forEach(function (b, i) { b.classList.toggle('primary', i === u); }); }
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var w = fitUser(u);
      var box = { x: 70, y: 46, w: 330, h: 200 };
      var S = A.axes(ctx, box, [-.1, 1.1], [-.1, 1.1], {
        xticks: 4, yticks: 4, xfmt: function (v) { return v.toFixed(1); },
        yfmt: function (v) { return v.toFixed(1); },
        xlab: 'x₁ — how romantic', ylab: 'x₂ — how much action'
      });
      /* shade the predicted rating over feature space */
      ctx.save(); ctx.globalAlpha = .11;
      for (var gx = 0; gx <= 34; gx++) for (var gy = 0; gy <= 24; gy++) {
        var fx = -.1 + 1.2 * gx / 34, fy = -.1 + 1.2 * gy / 24;
        var pr = A.clamp((w[0] * fx + w[1] * fy + w[2]) / 5, 0, 1);
        ctx.fillStyle = pr > .5 ? P.g : P.r;
        ctx.globalAlpha = .05 + .16 * Math.abs(pr - .5) * 2;
        ctx.fillRect(S.X(fx) - 6, S.Y(fy) - 6, 12, 12);
      }
      ctx.restore();
      MOVIES.forEach(function (m, i) {
        var rated = R[i][u] !== null;
        var pred = w[0] * XF[i][0] + w[1] * XF[i][1] + w[2];
        A.dot(ctx, S.X(XF[i][0]), S.Y(XF[i][1]), rated ? 7 : 6, rated ? (R[i][u] >= 3 ? P.g : P.r) : P.a);
        if (!rated) {
          ctx.save(); ctx.strokeStyle = P.a; ctx.lineWidth = 2; ctx.setLineDash([3, 3]);
          ctx.beginPath(); ctx.arc(S.X(XF[i][0]), S.Y(XF[i][1]), 11, 0, 6.2832); ctx.stroke(); ctx.restore();
        }
        A.txt(ctx, rated ? String(R[i][u]) : '→ ' + pred.toFixed(1),
          S.X(XF[i][0]) + 13, S.Y(XF[i][1]) + 4, { size: 11, mono: true, w: 700,
            fill: rated ? P.soft : P.a });
      });
      /* the fitted parameters */
      A.txt(ctx, USERS[u] + '’s learned taste', 470, 60, { size: 14, w: 700, fill: P.a });
      A.txt(ctx, 'w₁ (romance) = ' + w[0].toFixed(2), 470, 88, { size: 13, mono: true, fill: P.soft });
      A.txt(ctx, 'w₂ (action)  = ' + w[1].toFixed(2), 470, 110, { size: 13, mono: true, fill: P.soft });
      A.txt(ctx, 'b            = ' + w[2].toFixed(2), 470, 132, { size: 13, mono: true, fill: P.soft });
      var likes = w[0] > w[1] ? 'romance' : 'action';
      A.txt(ctx, '→ ' + USERS[u] + ' is a ' + likes + ' person', 470, 162,
        { size: 12.5, w: 700, fill: P.g });
      MOVIES.forEach(function (m, i) {
        if (R[i][u] !== null) return;
        var pred = w[0] * XF[i][0] + w[1] * XF[i][1] + w[2];
        A.txt(ctx, 'predict ' + pred.toFixed(2) + ' for “' + m + '”', 470, 196 + i * 18,
          { size: 11, fill: P.a });
      });
      A.txt(ctx, 'This is just linear regression — one separate little regression PER USER.', 70, 282,
        { size: 12.5, w: 700, fill: P.soft });
      A.txt(ctx, 'It only works because someone sat down and hand-labelled every film as romantic or action-y.',
        70, 302, { size: 12, fill: P.faint });
      A.txt(ctx, 'Nobody has time to do that for 10,000 films. Which is why the next lesson exists.',
        70, 322, { size: 12, w: 700, fill: P.a });
      ro.set('predicted rating = <b>w<sup>(j)</sup> · x<sup>(i)</sup> + b<sup>(j)</sup></b>' +
        '\ncost for user j: (1/2) Σ<sub>i : r(i,j)=1</sub> (w<sup>(j)</sup>·x<sup>(i)</sup> + b<sup>(j)</sup> − y<sup>(i,j)</sup>)² ' +
        '+ (λ/2) Σ (w<sub>k</sub><sup>(j)</sup>)²');
    }
    sync(); A.bind(c, render); render();
  });

  /* ============================================================
     3. Collaborative filtering — learn the features too
     ============================================================ */
  A.def('collabfilter', function (root) {
    var c = A.canvas(root, 760, 350), ctx = c.ctx;
    var n = 2, lr = 0.08, lam = 0.6;
    var X, W, B, hist, iter;
    function init() {
      X = MOVIES.map(function (_, i) { return [rand(i * 3 + 1), rand(i * 3 + 2)]; });
      W = USERS.map(function (_, j) { return [rand(j * 5 + 31), rand(j * 5 + 32)]; });
      B = USERS.map(function () { return 0; });
      hist = []; iter = 0;
    }
    function rand(s) { var v = Math.sin(s * 91.7 + 4.1) * 4351.17; return (v - Math.floor(v)) * 1.2 - .1; }
    function cost() {
      var J = 0, i, j, k;
      for (i = 0; i < 5; i++) for (j = 0; j < 4; j++) {
        if (R[i][j] === null) continue;
        var p = B[j]; for (k = 0; k < n; k++) p += W[j][k] * X[i][k];
        J += .5 * (p - R[i][j]) * (p - R[i][j]);
      }
      for (j = 0; j < 4; j++) for (k = 0; k < n; k++) J += lam / 2 * W[j][k] * W[j][k];
      for (i = 0; i < 5; i++) for (k = 0; k < n; k++) J += lam / 2 * X[i][k] * X[i][k];
      return J;
    }
    function step() {
      var gX = X.map(function () { return new Array(n).fill(0); });
      var gW = W.map(function () { return new Array(n).fill(0); });
      var gB = B.map(function () { return 0; });
      var i, j, k;
      for (i = 0; i < 5; i++) for (j = 0; j < 4; j++) {
        if (R[i][j] === null) continue;
        var p = B[j]; for (k = 0; k < n; k++) p += W[j][k] * X[i][k];
        var e = p - R[i][j];
        for (k = 0; k < n; k++) { gW[j][k] += e * X[i][k]; gX[i][k] += e * W[j][k]; }
        gB[j] += e;
      }
      for (j = 0; j < 4; j++) { for (k = 0; k < n; k++) gW[j][k] += lam * W[j][k]; }
      for (i = 0; i < 5; i++) { for (k = 0; k < n; k++) gX[i][k] += lam * X[i][k]; }
      for (j = 0; j < 4; j++) { for (k = 0; k < n; k++) W[j][k] -= lr * gW[j][k]; B[j] -= lr * gB[j]; }
      for (i = 0; i < 5; i++) for (k = 0; k < n; k++) X[i][k] -= lr * gX[i][k];
      iter++;
      if (iter % 4 === 0) { hist.push(cost()); if (hist.length > 120) hist.shift(); }
    }
    init();
    var bar = A.ctrls(root), ro = A.readout(root);
    A.button(bar, 'restart from random', function () { init(); });
    function pred(i, j) { var p = B[j]; for (var k = 0; k < n; k++) p += W[j][k] * X[i][k]; return p; }
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var x0 = 210, y0 = 66, cw = 74, ch = 36;
      USERS.forEach(function (u, j) {
        A.txt(ctx, u, x0 + j * cw + 35, y0 - 10, { align: 'center', size: 11.5, w: 700, fill: P.soft });
      });
      MOVIES.forEach(function (m, i) {
        A.txt(ctx, m.length > 17 ? m.slice(0, 16) + '…' : m, x0 - 12, y0 + i * ch + 23,
          { align: 'right', size: 10.5, fill: P.soft });
      });
      A.matrix(ctx, x0, y0, 5, 4, cw, ch, P,
        function (i, j) { return R[i][j] === null ? pred(i, j).toFixed(1) : String(R[i][j]); },
        { state: function (i, j) { return R[i][j] === null ? 1 : 0; }, size: 12 });
      A.txt(ctx, 'orange cells are the model’s guesses', x0 + 148, 46,
        { align: 'center', size: 11.5, w: 700, fill: P.a });
      /* the learned movie features */
      A.txt(ctx, 'learned features x⁽ⁱ⁾', 570, 46, { align: 'center', size: 12, w: 700, fill: P.p });
      MOVIES.forEach(function (m, i) {
        A.txt(ctx, '[' + X[i][0].toFixed(2) + ', ' + X[i][1].toFixed(2) + ']',
          570, 74 + i * 24, { align: 'center', size: 11.5, mono: true, fill: P.p });
      });
      A.txt(ctx, 'nobody labelled these —', 570, 208, { align: 'center', size: 10.5, fill: P.faint });
      A.txt(ctx, 'they were invented by the algorithm', 570, 222, { align: 'center', size: 10.5, fill: P.faint });
      /* cost curve */
      var box = { x: 70, y: 258, w: 300, h: 62 };
      if (hist.length > 2) {
        var mx = Math.max.apply(null, hist), mn = Math.min.apply(null, hist);
        ctx.save(); ctx.strokeStyle = P.a; ctx.lineWidth = 2; ctx.beginPath();
        hist.forEach(function (v, i) {
          var px = box.x + box.w * i / (hist.length - 1);
          var py = box.y + box.h - box.h * (v - mn) / (mx - mn + 1e-9);
          i === 0 ? ctx.moveTo(px, py) : ctx.lineTo(px, py);
        });
        ctx.stroke(); ctx.restore();
        A.txt(ctx, 'J = ' + hist[hist.length - 1].toFixed(3) + '   (iteration ' + iter + ')',
          box.x, box.y - 6, { size: 11.5, mono: true, fill: P.soft });
      }
      A.txt(ctx, 'gradient descent updates w, b AND x — all at the same time.', 400, 274,
        { size: 12, w: 700, fill: P.soft });
      A.txt(ctx, 'The users teach the algorithm what the movies are like,', 400, 294, { size: 11.5, fill: P.faint });
      A.txt(ctx, 'and the movies teach it what the users are like.', 400, 312, { size: 11.5, fill: P.faint });
      ro.set('J(w, b, x) = (1/2) <b>Σ</b><sub>(i,j) : r(i,j)=1</sub> (w<sup>(j)</sup>·x<sup>(i)</sup> + b<sup>(j)</sup> − y<sup>(i,j)</sup>)²' +
        ' + (λ/2)Σ(w<sub>k</sub><sup>(j)</sup>)² + (λ/2)Σ(x<sub>k</sub><sup>(i)</sup>)²' +
        '\nThe only change from the last lesson: <b>x is now a parameter too</b>, so the same sum is ' +
        'minimised over w, b <em>and</em> x.');
    }
    A.bind(c, render);
    A.loop(c.cv, function () {
      for (var s = 0; s < 3; s++) step();
      if (iter > 900) init();
      render();
    });
  });

  /* ============================================================
     4. Binary labels
     ============================================================ */
  A.def('binarylabels', function (root) {
    var c = A.canvas(root, 760, 450), ctx = c.ctx;
    var B = [[1, 1, 0, 0], [1, null, null, 0], [null, 1, 0, null], [0, 0, 1, 1], [0, 0, 1, null]];
    var ro = A.readout(root);
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var x0 = 230, y0 = 70, cw = 88, ch = 40;
      USERS.forEach(function (u, j) {
        A.txt(ctx, u, x0 + j * cw + 42, y0 - 12, { align: 'center', size: 12, w: 700, fill: P.soft });
      });
      MOVIES.forEach(function (m, i) {
        A.txt(ctx, m.length > 18 ? m.slice(0, 17) + '…' : m, x0 - 12, y0 + i * ch + 25,
          { align: 'right', size: 11, fill: P.soft });
      });
      A.matrix(ctx, x0, y0, 5, 4, cw, ch, P,
        function (i, j) { return B[i][j] === null ? '?' : (B[i][j] ? '1' : '0'); },
        { state: function (i, j) { return B[i][j] === null ? 4 : B[i][j] ? 3 : 0; }, size: 15 });
      /* the matrix spans y0=70 .. y0+5*ch=270 — every line below sits clear of it */
      A.txt(ctx, '1 = engaged (clicked, watched, bought, liked)', 40, 288, { size: 11.5, fill: P.g });
      A.txt(ctx, '0 = shown it and did NOT engage', 40, 306, { size: 11.5, fill: P.soft });
      A.txt(ctx, '? = never shown it at all', 40, 324, { size: 11.5, fill: P.r });
      A.txt(ctx, 'the “0 vs ?” distinction matters enormously and is the source of most bugs.', 40, 350,
        { size: 12, w: 700, fill: P.a });
      A.txt(ctx, 'Same algorithm, two swaps — exactly the jump from linear to logistic regression in Course 1.',
        40, 382, { size: 12.5, w: 700, fill: P.soft });
      A.txt(ctx, 'prediction:  w·x + b   →   g(w·x + b) = 1 / (1 + e^−(w·x+b))', 40, 406,
        { size: 12, mono: true, fill: P.a });
      A.txt(ctx, 'loss:  squared error   →   binary cross-entropy', 40, 428, { size: 12, mono: true, fill: P.a });
      ro.set('L(f, y) = −y·log(f) − (1−y)·log(1−f)   where f = g(w<sup>(j)</sup>·x<sup>(i)</sup> + b<sup>(j)</sup>)' +
        '\nThis is what real systems actually use: almost nobody has star ratings, and everybody has clicks.');
    }
    A.autoplay(root, c, render);
  });

  /* ============================================================
     5. Mean normalisation
     ============================================================ */
  A.def('meannorm', function (root) {
    var c = A.canvas(root, 760, 340), ctx = c.ctx;
    var on = false;
    var bar = A.ctrls(root), ro = A.readout(root);
    A.toggle(bar, 'subtract the row means', function (v) { on = v; render(); }, false);
    var means = R.map(function (row) {
      var v = row.filter(function (x) { return x !== null; });
      return v.reduce(function (s, x) { return s + x; }, 0) / v.length;
    });
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var names = USERS.concat(['Eve (new)']);
      var x0 = 250, y0 = 76, cw = 82, ch = 40;
      names.forEach(function (u, j) {
        A.txt(ctx, u, x0 + j * cw + 39, y0 - 12, { align: 'center', size: 11.5, w: 700,
          fill: j === 4 ? P.a : P.soft });
      });
      MOVIES.forEach(function (m, i) {
        A.txt(ctx, m.length > 17 ? m.slice(0, 16) + '…' : m, x0 - 12, y0 + i * ch + 25,
          { align: 'right', size: 10.5, fill: P.soft });
      });
      A.matrix(ctx, x0, y0, 5, 5, cw, ch, P, function (i, j) {
        if (j === 4) return on ? means[i].toFixed(1) : '0.0';
        if (R[i][j] === null) return '?';
        return on ? (R[i][j] - means[i]).toFixed(1) : String(R[i][j]);
      }, { state: function (i, j) { return j === 4 ? (on ? 3 : 4) : (R[i][j] === null ? 0 : 2); }, size: 12.5 });
      if (on) {
        A.txt(ctx, 'μ', x0 + 5 * cw + 20, y0 - 12, { align: 'center', size: 13, w: 700, fill: P.p });
        means.forEach(function (m, i) {
          A.txt(ctx, m.toFixed(2), x0 + 5 * cw + 20, y0 + i * ch + 25,
            { align: 'center', size: 11.5, mono: true, fill: P.p });
        });
      }
      A.txt(ctx, on ? 'each row now averages 0' : 'Eve has rated nothing at all', 40, 100,
        { size: 12.5, w: 700, fill: on ? P.g : P.r });
      (on
        ? ['so learning w = 0 for Eve', 'no longer means “predict 0”.', 'Adding μᵢ back gives her the',
           'average rating of each film —', 'a much more sensible start.']
        : ['Regularisation drives her w', 'to 0, so every prediction for', 'her is exactly 0.0.',
           'We would recommend nothing,', 'or recommend the worst films.']
      ).forEach(function (ln, i) {
        A.txt(ctx, ln, 40, 130 + i * 18, { size: 11, fill: on ? P.soft : P.faint });
      });
      A.txt(ctx, on ? 'predict:  w⁽ʲ⁾·x⁽ⁱ⁾ + b⁽ʲ⁾ + μᵢ   ← the mean is added back'
                   : 'predict:  w⁽ʲ⁾·x⁽ⁱ⁾ + b⁽ʲ⁾',
        250, 300, { size: 13, mono: true, w: 700, fill: on ? P.g : P.soft });
      A.txt(ctx, 'Normalise by ROW (per movie), not by column — the goal is helping new USERS.',
        250, 324, { size: 11.5, fill: P.faint });
      ro.set('Subtract each movie’s mean rating before training, then add it back when predicting.' +
        '\nA brand-new user gets the average rating of every film instead of 0 — much more useful, and it ' +
        'makes optimisation slightly faster too.');
    }
    A.bind(c, render); render();
  });

  /* ============================================================
     6. TensorFlow implementation with GradientTape
     ============================================================ */
  A.def('tfcollab', function (root) {
    var c = A.canvas(root, 760, 250), ctx = c.ctx;
    var lines = [
      ['w = tf.Variable(3.0)', 'a parameter TensorFlow will track'],
      ['x = 1.0 ;  y = 1.0 ;  alpha = 0.01', 'the data and the learning rate'],
      ['for iter in range(iterations):', 'the ordinary gradient-descent loop'],
      ['    with tf.GradientTape() as tape:', 'start recording every operation'],
      ['        fwb = w * x', 'forward: the prediction'],
      ['        costJ = (fwb - y) ** 2', 'forward: how wrong it is'],
      ['    [dJdw] = tape.gradient(costJ, [w])', 'replay the tape backwards → the gradient'],
      ['    w.assign_add(-alpha * dJdw)', 'the update step, by hand']
    ];
    var pre = document.createElement('pre');
    pre.innerHTML = lines.map(function (l, i) {
      return '<span class="ln" data-i="' + i + '">' + l[0].replace(/</g, '&lt;') + '</span>';
    }).join('\n');
    root.appendChild(pre);
    var note = A.readout(root);
    var step = 0;
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var taping = step >= 3 && step <= 5, backward = step === 6, updating = step === 7;
      A.rr(ctx, 60, 60, 300, 130, 12);
      ctx.fillStyle = taping ? P.bS : P.sunk; ctx.fill();
      ctx.strokeStyle = taping ? P.b : P.lineSoft; ctx.lineWidth = taping ? 2.4 : 1.2; ctx.stroke();
      A.txt(ctx, 'the tape', 210, 86, { align: 'center', size: 13, w: 700, fill: taping ? P.b : P.faint });
      A.txt(ctx, step >= 4 ? 'fwb = w × x' : '(empty)', 210, 118,
        { align: 'center', size: 13, mono: true, fill: step >= 4 ? P.b : P.faint });
      A.txt(ctx, step >= 5 ? 'costJ = (fwb − y)²' : '', 210, 144,
        { align: 'center', size: 13, mono: true, fill: step >= 5 ? P.b : P.faint });
      A.txt(ctx, taping ? 'recording…' : step > 5 ? 'recorded' : 'not started', 210, 172,
        { align: 'center', size: 11, fill: P.faint });
      A.arrow(ctx, 380, 125, 440, 125, backward ? P.a : P.line, backward ? 2.6 : 1.4);
      A.txt(ctx, 'replay backwards', 410, 112, { align: 'center', size: 10.5,
        fill: backward ? P.a : P.faint });
      A.rr(ctx, 460, 60, 240, 130, 12);
      ctx.fillStyle = backward || updating ? P.aS : P.sunk; ctx.fill();
      ctx.strokeStyle = backward || updating ? P.a : P.lineSoft;
      ctx.lineWidth = backward || updating ? 2.4 : 1.2; ctx.stroke();
      A.txt(ctx, 'dJ/dw', 580, 92, { align: 'center', size: 13, w: 700, fill: backward || updating ? P.a : P.faint });
      A.txt(ctx, step >= 6 ? '= 2(w·x − y)·x = 4.0' : '?', 580, 122,
        { align: 'center', size: 14, mono: true, w: 700, fill: step >= 6 ? P.a : P.faint });
      A.txt(ctx, updating ? 'w := 3.0 − 0.01(4.0) = 2.96' : '', 580, 156,
        { align: 'center', size: 12, mono: true, w: 700, fill: P.g });
      A.txt(ctx, 'Why write the loop by hand here? Because collaborative filtering’s cost is not a standard',
        60, 216, { size: 11.5, fill: P.soft });
      A.txt(ctx, 'Keras loss — it sums over a sparse set of (user, movie) pairs. GradientTape still handles it.',
        60, 234, { size: 11.5, fill: P.soft });
      pre.querySelectorAll('.ln').forEach(function (el, i) {
        var on = +el.dataset.i === step;
        el.style.display = 'block'; el.style.padding = '1px 6px'; el.style.borderRadius = '4px';
        el.style.background = on ? A.c('accent-soft') : 'transparent';
        el.style.color = on ? A.c('accent') : A.c('ink-soft');
        el.style.fontWeight = on ? '700' : '400';
      });
      note.set('<b>' + lines[step][0] + '</b>\n' + lines[step][1]);
    }
    var bar = A.ctrls(root);
    A.button(bar, '‹ back', function () { step = (step + lines.length - 1) % lines.length; render(lt); });
    A.button(bar, 'next step ›', function () { step = (step + 1) % lines.length; render(lt); }).classList.add('primary');
    root.appendChild(bar);
    A.autoplay(root, c, render);
  });

  /* ============================================================
     7. Finding related items
     ============================================================ */
  A.def('relateditems', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var pick = 0;
    var bar = A.ctrls(root), ro = A.readout(root);
    var SHORT = ['Love at Last', 'Romance Forever', 'Cute Puppies', 'Car Chases', 'Swords vs Karate'];
    SHORT.forEach(function (m, i) { A.button(bar, m, function () { pick = i; sync(); render(); }); });
    function sync() { bar.querySelectorAll('button').forEach(function (b, i) { b.classList.toggle('primary', i === pick); }); }
    function d2(i, j) {
      return (XF[i][0] - XF[j][0]) * (XF[i][0] - XF[j][0]) + (XF[i][1] - XF[j][1]) * (XF[i][1] - XF[j][1]);
    }
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var box = { x: 70, y: 46, w: 330, h: 210 };
      var S = A.axes(ctx, box, [-.15, 1.15], [-.15, 1.15], {
        xticks: 4, yticks: 4, xfmt: function (v) { return v.toFixed(1); },
        yfmt: function (v) { return v.toFixed(1); }, xlab: 'x₁', ylab: 'x₂'
      });
      var order = MOVIES.map(function (_, i) { return i; })
        .filter(function (i) { return i !== pick; })
        .sort(function (a, b) { return d2(pick, a) - d2(pick, b); });
      MOVIES.forEach(function (m, i) {
        var rank = order.indexOf(i);
        var near = rank >= 0 && rank < 2;
        if (i !== pick) A.line(ctx, S.X(XF[pick][0]), S.Y(XF[pick][1]), S.X(XF[i][0]), S.Y(XF[i][1]),
          near ? P.g : P.lineSoft, near ? 1.8 : 1, near ? null : [3, 3]);
        A.dot(ctx, S.X(XF[i][0]), S.Y(XF[i][1]), i === pick ? 9 : near ? 7 : 5,
          i === pick ? P.a : near ? P.g : P.faint);
        A.txt(ctx, SHORT[i], S.X(XF[i][0]) + 12, S.Y(XF[i][1]) + 4,
          { size: 10.5, w: i === pick || near ? 700 : 500, fill: i === pick ? P.a : near ? P.g : P.faint });
      });
      A.txt(ctx, 'because you watched', 450, 62, { size: 12, fill: P.faint });
      A.txt(ctx, SHORT[pick], 450, 84, { size: 15, w: 700, fill: P.a });
      A.txt(ctx, 'you might also like', 450, 116, { size: 12, fill: P.faint });
      order.slice(0, 3).forEach(function (i, r) {
        A.txt(ctx, (r + 1) + '. ' + SHORT[i], 450, 142 + r * 26,
          { size: 13, w: r < 2 ? 700 : 500, fill: r < 2 ? P.g : P.faint });
        A.txt(ctx, 'distance ' + Math.sqrt(d2(pick, i)).toFixed(3), 700, 142 + r * 26,
          { align: 'right', size: 11, mono: true, fill: P.faint });
      });
      A.txt(ctx, 'Two films are related if their learned feature vectors are close together.', 70, 288,
        { size: 12.5, w: 700, fill: P.soft });
      A.txt(ctx, 'You never have to know what x₁ and x₂ MEAN — distance works regardless.', 70, 310,
        { size: 12, fill: P.faint });
      ro.set('similarity = ‖ x<sup>(k)</sup> − x<sup>(i)</sup> ‖² = Σ<sub>l</sub> (x<sub>l</sub><sup>(k)</sup> − x<sub>l</sub><sup>(i)</sup>)²  — smallest wins.' +
        '\nAt scale, scanning every item is too slow. Production systems use approximate nearest-neighbour ' +
        'indexes (FAISS, ScaNN, HNSW) to do this in milliseconds over millions of items.');
    }
    sync(); A.bind(c, render); render();
  });

  /* ============================================================
     8. Collaborative vs content-based
     ============================================================ */
  A.def('cfvscbf', function (root) {
    var c = A.canvas(root, 760, 320), ctx = c.ctx;
    var rows = [
      ['what it uses', 'ratings from users similar to you', 'features OF the user and OF the item'],
      ['needs', 'lots of ratings per item', 'good descriptions: age, genre, country, cast'],
      ['cold start — new item', '✗ nobody has rated it yet', '✓ its features exist from day one'],
      ['cold start — new user', '✗ knows nothing about them', '✓ age, location, sign-up survey'],
      ['discovers', 'surprising links nobody described', 'what its features can express']
    ];
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var hot = Math.floor((t * .5) % rows.length);
      A.txt(ctx, 'COLLABORATIVE FILTERING', 300, 40, { align: 'center', size: 13, w: 700, fill: P.b });
      A.txt(ctx, 'CONTENT-BASED FILTERING', 590, 40, { align: 'center', size: 13, w: 700, fill: P.a });
      rows.forEach(function (r, i) {
        var y = 56 + i * 48, on = i === hot;
        A.txt(ctx, r[0], 150, y + 26, { align: 'right', size: 11.5, w: on ? 700 : 500,
          fill: on ? P.ink : P.faint });
        [[165, r[1], P.b], [450, r[2], P.a]].forEach(function (s) {
          A.rr(ctx, s[0], y, 275, 42, 7);
          ctx.fillStyle = on ? (s[2] === P.b ? P.bS : P.aS) : P.sunk; ctx.fill();
          ctx.strokeStyle = on ? s[2] : P.lineSoft; ctx.lineWidth = on ? 1.8 : 1; ctx.stroke();
          var words = s[1].split(' '), line = '', ln = 0;
          words.forEach(function (w) {
            if ((line + w).length > 36) {
              A.txt(ctx, line, s[0] + 12, y + 18 + ln * 14, { size: 10.5, w: on ? 700 : 500, fill: on ? s[2] : P.soft });
              line = w + ' '; ln++;
            } else line += w + ' ';
          });
          A.txt(ctx, line, s[0] + 12, y + 18 + ln * 14, { size: 10.5, w: on ? 700 : 500, fill: on ? s[2] : P.soft });
        });
      });
      A.txt(ctx, 'Real systems use BOTH: content-based to cover new users and items, collaborative to catch',
        40, 302, { size: 12, fill: P.soft });
      A.txt(ctx, 'the patterns nobody thought to describe.', 40, 318, { size: 12, w: 700, fill: P.a });
    }
    A.autoplay(root, c, render);
  });

})();

/* ---------- part 2 : deep content-based filtering, scale, ethics, PCA ---------- */
(function () {
  'use strict';

  function rnd(i) { var v = Math.sin(i * 33.71 + 9.13) * 17631.77; return v - Math.floor(v); }
  function gauss(i) {
    var r1 = rnd(i * 2 + 1), r2 = rnd(i * 2 + 2);
    return Math.sqrt(-2 * Math.log(r1 + 1e-9)) * Math.cos(6.2832 * r2);
  }

  /* ============================================================
     9. Deep learning for content-based filtering — two towers
     ============================================================ */
  A.def('deepcbf', function (root) {
    var c = A.canvas(root, 760, 350), ctx = c.ctx;
    var ro = A.readout(root);
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var phase = (t * .5) % 3;
      function tower(x, label, feats, colr, lit) {
        A.txt(ctx, label, x, 40, { align: 'center', size: 12.5, w: 700, fill: colr });
        feats.forEach(function (f, i) {
          A.rr(ctx, x - 78, 54 + i * 22, 156, 19, 4);
          ctx.fillStyle = P.sunk; ctx.fill();
          ctx.strokeStyle = P.lineSoft; ctx.stroke();
          A.txt(ctx, f, x, 68 + i * 22, { align: 'center', size: 10, fill: P.faint });
        });
        var y0 = 54 + feats.length * 22 + 8;
        var l1 = A.col(x, 4, y0 + 16, y0 + 76, 10), l2 = A.col(x, 3, y0 + 26, y0 + 66, 10);
        for (var i2 = 0; i2 < 4; i2++) for (var j = 0; j < 3; j++)
          A.link(ctx, l1[i2], l2[j], lit ? colr : P.line, lit ? 1 : .6, lit ? .5 : .22);
        l1.forEach(function (p) { A.neuron(ctx, p, lit ? .8 : .2, P, null, null, colr); });
        l2.forEach(function (p) { A.neuron(ctx, p, lit ? .8 : .2, P, null, null, colr); });
        A.txt(ctx, 'dense layers', x, y0 + 96, { align: 'center', size: 10, fill: P.faint });
        return y0 + 110;
      }
      var lit = phase > .6;
      var yEndU = tower(180, 'USER network', ['age', 'gender', 'country', 'avg rating per genre'], P.b, lit);
      var yEndM = tower(580, 'MOVIE network', ['year', 'genre(s)', 'average rating', 'cast / director'], P.a, lit);
      /* the two output vectors */
      var vy = Math.max(yEndU, yEndM);
      [[180, 'v_u', P.b], [580, 'v_m', P.a]].forEach(function (v) {
        A.rr(ctx, v[0] - 60, vy, 120, 30, 7);
        ctx.fillStyle = lit ? (v[2] === P.b ? P.bS : P.aS) : P.sunk; ctx.fill();
        ctx.strokeStyle = v[2]; ctx.lineWidth = 1.8; ctx.stroke();
        A.txt(ctx, v[1] + '  (32 numbers)', v[0], vy + 20, { align: 'center', size: 11.5, mono: true, w: 700, fill: v[2] });
      });
      var joined = phase > 1.6;
      A.line(ctx, 240, vy + 15, 340, vy + 15, joined ? P.g : P.line, joined ? 2.4 : 1.2);
      A.line(ctx, 520, vy + 15, 420, vy + 15, joined ? P.g : P.line, joined ? 2.4 : 1.2);
      A.rr(ctx, 340, vy - 2, 80, 34, 8);
      ctx.fillStyle = joined ? P.gS : P.sunk; ctx.fill();
      ctx.strokeStyle = joined ? P.g : P.lineSoft; ctx.lineWidth = joined ? 2.2 : 1.2; ctx.stroke();
      A.txt(ctx, 'v_u · v_m', 380, vy + 20, { align: 'center', size: 13, mono: true, w: 700,
        fill: joined ? P.g : P.faint });
      A.txt(ctx, joined ? '= the predicted rating' : '', 380, vy + 52,
        { align: 'center', size: 12, w: 700, fill: P.g });
      A.txt(ctx, 'The two networks can take completely different inputs and have completely different shapes —',
        40, 322, { size: 11.5, fill: P.soft });
      A.txt(ctx, 'they only have to agree on ONE thing: both must output a vector of the same length.',
        40, 340, { size: 11.5, w: 700, fill: P.a });
      ro.set('prediction = <b>v<sub>u</sub><sup>(j)</sup> · v<sub>m</sub><sup>(i)</sup></b>   ' +
        '(or g(v<sub>u</sub>·v<sub>m</sub>) for a binary label)' +
        '\nBoth towers are trained together, end to end, with one cost function — this is the ' +
        '“chain networks together” advantage from C2 W4 L13, being cashed in.');
    }
    A.autoplay(root, c, render);
  });

  /* ============================================================
     10. Recommending from a large catalogue
     ============================================================ */
  A.def('retrieval', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var K = 100;
    var bar = A.ctrls(root), ro = A.readout(root);
    A.slider(bar, { label: 'candidates retrieved', min: 20, max: 500, step: 10, value: K,
      fmt: function (v) { return v.toFixed(0); }, on: function (v) { K = v; render(); } });
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var stages = [
        { n: 'the whole catalogue', v: 10000, w: 620, col: P.faint,
          s: 'scoring all of these with the full model would take minutes' },
        { n: 'RETRIEVAL — fast and rough', v: K, w: A.clamp(620 * Math.sqrt(K / 10000) * 2.2, 90, 480), col: P.b,
          s: 'top 10 of each recently-watched genre, most-viewed in your country, similar to your last 3 films' },
        { n: 'RANKING — slow and accurate', v: K, w: A.clamp(620 * Math.sqrt(K / 10000) * 2.2, 90, 480), col: P.a,
          s: 'run the full two-tower network on just these' },
        { n: 'shown to the user', v: 10, w: 120, col: P.g, s: 'ranked by predicted rating' }
      ];
      var y = 46;
      stages.forEach(function (st, i) {
        var x = 380 - st.w / 2;
        A.rr(ctx, x, y, st.w, 44, 8);
        ctx.fillStyle = st.col === P.faint ? P.sunk : (st.col === P.b ? P.bS : st.col === P.a ? P.aS : P.gS);
        ctx.fill(); ctx.strokeStyle = st.col; ctx.lineWidth = 1.8; ctx.stroke();
        A.txt(ctx, st.n, 380, y + 20, { align: 'center', size: 12, w: 700, fill: st.col });
        A.txt(ctx, st.v.toLocaleString() + ' items', 380, y + 36, { align: 'center', size: 10.5, mono: true, fill: st.col });
        A.txt(ctx, st.s, 380, y + 60, { align: 'center', size: 10, fill: P.faint });
        if (i < 3) {
          A.arrow(ctx, 380, y + 66, 380, y + 76, P.line, 1.8);
        }
        y += 76;
      });
      var tradeoff = K < 60 ? ['too few candidates → faster, but you will miss good films', P.r]
        : K > 300 ? ['many candidates → better recommendations, slower and more expensive', P.m]
        : ['a reasonable balance — measure it offline before choosing', P.g];
      A.txt(ctx, tradeoff[0], 380, 320, { align: 'center', size: 12.5, w: 700, fill: tradeoff[1] });
      ro.set('<b>Retrieval</b> generates a large list of plausible candidates using cheap rules and ' +
        'precomputed nearest-neighbour lookups.  <b>Ranking</b> then scores only those with the expensive model.' +
        '\nHow to choose the candidate count: increase it offline and see whether recommendations actually ' +
        'improve. If they stop improving, stop paying for it.');
    }
    A.bind(c, render); render();
  });

  /* ============================================================
     11. Ethical use of recommender systems
     ============================================================ */
  A.def('ethicsrec', function (root) {
    var c = A.canvas(root, 760, 340), ctx = c.ctx;
    var mode = 0;
    var bar = A.ctrls(root), ro = A.readout(root);
    ['optimise for engagement', 'optimise for user benefit'].forEach(function (n, i) {
      A.button(bar, n, function () { mode = i; sync(); render(); });
    });
    function sync() { bar.querySelectorAll('button').forEach(function (b, i) { b.classList.toggle('primary', i === mode); }); }
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var engage = mode === 0;
      var cx = 250, cy = 160, Rr = 92;
      var nodes = [
        { a: -Math.PI / 2, t: 'show more of it', s: '' },
        { a: Math.PI / 6, t: engage ? 'user watches longer' : 'user finds it useful', s: '' },
        { a: Math.PI * 5 / 6, t: engage ? 'model learns: MORE' : 'model learns: more', s: '' }
      ];
      ctx.save(); ctx.strokeStyle = engage ? P.rS : P.gS; ctx.lineWidth = 24;
      ctx.beginPath(); ctx.arc(cx, cy, Rr, 0, 6.2832); ctx.stroke(); ctx.restore();
      var ang = (t * .9) % 6.2832;
      A.dot(ctx, cx + Math.cos(ang) * Rr, cy + Math.sin(ang) * Rr, 6, engage ? P.r : P.g);
      nodes.forEach(function (nd) {
        var x = cx + Math.cos(nd.a) * Rr, y = cy + Math.sin(nd.a) * Rr;
        A.dot(ctx, x, y, 10, engage ? P.r : P.g);
        A.dot(ctx, x, y, 6, P.panel);
        var lx = cx + Math.cos(nd.a) * (Rr + 36), ly = cy + Math.sin(nd.a) * (Rr + 36);
        var al = Math.abs(Math.cos(nd.a)) < .3 ? 'center' : (Math.cos(nd.a) > 0 ? 'left' : 'right');
        A.txt(ctx, nd.t, lx, ly, { align: al, size: 11.5, w: 700, fill: engage ? P.r : P.g });
      });
      A.txt(ctx, 'the feedback loop', cx, cy + 5, { align: 'center', size: 12.5, w: 700, fill: P.faint });
      /* what gets amplified */
      A.txt(ctx, engage ? 'what this amplifies' : 'what this amplifies', 570, 46,
        { align: 'center', size: 12.5, w: 700, fill: engage ? P.r : P.g });
      (engage
        ? ['outrage and conspiracy content', 'get-rich-quick and payday loans', 'algorithmic rabbit holes',
           'exploitative businesses that', 'simply bid more for attention', '',
           'None of this was intended.', 'It is what “maximise watch', 'time” means when you take', 'it literally.']
        : ['content people say afterwards', 'was worth their time', 'a transparent explanation of', 'why something was shown',
           'exploitative businesses filtered', 'out on purpose', '',
           'Costs engagement in the short', 'run. Andrew’s argument: be', 'transparent about the trade.']
      ).forEach(function (ln, i) {
        A.txt(ctx, ln, 440, 74 + i * 21, { size: 11.5, fill: ln ? (engage ? P.soft : P.soft) : P.faint });
      });
      A.txt(ctx, 'The maths in this week is neutral. What you point it at is not.', 40, 316,
        { size: 12.5, w: 700, fill: P.a });
      ro.set('Andrew’s framing: ask what the system is <b>really</b> optimising, and whether the people ' +
        'affected would agree that it serves them.' +
        '\nA recommender is unusual among ML systems in that it <b>changes the data it is later trained ' +
        'on</b> — it shapes the very preferences it claims to be measuring.');
    }
    sync();
    A.autoplay(root, c, render);
  });

  /* ============================================================
     12. TensorFlow implementation of content-based filtering
     ============================================================ */
  A.def('tfcbf', function (root) {
    var c = A.canvas(root, 760, 220), ctx = c.ctx;
    var lines = [
      ['user_NN = Sequential([Dense(256,"relu"), Dense(128,"relu"), Dense(32)])', 'tower 1 — ends at 32 units'],
      ['item_NN = Sequential([Dense(256,"relu"), Dense(128,"relu"), Dense(32)])', 'tower 2 — also ends at 32'],
      ['vu = tf.linalg.l2_normalize(user_NN(input_user), axis=1)', 'run the user tower, normalise to length 1'],
      ['vm = tf.linalg.l2_normalize(item_NN(input_item), axis=1)', 'run the item tower, normalise to length 1'],
      ['output = tf.keras.layers.Dot(axes=1)([vu, vm])', 'the dot product — the prediction'],
      ['model = Model([input_user, input_item], output)', 'one model with TWO inputs'],
      ['model.compile(optimizer=Adam(0.01), loss=MeanSquaredError())', 'train both towers together']
    ];
    var pre = document.createElement('pre');
    pre.innerHTML = lines.map(function (l, i) {
      return '<span class="ln" data-i="' + i + '">' + l[0].replace(/</g, '&lt;') + '</span>';
    }).join('\n');
    root.appendChild(pre);
    var note = A.readout(root);
    var step = 0;
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var uOn = step === 0 || step === 2, mOn = step === 1 || step === 3, dOn = step >= 4;
      [[150, 'user_NN', uOn, P.b], [430, 'item_NN', mOn, P.a]].forEach(function (tw) {
        A.rr(ctx, tw[0] - 90, 50, 180, 90, 10);
        ctx.fillStyle = tw[2] ? (tw[3] === P.b ? P.bS : P.aS) : P.sunk; ctx.fill();
        ctx.strokeStyle = tw[2] ? tw[3] : P.lineSoft; ctx.lineWidth = tw[2] ? 2.4 : 1.2; ctx.stroke();
        A.txt(ctx, tw[1], tw[0], 76, { align: 'center', size: 13, mono: true, w: 700, fill: tw[3] });
        A.txt(ctx, '256 → 128 → 32', tw[0], 100, { align: 'center', size: 11, mono: true, fill: P.faint });
        A.txt(ctx, tw[0] === 150 ? 'vu' : 'vm', tw[0], 126, { align: 'center', size: 12, mono: true, w: 700, fill: tw[3] });
      });
      A.arrow(ctx, 245, 95, 300, 95, dOn ? P.g : P.line, dOn ? 2.4 : 1.4);
      A.arrow(ctx, 335, 95, 290, 95, dOn ? P.g : P.line, 0.01);
      A.rr(ctx, 600, 60, 120, 70, 10);
      ctx.fillStyle = dOn ? P.gS : P.sunk; ctx.fill();
      ctx.strokeStyle = dOn ? P.g : P.lineSoft; ctx.lineWidth = dOn ? 2.4 : 1.2; ctx.stroke();
      A.txt(ctx, 'Dot', 660, 88, { align: 'center', size: 14, mono: true, w: 700, fill: dOn ? P.g : P.faint });
      A.txt(ctx, 'vu · vm', 660, 110, { align: 'center', size: 11.5, mono: true, fill: dOn ? P.g : P.faint });
      A.arrow(ctx, 525, 95, 595, 95, dOn ? P.g : P.line, dOn ? 2.4 : 1.4);
      A.txt(ctx, 'l2_normalize scales each vector to length 1, so the dot product becomes a cosine similarity —',
        40, 176, { size: 11.5, fill: P.soft });
      A.txt(ctx, 'it measures direction rather than magnitude, which trains far more stably.', 40, 194,
        { size: 11.5, fill: P.soft });
      A.txt(ctx, 'Note: the two towers do NOT share weights, and their inputs can be different sizes.',
        40, 212, { size: 11.5, w: 700, fill: P.a });
      pre.querySelectorAll('.ln').forEach(function (el, i) {
        var on = +el.dataset.i === step;
        el.style.display = 'block'; el.style.padding = '1px 6px'; el.style.borderRadius = '4px';
        el.style.background = on ? A.c('accent-soft') : 'transparent';
        el.style.color = on ? A.c('accent') : A.c('ink-soft');
        el.style.fontWeight = on ? '700' : '400';
      });
      note.set('<b>' + lines[step][0] + '</b>\n' + lines[step][1]);
    }
    var bar = A.ctrls(root);
    A.button(bar, '‹ back', function () { step = (step + lines.length - 1) % lines.length; render(); });
    A.button(bar, 'next step ›', function () { step = (step + 1) % lines.length; render(); }).classList.add('primary');
    root.appendChild(bar);
    A.bind(c, render); render();
  });

  /* ---------- a correlated 2-D dataset for PCA ---------- */
  var PTS = (function () {
    var a = [];
    for (var i = 0; i < 70; i++) {
      var u = gauss(i * 4 + 1) * 1.55, v = gauss(i * 4 + 3) * 0.42;
      a.push({ x: u * 0.94 - v * 0.34, y: u * 0.34 + v * 0.94 });
    }
    return a;
  })();
  function projVar(th) {
    var ux = Math.cos(th), uy = Math.sin(th);
    var ps = PTS.map(function (p) { return p.x * ux + p.y * uy; });
    var m = ps.reduce(function (s, v) { return s + v; }, 0) / ps.length;
    return ps.reduce(function (s, v) { return s + (v - m) * (v - m); }, 0) / ps.length;
  }
  var BESTTH = (function () {
    var b = 0, bv = -1;
    for (var th = 0; th < Math.PI; th += 0.002) { var v = projVar(th); if (v > bv) { bv = v; b = th; } }
    return b;
  })();
  var TOTVAR = projVar(BESTTH) + projVar(BESTTH + Math.PI / 2);

  /* ============================================================
     13. Reducing the number of features
     ============================================================ */
  A.def('pcaintro', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var ro = A.readout(root);
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var phase = A.clamp(((t * .35) % 3) - .4, 0, 1);
      var box = { x: 70, y: 46, w: 300, h: 230 };
      var S = A.axes(ctx, box, [-4, 4], [-4, 4], {
        xticks: 4, yticks: 4, xfmt: function (v) { return v.toFixed(0); },
        yfmt: function (v) { return v.toFixed(0); }, xlab: 'x₁ — length (cm)', ylab: 'x₂ — width (cm)'
      });
      var ux = Math.cos(BESTTH), uy = Math.sin(BESTTH);
      A.line(ctx, S.X(-4 * ux), S.Y(-4 * uy), S.X(4 * ux), S.Y(4 * uy), P.a, 2.4);
      PTS.forEach(function (p, i) {
        var d = p.x * ux + p.y * uy;
        var px = A.lerp(p.x, d * ux, A.ease(phase)), py = A.lerp(p.y, d * uy, A.ease(phase));
        if (phase > .04 && phase < .98)
          A.line(ctx, S.X(p.x), S.Y(p.y), S.X(d * ux), S.Y(d * uy), P.faint, .7, [2, 2]);
        A.dot(ctx, S.X(px), S.Y(py), 4, phase > .5 ? P.a : P.b);
      });
      A.txt(ctx, 'the new axis "z"', S.X(3 * ux) + 6, S.Y(3 * uy) - 6, { size: 11, w: 700, fill: P.a });
      /* the 1-D result */
      A.txt(ctx, 'after PCA: one number per point', 560, 46, { align: 'center', size: 12.5, w: 700, fill: P.a });
      A.line(ctx, 430, 160, 700, 160, P.line, 1.6);
      PTS.forEach(function (p) {
        var d = p.x * ux + p.y * uy;
        ctx.save(); ctx.globalAlpha = phase;
        A.dot(ctx, 565 + d * 34, 160, 4, P.a); ctx.restore();
      });
      A.txt(ctx, 'z', 700, 180, { size: 12, w: 700, fill: P.a });
      A.txt(ctx, 'Length and width move together — knowing one nearly tells you the other.', 430, 210,
        { size: 11.5, fill: P.soft });
      A.txt(ctx, 'So two numbers were never really two numbers. PCA finds the ONE direction that',
        430, 228, { size: 11.5, fill: P.soft });
      A.txt(ctx, 'carries almost all the information, and throws the rest away.', 430, 246,
        { size: 11.5, w: 700, fill: P.a });
      A.txt(ctx, 'Main use today: squashing 10, 50 or 1000 features down to 2 or 3 so a human can PLOT them and look.',
        70, 306, { size: 12, w: 700, fill: P.soft });
      ro.set('PCA finds new axes that are combinations of the old ones, ordered by how much of the data’s ' +
        'spread each one explains.' +
        '\nKeep the first few and you keep most of the information with far fewer numbers. ' +
        'It is <b>unsupervised</b> — there is no y anywhere.');
    }
    A.autoplay(root, c, render);
  });

  /* ============================================================
     14. The PCA algorithm — maximise the variance
     ============================================================ */
  A.def('pcaalgo', function (root) {
    var c = A.canvas(root, 760, 340), ctx = c.ctx;
    var th = 0.15;
    var bar = A.ctrls(root), ro = A.readout(root);
    A.slider(bar, { label: 'axis angle', min: 0, max: 3.1416, step: .01, value: th,
      fmt: function (v) { return (v * 180 / Math.PI).toFixed(0) + '°'; }, on: function (v) { th = v; render(); } });
    A.button(bar, 'snap to the best axis', function () { th = BESTTH; bar.querySelector('input').value = th; render(); });
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var box = { x: 70, y: 40, w: 300, h: 240 };
      var S = A.axes(ctx, box, [-4, 4], [-4, 4], {
        xticks: 4, yticks: 4, xfmt: function (v) { return v.toFixed(0); },
        yfmt: function (v) { return v.toFixed(0); }, xlab: 'x₁', ylab: 'x₂'
      });
      var ux = Math.cos(th), uy = Math.sin(th);
      var isBest = Math.abs(th - BESTTH) < .04;
      A.line(ctx, S.X(-4.4 * ux), S.Y(-4.4 * uy), S.X(4.4 * ux), S.Y(4.4 * uy),
        isBest ? P.g : P.a, 2.6);
      PTS.forEach(function (p) {
        var d = p.x * ux + p.y * uy;
        A.line(ctx, S.X(p.x), S.Y(p.y), S.X(d * ux), S.Y(d * uy), P.faint, .7, [2, 2]);
        A.dot(ctx, S.X(p.x), S.Y(p.y), 3.4, P.b);
        A.dot(ctx, S.X(d * ux), S.Y(d * uy), 3.4, isBest ? P.g : P.a);
      });
      /* variance vs angle */
      var box2 = { x: 450, y: 60, w: 250, h: 150 };
      var mxv = projVar(BESTTH) * 1.12;
      var S2 = A.axes(ctx, box2, [0, 3.1416], [0, mxv], {
        xticks: 4, yticks: 3, xfmt: function (v) { return (v * 180 / Math.PI).toFixed(0) + '°'; },
        yfmt: function (v) { return v.toFixed(1); }, xlab: 'axis angle', ylab: 'variance kept'
      });
      A.plot(ctx, S2, [0, 3.1416], projVar, P.a, 2.4);
      A.dot(ctx, S2.X(BESTTH), S2.Y(projVar(BESTTH)), 6, P.g);
      A.dot(ctx, S2.X(th), S2.Y(projVar(th)), 5, isBest ? P.g : P.a);
      A.txt(ctx, 'the maximum', S2.X(BESTTH) + 8, S2.Y(projVar(BESTTH)) + 16, { size: 10.5, w: 700, fill: P.g });
      var kept = projVar(th) / TOTVAR;
      A.txt(ctx, 'variance kept: ' + (kept * 100).toFixed(1) + '%', 450, 244,
        { size: 14, mono: true, w: 700, fill: isBest ? P.g : P.a });
      A.txt(ctx, isBest ? '← this is the first principal component' : 'rotate the axis to find the maximum',
        450, 266, { size: 11.5, w: 700, fill: isBest ? P.g : P.faint });
      A.txt(ctx, 'PCA picks the axis whose projections are the most SPREAD OUT. Spread = information kept.',
        70, 306, { size: 12, w: 700, fill: P.soft });
      A.txt(ctx, 'Equivalently — and this is the same statement — it is the axis that loses the least when you squash onto it.',
        70, 326, { size: 11.5, fill: P.faint });
      ro.set('1. subtract the mean of each feature (and usually scale them to comparable ranges)' +
        '\n2. the principal components are the <b>eigenvectors of the covariance matrix</b>, ordered by eigenvalue' +
        '\n3. project: z = x · u.  Reconstruct approximately: x̂ = z · u — a different thing from linear regression, ' +
        'which minimises vertical error against a <em>label</em>; PCA minimises perpendicular error and has no label at all.');
    }
    A.bind(c, render); render();
  });

  /* ============================================================
     15. PCA in code
     ============================================================ */
  A.def('pcacode', function (root) {
    var c = A.canvas(root, 760, 300), ctx = c.ctx;
    var ro = A.readout(root);
    var evr = [0.62, 0.21, 0.09, 0.045, 0.02, 0.008, 0.004, 0.003];
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var keep = 1 + Math.floor((t * .55) % 8);
      var cum = 0;
      A.txt(ctx, 'explained variance per component', 260, 40, { align: 'center', size: 12.5, w: 700, fill: P.soft });
      evr.forEach(function (v, i) {
        var x = 60 + i * 50, h = v * 320;
        A.rr(ctx, x, 200 - h, 40, h, 4);
        ctx.fillStyle = i < keep ? P.a : P.sunk; ctx.fill();
        ctx.strokeStyle = i < keep ? P.a : P.lineSoft; ctx.lineWidth = 1.2; ctx.stroke();
        A.txt(ctx, 'PC' + (i + 1), x + 20, 216, { align: 'center', size: 10, fill: i < keep ? P.a : P.faint });
        A.txt(ctx, (v * 100).toFixed(0) + '%', x + 20, 194 - h, { align: 'center', size: 10, mono: true,
          fill: i < keep ? P.a : P.faint });
        if (i < keep) cum += v;
      });
      A.txt(ctx, 'keeping ' + keep + ' component' + (keep > 1 ? 's' : '') + ' → ' +
        (cum * 100).toFixed(1) + '% of the variance', 60, 248, { size: 13.5, mono: true, w: 700, fill: P.a });
      A.txt(ctx, keep <= 3 ? 'few enough to plot and look at' : 'enough for most downstream models',
        60, 270, { size: 11.5, fill: P.faint });
      A.txt(ctx, 'Rule of thumb: keep enough components to reach 90–99% of the variance —', 480, 232,
        { align: 'right', size: 11, fill: P.soft });
      A.txt(ctx, 'or exactly 2 if the whole point is to draw a scatter plot.', 480, 250,
        { align: 'right', size: 11, w: 700, fill: P.a });
      A.txt(ctx, 'pca = PCA(n_components=' + keep + ')', 520, 76, { size: 12.5, mono: true, w: 700, fill: P.g });
      A.txt(ctx, 'X_red = pca.fit_transform(X)', 520, 98, { size: 12.5, mono: true, fill: P.soft });
      A.txt(ctx, 'pca.explained_variance_ratio_', 520, 120, { size: 12.5, mono: true, fill: P.soft });
      A.txt(ctx, 'pca.inverse_transform(X_red)', 520, 142, { size: 12.5, mono: true, fill: P.faint });
      A.txt(ctx, '← get an approximate x back', 520, 160, { size: 10.5, fill: P.faint });
      A.txt(ctx, 'PCA used to be recommended for speeding up supervised learning. With modern hardware',
        60, 292, { size: 11.5, fill: P.faint });
      ro.set('from sklearn.decomposition import PCA' +
        '\n<b>Visualisation is the main use today.</b> Andrew is explicit that the old advice — use PCA to ' +
        'compress features before a supervised model — is much less useful now that computers are fast and ' +
        'regularisation handles extra features well.');
    }
    A.autoplay(root, c, render);
  });

})();
