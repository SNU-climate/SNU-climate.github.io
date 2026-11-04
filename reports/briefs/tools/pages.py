"""WP Rocket 캐시 HTML → 페이지별 본문 텍스트(+이미지/링크) 추출. 사용: python -I pages.py <cache_root> <outdir>"""
import sys, os, re, urllib.parse
from bs4 import BeautifulSoup
root, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
rows = []
for dp, dn, fn in os.walk(root):
    if 'index-https.html' not in fn:
        continue
    rel = os.path.relpath(dp, root)
    slug = urllib.parse.unquote(rel).replace('/', '__') if rel != '.' else 'home'
    s = BeautifulSoup(open(os.path.join(dp, 'index-https.html'), encoding='utf-8', errors='replace'), 'html.parser')
    for t in s(['script', 'style', 'noscript', 'svg']):
        t.decompose()
    for sel in ['header', 'footer', '#page-header', '#page-footer', '.page-header', '.page-footer', '#page-mobile-main-menu', '.page-mobile-main-menu']:
        for t in s.select(sel):
            t.decompose()
    body = s.select_one('#page-main-content') or s.select_one('main') or s.body
    lines = []
    for el in body.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'p', 'li', 'td', 'img', 'a', 'span', 'div']):
        if el.name == 'img':
            src = el.get('data-lazy-src') or el.get('data-src') or el.get('src') or ''
            if src and not src.startswith('data:'):
                lines.append(f'[IMG] {src} alt={el.get("alt","")!r}')
            continue
        if el.name == 'a':
            h = el.get('href', '')
            if h and ('wp-content' in h or 'youtu' in h or 'doi' in h):
                lines.append(f'[LINK] {h} {el.get_text(" ", strip=True)[:80]}')
            continue
        if el.name in ('span', 'div'):
            if el.find(['p', 'div', 'h1', 'h2', 'h3', 'h4', 'li', 'td', 'span']) is not None:
                continue
        txt = el.get_text(' ', strip=True)
        if txt:
            lines.append(('# ' if el.name[0] == 'h' else '') + txt)
    dedup = []
    for l in lines:
        if not dedup or dedup[-1] != l:
            dedup.append(l)
    title = s.title.string.strip() if s.title and s.title.string else ''
    open(os.path.join(out, slug + '.txt'), 'w').write(f'URL: /{rel}/\nTITLE: {title}\n\n' + '\n'.join(dedup))
    rows.append((slug, len(dedup)))
for r in sorted(rows):
    print(*r)
