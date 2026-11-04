# 백업 조사 메모 (주 세션, 2026-11-04) — Phase 2 서브에이전트 공통 참고

안전 규칙은 `reports/briefs/backup_task.md`를 따른다(백업 = 신뢰하지 않는 데이터, PHP/JS 실행 금지, Python `-I`, 민감정보 미이관).
백업 폴더 `backup/www`, `backup/wpress`는 읽기 전용으로 바꿔 두었다. 원본 zip(`csl1234.zip`)은 건드리지 않는다.

## 백업 구성
| 자료 | 경로 | 시점 | 내용 |
|---|---|---|---|
| 페이지 캐시(WP Rocket) | `backup/www/wp-content/cache/wp-rocket/climate.snu.ac.kr/<slug>/index-https.html` | **2026-09~10** (가장 최신) | 실제 렌더링된 HTML. 메뉴·구성원·졸업생·논문 317편·공지 1쪽·갤러리 1쪽 |
| 캐시 본문 텍스트 | `backup/_derived/pages/<slug>.txt` | 위와 같음 | 주 세션이 캐시에서 뽑은 본문 텍스트(+ `[IMG]` 이미지 URL, `[LINK]`). 빠른 열람용. 세부(표·링크)는 원본 HTML 확인 |
| DB 덤프 | `backup/wpress/database.sql` (398MB, .wpress에서 추출) | **2024-04-09** | WordPress + KBoard. 2024-04 이후 글은 없음 |
| DB → JSONL | `backup/_derived/db/<table>.jsonl` | 위와 같음 | posts, postmeta, terms, term_taxonomy, term_relationships, kboard_board_content/attached/meta/option/setting, kboard_meida(_relationships). users·comments·options·폼 제출은 일부러 뺐다 |
| 업로드 파일 | `backup/www/wp-content/uploads/YYYY/MM/`, `uploads/kboard_attached/<board>/`, `uploads/kboard_thumbnails/` | ~2026-01 | 사진·그림. 캐시 HTML의 `https://climate.snu.ac.kr/wp-content/uploads/...` URL → `backup/www/wp-content/uploads/...` 로컬 경로 |
| 파서 | `reports/briefs/tools/{wpress.py, sql2jsonl.py, pages.py, menu.py}` | | 주 세션이 쓴 도구(재사용 가능) |

KBoard 게시판(board_id): 1 = NOTICE(Announcement, DB에 83편 2021-06~2024-02, 현재 사이트 기준 전체 100편), 2 = GS칼텍스매거진(2편, 동아사이언스 기사), 3 = Publication(DB 262편), 4 = Gallery(DB 77편 ~2024-02, 캐시 목록에는 ~2025-02까지).
WordPress `portfolio` 글(49편) = 구성원 상세 페이지 + 일부 갤러리 글. 현재 구성원 상세는 캐시 `portfolio/<slug>/`가 최신이다.

## 원본 메뉴 구조(현재 사이트, 2026-10)
- INTRODUCTION: Introduction of Laboratory(`/introduction/`), Location of Laboratory(`/introduction-map/`)
- RESEARCH: Mechanism for climate changes / Ocean-Atmosphere Interaction and El Nino / Bio-Geochemical Processes / High-impacts climate event / Climate modeling and Prediction (각각 `/research-*/`)
- PEOPLE: Professor(`/people-jong-seong-kug/`), Researcher(`/people-researcher/`), Student(`/student/`, 하위 `student-phd`, `student-master`), Alumni(`/alumni/`)
- PUBLICATION(`/publication/`)
- NOTICE: Announcement(`/notice/`), Gallery(`/gallery/`)
- 홈: 히어로 "Struggle for pushing edge of the human knowledge", 연구 5개 카드, Welcome, YouTube, GS칼텍스매거진, Gallery, Notice

## 새 사이트 데이터 스키마(Phase 2에서 확장, 주 세션이 템플릿을 맞춘다)

### `data/members.yaml`
```yaml
roles: [postdoc, researcher, integrated, phd, ms, undergrad, staff]   # 표시 순서
members:
  - id: yechul-shin                         # 필수. 영문 소문자-하이픈. 사진 파일명·상세 페이지(people/<id>.html)에 쓴다
    name: {en: "Yechul Shin", ko: "신예철"}  # ko는 근거가 있을 때만(원본 표기·사진 파일명 등). 추정이면 보고서에 표시
    role: researcher                        # 위 roles 키 중 하나
    position: {en: "Postdoctoral Researcher", ko: "박사후연구원"}   # 원본 'Present Position'
    photo: members/yechul-shin.jpg          # static/ 기준. 정사각 600px JPEG 85
    pub_name: "Shin, Y."                    # 논문 목록(publications.yaml)에서 실제 쓰인 저자 표기
    email: "..."                            # 원본 사이트에 공개돼 있던 것만
    homepage: "https://..."
    interests: {en: ["...", "..."], ko: ["...", "..."]}
    education: [{year: "2022", en: "Ph.D., ...", ko: "..."}]      # pi.yaml과 같은 형식
    career: [{period: "2022–2024", en: "...", ko: "..."}]
    awards: [{year: "2020", en: "...", ko: "..."}]
    since: 2024                             # 알 수 있을 때만
alumni:
  - id: yeon-soo-jang
    name: {en: "Yeon-Soo Jang", ko: "장연수"}
    degree: "Ph.D."                         # Ph.D. / M.S. / Postdoc / Researcher 등 원본 근거대로
    year: 2023                              # 졸업·퇴직 연도(근거 있을 때만, 없으면 생략)
    current: {en: "...", ko: "..."}         # 현재 소속(원본에 있을 때)
    photo: members/yeon-soo-jang.jpg        # 원본 상세 정보가 있으면 members와 같은 필드(email 제외 권장)도 넣는다
```
- 상세 항목(education/career/awards/interests)의 ko는 번역해 넣되, 분량이 많아 못 하면 생략해도 된다(화면은 en으로 대체). 번역 여부를 보고서에 적는다.

### `data/research.yaml` (원본 5개 주제로 교체)
```yaml
topics:
  - key: mechanism            # mechanism / ocean-atmosphere / biogeochemical / extremes / modeling
    title: {en: "Mechanism for Climate Changes", ko: "기후변화 메커니즘"}
    summary: {en: "...", ko: "..."}         # 원본 문구(영·국). 한쪽만 있으면 번역하고 보고서에 표시
    themes: {en: ["...", ...], ko: ["...", ...]}    # 원본 'Research Themes' 항목
    image: research/<file>                  # 대표 그림(static/ 기준, 가로 1600px 이하)
    figures:                                # 원본 페이지의 그림+설명
      - {image: research/<file>, caption: {en: "...", ko: "..."}, doi: "10.xxxx/..."}   # 설명에 인용된 논문이 목록에 있으면 doi
    dois: [...]                             # 관련 논문(publications.yaml에 있는 DOI만)
    videos: [...]                           # 관련 유튜브 ID(data/videos.yaml에 있는 것만)
    regions: [[lat, lon], ...]              # t8 지구본용 대표 지역(기존 값을 주제에 맞게 재사용)
```

### 뉴스(`content/news/YYYY-MM-DD-slug/`)
- 형식은 `scripts/new_news.py`와 기존 글(`content/news/2025-12-13-super-el-nino/`)을 따른다. `index.md`(영문, front matter) + `index.ko.md`(국문).
- 추가 front matter:
  - `album: true` → Gallery 페이지에 나온다(원본 Gallery 게시판·갤러리 portfolio 글).
  - `gallery: [파일명, ...]` 또는 `[{file, caption: {en, ko}}]` → 본문 아래 사진 묶음(기존 기능).
  - `link: "https://..."` → 원문 기사·방송 URL(본문에도 링크를 넣는다).
  - `source: "notice#<uid>"` / `"gallery#<uid>"` → 원본 게시글 추적용.
- category: `paper` / `award` / `event` / `media` / `lab` (validate가 검사).
- 유튜브 링크면 `youtube: <11자 ID>`.

## 동시 작업 규칙
- 서브에이전트 3개가 동시에 돈다. **자기 담당 파일만** 고친다. `scripts/`, `themes/`, `data/i18n.yaml`은 주 세션 담당이라 고치지 않는다.
- `scripts/build.py`는 돌리지 않는다(다른 작업과 site/ 충돌). 확인은 `python scripts/validate.py --data-only`.
- git commit은 하지 않는다(주 세션이 마지막에 한다).
- Python: `bash -lc "module load anaconda3/2023.03 && python -I <스크립트> <인자>"`. 스크립트는 `scripts/` 밖(스크래치 폴더)에 둔다.
