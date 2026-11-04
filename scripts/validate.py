#!/usr/bin/env python
"""데이터와 빌드 결과를 검사한다. 오류가 있으면 종료 코드 1.

사용: python scripts/validate.py [--theme all|<이름>] [--data-only] [--report]
검사 항목
  데이터: 필수 필드, DOI 중복, 논문 번호(1..N 연속·최신이 맨 위·연도 내림차순), 뉴스 첨부 파일·DOI·영상 연결,
          구성원 역할·사진, 연구 주제 그림, 예시(placeholder) 항목 경고, 국문 누락 경고
  빌드:   필수 페이지(EN/KO) 존재, EN/KO 페이지 수 일치, 상대 링크·이미지 대상 파일 존재, #앵커 존재, <title>
"""
import argparse
import html.parser
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

import sitelib as L

NEWS_CATS = {'paper', 'award', 'event', 'media', 'lab'}
PRES_TYPES = {'invited', 'keynote', 'oral', 'poster', 'seminar'}


class Report:
    def __init__(self):
        self.errors, self.warnings = [], []

    def err(self, msg):
        self.errors.append(msg)

    def warn(self, msg):
        self.warnings.append(msg)


def missing_ko(v):
    return isinstance(v, dict) and 'en' in v and not v.get('ko')


# ---------------------------------------------------------------- 데이터 검사
def check_data(R):
    D = L.load_all()
    raw = D['pubs_raw']

    # 논문
    seen = {}
    for i, p in enumerate(raw):
        tag = p.get('doi') or f'#{i}'
        for k in ('title', 'authors', 'journal'):
            if not p.get(k):
                R.err(f'publications: {tag} — {k} 없음')
        if not (p.get('year') or p.get('date')):
            R.err(f'publications: {tag} — year/date 없음(화면에서 제외됨)')
        for k in ('year', 'date'):
            if p.get(k) and not L.valid_date(p[k]):
                R.err(f"publications: {tag} — {k} 형식 오류 '{p[k]}' (YYYY / YYYY-MM / YYYY-MM-DD)")
        if p.get('year') and p.get('date') and L.valid_date(p['date']) and L.to_date(p['date']).year != L.pub_year(p):
            R.err(f"publications: {tag} — year({p['year']})와 date({p['date']}) 연도 불일치")
        d = str(p.get('doi') or '').lower()
        if d:
            if d in seen:
                R.err(f'publications: DOI 중복 {d}')
            seen[d] = p
    pubs = D['pubs']
    n = len(pubs)
    nums = [p['num'] for p in pubs]
    if nums != list(range(n, 0, -1)):
        R.err('publications: 번호가 N..1 연속(최신이 맨 위)이 아님')
    for a, b in zip(pubs, pubs[1:]):
        if L.pub_sort_key(a) < L.pub_sort_key(b):
            R.err(f"publications: 정렬 오류 {a.get('doi')} 가 {b.get('doi')} 보다 오래됐는데 위에 있음")
            break
    years = [p['year'] for p in pubs]
    if years != sorted(years, reverse=True):
        R.err('publications: 연도 내림차순이 아님')
    hidden = len(raw) - n
    if hidden:
        R.warn(f'publications: needs_review/hidden 으로 숨긴 항목 {hidden}건')

    for doi in D['pi'].get('selected_dois') or []:
        if doi.lower() not in seen:
            R.warn(f'pi.selected_dois: 논문 목록에 없음 {doi}')

    # 뉴스
    vids = {v['id'] for v in (D['videos'] or {}).get('videos') or []}
    for p in D['news']:
        tag = f"news/{p['slug']}"
        if not re.match(r'^\d{4}-\d{2}-\d{2}-[a-z0-9-]+$', p['slug']):
            R.warn(f'{tag}: 폴더 이름은 YYYY-MM-DD-영문-slug 형식을 권장')
        if not p.get('title'):
            R.err(f'{tag}: title 없음')
        elif missing_ko(p['title']):
            R.warn(f'{tag}: title.ko 없음')
        if not p.get('date'):
            R.err(f'{tag}: date 없음')
        elif not L.valid_date(p['date']):
            R.err(f"{tag}: date 형식 오류 '{p['date']}'")
        if p.get('category') not in NEWS_CATS:
            R.err(f"{tag}: category '{p.get('category')}' 는 {sorted(NEWS_CATS)} 중 하나여야 함")
        for f in [p.get('cover')] + [g.get('file') if isinstance(g, dict) else g for g in p.get('gallery') or []]:
            if f and not re.match(r'^(https?:)?//', str(f)) and not (p['dir'] / f).exists():
                R.err(f'{tag}: 첨부 파일 없음 {f}')
        if p.get('doi') and str(p['doi']).lower() not in seen:
            R.warn(f"{tag}: doi {p['doi']} 가 논문 목록에 없음(링크 카드 대신 DOI 링크만 표시)")
        if p.get('youtube') and not re.match(r'^[\w-]{11}$', str(p['youtube'])):
            R.err(f"{tag}: youtube '{p['youtube']}' 는 11자 영상 ID가 아님(URL이면 ID만 적기)")
        elif p.get('youtube') and p['youtube'] not in vids:
            R.warn(f"{tag}: youtube {p['youtube']} 가 videos.yaml에 없음(썸네일은 YouTube에서 직접 로드)")
        if not p['body'].get('ko'):
            R.warn(f'{tag}: index.ko.md 없음(국문 페이지에 영문 본문 표시)')

    # 구성원
    roles = set(D['members'].get('roles') or [])
    ids = set()
    for alum, group in ((False, D['members'].get('members') or []), (True, D['members'].get('alumni') or [])):
        for m in group:
            tag = f"{'alumni' if alum else 'members'}: {(m.get('name') or {}).get('en', '?')}"
            if not alum and m.get('role') not in roles:
                R.err(f"{tag} — role '{m.get('role')}' 가 roles 목록에 없음")
            if m.get('photo') and not (L.STATIC / m['photo']).exists():
                R.err(f"{tag} — 사진 없음 static/{m['photo']}")
            if m.get('id'):                  # 상세 페이지 people/<id>.html 파일명
                if not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', str(m['id'])):
                    R.err(f"{tag} — id '{m['id']}' 는 영문 소문자·숫자·하이픈만")
                if m['id'] in ids:
                    R.err(f"{tag} — id '{m['id']}' 중복")
                ids.add(m['id'])
    if D['pi'].get('photo') and not (L.STATIC / D['pi']['photo']).exists():
        R.err(f"pi: 사진 없음 static/{D['pi']['photo']}")

    # 연구
    for t in D['research']:
        for img in [t.get('image')] + [f.get('image') for f in t.get('figures') or []]:
            if img and not (L.STATIC / img).exists():
                R.err(f"research/{t.get('key')}: 그림 없음 static/{img}")
        for doi in t.get('dois') or []:
            if doi.lower() not in seen:
                R.warn(f"research/{t.get('key')}: doi {doi} 가 논문 목록에 없음")
        if missing_ko(t.get('title')) or missing_ko(t.get('summary')):
            R.warn(f"research/{t.get('key')}: 국문 누락")

    # 발표
    for p in D['presentations']:
        tag = f"presentations: {p.get('date')} {str(p.get('title'))[:40]}"
        for k in ('date', 'title', 'event'):
            if not p.get(k):
                R.err(f'{tag} — {k} 없음')
        if p.get('date') and not L.valid_date(p['date']):
            R.err(f"{tag} — date 형식 오류 '{p['date']}'")
        if p.get('type') not in PRES_TYPES:
            R.err(f"{tag} — type '{p.get('type')}' 는 {sorted(PRES_TYPES)} 중 하나여야 함")

    ph = [x for x in (D['members'].get('members') or []) + (D['members'].get('alumni') or []) + D['presentations']
          if x.get('placeholder')]
    if ph:
        R.warn(f'예시(placeholder) 항목 {len(ph)}건 남아 있음 — 실제 자료로 교체 필요')
    return D


# ---------------------------------------------------------------- 빌드 검사
class LinkParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.ids, self.dup_ids, self.has_title, self.lang = [], set(), set(), False, None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'html':
            self.lang = a.get('lang')
        if tag == 'title':
            self.has_title = True
        if a.get('id'):
            if a['id'] in self.ids:
                self.dup_ids.add(a['id'])
            self.ids.add(a['id'])
        for k in ('href', 'src'):
            if a.get(k):
                self.links.append((tag, k, a[k]))


def parse(path, cache):
    if path not in cache:
        p = LinkParser()
        p.feed(path.read_text(encoding='utf-8', errors='replace'))
        cache[path] = p
    return cache[path]


def check_site(R, theme_dir, D):
    name = theme_dir.name
    en = sorted(p.relative_to(theme_dir) for p in theme_dir.glob('*.html'))
    ko = sorted(p.relative_to(theme_dir / 'ko') for p in (theme_dir / 'ko').glob('*.html')) if (theme_dir / 'ko').exists() else []
    for page in L.PAGES:
        if Path(f'{page}.html') not in en:
            R.err(f'[{name}] 페이지 없음 {page}.html')
        if Path(f'{page}.html') not in ko:
            R.err(f'[{name}] 페이지 없음 ko/{page}.html')
    want_news = {f"{p['slug']}.html" for p in D['news']}
    en_news_set = {f.name for f in (theme_dir / 'news').glob('*.html')}
    ko_news_set = {f.name for f in (theme_dir / 'ko' / 'news').glob('*.html')}
    en_all = {p.relative_to(theme_dir) for p in theme_dir.rglob('*.html') if p.relative_to(theme_dir).parts[0] != 'ko'}
    ko_all = {p.relative_to(theme_dir / 'ko') for p in (theme_dir / 'ko').rglob('*.html')} if (theme_dir / 'ko').exists() else set()
    if en_all != ko_all:                    # 하위 폴더(news/, people/, research/)까지 EN/KO 짝이 맞는지
        R.err(f'[{name}] EN/KO 페이지 집합 불일치 {sorted(map(str, en_all ^ ko_all))[:10]}')
    for label, got in (('news', en_news_set), ('ko/news', ko_news_set)):
        if got != want_news:
            R.err(f'[{name}] {label} 상세 페이지가 뉴스 목록과 다름: 없음 {sorted(want_news - got)} / 남는 것 {sorted(got - want_news)}')

    # 생성된 논문 페이지: 번호가 N..1 순서로 빠짐없이, 연도 섹션은 내림차순
    n_pub = len(D['pubs'])
    for pp in (theme_dir / 'publications.html', theme_dir / 'ko' / 'publications.html'):
        if not pp.exists():
            continue
        text = pp.read_text(encoding='utf-8', errors='replace')
        nums = [int(x) for x in re.findall(r'\bid="pub-(\d+)"', text)]
        if nums != list(range(n_pub, 0, -1)):
            R.err(f'[{name}] {pp.relative_to(theme_dir)}: 논문 번호 순서 오류(기대 {n_pub}..1, 실제 {len(nums)}개, 처음 {nums[:3]})')
        years = [int(y) for y in re.findall(r'\bid="y(\d{4})"', text)]
        if years != sorted(set(years), reverse=True):
            R.err(f'[{name}] {pp.relative_to(theme_dir)}: 연도 섹션이 내림차순이 아니거나 중복')

    cache, bad = {}, 0
    for f in sorted(theme_dir.rglob('*.html')):
        p = parse(f, cache)
        rel = f.relative_to(theme_dir)
        if not p.has_title:
            R.err(f'[{name}] {rel}: <title> 없음')
        want_lang = 'ko' if rel.parts[0] == 'ko' else 'en'
        if p.lang != want_lang:
            R.err(f'[{name}] {rel}: <html lang="{p.lang}"> — "{want_lang}" 이어야 함')
        if p.dup_ids:
            R.err(f'[{name}] {rel}: 중복 id {sorted(p.dup_ids)[:5]}')
        for tag, attr, url in p.links:
            if url.lower().startswith('javascript:'):
                R.err(f'[{name}] {rel}: javascript: 링크 사용 → {url[:40]}')
                continue
            if re.match(r'^(https?:|mailto:|tel:|data:|//)', url):
                continue
            parts = urlsplit(url)
            if not parts.path:          # '#frag' 같은 문서 내 앵커
                if parts.fragment and parts.fragment not in p.ids:
                    R.err(f'[{name}] {rel}: 앵커 없음 #{parts.fragment}')
                    bad += 1
                continue
            target = (f.parent / unquote(parts.path)).resolve()
            if not target.exists():
                R.err(f'[{name}] {rel}: 깨진 {attr} → {url}')
                bad += 1
                continue
            if target.is_dir():
                R.err(f'[{name}] {rel}: 폴더를 가리킴(file://에서 페이지가 안 열림) → {url}')
                bad += 1
                continue
            if theme_dir.resolve() not in target.parents and target != theme_dir.resolve():
                R.err(f'[{name}] {rel}: 테마 폴더 밖을 가리킴 → {url}')
            if parts.fragment and target.suffix == '.html':
                if parts.fragment not in parse(target, cache).ids:
                    R.err(f'[{name}] {rel}: 앵커 없음 {url}')
                    bad += 1
        if bad > 50:
            R.err(f'[{name}] 링크 오류가 너무 많아 중단')
            break
    return len(en_all) + len(ko_all)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--theme', default='all')
    ap.add_argument('--data-only', action='store_true')
    ap.add_argument('--report', action='store_true', help='reports/validate.md로 저장')
    args = ap.parse_args()

    R = Report()
    D = check_data(R)
    counts = {}
    if not args.data_only:
        themes = L.list_themes() if args.theme == 'all' else [args.theme]
        for th in themes:
            d = L.SITE / th
            if not d.exists():
                R.err(f'[{th}] 빌드 결과 없음 — build.py --theme {th} 먼저 실행')
                continue
            counts[th] = check_site(R, d, D)

    lines = [f"# validate — 논문 {len(D['pubs'])}편(숨김 {len(D['pubs_raw']) - len(D['pubs'])}), "
             f"뉴스 {len(D['news'])}, 발표 {len(D['presentations'])}"]
    for th, c in counts.items():
        lines.append(f'- {th}: {c} pages')
    lines.append(f'\n## 오류 {len(R.errors)}')
    lines += [f'- {e}' for e in R.errors]
    lines.append(f'\n## 경고 {len(R.warnings)}')
    lines += [f'- {w}' for w in R.warnings]
    text = '\n'.join(lines)
    print(text)
    if args.report:
        (L.ROOT / 'reports').mkdir(exist_ok=True)
        (L.ROOT / 'reports' / 'validate.md').write_text(text + '\n', encoding='utf-8')
    sys.exit(1 if R.errors else 0)


if __name__ == '__main__':
    main()
