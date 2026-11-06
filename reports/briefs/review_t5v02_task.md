# 브리프: 확정 시안 t5.v02 개선분 독립 리뷰

작업 폴더는 `/data5/CSL_homepage/first_draft/`(정적 사이트 생성기, Jinja2)다. **한국어로 보고한다.**
리뷰어 세 명(Fable, Opus, Codex)이 서로의 결과를 보지 않고 같은 범위를 따로 본다.

## 배경
연구실 홈페이지 최종 시안으로 `t5.v02`(Science Magazine v02)가 확정됐다. 사용자 요청과 구현 내용은 다음과 같다.

1. **홈에서 PI 소개 줄 삭제**: 여는 글 아래 교수 사진·직함 줄을 지우고 "About the lab →" 링크만 남겼다.
2. **People 분리**: People을 랜딩 페이지가 아닌 독립 페이지 5개로 나눴다.
   - Professor = 기존 교수 개인 페이지 `people/jong-seong-kug.html`
   - `people-researchers` = postdoc·researcher·staff
   - `people-phd` = phd·integrated
   - `people-ms` = ms·undergrad
   - `people-alumni`
   - 메뉴의 People은 **누르면 아래로 하위 목록만 펼치는 드롭다운**이다(마우스를 올려도 펼침). 옛 주소 `people.html`은 교수 페이지로 이동시킨다(meta refresh).
3. **Cover story 넘기기**: 홈 커버 기사를 좌우 화살표로 과거 기사까지 넘겨 본다. 대상은 표지가 있는 논문·수상 소식(현재 8편)이다. 가로 scroll-snap 트랙에 ‹ › 버튼, 번호, ←→ 키를 붙였다.
4. **유튜브**: claude.ai 미리보기는 외부 iframe을 막아 "콘텐츠 차단" 화면이 뜬다. 그래서 `file://`이거나 `window.CSL_NO_EMBED`일 때는 재생 버튼이 YouTube를 새 탭으로 연다. 실제 http 서버에서는 기존처럼 페이지 안에서 재생된다(로컬 서버에서 재생 확인함).

## 범위(이것만 본다)
```bash
git -C /data5/CSL_homepage/first_draft diff b54c80a..HEAD -- themes/t5.v02 themes/_shared/assets/shared.js data/i18n.yaml scripts/preview/preview_family.py
```
- 핵심 파일:
  - `themes/t5.v02/templates/`: `base.html`, `index.html`, `_t5.html`(people_* 매크로), `people*.html`, `member.html`, `about.html`
  - `themes/t5.v02/assets/`: `t5.js`(새 파일), `style.css`
  - `themes/_shared/assets/shared.js`
- 빌드 결과: `site/t5.v02/`(영문), `site/t5.v02/ko/`(국문). HTML은 생성물이라 고치는 대상이 아니다. 문제는 템플릿·CSS·JS에서 찾는다.
- 캡처: `site/_shots/review_t5v02/*.png`
  - 데스크톱 홈·드롭다운·커버·People 페이지·교수 페이지
  - 모바일 메뉴·커버·석사과정(국문)
  - 다크 모드
  - 로컬 서버에서 유튜브가 재생되는 화면
- 규약: `themes/THEME_CONTRACT.md`. 콘텐츠 가이드: `CLAUDE.md`.

## 확인 방법(선택)
- 빌드: `bash -lc "module load anaconda3/2023.03 && python scripts/build.py --theme t5.v02 --out <스크래치 폴더>"`
  - `site/`를 덮어쓰지 않도록 반드시 `--out`으로 별도 폴더를 지정한다.
- Playwright: `~/.local/opt/shot`에 설치돼 있다. 사용 예는 `scripts/shot.mjs`와 `/tmp/claude-1500/-data5-CSL-homepage/3efc62de-b047-4116-9c2c-f3e7d402120c/scratchpad/t5check.mjs`를 본다.
  - 실행하려면 스크립트를 스크래치 폴더에 복사해 쓴다.

## 점검표
1. **드롭다운**
   - 마우스: 클릭·마우스 올림·바깥 클릭
   - 키보드: Tab 순서, Enter/Space, Esc 뒤 포커스 위치, 포커스가 메뉴를 벗어날 때
   - 터치·모바일: 메뉴 안 아코디언, Esc가 전체 메뉴와 충돌하지 않는지
   - aria-expanded·aria-current가 맞는지, JS가 없을 때 동작, 국문 글자 폭, 1180px·860px 경계 폭
2. **커버 넘기기**
   - 번호·버튼 비활성화가 맞는지, 연달아 누를 때, 손으로 스와이프할 때, 창 크기를 바꿀 때
   - 화면 밖 편의 inert가 맞는지, 스크린리더용 aria(carousel/slide, aria-live)
   - JS가 없을 때 가로 스크롤로 동작하는지, `prefers-reduced-motion`
   - 슬라이드 높이가 다를 때, 표지 없는 글(`cover-story--text`), 커버가 1편뿐일 때
   - 아래 "News" 사진 기사와 같은 글이 겹치지 않는지
3. **People 페이지**
   - 역할 분류와 인원수, 탭의 현재 표시
   - 개인 페이지의 "←" 링크(역할 페이지 + 앵커), about·푸터 링크
   - `people.html` 이동, 국문 페이지 제목·문구, 빈 역할일 때
4. **유튜브 대체 동작**
   - 새 탭 열기 조건이 맞는지(팝업 차단, `noopener`)
   - 실제 서버 동작이 바뀌지 않았는지, 다른 26개 테마에 미치는 영향
5. **화면**: 데스크톱·모바일(390px)·다크·국문에서 겹침·넘침·대비·포커스 링
6. **코드**
   - 주변 코드와의 일관성(주석 밀도, 명명), 중복, 쓰이지 않게 된 CSS·i18n 키
   - Jinja 매크로 반환값의 공백(`|trim`) 처리
   - 미리보기 스크립트의 테마 1개 모드

## 규칙
- **읽기만 한다.** 저장소 파일을 고치지 말고 git 명령으로 상태를 바꾸지 않는다.
  - 예외(Claude 리뷰어): 자기 보고서 파일 하나만 쓴다.
  - 빌드나 Playwright 실행이 필요하면 스크래치 폴더를 쓴다.
- 추측보다 근거를 댄다. 지적마다 재현 조건(어떤 화면·입력에서 무엇이 잘못되는지)을 적는다. 확신이 낮으면 "확신 낮음"이라고 표시한다.

## 출력
보고서 `reports/review_t5v02/<리뷰어>.md`(fable / opus / codex). Codex는 마지막 메시지가 그대로 보고서가 된다.

```
# t5.v02 리뷰 — <리뷰어>
## 지적 (심각도순, 15개 이내)
### N. [높음|중간|낮음] 한 줄 제목
- 위치: 파일:줄
- 문제: …
- 재현: …
- 수정안: …(코드 조각 가능)
## 확인했고 문제없음 (한 줄씩)
```
