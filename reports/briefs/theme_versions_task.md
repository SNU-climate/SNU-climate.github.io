# 브리프: 시안 확장 버전 v01·v02 만들기

작업 폴더 `/data5/CSL_homepage/first_draft/`. 한국어로 보고한다. 프롬프트에서 받은 **기준 테마(base)**와 **버전 접두(prefix)**로 작업한다(예: base `t8_globe`, prefix `t8` → `themes/t8.v01/`, `themes/t8.v02/`).

## 먼저 읽을 것
- `reports/review_round2.md` — 내 테마 절(강점·문제·v01 방향·v02 방향)과 "공통 권고"
- `themes/THEME_CONTRACT.md` — 특히 3-1절(선택 기능), **3-2절(공통 도우미: 뉴스·앨범 분리 목록, 분류 필터, 연도 목록, 교수 개인 페이지 `pi_page`, 연구 그림 매크로, 졸업생 사진, 발표 0건 메뉴 숨김)**, 4절(반드시 지킬 것). 리뷰 3-1절의 공통 문제 상당수는 이 도우미로 풀 수 있다. 리뷰가 "공통 빌드에서"라고 한 항목도 이 도우미를 써서 내 테마 안에서 해결한다.
- `themes/<base>/` — 출발점
- 선택 기능의 동작 예시: `themes/basic/templates/{member.html, research_topic.html, gallery.html, about.html, news.html, news_post.html}`, `themes/basic/theme.yaml`(extra_pages). 기능만 참고하고 디자인은 내 테마 것으로 만든다.

## 만들 것
1. `themes/<prefix>.v01/` — **정제판**. base를 복사한 뒤 리뷰의 v01 방향을 모두 반영한다(1차 리뷰 `reports/visual_review.md`의 내 테마 경미 문제 포함). 실제 데이터(구성원 45명·사진, 논문 318편, 뉴스 99 + 앨범 89, 발표 0건)에 맞게 다듬는다.
   - 앨범 89편이 뉴스에 섞이지 않게 `gallery.html` + `theme.yaml`의 `extra_pages: [gallery]`를 기본으로 쓴다(리뷰가 반대하면 따른다). 구성원 개인 페이지(`member.html`), 연구 주제 페이지(`research_topic.html`)도 리뷰 판단을 따른다.
2. `themes/<prefix>.v02/` — **확장판**. v01을 바탕으로 리뷰의 v02 방향(콘셉트를 밀어붙이는 기능 2~4개)을 구현한다.
   - 데이터는 빌드 컨텍스트에 있는 것만 쓴다(논문·연도별 통계·연구 regions·영상·뉴스·구성원). 없는 데이터(논문별 좌표 등)를 지어내지 않는다.
   - 외부 라이브러리는 테마 `assets/`에 넣어(vendoring) file://로도 동작하게 한다. 런타임 CDN·외부 API 금지.
3. 각 버전의 `theme.yaml`: `title`("<base 제목> v01"처럼), `concept{en, ko}`(무엇이 바뀌었는지 한두 문장), `palette`, 필요하면 `extra_pages`.

## 지킬 것
- 고칠 수 있는 곳은 `themes/<prefix>.v01/`, `themes/<prefix>.v02/`, `reports/themes_v/<prefix>.md`뿐이다. `scripts/`, `data/`, `content/`, `static/`, `themes/_shared/`, 다른 테마는 고치지 않는다(다른 에이전트 8개가 동시에 작업한다). 공통 도우미가 필요하면 내 테마 템플릿 안에 둔다.
- 규약 4절: `head_common()`/`scripts_common()`, 논문 번호·연도 섹션(`id="pub-N"`, `id="yYYYY"`)·검색, 언어 전환, EN/KO 모두.
- basic 계열(`basic.v01/v02`)은 원본 사이트 메뉴 구조(Introduction / Research / People / Publication / Notice)를 유지한다.
- git commit은 하지 않는다.

## 검증(내 테마만)
```bash
bash -lc "module load anaconda3/2023.03 && python scripts/build.py --theme <prefix>.v01 && python scripts/build.py --theme <prefix>.v02"
bash -lc "module load anaconda3/2023.03 && python scripts/validate.py --theme <prefix>.v01 && python scripts/validate.py --theme <prefix>.v02"   # 오류 0
node scripts/check_layout.mjs <prefix>.v01 <prefix>.v02 --sample                                                  # 문제 0
node scripts/shot.mjs <prefix>.v01            # 홈(데스크톱+모바일). 그 밖에 바꾼 페이지도 캡처해 직접 보고 한 번 다듬는다
```
`build.py --theme all`은 돌리지 않는다.

## 보고서 `reports/themes_v/<prefix>.md`
v01·v02 각각: 바꾼 점(리뷰 항목 번호와 대응), 새 기능 설명, 캡처 파일 경로, 남은 문제. 최종 응답은 5줄 이내(두 버전 핵심 한 줄씩, 검증 결과, 보고서 경로).
