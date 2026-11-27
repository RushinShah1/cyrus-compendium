"""Role ratings for every spell card, reviewed against one scale on 27 November 2026 and applied last.

A rating says how well the spell does that job compared with other spells of its own rank, cast from a slot of that rank.
0 means it does not do the job. 1 narrow or weak, 2 situational or mediocre, 3 useful or solid, 4 versatile or strong,
5 universal or exceptional, 6 transformative: a handful of spells that change how a fight or a problem works, or, for
damage, the clear outliers at their rank.

Damage is measured, not judged.
Step 1, damage per target: average damage on a hit or a failed save, plus persistent damage for two rounds, multiplied by
0.85 when a successful save takes nothing and by 0.75 when the spell needs both a hit and a failed save, divided by 2d6 (7)
per spell rank. Under 45% is 1, 45% to 80% is 2, 80% to 105% is 3, 105% to 120% is 4, 120% to 160% is 5, and more than
160% is 6. So 2d6 per rank against one target is 3.
Lasting spells: a cloud or zone is counted for what a creature caught in it cannot avoid, which is its damage when it
appears and its damage at the start of that creature's next turn. Damage for ending a turn in it or crossing it is not
counted. Damage he repeats by spending an action each round (Sustain, popping a blister) is
counted for one extra round at half.
Step 2, area: add one star for a small area or a few targets (10-foot burst, cones up to 30 feet, lines, emanations up to
15 feet, two or three targets) and two for a large one (20-foot burst or bigger, 60-foot cone or bigger, larger
emanations, any number of targets). A single square or a 5-foot burst adds nothing. A spell under 45% per target gains one
star at most. The total stops at 6.
Step 3, narrow targets: a spell that can only be aimed at a narrow kind of target (something metal, a creature taller than
him, creatures up to a set level) is one star lower.
Spells with several action versions use the two-action version. The drained condition removes Hit Points equal to the
target's level times its value, so a spell that drains is credited with that loss against a target of the level at which
the spell is first available. Cantrips are ranked against each other, with 2d4 as 3.
Rated by hand: spells that kill outright (Power Word Kill), summons, spells that deal their damage through a Strike, and
damage that is incidental to a wall, terrain or retaliation effect (0 to 2).
Readings that needed a choice: Ignition 4, between its ranged 2d4 (3) and melee 2d6 (5). Phantom Pain 4, persistent damage
counted once because it ends when the target stops being sickened. Agitate 2, damage the target avoids by moving counted at
half. Weapon Storm 3, for a d8 or d10 weapon; a d12 weapon makes it 4. Living Thunderbolt 5, counted for two full rounds
against one creature, because the damage lasts a minute and repeats on movement he makes anyway. Draw the Lightning 3, the extra damage on his first Strike
each round counted for two rounds, then one lower for the narrow target. Heat Metal 5 and Massacre 5, each one lower for
the narrow target. Blister 4, the first blister popped counted as the cast and the second at half. Implosion 5, 4 per
target and one more for a new target each round. Awaken Entropy 4, area counted as large because the first Sustain makes
it a 20-foot burst. Purple Worm Sting 3, the venom counted for two rounds. Chromatic Ray, Elemental Breath, Prismatic Spray
and Rainbow Fumarole use the average of their random results, and Comet Charge its best option.

Control (taking actions, movement or reactions away, or reshaping the field): 5 denies actions or movement with no save or
on a successful save, or is a large solid wall; 4 does something on a success and much more on a failure, or is reliable
but brief; 3 needs a failed save for a solid effect; 2 is brief or minor; 1 only on a critical failure. Incapacitation
spells sit one step lower.
Debuff (penalties to rolls and defences, blindness, weakness): the same steps, judged by the size of the penalty, how many
targets, and whether it lands on a success.
Buff / Heal, Positioning (moving himself, allies or enemies) and Utility (problems outside a fight) are judged by how much
they change, for how long and for how many.
"""
from spell_evals_base import E

R = {
    'Disintegrating Puddle': '420000',
    'Floating Flame': '400000',
    'Rainbow Fumarole': '400000',
    'Mirror Malefactors': '503000',
    'Puff of Poison': '500000',
    'Prismatic Spray': '330000',
    'Freezing Rain': '230000',
    'Rend Magic': '201000',
    'Elemental Breath': '500000',
    'Needle Darts': '500001',
    'Live Wire': '300000',
    'Frostbite': '301000',
    'Electric Arc': '400000',
    'Void Warp': '301000',
    'Telekinetic Projectile': '500000',
    'Tangle Vine': '030000',
    'Caustic Blast': '300000',
    'Scatter Scree': '320000',
    'Daze': '210000',
    'Gale Blast': '310020',
    'Slashing Gust': '400000',
    'Timber': '400000',
    'Phase Bolt': '500000',
    'Glass Shield': '100300',
    'Warp Step': '000020',
    'Haunting Hymn': '400000',
    'Thunderstrike': '501000',
    'Dehydrate': '302000',
    'Fleet Step': '000040',
    'Tailwind': '000032',
    'Grease': '030000',
    'Befuddle': '004000',
    'Briny Bolt': '324000',
    'Shocking Grasp': '600000',
    'Force Barrage': '300000',
    'Breathe Fire': '400000',
    'Dizzying Colors': '033000',
    'Pummeling Rubble': '300010',
    'Gust of Wind': '030010',
    'Curse of Slippery Steps': '020000',
    'Hydraulic Push': '500020',
    'Grim Tendrils': '300000',
    'Horizon Thunder Sphere': '500000',
    'Jump': '000020',
    'Conductive Weapon': '000300',
    'Friendfetch': '000030',
    'Acidic Burst': '400000',
    'Agitate': '220000',
    'Chilling Spray': '320000',
    'Déjà Vu': '020000',
    'Draw Ire': '202000',
    'Echoing Weapon': '000100',
    'Endure': '000200',
    'Enfeeble': '004000',
    'Flourishing Flora': '201000',
    'Gravitational Pull': '010030',
    'Noxious Vapors': '301100',
    'Shockwave': '033000',
    'Sleep': '030000',
    'Wall of Shrubs': '020000',
    'Propelling Air Stream': '300030',
    'Soothe': '000400',
    'Lose the Path': '020000',
    'Phantom Pain': '403000',
    'Acid Grip': '420040',
    'Invisibility': '000406',
    'Sudden Bolt': '600000',
    'Acid Arrow': '500000',
    'Laughing Fit': '040000',
    'Revealing Light': '003003',
    'Noise Blast': '301000',
    'Dimensional Drop': '140000',
    'Dispel Magic': '000005',
    'Blur': '000300',
    'Enlarge': '000400',
    'Blood Vendetta': '302000',
    'Animated Assault': '400000',
    'Ash Cloud': '211000',
    'Charitable Urge': '030000',
    'Exploding Earth': '510000',
    'Phantasmal Treasure': '020000',
    'Sticky Fire': '301000',
    'Spray of Salt': '400000',
    'Blood Runs Cold': '230000',
    'Unrelenting Gravity': '030010',
    'Disorienting Flash': '302000',
    'Ignite Fireworks': '303000',
    'Slow': '050000',
    'Time Jump': '000050',
    'Lightning Bolt': '600000',
    'Fireball': '500000',
    'Cave Fangs': '530000',
    'Blindness': '004000',
    'Paralyze': '040000',
    'Blister Bomb': '005000',
    'Magnetic Acceleration': '300000',
    'Widow’s Bite': '304000',
    "Eagle's Cry": '404000',
    'Agonizing Despair': '204000',
    'Dive and Breach': '300040',
    'Gravity Well': '020040',
    'Hypnotize': '030000',
    'Impending Doom': '323000',
    'Organsight': '200100',
    'Stinking Cloud': '044000',
    'Vampiric Feast': '300200',
    'Echo Jump': '400030',
    'Blazing Dive': '400030',
    'Magical Fetters': '033000',
    'Roaring Applause': '040000',
    'Skyglass Prison': '040000',
    'Heroism': '000400',
    'Begone': '010030',
    'Vision of Death': '304000',
    'Containment': '040300',
    'Life-Draining Roots': '400200',
    'Grasping Earth': '240000',
    'Chromatic Ray': '501000',
    'Draw the Lightning': '300300',
    'Grasp of the Deep': '230000',
    'Ice Storm': '420000',
    'Rust Cloud': '510000',
    'Vampiric Maiden': '230100',
    'Weapon Storm': '300000',
    'Sanguine Mist': '400100',
    "Mantis's Grasp": '330000',
    'Freezing Touch': '330000',
    'Friends to Foes': '204000',
    'Lost Things Returned': '040000',
    'Weight of the World': '253000',
    'Glacial Skewer': '320030',
    'Blazing Fissure': '430000',
    'Tornadic Gale': '420030',
    'Howling Blizzard': '520000',
    'Impaling Spike': '330000',
    'Corrosive Muck': '430000',
    'Banishment': '030000',
    'Acid Storm': '200000',
    'Blink Charge': '200040',
    'Grisly Growths': '302000',
    'Slither': '240000',
    'Stagnate Time': '040000',
    'Toxic Cloud': '400000',
    'Wall of Ice': '040000',
    'Blinding Foam': '304000',
    'Blood Feast': '500200',
    'Plasma Whirl': '400000',
    'Disintegrate': '400003',
    'Silver Spear': '300000',
    'Lignify': '040000',
    'Cast into Time': '402000',
    'Cursed Metamorphosis': '030000',
    'Dominate': '040000',
    'Necrotize': '303000',
    "Poltergeist's Fury": '200000',
    'Vampiric Exsanguination': '400200',
    'Vibrant Pattern': '033000',
    'Vitrifying Blast': '333000',
    'Wall of Metal': '040000',
    'Awaken Entropy': '400000',
    'Phantom Orchestra': '400000',
    'Missed Cue': '344000',
    'Curse of the Toad Prince': '040000',
    'Scintillating Safeguard': '000400',
    'Beheading Buzz Saw': '400000',
    'Eclipse Burst': '600000',
    'Telekinetic Bombardment': '430000',
    'Comet Charge': '300050',
    'Heaving Earth': '530020',
    'Power Word Blind': '035000',
    'Visions of Danger': '620000',
    'Arctic Rift': '430000',
    'Uncontrollable Dance': '044000',
    'Boil Blood': '503000',
    'Earthquake': '440000',
    'Whirlpool': '530000',
    'Polar Ray': '504000',
    'Metallic Meteorite Glyph': '300000',
    'Phantasmagoria': '540000',
    'Implosion': '500000',
    'Disappearance': '000606',
    'Defy the Gods': '205000',
    'Incarnate Tempest of Shades': '214000',
    'Heat Metal': '500000',
    'Inevitable Disaster': '500000',
    'Shadow Blast': '300000',
    'Chain Lightning': '600000',
    'Spirit Blast': '500000',
    'Frigid Flurry': '600050',
    'Spirit Song': '530000',
    'Falling Stars': '620000',
}

for _n, _r in R.items():
    _old, _g, _ev = E[_n]
    E[_n] = (_r, _g, _ev)
