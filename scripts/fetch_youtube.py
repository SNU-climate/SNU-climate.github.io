#!/usr/bin/env python
"""연구실 유튜브 채널 RSS에서 최신 영상을 받아 data/videos.yaml을 갱신한다.

사용: python scripts/fetch_youtube.py [--no-thumbs]
- RSS는 최신 15개만 준다. 이전에 받은 영상은 지우지 않고 유지한다(누적).
- featured(홈 화면 고정 영상)와 hidden(숨길 영상 ID) 목록은 손으로 관리하며 이 스크립트가 건드리지 않는다.
- 썸네일은 static/videos/<id>.jpg로 저장한다(오프라인·file:// 미리보기용).
"""
import argparse
import urllib.request
import xml.etree.ElementTree as ET

import sitelib as L
from pubtools import UA

VID_FILE = L.DATA / 'videos.yaml'
HEADER = ('# 유튜브 영상. videos 목록은 scripts/fetch_youtube.py가 자동 갱신한다.\n'
          '# featured: 홈 화면에 먼저 보일 영상 ID / hidden: 사이트에서 숨길 영상 ID (둘 다 수동 관리)\n')
NS = {'a': 'http://www.w3.org/2005/Atom', 'yt': 'http://www.youtube.com/xml/schemas/2015',
      'media': 'http://search.yahoo.com/mrss/'}


def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--no-thumbs', action='store_true')
    ap.add_argument('--refresh-thumbs', action='store_true', help='이미 받은 썸네일도 다시 받기')
    args = ap.parse_args()

    data = L.load_yaml(VID_FILE) or {}
    channel = data.get('channel') or {
        'handle': '@climatesystemlaboratory5423',
        'id': 'UC7gcaZ9FsIEy-KgYDWvkq_A',
        'url': 'https://www.youtube.com/@climatesystemlaboratory5423',
        'title': '기후시스템연구실 (Climate System Laboratory)',
    }
    old = {v['id']: v for v in data.get('videos', []) or []}

    root = ET.fromstring(fetch('https://www.youtube.com/feeds/videos.xml?channel_id=' + channel['id']))
    new = 0
    for e in root.findall('a:entry', NS):
        vid = e.find('yt:videoId', NS).text
        group = e.find('media:group', NS)
        desc = group.find('media:description', NS).text if group is not None else ''
        item = {
            'id': vid,
            'title': e.find('a:title', NS).text.strip(),
            'published': e.find('a:published', NS).text[:10],
            'description': (desc or '').strip()[:400],
            'thumb': f'videos/{vid}.jpg',
        }
        if vid not in old:
            new += 1
        old[vid] = {**old.get(vid, {}), **item}

    vdir = L.STATIC / 'videos'
    vdir.mkdir(parents=True, exist_ok=True)
    if not args.no_thumbs:
        for vid in old:
            f = vdir / f'{vid}.jpg'
            if f.exists() and not args.refresh_thumbs:
                continue
            for size in ('maxresdefault', 'sddefault', 'hqdefault'):   # 고해상도(1280×720)부터 시도
                try:
                    f.write_bytes(fetch(f'https://i.ytimg.com/vi/{vid}/{size}.jpg'))
                    break
                except Exception as ex:  # noqa: BLE001
                    if size == 'hqdefault':
                        print(f'[warn] 썸네일 실패 {vid}: {ex}')

    videos = sorted(old.values(), key=lambda v: v['published'], reverse=True)
    out = {'channel': channel, 'featured': data.get('featured', []) or [],
           'hidden': data.get('hidden', []) or [], 'videos': videos}
    L.dump_yaml(out, VID_FILE, HEADER)
    print(f'새 영상 {new}개, 전체 {len(videos)}개')


if __name__ == '__main__':
    main()
