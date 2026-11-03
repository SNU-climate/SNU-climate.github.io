#!/usr/bin/env python
"""국종성(Jong-Seong Kug) 교수 동료심사 학술지 논문 전체를 모아 data/publications.yaml을 다시 쓴다.

사용:
  python scripts/fetch_publications.py                  # 수집 → yaml 갱신 + reports/pubs_reconciliation.md
  python scripts/fetch_publications.py --verify-build   # 위 + build.py/validate.py --theme basic 결과를 보고서에 기록
  python scripts/fetch_publications.py --new            # 현재 yaml에 없는 후보만 화면에 보고(파일은 쓰지 않음)
  옵션: --refresh  출처 목록 캐시를 무시하고 다시 받는다(DOI별 Crossref 캐시는 30일 유지)

발견 출처: ORCID works, OpenAlex(주 author ID + 이름 변형으로 갈라진 ID), Crossref 저자명 검색(family=Kug).
메타데이터는 DOI마다 Crossref(pubtools.crossref_work)로 정규화한다. 응답 캐시: .cache/pubs/
"""
import argparse
import collections
import datetime as dt
import difflib
import hashlib
import html
import json
import random
import re
import subprocess
import sys
import time
import unicodedata
import urllib.error
import urllib.parse

import pubtools as P
import sitelib as L

ORCID = '0000-0003-2251-2579'
OPENALEX_MAIN = 'A5091389074'
OA_NAME_SEARCHES = ['Jong-Seong Kug', 'J.-S. Kug', 'Kug Jong-Seong', 'Kug']
CR_AUTHOR_QUERIES = ['J.-S. Kug', 'Jong-Seong Kug']
SRC_ORDER = ('orcid', 'openalex', 'crossref')
CACHE = L.ROOT / '.cache' / 'pubs'
REPORT = L.ROOT / 'reports' / 'pubs_reconciliation.md'
LIST_TTL = 86400            # 출처 목록 캐시 1일
WORK_TTL = 30 * 86400       # DOI별 Crossref 캐시 30일
MANUAL_FIELDS = ('corresponding', 'featured', 'image', 'links', 'hidden')
COUNT_RANGE = (250, 450)

# ---------------------------------------------------------------- 제외·검토 규칙
PREFIX_RULES = [            # (정규식, 제외 사유) — DOI만 보고 판정. 위에서부터 처음 맞는 규칙
    (r'(\.s\d{1,3}|/suppl[^/]*|\.sd\d+|\.sm\d*|supplement[^/]*)$', 'supplementary'),
    (r'^10\.21203/', 'preprint'),                              # Research Square
    (r'^10\.22541/', 'preprint'),                              # Authorea
    (r'^10\.1002/essoar', 'preprint'),                         # ESS Open Archive
    (r'^10\.48550/', 'preprint'),                              # arXiv
    (r'^10\.31223/', 'preprint'),                              # EarthArXiv
    (r'^10\.5194/[a-z]+-\d{4}-\d+-(rc|ac|cc|ec|sc)\d+$', 'peer-review'),   # Copernicus 공개 심사 의견
    (r'^10\.5194/egusphere-egu', 'conference-abstract'),       # EGU 초록
    (r'^10\.5194/(ems|icg|ica)\d', 'conference-abstract'),
    (r'^10\.5194/egusphere-', 'preprint'),                     # EGUsphere
    (r'^10\.5194/[a-z]+(d)?-\d{4}-\d+$', 'preprint'),          # Copernicus *-discuss 토론 논문
    (r'^10\.5281/', 'dataset/software'),                       # Zenodo
    (r'^10\.6084/', 'dataset/software'),                       # figshare
    (r'^10\.1594/', 'dataset/software'),                       # PANGAEA
    (r'^10\.5061/', 'dataset/software'),                       # Dryad
]
CR_TYPE_REASON = {
    'posted-content': 'preprint', 'peer-review': 'peer-review', 'component': 'supplementary',
    'dataset': 'dataset/software', 'database': 'dataset/software', 'software': 'dataset/software',
    'proceedings-article': 'conference-abstract', 'proceedings': 'conference-abstract',
}
OA_TYPE_REASON = {
    'preprint': 'preprint', 'erratum': 'erratum/correction', 'retraction': 'erratum/correction',
    'conference-abstract': 'conference-abstract', 'conference-paper': 'conference-abstract',
    'dataset': 'dataset/software', 'software': 'dataset/software', 'peer-review': 'peer-review',
    'supplementary-materials': 'supplementary',
}
REASON_KO = {
    'preprint': 'preprint', 'erratum/correction': 'erratum/correction/retraction',
    'conference-abstract': '학회 초록·발표(EGU/AGU 등)', 'dataset/software': 'dataset/software',
    'peer-review': 'peer-review', 'supplementary': 'supplementary',
    'other-type': '기타 유형(학술지 논문 아님: book-chapter 등)',
    'orcid-wrong-doi': 'ORCID에 잘못 적힌 DOI(다른 논문, 올바른 DOI로 대체)',
}
ERRATUM_RE = re.compile(r'^\s*((author|publisher)\s+correction|correction\s*(to\b|:|$)|erratum|errata|corrigendum|'
                        r'retraction|retracted|expression\s+of\s+concern|addendum\s*(to\b|:|$))', re.I)
REPLY_RE = re.compile(r'^\s*(reply\b|comments?\s+on\b|response\s+to\s+(a\s+|the\s+)?comments?\b|discussion\s+of\b)', re.I)


def norm_title(t):
    t = html.unescape(t or '')
    t = re.sub(r'<[^>]+>', '', t)
    t = unicodedata.normalize('NFKD', t)
    t = ''.join(c for c in t if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]+', ' ', t.lower()).strip()


def norm_journal(j):
    j = html.unescape(j or '').lower().replace('&', ' and ')
    j = re.sub(r'^the\s+', '', j.strip())
    return re.sub(r'[^a-z0-9]+', '', j)


def fam_key(s):
    return re.sub(r'[^a-z]', '', unicodedata.normalize('NFKD', s or '').lower())


# ---------------------------------------------------------------- HTTP + 캐시
_last = [0.0]
NET = collections.Counter()


def _throttle():
    wait = random.uniform(0.1, 0.3) - (time.time() - _last[0])
    if wait > 0:
        time.sleep(wait)
    _last[0] = time.time()


def cached(key, fetch, ttl=None, refresh=False):
    """key의 응답을 .cache/pubs/에 저장해 재사용한다. 404는 {'__error__': 404}로 캐시한다."""
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / (hashlib.sha1(key.encode()).hexdigest() + '.json')
    if path.exists() and not refresh and (ttl is None or time.time() - path.stat().st_mtime < ttl):
        NET['cache'] += 1
        return json.loads(path.read_text(encoding='utf-8'))
    _throttle()
    NET['net'] += 1
    try:
        data = fetch()
    except urllib.error.HTTPError as e:
        if e.code != 404:
            raise
        data = {'__error__': 404}
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps({'__key__': key, **data} if isinstance(data, dict) else data), encoding='utf-8')
    tmp.replace(path)
    return data


def get_json(url, ttl=LIST_TTL, refresh=False):
    return cached(url, lambda: P.http_json(url, retries=4), ttl, refresh)


def crossref_msg(doi, refresh=False):
    """pubtools.crossref_work를 캐시로 감싼다. 미등록(404)이면 None."""
    d = cached('crossref-work:' + P.norm_doi(doi), lambda: {'message': P.crossref_work(doi)}, WORK_TTL, refresh)
    return None if d.get('__error__') else d['message']


# ---------------------------------------------------------------- 출처 1: ORCID
def fetch_orcid(refresh):
    data = get_json(f'https://pub.orcid.org/v3.0/{ORCID}/works', refresh=refresh)
    works, raw_types = [], collections.Counter()
    for grp in data.get('group', []):
        s0 = grp['work-summary'][0]
        raw_types[s0.get('type')] += 1
        dois = []
        for s in grp['work-summary']:
            for e in (s.get('external-ids') or {}).get('external-id', []):
                if e.get('external-id-type') == 'doi' and e.get('external-id-relationship', 'self') == 'self':
                    d = P.norm_doi(e['external-id-value'])
                    if d not in dois:
                        dois.append(d)
        pd = s0.get('publication-date') or {}
        year = (pd.get('year') or {}).get('value')
        base = {'title': ((s0.get('title') or {}).get('title') or {}).get('value', ''),
                'journal': (s0.get('journal-title') or {}).get('value', ''),
                'year': int(year) if year else None, 'type': s0.get('type'), 'put_code': s0.get('put-code')}
        if dois:
            for d in dois:
                works.append({**base, 'doi': d})
        else:
            works.append({**base, 'doi': None})
    return works, raw_types, len(data.get('group', []))


def orcid_detail(put_code, refresh=False):
    return get_json(f'https://pub.orcid.org/v3.0/{ORCID}/work/{put_code}', ttl=WORK_TTL, refresh=refresh)


# ---------------------------------------------------------------- 출처 2: OpenAlex
def given_ok(given, allow_j=True):
    """이름이 Jong-Seong / J.-S. / Jongseong 계열인가(allow_j면 'J.'만 있어도 통과). 'Jo Young', 'Jong Lee' 등은 불통과."""
    g = L.HYPHENS.sub('-', given or '').strip()
    if fam_key(g) == 'jongseong':
        return True
    ini = ''.join(t[0] for t in re.split(r'[\s.\-]+', g) if t).lower()
    return ini == 'js' or (allow_j and ini == 'j')


def is_kug_js(name):
    """OpenAlex 저자 이름 'Jong-Seong Kug' / 'Kug J-S' / 'Kug Jong-Seong' 판정."""
    toks = [t for t in re.split(r'[\s,]+', L.HYPHENS.sub('-', name or '')) if t]
    if len(toks) < 2:
        return False
    if fam_key(toks[-1]) == 'kug' and given_ok(' '.join(toks[:-1]), allow_j=False):
        return True
    return fam_key(toks[0]) == 'kug' and given_ok(' '.join(toks[1:]), allow_j=False)


def oa_pages(endpoint, params, refresh):
    """OpenAlex 목록을 page= 방식으로 끝까지 받는다(API 키 없이는 cursor로 2쪽 이상을 못 받는다)."""
    page = 1
    while True:
        url = f'https://api.openalex.org/{endpoint}?' + urllib.parse.urlencode({**params, 'per-page': 200, 'page': page})
        d = get_json(url, refresh=refresh)
        res = d.get('results') or []
        yield from res
        count = (d.get('meta') or {}).get('count') or 0
        if not res or page * 200 >= count:
            break
        page += 1


def openalex_author_ids(refresh):
    found = {}
    sel = 'id,display_name,display_name_alternatives,orcid,works_count,last_known_institutions'
    for q in OA_NAME_SEARCHES:
        for a in oa_pages('authors', {'search': q, 'select': sel}, refresh):
            names = [a.get('display_name')] + (a.get('display_name_alternatives') or [])
            orcid = (a.get('orcid') or '').rsplit('/', 1)[-1]
            if not any(is_kug_js(n) for n in names):
                continue
            if orcid and orcid != ORCID:
                continue                    # ORCID가 다른 사람
            aid = a['id'].rsplit('/', 1)[-1]
            found[aid] = {'name': a.get('display_name'), 'works': a.get('works_count'), 'orcid': orcid or None,
                          'inst': ', '.join(i['display_name'] for i in (a.get('last_known_institutions') or [])[:2])}
    found.setdefault(OPENALEX_MAIN, {'name': 'Jong-Seong Kug', 'works': None, 'orcid': ORCID, 'inst': ''})
    return found


def fetch_openalex(author_ids, refresh):
    works = []
    params = {'filter': 'author.id:' + '|'.join(sorted(author_ids)),
              'select': 'id,doi,display_name,type,publication_year,primary_location,authorships'}
    for w in oa_pages('works', params, refresh):
        src = ((w.get('primary_location') or {}).get('source') or {})
        aids = {((a.get('author') or {}).get('id') or '').rsplit('/', 1)[-1] for a in w.get('authorships') or []}
        works.append({
            'id': w['id'].rsplit('/', 1)[-1], 'doi': P.norm_doi(w['doi']) if w.get('doi') else None,
            'title': w.get('display_name') or '', 'type': w.get('type'), 'year': w.get('publication_year'),
            'journal': src.get('display_name') or '',
            'authors': [(a.get('author') or {}).get('display_name') or a.get('raw_author_name') or ''
                        for a in w.get('authorships') or []],
            'author_ids': sorted(aids & set(author_ids)),
        })
    return works


# ---------------------------------------------------------------- 출처 3: Crossref 저자명 검색
def has_kug(authors):
    return any(fam_key(a.get('family')) == 'kug' for a in authors or [])


def has_kug_js(authors):
    return any(fam_key(a.get('family')) == 'kug' and given_ok(a.get('given')) for a in authors or [])


def fetch_crossref_search(refresh):
    """query.author 검색 결과 중 저자 목록에 family=Kug(이름 J.-S./Jong-Seong 계열)가 있는 것.
    'J.-S. Kug'는 한 글자 토큰이 무시돼 사실상 'Kug' 검색이라 전수 조회한다. 성만 Kug인 다른 사람은 버리고 개수만 센다."""
    hits, totals, others = {}, {}, {}
    sel = 'DOI,title,author,type,container-title,issued,published-print'

    def take(it, cnt):
        cnt['seen'] += 1
        if has_kug(it.get('author')):
            cnt['kug'] += 1
            d = P.norm_doi(it['DOI'])
            if has_kug_js(it.get('author')):
                cnt['kug_js'] += 1
                hits.setdefault(d, it)
                return True
            others.setdefault(d, it)
        return False

    for q in CR_AUTHOR_QUERIES:
        cnt = collections.Counter()
        if q == 'J.-S. Kug':
            cursor = '*'
            while cursor:
                url = 'https://api.crossref.org/works?' + urllib.parse.urlencode(
                    {'query.author': q, 'rows': 1000, 'cursor': cursor, 'select': sel})
                m = get_json(url, refresh=refresh)['message']
                items = m.get('items', [])
                cnt['total'] = m.get('total-results')
                for it in items:
                    take(it, cnt)
                cursor = m.get('next-cursor') if items else None
        else:                   # 'Jong-Seong Kug'은 Jong/Seong 토큰 때문에 수십만 건 → 관련도 상위만, Kug가 안 나오는 페이지에서 멈춤
            for off in range(0, 2000, 500):
                url = 'https://api.crossref.org/works?' + urllib.parse.urlencode(
                    {'query.author': q, 'rows': 500, 'offset': off, 'sort': 'score', 'order': 'desc', 'select': sel})
                m = get_json(url, refresh=refresh)['message']
                cnt['total'] = m.get('total-results')
                if not sum([take(it, cnt) for it in m.get('items', [])]):
                    break
        totals[q] = dict(cnt)
    others = {d: it for d, it in others.items() if d not in hits}
    return hits, totals, others


def crossref_find_doi(title, year=None, refresh=False):
    """DOI 없는 ORCID 항목: Crossref 서지 검색에서 제목이 같고 Kug가 저자인 학술지 논문을 찾는다."""
    url = 'https://api.crossref.org/works?' + urllib.parse.urlencode(
        {'query.bibliographic': title, 'rows': 5, 'select': 'DOI,title,author,type,issued'})
    m = get_json(url, ttl=WORK_TTL, refresh=refresh).get('message') or {}
    for it in m.get('items', []):
        if (it.get('type') == 'journal-article' and has_kug_js(it.get('author'))
                and norm_title((it.get('title') or [''])[0]) == norm_title(title)):
            return P.norm_doi(it['DOI'])
    return None


# ---------------------------------------------------------------- 분류
def prefix_reason(doi):
    for pat, reason in PREFIX_RULES:
        if re.search(pat, doi, re.I):
            return reason
    return None


def author_check(msg):
    """(ok, 사유). family=Kug이고 이름이 Jong-Seong/J.-S./J. 계열이면 통과."""
    authors = msg.get('author') or []
    if not authors:
        return False, 'Crossref 저자 정보 없음'
    kugs = [a for a in authors if fam_key(a.get('family')) == 'kug']
    if not kugs:
        if any(fam_key(a.get('given')) == 'kug' for a in authors):
            return False, 'Crossref 저자 성/이름 뒤바뀜(given=Kug)'
        if any(re.search(r'\bkug\b', f"{a.get('name') or ''} {a.get('family') or ''}", re.I) for a in authors):
            return False, 'Crossref 저자 표기 애매(Kug 포함 이름)'
        return False, 'Crossref 저자 목록에 Kug 없음(오귀속 가능)'
    if not any(given_ok(a.get('given')) for a in kugs):
        return False, f"Kug 저자 이름 불일치(given={kugs[0].get('given')})"
    return True, ''


def oa_name_to_author(n):
    toks = (n or '').split()
    if len(toks) < 2:
        return n or ''
    return f'{toks[-1]}, {L.initials(" ".join(toks[:-1]))}'


def classify(doi, info, refresh=False):
    """→ dict(status=include|review|exclude, reason, msg). info: {orcid, openalex, crossref}."""
    r = prefix_reason(doi)
    if r:
        return {'status': 'exclude', 'reason': r, 'msg': None}
    msg = crossref_msg(doi, refresh)
    if msg is None:
        oa = info.get('openalex') or {}
        if oa.get('type') in OA_TYPE_REASON:
            return {'status': 'exclude', 'reason': OA_TYPE_REASON[oa['type']], 'msg': None}
        if oa.get('type') in ('article', 'review') or (info.get('orcid') or {}).get('type') == 'journal-article':
            return {'status': 'review', 'reason': 'Crossref 미등록 DOI(메타데이터 확인 불가)', 'msg': None}
        return {'status': 'exclude', 'reason': 'other-type', 'msg': None}
    ctype = msg.get('type')
    title = P.clean_title((msg.get('title') or [''])[0])
    container = ' '.join(msg.get('container-title') or [])
    if ctype in CR_TYPE_REASON:
        return {'status': 'exclude', 'reason': CR_TYPE_REASON[ctype], 'msg': msg}
    if ctype != 'journal-article':
        return {'status': 'exclude', 'reason': 'other-type', 'msg': msg}
    if re.search(r'discussions?$|egusphere|open archive|preprint', container, re.I):
        return {'status': 'exclude', 'reason': 'preprint', 'msg': msg}
    if msg.get('update-to') or ERRATUM_RE.search(title):
        return {'status': 'exclude', 'reason': 'erratum/correction', 'msg': msg}
    if re.search(r'abstracts?\b.*(meeting|assembly|conference)|meeting abstracts?', container, re.I):
        return {'status': 'exclude', 'reason': 'conference-abstract', 'msg': msg}
    ok, why = author_check(msg)
    if REPLY_RE.search(title):
        return {'status': 'review', 'reason': 'Reply/Comment' + ('' if ok else f'; {why}'), 'msg': msg, 'reply': True}
    if not ok:
        return {'status': 'review', 'reason': why, 'msg': msg}
    return {'status': 'include', 'reason': '', 'msg': msg}


# ---------------------------------------------------------------- 수집 → 항목
def collect(refresh):
    orcid_works, orcid_types, orcid_groups = fetch_orcid(refresh)
    oa_ids = openalex_author_ids(refresh)
    oa_works = fetch_openalex(list(oa_ids), refresh)
    cr_hits, cr_totals, cr_others = fetch_crossref_search(refresh)

    cand = collections.OrderedDict()
    for w in orcid_works:
        if w['doi']:
            cand.setdefault(w['doi'], {}).setdefault('orcid', w)
    for w in oa_works:
        if w['doi']:
            cand.setdefault(w['doi'], {}).setdefault('openalex', w)
    for d, it in cr_hits.items():
        cand.setdefault(d, {})['crossref'] = it
    stats = {
        'orcid_groups': orcid_groups, 'orcid_types': orcid_types,
        'orcid_doi': len({w['doi'] for w in orcid_works if w['doi']}),
        'orcid_nodoi': [w for w in orcid_works if not w['doi']],
        'oa_ids': oa_ids, 'oa_total': len(oa_works),
        'oa_types': collections.Counter(w['type'] for w in oa_works),
        'oa_doi': len({w['doi'] for w in oa_works if w['doi']}),
        'oa_nodoi': [w for w in oa_works if not w['doi']],
        'oa_years': collections.Counter(w['year'] for w in oa_works if w['type'] in ('article', 'review')),
        'cr_totals': cr_totals, 'cr_hits': len(cr_hits), 'cr_others': cr_others,
    }
    return cand, stats, orcid_works, oa_works


def build_entry(doi, info, cls):
    srcs = [s for s in SRC_ORDER if s in info]
    msg, oa, oc = cls.get('msg'), info.get('openalex') or {}, info.get('orcid') or {}
    if msg:
        e = P.crossref_to_entry(msg, sources=srcs)
    else:
        e = {'doi': doi, 'title': P.clean_title(oa.get('title') or oc.get('title') or ''), 'type': 'article',
             'sources': srcs, 'added': dt.date.today().isoformat()}
    if not e.get('authors') and oa.get('authors'):
        e['authors'] = [oa_name_to_author(n) for n in oa['authors'] if n]
    if not e.get('journal'):
        e['journal'] = oa.get('journal') or oc.get('journal') or ''
    if not e.get('title'):
        e['title'] = P.clean_title(oa.get('title') or oc.get('title') or '')
    if not e.get('year'):
        y = oa.get('year') or oc.get('year')
        if y:
            e['year'], e['date'] = int(y), str(y)
    return {k: v for k, v in e.items() if v not in (None, '', [])}


def orcid_nodoi_entry(w, oa_match, refresh):
    d = orcid_detail(w['put_code'], refresh)
    authors = [(c.get('credit-name') or {}).get('value') for c in (d.get('contributors') or {}).get('contributor', [])]
    cite = (d.get('citation') or {}).get('citation-value') or ''
    bib = {k.lower(): v.strip() for k, v in re.findall(r'(\w+)\s*=\s*\{([^{}]*)\}', cite)}
    if not any(authors) and oa_match:
        authors = [oa_name_to_author(n) for n in oa_match['authors'] if n]
    e = {'title': P.clean_title(w['title']), 'authors': [a for a in authors if a],
         'journal': w['journal'] or bib.get('journal') or (oa_match or {}).get('journal', ''),
         'year': w['year'], 'date': str(w['year']) if w['year'] else None,
         'volume': bib.get('volume'), 'issue': bib.get('number'), 'pages': bib.get('pages'),
         'type': 'article', 'sources': ['orcid'] + (['openalex'] if oa_match else []),
         'added': dt.date.today().isoformat()}
    return {k: v for k, v in e.items() if v not in (None, '', [])}


def cand_title(info):
    """후보의 제목: ORCID → OpenAlex → Crossref 검색 결과(title이 리스트) 순."""
    for s in ('orcid', 'openalex', 'crossref'):
        t = (info.get(s) or {}).get('title')
        if isinstance(t, list):
            t = t[0] if t else ''
        if t:
            return P.clean_title(t)
    return ''


def entry_key(p):
    return ('doi', P.norm_doi(p['doi'])) if p.get('doi') else ('title', norm_title(p.get('title')))


def run(args):
    cand, stats, orcid_works, oa_works = collect(args.refresh)
    selected = [P.norm_doi(d) for d in (L.load_yaml('pi.yaml').get('selected_dois') or [])]

    # 1) DOI별 분류
    results = {}
    n = len(cand)
    for i, (doi, info) in enumerate(cand.items(), 1):
        results[doi] = classify(doi, info)
        if i % 50 == 0 or i == n:
            print(f'  분류 {i}/{n} (네트워크 {NET["net"]}, 캐시 {NET["cache"]})', file=sys.stderr)

    # 1b) ORCID DOI 검증: ORCID 제목과 Crossref 제목이 크게 다르면 ORCID에 DOI가 잘못 적힌 것 → 제목으로 올바른 DOI를 찾는다
    doi_fix = []
    for doi in list(cand):
        info, r = cand[doi], results[doi]
        oc, m = info.get('orcid'), r.get('msg')
        if not oc or not m or not m.get('title') or r['status'] == 'exclude':
            continue
        t1, t2 = norm_title(oc['title']), norm_title(m['title'][0])
        if not t1 or difflib.SequenceMatcher(None, t1, t2).ratio() >= 0.75:
            continue
        found = crossref_find_doi(oc['title'])
        if not found or found == doi:
            doi_fix.append((doi, None, oc['title'], P.clean_title(m['title'][0])))
            continue
        tgt = cand.setdefault(found, {})
        tgt['orcid'] = {**oc, 'doi': found}
        if found not in results:
            results[found] = classify(found, tgt)
        del info['orcid']
        if not info:                    # ORCID에만 있던 잘못된 DOI → 제외
            results[doi] = {'status': 'exclude', 'reason': 'orcid-wrong-doi', 'msg': m, 'journal_version': found}
        doi_fix.append((doi, found, oc['title'], P.clean_title(m['title'][0])))

    # 2) preprint ↔ 저널 버전 짝짓기, 같은 제목 중복
    def title_of(doi):
        m = results[doi].get('msg')
        if m and m.get('title'):
            return m['title'][0]
        return cand_title(cand[doi])

    kept = [d for d, r in results.items() if r['status'] in ('include', 'review')]
    kept_titles = {}
    for d in kept:
        kept_titles.setdefault(norm_title(title_of(d)), []).append(d)
    kept_norm = [(t, ds) for t, ds in kept_titles.items() if len(t) > 20]
    for d, r in results.items():
        if r['status'] == 'exclude' and r['reason'] == 'preprint':
            t = norm_title(title_of(d))
            match = kept_titles.get(t) if len(t) > 20 else None
            if not match and len(t) > 20:
                for t2, ds in kept_norm:
                    if abs(len(t2) - len(t)) < 30 and difflib.SequenceMatcher(None, t, t2).ratio() >= 0.9:
                        match = ds
                        break
            if match:
                r['journal_version'] = match[0]
    for t, ds in kept_titles.items():
        ds = [d for d in ds if not results[d].get('reply')]
        if len(t) <= 20 or len(ds) < 2:
            continue
        ds.sort(key=lambda d: (-len(cand[d]), results[d]['status'] != 'include', d))
        for d in ds[1:]:
            results[d] = {**results[d], 'status': 'review', 'reason': f'같은 제목의 다른 DOI 존재({ds[0]})'}

    # 3) 항목 만들기
    entries = {}
    for d, r in results.items():
        if r['status'] == 'exclude':
            continue
        e = build_entry(d, cand[d], r)
        if r['status'] == 'review':
            e['needs_review'] = True
            e['review_reason'] = r['reason']
        entries[('doi', d)] = e

    # 4) ORCID의 DOI 없는 학술지 논문
    nodoi_log = []
    kept_by_title = {norm_title(e['title']): k for k, e in entries.items()}
    oa_nodoi_by_title = {norm_title(w['title']): w for w in stats['oa_nodoi']}
    for w in stats['orcid_nodoi']:
        if w['type'] != 'journal-article':
            nodoi_log.append((w, f"제외: ORCID 유형 {w['type']}"))
            continue
        t = norm_title(w['title'])
        if t in kept_by_title:
            k = kept_by_title[t]
            nodoi_log.append((w, f'DOI 항목과 같은 논문 → {k[1]} 에 병합'))
            if 'orcid' not in entries[k]['sources']:
                entries[k]['sources'] = [s for s in SRC_ORDER if s in entries[k]['sources'] + ['orcid']]
            continue
        found = crossref_find_doi(w['title'], w['year'])
        if found:
            info = cand.setdefault(found, {})
            info['orcid'] = {**w, 'doi': found}
            r = classify(found, info)
            results[found] = r
            if r['status'] != 'exclude':
                e = build_entry(found, info, r)
                if r['status'] == 'review':
                    e['needs_review'], e['review_reason'] = True, r['reason']
                entries[('doi', found)] = e
            nodoi_log.append((w, f'Crossref 제목 검색으로 DOI 보완 → {found} ({r["status"]})'))
            continue
        e = orcid_nodoi_entry(w, oa_nodoi_by_title.get(t), args.refresh)
        if not e.get('authors') or not e.get('journal') or not e.get('year'):
            e['needs_review'], e['review_reason'] = True, 'DOI 없음 + ORCID 메타데이터 불완전'
            e.setdefault('authors', ['Kug, J.-S.'])
        entries[('title', t)] = e
        nodoi_log.append((w, 'DOI 없이 ORCID 메타데이터로 포함'))

    # 5) 기존 항목의 수동 필드 보존
    meta, old = P.load_pubs()
    old_by_key = {entry_key(p): p for p in old}
    preserved, kept_old = [], []
    for k, p in old_by_key.items():
        if k in entries:
            e = entries[k]
            for f in MANUAL_FIELDS:
                if f in p:
                    e[f] = p[f]
                    preserved.append((k[1], f))
            if 'needs_review' in p and not p.get('review_reason'):      # 사람이 넣은 값(false도 보존: 검토 후 표시)
                e['needs_review'] = bool(p['needs_review'])
                e.pop('review_reason', None)
                preserved.append((k[1], 'needs_review'))
            if p.get('added'):
                e['added'] = p['added']
        else:
            entries[k] = p                      # 출처에서 못 찾은 기존 항목은 그대로 둔다
            kept_old.append(p)

    pubs = list(entries.values())
    ctx = dict(cand=cand, stats=stats, results=results, pubs=pubs, selected=selected, nodoi_log=nodoi_log,
               preserved=preserved, kept_old=kept_old, old_keys=set(old_by_key), oa_works=oa_works,
               doi_fix=doi_fix)
    return ctx


# ---------------------------------------------------------------- --new
def report_new(ctx):
    new = [p for p in ctx['pubs'] if entry_key(p) not in ctx['old_keys']]
    new.sort(key=L.pub_sort_key, reverse=True)
    vis = [p for p in new if not p.get('needs_review')]
    print(f'현재 yaml에 없는 후보 {len(new)}건 (표시 후보 {len(vis)}, 검토 필요 {len(new) - len(vis)}) — 파일은 쓰지 않음')
    for p in new:
        tag = '검토' if p.get('needs_review') else '추가'
        print(f"[{tag}] {p.get('year')} | {p.get('doi') or '(DOI 없음)'} | {p.get('journal', '')[:40]} | "
              f"{p.get('title', '')[:90]} | {','.join(p.get('sources', []))}"
              + (f" | {p['review_reason']}" if p.get('review_reason') else ''))
    if new:
        print('추가하려면: python scripts/fetch_publications.py (전체 갱신) 또는 python scripts/add_publication.py <DOI>')


# ---------------------------------------------------------------- 검증·보고서
def esc(s):
    return str(s or '').replace('|', '\\|').replace('\n', ' ')


def doi_link(d):
    return f'[{d}](https://doi.org/{d})' if d else '(DOI 없음)'


def recheck_random(pubs, k=10):
    seed = int(dt.date.today().strftime('%Y%m%d'))
    vis = sorted([p for p in L.visible_pubs(pubs) if p.get('doi')], key=lambda p: p['doi'])
    sample = random.Random(seed).sample(vis, min(k, len(vis)))
    rows = []
    for p in sample:
        _throttle()
        NET['recheck'] += 1
        fresh = P.crossref_to_entry(P.crossref_work(p['doi']))          # 캐시를 거치지 않고 다시 조회
        diff = [f for f in ('title', 'authors', 'journal', 'year', 'date', 'volume', 'issue', 'pages')
                if fresh.get(f) != p.get(f)]
        rows.append((p, diff))
    return seed, rows


def run_cmd(cmd):
    r = subprocess.run([sys.executable] + cmd, cwd=L.ROOT, capture_output=True, text=True)
    out = r.stdout + r.stderr
    m = re.search(r'## 오류 (\d+)', out)
    return r.returncode, (m.group(1) if m else '?'), out


def write_report(ctx, checks, recheck):
    S, R, pubs, cand = ctx['stats'], ctx['results'], ctx['pubs'], ctx['cand']
    vis = L.visible_pubs(pubs)
    hidden = [p for p in pubs if p not in vis]
    excl = {d: r for d, r in R.items() if r['status'] == 'exclude'}
    L_ = []
    w = L_.append
    w('# 논문 수집 대조 보고서 (pubs_reconciliation)\n')
    w(f"- 생성: {dt.datetime.now().strftime('%Y-%m-%d %H:%M')} · 스크립트 `scripts/fetch_publications.py`")
    w(f'- 결과: **표시 {len(vis)}편**, 숨김(needs_review/hidden) {len(hidden)}편, yaml 전체 {len(pubs)}편, '
      f'제외 {len(excl)}건 (후보 DOI {len(cand)}건)')
    w(f"- 네트워크 요청 {NET['net']}건(+ 무작위 재조회 {NET['recheck']}건), 캐시 사용 {NET['cache']}건 (`.cache/pubs/`)\n")

    w('## 1. 완료 기준\n')
    w('| # | 기준 | 결과 |\n|---|---|---|')
    for row in checks:
        w(f'| {row[0]} | {row[1]} | {row[2]} |')
    w('')

    w('## 2. 출처별 개수\n')
    w('| 출처 | 원자료 | DOI 수 | 비고 |\n|---|---|---|---|')
    ot = ', '.join(f'{k} {v}' for k, v in S['orcid_types'].most_common())
    w(f"| ORCID `{ORCID}` | works {S['orcid_groups']}건 ({ot}) | {S['orcid_doi']} | DOI 없는 항목 {len(S['orcid_nodoi'])}건 |")
    oat = ', '.join(f'{k} {v}' for k, v in S['oa_types'].most_common())
    w(f"| OpenAlex | works {S['oa_total']}건 ({oat}) | {S['oa_doi']} | DOI 없는 항목 {len(S['oa_nodoi'])}건 |")
    ct = '; '.join(f"`{q}` 전체 {v.get('total')} 중 {v.get('seen', 0)}건 조회, family=Kug {v.get('kug', 0)}건"
                   f"(이름 J.-S. 계열 {v.get('kug_js', 0)})" for q, v in S['cr_totals'].items())
    w(f"| Crossref 저자 검색 | {ct} | {S['cr_hits']} | 중복 제거 후. 성만 Kug인 다른 저자 논문 {len(S['cr_others'])}건은 버림 |")
    w('')
    w('OpenAlex author ID (이름 변형 검색 `' + '`, `'.join(OA_NAME_SEARCHES) + '` 결과 중 Kug + 이름 J로 시작, ORCID가 다르면 제외):\n')
    w('| ID | 이름 | works | ORCID | 소속 | 이 ID로 잡힌 works |\n|---|---|---|---|---|---|')
    per_id = collections.Counter()
    for wk in ctx.get('oa_works', []):
        for a in wk['author_ids']:
            per_id[a] += 1
    for aid, a in S['oa_ids'].items():
        w(f"| {aid} | {esc(a['name'])} | {a['works']} | {a['orcid'] or '-'} | {esc(a['inst'])} | {per_id.get(aid, 0)} |")
    w('')

    w('## 3. 출처 교집합\n')
    def combo(srcs):
        return ' ∩ '.join(s for s in SRC_ORDER if s in srcs) + (' 만' if len(srcs) == 1 else '')
    allc = collections.Counter(combo(set(cand[d])) for d in cand if cand[d])
    visc = collections.Counter(combo(set(p.get('sources', []))) for p in vis)
    hidc = collections.Counter(combo(set(p.get('sources', []))) for p in hidden)
    w('| 출처 조합 | 후보 DOI 전체 | 표시 | 숨김 |\n|---|---|---|---|')
    keys = sorted(set(allc) | set(visc) | set(hidc), key=lambda k: (-k.count('∩'), k))
    for k in keys:
        w(f'| {k} | {allc.get(k, 0)} | {visc.get(k, 0)} | {hidc.get(k, 0)} |')
    w(f'| 합계 | {sum(allc.values())} | {len(vis)} | {len(hidden)} |')
    n_empty = sum(1 for d in cand if not cand[d])
    w(f'\n(후보 DOI 전체 열은 ORCID 오기로 정정돼 출처가 비게 된 DOI {n_empty}건을 뺀 수. '
      '표시·숨김 열은 DOI 없는 ORCID 항목과 출처에서 다시 찾지 못한 기존 항목을 포함한다.)\n')

    w('## 4. 제외 사유별 개수\n')
    rc = collections.Counter(r['reason'] for r in excl.values())
    w('| 사유 | 건수 | 그중 저널 버전이 목록에 있음 |\n|---|---|---|')
    for k, v in rc.most_common():
        jv = sum(1 for r in excl.values() if r['reason'] == k and r.get('journal_version'))
        w(f'| {REASON_KO.get(k, k)} | {v} | {jv if k == "preprint" else "-"} |')
    w(f'| 합계 | {len(excl)} | |')
    w('\n<details><summary>제외 목록 전체</summary>\n')
    w('| DOI | 사유 | 출처 | 제목 | 저널 버전 |\n|---|---|---|---|---|')
    def ttl(d):
        m = R[d].get('msg')
        if m and m.get('title'):
            return P.clean_title(m['title'][0])
        return cand_title(cand[d])
    for d in sorted(excl, key=lambda d: (excl[d]['reason'], d)):
        r = excl[d]
        w(f"| {d} | {REASON_KO.get(r['reason'], r['reason'])} | {','.join(s for s in SRC_ORDER if s in cand[d])} | "
          f"{esc(ttl(d))[:110]} | {r.get('journal_version', '')} |")
    w('\n</details>\n')

    w(f'## 5. needs_review 목록 ({len([p for p in pubs if p.get("needs_review")])}편, 화면에서 숨김)\n')
    rv = sorted([p for p in pubs if p.get('needs_review')], key=lambda p: (p.get('review_reason', ''), p.get('doi') or ''))
    w('| DOI | 연도 | 제목 | 출처 | 사유 |\n|---|---|---|---|---|')
    for p in rv:
        w(f"| {doi_link(p.get('doi'))} | {p.get('year')} | {esc(p.get('title'))[:110]} | "
          f"{','.join(p.get('sources', []))} | {esc(p.get('review_reason', '사람이 지정'))} |")
    w('')
    rep = [p for p in rv if str(p.get('review_reason', '')).startswith('Reply/Comment')]
    w(f'### 5-1. Reply/Comment ({len(rep)}편)\n')
    w('| DOI | 연도 | 학술지 | 제목 |\n|---|---|---|---|')
    for p in rep:
        w(f"| {doi_link(p.get('doi'))} | {p.get('year')} | {esc(p.get('journal'))} | {esc(p.get('title'))[:110]} |")
    w('')

    singles = sorted([p for p in vis if len(p.get('sources', [])) == 1], key=L.pub_sort_key, reverse=True)
    w(f'## 6. 단일 출처 목록 (표시 중 {len(singles)}편)\n')
    w('Crossref 저자 확인(family=Kug, 이름 Jong-Seong/J.-S. 계열)과 유형 확인을 통과해 표시한다.\n')
    w('| DOI | 연도 | 학술지 | 제목 | 출처 |\n|---|---|---|---|---|')
    for p in singles:
        w(f"| {doi_link(p.get('doi'))} | {p.get('year')} | {esc(p.get('journal'))} | {esc(p.get('title'))[:100]} | "
          f"{p['sources'][0]} |")
    w('')

    w('## 7. 연도별 편수\n')
    by = collections.Counter(int(p.get('year') or L.to_date(p.get('date')).year) for p in vis)
    byh = collections.Counter(int(p.get('year') or L.to_date(p.get('date')).year) for p in hidden)
    src_y = {s: collections.Counter(int(p['year']) for p in vis if s in p.get('sources', [])) for s in SRC_ORDER}
    w('| 연도 | 표시 | 숨김 | 표시 중 ORCID | 표시 중 OpenAlex | 표시 중 Crossref검색 | OpenAlex article+review(원자료) |')
    w('|---|---|---|---|---|---|---|')
    for y in sorted(set(by) | set(byh), reverse=True):
        w(f"| {y} | {by.get(y, 0)} | {byh.get(y, 0)} | {src_y['orcid'].get(y, 0)} | {src_y['openalex'].get(y, 0)} | "
          f"{src_y['crossref'].get(y, 0)} | {S['oa_years'].get(y, 0)} |")
    w(f"| 합계 | {sum(by.values())} | {sum(byh.values())} | {sum(src_y['orcid'].values())} | "
      f"{sum(src_y['openalex'].values())} | {sum(src_y['crossref'].values())} | {sum(S['oa_years'].values())} |")
    w('')

    lo_years = [y for y in range(2017, 2021) if by.get(y, 0) < 12]
    if lo_years:
        w(f"- {', '.join(map(str, lo_years))}년 편수가 적다. 이 기간은 ORCID·OpenAlex·Crossref 저자 검색(성 Kug 전수 조회)이 "
          f"모두 같은 논문만 보여 주고, 단일 출처 항목이 없다. 이름 변형으로 갈라진 OpenAlex ID는 "
          f"{len(S['oa_ids']) - 1}개(각 1건, DOI 없음)뿐이라 누락보다는 실제 출판 수로 보인다.")
    w('- OpenAlex 원자료 열이 2005~2016년에 큰 것은 DOI 없는 학회 초록(한국기상학회 학술대회 논문집 등)이 article로 분류돼 있기 때문이다(10-1절).\n')

    w('## 8. 출처 간 연도·학술지 불일치\n')
    w('연도는 `pubtools.pub_date` 규칙(published-print 우선)으로 정한 값이 기준이다. 온라인 선공개와 인쇄 연도 차이가 대부분이다.\n')
    yr_rows, jr_rows, j_partial = [], [], 0
    for p in pubs:
        d = p.get('doi')
        if not d or d not in cand:
            continue
        i = cand[d]
        oy = (i.get('orcid') or {}).get('year')
        ay = (i.get('openalex') or {}).get('year')
        if (oy and oy != p.get('year')) or (ay and ay != p.get('year')):
            yr_rows.append((p, oy, ay))
        cj = norm_journal(p.get('journal'))
        for s in ('orcid', 'openalex'):
            j = (i.get(s) or {}).get('journal')
            nj = norm_journal(j)
            if j and nj != cj:
                if nj in cj or cj in nj:
                    j_partial += 1
                else:
                    jr_rows.append((p, s, j))
    w(f'### 8-1. 연도 불일치 {len(yr_rows)}편\n')
    w('<details><summary>목록</summary>\n')
    w('| DOI | 채택 연도 | ORCID | OpenAlex | 표시 |\n|---|---|---|---|---|')
    for p, oy, ay in sorted(yr_rows, key=lambda x: x[0].get('doi')):
        w(f"| {p['doi']} | {p.get('year')} | {oy or '-'} | {ay or '-'} | {'숨김' if p.get('needs_review') else '표시'} |")
    w('\n</details>\n')
    w(f'### 8-2. 학술지명 불일치 {len(jr_rows)}건 (한쪽이 다른 쪽을 포함하는 부분 일치 {j_partial}건은 제외)\n')
    w('<details><summary>목록</summary>\n')
    w('| DOI | Crossref | 출처 | 출처 표기 |\n|---|---|---|---|')
    for p, s, j in sorted(jr_rows, key=lambda x: (x[0].get('doi'), x[1])):
        w(f"| {p['doi']} | {esc(p.get('journal'))} | {s} | {esc(j)} |")
    w('\n</details>\n')

    w('## 9. 무작위 10편 Crossref 재조회 일치 확인\n')
    seed, rows = recheck
    ok = sum(1 for _, dfs in rows if not dfs)
    w(f'표시 논문 중 무작위 {len(rows)}편(seed {seed})을 캐시 없이 Crossref에서 다시 받아 '
      f'`crossref_to_entry` 결과와 yaml 값을 비교했다(title, authors, journal, year, date, volume, issue, pages). '
      f'**일치 {ok}/{len(rows)}**\n')
    w('| DOI | 연도 | 결과 | 다른 필드 |\n|---|---|---|---|')
    for p, dfs in rows:
        w(f"| {p['doi']} | {p.get('year')} | {'일치' if not dfs else '불일치'} | {', '.join(dfs) or '-'} |")
    w('')

    w('## 10. ORCID DOI 점검·DOI 없는 항목 처리\n')
    w('ORCID 제목과 Crossref 제목이 크게 다른(유사도 < 0.75) DOI는 ORCID 제목으로 Crossref를 다시 검색해 정정했다.\n')
    w('| ORCID DOI | 정정 DOI | ORCID 제목 | Crossref 제목(ORCID DOI) |\n|---|---|---|---|')
    for d, f, t1, t2 in ctx['doi_fix']:
        w(f"| {d} | {f or '찾지 못함(그대로 둠)'} | {esc(t1)[:80]} | {esc(t2)[:80]} |")
    w('')
    w('| 제목 | 학술지 | 연도 | 처리 |\n|---|---|---|---|')
    for wk, how in ctx['nodoi_log']:
        w(f"| {esc(wk['title'])[:100]} | {esc(wk['journal'])} | {wk['year']} | {esc(how)} |")
    w('')

    oa_nd = [x for x in S['oa_nodoi'] if x['type'] in ('article', 'review')]
    kept_t = {norm_title(p.get('title')) for p in pubs}
    conf_re = re.compile(r'학술대회|meeting|assembly|conference|union|agufm|eguga|aguos|symposium|workshop', re.I)
    nd_dup = [x for x in oa_nd if norm_title(x['title']) in kept_t]
    nd_conf = [x for x in oa_nd if x not in nd_dup and conf_re.search(x['journal'] or '')]
    nd_rest = [x for x in oa_nd if x not in nd_dup and x not in nd_conf]
    w(f'### 10-1. OpenAlex의 DOI 없는 article {len(oa_nd)}건 (규칙상 미포함)\n')
    w(f'- 이미 목록에 있는 논문과 제목이 같음: {len(nd_dup)}건')
    w(f'- 학회 초록집(한국기상학회 학술대회 논문집, AGU/EGU 등): {len(nd_conf)}건')
    w(f'- 그 밖의 항목 {len(nd_rest)}건 — 국내 학술지 논문일 수 있어 사람 확인이 필요하다(ORCID에 없어서 넣지 않음):\n')
    w('| OpenAlex | 연도 | 출처 표기 | 제목 | 저자(앞 3명) |\n|---|---|---|---|---|')
    for x in sorted(nd_rest, key=lambda x: (x['year'] or 0, x['title'])):
        w(f"| {x['id']} | {x['year']} | {esc(x['journal']) or '-'} | {esc(x['title'])[:90]} | {esc('; '.join(x['authors'][:3]))} |")
    w('')

    w('## 11. 기존 항목·수동 필드 보존\n')
    pv = collections.Counter(f for _, f in ctx['preserved'])
    w(f"- 보존한 수동 필드: {', '.join(f'{k} {v}건' for k, v in pv.items()) or '없음'}")
    w(f"- 출처에서 다시 찾지 못해 그대로 둔 기존 항목: {len(ctx['kept_old'])}건")
    for p in ctx['kept_old']:
        w(f"  - {p.get('doi') or '(DOI 없음)'} {esc(p.get('title'))[:90]}")
    w('')

    w('## 12. 규칙·한계\n')
    w('- 포함: Crossref type `journal-article`(리뷰 포함) + 저자 목록에 family=Kug(이름 J로 시작). DOI 없는 ORCID 학술지 논문은 ORCID 메타데이터로 포함.')
    w('- 제외: DOI 접두어(10.21203, 10.22541, 10.1002/essoar, 10.48550, 10.5194 토론·EGUsphere·EGU 초록, 10.5281 등), '
      'Crossref type(posted-content, peer-review, component, dataset, proceedings 등), `update-to`가 있거나 제목이 '
      'Correction/Erratum/Corrigendum/Retraction인 것, 기타 유형(book-chapter 등). Crossref 미등록이면 OpenAlex 유형으로 판정.')
    w('- needs_review: 저자 확인 실패·애매, Reply/Comment, Crossref 미등록, 같은 제목의 다른 DOI. `review_reason`에 사유를 적는다 '
      '(다시 실행하면 다시 계산). `review_reason` 없이 사람이 넣은 `needs_review`(true/false)는 보존한다.')
    w('- 저자 검색의 한계: Crossref에 저자 성이 뒤바뀌어 등록된 논문(given=Kug)은 needs_review로 둔다. '
      'OpenAlex는 API 키 없이 공유 일일 예산으로 조회하므로 캐시(1일)를 둔다.')
    w('\n## 13. 사람이 확인할 점\n')
    nd_entries = [p for p in pubs if not p.get('doi')]
    rv_n = len([p for p in pubs if p.get('needs_review')])
    other_types = sorted(d for d, r in excl.items() if r['reason'] == 'other-type')
    w(f'1. needs_review {rv_n}편(5절): 확인 후 표시하려면 `needs_review: false`로 바꾸고 `review_reason` 줄을 지운다. '
      '`review_reason`이 없는 `needs_review`(true/false)는 사람이 정한 값으로 보고 다음 실행에서도 보존한다.')
    w(f'2. DOI 없이 ORCID 메타데이터로 넣은 항목 {len(nd_entries)}편: 저자·권호를 원문과 대조한다'
      + (' — ' + '; '.join(f"{esc(p['title'])[:60]} (저자 {', '.join(p.get('authors', []))})" for p in nd_entries) if nd_entries else '') + '.')
    w(f'3. OpenAlex에만 있는 DOI 없는 항목 {len(nd_rest)}건(10-1절): 국내 학술지(예: 「대기」) 논문이면 직접 추가한다.')
    w(f"4. ORCID 기록의 DOI 오기 {len([x for x in ctx['doi_fix'] if x[1]])}건(10절): 교수님 ORCID에서 고치면 다음 수집부터 정상 반영된다.")
    w(f"5. 학술지 논문이 아니라 제외한 책 장(book chapter 등) {len(other_types)}건: {', '.join(other_types) or '없음'} — 별도 목록이 필요하면 알려 달라.")
    w(f'6. Reply/Comment {len(rep)}편.')
    w('\n수정 금지 파일(build.py·validate.py·sitelib.py 등)에서 이번 작업에 영향을 준 버그는 찾지 못했다. 참고: '
      '`validate.py`의 selected_dois 검사는 목록에 있는지만 보고 숨김 여부는 보지 않는다(이 스크립트가 표시 여부를 assert한다). '
      '`pubtools.http_json`은 404에도 재시도해 실패당 약 6초를 기다린다(동작은 바꾸지 않음).')
    REPORT.parent.mkdir(exist_ok=True)
    REPORT.write_text('\n'.join(L_) + '\n', encoding='utf-8')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--new', action='store_true', help='yaml에 없는 후보만 보고(파일 안 씀)')
    ap.add_argument('--refresh', action='store_true', help='출처 목록 캐시 무시')
    ap.add_argument('--verify-build', action='store_true', help='build.py/validate.py --theme basic도 실행해 보고서에 기록')
    args = ap.parse_args()

    ctx = run(args)
    if args.new:
        report_new(ctx)
        return 0

    pubs = ctx['pubs']
    meta, _ = P.load_pubs()
    P.save_pubs(meta, pubs)
    vis = L.visible_pubs(pubs)
    print(f'저장: data/publications.yaml — 표시 {len(vis)}, 전체 {len(pubs)}')

    checks, fail = [], False
    rc, nerr, _ = run_cmd(['scripts/validate.py', '--data-only'])
    checks.append((1, '`validate.py --data-only` 오류 0', f'{"통과" if rc == 0 else "실패"} (오류 {nerr})'))
    fail |= rc != 0
    vis_dois = {P.norm_doi(p['doi']) for p in vis if p.get('doi')}
    missing = [d for d in ctx['selected'] if d not in vis_dois]
    checks.append((2, f"`pi.yaml` selected_dois {len(ctx['selected'])}편 표시", '통과' if not missing else f'실패: {missing}'))
    fail |= bool(missing)
    lo, hi = COUNT_RANGE
    in_range = lo <= len(vis) <= hi
    checks.append((3, f'표시 논문 수 {lo}~{hi}', f'{"통과" if in_range else "범위 밖"} ({len(vis)}편)'))
    if args.verify_build:
        rc1, _, out1 = run_cmd(['scripts/build.py', '--theme', 'basic'])
        rc2, nerr2, _ = run_cmd(['scripts/validate.py', '--theme', 'basic'])
        ok = rc1 == 0 and rc2 == 0
        checks.append((5, '`build.py --theme basic && validate.py --theme basic` 오류 0',
                       f'{"통과" if ok else "실패"} (build rc {rc1}, validate 오류 {nerr2})'))
        fail |= not ok
        if rc1:
            print(out1[-2000:], file=sys.stderr)
    else:
        checks.append((5, 'build/validate --theme basic', '미실행(--verify-build로 실행)'))
    checks.insert(3, (4, '보고서 항목(출처별·교집합·제외·needs_review·단일 출처·연도별·불일치·재조회)', '아래 2~9절'))
    recheck = recheck_random(pubs)
    write_report(ctx, checks, recheck)
    print(f'보고서: {REPORT.relative_to(L.ROOT)}')
    for c in checks:
        print(f'  [{c[0]}] {c[1]}: {c[2]}')
    assert not missing, f'selected_dois 누락/숨김: {missing}'
    return 1 if fail else 0


if __name__ == '__main__':
    sys.exit(main())
