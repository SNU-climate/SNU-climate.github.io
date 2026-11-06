"""claude.ai artifact용 시안 계열 미리보기(한 artifact = 한 계열의 v01·v02).
- 공지·앨범은 최근 글 일부만(파일 수 한도 511개)
- static/·assets/shared/를 루트 한 곳으로 모으고 HTML 안 경로를 고친다
- 모든 페이지 아래쪽에 전환 막대(계열 목록 · 전체 시안 목록 · 버전 바꾸기)
- 루트 index.html: 두 버전 카드(캡처·설명·영문/국문 링크)
- 테마가 1개(확정 시안)면 전환 막대·카드 없이 루트 index.html이 곧바로 그 테마의 홈으로 넘어간다(실제 사이트처럼 첫 화면이 홈)
  대신 모든 페이지 오른쪽 아래에 "의견 남기기" 버튼(claude.ai 댓글 창을 연다. 게시할 때 capabilities {comments: {composer_only: true}})
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
one = len(themes) == 1
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
# 확정 시안 미리보기의 "의견 남기기": claude.ai 댓글 창(shell composer)을 지금 보고 있는 부분에 연다.
# 댓글 기능을 쓸 수 없는 보기(claude.ai 밖, 권한 없음)에서는 버튼을 숨긴 채 둔다
FEEDBACK = ('<style>#csl-fb{position:fixed;right:max(16px,env(safe-area-inset-right,0px));bottom:calc(16px + env(safe-area-inset-bottom,0px));'
            'z-index:2147483000;display:inline-flex;align-items:center;gap:8px;padding:11px 18px;border:0;border-radius:999px;'
            'background:#b5121b;color:#fff;font:700 14px/1.2 -apple-system,"Segoe UI","Apple SD Gothic Neo","Noto Sans KR",sans-serif;'
            'box-shadow:0 6px 20px rgba(0,0,0,.25);cursor:pointer}#csl-fb[hidden]{display:none}'
            '#csl-fb:focus-visible{outline:3px solid #fff;outline-offset:2px;box-shadow:0 0 0 6px #b5121b}@media print{#csl-fb{display:none}}</style>'
            '<button id="csl-fb" type="button" hidden data-uncommentable>의견 남기기</button>'
            '<script>(async function(){var b=document.getElementById("csl-fb");if(!window.claude||!window.claude.use)return;'
            'var c=null;try{c=await window.claude.use("comments");}catch(e){}if(!c)return;b.hidden=false;'
            'b.addEventListener("click",async function(){var el=document.elementFromPoint(innerWidth/2,innerHeight/3);'
            'el=(el&&el.closest("section,article,header,figure,li,p"))||document.querySelector("main")||document.body;'
            'try{await c.openComposer({element:el});}catch(e){if(e&&(e.code==="unavailable"||e.code==="not_granted"))b.hidden=true;}});})();</script>')


def bar(theme, rel):
    up = '../' * len(Path(rel).parts)
    opts = ''.join(f'<option value="{t}"{" selected" if t == theme else ""}>{H.escape(metas[t].get("title") or t)}</option>'
                   for t in themes)
    return (f'<style>{BAR_CSS}</style><nav id="csl-pv" aria-label="시안 전환">'
            f'<a href="{up}index.html">← {H.escape(family)}</a>'
            f'<a class="pv-all" href="{main_url}" target="_blank" rel="noopener">전체 시안 ↗</a>'
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
        if one:                # 확정 시안: 유튜브 새 탭 표시 + 의견 남기기 버튼(전환 막대 없음)
            snippet = '<script>window.CSL_NO_EMBED=true;</script>' + FEEDBACK
        else:
            snippet = f'<script>window.CSL_PAGES={json.dumps(pages)};window.CSL_NO_EMBED=true;</script>' + bar(theme, rel)
        t = t.replace('</body>', snippet + '</body>', 1) if '</body>' in t else t + snippet
        f.write_text(t, encoding='utf-8')



def report():
    files = [f for f in out.rglob('*') if f.is_file()]
    print(f'files {len(files)}, MB {sum(f.stat().st_size for f in files) / 1e6:.1f}')


if one:
    # 루트 index.html(artifact 첫 화면)은 테마 홈으로 바로 넘긴다. 색은 t5 종이색에 맞춰 넘어가는 순간의 깜박임을 줄인다
    th = themes[0]
    lab = H.escape(B.tr(D['site']['lab']['name'], 'en'))
    (out / 'index.html').write_text(f'''<title>CSL 확정 시안</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
:root {{ --bg:#fbf9f4; --fg:#161513; --link:#b5121b; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --bg:#121110; --fg:#ede9e1; --link:#ff5f56; color-scheme: dark; }} }}
:root[data-theme="dark"] {{ --bg:#121110; --fg:#ede9e1; --link:#ff5f56; color-scheme: dark; }}
body {{ background:var(--bg); color:var(--fg); font:16px/1.7 -apple-system,"Segoe UI","Apple SD Gothic Neo","Noto Sans KR",sans-serif; }}
.wrap {{ max-width:720px; margin:0 auto; padding:32px 16px; }}
a {{ color:var(--link); }}
</style>
<script>location.replace('{th}/index.html');</script>
<div class="wrap"><p><a href="{th}/index.html">{lab}</a> · <a href="{th}/ko/index.html">국문</a></p></div>
''', encoding='utf-8')
    report()
    sys.exit(0)

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
    kind = {'v01': '정제판', 'v02': '확장판'}.get(ver, '')
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
@media (max-width:720px) {{ .grid {{ grid-template-columns:1fr; }} }}
</style>
<header class="band"><div class="wrap">
  <p class="eyebrow">기후시스템연구실 홈페이지 시안 · 확장 버전</p>
  <h1>{H.escape(family)} — v01 · v02</h1>
  <p class="lead">2차 리뷰를 반영한 정제판(v01)과 콘셉트를 확장한 확장판(v02)입니다. 카드를 누르면 사이트가 열리고, 아래쪽 막대에서 버전을 바꾸면 같은 페이지를 다른 버전으로 볼 수 있습니다. <a href="{main_url}" target="_blank" rel="noopener">전체 시안 목록 ↗</a></p>
</div></header>
<main><div class="wrap">
  <div class="grid">
{chr(10).join(cards)}
  </div>
  <p class="note">{limit_note} 이 미리보기 안에서는 유튜브 영상을 삽입할 수 없어, 재생 버튼을 누르면 YouTube가 새 탭으로 열립니다(실제 사이트에서는 페이지 안에서 재생됩니다).</p>
</div></main>
'''
(out / 'index.html').write_text(INDEX, encoding='utf-8')
report()
