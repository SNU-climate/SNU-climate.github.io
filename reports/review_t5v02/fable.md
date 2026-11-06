# t5.v02 리뷰 — Fable

범위: `git diff 7584534..148a7a8 -- themes/t5.v02 themes/_shared/assets/shared.js data/i18n.yaml scripts/preview/preview_family.py`
확인 방법: 스크래치 빌드(`build.py --theme t5.v02 --out …/review_fable/site`) + Playwright(chromium 1.48) 자동 점검 + 로컬 http 서버.
점검 스크립트·캡처: `/tmp/claude-1500/-data5-CSL-homepage/3efc62de-b047-4116-9c2c-f3e7d402120c/scratchpad/review_fable/{check.mjs,check2.mjs,check3.mjs,shots/}`.
저장소 파일은 이 보고서 외에 건드리지 않았다.

## 지적 (심각도순, 15개 이내)

### 1. [중간] 커버를 키보드로 넘길 때 포커스가 `body`로 떨어진다 (inert·disabled)
- 위치: `themes/t5.v02/assets/t5.js:45–47` (`s.inert = i !== cur`), `:43–44` (`prev.disabled`/`next.disabled`), `:55–60` (track keydown)
- 문제: (a) 현재 편의 링크(`.cover-link`)에 포커스를 둔 채 →를 누르면 keydown이 트랙까지 올라와 `go(1)`이 실행되고, 방금 포커스돼 있던 편이 `inert`가 되면서 포커스가 `document.body`로 빠진다. (b) 2번 편에서 ‹ 버튼에 포커스하고 Enter → 1번으로 가며 `prev.disabled = true` → 역시 포커스 소실. Chrome은 "sequential focus starting point"를 남겨 다음 Tab이 근처로 가지만, Firefox/Safari는 문서 처음으로 갈 수 있고 스크린리더는 포커스 소실을 아무것도 없는 곳으로 읽는다.
- 재현: 1440px 홈. `focus('.cover-story:not([inert]) .cover-link')` → ArrowRight → `document.activeElement` = `body`(측정값 `page-index:`). 2번 편에서 `focus('[data-cover-prev]')` → Enter → activeElement = `body`.
- 수정안:
  ```js
  track.addEventListener('keydown', function (e) {
    if (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return;
    e.preventDefault();
    if (document.activeElement !== track) track.focus({ preventScroll: true });  // 편 안의 링크에서 눌렀을 때
    go(e.key === 'ArrowRight' ? 1 : -1);
  });
  // update() 안: 비활성화할 버튼이 포커스를 갖고 있으면 반대쪽으로 넘긴다
  if (prev.disabled && document.activeElement === prev) next.focus();
  if (next.disabled && document.activeElement === next) prev.focus();
  ```
  또는 `disabled` 대신 `aria-disabled="true"`를 쓰고 click에서 무시하면 포커스 유지와 SR 안내가 둘 다 된다.

### 2. [중간] 데스크톱에서 hover 열림(CSS)과 클릭 토글(JS)이 충돌해 `aria-expanded`와 화면이 어긋난다
- 위치: `themes/t5.v02/assets/style.css:88` (`@media (hover: hover) and (min-width: 861px) { .nav-dd:hover .nav-dd-menu { display: block } }`), `themes/t5.v02/assets/t5.js:14`
- 문제: 마우스를 올리면 CSS만으로 열리므로 `aria-expanded="false"`인 채 메뉴가 보인다. 올린 상태에서 클릭 → `true`, 다시 클릭 → `false`인데 `:hover`가 살아 있어 메뉴는 계속 보인다. 사용자는 "닫기"를 눌렀는데 반응이 없는 것처럼 느끼고, 마우스를 떼야 닫힌다.
- 재현: 1440px, `hover('.nav-dd-btn')` → `exp=false / display=block`; click → `true / block`; click → `false / block`(여전히 보임); 마우스 이탈 → `none`.
- 수정안: JS가 있을 때는 hover도 JS로 처리해 상태를 한 곳에서 관리한다.
  ```js
  dd.addEventListener('pointerenter', function (e) { if (e.pointerType === 'mouse') set(true); });
  dd.addEventListener('pointerleave', function (e) { if (e.pointerType === 'mouse') set(false); });
  ```
  CSS hover 규칙은 `.nav-dd:not(.dd-js):hover .nav-dd-menu`로 한정(JS 없을 때만).

### 3. [중간] 영문 메뉴가 861–약 930px에서 두 줄로 꺾이고, 열린 드롭다운이 둘째 줄(Contact)을 덮는다
- 위치: `themes/t5.v02/assets/style.css:593–598` (1180px 구간 패딩), `:611` (860px 경계), `themes/t5.v02/templates/base.html:51` (svg 10px + gap 6px)
- 문제: 영문 메뉴 항목 폭 합이 865px로 861px 컨테이너보다 크다. 예전 링크 마크업도 861–900px에서 꺾였지만(기존 문제), 버튼의 화살표·gap 16px 때문에 꺾이는 구간이 ~930px까지 넓어졌고, 이제는 열린 패널(absolute)이 둘째 줄의 CONTACT를 가린다(캡처 `shots/dd_861.png`). 국문은 861–1440 모두 한 줄(48px).
- 재현: 영문 홈을 861·900·920px로 열면 `.nav-in` 높이 89px(2줄), 940px부터 45px(1줄). `.nav-dd`를 `<a>People</a>`로 바꿔 재면 920px은 1줄 → 16px가 경계를 넓힌 원인.
- 수정안: `@media (max-width: 960px) { .nav a, .nav-dd-btn { padding: 12px 8px; letter-spacing: .06em; } .nav a[aria-current="page"]::after, .nav a.is-section::after, .nav-dd-btn.is-section::after { left: 8px; right: 8px; } }` 또는 모바일 메뉴 경계를 860→940px로 올림.

### 4. [중간] 유튜브 새 탭 대체: `window.open`이 막히면 아무 반응이 없다 (확신 낮음 — claude.ai 샌드박스의 팝업 허용 여부는 여기서 확인 못 함)
- 위치: `themes/_shared/assets/shared.js:14–17`
- 문제: 재생 버튼이 `<button>` 그대로이고 `window.open()` 반환값을 보지 않는다. 팝업 차단기나 artifact iframe sandbox(`allow-popups` 없음)에서는 클릭해도 썸네일만 남고 안내가 없다. 버튼 라벨("Play: …")도 새 창이 열린다는 것을 알리지 않는다.
- 재현: 로컬 http + `window.CSL_NO_EMBED = true; window.open = () => null` 주입 뒤 `.yt-play` 클릭 → iframe 0, facade 그대로, URL 변화 없음.
- 수정안: 새 탭 모드에서는 로드 시점에 버튼을 진짜 링크로 바꿔 둔다(사용자 클릭의 링크 이동은 팝업 차단에 걸리지 않고, 가운데 클릭·우클릭도 된다).
  ```js
  if (location.protocol === 'file:' || window.CSL_NO_EMBED) {
    document.querySelectorAll('.yt-facade[data-yt] .yt-play').forEach(function (btn) {
      var a = document.createElement('a');
      a.className = btn.className; a.target = '_blank'; a.rel = 'noopener';
      a.href = 'https://www.youtube.com/watch?v=' + encodeURIComponent(btn.closest('.yt-facade').getAttribute('data-yt'));
      a.setAttribute('aria-label', (btn.getAttribute('aria-label') || '') + ' (YouTube)');
      while (btn.firstChild) a.appendChild(btn.firstChild);
      btn.replaceWith(a);
    });
  }
  ```
  최소한 `var w = window.open(...); if (!w) location.href = url;`.

### 5. [낮음] 모바일(390px)에서 구성원 탭 5개가 잘려 '졸업생'이 안 보이고 스크롤 힌트가 없다
- 위치: `themes/t5.v02/assets/style.css:901–908` (`.ptabs { flex-wrap: nowrap; overflow-x: auto; scrollbar-width: none }`), `themes/t5.v02/templates/_t5.html:190–194`
- 문제: 논문 탭(3개)용 규칙을 구성원 탭(5개)이 그대로 쓴다. 국문 교수 페이지 390px에서 "졸업생 23"이 오른쪽에서 잘리고 스크롤바도 숨겨 더 있다는 표시가 없다(캡처 `shots/m_pi_ko.png`).
- 재현: `ko/people/jong-seong-kug.html` 390px.
- 수정안: `people_tabs`에 `ptabs ptabs--people` 클래스를 주고 모바일에서 `flex-wrap: wrap`(두 줄) 허용하거나, `.years-fade`처럼 오른쪽 그라데이션으로 스크롤 힌트를 준다.

### 6. [낮음] 포커스 가능한 트랙에 역할·이름이 없고, 슬라이드 `aria-label`이 제목을 덮는다
- 위치: `themes/t5.v02/templates/index.html:38` (`<div class="cover-track" tabindex="0">`), `:40` (`<article aria-roledescription="slide" aria-label="1 / 8">`)
- 문제: 이름 없는 `div[tabindex=0]`은 스크린리더에서 "빈 포커스 지점"으로 읽힌다. APG 캐러셀은 키 처리를 맡는 요소에 `role="group"`·이름을 둔다. `<article aria-label="1 / 8">`은 article의 접근 가능한 이름을 번호로 덮어 기사 제목 대신 "1 / 8 slide"만 읽힌다.
- 수정안: 트랙에 `role="group" aria-label="{{ x.L('cover') }}"`(또는 `aria-labelledby`), 슬라이드는 `aria-label="{{ loop.index }} / {{ n }}: {{ tr(p.title) }}"` 또는 label을 빼고 `aria-roledescription="slide"`만 둔다.

### 7. [낮음] 안 쓰게 된 CSS가 남아 있다
- 위치: `themes/t5.v02/assets/style.css:421–427` (`.jump*`), `:428` (`.profile--card`), `:445` (`.profile-more`), `:449–450` (`.interest-list--compact*`), `:476` (`.team--alumni`), `:113–115` 선택자 목록의 `.jump a`, `:672`·`:674`의 `.profile--card`
- 문제: people.html이 리다이렉트 페이지로 줄면서 t5.v02 템플릿 어디에도 없다(grep 0건). `.byline*`·`.cover--text`는 정리됐는데 이들만 남았다.
- 수정안: 삭제.

### 8. [낮음] 커버 후보가 "최신 10편"이 아니라 2015년 수상 소식까지 거슬러 간다
- 위치: `themes/t5.v02/templates/index.html:9` (`cands … ns.covers|length < 10`)
- 문제: 표지 있는 논문·수상이 8편뿐이라 5/8이 2015–2021년 글(2015 APEC 상, 2016 이달의 과학자 등)이 "Cover story"로 돈다. 요청("과거 기사까지")대로이긴 하나 홈 첫 화면의 편집 톤과 어긋날 수 있다(편집 판단).
- 수정안(선택): 최근 N년(예: `p.year >= stats.last_year - 2`)으로 제한하거나, 그대로 두고 표지 있는 새 논문 뉴스가 쌓이면 자연 해소되게 둔다.

### 9. [낮음] 미리보기 1테마 모드: 카드 태그가 "확장판"으로 남고, `bar()`가 안 쓰는 `opts`를 만든다
- 위치: `scripts/preview/preview_family.py:101–102` (`kind`), `:48–49` (`opts`), `:115` (`one`)
- 문제: 실행 결과 eyebrow는 "확정 시안"인데 카드 태그는 `t5.v02 · 확장판`. `opts`는 테마 1개일 때 계산만 하고 버린다.
- 재현: `preview_family.py … 'Science Magazine' t5.v02` → `pv1/index.html`의 `<span class="tag">t5.v02 · 확장판</span>`.
- 수정안: `one = len(themes) == 1`을 cards 앞으로 올리고 `kind = '' if one else {...}.get(ver, '')`; `opts` 계산은 `len(themes) > 1` 분기 안으로.

### 10. [낮음] 자잘한 문구·마크업
- 위치: `themes/t5.v02/templates/people.html:6` (`{% block plead %}{% endblock %}`), `themes/t5.v02/templates/_t5.html:187` (`people_lead`)
- 문제: 레거시 people.html은 refresh가 안 될 때 빈 `<p class="phead-lead"></p>`를 남긴다. 영문 lead는 졸업생 1명이면 "1 alumni", 빈 역할이면 "0 members".
- 수정안: `{% block plead_wrap %}{% endblock %}`로 빈 p 제거; `'alumnus' if n == 1 else 'alumni'`.

## 확인했고 문제없음 (한 줄씩)
- 드롭다운 마우스: 클릭 토글, 바깥 클릭 닫힘, 마우스 올림 열림/이탈 닫힘(1440px) 확인.
- 드롭다운 키보드: Enter/Space 열림 → Tab으로 첫 항목(Professor) 진입 → 마지막 항목 지나면 닫힘(Publications로), Shift+Tab 이탈 시 닫힘, 2번째 항목에서 Esc → 닫히고 버튼으로 포커스 복귀, 닫힌 상태의 Esc는 무해.
- 모바일 아코디언: 메뉴 안 탭으로 열고 닫힘(aria-expanded 동기), Esc 1회는 드롭다운만 닫고 전체 메뉴는 유지(stopPropagation) — 주 세션 t5check 결과와 일치.
- aria-current: 하위 페이지·교수 페이지에서 해당 항목에만, 다른 구성원 개인 페이지는 버튼 `is-section`만(빌드 결과 확인). 드롭다운 항목의 `::after` 밑줄은 꺼지고 좌측 inset 표시 사용.
- JS 없음: `.nav-dd:not(.dd-js):focus-within`으로 메뉴 열리고 Tab으로 항목 진입; 커버 트랙 가로 스크롤 가능(scrollWidth 9808 > 1184), `.cover-nav`는 `hidden` 유지.
- 국문 메뉴 폭: 861·900·1000·1180·1181·1440 모두 한 줄(48px), 버튼과 링크 높이 동일(`font:` 단축의 line-height normal 영향 없음).
- 1180px 경계: 버튼 패딩·밑줄 위치가 링크 규칙과 함께 11px로 바뀜.
- 커버 번호·버튼: 시작 1/8 prev disabled, 끝 8/8 next disabled; 연타 3회(50ms 간격) → 4번에 정확히 정착(target 누적), 리사이즈 1000↔1440 뒤 `scrollLeft = cur*step` 유지, 휠(deltaX) 스크롤 후 번호 갱신, 터치 스와이프 → 2/8(캡처 `shots/m_cover_after_swipe.png`), reduced-motion에서 즉시 이동(100ms 내 완료).
- inert: 현재 편만 비-inert, 전환 중 scrollLeft≈step/2에서 교체; Tab 순서 트랙 → 현재 편 링크 → ‹ › 버튼.
- 슬라이드 높이 362–471px로 달라도 트랙 높이 471 고정(`align-items:center`)이라 넘길 때 아래 News가 점프하지 않음.
- News 중복: `cover_slugs` 제외로 홈 사진 기사 2편(KBS·유튜브 전쟁의 날씨)은 커버 8편과 겹치지 않음.
- 표지 없는 글: `cover-story--text .cover-link` 1열·860px 규칙 살아 있음; 커버 1편뿐이면 `n > 1` 조건으로 data-cover·tabindex·nav가 모두 빠지고 t5.js는 건너뜀.
- People 분류·인원: researchers 10(postdoc 2 + researcher 8), phd 4, ms 8, alumni 23 — members.yaml 집계와 일치; 역할이 둘 이상일 때만 소제목(researchers만 h2 2개). `about.html`의 22명은 placeholder 제외 `stats.members`로 기존과 동일.
- 개인 페이지 ← 링크: `../people-phd.html#phd` 등 역할 앵커 존재(`id="postdoc|researcher|phd|ms"`), 졸업생은 앵커 없이 `people-alumni.html`.
- `people.html` → `people/jong-seong-kug.html` meta refresh EN/KO 둘 다 동작(Playwright로 확인), `noindex`.
- 국문 제목·문구: `석사과정 | 기후시스템연구실`, lead `8명`; 빈 역할은 `{% else %}` + `common.empty` 처리.
- about·footer 링크: members → people-researchers, alumni → people-alumni, footer People → 교수 페이지(설계 선택).
- Jinja 매크로 공백: 매크로가 한 줄이라 `href`에 공백 없음(4개 페이지 grep 0건); `|trim`은 보험으로 무해.
- 유튜브 http: `.yt-play` 클릭 → `youtube-nocookie.com/embed/…` iframe 삽입 그대로, 팝업 없음; `CSL_NO_EMBED` → `youtube.com/watch?v=…` 새 탭, `window.opener === null`(noopener), iframe 0.
- 다른 26개 테마: `shared.js`만 공유하고 테마별 JS에 `yt-*` 참조 없음 → 바뀌는 것은 file://에서 새 탭으로 여는 동작뿐(shot.mjs 캡처는 재생을 누르지 않아 영향 없음).
- 모바일 390: 홈·국문 홈·교수(EN/KO)·졸업생·연구원(KO)·석사(KO)·people.html 가로 넘침 0; 다크: 버튼 ink/paper, 메뉴 paper 배경 + ink 테두리 + red 상단선으로 대비 충분; 페이지 JS 오류 0.
- `preview_family.py` 1테마 모드: 실행 성공(files 235), 전환 막대에서 select 제거, 모든 페이지에 `CSL_NO_EMBED=true` 주입, 안내 문구의 공지/앨범 수가 실제 집계(99/89)로 바뀜.
- i18n: `nav.people-*` 4개 키 EN/KO 모두 있음; `page_title`이 `t('nav.' ~ page)`로 바로 쓰임. `people.back`·`people.full_profile`은 t5.v02에서만 안 쓰고 다른 테마가 쓰므로 유지가 맞음.
- 코드 일관성: t5.js 주석 밀도·명명(`data-*` 훅, `set()`)이 shared.js와 같은 결; `_t5.html`의 people_* 매크로가 base·member·people-* 5곳에서 단일 출처로 쓰임.
- 규약: `THEME_CONTRACT.md` 1절은 테마 작업이 `_shared`·`scripts`·`data`를 건드리지 않게 하지만, 이번 건은 확정 테마 통합 작업이고 영향 범위가 위와 같이 좁아 허용 가능하다고 판단.
