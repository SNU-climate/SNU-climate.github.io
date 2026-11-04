# 백업 이관 보고서 A2 — 공지·갤러리·연구·소개·발표 (2026-11-04)

브리프: `reports/briefs/migrate_content.md` · 자료: DB 덤프(2024-04-09) JSONL, WP Rocket 캐시(2026-09~10), `wp-content/uploads`.
생성 도구(스크래치, 재실행 가능): `gen.py`(뉴스·사진), `research_img.py`(연구 그림·소개 사진), 명세 `spec_notice.yaml`·`spec_gallery.yaml`.
검증: `python scripts/validate.py --data-only` → **오류 0**, 경고 6(숨긴 논문 1, videos.yaml에 없는 유튜브 ID 5 — 썸네일은 YouTube에서 직접 로드). build.py는 돌리지 않음(지시).

## 1. 요약

| 원본 | 원본 건수 | 옮김 | 못 옮김 | 새 위치 |
|---|---|---|---|---|
| NOTICE(board 1) — DB | 83 (+휴지통 2) | 83 | 휴지통 2 | `content/news/` 뉴스 83편 |
| NOTICE — 2024-04 이후(캐시 목록 91–100 + 홈 위젯 1) | 11 (제목·날짜만) | 11 (제목만) | — | 뉴스 11편 |
| NOTICE — 번호 84–90 | 7 (목록·본문 없음) | 0 | **7** | — |
| GS칼텍스매거진(board 2) | 2 | 2 (1편은 공지 #256과 합침) | — | 뉴스 1편 + 합침 1 |
| Gallery(board 4) — DB | 77 (+휴지통 1) | 77 | 휴지통 1(테스트) | 앨범 77편 |
| Gallery — 2024-04 이후(캐시 1쪽) | 8 | 8 (사진 포함) | — | 앨범 8편 |
| 갤러리 portfolio 글 | 13 | 13 (8편은 게시판 글과 같은 사진이라 합침, 2편은 1편으로 합침) | — | 앨범 4편 + 합침 9 |
| 연구 5개 주제(`/research-*/`) | 5 | 5 (그림 13) | 숨김 섹션 그림 3 | `data/research.yaml`, `static/research/` |
| 소개·위치(`/introduction/`, `-map/`, 홈 히어로) | — | intro·tagline·photo | — | `data/site.yaml` `lab.*`, `static/img/lab-intro.jpg` |
| 학회 발표 | 원본에 없음 | placeholder 3건 삭제 | — | `data/presentations.yaml` → `presentations: []` |

- **새 뉴스 폴더 184개**(공지·매거진 95 + 앨범 89). 기존 뉴스 4편은 그대로(원본 공지와 같은 소식 없음 — 2024-02 이후 DB 공지가 없고, 2026년 논문 뉴스 3편과 겹치는 공지 제목도 없음). 전체 뉴스 188편.
- category: 뉴스 media 83 · award 9 · event 2 · paper 1 / 앨범 event 67 · lab 15 · award 6 · media 1.
- **사진 총용량 115.6 MB (477장)** — 앨범 사진 + 공지 본문 그림. 긴 변 1600px, JPEG 85, EXIF 회전 반영 후 EXIF 제거(ICC 색 프로파일만 유지). 300MB 미만이라 줄이지 않음. 원본 대비: 갤러리 원본 300.6 MB(415장) → 대폭 축소.
  - 별도: 연구 그림 13장 1.6 MB(`static/research/`), 소개 사진 0.24 MB, 공지 첨부 PDF 6개 18.8 MB.

## 2. 이관 규칙(판단한 것)

- **날짜**: 공지는 DB 작성일(원본 목록에 보이던 날짜). 단, 원본 사이트 이전 때 일괄 등록한 **2021-08-16 60편, 2021-06-11 7편**은 실제 기사 날짜가 아니어서 2026-11-04에 따로 바로잡았다(아래 §2.1). 갤러리는 제목 앞의 행사 시작일, 월만 있으면 1일(6편: 생일 5, 서울 나들이 1), 날짜 없으면 작성일(`International Workshop on Climate system` → 2023-05-18).
- **언어**: 원문이 국문이면 `index.ko.md` = 원문 그대로(HTML → Markdown, 링크 유지), `index.md` = 영문 제목 + 1~3문장 번역 요약 + 원문 링크 목록. 원제가 영문인 공지 8편(#229·250·255·258, 캐시 95·98·99·100)은 영문 제목이 원문이고 국문 제목이 번역(본문은 4편 모두 국문 원문).
- **링크**: 본문 첫 링크를 `link:`(원문 보기 버튼). 유튜브는 `youtube:`(7편). 논문 소식은 `doi:`(publications.yaml에 있는 것만, 22편 — 부록 A 비고).
- **본문 그림**: 공지 본문 `<img>`는 원본 크기 파일로 바꿔 `figN.jpg` + `gallery:`/`cover:`(10편, 그림 20장). 구 사이트 `csl.postech.ac.kr/editor/...` 그림 1장(#200, 같은 그림의 사본)은 백업에 없어 생략.
- **첨부**: 공지 첨부 PDF 6개를 영문 파일명으로 글 폴더에 복사하고 본문에 링크(#4·199·201·243·244·256).
- **앨범 사진 순서·표지**: 본문 `<img>` 순서 → 나머지 `kboard_meida`. 표지는 원본 목록 썸네일과 같은 사진을 찾아 지정(22편, dHash 비교), 나머지는 첫 사진.
- **2024-04 이후 갤러리 8편 사진**: `kboard_attached/4/2024xx·202503`의 파일명 앞 8자리(16진수 유닉스 시각)로 업로드 묶음을 나눠 목록 썸네일과 대조. 묶음 순서가 글 번호(uid 19014→19018) 순서와 일치하고, 사진 내용(현수막·장소)도 제목과 맞는 것을 눈으로 확인.
- **앨범 본문**: 원제목(행사 기간 포함) 한 줄 + 원문 본문이 있으면 그 내용(5편: 경주 워크샵, BK21 시상식, 2022·2023 기상학회, 2023 해양학회). 영문은 번역.
- **source**: `notice#uid`, `gallery#uid`, `gsmagazine#uid`, `portfolio#ID`(합친 글은 목록).

### 2.1 일괄 등록 공지 67편의 날짜 수정 (2026-11-04)

근거 우선순위: 원문 기사 페이지의 게시일(메타 태그) > 기사 URL 속 날짜 > 본문·제목의 명시 날짜 > 연·월만 나오는 근거. 논문 출판일로 추정하지 않았다.
각 글 `index.md`에 `date`(정밀도대로 YYYY-MM-DD / YYYY-MM / YYYY), `posted`(원 등록일), `date_source`(근거)를 넣었고, 날짜를 바꾼 57편은 폴더 이름도 새 날짜로 바꿨다(월·연까지만 확실하면 `YYYY-MM-`·`YYYY-` 접두, validate 규칙도 이에 맞춤). 아래 부록 A의 폴더 이름은 바뀐 이름이다.

| 결과 | 편수 |
|---|---|
| 날짜까지 확인 | 45 |
| 월까지만 확인 | 4 — 동아사이언스 2020년 11호·12호, 과학동아 2014년 4월호(원본 첨부 파일명), 2018 국가연구개발 성과평가 포상(2018-12) |
| 연도만 확인 | 8 — MBC 다시보기 3편(URL 연도 2014·2015·2015), 2015 한국기상학회 봄학술대회 수상, 임형규 장학생 인터뷰 2018·2019, SBS 희망TV 2018, 한국인 첫 APEC과학상 기사 모음(2015년 수상) |
| 근거 없음(등록일 유지) | 10 |

추론이 들어간 판정 2건: 한국일보 몬스터 엘니뇨 인터뷰는 본문의 "6월 13일 금요일자"가 2014–2021년 중 2014년에만 맞아 2014-06-13으로 정했다. 유튜브 영상 2편은 업로드 시각(태평양 시간)을 한국 시간으로 바꿔 2015-09-07, 2020-09-09로 정했다.

**근거 없음 10편** — 원문이 삭제됐거나 본문에 날짜가 없다. 실제 날짜를 알면 `date`만 고치고 폴더 이름을 바꾸면 된다.

| 폴더 | 사유 |
|---|---|
| `2021-06-11-jeon-jaegyu-award-woo` | 제4회 전재규 젊은과학자상(우성호) — 본문·링크에 날짜 없음 |
| `2021-06-11-kscc-young-scientist-award` | 한국기후변화학회 신진연구자상 — "지난 6월 19일"만 있고 연도 없음 |
| `2021-08-16-earth-com-plants-arctic` | Earth.com 기사 삭제(HTTP 410) |
| `2021-08-16-gs-caltex-tipping-points` | GS칼텍스 미디어허브 접속 안 됨 |
| `2021-08-16-jtbc-arctic-summer-heat` | JTBC 영상 삭제(김다슬 인터뷰) |
| `2021-08-16-kim-jung-sungki-thesis-award` | 정성기논문상 — "2018학년도"만 있음(학년도라 달력 날짜 단정 불가) |
| `2021-08-16-lim-science-donga-feature` | 과학동아 "11월호" — 연도 없음 |
| `2021-08-16-rok-pi-clips-phase-2` | SPREP 기사 접근 거부(HTTP 403) |
| `2021-08-16-samsung-wealth-management` | 첨부 간행물만 있음 |
| `2021-08-16-yonhap-iod-australia-fires` | 연합뉴스 네이버TV 영상 삭제 |

## 3. 합친 항목(중복 글을 만들지 않음)

| 원본 | 합친 대상 | 근거 |
|---|---|---|
| GS칼텍스매거진 #1 「동아사이언스 2020년 11호 기획_과학난제 기사」 | 공지 #256 (같은 제목, PDF 첨부) → `2020-11-dongascience-science-puzzles-11` | 제목 동일 |
| portfolio 819 「2014.05.15 UNIST-POSTECH 공동 세미나」 | gallery #260 | 같은 사진 파일(1415782843/833) |
| portfolio 874 「2014.8.5~8.7 POSTECH-OST JOINT WORKSHOP」 | gallery #261 | 같은 사진(1415857xxx) |
| portfolio 876 「irreversible climate change work」 | gallery #262 (장연수 생일) | 사진 3장이 #262와 완전히 같음(dHash 0) — 제목만 잘못 붙은 복제 글 |
| portfolio 878 「하계 드림프로그램」 | gallery #305 (2019 KGU) | 대표 이미지가 #305 사진을 자른 것(현수막 '2019 하계 드림프로그램') |
| portfolio 880 「OASIS 학술발표회」 | gallery #304 | #304 첫 사진을 자른 것 |
| portfolio 882 「김다영 박소원 석사 졸업식」 | gallery #312 | #312 사진을 자른 것 |
| portfolio 907 「2020 졸업식」 | gallery #309 (2019.02.09 김진수·임형규 박사 졸업식) | #309 사진을 자른 것(제목의 '2020'은 오기로 보임) |
| portfolio 6129 「단체 사진」 | gallery #696 (science 기사 촬영) | 같은 원본(F7A2014) |
| portfolio 17414 「CSL 단체 사진 2」 | portfolio 17411 「CSL 단체 사진」 → `2024-01-29-csl-group-photo` (2장) | 같은 날 촬영 단체 사진 |

공지와 갤러리가 같은 행사를 다룬 경우(예: 2018 국가연구개발 유공 포상 공지 #246 ↔ 갤러리 #294 시상 사진)는 게시판 성격이 달라(공지=소식, 갤러리=사진) 각각 유지했다.

## 4. 못 옮긴 항목과 이유

| 항목 | 수 | 이유 |
|---|---|---|
| 공지 번호 84–90 | 7 | DB(2024-04-09) 이후·캐시 목록 1쪽(91–100) 이전 글. 제목·날짜·본문 모두 백업에 없음 |
| 공지 휴지통 글 | 2 | #230(#231과 같은 글), #699 「TEST」 |
| 갤러리 휴지통 글 | 1 | #313 「테스트 제목입니다」 |
| 목록에 없는 갤러리 업로드 | 사진 8 + 썸네일 5 | `kboard_attached/4/202510/`(2025-10-14 업로드, 해외 워크숍 사진 8장), `kboard_thumbnails/4/202601/`(2026-01-28, KGU·2025 한국기상학회 가을학술대회 등 단체사진 썸네일 5장). 2026-10 캐시 Gallery 목록에 해당 글이 없어 제목·날짜를 알 수 없음 → 원 게시글 확인 후 추가 가능 |
| 연구 페이지 숨김 섹션 그림 | 3 | `/research-mechanism/`의 구버전 섹션(모든 기기에서 숨김): Group-433-1, Group-434 「Arctic amplification and atmospheric transport … [Kug et al. 2010, GRL]」(doi 10.1029/2010gl043673), Group-435 「Paleoclimate and aerosol feedback … [Lambert et al. 2013, Nature Climate Change]」(doi 10.1038/nclimate1785). 원본에서 보이지 않던 것이라 넣지 않음(필요하면 그대로 추가 가능) |
| 홈 연구 카드 그림 `main-1~5.png` | 5 | 432×78px 크기의 아이콘+제목 띠 이미지(글자 포함)라 대표 그림으로 부적합 → 각 주제 첫 그림을 `image`로 씀 |
| 홈 Welcome 장식 사진 `Rectangle-84.png` | 1 | 얼음 호수 풍경 장식 이미지(연구실 사진 아님). 소개 사진은 `/introduction/`의 F7A2039를 씀 |
| 「드론촬영」 portfolio 글의 유튜브(Wgy18CX6oq0) | 1 | DB에 oEmbed 캐시만 남아 있고 현재 원본 페이지에는 영상이 보이지 않음 → 넣지 않음(연구실 소개 영상으로 보이니 확인 후 `youtube:` 추가 가능) |
| 원본 사이트 FAX(054-279-8354, 취소선) | 1 | POSTECH 시절 번호, 원본에서도 취소선 처리 |

## 5. 확인 필요

### 5.1 원문 링크 필요(본문 없이 제목·날짜만 넣은 글, 12편)
캐시 목록에 제목·날짜만 남아 있다. 본문은 제목 한 줄. 원문 기사·영상 URL을 받으면 `link:`와 본문에 추가.

| 폴더 | 원본 | 비고 |
|---|---|---|
| `2025-06-25-sbs-forest-ecosystem-climate` | notice#19023 (91번) | |
| `2025-08-11-kbs-life-human-extinction` | notice#19024 (92번) | |
| `2025-09-08-unrealscience-gangneung-drought` | notice#19322 (93번) | |
| `2025-10-26-economy-science-korean-seas-winter` | notice#21418 (94번) | |
| `2026-05-15-nature-news-super-el-nino` | notice#22040 (95번) | 영문 원제 |
| `2026-06-08-mbc-super-typhoon-super-el-nino` | notice#22041 (96번) | |
| `2026-06-16-youtube-weather-of-war-super-el-nino` | notice#22042 (97번) | `youtube: rLo8Va_ZyGA` — videos.yaml의 같은 제목 영상(연구실 채널 재업로드, 원본 l9g-BJfStag)으로 연결 |
| `2026-06-24-nature-explainer-super-el-nino` | notice#22043 (98번) | 영문 원제(95번과 같은 제목) |
| `2026-07-08-net-zero-speaks-interview` | notice#22044 (99번) | 영문 원제, 유튜브 ID 모름 |
| `2026-08-05-live-science-super-el-nino-threshold` | notice#22045 (100번) | **원제가 목록에서 잘려 있음**("…climate change researc") — 전체 제목 필요 |
| `2026-10-07-kbs-strongest-el-nino-heavy-rain` | notice#22363 (101번, 홈 최신글 위젯) | `youtube: DaqKSaZQapQ` — videos.yaml의 같은 제목 영상으로 연결. 공지 목록 캐시(2026-09-12) 이후 글이라 번호는 추정 |
| `2020-12-dongascience-science-puzzles-12` | gsmagazine#2 | 원본 본문·첨부 없음 |

### 5.2 번역한 항목
- 공지 뉴스 95편: 국문 원문 글의 **영문 제목·요약은 모두 번역**(원문에 있는 내용만). 영문 원제 8편의 **국문 제목은 번역**(#229·250·255·258·95·98·99·100).
- 앨범 89편: 영문 제목·본문 번역(원제목이 영문인 것은 그대로). 원문 본문이 있던 5편의 영문 요약 번역.
- 연구: `themes.ko`(28항목)와 그림 설명 `caption.ko` 번역. title·summary는 영·국 원문. 그림 설명 2개(극한 기후 두 그림)는 그림 이미지 안에 적힌 설명문을 옮겨 적음.
- `lab.intro.ko`, `lab.tagline.ko` 번역(원문은 영문만).
- 사람 이름 로마자: 원본 구성원 목록 표기를 따름(Jinsoo Kim, Hyunggyu Lim, Yeon-Soo Jang, Daseul Kim, So-Won Park, Dayeong Kim, Kyung Min Noh, Woohyun Yang, Jaeheung Park, Ji-Hoon Oh, Sunhee Wang, Gayan). 목록에 없는 4명은 추정: 손혜영 → Hye-Young Son(논문 표기 Son, H.-Y.), 우성호 → Sung-Ho Woo(Woo, S.-H.), 민영미 → Young-Mi Min, 디아 → Diah(I Gusti Ayu Diah Valentina Lestari).

### 5.3 연락처
- 원본: 위치 페이지 주소 「서울특별시 관악구 관악로 1 서울대학교 501동 자연과학대학」, TEL 02-880-8177 / 꼬리말 「[08826] Room 501, 507, Seoul National University College of Natural Sciences…」, TEL 02-880-6725.
- `site.yaml`의 전화(연구실 880-8177, 교수실 880-6725)·연구실 507호는 원본과 일치 → **contact는 바꾸지 않음**. 다만 `address`의 **522호(교수실)는 원본에 없는 정보**(학과 페이지 출처로 보임)이고, 원본 꼬리말은 507호(연구실)를 주소로 썼다. 대표 주소를 522호/507호 중 무엇으로 할지 확인 필요.

### 5.4 그 밖
- **공지 첨부 PDF 공개 여부**: 원본 KBoard 설정에서 첨부 다운로드 권한이 '관리자'였다(방문자는 내려받을 수 없었음). 지시대로 옮겼으나 대부분 언론·간행물 지면(과학동아, 동아사이언스, M이코노미뉴스, 삼성생명 WM)이라 공개 게시 전 저작권 확인 필요. 공개하지 않으려면 해당 폴더의 PDF와 본문 '첨부' 줄을 지우면 된다(`2014-04-science-donga-fine-dust`, `2014-07-10-m-economy-el-nino-food-prices`, `2014-12-22-kiost-postech-workshop-2014`, `2021-08-16-lim-science-donga-feature`, `2021-08-16-samsung-wealth-management`, `2020-11-dongascience-science-puzzles-11`).
- 갤러리 portfolio 글 날짜: 「최상급자 전용 스키체험」·「드론촬영」 → WordPress 작성일 2021-06-18(원본 페이지 표시 날짜 2020-02-07은 복제 원본에서 따라온 값), 「22년 해양학회 추계학술대회」 → 작성일 2022-02-16(제목의 '22년'과 맞지 않음, 2021년 행사일 가능성), 「CSL 단체 사진」 → 페이지 표시일 2024-01-29. 스키·드론은 대표 이미지 1장(원본도 1장)뿐.
- 원문 그대로 둔 어긋남: #237 제목은 [연합뉴스]인데 본문은 YTN 인터뷰·YTN 링크(#239와 같은 링크). #4411·#13432는 링크 글자와 실제 주소가 달라 실제 주소(href)를 씀. #11668 본문의 '아래' 링크는 앞 글(#11166) 영상이 잘못 복사된 것이라 링크만 뺌.
- DOI 연결 판단: 기사 본문이 "연구 결과를 발표"라고 밝히고 논문이 하나로 특정되는 경우만 연결. 특정이 애매한 #237·239(엘니뇨-아마존 탄소), #252(시베리아 산불), #698(CO2 감축 후 비가역성, ITCZ 논문일 가능성)은 연결하지 않음.
- 앨범 표지: 원본 썸네일과 맞는 사진을 못 찾은 2편(`2023-08-18-phd-graduation-kyung-min-noh`, `2023-12-04-climate-engineering-forum`)은 첫 사진.
- 갤러리 #11153 사진 1장(`kboard_attached/4/202305/646581c0c16059159996.jpg`)은 원본 파일 끝 8바이트가 잘려 있음(아래쪽 몇 줄이 회색일 수 있음).
- 연구 `videos`·`regions`·`dois`는 기존 research.yaml 값을 새 주제에 맞게 재배치하고, 그림 설명에 인용된 논문·원본 기사와 연결된 논문만 추가(extremes ← 10.1038/ngeo2517, modeling ← 10.1038/s41598-018-33191-7, 그림 인용 3편). 대표 그림(`image`)은 주제별 원본 그림 중 하나(엘니뇨 주제는 가로로 긴 띠 그림 대신 MJO 그림).

## 6. 바뀐 파일

- `content/news/` 새 폴더 184개(부록 A·B), 기존 4편 미변경.
- `data/research.yaml` 전체 교체(키: mechanism / ocean-atmosphere / biogeochemical / extremes / modeling), `static/research/*.jpg` 13장.
- `data/site.yaml`: `lab.tagline`, `lab.intro`, `lab.photo: img/lab-intro.jpg` 추가(contact 미변경), `static/img/lab-intro.jpg`.
- `data/presentations.yaml`: placeholder 3건 삭제 → `presentations: []`.

### 부록 A. 공지·매거진 → 뉴스 (95편)

| 폴더(content/news/) | 원본 | category | 비고 | 국문 제목(원문) |
|---|---|---|---|---|
| `2014-04-04-mbc-el-nino-interview` | notice#3 | media |  | [MBC뉴스 인터뷰] 기상이변 주범 '엘니뇨'온다...피해에 철저한 대비 필요 |
| `2014-04-science-donga-fine-dust` | notice#4 | media | 그림 1; 첨부 PDF | [과학동아 인터뷰] 내 허파에 낀 초미세먼지는 정말 중국산일까 |
| `2021-06-11-kscc-young-scientist-award` | notice#5 | award |  | 국종성 교수, 신진연구자상 수상 |
| `2014-06-13-hankookilbo-monster-el-nino` | notice#6 | media | 그림 1 | [한국일보 인터뷰] 동태평양 수온 5~6도 급등...16년 만에 몬스터 엘니뇨가 온다. |
| `2021-06-11-jeon-jaegyu-award-woo` | notice#7 | award | 그림 1 | 제4회 전재규 젊은과학자상, 포스텍 우성호 박사 우수상 수상 |
| `2014-mbc-el-nino-korea-summer` | notice#198 | media |  | [MBC뉴스 인터뷰]5년 만에 중대형급 엘니뇨 온다...한반도 여름은? |
| `2014-07-10-m-economy-el-nino-food-prices` | notice#199 | media | 첨부 PDF | [M이코노미뉴스 인터뷰] 엘니뇨와 식량가격 |
| `2014-07-15-apcc-multimodel-patent` | notice#200 | media | 그림 1 | [연합뉴스,투데이에너지 기사]APEC 기후센터 '다중모델 확률예측 기법' 특허 |
| `2014-12-22-kiost-postech-workshop-2014` | notice#201 | event | 첨부 PDF | KIOST-POSTECH JOINT WORKSHOP (2014.12.22~12.24) |
| `2015-01-28-mk-winter-drought-siberian-snow` | notice#202 | media |  | [매일경제 인터뷰]한반도 극심한 겨울가뭄...원인은 시베리아 폭설 |
| `2015-04-21-kbs-phytoplankton-arctic-warming` | notice#203 | media | doi 10.1073/pnas.1416884112 | [KBS뉴스 인터뷰]북극 급격한 온난화, 식물성 플랑크톤 증폭 탓 |
| `2015-04-21-phytoplankton-two-faces` | notice#204 | media | doi 10.1073/pnas.1416884112 | [국민일보,한국일보 외 기사]지구 온난화 해결사? 오히려 온난화 20% 증폭…식물성 플랑크톤의 '두 얼굴' |
| `2015-04-21-ytn-science-phytoplankton` | notice#205 | media | doi 10.1073/pnas.1416884112 | [YTN Science 인터뷰]식물성 플랑크톤 두 얼굴...북극 온난화 증폭 |
| `2015-kms-spring-2015-presentation-award` | notice#206 | award | 그림 2 | 김진수 연구원, 2015년도 한국기상학회 봄학술대회 우수논문발표상 수상 |
| `2015-mbc-early-summer-heat` | notice#207 | media |  | [MBC뉴스 인터뷰]올해 초여름 불볕더위 빨리 온다...엘니뇨 변수 |
| `2015-05-14-ytn-super-el-nino-18-years` | notice#208 | media |  | [YTN뉴스인터뷰]18년만의 '슈퍼 엘니뇨'온다...올여름 비상 |
| `2015-08-17-apec-science-prize` | notice#209 | award | 그림 4 | 국종성 교수, 2015 APEC 과학상 수상 |
| `2015-mbc-el-nino-droughts-floods` | notice#210 | media |  | [MBC뉴스 인터뷰]동태평양 엘니뇨 발달…세계 곳곳 가뭄·홍수 |
| `2015-08-09-kbs-jang-yeong-sil-show` | notice#211 | media | 그림 5 | [KBS 궁금한일요일 장영실쇼] 국종성 교수, 지구온난화, 슈퍼태풍이 온다? 출연 |
| `2015-08-28-mk-seawater-2c-warmer` | notice#212 | media |  | [MK 뉴스 인터뷰] 엄청난 양의 바닷물 온도 2°C나 상승…무슨 일? |
| `2015-apec-science-prize-press` | notice#213 | media | 그림 1 | [한겨레 외 기사]한국인 첫'APEC과학상'국종성 교수 |
| `2015-09-01-kbs-arctic-cold-wave-secret` | notice#214 | media | doi 10.1038/ngeo2517 | [KBS 뉴스 인터뷰] 온난화 속 ‘북극 한파’ 비밀, 한국 과학자가 풀다 |
| `2015-09-02-obs-el-nino-stronger` | notice#215 | media |  | [OBS 뉴스 인터뷰]'엘니뇨' 더 강해진다…한반도 영향은? |
| `2015-09-04-ytn-super-el-nino-second-strongest` | notice#216 | media |  | [YTN 뉴스 인터뷰]슈퍼 엘니뇨 현실로..역대 2번째 강력 |
| `2015-09-02-khan-niagara-cold-wave` | notice#217 | media | doi 10.1038/ngeo2517 | [경향신문 기사]나이아가라 폭포 얼렸던 한파 원인, 국내 과학자가 풀어 |
| `2015-09-02-veritas-alpha-cold-wave` | notice#218 | media | doi 10.1038/ngeo2517 | [베리타스 알파 기사]전남대-포항공대 한파 현상 원인 밝혀내 |
| `2015-09-02-asiae-cold-wave` | notice#219 | media | doi 10.1038/ngeo2517 | [아시아경제 기사]전남대·포항공과대 공동 연구팀,동아시아 ·북미 한파 원인 규명 |
| `2015-09-06-ytn-el-nino-grain-prices` | notice#220 | media |  | [YTN 뉴스 인터뷰]최악 엘니뇨 기상이변에 곡물가도 들썩 |
| `2015-09-07-youtube-arctic-warming-cold-winters` | notice#221 | media | doi 10.1038/ngeo2517; yt O1GXEsNF0tM | [YouTube 동영상] Two distinct influences of Arctic warming on cold winters over North America and East Asia |
| `2015-10-02-obs-seoraksan-first-ice` | notice#222 | media |  | [OBS 뉴스 인터뷰]설악산 '첫 얼음'... 올겨울 대체로 '온화' |
| `2015-11-16-obs-november-rainy-spell` | notice#223 | media |  | [OBS 뉴스 인터뷰]"11월의 장마"...매일 비 온다 |
| `2015-11-17-kbs-super-el-nino-winter` | notice#224 | media |  | [KBS NEWS 인터뷰] 이번 겨울 '슈퍼 엘니뇨' 온다... 한반도 기후는? |
| `2015-12-31-yonhap-warmest-in-42-years` | notice#225 | media |  | [연합뉴스 기사]'冬來不似冬'...42년만의 최고기온 |
| `2016-01-05-obs-la-nina-coming` | notice#226 | media |  | [OBS 뉴스 인터뷰] 동장군 귀환…'엘니뇨' 가고 '라니냐' 온다 |
| `2016-01-26-mbc-weather-shock` | notice#227 | media |  | [MBC 뉴스 인터뷰] 기록적 한파에 '웨더쇼크', 경제도 일시적 마비 |
| `2016-01-27-scientist-of-the-month-award` | notice#228 | award | 그림 3 | 국종성 교수, 한국연구재단 '이달의 과학기술자상'수상 |
| `2016-05-23-natureindex-phytoplankton-arctic` | notice#229 | media | doi 10.1073/pnas.1416884112 | 식물성 플랑크톤이 북극을 데우고 있다는 사실을 연구자들은 어떻게 밝혀냈나 |
| `2016-08-23-repi-jeju-international-conference` | notice#231 | event |  | [포항공과대학교 환경공학부주관] ‘21세기 지역의 도전과제’ 국제학술대회, 제주서 성공적 개최 |
| `2016-11-24-donga-young-scientists` | notice#232 | media |  | [동아뉴스 기사] 이 젊은 과학자들, 대한민국의 미래를 연다 |
| `2017-07-10-kim-nature-geoscience-paper` | notice#233 | paper | doi 10.1038/ngeo2986 | 김진수 박사과정 학생 , "Nature Geoscience" 지 논문 게재 |
| `2017-07-11-news1-arctic-warming-crops` | notice#234 | media | doi 10.1038/ngeo2986 | [뉴스1뉴스 기사] 포스텍 연구팀 "북극 온난화가 곡물 생산 감소 원인" |
| `2017-11-08-kaos-science-lecture` | notice#235 | media |  | [카오스 과학강연] 지구의 낯선 미래 : 설국열차 대 인터스텔라 |
| `2017-11-26-sedaily-ai-column` | notice#236 | media |  | [서울경제 사설] [Science&Market] AI 만능주의를 경계한다 |
| `2018-01-17-yonhap-el-nino-amazon-carbon` | notice#237 | media |  | [연합뉴스 기사] 엘니뇨 현상이 '지구 허파' 아마존 밀림 탄소흡수 능력 줄인다 |
| `2018-03-15-bk21-plus-award-kim` | notice#238 | award |  | 김진수 박사과정 학생, 교육부, 'BK21 플러스' 우수 연구인력 수상 |
| `2018-01-17-ytn-el-nino-amazon` | notice#239 | media |  | [YTN 뉴스 인터뷰] "엘니뇨, '지구 허파' 아마존 숨통 막는다" |
| `2018-07-27-kbs-el-nino-mechanism` | notice#240 | media |  | [KBS 뉴스 인터뷰] 이상기후 주범 ‘엘니뇨’ 가면 벗다…발생 메커니즘 최초 규명 |
| `2018-08-16-ytn-science-climate-future` | notice#241 | media |  | [YTN사이언스 인터뷰] 기후변화와 지구의 미래 |
| `2018-10-10-yonhap-enso-17-months` | notice#242 | media | doi 10.1038/s41598-018-33191-7 | [연합뉴스기사] 기상이변 원인 엘니뇨·라니냐 17개월 전 예측 가능하다 |
| `2021-08-16-lim-science-donga-feature` | notice#243 | media | 첨부 PDF | 임형규 박사과정 학생 , "과학동아 11월호"에 연구소개 |
| `2021-08-16-samsung-wealth-management` | notice#244 | media | 첨부 PDF | [삼성생명 웰스매니지먼트(Wealth Management)]기상이변 피해, 장기적인 안목의 대책이 시급하다. |
| `2018-sbs-hope-tv` | notice#245 | media |  | [SBS 희망TV 출연] 2018 창사특집 희망TV SBS 6부 출연 |
| `2018-12-national-rnd-evaluation-award` | notice#246 | award |  | 국종성 교수, 2018 국가연구개발성과평가 유공 포상 수상 |
| `2019-lim-scholarship-interview-2019` | notice#247 | media |  | 임형규 박사과정 학생, 글로벌 우수 장학생 인터뷰(2019년) |
| `2018-lim-scholarship-interview-2018` | notice#248 | media |  | 임형규 박사과정 학생, 글로벌 우수 장학생 인터뷰(2018년) |
| `2021-08-16-kim-jung-sungki-thesis-award` | notice#249 | award | 그림 1 | 김진수 박사과정 학생, 정성기논문상 수상 |
| `2021-08-16-rok-pi-clips-phase-2` | notice#250 | media |  | ROK-PI CliPS 2단계, 태평양 지역 기상 서비스 강화 |
| `2019-10-16-hankookilbo-ieodo-winter` | notice#251 | media | doi 10.1007/s13143-019-00146-5 | [한국일보기사] 올 겨울 얼마나 추울지, “이어도 인근 해수 온도 보면 미리 안다” |
| `2020-01-16-kbs-siberia-fires-fine-dust` | notice#252 | media |  | [KBS 뉴스 인터뷰] 온난화로 시베리아도 ‘활활’…한반도 초미세먼지 ‘악화’ |
| `2021-08-16-yonhap-iod-australia-fires` | notice#253 | media |  | [연합뉴스 인터뷰] 호주 산불 주범 '인도양 다이폴'…포근한 겨울 불러왔다. |
| `2020-05-11-kyongbuk-plants-arctic` | notice#254 | media | doi 10.1038/s41467-020-15924-3 | [경북일보기사]‘식물의 반란’ 식물이 숨을 안 쉬면, 북극이 녹는다 |
| `2021-08-16-earth-com-plants-arctic` | notice#255 | media | doi 10.1038/s41467-020-15924-3 | 식물이 숨을 멈추면 북극 기온이 오른다 |
| `2020-11-dongascience-science-puzzles-11` | notice#256, gsmagazine#1 | media | 첨부 PDF | 동아사이언스 2020년 11호 기획_과학난제 기사 |
| `2021-08-16-gs-caltex-tipping-points` | notice#257 | media |  | [GS칼텍스매거진] 인터스텔라와 설국열차의 지구, 그 배후의 조종자, 기후변화 티핑포인트 |
| `2020-09-09-aspire-decade-video` | notice#258 | media | yt Qs19JBTUdu8 | APEC 과학상(ASPIRE) 10년 |
| `2021-08-16-jtbc-arctic-summer-heat` | notice#259 | media |  | [JTBC 인터뷰] [날씨박사] 7월에 북극 더워지면 '여름 폭염' 강해진다 |
| `2022-01-17-etnews-no-return-to-past-climate` | notice#698 | media |  | [전자신문] 이산화탄소 줄여도 과거 기후로 돌아갈수 없다 |
| `2022-07-04-leader-researcher-selection` | notice#3297 | award |  | [한국경제기사] 윤성로 교수 등 12명 기초과학 '리더연구자' 선정 |
| `2022-08-13-mk-hottest-spring-jet-stream` | notice#3728 | media | doi 10.1038/s41558-021-01211-6 | [매일경제] '가장 뜨거운 봄'…제트기류의 심술, 이제 서막일 뿐 |
| `2023-01-11-mk-climate-engineering-column` | notice#4411 | media |  | [매일경제] 구글 올해의 검색어 1위 기후변화...지구온난화 늦출 ‘기후공학’ 고민해야 |
| `2023-05-25-fnnews-arctic-phytoplankton-decline` | notice#11156 | media | doi 10.1029/2022ef003427 | [파이낸셜뉴스] 극지연, 북극해 식물플랑크톤 IPCC 예상보다 3배 빠르게 감소 |
| `2023-05-25-newstree-arctic-phytoplankton-decline` | notice#11157 | media | doi 10.1029/2022ef003427 | [뉴스트리] "북극해 식물플랑크톤 예상보다 3배 빨리 감소" 기후 변화 영향은? |
| `2023-06-26-mediagb-extreme-el-nino` | notice#11158 | media | doi 10.1126/sciadv.adh2412 | [미디어경북] POSTECH 국종성 교수팀, 이산화탄소 감축 시기의 극한 엘니뇨 증가 예측 |
| `2023-06-26-newstube-extreme-el-nino` | notice#11159 | media | doi 10.1126/sciadv.adh2412 | [뉴스특보] "이산화탄소 줄여도 강해지는 극한 엘니뇨...기후정책 새로 정립해야 할 때" |
| `2023-07-11-sbs-europe-summer-storm` | notice#11160 | media |  | [SBS뉴스] 차도 뒷걸음질... '시속 146km' 강력 여름 폭풍 유럽 강타 |
| `2023-07-11-kbs-north-pacific-high` | notice#11161 | media |  | [KBS뉴스] 장마·폭염 만드는 ‘북태평양 고기압’, 입체 추적 |
| `2023-08-07-pohang-mbc-climate-crisis` | notice#11162 | media | yt o5CvYBhnB70 | [포항MBC] 뜨거운 지구의 경고, 기후위기│톡톡동해인 230805 방송 |
| `2023-10-26-youth-agora-national-assembly` | notice#11166 | media | yt sE2lLXcaex4 | [대학알리] 청년아고라:기후위기 국회토론회 20231019 |
| `2023-10-30-ubc-jigu-suda` | notice#11668 | media |  | [UBC울산방송] 지구수다 시즌4 소소식탁 22회 출연(2023.10.28) |
| `2024-01-19-kisti-nurion-extreme-el-nino` | notice#13431 | media | doi 10.1126/sciadv.adh2412 | [KISTI] 누리온 슈퍼컴퓨터로 수행한 이산화탄소 감축시기의 극한 엘니뇨 증가 |
| `2024-01-23-kbs-arctic-cold-warm-earth` | notice#13432 | media |  | [KBS뉴스] 북극 한파 원인은 '역대급' 따뜻한 지구 |
| `2024-02-05-kbs-heated-ocean-after-mitigation` | notice#13433 | media | doi 10.1038/s41558-024-01928-0; yt 3xaMRNKV3bU | [KBS뉴스] '열 받은 바다', 온난화 완화 후에도 반격 계속된다 |
| `2024-02-06-sbs-kuroshio-high-winter` | notice#13435 | media |  | [SBSNews] 눈과 비 잦은 이번 겨울...'쿠로시오 고기압' 길어진 영향 |
| `2025-06-25-sbs-forest-ecosystem-climate` | notice#19023 | media |  | [SBS뉴스] 산림 생태계 파괴...기후변화로 더 빨라진다 |
| `2025-08-11-kbs-life-human-extinction` | notice#19024 | media |  | [KBS Life] 머지않아 40억 명의 인류가 사라진다! 지구 온난화로 인한 인류 멸종?! |
| `2025-09-08-unrealscience-gangneung-drought` | notice#19322 | media |  | [안될과학] 강릉은 왜 가뭄에 먼저 무너졌을까? 강릉에 없는 '이것' 때문이었다?! |
| `2025-10-26-economy-science-korean-seas-winter` | notice#21418 | media |  | [이코노미사이언스] 한반도 바다 온도 이상현상, 이번 겨울 기후는 어떻게 될까? |
| `2026-05-15-nature-news-super-el-nino` | notice#22040 | media |  | [nature news article] 정말 ‘슈퍼’ 엘니뇨가 오는가? 과학이 말하는 것 |
| `2026-06-08-mbc-super-typhoon-super-el-nino` | notice#22041 | media |  | [MBC 뉴스] 슈퍼 태풍이 슈퍼 엘니뇨 방아쇠 당겼다‥역대 최강 전망까지 [기후인사이트 32 \| 인싸M] |
| `2026-06-16-youtube-weather-of-war-super-el-nino` | notice#22042 | media | yt rLo8Va_ZyGA | [YouTube 손에잡히는경제] 전쟁을 부르는 날씨, 슈퍼 엘니뇨가 온다 - 국종성 교수 (서울대 지구환경과학부) |
| `2026-06-24-nature-explainer-super-el-nino` | notice#22043 | media |  | [nature news explainer] 정말 ‘슈퍼’ 엘니뇨가 오는가? 과학이 말하는 것 |
| `2026-07-08-net-zero-speaks-interview` | notice#22044 | media |  | [YouTube] Net Zero Speaks, 국종성 교수와의 대화 |
| `2026-08-05-live-science-super-el-nino-threshold` | notice#22045 | media |  | [LIVE SCIENCE] 슈퍼 엘니뇨가 이미 압박받는 기후 생태계를 임계점 너머로 밀어낼 수 있다, 기후변화 연구자… |
| `2026-10-07-kbs-strongest-el-nino-heavy-rain` | notice#22363 | media | yt DaqKSaZQapQ | [KBS NEWS] 역대 최강 엘니뇨 온다…“다음 달부터 많은 비” |
| `2020-12-dongascience-science-puzzles-12` | gsmagazine#2 | media |  | 동아사이언스 2020년 12호 기획_과학난제 기사 |

### 부록 B. 갤러리 → 앨범 뉴스 (89편, `album: true`)

| 폴더(content/news/) | 원본 | category | 사진 | 국문 제목 |
|---|---|---|---|---|
| `2014-05-15-unist-postech-seminar` | gallery#260, portfolio#819 | event | 2 | UNIST-POSTECH 공동 세미나 |
| `2014-08-05-postech-ost-joint-workshop` | gallery#261, portfolio#874 | event | 12 | POSTECH-OST JOINT WORKSHOP |
| `2014-09-01-birthday-yeon-soo-jang` | gallery#262, portfolio#876 | lab | 3 | 장연수 연구원 생일 |
| `2014-10-01-birthday-hyunggyu-lim` | gallery#263 | lab | 2 | 임형규 연구원 생일 |
| `2014-12-01-birthday-jinsoo-kim` | gallery#264 | lab | 4 | 김진수 연구원 생일 |
| `2014-12-01-birthday-hye-young-son` | gallery#265 | lab | 2 | 손혜영 연구원 생일 |
| `2014-12-21-kiost-postech-workshop` | gallery#266 | event | 8 | KIOST-POSTECH Workshop |
| `2015-02-24-el-nino-workshop-6th` | gallery#267 | event | 10 | 제6회 엘니뇨워크샵 |
| `2015-05-27-unist-postech-joint-workshop-2nd` | gallery#268 | event | 8 | 제2회 UNIST-POSTECH Joint Workshop |
| `2015-08-28-pohang-climate-change-symposium` | gallery#269 | event | 1 | 포항 기후변화 심포지움 |
| `2015-06-18-uljin-pyeonghae-workshop` | gallery#270 | lab | 7 | 울진 평해연수원 워크샵 |
| `2015-09-29-vlecd-workshop-9th` | gallery#271 | event | 10 | The 9th workshop of the Virtual Laboratory for the Earth's Climate Diagnostics Program, and the University Allied Workshop |
| `2015-12-20-nuist-postech-workshop` | gallery#272 | event | 2 | NUIST-POSTECH Workshop |
| `2016-02-01-gyeongju-climate-change-workshop` | gallery#273 | event | 2 | 경주 기후변화 공동워크샵 |
| `2016-04-09-gyeongju-cherry-blossom-marathon` | gallery#274 | lab | 4 | 경주 벚꽃 마라톤 |
| `2016-05-11-scientist-of-the-month-ceremony` | gallery#275 | award | 4 | 이달의 과학기술자상 시상식 |
| `2016-07-20-kiost-postech-ulleungdo-workshop` | gallery#276 | event | 4 | KIOST-POSTECH 울릉도 공동세미나 및 워크샵 |
| `2016-10-31-kms-fall-meeting` | gallery#277 | event | 4 | 2016년 한국기상학회 가을학술대회 |
| `2016-06-02-unist-postech-seminar` | gallery#278 | event | 6 | UNIST-POSTECH 공동세미나 |
| `2016-12-12-fei-fei-jin-agu-fellow-banquet` | gallery#279 | event | 3 | Prof. Fei-Fei Jin AGU Fellow Honor's Banquet |
| `2016-12-20-nuist-postech-workshop` | gallery#280 | event | 5 | NUIST-POSTECH Workshop |
| `2017-02-01-gangneung-workshop` | gallery#281 | event | 5 | 강릉 Workshop |
| `2017-02-01-birthday-jaeheung-park-diah` | gallery#282 | lab | 3 | 박재흥, 디아 연구원 생일 |
| `2017-02-10-postech-commencement` | gallery#283 | event | 4 | 2016학년도 POSTECH 학위수여식 |
| `2017-02-23-postech-hanyang-yonsei-cnu-workshop` | gallery#284 | event | 1 | POSTECH-한양대-연세대-전남대 공동 워크샵 |
| `2017-06-01-unist-postech-seminar` | gallery#285 | event | 9 | UNIST-POSTECH 공동세미나 |
| `2017-07-19-shipboard-seminar` | gallery#286 | event | 4 | 해양과학기지 및 관할해역 연구 선상세미나 |
| `2017-08-20-international-monsoon-workshop` | gallery#287 | event | 4 | 국제 몬순 워크샵 |
| `2017-12-19-nuist-postech-cityu-workshop-3rd` | gallery#288 | event | 7 | 3rd NUIST-POSTECH-CITYU Joint Workshop |
| `2018-01-17-kiost-postech-yangsan-workshop` | gallery#289 | event | 5 | KIOST-POSTECH 양산 공동세미나 및 워크샵 |
| `2018-02-09-postech-commencement` | gallery#290 | event | 3 | 2017학년도 POSTECH 학위수여식 |
| `2018-02-13-utokyo-postech-workshop` | gallery#291 | event | 7 | UTOKYO-POSTECH Joint Workshop |
| `2018-03-16-bk21-plus-award-ceremony` | gallery#292 | award | 4 | 2017년도 BK21플러스 사업 우수 참여인력 시상식 |
| `2018-05-17-unist-postech-seminar` | gallery#293 | event | 5 | UNIST-POSTECH 공동세미나 |
| `2018-12-28-national-rnd-evaluation-award` | gallery#294 | award | 4 | 2018 국가연구개발성과평가 유공 포상 수상 |
| `2019-02-08-jinsoo-kim-jung-sungki-award` | gallery#295 | award | 4 | 김진수 박사 정성기 논문상 수상 |
| `2019-07-19-mueunjae-chair-professor` | gallery#296 | award | 6 | 국종성 교수 무은재 석좌교수 추대식 |
| `2019-09-28-woohyun-yang-wedding` | gallery#297 | lab | 3 | 양우현 졸업생 결혼식 |
| `2018-12-16-nuist-cityu-postech-workshop` | gallery#298 | event | 5 | NUIST-CITYU-POSTECH Joint Workshop |
| `2019-01-15-postech-cnu-workshop` | gallery#299 | event | 5 | POSTECH-CNU Joint Workshop |
| `2019-02-11-enso-workshop` | gallery#300 | event | 4 | ENSO Workshop |
| `2019-04-21-kms-spring-meeting-climate` | gallery#301 | event | 3 | 봄 기상학회 기후분과 |
| `2019-05-15-teachers-day` | gallery#302 | lab | 4 | 스승의 날 |
| `2019-06-23-unist-postech-seminar` | gallery#303 | event | 4 | UNIST-POSTECH 공동세미나 |
| `2019-06-27-oasis-research-meeting` | gallery#304, portfolio#880 | event | 4 | OASIS 학술발표회 |
| `2019-07-03-kgu-annual-meeting` | gallery#305, portfolio#878 | event | 3 | Korea Geoscience Union 학술대회 |
| `2019-08-26-irreversible-climate-change-workshop` | gallery#306 | event | 4 | Irreversible Climate Change Workshop |
| `2019-10-30-kms-fall-meeting` | gallery#307 | event | 3 | 가을 기상학회 |
| `2019-12-18-nuist-cnu-postech-workshop-4th` | gallery#308 | event | 5 | 4th NUIST-CNU-POSTECH Joint Workshop |
| `2019-02-09-phd-graduation-jinsoo-kim-hyunggyu-lim` | gallery#309, portfolio#907 | event | 4 | 김진수, 임형규 박사 졸업식 |
| `2019-11-21-tvn-problematic-men` | gallery#310 | media | 3 | tvN 문제적남자 |
| `2020-02-03-postech-snu-kopri-workshop` | gallery#311 | event | 8 | POSTECH-SNU-KOPRI Joint Workshop |
| `2020-02-07-ms-graduation-dayeong-kim-so-won-park` | gallery#312, portfolio#882 | event | 8 | 김다영, 박소원 석사 졸업식 |
| `2021-12-20-leader-researcher-appointment` | gallery#694 | award | 2 | 차세대 리더연구자 임명장 수여식 |
| `2021-12-20-science-article-photo-shoot` | gallery#696, portfolio#6129 | lab | 6 | science 기사 촬영 |
| `2022-04-27-kms-spring-meeting-climate` | gallery#3298 | event | 5 | 봄 기상학회 기후분과 |
| `2022-05-01-seoul-outing` | gallery#3299 | lab | 2 | 서울 나들이 |
| `2022-07-06-postech-ysu-climate-workshop` | gallery#3727 | event | 2 | POSTECH-YSU Joint Workshop on Climate |
| `2022-08-17-kgu-annual-meeting` | gallery#3729 | event | 16 | KGU 연례학술대회 |
| `2022-10-19-kms-fall-meeting` | gallery#3956 | event | 13 | 한국기상학회 가을학술대회 |
| `2022-11-02-kso-fall-meeting` | gallery#4640 | event | 4 | 한국해양학회 추계학술대회 |
| `2023-01-17-ircc-kist-iprc-workshop` | gallery#5855 | event | 6 | IRCC-KIST-IPRC Joint workshop |
| `2023-04-19-fei-fei-jin-visit` | gallery#9982 | lab | 1 | Fei-Fei Jin 교수님 방문 |
| `2023-04-18-kms-spring-meeting` | gallery#11153 | event | 13 | 한국기상학회 춘계학술대회 |
| `2023-05-18-international-workshop-climate-system` | gallery#11154 | event | 1 | International Workshop on Climate system |
| `2023-05-16-unist-postech-seminar` | gallery#11155 | event | 13 | UNIST-POSTECH 공동세미나 |
| `2023-08-17-high-latitude-climate-workshop` | gallery#11163 | event | 4 | Workshop on High-latitude Earth Climate System |
| `2023-08-18-phd-graduation-kyung-min-noh` | gallery#11164 | event | 8 | 노경민 박사 졸업식 |
| `2023-08-28-kgu-annual-meeting` | gallery#11165 | event | 8 | KGU 연례학술대회 |
| `2023-10-19-national-assembly-climate-forum` | gallery#11167 | event | 3 | 기후위기 국회토론회 |
| `2023-11-01-kms-fall-meeting` | gallery#11669 | event | 10 | 한국기상학회 추계학술대회 |
| `2023-11-01-kso-fall-meeting` | gallery#11670 | event | 7 | 한국해양학회 추계학술대회 |
| `2023-11-22-kscc-annual-meeting` | gallery#11671 | event | 2 | 한국기후변화학회 |
| `2023-12-04-climate-engineering-forum` | gallery#11672 | event | 8 | 기후위기와 기후공학 포럼 |
| `2024-01-11-winter-workshop-abrupt-climate-change` | gallery#13430 | event | 12 | Winter Workshop on Abrupt climate change |
| `2024-02-02-postech-commencement` | gallery#13434 | event | 19 | 2024학년도 POSTECH 학위수여식 |
| `2024-02-18-ocean-sciences-meeting` | gallery#13436 | event | 2 | Ocean Sciences Meeting |
| `2024-04-22-korea-nordic-strategic-seminar` | gallery#15002 | event | 3 | Korea-Nordic Strategic Seminar |
| `2024-04-29-kms-spring-meeting` | gallery#15003 | event | 6 | 한국기상학회 봄학술대회 |
| `2024-07-01-kgu-annual-meeting` | gallery#16318 | event | 9 | KGU 연례학술대회 |
| `2024-07-16-summer-workshop-abrupt-climate-changes` | gallery#19014 | event | 4 | Summer Workshop on Abrupt climate changes |
| `2024-08-21-utokyo-snu-yonsei-workshop` | gallery#19015 | event | 5 | 2024 UTokyo-SNU-Yonsei Joint Workshop on Earth System Interaction under Changing Climate |
| `2024-10-09-permafrost-wildfire-workshop` | gallery#19016 | event | 4 | Response and Feedback of Arctic-boreal Permafrost and Wildfires to Climate Change Workshop |
| `2024-12-17-china-japan-korea-forum` | gallery#19017 | event | 1 | China-Japan-Korea Ocean and Earth System Science Forum |
| `2025-02-24-snu-kopri-high-latitude-workshop` | gallery#19018 | event | 5 | SNU-KOPRI Joint Workshop on High-latitude climate changes |
| `2021-06-18-ski-trip` | portfolio#903 | lab | 1 | 최상급자 전용 스키체험 |
| `2021-06-18-drone-filming` | portfolio#905 | lab | 1 | 드론촬영 |
| `2022-02-16-kso-fall-meeting-22` | portfolio#6174 | event | 1 | 22년 해양학회 추계학술대회 |
| `2024-01-29-csl-group-photo` | portfolio#17411, portfolio#17414 | lab | 2 | CSL 단체 사진 |
