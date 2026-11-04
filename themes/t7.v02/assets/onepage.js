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

  // 모바일 홈: 아래로 스크롤하면 섹션 칩 줄을 숨기고(상단 고정 영역 61px), 위로 스크롤하면 다시 보인다
  function initAutoHide() {
    var bar = document.querySelector('.bar');
    if (!bar || !document.body.classList.contains('is-home')) return;
    var mq = window.matchMedia('(max-width: 1239.98px)');
    var lastY = window.scrollY, ticking = false;
    function update() {
      ticking = false;
      var y = window.scrollY;
      if (!mq.matches || y < 140) { bar.classList.remove('is-compact'); lastY = y; return; }
      if (Math.abs(y - lastY) < 10) return;
      bar.classList.toggle('is-compact', y > lastY);
      lastY = y;
    }
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(update); }
    }, { passive: true });
    // 키보드로 칩에 들어오면 항상 보이게
    bar.addEventListener('focusin', function () { bar.classList.remove('is-compact'); });
  }

  // v02 · 연구 스크롤 스토리: 단계(.story-step)가 화면 가운데에 오면 고정된 그림판(.story-stage)의 그림을 바꾼다
  function initStory() {
    if (!('IntersectionObserver' in window)) return;
    document.querySelectorAll('[data-story]').forEach(function (sec) {
      var steps = Array.prototype.slice.call(sec.querySelectorAll('.story-step'));
      var imgs = Array.prototype.slice.call(sec.querySelectorAll('.story-img'));
      var dots = Array.prototype.slice.call(sec.querySelectorAll('.story-dots li'));
      if (steps.length < 2 || !imgs.length) return;
      function show(i) {
        steps.forEach(function (s, k) { s.classList.toggle('is-active', k === i); });
        imgs.forEach(function (a, k) { a.classList.toggle('is-on', k === i); if (k === i) a.removeAttribute('tabindex'); else a.setAttribute('tabindex', '-1'); });
        dots.forEach(function (d, k) { d.classList.toggle('is-on', k === i); });
      }
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) { if (e.isIntersecting) show(+e.target.getAttribute('data-step')); });
      }, { rootMargin: '-45% 0px -50% 0px', threshold: 0 });
      steps.forEach(function (s) { io.observe(s); });
    });
  }

  // v02 · 영상이 있는 논문(#pub-N)에 "▶ 영상" 링크를 붙인다(데이터: #pub-videos, videos[].pub에서 빌드 때 생성)
  function initPubVideos() {
    var el = document.getElementById('pub-videos');
    if (!el) return;
    var map;
    try { map = JSON.parse(el.textContent); } catch (e) { return; }
    var label = el.getAttribute('data-label') || 'Video';
    Object.keys(map).forEach(function (num) {
      var cite = document.querySelector('#pub-' + num + ' .pub-cite');
      if (!cite || cite.querySelector('.pub-video')) return;
      var a = document.createElement('a');
      a.className = 'pub-link pub-video';
      a.href = map[num];
      var ico = document.createElement('span');
      ico.setAttribute('aria-hidden', 'true');
      ico.textContent = '▶ ';
      a.appendChild(ico);
      a.appendChild(document.createTextNode(label));
      cite.appendChild(a);
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('[data-spy]').forEach(initSpy);
    initSheet();
    initAutoHide();
    initStory();
    initPubVideos();
  });
})();
