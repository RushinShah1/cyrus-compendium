"""Shared helpers: icon sprite, stars, grades, trait chips, rules cards, shell."""
import re, os, html as H

GI = '/home/claude/ext/game-icons'
ICONS = {
    'ancestry': 'delapouite/person', 'heritage': 'lorc/dna1', 'background': 'delapouite/bindle',
    'flank': 'lorc/pincers', 'burst': 'lorc/explosion-rays', 'cone': 'lorc/fire-breath', 'line': 'lorc/fire-ray',
    # navigation
    'home': 'lorc/open-book', 'spells': 'delapouite/spell-book', 'feats': 'lorc/laurel-crown', 'aspera': 'delapouite/glaive',
    'items': 'lorc/swap-bag', 'consumables': 'lorc/potion-ball', 'combat': 'lorc/crossed-swords', 'atlas': 'lorc/treasure-map', 'glossary': 'delapouite/rule-book', 'sheet': 'delapouite/character', 'dice': 'delapouite/dice-twenty-faces-twenty', 'rest': 'lorc/campfire', 'heart': 'lorc/ball-heart', 'corerules': 'lorc/book-cover',
    # traditions
    'arcane': 'lorc/orbital', 'occult': 'lorc/third-eye', 'divine': 'lorc/angel-wings', 'primal': 'delapouite/oak-leaf',
    # roles
    'damage': 'lorc/sword-wound', 'control': 'lorc/manacles', 'debuff': 'lorc/despair', 'buff': 'zeromancer/heart-plus',
    'position': 'lorc/sprint', 'utility': 'delapouite/toolbox',
    # defenses
    'ac': 'lorc/checked-shield', 'fortitude': 'lorc/muscle-up', 'reflex': 'felbrigg/dodge', 'will': 'lorc/brain',
    # access
    'book': 'delapouite/spell-book', 'scroll': 'lorc/scroll-unfurled', 'wand': 'lorc/crystal-wand', 'familiar': 'lorc/raven',
    'staff': 'lorc/wizard-staff',
    # badges and misc
    'spellstrike': 'lorc/spinning-sword', 'expansive': 'lorc/explosion-rays', 'sprinting': 'lorc/lightning-helix',
    'studious': 'lorc/bookmarklet', 'legacy': 'lorc/sands-of-time', 'heighten': 'delapouite/upgrade', 'eval': 'lorc/quill-ink',
    'rules': 'lorc/open-book', 'search': 'lorc/magnifying-glass', 'source': 'lorc/tied-scroll', 'teleport': 'lorc/teleport',
    'trip': 'lorc/tripwire', 'hand': 'sbed/hand', 'shadowgrasp': 'lorc/shadow-grasp', 'reach': 'lorc/spear-hook', 'team': 'delapouite/meeple-group',
    'target': 'lorc/archery-target', 'coins': 'delapouite/two-coins', 'gem': 'lorc/gem-pendant', 'ring': 'delapouite/ring',
    'boots': 'lorc/leather-boot', 'belt': 'lucasms/belt', 'gloves': 'delapouite/gloves', 'armor': 'lorc/breastplate',
    'helm': 'lorc/crested-helmet', 'rune': 'lorc/rune-stone', 'relic': 'lorc/relic-blade', 'hourglass': 'lorc/sands-of-time',
    'mind': 'lorc/brain', 'potion': 'lorc/drink-me', 'bottle': 'lorc/bottled-bolt', 'ghost': 'lorc/ghost', 'flag': 'delapouite/flag-objective',
    'knight': 'skoll/chess-knight', 'crown': 'delapouite/jewel-crown', 'upgrade': 'delapouite/upgrade', 'cap': 'delapouite/graduate-cap', 'talk': 'lorc/conversation',
    'castle': 'delapouite/castle', 'eye': 'delapouite/eye-target', 'invisible': 'delapouite/invisible', 'lightning': 'lorc/lightning-arc',
    'portal': 'lorc/magic-portal', 'gears': 'lorc/gears', 'skull': 'lorc/broken-skull', 'heart': 'lorc/heart-bottle',
    'dice': 'delapouite/rolling-dices', 'star': 'delapouite/star-formation', 'compass': 'lorc/compass', 'clock': 'skoll/pocket-watch',
    'fist': 'lorc/mailed-fist', 'cat': 'lorc/cat', 'web': 'lorc/spider-web', 'footsteps': 'skoll/footsteps', 'stairs': 'delapouite/jump-across',
    'shieldmagic': 'lorc/magic-shield', 'blade': 'lorc/rune-sword', 'brand': 'lorc/spinning-sword', 'bag': 'delapouite/backpack', 'swirl': 'lorc/star-swirl',
}


def sprite(extra=None):
    out = ['<svg xmlns="http://www.w3.org/2000/svg" style="display:none" aria-hidden="true">']
    for k, p in {**ICONS, **(extra or {})}.items():
        svg = open(f'{GI}/{p}.svg').read()
        body = re.sub(r'^<svg[^>]*>|</svg>\s*$', '', svg.strip())
        body = body.replace('<path d="M0 0h512v512H0z"/>', '')
        body = re.sub(r'\sfill="#fff"', '', body)
        out.append(f'<symbol id="i-{k}" viewBox="0 0 512 512">{body}</symbol>')
    out.append('</svg>')
    return '\n'.join(out)


def ic(name, cls='', title=None):
    t = f'<title>{H.escape(title)}</title>' if title else ''
    return f'<svg class="ic {cls}" aria-hidden="{"false" if title else "true"}">{t}<use href="#i-{name}"/></svg>'


ROLES = [('damage', 'Damage'), ('control', 'Control'), ('debuff', 'Debuff'), ('buff', 'Buff / Heal'), ('position', 'Positioning'),
         ('utility', 'Utility')]


def stars(n):
    n = int(n)
    if n >= 6:
        return '<span class="stars ex" title="Exceptional">' + '★' * 5 + '</span>'
    return f'<span class="stars" title="{n} of 5">' + f'<b>{"★" * n}</b>' + '★' * (5 - n) + '</span>'


def grade(g, label=None):
    if g in ('-', '', None):
        return '<span class="gr gr-na" title="Not applicable">–</span>'
    return f'<span class="gr gr-{g}" title="{label or ""} grade {g}">{g}</span>'


RARITY = {'uncommon', 'rare', 'unique'}


def traits(tlist, legacy=False):
    chips = []
    for name, url in tlist:
        low = name.lower()
        cls = 'trait r-' + low if low in RARITY else 'trait'
        chips.append(f'<a class="{cls}" href="{H.escape(url)}">{H.escape(name)}</a>')
    if legacy:
        chips.append(f'<span class="trait legacy" title="Legacy printing, allowed by table rules">{ic("legacy")}Legacy</span>')
    return '<div class="traits">' + ''.join(chips) + '</div>'


def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


def action_span(kind):
    ch = {'one': '1', 'two': '2', 'three': '3', 'reaction': 'r', 'free': 'f'}.get(kind)
    lab = {'one': 'One action', 'two': 'Two actions', 'three': 'Three actions', 'reaction': 'Reaction', 'free': 'Free action'}.get(kind, '')
    return f'<span class="pf" title="{lab}" aria-label="{lab}">{ch}</span>' if ch else ''


_NUM = {'1': 'one', '2': 'two', '3': 'three'}
_WORDS = {'one': '1 action', 'two': '2 actions', 'three': '3 actions', 'reaction': 'reaction', 'free': 'free action'}


def long_span(label):
    return f'<span class="pf-long" title="{H.escape(label)}">{ic("hourglass")}<span>{H.escape(label)}</span></span>'


def cast_info(e):
    """(glyph html for the card header, html for the Cast row, filter codes) for a spell, feat or item."""
    k = e.get('action')
    d = (e.get('fdoc') or {}).get('system', {}) if isinstance(e.get('fdoc'), dict) else {}
    t = str((d.get('time') or {}).get('value') or e.get('action_text') or '').strip()
    tl = t.lower()
    if not k:
        k = {'1': 'one', '2': 'two', '3': 'three', 'reaction': 'reaction', 'free': 'free'}.get(tl)
    if tl in ('2 or 3', 'two actions or three actions'):
        g = action_span('two') + '<span class="to">or</span>' + action_span('three')
        return g, g + ' <span class="muted">2 or 3 actions</span>', ['2', '3']
    if tl.startswith('2 to 2 rounds'):
        g = action_span('two') + '<span class="to">or</span>' + action_span('three') + '<span class="to">or</span>' + long_span('2 rounds')
        return g, g, ['2', '3', 'long']
    m = re.fullmatch(r'([123]) to ([123])', tl)
    if m:
        a, b = m.groups()
        g = action_span(_NUM[a]) + '<span class="to">to</span>' + action_span(_NUM[b])
        return g, g + f' <span class="muted">{a} to {b} actions</span>', [str(i) for i in range(int(a), int(b) + 1)]
    if k in _WORDS:
        code = {'one': '1', 'two': '2', 'three': '3', 'reaction': 'r', 'free': 'f'}[k]
        return action_span(k), action_span(k) + f' <span class="muted">{_WORDS[k]}</span>', [code]
    m = re.fullmatch(r'(\d+)\s*(minute|hour|day|round)s?', tl)
    if m:
        label = f'{m.group(1)} {m.group(2)}{"s" if m.group(1) != "1" else ""}'
        return long_span(label), long_span(label), ['long']
    return '', H.escape(t) if t else '', (['long'] if t else [])


def cast_text(e):
    """Human-readable cast/activation cell: glyph + words."""
    return cast_info(e)[1]


_VAR = re.compile(r'<h5 class="sub">(?P<name>[^<]+)</h5>\s*<div class="traits">(?P<tr>.*?)</div>\s*(?P<rest>(?:(?!<h5 class="sub">).)*)', re.S)


def _variant_level(name):
    import rules
    for n in (name, re.sub(r'^(.*) \((\w+)\)$', r'\2 \1', name)):
        try:
            return rules.get(n, 'item')['system']['level']['value']
        except Exception:
            pass
    return ''


def compress_variants(body):
    """Turn AoN's per-version blocks (name, source, price, change) into one compact table."""
    vs = list(_VAR.finditer(body))
    if len(vs) < 2:
        return body
    rows = []
    for m in vs:
        rest = m.group('rest')
        price = re.search(r'<p><strong>Price</strong>\s*(.*?)</p>', rest, re.S)
        bulk = re.search(r'<p><strong>Bulk</strong>\s*(.*?)</p>', rest, re.S)
        other = re.sub(r'<p><strong>(Source|Price|Bulk)</strong>.*?</p>', '', rest, flags=re.S).strip()
        other = re.sub(r'</?p>', ' ', other).strip() or '<span class="muted">Base version</span>'
        rows.append(f'<tr><td><b>{m.group("name")}</b></td><td class="num">{_variant_level(m.group("name"))}</td>'
                    f'<td class="num">{price.group(1) if price else ""}</td><td>{other}</td></tr>')
    head = body[:vs[0].start()]
    tbl = ('<div class="tw"><table class="tbl vt"><thead><tr><th>Version</th><th class="num">Level</th><th class="num">Price</th>'
           '<th>Changes</th></tr></thead><tbody>' + ''.join(rows) + '</tbody></table></div>')
    return head + tbl


def rules_card(e, cid, kicker='', extra_top='', evaluation='', ratings_html='', access_html='', show_trad=True,
               trad_glyph=None, more_fields=None, heading_level='h3'):
    """Generic card for a spell/feat/action/item with structured stat block."""
    fields = list(e['fields'])
    trad_html = ''
    if show_trad and e.get('traditions'):
        trad_html = '<span class="trads">' + ''.join(
            f'<span class="trad t-{t.lower()}">{ic(t.lower())}{t}</span>' for t in e['traditions']) + '</span>'
    rows = []
    if trad_html:
        rows.append(('Traditions', trad_html))
    ct = cast_text(e)
    if ct:
        rows.append(('Cast' if e.get('kind', 'spell') == 'spell' else 'Activate' if e.get('kind') == 'item' else 'Actions', ct))
    for k, v in fields + (more_fields or []):
        if k == 'Defense':
            v2 = re.sub(r'<[^>]+>', '', v)
            key = 'ac' if 'AC' in v2 else next((x for x in ('fortitude', 'reflex', 'will') if x in v2.lower()), None)
            v = (ic(key, 'def d-' + key) if key else '') + v
        rows.append((k, v))
    dl = ''.join(f'<dt>{k}</dt><dd>{v}</dd>' for k, v in rows)
    glyph = ic(trad_glyph, 'tg t-' + trad_glyph, trad_glyph.title()) if trad_glyph else ''
    height = ''
    if e.get('heightened'):
        hh = re.sub(r'<p>\s*<strong>\s*Heightened\s*\(([^)]*)\)\s*</strong>\s*(.*?)</p>', lambda m: f'<p class="hr"><span class="hl">{ic("heighten")}Heightened ({m.group(1)})</span><span class="hx">{m.group(2)}</span></p>', e['heightened'], flags=re.S)
        height = f'<section class="hgt">{hh}</section>'
    ev = f'<section class="ev"><h4>{ic("eval")}Evaluation</h4><p>{evaluation}</p></section>' if evaluation else ''
    src = f'<span class="src">{ic("source")}{H.escape(e.get("book", ""))}{" · text from Foundry PF2e" if e.get("source") == "foundry" else ""}</span>'
    act = cast_info(e)[0]
    return f'''<article class="card" id="{cid}" {extra_top}>
<header class="ch">{glyph}<{heading_level} class="cn"><a href="{H.escape(e["url"])}">{H.escape(e["name"])}</a></{heading_level}>{act}<span class="kick">{kicker}</span></header>
{traits(e["traits"], legacy=not e.get("remaster", True))}
{ratings_html}{access_html}
<div class="cb{' solo' if not rows else ''}">{'<dl class="st">' + dl + '</dl>' if rows else ''}<section class="rt"><h4>{ic("rules")}Rules text</h4>{compress_variants(e["body"])}</section></div>
{height}{ev}
<footer class="cf">{src}</footer>
</article>'''


def sort_bar(keys, bar_id=None, levels=3):
    """Multi-level sort: one select per level plus a direction toggle. keys: [(value, label)]."""
    opts = '<option value="default">Default order</option>' + ''.join(f'<option value="{v}">{H.escape(l)}</option>' for v, l in keys)
    parts = []
    for i in range(levels):
        lab = ['Sort by', 'then by', 'then by'][min(i, 2)]
        parts.append(f'<span class="slv"><label class="sl"><span>{lab}</span><select aria-label="{lab}">{opts}</select></label>'
                     f'<button type="button" class="chip mini sdir" data-d="asc" aria-label="Ascending">↑</button></span>')
    idattr = f' id="{bar_id}"' if bar_id else ''
    return f'<div class="sortbar"{idattr}>{"".join(parts)}<button type="button" class="chip mini sclear">Reset sort</button></div>'


def trait_dropdown(counts):
    tl = sorted(counts.items(), key=lambda kv: kv[0].lower())
    topts = ''.join(f'<label class="topt" data-n="{H.escape(t.lower())}"><input type="checkbox" value="{H.escape(t.lower())}"><span>{H.escape(t)}</span><span class="tn">{n}</span></label>' for t, n in tl)
    return (f'<div class="tsel"><button class="chip tbtn" type="button" aria-expanded="false">{ic("rules")}<span class="tlab">Choose traits</span><span class="caret" aria-hidden="true">▾</span></button>'
            f'<div class="tpanel" hidden><div class="thead"><label class="search tsearch">{ic("search")}<input type="search" placeholder="Find a trait" autocomplete="off"></label>'
            f'<div class="tmode" role="group" aria-label="How to match traits"><button class="chip mini on" type="button" data-tm="any">Any</button><button class="chip mini" type="button" data-tm="all">All</button></div></div>'
            f'<div class="tlist">{topts}</div><div class="tfoot"><button class="chip mini tclear" type="button">Clear traits</button><button class="chip mini tdone" type="button">Done</button></div></div>'
            f'<div class="tpills"></div></div>')
