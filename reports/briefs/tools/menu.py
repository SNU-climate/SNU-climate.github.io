import sys, datetime
from bs4 import BeautifulSoup
for ts in (1791342795, 1791349006, 1789168792):
    print(ts, datetime.datetime.utcfromtimestamp(ts))
html = open(sys.argv[1], encoding='utf-8', errors='replace').read()
s = BeautifulSoup(html, 'html.parser')
print('TITLE', s.title.string if s.title else None)
for ul in s.find_all('ul', id=True):
    if 'menu' not in ul['id']:
        continue
    print('== UL', ul['id'])
    def walk(u, d=0):
        for li in u.find_all('li', recursive=False):
            a = li.find('a')
            print('  ' * d, '-', a.get_text(' ', strip=True) if a else '?', '|', a.get('href') if a else '')
            sub = li.find('ul')
            if sub: walk(sub, d + 1)
    walk(ul)
    break
