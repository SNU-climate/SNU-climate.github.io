# 테마 규약 (모든 테마가 지킬 것)

테마 = `themes/<이름>/` 폴더. 같은 데이터를 각자의 디자인으로 렌더링한다. 참조 구현은 `themes/basic/`.

## 1. 폴더
```
themes/<이름>/
  theme.yaml            # title, concept{en,ko}, palette[색 3~5개]
  templates/            # Jinja2 템플릿(아래 10개 필수)
  assets/               # CSS·JS·폰트·이미지 → 빌드 시 site/<이름>/assets/ 로 복사
```
- 필수 템플릿: `index.html research.html people.html publications.html presentations.html news.html news_post.html videos.html contact.html` (+ 보통 `base.html`)
- 템플릿 검색 경로: `themes/<이름>/templates` → `themes/_shared`. 공통 매크로는 `{% import 'macros.html' as m with context %}`.
- **다른 테마 폴더, `_shared/`, `scripts/`, `data/`, `content/`는 수정하지 않는다.** 공통 기능이 꼭 필요하면 보고서에 제안만 적는다.

## 2. 빌드·검증
```
bash -lc "module load anaconda3/2023.03 && cd /data5/CSL_homepage/first_draft && python scripts/build.py --theme <이름> && python scripts/validate.py --theme <이름>"
```
- 완료 기준: 빌드 성공, validate **오류 0**(경고는 placeholder 1건만 허용), `site/<이름>/`에 EN 8 + KO 8 + 뉴스 상세(EN/KO) 페이지.
- 스크린샷(가능할 때): `node /data5/CSL_homepage/first_draft/scripts/shot.mjs <이름>` → `site/_shots/<이름>.png`, `<이름>_mobile.png`. 이미지를 직접 열어 겹침·넘침·대비를 확인한다.

## 3. 템플릿 컨텍스트 (scripts/build.py `make_ctx`)
| 이름 | 내용 |
|---|---|
| `lang`, `other_lang` | `'en'` / `'ko'` |
| `page` | 현재 페이지 키(`index`, `research`, …, 뉴스 상세는 `news`) |
| `nav` | `[{key, label, url, active}]` 메뉴 |
| `alt_url` | 같은 페이지의 다른 언어 URL (언어 토글) |
| `page_title`, `lab_name` | `<title>`용, 연구실 이름(현재 언어) |
| `site` | `data/site.yaml` (lab.name/affiliation/tagline/intro, contact, links, home.*개수) |
| `pi` | `data/pi.yaml` (name, title, roles, bio, interests, education, career, service, photo) |
| `research` | 주제 목록. 각 항목 `key, title, summary, image, regions[[lat,lon]], pubs[논문], video_items[영상]` |
| `member_groups` | `[(role키, [구성원])]` 비어 있지 않은 역할만. 라벨은 `t('people.role.' ~ role)` |
| `alumni`, `members_all` | 졸업생, 전체 구성원 |
| `pubs` | 표시할 논문, **최신순**, 각 `num`(오래된 것=1), `year, date, title, authors, journal, volume, issue, pages, doi, corresponding, featured, image, links` |
| `pubs_by_year` | `[(year, [논문])]` 연도 내림차순 |
| `selected_pubs`, `featured_pubs` | 대표 논문 |
| `presentations`, `pres_by_year` | 발표(최신순), `date, event, location, title, presenters, type, link, placeholder` |
| `news` | 뉴스(최신순). `slug, title, date, category, summary, cover, youtube, doi, gallery, pub(연결 논문), video` |
| `post`, `body_html`, `body_fallback` | 뉴스 상세 페이지에서만 |
| `videos`, `channel` | 영상(최신순; featured 우선) `id, title, published, description, thumb, pub` / 채널 `url, title` |
| `stats` | `pubs, first_year, last_year, per_year[(y,n)], top_journals[(j,n)], members, videos, news, presentations` |
| `has_placeholders`, `build_date`, `theme` | |

함수: `t('키')`(i18n.yaml 문구), `tr(값)`({en,ko} → 현재 언어), `fmt_date(d, style='long'|'month'|'year')`, `md(text)`,
`rich(title)`(논문 제목: sub/sup/i 허용), `authors(p)`(구성원 굵게 `<strong class="au-me">`), `cite(p)`, `doi_url(p)`,
`page_url('research')`, `news_url(post)`, `pub_url(p)`(`publications.html#pub-N`), `asset('style.css')`(테마 assets),
`static('videos/ID.jpg')`(공용 정적 파일), `cover_url(post)`, `video_thumb(v)`, `youtube_url(id)`, `yt_html(id, title)`,
`latest(n)`(뉴스·논문·발표 혼합 피드 `[{kind,date,title,url,meta,image,obj}]`), `is_me(name)`, `search_text(p)`.

공통 매크로(`themes/_shared/macros.html`): `head_common()`, `scripts_common()`, `lang_switch()`, `sample_badge(x)`,
`pub_item(p)`, `pub_list(pubs_by_year)`, `year_index(pubs_by_year)`, `news_card(p)`, `news_body(post)`, `video_card(v)`,
`youtube(id)`, `pres_item(p)`, `pres_list(pres_by_year)`, `member_card(m)`, `alumni_list(alumni)`, `initials_of(name)`.
매크로가 내는 클래스 이름(`.pub`, `.pub-num`, `.news-card`, `.video-card` 등)에 테마 CSS를 입히면 된다. 직접 마크업해도 된다.

### 3-1. 선택 기능 (Phase 2 추가, 테마에 템플릿이 있을 때만 동작)
| 기능 | 켜는 방법 | 내용 |
|---|---|---|
| 추가 페이지 | `theme.yaml`의 `extra_pages: [about, gallery]` + 같은 이름 템플릿 | 공통 8페이지 외 페이지. EN/KO 둘 다 만든다 |
| Gallery | `gallery.html` 템플릿 | `albums`(뉴스 중 `album: true`) 목록. 이 템플릿이 있으면 `news`와 `latest()`에서 앨범 글이 빠진다(`news_all`은 전체) |
| 구성원 상세 | `member.html` 템플릿 | `people/<id>.html`(id 있는 구성원·졸업생). 컨텍스트 `person`(+ `pubs` 자동 연결, `alumnus`). `member_url(m)`은 템플릿이 없으면 `''` |
| 연구 주제 상세 | `research_topic.html` 템플릿 | `research/<key>.html`. 컨텍스트 `topic`. `topic_url(r)`은 템플릿이 없으면 `research.html#key` |

추가 데이터: 구성원 `id, position, homepage, interests{en:[...]}, education, career, awards`, 졸업생 `id, photo, degree, year, current`,
연구 주제 `themes{en:[...]}`, `figures[{image, caption, doi, pub}]`, 논문 `corr_authors`(교신저자 → `authors()`가 `*` 표시), 뉴스 `album, link, year`.
`tr(값)`은 목록 값을 `, `로 이어 준다. 목록이 필요하면 `tr_list(값)`.

## 4. 반드시 지킬 것
1. `<head>`에 `{{ m.head_common() }}`, `</body>` 앞에 `{{ m.scripts_common() }}` (YouTube 클릭 로드·논문 검색·모바일 메뉴 JS).
2. **모든 URL은 위 함수로 만든다**(상대경로). `/`로 시작하는 절대경로·하드코딩 금지 → file://로 열어도 동작해야 한다.
3. 논문: 최신이 맨 위, 연도별 섹션(내림차순), 번호는 `p.num`(오래된 것 = 1). 검색 기능 유지(`data-pub-search`, `data-pub-item`, `data-pub-year`, `data-pub-count`, `data-pub-empty` — `m.pub_list`가 넣어 준다). 각 논문 요소 `id="pub-{{p.num}}"`.
4. 언어 토글(`m.lang_switch()` 또는 `alt_url` 링크)을 모든 페이지 헤더에 둔다. 화면 문구는 `t()`/`tr()`로만 쓰고 하드코딩하지 않는다(테마 고유 장식 문구는 예외).
5. YouTube는 `yt_html()`/`m.video_card()`(클릭해야 iframe 로드). 페이지 로드 시 iframe 자동 삽입 금지.
6. 모바일 메뉴: 버튼 `data-nav-toggle aria-controls="nav-id" aria-expanded="false"` → 대상에 `data-open` 속성이 토글된다.
7. 반응형: 폭 360px에서 가로 스크롤 없음, 좌우 여백 ≥ 16px. 라이트/다크(`prefers-color-scheme`) 둘 다 읽기 좋게(다크 전용 테마는 그 자체로 대비 확보).
8. 빈 데이터 대응: 구성원·발표·뉴스가 0개여도 깨지지 않게(`{% else %}` + `t('common.empty')`). `placeholder: true` 항목에는 `m.sample_badge(x)`.
9. 외부 라이브러리는 `assets/vendor/`에 파일로 넣는다(CDN 의존 금지). 웹폰트만 예외로 CDN 허용(jsdelivr Pretendard, Google Fonts) — 실패 시 시스템 글꼴로 대체되게 font-family 체인을 둔다.
10. 접근성: 이미지 alt, 메뉴 `aria-current="page"`, 키보드 포커스 표시, 본문 대비 4.5:1 이상.
11. 데이터를 지어내지 않는다. 장식용 숫자·그래프는 `stats` 등 실제 데이터에서만 만든다.
