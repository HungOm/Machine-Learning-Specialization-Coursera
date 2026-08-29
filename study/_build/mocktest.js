/* Load real built mock-quiz pages in jsdom, answer them, submit, and assert on
   the grading — the same harness idea as pagetest.js, aimed at quiz/*.html.

   jsdom is the only dependency and is not vendored:
     JSDOM=$HOME/node_modules/jsdom STUDY_ROOT=$PWD/study node study/_build/mocktest.js

   Checks the three things that would silently break the lane: that an
   incomplete quiz refuses to mark, that scoring is right in both directions,
   and that a miss lands in localStorage under 'M:' AND resolves back to a
   lesson through META.mockLesson — which is what puts it on the dashboard. */
const { JSDOM, VirtualConsole } = require(process.env.JSDOM || 'jsdom');
const fs = require('fs'), path = require('path');
const ROOT = process.env.STUDY_ROOT;

function load(rel) {
  const file = path.join(ROOT, rel);
  const vc = new VirtualConsole();
  const errs = [];
  vc.on('jsdomError', e => errs.push(e.message));
  const dom = new JSDOM(fs.readFileSync(file, 'utf8'), {
    runScripts: 'outside-only', virtualConsole: vc, url: 'https://x/' + rel,
  });
  const w = dom.window;
  // inject only the scripts this page needs, from disk
  ['assets/meta.js', 'assets/mock.js'].forEach(s => {
    w.eval(fs.readFileSync(path.join(ROOT, s), 'utf8'));
  });
  w.document.dispatchEvent(new w.Event('DOMContentLoaded', { bubbles: true }));
  return { w, errs };
}

let fails = 0;
function ok(cond, msg) { console.log((cond ? '  ok   ' : '  FAIL ') + msg); if (!cond) fails++; }

['quiz/c11.html', 'quiz/c23.html', 'quiz/c33.html'].forEach(page => {
  console.log('\n' + page);
  const { w, errs } = load(page);
  const d = w.document;
  ok(errs.length === 0, 'no runtime errors' + (errs.length ? ': ' + errs[0] : ''));

  const qs = [...d.querySelectorAll('li.mq')];
  ok(qs.length === 10, qs.length + ' questions found');

  const submit = d.getElementById('mq-submit');
  const score = d.getElementById('mq-score');
  const msg = d.getElementById('mq-msg');

  // --- submitting with nothing answered must refuse and say so
  submit.click();
  ok(/still unanswered/.test(msg.textContent), 'refuses to mark an incomplete quiz');
  ok(score.textContent === '—', 'score untouched before marking');

  // --- answer every question CORRECTLY
  qs.forEach(li => {
    li.querySelectorAll('ul.mq-opts > li').forEach(o => {
      if (o.dataset.c === '1') o.querySelector('input').checked = true;
    });
  });
  submit.click();
  ok(score.textContent === '10 / 10', 'all-correct scores 10 / 10 (got ' + score.textContent + ')');
  ok(score.className.indexOf('pass') >= 0, 'marked as a pass');
  ok(qs.every(li => li.classList.contains('marked')), 'every question marked');
  ok(qs.every(li => li.classList.contains('right')), 'every question flagged right');

  const shown = [...d.querySelectorAll('.mq-why')];
  ok(shown.length > 30, shown.length + ' rationales present on the page');
  ok(qs.every(li => [...li.querySelectorAll('input')].every(i => i.disabled)),
     'inputs locked after marking');

  // --- retry clears everything
  d.getElementById('mq-retry').click();
  ok(score.textContent === '—', 'retry resets the score');
  ok(qs.every(li => !li.classList.contains('marked')), 'retry unmarks every question');
  ok(qs.every(li => [...li.querySelectorAll('input')].every(i => !i.checked && !i.disabled)),
     'retry clears and re-enables the inputs');

  // --- answer every question WRONG, and check a miss is recorded for the dashboard
  qs.forEach(li => {
    const wrong = [...li.querySelectorAll('ul.mq-opts > li')].find(o => o.dataset.c === '0');
    if (wrong) wrong.querySelector('input').checked = true;
  });
  submit.click();
  ok(score.textContent === '0 / 10', 'all-wrong scores 0 / 10 (got ' + score.textContent + ')');
  ok(score.className.indexOf('fail') >= 0, 'marked as a fail');

  const Q = JSON.parse(w.localStorage.getItem('mls-quiz-v1') || '{}');
  const mocks = Object.keys(Q).filter(k => k.indexOf('M:') === 0);
  ok(mocks.length === 10, mocks.length + ' misses written to mls-quiz-v1 under M:');
  ok(mocks.every(k => Q[k].r === 0), 'all recorded as missed (r = 0)');

  // the dashboard traces a miss back to a lesson through META.mockLesson
  const map = w.META && w.META.mockLesson || {};
  ok(mocks.every(k => !!map[k.slice(2)]), 'every missed qid resolves to a lesson via META.mockLesson');

  const M = JSON.parse(w.localStorage.getItem('mls-mock-v1') || '{}');
  ok(Object.keys(M).length === 1, 'per-quiz score saved to mls-mock-v1');
});

console.log(fails ? '\n' + fails + ' FAILED' : '\nall mock-quiz assertions passed');
process.exit(fails ? 1 : 0);
