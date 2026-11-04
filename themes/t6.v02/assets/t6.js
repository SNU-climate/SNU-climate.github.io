/* t6.v02 — 인용 도구와 논문 목록 탐색.
   1) 인용: 논문마다 [Cite] → BibTeX / 인용문 탭, 복사 버튼. 논문 목록에서는 보이는 논문을 .bib로 내려받기.
      데이터는 페이지의 <script type="application/json" id="bib-data">(빌드 때 publications.yaml 필드로 만든 것)만 쓴다.
   2) 탐색(publications.html): 출판사 계열·교신저자·대표 논문·제목 키워드 렌즈 필터 + 연도 막대에 결과를 실시간 반영.
      shared.js의 논문 검색을 그대로 두고, 같은 검색창 입력 뒤에 한 번 더 걸러 최종 상태를 정한다(이 스크립트가 나중에 등록된다).
   외부 라이브러리·네트워크 요청 없음(file://에서도 동작). */
(function () {
  'use strict';
  var slice = function (x) { return Array.prototype.slice.call(x); };
  var data = null;
  var uid = 0;

  function readData() {
    var el = document.getElementById('bib-data');
    if (!el) return null;
    try { return JSON.parse(el.textContent); } catch (e) { return null; }
  }

  // ---------------------------------------------------------------- 인용문 만들기
  var STOP = { a: 1, an: 1, the: 1, on: 1, of: 1, in: 1, and: 1, to: 1, for: 1, by: 1, from: 1, with: 1, at: 1, under: 1, over: 1, its: 1, is: 1, are: 1 };
  function plain(s) { return String(s || '').normalize('NFD').replace(/[̀-ͯ]/g, ''); }
  function family(a) { return String(a || '').split(',')[0].trim(); }
  function bibKey(p) {
    var words = plain(p.t).toLowerCase().split(/[^a-z0-9]+/).filter(function (w) { return w && !STOP[w]; });
    return plain(family(p.a[0])).replace(/[^A-Za-z]/g, '').toLowerCase() + p.y + (words[0] || '');
  }
  function bibtex(p) {
    var fields = [
      ['author', p.a.join(' and ')], ['title', '{' + p.t + '}'], ['journal', p.j], ['year', p.y],
      ['volume', p.v], ['number', p.i], ['pages', String(p.pg || '').replace(/\s*[-–]\s*/g, '--')], ['doi', p.doi]
    ].filter(function (f) { return f[1] !== '' && f[1] !== null && f[1] !== undefined; });
    var w = 7;
    return '@article{' + bibKey(p) + ',\n' + fields.map(function (f) {
      return '  ' + (f[0] + '       ').slice(0, w) + ' = {' + String(f[1]).replace(/([&%#_])/g, '\\$1') + '}';
    }).join(',\n') + '\n}';
  }
  function textCite(p) {
    var a = p.a.slice();
    var au = a.length > 1 ? a.slice(0, -1).join(', ') + ', & ' + a[a.length - 1] : (a[0] || '');
    var s = au + ' (' + p.y + '). ' + p.t + '. ' + p.j;
    if (p.v) s += ', ' + p.v + (p.i ? '(' + p.i + ')' : '');
    if (p.pg) s += ', ' + String(p.pg).replace(/\s*-\s*/g, '–');
    s += '.';
    if (p.doi) s += ' https://doi.org/' + p.doi;
    return s;
  }

  function copyText(text, ta, done) {
    function fallback() {
      var ok = false;
      ta.focus(); ta.select();
      try { ok = document.execCommand('copy'); } catch (e) { ok = false; }
      done(ok);
    }
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(text).then(function () { done(true); }, fallback);
    } else { fallback(); }
  }

  // ---------------------------------------------------------------- 인용 창
  function buildBox(btn, p) {
    var L = data.labels || {};
    var box = document.createElement('div');
    box.className = 'cite-box';
    box.id = 'cite-' + btn.getAttribute('data-cite') + '-' + (++uid);
    var fmt = 'bib';
    box.innerHTML =
      '<div class="cite-tabs" role="tablist">' +
      '<button type="button" role="tab" aria-selected="true" data-fmt="bib"></button>' +
      '<button type="button" role="tab" aria-selected="false" data-fmt="txt"></button>' +
      '</div><textarea class="cite-text" readonly spellcheck="false" rows="9"></textarea>' +
      '<div class="cite-actions"><button type="button" class="btn btn--sm cite-copy"></button><span class="cite-msg" aria-live="polite"></span></div>';
    var tabs = slice(box.querySelectorAll('[data-fmt]'));
    tabs[0].textContent = L.bibtex || 'BibTeX';
    tabs[1].textContent = L.text || 'Text';
    var ta = box.querySelector('textarea');
    ta.setAttribute('aria-label', (L.cite || 'Cite') + ' — ' + p.t);
    var copyBtn = box.querySelector('.cite-copy');
    copyBtn.textContent = L.copy || 'Copy';
    var msg = box.querySelector('.cite-msg');
    function show() {
      ta.value = fmt === 'bib' ? bibtex(p) : textCite(p);
      ta.rows = fmt === 'bib' ? Math.min(12, ta.value.split('\n').length) : 4;
      tabs.forEach(function (t) { t.setAttribute('aria-selected', String(t.getAttribute('data-fmt') === fmt)); });
      msg.textContent = '';
    }
    tabs.forEach(function (t) { t.addEventListener('click', function () { fmt = t.getAttribute('data-fmt'); show(); }); });
    copyBtn.addEventListener('click', function () {
      copyText(ta.value, ta, function (ok) { msg.textContent = ok ? (L.copied || 'Copied') : (L.fail || ''); });
    });
    show();
    return box;
  }

  function initCite() {
    data = readData();
    if (!data || !data.pubs) return;
    slice(document.querySelectorAll('[data-cite]')).forEach(function (btn) {
      var p = data.pubs[btn.getAttribute('data-cite')];
      if (!p) return;
      btn.hidden = false;
      btn.addEventListener('click', function () {
        var li = btn.closest('.bib');
        var box = li.querySelector('.cite-box');
        if (!box) {
          box = buildBox(btn, p);
          btn.setAttribute('aria-controls', box.id);
          li.querySelector('.bib-main').appendChild(box);
          btn.setAttribute('aria-expanded', 'true');
          return;
        }
        box.hidden = !box.hidden;
        btn.setAttribute('aria-expanded', String(!box.hidden));
      });
    });
    var exp = document.querySelector('[data-bib-export]');
    if (exp && window.Blob && window.URL) {
      exp.hidden = false;
      exp.addEventListener('click', function () {
        var out = slice(document.querySelectorAll('[data-pub-item]')).filter(function (it) { return !it.hidden; })
          .map(function (it) { var p = data.pubs[(it.id || '').replace('pub-', '')]; return p ? bibtex(p) : ''; })
          .filter(Boolean);
        var url = URL.createObjectURL(new Blob([out.join('\n\n') + '\n'], { type: 'application/x-bibtex;charset=utf-8' }));
        var a = document.createElement('a');
        a.href = url; a.download = 'csl-publications.bib';
        document.body.appendChild(a); a.click(); a.remove();
        setTimeout(function () { URL.revokeObjectURL(url); }, 2000);
      });
    }
  }

  // ---------------------------------------------------------------- 논문 목록 탐색
  function initExplorer() {
    var root = document.querySelector('[data-px]');
    if (!root) return;
    var input = document.querySelector('[data-pub-search]');
    var items = slice(document.querySelectorAll('[data-pub-item]'));
    var years = slice(document.querySelectorAll('[data-pub-year]'));
    var countEl = document.querySelector('[data-pub-count]');
    var emptyEl = document.querySelector('[data-pub-empty]');
    var summary = root.querySelector('[data-px-summary]');
    var reset = root.querySelector('[data-px-reset]');
    var svg = root.querySelector('.px-svg');
    var H = svg ? parseFloat(svg.getAttribute('data-h')) : 0;
    var MAX = svg ? parseFloat(svg.getAttribute('data-max')) : 1;
    var bars = {};
    slice(root.querySelectorAll('.px-on')).forEach(function (r) { bars[r.getAttribute('data-y')] = r; });
    var pills = slice(document.querySelectorAll('.year-pills a[href^="#y"]'));
    var groups = slice(root.querySelectorAll('[data-px-group]'));
    var toggles = slice(root.querySelectorAll('[data-px-toggle]'));
    var state = { fam: '', lens: '', ca: false, feat: false };

    function sync() {
      groups.forEach(function (g) {
        var name = g.getAttribute('data-px-group');
        slice(g.querySelectorAll('button[data-val]')).forEach(function (b) {
          b.setAttribute('aria-pressed', String(b.getAttribute('data-val') === state[name]));
        });
      });
      toggles.forEach(function (b) { b.setAttribute('aria-pressed', String(!!state[b.getAttribute('data-px-toggle')])); });
    }

    function apply() {
      var terms = (input ? input.value : '').toLowerCase().trim().split(/\s+/).filter(Boolean);
      var n = 0, per = {};
      items.forEach(function (it) {
        var s = it.getAttribute('data-search') || '';
        var ok = terms.every(function (t) { return s.indexOf(t) !== -1; }) &&
          (!state.fam || it.getAttribute('data-fam') === state.fam) &&
          (!state.lens || (' ' + (it.getAttribute('data-lens') || '') + ' ').indexOf(' ' + state.lens + ' ') !== -1) &&
          (!state.ca || it.hasAttribute('data-ca')) &&
          (!state.feat || it.hasAttribute('data-feat'));
        it.hidden = !ok;
        if (ok) { n++; var y = it.getAttribute('data-y'); per[y] = (per[y] || 0) + 1; }
      });
      years.forEach(function (y) { y.hidden = !y.querySelector('[data-pub-item]:not([hidden])'); });
      if (countEl) countEl.textContent = n;
      if (emptyEl) emptyEl.hidden = n !== 0;
      Object.keys(bars).forEach(function (y) {
        var h = (per[y] || 0) / MAX * H;
        bars[y].setAttribute('height', h.toFixed(1));
        bars[y].setAttribute('y', (H - h).toFixed(1));
      });
      pills.forEach(function (a) { a.classList.toggle('is-empty', !per[a.getAttribute('href').slice(2)]); });
      var active = !!(state.fam || state.lens || state.ca || state.feat || terms.length);
      root.classList.toggle('px--active', active);
      if (reset) reset.hidden = !active;
      if (summary) summary.textContent = active ? n + ' / ' + items.length : '';
    }

    groups.forEach(function (g) {
      g.addEventListener('click', function (e) {
        var b = e.target.closest('button[data-val]');
        if (!b) return;
        var name = g.getAttribute('data-px-group');
        var v = b.getAttribute('data-val');
        state[name] = (state[name] === v && name === 'lens') ? '' : v;   // 키워드 줄은 다시 누르면 해제
        sync(); apply();
      });
    });
    toggles.forEach(function (b) {
      b.addEventListener('click', function () { var k = b.getAttribute('data-px-toggle'); state[k] = !state[k]; sync(); apply(); });
    });
    if (reset) reset.addEventListener('click', function () {
      state = { fam: '', lens: '', ca: false, feat: false };
      if (input) input.value = '';
      sync(); apply();
    });
    if (input) input.addEventListener('input', apply);

    // 주소의 ?lens=enso / ?fam=nature 로 바로 거른 목록을 열 수 있다(?q=는 shared.js가 처리)
    var qs = new URLSearchParams(location.search);
    var fromUrl = false;
    groups.forEach(function (g) {
      var name = g.getAttribute('data-px-group'), v = qs.get(name);
      if (v && g.querySelector('button[data-val="' + v.replace(/[^a-z]/g, '') + '"]')) { state[name] = v; fromUrl = true; }
    });
    // 휴대폰에서는 탐색 창을 접어 검색창 바로 아래에 목록이 오게 한다
    if (!fromUrl && window.matchMedia && !window.matchMedia('(min-width: 720px)').matches) root.open = false;
    sync(); apply();
  }

  document.addEventListener('DOMContentLoaded', function () {
    initCite();
    initExplorer();
  });
})();
