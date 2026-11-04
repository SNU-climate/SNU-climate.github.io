# 브리프: t8.v01·t8.v02를 밝은 배경(흰색)으로 전환

작업 폴더 `/data5/CSL_homepage/first_draft/`. 한국어로 보고한다.

## 요청(사용자)
"t8은 다크 화면 말고 밝은 배경(흰색)으로 고치면서 다른 내용들도 색 수정해줘."

## 범위
- 고칠 곳: `themes/t8.v01/`, `themes/t8.v02/`, `reports/themes_v/t8.md`(밝은 화면 전환 절 추가)만. 원래 시안 `themes/t8_globe/`는 비교용으로 다크를 유지한다. `scripts/`, `data/`, `themes/_shared/`, 다른 테마는 고치지 않는다.
- 먼저 읽을 것: `reports/themes_v/t8.md`(두 버전 구조), `themes/THEME_CONTRACT.md` 4절, 각 테마의 CSS·JS(`assets/`), 템플릿.

## 할 일
1. 기본 화면을 흰 배경(`#fff` 또는 아주 옅은 중성색)의 라이트 테마로 바꾼다. `color-scheme: dark` 고정을 풀고, 색은 토큰(`:root`)으로 정리한다. 다크 모드(`prefers-color-scheme: dark`)를 따로 지원할지는 판단해서 정하되, 지원한다면 기존 다크 팔레트를 재사용한다.
2. 다른 색도 흰 배경에 맞게 다시 고른다.
   - 지구본: 바다·육지·격자·대기 광선·밤 음영(v02)·연구 지역 점과 영역.
   - 네온 청록·주황 강조색은 흰 배경에서 대비가 부족하다. 짙은 톤으로 바꾼다(본문 4.5:1, 큰 글자·그래픽 3:1 이상).
   - 카드·칩·버튼·포커스 링·그래프(연도 막대, 타임라인 슬라이더)·지도 범례·코드풍 라벨.
   - 원본 그림(흰 배경 그림)의 액자 처리도 라이트에 맞게 정리한다.
3. 콘셉트(우주·지구본, 대담한 타이포)는 유지하면서 밝고 깨끗한 "과학 지도" 느낌으로 만든다. 두 버전 모두 같은 팔레트를 쓴다.
4. `theme.yaml`의 `concept`·`palette`를 밝은 화면에 맞게 갱신한다.

## 검증
```bash
bash -lc "module load anaconda3/2023.03 && python scripts/build.py --theme t8.v01 && python scripts/build.py --theme t8.v02"
bash -lc "module load anaconda3/2023.03 && python scripts/validate.py --theme t8.v01 && python scripts/validate.py --theme t8.v02"   # 오류 0
node scripts/check_layout.mjs t8.v01 t8.v02 --sample          # 문제 0
node scripts/shot.mjs t8.v01 ; node scripts/shot.mjs t8.v02   # 홈. 그 밖에 people, publications, research/mechanism, news 상세도 캡처해 직접 확인
```
`build.py --theme all`과 git commit은 하지 않는다. 최종 응답은 5줄 이내(바꾼 팔레트 요약, 검증 결과, 캡처 경로).
