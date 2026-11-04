/* basic.v02 게시판 동작: [data-board] 안에서 분류 탭([data-board-tabs] button[data-cat])과 검색([data-board-search])으로
   [data-board-item](data-cat, data-search)을 거르고, 빈 묶음([data-board-group])은 숨긴다. 주소의 ?q=, ?cat= 를 읽는다.
   공지(news.html)·갤러리(gallery.html)·이전 사이트 글(archive.html)이 함께 쓴다. 외부 의존 없음. */
(function () {
  'use strict';
  function init(root) {
    var items = Array.prototype.slice.call(root.querySelectorAll('[data-board-item]'));
    var groups = Array.prototype.slice.call(root.querySelectorAll('[data-board-group]'));
    var input = root.querySelector('[data-board-search]');
    var tabs = root.querySelector('[data-board-tabs]');
    var count = root.querySelector('[data-board-count]');
    var empty = root.querySelector('[data-board-empty]');
    var cat = '';
    function run() {
      var terms = input ? input.value.toLowerCase().trim().split(/\s+/).filter(Boolean) : [];
      var n = 0;
      items.forEach(function (it) {
        var s = it.getAttribute('data-search') || '';
        var ok = (!cat || it.getAttribute('data-cat') === cat) &&
          terms.every(function (t) { return s.indexOf(t) !== -1; });
        it.hidden = !ok;
        if (ok) n++;
      });
      groups.forEach(function (g) { g.hidden = !g.querySelector('[data-board-item]:not([hidden])'); });
      if (count) count.textContent = n;
      if (empty) empty.hidden = n !== 0;
    }
    function setCat(c) {
      cat = c || '';
      if (!tabs) return;
      tabs.querySelectorAll('button[data-cat]').forEach(function (b) {
        b.setAttribute('aria-pressed', String(b.getAttribute('data-cat') === cat));
      });
    }
    if (tabs) tabs.addEventListener('click', function (e) {
      var b = e.target.closest('button[data-cat]');
      if (!b) return;
      setCat(b.getAttribute('data-cat'));
      run();
    });
    if (input) input.addEventListener('input', run);
    var qs = new URLSearchParams(location.search);
    if (qs.get('cat') && tabs && tabs.querySelector('button[data-cat="' + qs.get('cat').replace(/[^\w-]/g, '') + '"]')) setCat(qs.get('cat'));
    if (qs.get('q') && input) input.value = qs.get('q');
    if (cat || (input && input.value)) run();
  }
  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('[data-board]').forEach(init);
  });
})();
