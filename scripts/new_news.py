#!/usr/bin/env python
"""뉴스 글 폴더를 만든다: content/news/YYYY-MM-DD-<slug>/{index.md, index.ko.md}

사용 예:
  python scripts/new_news.py --slug enso-paper --category paper \\
      --title-en "New paper on ENSO in Nature" --title-ko "엘니뇨 논문 Nature 게재" \\
      --doi 10.1038/xxxx --youtube VIDEOID --cover ~/fig1.png --image ~/fig2.png
- --date 기본값은 오늘. --cover/--image 파일은 글 폴더로 복사된다(--image는 여러 번 가능 → gallery).
- --doi 논문이 publications.yaml에 없으면 add_publication.py로 먼저 추가하라는 안내를 낸다.
- 만든 뒤 본문(index.md 영문, index.ko.md 국문)을 채우고 build.py → validate.py를 실행한다.
"""
import argparse
import datetime as dt
import re
import shutil
import sys
from pathlib import Path

import yaml

import sitelib as L

CATS = ('paper', 'award', 'event', 'media', 'lab')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--slug', required=True, help='영문 소문자-하이픈 (예: enso-paper)')
    ap.add_argument('--date', default=dt.date.today().isoformat())
    ap.add_argument('--category', choices=CATS, default='lab')
    ap.add_argument('--title-en', required=True)
    ap.add_argument('--title-ko', default='')
    ap.add_argument('--summary-en', default='')
    ap.add_argument('--summary-ko', default='')
    ap.add_argument('--doi')
    ap.add_argument('--youtube', help='YouTube 영상 ID 또는 URL')
    ap.add_argument('--cover', help='표지 그림 파일 경로')
    ap.add_argument('--image', action='append', default=[], help='본문 그림(gallery), 여러 번 지정 가능')
    a = ap.parse_args()

    slug = re.sub(r'[^a-z0-9-]+', '-', a.slug.lower()).strip('-')
    dt.date.fromisoformat(a.date)
    d = L.CONTENT / 'news' / f'{a.date}-{slug}'
    if d.exists():
        sys.exit(f'이미 있음: {d}')
    d.mkdir(parents=True)

    meta = {'title': {'en': a.title_en, 'ko': a.title_ko or a.title_en}, 'date': dt.date.fromisoformat(a.date),
            'category': a.category}
    if a.summary_en or a.summary_ko:
        meta['summary'] = {'en': a.summary_en or a.summary_ko, 'ko': a.summary_ko or a.summary_en}
    if a.doi:
        meta['doi'] = re.sub(r'^(https?://)?(dx\.)?doi\.org/', '', a.doi.strip()).lower()
        dois = {str(p.get('doi', '')).lower() for p in L.load_yaml('publications.yaml').get('publications', [])}
        if meta['doi'] not in dois:
            print(f"[안내] {meta['doi']} 가 논문 목록에 없습니다 → python scripts/add_publication.py {meta['doi']}")
    if a.youtube:
        m = re.search(r'(?:v=|youtu\.be/|shorts/|embed/)?([\w-]{11})(?:[?&].*)?$', a.youtube.strip())
        meta['youtube'] = m.group(1) if m else a.youtube.strip()
    if a.cover:
        src = Path(a.cover).expanduser()
        dst = d / ('cover' + src.suffix.lower())
        shutil.copy2(src, dst)
        meta['cover'] = dst.name
    gallery = []
    for i, img in enumerate(a.image, 1):
        src = Path(img).expanduser()
        dst = d / f'fig{i}{src.suffix.lower()}'
        shutil.copy2(src, dst)
        gallery.append({'file': dst.name, 'caption': {'en': '', 'ko': ''}})
    if gallery:
        meta['gallery'] = gallery

    fm = yaml.safe_dump(meta, allow_unicode=True, sort_keys=False, width=1000)
    (d / 'index.md').write_text(f'---\n{fm}---\n(English body — write here in Markdown.)\n', encoding='utf-8')
    (d / 'index.ko.md').write_text('(국문 본문을 Markdown으로 작성)\n', encoding='utf-8')
    print(f'생성: {d}')


if __name__ == '__main__':
    main()
