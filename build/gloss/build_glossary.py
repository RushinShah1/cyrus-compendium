"""Build an offline rules glossary from every Archives of Nethys link in the compendium, plus everything those entries link to.

Outputs /home/claude/site/assets/glossary.json and rewrites links in pages/*.html to carry data-g keys.
"""
import re, glob, html as H, json, sys, ast
from urllib.parse import unquote_plus
sys.path.insert(0, '/home/claude/build/gen')
import aon_index, entries

AON = 'https://2e.aonprd.com'
bu, bn, bid = aon_index.load()
SITE = '/home/claude/site'

TYPE = {'trait': 'Trait', 'condition': 'Condition', 'rules': 'Rules', 'action': 'Action', 'spell': 'Spell', 'equipment': 'Item',
        'feat': 'Feat', 'skill': 'Skill', 'weapon': 'Weapon', 'class': 'Class', 'relic': 'Relic', 'hybrid-study': 'Hybrid study',
        'background': 'Background', 'heritage': 'Heritage', 'mythic-spell': 'Spell', 'armor': 'Armour', 'shield': 'Shield'}
LINK = re.compile(r'\]\((/[A-Za-z]+\.aspx\?ID=\d+)[^)]*\)|url="(/[A-Za-z]+\.aspx\?ID=\d+)"', re.I)
SKIP = {'sources'}
CAT_PREF = ['condition', 'trait', 'action', 'spell', 'equipment', 'feat', 'skill', 'weapon', 'rules', 'relic', 'class', 'background', 'heritage']


def ids(v):
    if isinstance(v, list):
        return v
    try:
        return ast.literal_eval(v) if v else []
    except Exception:
        return []


def links_in(doc):
    out = set()
    for a, b in LINK.findall(doc.get('markdown') or ''):
        k = aon_index.norm(a or b)
        if k.split('-')[0] not in SKIP and k in bu:
            out.add(k)
    for rid in ids(doc.get('remaster_id')):
        if rid in bid:
            out.add(bid[rid])
    for m in re.finditer(r'<document level="\d+" id="([a-z-]+-\d+)"', doc.get('markdown') or ''):
        if m.group(1) in bid:
            out.add(bid[m.group(1)])
    return out


def resolve_name(q):
    """A Search.aspx?q= link: find the best AoN document by exact name, preferring remastered printings."""
    n = q.lower().strip()
    keys = [k for k in bn.get(n, []) if k in bu]
    if not keys:
        n2 = re.sub(r'\s*\((?:lesser|moderate|greater|major|true|minor|standard)\)$', '', n)
        keys = [k for k in bn.get(n2, []) if k in bu]
    if not keys:
        return None

    def rank(k):
        d = bu[k]
        cat = d.get('category') or ''
        return (1 if d.get('remaster_id') and d['remaster_id'] != '[]' else 0,
                CAT_PREF.index(cat) if cat in CAT_PREF else 99,
                0 if entries._norm(d.get('primary_source')) in entries.REMASTER_BOOKS else 1)
    return sorted(keys, key=rank)[0]


def seeds():
    s, q = set(), set()
    for f in glob.glob(SITE + '/pages/*.html'):
        h = open(f).read()
        for u in re.findall(r'href="https://2e\.aonprd\.com(/[^"]+)"', h):
            u = H.unescape(u)
            if 'Search.aspx' in u:
                m = re.search(r'q=([^&]+)', u)
                if m:
                    q.add(unquote_plus(m.group(1)))
            else:
                k = aon_index.norm(u)
                if k in bu:
                    s.add(k)
    return s, q


# ───────── rendering ─────────
def pre(md):
    t = md.replace('\r', '')
    t = re.sub(r'<image[^>]*/?>', '', t)
    t = re.sub(r'</?spoilers[^>]*>', '', t)
    t = re.sub(r'\[([^\]]+)\]\(/Sources\.aspx[^)]*\)', r'\1', t)
    t = re.sub(r'^(#{1,6})\s+(.+)$', lambda m: f'<h5 class="sub">{m.group(2).strip()}</h5>', t, flags=re.M)
    t = re.sub(r'^\s*-{3,}\s*$', '\n<hr>\n', t, flags=re.M)
    # bullet lists
    out, buf = [], []
    for line in t.split('\n'):
        m = re.match(r'^\s*[-*]\s+(.*)$', line)
        if m:
            buf.append(m.group(1))
            continue
        if buf:
            out.append('<ul>' + ''.join(f'<li>{x}</li>' for x in buf) + '</ul>')
            buf = []
        out.append(line)
    if buf:
        out.append('<ul>' + ''.join(f'<li>{x}</li>' for x in buf) + '</ul>')
    return '\n'.join(out)


def render_md(md, depth=0):
    md = re.sub(r'<title[^>]*>.*?</title>', '', md, count=1, flags=re.S)
    parts = re.split(r'<document level="\d+" id="([a-z-]+-\d+)"\s*/>', md)
    h = entries._md(pre(parts[0]))
    for i in range(1, len(parts), 2):
        ck = bid.get(parts[i])
        if ck and depth < 2:
            child = bu[ck]
            h += f'<h5 class="sub">{H.escape(child["name"])}</h5>' + render_md(child.get('markdown') or '', depth + 1)
        h += entries._md(pre(parts[i + 1]))
    h = re.sub(r'<p>\s*</p>', '', h)
    return h


KIND = {'spell': 'spell', 'feat': 'feat', 'action': 'action', 'equipment': 'item'}
SWAPPED = []


def foundry_html(e):
    tr = ''.join(f'<a class="trait" href="{H.escape(u)}">{H.escape(l)}</a>' for l, u in e.get('traits', []))
    fields = ''.join(f'<p><strong>{H.escape(l)}</strong> {v}</p>' for l, v in e.get('fields', []))
    body = e.get('body', '') + (f'<div class="hr">{e["heightened"]}</div>' if e.get('heightened') else '')
    src = f'<p><strong>Source</strong> {H.escape(e.get("book") or "")}</p>' if e.get('book') else ''
    note = ('<p class="gnote">This printing is newer than the offline Archives of Nethys archive, so its text comes from the '
            'Foundry PF2e system\'s transcription of the same book.</p>')
    return (f'<div class="traits">{tr}</div>' if tr else '') + src + fields + body + note


def bookkey(b):
    b = (b or '').lower()
    b = re.sub(r'pathfinder|lost omens|adventure path:|adventures?:|\(hardcover\)|hardcover compilation|#\d+:?|[^a-z0-9 ]', ' ', b)
    b = b.replace('archives', 'archive')
    return ' '.join(b.split())


LEGACY = {bookkey(x) for x in ['Core Rulebook', "Advanced Player's Guide", 'Gamemastery Guide', 'Secrets of Magic', 'Dark Archive',
                                 'Gods & Magic', 'Book of the Dead', 'Guns & Gears', 'Kingmaker Adventure Path', 'Kingmaker Companion Guide']}


def same_book(a, b):
    return bookkey(a) == bookkey(b)


CORE_BOOKS = ('Player Core', 'GM Core')
NAV = {}


def render_core_rule(d, depth=0):
    """A Player Core or GM Core rules section: its own text, with embedded rules sub-sections left to the section list
    and embedded actions, traits and similar short entries shown inline."""
    md = re.sub(r'<title[^>]*>.*?</title>', '', d.get('markdown') or '', count=1, flags=re.S)
    parts = re.split(r'<document level="\d+" id="([a-z-]+-\d+)"\s*/>', md)
    h = entries._md(pre(parts[0]))
    for i in range(1, len(parts), 2):
        ck = bid.get(parts[i])
        if ck and not ck.startswith('rules-') and depth < 1:
            child = bu[ck]
            h += f'<div class="gembed"><h5 class="sub">{H.escape(child["name"])}</h5>' + render_md(child.get('markdown') or '', 1) + '</div>'
        h += entries._md(pre(parts[i + 1]))
    return re.sub(r'<p>\s*</p>', '', h)


def build_nav():
    """Book structure for Player Core and GM Core: parent, children, reading order."""
    url2k = {}
    for k, d in bu.items():
        if k.startswith('rules-') and d.get('primary_source') in CORE_BOOKS:
            url2k[d['url']] = k
    raw = {x['id']: x for x in json.load(open('/home/claude/ext/aon/2e/data/rules.json')) if x.get('primary_source') in CORE_BOOKS}
    for i, x in raw.items():
        k = bid.get(i)
        if not k:
            continue
        kids = [bid[c] for c in re.findall(r'<document level="\d+" id="(rules-\d+)"', x['markdown']) if c in raw and c in bid]
        nx = url2k.get((x.get('next_link') or {}).get('url'))
        pv = url2k.get((x.get('previous_link') or {}).get('url'))
        NAV.setdefault(k, {}).update(b=x['primary_source'], c=kids, nx=nx, pv=pv)
        for c in kids:
            NAV.setdefault(c, {}).setdefault('p', k)


def basename(n):
    return re.sub(r'[^a-z0-9]', '', re.sub(r'\s*\([^)]*\)\s*$', '', (n or '').lower()))


def render_aon(k):
    d = bu[k]
    if k in NAV:
        return [d['name'], 'Rules', render_core_rule(d), '', NAV[k]]
    for rid in ids(d.get('remaster_id')):          # legacy printing with a remastered replacement
        if rid in bid:
            r = bu[bid[rid]]
            if basename(r.get('name')) == basename(d.get('name')):
                d = r                               # same name: the remaster supersedes it, so show the remaster
                break
            # renamed in the remaster: the legacy entry is still available, so show its own text with a pointer
            note = (f'<p class="gnote">Legacy printing. The remaster renamed and revised this as '
                    f'<a href="https://2e.aonprd.com{r["url"]}">{H.escape(r["name"])}</a>; this version remains available.</p>')
            return [d['name'], TYPE.get(d.get('category'), (d.get('type') or '').title()), note + render_md(d.get('markdown') or ''), 'legacy']
    cat = d.get('category')
    if cat in KIND:
        try:
            e = entries.entry(d['name'], KIND[cat])
        except KeyError:
            e = None
        if e is not None:
            if e.get('source') != 'aon' and (same_book(d.get('primary_source'), e.get('book'))
                                              or bookkey(d.get('primary_source')) not in LEGACY or not e.get('remaster')):
                e = None
        if e is not None and e.get('source') != 'aon':
            alt = [x for x in bn.get(d['name'].lower(), []) if x in bu and same_book(bu[x].get('primary_source'), e.get('book'))]
            if alt:
                d = bu[alt[0]]
                e = None
        if e is not None:
            if e.get('source') != 'aon':
                SWAPPED.append((d['name'], d.get('primary_source'), e.get('book')))
                return [e['name'], TYPE[cat], foundry_html(e), '']
            rk = aon_index.norm(e['url'])
            if rk != k and rk in bu:
                d = bu[rk]
    return [d['name'], TYPE.get(d.get('category'), (d.get('type') or '').title()), render_md(d.get('markdown') or ''),
            ('legacy' if ids(d.get('remaster_id')) else '')]


def render_foundry(name):
    for kind in ('item', 'spell', 'feat', 'action'):
        try:
            e = entries.entry(name, kind, foundry_kind='any')
        except KeyError:
            continue
        tr = ''.join(f'<a class="trait" href="{H.escape(u)}">{H.escape(l)}</a>' for l, u in e.get('traits', []))
        fields = ''.join(f'<p><strong>{H.escape(l)}</strong> {v}</p>' for l, v in e.get('fields', []))
        body = e.get('body', '') + (f'<div class="hr">{e["heightened"]}</div>' if e.get('heightened') else '')
        src = f'<p class="muted small">Source {H.escape(e.get("book") or "")}</p>' if e.get('book') else ''
        return [e['name'], {'item': 'Item', 'spell': 'Spell', 'feat': 'Feat', 'action': 'Action'}[kind],
                (f'<div class="traits">{tr}</div>' if tr else '') + src + fields + body, '']
    return None


def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


SKIP_CATS = {'source'}
TYPE_NAME = {'equipment': 'Item', 'item-bonus': 'Item', 'weapon': 'Weapon', 'armor': 'Armour', 'shield': 'Shield', 'rules': 'Rules',
             'mythic-spell': 'Spell', 'hybrid-study': 'Hybrid study', 'relic': 'Relic'}


def type_name(d):
    c = d.get('category') or ''
    if c in TYPE_NAME:
        return TYPE_NAME[c]
    t = d.get('type') or c.replace('-', ' ').title()
    words = t.split()
    return ' '.join([words[0]] + [w if w[:1].isupper() and w.lower() in PROPER else w.lower() for w in words[1:]]) if words else t


PROPER = {'magus', 'wizard', 'witch', 'bard', 'cleric', 'champion', 'druid', 'oracle', 'psychic', 'ranger', 'rogue', 'sorcerer', 'summoner',
          'swashbuckler', 'thaumaturge', 'inventor', 'investigator', 'gunslinger', 'kineticist', 'alchemist', 'barbarian', 'animist',
          'exemplar', 'commander', 'guardian', "hunter's", 'hellknight'}
OUT = SITE + '/assets/g'
SHARD_BYTES = 600_000


def main():
    import os, hashlib, shutil
    build_nav()
    s, q = seeds()
    qmap, fallback = {}, {}
    for name in q:
        k = resolve_name(name)
        if k:
            qmap[name.lower()] = k
        else:
            fallback[name.lower()] = name
    ALL = {}
    for k, d in bu.items():
        if d.get('category') in SKIP_CATS:
            continue
        r = render_aon(k)
        if not r[0] or not (r[2] or '').strip() or r[0][:1] in '(<' or '<%' in r[0]:
            continue
        if k not in NAV:
            r[1] = type_name(d)
        ALL[k] = r
    for low, name in fallback.items():
        r = render_foundry(name)
        if r:
            key = 'f-' + slug(name)
            ALL[key] = r
            qmap[low] = key
    extra = '/home/claude/build/sheet/extra_gloss.json'
    if os.path.exists(extra):
        for k, v in json.load(open(extra)).items():
            ALL.setdefault(k, v)
    frg = '/home/claude/build/fr/fr_gloss.json'
    if os.path.exists(frg):
        ALL.update(json.load(open(frg)))
    print('swapped to newer printing', len(SWAPPED), 'entries', len(ALL), 'unresolved', [n for n in fallback if n not in qmap][:20])
    for v in ALL.values():
        v[2] = rewrite(v[2], ALL, qmap)
    rules_page(ALL)
    # write: one index of names and types, and text shards loaded on demand; identical texts are stored once
    shutil.rmtree(OUT, ignore_errors=True)
    os.makedirs(OUT)
    types, tix = [], {}
    index, first, shards, cur, size = {}, {}, [], {}, 0
    for k in sorted(ALL, key=lambda k: (ALL[k][1], ALL[k][0].lower(), k)):
        name, typ, html, leg = ALL[k][:4]
        nav = ALL[k][4] if len(ALL[k]) > 4 else None
        if typ not in tix:
            tix[typ] = len(types); types.append(typ)
        h = hashlib.md5((html + json.dumps(nav)).encode()).hexdigest()
        tail = []
        if k in bu and leg:
            for rid in ids(bu[k].get('remaster_id')):
                if rid in bid and basename(bu[bid[rid]].get('name')) != basename(name):
                    tail = [bu[bid[rid]]['name']]
                break
        if h in first:
            index[k] = [name, tix[typ], first[h], 1 if leg else 0] + tail
            continue
        first[h] = k
        if size > SHARD_BYTES:
            shards.append(cur); cur, size = {}, 0
        cur[k] = [html, nav] if nav else [html]
        size += len(html) + 60
        index[k] = [name, tix[typ], len(shards), 1 if leg else 0] + tail
    shards.append(cur)
    for i, sh in enumerate(shards):
        json.dump(sh, open(f'{OUT}/s{i}.json', 'w'), separators=(',', ':'), ensure_ascii=False)
    json.dump({'v': 2, 't': types, 'n': len(shards), 'e': index}, open(f'{OUT}/index.json', 'w'), separators=(',', ':'), ensure_ascii=False)
    json.dump(qmap, open('/home/claude/build/gloss/qmap.json', 'w'))
    conds = condition_keys(ALL)
    for f in glob.glob(SITE + '/pages/*.html'):
        h = open(f).read()
        h2 = link_terms(rewrite(h, ALL, qmap), conds)
        if h2 != h:
            open(f, 'w').write(h2)
    for old in ('glossary.json', 'core.json'):
        if os.path.exists(SITE + '/assets/' + old):
            os.remove(SITE + '/assets/' + old)
    tot = sum(os.path.getsize(f) for f in glob.glob(OUT + '/*.json'))
    print('shards', len(shards), 'index MB', round(os.path.getsize(OUT + '/index.json') / 1e6, 2), 'total MB', round(tot / 1e6, 1),
          'distinct texts', len(first), 'types', len(types))


SKIP_COND = {'hidden', 'observed', 'broken', 'controlled', 'encumbered', 'unnoticed', 'friendly', 'helpful', 'hostile', 'indifferent', 'unfriendly'}


def condition_keys(G):
    out = {}
    for k, v in G.items():
        if k.startswith('conditions-') and v[0].lower() not in SKIP_COND:
            d = bu.get(k)
            rem = d and not ids(d.get('remaster_id'))
            if rem or v[0].lower() not in out:
                out[v[0].lower()] = k
    return out


SEG_RE = re.compile(r'(<section class="ev">.*?</section>|<td[^>]*>.*?</td>|<dd>.*?</dd>|<p class="prose">.*?</p>)', re.S)


def link_terms(h, conds):
    """Link the first mention of each condition in evaluations, table cells and prose, where it isn't already a link."""
    pat = re.compile(r'\b(' + '|'.join(sorted((re.escape(c) for c in conds), key=len, reverse=True)) + r')\b', re.I)

    def seg(m):
        block = m.group(0)
        if 'data-cond-linked' in block:
            return block
        done = set()
        parts = re.split(r'(<a\b.*?</a>|<[^>]+>)', block, flags=re.S)
        for i, part in enumerate(parts):
            if not part or part.startswith('<'):
                continue
            def rep(mm):
                w = mm.group(1).lower()
                if w in done:
                    return mm.group(0)
                done.add(w)
                return f'<a href="#" data-g="{conds[w]}">{mm.group(0)}</a>'
            parts[i] = pat.sub(rep, part)
        return ''.join(parts)
    return SEG_RE.sub(seg, h)


A_RE = re.compile(r'<a ([^>]*?)href="https://2e\.aonprd\.com(/[^"]+)"([^>]*)>')


def gkey(u, G, qmap):
    u = H.unescape(u)
    if 'Search.aspx' in u:
        m = re.search(r'q=([^&]+)', u)
        return qmap.get(unquote_plus(m.group(1)).lower()) if m else None
    k = aon_index.norm(u)
    return k if k in G else None


def rewrite(h, G, qmap):
    def sub(m):
        pre_, u, post = m.group(1), m.group(2), m.group(3)
        if 'data-g=' in pre_ + post:
            return m.group(0)
        k = gkey(u, G, qmap)
        if not k:
            return m.group(0)
        return f'<a {pre_}href="https://2e.aonprd.com{u}" data-g="{k}"{post}>'
    return A_RE.sub(sub, h)


START = {'Player Core': ['What is a Roleplaying Game?', 'The Flow of the Game', 'Chapter 8: Playing the Game', 'Checks', 'Turns', 'Actions',
                         'Basic Actions', 'Damage', 'Encounter Mode', 'Exploration Mode', 'Downtime Mode', 'Conditions Appendix',
                         'Leveling Up'],
         'GM Core': ['Chapter 1: Running the Game', 'Difficulty Classes', 'Building Encounters', 'Hazards', 'Treasure for New Characters',
                     'Chapter 4: Subsystems']}


def rules_page(ALL):
    def li(k, depth):
        n = ALL.get(k, [bu[k]['name']])[0] if k in bu or k in ALL else k
        kids = NAV.get(k, {}).get('c', [])
        sub = ('<ul class="toc">' + ''.join(li(c, depth + 1) for c in kids) + '</ul>') if kids and depth < 6 else ''
        return f'<li><a href="#" data-g="{k}">{H.escape(n)}</a>{sub}</li>'

    def count(k):
        return sum(1 + count(c) for c in NAV.get(k, {}).get('c', []))
    books = []
    for b in CORE_BOOKS:
        roots = [k for k, v in NAV.items() if v.get('b') == b and 'p' not in v]
        # reading order: follow next links from the first root
        order = {}
        start = [k for k in roots if not NAV[k].get('pv') or NAV.get(NAV[k]['pv'], {}).get('b') != b]
        seq, k, guard = 0, (start[0] if start else None), 0
        while k and guard < 3000:
            order.setdefault(k, seq); seq += 1; guard += 1
            k = NAV.get(k, {}).get('nx')
        roots.sort(key=lambda r: order.get(r, 9999))
        chapters = ''.join(
            f'<details class="toc-ch"><summary><span>{H.escape(ALL[r][0])}</span><small>{count(r)} sections</small></summary>'
            f'<ul class="toc top">{li(r, 0)}</ul></details>' for r in roots if r in ALL)
        names = {ALL[k][0]: k for k, v in NAV.items() if v.get('b') == b and k in ALL}
        quick = ''.join(f'<a class="chip" href="#" data-g="{names[n]}">{H.escape(n)}</a>' for n in START[b] if n in names)
        books.append(f'<section class="tocbook"><h2>{b}</h2><p class="muted small">Start here</p><div class="quick">{quick}</div>{chapters}</section>')
    page = f'''<div class="page doc" data-page="rules">
<header class="ph"><h1>Core rules</h1>
<p class="lede">The full rules text of Player Core and GM Core from Archives of Nethys, arranged as the books are. Open a chapter, then select any section to read it in a panel; each panel has Previous and Next buttons for reading straight through, and the path back to its chapter.</p></header>
<label class="search tocsearch"><svg class="ic" aria-hidden="true"><use href="#i-search"/></svg><input id="toc-q" type="search" placeholder="Find a section by name" autocomplete="off"></label>
<p class="muted small" id="toc-count"></p>
{''.join(books)}
<p class="muted small">Spells, feats, items, actions, traits and conditions from both books are in the Rules glossary as well, with type filters and full-text search.</p>
</div>'''
    open(SITE + '/pages/rules.html', 'w').write(page)


if __name__ == '__main__':
    main()
