/* Widgets for Foundations / Week 2 — Python, NumPy and pandas */
(function () {
  'use strict';

  function codeBox(ctx, P, x, y, w, lines, hot) {
    A.rr(ctx, x, y, w, lines.length * 19 + 16, 8);
    ctx.fillStyle = P.sunk; ctx.fill();
    ctx.strokeStyle = P.lineSoft; ctx.lineWidth = 1; ctx.stroke();
    lines.forEach(function (l, i) {
      var on = i === hot;
      if (on) {
        A.rr(ctx, x + 4, y + 6 + i * 19, w - 8, 18, 4);
        ctx.fillStyle = P.aS; ctx.fill();
      }
      A.txt(ctx, l, x + 12, y + 20 + i * 19,
        { size: 11.5, mono: true, w: on ? 700 : 500, fill: on ? P.a : P.soft });
    });
  }

  /* ============================================================
     1. Jupyter cells
     ============================================================ */
  A.def('fjupyter', function (root) {
    var c = A.canvas(root, 760, 320), ctx = c.ctx;
    var ro = A.readout(root);
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var step = Math.floor((t * .5) % 4);
      var cells = [
        ['x = 5', '', 'nothing printed — it just stored it'],
        ['x + 3', '8', 'the LAST line of a cell is shown automatically'],
        ['print(x)\nprint(x * 2)', '5\n10', 'print() shows things whenever you ask'],
        ['import numpy as np\nnp.array([1, 2, 3])', 'array([1, 2, 3])', 'libraries are imported once, at the top']
      ];
      var cur = cells[step];
      A.txt(ctx, 'A notebook is a stack of little boxes. You run them one at a time,', 40, 40,
        { size: 12.5, w: 700, fill: P.soft });
      A.txt(ctx, 'and each one remembers what the ones before it did.', 40, 60,
        { size: 12.5, w: 700, fill: P.soft });
      for (var i = 0; i < 4; i++) {
        var y = 84 + i * 54, on = i === step, past = i < step;
        A.txt(ctx, past || on ? 'In [' + (i + 1) + ']:' : 'In [ ]:', 40, y + 22,
          { size: 11.5, mono: true, w: 700, fill: on ? P.a : past ? P.faint : P.line });
        A.rr(ctx, 108, y, 340, 40, 6);
        ctx.fillStyle = on ? P.aS : P.sunk; ctx.fill();
        ctx.strokeStyle = on ? P.a : P.lineSoft; ctx.lineWidth = on ? 2 : 1; ctx.stroke();
        cells[i][0].split('\n').forEach(function (l, q) {
          A.txt(ctx, l, 120, y + (cells[i][0].indexOf('\n') > -1 ? 17 : 25) + q * 15,
            { size: 11.5, mono: true, fill: on ? P.a : P.soft });
        });
        if (past || on) {
          A.txt(ctx, cells[i][1] ? 'Out[' + (i + 1) + ']:' : '', 468, y + 22,
            { size: 11.5, mono: true, fill: P.faint });
          cells[i][1].split('\n').forEach(function (l, q) {
            A.txt(ctx, l, 530, y + (cells[i][1].indexOf('\n') > -1 ? 17 : 25) + q * 15,
              { size: 11.5, mono: true, w: 700, fill: P.g });
          });
        }
      }
      A.txt(ctx, cur[2], 40, 302, { size: 12, w: 700, fill: P.a });
      ro.set('<b>Shift + Enter</b> runs a cell and moves to the next. That is 95% of using Jupyter.' +
        '\nThe number in <code>In [3]</code> is the ORDER you ran things, not the position on the page — ' +
        'so if you run cells out of order, results can surprise you. <b>Restart &amp; Run All</b> is the ' +
        'cure when things get strange.');
    }
    A.autoplay(root, c, render);
  });

  /* ============================================================
     2. Types
     ============================================================ */
  A.def('ftypes', function (root) {
    var c = A.canvas(root, 760, 320), ctx = c.ctx;
    var T = [
      ['5', 'int', 'a whole number', 'P.b'],
      ['5.0', 'float', 'a decimal number — what ML uses everywhere', 'P.a'],
      ['"cat"', 'str', 'text, in quotes', 'P.g'],
      ['True', 'bool', 'yes or no. Capital T, capital F', 'P.p'],
      ['[1, 2, 3]', 'list', 'several things in order, in square brackets', 'P.m'],
      ['None', 'NoneType', 'deliberately nothing', 'P.faint']
    ];
    var ro = A.readout(root);
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var cols = { 'P.b': P.b, 'P.a': P.a, 'P.g': P.g, 'P.p': P.p, 'P.m': P.m, 'P.faint': P.faint };
      var hot = Math.floor((t * .6) % T.length);
      A.txt(ctx, 'Every value in Python has a TYPE, and the type decides what you can do with it.',
        40, 44, { size: 13, w: 700, fill: P.soft });
      T.forEach(function (r, i) {
        var y = 66 + i * 36, on = i === hot, col = cols[r[3]];
        A.rr(ctx, 40, y, 680, 31, 6);
        ctx.fillStyle = on ? P.sunk : 'transparent'; ctx.fill();
        ctx.strokeStyle = on ? col : P.lineSoft; ctx.lineWidth = on ? 1.8 : 1; ctx.stroke();
        A.txt(ctx, r[0], 58, y + 21, { size: 13.5, mono: true, w: 700, fill: on ? col : P.soft });
        A.txt(ctx, r[1], 200, y + 21, { size: 12.5, mono: true, w: 700, fill: col });
        A.txt(ctx, r[2], 300, y + 21, { size: 11.5, fill: P.faint });
      });
      A.txt(ctx, 'type(x) tells you which one you have. A very useful thing to print when confused.',
        40, 292, { size: 12, w: 700, fill: P.a });
      A.txt(ctx, 'Careful: "5" (text) and 5 (number) look identical on screen and behave nothing alike.',
        40, 314, { size: 12, fill: P.r });
      ro.set('<code>type(5)</code> → <code>&lt;class \'int\'&gt;</code>  ·  ' +
        '<code>type(5.0)</code> → <code>&lt;class \'float\'&gt;</code>' +
        '\n<code>"5" + "5"</code> gives <code>"55"</code>. <code>5 + 5</code> gives <code>10</code>. ' +
        'Same keystrokes, very different answer.');
    }
    A.autoplay(root, c, render);
  });

  /* ============================================================
     3. Lists vs NumPy arrays
     ============================================================ */
  A.def('flistarray', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var ro = A.readout(root);
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var step = Math.floor((t * .45) % 3);
      var ops = [
        ['x * 2', '[1, 2, 3, 1, 2, 3]', 'array([2, 4, 6])', 'repeats the list', 'doubles each number'],
        ['x + 10', 'TypeError!', 'array([11, 12, 13])', 'cannot add a number to a list', 'adds 10 to each'],
        ['x + y', '[1, 2, 3, 4, 5, 6]', 'array([5, 7, 9])', 'glues them end to end', 'adds them pairwise']
      ];
      var op = ops[step];
      A.txt(ctx, 'x = [1, 2, 3]', 130, 48, { align: 'center', size: 13, mono: true, w: 700, fill: P.faint });
      A.txt(ctx, 'x = np.array([1, 2, 3])', 520, 48, { align: 'center', size: 13, mono: true, w: 700, fill: P.g });
      [['a plain Python list', 60, 200, P.faint], ['a NumPy array', 400, 240, P.g]].forEach(function (pn) {
        A.rr(ctx, pn[1], 62, pn[2], 200, 10);
        ctx.fillStyle = pn[3] === P.g ? P.gS : P.sunk; ctx.fill();
        ctx.strokeStyle = pn[3]; ctx.lineWidth = 1.8; ctx.stroke();
        A.txt(ctx, pn[0], pn[1] + pn[2] / 2, 84, { align: 'center', size: 12, w: 700, fill: pn[3] });
      });
      A.txt(ctx, op[0], 380, 128, { align: 'center', size: 18, mono: true, w: 700, fill: P.a });
      A.txt(ctx, op[1], 160, 176, { align: 'center', size: 13, mono: true, w: 700,
        fill: op[1].indexOf('Error') > -1 ? P.r : P.soft });
      A.txt(ctx, op[3], 160, 202, { align: 'center', size: 10.5, fill: P.faint });
      A.txt(ctx, op[2], 520, 176, { align: 'center', size: 13, mono: true, w: 700, fill: P.g });
      A.txt(ctx, op[4], 520, 202, { align: 'center', size: 10.5, fill: P.g });
      A.txt(ctx, 'They look identical. They behave nothing alike — and Python does not warn you.',
        60, 292, { size: 12.5, w: 700, fill: P.r });
      A.txt(ctx, 'For maths you always want the array. np.array(my_list) converts one.', 60, 314,
        { size: 12, w: 700, fill: P.g });
      ro.set('A <b>list</b> is a general container — it can hold anything, and + means “join”.' +
        '\nA <b>NumPy array</b> is a maths object — all one type, and + means “add the numbers”.' +
        '\nThis single difference is behind a large share of beginner confusion.');
    }
    A.autoplay(root, c, render);
  });

  /* ============================================================
     4. Indexing and slicing
     ============================================================ */
  A.def('fslice', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var which = 0;
    var vals = [10, 20, 30, 40, 50, 60];
    var ops = [
      ['x[0]', function (i) { return i === 0; }, '10', 'the FIRST one. Counting starts at zero'],
      ['x[2]', function (i) { return i === 2; }, '30', 'the third one'],
      ['x[-1]', function (i) { return i === 5; }, '60', 'minus counts back from the end'],
      ['x[1:4]', function (i) { return i >= 1 && i < 4; }, '[20, 30, 40]', 'from 1 UP TO but NOT including 4'],
      ['x[:3]', function (i) { return i < 3; }, '[10, 20, 30]', 'from the start'],
      ['x[3:]', function (i) { return i >= 3; }, '[40, 50, 60]', 'to the end'],
      ['x[:]', function () { return true; }, '[10,20,30,40,50,60]', 'everything — the colon alone means “all”']
    ];
    var bar = A.ctrls(root), ro = A.readout(root);
    ops.forEach(function (o, i) { A.button(bar, o[0], function () { which = i; sync(); render(); }); });
    function sync() { bar.querySelectorAll('button').forEach(function (b, i) { b.classList.toggle('primary', i === which); }); }
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var op = ops[which];
      A.txt(ctx, 'x = np.array([10, 20, 30, 40, 50, 60])', 40, 46,
        { size: 13.5, mono: true, w: 700, fill: P.soft });
      vals.forEach(function (v, i) {
        var x = 60 + i * 108, on = op[1](i);
        A.rr(ctx, x, 74, 90, 58, 8);
        ctx.fillStyle = on ? P.aS : P.sunk; ctx.fill();
        ctx.strokeStyle = on ? P.a : P.lineSoft; ctx.lineWidth = on ? 2.4 : 1; ctx.stroke();
        A.txt(ctx, String(v), x + 45, 112, { align: 'center', size: 20, mono: true, w: 700,
          fill: on ? P.a : P.soft });
        A.txt(ctx, String(i), x + 45, 150, { align: 'center', size: 12, mono: true,
          w: 700, fill: on ? P.a : P.faint });
        A.txt(ctx, String(i - 6), x + 45, 168, { align: 'center', size: 10.5, fill: P.faint });
      });
      A.txt(ctx, 'index →', 20, 150, { align: 'right', size: 10.5, fill: P.faint });
      A.txt(ctx, 'or →', 20, 168, { align: 'right', size: 10.5, fill: P.faint });
      A.txt(ctx, op[0], 60, 210, { size: 22, mono: true, w: 700, fill: P.a });
      A.txt(ctx, '→  ' + op[2], 200, 210, { size: 18, mono: true, w: 700, fill: P.g });
      A.txt(ctx, op[3], 60, 238, { size: 12.5, fill: P.faint });
      A.txt(ctx, 'The rule everyone trips on: x[1:4] gives you 1, 2, 3 — it STOPS BEFORE 4.',
        40, 278, { size: 12.5, w: 700, fill: P.r });
      A.txt(ctx, 'Handy consequence: the number of items you get is just (end − start).', 40, 300,
        { size: 12, fill: P.faint });
      A.txt(ctx, 'For 2-D: M[row, col].  M[1, :] is all of row 1.  M[:, 2] is all of column 2.',
        40, 322, { size: 12, mono: true, w: 700, fill: P.b });
      ro.set('<code>x[start:stop]</code> — start is included, stop is <b>not</b>.' +
        '\nLeave one out and it means “from the beginning” or “to the end”. The bare colon ' +
        '<code>:</code> means “everything in this direction”, which is why <code>W[:, j]</code> reads ' +
        'as “every row, column j”.');
    }
    sync(); A.bind(c, render); render();
  });

  /* ============================================================
     5. Shape and axis
     ============================================================ */
  A.def('fshape', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var ro = A.readout(root);
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var ax = Math.floor((t * .35) % 2);
      var M = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]];
      var x0 = 130, y0 = 96, cw = 60, ch = 46;
      A.matrix(ctx, x0, y0, 3, 4, cw, ch, P, function (i, j) { return String(M[i][j]); },
        { state: function (i, j) { return ax === 0 ? (j === 1 ? 1 : 0) : (i === 1 ? 2 : 0); },
          size: 13, shape: 'shape = (3, 4)' });
      /* axis arrows */
      A.arrow(ctx, x0 - 26, y0 - 6, x0 - 26, y0 + 3 * ch - 10, ax === 0 ? P.a : P.line, ax === 0 ? 2.6 : 1.4);
      ctx.save(); ctx.translate(x0 - 42, y0 + 3 * ch / 2); ctx.rotate(-Math.PI / 2);
      A.txt(ctx, 'axis 0 — down the rows', 0, 0, { align: 'center', size: 11, w: 700,
        fill: ax === 0 ? P.a : P.faint }); ctx.restore();
      A.arrow(ctx, x0, y0 - 26, x0 + 4 * cw - 12, y0 - 26, ax === 1 ? P.b : P.line, ax === 1 ? 2.6 : 1.4);
      A.txt(ctx, 'axis 1 — across the columns', x0 + 4 * cw / 2, y0 - 34,
        { align: 'center', size: 11, w: 700, fill: ax === 1 ? P.b : P.faint });
      /* the results */
      var mx = 430;
      A.txt(ctx, 'M.shape → (3, 4)', mx, 76, { size: 14, mono: true, w: 700, fill: P.soft });
      A.txt(ctx, '3 rows, 4 columns. Always that order.', mx, 96, { size: 10.5, fill: P.faint });
      A.txt(ctx, ax === 0 ? 'M.sum(axis=0)' : 'M.sum(axis=1)', mx, 136,
        { size: 15, mono: true, w: 700, fill: ax === 0 ? P.a : P.b });
      A.txt(ctx, ax === 0 ? '→ array([15, 18, 21, 24])' : '→ array([10, 26, 42])', mx, 162,
        { size: 13, mono: true, w: 700, fill: P.g });
      A.txt(ctx, ax === 0 ? 'one answer per COLUMN — 4 of them' : 'one answer per ROW — 3 of them',
        mx, 184, { size: 11, fill: P.faint });
      A.txt(ctx, 'the trick that makes axis click', mx, 218, { size: 12, w: 700, fill: P.a });
      A.txt(ctx, 'axis = the direction that gets', mx, 240, { size: 11.5, fill: P.soft });
      A.txt(ctx, 'COLLAPSED and disappears.', mx, 258, { size: 11.5, w: 700, fill: P.a });
      A.txt(ctx, '(3,4) with axis=0 → (4,)', mx, 282, { size: 11, mono: true, fill: P.faint });
      A.txt(ctx, '(3,4) with axis=1 → (3,)', mx, 300, { size: 11, mono: true, fill: P.faint });
      A.txt(ctx, 'Print .shape constantly while you are learning. It is free and it answers most questions.',
        40, 322, { size: 12, w: 700, fill: P.g });
      ro.set('<code>M.shape</code> · <code>M.ndim</code> (how many dimensions) · <code>M.size</code> ' +
        '(total numbers)' +
        '\nMost NumPy confusion is shape confusion. When something behaves oddly, print the shape of ' +
        'every array involved — the wrong one is usually obvious immediately.');
    }
    A.autoplay(root, c, render);
  });

  /* ============================================================
     6. Creating arrays
     ============================================================ */
  A.def('fcreate', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var which = 0;
    var makers = [
      ['np.zeros(5)', [0, 0, 0, 0, 0], 'five zeros — an empty box to fill in later'],
      ['np.ones(5)', [1, 1, 1, 1, 1], 'five ones'],
      ['np.arange(5)', [0, 1, 2, 3, 4], 'count from 0, stop BEFORE 5'],
      ['np.arange(2, 7)', [2, 3, 4, 5, 6], 'count from 2, stop before 7'],
      ['np.linspace(0, 1, 5)', [0, 0.25, 0.5, 0.75, 1], 'five points evenly spread from 0 to 1 — ends INCLUDED'],
      ['np.zeros((2, 3))', null, 'a 2×3 grid of zeros — note the DOUBLE brackets']
    ];
    var bar = A.ctrls(root), ro = A.readout(root);
    makers.forEach(function (m, i) { A.button(bar, m[0].replace('np.', ''), function () { which = i; sync(); render(); }); });
    function sync() { bar.querySelectorAll('button').forEach(function (b, i) { b.classList.toggle('primary', i === which); }); }
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var m = makers[which];
      A.txt(ctx, m[0], 40, 56, { size: 20, mono: true, w: 700, fill: P.a });
      A.arrow(ctx, 40, 76, 90, 76, P.line, 2);
      if (m[1]) {
        m[1].forEach(function (v, i) {
          var x = 60 + i * 110;
          A.rr(ctx, x, 108, 92, 56, 8);
          ctx.fillStyle = P.aS; ctx.fill(); ctx.strokeStyle = P.a; ctx.lineWidth = 1.8; ctx.stroke();
          A.txt(ctx, String(v), x + 46, 144, { align: 'center', size: 18, mono: true, w: 700, fill: P.a });
        });
        A.txt(ctx, 'shape = (5,)', 60, 190, { size: 12.5, mono: true, fill: P.faint });
      } else {
        for (var i = 0; i < 2; i++) for (var j = 0; j < 3; j++) {
          var x = 60 + j * 92, y = 104 + i * 52;
          A.rr(ctx, x, y, 84, 44, 7);
          ctx.fillStyle = P.aS; ctx.fill(); ctx.strokeStyle = P.a; ctx.lineWidth = 1.8; ctx.stroke();
          A.txt(ctx, '0', x + 42, y + 29, { align: 'center', size: 17, mono: true, w: 700, fill: P.a });
        }
        A.txt(ctx, 'shape = (2, 3)', 60, 222, { size: 12.5, mono: true, fill: P.faint });
        A.txt(ctx, 'the extra brackets are the shape TUPLE — one argument, not two', 200, 222,
          { size: 11, w: 700, fill: P.r });
      }
      A.txt(ctx, m[2], 40, 258, { size: 13, w: 700, fill: P.soft });
      A.txt(ctx, 'arange stops BEFORE the number. linspace INCLUDES both ends. Nobody remembers this;',
        40, 296, { size: 12, fill: P.faint });
      A.txt(ctx, 'everybody looks it up. Knowing that they differ is the useful part.', 40, 318,
        { size: 12, w: 700, fill: P.a });
      ro.set('Also worth knowing: <code>np.full((2,3), 7)</code> fills with a value, ' +
        '<code>np.eye(3)</code> makes an identity matrix, <code>np.random.rand(3)</code> makes random ' +
        'numbers, <code>np.random.seed(1)</code> makes “random” repeatable — which you want in any ' +
        'experiment you might need to explain later.');
    }
    sync(); A.bind(c, render); render();
  });

  /* ============================================================
     7. Elementwise arithmetic
     ============================================================ */
  A.def('felementwise', function (root) {
    var c = A.canvas(root, 760, 300), ctx = c.ctx;
    var op = 0;
    var A1 = [1, 2, 3, 4], B1 = [10, 20, 30, 40];
    var ops = [['a + b', function (x, y) { return x + y; }],
               ['a - b', function (x, y) { return x - y; }],
               ['a * b', function (x, y) { return x * y; }],
               ['a / b', function (x, y) { return x / y; }],
               ['a ** 2', function (x) { return x * x; }],
               ['np.sqrt(a)', function (x) { return Math.sqrt(x); }]];
    var bar = A.ctrls(root), ro = A.readout(root);
    ops.forEach(function (o, i) { A.button(bar, o[0], function () { op = i; sync(); render(); }); });
    function sync() { bar.querySelectorAll('button').forEach(function (b, i) { b.classList.toggle('primary', i === op); }); }
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var hot = Math.floor((t * 1.1) % 4);
      var single = op >= 4;
      A.matrix(ctx, 90, 66, 1, 4, 74, 44, P, function (i, j) { return String(A1[j]); },
        { state: function (i, j) { return j === hot ? 1 : 0; }, label: 'a', size: 14 });
      if (!single) {
        A.matrix(ctx, 90, 134, 1, 4, 74, 44, P, function (i, j) { return String(B1[j]); },
          { state: function (i, j) { return j === hot ? 1 : 0; }, label: 'b', size: 14 });
      }
      A.txt(ctx, ops[op][0], 200, 210, { align: 'center', size: 17, mono: true, w: 700, fill: P.a });
      A.arrow(ctx, 400, 120, 450, 120, P.line, 2);
      var res = A1.map(function (v, i) { return ops[op][1](v, B1[i]); });
      A.matrix(ctx, 470, 98, 1, 4, 66, 44, P,
        function (i, j) { return res[j] % 1 === 0 ? String(res[j]) : res[j].toFixed(2); },
        { state: function (i, j) { return j === hot ? 3 : 0; }, label: 'result', size: 12 });
      A.txt(ctx, 'position ' + hot + ' with position ' + hot + ', kept separate', 470, 176,
        { size: 11, fill: P.faint });
      A.txt(ctx, 'Elementwise means: line them up and do the sum position by position.', 60, 246,
        { size: 12.5, w: 700, fill: P.soft });
      A.txt(ctx, 'The result is the SAME LENGTH as what you started with — nothing gets added up.',
        60, 268, { size: 12, fill: P.faint });
      A.txt(ctx, 'That is the difference from a dot product, which collapses everything into one number.',
        60, 290, { size: 12, w: 700, fill: P.a });
      ro.set('Every arithmetic operator works this way on arrays, and so do <code>np.sqrt</code>, ' +
        '<code>np.exp</code>, <code>np.log</code>, <code>np.abs</code> — they apply to every entry.' +
        '\nThis is why <code>sigmoid(Z)</code> works on a whole matrix at once with no loop: ' +
        '<code>1 / (1 + np.exp(-Z))</code> just does it to every number.');
    }
    sync();
    A.autoplay(root, c, render);
  });

  /* ============================================================
     8. Broadcasting
     ============================================================ */
  A.def('fbroadcast', function (root) {
    var c = A.canvas(root, 760, 340), ctx = c.ctx;
    var ro = A.readout(root);
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var ph = A.clamp(((t * .4) % 3) - .3, 0, 1), e = A.ease(ph);
      var M = [[1, 2, 3], [4, 5, 6]];
      var b = [10, 20, 30];
      A.matrix(ctx, 60, 96, 2, 3, 58, 44, P, function (i, j) { return String(M[i][j]); },
        { state: function () { return 2; }, label: 'Z   shape (2, 3)', size: 13 });
      A.txt(ctx, '+', 250, 132, { align: 'center', size: 22, fill: P.faint });
      /* the bias row, copied downwards as the animation runs */
      A.matrix(ctx, 280, 96, 1, 3, 58, 44, P, function (i, j) { return String(b[j]); },
        { state: function () { return 1; }, label: 'b   shape (1, 3)', size: 13 });
      if (e > .15) {
        ctx.save(); ctx.globalAlpha = A.clamp((e - .15) * 2, 0, .85);
        A.matrix(ctx, 280, 96 + 44, 1, 3, 58, 44, P, function (i, j) { return String(b[j]); },
          { state: function () { return 1; }, size: 13 });
        ctx.restore();
        A.txt(ctx, 'copied ↓', 280 + 88, 96 + 44 + 62, { align: 'center', size: 10.5, fill: P.a });
      }
      A.txt(ctx, '=', 470, 132, { align: 'center', size: 22, fill: P.faint });
      A.matrix(ctx, 500, 96, 2, 3, 62, 44, P,
        function (i, j) { return e > .55 ? String(M[i][j] + b[j]) : ''; },
        { state: function () { return e > .55 ? 3 : 0; }, label: 'shape (2, 3)', size: 13 });
      A.txt(ctx, 'The shapes do not match — and NumPy does it anyway.', 60, 46,
        { size: 13, w: 700, fill: P.soft });
      A.txt(ctx, 'It quietly STRETCHES the smaller one to fit. That is broadcasting.', 60, 66,
        { size: 12.5, fill: P.faint });
      A.txt(ctx, 'the rule, read right to left', 60, 236, { size: 12, w: 700, fill: P.a });
      A.txt(ctx, '(2, 3)  and  (1, 3)  →  last dims 3 = 3 ✓, then 2 vs 1 → the 1 gets stretched ✓',
        60, 258, { size: 12, mono: true, fill: P.soft });
      A.txt(ctx, 'Dimensions match if they are EQUAL, or one of them is 1.', 60, 280,
        { size: 12, w: 700, fill: P.g });
      A.txt(ctx, 'This is why  Z = np.matmul(A, W) + b  works with b as a single row: it gets added to',
        60, 306, { size: 11.5, fill: P.faint });
      A.txt(ctx, 'every row for you, with no loop and no copying in memory.', 60, 326,
        { size: 11.5, fill: P.faint });
      ro.set('Broadcasting is helpful right up until it is not. A (3,1) where you meant (1,3) can ' +
        'silently produce a <b>bigger, wrong</b> array instead of an error.' +
        '\nWhen a result has a surprising shape, that is almost always what happened. Print the shapes.');
    }
    A.autoplay(root, c, render);
  });

})();

/* ---------- part 2 : dot in code, axes, masks, reshape, pandas, errors ---------- */
(function () {
  'use strict';

  /* ============================================================
     9. np.dot, matmul and @
     ============================================================ */
  A.def('fdotcode', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var which = 0;
    var ops = [
      ['a * b', 'elementwise', 'array([4, 10, 18])', 'same length out. Nothing added up', false],
      ['(a * b).sum()', 'elementwise, then add', '32', 'the long way round to a dot product', true],
      ['np.dot(a, b)', 'the dot product', '32', 'the usual way for two vectors', true],
      ['a @ b', 'the @ operator', '32', 'the modern shorthand. Same thing', true],
      ['np.matmul(A, B)', 'matrix multiply', 'a whole grid', 'for 2-D. Use this, not np.dot, for matrices', true]
    ];
    var bar = A.ctrls(root), ro = A.readout(root);
    ops.forEach(function (o, i) { A.button(bar, o[0], function () { which = i; sync(); render(); }); });
    function sync() { bar.querySelectorAll('button').forEach(function (b, i) { b.classList.toggle('primary', i === which); }); }
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var a = [1, 2, 3], b = [4, 5, 6], o = ops[which];
      A.txt(ctx, 'a = np.array([1, 2, 3])      b = np.array([4, 5, 6])', 40, 46,
        { size: 13, mono: true, w: 700, fill: P.soft });
      A.matrix(ctx, 70, 78, 1, 3, 70, 42, P, function (i, j) { return String(a[j]); },
        { state: function () { return 2; }, label: 'a', size: 14 });
      A.matrix(ctx, 70, 148, 1, 3, 70, 42, P, function (i, j) { return String(b[j]); },
        { state: function () { return 2; }, label: 'b', size: 14 });
      A.txt(ctx, o[0], 330, 100, { size: 19, mono: true, w: 700, fill: P.a });
      A.txt(ctx, o[1], 330, 124, { size: 11.5, fill: P.faint });
      A.arrow(ctx, 330, 140, 400, 140, P.line, 2);
      if (!o[4]) {
        A.matrix(ctx, 330, 158, 1, 3, 66, 42, P,
          function (i, j) { return String(a[j] * b[j]); },
          { state: function () { return 1; }, size: 13 });
      } else {
        A.rr(ctx, 330, 158, 150, 50, 9);
        ctx.fillStyle = P.gS; ctx.fill(); ctx.strokeStyle = P.g; ctx.lineWidth = 2; ctx.stroke();
        A.txt(ctx, o[2], 405, 190, { align: 'center', size: 20, mono: true, w: 700, fill: P.g });
      }
      A.txt(ctx, o[3], 330, 230, { size: 12, w: 700, fill: P.a });
      /* the mental model */
      A.txt(ctx, 'one number out?', 560, 88, { size: 12, w: 700, fill: P.soft });
      A.txt(ctx, o[4] ? '✓ yes — it collapsed' : '✗ no — same length', 560, 110,
        { size: 12.5, w: 700, fill: o[4] ? P.g : P.r });
      A.txt(ctx, 'The one rule: * keeps things separate.', 40, 268, { size: 12.5, w: 700, fill: P.soft });
      A.txt(ctx, 'dot / @ / matmul multiply AND add, so they collapse.', 40, 290,
        { size: 12.5, w: 700, fill: P.soft });
      A.txt(ctx, 'Using * where you meant @ is a silent, expensive bug — it runs and gives wrong numbers.',
        40, 316, { size: 12, w: 700, fill: P.r });
      ro.set('For 1-D vectors <code>np.dot</code> and <code>@</code> are the same. For 2-D matrices ' +
        'prefer <code>@</code> or <code>np.matmul</code> — <code>np.dot</code> behaves differently once ' +
        'you go past 2 dimensions, which is a nasty surprise to find later.');
    }
    sync(); A.bind(c, render); render();
  });

  /* ============================================================
     10. Aggregating along an axis
     ============================================================ */
  A.def('faxis', function (root) {
    var c = A.canvas(root, 760, 340), ctx = c.ctx;
    var fn = 0, ax = 2;
    var fns = [['sum', function (a) { return a.reduce(function (x, y) { return x + y; }, 0); }],
               ['mean', function (a) { return a.reduce(function (x, y) { return x + y; }, 0) / a.length; }],
               ['max', function (a) { return Math.max.apply(null, a); }]];
    var bar = A.ctrls(root), ro = A.readout(root);
    fns.forEach(function (f, i) { A.button(bar, 'M.' + f[0] + '()', function () { fn = i; sync(); render(); }); });
    ['no axis', 'axis=0', 'axis=1'].forEach(function (n, i) {
      A.button(bar, n, function () { ax = i === 0 ? 2 : i - 1; sync(); render(); });
    });
    function sync() {
      var bs = bar.querySelectorAll('button');
      for (var i = 0; i < 3; i++) bs[i].classList.toggle('primary', i === fn);
      bs[3].classList.toggle('primary', ax === 2);
      bs[4].classList.toggle('primary', ax === 0);
      bs[5].classList.toggle('primary', ax === 1);
    }
    var M = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]];
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var f = fns[fn][1];
      var x0 = 110, y0 = 100, cw = 58, ch = 44;
      A.matrix(ctx, x0, y0, 3, 4, cw, ch, P, function (i, j) { return String(M[i][j]); },
        { state: function (i, j) { return ax === 2 ? 1 : ax === 0 ? (j === 1 ? 1 : 0) : (i === 1 ? 2 : 0); },
          size: 13, label: 'M   shape (3, 4)' });
      var out, lbl, shape;
      if (ax === 2) {
        out = [f([].concat.apply([], M))]; lbl = 'one number for the whole thing'; shape = '()';
      } else if (ax === 0) {
        out = [0, 1, 2, 3].map(function (j) { return f(M.map(function (r) { return r[j]; })); });
        lbl = 'one per COLUMN — the rows collapsed'; shape = '(4,)';
      } else {
        out = M.map(function (r) { return f(r); });
        lbl = 'one per ROW — the columns collapsed'; shape = '(3,)';
      }
      A.txt(ctx, 'M.' + fns[fn][0] + '(' + (ax === 2 ? '' : 'axis=' + ax) + ')', x0 + 120, 66,
        { align: 'center', size: 16, mono: true, w: 700, fill: P.a });
      A.arrow(ctx, 390, 150, 440, 150, P.line, 2);
      var vals = out.map(function (v) { return v % 1 === 0 ? String(v) : v.toFixed(2); });
      if (ax === 0) A.matrix(ctx, 460, 128, 1, 4, 60, 44, P, function (i, j) { return vals[j]; },
        { state: function () { return 3; }, size: 12, shape: 'shape ' + shape });
      else if (ax === 1) A.matrix(ctx, 500, 90, 3, 1, 70, 44, P, function (i) { return vals[i]; },
        { state: function () { return 3; }, size: 12, shape: 'shape ' + shape });
      else {
        A.rr(ctx, 480, 128, 110, 46, 8);
        ctx.fillStyle = P.gS; ctx.fill(); ctx.strokeStyle = P.g; ctx.lineWidth = 2; ctx.stroke();
        A.txt(ctx, vals[0], 535, 158, { align: 'center', size: 18, mono: true, w: 700, fill: P.g });
      }
      A.txt(ctx, lbl, 460, 250, { size: 12, w: 700, fill: P.a });
      A.txt(ctx, 'The axis you name is the one that DISAPPEARS.', 40, 288,
        { size: 13, w: 700, fill: P.g });
      A.txt(ctx, 'axis=0 collapses down the rows, leaving one answer per column. axis=1 does the opposite.',
        40, 310, { size: 12, fill: P.faint });
      A.txt(ctx, 'Leave axis out entirely and everything collapses to a single number.', 40, 332,
        { size: 12, fill: P.faint });
      ro.set('Same idea for <code>.min()</code>, <code>.std()</code>, <code>.argmax()</code>, ' +
        '<code>.cumsum()</code> — they all take <code>axis</code>.' +
        '\nRemember it by the shape: (3,4) with axis=0 gives (4,), with axis=1 gives (3,). The named ' +
        'axis is gone.');
    }
    sync(); A.bind(c, render); render();
  });

  /* ============================================================
     11. Boolean masks
     ============================================================ */
  A.def('fmask', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var thr = 25;
    var vals = [12, 31, 7, 44, 19, 28];
    var bar = A.ctrls(root), ro = A.readout(root);
    A.slider(bar, { label: 'x >', min: 0, max: 50, step: 1, value: thr,
      fmt: function (v) { return v.toFixed(0); }, on: function (v) { thr = v; render(); } });
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var mask = vals.map(function (v) { return v > thr; });
      A.txt(ctx, 'x = np.array([12, 31, 7, 44, 19, 28])', 40, 46,
        { size: 13, mono: true, w: 700, fill: P.soft });
      A.matrix(ctx, 60, 68, 1, 6, 92, 44, P, function (i, j) { return String(vals[j]); },
        { state: function (i, j) { return mask[j] ? 1 : 0; }, size: 14, label: 'x' });
      A.txt(ctx, 'x > ' + thr, 60, 148, { size: 15, mono: true, w: 700, fill: P.a });
      A.arrow(ctx, 130, 143, 175, 143, P.line, 2);
      A.matrix(ctx, 195, 126, 1, 6, 78, 36, P,
        function (i, j) { return mask[j] ? 'True' : 'False'; },
        { state: function (i, j) { return mask[j] ? 3 : 4; }, size: 10.5 });
      A.txt(ctx, 'a mask — one True/False per position, same length', 195, 182,
        { size: 11, fill: P.faint });
      var kept = vals.filter(function (v, i) { return mask[i]; });
      A.txt(ctx, 'x[x > ' + thr + ']', 60, 226, { size: 15, mono: true, w: 700, fill: P.g });
      A.arrow(ctx, 160, 221, 205, 221, P.line, 2);
      if (kept.length) {
        A.matrix(ctx, 225, 202, 1, kept.length, 76, 40, P,
          function (i, j) { return String(kept[j]); },
          { state: function () { return 3; }, size: 13 });
      } else {
        A.txt(ctx, 'array([])  — nothing passed', 225, 226, { size: 13, mono: true, fill: P.faint });
      }
      A.txt(ctx, 'putting the mask in the brackets keeps only the Trues', 225, 260,
        { size: 11, fill: P.faint });
      A.txt(ctx, 'A comparison on an array gives you a whole array of True/False — not one answer.',
        40, 292, { size: 12.5, w: 700, fill: P.soft });
      A.txt(ctx, 'mask.sum() counts the Trues, because True counts as 1. Very handy.', 40, 314,
        { size: 12, mono: true, w: 700, fill: P.b });
      ro.set('<code>(y_pred == y_true).mean()</code> is accuracy, in one line — the comparison makes a ' +
        'mask, and the mean of True/False is the fraction that are True.' +
        '\nCombine masks with <code>&amp;</code> (and) and <code>|</code> (or), and <b>each condition ' +
        'needs its own brackets</b>: <code>(x &gt; 5) &amp; (x &lt; 20)</code>.');
    }
    A.bind(c, render); render();
  });

  /* ============================================================
     12. Reshape, flatten, transpose
     ============================================================ */
  A.def('freshape', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var which = 0;
    var shapes = [
      ['x.reshape(2, 6)', 2, 6], ['x.reshape(3, 4)', 3, 4], ['x.reshape(4, 3)', 4, 3],
      ['x.reshape(-1, 4)', 3, 4], ['x.reshape(12)', 1, 12]
    ];
    var bar = A.ctrls(root), ro = A.readout(root);
    shapes.forEach(function (s, i) { A.button(bar, s[0].replace('x.', ''), function () { which = i; sync(); render(); }); });
    function sync() { bar.querySelectorAll('button').forEach(function (b, i) { b.classList.toggle('primary', i === which); }); }
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var s = shapes[which], R = s[1], C = s[2];
      A.txt(ctx, 'x = np.arange(12)      →  [0 1 2 3 4 5 6 7 8 9 10 11]', 40, 44,
        { size: 12.5, mono: true, w: 700, fill: P.soft });
      A.txt(ctx, s[0], 40, 76, { size: 17, mono: true, w: 700, fill: P.a });
      var cw = Math.min(58, 560 / C), ch = 42;
      A.matrix(ctx, 60, 100, R, C, cw, ch, P,
        function (i, j) { return String(i * C + j); },
        { state: function (i) { return i % 2 === 0 ? 1 : 2; }, size: 12,
          shape: 'shape = (' + R + ', ' + C + ')' });
      A.txt(ctx, 'The 12 numbers never move and never change. Only the shape you view them through changes.',
        40, 120 + R * ch + 30, { size: 12.5, w: 700, fill: P.soft });
      A.txt(ctx, 'The new shape must multiply to the SAME total: ' + R + ' × ' + C + ' = 12 ✓',
        40, 120 + R * ch + 52, { size: 12, fill: P.faint });
      A.txt(ctx, '-1 means “work this one out for me”. reshape(-1, 4) says “4 columns, however many rows that takes”.',
        40, 302, { size: 12, w: 700, fill: P.a });
      A.txt(ctx, 'Related: x.flatten() squashes to 1-D  ·  x.T swaps rows and columns (a different thing!)',
        40, 324, { size: 12, mono: true, fill: P.faint });
      ro.set('<b>reshape ≠ transpose.</b> Reshape re-cuts the same sequence into a new grid. Transpose ' +
        'genuinely moves numbers to mirrored positions. They can give different answers for the same shape.' +
        '\n<code>x.reshape(1, -1)</code> turns a (n,) into a (1, n) — the fix for “Keras wants 2-D”.');
    }
    sync(); A.bind(c, render); render();
  });

  /* ============================================================
     13. pandas DataFrames
     ============================================================ */
  A.def('fdataframe', function (root) {
    var c = A.canvas(root, 760, 340), ctx = c.ctx;
    var which = 0;
    var COLS = ['size', 'beds', 'age', 'price'];
    var ROWS = [[2104, 5, 45, 460], [1416, 3, 40, 232], [1534, 3, 30, 315], [852, 2, 36, 178]];
    var ops = [
      ['df', function () { return { r: [0, 1, 2, 3], c: [0, 1, 2, 3] }; }, 'the whole table'],
      ["df['size']", function () { return { r: [0, 1, 2, 3], c: [0] }; }, 'one column, by NAME → a Series'],
      ["df[['size','beds']]", function () { return { r: [0, 1, 2, 3], c: [0, 1] }; }, 'several columns → double brackets'],
      ['df.head(2)', function () { return { r: [0, 1], c: [0, 1, 2, 3] }; }, 'the first few rows — always your first move'],
      ["df[df['beds'] > 2]", function () { return { r: [0, 1, 2], c: [0, 1, 2, 3] }; }, 'filter rows with a mask'],
      ['df.iloc[1, 0]', function () { return { r: [1], c: [0] }; }, 'one cell by POSITION, like NumPy']
    ];
    var bar = A.ctrls(root), ro = A.readout(root);
    ops.forEach(function (o, i) { A.button(bar, o[0], function () { which = i; sync(); render(); }); });
    function sync() { bar.querySelectorAll('button').forEach(function (b, i) { b.classList.toggle('primary', i === which); }); }
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var sel = ops[which][1]();
      var x0 = 150, y0 = 106, cw = 92, ch = 42;
      COLS.forEach(function (n, j) {
        A.txt(ctx, n, x0 + j * cw + 44, y0 - 12, { align: 'center', size: 12, mono: true, w: 700,
          fill: sel.c.indexOf(j) >= 0 ? P.a : P.faint });
      });
      ROWS.forEach(function (r, i) {
        A.txt(ctx, String(i), x0 - 14, y0 + i * ch + 26, { align: 'right', size: 11.5, mono: true,
          fill: sel.r.indexOf(i) >= 0 ? P.b : P.faint });
      });
      A.txt(ctx, 'index', x0 - 14, y0 - 12, { align: 'right', size: 10, fill: P.faint });
      A.matrix(ctx, x0, y0, 4, 4, cw, ch, P, function (i, j) { return String(ROWS[i][j]); },
        { state: function (i, j) { return (sel.r.indexOf(i) >= 0 && sel.c.indexOf(j) >= 0) ? 1 : 0; },
          size: 12.5 });
      A.txt(ctx, ops[which][0], 40, 60, { size: 17, mono: true, w: 700, fill: P.a });
      A.txt(ctx, ops[which][2], 300, 60, { size: 12.5, w: 700, fill: P.soft });
      A.txt(ctx, 'A DataFrame is a spreadsheet: columns have NAMES, rows have an index.', 40, 296,
        { size: 12.5, w: 700, fill: P.soft });
      A.txt(ctx, 'That is the whole difference from NumPy — NumPy has positions, pandas has labels.',
        40, 318, { size: 12, fill: P.faint });
      A.txt(ctx, 'pandas is for loading and cleaning. NumPy is for the maths. You use both.', 40, 338,
        { size: 12, w: 700, fill: P.a });
      ro.set('<code>df = pd.read_csv("houses.csv")</code> · <code>df.head()</code> · ' +
        '<code>df.shape</code> · <code>df.info()</code> · <code>df.describe()</code>' +
        '\nThose five are genuinely most of what you need. Run <code>head()</code> and ' +
        '<code>describe()</code> on every dataset before you model anything.');
    }
    sync(); A.bind(c, render); render();
  });

  /* ============================================================
     14. pandas → NumPy
     ============================================================ */
  A.def('fpandasnumpy', function (root) {
    var c = A.canvas(root, 760, 320), ctx = c.ctx;
    var ro = A.readout(root);
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var e = A.ease(A.clamp(((t * .4) % 3) - .4, 0, 1));
      var COLS = ['size', 'beds', 'price'];
      var R = [[2104, 5, 460], [1416, 3, 232], [1534, 3, 315]];
      /* dataframe on the left */
      ctx.save(); ctx.globalAlpha = 1 - e * .55;
      COLS.forEach(function (n, j) {
        A.txt(ctx, n, 90 + j * 74 + 34, 86, { align: 'center', size: 11.5, mono: true, w: 700, fill: P.b });
      });
      A.matrix(ctx, 90, 96, 3, 3, 74, 42, P, function (i, j) { return String(R[i][j]); },
        { state: function () { return 2; }, size: 12, label: 'df   (a DataFrame)' });
      ctx.restore();
      A.arrow(ctx, 330, 140, 400, 140, e > .3 ? P.a : P.line, 2.4);
      A.txt(ctx, '.to_numpy()', 365, 128, { align: 'center', size: 11.5, mono: true, w: 700,
        fill: e > .3 ? P.a : P.faint });
      /* array on the right */
      ctx.save(); ctx.globalAlpha = .35 + e * .65;
      A.matrix(ctx, 430, 96, 3, 3, 74, 42, P, function (i, j) { return String(R[i][j]); },
        { state: function () { return 3; }, size: 12, label: 'X   (a NumPy array)' });
      ctx.restore();
      A.txt(ctx, 'the column names are GONE', 430 + 110, 186, { align: 'center', size: 11, fill: P.r });
      A.txt(ctx, 'Load and clean with pandas. Do the maths with NumPy. Cross over once, deliberately.',
        40, 226, { size: 12.5, w: 700, fill: P.soft });
      A.txt(ctx, 'X = df[[\'size\', \'beds\']].to_numpy()      # the features', 40, 256,
        { size: 12.5, mono: true, w: 700, fill: P.g });
      A.txt(ctx, 'y = df[\'price\'].to_numpy()                # the target', 40, 278,
        { size: 12.5, mono: true, w: 700, fill: P.g });
      A.txt(ctx, 'Once converted you lose the names — so select the columns you want BEFORE converting.',
        40, 308, { size: 12, w: 700, fill: P.a });
      ro.set('<code>.to_numpy()</code> is the modern spelling; <code>.values</code> is the old one you ' +
        'will see in older notebooks. Same thing.' +
        '\nA common shape trap: <code>df[\'price\']</code> gives shape <code>(m,)</code> while ' +
        '<code>df[[\'price\']]</code> gives <code>(m, 1)</code>. The double brackets keep it 2-D.');
    }
    A.autoplay(root, c, render);
  });

  /* ============================================================
     15. Reading an error message
     ============================================================ */
  A.def('ftraceback', function (root) {
    var c = A.canvas(root, 760, 340), ctx = c.ctx;
    var which = 0;
    var errs = [
      ['ValueError: shapes (3,4) and (3,4) not aligned',
       'you tried to matmul two shapes whose inner numbers do not match',
       'transpose one of them: A @ B.T'],
      ['IndexError: index 5 is out of bounds for axis 0 with size 5',
       'valid positions are 0 to 4. You asked for 5',
       'remember counting starts at zero — the last one is x[4] or x[-1]'],
      ['TypeError: can only concatenate list (not "int") to list',
       'you did my_list + 10, which Python reads as “glue a number onto a list”',
       'convert it first: np.array(my_list) + 10'],
      ['NameError: name \'nunpy\' is not defined',
       'a typo, or you never ran the import cell',
       'check the spelling, then run the import cell at the top'],
      ['KeyError: \'Price\'',
       'that column name is not in the DataFrame',
       "print(df.columns) — it is probably 'price' with a small p"]
    ];
    var bar = A.ctrls(root), ro = A.readout(root);
    ['ValueError', 'IndexError', 'TypeError', 'NameError', 'KeyError'].forEach(function (n, i) {
      A.button(bar, n, function () { which = i; sync(); render(); });
    });
    function sync() { bar.querySelectorAll('button').forEach(function (b, i) { b.classList.toggle('primary', i === which); }); }
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var e = errs[which];
      A.txt(ctx, 'A traceback looks terrifying and is mostly noise. Read it from the BOTTOM.',
        40, 44, { size: 13, w: 700, fill: P.soft });
      /* fake traceback */
      A.rr(ctx, 40, 62, 680, 130, 8);
      ctx.fillStyle = P.sunk; ctx.fill(); ctx.strokeStyle = P.lineSoft; ctx.stroke();
      var lines = ['Traceback (most recent call last)',
        '  File "<ipython-input-4>", line 3, in <module>',
        '    result = compute(X, W)',
        '  File "model.py", line 47, in compute',
        '    return np.matmul(A, B)'];
      lines.forEach(function (l, i) {
        A.txt(ctx, l, 56, 82 + i * 18, { size: 11, mono: true, fill: P.faint });
      });
      A.rr(ctx, 48, 168, 664, 20, 4); ctx.fillStyle = P.rS; ctx.fill();
      A.txt(ctx, e[0], 56, 182, { size: 11.5, mono: true, w: 700, fill: P.r });
      A.arrow(ctx, 30, 178, 44, 178, P.r, 2);
      A.txt(ctx, 'read this line ↑ first — it is the only one that says what went wrong', 56, 208,
        { size: 11.5, w: 700, fill: P.r });
      A.txt(ctx, 'what it means', 40, 244, { size: 12, w: 700, fill: P.a });
      A.txt(ctx, e[1], 40, 266, { size: 12.5, fill: P.soft });
      A.txt(ctx, 'what to do', 40, 296, { size: 12, w: 700, fill: P.g });
      A.txt(ctx, e[2], 40, 318, { size: 12.5, mono: true, fill: P.g });
      A.txt(ctx, 'The middle lines just show HOW the code got there. Useful later, ignorable at first.',
        40, 338, { size: 11, fill: P.faint });
      ro.set('Two habits that solve most of these: <b>print the shapes</b> of every array involved, ' +
        'and <b>print the type</b> of anything behaving strangely.' +
        '\nAnd read the last line properly — it is a plain English sentence, and it almost always ' +
        'names the actual problem.');
    }
    sync(); A.bind(c, render); render();
  });

  /* ============================================================
     16. Functions
     ============================================================ */
  A.def('ffunction', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var ro = A.readout(root);
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var hot = Math.floor((t * .55) % 5);
      var parts = [
        ['def', 'the word that says “I am defining a function”', 40, P.p],
        ['compute_cost', 'the NAME you will call it by', 84, P.a],
        ['(X, y, w, b)', 'the inputs it expects — the parameters', 240, P.b],
        [':', 'the colon starts the body. The indent that follows is part of the function', 380, P.faint],
        ['return', 'hands one value back to whoever called it', 40, P.g]
      ];
      A.txt(ctx, 'def compute_cost(X, y, w, b):', 40, 84, { size: 20, mono: true, w: 700, fill: P.soft });
      A.txt(ctx, '    m = X.shape[0]', 40, 114, { size: 15, mono: true, fill: P.faint });
      A.txt(ctx, '    err = (X @ w + b) - y', 40, 140, { size: 15, mono: true, fill: P.faint });
      A.txt(ctx, '    return np.sum(err ** 2) / (2 * m)', 40, 166, { size: 15, mono: true, fill: P.soft });
      /* highlight the current part */
      var hl = parts[hot];
      var y = hot === 4 ? 166 : 84;
      A.rr(ctx, hl[2] - 6, y - 18, hl[0].length * 11.4 + 12, 24, 4);
      ctx.strokeStyle = hl[3]; ctx.lineWidth = 2.2; ctx.stroke();
      A.txt(ctx, hl[0], hl[2], y, { size: 20, mono: true, w: 700, fill: hl[3] });
      A.txt(ctx, hl[1], 40, 210, { size: 13, w: 700, fill: hl[3] });
      A.txt(ctx, 'calling it', 40, 250, { size: 12, w: 700, fill: P.soft });
      A.txt(ctx, 'J = compute_cost(X_train, y_train, w, b)', 40, 274,
        { size: 14, mono: true, w: 700, fill: P.g });
      A.txt(ctx, 'the values you pass in are matched to the parameters IN ORDER', 40, 296,
        { size: 11.5, fill: P.faint });
      A.txt(ctx, 'Indentation is not decoration in Python — it is what says which lines are inside.',
        40, 322, { size: 12, w: 700, fill: P.r });
      ro.set('When you read a function you have not seen, read three things: its <b>name</b>, its ' +
        '<b>parameters</b>, and what it <b>returns</b>. That is usually enough to use it.' +
        '\nEvery graded exercise in this specialization is “fill in the body of a function whose ' +
        'signature is already written for you”.');
    }
    A.autoplay(root, c, render);
  });

})();
