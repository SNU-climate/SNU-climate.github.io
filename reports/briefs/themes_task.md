# 브리프: 홈페이지 템플릿 제작 (Task 3)

작업 폴더: `/data5/CSL_homepage/first_draft/`. 서울대 지구환경과학부 기후시스템연구실(국종성 교수) 홈페이지의 디자인 템플릿을 만든다.
모든 템플릿은 같은 데이터를 쓰며, 연구실이 최종 디자인을 고르기 위한 시안이다. 시안이라도 실제로 배포할 수 있는 완성도로 만든다.
한국어로 보고한다.

## 먼저 읽을 파일
1. `themes/THEME_CONTRACT.md` — **필수 규약**(폴더 구조, 컨텍스트 변수, 공통 매크로, 반드시 지킬 11가지, 빌드·검증·스크린샷 명령)
2. `themes/basic/` — 참조 구현(모든 페이지가 컨텍스트를 어떻게 쓰는지)
3. `themes/_shared/macros.html`, `themes/_shared/assets/shared.{js,css}`
4. `data/*.yaml`, `content/news/` — 실제 데이터(수정 금지)

## 담당 테마
주 세션이 지정한 두 테마만 만든다(아래 표에서 해당 행). 폴더 이름은 표의 `폴더` 그대로.

| 폴더 | 이름 | 디자인 방향 |
|---|---|---|
| `t1_classic` | Classic Academic | 전통적인 대학 연구실. 짙은 네이비(#0b2a5b 계열) + 흰 바탕, 세리프 제목(Noto Serif KR / Source Serif), 산세리프 본문. 상단 유틸리티 바(SNU·SEES 링크, 언어 토글) + 큰 연구실명 헤더 + 가로 메뉴. 홈: 등고선/등압선 느낌의 SVG 패턴 배너, 소개문 + 교수 카드, 날짜-제목 행 형식의 뉴스, 최근 논문. 짙은 네이비 푸터. SNU 로고 이미지는 쓰지 않는다(텍스트만). |
| `t2_minimal` | Modern Minimal | 넓은 여백, 큰 타이포그래피, 흑백(#111/#fff) + 포인트색 1개(예: #e5482d). Inter + Pretendard. 섹션 번호(01 Research, 02 People…), 얇은 그리드 선. 논문은 왼쪽에 연도가 sticky로 붙는 2단 목록. 장식 최소화, 정보 위계는 굵기·크기로만. |
| `t3_ocean` | Ocean–Atmosphere | 해수면온도 팔레트(심해 남색 → 청록 → 따뜻한 주황)의 풀스크린 그라디언트 히어로, 천천히 움직이는 파도/등온선 SVG 애니메이션(`prefers-reduced-motion`이면 정지). 반투명(glass) 카드, 둥근 모서리. 라이트: 하늘빛, 다크: 심해. |
| `t4_dashboard` | Climate Dashboard | 다크 기본의 데이터 대시보드. 상단에 **warming stripes** 배너: NASA GISTEMP v4 전지구 연평균 기온 편차(`https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv`)를 내려받아 `assets/data/`에 JS 상수로 저장하고 출처·기간을 화면에 표기(받을 수 없으면 stripes 없이 진행하고 보고). 지표 카드(논문 수, 활동 연도, 영상 수 등 `stats`), 연도별 논문 수 막대그래프(인라인 SVG, `stats.per_year`), 주요 학술지 막대. 모노스페이스 포인트(JetBrains Mono / IBM Plex Mono). |
| `t5_magazine` | Science Magazine | 과학 잡지처럼 뉴스 우선. 마스트헤드, 홈 상단에 최신 뉴스 대형 커버 기사 + 보조 기사 그리드, "Watch" 영상 줄, "From the journals" 최근 논문 띠, 연구 분야 피처 카드. 세리프 디스플레이 제목(Playfair Display / Noto Serif KR), 붉은 포인트. 뉴스 상세는 잡지 기사처럼(큰 표지, 드롭캡, 넓은 행간). |
| `t6_sidebar` | Sidebar Portfolio | 왼쪽 고정 사이드바(약 280px: 연구실명, 메뉴, 언어 토글, 연락처) + 오른쪽 본문(최대 860px). 모바일에서는 상단 바 + 접는 메뉴. al-folio 계열의 깔끔한 학술 스타일. 논문 왼쪽에 학술지 약칭 배지. 홈은 PI 중심(소개·사진 자리·뉴스·대표 논문). |
| `t7_onepage` | One-page Scroll | `index.html` 하나에 모든 섹션(히어로, 연구, 구성원, 최근 논문 10편 + 전체 보기, 뉴스, 영상, 연락처)을 담고, 스티키 내비가 현재 섹션을 표시(IntersectionObserver, 테마 JS). 모바일 우선, 큰 터치 영역. 다른 필수 페이지는 같은 스타일의 상세 페이지. 섹션 링크(`index.html#research` 등)는 실제 id와 일치해야 validate를 통과한다. |
| `t8_globe` | Interactive Globe | 우주/심해 느낌의 어두운 배경에 회전하는 지구본 히어로: d3-geo 정사영 + world-110m 지형을 `assets/vendor/`에 넣고(지형 데이터는 **JS 파일에 변수로 내장** — file://에서는 fetch가 안 된다), `research[].regions`를 빛나는 점으로 표시(클릭 → `research.html#<key>`), 드래그 회전, 감속 모션 설정 존중. 네온 청록·주황 포인트, 대담한 큰 타이포. |

## 공통 요구
- 규약(THEME_CONTRACT.md 4절) 11가지를 모두 지킨다. 특히 상대경로, 논문 연도 섹션·번호(`p.num`)·검색, 언어 토글, YouTube 클릭 로드, 360px 폭 가로 넘침 없음.
- JSON 같은 데이터는 fetch하지 말고 템플릿에서 `<script>` 안에 `{{ 값|tojson }}`으로 넣거나 JS 파일로 둔다(file:// 동작).
- 이미지가 없는 데이터(PI 사진, 연구 주제 그림, 구성원 사진)는 테마 스타일에 맞는 그래픽 대체물(이니셜, 그라디언트, SVG 패턴)로 보기 좋게 처리한다. 사진을 지어내거나 외부 스톡 이미지를 쓰지 않는다.
- 문구는 `t()`/`tr()`로. 새 UI 문구가 꼭 필요하면 테마 템플릿 안에서 `{{ 'Watch' if lang == 'en' else '영상' }}`처럼 처리하고 보고서에 i18n.yaml 추가 제안으로 적는다.
- 품질 확인: 빌드 → validate 오류 0 → 스크린샷(`node scripts/shot.mjs <폴더>`, 필요하면 `[page] --full --ko --dark`)을 **직접 열어 보고** 고친다. 홈, 논문, 뉴스 상세, 모바일은 꼭 본다. shot.mjs가 실패하면(브라우저 미설치) 스크린샷 없이 진행하고 보고서에 적는다.

## 수정 금지
담당하지 않은 테마 폴더, `themes/_shared/`, `themes/basic/`, `themes/THEME_CONTRACT.md`, `scripts/`, `data/`, `content/`, `static/`.
공통 쪽 버그나 개선이 필요하면 고치지 말고 보고서에 적는다. git commit은 하지 않는다(주 세션이 한다).

## 산출물·완료 기준 (테마마다)
1. `themes/<폴더>/`(theme.yaml의 `title`, `concept{en,ko}`, `palette` 포함)
2. `python scripts/build.py --theme <폴더>` 성공, `python scripts/validate.py --theme <폴더>` **오류 0**
3. `site/_shots/<폴더>.png`, `<폴더>_mobile.png` (가능하면)
4. 보고서 `reports/themes/<폴더>.md`: 디자인 요약, 확인한 화면, 남은 문제, 공통 코드 제안
5. 최종 응답은 테마당 2줄 이내(완료 기준 통과 여부 + 보고서 경로).
