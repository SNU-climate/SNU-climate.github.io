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

## 사용자 결정 대기(백업 이후)
- 배포 방식(학교 웹호스팅 업로드 방식), 9종 중 최종 테마 선택, 구성원 사진·소개 문구 확정.
