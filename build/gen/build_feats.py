import html as H, re
import kit
from kit import ic, stars, grade, slug
from entries import entry
from feat_list import *
from feat_evals import F, CLASS_ROLES, SKILL_ROLES, DED_ROLES

KIND = {'C':('fist','Class feat'),'S':('cap','Skill feat'),'G':('star','General feat'),'A':('ancestry','Ancestry feat'),'I':('upgrade','Skill increase'),'B':('crown','Attribute boosts'),'X':('swirl','Class feature'),'H':('heritage','Heritage'),'K':('background','Background')}
PLAN = [
 (1, [('H','Versatile Human → Fleet'),('K','Relentless Dedication → Canny Acumen, Warfare Lore'),('A',"Natural Ambition → Magus's Analysis"),('S','Additional Lore (Academia), from the campaign'),('X','Spellstrike, Arcane Cascade, Laughing Shadow, Dimensional Assault')]),
 (2, [('C','Force Fang'),('S','Additional Lore (Warfare)*')]),
 (3, [('G','Toughness'),('I','Athletics to expert'),('X','Rank 2 slots')]),
 (4, [('C','Expansive Spellstrike'),('S',"Kreighton's Cognitive Crossover")]),
 (5, [('A','General Training → Incredible Initiative'),('I','Arcana to expert'),('B','Str, Con, Int, Wis'),('X','Weapon expertise, rank 3 slots')]),
 (6, [('C','Reactive Strike'),('S','Magical Shorthand')]),
 (7, [('G','Improvise Strategy'),('I','Athletics to master'),('X','Weapon specialization, studious spells (Gecko Grip, Blur)')]),
 (8, [('C','Fused Staff, or Running Recharge if the stave isn\'t ready'),('S','Unmistakable Lore')]),
 (9, [('A','Multitalented → Witch Dedication'),('I','Arcana to master'),('X','Expert spellcasting, Dimensional Assault reaches full Speed')]),
 (10,[('C','Dimensional Disappearance'),('S','Courtly Graces'),('B','Str, Con, Int, Wis or Dex')]),
 (11,[('G',"Axuma's Awakening (reflavoured)"),('I','Society to expert'),('X','Studious: Haste, Ghostly Weapon')]),
 (12,[('C','Sprinting Spellstrike'),('S','Titan Wrestler')]),
 (13,[('A','Clever Improviser or Advanced General Training'),('I','Diplomacy to expert, or Society to master'),('X','Weapon mastery, studious: Fly, Translocate')]),
 (14,[('C','Hasted Assault'),('S','Quick Jump or Leverage Connections')]),
 (15,[('G','Unified Theory'),('I','Arcana to legendary'),('B','Con, Int, two of your choice'),('X','Greater weapon specialization')]),
 (16,[('C','Arcane Shroud (Running Recharge as the alternative)'),('S','Free pick')]),
]

_NRE = re.compile('|'.join(re.escape(n) for n in sorted(F, key=len, reverse=True)))
def link_names(txt):
    parts, last = [], 0
    for m in _NRE.finditer(txt):
        parts.append(H.escape(txt[last:m.start()]))
        parts.append(f'<a href="#" data-to="ft-{slug(m.group(0))}">{H.escape(m.group(0))}</a>')
        last = m.end()
    parts.append(H.escape(txt[last:]))
    return ''.join(parts)

def timeline():
    rows = []
    for lv, slots in PLAN:
        chips = ''.join(f'<span class="slot sk-{k}" title="{KIND[k][1]}">{ic(KIND[k][0])}<span class="k">{KIND[k][1]}</span> {link_names(t)}</span>' for k, t in slots)
        rows.append(f'<div class="lv">{lv}</div><div class="slots">{chips}</div>')
    return '<div class="tl">' + ''.join(rows) + '</div>'

def rate(r, roles):
    return '<div class="rate">' + ''.join(f'<div class="rc{" zero" if r[i]=="0" else ""}"><span class="rl">{ic(k,"ri")}{lab}</span>{stars(r[i])}</div>' for i,(k,lab) in enumerate(roles)) + '</div>'

def fcard(n, roles, kind='feat'):
    e = entry(n, kind)
    r, g, plan, ev = F[n]
    acc = f'<div class="acc"><div class="ag">{ic("crown")}<span>Pick for Cyrus</span>{grade(g)}</div><div class="bds"><span class="bd">{ic("clock")}{H.escape(plan)}</span></div></div>'
    lvl = e['level'] if e['level'].startswith('Feat') else f'Feat {e["level"]}'
    return kit.rules_card(e, 'ft-'+slug(n), kicker=lvl, evaluation=ev, ratings_html=rate(r, roles), access_html=acc, show_trad=False)

def feature_card(n, k, note):
    e = entry(n, k)
    if k == 'spell':
        kick = f'Focus {e["level"].replace("Spell ","")}' if e['level'].startswith('Spell') else f'Focus {e["level"]}'
    else:
        kick = 'Class feature' if k == 'feature' else 'Action'
    return kit.rules_card(e, 'ft-'+slug(n)+('-spell' if k=='spell' else ''), kicker=kick, evaluation=note, show_trad=(k=='spell'))

NOTES = {
 'Spellstrike': "Spellstrike is the centre of every turn Cyrus plays. For two actions he delivers a spell through Aspera's Strike, which means his spells use the weapon's 10-foot reach and his strongest single-target damage arrives on one attack roll. Save spells are the reliable choice: the target saves even if the Strike misses, and only a critical failure on the Strike wastes the spell. Attack-roll spells hit harder but rise and fall with the Strike, so they belong on turns when the target is off-guard. The cost is the multiple attack penalty, since Spellstrike counts as two attacks, and the need to recharge. The rest of the build, from Magus's Analysis to Dimensional Assault, exists largely to make that recharge cheap.",
 'Arcane Cascade': "Arcane Cascade is the stance Cyrus should be in for almost every round of every fight. It adds force damage to each melee Strike, gives a little resistance to spell damage, and through Laughing Shadow adds Speed and the larger off-guard bonus. Entering it costs an action, so on the opening turn it competes with moving into reach; from level 7 a studious spell lets him enter it for free. If he casts a spell earlier in the turn, the extra damage can take that spell's damage type, which is a useful way around force resistance or onto a known weakness.",
 'Laughing Shadow': "Laughing Shadow is what turns Cyrus from a reach fighter into a skirmisher. The Speed bonus extends both his Strides and Dimensional Assault, and against an off-guard target his stance damage rises to 3, then 5 at level 7 and 7 at level 15. Aspera's Shadow Synthesis lets him use it with Aspera in both hands. The design rewards turns that make the target off-guard before the Spellstrike lands: flanking with an ally, Trip, Improvise Strategy, or striking while invisible after Dimensional Disappearance. Against a target that is never off-guard it adds little beyond the Speed, which is why so much of the plan is about creating those conditions.",
 'Conflux Spells': "Conflux spells are Cyrus's focus spells, and each one also recharges Spellstrike when cast with at least one action. His pool is one Focus Point from Dimensional Assault, two from level 2 with Force Fang, and three from 14 with Hasted Assault. In a campaign with one or two fights a day and rest between them, Refocus nearly always restores the pool before the next fight, so he can spend every point in each encounter rather than saving them.",
 'Studious Spells': "Studious spells are a short list of spells tied to Cyrus's training and hybrid study, and casting one lets him enter Arcane Cascade as a free action on the same turn. That makes the opening round much more efficient: Blur from 7, and Haste from 11, give him a buff and the stance for the price of the spell alone. Gecko Grip, Ghostly Weapon, Fly and Translocate are situational, but each solves a real problem: climbing, incorporeal enemies, flying enemies and getting out of trouble.",
 'Dimensional Assault': "Dimensional Assault is Cyrus's best single action. It teleports him, makes a Strike at whatever the multiple attack penalty is at that point, and recharges Spellstrike, all for one action and one Focus Point. With Aspera he has to land within reach of an enemy, which means he can land 10 feet away on a square that flanks with an ally and is outside the target's own reach. Teleporting does not trigger reactions that respond to movement, so it is also how he crosses a front line safely. From level 9 its range becomes his full Speed. Its main limit is the Focus Point, which Force Fang also wants.",
 'Force Fang': "Force Fang is a one-action conflux spell that deals force damage to a creature within reach with no attack roll, so it cannot miss, and it recharges Spellstrike. After a Spellstrike, when Magus's Analysis has already been used on that creature, it is the best third action available because the alternative Strike would be at −10. The damage is small compared to a Spellstrike, so its real value is the guaranteed recharge with a little damage attached. It has the manipulate trait, so cast it from 10 feet away rather than inside an enemy's reach.",
 'Hasted Assault': "Hasted Assault makes Cyrus quickened for a minute, with the extra action limited to Stride or Strike, and recharges Spellstrike when cast. Over a typical fight that is three or four extra actions, most of which become the Stride to a flanking square that lets him Spellstrike every turn. He does not gain the extra action on the turn he casts it, so it is best cast in the first round. It has the manipulate trait, so cast it before closing in rather than next to an enemy.",
}

def build():
    tl = timeline()
    feats_class = '\n'.join(fcard(n, CLASS_ROLES) for n in CLASS)
    feats_skill = '\n'.join(fcard(n, SKILL_ROLES) for n in SKILLGEN)
    feats_anc = '\n'.join(fcard(n, CLASS_ROLES if False else SKILL_ROLES) for n in ANCESTRY)
    feats_ded = '\n'.join(fcard(n, DED_ROLES) for n in DEDICATIONS)
    feats_feat = '\n'.join(feature_card(n, k, NOTES.get(n,'')) for n,k in FEATURES)
    nav = ''.join(f'<a href="#" data-to="{i}">{t}</a>' for i,t in [('f-plan','Level plan'),('f-decide','Decisions'),('f-features','Class features'),('f-class','Class feats'),('f-skill','Skill and general'),('f-anc','Ancestry'),('f-ded','Level 9 dedication'),('f-attr','Attributes')])
    decide = f'''<div class="grid3">
<div class="panel"><h3>{ic('staff')}Level 8</h3><p><a href="#" data-to="ft-fused-staff">Fused Staff</a> if Aspera's stave is ready that level. Otherwise <a href="#" data-to="ft-running-recharge">Running Recharge</a>, and retrain into Fused Staff when the stave arrives.</p></div>
<div class="panel"><h3>{ic('occult','t-occult')}Level 9</h3><p><a href="#" data-to="ft-witch-dedication">Witch</a> for occult casting and a familiar. <a href="#" data-to="ft-psychic-dedication">Psychic</a> if a combat psi cantrip matters more. Either lets Cyrus cast Synesthesia from the stave.</p></div>
<div class="panel"><h3>{ic('clock')}Levels 14 and 16</h3><p><a href="#" data-to="ft-hasted-assault">Hasted Assault</a> at 14 and <a href="#" data-to="ft-arcane-shroud">Arcane Shroud</a> at 16. Being quickened most turns from 14 covers the movement <a href="#" data-to="ft-running-recharge">Running Recharge</a> would add, so the level-16 slot goes to a buff that can be refreshed for one action. Running Recharge stays the alternative.</p></div></div>'''
    attr = '''<div class="tw"><table class="tbl stack"><thead><tr><th>Level</th><th>Boosts</th><th>Why</th></tr></thead><tbody>
<tr><td data-l="Level">5</td><td data-l="Boosts">Str (partial, toward +5), Con, Int to +4, Wis</td><td data-l="Why">Int +4 lifts spell DC and adds a trained skill and language.</td></tr>
<tr><td data-l="Level">10</td><td data-l="Boosts">Str to +5, Con, Int (partial), Wis or Dex</td><td data-l="Why">Strength first for Aspera's attack and damage. Bank half of Int +5 if play will reach 15.</td></tr>
<tr><td data-l="Level">15</td><td data-l="Boosts">Int to +5, Con, two of Wis, Dex or Str</td><td data-l="Why">Int +5 arrives with master spellcasting at 17 in sight.</td></tr>
</tbody></table></div>'''
    page = f'''<div class="page doc" data-page="feats">
<header class="ph"><h1>Feat paths</h1>
<p class="lede">Human Laughing Shadow magus, levels 1 to 16. The route keeps Expansive at 4, Reactive Strike at 6, Improvise Strategy at 7 and Sprinting Spellstrike at 12. The open choices are level 8, the level-9 dedication and the late class feats. Feat levels follow the remastered magus in <em>Impossible Magic</em>. Ratings assume one or two fights a day with rests between them.</p></header>
<nav class="jumpbar scroll">{nav}</nav>
<h2 id="f-plan">Level plan</h2><p class="muted">Select a feat to open its details beside the plan. *If Warfare Lore is already trained from the background, the table's duplicate-training rule moves that training to another Lore (Engineering or Undead).</p>
{tl}
<h2 id="f-decide">Decisions still open</h2>{decide}
<h2 id="f-features">Class features and focus spells</h2><p class="muted">Rules Cyrus uses every turn.</p>{feats_feat}
<h2 id="f-class">Class feats</h2>{feats_class}
<h2 id="f-skill">Skill and general feats</h2>{feats_skill}
<h2 id="f-anc">Ancestry feats</h2>{feats_anc}
<h2 id="f-ded">Level 9 dedication</h2><p class="muted">Multitalented grants one of these at 9. The party has divine and primal casters but no occult caster.</p>{feats_ded}
<h2 id="f-attr">Attributes</h2>{attr}
</div>'''
    open('/home/claude/site/pages/feats.html','w').write(page)
    print('ok', len(page))

if __name__ == '__main__':
    build()
