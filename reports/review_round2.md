# 시안 9종 2차 리뷰 (실제 데이터 반영 후)

- 검토일: 2026-11-04 / 읽기 전용 검토(이 보고서와 `site/_shots/` 캡처 외에는 파일을 고치지 않음, 빌드도 하지 않음). 대상 빌드는 `site/<theme>/`(11-04 14:53 빌드).
- 데이터: 구성원 22 + 졸업생 23(사진), 논문 318, 뉴스 188(그중 앨범 89), 연구 5주제(원본 그림), 영상 15, 발표 0.
- 캡처(`site/_shots/`, 데스크톱 1440×900 + 모바일 390×844@2x): 테마마다 홈(첫 화면과 전체), people(전체), publications, news, 앨범 글 `news-2025-02-24-snu-kopri-high-latitude-workshop_full`, 논문 소식 `news-2026-10-23-permafrost-soil-moisture_full`, research(전체), contact, presentations(0건 빈 화면), videos, 국문 홈·people·publications·news, 국문 다크 홈. basic은 여기에 `people-yechul-shin_full`·`_ko`, `research-mechanism_full`, `gallery(_full)`, `about_full`, `people_ko_dark`를 더 찍었다. 모든 캡처에서 가로 넘침 경고는 0건이다.
- 자동 점검(Playwright, 스크래치패드 스크립트, 프로젝트에 추가하지 않음): 페이지 높이, 가로 넘침, 24px 미만 터치 대상, 모바일 메뉴 버튼 크기, 상단 고정 영역, 뉴스 목록 속 앨범 링크 수, 논문 수, 빈 화면 문구, JS 오류·404를 쟀다. JS 오류·404는 9종 모두 0건이다. 대비 검사는 근사치라 그라데이션 위 글자(t3 히어로)에서 오탐이 나서 판정 근거로 쓰지 않았다.
- 테마별 초안은 검토 에이전트 3개가 3종씩 나눠 썼다. 통합 단계에서 점수를 9종 기준으로 다시 맞췄고, 사실관계를 교차 확인해 고쳤다(예: 유튜브 썸네일은 15장 중 14장이 이미 1280×720).
- 심각도: **심각** = 보여 주기 전에 반드시 고칠 것 / **보통** = 사용성·완성도를 눈에 띄게 해침 / **경미** = 다듬기. 점수 1~5: 5 그대로 공개 가능, 4 작은 손질, 3 쓸 만하나 눈에 띄는 문제, 2 큰 손질 필요, 1 실패.

---

## 1. 요약

### 1-1. 점수표

| 테마 | 1 데이터 | 2 구조 | 3 시각 | 4 모바일 | 5 콘셉트 | 6 접근성·유지보수 | 합계 | 심각/보통/경미 | 한 줄 총평 |
|---|---|---|---|---|---|---|---|---|---|
| basic | 4 | **5** | 3 | 4 | 2 | 4 | **22** | 0/1/8 | 실데이터를 이미 가장 잘 소화하고 원본 메뉴를 그대로 잇는다. 생김새가 밋밋하다 |
| t1_classic | 2 | 3 | 4 | 3 | 3 | 3 | 18 | 1/3/7 | 대학 공식 사이트 톤은 좋으나 뉴스 목록이 가장 길고 basic과 성격이 겹친다 |
| t2_minimal | 3 | 3 | 4 | 4 | 4 | 3 | 21 | 1/3/6 | 타이포 콘셉트와 논문 페이지가 가장 좋다. 기후 소재와 연결된 장치가 없다 |
| t3_ocean | 3 | 3 | 4 | 3 | 3 | 3 | 19 | 1/4/4 | 그라데이션 완성도는 높지만 실데이터가 들어오며 고유 그래픽이 사라졌다 |
| t4_dashboard | 3 | 4 | 3 | 3 | 4 | 3 | 20 | 1/4/5 | 실데이터 현황판으로 독창적이다. 다크 고정, 구성원 카드, 국문 모노 라벨이 약점이다 |
| t5_magazine | 3 | 2 | 4 | 4 | 4 | 3 | 20 | 2/3/5 | 타이포·모바일 뉴스는 좋지만 연구실 소개문이 없고 커버가 한글 썸네일이다 |
| t6_sidebar | 2 | 3 | 4 | 3 | 3 | 3 | 18 | 1/5/4 | 정돈됐지만 홈이 교수 개인 페이지라 연구실 사이트로 읽히지 않는다 |
| t7_onepage | 3 | 4 | 4 | 3 | 4 | 4 | **22** | 1/5/4 | 길 찾기와 유지보수성이 가장 좋다. 홈의 빈 발표 섹션과 모바일 고정 영역만 고치면 된다 |
| t8_globe | 3 | 3 | 4 | 3 | 4 | 3 | 20 | 1/5/4 | 첫인상과 주제 연결성이 가장 강하다. 1차 지적 4건이 남아 있다 |

- **심각 9건**: 그중 8건은 같은 원인이다. basic 외 8종에서 뉴스 99건과 앨범 89건이 필터·연도 묶음·페이지 나눔 없이 한 목록으로 나온다. 나머지 1건은 t5에 연구실 소개문이 없는 문제다. 8건은 공통 빌드·매크로(3-1절 ①②)로 한꺼번에 풀 수 있다.
- **9종 공통 보통 1건**: 구성원 페이지가 PI 이력(학력·경력·봉사·수상)으로 시작해서, 실제 구성원 목록은 데스크톱 2,100~3,450px, 모바일 3,800~6,100px 아래에서야 시작한다(3-1절 ④).

### 1-2. 핵심 수치

| 테마 | 뉴스 목록 높이 px (데스크톱/모바일) | 뉴스 목록 속 앨범 | 구성원 목록 시작 px (D/M) | 모바일 메뉴 버튼 | 모바일 상단 고정 | 발표 0건 처리 |
|---|---|---|---|---|---|---|
| basic | 10,109 / 13,524 (공지 99) | 0 (갤러리 분리) | 3,066 / 6,081 | 66×44 | 69 | 안내문(`pres.empty`) |
| t1_classic | 37,485 / **75,891** | 89 | 2,488 / 4,027 | 92×**37** | 0 | 안내문, 메뉴 노출 |
| t2_minimal | **39,982** / 41,234 | 89 | 3,068 / 4,098 | **26**×44 | 61 | **홈 04 섹션이 빈 채로 나옴** |
| t3_ocean | 24,824 / 67,315 | 89 | 3,454 / 5,426 (점프 탭 있음) | 44×44 | 떠 있는 헤더 | 안내문 |
| t4_dashboard | 24,011 / 63,365 | 89 | 2,138 / 3,843 | 40×**36** | 0 | 안내문 |
| t5_magazine | 22,600 / 31,244 | 89 | 2,897 / 4,491 | 91×**35** | 0 | 빈 연도 막대가 남음 |
| t6_sidebar | 37,334 / **75,519** | 89 | 2,125 / 3,942 | 44×44 | 61 | `common.empty` 한 줄 |
| t7_onepage | 24,075 / 66,256 | 89 | 3,441 / 5,688 (점프 탭 있음) | 48×48 | **117** | **홈 05 섹션이 빈 채로 나오고, 목차에 "0"** |
| t8_globe | 25,534 / 68,530 | 89 | 2,453 / 3,961 | 42×40 | 69 | 안내문 |

논문 318편은 9종 모두 전부 표시되고 검색이 동작한다(`pubItems` 318). 가로 넘침과 JS 오류는 9종 모두 0이다.

### 1-3. 최종 후보 추천 순위

1. **t7_onepage**: 디자인 시안 중 길 찾기가 가장 좋다. 히어로 목차에 건수가 나오고, 스크롤 스파이와 번호 붙은 브레드크럼이 있다. 공통 매크로(`pub_list`, `news_card`, `pres_list`, `alumni_list`)를 가장 충실히 써서 공통 수정(앨범 분리, 졸업생 사진 등)이 그대로 반영된다. 터치 영역은 44~48px이고 포커스 표시와 Esc 닫기도 있다. 고칠 것(빈 발표 섹션, 홈 구성원 이니셜을 사진으로, 모바일 고정 117px, 다크 형광펜)이 작고 분명해서 v01만으로 공개 수준에 이른다.
2. **basic**: 실제 데이터를 이미 다 소화했고 심각 문제가 0건이다. 공지 99건과 갤러리 89건이 분리돼 있고, 개인 페이지 45개와 연구 주제 페이지 5개가 있다. 원본 메뉴(Introduction/Research/People/Publication/Notice)를 그대로 이어서 교수님·학생에게 가장 익숙하다. 약점은 시각뿐이다(웹폰트 없음, 밋밋함). v01에서 웹폰트를 넣고 PI 이력을 정리하면 가장 안전한 공개안이 된다. 다른 시안이 선택 기능을 이식할 때 참조할 기준 구현이기도 하다.
3. **t8_globe**: 차별성과 연구 소재 연결이 가장 강하다. 지구본 점이 `research.regions` 실데이터에서 나오고, 연구 페이지까지 미니 지구본이 이어진다. 합계는 t2보다 1점 낮지만, v02 확장(연구 영역 다각형, 논문 시간 슬라이더, 활동 지도)의 잠재력이 9종 중 가장 크다. 다만 다크 고정이 공식 홈페이지로 부담인지 교수님께 확인해야 하고, 1차 지적 4건이 남아 있어 v01 작업량이 t7보다 많다.
- **차점 t2_minimal(21점)**: 타이포 완성도와 논문 페이지는 9종 중 최고이고 모바일 뉴스도 압축돼 있다. 기후 소재와 연결된 장치가 없어 3위에서 밀렸다. 다크 고정이 부담이면 t8 대신 t2를 3위로 올린다.
- 이하: t4(20점, 실데이터 대시보드지만 다크 고정·구성원 카드가 약점) > t5(20점, 소개문 누락, 커버 그림 품질에 의존) > t3(19점, 고유 그래픽이 사라짐) > t1(18점, basic과 겹침) > t6(18점, PI 개인 홈 성격).
- 추천 3종은 성격이 서로 다르다(정보형 t7 / 원본 계승형 basic / 인상형 t8). 그래서 교수님이 방향을 고르기 쉽다. 어느 것을 골라도 3절 공통 권고 ①~④를 먼저 적용하고, 선택 기능(갤러리 분리, 구성원 개인 페이지)은 basic 구현을 가져다 쓴다.

### 1-4. 1차 리뷰(`visual_review.md`) 지적 처리 현황

| 1차 항목 | 상태 |
|---|---|
| 심각 1·2 basic 국문 줄바꿈, 모바일 헤더 | **해결**(`style.css:13` keep-all, `:53-58` 헤더 69px, 버튼 66×44) |
| 심각 3 t5 영문 홈 커버(저해상도·한글 자막) | **부분 해결**: 해상도는 1280×720이 됐다. 한글 자막과 파란 테두리는 남아서 보통으로 내렸다(공통 콘텐츠 문제, 3-2절) |
| 경미 6 유튜브 썸네일 해상도 | **해결**: `static/videos` 15장 중 14장이 1280×720. 남은 1장(`n8xFW4A_Oc8.jpg`)은 640×480 |
| 경미 4·7·16 t4 모바일 논문 그리드, placeholder 잘림, 브레드크럼 slug | 남음 |
| 경미 5 한글 라벨 자간(t1·t5·t8, t4 모노) | 남음(basic `.eyebrow`, t7도 같은 문제를 새로 확인) |
| 경미 8 t2 그리드선 겹침 / 9·10 t7 고정 영역·형광펜 / 11 t8 가장자리 마커 / 12 t1 연도 칩 표시 | 모두 남음 |
| 경미 13 터치 영역 | basic만 해결. t1 37px, t4 36px, t5 35px 남음. t8 40px, t2 폭 26px는 새로 확인 |
| 경미 14 국문 화면 영문 잔존(t4 "SNU / SEES", t8 "CSL · SNU") | 남음 |
| 경미 15 글자 간격 불균일 | 미확인(DPR1 캡처에서는 재현 안 됨. 실기기 확인 필요) |
| 경미 17 t3 모바일 히어로 여백 | 남음 |
| 경미 18 t6 배지 2줄, PI 중심 홈 | 남음(실제 사진·약력이 들어가 PI 중심 인상은 더 강해짐) |
| 경미 19 basic 연구 카드 말줄임 / 뉴스 상세 공백 | 말줄임은 해결, 오른쪽 공백은 남음 |

---

## 2. 테마별 검토

각 절의 "문제" 표에서 `(공통)`이 붙은 행은 3절에서 한꺼번에 푸는 것이 낫다.

### basic — Basic
**점수**: 데이터 4 / 구조 5 / 시각 3 / 모바일 4 / 콘셉트 2 / 접근성·유지보수 4
- 데이터 4: 공지 99건과 앨범 89건이 분리됐고 둘 다 연도 칩과 연도 섹션이 있다. 구성원 45명 개인 페이지와 발표 0건 안내문도 있다. 감점은 갤러리 모바일이 1열이라 36,930px라는 점이다.
- 구조 5: 원본 Introduction/Research/People/Publication/Notice 드롭다운을 그대로 따랐다. 연구 5주제, 구성원, 갤러리 상세에 메뉴 한 번으로 닿는다. PI 이력 과밀은 9종 공통이라 상대 점수에서 빼지 않았다.
- 시각 3: 깔끔하고 일관되지만 웹폰트가 없어 Arial 계열 대체 글꼴로 보인다. 뉴스 행 정렬이 들쭉날쭉하고 홈 영상 격자에 빈칸이 생긴다.
- 모바일 4: 헤더는 69px 1단 고정, 메뉴 버튼은 66×44px, 가로 넘침은 0이다. 감점은 논문 연도 칩 5줄과 갤러리 1열이다.
- 콘셉트 2: 의도적인 "원본 구조 계승형" 기준선이다. 시각적 차별성은 거의 없다.
- 접근성·유지보수 4: CSS 17.5KB(235행)로 가장 가볍고 공통 매크로를 최대한 쓴다. 드롭다운은 `:focus-within`으로 키보드 접근이 된다. 감점은 `:focus-visible` 전용 스타일 없음, 연도 칩 높이 약 24px, "Welcome" 하드코딩이다.

**강점**
- 원본 메뉴 드롭다운을 그대로 살렸고 선택 기능 4종(about, gallery, member, research_topic)을 모두 쓴다. 공지 99건과 갤러리 89건이 분리되고 둘 다 연도 칩과 연도 섹션이 있다(`themes/basic/templates/news.html:6-24`, `gallery.html:6-24`).
- 개인 페이지 45개에 참여 논문이 자동으로 붙는다(`basic_people-yechul-shin_full.png`: "Publications in the lab list (12)"). 연구 주제 페이지 5개에는 Research Themes, 그림 2~3장, 핵심 논문, 관련 영상, 이전/다음 링크가 있다(`basic_research-mechanism_full.png`).
- 1차 심각 2건이 모두 고쳐졌다.

**문제**
| 심각도 | 문제 | 캡처·위치 | 원인(파일:행/선택자) |
|---|---|---|---|
| 보통(공통) | 구성원 페이지의 첫 3,066px(전체 5,313px)를 PI의 학력·경력 14행·봉사·수상 18행·학회·대표 논문이 차지한다. 연구원·학생 카드는 그 아래에서 시작하고, 모바일에서는 6,081px부터 나온다. | `basic_people_full.png` y≈140–3,000, `basic_people_ko_mobile.png` | `templates/people.html:8-31`(PI 전체 CV 직접 출력). member.html이 있지만 PI는 개인 페이지 대상이 아니다 |
| 경미 | 웹폰트를 불러오지 않는다. 영문은 Arial/Helvetica 계열, 국문은 OS 글꼴로 보인다(9종 중 basic만). | `basic.png`, `basic_news.png` | `templates/base.html:8-11`에 폰트 `<link>` 없음, `style.css:5` |
| 경미 | 모바일 논문 페이지에서 연도 칩 27개가 5줄(약 330px)로 쌓여 검색창이 첫 화면 중간에 온다. 칩 높이는 약 24px다. | `basic_publications_mobile.png` | `templates/publications.html:5-6`(연도 → 검색 순), `style.css:178-179` `.pub-years a{padding:2px 8px}` |
| 경미 | 국문 화면에 영문 "Welcome", "YouTube"가 남아 있다. 국문 키커는 자간 .1em으로 벌어진다. | `basic_ko_dark.png` 히어로 키커 | `templates/index.html:31,65`, `about.html:9` 하드코딩, `style.css:83` `.eyebrow{letter-spacing:.1em}`, `:24` `.crumb`(`:lang(ko)` 보정 없음) |
| 경미 | 공지 목록에서 썸네일 있는 행과 없는 행의 글자 시작 위치가 달라 세로 정렬이 들쭉날쭉하다. | `basic_news.png` 3~5번째 행 | `style.css:148` `.news-row--text{grid-template-columns:1fr}` |
| 경미 | 홈 YouTube 영상 3개가 4칸 격자에 들어가 한 칸이 빈다. 영상 제목(국문)이 영문 페이지에서 어절 중간에 끊긴다("탄소/를"). | `basic_full.png` y≈2,620–2,830 | `style.css:74` `.grid-3{repeat(auto-fill,minmax(260px,1fr))}`, `index.html:66` `videos[:3]`. 줄바꿈은 공통(`m.video_card`에 `lang` 없음) |
| 경미 | 뉴스 상세가 왼쪽 820px 단만 쓰고 오른쪽 약 400px가 빈다(1차 지적 남음). | `basic_news-2026-10-23-permafrost-soil-moisture_full.png` | `style.css:157` `.post{max-width:820px}` |
| 경미 | 갤러리 모바일이 1열이라 앨범 89개가 36,930px까지 이어진다. | `basic_gallery_full_mobile.png` | `style.css:149` `.albums{minmax(250px,1fr)}` |
| 경미 | 소개 페이지 통계 "2000– / Years"(국문 "2000– / 연도")의 뜻이 바로 읽히지 않는다. | `basic_about_full.png` 통계 2번째 칸 | `templates/about.html:16` |

**1차 리뷰 지적 상태**: 국문 줄바꿈 해결 / 모바일 헤더 붕괴 해결 / Menu 버튼 28px 해결(66×44) / 고정 헤더 93px 해결(69px) / 연구 카드 말줄임 해결 / 논문 모바일 연도 칩 5줄 남음 / 뉴스 상세 오른쪽 공백 남음.

**v01 방향(정제판)**
- 구성원: `people.html:8-31`의 PI 섹션을 요약 카드(사진·직함·연락처·소개·관심 분야 칩)로 줄인다. 학력·경력·봉사·수상·학회·대표 논문은 PI 개인 페이지(member.html 재사용, 3-1절 ④)로 옮기거나 `<details>`로 접는다. people 상단에 역할 점프 탭(Professor·Researchers·Students·Alumni)을 둔다.
- 폰트: `base.html` `<head>`에 다른 테마와 같은 Pretendard dynamic-subset CSS를 넣는다.
- 국문: `:lang(ko) :is(.eyebrow,.crumb,.menu-top){letter-spacing:0}`. "Welcome"/"YouTube"는 `t()` 키로 바꾼다.
- 논문: 검색 → 연도 순서로 바꾸고, ≤600px에서는 `.pub-years`를 한 줄 가로 스크롤 + 오른쪽 페이드로 만든다. 칩 `min-height:32px` 이상.
- 공지 목록: 썸네일 없는 행에도 같은 폭의 빈 칸(카테고리 라벨)을 둬 정렬을 통일한다. 카테고리 필터 칩을 단다(3-1절 ②).
- 홈: `.grid-3`을 데스크톱에서 `repeat(3,1fr)`로 고정한다. 뉴스 상세는 `.post{margin-inline:auto}` 또는 오른쪽에 "관련 논문/최근 공지" 사이드를 둔다.
- 갤러리: 모바일 2열(`minmax(min(46%,250px),1fr)`).
- 접근성: `:focus-visible{outline:2px solid var(--accent-2);outline-offset:2px}`. 소개 통계는 "Since 2000"/"2000년부터"로 바꾼다.
- 선택 기능 판단
  - 구성원 개인 페이지: **유지**. 45명 모두 id·사진이 있고 학력은 43명분이 있다. pub_name 11명은 논문이 자동 연결된다. 학위·연도가 없는 졸업생 4명은 링크를 숨기는 조건을 검토한다.
  - 연구 주제 페이지: **유지**. 주제당 그림 2~3장, 핵심 논문 1~3편, 영상 1~3편, themes 4~7개로 한 페이지를 채울 만하다.
  - 갤러리 분리: **반드시 유지**.
  - extra_pages(about, gallery): **둘 다 유지**. about은 원본 Introduction 메뉴의 실체다.

**v02 방향(확장판)**
- **공지 게시판 분류·검색**: 공지 99건에 카테고리 탭과 제목 검색을 단다(논문 검색 JS 패턴 재사용, 행에 `data-search`). 데이터 `news`(category·title·year), 추가 데이터 없음. 난이도 하.
- **개인 페이지 논문 연표와 연구실 내 공저자**: 구성원별 참여 논문을 연도 막대 SVG로 그리고, 같은 논문의 다른 구성원을 링크로 묶는다. 데이터 `pubs`, `members.pub_name`. 추가 데이터는 pub_name이 없는 11명분. 난이도 중.
- **연구 주제 페이지 지역 지도와 주제별 전체 논문**: `research.regions`를 경위도 격자 SVG에 찍고(엘니뇨 = 열대 태평양, 북극 등), 핵심 논문 1~3편을 주제별 전체 목록으로 넓힌다. 추가 데이터는 논문별 주제 태그(`publications.yaml`의 `topics:`). 난이도 중.
- **원본 사이트 글 찾기**: 뉴스 front matter의 원본 게시판 번호(`source`)로 "이전 사이트 글 → 새 주소" 표를 만든다. 원본 메뉴에 익숙한 사용자를 위한 연속성 장치다. 난이도 하~중.

### t1_classic — Classic Academic
**점수**: 데이터 2 / 구조 3 / 시각 4 / 모바일 3 / 콘셉트 3 / 접근성·유지보수 3
- 데이터 2: 뉴스 188행이 연도 묶음·필터 없이 이어진다. 모바일은 75,891px로 9종 중 가장 길다. 79행은 같은 "CSL" 등압선 대체 그림이다. 졸업생 사진, 연구 figures·themes를 쓰지 않는다.
- 구조 3: 8개 평면 메뉴에 헤더 논문 검색이 있다. 원본의 Introduction·Gallery에 해당하는 곳이 없고, 0건인 발표가 최상위 메뉴에 있다.
- 시각 4: 유틸리티 바·세리프 마스트헤드·등압선 배너·네이비 푸터가 일관되고 다크도 안정적이다. 감점은 국문 라벨 자간, 220px 연구 그림, 들쭉날쭉한 구성원 카드다.
- 모바일 3: 헤더는 고정이 아니라 무난하다. 감점은 뉴스 항목마다 전체 폭 16:9 썸네일(항목당 약 400px), 메뉴 버튼 37px, 연도 칩 잘림 표시 없음이다.
- 콘셉트 3: 전통 대학 연구실 원형에 충실하고 등압선 모티프가 좋다. 다만 남색 대학 톤이 basic과 겹친다.
- 접근성·유지보수 3: `:focus-visible` 3px(`style.css:28`), 스킵 링크, 대비는 양호하다. 감점은 메뉴 버튼 37px, 유틸리티 링크 약 20px, 하드코딩 6곳이다.

**강점**
- 대학 공식 사이트 문법을 잘 지켰다. 서울대·학부 링크 유틸리티 바 → 세리프 연구실명(국문 병기) → 가로 메뉴 → 등압선 배너 → 4단 네이비 푸터(`t1_classic.png`, `t1_classic_full.png`).
- 헤더 검색창이 `publications.html?q=`로 연결돼 논문 필터가 실제로 동작한다(`templates/base.html:48-52`). 연구 페이지에는 sticky 사이드 목차, 논문 페이지에는 사이드 연도 그리드가 있다.
- 홈 흐름이 연구실 사이트에 맞다. 소개 → 연구 5주제 → PI 카드 → 뉴스 + 최근 논문 → 영상 → 대학원생 모집(`templates/index.html:19-95`).

**문제**
| 심각도 | 문제 | 캡처·위치 | 원인(파일:행/선택자) |
|---|---|---|---|
| 심각(공통) | 뉴스 188건(앨범 89 포함)이 연도 묶음·필터·페이지 나눔 없이 한 목록이다. 데스크톱 37,485px, 모바일 75,891px이다. 모바일은 항목마다 전체 폭 16:9 썸네일이 붙는다. "Skiing on an experts-only slope" 같은 앨범 글이 공지 사이에 섞인다. | `t1_classic_news.png`, `t1_classic_news_mobile.png` | `templates/news.html:8-25` 단일 루프, `style.css:270` `.news-row-link{250px 1fr}`, `:374`(680px 이하 1열·썸네일 전체 폭), `gallery.html` 없음 |
| 보통 | 국문 라벨에 영문 대문자용 자간이 그대로 붙어 "서 울 대 학 교 지 구 환 경 과 학 부", "연 구 책 임 자"처럼 벌어진다. | `t1_classic_ko_dark.png` 마스트헤드 위·배너 키커·PI 카드 머리 | `style.css:55` `.brand-aff` .06em, `:127` `.banner-kicker` .14em, `:145` `.pi-card-head`, `:210` `.side-h`, `:225` `.topic-num`, `:295` `.news-paper-label`, `:321` `.ftr-h` |
| 보통 | 연구 페이지 대표 그림(축·범례가 있는 논문 그림)이 220px 칸에 들어가 읽을 수 없다. 확대 링크도 없고, figures 2~3장과 themes는 나오지 않는다. | `t1_classic_research_full.png` 각 주제 왼쪽 위 | `style.css:223` `.topic-head{grid-template-columns:220px 1fr}`, `templates/research.html:19-21`(r.image만 사용) |
| 보통(공통) | 구성원 목록이 PI 이력 뒤 2,488px(모바일 4,027px)에서 시작한다. | `t1_classic_people_full.png` | `templates/people.html` PI CV 전체 출력 |
| 경미 | 발표 0건인데 최상위 메뉴 "Presentations"가 빈 페이지로 이어진다(안내문은 있음). | `t1_classic_presentations.png` | `data/site.yaml:54` nav 고정(공통) |
| 경미 | 졸업생 23명이 사진 없이 텍스트로만 나온다. 구성원 카드는 사진 64px이고 관심 분야 줄 수 제한이 없어 높이가 크게 다르다. | `t1_classic_people_full.png` 하단 | `m.alumni_list`(공통), `style.css:247` `.member-photo{width:64px}`, `:253` `.member-interests` |
| 경미 | 앨범 글 상세에서 cover(단체 사진)가 크게 나오고 아래 갤러리에 같은 사진이 또 나온다. | `t1_classic_news-2025-02-24-snu-kopri-high-latitude-workshop_full.png` | `news_post.html:18` `{% if post.cover and not post.youtube %}`(`not post.gallery` 없음, 공통) |
| 경미 | 썸네일 없는 79행이 모두 같은 남색 "CSL" 등압선 블록이다. | 뉴스 목록 2021년 이전 구간 | `templates/news.html:13` `x.iso_art(...)` |
| 경미 | 모바일 메뉴 버튼 높이 37px. 논문 모바일 YEARS 칩이 "20…"에서 잘리는데 스크롤 표시가 없다. | `t1_classic_mobile.png`, `t1_classic_publications_mobile.png` | `style.css:65-66` `.nav-btn{padding:9px 12px}`, `:352` `.side-years .pub-years` |
| 경미 | 첫 화면에 소속 "School of Earth and Environmental Sciences"가 세 번 반복된다. | `t1_classic.png` y≈18, 69, 498 | `templates/base.html:19,43`, `index.html:10` `.banner-aff` |
| 경미 | 화면 문구 하드코딩 6곳(학부명, "About the Laboratory", "Years", "Breadcrumb"). | — | `templates/base.html:19,67,104`, `index.html:23`, `publications.html:9`, `news_post.html:7` |

**1차 리뷰 지적 상태**: 모바일 YEARS 칩 표시 없음 남음 / 한글 라벨 자간 남음(실데이터 화면에서 눈에 띄어 보통으로 올림) / Menu 버튼 37px 남음 / 썸네일 해상도 해결.

**v01 방향(정제판)**
- 뉴스: `news.html`을 `with-side` 레이아웃으로 바꾼다. 왼쪽 sticky에는 연도 그리드(`.side-years` 재사용)와 카테고리 링크, 본문에는 연도 섹션을 둔다. 썸네일은 데스크톱 200px, 모바일 96px 가로형으로 줄이고 썸네일 없는 행은 iso_art 대신 텍스트 행으로 바꾼다.
- 갤러리: `extra_pages: [gallery]` + `templates/gallery.html`(등압선 프레임 + 금색 하단선 카드 4열, 연도별)을 둔다.
- 국문 자간: `html:lang(ko) :is(.brand-aff,.banner-kicker,.pi-card-head,.side-h,.topic-num,.news-paper-label,.ftr-h){letter-spacing:.01em}`(t2 `style.css:474` 방식).
- 연구: 그림 칸을 220px에서 360px 이상으로 넓히고 클릭 확대를 단다. 아니면 연구 주제 페이지로 넘긴다(아래).
- 구성원: 졸업생을 사진 카드로 바꾸고(공통 매크로 옵션), `.member-interests{-webkit-line-clamp:3}`, `.member-card{align-items:flex-start}`, 사진은 80px로 키운다.
- 앨범 상세 cover 중복, 메뉴 버튼 44px, 유틸리티 링크 `padding-block:8px`, 연도 칩 페이드, `.banner-aff`를 한 줄 소개로 교체, 하드코딩 → `t()`.
- 선택 기능 판단
  - 갤러리 분리: **사용**. 앨범 89편이라 필수다.
  - 연구 주제 페이지: **사용**. 지금은 그림 1장만 220px로 보여 figures 13장이 버려진다. research.html은 개요 + 사이드 목차로 두고 상세는 `research/<key>.html`로 뺀다.
  - 구성원 개인 페이지: **v01에서는 보류**. 학생 22명은 관심 분야 16명, pub_name 11명으로 데이터 편차가 크다. PI 이력 정리(3-1절 ④)에 PI 개인 페이지만 쓴다.
  - extra_pages: gallery만. 홈 "About the Laboratory"가 Introduction 역할을 한다.

**v02 방향(확장판)**
- **연구실 연혁(History) 페이지**: 2000→2026 연표에 연도별 논문 수 막대, PI 경력, 수상, 졸업생 배출, 주요 논문 뉴스를 겹친다. 데이터 `stats.per_year`, `pi.career/awards`, `alumni`(year·degree), `news`(paper/award). 추가 데이터는 선택적 milestones(POSTECH→SNU 2024 등). 난이도 중.
- **연도별 연차보고 아카이브**: 연도를 고르면 그해 논문·소식·영상·졸업생이 한 화면에 모인다. 데이터 `pubs_by_year`, `news`, `videos`, `alumni`, 추가 데이터 없음. 연도별 페이지 생성은 빌드 지원이 필요하다(한 페이지 + 앵커로도 가능). 난이도 중.
- **등압선 배너를 실제 연구 결과로**: 장식 `isobars.svg` 대신 연구실 논문의 엘니뇨 합성 SLP 같은 등치선을 정적 SVG로 쓰고 출처 DOI 캡션을 단다. 추가 데이터는 오프라인으로 만든 SVG 1~3장. 난이도 중~상.
- **졸업생 진로 표**: 학위·졸업연도·현직을 공식 표로 정리하고 집계한다. 데이터 `alumni`, 추가 데이터는 현직 20명분. 난이도 하.

### t2_minimal — Modern Minimal
**점수**: 데이터 3 / 구조 3 / 시각 4 / 모바일 4 / 콘셉트 4 / 접근성·유지보수 3
- 데이터 3: 뉴스 188행 단일 목록이라 데스크톱 39,982px로 가장 길다. 하지만 모바일은 112px 썸네일 압축 행이라 41,234px로 8종 중 두 번째로 짧다. 감점은 홈 "04 Presentations" 빈 섹션, 79행 빈 격자 칸, 직함·졸업생 사진·연구 figures 미사용이다.
- 구조 3: 메뉴 01–07과 홈 섹션 번호가 1:1로 맞는다. 원본 Introduction·Gallery에 해당하는 곳이 없고 메뉴에 Home이 없으며(로고가 대신), 0건 발표가 메뉴와 홈 모두에 나온다.
- 시각 4: 흑백 + 주홍 한 색, 큰 글자 위계, 국문 자간 보정, 다크 모두 정돈됐다. 감점은 그리드선 겹침(1차 그대로), 약 210px 연구 그림이다.
- 모바일 4: 뉴스 압축 행, sticky 연도 띠, 큰 번호 메뉴가 좋다. 감점은 그리드선 겹침과 메뉴 버튼 폭 26px다.
- 콘셉트 4: 번호 체계가 메뉴·홈·하위 머리말·논문까지 일관되고 다른 시안과 겹치지 않는다. 연구실 소재(기후·지구)와 연결된 장치는 거의 없다.
- 접근성·유지보수 3: `:focus-visible`(`style.css:46`), reduced-motion이 있다. 감점은 메뉴 버튼 폭 26px, 하드코딩 8곳, 자체 매크로(ui.pub·news_row·mcard·alist·pres)를 써서 공통 매크로 개선이 반영되지 않는다는 점이다.

**강점**
- 9종 중 가장 뚜렷한 에디토리얼 타이포그래피다. 번호(01–07)가 메뉴, 홈 섹션 머리, 하위 페이지 머리말까지 한 체계로 이어진다(`templates/ui.html:4` `no()`). 국문 자간 보정(`style.css:130,136,266,404,474`)과 keep-all(`:36`)이 있다.
- 논문 페이지가 모범적이다. 밑줄형 대형 검색창 + "318 papers", 큰 연도 sticky 라벨, 모바일 sticky 연도 띠, `#318` 번호(`t2_minimal_publications.png`, `style.css:290-321`).
- 모바일 뉴스는 요약을 숨기고 썸네일 112px 2단 행으로 압축했다(`style.css:233-239`). 메뉴는 1.5rem 번호 목록이다.

**문제**
| 심각도 | 문제 | 캡처·위치 | 원인(파일:행/선택자) |
|---|---|---|---|
| 심각(공통) | 뉴스 188건(앨범 89 포함)이 연도 묶음·필터·페이지 나눔 없이 한 목록이다(데스크톱 39,982px). 썸네일 없는 79행은 빈 격자 칸에 카테고리 글자만 있다. | `t2_minimal_news.png`, 목록 16,000px 지점 | `templates/news.html:6-8` 단일 루프, `ui.html:78` `nrow-img--empty`, `style.css:228-231`, `gallery.html` 없음 |
| 보통 | 발표 0건인데 홈 번호 섹션 "04 Presentations"가 "Nothing here yet." 한 줄로 비어 있다. 발표 페이지도 발표 전용 안내(`pres.empty`)가 아니라 일반 문구다. | `t2_minimal_full.png` y≈2,900–3,250 | `templates/index.html:91-114`(조건 없이 출력), `presentations.html:26` `t('common.empty')` |
| 보통 | 연구 대표 그림이 본문 오른쪽 약 210px 칸에 들어가 판독할 수 없다. 요약문은 40ch 좁은 단에 20줄 안팎으로 늘어진다. | `t2_minimal_research_full.png` 각 주제 상단 | `style.css:338` `.topic-lede{1.25fr 1fr}`, `:339` `.topic-sum{max-width:40ch}`, `research.html:19-23` |
| 보통(공통) | 구성원 목록이 PI 이력 뒤 3,068px(모바일 4,098px)에서 시작한다. | `t2_minimal_people_full.png` | `templates/people.html` |
| 경미 | 장식 세로 그리드선이 히어로 헤드라인·소개문 위를 지나간다(모바일 x≈42·390). | `t2_minimal.png`, `t2_minimal_mobile.png` | `style.css:122-128` `.hero-grid`, `:13` `--gridline:.07` |
| 경미 | 모바일(≤480px) 메뉴 버튼이 라벨을 숨겨 폭이 26px다. | `t2_minimal_mobile.png` 오른쪽 위 | `style.css:89` `.nav-btn{padding:0 2px}`, `:112` |
| 경미 | 구성원 카드에 직함(position)이 없다. 사진 72px에 여백이 많고 졸업생은 텍스트 표다. | `t2_minimal_people_full.png` | `templates/people.html:55-61` `.mcard`, `:77-81` `.alist`, `style.css:197` |
| 경미 | 앨범 상세 cover 중복. | `t2_minimal_news-2025-02-24-…_full.png` | `news_post.html:13`(공통) |
| 경미 | 영문 페이지의 국문 영상 제목이 어절 중간에서 끊긴다("깨웠/다."). 홈 통계 "News 188"에 앨범이 포함됐다. | `t2_minimal_full.png` 06 Videos, `t2_minimal.png` 통계 | `style.css:36` keep-all이 `lang(ko)`에만 있음, `index.html:13` `stats.news`(공통) |
| 경미 | 하드코딩 8곳. 자체 매크로라 교신저자 표시·member_url 같은 공통 개선이 자동 반영되지 않는다. | — | `base.html:17,61`, `news_post.html:20,21,34`, `research.html:22`, `publications.html:11,20`, `ui.html:36-49,68-80` |

**1차 리뷰 지적 상태**: 그리드선 겹침 남음 / 메뉴에 Home 없음은 의도로 판단(로고 `aria-current`) / 논문 모바일 연도 링크 5줄 허용 범위 / 국문 보정 유지.

**v01 방향(정제판)**
- 뉴스: 논문 페이지의 `.yr` 2단 패턴(왼쪽 sticky 큰 연도, 오른쪽 목록)을 `news.html`에 그대로 쓰고, 연도 링크 줄과 카테고리 텍스트 필터를 둔다. 썸네일 없는 행은 빈 격자 칸을 빼고 텍스트 행으로 바꾼다.
- 갤러리: `extra_pages: [gallery]` + 흑백 4열 사진 격자(연도 sticky, 앨범 번호). 통계는 News 99 / Albums 89로 나눈다.
- 발표 0건: 비어 있으면 홈 04 섹션과 메뉴 항목을 숨기고 `ui.no()` 번호를 다시 매긴다. 발표 페이지 문구는 `t('pres.empty')`.
- 그리드선: `.hero-grid`를 히어로 상단에만 보이게 `mask-image`로 처리하거나 `--gridline`을 .04로 낮추고 ≤560px에서 숨긴다.
- 연구: `.topic-lede`를 1열로 바꿔 그림을 본문 폭(최대 760px)으로 키우고, `.topic-sum`은 60ch로 넓힌다. 또는 연구 주제 페이지로 넘긴다.
- 구성원: `.mcard`에 `tr(mm.position)`을 출력하고 사진을 96px로 키운다. 졸업생은 48px 흑백 사진 + 이름·학위·연도.
- `.nav-btn{min-width:44px}`, 앨범 상세 cover 중복 수정. 자체 `ui.pub`은 `m.pub_item` + CSS 오버라이드로 바꾸고, 하드코딩은 `t()`로 옮긴다.
- 선택 기능 판단
  - 갤러리 분리: **사용**. 흑백 사진 격자가 콘셉트와도 맞는다.
  - 연구 주제 페이지: **사용**. 지금의 sticky 제목 + 장문 구조가 이미 상세 페이지 문법이다. figures 13장과 themes에 지면을 준다.
  - 구성원 개인 페이지: **안 씀**. 미니멀 콘셉트상 한 페이지 카드 격자로 충분하다.
  - extra_pages: gallery만.

**v02 방향(확장판)**
- **논문 연표 띠(Index strip)**: 히어로 통계 아래에 2000–2026 연도별 논문 수를 얇은 세로선 27개로 그린다. 최근 연도는 주홍, 누르면 그 해 앵커로 간다. 데이터 `stats.per_year`, 추가 데이터 없음. 난이도 하.
- **저널 인덱스 필터**: 논문 검색창 아래에 `stats.top_journals` 칩과 Featured·CA 토글을 둔다(기존 `data-pub-search` 확장). 난이도 하~중.
- **연구 지역 격자 지도**: 이미 있는 `ui.geo` 매크로(30° 격자 + 점)를 그림과 함께 쓴다. 5주제 regions를 번호(01–05)로 겹쳐 홈 01 섹션 옆에 둔다. 추가 데이터는 저해상도 해안선 path 1개(선택). 난이도 하.
- **논문 ↔ 영상 2단 목록**: 영상 페이지를 왼쪽 서지, 오른쪽 클릭형 영상의 에디토리얼 행으로 짠다. 데이터 `videos[].pub`, 추가 데이터는 DOI 없는 영상의 수동 매핑. 난이도 하.

### t3_ocean — Ocean–Atmosphere
**점수**: 데이터 3 / 구조 3 / 시각 4 / 모바일 3 / 콘셉트 3 / 접근성·유지보수 3
- 데이터 3: 논문 318편과 구성원 사진은 잘 나온다. 뉴스 79건이 같은 물결 플레이스홀더이고, 구성원 직위가 빠졌으며, 졸업생 사진은 쓰지 않는다.
- 구조 3: 메뉴는 표준이고 홈 intro에 소개문과 PI 카드가 있다. 다만 홈 첫 화면이 100svh 히어로뿐이고 뉴스 필터가 없다. people 점프 탭은 좋다.
- 시각 4: 라이트(하늘빛)·다크(심해)·국문 모두 일관된다.
- 모바일 3: 메뉴 버튼 44×44, 논문 연도 띠는 괜찮다. 뉴스 목록이 67,315px이고 히어로 위아래 여백이 1차 그대로다.
- 콘셉트 3: SST 팔레트와 등온선 히어로는 일관된다. 그러나 고유 그래픽 `o.topic_art`(위경도 미니맵 + regions)가 5주제 모두 `r.image`가 있어 한 번도 나오지 않는다. 남은 것은 흔한 "그라데이션 + glass 카드"다.
- 접근성·유지보수 3: `:focus-visible`(ocean.css:71), reduced-motion, 터치 44px이 있다. 공통 `m.member_card`를 복제한 자체 매크로가 직위와 `member_url`을 빠뜨렸다. CSS 37.8KB.

**강점**
- 히어로·서브 히어로·푸터 물결이 한 팔레트로 이어진다. 다크·국문 히어로(`t3_ocean_ko_dark.png`)도 무리가 없다.
- 연구 페이지에서 주제별로 원본 그림 + 본문 + Key papers(번호·CA·Featured 배지) + 관련 영상이 한 카드에 정리돼 있다(`t3_ocean_research_full.png`).
- 논문 페이지에 데스크톱 sticky 연도 3열 사이드바, 모바일 가로 연도 띠, people 페이지에 역할 점프 탭이 있다.

**문제**
| 심각도 | 문제 | 캡처·위치 | 원인(파일:행/선택자) |
|---|---|---|---|
| 심각(공통) | 뉴스 188건(앨범 89 포함)을 카드 한 격자에 다 넣는다. 79건은 같은 물결 플레이스홀더다. 데스크톱 24,824px, 모바일 67,315px. | `t3_ocean_news.png`, `t3_ocean_news_mobile.png` | `templates/news.html:23` `news[1:]` 전체, `_shared/macros.html:73` `news-card-img--empty` + `ocean.css:310`, `gallery.html` 없음 |
| 보통 | 구성원 카드에 직위가 없다(Research Professor·Postdoctoral Fellow 구분이 사라짐). | `t3_ocean_people_full.png` Researchers | 자체 `o.member_card`(`_ocean.html:98-107`)가 `mm.position`·`member_url()` 누락(빌드 HTML `member-position` 0건) |
| 보통 | 고유 연구 그래픽(SST 미니맵 + regions)이 실데이터에서 한 번도 나오지 않는다. | `t3_ocean_full.png`, `t3_ocean_research_full.png` | `_ocean.html:54` `{% if r.image %}` 분기 |
| 보통 | 홈 첫 화면이 100svh 히어로뿐이다. 모바일은 위 약 185px, 아래 약 130px가 빈다. | `t3_ocean_mobile.png`, `t3_ocean.png` | `ocean.css:175` `.hero{min-height:100svh}`, `:176` `.hero-in` padding |
| 보통(공통) | 구성원 목록이 PI 이력 뒤 3,454px(모바일 5,426px)에서 시작한다(점프 탭이 있어 영향은 작음). | `t3_ocean_people_full.png` | `templates/people.html` |
| 경미 | 앨범 상세 cover 중복. | `t3_ocean_news-2025-02-24-…_full.png` | `news_post.html:11`(공통) |
| 경미 | PI 학력·경력·봉사 3단 패널 높이 차가 커서(3건 대 15건) 아래가 빈다. | `t3_ocean_people_full.png` 상단 | `ocean.css:437` `.cv-grid` |
| 경미 | 떠 있는 고정 헤더(top 12px, 약 64px, 불투명도 .74)가 스크롤 내내 본문 카드를 덮는다. | contact·people 스크롤 중 | `ocean.css:99` `.hdr{position:fixed;top:12px}` |
| 경미 | 졸업생 사진 미사용, 하드코딩('Scroll down', 'Skip to content', 'Links'). | — | `people.html:58`, `index.html:22`, `base.html:15,65` |

**1차 리뷰 지적 상태**: 모바일 히어로 여백 남음 / 썸네일 해상도 해결 / 글자 간격 불균일 미확인 / "결함 거의 없음" 판정은 실데이터에서 뉴스·직위 문제가 드러나 **악화**.

**v01 방향(정제판)**
- 뉴스: 상위 1건 리드 + 연도별 섹션 + 카테고리 칩으로 바꾼다. 표지 없는 카드는 이미지 영역 없는 작은 텍스트 카드로 줄인다.
- 구성원: `o.member_card`를 지우고 `m.member_card(mm, 'member-card glass')`를 쓴다. `.member-position` 스타일을 추가한다.
- 히어로: 홈 `.hero{min-height:min(100svh,760px)}`. 모바일은 `min-height:auto`로 intro 첫 줄이 첫 화면에 걸치게 한다.
- 연구 그래픽: `topic_art`를 그림 대체용이 아니라 연구 카드 위 얇은 띠(위도 그라데이션 + regions 지점)로 항상 보여 준다.
- `.cv-grid`를 2열로 재배치하고, 앨범 cover 중복을 고친다.
- 선택 기능 판단
  - 갤러리 분리: **사용**. glass 카드 격자가 사진 앨범과 잘 맞는다.
  - 구성원 개인 페이지: **사용**. 22명 모두 id·사진이 있고, pub_name 기반 참여 논문 연결의 가치가 크다.
  - 연구 주제 페이지: **보류**. 지금 research 한 페이지 카드로 충분하다. figures는 카드 안 슬라이드로 넣는다.
  - extra_pages: about 하나(원본 Introduction용, 짧게).

**v02 방향(확장판)**
- **SST 아노말리 히어로**: 히어로 색을 실제 Niño3.4 월별 아노말리(최근 24개월) 띠로 그리고, 마우스를 올리면 그 달 값을 보여 준다. 추가 데이터는 NOAA ONI/Niño3.4 CSV를 빌드 때 `assets/data/nino34.js`로 변환(t4 `gistemp_to_js.py`와 같은 방식). 난이도 중.
- **연구 지역 해도(海圖)**: 연구 페이지 머리에 세계 해도를 두고 `research.regions` 12지점을 주제 색 핑으로 찍는다. 누르면 해당 주제 카드로 간다. 놀고 있는 `topic_art` 코드를 재사용한다. 추가 데이터 없음. 난이도 하.
- **논문 해류 타임라인**: `stats.per_year`를 물결 높이로 그린 파형(2000→2026)을 논문 페이지 상단에 둔다. 마루를 누르면 해당 연도로 간다. 난이도 하~중.
- **영상·논문 쌍 카드**: `v.pub`로 이미 연결된 영상을 "영상으로 보는 논문" 줄로 묶는다. 난이도 하.

### t4_dashboard — Climate Dashboard
**점수**: 데이터 3 / 구조 4 / 시각 3 / 모바일 3 / 콘셉트 4 / 접근성·유지보수 3
- 데이터 3: KPI 7개, 연도별 막대, 상위 학술지, 주제별 논문·영상 수가 모두 실데이터다. 감점은 뉴스 79건 점무늬 빈 칸과 데스크톱 구성원 카드에서 이름·이메일이 끊기는 문제다.
- 구조 4: 홈 한 화면에 개요·PI·지표·연구·최신 피드·논문·뉴스·영상이 모여 있어 핵심 정보에 가장 빨리 닿는 축이다.
- 시각 3: 다크 패널·모노 수치·stripes가 일관된다. 감점은 국문 모노 라벨 간격, 다크 위 흰 원본 그림, 구성원 카드 높이 차이다.
- 모바일 3: 논문 첫 화면을 연도 그리드 9×3이 다 차지하고, 메뉴 버튼 40×36, 뉴스 63,365px. 1차 지적이 모두 남았다.
- 콘셉트 4: 실제 GISTEMP warming stripes + 연구실 실적 대시보드로 차별성이 분명하다. 다크 고정과 `csl://` 장식은 호불호가 갈린다.
- 접근성·유지보수 3: `:focus-visible`, reduced-motion이 있다. 감점은 메뉴 버튼 36px, 템플릿 안 `'..' if en else '..'` 하드코딩 22곳, 국문 화면 "SNU / SEES"다.

**강점**
- 홈이 "연구실 현황판" 역할을 한다. 논문 318·활동 27년·연구 5분야/12지역·영상 15·학술지 45·구성원 22가 각 페이지로 바로 이어진다(`t4_dashboard_full.png`).
- 연구 페이지가 주제마다 원본 그림, 논문·영상 수, 지역 좌표, 대표 논문, 관련 영상을 패널로 정리한다. 정보 밀도가 가장 높다.
- warming stripes가 장식이 아니라 실데이터(`assets/data/gistemp.js`, 1880–2025, 출처 표기)다.

**문제**
| 심각도 | 문제 | 캡처·위치 | 원인(파일:행/선택자) |
|---|---|---|---|
| 심각(공통) | 뉴스 188건(앨범 89 포함)이 3열 카드 한 격자에 다 나온다. 79건은 점무늬 빈 칸이다. 데스크톱 24,011px, 모바일 63,365px. | `t4_dashboard_news.png`, `t4_dashboard_news_mobile.png` | `templates/news.html:4`, `style.css:300` `.news-card-img--empty`, `gallery.html` 없음 |
| 보통 | 데스크톱 구성원 카드가 240px 최소폭 5열이라 글 칸이 약 130px다. 이름이 감기고("Manuel Tobias / Blau") 이메일이 중간에서 끊긴다("…@snu.ac.k / r"). 행 높이가 약 230~455px로 들쭉날쭉하다. | `t4_dashboard_people_full.png` Postdoc·Researchers | `style.css:119` `.grid-4{minmax(min(100%,240px),1fr)}`, `:365` `.member-card{align-items:center}`, `:373` `.member-email{overflow-wrap:anywhere}`, `.member-position` 규칙 없음 |
| 보통 | 모바일 논문 첫 화면을 연도 그리드 27칸(9행×3열)이 다 차지하고 검색창은 첫 화면 아래에 있다. | `t4_dashboard_publications_mobile.png` | `publications.html:11-21` aside가 목록 앞, `style.css:248` `.year-bars` |
| 보통 | 국문 화면에서 모노 라벨이 한글 대체 글꼴로 나와 간격이 벌어진다("최종  수정", "교수  연구실"). 상단 "SNU / SEES"는 영문 그대로다. | `t4_dashboard_ko.png`, `t4_dashboard_people_ko_mobile.png` | `style.css:28` `.mono`, `:144` `.kv li span`, `base.html:20` |
| 보통(공통) | 구성원 목록이 PI 이력 뒤 2,138px(모바일 3,843px)에서 시작하고, 학력 패널(3건) 옆에 약 750px 빈 패널이 생긴다. | `t4_dashboard_people_full.png` | `people.html:25-31` `span-6`+`span-6` |
| 경미 | 뉴스 상세 브레드크럼에 slug 원문이 나온다. | `t4_dashboard_news-2025-02-24-…_full.png` | `news_post.html:4` `{{ post.slug }}` |
| 경미 | 모바일 검색 placeholder가 "Search title, author, ⁝"에서 잘린다. | `t4_dashboard_publications_mobile.png` | `style.css:226` `.pub-search` 모노 글꼴 |
| 경미 | 메뉴 버튼 40×36px, "SNU"/"SEES" 링크 22×19px. | 모바일 우상단 | `style.css:59` `.nav-btn{min-height:36px}`, `base.html:20` |
| 경미 | 앨범 상세 cover 중복, 갤러리 행 높이가 들쭉날쭉하다. | `t4_dashboard_news-2025-02-24-…_full.png` | `news_post.html:8`(공통) |
| 경미 | 다크 화면 안의 흰 원본 그림이 1000px 흰 판으로 튄다. 홈 "PAP / VID" 약어가 바로 읽히지 않는다. | `t4_dashboard_research_full.png` | `research.html:20` `.topic-img`, `index.html:110` |

**1차 리뷰 지적 상태**: 모바일 논문 연도 그리드, placeholder 잘림, 브레드크럼 slug, 국문 모노 라벨, "SNU / SEES", 메뉴 36px, 모바일 로고 붙음 모두 **남음** / 썸네일 해상도 해결.

**v01 방향(정제판)**
- 뉴스: 연도별 묶음 + 카테고리 칩 필터로 바꾼다. 표지 없는 글은 대시보드식 로그 행(`날짜 | CAT | 제목`, 모노)으로 그려 점무늬 79칸을 없앤다.
- 구성원: `.grid-4`를 `minmax(min(100%,300px),1fr)`(1440px에서 4열)로 넓히고 `.member-card{align-items:flex-start}`로 바꾼다. `.member-position` 스타일을 추가하고, 이메일은 `@` 앞에서만 줄이 바뀌게 한다(공통 매크로 `<wbr>`).
- 모바일 논문: ≤900px에서 검색을 먼저, 연도는 한 줄 가로 스크롤로 바꾼다.
- 국문: `:lang(ko) :is(.kv li span,.kpi-label,.panel-t){font-family:var(--sans);letter-spacing:0;text-transform:none}`. "SNU / SEES"는 `t()` 키로 옮긴다.
- 브레드크럼은 `t('news.title')`, 모바일 placeholder는 짧은 키, `.nav-btn{min-height:44px}`. 연구 그림은 흰 액자(`padding:12px; border-radius:8px; max-height:420px; object-fit:contain`)로 감싼다. 하드코딩 22곳은 i18n으로 옮긴다.
- 선택 기능 판단
  - 갤러리 분리: **사용**. 갤러리는 "event log" 격자로 만든다.
  - 구성원 개인 페이지: **사용**. 개인 KPI(논문 수·첫 논문 연도·주요 학술지)가 대시보드 콘셉트와 맞는다.
  - 연구 주제 페이지: **조건부**. research.html이 이미 충실해 우선순위는 낮다. figures·themes를 보이려면 도입한다.
  - extra_pages: about 불필요(홈 OVERVIEW가 겸함).

**v02 방향(확장판)**
- **stripes ↔ 논문 연동 타임라인**: stripes의 연도에 마우스를 올리면 그해 기온 편차, 연구실 논문 수, 대표 논문 제목을 보여 주고, 클릭하면 `publications.html#y<연도>`로 간다. 데이터 `gistemp.js`, `stats.per_year`, `pubs_by_year`, 추가 데이터 없음. 난이도 중.
- **ENSO 상태 패널**: 최근 Niño3.4 아노말리 스파크라인과 현재 단계 배지를 두고 연구 주제 02와 엘니뇨 언론 뉴스로 연결한다. 추가 데이터는 NOAA ONI CSV → `assets/data/oni.js`(갱신은 스크립트). 난이도 중.
- **공저 네트워크 패널**: `pubs.authors`로 공저 빈도 상위 공저자 표와 연도별 "1저자 구성원 비율"을 그린다. 추가 데이터 없음(빌드 집계 함수만). 난이도 중.
- **연구 지역 레이더 맵**: `research.regions`를 다크 지도에 찍고 주제 필터와 연동한다. 추가 데이터는 해안선 SVG 1장. 난이도 하~중.

### t5_magazine — Science Magazine
**점수**: 데이터 3 / 구조 2 / 시각 4 / 모바일 4 / 콘셉트 4 / 접근성·유지보수 3
- 데이터 3: 논문 318편(세리프 연도 목록)과 PI 프로필은 훌륭하다. 감점은 뉴스 79건의 같은 타이포 표지, 한글 자막 영문 커버, 구성원 직위 스타일 없음이다.
- 구조 2: 연구실 소개문(`site.lab.intro`)이 사이트 어디에도 없다. 9종 중 유일하게 원본 Introduction에 해당하는 내용이 없다. 홈이 소식 중심이고 뉴스 필터도 없다.
- 시각 4: 마스트헤드, 세리프, 붉은 포인트, 드롭캡, 다크까지 타이포 완성도가 가장 높은 축이다. 감점은 국문 키커 자간과 뉴스 격자 세로선 오류다.
- 모바일 4: 뉴스 목록이 40% 썸네일 + 제목 행이라 31,244px로 8종 중 가장 짧다. 감점은 메뉴 버튼 35px, 연도 띠 표시 없음, PI 사진 머리 잘림이다.
- 콘셉트 4: 과학 잡지 편집형은 다른 시안과 겹치지 않는다. 다만 표지 그림 품질에 기대는 구조인데, 앨범을 빼면 남는 뉴스 99건 중 79건이 이미지가 없다.
- 접근성·유지보수 3: `:focus-visible`, reduced-motion이 있다. 감점은 메뉴 35px, 국문 자간 보정 부족, `news_post.html`이 `m.news_body`를 다시 구현해 갤러리 링크가 빠진 점이다.

**강점**
- 잡지 타이포그래피(Playfair 마스트헤드, 세리프 본문, 드롭캡, 붉은 키커)가 가장 세련됐고 국문·다크에서도 무너지지 않는다(`t5_magazine_ko_dark.png`).
- 모바일 뉴스 목록이 촘촘한 행이라 188건 규모에서도 가장 짧다(31,244px).
- PI 프로필이 큰 초상, 드롭캡 약력, 번호 붙은 관심사, 3단 이력으로 인물 기사처럼 짜여 있다(`t5_magazine_people_full.png`).

**문제**
| 심각도 | 문제 | 캡처·위치 | 원인(파일:행/선택자) |
|---|---|---|---|
| 심각 | 연구실 소개문이 사이트 어디에도 없다. 홈은 태그라인 한 줄 뒤에 바로 뉴스가 나온다. | `t5_magazine_full.png` 전체 | t5 템플릿 전체에서 `site.lab.intro` grep 0건(다른 8종은 index에 있음) |
| 심각(공통) | 뉴스 188건(앨범 89 포함)이 한 목록이다. 79건은 "Media"·"Event" 타이포 표지가 반복된다. 데스크톱 22,600px, 모바일 31,244px. | `t5_magazine_news.png`, `t5_magazine_news_mobile.png` | `news.html:9-13` `news[1:]` 전체, `_t5.html:34-39` `art()`, `gallery.html` 없음 |
| 보통(공통) | 영문 홈에서 가장 큰 요소(커버)가 한글 자막과 파란 테두리가 있는 유튜브 썸네일이다(해상도는 1280×720으로 개선됨). | `t5_magazine.png`, `t5_magazine_mobile.png` | 콘텐츠 `content/news/2026-10-23-permafrost-soil-moisture/cover.jpg`, `index.html:15` `x.story_img(news[0])` |
| 보통 | 구성원 카드의 직위가 스타일 없이 기본 p로 나와 이름보다 크다. 사진이 세로 가운데로 떠서 행마다 높이가 다르다. | `t5_magazine_people_full.png` | `.member-position` 규칙 없음, `style.css:305` `.member-card{align-items:center}` |
| 보통(공통) | 구성원 목록이 PI 이력 뒤 2,897px(모바일 4,491px)에서 시작한다. | `t5_magazine_people_full.png` | `templates/people.html` |
| 경미 | 뉴스 격자 2행부터 왼쪽 여백에 세로 구분선이 그려진다(행 첫 칸에도 적용). | news 목록 y≈1,350 아래 왼쪽 | `style.css:121` `.stories-3 > .story + .story::before{left:-24px}` |
| 경미 | 국문에 영문용 넓은 자간이 남아 있다("서울대학교 · CSL", "교수 · 기후 변화 및 예측"). 국문 약력에 한글 드롭캡("국")도 어색하다. | `t5_magazine_ko_dark.png`, `t5_magazine_people_ko_mobile.png` | `style.css:46` `.mast-over`, `:70` `.kicker`, `:85` `.phead-kicker`, `:286` `.profile-role`, `people.html:96` `prose--dropcap` |
| 경미 | 발표 0건 화면에 빈 연도 nav의 4px 검은 막대만 남는다. | `t5_magazine_presentations.png` x 128–298, y≈540 | `presentations.html:7` 빈 `nav.pub-years`, `style.css:242` |
| 경미 | 앨범 상세 갤러리 사진에 링크가 없어 크게 볼 수 없고, cover가 갤러리에 다시 나온다. | `t5_magazine_news-2025-02-24-…_full.png` | `news_post.html:41`(`<img>`만 출력) |
| 경미 | 메뉴 버튼 91×35px, 모바일 placeholder 잘림, 연도 띠 스크롤 표시 없음, 모바일 PI 사진 머리 잘림. | `t5_magazine_mobile.png`, `t5_magazine_publications_mobile.png` | `style.css:51-52`, `:247`, `:428`, `:430` `.profile-portrait{aspect-ratio:16/10}` |

**1차 리뷰 지적 상태**: 영문 홈 커버 부분 해결(흐림 해소, 한글 자막 남음 → 보통) / 국문 키커 자간 남음 / placeholder 잘림 남음 / 메뉴 36px 남음 / "20 26" 글자 간격 미확인 / 썸네일 해상도 해결.

**v01 방향(정제판)**
- 소개문: 마스트헤드 아래 "Editor's note" 형식으로 `tr(site.lab.intro)`를 세리프 리드 문단으로 넣고 PI 미니 바이라인(사진·이름·직함 → people)을 붙인다.
- 커버: `news[0]` 대신 "표지가 있고 category가 paper/award인 최신 글"을 고른다. 콘텐츠 쪽에서는 이 글의 cover를 한글 없는 논문 그림으로 바꾼다(3-2절).
- 뉴스: 연도별 섹션(큰 세리프 연도)으로 묶고 카테고리 칩을 둔다. 표지 없는 글은 `story--sm` 텍스트 행으로 그린다.
- `style.css:121`을 `.stories-3 > .story:not(:nth-child(3n+1))::before`로 고친다.
- 구성원: `.member-position{font-size:.78rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--red)}`, `.member-card{align-items:flex-start}`.
- 국문: `html[lang=ko] :is(.mast-over,.kicker,.phead-kicker,.profile-role,.rule-h,.team-role){letter-spacing:.02em}`. 국문 드롭캡은 끈다.
- 발표 빈 화면 `{% if pres_by_year %}`, 갤러리는 `m.news_body`로 바꾼다. `.nav-btn{min-height:44px}`, 모바일 `object-position:50% 20%`, 연도 띠 페이드.
- 선택 기능 판단
  - 갤러리 분리: **반드시 사용**. 소식 중심 홈이라 앨범이 섞이면 커버와 More stories가 행사 사진으로 채워진다. "Photo essay" 섹션으로 만들면 콘셉트가 오히려 강해진다.
  - 구성원 개인 페이지: **사용**. PI 프로필 같은 "인물 기사" 템플릿과 맞는다.
  - 연구 주제 페이지: **사용**. 연구를 "Feature 기사"로 펼칠 수 있는 유일한 테마다.
  - extra_pages: **about 사용**. 메뉴는 About·Research·People·Publications·News·Gallery 순이 원본과 가깝다.

**v02 방향(확장판)**
- **연간 "Issue" 아카이브**: 연도마다 잡지 표지(대표 논문 제목 + 학술지 + 대표 그림 + 논문 수)를 자동 생성하고, 표지를 누르면 그해 논문·뉴스·영상을 묶은 연간호로 간다. 데이터 `pubs_by_year`, `featured_pubs`, `news`, `videos`. 연도별 페이지 생성은 빌드 지원이 필요하다. 난이도 중.
- **저널 섹션 면**: 상위 학술지(Climate Dynamics 53, J. Climate 36, GRL 35…)마다 최신 3편 + 총 편수 + 첫 게재 연도를 보여 준다. 데이터 `stats.top_journals`, `pubs`. 난이도 하.
- **엘니뇨·북극 Explainer 기사**: 연구 주제 상세를 Q&A 해설 기사로 꾸민다(엘니뇨란? → 연구실 발견 → 관련 논문·영상). 추가 데이터는 `research.yaml`의 `explainer{en,ko}` 3~5문단. 난이도 중.
- **Watch → "영상 + 논문" 카드**: 영상 카드 확장 영역에 연결 논문의 초록 첫 문장과 DOI를 보여 준다. 추가 데이터는 `publications.yaml`의 `abstract`(Crossref, 선택). 난이도 하~중.

### t6_sidebar — Sidebar Portfolio
**점수**: 데이터 2 / 구조 3 / 시각 4 / 모바일 3 / 콘셉트 3 / 접근성·유지보수 3
- 데이터 2: 논문 318편은 학술지 약칭 배지(45종 모두 매핑)로 잘 소화된다. 하지만 뉴스 모바일이 75,519px로 최장급이고, 모바일 논문의 DOI 칩 318개가 39×24px이며, 졸업생은 사진 없는 표, 79건은 같은 아이콘 썸네일이다.
- 구조 3: 고정 사이드바에 메뉴와 연락처가 늘 보이는 것은 좋다. 하지만 홈 h1이 PI 이름이고 연구실 소개는 둘째 단락이다. 뉴스 필터가 없고 빈 발표가 메뉴에 있다.
- 시각 4: 타이포·여백·라이트/다크·국문이 안정적이다.
- 모바일 3: 상단 바 61px, 메뉴 버튼 44×44는 적절하다. 뉴스 목록 길이와 DOI 칩 크기가 감점이다.
- 콘셉트 3: 사이드바 레이아웃은 9종 중 유일하다. 하지만 "PI 중심 홈"이 연구실 홈페이지 목적과 어긋나고, al-folio는 흔한 개인 학자 템플릿이다.
- 접근성·유지보수 3: `:focus-visible`, 건너뛰기 링크, 국문 자간 보정이 있다. 감점은 모바일 논문 페이지 터치 미달 327개, 자체 논문 매크로, 템플릿에 하드코딩한 학술지 사전 60여 개다.

**강점**
- 학술지 약칭·출판사 색 배지(`ui.html:4-58` `jbadge`)로 318편 목록에서 저널을 한눈에 구분한다.
- 데스크톱 고정 사이드바(`style.css:87-89`)에 메뉴·언어·연락처·소셜이 늘 보인다. 모바일 접이식 메뉴도 깔끔하다.
- 국문(keep-all 40행, 라벨 자간 보정 459행)과 다크 모드(27행)가 정돈돼 있다(`t6_sidebar_ko_dark.png`).

**문제**
| 심각도 | 문제 | 캡처·위치 | 원인(파일:행/선택자) |
|---|---|---|---|
| 심각(공통) | 뉴스 188건(앨범 89 포함)이 한 목록이다. 카드 높이는 데스크톱 약 200px, 모바일 약 400px이고, 문서 높이는 37,334px/75,519px다. | `t6_sidebar_news.png`, `t6_sidebar_news_mobile.png` | `templates/news.html:8-24`, `style.css:377` `.post-item-link`(220px 썸네일), `gallery.html` 없음 |
| 보통 | 홈이 교수 프로필이다(h1 "Jong-Seong Kug", 첫 화면은 약력과 사진). 원본 Introduction을 기대하는 방문자에게는 개인 홈페이지로 보인다(1차 "확인 필요"가 미결). | `t6_sidebar.png`, `t6_sidebar_ko_dark.png` | `index.html:4-7`, `:20-21`(bio가 먼저, `site.lab.intro`는 둘째 단락) |
| 보통 | 졸업생 23명이 사진 없는 표다. "Postdoc, 2021"이 2줄로 감기고, 셋째 열은 20칸이 빈다. | `t6_sidebar_people_full.png` 하단 | `people.html:66-76` `<table>`, `style.css:365-372` |
| 보통 | 모바일 논문 페이지의 DOI 칩(39×24px) 318개와 구성원 이메일(높이 15px)이 터치 권장 크기에 못 미친다. | `t6_sidebar_publications_mobile.png` | `style.css:254` `.chip-btn{padding:2px 9px}`, `:364` `.person-mail` |
| 보통 | 표지 없는 뉴스 79건이 같은 그라데이션 아이콘 썸네일로 반복된다. | `t6_sidebar_news.png` 3번째 카드 | `ui.html:143-146` `news_thumb`, `style.css:387` `.thumb--empty` |
| 보통(공통) | 구성원 목록이 PI 이력 뒤 2,125px(모바일 3,942px)에서 시작한다. 홈과 people 둘 다 PI 중심이다. | `t6_sidebar_people_full.png` | `templates/people.html` |
| 경미 | 학술지 배지 "Commun. Earth Env." 등 18자 이상 약칭이 2줄로 감긴다(1차 지적 남음). | `t6_sidebar_publications.png` x≈486, y≈800 | `style.css:232` `.bib-side{flex:0 0 112px}`, `:233` `.jb` |
| 경미 | 발표 0건 화면이 "Nothing here yet."뿐이다. | `t6_sidebar_presentations.png` | `presentations.html:27-29` `t('common.empty')` |
| 경미 | 홈 연구 카드 5개가 150px 칸에 원본 그림을 잘라 넣었다. 연구 페이지 그림도 300px로 작다. | `t6_sidebar_full.png`, `t6_sidebar_research_full.png` | `style.css:204` `.mini-grid`, `:317` `.proj-top` |
| 경미 | 하드코딩('Skip to content', 'Previous/이전 글', 'Years', 'Key study regions'). 모바일 연도 칩에 페이드가 없고, KO 버튼 높이가 36px다. 홈 소개 문장의 "Climate System Laboratory" 링크가 연구 페이지로 간다. | — | `base.html:17`, `news_post.html:23-24`, `publications.html:16`, `style.css:284`, `:108-110`, `index.html:6` |

**1차 리뷰 지적 상태**: 배지 2줄 남음 / PI 중심 홈 미결(실제 사진·약력이 들어가 인상이 더 강해짐) / 국문 보정 유지.

**v01 방향(정제판)**
- 홈을 연구실 중심으로 재배치한다. h1은 `lab_name`, 첫 단락은 `site.lab.intro`·`tagline`, 그다음 연구 분야 5 카드, PI 카드(사진+직함+"약력 보기") 순이다. 사이드바 레이아웃은 그대로 둔다.
- 뉴스: 갤러리를 분리하고 연도 섹션 + 분류 칩 + 연도 점프(`year-pills` 재사용)로 바꾼다. 모바일 썸네일은 96px 정사각 왼쪽 배치로 줄이고, 표지 없는 글은 썸네일을 빼 한 줄로 만든다.
- 졸업생: 표를 사진 카드 그리드(`.member-grid` + `.avatar`)로 바꾼다.
- 터치·배지: `.chip-btn` 모바일 `min-height:32px`(또는 DOI 칩 제거, 제목 링크로 대체). `.bib-side` 124px + `.jb{white-space:nowrap;text-overflow:ellipsis}`. `.sb-lang-mini` 44px.
- 발표는 `m.pres_list`로 바꾼다. 하드코딩은 `t()`로 옮기고, 학술지 사전은 `data/journals.yaml`로 옮기도록 공통 제안한다(3-1절).
- 선택 기능 판단
  - 구성원 개인 페이지: **사용**. al-folio의 "프로필 → 개인 페이지" 흐름과 맞고, 카드에 이메일·관심사를 다 넣지 않아도 된다.
  - 연구 주제 페이지: **사용**. al-folio "projects" 상세 패턴으로 figures·관련 논문·영상을 담는다.
  - 갤러리 분리: **사용**.
  - extra_pages: gallery만. 홈을 바꾸지 않는다면 about을 추가해야 한다.

**v02 방향(확장판)**
- **논문 인용 도구**: 각 논문에 BibTeX/인용 복사와 Abstract 펼치기를 단다. 빌드 때 `pubs` 필드로 BibTeX를 만든다. 추가 데이터는 abstract(선택). 난이도 하.
- **배지 기반 논문 필터**: 출판사·학술지 칩, "교신저자만", "대표 논문만" 토글, 연도 미니 차트를 단다(`data-pub-search` JS 확장). 추가 데이터 없음. 난이도 중.
- **개인 페이지를 연구 프로필로**: 참여 논문(배지), 연구실 내 공저자, 연구 주제 태그, 졸업생 현소속을 보여 준다. 추가 데이터는 구성원별 주제 키(선택). 난이도 중.
- **주제별 연구 타임라인**: 엘니뇨·북극·탄소순환 주제별 논문 수를 연도 축에 나란히 그린다. 추가 데이터는 논문 318편의 주제 태그(키워드 규칙으로 1차 자동 분류 후 확인). 난이도 중.

### t7_onepage — One-page Scroll
**점수**: 데이터 3 / 구조 4 / 시각 4 / 모바일 3 / 콘셉트 4 / 접근성·유지보수 4
- 데이터 3: 논문 318편(최근 10편이 홈에 나옴)과 연구 원본 그림(본문 폭)은 잘 소화한다. 감점은 홈 구성원이 사진 대신 이니셜 칩인 것, 79건 "CSL" 대체 썸네일, 발표 0건이 홈 05 섹션과 목차 "0"으로 노출되는 것이다.
- 구조 4: 히어로 목차(번호 + 건수), 스크롤 스파이, 섹션별 "View all", 번호 브레드크럼(`← Home / 06 News`)으로 길 찾기가 가장 명확하다. people 점프 탭도 있다.
- 시각 4: Space Grotesk 디스플레이 타이포와 카드 체계가 완성도 높고 다크도 좋다. 감점은 다크 형광펜과 국문 라벨 자간이다.
- 모바일 3: 2단 고정 헤더 117px에 논문 페이지는 연도 띠까지 고정이라 첫 화면의 약 20%를 차지한다. 섹션 탭과 햄버거 메뉴가 겹친다.
- 콘셉트 4: "한 장으로 보는 연구실 + 번호형 상세 페이지"가 연구실 소개 목적에 잘 맞는다. 원페이지형 자체는 흔해서 5점은 아니다.
- 접근성·유지보수 4: 섹션 탭·연도 칩 44px, 메뉴 버튼 48px, `:focus-visible` 3px, Esc 닫기, 동작 줄이기가 있다. 공통 매크로를 가장 충실히 쓴다. 감점은 하드코딩 7곳과 국문 자간 보정이 없는 점이다.

**강점**
- 홈 히어로 목차(`index.html:19-25`)가 연구 5 / 논문 318 / 뉴스 / 영상 15 건수를 같이 보여 주고, 스크롤 스파이(`onepage.js:15-79`)가 현재 위치를 표시한다.
- 상세 페이지 브레드크럼이 같은 섹션 번호를 써서(`base.html:50-54`, `_op.html:4`) 원페이지와 상세 페이지가 한 체계로 묶인다.
- 연구 페이지가 원본 그림을 본문 폭으로 크게 보여 준다(`t7_onepage_research_full.png`). 9종 중 연구 그림이 가장 잘 보이는 축이다.

**문제**
| 심각도 | 문제 | 캡처·위치 | 원인(파일:행/선택자) |
|---|---|---|---|
| 심각(공통) | 뉴스 188건(앨범 89 포함)을 3열 카드 그리드 하나에 넣는다. 79건은 보라색 "CSL" 대체 이미지다. 데스크톱 24,075px, 모바일 66,256px. | `t7_onepage_news.png`, `t7_onepage_news_mobile.png` | `news.html:8`, `onepage.css:318-320` `.ngrid`, `:327-331` `.news-card-img--empty::after`, `gallery.html` 없음 |
| 보통 | 홈에 발표 섹션(05)이 빈 채로 나오고("Nothing here yet."), 목차에 "Presentations 0"이 보인다. 첫인상에서 "발표 실적 0"으로 읽힌다. | `t7_onepage_full.png` 05 섹션, `t7_onepage_ko_dark.png` 목차 | `index.html:107-114`, `:4-5,22` `COUNTS.presentations` |
| 보통 | 홈 구성원 목록이 사진 22장을 두고 이니셜 칩(MT, YL…)만 보여 준다. | `t7_onepage_full.png` 03 People | `index.html:81` `mrow-init`, `onepage.css:254` |
| 보통 | 모바일 고정 영역이 크다. 로고 행 + 섹션 탭 행이 117px로 고정되고, 논문 페이지는 연도 띠까지 sticky다(1차 지적 남음). | `t7_onepage_mobile.png`, `t7_onepage_publications_mobile.png` | `onepage.css:97` `.bar{position:sticky}`, `:118` `.spy`, `:290` `.years{position:sticky}` |
| 보통 | 다크 국문 태그라인의 형광펜 띠(진한 금색, 높이 36%)가 글자 아랫부분을 덮는다(1차 지적 남음). | `t7_onepage_ko_dark.png` y≈342 | `onepage.css:169` `.hero-tag span`, `:42` 다크 `--amber` |
| 보통(공통) | 구성원 목록이 PI 이력 뒤 3,441px(모바일 5,688px)에서 시작한다(점프 탭이 있어 영향은 작음). PI 경력 칸만 약 1,600px로 길다. | `t7_onepage_people_full.png` | `onepage.css:420` `.cv-grid` |
| 경미 | 졸업생 23명이 텍스트 목록이다. | `t7_onepage_people_full.png` 하단 | `people.html:55` `m.alumni_list`(공통) |
| 경미 | 뉴스·앨범 상세 본문이 780px 왼쪽 정렬이라 오른쪽 약 400px가 빈다. 하단 "News" 3건은 관련 글이 아니라 최신 3건이고 이전/다음 글이 없다. | `t7_onepage_news-2025-02-24-…_full.png` | `onepage.css:443` `.post{max-width:780px}`, `news_post.html:14-19` |
| 경미 | 국문 대문자 라벨에 영문용 자간 .1–.12em이 그대로 붙는다. | `t7_onepage_people_ko.png` "연구 관심사" | `onepage.css:73` `.eyebrow`, `:250`, `:369`, `:403`, `:455` |
| 경미 | 하드코딩('Skip to content', 'Sections', `aria-label="Main"`, 'Breadcrumb', 'Top', 'On this page', 'Years'). 모바일 연도 띠에는 페이드가 없다. | `site/t7_onepage/ko/index.html` | `base.html:16,24,35,50,79`, `index.html:19`, `publications.html:8`, `onepage.css:290` |

**1차 리뷰 지적 상태**: 다크 형광펜 남음 / 모바일 고정 117px + 연도 띠 sticky 남음 / 섹션 탭 페이드 유지(연도 띠는 페이드 없음) / "20 26" 글자 간격 미확인.

**v01 방향(정제판)**
- 빈 섹션: `{% if presentations %}`일 때만 05 섹션을 출력하고 `COUNTS`·목차에서도 0건 항목을 뺀다. `op.num()`이 nav 순서를 따르므로 공통 nav 처리와 함께 번호가 다시 매겨진다.
- 홈 구성원: `index.html:81`을 `op.avatar(mm.photo, …)` 40px 원형 사진으로 바꾸고, 이니셜은 사진이 없을 때만 쓴다. 각 행을 개인 페이지로 연결한다.
- 모바일 고정: 1240px 미만에서는 아래로 스크롤할 때 `.spy` 행을 숨기고 위로 스크롤할 때 다시 보인다(`onepage.js`에 몇 줄). 상세 페이지에서는 `.spy`를 빼고 햄버거만 남긴다. `.years`는 860px 미만에서 `position:static`.
- 형광펜: 띠를 `transparent 78%`로 낮추고 다크에서는 불투명도 35%.
- 뉴스: 갤러리를 분리하고 연도 그룹 + 분류 칩 + 연도 점프(`.years` 재사용)로 바꾼다. 표지 없는 글은 텍스트 카드로 줄인다.
- 상세 페이지 가운데 정렬, 이전/다음 글 + 같은 분류 글 3건. `.cv-grid`에서 경력 칸을 `span 2`로 한다. 국문 라벨 `:lang(ko)` 보정, 하드코딩 → `t()`(`common.skip`·`common.top`은 이미 있음).
- 선택 기능 판단
  - 구성원 개인 페이지: **사용**. "각 섹션이 같은 스타일의 상세 페이지로 이어진다"는 콘셉트와 맞고, 홈 목록에서 바로 연결된다.
  - 연구 주제 페이지: **안 씀**. 원페이지 → `research.html#key` 구조가 이미 분명하다. 대신 research.html 각 섹션에 figures 2~3장(캡션·DOI)을 더한다.
  - 갤러리 분리: **사용**. 목차 건수도 바로잡힌다(News 99, Gallery 89).
  - extra_pages: gallery만. 히어로가 연구실 소개를 맡는다.

**v02 방향(확장판)**
- **목차를 연구실 대시보드로**: 히어로 목차 옆에 연도별 논문 스파크라인과 상위 학술지 3개를 두고, 목차 항목마다 최신 날짜("News · 2026-10-23")를 붙인다. 데이터 `stats.per_year`, `stats.top_journals`, `latest()`, 추가 데이터 없음. 난이도 하.
- **연구 주제 스크롤 스토리**: 스크롤에 따라 그림(`figures`)이 단계적으로 바뀌고 캡션과 관련 논문이 함께 나온다(엘니뇨 다양성 → 원격상관 → 예측). 기존 IntersectionObserver를 재사용한다. 추가 데이터는 그림별 1~2문장 설명(국/영). 난이도 중.
- **Watch the paper 띠**: 영상 설명의 DOI로 연결된 논문·영상 쌍을 카드 하나로 묶는다(예: 영구동토층 토양수분 → Earth's Future 2026). 데이터 `videos[].pub`, `news[].pub`, 추가 데이터 없음. 난이도 하.
- **소식 타임라인**: 뉴스·논문·앨범을 하나의 세로 연표로 합치고 분류 필터와 연도 접기를 둔다. 데이터 `latest(n)`, `news[].category`, `albums`. 난이도 중.

### t8_globe — Interactive Globe
**점수**: 데이터 3 / 구조 3 / 시각 4 / 모바일 3 / 콘셉트 4 / 접근성·유지보수 3
- 데이터 3: 논문 318편(연도 레일 + 건수), 구성원 사진, 연구 그림·논문·영상은 무리 없이 나온다. 감점은 졸업생 텍스트 목록, 79건 대체 이미지, 뉴스 리드 카드의 한글 썸네일, 방문자에게 뜻이 없는 좌표 칩("0° 150°E")이다.
- 구조 3: 일반적인 8메뉴다. 홈에 News, Recent Publications, Latest(혼합 피드)가 연달아 나와 같은 글이 두 번씩 보인다. 뉴스 상세에서 나가는 길은 "Back to news"뿐이고 뉴스 필터가 없다.
- 시각 4: 지구본 히어로와 네온 타이포의 인상이 가장 강하다. 감점은 흰 원본 그림, 구 밖으로 나온 마커, 국문 키커 자간이다.
- 모바일 3: 헤더 69px와 지구본은 괜찮다. 논문 페이지는 연도 칩 7줄 아래(약 620px)에 검색창이 있고 첫 화면에 논문이 없다. 메뉴 버튼 42×40, 언어 버튼 높이 36px.
- 콘셉트 4: 연구 지역을 지구본에 찍는 발상은 기후 연구실 소재와 직접 연결된다. 다만 지역 데이터가 주제당 2~3개의 이름 없는 점이라 지금은 장식에 가깝다.
- 접근성·유지보수 3: 지구본에 방향키 회전, `aria-label`, 범례 링크, 동작 줄이기 대응이 있다. 감점은 국문 자간 보정 누락, 하드코딩("CSL · SNU", "Main", "Regions", "Map data"), vendor JS 약 120KB다.

**강점**
- 홈 지구본이 실제 `research.regions`로 점을 찍는다(`_ui.html:4-8`). 범례와 점이 서로 강조되고, 범례에 포커스하면 해당 지역으로 회전한다(`globe.js:264-290`).
- 연구 페이지가 주제마다 원본 그림, 그 주제 지역만 표시한 미니 지구본, 관련 논문, 영상을 한 블록에 묶는다(`research.html:8-42`). 콘셉트가 하위 페이지까지 이어진다.
- 공통 매크로(`pub_list`, `news_card`, `member_card`, `pres_list`, `alumni_list`)를 그대로 써서 데이터 변경에 강하다. 발표 0건도 `pres.empty` 안내문으로 처리된다.

**문제**
| 심각도 | 문제 | 캡처·위치 | 원인(파일:행/선택자) |
|---|---|---|---|
| 심각(공통) | 뉴스 188건(앨범 89 포함)이 리드 카드 + 3열 그리드 하나에 들어간다. 79건은 같은 "주황 점" 대체 이미지다. 데스크톱 25,534px, 모바일 68,530px. | `t8_globe_news.png`, `t8_globe_news_mobile.png` | `news.html:5-8`, `style.css:315` `.news-card-img--empty`, `gallery.html` 없음 |
| 보통 | 모바일 논문 페이지에서 연도 칩 27개가 7줄로 감겨 약 235px를 차지하고 검색창이 그 아래에 있다. placeholder는 "journal"에서 잘린다. | `t8_globe_publications_mobile.png` | `publications.html:5-12`, `style.css:292-300` `.year-rail{flex-wrap:wrap}`, `:282` `.pub-search` |
| 보통 | 홈에 News(3), Recent Publications(5), Latest(6, 혼합)가 연달아 나와 같은 글이 반복된다. | `t8_globe_full.png` 02·03·05 섹션 | `index.html:59-87` |
| 보통(공통) | 뉴스 리드 카드가 한글 자막 유튜브 썸네일을 영문 화면의 가장 큰 그림(약 650px)으로 보여 준다. | `t8_globe_news.png` | `news.html:6` `news[0]` 리드, 콘텐츠 cover.jpg |
| 보통 | 메뉴 버튼 42×40px, 언어 버튼 높이 36px. | `t8_globe_mobile.png` | `style.css:74` `.nav-btn{min-height:40px}`, `:72` `.lang-switch` |
| 보통(공통) | 구성원 목록이 PI 이력 뒤 2,453px(모바일 3,961px)에서 시작한다. 학력 칸(3줄)이 경력 칸(17줄) 높이로 늘어나 빈 상자가 된다. | `t8_globe_people_full.png` | `style.css:399` `.cv-grid`(stretch), `:410` `.member-card{align-items:center}` |
| 경미 | 지구본 가장자리 마커(링 r 11px)가 구 밖으로 나온다(1차 지적 남음). | `t8_globe.png` x≈1258, `t8_globe_ko_mobile.png` | `globe.js:98` `vis = dist < π/2 − 0.04`, `:71-72`, `:105` 불투명도 하한 .15 |
| 경미 | 국문 키커·라벨에 자간 .12–.16em이 그대로 붙는다("논 문 출 판"). | `t8_globe_ko_mobile.png` y≈228 | `style.css:49` `.kicker`, `:123`, `:198`, `:254`, `:364`, `:431` |
| 경미 | 국문 헤더 "CSL · SNU"가 영문으로 남아 있다. `aria-label="Main"`, 'Regions', 'Map data', 'Years' 하드코딩. | `site/t8_globe/ko/index.html` | `base.html:16,21,23,55`, `index.html:32`, `publications.html:6`, `research.html:19` |
| 경미 | 흰 원본 그림이 어두운 화면에서 튄다. 지역 이름 없이 좌표만 나온다. 뉴스 상세에 이전/다음 글이 없고 졸업생은 텍스트 목록이다. | `t8_globe_research_full.png`, `t8_globe_full.png` | `style.css:243` `.topic-img`, `index.html:52` `ui.coord(c)`, `news_post.html:12-18` |

**1차 리뷰 지적 상태**: 가장자리 마커 남음 / 모바일 placeholder 잘림 남음 / 국문 키커 자간 남음 / "CSL · SNU" 남음 / (새로 확인) 모바일 논문 연도 칩 7줄, 메뉴 40px.

**v01 방향(정제판)**
- 마커: `globe.js:98` 기준을 `dist < π/2 − 0.18`(약 10°)로 키우고, `:105` 불투명도 하한을 0으로 내린다. 링은 `dist > π/2 − 0.35`에서 숨긴다.
- 모바일 논문: 860px 미만에서는 검색을 먼저 두고 `.year-rail`을 한 줄 가로 스크롤 + 페이드로 바꾼다. 건수 알약은 검색창 아래로 내린다.
- 홈: Latest 피드를 빼거나 News와 합친다. 좌표 칩은 지역 이름으로 바꾼다(`research.regions` 이름 추가, 3-1절).
- 국문: `:lang(ko) :is(.kicker,.sub-h,.hero-stats dt,.feed-kind,.news-paper-label,.contact dt){letter-spacing:.02em;text-transform:none}`. "CSL · SNU"는 국문에서 숨기거나 i18n 값으로 바꾼다.
- 터치 44px, 갤러리 분리 + 뉴스 연도 그룹·분류 칩(표지 없는 글은 `.feed-row` 스타일 재사용), 상세에 이전/다음 글과 연결 논문. 연구 그림에 어두운 틀(패딩 12px + `#0b1626`), `.cv-grid{align-items:start}`, `.member-card{align-items:flex-start}`.
- 선택 기능 판단
  - 구성원 개인 페이지: **사용**. 공통 `member_card`가 `member_url`을 이미 지원해서 비용이 작다.
  - 연구 주제 페이지: **사용**. 콘셉트를 가장 크게 살리는 지점이다. 주제별 큰 지구본(해당 지역으로 회전·확대), figures, themes, 논문·영상을 담고, 지금 8,626px인 연구 페이지도 나뉜다.
  - 갤러리 분리: **사용**. 워크숍 앨범은 v02 "활동 지도"의 소재가 된다.
  - extra_pages: gallery만.

**v02 방향(확장판)**
- **연구 영역 지구본**: 점 대신 실제 연구 영역(Niño3.4 상자, 북극권, 서태평양 웜풀, 동아시아, 남극 로스 빙붕)을 반투명 다각형으로 칠하고, 누르면 그 영역의 논문·영상 패널을 연다. 추가 데이터는 `research.yaml`의 `areas: [{name{en,ko}, bbox|polygon}]`. 난이도 중(d3-geo는 이미 있음).
- **논문 시간 슬라이더**: 2000–2026 슬라이더로 해마다 논문의 주제 영역을 밝혀 엘니뇨 → 북극 → 탄소순환으로 옮겨 간 흐름을 보여 준다. 추가 데이터는 논문별 주제·영역 태그(키워드 자동 분류 후 확인). 난이도 중~상.
- **연구실 활동 지도**: 워크숍·학회 앨범과 언론 출연을 장소별 핀으로 찍는다(SNU, KOPRI 인천, 하와이, 포항 등). 추가 데이터는 뉴스·앨범 front matter의 `location{name,lat,lon}`(이벤트만 채워도 됨). 난이도 중.
- **논문 그림 투어**: 주제 페이지에서 그림을 넘길 때마다 지구본이 그림 속 지역으로 회전한다(영구동토층 그림 → 시베리아). 추가 데이터는 그림별 `center[lat,lon]`. 난이도 중.

---

## 3. 공통 권고

### 3-1. 공통 빌드·매크로·데이터 구조로 풀 문제 (한 번 고치면 여러 테마에 반영)
1. **앨범 분리를 기본으로**(심각 8건의 절반): 지금은 `scripts/build.py`가 `gallery.html` 템플릿이 있을 때만 `news`에서 앨범을 뺀다. 이것을 기본 동작(또는 `theme.yaml`의 `albums: separate`)으로 바꾸고, `_shared`에 기본 `gallery.html`을 두거나 basic 것을 테마별 CSS로 입혀 쓰게 한다. `stats.news`(지금 188, `build.py:173`)는 앨범을 빼서 99로 하고 `stats.albums`를 새로 둔다. t2·t3·t4·t7 홈의 "News 188"이 함께 바로잡힌다.
2. **뉴스 목록 구조**(심각 8건의 나머지 절반): 공통 컨텍스트 `news_by_year`, 매크로 `news_year_index`, 카테고리 필터(`scripts_common`에 논문 검색과 같은 패턴의 `data-news-cat`)를 제공한다. 앨범을 빼면 남는 뉴스 99건 중 79건이 이미지가 없다. 그래서 "표지 없는 글 = 텍스트 행" 매크로 변형을 공통으로 두고, 테마마다 따로 만든 대체 이미지(등압선·물결·점무늬·"CSL" 블록)를 없앤다. 99건이면 페이지 나눔 없이 연도 묶음 + 필터로 충분하다.
3. **발표 0건 처리**: `site.yaml`에 `nav_hide_empty: true` 같은 옵션을 두고, build.py의 nav 생성(`build.py:331`)에서 0건 메뉴를 뺀다. 홈 섹션은 `{% if presentations %}`로 감싸고, 빈 화면 문구는 `pres.empty`로 통일한다(지금은 `common.empty`/`pres.empty`가 섞여 있다). 원본 사이트에 발표 목록이 없었으므로 첫 발표가 들어올 때까지 메뉴에서 숨기는 쪽을 권한다.
4. **PI 이력 과밀(9종 공통 보통)**: build.py가 `pi`를 `person` 컨텍스트로 넘겨 `people/<pi-id>.html`을 만들게 하고(member.html 재사용), people 페이지에는 PI 요약 카드만 둔다. 템플릿이 없는 테마를 위해 `<details>` 접기 매크로도 제공한다. people 상단의 역할 점프 탭(t3·t7 방식)을 공통 매크로로 만든다.
5. **`m.alumni_list`에 사진 옵션**: 졸업생 사진 23장이 basic 외 8종에서 쓰이지 않는다. `member_url`이 있으면 링크도 단다.
6. **`m.member_card` 정비**: `.member-position`을 내지만 t4·t5 CSS에는 규칙이 없고, t2·t3는 자체 카드라 직위 자체가 빠진다. 이메일은 `@` 앞에 `<wbr>`을 넣어 그 자리에서만 줄이 바뀌게 한다.
7. **연구 `figures`·`themes` 공통 매크로**(`topic_figures(r)`, `topic_themes(r)`): basic 외에서는 figures 13장과 themes가 쓰이지 않는다.
8. **앨범 상세 cover 중복**: 8종 `news_post.html`이 `{% if post.cover and not post.youtube %}`라 앨범 cover가 갤러리와 겹친다(basic만 `and not post.gallery`가 있다). 공통 헬퍼 `m.post_cover(post)`로 통일한다. t5는 `m.news_body`를 쓰지 않아 갤러리 링크도 빠졌다.
9. **영상 제목 언어**: `videos.yaml` 제목이 국문뿐인데 `m.video_card`에 `lang`이 없어 영문 페이지에서 keep-all이 걸리지 않는다(basic·t2에서 "탄소/를" 끊김). 매크로에 `lang="ko"`를 주거나 `title{en,ko}`를 둔다.
10. **i18n 키 보강**: 테마마다 `'…' if lang=='en' else '…'`나 영문 고정 문구가 반복된다(t4는 22곳). `common.years`, `common.prev/next`, `common.sections`, `common.breadcrumb`, `news.date/category/more`, `pubs.search_short`(모바일 placeholder 잘림 t4·t5·t8), `site.lab.affiliation_short`, `home.welcome`, `research.regions`를 추가한다. `common.skip`·`common.top`은 이미 있으니 쓰기만 하면 된다.
11. **모바일 논문 첫 화면**: 연도 인덱스 27개가 검색창과 목록을 밀어내는 문제가 basic·t4·t8에 있다(t1·t5·t6·t7은 가로 스크롤인데 페이드가 없다). `m.year_index`에 "모바일: 검색 먼저, 연도는 한 줄 가로 스크롤 + 페이드"를 기본으로 넣는다.
12. **`research.regions`에 이름 추가**: `[{name{en,ko}, lat, lon}]`. t8 좌표 칩과 툴팁, t2·t3·t4의 지도형 v02에 함께 쓰인다.
13. **학술지 약칭 사전을 데이터로**: t6 템플릿에 하드코딩된 60여 개를 `data/journals.yaml`로 옮기면 다른 테마의 배지·필터(v02)도 재사용할 수 있다.

### 3-2. 콘텐츠(데이터) 정리
- **대표 뉴스 표지**: `content/news/2026-10-23-permafrost-soil-moisture/cover.jpg`는 한글 자막과 파란 테두리가 있는 유튜브 썸네일이다. 8종 뉴스 목록 리드 카드와 t5 영문 홈 커버에 가장 크게 나온다. 한글 없는 논문 그림으로 바꾸고, `CLAUDE.md` 2)절에 "paper 뉴스 cover는 한글 없는 논문 그림"을 규칙으로 넣는다. 필요하면 `cover_en` 선택 필드를 둔다.
- 잘린 제목 복원: `content/news/2026-08-05-live-science-super-el-nino-threshold/index.md` "…climate change researc…".
- 졸업생 학위·연도 누락 4명(Danbi Lee, Donggeon Lee, Haechan Kimm, Mihyun Jo). current는 23명 중 3명만 있다. 구성원 `pub_name`은 22명 중 11명만 있다(개인 페이지의 논문 자동 연결에 필요).
- 640×480 썸네일 1장(`static/videos/n8xFW4A_Oc8.jpg`). 해상도 낮은 뉴스 표지 3장(`2014-07-15-apcc-multimodel-patent` 500px, `2021-06-18-ski-trip`·`drone-filming` 323px).

### 3-3. 테마별로 풀어야 하는 반복 패턴 (각 테마 CSS·템플릿)
- **국문 라벨 자간 `:lang(ko)` 보정 누락**: basic(`.eyebrow`), t1, t4(모노 → sans), t5, t7, t8. t2·t6에는 이미 있으니 그 방식을 따른다.
- **터치 44px 미달**: 메뉴 버튼 t1 37 / t4 36 / t5 35 / t8 40(언어 36) / t2 폭 26. 칩·링크는 basic 연도 칩 24, t6 DOI 칩 24, t1 유틸리티 바 약 22, t4 "SNU/SEES" 19.
- **카드 사진 세로 가운데 정렬로 행마다 위치가 다름**: t4·t5·t8 `.member-card{align-items:center}` → `flex-start`.
- **PI CV 3단 높이 불균형**: t3·t4·t7·t8. 학력+봉사 / 경력 2열로 바꾼다(④가 적용되면 PI 페이지 안의 문제로 줄어든다).
- **다크 화면의 흰 원본 그림**: t4·t8은 액자(패딩 + 배경) 처리를 한다.
- **뉴스 상세 오른쪽 공백**: basic·t7은 가운데 정렬하거나 사이드를 둔다. 이전/다음 글이 없는 테마(t7·t8)에는 추가한다.
- **연구 그림이 너무 작음**: t1 220px, t2 약 210px, t6 300px. 키우거나 연구 주제 페이지로 넘긴다.

### 3-4. 규약(`themes/THEME_CONTRACT.md`) 보강 제안
- 4절 체크리스트에 추가한다: `site.lab.intro`를 홈에 반드시 표시(t5 누락), 국문 대문자·자간 라벨의 `:lang(ko)` 보정, 0건 데이터 섹션은 홈에서 숨김, 터치 대상 44px, 표지 없는 뉴스 처리.
- 자체 마크업을 쓸 때 반드시 따라야 할 필드 목록(`position`, `member_url`, `corr_authors`, `links`, 앨범 cover 조건)을 명시한다. t2·t3·t5·t6처럼 공통 매크로를 복제하면 공통 개선이 빠지기 때문이다.
- 3-1절 ①이 들어가면 "갤러리 분리"는 선택 기능이 아니라 기본값으로 적는다.

### 3-5. 권장 작업 순서
1. 3-1 ①②③(앨범 분리, 뉴스 연도·필터·텍스트 행, 발표 0건) → 심각 9건 중 8건 해소
2. t5 소개문 추가 → 나머지 심각 1건 해소
3. 3-2 대표 뉴스 표지 교체 → t5·t8 첫인상, 8종 뉴스 리드 카드 개선
4. 3-1 ④⑤⑥(PI 이력, 졸업생 사진, 구성원 카드) → 9종 people 페이지 개선
5. 최종 후보 3종(t7·basic·t8)의 v01 테마별 작업 → 교수님 비교 검토 → 선택된 테마만 v02 진행

### 3-6. 검토 도구 메모
- `shot.mjs --full`로 긴 페이지를 찍으면 `loading="lazy"` 이미지 일부가 빈칸으로 찍힌다(t7 홈·people·research에서 확인). 화면 결함으로 오인하지 않도록 스크롤 간격을 줄이거나 캡처 전에 lazy를 해제하는 단계를 추가하는 것을 검토한다.
- 자동 대비 검사는 그라데이션·배경 이미지 위 글자를 판정하지 못한다(t3 히어로 오탐, t4·t8 다크 전용은 검사 대상이 거의 없음). 대비 확인은 캡처를 직접 보고 했다. 1차 리뷰의 "글자 간격 불균일"(DPR2 힌팅 추정)은 실기기에서 확인해야 한다.
