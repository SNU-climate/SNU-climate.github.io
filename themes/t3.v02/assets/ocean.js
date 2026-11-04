/* Ocean–Atmosphere v02
   1) 떠 있는 헤더: 아래로 스크롤하면 숨기고 위로 스크롤하면 보인다(메뉴가 열려 있거나 포커스가 있으면 유지).
   2) 논문 해류 타임라인([data-tl]): 검색하면 연도별 검색 결과 수로 두 번째 물결(.tl-q)을 그린다.
   3) 연구 지역 해도([data-sc-scroll]): 좁은 화면에서 가로로 스크롤될 때 태평양이 가운데 오게 맞춘다.
   4) 논문 목록([data-pub-videos]): 영상으로 소개된 논문 줄에 영상 링크를 붙인다. */
(function () {
  'use strict';

  function initHeader() {
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
  }

  // _ocean.html의 swell_d와 같은 곡선(폭 1000, 높이 200, 최댓값 y=20, 0은 y=176)
  function swellPath(vals, peak) {
    var W = 1000, top = 20, base = 176, n = vals.length, cw = W / n, pts = [];
    for (var i = 0; i < n; i++) pts.push([cw * (i + 0.5), base - (vals[i] / peak) * (base - top)]);
    function r(v) { return Math.round(v * 10) / 10; }
    var d = 'M0 ' + r(pts[0][1]) + ' L' + r(pts[0][0]) + ' ' + r(pts[0][1]);
    for (var k = 0; k < n - 1; k++) {
      var p0 = pts[k > 0 ? k - 1 : k], p1 = pts[k], p2 = pts[k + 1], p3 = pts[k + 2 < n ? k + 2 : k + 1];
      d += ' C' + r(p1[0] + (p2[0] - p0[0]) / 6) + ' ' + r(Math.min(p1[1] + (p2[1] - p0[1]) / 6, base)) +
        ' ' + r(p2[0] - (p3[0] - p1[0]) / 6) + ' ' + r(Math.min(p2[1] - (p3[1] - p1[1]) / 6, base)) +
        ' ' + r(p2[0]) + ' ' + r(p2[1]);
    }
    return d + ' L' + W + ' ' + r(pts[n - 1][1]) + ' L' + W + ' 200 L0 200Z';
  }

  function initSwell() {
    var box = document.querySelector('[data-tl]');
    var input = document.querySelector('[data-pub-search]');
    if (!box || !input) return;
    var years = (box.getAttribute('data-tl-years') || '').split(',').map(Number);
    var peak = Number(box.getAttribute('data-tl-max')) || 1;
    var q = box.querySelector('.tl-q');
    var count = document.querySelector('[data-tl-count]');
    var total = count ? count.textContent : '';
    function run() {
      var active = input.value.trim() !== '';
      box.classList.toggle('tl-box--search', active);
      if (!active) { q.setAttribute('hidden', ''); if (count) count.textContent = total; return; }
      var n = 0;
      var vals = years.map(function (y) {
        var sec = document.getElementById('y' + y);
        var c = sec ? sec.querySelectorAll('[data-pub-item]:not([hidden])').length : 0;
        n += c;
        return c;
      });
      q.setAttribute('d', swellPath(vals, peak));
      q.removeAttribute('hidden');
      if (count) count.textContent = n + ' / ' + total;
    }
    // shared.js가 같은 input 이벤트에서 목록을 거른 다음에 센다
    input.addEventListener('input', function () { window.setTimeout(run, 0); });
    window.setTimeout(run, 0);   // ?q= 로 들어온 경우
  }

  function initSeaChart() {
    document.querySelectorAll('[data-sc-scroll]').forEach(function (el) {
      if (el.scrollWidth > el.clientWidth + 4) el.scrollLeft = (el.scrollWidth - el.clientWidth) * 0.5;
    });
  }

  function initPubVideos() {
    var list = document.querySelector('[data-pub-videos]');
    if (!list) return;
    var label = list.getAttribute('data-label') || 'Video';
    list.querySelectorAll('li').forEach(function (li) {
      var item = document.getElementById('pub-' + li.getAttribute('data-num'));
      var cite = item && item.querySelector('.pub-cite');
      if (!cite) return;
      var a = document.createElement('a');
      a.className = 'pub-link pub-video';
      a.href = li.getAttribute('data-href');
      a.target = '_blank';
      a.rel = 'noopener';
      a.title = li.getAttribute('data-title') || label;
      a.textContent = '▶ ' + label;
      cite.appendChild(a);
    });
  }

  function ready(fn) {
    if (document.readyState !== 'loading') fn();
    else document.addEventListener('DOMContentLoaded', fn);
  }
  initHeader();
  ready(function () { initSwell(); initSeaChart(); initPubVideos(); });
})();
