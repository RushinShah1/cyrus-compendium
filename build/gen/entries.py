"""Unified rules entries: AoN archive text (exact) when it covers the printing, Foundry text otherwise."""
import json, re, html as H
from urllib.parse import quote_plus
import rules

AON = 'https://2e.aonprd.com'
_files = {'spell': 'spells', 'feat': 'feats', 'action': 'actions', 'item': 'equipment',
          'feature': 'class-features', 'skillaction': 'skill-general-actions', 'relic': 'relics', 'weapon': 'weapons'}
_cache = {}


def _load(kind):
    if kind not in _cache:
        d = {}
        try:
            for x in json.load(open(f'/home/claude/ext/aon/2e/data/{_files[kind]}.json')):
                d.setdefault(x['name'].lower(), []).append(x)
        except FileNotFoundError:
            pass
        _cache[kind] = d
    return _cache[kind]


TRAITS = {}
for t in sorted(json.load(open('/home/claude/ext/aon/2e/data/traits.json')),
                key=lambda t: 1 if (t.get('remaster_id') or '[]') != '[]' else 0):   # remastered printings first
    TRAITS.setdefault(t['name'].lower(), AON + t['url'])

GLYPH = {'Single Action': 'one', 'One Action': 'one', 'Two Actions': 'two', 'Three Actions': 'three', 'Reaction': 'reaction',
         'Free Action': 'free'}


def glyph_html(kind):
    ch = {'one': '1', 'two': '2', 'three': '3', 'reaction': 'r', 'free': 'f'}.get(kind)
    if not ch:
        return ''
    label = {'one': 'One action', 'two': 'Two actions', 'three': 'Three actions', 'reaction': 'Reaction', 'free': 'Free action'}[kind]
    return f'<span class="pf" title="{label}" aria-label="{label}">{ch}</span>'


def _md(md):
    """AoN markdown -> HTML."""
    t = md.replace('\r', '')
    t = re.sub(r'<actions string="([^"]+)"\s*/>', lambda m: glyph_html(GLYPH.get(m.group(1), '')) or m.group(1), t)
    t = re.sub(r'<title[^>]*>\s*(.*?)\s*</title>', lambda m: f'<h5 class="sub">{m.group(1)}</h5>', t, flags=re.S)
    t = re.sub(r'<traits>(.*?)</traits>', lambda m: '<div class="traits">' + ''.join(
        f'<a class="trait" href="{AON}{u}">{l}</a>' for l, u in re.findall(r'label="([^"]+)" url="([^"]+)"', m.group(1))) + '</div>', t, flags=re.S)
    t = re.sub(r'</?(column|row|aside|summary|additional-info|center|document|sample|nethys-search|spoilers|filter-[a-z-]+|page-[a-z-]+)[^>]*>', '', t)
    t = re.sub(r'\[([^\]]+)\]\((/[^)]+)\)', lambda m: f'<a href="{AON}{m.group(2)}">{m.group(1)}</a>', t)
    t = re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)', r'<a href="\2">\1</a>', t)
    t = re.sub(r'\[([^\]]+)\]\(([A-Za-z][^)]*\.aspx[^)]*)\)', lambda m: f'<a href="{AON}/{m.group(2)}">{m.group(1)}</a>', t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t, flags=re.S)
    t = re.sub(r'(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])', r'<em>\1</em>', t)
    t = re.sub(r'(?<![\w])_(?!\s)([^_\n]+?)(?<!\s)_(?![\w])', r'<em>\1</em>', t)
    blocks = [b.strip() for b in re.split(r'\n\s*\n', t) if b.strip()]
    out = []
    for b in blocks:
        if re.match(r'^<(ul|ol|table|h\d|div|p)\b', b):
            out.append(b)
        elif re.search(r'<(ul|ol|table)\b', b):
            pre, tag, post = re.split(r'(<(?:ul|ol|table)\b.*)', b, maxsplit=1, flags=re.S)[0], None, None
            rest_ = b[len(pre):]
            if pre.strip():
                out.append('<p>' + pre.strip().replace('\n', ' ') + '</p>')
            out.append(rest_)
        else:
            out.append('<p>' + b.replace('\n', ' ') + '</p>')
    return '\n'.join(out)


HEAD_KEEP = ['Prerequisites', 'Frequency', 'Trigger', 'Requirements', 'Cost', 'Range', 'Area', 'Targets', 'Target', 'Defense',
             'Saving Throw', 'Duration', 'Usage', 'Bulk', 'Activate', 'Effect', 'Price', 'Hands', 'Access']


def _acttext(s):
    n = {'Single Action': '1', 'One Action': '1', 'Two Actions': '2', 'Three Actions': '3'}
    if ' to ' in s:
        a, b = s.split(' to ', 1)
        if a in n and b in n:
            return f'{n[a]} to {n[b]}'
        if a in n:
            return f'{n[a]} to {b}'
    return {'Reaction': 'reaction', 'Free Action': 'free'}.get(s, n.get(s, s))


def _aon_entry(doc):
    md = doc['markdown'].replace('\r', '')
    head, _, rest = md.partition('\n---')
    title = re.search(r'<title[^>]*right="([^"]*)"[^>]*>(.*?)</title>', head, re.S)
    act = re.search(r'<actions string="([^"]+)"', title.group(2) if title else '')
    traits = re.findall(r'<trait label="([^"]+)" url="([^"]+)"', head)
    fields = []
    hh = re.sub(r'</?(column|row)[^>]*>', '\n', head)
    hh = re.sub(r'<traits>.*?</traits>', '', hh, flags=re.S)
    hh = re.sub(r'<title.*?</title>', '', hh, flags=re.S)
    parts = re.split(r'\*\*([A-Z][A-Za-z ]+?)\*\*', hh)
    for i in range(1, len(parts) - 1, 2):
        lab, val = parts[i].strip(), re.sub(r'\s+', ' ', parts[i + 1]).strip().rstrip(';')
        if lab in HEAD_KEEP and val:
            lab = {'Saving Throw': 'Defense', 'Target': 'Targets'}.get(lab, lab)
            fields.append((lab, _md(val).removeprefix('<p>').removesuffix('</p>')))
    trad = re.search(r'\*\*Traditions?\*\*\s*(.*?)\n\s*\n', hh, re.S)
    src = re.search(r'\*\*Source\*\*\s*(.*?)\n', hh)
    parts = re.split(r'\n---+\n', rest)
    body, height = [], []
    for p in parts:
        if not p.strip():
            continue
        for chunk in re.split(r'(?=\*\*Heightened)', p):
            (height if chunk.lstrip().startswith('**Heightened') else body).append(chunk)
    return dict(
        name=doc['name'], url=AON + doc['url'], source='aon', level=title.group(1) if title else '',
        action=GLYPH.get(act.group(1)) if act else None, action_text=_acttext(act.group(1)) if act else '',
        traits=[(l, AON + u) for l, u in traits], fields=fields,
        traditions=[x.strip() for x in re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', trad.group(1)).split(',')] if trad else [],
        book=re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', src.group(1)).strip() if src else doc.get('primary_source', ''),
        body=_md('\n\n'.join(body)), heightened=_md('\n\n'.join(height)))


def _foundry_entry(d, kind):
    s = d['system']
    lvl = s.get('level', {}).get('value', 1) or 1
    h = rules.render(s['description']['value'], lvl)
    head, body, height = rules.split_sections(h)
    tr = s.get('traits', {})
    traits = []
    rar = tr.get('rarity', 'common')
    if rar != 'common':
        traits.append((rar.title(), TRAITS.get(rar, AON)))
    for t in tr.get('value', []):
        nm = t.replace('-', ' ').title()
        traits.append((nm, TRAITS.get(t.replace('-', ' '), f'{AON}/Search.aspx?q={quote_plus(nm)}')))
    fields = []
    for k in ['Prerequisites', 'Frequency', 'Trigger', 'Requirements', 'Cost']:
        if k in head:
            fields.append((k, head[k]))
        elif k + 's' in head:
            fields.append((k, head[k + 's']))
    if kind == 'feat':
        pr = [x.get('value') for x in (s.get('prerequisites') or {}).get('value', [])]
        if pr and not any(f[0] == 'Prerequisites' for f in fields):
            fields.insert(0, ('Prerequisites', '; '.join(pr)))
    if kind == 'spell':
        a = s.get('area') or {}
        area = head.get('Area') or (f"{a.get('value')}-foot {a.get('type')}" if a else '')
        df = s.get('defense') or {}
        dtxt = ''
        if df.get('save'):
            dtxt = ('basic ' if df['save'].get('basic') else '') + df['save']['statistic'].title()
        elif df.get('passive'):
            dtxt = df['passive'].get('statistic', '').upper()
        dur = (s.get('duration') or {})
        durtxt = ('sustained' + (' up to ' + dur['value'] if dur.get('value') else '')) if dur.get('sustained') else dur.get('value', '')
        for lab, val in [('Range', s.get('range', {}).get('value')), ('Area', area), ('Targets', s.get('target', {}).get('value')),
                         ('Defense', dtxt), ('Duration', durtxt)]:
            if val:
                fields.append((lab, val))
    if kind == 'item':
        pr = (s.get('price') or {}).get('value') or {}
        ptxt = ', '.join(f'{v:,} {k}' for k, v in pr.items() if v)
        use = (s.get('usage') or {}).get('value', '')
        blk = (s.get('bulk') or {}).get('value')
        for lab, val in [('Price', ptxt), ('Usage', use.replace('-', ' ') if use else ''), ('Bulk', ('L' if blk == 0.1 else str(blk)) if blk not in (None, 0) else '')]:
            if val:
                fields.append((lab, val))
        # higher-level variants as separate Foundry items
        base = d['name']
        vs = []
        for nm, hits in rules.IDX.items():
            if nm.startswith(base.lower() + ' (') and any(p == 'equipment' for p, _ in hits):
                vd = json.load(open([f for p, f in hits if p == 'equipment'][0]))
                vs.append(vd)
        vs.sort(key=lambda x: x['system'].get('level', {}).get('value', 0))
        if vs:
            extra = []
            for vd in vs:
                vsys = vd['system']
                vpr = ', '.join(f'{v:,} {k}' for k, v in ((vsys.get('price') or {}).get('value') or {}).items() if v)
                vh = rules.render(vsys['description']['value'], vsys.get('level', {}).get('value', 1))
                extra.append(f'<h5 class="sub">{H.escape(vd["name"])} <span class="muted">Item {vsys.get("level", {}).get("value")}, {vpr}</span></h5>{vh}')
            body = body + '<details class="vars"><summary>Higher-level versions</summary>' + ''.join(extra) + '</details>'
    t = (s.get('time') or {}).get('value') if kind == 'spell' else None
    act = None
    if kind == 'spell':
        act = {'1': 'one', '2': 'two', '3': 'three', 'reaction': 'reaction', 'free': 'free'}.get(str(t).lower())
    else:
        at = (s.get('actionType') or {}).get('value')
        n = (s.get('actions') or {}).get('value')
        act = {'action': {1: 'one', 2: 'two', 3: 'three'}.get(n), 'reaction': 'reaction', 'free': 'free'}.get(at)
    pub = s.get('publication', {})
    return dict(name=d['name'], url=f'{AON}/Search.aspx?q={quote_plus(d["name"])}', source='foundry', level=str(lvl),
                action=act, action_text=str(t or ''), traits=traits, fields=fields,
                traditions=[x.title() for x in (tr.get('traditions') or [])],
                book=pub.get('title', '').replace('Pathfinder ', ''), body=body, heightened=height)


ACTION_OVERRIDE = {'Sprinting Spellstrike': 'two'}  # Foundry marks it passive; AoN/Impossible Magic print it as a 2-action activity


REMASTER_BOOKS = {'gm core', 'player core', 'player core 2', 'treasure vault (remastered)', 'guns gears (remastered)',
                  'rage of elements', 'battlecry', 'howl of the wild', 'war of immortals', 'impossible magic', 'monster core',
                  'dark archive (remastered)', 'secrets of magic'}


def _norm(b):
    """Book key that matches AoN's and Foundry's differing spellings of the same printing."""
    b = (b or '').lower()
    b = re.sub(r'pathfinder|lost omens|adventure path:|adventures?:|\(hardcover\)|hardcover compilation|#\d+:?|[^a-z0-9() ]', ' ', b)
    b = b.replace('archives', 'archive')
    b = ' '.join(b.split())
    b = re.sub(r'^the ', '', b)
    if b.startswith('kingmaker'):
        b = 'kingmaker'
    return b


_SCHOOLS = {'abjuration', 'conjuration', 'divination', 'enchantment', 'evocation', 'illusion', 'necromancy', 'transmutation'}
_RENAMED = {'positive': 'vitality', 'negative': 'void'}
_RARITY = ('uncommon', 'rare', 'unique')


def _spell_traits(shown, d):
    """Trait row for a spell card: the printed traits under current rules.

    Older printings list components and a school in place of concentrate and manipulate, so the row takes the
    traits from the Foundry record as well, drops the school and uses the current names of renamed traits."""
    have = {}
    for label, url in shown:
        k = _RENAMED.get(label.lower(), label.lower())
        if k in _SCHOOLS:
            continue
        have[k] = (k.title(), TRAITS.get(k, url))
    tr = d['system'].get('traits', {})
    rar = tr.get('rarity', 'common')
    if rar != 'common':
        have.setdefault(rar, (rar.title(), TRAITS.get(rar, AON)))
    for t in tr.get('value', []):
        k = t.replace('-', ' ')
        have.setdefault(k, (k.title(), TRAITS.get(k, f'{AON}/Search.aspx?q={quote_plus(k.title())}')))
    return [have[k] for k in sorted(have, key=lambda k: (k not in _RARITY, k))]


def entry(name, kind='spell', foundry_kind=None, prefer_source=None):
    fk = foundry_kind or {'spell': 'spell', 'feat': 'feat', 'action': 'action', 'item': 'item', 'feature': 'feature',
                          'skillaction': 'action'}.get(kind, 'any')
    try:
        d = rules.get(name, fk)
    except KeyError:
        d = None
    book = (d['system'].get('publication', {}).get('title', '').replace('Pathfinder ', '') if d else prefer_source) or ''
    cands = _load(kind).get(name.lower(), [])
    doc = None
    for c in cands:
        ps = c.get('primary_source', '')
        if prefer_source and ps == prefer_source:
            doc = c; break
        if book and _norm(ps) == _norm(book):
            doc = c; break
    if doc is None and d is not None and d['system'].get('publication', {}).get('remaster'):
        rem = [c for c in cands if _norm(c.get('primary_source', '')) in REMASTER_BOOKS - {'secrets of magic'}]
        if rem:
            doc = rem[0]
    if doc is None and d is None and cands:
        rem = [c for c in cands if _norm(c.get('primary_source', '')) in REMASTER_BOOKS]
        doc = (rem or cands)[0] if rem else cands[-1]
    if doc is not None:
        e = _aon_entry(doc)
        if not e['action'] and d is not None:
            e['action'] = _foundry_entry(d, fk if fk != 'any' else kind)['action']
        e['remaster'] = bool(d['system'].get('publication', {}).get('remaster')) if d else True
        e['fdoc'] = d
        e.setdefault('kind', kind)
        if kind == 'spell' and d is not None:
            e['traits'] = _spell_traits(e['traits'], d)
        return e
    if d is None:
        raise KeyError(name)
    e = _foundry_entry(d, fk)
    if name in ACTION_OVERRIDE:
        e['action'] = ACTION_OVERRIDE[name]
    e['remaster'] = bool(d['system'].get('publication', {}).get('remaster'))
    e['fdoc'] = d
    e.setdefault('kind', kind)
    return e


_RULES = None


def rule_html(rid, depth=0):
    """AoN rule page (exact text) with nested <document> children expanded."""
    global _RULES
    if _RULES is None:
        _RULES = {d['id']: d for d in json.load(open('/home/claude/ext/aon/2e/data/rules.json'))}
    d = _RULES.get(f'rules-{rid}')
    if not d:
        return '', ''
    md = d['markdown'].replace('\r', '')
    md = re.sub(r'<title[^>]*>.*?</title>', '', md, count=1, flags=re.S)
    md = re.sub(r'\*\*Source\*\*[^\n]*\n', '', md)
    md = re.sub(r'\[Click here[^\]]*\]\([^)]*\)\.?', '', md)
    parts = re.split(r'<document level="\d+" id="rules-(\d+)"\s*/>', md)
    out = _md(parts[0])
    for i in range(1, len(parts), 2):
        child = _RULES.get(f'rules-{parts[i]}')
        if child and depth < 3:
            body, _ = rule_html(parts[i], depth + 1)
            out += f'<h5 class="sub">{H.escape(child["name"])}</h5>' + body
        out += _md(parts[i + 1])
    out = re.sub(r'<h5 class="sub">\s*</h5>', '', out)
    return out, d['name']
