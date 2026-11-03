# t2_minimal — Modern Minimal

## 결과
- 빌드 성공(24쪽: EN 8 + KO 8 + 뉴스 상세 4×2), validate **오류 0**. 경고 2건은 데이터 쪽(placeholder 8건, 숨긴 논문 1건)이고 테마와 무관.
- 스크린샷: `site/_shots/t2_minimal.png`, `site/_shots/t2_minimal_mobile.png`
- 파일: `themes/t2_minimal/{theme.yaml, templates/(base, ui, 9개 페이지).html, assets/style.css}`

## 디자인 요약
- 흑백(#111/#fff)에 포인트색 하나(#e5482d). 작은 글자에는 대비 4.5:1을 넘기려고 #c93a1f를 쓰고, 다크 모드에서는 #ff6b4f를 쓴다. 글꼴은 Inter(라틴)와 Pretendard(한글). CDN에서 못 받으면 시스템 글꼴로 넘어간다.
- 섹션 번호는 `site.nav` 순서에서 자동으로 매긴다(01 Research … 07 Contact, `ui.no(key)`). 홈 섹션 머리, 하위 페이지 머리말, 모바일 메뉴에서 같은 번호를 쓴다.
- 장식은 얇은 선뿐이다. 히어로 뒤에 4단 세로 그리드 선이 있고, 섹션 위에는 검은 1px 선, 행 사이에는 옅은 선을 둔다. 위계는 굵기와 크기로만 나눈다(히어로 태그라인 최대 6.25rem, 페이지 제목 최대 8rem).
- 논문: 12단 그리드에서 왼쪽 3칸에 큰 연도(sticky, 헤더 바로 아래)를 두고 오른쪽 9칸에 목록을 둔다. 860px 이하에서는 연도가 상단 sticky 띠로 바뀐다. 번호는 `#p.num`이고, 검색 속성(data-pub-*)과 `id="pub-N"`은 그대로 지켰다. 연도 바로가기와 큰 밑줄형 검색창이 있다.
- 사진 대체물: 회색 정사각형에 가는 이니셜(영문 이름 기준)과 주홍 점 하나.
- 연구 주제 그림 대체물: 위경도 30° 격자 위에 `research[].regions` 실제 좌표를 주홍 점으로 찍는다(캡션 "Key study regions").
- 홈은 번호 섹션 7개다: 히어로(태그라인, 소개, `stats` 논문·영상·뉴스 수) → 01 연구 주제 행 → 02 PI → 03 최근 논문(연도|제목) → 04 발표 → 05 뉴스 행(표지 썸네일, 없으면 격자 대체물) → 06 영상 → 07 Join us.
- 뉴스 상세: 큰 제목과 요약, 왼쪽 sticky 정보칸(날짜·분류·연결 논문), 본문(`m.news_body`), 아래에 다른 소식 3건.

## 확인한 화면(직접 열어 봄)
- 데스크톱 EN: 홈(전체), 논문(전체 + 스크롤 중 sticky 연도), 연구, 구성원, 뉴스 상세
- 모바일: 홈(전체), 논문(sticky 연도 띠), 메뉴 열림, KO 구성원
- 다크: KO 홈, 뉴스 상세, 모바일 논문
- 360px 가로 넘침: 10종 페이지 × EN/KO 모두 0px(Playwright로 측정)
- 동작(Playwright): 논문 검색(건수 갱신, 빈 연도 숨김, 결과 없음 문구), YouTube는 클릭 전 iframe 0개이고 클릭 후 1개, 모바일 메뉴 `data-open` 토글, 중복 id 없음
- 논문이 11편에서 317편으로 늘어난 데이터로 다시 빌드해 확인함(연도 27개 바로가기, 히어로 숫자 317)

## 남은 문제
- 웹폰트는 CDN(Google Fonts, jsdelivr)을 쓴다. 오프라인에서는 시스템 산세리프로 표시된다.
- 홈 04 발표는 지금 예시(SAMPLE) 3건만 보인다(데이터 교체 대기).
- 구성원 역할마다 한 명씩이라 구성원 페이지에 여백이 많다. 실제 명단이 들어오면 자연스러워진다.

## 테마 안에서 직접 처리한 문구(i18n.yaml 추가 제안)
| 제안 키 | en | ko |
|---|---|---|
| `common.skip` | Skip to content | 본문 바로가기 |
| `pubs.years` (연도 내비 aria-label) | Years | 연도 |
| `pubs.paper_one` (단수) | paper | 편 |
| `news.more` | More news | 다른 소식 |
| `news.date` / `news.category_label` | Date / Category | 날짜 / 분류 |
| `research.regions` | Key study regions | 주요 연구 지역 |
| `common.snu` (푸터 링크) | Seoul National University | 서울대학교 |

## 공통 코드 제안(수정하지 않음)
1. `scripts/shot.mjs --full`: `loading="lazy"` 이미지가 로드되기 전에 찍혀 썸네일이 검게 나온다. 캡처 전에 끝까지 스크롤하고 기다리는 단계를 넣자.
2. `macros.news_body`: 연결 논문을 `pub_item`으로 그려서 뉴스 페이지에도 `id="pub-N"`과 `data-pub-item`이 붙는다. `pub_item(p, anchor=False)` 옵션이 있으면 좋겠다.
3. `shared.js` 모바일 메뉴: Esc 키나 바깥을 눌러 닫는 기능, 링크를 눌렀을 때 닫히는 기능을 추가하자(지금은 버튼으로만 닫힌다).
4. validate에 360px 가로 넘침 검사(shot.mjs의 overflow 값)를 넣으면 테마 회귀를 잡기 쉽다.
