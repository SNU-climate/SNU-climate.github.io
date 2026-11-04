/* t1.v02 전용: 연혁 페이지 연간 기록 펼치기, 홈 배너 연구 그림 넘기기. 외부 라이브러리 없음. */
(function () {
  'use strict';

  // 연혁: #yrYYYY 로 들어오거나 막대를 누르면 그해 연간 기록(<details>)을 연다
  function openYear(id) {
    var sec = document.getElementById(id);
    var d = sec && sec.querySelector('details.yr-rec');
    if (d) d.open = true;
  }
  function fromHash() {
    if (location.hash.indexOf('#yr') === 0) openYear(location.hash.slice(1));
  }

  function initHistory() {
    if (!document.querySelector('.chronicle')) return;
    fromHash();
    window.addEventListener('hashchange', fromHash);
    document.addEventListener('click', function (e) {
      var a = e.target.closest('a[href^="#yr"]');
      if (a) openYear(a.getAttribute('href').slice(1));
    });
    document.querySelectorAll('[data-yr-all]').forEach(function (b) {
      b.addEventListener('click', function () {
        var open = b.getAttribute('data-yr-all') === 'open';
        document.querySelectorAll('details.yr-rec').forEach(function (d) { d.open = open; });
      });
    });
  }

  // 홈 배너: 연구 그림(주제마다 1장) 이전/다음. 자동 전환은 하지 않는다
  function initPlates() {
    document.querySelectorAll('[data-plates]').forEach(function (box) {
      var slides = Array.prototype.slice.call(box.querySelectorAll('[data-plate]'));
      var ctrl = box.querySelector('.plate-ctrl');
      if (slides.length < 2 || !ctrl) return;
      var count = box.querySelector('[data-plate-count]');
      var i = 0;
      function show(k) {
        i = (k + slides.length) % slides.length;
        slides.forEach(function (s, j) { s.hidden = j !== i; });
        if (count) count.textContent = (i + 1) + ' / ' + slides.length;
      }
      box.querySelector('[data-plate-prev]').addEventListener('click', function () { show(i - 1); });
      box.querySelector('[data-plate-next]').addEventListener('click', function () { show(i + 1); });
      ctrl.hidden = false;
      show(0);
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    initHistory();
    initPlates();
  });
})();
