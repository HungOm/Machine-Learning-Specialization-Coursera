/* Widgets for Course 2 / Week 1 — Neural networks & forward propagation */
(function () {
  'use strict';

  /* ---------- shared network drawing helpers ---------- */
  function col(x, n, top, bot, r) {
    var out = [], i;
    if (n === 1) { return [{ x: x, y: (top + bot) / 2, r: r }]; }
    for (i = 0; i < n; i++) out.push({ x: x, y: top + (bot - top) * i / (n - 1), r: r });
    return out;
  }
  function link(ctx, p, q, colr, w, alpha) {
    ctx.save(); ctx.globalAlpha = alpha == null ? 1 : alpha;
    ctx.strokeStyle = colr; ctx.lineWidth = w;
    ctx.beginPath(); ctx.moveTo(p.x + p.r, p.y); ctx.lineTo(q.x - q.r, q.y); ctx.stroke();
    ctx.restore();
  }
  /* a neuron drawn as a circle whose fill shows its activation 0..1 */
  function neuron(ctx, p, a, P, label, sublabel, ring) {
    ctx.save();
    ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, 6.2832);
    ctx.fillStyle = P.panel; ctx.fill();
    ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, 6.2832);
    ctx.globalAlpha = 0.15 + 0.85 * A.clamp(a, 0, 1);
    ctx.fillStyle = ring || P.a; ctx.fill();
    ctx.globalAlpha = 1;
    ctx.lineWidth = 1.6; ctx.strokeStyle = ring || P.a;
    ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, 6.2832); ctx.stroke();
    ctx.restore();
    if (label != null) A.txt(ctx, label, p.x, p.y + 4,
      { align: 'center', size: 12, w: 700, mono: true, fill: a > .55 ? P.panel : P.ink });
    if (sublabel) A.txt(ctx, sublabel, p.x, p.y + p.r + 15, { align: 'center', size: 11, fill: P.faint });
  }
  /* travelling pulse along an edge */
  function pulse(ctx, p, q, t, colr, R) {
    var u = (t % 1);
    var x = A.lerp(p.x + p.r, q.x - q.r, u), y = A.lerp(p.y, q.y, u);
    A.dot(ctx, x, y, R || 3, colr);
  }

  /* ============================================================
     1. Biological neuron vs artificial neuron
     ============================================================ */
  A.def('bio-vs-artificial', function (root) {
    var c = A.canvas(root, 760, 300);
    var ctx = c.ctx;
    function render(t) {
      var P = A.pal();
      c.clear(P.panel);
      t = t || 0;
      /* ---- left: biological ---- */
      A.txt(ctx, 'A real brain cell', 30, 34, { size: 13, w: 700, fill: P.soft });
      var sx = 150, sy = 160;
      /* dendrites */
      for (var i = 0; i < 5; i++) {
        var ang = -2.5 + i * 0.42;
        var ex = sx + Math.cos(ang) * 95, ey = sy + Math.sin(ang) * 85;
        A.line(ctx, sx, sy, ex, ey, P.line, 2.4);
        A.dot(ctx, ex, ey, 4, P.line);
        var u = ((t * .55 + i * .17) % 1);
        A.dot(ctx, A.lerp(ex, sx, u), A.lerp(ey, sy, u), 3.4, P.b);
      }
      /* soma */
      ctx.save();
      ctx.beginPath(); ctx.ellipse(sx, sy, 30, 24, 0, 0, 6.2832);
      ctx.fillStyle = P.bS; ctx.fill(); ctx.strokeStyle = P.b; ctx.lineWidth = 2; ctx.stroke();
      ctx.restore();
      A.txt(ctx, 'adds it all up', sx, sy + 48, { align: 'center', size: 11, fill: P.faint });
      /* axon */
      A.line(ctx, sx + 30, sy, sx + 175, sy, P.line, 3);
      A.arrow(ctx, sx + 150, sy, sx + 182, sy, P.line, 2);
      var fire = ((t * .55) % 1);
      if (fire > .5) A.dot(ctx, A.lerp(sx + 30, sx + 175, (fire - .5) * 2), sy, 4.5, P.g);
      A.txt(ctx, 'fires a spike →', sx + 100, sy - 14, { size: 11, fill: P.faint, align: 'center' });

      /* divider */
      A.line(ctx, 380, 30, 380, 270, P.lineSoft, 1, [5, 5]);

      /* ---- right: artificial ---- */
      A.txt(ctx, 'Our maths copy of it', 410, 34, { size: 13, w: 700, fill: P.soft });
      var ins = col(470, 3, 90, 230, 17);
      var out = col(650, 1, 160, 160, 26);
      var xs = [1.0, 0.6, 0.9], ws = [2.0, -1.2, 1.4], b = -0.8;
      var z = 0; for (i = 0; i < 3; i++) z += xs[i] * ws[i]; z += b;
      var a = A.sig(z);
      for (i = 0; i < 3; i++) {
        var wgt = Math.abs(ws[i]);
        link(ctx, ins[i], out[0], ws[i] > 0 ? P.g : P.r, 1 + wgt * 1.4, .75);
        A.txt(ctx, 'w' + (i + 1) + ' = ' + ws[i].toFixed(1),
          (ins[i].x + out[0].x) / 2, (ins[i].y + out[0].y) / 2 - 6,
          { align: 'center', size: 10.5, mono: true, fill: ws[i] > 0 ? P.g : P.r });
        neuron(ctx, ins[i], xs[i], P, xs[i].toFixed(1), 'x' + (i + 1), P.b);
        pulse(ctx, ins[i], out[0], t * .55 + i * .17, P.b, 3.2);
      }
      neuron(ctx, out[0], a, P, a.toFixed(2), null, P.a);
      A.txt(ctx, 'z = w·x + b  →  g(z)', out[0].x, out[0].y + 46,
        { align: 'center', size: 11.5, mono: true, fill: P.faint });
      A.arrow(ctx, out[0].x + 30, out[0].y, out[0].x + 66, out[0].y, P.a, 2);
      A.txt(ctx, 'output', out[0].x + 48, out[0].y - 10, { align: 'center', size: 11, fill: P.faint });
      A.txt(ctx, 'Inputs are numbers. Each wire has a weight. The neuron adds them, then squashes the total into 0…1.',
        410, 275, { size: 11.5, fill: P.faint });
    }
    A.autoplay(root, c, render);
  });

  /* ============================================================
     2. Demand prediction (t-shirt)
     ============================================================ */
  A.def('demand', function (root) {
    var c = A.canvas(root, 760, 340), ctx = c.ctx;
    var v = { price: 180, ship: 12, mkt: 6, mat: 8 };
    var bar = A.ctrls(root);
    var ro = A.readout(root);
    A.slider(bar, { label: 'price $', min: 20, max: 400, step: 1, value: v.price,
      fmt: function (x) { return '$' + x; }, on: function (x) { v.price = x; render(); } });
    A.slider(bar, { label: 'shipping $', min: 0, max: 40, step: 1, value: v.ship,
      fmt: function (x) { return '$' + x; }, on: function (x) { v.ship = x; render(); } });
    A.slider(bar, { label: 'marketing', min: 0, max: 10, step: .1, value: v.mkt,
      fmt: function (x) { return x.toFixed(1); }, on: function (x) { v.mkt = x; render(); } });
    A.slider(bar, { label: 'material', min: 0, max: 10, step: .1, value: v.mat,
      fmt: function (x) { return x.toFixed(1); }, on: function (x) { v.mat = x; render(); } });

    function compute() {
      var afford = A.sig((160 - v.price - v.ship * 2) / 45);
      var aware = A.sig((v.mkt - 4.5) / 1.4);
      var qual = A.sig((v.mat * 0.9 + v.price / 60 - 5.2) / 1.3);
      var z = 3.1 * afford + 2.6 * aware + 2.4 * qual - 4.0;
      return { afford: afford, aware: aware, qual: qual, p: A.sig(z), z: z };
    }
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var r = compute();
      var ins = col(120, 4, 70, 280, 20);
      var hid = col(370, 3, 100, 250, 26);
      var out = col(620, 1, 175, 175, 30);
      var inLab = ['price', 'shipping', 'marketing', 'material'];
      var inVal = [v.price, v.ship, v.mkt, v.mat];
      var inNorm = [v.price / 400, v.ship / 40, v.mkt / 10, v.mat / 10];
      var hidLab = ['affordability', 'awareness', 'perceived quality'];
      var hidVal = [r.afford, r.aware, r.qual];
      var i, j;
      for (i = 0; i < 4; i++) for (j = 0; j < 3; j++)
        link(ctx, ins[i], hid[j], P.line, 1, .5);
      for (j = 0; j < 3; j++) link(ctx, hid[j], out[0], P.line, 1.4, .55);
      /* highlight the strongest live signals */
      for (i = 0; i < 4; i++) for (j = 0; j < 3; j++) {
        var s = inNorm[i] * hidVal[j];
        if (s > .28) { link(ctx, ins[i], hid[j], P.b, 1 + s * 2.4, .55); pulse(ctx, ins[i], hid[j], t * .5 + (i + j) * .2, P.b, 2.6); }
      }
      for (j = 0; j < 3; j++) if (hidVal[j] > .4) {
        link(ctx, hid[j], out[0], P.a, 1 + hidVal[j] * 3, .7);
        pulse(ctx, hid[j], out[0], t * .5 + j * .3, P.a, 3);
      }
      for (i = 0; i < 4; i++) {
        neuron(ctx, ins[i], inNorm[i], P, String(inVal[i]), inLab[i], P.b);
      }
      for (j = 0; j < 3; j++) neuron(ctx, hid[j], hidVal[j], P, hidVal[j].toFixed(2), hidLab[j], P.p);
      neuron(ctx, out[0], r.p, P, (r.p * 100).toFixed(0) + '%', 'top seller?', P.a);
      A.txt(ctx, 'input layer  x', 120, 315, { align: 'center', size: 11.5, w: 700, fill: P.faint });
      A.txt(ctx, 'hidden layer  a[1]', 370, 315, { align: 'center', size: 11.5, w: 700, fill: P.faint });
      A.txt(ctx, 'output layer  a[2]', 620, 315, { align: 'center', size: 11.5, w: 700, fill: P.faint });
      A.txt(ctx, 'Nobody told the middle neurons to mean "affordability" — that is just a story we tell. They learn whatever helps.',
        30, 26, { size: 11.5, fill: P.faint });
      ro.set('affordability = <b>' + r.afford.toFixed(3) + '</b>   awareness = <b>' + r.aware.toFixed(3) +
        '</b>   quality = <b>' + r.qual.toFixed(3) + '</b>\n' +
        'z = 3.1(' + r.afford.toFixed(2) + ') + 2.6(' + r.aware.toFixed(2) + ') + 2.4(' + r.qual.toFixed(2) +
        ') − 4.0 = <b>' + r.z.toFixed(2) + '</b>   →   g(z) = <b>' + r.p.toFixed(3) + '</b>');
    }
    A.autoplay(root, c, render);
  });

  /* ============================================================
     3. What each layer of an image network looks at
     ============================================================ */
  A.def('face-features', function (root) {
    var c = A.canvas(root, 760, 320), ctx = c.ctx;
    function face(x, y, s, P, col2) {
      ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
      ctx.strokeStyle = col2; ctx.lineWidth = 2 / s; ctx.fillStyle = 'transparent';
      ctx.beginPath(); ctx.ellipse(0, 0, 26, 33, 0, 0, 6.2832); ctx.stroke();
      ctx.beginPath(); ctx.ellipse(-10, -8, 6, 4, 0, 0, 6.2832); ctx.stroke();
      ctx.beginPath(); ctx.ellipse(10, -8, 6, 4, 0, 0, 6.2832); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(0, -4); ctx.lineTo(-3, 8); ctx.lineTo(3, 8); ctx.stroke();
      ctx.beginPath(); ctx.arc(0, 12, 11, .25, Math.PI - .25); ctx.stroke();
      ctx.restore();
    }
    function tile(x, y, w, hgt, P, drawer, on) {
      A.rr(ctx, x, y, w, hgt, 6);
      ctx.fillStyle = P.sunk; ctx.fill();
      ctx.strokeStyle = on ? P.a : P.lineSoft; ctx.lineWidth = on ? 2 : 1; ctx.stroke();
      ctx.save(); ctx.beginPath(); A.rr(ctx, x, y, w, hgt, 6); ctx.clip();
      drawer(x + w / 2, y + hgt / 2);
      ctx.restore();
    }
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var phase = Math.floor((t * .45) % 4);
      var xs = [40, 230, 420, 610], labs = ['the picture', 'layer 1: edges', 'layer 2: parts', 'layer 3: whole faces'];
      var i, k;
      for (i = 0; i < 4; i++) {
        A.txt(ctx, labs[i], xs[i] + 60, 40, { align: 'center', size: 12, w: 700, fill: phase === i ? P.a : P.soft });
        if (i < 3) A.arrow(ctx, xs[i] + 128, 165, xs[i] + 178, 165, phase > i ? P.a : P.line, 2);
      }
      /* the picture: pixelated face */
      tile(xs[0], 60, 120, 210, P, function (cx, cy) {
        ctx.save();
        for (var r = 0; r < 14; r++) for (var q = 0; q < 8; q++) {
          var px = cx - 60 + q * 15, py = cy - 105 + r * 15;
          ctx.fillStyle = P.sunk; ctx.fillRect(px, py, 15, 15);
        }
        ctx.globalAlpha = .95; face(cx, cy, 2.4, P, P.ink);
        ctx.globalAlpha = .25; ctx.strokeStyle = P.line; ctx.lineWidth = .6;
        for (r = 0; r <= 14; r++) { ctx.beginPath(); ctx.moveTo(cx - 60, cy - 105 + r * 15); ctx.lineTo(cx + 60, cy - 105 + r * 15); ctx.stroke(); }
        for (q = 0; q <= 8; q++) { ctx.beginPath(); ctx.moveTo(cx - 60 + q * 15, cy - 105); ctx.lineTo(cx - 60 + q * 15, cy + 105); ctx.stroke(); }
        ctx.restore();
      }, phase === 0);
      /* layer 1: little edges */
      for (k = 0; k < 9; k++) {
        var gx = xs[1] + (k % 3) * 42, gy = 60 + Math.floor(k / 3) * 42;
        tile(gx, gy, 36, 36, P, function (cx, cy) {
          var ang = k * 0.35;
          A.line(ctx, cx - Math.cos(ang) * 13, cy - Math.sin(ang) * 13,
            cx + Math.cos(ang) * 13, cy + Math.sin(ang) * 13, P.b, 3);
        }, phase === 1);
      }
      A.txt(ctx, 'tiny lines & corners', xs[1] + 60, 210, { align: 'center', size: 11, fill: P.faint });
      /* layer 2: parts */
      var parts = [
        function (cx, cy) { ctx.strokeStyle = P.p; ctx.lineWidth = 2; ctx.beginPath(); ctx.ellipse(cx, cy, 13, 8, 0, 0, 6.28); ctx.stroke(); A.dot(ctx, cx, cy, 4, P.p); },
        function (cx, cy) { ctx.strokeStyle = P.p; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(cx, cy - 12); ctx.lineTo(cx - 7, cy + 10); ctx.lineTo(cx + 7, cy + 10); ctx.stroke(); },
        function (cx, cy) { ctx.strokeStyle = P.p; ctx.lineWidth = 2; ctx.beginPath(); ctx.arc(cx, cy - 3, 12, .2, Math.PI - .2); ctx.stroke(); },
        function (cx, cy) { ctx.strokeStyle = P.p; ctx.lineWidth = 2; ctx.beginPath(); ctx.arc(cx, cy + 6, 14, Math.PI + .3, -.3); ctx.stroke(); }
      ];
      for (k = 0; k < 4; k++) {
        tile(xs[2] + (k % 2) * 62, 70 + Math.floor(k / 2) * 62, 56, 56, P, parts[k], phase === 2);
      }
      A.txt(ctx, 'eyes, noses, mouths', xs[2] + 60, 210, { align: 'center', size: 11, fill: P.faint });
      /* layer 3: faces */
      for (k = 0; k < 4; k++) {
        tile(xs[3] + (k % 2) * 62, 70 + Math.floor(k / 2) * 62, 56, 56, P, function (cx, cy) {
          face(cx, cy, .72 + (k % 2) * .12, P, P.g);
        }, phase === 3);
      }
      A.txt(ctx, 'whole face shapes', xs[3] + 60, 210, { align: 'center', size: 11, fill: P.faint });
      A.txt(ctx, 'Same idea every layer: build slightly bigger things out of the layer before. Nobody hand-drew these — they were learned.',
        40, 300, { size: 11.5, fill: P.faint });
    }
    A.autoplay(root, c, render);
  });

  /* ============================================================
     4. One layer of neurons
     ============================================================ */
  A.def('layer', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var x1 = 0.7, x2 = 0.3;
    var W = [[2.4, -1.1], [-1.8, 2.2], [1.3, 1.4]], b = [-0.6, -0.2, -1.5];
    var bar = A.ctrls(root), ro = A.readout(root);
    A.slider(bar, { label: 'x<sub>1</sub>', min: 0, max: 1, value: x1, on: function (v) { x1 = v; render(); } });
    A.slider(bar, { label: 'x<sub>2</sub>', min: 0, max: 1, value: x2, on: function (v) { x2 = v; render(); } });
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var ins = col(130, 2, 120, 220, 20), hid = col(420, 3, 80, 260, 28), out = col(650, 1, 170, 170, 24);
      var zs = [], as = [], i, j;
      for (j = 0; j < 3; j++) { var z = W[j][0] * x1 + W[j][1] * x2 + b[j]; zs.push(z); as.push(A.sig(z)); }
      for (i = 0; i < 2; i++) for (j = 0; j < 3; j++) {
        link(ctx, ins[i], hid[j], W[j][i] > 0 ? P.g : P.r, .8 + Math.abs(W[j][i]), .55);
        A.txt(ctx, W[j][i].toFixed(1), A.lerp(ins[i].x, hid[j].x, .34), A.lerp(ins[i].y, hid[j].y, .34) - 5,
          { align: 'center', size: 10, mono: true, fill: W[j][i] > 0 ? P.g : P.r });
        pulse(ctx, ins[i], hid[j], t * .6 + (i * 3 + j) * .13, P.b, 2.6);
      }
      neuron(ctx, ins[0], x1, P, x1.toFixed(2), 'x₁', P.b);
      neuron(ctx, ins[1], x2, P, x2.toFixed(2), 'x₂', P.b);
      for (j = 0; j < 3; j++) {
        neuron(ctx, hid[j], as[j], P, as[j].toFixed(2), 'a[1]' + (j + 1), P.p);
        A.txt(ctx, 'b = ' + b[j].toFixed(1), hid[j].x + 40, hid[j].y - 20, { size: 10.5, mono: true, fill: P.faint });
        A.txt(ctx, 'z = ' + zs[j].toFixed(2), hid[j].x + 40, hid[j].y - 6, { size: 10.5, mono: true, fill: P.faint });
        link(ctx, hid[j], out[0], P.a, 1.4, .5);
      }
      /* the vector box */
      A.rr(ctx, out[0].x - 34, out[0].y - 62, 68, 124, 10);
      ctx.fillStyle = P.aS; ctx.fill(); ctx.strokeStyle = P.a; ctx.lineWidth = 1.6; ctx.stroke();
      for (j = 0; j < 3; j++)
        A.txt(ctx, as[j].toFixed(2), out[0].x, out[0].y - 30 + j * 32,
          { align: 'center', size: 14, mono: true, w: 700, fill: P.a });
      A.txt(ctx, 'a[1]  — one vector', out[0].x, out[0].y + 82, { align: 'center', size: 11.5, w: 700, fill: P.faint });
      A.txt(ctx, 'a layer = several neurons that all read the SAME inputs and each output ONE number',
        30, 30, { size: 12, fill: P.soft, w: 600 });
      A.txt(ctx, 'input layer (layer 0)', 130, 300, { align: 'center', size: 11, fill: P.faint });
      A.txt(ctx, 'hidden layer 1: 3 units', 420, 300, { align: 'center', size: 11, fill: P.faint });
      ro.set('a<sub>1</sub><sup>[1]</sup> = g(' + W[0][0] + '·' + x1.toFixed(2) + ' + ' + W[0][1] + '·' + x2.toFixed(2) + ' + ' + b[0] + ') = g(' + zs[0].toFixed(2) + ') = <b>' + as[0].toFixed(3) + '</b>\n' +
        'a<sub>2</sub><sup>[1]</sup> = g(' + W[1][0] + '·' + x1.toFixed(2) + ' + ' + W[1][1] + '·' + x2.toFixed(2) + ' + ' + b[1] + ') = g(' + zs[1].toFixed(2) + ') = <b>' + as[1].toFixed(3) + '</b>\n' +
        'a<sub>3</sub><sup>[1]</sup> = g(' + W[2][0] + '·' + x1.toFixed(2) + ' + ' + W[2][1] + '·' + x2.toFixed(2) + ' + ' + b[2] + ') = g(' + zs[2].toFixed(2) + ') = <b>' + as[2].toFixed(3) + '</b>');
    }
    A.autoplay(root, c, render);
  });

  /* ============================================================
     5. Layer / unit notation tour
     ============================================================ */
  A.def('netnotation', function (root) {
    var c = A.canvas(root, 760, 340), ctx = c.ctx;
    var sizes = [3, 4, 4, 3, 1];
    var acts = sizes.map(function (n, li) {
      var arr = []; for (var i = 0; i < n; i++) arr.push(A.sig(Math.sin(i * 1.7 + li * 2.3) * 1.6));
      return arr;
    });
    var ro = A.readout(root);
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var cols = sizes.map(function (n, i) { return col(90 + i * 150, n, 90, 270, n > 3 ? 20 : 22); });
      var step = Math.floor(t * .6) % 12;
      var hl = { l: 1 + Math.floor(step / 3), j: step % 3 };
      if (hl.l > 4) hl.l = 4;
      var li, i, j;
      for (li = 1; li < cols.length; li++)
        for (i = 0; i < cols[li - 1].length; i++)
          for (j = 0; j < cols[li].length; j++) {
            var on = (li === hl.l && j === hl.j);
            link(ctx, cols[li - 1][i], cols[li][j], on ? P.a : P.line, on ? 2 : .8, on ? .95 : .35);
            if (on) pulse(ctx, cols[li - 1][i], cols[li][j], t * 1.1 + i * .16, P.a, 3);
          }
      for (li = 0; li < cols.length; li++) {
        for (j = 0; j < cols[li].length; j++) {
          var isHl = (li === hl.l && j === hl.j);
          neuron(ctx, cols[li][j], acts[li][j], P, null, null,
            li === 0 ? P.b : li === cols.length - 1 ? P.g : (isHl ? P.a : P.p));
          if (isHl) {
            ctx.save(); ctx.strokeStyle = P.a; ctx.lineWidth = 2.4; ctx.setLineDash([4, 3]);
            ctx.beginPath(); ctx.arc(cols[li][j].x, cols[li][j].y, cols[li][j].r + 7, 0, 6.2832); ctx.stroke(); ctx.restore();
          }
        }
        var lab = li === 0 ? 'x  (layer 0)' : li === cols.length - 1 ? 'layer ' + li + ' (output)' : 'layer ' + li;
        A.txt(ctx, lab, cols[li][0].x, 300, { align: 'center', size: 11.5, w: 700, fill: P.faint });
        A.txt(ctx, sizes[li] + (sizes[li] > 1 ? ' units' : ' unit'), cols[li][0].x, 316,
          { align: 'center', size: 10.5, fill: P.faint });
      }
      A.txt(ctx, 'the highlighted unit is', 40, 40, { size: 11.5, fill: P.faint });
      A.txt(ctx, 'a[' + hl.l + ']' + (hl.j + 1), 40, 66, { size: 22, w: 700, mono: true, fill: P.a });
      ro.set('a<sub>' + (hl.j + 1) + '</sub><sup>[' + hl.l + ']</sup> = g( <b>w</b><sub>' + (hl.j + 1) + '</sub><sup>[' + hl.l + ']</sup> · <b>a</b><sup>[' + (hl.l - 1) + ']</sup> + b<sub>' + (hl.j + 1) + '</sub><sup>[' + hl.l + ']</sup> )\n' +
        'superscript [' + hl.l + '] = which layer   ·   subscript ' + (hl.j + 1) + ' = which unit inside that layer   ·   it reads the WHOLE previous layer a<sup>[' + (hl.l - 1) + ']</sup>');
    }
    A.autoplay(root, c, render);
  });

  /* ============================================================
     6. Forward propagation on a drawable 8x8 digit
     ============================================================ */
  A.def('forward', function (root) {
    var c = A.canvas(root, 760, 360), ctx = c.ctx;
    var N = 8, grid = [];
    var tmplOne = [], tmplZero = [];
    (function () {
      var r, q;
      for (r = 0; r < N; r++) for (q = 0; q < N; q++) {
        grid.push(0);
        tmplOne.push((q === 3 || q === 4) && r > 0 && r < 7 ? 1 : 0);
        var dx = (q - 3.5) / 2.6, dy = (r - 3.5) / 3.2, d = dx * dx + dy * dy;
        tmplZero.push(d > .45 && d < 1.25 ? 1 : 0);
      }
      /* start with a hand-drawn-ish "1" */
      [11, 19, 27, 35, 43, 51, 12, 20, 28, 36, 44, 52, 10].forEach(function (i) { grid[i] = 1; });
    })();
    function score() {
      var i, so = 0, sz = 0, n = 0;
      for (i = 0; i < grid.length; i++) { so += grid[i] * (tmplOne[i] ? 1 : -0.45); sz += grid[i] * (tmplZero[i] ? 1 : -0.45); n += grid[i]; }
      var h = []; /* pretend hidden units: parts of the evidence */
      h.push(A.sig(so * .55 - 1.2));
      h.push(A.sig(sz * .55 - 1.2));
      h.push(A.sig((n - 12) * .35));
      var z = 4.2 * h[0] - 3.6 * h[1] - 0.6 * h[2] + 0.1;
      return { h: h, z: z, p: A.sig(z) };
    }
    var g0 = { x: 40, y: 70, s: 24 };
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var s = score(), r, q, i;
      A.txt(ctx, 'click the squares to draw a digit', 40, 40, { size: 12, w: 700, fill: P.soft });
      for (r = 0; r < N; r++) for (q = 0; q < N; q++) {
        i = r * N + q;
        var x = g0.x + q * g0.s, y = g0.y + r * g0.s;
        ctx.fillStyle = grid[i] ? P.ink : P.sunk;
        ctx.fillRect(x, y, g0.s - 2, g0.s - 2);
        ctx.strokeStyle = P.lineSoft; ctx.lineWidth = .8;
        ctx.strokeRect(x + .5, y + .5, g0.s - 3, g0.s - 3);
      }
      A.txt(ctx, 'x — 64 numbers (0 or 1)', 40 + N * g0.s / 2, g0.y + N * g0.s + 20,
        { align: 'center', size: 11, fill: P.faint });
      /* layers */
      var hid1 = col(400, 3, 110, 250, 24), out = col(600, 1, 180, 180, 30);
      var labels = ['looks like a 1', 'looks like a 0', 'how much ink'];
      var srcs = col(260, 3, 110, 250, 8);
      for (i = 0; i < 3; i++) {
        A.line(ctx, 40 + N * g0.s, 160, srcs[i].x, srcs[i].y, P.line, 1);
        link(ctx, srcs[i], hid1[i], P.b, 1.4, .6);
        pulse(ctx, srcs[i], hid1[i], t * .7 + i * .2, P.b, 3);
        neuron(ctx, hid1[i], s.h[i], P, s.h[i].toFixed(2), labels[i], P.p);
        link(ctx, hid1[i], out[0], i === 0 ? P.g : P.r, 1.6, .7);
        pulse(ctx, hid1[i], out[0], t * .7 + i * .3, i === 0 ? P.g : P.r, 3);
      }
      neuron(ctx, out[0], s.p, P, (s.p * 100).toFixed(0) + '%', 'P(it is a 1)', P.a);
      A.txt(ctx, 'a[1] — hidden layer', 400, 300, { align: 'center', size: 11, fill: P.faint });
      A.txt(ctx, 'a[2] — output', 600, 300, { align: 'center', size: 11, fill: P.faint });
      A.txt(ctx, 'x → a[1] → a[2].  Numbers only ever flow left to right. That is the whole of "forward propagation".',
        40, 340, { size: 11.5, fill: P.faint });
    }
    function hit(ev) {
      var p = c.pt(ev);
      var q = Math.floor((p.x - g0.x) / g0.s), r = Math.floor((p.y - g0.y) / g0.s);
      if (q >= 0 && q < N && r >= 0 && r < N) {
        grid[r * N + q] = grid[r * N + q] ? 0 : 1; render(lt);
        return true;
      }
      return false;
    }
    c.cv.addEventListener('pointerdown', function (e) { if (hit(e)) e.preventDefault(); });
    var bar = A.ctrls(root);
    A.button(bar, 'clear', function () { for (var i = 0; i < grid.length; i++) grid[i] = 0; render(lt); });
    A.button(bar, 'draw a 1', function () {
      for (var i = 0; i < grid.length; i++) grid[i] = 0;
      [11, 19, 27, 35, 43, 51, 12, 20, 28, 36, 44, 52, 10].forEach(function (i) { grid[i] = 1; }); render(lt);
    });
    A.button(bar, 'draw a 0', function () {
      for (var i = 0; i < grid.length; i++) grid[i] = tmplZero[i]; render(lt);
    });
    A.autoplay(root, c, render);
  });

})();

/* ---------- part 2 : code, data shapes, vectorisation, matrices ---------- */
(function () {
  'use strict';

  function col(x, n, top, bot, r) {
    var out = [], i;
    if (n === 1) return [{ x: x, y: (top + bot) / 2, r: r }];
    for (i = 0; i < n; i++) out.push({ x: x, y: top + (bot - top) * i / (n - 1), r: r });
    return out;
  }
  function link(ctx, p, q, colr, w, alpha) {
    ctx.save(); ctx.globalAlpha = alpha == null ? 1 : alpha;
    ctx.strokeStyle = colr; ctx.lineWidth = w;
    ctx.beginPath(); ctx.moveTo(p.x + p.r, p.y); ctx.lineTo(q.x - q.r, q.y); ctx.stroke(); ctx.restore();
  }
  function neuron(ctx, p, a, P, label, sub, ring) {
    ctx.save();
    ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, 6.2832); ctx.fillStyle = P.panel; ctx.fill();
    ctx.globalAlpha = .15 + .85 * A.clamp(a, 0, 1);
    ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, 6.2832); ctx.fillStyle = ring || P.a; ctx.fill();
    ctx.globalAlpha = 1; ctx.lineWidth = 1.6; ctx.strokeStyle = ring || P.a;
    ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, 6.2832); ctx.stroke(); ctx.restore();
    if (label != null) A.txt(ctx, label, p.x, p.y + 4, { align: 'center', size: 11.5, mono: true, w: 700, fill: a > .55 ? P.panel : P.ink });
    if (sub) A.txt(ctx, sub, p.x, p.y + p.r + 15, { align: 'center', size: 11, fill: P.faint });
  }
  /* a matrix drawn as a grid of cells; returns cell geometry */
  function matrix(ctx, x, y, rows, cols, cw, ch, P, get, opt) {
    opt = opt || {};
    var i, j;
    for (i = 0; i < rows; i++) for (j = 0; j < cols; j++) {
      var cx = x + j * cw, cy = y + i * ch;
      var st = opt.state ? opt.state(i, j) : 0;
      A.rr(ctx, cx, cy, cw - 3, ch - 3, 5);
      ctx.fillStyle = st === 1 ? P.aS : st === 2 ? P.bS : st === 3 ? P.gS : P.sunk;
      ctx.fill();
      ctx.strokeStyle = st === 1 ? P.a : st === 2 ? P.b : st === 3 ? P.g : P.lineSoft;
      ctx.lineWidth = st ? 1.8 : 1; ctx.stroke();
      var v = get(i, j);
      if (v !== null && v !== undefined)
        A.txt(ctx, v, cx + (cw - 3) / 2, cy + (ch - 3) / 2 + 4,
          { align: 'center', size: opt.size || 12, mono: true, w: st ? 700 : 500,
            fill: st === 1 ? P.a : st === 2 ? P.b : st === 3 ? P.g : P.soft });
    }
    /* brackets */
    var W = cols * cw - 3, H = rows * ch - 3;
    ctx.save(); ctx.strokeStyle = P.faint; ctx.lineWidth = 1.8;
    ctx.beginPath();
    ctx.moveTo(x - 7, y - 4); ctx.lineTo(x - 11, y - 4); ctx.lineTo(x - 11, y + H + 4); ctx.lineTo(x - 7, y + H + 4);
    ctx.moveTo(x + W + 7, y - 4); ctx.lineTo(x + W + 11, y - 4); ctx.lineTo(x + W + 11, y + H + 4); ctx.lineTo(x + W + 7, y + H + 4);
    ctx.stroke(); ctx.restore();
    if (opt.label) A.txt(ctx, opt.label, x + W / 2, y - 14, { align: 'center', size: 12, w: 700, fill: opt.labelColor || P.soft });
    if (opt.shape) A.txt(ctx, opt.shape, x + W / 2, y + H + 22, { align: 'center', size: 11, mono: true, fill: P.faint });
    return { w: W, h: H };
  }

  /* ============================================================
     7. TensorFlow inference, line by line
     ============================================================ */
  A.def('codeflow', function (root) {
    var c = A.canvas(root, 760, 260), ctx = c.ctx;
    var lines = [
      ['x = np.array([[200.0, 17.0]])', 'one example: 200°C for 17 minutes'],
      ['layer_1 = Dense(units=3, activation="sigmoid")', 'build hidden layer: 3 neurons'],
      ['a1 = layer_1(x)', 'run it → 3 numbers come out'],
      ['layer_2 = Dense(units=1, activation="sigmoid")', 'build output layer: 1 neuron'],
      ['a2 = layer_2(a1)', 'run it → 1 number, the probability'],
      ['yhat = 1 if a2 >= 0.5 else 0', 'threshold it into a yes / no']
    ];
    var pre = document.createElement('pre');
    pre.innerHTML = lines.map(function (l, i) {
      return '<span class="ln" data-i="' + i + '">' + l[0].replace(/</g, '&lt;') + '</span>';
    }).join('\n');
    root.appendChild(pre);
    var note = A.readout(root);
    var step = 0;
    var a1 = [0.0, 0.0, 0.0], a2 = 0;
    function compute() {
      var x1 = (200 - 175) / 40, x2 = (17 - 13) / 5;
      var W = [[1.9, -1.6], [-2.2, 1.7], [1.4, 1.5]], b = [-0.4, 0.3, -1.1];
      a1 = W.map(function (w, j) { return A.sig(w[0] * x1 + w[1] * x2 + b[j]); });
      a2 = A.sig(3.4 * a1[0] - 2.9 * a1[1] + 2.2 * a1[2] - 1.4);
    }
    compute();
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var ins = col(110, 2, 90, 170, 20), h = col(360, 3, 60, 200, 24), o = col(600, 1, 130, 130, 26);
      var i, j;
      var showA1 = step >= 2, showA2 = step >= 4;
      for (i = 0; i < 2; i++) for (j = 0; j < 3; j++)
        link(ctx, ins[i], h[j], step === 2 ? P.a : P.line, step === 2 ? 2 : .9, step === 2 ? .9 : .35);
      for (j = 0; j < 3; j++) link(ctx, h[j], o[0], step === 4 ? P.a : P.line, step === 4 ? 2 : .9, step === 4 ? .9 : .35);
      if (step === 2) for (i = 0; i < 2; i++) for (j = 0; j < 3; j++) {
        var u = (t * .9 + (i * 3 + j) * .12) % 1;
        A.dot(ctx, A.lerp(ins[i].x + 20, h[j].x - 24, u), A.lerp(ins[i].y, h[j].y, u), 3, P.a);
      }
      if (step === 4) for (j = 0; j < 3; j++) {
        var u2 = (t * .9 + j * .2) % 1;
        A.dot(ctx, A.lerp(h[j].x + 24, o[0].x - 26, u2), A.lerp(h[j].y, o[0].y, u2), 3, P.a);
      }
      neuron(ctx, ins[0], .7, P, '200', 'temperature', step === 0 ? P.a : P.b);
      neuron(ctx, ins[1], .5, P, '17', 'duration', step === 0 ? P.a : P.b);
      for (j = 0; j < 3; j++)
        neuron(ctx, h[j], showA1 ? a1[j] : 0, P, showA1 ? a1[j].toFixed(2) : '?', null,
          (step === 1 || step === 2) ? P.a : P.p);
      A.txt(ctx, 'layer_1  (units = 3)', 360, 232, { align: 'center', size: 11.5, w: 700, fill: (step === 1 || step === 2) ? P.a : P.faint });
      neuron(ctx, o[0], showA2 ? a2 : 0, P, showA2 ? a2.toFixed(2) : '?', null, (step >= 3) ? P.a : P.g);
      A.txt(ctx, 'layer_2  (units = 1)', 600, 232, { align: 'center', size: 11.5, w: 700, fill: step >= 3 ? P.a : P.faint });
      if (step === 5) {
        A.txt(ctx, a2 >= .5 ? 'ŷ = 1  (good roast)' : 'ŷ = 0  (bad roast)', 600, 60,
          { align: 'center', size: 15, w: 700, fill: a2 >= .5 ? P.g : P.r });
      }
      pre.querySelectorAll('.ln').forEach(function (el, i) {
        var on = +el.dataset.i === step;
        el.style.background = on ? A.c('accent-soft') : 'transparent';
        el.style.color = on ? A.c('accent') : A.c('ink-soft');
        el.style.fontWeight = on ? '700' : '400';
        el.style.display = 'block'; el.style.padding = '2px 6px';
        el.style.borderRadius = '4px';
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
     8. Data shapes in NumPy / TensorFlow
     ============================================================ */
  A.def('shapes', function (root) {
    var c = A.canvas(root, 760, 300), ctx = c.ctx;
    var mode = 0;
    var modes = [
      { code: 'np.array([[200, 17]])', rows: 1, cols: 2, shape: '(1, 2)', name: 'row vector — 1 example, 2 features', vals: [[200, 17]] },
      { code: 'np.array([[200],\n          [17]])', rows: 2, cols: 1, shape: '(2, 1)', name: 'column vector — a 2×1 matrix', vals: [[200], [17]] },
      { code: 'np.array([200, 17])', rows: 1, cols: 2, shape: '(2,)', name: '1-D array — NO rows or columns at all', vals: [[200, 17]], flat: true },
      { code: 'np.array([[200, 17],\n          [120, 5],\n          [425, 20]])', rows: 3, cols: 2, shape: '(3, 2)', name: 'the usual training set: 3 examples × 2 features', vals: [[200, 17], [120, 5], [425, 20]] }
    ];
    var bar = A.ctrls(root), ro = A.readout(root);
    modes.forEach(function (m, i) {
      A.button(bar, m.shape, function () { mode = i; render(); syncBtns(); });
    });
    function syncBtns() {
      bar.querySelectorAll('button').forEach(function (b, i) { b.classList.toggle('primary', i === mode); });
    }
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var m = modes[mode];
      var cw = 92, ch = 54;
      var x = 380 - (m.cols * cw) / 2, y = 110 - (m.rows * ch) / 2;
      matrix(ctx, x, y, m.rows, m.cols, cw, ch, P,
        function (i, j) { return String(m.vals[i][j]); },
        { state: function () { return 2; }, size: 15, shape: 'shape = ' + m.shape });
      if (m.flat) {
        A.txt(ctx, 'no outer bracket → it is just a list of numbers', 380, 200,
          { align: 'center', size: 12.5, fill: P.r, w: 600 });
        A.txt(ctx, 'TensorFlow wants the 2-D version', 380, 222, { align: 'center', size: 12, fill: P.faint });
      } else {
        A.txt(ctx, m.rows + ' row' + (m.rows > 1 ? 's' : '') + ' = ' + m.rows + ' training example' + (m.rows > 1 ? 's' : ''),
          380, 200, { align: 'center', size: 12.5, fill: P.soft, w: 600 });
        A.txt(ctx, m.cols + ' column' + (m.cols > 1 ? 's' : '') + ' = ' + m.cols + ' feature' + (m.cols > 1 ? 's' : ''),
          380, 222, { align: 'center', size: 12.5, fill: P.soft, w: 600 });
      }
      /* animated bracket highlight */
      var k = Math.floor(t * 1.5) % (m.rows * m.cols);
      var ki = Math.floor(k / m.cols), kj = k % m.cols;
      ctx.save(); ctx.strokeStyle = P.a; ctx.lineWidth = 2.4; ctx.setLineDash([4, 3]);
      A.rr(ctx, x + kj * cw - 3, y + ki * ch - 3, cw + 1, ch + 1, 7); ctx.stroke(); ctx.restore();
      A.txt(ctx, m.name, 380, 262, { align: 'center', size: 12.5, w: 700, fill: P.a });
      A.txt(ctx, m.code, 40, 40, { size: 13, mono: true, fill: P.soft });
      ro.set('<b>' + m.code.replace(/\n\s+/g, ' ') + '</b>   →   shape ' + m.shape +
        '\nTensorFlow (and Dense layers) always want <b>2-D</b>: rows = examples, columns = features.');
    }
    syncBtns();
    A.autoplay(root, c, render);
  });

  /* ============================================================
     9. Sequential — stacking layers
     ============================================================ */
  A.def('sequential', function (root) {
    var c = A.canvas(root, 760, 300), ctx = c.ctx;
    var ro = A.readout(root);
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var cyc = (t * .35) % 3;
      var boxes = [
        { n: 'input  x', s: 'shape (m, 2)', c: P.b },
        { n: 'Dense(3, "sigmoid")', s: 'a[1] — 3 numbers', c: P.p },
        { n: 'Dense(1, "sigmoid")', s: 'a[2] — 1 number', c: P.g }
      ];
      var y0 = 60, bh = 56, gap = 24;
      for (var i = 0; i < boxes.length; i++) {
        var drop = A.clamp((cyc - i * .55) * 3, 0, 1);
        var ey = y0 + i * (bh + gap) - (1 - A.ease(drop)) * 60;
        var al = .25 + .75 * drop;
        ctx.save(); ctx.globalAlpha = al;
        A.rr(ctx, 200, ey, 360, bh, 10);
        ctx.fillStyle = P.panel; ctx.fill();
        ctx.strokeStyle = boxes[i].c; ctx.lineWidth = 2; ctx.stroke();
        A.txt(ctx, boxes[i].n, 380, ey + 24, { align: 'center', size: 14, w: 700, mono: true, fill: boxes[i].c });
        A.txt(ctx, boxes[i].s, 380, ey + 42, { align: 'center', size: 11.5, fill: P.faint });
        ctx.restore();
        if (i < 2 && drop > .9) A.arrow(ctx, 380, ey + bh + 3, 380, ey + bh + gap - 4, P.line, 2);
      }
      A.txt(ctx, 'model = Sequential([ ... ])', 380, 40, { align: 'center', size: 13, mono: true, w: 700, fill: P.soft });
      A.txt(ctx, 'Sequential just means: “stack these, and feed each one into the next.”', 380, 280,
        { align: 'center', size: 12, fill: P.faint });
    }
    ro.set('model = Sequential([Dense(3, activation="sigmoid"), Dense(1, activation="sigmoid")])\n' +
      'model.compile(...)   ·   model.fit(X, Y)   ·   <b>model.predict(X_new)</b> runs the whole stack for you.');
    A.autoplay(root, c, render);
  });

  /* ============================================================
     10. Forward prop in a single layer — by hand
     ============================================================ */
  A.def('densehand', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var Wm = [[1, -3, 5], [-2, 4, -6]], b = [-1, 1, 2], ain = [0.6, 0.9];
    var stepN = 0, playing = true;
    var ro = A.readout(root);
    function zj(j) { return Wm[0][j] * ain[0] + Wm[1][j] * ain[1] + b[j]; }
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      if (playing) stepN = Math.floor(t * .5) % 4;
      var j = Math.min(stepN, 2), done = stepN;
      matrix(ctx, 60, 80, 2, 1, 62, 46, P, function (i) { return ain[i].toFixed(1); },
        { state: function () { return 2; }, label: 'a_in', shape: '(2,)' });
      matrix(ctx, 200, 80, 2, 3, 62, 46, P, function (i, jj) { return String(Wm[i][jj]); },
        { state: function (i, jj) { return (jj === j && stepN < 3) ? 1 : 0; }, label: 'W', shape: '(2, 3)' });
      matrix(ctx, 200, 200, 1, 3, 62, 46, P, function (i, jj) { return String(b[jj]); },
        { state: function (i, jj) { return (jj === j && stepN < 3) ? 1 : 0; }, label: 'b', shape: '(3,)' });
      matrix(ctx, 470, 80, 1, 3, 62, 46, P,
        function (i, jj) { return jj < done ? A.sig(zj(jj)).toFixed(2) : (jj === j && stepN < 3 ? '…' : ''); },
        { state: function (i, jj) { return jj < done ? 3 : (jj === j && stepN < 3 ? 1 : 0); }, label: 'a_out', shape: '(3,)' });
      if (stepN < 3) {
        var z = zj(j);
        A.txt(ctx, 'unit ' + (j + 1) + ':', 470, 190, { size: 13, w: 700, fill: P.a });
        A.txt(ctx, 'z = ' + Wm[0][j] + '×' + ain[0].toFixed(1) + ' + (' + Wm[1][j] + ')×' + ain[1].toFixed(1) + ' + (' + b[j] + ')',
          470, 212, { size: 12.5, mono: true, fill: P.soft });
        A.txt(ctx, '  = ' + z.toFixed(2), 470, 232, { size: 12.5, mono: true, fill: P.soft });
        A.txt(ctx, 'g(z) = 1/(1+e^−z) = ' + A.sig(z).toFixed(3), 470, 254, { size: 12.5, mono: true, fill: P.g, w: 700 });
      } else {
        A.txt(ctx, 'a_out = [' + [0, 1, 2].map(function (k) { return A.sig(zj(k)).toFixed(2); }).join(', ') + ']',
          470, 212, { size: 13.5, mono: true, w: 700, fill: P.g });
        A.txt(ctx, 'three units → three numbers → one vector', 470, 236, { size: 12, fill: P.faint });
      }
      A.txt(ctx, 'each neuron uses ONE COLUMN of W plus ONE entry of b', 60, 40, { size: 12.5, w: 700, fill: P.soft });
      A.txt(ctx, 'column ' + (j + 1) + ' of W  →  a_out[' + j + ']', 60, 300, { size: 12, fill: P.faint });
      ro.set('w = W[:, ' + j + '] = [' + Wm[0][j] + ', ' + Wm[1][j] + ']    b = b[' + j + '] = ' + b[j] +
        '\nz = np.dot(w, a_in) + b = <b>' + zj(j).toFixed(2) + '</b>    a_out[' + j + '] = g(z) = <b>' + A.sig(zj(j)).toFixed(3) + '</b>');
    }
    var bar = A.ctrls(root);
    A.toggle(bar, 'auto', function (on) { playing = on; }, true);
    A.button(bar, 'step ›', function () { playing = false; stepN = (stepN + 1) % 4; render(lt); });
    A.autoplay(root, c, render);
  });

  /* ============================================================
     11. General dense() — the loop
     ============================================================ */
  A.def('denseloop', function (root) {
    var c = A.canvas(root, 760, 260), ctx = c.ctx;
    var code = [
      'def dense(a_in, W, b):',
      '    units = W.shape[1]          # 3 columns → 3 neurons',
      '    a_out = np.zeros(units)     # empty box for answers',
      '    for j in range(units):      # ← one loop pass per neuron',
      '        w = W[:, j]             #   grab column j',
      '        z = np.dot(w, a_in) + b[j]',
      '        a_out[j] = sigmoid(z)',
      '    return a_out'
    ];
    var pre = document.createElement('pre');
    pre.innerHTML = code.map(function (l, i) { return '<span class="ln" data-i="' + i + '">' + l.replace(/</g, '&lt;') + '</span>'; }).join('\n');
    root.appendChild(pre);
    var Wm = [[1, -3, 5], [-2, 4, -6]], b = [-1, 1, 2], ain = [0.6, 0.9];
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var tick = Math.floor(t * 1.6) % 12;
      var j = Math.floor(tick / 4), sub = tick % 4;
      var lineOn = sub === 0 ? 4 : sub === 1 ? 5 : sub === 2 ? 6 : 3;
      if (tick >= 12) j = 2;
      matrix(ctx, 60, 70, 2, 3, 62, 46, P, function (i, jj) { return String(Wm[i][jj]); },
        { state: function (i, jj) { return jj === j ? 1 : 0; }, label: 'W', shape: 'W.shape = (2, 3)' });
      matrix(ctx, 330, 70, 1, 3, 62, 46, P,
        function (i, jj) { return jj < j ? A.sig(Wm[0][jj] * ain[0] + Wm[1][jj] * ain[1] + b[jj]).toFixed(2)
          : jj === j && sub === 3 ? A.sig(Wm[0][jj] * ain[0] + Wm[1][jj] * ain[1] + b[jj]).toFixed(2) : '0'; },
        { state: function (i, jj) { return jj < j || (jj === j && sub === 3) ? 3 : jj === j ? 1 : 0; }, label: 'a_out', shape: 'filled in one at a time' });
      A.txt(ctx, 'j = ' + j, 600, 60, { size: 24, w: 700, mono: true, fill: P.a });
      var z = Wm[0][j] * ain[0] + Wm[1][j] * ain[1] + b[j];
      A.txt(ctx, 'w = [' + Wm[0][j] + ', ' + Wm[1][j] + ']', 600, 92, { size: 12.5, mono: true, fill: P.soft });
      A.txt(ctx, 'z = ' + z.toFixed(2), 600, 112, { size: 12.5, mono: true, fill: P.soft });
      A.txt(ctx, 'g(z) = ' + A.sig(z).toFixed(3), 600, 132, { size: 12.5, mono: true, fill: P.g, w: 700 });
      A.txt(ctx, 'the loop walks along the columns of W, left to right', 60, 40, { size: 12.5, w: 700, fill: P.soft });
      A.txt(ctx, 'one pass of the loop = one neuron', 60, 210, { size: 12, fill: P.faint });
      pre.querySelectorAll('.ln').forEach(function (el, i) {
        var on = i === lineOn;
        el.style.display = 'block'; el.style.padding = '1px 6px'; el.style.borderRadius = '4px';
        el.style.background = on ? A.c('accent-soft') : 'transparent';
        el.style.color = on ? A.c('accent') : A.c('ink-soft');
        el.style.fontWeight = on ? '700' : '400';
      });
    }
    A.autoplay(root, c, render);
  });

  /* ============================================================
     12. One learning algorithm hypothesis
     ============================================================ */
  A.def('oneAlgo', function (root) {
    var c = A.canvas(root, 760, 300), ctx = c.ctx;
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var phase = (t * .25) % 2;
      /* brain blob */
      ctx.save();
      ctx.beginPath();
      ctx.ellipse(430, 150, 150, 105, 0, 0, 6.2832);
      ctx.fillStyle = P.sunk; ctx.fill(); ctx.strokeStyle = P.line; ctx.lineWidth = 2; ctx.stroke();
      ctx.restore();
      var aud = { x: 380, y: 205 }, vis = { x: 520, y: 120 };
      [[aud, 'auditory cortex', P.p], [vis, 'visual cortex', P.b]].forEach(function (r) {
        ctx.save(); ctx.beginPath(); ctx.ellipse(r[0].x, r[0].y, 62, 38, 0, 0, 6.2832);
        ctx.fillStyle = r[2]; ctx.globalAlpha = .18; ctx.fill(); ctx.globalAlpha = 1;
        ctx.strokeStyle = r[2]; ctx.lineWidth = 1.8; ctx.stroke(); ctx.restore();
        A.txt(ctx, r[1], r[0].x, r[0].y + 4, { align: 'center', size: 11.5, w: 700, fill: r[2] });
      });
      /* eye + ear sources */
      A.txt(ctx, '👁', 90, 120, { size: 34 });
      A.txt(ctx, '👂', 90, 235, { size: 34 });
      A.txt(ctx, 'eye', 100, 145, { align: 'center', size: 11, fill: P.faint });
      A.txt(ctx, 'ear', 100, 258, { align: 'center', size: 11, fill: P.faint });
      var rewired = phase > 1;
      /* ear → auditory (normal) */
      A.line(ctx, 120, 225, aud.x - 62, aud.y, rewired ? P.lineSoft : P.p, rewired ? 1.2 : 2.4, rewired ? [4, 4] : null);
      /* eye → visual (normal) or eye → auditory (rewired) */
      if (!rewired) {
        A.line(ctx, 120, 110, vis.x - 62, vis.y, P.b, 2.4);
        for (var i = 0; i < 3; i++) {
          var u = ((t * .8 + i * .33) % 1);
          A.dot(ctx, A.lerp(120, vis.x - 62, u), A.lerp(110, vis.y, u), 3.4, P.b);
        }
      } else {
        ctx.save(); ctx.strokeStyle = P.b; ctx.lineWidth = 2.4;
        ctx.beginPath(); ctx.moveTo(120, 110);
        ctx.quadraticCurveTo(230, 60, aud.x - 62, aud.y - 10); ctx.stroke(); ctx.restore();
        for (var k = 0; k < 3; k++) {
          var u2 = ((t * .8 + k * .33) % 1);
          var px = (1 - u2) * (1 - u2) * 120 + 2 * (1 - u2) * u2 * 230 + u2 * u2 * (aud.x - 62);
          var py = (1 - u2) * (1 - u2) * 110 + 2 * (1 - u2) * u2 * 60 + u2 * u2 * (aud.y - 10);
          A.dot(ctx, px, py, 3.4, P.b);
        }
      }
      A.txt(ctx, rewired ? 'REWIRED: eye plugged into the hearing part' : 'normal wiring',
        640, 40, { align: 'right', size: 13, w: 700, fill: rewired ? P.a : P.faint });
      A.txt(ctx, rewired ? '…and the hearing tissue learns to SEE.' : 'each patch of brain does its own job',
        640, 62, { align: 'right', size: 12, fill: P.faint });
      A.txt(ctx, 'The “one learning algorithm” hypothesis: maybe one piece of brain tissue can learn ANY input,',
        40, 285, { size: 11.5, fill: P.faint });
    }
    A.autoplay(root, c, render);
  });

  /* ============================================================
     13. Loop vs vectorised
     ============================================================ */
  A.def('vectorize', function (root) {
    var c = A.canvas(root, 760, 300), ctx = c.ctx;
    var N = 16;
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var cyc = (t * .55) % 1.9;
      A.txt(ctx, 'for-loop: one at a time', 40, 40, { size: 13, w: 700, fill: P.r });
      A.txt(ctx, 'vectorised: all at once', 420, 40, { size: 13, w: 700, fill: P.g });
      var done = Math.min(N, Math.floor(cyc / (1.6 / N)));
      var i, x, y;
      for (i = 0; i < N; i++) {
        x = 40 + (i % 8) * 40; y = 60 + Math.floor(i / 8) * 40;
        A.rr(ctx, x, y, 34, 34, 6);
        ctx.fillStyle = i < done ? P.gS : i === done ? P.aS : P.sunk; ctx.fill();
        ctx.strokeStyle = i < done ? P.g : i === done ? P.a : P.lineSoft;
        ctx.lineWidth = i === done ? 2 : 1; ctx.stroke();
        A.txt(ctx, String(i), x + 17, y + 22, { align: 'center', size: 11, mono: true, fill: P.faint });
      }
      var allOn = cyc > 1.6 ? 1 : 0;
      for (i = 0; i < N; i++) {
        x = 420 + (i % 8) * 40; y = 60 + Math.floor(i / 8) * 40;
        A.rr(ctx, x, y, 34, 34, 6);
        ctx.fillStyle = allOn ? P.gS : P.sunk; ctx.fill();
        ctx.strokeStyle = allOn ? P.g : P.lineSoft; ctx.lineWidth = allOn ? 2 : 1; ctx.stroke();
        A.txt(ctx, String(i), x + 17, y + 22, { align: 'center', size: 11, mono: true, fill: P.faint });
      }
      /* timing bars */
      A.txt(ctx, 'steps taken: ' + done + ' / ' + N, 40, 175, { size: 12, mono: true, fill: P.soft });
      A.txt(ctx, 'steps taken: ' + (allOn ? 1 : 0) + ' / 1', 420, 175, { size: 12, mono: true, fill: P.soft });
      A.rr(ctx, 40, 190, 320 * (done / N), 12, 6); ctx.fillStyle = P.r; ctx.fill();
      A.rr(ctx, 40, 190, 320, 12, 6); ctx.strokeStyle = P.line; ctx.lineWidth = 1; ctx.stroke();
      A.rr(ctx, 420, 190, 320 * allOn * 0.11, 12, 6); ctx.fillStyle = P.g; ctx.fill();
      A.rr(ctx, 420, 190, 320, 12, 6); ctx.strokeStyle = P.line; ctx.lineWidth = 1; ctx.stroke();
      A.txt(ctx, 'Python has to walk the list itself. Slow.', 40, 232, { size: 12, fill: P.faint });
      A.txt(ctx, 'NumPy hands the whole array to hardware that', 420, 232, { size: 12, fill: P.faint });
      A.txt(ctx, 'multiplies many numbers in parallel. Fast.', 420, 250, { size: 12, fill: P.faint });
      A.txt(ctx, 'Same maths. Same answer. Very different running time — this is why GPUs matter.',
        40, 285, { size: 12, w: 600, fill: P.soft });
    }
    A.autoplay(root, c, render);
  });

  /* ============================================================
     14. Dot product, animated
     ============================================================ */
  A.def('dotprod', function (root) {
    var c = A.canvas(root, 760, 280), ctx = c.ctx;
    var a = [1, 2, 3], w = [4, 5, 6];
    var ro = A.readout(root);
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var k = Math.floor((t * .8) % 4.4);
      var shown = Math.min(k, 3);
      matrix(ctx, 90, 70, 1, 3, 66, 50, P, function (i, j) { return String(a[j]); },
        { state: function (i, j) { return j === k ? 1 : j < k ? 2 : 0; }, label: 'a  (a row)', size: 15 });
      A.txt(ctx, '·', 320, 105, { size: 30, align: 'center', fill: P.faint });
      matrix(ctx, 360, 40, 3, 1, 66, 50, P, function (i) { return String(w[i]); },
        { state: function (i) { return i === k ? 1 : i < k ? 2 : 0; }, label: 'w  (a column)', size: 15 });
      A.txt(ctx, '=', 470, 105, { size: 26, align: 'center', fill: P.faint });
      var terms = [], sum = 0;
      for (var i = 0; i < shown; i++) { terms.push(a[i] + '×' + w[i]); sum += a[i] * w[i]; }
      A.txt(ctx, terms.length ? terms.join('  +  ') : '…', 520, 95, { size: 15, mono: true, fill: P.soft });
      if (shown > 0) A.txt(ctx, '= ' + sum, 520, 122, { size: 20, mono: true, w: 700, fill: k >= 3 ? P.g : P.a });
      if (k < 3) {
        A.txt(ctx, 'pair up number ' + (k + 1) + ' with number ' + (k + 1) + ', multiply, and add to the running total',
          90, 200, { size: 12.5, fill: P.soft });
        /* draw the pairing line */
        A.line(ctx, 90 + k * 66 + 31, 122, 393, 40 + k * 50 + 24, P.a, 1.6, [4, 3]);
      } else {
        A.txt(ctx, 'a · w = 1×4 + 2×5 + 3×6 = 32   →   ONE number', 90, 200, { size: 13.5, mono: true, w: 700, fill: P.g });
      }
      A.txt(ctx, 'A dot product turns two lists of numbers into a single number.', 90, 240, { size: 12, fill: P.faint });
      A.txt(ctx, 'That single number is exactly what one neuron needs.', 90, 260, { size: 12, fill: P.faint });
      ro.set('np.dot(a, w) = <b>32</b>    ·    in maths this is written  <b>a · w</b>  or  <b>a<sup>T</sup>w</b>' +
        '\nBoth lists must be the SAME length, or there is nothing to pair up.');
    }
    A.autoplay(root, c, render);
  });

  /* ============================================================
     15. Matrix × matrix, cell by cell
     ============================================================ */
  A.def('matmul', function (root) {
    var c = A.canvas(root, 760, 340), ctx = c.ctx;
    var Am = [[1, -1, 0.1], [2, -2, 0.2]];        /* 2 x 3 */
    var Bm = [[3, 5, 7, 9], [4, 6, 8, 10], [1, 1, 1, 1]];  /* 3 x 4 */
    var R = 2, K = 3, C = 4;
    function cell(i, j) { var s = 0; for (var k = 0; k < K; k++) s += Am[i][k] * Bm[k][j]; return s; }
    var ro = A.readout(root);
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var n = R * C, idx = Math.floor((t * .9) % (n + 2));
      var cur = Math.min(idx, n - 1), ci = Math.floor(cur / C), cj = cur % C;
      var doneAll = idx >= n;
      matrix(ctx, 60, 90, R, K, 54, 44, P, function (i, k) { return Am[i][k].toString(); },
        { state: function (i) { return (!doneAll && i === ci) ? 1 : 0; }, label: 'A   (2 × 3)', size: 12 });
      A.txt(ctx, '×', 240, 130, { size: 24, align: 'center', fill: P.faint });
      matrix(ctx, 275, 68, K, C, 50, 44, P, function (k, j) { return Bm[k][j].toString(); },
        { state: function (k, j) { return (!doneAll && j === cj) ? 2 : 0; }, label: 'W   (3 × 4)', size: 12 });
      A.txt(ctx, '=', 500, 130, { size: 24, align: 'center', fill: P.faint });
      matrix(ctx, 535, 90, R, C, 52, 44, P,
        function (i, j) { var o = i * C + j; return (o < idx || doneAll) ? cell(i, j).toFixed(1) : ''; },
        { state: function (i, j) { var o = i * C + j; return (o === cur && !doneAll) ? 1 : (o < idx || doneAll) ? 3 : 0; },
          label: 'Z   (2 × 4)', size: 11 });
      /* the rule */
      A.txt(ctx, '(2 × 3) × (3 × 4)  →  (2 × 4)', 380, 40, { align: 'center', size: 14, mono: true, w: 700, fill: P.soft });
      A.txt(ctx, 'the inner 3s must match — they are what gets paired up and summed away',
        380, 60, { align: 'center', size: 11.5, fill: P.faint });
      if (!doneAll) {
        var parts = [];
        for (var k = 0; k < K; k++) parts.push(Am[ci][k] + '×' + Bm[k][cj]);
        A.txt(ctx, 'Z[' + ci + '][' + cj + '] = row ' + (ci + 1) + ' of A  ·  column ' + (cj + 1) + ' of W',
          60, 250, { size: 13, w: 700, fill: P.a });
        A.txt(ctx, '= ' + parts.join('  +  ') + '  =  ' + cell(ci, cj).toFixed(1),
          60, 274, { size: 13, mono: true, fill: P.soft });
      } else {
        A.txt(ctx, 'every cell of Z is one dot product: a row meeting a column.', 60, 262, { size: 13, w: 700, fill: P.g });
      }
      A.txt(ctx, 'Matrix multiply = a whole table of dot products, computed in one go.', 60, 315, { size: 12, fill: P.faint });
      ro.set('Rows of the answer come from rows of <b>A</b>. Columns of the answer come from columns of <b>W</b>.' +
        '\nShape rule: <b>(m × n) × (n × p) = (m × p)</b> — the two inner numbers must be equal.');
    }
    A.autoplay(root, c, render);
  });

  /* ============================================================
     16. Matmul in code = a whole dense layer
     ============================================================ */
  A.def('matmulcode', function (root) {
    var c = A.canvas(root, 760, 300), ctx = c.ctx;
    var AT = [[200, 17]], Wm = [[1, -3, 5], [-2, 4, -6]], b = [[-1, 1, 2]];
    function z(j) { return AT[0][0] * Wm[0][j] + AT[0][1] * Wm[1][j] + b[0][j]; }
    var ro = A.readout(root);
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var stage = Math.floor((t * .5) % 3);
      matrix(ctx, 50, 110, 1, 2, 66, 46, P, function (i, j) { return String(AT[0][j]); },
        { state: function () { return 2; }, label: 'A_T  (1 × 2)' });
      A.txt(ctx, '@', 200, 138, { size: 22, align: 'center', fill: P.faint });
      matrix(ctx, 230, 88, 2, 3, 58, 46, P, function (i, j) { return String(Wm[i][j]); },
        { state: function () { return stage >= 1 ? 1 : 0; }, label: 'W  (2 × 3)' });
      A.txt(ctx, '+', 430, 138, { size: 22, align: 'center', fill: P.faint });
      matrix(ctx, 460, 110, 1, 3, 58, 46, P, function (i, j) { return String(b[0][j]); },
        { state: function () { return stage >= 2 ? 1 : 0; }, label: 'b  (1 × 3)' });
      A.txt(ctx, '=', 650, 138, { size: 22, align: 'center', fill: P.faint });
      matrix(ctx, 620, 200, 1, 3, 46, 40, P, function (i, j) { return z(j).toFixed(0); },
        { state: function () { return 3; }, label: 'Z  (1 × 3)', size: 11 });
      A.txt(ctx, 'one line of NumPy = one whole layer, for every example at once',
        50, 40, { size: 13, w: 700, fill: P.soft });
      A.txt(ctx, 'Z = np.matmul(A_T, W) + b', 50, 70, { size: 14, mono: true, w: 700, fill: P.a });
      A.txt(ctx, 'A_out = g(Z)', 50, 232, { size: 14, mono: true, w: 700, fill: P.g });
      A.txt(ctx, 'No Python loop anywhere. NumPy walks the rows and columns for you, in fast compiled code.',
        50, 272, { size: 12, fill: P.faint });
      ro.set('def dense(A_T, W, b):\n    Z = np.matmul(A_T, W) + b\n    return g(Z)' +
        '\n\nRows of <b>A_T</b> = your examples. Columns of <b>W</b> = your neurons. Every example meets every neuron in one shot.');
    }
    A.autoplay(root, c, render);
  });

})();
