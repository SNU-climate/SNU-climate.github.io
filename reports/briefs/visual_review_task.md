# 브리프: 템플릿 9종 독립 시각 검토 (Verification 3)

한국어로 보고한다. **파일을 수정하지 않는다**(읽기·검토만).

## 볼 것
스크린샷 폴더 `/data5/CSL_homepage/first_draft/site/_shots/`. 테마: basic, t1_classic, t2_minimal, t3_ocean, t4_dashboard, t5_magazine, t6_sidebar, t7_onepage, t8_globe.
테마마다 다음 이미지를 직접 열어 본다(데스크톱 1440×900 / 모바일 390×844, 뷰포트 첫 화면):
- `<t>.png`, `<t>_mobile.png` — 영문 홈(라이트)
- `<t>_ko_dark.png`, `<t>_ko_dark_mobile.png` — 국문 홈(다크 모드)
- `<t>_publications.png`, `<t>_publications_mobile.png` — 논문 목록
- `<t>_news-2026-10-23-permafrost-soil-moisture.png`, `..._mobile.png` — 뉴스 상세
필요하면 HTML(`site/<t>/...`)과 테마 CSS(`themes/<t>/assets/`)를 읽어 원인을 확인한다.

## 검사 기준
1. 겹침·잘림·넘침(글자가 다른 요소와 겹침, 버튼 줄바꿈, 잘린 제목)
2. 대비(본문·메뉴 글자가 배경과 구분되는지, 다크 모드에서 안 보이는 요소)
3. 국문 표시(한글 글꼴·줄바꿈·어색한 자간, 영문이 남은 화면 문구)
4. 논문 목록 규칙: 최신이 맨 위, 연도 섹션, 번호(최신 317 → 오래된 1), 검색창
5. 모바일: 메뉴 버튼, 헤더 높이, 터치 영역, 첫 화면에 핵심 정보
6. 디자인 완성도(시안으로 보여줄 수준인지)

## 산출물
`/data5/CSL_homepage/first_draft/reports/visual_review.md`:
- 테마별 표: 기준 1~6 각각 통과/문제(문제면 이미지 이름과 구체적 위치·원인 추정)
- 심각도 순 수정 목록(심각: 사용자에게 보여주기 전에 꼭 고칠 것 / 경미)
- 테마별 한 줄 총평
최종 응답 5줄 이내: 심각한 문제 수와 해당 테마, 보고서 경로.
