/* Widgets for Course 4 / Week 3 — the transformer block */
(function () {
  'use strict';

  /* ============================================================
     1. Positional encoding
     ============================================================ */
  A.def('c4-posenc', function (root) {
    var c = A.canvas(root, 760, 340), ctx = c.ctx;
    var d = 8, T = 24, pos = 3;
    var bar = A.ctrls(root), log = A.log(root), ro = A.readout(root);
    A.slider(bar, { label: 'position', min: 0, max: 23, step: 1, value: pos,
      fmt: function (v) { return v.toFixed(0); }, on: function (v) { pos = v; render(); } });
    function pe(p, k) {
      var i = Math.floor(k / 2), denom = Math.pow(10000, 2 * i / d);
      return (k % 2 === 0) ? Math.sin(p / denom) : Math.cos(p / denom);
    }
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var box = { x: 70, y: 40, w: 620, h: 170 };
      var S = A.axes(ctx, box, [0, T - 1], [-1.15, 1.15], {
        xticks: 6, yticks: 4, xfmt: function (v) { return v.toFixed(0); },
        yfmt: function (v) { return v.toFixed(1); }, xlab: 'position', ylab: 'value'
      });
      var cols = [P.a, P.b, P.p, P.g];
      for (var k = 0; k < 8; k += 2) {
        A.plot(ctx, S, [0, T - 1], function (x) { return pe(x, k); }, cols[k / 2], k === 0 ? 2.4 : 1.8);
      }
      A.txt(ctx, 'dim 0 — fast', 90, 60, { size: 11, w: 700, fill: cols[0] });
      A.txt(ctx, 'dim 2', 190, 60, { size: 11, w: 700, fill: cols[1] });
      A.txt(ctx, 'dim 4', 250, 60, { size: 11, w: 700, fill: cols[2] });
      A.txt(ctx, 'dim 6 — slow', 310, 60, { size: 11, w: 700, fill: cols[3] });
      ctx.save(); ctx.strokeStyle = P.a; ctx.lineWidth = 1.6; ctx.setLineDash([4, 4]);
      ctx.beginPath(); ctx.moveTo(S.X(pos), S.Y(-1.15)); ctx.lineTo(S.X(pos), S.Y(1.15));
      ctx.stroke(); ctx.restore();
      /* the fingerprint at this position */
      A.txt(ctx, 'the encoding at position ' + pos + ':', 70, 250, { size: 12.5, w: 700, fill: P.soft });
      var vals = [];
      for (var q = 0; q < 8; q++) vals.push(pe(pos, q));
      vals.forEach(function (v, q) {
        var x = 70 + q * 78;
        A.rr(ctx, x, 260, 70, 34, 5);
        ctx.fillStyle = v >= 0 ? P.bS : P.rS; ctx.fill();
        ctx.strokeStyle = v >= 0 ? P.b : P.r; ctx.stroke();
        A.txt(ctx, v.toFixed(3), x + 35, 282, { align: 'center', size: 11, mono: true, fill: P.soft });
      });
      var nrm = Math.sqrt(vals.reduce(function (a, b) { return a + b * b; }, 0));
      A.txt(ctx, 'This pattern is added to the word embedding before attention ever runs.',
        70, 322, { size: 12, fill: P.faint });
      log.set('position ' + pos + '  ·  ‖PE‖ = ' + nrm.toFixed(4) +
        '  (the same for every position, because sin² + cos² = 1)',
        'PE(pos, 2i) = sin(pos / 10000^(2i/d))   PE(pos, 2i+1) = cos(same)');
      ro.set('Fast dimensions separate neighbours; slow ones separate distant positions.\n' +
        'Read together, the combination names one position uniquely — like clock hands.');
    }
    A.bind(c, render); render();
  });

  /* ============================================================
     2. Residual connections
     ============================================================ */
  A.def('c4-residual', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var nLayers = 12, useRes = true;
    var bar = A.ctrls(root), log = A.log(root), ro = A.readout(root);
    A.slider(bar, { label: 'layers', min: 1, max: 48, step: 1, value: nLayers,
      fmt: function (v) { return v.toFixed(0); }, on: function (v) { nLayers = v; render(); } });
    A.toggle(bar, 'residual connection', function (v) { useRes = v; render(); }, true);
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var box = { x: 70, y: 40, w: 620, h: 190 };
      var S = A.axes(ctx, box, [1, 48], [-9, 0.4], {
        xticks: 5, yticks: 4, xfmt: function (v) { return v.toFixed(0); },
        yfmt: function (v) { return '1e' + v.toFixed(0); },
        xlab: 'depth (layers)', ylab: 'gradient reaching layer 1'
      });
      A.plot(ctx, S, [1, 48], function (n) { return Math.max(-9, Math.log10(Math.pow(0.7, n))); },
        P.r, 2.4);
      ctx.save(); ctx.strokeStyle = P.g; ctx.lineWidth = 2.4; ctx.setLineDash([5, 4]);
      ctx.beginPath(); ctx.moveTo(S.X(1), S.Y(0)); ctx.lineTo(S.X(48), S.Y(0)); ctx.stroke(); ctx.restore();
      A.txt(ctx, 'with residual — the identity path never shrinks', S.X(14), S.Y(0) - 10,
        { size: 11.5, w: 700, fill: P.g });
      A.txt(ctx, 'without — 0.7 per layer, multiplied', S.X(6), S.Y(-3.4),
        { size: 11.5, w: 700, fill: P.r });
      var g = Math.pow(0.7, nLayers);
      A.dot(ctx, S.X(nLayers), S.Y(useRes ? 0 : Math.max(-9, Math.log10(g))), 6, useRes ? P.g : P.r);
      A.txt(ctx, useRes ? 'y = x + Sublayer(x)      →      ∂y/∂x = 1 + ∂Sublayer/∂x'
                        : 'y = Sublayer(x)          →      ∂y/∂x = ∂Sublayer/∂x',
        70, 268, { size: 13, mono: true, w: 700, fill: useRes ? P.g : P.r });
      A.txt(ctx, useRes ? 'The 1 is a route home that no chain of multiplications can shrink.'
                        : 'Every layer multiplies the gradient again. Nothing protects it.',
        70, 294, { size: 12, fill: P.faint });
      A.txt(ctx, 'The same enemy as C2 W2 and C4 W1: many numbers below 1, multiplied.',
        70, 318, { size: 11.5, fill: P.faint });
      log.set('depth ' + nLayers + ':  without residual → ' + g.toExponential(3) +
        '   with residual → ≥ 1', 'y = x + f(x)  ⇒  ∂y/∂x = 1 + f′(x)');
      ro.set('This is the idea (ResNet, 2015) that made very deep networks trainable.\n' +
        'A transformer uses it twice in every single block.');
    }
    A.bind(c, render); render();
  });

  /* ============================================================
     3. Layer normalization
     ============================================================ */
  A.def('c4-layernorm', function (root) {
    var c = A.canvas(root, 760, 320), ctx = c.ctx;
    var vals = [2, 8, 4, 6];
    var bar = A.ctrls(root), log = A.log(root), ro = A.readout(root);
    vals.forEach(function (v, i) {
      A.slider(bar, { label: 'x' + (i + 1), min: -6, max: 14, step: 1, value: v,
        fmt: function (q) { return q.toFixed(0); }, on: function (q) { vals[i] = q; render(); } });
    });
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var mu = vals.reduce(function (a, b) { return a + b; }, 0) / vals.length;
      var sd = Math.sqrt(vals.reduce(function (a, b) { return a + (b - mu) * (b - mu); }, 0) / vals.length);
      var out = vals.map(function (v) { return sd === 0 ? 0 : (v - mu) / sd; });
      A.txt(ctx, 'before — one position’s vector', 60, 44, { size: 12.5, w: 700, fill: P.soft });
      vals.forEach(function (v, i) {
        var x = 60 + i * 150, h = Math.abs(v) * 6;
        A.rr(ctx, x, 100 - (v > 0 ? h : 0), 130, Math.max(4, h), 5);
        ctx.fillStyle = v >= 0 ? P.bS : P.rS; ctx.fill();
        ctx.strokeStyle = v >= 0 ? P.b : P.r; ctx.stroke();
        A.txt(ctx, String(v), x + 65, 122, { align: 'center', size: 13, mono: true, w: 700, fill: P.soft });
      });
      A.txt(ctx, 'mean = ' + mu.toFixed(3) + '   std = ' + sd.toFixed(4), 60, 148,
        { size: 12, mono: true, fill: P.faint });
      A.arrow(ctx, 375, 160, 375, 184, P.a, 2.2);
      A.txt(ctx, 'subtract the mean, divide by the standard deviation', 395, 178,
        { size: 11.5, fill: P.a });
      A.txt(ctx, 'after', 60, 214, { size: 12.5, w: 700, fill: P.g });
      out.forEach(function (v, i) {
        var x = 60 + i * 150, h = Math.abs(v) * 26;
        A.rr(ctx, x, 262 - (v > 0 ? h : 0), 130, Math.max(4, h), 5);
        ctx.fillStyle = P.gS; ctx.fill(); ctx.strokeStyle = P.g; ctx.stroke();
        A.txt(ctx, v.toFixed(3), x + 65, 284, { align: 'center', size: 13, mono: true, w: 700, fill: P.g });
      });
      var m2 = out.reduce(function (a, b) { return a + b; }, 0) / out.length;
      A.txt(ctx, 'mean = ' + m2.toFixed(4) + '   std = ' +
        Math.sqrt(out.reduce(function (a, b) { return a + (b - m2) * (b - m2); }, 0) / out.length).toFixed(4),
        60, 310, { size: 12, mono: true, w: 700, fill: P.g });
      log.set('mean ' + mu.toFixed(3) + ' → 0.0000   ·   std ' + sd.toFixed(4) + ' → 1.0000',
        'LN(x) = γ · (x − μ)/σ + β    (γ and β are learned, one per feature)');
      ro.set('This is the z-score from C1 W2, applied inside the network instead of at the input.\n' +
        'It normalises across one position’s features — <b>not</b> across the batch.');
    }
    A.bind(c, render); render();
  });

  /* ============================================================
     4. The feed-forward layer
     ============================================================ */
  A.def('c4-ffn', function (root) {
    var c = A.canvas(root, 760, 320), ctx = c.ctx;
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var stage = Math.floor((t * 0.55) % 3);
      var stages = [
        ['512 in', 'one position’s vector arrives', 130, P.b],
        ['2048 wide', 'expand, then ReLU — this is where the non-linearity happens', 320, P.a],
        ['512 out', 'shrink back, so the block’s output matches its input', 130, P.g]
      ];
      stages.forEach(function (s, i) {
        var x = 70 + i * 230, on = i === stage;
        var h = s[2] * 0.62;
        A.rr(ctx, x, 150 - h / 2, 170, h, 9);
        ctx.fillStyle = on ? (i === 1 ? P.aS : i === 0 ? P.bS : P.gS) : P.sunk; ctx.fill();
        ctx.strokeStyle = on ? s[3] : P.lineSoft; ctx.lineWidth = on ? 2.4 : 1.2; ctx.stroke();
        A.txt(ctx, s[0], x + 85, 154, { align: 'center', size: 15, w: 700, fill: on ? s[3] : P.faint });
        if (i < 2) A.arrow(ctx, x + 176, 150, x + 224, 150, on ? s[3] : P.line, on ? 2.4 : 1.4);
      });
      A.txt(ctx, stages[stage][1], 70, 250, { size: 12.5, w: 700, fill: stages[stage][3] });
      A.txt(ctx, 'The SAME network is applied at every position, independently. No information',
        70, 278, { size: 12, fill: P.faint });
      A.txt(ctx, 'moves between positions here — that was attention’s job.', 70, 298,
        { size: 12, w: 700, fill: P.a });
      A.txt(ctx, 'Two thirds of a block’s parameters live in this hourglass.', 70, 44,
        { size: 12.5, w: 700, fill: P.soft });
    }
    A.autoplay(root, c, render);
  });

  /* ============================================================
     5. The block, assembled
     ============================================================ */
  A.def('c4-block', function (root) {
    var c = A.canvas(root, 760, 350), ctx = c.ctx;
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var step = Math.floor((t * 0.5) % 6);
      var rows = [
        ['layer norm', 'standardise each position', P.p, false],
        ['attention', 'gather from other positions', P.a, true],
        ['+ residual', 'add the input back', P.g, false],
        ['layer norm', 'standardise again', P.p, false],
        ['feed-forward', 'process each position alone', P.b, false],
        ['+ residual', 'add the input back again', P.g, false]
      ];
      rows.forEach(function (r, i) {
        var y = 46 + i * 48, on = i === step;
        A.rr(ctx, 180, y, 400, 40, 8);
        ctx.fillStyle = on ? P.aS : P.sunk; ctx.fill();
        ctx.strokeStyle = on ? P.a : P.lineSoft; ctx.lineWidth = on ? 2.2 : 1; ctx.stroke();
        A.txt(ctx, r[0], 200, y + 25, { size: 13, w: 700, fill: on ? P.a : r[2] });
        A.txt(ctx, r[1], 350, y + 25, { size: 11.5, fill: P.faint });
        if (r[3]) A.txt(ctx, '← the only place positions interact', 594, y + 25,
          { size: 11, w: 700, fill: P.a });
        if (i < 5) A.arrow(ctx, 380, y + 41, 380, y + 46, P.line, 1.4);
      });
      /* residual arcs */
      [[46, 142], [190, 286]].forEach(function (p) {
        ctx.save(); ctx.strokeStyle = P.g; ctx.lineWidth = 1.8; ctx.setLineDash([4, 3]);
        ctx.beginPath(); ctx.moveTo(176, p[0] + 8);
        ctx.quadraticCurveTo(120, (p[0] + p[1]) / 2, 176, p[1] + 20);
        ctx.stroke(); ctx.restore();
      });
      A.txt(ctx, 'two sublayers, each wrapped the same way', 180, 32,
        { size: 12.5, w: 700, fill: P.soft });
      A.txt(ctx, 'Output has the same shape as the input — which is the whole reason blocks stack.',
        60, 336, { size: 12, w: 700, fill: P.g });
    }
    A.autoplay(root, c, render);
  });

  /* ============================================================
     6. Stacking
     ============================================================ */
  A.def('c4-stack', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var depth = 4;
    var bar = A.ctrls(root), ro = A.readout(root);
    A.slider(bar, { label: 'blocks', min: 1, max: 12, step: 1, value: depth,
      fmt: function (v) { return v.toFixed(0); }, on: function (v) { depth = v; render(); } });
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var N = 9;
      A.txt(ctx, 'how far information has travelled after ' + depth + ' block' +
        (depth === 1 ? '' : 's'), 60, 42, { size: 12.5, w: 700, fill: P.soft });
      for (var i = 0; i < N; i++) {
        var x = 60 + i * 76;
        /* after d blocks, position 4 has reached everything within d hops -- here all positions
           are reachable in one block, so shade by how many rounds of mixing have happened */
        var lit = Math.min(1, depth / 3);
        A.rr(ctx, x, 70, 66, 40, 6);
        ctx.save(); ctx.globalAlpha = 0.25 + 0.75 * lit;
        ctx.fillStyle = P.aS; ctx.fill(); ctx.restore();
        ctx.strokeStyle = P.a; ctx.lineWidth = 1.4; ctx.stroke();
        A.txt(ctx, 'pos ' + (i + 1), x + 33, 95, { align: 'center', size: 11, fill: P.a });
      }
      for (var b = 0; b < depth; b++) {
        var y = 128 + b * 15;
        if (y > 250) break;
        A.rr(ctx, 60 + b * 3, y, 640 - b * 6, 11, 3);
        ctx.fillStyle = P.sunk; ctx.fill(); ctx.strokeStyle = P.lineSoft; ctx.stroke();
      }
      A.txt(ctx, depth + ' identical block' + (depth === 1 ? '' : 's') + ', each with its own weights',
        60, 274, { size: 12, fill: P.faint });
      A.txt(ctx, 'Each block gathers from positions that have already gathered. Information compounds.',
        60, 298, { size: 12, w: 700, fill: P.a });
      A.txt(ctx, 'GPT-2 small: 12 blocks.  GPT-3: 96.', 60, 320, { size: 11.5, fill: P.faint });
      ro.set('The “early layers = syntax, late = semantics” story is a reasonable sketch of probing ' +
        'results — and is cited far more confidently than the evidence supports.');
    }
    A.bind(c, render); render();
  });

  /* ============================================================
     7. GPT vs BERT
     ============================================================ */
  A.def('c4-gptbert', function (root) {
    var c = A.canvas(root, 760, 320), ctx = c.ctx;
    var causal = true;
    var bar = A.ctrls(root), ro = A.readout(root);
    A.toggle(bar, 'causal mask', function (v) { causal = v; render(); }, true);
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var N = 5;
      A.matrix(ctx, 90, 76, N, N, 58, 34, P, function (i, j) {
        return (causal && j > i) ? '' : '●';
      }, { state: function (i, j) { return (causal && j > i) ? 0 : 3; }, size: 11,
           label: causal ? 'GPT — causal' : 'BERT — bidirectional' });
      var facts = causal
        ? [['can generate text', 'yes — one token at a time', P.g],
           ['sees the future', 'no', P.g],
           ['trained to', 'predict the next token', P.soft],
           ['good at', 'writing, completion, chat', P.soft]]
        : [['can generate text', 'no', P.r],
           ['sees the future', 'yes — the whole sentence', P.b],
           ['trained to', 'fill in hidden tokens', P.soft],
           ['good at', 'classification, search, extraction', P.soft]];
      facts.forEach(function (f, i) {
        var y = 86 + i * 42;
        A.txt(ctx, f[0], 620, y, { align: 'right', size: 11.5, fill: P.faint });
        A.txt(ctx, f[1], 630, y, { size: 12.5, w: 700, fill: f[2] });
      });
      A.txt(ctx, 'The block itself is identical in both. One triangle of −∞ is the whole difference.',
        90, 284, { size: 12.5, w: 700, fill: P.a });
      A.txt(ctx, 'There is also an encoder–decoder arrangement using both — the 2017 original, and T5.',
        90, 306, { size: 11.5, fill: P.faint });
      ro.set('Decoder-only dominates public attention because <b>generation is visible</b> — not ' +
        'because it wins everywhere.\nFor pure classification a BERT-style encoder is often more ' +
        'accurate and much cheaper to run.');
    }
    A.bind(c, render); render();
  });

  /* ============================================================
     8. Counting a real model
     ============================================================ */
  A.def('c4-count', function (root) {
    var c = A.canvas(root, 760, 340), ctx = c.ctx;
    var d = 768, L = 12, V = 50257, ctxLen = 1024;
    var bar = A.ctrls(root), log = A.log(root), ro = A.readout(root);
    A.slider(bar, { label: 'width d', min: 128, max: 2048, step: 64, value: d,
      fmt: function (v) { return v.toFixed(0); }, on: function (v) { d = v; render(); } });
    A.slider(bar, { label: 'layers', min: 2, max: 48, step: 1, value: L,
      fmt: function (v) { return v.toFixed(0); }, on: function (v) { L = v; render(); } });
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var emb = V * d, pemb = ctxLen * d;
      var attn = 4 * d * d, ff = 2 * d * (4 * d), ln = 4 * d;
      var blk = attn + ff + ln, total = emb + pemb + L * blk;
      var rows = [
        ['token embeddings', V + ' × ' + d, emb, P.p],
        ['positional embeddings', ctxLen + ' × ' + d, pemb, P.p],
        ['attention × ' + L, '4 × ' + d + '² × ' + L, attn * L, P.a],
        ['feed-forward × ' + L, '2 × ' + d + ' × ' + (4 * d) + ' × ' + L, ff * L, P.b],
        ['layer norms × ' + L, '4 × ' + d + ' × ' + L, ln * L, P.faint]
      ];
      A.txt(ctx, 'every number in a model card, computed from first principles', 60, 40,
        { size: 12.5, w: 700, fill: P.soft });
      rows.forEach(function (r, i) {
        var y = 62 + i * 42;
        A.txt(ctx, r[0], 60, y + 22, { size: 12.5, w: 700, fill: r[3] });
        A.txt(ctx, r[1], 250, y + 22, { size: 11.5, mono: true, fill: P.faint });
        var frac = r[2] / total;
        A.rr(ctx, 400, y + 8, Math.max(3, 200 * frac), 18, 4);
        ctx.fillStyle = r[3]; ctx.globalAlpha = .55; ctx.fill(); ctx.globalAlpha = 1;
        A.txt(ctx, (r[2] / 1e6).toFixed(1) + ' M', 614, y + 22, { size: 12, mono: true, fill: P.soft });
        A.txt(ctx, (frac * 100).toFixed(1) + '%', 700, y + 22, { size: 11.5, mono: true, fill: P.faint });
      });
      A.rr(ctx, 60, 278, 640, 42, 8);
      ctx.fillStyle = P.aS; ctx.fill(); ctx.strokeStyle = P.a; ctx.lineWidth = 2; ctx.stroke();
      A.txt(ctx, 'total', 80, 305, { size: 13, w: 700, fill: P.a });
      A.txt(ctx, (total / 1e6).toFixed(1) + ' M parameters', 640, 305,
        { align: 'right', size: 15, mono: true, w: 700, fill: P.a });
      log.set('d=' + d + ' · L=' + L + ' · V=' + V + ' → ' + total.toLocaleString() + ' parameters',
        'total = V·d + ctx·d + L·(4d² + 8d² + 4d)');
      ro.set('At d = 768 and 12 layers this comes to <b>124.4 M</b> — and the published figure for ' +
        'GPT-2 small is 124 M.\nThe arithmetic is exact, and it is arithmetic you can now do.');
    }
    A.bind(c, render); render();
  });

})();
