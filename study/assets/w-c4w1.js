/* Widgets for Course 4 / Week 1 — sequences, embeddings, and the old answers */
(function () {
  'use strict';

  /* ============================================================
     1. Order matters — the same words, two meanings
     ============================================================ */
  A.def('c4-orderbag', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var which = 0;
    var S = [['the', 'dog', 'bit', 'the', 'man'], ['the', 'man', 'bit', 'the', 'dog']];
    var bar = A.ctrls(root), ro = A.readout(root);
    A.button(bar, 'the dog bit the man', function () { which = 0; sync(); render(); });
    A.button(bar, 'the man bit the dog', function () { which = 1; sync(); render(); });
    function sync() {
      bar.querySelectorAll('button').forEach(function (b, i) { b.classList.toggle('primary', i === which); });
    }
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var words = S[which];
      A.txt(ctx, 'the sentence, in order', 60, 44, { size: 12.5, w: 700, fill: P.a });
      words.forEach(function (w, i) {
        var x = 60 + i * 128;
        A.rr(ctx, x, 56, 118, 44, 8);
        ctx.fillStyle = P.aS; ctx.fill(); ctx.strokeStyle = P.a; ctx.lineWidth = 1.8; ctx.stroke();
        A.txt(ctx, w, x + 59, 84, { align: 'center', size: 15, w: 700, fill: P.a });
        A.txt(ctx, 'position ' + (i + 1), x + 59, 116, { align: 'center', size: 10, fill: P.faint });
        if (i < 4) A.arrow(ctx, x + 120, 78, x + 126, 78, P.line, 1.6);
      });
      /* the bag — sorted counts, identical for both */
      A.txt(ctx, 'what a bag-of-words model receives', 60, 168, { size: 12.5, w: 700, fill: P.soft });
      var counts = {};
      words.forEach(function (w) { counts[w] = (counts[w] || 0) + 1; });
      Object.keys(counts).sort().forEach(function (w, i) {
        var x = 60 + i * 150;
        A.rr(ctx, x, 180, 140, 44, 8);
        ctx.fillStyle = P.sunk; ctx.fill(); ctx.strokeStyle = P.lineSoft; ctx.stroke();
        A.txt(ctx, w + ' × ' + counts[w], x + 70, 208, { align: 'center', size: 14, mono: true, fill: P.soft });
      });
      A.txt(ctx, 'Both sentences produce this identical bag. To a model that only counts words they',
        60, 262, { size: 12.5, fill: P.soft });
      A.txt(ctx, 'are not merely similar — they are the SAME input, and it can never tell them apart.',
        60, 282, { size: 12.5, w: 700, fill: P.r });
      A.txt(ctx, 'Order is not extra detail here. It is the entire difference in meaning.',
        60, 312, { size: 12, fill: P.faint });
      ro.set('Everything in Courses 1–3 treated an example as an unordered set of features.\n' +
        'A sequence is not a set — and every mechanism in this course exists to put position back in.');
    }
    sync(); A.bind(c, render); render();
  });

  /* ============================================================
     2. Tokens — three ways to cut one word
     ============================================================ */
  A.def('c4-tokens', function (root) {
    var c = A.canvas(root, 760, 340), ctx = c.ctx;
    var mode = 2;
    var WORD = 'unbelievable';
    var CUTS = [
      WORD.split(''),
      [WORD],
      ['un', 'bel', 'ievable']
    ];
    var META = [
      ['characters', '~100', 'every sequence becomes very long, and one letter means almost nothing'],
      ['whole words', 'millions, still incomplete', 'any word never seen in training cannot be represented at all'],
      ['subword (BPE)', '~30,000–100,000', 'the working compromise — single characters stay in the vocabulary, so nothing is unrepresentable']
    ];
    var bar = A.ctrls(root), ro = A.readout(root);
    ['characters', 'whole words', 'subword'].forEach(function (n, i) {
      A.button(bar, n, function () { mode = i; sync(); render(); });
    });
    function sync() {
      bar.querySelectorAll('button').forEach(function (b, i) { b.classList.toggle('primary', i === mode); });
    }
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var pieces = CUTS[mode], m = META[mode];
      A.txt(ctx, 'the word', 60, 46, { size: 12, fill: P.faint });
      A.txt(ctx, WORD, 60, 76, { size: 26, mono: true, w: 700, fill: P.soft });
      A.txt(ctx, 'cut into ' + pieces.length + ' token' + (pieces.length === 1 ? '' : 's'),
        60, 118, { size: 12.5, w: 700, fill: P.a });
      var x = 60;
      pieces.forEach(function (p) {
        var w = Math.max(34, p.length * 13 + 20);
        A.rr(ctx, x, 132, w, 42, 7);
        ctx.fillStyle = P.aS; ctx.fill(); ctx.strokeStyle = P.a; ctx.lineWidth = 1.8; ctx.stroke();
        A.txt(ctx, p, x + w / 2, 159, { align: 'center', size: 15, mono: true, w: 700, fill: P.a });
        x += w + 8;
      });
      A.rr(ctx, 60, 198, 640, 74, 9);
      ctx.fillStyle = P.sunk; ctx.fill(); ctx.strokeStyle = P.lineSoft; ctx.stroke();
      A.txt(ctx, m[0], 76, 222, { size: 13, w: 700, fill: P.soft });
      A.txt(ctx, 'vocabulary needed: ' + m[1], 76, 244, { size: 11.5, mono: true, fill: P.faint });
      A.txt(ctx, m[2], 76, 264, { size: 11.5, fill: mode === 2 ? P.g : P.r });
      A.txt(ctx, 'The vocabulary is fixed before training and never grows. A model cannot learn a new',
        60, 300, { size: 12, fill: P.faint });
      A.txt(ctx, 'token later — only new arrangements of the tokens it was born with.',
        60, 320, { size: 12, w: 700, fill: P.a });
      ro.set('A useful rough figure for English: about <b>0.75 words per token</b>.\n' +
        'This is also why models are poor at spelling — they never see the letters, only the chunks.');
    }
    sync(); A.bind(c, render); render();
  });

  /* ============================================================
     3. One-hot — every word equally far from every other
     ============================================================ */
  A.def('c4-onehot', function (root) {
    var c = A.canvas(root, 760, 320), ctx = c.ctx;
    var WORDS = ['cat', 'dog', 'bulldozer'];
    var IDX = [2, 5, 9], V = 12;
    var pick = 0;
    var bar = A.ctrls(root), ro = A.readout(root);
    WORDS.forEach(function (w, i) { A.button(bar, 'compare ' + w, function () { pick = i; sync(); render(); }); });
    function sync() {
      bar.querySelectorAll('button').forEach(function (b, i) { b.classList.toggle('primary', i === pick); });
    }
    function render() {
      var P = A.pal(); c.clear(P.panel);
      A.txt(ctx, 'a 12-slot vocabulary (real ones are ~50,000)', 60, 40, { size: 12, fill: P.faint });
      WORDS.forEach(function (w, r) {
        var y = 62 + r * 62, on = r === pick;
        A.txt(ctx, w, 108, y + 26, { align: 'right', size: 13, w: 700, fill: on ? P.a : P.soft });
        for (var j = 0; j < V; j++) {
          var x = 122 + j * 46, hot = j === IDX[r];
          A.rr(ctx, x, y, 42, 40, 5);
          ctx.fillStyle = hot ? (on ? P.aS : P.bS) : P.sunk; ctx.fill();
          ctx.strokeStyle = hot ? (on ? P.a : P.b) : P.lineSoft; ctx.lineWidth = hot ? 1.8 : 1; ctx.stroke();
          A.txt(ctx, hot ? '1' : '0', x + 21, y + 25, { align: 'center', size: 12, mono: true,
            w: hot ? 700 : 400, fill: hot ? (on ? P.a : P.b) : P.faint });
        }
      });
      var other = (pick + 1) % 3, other2 = (pick + 2) % 3;
      A.txt(ctx, 'every dot product between two DIFFERENT words:', 60, 268, { size: 12.5, w: 700, fill: P.soft });
      A.txt(ctx, WORDS[pick] + ' · ' + WORDS[other] + ' = 0        ' +
                 WORDS[pick] + ' · ' + WORDS[other2] + ' = 0',
        60, 292, { size: 14, mono: true, w: 700, fill: P.r });
      A.txt(ctx, 'Identical. The encoding has already deleted every relationship between words.',
        60, 314, { size: 12, fill: P.faint });
      ro.set('The 1s never line up, so every product term is zero — there is no arrangement of ' +
        'one-hot vectors in which two words are more alike than two others.\n' +
        'Since this course measures similarity with dot products, that is fatal.');
    }
    sync(); A.bind(c, render); render();
  });

  /* ============================================================
     4. Embeddings — a lookup table, and cosine similarity
     ============================================================ */
  A.def('c4-embed', function (root) {
    var c = A.canvas(root, 760, 360), ctx = c.ctx;
    /* deliberately 2-D so it can be drawn honestly */
    var E = { king: [2.0, 1.0], queen: [1.9, 1.3], man: [1.6, 0.2], woman: [1.5, 0.5], banana: [0.2, 1.9] };
    var names = Object.keys(E);
    var a = 0, b = 1;
    var bar = A.ctrls(root), ro = A.readout(root);
    A.slider(bar, { label: 'word A', min: 0, max: names.length - 1, step: 1, value: 0,
      fmt: function (v) { return names[v]; }, on: function (v) { a = v; render(); } });
    A.slider(bar, { label: 'word B', min: 0, max: names.length - 1, step: 1, value: 1,
      fmt: function (v) { return names[v]; }, on: function (v) { b = v; render(); } });
    function dot(u, v) { return u[0] * v[0] + u[1] * v[1]; }
    function nrm(u) { return Math.sqrt(dot(u, u)); }
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var box = { x: 60, y: 40, w: 300, h: 240 };
      var S = A.axes(ctx, box, [0, 2.6], [0, 2.4], {
        xticks: 4, yticks: 4, xfmt: function (v) { return v.toFixed(1); },
        yfmt: function (v) { return v.toFixed(1); }, xlab: 'dimension 1', ylab: 'dimension 2'
      });
      names.forEach(function (n, i) {
        var v = E[n], on = i === a || i === b;
        var col = i === a ? P.a : i === b ? P.b : P.faint;
        A.line(ctx, S.X(0), S.Y(0), S.X(v[0]), S.Y(v[1]), col, on ? 2.4 : 1);
        A.dot(ctx, S.X(v[0]), S.Y(v[1]), on ? 6 : 4, col);
        A.txt(ctx, n, S.X(v[0]) + 8, S.Y(v[1]) - 6, { size: 11.5, w: on ? 700 : 500, fill: col });
      });
      var u = E[names[a]], w = E[names[b]];
      var d = dot(u, w), cs = d / (nrm(u) * nrm(w));
      A.txt(ctx, 'cosine similarity', 420, 62, { size: 12.5, w: 700, fill: P.soft });
      A.txt(ctx, names[a] + ' · ' + names[b] + ' = ' + d.toFixed(3), 420, 92,
        { size: 13, mono: true, fill: P.soft });
      A.txt(ctx, '‖' + names[a] + '‖ = ' + nrm(u).toFixed(3) +
                 '   ‖' + names[b] + '‖ = ' + nrm(w).toFixed(3), 420, 114,
        { size: 12, mono: true, fill: P.faint });
      A.rr(ctx, 420, 130, 280, 54, 8);
      ctx.fillStyle = cs > 0.9 ? P.gS : cs > 0.6 ? P.aS : P.sunk; ctx.fill();
      ctx.strokeStyle = cs > 0.9 ? P.g : cs > 0.6 ? P.a : P.lineSoft; ctx.lineWidth = 1.8; ctx.stroke();
      A.txt(ctx, 'cos = ' + cs.toFixed(3), 560, 164, { align: 'center', size: 22, mono: true, w: 700,
        fill: cs > 0.9 ? P.g : cs > 0.6 ? P.a : P.soft });
      A.txt(ctx, cs > 0.9 ? 'nearly the same direction — closely related'
                          : cs > 0.6 ? 'partly aligned' : 'largely unrelated',
        420, 206, { size: 11.5, fill: P.faint });
      A.txt(ctx, 'Real embeddings have 512 dimensions, not 2 — but the arithmetic is identical,',
        60, 306, { size: 12, fill: P.faint });
      A.txt(ctx, 'and the dot product is the same one you have used since Foundations.',
        60, 326, { size: 12, fill: P.faint });
      A.txt(ctx, 'Nobody assigned these numbers. Gradient descent did, exactly as in C3 W2.',
        60, 350, { size: 12, w: 700, fill: P.a });
      ro.set('Cosine divides out both lengths, so only <b>direction</b> counts.\n' +
        'That matters because vector length tracks how often a token appeared in training — ' +
        'which is not what you want to compare meanings on.');
    }
    A.bind(c, render); render();
  });

  /* ============================================================
     5. The RNN — one summary, updated word by word
     ============================================================ */
  A.def('c4-rnn', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var WORDS = ['the', 'keys', 'to', 'the', 'cabinet', 'are', 'on', 'the', 'table'];
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var step = Math.floor((t * 0.9) % (WORDS.length + 1));
      A.txt(ctx, 'reading one word at a time, carrying a running summary', 50, 40,
        { size: 12.5, w: 700, fill: P.soft });
      WORDS.forEach(function (w, i) {
        var x = 50 + i * 78, seen = i < step, now = i === step - 1;
        A.rr(ctx, x, 58, 70, 36, 6);
        ctx.fillStyle = now ? P.aS : seen ? P.sunk : P.panel; ctx.fill();
        ctx.strokeStyle = now ? P.a : seen ? P.lineSoft : P.line; ctx.lineWidth = now ? 2 : 1; ctx.stroke();
        A.txt(ctx, w, x + 35, 82, { align: 'center', size: 12, mono: true,
          w: now ? 700 : 500, fill: now ? P.a : seen ? P.soft : P.faint });
      });
      /* the hidden state, and how much of each word survives in it */
      A.txt(ctx, 'h — the hidden state (one fixed-size summary)', 50, 138,
        { size: 12.5, w: 700, fill: P.b });
      A.rr(ctx, 50, 152, 650, 52, 9);
      ctx.fillStyle = P.bS; ctx.fill(); ctx.strokeStyle = P.b; ctx.lineWidth = 2; ctx.stroke();
      for (var i = 0; i < step; i++) {
        /* each earlier word's share decays as later words overwrite it */
        var age = step - 1 - i;
        var share = Math.pow(0.62, age);
        var w = Math.max(2, 620 * share / 2.6);
        var xx = 60 + i * 6;
        ctx.save(); ctx.globalAlpha = Math.max(0.12, share);
        A.rr(ctx, xx, 162, w, 32, 4); ctx.fillStyle = P.b; ctx.fill(); ctx.restore();
      }
      A.txt(ctx, step === 0 ? 'empty' : 'mostly the last word or two — earlier ones faded',
        375, 226, { align: 'center', size: 11.5, fill: P.faint });
      A.txt(ctx, 'Same weights at every position, so any sentence length fits one model. That is the',
        50, 264, { size: 12, fill: P.soft });
      A.txt(ctx, 'elegant part — and the fading you can see above is the price.', 50, 284,
        { size: 12, w: 700, fill: P.a });
      A.txt(ctx, 'By the time it reaches “table”, “keys” is nearly gone — yet ' +
        '“are” had to agree with it.', 50, 314, { size: 11.5, fill: P.faint });
    }
    A.autoplay(root, c, render);
  });

  /* ============================================================
     6. Vanishing gradient across time
     ============================================================ */
  A.def('c4-vanish', function (root) {
    var c = A.canvas(root, 760, 340), ctx = c.ctx;
    var slope = 0.25;
    var bar = A.ctrls(root), log = A.log(root), ro = A.readout(root);
    A.slider(bar, { label: 'slope per step', min: 0.1, max: 0.95, step: .05, value: slope,
      fmt: function (v) { return v.toFixed(2); }, on: function (v) { slope = v; render(); } });
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var box = { x: 70, y: 40, w: 620, h: 200 };
      var S = A.axes(ctx, box, [0, 50], [-32, 0], {
        xticks: 5, yticks: 4,
        xfmt: function (v) { return v.toFixed(0); },
        yfmt: function (v) { return '1e' + v.toFixed(0); },
        xlab: 'steps back through the sequence', ylab: 'gradient reaching there'
      });
      A.plot(ctx, S, [1, 50], function (n) {
        return Math.max(-32, Math.log10(Math.pow(slope, n)));
      }, P.r, 2.6);
      /* the reference: a one-step path, which is what attention gives you */
      ctx.save(); ctx.strokeStyle = P.g; ctx.lineWidth = 2.2; ctx.setLineDash([5, 4]);
      ctx.beginPath(); ctx.moveTo(S.X(0), S.Y(0)); ctx.lineTo(S.X(50), S.Y(0)); ctx.stroke(); ctx.restore();
      A.txt(ctx, 'attention: one step, no decay', S.X(26), S.Y(0) - 10, { size: 11.5, w: 700, fill: P.g });
      A.txt(ctx, 'RNN: multiplied every step', S.X(12), S.Y(-14), { size: 11.5, w: 700, fill: P.r });
      var g20 = Math.pow(slope, 20);
      A.txt(ctx, 'Twenty words back is an ordinary distance in a sentence. At this slope the update',
        70, 276, { size: 12, fill: P.soft });
      A.txt(ctx, 'arriving there is ' + g20.toExponential(1) + ' of the signal — it does not arrive at all.',
        70, 296, { size: 12, w: 700, fill: P.r });
      A.txt(ctx, 'LSTMs push the usable range from roughly 10 steps to perhaps 100. Still a ceiling.',
        70, 326, { size: 11.5, fill: P.faint });
      log.set('slope ' + slope.toFixed(2) + ':  10 steps → ' + Math.pow(slope, 10).toExponential(2) +
        '   20 steps → ' + g20.toExponential(2) + '   50 steps → ' + Math.pow(slope, 50).toExponential(2),
        'gradient ∝ slope^distance   (one factor per timestep, exactly as one per layer in C2 W2)');
      ro.set('This is the same arithmetic as deep sigmoid networks in C2 W2 — many slopes below 1 ' +
        'multiplied together.\nThe difference is that sequences are far longer than networks are deep.');
    }
    A.bind(c, render); render();
  });

  /* ============================================================
     7. The bottleneck, versus attention
     ============================================================ */
  A.def('c4-bottleneck', function (root) {
    var c = A.canvas(root, 760, 350), ctx = c.ctx;
    var useAttn = true;
    var bar = A.ctrls(root), ro = A.readout(root);
    A.toggle(bar, 'use attention', function (v) { useAttn = v; render(); }, true);
    var SRC = ['le', 'chat', 'noir', 'dort'];
    var OUT = ['the', 'black', 'cat', 'sleeps'];
    /* which source word each output word mostly needs */
    var FOCUS = [0, 2, 1, 3];
    var pick = 1;
    OUT.forEach(function (w, i) { A.button(bar, 'output: ' + w, function () { pick = i; render(); }); });
    function render() {
      var P = A.pal(); c.clear(P.panel);
      A.txt(ctx, 'source', 50, 44, { size: 12, w: 700, fill: P.b });
      SRC.forEach(function (w, i) {
        var x = 50 + i * 120;
        A.rr(ctx, x, 56, 108, 40, 7);
        ctx.fillStyle = P.bS; ctx.fill(); ctx.strokeStyle = P.b; ctx.lineWidth = 1.6; ctx.stroke();
        A.txt(ctx, w, x + 54, 82, { align: 'center', size: 13, mono: true, w: 700, fill: P.b });
      });
      if (!useAttn) {
        A.rr(ctx, 200, 128, 180, 46, 8);
        ctx.fillStyle = P.rS; ctx.fill(); ctx.strokeStyle = P.r; ctx.lineWidth = 2.2; ctx.stroke();
        A.txt(ctx, 'ONE vector', 290, 148, { align: 'center', size: 12.5, w: 700, fill: P.r });
        A.txt(ctx, 'everything must fit here', 290, 166, { align: 'center', size: 10.5, fill: P.r });
        SRC.forEach(function (w, i) { A.arrow(ctx, 104 + i * 120, 98, 290, 126, P.line, 1.4); });
        A.arrow(ctx, 290, 176, 290, 212, P.r, 2);
      } else {
        SRC.forEach(function (w, i) {
          var wgt = i === FOCUS[pick] ? 0.7 : 0.1;
          ctx.save(); ctx.globalAlpha = 0.25 + wgt;
          A.arrow(ctx, 104 + i * 120, 98, 300, 212, i === FOCUS[pick] ? P.a : P.line,
            i === FOCUS[pick] ? 2.6 : 1);
          ctx.restore();
          A.txt(ctx, 'α = ' + wgt.toFixed(1), 104 + i * 120, 118,
            { align: 'center', size: 10.5, mono: true, fill: i === FOCUS[pick] ? P.a : P.faint });
        });
      }
      A.txt(ctx, 'generating output word:', 50, 232, { size: 12, fill: P.faint });
      OUT.forEach(function (w, i) {
        var x = 50 + i * 120, on = i === pick;
        A.rr(ctx, x, 244, 108, 40, 7);
        ctx.fillStyle = on ? P.aS : P.sunk; ctx.fill();
        ctx.strokeStyle = on ? P.a : P.lineSoft; ctx.lineWidth = on ? 2 : 1; ctx.stroke();
        A.txt(ctx, w, x + 54, 270, { align: 'center', size: 13, mono: true, w: on ? 700 : 500,
          fill: on ? P.a : P.soft });
      });
      A.txt(ctx, useAttn
        ? 'Every source position stays available. The model picks a different mixture for each output word.'
        : 'The whole source is crushed into one fixed vector before a single output word is written.',
        50, 312, { size: 12, w: 700, fill: useAttn ? P.g : P.r });
      A.txt(ctx, useAttn
        ? 'Note the reordering: French “chat noir” becomes English “black cat”, and attention simply looks where it needs to.'
        : 'Quality collapsed as sentences grew longer — that chart is why attention was invented.',
        50, 336, { size: 11.5, fill: P.faint });
      ro.set('Attention is a <b>weighted average</b> of every position, with weights from a softmax.\n' +
        'You have known both halves since Course 2 — what is new is what they are pointed at.');
    }
    A.bind(c, render); render();
  });

  /* ============================================================
     8. Week 1 recap
     ============================================================ */
  A.def('c4-w1recap', function (root) {
    var c = A.canvas(root, 760, 340), ctx = c.ctx;
    function render(t) {
      var P = A.pal(); c.clear(P.panel);
      t = t || 0;
      var step = Math.floor((t * 0.5) % 4);
      var rows = [
        ['tokens', 'text cut into pieces from a fixed vocabulary', P.b],
        ['embeddings', 'each token looked up in a learned table → a vector', P.p],
        ['the RNN answer', 'one running summary — forgets, and cannot parallelise', P.r],
        ['attention', 'read every position directly, weighted by relevance', P.g]
      ];
      rows.forEach(function (r, i) {
        var y = 54 + i * 62, on = i === step;
        A.rr(ctx, 50, y, 650, 50, 9);
        ctx.fillStyle = on ? P.aS : P.sunk; ctx.fill();
        ctx.strokeStyle = on ? P.a : P.lineSoft; ctx.lineWidth = on ? 2.2 : 1; ctx.stroke();
        A.txt(ctx, r[0], 70, y + 22, { size: 13, w: 700, fill: on ? P.a : r[2] });
        A.txt(ctx, r[1], 70, y + 40, { size: 11.5, fill: P.faint });
        if (i < 3) A.arrow(ctx, 375, y + 52, 375, y + 60, P.line, 1.4);
      });
      A.txt(ctx, 'The question that ends the week: if attention already connects any two positions in',
        50, 312, { size: 12, fill: P.soft });
      A.txt(ctx, 'one step — what is the RNN still for?', 50, 332, { size: 12.5, w: 700, fill: P.a });
    }
    A.autoplay(root, c, render);
  });

})();
