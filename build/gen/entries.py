"""Rules entries, taken only from the Archives of Nethys data."""
import json, re, html as H
from urllib.parse import quote_plus

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
    head, sep, rest = md.partition('\n---')
    if not sep:      # an entry with no rule line under its header: the header ends with the Source paragraph
        m = re.search(r'\*\*Source\*\*[^\n]*\n', md)
        if m:
            head, rest = md[:m.end()], md[m.end():]
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


ACTION_OVERRIDE = {}
ALIAS = {('Studious Spells', 'feature'): 'Studious Spell'}   # the name the current magus class entry uses

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



_SCHOOLS = {'abjuration', 'conjuration', 'divination', 'enchantment', 'evocation', 'necromancy', 'transmutation'}
_RENAMED = {'positive': 'vitality', 'negative': 'void'}
ATTACK_NOT_ON_CAST = {   # the attack roll belongs to something the spell creates or controls, not to casting it
    'Illusory Creature': 'the illusion makes its own attacks', 'Tangling Creepers': 'the vine attack is a later action',
    'Puppet Strings': 'the controlled creature makes the Strike'}
_COMPONENT_TRAIT = {'verbal': 'Concentrate', 'somatic': 'Manipulate', 'material': 'Manipulate', 'focus': 'Manipulate'}
_FALLBACK_FILES = {'feature': ['hybrid-studies'], 'item': ['weapons', 'armors', 'shields'], 'action': ['skill-general-actions']}


def _key(name):
    return name.lower().replace('’', "'").strip()


def _cands(name, kind):
    """Every Archives of Nethys document of this kind with this name."""
    k = _key(name)
    out = list(_load(kind).get(k, []))
    if not out:
        for f in _FALLBACK_FILES.get(kind, []):
            fk = 'file:' + f
            if fk not in _cache:
                d = {}
                for x in json.load(open(f'/home/claude/ext/aon/2e/data/{f}.json')):
                    d.setdefault(_key(x['name']), []).append(x)
                _cache[fk] = d
            out += _cache[fk].get(k, [])
    return out


def _idnum(c):
    n = re.findall(r'\d+', c.get('id') or '')
    return int(n[0]) if n else 0


def pick(cands, prefer_source=None):
    """The current printing among documents that share a name: one that no later printing has replaced, the page's
    own document ahead of the rows for its versions, a rulebook ahead of other books, then the most recent release."""
    if prefer_source:
        for c in cands:
            if c.get('primary_source') == prefer_source:
                return c
    pool = [c for c in cands if not c.get('remaster_id')] or cands
    pool = [c for c in pool if not c.get('exclude_from_search')] or pool     # an item's activation row is not the action
    pool = [c for c in pool if not c.get('item_parent_id')] or pool
    return max(pool, key=lambda c: (c.get('primary_source_category') == 'Rulebooks', c.get('release_date') or '', _idnum(c)))


def is_legacy(doc):
    """A printing from before the remaster that no later book has replaced."""
    if doc.get('category') == 'spell':
        return bool(set(doc.get('component') or []) & set(_COMPONENT_TRAIT))     # written with spell components
    return (doc.get('release_date') or '9') < '2023-08-02'                       # before Rage of Elements, the first book in the new format


def _spell_traits(shown, doc):
    """Trait row for a spell. A printing that lists spell components gains the traits those components give the spell
    (Core Rulebook pg. 303: verbal gives concentrate; somatic, material and focus give manipulate). Its school trait is
    dropped, and a trait the entry lists under both its old and new name is shown under the new one."""
    listed = [t.lower() for t in (doc.get('trait') or [])]
    out = []
    for l, u in shown:
        new = _RENAMED.get(l.lower())
        if new and new in listed:          # the entry lists both the old trait name and the one that replaced it
            l, u = new.title(), TRAITS.get(new, u)
        if l.lower() not in [x.lower() for x, _ in out]:
            out.append((l, u))
    comps = [c for c in (doc.get('component') or []) if c in _COMPONENT_TRAIT]
    if comps:
        out = [(l, u) for l, u in out if l.lower() not in _SCHOOLS]
        for c in comps:
            t = _COMPONENT_TRAIT[c]
            if t.lower() not in [l.lower() for l, _ in out]:
                out.append((t, TRAITS.get(t.lower(), AON + '/Traits.aspx')))
    # a spell whose casting calls for a spell attack roll has the attack trait, even where the entry leaves it out
    if 'attack' not in [l.lower() for l, _ in out] and doc.get('name') not in ATTACK_NOT_ON_CAST:
        body = (doc.get('markdown') or '').partition('\n---')[2].split('**Heightened')[0]
        if (doc.get('saving_throw') or '').strip() == 'AC' or re.search(r'spell attack (?:roll|against)', body, re.I):
            out.append(('Attack', TRAITS.get('attack', AON + '/Traits.aspx')))
    rar = [x for x in out if x[0].lower() in ('uncommon', 'rare', 'unique')]
    rest = sorted([x for x in out if x not in rar], key=lambda x: x[0].lower())
    return rar + rest


def entry(name, kind='spell', foundry_kind=None, prefer_source=None):
    """The Archives of Nethys entry for a name. foundry_kind is accepted for older callers and ignored."""
    name = ALIAS.get((name, kind), name)
    cands = _cands(name, kind)
    if not cands:
        base = re.sub(r'\s*\([^)]*\)\s*$', '', name)
        if base != name:
            cands = _cands(base, kind)
    if cands and all(c.get('remaster_id') for c in cands) and not prefer_source:
        # every printing under this name has been replaced: the current one carries a class in its name
        k = _key(name) + ' ('
        alts = [c for n, cs in _load(kind).items() if n.startswith(k) for c in cs if not c.get('remaster_id')]
        alts = [c for c in alts if 'Magus' in (c.get('trait') or [])] or (alts if len(alts) == 1 else [])
        if alts:
            cands = alts
    if not cands:
        raise KeyError(f'{name} ({kind}) is not in the Archives of Nethys data')
    doc = pick(cands, prefer_source)
    e = _aon_entry(doc)
    if name in ACTION_OVERRIDE:
        e['action'] = ACTION_OVERRIDE[name]
    e['remaster'] = not is_legacy(doc)
    e['doc'] = doc
    e['fdoc'] = None
    e.setdefault('kind', kind)
    if kind == 'spell':
        e['traits'] = _spell_traits(e['traits'], doc)
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


