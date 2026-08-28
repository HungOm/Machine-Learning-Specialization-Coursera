/* Widgets for Course 2 / Week 4 — decision trees and tree ensembles */
(function () {
  'use strict';

  /* the ten cats-and-not-cats from the lectures
     E: 1 = pointy, 0 = floppy   F: 1 = round, 0 = not round   W: 1 = whiskers present */
  var CATS = [
    { E: 1, F: 1, W: 1, y: 1, wt: 7.2 },   /* pointy, round,     whiskers  -> cat     */
    { E: 1, F: 1, W: 1, y: 1, wt: 8.8 },
    { E: 1, F: 1, W: 0, y: 1, wt: 9.2 },
    { E: 1, F: 1, W: 0, y: 1, wt: 8.4 },
    { E: 1, F: 0, W: 1, y: 0, wt: 7.6 },   /* pointy, not round, whiskers  -> not cat */
    { E: 0, F: 0, W: 1, y: 1, wt: 10.2 },  /* floppy, not round, whiskers  -> cat     */
    { E: 0, F: 1, W: 0, y: 0, wt: 15.0 },
    { E: 0, F: 1, W: 0, y: 0, wt: 18.0 },
    { E: 0, F: 1, W: 0, y: 0, wt: 11.0 },
    { E: 0, F: 0, W: 0, y: 0, wt: 20.0 }
  ];
  var FEAT = [
    { k: 'E', n: 'ear shape', yes: 'pointy', no: 'floppy' },
    { k: 'F', n: 'face shape', yes: 'round', no: 'not round' },
    { k: 'W', n: 'whiskers', yes: 'present', no: 'absent' }
  ];
  function H(p) {
    if (p <= 0 || p >= 1) return 0;
    return -p * Math.log2(p) - (1 - p) * Math.log2(1 - p);
  }
  function frac(set) { return set.length ? set.filter(function (e) { return e.y === 1; }).length / set.length : 0; }
  function split(set, k) {
    return { yes: set.filter(function (e) { return e[k] === 1; }),
             no: set.filter(function (e) { return e[k] === 0; }) };
  }
  function gain(set, k) {
    var s = split(set, k), n = set.length;
    if (!s.yes.length || !s.no.length) return 0;
    return H(frac(set)) - (s.yes.length / n * H(frac(s.yes)) + s.no.length / n * H(frac(s.no)));
  }
  /* little cat / not-cat glyph */
  function critter(ctx, x, y, s, isCat, P) {
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
    ctx.fillStyle = isCat ? P.a : P.faint;
    ctx.beginPath(); ctx.arc(0, 0, 7, 0, 6.2832); ctx.fill();
    if (isCat) {
      ctx.beginPath(); ctx.moveTo(-6, -4); ctx.lineTo(-8, -11); ctx.lineTo(-2, -6); ctx.closePath(); ctx.fill();
      ctx.beginPath(); ctx.moveTo(6, -4); ctx.lineTo(8, -11); ctx.lineTo(2, -6); ctx.closePath(); ctx.fill();
    } else {
      ctx.beginPath(); ctx.ellipse(-6, -3, 2.6, 5, .5, 0, 6.2832); ctx.fill();
      ctx.beginPath(); ctx.ellipse(6, -3, 2.6, 5, -.5, 0, 6.2832); ctx.fill();
    }
    ctx.restore();
  }
  function node(ctx, x, y, w, h, label, sub, P, on, colr) {
    A.rr(ctx, x - w / 2, y - h / 2, w, h, 9);
    ctx.fillStyle = on ? P.aS : P.sunk; ctx.fill();
    ctx.strokeStyle = on ? P.a : (colr || P.lineSoft); ctx.lineWidth = on ? 2.2 : 1.4; ctx.stroke();
    A.txt(ctx, label, x, y + (sub ? -2 : 4), { align: 'center', size: 12.5, w: 700,
      fill: on ? P.a : (colr || P.soft) });
    if (sub) A.txt(ctx, sub, x, y + 14, { align: 'center', size: 10.5, fill: P.faint });
  }

  /* ============================================================
     1. A decision tree, classifying
     ============================================================ */
  A.def('treeplay', function (root) {
    var c = A.canvas(root, 760, 340), ctx = c.ctx;
    var ex = { E: 1, F: 1, W: 1 };
    var bar = A.ctrls(root), ro = A.readout(root);
    A.toggle(bar, 'pointy ears', function (v) { ex.E = v ? 1 : 0; render(); }, true);
    A.toggle(bar, 'round face', function (v) { ex.F = v ? 1 : 0; render(); }, true);
    A.toggle(bar, 'whiskers', function (v) { ex.W = v ? 1 : 0; render(); }, true);
    function path() {
      if (ex.E === 1) return ['root', ex.F === 1 ? 'L1' : 'L2', ex.F === 1 ? 1 : 0];
      return ['root', ex.W === 1 ? 'R1' : 'R2', ex.W === 1 ? 1 : 0];
    }
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var p = path(), res = p[2];
      var N = {
        root: { x: 380, y: 60, w: 150, h: 44, l: 'ear shape?', s: null },
        mid1: { x: 210, y: 165, w: 150, h: 44, l: 'face shape?', s: null },
        mid2: { x: 550, y: 165, w: 150, h: 44, l: 'whiskers?', s: null },
        L1: { x: 120, y: 275, w: 118, h: 44, l: 'CAT', s: '4 of 4' },
        L2: { x: 300, y: 275, w: 118, h: 44, l: 'not cat', s: '0 of 1' },
        R1: { x: 470, y: 275, w: 118, h: 44, l: 'CAT', s: '1 of 1' },
        R2: { x: 640, y: 275, w: 118, h: 44, l: 'not cat', s: '0 of 4' }
      };
      var edges = [
        ['root', 'mid1', 'pointy', ex.E === 1], ['root', 'mid2', 'floppy', ex.E === 0],
        ['mid1', 'L1', 'round', ex.E === 1 && ex.F === 1], ['mid1', 'L2', 'not round', ex.E === 1 && ex.F === 0],
        ['mid2', 'R1', 'present', ex.E === 0 && ex.W === 1], ['mid2', 'R2', 'absent', ex.E === 0 && ex.W === 0]
      ];
      edges.forEach(function (e) {
        var a = N[e[0]], b = N[e[1]];
        A.line(ctx, a.x, a.y + a.h / 2, b.x, b.y - b.h / 2, e[3] ? P.a : P.line, e[3] ? 2.6 : 1.3);
        A.txt(ctx, e[2], (a.x + b.x) / 2 + (b.x < a.x ? -22 : 22), (a.y + b.y) / 2,
          { align: 'center', size: 10.5, w: e[3] ? 700 : 500, fill: e[3] ? P.a : P.faint });
        if (e[3]) {
          var u = (t * .8) % 1;
          A.dot(ctx, A.lerp(a.x, b.x, u), A.lerp(a.y + a.h / 2, b.y - b.h / 2, u), 4, P.a);
        }
      });
      var live = { root: true, mid1: ex.E === 1, mid2: ex.E === 0 };
      live[p[1]] = true;
      Object.keys(N).forEach(function (k) {
        var n = N[k];
        var isLeaf = k[0] === 'L' || k[0] === 'R';
        node(ctx, n.x, n.y, n.w, n.h, n.l, n.s, P, !!live[k],
          isLeaf ? (n.l === 'CAT' ? P.g : P.faint) : P.soft);
      });
      /* the animal being classified */
      A.rr(ctx, 30, 30, 130, 96, 10); ctx.fillStyle = P.sunk; ctx.fill();
      ctx.strokeStyle = P.line; ctx.stroke();
      critter(ctx, 95, 66, 1.7, res === 1, P);
      A.txt(ctx, 'your animal', 95, 108, { align: 'center', size: 11, fill: P.faint });
      A.txt(ctx, res === 1 ? '→ CAT' : '→ not a cat', 95, 122,
        { align: 'center', size: 12.5, w: 700, fill: res === 1 ? P.g : P.faint });
      A.txt(ctx, 'A decision tree is a flowchart of yes/no questions. Making a prediction = walking one path.',
        30, 322, { size: 12, fill: P.faint });
      ro.set('ear = <b>' + (ex.E ? 'pointy' : 'floppy') + '</b>, face = <b>' + (ex.F ? 'round' : 'not round') +
        '</b>, whiskers = <b>' + (ex.W ? 'present' : 'absent') + '</b>  →  <b>' +
        (res ? 'cat' : 'not a cat') + '</b>\nOnly the features ON THE PATH were used. ' +
        (ex.E ? 'Whiskers were never even looked at.' : 'Face shape was never even looked at.'));
    }
    A.autoplay(root, c, render);
  });

  /* ============================================================
     2. The two decisions in learning a tree
     ============================================================ */
  A.def('treeprocess', function (root) {
    var c = A.canvas(root, 760, 340), ctx = c.ctx;
    var stops = [
      ['a node is 100% one class', 'nothing left to separate — make it a leaf'],
      ['splitting would exceed max depth', 'keeps the tree small, and small trees generalise'],
      ['the information gain is tiny', 'not worth the extra complexity for 0.001'],
      ['too few examples in a node', 'a split decided by 2 examples is noise, not signal']
    ];
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var hot = Math.floor((t * .5) % 4);
      A.rr(ctx, 40, 42, 320, 116, 10); ctx.fillStyle = P.aS; ctx.fill();
      ctx.strokeStyle = P.a; ctx.lineWidth = 1.8; ctx.stroke();
      A.txt(ctx, 'DECISION 1', 200, 66, { align: 'center', size: 11, w: 800, fill: P.a });
      A.txt(ctx, 'which feature to split on?', 200, 90, { align: 'center', size: 15, w: 700, fill: P.a });
      A.txt(ctx, 'answer: the one that makes the two', 200, 116, { align: 'center', size: 12, fill: P.soft });
      A.txt(ctx, 'resulting groups as PURE as possible', 200, 134, { align: 'center', size: 12, fill: P.soft });
      A.txt(ctx, '(lessons 3 and 4)', 200, 150, { align: 'center', size: 10.5, fill: P.faint });
      A.rr(ctx, 400, 42, 320, 116, 10); ctx.fillStyle = P.pS; ctx.fill();
      ctx.strokeStyle = P.p; ctx.lineWidth = 1.8; ctx.stroke();
      A.txt(ctx, 'DECISION 2', 560, 66, { align: 'center', size: 11, w: 800, fill: P.p });
      A.txt(ctx, 'when do you stop splitting?', 560, 90, { align: 'center', size: 15, w: 700, fill: P.p });
      A.txt(ctx, 'answer: any of four rules —', 560, 116, { align: 'center', size: 12, fill: P.soft });
      A.txt(ctx, 'and they are all about not overfitting', 560, 134, { align: 'center', size: 12, fill: P.soft });
      stops.forEach(function (s, i) {
        var y = 186 + i * 32, on = i === hot;
        A.rr(ctx, 60, y, 640, 28, 6);
        ctx.fillStyle = on ? P.pS : P.sunk; ctx.fill();
        ctx.strokeStyle = on ? P.p : P.lineSoft; ctx.lineWidth = on ? 1.8 : 1; ctx.stroke();
        A.txt(ctx, 'stop when ' + s[0], 76, y + 18, { size: 12, w: on ? 700 : 500, fill: on ? P.p : P.soft });
        A.txt(ctx, s[1], 400, y + 18, { size: 11, fill: P.faint });
      });
      A.txt(ctx, 'A bigger tree always fits the training data better — and a tree deep enough to isolate every',
        40, 24, { size: 11.5, fill: P.faint });
      A.txt(ctx, 'example is the purest possible overfit.', 40, 334, { size: 11.5, w: 700, fill: P.soft });
    }
    A.autoplay(root, c, render);
  });

  /* ============================================================
     3. Entropy
     ============================================================ */
  A.def('entropy', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var p = 0.5;
    var bar = A.ctrls(root), ro = A.readout(root);
    A.slider(bar, { label: 'fraction that are cats', min: 0, max: 1, step: 1 / 12, value: p,
      fmt: function (v) { return Math.round(v * 12) + '/12'; }, on: function (v) { p = v; render(); } });
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var box = { x: 420, y: 44, w: 280, h: 200 };
      var S = A.axes(ctx, box, [0, 1], [0, 1.05], {
        xticks: 4, yticks: 4, xfmt: function (v) { return v.toFixed(2); },
        yfmt: function (v) { return v.toFixed(1); }, xlab: 'p — fraction of cats', ylab: 'H(p) — impurity'
      });
      A.plot(ctx, S, [0.0005, 0.9995], H, P.a, 2.8);
      A.dot(ctx, S.X(p), S.Y(H(p)), 7, P.a);
      A.line(ctx, S.X(p), box.y + box.h, S.X(p), S.Y(H(p)), P.a, 1.2, [3, 3]);
      A.txt(ctx, 'H = ' + H(p).toFixed(3), S.X(p) + 8, S.Y(H(p)) - 10,
        { size: 12.5, mono: true, w: 700, fill: P.a });
      A.txt(ctx, 'pure', S.X(.03), S.Y(.06), { size: 11, fill: P.g });
      A.txt(ctx, 'pure', S.X(.9), S.Y(.06), { size: 11, fill: P.g });
      A.txt(ctx, 'total mess', S.X(.5), S.Y(1.02), { align: 'center', size: 11, w: 700, fill: P.r });
      /* the jar of animals */
      var nCat = Math.round(p * 12);
      A.txt(ctx, 'a bag of 12 animals', 190, 34, { align: 'center', size: 12.5, w: 700, fill: P.soft });
      A.rr(ctx, 70, 46, 240, 190, 12); ctx.fillStyle = P.sunk; ctx.fill();
      ctx.strokeStyle = P.line; ctx.lineWidth = 1.6; ctx.stroke();
      for (var i = 0; i < 12; i++) {
        var x = 108 + (i % 4) * 58, y = 84 + Math.floor(i / 4) * 56;
        critter(ctx, x, y, 1.5, i < nCat, P);
      }
      A.txt(ctx, nCat + ' cats, ' + (12 - nCat) + ' not', 190, 258,
        { align: 'center', size: 13, w: 700, fill: P.a });
      var verdict = (nCat === 0 || nCat === 12) ? ['completely pure — H = 0', P.g]
        : (nCat === 6) ? ['maximum mess — H = 1', P.r] : ['partly mixed', P.soft];
      A.txt(ctx, verdict[0], 190, 280, { align: 'center', size: 12.5, w: 700, fill: verdict[1] });
      A.txt(ctx, 'Entropy answers one question: “if I reach into this bag, how surprised will I be?”',
        60, 310, { size: 12, w: 600, fill: P.soft });
      A.txt(ctx, 'All cats → never surprised → 0. Half and half → maximum surprise → 1.',
        60, 326, { size: 11.5, fill: P.faint });
      ro.set('H(p) = −p·log₂(p) − (1−p)·log₂(1−p)' +
        '\np = ' + p.toFixed(3) + '  →  H = <b>' + H(p).toFixed(4) + '</b>   ' +
        '(log base 2, so a 50/50 bag is exactly 1 bit of uncertainty — one coin flip)');
    }
    A.bind(c, render); render();
  });

  /* ============================================================
     4. Information gain — choosing the split
     ============================================================ */
  A.def('infogain', function (root) {
    var c = A.canvas(root, 760, 340), ctx = c.ctx;
    var ro = A.readout(root);
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var gains = FEAT.map(function (f) { return gain(CATS, f.k); });
      var best = 0; gains.forEach(function (g, i) { if (g > gains[best]) best = i; });
      var reveal = Math.min(3, Math.floor((t * .7) % 5));
      A.txt(ctx, 'root node: 5 cats, 5 not cats  →  H = 1.00  (maximum mess)', 40, 34,
        { size: 13, w: 700, fill: P.soft });
      FEAT.forEach(function (f, i) {
        var s = split(CATS, f.k), x = 40 + i * 240, shown = i < reveal;
        var wH = s.yes.length / 10 * H(frac(s.yes)) + s.no.length / 10 * H(frac(s.no));
        var on = reveal > 3 && i === best;
        A.rr(ctx, x, 50, 220, 230, 10);
        ctx.fillStyle = on ? P.aS : P.sunk; ctx.fill();
        ctx.strokeStyle = on ? P.a : P.lineSoft; ctx.lineWidth = on ? 2.4 : 1.2; ctx.stroke();
        A.txt(ctx, 'split on ' + f.n, x + 110, 72, { align: 'center', size: 13, w: 700,
          fill: on ? P.a : P.soft });
        if (!shown) { A.txt(ctx, '…', x + 110, 160, { align: 'center', size: 20, fill: P.faint }); return; }
        [[s.yes, f.yes, 96], [s.no, f.no, 176]].forEach(function (br) {
          var set = br[0], y = br[2];
          var nc = set.filter(function (e) { return e.y === 1; }).length;
          A.txt(ctx, br[1] + ' — ' + nc + ' / ' + set.length + ' cats', x + 16, y,
            { size: 11.5, w: 600, fill: P.soft });
          for (var k = 0; k < set.length; k++)
            critter(ctx, x + 26 + k * 28, y + 22, 1.1, set[k].y === 1, P);
          A.txt(ctx, 'H = ' + H(frac(set)).toFixed(3), x + 16, y + 48,
            { size: 11.5, mono: true, fill: P.faint });
        });
        A.txt(ctx, 'weighted H = ' + wH.toFixed(3), x + 16, 250, { size: 11.5, mono: true, fill: P.faint });
        A.txt(ctx, 'gain = ' + gains[i].toFixed(3), x + 16, 268,
          { size: 13, mono: true, w: 700, fill: on ? P.a : P.soft });
      });
      if (reveal > 3) {
        A.txt(ctx, '→ split on ' + FEAT[best].n + ': it removes the most uncertainty (' +
          gains[best].toFixed(2) + ' bits)', 40, 306, { size: 13.5, w: 700, fill: P.a });
      } else {
        A.txt(ctx, 'try every feature, compute the gain, keep the biggest…', 40, 306,
          { size: 13, fill: P.faint });
      }
      A.txt(ctx, 'the weighting matters: a very pure branch holding 1 example is worth less than a fairly pure one holding 9',
        40, 328, { size: 11.5, fill: P.faint });
      ro.set('gain = H(root) − [ (w<sub>left</sub>·H(left) + w<sub>right</sub>·H(right)) ]' +
        '\near shape <b>' + gains[0].toFixed(4) + '</b>   ·   face shape <b>' + gains[1].toFixed(4) +
        '</b>   ·   whiskers <b>' + gains[2].toFixed(4) + '</b>');
    }
    A.autoplay(root, c, render);
  });

  /* ============================================================
     5. Building the whole tree, recursively
     ============================================================ */
  A.def('treebuild', function (root) {
    var c = A.canvas(root, 760, 340), ctx = c.ctx;
    var ro = A.readout(root);
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var step = Math.floor((t * .45) % 6);
      var sE = split(CATS, 'E');
      var sEF = split(sE.yes, 'F'), sEW = split(sE.no, 'W');
      var items = [
        { k: 'root', x: 380, y: 56, set: CATS, l: 'all 10\n5 cats', show: 0 },
        { k: 'a', x: 210, y: 150, set: sE.yes, l: 'pointy', show: 1 },
        { k: 'b', x: 550, y: 150, set: sE.no, l: 'floppy', show: 1 },
        { k: 'c', x: 120, y: 258, set: sEF.yes, l: 'round', show: 2 },
        { k: 'd', x: 300, y: 258, set: sEF.no, l: 'not round', show: 2 },
        { k: 'e', x: 470, y: 258, set: sEW.yes, l: 'whiskers', show: 3 },
        { k: 'f', x: 640, y: 258, set: sEW.no, l: 'no whiskers', show: 3 }
      ];
      var links = [[0, 1], [0, 2], [1, 3], [1, 4], [2, 5], [2, 6]];
      links.forEach(function (e) {
        var a = items[e[0]], b = items[e[1]];
        if (step >= b.show) A.line(ctx, a.x, a.y + 24, b.x, b.y - 24, P.line, 1.6);
      });
      items.forEach(function (it) {
        if (step < it.show) return;
        var nc = it.set.filter(function (e) { return e.y === 1; }).length;
        var pure = nc === 0 || nc === it.set.length;
        var justNow = step === it.show;
        A.rr(ctx, it.x - 62, it.y - 26, 124, 52, 9);
        ctx.fillStyle = justNow ? P.aS : (pure ? (nc ? P.gS : P.sunk) : P.sunk); ctx.fill();
        ctx.strokeStyle = justNow ? P.a : (pure ? (nc ? P.g : P.line) : P.lineSoft);
        ctx.lineWidth = justNow ? 2.2 : 1.4; ctx.stroke();
        A.txt(ctx, it.l, it.x, it.y - 8, { align: 'center', size: 11.5, w: 700,
          fill: justNow ? P.a : P.soft });
        A.txt(ctx, nc + ' cat / ' + (it.set.length - nc) + ' not', it.x, it.y + 8,
          { align: 'center', size: 11, mono: true, fill: P.faint });
        if (pure && step >= 4) A.txt(ctx, nc ? '✓ LEAF: cat' : '✓ LEAF: not cat', it.x, it.y + 40,
          { align: 'center', size: 11, w: 700, fill: nc ? P.g : P.faint });
      });
      var msg = ['start: all 10 examples, H = 1.0 — pick the best split (ear shape)',
        'two groups. now treat EACH ONE as a brand new little problem',
        'left branch: best split is face shape',
        'right branch: best split is whiskers',
        'every group is now 100% one class — stop',
        'done. the recursion ended because there was nothing left to separate'][step];
      A.txt(ctx, msg, 40, 320, { size: 12.5, w: 700, fill: P.a });
      /* the root box's top edge is at y=30 (56-26) — keep this caption clear above it */
      A.txt(ctx, 'recursion: the algorithm for a branch is the SAME algorithm as for the whole tree, on less data',
        40, 16, { size: 12, fill: P.faint });
      ro.set('build(node):\n  if stopping criterion met → make a leaf, predict the majority class\n' +
        '  else → pick the feature with the highest information gain,\n' +
        '         split the examples, and call <b>build()</b> on each half');
    }
    A.autoplay(root, c, render);
  });

  /* ============================================================
     6. One-hot encoding
     ============================================================ */
  A.def('onehot', function (root) {
    var c = A.canvas(root, 760, 320), ctx = c.ctx;
    var vals = ['pointy', 'floppy', 'oval'];
    var rows = [0, 1, 2, 0, 2];
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var phase = A.clamp(((t * .4) % 3) - .3, 0, 1);
      A.txt(ctx, 'one column, three possible values', 150, 40, { align: 'center', size: 12.5, w: 700, fill: P.soft });
      A.matrix(ctx, 60, 60, 5, 1, 180, 42, P, function (i) { return vals[rows[i]]; },
        { state: function () { return 2; }, size: 12.5, label: 'ear shape' });
      A.arrow(ctx, 260, 165, 320, 165, P.line, 2);
      A.txt(ctx, 'one-hot', 290, 155, { align: 'center', size: 11, fill: P.faint });
      A.txt(ctx, 'three columns, each 0 or 1', 530, 40, { align: 'center', size: 12.5, w: 700, fill: P.soft });
      A.matrix(ctx, 380, 60, 5, 3, 100, 42, P,
        function (i, j) { return phase > .35 ? (rows[i] === j ? '1' : '0') : ''; },
        { state: function (i, j) { return phase > .35 && rows[i] === j ? 3 : 0; }, size: 13 });
      ['pointy', 'floppy', 'oval'].forEach(function (v, j) {
        A.txt(ctx, v, 380 + j * 100 + 48, 52, { align: 'center', size: 10.5, fill: P.faint });
      });
      A.txt(ctx, 'exactly ONE of the three is hot (= 1) in every row — hence the name', 380, 288,
        { align: 'center', size: 12, fill: P.faint });
      A.txt(ctx, 'Now every feature is binary again, so the yes/no tree works unchanged. Bonus: neural networks need this too.',
        40, 310, { size: 12, w: 700, fill: P.soft });
    }
    A.autoplay(root, c, render);
  });

  /* ============================================================
     7. Splitting on a continuous feature
     ============================================================ */
  A.def('contsplit', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var th = 9.0;
    var bar = A.ctrls(root), ro = A.readout(root);
    A.slider(bar, { label: 'threshold (lb)', min: 6, max: 21, step: .1, value: th,
      fmt: function (v) { return v.toFixed(1); }, on: function (v) { th = v; render(); } });
    function gainAt(t0) {
      var lo = CATS.filter(function (e) { return e.wt <= t0; });
      var hi = CATS.filter(function (e) { return e.wt > t0; });
      if (!lo.length || !hi.length) return 0;
      return H(.5) - (lo.length / 10 * H(frac(lo)) + hi.length / 10 * H(frac(hi)));
    }
    function render() {
      var P = A.pal(); c.clear(P.panel);
      /* the number line */
      var x0 = 60, x1 = 700, W = x1 - x0;
      function px(w) { return x0 + (w - 6) / 15 * W; }
      A.line(ctx, x0, 110, x1, 110, P.line, 1.6);
      for (var v = 6; v <= 21; v += 3) {
        A.line(ctx, px(v), 106, px(v), 116, P.line, 1.2);
        A.txt(ctx, v + ' lb', px(v), 132, { align: 'center', size: 11, fill: P.faint });
      }
      CATS.forEach(function (e) { critter(ctx, px(e.wt), 84, 1.3, e.y === 1, P); });
      A.line(ctx, px(th), 56, px(th), 124, P.a, 2.4);
      A.txt(ctx, '≤ ' + th.toFixed(1), px(th) - 8, 50, { align: 'right', size: 12, w: 700, fill: P.a });
      A.txt(ctx, '> ' + th.toFixed(1), px(th) + 8, 50, { size: 12, w: 700, fill: P.a });
      A.txt(ctx, 'weight is a NUMBER, not a category — so the question becomes “is it ≤ some threshold?”',
        60, 34, { size: 12, w: 700, fill: P.soft });
      /* the gain curve */
      var box = { x: 60, y: 160, w: 640, h: 110 };
      var S = A.axes(ctx, box, [6, 21], [0, .6], {
        xticks: 5, yticks: 3, xfmt: function (v) { return v.toFixed(0); },
        yfmt: function (v) { return v.toFixed(1); }, xlab: 'candidate threshold (lb)', ylab: 'gain'
      });
      A.plot(ctx, S, [6.05, 20.95], gainAt, P.a, 2.4);
      var bestT = 6, bestG = 0;
      for (var w = 6; w <= 21; w += .1) { var g = gainAt(w); if (g > bestG) { bestG = g; bestT = w; } }
      A.dot(ctx, S.X(bestT), S.Y(bestG), 6, P.g);
      A.txt(ctx, 'best: ≤ ' + bestT.toFixed(1) + ' lb  (gain ' + bestG.toFixed(3) + ')',
        S.X(bestT) + 10, S.Y(bestG) - 6, { size: 11.5, w: 700, fill: P.g });
      A.dot(ctx, S.X(th), S.Y(gainAt(th)), 6, P.a);
      A.txt(ctx, 'The algorithm literally tries every sensible threshold and keeps the best one.', 60, 296,
        { size: 12, w: 700, fill: P.soft });
      A.txt(ctx, 'With m examples there are only m−1 thresholds worth trying — midway between neighbouring values.',
        60, 316, { size: 11.5, fill: P.faint });
      ro.set('your threshold ' + th.toFixed(1) + ' lb  →  gain <b>' + gainAt(th).toFixed(4) + '</b>' +
        '\nbest possible threshold ' + bestT.toFixed(1) + ' lb  →  gain <b>' + bestG.toFixed(4) + '</b>' +
        '\nThis feature then competes against ear shape, face shape and whiskers on exactly this number.');
    }
    A.bind(c, render); render();
  });

})();

/* ---------- part 2 : regression trees and ensembles ---------- */
(function () {
  'use strict';

  var CATS = [
    { E: 1, F: 1, W: 1, y: 1, wt: 7.2 }, { E: 1, F: 1, W: 1, y: 1, wt: 8.8 },
    { E: 1, F: 1, W: 0, y: 1, wt: 9.2 }, { E: 1, F: 1, W: 0, y: 1, wt: 8.4 },
    { E: 1, F: 0, W: 1, y: 0, wt: 7.6 }, { E: 0, F: 0, W: 1, y: 1, wt: 10.2 },
    { E: 0, F: 1, W: 0, y: 0, wt: 15.0 }, { E: 0, F: 1, W: 0, y: 0, wt: 18.0 },
    { E: 0, F: 1, W: 0, y: 0, wt: 11.0 }, { E: 0, F: 0, W: 0, y: 0, wt: 20.0 }
  ];
  var FEAT = [
    { k: 'E', n: 'ear shape', yes: 'pointy', no: 'floppy' },
    { k: 'F', n: 'face shape', yes: 'round', no: 'not round' },
    { k: 'W', n: 'whiskers', yes: 'present', no: 'absent' }
  ];
  function mean(a) { return a.reduce(function (s, v) { return s + v; }, 0) / (a.length || 1); }
  function variance(a) { var m = mean(a); return mean(a.map(function (v) { return (v - m) * (v - m); })); }
  function splitBy(set, k) {
    return { yes: set.filter(function (e) { return e[k] === 1; }),
             no: set.filter(function (e) { return e[k] === 0; }) };
  }
  function critter(ctx, x, y, s, isCat, P) {
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
    ctx.fillStyle = isCat ? P.a : P.faint;
    ctx.beginPath(); ctx.arc(0, 0, 7, 0, 6.2832); ctx.fill();
    if (isCat) {
      ctx.beginPath(); ctx.moveTo(-6, -4); ctx.lineTo(-8, -11); ctx.lineTo(-2, -6); ctx.closePath(); ctx.fill();
      ctx.beginPath(); ctx.moveTo(6, -4); ctx.lineTo(8, -11); ctx.lineTo(2, -6); ctx.closePath(); ctx.fill();
    } else {
      ctx.beginPath(); ctx.ellipse(-6, -3, 2.6, 5, .5, 0, 6.2832); ctx.fill();
      ctx.beginPath(); ctx.ellipse(6, -3, 2.6, 5, -.5, 0, 6.2832); ctx.fill();
    }
    ctx.restore();
  }
  function rnd(i) { var v = Math.sin(i * 91.3457 + 33.11) * 19731.221; return v - Math.floor(v); }

  /* ============================================================
     8. Regression trees — predicting a number
     ============================================================ */
  A.def('regtree', function (root) {
    var c = A.canvas(root, 760, 340), ctx = c.ctx;
    var pick = 0;
    var bar = A.ctrls(root), ro = A.readout(root);
    FEAT.forEach(function (f, i) { A.button(bar, 'split on ' + f.n, function () { pick = i; sync(); render(); }); });
    function sync() { bar.querySelectorAll('button').forEach(function (b, i) { b.classList.toggle('primary', i === pick); }); }
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var all = CATS.map(function (e) { return e.wt; });
      var vAll = variance(all);
      var reds = FEAT.map(function (f) {
        var s = splitBy(CATS, f.k);
        var vy = variance(s.yes.map(function (e) { return e.wt; }));
        var vn = variance(s.no.map(function (e) { return e.wt; }));
        return vAll - (s.yes.length / 10 * vy + s.no.length / 10 * vn);
      });
      var best = 0; reds.forEach(function (r, i) { if (r > reds[best]) best = i; });
      var f = FEAT[pick], s = splitBy(CATS, f.k);
      A.txt(ctx, 'now the label is a NUMBER (weight in lb), not yes/no', 40, 34,
        { size: 13, w: 700, fill: P.soft });
      /* root */
      A.rr(ctx, 300, 50, 170, 52, 9); ctx.fillStyle = P.sunk; ctx.fill();
      ctx.strokeStyle = P.lineSoft; ctx.lineWidth = 1.4; ctx.stroke();
      A.txt(ctx, 'all 10 animals', 385, 70, { align: 'center', size: 12, w: 700, fill: P.soft });
      A.txt(ctx, 'mean ' + mean(all).toFixed(2) + ' lb  ·  var ' + vAll.toFixed(2), 385, 88,
        { align: 'center', size: 11, mono: true, fill: P.faint });
      [[s.yes, f.yes, 190], [s.no, f.no, 580]].forEach(function (br) {
        var set = br[0], x = br[2];
        var ws = set.map(function (e) { return e.wt; });
        A.line(ctx, 385, 102, x, 148, P.line, 1.8);
        A.txt(ctx, br[1], (385 + x) / 2, 128, { align: 'center', size: 11, w: 700, fill: P.faint });
        A.rr(ctx, x - 100, 148, 200, 74, 9); ctx.fillStyle = P.gS; ctx.fill();
        ctx.strokeStyle = P.g; ctx.lineWidth = 1.6; ctx.stroke();
        A.txt(ctx, ws.map(function (v) { return v.toFixed(1); }).join('  '), x, 170,
          { align: 'center', size: 11, mono: true, fill: P.soft });
        A.txt(ctx, 'predict ' + mean(ws).toFixed(2) + ' lb', x, 194,
          { align: 'center', size: 14, w: 700, fill: P.g });
        A.txt(ctx, 'variance ' + variance(ws).toFixed(2), x, 212,
          { align: 'center', size: 11, mono: true, fill: P.faint });
      });
      /* variance-reduction comparison */
      FEAT.forEach(function (ff, i) {
        var y = 244 + i * 26, on = i === pick;
        A.txt(ctx, ff.n, 190, y + 12, { align: 'right', size: 12, w: on ? 700 : 500,
          fill: i === best ? P.a : P.soft });
        A.rr(ctx, 200, y, 300, 18, 4); ctx.fillStyle = P.sunk; ctx.fill();
        A.rr(ctx, 200, y, Math.max(3, 300 * reds[i] / Math.max.apply(null, reds)), 18, 4);
        ctx.fillStyle = i === best ? P.a : P.faint; ctx.globalAlpha = on ? .9 : .5; ctx.fill(); ctx.globalAlpha = 1;
        A.txt(ctx, 'reduces variance by ' + reds[i].toFixed(2), 510, y + 13,
          { size: 11.5, mono: true, w: on ? 700 : 500, fill: i === best ? P.a : P.faint });
      });
      A.txt(ctx, 'Same algorithm as before with ONE substitution: variance replaces entropy.', 40, 328,
        { size: 12.5, w: 700, fill: P.soft });
      ro.set('Classification: choose the split with the biggest <b>reduction in entropy</b>, predict the majority class.' +
        '\nRegression: choose the split with the biggest <b>reduction in variance</b>, predict the mean.' +
        '\nEverything else — recursion, stopping rules, one-hot, thresholds — is identical.');
    }
    sync(); A.bind(c, render); render();
  });

  /* ============================================================
     9. Why one tree is fragile — use many
     ============================================================ */
  A.def('ensemble', function (root) {
    var c = A.canvas(root, 760, 320), ctx = c.ctx;
    var changed = false;
    var bar = A.ctrls(root), ro = A.readout(root);
    A.toggle(bar, 'change ONE training example', function (v) { changed = v; render(); }, false);
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var trees = [
        { root: 'ear shape', v: 1, v2: 1 },
        { root: 'whiskers', v: 1, v2: 0 },
        { root: 'face shape', v: 0, v2: 0 }
      ];
      if (changed) { trees[0].root = 'whiskers'; }
      A.txt(ctx, 'the same animal, judged by three different trees', 40, 34,
        { size: 13, w: 700, fill: P.soft });
      var votes = 0;
      trees.forEach(function (tr, i) {
        var x = 60 + i * 230, vote = changed ? tr.v2 : tr.v;
        votes += vote;
        A.rr(ctx, x, 52, 200, 150, 10); ctx.fillStyle = P.sunk; ctx.fill();
        ctx.strokeStyle = P.lineSoft; ctx.lineWidth = 1.4; ctx.stroke();
        A.txt(ctx, 'tree ' + (i + 1), x + 100, 74, { align: 'center', size: 12, w: 700, fill: P.faint });
        /* mini tree glyph */
        var rx = x + 100, ry = 100;
        A.line(ctx, rx, ry + 8, rx - 40, ry + 46, P.line, 1.6);
        A.line(ctx, rx, ry + 8, rx + 40, ry + 46, P.line, 1.6);
        A.dot(ctx, rx, ry, 9, P.p);
        A.dot(ctx, rx - 40, ry + 52, 8, vote ? P.a : P.faint);
        A.dot(ctx, rx + 40, ry + 52, 8, vote ? P.faint : P.a);
        A.txt(ctx, tr.root, rx, ry - 16, { align: 'center', size: 11, mono: true, fill: P.p });
        A.txt(ctx, vote ? 'votes CAT' : 'votes not cat', x + 100, 190,
          { align: 'center', size: 12.5, w: 700, fill: vote ? P.a : P.faint });
      });
      A.rr(ctx, 240, 218, 280, 56, 10);
      ctx.fillStyle = votes >= 2 ? P.aS : P.sunk; ctx.fill();
      ctx.strokeStyle = votes >= 2 ? P.a : P.line; ctx.lineWidth = 2; ctx.stroke();
      A.txt(ctx, votes + ' of 3 say cat  →  ' + (votes >= 2 ? 'CAT' : 'not a cat'), 380, 244,
        { align: 'center', size: 15, w: 700, fill: votes >= 2 ? P.a : P.faint });
      A.txt(ctx, 'majority vote', 380, 264, { align: 'center', size: 11, fill: P.faint });
      A.txt(ctx, changed
        ? 'ONE changed example flipped tree 1 completely — and the ensemble still gives the same answer.'
        : 'Now press the button and change a single training example.',
        40, 300, { size: 12.5, w: 700, fill: changed ? P.g : P.soft });
      ro.set('A single decision tree is <b>high variance</b>: change one example and the root split can change, ' +
        'which changes everything below it.\nAveraging many trees cancels that out. The ensemble is far more ' +
        'stable than any of its members — which is the entire idea behind the rest of this week.');
    }
    A.autoplay(root, c, render);
  });

  /* ============================================================
     10. Sampling with replacement
     ============================================================ */
  A.def('bagging', function (root) {
    var c = A.canvas(root, 760, 320), ctx = c.ctx;
    var seed = 1;
    var bar = A.ctrls(root), ro = A.readout(root);
    A.button(bar, 'draw a new bag', function () { seed++; render(); }).classList.add('primary');
    function draw() {
      var out = [];
      for (var i = 0; i < 10; i++) out.push(Math.floor(rnd(seed * 97 + i * 13) * 10));
      return out;
    }
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var picks = draw();
      var counts = new Array(10).fill(0);
      picks.forEach(function (p) { counts[p]++; });
      A.txt(ctx, 'the original training set — 10 animals', 40, 36, { size: 12.5, w: 700, fill: P.soft });
      for (var i = 0; i < 10; i++) {
        var x = 60 + i * 66;
        A.rr(ctx, x - 24, 50, 48, 54, 8);
        ctx.fillStyle = counts[i] ? P.sunk : P.rS; ctx.fill();
        ctx.strokeStyle = counts[i] ? P.lineSoft : P.r; ctx.lineWidth = counts[i] ? 1 : 1.6; ctx.stroke();
        critter(ctx, x, 72, 1.3, CATS[i].y === 1, P);
        A.txt(ctx, String(i + 1), x, 98, { align: 'center', size: 10, fill: P.faint });
        if (!counts[i]) A.txt(ctx, 'left out', x, 118, { align: 'center', size: 9.5, w: 700, fill: P.r });
      }
      A.arrow(ctx, 380, 138, 380, 164, P.line, 2);
      A.txt(ctx, 'draw 10 times, putting each one BACK each time', 400, 154, { size: 11.5, fill: P.faint });
      A.txt(ctx, 'the new bag — also 10 animals, but with repeats', 40, 190, { size: 12.5, w: 700, fill: P.soft });
      picks.forEach(function (p, i) {
        var x = 60 + i * 66;
        A.rr(ctx, x - 24, 202, 48, 54, 8);
        ctx.fillStyle = P.aS; ctx.fill(); ctx.strokeStyle = P.a; ctx.lineWidth = 1.4; ctx.stroke();
        critter(ctx, x, 224, 1.3, CATS[p].y === 1, P);
        A.txt(ctx, String(p + 1), x, 250, { align: 'center', size: 10, w: 700, fill: P.a });
      });
      var uniq = counts.filter(function (v) { return v > 0; }).length;
      A.txt(ctx, uniq + ' of the 10 originals appear; ' + (10 - uniq) + ' are missing entirely, and some appear twice or more.',
        40, 282, { size: 12.5, w: 700, fill: P.soft });
      A.txt(ctx, 'That is the point: each tree sees a slightly different world, so each tree is different.',
        40, 302, { size: 12, fill: P.faint });
      ro.set('“With replacement” means the animal goes back in the bag after being drawn, so it can be picked again.' +
        '\nOn average each bootstrap sample contains about <b>63%</b> of the distinct originals — ' +
        '1 − (1 − 1/m)<sup>m</sup> → 1 − 1/e ≈ 0.632. The ~37% left out are the “out-of-bag” examples, ' +
        'and they make a free validation set.');
    }
    A.bind(c, render); render();
  });

  /* ============================================================
     11. Random forest
     ============================================================ */
  A.def('forest', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var B = 12;
    var bar = A.ctrls(root), ro = A.readout(root);
    A.slider(bar, { label: 'trees B =', min: 1, max: 24, step: 1, value: B,
      fmt: function (v) { return v.toFixed(0); }, on: function (v) { B = v; render(); } });
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var yes = 0, i;
      for (i = 0; i < B; i++) if (rnd(i * 7 + 3) < .68) yes++;
      A.txt(ctx, 'each tree gets its own bootstrap sample AND its own random subset of features',
        40, 34, { size: 12.5, w: 700, fill: P.soft });
      for (i = 0; i < B; i++) {
        var x = 60 + (i % 8) * 84, y = 60 + Math.floor(i / 8) * 84;
        var vote = rnd(i * 7 + 3) < .68;
        A.rr(ctx, x, y, 70, 66, 8);
        ctx.fillStyle = P.sunk; ctx.fill();
        ctx.strokeStyle = vote ? P.a : P.lineSoft; ctx.lineWidth = 1.3; ctx.stroke();
        var rx = x + 35, ry = y + 20;
        A.line(ctx, rx, ry + 6, rx - 14, ry + 24, P.line, 1.3);
        A.line(ctx, rx, ry + 6, rx + 14, ry + 24, P.line, 1.3);
        A.dot(ctx, rx, ry, 5.5, P.p);
        A.dot(ctx, rx - 14, ry + 28, 5, vote ? P.a : P.faint);
        A.dot(ctx, rx + 14, ry + 28, 5, vote ? P.faint : P.a);
        A.txt(ctx, vote ? 'cat' : 'not', rx, y + 60, { align: 'center', size: 10, w: 700,
          fill: vote ? P.a : P.faint });
      }
      var ybar = 60 + Math.ceil(B / 8) * 84 + 12;
      A.txt(ctx, 'votes: ' + yes + ' cat  ·  ' + (B - yes) + ' not cat', 40, ybar + 16,
        { size: 13, w: 700, fill: P.soft });
      A.rr(ctx, 40, ybar + 26, 660, 24, 6); ctx.fillStyle = P.sunk; ctx.fill();
      A.rr(ctx, 40, ybar + 26, 660 * yes / B, 24, 6); ctx.fillStyle = P.a; ctx.globalAlpha = .8; ctx.fill();
      ctx.globalAlpha = 1;
      A.txt(ctx, 'final answer: ' + (yes * 2 > B ? 'CAT' : 'not a cat'), 40, ybar + 70,
        { size: 14, w: 700, fill: yes * 2 > B ? P.a : P.faint });
      A.txt(ctx, 'At each node it may only choose from √n randomly picked features — so the trees cannot all',
        300, ybar + 60, { size: 11.5, fill: P.faint });
      A.txt(ctx, 'agree on the same dominant split. Forced disagreement is what makes the vote worth taking.',
        300, ybar + 76, { size: 11.5, fill: P.faint });
      ro.set('for b = 1 … B:  draw a bootstrap sample  →  train a tree, choosing each split from a random ' +
        'subset of k ≈ √n features\npredict: <b>majority vote</b> (classification) or <b>average</b> (regression).' +
        '\nMore trees never hurts accuracy — it only costs compute. Past ~100 the gains flatten.');
    }
    A.bind(c, render); render();
  });

  /* ============================================================
     12. Boosting / XGBoost
     ============================================================ */
  A.def('boosting', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var round = Math.floor((t * .4) % 4);
      /* which examples each round gets wrong */
      var wrongSets = [[2, 5, 7, 9], [5, 9], [9], []];
      var weights = new Array(10).fill(1);
      for (var r = 0; r < round; r++)
        wrongSets[r].forEach(function (i) { weights[i] *= 2.2; });
      A.txt(ctx, 'round ' + (round + 1) + ' of 4', 40, 36, { size: 14, w: 700, fill: P.a });
      A.txt(ctx, 'each new tree focuses on the examples the trees so far keep getting WRONG',
        130, 36, { size: 12.5, fill: P.soft });
      for (var i = 0; i < 10; i++) {
        var x = 62 + i * 68, wgt = weights[i];
        var sz = 1.1 + Math.min(1.5, Math.log2(wgt)) * .5;
        var isWrong = round < 4 && wrongSets[round].indexOf(i) >= 0;
        A.rr(ctx, x - 28, 60, 56, 92, 8);
        ctx.fillStyle = isWrong ? P.rS : P.sunk; ctx.fill();
        ctx.strokeStyle = isWrong ? P.r : P.lineSoft; ctx.lineWidth = isWrong ? 2 : 1; ctx.stroke();
        critter(ctx, x, 100, sz, CATS[i].y === 1, P);
        A.txt(ctx, '×' + wgt.toFixed(1), x, 140, { align: 'center', size: 10.5, mono: true, w: 700,
          fill: wgt > 1.5 ? P.r : P.faint });
        if (isWrong) A.txt(ctx, 'wrong', x, 170, { align: 'center', size: 10, w: 700, fill: P.r });
      }
      A.txt(ctx, 'attention weight', 40, 140, { align: 'right', size: 10.5, fill: P.faint });
      /* the growing chain of trees */
      for (var k = 0; k <= round; k++) {
        var tx = 90 + k * 170;
        A.rr(ctx, tx - 60, 196, 120, 62, 9);
        ctx.fillStyle = k === round ? P.aS : P.sunk; ctx.fill();
        ctx.strokeStyle = k === round ? P.a : P.lineSoft; ctx.lineWidth = k === round ? 2 : 1.2; ctx.stroke();
        A.txt(ctx, 'tree ' + (k + 1), tx, 216, { align: 'center', size: 11.5, w: 700,
          fill: k === round ? P.a : P.faint });
        A.dot(ctx, tx, 236, 6, k === round ? P.a : P.faint);
        A.line(ctx, tx, 240, tx - 16, 252, k === round ? P.a : P.line, 1.4);
        A.line(ctx, tx, 240, tx + 16, 252, k === round ? P.a : P.line, 1.4);
        if (k < round) A.arrow(ctx, tx + 62, 227, tx + 106, 227, P.a, 1.8);
      }
      A.txt(ctx, 'Random forest: every tree sees a random sample. Boosting: every tree sees a DELIBERATE sample —',
        40, 288, { size: 12, fill: P.soft });
      A.txt(ctx, 'the hard cases. Like a student re-doing only the questions they got wrong.', 40, 306,
        { size: 12, w: 700, fill: P.a });
      A.txt(ctx, 'XGBoost adds built-in regularisation, clever stopping rules and a very fast implementation.',
        40, 324, { size: 11.5, fill: P.faint });
    }
    A.autoplay(root, c, render);
  });

  /* ============================================================
     13. Trees vs neural networks
     ============================================================ */
  A.def('treevsnn', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var rows = [
      ['tabular / structured data (spreadsheets)', 1, 'trees usually win, and train in seconds'],
      ['images, audio, text', 0, 'neural networks, no contest'],
      ['fast to train', 1, 'often minutes vs hours'],
      ['works on raw pixels', 0, 'trees have no notion of “nearby”'],
      ['easy to explain to a human', 1, 'a small tree is literally a flowchart'],
      ['transfer learning available', 0, 'you cannot pre-train a tree'],
      ['chains into a bigger system', 0, 'networks stack; trees do not']
    ];
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var hot = Math.floor((t * .55) % rows.length);
      A.txt(ctx, 'DECISION TREES', 220, 40, { align: 'center', size: 14, w: 700, fill: P.g });
      A.txt(ctx, 'NEURAL NETWORKS', 600, 40, { align: 'center', size: 14, w: 700, fill: P.b });
      rows.forEach(function (r, i) {
        var y = 58 + i * 34, on = i === hot, tree = r[1] === 1;
        A.rr(ctx, 40, y, 680, 30, 6);
        ctx.fillStyle = on ? (tree ? P.gS : P.bS) : P.sunk; ctx.fill();
        ctx.strokeStyle = on ? (tree ? P.g : P.b) : P.lineSoft; ctx.lineWidth = on ? 1.8 : 1; ctx.stroke();
        A.txt(ctx, r[0], 330, y + 20, { align: 'center', size: 12, w: on ? 700 : 500,
          fill: on ? (tree ? P.g : P.b) : P.soft });
        A.txt(ctx, tree ? '✓' : '·', 120, y + 21, { align: 'center', size: 16, w: 700,
          fill: tree ? P.g : P.faint });
        A.txt(ctx, tree ? '·' : '✓', 560, y + 21, { align: 'center', size: 16, w: 700,
          fill: tree ? P.faint : P.b });
        if (on) A.txt(ctx, r[2], 640, y + 20, { align: 'center', size: 10.5, fill: P.faint });
      });
      A.txt(ctx, 'On a spreadsheet of numbers and categories, try XGBoost FIRST. It is fast, it needs almost',
        40, 306, { size: 12, fill: P.soft });
      A.txt(ctx, 'no tuning, and it is still the thing to beat on most tabular problems.', 40, 324,
        { size: 12, w: 700, fill: P.g });
    }
    A.autoplay(root, c, render);
  });

})();
