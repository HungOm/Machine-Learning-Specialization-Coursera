/* Widgets for Course 1 / Week 2 — multiple features, vectorisation, scaling */
(function () {
  'use strict';

  /* size (sqft), bedrooms, floors, age -> price ($1000s) */
  var ROWS = [
    [2104, 5, 1, 45, 460], [1416, 3, 2, 40, 232], [1534, 3, 2, 30, 315],
    [852, 2, 1, 36, 178], [1940, 4, 2, 12, 385], [1000, 2, 1, 8, 210]
  ];
  var COLS = ['size (sqft)', 'bedrooms', 'floors', 'age (yrs)'];
  var W = [0.1, 4, 10, -2], B = 80;

  /* ============================================================
     1. Multiple features
     ============================================================ */
  A.def('multifeatures', function (root) {
    var c = A.canvas(root, 760, 340), ctx = c.ctx;
    var ro = A.readout(root);
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var hi = Math.floor((t * .55) % ROWS.length), hj = Math.floor((t * .55 / ROWS.length) % 4);
      var x0 = 150, y0 = 84, cw = 104, ch = 36;
      COLS.forEach(function (n, j) {
        A.txt(ctx, 'x' + (j + 1), x0 + j * cw + 50, y0 - 26, { align: 'center', size: 13, mono: true,
          w: 700, fill: j === hj ? P.a : P.soft });
        A.txt(ctx, n, x0 + j * cw + 50, y0 - 10, { align: 'center', size: 9.5, fill: P.faint });
      });
      A.txt(ctx, 'y', x0 + 4 * cw + 40, y0 - 26, { align: 'center', size: 13, mono: true, w: 700, fill: P.g });
      A.txt(ctx, 'price', x0 + 4 * cw + 40, y0 - 10, { align: 'center', size: 9.5, fill: P.faint });
      A.matrix(ctx, x0, y0, ROWS.length, 4, cw, ch, P,
        function (i, j) { return String(ROWS[i][j]); },
        { state: function (i, j) { return i === hi && j === hj ? 1 : i === hi ? 2 : 0; }, size: 12 });
      A.matrix(ctx, x0 + 4 * cw + 8, y0, ROWS.length, 1, 76, ch, P,
        function (i) { return String(ROWS[i][4]); },
        { state: function (i) { return i === hi ? 3 : 0; }, size: 12 });
      ROWS.forEach(function (r, i) {
        A.txt(ctx, 'x⁽' + (i + 1) + '⁾', x0 - 14, y0 + i * ch + 24, { align: 'right', size: 12,
          mono: true, w: i === hi ? 700 : 500, fill: i === hi ? P.a : P.faint });
      });
      A.txt(ctx, 'x' + (hj + 1) + '⁽' + (hi + 1) + '⁾ = ' + ROWS[hi][hj], 40, 300,
        { size: 15, mono: true, w: 700, fill: P.a });
      A.txt(ctx, 'subscript = which feature · superscript in round brackets = which example', 40, 322,
        { size: 11.5, fill: P.faint });
      A.txt(ctx, 'n = 4 features, m = ' + ROWS.length + ' examples', 40, 60, { size: 12.5, w: 700, fill: P.soft });
      A.txt(ctx, 'one row is one house — a VECTOR of four numbers, written x⁽ⁱ⁾ (bold x)', 40, 40,
        { size: 12, fill: P.faint });
      ro.set('f<sub>w,b</sub>(x) = <b>w<sub>1</sub>x<sub>1</sub> + w<sub>2</sub>x<sub>2</sub> + ' +
        'w<sub>3</sub>x<sub>3</sub> + w<sub>4</sub>x<sub>4</sub> + b</b>' +
        '\nOne weight per feature, plus one bias. With the example weights: price ≈ 0.1×size + 4×beds + ' +
        '10×floors − 2×age + 80.' +
        '\nRead those as: +$100 per sqft, +$4k per bedroom, +$10k per floor, −$2k per year of age.');
    }
    A.bind(c, function () { render(lt); });
    var lt = 0; A.loop(c.cv, function (t) { lt = t; render(t); });
  });

  /* ============================================================
     2. Vectorisation
     ============================================================ */
  A.def('vectorization', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var ro = A.readout(root);
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var k = Math.floor((t * 1.3) % 6);
      var x = ROWS[0].slice(0, 4);
      /* the two vectors */
      A.txt(ctx, 'w', 96, 62, { align: 'center', size: 13, mono: true, w: 700, fill: P.b });
      A.matrix(ctx, 120, 44, 1, 4, 78, 40, P, function (i, j) { return String(W[j]); },
        { state: function (i, j) { return j === k && k < 4 ? 1 : 0; }, size: 12.5 });
      A.txt(ctx, 'x', 96, 118, { align: 'center', size: 13, mono: true, w: 700, fill: P.a });
      A.matrix(ctx, 120, 100, 1, 4, 78, 40, P, function (i, j) { return String(x[j]); },
        { state: function (i, j) { return j === k && k < 4 ? 1 : 0; }, size: 12.5 });
      /* the running sum */
      var terms = [], sum = 0;
      for (var i = 0; i < Math.min(k, 4); i++) { terms.push(W[i] + '×' + x[i]); sum += W[i] * x[i]; }
      A.txt(ctx, terms.length ? terms.join('  +  ') : '…', 120, 172,
        { size: 12.5, mono: true, fill: P.soft });
      if (k >= 4) {
        A.txt(ctx, '+ b = ' + B, 120, 196, { size: 12.5, mono: true, fill: P.soft });
        A.txt(ctx, '= ' + (sum + B).toFixed(1), 120, 224, { size: 18, mono: true, w: 700, fill: P.g });
      } else {
        A.txt(ctx, 'running total: ' + sum.toFixed(1), 120, 196, { size: 12.5, mono: true, fill: P.faint });
      }
      /* the three ways to write it */
      var ways = [
        ['without vectorisation', 'f = w[0]*x[0] + w[1]*x[1] + w[2]*x[2] + w[3]*x[3] + b', 'unreadable, and hopeless at n = 100', P.r],
        ['a for loop', 'f = 0\nfor j in range(n):\n    f = f + w[j] * x[j]\nf = f + b', 'readable, and slow', P.m],
        ['vectorised', 'f = np.dot(w, x) + b', 'short AND fast', P.g]
      ];
      ways.forEach(function (wy, i) {
        var y = 52 + i * 92;
        A.rr(ctx, 400, y, 320, 80, 9);
        ctx.fillStyle = wy[3] === P.g ? P.gS : P.sunk; ctx.fill();
        ctx.strokeStyle = wy[3]; ctx.lineWidth = wy[3] === P.g ? 2 : 1.2; ctx.stroke();
        A.txt(ctx, wy[0], 414, y + 18, { size: 11.5, w: 700, fill: wy[3] });
        wy[1].split('\n').forEach(function (ln, q) {
          A.txt(ctx, ln, 414, y + 36 + q * 12, { size: 9, mono: true, fill: P.soft });
        });
        A.txt(ctx, wy[2], 706, y + 72, { align: 'right', size: 9.5, fill: P.faint });
      });
      A.txt(ctx, 'All three compute exactly the same number. Only the third is worth writing.',
        40, 264, { size: 12.5, w: 700, fill: P.soft });
      A.txt(ctx, 'NumPy indexes from 0, but the maths indexes from 1. w₁ in a formula is w[0] in code —',
        40, 292, { size: 11.5, fill: P.faint });
      A.txt(ctx, 'a permanent, low-grade source of off-by-one bugs. Be deliberate about it.', 40, 310,
        { size: 11.5, fill: P.faint });
      ro.set('f<sub>w,b</sub>(x) = <b><span class="ov vec">w</span> · <span class="ov vec">x</span> + b</b>  =  np.dot(w, x) + b' +
        '\nThe dot product multiplies matching entries and adds them all up — exactly the weighted sum ' +
        'the model needs, in one operation.');
    }
    A.bind(c, function () { render(lt); });
    var lt = 0; A.loop(c.cv, function (t) { lt = t; render(t); });
  });

  /* ============================================================
     3. Why vectorisation is fast
     ============================================================ */
  A.def('vectorfast', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var N = 16;
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var cyc = (t * .5) % 2.1;
      var done = Math.min(N, Math.floor(cyc / (1.75 / N)));
      A.txt(ctx, 'the for loop — one multiplication per tick of the clock', 40, 40,
        { size: 12.5, w: 700, fill: P.r });
      for (var i = 0; i < N; i++) {
        var x = 44 + (i % 8) * 42, y = 56 + Math.floor(i / 8) * 40;
        A.rr(ctx, x, y, 36, 32, 5);
        ctx.fillStyle = i < done ? P.gS : i === done ? P.aS : P.sunk; ctx.fill();
        ctx.strokeStyle = i < done ? P.g : i === done ? P.a : P.lineSoft;
        ctx.lineWidth = i === done ? 2 : 1; ctx.stroke();
        A.txt(ctx, 'w' + i, x + 18, y + 14, { align: 'center', size: 9, mono: true, fill: P.faint });
        A.txt(ctx, '×x' + i, x + 18, y + 26, { align: 'center', size: 9, mono: true, fill: P.faint });
      }
      A.txt(ctx, 't = ' + done, 400, 84, { size: 14, mono: true, w: 700, fill: P.r });
      A.txt(ctx, done + ' of ' + N + ' done', 400, 106, { size: 11, fill: P.faint });
      /* vectorised */
      var allOn = cyc > 1.75;
      A.txt(ctx, 'np.dot — all of them in one go, then a specialised add-them-up circuit', 40, 168,
        { size: 12.5, w: 700, fill: P.g });
      for (i = 0; i < N; i++) {
        var x2 = 44 + (i % 8) * 42, y2 = 184 + Math.floor(i / 8) * 40;
        A.rr(ctx, x2, y2, 36, 32, 5);
        ctx.fillStyle = allOn ? P.gS : P.sunk; ctx.fill();
        ctx.strokeStyle = allOn ? P.g : P.lineSoft; ctx.lineWidth = allOn ? 2 : 1; ctx.stroke();
        A.txt(ctx, 'w' + i, x2 + 18, y2 + 14, { align: 'center', size: 9, mono: true, fill: P.faint });
        A.txt(ctx, '×x' + i, x2 + 18, y2 + 26, { align: 'center', size: 9, mono: true, fill: P.faint });
      }
      A.txt(ctx, 't = ' + (allOn ? 1 : 0), 400, 212, { size: 14, mono: true, w: 700, fill: P.g });
      A.txt(ctx, allOn ? 'all ' + N + ' at once' : 'waiting…', 400, 234, { size: 11, fill: P.faint });
      A.txt(ctx, 'Your computer has hardware that can multiply many pairs of numbers simultaneously.',
        40, 282, { size: 12, fill: P.soft });
      A.txt(ctx, 'A Python loop hands it one pair at a time, so almost all of that hardware sits idle.',
        40, 302, { size: 12, fill: P.soft });
      A.txt(ctx, 'This is also exactly why GPUs matter for machine learning.', 40, 322,
        { size: 12, w: 700, fill: P.a });
    }
    A.bind(c, function () { render(lt); });
    var lt = 0; A.loop(c.cv, function (t) { lt = t; render(t); });
  });

  /* ============================================================
     4. Gradient descent for multiple linear regression
     ============================================================ */
  A.def('gdmulti', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var ro = A.readout(root);
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var j = Math.floor((t * .7) % 5);
      A.txt(ctx, 'repeat until convergence — updating all n + 1 parameters simultaneously', 40, 40,
        { size: 12.5, w: 700, fill: P.soft });
      for (var q = 0; q < 4; q++) {
        var y = 62 + q * 44, on = q === j;
        A.rr(ctx, 40, y, 500, 36, 7);
        ctx.fillStyle = on ? P.aS : P.sunk; ctx.fill();
        ctx.strokeStyle = on ? P.a : P.lineSoft; ctx.lineWidth = on ? 2 : 1; ctx.stroke();
        A.txt(ctx, 'w' + (q + 1) + ' := w' + (q + 1) + ' − α · (1/m) Σ ( f(x⁽ⁱ⁾) − y⁽ⁱ⁾ ) · x' + (q + 1) + '⁽ⁱ⁾',
          56, y + 23, { size: 12.5, mono: true, w: on ? 700 : 500, fill: on ? P.a : P.soft });
      }
      var yb = 62 + 4 * 44, onb = j === 4;
      A.rr(ctx, 40, yb, 500, 36, 7);
      ctx.fillStyle = onb ? P.aS : P.sunk; ctx.fill();
      ctx.strokeStyle = onb ? P.a : P.lineSoft; ctx.lineWidth = onb ? 2 : 1; ctx.stroke();
      A.txt(ctx, 'b  := b  − α · (1/m) Σ ( f(x⁽ⁱ⁾) − y⁽ⁱ⁾ )', 56, yb + 23,
        { size: 12.5, mono: true, w: onb ? 700 : 500, fill: onb ? P.a : P.soft });
      A.txt(ctx, 'notice', 570, 82, { size: 12, w: 700, fill: P.faint });
      ['every line is identical', 'except for the x_j at the end', '', 'the b line has no x at all',
       '(you can think of it as', 'x₀ = 1, always)'
      ].forEach(function (l, i) {
        A.txt(ctx, l, 570, 104 + i * 20, { size: 10.5, fill: P.faint });
      });
      A.txt(ctx, 'in code, all of it is two lines:', 40, 262, { size: 12, fill: P.faint });
      A.txt(ctx, 'w = w - alpha * (1/m) * np.dot(err, X)', 40, 286,
        { size: 13, mono: true, w: 700, fill: P.g });
      A.txt(ctx, 'b = b - alpha * (1/m) * np.sum(err)', 40, 308,
        { size: 13, mono: true, w: 700, fill: P.g });
      ro.set('There is an alternative for linear regression only: the <b>normal equation</b>, which solves ' +
        'for w and b in one shot with no iterations and no α.' +
        '\nIt does not generalise to any other algorithm, it is slow when n is large (roughly n³), and ' +
        'scikit-learn may use it internally without telling you. Worth knowing it exists; not worth ' +
        'reaching for.');
    }
    A.bind(c, function () { render(lt); });
    var lt = 0; A.loop(c.cv, function (t) { lt = t; render(t); });
  });

  /* ============================================================
     5. Feature scaling
     ============================================================ */
  A.def('featurescaling', function (root) {
    var c = A.canvas(root, 760, 350), ctx = c.ctx;
    var scaled = false, method = 2;
    var bar = A.ctrls(root), ro = A.readout(root);
    A.toggle(bar, 'apply scaling', function (v) { scaled = v; render(); }, false);
    ['divide by max', 'mean normalisation', 'z-score'].forEach(function (n, i) {
      A.button(bar, n, function () { method = i; scaled = true; sync(); render(); });
    });
    function sync() {
      var bs = bar.querySelectorAll('button');
      bs[0].classList.toggle('primary', scaled);
      for (var i = 1; i < 4; i++) bs[i].classList.toggle('primary', scaled && method === i - 1);
    }
    function render() {
      var P = A.pal(); c.clear(P.panel);
      /* contours of a quadratic cost with very different curvatures */
      var ratio = scaled ? 1 : 26;
      var box = { x: 70, y: 52, w: 300, h: 220 };
      var S = A.axes(ctx, box, [-3, 3], [-3, 3], {
        xticks: 4, yticks: 4, xlab: 'w₁ (size)', ylab: 'w₂ (bedrooms)'
      });
      for (var L = 0.12; L < 12; L *= 1.9) {
        ctx.save(); ctx.strokeStyle = P.lineSoft; ctx.lineWidth = 1.1; ctx.beginPath();
        for (var th = 0; th <= 6.3; th += .05) {
          var xx = Math.sqrt(2 * L / (1 / ratio)) * Math.cos(th) * .16;
          var yy = Math.sqrt(2 * L * ratio) * Math.sin(th) * .16;
          var px = S.X(A.clamp(xx, -3.4, 3.4)), py = S.Y(A.clamp(yy, -3.4, 3.4));
          th === 0 ? ctx.moveTo(px, py) : ctx.lineTo(px, py);
        }
        ctx.closePath(); ctx.stroke(); ctx.restore();
      }
      /* a gradient-descent path across it */
      var wx = -2.4, wy = 2.2, al = scaled ? .28 : .0075;
      ctx.save(); ctx.strokeStyle = P.a; ctx.lineWidth = 1.8; ctx.beginPath();
      ctx.moveTo(S.X(wx), S.Y(wy));
      for (var n = 0; n < 90; n++) {
        wx -= al * (1 / ratio) * wx * 39; wy -= al * ratio * wy * 1.5;
        if (!isFinite(wx) || Math.abs(wx) > 9) break;
        ctx.lineTo(S.X(A.clamp(wx, -3.2, 3.2)), S.Y(A.clamp(wy, -3.2, 3.2)));
      }
      ctx.stroke(); ctx.restore();
      A.dot(ctx, S.X(0), S.Y(0), 5, P.g);
      A.txt(ctx, scaled ? 'round bowl → a direct path' : 'squashed bowl → it zig-zags',
        box.x + box.w / 2, 40, { align: 'center', size: 12.5, w: 700, fill: scaled ? P.g : P.r });
      /* the ranges */
      A.txt(ctx, 'feature ranges', 545, 52, { align: 'center', size: 12.5, w: 700, fill: P.soft });
      var ranges = scaled
        ? [['x₁ size', method === 2 ? '−0.7 … 1.9' : method === 1 ? '−0.5 … 0.5' : '0.25 … 1'],
           ['x₂ beds', method === 2 ? '−1.4 … 1.6' : method === 1 ? '−0.5 … 0.5' : '0.4 … 1']]
        : [['x₁ size', '300 … 2000'], ['x₂ beds', '0 … 5']];
      ranges.forEach(function (r, i) {
        var y = 84 + i * 54;
        A.txt(ctx, r[0], 430, y + 14, { size: 12, mono: true, fill: P.soft });
        A.txt(ctx, r[1], 700, y + 14, { align: 'right', size: 12, mono: true, w: 700,
          fill: scaled ? P.g : P.r });
        var frac = scaled ? .82 : (i === 0 ? 1 : .0029);
        A.rr(ctx, 430, y + 22, 270, 12, 4); ctx.fillStyle = P.sunk; ctx.fill();
        A.rr(ctx, 430, y + 22, Math.max(3, 270 * frac), 12, 4);
        ctx.fillStyle = scaled ? P.g : P.r; ctx.globalAlpha = .8; ctx.fill(); ctx.globalAlpha = 1;
      });
      var formulas = [
        ['divide by max', 'x₁ := x₁ / 2000', 'lands in 0 … 1'],
        ['mean normalisation', 'x₁ := (x₁ − μ₁) / (max − min)', 'centred on 0, roughly −0.5 … 0.5'],
        ['z-score', 'x₁ := (x₁ − μ₁) / σ₁', 'mean 0, standard deviation 1 — the usual choice']
      ];
      var f = formulas[scaled ? method : 2];
      A.txt(ctx, f[0], 430, 208, { size: 12, w: 700, fill: P.a });
      A.txt(ctx, f[1], 430, 230, { size: 12.5, mono: true, fill: P.soft });
      A.txt(ctx, f[2], 430, 250, { size: 10.5, fill: P.faint });
      A.txt(ctx, 'A feature ranging 300–2000 next to one ranging 0–5 makes the cost surface a long thin canyon.',
        70, 300, { size: 12, fill: P.soft });
      A.txt(ctx, 'Gradient descent then bounces across the canyon instead of running down it. Aim for roughly −1 … 1.',
        70, 320, { size: 12, w: 700, fill: P.a });
      A.txt(ctx, 'Rules of thumb: −3…3 is fine, −0.3…0.3 is fine. 0…0.001 or −100…100 needs rescaling.',
        70, 342, { size: 11, fill: P.faint });
      ro.set('Compute μ and σ on the <b>training set only</b>, then apply the same numbers to every future ' +
        'example — including at prediction time.' +
        '\nForgetting to scale a new input the same way is one of the most common production bugs there is.');
    }
    sync(); A.bind(c, render); render();
  });

  /* ============================================================
     6. Checking for convergence
     ============================================================ */
  A.def('convergence', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var which = 0;
    var bar = A.ctrls(root), ro = A.readout(root);
    ['healthy', 'α too large', 'a bug'].forEach(function (n, i) {
      A.button(bar, n, function () { which = i; sync(); render(); });
    });
    function sync() { bar.querySelectorAll('button').forEach(function (b, i) { b.classList.toggle('primary', i === which); }); }
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var box = { x: 80, y: 50, w: 600, h: 200 };
      var S = A.axes(ctx, box, [0, 400], [0, 1.15], {
        xticks: 4, yticks: 4, xfmt: function (v) { return v.toFixed(0); },
        yfmt: function (v) { return v.toFixed(1); },
        xlab: 'iterations', ylab: 'J(w, b)'
      });
      var f = which === 0 ? function (i) { return 0.06 + 0.94 * Math.exp(-i / 55); }
        : which === 1 ? function (i) { return 0.5 + 0.45 * Math.sin(i / 9) * (1 + i / 500); }
        : function (i) { return 0.2 + 0.75 * (i / 400); };
      A.plot(ctx, S, [0, 400], function (i) { return A.clamp(f(i), 0, 1.15); },
        which === 0 ? P.g : P.r, 2.8);
      if (which === 0) {
        A.line(ctx, box.x, S.Y(0.06), box.x + box.w, S.Y(0.06), P.faint, 1.4, [5, 4]);
        A.txt(ctx, 'flattening out — it has converged', S.X(250), S.Y(0.16),
          { size: 11.5, w: 700, fill: P.g });
      }
      var msg = [
        ['✓ healthy', P.g, 'J falls on every iteration and flattens. This is what you want to see.'],
        ['✗ α is too large', P.r, 'J oscillates or grows. Halve α and try again — this is almost always the cause.'],
        ['✗ J is increasing steadily', P.r, 'Either α is far too large, or there is a bug — a plus sign where a minus should be.']
      ][which];
      A.txt(ctx, msg[0], 80, 280, { size: 15, w: 700, fill: msg[1] });
      A.txt(ctx, msg[2], 80, 302, { size: 12, fill: P.soft });
      A.txt(ctx, 'The number of iterations needed varies enormously between problems — 30, 1,000, 100,000.',
        80, 324, { size: 11, fill: P.faint });
      ro.set('Plot J against iterations. Always. It is the single cheapest diagnostic in machine learning ' +
        'and it takes three lines of matplotlib.' +
        '\nAn automatic test — “declare convergence when J falls by less than ε = 0.001 in one iteration” — ' +
        'exists, but choosing ε is hard and Andrew says he prefers looking at the graph.');
    }
    sync(); A.bind(c, render); render();
  });

  /* ============================================================
     7. Choosing the learning rate
     ============================================================ */
  A.def('alphachoice', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var ro = A.readout(root);
    var trials = [
      { a: 0.001, col: null, rate: 420 }, { a: 0.003, col: null, rate: 190 },
      { a: 0.01, col: null, rate: 62 }, { a: 0.03, col: null, rate: 24 },
      { a: 0.1, col: null, rate: -1 }
    ];
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var cols = [P.faint, P.b, P.g, P.p, P.r];
      var box = { x: 80, y: 54, w: 420, h: 210 };
      var S = A.axes(ctx, box, [0, 200], [0, 1.2], {
        xticks: 4, yticks: 4, xfmt: function (v) { return v.toFixed(0); },
        yfmt: function (v) { return v.toFixed(1); }, xlab: 'iterations', ylab: 'J'
      });
      var hot = Math.floor((t * .5) % trials.length);
      trials.forEach(function (tr, i) {
        var f = tr.rate < 0
          ? function (x) { return A.clamp(0.5 + 0.55 * Math.sin(x / 6) * (1 + x / 90), 0, 1.2); }
          : function (x) { return 0.05 + 0.95 * Math.exp(-x / tr.rate); };
        A.plot(ctx, S, [0, 200], f, i === hot ? cols[i] : P.lineSoft, i === hot ? 2.8 : 1.4);
      });
      trials.forEach(function (tr, i) {
        var y = 62 + i * 40, on = i === hot;
        A.rr(ctx, 530, y, 190, 34, 6);
        ctx.fillStyle = on ? (tr.rate < 0 ? P.rS : P.gS) : P.sunk; ctx.fill();
        ctx.strokeStyle = on ? cols[i] : P.lineSoft; ctx.lineWidth = on ? 2 : 1; ctx.stroke();
        A.txt(ctx, 'α = ' + tr.a, 544, y + 22, { size: 12.5, mono: true, w: on ? 700 : 500,
          fill: on ? cols[i] : P.soft });
        A.txt(ctx, tr.rate < 0 ? 'diverges' : tr.rate > 300 ? 'far too slow' : tr.rate > 100 ? 'slow' : 'good',
          706, y + 22, { align: 'right', size: 10.5, fill: on ? cols[i] : P.faint });
      });
      A.txt(ctx, 'try a ladder of values, roughly ×3 apart, and plot J for each', 80, 40,
        { size: 12.5, w: 700, fill: P.soft });
      A.txt(ctx, 'Pick the LARGEST α that still gives a smooth decrease. Then, if you like, one more notch down.',
        80, 292, { size: 12, w: 700, fill: P.a });
      A.txt(ctx, 'Debugging trick: set α to something tiny like 0.0001. If J still does not fall, it is not α — it is a bug.',
        80, 314, { size: 11.5, fill: P.faint });
      ro.set('0.001 · 0.003 · 0.01 · 0.03 · 0.1 · 0.3 · 1 — the ladder Andrew suggests.' +
        '\nToo small wastes your time; too large diverges. There is usually a comfortable range of a ' +
        'factor of ten in between, so you do not need to be precise.');
    }
    A.bind(c, function () { render(lt); });
    var lt = 0; A.loop(c.cv, function (t) { lt = t; render(t); });
  });

  /* ============================================================
     8. Feature engineering
     ============================================================ */
  A.def('featureeng', function (root) {
    var c = A.canvas(root, 760, 320), ctx = c.ctx;
    var ro = A.readout(root);
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var phase = A.clamp(((t * .4) % 3) - .4, 0, 1);
      /* the plot of land */
      A.txt(ctx, 'a plot of land', 170, 42, { align: 'center', size: 12.5, w: 700, fill: P.soft });
      var w = 150, h = 100, x0 = 95, y0 = 62;
      A.rr(ctx, x0, y0, w, h, 6);
      ctx.fillStyle = P.a; ctx.globalAlpha = .1 + .3 * phase; ctx.fill(); ctx.globalAlpha = 1;
      ctx.strokeStyle = P.a; ctx.lineWidth = 2; ctx.stroke();
      A.arrow(ctx, x0, y0 - 12, x0 + w, y0 - 12, P.b, 1.6);
      A.txt(ctx, 'x₁ = frontage', x0 + w / 2, y0 - 20, { align: 'center', size: 11, w: 700, fill: P.b });
      A.arrow(ctx, x0 - 14, y0, x0 - 14, y0 + h, P.g, 1.6);
      ctx.save(); ctx.translate(x0 - 26, y0 + h / 2); ctx.rotate(-Math.PI / 2);
      A.txt(ctx, 'x₂ = depth', 0, 0, { align: 'center', size: 11, w: 700, fill: P.g }); ctx.restore();
      if (phase > .3) A.txt(ctx, 'x₃ = area', x0 + w / 2, y0 + h / 2 + 5,
        { align: 'center', size: 14, w: 700, fill: P.a });
      /* the models */
      A.txt(ctx, 'the obvious model', 480, 42, { size: 12.5, w: 700, fill: P.faint });
      A.txt(ctx, 'f = w₁·frontage + w₂·depth + b', 480, 66, { size: 13, mono: true, fill: P.soft });
      A.txt(ctx, 'it can add them. It cannot multiply them.', 480, 86, { size: 10.5, fill: P.faint });
      if (phase > .3) {
        A.txt(ctx, 'the engineered model', 480, 126, { size: 12.5, w: 700, fill: P.a });
        A.txt(ctx, 'x₃ = frontage × depth', 480, 150, { size: 13, mono: true, w: 700, fill: P.a });
        A.txt(ctx, 'f = w₁·frontage + w₂·depth', 480, 174, { size: 13, mono: true, fill: P.soft });
        A.txt(ctx, '    + w₃·area + b', 480, 194, { size: 13, mono: true, w: 700, fill: P.a });
        A.txt(ctx, 'now it can use the area — which is what actually', 480, 218, { size: 10.5, fill: P.faint });
        A.txt(ctx, 'determines what a plot of land is worth.', 480, 234, { size: 10.5, fill: P.faint });
      }
      A.txt(ctx, 'Feature engineering: using your knowledge of the problem to invent new features that make',
        60, 272, { size: 12, fill: P.soft });
      A.txt(ctx, 'the pattern easy for the model to express.', 60, 290, { size: 12, w: 700, fill: P.a });
      A.txt(ctx, 'It was the main lever in classical ML. Neural networks reduce the need for it, and do not remove it.',
        60, 310, { size: 11, fill: P.faint });
      ro.set('The model can only combine features the way its formula allows — here, by adding them. ' +
        'Anything else you want it to use, you must <b>hand it directly</b>.' +
        '\nRatios, differences, products, logs, counts per unit time — these are where domain knowledge ' +
        'enters a machine learning system.');
    }
    A.bind(c, function () { render(lt); });
    var lt = 0; A.loop(c.cv, function (t) { lt = t; render(t); });
  });

  /* ============================================================
     9. Polynomial regression
     ============================================================ */
  A.def('polyreg', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var mode = 1;
    var bar = A.ctrls(root), ro = A.readout(root);
    ['w₁x + b', 'w₁x + w₂x² + b', 'w₁x + w₂x² + w₃x³ + b', 'w₁√x + b'].forEach(function (n, i) {
      A.button(bar, n, function () { mode = i; sync(); render(); });
    });
    function sync() { bar.querySelectorAll('button').forEach(function (b, i) { b.classList.toggle('primary', i === mode); }); }
    var D = [];
    (function () {
      for (var i = 0; i < 22; i++) {
        var x = .3 + i * .17;
        D.push({ x: x, y: 120 * Math.sqrt(x) + 40 + Math.sin(i * 5.1) * 12 });
      }
    })();
    /* least squares over a chosen basis */
    function fit(basis) {
      var k = basis.length, A2 = [], b2 = [], i, j, q;
      for (i = 0; i < k; i++) {
        A2.push(new Array(k).fill(0)); b2.push(0);
        for (j = 0; j < k; j++) for (q = 0; q < D.length; q++) A2[i][j] += basis[i](D[q].x) * basis[j](D[q].x);
        for (q = 0; q < D.length; q++) b2[i] += basis[i](D[q].x) * D[q].y;
      }
      /* gaussian elimination */
      var Mx = A2.map(function (r, ri) { return r.slice().concat([b2[ri]]); });
      for (i = 0; i < k; i++) {
        var p = i;
        for (j = i + 1; j < k; j++) if (Math.abs(Mx[j][i]) > Math.abs(Mx[p][i])) p = j;
        var tm = Mx[i]; Mx[i] = Mx[p]; Mx[p] = tm;
        if (Math.abs(Mx[i][i]) < 1e-12) Mx[i][i] = 1e-12;
        for (j = i + 1; j < k; j++) {
          var f2 = Mx[j][i] / Mx[i][i];
          for (q = i; q <= k; q++) Mx[j][q] -= f2 * Mx[i][q];
        }
      }
      var sol = new Array(k);
      for (i = k - 1; i >= 0; i--) {
        var s = Mx[i][k];
        for (j = i + 1; j < k; j++) s -= Mx[i][j] * sol[j];
        sol[i] = s / Mx[i][i];
      }
      return sol;
    }
    var BASES = [
      [function () { return 1; }, function (x) { return x; }],
      [function () { return 1; }, function (x) { return x; }, function (x) { return x * x; }],
      [function () { return 1; }, function (x) { return x; }, function (x) { return x * x; }, function (x) { return x * x * x; }],
      [function () { return 1; }, function (x) { return Math.sqrt(x); }]
    ];
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var basis = BASES[mode], co = fit(basis);
      function f(x) { var s = 0; for (var i = 0; i < basis.length; i++) s += co[i] * basis[i](x); return s; }
      var box = { x: 80, y: 46, w: 420, h: 210 };
      var S = A.axes(ctx, box, [0, 4.2], [0, 340], {
        xticks: 4, yticks: 4, xfmt: function (v) { return v.toFixed(1); },
        yfmt: function (v) { return v.toFixed(0); }, xlab: 'size x', ylab: 'price'
      });
      A.plot(ctx, S, [0.05, 4.2], function (x) { return A.clamp(f(x), -50, 400); }, P.a, 2.8);
      D.forEach(function (p) { A.dot(ctx, S.X(p.x), S.Y(p.y), 4.4, P.b); });
      var err = 0; D.forEach(function (p) { var e = f(p.x) - p.y; err += e * e; });
      err /= (2 * D.length);
      A.txt(ctx, 'J = ' + err.toFixed(1), 540, 74, { size: 16, mono: true, w: 700, fill: P.a });
      var note = [
        'a straight line cannot bend at all',
        'better — but a parabola eventually turns DOWN, which is nonsense for house prices',
        'a cubic keeps rising, and fits well',
        'a square root: rises fast then flattens. Often the most natural shape here'
      ][mode];
      var words = note.split(' '), line = '', ln = 0;
      words.forEach(function (wd) {
        if ((line + wd).length > 26) {
          A.txt(ctx, line, 540, 106 + ln * 18, { size: 11, fill: P.soft }); line = wd + ' '; ln++;
        } else line += wd + ' ';
      });
      A.txt(ctx, line, 540, 106 + ln * 18, { size: 11, fill: P.soft });
      A.txt(ctx, 'It is still LINEAR regression — linear in the parameters w, not in x.', 80, 284,
        { size: 12.5, w: 700, fill: P.soft });
      A.txt(ctx, 'You are not changing the algorithm. You are handing it x² and x³ as extra features.',
        80, 304, { size: 12, fill: P.faint });
      A.txt(ctx, 'Which makes feature scaling essential: if x is 1–1000, then x³ is 1–1,000,000,000.',
        80, 324, { size: 12, w: 700, fill: P.r });
      ro.set('Polynomial regression = linear regression on engineered features x², x³, √x.' +
        '\nChoosing which powers to include is a modelling decision. Course 2 Week 3 gives you the tools ' +
        '(train/cross-validation split, bias and variance) to make it from evidence rather than taste.');
    }
    sync(); A.bind(c, render); render();
  });

})();
