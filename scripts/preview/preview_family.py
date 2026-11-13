"""claude.ai artifact용 시안 계열 미리보기(한 artifact = 한 계열의 v01·v02).
- 공지·앨범은 최근 글 일부만(파일 수 한도 511개)
- static/·assets/shared/를 루트 한 곳으로 모으고 HTML 안 경로를 고친다
- 모든 페이지 아래쪽에 전환 막대(계열 목록 · 전체 시안 목록 · 버전 바꾸기)
- 테마가 자체 호스팅하는 Google Fonts(assets/fonts, 파일 140여 개)는 빼고 Google Fonts 링크로 바꾼다(파일 수 한도)
- 루트 index.html: 두 버전 카드(캡처·설명·영문/국문 링크)
- 테마가 1개(확정 시안)면 전환 막대·카드 없이 루트 index.html이 곧바로 그 테마의 홈으로 넘어간다(실제 사이트처럼 첫 화면이 홈)
  대신 모든 페이지 오른쪽 아래에 "의견 남기기"(누른 뒤 고른 부분에 claude.ai 댓글 창을 연다)와 "사진 보내기" 버튼.
  게시할 때 capabilities {comments: {composer_only: true}, assets: {upload: "interact"}, db: {}, user: {}}
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
# 확정 시안 미리보기의 "의견 남기기": 버튼을 누르면 고르기 상태가 된다(빨간 커서, 마우스가 올라간 부분에 빨간 테두리).
# 그 상태에서 누른 부분(글자를 드래그했으면 그 구간)에 claude.ai 댓글 창(shell composer)을 연다. Esc나 버튼을 다시 누르면 취소.
# 댓글 기능을 쓸 수 없는 보기(claude.ai 밖, 권한 없음)에서는 버튼을 숨긴 채 둔다.
# "사진 보내기"와 함께 미리보기의 shared/shared.js 끝에 붙인다(모든 페이지가 불러온다. 고칠 때 이 파일 하나만 다시 게시하면 된다)
FEEDBACK_HTML = r'''<style>
#csl-fb{position:fixed;right:max(16px,env(safe-area-inset-right,0px));bottom:calc(16px + env(safe-area-inset-bottom,0px));
z-index:2147483000;display:inline-flex;align-items:center;gap:8px;padding:11px 18px;border:0;border-radius:999px;
background:#b5121b;color:#fff;font:700 14px/1.2 -apple-system,"Segoe UI","Apple SD Gothic Neo","Noto Sans KR",sans-serif;
box-shadow:0 6px 20px rgba(0,0,0,.25);cursor:pointer}
#csl-fb[aria-pressed=true]{background:#10203a}
#csl-fb[hidden],#csl-hint[hidden]{display:none}
#csl-fb:focus-visible{outline:3px solid #fff;outline-offset:2px;box-shadow:0 0 0 6px #b5121b}
#csl-hint{position:fixed;left:50%;top:calc(12px + env(safe-area-inset-top,0px));transform:translateX(-50%);z-index:2147483000;
padding:9px 16px;border-radius:999px;background:#b5121b;color:#fff;box-shadow:0 6px 20px rgba(0,0,0,.25);pointer-events:none;
max-width:calc(100vw - 24px);box-sizing:border-box;text-align:center;
font:600 14px/1.35 -apple-system,"Segoe UI","Apple SD Gothic Neo","Noto Sans KR",sans-serif}
html.csl-pick,html.csl-pick *{cursor:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24'%3E%3Ccircle cx='12' cy='12' r='7' fill='%23b5121b' fill-opacity='.25' stroke='%23b5121b' stroke-width='2'/%3E%3Cpath d='M12 1v8M12 15v8M1 12h8M15 12h8' stroke='%23b5121b' stroke-width='2'/%3E%3C/svg%3E") 12 12,crosshair!important}
html.csl-pick #csl-fb{cursor:pointer!important}
.csl-pick-hi{outline:2px solid #b5121b!important;outline-offset:2px!important}
@media print{#csl-fb,#csl-hint{display:none}}
</style>
<button id="csl-fb" type="button" hidden data-uncommentable aria-pressed="false">의견 남기기</button>
<div id="csl-hint" hidden data-uncommentable role="status">의견을 남길 부분을 누르세요. 글자를 드래그해 고를 수도 있습니다. (취소: Esc)</div>'''
FEEDBACK_JS = r'''(async function(){
var b=document.getElementById("csl-fb"),hint=document.getElementById("csl-hint"),root=document.documentElement;
if(!window.claude||!window.claude.use)return;
var c=null;try{c=await window.claude.use("comments");}catch(e){}
if(!c)return;
b.hidden=false;
var on=false,hi=null,SEL="p,li,h1,h2,h3,h4,h5,figure,figcaption,img,dt,dd,td,th,blockquote,a,button,article,section,header,footer";
function pick(t){if(!t||!t.closest||t.closest("[data-uncommentable]"))return null;return t.closest(SEL)||t;}
function mark(el){if(hi)hi.classList.remove("csl-pick-hi");hi=el;if(hi)hi.classList.add("csl-pick-hi");}
function set(v){on=v;root.classList.toggle("csl-pick",v);hint.hidden=!v;b.textContent=v?"취소 (Esc)":"의견 남기기";
b.setAttribute("aria-pressed",String(v));if(!v)mark(null);}
async function open(target){set(false);
try{await c.openComposer(target);}catch(e){if(e&&(e.code==="unavailable"||e.code==="not_granted"))b.hidden=true;}}
b.addEventListener("click",function(){set(!on);if(on){var s=window.getSelection();if(s)s.removeAllRanges();}});
document.addEventListener("mouseover",function(e){if(on)mark(pick(e.target));},true);
document.addEventListener("click",function(e){
if(!on||(e.target.closest&&e.target.closest("[data-uncommentable]")))return;
e.preventDefault();e.stopPropagation();
var s=window.getSelection();
if(s&&!s.isCollapsed&&s.rangeCount&&String(s).trim()){open({range:s.getRangeAt(0)});return;}
var el=pick(e.target);if(el)open({element:el});},true);
document.addEventListener("keydown",function(e){if(on&&e.key==="Escape"){set(false);b.focus();}});
})();'''
# 확정 시안 미리보기의 "사진 보내기": 사진을 artifact 자산(assets)으로 올리고, 어디에 쓸 사진인지를 db의 uploads에 한 줄 남긴다.
# 게시할 때 capabilities {assets: {upload: "interact"}, db: {}, user: {}}. 올릴 권한이 없는 보기에서는 버튼을 숨긴 채 둔다.
# 올라온 파일은 그림으로만 다룬다(코드·스타일로 불러오지 않는다).
# 페이지마다 넣지 않고 미리보기의 shared/shared.js 끝에 붙인다(모든 페이지가 불러온다. 고칠 때 이 파일 하나만 다시 게시하면 된다)
UPLOAD_HTML = r'''<style>
#csl-up,#csl-up-p{position:fixed;right:max(16px,env(safe-area-inset-right,0px));z-index:2147483000;
font:700 14px/1.2 -apple-system,"Segoe UI","Apple SD Gothic Neo","Noto Sans KR",sans-serif}
#csl-up{bottom:calc(68px + env(safe-area-inset-bottom,0px));padding:11px 18px;border:0;border-radius:999px;background:#10203a;color:#fff;
box-shadow:0 6px 20px rgba(0,0,0,.25);cursor:pointer}
#csl-up-p{bottom:calc(120px + env(safe-area-inset-bottom,0px));width:min(320px,calc(100vw - 32px));box-sizing:border-box;padding:14px;border-radius:14px;
background:#fff;color:#10203a;box-shadow:0 8px 30px rgba(0,0,0,.3);font-weight:500;line-height:1.5}
#csl-up[hidden],#csl-up-p[hidden]{display:none}
#csl-up-p input{display:block;width:100%;box-sizing:border-box;margin:6px 0 10px;font:inherit;color:inherit}
#csl-up-p input[type=text]{padding:8px 10px;border:1px solid #9aa4b5;border-radius:8px;background:#fff}
#csl-up-p button{padding:9px 16px;border:0;border-radius:999px;background:#b5121b;color:#fff;font:inherit;font-weight:700;cursor:pointer}
#csl-up-p button[disabled]{opacity:.5;cursor:default}
#csl-up-msg{margin:10px 0 0;font-size:13px;white-space:pre-line}
#csl-up:focus-visible{outline:3px solid #fff;outline-offset:2px;box-shadow:0 0 0 6px #10203a}
@media print{#csl-up,#csl-up-p{display:none}}
</style>
<button id="csl-up" type="button" hidden data-uncommentable aria-expanded="false" aria-controls="csl-up-p">사진 보내기</button>
<div id="csl-up-p" hidden data-uncommentable role="group" aria-label="사진 보내기">
<label for="csl-up-f">사진 (JPG·PNG·GIF·WebP, 한 장에 20MB까지)</label>
<input id="csl-up-f" type="file" accept="image/jpeg,image/png,image/gif,image/webp" multiple>
<label for="csl-up-n">어디에 쓸 사진인가요?</label>
<input id="csl-up-n" type="text" maxlength="300" placeholder="예: 홍길동 구성원 사진 / 12월 AGU 갤러리">
<button id="csl-up-s" type="button">보내기</button>
<p id="csl-up-msg" role="status"></p>
</div>'''
UPLOAD_JS = r'''(async function(){
var b=document.getElementById("csl-up"),p=document.getElementById("csl-up-p"),f=document.getElementById("csl-up-f"),
n=document.getElementById("csl-up-n"),s=document.getElementById("csl-up-s"),m=document.getElementById("csl-up-msg");
if(!window.claude||!window.claude.use)return;
var a=null,db=null,u=null;
try{var r=await Promise.all([window.claude.use("assets"),window.claude.use("db"),window.claude.use("user")]);a=r[0];db=r[1];u=r[2];}catch(e){}
if(!a||!db)return;
b.hidden=false;
b.addEventListener("click",function(){p.hidden=!p.hidden;b.setAttribute("aria-expanded",String(!p.hidden));if(!p.hidden)f.focus();});
var OK=["image/jpeg","image/png","image/gif","image/webp"],MAX=20*1024*1024;
var WHY={too_large:"20MB를 넘습니다",unsupported_type:"지원하지 않는 형식입니다",quota_or_state:"저장 공간이 가득 찼습니다. 담당자에게 알려 주세요",
rate_limited:"잠시 뒤 다시 보내 주세요",upstream_auth:"페이지를 새로 고친 뒤 다시 보내 주세요",not_granted:"올릴 권한이 없습니다"};
s.addEventListener("click",async function(){
var files=Array.prototype.slice.call(f.files||[]),note=n.value.trim();
if(!files.length){m.textContent="사진을 먼저 골라 주세요.";return;}
if(!note){m.textContent="어디에 쓸 사진인지 한 줄 적어 주세요.";n.focus();return;}
s.disabled=true;var ok=0,bad=[],uid=null;
try{uid=u?await u.id():null;}catch(e){}
for(var i=0;i<files.length;i++){var x=files[i];
m.textContent="보내는 중… ("+(i+1)+"/"+files.length+")";
if(OK.indexOf(x.type)<0){bad.push(x.name+": JPG·PNG·GIF·WebP만 보낼 수 있습니다(HEIC는 JPG로 바꿔 주세요)");continue;}
if(x.size>MAX){bad.push(x.name+": 20MB를 넘습니다");continue;}
try{var res=await a.upload(x);
await db.collection("uploads").add({assetId:res.id,filename:x.name,note:note,page:location.pathname,title:document.title,
uploader:uid,time:new Date().toISOString(),sizeBytes:res.sizeBytes,contentType:res.contentType,done:false});
ok++;}catch(e){bad.push(x.name+": "+(WHY[e&&e.code]||"보내지 못했습니다. 잠시 뒤 다시 해 주세요"));}}
m.textContent=(ok?ok+"장을 보냈습니다. 담당자가 확인 후 반영합니다.":"")+(bad.length?(ok?"\n":"")+bad.join("\n"):"");
if(ok&&!bad.length){f.value="";n.value="";}
s.disabled=false;});
})();'''

# 사이트는 Google Fonts를 자체 호스팅하지만(assets/fonts), 미리보기는 파일 수 한도 때문에 Google Fonts 링크를 쓴다
GFONTS = ('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;0,800;0,900;1,600;1,700'
          '&family=Noto+Serif+KR:wght@500;700;900&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap')


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
    shutil.rmtree(tdir / 'assets' / 'fonts', ignore_errors=True)
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
        t = re.sub(r'href="[^"]*assets/fonts/google-fonts\.css[^"]*"', f'href="{H.escape(GFONTS)}"', t)
        if one:                # 확정 시안: 유튜브 새 탭 표시 + 의견 남기기 버튼(전환 막대 없음)
            snippet = '<script>window.CSL_NO_EMBED=true;</script>'
        else:
            snippet = f'<script>window.CSL_PAGES={json.dumps(pages)};window.CSL_NO_EMBED=true;</script>' + bar(theme, rel)
        t = t.replace('</body>', snippet + '</body>', 1) if '</body>' in t else t + snippet
        f.write_text(t, encoding='utf-8')



def report():
    files = [f for f in out.rglob('*') if f.is_file()]
    print(f'files {len(files)}, MB {sum(f.stat().st_size for f in files) / 1e6:.1f}')


if one:
    with open(out / 'shared' / 'shared.js', 'a', encoding='utf-8') as f:
        # 예전에 게시한 페이지에는 "의견 남기기"가 페이지 안에 들어 있다. 그 버튼은 지우고 새로 넣는다
        f.write('\n/* 미리보기 전용: 의견 남기기 · 사진 보내기 */\ndocument.addEventListener("DOMContentLoaded",function(){'
                'var old=document.getElementById("csl-fb");if(old)old.remove();'
                f'document.body.insertAdjacentHTML("beforeend",{json.dumps(FEEDBACK_HTML + UPLOAD_HTML, ensure_ascii=False)});\n'
                f'{FEEDBACK_JS}\n{UPLOAD_JS}\n}});\n')
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
