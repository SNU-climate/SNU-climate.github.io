/* Interactive Globe v02 — d3-geo orthographic + Natural Earth 110m land (assets/vendor/world-110m.js).
   - 홈: [data-globe] 큰 지구본(자동 회전·드래그·방향키). 연구 지역은 반투명 색 영역(반경 7° 원)으로 칠하고,
     지역이나 범례를 누르면 [data-explore] 탐색 카드(그 분야 논문·영상)를 연다. 지금 밤인 쪽을 실시간으로 어둡게 칠한다.
   - 연구 개요: [data-mini-globe="key"] 주제별 작은 지구본(해당 주제 지역만)
   - 연구 주제 페이지: [data-topic-globe="key"] 큰 지구본. [data-region] 버튼 → 그 지역으로 회전·확대, [data-tour] 차례로 둘러보기
   - 홈 논문 타임라인: [data-timeline] 연도 막대 + 슬라이더 + 재생(지구본 스크립트와 별개로 동작)
   영역 원은 research.yaml의 regions 좌표를 중심으로 그린 표시일 뿐, 실제 연구 영역 경계가 아니다.
   지평선 근처 마커는 흐리게 하다가 지평선 10° 앞에서 숨겨 구 밖으로 나오지 않게 한다.
   prefers-reduced-motion 이면 자동 회전·관성·전환 애니메이션을 끈다(드래그는 사용자가 직접 하는 것이라 유지). */
(function () {
  'use strict';
  var SVGNS = 'http://www.w3.org/2000/svg';
  var FALLBACK = ['#00796b', '#c2410c', '#1f5fc9', '#467510', '#b8237a'];   // style.css --t0..--t4 와 같게
  var HIDE = Math.PI / 2 - 0.18;      // 이보다 멀면(지평선 약 10° 앞) 마커를 숨긴다
  var RING = Math.PI / 2 - 0.35;      // 이보다 멀면 바깥 링(펄스)을 숨긴다
  var uid = 0;

  function ready(fn) {
    if (document.readyState !== 'loading') fn();
    else document.addEventListener('DOMContentLoaded', fn);
  }
  function el(name, attrs, parent) {
    var e = document.createElementNS(SVGNS, name);
    for (var k in attrs) if (attrs[k] != null) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  }
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
  function ease(t) { return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; }
  function wrap180(d) { return ((d + 540) % 360) - 180; }

  function makeGlobe(host, o) {
    var d3 = window.d3;
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var id = 'gl' + (++uid);
    var land = o.land, grat = d3.geoGraticule10();
    var proj = d3.geoOrthographic().clipAngle(90).precision(0.6);
    var path = d3.geoPath(proj);
    var rot = [-o.center[0], -o.center[1], 0];
    var zoom = 1;
    var sun = o.night ? subsolar(new Date()) : null;
    var R = 100, W = 200, PAD = o.mini ? 1.1 : 1.16;

    var svg = el('svg', { 'class': 'globe-svg', focusable: 'false' }, host);
    if (!o.links) svg.setAttribute('aria-hidden', 'true');
    var defs = el('defs', {}, svg);
    var g1 = el('radialGradient', { id: id + 'o', cx: '40%', cy: '36%', r: '72%' }, defs);
    // 정지점 색은 style.css 토큰(.g-o*, .g-h*, .g-s* → --g-ocean-*, --g-air, --g-lo)에서 정한다
    el('stop', { offset: '0%', 'class': 'g-o0' }, g1);
    el('stop', { offset: '62%', 'class': 'g-o1' }, g1);
    el('stop', { offset: '100%', 'class': 'g-o2' }, g1);
    var g2 = el('radialGradient', { id: id + 'h', cx: '50%', cy: '50%', r: '50%' }, defs);
    el('stop', { offset: '80%', 'class': 'g-h0' }, g2);
    el('stop', { offset: '88%', 'class': 'g-h1' }, g2);
    el('stop', { offset: '100%', 'class': 'g-h2' }, g2);
    var g3 = el('radialGradient', { id: id + 's', cx: '36%', cy: '30%', r: '75%' }, defs);
    el('stop', { offset: '0%', 'class': 'g-s0' }, g3);
    el('stop', { offset: '55%', 'class': 'g-s1' }, g3);
    el('stop', { offset: '100%', 'class': 'g-s2' }, g3);
    var fl = el('filter', { id: id + 'f', x: '-100%', y: '-100%', width: '300%', height: '300%' }, defs);
    el('feGaussianBlur', { stdDeviation: o.mini ? 1.2 : 2, result: 'b' }, fl);
    var fm = el('feMerge', {}, fl);
    el('feMergeNode', { 'in': 'b' }, fm);
    el('feMergeNode', { 'in': 'SourceGraphic' }, fm);
    // 확대할 때 구가 렌즈(원) 안에서만 보이도록 자른다
    var clip = el('clipPath', { id: id + 'c' }, defs);
    var clipC = el('circle', {}, clip);

    var halo = el('circle', { 'class': 'g-halo', fill: 'url(#' + id + 'h)' }, svg);
    var body = el('g', { 'clip-path': o.zoomable ? 'url(#' + id + 'c)' : null }, svg);
    var pSphere = el('path', { 'class': 'g-sphere', fill: 'url(#' + id + 'o)' }, body);
    var pGrat = el('path', { 'class': 'g-grat' }, body);
    var pLand = el('path', { 'class': 'g-land' }, body);
    var pNight = o.night ? el('path', { 'class': 'g-night' }, body) : null;
    var pNight2 = o.night ? el('path', { 'class': 'g-night g-night--deep' }, body) : null;
    var gCaps = o.caps ? el('g', { 'class': 'g-caps' }, body) : null;
    var pShade = el('path', { 'class': 'g-shade', fill: 'url(#' + id + 's)' }, body);
    var pRim = el('path', { 'class': 'g-rim' }, body);
    var lens = o.zoomable ? el('circle', { 'class': 'g-lens' }, svg) : null;
    var gMarks = el('g', { 'class': 'g-marks', 'clip-path': o.zoomable ? 'url(#' + id + 'c)' : null }, svg);

    var marks = [];
    o.topics.forEach(function (t) {
      (t.regions || []).forEach(function (r, i) {
        var node = o.links ? el('a', { href: t.url, 'class': 'g-mark', 'data-key': t.key }, gMarks)
                           : el('g', { 'class': 'g-mark', 'data-key': t.key }, gMarks);
        node.style.setProperty('--c', t.color);
        var name = (t.names && t.names[i]) || '';
        if (o.links) node.setAttribute('aria-label', t.title + (name ? ' — ' + name : ''));
        var cap = null, capGeo = null;
        if (gCaps) {
          capGeo = d3.geoCircle().center([r[1], r[0]]).radius(o.caps)();
          cap = el('path', { 'class': 'g-cap', 'data-key': t.key }, gCaps);
          cap.style.setProperty('--c', t.color);
        }
        var ring = el('circle', { 'class': 'g-ring', r: o.mini ? 7 : 11 }, node);
        el('circle', { 'class': 'g-hit', r: o.mini ? 8 : 16 }, node);
        el('circle', { 'class': 'g-dot', r: o.mini ? 3.6 : 5.2, filter: 'url(#' + id + 'f)' }, node);
        var tt = el('title', {}, node); tt.textContent = t.title + (name ? ' — ' + name : '');
        marks.push({ node: node, ring: ring, cap: cap, capGeo: capGeo, ll: [r[1], r[0]], t: t, i: i, name: name, x: 0, y: 0, vis: false });
      });
    });

    function size() {
      W = Math.max(80, host.clientWidth);
      R = W / 2 / PAD;
      svg.setAttribute('viewBox', '0 0 ' + W + ' ' + W);
      halo.setAttribute('cx', W / 2); halo.setAttribute('cy', W / 2); halo.setAttribute('r', R * 1.16);
      clipC.setAttribute('cx', W / 2); clipC.setAttribute('cy', W / 2); clipC.setAttribute('r', R * 1.08);
      if (lens) { lens.setAttribute('cx', W / 2); lens.setAttribute('cy', W / 2); lens.setAttribute('r', R * 1.08); }
    }

    function render() {
      proj.translate([W / 2, W / 2]).scale(R * zoom).rotate(rot);
      var sphere = path({ type: 'Sphere' });
      pSphere.setAttribute('d', sphere);
      pShade.setAttribute('d', sphere);
      pRim.setAttribute('d', sphere);
      pGrat.setAttribute('d', path(grat) || '');
      pLand.setAttribute('d', path(land) || '');
      if (pNight && sun) {
        var anti = [wrap180(sun[0] + 180), -sun[1]];
        pNight.setAttribute('d', path(d3.geoCircle().center(anti).radius(90)()) || '');
        pNight2.setAttribute('d', path(d3.geoCircle().center(anti).radius(84)()) || '');
      }
      if (lens) lens.style.opacity = clamp((zoom - 1) * 3, 0, 1).toFixed(2);
      var c = [-rot[0], -rot[1]];
      marks.forEach(function (mk) {
        if (mk.cap) mk.cap.setAttribute('d', path(mk.capGeo) || '');
        var dist = d3.geoDistance(mk.ll, c);
        var vis = dist < HIDE;
        mk.vis = vis;
        if (!vis) { mk.node.style.display = 'none'; return; }
        var p = proj(mk.ll);
        mk.x = p[0]; mk.y = p[1];
        mk.node.style.display = '';
        mk.node.setAttribute('transform', 'translate(' + p[0].toFixed(1) + ',' + p[1].toFixed(1) + ')');
        mk.node.style.opacity = clamp((HIDE - dist) / 0.3, 0, 1).toFixed(2);
        mk.ring.style.display = dist > RING ? 'none' : '';
      });
      if (o.onRender) o.onRender(marks);
    }

    // ---------------------------------------------------------------- 애니메이션 루프
    var auto = !!o.auto && !reduce, vel = [0, 0], dragging = false, moved = 0, anim = null;
    var lastInteract = 0, raf = 0, last = 0, onScreen = true, held = false;
    var SPEED = 0.0055;                 // 자동 회전 deg/ms (약 5.5°/s)

    function frame(ts) {
      raf = 0;
      var dt = last ? Math.min(64, ts - last) : 16;
      last = ts;
      var keep = false;
      if (anim) {
        var k = clamp((ts - anim.t0) / anim.dur, 0, 1), e = ease(k);
        rot[0] = anim.from[0] + anim.d[0] * e;
        rot[1] = anim.from[1] + anim.d[1] * e;
        zoom = anim.z0 + (anim.z1 - anim.z0) * e;
        if (k >= 1) { anim = null; lastInteract = performance.now(); }
        keep = true;
      } else if (!dragging) {
        if (Math.abs(vel[0]) > 0.002 || Math.abs(vel[1]) > 0.002) {
          rot[0] += vel[0] * dt;
          rot[1] = clamp(rot[1] + vel[1] * dt, -70, 70);
          var f = Math.pow(0.94, dt / 16);
          vel[0] *= f; vel[1] *= f;
          keep = true;
        } else if (auto) {
          if (!held && ts - lastInteract > 2600) rot[0] += SPEED * dt;
          keep = true;
        }
      }
      render();
      if (keep && onScreen && !document.hidden) raf = requestAnimationFrame(frame);
      else last = 0;
    }
    function kick() { if (!raf && onScreen && !document.hidden) raf = requestAnimationFrame(frame); }

    function rotateTo(lon, lat, z) {
      var target = [-lon, -clamp(lat, -60, 60)];
      var d = [wrap180(target[0] - rot[0]), target[1] - rot[1]];
      var z1 = z == null ? zoom : z;
      vel = [0, 0];
      lastInteract = performance.now();
      if (reduce) { rot[0] += d[0]; rot[1] += d[1]; zoom = z1; render(); return; }
      anim = { from: [rot[0], rot[1]], d: d, z0: zoom, z1: z1, t0: performance.now(), dur: 900 };
      kick();
    }
    function hold(v) {                  // 마우스가 지구본·범례 위에 있으면 자동 회전을 멈춘다
      held = !!v;
      if (!held) lastInteract = performance.now();
      kick();
    }
    function highlight(key, idx) {
      marks.forEach(function (mk) {
        var hot = !!key && mk.t.key === key && (idx == null || mk.i === idx);
        mk.node.classList.toggle('is-hot', hot);
        mk.node.classList.toggle('is-dim', !!key && !hot);
        if (mk.cap) {
          mk.cap.classList.toggle('is-hot', !!key && mk.t.key === key);
          mk.cap.classList.toggle('is-dim', !!key && mk.t.key !== key);
        }
      });
    }

    // ---------------------------------------------------------------- 드래그(포인터)
    var px = 0, py = 0, lt = 0, pid = null;
    svg.addEventListener('pointerdown', function (e) {
      if (e.button !== 0) return;
      dragging = true; moved = 0; px = e.clientX; py = e.clientY; lt = e.timeStamp; pid = e.pointerId;
      vel = [0, 0]; anim = null;
    });
    svg.addEventListener('pointermove', function (e) {
      if (!dragging || e.pointerId !== pid) return;
      var dx = e.clientX - px, dy = e.clientY - py;
      px = e.clientX; py = e.clientY;
      moved += Math.abs(dx) + Math.abs(dy);
      if (moved > 4 && !svg.hasPointerCapture(pid)) {     // 클릭(링크)과 드래그를 구분: 움직였을 때만 캡처
        try { svg.setPointerCapture(pid); } catch (err) { /* ignore */ }
        host.classList.add('is-dragging');
      }
      var k = 180 / (Math.PI * R * zoom) * (W / Math.max(1, host.clientWidth));
      rot[0] += dx * k;
      rot[1] = clamp(rot[1] - dy * k, -70, 70);
      var dt = Math.max(8, e.timeStamp - lt); lt = e.timeStamp;
      vel = reduce ? [0, 0] : [dx * k / dt, -dy * k / dt];
      render();
    });
    function end(e) {
      if (!dragging) return;
      dragging = false;
      host.classList.remove('is-dragging');
      if (e && e.timeStamp - lt > 90) vel = [0, 0];
      lastInteract = performance.now();
      kick();
    }
    svg.addEventListener('pointerenter', function (e) { if (e.pointerType === 'mouse') hold(true); });
    svg.addEventListener('pointerleave', function (e) { if (e.pointerType === 'mouse') hold(false); });
    svg.addEventListener('pointerup', end);
    svg.addEventListener('pointercancel', end);
    svg.addEventListener('lostpointercapture', end);
    svg.addEventListener('click', function (e) {      // 드래그 직후의 click은 링크로 보내지 않는다(키보드 Enter는 통과)
      if (moved > 6) { e.preventDefault(); e.stopPropagation(); }
      moved = 0;
    }, true);

    // ---------------------------------------------------------------- 키보드(호스트에 tabindex가 있을 때)
    host.addEventListener('keydown', function (e) {
      if (e.target !== host) return;
      var step = { ArrowLeft: [-20, 0], ArrowRight: [20, 0], ArrowUp: [0, 12], ArrowDown: [0, -12] }[e.key];
      if (!step) return;
      e.preventDefault();
      rotateTo(-rot[0] - step[0], -rot[1] + step[1]);
    });

    // 화면 밖이거나 탭이 숨겨지면 멈춘다
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (ents) {
        onScreen = ents[0].isIntersecting;
        if (onScreen) kick();
      }).observe(host);
    }
    document.addEventListener('visibilitychange', function () { if (!document.hidden) kick(); });
    if ('ResizeObserver' in window) {
      new ResizeObserver(function () { size(); render(); }).observe(host);
    } else {
      window.addEventListener('resize', function () { size(); render(); });
    }

    size();
    render();
    host.classList.add('is-ready');
    kick();
    if (o.night) setInterval(function () { sun = subsolar(new Date()); render(); }, 60000);
    return { rotateTo: rotateTo, highlight: highlight, hold: hold, marks: marks, svg: svg,
             stop: function () { vel = [0, 0]; anim = null; } };
  }

  // 태양 직하점 [경도, 위도] (NOAA 근사식, 오차 1° 미만). 밤 = 직하점의 대척점을 중심으로 한 반구
  function subsolar(date) {
    var rad = Math.PI / 180;
    var d = (date.getTime() - Date.UTC(2000, 0, 1, 12)) / 864e5;
    var g = (357.529 + 0.98560028 * d) * rad;
    var q = 280.459 + 0.98564736 * d;
    var L = (q + 1.915 * Math.sin(g) + 0.020 * Math.sin(2 * g)) * rad;
    var e = (23.439 - 0.00000036 * d) * rad;
    var dec = Math.asin(Math.sin(e) * Math.sin(L));
    var ra = Math.atan2(Math.cos(e) * Math.sin(L), Math.cos(L)) / rad;
    var gmst = (18.697374558 + 24.06570982441908 * d) % 24;
    return [wrap180(ra - gmst * 15), dec / rad];
  }


  // ---------------------------------------------------------------- 홈 논문 타임라인
  // 막대·패널은 서버에서 그려 두고(실제 연도별 편수), 여기서는 연도 선택·재생만 한다.
  function initTimeline() {
    var tl = document.querySelector('[data-timeline]');
    if (!tl) return;
    var range = tl.querySelector('[data-tl-range]'), out = tl.querySelector('[data-tl-out]');
    var play = tl.querySelector('[data-tl-play]'), playLab = tl.querySelector('[data-tl-play-label]');
    var live = tl.querySelector('.tl-panels');
    var bars = Array.prototype.slice.call(tl.querySelectorAll('[data-y]'));
    var panels = Array.prototype.slice.call(tl.querySelectorAll('[data-tl-panel]'));
    if (!range || !panels.length) return;
    var lo = +range.min, hi = +range.max, timer = 0;
    function show(y) {
      y = clamp(y, lo, hi);
      range.value = y;
      if (out) out.textContent = y;
      range.setAttribute('aria-valuetext', String(y));
      bars.forEach(function (b) { b.classList.toggle('is-on', +b.getAttribute('data-y') === y); });
      var any = false;
      panels.forEach(function (p) { var on = +p.getAttribute('data-tl-panel') === y; p.hidden = !on; any = any || on; });
      tl.classList.toggle('is-empty', !any);
    }
    function setPlay(on) {
      clearInterval(timer); timer = 0;
      play.setAttribute('aria-pressed', String(on));
      if (playLab) playLab.textContent = play.getAttribute(on ? 'data-pause' : 'data-play');
      if (live) live.setAttribute('aria-live', on ? 'off' : 'polite');
      if (!on) return;
      if (+range.value >= hi) show(lo);
      timer = setInterval(function () {
        if (+range.value >= hi) { setPlay(false); return; }
        show(+range.value + 1);
      }, 900);
    }
    range.addEventListener('input', function () { setPlay(false); show(+range.value); });
    bars.forEach(function (b) {
      b.addEventListener('click', function () { setPlay(false); show(+b.getAttribute('data-y')); range.focus(); });
    });
    play.addEventListener('click', function () { setPlay(play.getAttribute('aria-pressed') !== 'true'); });
    range.hidden = false; play.hidden = false; if (out) out.hidden = false;
    tl.classList.add('is-ready');
    show(+range.value);
  }
  ready(initTimeline);

  ready(function () {
    var d3 = window.d3, topo = window.topojson, world = window.WORLD_LAND_110M;
    if (!d3 || !d3.geoOrthographic || !topo || !world) return;
    var land = topo.feature(world, world.objects.land);
    var css = getComputedStyle(document.documentElement);
    var topics = (window.CSL_TOPICS || []).map(function (t) {
      var c = (css.getPropertyValue('--t' + t.ci) || '').trim() || FALLBACK[t.ci % FALLBACK.length];
      return { key: t.key, title: t.title, url: t.url, regions: t.regions || [], names: t.names || [], color: c };
    });
    function byKey(key) { return topics.filter(function (x) { return x.key === key; })[0]; }
    function centerOf(t) {               // 주제의 지역들이 한 화면에 들어오도록 구면 중심점
      var c = d3.geoCentroid({ type: 'MultiPoint', coordinates: t.regions.map(function (r) { return [r[1], r[0]]; }) });
      if (!isFinite(c[0]) || !isFinite(c[1])) c = [t.regions[0][1], t.regions[0][0]];
      return [c[0], clamp(c[1], -60, 60)];
    }

    // ---------------- 홈 지구본
    var host = document.querySelector('[data-globe]');
    if (host) {
      var tip = host.querySelector('[data-globe-tip]');
      var legend = document.querySelector('[data-globe-legend]');
      var hot = null;                  // {key, i}
      var open = null, opener = null;  // 열린 탐색 카드 {key, i}
      var g = makeGlobe(host, {
        land: land, topics: topics, links: true, auto: true, center: [150, 18], caps: 7, night: true,
        onRender: function (marks) {
          if (!tip || !hot) return;
          var mk = marks.filter(function (x) { return x.t.key === hot.key && (hot.i == null || x.i === hot.i) && x.vis; })[0];
          if (!mk) { tip.hidden = true; return; }
          var s = host.clientWidth / (parseFloat(host.querySelector('svg').getAttribute('viewBox').split(' ')[2]) || 1);
          tip.style.left = (mk.x * s) + 'px';
          tip.style.top = (mk.y * s) + 'px';
          tip.hidden = false;
        }
      });
      function setHot(key, i, rotate) {
        hot = key ? { key: key, i: i } : null;
        g.highlight(key, i);
        if (legend) legend.querySelectorAll('[data-topic]').forEach(function (a) {
          a.classList.toggle('is-hot', a.getAttribute('data-topic') === key);
        });
        var t = key && byKey(key);
        if (tip) {
          if (t) {
            var name = i != null ? t.names[i] : '';
            tip.textContent = t.title + (name ? ' · ' + name : '');
            tip.style.setProperty('--c', t.color);
          } else tip.hidden = true;
        }
        if (t && rotate && t.regions.length) g.rotateTo(t.regions[0][1], t.regions[0][0]);
      }
      g.marks.forEach(function (mk) {
        mk.node.addEventListener('pointerenter', function () { if (!open) setHot(mk.t.key, mk.i, false); });
        mk.node.addEventListener('pointerleave', function () { if (!open) setHot(null); });
        mk.node.addEventListener('focus', function () { if (!open) setHot(mk.t.key, mk.i, false); });
        mk.node.addEventListener('blur', function () { if (!open) setHot(null); });
      });
      // ---- 탐색 카드
      var box = document.querySelector('[data-explore]');
      function aim(t, i) {                             // 카드가 아래를 덮으므로 지역이 위쪽에 오게 돌린다
        var r = t.regions[i] || t.regions[0];
        g.rotateTo(r[1], clamp(r[0] - 24, -60, 60));
      }
      function pick(key, i) {
        var t = byKey(key), card = box.querySelector('[data-xp="' + key + '"]');
        if (!t || !card) return;
        open = { key: key, i: i };
        card.querySelectorAll('[data-xp-r]').forEach(function (b) { b.setAttribute('aria-pressed', String(+b.getAttribute('data-xp-r') === i)); });
        var lab = card.querySelector('[data-xp-region]');
        if (lab) lab.textContent = t.names[i] || '';
        g.highlight(key, i);
        aim(t, i);
      }
      function openCard(key, i, kb, from) {
        if (!box) return false;
        box.querySelectorAll('[data-xp]').forEach(function (c) { c.hidden = c.getAttribute('data-xp') !== key; });
        box.hidden = false;
        if (legend) { legend.setAttribute('inert', ''); legend.setAttribute('aria-hidden', 'true'); }
        host.classList.add('is-exploring');
        g.hold(true);
        if (tip) tip.hidden = true;
        hot = null;
        pick(key, i || 0);
        opener = kb ? from : null;
        if (kb) { var f = box.querySelector('[data-xp="' + key + '"] [data-xp-focus]'); if (f) f.focus(); }
        return true;
      }
      function closeCard() {
        if (!box || box.hidden) return;
        box.hidden = true;
        if (legend) { legend.removeAttribute('inert'); legend.removeAttribute('aria-hidden'); }
        host.classList.remove('is-exploring');
        open = null;
        g.highlight(null);
        g.hold(false);
        if (opener && document.contains(opener)) opener.focus();
        opener = null;
      }
      if (box) {
        box.addEventListener('click', function (e) {
          if (e.target.closest('[data-xp-close]')) { closeCard(); return; }
          var b = e.target.closest('[data-xp-r]');
          if (b && open) pick(open.key, +b.getAttribute('data-xp-r'));
        });
        document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !box.hidden) closeCard(); });
        g.marks.forEach(function (mk) {
          mk.node.addEventListener('click', function (e) {
            if (e.defaultPrevented) return;              // 드래그 직후 클릭
            e.preventDefault();
            openCard(mk.t.key, mk.i, e.detail === 0, mk.node);
          });
        });
      }

      if (legend) legend.querySelectorAll('[data-topic]').forEach(function (a) {
        var key = a.getAttribute('data-topic');
        a.addEventListener('pointerenter', function () { if (!open) { g.hold(true); setHot(key, 0, true); } });
        a.addEventListener('focus', function () { if (!open) { g.hold(true); setHot(key, 0, true); } });
        a.addEventListener('pointerleave', function () { if (!open) { g.hold(false); setHot(null); } });
        a.addEventListener('blur', function () { if (!open) { g.hold(false); setHot(null); } });
        a.addEventListener('click', function (e) {
          if (box && openCard(key, 0, e.detail === 0, a)) e.preventDefault();
        });
      });

      var nk = document.querySelector('[data-night-key]');
      if (nk) {
        var tm = nk.querySelector('[data-night-time]');
        var tick = function () {
          var d = new Date();
          if (tm) { tm.textContent = 'UTC ' + ('0' + d.getUTCHours()).slice(-2) + ':' + ('0' + d.getUTCMinutes()).slice(-2); tm.setAttribute('datetime', d.toISOString()); }
        };
        tick(); setInterval(tick, 60000);
        nk.hidden = false;
      }
    }

    // ---------------- 연구 개요 미니 지구본
    document.querySelectorAll('[data-mini-globe]').forEach(function (h) {
      var t = byKey(h.getAttribute('data-mini-globe'));
      if (!t || !t.regions.length) return;
      makeGlobe(h, { land: land, topics: [t], links: false, auto: false, mini: true, center: centerOf(t) });
    });

    // ---------------- 연구 주제 페이지: 지역 버튼 → 회전·확대
    document.querySelectorAll('[data-topic-globe]').forEach(function (h) {
      var t = byKey(h.getAttribute('data-topic-globe'));
      if (!t || !t.regions.length) return;
      var home = centerOf(t);
      var gl = makeGlobe(h, { land: land, topics: [t], links: false, auto: false, zoomable: true, center: home, caps: 7 });
      var cap = document.querySelector('[data-region-caption]');
      var btns = Array.prototype.slice.call(document.querySelectorAll('[data-region]'));
      var tourBtn = document.querySelector('[data-tour]');
      var cur = -1, timer = 0;
      var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      function show(i) {
        cur = i;
        btns.forEach(function (b) { b.setAttribute('aria-pressed', String(+b.getAttribute('data-region') === cur)); });
        if (cur < 0) { gl.highlight(null); gl.rotateTo(home[0], home[1], 1); if (cap) cap.textContent = ''; return; }
        var r = t.regions[cur];
        gl.highlight(t.key, cur);
        gl.rotateTo(r[1], r[0], 1.8);
        if (cap) cap.textContent = t.names[cur] || '';
      }
      function setTour(on) {
        if (!tourBtn) return;
        clearInterval(timer); timer = 0;
        tourBtn.setAttribute('aria-pressed', String(on));
        var lab = tourBtn.querySelector('[data-tour-label]');
        if (lab) lab.textContent = tourBtn.getAttribute(on ? 'data-pause' : 'data-play');
        if (cap) cap.setAttribute('aria-live', on ? 'off' : 'polite');
        if (on) {
          show((cur + 1) % t.regions.length);
          timer = setInterval(function () { show((cur + 1) % t.regions.length); }, 3000);
        }
      }
      btns.forEach(function (b) {
        b.setAttribute('aria-pressed', 'false');
        b.addEventListener('click', function () {
          var i = +b.getAttribute('data-region');
          setTour(false);
          show(i === cur ? -1 : i);
        });
      });
      if (tourBtn && t.regions.length > 1 && !reduce) {
        tourBtn.hidden = false;
        tourBtn.addEventListener('click', function () { setTour(tourBtn.getAttribute('aria-pressed') !== 'true'); });
        gl.svg.addEventListener('pointerdown', function () { if (timer) setTour(false); });
        h.addEventListener('keydown', function () { if (timer) setTour(false); });
      }
    });
  });
})();
