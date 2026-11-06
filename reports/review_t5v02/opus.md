# t5.v02 리뷰 — Opus

범위: `git diff 7584534..148a7a8 -- themes/t5.v02 themes/_shared/assets/shared.js data/i18n.yaml scripts/preview/preview_family.py`
확인 방법: 스크래치 폴더에 다시 빌드했고 결과가 `site/t5.v02`와 같았다. `validate.py --theme t5.v02`는 오류 0이다. Playwright(Chromium)로 1440·1180·1100·1000·900·861·860·390·360px, EN/KO, 다크, JS 끔, reduced-motion을 확인했다. `python -m http.server`로 실제 http 동작도 확인했다. 점검 스크립트와 캡처는 `/tmp/claude-1500/-data5-CSL-homepage/3efc62de-b047-4116-9c2c-f3e7d402120c/scratchpad/review_opus/`(`check1.mjs`, `stale.mjs`, `shots/`)에 있다.

## 지적 (심각도순, 15개 이내)

### 1. [중간] 커버를 넘기면 키보드 포커스가 body로 사라짐(inert·disabled)
- 위치: `themes/t5.v02/assets/t5.js:44-46`
- 문제: `update()`는 화면 밖 편을 `inert`로 만든다. 그런데 커버 링크에 포커스가 있는 채로 넘기면, 포커스를 가진 편 자신이 inert가 되어 포커스가 `<body>`로 빠진다. 그다음 ←→ 키는 트랙에 닿지 않아 아무 일도 하지 않는다. 브리프가 내세운 "←→ 키" 기능이 링크에 포커스가 있을 때는 한 번만 동작한다. ›를 눌러 마지막 편에 닿을 때도 같다. 포커스를 가진 버튼이 `disabled`가 되면서 포커스가 body로 빠진다(‹와 첫 편도 같다).
- 재현: 홈(1440px)에서 Tab으로 커버 트랙 → Tab(커버 링크 포커스) → `→`. 2/8로 넘어가지만 `document.activeElement`가 `BODY`다. `→`를 다시 눌러도 2/8에 머문다. ›를 연달아 눌러 8/8에 닿으면 activeElement가 `BODY`다.
- 수정안:
  ```js
  slides.forEach(function (s, i) {
    if (i !== cur && s.contains(document.activeElement)) track.focus({ preventScroll: true });
    s.inert = i !== cur;
  });
  var f = document.activeElement;                 // 비활성화될 버튼에 포커스가 있으면 반대쪽으로
  prev.disabled = cur === 0; next.disabled = cur === slides.length - 1;
  if (f && f.disabled) (f === next ? prev : next).focus();
  ```
  (또는 `disabled` 대신 `aria-disabled="true"`를 쓰고 클릭을 무시한다.)

### 2. [중간] 커버 링크의 포커스 링이 트랙의 overflow에 잘림. 가장 높은 편에서는 아예 안 보임
- 위치: `themes/t5.v02/assets/style.css:141-142`(`.cover-track { overflow-x: auto }`), `:30`(`a:focus-visible { outline-offset: 2px }`)
- 문제: 스크롤 컨테이너는 자기 박스 밖을 잘라 낸다. `.cover-link`는 트랙과 폭이 같아서 좌우 링이 항상 잘린다. 트랙 높이를 정하는 가장 높은 편은 링크 박스가 트랙 박스와 정확히 같아(측정: link `[-65,406,128,1312]` = track 같은 값) 링이 네 변 모두 잘려 보이지 않는다(WCAG 2.4.7). 가장 높은 편은 데스크톱에서 2번째, 모바일에서 1번째다. 커버가 1편뿐일 때도 트랙은 `overflow-x:auto`라서 같은 일이 생긴다.
- 재현: 1440px 홈에서 › 한 번 → 트랙 포커스 → Tab. 링크에 포커스가 있지만 테두리가 보이지 않는다(`shots/ring_d_slide2.png`). 1번째 편은 위아래 선만 보인다(`shots/c1_link_focus.png`). 390px에서는 1번째 편부터 보이지 않는다.
- 수정안: `.cover-track .cover-link:focus-visible { outline-offset: -3px; }`처럼 안쪽 링을 쓴다. 또는 트랙에 `padding: 6px; margin: -6px; scroll-padding: 6px;`을 준다.

### 3. [중간] 모바일 People 탭에서 현재 탭이 화면 밖에 있음
- 위치: `themes/t5.v02/assets/style.css:906-908`(`.ptabs { flex-wrap: nowrap; overflow-x: auto; scrollbar-width: none }`), `templates/_t5.html:190-194`
- 문제: 탭 5개가 한 줄 가로 스크롤이고 스크롤 막대가 숨겨져 있으며 현재 탭으로 옮겨 주지 않는다. EN 390px에서 Alumni 페이지는 현재 탭(left 509px)이, M.S. 페이지는 현재 탭(left 375px)이 화면(오른쪽 끝 374px) 밖에 있다. Alumni 페이지는 탭 사이 틈에서 정확히 잘려 "Professor · Researchers · Ph.D. Students"만 보인다. 그래서 탭이 더 있다는 단서도 없다(`shots/tabs_people-alumni.html.png`). 점검표의 "탭의 현재 표시"를 만족하지 못한다. 국문은 "졸업생"이 반쯤 잘린다.
- 재현: 390px, `people-alumni.html` / `people-ms.html`(EN).
- 수정안: t5.js에서 `document.querySelectorAll('.ptabs [aria-current]').forEach(function (a) { a.scrollIntoView({ block: 'nearest', inline: 'center' }); });`. 오른쪽 끝에 `.years-fade` 같은 흐림 단서를 더하거나, People 탭만 모바일에서 `flex-wrap: wrap`을 쓴다. 논문 탭(`pub_tabs`)도 같은 방식으로 고쳐진다.

### 4. [낮음] `scrollend`가 없는 브라우저에서는 목적지(target)가 남아 키·버튼이 반대로 움직임. resize는 높이만 바뀌어도 동작
- 위치: `themes/t5.v02/assets/t5.js:47-52, 66, 68`
- 문제: 마지막(첫) 편에서 →(←)를 누르면 스크롤이 생기지 않는다. 그래도 `target`이 그 번호로 설정된다. 이 값은 `scrollend`나 `target === cur`일 때만 풀린다. `scrollend`가 없으면 트랙패드·휠로 옮긴 뒤에도 이 값이 남아, 다음 키 입력이 남은 목적지를 기준으로 계산된다. 그래서 반대로 이동한다. Chromium에서 `scrollend` 등록을 막아 재현했다(`stale.mjs`): 8/8에서 → → 휠로 6/8 → ← → **7/8**이 된다(정상은 5/8). Safari 지원 여부는 확신 낮음. resize 핸들러는 너비가 그대로여도 `scrollLeft`를 다시 정한다. 모바일 주소창이 접히면서 생기는 resize가 부드러운 넘김 도중에 오면 넘김이 끊길 수 있다(확신 낮음).
- 재현: 위 `stale.mjs`의 no-scrollend 경우.
- 수정안: `go()` 안에서 `if (i === cur) { target = null; return; }`로 스크롤 없는 목적지를 만들지 않는다. `track.addEventListener('wheel', function () { target = null; }, { passive: true });`를 더한다. resize는 `if (track.clientWidth === lastW) return;`로 너비가 바뀔 때만 처리한다.

### 5. [낮음] 번호 aria-live에 `aria-atomic`이 없고, 스크롤하는 동안 프레임마다 다시 씀
- 위치: `themes/t5.v02/templates/index.html:57`, `assets/t5.js:43`
- 문제: live 영역 안에서는 `<span data-cover-i>`만 바뀐다. 그래서 스크린리더는 "2 / 8"이 아니라 "2"만 읽는다. `update()`는 스크롤 중 rAF마다 같은 값으로 `textContent`를 다시 쓴다. 이때 텍스트 노드가 교체되어 같은 번호를 거듭 읽을 수 있다(확신 낮음, NVDA·JAWS 확인 필요).
- 재현: 코드 확인. 스와이프 한 번에 `update()`가 수십 번 불린다.
- 수정안: `<span class="cover-count" aria-live="polite" aria-atomic="true">`. `update()`는 `if (i === shown) return;`처럼 바뀔 때만 DOM·inert·disabled를 갱신한다.

### 6. [낮음] 편마다 높이가 달라 짧은 편 위아래에 큰 여백이 생김
- 위치: `themes/t5.v02/assets/style.css:141`(`.cover-track { align-items: center }`)
- 문제: 트랙 높이는 가장 긴 편을 따른다. 짧은 편은 세로 가운데에 놓인다. 측정값: 모바일 EN 602px 대 431px, KO 587px 대 411px. 짧은 편(예: 4/8 수상 소식)은 그림 위와 "더 보기" 아래에 각각 약 88px 빈칸이 생기고, 넘길 때마다 그림의 위쪽 선이 오르내린다.
- 재현: 390px KO 홈, 4/8로 이동(`shots/m_cover_short_ko.png`).
- 수정안: `align-items: start`로 그림 위치를 고정한다. 그러면 빈칸은 아래에만 생기고 ‹ › 위치도 그대로다.

### 7. [낮음] 드롭다운: 마우스를 올린 채로 누르면 눈에 보이는 변화 없이 상태만 바뀌고, 마우스가 떠나도 열려 있음. Esc는 드롭다운 안에 포커스가 있을 때만 동작
- 위치: `themes/t5.v02/assets/t5.js:14-23`, `assets/style.css:88`
- 문제: 데스크톱에서는 마우스를 올리면 이미 펼쳐진다. 이때 누르면(예전에는 People이 링크였다) `data-open`이 켜지는데 화면은 그대로다. 마우스를 치우면 메뉴가 그대로 남는다. 다시 눌러 닫아도 마우스가 위에 있으면 계속 보인다. Esc 처리기는 `dd`에 붙어 있다. macOS Safari·Firefox는 버튼을 클릭해도 포커스를 주지 않으므로, 마우스로 연 메뉴는 Esc로 닫히지 않는다(확신 중간).
- 재현: 1440px에서 People에 마우스 올림 → 클릭 → 마우스를 (700,700)으로 옮겨도 메뉴가 보인다. 버튼 포커스를 해제(blur)한 뒤 Esc를 눌러도 `aria-expanded="true"`가 그대로다.
- 수정안: 마우스를 올릴 수 있는 데스크톱(`matchMedia('(hover: hover) and (min-width: 861px)')`)에서는 `mouseenter`/`mouseleave`로 `set(true/false)`해서 `aria-expanded`까지 맞추고, `.dd-js`에서는 CSS `:hover` 규칙을 끈다. Esc는 `document`에 `if (dd.hasAttribute('data-open')) { e.stopImmediatePropagation(); set(false); btn.focus(); }`로 단다. t5.js 처리기는 shared.js의 DOMContentLoaded 처리기보다 먼저 등록되므로 모바일 메뉴 충돌도 막힌다.

### 8. [낮음] `people_key`의 기본값(people-researchers)이 페이지 본문의 역할 묶음과 맞지 않음
- 위치: `themes/t5.v02/templates/_t5.html:177-186`
- 문제: `people_key`는 어느 묶음에도 없는 역할을 `people-researchers`로 보낸다(`{% else %}people-researchers`). 하지만 `people_page`·`people_n`은 `postdoc/researcher/staff`만 그린다. 그래서 `members.yaml`의 `roles:`에 새 역할(예: `visiting`)을 넣으면 그 사람은 People 페이지 어디에도 나오지 않는다. 개인 페이지의 ← 링크 `people-researchers.html#visiting`도 앵커가 없어 validate 오류가 된다.
- 재현: 코드 확인(현재 데이터의 역할 7종은 모두 묶음 안에 있어 지금은 문제없음).
- 수정안: researchers 페이지를 "나머지 역할 전부"로 정의한다(`people_page`·`people_n`에서 다른 두 묶음에 없는 역할을 포함). 또는 else 분기를 빼고 validate에서 역할 목록을 묶음과 대조한다.

### 9. [낮음] People 페이지에서 제목 단계를 건너뜀
- 위치: `themes/t5.v02/templates/_t5.html:206`, `themes/_shared/macros.html:146`(`member_card`가 `h4`)
- 문제: 예전 people.html은 h2(Members) → h3(역할) → h4(이름) 순서였다. 이제 Ph.D.·M.S.·Alumni처럼 역할이 하나인 페이지는 h1 → h4, Researchers는 h1 → h2 → h4로 단계를 건너뛴다.
- 재현: `people-ms.html` 제목 순서는 `H1,H4,H4…`(Playwright 측정).
- 수정안: 역할이 하나여도 `<h2 class="visually-hidden">`을 두고, 이름을 h3로 내는 테마 전용 카드를 쓴다(공통 매크로는 그대로 둔다).

### 10. [낮음] "Researchers/연구원" 페이지 이름이 역할 이름과 같고, about의 구성원 수 링크가 일부 페이지로 감
- 위치: `data/i18n.yaml:14`, `themes/t5.v02/templates/about.html:26`
- 문제: 페이지 이름 `nav.people-researchers`("Researchers"/"연구원")가 `people.role.researcher`와 같다. 그래서 h1 "Researchers"와 탭 "Researchers 10" 아래에 소제목 "Researchers 8"이 다시 나온다. 국문 "연구원" 페이지에는 staff("행정직원")도 들어간다. about의 "Members 22" 숫자는 10명만 있는 `people-researchers`로 연결된다(확신 낮음, 명명은 사용자가 정할 일).
- 재현: `people-researchers.html`, `about.html`의 숫자 행.
- 수정안: 페이지 이름을 "Research Staff / 연구진"처럼 역할 이름과 다르게 짓는다. about 숫자는 교수 페이지(People 첫 탭)로 연결하거나 링크를 뺀다.

### 11. [낮음] 유튜브 대체: 팝업이 막히면 반응이 없고, 규약 문서를 갱신하지 않음
- 위치: `themes/_shared/assets/shared.js:14-17`, `themes/THEME_CONTRACT.md:89`
- 문제: `window.open(…, 'noopener')`는 항상 `null`을 돌려준다. 그래서 팝업이 막혔는지 알 수 없다. 미리보기 iframe에 `allow-popups`가 없거나 팝업 차단기가 막으면 재생 버튼을 눌러도 아무 일이 일어나지 않는다(claude.ai 샌드박스 속성은 확인 못 함, 확신 낮음). 규약 4-5절은 여전히 "클릭해야 iframe 로드"라고만 적혀 있다. 그래서 27개 테마 모두에 적용되는 file://·`CSL_NO_EMBED` 동작이 문서에 없다.
- 재현: http에서는 iframe이 생기고(변경 없음), file:// 와 `CSL_NO_EMBED`에서는 새 탭이 열리며 `opener === null`이다(`yt.mjs`). 차단 상황은 재현하지 않았다.
- 수정안: `var w = window.open(url, '_blank'); if (w) { w.opener = null; return; }` 다음에, 막혔을 때는 facade 안에 `<a href="…" target="_blank" rel="noopener">YouTube에서 보기 ↗</a>`를 넣는다. 규약 3-2절에 `CSL_NO_EMBED`, 4-5절에 file:// 예외를 한 줄씩 적는다.

### 12. [낮음] 쓰이지 않게 된 CSS, 하드코딩 문구, 낡은 주석
- 위치: `themes/t5.v02/assets/style.css:115`(`.jump a`), `:421-426`(`.jump*`), `:428`·`:672`·`:674`(`.profile--card`), `:445`(`.profile-more`), `:449-450`(`.interest-list--compact`), `:476`(`.team--alumni`), `:734`, `:93`; `templates/_t5.html:23-24, 187`
- 문제: 옛 people.html에서만 쓰던 규칙이 남아 있다. `people_lead`는 'member/members/alumni/명'을 직접 쓴다. 그런데 같은 뜻의 `_L.members_n`·`_L.alumni_n`은 쓰이지 않고 남아 있다. `.ptabs` 앞 주석은 여전히 "/* 논문 탭 */"인데 이제 People 탭도 쓴다. `.ptabs-wrap` 규칙은 nav 절에 들어가 있다. 상태 클래스 이름도 `dd-js`와 `cover--js`로 서로 다르다.
- 재현: `git grep -e jump -e profile--card -e team--alumni 148a7a8 -- themes/t5.v02/templates`의 결과가 없다.
- 수정안: 위 규칙을 지운다. `people_lead`는 `L('members_n')`·`L('alumni_n')`을 쓴다. 주석은 "논문·구성원 탭"으로 바꾸고 `.ptabs-wrap`은 v02 탭 절로 옮긴다. `dd-js`는 `nav-dd--js`로 바꾼다.

### 13. [낮음] 미리보기 스크립트의 테마 1개 모드: 쓰지 않는 `CSL_PAGES`가 HTML의 22%를 차지하는 등
- 위치: `scripts/preview/preview_family.py:83, 102, 143`
- 문제: 테마가 1개이면 버전 선택 상자를 그리지 않는다. 그런데도 모든 페이지에 전체 페이지 목록 JSON(`window.CSL_PAGES`)을 넣는다. 스크래치 실행(공지 10, 앨범 8) 결과는 HTML 4.38MB 중 0.96MB다. 카드 태그도 확정 시안에 `t5.v02 · 확장판`으로 나온다. 카드를 가로로 놓으면 모바일 썸네일(`.thumb .m { bottom:-18px }`)의 아래 17px가 카드의 `overflow:hidden`에 잘린다.
- 재현: `preview_family.py <repo> <scratch> 10 8 <url> 'Science Magazine' t5.v02`(`shots/pv_index_d.png`).
- 수정안: `pages_js = f'window.CSL_PAGES={json.dumps(pages)};' if len(themes) > 1 else ''`. `one`일 때 kind는 '확정 시안'으로 쓴다. `.grid--one .thumb .m { bottom: 12px; }`.

### 14. [낮음] `people.html`로 이동할 때 #앵커가 버려짐(필요성 낮음)
- 위치: `themes/t5.v02/templates/people.html:4`
- 문제: 옛 주소 `people.html#alumni`·`#phd`로 들어와도 meta refresh가 항상 교수 페이지로 보낸다. 사이트 안에는 이런 링크가 더 없다(content·data에서 확인). 다만 미리보기 링크나 북마크로 남아 있을 수 있다.
- 재현: `people.html#alumni` → `people/jong-seong-kug.html`.
- 수정안: meta 앞에 `<script>var m={alumni:'people-alumni',phd:'people-phd',integrated:'people-phd',ms:'people-ms',undergrad:'people-ms',postdoc:'people-researchers',researcher:'people-researchers',staff:'people-researchers'},h=location.hash.slice(1);if(m[h])location.replace(m[h]+'.html'+(h==='alumni'?'':'#'+h));</script>`를 넣는다.

## 확인했고 문제없음 (한 줄씩)
- 빌드 성공. validate 오류 0(경고 6건은 기존 데이터 경고). 스크래치 빌드는 `site/t5.v02`와 파일 단위로 같다.
- 드롭다운 키보드: Research → People(버튼) → 닫혀 있으면 Publications로 간다. Enter·Space로 펼친다. Tab으로 5개 항목을 지나 밖으로 나가면 닫힌다. 메뉴 안에서 Esc를 누르면 닫히고 포커스가 버튼으로 돌아온다.
- 드롭다운 마우스: 버튼 아래 경계와 메뉴 위 경계가 같은 픽셀이다(283px). 그래서 내려가는 도중에 닫히지 않는다. 바깥을 클릭하면 닫힌다.
- 모바일 아코디언: Esc 1회는 하위 목록만, 2회는 전체 메뉴를 닫는다. 메뉴를 닫았다 열면 하위 목록이 접혀 있다.
- JS가 없을 때 데스크톱은 focus-within·hover로 펼쳐진다. 모바일 메뉴는 원래 JS가 있어야 열린다(기존 동작).
- 경계 폭: 861–920px EN에서 메뉴가 두 줄이 되는 것은 기존에도 그랬다(caret 16px 때문에 늘어난 구간은 905–921px뿐). KO는 861px에서도 한 줄이다. 860px 이하는 햄버거 메뉴로 바뀐다. 가로 넘침 없음.
- aria-current: people-* 페이지와 교수 페이지에서 드롭다운과 탭 모두 맞다. 구성원 개인 페이지에서는 버튼만 `is-section`이다. `<title>`도 맞다("M.S. Students | …").
- 커버: 번호와 ‹ › 비활성화가 맞다. 6번 연달아 누르면 7/8이 된다. 휠·스와이프 뒤에도 스냅 위치와 번호가 맞다. 900px로 줄여도 같은 편을 유지한다. reduced-motion에서는 바로 이동한다. JS가 없으면 nav가 숨고 가로 스크롤로 동작한다.
- 커버 8편은 표지가 있는 paper/award 전부다. 아래 News 사진 기사·짧은 소식과 겹치는 글은 0건이다.
- lazy 이미지: 다음 1–2편을 미리 받아 두어 넘길 때 빈 칸이 생기지 않는다.
- People: 연구원 10(postdoc 2 + researcher 8), 박사 4, 석사 8, 졸업생 23. 국문 제목은 연구원·박사과정·석사과정·졸업생이고 리드는 "N명"이다. 빈 역할이면 `common.empty`가 나온다.
- 개인 페이지 ←는 소속 페이지 + `#role`로 가고 validate 앵커 검사를 통과한다. 졸업생은 앵커 없이 간다. about·푸터의 People 링크도 맞다.
- `people.html`·`ko/people.html`은 교수 페이지로 이동하고 noindex다. 상대 경로도 맞다(`../ko/people/…`).
- 360·390px에서 새 페이지와 홈 모두 가로 넘침 0이다. 다크 모드에서 드롭다운·커버 버튼의 대비에 문제가 없다.
- 유튜브: http에서는 iframe 재생이 그대로다. 다른 26개 테마에는 자체 YouTube 처리기가 없어 충돌이 없다. i18n `nav`를 순회하는 코드가 없어 새 키가 다른 테마 메뉴에 섞이지 않는다.
- Jinja 매크로 반환값: 생성된 HTML의 href에 공백이 없다(`|trim`을 빠뜨린 `people_tabs`도 매크로 본문이 한 줄이라 문제없음).
- 미리보기 테마 1개 모드: 선택 상자와 스크립트가 빠지고, 카드가 가로로 놓이며, 안내 문구도 확정 시안용으로 바뀐다.
