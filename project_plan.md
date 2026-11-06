# 기후시스템연구실(국종성 교수) 홈페이지 — project_plan

## Context
- climate.snu.ac.kr이 외부에서 접속되지 않는다. 이 서버(SNU 대역)에서도 403이 나고, Internet Archive도 현재 내려가 있다. 원본 백업은 약 2시간 뒤에 받는다.
- 목표: 어떤 웹서버에도 올릴 수 있는 **순수 정적 HTML** 사이트. 배포 방식은 백업을 보고 나중에 정한다.
- 콘텐츠 관리 방식: 학생이 Claude에게 정보를 주면 Claude가 **데이터 파일(YAML/Markdown)만** 고치고 빌드한다. HTML은 직접 고치지 않는다.
- 언어: 영문을 기본으로 하고 국문 토글(`/`, `/ko/`)을 둔다.
- 지금(백업 전): 데이터 구조와 빌드 시스템을 만들고, 템플릿 8종과 교수님 전체 논문 목록을 만든다. 백업이 오면 실제 콘텐츠를 옮기고 기본 형식(basic 테마)을 완성한다.
- 확인된 공개 정보: 학과 교수 페이지(학력·경력·연락처·대표 논문), ORCID `0000-0003-2251-2579`, OpenAlex `A5091389074`, YouTube `@climatesystemlaboratory5423`.

## Global Constraints
| 항목 | 값 |
|---|---|
| 작업 폴더 | `/data5/CSL_homepage/first_draft/` |
| 빌드 | Python 3.10 (anaconda3/2023.03) + Jinja2 3.1 + PyYAML + markdown. 실행은 `bash -lc "module load anaconda3/2023.03 && python scripts/build.py --theme all"` |
| 산출물 | `site/<theme>/`: 상대경로로 연결해 서버에서도, 파일을 더블클릭해서도(file://) 열린다. 외부 JS 라이브러리는 테마 assets에 vendoring한다 |
| 언어 | EN = `site/<theme>/`, KO = `site/<theme>/ko/`. UI 문자열은 `data/i18n.yaml`, 콘텐츠는 `{en, ko}` 필드(ko가 없으면 en으로 대체) |
| 논문 표시 | 최신 논문이 맨 위. 번호는 가장 오래된 논문 = 1, 최신 = N이며 빌드할 때 자동으로 매긴다. 연도별 섹션은 내림차순, 같은 해 안에서는 출판일 내림차순 |
| 논문 범위 | 동료심사 학술지 논문(article/review)만 넣는다. preprint·erratum·학회초록·dataset·peer-review는 뺀다 |
| 버전 관리 | `first_draft/`에서 `git init`(로컬 전용, push 안 함). Claude 수정이 잘못되면 되돌릴 수 있게 한다 |

## 폴더 구조
```
first_draft/
  CLAUDE.md               # 콘텐츠 관리 가이드(학생 요청 → Claude가 수정하는 절차)
  project_plan.md         # 이 계획의 사본(PLAN.md 이중 저장)
  data/  site.yaml pi.yaml members.yaml research.yaml publications.yaml
         presentations.yaml videos.yaml i18n.yaml
  content/news/YYYY-MM-DD-slug/{index.md, index.ko.md, 그림·영상썸네일}
  static/{img,members,research}/
  themes/_shared/         # 공통 매크로(논문 항목, 뉴스 카드, YouTube facade, 언어 토글)
  themes/{basic,t1..t8}/{templates/*.html, assets/}
  scripts/ build.py validate.py fetch_publications.py add_publication.py
           fetch_youtube.py new_news.py
  site/ gallery/index.html + 테마별 빌드 결과
  backup/                 # 원본 백업(읽기 전용, 신뢰하지 않는 데이터로 취급)
  reports/                # pubs_reconciliation.md, verification_report.md
/data5/CSL_homepage/.claude/CLAUDE.md   # 프로젝트 오버라이드(## PLAN, ## VERIFICATION: 연구용 문서 3종 생략) + first_draft/CLAUDE.md 안내
```
모든 테마가 같은 페이지 세트를 같은 데이터로 렌더링한다: Home, Research, People, Publications, Presentations, News(목록·상세), Videos, Contact. 그래서 나중에 기능을 추가할 때 데이터·스크립트 쪽만 늘리면 모든 테마에 반영된다.

## Tasks

### Phase 1 — 백업 전(지금)

**Task 1: 골격 + 데이터 스키마 + build.py + validate.py** (주 세션, Opus 5.5)
- 위 폴더 구조와 YAML 스키마를 만들고, 학과 페이지의 공개 정보(교수 프로필·연락처 501동 522호/507호, 대전공·연구내용)를 넣는다.
- `build.py`: 테마를 선택해 EN/KO 두 언어로 렌더링한다. 논문 번호 매기기, 연도별 그룹, 홈 화면 "Latest" 피드(뉴스+논문+발표를 날짜순으로 섞음), 갤러리 페이지 생성까지 한다.
- `validate.py`: 스키마 검사, DOI 중복, 번호 assert(1..N 연속, 최신이 맨 위), 내부 링크·이미지 깨짐, KO 누락 경고.
- 완료 기준: 최소 테마(basic 골격)로 빌드가 끝나고, 16개 페이지(8×2언어)가 생성되고, validate가 0 error.

**Task 2: 국종성 교수 전체 논문 수집** (서브에이전트, Opus 5.5 — Task 1의 스키마만 있으면 Task 3과 병렬)
- `fetch_publications.py`: ORCID(270편) ∪ OpenAlex(article 435건, 중복·오귀속 포함) ∪ Crossref(저자명 검색) → DOI로 중복 제거 → Crossref 메타데이터로 정규화(저자, 제목, 학술지, 권·쪽, 출판일) → 저자 목록에 Kug가 있는지 확인 → 제외 유형 필터.
- 출처가 1곳뿐이거나 저자 확인이 애매한 항목은 `needs_review: true`로 표시하고 기본 화면에서는 숨긴다.
- 완료 기준: `data/publications.yaml` 생성, `reports/pubs_reconciliation.md`(출처별 개수, 교집합, 제외 사유별 개수, 검토 필요 목록). 학과 페이지 대표 논문 5편이 모두 들어 있다(assert).

**Task 3: 템플릿 8종** (서브에이전트 4개 × 2테마, Opus 5.5, 병렬. 테마 폴더가 분리돼 있어 충돌 없음)
| # | 이름 | 콘셉트 |
|---|---|---|
| t1 | Classic Academic | SNU 네이비 + 세리프 제목, 상단 메뉴. 전통적인 대학 연구실 |
| t2 | Modern Minimal | 넓은 여백, Pretendard/Inter, 흑백 + 포인트색 1개, 에디토리얼 타이포 |
| t3 | Ocean–Atmosphere | 해수면온도 팔레트의 풀스크린 그라디언트 히어로, 반투명 카드 |
| t4 | Climate Dashboard | 다크 테마, warming stripes 배너(실제 전지구 기온 편차 데이터, 출처 표기), 수치·지표 카드 |
| t5 | Science Magazine | 뉴스 우선 레이아웃. 대형 그림 카드, 연구 하이라이트와 영상을 전면에 |
| t6 | Sidebar Portfolio | 고정 좌측 사이드바 + 우측 스크롤 본문(al-folio 계열) |
| t7 | One-page Scroll | 단일 긴 페이지 + 스티키 내비, 모바일 우선. 상세 페이지는 별도 |
| t8 | Interactive Globe | 회전하는 지구본 히어로(d3-geo, vendoring)에 연구 지역 표시, 대담한 현대 스타일 |
- 공통 요구: 반응형(폰 폭 16px 거터), 라이트/다크 대응, KO/EN 토글, 논문 연도 섹션·번호 규칙 준수, YouTube는 클릭해야 로드되는 facade(youtube-nocookie) 사용.
- 완료 기준: 테마마다 빌드 성공, validate 0 error, 16개 페이지 생성.

**Task 4: 관리 도구 + Claude 관리 가이드** (주 세션)
- `add_publication.py <DOI>`: Crossref에서 메타데이터를 받아 추가하고 중복을 검사한다.
- `fetch_publications.py --new`: 마지막 갱신 이후 새 논문을 탐지해 후보만 보고한다(자동 추가 안 함).
- `new_news.py`: 뉴스 폴더 골격을 만든다. front matter: `title{en,ko}`, `date`, `category`(paper/award/event/media), `doi`(논문 항목과 자동 연결), `cover`, `youtube`, `gallery`.
- `fetch_youtube.py`: 채널 RSS에서 최신 영상을 받아 `videos.yaml`을 갱신한다(featured 수동 지정 유지).
- 발표 추가는 `presentations.yaml` 항목(date, event, location, title, presenters, type: oral/poster/invited)으로 한다.
- `first_draft/CLAUDE.md`: 요청 유형별(논문/뉴스/발표/구성원/영상) 수정 위치 → build → validate → git commit 절차, HTML 직접 수정 금지.
- 완료 기준: 각 스크립트를 실제 DOI 1건과 테스트 뉴스 1건으로 실행해 반영되는지 확인하고, 테스트 항목은 삭제한다.

**Task 5: 갤러리 + 미리보기**
- `site/gallery/index.html`: 9종(basic + t1..t8)의 썸네일·설명·링크.
- 스크린샷은 서버에 브라우저가 없으므로 Playwright chromium을 사용자 영역에 설치해 시도한다. 실패하면 iframe 미리보기로 대체한다.
- 미리보기는 서버에서 `python -m http.server`로 띄우거나 파일을 직접 연다. 대표 화면 스크린샷은 SendUserFile로 보낸다.

### Phase 2 — 백업 수신 후

**Task 6: 백업 분석·이관** (서브에이전트, Opus 5.5)
- `backup/`에 압축을 풀고 PHP/JS는 실행하지 않고 파싱만 한다. 형식(WordPress DB 덤프 / HTML 미러 / 기타)에 맞게 메뉴 구조, 구성원·졸업생, 연구 주제, 사진, 뉴스, 발표, 논문 목록을 추출해 data/content로 옮긴다.
- 완료 기준: `reports/backup_mapping.md`(원본 페이지 → 새 데이터 파일 대응표, 옮기지 못한 항목 목록).

**Task 7: 논문 목록 대조**
- 백업의 연구실 논문 목록과 Task 2 결과를 대조한다. 백업에만 있는 항목은 추가하고, 교신저자(CA) 표기와 연구실 구성원 굵게 표시를 반영하고, `needs_review` 항목을 해소한다.
- 완료 기준: reconciliation 보고서를 갱신하고 미해결 0건(또는 사용자 확인 목록으로 넘김).

**Task 8: 기본 형식(basic 테마) 완성**
- 원본 사이트의 메뉴 구성과 정보 배치를 따르되 현대적으로 정돈한다. 이어서 9종 전체를 다시 빌드한다.

## Verification
1. 모든 테마 `build.py --theme all`이 성공하고 `validate.py`가 0 error(번호·정렬 assert, 링크·이미지, 스키마, EN/KO 페이지 수 일치).
2. 논문: 3개 출처 교차 대조 보고서, 대표 논문 5편 포함, 무작위 10편의 Crossref 메타데이터 일치 확인.
3. 화면: 테마별 데스크톱·모바일 스크린샷을 별도 서브에이전트(Opus 5.5)가 확인한다(겹침, 넘침, 다크모드, KO 토글).
4. Codex 로그인 상태면 build/validate 스크립트를 교차 리뷰한다. 안 되어 있으면 `reports/verification_report.md`에 "Codex 미실시"를 적는다.
5. 결과는 `reports/verification_report.md`에 정리하고, 작업이 끝나면 Notion "Working Note"에 기록한다(대표 스크린샷 1장).

## 진행 기록
- 2026-11-03 Phase 1 완료(Task 1~5 + Verification). 결과: `reports/verification_report.md`
- 계획 대비 변경: 갤러리는 `site/gallery/index.html` 대신 **`site/index.html`**. 논문 `needs_review` 기준은 "출처 1곳"이 아니라 **Crossref 저자 확인 실패·유형 애매**(단일 출처라도 Crossref로 Kug 저자·학술지 논문이 확인되면 표시, 보고서에 목록화 — 실제 단일 출처 0편). 레이아웃 검사 스크립트 `scripts/check_layout.mjs` 추가. 경미한 디자인 문제 16건은 최종 테마 선택 후 해당 테마만 수정.
- Phase 2 작업 지시서: `reports/briefs/backup_task.md`
- 2026-11-04 Phase 2 완료(Task 6~8). 백업 = WordPress 전체(캐시 2026-10 + DB 2024-04 + uploads). 서브에이전트 3개 병렬(구성원 / 공지·갤러리·연구 / 논문 대조), 주 세션은 빌드 확장 + basic 재구성. 결과: `reports/backup_mapping.md`, `reports/verification_report.md`
- Phase 2 변경: Gallery는 별도 콘텐츠 형식 대신 뉴스에 `album: true`. 선택 페이지 기능(`theme.yaml` extra_pages, `member.html`→`people/<id>.html`, `research_topic.html`→`research/<key>.html`)은 basic만 사용(다른 테마는 기존 8페이지). 구성원 굵게 표시는 정확 일치 + 기간·제외 규칙. 언론 PDF 6개는 저작권 확인 전까지 비공개 보류.
- 2026-11-04 Phase 3: 2차 리뷰(`reports/review_round2.md`, Opus) → 공통 도우미(뉴스·앨범 분리·필터, 교수 페이지 `pi_page`, 발표 0건 메뉴 숨김 등) → 시안마다 v01(정제)·v02(확장) 18개(`themes/<prefix>.v01|v02`, 보고서 `reports/themes_v/`). 27개 테마 빌드·검증 오류 0, 표본 레이아웃 846쪽 문제 0. 갤러리(`site/index.html`)는 시안별 버전 묶음.

### Phase 4 — 확정 시안 t5.v02 개선 (2026-11-06)

**Context**: 사용자가 최종 시안을 **t5.v02(Science Magazine v02)**로 확정했다. 앞으로는 이 테마만 다듬는다. 이번 요청은 6가지다. ① 글꼴 상표권 점검 ② 홈에서 PI 소개 줄 삭제 ③ People을 역할별 독립 페이지 5개 + 드롭다운으로 바꾸기 ④ Cover story 좌우 넘기기 ⑤ 유튜브 "콘텐츠 차단" 원인과 대응 ⑥ Fable·Opus·Codex(gpt-6.1-sol) 3자 리뷰를 반영한 뒤 전용 artifact로 게시.

**조사 결과(계획 근거)**
- **글꼴**: 4종 모두 SIL OFL 1.1이다(원문 확인). Playfair Display와 Pretendard에는 예약 글꼴 이름(RFN)이 있고, Source Serif 4와 Noto Serif KR에는 없다. RFN은 **글꼴을 고친 파생본에 같은 이름을 쓰는 것**만 막는다. 원본을 웹에서 쓰거나 함께 배포하는 것은 허용된다. 따라서 교체는 필요 없다. 지켜야 할 것은 하나다: 나중에 글꼴 파일을 사이트에 직접 넣을 때 직접 서브셋하지 말고 공식 배포 파일과 OFL.txt를 그대로 넣는다. Georgia·Times New Roman·나눔명조는 이름만 지정하는 대체 글꼴(local)이라 배포하지 않는다.
- **유튜브**: `themes/_shared/assets/shared.js`는 클릭하면 youtube-nocookie iframe을 넣는다. claude.ai artifact가 외부 iframe을 보안 정책(CSP)으로 막기 때문에 Chrome이 "콘텐츠가 차단됨" 화면을 띄운다. 사이트 결함이 아니고, 실제 웹서버(http/https)에서는 재생된다. 파일을 더블클릭해 연 경우(file://)에는 YouTube가 referrer 없는 요청을 거부해 오류 153이 난다.
- **커버 후보**: 커버 규칙(표지나 영상이 있는 논문·수상 뉴스)에 맞는 글이 8편이다.
- **구성원**: 박사후연구원 2, 연구원 8, 박사과정 4, 석사과정 8, 졸업생 약 23명. 교수 개인 페이지 `people/jong-seong-kug.html`이 이미 있다(`pi_page: true`).
- **artifact 한도**: t5.v02 전체 빌드는 파일 1063개다(앨범 89개의 사진 457장 포함). 한 버전에 511개까지만 들어가므로 공지·뉴스 99편은 전부 넣고, 앨범은 한도 안에서 최근 것부터 넣는다(약 10개).

**작업**(주 세션 직접. t5.v02 한 테마의 템플릿·CSS·JS 수정 수준이다)
1. **확정 기록**: `project_plan.md`(이중 저장), `first_draft/CLAUDE.md`(배포 테마 t5.v02, 화면 확인은 t5.v02로), 메모리(project).
2. **글꼴 보고서**: `reports/font_license.md`(글꼴·라이선스·저작권자·RFN·사용 방식·판정, 직접 넣을 때의 주의). 코드는 바꾸지 않는다.
3. **홈 PI 삭제**: `themes/t5.v02/templates/index.html` ednote의 `.byline`(사진·직함·이름)을 지운다. "About the lab →" 링크만 본문 아래에 남긴다. 관련 CSS도 정리한다.
4. **People 분리 + 드롭다운**
   - 새 페이지(theme.yaml `extra_pages`에 추가): `people-researchers`(postdoc·researcher·staff, 역할별 소제목), `people-phd`(phd·integrated), `people-ms`(ms·undergrad), `people-alumni`. 각 페이지 위에는 5개 페이지를 오가는 탭(`x.people_tabs(active)`, `pub_tabs` 방식)을 둔다. 템플릿은 `_t5.html` 공통 매크로 하나를 쓴다.
   - Professor는 기존 교수 페이지 `people/jong-seong-kug.html`로 연결한다(중복 페이지를 만들지 않는다).
   - `base.html` 메뉴의 People을 `<button aria-expanded>`로 바꾸고, 하위 목록 5개(Professor / Researchers / Ph.D. Students / M.S. Students / Alumni)를 붙인다. 누르면 펼쳐지고, 마우스를 올려도 펼쳐진다(`@media (hover:hover)`). Esc·바깥 클릭·포커스 이탈 시 닫힌다. 모바일 메뉴 안에서는 아코디언으로 펼친다. People 하위 페이지와 개인 페이지에서는 People이 현재 구역으로 표시된다. JS는 새 `assets/t5.js`(base에서 defer로 로드).
   - `people.html`: 교수 페이지로 즉시 이동하는 페이지(meta refresh)로 바꾸고, 이동이 안 될 때를 위해 5개 링크를 둔다. 개인 페이지의 "← People"은 그 사람의 역할 페이지로, about의 구성원·졸업생 링크와 푸터 People 링크도 새 페이지로 바꾼다.
   - `data/i18n.yaml`: `nav.people-*`(페이지 제목), `menu.phd`·`menu.ms`를 추가한다(`menu.professor/researchers/alumni`는 재사용).
5. **Cover story 넘기기**: 커버 후보 8편을 슬라이드로 만든다. 가로 scroll-snap 트랙과 ‹ › 버튼, "1 / 8" 표시(aria-live)를 두고, 키보드 ←→와 터치 스와이프를 지원한다. 자동 재생은 하지 않는다. 끝에 닿으면 버튼을 비활성화한다. 2번째 슬라이드부터 이미지는 lazy 로드. JS가 없으면 버튼을 숨기고 가로 스크롤로 동작한다. 아래 "News" 사진 기사 2편은 커버에 들어간 글을 뺀다. 코드는 `index.html`, `style.css`, `t5.js`.
6. **유튜브 대응**: `shared.js` 재생 버튼이 `location.protocol === 'file:'`이거나 `window.CSL_NO_EMBED`이면 iframe 대신 `youtube.com/watch?v=<id>`를 새 탭으로 연다. 미리보기 빌드(`scripts/preview/preview_family.py`)가 페이지마다 `CSL_NO_EMBED=true`를 넣는다. 실제 서버에서는 지금처럼 페이지 안에서 재생된다.
7. **빌드·검증 1차**(아래 검증 절차) 후 커밋.
8. **3자 리뷰**: 지시서 `reports/briefs/review_t5v02_task.md`(범위: 이번 diff·캡처 경로·점검표[드롭다운 마우스·키보드·터치, 캐러셀 접근성과 JS 없을 때, 역할 분류·링크, 유튜브 대체 동작, 데스크톱·모바일·다크·국문, 코드 일관성], 출력: 심각도·파일:줄·수정안).
   - Fable: Agent `model: fable`
   - Opus: Agent `model: opus`
   - Codex: `codex exec -m gpt-6.1-sol -s read-only -o reports/review_t5v02/codex.md`(백그라운드)
   - 셋은 서로의 결과를 보지 않고 병렬로 돌린다. 결과는 각각 `reports/review_t5v02/{fable,opus,codex}.md`에 둔다.
   - 주 세션이 지적을 하나씩 코드로 확인해 반영하거나 사유를 적어 기각하고, `reports/review_t5v02/summary.md`에 정리한다. 반영 후 다시 빌드·검증하고 커밋한다.
9. **전용 artifact**: `preview_family.py`에 테마 1개일 때의 첫 화면 배치를 추가한다. 스냅숏에서 빌드하고(공지 99편, 앨범은 파일 수 505개 이하가 되도록), linkcheck 0을 확인한 뒤 새 artifact로 2~3회에 나눠 게시한다. 기존 전체 시안 목록 artifact 맨 위에는 "확정 시안 t5.v02 →" 링크 한 줄을 추가한다. README의 artifact 표를 갱신하고 Notion Working Note에 캡처와 함께 기록한다.

**검증**
- `build.py --theme all` 성공(shared.js·i18n이 모든 테마에 영향) → `validate.py` 오류 0 → `check_layout.mjs t5.v02`(전체 페이지) + `check_layout.mjs --sample`(모든 테마 JS 오류 0).
- 캡처: `shot.mjs t5.v02`(홈, `--ko`, `--dark`), `people-researchers`, `people-alumni`. 임시 Playwright 스크립트로 드롭다운을 연 상태, 커버 다음 슬라이드, 키보드 조작, 모바일 메뉴 펼침을 캡처해 직접 확인한다.
- 유튜브: file://에서는 재생 클릭 시 새 탭(popup) 이벤트가 생기는지, 로컬 http 서버에서는 iframe이 들어가는지 Playwright로 확인한다(외부망 접속 여부는 결과에 적는다).
- artifact: 파일 수 511개 이하, linkcheck 0. 전환 막대와 유튜브 새 탭 동작은 사용자 브라우저에서 최종 확인한다(claude.ai 로그인이 필요해 내가 확인할 수 없다).

**진행 기록(2026-11-06)**: 1~9 완료(커밋 6b1e5f0 → 1020230 → a67dca0).
- 계획 대비 변경:
  - 사용자 요청으로 홈 PI 줄은 옮기지 않고 삭제했다.
  - People 클릭 시 하위 목록만 펼치고, 마우스를 올려도 펼친다(올려서 연 메뉴를 누르면 고정).
  - 유튜브 새 탭은 `window.open` 대신 재생 버튼을 링크로 바꾸는 방식이다(리뷰 반영).
- 리뷰: Fable 10건, Opus 14건, Codex 2건 중 16항목 반영, 3항목 사유 기록. 정리는 `reports/review_t5v02/summary.md`
- 전용 artifact: https://claude.ai/artifact/FqGJhpW2DekCscmREc2MW9 (공지 99편 전부, 앨범 9개, 파일 496개). 전체 시안 목록 맨 위에 링크를 걸었다.

### 배포 — GitHub Pages (2026-11-06)
- 결정: 계산 서버 직접 운영은 하지 않는다(CentOS Linux 8 지원 종료, 방화벽 개방 부담). 연구실 무료 조직 `SNU-climate`(교수님 Owner 예정)의 공개 저장소 `SNU-climate.github.io`에 원본을 올리고, GitHub Actions(`.github/workflows/pages.yml`)가 t5.v02를 빌드·검증해 https://snu-climate.github.io 로 배포한다. PR은 빌드·검증만 한다.
- 협업: 이슈 양식 4종(논문·뉴스·구성원·발표), `CONTRIBUTING.md`(웹 수정→PR, Claude Code 사용법).
- 공개 전 정리: 커밋 작성자 이메일을 GitHub noreply로 바꿔 이력을 다시 썼다(문서 속 커밋 해시도 새 해시로 교체). `backup/`·`csl1234.zip`·`site/`는 제외.
- 도메인: `climate.snu.ac.kr`은 2026-11-06 현재 학교 DNS에서 삭제된 상태다. 마이스누 "홈페이지 운영신청"(유효기간 1년, 매년 연장)으로 CNAME `climate.snu.ac.kr` → `snu-climate.github.io`와 GitHub 도메인 검증 TXT를 신청한다(임시 도메인명 `snu-climate.github.io`, 메일 구분 TXT, 서비스포트·SSL 체크 안 함).

- main 보호(2026-11-06), ruleset 2개.
  - "main PR 규칙": PR 필수(승인 1명, 새 push 시 승인 해제) + 자동 검사 `build` 통과. 조직 Owner·저장소 관리자는 우회할 수 있다(서버에서 바로 push 가능).
  - "main 이력 보호": 강제 push·삭제 금지. 우회할 수 있는 사람이 없다.

## 사용자 결정 대기
- 교수님 Owner 초대, 도메인 검증 TXT 발급 후 학교 운영신청 제출, 구성원 사진·소개 문구 확정.
