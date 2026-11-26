"""Forgotten Realms deities for the character sheet and the rules glossary.

Reads fr_data1.py and fr_data2.py, checks every weapon, domain and spell against the sheet data, and writes:
  fr_deities.json  sheet records (merged into core.json by sheet/build_sheet_data.py)
  fr_gloss.json    glossary entries of type 'Deity (Forgotten Realms)' (merged by gloss/build_glossary.py)
"""
import html as H
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from fr_data1 import FAERUNIAN
from fr_data2 import DWARVEN, ELVEN, DROW, HALFLING, GNOMISH, ORCISH

CS = '/home/claude/site/assets/cs'
HERE = os.path.dirname(os.path.abspath(__file__))
TYPE = 'Deity (Forgotten Realms)'
PANTHEONS = [('Faerûnian pantheon', FAERUNIAN), ('Morndinsamman (dwarven pantheon)', DWARVEN), ('Seldarine (elven pantheon)', ELVEN),
             ('Dark Seldarine (drow pantheon)', DROW), ("Yondalla's Children (halfling pantheon)", HALFLING),
             ('Lords of the Golden Hills (gnome pantheon)', GNOMISH), ('Orc pantheon', ORCISH)]
ALIGN = {'LG': 'lawful good', 'NG': 'neutral good', 'CG': 'chaotic good', 'LN': 'lawful neutral', 'N': 'neutral',
         'CN': 'chaotic neutral', 'LE': 'lawful evil', 'NE': 'neutral evil', 'CE': 'chaotic evil'}
ATTR = {'str': 'Strength', 'dex': 'Dexterity', 'con': 'Constitution', 'int': 'Intelligence', 'wis': 'Wisdom', 'cha': 'Charisma'}
F_AND_P = 'Faiths and Pantheons (2002)'

items = json.load(open(f'{CS}/items.json'))['e']
spells = json.load(open(f'{CS}/spells.json'))['e']
core = json.load(open(f'{CS}/core.json'))['e']
gidx = json.load(open('/home/claude/site/assets/g/index.json'))
types = gidx['t']
spell_by_name = {}
for k, r in spells.items():
    if not r.get('leg'):
        spell_by_name.setdefault(r['n'].lower(), r)
domains = set()
for r in core.values():
    if r.get('t') == 'deity' and r.get('domains'):
        domains |= set(r['domains'].get('primary') or []) | set(r['domains'].get('alternate') or [])


def gkey(name, typ):
    """Glossary key for a name of a given AoN type, or None."""
    want = name.lower()
    for k, v in gidx['e'].items():
        if v[0].lower() == want and types[v[1]] == typ and not v[3]:
            return k
    return None


def link(name, key, em=False):
    t = f'<em>{H.escape(name)}</em>' if em else H.escape(name)
    return f'<a href="#" data-g="{key}">{t}</a>' if key else t


SKILL_KEYS = {s: gkey(s.title(), 'Skill') for s in ['acrobatics', 'arcana', 'athletics', 'crafting', 'deception', 'diplomacy', 'intimidation', 'medicine', 'nature',
                                                    'occultism', 'performance', 'religion', 'society', 'stealth', 'survival', 'thievery']}
DOMAIN_KEYS = {}
FONT_KEYS = {'heal': (spells.get('sp:heal') or {}).get('g'), 'harm': (spells.get('sp:harm') or {}).get('g')}

errors, recs, gloss = [], {}, {}
for pan, rows in PANTHEONS:
    for row in rows:
        (slug, name, title, al, portfolio, symbol, lore, edicts, anathema, sanct, attrs, font, skill, (wname, wslug),
         doms, alt, cspells, src) = row
        w = items.get('eq:' + wslug) or ({'n': 'Fist', 'g': gkey('Fist', 'Weapon')} if wslug == 'fist' else None)
        if not w:
            errors.append(f'{name}: weapon {wslug}')
        for d in doms + alt:
            if d not in domains:
                errors.append(f'{name}: domain {d}')
        sp = []
        for _, sn in sorted(cspells.items()):
            r = spell_by_name.get(sn.lower())
            if not r:
                errors.append(f'{name}: spell {sn}')
                continue
            sp.append(r)
        sp.sort(key=lambda r: r.get('lv') or 0)
        if skill not in SKILL_KEYS:
            errors.append(f'{name}: skill {skill}')
        key = 'fr-' + slug
        s_modal, s_what = (sanct.split('-') if sanct else (None, None))
        recs['de:' + key] = {'k': 'de:' + key, 'n': name, 't': 'deity', 'sl': key, 'src': 'Forgotten Realms, conversion', 'g': 'fr:' + slug,
                             'font': font, 'skill': [skill], 'weapons': [wslug], 'attr': attrs,
                             'domains': {'primary': doms, 'alternate': alt},
                             'sanct': {'modal': s_modal, 'what': [s_what]} if sanct else None,
                             'cat': 'deity', 'fr': 1, 'pan': pan, 'title': title}
        for d in doms + alt:
            if d not in DOMAIN_KEYS:
                DOMAIN_KEYS[d] = gkey(d.title(), 'Domain')
        sanct_txt = {'holy-must': 'must choose holy', 'holy-can': 'can choose holy', 'unholy-must': 'must choose unholy',
                     'unholy-can': 'can choose unholy'}.get(sanct, 'none')
        wl = link((w or {}).get('n', wslug.replace('-', ' ').title()), (w or {}).get('g'))
        if wname.lower() != (w or {}).get('n', '').lower():
            wl += f' ({H.escape(wname)} in Forgotten Realms lore)'
        html = (
            f'<div class="traits"><span class="trait fr">Forgotten Realms</span></div>'
            f'<p><strong>Source</strong> Forgotten Realms. Alignment and symbol from {H.escape(src)}; portfolio and favoured weapon from {F_AND_P}. '
            f'The Pathfinder statistics under Devotee Benefits are a proposed conversion, to be agreed with the GM.</p>'
            f'<p>{H.escape(lore)}</p>'
            f'<p><strong>Title</strong> {H.escape(name)}, {H.escape(title)}</p>'
            f'<p><strong>Pantheon</strong> {H.escape(pan)}</p>'
            f'<p><strong>Alignment</strong> {ALIGN[al].capitalize()} ({al})</p>'
            f'<p><strong>Area of Concern</strong> {H.escape(portfolio)}</p>'
            f'<p><strong>Religious Symbol</strong> {H.escape(symbol)}</p>'
            f'<p><strong>Edicts</strong> {H.escape(", ".join(edicts))}</p>'
            f'<p><strong>Anathema</strong> {H.escape(", ".join(anathema))}</p>'
            f'<h5 class="sub">Devotee Benefits (proposed conversion)</h5>'
            f'<p><strong>Divine Attribute</strong> {" or ".join(ATTR[a] for a in attrs)}</p>'
            f'<p><strong>Divine Font</strong> {" or ".join(link(f.title(), FONT_KEYS.get(f)) for f in font)}</p>'
            f'<p><strong>Divine Sanctification</strong> {sanct_txt}</p>'
            f'<p><strong>Divine Skill</strong> {link(skill.title(), SKILL_KEYS.get(skill))}</p>'
            f'<p><strong>Favored Weapon</strong> {wl}</p>'
            f'<p><strong>Domains</strong> {", ".join(link(d, DOMAIN_KEYS.get(d)) for d in doms)}</p>'
            f'<p><strong>Alternate Domains</strong> {", ".join(link(d, DOMAIN_KEYS.get(d)) for d in alt)}</p>'
            f'<p><strong>Cleric Spells</strong> {"; ".join(("cantrip" if "cantrip" in (r.get("tr") or []) else f"rank {r.get(chr(108) + chr(118))}") + ": " + link(r["n"].lower(), r.get("g"), em=True) for r in sp)}</p>'
        )
        gloss['fr:' + slug] = [name, TYPE, html, 0]

if errors:
    print('\n'.join(errors))
    sys.exit(1)
json.dump(recs, open(f'{HERE}/fr_deities.json', 'w'), ensure_ascii=False)
json.dump(gloss, open(f'{HERE}/fr_gloss.json', 'w'), ensure_ascii=False)
print('deities', len(recs), 'by pantheon', {p: len(r) for p, r in PANTHEONS})
