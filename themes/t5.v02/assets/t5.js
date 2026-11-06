/* t5.v02 공통 동작: People 드롭다운, 홈 커버 기사 넘기기. JS가 없어도 메뉴(마우스 올림·포커스)·커버(가로 스크롤)는 동작한다. */
(function () {
  'use strict';

  // 드롭다운: [data-dd] 안의 버튼이 aria-expanded와 data-open을 토글. 상태는 set() 한 곳에서만 바꾼다.
  // 마우스를 올릴 수 있는 데스크톱에서는 올리면 열리고(떠나면 닫힘), 그 상태에서 누르면 고정된다.
  // Esc·바깥 클릭·포커스 이탈 시 닫힘
  var canHover = window.matchMedia('(hover: hover) and (min-width: 861px)');
  document.querySelectorAll('[data-dd]').forEach(function (dd) {
    var btn = dd.querySelector('button[aria-controls]');
    if (!btn) return;
    var byHover = false;          // 마우스 올림으로 열린 상태(누르지 않음)
    dd.classList.add('nav-dd--js');
    function set(open) {
      btn.setAttribute('aria-expanded', String(open));
      dd.toggleAttribute('data-open', open);
      if (!open) byHover = false;
    }
    function isOpen() { return btn.getAttribute('aria-expanded') === 'true'; }
    btn.addEventListener('click', function () {
      if (byHover) { byHover = false; return; }      // 올려서 열린 메뉴를 누르면 닫지 않고 고정
      set(!isOpen());
    });
    dd.addEventListener('mouseenter', function () {
      if (canHover.matches && !isOpen()) { set(true); byHover = true; }
    });
    dd.addEventListener('mouseleave', function () { if (byHover) set(false); });
    // 캡처 단계: 모바일 메뉴 전체를 닫는 shared.js의 Esc보다 먼저 받아 드롭다운만 닫는다
    document.addEventListener('keydown', function (e) {
      if (e.key !== 'Escape' || !isOpen()) return;
      e.stopPropagation();
      var inside = dd.contains(document.activeElement);
      set(false);
      if (inside) btn.focus();
    }, true);
    dd.addEventListener('focusout', function (e) { if (e.relatedTarget && !dd.contains(e.relatedTarget)) set(false); });
    document.addEventListener('click', function (e) { if (!dd.contains(e.target)) set(false); });
  });

  // 커버 기사: [data-cover] 트랙을 ‹ › 버튼·←→ 키로 한 편씩 넘기고, 보이는 편 번호를 갱신. 화면 밖 편은 inert.
  // 끝에 닿은 버튼은 disabled 대신 aria-disabled(포커스가 사라지지 않게)
  document.querySelectorAll('[data-cover]').forEach(function (box) {
    var track = box.querySelector('[data-cover-track]');
    var nav = box.querySelector('[data-cover-nav]');
    if (!track || !nav) return;
    var slides = Array.prototype.slice.call(track.children);
    var prev = nav.querySelector('[data-cover-prev]');
    var next = nav.querySelector('[data-cover-next]');
    var out = nav.querySelector('[data-cover-i]');
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
    var cur = -1, raf = 0, target = null, lastW = track.clientWidth;   // target: 부드럽게 넘어가는 중인 목적지(연달아 누를 때 기준)
    box.classList.add('cover--js');
    nav.hidden = false;

    function step() { return slides.length > 1 ? slides[1].offsetLeft - slides[0].offsetLeft : track.clientWidth; }
    function update() {
      var i = Math.max(0, Math.min(slides.length - 1, Math.round(track.scrollLeft / step())));
      if (target === i) target = null;
      if (i === cur) return;                       // 바뀔 때만 번호·inert·버튼 갱신
      cur = i;
      out.textContent = String(cur + 1);
      prev.setAttribute('aria-disabled', String(cur === 0));
      next.setAttribute('aria-disabled', String(cur === slides.length - 1));
      slides.forEach(function (s, k) {
        if (k !== cur && s.contains(document.activeElement)) track.focus({ preventScroll: true });   // 포커스를 가진 편이 inert가 되기 전에 트랙으로
        s.inert = k !== cur;
      });
    }
    function go(d) {
      var i = Math.max(0, Math.min(slides.length - 1, (target === null ? cur : target) + d));
      if (i === cur) { target = null; return; }    // 끝에서 더 누르면 목적지를 만들지 않는다
      target = i;
      track.scrollTo({ left: i * step(), behavior: reduce.matches ? 'auto' : 'smooth' });
    }
    prev.addEventListener('click', function () { if (prev.getAttribute('aria-disabled') !== 'true') go(-1); });
    next.addEventListener('click', function () { if (next.getAttribute('aria-disabled') !== 'true') go(1); });
    track.addEventListener('keydown', function (e) {
      if (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return;
      e.preventDefault();
      if (document.activeElement !== track) track.focus({ preventScroll: true });   // 편 안의 링크에서 눌렀을 때
      go(e.key === 'ArrowRight' ? 1 : -1);
    });
    track.addEventListener('scroll', function () {
      cancelAnimationFrame(raf);
      raf = requestAnimationFrame(update);
    }, { passive: true });
    track.addEventListener('scrollend', function () { target = null; update(); });
    // 손·휠로 넘기기 시작하면 목적지 해제
    track.addEventListener('pointerdown', function () { target = null; });
    track.addEventListener('wheel', function () { target = null; }, { passive: true });
    window.addEventListener('resize', function () {
      if (track.clientWidth === lastW) return;     // 높이만 바뀐 resize(모바일 주소창)는 무시
      lastW = track.clientWidth;
      track.scrollLeft = cur * step();
    });
    update();
  });
})();
