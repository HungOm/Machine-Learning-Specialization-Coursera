/* Widgets for Course 4 / Week 2 — attention */
(function () {
  'use strict';

  /* shared: the hand-worked 3-token example used across the week */
  var Q3 = [[1, 0], [0, 1], [1, 1]];
  var K3 = [[1, 0], [0, 1], [1, 1]];
  var V3 = [[10, 0], [0, 10], [5, 5]];
  var TOK = ['tok 1', 'tok 2', 'tok 3'];

  function dot(a, b) { var s = 0; for (var i = 0; i < a.length; i++) s += a[i] * b[i]; return s; }
  function softmax(r) {
    var m = Math.max.apply(null, r);
    var e = r.map(function (v) { return Math.exp(v - m); });
    var s = e.reduce(function (a, b) { return a + b; }, 0);
    return e.map(function (v) { return v / s; });
  }
  function attnWeights(scale) {
    var dk = 2, out = [];
    for (var i = 0; i < 3; i++) {
      var row = [];
      for (var j = 0; j < 3; j++) row.push(dot(Q3[i], K3[j]) / (scale ? Math.sqrt(dk) : 1));
      out.push(softmax(row));
    }
    return out;
  }

  /* ============================================================
     1. The idea — every position looking at every other
     ============================================================ */
  A.def('c4-attn-idea', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var pick = 0;
    var bar = A.ctrls(root), ro = A.readout(root);
    TOK.forEach(function (t, i) { A.button(bar, 'from ' + t, function () { pick = i; sync(); render(); }); });
    function sync() { bar.querySelectorAll('button').forEach(function (b, i) { b.classList.toggle('primary', i === pick); }); }
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var W = attnWeights(true);
      A.txt(ctx, 'every position asks every position: how relevant are you to me?', 50, 40,
        { size: 12.5, w: 700, fill: P.soft });
      /* positions along the top */
      TOK.forEach(function (t, i) {
        var x = 150 + i * 180;
        A.rr(ctx, x, 60, 150, 44, 8);
        var on = i === pick;
        ctx.fillStyle = on ? P.aS : P.sunk; ctx.fill();
        ctx.strokeStyle = on ? P.a : P.lineSoft; ctx.lineWidth = on ? 2.2 : 1; ctx.stroke();
        A.txt(ctx, t, x + 75, 88, { align: 'center', size: 13, w: 700, fill: on ? P.a : P.soft });
      });
      /* arrows down to the sources, thickness = weight */
      var w = W[pick];
      TOK.forEach(function (t, j) {
        var x = 150 + j * 180 + 75, from = 150 + pick * 180 + 75;
        ctx.save(); ctx.globalAlpha = 0.25 + w[j];
        A.arrow(ctx, from, 106, x, 186, j === 0 ? P.b : j === 1 ? P.p : P.g, 1 + w[j] * 5);
        ctx.restore();
        A.txt(ctx, w[j].toFixed(4), x, 176, { align: 'center', size: 12, mono: true, w: 700,
          fill: j === 0 ? P.b : j === 1 ? P.p : P.g });
      });
      TOK.forEach(function (t, j) {
        var x = 150 + j * 180;
        A.rr(ctx, x, 192, 150, 40, 7);
        ctx.fillStyle = P.sunk; ctx.fill(); ctx.strokeStyle = P.lineSoft; ctx.stroke();
        A.txt(ctx, 'value ' + (j + 1), x + 75, 217, { align: 'center', size: 11.5, mono: true, fill: P.soft });
      });
      A.txt(ctx, 'weights sum to ' + w.reduce(function (a, b) { return a + b; }, 0).toFixed(4) +
        ' — which is what makes the result an average', 50, 266, { size: 12, w: 700, fill: P.g });
      A.txt(ctx, 'Score every pair, softmax into weights, take a weighted average. Both halves are',
        50, 294, { size: 12, fill: P.faint });
      A.txt(ctx, 'operations you have used since Course 2.', 50, 314, { size: 12, fill: P.faint });
      ro.set('Each row of the weight matrix is one position’s own recipe for mixing every other ' +
        'position.\nRows sum to 1; columns do not, and are not meant to.');
    }
    sync(); A.bind(c, render); render();
  });

  /* ============================================================
     2. Q, K, V — one input, three projections
     ============================================================ */
  A.def('c4-qkv', function (root) {
    var c = A.canvas(root, 760, 320), ctx = c.ctx;
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var lit = Math.floor((t * 0.6) % 3);
      A.matrix(ctx, 60, 96, 3, 2, 52, 42, P, function (i, j) { return ['a', 'b', 'c'][i] + (j + 1); },
        { state: function () { return 2; }, size: 12, label: 'X  (T × d)' });
      A.txt(ctx, 'the same input,', 60, 200, { size: 12, fill: P.faint });
      A.txt(ctx, 'three times', 60, 218, { size: 12, w: 700, fill: P.soft });
      var defs = [
        ['W', 'Q', 'what am I looking for?', P.a, 'Q'],
        ['W', 'K', 'what do I advertise?', P.b, 'K'],
        ['W', 'V', 'what do I hand over?', P.g, 'V']
      ];
      defs.forEach(function (d, i) {
        var y = 52 + i * 84, on = i === lit;
        A.arrow(ctx, 178, 130, 236, y + 24, on ? d[3] : P.line, on ? 2.4 : 1.2);
        A.rr(ctx, 244, y, 120, 48, 8);
        ctx.fillStyle = on ? (i === 0 ? P.aS : i === 1 ? P.bS : P.gS) : P.sunk; ctx.fill();
        ctx.strokeStyle = on ? d[3] : P.lineSoft; ctx.lineWidth = on ? 2.2 : 1; ctx.stroke();
        A.txt(ctx, d[0] + '₁'.replace('₁', ''), 0, 0, { size: 1 });
        A.txt(ctx, 'W' + d[1], 304, y + 30, { align: 'center', size: 17, w: 700,
          fill: on ? d[3] : P.faint });
        A.arrow(ctx, 370, y + 24, 424, y + 24, on ? d[3] : P.line, on ? 2.4 : 1.2);
        A.rr(ctx, 432, y, 90, 48, 8);
        ctx.fillStyle = on ? (i === 0 ? P.aS : i === 1 ? P.bS : P.gS) : P.sunk; ctx.fill();
        ctx.strokeStyle = on ? d[3] : P.lineSoft; ctx.lineWidth = on ? 2.2 : 1; ctx.stroke();
        A.txt(ctx, d[4], 477, y + 32, { align: 'center', size: 20, w: 700, fill: on ? d[3] : P.faint });
        A.txt(ctx, d[2], 540, y + 30, { size: 12, w: on ? 700 : 500, fill: on ? d[3] : P.faint });
      });
      A.txt(ctx, 'Three separate learned matrices. The model can represent “what I want” and',
        60, 268, { size: 12, fill: P.soft });
      A.txt(ctx, '“what I offer” as different things — and it learns to.', 60, 288,
        { size: 12, w: 700, fill: P.a });
      A.txt(ctx, 'Self-attention: all three come from the same sequence.', 60, 312,
        { size: 11.5, fill: P.faint });
    }
    A.autoplay(root, c, render);
  });

  /* ============================================================
     3. Attention by hand — the four steps
     ============================================================ */
  A.def('c4-attn-hand', function (root) {
    var c = A.canvas(root, 760, 340), ctx = c.ctx;
    var step = 0;
    var bar = A.ctrls(root), log = A.log(root), ro = A.readout(root);
    var NAMES = ['1 · score', '2 · scale', '3 · softmax', '4 · mix'];
    NAMES.forEach(function (n, i) { A.button(bar, n, function () { step = i; sync(); render(); }); });
    function sync() { bar.querySelectorAll('button').forEach(function (b, i) { b.classList.toggle('primary', i === step); }); }
    function raw(i, j) { return dot(Q3[i], K3[j]); }
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var dk = Math.sqrt(2), W = attnWeights(true);
      var get, label, note;
      if (step === 0) { get = function (i, j) { return raw(i, j).toFixed(0); }; label = 'QKᵀ  — every query · every key'; note = 'q₁·k₁ = [1,0]·[1,0] = 1'; }
      else if (step === 1) { get = function (i, j) { return (raw(i, j) / dk).toFixed(4); }; label = '÷ √dₖ = √2 = 1.4142'; note = '1 ÷ 1.4142 = 0.7071'; }
      else if (step === 2) { get = function (i, j) { return W[i][j].toFixed(4); }; label = 'softmax, each ROW independently'; note = 'e^0.7071 = 2.028, sum = 5.056 → 0.4011'; }
      else { get = null; label = ''; note = ''; }

      if (step < 3) {
        A.matrix(ctx, 220, 76, 3, 3, 96, 52, P, get,
          { state: function (i, j) { return step === 2 ? 3 : (i === j ? 1 : 0); }, size: 13, label: label });
        A.txt(ctx, 'rows = queries (who is asking)', 60, 108, { size: 11.5, fill: P.faint });
        A.txt(ctx, 'cols = keys (who is offering)', 60, 128, { size: 11.5, fill: P.faint });
        A.txt(ctx, note, 220, 268, { size: 12.5, mono: true, w: 700, fill: P.a });
        if (step === 2) {
          A.txt(ctx, 'every row sums to exactly 1.0000', 220, 292,
            { size: 12.5, w: 700, fill: P.g });
          A.txt(ctx, 'columns do not — and are not supposed to', 220, 312,
            { size: 11.5, fill: P.faint });
        }
      } else {
        var out = W.map(function (w) {
          return [0, 1].map(function (d) { return w[0] * V3[0][d] + w[1] * V3[1][d] + w[2] * V3[2][d]; });
        });
        A.matrix(ctx, 70, 90, 3, 3, 84, 50, P, function (i, j) { return W[i][j].toFixed(3); },
          { state: function () { return 3; }, size: 12, label: 'weights' });
        A.txt(ctx, '×', 340, 148, { align: 'center', size: 22, fill: P.faint });
        A.matrix(ctx, 372, 90, 3, 2, 66, 50, P, function (i, j) { return String(V3[i][j]); },
          { state: function () { return 2; }, size: 12, label: 'V' });
        A.txt(ctx, '=', 522, 148, { align: 'center', size: 22, fill: P.faint });
        A.matrix(ctx, 552, 90, 3, 2, 76, 50, P, function (i, j) { return out[i][j].toFixed(3); },
          { state: function () { return 1; }, size: 12, label: 'output' });
        A.txt(ctx, 'row 1:  0.4011×10 + 0.1978×0 + 0.4011×5 = 6.017', 70, 274,
          { size: 12.5, mono: true, w: 700, fill: P.a });
        A.txt(ctx, 'Each output row is that position’s weighted average of every value.', 70, 300,
          { size: 12, fill: P.faint });
        A.txt(ctx, 'Same number of rows in as out — which is why attention layers stack.', 70, 322,
          { size: 12, w: 700, fill: P.g });
      }
      log.set('step ' + (step + 1) + ' of 4 · ' + NAMES[step].split('· ')[1] +
        (step === 2 ? '  — row sums: 1.0000, 1.0000, 1.0000' : ''),
        'Attention(Q,K,V) = softmax(QKᵀ / √dₖ) V');
      ro.set('Three tokens, dₖ = 2, every number checkable with a calculator.\n' +
        'Do this once on paper and the mechanism stops being mysterious.');
    }
    sync(); A.bind(c, render); render();
  });

  /* ============================================================
     4. Self-attention — what does "it" refer to?
     ============================================================ */
  A.def('c4-selfattn', function (root) {
    var c = A.canvas(root, 760, 300), ctx = c.ctx;
    var alt = 0;
    var WORDS = ['the', 'animal', 'did not', 'cross', 'the', 'street', 'because', 'it', 'was', 'too'];
    var ENDS = ['tired', 'wide'];
    var FOCUS = [1, 5];    /* tired -> animal, wide -> street */
    var bar = A.ctrls(root), ro = A.readout(root);
    ENDS.forEach(function (e, i) { A.button(bar, '…too ' + e, function () { alt = i; sync(); render(); }); });
    function sync() { bar.querySelectorAll('button').forEach(function (b, i) { b.classList.toggle('primary', i === alt); }); }
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var all = WORDS.concat([ENDS[alt]]);
      var itIdx = 7, tgt = FOCUS[alt];
      A.txt(ctx, 'which word does “it” attend to?', 50, 42, { size: 12.5, w: 700, fill: P.soft });
      var x = 50;
      var pos = [];
      all.forEach(function (w, i) {
        var wd = Math.max(46, w.length * 9 + 22);
        var on = i === itIdx, target = i === tgt;
        A.rr(ctx, x, 62, wd, 40, 6);
        ctx.fillStyle = on ? P.aS : target ? P.gS : P.sunk; ctx.fill();
        ctx.strokeStyle = on ? P.a : target ? P.g : P.lineSoft;
        ctx.lineWidth = (on || target) ? 2.2 : 1; ctx.stroke();
        A.txt(ctx, w, x + wd / 2, 87, { align: 'center', size: 12, w: (on || target) ? 700 : 500,
          fill: on ? P.a : target ? P.g : P.soft });
        pos.push(x + wd / 2);
        x += wd + 6;
      });
      /* the attention arc from "it" to its referent */
      ctx.save(); ctx.strokeStyle = P.a; ctx.lineWidth = 2.6;
      ctx.beginPath(); ctx.moveTo(pos[itIdx], 106);
      ctx.quadraticCurveTo((pos[itIdx] + pos[tgt]) / 2, 178, pos[tgt], 106);
      ctx.stroke(); ctx.restore();
      A.dot(ctx, pos[tgt], 106, 4.5, P.g);
      A.txt(ctx, 'strong attention', (pos[itIdx] + pos[tgt]) / 2, 196,
        { align: 'center', size: 11.5, w: 700, fill: P.a });
      A.txt(ctx, 'Only the last word changed. The sentence structure is identical — and the',
        50, 236, { size: 12, fill: P.soft });
      A.txt(ctx, 'referent of “it” moved from “' + ['animal', 'street'][alt] +
        '” because of what is plausible, not what is grammatical.', 50, 256,
        { size: 12, w: 700, fill: P.a });
      A.txt(ctx, 'This is the classic Winograd example — designed to need world knowledge.',
        50, 284, { size: 11.5, fill: P.faint });
      ro.set('Self-attention does not <em>solve</em> coreference; it is the mechanism that lets ' +
        'knowledge be applied to the right pair of words.\nSome trained heads do this systematically ' +
        'without ever being asked to.');
    }
    sync(); A.bind(c, render); render();
  });

  /* ============================================================
     5. Why scale by root d
     ============================================================ */
  A.def('c4-scale', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var dk = 64, scaled = true;
    var bar = A.ctrls(root), log = A.log(root), ro = A.readout(root);
    A.slider(bar, { label: 'dₖ', min: 2, max: 512, step: 2, value: dk,
      fmt: function (v) { return v.toFixed(0); }, on: function (v) { dk = v; render(); } });
    A.toggle(bar, 'divide by √dₖ', function (v) { scaled = v; render(); }, true);
    function render() {
      var P = A.pal(); c.clear(P.panel);
      /* typical score spread grows as sqrt(dk) */
      var spread = Math.sqrt(dk);
      var s = scaled ? [1, 0, -0.4] : [spread, 0, -0.4 * spread];
      var w = softmax(s);
      A.txt(ctx, 'three typical scores at dₖ = ' + dk.toFixed(0) +
        (scaled ? ', after scaling' : ', unscaled'), 50, 42, { size: 12.5, w: 700, fill: P.soft });
      s.forEach(function (v, i) {
        var y = 62 + i * 34;
        A.txt(ctx, 'score ' + (i + 1), 110, y + 20, { align: 'right', size: 12, fill: P.faint });
        var len = A.clamp(Math.abs(v) * 12, 2, 380);
        A.rr(ctx, 122, y, len, 24, 4);
        ctx.fillStyle = v >= 0 ? P.bS : P.rS; ctx.fill();
        ctx.strokeStyle = v >= 0 ? P.b : P.r; ctx.stroke();
        A.txt(ctx, v.toFixed(2), 130 + len, y + 17, { size: 12, mono: true, fill: P.soft });
      });
      A.txt(ctx, 'after softmax', 50, 194, { size: 12.5, w: 700, fill: P.soft });
      w.forEach(function (v, i) {
        var y = 208 + i * 30;
        A.rr(ctx, 122, y, Math.max(2, v * 380), 22, 4);
        ctx.fillStyle = P.aS; ctx.fill(); ctx.strokeStyle = P.a; ctx.stroke();
        A.txt(ctx, v.toFixed(4), 130 + Math.max(2, v * 380), y + 16,
          { size: 12, mono: true, w: 700, fill: P.a });
      });
      var mx = Math.max.apply(null, w);
      A.txt(ctx, mx > 0.99 ? 'saturated — gradient through this softmax is ~0, so it cannot learn'
                           : 'soft — there is still gradient to learn from',
        50, 312, { size: 12.5, w: 700, fill: mx > 0.99 ? P.r : P.g });
      log.set('dₖ = ' + dk.toFixed(0) + '  ·  √dₖ = ' + spread.toFixed(3) +
        '  ·  largest weight = ' + mx.toFixed(4) + (scaled ? '  (scaled)' : '  (UNSCALED)'),
        'std of q·k ≈ √dₖ when components are unit-variance — so divide by exactly that');
      ro.set('Measured: at dₖ = 512 the spread of an unscaled dot product is about <b>22.6</b>, ' +
        'and √512 = 22.63.\nThe theory is exact, and the fix is to divide by it.');
    }
    A.bind(c, render); render();
  });

  /* ============================================================
     6. Multi-head
     ============================================================ */
  A.def('c4-multihead', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var WORDS = ['the', 'tired', 'cat', 'sat', 'down'];
    /* three plausible, deliberately different patterns */
    var HEADS = [
      { n: 'head 1 — adjective → noun', col: 'b', w: [0, 0, 1, 0, 0] },
      { n: 'head 2 — subject → verb', col: 'p', w: [0, 0, 0, 1, 0] },
      { n: 'head 3 — previous token', col: 'g', w: [0, 1, 0, 0, 0] }
    ];
    var from = 1;
    var bar = A.ctrls(root), ro = A.readout(root);
    A.slider(bar, { label: 'attending from', min: 0, max: 4, step: 1, value: 1,
      fmt: function (v) { return WORDS[v]; }, on: function (v) { from = v; render(); } });
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var cols = { b: P.b, p: P.p, g: P.g };
      A.txt(ctx, 'three heads, same sentence, different relationships', 50, 40,
        { size: 12.5, w: 700, fill: P.soft });
      HEADS.forEach(function (h, k) {
        var y = 60 + k * 84;
        A.txt(ctx, h.n, 50, y + 14, { size: 11.5, w: 700, fill: cols[h.col] });
        WORDS.forEach(function (w, i) {
          var x = 50 + i * 132;
          /* shift the pattern relative to the source position */
          var tgt = A.clamp(from + (k === 0 ? 1 : k === 1 ? 2 : -1), 0, 4);
          var on = i === tgt, src = i === from;
          A.rr(ctx, x, y + 24, 122, 38, 6);
          ctx.fillStyle = src ? P.aS : on ? (k === 0 ? P.bS : k === 1 ? P.pS : P.gS) : P.sunk;
          ctx.fill();
          ctx.strokeStyle = src ? P.a : on ? cols[h.col] : P.lineSoft;
          ctx.lineWidth = (src || on) ? 2 : 1; ctx.stroke();
          A.txt(ctx, w, x + 61, y + 48, { align: 'center', size: 12, w: (src || on) ? 700 : 500,
            fill: src ? P.a : on ? cols[h.col] : P.soft });
        });
      });
      A.txt(ctx, 'Each head has its own W_Q, W_K, W_V — so each can chase a different kind of link.',
        50, 320, { size: 12, w: 700, fill: P.a });
      ro.set('8 heads of size 64 costs the <b>same</b> parameters as 1 head of size 512 — the ' +
        'budget is redistributed, not increased.\nWₒ at the end is what lets the heads’ ' +
        'outputs actually mix.');
    }
    A.bind(c, render); render();
  });

  /* ============================================================
     7. Masking
     ============================================================ */
  A.def('c4-mask', function (root) {
    var c = A.canvas(root, 760, 320), ctx = c.ctx;
    var masked = true;
    var bar = A.ctrls(root), ro = A.readout(root);
    A.toggle(bar, 'causal mask', function (v) { masked = v; render(); }, true);
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var N = 5;
      A.txt(ctx, masked ? 'masked — no position can see the future'
                        : 'unmasked — every position sees everything',
        50, 42, { size: 13, w: 700, fill: masked ? P.g : P.b });
      A.matrix(ctx, 150, 76, N, N, 78, 40, P, function (i, j) {
        if (masked && j > i) return '0';
        return (1 / (masked ? (i + 1) : N)).toFixed(2);
      }, { state: function (i, j) { return (masked && j > i) ? 4 : 3; }, size: 12,
           label: 'attention weights' });
      A.txt(ctx, 'row = position asking', 50, 128, { size: 11.5, fill: P.faint });
      A.txt(ctx, 'col = position offered', 50, 148, { size: 11.5, fill: P.faint });
      A.txt(ctx, masked
        ? 'Row 1 sees only itself. Row 5 sees all five. The staircase edge is “now”.'
        : 'Every row sees every column — including words that have not been written yet.',
        50, 296, { size: 12, w: 700, fill: masked ? P.g : P.r });
      A.txt(ctx, 'Set to −∞ BEFORE the softmax, so e^(−∞) = 0 removes them exactly.',
        50, 274, { size: 12, fill: P.faint });
      ro.set('Masked (GPT-style) → can generate text one token at a time.\n' +
        'Unmasked (BERT-style) → better at understanding a whole sentence, cannot generate.\n' +
        'One triangle of −∞ is the entire difference.');
    }
    A.bind(c, render); render();
  });

  /* ============================================================
     8. The quadratic cost
     ============================================================ */
  A.def('c4-cost', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var T = 100;
    var bar = A.ctrls(root), log = A.log(root), ro = A.readout(root);
    A.slider(bar, { label: 'sequence length T', min: 10, max: 4000, step: 10, value: T,
      fmt: function (v) { return v.toFixed(0); }, on: function (v) { T = v; render(); } });
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var box = { x: 70, y: 40, w: 380, h: 210 };
      var S = A.axes(ctx, box, [0, 4000], [0, 16], {
        xticks: 4, yticks: 4,
        xfmt: function (v) { return (v / 1000).toFixed(1) + 'k'; },
        yfmt: function (v) { return '1e' + v.toFixed(0); },
        xlab: 'sequence length', ylab: 'work'
      });
      A.plot(ctx, S, [10, 4000], function (x) { return Math.log10(x * x); }, P.r, 2.6);
      A.plot(ctx, S, [10, 4000], function (x) { return Math.log10(x); }, P.g, 2.2, [5, 4]);
      A.txt(ctx, 'attention  O(T²)', S.X(2200), S.Y(Math.log10(2200 * 2200)) - 12,
        { size: 11.5, w: 700, fill: P.r });
      A.txt(ctx, 'RNN  O(T)', S.X(2400), S.Y(Math.log10(2400)) + 18, { size: 11.5, w: 700, fill: P.g });
      A.dot(ctx, S.X(T), S.Y(Math.log10(T * T)), 6, P.a);
      /* the growing square */
      var side = A.clamp(Math.sqrt(T) * 3.1, 20, 160);
      A.rr(ctx, 560, 150 - side / 2, side, side, 5);
      ctx.fillStyle = P.aS; ctx.fill(); ctx.strokeStyle = P.a; ctx.lineWidth = 2; ctx.stroke();
      A.txt(ctx, 'T × T', 560 + side / 2, 154, { align: 'center', size: 12, w: 700, fill: P.a });
      A.txt(ctx, 'the score matrix', 560 + side / 2, 150 + side / 2 + 22,
        { align: 'center', size: 11, fill: P.faint });
      A.txt(ctx, 'Doubling the input quadruples the work. Not doubles — quadruples.',
        70, 290, { size: 12.5, w: 700, fill: P.a });
      A.txt(ctx, 'And that is per layer, per head.', 70, 312, { size: 11.5, fill: P.faint });
      log.set('T = ' + T.toFixed(0) + '  →  ' + (T * T).toLocaleString() +
        ' pairwise scores per head per layer', 'cost ∝ T² in both time and memory');
      ro.set('This is the price of one-step paths between any two positions.\n' +
        'It is why context windows are a headline number, and why making attention cheaper is an ' +
        'entire research subfield.');
    }
    A.bind(c, render); render();
  });

})();
