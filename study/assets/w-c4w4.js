/* Widgets for Course 4 / Week 4 — from transformer to language model */
(function () {
  'use strict';

  function softmax(a) {
    var m = Math.max.apply(null, a);
    var e = a.map(function (v) { return Math.exp(v - m); });
    var s = e.reduce(function (x, y) { return x + y; }, 0);
    return e.map(function (v) { return v / s; });
  }

  /* ============================================================
     1. Next-token prediction
     ============================================================ */
  A.def('c4-nexttoken', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var CTXT = ['the', 'capital', 'of', 'France', 'is'];
    var CAND = ['Paris', 'the', 'a', 'Lyon'];
    var LOGITS = [6.0, 2.0, 1.5, 1.0];
    var step = 0;
    var bar = A.ctrls(root), log = A.log(root), ro = A.readout(root);
    ['1 · read', '2 · predict', '3 · compare', '4 · adjust'].forEach(function (n, i) {
      A.button(bar, n, function () { step = i; sync(); render(); });
    });
    function sync() { bar.querySelectorAll('button').forEach(function (b, i) { b.classList.toggle('primary', i === step); }); }
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var p = softmax(LOGITS);
      A.txt(ctx, 'context (masked — the model cannot see what comes next)', 50, 40,
        { size: 12, fill: P.faint });
      CTXT.forEach(function (w, i) {
        var x = 50 + i * 116;
        A.rr(ctx, x, 54, 106, 38, 6);
        ctx.fillStyle = P.sunk; ctx.fill(); ctx.strokeStyle = P.lineSoft; ctx.stroke();
        A.txt(ctx, w, x + 53, 78, { align: 'center', size: 12.5, mono: true, fill: P.soft });
      });
      A.rr(ctx, 50 + 5 * 116, 54, 106, 38, 6);
      ctx.fillStyle = step >= 1 ? P.aS : P.panel; ctx.fill();
      ctx.strokeStyle = P.a; ctx.lineWidth = 2; ctx.setLineDash([4, 3]); ctx.stroke();
      ctx.setLineDash([]);
      A.txt(ctx, step >= 1 ? '?' : '', 50 + 5 * 116 + 53, 80,
        { align: 'center', size: 18, w: 700, fill: P.a });

      if (step >= 1) {
        A.txt(ctx, 'the model’s distribution over 50,257 tokens (top 4 shown)', 50, 126,
          { size: 12, fill: P.faint });
        CAND.forEach(function (t, i) {
          var y = 140 + i * 34;
          var right = (i === 0);
          A.txt(ctx, t, 130, y + 20, { align: 'right', size: 12.5, mono: true,
            fill: (step >= 2 && right) ? P.g : P.soft });
          A.rr(ctx, 142, y, Math.max(4, p[i] * 440), 24, 4);
          ctx.fillStyle = (step >= 2 && right) ? P.gS : P.aS; ctx.fill();
          ctx.strokeStyle = (step >= 2 && right) ? P.g : P.a; ctx.stroke();
          A.txt(ctx, p[i].toFixed(4), 150 + Math.max(4, p[i] * 440), y + 17,
            { size: 11.5, mono: true, fill: P.soft });
          if (step >= 2 && right) A.txt(ctx, '← the token that actually came next', 400, y + 17,
            { size: 11.5, w: 700, fill: P.g });
        });
      }
      if (step >= 2) {
        var loss = -Math.log(p[0]);
        A.txt(ctx, 'loss = −log(' + p[0].toFixed(4) + ') = ' + loss.toFixed(4), 50, 296,
          { size: 13, mono: true, w: 700, fill: P.a });
        A.txt(ctx, step >= 3 ? 'backpropagate, update every weight, move to the next position'
                             : 'the same cross-entropy loss as C2 W2', 50, 320,
          { size: 12, fill: step >= 3 ? P.g : P.faint });
        log.set('p(correct) = ' + p[0].toFixed(4) + '  ·  loss = ' + loss.toFixed(4) +
          '  ·  perplexity = ' + Math.exp(loss).toFixed(2),
          'L = −Σ log P(x_t | x_<t)   — cross-entropy, exactly as in C2 W2');
      }
      ro.set('Every position in the sequence produces a loss term simultaneously.\n' +
        'A 1,000-token document supplies 1,000 training signals in one forward pass.');
    }
    sync(); A.bind(c, render); render();
  });

  /* ============================================================
     2. Generation and temperature
     ============================================================ */
  A.def('c4-generate', function (root) {
    var c = A.canvas(root, 760, 320), ctx = c.ctx;
    var T = 1.0;
    var LOG = [3.0, 2.0, 1.0, 0.5];
    var TOK = ['cat', 'dog', 'car', 'the'];
    var bar = A.ctrls(root), log = A.log(root), ro = A.readout(root);
    A.slider(bar, { label: 'temperature', min: 0.1, max: 2.0, step: .1, value: T,
      fmt: function (v) { return v.toFixed(1); }, on: function (v) { T = v; render(); } });
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var p = softmax(LOG.map(function (v) { return v / T; }));
      A.txt(ctx, 'the model produced ONE set of scores. Everything below happens afterwards.',
        50, 40, { size: 12.5, w: 700, fill: P.soft });
      A.txt(ctx, 'raw scores (logits)', 50, 70, { size: 11.5, fill: P.faint });
      LOG.forEach(function (v, i) {
        var x = 50 + i * 172;
        A.rr(ctx, x, 80, 160, 30, 5);
        ctx.fillStyle = P.sunk; ctx.fill(); ctx.strokeStyle = P.lineSoft; ctx.stroke();
        A.txt(ctx, TOK[i] + '  ' + v.toFixed(1), x + 80, 101,
          { align: 'center', size: 12, mono: true, fill: P.soft });
      });
      A.txt(ctx, 'after dividing by T = ' + T.toFixed(1) + ' and softmaxing', 50, 148,
        { size: 12.5, w: 700, fill: P.a });
      p.forEach(function (v, i) {
        var y = 160 + i * 32;
        A.txt(ctx, TOK[i], 108, y + 20, { align: 'right', size: 12.5, mono: true, fill: P.soft });
        A.rr(ctx, 120, y, Math.max(4, v * 460), 24, 4);
        ctx.fillStyle = P.aS; ctx.fill(); ctx.strokeStyle = P.a; ctx.stroke();
        A.txt(ctx, v.toFixed(4), 128 + Math.max(4, v * 460), y + 17,
          { size: 11.5, mono: true, w: 700, fill: P.a });
      });
      var verdict = T <= 0.3 ? ['deterministic — the same output every time', P.b]
        : T <= 0.8 ? ['focused', P.g]
        : T <= 1.2 ? ['the model’s honest distribution', P.g]
        : ['flattened — reaching for options it thinks are unlikely', P.r];
      A.txt(ctx, verdict[0], 50, 308, { size: 12.5, w: 700, fill: verdict[1] });
      log.set('T = ' + T.toFixed(1) + '  ·  top token ' + (p[0] * 100).toFixed(1) + '%  ·  ' +
        'entropy ' + (-p.reduce(function (a, v) { return a + (v > 0 ? v * Math.log(v) : 0); }, 0)).toFixed(3),
        'p = softmax(logits / T)   — T divides BEFORE the softmax, not after');
      ro.set('Not one weight of the model changes with temperature.\n' +
        'Two systems running identical weights at different temperatures behave very differently.');
    }
    A.bind(c, render); render();
  });

  /* ============================================================
     3. Scale
     ============================================================ */
  A.def('c4-scale-story', function (root) {
    var c = A.canvas(root, 760, 320), ctx = c.ctx;
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var lit = Math.floor((t * 0.45) % 3);
      var models = [
        ['GPT-1  2018', '117 M', '12 layers · d 768', 40, P.b],
        ['GPT-2  2019', '1.5 B', '48 layers · d 1600', 90, P.p],
        ['GPT-3  2020', '175 B', '96 layers · d 12288', 170, P.a]
      ];
      models.forEach(function (m, i) {
        var x = 80 + i * 220, on = i === lit, h = m[3];
        A.rr(ctx, x, 210 - h, 170, h, 8);
        ctx.fillStyle = on ? P.aS : P.sunk; ctx.fill();
        ctx.strokeStyle = on ? P.a : P.lineSoft; ctx.lineWidth = on ? 2.4 : 1.2; ctx.stroke();
        A.txt(ctx, m[1], x + 85, 210 - h / 2 + 6, { align: 'center', size: 17, w: 700,
          fill: on ? P.a : P.soft });
        A.txt(ctx, m[0], x + 85, 232, { align: 'center', size: 12, w: 700, fill: on ? P.a : P.faint });
        A.txt(ctx, m[2], x + 85, 250, { align: 'center', size: 10.5, fill: P.faint });
      });
      A.txt(ctx, 'the architecture, across all three:', 80, 42, { size: 12.5, fill: P.faint });
      A.rr(ctx, 80, 54, 610, 34, 7);
      ctx.fillStyle = P.gS; ctx.fill(); ctx.strokeStyle = P.g; ctx.lineWidth = 1.8; ctx.stroke();
      A.txt(ctx, 'transformer decoder — unchanged', 385, 76,
        { align: 'center', size: 13, w: 700, fill: P.g });
      A.txt(ctx, 'A factor of about 1,500 in parameters, and the block you drew in Week 3 is',
        80, 284, { size: 12, fill: P.soft });
      A.txt(ctx, 'still the block. That is the uncomfortable finding.', 80, 304,
        { size: 12, w: 700, fill: P.a });
    }
    A.autoplay(root, c, render);
  });

  /* ============================================================
     4. RLHF
     ============================================================ */
  A.def('c4-rlhf', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var step = Math.floor((t * 0.4) % 3);
      var stages = [
        ['1 · pretraining', 'hundreds of billions of tokens', 'language, facts, reasoning', 'months of compute', P.b],
        ['2 · supervised fine-tuning', 'tens of thousands of written answers', 'the FORMAT of a helpful reply', 'modest', P.p],
        ['3 · RLHF', 'humans ranking pairs of answers', 'what people actually prefer, and what to decline', 'modest', P.a]
      ];
      stages.forEach(function (s, i) {
        var y = 50 + i * 88, on = i === step;
        A.rr(ctx, 50, y, 650, 74, 9);
        ctx.fillStyle = on ? P.aS : P.sunk; ctx.fill();
        ctx.strokeStyle = on ? P.a : P.lineSoft; ctx.lineWidth = on ? 2.4 : 1; ctx.stroke();
        A.txt(ctx, s[0], 70, y + 24, { size: 13.5, w: 700, fill: on ? P.a : s[4] });
        A.txt(ctx, 'data: ' + s[1], 70, y + 44, { size: 11.5, fill: P.faint });
        A.txt(ctx, 'teaches: ' + s[2], 70, y + 62, { size: 11.5, fill: on ? P.a : P.soft });
        A.txt(ctx, s[3], 682, y + 24, { align: 'right', size: 11, mono: true, fill: P.faint });
        if (i < 2) A.arrow(ctx, 375, y + 75, 375, y + 87, P.line, 1.6);
      });
      A.txt(ctx, 'Stage 1 is where the capability comes from. Stages 2 and 3 are where the',
        50, 306, { size: 12, fill: P.soft });
      A.txt(ctx, 'BEHAVIOUR comes from — and they are cheap by comparison.', 50, 324,
        { size: 12, w: 700, fill: P.a });
    }
    A.autoplay(root, c, render);
  });

  /* ============================================================
     5. Context and the KV cache
     ============================================================ */
  A.def('c4-context', function (root) {
    var c = A.canvas(root, 760, 320), ctx = c.ctx;
    var T = 8192;
    var bar = A.ctrls(root), log = A.log(root), ro = A.readout(root);
    A.slider(bar, { label: 'context tokens', min: 1024, max: 128000, step: 1024, value: T,
      fmt: function (v) { return v >= 1000 ? (v / 1000).toFixed(0) + 'k' : v.toFixed(0); },
      on: function (v) { T = v; render(); } });
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var L = 12, d = 768;
      var cache = 2 * L * d * T * 2;          /* K and V, fp16 */
      var comps = T * T;
      var box = { x: 70, y: 40, w: 300, h: 180 };
      var S = A.axes(ctx, box, [0, 128000], [0, 11], {
        xticks: 4, yticks: 4,
        xfmt: function (v) { return (v / 1000).toFixed(0) + 'k'; },
        yfmt: function (v) { return '1e' + v.toFixed(0); },
        xlab: 'context length', ylab: 'attention work'
      });
      A.plot(ctx, S, [1024, 128000], function (x) { return Math.log10(x * x); }, P.r, 2.6);
      A.dot(ctx, S.X(T), S.Y(Math.log10(comps)), 6, P.a);
      A.txt(ctx, 'attention  O(T²)', S.X(40000), S.Y(Math.log10(40000 * 40000)) - 12,
        { size: 11.5, w: 700, fill: P.r });
      /* the cache bar */
      A.txt(ctx, 'KV cache (GPT-2 small, fp16)', 420, 58, { size: 12.5, w: 700, fill: P.soft });
      var frac = cache / (2 * L * d * 128000 * 2);
      A.rr(ctx, 420, 74, 280, 30, 5);
      ctx.fillStyle = P.sunk; ctx.fill(); ctx.strokeStyle = P.lineSoft; ctx.stroke();
      A.rr(ctx, 420, 74, Math.max(4, 280 * frac), 30, 5);
      ctx.fillStyle = P.aS; ctx.fill(); ctx.strokeStyle = P.a; ctx.lineWidth = 1.8; ctx.stroke();
      A.txt(ctx, (cache / 1e6).toFixed(0) + ' MB per sequence', 560, 95,
        { align: 'center', size: 13, mono: true, w: 700, fill: P.a });
      A.txt(ctx, 'grows LINEARLY with context —', 420, 132, { size: 11.5, fill: P.faint });
      A.txt(ctx, 'and is usually what limits how many', 420, 150, { size: 11.5, fill: P.faint });
      A.txt(ctx, 'users one machine can serve.', 420, 168, { size: 11.5, fill: P.faint });
      A.txt(ctx, 'Two different costs: compute grows with T², memory with T.', 70, 254,
        { size: 12.5, w: 700, fill: P.a });
      A.txt(ctx, 'Anything outside the window does not exist. There is no memory beyond it.',
        70, 280, { size: 12, fill: P.faint });
      A.txt(ctx, 'For a 124M-parameter model, a 128k cache is larger than the model itself.',
        70, 304, { size: 11.5, fill: P.faint });
      log.set('T = ' + T.toLocaleString() + '  ·  ' + comps.toExponential(2) +
        ' attention comparisons  ·  KV cache ' + (cache / 1e6).toFixed(0) + ' MB',
        'compute ∝ T²   ·   KV cache = 2 · layers · d · T · bytes');
      ro.set('The cache exists so generation does not recompute every previous token’s keys and ' +
        'values at every step.\nWithout it generation would be cubic in length rather than quadratic.');
    }
    A.bind(c, render); render();
  });

  /* ============================================================
     6. What it cannot do
     ============================================================ */
  A.def('c4-limits', function (root) {
    var c = A.canvas(root, 760, 340), ctx = c.ctx;
    var pick = 0;
    var ITEMS = [
      ['hallucination', 'the objective rewards LIKELY continuations — nothing ever distinguished true from plausible', 'W4 L1'],
      ['no “I don’t know”', 'the softmax always produces a confident distribution; there is no abstain token', 'C2 W2'],
      ['arithmetic on odd numbers', 'learned as token patterns, not as an algorithm', 'W4 L1'],
      ['counting letters', 'the model receives subword chunks — it never sees letters', 'W1 L2'],
      ['forgetting the conversation', 'anything outside the context window does not exist', 'W4 L5']
    ];
    var bar = A.ctrls(root), ro = A.readout(root);
    ITEMS.forEach(function (it, i) { A.button(bar, it[0], function () { pick = i; sync(); render(); }); });
    function sync() { bar.querySelectorAll('button').forEach(function (b, i) { b.classList.toggle('primary', i === pick); }); }
    function render() {
      var P = A.pal(); c.clear(P.panel);
      A.txt(ctx, 'every failure below follows from a mechanism you already know', 50, 42,
        { size: 12.5, w: 700, fill: P.soft });
      ITEMS.forEach(function (it, i) {
        var y = 60 + i * 46, on = i === pick;
        A.rr(ctx, 50, y, 650, 38, 7);
        ctx.fillStyle = on ? P.rS : P.sunk; ctx.fill();
        ctx.strokeStyle = on ? P.r : P.lineSoft; ctx.lineWidth = on ? 2.2 : 1; ctx.stroke();
        A.txt(ctx, it[0], 70, y + 24, { size: 12.5, w: 700, fill: on ? P.r : P.soft });
        A.txt(ctx, it[2], 682, y + 24, { align: 'right', size: 10.5, mono: true, fill: P.faint });
      });
      A.rr(ctx, 50, 296, 650, 32, 6);
      ctx.fillStyle = P.aS; ctx.fill(); ctx.strokeStyle = P.a; ctx.lineWidth = 1.8; ctx.stroke();
      A.txt(ctx, ITEMS[pick][1], 66, 317, { size: 11.5, w: 700, fill: P.a });
      ro.set('Knowing <b>where</b> a system fails, and why, is as much a mark of understanding as ' +
        'knowing what it can do.\nScale reduces several of these and removes none.');
    }
    sync(); A.bind(c, render); render();
  });

  /* ============================================================
     7. The roadmap
     ============================================================ */
  A.def('c4-roadmap', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var lit = Math.floor((t * 0.4) % 5);
      var path = [
        ['Foundations', 'a function; a derivative', P.faint],
        ['Course 1', 'model + cost + gradient descent', P.b],
        ['Course 2', 'stack it; diagnose it', P.p],
        ['Course 3', 'no labels; learn from reward', P.g],
        ['Course 4', 'every position reads every other', P.a]
      ];
      path.forEach(function (p, i) {
        var y = 46 + i * 46, on = i === lit;
        A.rr(ctx, 50, y, 400, 38, 7);
        ctx.fillStyle = on ? P.aS : P.sunk; ctx.fill();
        ctx.strokeStyle = on ? P.a : P.lineSoft; ctx.lineWidth = on ? 2.2 : 1; ctx.stroke();
        A.txt(ctx, p[0], 68, y + 24, { size: 12.5, w: 700, fill: on ? P.a : p[2] });
        A.txt(ctx, p[1], 175, y + 24, { size: 11.5, fill: P.faint });
        if (i < 4) A.arrow(ctx, 250, y + 39, 250, y + 45, P.line, 1.4);
      });
      var next = ['CNNs and vision', 'training at scale', 'RAG, agents, fine-tuning',
                  'eigenvectors, MLE, matrix calculus', 'interpretability and safety'];
      A.txt(ctx, 'roads leading out', 480, 40, { size: 12.5, w: 700, fill: P.soft });
      next.forEach(function (n, i) {
        A.txt(ctx, '· ' + n, 480, 66 + i * 24, { size: 11.5, fill: P.faint });
      });
      A.txt(ctx, 'Every course is model + cost + optimiser. Course 4 changed only the model —',
        50, 296, { size: 12, fill: P.soft });
      A.txt(ctx, 'the cost is still cross-entropy and the optimiser is still Adam.', 50, 316,
        { size: 12, w: 700, fill: P.a });
    }
    A.autoplay(root, c, render);
  });

})();
