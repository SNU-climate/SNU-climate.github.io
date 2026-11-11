#!/usr/bin/env python3
"""Move CSL site's Google Fonts CSS & WOFF2 assets onto its own GitHub Pages origin.

Run from a local clone of your GitHub fork:
    py -3 self_host_google_fonts.py  # Windows
    python3 self_host_google_fonts.py  # macOS / Linux

Uses only Python's standard library, no pip packages needed.
"""
from __future__ import annotations

import argparse
import hashlib
import html
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import re
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

HERE = Path('themes/t5.v02')
BASE_REL = HERE / 'templates/base.html'
FONT_REL = HERE / 'assets/fonts'
CSS_NAME = 'google-fonts.css'
UA = (
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
    'AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/131.0.0.0 Safari/537.36'
)
FONT_URL_RE = re.compile(r'https://fonts\.gstatic\.com/[^)\s\'\"]+')
LINK_RE = re.compile(r'<link\s+rel="stylesheet"\s+href="(?P<url>https://fonts\.googleapis\.com/css2\?[^\"]+)"\s*/?>')
LICENSE_URLS = {
    'playfair-display': 'https://raw.githubusercontent.com/google/fonts/main/ofl/playfairdisplay/OFL.txt',
    'noto-serif-kr': 'https://raw.githubusercontent.com/google/fonts/main/ofl/notoserifkr/OFL.txt',
    'source-serif-4': 'https://raw.githubusercontent.com/google/fonts/main/ofl/sourceserif4/OFL.txt',
}


def retrieve(url: str) -> bytes:
    req = Request(url, headers={'User-Agent': UA, 'Accept': '*/*'})
    with urlopen(req, timeout=60) as response:
        data = response.read()
    if not data:
        raise RuntimeError(f'Empty download: {url}')
    return data


def main(root: Path) -> None:
    base_path = root / BASE_REL
    if not base_path.is_file():
        raise SystemExit(f'Could not find {base_path}\nRun this script from your cloned repository root.')
    original = base_path.read_text(encoding='utf-8')
    link = LINK_RE.search(original)
    if not link:
        if "asset('fonts/google-fonts.css')" in original:
            raise SystemExit('Looks like Google Fonts self-hosting is already applied to base.html.')
        raise SystemExit('Google Fonts CSS link was not found in base.html; check the current source.')
    api_url = html.unescape(link.group('url'))
    print('Downloading the Google Fonts CSS stylesheet...')
    stylesheet = retrieve(api_url).decode('utf-8')
    if '@font-face' not in stylesheet:
        raise RuntimeError('Google Fonts API did not return @font-face CSS. Original base.html was not modified.')
    urls = sorted(set(FONT_URL_RE.findall(stylesheet)))
    if not urls:
        raise RuntimeError('No fonts.gstatic.com font links found. Original base.html was not modified.')
    print(f'Found {len(urls)} distinct font files in the stylesheet.')

    dest = root / FONT_REL
    font_dir = dest / 'files'
    font_dir.mkdir(parents=True, exist_ok=True)
    mapping: dict[str, str] = {}
    for url in urls:
        suffix = Path(urlsplit(url).path).suffix.lower()
        if suffix not in ('.woff2', '.woff', '.ttf', '.otf'):
            raise RuntimeError(f'Unexpected font format for {url}; stopping.')
        name = hashlib.sha256(url.encode('utf-8')).hexdigest()[:20] + suffix
        mapping[url] = 'files/' + name

    def get_font(url: str) -> tuple[str, int]:
        file_path = dest / mapping[url]
        if not file_path.exists():
            contents = retrieve(url)
            tmp = file_path.with_name(file_path.name + '.tmp')
            tmp.write_bytes(contents)
            tmp.replace(file_path)
            return url, len(contents)
        return url, 0

    total_bytes = 0
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = [pool.submit(get_font, url) for url in urls]
        for i, future in enumerate(as_completed(futures), start=1):
            _, size = future.result()
            total_bytes += size
            if i % 20 == 0 or i == len(urls):
                print(f'  Font files ready: {i}/{len(urls)}')

    for url, relative in mapping.items():
        stylesheet = stylesheet.replace(url, './' + relative)
    if 'fonts.gstatic.com' in stylesheet:
        raise RuntimeError('An external font link remains in the stylesheet; stopping.')

    print('Downloading the font license notices...')
    for name, url in LICENSE_URLS.items():
        license_text = retrieve(url)
        if b'OPEN FONT LICENSE' not in license_text.upper():
            raise RuntimeError(f'Unexpected license contents for {name}')
        (dest / f'LICENSE-{name}.txt').write_bytes(license_text)

    css_path = dest / CSS_NAME
    css_path.write_text(
        '/* Self-hosted Google Fonts, generated from the existing CSS2 request. */\n'
        + '/* Font files and license notices are stored in this folder. */\n'
        + stylesheet,
        encoding='utf-8',
    )

    updated = original.replace(link.group(0), '<link rel="stylesheet" href="{{ asset(\'fonts/google-fonts.css\') }}">', 1)
    updated = re.sub(r'(?m)^[ \t]*<link rel="preconnect" href="https://fonts\.googleapis\.com">[ \t]*\r?\n', '', updated)
    updated = re.sub(r'(?m)^[ \t]*<link rel="preconnect" href="https://fonts\.gstatic\.com" crossorigin>[ \t]*\r?\n', '', updated)
    base_path.write_text(updated, encoding='utf-8')

    print('\nSuccess!')
    print('  HTML changed:', base_path.relative_to(root))
    print('  CSS created:', css_path.relative_to(root))
    print('  Font files:', len(urls))
    print('  Newly downloaded size: %.1f MB' % (total_bytes / 1024**2))
    print('  License files:', len(LICENSE_URLS))
    print('Keep the Pretendard link unchanged here; fix its SRI separately.')
    print('Review and commit these files on your own fork, then open a PR to the original repo.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Self-host the CSL Google Fonts styles and font binaries')
    parser.add_argument('--root', type=Path, default=Path.cwd(), help='Local clone root (default: current directory)')
    args = parser.parse_args()
    main(args.root.expanduser().resolve())
