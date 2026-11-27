"""Evaluations rewritten to one standard, rank by rank. Applied last.

Standard for a spell worth considering (S, A or B):
  paragraph 1 - what the spell is for (the defence it targets and its role), what it does, its rider and its
                heightening, and what it does inside Cyrus's turn: Spellstrike payload, Expansive area, direct cast,
                reaction or third action;
  paragraph 2 - how it compares with the other spells that fill the same niche at the same rank (or lower-rank
                spells heightened to it), and the place it earns: default preparation, spellbook pick for coverage,
                scroll or wand, or none.
A C or D spell gets one short paragraph: its role and why it does not earn a place.
No rules explanations that apply to every spell, no reference to other pages, printings, the party or the campaign.
Paragraphs are separated by a blank line.
"""
from spell_evals_base import E


def w(name, text, grades=None, ratings=None):
    r, g, _ = E[name]
    E[name] = (ratings or r, grades or g, text.strip())


# ───────────────────────── rank 2 ─────────────────────────
w('Acid Grip', """As a Reflex-targeting single-target option, Acid Grip deals modest damage (2d8 acid plus 1d6 persistent acid) and moves the target in a direction Cyrus chooses: 5 feet on a success, 10 on a failure and 20 on a critical failure. The persistent acid also takes 10 feet off the target's Speed. Through Spellstrike it turns a Strike into a reposition, pulling an enemy into a flank, off an ally or out of a doorway, and it works just as well cast from 120 feet. Both parts of the damage improve every two ranks.

Compared with the other rank-2 payloads it deals about half the damage of Sudden Bolt, but it is the only one that still does something useful when the target saves. That reliability makes it the default rank-2 preparation.""")

w('Invisibility', """As a positioning and utility spell, Invisibility makes one creature invisible for 10 minutes and ends when that creature takes a hostile action. At rank 2 it is a scouting, infiltration and escape tool. Heightened to rank 4 it lasts a minute and survives hostile actions, so Cyrus fights unseen: enemies are off-guard to his Strikes, which turns on Laughing Shadow's extra damage, and they need a flat check to target him at all.

No other rank-2 spell does the same job, and it is only on the arcane and occult lists. The rank-2 version suits a wand or scroll as well as a slot. The rank-4 version is one of his best buffs to cast before a fight, until Dimensional Disappearance at level 10 gives a similar effect.""")

w('Telekinetic Maneuver', """As an AC-targeting control option, Telekinetic Maneuver uses a spell attack roll in place of an Athletics check to Disarm, Shove, Reposition or Trip a creature within 60 feet. Through Spellstrike the Strike's result decides the manoeuvre as well, so one activity deals weapon damage and trips or moves the target, with no separate Athletics action. A tripped target is off-guard and provokes Reactive Strike when it stands. The spell deals no damage of its own and does not heighten.

Compared with the attack-roll damage spells at this rank it trades their damage for a manoeuvre on every hit, which suits a reach weapon. It is the control alternative to Acid Grip when AC is the weaker defence.""")

w('Blazing Bolt', """As an AC-targeting damage option, Blazing Bolt deals 4d6 fire through Spellstrike and gains 2d6 per rank. Cast directly with three actions it fires a ray at each of three creatures.

Compared with Briny Bolt heightened to the same rank it deals the same damage without the blinded rider, and fire is resisted more often than bludgeoning. It earns a place only as a second damage type for attack payloads, or for the three-ray version on a turn when Cyrus cannot reach melee.""")

w('Sudden Bolt', """As a Reflex-targeting single-target damage option, Sudden Bolt deals 4d12 electricity (26 on average) with a basic save, the highest single-target damage at rank 2, and gains 1d12 per rank. Because it uses a save, the damage still applies when the Strike misses. It has no rider.

Compared with Acid Grip it deals roughly twice the damage and nothing else, and it is well ahead of Thunderstrike heightened to rank 2. It is the pick when a rank-2 slot is wanted purely for damage against a target with weak Reflex.""")

w('Acid Arrow', """As an AC-targeting damage option, Acid Arrow deals 3d8 acid plus 1d6 persistent acid on a hit and improves only every two ranks. Briny Bolt and Blazing Bolt gain damage every rank, so it falls behind in any higher slot, and its only claim to a place is acid as a damage type.""")

w('Disintegrating Puddle', """As an AC-targeting damage option, Disintegrating Puddle deals 2d12 acid on a hit and leaves acid in the target's space and every adjacent space for a minute, dealing 1d4 to creatures that enter or start their turn there. Its range is 30 feet and both parts improve every two ranks.

Compared with the other attack payloads at this rank its initial damage is similar, and the puddle is the reason to take it: at a doorway or chokepoint it damages everything that comes through. In open ground enemies step out of it, and allies fighting next to the target stand in it too.""")

w('Laughing Fit', """As a Will-targeting control option, Laughing Fit stops a living creature from using reactions even on a successful save, slows it by one action on a failure, and on a critical failure knocks it prone and costs it a whole round. It must be sustained each turn. As a mental effect it does nothing to mindless creatures.

Compared with the other rank-2 Will spells it has the most useful success effect for a melee group, because it switches off an enemy's reaction for as long as it is sustained. The sustain action competes with recharging Spellstrike, so it suits a fight against one dangerous enemy and not routine use.""")

w('Stupefy', """As a Will-targeting debuff, Stupefy makes the target stupefied 1 until the start of Cyrus's next turn on a success and stupefied 2 for a minute on a failure, which hampers a spellcaster and lowers its Will saves. The success effect is too brief to matter, and Fear from a rank-1 slot is the broader debuff.""")

w('Revealing Light', """As a Reflex-targeting area debuff, Revealing Light dazzles every creature in a 10-foot burst for 2 rounds on a success, a minute on a failure and 10 minutes on a critical failure, and deals no damage. Invisible creatures in the area become merely concealed, and other concealment is removed. Its range is 120 feet.

Compared with Ignite Fireworks it dazzles for longer and answers invisibility, but adds no damage. Its main job is a specific problem, so it is better carried as a scroll than prepared, unless invisible enemies are expected.""")

w('Noise Blast', """As a Fortitude-targeting area option, Noise Blast deals respectable damage (2d10 sonic) with a very minor rider: creatures that fail are deafened for a round. A critical failure also stuns for one action. Its 10-foot burst works with Expansive Spellstrike when it can catch several enemies without hitting allies, and its 30-foot range limits it as a direct cast. Heightened damage of 1d10 per rank is solid for an area spell, but not outstanding.

Compared with the other Fortitude area spells at this rank, Spray of Salt deals slightly more damage in a cone that is easier to aim away from allies, and Disorienting Flash deals the same damage with twice the range, a dazzled rider and three sizes to choose from. The stun on a critical failure is Noise Blast's only advantage, which makes it the third choice of the three.""")

w('Dimensional Drop', """As a Reflex-targeting control option, Dimensional Drop sends a creature standing on the ground through a portal that drops it back onto its own space: 10 feet on a success, 20 on a failure and 40 on a critical failure. It takes falling damage and, like any creature damaged by a fall, lands prone, so even a successful save leaves the target prone. Through Spellstrike that is a Strike followed by an enemy that is off-guard and provokes Reactive Strike when it stands. From rank 5 it targets five creatures. Its damage is small and does not improve.

Compared with Telekinetic Maneuver it knocks prone on a save and not on the Strike's roll, so it still works when the Strike misses, and compared with Unrelenting Gravity it does so on a success as well as a failure. It cannot target a creature in the air, and a creature with a fly Speed can use its reaction to Arrest the Fall against his spell DC.""", grades='ADD', ratings='240000')

w('Dispel Magic', """As a utility spell, Dispel Magic attempts to counteract one spell effect, or suppresses a magic item for 10 minutes. The counteract check depends on the rank it is cast at, so a rank-2 copy only handles low-rank effects and the useful copy is the one in a high slot.

Nothing else replaces it when a fight turns on a single enemy spell, but that is rare enough that a scroll of the right rank is a better way to carry it than a daily slot.""")

w('See the Unseen', """As a utility spell, See the Unseen lets Cyrus see invisible creatures as concealed for 10 minutes, and see incorporeal creatures through nearby surfaces. From rank 5 it lasts 8 hours.

It improves only his own sight, where Revealing Light exposes an invisible creature to everyone. Its long duration makes it a wand or scroll spell: a rank-5 wand covers a whole day without a slot.""")

w('Mirror Image', """As a defensive buff, Mirror Image gives Cyrus three images for a minute. An attack that would hit him has a 3 in 4 chance of destroying an image, with the odds falling as images are lost, and a miss that is not a critical failure also destroys one. Against an enemy that makes several attacks a turn it prevents two or three hits.

Compared with Blur, which gives a 20 per cent miss chance for the whole minute, it protects more against a few large hits and runs out sooner against many small ones. It takes two actions and only protects the caster, so it is worth a slot only before a fight in which he expects to be the main target.""")

w('Resist Energy', """As a defensive buff, Resist Energy gives one creature resistance 5 to acid, cold, electricity, fire or sonic damage for 10 minutes. At rank 4 it is resistance 10 on two creatures, and at rank 7 resistance 15 on five.

It is only worth casting when the damage type is known in advance, which makes it a scroll or wand spell, and a prepared one only on a day with a known energy threat.""")

w('Blur', """As a defensive buff, Blur makes one creature concealed for a minute, so every attack against it has a 20 per cent chance to miss. The concealment cannot be used to Hide.

Its value to Cyrus arrives at level 7, when it becomes a studious spell: it enters his spellbook without being learned, and casting it lets him enter Arcane Cascade as a free action, so two actions on an opening turn give both the stance and the defence. Before level 7 it is an ordinary buff that Mirror Image matches.""")

w("Loose Time's Arrow", """As a positioning buff, Loose Time's Arrow makes up to six creatures within 30 feet quickened until the end of Cyrus's next turn, with the extra action limited to a Step or a Stride. It gives the whole group one free move at the start of a fight.

Haste at rank 3 does far more for one creature over a whole fight. This spell is for the opening round on a large map, when everyone needs to close distance together.""")

w('Enlarge', """As a buff, Enlarge makes a creature Large for 5 minutes: its reach increases by 5 feet, its melee Strikes gain a +2 status bonus to damage, and it is clumsy 1. At rank 4 the target becomes Huge, with +4 damage and 10 feet of extra reach.

On Cyrus it extends his reach to 15 feet, which widens the area Reactive Strike covers, at the cost of clumsy 1 and a larger space that is harder to place for flanking and teleporting. It does most on a melee ally, and its duration suits a scroll or wand used before a fight.""")

w('Gecko Grip', """As a mobility spell, Gecko Grip gives a creature a climb Speed equal to its Speed for 10 minutes, or an hour from rank 5. Cyrus can reach high ground or fight from a wall without Athletics checks.

Like Blur it becomes a studious spell at level 7, entering his spellbook and granting a free Arcane Cascade when cast. It is prepared for a known climb or a vertical battlefield and otherwise stays in the book.""")

w('Hidebound', """As a defensive reaction, Hidebound gives a creature within 60 feet resistance 5 to physical damage when it is hit by a Strike. The resistance lasts until the start of that creature's next turn, so it also reduces every further Strike against it that round, and it rises by 3 every two ranks.

Compared with Warping Pull it covers only Strikes and stops less of a single hit, but it keeps working for the whole round and does not move the ally. It uses his reaction, so from level 6 it competes with Reactive Strike. It costs no action on his turn, which makes a low-rank slot a cheap place to keep it, and Axuma's Awakening at 11 can provide it without a slot. A scroll or wand is a poor way to carry a reaction, because he would have to hold it ready in a hand.""")

w('Warping Pull', """As a defensive reaction, Warping Pull triggers when any effect would damage an ally within 30 feet. It teleports the ally up to 10 feet towards Cyrus and gives it resistance 5 to that damage, rising by 5 every two ranks. It works against spells and area damage as well as Strikes, and the teleport can take the ally out of an enemy's reach or into a flanking position.

Compared with Hidebound it reduces more of a single hit and improves faster, but it applies to one effect only. It also competes with Reactive Strike for his reaction from level 6, and Axuma's Awakening at 11 can provide it without a slot.""")

w('Water Breathing', """As a utility spell, Water Breathing lets up to five creatures breathe underwater for an hour, for 8 hours from rank 3 and for the whole day from rank 4. It solves one problem completely, and is bought as a scroll when water is known to be ahead.""")

w('Blood Vendetta', """As a Will-targeting reaction, Blood Vendetta triggers when a creature deals piercing, slashing or bleed damage to Cyrus. The attacker takes 2d6 persistent bleed damage, halved on a successful save, and on a failure it also has weakness 1 to piercing and slashing until the bleeding stops. The bleed rises by 2d6 every two ranks.

It is damage for no action on his turn, but he has to be hit first, and from level 6 Reactive Strike usually makes better use of the reaction. Creatures that cannot bleed are immune.""")

w('Embed Message', """As a utility spell, Embed Message stores a message of up to 25 words on an object or willing creature, delivered by illusory text and a voice when a chosen trigger occurs nearby. It has no use in a fight and is a tool for signals and warnings. Aspera's stave is planned to carry it, which is a better home for it than a slot.""")

w('Propulsive Breeze', """As a positioning reaction, Propulsive Breeze pushes an ally within 60 feet a further 15 feet at the end of its Stride or Leap, in the direction it was already moving. It can carry a melee ally into reach in a single action.

It uses his reaction on an ally's turn, so from level 6 it costs him Reactive Strike for that round, and it only extends movement in a straight line. It is a minor pick for a low-rank slot on a large map.""")

w('Pyrefowl Rebuke', """As a defensive reaction, Pyrefowl Rebuke deals 1d6 fire to a creature that hits Cyrus from within 10 feet and flies him 10 feet directly away from it. The damage is negligible, and the movement takes him away from an enemy he wants inside his reach, so it works against the way he fights.""")

w('Animated Assault', """As a Reflex-targeting area option, Animated Assault deals 2d10 bludgeoning in a 10-foot burst, and 1d10 again each round it is sustained. The first hit is ordinary for the rank, and the repeat damage needs an action every turn that Cyrus spends on recharging Spellstrike, so Ignite Fireworks or Vomit Swarm is the better Reflex area spell.""")

w('Ash Cloud', """As a Fortitude-targeting area option, Ash Cloud fills a 20-foot burst with smoke for a minute, dealing 2d4 fire to creatures that start their turn inside and acting as difficult terrain for flyers. It takes three actions, so it cannot be combined with Spellstrike, and the damage is low for a whole turn.""")

w('Charitable Urge', """As a Will-targeting control option, Charitable Urge stuns the target for one action on a successful save. On a failure the target must begin its next turn by handing an item to the nearest creature, or lose the round if all it holds is the weapon it is fighting with. It does nothing to a creature that carries no items.

Compared with Laughing Fit it costs the target an action on a success with no sustain, which is strong for the rank. It has the incapacitation trait, so from a rank-2 slot a target above level 4 treats a success as a critical success and is unaffected. That limits it to enemies of low level unless it is heightened.""")

w('Darkness', """As a utility spell, Darkness fills a 20-foot burst with magical darkness for a minute. Cyrus has no darkvision, so it blinds him as much as his enemies, and it takes three actions. Its only use is to cover a retreat.""")

w('Darkvision', """As a utility buff, Darkvision gives Cyrus darkvision for an hour. As a human he has neither darkvision nor low-light vision, so without it he fights in the dark by a light source or not at all. From rank 3 it can be cast on another creature, and from rank 5 it lasts until his next daily preparations.

Its duration makes a wand the best way to carry it. A prepared slot is for a day known to be spent underground or at night.""")

w('Deafness', """As a Fortitude-targeting debuff, Deafness deafens one creature, for a round on a success and 10 minutes on a failure. Deafened hampers only auditory actions and Perception, which rarely decides a fight.""")

w('Entangling Flora', """As a Reflex-targeting area control option, Entangling Flora turns a 20-foot burst into difficult terrain for a minute. Creatures that start their turn inside must save or take a 10-foot penalty to their Speeds, and are immobilised for a round on a critical failure. It needs no sustaining, and it affects only squares that contain plants.

Compared with Web it takes two actions and covers a larger area, but its hold on each creature is weaker. A 20-foot burst is too large to place through Expansive Spellstrike without covering Cyrus and his allies, so it is cast directly to hold a group back while the rest of the fight is dealt with.""")

w('Environmental Endurance', """As a utility spell, Environmental Endurance protects one creature from severe heat or severe cold until the next daily preparations, from both at rank 3 and from extreme temperatures at rank 5. It matters only on an expedition into such a climate, where a wand or scroll covers it.""")

w('Exploding Earth', """As an AC-targeting damage option, Exploding Earth deals 4d6 bludgeoning plus 1d6 splash, and a critical hit can knock the target prone. It improves only every two ranks, half the rate of Briny Bolt, and the splash also hits allies standing next to the target.""")

w('False Vitality', """As a defensive buff, False Vitality gives Cyrus 10 temporary Hit Points for 8 hours, plus 3 for each rank above 2. Cast in the morning, it adds a buffer to the first fight of the day for no action in combat.

It affects only the caster, and the Hit Points do not return once lost. A wand is the best way to carry it, since it then costs no slot at all.""")

w('Floating Flame', """As a Reflex-targeting damage option, Floating Flame deals 3d6 fire to creatures in one square and can be moved 10 feet each round by sustaining it, damaging whatever it passes through. The sustain action competes with recharging Spellstrike every turn, which makes it a poor fit for Cyrus.""")

w('Heat Metal', """As a Reflex-targeting single-target damage option, Heat Metal deals 4d6 fire plus 2d4 persistent fire to a creature made of metal, or to one wearing or holding a metal item. The persistent damage belongs to the item, so it continues until a flat check ends it or the creature lets go, and releasing a held item improves its save by one degree. It does nothing to a target without metal. The damage rises by 2d6 and 1d4 per rank.

Compared with Sudden Bolt it deals less at once and more over time, and it needs the right target. Against an armoured enemy it is a strong payload; as a general pick, Sudden Bolt or Acid Grip is safer.""")

w('Humanoid Form', """As a utility spell, Humanoid Form changes Cyrus's appearance to that of another Small or Medium humanoid for 10 minutes, without changing his statistics. It is a disguise that holds up to touch, which suits infiltration, and it is carried as a scroll.""")

w('Illusory Creature', """As a utility spell, Illusory Creature creates an illusion of a Large or smaller creature that acts when the spell is sustained, can flank, and deals a little mental damage. It ends when it is hit or fails a save. In a fight the sustain action competes with recharging Spellstrike. Outside a fight it is a convincing decoy or distraction, which is the reason to carry a scroll.""")

w('Knock', """As a utility spell, Knock gives a +4 status bonus to open a door, lock or container, and lets Cyrus attempt the Thievery check as part of the casting, adding his level even though he is untrained. It is his way past a lock without breaking it. A scroll is the right way to carry it, since locks rarely appear on a schedule.""")

w('Lucky Number', """As a utility buff, Lucky Number is cast during daily preparations. Cyrus rolls 1d10, and once that day, when a d20 for an attack, save or skill check shows that number, he can use a reaction to reroll it. The chance of it applying to a roll that matters is small, so it is worth having only from a wand, where it costs no slot.""")

w('Mist', """As a utility spell, Mist conceals everything inside a 20-foot burst for a minute, and everything outside it from those within. It covers a retreat or blunts ranged attackers, but it hampers the party's own attacks equally and takes three actions.""")

w('Oaken Resilience', """As a defensive buff, Oaken Resilience gives resistance 2 to bludgeoning and piercing damage and weakness 3 to fire. The resistance is too small to justify a slot, and the weakness is a real cost.""")

w('Phantasmal Treasure', """As a Will-targeting control option, Phantasmal Treasure fascinates a living creature with an illusion, for its own turn on a success and for a minute on a failure. Fascination ends as soon as anyone acts against the target, and the target can disbelieve the illusion, so it removes one enemy only for as long as the party ignores it.""")

w('Shrink', """As a utility spell, Shrink makes a creature Tiny for 5 minutes, with a reach of 0 feet. It helps one creature through a small gap or out of sight, and it removes Cyrus's reach while it lasts.""")

w('Splinter Volley', """As an AC-targeting damage option, Splinter Volley deals 4d6 piercing, with a little bleed on a critical hit, and a third action sends it at a second target. It improves by 4d6 every two ranks, the same rate as Briny Bolt, without the blinded rider, so it offers piercing as a damage type and nothing else.""")

w('Sticky Fire', """As an AC-targeting debuff, Sticky Fire deals 1d8 fire and 1d8 persistent fire on a hit and leaves the target enfeebled 1 until the fire goes out. Its damage is low for the rank and improves only every two ranks, so it is a minor debuff that lasts only as long as a flat check allows.""")

w('Summon Elemental', """As a summoning spell, Summon Elemental brings a low-level elemental that acts only when the spell is sustained. It takes three actions to cast and one on every turn after, which leaves no room for Spellstrike and recharging.""")

w('Translate', """As a utility spell, Translate lets one creature understand a single language for an hour, speak it from rank 3, and covers ten creatures from rank 4. When no one shares a language it is the only way to talk or read, so a scroll or wand is worth carrying.""")

w('Vomit Swarm', """As a Reflex-targeting area option, Vomit Swarm deals 2d8 piercing in a 30-foot cone, and creatures that fail are sickened 1. Through Expansive Spellstrike a cone is the easiest area to point away from allies, and sickened lowers the AC, attacks and saves of everything it catches. The damage rises by 1d8 per rank.

Compared with Ignite Fireworks it deals the same damage in a larger area, and its rider is the stronger condition, but the rider needs a failed save where Ignite Fireworks dazzles on a success. It is the better pick against groups likely to fail a Reflex save.""")

w('Water Walk', """As a utility spell, Water Walk lets one creature walk on liquid for 10 minutes, or ten creatures for an hour from rank 4. It is a scroll for a river or coastal crossing.""")

w('Web', """As a Reflex-targeting area control option, Web fills a 10-foot burst with webbing for a minute. The squares are difficult terrain, and a creature that moves in them must pass an Athletics check or a Reflex save or lose Speed, and is immobilised on a critical failure. Squares can be cleared with slashing or fire damage.

It takes three actions, so it cannot be combined with Spellstrike and costs a whole turn. Compared with Entangling Flora it holds each creature more firmly in a smaller area. It is worth that turn at a chokepoint and rarely elsewhere.""")

w('Marvelous Mount', """As a utility spell, Marvelous Mount conjures a mount with a Speed of 40 feet for one creature for 8 hours, faster and able to cross water at higher ranks. It is a travel convenience with no use in a fight.""")

w('Blazing Armory', """As a utility spell, Blazing Armory creates a +1 striking weapon that deals fire damage in a creature's free hand for 5 minutes. Cyrus fights with his own weapon in both hands, so it does nothing for him.""")

w('Binding Muzzle', """As a Fortitude-targeting control option, Binding Muzzle clamps a creature's mouth shut, so it cannot bite, use a breath weapon or drink: for a round on a success and for a minute on a failure, when spells that need speech also become unreliable. Its range is 100 feet, and from rank 5 it targets five creatures.

It does nothing to an enemy that fights with weapons or claws, so it is a narrow answer to creatures that rely on a bite or a breath weapon. That makes it a scroll to carry and not a daily preparation.""")

w('Spray of Salt', """As a Fortitude-targeting area option, Spray of Salt deals 5d4 acid in a 15-foot cone, the highest Fortitude area damage at rank 2, and gains 2d4 per rank. Creatures with the ooze, unholy or water trait also take persistent spirit damage on a failure, and it has no rider against anything else. Through Expansive Spellstrike a short cone is easy to point away from allies, though it rarely catches more than two or three enemies.

Compared with Disorienting Flash and Noise Blast it deals slightly more damage in a smaller, safer area and gives up their riders. It is the pick when the slot is wanted for Fortitude damage; Disorienting Flash is the pick when flexibility matters more.""")

w('Blood Runs Cold', """As a Fortitude-targeting single-target option, Blood Runs Cold deals 1d6 persistent cold damage and slows the target by one action for a round on a failure, or until the cold ends on a critical failure. A success halves the damage and does not slow. The damage rises by 1d6 every two ranks.

Compared with Slow at rank 3, which costs the target an action even on a success, it needs a failed save to do the same, and its damage is low. It is a Fortitude payload for a rank-2 slot before Slow is available, and has little use after.""")

w('Unrelenting Gravity', """As a Fortitude-targeting control option, Unrelenting Gravity makes the target encumbered for a round on a success, which is clumsy 1 and a 10-foot penalty to Speed, and knocks it prone as well on a failure. A flying creature that fails falls. From rank 4 it targets five creatures.

Compared with Dimensional Drop, which leaves a grounded target prone even on a successful Reflex save, it is the weaker way to put an enemy on the floor. Its use is against targets with weak Fortitude or targets in the air.""")

w('Disorienting Flash', """As a Fortitude-targeting area option, Disorienting Flash deals modest sonic damage and dazzles creatures that fail until the end of Cyrus's next turn. Its size depends on the actions spent: one action affects a single square for 1d10, two actions a 10-foot burst for 2d10, and three actions a 20-foot burst for 2d10 that also deafens. The two-action version is the Spellstrike payload, the one-action version fits after a Spellstrike on the same turn, and the three-action version is a direct cast at a group within 60 feet. Each version gains 1d10 per rank.

Compared with Spray of Salt it deals slightly less damage in a burst that is harder to keep off allies, and its dazzled rider needs a failed save where Ignite Fireworks dazzles on a success. Its advantage is three sizes from one slot.""")

w('Ignite Fireworks', """As a Reflex-targeting area option, Ignite Fireworks deals light damage (1d8 fire and 1d8 sonic) in a 10-foot burst and dazzles every creature that does not critically succeed: for a round on a success, 3 rounds on a failure and a minute on a critical failure. A dazzled creature treats everything as concealed, so each of its attacks has a 20 per cent chance to miss. Each damage type rises by 1d8 every two ranks, and its range is 60 feet.

Compared with Vomit Swarm it deals the same damage in a smaller area, but its rider applies on a successful save, which makes it the more reliable debuff. Compared with Revealing Light it dazzles for less time and adds damage. Through Expansive Spellstrike a 10-foot burst needs care when allies stand beside the target.""")


# ───────────── corrections outside rank 2 ─────────────
# Scatter Scree's area is two contiguous 5-foot cubes, which Expansive Spellstrike does not cover.
w('Scatter Scree', """As a Reflex-targeting cantrip, Scatter Scree deals light damage (2d4 bludgeoning, rising by 1d4 per rank) in two adjacent 5-foot cubes and leaves the ground there as difficult terrain for a minute. Its area is not a burst, cone or line, so through Spellstrike it affects only the target and the target's space, even with Expansive Spellstrike. Cast directly from 30 feet it slows movement through a doorway or corridor. The damage is too low for regular use, and casting it again ends the earlier one.""")
