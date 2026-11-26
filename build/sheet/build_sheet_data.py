import os
"""Character sheet data: every option a player character can take, from the Foundry PF2e system's structured data
(which carries the rule elements that drive the calculations), linked to the glossary entry that shows its Archives of
Nethys text. Output: /home/claude/site/assets/cs/*.json and /home/claude/build/sheet/extra_gloss.json."""
import json, glob, re, os, sys, html as H
sys.path.insert(0, '/home/claude/build/gloss')
sys.path.insert(0, '/home/claude/build/gen')
import aon_index
import rules as frules

P = '/home/claude/pf2e/packs/pf2e'
OUT = '/home/claude/site/assets/cs'
os.makedirs(OUT, exist_ok=True)
LANG = {}
for f in ('en.json', 're-en.json', 'action-en.json'):
    def flat(d, pre=''):
        for k, v in d.items():
            if isinstance(v, dict):
                flat(v, pre + k + '.')
            else:
                LANG[pre + k] = v
    flat(json.load(open('/home/claude/pf2e/static/lang/' + f)))

PACKS = {  # Foundry compendium name: (folder, short code)
    'feats-srd': ('feats', 'ft'), 'classfeatures': ('class-features', 'cf'), 'ancestryfeatures': ('ancestry-features', 'af'),
    'actionspf2e': ('actions', 'ac'), 'classes': ('classes', 'cl'), 'ancestries': ('ancestries', 'an'), 'heritages': ('heritages', 'he'),
    'backgrounds': ('backgrounds', 'bg'), 'deities': ('deities', 'de'), 'equipment-srd': ('equipment', 'eq'), 'spells-srd': ('spells', 'sp'),
    'conditionitems': ('conditions', 'co'), 'feat-effects': ('feat-effects', 'fe'), 'spell-effects': ('spell-effects', 'se'),
    'equipment-effects': ('equipment-effects', 'ee'), 'other-effects': ('other-effects', 'oe'), 'familiar-abilities': ('familiar-abilities', 'fa'),
}


def sluggify(s):
    s = re.sub(r"[’']", '', s.lower())
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')


RAW = {}          # key -> foundry document
BYNAME, BYID = {}, {}
for pack, (folder, code) in PACKS.items():
    for f in sorted(glob.glob(f'{P}/{folder}/**/*.json', recursive=True)):
        if f.endswith('_folders.json'):
            continue
        d = json.load(open(f))
        if not isinstance(d, dict) or 'system' not in d:
            continue
        key = f'{code}:{sluggify(d["name"])}'
        if key in RAW:
            key += '-' + d['_id'][:4].lower()
        RAW[key] = d
        BYNAME[(pack, d['name'])] = key
        BYID[(pack, d['_id'])] = key
print('foundry documents', len(RAW))

UUID = re.compile(r'^Compendium\.pf2e\.([\w-]+)\.Item\.(.+)$')


def resolve_uuid(u):
    m = UUID.match(u or '')
    if not m:
        return None
    pack, ref = m.group(1), m.group(2)
    return BYID.get((pack, ref)) or BYNAME.get((pack, ref))


def fix(v):
    """Replace compendium references inside rule elements with sheet keys."""
    if isinstance(v, str):
        k = resolve_uuid(v)
        return ('@' + k) if k else v
    if isinstance(v, list):
        return [fix(x) for x in v]
    if isinstance(v, dict):
        return {k: fix(x) for k, x in v.items()}
    return v


UNUSED_RE = {'TokenLight', 'TokenImage', 'TokenEffectIcon', 'TokenMark', 'TokenName', 'Aura', 'EphemeralEffect'}


def clean_rules(rs):
    out = []
    for r in rs or []:
        if r.get('key') in UNUSED_RE:
            continue
        r = {k: v for k, v in r.items() if k not in ('label', 'img') or r.get('key') in ('RollOption', 'ChoiceSet', 'Note', 'FlatModifier', 'Strike', 'DamageDice')}
        out.append(fix(r))
    return out


def tr(s):
    return LANG.get(s, s) if isinstance(s, str) else s


# ───────── glossary links ─────────
bu, bn, bid = aon_index.load()
CATS = {'feat': {'feat', 'class-feature'}, 'action': {'action', 'feat', 'familiar-ability', 'creature-ability', 'skill-general-action'}, 'spell': {'spell', 'ritual'}, 'class': {'class'}, 'ancestry': {'ancestry'},
        'heritage': {'heritage', 'ancestry'}, 'background': {'background'}, 'deity': {'deity'}, 'condition': {'condition'},
        'weapon': {'weapon', 'equipment'}, 'armor': {'armor', 'equipment'}, 'shield': {'shield', 'equipment'},
        'equipment': {'equipment'}, 'consumable': {'equipment'}, 'treasure': {'equipment'}, 'backpack': {'equipment'},
        'kit': {'equipment'}, 'ammo': {'equipment'}, 'effect': set()}


def bookkey(b):
    b = (b or '').lower()
    b = re.sub(r'pathfinder|lost omens|adventure path:|adventures?:|\(hardcover\)|hardcover compilation|#\d+:?|[^a-z0-9 ]', ' ', b)
    return ' '.join(b.replace('archives', 'archive').split())


def nname(s):
    return re.sub(r'[^a-z0-9]+', ' ', (s or '').lower().replace('’', "'")).strip()


LEGACY_BOOKS = {bookkey(x) for x in ['Core Rulebook', "Advanced Player's Guide", 'Gamemastery Guide', 'Secrets of Magic', 'Dark Archive',
                'Gods & Magic', 'Book of the Dead', 'Guns & Gears', 'Lost Omens Character Guide', 'Lost Omens Ancestry Guide', 'Treasure Vault',
                'Lost Omens World Guide', 'Lost Omens Legends', 'Lost Omens Gods & Magic']}
BN = {}
for k, d in bu.items():
    BN.setdefault(nname(d.get('name')), []).append(k)
EXTRA = {}


def gloss_key(d, key):
    typ = d['type']
    cats = CATS.get(typ, set())
    if typ == 'feat' and key.startswith('cf:'):
        cats = {'class-feature', 'feat', 'hybrid-study', 'arcane-school', 'doctrine', 'muse', 'instinct', 'racket', 'mystery', 'patron',
                'bloodline', 'cause', 'methodology', 'research-field', 'style', 'implement', 'innovation', 'hunters-edge', 'way',
                'element', 'conscious-mind', 'subconscious-mind', 'eidolon', 'druidic-order', 'apparition', 'practice', 'lesson',
                'tactic', 'ikon', 'epithet'}
    if typ == 'feat' and key.startswith('af:'):
        cats = {'feat', 'heritage', 'ancestry'}
    book = (d['system'].get('publication') or {}).get('title', '')
    cands = [k for k in BN.get(nname(d['name']), []) if bu[k].get('category') in cats] if cats else []
    if not cands and cats and re.search(r'\([^)]*\)$', d['name']):
        bk = bookkey((d['system'].get('publication') or {}).get('title', ''))
        cands = [k for k in BN.get(nname(re.sub(r'\s*\([^)]*\)$', '', d['name'])), []) if bu[k].get('category') in cats
                 and bookkey(bu[k].get('primary_source')) == bk]
        if len(cands) > 1:
            cands = []
    same = [k for k in cands if bookkey(bu[k].get('primary_source')) == bookkey(book)]
    if same:
        return sorted(same, key=lambda k: k.startswith('d:'))[0]
    rem = (d['system'].get('publication') or {}).get('remaster')
    if cands and not rem:
        return sorted(cands, key=lambda k: k.startswith('d:'))[0]
    if cands:
        # a remastered Foundry entry whose archive match is another printing: use the archive text only when that
        # printing is not a legacy book (the archive predates some remastered books, such as Impossible Magic)
        ok = [k for k in cands if bookkey(bu[k].get('primary_source')) not in LEGACY_BOOKS]
        if ok:
            return sorted(ok, key=lambda k: k.startswith('d:'))[0]
    if typ in ('effect',):
        return None
    # newer than the archive: keep Foundry's own text as a glossary entry
    gk = 'f:' + key
    lvl = (d['system'].get('level') or {}).get('value', 1) or 1
    body = frules.render(d['system'].get('description', {}).get('value', ''), lvl)
    trs = d['system'].get('traits', {}).get('value', []) or []
    th = ''.join(f'<span class="trait">{H.escape(t.replace("-", " ").title())}</span>' for t in trs)
    note = ('<p class="gnote">This printing is newer than the offline Archives of Nethys archive, so its text comes from the '
            'Foundry PF2e system\'s transcription of the same book.</p>')
    TN = {'feat': 'Feat', 'spell': 'Spell', 'action': 'Action', 'weapon': 'Weapon', 'armor': 'Armour', 'shield': 'Shield', 'class': 'Class',
          'ancestry': 'Ancestry', 'heritage': 'Heritage', 'background': 'Background', 'deity': 'Deity'}
    tname = 'Class feature' if key.startswith('cf:') else TN.get(typ, 'Item')
    EXTRA[gk] = [d['name'], tname, (f'<div class="traits">{th}</div>' if th else '') + (f'<p><strong>Source</strong> {H.escape(book.replace("Pathfinder ", ""))}</p>' if book else '') + body + note, '']
    return gk


# ───────── records ─────────
def price_cp(p):
    v = (p or {}).get('value') or {}
    return int(round(v.get('pp', 0) * 1000 + v.get('gp', 0) * 100 + v.get('sp', 0) * 10 + v.get('cp', 0)))


def common(key, d):
    s = d['system']
    t = s.get('traits') or {}
    r = {'k': key, 'n': d['name'], 't': d['type'], 'sl': s.get('slug') or sluggify(d['name'])}
    lv = (s.get('level') or {}).get('value') if isinstance(s.get('level'), dict) else s.get('level')
    if lv is not None:
        r['lv'] = lv
    if t.get('value'):
        r['tr'] = t['value']
    if t.get('otherTags'):
        r['tags'] = t['otherTags']
    rar = t.get('rarity') or s.get('rarity')
    if rar and rar != 'common':
        r['rar'] = rar
    pub = s.get('publication') or {}
    if pub.get('title'):
        r['src'] = pub['title'].replace('Pathfinder ', '')
    rs = clean_rules(s.get('rules'))
    if rs:
        r['rules'] = rs
    g = gloss_key(d, key)
    if g:
        r['g'] = g
    return r


def acts(s):
    at = (s.get('actionType') or {}).get('value')
    n = (s.get('actions') or {}).get('value')
    if at == 'action':
        return str(n or 1)
    return at if at in ('reaction', 'free') else None


DB = {}
for key, d in RAW.items():
    s = d['system']
    typ = d['type']
    r = common(key, d)
    if typ in ('feat', 'action'):
        cat = s.get('category')
        if cat:
            r['cat'] = cat
        a = acts(s)
        if a:
            r['act'] = a
        pre = [x.get('value') for x in (s.get('prerequisites') or {}).get('value', []) if x.get('value')]
        if pre:
            r['pre'] = pre
        if s.get('maxTakable') not in (None, 1):
            r['max'] = s['maxTakable']
        if s.get('selfEffect'):
            se = resolve_uuid(s['selfEffect'].get('uuid'))
            if se:
                r['se'] = se
        sf = s.get('subfeatures') or {}
        sf = {k: v for k, v in sf.items() if v}
        if sf:
            r['sub'] = sf
        if s.get('frequency'):
            r['freq'] = s['frequency']
        if s.get('onlyLevel1'):
            r['l1'] = 1
    elif typ == 'class':
        r.update(hp=s['hp'], key=s['keyAbility']['value'], perc=s['perception'], saves=s['savingThrows'], atk=s['attacks'],
                 dfn=s['defenses'], sc=s.get('spellcasting', 0), skills=s['trainedSkills'],
                 lv={k: s[k]['value'] for k in ('ancestryFeatLevels', 'classFeatLevels', 'generalFeatLevels', 'skillFeatLevels', 'skillIncreaseLevels')},
                 items=sorted([[v['level'], resolve_uuid(v['uuid'])] for v in s['items'].values() if resolve_uuid(v['uuid'])]))
    elif typ == 'ancestry':
        r.update(hp=s['hp'], size=s['size'], speed=s['speed'], boosts=[v['value'] for v in s['boosts'].values()],
                 flaws=[v['value'] for v in s['flaws'].values()], langs=s['languages']['value'], addl=s['additionalLanguages'],
                 vision=s.get('vision'), reach=s.get('reach', 5), hands=s.get('hands', 2),
                 items=[resolve_uuid(v['uuid']) for v in (s.get('items') or {}).values() if resolve_uuid(v['uuid'])])
    elif typ == 'heritage':
        r['anc'] = (s.get('ancestry') or {}).get('slug')
    elif typ == 'background':
        r.update(boosts=[v['value'] for v in s['boosts'].values()], skills=s['trainedSkills'],
                 items=[resolve_uuid(v['uuid']) for v in (s.get('items') or {}).values() if resolve_uuid(v['uuid'])])
    elif typ == 'deity':
        r.update(font=s.get('font'), skill=s.get('skill'), weapons=s.get('weapons'), attr=s.get('attribute'),
                 domains=s.get('domains'), sanct=s.get('sanctification'), cat=s.get('category'))
    elif typ == 'spell':
        tt = s.get('traits') or {}
        r.update(trad=tt.get('traditions') or [], time=(s.get('time') or {}).get('value'), rng=(s.get('range') or {}).get('value'),
                 area=s.get('area'), dfn=s.get('defense'), dur=(s.get('duration') or {}).get('value'),
                 sus=(s.get('duration') or {}).get('sustained'), tgt=(s.get('target') or {}).get('value'))
        if s.get('ritual'):
            r['ritual'] = 1
        dm = {i: {'f': v.get('formula'), 't': v.get('type'), 'c': v.get('category'), 'h': 1 if 'healing' in (v.get('kinds') or []) and 'damage' not in (v.get('kinds') or []) else (2 if 'healing' in (v.get('kinds') or []) else 0)}
              for i, v in (s.get('damage') or {}).items() if v.get('formula')}
        if dm:
            r['dmg'] = dm
            ht = s.get('heightening') or {}
            if ht.get('type') == 'interval' and ht.get('damage'):
                r['hti'] = [ht.get('interval', 1), ht['damage']]
            elif ht.get('type') == 'fixed':
                fx = {lv: {i: v.get('formula') for i, v in (x.get('damage') or {}).items() if isinstance(v, dict) and v.get('formula')} for lv, x in (ht.get('levels') or {}).items()}
                fx = {lv: v for lv, v in fx.items() if v}
                if fx:
                    r['htf'] = fx
        r = {k: v for k, v in r.items() if v not in (None, '', [], False)}
    elif typ in ('weapon', 'armor', 'shield', 'equipment', 'consumable', 'treasure', 'backpack', 'kit', 'ammo'):
        r['cp'] = price_cp(s.get('price'))
        r['bulk'] = (s.get('bulk') or {}).get('value', 0)
        if (s.get('apex') or {}).get('attribute'):
            r['apex'] = s['apex']['attribute']   # the attribute an apex item raises when invested
        use = (s.get('usage') or {}).get('value')
        if use:
            r['use'] = use
        if s.get('baseItem'):
            r['base'] = s['baseItem']
        if typ == 'weapon':
            r.update(cat=s['category'], grp=s.get('group'), dmg=s['damage'], rng=s.get('range'), reload=(s.get('reload') or {}).get('value'),
                     runes=s.get('runes'), spec=1 if s.get('specific') else 0)
            if s.get('splashDamage', {}).get('value'):
                r['splash'] = s['splashDamage']['value']
            if (s.get('bonusDamage') or {}).get('value'):
                r['bdmg'] = s['bonusDamage']['value']
            if (s.get('bonus') or {}).get('value'):
                r['bonus'] = s['bonus']['value']
        elif typ == 'armor':
            r.update(cat=s['category'], grp=s.get('group'), ac=s['acBonus'], dex=s.get('dexCap'), chk=s.get('checkPenalty', 0),
                     spd=s.get('speedPenalty', 0), str=s.get('strength'), runes=s.get('runes'), spec=1 if s.get('specific') else 0)
        elif typ == 'shield':
            r.update(ac=s['acBonus'], hard=s.get('hardness', 0), hp=(s.get('hp') or {}).get('max', 0), spd=s.get('speedPenalty', 0),
                     runes=s.get('runes'))
        elif typ == 'consumable':
            r['cat'] = s.get('category')
            if (s.get('uses') or {}).get('max'):
                r['uses'] = s['uses']['max']
            if s.get('damage'):
                r['dmgf'] = s['damage']
        elif typ == 'backpack':
            r['cap'] = (s.get('bulk') or {}).get('capacity')
            r['ign'] = (s.get('bulk') or {}).get('ignored')
        elif typ == 'kit':
            r['kit'] = [[resolve_uuid(v.get('uuid')), v.get('quantity', 1)] for v in (s.get('items') or {}).values() if resolve_uuid(v.get('uuid'))]
        if s.get('quantity', 1) not in (1, None):
            r['qty'] = s['quantity']
    elif typ in ('effect', 'condition'):
        if typ == 'condition':
            r['val'] = (s.get('value') or {}).get('isValued')
            if s.get('overrides'):
                r['over'] = s['overrides']
            r['g'] = gloss_key({**d, 'type': 'condition'}, key)
        bd = s.get('badge')
        if bd:
            r['badge'] = bd
        if s.get('duration'):
            r['dur'] = s['duration']
    DB[key] = r

# ───────── legacy entries the remaster renamed: still available, without rule automation ─────────
import ast
def _l(v):
    try:
        return ast.literal_eval(v) if isinstance(v, str) else (v or [])
    except Exception:
        return []
def basename(n):
    return re.sub(r'[^a-z0-9]', '', re.sub(r'\s*\([^)]*\)\s*$', '', (n or '').lower()))
FNAMES = {basename(r['n']) + '|' + r['t'] for r in DB.values()}
CLASSES = {r['sl'] for r in DB.values() if r['t'] == 'class'}
ANCS = {r['sl'] for r in DB.values() if r['t'] == 'ancestry'}
nleg = 0
for fname, typ in (('spells', 'spell'), ('equipment', 'equipment'), ('feats', 'feat')):
    for x in json.load(open(f'/home/claude/ext/aon/2e/data/{fname}.json')):
        rn = _l(x.get('remaster_name'))
        if not rn or basename(rn[0]) == basename(x['name']):
            continue
        t = typ
        trs = [sluggify(t2) for t2 in _l(x.get('trait_raw') or x.get('trait'))]
        if typ == 'equipment':
            cat = x.get('item_category') or ''
            if cat in ('Weapons', 'Armor', 'Shields'):
                continue
            t = 'consumable' if 'consumable' in trs else 'equipment'
        if basename(x['name']) + '|' + t in FNAMES:
            continue
        key = 'lg:' + sluggify(x['name'])
        if key in DB:
            continue
        gk = bid.get(x.get('id'))
        r = {'k': key, 'n': x['name'], 't': t, 'sl': sluggify(x['name']), 'lv': int(x.get('level') or 0) if str(x.get('level') or '0').lstrip('-').isdigit() else 0,
             'tr': trs, 'src': x.get('primary_source'), 'leg': 1, 'now': rn[0]}
        if (x.get('rarity') or 'common') != 'common':
            r['rar'] = x['rarity'].lower()
        if gk:
            r['g'] = gk
        if 'apex' in trs:
            am = re.search(r'increase your (Strength|Dexterity|Constitution|Intelligence|Wisdom|Charisma) (?:score|modifier)', x.get('markdown') or '')
            if am:
                r['apex'] = am.group(1)[:3].lower()
        if t == 'spell':
            r['trad'] = [y.lower() for y in _l(x.get('tradition'))]
            a = (x.get('actions') or '').lower()
            r['time'] = {'single action': '1', 'two actions': '2', 'three actions': '3', 'reaction': 'reaction', 'free action': 'free'}.get(a, a)
            if x.get('spell_type') == 'Cantrip':
                r['tr'] = r['tr'] + ['cantrip']
            if x.get('spell_type') == 'Focus':
                r['tr'] = r['tr'] + ['focus']
            if x.get('spell_type') == 'Ritual':
                continue
        elif t in ('equipment', 'consumable'):
            r['cp'] = int(float(x.get('price') or 0))
            b = x.get('bulk')
            r['bulk'] = float(b) if b not in (None, '', '-') and re.match(r'^[0-9.]+$', str(b)) else 0
            if x.get('usage'):
                r['use'] = sluggify(x['usage'])
        else:
            if 'archetype' in trs or 'dedication' in trs:
                r['cat'] = 'class'
            elif 'general' in trs:
                r['cat'] = 'skill' if 'skill' in trs else 'general'
            elif 'skill' in trs:
                r['cat'] = 'skill'
            elif any(t2 in CLASSES for t2 in trs):
                r['cat'] = 'class'
            else:
                r['cat'] = 'ancestry'
            pre = re.search(r'\*\*Prerequisites\*\*\s*([^\n<]+)', x.get('markdown') or '')
            if pre:
                r['pre'] = [re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', p2).strip() for p2 in pre.group(1).split(';') if p2.strip()]
        DB[key] = r
        nleg += 1
print('renamed legacy entries added', nleg)

# ───────── spells per day, from the Foundry class journals ─────────
SLOTS = {}
jd = json.load(open(f'{P}/journals/classes.json'))
for page in jd['pages']:
    h = (page.get('text') or {}).get('content') or ''
    for tb in re.findall(r'<table.*?</table>', h, re.S):
        rows = [[re.sub(r'<[^>]+>', '', c).strip() for c in re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>', row, re.S)]
                for row in re.findall(r'<tr.*?</tr>', tb, re.S)]
        rows = [x for x in rows if x]
        if not rows or 'Cantrips' not in rows[0]:
            continue
        head = rows[0]
        tab = {}
        for row in rows[1:]:
            if not row[0].isdigit():
                continue
            vals = []
            for c in row[1:]:
                c = c.replace('—', '').replace('-', '').replace('*', '').strip()
                vals.append(int(re.match(r'\d+', c).group(0)) if re.match(r'\d+', c) else 0)
            tab[int(row[0])] = vals
        SLOTS.setdefault(page['name'].lower(), []).append({'head': head, 'rows': tab})
print('spell tables', {k: len(v) for k, v in SLOTS.items()})

REFS = set(re.findall(r'"(PF2E\.[A-Za-z0-9_.]+)"', json.dumps(DB)))
core = {'v': 1, 'slots': SLOTS, 'runes': json.load(open('/home/claude/build/sheet/runes.json')), 'materials': json.load(open('/home/claude/build/sheet/materials.json')),
        'lang': {k: v for k, v in LANG.items() if re.match(r'PF2E\.(Skill|Saves?|Ability|Attribute|WeaponGroup|Weapon\.Base|ArmorGroup|Trait|Language|SpecificRule|WeaponPropertyRune|ArmorPropertyRune|ConditionType|Damage|Item\.Weapon\.Rune|ArmorPotencyRune|WeaponPotencyRune|ArmorResilientRune|WeaponStrikingRune|PreciousMaterial|BulkTypes|PersistentDamage|ProficiencyLevel|TraitDescription)', k) and isinstance(v, str) and len(v) < 800}}
core['lang'].update({k: LANG[k] for k in REFS if k in LANG and isinstance(LANG[k], str)})
groups = {'core': ('class', 'ancestry', 'heritage', 'background', 'deity', 'condition'),
          'feats': ('feat',), 'actions': ('action',), 'items': ('weapon', 'armor', 'shield', 'equipment', 'consumable', 'treasure', 'backpack', 'kit', 'ammo'),
          'spells': ('spell',), 'effects': ('effect',)}
sizes = {}
for g, types in groups.items():
    recs = {k: v for k, v in DB.items() if v['t'] in types}
    obj = {'v': 1, 'e': recs}
    if g == 'core':
        # Forgotten Realms deities: lore with proposed Pathfinder statistics, built by fr/build_fr.py
        frp = '/home/claude/build/fr/fr_deities.json'
        if os.path.exists(frp):
            obj['e'].update(json.load(open(frp)))
        obj.update(core)
    p = f'{OUT}/{g}.json'
    json.dump(obj, open(p, 'w'), separators=(',', ':'), ensure_ascii=False)
    sizes[g] = (len(recs), round(os.path.getsize(p) / 1e6, 2))
print(sizes)
json.dump(EXTRA, open('/home/claude/build/sheet/extra_gloss.json', 'w'), ensure_ascii=False)
print('foundry-only glossary entries', len(EXTRA))
