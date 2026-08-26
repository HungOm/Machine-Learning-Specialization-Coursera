/* Widgets for Course 3 / Week 3 — reinforcement learning */
(function () {
  'use strict';

  var N = 6;
  /* value iteration on the 6-state Mars rover */
  function solveRover(rewards, gamma, misstep) {
    misstep = misstep || 0;
    var V = new Array(N).fill(0), i, s, it;
    for (s = 0; s < N; s++) V[s] = rewards[s];
    for (it = 0; it < 400; it++) {
      var nv = V.slice();
      for (s = 1; s < N - 1; s++) {
        var qs = [0, 1].map(function (a) {           /* 0 = left, 1 = right */
          var intended = a === 0 ? s - 1 : s + 1;
          var other = a === 0 ? s + 1 : s - 1;
          intended = Math.max(0, Math.min(N - 1, intended));
          other = Math.max(0, Math.min(N - 1, other));
          return rewards[s] + gamma * ((1 - misstep) * V[intended] + misstep * V[other]);
        });
        nv[s] = Math.max(qs[0], qs[1]);
      }
      V = nv;
    }
    var Q = [];
    for (s = 0; s < N; s++) {
      if (s === 0 || s === N - 1) { Q.push([rewards[s], rewards[s]]); continue; }
      Q.push([0, 1].map(function (a) {
        var intended = a === 0 ? s - 1 : s + 1, other = a === 0 ? s + 1 : s - 1;
        intended = Math.max(0, Math.min(N - 1, intended));
        other = Math.max(0, Math.min(N - 1, other));
        return rewards[s] + gamma * ((1 - misstep) * V[intended] + misstep * V[other]);
      }));
    }
    return { V: V, Q: Q };
  }
  var LBL = ['1', '2', '3', '4', '5', '6'];

  function drawRover(ctx, x, y, s, P, colr) {
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
    ctx.fillStyle = colr || P.a;
    A.rr(ctx, -14, -10, 28, 15, 4); ctx.fill();
    ctx.beginPath(); ctx.arc(-8, 7, 5, 0, 6.2832); ctx.fill();
    ctx.beginPath(); ctx.arc(8, 7, 5, 0, 6.2832); ctx.fill();
    ctx.fillStyle = P.panel;
    ctx.beginPath(); ctx.arc(-8, 7, 2, 0, 6.2832); ctx.fill();
    ctx.beginPath(); ctx.arc(8, 7, 2, 0, 6.2832); ctx.fill();
    ctx.restore();
  }
  /* draw the 6-state strip, return an x() function */
  function strip(ctx, P, y, rewards, opts) {
    opts = opts || {};
    var x0 = 90, cw = 100;
    for (var s = 0; s < N; s++) {
      var term = s === 0 || s === N - 1;
      var x = x0 + s * cw;
      A.rr(ctx, x - 42, y - 30, 84, 60, 10);
      ctx.fillStyle = term ? (rewards[s] >= 100 ? P.gS : P.mS) : P.sunk;
      ctx.fill();
      ctx.strokeStyle = opts.hi === s ? P.a : (term ? (rewards[s] >= 100 ? P.g : P.m) : P.lineSoft);
      ctx.lineWidth = opts.hi === s ? 2.6 : 1.4; ctx.stroke();
      A.txt(ctx, LBL[s], x, y - 8, { align: 'center', size: 15, w: 700,
        fill: opts.hi === s ? P.a : P.soft });
      A.txt(ctx, 'R = ' + rewards[s], x, y + 14, { align: 'center', size: 11.5, mono: true,
        fill: term ? (rewards[s] >= 100 ? P.g : P.m) : P.faint });
      if (term) A.txt(ctx, 'terminal', x, y + 44, { align: 'center', size: 10, fill: P.faint });
    }
    return function (s) { return x0 + s * cw; };
  }

  /* ============================================================
     1. What is reinforcement learning?
     ============================================================ */
  A.def('whatisrl', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var ro = A.readout(root);
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var phase = (t * .55) % 3;
      A.rr(ctx, 90, 90, 200, 90, 12);
      ctx.fillStyle = phase < 1 ? P.aS : P.sunk; ctx.fill();
      ctx.strokeStyle = phase < 1 ? P.a : P.lineSoft; ctx.lineWidth = phase < 1 ? 2.4 : 1.4; ctx.stroke();
      A.txt(ctx, 'AGENT', 190, 126, { align: 'center', size: 16, w: 700, fill: phase < 1 ? P.a : P.faint });
      A.txt(ctx, 'the thing that decides', 190, 150, { align: 'center', size: 11, fill: P.faint });
      A.rr(ctx, 470, 90, 200, 90, 12);
      ctx.fillStyle = phase >= 1 && phase < 2 ? P.bS : P.sunk; ctx.fill();
      ctx.strokeStyle = phase >= 1 && phase < 2 ? P.b : P.lineSoft;
      ctx.lineWidth = phase >= 1 && phase < 2 ? 2.4 : 1.4; ctx.stroke();
      A.txt(ctx, 'ENVIRONMENT', 570, 126, { align: 'center', size: 16, w: 700,
        fill: phase >= 1 && phase < 2 ? P.b : P.faint });
      A.txt(ctx, 'the world it acts in', 570, 150, { align: 'center', size: 11, fill: P.faint });
      /* action arrow */
      ctx.save(); ctx.strokeStyle = phase < 1 ? P.a : P.line; ctx.lineWidth = phase < 1 ? 2.6 : 1.4;
      ctx.beginPath(); ctx.moveTo(292, 112); ctx.bezierCurveTo(360, 76, 400, 76, 468, 112); ctx.stroke(); ctx.restore();
      A.txt(ctx, 'action  a', 380, 72, { align: 'center', size: 12.5, w: 700, fill: phase < 1 ? P.a : P.faint });
      /* state + reward arrow */
      ctx.save(); ctx.strokeStyle = phase >= 1 ? P.b : P.line; ctx.lineWidth = phase >= 1 ? 2.6 : 1.4;
      ctx.beginPath(); ctx.moveTo(468, 158); ctx.bezierCurveTo(400, 196, 360, 196, 292, 158); ctx.stroke(); ctx.restore();
      A.txt(ctx, 'new state  s′     reward  R', 380, 214, { align: 'center', size: 12.5, w: 700,
        fill: phase >= 1 ? P.b : P.faint });
      if (phase < 1) { var u = phase; A.dot(ctx, A.lerp(292, 468, u), 84 + Math.sin(u * 3.14) * -8, 6, P.a); }
      else if (phase < 2) { var u2 = phase - 1; A.dot(ctx, A.lerp(468, 292, u2), 176 + Math.sin(u2 * 3.14) * 8, 6, P.b); }
      A.txt(ctx, 'Nobody ever says “the correct action here was X”.', 40, 262, { size: 12.5, w: 700, fill: P.soft });
      A.txt(ctx, 'You only get a reward — and often only much later.', 40, 282, { size: 12.5, w: 700, fill: P.a });
      A.txt(ctx, 'That is the whole difference from supervised learning: no (x, y) pairs, just consequences.',
        40, 310, { size: 11.5, fill: P.faint });
      ro.set('Supervised learning: “here is the input, here is the right answer.”' +
        '\nReinforcement learning: “here is the situation. Do something. …that was worth 3 points.”' +
        '\nThe job is to find a <b>policy</b> — a rule mapping every state to an action — that collects the most reward.');
    }
    A.bind(c, function () { render(lt); });
    var lt = 0; A.loop(c.cv, function (t) { lt = t; render(t); });
  });

  /* ============================================================
     2. The Mars rover example
     ============================================================ */
  A.def('marsrover', function (root) {
    var c = A.canvas(root, 760, 320), ctx = c.ctx;
    var rewards = [100, 0, 0, 0, 0, 40];
    var pos = 3, trail = [3], rewSum = 0, steps = 0;
    var bar = A.ctrls(root), ro = A.readout(root);
    A.button(bar, '← go left', function () { moveTo(pos - 1); });
    A.button(bar, 'go right →', function () { moveTo(pos + 1); });
    A.button(bar, 'reset to state 4', function () { pos = 3; trail = [3]; rewSum = 0; steps = 0; render(); });
    function moveTo(np) {
      if (pos === 0 || pos === N - 1) return;
      pos = Math.max(0, Math.min(N - 1, np));
      trail.push(pos); steps++;
      rewSum += rewards[pos] * Math.pow(0.5, steps);
      render();
    }
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var X = strip(ctx, P, 130, rewards, { hi: pos });
      drawRover(ctx, X(pos), 82, 1.1, P, P.a);
      /* the trail */
      trail.forEach(function (s, i) {
        if (i === 0) return;
        A.arrow(ctx, X(trail[i - 1]), 198 + i * 0, X(s), 198, P.faint, 1.4);
      });
      A.txt(ctx, 'six positions. Two of them are worth stopping at.', 40, 46, { size: 13, w: 700, fill: P.soft });
      A.txt(ctx, 'state 1 holds the interesting rock (reward 100). State 6 holds a duller one (reward 40).',
        40, 68, { size: 11.5, fill: P.faint });
      A.txt(ctx, 'path so far: ' + trail.map(function (s) { return LBL[s]; }).join(' → '), 40, 236,
        { size: 13, mono: true, fill: P.soft });
      A.txt(ctx, 'steps taken: ' + steps, 40, 258, { size: 12.5, mono: true, fill: P.faint });
      var terminal = pos === 0 || pos === N - 1;
      A.txt(ctx, terminal ? '✓ reached a terminal state — the episode is over' : 'still going…',
        40, 282, { size: 13, w: 700, fill: terminal ? P.g : P.faint });
      A.txt(ctx, 'discounted return so far (γ = 0.5): ' + rewSum.toFixed(2), 40, 306,
        { size: 13, mono: true, w: 700, fill: P.a });
      ro.set('At every step the rover sees a <b>state</b> (which of the six squares it is on), picks an ' +
        '<b>action</b> (left or right), lands in a <b>new state</b>, and collects a <b>reward</b>.' +
        '\nGoing left from state 4 takes 3 steps to reach a reward of 100. Going right takes 2 steps to reach 40. ' +
        'Which is better? That is exactly what the next lesson answers.');
    }
    A.bind(c, render); render();
  });

  /* ============================================================
     3. The Return
     ============================================================ */
  A.def('returns', function (root) {
    var c = A.canvas(root, 760, 340), ctx = c.ctx;
    var g = 0.5;
    var bar = A.ctrls(root), ro = A.readout(root);
    A.slider(bar, { label: 'γ (discount)', min: .1, max: .99, step: .01, value: g,
      fmt: function (v) { return v.toFixed(2); }, on: function (v) { g = v; render(); } });
    var rewards = [100, 0, 0, 0, 0, 40];
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var start = 3;
      var pathL = [3, 2, 1, 0], pathR = [3, 4, 5];
      function ret(path) {
        var s = 0;
        path.forEach(function (st, i) { s += Math.pow(g, i) * rewards[st]; });
        return s;
      }
      var rl = ret(pathL), rr = ret(pathR);
      A.txt(ctx, 'starting at state 4 — two ways to go', 40, 40, { size: 13, w: 700, fill: P.soft });
      [[pathL, 'go LEFT (3 steps to the big reward)', 90, rl, rl >= rr],
       [pathR, 'go RIGHT (2 steps to the small reward)', 210, rr, rr > rl]
      ].forEach(function (row) {
        var path = row[0], y = row[2], win = row[4];
        A.txt(ctx, row[1], 40, y - 26, { size: 12.5, w: 700, fill: win ? P.a : P.faint });
        var terms = [];
        path.forEach(function (st, i) {
          var x = 60 + i * 92;
          A.rr(ctx, x, y - 14, 64, 44, 8);
          ctx.fillStyle = rewards[st] ? (rewards[st] >= 100 ? P.gS : P.mS) : P.sunk; ctx.fill();
          ctx.strokeStyle = rewards[st] ? (rewards[st] >= 100 ? P.g : P.m) : P.lineSoft; ctx.stroke();
          A.txt(ctx, LBL[st], x + 32, y + 4, { align: 'center', size: 13, w: 700, fill: P.soft });
          A.txt(ctx, 'R=' + rewards[st], x + 32, y + 22, { align: 'center', size: 10, mono: true, fill: P.faint });
          if (i < path.length - 1) A.arrow(ctx, x + 66, y + 8, x + 88, y + 8, P.line, 1.6);
          terms.push((i === 0 ? '' : 'γ' + (i > 1 ? '^' + i : '') + '·') + rewards[st]);
        });
        var tx = 60 + path.length * 92 + 20;
        A.txt(ctx, '= ' + terms.join(' + '), tx, y - 2, { size: 11.5, mono: true, fill: P.faint });
        A.txt(ctx, 'return = ' + row[3].toFixed(2), tx, y + 22,
          { size: 15, mono: true, w: 700, fill: win ? P.a : P.soft });
      });
      A.rr(ctx, 40, 250, 680, 40, 8);
      ctx.fillStyle = P.aS; ctx.fill(); ctx.strokeStyle = P.a; ctx.lineWidth = 1.6; ctx.stroke();
      A.txt(ctx, 'with γ = ' + g.toFixed(2) + ' the rover should go ' + (rl >= rr ? 'LEFT' : 'RIGHT') +
        '  —  ' + (rl >= rr ? 'patience pays' : 'the far reward is discounted too heavily'),
        380, 275, { align: 'center', size: 13.5, w: 700, fill: P.a });
      A.txt(ctx, 'γ near 1 = a patient agent that happily waits for a bigger payoff later.', 40, 312,
        { size: 12, fill: P.soft });
      A.txt(ctx, 'γ near 0 = an impatient agent that grabs whatever is closest. Try 0.3, then 0.9.', 40, 332,
        { size: 12, w: 700, fill: P.a });
      ro.set('Return = R<sub>1</sub> + γR<sub>2</sub> + γ²R<sub>3</sub> + γ³R<sub>4</sub> + …' +
        '\nEach step into the future is multiplied by another γ, so distant rewards count for less. ' +
        'Typical values are 0.9, 0.99, 0.999 — this course uses 0.5 only to keep the arithmetic readable.');
    }
    A.bind(c, render); render();
  });

  /* ============================================================
     4. Policies
     ============================================================ */
  A.def('policies', function (root) {
    var c = A.canvas(root, 760, 320), ctx = c.ctx;
    var which = 0;
    var rewards = [100, 0, 0, 0, 0, 40];
    var pols = [
      { n: 'always go left', pi: [0, 0, 0, 0, 0, 0] },
      { n: 'always go right', pi: [1, 1, 1, 1, 1, 1] },
      { n: 'go to the nearer reward', pi: [0, 0, 0, 1, 1, 1] },
      { n: 'the OPTIMAL policy', pi: null }
    ];
    var bar = A.ctrls(root), ro = A.readout(root);
    pols.forEach(function (p, i) { A.button(bar, p.n, function () { which = i; sync(); render(); }); });
    function sync() { bar.querySelectorAll('button').forEach(function (b, i) { b.classList.toggle('primary', i === which); }); }
    function evalPolicy(pi, g) {
      var V = rewards.slice(), it, s;
      for (it = 0; it < 300; it++) {
        var nv = V.slice();
        for (s = 1; s < N - 1; s++) {
          var ns = pi[s] === 0 ? s - 1 : s + 1;
          nv[s] = rewards[s] + g * V[ns];
        }
        V = nv;
      }
      return V;
    }
    function render() {
      var P = A.pal(); c.clear(P.panel);
      var sol = solveRover(rewards, .5, 0);
      var pi = pols[which].pi || sol.Q.map(function (q) { return q[0] >= q[1] ? 0 : 1; });
      var V = pols[which].pi ? evalPolicy(pi, .5) : sol.V;
      var X = strip(ctx, P, 128, rewards, {});
      for (var s = 1; s < N - 1; s++) {
        var dir = pi[s] === 0 ? -1 : 1;
        A.arrow(ctx, X(s), 78, X(s) + dir * 40, 78, P.a, 2.4);
        A.txt(ctx, 'π(' + LBL[s] + ') = ' + (pi[s] === 0 ? '←' : '→'), X(s), 200,
          { align: 'center', size: 12, mono: true, w: 700, fill: P.a });
        A.txt(ctx, V[s].toFixed(1), X(s), 224, { align: 'center', size: 13, mono: true, w: 700, fill: P.g });
      }
      A.txt(ctx, 'value of', 48, 224, { align: 'right', size: 11, fill: P.faint });
      A.txt(ctx, 'each state', 48, 238, { align: 'right', size: 11, fill: P.faint });
      A.txt(ctx, 'a policy π is just a lookup table: state in, action out', 40, 44,
        { size: 13, w: 700, fill: P.soft });
      var tot = V.slice(1, N - 1).reduce(function (a, b) { return a + b; }, 0);
      var best = sol.V.slice(1, N - 1).reduce(function (a, b) { return a + b; }, 0);
      A.txt(ctx, 'total value across the four non-terminal states: ' + tot.toFixed(1) +
        (Math.abs(tot - best) < .01 ? '  ← the best possible' : '  (best possible: ' + best.toFixed(1) + ')'),
        40, 266, { size: 12.5, mono: true, w: 700, fill: Math.abs(tot - best) < .01 ? P.g : P.soft });
      A.txt(ctx, 'The goal of reinforcement learning is to find the policy that maximises the expected return',
        40, 296, { size: 12, fill: P.soft });
      A.txt(ctx, 'from EVERY state. Note that the optimal policy sends state 5 right and state 4 left — a split decision.',
        40, 314, { size: 11.5, fill: P.faint });
      ro.set('π(s) = a  —  “when you are in state s, do a”.' +
        '\nThe optimal policy is written π*(s). Finding it is the entire problem, and the state-action ' +
        'value function in the next lesson is the tool that finds it.');
    }
    sync(); A.bind(c, render); render();
  });

  /* ============================================================
     5. Review of key concepts (the MDP)
     ============================================================ */
  A.def('mdpreview', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var items = [
      ['states  S', 'where you can be', 'the 6 squares · the helicopter’s position and speed · the board position'],
      ['actions  A', 'what you can do', 'left / right · move the control stick · place a piece'],
      ['rewards  R(s)', 'what each state is worth', '100 · 0 · 40 · −1000 for crashing'],
      ['discount  γ', 'how patient you are', '0.5 in this course · 0.99 in real problems'],
      ['policy  π(s)', 'the rule you are learning', 'state in → action out'],
      ['return', 'what you are maximising', 'R₁ + γR₂ + γ²R₃ + …']
    ];
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var hot = Math.floor((t * .5) % items.length);
      A.txt(ctx, 'This whole setup has a name: a MARKOV DECISION PROCESS', 40, 38,
        { size: 13.5, w: 700, fill: P.a });
      items.forEach(function (r, i) {
        var y = 54 + i * 40, on = i === hot;
        A.rr(ctx, 40, y, 680, 34, 7);
        ctx.fillStyle = on ? P.aS : P.sunk; ctx.fill();
        ctx.strokeStyle = on ? P.a : P.lineSoft; ctx.lineWidth = on ? 1.8 : 1; ctx.stroke();
        A.txt(ctx, r[0], 130, y + 22, { align: 'right', size: 13, mono: true, w: 700,
          fill: on ? P.a : P.soft });
        A.txt(ctx, r[1], 150, y + 22, { size: 12, w: on ? 700 : 500, fill: on ? P.a : P.soft });
        A.txt(ctx, r[2], 710, y + 22, { align: 'right', size: 10.5, fill: P.faint });
      });
      A.txt(ctx, '“Markov” means: the future depends only on WHERE YOU ARE NOW, not on how you got here.',
        40, 310, { size: 12, w: 700, fill: P.soft });
      A.txt(ctx, 'If that is false for your problem, put the missing history INTO the state.', 40, 326,
        { size: 11.5, fill: P.faint });
    }
    A.bind(c, function () { render(lt); });
    var lt = 0; A.loop(c.cv, function (t) { lt = t; render(t); });
  });

  /* ============================================================
     6 + 7. The state-action value function Q(s, a)
     ============================================================ */
  function qWidget(name, withRewardSliders) {
    A.def(name, function (root) {
      var c = A.canvas(root, 760, 340), ctx = c.ctx;
      var g = 0.5, rL = 100, rR = 40;
      var bar = A.ctrls(root), ro = A.readout(root);
      A.slider(bar, { label: 'γ', min: .1, max: .99, step: .01, value: g,
        fmt: function (v) { return v.toFixed(2); }, on: function (v) { g = v; render(); } });
      if (withRewardSliders) {
        A.slider(bar, { label: 'reward at state 1', min: 0, max: 200, step: 5, value: rL,
          fmt: function (v) { return v.toFixed(0); }, on: function (v) { rL = v; render(); } });
        A.slider(bar, { label: 'reward at state 6', min: 0, max: 200, step: 5, value: rR,
          fmt: function (v) { return v.toFixed(0); }, on: function (v) { rR = v; render(); } });
      }
      function render() {
        var P = A.pal(); c.clear(P.panel);
        var rewards = [rL, 0, 0, 0, 0, rR];
        var sol = solveRover(rewards, g, 0);
        var X = strip(ctx, P, 108, rewards, {});
        for (var s = 1; s < N - 1; s++) {
          var q = sol.Q[s], bestA = q[0] >= q[1] ? 0 : 1;
          [0, 1].forEach(function (a) {
            var y = 178 + a * 34, isBest = a === bestA;
            A.rr(ctx, X(s) - 42, y, 84, 28, 6);
            ctx.fillStyle = isBest ? P.aS : P.sunk; ctx.fill();
            ctx.strokeStyle = isBest ? P.a : P.lineSoft; ctx.lineWidth = isBest ? 1.8 : 1; ctx.stroke();
            A.txt(ctx, (a === 0 ? '← ' : '→ ') + q[a].toFixed(1), X(s), y + 19,
              { align: 'center', size: 12.5, mono: true, w: isBest ? 700 : 500,
                fill: isBest ? P.a : P.faint });
          });
          A.arrow(ctx, X(s), 66, X(s) + (bestA === 0 ? -38 : 38), 66, P.a, 2.2);
          A.txt(ctx, 'V = ' + sol.V[s].toFixed(1), X(s), 258, { align: 'center', size: 12, mono: true,
            w: 700, fill: P.g });
        }
        A.txt(ctx, 'Q(s, ←)', 44, 197, { align: 'right', size: 11.5, mono: true, fill: P.faint });
        A.txt(ctx, 'Q(s, →)', 44, 231, { align: 'right', size: 11.5, mono: true, fill: P.faint });
        A.txt(ctx, 'V(s)', 44, 258, { align: 'right', size: 11.5, mono: true, fill: P.g });
        A.txt(ctx, 'Q(s, a) = the return if you take action a ONCE, then behave optimally forever after',
          40, 40, { size: 12.5, w: 700, fill: P.soft });
        var pol = [];
        for (s = 1; s < N - 1; s++) pol.push(sol.Q[s][0] >= sol.Q[s][1] ? '←' : '→');
        A.txt(ctx, 'optimal policy for states 2–5:  ' + pol.join('  '), 40, 292,
          { size: 14, mono: true, w: 700, fill: P.a });
        A.txt(ctx, withRewardSliders
          ? 'Drag the rewards and γ — watch the arrows flip. Try reward 6 = 200, or γ = 0.9.'
          : 'π*(s) = whichever action has the larger Q. That is the entire method.',
          40, 318, { size: 12, w: 700, fill: withRewardSliders ? P.a : P.soft });
        ro.set('Once you know Q(s, a) for every state and action, the optimal policy is free:' +
          '\n<b>π*(s) = argmax<sub>a</sub> Q(s, a)</b>  —  just look at the two numbers and take the bigger one.' +
          '\nAnd V(s) = max<sub>a</sub> Q(s, a), the value of being in that state at all.');
      }
      A.bind(c, render); render();
    });
  }
  qWidget('qfunction', false);
  qWidget('qexample', true);

  /* ============================================================
     8. The Bellman equation
     ============================================================ */
  A.def('bellman', function (root) {
    var c = A.canvas(root, 760, 340), ctx = c.ctx;
    var s = 3, a = 0, g = 0.5;
    var rewards = [100, 0, 0, 0, 0, 40];
    var bar = A.ctrls(root), ro = A.readout(root);
    A.slider(bar, { label: 'state s =', min: 1, max: 4, step: 1, value: s,
      fmt: function (v) { return LBL[v]; }, on: function (v) { s = v; render(); } });
    A.button(bar, 'action: ←', function () { a = 0; sync(); render(); });
    A.button(bar, 'action: →', function () { a = 1; sync(); render(); });
    function sync() {
      var bs = bar.querySelectorAll('button');
      bs[0].classList.toggle('primary', a === 0); bs[1].classList.toggle('primary', a === 1);
    }
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var sol = solveRover(rewards, g, 0);
      var sp = a === 0 ? s - 1 : s + 1;
      var X = strip(ctx, P, 100, rewards, { hi: s });
      A.arrow(ctx, X(s), 58, X(sp), 58, P.a, 2.4);
      A.txt(ctx, a === 0 ? 'left' : 'right', (X(s) + X(sp)) / 2, 46, { align: 'center', size: 11, w: 700, fill: P.a });
      ctx.save(); ctx.setLineDash([4, 3]); ctx.strokeStyle = P.b; ctx.lineWidth = 2;
      A.rr(ctx, X(sp) - 46, 66, 92, 68, 12); ctx.stroke(); ctx.restore();
      /* the equation, decomposed */
      var Rs = rewards[s], Vsp = sol.V[sp], Q = Rs + g * Vsp;
      var parts = [
        ['Q(s, a)', Q.toFixed(2), P.a],
        ['=', '', P.faint],
        ['R(s)', Rs.toFixed(0), P.g],
        ['+', '', P.faint],
        ['γ', g.toFixed(2), P.m],
        ['×', '', P.faint],
        ['max Q(s′, a′)', Vsp.toFixed(2), P.b]
      ];
      var px = 70;
      parts.forEach(function (p) {
        var w = p[0].length * 9 + 24;
        if (p[1]) {
          A.rr(ctx, px, 186, w, 54, 8);
          ctx.fillStyle = p[2] === P.a ? P.aS : p[2] === P.g ? P.gS : p[2] === P.b ? P.bS : P.mS;
          ctx.fill(); ctx.strokeStyle = p[2]; ctx.lineWidth = 1.6; ctx.stroke();
          A.txt(ctx, p[0], px + w / 2, 206, { align: 'center', size: 12, mono: true, w: 700, fill: p[2] });
          A.txt(ctx, p[1], px + w / 2, 230, { align: 'center', size: 15, mono: true, w: 700, fill: p[2] });
          px += w + 12;
        } else {
          A.txt(ctx, p[0], px + 8, 220, { align: 'center', size: 18, fill: P.faint });
          px += 26;
        }
      });
      A.txt(ctx, 'the reward you get RIGHT NOW', 190, 262, { align: 'center', size: 10.5, fill: P.g });
      A.txt(ctx, 'the best you can do from wherever you land, discounted', 520, 262,
        { align: 'center', size: 10.5, fill: P.b });
      A.txt(ctx, 'Every return splits into exactly two pieces: what you get now, and the value of what comes next.',
        40, 294, { size: 12.5, w: 700, fill: P.soft });
      A.txt(ctx, 'That recursive split is the Bellman equation, and every RL algorithm in existence is built on it.',
        40, 314, { size: 12, fill: P.faint });
      A.txt(ctx, 'At a terminal state there is no “next”, so Q(s, a) = R(s) and the recursion stops.',
        40, 334, { size: 11.5, fill: P.faint });
      ro.set('<b>Q(s, a) = R(s) + γ · max<sub>a′</sub> Q(s′, a′)</b>' +
        '\ns = where you are   ·   a = what you do   ·   s′ = where you end up   ·   a′ = what you would do next' +
        '\nHere: Q(' + LBL[s] + ', ' + (a === 0 ? '←' : '→') + ') = ' + Rs + ' + ' + g + ' × ' +
        Vsp.toFixed(2) + ' = <b>' + Q.toFixed(2) + '</b>');
    }
    sync();
    A.bind(c, function () { render(lt); });
    var lt = 0; A.loop(c.cv, function (t) { lt = t; render(t); });
  });

  /* ============================================================
     9. Stochastic environments
     ============================================================ */
  A.def('stochastic', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var miss = 0.1;
    var rewards = [100, 0, 0, 0, 0, 40];
    var bar = A.ctrls(root), ro = A.readout(root);
    A.slider(bar, { label: 'chance of a misstep', min: 0, max: .5, step: .01, value: miss,
      fmt: function (v) { return (v * 100).toFixed(0) + '%'; }, on: function (v) { miss = v; render(); } });
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var sol = solveRover(rewards, .5, miss);
      var X = strip(ctx, P, 108, rewards, { hi: 3 });
      /* the two possible outcomes of "go left" from state 4 */
      A.arrow(ctx, X(3) - 8, 62, X(2) + 8, 62, P.g, 2.6);
      A.txt(ctx, (100 * (1 - miss)).toFixed(0) + '% — as intended', (X(3) + X(2)) / 2, 48,
        { align: 'center', size: 10.5, w: 700, fill: P.g });
      A.arrow(ctx, X(3) + 8, 62, X(4) - 8, 62, P.r, 1.4 + miss * 6);
      A.txt(ctx, (100 * miss).toFixed(0) + '% — slips the wrong way', (X(3) + X(4)) / 2, 48,
        { align: 'center', size: 10.5, w: 700, fill: P.r });
      /* animated dice roll */
      var roll = Math.floor(t * .8) % 2;
      var slipped = (Math.sin(Math.floor(t * .8) * 41.3) * 1000 % 1 + 1) % 1 < miss;
      drawRover(ctx, slipped ? X(4) : X(2), 172, .9, P, slipped ? P.r : P.g);
      A.txt(ctx, slipped ? 'slipped!' : 'went as planned', slipped ? X(4) : X(2), 202,
        { align: 'center', size: 11, w: 700, fill: slipped ? P.r : P.g });
      /* values */
      for (var s = 1; s < N - 1; s++)
        A.txt(ctx, 'V = ' + sol.V[s].toFixed(1), X(s), 236, { align: 'center', size: 12, mono: true,
          w: 700, fill: P.a });
      var clean = solveRover(rewards, .5, 0);
      A.txt(ctx, 'Every value has fallen. A world you cannot fully control is worth less to be in.',
        40, 268, { size: 12.5, w: 700, fill: P.soft });
      A.txt(ctx, 'V(4): ' + clean.V[3].toFixed(2) + ' with perfect control  →  ' + sol.V[3].toFixed(2) +
        ' with a ' + (miss * 100).toFixed(0) + '% misstep chance', 40, 290,
        { size: 12, mono: true, fill: P.faint });
      A.txt(ctx, 'The fix is small: maximise the EXPECTED return — the average over all the ways it could go.',
        40, 316, { size: 12, w: 700, fill: P.a });
      ro.set('Q(s, a) = R(s) + γ · <b>E</b>[ max<sub>a′</sub> Q(s′, a′) ]' +
        '\nThe only change is that <b>E</b>[…] — an average weighted by how likely each outcome is. ' +
        'Everything else in the course carries over untouched.');
    }
    A.bind(c, function () { render(lt); });
    var lt = 0; A.loop(c.cv, function (t) { lt = t; render(t); });
  });

})();

/* ---------- part 2 : continuous states and deep Q-learning ---------- */
(function () {
  'use strict';

  /* ============================================================
     10. Continuous state spaces
     ============================================================ */
  A.def('continuousstates', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var ro = A.readout(root);
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      /* discrete rover */
      A.txt(ctx, 'DISCRETE — the Mars rover', 180, 40, { align: 'center', size: 12.5, w: 700, fill: P.faint });
      for (var s = 0; s < 6; s++) {
        var x = 55 + s * 42;
        A.rr(ctx, x, 58, 34, 34, 6);
        var on = Math.floor((t * 1.1) % 6) === s;
        ctx.fillStyle = on ? P.aS : P.sunk; ctx.fill();
        ctx.strokeStyle = on ? P.a : P.lineSoft; ctx.stroke();
        A.txt(ctx, String(s + 1), x + 17, 80, { align: 'center', size: 12, w: 700, fill: on ? P.a : P.faint });
      }
      A.txt(ctx, 'six possible states. You could write them all down.', 180, 116,
        { align: 'center', size: 11, fill: P.faint });
      /* continuous truck */
      A.txt(ctx, 'CONTINUOUS — a self-driving truck', 560, 40, { align: 'center', size: 12.5, w: 700, fill: P.a });
      var tx = 560 + Math.sin(t * .6) * 70, ty = 84 + Math.cos(t * .43) * 12, th = Math.sin(t * .6) * .22;
      ctx.save(); ctx.translate(tx, ty); ctx.rotate(th);
      ctx.fillStyle = P.a; A.rr(ctx, -30, -12, 60, 22, 5); ctx.fill();
      ctx.fillStyle = P.ink;
      ctx.beginPath(); ctx.arc(-16, 12, 5, 0, 6.2832); ctx.fill();
      ctx.beginPath(); ctx.arc(16, 12, 5, 0, 6.2832); ctx.fill();
      ctx.restore();
      A.line(ctx, 420, 118, 700, 118, P.lineSoft, 1.4);
      var st = [
        ['x', (tx - 560).toFixed(2)], ['y', (ty - 84).toFixed(2)], ['θ', th.toFixed(3)],
        ['ẋ', (Math.cos(t * .6) * .42).toFixed(2)], ['ẏ', (-Math.sin(t * .43) * .05).toFixed(2)],
        ['θ̇', (Math.cos(t * .6) * .13).toFixed(3)]
      ];
      st.forEach(function (r, i) {
        var x = 430 + (i % 3) * 95, y = 148 + Math.floor(i / 3) * 30;
        A.txt(ctx, r[0] + ' = ' + r[1], x, y, { size: 12, mono: true, fill: P.a });
      });
      A.txt(ctx, 'six NUMBERS, each of which can be anything.', 560, 214,
        { align: 'center', size: 11, fill: P.faint });
      A.txt(ctx, 'You could never write them all down — there are infinitely many.', 560, 230,
        { align: 'center', size: 11, w: 700, fill: P.a });
      A.txt(ctx, 'An autonomous helicopter needs twelve: x, y, z, roll, pitch, yaw, and the rate of change of each.',
        40, 268, { size: 12, fill: P.soft });
      A.txt(ctx, 'A lookup table of Q values is now impossible. This is exactly the moment a neural network is needed —',
        40, 292, { size: 12, fill: P.soft });
      A.txt(ctx, 'not to store Q(s,a), but to COMPUTE it from a vector of numbers.', 40, 312,
        { size: 12, w: 700, fill: P.a });
      ro.set('Discrete state: s ∈ {1, 2, 3, 4, 5, 6} — a Q table with 6 × 2 = 12 entries works fine.' +
        '\nContinuous state: s ∈ ℝ<sup>n</sup> — a table would need infinitely many rows. ' +
        'So instead we train a function that <b>takes s and returns Q</b>.');
    }
    A.bind(c, function () { render(lt); });
    var lt = 0; A.loop(c.cv, function (t) { lt = t; render(t); });
  });

  /* ============================================================
     11. The lunar lander
     ============================================================ */
  A.def('lunarlander', function (root) {
    var c = A.canvas(root, 760, 350), ctx = c.ctx;
    var ro = A.readout(root);
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var cyc = (t * .28) % 1;
      var lx = 190 + (1 - cyc) * 60 - 40, ly = 60 + cyc * 150, ang = (1 - cyc) * .35;
      var landed = cyc > .93;
      /* ground and pad */
      A.line(ctx, 40, 236, 350, 236, P.line, 2);
      A.rr(ctx, 160, 230, 70, 8, 3); ctx.fillStyle = P.g; ctx.fill();
      A.txt(ctx, 'landing pad', 195, 254, { align: 'center', size: 10.5, w: 700, fill: P.g });
      /* the lander */
      ctx.save(); ctx.translate(lx, landed ? 222 : ly); ctx.rotate(landed ? 0 : ang);
      ctx.fillStyle = P.a; A.rr(ctx, -16, -14, 32, 24, 5); ctx.fill();
      ctx.strokeStyle = P.a; ctx.lineWidth = 2.4;
      ctx.beginPath(); ctx.moveTo(-12, 10); ctx.lineTo(-18, 22); ctx.moveTo(12, 10); ctx.lineTo(18, 22); ctx.stroke();
      if (!landed) {                                     /* the thruster flame */
        ctx.fillStyle = P.m;
        ctx.beginPath(); ctx.moveTo(-6, 10); ctx.lineTo(0, 24 + Math.sin(t * 20) * 5); ctx.lineTo(6, 10);
        ctx.closePath(); ctx.fill();
      }
      ctx.restore();
      A.txt(ctx, landed ? '✓ soft landing on the pad: +100' : 'firing the main engine: −0.3 per step',
        195, 288, { align: 'center', size: 12, w: 700, fill: landed ? P.g : P.faint });
      /* state vector */
      A.txt(ctx, 'the state s — eight numbers', 550, 40, { align: 'center', size: 12.5, w: 700, fill: P.b });
      [['x', 'how far left / right of the pad'], ['y', 'height above the ground'],
       ['ẋ', 'sideways speed'], ['ẏ', 'falling speed'],
       ['θ', 'tilt angle'], ['θ̇', 'how fast it is spinning'],
       ['l', '1 if the left leg is touching down'], ['r', '1 if the right leg is touching down']
      ].forEach(function (r, i) {
        var y = 60 + i * 24;
        A.txt(ctx, r[0], 420, y + 12, { size: 13, mono: true, w: 700, fill: P.b });
        A.txt(ctx, r[1], 448, y + 12, { size: 11, fill: P.faint });
      });
      A.txt(ctx, 'the actions — four of them', 550, 276, { align: 'center', size: 12.5, w: 700, fill: P.a });
      ['do nothing', 'fire the left thruster', 'fire the main engine', 'fire the right thruster']
        .forEach(function (n, i) {
          var x = 400 + (i % 2) * 170, y = 290 + Math.floor(i / 2) * 24;
          A.txt(ctx, '· ' + n, x, y + 12, { size: 11, fill: P.a });
        });
      A.txt(ctx, 'the reward function is where the real design work happens', 40, 316,
        { size: 12, w: 700, fill: P.soft });
      A.txt(ctx, 'reaching the pad +100 to +140  ·  crashing −100  ·  a leg touching down +10  ·  fuel costs −0.03 / −0.3',
        40, 336, { size: 11, fill: P.faint });
      ro.set('Writing the reward function is far more of an art than writing the algorithm. ' +
        'This one balances four goals at once — get there, do not crash, stay upright, and do not waste fuel.' +
        '\nGet it slightly wrong and you get a lander that hovers forever, or one that dives to the pad and explodes.');
    }
    A.bind(c, function () { render(lt); });
    var lt = 0; A.loop(c.cv, function (t) { lt = t; render(t); });
  });

  /* ============================================================
     12. Learning the state-value function (deep Q-learning)
     ============================================================ */
  A.def('dqn', function (root) {
    var c = A.canvas(root, 760, 350), ctx = c.ctx;
    var ro = A.readout(root);
    var steps = [
      ['initialise the neural network with RANDOM weights', 'it is a terrible guess at Q(s,a) — that is fine'],
      ['fly the lander, taking actions', 'badly at first. Store each (s, a, R(s), s′) tuple'],
      ['keep only the 10,000 most recent tuples', 'this is the REPLAY BUFFER'],
      ['build a training set from them', 'x = (s, a)     y = R(s) + γ · max Q(s′, a′)'],
      ['train Q_new so that Q_new(x) ≈ y', 'ordinary supervised learning — the C2 W2 loop'],
      ['set Q = Q_new, and go again', 'the targets y improve as Q improves. Repeat 10,000 times']
    ];
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var step = Math.floor((t * .45) % 6);
      steps.forEach(function (s, i) {
        var y = 40 + i * 44, on = i === step;
        A.rr(ctx, 40, y, 420, 38, 7);
        ctx.fillStyle = on ? P.aS : P.sunk; ctx.fill();
        ctx.strokeStyle = on ? P.a : P.lineSoft; ctx.lineWidth = on ? 2 : 1; ctx.stroke();
        A.txt(ctx, (i + 1) + '. ' + s[0], 54, y + 17, { size: 11.5, w: on ? 700 : 500,
          fill: on ? P.a : P.soft });
        A.txt(ctx, s[1], 54, y + 31, { size: 10, mono: i === 3, fill: P.faint });
      });
      /* the replay buffer */
      A.txt(ctx, 'replay buffer', 600, 40, { align: 'center', size: 12.5, w: 700, fill: P.b });
      var fill = step >= 2 ? 10 : Math.max(0, Math.floor((t * 3) % 11));
      for (var i = 0; i < 10; i++) {
        var y = 54 + i * 22, has = i < fill;
        A.rr(ctx, 490, y, 220, 18, 4);
        ctx.fillStyle = has ? P.bS : P.sunk; ctx.fill();
        ctx.strokeStyle = has ? P.b : P.lineSoft; ctx.stroke();
        if (has) A.txt(ctx, '(s' + (i + 1) + ', a' + (i + 1) + ', R' + (i + 1) + ', s′' + (i + 1) + ')',
          600, y + 13, { align: 'center', size: 10.5, mono: true, fill: P.b });
      }
      A.txt(ctx, 'oldest tuples fall off the end', 600, 292, { align: 'center', size: 10, fill: P.faint });
      A.txt(ctx, 'The strange, wonderful part: the targets y are computed using the SAME network you are training.',
        40, 320, { size: 12, w: 700, fill: P.soft });
      A.txt(ctx, 'You are chasing a moving target — and, remarkably, it converges anyway.', 40, 340,
        { size: 12, w: 700, fill: P.a });
      ro.set('This is <b>DQN</b> — the algorithm behind DeepMind’s Atari results in 2013–2015.' +
        '\nThe replay buffer matters more than it looks: consecutive frames are highly correlated, and ' +
        'training on them in order makes the network unstable. Sampling randomly from the buffer breaks that ' +
        'correlation.');
    }
    A.bind(c, function () { render(lt); });
    var lt = 0; A.loop(c.cv, function (t) { lt = t; render(t); });
  });

  /* ============================================================
     13. Improved network architecture
     ============================================================ */
  A.def('dqnarch', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var ro = A.readout(root);
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var pass = Math.floor((t * 1.2) % 5);
      /* left: naive */
      A.txt(ctx, '✗ the obvious way', 190, 40, { align: 'center', size: 13, w: 700, fill: P.r });
      A.rr(ctx, 60, 54, 260, 34, 7); ctx.fillStyle = P.sunk; ctx.fill();
      ctx.strokeStyle = P.lineSoft; ctx.stroke();
      A.txt(ctx, 'input: 8 state numbers + 4 one-hot action = 12', 190, 76,
        { align: 'center', size: 11, mono: true, fill: P.soft });
      var l1 = A.col(190, 4, 112, 178, 12), l2 = A.col(190, 1, 210, 210, 14);
      l1.forEach(function (p) { A.neuron(ctx, p, .7, P, null, null, P.faint); });
      A.neuron(ctx, l2[0], .8, P, null, null, P.r);
      l1.forEach(function (p) { A.link(ctx, p, l2[0], P.line, .8, .3); });
      A.txt(ctx, 'output: Q(s, a) — ONE number', 190, 248, { align: 'center', size: 11, fill: P.r });
      A.txt(ctx, 'to pick an action you must run it', 190, 272, { align: 'center', size: 11, fill: P.faint });
      A.txt(ctx, 'FOUR separate times, once per action', 190, 288, { align: 'center', size: 11, w: 700, fill: P.r });
      for (var k = 0; k < 4; k++) {
        A.dot(ctx, 130 + k * 40, 306, 6, pass > k ? P.r : P.line);
      }
      A.txt(ctx, 'forward passes: ' + Math.min(4, pass), 190, 326, { align: 'center', size: 11, mono: true, fill: P.faint });
      A.line(ctx, 380, 40, 380, 300, P.lineSoft, 1.4, [5, 5]);
      /* right: improved */
      A.txt(ctx, '✓ the improved way', 570, 40, { align: 'center', size: 13, w: 700, fill: P.g });
      A.rr(ctx, 440, 54, 260, 34, 7); ctx.fillStyle = P.gS; ctx.fill();
      ctx.strokeStyle = P.g; ctx.lineWidth = 1.6; ctx.stroke();
      A.txt(ctx, 'input: just the 8 state numbers', 570, 76, { align: 'center', size: 11, mono: true, fill: P.g });
      var r1 = A.col(570, 4, 112, 178, 12), r2 = A.col(570, 4, 196, 268, 12);
      r1.forEach(function (p) { A.neuron(ctx, p, .7, P, null, null, P.faint); });
      r1.forEach(function (p) { r2.forEach(function (q) { A.link(ctx, p, q, P.line, .8, .3); }); });
      var names = ['nothing', 'left', 'main', 'right'];
      r2.forEach(function (p, i) {
        A.neuron(ctx, p, .8, P, null, null, P.g);
        A.txt(ctx, 'Q(s, ' + names[i] + ')', p.x + 22, p.y + 4, { size: 10.5, mono: true, fill: P.g });
      });
      A.txt(ctx, 'all four Q values in ONE forward pass', 570, 296,
        { align: 'center', size: 11.5, w: 700, fill: P.g });
      A.dot(ctx, 570, 314, 6, P.g);
      A.txt(ctx, 'forward passes: 1', 570, 328, { align: 'center', size: 11, mono: true, fill: P.faint });
      ro.set('Same network, reorganised: put the actions on the <b>output</b> side instead of the input side.' +
        '\nFour times less compute every single time the agent picks an action — and picking an action happens ' +
        'millions of times during training. It also makes max<sub>a′</sub> Q(s′, a′) a single <code>max()</code> ' +
        'over four numbers you already have.');
    }
    A.bind(c, function () { render(lt); });
    var lt = 0; A.loop(c.cv, function (t) { lt = t; render(t); });
  });

  /* ============================================================
     14. ε-greedy policy
     ============================================================ */
  A.def('epsilongreedy', function (root) {
    var c = A.canvas(root, 760, 340), ctx = c.ctx;
    var eps = 0.3;
    var bar = A.ctrls(root), ro = A.readout(root);
    A.slider(bar, { label: 'ε', min: 0, max: 1, step: .01, value: eps,
      fmt: function (v) { return v.toFixed(2); }, on: function (v) { eps = v; render(); } });
    var Q = [12, 31, 24, 9];
    var names = ['do nothing', 'left thruster', 'main engine', 'right thruster'];
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var tick = Math.floor(t * 1.6);
      var r1 = ((Math.sin(tick * 91.7) * 4351.17) % 1 + 1) % 1;
      var r2 = ((Math.sin(tick * 27.3) * 1731.9) % 1 + 1) % 1;
      var exploring = r1 < eps;
      var chosen = exploring ? Math.floor(r2 * 4) : 1;
      A.txt(ctx, 'the network currently believes:', 40, 40, { size: 12.5, w: 700, fill: P.soft });
      Q.forEach(function (q, i) {
        var y = 56 + i * 40, isBest = i === 1, isChosen = i === chosen;
        A.rr(ctx, 200, y, 300, 30, 6);
        ctx.fillStyle = isChosen ? (exploring ? P.pS : P.aS) : P.sunk; ctx.fill();
        ctx.strokeStyle = isChosen ? (exploring ? P.p : P.a) : P.lineSoft;
        ctx.lineWidth = isChosen ? 2.2 : 1; ctx.stroke();
        A.rr(ctx, 202, y + 2, 296 * q / 40, 26, 5);
        ctx.fillStyle = isBest ? P.a : P.faint; ctx.globalAlpha = .28; ctx.fill(); ctx.globalAlpha = 1;
        A.txt(ctx, names[i], 190, y + 20, { align: 'right', size: 12, w: isChosen ? 700 : 500,
          fill: isChosen ? (exploring ? P.p : P.a) : P.soft });
        A.txt(ctx, 'Q = ' + q, 510, y + 20, { size: 12, mono: true, fill: P.faint });
        if (isBest) A.txt(ctx, '← greedy choice', 570, y + 20, { size: 11, w: 700, fill: P.a });
        if (isChosen) A.txt(ctx, '✓ TAKEN', 700, y + 20, { align: 'right', size: 12, w: 700,
          fill: exploring ? P.p : P.a });
      });
      A.rr(ctx, 40, 226, 680, 44, 8);
      ctx.fillStyle = exploring ? P.pS : P.aS; ctx.fill();
      ctx.strokeStyle = exploring ? P.p : P.a; ctx.lineWidth = 1.8; ctx.stroke();
      A.txt(ctx, exploring
        ? 'EXPLORING (' + (eps * 100).toFixed(0) + '% of the time) — pick at random, just to see what happens'
        : 'EXPLOITING (' + ((1 - eps) * 100).toFixed(0) + '% of the time) — take whatever Q says is best',
        380, 253, { align: 'center', size: 13.5, w: 700, fill: exploring ? P.p : P.a });
      A.txt(ctx, 'Why explore at all? Because a randomly-initialised Q might permanently believe “firing the main',
        40, 292, { size: 11.5, fill: P.soft });
      A.txt(ctx, 'engine is bad”. If you never try it, you never find out otherwise — and never fix the belief.',
        40, 310, { size: 11.5, fill: P.soft });
      A.txt(ctx, 'Standard practice: start at ε = 1.0 (all random) and decay it towards 0.01 as Q gets good.',
        40, 332, { size: 12, w: 700, fill: P.a });
      ro.set('With probability <b>1 − ε</b>: take argmax<sub>a</sub> Q(s, a).  With probability <b>ε</b>: pick at random.' +
        '\nConfusingly, the “greedy” part is the 1 − ε part. Some texts call this “ε-greedy exploration”; ' +
        'either way ε is the fraction of the time you deliberately ignore your own advice.');
    }
    A.bind(c, function () { render(lt); });
    var lt = 0; A.loop(c.cv, function (t) { lt = t; render(t); });
  });

  /* ============================================================
     15. Mini-batch and soft updates
     ============================================================ */
  A.def('minibatch', function (root) {
    var c = A.canvas(root, 760, 330), ctx = c.ctx;
    var tau = 0.01;
    var bar = A.ctrls(root), ro = A.readout(root);
    A.slider(bar, { label: 'τ (soft update)', min: .001, max: 1, step: .001, value: tau,
      fmt: function (v) { return v.toFixed(3); }, on: function (v) { tau = v; render(); } });
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      /* mini-batch */
      A.txt(ctx, 'MINI-BATCH — do not use all 10,000 tuples every step', 40, 38,
        { size: 12.5, w: 700, fill: P.b });
      var pick = Math.floor(t * .8) % 5;
      for (var i = 0; i < 50; i++) {
        var x = 46 + (i % 25) * 26, y = 54 + Math.floor(i / 25) * 24;
        var inBatch = (i % 5) === pick;
        A.rr(ctx, x, y, 22, 18, 3);
        ctx.fillStyle = inBatch ? P.bS : P.sunk; ctx.fill();
        ctx.strokeStyle = inBatch ? P.b : P.lineSoft; ctx.lineWidth = inBatch ? 1.6 : 1; ctx.stroke();
      }
      A.txt(ctx, 'each step trains on a random subset of 1,000 — noisier per step, far more steps per second',
        46, 122, { size: 11, fill: P.faint });
      A.txt(ctx, 'the same trick works for ordinary gradient descent on any large dataset', 46, 140,
        { size: 11, fill: P.faint });
      /* soft update */
      A.txt(ctx, 'SOFT UPDATE — do not replace Q with Q_new all at once', 40, 178,
        { size: 12.5, w: 700, fill: P.a });
      var barX = 60, barW = 460;
      A.rr(ctx, barX, 200, barW, 30, 6); ctx.fillStyle = P.sunk; ctx.fill();
      ctx.strokeStyle = P.lineSoft; ctx.stroke();
      A.rr(ctx, barX, 200, barW * tau, 30, 6); ctx.fillStyle = P.a; ctx.globalAlpha = .8; ctx.fill();
      ctx.globalAlpha = 1;
      A.txt(ctx, (tau * 100).toFixed(1) + '% new', barX + 10, 220, { size: 12, w: 700,
        fill: tau > .2 ? P.panel : P.a });
      A.txt(ctx, ((1 - tau) * 100).toFixed(1) + '% old', barX + barW - 10, 220,
        { align: 'right', size: 12, w: 700, fill: P.soft });
      A.txt(ctx, 'W := ' + tau.toFixed(3) + '·W_new + ' + (1 - tau).toFixed(3) + '·W_old', 540, 220,
        { size: 12.5, mono: true, w: 700, fill: P.a });
      var msg = tau > .5 ? ['τ near 1 — the same as replacing it outright. Q can lurch and oscillate.', P.r]
        : tau < .02 ? ['τ small — Q creeps forward. Much more stable, and the usual choice.', P.g]
        : ['a middle value — faster than 0.01, less stable.', P.m];
      A.txt(ctx, msg[0], 60, 258, { size: 12.5, w: 700, fill: msg[1] });
      A.txt(ctx, 'Remember the targets y are computed FROM Q. If Q jumps, every target jumps, and the network',
        40, 292, { size: 11.5, fill: P.soft });
      A.txt(ctx, 'is chasing a target that keeps moving. Soft updates stop the target moving so violently.',
        40, 310, { size: 11.5, w: 700, fill: P.a });
      ro.set('Two refinements that turn “sometimes works” into “reliably works”:' +
        '\n<b>Mini-batch</b> — train on a random 1,000 of the 10,000 stored tuples each step.' +
        '\n<b>Soft update</b> — blend the new weights into the old ones instead of swapping them, so the ' +
        'training targets change smoothly.');
    }
    A.bind(c, function () { render(lt); });
    var lt = 0; A.loop(c.cv, function (t) { lt = t; render(t); });
  });

  /* ============================================================
     16. The state of reinforcement learning
     ============================================================ */
  A.def('rlstate', function (root) {
    var c = A.canvas(root, 760, 320), ctx = c.ctx;
    function render(t) {
      var P = A.pal(); c.clear(P.panel); t = t || 0;
      var rows = [
        ['works beautifully in a simulator', 1, 'games, physics sims, the lunar lander you just built'],
        ['much harder on real robots', 0, 'the simulator is never the real world'],
        ['very sensitive to the reward function', 0, 'small changes → wildly different behaviour'],
        ['needs an enormous number of trials', 0, 'fine in sim, impossible if each trial costs a real drone'],
        ['fewer production applications than supervised learning', 0, 'this is Andrew’s own honest framing'],
        ['a genuinely exciting research direction', 1, 'and the foundation of RLHF, which aligns modern LLMs']
      ];
      var hot = Math.floor((t * .5) % rows.length);
      A.txt(ctx, 'An honest scorecard, in Andrew’s own framing', 40, 38, { size: 13.5, w: 700, fill: P.soft });
      rows.forEach(function (r, i) {
        var y = 54 + i * 40, on = i === hot, good = r[1] === 1;
        A.rr(ctx, 40, y, 680, 34, 7);
        ctx.fillStyle = on ? (good ? P.gS : P.mS) : P.sunk; ctx.fill();
        ctx.strokeStyle = on ? (good ? P.g : P.m) : P.lineSoft; ctx.lineWidth = on ? 1.8 : 1; ctx.stroke();
        A.txt(ctx, good ? '✓' : '⚠', 62, y + 23, { align: 'center', size: 14, w: 700,
          fill: good ? P.g : P.m });
        A.txt(ctx, r[0], 84, y + 22, { size: 12, w: on ? 700 : 500,
          fill: on ? (good ? P.g : P.m) : P.soft });
        A.txt(ctx, r[2], 710, y + 22, { align: 'right', size: 10.5, fill: P.faint });
      });
      A.txt(ctx, 'The hype exceeds the deployed reality — and the ideas are still worth knowing, because RL from',
        40, 300, { size: 11.5, fill: P.soft });
      A.txt(ctx, 'human feedback is how every modern chat model is tuned.', 40, 318,
        { size: 11.5, w: 700, fill: P.a });
    }
    A.bind(c, function () { render(lt); });
    var lt = 0; A.loop(c.cv, function (t) { lt = t; render(t); });
  });

})();
