# t1_classic — Classic Academic

## 결과
- 빌드 성공(24쪽: EN 8 + KO 8 + 뉴스 상세 4×2), validate **오류 0**. 경고 2건(placeholder 8건, 숨긴 논문 1건)은 데이터 쪽이며 테마와 무관.
- 스크린샷: `site/_shots/t1_classic.png`, `site/_shots/t1_classic_mobile.png`
- 파일: `themes/t1_classic/{theme.yaml, templates/(base, _t1, 9개 페이지).html, assets/style.css, assets/isobars.svg}`

## 디자인 요약
- 짙은 네이비(#0b2a5b) + 흰 바탕, 장식 선에만 금색(#b8954a, 텍스트에는 쓰지 않음). 제목은 Source Serif 4 / Noto Serif KR, 본문은 Pretendard. CDN 실패 시 Georgia·시스템 산세리프로 대체.
- 헤더 3단: ① 유틸리티 바(서울대·지구환경과학부 링크, YouTube, 이메일, 언어 토글) ② 큰 연구실명(세리프) + 다른 언어 이름 + 소속, 오른쪽에 논문 검색창(`publications.html?q=` 로 제출 → shared.js가 바로 필터) ③ 가로 메뉴(활성 메뉴는 네이비 탭, 아래 3px 네이비 선). SNU 로고 없이 텍스트와 등압선 모양의 작은 SVG 엠블럼만 쓴다.
- 홈: 등압선 배너(장식용 해석적 압력장의 등치선을 matplotlib로 뽑아 `assets/isobars.svg`로 저장 — 데이터 아님, 숫자 표기 없음) → 연구실 소개 + 연구 분야 5개(로마 숫자 목록) | 교수 카드(이니셜 모노그램, 직함·보직·연락처) → 뉴스(날짜-분류-제목 행) | 최근 논문 5편 → 영상 3편 → Join us.
- 하위 페이지: 연한 회청색 머리띠(빵부스러기 + 세리프 제목 + 소개). 연구·논문은 왼쪽 sticky 보조 내비(연구 주제 목록 / 연도 칩), 뉴스 상세는 오른쪽에 다른 소식 목록.
- 그림 대체물: 연구 주제·교수·구성원·연락처 그림은 같은 등압선 SVG를 네이비 패널에 배경으로 깔고(주제마다 위치를 달리함) 로마 숫자나 이니셜을 얹는다.
- 다크 모드: 바탕 #0c1422, 글자 #e2e8f2, 링크·강조 #9cc2ff. 배너·유틸리티 바·푸터는 더 짙은 네이비로 유지.
- 한국어 줄바꿈은 `word-break: keep-all`.

## 확인한 화면(직접 열어 봄)
- 데스크톱 EN: 홈(전체), 연구, 논문, 구성원, 뉴스 상세(permafrost), 뉴스 목록, 연락처(다크)
- 모바일: 홈(전체), 논문(KO, 다크), 뉴스 목록, 메뉴 열림(360px)
- 다크: KO 홈(전체), KO 논문(데스크톱·모바일), 연락처
- Playwright 점검(직접 작성한 스크립트): 24쪽 × (360px 라이트, 1440px 다크) 모두 가로 넘침 0px, 로드 시 iframe 0개, 모바일 메뉴 토글(`data-open`, `aria-expanded`) 정상, 콘솔 오류 없음. 마스트헤드 검색 → `publications.html?q=ENSO`로 이동해 필터 적용 확인.
- 작업 중 논문 데이터가 11편 → 317편으로 늘어서 다시 확인함(연도 27개 칩: 데스크톱은 격자, 모바일은 가로 스크롤 한 줄).

## 남은 문제
- 뉴스 표지·영상 썸네일이 YouTube hqdefault(480×360, 위아래 검은 띠)라 크게 띄우면 흐리다. 16:9로 잘라 띠는 숨겼다.
- 웹폰트는 CDN(Google Fonts, jsdelivr). 오프라인에서는 대체 글꼴로 보인다.
- 구성원·발표는 아직 예시(SAMPLE) 데이터라 구성원 페이지 여백이 많다.
- 마스트헤드 검색창은 900px 이하에서 숨긴다(모바일은 논문 페이지 검색창 사용).

## 테마 안에서 직접 처리한 문구(i18n.yaml 추가 제안)
| 제안 키 | en | ko |
|---|---|---|
| `common.dept` | School of Earth and Environmental Sciences | 지구환경과학부 |
| `home.about` | About the Laboratory | 연구실 소개 |
| `pubs.years` | Years | 연도 |
| `common.breadcrumb` (aria-label) | Breadcrumb | 현재 위치 |

(작업 중 주 세션이 추가한 `common.skip`, `common.snu`, `common.links`는 적용함.)

## 공통 코드 제안(수정하지 않음)
1. `year_index` 매크로의 `aria-label="Years"`가 영어로 고정돼 있다 → `t('pubs.years')`.
2. 뉴스 표지가 없을 때 쓸 고해상도 썸네일(maxresdefault 또는 논문 그림)을 `new_news.py`/`fetch_youtube.py`에서 받아 두면 큰 표지가 선명해진다.
3. `shot.mjs`의 모바일 폭은 390px이다. 규약(360px)과 맞추려면 `--w 360` 같은 옵션이나 validate 쪽 넘침 검사를 추가하자.
4. validate 완료 기준이 "경고는 placeholder 1건만"인데, 데이터에 숨긴 논문이 생기면 모든 테마에 경고가 1건 더 붙는다. 기준 문구를 "데이터 경고 제외"로 고치자.
