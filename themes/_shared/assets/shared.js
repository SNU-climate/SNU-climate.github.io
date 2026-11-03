/* 공통 동작: YouTube 클릭 로드, 논문 검색, 모바일 메뉴 토글. 모든 테마가 불러온다. */
(function () {
  'use strict';

  // YouTube facade: 클릭하기 전에는 썸네일만 보여주고, 클릭하면 youtube-nocookie iframe으로 바꾼다.
  document.addEventListener('click', function (e) {
    var btn = e.target.closest('.yt-play');
    if (!btn) return;
    var box = btn.closest('.yt-facade');
    var id = box && box.getAttribute('data-yt');
    if (!id) return;
    var f = document.createElement('iframe');
    f.src = 'https://www.youtube-nocookie.com/embed/' + encodeURIComponent(id) + '?autoplay=1&rel=0';
    f.title = btn.getAttribute('aria-label') || 'YouTube video';
    f.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
    f.allowFullscreen = true;
    f.loading = 'lazy';
    box.innerHTML = '';
    box.appendChild(f);
    box.classList.add('yt-loaded');
  });

  // 논문 검색: [data-pub-search] 입력 → [data-pub-item]의 data-search로 필터, 빈 연도 섹션 숨김
  function initPubSearch() {
    var input = document.querySelector('[data-pub-search]');
    if (!input) return;
    var items = Array.prototype.slice.call(document.querySelectorAll('[data-pub-item]'));
    var years = Array.prototype.slice.call(document.querySelectorAll('[data-pub-year]'));
    var countEl = document.querySelector('[data-pub-count]');
    var emptyEl = document.querySelector('[data-pub-empty]');
    function run() {
      var terms = input.value.toLowerCase().trim().split(/\s+/).filter(Boolean);
      var n = 0;
      items.forEach(function (it) {
        var s = it.getAttribute('data-search') || '';
        var ok = terms.every(function (t) { return s.indexOf(t) !== -1; });
        it.hidden = !ok;
        if (ok) n++;
      });
      years.forEach(function (y) {
        y.hidden = !y.querySelector('[data-pub-item]:not([hidden])');
      });
      if (countEl) countEl.textContent = n;
      if (emptyEl) emptyEl.hidden = n !== 0;
    }
    input.addEventListener('input', run);
    var q = new URLSearchParams(location.search).get('q');
    if (q) { input.value = q; run(); }
  }

  // 모바일 메뉴: [data-nav-toggle] 버튼이 aria-controls 대상의 data-open을 토글
  function initNavToggle() {
    document.querySelectorAll('[data-nav-toggle]').forEach(function (btn) {
      var target = document.getElementById(btn.getAttribute('aria-controls'));
      if (!target) return;
      btn.addEventListener('click', function () {
        var open = btn.getAttribute('aria-expanded') === 'true';
        btn.setAttribute('aria-expanded', String(!open));
        target.toggleAttribute('data-open', !open);
        document.documentElement.classList.toggle('nav-open', !open);
      });
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    initPubSearch();
    initNavToggle();
  });
})();
