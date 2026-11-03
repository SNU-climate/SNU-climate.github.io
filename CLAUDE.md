# 기후시스템연구실 홈페이지 — 콘텐츠 관리 가이드 (Claude용)

학생이 "논문 나왔어요", "학회 발표 추가해 주세요", "신입생 들어왔어요"처럼 정보를 주면 Claude가 이 가이드대로 **데이터 파일만** 고치고 빌드한다.

## 절대 규칙
1. `site/` 안의 HTML은 **직접 고치지 않는다.** 항상 `data/`, `content/`, `static/`을 고친 뒤 빌드한다.
2. 정보를 지어내지 않는다. 날짜·저자·학회명·소속처럼 빠진 정보는 학생에게 묻는다. 논문 메타데이터는 DOI로 Crossref에서 받는다.
3. 국문과 영문을 모두 채운다. 학생이 한쪽 언어만 주면 다른 언어로 번역해 채우고, 번역했다는 사실을 학생에게 알린다.
4. 수정이 끝나면 반드시 **빌드 → 검증 → git commit** 순서로 마무리한다. 검증 오류가 0이 아니면 커밋하지 않는다.
5. 개인정보(전화번호, 개인 이메일, 사진)는 본인이 공개에 동의한 것만 넣는다.

## 명령 (항상 이 폴더에서)
```bash
cd /data5/CSL_homepage/first_draft
bash -lc "module load anaconda3/2023.03 && python scripts/build.py --theme all"      # 전체 빌드
bash -lc "module load anaconda3/2023.03 && python scripts/validate.py"               # 검증(오류 0이어야 함)
git add -A && git commit -m "<무엇을 바꿨는지 한 줄>"                                   # 기록(push 안 함)
```
배포 테마가 정해지면 `python scripts/build.py --theme <테마> --out dist`로 배포용 폴더를 만든다(배포 절차는 추후 결정).

## 요청 유형별 절차

### 1) 새 논문
```bash
python scripts/add_publication.py <DOI> [--corresponding] [--featured]
```
- 교수님이 교신저자면 `--corresponding`, 대표 논문이면 `--featured`.
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
- 사진: `static/members/<영문이름>.jpg`(정사각형, 600px, JPEG 85) → `photo: members/<영문이름>.jpg`.
- `pub_name: "Family, I.-I."`를 넣으면 논문·발표 목록에서 이름이 굵게 표시된다.
- 졸업하면 `members:`에서 빼고 `alumni:`에 `name, degree, year, current`로 옮긴다.

### 5) 유튜브 영상
- `python scripts/fetch_youtube.py` → 채널의 최신 영상과 썸네일이 `data/videos.yaml`, `static/videos/`에 반영된다.
- 홈에 먼저 보일 영상은 `featured: [ID, ...]`, 숨길 영상은 `hidden: [ID]`.
- 영상 설명에 논문 DOI가 있으면 사이트에서 해당 논문과 자동으로 연결된다.

### 6) 연구 주제·소개 문구·연락처
- 연구 주제: `data/research.yaml` (`title`, `summary`, `image`, 관련 `dois`, `videos`, 지구본 테마용 `regions`).
- 연구실 소개·연락처·링크: `data/site.yaml`. 교수 약력: `data/pi.yaml`. 화면 고정 문구: `data/i18n.yaml`.

## 마무리 체크리스트
- [ ] validate 오류 0 (경고는 내용 확인)
- [ ] 바뀐 페이지를 EN/KO 둘 다 확인 (`site/<테마>/...html`, `site/<테마>/ko/...html`)
- [ ] git commit
- [ ] 학생에게 바뀐 내용과, 번역·추정한 부분이 있으면 그 사실을 알린다

## 폴더 요약
`data/`(YAML) · `content/news/`(뉴스 글) · `static/`(사진·그림·썸네일) · `themes/`(디자인, 규약은 `themes/THEME_CONTRACT.md`) ·
`scripts/`(빌드·검증·관리) · `site/`(빌드 결과, git 제외) · `reports/`(검증·대조 보고서) · `project_plan.md`(계획)
