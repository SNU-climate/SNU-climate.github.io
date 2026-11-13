# 홈페이지 수정 방법

`main` 브랜치에 반영되면 GitHub Actions가 확정 테마(`t5.v02`)를 빌드·검증해 1~2분 안에 자동 배포합니다.
HTML(`site/`)은 빌드 결과라서 직접 고치지 않고, 아래 데이터 파일만 고칩니다.

## 방법 1 — 이슈로 요청하기 (가장 쉬움)
**Issues → New issue**에서 양식(논문 추가 / 뉴스·행사·수상 / 구성원 / 학회 발표)을 골라 채우면 홈페이지 담당자(백경민, [HANDOVER.md](HANDOVER.md))가 반영합니다.
사진·그림은 입력 칸에 끌어다 놓으면 됩니다.

## 방법 2 — GitHub 웹에서 직접 고치기
1. 아래 표에서 고칠 파일을 열고 연필(✏️) 아이콘을 누릅니다.
2. 수정한 뒤 **Commit changes → Create a new branch … and start a pull request**를 고릅니다.
3. Pull Request에서 자동 검사(Build and deploy)가 초록색 ✓인지 확인합니다. 빨간 X면 **Details**에서 오류 줄을 보고 고칩니다.
4. 담당자가 확인(승인)하고 병합하면 배포됩니다. `main`은 보호돼 있어서 자동 검사 통과와 승인 1명이 있어야 병합할 수 있습니다.

| 내용 | 파일 |
|---|---|
| 논문 | `data/publications.yaml` |
| 학회 발표 | `data/presentations.yaml` (맨 위에 추가) |
| 구성원·졸업생 | `data/members.yaml`, 사진은 `static/members/` |
| 뉴스·행사·갤러리 | `content/news/<날짜-slug>/index.md`(영문), `index.ko.md`(국문) |
| 연구 주제 | `data/research.yaml` |
| 연구실 소개·연락처 | `data/site.yaml`, 교수 약력 `data/pi.yaml` |

각 파일의 입력 형식은 [`CLAUDE.md`](CLAUDE.md)의 "요청 유형별 절차"를 따릅니다.

## 방법 3 — 내 컴퓨터에서 (Claude Code 사용 가능)
```bash
git clone https://github.com/SNU-climate/SNU-climate.github.io.git
cd SNU-climate.github.io
pip install -r requirements.txt
python scripts/build.py --theme t5.v02      # 결과: site/t5.v02/index.html
python scripts/validate.py --theme t5.v02   # 오류 0이어야 함
```
Claude Code에서 이 폴더를 열고 "논문 나왔어요, DOI는 …"처럼 요청하면 `CLAUDE.md` 가이드대로 데이터 수정·빌드·검증까지 합니다.
작업은 새 브랜치에서 하고 Pull Request로 올립니다.

## 지켜 주세요
- 정보를 추측해서 넣지 않습니다. 빠진 정보(날짜·저자·학회명)는 확인 후 넣습니다.
- 국문·영문을 모두 채웁니다.
- 사진은 긴 변 1600px 이하(구성원 사진은 정사각형 600px), 위치정보(EXIF)를 지웁니다.
- 이메일·사진 같은 개인정보는 본인이 공개에 동의한 것만 넣습니다.
- 이 저장소는 공개 저장소입니다. 비밀번호·내부 문서·원본 백업은 올리지 않습니다.
