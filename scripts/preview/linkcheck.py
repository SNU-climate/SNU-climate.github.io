"""미리보기 폴더 안 모든 HTML의 상대 링크(src/href)가 실제 파일을 가리키는지 검사. 사용: python -I linkcheck.py <폴더>"""
import html.parser
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

root = Path(sys.argv[1]).resolve()


class P(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        for k, v in attrs:
            if k in ('src', 'href') and v:
                self.links.append(v)


bad, n = [], 0
for f in sorted(root.rglob('*.html')):
    p = P()
    p.feed(f.read_text(encoding='utf-8', errors='replace'))
    for u in p.links:
        if re.match(r'^(https?:|mailto:|tel:|data:|//|#|javascript:)', u):
            continue
        n += 1
        t = (f.parent / unquote(urlsplit(u).path)).resolve()
        if not t.is_file() or root not in t.parents:
            bad.append(f'{f.relative_to(root)} → {u}')
print(f'links {n}, broken {len(bad)}')
for b in bad[:20]:
    print(' ', b)
