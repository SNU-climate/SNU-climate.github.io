/* t5.v02 공통 동작: People 드롭다운, 홈 커버 기사 넘기기. JS가 없어도 메뉴(마우스 올림)·커버(가로 스크롤)는 동작한다. */
(function () {
  'use strict';

  // 드롭다운: [data-dd] 안의 버튼이 aria-expanded와 data-open을 토글. Esc·바깥 클릭·포커스 이탈 시 닫힘
  document.querySelectorAll('[data-dd]').forEach(function (dd) {
    var btn = dd.querySelector('button[aria-controls]');
    if (!btn) return;
    dd.classList.add('dd-js');
    function set(open) {
      btn.setAttribute('aria-expanded', String(open));
      dd.toggleAttribute('data-open', open);
    }
    btn.addEventListener('click', function () { set(btn.getAttribute('aria-expanded') !== 'true'); });
    dd.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && btn.getAttribute('aria-expanded') === 'true') {
        e.stopPropagation();          // 모바일 메뉴 전체가 같이 닫히지 않게
        set(false);
        btn.focus();
      }
    });
    dd.addEventListener('focusout', function (e) { if (e.relatedTarget && !dd.contains(e.relatedTarget)) set(false); });
    document.addEventListener('click', function (e) { if (!dd.contains(e.target)) set(false); });
  });

  // 커버 기사: [data-cover] 트랙을 ‹ › 버튼·←→ 키로 한 편씩 넘기고, 보이는 편 번호를 갱신. 화면 밖 편은 inert
  document.querySelectorAll('[data-cover]').forEach(function (box) {
    var track = box.querySelector('[data-cover-track]');
    var nav = box.querySelector('[data-cover-nav]');
    if (!track || !nav) return;
    var slides = Array.prototype.slice.call(track.children);
    var prev = nav.querySelector('[data-cover-prev]');
    var next = nav.querySelector('[data-cover-next]');
    var out = nav.querySelector('[data-cover-i]');
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
    var cur = 0, raf = 0, target = null;   // target: 부드럽게 넘어가는 중인 목적지(연달아 누를 때 기준)
    box.classList.add('cover--js');
    nav.hidden = false;

    function step() { return slides.length > 1 ? slides[1].offsetLeft - slides[0].offsetLeft : track.clientWidth; }
    function update() {
      cur = Math.max(0, Math.min(slides.length - 1, Math.round(track.scrollLeft / step())));
      out.textContent = String(cur + 1);
      prev.disabled = cur === 0;
      next.disabled = cur === slides.length - 1;
      slides.forEach(function (s, i) { s.inert = i !== cur; });
      if (target === cur) target = null;
    }
    function go(d) {
      var i = Math.max(0, Math.min(slides.length - 1, (target === null ? cur : target) + d));
      target = i;
      track.scrollTo({ left: i * step(), behavior: reduce.matches ? 'auto' : 'smooth' });
    }
    prev.addEventListener('click', function () { go(-1); });
    next.addEventListener('click', function () { go(1); });
    track.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
        e.preventDefault();
        go(e.key === 'ArrowRight' ? 1 : -1);
      }
    });
    track.addEventListener('scroll', function () {
      cancelAnimationFrame(raf);
      raf = requestAnimationFrame(update);
    }, { passive: true });
    track.addEventListener('scrollend', function () { target = null; update(); });
    track.addEventListener('pointerdown', function () { target = null; });   // 손으로 넘기기 시작하면 목적지 해제
    window.addEventListener('resize', function () { track.scrollLeft = cur * step(); update(); });
    update();
  });
})();
