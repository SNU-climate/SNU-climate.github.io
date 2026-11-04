# 브리프 B: 논문 목록 ↔ 원본 사이트 대조 (Task 7)

작업 폴더 `/data5/CSL_homepage/first_draft/`. 한국어로 보고. 먼저 `reports/briefs/backup_survey.md`(자료 위치·동시 작업 규칙)와 `reports/briefs/backup_task.md`(안전 규칙), `reports/pubs_reconciliation.md`(1차 수집 결과)를 읽는다.

## 담당 파일(이것만 고친다)
`data/publications.yaml`, `reports/pubs_reconciliation.md`("## 백업 대조" 절 추가). 논문 추가는 `scripts/add_publication.py`, 수집 캐시는 `.cache/pubs/`를 써도 된다. `scripts/`의 코드는 고치지 않는다.

## 원본 목록
- 1순위: 캐시 `backup/www/wp-content/cache/wp-rocket/climate.snu.ac.kr/publication/index-https.html`(2026-10, 전체 317편, 번호·저자(교신저자 `*`)·연도·제목·학술지·DOI). 텍스트판 `backup/_derived/pages/publication.txt`.
- 2순위: DB KBoard board 3(`backup/_derived/db/kboard_board_content.jsonl`, 2024-04 기준 262편) — 1순위에서 정보가 깨진 항목 보완용.

## 할 일
1. 원본 항목을 파싱해 `data/publications.yaml`과 DOI(정규화: 소문자, `https://doi.org/` 제거)로 맞춘다. DOI가 없거나 틀리면 제목 유사도(+연도)로 맞춘다.
2. **교신저자**: 원본에서 `J.-S. Kug*`이면 `corresponding: true`. 원본에서 `*`가 붙은 모든 저자를 `corr_authors: ["Family, I.-I.", ...]`로 기록한다 — 이름은 **우리 yaml의 authors 목록에 있는 표기 그대로**(성+이니셜로 매칭). 매칭이 안 되는 별표 저자는 보고서에.
3. **원본에만 있는 논문**: 원본의 DOI로 `add_publication.py <DOI> [--corresponding]` 추가. DOI가 없으면 Crossref 제목 검색으로 찾고, 그래도 없으면 원본 정보로 직접 입력(`type: article`, `source: backup`). 학술지 논문이 아닌 것(학회 초록·보고서·preprint)은 1차 수집 규칙대로 빼고 보고서에 이유를 적는다.
4. **우리 목록에만 있는 논문**: 지우지 않는다. Crossref 저자 목록에 Kug가 있는지 다시 보고, 원본에 왜 없는지(원본 누락 추정 / 오귀속 의심)를 분류해 보고서에. 오귀속이 확실하면 `hidden: true` + `note:`.
5. `needs_review: true` 항목: 원본에 있으면 해제, 없으면 사유를 보고서에.
6. 1차 보고서의 확인 필요 항목을 원본과 대조: DOI 없는 국내 학술지 13건(원본에 있으면 추가), APJAS 2008 "Kang, I.-K." 표기, 숨긴 BAMS DOI, ORCID DOI 오기.
7. 연도: 원본 연도와 우리 연도가 다른 항목을 목록화(우리 규칙은 published-print 우선). 고치지 말고 보고서에 표로.

## 완료 기준
- `python scripts/validate.py --data-only` 오류 0(다른 에이전트 작업 중 생기는 구성원·뉴스 경고는 무시). `build.py`는 돌리지 않는다.
- `reports/pubs_reconciliation.md` "## 백업 대조": 원본 N편 ↔ 우리 M편, 일치/원본만/우리만 건수, 추가·숨김·교신저자 표기 건수, 연도 차이 표, 사람이 확인할 목록.
- 최종 응답 5줄 이내: 최종 표시 편수, 추가/숨김/교신저자 건수, 확인 필요 건수.
