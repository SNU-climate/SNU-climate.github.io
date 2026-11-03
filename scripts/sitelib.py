"""데이터 로딩·정규화 공용 모듈 (build.py, validate.py, 관리 스크립트에서 함께 쓴다)."""
import datetime as dt
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / 'data'
CONTENT = ROOT / 'content'
THEMES = ROOT / 'themes'
STATIC = ROOT / 'static'
SITE = ROOT / 'site'
LANGS = ('en', 'ko')
PAGES = ('index', 'research', 'people', 'publications', 'presentations', 'news', 'videos', 'contact')


# ---------------------------------------------------------------- YAML
def load_yaml(path):
    path = Path(path)
    if not path.is_absolute():
        path = DATA / path
    if not path.exists():
        return {}
    with open(path, encoding='utf-8') as f:
        return yaml.safe_load(f) or {}


def dump_yaml(obj, path, header=''):
    text = yaml.safe_dump(obj, allow_unicode=True, sort_keys=False, width=1000)
    path = Path(path)
    tmp = path.with_suffix(path.suffix + '.tmp')
    with open(tmp, 'w', encoding='utf-8') as f:     # 동시에 빌드 중인 프로세스가 반쯤 쓴 파일을 읽지 않도록
        f.write(header + text)
    tmp.replace(path)


# ---------------------------------------------------------------- 날짜
def to_date(v):
    """date / datetime / 'YYYY' / 'YYYY-MM' / 'YYYY-MM-DD' / int → date (정렬용, 모르는 부분은 1로 채움)."""
    if v is None or v == '':
        return dt.date(1900, 1, 1)
    if isinstance(v, dt.datetime):
        return v.date()
    if isinstance(v, dt.date):
        return v
    if isinstance(v, int):
        return dt.date(v, 1, 1)
    parts = [int(x) for x in re.findall(r'\d+', str(v))[:3]]
    while len(parts) < 3:
        parts.append(1)
    return dt.date(*parts)


def date_precision(v):
    """표시용 정밀도: 'day' / 'month' / 'year'."""
    if isinstance(v, (dt.date, dt.datetime)):
        return 'day'
    n = len(re.findall(r'\d+', str(v or '')))
    return {1: 'year', 2: 'month'}.get(n, 'day')


# ---------------------------------------------------------------- 이름
HYPHENS = re.compile('[‐‑‒–—−]')


def name_key(name):
    """'Kug, J.-S.' / 'Kug, Jong-Seong' / 'J.-S. Kug' → 'kug|js' (굵게 표시 매칭용)."""
    name = HYPHENS.sub('-', str(name)).strip()
    if ',' in name:
        family, given = [x.strip() for x in name.split(',', 1)]
    else:
        toks = name.split()
        family, given = (toks[-1], ' '.join(toks[:-1])) if toks else ('', '')
    family = re.sub(r'[^a-z]', '', family.lower())
    initials = ''.join(w[0] for w in re.split(r'[\s.\-]+', given) if w).lower()
    return f'{family}|{initials}'


def same_person(key, keys):
    """성이 같고 이니셜이 같거나 한쪽이 다른 쪽의 앞부분이면 같은 사람으로 본다('kug|j' ~ 'kug|js')."""
    fam, ini = key.split('|', 1)
    for k in keys:
        f2, i2 = k.split('|', 1)
        if fam == f2 and ini and i2 and (ini.startswith(i2) or i2.startswith(ini)):
            return True
    return False


def initials(given):
    """'Jong-Seong' → 'J.-S.', 'Michael J.' → 'M. J.'"""
    out = []
    for tok in re.split(r'(\s+|-)', HYPHENS.sub('-', given).strip()):
        if not tok:
            continue
        if tok == '-':
            out.append('-')
        elif tok.isspace():
            out.append(' ')
        else:
            out.append(tok[0].upper() + '.')
    return ''.join(out).replace('. -', '.-')


# ---------------------------------------------------------------- 논문
def visible_pubs(pubs):
    return [p for p in pubs if not p.get('needs_review') and not p.get('hidden')]


def pub_sort_key(p):
    return (to_date(p.get('date') or p.get('year')), str(p.get('doi') or '').lower(), str(p.get('title') or ''))


def number_pubs(pubs):
    """표시할 논문에 번호를 매긴다: 가장 오래된 논문 = 1, 최신 = N. 반환은 최신순."""
    vis = [dict(p) for p in visible_pubs(pubs)]
    for p in vis:
        if not p.get('year'):
            p['year'] = to_date(p.get('date')).year
        p['year'] = int(p['year'])
    vis.sort(key=pub_sort_key)
    for i, p in enumerate(vis, 1):
        p['num'] = i
    return list(reversed(vis))


def group_by_year(items, year_of=lambda x: x['year']):
    """최신순 리스트 → [(year, [items]), ...] (연도 내림차순, 원래 순서 유지)."""
    groups = []
    for it in items:
        y = year_of(it)
        if not groups or groups[-1][0] != y:
            groups.append((y, []))
        groups[-1][1].append(it)
    return groups


# ---------------------------------------------------------------- 뉴스
FRONT = re.compile(r'^---\s*\n(.*?)\n---\s*\n?(.*)$', re.S)


def split_front_matter(text):
    m = FRONT.match(text)
    if not m:
        return {}, text
    return (yaml.safe_load(m.group(1)) or {}), m.group(2)


def load_news(include_drafts=False):
    posts = []
    root = CONTENT / 'news'
    if not root.exists():
        return posts
    for d in sorted(root.iterdir()):
        if not d.is_dir() or d.name.startswith(('_', '.')):
            continue
        md = d / 'index.md'
        if not md.exists():
            continue
        meta, body_en = split_front_matter(md.read_text(encoding='utf-8'))
        if meta.get('draft') and not include_drafts:
            continue
        body_ko = None
        ko = d / 'index.ko.md'
        if ko.exists():
            meta_ko, body_ko = split_front_matter(ko.read_text(encoding='utf-8'))
            for k, v in meta_ko.items():          # index.ko.md 앞머리 값은 ko 쪽으로 덮어쓴다
                if isinstance(meta.get(k), dict):
                    meta[k] = {**meta[k], 'ko': v}
                else:
                    meta.setdefault(k, v)
        post = dict(meta)
        post['slug'] = d.name
        post['dir'] = d
        post['body'] = {'en': body_en.strip(), 'ko': (body_ko or '').strip() or None}
        post['files'] = sorted(f.name for f in d.iterdir() if f.is_file() and f.suffix.lower() != '.md')
        posts.append(post)
    posts.sort(key=lambda p: (to_date(p.get('date')), p['slug']), reverse=True)
    return posts


# ---------------------------------------------------------------- 전체 데이터
def load_all():
    site = load_yaml('site.yaml')
    members = load_yaml('members.yaml')
    pubs_raw = load_yaml('publications.yaml').get('publications', []) or []
    pres = load_yaml('presentations.yaml').get('presentations', []) or []
    pres = sorted(pres, key=lambda p: to_date(p.get('date')), reverse=True)
    for p in pres:
        p['year'] = to_date(p.get('date')).year
    return {
        'site': site,
        'pi': load_yaml('pi.yaml'),
        'members': members,
        'research': load_yaml('research.yaml').get('topics', []) or [],
        'pubs_raw': pubs_raw,
        'pubs': number_pubs(pubs_raw),
        'presentations': pres,
        'videos': load_yaml('videos.yaml'),
        'i18n': load_yaml('i18n.yaml'),
        'news': load_news(),
    }


def list_themes():
    return sorted(d.name for d in THEMES.iterdir()
                  if d.is_dir() and not d.name.startswith(('_', '.')) and (d / 'templates').is_dir())
