"""Crossref 메타데이터 → publications.yaml 항목 변환 (add_publication.py, fetch_publications.py 공용)."""
import datetime as dt
import html
import json
import re
import time
import urllib.parse
import urllib.request

import sitelib as L

UA = 'CSL-homepage/1.0 (Climate System Laboratory, Seoul National University; https://climate.snu.ac.kr/)'
PUB_FILE = L.DATA / 'publications.yaml'
PUB_HEADER = (
    '# 논문 목록. 번호는 빌드할 때 자동으로 매긴다(가장 오래된 논문 = 1).\n'
    '# 새 논문은 `python scripts/add_publication.py <DOI>`로 추가한다.\n'
    '# 수동 필드: corresponding(교신저자 여부), featured(주요 논문), image(static/ 기준 그림), links{pdf,data,code},\n'
    '#           corr_authors(* 표시할 교신저자, authors와 같은 표기), note, source(backup 등 출처),\n'
    '#           needs_review(true면 화면에서 숨김), hidden(true면 숨김)\n'
)
KEEP_TAGS = re.compile(r'</?(sub|sup|i|em)>', re.I)


def http_json(url, retries=3):
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'application/json'})
            with urllib.request.urlopen(req, timeout=40) as r:
                return json.load(r)
        except Exception:
            if i == retries - 1:
                raise
            time.sleep(2 * (i + 1))


def norm_doi(doi):
    doi = str(doi).strip()
    doi = re.sub(r'^(https?://)?(dx\.)?doi\.org/', '', doi, flags=re.I)
    doi = re.sub(r'^doi:\s*', '', doi, flags=re.I)
    return doi.lower()


def clean_title(t):
    """Crossref 제목에서 <sub>/<sup>/<i> 외 태그를 지우고 공백을 정리한다."""
    t = html.unescape(t or '')
    t = re.sub(r'<(?!/?(sub|sup|i|em)>)[^>]+>', '', t, flags=re.I)
    t = re.sub(r'<(/?)em>', r'<\1i>', t, flags=re.I)
    t = re.sub(r'\s+', ' ', t).strip()
    return re.sub(r'\s+(<su[bp]>)', r'\1', t, flags=re.I)   # 'CO <sub>2</sub>' → 'CO<sub>2</sub>'


def fmt_author(a):
    family = (a.get('family') or '').strip()
    given = (a.get('given') or '').strip()
    if not family:
        return (a.get('name') or '').strip()
    if family.isupper() and len(family) > 2:
        family = family.title()
    return f'{family}, {L.initials(given)}' if given else family


def _parts(msg, key):
    p = (msg.get(key) or {}).get('date-parts') or [[]]
    return [x for x in p[0] if x] if p and p[0] else []


def pub_date(msg):
    """연도 기준: published-print가 있으면 그것(학술지 권호 연도), 없으면 issued(온라인 공개일)."""
    parts = _parts(msg, 'published-print') or _parts(msg, 'issued') or _parts(msg, 'published-online')
    if not parts:
        return None, None
    year = int(parts[0])
    date = '-'.join(f'{x:02d}' if i else str(x) for i, x in enumerate(parts[:3]))
    return year, date


def crossref_work(doi):
    msg = http_json('https://api.crossref.org/works/' + urllib.parse.quote(norm_doi(doi)))['message']
    return msg


def crossref_to_entry(msg, sources=('crossref',)):
    year, date = pub_date(msg)
    pages = msg.get('page') or msg.get('article-number') or ''
    entry = {
        'doi': norm_doi(msg['DOI']),
        'title': clean_title((msg.get('title') or [''])[0]),
        'authors': [fmt_author(a) for a in msg.get('author', []) if fmt_author(a)],
        'journal': html.unescape((msg.get('container-title') or [''])[0]),
        'year': year,
        'date': date,
        'volume': msg.get('volume') or None,
        'issue': msg.get('issue') or None,
        'pages': str(pages) or None,
        'type': 'article',
        'sources': list(sources),
        'added': dt.date.today().isoformat(),
    }
    if not year:                    # 발행일이 없으면 공개하지 않고 사람이 확인하게 둔다
        entry['needs_review'] = True
    return {k: v for k, v in entry.items() if v not in (None, '', [])}


def load_pubs():
    data = L.load_yaml(PUB_FILE)
    return data.get('meta', {}) or {}, data.get('publications', []) or []


def save_pubs(meta, pubs):
    pubs = sorted(pubs, key=L.pub_sort_key, reverse=True)
    meta = dict(meta or {})
    meta['updated'] = dt.date.today().isoformat()
    meta['count_visible'] = len(L.visible_pubs(pubs))
    meta['count_total'] = len(pubs)
    L.dump_yaml({'meta': meta, 'publications': pubs}, PUB_FILE, PUB_HEADER)
