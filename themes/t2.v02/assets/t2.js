/* t2.v02 전용 동작(외부 라이브러리 없음). shared.js(검색·메뉴·영상) 다음에 불러온다.
   1) 홈 논문 연표 띠: 막대에 올리면 그 해 편수  2) 홈 연구 지도: 주제 줄 ↔ 지도 점 강조
   3) 논문 저널·대표·교신·영상 필터(검색어와 함께)  4) 영상이 있는 논문에 영상 링크 */
(function () {
  'use strict';
  function $$(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }

  function initStrip() {
    var out = document.querySelector('[data-strip-out]');
    var bars = $$('.strip-bar[data-y]');
    if (!out || !bars.length) return;
    var last = bars[bars.length - 1];
    function show(b) { out.textContent = b.getAttribute('aria-label'); }
    show(last);
    bars.forEach(function (b) {
      b.addEventListener('mouseenter', function () { show(b); });
      b.addEventListener('focus', function () { show(b); });
      b.addEventListener('mouseleave', function () { show(last); });
      b.addEventListener('blur', function () { show(last); });
    });
  }

  function initMap() {
    var map = document.querySelector('[data-rmap]');
    var rows = $$('[data-rmap-rows] [data-topic]');
    if (!map || !rows.length) return;
    var marks = $$('.rm-mk', map);
    function on(t) {
      map.classList.toggle('is-focus', !!t);
      marks.forEach(function (mk) {
        var hit = !!t && (' ' + mk.getAttribute('data-t') + ' ').indexOf(' ' + t + ' ') !== -1;
        mk.classList.toggle('is-hit', hit);
      });
      rows.forEach(function (r) { r.classList.toggle('is-hit', !!t && r.getAttribute('data-topic') === t); });
    }
    rows.forEach(function (r) {
      var t = r.getAttribute('data-topic');
      r.addEventListener('mouseenter', function () { on(t); });
      r.addEventListener('focus', function () { on(t); });
      r.addEventListener('mouseleave', function () { on(''); });
      r.addEventListener('blur', function () { on(''); });
    });
    marks.forEach(function (mk) {
      var ts = mk.getAttribute('data-t').trim().split(/\s+/);
      function hi() {
        map.classList.add('is-focus');
        marks.forEach(function (x) { x.classList.toggle('is-hit', x === mk); });
        rows.forEach(function (r) { r.classList.toggle('is-hit', ts.indexOf(r.getAttribute('data-topic')) !== -1); });
      }
      mk.addEventListener('mouseenter', hi);
      mk.addEventListener('focus', hi);
      mk.addEventListener('mouseleave', function () { on(''); });
      mk.addEventListener('blur', function () { on(''); });
    });
  }

  function videoMap() {
    var el = document.getElementById('pub-videos');
    if (!el) return null;
    try { return { map: JSON.parse(el.textContent), label: el.getAttribute('data-label') || 'Video' }; } catch (e) { return null; }
  }

  function initPubVideos(vm) {
    if (!vm) return;
    Object.keys(vm.map).forEach(function (id) {
      var li = document.getElementById(id);
      var cite = li && li.querySelector('.pub-cite');
      if (!cite) return;
      var a = document.createElement('a');
      a.className = 'pub-link pub-video';
      a.href = vm.map[id];
      a.textContent = '▶ ' + vm.label;
      cite.appendChild(a);
    });
  }

  function initPubFilters(vm) {
    var box = document.querySelector('[data-pub-filters]');
    var input = document.querySelector('[data-pub-search]');
    if (!box || !input) return;
    var items = $$('[data-pub-item]');
    var years = $$('[data-pub-year]');
    var countEl = document.querySelector('[data-pub-count]');
    var emptyEl = document.querySelector('[data-pub-empty]');
    var vids = (vm && vm.map) || {};
    items.forEach(function (it) {
      var j = it.querySelector('.pub-cite i');
      it._j = j ? j.textContent.trim() : '';
      it._f = !!it.querySelector('.pub-featured');
      it._c = !!it.querySelector('.pub-ca');
      it._v = Object.prototype.hasOwnProperty.call(vids, it.id);
    });
    var st = { journal: '', featured: false, ca: false, video: false };
    function apply() {                       // shared.js 검색이 먼저 돈 뒤 실행된다
      var n = 0;
      items.forEach(function (it) {
        if (it.hidden) return;
        var ok = (!st.journal || it._j === st.journal) && (!st.featured || it._f) && (!st.ca || it._c) && (!st.video || it._v);
        if (!ok) it.hidden = true; else n++;
      });
      years.forEach(function (y) { y.hidden = !y.querySelector('[data-pub-item]:not([hidden])'); });
      if (countEl) countEl.textContent = n;
      if (emptyEl) emptyEl.hidden = n !== 0;
    }
    input.addEventListener('input', apply);
    box.addEventListener('click', function (e) {
      var b = e.target.closest('button');
      if (!b) return;
      var on = b.getAttribute('aria-pressed') !== 'true';
      if (b.hasAttribute('data-journal')) {
        $$('[data-journal]', box).forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
        st.journal = on ? b.getAttribute('data-journal') : '';
      } else {
        st[b.getAttribute('data-toggle')] = on;
      }
      b.setAttribute('aria-pressed', String(on));
      input.dispatchEvent(new Event('input'));   // 검색을 다시 돌리면 apply가 뒤따른다
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    var vm = videoMap();
    initStrip();
    initMap();
    initPubVideos(vm);
    initPubFilters(vm);
  });
})();
