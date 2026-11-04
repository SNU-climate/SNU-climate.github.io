/* t5.v02 연간호: 표지를 누르면 그해 호 하나만 보인다(#issue-YYYY). JS가 없으면 모든 호가 차례로 보인다. */
(function () {
  'use strict';
  function init() {
    var secs = Array.prototype.slice.call(document.querySelectorAll('[data-issue]'));
    if (!secs.length) return;
    var links = Array.prototype.slice.call(document.querySelectorAll('[data-issue-link]'));
    function show(id, scroll) {
      var target = null;
      secs.forEach(function (s) { if (s.id === id) target = s; });
      if (!target) target = secs[0];
      secs.forEach(function (s) { s.hidden = s !== target; });
      links.forEach(function (a) {
        if (a.getAttribute('href') === '#' + target.id) {
          a.setAttribute('aria-current', 'true');
          // 휴대폰의 가로 진열대: 고른 표지가 보이도록 진열대만 옆으로 민다(페이지는 움직이지 않음)
          var rack = a.parentNode;
          if (rack && rack.scrollWidth > rack.clientWidth) rack.scrollLeft = a.offsetLeft - (rack.clientWidth - a.offsetWidth) / 2;
        } else a.removeAttribute('aria-current');
      });
      if (scroll) target.scrollIntoView({ block: 'start' });
    }
    document.documentElement.classList.add('js-issues');
    show(location.hash.slice(1), /^#issue-/.test(location.hash));
    window.addEventListener('hashchange', function () {
      if (/^#issue-/.test(location.hash)) show(location.hash.slice(1), true);
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
