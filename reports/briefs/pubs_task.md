# 브리프: 국종성 교수 전체 논문 수집 (Task 2)

작업 폴더: `/data5/CSL_homepage/first_draft/` (계획: `project_plan.md` Task 2). 한국어로 보고한다.
Python 실행: `bash -lc "module load anaconda3/2023.03 && cd /data5/CSL_homepage/first_draft && python scripts/..."`

## 목표
`data/publications.yaml`에 국종성(Jong-Seong Kug) 교수의 **동료심사 학술지 논문 전부**를 넣는다.
사이트는 최신 논문을 맨 위에, 연도별 섹션으로, 번호(가장 오래된 논문 = 1)를 붙여 보여준다. 번호·정렬은 build.py가 하므로 데이터만 정확하면 된다.

## 먼저 읽을 파일
- `scripts/pubtools.py`: Crossref 조회·정규화(`crossref_work`, `crossref_to_entry`, `pub_date`, `norm_doi`, `load_pubs`, `save_pubs`). **반드시 재사용**한다. 함수를 추가하는 것은 되지만 기존 함수의 동작은 바꾸지 않는다.
- `scripts/sitelib.py` (`name_key`, `number_pubs`), `data/publications.yaml`(현재 11편 시드, `corresponding`/`featured` 수동 필드 포함)

## 만들 것
1. `scripts/fetch_publications.py`
   - 기본 실행: 아래 출처를 모아 `data/publications.yaml`을 다시 쓰고 `reports/pubs_reconciliation.md`를 만든다.
   - `--new`: 현재 yaml에 없는 후보만 찾아 화면에 보고하고 **파일은 쓰지 않는다**(나중에 정기 점검용).
   - 응답 캐시: `.cache/pubs/`(gitignore됨). 요청 사이 간격 0.1~0.3초, 실패 시 재시도.
2. `reports/pubs_reconciliation.md`

## 출처 (발견용)
- ORCID `0000-0003-2251-2579` works (`https://pub.orcid.org/v3.0/<orcid>/works`, journal-article 약 270편)
- OpenAlex author `A5091389074` (article 약 435건, 중복·오귀속 포함). 이름 변형으로 갈라진 다른 author ID도 검색해 본다(예: `https://api.openalex.org/authors?search=Kug`). 2017~2020년 수가 적어 갈라진 ID가 있을 가능성이 있다.
- Crossref `query.author=Jong-Seong Kug`(및 `J.-S. Kug`) 검색 결과 중 저자 목록에 family=Kug가 있는 것
- 각 DOI의 메타데이터는 Crossref(`pubtools.crossref_work`)로 정규화한다. 이것은 출처 수에 세지 않는다.

## 규칙
- 포함: journal-article(리뷰 논문 포함). DOI가 없는 오래된 국내 학술지 논문도 ORCID에 있으면 포함(`doi` 없이, 메타데이터는 ORCID 값).
- 제외(보고서에 사유별 개수): preprint(예: 10.21203 Research Square, 10.22541/10.1002/essoar, 10.5194/egusphere·*-discuss, 10.48550 arXiv), erratum/correction/corrigendum/retraction, 학회 초록(EGU/AGU abstract), dataset/software(zenodo 10.5281 등), peer-review, supplementary.
- 같은 논문의 preprint와 저널 버전이 함께 있으면 저널 버전만 남긴다(제목 정규화 비교).
- 저자 확인: Crossref 저자 목록에 family가 Kug(대소문자 무시)인 저자가 있어야 한다. 없거나 애매하면 `needs_review: true`(화면에서 숨김).
- Reply/Comment류는 `needs_review: true`로 두고 보고서에 따로 적는다.
- 출처가 1곳뿐이지만 Crossref 저자 확인과 유형 확인을 통과한 항목은 표시한다(`needs_review` 없음). 보고서 "단일 출처" 목록에는 적는다.
- 연도: `pubtools.pub_date` 규칙(published-print가 있으면 그 연도, 없으면 issued). 학과 페이지와 맞추기 위한 규칙이니 바꾸지 않는다.
- 기존 항목의 수동 필드(`corresponding`, `featured`, `image`, `links`, `hidden`, 사람이 넣은 `needs_review`)는 DOI 기준으로 **보존**한다.
- `sources`에는 발견된 출처(`orcid`, `openalex`, `crossref`)를 적는다.
- 저장은 `pubtools.save_pubs`(원자적 쓰기, 최신순 정렬)를 쓴다. 다른 테마 작업이 동시에 빌드 중이다.

## 수정 금지
`themes/`, `scripts/build.py`, `scripts/validate.py`, `scripts/sitelib.py`, `data/`의 다른 파일, `content/`.
(버그를 발견하면 고치지 말고 보고서에 적는다.)

## 완료 기준 (모두 확인하고 결과를 보고서에 적는다)
1. `python scripts/validate.py --data-only` 오류 0.
2. `data/pi.yaml`의 `selected_dois` 5편이 모두 있고 표시 상태(needs_review 아님)다(assert).
3. 표시 논문 수가 250~450편 범위다. 벗어나면 이유를 분석해 보고서에 적는다.
4. 보고서: 출처별 개수, 출처 교집합(ORCID∩OpenAlex∩Crossref 등), 제외 사유별 개수, needs_review 목록(DOI·제목·사유), 단일 출처 목록, 연도별 편수 표, 출처 간 연도·학술지 불일치 목록, 무작위 10편의 Crossref 재조회 일치 확인 결과.
5. `python scripts/build.py --theme basic && python scripts/validate.py --theme basic` 오류 0.

## 최종 응답
주 세션에는 5줄 이내로: 표시/숨김 편수, 제외 편수, 완료 기준 통과 여부, 보고서 경로, 사람이 확인해야 할 점.
