import re, html as H, json
import kit
from kit import ic, stars, grade, slug, ROLES
from entries import entry
from spell_list import RANKS
from occult_list import OCCULT
from spell_evals import E
from picks import P
from heightened import HR
from considered import C as CONSIDERED, CG
from collections import Counter
TRAITS = Counter()

GORDER = 'SABCDF'


def act_codes(e):
    return ' '.join(kit.cast_info(e)[2]) or 'long'


def hr_html(name, r, g, labels):
    rows = []
    for rk, ch, gr in HR.get(name, []):
        cells = ''.join(f'<span class="hrc">{ic(k, "ri ro-" + k)}{lab}{stars(str(ch[lab]))}</span>' for k, lab in ROLES if lab in ch)
        gcells = ''
        if gr:
            gcells = ''.join(f'<span class="hrc">{ic(k)}{lab}{grade(gr[i], lab)}</span>' for i, (k, lab) in enumerate(labels[:1]) if gr[i] != g[i])
        rows.append(f'<div class="hrr"><span class="hrk">Rank {rk}</span><div class="hrv">{cells}{gcells}</div></div>')
    if not rows:
        return ''
    return '<div class="hrt"><p class="hrh">Ratings when heightened</p>' + ''.join(rows) + '</div>'


def best(r, g, name):
    rr = list(r)
    gg = list(g)
    for rk, ch, gr in HR.get(name, []):
        for i, (k, lab) in enumerate(ROLES):
            if lab in ch and ch[lab] > int(rr[i]):
                rr[i] = str(ch[lab])
        if gr:
            for i in range(min(1, len(gg), len(gr))):
                if gr[i] in GORDER and (gg[i] not in GORDER or GORDER.index(gr[i]) < GORDER.index(gg[i])):
                    gg[i] = gr[i]
    return ''.join(rr), ''.join(gg)

STUDIOUS = {'Gecko Grip': 7, 'Blur': 7, 'Haste': 11, 'Ghostly Weapon': 11, 'Fly': 13, 'Translocate': 13}
SLOT_LVL = {1: 1, 2: 3, 3: 5, 4: 7, 5: 9, 6: 11, 7: 13, 8: 15, 9: 17}
missing = []


_SHAPE = re.compile(r'\d+-\s*foot[- ]+(burst|cone|line)', re.I)
_MULTI = re.compile(r'\b(two|three|four|five|six|[2-9])\s+\d+-\s*foot[- ]+burst', re.I)
_ACTS = {'Single Action': '1', 'Two Actions': '2', 'Three Actions': '3'}


AREA_NOT_ON_CAST = {'Blister': 'the cone comes from popping a blister with a later action'}


def _plain(md):
    t = re.sub(r'\{\{\w+ \d+ "([^"]+)"\}\}', r'\1', md or '')
    return re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', t)


def spellstrike_areas(e):
    """Area shapes the spell has when cast with 1 or 2 actions, which is what Spellstrike can deliver.

    A spell whose area depends on the number of actions is read version by version. A spell that creates several
    bursts is left out, because Expansive Spellstrike places a single burst."""
    doc = e.get('doc') or {}
    body = _plain((doc.get('markdown') or '').partition('\n---')[2])
    atxt = _plain(doc.get('area_raw') or '')
    if _MULTI.search(body) or _MULTI.search(atxt):
        return set()
    found = lambda t: {m.lower() for m in _SHAPE.findall(t)}
    parts = re.split(r'<actions string="(Single Action|Two Actions|Three Actions)" />', body.split('**Heightened')[0])
    versions = {_ACTS[parts[i]]: parts[i + 1] for i in range(1, len(parts) - 1, 2)}
    if any(found(v) for v in versions.values()):
        return set().union(*(found(v) for k, v in versions.items() if k in '12'))
    shapes = found(atxt) | {t.lower() for t in (doc.get('area_type') or []) if t.lower() in ('burst', 'cone', 'line')}
    if atxt.strip().lower() in ('', 'varies') and e['name'] not in AREA_NOT_ON_CAST:      # the area is given in the text
        shapes |= found(body.split('**Heightened')[0])
    return shapes


_SAVE_TEXT = re.compile(r'(?:basic|attempts?(?: an?)?(?: initial| new)?|succeeds? (?:at|on) an?|with an?|against an?|makes? an?|rolls? an?|check or)\s+'
                        r'(?:DC \d+ )?(?:basic )?(Fortitude|Reflex|Will)\s+(?:saves?|saving throws?)\b', re.I)
# the entry mentions a save, but not one that casting the spell on a creature requires
SAVE_NOT_ON_CAST = {
    'Elemental Absorption': 'the save is against damage released later',
    'Wall of Mirrors': 'the save is made by a creature that later attacks the wall',
    'Cloak of Colors': 'the save is made by a creature that later hits the target',
    'Zealous Conviction': 'the save is a willing target resisting a later request',
    'Unrelenting Observation': 'the save applies only to an unwilling creature chosen as the sensor',
    'Retrocognition': 'the save is the caster\'s own',
    'Proximal Shift': 'the saves are made by creatures beside the caster\'s own departure and arrival spaces',
}


def _defence(e):
    """(attack roll?, saving throws) a spell requires. The entry's Attack trait and its Defense or Saving Throw line
    decide. An entry with no such line is read for a spell attack roll or a save that creatures attempt."""
    doc = e.get('doc') or {}
    traits = [a.lower() for a, _ in e.get('traits', [])]
    dv = re.sub('<[^>]+>', '', ' '.join(v for k, v in e['fields'] if k == 'Defense')).lower() + ' ' + _plain(doc.get('saving_throw') or '').lower()
    body = _plain((doc.get('markdown') or '').partition('\n---')[2]).split('**Heightened')[0]
    attack = 'attack' in traits or bool(re.search(r'\bac\b', dv))
    saves = [x for x in ('fortitude', 'reflex', 'will') if x in dv]
    if not dv.strip():
        attack = attack or bool(re.search(r'spell attack (?:roll|against)', body, re.I))
        if e['name'] not in SAVE_NOT_ON_CAST:
            found = [m.lower() for m in _SAVE_TEXT.findall(body)]
            saves = [x for x in ('fortitude', 'reflex', 'will') if x in found]
    return attack, saves


def badges(e, name):
    doc = e.get('doc') or {}
    acts = doc.get('actions') or ''
    attack, saves = _defence(e)
    # Spellstrike takes a spell that can be cast with 1 or 2 actions and needs a spell attack roll or a saving throw
    eligible = bool(re.search(r'Single Action|Two Actions', acts)) and (attack or bool(saves))
    shapes = spellstrike_areas(e)
    out = []
    if eligible:
        out.append(f'<span class="bd b-ss" title="Can be delivered with Spellstrike">{ic("spellstrike")}Spellstrike</span>')
        if shapes & {'burst', 'cone', 'line'}:
            out.append(f'<span class="bd b-ex" title="Expansive Spellstrike keeps the area">{ic("expansive")}Expansive</span>')
        if 'line' in shapes:
            out.append(f'<span class="bd b-sp" title="Works with Sprinting Spellstrike">{ic("sprinting")}Sprinting</span>')
    if name in STUDIOUS:
        out.append(f'<span class="bd b-st" title="Laughing Shadow studious spell">{ic("studious")}Studious {STUDIOUS[name]}</span>')
    return ''.join(out), bool(eligible)


def defense_key(e):
    """Space-separated defences a spell targets: 'ac' for an attack roll, plus any saving throw."""
    attack, saves = _defence(e)
    return ' '.join((['ac'] if attack else []) + saves) or 'none'


NO_CAST_TRAITS = {'Blood Vendetta', 'Utter Destruction'}  # listed with neither trait on Archives of Nethys


def card(name, rank, occult_only):
    e = entry(name, 'spell')
    if name not in E:
        missing.append(name)
        r, g, ev = '000000', '---', ''
    else:
        r, g, ev = E[name]
    trads = [t.lower() for t in e['traditions']]
    tg = 'arcane' if 'arcane' in trads else 'occult'
    cantrip = rank == 0
    labels = [('book', 'Spellbook'), ('scroll', 'Scroll'), ('wand', 'Wand')]
    if cantrip and tg == 'occult':
        labels[0] = ('familiar', 'Familiar')
    ratings = '<div class="rate">' + ''.join(
        f'<div class="rc{" zero" if r[i] == "0" else ""}"><span class="rl">{ic(k, "ri ro-" + k)}{lab}</span>{stars(r[i])}</div>'
        for i, (k, lab) in enumerate(ROLES)) + '</div>'
    bd, elig = badges(e, name)
    acc = '<div class="acc">' + ''.join(
        f'<div class="ag">{ic(k)}<span>{lab}</span>{grade(g[i] if i < len(g) else "-", lab)}</div>' for i, (k, lab) in enumerate(labels)) + \
        f'<div class="bds">{bd}</div></div>'
    kick = 'Cantrip' if cantrip else f'Spell {rank}'
    dk = defense_key(e)
    xh = hr_html(name, r, g, labels)
    if xh:
        e = dict(e)
        e['heightened'] = (e.get('heightened') or '') + xh
    br, bg = best(r, g, name)
    tnames = [t for t, _ in e.get('traits', [])]
    # every spell has concentrate or manipulate unless its published entry is checked and listed here
    if not {'concentrate', 'manipulate'} & {t.lower() for t in tnames} and name not in NO_CAST_TRAITS:
        import sys
        print(f'TRAIT CHECK: {name} has neither concentrate nor manipulate: {tnames}', file=sys.stderr)
    # the Spellstrike tags can be filtered like traits
    tnames = tnames + [lab for cls, lab in (('b-ss', 'Spellstrike'), ('b-ex', 'Expansive Spellstrike'), ('b-sp', 'Sprinting Spellstrike'), ('b-st', 'Studious spell')) if cls in bd]
    TRAITS.update(tnames)
    attrs = (f'data-traits="{H.escape("|".join(t.lower() for t in tnames))}" data-rank="{rank}" data-trad="{tg}" data-def="{dk}" data-r="{br}" data-g="{bg}" data-act="{act_codes(e)}" '
             f'data-name="{H.escape(name.lower())}" data-ss="{1 if elig else 0}"')
    return kit.rules_card(e, 'sp-' + slug(name), kicker=kick, extra_top=attrs, evaluation=ev, ratings_html=ratings,
                          access_html=acc, trad_glyph=tg)


def link(n):
    base = n.split(' (')[0]
    extra = n[len(base):]
    return f'<a class="jump" href="#" data-to="sp-{slug(base)}">{H.escape(base)}</a>{H.escape(extra)}'


def item_picks(rank, idx):
    names = RANKS[rank] + OCCULT.get(rank, [])
    order = {'S': 0, 'A': 1}
    best_ = [n for n in names if n in E and len(E[n][1]) > idx and E[n][1][idx] in order]
    best_.sort(key=lambda n: (order[E[n][1][idx]], names.index(n)))
    return best_[:6]


def picks_html(rank):
    p = P.get(rank)
    if not p:
        return ''
    p = dict(p)
    if rank:
        p['scroll'] = item_picks(rank, 1)
        p['wand'] = item_picks(rank, 2)
    roles = ''.join(
        f'<div class="pk">{ic(k, "ro-" + k)}<span class="pl">{lab}</span><span class="pv">{", ".join(link(n) for n in p.get(lab, [])) or "<span class=muted>Nothing stands out</span>"}</span></div>'
        for k, lab in ROLES)
    acc = ''
    for key, lab, icn in [('book', 'Spellbook', 'book'), ('scroll', 'Scrolls', 'scroll'), ('wand', 'Wands', 'wand'), ('familiar', 'Familiar', 'familiar')]:
        if p.get(key):
            acc += f'<div class="pk">{ic(icn)}<span class="pl">{lab}</span><span class="pv">{", ".join(link(n) for n in p[key])}</span></div>'
    cover = ''
    if p.get('saves'):
        rows = ''.join(
            f'<div class="pk">{ic("shieldmagic")}<span class="pl">{d}</span><span class="pv">{", ".join(link(n) for n in p["saves"].get(d, [])) or "<span class=muted>No card at this rank</span>"}</span></div>'
            for d in ('AC', 'Fortitude', 'Reflex', 'Will'))
        types = f'<div class="pk">{ic("damage")}<span class="pl">Damage types</span><span class="pv">{H.escape(p["types"])}</span></div>' if p.get('types') else ''
        cover = f'<h4 class="pkh">Payloads by defence</h4><div class="pkg"><div>{rows}</div><div>{types}</div></div>'
    prep = f'<p class="prep">{H.escape(p["prep"])}</p>' if p.get('prep') else ''
    note = f'<p class="muted small">{H.escape(p["note"])}</p>' if p.get('note') else ''
    title = 'Cantrip picks' if rank == 0 else f'Rank {rank} picks'
    return f'<aside class="picks"><h3>{ic("star")}{title}</h3>{prep}<div class="pkg"><div>{roles}</div><div>{acc}</div></div>{cover}{note}</aside>'


def considered_html(rank):
    d = CONSIDERED.get(rank)
    if not d:
        return ''
    order = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
    items = sorted(d.items(), key=lambda kv: (order.get(CG.get(kv[0], 'D'), 9), kv[0].lower()))
    rows = ''.join(f'<tr><td class="cn">{H.escape(n)}</td><td>{grade(CG.get(n, "D"), "Spellbook")}</td><td>{H.escape(r)}</td></tr>' for n, r in items)
    label = 'Rank 10 arcane spells (a magus never casts these)' if rank == 10 else f'Other arcane spells at this rank ({len(d)})'
    return (f'<details class="considered"><summary>{ic("rules")}{label}</summary>'
            f'<table class="ctab"><thead><tr><th>Spell</th><th>Grade</th><th>Why it has no card</th></tr></thead><tbody>{rows}</tbody></table></details>')


def build():
    secs = []
    nav = []
    for rank in range(0, 10):
        names = [(n, False) for n in RANKS[rank]] + [(n, True) for n in OCCULT.get(rank, [])]
        cards = '\n'.join(card(n, rank, o) for n, o in names)
        if rank == 0:
            h, sub = 'Cantrips', 'Five prepared each day. Cantrips heighten to half Cyrus\'s level, rounded up.'
        else:
            lv = SLOT_LVL[rank]
            sub = f'First slot at level {lv}, second at level {lv + 1}.' if rank > 1 else 'Two slots from level 2.'
        hid = f'rank-{rank}'
        nav.append(f'<a href="#" data-to="{hid}">{"Cantrips" if rank == 0 else "Rank " + str(rank)}</a>')
        secs.append(f'<section class="rank" id="{hid}" data-rank="{rank}"><div class="rh"><h2>{"Cantrips" if rank == 0 else "Rank " + str(rank)}</h2>'
                    f'<p class="muted">{sub}</p></div>{cards}{picks_html(rank)}{considered_html(rank)}{considered_html(10) if rank == 9 else ''}</section>')
    legend = legend_html()
    controls = controls_html()
    page = f'''<div class="page" data-page="spells">
<header class="ph"><h1>Spells, scrolls and wands</h1>
<p class="lede">Every arcane spell has been reviewed for Cyrus: those with a realistic use have full cards, and the rest are listed and graded at the end of each rank with the reason they have none. The page also covers the occult spells he could cast from scrolls, wands and Aspera's stave after a Witch or Psychic dedication at level 9. Rules text is AoN's own wording, with the source under each card. Grades assume one or two fights a day, so spell slots and daily wand casts work out to roughly one per fight.</p></header>
{legend}
{controls}
<p class="count muted" id="spell-count"></p>
{''.join(secs)}
</div>'''
    open('/home/claude/site/pages/spells.html', 'w').write(page)
    print('missing evals:', missing)


STAR_SCALE = [(1, 'Narrow / Weak'), (2, 'Situational / Mediocre'), (3, 'Useful / Solid'), (4, 'Versatile / Strong'),
              (5, 'Universal / Exceptional'), (6, 'Indispensable / Transformative')]
GRADE_NAMES = [('S', 'Core'), ('A', 'Strong'), ('B', 'Situational'), ('C', 'Niche'), ('D', 'Poor'), ('F', 'Unavailable')]


def legend_html():
    roles = ''.join(f'<span class="lg">{ic(k, "ro-" + k)}{lab}</span>' for k, lab in ROLES)
    scale = ''.join(f'<span class="lg">{stars(n)}<span>{t}</span></span>' for n, t in STAR_SCALE)
    grades = ''.join(f'<span class="lg">{grade(g)}<span>{t}</span></span>' for g, t in GRADE_NAMES)
    srcs = ''.join(f'<span class="lg">{ic(i)}{t}</span>' for i, t in [('book', 'Spellbook'), ('scroll', 'Scroll'), ('wand', 'Wand'), ('familiar', 'Familiar cantrip')])
    return f'''<section class="legend">
<div class="lgc"><h4>Roles</h4><div class="lgg c2">{roles}</div></div>
<div class="lgc"><h4>Stars: scope or impact</h4><div class="lgg c1">{scale}</div></div>
<div class="lgc"><h4>Grades by source</h4><div class="lgg c2">{srcs}</div><div class="lgg c2 gap">{grades}</div><p class="muted small lgn">Scroll and wand grades include the action cost. With Aspera in both hands, using either in combat costs at least a regrip, so combat spells grade low unless they solve a specific problem. Utility spells and long-lasting buffs grade highest.</p></div>
<div class="lgc"><h4>Tradition and delivery</h4><div class="lgg c1"><span class="lg">{ic("arcane", "tg t-arcane")}Arcane, in his spellbook</span><span class="lg">{ic("occult", "tg t-occult")}Occult only, from items after level 9</span></div>
<div class="lgg c2 gap"><span class="bd b-ss">{ic("spellstrike")}Spellstrike</span><span class="bd b-ex">{ic("expansive")}Expansive</span><span class="bd b-sp">{ic("sprinting")}Sprinting</span><span class="bd b-st">{ic("studious")}Studious</span></div></div>
</section>'''


SORT_KEYS = [('num:rank', 'Rank'), ('str:name', 'Name'), ('grade:g:0', 'Spellbook grade'), ('grade:g:1', 'Scroll grade'), ('grade:g:2', 'Wand grade')] + \
    [(f'rating:r:{i}', f'{lab} rating') for i, (k, lab) in enumerate(ROLES)] + [('act', 'Action cost'), ('str:def', 'Defense')]


def controls_html():
    defs = [('all', 'Any', None), ('ac', 'AC', 'ac'), ('fortitude', 'Fortitude', 'fortitude'), ('reflex', 'Reflex', 'reflex'),
            ('will', 'Will', 'will'), ('none', 'No roll', None)]
    dbtn = ''.join(f'<button class="chip{" on" if k == "all" else ""}" data-f="def" data-v="{k}">{ic(i, "d-" + i) if i else ""}{lab}</button>' for k, lab, i in defs)
    rbtn = '<button class="chip on" data-f="role" data-v="all">Any</button>' + ''.join(
        f'<button class="chip" data-f="role" data-v="{i}">{ic(k, "ro-" + k)}{lab}</button>' for i, (k, lab) in enumerate(ROLES))
    sbtn = ''.join(f'<button class="chip mini{" on" if n >= 4 else ""}{" purple" if n == 6 else ""}" data-m="stars" data-v="{n}">{min(n, 5)}<span class="st1">★</span></button>' for n in range(1, 7))
    tbtn = (f'<button class="chip on" data-f="trad" data-v="all">Both</button><button class="chip" data-f="trad" data-v="arcane">{ic("arcane", "t-arcane")}Arcane</button>'
            f'<button class="chip" data-f="trad" data-v="occult">{ic("occult", "t-occult")}Occult only</button>')
    abtn = '<button class="chip on" data-f="acc" data-v="all">Any</button>' + ''.join(
        f'<button class="chip" data-f="acc" data-v="{i}">{ic(k)}{lab}</button>' for i, (k, lab) in enumerate([('book', 'Spellbook'), ('scroll', 'Scroll'), ('wand', 'Wand')]))
    acts = [('1', 'one', '1 action'), ('2', 'two', '2 actions'), ('3', 'three', '3 actions'), ('r', 'reaction', 'Reaction'), ('f', 'free', 'Free action')]
    xbtn = ''.join(f'<button class="chip mini act" data-m="acts" data-v="{v}" title="{lab}" aria-label="{lab}">{kit.action_span(k)}</button>' for v, k, lab in acts) + \
        '<button class="chip mini act" data-m="acts" data-v="long" title="Cast over 1 minute or longer">{}Longer</button>'.format(ic('hourglass'))
    gbtn = ''.join(f'<button class="chip mini g-{g}{" on" if g in "SA" else ""}" data-m="grades" data-v="{g}">{g}</button>' for g in 'SABCDF')
    kbtn = ''.join(f'<button class="chip mini rk" data-m="ranks" data-v="{r}">{"Cantrip" if r == 0 else r}</button>' for r in range(10))
    tl = sorted(TRAITS.items(), key=lambda kv: kv[0].lower())
    topts = ''.join(f'<div class="topt" data-n="{H.escape(t.lower())}"><label><input type="checkbox" value="{H.escape(t.lower())}"><span>{H.escape(t)}</span></label><span class="tn">{n}</span><button type="button" class="tx" data-x="{H.escape(t.lower())}" aria-pressed="false" aria-label="Exclude {H.escape(t)}">Exclude</button></div>' for t, n in tl)
    trait_row = f'''<div class="tsel" id="tsel"><button class="chip tbtn" type="button" aria-expanded="false" aria-controls="tpanel">{ic("rules")}<span class="tlab">Choose traits and tags</span><span class="caret" aria-hidden="true">▾</span></button>
<div class="tpanel" id="tpanel" hidden><div class="thead"><label class="search tsearch">{ic("search")}<input type="search" placeholder="Find a trait or tag" autocomplete="off"></label>
<div class="tmode" role="group" aria-label="How to match traits"><button class="chip mini on" type="button" data-tm="any">Any</button><button class="chip mini" type="button" data-tm="all">All</button></div></div>
<div class="tlist">{topts}</div><div class="tfoot"><button class="chip mini" type="button" id="tclear">Clear traits</button><button class="chip mini" type="button" id="tdone">Done</button></div></div>
<div class="tpills" id="tpills"></div></div>'''
    return f'''<details class="fbox" id="spell-filters" open><summary><span>{ic("search")}Filters</span><span class="fact" id="fact"></span></summary>
<div class="controls" id="spell-controls">
<div class="ctop"><label class="search">{ic("search")}<input id="spell-q" type="search" placeholder="Search spells" autocomplete="off"></label><button class="chip" type="button" id="fclear">Clear all filters</button></div>
<div class="cr"><span class="cgl">Rank</span><div class="cc">{kbtn}</div></div>
<div class="cr"><span class="cgl">Actions</span><div class="cc">{xbtn}</div></div>
<div class="cr"><span class="cgl">Defense</span><div class="cc">{dbtn}</div></div>
<div class="cr"><span class="cgl">Traits</span><div class="cc">{trait_row}</div></div>
<div class="cr"><span class="cgl">Role</span><div class="cc">{rbtn}</div></div>
<div class="cr sub" id="stars-row"><span class="cgl">Role rating</span><div class="cc">{sbtn}</div></div>
<div class="cr"><span class="cgl">Tradition</span><div class="cc">{tbtn}</div></div>
<div class="cr"><span class="cgl">Source</span><div class="cc">{abtn}</div></div>
<div class="cr sub" id="grades-row"><span class="cgl">Grade</span><div class="cc">{gbtn}</div></div>
<div class="cr"><span class="cgl">Sort</span><div class="cc">{kit.sort_bar(SORT_KEYS, 'spell-sort')}</div></div>
<div class="cr"><span class="cgl">Show</span><div class="cc"><button class="chip" data-f="ss" data-v="1">{ic("spellstrike")}Spellstrike only</button><button class="chip tog" id="compact">{ic("rules")}Hide rules text</button></div></div>
</div></details>'''


if __name__ == '__main__':
    build()
