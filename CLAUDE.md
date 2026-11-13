# 기후시스템연구실 홈페이지 — 콘텐츠 관리 가이드 (Claude용)

학생이 "논문 나왔어요", "학회 발표 추가해 주세요", "신입생 들어왔어요"처럼 정보를 주면 Claude가 이 가이드대로 **데이터 파일만** 고치고 빌드한다.

## 절대 규칙
1. `site/` 안의 HTML은 **직접 고치지 않는다.** 항상 `data/`, `content/`, `static/`을 고친 뒤 빌드한다.
2. 정보를 지어내지 않는다. 날짜·저자·학회명·소속처럼 빠진 정보는 학생에게 묻는다. 논문 메타데이터는 DOI로 Crossref에서 받는다.
3. 국문과 영문을 모두 채운다. 학생이 한쪽 언어만 주면 다른 언어로 번역해 채우고, 번역했다는 사실을 학생에게 알린다.
4. 수정이 끝나면 반드시 **빌드 → 검증 → git commit** 순서로 마무리한다. 검증 오류가 0이 아니면 커밋하지 않는다.
5. 개인정보(전화번호, 개인 이메일, 사진)는 본인이 공개에 동의한 것만 넣는다.

## 명령 (항상 이 폴더에서)
작업 폴더는 **각자 자기 계정에 받은 복사본**이다(예: `~/CSL_homepage`). 서버 공유 폴더 `/data5/CSL_homepage/first_draft`는 2026-11-13부터 보관용이라 거기서 작업하지 않는다. 처음 받는 법과 두 사람 작업 규칙은 `HANDOVER.md` 6절.
```bash
cd ~/CSL_homepage
git pull                                                                                 # 시작 전 최신 받기(커밋 안 한 변경이 있으면 먼저 사용자에게 묻는다)
bash -lc "module load anaconda3/2023.03 && python scripts/build.py --theme t5.v02"   # 빌드(결과: site/t5.v02)
bash -lc "module load anaconda3/2023.03 && python scripts/validate.py --theme t5.v02"  # 검증(오류 0이어야 함)
git status                                                                               # 바뀐 파일이 이번 작업 것뿐인지 확인
git add -A && git commit -m "<무엇을 바꿨는지 한 줄>"                                   # 기록
git pull --rebase && git push                                                            # 배포(학생이 바뀐 화면을 확인한 뒤). 충돌 나면 해결 후 빌드·검증 다시
```
커밋 작성자는 그 복사본의 `git config user.name`·`user.email`(GitHub noreply 메일)이다. 설정이 없거나 개인 메일이면 커밋 전에 사용자에게 알린다. `git push --force`는 쓰지 않는다.
**확정 테마: `t5.v02`**(Science Magazine v02, 2026-11-06). 바뀐 화면은 이 테마로 확인한다: `node scripts/shot.mjs t5.v02 [page]`.
**배포**: GitHub `SNU-climate/SNU-climate.github.io`의 `main`에 push하면 GitHub Actions(`.github/workflows/pages.yml`)가 t5.v02를 빌드·검증해 https://climate.snu.ac.kr 로 1~2분 안에 배포한다(커스텀 도메인·HTTPS는 저장소 Pages 설정에 있으므로 CNAME 파일을 따로 두지 않는다). 테마를 바꾸려면 workflow의 `THEME` 한 줄만 고친다. 다른 구성원의 수정은 이슈 양식이나 Pull Request로 받는다(`CONTRIBUTING.md`). `main` 보호 규칙은 두 개다. "main PR 규칙": 일반 구성원은 PR + 자동 검사 `build` 통과 + 승인 1명이 있어야 병합된다. 조직 Owner(이 서버의 jongsooshin5 계정 포함)는 우회해 바로 push할 수 있다. "main 이력 보호": 강제 push(force push)와 main 삭제를 Owner를 포함한 **모두**에게 막는다. 그러니 이력을 다시 쓰지 말고 되돌릴 때는 `git revert`를 쓴다. 공개 저장소이므로 비밀번호·원본 백업·개인 이메일은 커밋하지 않는다.

## 요청 유형별 절차

### 1) 새 논문
```bash
python scripts/add_publication.py <DOI> [--corresponding] [--featured]
```
- 교수님이 교신저자면 `--corresponding`, 대표 논문이면 `--featured`. 저자 이름 뒤 `*`(교신저자) 표시는 해당 항목에 `corr_authors: ["Kug, J.-S.", ...]`(authors와 같은 표기)를 넣는다.
- 번호(가장 오래된 논문 = 1)와 연도 섹션은 빌드할 때 자동으로 정해지니 손대지 않는다.
- DOI가 없으면 `data/publications.yaml`에 직접 넣는다: `title, authors["Family, I.-I."], journal, year, date, volume, issue, pages, type: article`.
- 논문 그림을 넣으려면 `static/research/<파일>`에 두고 해당 항목에 `image: research/<파일>`을 쓴다.
- 정기 점검: `python scripts/fetch_publications.py --new`로 ORCID·OpenAlex·Crossref에 새로 잡힌 논문 후보를 확인한다(파일은 안 바뀜). 후보는 학생/교수님 확인 후 `add_publication.py`로 추가한다.

### 2) 논문 출판 뉴스(그림·소개·영상)
```bash
python scripts/new_news.py --slug <영문-짧은-이름> --category paper --doi <DOI> \
  --title-en "..." --title-ko "..." --summary-en "..." --summary-ko "..." \
  --youtube <영상ID 또는 URL> --cover <대표그림 경로> --image <추가그림 경로>
```
- 논문이 목록에 없으면 먼저 1)로 추가한다. 그래야 뉴스 아래에 논문 카드가 자동으로 붙는다.
- `content/news/<날짜-slug>/index.md`(영문)와 `index.ko.md`(국문) 본문을 쓴다. 학생이 준 소개 글·보도자료를 바탕으로 쓰고, 논문에 없는 주장을 더하지 않는다.
- 본문 중간에 영상을 넣으려면 `[[youtube:영상ID]]`, 그림은 `![설명](fig1.png)`.
- category: `paper`(논문) / `award`(수상) / `event`(행사) / `media`(언론·영상) / `lab`(연구실 소식).
- 그림은 가로 1600px 이하로 줄여 넣는다(Pillow: `Image.thumbnail((1600,1600))`, JPEG 품질 85).
- 언론 기사·방송은 `category: media`와 원문 주소 `link: "https://..."`(상세 페이지에 "원문 보기" 버튼).
- **갤러리(학회·워크숍·행사 사진)**: 뉴스와 같은 형식에 `album: true`, `gallery: [사진 파일들]`, `cover: <대표 사진>`. Gallery 메뉴에 나오고 공지 목록에서는 빠진다. 사진은 긴 변 1600px, EXIF(위치정보) 제거.

### 3) 학회 발표
`data/presentations.yaml`의 `presentations:` 맨 위에 추가한다.
```yaml
  - date: 2026-12-14
    event: "AGU Fall Meeting 2026"
    location: "San Francisco, CA, USA"
    title: "발표 제목"
    presenters: ["Hong, G.-D.", "Kug, J.-S."]   # 논문과 같은 "Family, I.-I." 형식 → 구성원이면 굵게 표시
    type: oral        # invited / keynote / oral / poster / seminar
    link: null        # 초록·슬라이드 URL이 있으면
```
`placeholder: true`인 예시 항목은 실제 발표가 들어오면 지운다.

### 4) 구성원(입학·졸업)
- `data/members.yaml`의 `members:`에 추가. `role`: postdoc / researcher / integrated / phd / ms / undergrad / staff.
- `id: <영문-이름>`(소문자-하이픈)을 넣으면 개인 페이지 `people/<id>.html`이 생긴다. 개인 페이지 항목:
  `position{en,ko}`, `email`, `homepage`, `interests{en:[...], ko:[...]}`, `education`·`career`·`awards`(`[{year 또는 period, en, ko}]`).
- 사진: `static/members/<id>.jpg`(정사각형, 600px, JPEG 85) → `photo: members/<id>.jpg`.
- `pub_name: "Family, I.-I."`를 넣으면 논문·발표 목록에서 이름이 굵게 표시되고, 개인 페이지에 참여 논문이 자동으로 붙는다.
- 졸업하면 `members:`에서 빼고 `alumni:`로 옮긴다(`id, name, degree, year, current, photo` + 개인 페이지 항목 유지 가능, email은 뺀다).

### 5) 유튜브 영상
- `python scripts/fetch_youtube.py` → 채널의 최신 영상과 썸네일이 `data/videos.yaml`, `static/videos/`에 반영된다.
- 홈에 먼저 보일 영상은 `featured: [ID, ...]`, 숨길 영상은 `hidden: [ID]`.
- 영상 설명에 논문 DOI가 있으면 사이트에서 해당 논문과 자동으로 연결된다.

### 6) 연구 주제·소개 문구·연락처
- 연구 주제: `data/research.yaml` (`title`, `summary`, `image`, 관련 `dois`, `videos`, 지구본 테마용 `regions`).
- 연구실 소개·연락처·링크: `data/site.yaml`. 교수 약력: `data/pi.yaml`. 화면 고정 문구: `data/i18n.yaml`.

## 마무리 체크리스트
- [ ] validate 오류 0 (경고는 내용 확인)
- [ ] 바뀐 페이지를 EN/KO 둘 다 확인 (`site/t5.v02/...html`, `site/t5.v02/ko/...html`)
- [ ] git commit → (학생 확인 후) git push
- [ ] 학생에게 바뀐 내용과, 번역·추정한 부분이 있으면 그 사실을 알린다

## 폴더 요약
`data/`(YAML) · `content/news/`(뉴스 글) · `static/`(사진·그림·썸네일) · `themes/`(디자인: 확정 테마 `t5.v02`와 공용 `_shared`만 둔다. 규약은 `themes/THEME_CONTRACT.md`) ·
`scripts/`(빌드·검증·관리) · `site/`(빌드 결과, git 제외) · `project_plan.md`(계획)
이전 시안 테마 26종·검토 보고서(`reports/`)·원본 백업(`backup/`)은 2026-11-11에 정리했다. 필요하면 서버의 `/data5/CSL_homepage/first_draft_20261111`(정리 전 복사본)이나 git 이력에서 찾는다.
**월 1회 백업(선택)**: 복사본의 `.git/hooks/pre-push`가 있으면 push 직전에 이번 달 백업(`../<폴더이름>_YYYYMMDD`)이 없을 때 폴더 전체(`.git` 포함, `site/` 제외)를 복사한다. 실패해도 push는 막지 않는다. 훅은 git에 올라가지 않으므로 복사본마다 따로 둔다(`HANDOVER.md` 6-1절).
