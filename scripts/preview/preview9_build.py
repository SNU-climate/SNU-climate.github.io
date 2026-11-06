"""claude.ai artifact용 9개 테마 미리보기 빌드.
- 공지·앨범은 최근 글 일부만(파일 수 한도 511개)
- 테마마다 복사되는 static/·assets/shared/를 루트 한 곳(static/, shared/)으로 모으고 HTML 경로를 고친다
- 모든 페이지 아래쪽에 시안 전환 막대(목록으로 · 다른 시안으로 같은 페이지 열기)를 넣는다
사용: python preview9_build.py <first_draft 스냅숏> <출력 폴더> <공지 수> <앨범 수>"""
import re
import shutil
import sys
from pathlib import Path

src, out = Path(sys.argv[1]), Path(sys.argv[2])
n_news, n_album = int(sys.argv[3]), int(sys.argv[4])
sys.path.insert(0, str(src / 'scripts'))
import build as B      # noqa: E402
import sitelib as L    # noqa: E402

THEMES = [('basic', 'Basic (원본 구조)'), ('t1_classic', 'Classic Academic'), ('t2_minimal', 'Modern Minimal'),
          ('t3_ocean', 'Ocean–Atmosphere'), ('t4_dashboard', 'Climate Dashboard'), ('t5_magazine', 'Science Magazine'),
          ('t6_sidebar', 'Sidebar Portfolio'), ('t7_onepage', 'One-page Scroll'), ('t8_globe', 'Interactive Globe')]

data = L.load_all()
news = [p for p in data['news'] if not p.get('album')][:n_news]
albums = [p for p in data['news'] if p.get('album')][:n_album]
data['news'] = sorted(news + albums, key=lambda p: (L.to_date(p.get('date')), p['slug']), reverse=True)
D = B.derive(data)

for keep in ('index.html', 'shots'):          # 첫 화면·캡처는 남기고 나머지는 새로 만든다
    pass
for d in out.iterdir() if out.exists() else []:
    if d.name not in ('index.html', 'shots'):
        shutil.rmtree(d) if d.is_dir() else d.unlink()
out.mkdir(parents=True, exist_ok=True)

BAR_CSS = ('#csl-pv{position:fixed;left:50%;transform:translateX(-50%);bottom:calc(12px + env(safe-area-inset-bottom,0px));'
           'z-index:2147483000;display:flex;gap:8px;align-items:center;padding:6px 8px 6px 12px;border-radius:999px;'
           'background:rgba(16,26,46,.92);color:#fff;font:600 13px/1.2 -apple-system,"Segoe UI","Apple SD Gothic Neo","Noto Sans KR",sans-serif;'
           'box-shadow:0 6px 24px rgba(0,0,0,.3);max-width:calc(100vw - 24px)}'
           '#csl-pv a{color:#fff;text-decoration:none;white-space:nowrap}#csl-pv a:hover{text-decoration:underline}'
           '#csl-pv label{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}'
           '#csl-pv select{min-width:0;max-width:52vw;font:inherit;color:#10203a;background:#fff;border:0;border-radius:999px;padding:6px 10px}'
           '@media print{#csl-pv{display:none}}')


def bar(theme, rel):
    """theme 폴더 안의 rel 경로 페이지에 넣을 전환 막대 HTML."""
    up = '../' * (len(Path(rel).parts))       # 페이지 위치 → 미리보기 루트
    opts = ''.join(f'<option value="{t}"{" selected" if t == theme else ""}>{name}</option>' for t, name in THEMES)
    return (f'<style>{BAR_CSS}</style><nav id="csl-pv" aria-label="시안 전환">'
            f'<a href="{up}index.html">← 시안 목록</a><label for="csl-pv-s">다른 시안으로 보기</label>'
            f'<select id="csl-pv-s" data-up="{up}" data-rel="{rel}">{opts}</select></nav>'
            '<script>(function(){var s=document.getElementById("csl-pv-s");s.addEventListener("change",function(){'
            'var up=s.dataset.up,rel=s.dataset.rel,t=s.value,ok=window.CSL_PAGES[t]||[];'
            'location.href=up+t+"/"+(ok.indexOf(rel)>=0?rel:(rel.indexOf("ko/")===0?"ko/index.html":"index.html"));});})();</script>')


pages = {}
for theme, _ in THEMES:
    tdir = out / theme
    B.build_theme(theme, D, tdir)
    (tdir / B.BUILD_MARK).unlink()
    # static/ 과 assets/shared/ 를 루트로 모은다(내용은 테마와 무관하게 같다)
    if not (out / 'static').exists():
        shutil.move(str(tdir / 'static'), str(out / 'static'))
    else:
        shutil.rmtree(tdir / 'static')
    if not (out / 'shared').exists():
        shutil.move(str(tdir / 'assets' / 'shared'), str(out / 'shared'))
    else:
        shutil.rmtree(tdir / 'assets' / 'shared')
    pages[theme] = sorted(p.relative_to(tdir).as_posix() for p in tdir.rglob('*.html'))

import json   # noqa: E402
for theme, _ in THEMES:
    tdir = out / theme
    for f in tdir.rglob('*.html'):
        rel = f.relative_to(tdir).as_posix()
        html = f.read_text(encoding='utf-8')
        # 테마 루트 기준 'static/…', 'assets/shared/…' → 미리보기 루트 기준(한 단계 위)
        html = re.sub(r'((?:src|href|data-[\w-]+|content)=")((?:\.\./)*)static/', r'\1\2../static/', html)
        html = re.sub(r'((?:src|href)=")((?:\.\./)*)assets/shared/', r'\1\2../shared/', html)
        html = re.sub(r"url\((['\"]?)((?:\.\./)*)static/", r'url(\1\2../static/', html)
        snippet = f'<script>window.CSL_PAGES={json.dumps(pages)};window.CSL_NO_EMBED=true;</script>' + bar(theme, rel)
        html = html.replace('</body>', snippet + '</body>', 1) if '</body>' in html else html + snippet
        f.write_text(html, encoding='utf-8')

files = [f for f in out.rglob('*') if f.is_file()]
print(f'files {len(files)}, MB {sum(f.stat().st_size for f in files) / 1e6:.1f}, html {sum(1 for f in files if f.suffix == ".html")}')
