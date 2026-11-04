/* Ocean–Atmosphere v01: 떠 있는 헤더가 본문을 덮지 않도록 아래로 스크롤하면 숨기고, 위로 스크롤하면 다시 보인다.
   메뉴가 열려 있거나 헤더 안에 포커스가 있으면 숨기지 않는다. */
(function () {
  'use strict';
  var hdr = document.querySelector('[data-hdr]');
  if (!hdr) return;
  var lastY = window.scrollY, ticking = false;
  function update() {
    var y = window.scrollY;
    var open = document.documentElement.classList.contains('nav-open') || hdr.contains(document.activeElement);
    hdr.classList.toggle('hdr--solid', y > 40);
    if (open || y < 120 || y < lastY - 4) hdr.classList.remove('hdr--away');
    else if (y > lastY + 4) hdr.classList.add('hdr--away');
    if (Math.abs(y - lastY) > 4) lastY = y;
    ticking = false;
  }
  window.addEventListener('scroll', function () {
    if (!ticking) { ticking = true; window.requestAnimationFrame(update); }
  }, { passive: true });
  hdr.addEventListener('focusin', function () { hdr.classList.remove('hdr--away'); });
  update();
})();
