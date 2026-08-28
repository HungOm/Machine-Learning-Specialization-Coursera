/* Headless smoke test: mount every widget, run a few animation frames,
   and report any runtime error. Stubs just enough DOM + canvas. */
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ASSETS = process.argv[2];
const files = process.argv.slice(3);

function ctxStub() {
  const noop = () => {};
  const target = {
    measureText: () => ({ width: 20 }),
    createLinearGradient: () => ({ addColorStop: noop }),
    createRadialGradient: () => ({ addColorStop: noop }),
    getImageData: () => ({ data: new Uint8ClampedArray(4) }),
    setTransform: noop, save: noop, restore: noop,
  };
  return new Proxy(target, {
    get(t, k) {
      if (k in t) return t[k];
      if (typeof k === 'symbol') return undefined;
      return (...a) => undefined;
    },
    set() { return true; }
  });
}

function el(tag) {
  const node = {
    tagName: (tag || 'div').toUpperCase(),
    children: [], style: {}, dataset: {}, _cls: new Set(),
    innerHTML: '', textContent: '', value: '0',
    clientWidth: 760, clientHeight: 300, offsetTop: 0, width: 760, height: 300,
    appendChild(c) { c.parentNode = this; this.children.push(c); return c; },
    insertBefore(c, ref) {
      c.parentNode = this;
      const i = ref ? this.children.indexOf(ref) : -1;
      i < 0 ? this.children.push(c) : this.children.splice(i, 0, c);
      return c;
    },
    get nextSibling() {
      const p = this.parentNode; if (!p) return null;
      const i = p.children.indexOf(this);
      return i >= 0 && i + 1 < p.children.length ? p.children[i + 1] : null;
    },
    addEventListener() {}, removeEventListener() {},
    getBoundingClientRect() { return { left: 0, top: 0, width: 760, height: 300 }; },
    getContext() { return this._ctx || (this._ctx = ctxStub()); },
    querySelectorAll(sel) {
      const out = [];
      const byClass = sel.startsWith('.');
      const want = byClass ? sel.slice(1) : sel.toUpperCase();
      (function walk(n) {
        n.children.forEach(c => {
          if (sel === '*' || (byClass ? c._cls.has(want) : c.tagName === want)) out.push(c);
          walk(c);
        });
      })(node);
      out.forEach = Array.prototype.forEach.bind(out);
      return out;
    },
    querySelector() { return null; },
    setAttribute() {}, removeAttribute() {}, getAttribute() { return null; },
    focus() {}, blur() {},
  };
  node.classList = {
    add: c => node._cls.add(c), remove: c => node._cls.delete(c),
    toggle: (c, v) => (v === undefined ? (node._cls.has(c) ? node._cls.delete(c) : node._cls.add(c))
                                       : (v ? node._cls.add(c) : node._cls.delete(c))),
    contains: c => node._cls.has(c)
  };
  return node;
}

const cssVars = {
  '--bg': '#fff', '--bg-panel': '#fff', '--bg-sunk': '#eee', '--ink': '#111',
  '--ink-soft': '#555', '--ink-faint': '#888', '--line': '#ddd', '--line-soft': '#eee',
  '--accent': '#b4531f', '--accent-soft': '#f6e7dc', '--blue': '#2a5d9f', '--blue-soft': '#e2ecf8',
  '--green': '#2f7a4f', '--green-soft': '#e0f0e6', '--purple': '#6b46a8', '--purple-soft': '#ece4f7',
  '--amber': '#9a6b12', '--amber-soft': '#f8eed6', '--red': '#a8322c', '--red-soft': '#f8e2e0',
};

const rafQueue = [];
const win = {
  devicePixelRatio: 2,
  requestAnimationFrame(fn) { rafQueue.push(fn); return rafQueue.length; },
  cancelAnimationFrame() {},
  getComputedStyle() { return { getPropertyValue: k => cssVars[k] || '#888' }; },
  matchMedia() { return { matches: false, addEventListener() {}, addListener() {} }; },
  addEventListener() {}, dispatchEvent() {},
  console,
  localStorage: { getItem: () => null, setItem() {}, removeItem() {} },
};
win.window = win;
const doc = {
  readyState: 'complete',
  documentElement: el('html'),
  body: el('body'),
  createElement: el,
  addEventListener() {},
  querySelectorAll() { const a = []; a.forEach = Array.prototype.forEach.bind(a); return a; },
  querySelector() { return null; },
  getElementById() { return null; },
};
win.document = doc;
win.getComputedStyle = win.getComputedStyle;
doc.documentElement.style.setProperty = () => {};

const sandbox = vm.createContext(win);
sandbox.global = sandbox;
sandbox.globalThis = sandbox;
sandbox.ResizeObserver = class { observe() {} disconnect() {} };
sandbox.IntersectionObserver = class { constructor(cb) { this.cb = cb; } observe() {} disconnect() {} };
sandbox.Event = class { constructor(n) { this.type = n; } };
sandbox.Math = Math; sandbox.JSON = JSON; sandbox.console = console;

for (const f of files) {
  const src = fs.readFileSync(path.join(ASSETS, f), 'utf8');
  vm.runInContext(src, sandbox, { filename: f });
}

const A = sandbox.A;
const names = Object.keys(A.widgets);
if (process.env.LIST_ONLY) { console.log(names.join('\n')); process.exit(0); }
// --list supported
let bad = 0;
for (const name of names) {
  rafQueue.length = 0;
  const root = el('div');
  try {
    A.widgets[name](root, {});
    // drive a handful of frames
    for (let i = 0; i < 6 && rafQueue.length; i++) {
      const fn = rafQueue.shift();
      fn(1000 + i * 900);
    }
    console.log('  ok    ' + name);
  } catch (e) {
    bad++;
    console.log('  FAIL  ' + name + '  →  ' + e.message);
    console.log('        ' + (e.stack || '').split('\n')[1]);
  }
}
console.log(bad ? '\n' + bad + ' widget(s) failed' : '\nall ' + names.length + ' widgets ran clean');
process.exit(bad ? 1 : 0);
