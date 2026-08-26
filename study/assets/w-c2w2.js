/* Widgets for Course 2 / Week 2 — training, activations, softmax, Adam */
(function () {
  'use strict';

  /* ============================================================
     1. The three steps of training
     ============================================================ */
  A.def('trainsteps', function (root) {
    var c = A.canvas(root, 760, 320), ctx = c.ctx;
    var steps = [
      { n: '1 · Define the model', code: 'Sequential([Dense(25, "relu"),\n            Dense(15, "relu"),\n            Dense(1,  "sigmoid")])',
        lr: 'z = np.dot(w, x) + b\nf = 1 / (1 + np.exp(-z))', say: 'what is f(x)?' },
      { n: '2 · Say what "wrong" means', code: 'model.compile(\n    loss=BinaryCrossentropy())',
        lr: 'loss = -y*log(f) - (1-y)*log(1-f)', say: 'how bad is a guess?' },
      { n: '3 · Minimise it', code: 'model.fit(X, Y, epochs=100)',
        lr: 'w = w - alpha * dJ_dw\nb = b - alpha * dJ_db', say: 'nudge everything downhill' }
    ];
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var cur = Math.floor((t * .35) % 3);
      for (var i = 0; i < 3; i++) {
        var y = 40 + i * 92, on = i === cur;
        A.rr(ctx, 30, y, 700, 80, 10);
        ctx.fillStyle = on ? P.aS : P.sunk; ctx.fill();
        ctx.strokeStyle = on ? P.a : P.lineSoft; ctx.lineWidth = on ? 2 : 1; ctx.stroke();
        A.txt(ctx, steps[i].n, 46, y + 24, { size: 13.5, w: 700, fill: on ? P.a : P.soft });
        A.txt(ctx, steps[i].say, 46, y + 44, { size: 11.5, fill: P.faint });
        steps[i].code.split('\n').forEach(function (ln, k) {
          A.txt(ctx, ln, 250, y + 22 + k * 15, { size: 11, mono: true, fill: on ? P.ink : P.faint });
        });
        A.txt(ctx, 'same idea in logistic regression:', 500, y + 18, { size: 10, fill: P.faint });
        steps[i].lr.split('\n').forEach(function (ln, k) {
          A.txt(ctx, ln, 500, y + 34 + k * 15, { size: 10.5, mono: true, fill: on ? P.b : P.faint });
        });
      }
      A.txt(ctx, 'Training a neural network is the same three steps you already did in Course 1.',
        30, 26, { size: 12, w: 600, fill: P.soft });
      A.txt(ctx, 'Only the model in step 1 got bigger.', 30, 310, { size: 12, fill: P.faint });
    }
    A.bind(c, function () { render(lt); });
    var lt = 0; A.loop(c.cv, function (t) { lt = t; render(t); });
  });

  /* ============================================================
     2. Binary cross-entropy loss
     ============================================================ */
  A.def('losscurve', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var f = 0.7, y = 1;
    var bar = A.ctrls(root), ro = A.readout(root);
    A.slider(bar, { label: 'model says f =', min: .01, max: .99, value: f,
      on: function (v) { f = v; render(); } });
    A.button(bar, 'truth: y = 1', function (b) { y = 1; syncY(); render(); });
    A.button(bar, 'truth: y = 0', function (b) { y = 0; syncY(); render(); });
    function syncY() {
      var bs = bar.querySelectorAll('button');
      bs[0].classList.toggle('primary', y === 1);
      bs[1].classList.toggle('primary', y === 0);
    }
    function loss(fv) { return y === 1 ? -Math.log(fv) : -Math.log(1 - fv); }
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var box = { x: 70, y: 40, w: 620, h: 220 };
      var S = A.axes(ctx, box, [0, 1], [0, 5], {
        xticks: 5, yticks: 5,
        xfmt: function (v) { return v.toFixed(1); },
        yfmt: function (v) { return v.toFixed(0); },
        xlab: 'f(x) — what the model predicted', ylab: 'loss'
      });
      /* both curves, the inactive one faded */
      A.plot(ctx, S, [0.005, 0.995], function (v) { return Math.min(5, -Math.log(v)); },
        y === 1 ? P.g : P.lineSoft, y === 1 ? 2.6 : 1.6);
      A.plot(ctx, S, [0.005, 0.995], function (v) { return Math.min(5, -Math.log(1 - v)); },
        y === 0 ? P.r : P.lineSoft, y === 0 ? 2.6 : 1.6);
      A.txt(ctx, 'if the truth is y = 1', S.X(.12), S.Y(4.1), { size: 12, w: 700, fill: y === 1 ? P.g : P.faint });
      A.txt(ctx, 'if the truth is y = 0', S.X(.62), S.Y(4.1), { size: 12, w: 700, fill: y === 0 ? P.r : P.faint });
      var Lv = Math.min(loss(f), 5);
      A.line(ctx, S.X(f), box.y, S.X(f), S.Y(0), P.a, 1.4, [4, 3]);
      A.dot(ctx, S.X(f), S.Y(Lv), 7, P.a);
      A.txt(ctx, 'loss = ' + loss(f).toFixed(2), S.X(f) + 12, S.Y(Lv) - 10,
        { size: 13, mono: true, w: 700, fill: P.a });
      A.txt(ctx, 'Confident and right → almost no loss. Confident and WRONG → the loss explodes.',
        70, 296, { size: 12.5, w: 600, fill: P.soft });
      A.txt(ctx, 'That asymmetry is the whole point: the model is punished hardest for being sure of a lie.',
        70, 316, { size: 12, fill: P.faint });
      ro.set('L(f, y) = <b>−y·log(f) − (1−y)·log(1−f)</b>\n' +
        'y = ' + y + ',  f = ' + f.toFixed(2) + '  →  L = ' +
        (y === 1 ? '−log(' + f.toFixed(2) + ')' : '−log(1 − ' + f.toFixed(2) + ')') +
        ' = <b>' + loss(f).toFixed(3) + '</b>');
    }
    syncY();
    A.bind(c, render); render();
  });

  /* ============================================================
     3. The activation function zoo
     ============================================================ */
  A.def('activations', function (root) {
    var c = A.canvas(root, 760, 340), ctx = c.ctx;
    var z = 1.2, which = 0;
    var fns = [
      { n: 'sigmoid', f: A.sig, d: function (v) { var s = A.sig(v); return s * (1 - s); },
        r: '0 … 1', use: 'output layer, binary classification' },
      { n: 'ReLU', f: function (v) { return Math.max(0, v); }, d: function (v) { return v > 0 ? 1 : 0; },
        r: '0 … ∞', use: 'hidden layers — the default' },
      { n: 'linear', f: function (v) { return v; }, d: function () { return 1; },
        r: '−∞ … ∞', use: 'output layer, regression ("no activation")' },
      { n: 'tanh', f: function (v) { return Math.tanh(v); }, d: function (v) { var th = Math.tanh(v); return 1 - th * th; },
        r: '−1 … 1', use: 'older hidden layers; zero-centred sigmoid' }
    ];
    var bar = A.ctrls(root), ro = A.readout(root);
    fns.forEach(function (fn, i) { A.button(bar, fn.n, function () { which = i; sync(); render(); }); });
    A.slider(bar, { label: 'z =', min: -6, max: 6, value: z, on: function (v) { z = v; render(); } });
    function sync() { bar.querySelectorAll('button').forEach(function (b, i) { b.classList.toggle('primary', i === which); }); }
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var box = { x: 70, y: 30, w: 620, h: 230 };
      var S = A.axes(ctx, box, [-6, 6], [-1.6, 3], {
        xticks: 6, yticks: 4, xfmt: function (v) { return v.toFixed(0); },
        yfmt: function (v) { return v.toFixed(1); }, xlab: 'z  (the weighted sum)', ylab: 'g(z)'
      });
      A.line(ctx, box.x, S.Y(0), box.x + box.w, S.Y(0), P.line, 1.2);
      A.line(ctx, S.X(0), box.y, S.X(0), box.y + box.h, P.line, 1.2);
      fns.forEach(function (fn, i) {
        if (i === which) return;
        A.plot(ctx, S, [-6, 6], fn.f, P.lineSoft, 1.4);
      });
      var F = fns[which];
      A.plot(ctx, S, [-6, 6], F.f, P.a, 2.8);
      /* the slope (derivative) as a short tangent */
      var gv = F.f(z), dv = F.d(z);
      A.line(ctx, S.X(z - 1.3), S.Y(gv - dv * 1.3), S.X(z + 1.3), S.Y(gv + dv * 1.3), P.b, 2, [5, 3]);
      A.dot(ctx, S.X(z), S.Y(gv), 7, P.a);
      A.txt(ctx, F.n, S.X(-5.6), S.Y(2.7), { size: 16, w: 700, fill: P.a });
      A.txt(ctx, 'range ' + F.r, S.X(-5.6), S.Y(2.35), { size: 12, fill: P.faint });
      A.txt(ctx, 'slope here = ' + dv.toFixed(3) + (Math.abs(dv) < 0.02 ? '   ← flat! learning stalls' : ''),
        70, 300, { size: 12.5, mono: true, fill: Math.abs(dv) < 0.02 ? P.r : P.b });
      A.txt(ctx, 'used for: ' + F.use, 70, 322, { size: 12, fill: P.faint });
      ro.set('g(' + z.toFixed(2) + ') = <b>' + gv.toFixed(3) + '</b>    slope g′(' + z.toFixed(2) + ') = <b>' + dv.toFixed(3) + '</b>' +
        '\nThe slope is what gradient descent uses. Where the curve is flat, the model barely learns — drag z out to ±6 on sigmoid and watch.');
    }
    sync(); A.bind(c, render); render();
  });

  /* ============================================================
     4. Choosing an activation — the decision flow
     ============================================================ */
  A.def('actchoice', function (root) {
    var c = A.canvas(root, 760, 320), ctx = c.ctx;
    var pick = 0;
    var cases = [
      { q: 'binary: yes / no', a: 'sigmoid', why: 'output must be a probability in 0…1' },
      { q: 'regression: can be negative', a: 'linear', why: 'house price change, temperature — any real number' },
      { q: 'regression: never negative', a: 'ReLU', why: 'house price, count, duration — 0 or more' },
      { q: 'multiclass: pick one of many', a: 'softmax', why: 'probabilities across classes that add to 1' }
    ];
    var bar = A.ctrls(root);
    cases.forEach(function (cs, i) { A.button(bar, cs.q, function () { pick = i; sync(); render(); }); });
    function sync() { bar.querySelectorAll('button').forEach(function (b, i) { b.classList.toggle('primary', i === pick); }); }
    function render() {
      var P = A.pal(); c.clear(P.panel);
      A.txt(ctx, 'HIDDEN layers', 190, 46, { align: 'center', size: 13, w: 700, fill: P.soft });
      A.rr(ctx, 60, 60, 260, 90, 10); ctx.fillStyle = P.gS; ctx.fill();
      ctx.strokeStyle = P.g; ctx.lineWidth = 2; ctx.stroke();
      A.txt(ctx, 'ReLU', 190, 100, { align: 'center', size: 28, w: 700, fill: P.g });
      A.txt(ctx, 'almost always. no thinking required.', 190, 126, { align: 'center', size: 11.5, fill: P.g });
      A.txt(ctx, 'faster than sigmoid, and flat on only ONE side', 190, 172, { align: 'center', size: 11.5, fill: P.faint });
      A.txt(ctx, 'so gradients survive deep stacks', 190, 190, { align: 'center', size: 11.5, fill: P.faint });

      A.txt(ctx, 'OUTPUT layer — depends on the question', 540, 46, { align: 'center', size: 13, w: 700, fill: P.soft });
      cases.forEach(function (cs, i) {
        var y = 60 + i * 52, on = i === pick;
        A.rr(ctx, 380, y, 330, 44, 8);
        ctx.fillStyle = on ? P.aS : P.sunk; ctx.fill();
        ctx.strokeStyle = on ? P.a : P.lineSoft; ctx.lineWidth = on ? 2 : 1; ctx.stroke();
        A.txt(ctx, cs.q, 394, y + 19, { size: 12, w: on ? 700 : 500, fill: on ? P.a : P.soft });
        A.txt(ctx, cs.why, 394, y + 34, { size: 10.5, fill: P.faint });
        A.txt(ctx, cs.a, 700, y + 26, { align: 'right', size: 15, w: 700, mono: true, fill: on ? P.a : P.faint });
      });
      A.txt(ctx, 'Rule of thumb: ReLU everywhere inside, and let the output activation match what you are predicting.',
        60, 290, { size: 12, w: 600, fill: P.soft });
    }
    sync(); A.bind(c, render); render();
  });

  /* ============================================================
     5. Why we need a non-linear activation at all
     ============================================================ */
  A.def('relubuild', function (root) {
    var c = A.canvas(root, 760, 340), ctx = c.ctx;
    var n = 4;
    var bar = A.ctrls(root), ro = A.readout(root);
    A.slider(bar, { label: 'ReLU units', min: 1, max: 8, step: 1, value: n,
      fmt: function (v) { return v.toFixed(0); }, on: function (v) { n = v; render(); } });
    var knees = [-3, -1.4, 0.2, 1.6, 2.6, 3.4, 4.2, 5];
    var slopes = [1.2, -1.9, 2.4, -1.5, 1.1, -0.9, 1.6, -1.2];
    function relsum(x) {
      var s = 0.4;
      for (var i = 0; i < n; i++) s += slopes[i] * Math.max(0, x - knees[i]);
      return s;
    }
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var b1 = { x: 60, y: 46, w: 290, h: 210 }, b2 = { x: 430, y: 46, w: 280, h: 210 };
      var S1 = A.axes(ctx, b1, [-4, 6], [-4, 6], { xticks: 4, yticks: 4, xlab: 'x', ylab: 'output' });
      A.txt(ctx, 'linear activation everywhere', b1.x + b1.w / 2, 32, { align: 'center', size: 13, w: 700, fill: P.r });
      /* stack of linear layers collapses to a line */
      A.plot(ctx, S1, [-4, 6], function (x) { return 0.8 * x + 0.6; }, P.r, 2.8);
      A.txt(ctx, 'g(g(g(x))) is still', b1.x + 14, b1.y + 26, { size: 12, fill: P.faint });
      A.txt(ctx, 'a straight line.', b1.x + 14, b1.y + 44, { size: 12, w: 700, fill: P.r });
      A.txt(ctx, 'Ten layers, still a line.', b1.x + 14, b1.y + 66, { size: 12, fill: P.faint });
      A.txt(ctx, 'You have an expensive', b1.x + 14, b1.y + 92, { size: 12, fill: P.faint });
      A.txt(ctx, 'linear regression.', b1.x + 14, b1.y + 110, { size: 12, fill: P.faint });

      var S2 = A.axes(ctx, b2, [-4, 6], [-4, 6], { xticks: 4, yticks: 4, xlab: 'x', ylab: 'output' });
      A.txt(ctx, n + ' ReLU units, added up', b2.x + b2.w / 2, 32, { align: 'center', size: 13, w: 700, fill: P.g });
      for (var i = 0; i < n; i++) {
        (function (k) {
          A.plot(ctx, S2, [-4, 6], function (x) { return 0.4 + slopes[k] * Math.max(0, x - knees[k]); },
            P.lineSoft, 1.2);
        })(i);
      }
      A.plot(ctx, S2, [-4, 6], relsum, P.g, 2.8);
      for (i = 0; i < n; i++) {
        if (knees[i] > -4 && knees[i] < 6) A.dot(ctx, S2.X(knees[i]), S2.Y(relsum(knees[i])), 4, P.a);
      }
      A.txt(ctx, 'each unit adds one "kink"', b2.x + 10, b2.y + 200, { size: 11.5, fill: P.faint });
      A.txt(ctx, 'A bend is only possible because ReLU is NOT a straight line. Straight things added together stay straight.',
        60, 296, { size: 12.5, w: 600, fill: P.soft });
      A.txt(ctx, 'Enough kinks and you can trace any curve you like — that is the universal approximation idea, drawn.',
        60, 318, { size: 12, fill: P.faint });
      ro.set('linear ∘ linear = linear:  W₂(W₁x + b₁) + b₂ = (W₂W₁)x + (W₂b₁ + b₂) = <b>W′x + b′</b>' +
        '\nThe two layers algebraically collapse into one. Non-linear g is what stops the collapse.');
    }
    A.bind(c, render); render();
  });

  /* ============================================================
     6. Multiclass — more than two answers
     ============================================================ */
  A.def('multiclass', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var many = true;
    var pts = [];
    (function () {
      var cen = [[-1.4, 1.2], [1.5, 1.4], [-1.3, -1.3], [1.6, -1.2]];
      for (var k = 0; k < 4; k++) for (var i = 0; i < 22; i++) {
        var a = (i * 2.399), r = .28 + .55 * ((i * 37 % 19) / 19);
        pts.push({ x: cen[k][0] + Math.cos(a) * r * 1.6, y: cen[k][1] + Math.sin(a) * r * 1.6, k: k });
      }
    })();
    var bar = A.ctrls(root);
    A.toggle(bar, '4 classes', function (v) { many = v; render(); }, true);
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var cols = [P.a, P.b, P.g, P.p];
      var box = { x: 70, y: 30, w: 300, h: 250 };
      var S = A.axes(ctx, box, [-3, 3], [-3, 3], { xticks: 4, yticks: 4, xlab: 'x₁', ylab: 'x₂' });
      pts.forEach(function (p) {
        var k = many ? p.k : (p.k < 2 ? 0 : 1);
        A.dot(ctx, S.X(p.x), S.Y(p.y), 4, cols[k]);
      });
      if (many) {
        A.line(ctx, S.X(0), box.y, S.X(0), box.y + box.h, P.ink, 1.6, [5, 4]);
        A.line(ctx, box.x, S.Y(0), box.x + box.w, S.Y(0), P.ink, 1.6, [5, 4]);
        A.txt(ctx, '4 regions — needs 4 output units', box.x + box.w / 2, 316,
          { align: 'center', size: 12, w: 700, fill: P.soft });
      } else {
        A.line(ctx, box.x, S.Y(0), box.x + box.w, S.Y(0), P.ink, 1.8, [5, 4]);
        A.txt(ctx, 'one boundary — 1 output unit is enough', box.x + box.w / 2, 316,
          { align: 'center', size: 12, w: 700, fill: P.soft });
      }
      /* the output layer picture */
      var K = many ? 4 : 1;
      var o = A.col(600, K, 70, 240, 22);
      var probs = many ? [.62, .21, .11, .06] : [.73];
      for (var j = 0; j < K; j++) {
        A.neuron(ctx, o[j], probs[j], P, probs[j].toFixed(2), many ? 'P(class ' + (j + 1) + ')' : 'P(y=1)', cols[j]);
      }
      A.txt(ctx, many ? 'output layer: 4 units + softmax' : 'output layer: 1 unit + sigmoid',
        600, 40, { align: 'center', size: 12.5, w: 700, fill: P.soft });
      if (many) A.txt(ctx, 'these four always add to 1.00', 600, 280, { align: 'center', size: 11.5, fill: P.faint });
      A.txt(ctx, 'Handwritten digits (0–9) need 10 units. Defect types, animal species, disease grades — same shape.',
        70, 300, { size: 11.5, fill: P.faint });
    }
    A.bind(c, render); render();
  });

  /* ============================================================
     7. Softmax, step by step
     ============================================================ */
  A.def('softmax', function (root) {
    var c = A.canvas(root, 760, 340), ctx = c.ctx;
    var z = [2.0, 1.0, 0.1, -0.5];
    var bar = A.ctrls(root), ro = A.readout(root);
    z.forEach(function (v, i) {
      A.slider(bar, { label: 'z<sub>' + (i + 1) + '</sub>', min: -4, max: 4, value: v,
        on: function (nv) { z[i] = nv; render(); } });
    });
    function calc() {
      var e = z.map(Math.exp), s = e.reduce(function (a, b) { return a + b; }, 0);
      return { e: e, s: s, a: e.map(function (v) { return v / s; }) };
    }
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var r = calc(), cols = [P.a, P.b, P.g, P.p];
      var stages = [
        { t: 'z — raw scores', x: 60, get: function (i) { return z[i]; }, max: 4, min: -4 },
        { t: 'e^z — always positive', x: 300, get: function (i) { return r.e[i]; }, max: Math.max.apply(null, r.e), min: 0 },
        { t: 'e^z / Σ — adds to 1', x: 540, get: function (i) { return r.a[i]; }, max: 1, min: 0 }
      ];
      stages.forEach(function (st, si) {
        A.txt(ctx, st.t, st.x + 80, 34, { align: 'center', size: 12.5, w: 700, fill: P.soft });
        for (var i = 0; i < 4; i++) {
          var y = 56 + i * 52;
          var v = st.get(i);
          var frac = si === 0 ? (v - st.min) / (st.max - st.min) : v / (st.max || 1);
          A.rr(ctx, st.x, y, 160, 34, 6); ctx.fillStyle = P.sunk; ctx.fill();
          A.rr(ctx, st.x, y, Math.max(3, 160 * A.clamp(frac, 0, 1)), 34, 6);
          ctx.fillStyle = cols[i]; ctx.globalAlpha = si === 2 ? .85 : .45; ctx.fill(); ctx.globalAlpha = 1;
          A.txt(ctx, si === 0 ? v.toFixed(2) : si === 1 ? v.toFixed(2) : (v * 100).toFixed(1) + '%',
            st.x + 152, y + 22, { align: 'right', size: 12.5, mono: true, w: 700, fill: P.ink });
          if (si === 0) A.txt(ctx, 'class ' + (i + 1), st.x - 10, y + 22, { align: 'right', size: 11, fill: P.faint });
        }
        if (si < 2) A.arrow(ctx, st.x + 172, 140, st.x + 216, 140, P.line, 2);
      });
      A.txt(ctx, 'exp', 250, 130, { align: 'center', size: 11, fill: P.faint });
      A.txt(ctx, '÷ Σ = ' + r.s.toFixed(2), 490, 130, { align: 'center', size: 11, mono: true, fill: P.faint });
      A.txt(ctx, 'Σ = ' + r.a.reduce(function (a, b) { return a + b; }, 0).toFixed(3),
        620, 290, { align: 'center', size: 13, mono: true, w: 700, fill: P.g });
      A.txt(ctx, 'Two jobs: exp makes everything positive, dividing by the total makes them add to exactly 1.',
        60, 290, { size: 12, w: 600, fill: P.soft });
      A.txt(ctx, 'Raise one z and every other probability falls — they compete for a fixed budget of 1.',
        60, 312, { size: 12, fill: P.faint });
      ro.set('a<sub>j</sub> = e<sup>z<sub>j</sub></sup> / (e<sup>z<sub>1</sub></sup> + e<sup>z<sub>2</sub></sup> + e<sup>z<sub>3</sub></sup> + e<sup>z<sub>4</sub></sup>)' +
        '\na = [' + r.a.map(function (v) { return v.toFixed(3); }).join(', ') + ']   sum = <b>' +
        r.a.reduce(function (a, b) { return a + b; }, 0).toFixed(3) + '</b>');
    }
    A.bind(c, render); render();
  });

})();

/* ---------- part 2 : softmax network, stability, Adam, layers, calculus ---------- */
(function () {
  'use strict';

  /* ============================================================
     8. Softmax output layer inside a network
     ============================================================ */
  A.def('softmaxnn', function (root) {
    var c = A.canvas(root, 760, 340), ctx = c.ctx;
    var zs = [1.6, 0.4, -0.6, 2.1, -1.2, 0.1, 0.9, -0.3, 1.1, -2.0];
    function soft() {
      var e = zs.map(Math.exp), s = e.reduce(function (a, b) { return a + b; }, 0);
      return e.map(function (v) { return v / s; });
    }
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var a = soft();
      var h1 = A.col(140, 5, 60, 280, 15), h2 = A.col(300, 4, 90, 250, 15), o = A.col(470, 10, 40, 300, 12);
      var i, j;
      for (i = 0; i < 5; i++) for (j = 0; j < 4; j++) A.link(ctx, h1[i], h2[j], P.line, .7, .3);
      for (i = 0; i < 4; i++) for (j = 0; j < 10; j++) A.link(ctx, h2[i], o[j], P.line, .7, .25);
      for (i = 0; i < 5; i++) A.neuron(ctx, h1[i], .5, P, null, null, P.p);
      for (i = 0; i < 4; i++) A.neuron(ctx, h2[i], .6, P, null, null, P.p);
      var hot = Math.floor((t * .7) % 10);
      for (j = 0; j < 10; j++) A.neuron(ctx, o[j], a[j] * 3, P, null, null, j === hot ? P.a : P.b);
      /* the softmax box spanning all ten */
      ctx.save(); ctx.setLineDash([5, 4]); ctx.strokeStyle = P.a; ctx.lineWidth = 2;
      A.rr(ctx, 452, 24, 36, 292, 12); ctx.stroke(); ctx.restore();
      A.txt(ctx, 'softmax', 470, 18, { align: 'center', size: 11.5, w: 700, fill: P.a });
      /* probability bars */
      for (j = 0; j < 10; j++) {
        var y = o[j].y;
        A.txt(ctx, String(j), 512, y + 4, { size: 11, mono: true, fill: P.faint });
        A.rr(ctx, 528, y - 7, Math.max(2, 170 * a[j]), 14, 4);
        ctx.fillStyle = j === hot ? P.a : P.b; ctx.globalAlpha = .8; ctx.fill(); ctx.globalAlpha = 1;
        A.txt(ctx, (a[j] * 100).toFixed(1) + '%', 715, y + 4, { align: 'right', size: 10.5, mono: true, fill: P.soft });
      }
      A.txt(ctx, 'z' + hot + ' feeds a' + hot + ' — but so does every other z. Softmax is the ONE activation where',
        140, 322, { size: 11.5, fill: P.faint });
      A.txt(ctx, 'each output depends on all the others.', 140, 336, { size: 11.5, w: 700, fill: P.a });
      A.txt(ctx, '25 → 15 → 10 with softmax', 140, 30, { size: 12.5, w: 700, fill: P.soft });
    }
    A.bind(c, function () { render(lt); });
    var lt = 0; A.loop(c.cv, function (t) { lt = t; render(t); });
  });

  /* ============================================================
     9. Numerical stability of softmax / sigmoid
     ============================================================ */
  A.def('numstab', function (root) {
    var c = A.canvas(root, 760, 320), ctx = c.ctx;
    var z = 12;
    var bar = A.ctrls(root), ro = A.readout(root);
    A.slider(bar, { label: 'z =', min: -40, max: 40, step: .5, value: z,
      fmt: function (v) { return v.toFixed(1); }, on: function (v) { z = v; render(); } });
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var a = A.sig(z);
      var a32 = Math.fround(a);                 /* what float32 would hold */
      var lossRound = -Math.log(Math.max(a32, 0) || Number.MIN_VALUE);
      var lossDirect = Math.log(1 + Math.exp(-z));  /* softplus(-z), the stable form */
      var err = Math.abs(lossRound - lossDirect);
      A.txt(ctx, 'the round-trip: z → a → log(a)', 60, 40, { size: 13, w: 700, fill: P.r });
      A.txt(ctx, 'the direct route: z → loss', 420, 40, { size: 13, w: 700, fill: P.g });
      A.rr(ctx, 50, 56, 330, 180, 10); ctx.fillStyle = P.rS; ctx.fill();
      ctx.strokeStyle = P.r; ctx.lineWidth = 1.4; ctx.stroke();
      A.rr(ctx, 410, 56, 300, 180, 10); ctx.fillStyle = P.gS; ctx.fill();
      ctx.strokeStyle = P.g; ctx.lineWidth = 1.4; ctx.stroke();
      var rows = [
        ['z', z.toFixed(1)],
        ['a = 1/(1+e^−z)', a.toPrecision(12)],
        ['stored as float32', a32.toPrecision(12)],
        ['loss = −log(a)', lossRound.toPrecision(8)]
      ];
      rows.forEach(function (r, i) {
        A.txt(ctx, r[0], 66, 84 + i * 38, { size: 12, fill: P.soft });
        A.txt(ctx, r[1], 364, 84 + i * 38, { align: 'right', size: 12.5, mono: true, w: 700, fill: P.ink });
      });
      var rows2 = [
        ['z', z.toFixed(1)],
        ['loss = log(1 + e^−z)', lossDirect.toPrecision(12)],
        ['(never builds a at all)', ''],
        ['error avoided', err === 0 ? 'none yet' : err.toPrecision(3)]
      ];
      rows2.forEach(function (r, i) {
        A.txt(ctx, r[0], 426, 84 + i * 38, { size: 12, fill: P.soft });
        A.txt(ctx, r[1], 694, 84 + i * 38, { align: 'right', size: 12.5, mono: true, w: 700,
          fill: i === 3 && err > 1e-6 ? P.r : P.ink });
      });
      var warnMsg = a32 === 1 ? 'a rounded to exactly 1.0 → −log(1) = 0 → the loss VANISHED'
        : a32 === 0 ? 'a rounded to exactly 0 → −log(0) = ∞ → NaN'
        : err > 1e-5 ? 'rounding has already eaten ' + err.toPrecision(2) + ' of loss'
        : 'still safe at this z — push the slider past ±16';
      A.txt(ctx, warnMsg, 380, 264, { align: 'center', size: 13, w: 700,
        fill: (a32 === 1 || a32 === 0 || err > 1e-5) ? P.r : P.faint });
      A.txt(ctx, 'The fix: let the framework keep the raw z (the "logits") and compute the loss in one step.',
        380, 292, { align: 'center', size: 12, fill: P.soft });
      ro.set('<b>from_logits=True</b> tells Keras: the output layer is <code>linear</code>, and the loss function' +
        ' should do the sigmoid/softmax itself — algebraically rearranged so nothing ever rounds to 0 or 1.' +
        '\nDense(10, activation=<b>"linear"</b>)  +  SparseCategoricalCrossentropy(<b>from_logits=True</b>)');
    }
    A.bind(c, render); render();
  });

  /* ============================================================
     10. Multi-label vs multi-class
     ============================================================ */
  A.def('multilabel', function (root) {
    var c = A.canvas(root, 760, 300), ctx = c.ctx;
    var has = [true, false, true];
    var bar = A.ctrls(root);
    ['car', 'bus', 'pedestrian'].forEach(function (n, i) {
      A.toggle(bar, n, function (v) { has[i] = v; render(); }, has[i]);
    });
    function render() {
      var P = A.pal(); c.clear(P.panel);
      /* the "photo" */
      A.rr(ctx, 50, 60, 250, 170, 10); ctx.fillStyle = P.sunk; ctx.fill();
      ctx.strokeStyle = P.line; ctx.lineWidth = 1.4; ctx.stroke();
      A.txt(ctx, 'one photo', 175, 46, { align: 'center', size: 12.5, w: 700, fill: P.soft });
      ctx.save(); ctx.beginPath(); A.rr(ctx, 50, 60, 250, 170, 10); ctx.clip();
      A.line(ctx, 50, 200, 300, 200, P.line, 2);
      if (has[0]) { A.rr(ctx, 80, 160, 70, 34, 8); ctx.fillStyle = P.a; ctx.fill();
        A.dot(ctx, 96, 196, 7, P.ink); A.dot(ctx, 134, 196, 7, P.ink);
        A.txt(ctx, 'car', 115, 182, { align: 'center', size: 11, w: 700, fill: '#fff' }); }
      if (has[1]) { A.rr(ctx, 180, 130, 90, 64, 6); ctx.fillStyle = P.b; ctx.fill();
        A.dot(ctx, 198, 196, 8, P.ink); A.dot(ctx, 252, 196, 8, P.ink);
        A.txt(ctx, 'bus', 225, 168, { align: 'center', size: 11, w: 700, fill: '#fff' }); }
      if (has[2]) { A.dot(ctx, 160, 158, 8, P.g);
        ctx.strokeStyle = P.g; ctx.lineWidth = 4;
        ctx.beginPath(); ctx.moveTo(160, 166); ctx.lineTo(160, 186);
        ctx.moveTo(160, 186); ctx.lineTo(152, 200); ctx.moveTo(160, 186); ctx.lineTo(168, 200);
        ctx.moveTo(150, 174); ctx.lineTo(170, 174); ctx.stroke(); }
      ctx.restore();
      /* three independent sigmoids */
      var o = A.col(520, 3, 80, 210, 26), names = ['car?', 'bus?', 'pedestrian?'];
      for (var j = 0; j < 3; j++) {
        var p = has[j] ? .93 - j * .04 : .05 + j * .02;
        A.neuron(ctx, o[j], p, P, p.toFixed(2), names[j], has[j] ? P.g : P.line);
        A.txt(ctx, 'sigmoid', o[j].x + 44, o[j].y + 4, { size: 11, mono: true, fill: P.faint });
        A.arrow(ctx, 320, 145, o[j].x - 30, o[j].y, P.line, 1.4);
      }
      A.txt(ctx, 'three separate yes/no questions', 560, 46, { align: 'center', size: 12.5, w: 700, fill: P.soft });
      var sum = 0; for (j = 0; j < 3; j++) sum += has[j] ? .93 - j * .04 : .05 + j * .02;
      A.txt(ctx, 'they add to ' + sum.toFixed(2) + ' — and that is fine, nobody said they must add to 1',
        380, 254, { align: 'center', size: 12, fill: P.faint });
      A.txt(ctx, 'MULTI-LABEL: several answers can be true at once → several sigmoids.  ' +
        'MULTI-CLASS: exactly one is true → one softmax.',
        380, 280, { align: 'center', size: 11.5, w: 600, fill: P.soft });
    }
    A.bind(c, render); render();
  });

  /* ============================================================
     11. Gradient descent vs Adam on a ravine
     ============================================================ */
  A.def('adam', function (root) {
    var c = A.canvas(root, 760, 340), ctx = c.ctx;
    var lr = 0.06, K = 18;   /* curvature ratio: makes a long narrow valley */
    var bar = A.ctrls(root), ro = A.readout(root);
    A.slider(bar, { label: 'learning rate α', min: .005, max: .12, step: .005, value: lr,
      fmt: function (v) { return v.toFixed(3); }, on: function (v) { lr = v; reset(); } });
    A.button(bar, 'restart', function () { reset(); });
    var gd, ad;
    function reset() {
      gd = { w: [-2.6, 0.9], path: [] };
      ad = { w: [-2.6, 0.9], m: [0, 0], v: [0, 0], t: 0, path: [], lr: [lr, lr] };
    }
    reset();
    function grad(w) { return [w[0], K * w[1]]; }
    function stepGD() {
      var g = grad(gd.w);
      gd.w = [gd.w[0] - lr * g[0], gd.w[1] - lr * g[1]];
      gd.path.push(gd.w.slice()); if (gd.path.length > 220) gd.path.shift();
    }
    function stepAdam() {
      var g = grad(ad.w), b1 = .9, b2 = .999, eps = 1e-8;
      ad.t++;
      for (var i = 0; i < 2; i++) {
        ad.m[i] = b1 * ad.m[i] + (1 - b1) * g[i];
        ad.v[i] = b2 * ad.v[i] + (1 - b2) * g[i] * g[i];
        var mh = ad.m[i] / (1 - Math.pow(b1, ad.t)), vh = ad.v[i] / (1 - Math.pow(b2, ad.t));
        var stepSize = lr * 3 / (Math.sqrt(vh) + eps);
        ad.lr[i] = stepSize;
        ad.w[i] -= stepSize * mh;
      }
      ad.path.push(ad.w.slice()); if (ad.path.length > 220) ad.path.shift();
    }
    var frame = 0;
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var box = { x: 70, y: 30, w: 620, h: 230 };
      var S = A.axes(ctx, box, [-3, 3], [-1.2, 1.2], {
        xticks: 6, yticks: 4, xfmt: function (v) { return v.toFixed(0); },
        yfmt: function (v) { return v.toFixed(1); }, xlab: 'w₁ (gentle direction)', ylab: 'w₂ (steep)'
      });
      /* contours of J = 0.5(w1^2 + K w2^2) */
      for (var L = 0.15; L < 6; L *= 1.9) {
        ctx.save(); ctx.strokeStyle = P.lineSoft; ctx.lineWidth = 1; ctx.beginPath();
        for (var th = 0; th <= 6.3; th += .06) {
          var x = Math.sqrt(2 * L) * Math.cos(th), y = Math.sqrt(2 * L / K) * Math.sin(th);
          var px = S.X(x), py = S.Y(y);
          th === 0 ? ctx.moveTo(px, py) : ctx.lineTo(px, py);
        }
        ctx.closePath(); ctx.stroke(); ctx.restore();
      }
      A.dot(ctx, S.X(0), S.Y(0), 5, P.g);
      A.txt(ctx, 'minimum', S.X(0) + 10, S.Y(0) - 8, { size: 11, fill: P.g });
      function trail(path, colr) {
        ctx.save(); ctx.strokeStyle = colr; ctx.lineWidth = 1.8; ctx.beginPath();
        path.forEach(function (p, i) {
          var px = S.X(A.clamp(p[0], -3, 3)), py = S.Y(A.clamp(p[1], -1.2, 1.2));
          i === 0 ? ctx.moveTo(px, py) : ctx.lineTo(px, py);
        });
        ctx.stroke(); ctx.restore();
        var last = path[path.length - 1];
        if (last) A.dot(ctx, S.X(A.clamp(last[0], -3, 3)), S.Y(A.clamp(last[1], -1.2, 1.2)), 6, colr);
      }
      trail(gd.path, P.r); trail(ad.path, P.g);
      A.txt(ctx, '● plain gradient descent', 90, 52, { size: 12, w: 700, fill: P.r });
      A.txt(ctx, '● Adam', 90, 70, { size: 12, w: 700, fill: P.g });
      var dGD = Math.hypot(gd.w[0], gd.w[1]), dAD = Math.hypot(ad.w[0], ad.w[1]);
      A.txt(ctx, 'steps taken: ' + ad.t, 70, 292, { size: 12, mono: true, fill: P.faint });
      A.txt(ctx, 'distance to minimum — GD: ' + dGD.toFixed(3) + '   Adam: ' + dAD.toFixed(3),
        70, 312, { size: 12.5, mono: true, fill: P.soft });
      A.txt(ctx, "Adam's own step size:  w₁ " + ad.lr[0].toFixed(3) + '   w₂ ' + ad.lr[1].toFixed(3),
        70, 332, { size: 12.5, mono: true, fill: P.g });
      ro.set('Plain GD must use ONE α for both directions: big enough for w₁ makes it bounce in w₂.' +
        '\nAdam keeps a separate step size per parameter and grows it when the gradient is consistent — ' +
        'so it takes long strides along the valley floor and small careful ones across it.');
    }
    A.bind(c, render);
    A.loop(c.cv, function () {
      frame++;
      if (frame % 3 === 0) { stepGD(); stepAdam(); }
      if (ad.t > 200) reset();
      render();
    });
  });

  /* ============================================================
     12. A convolutional layer
     ============================================================ */
  A.def('conv', function (root) {
    var c = A.canvas(root, 760, 320), ctx = c.ctx;
    var N = 20, sig = [];
    for (var i = 0; i < N; i++)
      sig.push(0.5 + 0.42 * Math.sin(i * .9) * Math.exp(-Math.pow((i - 7) / 4, 2)) +
        0.3 * Math.exp(-Math.pow((i - 14) / 1.4, 2)));
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var W = 5, nUnits = N - W + 1;
      var hot = Math.floor((t * 1.1) % nUnits);
      var x0 = 60, cw = 30, base = 190;
      /* the input signal */
      for (var i = 0; i < N; i++) {
        var h = sig[i] * 110;
        var inWin = i >= hot && i < hot + W;
        A.rr(ctx, x0 + i * cw, base - h, cw - 4, h, 3);
        ctx.fillStyle = inWin ? P.a : P.sunk; ctx.fill();
        ctx.strokeStyle = inWin ? P.a : P.lineSoft; ctx.lineWidth = 1; ctx.stroke();
      }
      A.line(ctx, x0 - 6, base, x0 + N * cw, base, P.line, 1.4);
      A.txt(ctx, 'the input — an EKG trace, read left to right', x0, 40, { size: 12.5, w: 700, fill: P.soft });
      /* the window */
      ctx.save(); ctx.strokeStyle = P.a; ctx.lineWidth = 2.4; ctx.setLineDash([5, 3]);
      A.rr(ctx, x0 + hot * cw - 4, 60, W * cw, base - 52, 8); ctx.stroke(); ctx.restore();
      /* the units */
      var uy = 250;
      for (var j = 0; j < nUnits; j++) {
        var s = 0; for (var k = 0; k < W; k++) s += sig[j + k];
        s = A.clamp((s / W - .35) * 2.6, 0, 1);
        var ux = x0 + (j + (W - 1) / 2) * cw + cw / 2 - 2;
        A.dot(ctx, ux, uy, j === hot ? 11 : 7, j === hot ? P.a : P.b);
        ctx.save(); ctx.globalAlpha = .35 + .65 * s;
        A.dot(ctx, ux, uy, j === hot ? 9 : 5, j === hot ? P.a : P.b); ctx.restore();
        if (j === hot) {
          A.arrow(ctx, x0 + (hot + (W - 1) / 2) * cw + cw / 2 - 2, base + 10, ux, uy - 14, P.a, 1.8);
        }
      }
      A.txt(ctx, 'a convolutional layer — each unit only looks at a small window', x0, 288,
        { size: 12.5, w: 700, fill: P.soft });
      A.txt(ctx, 'unit ' + (hot + 1) + ' sees inputs ' + (hot + 1) + '–' + (hot + W) +
        '  ·  fewer weights, faster, less overfitting, and the same detector reused everywhere',
        x0, 308, { size: 11.5, fill: P.faint });
    }
    A.bind(c, function () { render(lt); });
    var lt = 0; A.loop(c.cv, function (t) { lt = t; render(t); });
  });

  /* ============================================================
     13. What a derivative is
     ============================================================ */
  A.def('deriv', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var w = 2, eps = 0.9;
    var bar = A.ctrls(root), ro = A.readout(root);
    A.slider(bar, { label: 'w =', min: -3, max: 3, value: w, on: function (v) { w = v; render(); } });
    A.slider(bar, { label: 'tiny nudge ε =', min: .02, max: 1.2, value: eps,
      fmt: function (v) { return v.toFixed(2); }, on: function (v) { eps = v; render(); } });
    function J(x) { return x * x; }
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var box = { x: 70, y: 30, w: 620, h: 220 };
      var S = A.axes(ctx, box, [-3.4, 3.4], [-.5, 9.5], {
        xticks: 4, yticks: 4, xfmt: function (v) { return v.toFixed(0); },
        yfmt: function (v) { return v.toFixed(0); }, xlab: 'w', ylab: 'J(w) = w²'
      });
      A.plot(ctx, S, [-3.2, 3.2], J, P.p, 2.6);
      var y1 = J(w), y2 = J(w + eps);
      /* rise / run triangle */
      ctx.save(); ctx.fillStyle = P.aS; ctx.globalAlpha = .8;
      ctx.beginPath(); ctx.moveTo(S.X(w), S.Y(y1)); ctx.lineTo(S.X(w + eps), S.Y(y1));
      ctx.lineTo(S.X(w + eps), S.Y(y2)); ctx.closePath(); ctx.fill(); ctx.restore();
      A.line(ctx, S.X(w), S.Y(y1), S.X(w + eps), S.Y(y1), P.a, 2);
      A.line(ctx, S.X(w + eps), S.Y(y1), S.X(w + eps), S.Y(y2), P.a, 2);
      A.txt(ctx, 'run = ' + eps.toFixed(2), (S.X(w) + S.X(w + eps)) / 2, S.Y(y1) + 18,
        { align: 'center', size: 11.5, mono: true, fill: P.a });
      A.txt(ctx, 'rise = ' + (y2 - y1).toFixed(3), S.X(w + eps) + 8, (S.Y(y1) + S.Y(y2)) / 2,
        { size: 11.5, mono: true, fill: P.a });
      /* true tangent */
      var d = 2 * w;
      A.line(ctx, S.X(w - 1.6), S.Y(y1 - d * 1.6), S.X(w + 1.6), S.Y(y1 + d * 1.6), P.g, 2, [6, 4]);
      A.dot(ctx, S.X(w), S.Y(y1), 6, P.g);
      var slopeApprox = (y2 - y1) / eps;
      A.txt(ctx, 'measured slope  rise/run = ' + slopeApprox.toFixed(3), 70, 284,
        { size: 12.5, mono: true, fill: P.a });
      A.txt(ctx, 'true derivative dJ/dw = 2w = ' + d.toFixed(3), 70, 304,
        { size: 12.5, mono: true, w: 700, fill: P.g });
      A.txt(ctx, 'shrink ε and the two numbers meet. THAT is all a derivative is.',
        70, 324, { size: 12, fill: P.faint });
      ro.set('“If I nudge w up by a tiny ε, how much does J go up?” — divided by ε.' +
        '\nGradient descent uses the sign to know which way is downhill, and the size to know how far to step.');
    }
    A.bind(c, render); render();
  });

  /* ============================================================
     14. Computation graph — forward then backward
     ============================================================ */
  A.def('compgraph', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var w = 3, b = 1, x = -2, y = 2;
    var step = 0, playing = true;
    var ro = A.readout(root);
    function vals() {
      var cv = w * x, a = cv + b, d = a - y, J = 0.5 * d * d;
      return { c: cv, a: a, d: d, J: J };
    }
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      if (playing) step = Math.floor((t * .55) % 8);
      var V = vals();
      var nodes = [
        { x: 90,  y: 120, lab: 'c = w·x', val: V.c.toFixed(1), sub: 'w=' + w + ', x=' + x },
        { x: 260, y: 120, lab: 'a = c + b', val: V.a.toFixed(1), sub: 'b=' + b },
        { x: 430, y: 120, lab: 'd = a − y', val: V.d.toFixed(1), sub: 'y=' + y },
        { x: 610, y: 120, lab: 'J = ½d²', val: V.J.toFixed(1), sub: 'the cost' }
      ];
      /* derivatives, right to left */
      var dJ_dd = V.d, dd_da = 1, dJ_da = dJ_dd * dd_da, da_dc = 1, dJ_dc = dJ_da * da_dc, dJ_dw = dJ_dc * x;
      var derivs = [dJ_dw, dJ_dc, dJ_da, dJ_dd];
      var fwd = step < 4;
      nodes.forEach(function (n, i) {
        var on = fwd ? i === step : i === (7 - step);
        A.rr(ctx, n.x - 62, n.y - 34, 124, 68, 10);
        ctx.fillStyle = on ? (fwd ? P.bS : P.aS) : P.sunk; ctx.fill();
        ctx.strokeStyle = on ? (fwd ? P.b : P.a) : P.lineSoft; ctx.lineWidth = on ? 2.4 : 1; ctx.stroke();
        A.txt(ctx, n.lab, n.x, n.y - 12, { align: 'center', size: 12.5, mono: true, w: 700, fill: P.soft });
        A.txt(ctx, n.val, n.x, n.y + 14, { align: 'center', size: 20, mono: true, w: 700,
          fill: on ? (fwd ? P.b : P.a) : P.ink });
        A.txt(ctx, n.sub, n.x, n.y + 50, { align: 'center', size: 11, fill: P.faint });
        if (i < 3) {
          if (fwd) A.arrow(ctx, n.x + 64, n.y, nodes[i + 1].x - 64, n.y, step > i ? P.b : P.line, 2);
          else A.arrow(ctx, nodes[i + 1].x - 64, n.y - 46, n.x + 64, n.y - 46, (7 - step) <= i ? P.a : P.line, 2);
        }
      });
      if (!fwd) {
        var k = 7 - step;
        A.txt(ctx, '∂J/∂' + ['w', 'c', 'a', 'd'][k] + ' = ' + derivs[k].toFixed(2),
          nodes[k].x, 50, { align: 'center', size: 14, mono: true, w: 700, fill: P.a });
      }
      A.txt(ctx, fwd ? 'FORWARD: numbers flow left to right' : 'BACKWARD: derivatives flow right to left',
        380, 245, { align: 'center', size: 14, w: 700, fill: fwd ? P.b : P.a });
      A.txt(ctx, fwd ? 'each node computes its value from the ones before it'
        : 'each node multiplies by its own local slope — that is the chain rule',
        380, 268, { align: 'center', size: 12, fill: P.faint });
      A.txt(ctx, 'Backprop costs about the same as one forward pass — that is why training is affordable at all.',
        380, 305, { align: 'center', size: 12, w: 600, fill: P.soft });
      ro.set('Forward:  c = w·x = ' + V.c.toFixed(1) + '   a = c + b = ' + V.a.toFixed(1) +
        '   d = a − y = ' + V.d.toFixed(1) + '   J = ½d² = ' + V.J.toFixed(1) +
        '\nBackward: ∂J/∂d = d = ' + dJ_dd.toFixed(1) + '  →  ∂J/∂a = ' + dJ_da.toFixed(1) +
        '  →  ∂J/∂c = ' + dJ_dc.toFixed(1) + '  →  <b>∂J/∂w = ∂J/∂c · x = ' + dJ_dw.toFixed(1) + '</b>');
    }
    var bar = A.ctrls(root);
    A.toggle(bar, 'auto', function (on) { playing = on; }, true);
    A.button(bar, 'step ›', function () { playing = false; step = (step + 1) % 8; render(lt); });
    A.bind(c, function () { render(lt); });
    var lt = 0; A.loop(c.cv, function (t) { lt = t; render(t); });
  });

  /* ============================================================
     15. Backprop through a larger network
     ============================================================ */
  A.def('bignet', function (root) {
    var c = A.canvas(root, 760, 320), ctx = c.ctx;
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var sizes = [4, 5, 5, 3, 1];
      var cols = sizes.map(function (n, i) { return A.col(90 + i * 145, n, 70, 250, 16); });
      var cyc = (t * .32) % 2, fwd = cyc < 1;
      var prog = (cyc % 1) * 4;
      var li, i, j;
      for (li = 1; li < cols.length; li++)
        for (i = 0; i < cols[li - 1].length; i++)
          for (j = 0; j < cols[li].length; j++) {
            var reached = fwd ? prog > li - 1 : prog > (cols.length - 1 - li);
            A.link(ctx, cols[li - 1][i], cols[li][j], reached ? (fwd ? P.b : P.a) : P.line,
              reached ? 1.1 : .6, reached ? .55 : .18);
          }
      for (li = 0; li < cols.length; li++)
        for (j = 0; j < cols[li].length; j++) {
          var lit = fwd ? prog > li - .3 : prog > (cols.length - 1 - li) - .3;
          A.neuron(ctx, cols[li][j], lit ? .85 : .12, P, null, null,
            fwd ? (li === 0 ? P.b : P.p) : P.a);
        }
      /* moving pulses */
      var layerNow = Math.min(3, Math.floor(prog));
      for (i = 0; i < cols[layerNow].length; i++)
        for (j = 0; j < cols[layerNow + 1].length; j++) {
          var u = prog % 1;
          if (fwd) A.pulse(ctx, cols[layerNow][i], cols[layerNow + 1][j], u, P.b, 2.6);
          else {
            var Li = cols.length - 2 - layerNow;
            A.pulse(ctx, cols[Li + 1][j % cols[Li + 1].length], cols[Li][i % cols[Li].length], 1 - u, P.a, 2.6);
          }
        }
      A.txt(ctx, fwd ? 'FORWARD PASS — compute every activation, left to right'
        : 'BACKWARD PASS — compute every derivative, right to left',
        380, 40, { align: 'center', size: 14, w: 700, fill: fwd ? P.b : P.a });
      A.txt(ctx, fwd ? 'cost: one multiply-add per weight'
        : 'cost: about two multiply-adds per weight — not one per weight per parameter',
        380, 282, { align: 'center', size: 12, fill: P.faint });
      A.txt(ctx, 'Naively nudging each weight one at a time would cost N forward passes. Backprop gets all N derivatives in one sweep.',
        380, 304, { align: 'center', size: 11.5, w: 600, fill: P.soft });
    }
    A.bind(c, function () { render(lt); });
    var lt = 0; A.loop(c.cv, function (t) { lt = t; render(t); });
  });

})();
