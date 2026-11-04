# basic 계열 확장 버전 보고서 (basic.v01 · basic.v02)

- 작업일: 2026-11-04 / 기준 테마 `themes/basic/` → `themes/basic.v01/`(정제판), `themes/basic.v02/`(확장판)
- 근거: `reports/review_round2.md` 2절 basic(문제 표 9행, v01·v02 방향)과 3절 공통 권고, `reports/visual_review.md` basic 경미 5·6, `themes/THEME_CONTRACT.md` 3-1·3-2·4절
- 원본 메뉴 구조(Introduction / Research / People / Publication / Notice 드롭다운)는 두 버전 모두 그대로 유지했다.
- 고친 곳은 두 테마 폴더와 이 보고서뿐이다(`scripts/`, `data/`, `content/`, `static/`, `_shared/`, 다른 테마는 건드리지 않음. `build.py --theme all`, git commit 안 함).

## 검증 결과
| 항목 | basic.v01 | basic.v02 |
|---|---|---|
| `build.py --theme …` | 498쪽 | 500쪽(+ archive EN/KO) |
| `validate.py --theme …` | **오류 0**, 경고 6(모두 데이터 공통: 숨긴 논문 1, videos.yaml에 없는 유튜브 ID 5) | **오류 0**, 경고 6(같음) |
| `check_layout.mjs … --sample`(360px) | 38쪽 문제 0 | 40쪽 문제 0 |
| JS 동작(Playwright, 스크래치 스크립트) | 공지 분류 필터(논문 출판 4건), 논문 검색(permafrost 3), 모바일 메뉴 정상, JS 오류 0 | 게시판 분류(수상 9)·검색(kbs 11)·빈 결과 문구, `?q=엘니뇨`(26), 이전 글 `#198`(1)·포트폴리오(13), 갤러리 검색(workshop 31), JS 오류 0 |

---

## basic.v01 — 정제판

`theme.yaml`: `title: Basic v01`, `extra_pages: [about, gallery]`, `pi_page: true`(교수 개인 페이지 `people/jong-seong-kug.html` 생성).

### 바꾼 점(리뷰 항목 대응)
| 리뷰 항목 | 처리 | 파일 |
|---|---|---|
| 문제 1(보통·공통) PI 이력 과밀 / 공통 ④ | people 첫머리를 **교수 요약 카드**(사진·직함·연락처·소개·관심 분야 칩·"자세한 이력" 버튼)로 줄이고, 학력·경력·학술 활동·수상·학회 회원·대표 논문은 `pi_page` 개인 페이지로 옮김. 개인 페이지는 학력+경력+학회 회원 / 학술 활동+수상 2단으로 행 수를 맞춤. 상단에 역할 점프 탭(교수·연구원 10·학생 12·졸업생 23, 데스크톱 고정). 구성원 카드는 데스크톱 약 820px부터 시작(기존 3,066px) | `templates/people.html`, `member.html` |
| 문제 2 웹폰트 없음 | Pretendard Variable dynamic-subset CSS(jsdelivr, 규약 4-9 예외) + 시스템 글꼴 대체 체인 | `base.html`, `style.css` |
| 문제 3 모바일 논문 연도 칩 5줄 / 공통 ⑪ | **검색창 → 연도 칩 → 목록** 순서로 바꿈. ≤600px에서 연도 칩을 한 줄 가로 스크롤 + 오른쪽 페이드로, 칩 높이 34~36px | `publications.html`, `.chip-row` |
| 문제 4 국문 "Welcome"/"YouTube", 키커 자간 | `t('home.welcome')`, `t('menu.videos')`로 교체(홈·소개·푸터). `:lang(ko) :is(.eyebrow,.crumb,.menu-top,…){letter-spacing:0;text-transform:none}` | `index.html`, `about.html`, `base.html`, `style.css` |
| 문제 5 공지 목록 정렬 / 공통 ② | `news_by_year` + `m.news_filter()`(분류 버튼, 건수 포함) + `m.year_links`. 표지가 없는 글에도 **같은 폭의 분류 라벨 칸**을 둬 제목 시작 위치를 통일(라벨 칸은 높이를 낮춰 목록이 길어지지 않게) | `news.html` |
| 문제 6 홈 영상 격자 빈칸 / 영상 제목 끊김(공통 ⑨) | 데스크톱 900px 이상 `repeat(3,1fr)` 고정(`.grid-3--fixed`). 영상 제목은 공통 매크로의 `text_lang` 덕분에 `lang="ko"` keep-all 적용 | `index.html`, `style.css` |
| 문제 7 뉴스 상세 오른쪽 공백(1차 경미 6·19 포함) | 본문 + 오른쪽 **'다른 소식' 사이드**(최근 공지 6건, 데스크톱 고정) + 아래 **이전/다음 글**(앨범은 앨범끼리). 표지는 `m.post_cover`(공통 ⑧) | `news_post.html` |
| 문제 8 갤러리 모바일 1열 | `minmax(min(46%,250px),1fr)`로 휴대폰 2열. 사진 수는 표지 위 배지(카메라 아이콘 + 숫자, "1 photos" 문법 문제 회피) | `gallery.html`, `style.css` |
| 문제 9 소개 통계 "2000– / Years" | "318 논문 · 2000년부터"(Since 2000)로 합치고 졸업생 수 칸 추가. 통계 칸은 해당 페이지로 링크 | `about.html` |
| 접근성 감점(포커스·칩 24px) | `:focus-visible{outline:2px solid var(--accent-2)}`, 칩·필터·메뉴 터치 34~44px, 모바일 하위 메뉴 44px | `style.css` |
| 공통 ③ 발표 0건 | Publication 드롭다운의 Presentations 하위 메뉴를 `{% if presentations %}`로 숨김(첫 발표가 들어오면 자동 노출). 페이지 자체와 빈 화면 문구(`pres.empty`)는 유지 | `base.html` |
| 공통 ⑥ 이메일 줄바꿈 | 교수 카드·개인 페이지 이메일에 `m.email_wbr` | `people.html`, `member.html` |
| 1차 경미 5(헤더·Menu 버튼) | 이미 해결된 69px 헤더 유지 + 모바일 브랜드 말줄임(겹침 수정), 햄버거 아이콘 + 44px 버튼 | `base.html`, `style.css` |

### 그 밖의 다듬기
- 실제 데이터 반영: 홈 히어로 아래 **사실 띠**(318 논문·2000년부터 / 연구 분야 5 / 구성원 22 / 졸업생 23 — 모두 `stats`), 연구 주제 페이지에 연구 지역 칩(`region_names`), 국문 제목에 `lang`(text_lang)으로 keep-all.
- 시각: 상단 3px 남색 띠, 섹션 제목 밑 강조선, 카드 테두리·hover, 뉴스 분류별 색(논문·수상·행사·언론·연구실, 라이트/다크 각각), 공지 상세 논문 카드 왼쪽 강조선.
- 선택 기능 판단(리뷰 그대로): 구성원 개인 페이지 유지(45 + 교수), 연구 주제 페이지 유지, 갤러리 분리 유지, about·gallery 유지. 학위·연도가 없는 졸업생 6명(리뷰 집계 4명 + degree만 있는 2명)은 개인 페이지에 학력·경력이 있어 링크를 숨기지 않았고, 카드에는 빈 학위 줄을 출력하지 않게 했다.

### 캡처(`site/_shots/`)
`basic.v01.png`·`_mobile.png`(홈), `basic.v01_full.png`, `basic.v01_ko_dark(_mobile).png`, `basic.v01_people_full(_mobile).png`, `basic.v01_people_ko(_mobile).png`, `basic.v01_people-jong-seong-kug(_full)(_mobile).png`, `basic.v01_people-yechul-shin(_mobile).png`, `basic.v01_publications(_mobile).png`, `basic.v01_news(_mobile).png`, `basic.v01_news_ko(_mobile).png`, `basic.v01_gallery(_mobile).png`, `basic.v01_news-2026-10-23-permafrost-soil-moisture(_mobile).png`, `basic.v01_about(_mobile).png`

---

## basic.v02 — 확장판

`theme.yaml`: `title: Basic v02`, `extra_pages: [about, gallery, archive]`, `pi_page: true`. v01 전체를 바탕으로 리뷰 v02 방향 4가지를 구현했다(+ 논문 연도 막대). 데이터는 빌드 컨텍스트에 있는 것만 썼고 런타임 외부 요청은 없다(웹폰트 제외).

### 새 기능
1. **공지 게시판 분류·검색**(리뷰 v02-①) — `news.html`, `assets/board.js`
   - 원본 게시판처럼 **번호(99…1)·분류·제목·날짜** 한 줄 목록(연도 묶음 유지). 영상·사진이 있는 글은 제목 옆 아이콘.
   - 분류 탭(건수) + 제목·요약 검색(국·영 제목을 함께 색인) + "표시 n / 99" + 빈 결과 문구. `?q=`, `?cat=` 주소 지원.
   - 목록 높이가 v01 썸네일 행보다 크게 줄었다. 모바일은 "분류 · 날짜 / 제목" 2줄.
   - 같은 `board.js`를 갤러리 검색(89 앨범)과 4번 표에도 쓴다(테마 안에 있는 50행 스크립트, 의존성 없음).
2. **개인 페이지 논문 연표와 연구실 내 공저자**(리뷰 v02-②) — `member.html`, `ui.html`의 `year_bars`
   - 구성원: 참여 논문 연도별 막대 SVG(최소 5년 폭, 막대를 누르면 아래 연도별 목록 `#pyYYYY`로 이동) + **연구실 내 공저자**(같은 논문에 이름이 있는 구성원·졸업생, 사진·편수, 개인 페이지 링크, 편수 순). 논문 목록은 연도별로 묶었다.
   - 교수 페이지: 연구실 전체 318편 연도별 막대(`stats.per_year_full`, 막대 → 논문 목록의 그 해) + 대표 논문.
   - 매칭은 `pub_name` 표기 일치 + `is_me()`의 기간·제외 규칙. `pub_name`이 있는 29명(구성원 11 + 졸업생 18)에게 나온다.
3. **연구 지역 지도**(리뷰 v02-③, 일부) — `research.html`, `research_topic.html`, `ui.html`의 `region_map`, `assets/land.svg`
   - 연구 페이지: 5개 분야의 `regions` 12점을 **태평양 중심 경위도 격자 지도** 한 장에 분야 색으로 표시(같은 좌표는 옆으로 살짝 밀어 겹침 방지, 점 → 해당 분야 섹션 링크, 범례에 지역 이름).
   - 주제 페이지: 요약 옆(넓은 화면) 카드에 그 주제 지역을 번호로, 다른 주제 지역은 흐리게. 번호 목록에 지역 이름과 위경도.
   - 바탕 육지는 `tools/make_land.mjs`가 Natural Earth 110m(world-atlas, 공개/ISC)을 d3-geo로 등장방형(중심 160°E) 투영해 만든 정적 SVG(55KB). 라이브러리는 `tools/vendor/`에만 두고 런타임에는 쓰지 않는다. 점은 Jinja에서 같은 식으로 계산해 JS 없이 그린다.
   - "주제별 전체 논문"은 논문별 주제 태그가 데이터에 없어 구현하지 않았다(지어내지 않음).
4. **이전 사이트 글 찾기**(리뷰 v02-④) — `archive.html`(extra page), Notice 드롭다운·푸터에 링크
   - 뉴스·앨범 앞머리의 `source`(예: `notice#198`, `gallery#265`, `portfolio#874`)로 **원래 게시판·번호 → 새 글·새 위치(공지/갤러리)** 표 194행(184편, 한 글에 출처가 여럿이면 각각). 게시판 탭(공지 94·갤러리 85·포트폴리오 13·GS칼텍스 매거진 2) + 번호·제목 검색.
   - 원본 사이트의 주소 형식은 자료에 없어서 주소는 만들지 않고 게시판 이름과 번호만 보인다. `source`가 없는 4편은 표에 없다.
5. (덧붙임) **논문 연도 막대** — `publications.html` 상단, 막대 → 연도 섹션. 연도 칩·검색 순서는 v01과 같다.

### 캡처(`site/_shots/`)
`basic.v02.png`·`_mobile.png`(홈), `basic.v02_news(_mobile).png`(게시판), `basic.v02_research(_mobile).png`, `basic.v02_research_ko_dark(_mobile).png`, `basic.v02_research-mechanism(_mobile).png`, `basic.v02_research-ocean-atmosphere(_mobile).png`, `basic.v02_people-yechul-shin(_full)(_mobile).png`(연표·공저자), `basic.v02_people-jong-seong-kug(_full)(_ko)(_mobile).png`, `basic.v02_publications(_mobile).png`, `basic.v02_archive(_mobile).png`, `basic.v02_archive_ko(_mobile).png`

---

## 남은 문제·제안
- **테마 전용 문구**: i18n.yaml에 없는 문구(Since {y}, 게시판 열 이름·검색 안내, 연표·공저자·지도·이전 글 제목 등)는 각 테마의 `templates/ui.html`(`TX`, EN/KO)에 두고 `tr()`로 쓴다. 공통 키로 올릴 후보: `common.since`, `news.search`, `news.no_match`, `people.coauthors`, `pubs.per_year`, `research.map_note`, `archive.*`.
- **공저자 매칭**: 저자 표기가 `pub_name`과 글자 단위로 같아야 잡힌다(예: Park, J.-H.는 표기 변형 1편이 빠질 수 있음). `pub_name`이 없는 구성원 11명은 논문·연표·공저자가 없다(데이터 보강 필요, 리뷰 3-2).
- **지도**: 점 자료만 있어 영역(다각형)은 그리지 않았다. 태평양 중심이라 경계선(20°W)이 아이슬란드·그린란드 동쪽 끝을 지난다. 바탕 SVG를 바꾸려면 `node themes/basic.v02/tools/make_land.mjs`를 다시 실행한다.
- **이전 글 표**: 2024년 이후 글의 번호는 원본 캐시의 큰 글 번호(예: #19018)라 옛 게시판 목록 번호와 다를 수 있다. 원본 주소 형식이 확인되면 "원본 주소" 열을 더할 수 있다.
- v02 게시판은 의도적으로 썸네일을 뺐다(원본 게시판형). 사진 위주로 보려면 v01 방식이 낫다.
- 콘텐츠 공통 문제(리뷰 3-2)는 그대로다: 대표 논문 뉴스 표지의 한글 자막 썸네일(홈 영상 카드·공지 상세), 잘린 영문 제목 1건("…climate change researc…").
- 웹폰트는 jsdelivr CDN(규약 허용 예외)이라 오프라인에서는 시스템 글꼴로 보인다.
