/* Climate Dashboard — warming stripes (NASA GISTEMP v4, assets/data/gistemp.js) */
(function () {
  'use strict';

  // Ed Hawkins' warming stripes palette (ColorBrewer RdBu, 8 blues + 8 reds)
  var COLORS = ['#08306b', '#08519c', '#2171b5', '#4292c6', '#6baed6', '#9ecae1', '#c6dbef', '#deebf7',
    '#fee0d2', '#fcbba1', '#fc9272', '#fb6a4a', '#ef3b2c', '#cb181d', '#a50f15', '#67000d'];

  function ready(fn) {
    if (document.readyState !== 'loading') fn();
    else document.addEventListener('DOMContentLoaded', fn);
  }

  ready(function () {
    var G = window.GISTEMP;
    var ko = document.documentElement.lang === 'ko';
    if (!G || !G.anom || !G.anom.length) {
      // 자료가 없으면 stripes 영역과 출처 문구를 숨긴다
      document.querySelectorAll('.stripes-hero, [data-gistemp-credit], [data-stripe-band]').forEach(function (el) { el.hidden = true; });
      return;
    }
    var a = G.anom, n = a.length, start = G.start, end = start + n - 1;

    // 색 척도: 1971–2000 평균을 중심으로 대칭(Hawkins 방식). 표시 수치는 원자료(1951–1980 기준 편차) 그대로.
    var i0 = Math.max(0, 1971 - start), i1 = Math.min(n - 1, 2000 - start), ref = 0, c = 0, i;
    for (i = i0; i <= i1; i++) { ref += a[i]; c++; }
    if (!c) { for (i = 0; i < n; i++) ref += a[i]; c = n; }
    ref /= c;
    var L = 0;
    for (i = 0; i < n; i++) L = Math.max(L, Math.abs(a[i] - ref));
    function color(v) {
      var k = Math.floor(((v - ref) / (L || 1) + 1) / 2 * COLORS.length);
      return COLORS[Math.max(0, Math.min(COLORS.length - 1, k))];
    }
    function fmt(v) { return (v > 0 ? '+' : v < 0 ? '−' : '±') + Math.abs(v).toFixed(2) + ' °C'; }

    var stops = a.map(function (v, j) {
      return color(v) + ' ' + (j / n * 100).toFixed(4) + '% ' + ((j + 1) / n * 100).toFixed(4) + '%';
    }).join(',');
    var grad = 'linear-gradient(90deg,' + stops + ')';

    document.querySelectorAll('[data-gistemp-period]').forEach(function (el) { el.textContent = start + '–' + end; });
    document.querySelectorAll('[data-stripe-band]').forEach(function (el) { el.style.backgroundImage = grad; });

    var box = document.querySelector('[data-stripes]');
    if (!box) return;
    box.style.backgroundImage = grad;
    var cursor = box.querySelector('[data-stripes-cursor]');
    var out = document.querySelector('[data-stripes-readout]');
    var hot = 0;
    for (i = 1; i < n; i++) if (a[i] > a[hot]) hot = i;
    var summary = end + ' ' + fmt(a[n - 1]) + ' · ' + (ko ? '최고 ' : 'warmest ') + (start + hot) + ' ' + fmt(a[hot]);
    // 키보드로 연도를 고를 수 있는 slider (←/→, PageUp/Down, Home/End)
    box.setAttribute('role', 'slider');
    box.setAttribute('tabindex', '0');
    box.setAttribute('aria-label', (box.getAttribute('data-label') || 'Warming stripes') + ' ' + start + '–' + end + ', NASA GISTEMP v4');
    box.setAttribute('aria-valuemin', start);
    box.setAttribute('aria-valuemax', end);
    box.setAttribute('aria-valuenow', end);
    box.setAttribute('aria-valuetext', summary);
    if (out) out.textContent = summary;

    var cur = -1;
    function show(j) {
      cur = Math.max(0, Math.min(n - 1, j));
      if (cursor) {
        cursor.hidden = false;
        cursor.style.left = (cur / n * 100) + '%';
        cursor.style.width = Math.max(100 / n, 0.35) + '%';
      }
      var txt = (start + cur) + ' ΔT ' + fmt(a[cur]);
      if (out) out.textContent = txt;
      box.setAttribute('aria-valuenow', start + cur);
      box.setAttribute('aria-valuetext', txt);
    }
    function reset() {
      cur = -1;
      if (cursor) cursor.hidden = true;
      if (out) out.textContent = summary;
    }
    box.addEventListener('pointermove', function (e) {
      var r = box.getBoundingClientRect();
      show(Math.floor((e.clientX - r.left) / r.width * n));
    });
    box.addEventListener('pointerleave', function () { if (document.activeElement !== box) reset(); });
    box.addEventListener('focus', function () { show(n - 1); });
    box.addEventListener('blur', reset);
    box.addEventListener('keydown', function (e) {
      var step = { ArrowLeft: -1, ArrowRight: 1, PageDown: -10, PageUp: 10 }[e.key];
      if (step) { e.preventDefault(); show((cur < 0 ? n - 1 : cur) + step); }
      else if (e.key === 'Home') { e.preventDefault(); show(0); }
      else if (e.key === 'End') { e.preventDefault(); show(n - 1); }
    });
  });
})();
