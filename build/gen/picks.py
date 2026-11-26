# Rank-end summaries. Keys: role -> list of spell names; plus 'book', 'scroll', 'wand' and an optional 'note'.
P = {}
P[0] = dict(
    Damage=['Gouging Claw', 'Ignition', 'Needle Darts'], Control=['Tangle Vine'], Debuff=['Frostbite'],
    **{'Buff / Heal': ['Shield'], 'Positioning': [], 'Utility': ['Detect Magic', 'Message']},
    book=['Gouging Claw', 'Ignition', 'Needle Darts', 'Frostbite', 'Shield', 'Electric Arc', 'Tangle Vine', 'Detect Magic'],
    prep="Daily five: Gouging Claw, Ignition or Needle Darts (by enemy), Frostbite, Shield, and one utility.",
    familiar=['Guidance', 'Read the Air'],
    note="Familiar cantrips only apply if Cyrus takes Witch Dedication at 9.")
P[1] = dict(
    Damage=['Thunderstrike', 'Shocking Grasp'], Control=['Grease', 'Gust of Wind'], Debuff=['Briny Bolt', 'Fear'],
    **{'Buff / Heal': ['Sure Strike'], 'Positioning': ['Fleet Step', 'Gust of Wind'], 'Utility': ['Illusory Object', 'Gentle Landing']},
    book=['Sure Strike', 'Briny Bolt', 'Thunderstrike', 'Fear', 'Shocking Grasp', 'Gust of Wind', 'Grease'],
    scroll=['Illusory Disguise', 'Illusory Object', 'Helpful Steps', 'Friendfetch', 'Soothe'],
    wand=['Pocket Library', 'Soothe (occult, after 9)'],
    prep="Both rank-1 slots should usually be Sure Strike. From level 12, keep Gust of Wind for a cheap Sprinting Spellstrike.")
P[2] = dict(
    Damage=['Blazing Bolt', 'Sudden Bolt'], Control=['Telekinetic Maneuver', 'Laughing Fit'], Debuff=['Revealing Light'],
    **{'Buff / Heal': ['Blur', 'Resist Energy'], 'Positioning': ['Acid Grip', "Loose Time's Arrow"], 'Utility': ['Invisibility', 'Dispel Magic']},
    book=['Acid Grip', 'Invisibility', 'Telekinetic Maneuver', 'Blazing Bolt', 'Revealing Light', 'Laughing Fit'],
    scroll=['Dispel Magic', 'Revealing Light', 'Resist Energy', 'Water Breathing', 'Clear Mind', 'Silence'],
    wand=['Invisibility', 'Tailwind', 'See the Unseen'],
    prep="Acid Grip and Telekinetic Maneuver as payloads; Invisibility when the plan involves an approach.")
P[3] = dict(
    Damage=['Lightning Bolt', 'Magnetic Acceleration'], Control=['Slow', 'Paralyze'], Debuff=['Blister Bomb', 'Blindness'],
    **{'Buff / Heal': ['Haste', 'Heroism'], 'Positioning': ['Time Jump'], 'Utility': ['Hypercognition', 'Ghostly Weapon']},
    book=['Haste', 'Slow', 'Lightning Bolt', 'Time Jump', 'Blister Bomb'],
    scroll=['Ghostly Weapon', 'Earthbind', 'Heroism', 'Hypercognition'],
    wand=['Haste', 'Hypercognition (occult, after 9)'],
    prep="Haste and Slow are the two spells only Cyrus brings. Lightning Bolt becomes the Sprinting staple at 12.")
P[4] = dict(
    Damage=['Force Rain'], Control=['Containment', 'Grasping Earth'], Debuff=['Vision of Death'],
    **{'Buff / Heal': ['Invisibility'], 'Positioning': ['Fly', 'Translocate'], 'Utility': ['Clairvoyance']},
    book=['Fly', 'Translocate', 'Containment', 'Vision of Death'],
    scroll=['Clairvoyance', 'Unfettered Movement', 'Tortoise and the Hare'],
    wand=['Invisibility (rank 4)', 'Clairvoyance'],
    prep="Heighten Invisibility to rank 4 for a fight where Cyrus wants to attack unseen. Fly and Translocate become studious at 13.")
P[5] = dict(
    Damage=['Glacial Skewer', 'Blazing Fissure'], Control=['Wall of Stone', 'Weight of the World'], Debuff=['Synesthesia'],
    **{'Buff / Heal': ['Shadow Siphon'], 'Positioning': ['Tornadic Gale', 'Space Fold Gate'], 'Utility': ['Sending', 'Magic Passage']},
    book=['Weight of the World', 'Wall of Stone', 'Glacial Skewer', 'Blazing Fissure', 'Tornadic Gale'],
    scroll=['Magic Passage', 'Sending', 'Space Fold Gate', 'Banishment'],
    wand=['See the Unseen (rank 5)', 'Synesthesia (stave)'],
    prep="Weight of the World and Wall of Stone. Blazing Fissure is the rank-5 Sprinting line when prone helps more than damage.")
P[6] = dict(
    Damage=['Chain Lightning', 'Disintegrate', 'Living Thunderbolt'], Control=['Wall of Force', 'Petrify'], Debuff=[],
    **{'Buff / Heal': ['Zealous Conviction'], 'Positioning': ['Living Thunderbolt', 'Collective Transposition'], 'Utility': ['Truesight', 'Teleport']},
    book=['Living Thunderbolt', 'Chain Lightning', 'Disintegrate', 'Wall of Force'],
    scroll=['Truesight', 'Teleport', 'Zealous Conviction'],
    wand=[],
    prep="Living Thunderbolt for Sprinting Spellstrike turns. Chain Lightning is the reliable damage slot; Disintegrate when Sure Strike or an off-guard target makes the hit likely.")
P[7] = dict(
    Damage=['Frigid Flurry', 'Telekinetic Bombardment'], Control=['Telekinetic Bombardment'], Debuff=['Defy the Gods'],
    **{'Buff / Heal': ['True Target', 'Haste (rank 7)'], 'Positioning': ['Frigid Flurry'], 'Utility': ['Contingency']},
    book=['True Target', 'Frigid Flurry', 'Telekinetic Bombardment', 'Contingency'],
    scroll=['Ethereal Jaunt'],
    wand=[],
    prep="True Target for the boss, Frigid Flurry as the line. Rank-7 Haste on six creatures is the strongest opener the party has.")
P[8] = dict(
    Damage=['Arctic Rift', 'Roar of Freedom'], Control=['Quandary', 'Uncontrollable Dance'], Debuff=['Uncontrollable Dance'],
    **{'Buff / Heal': ['Disappearance', 'Roar of Freedom'], 'Positioning': [], 'Utility': ['Disappearance']},
    book=['Disappearance', 'Quandary', 'Arctic Rift', 'Roar of Freedom', 'Uncontrollable Dance'],
    scroll=['Falling Sky'], wand=[],
    prep="Disappearance makes every Strike hit an off-guard target. Quandary removes the worst enemy for most of a fight.")
P[9] = dict(
    Damage=['Dimensional Excision', 'Falling Stars'], Control=['Remake Physiology'], Debuff=['Remake Physiology'],
    **{'Buff / Heal': ['Foresight'], 'Positioning': [], 'Utility': []},
    book=['Foresight', 'Remake Physiology', 'Dimensional Excision'], scroll=[], wand=[],
    prep="Cyrus gets rank-9 slots at 17. Foresight on whichever ally the boss targets and Remake Physiology on the boss.")

# additions from the full review of the arcane list
def _add(rank, key, *names):
    lst = P[rank].setdefault(key, [])
    for n in names:
        if n not in lst:
            lst.append(n)
_add(1, 'Damage', 'Acidic Burst'); _add(1, 'Control', 'Shockwave'); _add(1, 'Debuff', 'Enfeeble')
_add(1, 'book', 'Acidic Burst', 'Shockwave'); _add(1, 'scroll', 'Pest Form', 'Charm'); _add(1, 'wand', 'Alarm')
_add(2, 'Damage', 'Heat Metal'); _add(2, 'Control', 'Charitable Urge', 'Entangling Flora'); _add(2, 'Debuff', 'Vomit Swarm')
_add(2, 'Utility', 'Knock'); _add(2, 'book', 'Heat Metal', 'Charitable Urge', 'Vomit Swarm')
_add(2, 'scroll', 'Knock', 'Translate'); _add(2, 'wand', 'Darkvision', 'False Vitality')
_add(3, 'Damage', 'Vampiric Feast', 'Agonizing Despair'); _add(3, 'Control', 'Stinking Cloud'); _add(3, 'Debuff', "Day's Weight")
_add(3, 'Utility', 'Shared Invisibility'); _add(3, 'book', 'Vampiric Feast', 'Agonizing Despair', 'Shared Invisibility')
_add(4, 'Damage', 'Chromatic Ray'); _add(4, 'Control', 'Grasp of the Deep'); _add(4, 'Buff / Heal', 'Mountain Resilience', 'Winning Streak')
_add(4, 'book', 'Chromatic Ray', 'Grasp of the Deep')
_add(5, 'Damage', 'Grisly Growths', 'Mirror Malefactors'); _add(5, 'Control', 'Wave of Despair', 'Stagnate Time'); _add(5, 'Debuff', "Mariner's Curse")
_add(5, 'book', 'Wave of Despair', 'Grisly Growths')
_add(6, 'Damage', 'Necrotize'); _add(6, 'Control', 'Lignify', 'Vitrifying Blast'); _add(6, 'Debuff', 'Vitrifying Blast')
_add(6, 'book', 'Necrotize', 'Lignify')
_add(7, 'Control', 'Power Word Blind'); _add(7, 'Debuff', 'Power Word Blind'); _add(7, 'Buff / Heal', 'Time Beacon', 'Energy Aegis')
_add(7, 'book', 'Time Beacon', 'Power Word Blind'); _add(7, 'wand', 'Energy Aegis')
_add(8, 'Damage', 'Boil Blood'); _add(8, 'Control', 'Power Word Stun'); _add(8, 'book', 'Power Word Stun', 'Boil Blood')
_add(9, 'Damage', 'Power Word Kill'); _add(9, 'Debuff', 'Unspeakable Shadow'); _add(9, 'Positioning', 'Bilocation')
_add(9, 'book', 'Power Word Kill', 'Unspeakable Shadow', 'Bilocation')
P[2]['prep'] = "Acid Grip and Telekinetic Maneuver as payloads; Charitable Urge or Heat Metal when the enemy suits them; Invisibility when the plan involves an approach."
P[3]['prep'] = "Haste and Slow are the two spells only Cyrus brings. Vampiric Feast and Agonizing Despair are the strongest single-target payloads. Lightning Bolt becomes the Sprinting staple at 12."
P[5]['prep'] = "Weight of the World and Wall of Stone, with Wave of Despair for groups. Blazing Fissure is the rank-5 Sprinting line when prone helps more than damage."
P[8]['prep'] = "Roar of Freedom is the best final action Cyrus has: one action for area damage, a debuff and temporary Hit Points. Disappearance makes every Strike hit an off-guard target. Power Word Stun takes actions from a boss for one action and no save, leaving two for Spellstrike."
_add(6, 'Damage', 'Missed Cue'); _add(6, 'Debuff', 'Missed Cue'); _add(6, 'book', 'Missed Cue')
_add(4, 'Damage', "Mantis's Grasp"); _add(4, 'Debuff', 'Entangle Fate'); _add(4, 'book', "Mantis's Grasp", 'Entangle Fate')
_add(9, 'Buff / Heal', 'Prismatic Shield')
