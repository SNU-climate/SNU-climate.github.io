/* Climate Dashboard v02 — 연구실 타임라인, 연구 지역 레이더 지도, 공저 네트워크.
   데이터는 모두 빌드된 HTML(data-* 속성, JSON 조각)과 assets/data/gistemp.js에서만 읽는다. 외부 요청 없음. */
(function () {
  'use strict';
  var SVGNS = 'http://www.w3.org/2000/svg';

  function ready(fn) {
    if (document.readyState !== 'loading') fn();
    else document.addEventListener('DOMContentLoaded', fn);
  }
  function $(sel, root) { return (root || document).querySelector(sel); }
  function $$(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }
  function el(tag, attrs, text) {
    var e = document.createElement(tag);
    for (var k in attrs || {}) e.setAttribute(k, attrs[k]);
    if (text != null) e.textContent = text;
    return e;
  }
  function svg(tag, attrs) {
    var e = document.createElementNS(SVGNS, tag);
    for (var k in attrs || {}) e.setAttribute(k, attrs[k]);
    return e;
  }

  /* ---------------------------------------------------------------- 1. 기후 × 연구실 타임라인 */
  function initTimeline() {
    var root = $('[data-timeline]');
    if (!root) return;
    var plot = $('[data-tl-plot]', root), read = $('[data-tl-read]', root), sum = $('[data-tl-sum]', root);
    var cols = $$('[data-tl-col]', root);
    var S = window.CSL_STRIPES;
    var na = root.getAttribute('data-na') || 'ΔT n/a';
    var labLabel = root.getAttribute('data-lab-label') || 'lab-led';
    var papersLabel = root.getAttribute('data-papers-label') || 'papers';

    function anomOf(y) {
      if (!S) return null;
      var i = y - S.start;
      return i >= 0 && i < S.anom.length ? S.anom[i] : null;
    }
    // 줄무늬 칸 색칠(GISTEMP 범위 밖이면 빗금)
    cols.forEach(function (c) {
      var v = anomOf(+c.getAttribute('data-y'));
      var cell = $('[data-tl-stripe]', c);
      if (v == null) cell.classList.add('tl-stripe--na');
      else cell.style.background = S.color(v);
    });

    function setSummary() {
      read.textContent = '';
      read.appendChild(el('span', { 'class': 'tl-read-sum' }, sum ? sum.textContent : ''));
    }
    var cur = -1;
    function show(i) {
      cur = Math.max(0, Math.min(cols.length - 1, i));
      var c = cols[cur], y = +c.getAttribute('data-y'), n = +c.getAttribute('data-n'), lab = +c.getAttribute('data-lab');
      cols.forEach(function (x, j) { x.classList.toggle('is-on', j === cur); });
      plot.classList.add('has-on');
      var v = anomOf(y);
      read.textContent = '';
      read.appendChild(el('b', { 'class': 'tl-read-y' }, String(y)));
      read.appendChild(el('span', { 'class': 'tl-read-dt' + (v == null ? ' is-na' : '') }, v == null ? na : 'ΔT ' + S.fmt(v)));
      read.appendChild(el('span', { 'class': 'tl-read-n' }, n + ' ' + papersLabel + (n ? ' · ' + labLabel + ' ' + lab : '')));
      var t = c.getAttribute('data-title');
      if (t) read.appendChild(el('span', { 'class': 'tl-read-t' }, '#' + c.getAttribute('data-num') + ' ' + t));
      plot.setAttribute('aria-valuenow', y);
      plot.setAttribute('aria-valuetext', read.textContent);
    }
    function reset() {
      cur = -1;
      plot.classList.remove('has-on');
      cols.forEach(function (x) { x.classList.remove('is-on'); });
      setSummary();
    }
    setSummary();
    cols.forEach(function (c, i) {
      c.addEventListener('pointerenter', function () { show(i); });
    });
    plot.addEventListener('pointerleave', function () { if (document.activeElement !== plot) reset(); });
    plot.addEventListener('focus', function () { show(cur < 0 ? cols.length - 1 : cur); });
    plot.addEventListener('blur', reset);
    plot.addEventListener('keydown', function (e) {
      var step = { ArrowLeft: -1, ArrowRight: 1, PageDown: -5, PageUp: 5 }[e.key];
      if (step) { e.preventDefault(); show((cur < 0 ? cols.length - 1 : cur) + step); }
      else if (e.key === 'Home') { e.preventDefault(); show(0); }
      else if (e.key === 'End') { e.preventDefault(); show(cols.length - 1); }
      else if (e.key === 'Enter' && cur >= 0 && cols[cur].href) { location.href = cols[cur].href; }
    });
  }

  /* ---------------------------------------------------------------- 2. 연구 지역 레이더 지도 */
  function initMaps() {
    $$('[data-rmap]').forEach(function (map) {
      var box = $('.rmap-box', map), tip = $('[data-rmap-tip]', map);
      var mks = $$('.mk', map);
      var focus = map.getAttribute('data-focus') || '';

      function showTip(mk) {
        if (!tip) return;
        tip.textContent = mk.getAttribute('data-name') + ' — ' + mk.getAttribute('data-topic-title');
        tip.hidden = false;
        var b = box.getBoundingClientRect(), r = mk.getBoundingClientRect();
        var x = r.left + r.width / 2 - b.left, y = r.top - b.top;
        tip.style.left = Math.max(4, Math.min(b.width - tip.offsetWidth - 4, x - tip.offsetWidth / 2)) + 'px';
        tip.style.top = Math.max(4, y - tip.offsetHeight - 6) + 'px';
      }
      function hideTip() { if (tip) tip.hidden = true; }
      mks.forEach(function (mk) {
        mk.addEventListener('pointerenter', function () { showTip(mk); });
        mk.addEventListener('pointerleave', hideTip);
        mk.addEventListener('focus', function () { showTip(mk); });
        mk.addEventListener('blur', hideTip);
      });

      // 주제 강조: key가 비면 전체(또는 페이지 고정 focus)
      function highlight(key) {
        var k = key || focus;
        mks.forEach(function (mk) { mk.classList.toggle('is-dim', !!k && mk.getAttribute('data-topic') !== k); });
        $$('.rmap-legend li', map).forEach(function (li) { li.classList.toggle('is-dim', !!k && li.getAttribute('data-topic') !== k); });
      }

      // 연구 페이지: 주제 필터 → 표시·범례·주제 패널을 함께 거른다
      var filter = $('[data-rmap-filter]', map);
      if (filter) {
        filter.addEventListener('click', function (e) {
          var b = e.target.closest('button[data-topic]');
          if (!b) return;
          var key = b.getAttribute('data-topic');
          $$('button', filter).forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
          highlight(key);
          $$('[data-topic-panel]').forEach(function (p) { p.hidden = !!key && p.getAttribute('data-topic-panel') !== key; });
        });
      }
      // 홈: 왼쪽 주제 행에 올리면 해당 지역만 밝힌다
      var rows = map.parentNode && $('[data-rmap-rows]', map.parentNode);
      if (rows) {
        $$('[data-topic]', rows).forEach(function (row) {
          var key = row.getAttribute('data-topic');
          row.addEventListener('pointerenter', function () { highlight(key); });
          row.addEventListener('focusin', function () { highlight(key); });
          row.addEventListener('pointerleave', function () { highlight(''); });
          row.addEventListener('focusout', function () { highlight(''); });
        });
        mks.forEach(function (mk) {
          var key = mk.getAttribute('data-topic');
          mk.addEventListener('pointerenter', function () {
            $$('[data-topic]', rows).forEach(function (row) { row.classList.toggle('is-on', row.getAttribute('data-topic') === key); });
          });
          mk.addEventListener('pointerleave', function () {
            $$('[data-topic]', rows).forEach(function (row) { row.classList.remove('is-on'); });
          });
        });
      }
    });
  }

  /* ---------------------------------------------------------------- 3. 공저 네트워크 */
  function initCoauth() {
    var root = $('[data-coauth]');
    if (!root) return;
    var raw = $('[data-coauth-json]', root);
    var data;
    try { data = JSON.parse(raw.textContent); } catch (e) { return; }
    var net = $('[data-coauth-net]', root), bars = $('[data-coauth-bars]', root), info = $('[data-coauth-info]', root);
    var period = $('[data-coauth-period]', root);
    var lab = {}; (data.lab || []).forEach(function (n) { lab[n] = true; });
    var LIM = +root.getAttribute('data-limit') || 10, N = 12;
    var T = { withPI: root.getAttribute('data-with'), lab: root.getAttribute('data-lab'), ext: root.getAttribute('data-ext'), pi: root.getAttribute('data-pi') };
    function fam(a) { return String(a).split(',')[0]; }
    function uniq(list) { var s = {}, o = []; (list || []).forEach(function (a) { if (!s[a]) { s[a] = 1; o.push(a); } }); return o; }

    function compute(since) {
      var cnt = {}, span = {}, rows = data.rows.filter(function (r) { return r[0] >= since; });
      rows.forEach(function (r) {
        uniq(r[1]).forEach(function (a) {
          if (fam(a) === data.pi) return;
          cnt[a] = (cnt[a] || 0) + 1;
          var s = span[a] || [r[0], r[0]];
          span[a] = [Math.min(s[0], r[0]), Math.max(s[1], r[0])];
        });
      });
      var names = Object.keys(cnt).sort(function (a, b) { return cnt[b] - cnt[a] || (a < b ? -1 : 1); });
      var top = names.slice(0, N), idx = {};
      top.forEach(function (a, i) { idx[a] = i; });
      var pair = {};
      rows.forEach(function (r) {
        var ids = uniq(r[1]).filter(function (a) { return a in idx; }).map(function (a) { return idx[a]; }).sort(function (a, b) { return a - b; });
        for (var i = 0; i < ids.length; i++) for (var j = i + 1; j < ids.length; j++) {
          var k = ids[i] + ',' + ids[j];
          pair[k] = (pair[k] || 0) + 1;
        }
      });
      return { cnt: cnt, span: span, names: names, top: top, pair: pair, papers: rows.length };
    }

    function describe(res, a) {
      var s = res.span[a];
      return a + ' — ' + res.cnt[a] + ' ' + T.withPI + ' · ' + s[0] + (s[1] !== s[0] ? '–' + s[1] : '') + ' · ' + (lab[a] ? T.lab : T.ext);
    }

    function renderBars(res) {
      bars.textContent = '';
      var top = res.names.slice(0, LIM), max = top.length ? res.cnt[top[0]] : 1;
      top.forEach(function (a) {
        var li = el('li', { 'class': 'hb' + (lab[a] ? ' hb--lab' : '') });
        li.appendChild(el('span', { 'class': 'hb-label' }, a));
        li.appendChild(el('span', { 'class': 'hb-n mono' }, String(res.cnt[a])));
        var tr = el('span', { 'class': 'hb-track', 'aria-hidden': 'true' });
        var f = el('span', { 'class': 'hb-fill' }); f.style.width = (res.cnt[a] / max * 100).toFixed(1) + '%';
        tr.appendChild(f); li.appendChild(tr);
        li.appendChild(el('span', { 'class': 'hb-sub mono' }, res.span[a][0] + '–' + res.span[a][1]));
        bars.appendChild(li);
      });
    }

    function renderNet(res) {
      net.textContent = '';
      var W = 460, C = W / 2, R = 150;
      var s = svg('svg', { viewBox: '0 0 ' + W + ' ' + W, 'class': 'net-svg', role: 'group', 'aria-label': root.closest('section') ? (root.closest('section').querySelector('.panel-t') || {}).textContent || '' : '' });
      var gE = svg('g', { 'class': 'net-edges' }), gS = svg('g', { 'class': 'net-spokes' }), gN = svg('g', { 'class': 'net-nodes' });
      s.appendChild(gE); s.appendChild(gS); s.appendChild(gN);
      var top = res.top, max = top.length ? res.cnt[top[0]] : 1;
      var pos = top.map(function (a, i) {
        var ang = -Math.PI / 2 + i * 2 * Math.PI / top.length;
        return { x: C + R * Math.cos(ang), y: C + R * Math.sin(ang), ang: ang };
      });
      // 공저자끼리의 선(같은 논문에 2편 이상)
      var pmax = 1, k;
      for (k in res.pair) pmax = Math.max(pmax, res.pair[k]);
      var edges = [];
      for (k in res.pair) {
        if (res.pair[k] < 2) continue;
        var ij = k.split(','), a = pos[+ij[0]], b = pos[+ij[1]];
        var mx = (a.x + b.x) / 2, my = (a.y + b.y) / 2;
        var cx = mx + (C - mx) * 0.55, cy = my + (C - my) * 0.55;
        var p = svg('path', { d: 'M' + a.x.toFixed(1) + ' ' + a.y.toFixed(1) + 'Q' + cx.toFixed(1) + ' ' + cy.toFixed(1) + ' ' + b.x.toFixed(1) + ' ' + b.y.toFixed(1),
          'class': 'net-edge', 'stroke-width': (0.6 + 3 * res.pair[k] / pmax).toFixed(2), 'data-i': ij[0], 'data-j': ij[1] });
        p.style.opacity = (0.18 + 0.5 * res.pair[k] / pmax).toFixed(2);
        gE.appendChild(p); edges.push(p);
      }
      // 교수 ↔ 공저자(굵기 = 공저 수)
      var spokes = pos.map(function (q, i) {
        var l = svg('line', { x1: C, y1: C, x2: q.x.toFixed(1), y2: q.y.toFixed(1), 'class': 'net-spoke' + (lab[top[i]] ? ' is-lab' : ''),
          'stroke-width': (1 + 5 * res.cnt[top[i]] / max).toFixed(2) });
        gS.appendChild(l);
        return l;
      });
      // 가운데 교수 노드
      var piG = svg('g', { 'class': 'net-pi' });
      piG.appendChild(svg('circle', { cx: C, cy: C, r: 26 }));
      var pt = svg('text', { x: C, y: C + 4, 'text-anchor': 'middle' }); pt.textContent = T.pi;
      piG.appendChild(pt);
      var nodes = top.map(function (a, i) {
        var q = pos[i], r = 5 + 10 * Math.sqrt(res.cnt[a] / max);
        var g = svg('g', { 'class': 'net-node' + (lab[a] ? ' is-lab' : ''), tabindex: '0', role: 'img', 'aria-label': describe(res, a) });
        g.appendChild(svg('circle', { cx: q.x.toFixed(1), cy: q.y.toFixed(1), r: r.toFixed(1) }));
        var cos = Math.cos(q.ang), sin = Math.sin(q.ang), d = r + 6;
        var t = svg('text', { x: (q.x + cos * d).toFixed(1), y: (q.y + sin * d + 4 + (sin > 0.9 ? 6 : sin < -0.9 ? -4 : 0)).toFixed(1),
          'text-anchor': cos > 0.25 ? 'start' : cos < -0.25 ? 'end' : 'middle' });
        t.textContent = a;
        g.appendChild(t);
        var n = svg('text', { x: q.x.toFixed(1), y: (q.y + 4).toFixed(1), 'text-anchor': 'middle', 'class': 'net-n' });
        n.textContent = res.cnt[a];
        if (r >= 10) g.appendChild(n);
        gN.appendChild(g);
        function on() {
          s.classList.add('has-on');
          nodes.forEach(function (x, j) { x.classList.toggle('is-on', j === i); });
          spokes.forEach(function (x, j) { x.classList.toggle('is-on', j === i); });
          edges.forEach(function (x) { x.classList.toggle('is-on', +x.getAttribute('data-i') === i || +x.getAttribute('data-j') === i); });
          info.textContent = describe(res, a);
        }
        function off() {
          s.classList.remove('has-on');
          [].concat(nodes, spokes, edges).forEach(function (x) { x.classList.remove('is-on'); });
          info.textContent = '';
        }
        g.addEventListener('pointerenter', on); g.addEventListener('focus', on);
        g.addEventListener('pointerleave', off); g.addEventListener('blur', off);
        return g;
      });
      gN.appendChild(piG);
      net.appendChild(s);
    }

    function run(since) {
      var res = compute(since);
      renderNet(res);
      renderBars(res);
      info.textContent = '';
    }
    if (period) {
      period.hidden = false;
      period.addEventListener('click', function (e) {
        var b = e.target.closest('button[data-since]');
        if (!b) return;
        $$('button', period).forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
        run(+b.getAttribute('data-since'));
      });
    }
    run(0);
  }

  ready(function () {
    initTimeline();
    initMaps();
    initCoauth();
  });
})();
