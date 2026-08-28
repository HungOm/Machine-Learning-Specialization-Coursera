/* Widgets for Foundations / Week 1 — the maths you actually need.
   All names are prefixed f… so they never collide with the course widgets. */
(function () {
  'use strict';

  /* ============================================================
     1. A function is a machine
     ============================================================ */
  A.def('ffnmachine', function (root) {
    var c = A.canvas(root, 760, 300), ctx = c.ctx;
    var x = 3, which = 0;
    var fns = [
      { n: 'f(x) = 2x + 1', f: function (v) { return 2 * v + 1; }, say: 'double it, then add one' },
      { n: 'f(x) = x²', f: function (v) { return v * v; }, say: 'multiply it by itself' },
      { n: 'f(x) = x / 2', f: function (v) { return v / 2; }, say: 'halve it' }
    ];
    var bar = A.ctrls(root), ro = A.readout(root);
    A.slider(bar, { label: 'x =', min: -5, max: 8, step: .5, value: x,
      fmt: function (v) { return v.toFixed(1); }, on: function (v) { x = v; render(); } });
    fns.forEach(function (f, i) { A.button(bar, f.n, function () { which = i; sync(); render(); }); });
    function sync() { bar.querySelectorAll('button').forEach(function (b, i) { b.classList.toggle('primary', i === which); }); }
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var F = fns[which], y = F.f(x);
      /* the machine */
      A.rr(ctx, 300, 90, 170, 110, 12);
      ctx.fillStyle = P.aS; ctx.fill(); ctx.strokeStyle = P.a; ctx.lineWidth = 2.4; ctx.stroke();
      A.txt(ctx, 'f', 385, 140, { align: 'center', size: 40, w: 700, fill: P.a });
      A.txt(ctx, F.say, 385, 172, { align: 'center', size: 11.5, fill: P.a });
      /* input */
      A.rr(ctx, 90, 118, 110, 54, 9);
      ctx.fillStyle = P.bS; ctx.fill(); ctx.strokeStyle = P.b; ctx.lineWidth = 1.8; ctx.stroke();
      A.txt(ctx, x.toFixed(1), 145, 152, { align: 'center', size: 22, mono: true, w: 700, fill: P.b });
      A.txt(ctx, 'x — the input', 145, 106, { align: 'center', size: 11.5, w: 700, fill: P.b });
      A.arrow(ctx, 206, 145, 294, 145, P.b, 2.4);
      var u = (t * .9) % 1;
      A.dot(ctx, A.lerp(206, 294, u), 145, 5, P.b);
      /* output */
      A.rr(ctx, 570, 118, 110, 54, 9);
      ctx.fillStyle = P.gS; ctx.fill(); ctx.strokeStyle = P.g; ctx.lineWidth = 1.8; ctx.stroke();
      A.txt(ctx, y.toFixed(2), 625, 152, { align: 'center', size: 22, mono: true, w: 700, fill: P.g });
      A.txt(ctx, 'f(x) — the output', 625, 106, { align: 'center', size: 11.5, w: 700, fill: P.g });
      A.arrow(ctx, 476, 145, 564, 145, P.g, 2.4);
      A.dot(ctx, A.lerp(476, 564, u), 145, 5, P.g);
      A.txt(ctx, 'Put a number in one end. A different number comes out the other.', 60, 42,
        { size: 13, w: 700, fill: P.soft });
      A.txt(ctx, 'Same input always gives the same output. That is the whole rule.', 60, 226,
        { size: 12, fill: P.faint });
      A.txt(ctx, '“f(3)” does NOT mean f times 3. It means “put 3 into the machine f”.', 60, 250,
        { size: 12, w: 700, fill: P.r });
      A.txt(ctx, 'Other letters get used too — g, h, J, σ. They are all just machines with names.',
        60, 274, { size: 12, fill: P.faint });
      ro.set('<b>' + F.n + '</b>  with x = ' + x.toFixed(1) + '  gives  <b>' + y.toFixed(2) + '</b>' +
        '\nIn code this is a <code>def</code>: <code>def f(x): return ' +
        ['2*x + 1', 'x**2', 'x/2'][which] + '</code>');
    }
    sync();
    A.autoplay(root, c, render);
  });

  /* ============================================================
     2. Reading a graph
     ============================================================ */
  A.def('freadgraph', function (root) {
    var c = A.canvas(root, 760, 340), ctx = c.ctx;
    var qx = 2.2;
    var bar = A.ctrls(root), ro = A.readout(root);
    A.slider(bar, { label: 'x =', min: -3, max: 5, step: .1, value: qx,
      fmt: function (v) { return v.toFixed(1); }, on: function (v) { qx = v; render(); } });
    function f(x) { return 0.6 * x * x - 1.2 * x + 1.5; }
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var box = { x: 90, y: 46, w: 560, h: 210 };
      var S = A.axes(ctx, box, [-3.4, 5.4], [-1, 10], {
        xticks: 4, yticks: 4, xfmt: function (v) { return v.toFixed(0); },
        yfmt: function (v) { return v.toFixed(0); },
        xlab: 'x  — read along the bottom', ylab: 'y  — read up the side'
      });
      A.line(ctx, box.x, S.Y(0), box.x + box.w, S.Y(0), P.line, 1.4);
      A.line(ctx, S.X(0), box.y, S.X(0), box.y + box.h, P.line, 1.4);
      A.txt(ctx, 'origin (0, 0)', S.X(0) + 8, S.Y(0) + 16, { size: 10.5, fill: P.faint });
      A.plot(ctx, S, [-3.4, 5.4], f, P.a, 2.8);
      var qy = f(qx);
      A.line(ctx, S.X(qx), S.Y(0), S.X(qx), S.Y(qy), P.b, 1.8, [4, 3]);
      A.line(ctx, S.X(0), S.Y(qy), S.X(qx), S.Y(qy), P.g, 1.8, [4, 3]);
      A.dot(ctx, S.X(qx), S.Y(qy), 7, P.a);
      A.txt(ctx, qx.toFixed(1), S.X(qx), S.Y(0) + 18, { align: 'center', size: 12, mono: true, w: 700, fill: P.b });
      A.txt(ctx, qy.toFixed(2), S.X(0) - 10, S.Y(qy) + 4, { align: 'right', size: 12, mono: true, w: 700, fill: P.g });
      A.txt(ctx, '(' + qx.toFixed(1) + ', ' + qy.toFixed(2) + ')', S.X(qx) + 12, S.Y(qy) - 10,
        { size: 13, mono: true, w: 700, fill: P.a });
      A.txt(ctx, 'A graph is a picture of a function. Every dot on the curve is one input paired with its output.',
        90, 292, { size: 12.5, w: 700, fill: P.soft });
      A.txt(ctx, 'Go ACROSS to your x, then UP to the curve, then LEFT to read the answer. Always that order.',
        90, 314, { size: 12, fill: P.faint });
      A.txt(ctx, 'A point is written (x, y) — across first, up second. Everyone mixes this up once.',
        90, 334, { size: 12, fill: P.faint });
      ro.set('x = ' + qx.toFixed(1) + '  →  y = f(' + qx.toFixed(1) + ') = <b>' + qy.toFixed(3) + '</b>' +
        '\nIn NumPy you draw this with two arrays: <code>xs = np.linspace(-3, 5, 200)</code> then ' +
        '<code>ys = f(xs)</code> then <code>plt.plot(xs, ys)</code>.');
    }
    A.bind(c, render); render();
  });

  /* ============================================================
     3. The Greek alphabet you will actually meet
     ============================================================ */
  A.def('fgreek', function (root) {
    var c = A.canvas(root, 760, 540), ctx = c.ctx;
    var G = [
      ['α', 'alpha', 'AL-fa', 'learning rate — step size'],
      ['β', 'beta', 'BAY-ta', 'decay rates in Adam'],
      ['γ', 'gamma', 'GAM-a', 'discount — how patient an agent is'],
      ['ε', 'epsilon', 'EP-si-lon', 'a tiny number, or a threshold'],
      ['θ', 'theta', 'THAY-ta', 'parameters (another name for w and b)'],
      ['λ', 'lambda', 'LAM-da', 'regularisation strength — stiffness'],
      ['μ', 'mu', 'mew', 'the mean — the average'],
      ['π', 'pi', 'pie', 'a policy in RL (NOT 3.14159 there)'],
      ['σ', 'sigma', 'SIG-ma', 'standard deviation — spread'],
      ['σ²', 'sigma squared', '—', 'variance'],
      ['τ', 'tau', 'taw', 'soft-update rate'],
      ['Σ', 'capital sigma', 'SIG-ma', 'ADD all of these up'],
      ['Π', 'capital pi', 'pie', 'MULTIPLY all of these together'],
      ['∂', 'partial', 'PAR-shal', 'rate of change of'],
      ['∇', 'nabla / del', 'NAB-la', 'the gradient — all the slopes at once'],
      ['∈', 'element of', '—', '“is one of”'],
      ['≈', 'approximately', '—', '“roughly equals”'],
      ['∞', 'infinity', 'in-FIN-i-ty', 'endlessly large']
    ];
    /* Clip text to a pixel width instead of trusting it to fit. Two
       independently-positioned strings on one canvas row never collide if
       neither is ever drawn wider than the space it was given — that is the
       bug this replaces: the meaning column used to be right-aligned with no
       width limit, so a long one ran backwards straight into the pronunciation
       column next to it. */
    function clip(text, maxW, size, weight) {
      ctx.save();
      ctx.font = (weight || 500) + ' ' + size + 'px -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif';
      var w = ctx.measureText(text).width;
      if (w <= maxW) { ctx.restore(); return text; }
      var s = text;
      while (s.length > 1 && ctx.measureText(s + '…').width > maxW) s = s.slice(0, -1);
      ctx.restore();
      return s + '…';
    }
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var hot = Math.floor((t * .8) % G.length);
      A.txt(ctx, 'Symbols are not maths. They are shorthand — and nobody can read them until', 40, 34,
        { size: 12.5, w: 700, fill: P.soft });
      A.txt(ctx, 'somebody says them out loud once.', 40, 54, { size: 12.5, w: 700, fill: P.soft });
      G.forEach(function (g, i) {
        var col = i % 2, row = Math.floor(i / 2);
        var x = 40 + col * 355, y = 74 + row * 46, on = i === hot;
        A.rr(ctx, x, y, 340, 40, 6);
        ctx.fillStyle = on ? P.aS : P.sunk; ctx.fill();
        ctx.strokeStyle = on ? P.a : P.lineSoft; ctx.lineWidth = on ? 1.6 : 1; ctx.stroke();
        /* line 1: symbol · name (left) · pronunciation (right) — both short,
           always with room between them, so this pair can never collide */
        A.txt(ctx, g[0], x + 20, y + 18, { align: 'center', size: 16, w: 700, fill: on ? P.a : P.soft });
        A.txt(ctx, g[1], x + 42, y + 17, { size: 12, w: on ? 700 : 500, fill: on ? P.a : P.soft });
        A.txt(ctx, g[2] === '—' ? '' : '“' + g[2] + '”', x + 320, y + 17,
          { align: 'right', size: 10.5, fill: P.faint });
        /* line 2: the meaning, alone on its own line, clipped to the row's
           own width so it can never reach back up into line 1 */
        A.txt(ctx, clip(g[3], 290, 10.5), x + 42, y + 33, { size: 10.5, fill: P.faint });
      });
      A.txt(ctx, 'Say the highlighted one out loud. That is genuinely the whole exercise.',
        40, 74 + 9 * 46 + 14, { size: 12, w: 700, fill: P.a });
    }
    A.autoplay(root, c, render);
  });

  /* ============================================================
     4. Slope — rise over run
     ============================================================ */
  A.def('fslope', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var m = 1.5, b = 1;
    var bar = A.ctrls(root), ro = A.readout(root);
    A.slider(bar, { label: 'slope', min: -3, max: 3, step: .1, value: m,
      fmt: function (v) { return v.toFixed(1); }, on: function (v) { m = v; render(); } });
    A.slider(bar, { label: 'start height', min: -3, max: 5, step: .1, value: b,
      fmt: function (v) { return v.toFixed(1); }, on: function (v) { b = v; render(); } });
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var box = { x: 80, y: 44, w: 400, h: 220 };
      var S = A.axes(ctx, box, [-1, 6], [-3, 8], {
        xticks: 4, yticks: 4, xfmt: function (v) { return v.toFixed(0); },
        yfmt: function (v) { return v.toFixed(0); }, xlab: 'x', ylab: 'y'
      });
      A.line(ctx, box.x, S.Y(0), box.x + box.w, S.Y(0), P.line, 1.2);
      A.plot(ctx, S, [-1, 6], function (x) { return m * x + b; }, P.a, 2.8);
      /* the triangle */
      var x0 = 1.5, x1 = 3.5, y0 = m * x0 + b, y1 = m * x1 + b;
      ctx.save(); ctx.fillStyle = P.bS; ctx.globalAlpha = .85;
      ctx.beginPath(); ctx.moveTo(S.X(x0), S.Y(y0)); ctx.lineTo(S.X(x1), S.Y(y0));
      ctx.lineTo(S.X(x1), S.Y(y1)); ctx.closePath(); ctx.fill(); ctx.restore();
      A.line(ctx, S.X(x0), S.Y(y0), S.X(x1), S.Y(y0), P.b, 2.4);
      A.line(ctx, S.X(x1), S.Y(y0), S.X(x1), S.Y(y1), P.g, 2.4);
      A.txt(ctx, 'run = 2', (S.X(x0) + S.X(x1)) / 2, S.Y(y0) + 18,
        { align: 'center', size: 12, mono: true, w: 700, fill: P.b });
      A.txt(ctx, 'rise = ' + (y1 - y0).toFixed(1), S.X(x1) + 8, (S.Y(y0) + S.Y(y1)) / 2,
        { size: 12, mono: true, w: 700, fill: P.g });
      A.dot(ctx, S.X(0), S.Y(b), 6, P.a);
      /* the sum */
      A.txt(ctx, 'slope  =', 540, 90, { size: 14, w: 700, fill: P.soft });
      A.txt(ctx, 'rise', 620, 82, { align: 'center', size: 14, mono: true, fill: P.g });
      A.line(ctx, 596, 90, 646, 90, P.soft, 1.6);
      A.txt(ctx, 'run', 620, 106, { align: 'center', size: 14, mono: true, fill: P.b });
      A.txt(ctx, '=  ' + (y1 - y0).toFixed(1) + ' / 2  =  ' + m.toFixed(2), 540, 138,
        { size: 14, mono: true, w: 700, fill: P.a });
      A.txt(ctx, m > 0 ? 'positive → goes UP to the right'
        : m < 0 ? 'negative → goes DOWN to the right' : 'zero → flat',
        540, 172, { size: 12, w: 700, fill: m > 0 ? P.g : m < 0 ? P.r : P.faint });
      A.txt(ctx, 'the line crosses the y-axis at ' + b.toFixed(1), 540, 196, { size: 11.5, fill: P.faint });
      A.txt(ctx, 'Slope answers one question: if I step 1 to the right, how far up do I go?',
        80, 292, { size: 12.5, w: 700, fill: P.soft });
      A.txt(ctx, 'Steeper line = bigger number. Downhill = negative number. Flat = zero.',
        80, 314, { size: 12, fill: P.faint });
      ro.set('y = <b>' + m.toFixed(1) + '</b>x + <b>' + b.toFixed(1) + '</b>' +
        '\nIn machine learning this exact line is written <b>f(x) = wx + b</b> — w is the slope, ' +
        'b is the start height. Same thing, different letters.');
    }
    A.bind(c, render); render();
  });

  /* ============================================================
     5. What a derivative actually is
     ============================================================ */
  A.def('fderiv', function (root) {
    var c = A.canvas(root, 760, 340), ctx = c.ctx;
    var x0 = 1.4, h = 1.6;
    var bar = A.ctrls(root), ro = A.readout(root);
    A.slider(bar, { label: 'point x', min: -2, max: 2.6, step: .05, value: x0,
      fmt: function (v) { return v.toFixed(2); }, on: function (v) { x0 = v; render(); } });
    A.slider(bar, { label: 'gap h — shrink it', min: .02, max: 1.8, step: .01, value: h,
      fmt: function (v) { return v.toFixed(2); }, on: function (v) { h = v; render(); } });
    function f(x) { return x * x; }
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var box = { x: 80, y: 40, w: 420, h: 220 };
      var S = A.axes(ctx, box, [-2.4, 3.2], [-0.5, 9], {
        xticks: 4, yticks: 4, xfmt: function (v) { return v.toFixed(0); },
        yfmt: function (v) { return v.toFixed(0); }, xlab: 'x', ylab: 'f(x) = x²'
      });
      A.plot(ctx, S, [-2.4, 3.2], f, P.p, 2.8);
      var y0 = f(x0), y1 = f(x0 + h);
      /* the rise/run triangle across the gap */
      ctx.save(); ctx.fillStyle = P.aS; ctx.globalAlpha = .8;
      ctx.beginPath(); ctx.moveTo(S.X(x0), S.Y(y0)); ctx.lineTo(S.X(x0 + h), S.Y(y0));
      ctx.lineTo(S.X(x0 + h), S.Y(y1)); ctx.closePath(); ctx.fill(); ctx.restore();
      /* the chord (secant) */
      var slopeApprox = (y1 - y0) / h;
      A.line(ctx, S.X(x0 - 1), S.Y(y0 - slopeApprox), S.X(x0 + h + 1), S.Y(y1 + slopeApprox),
        P.a, 2.2);
      /* the true tangent */
      var d = 2 * x0;
      A.line(ctx, S.X(x0 - 1.4), S.Y(y0 - d * 1.4), S.X(x0 + 1.4), S.Y(y0 + d * 1.4), P.g, 2, [6, 4]);
      A.dot(ctx, S.X(x0), S.Y(y0), 6.5, P.a);
      A.dot(ctx, S.X(x0 + h), S.Y(y1), 5, P.a);
      A.legend(root, [[P.a, 'the line through two points (a chord)'], [P.g, 'the true slope AT the point (the tangent)']]);
      /* the numbers */
      var mx = 540;
      A.txt(ctx, 'rise  = f(x+h) − f(x)', mx, 76, { size: 11.5, mono: true, fill: P.faint });
      A.txt(ctx, '      = ' + (y1 - y0).toFixed(4), mx, 94, { size: 12, mono: true, fill: P.soft });
      A.txt(ctx, 'run   = h = ' + h.toFixed(2), mx, 118, { size: 12, mono: true, fill: P.soft });
      A.txt(ctx, 'rise/run = ' + slopeApprox.toFixed(4), mx, 148,
        { size: 14, mono: true, w: 700, fill: P.a });
      A.txt(ctx, 'true slope 2x = ' + d.toFixed(4), mx, 174,
        { size: 14, mono: true, w: 700, fill: P.g });
      A.txt(ctx, 'difference: ' + Math.abs(slopeApprox - d).toFixed(4), mx, 200,
        { size: 11.5, mono: true, fill: Math.abs(slopeApprox - d) < .05 ? P.g : P.faint });
      A.txt(ctx, h < 0.1 ? '↑ shrink h and they meet' : 'now shrink the gap h →', mx, 228,
        { size: 11.5, w: 700, fill: P.a });
      A.txt(ctx, 'A derivative is the slope of a curve at ONE exact point.', 80, 292,
        { size: 12.5, w: 700, fill: P.soft });
      A.txt(ctx, 'You cannot do rise-over-run at a single point — you need two. So take two points very close',
        80, 312, { size: 12, fill: P.faint });
      A.txt(ctx, 'together, and squeeze the gap towards zero. Whatever number it settles on is the derivative.',
        80, 332, { size: 12, fill: P.faint });
      ro.set('<b>f′(x) = lim<sub>h→0</sub> [ f(x+h) − f(x) ] / h</b>  — that “lim” just means “as h shrinks to nothing”.' +
        '\nFor f(x) = x² the answer is always <b>2x</b>. You do not need to prove that; you need to know ' +
        'that a derivative is a <b>slope</b>, and that its sign says which way is uphill.');
    }
    A.bind(c, render); render();
  });

  /* ============================================================
     6. Partial derivatives
     ============================================================ */
  A.def('fpartial', function (root) {
    var c = A.canvas(root, 760, 340), ctx = c.ctx;
    var w = 1.2, b = 0.6, which = 0;
    var bar = A.ctrls(root), ro = A.readout(root);
    A.slider(bar, { label: 'w', min: -2.5, max: 2.5, step: .05, value: w,
      fmt: function (v) { return v.toFixed(2); }, on: function (v) { w = v; render(); } });
    A.slider(bar, { label: 'b', min: -2.5, max: 2.5, step: .05, value: b,
      fmt: function (v) { return v.toFixed(2); }, on: function (v) { b = v; render(); } });
    ['freeze b, wiggle w', 'freeze w, wiggle b'].forEach(function (n, i) {
      A.button(bar, n, function () { which = i; sync(); render(); });
    });
    function sync() { bar.querySelectorAll('button').forEach(function (b2, i) { b2.classList.toggle('primary', i === which); }); }
    function J(ww, bb) { return ww * ww + 2 * bb * bb + 1; }
    function render() {
      var P = A.pal(); c.clear(P.panel);
      /* contour map of J */
      var box = { x: 70, y: 46, w: 250, h: 210 };
      var S = A.axes(ctx, box, [-2.6, 2.6], [-2.6, 2.6], { xticks: 4, yticks: 4, xlab: 'w', ylab: 'b' });
      for (var L = .4; L < 14; L *= 1.7) {
        ctx.save(); ctx.strokeStyle = P.lineSoft; ctx.lineWidth = 1; ctx.beginPath();
        for (var th = 0; th <= 6.3; th += .05) {
          var xx = Math.sqrt(L) * Math.cos(th), yy = Math.sqrt(L / 2) * Math.sin(th);
          var px = S.X(xx), py = S.Y(yy);
          th === 0 ? ctx.moveTo(px, py) : ctx.lineTo(px, py);
        }
        ctx.closePath(); ctx.stroke(); ctx.restore();
      }
      A.dot(ctx, S.X(w), S.Y(b), 7, P.a);
      if (which === 0) A.line(ctx, box.x, S.Y(b), box.x + box.w, S.Y(b), P.b, 2, [5, 3]);
      else A.line(ctx, S.X(w), box.y, S.X(w), box.y + box.h, P.g, 2, [5, 3]);
      A.txt(ctx, 'the whole landscape', box.x + box.w / 2, 36, { align: 'center', size: 12, w: 700, fill: P.soft });
      A.txt(ctx, which === 0 ? 'walking along the blue line only' : 'walking along the green line only',
        box.x + box.w / 2, 278, { align: 'center', size: 11, fill: which === 0 ? P.b : P.g });
      /* the slice, as an ordinary 1-D curve */
      var b2 = { x: 400, y: 46, w: 300, h: 210 };
      var S2 = A.axes(ctx, b2, [-2.6, 2.6], [0, 16], {
        xticks: 4, yticks: 4, xfmt: function (v) { return v.toFixed(0); },
        yfmt: function (v) { return v.toFixed(0); },
        xlab: which === 0 ? 'w  (b held still)' : 'b  (w held still)', ylab: 'J'
      });
      var slice = which === 0 ? function (v) { return J(v, b); } : function (v) { return J(w, v); };
      A.plot(ctx, S2, [-2.6, 2.6], slice, which === 0 ? P.b : P.g, 2.8);
      var here = which === 0 ? w : b;
      var slope = which === 0 ? 2 * w : 4 * b;
      A.dot(ctx, S2.X(here), S2.Y(slice(here)), 6.5, P.a);
      A.line(ctx, S2.X(here - .9), S2.Y(slice(here) - slope * .9),
        S2.X(here + .9), S2.Y(slice(here) + slope * .9), P.a, 2, [5, 3]);
      A.txt(ctx, 'one slice through it', b2.x + b2.w / 2, 36, { align: 'center', size: 12, w: 700, fill: P.soft });
      A.txt(ctx, 'Freeze everything except one variable, and a hill becomes an ordinary curve you already',
        70, 296, { size: 12.5, w: 700, fill: P.soft });
      A.txt(ctx, 'know how to find the slope of. That is all a partial derivative is.', 70, 316,
        { size: 12.5, w: 700, fill: P.soft });
      A.txt(ctx, 'The curly ∂ instead of a straight d is the only way you can tell — it means “others held still”.',
        70, 336, { size: 11.5, fill: P.faint });
      ro.set('∂J/∂w = <b>' + (2 * w).toFixed(2) + '</b>   (b treated as a fixed number)' +
        '\n∂J/∂b = <b>' + (4 * b).toFixed(2) + '</b>   (w treated as a fixed number)' +
        '\nCollect them into one list and you have the <b>gradient</b>: ∇J = [' +
        (2 * w).toFixed(2) + ', ' + (4 * b).toFixed(2) + ']');
    }
    sync(); A.bind(c, render); render();
  });

  /* ============================================================
     7. Sigma notation is a for loop
     ============================================================ */
  A.def('fsigma', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var vals = [3, 1, 4, 1, 5];
    var ro = A.readout(root);
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var k = Math.floor((t * 1.1) % (vals.length + 2));
      /* the notation */
      A.txt(ctx, 'Σ', 100, 130, { align: 'center', size: 60, w: 700, fill: P.a });
      A.txt(ctx, 'i = 1', 100, 168, { align: 'center', size: 13, fill: P.a });
      A.txt(ctx, '5', 100, 74, { align: 'center', size: 13, fill: P.a });
      A.txt(ctx, 'x', 148, 130, { size: 34, fill: P.soft });
      A.txt(ctx, 'i', 168, 140, { size: 16, fill: P.soft });
      A.txt(ctx, 'start here', 100, 192, { align: 'center', size: 10, fill: P.faint });
      A.txt(ctx, 'stop here', 100, 56, { align: 'center', size: 10, fill: P.faint });
      A.txt(ctx, 'add up this', 158, 176, { align: 'center', size: 10, fill: P.faint });
      A.arrow(ctx, 210, 130, 250, 130, P.line, 2);
      /* the unrolled version */
      var terms = [], sum = 0;
      for (var i = 0; i < Math.min(k, 5); i++) { terms.push('x' + (i + 1)); sum += vals[i]; }
      A.txt(ctx, 'means exactly this:', 280, 70, { size: 12.5, w: 700, fill: P.soft });
      A.txt(ctx, 'x₁ + x₂ + x₃ + x₄ + x₅', 280, 100, { size: 18, mono: true, fill: P.a });
      A.txt(ctx, 'with x = [3, 1, 4, 1, 5]:', 280, 134, { size: 12, fill: P.faint });
      for (i = 0; i < 5; i++) {
        var on = i < k;
        var x = 280 + i * 52;
        A.rr(ctx, x, 146, 44, 40, 6);
        ctx.fillStyle = on ? P.aS : P.sunk; ctx.fill();
        ctx.strokeStyle = on ? P.a : P.lineSoft; ctx.lineWidth = on ? 1.8 : 1; ctx.stroke();
        A.txt(ctx, String(vals[i]), x + 22, 172, { align: 'center', size: 17, mono: true, w: 700,
          fill: on ? P.a : P.faint });
        A.txt(ctx, 'x' + (i + 1), x + 22, 142, { align: 'center', size: 10, fill: P.faint });
      }
      A.txt(ctx, 'running total: ' + sum, 280, 212, { size: 15, mono: true, w: 700, fill: P.g });
      if (k > 5) A.txt(ctx, '= 14', 280, 240, { size: 22, mono: true, w: 700, fill: P.g });
      /* the code */
      A.txt(ctx, 'the same thing, in code', 40, 250, { size: 12, w: 700, fill: P.soft });
      A.txt(ctx, 'total = 0', 40, 274, { size: 12.5, mono: true, fill: P.faint });
      A.txt(ctx, 'for i in range(5):', 40, 292, { size: 12.5, mono: true, fill: P.faint });
      A.txt(ctx, '    total = total + x[i]', 40, 310, { size: 12.5, mono: true, fill: P.faint });
      A.txt(ctx, 'or just:  np.sum(x)', 40, 332, { size: 12.5, mono: true, w: 700, fill: P.g });
      ro.set('<b>Σ is a for loop wearing a hat.</b> The letter under it is the counter, the number on top ' +
        'is where it stops, and what follows is the thing you add up each time.' +
        '\nWhen you see Σ in a formula, read it as: “now add this up for every example”.');
    }
    A.autoplay(root, c, render);
  });

  /* ============================================================
     8. Pi notation (multiply them all)
     ============================================================ */
  A.def('fpi', function (root) {
    var c = A.canvas(root, 760, 300), ctx = c.ctx;
    var vals = [0.5, 0.4, 0.6, 0.3];
    var ro = A.readout(root);
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var k = Math.floor((t * 1.1) % (vals.length + 2));
      A.txt(ctx, 'Π', 90, 122, { align: 'center', size: 58, w: 700, fill: P.p });
      A.txt(ctx, 'j = 1', 90, 158, { align: 'center', size: 12.5, fill: P.p });
      A.txt(ctx, '4', 90, 70, { align: 'center', size: 12.5, fill: P.p });
      A.txt(ctx, 'p', 134, 122, { size: 30, fill: P.soft });
      A.txt(ctx, 'j', 152, 132, { size: 15, fill: P.soft });
      A.arrow(ctx, 190, 120, 232, 120, P.line, 2);
      A.txt(ctx, 'same idea as Σ — but MULTIPLY instead of add', 262, 66,
        { size: 12.5, w: 700, fill: P.soft });
      var prod = 1, shown = Math.min(k, 4);
      for (var i = 0; i < 4; i++) {
        var on = i < k, x = 262 + i * 76;
        A.rr(ctx, x, 86, 62, 40, 6);
        ctx.fillStyle = on ? P.pS : P.sunk; ctx.fill();
        ctx.strokeStyle = on ? P.p : P.lineSoft; ctx.lineWidth = on ? 1.8 : 1; ctx.stroke();
        A.txt(ctx, vals[i].toFixed(1), x + 31, 112, { align: 'center', size: 16, mono: true, w: 700,
          fill: on ? P.p : P.faint });
        if (i < 3) A.txt(ctx, '×', x + 68, 112, { align: 'center', size: 16, fill: P.faint });
        if (on) prod *= vals[i];
      }
      A.txt(ctx, 'running product: ' + (shown ? prod.toFixed(4) : '1'), 262, 152,
        { size: 14, mono: true, w: 700, fill: P.p });
      if (k > 4) A.txt(ctx, '= 0.036', 262, 180, { size: 20, mono: true, w: 700, fill: P.g });
      A.txt(ctx, 'Notice what happens: four ordinary-looking numbers multiply down to something tiny.',
        40, 222, { size: 12.5, w: 700, fill: P.soft });
      A.txt(ctx, 'That is exactly the point in anomaly detection — being slightly odd in four ways at once',
        40, 244, { size: 12, fill: P.faint });
      A.txt(ctx, 'is far rarer than being slightly odd in one way.', 40, 264, { size: 12, fill: P.faint });
      A.txt(ctx, 'in code:  np.prod(p)', 40, 290, { size: 12.5, mono: true, w: 700, fill: P.g });
      ro.set('<b>Π</b> (capital pi) means multiply them all together. Nothing to do with 3.14159 — that is ' +
        'lowercase π.' +
        '\nMultiplying many numbers below 1 gets very small very fast, which is why code often adds up ' +
        '<b>logs</b> instead: log(a×b) = log(a) + log(b).');
    }
    A.autoplay(root, c, render);
  });

  /* ============================================================
     9. Vectors
     ============================================================ */
  A.def('fvector', function (root) {
    var c = A.canvas(root, 760, 340), ctx = c.ctx;
    var vx = 3, vy = 2;
    var bar = A.ctrls(root), ro = A.readout(root);
    A.slider(bar, { label: 'first number', min: -4, max: 5, step: .5, value: vx,
      fmt: function (v) { return v.toFixed(1); }, on: function (v) { vx = v; render(); } });
    A.slider(bar, { label: 'second number', min: -4, max: 5, step: .5, value: vy,
      fmt: function (v) { return v.toFixed(1); }, on: function (v) { vy = v; render(); } });
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var box = { x: 80, y: 44, w: 260, h: 220 };
      var S = A.axes(ctx, box, [-4.5, 5.5], [-4.5, 5.5], { xticks: 4, yticks: 4, xlab: 'x₁', ylab: 'x₂' });
      A.line(ctx, box.x, S.Y(0), box.x + box.w, S.Y(0), P.line, 1.2);
      A.line(ctx, S.X(0), box.y, S.X(0), box.y + box.h, P.line, 1.2);
      A.line(ctx, S.X(0), S.Y(0), S.X(vx), S.Y(0), P.b, 2, [4, 3]);
      A.line(ctx, S.X(vx), S.Y(0), S.X(vx), S.Y(vy), P.g, 2, [4, 3]);
      A.arrow(ctx, S.X(0), S.Y(0), S.X(vx), S.Y(vy), P.a, 3);
      A.txt(ctx, vx.toFixed(1), (S.X(0) + S.X(vx)) / 2, S.Y(0) + 16,
        { align: 'center', size: 11.5, mono: true, w: 700, fill: P.b });
      A.txt(ctx, vy.toFixed(1), S.X(vx) + 8, (S.Y(0) + S.Y(vy)) / 2,
        { size: 11.5, mono: true, w: 700, fill: P.g });
      /* the written forms */
      var mx = 400;
      A.txt(ctx, 'three ways to write the same thing', mx, 62, { size: 12.5, w: 700, fill: P.soft });
      A.txt(ctx, 'x = [' + vx.toFixed(1) + ', ' + vy.toFixed(1) + ']', mx, 96,
        { size: 17, mono: true, w: 700, fill: P.a });
      A.overArrow(ctx, mx, 82, 10, P.a);   /* no font has U+20D7, so draw it */
      A.txt(ctx, 'a list of numbers', mx + 200, 96, { align: 'right', size: 10.5, fill: P.faint });
      A.txt(ctx, 'an arrow from the origin', mx, 126, { size: 13, fill: P.soft });
      A.txt(ctx, 'a point in space', mx, 150, { size: 13, fill: P.soft });
      A.txt(ctx, 'the little arrow above it (or bold x) just says “this is a list, not one number”',
        mx, 178, { size: 10.5, fill: P.faint });
      /* length */
      var len = Math.hypot(vx, vy);
      A.txt(ctx, 'length  ‖x‖ = √(' + vx.toFixed(1) + '² + ' + vy.toFixed(1) + '²) = ' + len.toFixed(3),
        mx, 214, { size: 12.5, mono: true, w: 700, fill: P.g });
      A.txt(ctx, 'np.linalg.norm(x)', mx, 236, { size: 12, mono: true, fill: P.faint });
      A.txt(ctx, 'In machine learning a vector is almost always just “one row of your spreadsheet”.',
        80, 296, { size: 12.5, w: 700, fill: P.soft });
      A.txt(ctx, 'Two numbers you can draw. Four hundred numbers you cannot — and the maths is identical.',
        80, 318, { size: 12, fill: P.faint });
      ro.set('<code>x = np.array([' + vx.toFixed(1) + ', ' + vy.toFixed(1) + '])</code>   ·   ' +
        '<code>x.shape</code> → <code>(2,)</code>   ·   <code>len(x)</code> → <code>2</code>' +
        '\nThe number of entries is the number of <b>dimensions</b>. A house with 4 features is a ' +
        '4-dimensional vector — perfectly ordinary, just impossible to draw.');
    }
    A.bind(c, render); render();
  });

  /* ============================================================
     10. The dot product, and what it means
     ============================================================ */
  A.def('fdot', function (root) {
    var c = A.canvas(root, 760, 340), ctx = c.ctx;
    var ang = 0.6;
    var bar = A.ctrls(root), ro = A.readout(root);
    A.slider(bar, { label: 'angle between them', min: 0, max: 3.14, step: .01, value: ang,
      fmt: function (v) { return (v * 180 / Math.PI).toFixed(0) + '°'; },
      on: function (v) { ang = v; render(); } });
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var a = [3, 0], b = [3 * Math.cos(ang), 3 * Math.sin(ang)];
      var dp = a[0] * b[0] + a[1] * b[1];
      /* step by step */
      var k = Math.floor((t * .9) % 4);
      var A1 = [1, 2, 3], W1 = [4, 5, 6];
      A.txt(ctx, 'step one: pair them up and multiply', 40, 40, { size: 12.5, w: 700, fill: P.soft });
      for (var i = 0; i < 3; i++) {
        var x = 46 + i * 92, on = i === k;
        A.rr(ctx, x, 54, 40, 34, 5);
        ctx.fillStyle = on ? P.aS : P.sunk; ctx.fill();
        ctx.strokeStyle = on ? P.a : P.lineSoft; ctx.stroke();
        A.txt(ctx, String(A1[i]), x + 20, 77, { align: 'center', size: 15, mono: true, w: 700,
          fill: on ? P.a : P.soft });
        A.txt(ctx, '×', x + 46, 77, { align: 'center', size: 14, fill: P.faint });
        A.rr(ctx, x + 54, 54, 40, 34, 5);
        ctx.fillStyle = on ? P.aS : P.sunk; ctx.fill();
        ctx.strokeStyle = on ? P.a : P.lineSoft; ctx.stroke();
        A.txt(ctx, String(W1[i]), x + 74, 77, { align: 'center', size: 15, mono: true, w: 700,
          fill: on ? P.a : P.soft });
        A.txt(ctx, '= ' + (A1[i] * W1[i]), x + 40, 108, { align: 'center', size: 12.5, mono: true,
          fill: i <= k ? P.g : P.faint });
      }
      A.txt(ctx, 'step two: add those up', 40, 140, { size: 12.5, w: 700, fill: P.soft });
      A.txt(ctx, '4 + 10 + 18 = 32', 46, 166, { size: 17, mono: true, w: 700, fill: P.g });
      A.txt(ctx, 'two lists in → ONE number out', 46, 190, { size: 11.5, fill: P.faint });
      A.txt(ctx, 'np.dot(a, w)   ·   a @ w   ·   (a * w).sum()', 46, 216,
        { size: 12, mono: true, w: 700, fill: P.b });
      /* geometry */
      var cx = 570, cy = 150, R = 84;
      A.line(ctx, cx - 100, cy, cx + 110, cy, P.lineSoft, 1);
      A.arrow(ctx, cx, cy, cx + R, cy, P.b, 3);
      A.arrow(ctx, cx, cy, cx + Math.cos(-ang) * R, cy + Math.sin(-ang) * R, P.a, 3);
      ctx.save(); ctx.strokeStyle = P.faint; ctx.lineWidth = 1.4;
      ctx.beginPath(); ctx.arc(cx, cy, 30, -ang, 0); ctx.stroke(); ctx.restore();
      A.txt(ctx, (ang * 180 / Math.PI).toFixed(0) + '°', cx + 40, cy - 12,
        { size: 11.5, w: 700, fill: P.faint });
      var meaning = ang < 0.5 ? ['pointing the SAME way → big positive', P.g]
        : ang < 1.4 ? ['partly aligned → smaller positive', P.m]
        : Math.abs(ang - Math.PI / 2) < 0.12 ? ['at right angles → exactly ZERO', P.b]
        : ['pointing OPPOSITE ways → negative', P.r];
      A.txt(ctx, 'a · b = ' + dp.toFixed(2), cx, 254, { align: 'center', size: 16, mono: true,
        w: 700, fill: meaning[1] });
      A.txt(ctx, meaning[0], cx, 276, { align: 'center', size: 11.5, w: 700, fill: meaning[1] });
      A.txt(ctx, 'The dot product measures how much two arrows point the same way.', 40, 252,
        { size: 12, w: 700, fill: P.soft });
      A.txt(ctx, 'A neuron uses it to ask: how much does this input resemble the pattern I am looking for?',
        40, 300, { size: 12, fill: P.faint });
      A.txt(ctx, 'Both lists must be the SAME length — otherwise there is nothing to pair up.',
        40, 322, { size: 12, w: 700, fill: P.r });
      ro.set('<b>a · b = a₁b₁ + a₂b₂ + … + aₙbₙ</b>   (multiply the pairs, add them up)' +
        '\nGeometrically: <b>a · b = |a| |b| cos θ</b>. Positive = aligned, zero = perpendicular, ' +
        'negative = opposed.');
    }
    A.autoplay(root, c, render);
  });

})();

/* ---------- part 2 : matrices, exp/log, probability, statistics ---------- */
(function () {
  'use strict';

  /* ============================================================
     11. Matrices and shapes
     ============================================================ */
  A.def('fmatrix', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var rows = 3, cols = 4;
    var bar = A.ctrls(root), ro = A.readout(root);
    A.slider(bar, { label: 'rows', min: 1, max: 5, step: 1, value: rows,
      fmt: function (v) { return v.toFixed(0); }, on: function (v) { rows = v; render(); } });
    A.slider(bar, { label: 'columns', min: 1, max: 6, step: 1, value: cols,
      fmt: function (v) { return v.toFixed(0); }, on: function (v) { cols = v; render(); } });
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var n = rows * cols, k = Math.floor((t * 1.2) % n);
      var ki = Math.floor(k / cols), kj = k % cols;
      var cw = 62, ch = 44;
      var x0 = 300 - cols * cw / 2, y0 = 100;
      A.matrix(ctx, x0, y0, rows, cols, cw, ch, P,
        function (i, j) { return String((i + 1) * 10 + (j + 1)); },
        { state: function (i, j) { return (i === ki && j === kj) ? 1 : (i === ki ? 2 : 0); },
          size: 13, shape: 'shape = (' + rows + ', ' + cols + ')' });
      /* row/col labels */
      for (var i = 0; i < rows; i++)
        A.txt(ctx, 'row ' + i, x0 - 12, y0 + i * ch + 26, { align: 'right', size: 10.5,
          fill: i === ki ? P.b : P.faint });
      for (var j = 0; j < cols; j++)
        A.txt(ctx, 'col ' + j, x0 + j * cw + 30, y0 - 12, { align: 'center', size: 10.5,
          fill: j === kj ? P.a : P.faint });
      A.txt(ctx, 'A matrix is a grid of numbers. Nothing more mysterious than a spreadsheet.',
        40, 44, { size: 13, w: 700, fill: P.soft });
      A.txt(ctx, 'Its SHAPE is (rows, columns) — always that order.', 40, 66, { size: 12, fill: P.faint });
      var mx = 470;
      A.txt(ctx, 'M[' + ki + ', ' + kj + '] = ' + ((ki + 1) * 10 + (kj + 1)), mx, 110,
        { size: 17, mono: true, w: 700, fill: P.a });
      A.txt(ctx, 'row first, then column', mx, 132, { size: 10.5, fill: P.faint });
      A.txt(ctx, 'M.shape → (' + rows + ', ' + cols + ')', mx, 164, { size: 13, mono: true, fill: P.soft });
      A.txt(ctx, 'M.shape[0] → ' + rows + '   (rows)', mx, 186, { size: 12, mono: true, fill: P.b });
      A.txt(ctx, 'M.shape[1] → ' + cols + '   (columns)', mx, 206, { size: 12, mono: true, fill: P.a });
      A.txt(ctx, 'M.size → ' + (rows * cols) + '   (total numbers)', mx, 226, { size: 12, mono: true, fill: P.faint });
      A.txt(ctx, 'In machine learning, almost always: rows = your examples, columns = your features.',
        40, 280, { size: 12.5, w: 700, fill: P.a });
      A.txt(ctx, 'So a (1000, 4) matrix is 1000 houses, each described by 4 numbers.', 40, 302,
        { size: 12, fill: P.faint });
      A.txt(ctx, 'Counting from ZERO is a programming thing. Maths counts from 1. Both appear in this course.',
        40, 324, { size: 11.5, fill: P.faint });
      ro.set('<code>M = np.zeros((' + rows + ', ' + cols + '))</code>  ·  ' +
        '<code>M[' + ki + ', ' + kj + ']</code> one number  ·  ' +
        '<code>M[' + ki + ']</code> a whole row  ·  <code>M[:, ' + kj + ']</code> a whole column' +
        '\nA <b>vector</b> is just a matrix with one row (or one column). A single number is called a ' +
        '<b>scalar</b>.');
    }
    A.autoplay(root, c, render);
  });

  /* ============================================================
     12. Matrix multiplication, step by step
     ============================================================ */
  A.def('fmatmul', function (root) {
    var c = A.canvas(root, 760, 340), ctx = c.ctx;
    var Am = [[1, 2], [3, 4], [5, 6]];      /* 3x2 */
    var Bm = [[7, 8, 9], [10, 11, 12]];     /* 2x3 */
    var R = 3, K = 2, C = 3;
    function cell(i, j) { var s = 0; for (var k = 0; k < K; k++) s += Am[i][k] * Bm[k][j]; return s; }
    var ro = A.readout(root);
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var n = R * C, idx = Math.floor((t * .85) % (n + 2));
      var cur = Math.min(idx, n - 1), ci = Math.floor(cur / C), cj = cur % C;
      var done = idx >= n;
      A.matrix(ctx, 50, 96, R, K, 52, 44, P, function (i, k) { return String(Am[i][k]); },
        { state: function (i) { return (!done && i === ci) ? 1 : 0; }, label: 'A  (3 × 2)', size: 13 });
      A.txt(ctx, '×', 186, 152, { align: 'center', size: 22, fill: P.faint });
      A.matrix(ctx, 216, 74, K, C, 52, 44, P, function (k, j) { return String(Bm[k][j]); },
        { state: function (k, j) { return (!done && j === cj) ? 2 : 0; }, label: 'B  (2 × 3)', size: 13 });
      A.txt(ctx, '=', 400, 152, { align: 'center', size: 22, fill: P.faint });
      A.matrix(ctx, 430, 96, R, C, 56, 44, P,
        function (i, j) { var o = i * C + j; return (o < idx || done) ? String(cell(i, j)) : ''; },
        { state: function (i, j) { var o = i * C + j; return (o === cur && !done) ? 1 : (o < idx || done) ? 3 : 0; },
          label: 'A @ B  (3 × 3)', size: 12 });
      A.txt(ctx, '(3 × 2) × (2 × 3) = (3 × 3)', 380, 46, { align: 'center', size: 14, mono: true, w: 700, fill: P.soft });
      A.txt(ctx, 'the two middle numbers must MATCH — they get used up and vanish', 380, 66,
        { align: 'center', size: 11, fill: P.faint });
      if (!done) {
        var parts = [];
        for (var k = 0; k < K; k++) parts.push(Am[ci][k] + '×' + Bm[k][cj]);
        A.txt(ctx, 'the highlighted cell = row ' + (ci + 1) + ' of A  ·  column ' + (cj + 1) + ' of B',
          50, 236, { size: 12.5, w: 700, fill: P.a });
        A.txt(ctx, '= ' + parts.join(' + ') + ' = ' + cell(ci, cj), 50, 258,
          { size: 13.5, mono: true, fill: P.soft });
      } else {
        A.txt(ctx, 'every cell of the answer is one dot product: a row meeting a column.', 50, 244,
          { size: 13, w: 700, fill: P.g });
      }
      A.txt(ctx, 'Matrix multiply is just a whole grid of dot products, done in one go.', 50, 292,
        { size: 12.5, w: 700, fill: P.soft });
      A.txt(ctx, 'Order matters: A @ B and B @ A are different, and usually one of them is not even legal.',
        50, 314, { size: 12, fill: P.r });
      A.txt(ctx, 'Careful: A * B in NumPy is elementwise, NOT this. Use A @ B or np.matmul(A, B).',
        50, 336, { size: 12, w: 700, fill: P.r });
      ro.set('<b>Shape trick:</b> write the shapes next to each other — (3×<b>2</b>)(<b>2</b>×3). ' +
        'Middles match → legal. The answer is the outer two → (3×3).' +
        '\n<code>A @ B</code> · <code>np.matmul(A, B)</code> · <code>A.dot(B)</code> — all the same thing.');
    }
    A.autoplay(root, c, render);
  });

  /* ============================================================
     13. Transpose
     ============================================================ */
  A.def('ftranspose', function (root) {
    var c = A.canvas(root, 760, 300), ctx = c.ctx;
    var ro = A.readout(root);
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var ph = A.clamp(((t * .5) % 3) - .5, 0, 1), e = A.ease(ph);
      var M = [[1, 2, 3], [4, 5, 6]];
      var cw = 56, ch = 44;
      /* animate each cell from its old spot to its transposed spot */
      var ox = 120, oy = 100, tx = 470, ty = 84;
      for (var i = 0; i < 2; i++) for (var j = 0; j < 3; j++) {
        var fx = ox + j * cw, fy = oy + i * ch;
        var gx = tx + i * cw, gy = ty + j * ch;
        var x = A.lerp(fx, gx, e), y = A.lerp(fy, gy, e);
        A.rr(ctx, x, y, cw - 4, ch - 4, 5);
        ctx.fillStyle = e > .5 ? P.gS : P.bS; ctx.fill();
        ctx.strokeStyle = e > .5 ? P.g : P.b; ctx.lineWidth = 1.6; ctx.stroke();
        A.txt(ctx, String(M[i][j]), x + (cw - 4) / 2, y + 28,
          { align: 'center', size: 15, mono: true, w: 700, fill: e > .5 ? P.g : P.b });
      }
      A.txt(ctx, 'M   shape (2, 3)', ox + 82, 76, { align: 'center', size: 12, mono: true, w: 700,
        fill: e > .5 ? P.faint : P.b });
      A.txt(ctx, 'M.T   shape (3, 2)', tx + 54, 62, { align: 'center', size: 12, mono: true, w: 700,
        fill: e > .5 ? P.g : P.faint });
      A.arrow(ctx, 330, 130, 400, 130, P.line, 2);
      A.txt(ctx, '.T', 365, 118, { align: 'center', size: 13, mono: true, w: 700, fill: P.a });
      A.txt(ctx, 'Transpose = tip it on its side. Rows become columns; columns become rows.',
        40, 44, { size: 13, w: 700, fill: P.soft });
      A.txt(ctx, 'The numbers do not change. Only where they sit changes.', 40, 244,
        { size: 12, fill: P.faint });
      A.txt(ctx, 'You will use it constantly for one boring reason: making two shapes line up so they',
        40, 266, { size: 12, fill: P.faint });
      A.txt(ctx, 'can be multiplied. (2,3) won\'t meet (2,3) — but (2,3) meets (3,2) perfectly.',
        40, 288, { size: 12, w: 700, fill: P.a });
      ro.set('<code>M.T</code>  ·  <code>np.transpose(M)</code>  —  the same thing.' +
        '\nWritten <b>M<sup>T</sup></b> in maths, said “M transpose”. It is plumbing, not a deep idea: ' +
        'you reach for it when the shapes refuse to match.');
    }
    A.autoplay(root, c, render);
  });

  /* ============================================================
     14. Exponentials and e
     ============================================================ */
  A.def('fexp', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var z = 1;
    var bar = A.ctrls(root), ro = A.readout(root);
    A.slider(bar, { label: 'z =', min: -4, max: 4, step: .05, value: z,
      fmt: function (v) { return v.toFixed(2); }, on: function (v) { z = v; render(); } });
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var box = { x: 80, y: 44, w: 380, h: 210 };
      var S = A.axes(ctx, box, [-4, 4], [0, 30], {
        xticks: 4, yticks: 4, xfmt: function (v) { return v.toFixed(0); },
        yfmt: function (v) { return v.toFixed(0); }, xlab: 'z', ylab: 'e^z'
      });
      A.plot(ctx, S, [-4, 4], function (v) { return Math.exp(v); }, P.a, 2.8);
      A.line(ctx, box.x, S.Y(0), box.x + box.w, S.Y(0), P.line, 1.2);
      A.dot(ctx, S.X(z), S.Y(Math.min(Math.exp(z), 30)), 7, P.a);
      A.dot(ctx, S.X(0), S.Y(1), 5, P.g);
      A.txt(ctx, 'e⁰ = 1  (always)', S.X(0) + 8, S.Y(1) - 8, { size: 11, w: 700, fill: P.g });
      var mx = 500;
      A.txt(ctx, 'e ≈ 2.71828…', mx, 74, { size: 16, mono: true, w: 700, fill: P.a });
      A.txt(ctx, 'a fixed number, like π. Nothing to solve.', mx, 96, { size: 11, fill: P.faint });
      [['e^' + z.toFixed(2), Math.exp(z).toFixed(4)],
       ['e^0', '1'], ['e^1', '2.718'], ['e^−1', '0.368'], ['e^10', '22026'], ['e^−10', '0.000045']
      ].forEach(function (r, i) {
        A.txt(ctx, r[0], mx, 126 + i * 24, { size: 12.5, mono: true, fill: i === 0 ? P.a : P.faint });
        A.txt(ctx, '= ' + r[1], mx + 90, 126 + i * 24, { size: 12.5, mono: true, w: i === 0 ? 700 : 500,
          fill: i === 0 ? P.a : P.faint });
      });
      A.txt(ctx, 'Two facts do all the work:', 80, 284, { size: 12.5, w: 700, fill: P.soft });
      A.txt(ctx, '• e to ANY power is always POSITIVE — that is why softmax uses it', 80, 304,
        { size: 12, fill: P.soft });
      A.txt(ctx, '• big positive z → enormous. Big negative z → almost zero, but never quite',
        80, 324, { size: 12, fill: P.soft });
      ro.set('<code>np.exp(z)</code>  ·  in maths written <b>e<sup>z</sup></b> or <b>exp(z)</b>.' +
        '\nWhy e and not 10? Because e is the one base whose curve has slope exactly equal to its own ' +
        'height — which makes every derivative in this course come out clean. That is the entire reason.');
    }
    A.bind(c, render); render();
  });

  /* ============================================================
     15. Logarithms
     ============================================================ */
  A.def('flog', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var p = 0.5;
    var bar = A.ctrls(root), ro = A.readout(root);
    A.slider(bar, { label: 'p =', min: .001, max: 1, step: .001, value: p,
      fmt: function (v) { return v.toFixed(3); }, on: function (v) { p = v; render(); } });
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var box = { x: 80, y: 44, w: 360, h: 200 };
      var S = A.axes(ctx, box, [0, 1], [0, 7], {
        xticks: 5, yticks: 4, xfmt: function (v) { return v.toFixed(1); },
        yfmt: function (v) { return v.toFixed(0); }, xlab: 'p  (a probability)', ylab: '−log(p)'
      });
      A.plot(ctx, S, [.001, 1], function (v) { return Math.min(7, -Math.log(v)); }, P.a, 2.8);
      A.dot(ctx, S.X(p), S.Y(Math.min(-Math.log(p), 7)), 7, P.a);
      A.line(ctx, S.X(p), box.y + box.h, S.X(p), S.Y(Math.min(-Math.log(p), 7)), P.a, 1.4, [4, 3]);
      var mx = 480;
      A.txt(ctx, 'log undoes exp', mx, 70, { size: 13, w: 700, fill: P.soft });
      A.txt(ctx, 'e^x = y   ↔   log(y) = x', mx, 94, { size: 13, mono: true, fill: P.a });
      A.txt(ctx, '“what power do I raise e to,', mx, 118, { size: 10.5, fill: P.faint });
      A.txt(ctx, 'to get this number?”', mx, 134, { size: 10.5, fill: P.faint });
      [['−log(1.0)', '0'], ['−log(0.5)', '0.69'], ['−log(0.1)', '2.30'],
       ['−log(0.01)', '4.61'], ['−log(0.001)', '6.91'], ['−log(' + p.toFixed(3) + ')', (-Math.log(p)).toFixed(2)]
      ].forEach(function (r, i) {
        var last = i === 5;
        A.txt(ctx, r[0], mx, 164 + i * 21, { size: 12, mono: true, fill: last ? P.a : P.faint });
        A.txt(ctx, '= ' + r[1], mx + 106, 164 + i * 21, { size: 12, mono: true, w: last ? 700 : 500,
          fill: last ? P.a : P.faint });
      });
      A.txt(ctx, 'The one job logs do in this course: turn a TINY probability into a HUGE penalty.',
        80, 274, { size: 12.5, w: 700, fill: P.a });
      A.txt(ctx, 'Also handy: log turns multiplying into adding. log(a × b) = log(a) + log(b) —', 80, 296,
        { size: 12, fill: P.faint });
      A.txt(ctx, 'which is how code avoids multiplying a hundred small numbers down to zero.', 80, 318,
        { size: 12, fill: P.faint });
      ro.set('<code>np.log(p)</code> is the <b>natural</b> log (base e) — the default everywhere in ML.' +
        '\n<code>np.log2(p)</code> is base 2, used for entropy so the answer comes out in “bits”. ' +
        '<code>np.log10</code> is base 10. Same idea, different question.');
    }
    A.bind(c, render); render();
  });

  /* ============================================================
     16. Probability basics
     ============================================================ */
  A.def('fprob', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var reds = 3;
    var bar = A.ctrls(root), ro = A.readout(root);
    A.slider(bar, { label: 'red balls', min: 0, max: 10, step: 1, value: reds,
      fmt: function (v) { return v.toFixed(0); }, on: function (v) { reds = v; render(); } });
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var total = 10, pr = reds / total;
      A.rr(ctx, 50, 60, 250, 150, 12); ctx.fillStyle = P.sunk; ctx.fill();
      ctx.strokeStyle = P.line; ctx.lineWidth = 1.6; ctx.stroke();
      for (var i = 0; i < 10; i++) {
        var x = 82 + (i % 5) * 48, y = 96 + Math.floor(i / 5) * 52;
        A.dot(ctx, x, y, 17, i < reds ? P.r : P.b);
      }
      A.txt(ctx, 'a bag of 10 balls', 175, 46, { align: 'center', size: 12.5, w: 700, fill: P.soft });
      var mx = 340;
      A.txt(ctx, 'P(red)', mx, 78, { size: 13, mono: true, w: 700, fill: P.r });
      A.txt(ctx, '= ' + reds + ' / 10 = ' + pr.toFixed(2), mx + 70, 78, { size: 13, mono: true, fill: P.soft });
      A.txt(ctx, 'P(not red)', mx, 106, { size: 13, mono: true, w: 700, fill: P.b });
      A.txt(ctx, '= 1 − ' + pr.toFixed(2) + ' = ' + (1 - pr).toFixed(2), mx + 70, 106,
        { size: 13, mono: true, fill: P.soft });
      A.txt(ctx, 'they must add to 1', mx, 128, { size: 10.5, fill: P.faint });
      A.txt(ctx, 'two draws, putting it back:', mx, 166, { size: 12, w: 700, fill: P.soft });
      A.txt(ctx, 'P(red AND red) = ' + pr.toFixed(2) + ' × ' + pr.toFixed(2) + ' = ' + (pr * pr).toFixed(3),
        mx, 190, { size: 12.5, mono: true, fill: P.a });
      A.txt(ctx, '“AND” of independent things → MULTIPLY', mx, 212, { size: 10.5, fill: P.faint });
      A.txt(ctx, 'P(red OR blue) = ' + pr.toFixed(2) + ' + ' + (1 - pr).toFixed(2) + ' = 1.00',
        mx, 238, { size: 12.5, mono: true, fill: P.g });
      A.txt(ctx, '“OR” of separate things → ADD', mx, 260, { size: 10.5, fill: P.faint });
      A.txt(ctx, 'A probability is always between 0 (never) and 1 (certain). Multiply for AND, add for OR.',
        50, 292, { size: 12.5, w: 700, fill: P.soft });
      A.txt(ctx, 'P(y = 1 | x) is read “the probability that y is 1, GIVEN that we saw x”. The bar means “given”.',
        50, 316, { size: 12, w: 700, fill: P.a });
      ro.set('Notice the AND rule multiplying things below 1 makes them shrink fast — 0.5 × 0.5 × 0.5 = 0.125.' +
        '\nThat single fact is the engine behind <b>anomaly detection</b> (C3 W1) and behind why softmax ' +
        'and cross-entropy behave the way they do.');
    }
    A.bind(c, render); render();
  });

  /* ============================================================
     17. Mean, variance, standard deviation
     ============================================================ */
  A.def('fstats', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var spread = 1.0;
    var bar = A.ctrls(root), ro = A.readout(root);
    A.slider(bar, { label: 'spread them out', min: .15, max: 3, step: .05, value: spread,
      fmt: function (v) { return v.toFixed(2); }, on: function (v) { spread = v; render(); } });
    var base = [-1.6, -0.8, -0.2, 0.3, 0.9, 1.4];
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var vals = base.map(function (v) { return 5 + v * spread; });
      var m = vals.reduce(function (a, b) { return a + b; }, 0) / vals.length;
      var sq = vals.map(function (v) { return (v - m) * (v - m); });
      var varr = sq.reduce(function (a, b) { return a + b; }, 0) / vals.length;
      var sd = Math.sqrt(varr);
      var box = { x: 70, y: 60, w: 620, h: 70 };
      var S = A.axes(ctx, box, [0, 10], [0, 1], { xticks: 5, yticks: 1,
        xfmt: function (v) { return v.toFixed(0); }, yfmt: function () { return ''; }, xlab: 'value' });
      /* the mean, and each deviation */
      A.line(ctx, S.X(m), box.y - 8, S.X(m), box.y + box.h + 8, P.a, 2.4);
      A.txt(ctx, 'μ = ' + m.toFixed(2), S.X(m), box.y - 16, { align: 'center', size: 12, mono: true,
        w: 700, fill: P.a });
      ctx.save(); ctx.fillStyle = P.b; ctx.globalAlpha = .12;
      ctx.fillRect(S.X(m - sd), box.y, S.X(m + sd) - S.X(m - sd), box.h); ctx.restore();
      A.txt(ctx, '± one σ', S.X(m + sd) + 6, box.y + 20, { size: 10.5, fill: P.b });
      vals.forEach(function (v, i) {
        A.line(ctx, S.X(v), box.y + box.h / 2, S.X(m), box.y + box.h / 2, P.faint, 1, [3, 3]);
        A.dot(ctx, S.X(v), box.y + box.h / 2, 6, P.b);
      });
      /* the working */
      A.txt(ctx, 'the recipe, in order', 70, 166, { size: 12.5, w: 700, fill: P.soft });
      [['1. mean μ', 'add them up, divide by how many', m.toFixed(3), P.a],
       ['2. deviations', 'how far is each one from μ?', '(shown as dashes)', P.faint],
       ['3. square them', 'so being below counts the same as above', sq.map(function (s) { return s.toFixed(1); }).join(', '), P.faint],
       ['4. variance σ²', 'the average of those squares', varr.toFixed(3), P.p],
       ['5. std dev σ', 'square root of the variance', sd.toFixed(3), P.g]
      ].forEach(function (r, i) {
        var y = 190 + i * 24;
        A.txt(ctx, r[0], 70, y, { size: 12, w: 700, fill: r[3] });
        A.txt(ctx, r[1], 190, y, { size: 11, fill: P.faint });
        A.txt(ctx, r[2], 690, y, { align: 'right', size: 11.5, mono: true, fill: r[3] });
      });
      A.txt(ctx, 'Mean = the middle. Standard deviation = the typical distance from that middle.',
        70, 320, { size: 12.5, w: 700, fill: P.soft });
      ro.set('<code>x.mean()</code> · <code>x.var()</code> · <code>x.std()</code> — or ' +
        '<code>np.mean(x)</code>, <code>np.var(x)</code>, <code>np.std(x)</code>.' +
        '\nWhy square in step 3? Because plain distances would cancel out — the ones below the mean ' +
        'are negative. Squaring makes them all count. σ then un-squares it so the answer is back in ' +
        'the original units.');
    }
    A.bind(c, render); render();
  });

  /* ============================================================
     18. The normal distribution
     ============================================================ */
  A.def('fnormal', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var mu = 5, sd = 1.2;
    var bar = A.ctrls(root), ro = A.readout(root);
    A.slider(bar, { label: 'μ  (middle)', min: 2, max: 8, step: .1, value: mu,
      fmt: function (v) { return v.toFixed(1); }, on: function (v) { mu = v; render(); } });
    A.slider(bar, { label: 'σ  (width)', min: .3, max: 2.5, step: .05, value: sd,
      fmt: function (v) { return v.toFixed(2); }, on: function (v) { sd = v; render(); } });
    function npdf(x) { return Math.exp(-(x - mu) * (x - mu) / (2 * sd * sd)) / (Math.sqrt(6.2832) * sd); }
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var box = { x: 70, y: 44, w: 620, h: 190 };
      var S = A.axes(ctx, box, [0, 10], [0, 1.4], {
        xticks: 5, yticks: 3, xfmt: function (v) { return v.toFixed(0); },
        yfmt: function (v) { return v.toFixed(1); }, xlab: 'value', ylab: 'how common'
      });
      [[3, .997, P.mS], [2, .95, P.bS], [1, .68, P.gS]].forEach(function (band) {
        ctx.save(); ctx.fillStyle = band[2]; ctx.beginPath();
        ctx.moveTo(S.X(mu - band[0] * sd), S.Y(0));
        for (var v = mu - band[0] * sd; v <= mu + band[0] * sd; v += .03) ctx.lineTo(S.X(v), S.Y(npdf(v)));
        ctx.lineTo(S.X(mu + band[0] * sd), S.Y(0)); ctx.closePath(); ctx.fill(); ctx.restore();
      });
      A.plot(ctx, S, [0, 10], npdf, P.a, 2.8);
      A.line(ctx, S.X(mu), box.y, S.X(mu), S.Y(0), P.a, 1.6, [4, 3]);
      A.txt(ctx, 'μ', S.X(mu), box.y + 14, { align: 'center', size: 15, w: 700, fill: P.a });
      [[1, '68%', P.g], [2, '95%', P.b], [3, '99.7%', P.m]].forEach(function (band, i) {
        A.txt(ctx, '± ' + band[0] + 'σ holds ' + band[1], 70, 264 + i * 20,
          { size: 12, w: 700, fill: band[2] });
      });
      A.txt(ctx, 'Measure a thousand people\'s heights and you get this hill: lots in the middle, few at the edges.',
        70, 254, { size: 12.5, w: 700, fill: P.soft });
      A.txt(ctx, 'Two numbers describe it completely: where the top is (μ) and how wide it is (σ).',
        330, 284, { size: 12, fill: P.faint });
      A.txt(ctx, 'Small σ = a tall narrow spike, so anything off-centre looks instantly suspicious.',
        330, 304, { size: 12, fill: P.faint });
      A.txt(ctx, 'The area under the whole curve is always exactly 1.', 330, 324, { size: 12, w: 700, fill: P.a });
      ro.set('<b>p(x) = (1 / (√(2π)·σ)) · e<sup>−(x−μ)² / 2σ²</sup></b>' +
        '\nDo not memorise it — recognise the parts. <b>(x−μ)²</b> is “how far from the middle, squared”. ' +
        'The <b>e<sup>−…</sup></b> makes it fall away fast. The fraction in front is just scaling so the ' +
        'area comes to 1.' +
        '\n<code>np.random.normal(mu, sigma, size)</code> draws samples from it.');
    }
    A.bind(c, render); render();
  });

  /* ============================================================
     19. min, max, argmin, argmax
     ============================================================ */
  A.def('fargmax', function (root) {
    var c = A.canvas(root, 760, 300), ctx = c.ctx;
    var vals = [12, 31, 7, 24, 19];
    var ro = A.readout(root);
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var mode = Math.floor((t * .5) % 4);
      var mx = Math.max.apply(null, vals), mn = Math.min.apply(null, vals);
      var ai = vals.indexOf(mx), ii = vals.indexOf(mn);
      var target = (mode === 0 || mode === 2) ? mx : mn;
      A.txt(ctx, 'x = [12, 31, 7, 24, 19]', 40, 44, { size: 14, mono: true, w: 700, fill: P.soft });
      vals.forEach(function (v, i) {
        var x = 60 + i * 108, on = v === target;
        A.rr(ctx, x, 64, 88, 62, 8);
        ctx.fillStyle = on ? P.aS : P.sunk; ctx.fill();
        ctx.strokeStyle = on ? P.a : P.lineSoft; ctx.lineWidth = on ? 2.4 : 1; ctx.stroke();
        A.txt(ctx, String(v), x + 44, 104, { align: 'center', size: 22, mono: true, w: 700,
          fill: on ? P.a : P.soft });
        A.txt(ctx, 'index ' + i, x + 44, 142, { align: 'center', size: 10.5,
          fill: on && mode >= 2 ? P.g : P.faint });
      });
      var rows = [
        ['max(x)', mx, 'the biggest VALUE', P.a],
        ['min(x)', mn, 'the smallest VALUE', P.a],
        ['argmax(x)', ai, 'the POSITION of the biggest', P.g],
        ['argmin(x)', ii, 'the POSITION of the smallest', P.g]
      ];
      rows.forEach(function (r, i) {
        var y = 178 + i * 26, on = i === mode;
        A.rr(ctx, 40, y, 400, 23, 5);
        ctx.fillStyle = on ? (r[3] === P.g ? P.gS : P.aS) : P.sunk; ctx.fill();
        ctx.strokeStyle = on ? r[3] : P.lineSoft; ctx.lineWidth = on ? 1.6 : 1; ctx.stroke();
        A.txt(ctx, r[0], 54, y + 16, { size: 12, mono: true, w: 700, fill: on ? r[3] : P.soft });
        A.txt(ctx, '= ' + r[1], 150, y + 16, { size: 12, mono: true, w: 700, fill: on ? r[3] : P.soft });
        A.txt(ctx, r[2], 210, y + 16, { size: 11, fill: P.faint });
      });
      A.txt(ctx, 'The “arg” prefix means: don\'t give me the value — give me WHERE it is.',
        460, 190, { size: 12, w: 700, fill: P.g });
      A.txt(ctx, 'That is exactly what you want when', 460, 216, { size: 11.5, fill: P.faint });
      A.txt(ctx, 'picking a class or an action: you need', 460, 234, { size: 11.5, fill: P.faint });
      A.txt(ctx, 'to know WHICH one won, not its score.', 460, 252, { size: 11.5, fill: P.faint });
      A.txt(ctx, 'np.argmax(p, axis=1) → the predicted class for each row', 40, 288,
        { size: 12.5, mono: true, w: 700, fill: P.b });
      ro.set('<code>np.max(x)</code> · <code>np.min(x)</code> · <code>np.argmax(x)</code> · ' +
        '<code>np.argmin(x)</code>' +
        '\nIn formulas: <b>argmax<sub>a</sub> Q(s,a)</b> means “the ACTION a that makes Q biggest” — ' +
        'the action, not the number. Same word, same meaning.');
    }
    A.autoplay(root, c, render);
  });

})();
