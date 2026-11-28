# Rank-end summaries, written against three goals: a spell for every defence (AC, Fortitude, Reflex, Will),
# varied damage types, and tactical variety at each rank.
# Keys: role -> spell names; 'saves' -> defence -> spell names; 'book' spellbook picks in priority order;
# 'types' damage types among the spellbook picks; 'prep' and an optional 'note'.
# Scroll and wand picks are worked out from the grades in build_spells.py.
P = {}


def _p(rank, damage, control, debuff, buff, positioning, utility, saves, book, book2, types, prep, **kw):
    P[rank] = dict(Damage=damage, Control=control, Debuff=debuff, saves=saves, book=book, book2=book2, types=types, prep=prep,
                   **{'Buff / Heal': buff, 'Positioning': positioning, 'Utility': utility}, **kw)


_p(0,
   ['Gouging Claw', 'Ignition', 'Needle Darts'], ['Tangle Vine'], ['Frostbite'], ['Shield'], [], ['Detect Magic', 'Message'],
   dict(AC=['Gouging Claw', 'Ignition', 'Needle Darts', 'Live Wire'], Fortitude=['Frostbite'], Reflex=['Electric Arc'], Will=['Daze']),
   ['Gouging Claw', 'Ignition', 'Frostbite', 'Electric Arc', 'Shield', 'Message'],
   ['Needle Darts', 'Live Wire', 'Tangle Vine', 'Detect Magic'],
   'bleed, fire, cold, electricity, piercing, slashing',
   "Daily five: Gouging Claw, Ignition or Needle Darts (by enemy), Frostbite or Electric Arc as the save cantrip, Shield, and one utility. "
   "Daze is the only Will cantrip and is graded C, so Will coverage starts at rank 1 with Fear.",
   familiar=['Guidance', 'Read the Air'],
   note="Familiar cantrips apply from the Witch Dedication at 9.")

_p(1,
   ['Thunderstrike', 'Shocking Grasp', 'Dehydrate', 'Acidic Burst'], ['Grease', 'Gust of Wind', 'Shockwave'], ['Briny Bolt', 'Fear', 'Enfeeble'],
   ['Sure Strike'], ['Fleet Step', 'Gust of Wind'], ['Illusory Object', 'Gentle Landing'],
   dict(AC=['Briny Bolt', 'Shocking Grasp'], Fortitude=['Dehydrate', 'Gust of Wind'], Reflex=['Thunderstrike', 'Shockwave'], Will=['Fear', 'Befuddle']),
   ['Sure Strike', 'Briny Bolt', 'Thunderstrike', 'Fear', 'Shockwave', 'Dehydrate'],
   ['Shocking Grasp', 'Gust of Wind', 'Grease', 'Acidic Burst', 'Illusory Object'],
   'bludgeoning, electricity, sonic, fire, acid',
   "Both rank-1 slots should usually be Sure Strike. Once a Ring of Wizardry adds rank-1 slots at 7, Fear and a damage spell fit beside it. "
   "From level 12, keep Gust of Wind for a cheap Sprinting Spellstrike.")

_p(2,
   ['Sudden Bolt', 'Blazing Bolt', 'Spray of Salt', 'Heat Metal'], ['Telekinetic Maneuver', 'Laughing Fit', 'Charitable Urge', 'Entangling Flora'],
   ['Ignite Fireworks', 'Disorienting Flash', 'Revealing Light', 'Vomit Swarm'], ['Blur', 'Hidebound', 'Warping Pull', 'Resist Energy'],
   ['Acid Grip', "Loose Time's Arrow", 'Warping Pull'], ['Invisibility', 'Dispel Magic', 'Gecko Grip', 'Knock'],
   dict(AC=['Telekinetic Maneuver', 'Blazing Bolt'], Fortitude=['Spray of Salt', 'Disorienting Flash'], Reflex=['Acid Grip', 'Ignite Fireworks', 'Sudden Bolt'], Will=['Laughing Fit', 'Charitable Urge']),
   ['Acid Grip', 'Invisibility', 'Telekinetic Maneuver', 'Ignite Fireworks', 'Spray of Salt', 'Disorienting Flash', 'Hidebound', 'Warping Pull'],
   ['Laughing Fit', 'Revealing Light', 'Sudden Bolt', 'Blazing Bolt', 'Heat Metal', 'Charitable Urge', 'Vomit Swarm'],
   'acid, fire, sonic, electricity, piercing',
   "Acid Grip is the default spell. The second slot goes to Ignite Fireworks or a Fortitude area spell against groups, Telekinetic Maneuver against one strong enemy, "
   "or Invisibility when the plan involves an approach. No Fortitude or Will spell at this rank is graded above B, so learn one of Spray of Salt and Disorienting Flash, not both, "
   "and rely on Fear at rank 1 and Slow at rank 3 for those saves. Blur and Gecko Grip enter the spellbook at 7 as studious spells.")

_p(3,
   ['Lightning Bolt', 'Vampiric Feast', 'Agonizing Despair', 'Gravity Wave', 'Magnetic Acceleration'], ['Slow', 'Skyglass Prison', 'Stinking Cloud', 'Paralyze'],
   ['Blister Bomb', "Day's Weight", 'Roaring Applause', 'Blindness'], ['Haste', 'Heroism', 'Wooden Double', "Cloud Dragon's Cloak"],
   ['Blazing Dive', 'Echo Jump', 'Time Jump'], ['Hypercognition', 'Ghostly Weapon', 'Shared Invisibility'],
   dict(AC=['Magnetic Acceleration', 'Shocking Grasp (rank 3)'], Fortitude=['Slow', 'Vampiric Feast', 'Gravity Wave', 'Skyglass Prison'], Reflex=['Lightning Bolt', 'Blazing Dive', 'Echo Jump', 'Fireball'], Will=['Agonizing Despair', 'Roaring Applause']),
   ['Haste', 'Slow', 'Lightning Bolt', 'Blazing Dive', 'Echo Jump', 'Time Jump', 'Agonizing Despair', 'Vampiric Feast', 'Roaring Applause', 'Gravity Wave'],
   ['Skyglass Prison', 'Blister Bomb', 'Shared Invisibility', 'Wooden Double', "Cloud Dragon's Cloak", "Day's Weight", 'Stinking Cloud'],
   'electricity, fire, force, void, mental, bludgeoning',
   "Haste and Slow are the default pair until more slots arrive. Vampiric Feast and Agonizing Despair are the strongest single-target spells, on Fortitude and Will. "
   "Blazing Dive carries him into a fight with a Strike, and Echo Jump takes him out after one. "
   "Roaring Applause sets up Reactive Strike against anything that is not mindless. No attack spell at this rank is graded above B, so heighten Shocking Grasp when AC is the weak defence. "
   "Lightning Bolt becomes the Sprinting Spellstrike line at 12. Ghostly Weapon enters the spellbook at 11 as a studious spell.")

_p(4,
   ['Force Rain', 'Chromatic Ray', "Mantis's Grasp", 'Grasp of the Deep'], ['Wall of Mirrors', 'Containment', 'Grasping Earth', 'Freezing Touch'],
   ['Vision of Death', 'Entangle Fate', 'Friends to Foes', 'Lost Things Returned'], ['Invisibility (rank 4)', 'Mountain Resilience', 'Winning Streak'],
   ['Fly', 'Translocate'], ['Clairvoyance'],
   dict(AC=['Chromatic Ray'], Fortitude=['Freezing Touch', 'Grasping Earth'], Reflex=['Force Rain', "Mantis's Grasp"], Will=['Grasp of the Deep', 'Friends to Foes', 'Vision of Death']),
   ['Fly', 'Translocate', 'Wall of Mirrors', 'Force Rain', 'Chromatic Ray', 'Freezing Touch', 'Grasp of the Deep', "Mantis's Grasp"],
   ['Friends to Foes', 'Entangle Fate', 'Lost Things Returned', 'Vision of Death', 'Containment'],
   'force, cold, bludgeoning, mental',
   "Heighten Invisibility to rank 4 for a fight where Cyrus wants to attack unseen. Force Rain is the flexible damage slot at one, two or three actions. "
   "Freezing Touch, Mantis's Grasp and Grasp of the Deep give a spell for Fortitude, Reflex and Will. Fly and Translocate become studious at 13.")

_p(5,
   ['Glacial Skewer', 'Blazing Fissure', 'Grisly Growths', 'Mirror Malefactors', 'Blood Feast', 'Plasma Whirl'], ['Wall of Stone', 'Weight of the World', 'Wave of Despair', 'Stagnate Time'],
   ['Synesthesia', "Mariner's Curse"], ['Shadow Siphon'], ['Tornadic Gale', 'Space Fold Gate'], ['Sending', 'Magic Passage', 'Truespeech'],
   dict(AC=['Glacial Skewer', 'Blood Feast'], Fortitude=['Weight of the World', 'Grisly Growths'], Reflex=['Blazing Fissure', 'Tornadic Gale', 'Plasma Whirl'], Will=['Mirror Malefactors', 'Wave of Despair', 'Stagnate Time']),
   ['Weight of the World', 'Wall of Stone', 'Glacial Skewer', 'Blazing Fissure', 'Wave of Despair', 'Mirror Malefactors', 'Grisly Growths'],
   ['Tornadic Gale', 'Plasma Whirl', 'Blood Feast', 'Stagnate Time', 'Truespeech'],
   'bludgeoning, fire, cold, piercing, mental, bleed',
   "Weight of the World and Wall of Stone, with Wave of Despair for groups. Blazing Fissure is the rank-5 Sprinting line when prone helps more than damage. "
   "Every defence has an A-graded spell at this rank.")

_p(6,
   ['Chain Lightning', 'Disintegrate', 'Living Thunderbolt', 'Necrotize', 'Missed Cue', 'Silver Spear', 'Phantasmal Calamity'], ['Wall of Force', 'Petrify', 'Lignify', 'Vitrifying Blast', 'Curse of the Toad Prince'],
   ['Vitrifying Blast', 'Missed Cue'], ['Zealous Conviction'], ['Living Thunderbolt', 'Collective Transposition'], ['Truesight', 'Teleport'],
   dict(AC=['Disintegrate', 'Silver Spear'], Fortitude=['Necrotize', 'Lignify', 'Vampiric Exsanguination'], Reflex=['Living Thunderbolt', 'Chain Lightning', 'Vitrifying Blast'], Will=['Missed Cue', 'Phantasmal Calamity', 'Curse of the Toad Prince']),
   ['Living Thunderbolt', 'Chain Lightning', 'Disintegrate', 'Wall of Force', 'Missed Cue', 'Necrotize', 'Lignify'],
   ['Silver Spear', 'Phantasmal Calamity', 'Curse of the Toad Prince', 'Vitrifying Blast', 'Vampiric Exsanguination'],
   'electricity, void, mental, piercing',
   "Living Thunderbolt for Sprinting Spellstrike turns. Chain Lightning is the reliable damage slot; Disintegrate when Sure Strike or an off-guard target makes the hit likely. "
   "Missed Cue and Necrotize are the Will and Fortitude spells.")

_p(7,
   ['Frigid Flurry', 'Telekinetic Bombardment', 'Comet Charge'], ['Telekinetic Bombardment', 'Power Word Blind'], ['Defy the Gods', 'Power Word Blind'],
   ['True Target', 'Haste (rank 7)', 'Time Beacon', 'Energy Aegis'], ['Frigid Flurry', 'Comet Charge'], ['Contingency'],
   dict(AC=['Comet Charge', 'Disintegrate (rank 7)'], Fortitude=['Necrotize (rank 7)'], Reflex=['Frigid Flurry', 'Telekinetic Bombardment'], Will=['Warp Mind', 'Missed Cue (rank 7)']),
   ['True Target', 'Frigid Flurry', 'Telekinetic Bombardment', 'Comet Charge', 'Power Word Blind', 'Time Beacon'],
   ['Contingency', 'Energy Aegis', 'Warp Mind'],
   'cold, slashing, bludgeoning',
   "True Target for the boss, Frigid Flurry as the line. Rank-7 Haste on six creatures is the strongest opening spell for the whole party. "
   "This rank's own spells target Reflex and AC, so Fortitude and Will come from Necrotize and Missed Cue heightened into these slots.")

_p(8,
   ['Arctic Rift', 'Roar of Freedom', 'Polar Ray', 'Boil Blood'], ['Quandary', 'Uncontrollable Dance', 'Power Word Stun', 'Falling Sky'], ['Uncontrollable Dance'],
   ['Disappearance', 'Roar of Freedom'], [], ['Disappearance'],
   dict(AC=['Polar Ray'], Fortitude=['Arctic Rift', 'Boil Blood', 'Falling Sky'], Reflex=['Metallic Meteorite Glyph', 'Frigid Flurry (rank 8)'], Will=['Roar of Freedom', 'Uncontrollable Dance']),
   ['Disappearance', 'Quandary', 'Arctic Rift', 'Roar of Freedom', 'Uncontrollable Dance', 'Power Word Stun', 'Boil Blood'],
   ['Falling Sky', 'Polar Ray', 'Metallic Meteorite Glyph'],
   'cold, sonic, fire',
   "Roar of Freedom is the best final action Cyrus has: one action for area damage, a debuff and temporary Hit Points. Disappearance makes every Strike hit an off-guard target. "
   "Power Word Stun takes actions from a boss for one action and no save, leaving two for Spellstrike. Polar Ray is the spell against AC, and its drain lowers the Fortitude save for Arctic Rift or Boil Blood. Reflex has no A-graded spell at this rank, so Frigid Flurry heightened covers it.")

_p(9,
   ['Dimensional Excision', 'Falling Stars', 'Power Word Kill'], ['Remake Physiology'], ['Remake Physiology', 'Unspeakable Shadow'],
   ['Foresight', 'Prismatic Shield'], ['Bilocation'], [],
   dict(AC=['Disintegrate (rank 9)'], Fortitude=['Remake Physiology', 'Massacre'], Reflex=['Falling Stars'], Will=['Dimensional Excision', 'Unspeakable Shadow']),
   ['Foresight', 'Remake Physiology', 'Dimensional Excision', 'Power Word Kill', 'Unspeakable Shadow'],
   ['Bilocation', 'Prismatic Shield', 'Falling Stars'],
   'bleed, bludgeoning, fire',
   "Cyrus gets rank-9 slots at 17. Foresight on whichever ally the boss targets and Remake Physiology on the boss. "
   "No attack spell at this rank has a card, so Disintegrate heightened is the spell against AC.")

BOOK = {
    0: ['Gouging Claw', 'Ignition', 'Frostbite', 'Electric Arc', 'Shield', 'Message', 'Needle Darts', 'Tangle Vine', 'Detect Magic'],
    1: ['Sure Strike', 'Briny Bolt', 'Thunderstrike', 'Fear', 'Shockwave', 'Dehydrate', 'Shocking Grasp', 'Gust of Wind', 'Grease', 'Acidic Burst'],
    2: ['Acid Grip', 'Invisibility', 'Telekinetic Maneuver', 'Ignite Fireworks', 'Spray of Salt', 'Disorienting Flash', 'Hidebound', 'Warping Pull',
        'Laughing Fit', 'Revealing Light', 'Blazing Bolt', 'Heat Metal', 'Charitable Urge', 'Vomit Swarm'],
    3: ['Haste', 'Slow', 'Lightning Bolt', 'Blazing Dive', 'Echo Jump', 'Time Jump', 'Agonizing Despair', 'Vampiric Feast', 'Roaring Applause', 'Gravity Wave', 'Blister Bomb', 'Shared Invisibility'],
    4: ['Fly', 'Translocate', 'Wall of Mirrors', 'Force Rain', 'Chromatic Ray', 'Freezing Touch', 'Grasp of the Deep', "Mantis's Grasp", 'Entangle Fate', 'Vision of Death', 'Containment'],
    5: ['Weight of the World', 'Wall of Stone', 'Glacial Skewer', 'Blazing Fissure', 'Wave of Despair', 'Mirror Malefactors', 'Grisly Growths', 'Tornadic Gale'],
    6: ['Living Thunderbolt', 'Chain Lightning', 'Disintegrate', 'Wall of Force', 'Missed Cue', 'Necrotize', 'Lignify'],
    7: ['True Target', 'Frigid Flurry', 'Telekinetic Bombardment', 'Comet Charge', 'Power Word Blind', 'Time Beacon', 'Contingency'],
    8: ['Disappearance', 'Quandary', 'Arctic Rift', 'Roar of Freedom', 'Uncontrollable Dance', 'Power Word Stun', 'Polar Ray', 'Boil Blood'],
    9: ['Foresight', 'Remake Physiology', 'Dimensional Excision', 'Power Word Kill', 'Unspeakable Shadow', 'Bilocation'],
}
TYPES = {0: 'bleed, fire, cold, electricity, piercing', 2: 'acid, fire, sonic, piercing', 6: 'electricity, void, mental', 9: 'bleed'}
for _r in P:
    P[_r]['book'] = BOOK[_r]
    P[_r].pop('book2', None)
    if _r in TYPES:
        P[_r]['types'] = TYPES[_r]


# ── Preparation notes in their current wording ──
_PREP = {
0: "Cyrus prepares five cantrips each day. Gouging Claw is always one of them, with Ignition or Needle Darts as a second attack cantrip according to the enemy, Frostbite or Electric Arc as a cantrip settled by a save, Shield, and one cantrip for use outside combat. Daze is the only cantrip that targets Will and is graded C, so his spells against Will begin at rank 1 with Fear.",
1: "Both rank-1 slots usually hold Sure Strike, because each casting improves a whole Spellstrike. Once a Ring of Wizardry adds rank-1 slots at level 7, there is room beside it for Fear and a damage spell. From level 12 Gust of Wind is worth a slot as well, since it gives him a Sprinting Spellstrike at very little cost.",
2: "Acid Grip takes the first slot on most days. The second goes to Ignite Fireworks or a Fortitude area spell against groups, to Telekinetic Maneuver against one strong enemy, or to Invisibility when he intends to approach unseen. No Fortitude or Will spell at this rank is graded above B, so he needs only one of Spray of Salt and Disorienting Flash and relies on Fear at rank 1 and Slow at rank 3 for those saves. Blur and Gecko Grip enter his spellbook at level 7 as studious spells.",
3: "Haste and Slow fill both slots until he has more of them. Vampiric Feast and Agonizing Despair are the strongest single-target spells, against Fortitude and Will respectively. Blazing Dive carries him into a fight with a Strike, and Echo Jump takes him out of reach after one. Roaring Applause provokes his Reactive Strike against anything that is not mindless. No attack spell at this rank is graded above B, so when AC is an enemy's weakest defence he casts Shocking Grasp from a rank-3 slot. Lightning Bolt becomes his line for Sprinting Spellstrike at level 12, and Ghostly Weapon enters his spellbook at 11 as a studious spell.",
4: "Invisibility belongs in a rank-4 slot for a fight in which Cyrus wants to attack unseen. Force Rain is the most adaptable damage spell, since it can be cast with one, two or three actions. Freezing Touch, Mantis's Grasp and Grasp of the Deep give him a spell against Fortitude, Reflex and Will. Fly and Translocate become studious spells at level 13.",
5: "Weight of the World and Wall of Stone are the two spells he prepares most often at this rank, with Wave of Despair in place of one of them against groups. Blazing Fissure is the line for Sprinting Spellstrike when knocking enemies prone matters more than damage. Every defence has an A-graded spell at this rank.",
6: "Living Thunderbolt is for fights in which he expects to use Sprinting Spellstrike. Chain Lightning is the dependable damage spell, and Disintegrate takes its place when Sure Strike or an off-guard target makes a hit likely. Missed Cue and Necrotize are his spells against Will and Fortitude.",
7: "True Target is the spell for a single powerful enemy, and Frigid Flurry is the line. Haste from a rank-7 slot affects six creatures, which makes it the strongest spell with which to open a fight for everyone on his side. The spells that belong to this rank target Reflex and AC, so against Fortitude and Will he casts Necrotize and Missed Cue from these slots.",
8: "Roar of Freedom is the best use Cyrus has for a third action, giving area damage, a penalty to enemies and temporary Hit Points to allies. Disappearance makes every Strike land on an off-guard target. Power Word Stun takes actions from a powerful enemy for one action with no save, which leaves two for a Spellstrike. Polar Ray is the spell against AC, and its drain lowers the target's Fortitude save for an Arctic Rift or Boil Blood that follows. Reflex has no A-graded spell at this rank, so Frigid Flurry cast from a rank-8 slot takes that place.",
9: "Cyrus gains rank-9 slots at level 17. Foresight goes on whichever ally the most dangerous enemy is attacking, and Remake Physiology on that enemy. No attack spell at this rank has a card, so Disintegrate cast from a rank-9 slot is the spell against AC.",
}
for _r, _t in _PREP.items():
    P[_r]['prep'] = _t
