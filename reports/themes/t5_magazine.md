# t5_magazine — Science Magazine

## 결과
- 빌드 성공(24쪽: EN 8 + KO 8 + 뉴스 상세 4×2), validate **오류 0**. 경고 2건(placeholder 8건, 숨긴 논문 1건)은 데이터 쪽이며 테마와 무관.
- 스크린샷: `site/_shots/t5_magazine.png`, `site/_shots/t5_magazine_mobile.png`
- 파일: `themes/t5_magazine/{theme.yaml, templates/(base, _t5, 9개 페이지).html, assets/style.css}`

## 디자인 요약
- 종이색 바탕(#fbf9f4) + 잉크(#161513) + 붉은 포인트(#b5121b, 다크 #ff5f56). 제목은 Playfair Display / Noto Serif KR(한국어 900), 기사 본문은 Source Serif 4 / Noto Serif KR, UI는 Pretendard.
- 마스트헤드: 상단 띠(최종 수정일, 소속, YouTube, 언어 토글) → 가운데 큰 연구실명(Playfair 900) + 태그라인 → 대문자 자간 메뉴(활성은 붉은 밑줄), 아래 이중선. 모바일은 왼쪽 정렬 제목 + 메뉴 버튼.
- 홈(뉴스 우선): ① 커버 스토리(최신 뉴스: 큰 16:9 표지 | "Cover story", 분류·날짜, 큰 헤드라인, 요약, Read more) ② 보조 기사 3개(세로 구분선 그리드) ③ 검은 띠의 "Watch" — 영상 3편 + 채널 타일(실제 영상 수 `stats.videos`) ④ "From the journals" — 최신 논문 5편(학술지명·`№ p.num`·제목·제1저자 et al.) ⑤ 연구 분야 피처 카드(첫 카드는 2칸) ⑥ Join us.
- 연구 주제 그림 대체물: 주제별 색 그라디언트 위에 위경도 30° 격자와 `research[].regions` 실제 좌표 점(맥동 링, 감속 모션 설정이면 정지) + 좌표 표기(예: `45°N 100°W`). 지어낸 지형·숫자 없음.
- 뉴스 상세(잡지 기사): 가운데 정렬 분류·날짜 → 큰 헤드라인 → 이탤릭 요약(dek) → 바이라인 → 큰 표지(최대 1000px) → 본문 720px, 1.19rem·행간 1.86, 첫 글자 붉은 드롭캡 → 영상(표지가 있으면 본문 아래, 본문의 "아래 영상" 문구와 맞춤; 표지가 없고 영상만 있으면 영상이 표지) → 연결 논문 → 다른 소식 3건. 표지·영상이 모두 없으면 타이포그래피 표지(분류 단어 + 동심원 무늬). 본문이 숫자로 시작하면("2024년 3월…") 드롭캡이 숫자를 쪼개므로 자동으로 끈다.
- 논문·발표: 왼쪽 sticky 연도 색인(Playfair 숫자 2열), 오른쪽에 밑줄형 검색창과 붉은 큰 연도 제목, 논문은 제목이 먼저 오도록 CSS `order`로 배치(매크로 마크업·data 속성은 그대로).
- 구성원: PI 프로필(검은 바탕 + 붉은 원 이니셜 초상 대체물, 큰 이름, 드롭캡 약력, 연구 관심사 번호 목록, 학력·경력·학술 활동 3단), 구성원 카드(붉은 원 이니셜).
- 영상 페이지: 첫 영상을 2×2 크기로 키운 그리드. 연락처: 정보 표 + 붉은 Join us 상자.

## 확인한 화면(직접 열어 봄)
- 데스크톱 EN: 홈(전체), 뉴스 상세(permafrost, 전체), 논문, 연구, 구성원, 영상, 발표
- 모바일: 홈(전체), 메뉴 열림(360px), KO 뉴스 상세(low-cloud)
- 다크: KO 홈, KO 뉴스 상세(joined-snu: 타이포그래피 표지·드롭캡 꺼짐 확인), 연락처
- Playwright 점검(직접 작성한 스크립트): 24쪽 × (360px 라이트, 1440px 다크) 모두 가로 넘침 0px, 로드 시 iframe 0개, 모바일 메뉴 토글 정상, 콘솔 오류 없음. 논문 검색 필터(건수 갱신·빈 연도 숨김) 확인.
- 작업 중 논문이 11편 → 317편으로 늘어서 다시 확인함(연도 색인 27개를 2열로 바꾸고 화면 높이를 넘으면 자체 스크롤).

## 남은 문제
- 표지가 YouTube hqdefault(480×360) 썸네일이라 커버 스토리·기사 표지에서 흐리다(16:9로 잘라 검은 띠는 숨김). 논문 그림이나 고해상도 표지가 들어오면 해결된다.
- 웹폰트 CDN 의존(Google Fonts, jsdelivr). 오프라인에서는 Georgia·시스템 글꼴.
- 홈 Watch·From the journals 줄은 1080px 이하에서 가로 스크롤(스크롤 스냅)로 바뀐다. 문서 자체 가로 넘침은 없다.
- 구성원·발표는 예시(SAMPLE) 데이터.

## 테마 안에서 직접 처리한 문구(i18n.yaml 추가 제안)
| 제안 키 | en | ko |
|---|---|---|
| `home.cover_story` | Cover story | 커버 스토리 |
| `home.watch` | Watch | 영상으로 보기 |
| `home.from_journals` | From the journals | 최근 학술지 논문 |
| `common.dept` | School of Earth and Environmental Sciences | 지구환경과학부 |

(작업 중 주 세션이 추가한 `common.skip`, `common.snu`, `common.links`, `common.more_news`, `common.lang_fallback`과 `pub_item(anchor=False)`는 적용함.)

## 공통 코드 제안(수정하지 않음)
1. `macros.news_body(p, video=True)`처럼 영상 출력을 끌 수 있으면, 영상을 표지로 쓰는 테마가 매크로를 그대로 쓸 수 있다(지금은 테마에서 본문 블록을 직접 마크업함).
2. `pub_item`에 `title_first=True` 옵션이 있으면 잡지·포트폴리오형 테마가 CSS `order` 없이 제목 우선 배치를 할 수 있다.
3. 발표 페이지용 연도 바로가기 매크로(`pres_year_index`)가 없어 테마에서 직접 만들었다.
4. 뉴스 표지로 쓸 고해상도 이미지(maxresdefault 또는 논문 그림)를 `new_news.py`에서 받도록 하면 큰 표지 품질이 좋아진다.
