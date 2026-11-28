"""Combat flow and teamwork page."""
import html as H
import kit
from kit import ic, grade, slug, action_span
from entries import entry
from build_items import rules_box, table
from feat_evals import CLASS_ROLES
from build_feats import rate
from grid import Grid, fig, COL, space, flank_squares, in_reach10, ft
from build_atlas import key, sprint_fig, TOKENS


# ───────────── diagrams ─────────────
def diagrams():
    # 1. Reach: Cyrus two squares from a 5-foot enemy
    g1 = Grid(7, 7, "Aspera's reach")
    g1.shade({(x, y) for x in range(7) for y in range(7) if max(abs(x - 2), abs(y - 3)) <= 2 and (x, y) != (2, 3)}, COL['reach'])
    g1.box(3, 2, 3, 3, COL['E']).token(2, 3, 'C').token(4, 3, 'E')
    # 2. Dimensional Assault landing squares
    cx, cy, tx, ty, ax = 2, 3, 7, 3, 8
    tsp = space(tx, ty)
    fl = flank_squares(tsp, (ax, ty), (0, 0, 11, 7), blocked={(cx, cy)})
    g2 = Grid(11, 7, 'Dimensional Assault')
    rng = {(x, y) for x in range(11) for y in range(7) if ft(x - cx, y - cy) <= 20 and (x, y) != (cx, cy)}
    g2.shade(rng, COL['range'])
    land = {p for p in rng if in_reach10(p, tsp) and p not in tsp and p != (ax, ty)}
    g2.shade(land, COL['reach']).shade(land & set(fl), COL['flank'])
    best = (5, 3)
    g2.arrow(cx + .5, cy + .5, best[0] + .25, best[1] + .5, dash=True)
    g2.target(tx, ty).token(ax, ty, 'A').token(cx, cy, 'C')
    return figs_html([
        fig(g1, "Aspera's reach", "Blue squares are within 10 feet, including two squares diagonally. The dashed outline is a 5-foot enemy's reach: from two squares away Cyrus can hit it, and it has to move to hit him."),
        fig(g2, 'Dimensional Assault', "Lighter squares are within range, shown as 20 feet. Blue squares are within reach of the target; green squares are within reach and flank with the ally."),
    ], 2) + figs_html([sprint_fig()], 1)


def figs_html(items, cols):
    return f'<div class="figs c{cols}">{"".join(items)}</div>'


# ───────────── turn patterns ─────────────
def step(kind, name, tag=''):
    g = {'1': action_span('one'), '2': action_span('two'), 'f': action_span('free'), 'r': action_span('reaction'), 'q': '<span class="pf q">1</span>'}[kind]
    t = f'<span class="mp">{tag}</span>' if tag else ''
    return f'<span class="stp k{kind}">{g}<span class="sn">{name}</span>{t}</span>'


SITUATIONS = [
    ('t-ready', 'Enemy in reach, Spellstrike charged', [
        ('Spellstrike, then Analysis', 1, [('2', 'Spellstrike', 'MAP 0'), ('1', "Magus's Analysis", 'recharges')],
         "The default against a creature he hasn't analysed today. Analysis gets +1 to the Recall Knowledge check if the Strike hit, and it recharges Spellstrike for next turn."),
        ('Spellstrike, then Force Fang', 2, [('2', 'Spellstrike', 'MAP 0'), ('1', 'Force Fang', 'recharges')],
         "For a creature already analysed today. Force Fang can't miss and recharges Spellstrike. It has the manipulate trait, so use it from outside the enemy's reach."),
        ('Improvise Strategy, then Spellstrike', 7, [('1', 'Improvise Strategy'), ('2', 'Spellstrike', 'MAP 0')],
         "When the target isn't flanked or prone. Improvise Strategy has no attack trait, so the Spellstrike keeps full accuracy against an off-guard target. Once per enemy per fight."),
        ('Spellstrike into Dimensional Disappearance', 10, [('2', 'Spellstrike', 'MAP 0'), ('1', 'Dimensional Assault', 'no Strike')],
         "With Dimensional Disappearance, skip the Strike: Cyrus teleports out of reach, turns invisible and ends the turn recharged. Use it when staying in place would cost more than the next Spellstrike gains."),
    ]),
    ('t-spent', 'Enemy in reach, Spellstrike spent', [
        ('Analysis, then Spellstrike', 1, [('1', "Magus's Analysis", 'recharges'), ('2', 'Spellstrike', 'MAP 0')],
         "Against a new creature, Analysis is a recharge with a Recall Knowledge check attached, so it is always better than the plain Recharge action."),
        ('Recharge, then Spellstrike', 1, [('1', 'Recharge Spellstrike'), ('2', 'Spellstrike', 'MAP 0')],
         "Only once Analysis has been used on this creature today and no Focus Point is worth spending. It costs the whole turn, so it only works when he doesn't need to move."),
        ('Off-Spellstrike', 7, [('1', 'Improvise Strategy'), ('1', 'Trip', 'MAP 0'), ('1', 'Dimensional Assault', 'Strike at MAP −5')],
         "Clumsy 1 from Improvise Strategy lowers the target's Reflex DC for the Trip. Dimensional Assault then moves Cyrus to the best flanking square, Strikes the prone target and recharges Spellstrike, so the next turn opens with a full-accuracy Spellstrike."),
        ('Running Recharge, then Spellstrike', 4, [('1', 'Running Recharge', 'recharges'), ('2', 'Spellstrike', 'MAP 0')],
         "Running Recharge recharges Spellstrike and moves him up to half his Speed, or a Step, in one action, so he can reach a flanking square and Spellstrike without spending a Focus Point. Use it once Analysis has been spent on this creature and he needs to move; if the target is already in reach and flanked, Force Fang adds damage for the same action."),
    ]),
    ('t-far', 'No enemy in reach', [
        ('Stride, then Spellstrike', 1, [('1', 'Stride'), ('2', 'Spellstrike', 'MAP 0')],
         "The plain approach when Spellstrike is charged and an enemy is within one Stride. End on a square two away from the target, opposite an ally."),
        ('Spellcasting into Dimensional Strike/Disappearance', 1, [('2', 'Spell without an attack roll'), ('1', 'Dimensional Assault', 'either order')],
         "When Spellstrike is spent and the target is beyond one Stride. Before level 10, take Dimensional Assault first so its Strike is at full accuracy, then cast a spell that doesn't need an attack roll, such as Slow, Fear or a buff. From 10, Dimensional Disappearance lets him skip the Strike, so the order is free: cast first and teleport out invisible, or teleport in and cast. Either way the turn ends with Spellstrike recharged."),
        ('Sprinting Spellstrike into Analysis or Disappearance', 12, [('2', 'Sprinting Spellstrike', 'line spell'), ('1', "Analysis or Dimensional Assault", 'recharges')],
         "His defining high-level turn. He moves up to the line's length through enemies without triggering reactions, Spellstrikes, and with Expansive Spellstrike the line follows his path, so every creature he passes through is in the area as well as the target. The last action is Analysis against a new creature, or Dimensional Assault without the Strike to teleport out invisible and recharged when ending the turn in the middle of a group would be dangerous."),
        ('Closing into enemies', 1, [('1', 'Stride'), ('1', 'Stride'), ('1', 'Recharge or Step')],
         "When nothing is in range of even Dimensional Assault. End two squares from where the enemy will be, so it has to come to him and provoke Reactive Strike."),
    ]),
    ('t-cast', 'Turns without Spellstrike', [
        ('Mid-level opening', 7, [('2', 'Blur or Haste', 'studious'), ('f', 'Arcane Cascade'), ('1', 'Stride')],
         "Casting a studious spell lets him enter Arcane Cascade for free. Blur from 7, Haste from 11. The buff costs no tempo because the stance would have cost an action anyway."),
        ('Off-Spellstrike Spellcasting', 1, [('1', "Magus's Analysis", 'recharges'), ('2', 'Area, control or buff spell')],
         "For turns where a spell does more cast normally: enemies grouped away from his reach, any Expansive placement catching an ally, Slow on a boss, or Haste on an ally. Analysis first in most cases, because it recharges Spellstrike and tells him which save to target before he picks the spell. Stride first instead when he needs range or line of effect, or Stride after to reposition once the spell is cast."),
    ]),
    ('t-late', 'Higher-level turns', [
        ('Hasted Assault Setup', 14, [('1', 'Hasted Assault', 'recharges'), ('2', 'Spellstrike', 'MAP 0')],
         "Quickened for a minute for Stride or Strike, and it recharges Spellstrike. Every later turn has a free Stride to a flanking square. Cast it before closing in, because it has the manipulate trait."),
        ('Living Thunderbolt Setup', 12, [('2', 'Living Thunderbolt'), ('1', 'Stride')],
         "Living Thunderbolt the turn before a Sprinting Spellstrike lets him fly the path, and every creature he passes through also takes its electricity damage."),
        ('Quickened Spellstrike', 5, [('q', 'Stride', 'quickened'), ('2', 'Spellstrike', 'MAP 0'), ('1', 'Analysis or Arcane Cascade')],
         "With Haste or Hasted Assault, the extra action moves him to the flanking square, so he can Spellstrike and still use his last action. That is Analysis against a new creature, or from 16 re-entering Arcane Cascade to refresh Arcane Shroud: with Invisibility, attacks against him need a DC 11 flat check until his next hostile action. Open the following turn with the plain Recharge, which isn't hostile, so the next Spellstrike is made while hidden against an off-guard target."),
        ('Quickened Off-Spellstrike', 7, [('q', 'Stride', 'quickened'), ('1', 'Improvise Strategy'), ('1', 'Trip', 'MAP 0'), ('1', 'Dimensional Assault', 'Strike at MAP −5')],
         "The Off-Spellstrike turn with the quickened Stride used to close distance first, so it works even when the target starts out of reach."),
    ]),
]


def turns():
    out = []
    for sid, head, pats in SITUATIONS:
        cards = ''.join(
            f'<article class="turn"><header><h4>{H.escape(n)}</h4><span class="lvl">Level {lvl}+</span></header>'
            f'<div class="steps">{"".join(step(*s) for s in st)}</div><p>{txt}</p></article>' for n, lvl, st, txt in pats)
        out.append(f'<h3 class="ah" id="{sid}">{head}</h3><div class="turns">{cards}</div>')
    return ''.join(out)


# ───────────── action cards ─────────────
A = {
    'Trip': ('324302', 'S', "Trip is Cyrus's main setup action. Aspera's trip trait means he can use it with both hands on the weapon, and at 10 feet of reach he can trip an enemy that cannot reach him. A prone target is off-guard, which turns on Laughing Shadow's extra damage and helps every melee ally, takes a –2 penalty to its own attacks, and has to spend an action to Stand, which provokes Reactive Strike from level 6. Its cost is the multiple attack penalty: a Spellstrike after a Trip is at −5. It also stops working on creatures more than one size larger until Titan Wrestler at 12. With master Athletics from level 7, it should succeed often enough to plan turns around."),
    'Recall Knowledge': ('100003', 'B', "Recall Knowledge itself is rarely worth an action in combat, because Magus's Analysis does the same thing and recharges Spellstrike. It matters for its rules: Analysis uses it, so Cyrus's Arcana, Society and Lore proficiencies decide how often Analysis tells him something useful. The plain action is worth using on a second enemy he has already analysed today, or out of combat."),
    'Step': ('101231', 'B', "Step moves only 5 feet but never triggers reactions. With 10 feet of reach, a single Step usually turns an adjacent enemy into one he can hit but that cannot hit back, or moves him from a non-flanking square onto one. It is the safest use of a spare third action when nothing better is available."),
    'Reactive Strike': ('442201', 'A', "Reactive Strike is what makes Aspera's reach a threat on the enemy's turn as well as Cyrus's own. With 10 feet of reach it covers every square within two of him, it ignores the multiple attack penalty, and it punishes the actions enemies most want to take against a reach fighter: Stepping in, Standing up after a Trip, and casting with manipulate actions. It competes with a Shield Block for his one reaction, and enemies with their own reach or ranged attacks can avoid it, but in most fights it adds a free Strike every round or two."),
    'Escape': ('100320', 'C', "Escape has the attack trait, so it counts toward the multiple attack penalty, and it needs a good roll against the grabbing creature's DC. Cyrus can use Athletics, which he raises anyway for Trip, so his odds are reasonable. Spells such as Living Thunderbolt and Unfettered Movement make him much harder to hold later on. Keep Escape as the fallback when he is grabbed before those are available."),
    'Grapple': ('103101', 'C', "Grapple needs a free hand, so Cyrus has to let go of Aspera and spend an Interact action to regrip afterwards, and while one hand is off the weapon he cannot Strike with it. Grabbed and restrained are strong conditions, but a party member with a free hand is better placed to impose them. Grapple is for unusual moments, such as stopping a fleeing caster when Trip has failed."),
    'Shove': ('102111', 'C', "Shove also needs a free hand, which costs Cyrus his grip on Aspera. Pushing an enemy away is less useful for a reach fighter, who would rather have it 10 feet away than 15. It has value for pushing a creature off a ledge or out of a doorway, but it is a situational choice."),
    'Reposition': ('102112', 'C', "Reposition needs a free hand unless Cyrus is grabbing the target. It can move an enemy into a flanking line or away from an ally, but the hand cost and the multiple attack penalty make it a niche option. Choose Trip unless moving the creature is the point."),
    'Disarm': ('101101', 'D', "Disarm needs a free hand, and even a success only weakens the target's grip. Against weapon users that rely on one item it can matter, but Trip gives a more reliable benefit for the same action and multiple attack penalty."),
    'Interact': ('100002', 'B', "Interact is how Cyrus regrips Aspera after letting go with one hand, draws a potion or a scroll, or retrieves an item. Releasing a hand is free, but taking it back costs this action, which is the real price of using consumables, Grapple or Shove mid-fight. Fused Staff at 8 removes much of this cost for spells, because the stave's spells are cast through Aspera."),
    'Refocus': ('300003', 'A', "With one or two fights a day and rests between them, Refocus nearly always restores Cyrus's Focus Points before the next fight. That makes Dimensional Assault and Force Fang reliable once-or-twice-per-fight tools rather than resources to hoard, and it is why the turn patterns spend Focus Points freely."),
}


def action_cards():
    out = []
    for n, (r, g, ev) in A.items():
        e = dict(entry(n, 'action'), kind='action')
        acc = f'<div class="acc"><div class="ag">{ic("crown")}<span>Use for Cyrus</span>{grade(g)}</div></div>'
        kick = 'Athletics' if n in ('Trip', 'Grapple', 'Shove', 'Reposition', 'Disarm') else 'Magus feat 6' if n == 'Reactive Strike' else 'Basic action'
        out.append(kit.rules_card(e, 'ac-' + slug(n), kicker=kick,
                                  evaluation=ev, ratings_html=rate(r, CLASS_ROLES), access_html=acc, show_trad=False))
    return ''.join(out)


def defence_table():
    from picks import P
    notes = {
        'AC': 'The Strike roll decides the spell, so a miss loses both. Use them against an off-guard target or when AC is the weak defence.',
        'Reflex': 'Most of his area damage, so it is the widest choice for Expansive Spellstrike.',
        'Fortitude': 'Often the lowest save of spellcasters and agile creatures.',
        'Will': 'Often the lowest save of brutes and animals. Mindless creatures are immune to mental effects, which covers most Will spells.',
    }
    rows = []
    for d in ('AC', 'Reflex', 'Fortitude', 'Will'):
        names = []
        for r in range(0, 10):
            for n in P[r]['saves'].get(d, [])[:2]:
                if ' (' not in n and n not in names:
                    names.append(n)
        rows.append([d, ', '.join(names), notes[d]])
    return table(['Weak defence', 'Spells by rank, lowest first', 'Notes'], rows)


PARTY = [
    ('Mira', 'Champion', 'Divine (focus spells)', "Her champion's reaction covers allies within 15 feet, so end turns inside that distance and flank with her from 10 feet."),
    ('Cassius', 'Fighter', 'None', "Trip, flank or frighten the enemy he is fighting. A tripped enemy that Stands provokes his Reactive Strike."),
    ('Yara', 'Cleric', 'Divine', "Carry emergency healing so hers is not the only source. Agree who prepares Dispel Magic and Fly."),
    ('Theldren', 'Druid', 'Primal', "Haste, Slow, Fireball, Fly and Dispel Magic are on both lists, so agree who prepares each. Say where Cyrus will end his turn before an area spell goes down."),
    ('Adrian', 'Animist', 'Divine', "His apparitions change from day to day, so ask which defence his spells target that day."),
]


LEVELS = [
    ('1 to 4', "One Spellstrike, then a recharge. Magus's Analysis recharges once per creature each day, Dimensional Assault and Force Fang recharge for a Focus Point each, and Arcane Cascade costs an action in the first round.",
     "Cantrips are the usual spell in a Spellstrike, with Gouging Claw first. Both rank-1 slots go to Sure Strike. Expansive Spellstrike and Running Recharge arrive at 4, with two rank-2 slots."),
    ('5 to 8', "Haste and Slow at 5. Reactive Strike at 6 makes his reach a threat off-turn. Improvise Strategy at 7 gives off-guard without an attack, studious spells give a free Arcane Cascade, and master Athletics makes Trip reliable.",
     "Slotted spells start to cover each save. A Ring of Wizardry adds rank-1 slots at 7 and Aspera's stave adds charges at 8, so Sure Strike no longer competes with attack spells for slots."),
    ('9 to 12', "Dimensional Assault reaches his full Speed at 9. Dimensional Disappearance at 10 makes each teleport an escape or an attack from hiding. Sprinting Spellstrike at 12 turns line spells into movement and area damage.",
     "The Witch Dedication at 9 opens occult scrolls, wands and Synesthesia from the stave. Haste becomes a studious spell at 11."),
    ('13 to 16', "Hasted Assault at 14 makes him quickened for a whole fight and adds a third Focus Point. Arcane Shroud at 16 adds a short buff each time he enters Arcane Cascade.",
     "Fly and Translocate become studious spells at 13. Rank-5 to rank-8 slots give an A-graded spell for most defences at each rank."),
    ('17 to 20', "Rank-9 slots and master spellcasting at 17. Double Spellstrike at 19 delivers two spells in one Spellstrike once a day. Supreme Spellstrike at 20 makes him permanently quickened for a Strike or a recharge.",
     "Aspera's planned grand gift at 17 removes the limit on the quickened action. Stolen Spell at 18 only matters against enemy spellcasters."),
]


def combat_page():
    nav = ''.join(f'<a href="#" data-to="{a}">{b}</a>' for a, b in [
        ('cb-levels', 'By level'), ('cb-turns', 'Turn patterns'), ('cb-grid', 'Positioning'), ('cb-off', 'Off-turn'), ('cb-def', 'Targeting'), ('cb-party', 'Party'), ('cb-act', 'Actions')])
    sit = ''.join(f'<a href="#" data-to="{sid}">{h}</a>' for sid, h, _ in SITUATIONS)
    party = table(['Character', 'Class', 'Spell tradition', 'Working together'], [list(p) for p in PARTY])
    levels = table(['Levels', 'How a turn works', 'Spells and resources'], [list(r) for r in LEVELS])
    page = f'''<div class="page doc" data-page="combat">
<header class="ph"><h1>Combat flow and teamwork</h1>
<p class="lede">Turn patterns by situation and level, positioning, targeting and the party. Focus Points are assumed full at the start of each fight.</p></header>
<nav class="jumpbar scroll">{nav}</nav>

<h2 id="cb-levels">{ic("upgrade")}Play patterns by level</h2>
<p class="prose">What changes at each stage of the plan. The turn cards below give the level each turn becomes available.</p>
{levels}

<h2 id="cb-turns">{ic("clock")}Turn patterns</h2>
<p class="prose">Each card is one turn. Glyphs show action cost; tags show the multiple attack penalty at that point. Spellstrike counts as two attacks once it resolves, so any attack after it is at −10. Recharge, Analysis, Force Fang and Improvise Strategy have no attack trait.</p>
<nav class="jumpbar scroll sm">{sit}</nav>
{turns()}

<h2 id="cb-grid">{ic("position")}Positioning</h2>
{key(*TOKENS, ('range', 'Within range'), ('reachsq', 'Within reach'), ('flanksq', 'Within reach and flanking'), ('area', 'Spell area'))}
{diagrams()}

<h2 id="cb-off">{ic("reach")}Off-turn</h2>
<div class="panel"><p>From level 6, Reactive Strike covers every square within 10 feet. It triggers on move and manipulate actions, ranged attacks and leaving a square, so a prone enemy that Stands, an enemy that Strides through his reach, or a caster within reach all provoke it. A Step does not trigger it. A critical hit disrupts a manipulate action. Ending each turn charged, two squares from the target and opposite an ally leaves the enemy a choice between staying flanked and provoking.</p></div>

<h2 id="cb-def">{ic("target")}Targeting by defence</h2>
<p class="prose">Magus's Analysis and the party's Recall Knowledge should identify the weakest defence. Preparing spells for at least three defences keeps a good Spellstrike available.</p>
{defence_table()}

<h2 id="cb-party">{ic("team")}Party</h2>
{party}

<h2 id="cb-act">{ic("fist")}Actions</h2>
<p class="prose">Basic and Athletics actions with their rules text. Class actions are on the Feat paths page.</p>
{action_cards()}
</div>'''
    open('/home/claude/site/pages/combat.html', 'w').write(page)


if __name__ == '__main__':
    combat_page()
    print('ok')
