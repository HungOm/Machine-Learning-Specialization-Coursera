/* Widgets for Course 1 / Week 1 — intro, linear regression, gradient descent */
(function () {
  'use strict';

  /* houses: size in 1000 sqft -> price in $1000s */
  var HOUSE = [
    { x: 1.0, y: 300 }, { x: 1.4, y: 355 }, { x: 1.9, y: 445 }, { x: 2.1, y: 500 },
    { x: 2.6, y: 545 }, { x: 3.0, y: 640 }, { x: 3.4, y: 690 }, { x: 3.9, y: 795 }
  ];
  var M = HOUSE.length;
  function cost(w, b, D) {
    D = D || HOUSE;
    var s = 0;
    D.forEach(function (p) { var e = w * p.x + b - p.y; s += e * e; });
    return s / (2 * D.length);
  }
  /* closed-form least squares, for the "correct answer" marker */
  var FIT = (function () {
    var sx = 0, sy = 0, sxx = 0, sxy = 0;
    HOUSE.forEach(function (p) { sx += p.x; sy += p.y; sxx += p.x * p.x; sxy += p.x * p.y; });
    var w = (M * sxy - sx * sy) / (M * sxx - sx * sx);
    return { w: w, b: (sy - w * sx) / M };
  })();
  /* second-derivative matrix of J, used to draw exact elliptical contours */
  var HESS = (function () {
    var A = 0, B = 0;
    HOUSE.forEach(function (p) { A += p.x * p.x; B += p.x; });
    return { A: A / M, B: B / M };
  })();
  function eig() {
    var A = HESS.A, B = HESS.B, tr = A + 1, det = A - B * B;
    var disc = Math.sqrt(Math.max(0, tr * tr / 4 - det));
    var l1 = tr / 2 + disc, l2 = tr / 2 - disc;
    function vec(l) {
      var vx = B, vy = l - A;
      if (Math.abs(vx) < 1e-9 && Math.abs(vy) < 1e-9) { vx = 1; vy = 0; }
      var n = Math.hypot(vx, vy);
      return [vx / n, vy / n];
    }
    return { l1: l1, l2: l2, u1: vec(l1), u2: vec(l2) };
  }
  var EIG = eig();
  function contour(ctx, S, level, colr, lw) {
    var Jm = cost(FIT.w, FIT.b);
    var L = level - Jm;
    if (L <= 0) return;
    ctx.save(); ctx.strokeStyle = colr; ctx.lineWidth = lw || 1; ctx.beginPath();
    var r1 = Math.sqrt(2 * L / EIG.l1), r2 = Math.sqrt(2 * L / EIG.l2);
    for (var t = 0; t <= 6.2832 + .05; t += .05) {
      var dw = EIG.u1[0] * r1 * Math.cos(t) + EIG.u2[0] * r2 * Math.sin(t);
      var db = EIG.u1[1] * r1 * Math.cos(t) + EIG.u2[1] * r2 * Math.sin(t);
      var px = S.X(FIT.w + dw), py = S.Y(FIT.b + db);
      t === 0 ? ctx.moveTo(px, py) : ctx.lineTo(px, py);
    }
    ctx.closePath(); ctx.stroke(); ctx.restore();
  }

  /* ============================================================
     1. What is machine learning?
     ============================================================ */
  A.def('whatisml', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var ro = A.readout(root);
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var game = Math.floor((t * .6) % 6);
      A.txt(ctx, '“the field of study that gives computers the ability to learn', 40, 40,
        { size: 14, w: 700, fill: P.soft });
      A.txt(ctx, 'without being explicitly programmed”  — Arthur Samuel, 1959', 40, 62,
        { size: 14, w: 700, fill: P.soft });
      /* a little checkerboard, playing itself */
      A.txt(ctx, 'Samuel’s checkers program played itself tens of thousands of times', 40, 96,
        { size: 12, fill: P.faint });
      for (var r = 0; r < 4; r++) for (var q = 0; q < 4; q++) {
        var x = 44 + q * 32, y = 110 + r * 32;
        ctx.fillStyle = (r + q) % 2 ? P.sunk : P.line;
        ctx.fillRect(x, y, 32, 32);
      }
      var pcs = [[0, 0], [2, 0], [1, 3], [3, 3]];
      pcs.forEach(function (p, i) {
        var off = i < 2 ? Math.sin(t * 1.2 + i) * 6 : 0;
        A.dot(ctx, 44 + p[0] * 32 + 16 + off, 110 + p[1] * 32 + 16, 11, i < 2 ? P.a : P.b);
      });
      A.txt(ctx, 'game ' + (10000 + game * 4137).toLocaleString(), 44, 262,
        { size: 11.5, mono: true, fill: P.faint });
      A.txt(ctx, 'it ended up better than Samuel himself', 44, 280, { size: 11.5, w: 700, fill: P.a });
      /* the two branches */
      [['SUPERVISED learning', 'you are given the right answers', 'x → y', P.b,
        ['house size → price', 'email → spam or not', 'image → “is there a cat?”']],
       ['UNSUPERVISED learning', 'no answers — find structure yourself', 'x only', P.a,
        ['group customers into segments', 'spot the unusual server', 'squash 50 features into 2']]
      ].forEach(function (br, i) {
        var x = 250 + i * 250;
        A.rr(ctx, x, 110, 230, 170, 10);
        ctx.fillStyle = br[3] === P.b ? P.bS : P.aS; ctx.fill();
        ctx.strokeStyle = br[3]; ctx.lineWidth = 1.8; ctx.stroke();
        A.txt(ctx, br[0], x + 115, 136, { align: 'center', size: 13, w: 700, fill: br[3] });
        A.txt(ctx, br[1], x + 115, 156, { align: 'center', size: 10.5, fill: br[3] });
        A.txt(ctx, br[2], x + 115, 180, { align: 'center', size: 15, mono: true, w: 700, fill: br[3] });
        br[4].forEach(function (e, k) {
          A.txt(ctx, '· ' + e, x + 16, 210 + k * 22, { size: 11, fill: P.soft });
        });
      });
      A.txt(ctx, 'These two account for essentially everything in this specialization. Supervised learning is by far',
        250, 302, { size: 11.5, fill: P.faint });
      A.txt(ctx, 'the more used of the two, and it is what Courses 1 and 2 are about.', 250, 320,
        { size: 11.5, w: 700, fill: P.b });
      ro.set('The practical definition: <b>a program learns from experience E at task T, measured by ' +
        'performance P, if its performance at T improves with more E</b> (Tom Mitchell, 1997).' +
        '\nThe useful version: you show it examples instead of writing the rules.');
    }
    A.autoplay(root, c, render);
  });

  /* ============================================================
     2. Supervised learning
     ============================================================ */
  A.def('supervised', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var mode = 0;
    var bar = A.ctrls(root), ro = A.readout(root);
    ['regression — predict a number', 'classification — predict a category'].forEach(function (n, i) {
      A.button(bar, n, function () { mode = i; sync(); render(); });
    });
    function sync() { bar.querySelectorAll('button').forEach(function (b, i) { b.classList.toggle('primary', i === mode); }); }
    var TUM = [];
    (function () {
      for (var i = 0; i < 18; i++) {
        var s = Math.sin(i * 7.3) * .5 + .5;
        TUM.push({ x: .4 + s * 4.6 + (i % 3) * .18, y: (.4 + s * 4.6) > 2.6 ? 1 : 0 });
      }
      TUM[7].y = 1; TUM[11].y = 0;
    })();
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      if (mode === 0) {
        var box = { x: 80, y: 48, w: 400, h: 210 };
        var S = A.axes(ctx, box, [0, 4.4], [0, 900], {
          xticks: 4, yticks: 4, xfmt: function (v) { return v.toFixed(1); },
          yfmt: function (v) { return v.toFixed(0); },
          xlab: 'house size (1000 sqft)', ylab: 'price ($1000s)'
        });
        A.plot(ctx, S, [0, 4.4], function (x) { return FIT.w * x + FIT.b; }, P.a, 2.4);
        HOUSE.forEach(function (p) { A.dot(ctx, S.X(p.x), S.Y(p.y), 5, P.b); });
        var qx = 2.2 + Math.sin(t * .5) * 1.4, qy = FIT.w * qx + FIT.b;
        A.line(ctx, S.X(qx), S.Y(0), S.X(qx), S.Y(qy), P.g, 1.6, [4, 3]);
        A.line(ctx, box.x, S.Y(qy), S.X(qx), S.Y(qy), P.g, 1.6, [4, 3]);
        A.dot(ctx, S.X(qx), S.Y(qy), 7, P.g);
        A.txt(ctx, '$' + qy.toFixed(0) + 'k', S.X(qx) + 10, S.Y(qy) - 10,
          { size: 13, mono: true, w: 700, fill: P.g });
        A.txt(ctx, 'REGRESSION', 620, 74, { align: 'center', size: 15, w: 700, fill: P.a });
        ['predict a NUMBER', 'from infinitely many', 'possible values', '',
         'house price', 'tomorrow’s temperature', 'how long a repair takes'
        ].forEach(function (l, i) {
          A.txt(ctx, l, 620, 104 + i * 22, { align: 'center', size: 11.5,
            fill: i < 3 ? P.soft : P.faint });
        });
      } else {
        var box2 = { x: 80, y: 60, w: 400, h: 180 };
        var S2 = A.axes(ctx, box2, [0, 5.4], [-0.35, 1.35], {
          xticks: 5, yticks: 2, xfmt: function (v) { return v.toFixed(0); },
          yfmt: function (v) { return v.toFixed(0); },
          xlab: 'tumour size (cm)', ylab: 'malignant?'
        });
        TUM.forEach(function (p) {
          A.dot(ctx, S2.X(p.x), S2.Y(p.y), 5.5, p.y ? P.r : P.b);
        });
        A.line(ctx, S2.X(2.75), box2.y, S2.X(2.75), box2.y + box2.h, P.a, 2, [5, 3]);
        A.txt(ctx, 'boundary', S2.X(2.75) + 8, box2.y + 16, { size: 11, w: 700, fill: P.a });
        A.txt(ctx, 'benign (0)', box2.x + 10, S2.Y(0) - 10, { size: 11, fill: P.b });
        A.txt(ctx, 'malignant (1)', box2.x + 10, S2.Y(1) - 10, { size: 11, fill: P.r });
        A.txt(ctx, 'CLASSIFICATION', 620, 74, { align: 'center', size: 15, w: 700, fill: P.a });
        ['predict a CATEGORY', 'from a small fixed set', 'of possible answers', '',
         'benign or malignant', 'spam or not spam', 'which of 10 digits'
        ].forEach(function (l, i) {
          A.txt(ctx, l, 620, 104 + i * 22, { align: 'center', size: 11.5,
            fill: i < 3 ? P.soft : P.faint });
        });
        A.txt(ctx, 'the categories need not be numbers, and 0/1 is just a convenient label',
          80, 268, { size: 11, fill: P.faint });
      }
      A.txt(ctx, 'Both are supervised: every training example arrives with its correct answer y attached.',
        80, 300, { size: 12.5, w: 700, fill: P.soft });
      A.txt(ctx, 'The algorithm learns the mapping x → y by being shown many (x, y) pairs.', 80, 320,
        { size: 12, fill: P.faint });
      ro.set('<b>Regression</b>: infinitely many possible outputs (any number). ' +
        '<b>Classification</b>: a small, finite set of categories.' +
        '\nThat single distinction decides the model, the cost function and the metric — it is the first ' +
        'question to ask about any new problem.');
    }
    sync();
    A.autoplay(root, c, render);
  });

  /* ============================================================
     3. Unsupervised learning
     ============================================================ */
  A.def('unsupervised', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var phase = Math.floor((t * .35) % 3);
      var panels = [
        { n: 'CLUSTERING', s: 'group things that belong together', e: 'Google News grouping the same story · DNA microarrays · customer segments' },
        { n: 'ANOMALY DETECTION', s: 'find the odd one out', e: 'fraudulent transactions · a failing engine · an intruder in server logs' },
        { n: 'DIMENSIONALITY REDUCTION', s: 'squash it smaller without losing much', e: 'compress 50 features to 2 so a human can plot them' }
      ];
      panels.forEach(function (pn, i) {
        var x = 30 + i * 245, on = i === phase;
        A.rr(ctx, x, 44, 225, 214, 10);
        ctx.fillStyle = on ? P.aS : P.sunk; ctx.fill();
        ctx.strokeStyle = on ? P.a : P.lineSoft; ctx.lineWidth = on ? 2.2 : 1.2; ctx.stroke();
        A.txt(ctx, pn.n, x + 112, 68, { align: 'center', size: 12, w: 700, fill: on ? P.a : P.faint });
        A.txt(ctx, pn.s, x + 112, 86, { align: 'center', size: 10.5, fill: P.faint });
        /* a little picture per panel */
        var cx = x + 112, cy = 158;
        if (i === 0) {
          [[-40, -22, P.a], [40, -18, P.b], [0, 30, P.g]].forEach(function (g) {
            for (var k = 0; k < 7; k++) {
              var a2 = k * 2.4, rr = 12 + (k % 3) * 7;
              A.dot(ctx, cx + g[0] + Math.cos(a2) * rr, cy + g[1] + Math.sin(a2) * rr, 3.4,
                on ? g[2] : P.faint);
            }
          });
        } else if (i === 1) {
          for (var k2 = 0; k2 < 26; k2++) {
            var a3 = k2 * 1.7, r3 = 8 + (k2 % 5) * 6;
            A.dot(ctx, cx + Math.cos(a3) * r3, cy + Math.sin(a3) * r3 * .8, 3.2, P.faint);
          }
          A.dot(ctx, cx + 62, cy - 34, 6, on ? P.r : P.faint);
          if (on) {
            ctx.save(); ctx.strokeStyle = P.r; ctx.lineWidth = 1.6; ctx.setLineDash([3, 3]);
            ctx.beginPath(); ctx.arc(cx + 62, cy - 34, 12, 0, 6.2832); ctx.stroke(); ctx.restore();
          }
        } else {
          for (var k3 = 0; k3 < 16; k3++) {
            var u = -1 + 2 * k3 / 15;
            A.dot(ctx, cx + u * 62, cy - 26 + u * 22 + Math.sin(k3 * 3.1) * 6, 3.4, P.faint);
            if (on) A.dot(ctx, cx + u * 62, cy + 34, 3.4, P.a);
          }
          if (on) A.line(ctx, cx - 68, cy + 34, cx + 68, cy + 34, P.a, 1.4);
        }
        /* the bulleted list below is the only rendering — a leftover single-line version of
           the same string used to be drawn here too and overflowed across panel boundaries */
        var words = pn.e.split(' · ');
        words.forEach(function (wd, k) {
          A.txt(ctx, '· ' + wd, x + 12, 206 + k * 15, { size: 9.5, fill: on ? P.soft : P.faint });
        });
      });
      A.txt(ctx, 'No y anywhere. Nobody says which news stories go together — the algorithm works it out.',
        30, 286, { size: 12.5, w: 700, fill: P.soft });
      A.txt(ctx, 'Course 3 covers all three of these properly. This lesson is just the map.',
        30, 308, { size: 12, fill: P.faint });
    }
    A.autoplay(root, c, render);
  });

  /* ============================================================
     4. The linear regression model
     ============================================================ */
  A.def('linreg', function (root) {
    var c = A.canvas(root, 760, 340), ctx = c.ctx;
    var w = 120, b = 120;
    var bar = A.ctrls(root), ro = A.readout(root);
    A.slider(bar, { label: 'w (slope)', min: 0, max: 300, step: 1, value: w,
      fmt: function (v) { return v.toFixed(0); }, on: function (v) { w = v; render(); } });
    A.slider(bar, { label: 'b (intercept)', min: -100, max: 400, step: 1, value: b,
      fmt: function (v) { return v.toFixed(0); }, on: function (v) { b = v; render(); } });
    A.button(bar, 'best fit', function () {
      w = Math.round(FIT.w); b = Math.round(FIT.b);
      var ins = bar.querySelectorAll('input'); ins[0].value = w; ins[1].value = b;
      bar.querySelectorAll('output')[0].textContent = w; bar.querySelectorAll('output')[1].textContent = b;
      render();
    });
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var box = { x: 80, y: 44, w: 400, h: 220 };
      var S = A.axes(ctx, box, [0, 4.4], [0, 900], {
        xticks: 4, yticks: 4, xfmt: function (v) { return v.toFixed(1); },
        yfmt: function (v) { return v.toFixed(0); },
        xlab: 'x — size (1000 sqft)', ylab: 'y — price ($1000s)'
      });
      A.plot(ctx, S, [0, 4.4], function (x) { return w * x + b; }, P.a, 2.6);
      HOUSE.forEach(function (p) {
        A.dot(ctx, S.X(p.x), S.Y(p.y), 5, P.b);
        A.line(ctx, S.X(p.x), S.Y(p.y), S.X(p.x), S.Y(w * p.x + b), P.r, 1.2, [3, 2]);
      });
      A.dot(ctx, S.X(0), S.Y(b), 6, P.g);
      A.txt(ctx, 'b = ' + b, S.X(0) + 10, S.Y(b) - 8, { size: 12, mono: true, w: 700, fill: P.g });
      /* the notation panel */
      A.txt(ctx, 'the model', 620, 66, { align: 'center', size: 13, w: 700, fill: P.soft });
      A.txt(ctx, 'f(x) = wx + b', 620, 96, { align: 'center', size: 20, mono: true, w: 700, fill: P.a });
      [['w', 'the slope — $' + w + 'k per 1000 sqft'],
       ['b', 'the intercept — where it crosses'],
       ['x', 'the input (a feature)'],
       ['ŷ', 'the prediction f(x)'],
       ['y', 'the TRUE price (the target)'],
       ['m', M + ' training examples']
      ].forEach(function (r, i) {
        A.txt(ctx, r[0], 528, 130 + i * 24, { size: 13, mono: true, w: 700, fill: P.a });
        A.txt(ctx, r[1], 552, 130 + i * 24, { size: 10.5, fill: P.faint });
      });
      A.txt(ctx, 'red dashes are the errors: how wrong each prediction is', 80, 292,
        { size: 12, fill: P.faint });
      A.txt(ctx, 'total squared error J = ' + cost(w, b).toFixed(1) +
        (Math.abs(cost(w, b) - cost(FIT.w, FIT.b)) < 30 ? '   ← close to the best possible' : ''),
        80, 314, { size: 13, mono: true, w: 700, fill: P.a });
      ro.set('f<sub>w,b</sub>(x) = <b>wx + b</b>   —  the whole model. A straight line, with two numbers to choose.' +
        '\nThe superscript notation: x<sup>(i)</sup>, y<sup>(i)</sup> is the i-th training example. ' +
        'x<sup>(2)</sup> = ' + HOUSE[1].x + ', y<sup>(2)</sup> = ' + HOUSE[1].y +
        '. Round brackets mean “example number”, never a power.');
    }
    A.bind(c, render); render();
  });

  /* ============================================================
     5. The cost function formula
     ============================================================ */
  A.def('costformula', function (root) {
    var c = A.canvas(root, 760, 340), ctx = c.ctx;
    var w = 150, b = 100;
    var bar = A.ctrls(root), ro = A.readout(root);
    A.slider(bar, { label: 'w', min: 0, max: 300, step: 1, value: w,
      fmt: function (v) { return v.toFixed(0); }, on: function (v) { w = v; render(); } });
    A.slider(bar, { label: 'b', min: -100, max: 400, step: 1, value: b,
      fmt: function (v) { return v.toFixed(0); }, on: function (v) { b = v; render(); } });
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var hot = Math.floor((t * .9) % M);
      var box = { x: 70, y: 44, w: 340, h: 210 };
      var S = A.axes(ctx, box, [0, 4.4], [0, 900], {
        xticks: 4, yticks: 4, xfmt: function (v) { return v.toFixed(1); },
        yfmt: function (v) { return v.toFixed(0); }, xlab: 'x', ylab: 'y'
      });
      A.plot(ctx, S, [0, 4.4], function (x) { return w * x + b; }, P.a, 2.4);
      HOUSE.forEach(function (p, i) {
        var pred = w * p.x + b, err = pred - p.y;
        var on = i === hot;
        /* the squared error, drawn as an actual square */
        if (on) {
          var side = Math.abs(S.Y(p.y) - S.Y(pred));
          ctx.save(); ctx.fillStyle = P.r; ctx.globalAlpha = .18;
          ctx.fillRect(S.X(p.x), Math.min(S.Y(p.y), S.Y(pred)), side, side);
          ctx.globalAlpha = 1; ctx.strokeStyle = P.r; ctx.lineWidth = 1.4;
          ctx.strokeRect(S.X(p.x), Math.min(S.Y(p.y), S.Y(pred)), side, side);
          ctx.restore();
        }
        A.line(ctx, S.X(p.x), S.Y(p.y), S.X(p.x), S.Y(pred), on ? P.r : P.line, on ? 2.4 : 1.2);
        A.dot(ctx, S.X(p.x), S.Y(p.y), on ? 6.5 : 4.5, on ? P.r : P.b);
      });
      /* the running calculation */
      var p2 = HOUSE[hot], pred2 = w * p2.x + b, e2 = pred2 - p2.y;
      A.txt(ctx, 'example ' + (hot + 1) + ' of ' + M, 450, 60, { size: 12.5, w: 700, fill: P.r });
      [['x⁽ⁱ⁾', p2.x.toFixed(1)], ['y⁽ⁱ⁾ (true)', p2.y.toFixed(0)],
       ['f(x⁽ⁱ⁾) (predicted)', pred2.toFixed(1)],
       ['error = f − y', e2.toFixed(1)], ['error²', (e2 * e2).toFixed(0)]
      ].forEach(function (r, i) {
        A.txt(ctx, r[0], 450, 88 + i * 24, { size: 11.5, fill: P.soft });
        A.txt(ctx, r[1], 700, 88 + i * 24, { align: 'right', size: 12.5, mono: true, w: 700,
          fill: i === 4 ? P.r : P.ink });
      });
      A.line(ctx, 450, 212, 700, 212, P.line, 1);
      A.txt(ctx, 'add all ' + M + ' squares, divide by 2m', 450, 232, { size: 11, fill: P.faint });
      A.txt(ctx, 'J(w, b) = ' + cost(w, b).toFixed(2), 450, 262,
        { size: 18, mono: true, w: 700, fill: P.a });
      A.txt(ctx, 'The square makes big mistakes hurt disproportionately, and makes every error positive so',
        70, 292, { size: 11.5, fill: P.soft });
      A.txt(ctx, 'overshooting and undershooting cannot cancel out.', 70, 310, { size: 11.5, fill: P.soft });
      A.txt(ctx, 'The 2 in 2m is pure convenience — it cancels when you differentiate.', 70, 330,
        { size: 11.5, w: 700, fill: P.a });
      ro.set('J(w, b) = <b>(1 / 2m) Σ<sub>i=1..m</sub> ( f<sub>w,b</sub>(x<sup>(i)</sup>) − y<sup>(i)</sup> )²</b>' +
        '\nOne number summarising how wrong the whole line is. Smaller is better; the goal is to find ' +
        'the w and b that make it smallest.');
    }
    A.autoplay(root, c, render);
  });

  /* ============================================================
     6. Cost function intuition (b fixed at 0)
     ============================================================ */
  A.def('costintuition', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var w = 0.5;
    var D = [{ x: 1, y: 1 }, { x: 2, y: 2 }, { x: 3, y: 3 }];
    var bar = A.ctrls(root), ro = A.readout(root);
    A.slider(bar, { label: 'w', min: -0.5, max: 2.5, step: .01, value: w,
      fmt: function (v) { return v.toFixed(2); }, on: function (v) { w = v; render(); } });
    function J(ww) {
      var s = 0; D.forEach(function (p) { var e = ww * p.x - p.y; s += e * e; });
      return s / (2 * D.length);
    }
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var b1 = { x: 70, y: 50, w: 280, h: 200 };
      var S1 = A.axes(ctx, b1, [0, 3.4], [0, 3.4], {
        xticks: 3, yticks: 3, xfmt: function (v) { return v.toFixed(0); },
        yfmt: function (v) { return v.toFixed(0); }, xlab: 'x', ylab: 'y'
      });
      A.txt(ctx, 'the model  f(x) = wx', b1.x + b1.w / 2, 38, { align: 'center', size: 12.5, w: 700, fill: P.soft });
      A.plot(ctx, S1, [0, 3.4], function (x) { return w * x; }, P.a, 2.6);
      D.forEach(function (p) {
        A.line(ctx, S1.X(p.x), S1.Y(p.y), S1.X(p.x), S1.Y(w * p.x), P.r, 1.6, [3, 2]);
        A.dot(ctx, S1.X(p.x), S1.Y(p.y), 5.5, P.b);
      });
      var b2 = { x: 430, y: 50, w: 280, h: 200 };
      var S2 = A.axes(ctx, b2, [-0.5, 2.5], [0, 2.6], {
        xticks: 3, yticks: 3, xfmt: function (v) { return v.toFixed(1); },
        yfmt: function (v) { return v.toFixed(1); }, xlab: 'w', ylab: 'J(w)'
      });
      A.txt(ctx, 'the cost  J(w)', b2.x + b2.w / 2, 38, { align: 'center', size: 12.5, w: 700, fill: P.soft });
      A.plot(ctx, S2, [-0.5, 2.5], J, P.p, 2.6);
      A.dot(ctx, S2.X(w), S2.Y(J(w)), 7, P.a);
      A.line(ctx, S2.X(w), b2.y + b2.h, S2.X(w), S2.Y(J(w)), P.a, 1.2, [3, 3]);
      A.dot(ctx, S2.X(1), S2.Y(0), 5, P.g);
      A.txt(ctx, 'minimum at w = 1', S2.X(1) + 8, S2.Y(0) - 10, { size: 11, w: 700, fill: P.g });
      A.txt(ctx, 'J = ' + J(w).toFixed(3), S2.X(w) + 10, S2.Y(J(w)) - 10,
        { size: 12, mono: true, w: 700, fill: P.a });
      A.txt(ctx, 'Every choice of w on the left becomes ONE POINT on the right.', 70, 282,
        { size: 12.5, w: 700, fill: P.soft });
      A.txt(ctx, 'The left panel is the model, in the world of the data. The right panel is the cost, in the world of the parameters.',
        70, 302, { size: 11.5, fill: P.faint });
      A.txt(ctx, 'Training means: find the lowest point on the right. Everything from here is about how to do that.',
        70, 322, { size: 11.5, w: 700, fill: P.a });
      ro.set('With b fixed at 0 there is only one parameter, so J is a curve you can actually draw. ' +
        'It is a <b>parabola</b>, and it has exactly one lowest point.' +
        '\nHere the data lies perfectly on y = x, so J(1) = 0 exactly. Real data never does, and the ' +
        'minimum of J is above zero.');
    }
    A.bind(c, render); render();
  });

  /* ============================================================
     7. Visualising J(w, b) — the contour plot
     ============================================================ */
  A.def('costcontour', function (root) {
    var c = A.canvas(root, 760, 350), ctx = c.ctx;
    var w = 90, b = 300;
    var ro = A.readout(root);
    var box = { x: 420, y: 52, w: 290, h: 230 };
    var WR = [40, 300], BR = [-150, 450];
    function S() {
      return { X: function (v) { return A.map(v, WR[0], WR[1], box.x, box.x + box.w); },
               Y: function (v) { return A.map(v, BR[0], BR[1], box.y + box.h, box.y); } };
    }
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var b1 = { x: 60, y: 52, w: 290, h: 230 };
      var S1 = A.axes(ctx, b1, [0, 4.4], [0, 900], {
        xticks: 4, yticks: 4, xfmt: function (v) { return v.toFixed(1); },
        yfmt: function (v) { return v.toFixed(0); }, xlab: 'size', ylab: 'price'
      });
      A.txt(ctx, 'the line these parameters give', b1.x + b1.w / 2, 40,
        { align: 'center', size: 12, w: 700, fill: P.soft });
      A.plot(ctx, S1, [0, 4.4], function (x) { return w * x + b; }, P.a, 2.6);
      HOUSE.forEach(function (p) { A.dot(ctx, S1.X(p.x), S1.Y(p.y), 4.6, P.b); });
      /* the contour panel */
      var Sc = A.axes(ctx, box, WR, BR, {
        xticks: 4, yticks: 4, xfmt: function (v) { return v.toFixed(0); },
        yfmt: function (v) { return v.toFixed(0); }, xlab: 'w', ylab: 'b'
      });
      A.txt(ctx, 'J(w, b) seen from above', box.x + box.w / 2, 40,
        { align: 'center', size: 12, w: 700, fill: P.soft });
      var Jmin = cost(FIT.w, FIT.b);
      [1.05, 1.25, 1.7, 2.6, 4.4, 8, 15, 28].forEach(function (k, i) {
        contour(ctx, Sc, Jmin * k + 40 * k, i === 0 ? P.a : P.lineSoft, i === 0 ? 1.6 : 1.1);
      });
      A.dot(ctx, Sc.X(FIT.w), Sc.Y(FIT.b), 6, P.g);
      A.txt(ctx, 'minimum', Sc.X(FIT.w) + 9, Sc.Y(FIT.b) + 4, { size: 10.5, w: 700, fill: P.g });
      A.dot(ctx, Sc.X(w), Sc.Y(b), 8, P.a);
      A.txt(ctx, 'you', Sc.X(w) + 10, Sc.Y(b) - 8, { size: 11, w: 700, fill: P.a });
      A.txt(ctx, 'drag inside the right panel', box.x + box.w / 2, box.y + box.h + 52,
        { align: 'center', size: 11, fill: P.faint });
      A.txt(ctx, 'w = ' + w.toFixed(0) + '   b = ' + b.toFixed(0) + '   J = ' + cost(w, b).toFixed(1),
        60, 312, { size: 13.5, mono: true, w: 700, fill: P.a });
      A.txt(ctx, 'Each ring is a set of (w, b) pairs that are all EQUALLY wrong — like height lines on a map.',
        60, 336, { size: 11.5, fill: P.faint });
      ro.set('J(w, b) is a <b>bowl</b> — a 3-D surface over the two parameters. Contours are that bowl ' +
        'seen from directly above.' +
        '\nThe centre of the smallest ring is the best line. Every gradient-descent picture in this course ' +
        'is a path across this map.');
    }
    function drag(ev) {
      var p = c.pt(ev);
      if (p.x < box.x - 10 || p.x > box.x + box.w + 10) return;
      w = A.clamp(A.map(p.x, box.x, box.x + box.w, WR[0], WR[1]), WR[0], WR[1]);
      b = A.clamp(A.map(p.y, box.y + box.h, box.y, BR[0], BR[1]), BR[0], BR[1]);
      render();
    }
    var down = false;
    c.cv.addEventListener('pointerdown', function (e) { down = true; drag(e); e.preventDefault(); });
    c.cv.addEventListener('pointermove', function (e) { if (down) drag(e); });
    window.addEventListener('pointerup', function () { down = false; });
    A.bind(c, render); render();
  });

})();

/* ---------- part 2 : gradient descent ---------- */
(function () {
  'use strict';

  var HOUSE = [
    { x: 1.0, y: 300 }, { x: 1.4, y: 355 }, { x: 1.9, y: 445 }, { x: 2.1, y: 500 },
    { x: 2.6, y: 545 }, { x: 3.0, y: 640 }, { x: 3.4, y: 690 }, { x: 3.9, y: 795 }
  ];
  var M = HOUSE.length;
  function cost(w, b) {
    var s = 0; HOUSE.forEach(function (p) { var e = w * p.x + b - p.y; s += e * e; });
    return s / (2 * M);
  }
  function grads(w, b) {
    var gw = 0, gb = 0;
    HOUSE.forEach(function (p) { var e = w * p.x + b - p.y; gw += e * p.x; gb += e; });
    return [gw / M, gb / M];
  }
  var FIT = (function () {
    var sx = 0, sy = 0, sxx = 0, sxy = 0;
    HOUSE.forEach(function (p) { sx += p.x; sy += p.y; sxx += p.x * p.x; sxy += p.x * p.y; });
    var w = (M * sxy - sx * sy) / (M * sxx - sx * sx);
    return { w: w, b: (sy - w * sx) / M };
  })();

  /* ============================================================
     8. Gradient descent — the hill analogy
     ============================================================ */
  A.def('gradientdescent', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var ro = A.readout(root);
    function land(x) {
      return 150 - 52 * Math.sin(x * 1.05) - 34 * Math.sin(x * 2.3 + 1.1) - 16 * Math.sin(x * .45);
    }
    function slope(x) { return (land(x + .01) - land(x - .01)) / .02; }
    function render(t) {
      var P = A.pal(); c.clear(P.panel);
      t = t || 0;
      var box = { x: 50, y: 50, w: 660, h: 200 };
      /* the hills */
      ctx.save(); ctx.beginPath();
      ctx.moveTo(box.x, box.y + box.h);
      for (var i = 0; i <= 660; i++) {
        var u = i / 660 * 9;
        ctx.lineTo(box.x + i, box.y + land(u) * .95);
      }
      ctx.lineTo(box.x + box.w, box.y + box.h); ctx.closePath();
      ctx.fillStyle = P.sunk; ctx.fill();
      ctx.strokeStyle = P.line; ctx.lineWidth = 2; ctx.stroke(); ctx.restore();
      /* two walkers from two starts */
      var starts = [1.1, 6.4], cols = [P.a, P.b];
      starts.forEach(function (s0, k) {
        var x = s0, lr = 0.012;
        var steps = Math.min(160, Math.floor((t * 26) % 210));
        var path = [x];
        for (var n = 0; n < steps; n++) { x -= lr * slope(x); path.push(x); }
        ctx.save(); ctx.strokeStyle = cols[k]; ctx.lineWidth = 1.6; ctx.globalAlpha = .5;
        ctx.beginPath();
        path.forEach(function (px, n) {
          var sx = box.x + px / 9 * 660, sy = box.y + land(px) * .95;
          n === 0 ? ctx.moveTo(sx, sy) : ctx.lineTo(sx, sy);
        });
        ctx.stroke(); ctx.restore();
        var fx = box.x + x / 9 * 660, fy = box.y + land(x) * .95;
        A.dot(ctx, fx, fy - 7, 8, cols[k]);
        A.txt(ctx, 'start ' + (k + 1), box.x + s0 / 9 * 660, box.y + land(s0) * .95 - 20,
          { align: 'center', size: 10.5, fill: cols[k] });
      });
      A.txt(ctx, 'you are standing on a hilly landscape in thick fog', 50, 36,
        { size: 13, w: 700, fill: P.soft });
      A.txt(ctx, 'spin around, find the steepest way DOWN, take one small step, repeat', 50, 274,
        { size: 12.5, w: 700, fill: P.a });
      A.txt(ctx, 'Two different starting points, two different valleys. Neither walker can see the other, and neither',
        50, 300, { size: 11.5, fill: P.faint });
      A.txt(ctx, 'knows whether a deeper valley exists elsewhere — these are LOCAL minima.', 50, 318,
        { size: 11.5, w: 700, fill: P.r });
      ro.set('Gradient descent is not clever. It is “look at your feet, step downhill, repeat”.' +
        '\nGood news for linear regression: its cost function is a single smooth <b>bowl</b> with no ' +
        'local minima at all, so this problem cannot arise there. It very much can for neural networks.');
    }
    A.autoplay(root, c, render);
  });

  /* ============================================================
     9. Implementing gradient descent — the simultaneous update
     ============================================================ */
  A.def('gdsteps', function (root) {
    var c = A.canvas(root, 760, 320), ctx = c.ctx;
    var ro = A.readout(root);
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var step = Math.floor((t * .6) % 4);
      var w0 = 100, b0 = 200, g = grads(w0, b0), alpha = 0.1;
      var tmp_w = w0 - alpha * g[0], tmp_b = b0 - alpha * g[1];
      var wrong_w = tmp_w;
      var wrong_g = grads(wrong_w, b0);
      var wrong_b = b0 - alpha * wrong_g[1];
      /* correct */
      A.txt(ctx, '✓ CORRECT — simultaneous update', 200, 44, { align: 'center', size: 13, w: 700, fill: P.g });
      var right = [
        'tmp_w = w − α · ∂J/∂w',
        'tmp_b = b − α · ∂J/∂b   ← uses the OLD w',
        'w = tmp_w',
        'b = tmp_b'
      ];
      right.forEach(function (l, i) {
        var on = i === step;
        A.rr(ctx, 40, 60 + i * 42, 320, 34, 6);
        ctx.fillStyle = on ? P.gS : P.sunk; ctx.fill();
        ctx.strokeStyle = on ? P.g : P.lineSoft; ctx.lineWidth = on ? 1.8 : 1; ctx.stroke();
        A.txt(ctx, l, 54, 82 + i * 42, { size: 11.5, mono: true, w: on ? 700 : 500,
          fill: on ? P.g : P.soft });
      });
      /* wrong */
      A.txt(ctx, '✗ WRONG — sequential update', 560, 44, { align: 'center', size: 13, w: 700, fill: P.r });
      var wrong = [
        'tmp_w = w − α · ∂J/∂w',
        'w = tmp_w                ← updated too early',
        'tmp_b = b − α · ∂J/∂b   ← now uses the NEW w',
        'b = tmp_b'
      ];
      wrong.forEach(function (l, i) {
        var on = i === step;
        A.rr(ctx, 400, 60 + i * 42, 320, 34, 6);
        ctx.fillStyle = on ? P.rS : P.sunk; ctx.fill();
        ctx.strokeStyle = on ? P.r : P.lineSoft; ctx.lineWidth = on ? 1.8 : 1; ctx.stroke();
        A.txt(ctx, l, 414, 82 + i * 42, { size: 11.5, mono: true, w: on ? 700 : 500,
          fill: on ? P.r : P.soft });
      });
      A.txt(ctx, 'from w = ' + w0 + ', b = ' + b0 + ', α = ' + alpha + ':', 40, 254,
        { size: 12, fill: P.faint });
      A.txt(ctx, 'correct → w = ' + tmp_w.toFixed(3) + ',  b = ' + tmp_b.toFixed(3), 40, 276,
        { size: 12.5, mono: true, w: 700, fill: P.g });
      A.txt(ctx, 'wrong   → w = ' + wrong_w.toFixed(3) + ',  b = ' + wrong_b.toFixed(3), 40, 298,
        { size: 12.5, mono: true, w: 700, fill: P.r });
      A.txt(ctx, 'different numbers — and the difference compounds over thousands of iterations',
        400, 298, { size: 11, fill: P.faint });
      ro.set('Both parameters must be updated from the <b>same</b> old values. Compute both changes first, ' +
        'then assign both.' +
        '\nThe sequential version is not gradient descent — it is a different algorithm that happens to ' +
        'often still work, which is exactly what makes the bug hard to notice.');
    }
    A.autoplay(root, c, render);
  });

  /* ============================================================
     10. Gradient descent intuition — the sign of the derivative
     ============================================================ */
  A.def('gdintuition', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var w = 2.4;
    var bar = A.ctrls(root), ro = A.readout(root);
    A.slider(bar, { label: 'w', min: -2.6, max: 2.6, step: .01, value: w,
      fmt: function (v) { return v.toFixed(2); }, on: function (v) { w = v; render(); } });
    function J(x) { return x * x + 1; }
    function dJ(x) { return 2 * x; }
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var box = { x: 90, y: 44, w: 580, h: 210 };
      var S = A.axes(ctx, box, [-2.8, 2.8], [0, 8], {
        xticks: 4, yticks: 4, xfmt: function (v) { return v.toFixed(0); },
        yfmt: function (v) { return v.toFixed(0); }, xlab: 'w', ylab: 'J(w)'
      });
      A.plot(ctx, S, [-2.8, 2.8], J, P.p, 2.8);
      var d = dJ(w), alpha = 0.25;
      var nw = w - alpha * d;
      /* the tangent */
      A.line(ctx, S.X(w - 1.1), S.Y(J(w) - d * 1.1), S.X(w + 1.1), S.Y(J(w) + d * 1.1), P.b, 2.2, [6, 4]);
      A.dot(ctx, S.X(w), S.Y(J(w)), 7, P.a);
      A.arrow(ctx, S.X(w), S.Y(J(w)) + 26, S.X(nw), S.Y(J(w)) + 26, P.g, 2.4);
      A.dot(ctx, S.X(nw), S.Y(J(nw)), 5, P.g);
      A.txt(ctx, d > 0 ? 'slope is POSITIVE' : d < 0 ? 'slope is NEGATIVE' : 'slope is ZERO',
        S.X(w), S.Y(J(w)) - 22, { align: 'center', size: 12.5, w: 700,
          fill: d > 0 ? P.r : d < 0 ? P.b : P.g });
      A.txt(ctx, Math.abs(d) < .02 ? 'nowhere to go — you are at the minimum'
        : d > 0 ? 'so subtracting α·slope moves w LEFT' : 'so subtracting α·slope moves w RIGHT',
        S.X(w), S.Y(J(w)) + 48, { align: 'center', size: 11.5, fill: P.g });
      A.txt(ctx, 'w := w − α · dJ/dw', 90, 288, { size: 16, mono: true, w: 700, fill: P.a });
      A.txt(ctx, '   = ' + w.toFixed(2) + ' − ' + alpha + ' × (' + d.toFixed(2) + ') = ' + nw.toFixed(3),
        90, 312, { size: 13, mono: true, fill: P.soft });
      A.txt(ctx, 'The minus sign is the whole trick: it always sends you the opposite way to the uphill direction.',
        380, 288, { size: 11.5, w: 700, fill: P.soft });
      A.txt(ctx, 'And the step shrinks automatically as the slope flattens near the bottom.', 380, 310,
        { size: 11.5, fill: P.faint });
      ro.set('Positive slope → w decreases. Negative slope → w increases. Either way you move <b>towards</b> ' +
        'the minimum.' +
        '\nNotice you never have to know where the minimum <em>is</em>. The local slope alone is enough — ' +
        'which is why this works in a million dimensions where you could never look.');
    }
    A.bind(c, render); render();
  });

  /* ============================================================
     11. The learning rate
     ============================================================ */
  A.def('learningrate', function (root) {
    var c = A.canvas(root, 760, 340), ctx = c.ctx;
    var la = -1.0;                                     /* log10 alpha */
    var bar = A.ctrls(root), ro = A.readout(root);
    A.slider(bar, { label: 'α = 10^', min: -3, max: .08, step: .02, value: la,
      fmt: function (v) { return Math.pow(10, v).toFixed(3); }, on: function (v) { la = v; render(); } });
    function J(x) { return x * x + 1; }
    function dJ(x) { return 2 * x; }
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var alpha = Math.pow(10, la);
      var box = { x: 80, y: 44, w: 380, h: 220 };
      var S = A.axes(ctx, box, [-3.2, 3.2], [0, 11], {
        xticks: 4, yticks: 4, xfmt: function (v) { return v.toFixed(0); },
        yfmt: function (v) { return v.toFixed(0); }, xlab: 'w', ylab: 'J(w)'
      });
      A.plot(ctx, S, [-3.2, 3.2], J, P.p, 2.6);
      var x = -2.6, pts = [x], diverged = false;
      for (var n = 0; n < 26; n++) {
        x = x - alpha * dJ(x);
        if (!isFinite(x) || Math.abs(x) > 60) { diverged = true; break; }
        pts.push(x);
      }
      var shown = Math.min(pts.length, 2 + Math.floor((t * 3) % (pts.length + 6)));
      for (var i = 0; i < shown; i++) {
        var xi = A.clamp(pts[i], -3.2, 3.2);
        A.dot(ctx, S.X(xi), S.Y(Math.min(J(pts[i]), 11)), 4.5, P.a);
        if (i > 0) {
          var xp = A.clamp(pts[i - 1], -3.2, 3.2);
          A.line(ctx, S.X(xp), S.Y(Math.min(J(pts[i - 1]), 11)),
            S.X(xi), S.Y(Math.min(J(pts[i]), 11)), P.a, 1.4);
        }
      }
      /* the verdict */
      var verdict = diverged ? ['α far too LARGE — it diverges', P.r,
          'each step overshoots further than the last. J grows towards infinity, and in code you get NaN.']
        : alpha < 0.02 ? ['α too SMALL — correct but glacial', P.m,
          'it will get there. It might take a hundred thousand iterations.']
        : alpha > 0.85 ? ['α too large — it oscillates', P.r,
          'bouncing back and forth across the minimum, converging slowly or not at all.']
        : ['α about right', P.g,
          'big confident steps at first, naturally smaller ones as the slope flattens.'];
      A.rr(ctx, 490, 60, 230, 130, 10);
      ctx.fillStyle = verdict[1] === P.g ? P.gS : verdict[1] === P.m ? P.mS : P.rS; ctx.fill();
      ctx.strokeStyle = verdict[1]; ctx.lineWidth = 2; ctx.stroke();
      A.txt(ctx, 'α = ' + alpha.toFixed(3), 605, 88, { align: 'center', size: 16, mono: true, w: 700, fill: verdict[1] });
      A.txt(ctx, verdict[0], 605, 114, { align: 'center', size: 12, w: 700, fill: verdict[1] });
      var words = verdict[2].split(' '), line = '', ln = 0;
      words.forEach(function (wd) {
        if ((line + wd).length > 30) {
          A.txt(ctx, line, 605, 138 + ln * 15, { align: 'center', size: 10, fill: verdict[1] });
          line = wd + ' '; ln++;
        } else line += wd + ' ';
      });
      A.txt(ctx, line, 605, 138 + ln * 15, { align: 'center', size: 10, fill: verdict[1] });
      A.txt(ctx, 'steps to get within 0.01: ' + (diverged ? 'never' : pts.length >= 26 ? 'more than 26' : pts.length),
        490, 214, { size: 11.5, mono: true, fill: P.soft });
      A.txt(ctx, 'Andrew’s suggestion: try 0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1 — roughly ×3 each time —',
        80, 296, { size: 12, fill: P.soft });
      A.txt(ctx, 'and plot J against iterations for each. Pick the largest α that still decreases smoothly.',
        80, 316, { size: 12, w: 700, fill: P.a });
      ro.set('Even with a fixed α, the steps get smaller near the minimum on their own — because the ' +
        '<b>slope</b> gets smaller. You never need to decrease α by hand.' +
        '\nIf J ever <em>increases</em> between iterations, α is too large. That is the single most useful ' +
        'debugging rule in this course.');
    }
    A.autoplay(root, c, render);
  });

  /* ============================================================
     12. Gradient descent for linear regression — a convex bowl
     ============================================================ */
  A.def('gdlinreg', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var ro = A.readout(root);
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      /* convex bowl vs wiggly surface */
      [[190, 'squared error cost', 'ONE minimum — always', P.g, false],
       [570, 'a neural network cost', 'many local minima', P.r, true]
      ].forEach(function (pn) {
        var cx = pn[0];
        A.txt(ctx, pn[1], cx, 46, { align: 'center', size: 13, w: 700, fill: pn[3] });
        ctx.save(); ctx.strokeStyle = pn[3]; ctx.lineWidth = 2.4; ctx.beginPath();
        for (var i = 0; i <= 120; i++) {
          var u = -1 + 2 * i / 120;
          var y = pn[4]
            ? 150 - 30 * Math.sin(u * 4.1) - 22 * Math.sin(u * 8.3 + 1) + 42 * u * u
            : 66 + 92 * u * u;
          var px = cx + u * 130, py = 60 + y * .62;
          i === 0 ? ctx.moveTo(px, py) : ctx.lineTo(px, py);
        }
        ctx.stroke(); ctx.restore();
        if (!pn[4]) {
          A.dot(ctx, cx, 60 + 66 * .62, 6, P.g);
          A.txt(ctx, 'wherever you start, you end here', cx, 190, { align: 'center', size: 10.5, fill: P.g });
        } else {
          [-0.62, 0.03, 0.66].forEach(function (u) {
            var y = 150 - 30 * Math.sin(u * 4.1) - 22 * Math.sin(u * 8.3 + 1) + 42 * u * u;
            A.dot(ctx, cx + u * 130, 60 + y * .62, 5, P.r);
          });
          A.txt(ctx, 'where you end depends on where you start', cx, 190, { align: 'center', size: 10.5, fill: P.r });
        }
      });
      A.txt(ctx, 'the derivatives, worked out', 40, 226, { size: 12.5, w: 700, fill: P.soft });
      A.txt(ctx, '∂J/∂w = (1/m) Σ ( f(x⁽ⁱ⁾) − y⁽ⁱ⁾ ) · x⁽ⁱ⁾', 40, 254,
        { size: 14, mono: true, w: 700, fill: P.a });
      A.txt(ctx, '∂J/∂b = (1/m) Σ ( f(x⁽ⁱ⁾) − y⁽ⁱ⁾ )', 40, 280,
        { size: 14, mono: true, w: 700, fill: P.a });
      A.txt(ctx, 'the only difference is the extra · x⁽ⁱ⁾ on the w version', 40, 302,
        { size: 11.5, fill: P.faint });
      A.txt(ctx, 'this is where the 2 in 1/2m goes:', 430, 240, { size: 11, fill: P.faint });
      A.txt(ctx, 'd/dw of (…)² brings down a 2,', 430, 258, { size: 11, fill: P.faint });
      A.txt(ctx, 'which cancels the 2 in the denominator.', 430, 276, { size: 11, fill: P.faint });
      A.txt(ctx, 'A tidier formula, for free.', 430, 300, { size: 11, w: 700, fill: P.a });
      ro.set('The squared-error cost for linear regression is <b>convex</b> — a single smooth bowl. ' +
        'It has exactly one minimum and gradient descent always finds it, from any starting point.' +
        '\nThis is a genuinely special property. You lose it the moment you build a neural network.');
    }
    A.autoplay(root, c, render);
  });

  /* ============================================================
     13. Running gradient descent
     ============================================================ */
  A.def('gdrunning', function (root) {
    var c = A.canvas(root, 760, 350), ctx = c.ctx;
    var alpha = 0.08, w = 40, b = 380, it = 0, hist = [];
    var bar = A.ctrls(root), ro = A.readout(root);
    A.slider(bar, { label: 'α', min: .005, max: .16, step: .005, value: alpha,
      fmt: function (v) { return v.toFixed(3); }, on: function (v) { alpha = v; reset(); } });
    A.button(bar, 'restart', function () { reset(); });
    function reset() { w = 40; b = 380; it = 0; hist = [cost(w, b)]; }
    reset();
    function step() {
      var g = grads(w, b);
      w -= alpha * g[0]; b -= alpha * g[1]; it++;
      if (it % 2 === 0) { hist.push(cost(w, b)); if (hist.length > 200) hist.shift(); }
    }
    var box = { x: 400, y: 46, w: 290, h: 190 };
    var WR = [20, 300], BR = [-120, 440];
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var b1 = { x: 60, y: 46, w: 280, h: 190 };
      var S1 = A.axes(ctx, b1, [0, 4.4], [0, 900], {
        xticks: 4, yticks: 3, xfmt: function (v) { return v.toFixed(1); },
        yfmt: function (v) { return v.toFixed(0); }, xlab: 'size', ylab: 'price'
      });
      A.plot(ctx, S1, [0, 4.4], function (x) { return w * x + b; }, P.a, 2.6);
      HOUSE.forEach(function (p) { A.dot(ctx, S1.X(p.x), S1.Y(p.y), 4.4, P.b); });
      A.txt(ctx, 'the fit, improving', b1.x + b1.w / 2, 36, { align: 'center', size: 12, w: 700, fill: P.soft });
      var Sc = A.axes(ctx, box, WR, BR, {
        xticks: 4, yticks: 3, xfmt: function (v) { return v.toFixed(0); },
        yfmt: function (v) { return v.toFixed(0); }, xlab: 'w', ylab: 'b'
      });
      A.txt(ctx, 'the path across the cost map', box.x + box.w / 2, 36,
        { align: 'center', size: 12, w: 700, fill: P.soft });
      /* shaded cost field */
      ctx.save(); ctx.globalAlpha = .5;
      for (var gx = 0; gx <= 30; gx++) for (var gy = 0; gy <= 20; gy++) {
        var ww = WR[0] + (WR[1] - WR[0]) * gx / 30, bb = BR[0] + (BR[1] - BR[0]) * gy / 20;
        var J = cost(ww, bb), v = A.clamp(Math.log(1 + J) / 12, 0, 1);
        ctx.fillStyle = P.a; ctx.globalAlpha = .04 + v * .22;
        ctx.fillRect(Sc.X(ww) - 6, Sc.Y(bb) - 6, 12, 12);
      }
      ctx.restore();
      /* replay the whole path from the start, deterministically */
      var pw = 40, pb = 380;
      ctx.save(); ctx.strokeStyle = P.a; ctx.lineWidth = 1.8; ctx.beginPath();
      ctx.moveTo(Sc.X(pw), Sc.Y(pb));
      for (var n = 0; n < it; n++) {
        var g = grads(pw, pb); pw -= alpha * g[0]; pb -= alpha * g[1];
        ctx.lineTo(Sc.X(A.clamp(pw, WR[0], WR[1])), Sc.Y(A.clamp(pb, BR[0], BR[1])));
      }
      ctx.stroke(); ctx.restore();
      A.dot(ctx, Sc.X(A.clamp(w, WR[0], WR[1])), Sc.Y(A.clamp(b, BR[0], BR[1])), 6, P.a);
      A.dot(ctx, Sc.X(FIT.w), Sc.Y(FIT.b), 5, P.g);
      /* the learning curve */
      var b3 = { x: 60, y: 262, w: 630, h: 56 };
      if (hist.length > 2) {
        var mx = hist[0], mn = Math.min.apply(null, hist);
        ctx.save(); ctx.strokeStyle = P.p; ctx.lineWidth = 2; ctx.beginPath();
        hist.forEach(function (v, i) {
          var px = b3.x + b3.w * i / Math.max(1, hist.length - 1);
          var py = b3.y + b3.h - b3.h * (v - mn) / (mx - mn + 1e-9);
          i === 0 ? ctx.moveTo(px, py) : ctx.lineTo(px, py);
        });
        ctx.stroke(); ctx.restore();
        A.txt(ctx, 'J against iterations — it should fall on EVERY step', b3.x, b3.y - 6,
          { size: 11, fill: P.faint });
      }
      A.txt(ctx, 'iteration ' + it + '   w = ' + w.toFixed(1) + '   b = ' + b.toFixed(1) +
        '   J = ' + cost(w, b).toFixed(1), 60, 338, { size: 12.5, mono: true, w: 700, fill: P.a });
      ro.set('This is <b>batch</b> gradient descent: every single step uses all ' + M +
        ' training examples.' +
        '\nWatch the path: big strides down the steep sides of the valley, then a long slow crawl along ' +
        'the flat floor towards the minimum. That elongated valley is why feature scaling (Week 2) matters.');
    }
    A.bind(c, render);
    var acc = 0;
    A.loop(c.cv, function (t) {
      if (t - acc > 0.06) { acc = t; if (it < 220) step(); else reset(); }
      render();
    });
  });

})();
