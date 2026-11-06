"""claude.ai artifact용 시안 계열 미리보기(한 artifact = 한 계열의 v01·v02).
- 공지·앨범은 최근 글 일부만(파일 수 한도 511개)
- static/·assets/shared/를 루트 한 곳으로 모으고 HTML 안 경로를 고친다
- 모든 페이지 아래쪽에 전환 막대(계열 목록 · 전체 시안 목록 · 버전 바꾸기)
- 루트 index.html: 두 버전 카드(캡처·설명·영문/국문 링크)
사용: python preview_family.py <소스 루트> <출력 폴더> <공지 수> <앨범 수> <전체 목록 URL> <계열 이름> <테마...>"""
import html as H
import json
import re
import shutil
import sys
from pathlib import Path

from PIL import Image

src, out = Path(sys.argv[1]), Path(sys.argv[2])
n_news, n_album, main_url, family = int(sys.argv[3]), int(sys.argv[4]), sys.argv[5], sys.argv[6]
themes = sys.argv[7:]
sys.path.insert(0, str(src / 'scripts'))
import build as B      # noqa: E402
import sitelib as L    # noqa: E402

data = L.load_all()
n_news_all = sum(1 for p in data['news'] if not p.get('album'))
n_album_all = sum(1 for p in data['news'] if p.get('album'))
news = [p for p in data['news'] if not p.get('album')][:n_news]
albums = [p for p in data['news'] if p.get('album')][:n_album]
data['news'] = sorted(news + albums, key=lambda p: (L.to_date(p.get('date')), p['slug']), reverse=True)
D = B.derive(data)

if out.exists():
    shutil.rmtree(out)
out.mkdir(parents=True)
metas = {t: (L.load_yaml(src / 'themes' / t / 'theme.yaml') or {}) for t in themes}

BAR_CSS = ('#csl-pv{position:fixed;left:50%;transform:translateX(-50%);bottom:calc(12px + env(safe-area-inset-bottom,0px));'
           'z-index:2147483000;display:flex;gap:10px;align-items:center;padding:6px 8px 6px 12px;border-radius:999px;'
           'background:rgba(16,26,46,.92);color:#fff;font:600 13px/1.2 -apple-system,"Segoe UI","Apple SD Gothic Neo","Noto Sans KR",sans-serif;'
           'box-shadow:0 6px 24px rgba(0,0,0,.3);max-width:calc(100vw - 24px)}'
           '#csl-pv a{color:#fff;text-decoration:none;white-space:nowrap}#csl-pv a:hover{text-decoration:underline}'
           '#csl-pv label{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}'
           '#csl-pv select{min-width:0;max-width:44vw;font:inherit;color:#10203a;background:#fff;border:0;border-radius:999px;padding:6px 10px}'
           '@media (max-width:480px){#csl-pv .pv-all{display:none}}@media print{#csl-pv{display:none}}')


def bar(theme, rel):
    up = '../' * len(Path(rel).parts)
    head = (f'<style>{BAR_CSS}</style><nav id="csl-pv" aria-label="시안 전환">'
            f'<a href="{up}index.html">← {H.escape(family)}</a>'
            f'<a class="pv-all" href="{main_url}" target="_blank" rel="noopener">전체 시안 ↗</a>')
    if len(themes) == 1:       # 버전이 하나면 바꾸기 목록 없음
        return head + '</nav>'
    opts = ''.join(f'<option value="{t}"{" selected" if t == theme else ""}>{H.escape(metas[t].get("title") or t)}</option>'
                   for t in themes)
    return (head +
            f'<label for="csl-pv-s">다른 버전으로 보기</label><select id="csl-pv-s" data-up="{up}" data-rel="{rel}">{opts}</select></nav>'
            '<script>(function(){var s=document.getElementById("csl-pv-s");s.addEventListener("change",function(){'
            'var up=s.dataset.up,rel=s.dataset.rel,t=s.value,ok=window.CSL_PAGES[t]||[];'
            'location.href=up+t+"/"+(ok.indexOf(rel)>=0?rel:(rel.indexOf("ko/")===0?"ko/index.html":"index.html"));});})();</script>')


pages = {}
for theme in themes:
    tdir = out / theme
    B.build_theme(theme, D, tdir)
    (tdir / B.BUILD_MARK).unlink()
    for name, dest in (('static', out / 'static'), ('assets/shared', out / 'shared')):
        s = tdir / name
        if not dest.exists():
            shutil.move(str(s), str(dest))
        else:
            shutil.rmtree(s)
    pages[theme] = sorted(p.relative_to(tdir).as_posix() for p in tdir.rglob('*.html'))

for theme in themes:
    tdir = out / theme
    for f in tdir.rglob('*.html'):
        rel = f.relative_to(tdir).as_posix()
        t = f.read_text(encoding='utf-8')
        # 테마 루트 기준 'static/…', 'assets/shared/…' → 미리보기 루트 기준(한 단계 위). 속성·인라인 JSON·url() 모두
        t = re.sub(r'(["\'(])((?:\.\./)*)static/', r'\1\2../static/', t)
        t = re.sub(r'(["\'(])((?:\.\./)*)assets/shared/', r'\1\2../shared/', t)
        pages_js = f'window.CSL_PAGES={json.dumps(pages)};' if len(themes) > 1 else ''
        snippet = f'<script>{pages_js}window.CSL_NO_EMBED=true;</script>' + bar(theme, rel)
        t = t.replace('</body>', snippet + '</body>', 1) if '</body>' in t else t + snippet
        f.write_text(t, encoding='utf-8')

# 캡처(사이트 _shots의 홈 캡처를 JPEG로)
(out / 'shots').mkdir()
for theme in themes:
    for suf, w in (('', 1200), ('_mobile', 390)):
        p = src / 'site' / '_shots' / f'{theme}{suf}.png'
        if p.exists():
            im = Image.open(p).convert('RGB')
            if im.width > w:
                im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
            im.save(out / 'shots' / f'{theme}{suf}.jpg', quality=82, optimize=True, progressive=True)

cards = []
for theme in themes:
    m = metas[theme]
    ver = theme.split('.', 1)[1] if '.' in theme else ''
    kind = '확정 시안' if len(themes) == 1 else {'v01': '정제판', 'v02': '확장판'}.get(ver, '')
    concept = m.get('concept') or {}
    desc = concept.get('ko') if isinstance(concept, dict) else concept
    cards.append(f'''      <article class="card">
        <a class="thumb" href="{theme}/index.html"><img src="shots/{theme}.jpg" alt="{H.escape(m.get('title') or theme)} 홈 화면"><img class="m" src="shots/{theme}_mobile.jpg" alt=""></a>
        <div class="body">
          <span class="tag">{theme}{(' · ' + kind) if kind else ''}</span>
          <h2>{H.escape(m.get('title') or theme)}</h2>
          <p>{H.escape(desc or '')}</p>
          <div class="btns"><a class="btn" href="{theme}/index.html">영문 사이트</a><a class="btn btn--ghost" href="{theme}/ko/index.html">국문 사이트</a></div>
        </div>
      </article>''')

one = len(themes) == 1      # 테마 1개(확정 시안): 카드 1장을 가로로 넓게, 안내 문구도 확정 시안용
if one:
    eyebrow, heading = '기후시스템연구실 홈페이지 · 확정 시안', H.escape(family)
    lead = '최종 확정한 시안입니다. 카드를 누르면 사이트가 열리고, 사이트 안의 메뉴로 모든 페이지를 볼 수 있습니다.'
else:
    eyebrow, heading = '기후시스템연구실 홈페이지 시안 · 확장 버전', f'{H.escape(family)} — v01 · v02'
    lead = ('2차 리뷰를 반영한 정제판(v01)과 콘셉트를 확장한 확장판(v02)입니다. 카드를 누르면 사이트가 열리고, '
            '아래쪽 막대에서 버전을 바꾸면 같은 페이지를 다른 버전으로 볼 수 있습니다.')

# 미리보기 용량 제한(파일 511개) 안내: 공지를 모두 넣었으면 앨범만 줄였다고 쓴다
if len(news) == n_news_all:
    limit_note = f'미리보기 용량 제한(파일 511개) 때문에 공지·뉴스 {n_news_all}편은 모두 넣고, 갤러리는 최근 {len(albums)}개만 넣었습니다(실제 사이트: 앨범 {n_album_all}개).'
else:
    limit_note = (f'미리보기 용량 제한(파일 511개) 때문에 공지·뉴스는 최근 {len(news)}편, 갤러리는 최근 {len(albums)}개만 넣었습니다'
                  f'(실제 사이트: 공지 {n_news_all}편, 앨범 {n_album_all}개).')

INDEX = f'''<title>CSL 시안 {H.escape(family)}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
/* 레이아웃: 상단 띠 → 버전 카드 2장(눌러서 사이트 열기) → 안내 */
:root {{ --bg:#f5f7fa; --surface:#fff; --fg:#15213a; --muted:#586580; --line:#d9e0ea; --accent:#1d3b6e; --accent-2:#2a78ad; --band:#10284d; --band-fg:#eef3fb; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --bg:#0c1320; --surface:#131d2e; --fg:#e4eaf4; --muted:#96a3b9; --line:#24324a; --accent:#a3c4ff; --accent-2:#6cc0e0; --band:#0a1a33; --band-fg:#e4eaf4; color-scheme: dark; }} }}
:root[data-theme="dark"] {{ --bg:#0c1320; --surface:#131d2e; --fg:#e4eaf4; --muted:#96a3b9; --line:#24324a; --accent:#a3c4ff; --accent-2:#6cc0e0; --band:#0a1a33; --band-fg:#e4eaf4; color-scheme: dark; }}
body {{ background:var(--bg); color:var(--fg); font:16px/1.7 -apple-system,"Segoe UI","Apple SD Gothic Neo","Noto Sans KR",sans-serif; word-break:keep-all; overflow-wrap:break-word; }}
a {{ color:var(--accent-2); }}
.wrap {{ max-width:1180px; margin:0 auto; padding-left:max(16px, env(safe-area-inset-left, 0px)); padding-right:max(16px, env(safe-area-inset-right, 0px)); }}
.band {{ background:var(--band); color:var(--band-fg); }} .band .wrap {{ padding-block:36px 30px; display:grid; gap:10px; }}
.eyebrow {{ margin:0; font-size:.78rem; letter-spacing:.12em; text-transform:uppercase; opacity:.8; }}
h1 {{ margin:0; font-size:clamp(1.6rem, 4vw, 2.4rem); line-height:1.25; text-wrap:balance; }}
.lead {{ margin:0; max-width:46em; opacity:.9; }} .band a {{ color:var(--band-fg); }}
main .wrap {{ padding-block:32px 56px; display:grid; gap:20px; }}
.grid {{ display:grid; grid-template-columns:repeat(2, minmax(0, 1fr)); gap:24px; }}
.card {{ background:var(--surface); border:1px solid var(--line); border-radius:12px; overflow:hidden; display:grid; align-content:start; min-width:0; }}
.thumb {{ position:relative; display:block; border-bottom:1px solid var(--line); }}
.thumb img {{ width:100%; max-width:100%; aspect-ratio:16 / 10; object-fit:cover; object-position:top; display:block; }}
.thumb .m {{ position:absolute; right:12px; bottom:-18px; width:22%; aspect-ratio:390 / 844; border-radius:8px; border:3px solid var(--surface); box-shadow:0 6px 18px rgba(10,20,40,.25); }}
.body {{ padding:28px 18px 18px; display:grid; gap:8px; min-width:0; }}
.tag {{ justify-self:start; font:600 .74rem/1 ui-monospace,monospace; padding:5px 8px; border-radius:4px; background:var(--accent); color:var(--surface); }}
h2 {{ margin:0; font-size:1.2rem; }} .body p {{ margin:0; color:var(--muted); font-size:.93rem; }}
.btns {{ display:flex; flex-wrap:wrap; gap:8px; margin-top:4px; }}
.btn {{ display:inline-block; padding:8px 16px; border-radius:999px; background:var(--accent); color:var(--surface); text-decoration:none; font-weight:700; font-size:.92rem; }}
.btn--ghost {{ background:transparent; color:var(--accent); border:1px solid var(--accent); }}
.btn:focus-visible, .thumb:focus-visible {{ outline:3px solid var(--accent-2); outline-offset:2px; }}
.note {{ margin:0; color:var(--muted); font-size:.88rem; }}
.grid--one {{ grid-template-columns:1fr; }}
.grid--one .card {{ grid-template-columns:minmax(0, 1.5fr) minmax(0, 1fr); }}
.grid--one .thumb {{ border-bottom:0; border-right:1px solid var(--line); }}
.grid--one .body {{ align-content:center; padding:28px; }}
.grid--one .thumb .m {{ bottom:12px; }}
@media (max-width:720px) {{ .grid {{ grid-template-columns:1fr; }} .grid--one .card {{ grid-template-columns:1fr; }} .grid--one .thumb {{ border-right:0; border-bottom:1px solid var(--line); }} }}
</style>
<header class="band"><div class="wrap">
  <p class="eyebrow">{eyebrow}</p>
  <h1>{heading}</h1>
  <p class="lead">{lead} <a href="{main_url}" target="_blank" rel="noopener">전체 시안 목록 ↗</a></p>
</div></header>
<main><div class="wrap">
  <div class="grid{' grid--one' if one else ''}">
{chr(10).join(cards)}
  </div>
  <p class="note">{limit_note} 이 미리보기 안에서는 유튜브 영상을 삽입할 수 없어, 재생 버튼을 누르면 YouTube가 새 탭으로 열립니다(실제 사이트에서는 페이지 안에서 재생됩니다).</p>
</div></main>
'''
(out / 'index.html').write_text(INDEX, encoding='utf-8')
files = [f for f in out.rglob('*') if f.is_file()]
print(f'files {len(files)}, MB {sum(f.stat().st_size for f in files) / 1e6:.1f}')
