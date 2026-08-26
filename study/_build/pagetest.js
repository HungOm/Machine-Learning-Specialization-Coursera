/* Load real built pages in jsdom, run the real scripts, assert on the result.
   External <script src> are NOT fetched (offline site, file:// URLs) — the test
   injects exactly the files on disk instead, so what runs is what ships. */
/* jsdom is the only dependency and is not vendored. Point JSDOM at it if it is
   not resolvable from here, e.g.
     JSDOM=$HOME/node_modules/jsdom STUDY_ROOT=$PWD/study node your-test.js   */
const { JSDOM, VirtualConsole } = require(process.env.JSDOM || 'jsdom');
const fs = require('fs'), path = require('path');
const ROOT = process.env.STUDY_ROOT;

function loadPage(rel, { storage = {}, scripts = [] } = {}) {
  const file = path.join(ROOT, rel);
  const vc = new VirtualConsole();
  const errs = [];
  vc.on('jsdomError', e => errs.push('jsdomError: ' + (e.message || e)));
  vc.on('error', (...a) => errs.push('console.error: ' + a.join(' ')));

  const dom = new JSDOM(fs.readFileSync(file, 'utf8'), {
    url: 'file://' + file,
    runScripts: 'dangerously',
    pretendToBeVisual: true,
    virtualConsole: vc,
    beforeParse(win) {
      const store = Object.assign({}, storage);
      Object.defineProperty(win, 'localStorage', {
        value: {
          getItem: k => (k in store ? store[k] : null),
          setItem: (k, v) => { store[k] = String(v); },
          removeItem: k => { delete store[k]; },
          clear: () => { for (const k in store) delete store[k]; },
          get length() { return Object.keys(store).length; },
          key: i => Object.keys(store)[i] ?? null,
          _dump: () => store,
        }, configurable: true,
      });
      win.HTMLCanvasElement.prototype.getContext = () => new Proxy({}, {
        get: (t, p) => p === 'canvas' ? { width: 600, height: 300 }
          : p === 'measureText' ? (() => ({ width: 20 }))
          : p === 'createLinearGradient' || p === 'createRadialGradient' ? (() => ({ addColorStop() {} }))
          : (typeof p === 'string' ? (() => {}) : undefined),
        set: () => true,
      });
      win.matchMedia = q => ({ matches: false, media: q, onchange: null,
        addListener() {}, removeListener() {}, addEventListener() {}, removeEventListener() {}, dispatchEvent() {} });
      win.requestAnimationFrame = () => 0;
      win.cancelAnimationFrame = () => {};
      win.scrollTo = () => {};
      win.print = () => { win.__printed = (win.__printed || 0) + 1; };
      win.URL.createObjectURL = () => 'blob:fake';
      win.URL.revokeObjectURL = () => {};
      win.getComputedStyle = () => ({ getPropertyValue: () => '#888', fontSize: '14px' });
    },
  });

  const win = dom.window, doc = win.document;
  return new Promise(res => {
    function go() {
      // run the site's own scripts, in order, against the parsed DOM
      for (const rel of scripts) {
        const s = doc.createElement('script');
        s.textContent = fs.readFileSync(path.join(ROOT, rel), 'utf8');
        doc.head.appendChild(s);
      }
      doc.dispatchEvent(new win.Event('DOMContentLoaded', { bubbles: true }));
      res({ dom, win, doc, errs, storage: win.localStorage });
    }
    if (doc.readyState === 'complete') go();
    else win.addEventListener('load', go);
  });
}
module.exports = { loadPage, ROOT };
