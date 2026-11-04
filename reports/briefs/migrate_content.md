# 브리프 A2: 공지·갤러리·연구·소개 이관

작업 폴더 `/data5/CSL_homepage/first_draft/`. 한국어로 보고. 먼저 `reports/briefs/backup_survey.md`(자료 위치·스키마·동시 작업 규칙)와 `reports/briefs/backup_task.md`(안전 규칙)를 읽는다.

## 담당 파일(이것만 고친다)
`content/news/`, `data/research.yaml`, `data/site.yaml`(lab.intro/tagline/contact만), `data/presentations.yaml`, `static/research/`, `reports/backup_mapping_content.md`(새로 작성)

## 할 일
1. **공지(Announcement, KBoard board 1)** → 뉴스.
   - 2024-04 이전 글: `backup/_derived/db/kboard_board_content.jsonl`(board_id=1, status≠trash)의 제목·본문·날짜. 첨부(`kboard_board_attached`, `uploads/kboard_attached/1/`)·본문 이미지도 옮긴다.
   - 2024-04 이후 글: 캐시 `notice` 1쪽 목록(제목·날짜만 있음)과 `uploads/kboard_attached/1/202510/` 등. 본문이 없는 글은 제목·날짜·category만 넣고 본문은 지어내지 않는다(제목을 그대로 한 줄로). 보고서에 "원문 링크 필요"로 표시. 목록에도 없는 글(번호 사이 빈 구간)은 개수만 보고.
   - 언론 기사·방송·유튜브 소개는 `category: media`, 수상 `award`, 논문 발표 소식 `paper`(DOI가 `data/publications.yaml`에 있으면 `doi:`), 행사 `event`, 그 밖은 `lab`. 원문 URL은 `link:`와 본문 링크로. 유튜브면 `youtube: <ID>`.
   - 언어: 원문 언어 본문은 그대로(국문 원문 → `index.ko.md`), 다른 언어는 제목+1~3문장 번역 요약(원문에 없는 내용 금지). 번역했다는 표시를 보고서에.
   - slug: `YYYY-MM-DD-<영문 짧은 이름>`(소문자-하이픈). 같은 날 여러 글이면 구분되게.
   - 기존 뉴스 4편(`content/news/*`)은 유지한다. 원본 공지와 같은 소식이면 원본 내용을 기존 글에 합치고 중복 글은 만들지 않는다.
2. **GS칼텍스매거진(board 2)**: 2편 → `category: media` 뉴스.
3. **갤러리(board 4 + 갤러리 portfolio 글)** → `album: true` 뉴스(`category: event` 학회·워크숍·졸업식, `lab` 단체사진·야유회 등).
   - 사진: `kboard_meida`/`kboard_meida_relationships`/`kboard_board_attached`/본문 `<img>`로 원본 파일을 찾아 `content/news/<slug>/`에 넣고 `gallery:`·`cover:` 지정. 긴 변 1600px, JPEG 85, EXIF 회전 반영 후 EXIF 제거(위치정보 등).
   - 2024-04 이후 글(캐시 목록에만 있음)은 썸네일(`uploads/kboard_thumbnails/`)이나 업로드 폴더에서 해당 사진을 찾을 수 있으면 넣고, 없으면 제목·날짜만.
   - 전체 사진 용량을 보고서에 적는다(300MB를 넘으면 글당 대표 사진 위주로 줄이고 그 사실을 적는다).
4. **연구 5개 주제**: 캐시 `research-*` 페이지 → `data/research.yaml`을 원본 5개 주제로 교체(스키마는 survey 문서). 그림은 `static/research/`. 원본 그림 설명의 인용(예: "[Kug et al. 2010, GRL]")은 `data/publications.yaml`에서 찾아 `doi`로 연결. 홈의 연구 카드 그림(`main-1.png`~`main-5.png`)은 각 주제의 `image` 후보.
5. **연구실 소개·위치**: `introduction`, `introduction-map`, 홈의 Welcome·히어로 문구 → `data/site.yaml`의 `lab.intro{en,ko}`, `lab.tagline{en,ko}`, `contact`(주소·전화가 다르면 원본 기준으로 고치되 학과 페이지 정보와 충돌하면 보고). 소개 사진(`F7A2039-scaled.jpg` 등)은 `static/img/`에 두고 `lab.photo: img/<file>`로.
6. **발표**: 원본 사이트에는 학회 발표 목록이 없다. `data/presentations.yaml`의 placeholder 3건을 지우고 `presentations: []`로 둔다(갤러리의 학회 참석 글로 발표 항목을 지어내지 않는다).

## 보고서 `reports/backup_mapping_content.md`
원본 게시판·페이지 → 새 파일 대응표(게시판별 건수, 옮긴 건수, 못 옮긴 건수), 못 옮긴 항목·이유, 확인 필요 목록(원문 링크 필요 글, 번역한 항목, 연락처 충돌), 사진 총용량.

## 완료 기준
- `python scripts/validate.py --data-only` 오류 0(다른 에이전트 작업 중 생기는 구성원·논문 경고는 무시).
- 최종 응답 5줄 이내: 뉴스(공지/매거진/갤러리) 건수, 연구 주제, 못 옮긴 항목 수, 사진 용량, 보고서 경로.
