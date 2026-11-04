# 백업 이관: 구성원·졸업생·교수 (브리프 A1)

작성 2026-11-04. 출처는 원본 홈페이지 WP Rocket 캐시(2026-09~10, `backup/www/wp-content/cache/wp-rocket/climate.snu.ac.kr/`)이고, 사진은 `backup/www/wp-content/uploads/` 원본 파일을 썼다.
바꾼 파일: `data/members.yaml`(전면 교체), `data/pi.yaml`(사진·경력·학회활동 보완, `awards`·`memberships` 신설), `static/members/*.jpg` 46장.
파싱·사진 스크립트는 스크래치 폴더에 있다(`lists.py`, `detail.py`, `photos.py`, `mkphotos.py`, `pubnames.py`, `dbdiff.py`). 백업은 경로 인자로만 넘겼고 `python -I`로 실행했다.

## 1. 요약

| 항목 | 건수 | 비고 |
|---|---|---|
| 현재 구성원 | 22 | postdoc 2, researcher 8, phd 4, ms 8 (integrated 0: 통합과정 근거 없음) |
| 졸업생 | 23 | 원본 alumni 목록 24항목. 임형규(Hyunggyu Lim) 상세 페이지 2개를 1명으로 합쳤다 |
| 사진 | 46 | 구성원·졸업생 45(전원 사진 있음) + 교수 1 |
| 삭제한 예시 항목 | 5 | members `placeholder` 4 + alumni 1 |
| pub_name 지정 | 29 | 현재 11, 졸업생 18 |
| 한글 이름 | 36 | 근거(사진 파일명·alt, 2024-04 DB 첨부 제목)가 있는 사람만. 외국인 8명과 Jaehwi Yoo는 영문만 |
| 확인 필요 | **61** | §6 (한글 이름 37 + role 4 + 졸업생 학위·연도 6 + 사진 3 + pub_name 6 + 이메일 1 + 교수 2 + 번역 2) |

검증 결과: `python scripts/validate.py --data-only`에서 오류 0. 경고 2건(논문 숨김 1, placeholder 3건)은 presentations·publications 쪽(다른 담당)에서 나온 것이다. 구성원 쪽 placeholder는 0건.

## 2. 원본 페이지 → 새 데이터 대응표

사진 경로는 `backup/www/wp-content/uploads/` 기준이다. 결과물은 `static/members/<id>.jpg`(정사각 600px, 가운데 크롭, JPEG 85, EXIF 없음).
워드프레스 리사이즈본·편집본(`-150x150`, `-e17…`, `-scaled`)은 접미사를 떼어 원본 크기 파일을 썼다. 예외는 김다영(§6-C).

### 2.1 현재 구성원 (22)

| # | 원본 페이지 | id | 이름 (en / ko) | role · position | 사진 원본 | 한글 이름 근거 | pub_name |
|---|---|---|---|---|---|---|---|
| 1 | people-researcher → portfolio/hyunju-lee | hyunju-lee | Hyunju Lee / 이현주 | researcher · Researcher | 2025/12/이현주-사진.jpg (413×531) | 사진 파일명·alt "이현주 사진" | — (목록에 "Lee, H.-J." 없음) |
| 2 | 〃 portfolio/chao-liu | chao-liu | Chao Liu / — | researcher · Ph.D. Researcher | 2025/12/차오리우-사진_수정본.jpg (414×533) | 외국인. 파일명은 "차오리우" | Liu, C. |
| 3 | 〃 portfolio/jae-heung-park | jaeheung-park | Jaeheung Park / 박재형 | researcher · Research Professor | 2021/06/researcher_박재형.png (376×484) | 파일명 "researcher_박재형" | Park, J.-H. |
| 4 | 〃 portfolio/blau-manuel-tobias | manuel-tobias-blau | Manuel Tobias Blau / — | postdoc · Postdoctoral Fellow | 2025/06/마누엘-사진.jpg (414×533) | 외국인. 파일명은 "마누엘" | — |
| 5 | 〃 portfolio/yu-liang | yu-liang | Yu Liang / — | postdoc · Postdoctoral Fellow | 2025/12/유리양-사진.png (413×531) | 외국인. 파일명은 "유리양" | — |
| 6 | 〃 portfolio/yechul-shin | yechul-shin | Yechul Shin / 신예철 | researcher · Researcher | 2022/11/신예철.jpg (419×539) | 파일명·alt "신예철" | Shin, Y. |
| 7 | 〃 portfolio/jong-hwa-lee | jonghwa-lee | Jonghwa Lee / 이종화 | researcher · Researcher | 2022/11/이종화-연구원님.jpg (413×531) | 파일명 "이종화-연구원님" | — |
| 8 | 〃 portfolio/yoon-hee-cho (슬러그 재사용) | minseo-cho | Minseo Cho / 조민서 | researcher · Researcher | 2021/12/증명사진조민서.jpg (2002×2574) | 파일명·alt "증명사진(조민서)" | Cho, M. (추정) |
| 9 | 〃 portfolio/yeonjun-suh | yeonjun-suh | Yeonjun Suh / 서연준 | researcher · Researcher | 2025/12/서연준-사진.jpg (354×472) | 파일명 "서연준 사진" | — |
| 10 | 〃 portfolio/kyung-na-kim | kyungna-kim | Kyungna Kim / 김경나 | researcher · Researcher | 2021/06/researcher_김경나.png (376×484) | 파일명 "researcher_김경나" | Kim, K. (추정) |
| 11 | student·student-phd → portfolio/huiji-lee | huiji-lee | Huiji Lee / 이희지 | phd · Ph.D. Candidate | 2024/02/KakaoTalk_20240205_145134178.jpg (354×472) | 2024-04 DB 첨부 제목 "이희지"(uploads/2022/07/이희지.jpg). 현재 사진 파일명에는 이름이 없다 | Lee, H. |
| 12 | 〃 portfolio/sunhee-wang | sunhee-wang | Sunhee Wang / 왕선희 | phd · Ph.D. Candidate | 2022/07/왕선희.jpg (376×462) | 파일명·alt "왕선희" | Wang, S. |
| 13 | 〃 portfolio/hyung-jeon-kang | hyungjeon-kang | Hyungjeon Kang / 강형전 | phd · Ph.D. Candidate | 2022/07/강형전.jpg (3199×4113) | 파일명·alt "강형전" | Kang, H.-J. (추정) |
| 14 | 〃 portfolio/jiho-ko-2 | jiho-ko | Jiho Ko / 고지호 | phd · Ph.D. Candidate | 2022/07/고지호-1.jpg (353×443) | 파일명·alt "고지호" | Ko, J. |
| 15 | student·student-master → portfolio/jun-seong-moon | junseong-moon | Junseong Moon / 문준성 | ms · M.S. Candidate | 2026/01/문준성-사진.jpg (413×531) | 파일명 "문준성 사진" | — |
| 16 | 〃 portfolio/seung-jae | seungjae-hong | Seungjae Hong / 홍승재 | ms · M.S. Candidate | 2024/07/홍승재형2.jpg (1807×2410) | 파일명 "홍승재형(2)"에서 호칭 '형'을 뺐다 | Hong, S.-J. |
| 17 | 〃 portfolio/jinhyuk-mun | jinhyuk-mun | Jinhyuk Mun / 문진혁 | ms · M.S. Candidate | 2024/03/문진혁.jpg (248×319) | 파일명·alt "문진혁" | Mun, J.-H. |
| 18 | 〃 portfolio/gyeongmin-baek-2 | gyeongmin-baek | Gyeongmin Baek / 백경민 | ms · M.S. Candidate | 2024/10/백경민-증명사진.jpg (803×1071) | 파일명 "백경민-증명사진" | — |
| 19 | student/page/2·student-master → portfolio/seongho-park | seongho-park | Seongho Park / 박성호 | ms · M.S. Candidate | 2025/03/박성호-사진.jpg (419×539) | 파일명 "박성호 사진" | — |
| 20 | 〃 portfolio/jaeyeong-lee | jaeyeong-lee | Jaeyeong Lee / 이재영 | ms · M.S. Candidate | 2025/03/이재영-사진-1.jpg (359×461) | 파일명 "이재영 사진" | — |
| 21 | 〃 portfolio/jiwoo-kim | jiwoo-kim | Jiwoo Kim / 김지우 | ms · M.S. Candidate | 2025/03/김지우-사진-1.jpg (358×461) | 파일명 "김지우 사진" | — |
| 22 | 〃 portfolio/jeong-hyeon-lee | jeonghyeon-lee | Jeonghyeon Lee / 이정현 | ms · M.S. Candidate | 2026/01/이정현-사진픽셀.jpg (375×482) | 파일명 "이정현-사진픽셀" | — |

학생 수는 원본 student 1~2쪽 12명 = student-phd 4명 + student-master 8명과 일치한다.

### 2.2 졸업생 (23)

원본 `alumni` 1~3쪽(4쪽은 비어 있음)과 `portfolio-category/alumni` 1~2쪽에는 같은 24항목이 있다. 알 수 있는 경우 원본 상세 페이지의 education·career·awards·interests를 영문으로 넣었다.

| # | 원본 상세 페이지 | id | 이름 (en / ko) | degree · year (근거) | 사진 원본 | 한글 이름 근거 | pub_name |
|---|---|---|---|---|---|---|---|
| 1 | portfolio/yeon-soo-jang | yeon-soo-jang | Yeon-Soo Jang / 장연수 | Ph.D. · 2023 (EDUCATION: POSTECH Ph.D. 2023) | 2021/06/student_장연수.png | 파일명 | Jang, Y.-S. |
| 2 | portfolio/kyung-min-noh | kyung-min-noh | Kyung Min Noh / 노경민 | Ph.D. · 2023 | 2021/06/student_노경민.png | 파일명 | Noh, K.-M. ("Noh, K. M."와 같은 키) |
| 3 | portfolio/so-won-park | so-won-park | So-Won Park / 박소원 | Ph.D. · 2023 | 2021/06/student_박소원.png | 파일명 | Park, S.-W. |
| 4 | portfolio/na-yeon-shin | na-yeon-shin | Na-Yeon Shin / 신나연 | Ph.D. · 2024 | 2021/06/student_신나연.png | 파일명 | Shin, N.-Y. |
| 5 | portfolio/ullala-pathiranage-gayan-pathirana | ullala-pathiranage-gayan-pathirana | Ullala Pathiranage Gayan Pathirana / — | Ph.D. · 2024 | 2023/03/가얀.jpg | 외국인. 파일명은 "가얀" | Pathirana, G. |
| 6 | portfolio/danbi-lee | danbi-lee | Danbi Lee / 이단비 | — (§6-B) | 2021/12/증명사진-1.jpg | 같은 업로드 폴더의 "이단비.png"(DB 첨부 제목 "이단비") | Lee, D. |
| 7 | portfolio/da-seul-kim | daseul-kim | Daseul Kim / 김다슬 | M.S. · 2022 | 2021/12/증명사진.jpg (996×1280) | DB 옛 리비전에 "student김다슬.png" + "Da-Seul Kim", uploads/2021/06/student_김다슬.png | Kim, D.-S. |
| 8 | portfolio/donggeon-lee | donggeon-lee | Donggeon Lee / 이동건 | — (§6-B) | 2021/06/student_이동건.png | 파일명 | Lee, D.-G. |
| 9 | portfolio/haechan-kim | haechan-kimm | Haechan Kimm / 김해찬 | — (§6-B) | 2022/07/김해찬-2.jpg | 파일명·alt | Kimm, H. |
| 10 | portfolio/geon-il-kim | geonil-kim | Geonil Kim / 김건일 | Ph.D. · 2024 | 2021/06/student_김건일.png | 파일명 | Kim, G.-I. |
| 11 | portfolio/ji-hoon-oh | ji-hoon-oh | Ji-Hoon Oh / 오지훈 | Ph.D. · 2024 | 2021/06/student_오지훈.png | 파일명 | Oh, J.-H. |
| 12 | portfolio/jiuwei-zhao-2 (슬러그 재사용) | yi-kai-wu | Yi Kai Wu / — | Postdoc · 연도 없음 (CAREER: 2021– POSTECH 박사후) | 2022/11/이카이-1.jpg | 외국인. 파일명은 "이카이" | Wu, Y.-K. |
| 13 | portfolio/hyunggy-lim (2023) + portfolio/hyung-gyu-lim (2022) | hyunggyu-lim | Hyunggyu Lim / 임형규 | Ph.D. · 2019, current KIOST | 2023/04/명함사진_2020.jpeg (1649×2199) | 옛 페이지 사진 파일명 "alumni_임형규" | Lim, H.-G. |
| 14 | portfolio/jin-soo-kim | jinsoo-kim | Jinsoo Kim / 김진수 | Ph.D. · 2019, current Univ. Zurich | 2021/06/alumni_김진수.png | 파일명 | Kim, J.-S. |
| 15 | portfolio/da-yeong-kim | dayeong-kim | Dayeong Kim / 김다영 | M.S. · 2019 | 2021/06/Rectangle-497-e1721277841761.png (154×199, §6-C) | alt "김다영 박소원 석사 졸업식" | — |
| 16 | portfolio/mi-hyun-jo | mihyun-jo | Mihyun Jo / 조미현 | — (§6-B) | 2021/06/alumni_조미현.png | 파일명 | — |
| 17 | portfolio/jiuwei-zhao | jiuwei-zhao | Jiuwei Zhao / — | Postdoc · 2021 (CAREER: 2019–2021 POSTECH Post-Doc) | 2021/06/researcher_zhao.png | 외국인 | Zhao, J. |
| 18 | portfolio/sun-yong-kim | sunyong-kim | Sunyong Kim / 김선용 | Ph.D. · 2021 | 2021/06/student_김선용.png | 파일명 | — (§6-E) |
| 19 | portfolio/i-gusti-ayu-diah-valentina-lestari | i-gusti-ayu-diah-valentina-lestari | I Gusti Ayu Diah Valentina Lestari / — | M.S. · 2017 | 2021/06/alumni_lestari.png | 외국인 | — |
| 20 | portfolio/woo-hyun-yang | woohyun-yang | Woohyun Yang / 양우현 | M.S. · 2018 | 2022/02/KakaoTalk_Photo_2022-02-15-13-06-57.jpeg | DB 옛 리비전에 "Alumni양우현.png" + "Woo-Hyun Yang", uploads/2021/06/alumni_양우현.png | Yang, W.-H. |
| 21 | portfolio/chang-eun-kim | changeun-kim | Changeun Kim / 김창은 | M.S. · 2020 | 2021/06/alumni_김창은.png | 파일명 | Kim, C.-E. (추정) |
| 22 | portfolio/li-jianying | jianying-li | Jianying Li / — | Postdoc · 2019, current CAMS | 2021/06/alumni_lijiaying.png | 외국인 | LI, J.-Y. |
| 23 | portfolio/jae-hwi-yoo | jaehwi-yoo | Jaehwi Yoo / — | Researcher · 연도 없음 (Present Position "Researcher") | 2021/06/researcher_yoo.png | 근거 없음 | — |

### 2.3 교수 (people-jong-seong-kug ↔ data/pi.yaml)

| 항목 | 처리 | 근거·선택 |
|---|---|---|
| 사진 | `photo: members/kug.jpg` | 원본 2021/06/People-Professor_seonghug.png(376×484)는 정사각이 아니라서 자르지 않고 비율을 유지한 채 긴 변 600px(466×600)로 맞췄다 |
| 경력: KIOST 기간 | 학과 "2009–2014 Senior Research Scientist" → 원본대로 "2009–2013 Senior" + "2013–2014 Principal Research Scientist" | **원본(연구실 사이트)** 채택. 원본이 더 자세하고 학과 값과 모순되지 않는다 |
| 경력 추가(원본에만 있음) | KMOU 교수, Center for Earth Climate Changes 센터장, UST 부교수(2010–2014), 도쿄대 방문교수(2007), 이화여대·서울대 강사(2013/2006/2005), 서울대 조교(1999–2001) | 원본에서 보완 |
| 경력: 그 밖의 항목 | 2024.03–, 2019–2024.02, 2014–2019, 2007–2009, 2003–2007 | **학과 값** 유지(월 단위까지 있음). 원본의 중복 줄(2014–2019 두 번)은 하나만 남겼다 |
| 학회활동(service) 추가 | Regional Economies and Policies 편집위원(2012–), East Asia Climate(EAC) 회원(2005–) | 원본에서 보완 |
| 학회활동: 값이 다른 3건 | 한림원 준회원(학과 2014–2019 / 원본 2016–present), CLIVAR 패널(학과 2016–2020 / 원본 2016–present), APJAS 부편집장(학과 2012– / 원본 2014–present) | **학과 값** 유지. 학과 페이지가 최근(2026-11-03) 확인한 공식 자료이고 원본은 갱신이 멈춘 것으로 보인다 |
| 수상 `awards` (신설) | 15건 | 원본에만 있음 |
| 학회 회원 `memberships` (신설) | 6건(AMS, 한국기후변화학회, 한국해양학회, 재미한인대기과학자회, 한국기상학회, AGU) | 원본에만 있음 |
| 소속·연락처 | 원본 "Division of Environmental Sciences, SNU" → 학과 "School of Earth and Environmental Sciences" 유지. 전화·이메일은 같다 | 학과 값 |
| 학력 | 같다(원본에는 월까지 있음: 2003.08/2000.02/1998.02). 바꾸지 않았다 | — |

## 3. 옮기지 못한(옮기지 않은) 항목과 이유

- **개인 PUBLICATION 목록**(전원): 브리프 지시에 따라 옮기지 않았다. `pub_name`으로 publications.yaml과 자동 연결된다.
- **since**(합류 연도): 원본에 입학·합류 연도가 명시돼 있지 않아 전원 생략했다(경력의 "present" 항목으로 추정은 할 수 있다).
- **졸업생 이메일**: 스키마 권장에 따라 넣지 않았다.
- **졸업생 상세 항목의 국문**: education/career/awards는 영문만 넣었다(관심분야 ko만 번역). 화면에서는 en으로 대체된다.
- **프로필 링크**: 스키마에 필드가 하나(`homepage`)뿐이다.
  - Manuel Blau의 ORCID(0000-0003-4649-6040)·ResearchGate, Yechul Shin의 Google Scholar는 넣지 못했다. homepage에는 각각 Google Scholar와 개인 사이트를 넣었다.
  - 교수 ResearchGate(`researchgate.net/profile/J-S-Kug`)는 pi.yaml에 필드가 없어 넣지 않았다.
- **잘못된 링크**: 여러 졸업생 페이지(Changeun Kim, Na-Yeon Shin, So-Won Park, Sunyong Kim, Gayan)의 ResearchGate 아이콘이 모두 `Dong-Geon-Lee-2`를 가리킨다. 임형규 2023 페이지는 `Jin-Soo-Kim-2`를 가리킨다. 템플릿 복사 오류로 보여 쓰지 않았다. 본인 링크가 맞아 보이는 것만 homepage로 넣었다(장연수·노경민·김건일·오지훈·김진수·이단비·이동건·임형규(옛 페이지)).
- **원본 오류로 뺀 줄**
  - Yu Liang 학력 B.S. 칸의 "Engineering, Ulsan National Institute of Science and Technology, South Korea, B.S."는 다른 사람 페이지에서 복사한 잔여물로 보인다.
  - Jianying Li CAREER의 "Lecturer, Ehwa University… / SNU…(2006, 2005)"는 교수 페이지 문구를 복사한 것이다.
- **기타 미이관**: Jianying Li의 PROJECT 목록 6건, Lestari의 고교 학력, 졸업생 페이지의 오래된 Present Position("Ph.D. Candidates" 등).
- **이메일 1개만 반영**(스키마는 단일 값): 이현주의 두 번째 주소(gmail), 박재형의 Sub 주소(postech)는 넣지 않았다.
- **갤러리성 portfolio 글**(2020 졸업식, CSL 단체 사진, OASIS 학술발표회 등 13건): 구성원이 아니라서 이 작업 범위가 아니다(뉴스·갤러리 담당).

## 4. 2024-04 DB에만 있고 현재 캐시에 없는 사람 (옮기지 않음)

`backup/_derived/db/posts.jsonl`에서 post_type=portfolio이고 publish 상태인 글 중 현재 캐시 목록에 없는 구성원 글이다.

| DB post ID | 이름 | 당시 분류 | 마지막 수정 | 비고 |
|---|---|---|---|---|
| 15005 | Dongkyu Park | researcher | 2023-09-18 | 현재 목록에 없음. 이미 떠난 사람일 수 있음 |
| 13264 | Guseul Woo | researcher | 2023-04-13 | 〃 |
| 7519 | Xin Geng | researcher | 2023-12-19 | 〃. "Geng, X."가 2023~2025 논문에 다수 나온다 |
| 18228 | Jinhyuk Mun | master-candidates | 2024-03-06 | 같은 사람이 현재 새 글(21071)로 있다. 누락 아님 |
| 6645 | Sunhee Wang | master-candidates | 2023-03-02 | 같은 사람이 현재 phd 글(21393)로 있다. 누락 아님 |

## 5. 원문을 손본 내용(오타·표기 정리)

- 학력은 원문 "학과, 대학, 국가 학위"를 "학위, 학과, 대학, 국가" 순서로 바꿨다(pi.yaml 형식). 기간의 "present"는 "2024–"처럼 적었다.
- 박재형: Present Position "Researcher Professor" → "Research Professor". 수상 영문은 원문 괄호의 국문(젊은대기과학자상, 우수학위논문상)에 맞춰 정리했다.
- Yu Liang: "2013.1 - 2023.9 Postdoc Fellow" → "2023.01–2023.09"(박사 졸업 2022.12와 맞지 않는 오타). "Postdoc Fellow"는 "Postdoctoral Fellow"로 바꿨다.
- 철자 수정: "Nature Sciences" → "Natural Sciences"(이현주), "German" → "Germany"(Blau), "Environment Engineering" → "Environmental Engineering"(홍승재), "Divisionof" → "Division of"(김다슬·김다영·양우현), "Busan National University" → "Pusan National University"(신나연·오지훈·김창은), "Ocean Scienad" → "Ocean Science"(김선용), "ohang" → "Pohang"(Jiuwei Zhao), "vest oral"·"Intergrative"·"Ocenography"·"Postedoctoral"·"Institution of Ocean" 정정(임형규), "Disse rtation" → "Dissertation"(김진수), "Induce" → "Induced"(Lestari). 수상명 앞의 "for"는 지웠다.
- 임형규: 2023 페이지의 관심분야 문구가 깨져 있어("investigate interation" 등) 2022 페이지의 관심분야를 썼다. 2022 페이지에만 있는 경력 2건과 장학 1건도 합쳤다.
- Lestari: Electronics Lab 조교 3줄(2013, 2013, 2012)을 1줄(2012–2013)로 합쳤다.
- 교수: "Korea Oceanographical Society" → "Korean Society of Oceanography", "Korea Meteorological Society" → "Korean Meteorological Society", "Climate Change Society" → "Korea Climate Change Society", "POSTECH-Donga daily news" → "POSTECH–Dong-A Ilbo", "Ehwa" → "Ewha Womans".
- 학생 position: 원본 분류명 "Ph.D. Candidates"/"Master Candidates" → "Ph.D. Candidate"(박사과정)/"M.S. Candidate"(석사과정).

## 6. 확인 필요 목록 (61건)

### A. 한글 이름 (37) — 근거는 §2 표. 전부 원본 사진 파일명·alt 또는 2024-04 DB 첨부 제목에서 가져왔다
- 현재 구성원 19: 이현주, 박재형, 신예철, 이종화, 조민서, 서연준, 김경나, 이희지\*, 왕선희, 강형전, 고지호, 문준성, 홍승재\*, 문진혁, 백경민, 박성호, 이재영, 김지우, 이정현
- 졸업생 17: 장연수, 노경민, 박소원, 신나연, 이단비\*, 김다슬\*, 이동건, 김해찬, 김건일, 오지훈, 임형규, 김진수, 김다영, 조미현, 김선용, 양우현\*, 김창은
- \* 현재 사진 파일명에는 이름이 없어 간접 근거(DB·같은 폴더의 다른 파일, 호칭 제거)로 넣은 것. 특히 확인할 것
- 미기입 1: Jaehwi Yoo(근거 없음). 외국인 8명(Chao Liu, Manuel Tobias Blau, Yu Liang, Gayan Pathirana, Yi Kai Wu, Jiuwei Zhao, Lestari, Jianying Li)은 영문 표기를 유지했다(파일명의 음차 "차오리우·마누엘·유리양·가얀·이카이"는 쓰지 않았다)

### B. role·학위 애매 (role 4 + 졸업생 6)
1. Chao Liu: Present Position "Ph.D. Researcher" → `researcher`. postdoc일 수 있음.
2. 이현주·신예철: 박사 학위자인데 Present Position이 "Researcher" → `researcher`. postdoc 여부 확인.
3. 조민서·서연준: 상세 페이지에 이메일만 있다. researcher/staff 구분과 학력 확인.
4. 통합과정: 근거가 없어 박사과정 4명을 모두 `phd`로 넣었다(`integrated` 0명).
5. 이단비·이동건: alumni 목록에 있는데 Present Position은 "Ph.D. Candidates" → degree·year 생략.
6. 김해찬: alumni인데 "Master Candidates" → degree·year 생략.
7. 조미현: 서울대 박사(2015)이고 연구실에서의 신분을 알 수 없다 → degree 생략.
8. Yi Kai Wu·Jaehwi Yoo: degree를 역할(Postdoc/Researcher)로 넣었다. 연도는 알 수 없다.
9. Jiuwei Zhao·Jianying Li: degree "Postdoc". year는 POSTECH 박사후 종료 연도(2021/2019)로 넣었다.
10. current 3명(임형규 KIOST, 김진수 Univ. Zurich, Jianying Li CAMS): 원본 페이지가 마지막으로 갱신된 2022~2023년 기준이라 지금과 다를 수 있다.

### C. 사진 (3)
11. 김다영: 원본 Rectangle-497.png(323×323)는 김다영·박소원 2인 졸업 사진이다. 그래서 원본 사이트가 쓴 WP 편집본(154×199)을 600px로 확대했다(저화질). 증명사진으로 바꾸면 좋다.
12. 신예철·박성호: 야외 전신 사진이라 가운데 크롭에서 얼굴이 작다. 박성호 상세 페이지가 쓰던 편집본(`-e1741155899478`)은 백업에 없다.
13. 교수: 원본이 376×484라서 466×600으로 확대했다(저화질). 학과 페이지의 고해상도 사진으로 바꿀지 결정이 필요하다.
- 참고: 원본 대부분이 긴 변 500px 안팎이라 600px 정사각으로 확대됐다(사진 없음은 0명).

### D. pub_name (6)
14. 이희지 "Lee, H.": 9건 중 본인 것은 2024~2026 생지화학 논문 5건으로 보인다. 개인 논문 목록의 "A biological dipole…"로 확인했다. 2017(계절예측 리뷰)·2018(산불 에어로졸)·2025 Steinert et al.(NORCE 공저)은 다른 Lee, H.일 가능성이 높아 개인 페이지와 굵게 표시에 섞인다. 접두 일치로 "Lee, H. C." 1건도 굵게 표시된다.
15. 이단비 "Lee, D.": 2023·2025·2026(Borneo) 논문은 본인 개인 목록으로 확인했다. 2015 BAMS(Weller et al., 목록에 2번 중복)는 다른 사람이다. 2026 Piao et al.과 Mun et al.도 확인이 필요하다.
16. 박재형 "Park, J.-H.": 2016 Lim et al.(화산)과 2023 "Park, J. H."(북극 하천·식물플랑크톤)은 다른 사람일 수 있다. 접두 일치로 "Park, J." 2009~2011 3건이 굵게 표시된다.
17. 추정 연결 4명(개인 논문 목록에는 해당 논문이 없다)
    - 김경나 "Kim, K."(2023 Geng et al.)
    - 조민서 "Cho, M."(2022 Shin et al. 딥러닝 ENSO)
    - 강형전 "Kang, H.-J."(2025 Park et al. 북극 오존)
    - 김창은 "Kim, C.-E."(2019 Science, Cai et al.)
18. Jianying Li: publications.yaml 표기가 대문자 "LI, J.-Y."다(2022). pub_name도 그대로 적었다. 논문 쪽 표기 정리가 필요하다.
19. 모호해서 지정하지 않은 사람
    - 김선용: "Kim, S." 13건. 2015~2022 동아시아 원격상관 논문이 본인 것인지 불명
    - 이종화: 2013 "Lee, J.-H."/"Lee, J. H."
    - Jaehwi Yoo: 2017 "Yoo, J. H."
    - 이재영·이정현: 2025 "Lee, J."
    - 김지우: "Kim, J."
    - 김다영: "Kim, D."

### E. 이메일 (1)
20. postech.ac.kr 주소를 쓰는 현재 구성원 3명(이종화 jhlee20@, 김경나 knakim@, 왕선희 shwang1@)은 주소가 지금도 유효한지 확인이 필요하다. 박재형은 원본 "Main" 표기대로 gmail을, 신예철은 원본대로 gmail을 넣었다. 개인 메일 공개에 동의했는지 확인한다(원본 사이트에는 공개돼 있었다).

### F. 교수 (2)
21. KMOU 교수와 Center for Earth Climate Changes 센터장은 원본에 연도가 없다. 2013–2014 줄 바로 아래에 있어 기간을 "2013–2014"로 추정했다.
22. 학회활동 3건(한림원 준회원, CLIVAR 패널, APJAS 부편집장)은 학과 페이지와 원본의 기간이 달라 학과 값을 유지했다. 맞는지 확인한다.

### G. 번역 (2)
23. 일반: 현재 구성원 상세 항목(position, interests, education, career, awards)의 ko, 교수 보완 항목(경력·학회활동·수상·회원)의 ko, 졸업생 interests의 ko는 모두 영문 원문을 번역했다. 원본에 국문이 있던 것은 박재형 수상 2건뿐이다.
24. 특히 불확실한 번역
    - 교수 수상명 "Muenjae Distinguished Professor" → "POSTECH 무은재 교수", "Distinguished Young Professor" → "POSTECH 젊은 석학교수", "Scientist of the Month" → "이달의 과학기술자상(장관상)"
    - "Center for Earth Climate Changes"(영문 병기), "Korean Atmospheric Scientists in America" → "재미한인대기과학자회"
    - Yu Liang 소속 "Research Institute for Basic Sciences"와 김경나 경력 "Bomin Science Consulting"은 ko에도 영문을 그대로 두었다
    - 신예철 학과명("Earth Science and Engineering" → "지구과학·공학")

## 7. 주 세션 참고(템플릿)

- `alumni_list` 매크로는 `{{ a.degree }}, {{ a.year }}`를 그대로 찍는다. 그래서 degree·year가 없는 6명(이단비, 이동건, 김해찬, 조미현, Yi Kai Wu, Jaehwi Yoo)은 ", "가 남는다. 빈 값 처리가 필요하다.
- pi.yaml에 새로 만든 `awards`·`memberships`는 템플릿에 표시가 필요하다. 교수 사진은 정사각이 아니다(466×600).
- 졸업생 상세 항목 중 일부는 연도가 없다(`career`/`awards`에 period·year 없는 항목: Lestari 연구경험 5건, Jianying Li 수상 3건).
