/* Print bar: choose clean (black ink) or colour, then hand off to the browser's
   "Save as PDF". Opt in per page with <body data-printable="Title|Subtitle">. */
(function () {
  'use strict';
  var KEY = 'mls-print-mode-v1';

  function mode() {
    try { return localStorage.getItem(KEY) || 'color'; } catch (e) { return 'color'; }
  }
  function setMode(m) {
    document.documentElement.setAttribute('data-print', m);
    try { localStorage.setItem(KEY, m); } catch (e) { }
    document.querySelectorAll('.printbar [data-pm]').forEach(function (b) {
      b.classList.toggle('on', b.dataset.pm === m);
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    var spec = document.body.dataset.printable;
    if (!spec) return;
    var bits = spec.split('|'), title = bits[0] || document.title, sub = bits[1] || '';
    var main = document.querySelector('main');
    if (!main) return;

    /* running head — only ever visible on paper */
    var head = document.createElement('div');
    head.className = 'print-head';
    head.innerHTML = esc(title) + '<b>' + esc(sub) + '</b>';
    main.insertBefore(head, main.firstChild);

    /* the bar itself */
    var bar = document.createElement('div');
    bar.className = 'printbar';
    bar.innerHTML =
      '<span class="pl">Print / PDF</span>' +
      '<button class="btn" data-pm="mono" title="black ink only, no fills — cheap to print">clean</button>' +
      '<button class="btn" data-pm="color" title="keeps the accent colours; always prints the light theme">colour</button>' +
      '<button class="btn primary" data-go="1">print…</button>' +
      '<span class="ph">⌘P works too · what you filter is what prints</span>';
    main.insertBefore(bar, head.nextSibling);

    bar.querySelectorAll('[data-pm]').forEach(function (b) {
      b.addEventListener('click', function () { setMode(b.dataset.pm); });
    });
    bar.querySelector('[data-go]').addEventListener('click', function () {
      openAll();
      window.print();
    });

    setMode(mode());
  });

  /* a <details> that is shut prints as a shut box — open them first */
  function openAll() {
    document.querySelectorAll('main details:not([open])').forEach(function (d) {
      d.setAttribute('open', ''); d.dataset.wasShut = '1';
    });
  }
  window.addEventListener('afterprint', function () {
    document.querySelectorAll('main details[data-was-shut]').forEach(function (d) {
      d.removeAttribute('open'); delete d.dataset.wasShut;
    });
  });

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }
})();
