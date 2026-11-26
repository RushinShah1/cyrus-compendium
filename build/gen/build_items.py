import html as H, re
import kit
from kit import ic, stars, grade, slug
from entries import entry, rule_html
from item_data import I, ITEM_ROLES
from collections import Counter


def rate(r):
    return '<div class="rate">' + ''.join(
        f'<div class="rc{" zero" if r[i] == "0" else ""}"><span class="rl">{ic(k, "ri")}{lab}</span>{stars(r[i])}</div>'
        for i, (k, lab) in enumerate(ITEM_ROLES)) + '</div>'


TRAITS = Counter()


def _lvl(e):
    m = re.search(r'\d+', str(e.get('level', '')))
    return int(m.group()) if m else 0


def icard(n, data, kind='item'):
    try:
        e = entry(n, kind, foundry_kind='item')
    except KeyError:
        e = entry(n, kind, foundry_kind='any')
    tnames = [t for t, _ in e.get('traits', [])]
    TRAITS.update(tnames)
    plan = data.get('plan')
    pbadge = ''
    if plan:
        pbadge = f'<span class="bd plan plan-{plan[1].lower()}">{ic("flag")}{plan[1]} at {plan[0]}</span>'
    band = data.get('band')
    bands = (f'<span class="bd">{ic("clock")}{H.escape(band)}</span>' if band else '')
    acc = f'<div class="acc"><div class="ag">{ic("coins")}<span>Grade</span>{grade(data["g"])}</div><div class="bds">{pbadge}{bands}</div></div>'
    lvl = e['level'] if str(e['level']).startswith(('Item', 'Weapon', 'Relic')) else f'Item {e["level"]}'
    inv = '1' if any(t.lower() == 'invested' for t in tnames) else '0'
    cat = slug(data['cat'])
    attrs = (f'data-name="{H.escape(n.lower())}" data-lvl="{_lvl(e)}" data-cat="{cat}" data-g="{data["g"]}" data-r="{data["r"]}" '
             f'data-inv="{inv}" data-plan="{(plan[1].lower() + " " + str(plan[0])) if plan else ""}" data-planlvl="{plan[0] if plan else ""}" '
             f'data-act="@@ACT@@" data-traits="{H.escape("|".join(t.lower() for t in tnames))}"')
    h = kit.rules_card(e, 'it-' + slug(n), kicker=lvl, extra_top=attrs, evaluation=data['ev'], ratings_html=rate(data['r']), access_html=acc, show_trad=False)
    rt = h.split('class="ev', 1)[0] if 'class="ev' in h else h
    acts = []
    for t in re.findall(r'class="pf[^"]*" title="([^"]+)"', rt):
        t = t.lower()
        code = '1' if t.startswith('one') or t.startswith('single') else '2' if t.startswith('two') else '3' if t.startswith('three') else 'r' if 'reaction' in t else 'f' if 'free' in t else None
        if code and code not in acts:
            acts.append(code)
    if re.search(r'Activate[^<]{0,80}?(minute|hour|day)', rt) and 'long' not in acts:
        acts.append('long')
    return h.replace('@@ACT@@', ' '.join(acts) or 'none', 1)


def rules_box(rid, title=None, open_=False):
    h, n = rule_html(rid)
    return (f'<details class="rbox"{" open" if open_ else ""}><summary>{ic("rules")}{H.escape(title or n)} '
            f'<span class="muted">rules text, AoN</span></summary><div class="rt">{h}'
            f'<p class="muted small"><a href="https://2e.aonprd.com/Rules.aspx?ID={rid}">Open on Archives of Nethys</a></p></div></details>')


def table(head, rows, cls='stack', num=()):
    th = ''.join(f'<th class="{"num" if i in num else ""}">{h}</th>' for i, h in enumerate(head))
    trs = ''.join('<tr>' + ''.join(f'<td data-l="{head[i]}" class="{"num" if i in num else ""}">{c}</td>' for i, c in enumerate(r)) + '</tr>' for r in rows)
    return f'<div class="tw"><table class="tbl {cls}"><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>'


def J(n, pre='it'):
    return f'<a href="#" data-to="{pre}-{slug(n)}">{H.escape(n)}</a>'


def chips(k, opts, mode='single', default='all'):
    return ''.join(f'<button class="chip{" mini" if mode == "multi" else ""}{" on" if mode == "single" and v == default else ""}" type="button" data-k="{k}" data-mode="{mode}" data-v="{v}">{lab}</button>' for v, lab in opts)


def catalog_controls(cats, roles, sort_keys, levels=True, invest=True, plan=True, label='items'):
    rows = []
    if levels:
        rows.append(('Item level', chips('lvl', [('1-4', '1–4'), ('5-8', '5–8'), ('9-12', '9–12'), ('13-16', '13–16'), ('17-20', '17–20')], 'multi')))
    rows.append(('Category', chips('cat', [(slug(c), c) for c in cats], 'multi')))
    if plan:
        rows.append(('Purchase plan', chips('plan', [('all', 'Any'), ('plan', 'In the plan'), ('core', 'Core purchases only')])))
    rows.append(('Grade', chips('g', [(g, g) for g in 'SABCD'], 'multi')))
    rows.append(('Role', chips('role', [('all', 'Any')] + [(str(i), f'{ic(k)}{lab}') for i, (k, lab) in enumerate(roles)])))
    sb = ''.join(f'<button class="chip mini{" on" if n >= 4 else ""}{" purple" if n == 6 else ""}" type="button" data-m="stars" data-v="{n}">{min(n, 5)}<span class="st1">★</span></button>' for n in range(1, 7))
    rows.append(('Role rating', sb, 'sub stars-row'))
    if invest:
        rows.append(('Invested', chips('inv', [('all', 'Any'), ('1', 'Invested'), ('0', 'Not invested')])))
    acts = [('1', 'one', '1 action'), ('2', 'two', '2 actions'), ('r', 'reaction', 'Reaction'), ('f', 'free', 'Free action'), ('long', None, 'Longer'), ('none', None, 'Passive')]
    rows.append(('Activation', ''.join(f'<button class="chip mini act" type="button" data-k="act" data-mode="multi" data-v="{v}" title="{lab}" aria-label="{lab}">{kit.action_span(k) if k else lab}</button>' for v, k, lab in acts)))
    rows.append(('Traits', kit.trait_dropdown(TRAITS)))
    rows.append(('Sort', kit.sort_bar(sort_keys)))
    body = ''.join(f'<div class="cr {r[2] if len(r) > 2 else ""}"><span class="cgl">{r[0]}</span><div class="cc">{r[1]}</div></div>' for r in rows)
    return (f'<details class="fbox catalog" open><summary><span>{ic("search")}Filters and sorting</span><span class="fact" id="fact"></span></summary>'
            f'<div class="controls"><div class="ctop"><label class="search">{ic("search")}<input class="cq" type="search" placeholder="Search {label}" autocomplete="off"></label>'
            f'<button class="chip fclear" type="button">Clear all filters</button></div>{body}</div></details><p class="muted small" id="cat-count"></p>')


ITEM_SORT = [('num:planlvl', 'Planned level'), ('num:lvl', 'Item level'), ('grade:g:0', 'Grade'), ('str:name', 'Name'), ('str:cat', 'Category')] + \
    [(f'rating:r:{i}', f'{lab} rating') for i, (k, lab) in enumerate(ITEM_ROLES)]


# ───────────────────────── Items ─────────────────────────
PLAN = [
    ('3', '+1 weapon potency (from 2)', f'{J("Ancestral Geometry")}, {J("Clay Sphere")} on Aspera, Lattice Armor', f'{J("Devilwing Badge")}, {J("Rime Crystal")}, {J("Flaming Star")} or {J("Jolt Coil")} in place of Clay Sphere; {J("Mage\'s Hat")}; {J("Pendant of the Occult")} for Guidance at will; a light hammer as a thrown backup', ''),
    ('4', 'Striking', f'{J("Healer\'s Gloves")}, a {J("Potion Patch", "it")} loaded with a healing potion', f'{J("Lifting Belt")} or {J("Mage\'s Hat")} as the early skill item; {J("Ghost Touch")} if incorporeal enemies appear', ''),
    ('5', '+1 armour potency; ' + J('Fearsome') + ' in Aspera\'s only property slot', f'{J("Shawl of Seasons")} set to spring for 40-foot Speed in Arcane Cascade', f'{J("Hooked")} in place of Fearsome; {J("Mobile")} in the armour; {J("Diplomat\'s Badge")}; {J("Pristine Epaulets")}; {J("Convincing")} or {J("Cunning")} if social scenes or Recall Knowledge matter more than the planned runes', ''),
    ('6', '', f'{J("Endless Grimoire")}, greater {J("Clay Sphere")} for a daily Enlarge', f'{J("Tactician\'s Helm")} once Reactive Strike is in use; {J("Choker of Elocution")}; standard {J("Phantasmal Doorknob")}', '+1 rank-1 preparation'),
    ('7', J('Sunweave') + ' in the armour\'s only slot', f'{J("Ring of Wizardry")} (Type I), {J("Retrieval Belt")}, {J("Kindler Cameo")}', f'{J("Cloak of Illusions")} for a daily Invisibility until 10, or {J("Cloak of Social Graces")} for Diplomacy and a daily Heroism; {J("Red Thread Knot")}; {J("Rooting")}; {J("Warding Statuette")}', '+2 rank-1 slots'),
    ('8', 'Resilient; ' + J('Astral') + ' takes Aspera\'s only slot and Fearsome moves to a runestone', 'Aspera\'s stave with Fused Staff', f'{J("Frost")}, {J("Corrosive")}, {J("Flaming")} or {J("Shock")} in place of Astral if spirits are rare', ''),
    ('9', '', f'Greater {J("Retrieval Belt")} for three stored items, greater {J("Healer\'s Gloves")}', f'{J("Thunderblast Slippers")}, since the footwear slot is free until 13; {J("Vigilant Eye")} against invisible enemies; {J("Armbands of Athleticism")}; {J("Messenger\'s Ring")}; greater {J("Pendant of the Occult")} if Occultism reaches expert; {J("Humbug Pocket")} or {J("Thousand-Blade Thesis")} where they fit the campaign', ''),
    ('10', '+2 weapon potency: ' + J('Fearsome') + ' returns in the second slot', f'Greater {J("Phantasmal Doorknob")} on Aspera, greater {J("Endless Grimoire")}, {J("Ring of Wizardry")} Type II', f'{J("Ashen")} in place of Fearsome; Clay Sphere moved to the armour if its daily Enlarge is worth more than an armour talisman such as the Mortalis Coin; {J("Sash of Prowess")} in place of the armbands; {J("Open Mind")} for a Hypercognition once an hour; {J("Echo Receptors")} if darkness and invisibility keep costing turns; {J("Winged Sandals")} for a vertical mission', 'Rank-3 preparation; ring adds two rank-2 slots and one rank-1'),
    ('11', '+2 armour potency (second slot), greater ' + J('Sunweave'), f'{J("Master Magus Ring")}, greater {J("Obsidian Goggles")}', f'Greater {J("Brooch of Inspiration")} if Academia and Warfare Lore come up often; {J("Accolade Robe")} was considered and passed over', ''),
    ('12', 'Greater striking, ' + J('Fortification') + ' in the second armour slot, greater ' + J('Fearsome'), f'{J("Ring of Wizardry")} Type III', 'The moderate <a href="#" data-to="it-dread-lesser">Dread</a> rune in place of Fortification if the party keeps enemies frightened', 'Ring adds two rank-3 slots and one rank-2'),
    ('13–14', 'Greater resilient at 14', f'{J("Ring of Wizardry")} Type IV and major {J("Endless Grimoire")} at 14', f'{J("Propulsive Boots")} at 13 or greater {J("Boots of Bounding")} at 14; greater {J("Cloak of Social Graces")} at 13', 'Rank-5 preparation; ring adds two rank-4 slots and one rank-3'),
    ('15–16', 'Greater ' + J('Astral') + ' at 15; +3 weapon potency at 16 with ' + J('Frost') + ' as the third rune', 'Upgrades to the runes Cyrus uses most', f'{J("Keen")} as the third rune in place of Frost; greater {J("Ashen")} at 16 if Ashen is in use', ''),
    ('17–20', '+3 armour potency and greater Fortification at 18, with ' + J('Antimagic') + ' as the third armour rune; major striking at 19, major resilient at 20', f'The apex decision: an Intelligence apex on Aspera, or {J("Bracers of Strength")}', f'{J("Spellwatch")} in place of Antimagic; high-grade {J("Djezet Armor")} at 19 or {J("Orichalcum Armor")} at 20 for a fourth armour rune; {J("Crown of Intellect")} as the published Intelligence comparison; true {J("Endless Grimoire")} at 18', 'Rank-7 preparation at 18'),
]


def items_page():
    from item_data import I
    plan = table(['Level', 'Runes', 'Core purchases', 'Alternatives and conditions', 'Spellcasting capacity'], [list(r) for r in PLAN])
    runes = table(['Item level', 'Rune', 'Effect'], [
        ['2', '+1 weapon potency', '+1 item to weapon attacks, 1 property slot'], ['4', 'Striking', '2 weapon damage dice'],
        ['5', '+1 armor potency', '+1 item AC, 1 property slot'], ['8', 'Resilient', '+1 item to saves'],
        ['10', '+2 weapon potency', '+2 item to attacks, 2 property slots'], ['11', '+2 armor potency', '+2 item AC, 2 property slots'],
        ['12', 'Greater striking', '3 weapon damage dice'], ['14', 'Greater resilient', '+2 item to saves'],
        ['16', '+3 weapon potency', '+3 item to attacks, 3 property slots'], ['18', '+3 armor potency', '+3 item AC, 3 property slots'],
        ['19', 'Major striking', '4 weapon damage dice'], ['20', 'Major resilient', '+3 item to saves']], num=(0,))
    armour = table(['Armour', 'When', 'AC', 'Dex cap', 'Strength', 'Check penalty', 'Speed penalty', 'Bulk'], [
        ['<a href="https://2e.aonprd.com/Search.aspx?q=Lattice+Armor">Lattice Armor</a>', 'Current, with Dexterity +1', '+4', '+1', '+3', '−2', '−5 ft', '2'],
        ['<a href="https://2e.aonprd.com/Search.aspx?q=Scale+Mail">Scale Mail</a>', 'If Dexterity reaches +2', '+3', '+2', '+2', '−2', '−5 ft', '2'],
        ['<a href="https://2e.aonprd.com/Search.aspx?q=Breastplate">Breastplate</a>', 'For a dragonhide suit', '+4', '+1', '+3', '−2', '−5 ft', '2']])
    groups = [('Weapon runes', 'Weapon rune', 'Aspera holds one property rune per point of potency.'),
              ('Armour runes', 'Armour rune', 'The armour holds one property rune per point of potency.'),
              ('Armour materials', 'Armour material', 'The armour can be made of one precious material. Low grade holds runes up to level 8, standard grade up to level 15 and high grade any rune.'),
              ('Spellhearts', 'Spellheart', 'Aspera and the armour each hold one spellheart or talisman.'),
              ('Worn and held items', None, 'Investment limit: 10 items.')]
    cats = ['Weapon rune', 'Armour rune', 'Armour material', 'Spellheart', 'Worn item', 'Held item']
    order = {}
    for n, d in I.items():
        order.setdefault(d['cat'], []).append(n)
    sec = []
    for title, cat, note in groups:
        names = order.get(cat, []) if cat else order.get('Worn item', []) + order.get('Held item', [])
        names = sorted(names, key=lambda n: (I[n]['plan'][0] if I[n]['plan'] else 99, n))
        sec.append(f'<section class="catgroup"><h2>{title}</h2><p class="muted">{note}</p>' + ''.join(icard(n, I[n]) for n in names) + '</section>')
    body = ''.join(sec)
    controls = catalog_controls(cats, ITEM_ROLES, ITEM_SORT)
    nav = ''.join(f'<a href="#" data-to="{a}">{b}</a>' for a, b in [('i-order', 'Purchase plan'), ('i-runes', 'Fundamental runes'), ('i-armour', 'Armour'), ('i-cat', 'Item catalogue')])
    page = f'''<div class="page doc" data-page="items">
<header class="ph"><h1>Itemisation</h1>
<p class="lede">The purchase plan by level, then every item considered for Cyrus with a grade, the level it enters the plan and an evaluation. Items in the plan are marked Core, Option or Situational.</p></header>
<nav class="jumpbar scroll">{nav}</nav>
<h2 id="i-order">Purchase plan</h2>
<p class="muted">Fundamental runes come first at each level. Core purchases are the planned items; alternatives replace or join them when the condition applies. The levels are the earliest point each purchase makes sense, not a schedule: items and merchants have to be found in play, so some will arrive later than listed or not at all, and the plan adjusts to what turns up.</p>{plan}
<h2 id="i-runes">Fundamental runes</h2><p class="muted">Standard progression. Moving a rune between items costs 10% of its price and a day.</p>{runes}
<h2 id="i-armour">Armour</h2><p class="muted">Cyrus wears Lattice Armor while his Dexterity modifier is +1. If it reaches +2, Scale Mail gives the same total AC with its higher cap filled and has a lower Strength threshold, so he will likely change to it. In either armour, meeting the Strength threshold removes both the check penalty and the Speed penalty, which matters because Speed drives Dimensional Assault. Moving the armour's runes to the new suit costs 10% of their price. A Breastplate has the same numbers as Lattice Armor, which matters only for materials that can't make chain armour. The suit can also be made of a precious material; those are graded with the item catalogue below. Ordinary armour holds any rune, but precious armour is limited by its grade: low grade holds runes only up to level 8 and standard grade only up to level 15, so a precious suit needs standard grade by 11 for +2 armour potency and high grade by 18 for +3.</p>{armour}
<h2 id="i-cat">Item catalogue</h2>
{controls}
{body}
{rules_box(1510, "Spellhearts")}
{rules_box(3138, "Investing magic items")}
</div>'''
    open('/home/claude/site/pages/items.html', 'w').write(page)


# ───────────────────────── Consumables ─────────────────────────
CONS_SORT = [('num:lvl', 'Item level'), ('grade:g:0', 'Grade'), ('str:name', 'Name'), ('str:cat', 'Category')] + \
    [(f'rating:r:{i}', f'{lab} rating') for i, (k, lab) in enumerate(ITEM_ROLES)]


def consumables_page():
    from item_data import C
    global TRAITS
    TRAITS = Counter()
    kit_tbl = table(['Carry', 'Item', 'Why'], [
        ['Always', f'{J("Healing Potion")} in a {J("Potion Patch")}', 'The emergency heal that keeps both hands on Aspera. One patch works at a time and lapses at daily preparations.'],
        ['Always', f'{J("Mortalis Coin")} on the armour', 'Free insurance against the critical hit that would leave him dying 2.'],
        ['Always', J("Cat's Eye Elixir"), 'Concealment and invisibility would otherwise waste a Spellstrike.'],
        ['Always', J('Transmuting Ingot') + ' for silver and cold iron', 'A known material weakness becomes extra damage on every hit.'],
        ['Planned fight', f'{J("Potion of Quickness")} in a patch, {J("Numbing Tonic")} or {J("Mistform Elixir")}', 'Drunk before initiative or in the patch for one action.'],
        ['Known terrain', f'{J("Emerald Grasshopper")}', 'A gap, ledge or rooftop route with both hands on Aspera.'],
        ['Known enemy', f'{J("Ghostbane Fulu")}, {J("Escape Fulu")}, {J("Salve of Mental Pattern")}, {J("Oil of Revelation")}', 'Ghosts before Astral, grapplers, mental damage, invisible enemies.'],
        ['Boss fight', f'{J("Dazing Coil")} or {J("Grinning Pugwampi")} swapped onto Aspera, {J("Reactive Flash")}', 'Worth the 10-minute swap off the Doorknob when the fight is planned.'],
        ['Negotiation', J('Heartening Missive (Butterfly)'), 'One important Diplomacy check by a known recipient.'],
    ])
    hands = table(['Starting from', 'Sequence', 'Cost'], [
        ['Aspera in two hands, item worn', 'Release (free), draw (1), use (usually 1), regrip (1)', '3 actions'],
        ['Item in a Retrieval Belt or Prism', 'Release (free), retrieve (free), use (1), regrip (1)', '2 actions'],
        ['Potion loaded in a Potion Patch', 'Activate the patch (1)', '1 action, both hands stay on Aspera'],
    ])
    cats = ['Healing and defence', 'Access and hands', 'Weapon treatments', 'Movement', 'Mission supplies', 'Offense']
    by = {}
    for n, d in C.items():
        by.setdefault(d['cat'], []).append(n)
    body = ''.join(f'<section class="catgroup"><h2>{c}</h2>' + ''.join(icard(n, C[n]) for n in by.get(c, [])) + '</section>' for c in cats)
    controls = catalog_controls(cats, ITEM_ROLES, CONS_SORT, invest=False, plan=False, label='consumables')
    page = f'''<div class="page doc" data-page="consumables">
<header class="ph"><h1>Consumables</h1>
<p class="lede">Aspera is held in two hands, so how an item reaches Cyrus's hand matters as much as what it does. The aim is one emergency answer ready, one way to reach the fight, and a few answers to the encounter he expects.</p></header>
<nav class="jumpbar scroll"><a href="#" data-to="c-kit">What to carry</a><a href="#" data-to="c-slots">Attachment slots</a><a href="#" data-to="c-handseq">Hands</a><a href="#" data-to="c-cat">Catalogue</a></nav>
<h2 id="c-kit">What to carry</h2>{kit_tbl}
<h2 id="c-slots">Attachment slots</h2><p class="prose">Aspera and the armour can each hold one talisman or one spellheart, not both. Aspera carries a spellheart from level 3, so a weapon talisman means removing the spellheart with a 10-minute Affix before the fight, which is only worth it for a planned boss. The armour's slot is where Cyrus's best talismans go, the Mortalis Coin, Emerald Grasshopper or Retrieval Prism, so it should stay free for them unless a spellheart there is worth more. Whetstones and oils don't use either slot.</p>
<h2 id="c-handseq">Hands, drawing and the grip</h2><p class="muted">Removing a hand is free. Drawing and regripping are Interact actions.</p>{hands}
{rules_box(2150, "Drawing and stowing items")}
<h2 id="c-cat">Catalogue</h2>
{controls}
{body}
{rules_box(3203, "Talismans")}
</div>'''
    open('/home/claude/site/pages/consumables.html', 'w').write(page)


# ───────────────────────── Aspera ─────────────────────────
STAVE = [
    ('Level 8', 'Cantrip', ['Time Sense', 'Figment'], 'Cantrips cost no charges, so Figment never needs one of his prepared cantrips.'),
    ('Level 8', 'Rank 1', ['Sure Strike', 'Befuddle', 'Illusory Object'], 'Sure Strike from charges is the main reason to fuse the stave.'),
    ('Level 8', 'Rank 2', ["Loose Time's Arrow", 'Invisibility', 'Embed Message'], 'Party opener, scouting and messages.'),
    ('Level 8', 'Rank 3', ['Time Jump', 'Slow', 'Illusory Disguise'], 'One-action repositioning, Fortitude control, and a disguise that can copy a specific person.'),
    ('Level 10', 'Rank 4', ['Wall of Mirrors', 'Vision of Death'], 'A wall and a Will attack.'),
    ('Level 12', 'Rank 5', ['Space Fold Gate', 'Synesthesia'], 'Synesthesia is occult and castable from the stave once he has the dedication at 9.'),
    ('Level 14', 'Rank 6', ['Cast into Time', 'Mislead'], 'Temporal damage and a decoy.'),
    ('Level 16', 'Rank 4', ['Clairvoyance'], 'Scouting before a fight.'),
    ('Level 16', 'Rank 7', ['Haste', 'True Target'], 'Haste at rank 7 targets six creatures, which covers the whole party for 7 charges.'),
]
GIFTS = [('Repository of Knowledge', 'First minor gift', 'Mind'), ('Sands of the Hourglass', 'Second minor gift, relic level 5+', 'Time'),
         ('Precognition', 'First major gift, 9+', 'Time'), ('Temporal Pulse', 'Second major gift, 13+', 'Time'),
        ]
# Aspera's custom fifth gift and the abilities that come with it at relic level 17
CUSTOM_GIFTS = [
    ('Unrestricted Quickening', 'Grand gift, 17+', 'Time', [], None,
     "<p>While you're wielding the relic, you can use the extra action from the quickened condition for any action, or as part of any activity, regardless of the restrictions of the effect that made you quickened.</p>"
     "<p><strong>Quick Start</strong> When you roll initiative, you become quickened until the end of your first turn.</p>",
     "From level 14, Hasted Assault quickens Cyrus for a minute in most fights, and Haste, Loose Time's Arrow and Temporal Pulse quicken him too. With this gift every quickened turn is a full four actions: a 2-action spell and a Spellstrike, Spellstrike with Recharge Spellstrike and Arcane Cascade, or a 3-action activity and a Step. Quick Start covers the first round, before Hasted Assault takes effect, so the gift works from the opening turn of every fight. Quickened from several sources still gives only one extra action."),
    ('Unravelling Strike', 'Relic ability, 17+', 'Mind', ['Concentrate'], 'free',
     "<p><strong>Frequency</strong> once per hour; <strong>Trigger</strong> You hit a creature with a Strike using the relic, including a Strike made as part of Spellstrike.</p>"
     "<p><strong>Effect</strong> The relic attempts to counteract one spell or magical effect on the target, chosen by you. If you don't know what effects are on the target, the relic attempts to counteract the effect with the highest rank.</p>",
     "A free dispel on a hit, once a fight. It removes a boss's protective spell, haste, flight or invisibility without costing an action. It uses Cyrus's counteract modifier and a counteract rank of half the relic's level, 9 at level 17. None of Aspera's other gifts or stave spells deal with an enemy's own magic."),
    ('Arcane Persuasion', 'Relic ability, 17+', 'Mind', [], None,
     "<p>While the relic is on your person, you gain a +2 item bonus to Arcana and Society checks. When you interact with spellcasters or creatures with magical traits, or the subject is magic, you can use Arcana in place of Diplomacy to Make an Impression or Request, and in place of Deception to Lie.</p>",
     "Cyrus's Charisma is low, but his Arcana is legendary from 15. This lets that expertise carry conversations with the Conclave, the Spellguard, Blackstaff scholars, rival casters and magical creatures. The item bonus helps him identify magic and work through wards and old writing. A +3 Arcana or Society item would replace the bonus, but not the skill substitution."),
]
GIFT_NOTES = {
    'Repository of Knowledge': "The weakest of Aspera's gifts in combat, but a good first gift for this character. Three extra Lores that rise to expert and master with the relic give Magus's Analysis and his Recall Knowledge more subjects to draw on, and the choice of Lores is a way to tie Aspera's history into the campaign. Choose subjects that the party doesn't already cover rather than ones that overlap Warfare Lore.",
    'Sands of the Hourglass': "A strong debuff that works even on a successful save: clumsy 1 and enfeebled 1 for a minute, rising to clumsy 2, enfeebled 2 and drained on a failure. Clumsy lowers the target's AC and Reflex DC, which helps every Spellstrike with a Reflex spell and every Trip, and enfeebled weakens a brute's attacks on the front line. It costs two actions and has a 30-foot range, so it is best used on the opening turn against the most dangerous enemy, before Cyrus closes in. The once-per-hour limit means once per fight in practice.",
    'Precognition': "Precognition lets Cyrus play a turn twice and keep the better result, once a day. That is the strongest possible protection for a decisive turn: a Sprinting Spellstrike with a high-rank line spell, a Trip setup against a boss, or a turn where a critical failure would waste his best slot. It costs no actions, so the only question is which turn to save it for. With one or two fights a day, it should be spent in the first fight that matters.",
    'Temporal Pulse': "A once-a-day action that can slow every chosen enemy within 30 feet and quicken an ally for each enemy it slows. Against a group it can be the most valuable action anyone in the party takes that day, and it is still useful against a single boss. Because it targets Will, it is weakest against strong-willed casters. It has a 30-foot radius, so Cyrus needs to be in the middle of the fight to use it well, which suits his position at reach.",
    '_unused_time_jump': "A third Time gift in place of the grand gift. The relic casts Time Jump once a day: for one action Cyrus takes two move actions while time is paused, so nothing can react to his movement. That is effectively a free extra Stride and Stride on the turn he needs to cross the battlefield, followed by two actions for a Spellstrike, and it costs no Focus Point. It is less dramatic than Time Reversal, but it is useful in nearly every fight, whereas Time Reversal only matters once a fight has already gone badly.",
}


def gift_card(n, tier, aspect):
    e = entry(n, 'relic', foundry_kind='any')
    return kit.rules_card(e, 'gift-' + slug(n), kicker=f'{aspect} · {tier}', evaluation=GIFT_NOTES.get(n, ''), show_trad=False)


def custom_gift_card(n, tier, aspect, tr, act, body, ev):
    e = {'name': n, 'url': '#aspera', 'traits': [(t, 'https://2e.aonprd.com/Traits.aspx?Name=' + t) for t in tr], 'fields': [], 'body': body, 'book': 'Aspera, custom', 'action': {'free': 'free'}.get(act), 'kind': 'item', 'remaster': True}
    return kit.rules_card(e, 'gift-' + slug(n), kicker=f'{aspect} · {tier}', evaluation=ev, show_trad=False)


def weapon_row(n):
    import rules
    d = rules.get(n, 'item')
    s = d['system']
    dmg = s.get('damage', {})
    traits = ', '.join(t.replace('-', ' ').replace('deadly d', 'deadly d').title() for t in s['traits']['value'])
    return [f'<a href="https://2e.aonprd.com/Search.aspx?q={n}">{n}</a>', f'{dmg.get("dice", 1)}{dmg.get("die")} {dmg.get("damageType", "")}', traits, str(s.get('bulk', {}).get('value', ''))]


def aspera_page():
    comp = table(['Weapon', 'Damage', 'Traits', 'Bulk'], [
        ['<b>Aspera</b>', '1d8 slashing', 'Reach, Trip, Deadly d10', '2'],
        weapon_row('Fauchard'), weapon_row('Glaive'), weapon_row('Guisarme')])
    stave = table(['Stage', 'Rank', 'Spells', 'Role'],
                  [[a, b, ', '.join(f'<a href="#spells" class="xs">{H.escape(x)}</a>' for x in c), d] for a, b, c, d in STAVE])
    gifts = ''.join(gift_card(*g) for g in GIFTS) + ''.join(custom_gift_card(*g) for g in CUSTOM_GIFTS)
    rune_names = sorted([n for n, d in I.items() if d['cat'] == 'Weapon rune'], key=lambda n: ('SABCD'.index(I[n]['g']), I[n]['plan'][0] if I[n]['plan'] else 99, n))
    runes = table(['Rune', 'Grade', 'Plan', 'Summary'], [[J(n), grade(I[n]['g']), (f'{I[n]["plan"][1]} at {I[n]["plan"][0]}' if I[n]['plan'] else '—'),
                   H.escape(I[n]['ev'].split('. ')[0].rstrip('.') + '.')] for n in rune_names])
    gifttbl = table(['Gift', 'Relic level', 'Tier', 'Aspect', 'Choice'], [['1', '1', 'Minor', 'Mind', J('Repository of Knowledge', 'gift')], ['2', '5', 'Minor', 'Time', J('Sands of the Hourglass', 'gift')], ['3', '9', 'Major', 'Time', J('Precognition', 'gift')], ['4', '13', 'Major', 'Time', J('Temporal Pulse', 'gift')], ['5', '17', 'Grand', 'Time', J('Unrestricted Quickening', 'gift')], ['', '17', 'Relic ability', 'Mind', J('Unravelling Strike', 'gift')], ['', '17', 'Relic ability', 'Mind', J('Arcane Persuasion', 'gift')]], num=(0, 1))
    nav = ''.join(f'<a href="#" data-to="{a}">{b}</a>' for a, b in [('a-weapon', 'The weapon'), ('a-relic', 'Relic growth'), ('a-stave', 'The fused stave'), ('a-runes', 'Runes')])
    page = f'''<div class="page doc" data-page="aspera">
<header class="ph"><h1>Aspera</h1>
<p class="lede">Cyrus's relic polearm: its weapon profile, relic gifts, fused stave and property runes.</p>
<p class="muted small">{ic("relic")} Approved by Alex and gained at level 3.</p></header>
<nav class="jumpbar scroll">{nav}</nav>
<h2 id="a-weapon">The weapon</h2>
<div class="grid2">
<div class="panel"><h3>{ic("aspera")}Profile</h3><dl class="st">
<dt>Category</dt><dd>Martial melee weapon</dd><dt>Group</dt><dd>Polearm</dd><dt>Hands</dt><dd>2</dd><dt>Damage</dt><dd>1d8 slashing</dd><dt>Traits</dt><dd>Reach, Trip, Deadly d10</dd><dt>Bulk</dt><dd>2</dd>
<dt>Reach</dt><dd>10 feet, including two squares diagonally</dd></dl></div>
<div class="panel"><h3>{ic("shadowgrasp")}Shadow Synthesis</h3><p>Aspera's Shadow Synthesis ability lets it benefit from Laughing Shadow's off-guard damage boost while held in both hands, as if its wielder had a hand free.</p></div></div>
<p class="muted">Published comparisons. Aspera matches the fauchard's shape, trading sweep for a bigger deadly die.</p>{comp}
<h2 id="a-relic">Relic growth</h2>
<p class="prose">Aspera's aspects are Time and Mind. Gifts arrive as the relic grows, and gift saves use the better of Cyrus's class DC and spell DC. The fifth gift is a custom grand gift, Unrestricted Quickening, which comes with Quick Start. Unravelling Strike and Arcane Persuasion arrive with it at relic level 17.</p>
{gifttbl}
{rules_box(3256, "Relic gifts")}
{gifts}
<h2 id="a-stave">The fused stave</h2>
<p class="prose">With <a href="#feats">Fused Staff</a> at 8, the stave's spells are cast from Aspera itself. Cyrus prepares it each day for charges equal to his highest slot rank, and can spend a slot to add that slot's rank in charges. With one or two fights a day, the charges cover both fights. The spell list below is the bespoke plan, built around time, the mind and illusion. Each spell is cast at the rank listed and costs that many charges, so Haste and Illusory Disguise are their heightened versions.</p>
{stave}
{rules_box(3211, "Staves")}
<h2 id="a-runes">Property runes</h2>
<p class="muted">Full rules text and evaluations are in the item catalogue on the Itemisation page.</p>
{runes}
</div>'''
    open('/home/claude/site/pages/aspera.html', 'w').write(page)


if __name__ == '__main__':
    items_page(); consumables_page(); aspera_page(); print('ok')
