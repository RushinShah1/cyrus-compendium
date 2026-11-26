"""Load Foundry PF2e entries and render their description HTML as clean AoN-style rules text."""
import json, pickle, re, math, html

IDX = pickle.load(open('/home/claude/build/idx.pkl', 'rb'))
_AON = {}
for fn in ['/home/claude/build/spell_aon.json']:
    try:
        _AON.update(json.load(open(fn)))
    except Exception:
        pass

PACK_PREF = {'spell': ['spells'], 'feat': ['feats'], 'item': ['equipment'], 'action': ['actions'],
             'feature': ['class-features'], 'any': None}


def get(name, kind='any', pick=None):
    hits = IDX.get(name.lower(), [])
    packs = PACK_PREF.get(kind)
    if packs:
        hits = [h for h in hits if h[0] in packs]
    if not hits:
        raise KeyError(f'{name} ({kind}) not found')
    ds = [json.load(open(f)) for _, f in hits]
    if pick:
        ds = [d for d in ds if pick(d)] or ds
    # prefer remaster
    ds.sort(key=lambda d: (not d['system'].get('publication', {}).get('remaster', False)))
    return ds[0]


def _eval_num(expr, lvl):
    e = expr.replace('@item.level', str(lvl)).replace('@item.rank', str(lvl)).replace('@actor.level', str(lvl))
    e = e.replace('floor', 'math.floor').replace('ceil', 'math.ceil').replace('max', 'max').replace('min', 'min')
    try:
        v = eval(e, {'math': math, 'max': max, 'min': min, 'ternary': lambda c, a, b: a if c else b,
                     'gte': lambda a, b: a >= b, 'gt': lambda a, b: a > b, 'lte': lambda a, b: a <= b,
                     'lt': lambda a, b: a < b, 'eq': lambda a, b: a == b})
        return str(int(v)) if float(v).is_integer() else str(v)
    except Exception:
        return expr


def _formula(f, lvl):
    f = f.strip()
    out, i = '', 0
    while i < len(f):
        m = re.match(r'(floor|ceil|max|min)?\(', f[i:])
        if m:
            j = i + len(m.group(0)); depth = 1
            while j < len(f) and depth:
                if f[j] == '(':
                    depth += 1
                elif f[j] == ')':
                    depth -= 1
                j += 1
            grp = f[i:j]
            if '@' in grp:
                v = _eval_num(grp, lvl)
                if re.fullmatch(r'-?[\d.]+', v):
                    out += v
                else:
                    pre = m.group(0)
                    out += pre + _formula(grp[len(pre):-1], lvl) + ')'
            else:
                out += grp
            i = j
        else:
            out += f[i]; i += 1
    f = out
    if '@' in f:
        f = re.sub(r'[\w.@+\-*/ ]*@[\w.]+[\w.@+\-*/ ]*', lambda m: _eval_num(m.group(0), lvl), f)
    f = f.strip()
    if re.fullmatch(r'[\d+\-*/ ().]+', f):
        f = _eval_num(f, lvl)
    f = re.sub(r'\+0\b', '', f)
    while re.fullmatch(r'\((.*)\)', f) and f.count('(') == 1:
        f = f[1:-1]
    f = re.sub(r'^\((\d+d\d+(?:\+\d+)?)\)$', r'\1', f)
    if f.startswith('(') and f.endswith(')') and f.count('(') == 1:
        f = f[1:-1]
    return f


def _damage(body, lvl):
    # split top-level commas
    parts, depth, cur = [], 0, ''
    for ch in body:
        if ch in '[(':
            depth += 1
        elif ch in '])':
            depth -= 1
        if ch == ',' and depth == 0:
            parts.append(cur); cur = ''
        else:
            cur += ch
    parts.append(cur)
    out = []
    for p in parts:
        m = re.match(r'^(.*)\[([^\[\]]*)\]$', p.strip())
        if not m:
            out.append(_formula(p, lvl)); continue
        form, types = m.group(1), [t.strip() for t in m.group(2).split(',')]
        # nested ((x)[splash])?
        form = re.sub(r'\[(splash|precision)\]', r' \1', form)
        form = _formula(form.strip(), lvl)
        words = []
        if 'persistent' in types: words.append('persistent')
        if 'splash' in types: words.append('splash')
        if 'precision' in types: words.append('precision')
        words += [t for t in types if t not in ('persistent', 'splash', 'precision', 'healing')]
        out.append(f'{form} {" ".join(words)}'.strip())
    return ' plus '.join(out)


TITLE = lambda s: s.replace('-', ' ').title().replace(' Lore', ' Lore')


def render(desc, lvl=1):
    h = desc
    h = re.sub(r'@Embed\[[^\]]*\]', '', h)
    # paragraphs that only hold effect links -> drop
    h = re.sub(r'<p>\s*@UUID\[Compendium\.pf2e\.(?:spell-effects|feat-effects|equipment-effects|other-effects|bestiary-effects|campaign-effects)[^\]]*\](?:\{[^}]*\})?\s*</p>', '', h)
    h = re.sub(r'@UUID\[Compendium\.pf2e\.(?:spell-effects|feat-effects|equipment-effects|other-effects|bestiary-effects|campaign-effects)[^\]]*\](?:\{[^}]*\})?', '', h)

    def uuid(m):
        path, label = m.group(1), m.group(2)
        name = label or path.split('.Item.')[-1].split('.')[-1]
        if 'conditionitems' in path:
            name = name.lower()
        if 'spells-srd' in path:
            return f'<em>{name.lower() if not label else name}</em>'
        return name
    h = re.sub(r'@UUID\[([^\]]+)\](?:\{([^}]*)\})?', uuid, h)

    h = re.sub(r'<p>\s*@Damage\[[^<]*?\]\{[^}]*\}\s*</p>', '', h)

    def dmg(m):
        if m.group(2):
            return m.group(2)
        body = re.sub(r'\|[a-z-]+:[^\]|]*', '', m.group(1))
        return _damage(body, lvl)
    h = re.sub(r'@Damage\[((?:[^\[\]]|\[[^\[\]]*(?:\[[^\[\]]*\])?[^\[\]]*\])*)\](?:\{([^}]*)\})?', dmg, h)

    def chk(m):
        body, label = m.group(1), m.group(2)
        if label:
            return label
        parts = body.split('|')
        typ = parts[0].replace('type:', '')
        opts = {}
        flags = set()
        for p in parts[1:]:
            if ':' in p:
                k, v = p.split(':', 1); opts[k] = v
            else:
                flags.add(p)
        if typ == 'flat':
            return f'DC {opts.get("dc", "?")} flat check'
        name = TITLE(typ)
        dc = opts.get('dc')
        s = ('basic ' if 'basic' in flags or opts.get('basic') == 'true' else '') + name
        if dc and dc.isdigit():
            s = f'DC {dc} ' + s
        return s
    h = re.sub(r'@Check\[([^\]]+)\](?:\{([^}]*)\})?', chk, h)

    def tpl(m):
        body, label = m.group(1), m.group(2)
        if label:
            return label
        opts = dict(p.split(':', 1) for p in body.split('|') if ':' in p)
        typ = opts.get('type') or body.split('|')[0]
        return f'{opts.get("distance", "?")}-foot {typ}'
    h = re.sub(r'@Template\[([^\]]+)\](?:\{([^}]*)\})?', tpl, h)

    def inline(m):
        body, label = m.group(1), m.group(2)
        if label:
            return label
        b = body.strip()
        if b.startswith('/act'):
            return TITLE(b.split()[1])
        mm = re.match(r'/b?r\s+\{?([^}\s#]+)', b)
        if mm:
            return _formula(re.sub(r'\[[^\]]*\]', '', mm.group(1)), lvl)
        return b
    h = re.sub(r'\[\[(.+?)\]\](?:\{([^}]*)\})?', inline, h)
    h = re.sub(r'@Localize\[[^\]]*\]', '', h)
    h = h.replace('<span class="action-glyph">', '<span class="ag" data-a="').replace('</span>', '"></span>') if False else h
    h = re.sub(r'<span class="action-glyph">([^<]+)</span>', lambda m: glyph(m.group(1)), h)
    h = re.sub(r'<p>\s*</p>', '', h)
    h = re.sub(r'\s+</p>', '</p>', h)
    return h.strip()


def glyph(code):
    c = str(code).strip().lower()
    m = {'1': 'one', 'a': 'one', '2': 'two', 'd': 'two', '3': 'three', 't': 'three', 'r': 'reaction', 'f': 'free',
         'reaction': 'reaction', 'free': 'free', 'one': 'one', 'two': 'two', 'three': 'three'}.get(c)
    if not m:
        return code
    ch = {'one': '1', 'two': '2', 'three': '3', 'reaction': 'r', 'free': 'f'}[m]
    return f'<span class="pf" aria-label="{m} action">{ch}</span>'


def split_sections(h):
    """Split rendered description into (header_fields, body_html, heightened_html, extra_tail)."""
    segs = re.split(r'<hr\s*/?>', h)
    head = {}
    # leading Trigger/Requirements/Cost paragraphs
    first = segs[0]
    paras = re.findall(r'<p>(.*?)</p>', first, re.S)
    if paras and all(re.match(r'\s*<strong>(Trigger|Requirements?|Cost|Frequency|Prerequisites?)</strong>', p) for p in paras) and len(segs) > 1:
        for p in paras:
            mm = re.match(r'\s*<strong>([^<]+)</strong>\s*(.*)', p, re.S)
            head[mm.group(1).strip()] = mm.group(2).strip()
        segs = segs[1:]
    for mm in re.finditer(r'<p>\s*<strong>Area</strong>\s*(?:\(continued\))?\s*(.*?)</p>', '\n'.join(segs), re.S):
        head['Area'] = mm.group(1).strip().rstrip('.')
    segs = [re.sub(r'<p>\s*<strong>Area</strong>.*?</p>', '', x, flags=re.S) for x in segs]
    body, height = [], []
    for s in segs:
        if re.search(r'<strong>\s*Heightened', s):
            # a segment may mix text then heightened paragraphs
            ps = re.split(r'(?=<p>\s*<strong>\s*Heightened)', s)
            for p in ps:
                (height if 'Heightened' in p[:60] else body).append(p)
        else:
            body.append(s)
    # body inline leading trigger (feats: "<strong>Trigger</strong> ... <hr/>")
    b = '\n'.join(x.strip() for x in body if x.strip())
    # Feats sometimes inline Requirements/Trigger at the start of the first paragraph without hr
    while True:
        mm = re.match(r'\s*<p>\s*<strong>(Trigger|Requirements?|Frequency|Cost|Prerequisites?)</strong>\s*(.*?)</p>', b, re.S)
        if not mm:
            break
        head[mm.group(1)] = mm.group(2).strip(); b = b[mm.end():]
    return head, b.strip(), '\n'.join(x.strip() for x in height if x.strip())


def aon(name, kind='Spells'):
    if name in _AON:
        return _AON[name]
    from urllib.parse import quote_plus
    return f'https://2e.aonprd.com/Search.aspx?q={quote_plus(name)}'
