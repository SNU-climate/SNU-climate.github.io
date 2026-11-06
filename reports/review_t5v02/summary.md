# t5.v02 3자 리뷰 반영 요약 (2026-11-06)

**리뷰 범위**: `7584534..148a7a8`. 지시서는 `reports/briefs/review_t5v02_task.md`다.
**리뷰어**: 세 명이 서로의 결과를 보지 않고 병렬로 검토했다.
- Fable(`fable.md`): 10건
- Opus(`opus.md`): 14건
- Codex gpt-6.1-sol(`codex.md`): 2건

높음은 0건이다. 지적마다 코드와 Playwright로 재현을 확인한 뒤 반영 여부를 정했다.

## 반영

| # | 지적 | 지적한 리뷰어 | 조치 |
|---|---|---|---|
| 1 | 커버를 키보드로 넘기면 포커스가 body로 빠짐(링크가 inert, 끝 버튼이 disabled) | 셋 다 | ←→를 누르면 포커스를 트랙으로 옮긴다. inert로 바꾸기 전에 포커스를 가진 편이 있으면 트랙으로 옮긴다. 끝 버튼은 `aria-disabled`로 바꿔 포커스를 유지한다(`t5.js`). |
| 2 | 마우스 올림(CSS)과 클릭(JS)이 충돌해 aria-expanded가 어긋남. 마우스로 연 메뉴는 Esc로 안 닫힘 | 셋 다 | JS가 있으면 올림도 `set()`으로 처리하고, 올려서 연 메뉴를 누르면 고정한다. CSS `:hover`는 JS가 없을 때만 쓴다. Esc는 document 캡처 단계에서 받는다(모바일 메뉴 Esc와 충돌하지 않음). |
| 3 | 커버 링크 포커스 링이 트랙 overflow에 잘림 | Opus | `.cover-track .cover-link:focus-visible { outline-offset: -3px }` |
| 4 | 모바일에서 구성원 탭 5개가 잘려 현재 탭·Alumni가 안 보임 | Fable·Opus | 600px 이하에서 `.ptabs--people`이 줄바꿈한다. 현재 탭은 항상 화면 안에 있다. |
| 5 | 영문 메뉴가 861–930px에서 두 줄로 꺾이고 드롭다운이 둘째 줄을 가림 | Fable(Opus는 기존 문제로 확인) | 861–980px에서 메뉴 간격을 줄였다. 861·900·940·980px 모두 한 줄(45px)이다. |
| 6 | 팝업이 막히면 유튜브 새 탭이 무반응 | Fable·Opus(확신 낮음) | 새 탭 모드에서는 재생 버튼을 처음부터 진짜 링크(`<a target=_blank>`)로 바꿔 둔다(`shared.js initYtLinks`). 가운데 클릭도 된다. |
| 7 | 규약 문서에 file://·`CSL_NO_EMBED` 동작이 없음 | Opus | `THEME_CONTRACT.md` 4-5절에 한 줄 추가 |
| 8 | 끝에서 누르면 목적지가 남아 `scrollend`가 없는 브라우저에서 반대로 움직임. 높이만 바뀐 resize에도 위치를 다시 잡음 | Opus | 끝에서는 목적지를 만들지 않는다. 휠을 쓰면 목적지를 해제한다. 너비가 바뀔 때만 위치를 다시 잡는다. |
| 9 | 번호 aria-live가 "2"만 읽음, 스크롤 중 매 프레임 다시 씀 | Opus | `aria-atomic="true"`를 넣고, 번호가 바뀔 때만 DOM을 갱신한다. |
| 10 | 슬라이드 높이가 달라 그림이 오르내림 | Opus | 트랙 `align-items: start` |
| 11 | 트랙에 역할·이름이 없고, 슬라이드 label이 제목을 덮음 | Fable | 트랙에 `role="group"`과 이름을 붙였다. 슬라이드 label은 "N / 8: 제목"이다. |
| 12 | 새 역할이 생기면 People 페이지 어디에도 안 나옴 | Opus | 역할 → 페이지 표에 학생 역할만 적고, 나머지 역할은 모두 Researchers 페이지에 나오게 했다(`_ROLE_PAGE`). |
| 13 | 안 쓰게 된 CSS(.jump, .profile--card 등), 단수 문구("1 alumni"), 빈 lead | Fable·Opus | 지웠고, `L('members_n'/'alumni_n')` 사용과 단수형을 처리했다. people.html은 lead를 없앴다. |
| 14 | about의 구성원 수 링크가 일부 페이지(연구원)로 감 | Opus | 구성원 탭 첫 페이지(교수)로 연결 |
| 15 | 옛 주소 `people.html#phd` 등의 앵커가 버려짐 | Opus | 앵커에 맞는 구성원 페이지로 이동하는 짧은 스크립트를 넣었다. |
| 16 | 미리보기 1테마 모드: 카드 태그 "확장판", 안 쓰는 opts·CSL_PAGES(HTML의 22%), 모바일 썸네일이 잘림 | Fable·Opus | 태그는 "확정 시안"으로 바꿨다. opts·CSL_PAGES는 버전이 여럿일 때만 만든다. `.grid--one .thumb .m { bottom: 12px }` |

## 반영하지 않음(사유)

- **커버가 2015년 글까지 거슬러 감**(Fable): 사용자가 "과거 story도 넘기면서" 보기를 요청했다. 표지 있는 새 논문 뉴스가 쌓이면 자연히 최근 글로 채워진다(최대 10편).
- **People 페이지 제목 단계 h1 → h4**(Opus): 이름 h4는 27개 테마가 함께 쓰는 `member_card` 매크로의 구조다. 확정 테마만을 위해 카드를 복제하기보다는, 배포 전 접근성 점검 때 공통 매크로에 heading 인자를 추가하는 쪽이 낫다.
- **"Researchers" 페이지 이름이 역할 이름과 같음, staff가 연구원 페이지에 들어감**(Opus): 페이지 이름은 사용자가 지정했다(PROFESSOR/Researchers/Ph.D. Students/M.S. Students/ALUMNI). 현재 staff는 0명이다.
- **`dd-js`와 `cover--js` 이름 불일치**(Opus): 드롭다운 쪽을 `nav-dd--js`로 바꿔 BEM 형식으로 맞췄다(반영).

## 검증(반영 후)
- `build.py --theme all` 성공, `validate.py` 오류 0(경고 6건은 기존 데이터 경고)
- `check_layout.mjs t5.v02`: 510쪽, 문제 0
- Playwright로 확인한 것:
  - 커버 링크 →→ 뒤 포커스가 트랙에 있음. Enter로 끝까지 가도 포커스가 버튼에 남음.
  - 드롭다운: 올림, 올림+클릭(고정), 이탈, 포커스 없는 Esc, 고정 후 클릭이 모두 기대대로 동작
  - 영문 메뉴 861–1000px 한 줄
  - 모바일 탭: 현재 탭이 화면 안
  - `people.html#phd` → `people-phd.html#phd`
  - file://: 재생 버튼이 `<a target=_blank>`
  - http 로컬 서버: iframe 재생
  - JS 오류 0
