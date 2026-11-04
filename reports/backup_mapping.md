# 원본 홈페이지 백업 → 새 사이트 이관 총괄 (2026-11-04)

백업 `csl1234.zip`(2.6GB, cafe24 호스팅 전체) → `backup/`(읽기 전용, git 제외). 세부 보고서:
- 구성원·졸업생·교수: [`backup_mapping_people.md`](backup_mapping_people.md)
- 공지·갤러리·연구·소개·발표: [`backup_mapping_content.md`](backup_mapping_content.md)
- 논문 대조: [`pubs_reconciliation.md`](pubs_reconciliation.md) "## 백업 대조"
- 조사 메모·작업 지시서: [`briefs/backup_survey.md`](briefs/backup_survey.md), `briefs/migrate_*.md`, `briefs/pubs_backup_task.md`

## 1. 백업 구성
| 자료 | 시점 | 쓴 곳 |
|---|---|---|
| WordPress(billey 테마 + Elementor) + KBoard 게시판 + phpMyAdmin(`dbeditor/`) | — | 실행하지 않음 |
| WP Rocket 페이지 캐시 `wp-content/cache/wp-rocket/climate.snu.ac.kr/` | 2026-09~10 | **현재 내용의 1순위 출처**(메뉴·구성원·졸업생·논문·공지 1쪽·갤러리 1쪽) |
| All-in-One WP Migration 백업 `.wpress` 안의 `database.sql` | 2024-04-09 | 공지·갤러리 본문, 구성원 상세 비교 |
| `wp-content/uploads/` | ~2026-01 | 사진·그림 |
| `wp-config.php`, `.ftpaccess`, DB의 users·comments·options·폼 제출 | — | **민감정보라 읽거나 옮기지 않음** |

## 2. 원본 메뉴 → 새 사이트(basic 테마)
| 원본 메뉴 | 원본 주소 | 새 페이지 | 데이터 |
|---|---|---|---|
| INTRODUCTION › Introduction of Laboratory | `/introduction/` | `about.html` | `site.yaml` lab.intro·photo |
| INTRODUCTION › Location of Laboratory | `/introduction-map/` | `contact.html` | `site.yaml` contact |
| RESEARCH › 5개 주제 | `/research-*/` | `research.html` + `research/<key>.html` | `research.yaml`(그림 13장) |
| PEOPLE › Professor | `/people-jong-seong-kug/` | `people.html#pi` | `pi.yaml` |
| PEOPLE › Researcher / Student / Alumni | `/people-researcher/`, `/student/`, `/alumni/` | `people.html#researchers/#students/#alumni` + `people/<id>.html` | `members.yaml`(22 + 졸업생 23, 사진 46) |
| PUBLICATION | `/publication/` | `publications.html` | `publications.yaml`(318편, 교신저자 58편 표시) |
| NOTICE › Announcement | `/notice/` | `news.html` | `content/news/`(공지·매거진 95 + 기존 4) |
| NOTICE › Gallery | `/gallery/` | `gallery.html` | `content/news/`의 `album: true` 89편(사진 477장, 115.6MB) |
| (새 메뉴) Presentations, YouTube | — | `presentations.html`, `videos.html` | `presentations.yaml`(빈 목록), `videos.yaml` |

## 3. 옮기지 못한 것
| 항목 | 건수 | 이유 |
|---|---|---|
| 공지 번호 84–90 | 7 | 2024-04 DB 이후·캐시 1쪽 이전 글이라 백업 어디에도 없음 |
| 2024-04 이후 공지 본문 | 11(+1) | 캐시 목록에 제목·날짜만 있음 → 제목만 넣음, 원문 링크 필요 |
| 원본 논문 목록 No.263–297 | 35 | 백업에 없음(우리 목록에는 Crossref로 이미 들어 있음) |
| 2024-04 DB에만 있는 구성원 | 3 | 현재 사이트에 없음(Dongkyu Park, Guseul Woo, Xin Geng) |
| 공지 첨부 PDF | 6 | 원본에서 관리자만 받을 수 있던 언론 지면 → 저작권 확인 전까지 `backup/_held_pdfs/`에 보류 |
| 목록에 없는 갤러리 업로드 사진 | 13 | 어느 글의 사진인지 알 수 없음 |
| 휴지통 글 | 3 | 삭제된 글 |

## 4. 주 세션 결정
- 언론 PDF 6개는 공개하지 않음(위 표). 본문의 첨부 줄도 뺐다.
- 구성원 굵게 표시는 저자 표기가 **정확히 같을 때만**(교수는 기존처럼 이니셜 접두 매칭). 동명이인은 `pub_since/pub_until/pub_exclude`로 좁힌다(이희지 2024~, Steinert 2025 제외 / 이단비 2023~).
- 학회 발표 목록은 원본에 없어 빈 목록으로 두었다(갤러리의 학회 참석 글로 발표 항목을 만들지 않음).

## 5. 사람이 확인할 것(요약 — 세부는 각 보고서)
1. 공지 67편의 날짜가 실제 기사 날짜가 아니라 2021년 사이트 이전 때 일괄 등록한 날짜(2021-08-16 60편, 2021-06-11 7편)
2. 원문 링크가 필요한 최근 공지 12편
3. 구성원 한글 이름 37건(사진 파일명 등 간접 근거), role 4건, 졸업생 학위·연도 6건, 사진 3건
4. 동명이인 저자 표기(이단비 2026 Piao·Mun 논문, 박재형 2016·2023, 추정 연결 4명)
5. 논문: 교신저자 `(CA)` 해석, 원본 누락 추정 8편, 연도 차이 12건
6. 주소의 교수실 522호(원본 위치 페이지는 501·507호만 표기)
