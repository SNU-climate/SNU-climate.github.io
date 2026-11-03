# t4_dashboard — Climate Dashboard

## 완료 기준
- `build.py --theme t4_dashboard`: 24쪽(EN 8 + KO 8 + 뉴스 상세 4×2). `validate.py`: **오류 0**.
- 경고 2건: placeholder 8건, 그리고 `publications: needs_review/hidden 1건`. 두 번째 경고는 작업 도중 주 세션이 논문 데이터를 317편(숨김 1)으로 바꾸면서 생긴 데이터 쪽 경고이고, 테마와는 관계없다.
- 스크린샷: `site/_shots/t4_dashboard.png`, `t4_dashboard_mobile.png`(최종). 검토용 파일은 `_publications`, `_research`, `_people`, `_news-…`, `_ko`, `_full`.

## 디자인 요약
- **다크 전용** 데이터 대시보드(`color-scheme: dark`). 배경 #0b0f16, 패널 #121a26, 포인트는 cool #5cc8ff와 warm #ff7a45 두 가지다. 본문은 Inter와 Pretendard, 수치·라벨은 JetBrains Mono를 쓰고, 웹폰트를 못 받으면 시스템 글꼴로 대체되도록 글꼴 체인을 두었다.
- 상단 구조: 시스템 바(SNU/SEES 링크, 최종 수정일) → 브랜드(CSL 배지) → 탭형 메뉴 → 5px 온난화 줄무늬 띠. 띠는 홈을 뺀 모든 페이지에 들어간다.
- **Warming stripes**(홈 상단 전폭 배너)
  - 자료: NASA GISTEMP v4 `GLB.Ts+dSST.csv`를 2026-11-03에 내려받았다. 연평균(J-D) **1880–2025**(146년)이며, 2026년은 연평균이 `***`라 넣지 않았다.
  - 저장: `assets/data/gistemp.js`에 `window.GISTEMP`(출처·URL·기준기간·조회일 포함)로 넣었다. 다시 만드는 스크립트는 `themes/t4_dashboard/tools/gistemp_to_js.py`.
  - 색: Hawkins 팔레트 16단계, 1971–2000 평균을 중심으로 대칭이다. 화면에 보이는 값은 원자료(1951–1980 대비 편차) 그대로다.
  - 화면 표기: 배너 아래에 기간(1880–2025), 최신값·최고값(`2025 +1.18 °C · warmest 2024 +1.28 °C`), 출처 링크·기준기간을 적었다. 푸터에도 출처·기간이 있다.
  - 조작: 마우스를 올리면 그해 값이 나온다. 키보드로는 `role="slider"`로 ←/→, PageUp/Down, Home/End를 쓸 수 있고 `aria-valuetext`가 갱신된다.
- **지표 카드**(모두 실제 데이터에서 계산): 논문 수, 활동 연도(first–last), 연구 분야 수와 대표 지역 수, 영상 수, 뉴스 수와 최신 월, 학술지 수.
  - 학술지 수는 `pubs|map('journal')|unique`로 센 고유 개수다. `stats.top_journals`는 10개에서 잘리므로 쓰지 않았다.
  - `stats.members`가 0이면(지금은 모두 예시 구성원) 카드를 숨긴다.
- **연도별 논문 수**: 인라인 SVG다. 빈 해는 0으로 채우고, 가로 좌표를 %로 써서 폭이 바뀌어도 글자 크기는 그대로다.
  - 마지막 해는 주황색으로 표시하고, 그해가 빌드 연도이면 "year to date / 현재까지 집계" 주석을 붙인다.
  - 모바일에서는 연도 라벨을 하나 걸러 숨긴다. `<title>/<desc>`에 전체 값을 넣었다.
- **주요 학술지**: 가로 막대(상위 6개, 홈).
- 홈 구성: 개요 + PI 카드, 연구 분야 행(번호, 요약, 대표 지역 위경도 칩, 논문/영상 수), Latest 로그, 최근 논문, 뉴스, 영상.
- 하위 페이지
  - 연구: 주제별 패널. 지표와 위경도를 보여 주고, 관련 논문은 `#번호 → publications.html#pub-N` 링크로 단다. 같은 논문이 두 주제에 걸려도 id가 겹치지 않도록 직접 마크업했다.
  - 논문: 왼쪽에 sticky 연도 인덱스(막대 + 편수, 길면 패널 안에서 스크롤, 모바일은 칩), 오른쪽에 `m.pub_list`(검색·연도 섹션·`p.num`).
  - 구성원: PI 패널과 이력 타임라인. 이니셜 아바타는 그라디언트로 처리했다.
  - 뉴스: 커버가 없으면 점 격자 그래픽으로 대체한다.
  - 연락처: 키-값 패널.

## 확인한 화면
- 데스크톱 1440: 홈(전체 길이), 논문, 연구, 구성원, 뉴스 상세(permafrost), 국문 홈.
- 모바일 390: 홈(전체 길이), 논문, 연구, 메뉴를 연 상태.
- 자동 점검(Playwright)
  - 전 24쪽을 360px에서 열었을 때 가로 넘침 0, JS 오류 0.
  - 메뉴 토글(`data-open`, `aria-expanded`) 정상.
  - stripes: hover 값(1953 +0.08 °C), Home 키(1880 −0.17 °C) 정상.
  - 다른 에이전트의 공용 점검 스크립트(360 라이트 / 1440 다크, 로드 시 iframe 없음)에서도 문제 0건.
- 대비: muted #a3b4c9 / 패널 7.6:1, dim #8597ae / 패널 5.4:1, 링크 10.5:1.

## 남은 문제
- 다크 전용이라 라이트 모드가 없다(브리프의 "다크 기본"에 맞춤).
- JetBrains Mono에는 한글이 없어서, 국문 페이지의 모노 라벨(예: "교수 연구실")은 시스템 고정폭이나 산세리프로 대체되고 자간이 넓어 보인다.
- 연도 막대에 축 제목은 따로 없다(패널 제목이 대신한다).
- 전체 길이 스크린샷에서 lazy 이미지가 비어 보이는 것은 캡처 방식 때문이고, 실제 화면에서는 정상이다.
- GISTEMP 자료는 정적 스냅샷이다. 새해(1월 중순 이후)에 `tools/gistemp_to_js.py`로 갱신해야 그해 줄무늬가 추가된다. 사용법은 스크립트 docstring에 있다.

## 공통 코드 제안 (수정하지 않음)
1. **i18n.yaml 추가 제안**(지금은 템플릿 안에서 `'…' if lang=='en' else '…'`로 처리):
   - `common.skip`(Skip to content / 본문 바로가기)
   - `dash.overview`(Overview / 개요), `dash.years_active`(Years active / 활동 연도), `dash.journals`(Journals / 학술지)
   - `dash.per_year`(Publications per year / 연도별 논문 수), `dash.top_journals`(Top journals / 주요 학술지)
   - `dash.regions`(Regions / 대표 지역), `dash.ytd`(year to date / 현재까지 집계)
   - `dash.source`(Source / 자료), `dash.stripes`(Warming stripes / 온난화 줄무늬), `dash.anomaly_base`(anomaly vs 1951–1980 / 1951–1980 평균 대비 편차)
2. `build.py` stats
   - `stats.journals`(고유 학술지 수)를 추가하면 좋겠다. 지금은 `top_journals`가 `[:10]`에서 잘려서, 길이를 "학술지 수"로 쓰면 틀린 값이 된다.
   - 빈 해를 0으로 채운 `stats.per_year_full`이 있으면 차트 테마들이 같은 로직을 반복하지 않아도 된다.
3. `_shared/macros.html`
   - `news_body`의 국문 대체 안내문("※ 한국어 본문이 아직 없어…")이 하드코딩되어 있다. i18n 키로 옮기는 것을 제안한다.
   - `basic/research.html`처럼 `m.pub_item`을 주제마다 반복해 쓰면, 같은 논문이 여러 주제에 속할 때 `id="pub-N"`이 중복된다. 연구 페이지용으로 id 없는 변형(`pub_item(p, anchor=False)`)을 두면 좋겠다.
4. `shared.js` 메뉴 토글에 Esc로 닫기와 메뉴 링크를 누르면 닫히는 동작을 추가하면 접근성이 좋아진다.
