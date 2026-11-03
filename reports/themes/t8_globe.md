# t8_globe — Interactive Globe

## 완료 기준
- `build.py --theme t8_globe`: 24쪽(EN 8 + KO 8 + 뉴스 상세 4×2). `validate.py`: **오류 0**.
- 경고 2건: placeholder 8건, 그리고 `publications: needs_review/hidden 1건`. 두 번째 경고는 작업 도중 주 세션이 논문 데이터를 317편(숨김 1)으로 바꾸면서 생긴 데이터 쪽 경고이고, 테마와는 관계없다.
- 스크린샷: `site/_shots/t8_globe.png`, `t8_globe_mobile.png`(최종). 검토용 파일은 `_research`, `_publications`, `_people`, `_news`, `_news-2025-12-13-super-el-nino`, `_contact`, `_ko`, `_ko_mobile`, `_full`.

## 디자인 요약
- **다크 전용**, 우주·심해 분위기(`color-scheme: dark`).
  - 배경: 짙은 남색 그라디언트 위에 청록·주황 성운광을 얹고, 크기가 다른 타일 두 겹(311px, 487px)으로 별을 찍어 반복 무늬가 덜 보이게 했다.
  - 포인트: 네온 청록 #2ef2d0, 주황 #ff8a3d.
  - 글꼴: 제목은 Space Grotesk 700에 큰 크기(홈 히어로 최대 6rem, 국문은 4.3rem으로 줄여 한 줄 유지), 본문은 Pretendard. 둘 다 대체 글꼴 체인이 있다.
- **히어로 지구본**(`assets/globe.js`)
  - 렌더링: d3-geo 정사영으로 바다 그라디언트, 경위선, 육지(청록 외곽선), 음영, 대기 halo를 그린다.
  - 연구 지역 표시: `research[].regions`를 주제별 색(`--t0..--t4`, 청록·주황·하늘·라임·자홍)의 빛나는 점과 맥동 링으로 표시한다(11개). 각 점은 SVG `<a href="research.html#key">`라서 클릭과 키보드 Tab/Enter 모두 이동한다. 뒤쪽 반구의 점은 숨기고, 가장자리로 갈수록 흐려진다.
  - 회전: 자동 회전(약 5.5°/s)을 기본으로 하고, 드래그 회전에는 관성이 있다. 터치에서는 `touch-action: pan-y`라 세로 스와이프로 페이지가 스크롤된다.
  - 키보드: 지구본에 포커스를 두고 방향키로 돌린다.
  - 회전 정지 조건: 마우스가 지구본이나 범례 위에 있을 때, 화면 밖일 때(IntersectionObserver), 탭이 숨겨졌을 때.
  - 드래그와 클릭 구분: 4px 이상 움직였을 때만 포인터를 캡처해서, 링크 클릭이 막히지 않는다.
  - **`prefers-reduced-motion`**: 자동 회전·관성·전환 애니메이션·맥동을 끈다. 드래그만 남는다.
- **범례**: 지구본 아래 주제 목록. 각 항목은 `research.html#key` 링크이고 지역 수를 보여 준다. 마우스를 올리거나 포커스하면 지구본이 그 주제의 첫 지역으로 돌아가고, 해당 점이 강조되며 툴팁이 뜬다. JS가 없어도 링크 목록은 그대로 동작한다.
- **지형 자료**
  - `assets/vendor/world-110m.js`: world-atlas@2.0.2 land-110m(Natural Earth, public domain)을 `window.WORLD_LAND_110M` 변수로 넣었다. fetch를 쓰지 않으므로 file://에서도 동작한다.
  - 라이브러리: d3-array@3, d3-geo@3.1.2, topojson-client@3 UMD를 `assets/vendor/`에 두었다. 라이선스는 `vendor/LICENSES.txt`.
  - npm 설치는 테마 밖 스크래치 폴더에서 했다. vendor 전체 크기는 약 116KB.
- 홈 구성: 히어로(소속, 큰 연구실명, 태그라인, CTA, 지구본, 범례, 실제 수치 4개 — 논문, 연구 분야, 영상, 연구 지역), 소개문, 01 연구 분야 카드(외곽선 번호, 주제색, 위경도 칩), 02 뉴스, 03 최근 논문, 04 영상, 05 Latest, Join us 띠.
- 하위 페이지
  - 공통 머리: 큰 제목과 장식 행성(CSS, 위성 궤도 애니메이션, 감속 모션이면 정지, 모바일에서는 숨김).
  - 연구: 주제마다 **미니 지구본**이 해당 주제의 지역을 중심에 두고 그 지역 점만 보여 준다(드래그 가능, `aria-hidden`). 위경도는 figcaption 텍스트로도 적었다. 관련 논문은 원형 번호 배지로 `publications.html#pub-N`에 연결된다.
  - 논문: 왼쪽에 sticky 연도 레일(편수 포함, 길면 스크롤, 모바일은 칩), 오른쪽에 `m.pub_list`(검색·연도 섹션·`p.num`).
  - 구성원: PI 행성형 이니셜 원판과 궤도형 이력 타임라인.
  - 뉴스: 최신 1건을 가로 대형 카드로 둔다.
  - 연락처: 큰 그라디언트 이메일.

## 확인한 화면
- 데스크톱 1440: 홈(전체 길이), 연구(미니 지구본), 논문(317편), 구성원, 뉴스 상세(super-el-nino), 국문 홈, 범례 hover 상태(극지 주제로 회전·강조·툴팁).
- 모바일 390: 홈(전체 길이), 연구, 논문, 국문 홈, 메뉴를 연 상태.
- 자동 점검(Playwright)
  - 전 24쪽을 360px에서 열었을 때 가로 넘침 0, JS 오류 0.
  - 메뉴 토글 정상.
  - 지구본: 점 11개, 육지 경로 생성, 드래그 회전 동작. 드래그 직후 실제 마우스 클릭과 Tab+Enter 모두 `research.html#climate-change`로 이동(감속 모션 켬/끔 두 경우).
  - 감속 모션에서 1.5초 동안 지구본이 정지해 있음, 미니 지구본 5개 생성.
  - 다른 에이전트의 공용 점검 스크립트에서도 문제 0건.
- 대비: muted #a8bdd6 / glass 7.7:1, dim #8aa0bb 5.5:1, 청록 / 배경 13:1, 주황 8:1.

## 남은 문제
- 다크 전용이라 라이트 모드가 없다(브리프의 "어두운 배경" 컨셉).
- 지구본은 JS가 필요하다. JS가 없으면 지구본 자리에 CSS 구체만 남고, 범례 링크로 모든 기능에 접근할 수 있다.
- 한 주제의 지역이 서로 반대편에 있으면(예: 극지 80°N / 78°S) 미니 지구본에는 첫 지역 쪽만 보인다. 모든 위경도는 캡션에 적어 두었다.
- 대표 지역 좌표는 `data/research.yaml` 값을 그대로 쓴다(장식용 점이 아니라 데이터). 좌표가 바뀌면 자동으로 반영된다.
- 전체 길이 스크린샷에서 lazy 이미지가 비어 보이는 것은 캡처 방식 때문이다.

## 공통 코드 제안 (수정하지 않음)
1. **i18n.yaml 추가 제안**(지금은 템플릿 안에서 처리):
   - `common.skip`(Skip to content / 본문 바로가기)
   - `globe.label`(지구본 aria-label 문장)
   - `globe.hint`(Drag to rotate · tap a glowing point / 드래그해서 돌리기 · 빛나는 점을 눌러 보세요)
   - `globe.regions`(Regions / 연구 지역)
   - `common.map_data`(Map data / 지도 자료)
2. `research.yaml`의 `regions`에 지역 이름(예: `{lat, lon, name{en,ko}}`)을 넣을 수 있으면 툴팁·캡션에 "Equatorial Pacific"처럼 의미 있는 이름을 보여 줄 수 있다.
3. 공통 제안(t4와 같음)
   - `macros.news_body`의 국문 대체 안내문 하드코딩을 i18n으로 옮긴다.
   - 연구 페이지에서 `pub_item` id가 중복되는 문제를 막는다.
   - `stats.journals`(고유 학술지 수) 추가.
   - `shared.js` 메뉴에 Esc로 닫기 추가.
