/* One-page Scroll 테마: 스크롤 위치에 따라 [data-spy] 메뉴의 현재 항목을 표시(IntersectionObserver),
   전체 메뉴(sheet)는 링크를 누르거나 Esc를 누르면 닫는다. */
(function () {
  'use strict';
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // 가로로 스크롤되는 메뉴 안에서 현재 항목이 보이도록(세로 스크롤은 건드리지 않음)
  function reveal(bar, a, instant) {
    if (bar.scrollWidth <= bar.clientWidth + 1) return;
    var ar = a.getBoundingClientRect(), br = bar.getBoundingClientRect();
    var left = bar.scrollLeft + (ar.left - br.left) - (bar.clientWidth - ar.width) / 2;
    bar.scrollTo({ left: Math.max(0, left), behavior: (reduce || instant) ? 'auto' : 'smooth' });
  }

  function initSpy(bar) {
    // 상세 페이지: 현재 페이지 칩이 화면 밖에 있으면 보이게
    var here = bar.querySelector('[aria-current="page"]');
    if (here) reveal(bar, here, true);
    if (!('IntersectionObserver' in window)) return;
    var links = Array.prototype.slice.call(bar.querySelectorAll('a[href^="#"]'));
    var byId = {};
    var targets = [];
    links.forEach(function (a) {
      var id = decodeURIComponent(a.getAttribute('href').slice(1));
      var el = id && document.getElementById(id);
      if (!el) return;
      if (!byId[id]) { byId[id] = []; targets.push(el); }
      byId[id].push(a);
    });
    if (!targets.length) return;
    // 같은 섹션을 가리키는 다른 링크(전체 메뉴)도 함께 표시
    var extra = Array.prototype.slice.call(document.querySelectorAll('#sheet a[href^="#"]'));
    extra.forEach(function (a) {
      var id = decodeURIComponent(a.getAttribute('href').slice(1));
      if (byId[id] && bar.matches('.spy')) byId[id].push(a);
    });

    var current = null;
    function setActive(id) {
      if (!id || id === current) return;
      current = id;
      Object.keys(byId).forEach(function (k) {
        byId[k].forEach(function (a) {
          if (k === id) { a.setAttribute('aria-current', 'location'); a.classList.add('is-active'); }
          else { a.removeAttribute('aria-current'); a.classList.remove('is-active'); }
        });
      });
      var a = byId[id][0];
      if (a) reveal(bar, a);
    }

    var visible = {};
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) visible[e.target.id] = e.target; else delete visible[e.target.id];
      });
      var best = null, bestTop = Infinity;
      Object.keys(visible).forEach(function (id) {
        var top = visible[id].getBoundingClientRect().top;
        if (top < bestTop) { bestTop = top; best = id; }
      });
      if (best) setActive(best);
    }, { rootMargin: '-38% 0px -58% 0px', threshold: 0 });
    targets.forEach(function (el) { io.observe(el); });

    // 페이지 맨 아래에서는 마지막 섹션(짧아서 기준선에 닿지 않을 수 있음)을 현재로
    var ticking = false;
    window.addEventListener('scroll', function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () {
        ticking = false;
        var doc = document.documentElement;
        if (window.innerHeight + window.scrollY >= doc.scrollHeight - 4) {
          setActive(targets[targets.length - 1].id);
        }
      });
    }, { passive: true });
  }

  function initSheet() {
    var btn = document.querySelector('[data-nav-toggle][aria-controls="sheet"]');
    var sheet = document.getElementById('sheet');
    if (!btn || !sheet) return;
    function close() { if (btn.getAttribute('aria-expanded') === 'true') btn.click(); }
    sheet.addEventListener('click', function (e) { if (e.target.closest('a')) close(); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && btn.getAttribute('aria-expanded') === 'true') { close(); btn.focus(); }
    });
    // 넓은 화면으로 바뀌면(버튼이 사라지면) 열린 메뉴를 닫는다
    var mq = window.matchMedia('(min-width: 1240px)');
    var onChange = function () { if (mq.matches) close(); };
    if (mq.addEventListener) mq.addEventListener('change', onChange); else if (mq.addListener) mq.addListener(onChange);
  }

  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('[data-spy]').forEach(initSpy);
    initSheet();
  });
})();
