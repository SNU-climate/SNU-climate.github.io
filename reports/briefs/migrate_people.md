# 브리프 A1: 구성원·졸업생·교수 이관

작업 폴더 `/data5/CSL_homepage/first_draft/`. 한국어로 보고. 먼저 `reports/briefs/backup_survey.md`(자료 위치·스키마·동시 작업 규칙)와 `reports/briefs/backup_task.md`(안전 규칙)를 읽는다.

## 담당 파일(이것만 고친다)
`data/members.yaml`, `data/pi.yaml`, `static/members/`, `reports/backup_mapping_people.md`(새로 작성)

## 할 일
1. **현재 구성원**(캐시 2026-10 기준): `people-researcher`, `student`(1~2쪽), `student-phd`, `student-master` 페이지와 각 사람의 `portfolio/<slug>/` 상세 페이지.
   - role: 원본 Researcher 페이지 사람은 Present Position에 따라 `postdoc`/`researcher`/`staff`, 학생은 student-phd → `phd`(통합과정이 확인되면 `integrated`), student-master → `ms`.
   - 상세 페이지의 Present Position, E-mail, Homepage, EDUCATION, RESEARCH EXPERIENCE(→ career), AWARDS, RESEARCH INTERESTS를 스키마대로 옮긴다. 상세 페이지의 개인 PUBLICATION 목록은 옮기지 않는다(논문은 publications.yaml에서 자동 연결 예정).
   - `pub_name`: 그 사람이 `data/publications.yaml`의 authors에 실제로 나오는 표기(예: "Shin, Y."). 목록에 없으면 생략.
   - 한글 이름: 원본에 근거가 있을 때만(사진 파일명·alt의 한글 이름 등). 근거와 함께 보고서에 "확인 필요"로 표시.
2. **졸업생**: `alumni`(+ `page/2`), `portfolio-category/alumni`(+ `page/2`)와 상세 페이지. degree·year·current는 원본 근거가 있을 때만.
3. **교수**: `people-jong-seong-kug` 페이지 ↔ `data/pi.yaml`. 사진(`static/members/kug.jpg`, 600px 정사각; 정사각이 아니면 얼굴 중심으로 자르지 말고 비율 유지 후 긴 변 600px)과 원본에만 있는 수상·경력·학회활동을 보완. 기존 값과 다르면 원본(연구실 사이트)과 학과 페이지 중 무엇을 택했는지 보고서에 적는다.
4. **사진**: 캐시 HTML의 이미지 URL → `backup/www/wp-content/uploads/...` 원본 파일. 워드프레스 리사이즈본(`-150x150`, `-e1736...`)보다 원본 크기 파일을 찾아 쓴다(파일명에서 접미사 제거). 정사각 600px로 가운데 기준 크롭, JPEG 85, `static/members/<id>.jpg`. Pillow 사용.
5. **예시 항목 삭제**: `placeholder: true` 구성원·졸업생 모두 지운다.
6. **2024-04 DB와 차이**: `backup/_derived/db/posts.jsonl`(post_type=portfolio)에만 있고 현재 캐시에 없는 사람은 옮기지 말고 보고서에 목록만 적는다(이미 떠난 사람일 수 있음).

## 보고서 `reports/backup_mapping_people.md`
원본 페이지 → 새 데이터 대응표(사람별 한 줄: 이름, role, 사진 원본 경로, 한글 이름 근거), 옮기지 못한 항목·이유, 확인 필요 목록(한글 이름 추정, role 애매, 사진 없음, 번역한 항목).

## 완료 기준
- `python scripts/validate.py --data-only` 오류 0(다른 에이전트 작업 중 생기는 뉴스·논문 경고는 무시).
- 최종 응답 5줄 이내: 이관 인원(현재/졸업생), 사진 수, 확인 필요 건수, 보고서 경로.
