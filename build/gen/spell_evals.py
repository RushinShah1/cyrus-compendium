import re
# Ratings: Damage, Control, Debuff, Buff/Heal, Positioning, Utility  (0-5, 6 = exceptional / purple)
# Grades: Spellbook (or Familiar for occult cantrips), Scroll, Wand.  '-' = not applicable.
from spell_evals_base import E, s

# ───────────── Cantrips ─────────────
s('Gouging Claw', '500000', 'S--', "Gouging Claw is Cyrus's default Spellstrike payload and should be prepared every day. Because it is an attack spell, Spellstrike resolves it with Aspera's attack roll, so its accuracy matches his weapon rather than his lower spell attack, and its touch range becomes Aspera's 10-foot reach. The persistent bleed keeps working while he spends the next turn recharging, which gives it the best sustained damage of any cantrip he can deliver. Its weakness is creatures immune to bleed, such as constructs, elementals and most undead, where Ignition or Needle Darts should take its place.")
s('Ignition', '400000', 'A--', "Ignition is the best second attack cantrip for Cyrus. When the target is within his melee reach it uses d6s instead of d4s, and Aspera's 10-foot reach counts, so Spellstrike always delivers the stronger version. Fire is the most common weakness among undead, trolls, swarms and plant creatures, which makes Ignition the natural swap when Gouging Claw's bleed would be wasted. If cantrip slots are tight, a Flaming Star spellheart can provide Ignition instead.")
s('Needle Darts', '400001', 'A--', "Needle Darts deals piercing damage and takes on the properties of the metal Cyrus casts it with. Carrying a silver piece and a cold-iron piece lets him exploit the weaknesses of devils, demons, fey and lycanthropes without separate weapons. Its 60-foot range also makes it his best direct cast when nothing is within Aspera's reach. It scales slightly behind Gouging Claw on raw damage, so prepare it when the enemy roster suggests a material weakness or ranged fighting.")
s('Live Wire', '400000', 'B--', "Live Wire still deals its electricity damage on a failed attack roll, so a Spellstrike that misses without critically failing still does something. However, it only heightens every two ranks, so from about level 7 it falls behind Gouging Claw and Ignition on expected damage. It is a reasonable early choice and an option against foes with very high AC, but it should not stay in the daily five long term.")
s('Frostbite', '310000', 'B--', "Frostbite is Cyrus's Fortitude cantrip. Because it uses a save, the target still rolls against it when Aspera's Strike misses, which makes it a dependable payload against heavily armoured foes with weak Fortitude. Its damage is lower than the attack cantrips and it depends on his spell DC, which trails a full caster's. The bludgeoning weakness on a critical failure only matters if an ally is about to hit with bludgeoning damage.")
s('Electric Arc', '300000', 'B--', "Electric Arc loses its main strength in Spellstrike, because the spell only affects the creature Cyrus hits. Its value for him is as a direct cast at two enemies from 30 feet when nothing is within reach. It is worth preparing on days when the party expects flyers or enemies behind difficult terrain, but it is not a core cantrip for a melee magus.")
s('Void Warp', '201000', 'C--', "Void Warp is a second Fortitude option that only affects living creatures, so it does nothing against the undead that Frostbite handles well. The enfeebled rider needs a critical failure against Cyrus's spell DC, which will rarely happen against appropriately levelled foes. Frostbite covers the same defence more broadly.")
s('Telekinetic Projectile', '300001', 'C--', "Telekinetic Projectile lets Cyrus choose bludgeoning, piercing or slashing damage based on the object he throws, which can get past an unusual physical resistance. It needs a loose object of 1 Bulk or less nearby, and none of the object's material properties carry over. Needle Darts does the same job with longer range and material weaknesses, so this rarely earns a cantrip slot.")
s('Tangle Vine', '030100', 'B--', "Tangle Vine deals no damage of its own, but as a Spellstrike payload Aspera still deals its damage and a hit also imposes a 10-foot Speed penalty, with a critical hit immobilising the target. That makes it useful against skirmishers that try to Step out of Cyrus's reach or run past him to the back line. It is a situational pick for fights against mobile enemies rather than a daily cantrip.")
s('Caustic Blast', '200000', 'C--', "Caustic Blast is the cheapest burst payload for Expansive Spellstrike, a 5-foot burst centred on a corner of the target's square. The damage is low and the Reflex save uses Cyrus's spell DC, so it only earns its place against swarms or tightly packed weak enemies. In most fights a single-target attack cantrip deals more total damage.")
s('Scatter Scree', '120000', 'C--', "Scatter Scree creates difficult terrain in a short line as well as dealing minor damage. With Expansive Spellstrike the line starts next to the target, which can slow a group trying to reach the party's casters. Its damage and length are both too small for regular use, and it ends if cast again.")
s('Daze', '110000', 'C--', "Daze is Cyrus's only cantrip that targets Will, and its damage is nonlethal. The stun only happens on a critical failure, which is unlikely against his spell DC. It is worth knowing for jobs where the party wants enemies alive, but it is not a combat cantrip.")
s('Shield', '000400', 'A--', "Shield costs one action and doesn't need a free hand, so Cyrus can cast it while holding Aspera in both hands. It is a sensible third action when moving or recharging isn't needed, and Shield Block can absorb a large hit or a damaging spell. Its limitation is that Shield Block uses his reaction, which he usually wants for Reactive Strike from level 6.")
s('Detect Magic', '000004', 'B--', "Detect Magic is essential for the party, but Yara and Theldren can also cast it, so Cyrus only needs it on investigation-heavy days or when the casters have chosen other cantrips. Its heightened versions reveal the strength and approximate location of magic. Magic Sense at level 12 would make it permanent if he took that feat.")
s('Figment', '010003', 'B--', "Figment creates a simple sound or image and lets Cyrus Create a Diversion with a +2 bonus. It is cheap, flexible support for scouting and infiltration, such as drawing a guard away from a door. Its effects look crude up close, so it works best as a quick distraction.")
s('Telekinetic Hand', '000003', 'C--', "Telekinetic Hand moves light unattended objects from range, which helps with traps, pressure plates and retrieving items from dangerous places. It is useful on dungeon days but rarely needed in the city and court scenes the campaign often features.")
s('Message', '000003', 'B--', "Message is one-action silent communication at 120 feet, rising to 500 feet at rank 3. It is valuable for coordinating the party during infiltration or court scenes where open discussion would give the plan away. Beyond that coordination it does little in combat.")
s('Time Sense', '000102', 'C--', "Time Sense fits Aspera's time theme, which is why it is the stave's cantrip. The +1 status bonus to a precisely timed roll rarely applies. It belongs on the stave rather than in one of Cyrus's five prepared cantrips.")

# ───────────── Rank 1 ─────────────
s('Sure Strike', '000600', 'SCC', "Sure Strike is the most important rank-1 spell a magus can prepare. For one action, the next attack roll is rolled twice using the better result and ignores concealment and circumstance penalties, which makes a high-value Spellstrike close to certain. With one or two fights a day, Cyrus's two rank-1 slots cover each fight, and the 10-minute immunity limits it to once per fight anyway, so a wand or scroll adds little. Pair it with the turn's biggest attack payload, such as Glacial Skewer or Disintegrate, rather than a cantrip.")
s('Thunderstrike', '410000', 'ACD', "Thunderstrike is a single-target basic Reflex save that heightens by a full set of dice every rank, so it stays a respectable payload from any slot. Because it uses a save, it still resolves when Aspera's Strike misses. Enemies in metal armour take a penalty to the save and become clumsy if damaged, which lowers their Reflex DC for Cyrus's Trip. It pairs well with Shocking Grasp: one targets Reflex, the other AC.")
s('Fear', '014000', 'ABB', "Fear imposes frightened 1 even on a successful save, which lowers the target's AC, saves and checks for the whole party. Through Spellstrike it costs no actions beyond the Strike, and at rank 3 it can target five creatures as a direct cast. With one or two fights a day, a wand gives a free group debuff most days. Its weakness is creatures immune to fear or mental effects, which are common among undead and constructs.")
s('Fleet Step', '000050', 'BBC', "Fleet Step grants a +30-foot status bonus to Speed for a minute. It is useful before a chase, an objective run or a fight on a large map, and it is one of the spells Arcane Shroud can apply later. Because it is a status bonus, it replaces Laughing Shadow's +5 feet rather than adding to it, so the real gain is 25 feet.")
s('Tailwind', '000042', 'CCB', "Tailwind's rank-2 version lasts eight hours, which makes it a classic wand spell. For Cyrus it is weaker than usual because it is a status bonus that overlaps Laughing Shadow's, so it only adds 5 feet while he is in stance. It is still worth the wand if he spends long periods out of stance, such as while travelling.")
s('Grease', '040020', 'BBC', "Grease is best cast normally over four squares, where any creature standing there may fall prone. Prone enemies are off-guard, which turns on Laughing Shadow's increased damage and helps the party's melee allies. The object mode can also disarm a weapon or spellcasting focus on a critical failure. As a Spellstrike payload it loses its area, so treat it as a direct-cast control spell.")
s('Befuddle', '003000', 'BCC', "Befuddle makes the target clumsy and stupefied even on a successful save. Clumsy lowers AC and the Reflex DC that Cyrus's Trip targets, so it sets up his own follow-up actions as well as the party's. Stupefied interferes with enemy spellcasting. The effects last only one round, so it is best used immediately before the party acts.")
s('Briny Bolt', '330000', 'SBC', "Briny Bolt is an attack spell, so through Spellstrike every hit with Aspera also blinds the target until it spends an action to clear its eyes. That either costs the enemy an action or forces it to make flat checks for every attack. It heightens by 2d6 per rank, so it stays relevant. Because it rides Aspera's attack roll rather than his spell DC, it is the most reliable debuff payload Cyrus has at rank 1.")
s('Shocking Grasp', '400000', 'ACD', "Shocking Grasp is a legacy spell that stays available under the table's rules because it wasn't reprinted under the same name. It deals 2d12 electricity plus 1d12 per rank on Aspera's attack roll, with a bonus to hit and persistent damage against metal-armoured targets. It is a strong attack payload for heightened slots and complements Thunderstrike, which targets Reflex instead of AC.")
s('Force Barrage', '200000', 'CCC', "Force Barrage cannot be used with Spellstrike because it has neither an attack roll nor a save. Its role is a guaranteed finisher against a fleeing enemy at 120 feet. That doesn't justify a slot when Cyrus has better uses for them.")
s('Breathe Fire', '200000', 'CCD', "Breathe Fire is a 15-foot cone. With Expansive Spellstrike from reach, the cone starts from a square next to the target and can be aimed away from Cyrus. Its area is small and Lightning Bolt replaces it at level 5, so it is only worth learning if the early campaign features many grouped weak enemies.")
s('Dizzying Colors', '043000', 'BCC', "Dizzying Colors can stun and blind creatures that fail their save, which effectively ends their turn. It has the incapacitation trait, so it is much less reliable against enemies higher in level than Cyrus, and his spell DC makes failures less common. It is best against groups of lower-level enemies, with the cone aimed away from allies using Expansive Spellstrike.")
s('Pummeling Rubble', '200020', 'CCD', "Pummeling Rubble is a cone that pushes failed targets directly away from Cyrus. Acid Grip lets him choose the direction and distance, and its damage is modest, so it rarely earns a place in the spellbook.")
s('Gust of Wind', '030030', 'ACC', "Gust of Wind becomes an important spell from level 12, when it is the cheapest payload for Sprinting Spellstrike. It lets Cyrus move up to 60 feet in a line without triggering reactions, and every Large or smaller creature in the line that fails its Fortitude save is knocked prone, leaving it off-guard for his Laughing Shadow damage and for his allies. Flying creatures that fail take the critical failure effect instead. Before level 12 it is a reasonable direct-cast control spell.")
s('Goblin Pox', '003000', 'BCD', "Goblin Pox delivers sickened 1 even on a successful save, through Aspera's reach. It works well in longer fights against a single living enemy. Goblins and goblin dogs are immune, and it does nothing to undead or constructs.")
s('Leaden Steps', '012000', 'BCD', "Leaden Steps makes the target encumbered, which means clumsy 1 and a Speed penalty, and gives it electricity weakness that grows with the spell's rank. It sets up electricity payloads such as Thunderstrike, Shocking Grasp and Lightning Bolt. It has to be sustained to last, which competes with Cyrus's recharge actions.")
s('Command', '030000', 'CCD', "Command forces the target to spend an action as Cyrus chooses, such as dropping its weapon or falling prone, but does nothing on a successful save. Fear is usually the better Will payload because it always has an effect.")
s('Curse of Slippery Steps', '030010', 'CCD', "Curse of Slippery Steps makes all terrain difficult for the target, for a round on a success and much longer on a failure. It helps against a single runner or charger, but it rarely changes a fight enough to justify the slot.")
s('Hydraulic Push', '300030', 'BCD', "Hydraulic Push is an attack spell that pushes the target 5 feet on a hit, or 10 on a critical hit. Through Spellstrike it can break a grapple, push an enemy off a ledge or into a hazard, or move it into a melee ally's reach. Acid Grip offers more control over direction and distance.")
s('Grim Tendrils', '201000', 'CCD', "Grim Tendrils is a 30-foot Fortitude line that only affects living creatures. Its damage and length are both small, and Lightning Bolt replaces it as Cyrus's line spell from level 5.")
s('Horizon Thunder Sphere', '300000', 'BCD', "The two-action version of Horizon Thunder Sphere is an attack payload that heightens by 2d6 per rank, which puts its damage close to Shocking Grasp's, with dazzled on a critical hit. The two-round version is too slow for a magus. It is a reasonable second electricity attack payload.")
s('Mystic Armor', '000200', 'DDD', "Mystic Armor uses unarmoured proficiency, and Cyrus wears medium armour. It only matters if he gives up armour for Laughing Shadow's +10-foot unarmoured Speed bonus, which isn't part of the plan.")
s('Jump', '000030', 'CCC', "Jump moves Cyrus 30 feet through the air for one action. It helps on vertical maps before Time Jump or Fly are available, and at rank 3 it lasts a minute on one creature. Dimensional Assault covers most of the same needs in combat.")
s('Gentle Landing', '000003', 'BBD', "Gentle Landing is a reaction, so it only helps if it is prepared or the scroll is already in hand when someone falls. It is worth preparing on days involving cliffs, towers or airships.")
s('Interposing Earth', '000300', 'CCD', "Interposing Earth gives cover against one Strike or area effect as a reaction. It competes with Reactive Strike for Cyrus's reaction and usually gives less value.")
s('Illusory Object', '020004', 'BAC', "Illusory Object creates a convincing fake wall, door, crate or similar object, and its rank-2 version adds sound and touch for an hour. It solves a wide range of infiltration and escape problems. Because Cyrus can't predict when he will need it, a scroll is the best way to carry it.")
s('Illusory Disguise', '000004', 'CAC', "Illusory Disguise supports planned infiltration. At rank 3 it copies a specific person and at rank 4 it disguises up to ten creatures. It is a strong scroll for court and city scenarios where the party can plan the use in advance.")
s('Helpful Steps', '000023', 'CAC', "Helpful Steps is a legacy spell that creates a 40-foot staircase or ladder the whole party can use. It is cheaper than casting Fly on each person to get everyone up a wall or cliff. A scroll covers the occasional need.")
s('Runic Weapon', '000300', 'CDD', "Runic Weapon gives a weapon temporary fundamental runes. Aspera already has its runes, so this only helps a backup weapon.")
s('Conductive Weapon', '200200', 'CCD', "Conductive Weapon makes a metal weapon a +1 shock weapon for a minute, with a larger die against metal-armoured enemies. It can be cast before a fight against armoured soldiers if Aspera has an empty property slot, but a permanent rune is usually the better investment.")
s('Friendfetch', '000040', 'CBD', "Friendfetch is a legacy spell that pulls one or two willing allies straight towards Cyrus. It can rescue a downed or grabbed ally from a dangerous position without spending Yara's actions. A scroll is a sensible emergency option.")
s('Pocket Library', '000003', 'CCB', "Pocket Library gives a status bonus to Recall Knowledge with one chosen skill and removes critical failures. It takes three actions to cast, so it belongs in exploration. A rank-1 wand gives a daily boost to Cyrus's Arcana or Lore checks, which suits his role as the party's scholar.")

# ───────────── Rank 2 ─────────────
s('Acid Grip', '332050', 'SBC', "Acid Grip moves the target even on a successful save, so the payload always accomplishes something. Cyrus chooses the direction, which lets him pull an enemy off a caster, drag it into a melee ally's reach, or move it out of a corridor. The persistent acid also cuts the target's Speed by 10 feet. It works as a 120-foot direct cast as well as a Spellstrike payload, and it heightens well.")
s('Invisibility', '000436', 'SAA', "Invisibility is one of the most important spells Cyrus brings, because no one else in the party has it. The rank-2 version is the scouting and extraction tool and makes an excellent wand. The rank-4 version lasts through hostile actions, so Cyrus can fight while undetected, which makes his targets off-guard and turns on Laughing Shadow's damage. Dimensional Disappearance gives him a similar effect from level 10, freeing the slot for other spells.")
s('Blazing Bolt', '400000', 'ACD', "Through Spellstrike, Blazing Bolt uses its two-action version, which deals 4d6 fire on Aspera's attack roll and heightens by 2d6 per rank. That makes it a strong damage payload for higher slots that doesn't depend on Cyrus's spell DC. Its multi-target option is lost in Spellstrike, but it stays a good direct cast against several enemies.")
s('Telekinetic Maneuver', '040040', 'ACD', "Telekinetic Maneuver lets Cyrus Trip, Shove, Reposition or Disarm with a spell attack. Through Spellstrike, the Strike result decides both the weapon damage and the manoeuvre, so he can damage and trip a target in one activity without a separate Athletics action. It fits his tripping style well. It doesn't heighten, so it always occupies a rank-2 slot.")
s('Sudden Bolt', '400000', 'BCD', "Sudden Bolt is a legacy spell that deals 4d12 electricity with a basic Reflex save and heightens by 1d12 per rank, the largest single-target save damage at rank 2. The save resolves even if Aspera's Strike misses. It is a sound choice if Cyrus wants a high-damage save payload alongside his attack payloads.")
s('Acid Arrow', '300000', 'CCD', "Acid Arrow is a legacy attack spell with persistent acid damage. It only heightens every two ranks, so Blazing Bolt outperforms it as a heightened attack payload.")
s('Disintegrating Puddle', '320000', 'BCD', "Disintegrating Puddle is an attack payload that also leaves acid around the target for a minute. It is most useful when enemies need to cross that area to reach the party, such as at a doorway or chokepoint.")
s('Laughing Fit', '042000', 'BCD', "Laughing Fit stops the target's reactions even on a successful save, and a failure also slows it. It is valuable before the party moves past an enemy with Reactive Strike or a similar reaction. It must be sustained each turn, which takes an action Cyrus usually needs to recharge or move.")
s('Stupefy', '003000', 'CCD', "Stupefy hampers an enemy caster, but its success effect only lasts until Cyrus's next turn. Befuddle and Improvise Strategy cover the same purpose and offer more.")
s('Revealing Light', '003004', 'BAC', "Revealing Light makes invisible creatures concealed and removes other concealment, so the whole party can target them. Its 10-foot burst works with Expansive Spellstrike. A scroll is the practical way to carry it, since invisible enemies are occasional.")
s('Noise Blast', '300000', 'BCD', "Noise Blast is a Fortitude burst for Expansive Spellstrike, and a critical failure stuns. It is a useful alternative to Reflex area spells when a group of enemies has weak Fortitude.")
s('Dimensional Drop', '230000', 'BCD', "Dimensional Drop deals falling damage and leaves the target prone, which makes it off-guard. It is a Reflex payload for grounded enemies that sets up Laughing Shadow's damage on the next Strike.")
s('Dispel Magic', '020005', 'BAD', "Dispel Magic counteracts a spell effect or temporarily suppresses a magic item. The Cleric and Druid can also cast it, so Cyrus doesn't need to prepare it often. A scroll's rank is fixed, so buy the rank that can counteract the effects the party expects to face.")
s('See the Unseen', '000004', 'BBA', "See the Unseen lets Cyrus see invisible creatures as concealed and see incorporeal creatures through nearby surfaces. The rank-5 wand lasts eight hours, which covers a full day of exploration. It is a good wand once the campaign brings invisible or incorporeal threats.")
s('Blur', '000400', 'ABB', "Blur is a studious spell from level 7, so casting it lets Cyrus enter Arcane Cascade as a free action. That makes for an efficient opening turn: he becomes concealed and enters stance for two actions. The concealment doesn't let him Hide, but enemy attacks miss whenever they fail the flat check.")
s('Mirror Image', '000400', 'BBC', "Mirror Image is a legacy defensive spell that creates three images to absorb hits. It is most effective against enemies that make many weapon attacks, such as a creature with several natural weapons.")
s('Resist Energy', '000400', 'BAB', "Resist Energy grants resistance to one energy type, rising to resistance 10 for two creatures at rank 4. Cast it before a fight against a known energy source, such as a dragon or elemental.")
s("Loose Time's Arrow", '000340', 'BBB', "Loose Time's Arrow quickens up to six creatures for an extra Step or Stride. It is a strong opening spell when the party needs to close distance or cross a large map, and it fits Aspera's time theme.")
s('Enlarge', '000430', 'BBC', "Enlarge is excellent on Mira or Cassius, who gain reach and damage. On Cyrus it gives 15-foot reach with Aspera and extra damage, at the cost of clumsy 1 and a larger footprint that makes flanking and teleport landing harder.")
s('Gecko Grip', '000032', 'ACC', "Gecko Grip is a studious spell from level 7, so it is already in Cyrus's spellbook and grants a free Arcane Cascade. A climb Speed equal to his Speed lets him fight from walls or reach high ground without Athletics checks.")
s('Water Breathing', '000003', 'CAD', "Water Breathing lets up to five creatures breathe underwater for an hour. A scroll is the right way to carry it when the adventure involves water.")
s('Blood Vendetta', '220000', 'CCD', "Blood Vendetta is a reaction that needs Cyrus to take piercing, slashing or bleed damage first. It competes with Reactive Strike, which is usually the better use of his reaction.")
s('Embed Message', '000002', 'CCD', "Embed Message leaves a hidden message that triggers on a chosen condition. It is a roleplay tool for dead drops and warnings that rarely needs a prepared slot.")

# ───────────── Rank 3 ─────────────
s('Haste', '000650', 'SAA', "Haste gives an extra Stride or Strike that lets Cyrus close distance and Spellstrike on the same turn, every turn. It is the biggest improvement to his action economy before Hasted Assault, and on Mira or Cassius it is an extra Strike each round. It becomes a studious spell at level 11, which adds a free Arcane Cascade. The Druid can also cast it, so the party should agree who prepares it. With one or two fights a day, a rank-3 wand means a Haste in nearly every fight without using a slot.")
s('Slow', '050400', 'SAB', "Slow imposes slowed 1 for a round even on a successful save, and a failure lasts a minute. Delivered through Spellstrike, it takes a third of a boss's actions while Cyrus still deals weapon damage. At rank 6 it can target ten creatures as a direct cast. The Druid can also cast it, but only Cyrus can combine it with a Strike.")
s('Time Jump', '000060', 'ABC', "Time Jump gives two movement actions for one action, and no creature can react to them. Cyrus can use it to reach a back-line caster or escape a surround and still Spellstrike on the same turn. Casting it again within a minute leaves him stupefied 4, so it is a once-per-fight tool.")
s('Lightning Bolt', '400000', 'SBD', "Lightning Bolt is Cyrus's main line spell. With Expansive Spellstrike, the 120-foot line starts from a square next to the target, so it rarely catches allies. From level 12 it becomes the standard Sprinting Spellstrike payload, letting him move along the line through enemies without triggering reactions and damage everything he passes. Learn it at level 5 and keep it for the whole campaign.")
s('Fireball', '400000', 'BBD', "Fireball is excellent cast normally from up to 500 feet. As an Expansive Spellstrike payload, its 20-foot burst centred on a corner of the target's square usually includes Cyrus at 10-foot reach, so it is better as a direct cast. The Druid can also cast it.")
s('Cave Fangs', '430000', 'BBD', "Cave Fangs deals piercing damage and leaves the area as difficult terrain for a minute. Physical damage avoids the elemental resistances many creatures have. Its burst has the same self-damage problem as Fireball when used with Expansive Spellstrike.")
s('Blindness', '005000', 'BCD', "Blindness blinds the target for a minute on a failed save, which is crippling. A successful save only blinds it until its next turn begins, and the incapacitation trait makes it unreliable against bosses. It is a Fortitude payload for dangerous enemies of Cyrus's level or lower.")
s('Paralyze', '050000', 'BCD', "Paralyze stuns on a success and paralyses on a failure. The incapacitation trait limits it to enemies of Cyrus's level or lower, and his spell DC makes failures less likely.")
s('Blister Bomb', '004000', 'ACD', "Blister Bomb imposes sickened 2 on a successful save, which is a −2 penalty to AC, attacks and saves for every creature in the burst. The 5-foot burst is easy to place with Expansive Spellstrike without catching allies. It doesn't affect creatures immune to disease.")
s('Earthbind', '030000', 'CBD', "Earthbind forces a flying creature to the ground. It is a situational scroll for adventures involving wyverns, harpies or other flyers.")
s('Magnetic Acceleration', '400000', 'BCD', "Magnetic Acceleration deals 3d6 bludgeoning and 3d6 piercing on Aspera's attack roll and heightens by 1d6 of each per rank, the same 2d6 per rank as Briny Bolt and Blazing Bolt, with no effect beyond the damage. Its +1 bonus against targets in metal armour or made of metal applies to the spell's own attack roll; through Spellstrike the Strike's roll decides the result, so the bonus is unlikely to apply. Briny Bolt deals the same damage and also blinds, so Magnetic Acceleration is worth preparing only when blinding wouldn't matter, such as against a creature that doesn't rely on sight.")
s('Wooden Double', '000400', 'BCD', "Wooden Double is a reaction that turns a critical hit against Cyrus into a hit on a wooden decoy. It is worth preparing against enemies known for large critical hits.")
s('Ghostly Weapon', '000302', 'ABD', "Ghostly Weapon becomes a studious spell at level 11. Until then, a scroll lets Aspera affect incorporeal undead fully for five minutes, which matters in a campaign with haunts and spirits.")

import spell_evals2, spell_evals3, spell_evals4, spell_evals5, spell_evals6  # noqa: ranks 4-9, occult, expansions, completeness pass, full review


# scroll and wand grades follow one set of criteria (see item_grades.py); spellbook grades are unchanged
from item_grades import G as _G
for _n, (_sc, _wd) in _G.items():
    if _n in E:
        _r, _g, _e = E[_n]
        E[_n] = (_r, _g[0] + _sc + _wd, _e)

_FIX = {
 'Fear': ("With one or two fights a day, a wand gives a free group debuff most days.", "From a wand it costs too many actions in combat to beat a prepared copy."),
 'Haste': (" With one or two fights a day, a rank-3 wand means a Haste in nearly every fight without using a slot.", " A wand only pays off when he can open a fight from range with it already in hand."),
 'Mirror Image': (", ideally from a wand or scroll rather than a slot", ""),
 'Soothe': ("With one or two fights a day, a wand gives a free heal in nearly every fight, making it one of the best occult purchases.", "A wand gives a daily heal after a fight, which saves Yara's slots, but in combat the action cost makes it a poor choice."),
 'Protection': ("A wand provides a daily defensive buff for the start of a fight.", "From a wand it costs too many actions at the start of a fight to be worth it over his own opening."),
 'Liberating Command': ("A wand is attractive because it can be used every day without planning.", "From a wand the draw and regrip make it slower than an ally's own Escape attempt."),
 'Dimensional Drop': ("It is worth carrying as a scroll or preparing on days when Cyrus expects grounded brutes", "It is worth preparing on days when Cyrus expects grounded brutes"),
 'Invisibility': ("makes an excellent wand", "makes a good wand"),
 'Lucky Number': ("It is cast during preparations, so the scroll works as well as a slot and needs no hands later.", "It is cast during preparations and needs no hands later, so a wand gives a free reroll chance every day."),
}
for _n, (_a, _b) in _FIX.items():
    _r, _g, _e = E[_n]
    E[_n] = (_r, _g, _e.replace(_a, _b))

# rarity doesn't restrict this table, so it plays no part in grades or evaluations
_RARITY = {
 'Warping Pull': ("It is uncommon, so learning it needs access; Axuma's Awakening gives it at 11 without that, and it is one of the planned picks there.", "Axuma's Awakening also gives it at 11 without a slot, and it is one of the planned picks there."),
 'Pyrefowl Rebuke': (" It is uncommon and from an adventure path.", ""),
 'Locate': ("It is uncommon, so it needs access, and a scroll is enough for the occasional search for a stolen item or missing person.", "A scroll is enough for the occasional search for a stolen item or missing person."),
 'Mind Reading': ("It is uncommon and the target may notice, but", "The target may notice, but"),
 'Echo Jump': ("It is uncommon, and allies next to him are caught in the blast.", "Allies next to him are caught in the blast."),
 'Temporal Twin': (" and is uncommon.", "."),
 'Glass Sand': (" It is uncommon, and Crashing Wave covers the same role without access.", " Crashing Wave covers much the same role."),
 'Magical Fetters': ("It is uncommon and has the incapacitation trait", "It has the incapacitation trait"),
 'Radiant Globe': (" but it must be sustained and is uncommon.", " but it must be sustained."),
 'Wall of Mirrors': ("It is rare, so outside Aspera's stave it needs access, and from a scroll it is still a strong answer to an encounter that needs splitting.", "It is planned for Aspera's stave at level 10, and from a scroll it is still a strong answer to an encounter that needs splitting."),
 'Rebounding Barrier': ("It is rare, so it needs Alex's approval, and it only protects Cyrus himself.", "It only protects Cyrus himself."),
 'Dispelling Globe': ("immobile, uncommon and counteracts", "immobile and counteracts"),
 'Liminal Doorway': (" It is uncommon, so it needs access.", ""),
 'Peaceful Bubble': ("It is uncommon and only matters", "It only matters"),
 'Discern Lies': ("In interrogations and court scenes it is a strong edge, but it is uncommon.", "In interrogations and court scenes it is a strong edge."),
 'Drop Dead': (" It is uncommon, so it needs access.", ""),
 'Mind Probe': ("It is uncommon, but in a campaign", "In a campaign"),
 'Truespeech': ("It is uncommon, but in a campaign", "In a campaign"),
 'Umbral Journey': ("It is uncommon and only matters", "It only matters"),
 'Telepathic Bond': ("It is uncommon, but it suits", "It suits"),
 "King's Castle": ("but it is uncommon and costs two actions.", "but it costs two actions."),
 'Blinding Foam': (", and it is uncommon.", "."),
 'Dominate': ("but it is uncommon and has the incapacitation trait", "but it has the incapacitation trait"),
 'Zero Gravity': ("It is uncommon and must be sustained.", "It must be sustained."),
 'Scrying': ("It is uncommon, but it is the classic way", "It is the classic way"),
 'Utter Destruction': (", and Utter Destruction is uncommon.", "."),
 'Interplanar Teleport': ("It is uncommon and needs a planar key", "It needs a planar key"),
 'Planar Palace': ("It is uncommon, but it guarantees", "It guarantees"),
 'Planar Seal': ("It is uncommon and only matters", "It only matters"),
 'Power Word Blind': (" It is uncommon.", ""),
 'Reverse Gravity': (" It is uncommon.", ""),
 'Hidden Mind': ("It is uncommon and strongest", "It is strongest"),
 'Pinpoint': ("It is uncommon, but it ends any search.", "It ends any search."),
 'Power Word Stun': (" It is uncommon.", ""),
 'Sudden Transposition': (" It is uncommon.", ""),
 'Detonate Magic': ("It is uncommon and depends", "It depends"),
 'Power Word Kill': (" It is uncommon.", ""),
}
for _n, (_a, _b) in _RARITY.items():
    _r, _g, _e = E[_n]
    assert _a in _e, _n
    E[_n] = (_r, _g, _e.replace(_a, _b))
# spellbook grades that had been held down by rarity
for _n, _sb in {'Power Word Stun': 'S', 'Mind Reading': 'B', 'Locate': 'B', 'Discern Lies': 'B', 'Mind Probe': 'B',
                'Scrying': 'B', 'Truespeech': 'A', 'Glass Sand': 'B', 'Liminal Doorway': 'B'}.items():
    _r, _g, _e = E[_n]
    E[_n] = (_r, _sb + _g[1:], _e)

# party members by name, not by class
_PARTY = {'Druid': 'Theldren', 'Cleric': 'Yara', 'Champion': 'Mira', 'Fighter': 'Cassius', 'Animist': 'Adrian'}
def _names(t):
    t = re.sub(r"\b[Tt]he (Druid|Cleric|Champion|Fighter|Animist) and (Druid|Cleric|Champion|Fighter|Animist)\b",
               lambda m: _PARTY[m.group(1)] + ' and ' + _PARTY[m.group(2)], t)
    t = re.sub(r"\b[Tt]he (party's )?(Druid|Cleric|Champion|Fighter|Animist)\b", lambda m: _PARTY[m.group(2)], t)
    return t
for _n, (_r, _g, _e) in list(E.items()):
    E[_n] = (_r, _g, _names(_e))
_r, _g, _e = E['Fireball']
E['Fireball'] = (_r, _g, _e.replace("Theldren can also cast it.", "Theldren can also cast it, so Cyrus rarely needs to prepare it himself."))

# other party members: mention them only as context, without assuming what they prepare
_CTX = {
 'Detect Magic': ("Detect Magic is essential for the party, but Yara and Theldren can also cast it, so Cyrus only needs it on investigation-heavy days or when the casters have chosen other cantrips.",
                  "Detect Magic is essential for the party, and Cyrus is the strongest Arcana user, so it is worth knowing even if another caster sometimes covers it. It earns a cantrip slot mainly on investigation-heavy days."),
 'Dispel Magic': ("Yara and Theldren can also cast it, so Cyrus doesn't need to prepare it often.",
                  "Yara and Theldren have it on their spell lists too, so the party can decide between them who keeps a copy ready."),
 'Haste': ("Theldren can also cast it, so the party should agree who prepares it.",
           "It is also on Theldren's spell list, which gives the party a second source on days when both want it."),
 'Slow': ("Theldren can also cast it, but only Cyrus can combine it with a Strike.",
          "It is also on Theldren's spell list, but only Cyrus can deliver it with a Strike."),
 'Fireball': ("Theldren can also cast it, so Cyrus rarely needs to prepare it himself.",
              "It is also available to Theldren, should the party want a very long-range area option, while Cyrus spends those opening turns buffing allies or himself as he closes the gap on a large map."),
 'Fly': ("Theldren and Yara can cast it as well, so the party should agree who prepares it on a given day.",
         "It is also on Theldren's and Yara's spell lists, so on a day that needs several flyers the party has more than one source."),
 'Eclipse Burst': ("Theldren's area spells usually cover this role.",
                   "Long-range area spells are something a primal caster such as Theldren may cover instead, which frees Cyrus's slot for a payload."),
 'Gravity Well': ("such as an Expansive Spellstrike or Theldren's spells", "such as an Expansive Spellstrike or an ally's area spell"),
 'Shadow Projectile': ("Theldren's, Yara's and Adrian's ranged spell attacks qualify, so it can raise one of their hits.",
                       "Ranged spell attacks from the party's casters qualify, so it can raise one of their hits."),
 'Bless': ("Yara can cast it, so Cyrus only needs a scroll on days it isn't prepared.",
           "It is also on Yara's spell list, so a scroll is only worth carrying as a backup."),
 'Bane': ("Yara can also cast it from the divine list, and sustaining it each turn competes with Cyrus's recharge actions.",
          "Sustaining it each turn competes with Cyrus's recharge actions."),
 'Cleanse Affliction': ("Yara shares this spell, so Cyrus only needs a scroll as backup once Yara's slots are spent.",
                        "It is also on Yara's spell list, so a scroll is a backup for a long day or an affliction that needs a second attempt."),
 'Heroism': ("Yara can cast it from the divine list, so Cyrus's scroll or wand mainly frees Yara's slots for healing and other spells.",
             "It is also on Yara's spell list, so Cyrus's scroll or wand is a way to cover it when her slots are needed elsewhere."),
 'Sound Body': ("Yara can remove some of these conditions, but not all, so a scroll is a strong backup.",
                "A divine caster may be able to remove some of these conditions, but a scroll covers all of them when it matters."),
 'Sanctuary': ("while Yara heals", "while the party gets them back on their feet"),
 'Friendfetch': ("without spending Yara's actions", "without spending a healer's actions"),
 'Gentle Breeze': ("which spares Yara's slots after a fight", "which spares the party's other healing after a fight"),
 'Soothe': ("A wand gives a daily heal after a fight, which saves Yara's slots, but in combat", "A wand gives a daily heal after a fight, but in combat"),
}
for _n, (_a, _b) in _CTX.items():
    _r, _g, _e = E[_n]
    assert _a in _e, _n
    E[_n] = (_r, _g, _e.replace(_a, _b))
_r, _g, _e = E['Bane']
E['Bane'] = (_r, _g, _e.replace("A scroll is only worth it on days Yara doesn't prepare it.", "The penalty is small for the actions it costs, so a scroll is a minor backup at most."))
_r, _g, _e = E['Soothe']
E['Soothe'] = (_r, _g, _e.replace("without taking Yara's actions, and the party has no other occult healing", "without taking another healer's actions"))

# allies described by role rather than by name where the name adds nothing
_ALLY = {
 'Gale Blast': ("adjacent allies such as Mira and Cassius", "adjacent allies"),
 'Enfeeble': ("which protects Mira and Cassius", "which protects whoever is holding the front line"),
 'Shockwave': ("give Mira and Cassius easier hits", "give the party's melee attackers easier hits"),
 'Enlarge': ("Enlarge is excellent on Mira or Cassius, who gain reach and damage.", "Enlarge is excellent on a melee ally, who gains reach and damage."),
 'Propulsive Breeze': ("which can get Mira or Cassius into melee in one move", "which can get a melee ally into the fight in one move"),
 'Haste': ("and on Mira or Cassius it is an extra Strike each round", "and on a melee ally it is an extra Strike each round"),
 'Temporal Twin': ("On Mira or Cassius it is effectively an extra Strike", "On a melee ally it is effectively an extra Strike"),
 'Mountain Resilience': ("On Cyrus or Mira it prevents", "On Cyrus or another front-liner it prevents"),
 'Winning Streak': ("so on Mira or Cassius it is an extra Strike for a cheap cast", "so on a melee ally it is an extra Strike for a cheap cast"),
 'Cloak of Colors': ("Cast on Mira or Cassius, it punishes every enemy that attacks them.", "Cast on a front-liner, it punishes every enemy that attacks them."),
 'Energy Aegis': ("Cast in the morning on Cyrus or Mira,", "Cast in the morning on Cyrus or an ally,"),
 'Mask of Terror': ("On Mira, Cassius or Cyrus it frightens", "On Cyrus or a front-liner it frightens"),
 'Foresight': ("Mira, or whoever the boss is likely to target, is the natural recipient.", "Whoever the boss is likely to target is the natural recipient."),
 'Sound Body': ("Removing slowed from Mira or Cassius in a hard fight", "Removing slowed from an ally in a hard fight"),
 'Draw Ire': ("It can protect Yara or Theldren from an enemy that has reached them.", "It can protect a vulnerable ally from an enemy that has reached them."),
}
for _n, (_a, _b) in _ALLY.items():
    _r, _g, _e = E[_n]
    assert _a in _e, (_n, _a)
    E[_n] = (_r, _g, _e.replace(_a, _b))
_r, _g, _e = E['Draw Ire']
E['Draw Ire'] = (_r, _g, _e.replace("only sensible when Mira can't", "only sensible when the party's main defender can't"))
_r, _g, _e = E['Sound Body']
E['Sound Body'] = (_r, _g, _e.replace("and from rank 4 drained and slowed, on a willing creature.", "on a willing creature, adding drained and slowed at rank 4, petrified at rank 6 and stunned at rank 8."))


# Aspera's stave (from level 8): spells that are on it are noted where the stave changes how Cyrus gets them
_STAVE = {
 'Figment': ("Its effects look crude up close, so it works best as a quick distraction.", "Its effects look crude up close, so it works best as a quick distraction. It is a cantrip on Aspera's stave from level 8, so it costs no charges and doesn't need one of his prepared cantrips."),
 'Illusory Object': ("Because Cyrus can't predict when he will need it, a scroll is the best way to carry it.", "It is on Aspera's stave at rank 1 from level 8, which covers the unplanned uses; before then a scroll is the best way to carry it. The stave's rank-1 version has no sound or touch, so the rank-2 version still needs a scroll or a slot."),
 'Illusory Disguise': ("It is a strong scroll for court and city scenarios where the party can plan the use in advance.", "Aspera's stave has it at rank 3 from level 8, so Cyrus can copy a specific person for 3 charges whenever the party needs it. The rank-4 version for the whole party still needs a scroll or a slot."),
 'Embed Message': ("It rarely needs one of Cyrus's prepared slots, but it fits Aspera's theme of things that speak across time.", "It is on Aspera's stave at rank 2 from level 8, which is the right place for it: it fits the stave's theme and never takes a prepared slot."),
 'Clairvoyance': ("since Cyrus can scout the next encounter before committing.", "since Cyrus can scout the next encounter before committing. It joins Aspera's stave at level 16, where 4 charges spent between fights cost little."),
 'Haste': ("At rank 7 it targets six creatures, so one cast gives the whole party an extra action every turn for a minute.", "At rank 7 it targets six creatures, so one cast gives the whole party an extra action every turn for a minute. Aspera's stave has that version from level 16 for 7 of his 8 daily charges, which makes it the stave's strongest spell; the stave doesn't have the single-target rank-3 version."),
 'True Target': ("Its value depends on initiative", "It is on Aspera's stave from level 16. Its value depends on initiative"),
}
for _n, (_a, _b) in _STAVE.items():
    _r, _g, _e = E[_n]
    assert _a in _e, _n
    E[_n] = (_r, _g, _e.replace(_a, _b))

import spell_evals7  # noqa: E402,F401  general rewrites
import spell_evals8  # noqa: E402,F401  evaluations rewritten to one standard, applied last
import spell_ratings  # noqa: E402,F401  role ratings reviewed against one scale
