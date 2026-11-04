#!/usr/bin/env python
"""데이터(YAML/Markdown) → 정적 HTML 사이트 빌드.

사용:
  python scripts/build.py --theme all                 # 모든 테마 + 템플릿 갤러리(site/index.html)
  python scripts/build.py --theme t1_classic          # 한 테마만 → site/t1_classic/
  python scripts/build.py --theme basic --out dist    # 배포용 폴더로 출력

출력 구조(테마 하나): index.html, research.html, ... , news/<slug>.html (영문)
                     ko/index.html, ko/research.html, ... (국문)
                     assets/(테마 CSS·JS), assets/shared/(공통), static/(이미지·썸네일·뉴스 첨부)
모든 링크는 상대경로라 웹서버에서도, 파일을 직접 열어도 동작한다.
"""
import argparse
import datetime as dt
import re
import shutil
from pathlib import Path
from urllib.parse import quote

import jinja2
import markdown
from markupsafe import Markup, escape

import sitelib as L

MONTHS = 'Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split()
DOI_RE = re.compile(r'10\.\d{4,9}/[^\s"<>)\]]+')
RICH_OK = re.compile(r'&lt;(/?)(sub|sup|i)&gt;')
YT_SHORT = re.compile(r'\[\[youtube:([\w-]{11})\]\]')
YT_ID = re.compile(r'^[\w-]{11}$')
BUILD_MARK = '.csl-build'      # build.py가 만든 출력 폴더 표시(이 파일이 없는 폴더는 지우지 않는다)


# ---------------------------------------------------------------- 언어 독립 헬퍼
def tr(v, lang):
    """{en, ko} → 해당 언어 값(없으면 en). 목록 값은 ', '로 이어 문자열로 돌려준다(목록 그대로는 tr_list)."""
    v = tr_list(v, lang) if isinstance(v, dict) else v
    if isinstance(v, list):
        return ', '.join(str(x) for x in v)
    return '' if v is None else v


def tr_list(v, lang):
    """{en: [...], ko: [...]} 또는 [...] → 해당 언어 목록."""
    if isinstance(v, dict):
        v = v.get(lang) or v.get('en') or next((x for x in v.values() if x), [])
    return v if isinstance(v, list) else ([v] if v else [])


def i18n_get(tree, key, lang):
    node = tree
    for k in key.split('.'):
        if not isinstance(node, dict) or k not in node:
            return key
        node = node[k]
    return tr(node, lang)


def fmt_date(v, lang, style='long'):
    if not v:
        return ''
    d, prec = L.to_date(v), L.date_precision(v)
    if style == 'year' or prec == 'year':
        return str(d.year)
    month_only = style == 'month' or prec == 'month'
    if lang == 'ko':
        return f'{d.year}. {d.month}.' if month_only else f'{d.year}. {d.month}. {d.day}.'
    return f'{MONTHS[d.month - 1]} {d.year}' if month_only else f'{MONTHS[d.month - 1]} {d.day}, {d.year}'


def rich(text):
    """HTML을 이스케이프하되 <sub>, <sup>, <i>만 살린다(논문 제목용)."""
    return Markup(RICH_OK.sub(r'<\1\2>', str(escape(text or ''))))


def strip_tags(text):
    return re.sub(r'<[^>]+>', '', str(text or ''))


HANGUL = re.compile(r'[\uac00-\ud7a3]')


def group_years(items):
    """최신순 목록 → [(연도, [항목])] 연도 내림차순(뉴스·앨범용)."""
    out = []
    for p in items:
        if not out or out[-1][0] != p['year']:
            out.append((p['year'], []))
        out[-1][1].append(p)
    return out


# ---------------------------------------------------------------- 파생 데이터(언어 공통)
def derive(data):
    site, pi, members = data['site'], data['pi'], data['members']
    pubs = data['pubs']
    by_doi = {str(p.get('doi', '')).lower(): p for p in pubs if p.get('doi')}

    vids_cfg = data['videos'] or {}
    hidden = set(vids_cfg.get('hidden') or [])
    featured_ids = list(vids_cfg.get('featured') or [])
    videos = []
    for v in vids_cfg.get('videos') or []:
        if v['id'] in hidden:
            continue
        v = dict(v)
        m = DOI_RE.search(v.get('description') or '')
        if m:
            v['doi'] = m.group(0).rstrip('.').lower()
            v['pub'] = by_doi.get(v['doi'])
        videos.append(v)
    videos.sort(key=lambda v: str(v.get('published', '')), reverse=True)
    videos.sort(key=lambda v: featured_ids.index(v['id']) if v['id'] in featured_ids else len(featured_ids))
    by_vid = {v['id']: v for v in videos}

    news = []
    for p in data['news']:
        p = dict(p)
        p['year'] = L.to_date(p.get('date')).year
        if p.get('doi'):
            p['pub'] = by_doi.get(str(p['doi']).lower())
        if p.get('youtube'):
            p['video'] = by_vid.get(p['youtube'])
        news.append(p)

    research = []
    for t in data['research']:
        t = dict(t)
        t['pubs'] = [by_doi[d.lower()] for d in t.get('dois') or [] if d.lower() in by_doi]
        t['video_items'] = [by_vid[v] for v in t.get('videos') or [] if v in by_vid]
        t['figures'] = [{**f, 'pub': by_doi.get(str(f.get('doi', '')).lower())} for f in t.get('figures') or []]
        research.append(t)

    roles = members.get('roles') or ['postdoc', 'researcher', 'integrated', 'phd', 'ms', 'undergrad', 'staff']
    mlist = members.get('members') or []
    member_groups = [(r, [m for m in mlist if m.get('role') == r]) for r in roles]
    member_groups = [(r, ms) for r, ms in member_groups if ms]
    alumni = sorted(members.get('alumni') or [], key=lambda a: a.get('year') or 0, reverse=True)

    # 구성원 굵게 표시 규칙: pub_name과 저자 표기가 정확히 같을 때만(흔한 성·이니셜의 접두 매칭은 오표시가 많다).
    # 동명이인이 섞이면 members.yaml에 pub_since/pub_until(연도)·pub_exclude[DOI]로 범위를 좁힌다.
    member_rules = [{'key': L.name_key(m['pub_name']), 'since': m.get('pub_since'), 'until': m.get('pub_until'),
                     'exclude': {str(d).lower() for d in m.get('pub_exclude') or []}}
                    for m in mlist + alumni if m.get('pub_name')]

    def rule_ok(r, p):
        y = p.get('year') or 0
        return ((not r['since'] or y >= r['since']) and (not r['until'] or y <= r['until'])
                and str(p.get('doi', '')).lower() not in r['exclude'])

    def own_pubs(m):   # 구성원 상세 페이지용 참여 논문
        if not m.get('pub_name'):
            return []
        r = next(x for x in member_rules if x['key'] == L.name_key(m['pub_name']))
        return [p for p in pubs if rule_ok(r, p) and any(L.name_key(a) == r['key'] for a in p.get('authors') or [])]
    people_pages = [{**m, 'pubs': own_pubs(m), 'alumnus': alum}
                    for alum, group in ((False, mlist), (True, alumni)) for m in group if m.get('id')]
    # 교수 개인 페이지(theme.yaml의 pi_page: true일 때만 만든다). 논문은 대표 논문만 붙인다.
    pi_person = {**pi, 'id': pi.get('id') or 'jong-seong-kug', 'is_pi': True, 'alumnus': False, 'role': 'pi',
                 'position': pi.get('title'),
                 'pubs': [by_doi[d.lower()] for d in pi.get('selected_dois') or [] if d.lower() in by_doi]}
    news_items = [p for p in news if not p.get('album')]
    albums = [p for p in news if p.get('album')]

    hl = {L.name_key(n) for n in site.get('highlight_names') or []}     # 교수: 이니셜 접두 매칭 허용('Kug, J.')

    years = sorted({p['year'] for p in pubs})
    per_year = [(y, sum(1 for p in pubs if p['year'] == y)) for y in years]
    journals = {}
    for p in pubs:
        journals[p.get('journal', '')] = journals.get(p.get('journal', ''), 0) + 1
    top_journals = sorted(journals.items(), key=lambda x: -x[1])[:10]

    pres = data['presentations']
    return {
        'site': site, 'pi': pi, 'i18n': data['i18n'],
        'pubs': pubs, 'pubs_by_year': L.group_by_year(pubs), 'pub_by_doi': by_doi,
        'featured_pubs': [p for p in pubs if p.get('featured')],
        'selected_pubs': [by_doi[d.lower()] for d in pi.get('selected_dois') or [] if d.lower() in by_doi],
        'presentations': pres, 'pres_by_year': L.group_by_year(pres),
        'news': news, 'news_all': news, 'albums': albums, 'news_items': news_items,
        'news_by_year': group_years(news_items), 'albums_by_year': group_years(albums),
        'news_cats': [(c, sum(1 for p in news_items if p.get('category') == c))
                      for c in ('paper', 'award', 'event', 'media', 'lab') if any(p.get('category') == c for p in news_items)],
        'pi_person': pi_person,
        'videos': videos, 'channel': vids_cfg.get('channel') or {},
        'research': research, 'member_groups': member_groups, 'members_all': mlist, 'alumni': alumni,
        'people_pages': people_pages,
        'highlight_keys': hl, 'member_rules': member_rules, 'rule_ok': rule_ok,
        'stats': {
            'pubs': len(pubs), 'first_year': years[0] if years else None, 'last_year': years[-1] if years else None,
            'per_year': per_year, 'top_journals': top_journals, 'journals': len(journals),
            'per_year_full': [(y, dict(per_year).get(y, 0)) for y in range(years[0], years[-1] + 1)] if years else [],
            'members': len([m for m in mlist if not m.get('placeholder')]),
            'videos': len(videos), 'news': len(news), 'presentations': len(pres),
            'news_items': len(news_items), 'albums': len(albums), 'alumni': len(alumni),
        },
        'has_placeholders': any(x.get('placeholder') for x in mlist + pres + (members.get('alumni') or [])),
        'build_date': dt.date.today().isoformat(),
    }


# ---------------------------------------------------------------- 언어·페이지별 컨텍스트
def make_ctx(D, theme_meta, lang, page, depth, post=None, person=None, topic=None):
    other = 'ko' if lang == 'en' else 'en'
    root = '../' * depth
    site = D['site']
    tpl = theme_meta.get('_tpl', set())       # 이 테마에 있는 템플릿 파일 이름(선택 페이지 판단용)
    # Gallery 페이지가 있는 테마는 앨범 글(album: true)을 뉴스 목록·최신 소식에서 빼고 Gallery에만 보인다
    news_list = [p for p in D['news'] if not p.get('album')] if 'gallery.html' in tpl else D['news']

    def lang_prefix(lg):
        return 'ko/' if lg == 'ko' else ''

    def page_url(key, lg=None):
        return f'{root}{lang_prefix(lg or lang)}{key}.html'

    def news_url(p, lg=None):
        return f"{root}{lang_prefix(lg or lang)}news/{p['slug']}.html"

    def member_url(m, lg=None):
        """구성원 상세 페이지(테마에 member.html이 있고 id가 있을 때). 없으면 ''."""
        if m.get('is_pi') or m is D['pi']:
            m = D['pi_person'] if theme_meta.get('pi_page') else {}
        if 'member.html' in tpl and m.get('id'):
            return f"{root}{lang_prefix(lg or lang)}people/{m['id']}.html"
        return ''

    def topic_url(r, lg=None):
        """연구 주제 상세 페이지(테마에 research_topic.html이 있을 때), 없으면 research.html#key."""
        if 'research_topic.html' in tpl:
            return f"{root}{lang_prefix(lg or lang)}research/{r['key']}.html"
        return page_url('research', lg) + f"#{r['key']}"

    def asset(path):
        return f'{root}assets/{path}'

    def static(path):
        if not path:
            return ''
        if re.match(r'^(https?:)?//', str(path)):
            return path
        path = str(path)[2:] if str(path).startswith('./') else str(path)
        return f'{root}static/{quote(path, safe="/")}'   # 파일명의 #, 공백, 한글 등을 URL 인코딩

    def t(key):
        return i18n_get(D['i18n'], key, lang)

    def _tr(v):
        return tr(v, lang)

    def _fmt_date(v, style='long'):
        return fmt_date(v, lang, style)

    def video_thumb(v):
        vid = v if isinstance(v, str) else v.get('id')
        if (L.STATIC / 'videos' / f'{vid}.jpg').exists():
            return static(f'videos/{vid}.jpg')
        return f'https://i.ytimg.com/vi/{vid}/hqdefault.jpg'

    def youtube_url(vid):
        return f'https://www.youtube.com/watch?v={vid}'

    def yt_html(vid, title=''):
        if not YT_ID.match(str(vid or '')):          # 영상 ID 형식이 아니면 그리지 않는다(속성 주입 방지)
            return ''
        return (f'<div class="yt-facade" data-yt="{vid}"><button type="button" class="yt-play" '
                f'aria-label="{escape(t("videos.play"))}: {escape(title)}"><img src="{escape(video_thumb(vid))}" alt="" '
                f'loading="lazy"><span class="yt-icon" aria-hidden="true"></span></button></div>')

    def md(text, p=None):
        text = YT_SHORT.sub(lambda m: '\n\n' + yt_html(m.group(1)) + '\n\n', text or '')
        html = markdown.markdown(text, extensions=['extra', 'sane_lists'])
        if p is not None:                       # 뉴스 본문의 첨부 파일 경로를 static/news/<slug>/로 바꾼다
            files = set(p.get('files', []))

            def fix(m):                         # './fig.png', 'sub/fig.png', 'a.pdf#page=2' 모두 처리
                url = m.group(2)
                cut = min([i for i in (url.find('?'), url.find('#')) if i >= 0], default=len(url))
                path, suffix = url[:cut], url[cut:]
                path = path[2:] if path.startswith('./') else path
                if path in files:
                    return f'{m.group(1)}="{static("news/" + p["slug"] + "/" + path)}{suffix}"'
                return m.group(0)
            html = re.sub(r'\b(src|href)="(?!https?:|mailto:|tel:|#|/|data:)([^"]+)"', fix, html)
        return Markup(html)

    def cover_url(p):
        c = p.get('cover')
        if c:
            return c if re.match(r'^(https?:)?//', c) else static(f"news/{p['slug']}/{c}")
        if p.get('youtube'):
            return video_thumb(p['youtube'])
        return ''

    def is_me(name, p=None):
        """교수(접두 매칭) 또는 구성원(정확히 일치 + 논문 p가 주어지면 기간·제외 규칙)이면 True."""
        key = L.name_key(name)
        if L.same_person(key, D['highlight_keys']):
            return True
        return any(r['key'] == key and (p is None or D['rule_ok'](r, p)) for r in D['member_rules'])

    def authors(p, limit=12):
        """저자 목록. 연구실 구성원은 <strong class="au-me">, 교신저자는 *, 너무 길면 앞부분 + … + 구성원 이름."""
        names = list(p.get('authors') or [])
        corr = set(p.get('corr_authors') or [])

        def one(n):   # 이름 중간(하이픈)에서 줄바꿈되지 않도록 이름마다 감싼다
            star = '<span class="au-corr" title="Corresponding author">*</span>' if n in corr else ''
            return (f'<strong class="au au-me">{escape(n)}{star}</strong>' if is_me(n, p)
                    else f'<span class="au">{escape(n)}{star}</span>')
        if len(names) <= limit:
            return Markup(', '.join(one(n) for n in names))
        s = ', '.join(one(n) for n in names[:limit - 2]) + ', …'
        rest_me = [n for n in names[limit - 2:] if is_me(n, p)]
        if rest_me:
            s += ' ' + ', '.join(one(n) for n in rest_me)
        return Markup(s)

    def cite(p):
        s = f"<i>{escape(p.get('journal', ''))}</i>"
        if p.get('volume'):
            s += f" <b>{escape(p['volume'])}</b>"
            if p.get('issue'):
                s += f"({escape(p['issue'])})"
        if p.get('pages'):
            s += f", {escape(p['pages'])}"
        return Markup(s)

    def doi_url(p):
        d = p.get('doi') if isinstance(p, dict) else p
        return f'https://doi.org/{d}' if d else (p.get('url') if isinstance(p, dict) else '')

    def pub_url(p):
        return page_url('publications') + f"#pub-{p['num']}"

    def search_text(p):
        return ' '.join([strip_tags(p.get('title', '')), ' '.join(p.get('authors') or []),
                         p.get('journal', ''), str(p.get('year', '')), p.get('doi', '')]).lower()

    def latest(n=None):
        items = []
        for p in news_list:
            items.append({'kind': 'news', 'date': p.get('date'), 'title': _tr(p.get('title')),
                          'url': news_url(p), 'meta': t('news.category.' + str(p.get('category', 'lab'))),
                          'image': cover_url(p), 'obj': p})
        for p in D['pubs'][:40]:
            items.append({'kind': 'publication', 'date': p.get('date') or p.get('year'), 'title': p.get('title'),
                          'url': pub_url(p), 'meta': p.get('journal', ''), 'image': static(p['image']) if p.get('image') else '', 'obj': p})
        for p in D['presentations']:
            items.append({'kind': 'presentation', 'date': p.get('date'), 'title': p.get('title'),
                          'url': page_url('presentations'), 'meta': p.get('event', ''), 'image': '', 'obj': p})
        items.sort(key=lambda x: L.to_date(x['date']), reverse=True)
        return items[:n or site.get('home', {}).get('latest', 8)]

    hide = {'presentations'} if site.get('nav_hide_empty', True) and not D['presentations'] else set()
    nav = [{'key': k, 'label': t('nav.' + k), 'url': page_url(k), 'active': k == page}
           for k in site.get('nav') or L.PAGES if k not in hide]
    lab_name = _tr(site['lab']['name'])
    if post is not None:
        page_title = f"{_tr(post.get('title'))} | {lab_name}"
        alt_url = news_url(post, other)
    elif person is not None:
        page_title = f"{_tr(person.get('name'))} | {lab_name}"
        alt_url = member_url(person, other)
    elif topic is not None:
        page_title = f"{_tr(topic.get('title'))} | {lab_name}"
        alt_url = topic_url(topic, other)
    else:
        page_title = lab_name if page == 'index' else f"{t('nav.' + page)} | {lab_name}"
        alt_url = page_url(page, other)

    ctx = dict(D)
    ctx['news'] = news_list
    ctx.update({
        'lang': lang, 'other_lang': other, 'root': root, 'page': page, 'nav': nav, 'alt_url': alt_url,
        'page_title': page_title, 'lab_name': lab_name, 'theme': theme_meta, 'post': post,
        'person': person, 'topic': topic, 'tr_list': lambda v: tr_list(v, lang),
        'member_url': member_url, 'topic_url': topic_url,
        't': t, 'tr': _tr, 'fmt_date': _fmt_date, 'md': md, 'rich': rich, 'strip_tags': strip_tags,
        'page_url': page_url, 'news_url': news_url, 'asset': asset, 'static': static,
        'video_thumb': video_thumb, 'youtube_url': youtube_url, 'yt_html': lambda v, ti='': Markup(yt_html(v, ti)),
        'cover_url': cover_url, 'authors': authors, 'cite': cite, 'doi_url': doi_url, 'pub_url': pub_url,
        'search_text': search_text, 'latest': latest, 'is_me': is_me,
        'text_lang': lambda s: 'ko' if HANGUL.search(str(s or '')) else 'en',
    })
    if post is not None:
        body = post['body'].get(lang) or post['body'].get('en') or ''
        ctx['body_html'] = md(body, post)
        ctx['body_fallback'] = lang == 'ko' and not post['body'].get('ko')
    return ctx


# ---------------------------------------------------------------- 빌드
def render(env, template, dest, ctx):
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(env.get_template(template).render(**ctx), encoding='utf-8')


def safe_clear(out):
    """출력 폴더를 비운다. 원본 폴더(프로젝트·data·content 등)나 build.py가 만들지 않은 폴더는 거부한다."""
    out = out.resolve()
    protected = [L.ROOT, L.DATA, L.CONTENT, L.THEMES, L.STATIC, L.ROOT / 'scripts', L.ROOT / 'reports', L.SITE]
    if any(out == d or out in d.parents for d in protected) or out == Path(out.anchor) or out == Path.home():
        raise SystemExit(f'[build] 출력 폴더로 쓸 수 없는 경로: {out}')
    if out.exists():
        if out.parent != L.SITE.resolve() and any(out.iterdir()) and not (out / BUILD_MARK).exists():
            raise SystemExit(f'[build] {out} 는 build.py가 만든 폴더가 아니어서 지우지 않습니다(비어 있는 폴더를 지정하세요).')
        shutil.rmtree(out)


def build_theme(theme, D, out):
    tdir = L.THEMES / theme
    meta = L.load_yaml(tdir / 'theme.yaml') or {'name': theme}
    meta.setdefault('name', theme)
    safe_clear(out)
    out.mkdir(parents=True)
    (out / BUILD_MARK).write_text(f'{theme} {D["build_date"]}\n', encoding='utf-8')
    if (tdir / 'assets').exists():
        shutil.copytree(tdir / 'assets', out / 'assets')
    shutil.copytree(L.THEMES / '_shared' / 'assets', out / 'assets' / 'shared', dirs_exist_ok=True)
    if L.STATIC.exists():
        shutil.copytree(L.STATIC, out / 'static')
    for p in D['news']:
        if p['files']:
            dst = out / 'static' / 'news' / p['slug']
            dst.mkdir(parents=True, exist_ok=True)
            for f in p['files']:
                (dst / f).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(p['dir'] / f, dst / f)

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader([str(tdir / 'templates'), str(L.THEMES / '_shared')]),
        autoescape=jinja2.select_autoescape(['html']), trim_blocks=True, lstrip_blocks=True,
        undefined=jinja2.ChainableUndefined)
    # 선택 페이지: theme.yaml의 extra_pages(예: gallery, about)와 상세 템플릿(member.html, research_topic.html)
    meta['_tpl'] = {f.name for f in (tdir / 'templates').glob('*.html')}
    extra = [pg for pg in meta.get('extra_pages') or [] if f'{pg}.html' in meta['_tpl']]
    n = 0
    for lang in L.LANGS:
        base, depth = (out, 0) if lang == 'en' else (out / 'ko', 1)
        for page in list(L.PAGES) + extra:
            render(env, f'{page}.html', base / f'{page}.html', make_ctx(D, meta, lang, page, depth))
            n += 1
        for p in D['news']:
            render(env, 'news_post.html', base / 'news' / f"{p['slug']}.html",
                   make_ctx(D, meta, lang, 'gallery' if p.get('album') and 'gallery' in extra else 'news',
                            depth + 1, post=p))
            n += 1
        if 'member.html' in meta['_tpl']:
            for m in D['people_pages'] + ([D['pi_person']] if meta.get('pi_page') else []):
                render(env, 'member.html', base / 'people' / f"{m['id']}.html",
                       make_ctx(D, meta, lang, 'people', depth + 1, person=m))
                n += 1
        if 'research_topic.html' in meta['_tpl']:
            for r in D['research']:
                render(env, 'research_topic.html', base / 'research' / f"{r['key']}.html",
                       make_ctx(D, meta, lang, 'research', depth + 1, topic=r))
                n += 1
    return n


def build_gallery(themes, D):
    metas = []
    for th in themes:
        m = L.load_yaml(L.THEMES / th / 'theme.yaml') or {}
        m['name'] = th
        m['shot'] = f'_shots/{th}.png' if (L.SITE / '_shots' / f'{th}.png').exists() else ''
        m['shot_m'] = f'_shots/{th}_mobile.png' if (L.SITE / '_shots' / f'{th}_mobile.png').exists() else ''
        m['family'] = th.split('.')[0].split('_')[0]      # 't8_globe', 't8.v01', 't8.v02' → 't8'
        m['version'] = th.split('.', 1)[1] if '.' in th else ''
        metas.append(m)
    families = {}
    for m in metas:                                       # 원본 시안 먼저, 그다음 v01, v02 …
        families.setdefault(m['family'], []).append(m)
    groups = [sorted(ms, key=lambda m: (m['version'] != '', m['version'])) for ms in families.values()]
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(str(Path(__file__).parent / 'templates')),
                             autoescape=True, trim_blocks=True, lstrip_blocks=True)
    html = env.get_template('gallery.html').render(themes=metas, groups=groups, D=D, tr=tr, build_date=D['build_date'])
    (L.SITE / 'index.html').write_text(html, encoding='utf-8')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--theme', default='all')
    ap.add_argument('--out', default=None, help='출력 폴더(한 테마일 때만). 기본: site/<theme>')
    args = ap.parse_args()

    D = derive(L.load_all())
    themes = L.list_themes() if args.theme == 'all' else [args.theme]
    for th in themes:
        if not (L.THEMES / th / 'templates').is_dir():
            raise SystemExit(f'테마 없음: {th}')
        out = Path(args.out).resolve() if (args.out and len(themes) == 1) else L.SITE / th
        n = build_theme(th, D, out)
        print(f'[build] {th}: {n} pages → {out}')
    if args.theme == 'all':
        build_gallery(themes, D)
        print(f'[build] gallery → {L.SITE / "index.html"}')


if __name__ == '__main__':
    main()
