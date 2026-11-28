"""Spell evaluations, rewritten to one standard and applied last.

An evaluation judges the spell. It does not describe it: the rules text sits directly above it on the card.
 - Say how good the spell is at its job and why: its damage for the rank, what the rider is worth, what a successful
   save still gives, how safe the area is around allies, its range and action cost, how it heightens. A mechanic is
   mentioned only as the reason for a judgement, and a number only where a comparison needs it.
 - Give the use cases: when Cyrus would prepare or cast it, how he delivers it (Spellstrike, Expansive Spellstrike, a
   direct cast, a reaction, before a fight, a scroll or wand), against what kind of enemy or problem, and where it is the
   wrong choice.
 - Compare it with the spells that compete for the same job, and end on the place it earns.
 - Facts that shape every judgement: an enemy of his level or higher resists a save spell more often than not, whoever
   casts it, so an effect on a successful save is worth a great deal and a critical failure is rare. His spell DC is
   level with a full caster's or one or two points behind until level 19 (see the handoff), so never blame a spell's
   unreliability on his DC. An attack-roll spell delivered by Spellstrike uses the Strike's roll; he has two slots of
   each rank; sustaining a spell and recharging Spellstrike compete for the same action; from level 6 a reaction spell
   competes with Reactive Strike.
 - Plain wording, British spelling, sentences that vary. No party names, campaign, named monsters, printings or
   references to other pages. S, A and B cards run to roughly 70 to 110 words; C, D and F cards to 30 to 50.
"""
from spell_evals_base import E


def w(name, text, grades=None, ratings=None):
    r, g, _ = E[name]
    E[name] = (ratings or r, grades or g, text.strip())


# ───────────────────────── rank 2 ─────────────────────────
w('Acid Grip', """The most dependable spell at this rank, because it achieves something at every result short of a critical success. Its damage is fair once the persistent acid is counted. Its worth is the forced move, which Cyrus aims: an enemy comes off a pinned ally, into a flank or out of a doorway, and has to spend actions inside his reach to get back. Enemies of his level or higher save more often than they fail, so a spell that still shifts them on a success is worth far more than one that needs a failure.

It is the wrong pick against a lone enemy that is already where the party wants it; Sudden Bolt's damage serves better there. Otherwise prepare it by default, and keep it in a rank-2 slot at every level.""")

w('Invisibility', """Two different spells, depending on the slot. From a rank-2 slot it is for everything outside a fight: scouting ahead, passing a guard post, getting one person out of a bad situation. It ends at the first hostile act, so it does nothing for his damage.

From a rank-4 slot it is among the best things he can cast as a fight opens. An enemy that cannot see him is off-guard to every Strike, which switches on Laughing Shadow's extra damage without help from anyone, and each attack aimed at him has to find him first. Enemies that sense without sight, or that can see the invisible, undo it. The rank-2 use is occasional enough for a scroll or wand; the rank-4 use earns a slot until Dimensional Disappearance at 10.""", grades='SAB')

w('Telekinetic Maneuver', """This turns a Spellstrike into a Strike and a Trip, Shove or Reposition in one activity, settled by the Strike's roll, with no save for the target and no separate Athletics action. A tripped enemy is off-guard, which feeds Laughing Shadow, and from level 6 it provokes Reactive Strike when it stands. Against one dangerous melee enemy that is two or three of its actions spoiled across a round.

It adds no damage, so it is the wrong spell when the target simply needs to die, and it does little to an enemy that cannot be knocked down or moved. Dimensional Drop gets the same prone result from a Reflex save even when the Strike misses; this is the better choice against agile enemies and when a shove is what the position needs.""")

w('Blazing Bolt', """Plain attack-roll damage at a fair rate for the rank, delivered on the Strike's roll and doubled with it on a critical hit. That is all it offers through Spellstrike, and Briny Bolt heightened to the same slot matches the damage and adds a chance to blind, in a damage type that is resisted far less often than fire.

Its one distinct use is the three-action cast, which spreads rays over three enemies on a turn when he cannot reach melee. That turn comes up rarely for a magus. Learn it only if a second damage type among his attack spells matters to the day ahead.""")

w('Sudden Bolt', """The hardest single-target hit available at this rank, roughly double what the other spells at the rank deal, and because it runs on a save it still does half when the Strike connects and the target succeeds. It has no rider and no area, so it does exactly one thing: remove hit points from one enemy.

That makes it the right slot against a single tough target, and against anything with poor Reflex such as slow, heavily armoured enemies. It is poor value against a group, and against quick enemies who will often halve it. Acid Grip is the more useful default; this is what he prepares when the day calls for damage and nothing else.""")

w('Acid Arrow', """Adequate on the day it is learned and worse in every slot above, because its damage grows only every second rank while Briny Bolt and Blazing Bolt grow every rank. The persistent acid is a small extra that seldom lasts. Acid as a damage type is its only argument, and Acid Grip already covers that with a far better effect.""")

w('Disintegrating Puddle', """An attack spell whose value depends entirely on where the target is standing. The hit itself is ordinary. The acid it leaves around the target lasts the whole fight, so at a doorway, on a bridge or in a corridor every enemy coming through pays for it, and a magus who holds a chokepoint at reach is well placed to exploit that.

In open ground it does little, since enemies simply walk out, and allies fighting beside the target stand in the acid as well. Its short range also limits it as a direct cast. Worth learning for dungeon days; Briny Bolt is the better attack spell everywhere else.""")

w('Laughing Fit', """The best answer at this rank to an enemy whose reactions are the problem. Even a successful save shuts those reactions off, which lets the whole party move, cast and stand up around it freely, and a failure takes an action away each round on top. Against one dangerous enemy that is a large swing for a rank-2 slot.

The cost is the sustain. Each round it competes with recharging Spellstrike, so Cyrus keeps it running in place of his own burst damage, and it is best when the party's other strikers benefit more than he loses. Mindless creatures and anything not alive ignore it entirely. Prepare it for a known single threat, not as routine.""")

w('Stupefy', """A debuff aimed at spellcasters that barely functions unless the target fails outright, which a capable enemy often will not. The effect on a success is over before it matters. Fear from a rank-1 slot hampers any kind of enemy, works on a success, and costs less.""")

w('Revealing Light', """A problem-solver more than a combat spell. Its real job is ending invisibility and concealment for the whole party at once, at long range, and nothing else at this rank does that. The dazzle it leaves is a decent consolation, since it applies even on a successful save.

It deals no damage, so on a day without hidden enemies it is a wasted slot, and Ignite Fireworks dazzles nearly as well while hurting. That makes it a scroll to carry at all times and a preparation only when unseen enemies are expected. Through Expansive Spellstrike the burst will dazzle allies next to the target as readily as enemies.""")

w('Noise Blast', """Respectable area damage against Fortitude with a rider that almost never matters: being deafened for a round changes little for most enemies. The stun on a critical failure is the one real prize, and critical failures are uncommon against anything of his level or higher. The burst suits Expansive Spellstrike when two or three enemies are bunched and no ally stands beside the target; its short range makes it awkward to cast directly.

Of the three Fortitude area spells at this rank it comes last. Spray of Salt hits a little harder in a cone that is easier to keep off allies, and Disorienting Flash matches its damage from twice the range with a rider worth having. Take it only if both of those are unavailable.""")

w('Dimensional Drop', """A way to put an enemy on the ground that works even when it saves. Any fall that deals damage leaves the creature prone, so every result short of a critical success ends with the target off-guard and an action down to stand, and from level 6 standing provokes Reactive Strike. Delivered by Spellstrike it does this whether or not the Strike hits. The damage itself is trivial and never improves.

It is the right spell against a single strong melee enemy, and a fine opener for the party's other strikers. It does nothing to a creature in the air, and one with a fly Speed can use its reaction to catch itself. Unrelenting Gravity needs a failed save for the same result, and Telekinetic Maneuver needs the Strike to hit.""", grades='ADD', ratings='240000')

w('Dispel Magic', """Irreplaceable on the rare day it is needed and dead weight on the rest. When a fight turns on one enemy spell, a wall, a curse on an ally or a buff on the enemy, nothing else removes it. Its chance depends on the slot it is cast from, so a rank-2 copy only handles weak magic and the copy that matters sits in one of his two highest slots, which he can seldom spare.

That is the argument for a scroll of the highest rank he can afford: the answer is on hand without costing daily damage. Prepare it only when he knows he is walking into enemy spellcasters.""")

w('See the Unseen', """A personal fix for invisible and incorporeal enemies, where Revealing Light is the fix for the whole party. It leaves the creature concealed, so it helps without solving the problem, and it does nothing for allies who still cannot see the target.

Its value is its duration. Ten minutes covers a dungeon wing, and from rank 5 it lasts most of a day, which makes a wand the obvious home: cast in the morning, it removes one way of being ambushed for no slot. As a prepared spell at low rank it is hard to justify over Revealing Light on a scroll.""")

w('Mirror Image', """Strong protection against a few heavy hits and weak protection against many light ones, because each attack that would have landed uses up an image. Against a single hard-hitting enemy it will usually absorb two or three Strikes, which is more than any other defensive spell at this rank prevents.

It costs two actions and protects only him, so it belongs to the round before a fight starts, or to an opening turn when he cannot reach anyone anyway. Cast in the middle of a fight it costs a Spellstrike. Blur gives less protection for longer and, from level 7, comes with a free Arcane Cascade, which is why this drops out of his preparation at that point.""")

w('Resist Energy', """Very good when the damage type is known and useless when it is not. Against an enemy built around one element it takes a steady bite out of every hit for a whole fight, and at higher ranks it covers the front line together.

That dependence on foreknowledge is why it suits a scroll or wand better than a daily slot. Ten minutes is long enough to cast outside the door once the party knows what is behind it. Prepare it only for a day with a known elemental threat.""")

w('Blur', """An average defensive buff until level 7 and a very good one after. Before then it is two actions for a one-in-five miss chance, which Mirror Image beats against the enemies that matter most.

At 7 it becomes a studious spell. It enters his spellbook free, and casting it lets him enter Arcane Cascade as a free action, so the two actions he would have spent on stance and defence separately become one cast. From then on it is the natural first turn of any fight in which he expects to be attacked, and it works on an ally if someone else needs it more. Keep one prepared from level 7.""")

w("Loose Time's Arrow", """A fast start for the whole party from one rank-2 slot. Its use is the first round of a fight on a big map, or an ambush where everyone needs to close or get clear at once, and in that round it can be worth more than any damage spell he could have cast.

Outside that round it does nothing, and it costs him his own opening Spellstrike. Haste at rank 3 does far more for one person over a whole fight. Worth a slot when the party is slow to engage; otherwise leave it.""")

w('Enlarge', """A damage and reach buff with a real cost attached. The extra reach widens the area Cyrus threatens with Reactive Strike, and the damage bonus applies to every Strike, but the clumsy condition lowers his AC and Reflex, and a Large body is harder to fit into a flank or a corridor and harder to place when he teleports.

It usually does more on a melee ally who makes more Strikes each round than he does. Five minutes is long enough to cast before opening a door, which makes it a reasonable scroll or wand. As one of his own two rank-2 slots it rarely beats a spell he can Strike with.""")

w('Gecko Grip', """Reliable vertical movement with no Athletics check, for ten minutes. It solves walls, pits, ships' rigging and enemies shooting from a ledge, and it lets him fight from a surface where few melee enemies can follow.

It is situational, which would normally mean a scroll, but at level 7 it becomes a studious spell: it enters his spellbook free and gives a free Arcane Cascade when cast. That makes it a sound opening action in any fight with height in it. Prepare it when the terrain is known to be vertical; otherwise it waits in the book.""")

w('Hidebound', """A reaction that takes a little off every Strike against one ally for a whole round, cast from range and for no action on his own turn. Against an enemy that attacks several times it prevents more in total than its small number suggests, and it scales acceptably in higher slots.

The costs are the reaction and the slot. From level 6 it competes with Reactive Strike, so it is best in rounds when no enemy is likely to provoke. It cannot sensibly go on a scroll or wand, since he would need the item in hand. Warping Pull stops more of one big hit and works against spells; this is the better choice against a flurry of attacks. Axuma's Awakening at 11 can supply either without a slot.""")

w('Warping Pull', """The stronger of his two protective reactions against a single large hit. It works on any source of damage, including spells and breath weapons, and its resistance grows quickly in higher slots. The short teleport matters as much as the number: it can take an ally out of an enemy's reach before the next attack, or bring them into a flank.

It protects against one effect only, so Hidebound is better against an enemy that makes many attacks, and the ally has to be within 30 feet. Like any reaction spell it competes with Reactive Strike from level 6. A low-rank slot is a cheap place to keep it.""")

w('Water Breathing', """A complete answer to one problem, for the whole party, for hours. There is no reason to hold a daily slot for it: buy a scroll when water is known to be ahead, and at higher ranks one casting covers the day.""")

w('Blood Vendetta', """Damage for no action on his turn, which is attractive for a class as short of actions as the magus. The persistent bleed is respectable for the slot and the weakness it adds helps every slashing hit that follows, his own included.

The conditions are awkward. He has to be hit first, by the right damage type, and the enemy then gets a save. From level 6 Reactive Strike is nearly always the better use of the reaction. Creatures that cannot bleed ignore it. A reasonable low-slot choice before 6, and seldom after.""")

w('Embed Message', """Useful only away from a fight, as a warning, a signal or a message left behind. It is cheap and occasionally clever, and never worth a daily slot. Aspera's stave is planned to hold it, which gives him the option for nothing.""")

w('Propulsive Breeze', """A small reaction that gets a melee ally into reach one action sooner, which on a large battlefield can mean an extra Strike for them in the first round. It only extends a straight-line move, and from level 6 it costs him Reactive Strike for the round. A minor pick for a spare low slot.""")

w('Pyrefowl Rebuke', """It works against the way he fights. The damage is negligible, and the movement carries him away from an enemy he wants standing inside his reach. A reaction spent on this is a reaction not spent on Reactive Strike or on protecting an ally.""")

w('Animated Assault', """Ordinary area damage on the first round, with more only if he sustains it. Each sustain is an action he needs for recharging Spellstrike, so in practice he gets the first hit and little else. Ignite Fireworks and Vomit Swarm give more for the same slot.""")

w('Ash Cloud', """A whole turn for a small amount of damage each round and some hindrance to fliers. Three actions rules out Spellstrike, and the cloud troubles allies who enter it as much as enemies. Only worth considering to hold a group of flying creatures back, and better spells do that later.""")

w('Charitable Urge', """Unusually strong for the rank when it works: even a successful save costs the enemy an action, with no sustain, and a failure wastes most of its next turn. Against low-level enemies holding weapons or items it is a better control spell than Laughing Fit.

Incapacitation is the catch. From a rank-2 slot any enemy above level 4 treats its save as one step better, so the dangerous targets shrug it off, and those are the ones worth controlling. It also does nothing to a creature that carries nothing. Useful at levels 3 and 4, then only if heightened into slots he needs for other things.""")

w('Darkness', """It blinds him as surely as it blinds the enemy, since he has no darkvision, and it takes a full turn to cast. Its one use is covering a retreat. A party in which everyone sees in the dark could exploit it; this is not that party member.""")

w('Darkvision', """A necessity on some days and irrelevant on others. As a human he has no way to see in darkness, and fighting by torchlight gives away his position and leaves him at a disadvantage against anything that can see him first.

The hour-long duration, rising to a full day in higher slots, is exactly what a wand is for: cast once in the morning and forgotten. Until he owns one, a scroll in the pack covers the unexpected cave. A prepared slot only makes sense for a day he knows will be spent underground or at night.""")

w('Deafness', """Being deafened inconveniences an enemy without stopping it from doing anything that matters in most fights. A single-target spell with that as its best result is a poor use of any slot.""")

w('Entangling Flora', """Area control that needs no sustaining and slows a group for a whole fight, which is rare at this rank. It is at its best splitting an encounter: half the enemies wade through it while the party deals with the rest, and Cyrus holds the near edge at reach.

It needs plants or soil underfoot, so it fails on stone floors, and its area is far too large to drop on a melee through Expansive Spellstrike without catching the party. Treat it as a direct cast in the first round. Web holds each creature more firmly in a smaller space but costs three actions.""")

w('Environmental Endurance', """Protection from heat or cold for a whole day. It matters on an expedition and nowhere else, and a scroll or wand covers that without touching his daily slots.""")

w('Exploding Earth', """Attack-roll damage with a little splash and a chance to knock prone on a critical hit. It improves at half the rate of Briny Bolt, and the splash lands on allies standing beside the target, which is where his allies usually are. No reason to learn it.""")

w('False Vitality', """A buffer of temporary Hit Points that lasts a working day and costs no action in a fight. It softens the first hits of the first encounter and then it is gone, and it only works on him.

The long duration makes it a wand spell: cast at breakfast, it is free durability every day. In a slot it has to compete with spells that decide fights, and it loses.""")

w('Floating Flame', """Its damage depends on sustaining and moving it every round, and that action is the one he needs for recharging Spellstrike. Full casters can make it pay over a long fight. He cannot.""")

w('Heat Metal', """Excellent against the right target and useless against the wrong one. Against an enemy in metal armour the persistent fire keeps burning with no easy way to end it, and over a few rounds the total passes any other spell at this rank. Against an enemy holding a metal weapon it forces a choice between dropping the weapon and burning.

Against anything without metal it does nothing at all, so it cannot be a default preparation. Learn it and prepare it when the day's enemies are known to wear armour; Sudden Bolt is the safer general choice.""")

w('Humanoid Form', """A disguise that holds up to casual inspection and gives a bonus to pass as someone else. For a character who does much of the party's talking it has real uses in infiltration, and none in a fight. Carry a scroll.""")

w('Illusory Creature', """In a fight it asks for an action every round that he needs for Spellstrike, and it vanishes at the first hit. Outside a fight it is a convincing decoy, distraction or lure. That second use is worth a scroll and not a slot.""")

w('Knock', """His way past a lock when nobody in the party is good with one. The bonus is large, and he can attempt the check himself as part of the casting. Locks do not appear on a schedule, so this lives on a scroll.""")

w('Lucky Number', """A one-in-twenty chance, once a day, to reroll a d20 that happened to show the right number. The odds of it landing on a roll that matters are small. Tolerable from a wand, where it costs nothing, and not worth a slot.""")

w('Mist', """Concealment that hampers both sides equally and takes a whole turn. It can blunt enemy archers or cover a withdrawal, but it also hides the enemy from his own party. Rarely the best use of three actions.""")

w('Oaken Resilience', """A tiny resistance bought with a larger weakness to fire. The trade is bad even before the slot is counted.""")

w('Phantasmal Treasure', """It takes one enemy out of a fight only for as long as the party leaves it alone, and the target gets repeated chances to see through it. On a success it does almost nothing. Too fragile to plan around.""")

w('Shrink', """A utility trick for fitting someone through a gap or hiding them. Cast on himself it removes his reach, which is the centre of how he fights.""")

w('Splinter Volley', """The same damage rate as Briny Bolt with no rider, in a different physical type. The option of a second target for a third action is of no use through Spellstrike. Learn Briny Bolt first; this adds nothing to it.""")

w('Sticky Fire', """Low damage and a minor debuff that lasts only until a flat check ends the fire. Improving every second rank, it is behind from the start and further behind in every higher slot.""")

w('Summon Elemental', """Three actions to cast and one every round after leaves no room for Spellstrike and recharging, and a creature summoned from a low slot contributes little. Summoning does not fit a magus's turn.""")

w('Translate', """When no one shares a language it is the only way to talk or read at all, and for the party's negotiator that can decide an encounter. It still belongs on a scroll or a wand, because the need is occasional and never urgent to the minute.""")

w('Vomit Swarm', """Solid area damage against Reflex in a cone, which is the easiest shape to use through Expansive Spellstrike: Cyrus points it away from his allies and catches whatever stands behind the target. The sickened rider is the best debuff among the rank-2 area spells, lowering the attacks, saves and AC of everything that fails for as long as it lasts.

The rider needs a failed save, which is far from certain against capable enemies. Ignite Fireworks deals the same damage and dazzles even on a success, so it is the steadier choice; this is the better one against crowds of weak enemies that will fail often.""")

w('Water Walk', """A crossing solved for ten minutes. Buy the scroll when a river or harbour is in the way.""")

w('Web', """The firmest area control at this rank, and the cost is a full turn with no Strike. At a doorway or corridor it can hold a group in place for most of a fight, and that is worth the turn. In the open, enemies walk round it or burn it away.

Entangling Flora covers more ground for two actions where plants grow. For a magus this is a first-round spell for a prepared position and little else.""")

w('Marvelous Mount', """Travel convenience for one person. It has no bearing on a fight and rarely beats hiring a horse.""")

w('Blazing Armory', """It arms someone with a weapon they did not bring. Cyrus fights with his own weapon in both hands, and any ally who needs a weapon has brought one.""")

w('Binding Muzzle', """A narrow answer to creatures that depend on a bite or a breath weapon. Against those it is strong, because even a successful save closes the mouth for a round, and at long range. Against anything that fights with weapons, claws or spells cast without speech it does nothing.

That narrowness makes it a scroll to carry when such an enemy is expected.""")

w('Spray of Salt', """The hardest-hitting Fortitude area spell at this rank, in a short cone that is easy to steer away from allies through Expansive Spellstrike. It has no rider against ordinary enemies, so it is simply damage against a save that slow, heavily armoured enemies pass and spellcasters and skirmishers fail.

The cone is small and will rarely catch more than two or three enemies, and acid is a damage type his other spells already cover. Choose it over Disorienting Flash when the slot is wanted for damage, and Disorienting Flash over it when flexibility matters more.""")

w('Blood Runs Cold', """A Fortitude spell that takes an action from a single enemy if it fails. Against one strong enemy a lost action is worth more than the small damage that comes with it, and persistent cold keeps the slow going on a critical failure.

A successful save reduces it to a few points of damage, and against a strong single enemy that is the common result. Slow at rank 3 costs the target an action even on a success, so this is a stopgap for levels 3 and 4 against enemies with poor Fortitude, and has little use afterwards.""")

w('Unrelenting Gravity', """Its strength is the effect on a successful save: a round of being slower and easier to hit. Its headline effect, knocking the target prone, needs a failure. Dimensional Drop puts a grounded enemy prone even when it saves, which makes that the better spell for the same job in most fights.

This one earns consideration against flying creatures, which it brings down on a failure, and against enemies whose Fortitude is clearly worse than their Reflex. In a rank-4 slot it reaches five targets, which changes its value considerably.""")

w('Disorienting Flash', """Three sizes of Fortitude area damage from one prepared slot, which matters to a caster with only two slots at the rank. The two-action burst is the version to use with Spellstrike. The one-action version fits a turn in which he has already used Spellstrike. The three-action version reaches a group he cannot get to in melee. Dazzled is a worthwhile rider, since it gives each of the enemy's attacks a chance to miss.

The burst is harder to keep off allies than a cone, the rider needs a failed save, and its damage is a little behind Spray of Salt. Pick it for the day when he does not know what the fights will look like.""")

w('Ignite Fireworks', """The most reliable debuff among the rank-2 area spells, because the dazzle lands on a successful save. Against strong enemies a success is the result he should plan around, and a round in which several enemies each risk missing is worth more than the light damage. On a failure the dazzle lasts most of a fight.

Its burst needs care through Expansive Spellstrike when allies stand beside the target, since they are dazzled too. It is another Reflex spell in a list already heavy with them. Vomit Swarm matches the damage with a stronger rider that needs a failure; this one is the safer pick against tough enemies.""")


# ───────────────────────── cantrips ─────────────────────────
w('Gouging Claw', """His default spell for Spellstrike, and the reason a magus never runs out of things to cast. It has the highest damage of any cantrip, it rides the Strike's attack roll so it is as accurate as his weapon and doubles on the same critical hit, and its touch range stops mattering because Spellstrike delivers it at reach. The bleed keeps working through the turn he spends recharging.

The choice of slashing or piercing covers most physical resistances. Its one blind spot is creatures that do not bleed and resist both types, which is when Ignition takes over. Prepare it every day.""")

w('Ignition', """The second attack cantrip to learn, and the one to reach for when fire is what the enemy fears. Delivered at reach it uses its larger melee dice, so through Spellstrike he always gets the better version, and fire is the energy weakness met most often.

It trails Gouging Claw slightly on ordinary targets and has no rider unless the Strike is a critical hit. It also doubles as a ranged cast at 30 feet on a turn when nothing is in reach, which Gouging Claw cannot do. Prepare both; choose between them by the target.""")

w('Needle Darts', """An attack cantrip with two real advantages over the others. It takes on the metal it is cast from, so a silver coin and a cold iron nail in his pouch let him strike a material weakness without owning a second weapon, and its 60-foot range makes it his best direct cast when he cannot close.

Its damage sits a little behind Gouging Claw's on a target with no weakness, and piercing duplicates what Gouging Claw already offers. Worth a cantrip slot once he carries the metals; before that, Ignition is the more useful second pick.""")

w('Live Wire', """The only attack cantrip that still does something when the Strike misses, which smooths out the bad rolls that hurt a Spellstrike turn most. That makes it a sensible choice at low levels and against enemies with high AC.

It grows at half the rate of Gouging Claw and Ignition, so by level 7 or so the reliability no longer makes up the gap. Electricity is a useful third energy type. A good early cantrip that he will swap out later.""")

w('Frostbite', """His save-based cantrip for enemies whose AC is the problem. A heavily armoured target with poor Fortitude takes this even when the Strike misses, and cold is a damage type none of his attack cantrips provide. Its 60-foot range also makes it a respectable direct cast.

It hits less hard than the attack cantrips, and a successful save halves it, so against most targets Gouging Claw remains the better choice. Keep it prepared for the fights where the Strike is unlikely to land.""")

w('Electric Arc', """A fine cantrip for a full caster and a compromised one for him. Through Spellstrike only the creature he hits is affected, which throws away the second target that makes the spell good. What remains is a direct cast against two enemies on a turn when he cannot reach melee, and electricity as a damage type.

That is enough to keep it for days with fliers or enemies across difficult ground. It cannot go into a Spellstrike, and on most days Needle Darts covers the ranged turn better.""")

w('Void Warp', """A second Fortitude cantrip that does nothing to anything that is not alive, where Frostbite hurts everything. The rider only appears on a critical failure, which is rare. No reason to take both, and Frostbite is the one to take.""")

w('Telekinetic Projectile', """A choice of physical damage types from one cantrip, depending on the object thrown. Gouging Claw already gives two of the three with more damage and a bleed, and this needs a loose object within range. Only bludgeoning sets it apart, and his attack spells seldom need it.""")

w('Tangle Vine', """A spell that trades damage for control. The Strike still deals its own damage, and a hit slows the target on top, with a critical hit rooting it in place. Against an enemy trying to get past him to the back line, or one that keeps stepping out of reach, that can be worth more than a cantrip's dice, and it scales to last longer.

It is situational, and the enemy can break free with an action, although that action is one it does not spend attacking. Worth knowing for fights with skirmishers; Gouging Claw is still the everyday choice.""")

w('Caustic Blast', """The cheapest burst he can put through Expansive Spellstrike, and too weak to justify it. The damage is low, it improves every second rank, and the small burst rarely catches a second enemy without catching an ally. Slot spells do this job properly.""")

w('Scatter Scree', """Light damage and a patch of difficult terrain. Its area is not a burst, cone or line, so even with Expansive Spellstrike it only roughens the target's own space. Cast directly it can slow movement through a doorway, which is a minor use for a cantrip slot.""")

w('Daze', """The only cantrip that targets Will, with weak damage and a stun that needs a critical failure. It is worth having only if he wants every save covered at cantrip level, or needs to subdue someone without killing them.""")

w('Shield', """One action, no free hand, and a point of AC for the round, which fits a two-handed fighter with a spare third action better than anything else on the list. The block is the real prize: it can take the edge off a spell or a single heavy hit, something an ordinary shield cannot do against magic.

Blocking uses his reaction, so from level 6 it competes with Reactive Strike, and once used the spell is gone for ten minutes. Even so, the AC alone is worth the action on any turn that does not need a Stride or a recharge. Prepare it every day.""")

w('Detect Magic', """Not a combat spell, and still one of the most useful cantrips in the game. Knowing whether a room, a door or a stranger carries magic prevents a good share of the party's avoidable mistakes, and he is the natural person to cast it as the party's Arcana specialist.

It tells him only that magic is present until it is heightened. If another caster already keeps it running he can spend the cantrip elsewhere; if not, it belongs on his list for any day of exploration.""")

w('Figment', """A small illusion that is worth more to a talker than to a fighter. A noise down a corridor or a shape at a window gives him a bonus to Create a Diversion and draws a guard's attention at range, which suits the way he approaches infiltration and negotiation.

It is crude up close and needs sustaining, so it is a distraction, never a disguise. Aspera's stave is planned to carry it from level 8, which gives him the option without a cantrip slot.""")

w('Telekinetic Hand', """Moves a small object from a safe distance: a key off a hook, a lever, a suspicious box. Handy during exploration, with no use in a fight, and a ten-foot pole or a careful ally covers most of the same ground.""")

w('Message', """Silent, one-action communication across a room or a courtyard. For a party that plans, splits up or works a social scene it is very useful: a warning to a scout, a cue during a negotiation, a question nobody else should hear.

It does nothing in a fight beyond coordination. As the party's face he gets more from it than most, and it costs one of only a handful of cantrip slots. Keep it on days built around stealth or talking.""")

w('Time Sense', """Knowing the exact time has occasional uses for coordinating a plan, and the small bonus it offers almost never applies. It suits Aspera's theme, which is why it is the stave's cantrip, and it does not merit a prepared slot.""")

w('Eat Fire', """A reaction that blunts one fire effect and leaves him with a puff of smoke to use. The resistance is small, it competes with Reactive Strike, and it only matters against one damage type. A scroll of Resist Energy answers a fire-heavy day far better.""")

w('Gale Blast', """A small burst around himself that can shove adjacent enemies back to the distance where his reach weapon works best and theirs do not. That is a neat fit for a reach fighter in principle. In practice the damage is poor, the push needs a failed save, and a Step achieves the same spacing for one action.""")

w('Puff of Poison', """A Fortitude spell whose persistent damage keeps going while he recharges. Poison is among the most commonly resisted types, the range is very short, and it grows only every second rank. Frostbite is the better Fortitude cantrip in nearly every fight.""")

w('Spout', """A Reflex cantrip whose rider, making the target off-guard, would feed Laughing Shadow nicely, except that it needs a critical failure. Without that it is plain low damage that improves slowly. Not worth a slot on the chance.""")

w('Slashing Gust', """It needs a free hand, and two free hands to reach a second target. He fights with both hands on his weapon, so he cannot use it with Spellstrike at all.""")

w('Timber', """A short line of Reflex damage with a rider on a critical failure only. A line that short seldom reaches a second enemy even through Expansive Spellstrike, and the damage is ordinary. Slot spells make far better area attacks.""")

w('Phase Bolt', """An attack cantrip that partly ignores shields and cover, which is a real advantage against a few enemies and none against the rest. Its damage falls behind Gouging Claw's as he levels. Consider it only when shield-users or enemies behind cover are the day's problem.""")

w('Glass Shield', """The same AC as Shield with a much weaker block and a little damage to whoever breaks it. Shield's higher Hardness is what makes blocking worthwhile, so this is the worse version of a cantrip he already wants.""")

w('Warp Step', """Two Strides for two actions with a small Speed bonus that does not stack with the one Laughing Shadow already gives him in stance. He would be paying a cantrip slot for nothing he does not have, and Dimensional Assault covers repositioning far better.""")

w('Light', """He cannot see in the dark, so he needs light on many days, and this provides it hands-free until his next preparations. A torch or an everburning torch does the same without using one of his few cantrip slots, which is the only reason it is not prepared daily.

Take it on a day underground if nobody else in the party is carrying light; a movable light at 120 feet is also a decent way to see what is ahead without walking into it.""")

w('Prestidigitation', """Cleaning, warming, tidying and small flourishes. It has some charm in social scenes where appearance counts, and no effect on anything that matters mechanically. A luxury for a character with cantrip slots to spare, which he does not have.""")

w('Read Aura', """Tells him whether an object is magical and makes identifying it easier, and he is the party member most likely to be doing the identifying. It takes a minute, so it belongs to the quiet after a fight.

Detect Magic answers the first half of the question faster, and the bonus here is modest. Prepare it on days when the party expects to sort through loot or search a magical site; otherwise leave it in the book.""")

w('Infectious Enthusiasm', """Two actions for a one-point bonus that lasts a round, and allies must spend actions of their own to share it. For a class that needs every action for Spellstrike and recharging, that is far too expensive.""")


# ───────────────────────── rank 1 ─────────────────────────
w('Sure Strike', """The single most valuable rank-1 spell for a magus. A Spellstrike puts a whole turn's damage on one attack roll, and this lets him roll that attack twice. It raises the chance of a hit and, more importantly, the chance of a critical hit that doubles both the Strike and the spell. It also cuts through concealment, which otherwise costs him one attack in five.

It costs an action, so it belongs on a turn where he starts within reach with Spellstrike charged, and it works once per fight. With one or two fights a day, his two rank-1 slots cover exactly that. Prepare it in both until higher slots free one up.""")

w('Thunderstrike', """A dependable single-target spell that keeps pace in any slot, since it gains a full set of dice with every rank. Because it runs on a Reflex save it still does half damage when the target succeeds, and it applies even when the Strike misses. Against an enemy in metal armour it is better still, since such enemies save at a penalty and come out of it easier to hit.

It has no rider otherwise, and quick enemies will often halve it. Sudden Bolt hits harder from rank 2 up; this stays the standard save-based damage spell for his lower slots and a good scroll for a ranged turn at 120 feet.""")

w('Dehydrate', """Weak in a rank-1 slot and one of the best heightened damage spells he has. Each two ranks add a great deal of persistent fire and widen the burst, and persistent damage keeps landing through the turns he spends recharging. Enemies also have to keep saving or become enfeebled, which blunts the ones that hit back in melee.

Its real damage arrives over several rounds, so it suits long fights against durable enemies and wastes itself on anything that will die quickly. The burst will catch allies through Expansive Spellstrike. Learn it early and prepare it from rank 3 upward.""")

w('Fear', """The best debuff he can deliver for the slot, because it works on a successful save. A frightened enemy is worse at everything for a round or more: easier to hit, easier to affect with the next spell, less accurate in return. Through Spellstrike that comes on top of a Strike, and every ally who acts before it wears off benefits.

From a rank-3 slot it covers five enemies as a direct cast, which is a strong opening against a group. Mindless creatures and anything immune to fear ignore it, so it needs a backup on such days. Keep one prepared at most levels.""")

w('Fleet Step', """A large Speed bonus for a minute. Useful for a chase, a race to an objective, or a fight on a very large map, and largely wasted elsewhere, because Dimensional Assault and his reach already solve most positioning problems. As a status bonus it replaces Laughing Shadow's Speed bonus instead of adding to it. Prepare it for a known need.""")

w('Tailwind', """An all-day Speed bonus from a rank-2 wand is a staple for most characters. For him it is worth less than usual, since it overlaps the status bonus Laughing Shadow gives in stance. It still helps on the turn before he has entered Arcane Cascade and all day outside combat, which is enough to justify the wand and never a slot.""")

w('Grease', """A cheap way to knock several enemies prone at once, which leaves them off-guard for Laughing Shadow and for every melee ally, and costs each an action to stand. It works best cast directly over a doorway or a tight group in the first round. Through Spellstrike it loses most of its area.

It depends on failed Reflex saves, and enemies with good balance barely notice it. A reasonable rank-1 slot against clumsy or heavily armoured groups; otherwise Fear does more.""")

w('Befuddle', """A setup spell. Even on a successful save the target is easier to hit and worse at casting for a round, and the clumsy condition also lowers the Reflex DC his Trip is rolled against. The effect is over quickly, so its worth depends on the party acting on it straight away.

Fear gives a similar penalty that applies to more of what the enemy does and fades more slowly. This is the better choice specifically against a spellcaster, where stupefied can make its next spell fail. Mindless creatures are immune.""")

w('Briny Bolt', """The best attack spell he can learn at low level. Every hit blinds the target for a round unless it spends an action clearing its eyes, so the enemy either loses an action or attacks with a coin-flip chance to miss, and a blinded enemy is off-guard to the whole party. That rider rides his Strike's roll, with no save to resist it, and the damage keeps growing with each rank.

It needs a creature with eyes to matter, and bludgeoning is the least exciting damage type. Prepare it in whichever rank is not holding Sure Strike, and keep heightening it.""")

w('Shocking Grasp', """Heavy attack-roll damage, a little ahead of Briny Bolt at every rank, and better again against enemies in metal armour, where it gains accuracy and leaves persistent damage behind. Its touch range is no drawback through Spellstrike.

It has no rider against other targets, so on most days Briny Bolt's blind is worth more than the extra dice. Choose this when the fight is about finishing one enemy quickly, when electricity is the weakness, or when the enemy is wearing plate.""")

w('Force Barrage', """It cannot be delivered by Spellstrike, since it has neither an attack roll nor a save. What it offers is damage that cannot miss, at long range, which is useful for finishing a fleeing enemy or breaking a spellcaster's concentration. That is a job for a wand or scroll, not for one of his slots.""")

w('Breathe Fire', """The basic cone for Expansive Spellstrike, with damage that keeps pace by rank and nothing else to recommend it. The cone is short, so it rarely catches more than two enemies. Fine as a first area spell at level 2 to 4; better cones replace it quickly.""")

w('Dizzying Colors', """Capable of ending the turns of several weak enemies at once, and unreliable against anything that matters. Incapacitation makes strong enemies treat their saves as a step better, and failures are far from certain even among the rest. The dazzle on a success is some compensation.

Its place is a fight against a crowd of lower-level enemies, with the cone pointed away from allies. Against a single strong enemy it is a wasted slot.""")

w('Pummeling Rubble', """A small cone of weak damage that pushes enemies directly away from him, which a reach fighter seldom wants. Acid Grip moves an enemy where he chooses and does it on a successful save. This has no place once that is available.""")

w('Gust of Wind', """Modest at low level and important from level 12. Until then it is a line that knocks down what fails a Fortitude save and stops fliers and archers behind it, useful mainly for clearing fog or holding a corridor.

With Sprinting Spellstrike it becomes the cheapest way to cross sixty feet without provoking reactions and leave a row of prone, off-guard enemies along the way, all from a rank-1 slot. It does nothing to Huge creatures and needs failed saves to knock anything down. Learn it by 12 and keep a copy prepared from then on.""")

w('Goblin Pox', """A debuff that still sickens on a successful save, delivered at reach through Spellstrike. Sickened lowers everything the enemy rolls and lingers until it spends an action retching, so in a long fight against one living enemy it pays back well.

Fear does the same job on more kinds of enemy and fades by itself. This is the alternative for targets immune to fear, as long as they are alive and can catch a disease.""")

w('Leaden Steps', """A setup spell for electricity. The weakness it creates adds to every later hit from Thunderstrike, Shocking Grasp or a shock rune, and the encumbered target is slower and easier to hit, which helps keep it inside his reach.

Keeping it going costs a sustain each round, which competes with recharging, and on a successful save it lasts only a moment. It pays off in a party that leans on electricity; cast by him alone, the setup turn usually costs more damage than the weakness returns.""")

w('Command', """It does nothing on a successful save, and against a capable enemy that is the likely result. When it works it wastes one enemy action. Fear costs the same slot and always achieves something.""")

w('Curse of Slippery Steps', """It hampers one enemy's movement. That can spoil a charge or slow a runner, but it does not stop the enemy attacking, and Tangle Vine does a similar job as a cantrip. Not worth a slot.""")

w('Hydraulic Push', """Decent attack-roll damage with a shove attached. Through Spellstrike the push can break a grapple on an ally, move an enemy into a waiting ally's reach or off a ledge, and it is settled by the Strike's roll.

The push is always straight back and only five feet on a normal hit, where Acid Grip moves a target in any direction and works on a save. Briny Bolt is the better attack spell for general use. This earns a place only where knocking something backward is the point.""")

w('Grim Tendrils', """A low-damage line against Fortitude that harms only the living. It is one of the few rank-1 lines, which gives it a small role with Sprinting Spellstrike, but Gust of Wind fills that role with a far better effect.""")

w('Horizon Thunder Sphere', """A sound attack spell in its two-action form: electricity damage close to Shocking Grasp's, delivered on the Strike's roll. That gives him a second electricity option that grows every rank.

Its other casting modes do not suit him. The three-action version leaves no room for a Strike and the two-round version is too slow for a class that fights in bursts. With no rider on a normal hit, Briny Bolt usually does more for the fight. Learn it only if he wants electricity without Shocking Grasp's touch range for direct casts.""")

w('Mystic Armor', """It replaces armour he already wears. It would matter only if he gave up medium armour for the larger unarmoured Speed bonus from Laughing Shadow, and that trade costs too much AC for a front-line fighter.""")

w('Jump', """A one-action leap that clears a gap or reaches a ledge. It helps on broken ground before he has Fly, and Dimensional Assault already handles most short repositioning. A scroll at most.""")

w('Gentle Landing', """It turns a lethal fall into nothing, for anyone within 60 feet, as a reaction. Most falls happen outside combat, on a climb or a bridge, where his reaction is free anyway.

The need is rare and total when it comes, which is the profile of a scroll: held in hand while the party climbs, it is the cheapest insurance he can buy. A prepared slot is justified only for a day of flying or cliffs.""")

w('Interposing Earth', """A defensive reaction that makes one attack or blast less likely to hurt and slightly smaller if it does. Before level 6 he has nothing else to do with his reaction, so a spare rank-1 slot spent here is reasonable.

From 6 it competes with Reactive Strike and usually loses, and the protection is small next to Hidebound or Warping Pull at rank 2. An early-levels spell.""")

w('Illusory Object', """One of the most flexible utility spells he can know. A false wall, a closed door where there is an open one, a crate to hide behind: it solves escapes, ambushes and infiltration problems that no combat spell touches, and at rank 2 it holds up to touch and sound for an hour.

It has no direct use in a fight and needs a little imagination and a little time. Aspera's stave is planned to carry it from level 8; before then a scroll is the right way to have it on hand.""")

w('Illusory Disguise', """A disguise for planned infiltration, better in higher slots, where it can copy a specific person or cover the whole party. For the party's talker that is a real tool. It is never needed at a moment's notice, so a scroll, or later the stave, covers it.""")

w('Helpful Steps', """A staircase or ladder the whole party can use, which is far cheaper than giving everyone a way to fly or climb. It solves a wall or a pit completely and has no other use. Scroll.""")

w('Runic Weapon', """It grants runes his weapon already has. It matters only if he is disarmed or forced to fight with a borrowed weapon, and even then it costs two actions.""")

w('Conductive Weapon', """A minute of extra electricity damage on a metal weapon, more against armoured enemies. Cast before a fight it adds a little to every Strike, his or an ally's. Two actions in a fight are never worth it, and a permanent rune does the same job later.""")

w('Friendfetch', """Pulls one or two allies straight to him, which can drag someone out of a grapple, a hazard or an enemy's reach without costing them an action. That is a real rescue tool on the day it is needed, and an idle slot otherwise. A scroll suits it.""")

w('Pocket Library', """A day-long bonus to Recall Knowledge in one skill, with no critical failures. He identifies enemies for the party, and knowing a creature's weak save decides which spell he uses, so the benefit is real. It lasts 24 hours, which makes it ideal for a wand cast each morning.""")

w('Schadenfreude', """It only triggers when he critically fails a save, which he cannot plan for and hopes never happens. A slot held for his own worst moments is a slot wasted in every fight that goes well.""")

w('Acidic Burst', """One of the best damage rates of any save spell, and awkward to use as written, since cast normally it burns every ally standing next to him. Spellstrike solves that. Delivered through a Strike it affects only the target, at reach, and becomes a strong single-target Reflex spell in acid that keeps pace in every slot.

It has no rider, and it competes with Thunderstrike and later Sudden Bolt for the same job; the choice between them is mostly about damage type. Do not cast it directly unless he is surrounded by enemies alone.""")

w('Agitate', """A spell that punishes an enemy for standing still, which suits a fighter with reach and Reactive Strike. A target that must move each turn or take damage either gives up position or provokes, and it has an effect even on a successful save.

The damage is modest and avoidable, and an enemy that wanted to move anyway loses nothing. It is best against an archer or caster that has found a safe spot, and against anything standing inside his reach from level 6. Mindless creatures are immune.""")

w('Alarm', """A warded campsite for the night. It is the textbook wand spell: cast every evening, it protects every rest for no slot. In a prepared slot it would cost him a Sure Strike, which is not a trade worth making.""")

w('Ant Haul', """Extra carrying capacity for a day. With his Strength he is rarely the one who needs it.""")

w('Anticipate Peril', """A small initiative bonus on one roll. He already invests in initiative through Incredible Initiative, and a rank-1 slot spent on Sure Strike does far more once the fight has begun.""")

w('Carryall', """A floating platform for cargo. Convenient for hauling loot and irrelevant otherwise; a pack animal or a spacious pouch does the job without a slot.""")

w('Charm', """A social spell for the party's negotiator, to be used with care. When it works it turns a guard, a clerk or a reluctant witness friendly for an hour, which opens doors Diplomacy alone might not. It fails outright against anyone the party has threatened, it carries incapacitation, and being caught casting it tends to end the conversation.

Success is uncertain, so it supplements his Diplomacy instead of replacing it. A scroll or wand suits it, since the need is occasional and never arises mid-fight.""")

w('Chilling Spray', """A small cone that slows what fails, with weak damage that improves slowly. The Speed penalty is rarely decisive, and Breathe Fire does more damage in the same shape.""")

w('Déjà Vu', """Clever against an enemy that has just wasted a turn, and nothing at all on a successful save. Incapacitation makes success the usual result against anything dangerous.""")

w('Draw Ire', """A taunt that works even on a successful save, discouraging one enemy from attacking anyone but him. He is not the party's most durable member, so inviting attacks is seldom what he wants, and the penalty is small.""")

w('Echoing Weapon', """Its damage builds with the number of Strikes made in a turn. He makes one or two, so he gets almost nothing from it; it belongs on someone who attacks three or four times.""")

w('Endure', """A few temporary Hit Points for one action at touch range. The amount is too small to change a fight, and any of his other rank-1 spells does more with the slot.""")

w('Enfeeble', """A defensive debuff in disguise. An enfeebled enemy hits less often and less hard and is worse at grappling and shoving, and some of that applies even on a successful save. Against a single brute that is hurting the front line it protects everyone it attacks.

Fear weakens more of what an enemy does and also helps the party land its own attacks, so it is usually the better pick. This is the choice against enemies immune to fear or mental effects, provided they rely on Strength.""")

w('Flourishing Flora', """A tiny burst with a choice of damage type and a rider only on a critical failure. The damage is poor and the area too small to justify Expansive Spellstrike. Flexibility of type is better bought with cantrips.""")

w('Gravitational Pull', """A one-action pull, which is what makes it interesting. On a turn when he has already used Spellstrike it can drag an archer or caster into his reach, set up Reactive Strike, or pull an enemy off an ally, all for his third action. It can also go into a Spellstrike, though better spells exist.

It does nothing on a successful Fortitude save, so big, sturdy enemies ignore it. Light, fragile targets are exactly the ones he wants to pull, which makes it a fair use of a low slot once his main spells sit in higher ranks.""")

w('Kinetic Ram', """It pushes enemies away from him, which is the opposite of what a reach fighter with Reactive Strike usually wants. The one-action version can free an ally from a grapple or clear a space. Gravitational Pull is the more useful member of this pair.""")

w('Mending', """Repairs a broken mundane object over ten minutes. A repair kit does the same, and he is trained in Crafting.""")

w('Mindlink', """Ten minutes of explanation delivered in a moment. Occasionally handy for briefing someone under time pressure or in silence; Message covers most of the same need for a cantrip.""")

w('Mud Pit', """Difficult terrain over a good area with no save, which is reliable, and nothing more than that. It costs a full turn. Entangling Flora and Web do more to the creatures inside.""")

w('Noxious Vapors', """A small poison cloud around himself that hurts allies as readily as enemies and hides everyone inside from everyone else. The concealment helps and hinders in equal measure, and poison is widely resisted.""")

w('Penumbral Shroud', """It dims the light for one creature. That might help an ally who is sensitive to light or hinder a sentry slightly. He has no regular use for it.""")

w('Pest Form', """One of the best scouting tools he can have. A rat or a sparrow passes unremarked in places where an invisible intruder would be noticed by scent or sound, and ten minutes is long enough to look round a building. From rank 4 the form can fly.

He cannot attack or cast while changed, and a scout who is caught is alone and tiny. It belongs on a scroll or wand for the days that call for reconnaissance, where its value is high.""")

w('Phantasmal Minion', """A servant that fetches and carries. It costs a full turn to summon and an action each round to direct, and it has no use in a fight.""")

w('Shattering Gem', """A coin-flip chance to block one hit for an ally before it breaks. Two actions and a slot for protection that fails half the time is poor value beside Hidebound or Warping Pull.""")

w('Shockwave', """A cone that sets up the whole party's melee. Enemies that fail fall prone, and even those that succeed are off-guard for a round, so every result short of a critical success switches on Laughing Shadow's extra damage and makes his allies' Strikes easier. Through Expansive Spellstrike the cone points away from his own side.

It deals almost no damage, so it is a setup turn and should be cast when allies are positioned to follow it. It does nothing to creatures that are flying or otherwise off the ground. A good rank-1 slot from level 4.""")

w('Sleep', """Weak in a fight, where a sleeper wakes at the first loud noise or blow, and it carries incapacitation. Its use is quiet work: putting a sentry out before anyone raises an alarm. That is a scroll's job.""")

w('Snowball', """An attack spell with a slowing rider, which sounds better than it plays. Its damage falls well behind Briny Bolt and Shocking Grasp as it heightens, and Briny Bolt's blind is the stronger effect.""")

w('Spider Sting', """Poison damage and a weakening effect that both depend on failed Fortitude saves over several rounds. Poison is widely resisted, so the full effect is rare. Enfeeble does the debuff more reliably.""")

w('Summon Animal', """A full turn to cast, an action every round to keep, and a creature too weak to threaten anything he is fighting. Summoning does not fit the way a magus spends actions.""")

w('Tether', """Keeps one enemy close. A runner, a skirmisher that keeps retreating out of reach, or a caster trying to back away is held within 30 feet with its Speed reduced, and a critical failure roots it. For a fighter who wants enemies inside his reach that has clear uses.

It does nothing on a critical success and little on a success, and the tether can be cut. It is a niche pick for fights where the enemy's plan is to stay away from him; Tangle Vine offers a lighter version as a cantrip.""")

w('Thoughtful Gift', """Sends a potion or scroll across the battlefield into an ally's hand for one action. Occasionally that saves a life. Usually the ally could have drawn their own.""")

w('Ventriloquism', """Throwing his voice supports a diversion or a bluff. It suits his role as the party's talker in a small way, and Figment covers the same ground as a cantrip.""")

w('Wall of Shrubs', """Light cover along a long line, improving in higher slots. It can shield the party from archers or screen a withdrawal, and it costs a whole turn. Later walls do the job far better.""")

w('Propelling Air Stream', """An attack spell that also lifts him off the ground. Through Spellstrike the damage rides the Strike, and whether or not it hits he can fly for a turn, which reaches an enemy on a ledge, crosses a gap, or puts him above difficult ground. Its damage keeps pace with Briny Bolt's.

The flight is brief and slow, and it has no effect on the target beyond damage, so on level ground Briny Bolt is better. Learn it for fights with height in them before Fly is available.""")


# ───────────────────────── rank 3 ─────────────────────────
w('Haste', """The best buff he can cast, on himself or on an ally. A magus's turn is always one action short: Stride, Spellstrike and recharge do not fit in three. The extra Stride or Strike each round fixes that for a whole fight, letting him close and Spellstrike in the same turn, or Spellstrike and still make a second Strike.

It costs two actions up front, so it belongs in the first round, ideally while the enemy is still out of reach. From level 11 it is a studious spell and comes with a free Arcane Cascade, which removes most of that cost. On a melee ally who attacks more often than he does it can be worth even more. Prepare one from the level he gains rank-3 slots.""")

w('Slow', """The strongest single-target control spell he can deliver, because it works on a successful save. One action lost for a round is a third of an enemy's turn, and that is the floor; a failure takes it for the whole fight. Through Spellstrike it comes on top of a Strike, with no sustain and no incapacitation.

It is aimed at Fortitude, which is usually the best save of large, dangerous enemies, so failures will be uncommon against exactly the targets he wants it for. The success effect is still worth the slot. Against a group it waits for rank 6, when it reaches ten targets. Keep one prepared for any day with a serious single enemy.""")

w('Time Jump', """Two moves for one action that nothing can react to. It gets him out of a surround, past a front line to the caster behind it, or up to a target with two actions still in hand for Spellstrike, and it ignores Reactive Strike from the enemy entirely.

Dimensional Assault already gives him a teleport and a Strike from his Focus Points, so this is the second answer to the same problem, for fights where one reposition is not enough or the distance is too great. A slot well spent on large or crowded battlefields; a luxury on small ones.""")

w('Lightning Bolt', """His main line spell and one of his best spells. The damage is high and grows every rank, and a line through Expansive Spellstrike is the easiest area to keep off allies: it starts beside the target and runs away from the party through whatever stands behind. Even with a single enemy in it, it is strong single-target Reflex damage.

From level 12 it is the natural spell for Sprinting Spellstrike, carrying him along its length. It has no rider and electricity is occasionally resisted. Prepare it from level 5 and keep heightening it.""")

w('Fireball', """Excellent for a full caster and awkward for him. Its damage and its enormous range are as good as ever when cast directly at a group across the battlefield, which is a fair use of a turn before melee is joined.

Through Spellstrike it is a problem. A 20-foot burst centred beside his target covers him and any ally nearby, so he can rarely afford to use it that way. Lightning Bolt and Crashing Wave put similar damage into shapes he can control. Learn it for the direct cast if a slot is spare; do not build turns around it.""")

w('Cave Fangs', """Fireball's damage in piercing, with difficult terrain left behind for the fight. Physical damage gets past the elemental resistances that blunt fire, and the terrain slows enemies trying to cross it to reach the party.

It shares Fireball's fault through Spellstrike, since the burst is too large to place around his own position, and its range is much shorter. Cast directly in the first round at a group that has to come through it, it is a strong opener. Otherwise his cone and line spells serve him better.""")

w('Blindness', """Crippling when it lands and marginal when it does not. A blinded enemy for a minute is effectively out of the fight; a successful save reduces that to a moment, and incapacitation hands strong enemies a better result still.

So it is a spell for enemies at or below his level with poor Fortitude, such as spellcasters, and for those it is among the best spells available. Against a single powerful enemy Slow is far more dependable. Briny Bolt offers a round of blindness on a hit with no save at all.""")

w('Paralyze', """Very strong against an enemy of his level or lower. Even a successful save costs the target an action, and a failure leaves it helpless for a round, off-guard and open to critical hits from the whole party.

Incapacitation limits it. Against anything above his level the save improves by a step and the spell mostly fails, and those are usually the enemies he most wants stopped. It is also mental, so mindless creatures are immune. Prepare it for fights against several dangerous equals; use Slow for the single big threat.""")

w('Blister Bomb', """A debuff that lands hard even when the enemy saves. Sickened 2 on a success is a heavy penalty to everything the target rolls, and it applies to each creature in a small burst that is easy to place through Expansive Spellstrike without touching allies. The whole party hits more often and is hit less until the enemies spend actions shaking it off.

It deals no immediate damage, so it is a setup for a longer fight, and creatures immune to disease ignore it. Against two or three tough living enemies it is one of the best uses of a rank-3 slot.""")

w('Earthbind', """A direct answer to a flying enemy, which he otherwise struggles to reach. Even a success brings the creature down for a moment. It has no other use, so it lives on a scroll, where it has saved many melee characters' days.""")

w('Magnetic Acceleration', """Attack-roll damage at the same rate as Briny Bolt, split across two physical types, with nothing added. Its accuracy bonus against metal applies to the spell's own roll, so through Spellstrike it is unlikely to help.

Its long range makes it a respectable direct cast when he cannot reach melee. Through Spellstrike, Briny Bolt does the same damage and blinds. Learn it only for the ranged turn.""")

w('Widow’s Bite', """The only worthwhile spell for Spellstrike that lacks the manipulate trait. Casting it does not trigger Reactive Strike and cannot be lost to the flat check for being grabbed, so it is the Spellstrike for the turn when a large enemy with reach, or one that has hold of him, makes any other spell a risk. The effect suits the same enemies: the target is enfeebled for as long as the poison lasts, decided by the Strike's roll with no save, and the persistent damage keeps working while he recharges.

Poison is the most commonly resisted damage type and many creatures are immune, which removes the enfeebled effect with it, and the spell grows only every second rank. Prepare it against living brutes; Briny Bolt is safer against an unknown enemy.""")

w("Eagle's Cry", """A cone that damages and frightens in one cast, and the fear lands on a successful save. Every enemy caught is worse at attacking and defending for at least a round, on top of respectable sonic damage, and a cone is easy to aim through Expansive Spellstrike.

It targets Fortitude, so big enemies will often take the half-damage result, which still frightens them. It does not improve its fear in higher slots. For a group fight this is among the best rank-3 spells.""")

w('Wooden Double', """Insurance against the worst moment of a fight. He chooses to use it after a critical hit has been rolled against him, so it never wastes a reaction on an ordinary blow, and it turns a doubled hit from a powerful enemy into damage on a block of wood.

It competes with Reactive Strike only in the rounds when he is critically hit, which is when he would rather be alive. One low or middle slot kept for this is good value in any fight against an enemy above his level.""")

w('Ghostly Weapon', """Whether he can contribute against incorporeal enemies depends on this spell. Without ghost touch his weapon does a fraction of its damage to them; with it he fights normally for a whole encounter.

It is narrow, which would normally mean a scroll. From level 11 it is a studious spell, so it is in his book for free and grants Arcane Cascade when cast, which makes it a clean opening action on the right day. Carry a scroll until then, and prepare it when spirits are expected.""")

w("Cloud Dragon's Cloak", """A reaction that gives an ally a coin-flip chance to avoid a ranged attack, and every other ranged attack that round. Against archers or spell attacks focused on one ally it prevents a great deal for a single reaction.

It does nothing against melee, and it competes with Reactive Strike. Its best use is on days when the enemy fights at range and nothing is going to provoke him anyway.""")

w('Shadow Projectile', """A reaction that adds damage and a better chance to hit to an ally's ranged attack. In a party with archers or casters who use spell attacks it turns an idle reaction into some damage and a debuff.

It works once per enemy and needs the ally to be close. From level 6 Reactive Strike is the stronger habit for his reaction. A minor pick for a spare slot.""")

w('Agonizing Despair', """Damage and fear together against Will, with the fear applying even on a successful save. Through Spellstrike it adds a modest hit to the Strike and leaves the target frightened for the party's next attacks, and it keeps growing in higher slots.

It gives him a Will option that is not wasted when the enemy saves, which his list otherwise lacks. Mindless creatures and anything immune to fear or mental effects ignore it. Fear does the debuff alone for a rank-1 slot; this is for when he wants the damage too.""")

w('Aqueous Orb', """A rolling sphere that can swallow enemies, driven by a sustain each round. That action is the one he needs for recharging, and the orb achieves little unless it is moved every turn.""")

w('Clairaudience', """Listening through walls at a distance, for ten minutes. For a party that plans its approach it can reveal numbers, passwords or intentions before a door is opened. It takes a minute to cast and belongs on a scroll.""")

w('Cozy Cabin', """Shelter for a night in the wild. Comfortable, and without any bearing on a fight; a tent does most of the same work.""")

w('Crashing Wave', """Fireball's damage in a cone, in a type almost nothing resists. For him that shape is the point: through Expansive Spellstrike a 30-foot cone starts beside his target and spreads away from the party, so it is the area spell he can use most freely in a melee.

It has no rider. Lightning Bolt hits a single target harder and suits Sprinting Spellstrike later; this catches more enemies when they stand in a group. Worth learning alongside it.""")

w('Curse of Lost Time', """A debuff that makes a living target both easier to hit and weaker in return, with a brief version on a successful save. Clumsy also lowers the Reflex DC his Trip is rolled against. Against constructs and objects it deals damage instead, which gives it an unusual second use.

The lasting effect needs a failed Fortitude save, and the success effect is over in a round. Fear and Blister Bomb give more reliable penalties. A reasonable pick against constructs; otherwise marginal.""")

w("Day's Weight", """A long-range debuff that lowers a living enemy's AC, saves, attacks and damage together, and gives a round of it even on a success. On a failure it lasts the fight. The whole party benefits from the AC and save penalty, and the front line from the weaker attacks.

It deals no damage and aims at Fortitude, which strong enemies usually pass. Slow takes more from a single enemy for the same slot. This is the better opener when the party is about to throw spells of its own at the target, and at rank 6 it covers a whole group.""")

w('Dive and Breach', """Movement and area damage in one cast. He leaves one group, appears beside another and damages creatures at both ends, with an action left over. For a skirmisher that is an attractive turn when two clusters of enemies are within range.

Through Spellstrike he Strikes first and then dives, and only the creature he struck takes the damage, which is modest for the slot. Echo Jump does the same job with force damage and no Leap, so this is the second choice of the two; it moves him further and gains a die at every rank.""")

w('Dream Message', """A one-way message to anyone he has met, wherever they are. Useful for reports, warnings and requests between adventures, and never urgent. A scroll or a wand covers it.""")

w('Elemental Absorption', """A minute of resistance to one element with a counterattack attached. The resistance is small and the release costs two actions he would rather spend on a Spellstrike. Resist Energy protects better for longer.""")

w('Enthrall', """It holds a crowd's attention while he keeps talking, which can cover an ally's movements or buy time. It suits his role, needs sustaining, and does nothing against anyone already hostile. Occasional scroll use at most.""")

w('Gravity Well', """A setup spell for area damage. It drags everything in a wide burst towards one point, which bunches enemies for a following Lightning Bolt, Crashing Wave or an ally's blast, and can pull them off a ledge or out of cover.

It deals no damage and depends on failed Reflex saves to move anything far. It also costs him a turn without a Strike. It pays off when the party has area spells ready to follow it, and seldom otherwise.""")

w('Hypnotize', """A cloud that dazzles whatever is inside it and can hold weaker enemies fascinated. The dazzle needs no save, which is useful. Keeping the cloud in place costs a sustain every round, and fascination ends when anyone attacks the creature. More use against guards than in a fight to the death.""")

w('Impending Doom', """A slow-building curse on one living enemy that makes it off-guard, then frightened, and on a failure stunned and hurt at the end. Some of that happens even on a successful save, and off-guard feeds Laughing Shadow from the first round.

It takes three rounds to finish, which is longer than many fights last, and incapacitation weakens it against strong enemies. It is best opened early against a durable enemy of his own level. Mindless creatures are immune.""")

w('Levitate', """Slow vertical movement for one creature or object. It crosses a pit or lifts someone to a ledge, and the penalty to attacks while floating makes it useless in a fight. Gecko Grip and later Fly do the job better.""")

w('Locate', """Points the way to a specific object, and to a specific creature in a higher slot. When something has been stolen or someone has gone missing it can save a day of searching. The need is occasional, so a scroll is enough.""")

w('Mind Reading', """A tool for the party's negotiator. A glimpse of surface thoughts during an interrogation or a tense bargain can expose a lie or reveal what the other side wants, and that is information no skill check provides so directly.

It needs a failed Will save, and a target that succeeds may realise what was attempted, which has consequences in polite company. It suits a scroll kept for the conversation that matters.""")

w('Organsight', """Extra precision damage on his next piercing or slashing hit, bought with a Recall Knowledge check each round. He identifies enemies anyway, so the check is something he is good at, and the damage applies to a Spellstrike.

It costs two actions to set up and one each round to renew, and a magus has none to spare. The return is too small for that price except in a long fight against a single enemy.""")

w('Phantom Prison', """Removes one enemy from a fight for as long as the party ignores it, which against a group lets everyone concentrate on the rest. That is powerful when it holds.

It costs a full turn, has incapacitation, relies on a failed Will save, and breaks down each time the target tests the walls or is attacked. Too many ways to fail for a class that gives up a Spellstrike to cast it.""")

w('Safe Passage', """Protection for the party while crossing one stretch of dangerous ground. It answers a specific hazard and nothing else. A scroll if the route is known to need it.""")

w('Shared Invisibility', """The best way to move the whole party unseen. Ten minutes of invisibility for six people is enough to pass a guarded gate, cross open ground or set an ambush, and the first round of that ambush is worth a great deal with every enemy off-guard.

Everyone must stay close to him, and the first hostile act ends it for all, so it does not carry into the fight itself. It is a spell for a plan, and plans can be made around a scroll. Prepare it when the day's work is infiltration.""")

w('Stinking Cloud', """Area control that can decide a fight against a group. Enemies that stay in the cloud are sickened, and those that fail are slowed as well, which takes an action from every one of them each round. The concealment also shields the party from archers behind it.

The cloud does the same to allies, so it must be placed on the enemy's side of the field and cast directly; it is far too big for Expansive Spellstrike. Poison immunity makes it useless against many unliving enemies. A strong opening spell on the right day.""")

w('Tempest Cloak', """Protection for one ally against arrows and a ring of difficult terrain around them. It can keep a caster safer from archers and from enemies trying to close. It costs two actions and does nothing for him directly.""")

w('Vampiric Feast', """Solid damage that pays some of itself back. Through Spellstrike its touch range becomes his reach, and the temporary Hit Points he gains make it the only spell that leaves him sturdier after casting it. A basic save means half damage and half the buffer even when the target succeeds.

It works only on living creatures and aims at Fortitude, the save tough enemies pass most often. Void damage is rarely resisted by the living. A good spell for a fight in which he expects to be hit.""")

w('Wall of Thorns', """A long barrier that hurts whatever pushes through and gives cover across it. It can split an encounter in half for a minute, which is a strong effect for the rank.

It takes a whole turn, and determined enemies can hack a gap in a round or two. It suits a party that wants to fight half the enemy at a time and a caster with turns to spare, which he is not.""")

w('Wall of Water', """A barrier that slows crossing and hampers fire and ranged attacks through it. It stops very little outright. Wall of Thorns is the better wall for the same turn.""")

w('Wall of Wind', """Close to complete protection from arrows and bolts for a minute, and a real obstacle to fliers. Against an ambush by archers it protects the whole party at once.

It costs a full turn and does nothing against melee or spells. Keep it as a scroll for the fight that opens with a volley.""")

w('Warding Aggression', """A small AC bonus against one enemy that lasts only while he keeps hitting it. It replaces a Spellstrike on the turn it is cast and gives less than Shield does for one action.""")

w('Echo Jump', """With the common-sense, flavour-fitting ruling the GM prefers, Echo Jump lets Cyrus strike an enemy and be somewhere else before it can answer. He lands the blow, the spell adds a burst of force to it, and he vanishes to a spot up to 30 feet away; because it is a teleport, neither that enemy nor anything else nearby gets a reaction as he goes. That makes it the spell for a creature he does not want to stand next to, one with a long reach, a grab or a punishing reaction, and for turns when the fight needs him on the far side of the room once the blow is struck. Force is a type that almost nothing resists, so the extra damage can be relied on.

He can also cast it without attacking, simply to get out when he is surrounded, though the burst then spreads around the space he left and will catch any ally standing beside him.""", grades='ADD', ratings='400040')

w('Temporal Twin', """Lets an ally repeat one action from a spot he chooses. On a hard-hitting ally that is one extra Strike for two of his actions and a rank-3 slot, which is a poor exchange beside Haste.""")

w('Blazing Dive', """With the common-sense, flavour-fitting ruling the GM prefers, Blazing Dive answers the problem Cyrus has at the start of most fights, which is that the enemy worth hitting is rarely standing next to him. Rather than spend a turn walking, he flies up to 60 feet, comes down within reach of his target and Strikes as he lands, with the spell's heat and impact added to the blow. Because he arrives through the air, a gap, a barricade or a line of guards in the way does not stop him.

It asks for some care in return. He has to rise 15 feet before he dives, so a low ceiling rules it out, and because he is flying, not teleporting, enemies he leaves behind can still strike at him as he goes. The damage is part bludgeoning and part fire, so an enemy that resists fire takes a good deal less.""", grades='ADD', ratings='400040')

w('Oneiric Mire', """Entangling Flora's effect against Will instead of Reflex, which helps against nimble enemies. It needs a whole turn and failed saves, and difficult terrain alone is modest control for that price.""")

w('Veil of Privacy', """Protection from scrying and detection for eight hours. It matters only when the party knows it is being watched by magic, which is a rare kind of problem.""")

w('Coral Scourge', """A slow-building penalty to one enemy's AC and Reflex that needs repeated failed saves and carries incapacitation. Too unreliable; Fear gives a similar benefit at once.""")

w('Glass Sand', """A very long cone of slashing damage with a little bleed. Through Expansive Spellstrike sixty feet of cone can catch an entire group behind his target, more than Crashing Wave's thirty.

The damage is lower than Crashing Wave's, and slashing is resisted more often than bludgeoning. It is the pick for big, deep formations and open ground; Crashing Wave is better in ordinary rooms.""")

w('Magical Fetters', """A heavy penalty to one enemy's AC, Reflex and Speed for the whole fight, if it fails. A success gives a mild version for a round. Against an enemy of his level the full effect makes every attack against it far more likely to hit and to crit.

Incapacitation means it rarely lands on anything stronger than him. It is a spell for equal or weaker enemies with poor Reflex, where it can be excellent.""")

w('Radiant Globe', """A dome that destroys arrows passing through it. It protects a small area from archers for as long as he spends an action each round on it, after a whole turn to cast. Wall of Wind does more for less upkeep.""")

w('Disruptive Transfer', """A teleport as far as his Speed that dazzles whoever was next to him. With Laughing Shadow's Speed it covers good distance and it provokes nothing. Dimensional Assault already does this job with a Strike included, so the slot is hard to justify.""")

w('Percussive Impact', """Attack-roll damage that starts behind Briny Bolt and catches up only in his highest slots, since it grows every second rank. Sonic and bludgeoning are both seldom resisted. A late-game option at most; nothing sets it apart before then.""")

w('Roaring Applause', """A control spell built for someone with Reactive Strike. Even on a successful save the target loses its reactions for as long as he sustains the spell, which frees the whole party to move and cast around it. On a failure it also loses an action each round, and its own applause provokes his Reactive Strike at the start of each of its turns.

The sustain competes with recharging, so he is trading some of his own burst for a hobbled enemy and free attacks. Against one dangerous enemy from level 6 that is a good trade. Mindless creatures are immune, and the target has to be able to perceive him.""")

w('Gravity Wave', """Damage and a knockdown across a cone. Every enemy that fails is prone, off-guard for Laughing Shadow and for the party's melee, and has to spend an action standing where Reactive Strike can punish it. The cone is easy to steer through Expansive Spellstrike.

It asks for failed Fortitude saves, which big enemies often avoid, and its damage is a step below Crashing Wave's. Against groups of ordinary enemies it is one of his best spells at this rank; against one sturdy enemy Dimensional Drop is the surer way to get it on the ground.""")

w('Skyglass Prison', """Pins an enemy in place even when it saves. A target that cannot move for a round cannot reach the party's casters, cannot retreat from his reach, and must spend actions breaking out on a failure. For a reach fighter who wants an enemy held where he can hit it, that is ideal.

It does not stop the enemy attacking whoever is adjacent, and it targets Fortitude. Its best use is on a mobile enemy, an archer, or something trying to flee.""")

w('Lightning Lasso', """Damage with a hold attached, if the target fails. Keeping the hold costs a sustain each round, the action he needs for recharging, and the enemy can simply Escape. Skyglass Prison holds an enemy without upkeep and does so on a success.""")

w('Rend Magic', """An anti-caster spell. The initial force damage is a little under the usual for the rank and rides the Strike, and afterwards the target is hurt every time it casts a spell, which punishes exactly the enemy he most wants to pressure. Force is almost never resisted.

Against anything that does not cast it is plain damage and ends at once. Prepare it when enemy spellcasters are expected; otherwise Briny Bolt offers more.""")

w('Tricks and Treats', """A burst around himself that makes enemies clumsy even on a success and takes their reactions on a failure. Being surrounded is when he wants it, and removing reactions lets him and his allies move freely.

It needs failed Will saves for its better effect, does nothing to enemies carrying no valuables, and through Spellstrike it reaches only the creature he strikes. A curiosity more than a staple.""")


# ───────────────────────── rank 4 ─────────────────────────
w('Fly', """The answer to most problems of height and terrain, and the only way he fights a flying enemy with his weapon instead of a cantrip from the ground. Five minutes covers a whole encounter, and cast on a melee ally it solves the same problem for them.

Before level 13 it costs two actions he would rather spend attacking, so it is best cast before the fight when the need is visible. At 13 it becomes a studious spell with a free Arcane Cascade, which makes it a good opening action whenever the battlefield has depth. Keep a scroll until he can spare the slot.""")

w('Translocate', """A long teleport with no line to walk and nothing to provoke. It leaves a grapple, crosses a chasm, passes a portcullis or reaches a distant enemy in one cast, and in a higher slot it becomes an escape over a mile.

Dimensional Assault covers short hops within a fight more cheaply, so this is for the distances that spell cannot reach. From level 13 it is a studious spell, in his book for free and bundled with Arcane Cascade. Worth a scroll before then and an occasional slot after.""")

w('Vision of Death', """His best spell against Will. The damage is solid for the rank, and the fear applies on a successful save, so the slot is never wasted on a living enemy that can feel fear. Delivered through Spellstrike it adds a solid hit and leaves the target easier for everyone to hit and affect.

Mindless creatures and anything immune to mental or death effects ignore it completely, which rules it out on some days. Where it works it is the strongest thing he can do to an enemy with a weak Will, such as a brute. Prepare it when the day's enemies are known to be living and thinking.""", grades='ADD')

w('Containment', """A force cage for one creature, with two opposite uses. On an enemy it removes a threat from the fight for a while if it fails its save; on a fallen ally it stops them being finished off. The second use is the more dependable, since a willing target does not save.

Nothing passes the field in either direction, so a contained enemy cannot be attacked either, and an enemy that saves is merely delayed. A situational spell that suits a scroll.""")

w('Force Rain', """Three castings in one slot, all in a damage type almost nothing resists. The two-action burst is a strong choice for Expansive Spellstrike, in a compact area. The one-action version is the standout: single-square force damage on a basic save, which he can add after a Spellstrike on the same turn with no attack penalty. The three-action version deals fixed damage with no save at all.

It has no rider, and Reflex is the save his list already leans on. Its flexibility and damage type make it one of the best general-purpose slots at this rank.""")

w('Life-Draining Roots', """A short line of piercing damage that gives him temporary Hit Points for each living creature hit. The line is too short to catch many, so the buffer is usually small, and Lightning Bolt does more damage in a far longer line.""")

w('Grasping Earth', """Area control that holds enemies in place and leaves them off-guard, which suits Laughing Shadow and a party of melee strikers. A grabbed enemy cannot follow the party's casters or leave his reach.

Its damage and its staying power both come from sustaining, which costs him his recharge, and it needs failed Fortitude saves from the kind of enemy that seldom fails them. Skyglass Prison pins one enemy more reliably; this is for holding a cluster.""")

w('Confusion', """An action lost even on a success, and on a failure an enemy that may turn on its own side. Against a group of dangerous enemies the failure result can swing a fight, and through Spellstrike the stun on a success comes on top of a Strike.

It is single-target at this rank and needs a failed save for the big effect; a confused enemy may also simply attack him. Mindless creatures are immune. Paralyze does more to one equal enemy, so this is the choice when the enemy outnumbers the party.""")

w('Unfettered Movement', """Protection from grapples, webs, and anything else that would slow or hold one creature, for ten minutes. Against an enemy that grabs or restrains it is close to a complete answer. Cast it from a scroll before such a fight.""")

w('Clairvoyance', """Seeing a place before entering it. A minute of casting buys a look at the room beyond the door, which is worth a great deal to a party that plans. It has no use once a fight has started, so it belongs on a scroll.""")

w('Wall of Mirrors', """A solid wall for two actions, which is rare at any rank. It blocks movement, arrows and line of effect, so it can cut a fight in half, seal a corridor against reinforcements, or shelter the party from a volley, and it lasts a minute unless dismissed. Enemies that attack it suffer for doing so.

Most walls cost a whole turn; this leaves him an action to Stride or raise Shield. It deals no damage of its own, and a wall in the wrong place hinders his allies as much as the enemy. With that granted, it is one of the strongest control spells he can prepare.""")

w('Zephyr Slip', """A reaction that carries him away from an enemy that has just closed with him. He wants enemies inside his reach, and he wants his reaction for Reactive Strike. It solves a problem he does not have.""")

w('Rebounding Barrier', """A reaction that cuts one physical hit against him and returns a little damage. The reduction is decent, but it competes with Reactive Strike and Wooden Double guards against the hits that actually threaten his life.""")

w('Bestial Curse', """A curse that hampers humanoids only, and only if they fail a Fortitude save. Narrow in target and weak in effect; nothing recommends it over Fear or Slow.""")

w('Chromatic Ray', """A very hard-hitting attack spell with a random element. The damage is among the highest he can put on a Strike's roll at this rank, and doubled on a critical hit it can end a fight. Three of the four colours simply deal heavy energy damage; the fourth trades it for a debuff.

He cannot choose the damage type, so a resistant or immune enemy may blunt it, and it does not grow smoothly with rank. For raw damage on an attack roll it is hard to beat when the target has no known resistances.""")

w('Countless Eyes', """Stops one creature from being flanked. It helps an ally who is being surrounded and costs two actions for a narrow benefit. Seldom the best use of a turn.""")

w('Creation', """A temporary object made to order: a ladder, a plank, a wedge, a simple tool. Useful for solving physical problems with a minute to spare. A scroll or wand covers the occasional need.""")

w('Dispelling Globe', """A stationary bubble that tries to counter spells aimed into it. Against a fight he knows will be full of enemy magic it can protect him and whoever stands with him. It holds him to one spot, which suits a reach fighter poorly, and it counters only weaker spells.""")

w('Draw the Lightning', """Damage on a target above him, followed by a minute of extra electricity on his first Strike each round. The lasting bonus is the attraction, since it adds to every Spellstrike for the rest of the fight at no further cost.

The target must be taller than him or higher up, which rules it out against many enemies, and the bonus is modest per hit. It pays over a long fight against a large creature and not otherwise.""")

w('Dull Ambition', """A curse that worsens one enemy's initiative and, on a failure, its other checks for a long time. Its strongest part comes too late to matter in a fight that has already started. An oddity for intrigue more than combat.""")

w('Fire Shield', """A sturdier magical shield than the cantrip, which needs no hand and burns enemies that strike him in melee. Against a fight with many small hits the block absorbs a good deal over a minute.

Raising it costs an action each round and blocking costs his reaction, the same two things he is always short of. It suits a turn pattern with a spare third action and no Reactive Strike to keep ready.""")

w('Flicker', """Resistance to nearly all damage for a minute, with a random teleport at the end of every turn. The resistance is useful. The teleports keep moving him out of the position he chose, and for a fighter who depends on reach and flanking that is a serious cost.""")

w('Grasp of the Deep', """Moderate damage against Will with a grab on a failure. A grabbed enemy cannot move away from his reach and is off-guard, which switches on Laughing Shadow's damage for every later Strike, and breaking free costs the enemy an action against his spell DC.

A success still halves the damage, so the slot is never wasted, but the grab needs a failure. Mental effects do not work on mindless creatures. It is a good second Will spell behind Vision of Death, better against an enemy he wants pinned.""")

w('Ice Storm', """A whole turn to cast, a sustain to keep, and modest damage with difficult terrain. Full casters make it work from the back line. For him it costs two turns of Spellstrike for less damage than one of them.""")

w('Invisibility Curtain', """A wall that hides everyone on one side from the other. It can screen an approach or a retreat, at the price of a turn and a sustain each round. Shared Invisibility is the simpler tool for moving unseen.""")

w('Liminal Doorway', """A hidden room that lasts eight hours. It is a safe place to rest in hostile territory, or to hide people and goods. Ten minutes to cast, never urgent, and well suited to a scroll or wand.""")

w('Mercurial Stride', """A double Stride that passes through one enemy and poisons it. Getting past a blocker has some value, but Dimensional Assault and Time Jump do it better and the poison is minor.""")

w("Mirror's Misfortune", """An illusory double that makes attackers who strike it roll worse afterwards. It protects less reliably than Mirror Image or Blur, and those are available two ranks lower.""")

w('Morass of Ages', """An aura that can slow every enemy near him, growing as he sustains it. A front-line fighter surrounded by enemies is where such an aura belongs, and taking an action from each of them is powerful.

Each creature saves once, against Fortitude, and those that succeed are unaffected for the rest of the spell. Sustaining it costs the action he needs to recharge. Strong on paper, and too dependent on failed saves to rely on.""")

w('Mountain Resilience', """Steady resistance to physical damage, which is what most enemies deal. Twenty minutes is long enough to cast before a fight, and on a front-line ally or on himself it takes a bite out of every weapon hit. The stronger versions in higher slots are worth far more.

Each hit shortens it, so against a swarm of attacks it runs out quickly, and it does nothing against energy or spells. A good scroll or wand for the fight he can see coming; in a slot it competes with spells that end fights sooner.""")

w('Nightmare', """Harasses a known enemy from a distance by spoiling its sleep. It is a plot tool with no place in an adventuring day's slots.""")

w("Outcast's Curse", """Makes one creature worse at social checks and disliked by others. It could undermine a rival in an intrigue. It needs a touch and a failed save, and has no use in a fight.""")

w('Peaceful Bubble', """Hides a camp from scrying and magical detection for a day. It matters only when the party is being hunted by magic. A scroll if so.""")

w('Rust Cloud', """Heavy damage every round for a minute with no sustain, across a large area. Left on a group that cannot easily leave, such as enemies holding a room, it does more total damage than almost anything else at this rank, and the concealment hampers their archers.

It costs a full turn and harms allies who enter, so it must be placed where the party will not fight, and enemies who can walk out will. It is a strong opening spell for an assault on a fixed position, and wasted in a mobile skirmish.""")

w('Seal Fate', """Gives a living enemy a weakness to a damage type he chooses, briefly on a success and for a minute on a failure. Paired with a spell of the matching type and a party that deals the same type it adds up. The setup costs him a Spellstrike turn, and the short version barely repays it.""")

w('Shape Stone', """Reshapes a block of stone: a hole in a wall, a sealed doorway, a step, a barricade. A good problem-solver in stone buildings and caves, and a scroll covers it.""")

w('Solid Fog', """A fog bank that blocks sight and slows movement for everyone in it. It costs a full turn and hinders the party as much as the enemy. Useful for covering a retreat and little else.""")

w('Spell Immunity', """Protection against one named spell for a day. When the party knows what an enemy caster will throw, it can neutralise that enemy's best trick. Without that knowledge it is a guess. A scroll for the well-scouted fight.""")

w('Suggestion', """A persuasive nudge that can send a guard away, stall a pursuer or end a standoff without a fight. In the hands of the party's negotiator it has clear uses, and a suggestion that seems reasonable may never be recognised as magic.

It has incapacitation and needs a failed save, so it works on minor figures more than on anyone important, and a target that resists strongly knows what he tried. Carry it as a scroll and use it where failure would not be a disaster.""")

w('Telepathy', """Silent two-way conversation with creatures nearby. It can replace a shared language in a pinch. Message and Translate cover most of the same needs more cheaply.""")

w('Vampiric Maiden', """Damage and a small buffer of temporary Hit Points against a Fortitude save, with a hold on a failure. Vampiric Feast from rank 3 does more damage and returns more to him through his reach.""")

w('Vapor Form', """Turns a creature into a drifting cloud that fits through cracks and under doors. It is an infiltration and escape tool; in a fight the target can do almost nothing. Scroll.""")

w('Wall of Fire', """A burning line or ring that damages whatever crosses and blocks sight. A ring around a group forces a choice between staying put and burning, and a line across a corridor taxes every reinforcement.

It takes a whole turn, fire is commonly resisted, and enemies with ranged attacks may simply stay behind it. It suits a caster who can afford the turn. Wall of Mirrors does the blocking for two actions.""")

w('Weapon Storm', """Area damage based on his weapon's damage die, in a cone or around himself. The damage falls short of dedicated area spells of the same rank, and it grows slowly. Crashing Wave and Force Rain are better choices.""")

w('Winning Streak', """A one-action burst of speed for an ally or himself that continues while the party keeps landing critical hits. On the right turn it gives a striker an extra attack for a single action, which is cheap.

Its length depends on luck, and a rank-4 slot is a high price for what is usually one round. Haste does the same job for a whole fight from rank 3. Consider it only for a party that crits often.""")

w('Replicate', """An illusory copy of a willing person that can walk and say a few words. It can cover an absence or serve as a decoy in an intrigue. A full turn to cast, a sustain to keep, and no use in a fight.""")

w('Discern Lies', """A large bonus to notice a lie for ten minutes. For the character who conducts the party's negotiations and interrogations that is exactly the right tool at the right moment, and it involves no save for the other side to pass.

It tells him that something is false, not what the truth is. The need is predictable, since he knows when an important conversation is coming, so a scroll serves well.""")

w('Planar Tether', """Stops a creature from teleporting or leaving the plane. Against an enemy whose habit is to vanish when losing, it can decide whether the party finishes the job. A narrow answer worth a scroll when such an enemy is known.""")

w('Sanguine Mist', """A cloud of void damage that grows stronger and feeds him temporary Hit Points while he sustains it. The first burst is decent. The rest needs the action he uses to recharge, and it harms living allies too.""")

w("Mantis's Grasp", """Solid force damage with a hold on a failure, from long range. Force is almost never resisted, and an immobilised enemy cannot leave his reach or reach the party's casters. Through Spellstrike it competes with the best at this rank, and it is equally good cast directly.

The hold needs a failed Reflex save and lasts a round unless the failure is critical. It is a stronger single-target option than Force Rain against an enemy he wants pinned.""")

w('Entangle Fate', """Makes several enemies off-guard even when they save. Off-guard lowers their AC against the whole party and switches on Laughing Shadow's extra damage without any need to flank, and for up to four enemies at once that is a large benefit from one cast.

It deals no damage and the stronger effects need several failures. Cast as a fight begins against a group, it raises the party's damage for the rounds that follow more than a damage spell would.""")

w("Infiltrator's Tunnel", """A door through a wall. Two linked portals let him step into a sealed room, past a locked gate or out of a cell, and in a higher slot the party can follow. For planned infiltration it removes obstacles that would otherwise take skill checks or noise.

It has no combat role beyond an escape route. A scroll for the job that needs it.""")

w('Freezing Touch', """A spell that can root an enemy for the fight. On a failure the target is stuck until it breaks free, taking persistent cold all the while, and trying to escape costs it actions. Through Spellstrike the touch becomes his reach, and even a success leaves some damage ticking.

It targets Fortitude, so the hold is least likely on the big enemies he would most like to stop, and the damage arrives slowly. Use it on mobile or fragile enemies; Skyglass Prison holds for a round even on a save.""")

w('Friends to Foes', """Damage and fear against Will, with a twist that suits group fights: the fear does not fade while the target stands near its allies. In a tight formation that keeps an enemy weakened for much longer than ordinary fear would, and it applies even on a successful save.

Against a lone enemy the twist does nothing and Vision of Death hits harder. Mindless creatures are immune. Choose it for fights against several intelligent enemies who stay together.""")

w('Lost Things Returned', """Takes an action from an enemy even on a successful save, like Slow, but against Will instead of Fortitude. That makes it the answer to big enemies with strong bodies and weaker minds, which Slow struggles against. On a failure it lasts the fight.

An ally can end it early for a burst of damage, which gives the party a choice. Mindless creatures are immune. Worth learning as the Will-save counterpart to Slow.""")

w('Gift of Dusk', """A debuff that weakens an enemy's attacks for a full minute even when it saves. Against a hard-hitting brute a minute of reduced damage is a real defensive gain for the front line, and a failure makes it worse.

It adds no damage and has no effect on creatures without a shadow. Enfeeble gives a shorter version from rank 1. A fair pick against one powerful melee enemy when the party needs to survive it.""")

w('Unending Tears', """Dazzles one enemy until it spends an action clearing its eyes, even on a success. An action lost or a chance to miss is a modest return for a rank-4 slot, and Ignite Fireworks dazzles a whole group from rank 2.""")


# ───────────────────────── rank 5 ─────────────────────────
w('Weight of the World', """The best single-target spell at this rank, and the reason is the successful save. An enemy that passes still loses an action and spends a round dazzled; one that fails loses two actions and stays dazzled for the fight. Against a single powerful enemy, where each of its actions is worth more than anything else on the field, that is the most valuable thing he can attach to a Strike.

It aims at Fortitude, so failures will be rare against big enemies, but the spell is built to be worth casting on a success. The damage is a secondary benefit. Prepare it in a top slot from level 9 on any day with a serious single enemy, and cast it directly from range if the Strike cannot reach.""")

w('Wall of Stone', """The strongest battlefield control he can cast at this rank. A hundred and twenty feet of shaped stone can cut an encounter in half, close a corridor behind the party, wall off reinforcements, or become a bridge or a stair. There is no save; the enemy must break it or go round, and either costs rounds.

It takes his whole turn, so it is a first-round spell, cast while the enemy is still closing, and a misplaced wall hinders the party as much as the enemy. On a day with a large or awkward fight in prospect, one slot spent here can be worth more than any attack spell.""")

w('Glacial Skewer', """An attack spell with a positional trick. The damage is solid for the rank and rides the Strike's roll, doubling on a critical hit, and cold and piercing together are seldom both resisted. If the push drives the target into a wall, pillar or other large obstacle, it is pinned there.

The push otherwise moves the enemy out of his reach, which he does not always want, so it rewards choosing his angle before the Strike. Indoors, with a wall behind the target, the pin makes it the best attack spell at this rank; in open ground Blood Feast hits harder and a heightened Briny Bolt serves as well.""")

w('Blazing Fissure', """The line spell to build turns around from level 9. Its damage matches the best at the rank, split between fire and bludgeoning so that resistance rarely stops all of it, and every enemy that fails is knocked prone: off-guard for Laughing Shadow and the party's melee, and an action down to stand where Reactive Strike waits.

Through Expansive Spellstrike the line runs away from his allies, and with Sprinting Spellstrike at 12 it carries him the length of the field through a row of fallen enemies. It affects only creatures on the ground. Lightning Bolt hits a little harder in a higher slot; this does more to the fight.""")

w('Tornadic Gale', """A line that gathers its own targets. It pulls smaller enemies from either side into the line before damaging them, which turns a loose group into a full row of victims, and it lifts and drops those that fail. With Sprinting Spellstrike it sweeps up enemies as he passes.

It does not pull Large creatures, and the damage has no second type to fall back on. Blazing Fissure is the steadier choice against big enemies in a file; this is better against a scattered crowd of ordinary ones.""")

w('Howling Blizzard', """A wide, long cone of heavy cold damage that leaves difficult terrain for a round. Through Expansive Spellstrike sixty feet of cone covers most of a battlefield beyond his target, and the terrain slows whatever survives.

It is plain damage with a brief hindrance, and cold is sometimes resisted. The three-action version is an ordinary long-range blast that he will seldom have a reason to cast. Against a group it is solid; Blazing Fissure and Elemental Breath usually offer more.""")

w('Impaling Spike', """Moderate damage with a pin on a failure, in cold iron, which adds extra harm against creatures weak to it. An impaled enemy stays where it is until it tears free, which holds it inside his reach.

The pin needs a failed Reflex save, so it is least likely against the agile enemies he most wants to hold, and the range is short. A good spell against fey and fiends with that weakness, and average otherwise.""")

w('Shadow Siphon', """A reaction that weakens an enemy's damaging spell for the whole party. When it succeeds it can halve a blast that would have hurt everyone. It depends on a counteract check and holds a rank-5 slot in reserve for a moment that may not come.""")

w('Corrosive Muck', """Two pools that slow and burn whatever crosses them, for a minute, with no sustain. Placed across the approaches to the party they punish every enemy that advances, and the damage each round is substantial.

It works as a direct cast before lines are joined and not through Spellstrike, because Expansive Spellstrike places one burst. Enemies with ranged attacks can ignore it. Good for defending a position.""")

w('Banishment', """Removes a creature that does not belong on this plane, outright, on a failed save. Against summoned and extraplanar enemies it can end a fight in one cast. It does nothing to natives and carries incapacitation, so it belongs on a scroll for the day such enemies appear.""")

w('Space Fold Gate', """A gate between two points that the whole party can use for a minute. It crosses chasms and reaches objectives, at the price of a full turn and a sustain. An exploration tool that a scroll can hold.""")

w('Magic Passage', """A tunnel through ten feet of wall for an hour. It bypasses doors, guards and traps altogether, and for a party that plans its way in that is extremely useful. Scroll.""")

w('Scouting Eye', """A mobile, invisible eye for scouting ahead. It sees what he would see and goes where he would not want to. It needs a minute to cast and a sustain to move, which is no hardship outside a fight. Scroll.""")

w('Sending', """A short message to anyone he knows well, anywhere on the same world, with a reply. For keeping in touch with allies and patrons far away it has no substitute, and a scroll or wand covers it.""")

w('Drop Dead', """A reaction that fakes an ally's death and hides them when they are hit. Against enemies that stop attacking the fallen, it pulls a badly hurt ally out of danger for the price of one reaction.

The trick fails if the apparent death is implausible, needs sustaining, and ends when the ally acts. It also competes with Reactive Strike. A clever emergency measure for a spare slot, not something to plan a day around.""")

w('Acid Storm', """Acid rain over a wide area for a minute with no sustain. The damage each round is low for the slot, and enemies can walk out of it. Rust Cloud does the same job far harder from rank 4.""")

w('Blink Charge', """Dimensional Assault from a spell slot. He appears beside an enemy up to 60 feet away and Strikes with extra force damage, provoking nothing on the way. On a day when his Focus Points are spent, or the gap is too wide for the focus spell, it gets him into the fight with a hit.

It is not a Spellstrike, so the Strike carries only the small bonus damage, and a rank-5 slot is expensive for that. Worth a scroll; rarely worth the slot.""")

w('Blister', """A spell that stores damage for later turns. Each blister can be burst for a single action, releasing a cone of acid from the target, so on following rounds he can Spellstrike and still set off what amounts to a second damage spell with his third action.

The number of blisters depends on the Fortitude save, and a success yields only one. The cones spread from the target, so allies near it are at risk. Against a durable enemy that fails, the total damage is excellent; against a successful save it is thin.""")

w('Cloak of Colors', """A defensive buff that fights back. Enemies beside the target are dazzled without a save, and those that hit it in melee risk being blinded. On a front-line ally it reduces incoming hits for a minute.

The blinding effect has incapacitation and needs a failed save, so against strong enemies only the dazzle is dependable. Two actions in the first round is the cost. A reasonable opening buff when he is not yet in reach.""")

w('Elemental Breath', """A long cone of very high damage with a rider, in a random element. Through Expansive Spellstrike sixty feet of cone covers the field beyond his target, and each element adds something useful to the damage.

With two actions he cannot choose the element, so he risks rolling one the enemy resists, and the three-action version that lets him choose cannot go through Spellstrike. It is the hardest-hitting cone he has at this rank when resistances are not a concern.""")

w('Flowing Strike', """A long move that provokes nothing, with a Strike along the way. It takes his whole turn and delivers less than a Stride and a Spellstrike would. Sprinting Spellstrike does the same thing properly from level 12.""")

w('Forceful Hand', """A floating hand that shields him or an ally while he sustains it. The protection is modest and the sustain is the action he needs for recharging. Not a magus's spell.""")

w('Freezing Rain', """Difficult terrain now and damage later, after a full turn and with a sustain. Too slow for a class whose turns are worth so much.""")

w('Geyser', """Damage, a throw into the air and a fall that leaves enemies prone, at very long range. Prone enemies are off-guard for Laughing Shadow, and the range makes it a good opening cast before melee is joined.

Its area is a cylinder, which Expansive Spellstrike does not cover, so it is a direct cast only. Blazing Fissure knocks prone along a line he can deliver with a Strike. Take it for the long-range opener if a slot is free.""")

w('Glimmer of Charm', """An aura that softens the attitude of people near him. It could ease a tense negotiation, but it needs sustaining, has incapacitation, and using magic on the people he is negotiating with carries its own risks.""")

w('Grisly Growths', """Solid single-target damage against Fortitude, with a basic save so that half still lands on a success, and it works on almost any creature with a body, living or not, which Vampiric Feast does not. The sight of it also sickens creatures within 30 feet that fail a Will save, the target included, which is a useful penalty across a group of enemies.

That second effect does not spare allies, so it suits a target standing among its own side, and mindless creatures ignore it. Weight of the World does far more against one strong enemy; this is the choice when the aim is to finish something whose Fortitude is not its best save.""")

w('Hallucination', """Changes what one creature perceives for an hour: a person it cannot see, a door that looks like a wall, a stranger who looks like a friend. For intrigue and infiltration it is a subtle, powerful tool, and it draws little attention when cast.

It has incapacitation and depends on a failed save, and the target gets chances to see through it. It has no use in a fight. A scroll or wand for the scheme that calls for it.""")

w('Illusory Scene', """A full illusory scene with moving figures, sound and smell, lasting an hour. It can fake a camp, a patrol or a gathering to mislead pursuers or draw guards away. Ten minutes to cast, so it is a planning tool for a scroll.""")

w('Imaginary Lockbox', """Hides a container in his mind until his next preparations. Useful for smuggling something past a search. Very narrow.""")

w('Invoke Spirits', """Low damage in a small burst that must be sustained and moved, with fear only on a critical failure. It asks for his recharge action every round and returns very little for a rank-5 slot.""")

w("Mariner's Curse", """A penalty that does not wear off. On a failure the target stays sickened for the rest of the fight, however often it retches, which outlasts fear and lowers its attacks, saves and AC throughout. Even a success sickens it until it spends an action.

It needs a touch, which Spellstrike supplies at reach, and a failed Will save for the lasting version. Against a long fight with one durable enemy it gives more over time than Fear; in a short fight Fear costs four ranks less.""")

w('Mind Probe', """Questioning a creature's memories directly. For an investigation it can produce answers no ordinary interrogation would, and he is the party member who asks the questions.

It takes a minute to cast, needs a failed Will save, and each answer can still be resisted. It is an out-of-combat tool for a scroll, used on a captive or a cooperative witness.""")

w('Mirror Malefactors', """The one sustained spell that pays a magus back. The first cast is heavy mental damage with fear that cannot be shaken off while the mirrors last, and each sustain repeats the damage. That makes his third action as strong as a damage spell on every following round, alongside a Strike.

Sustaining does compete with recharging Spellstrike, so he alternates between them or gives up the recharge while the mirrors run. It works on Large or smaller creatures with minds. Against one tough enemy of that size it is among the highest total damage he can produce from a single slot.""")

w('Pressure Zone', """A wide area that makes living enemies clumsy, which lowers their AC and Reflex for every attacker and for his Trip. The effect on a failure lasts and compounds.

It takes his whole turn and aims at Fortitude, and those that succeed are affected only briefly and then immune. Worth it at very long range before a fight against a group; otherwise it costs too much of his own offence.""")

w('Quicken Time', """Speeds up everyone in an area, enemies included. Unless the party can occupy the zone alone it helps both sides, which limits it to the opening round around his own group. Haste on one ally is more dependable.""")

w('Rewinding Step', """A prepared return to a marked spot within ten minutes. It is a planned escape route for a heist or a risky scouting trip, and has no ordinary combat use.""")

w('Slither', """Area control that grabs and holds without sustaining. Enemies caught are off-guard and stuck, and they must save again each round they remain, so over a minute it ties down a group thoroughly. That suits Laughing Shadow and the party's melee very well.

It costs a full turn and harms allies who enter the area. Cast in the first round on the enemy's side of the field, it is one of the better control spells at this rank for a class that can only afford one such turn per fight.""")

w('Stagnate Time', """An area that can take an action from every enemy inside it each round, for a minute, with no sustain. Over a fight that is an enormous number of lost enemy actions if they fail their saves and stay put.

Nothing happens on a successful Will save, it affects allies who enter, and enemies can leave. For two actions it is still one of the strongest area effects he can cast when the enemy must hold ground. Use it against groups defending a spot.""")

w('Subconscious Suggestion', """A suggestion that waits for a trigger. It suits a long game: a steward who will leave a door unlocked, a guard who will look away at a signal. With incapacitation it works on minor figures. A scroll for intrigue.""")

w('Summon Dragon', """A full turn to cast and an action each round to keep, for a creature well below the level of anything he is fighting. As with every summon, it costs him the actions his own turn runs on.""")

w('Telekinetic Haul', """Moves a very heavy object at range. It lifts a portcullis, shifts a boulder or drops something large. Occasional engineering, covered by a scroll.""")

w('Toxic Cloud', """A drifting cloud of heavy poison damage each round for a minute. Against breathing enemies that cannot escape its path the total is high. It takes a full turn, moves where it will, harms allies, and poison immunity is common among the unliving.""")

w('Truespeech', """Removes every language barrier for an hour, and in a higher slot for a working day. For the party's negotiator it turns encounters that would have been fights or stalemates into conversations.

It is needed on particular days and not in the middle of a fight, so a wand or scroll is the right home. On a journey among strangers it is one of the most valuable utility spells he can carry.""")

w('Umbral Journey', """Fast overland travel for the whole party. It shortens long journeys dramatically and has no other use. A scroll when distance is the problem.""")

w('Wall of Ice', """An opaque wall or dome that blocks sight and movement and chills those who break through. A dome can trap a small group or shelter the party for a round or two.

It costs a full turn and can be shattered. Wall of Stone at the same rank is larger, stronger and more flexible; this is the alternative when blocking sight matters most.""")

w('Wave of Despair', """A cone that strips reactions from every enemy in it, even those that save, and can go on to take actions from those that fail. Removing reactions from a whole group for a round lets the party move, cast and retreat without punishment, and through Expansive Spellstrike the cone is easy to aim.

The lasting effects depend on failed Will saves, and mindless creatures are immune. It deals no damage. Against several enemies with dangerous reactions it is a very strong opening.""")

w('Etheric Shards', """Difficult terrain that also hinders fliers and incorporeal creatures, with light damage for moving through it. It slows an advance. For a rank-5 slot that is a small effect.""")

w('Telepathic Bond', """Silent communication among the whole party at any distance for eight hours. For a split party or an infiltration it is ideal. A scroll covers the day it is wanted.""")

w("King's Castle", """Swaps his position with a willing ally. It can pull a threatened caster out of melee by putting him there instead, which is a fair trade for a front-line fighter. A narrow rescue for a rank-5 slot.""")

w('Control Water', """Raises or lowers water over a wide area. It matters in flooded ruins and at sea, and nowhere else.""")

w('Blinding Bottle', """A very large burst that can blind a whole group for several rounds. Blinded enemies are nearly helpless, so when it lands the fight is effectively decided.

It has incapacitation, aims at Fortitude and is a poison, so strong enemies, tough enemies and the unliving all shrug it off, and a 30-foot burst cannot be used anywhere near the party. It is a direct cast at long range against a crowd of weaker living enemies.""")

w('Blinding Foam', """An attack spell that blinds on a hit, with no save. Through Spellstrike a successful Strike leaves the target blind until it spends three actions clearing its eyes, taking acid all the while. Against an enemy of his level that is close to a won fight.

It has incapacitation, so a higher-level enemy treats his hit as a step worse and usually avoids the blindness. Against equals it is outstanding; against a single powerful enemy Briny Bolt's brief blind is more reliable.""")

w('Blood Feast', """The hardest-hitting attack spell at this rank, with a buffer of temporary Hit Points equal to half of what it deals. It rides the Strike's roll and its touch range becomes his reach, so a hit both removes a large part of an enemy and makes him harder to kill in return.

It has no control effect. It gains dice with every rank, so in a rank-6 slot it still deals more on a hit than Disintegrate does after its Fortitude save. When the aim is damage on an attack roll, and he expects to be hit back, nothing at rank 5 does it better.""")

w('Boomerang Shot', """Heavy attack-roll damage that ignores concealment and most cover. As a direct cast that makes it the answer to an archer behind a wall or an enemy in fog. Through Spellstrike those advantages seldom apply, and its damage is roughly level with a heightened Briny Bolt, without the blind.""")

w('Plasma Whirl', """A cone in three sizes with two damage types, so resistance to one rarely stops it. The one-action cone fits after a Spellstrike on the same turn, the two-action cone works through Expansive Spellstrike, and the three-action version adds a sickening effect he can only get by casting it directly.

Its damage at each size is a little behind the best single-purpose spells. What it offers is choice from one prepared slot, which is worth having when the day is unknown.""")

w('Crucible of Iron', """A debuff that works on a successful save: the target is dazzled and burning. On a failure it is also weakened for the fight until it breaks free. It suits a Spellstrike against an enemy he expects to save.

The effects are individually mild, and Weight of the World does far more to a single enemy from the same slot. A second choice for when Fortitude is the target's strongest save.""")

w('Scouring Pulse', """Very strong against undead and nothing at all against the living. In the right fight it is heavy damage over a column, with lingering damage and a glow that strips concealment and invisibility from what it hits.

Its cylinder cannot be used with Expansive Spellstrike, so it is a direct cast. Prepare it only when undead are certain; otherwise the slot does nothing.""")


# ───────────────────────── rank 6 ─────────────────────────
w('Disintegrate', """The largest single hit he can attach to a Strike at this rank, with a catch. It needs the attack to land and then gives the target a basic Fortitude save as well, so a strong enemy that is hit will often halve it. Only a critical hit, which worsens that save, produces the famous numbers.

That makes it a Sure Strike spell: with the roll taken twice and the target off-guard, the chance of the critical hit is high enough to justify the slot. Without that setup Chain Lightning is as good on average and less swingy. It also destroys walls of force and objects outright, which is occasionally the whole point.""")

w('Chain Lightning', """The most dependable heavy damage at this rank. Through Spellstrike only the creature he strikes is affected, but that is still a very large hit on a basic save that applies even when the Strike misses. Cast directly instead, it arcs through every enemy on the field at great range with no risk to allies, which no other area spell can claim.

That gives one prepared slot two excellent uses: a single-target hit through Spellstrike, or the safest area spell in the game on a turn he cannot reach melee. It has no rider and electricity is sometimes resisted. Keep one prepared from level 11.""")

w('Living Thunderbolt', """It does more for the way he fights than any other spell at this rank. For a minute he flies fast, slips grapples, and damages every enemy he moves through, so each Stride on the way to a Spellstrike becomes an area attack that costs him nothing extra. Flying at that speed also puts every enemy on the field within reach of a full turn.

It takes two actions at the start of a fight and occupies one of his two top slots, and the damage is electricity throughout. Against a group, the total over a minute dwarfs any single spell. Prepare it for any large fight from level 11.""")

w('Wall of Force', """The strongest barrier available: invisible, nearly unbreakable for a minute, and proof against everything physical. It splits an encounter cleanly, shuts a pursuer out, or buys the party a round to recover, and enemies cannot see through the plan because they can still see through the wall.

It costs a full turn, and allies cannot attack through it either. Wall of Stone covers more ground and lasts; this is harder to get past. A scroll kept for the fight that must be divided is good value.""")

w('Silver Spear', """Strong attack-roll damage that becomes exceptional against fiends, where it deals a second full set of spirit damage and can stop them teleporting away. Being silver, it also strikes that weakness in creatures that have it.

Against ordinary enemies it is solid but unremarkable for the slot, with no rider. Prepare it when fiends or silver-weak enemies are expected, and it is the best spell he has; otherwise Chain Lightning serves better.""")

w('Petrify', """A slow on a successful save, with the chance of removing the enemy entirely if it fails and keeps failing. The success effect is what he can count on; it costs any enemy an action.

The later saves have incapacitation, so a strong enemy is unlikely to turn to stone, and Slow gives the same guaranteed effect from rank 3. It suits a fight against several equals, where one of them might well be removed for good.""")

w('Cast into Time', """A short cone of mental and bludgeoning damage against Fortitude that sickens what fails. Its damage is below the better spells at this rank, the cone seldom holds more than two enemies, and the creatures it removes are back before they would have acted. Vitrifying Blast and Vampiric Exsanguination are stronger cones.""")

w('Unexpected Transposition', """A reaction that puts someone else in the path of an attack aimed at him. Swapping with an enemy makes its ally strike it; swapping with a sturdy friend spares him a hit he could not afford.

An unwilling target gets a Will save, and the reaction competes with Reactive Strike. It can produce a spectacular turn, and it can also do nothing. A spare slot's worth of opportunism.""")

w('Collective Transposition', """Rearranges the battlefield: two creatures moved anywhere within thirty feet of him. Allies go willingly, so it can set a flank, rescue a caster or bring a striker into reach in one cast, and enemies that fail are moved where the party wants them.

Enemies get a Will save and it deals no damage. Through Spellstrike it moves only the creature he strikes, so the two-creature use is a cast on its own. Useful in a party that fights by position; often a luxury.""")

w('Truesight', """Sees through illusions, disguises and shape-changes for ten minutes. On the day the enemy relies on such tricks it is decisive, and otherwise it does nothing. A scroll.""")

w('Mislead', """Invisibility that survives attacking, plus a decoy that acts in his place. Enemies are off-guard to him throughout, which keeps Laughing Shadow's damage running, and their attacks go to the double as long as they are fooled.

It must be sustained, which costs the recharge action, and Dimensional Disappearance already gives him invisibility from level 10. Clever, and largely redundant by the time he can cast it.""")

w('Teleport', """Long-distance travel for the party. It ends journeys and enables retreats to safety between adventures. Ten minutes to cast, so it is a scroll or wand matter, never a combat slot.""")

w('Arrow Salvo', """Very heavy piercing damage over a large burst at range. As a direct cast before melee it is one of the best area spells of the rank, and it avoids the energy resistances that blunt fire and cold.

The burst is far too large for Expansive Spellstrike. Chain Lightning does similar work without endangering allies. Take it only if he wants a pure long-range blast.""")

w('Chromatic Image', """Mirror Image with teeth: each image destroyed hurts or hinders the attacker. Against an enemy with many attacks it both prevents damage and returns some.

It is two actions that protect only him, and Blur with a free Arcane Cascade does the defensive job more cheaply from level 7. A rank-6 slot is a great deal to pay for it.""")

w('Cursed Metamorphosis', """Turns an enemy into a harmless animal for a minute on a failure, which removes it from the fight. A success still sickens it.

It has incapacitation and aims at Fortitude, so it is for enemies of his level or below, and against those it competes with simply killing them. Good against one of several strong equals; useless against a single superior enemy.""")

w('Dominate', """Control of an enemy on a failed save, turning it on its allies. Even a success costs it an action. When it works on something dangerous the fight swings completely.

Incapacitation restricts it to enemies of his level or lower, the target saves again every round, and mindless creatures are immune. A gamble, and an expensive one for a caster with two slots at the rank.""")

w('Field of Razors', """Damaging difficult terrain over a wide area. It taxes movement for a minute but costs a whole turn, and Rust Cloud hurts more from rank 4.""")

w('Flame Vortex', """A column of fire that must be sustained and steered, usable only outdoors or under a high ceiling. Low damage for the rank and a sustain he cannot spare.""")

w('Frost Pillar', """Encases one enemy in ice on a failed save, leaving it restrained and off-guard. It needs sustaining, the ice can be broken, and a success merely shifts the target a step. Skyglass Prison holds an enemy more reliably from rank 3.""")

w('Lignify', """Slow with a higher ceiling. A successful save still costs the target an action for a round, so it is never wasted on a powerful enemy, and a failure keeps it slowed with a chance of ending it altogether. It reaches 120 feet as a direct cast.

The follow-up saves have incapacitation, so the petrifying end is for equals. Through Spellstrike it competes with Slow three ranks lower, which gives the same floor for far less. Use this when the top slot has nothing better to do against a creature of flesh.""")

w('Necrotize', """Void damage with a lingering debuff, against Fortitude. The damage is solid for the rank, and the random debilitation always adds something: a weakness, a penalty, or a hindrance to movement.

It works only on the living, and he cannot choose which debilitation appears. Chain Lightning hits harder against Reflex, so choose this for the debilitation or when Fortitude is the weaker save.""")

w('Never Mind', """Crippling to a spellcaster if it fails, and close to nothing if it succeeds. With incapacitation as well, it is too unreliable against the enemies whose casting most needs stopping.""")

w('Phantasmal Calamity', """Heavy mental damage over a huge area at extreme range, against Will. It is one of the few area spells that targets that save, which makes it valuable against crowds of brutes, and it is a strong opening cast.

The burst is too large for Expansive Spellstrike, and mindless creatures are immune. As a direct cast it is his best area option against enemies with poor Will.""")

w("Poltergeist's Fury", """A storm of debris around himself that grows as he sustains it. It takes a full turn to start and an action each round, and it endangers allies who fight beside him.""")

w('Purple Worm Sting', """Poison that deals heavy damage over several rounds if the target keeps failing Fortitude saves. Poison immunity and resistance are common and the damage arrives late. Better spells exist at every rank.""")

w('Repulsion', """An aura that keeps enemies away from him. He fights by keeping enemies inside his reach, so this undoes his own plan. It might shelter a retreat.""")

w('Spellwrack', """Punishes an enemy for carrying spell effects. Against a heavily buffed opponent it strips its magic faster and hurts it meanwhile. Against anything else it does nothing.""")

w('Tangling Creepers', """A vast area that slows everything in it for ten minutes. It hampers an army's advance, and it costs a full turn and a sustain to do more than that. Rarely worth a top slot.""")

w('Vampiric Exsanguination', """A cone of heavy void damage that also gives him a large buffer of temporary Hit Points. Through Expansive Spellstrike it runs away from his allies, and against a group of living enemies it is both his area damage and his defence for the next round.

It harms only the living, and Fortitude is the save tough enemies pass. With those limits understood, it is one of the best cone spells at this rank for a fighter who expects to be hit.""")

w('Vibrant Pattern', """Dazzles what stands in it and can blind enemies that fail a Will save. It needs sustaining and has incapacitation, so it is aimed at groups of weaker enemies, where his actions are better spent attacking.""")

w('Vitrifying Blast', """A cone that damages, slows and makes brittle. Enemies that fail lose an action and take extra harm from bludgeoning and sonic, and even those that succeed are briefly weak to both. In a party with heavy bludgeoning damage that weakness is worth as much as the spell's own dice.

The cone is short, so it rarely catches more than two or three, and it relies on failed Reflex saves for the slow. A good spell when allies can exploit the weakness.""")

w('Wall of Metal', """A tall metal wall. Wall of Force is stronger and Wall of Stone is larger and permanent; this has little to offer beside them.""")

w('Zero Gravity', """Sets everything in a column adrift. It can strand melee enemies, but it needs a full turn and a sustain and hampers the party equally.""")

w('Awaken Entropy', """Damage over time in a small area that costs a full turn and a sustain. The return is far too low for a rank-6 slot.""")

w('Explosive Barrage', """A large burst and several small ones of mixed fire and sonic damage against Fortitude. As a direct cast it covers a scattered group well, and two damage types make resistance less of a worry.

Its several bursts cannot be delivered by Expansive Spellstrike, so it is only a ranged turn for him. Chain Lightning does that job with no risk to allies.""")

w('Frozen Fog', """A cloud that damages each round, slows and makes enemies clumsy, lasting a minute without sustaining. On a group that must stay where it is, the total is high and the penalties help the party's attacks.

The fog conceals everything inside it, including the enemies from his own party, and harms allies who enter. A sound opening spell against a held position.""")

w('Phantom Orchestra', """Sonic damage each time it is sustained. All of its value sits in an action he needs for recharging Spellstrike.""")

w('Scrying', """Watching a specific creature from anywhere. For finding an enemy, checking on a prisoner or learning what a rival is doing, it is the classic tool. Ten minutes to cast and a save to overcome; a scroll.""")

w('Utter Destruction', """A cone of two damage types with a deafening rider. Its damage is well below Vampiric Exsanguination's and Chain Lightning's at the same rank.""")

w('Missed Cue', """The best Will spell he can prepare. Solid mental damage, fear even on a successful save, and on a failure the target is slowed for as long as it remains frightened, which costs it actions over at least two rounds. Damage, a debuff and lost actions from a single Strike is as much as any spell at this rank offers.

It is a fear and mental effect, so mindless and fearless creatures ignore it. Where it is allowed and the enemy can feel fear, it belongs in a top slot.""")

w('Word of Revision', """A reaction that undoes a disaster: an ally's failed save is rolled again, or a killing blow leaves them standing. Once per creature each day it can prevent the single worst event of a fight.

It occupies a top slot for something that may not happen. For a party facing an enemy with deadly save effects it is excellent insurance.""")

w('Curse of the Toad Prince', """A toad for a minute on a failure, and even on a success the target is sickened and drops what it holds, which disarms a weapon user. That success effect gives it a floor most transformation spells lack.

It works only on humanoids and has incapacitation, so it is aimed at enemies of his level or lower. Against a humanoid of equal level it is very strong; against anything else it does not apply.""")

w('Proximal Shift', """A teleport that knocks down those he leaves and damages those he joins. It moves him sixty feet without provoking and makes a small impact at both ends.

It replaces a Spellstrike for the turn, and the effects are modest for a rank-6 slot. Dimensional Assault and Time Jump cover his movement more cheaply.""")


# ───────────────────────── rank 7 ─────────────────────────
w('True Target', """Sure Strike for the whole party, for one action. He and three allies each roll their first attack against the chosen enemy twice and ignore concealment, which against a single powerful enemy raises everyone's chance to hit and to crit in the round that matters most. For his own Spellstrike it does everything Sure Strike does without the ten-minute wait between uses.

It costs a top slot, so it competes with his hardest-hitting spells, and against a crowd its focus on one creature wastes it. In a fight against one dangerous enemy, with the party ready to attack, it is the best single action he can take.""")

w('Frigid Flurry', """A line that harms only enemies and carries him to its far end. Because it ignores allies it can be sent straight through a mixed melee, which no other line or cone allows, and the heavy damage comes in two types so that resistance seldom stops it. The movement at the end puts him where he chooses without provoking.

Through Expansive Spellstrike it covers the field beyond his target, and with Sprinting Spellstrike it is the cleanest spell he has for it. It has no rider. From level 13 it is his default area spell.""")

w('Beheading Buzz Saw', """A line of heavy slashing and persistent bleed with a small chance of killing outright. The bleed is unusually large and keeps working for rounds.

A successful save avoids everything, including half damage, and that is the common result on the enemies that matter. Frigid Flurry is far more dependable. Creatures that do not bleed lose half of what it offers.""")

w('Eclipse Burst', """An enormous burst of cold and void damage at long range. It is far too large to use near the party and cannot go through Expansive Spellstrike in any sensible way. A blast for a caster who stands at the back.""")

w('Telekinetic Bombardment', """Very heavy damage with a knockdown, and a choice of shape. The line version works through Expansive and Sprinting Spellstrike and leaves enemies that fail prone and off-guard, with rubble that slows whoever is left. At 500 feet it is also a fine opening cast.

It needs something large to throw, which the GM decides, and the knockdown needs failed Reflex saves. Bludgeoning is almost never resisted. A strong alternative to Frigid Flurry when control matters more than sparing allies.""")

w('Comet Charge', """Movement and a heavy attack-roll hit in one cast. He flies up to 120 feet without provoking, strikes with a choice of damage types, and has the target off-guard if he started above it. Through Spellstrike the damage rides his weapon's roll, so it is as reliable as his best attack spells and can aim at a known weakness.

It carries no control effect. Its real value is closing a long gap and delivering a full Spellstrike in the same turn, which otherwise costs him a round. A good top-slot choice on large battlefields.""")

w('Defy the Gods', """A debuff that lands on a success: the target is drained and stupefied, which lowers its Fortitude, its Hit Points and its spellcasting together. Against divine casters and creatures of the heavens or hells it also protects him from their damage.

It adds no damage and its effects are slow to pay off. It is a specialist's spell for a known divine or unholy enemy, and otherwise a poor use of a rank-7 slot.""")

w('Spell Riposte', """A reaction that tries to turn a spell aimed at him back on its caster. When it works it both saves him and hurts the enemy. It relies on a counteract check, does nothing against area spells, and holds a top slot idle until the moment comes.""")

w('Contingency', """A stored spell that casts itself when a condition he sets is met: a teleport when he is badly hurt, a defensive spell when he is first attacked. It costs no action in the fight and cannot be forgotten in the moment.

It takes ten minutes to prepare and a rank-7 slot to hold a spell of rank 4 or lower, which is a steep price each day. A scroll cast in the morning gives the same safety net and leaves the slot free.""")

w('Duplicate Foe', """A weaker copy of an enemy that fights for him while he sustains it. A full turn to cast and an action each round is the same cost that rules out every summon.""")

w('Energy Aegis', """Resistance to almost every kind of energy, for a whole day, on one creature. It costs nothing during a fight and takes a little off every spell and breath weapon that hits. Over a long adventuring day that adds up to a great deal of prevented damage.

Its duration makes it the ideal wand: cast each morning, it never touches his slots. As a prepared spell it would cost a top-rank slot he needs for attacking, which is too much.""")

w('Fiery Body', """He becomes living flame, immune to fire and stronger with fire spells, and vulnerable to cold and water. The aura rewards being touched, and he fights at reach. The benefits do not match the way he plays.""")

w('Heaving Earth', """A shockwave along the ground that shoves creatures in its path and hits one target at the end. Moderate control for a top slot, and far behind the line spells he already has.""")

w('Hungry Depths', """A growing vortex that needs a full turn and a sustain every round. Whatever its eventual damage, he cannot afford the actions.""")

w('Interplanar Teleport', """Travel between planes for the party. It is the key to a certain kind of adventure and useless in any other. A scroll when the journey requires it.""")

w('Lifewood Cage', """A cage that traps every creature in a large cube on a failed save, protecting them and holding them at once. It can remove half an encounter for a minute.

It takes a full turn and a sustain, enemies that succeed are simply moved outside, and the bars shelter those inside from the party's attacks too. Wall of Stone divides a fight more reliably.""")

w('Mask of Terror', """A defensive buff that makes attackers afraid. Each creature that tries to harm the target must save or be frightened, and may lose the action entirely. On whoever the enemy is focusing on, it weakens a good share of incoming attacks for a minute.

It needs failed saves and each creature is affected only once per round. Mindless enemies ignore it. A reasonable opening cast on a front-line ally when he cannot yet reach the enemy.""")

w('Momentary Recovery', """A teleport with a pause in which he can act on himself. It gives him a moment to drink a potion or cast a personal spell out of harm's way. Translocate moves him further for less.""")

w('Planar Palace', """A secure demiplane to rest in until the next day. It guarantees an undisturbed night in hostile country. A scroll for expeditions.""")

w('Planar Seal', """Blocks teleportation and planar travel across a wide area for a day. It matters against enemies that arrive or flee by magic, and only then.""")

w('Power Word Blind', """Blindness for one action with no save. Against enemies near his level the target is blind for minutes, which all but removes it from the fight, and one action leaves room for a full Spellstrike on the same turn.

Its strength depends entirely on the target's level: much stronger enemies are only dazzled. Against equals and slightly stronger foes it is one of the most efficient actions he can take from a top slot.""")

w('Prismatic Armor', """Resistance to seven damage types for a minute, with a chance to dazzle attackers. On whoever is taking the punishment it prevents a great deal in a fight with mixed energy damage. Energy Aegis gives a similar spread for a whole day from a wand.""")

w('Prismatic Spray', """A cone of random effects, some of them devastating. It can petrify, confuse or slow, or simply deal heavy damage, and each creature rolls separately.

The randomness is the problem for a caster with two slots at the rank: he cannot count on the result he needs. Frigid Flurry delivers known damage where he wants it.""")

w('Project Image', """Lets him cast from an illusory double. His spells go through his weapon, so a double that cannot Strike adds little.""")

w('Reverse Gravity', """Throws every creature in a wide column to the ceiling and holds it there for a minute. Enemies that cannot fly are out of the fight or badly placed, with no save for most of the effect.

It takes a full turn and it catches allies in the area. Used at range on the enemy's formation in the first round, it is among the strongest control spells he can cast.""")

w('Retrocognition', """Impressions of what happened in a place, reaching back years with enough time. For an investigation it can answer questions nobody living can. Scroll.""")

w('Shadow Raid', """Area damage that harms only enemies, in a type he chooses, and keeps hurting those who stay. Because allies are safe it can be dropped directly on a melee, which is rare among large bursts.

It costs a full turn and the damage per round is moderate for the slot. The enemy also picks the easier of two saves. Worth it when the fight is a tangle and he cannot aim a line.""")

w('Time Beacon', """A second chance at a turn, for one action. Cast first, it lets him take back a missed Spellstrike, a poor damage roll or a move that went wrong, and try the turn again. On a turn built around a top-rank spell and a single attack roll, that safety is worth a great deal.

It uses a high slot and an action that might have been Sure Strike or True Target, which raise the odds instead of insuring against them. Best kept for the one turn in a fight that has to work.""")

w('Vacuum', """Suffocates creatures around him, with incapacitation, a sustain, and equal danger to allies. Nothing about it suits him.""")

w('Warp Mind', """Confusion with no further saves for a minute, or permanently on a critical failure. With incapacitation it is aimed at equals and lesser enemies, and against those it is a strong spell; against a superior enemy it will not land.""")

w('Incarnate Tempest of Shades', """A full turn to call a manifestation that drains enemies as it arrives and frightens them as it leaves. It deals no damage and both effects need failed saves. A magus gives up too much to cast it.""")

w('Puppet Strings', """Control over an enemy's movements and some of its attacks if it fails, and a mild penalty if it saves. It has incapacitation and needs sustaining, so it works on lesser enemies at the cost of his own burst.""")

w('Spell Turning', """An hour-long ward that gives him one attempt to reflect a targeted spell. It can be cast before a fight with a known enemy caster, which is its advantage over Spell Riposte. It still depends on a counteract check and uses his reaction.""")


# ───────────────────────── rank 8 ─────────────────────────
w('Arctic Rift', """A long line aimed at Fortitude, which gives his Sprinting Spellstrike a spell for enemies that dodge everything else. The damage is very heavy, each enemy that fails loses an action, and a critical failure freezes it in place.

Big, tough creatures pass Fortitude saves more often than not, so the slow is least likely where it would matter most, and half damage is the usual result against them. It is the right line for nimble enemies and for groups of mixed types. Frigid Flurry remains safer in a crowded melee because it spares allies.""")

w('Disappearance', """Invisibility that defeats every precise sense and does not end when he attacks, for ten minutes. Every Strike in that time is against an off-guard target, so Laughing Shadow's extra damage is permanent, and enemies must guess his square before they can even try to hit him. No other defensive spell he can cast prevents as much.

It lasts long enough to cast before a fight, which removes its action cost. Enemies with reliable ways to find the unseen blunt it. Even beside Dimensional Disappearance it is worth a top slot for a fight that matters, and it can be given to an ally instead.""")

w('Quandary', """Removes one enemy from the fight with no saving throw at all. The target is shut in a puzzle room until it reasons its way out against his spell DC, which usually takes a few rounds, and during that time the party fights everyone else unopposed.

It needs sustaining, which costs his recharge each round, and the enemy returns unharmed. That makes it a tool for dividing a fight: remove the strongest enemy, finish the others, then face it together. For that purpose nothing at this rank is as certain.""")

w('Roar of Freedom', """More effect for one action than any other spell he can prepare. It deals heavy damage to every enemy around him, weakens those that fail, and gives his nearby allies a buffer of temporary Hit Points, and it still leaves two actions for a full Spellstrike on the same turn.

It harms only enemies, so standing in the middle of a melee is where he wants to be when he casts it. The debuff needs failed Will saves, but the damage and the Hit Points do not depend on them. Prepare it in a top slot from level 15 for any fight where he will be surrounded.""")

w('Desiccate', """Heavy void damage to any number of living creatures he chooses, out to 500 feet. Because he picks the targets it is completely safe for allies, and it can thin an entire enemy force before the lines meet.

It cannot be delivered by a Strike, and it does nothing to the unliving or to creatures without moisture. It is a ranged turn's spell. Chain Lightning does similar work two ranks lower against any kind of creature.""")

w('Uncontrollable Dance', """Three rounds of an enemy that is off-guard, cannot use reactions, and must waste an action each turn, even when it saves. That floor is remarkable: it feeds Laughing Shadow, frees the whole party from the enemy's reactions, and costs it a third of its turns.

It has incapacitation, so a higher-level enemy treats a success as a critical success and is unaffected, and mindless creatures are immune. Against an enemy of his level or lower it is one of the strongest spells there is; against a superior one it is a wasted slot.""")

w('Falling Sky', """Throws everything in a huge column to the ground, prone even on a successful save, and brings fliers crashing down with heavy damage. Against a flying enemy or a flock of them it is the definitive answer, and a prone group is off-guard for the whole party.

It has incapacitation for the stun, and the column is too big to use near allies. As a direct cast against airborne enemies it has no equal on his list.""")

w('Boil Blood', """Fire damage against Fortitude with a large second effect on a failure: the target is drained 2, which removes two further Hit Points for each of its levels and lowers its later Fortitude saves. A failed save is therefore one of the heaviest single-target results at this rank, and through Spellstrike it is simple to use.

On a success it is half the fire damage and no drain, and strong enemies pass Fortitude more often than not, so Polar Ray, whose drain needs only the Strike to hit, is the more reliable of the two. Creatures without blood are immune, and fire is commonly resisted. Choose it when Fortitude is the target's weaker save.""")

w('Confusing Colors', """A cloud that dazzles widely and confuses or stuns those that fail. It needs sustaining and has incapacitation, so it is a spell for crowds of lesser enemies from someone who can afford the upkeep.""")

w('Dream Council', """A meeting in a shared dream for up to twelve people anywhere. Useful for coordinating allies across distance. No bearing on a fight.""")

w('Earthquake', """Shakes a vast area with penalties, fissures and collapsing structures. Its size makes it nearly impossible to use without catching the party, and its effects depend heavily on the terrain.""")

w('Hidden Mind', """A day-long ward against mental effects and magical spying for one creature. Against an enemy that dominates or reads minds it protects the person most at risk. A scroll for that day.""")

w('Pinpoint', """Tells him exactly where a creature or object is, anywhere. It ends a search at once. Ten minutes to cast; a scroll.""")

w('Power Word Stun', """A stun for one action with no saving throw. Even the strongest enemy loses an action, and one of his level or a little above loses a whole round or more. Nothing else lets him take an action from a single powerful enemy with certainty and still Spellstrike in the same turn.

It works once per target in a fight. A magus could hardly ask for a better use of a top slot against one dangerous enemy.""")

w('Prismatic Wall', """A wall that harms and hinders anything trying to pass, lasting an hour. As a barrier it is close to absolute. It takes a full turn and blocks his own allies' attacks as well.""")

w('Rainbow Fumarole', """A column of random fire effects after a full turn. Unreliable and slow.""")

w('Unrelenting Observation', """Lets several people track one creature or object perfectly. A specialised tool for a chase or surveillance.""")

w('Whirlpool', """A battlefield spell for a fight against many enemies, cast from far outside it. The area is large enough to hold most of an encounter and all of it is difficult terrain. Every Sustain repeats the damage and drags creatures that fail back toward the middle, so enemies pay again for each round they spend getting out. By the second Sustain it has dealt more than a single blast at the rank would.

The cost is the actions. It takes a whole turn to cast, which rules out Spellstrike, and each Sustain is the action he would spend recharging. It also hits allies, so it has to land before the lines meet. Prepare it when a large group is expected and he can open from range; Arctic Rift serves better once the fight is joined.""", grades='BDD')

w('Sudden Transposition', """Moves enemies anywhere within 60 feet of him, with solid damage if they fail. Cast on its own it takes two creatures: he can pull an archer and a caster into his reach, or throw two brutes away from his allies, and the move alone can decide a round. Through Spellstrike it reaches only the creature he strikes, which is enough to send a dangerous enemy to the far side of the fight after the hit.

Nothing happens on a successful Fortitude save, which is the strong save of most large enemies. Most useful when the enemy's position is the problem and the target is not one of the hardy ones.""")

w('Incarnate Archmage', """A full turn for light damage and some disruption of enemy magic. The return is far too small for a rank-8 slot and three actions.""")

w('Take Your Places', """Teleports up to four allies anywhere within sixty feet. In one cast the party can surround an enemy, leave a trap, or get its wounded clear, and no one provokes.

It moves only the willing and does nothing by itself to the enemy. Valuable in a party that plans around position; expensive at this rank otherwise.""")

w('Polar Ray', """The strongest attack spell at this rank against a single powerful enemy, once the drain is counted. A hit deals moderate cold damage and leaves the target drained 2 with no save, which removes two further Hit Points for each of its levels and lowers its Fortitude saves for the rest of the fight. Against a creature of level 15 or higher that is more in total than Blood Feast or a heightened Briny Bolt delivers, and it sets up Slow, Arctic Rift or Weight of the World.

The drain does not double on a critical hit and does not stack with itself, so a second casting on the same enemy adds only the cold damage. Constructs and other creatures immune to drained take the cold alone. Prepare one for the day's main enemy.""", grades='ADD')

w('Metallic Meteorite Glyph', """Very heavy bludgeoning damage on a basic Reflex save, in a type almost nothing resists. Through Spellstrike its two-action form is simple and strong, and half damage on a success keeps it worthwhile.

The slower castings that add targets do not fit his turn. Chain Lightning heightened to this slot is comparable and more flexible. A good choice when electricity is resisted.""")


# ───────────────────────── rank 9 ─────────────────────────
w('Foresight', """An hour of protection for the person who matters most. With his reaction he can make an ally roll a save twice, or make an enemy roll twice and take the worse result on an attack against them. Over a fight that prevents several of the worst outcomes, and an hour often covers both of a day's encounters.

It uses his reaction each time, so it competes with Reactive Strike, and it holds one of his two highest slots. Cast on himself it is strong; cast on the party's healer or most fragile member it may be stronger. It costs no action once the fight begins, which is why it rates so highly.""")

w('Remake Physiology', """The heaviest debuff he can deliver. A living target is slowed in its movement and made worse at attacking, defending, casting and seeing, all at once, and it suffers a round of this even on a successful save. On a failure it lasts the fight, and everything the party does to that enemy afterwards is easier.

It needs a touch, which Spellstrike provides at reach, and it adds no damage. Against a single powerful enemy at the start of a fight, it is worth more than any damage spell in the same slot.""")

w('Falling Stars', """Four huge bursts of mixed damage anywhere within 500 feet. It covers an entire battlefield and lets him choose the energy type. As several bursts it cannot be delivered by a Strike, and it is too large to use near allies. A spell for open war, cast from a distance.""")

w('Phantasmagoria', """Heavy mental damage to as many creatures as he chooses, with reactions removed even on a success and confusion on a failure. Since he picks the targets it is safe in any melee, and stripping a whole enemy force of reactions for a round frees the party completely.

It is a direct cast and a mental effect, so mindless enemies ignore it. Among his top-rank area options it is the one that can always be used, wherever the party is standing.""")

w('Dimensional Excision', """Enormous untyped damage with heavy bleed, against Will, and without the mental trait, so almost nothing is immune. Half still lands on a success. Against creatures away from their home plane the save is much harder.

It has no control effect. As pure damage for his highest slot it is the most widely applicable he has.""")

w('Implosion', """A large fixed amount of damage to one target, then to a new target each round he sustains it. The first hit can ride a Strike. The later ones cost his recharge action, and no creature can be hit twice. Good total damage against a group, at the price of his own rhythm.""")

w('Massacre', """A line that kills weaker creatures outright and deals heavy damage to the rest. If nothing dies it turns on him. Against a column of lesser enemies it is devastating; against anything near his own level it is a gamble with his own Hit Points.""")

w('Bilocation', """A second body for ten minutes. He can act from whichever is better placed, both move when one moves, and together they cover twice the ground with reach and Reactive Strike. It makes flanking trivial and lets him threaten two parts of a fight at once.

Both bodies share his Hit Points and conditions, so area effects that catch both hurt once but any attack on either reaches him. It lasts long enough to cast beforehand. A strong, unusual use of a top slot for a positional fighter.""")

w('Detonate Magic', """Counters a spell or magic item and turns it into an explosion. It depends on a counteract check and on the enemy having magic worth destroying. Dispel Magic on a scroll does the essential part.""")

w('Magnetic Dominion', """Moves every armoured or metallic creature within a hundred feet as he wishes. Against an armoured army it is spectacular. It costs a full turn and a sustain, and against anything not made of or clad in metal it does nothing.""")

w('Power Word Kill', """Death with no save for a weaker enemy, and a large fixed loss of Hit Points for a stronger one, all for a single action. Against a powerful enemy that is guaranteed damage that leaves two actions for a Spellstrike, which no other top-rank spell offers.

It works once per target. As a finisher on an enemy already hurt, or as a certain opening blow, it is among the best uses of his highest slot.""")

w('Prismatic Sphere', """A seven-layered shell around a small space, nearly impassable for an hour. It protects a held position superbly and pins him to one spot, which is not how he fights.""")

w('Resplendent Mansion', """A grand, secure dwelling until the next day. Comfort and safety for the party between adventures. No effect on a fight.""")

w('Telepathic Demand', """A message with a suggestion attached, sent to someone he has contacted before, anywhere. A tool for long-range intrigue, with incapacitation and a full turn to cast.""")

w('Unspeakable Shadow', """Fear that costs actions. Even on a successful save the target is frightened and must spend an action each turn dealing with its own shadow, and on a failure the fear will not fade. Against a single enemy that is both a strong debuff and a steady drain on its turns.

It is a mental fear effect, so the usual immunities apply. Remake Physiology weakens a target more broadly; this is the better choice when taking actions matters most.""")

w('Incarnate Draconic Legion', """A full turn for a line and a cone of heavy damage that cannot overlap. The damage is real, but Frigid Flurry through a Strike does comparable work and leaves him a turn.""")

w('Prismatic Shield', """A one-action defence for a round: melee attackers suffer random prismatic effects, arrows are stopped, and spells aimed at him may be turned aside. On a turn when he expects the enemy's full attention it prevents a great deal and still leaves two actions for a Spellstrike.

It lasts one round and uses his highest slot. Best saved for the round a powerful enemy turns on him.""")

w('Weird', """Heavy mental damage and fear to any number of chosen creatures, with a chance of death on a critical failure. It is safe for allies and frightens even those that save.

Phantasmagoria does the same damage and removes reactions instead, which usually helps the party more. Both are fear or mental effects with the same immunities. Take one of them, not both.""")


# ───────── occult spells, from Witch Dedication, scrolls, wands or the stave after level 9 ─────────
w('Guidance', """The best cantrip to take with Witch Dedication. One action adds a point to an ally's most important roll of the round, or to his own Spellstrike, and it asks nothing else of his turn. It suits the third action he so often has spare. Each creature benefits once an hour, so it is for the roll that matters, not for every roll.""")

w('Forbidding Ward', """A small, lasting bonus to one ally's AC and saves against one enemy. Against a single dangerous foe it protects whoever that foe is attacking for the whole fight. It needs two actions and then a sustain each round, which is more upkeep than Guidance and competes with recharging.""")

w('Haunting Hymn', """A short cone of weak sonic damage against Fortitude. His arcane cantrips already do this job better, and a dedication cantrip is better spent on support.""")

w('Wash Your Luck', """Cancels a misfortune effect on one later roll. Misfortune is rare enough that the cantrip would sit unused in most fights.""")

w('Know the Way', """Tells him which way is north and where he last was. A convenience for exploration and nothing more.""")

w('Read the Air', """A social cantrip for the party's negotiator: a quick read of the room and a small bonus to making a good first impression. It supports the scenes where he does the talking. Guidance helps in more situations, which makes this the second choice for the dedication's cantrip.""")

w('Soothe', """Ranged healing he can cast from a scroll or wand once the dedication opens the occult list. It lets him pick up a fallen ally when the party's healers are busy or down. The amount is modest, so it is an emergency measure, and a wand gives one such rescue each day.""")

w('Bless', """A small attack bonus for the party in an aura around him. He fights in the middle of his allies, so the aura is well placed, but it costs two actions at the start and the party's divine caster does it better. A scroll at most.""")

w('Bane', """A small attack penalty for enemies near him if they fail a Will save. The effect is slight and needs a failed save. Fear does more to one enemy for certain.""")

w('Sanctuary', """Makes enemies save before they can attack the protected creature. It is at its best on a downed or fragile ally who will not be attacking. Useful from a scroll in a rescue; it ends if the target fights.""")

w('Protection', """A point of AC and saves for a minute. Small, and two actions to cast. From a wand before a known fight it is a fair use of the charge; in combat the actions are worth more.""")

w('Liberating Command', """One action to give a grabbed or restrained ally an immediate attempt to break free. Cheap and occasionally vital against enemies that grapple. A scroll or wand covers the need.""")

w('Ill Omen', """Makes one enemy roll its next attack twice and take the worse result, if it fails a save. Nothing happens on a success, and against a capable enemy that is the usual outcome.""")

w('Lose the Path', """A reaction that spoils an enemy's Stride, which can stop a charge short of its target. It competes with Reactive Strike, and an enemy moving past him is exactly what Reactive Strike punishes.""")

w('Phantom Pain', """Light mental damage with a lingering sickness if the target fails. The damage is poor and the sickened effect needs the failure. Goblin Pox sickens on a success from his own list.""")

w('Spirit Link', """Moves Hit Points from him to an ally each round for ten minutes. As a front-line fighter he usually needs his own. It could help keep a fragile ally standing between fights.""")

w('Gentle Breeze', """Slow healing for the whole party over ten minutes, and a bonus to Medicine in the area. Between fights it tops everyone up without anyone's daily resources but the wand's. That makes it one of the best wands he can carry after the dedication.""")

w('Sound Body', """Removes blindness, deafness, sickness, weakness or dazzle from an ally. When a key party member is blinded mid-fight, a scroll of this is the fix. Carry one.""")

w('Calm', """Stops a group from fighting if they fail their saves. It can halt a brawl or pacify guards without bloodshed, which suits a negotiator. It has incapacitation and needs sustaining, so it works on lesser opponents.""")

w('Silence', """Makes one willing creature soundless, and at rank 4 silences an area. For stealth it removes the noise of armour; the area version shuts down enemy spellcasters who stand in it. A scroll for infiltration, and a rank-4 scroll for a fight against a caster.""")

w('Clear Mind', """Counters fear and stupefaction on an ally, and stronger mental conditions in higher slots. On the day an enemy controls or confuses the party it is the cure. A scroll.""")

w('Cleanse Affliction', """Eases or removes a curse, disease or poison. These are problems for after a fight, and the party's divine caster normally handles them. A scroll as a backup.""")

w('Sure Footing', """Counters conditions that hinder movement: clumsy, grabbed, paralysed, and more in higher slots. A paralysed ally is one hit from disaster, so a scroll of this is worth carrying against enemies that paralyse.""")

w('Paranoia', """Makes one enemy distrust everyone, which may turn it against its own side. The useful result needs a failed save and the effect is hard to steer.""")

w('Augury', """A vague answer about a course of action in the next half hour. It can settle a debate about which door to open. Ten minutes to cast; a scroll for curiosity.""")

w('Spiritual Armament', """A spell attack with spirit damage that can be repeated by sustaining. Through Spellstrike it would ride his Strike, but his arcane spells hit harder, and the sustain competes with recharging.""")

w('Status', """Lets him know where an ally is and how they fare for a whole day. Useful when the party splits up. A wand makes it routine.""")

w('Heroism', """A bonus to attacks, saves and skills for ten minutes. Cast before a fight on himself, it makes every Spellstrike a little more likely to hit and to crit, and it lasts long enough to cost no action in combat. After the dedication a scroll or wand of this is one of the better things he can buy.""")

w('Hypercognition', """Up to six Recall Knowledge checks for a single action. He is the party's main source of information about enemies, and learning a creature's weak save and resistances in the first round shapes every spell he chooses afterwards. A wand of this is an excellent purchase.""")

w('Defensive Prescience', """A reaction that protects a familiar from an attack. It matters only if the Witch familiar is at risk, which he can avoid by keeping it out of fights.""")

w('Begone', """One action to hurl an enemy back if it fails a Fortitude save. It can clear a foe off an ally or over an edge. A failure is needed and big enemies seldom oblige.""")

w('Strength of Mind', """A bonus against mental effects and effects that hinder movement, for one action. Cast before meeting an enemy that charms or frightens, it shores up a weak save. A scroll.""")

w('Focusing Hum', """Helps stupefied casters and steadies confused allies near him while sustained. Too narrow, and the sustain is costly.""")

w('Infectious Melody', """Forces enemies to sing when they speak. It hampers their coordination slightly and little else.""")

w('Tortoise and the Hare', """Slows an enemy for a round even on a successful save, and on a failure also quickens him or an ally. It is Slow with a bonus attached. From a scroll it is a strong opening against a single enemy; Slow from his own slots gives the same floor.""")

w('Read Omens', """A cryptic hint about an event in the coming week. Flavourful, and of little practical use to the build.""")

w('Honeyed Words', """A large bonus to Lie for ten minutes. For the party's face in an infiltration or a tense deception it can carry a whole scene. A scroll for the day it is needed.""")

w('Synesthesia', """One of the strongest debuffs in the game, and it is on the occult list. The target is easier to hit, slower, struggles to target anyone, and may lose its spells, and it suffers a round of this even on a successful save.

He can only use it from a scroll or the stave, so it costs two actions and no Strike. Against a single powerful enemy at the start of a fight, that turn is worth it.""")

w('Strange Geometry', """Illusory terrain that slows those who believe it, for a full turn's casting. Weak control at a high cost.""")

w('Inevitable Disaster', """A large fixed amount of damage that arrives after a delay of a few rounds. The delay makes it hard to plan around and it cannot ride a Strike from a scroll.""")

w('Death Ward', """Resistance to void damage and protection against death effects for ten minutes. Against undead and necromancers it guards the party member most at risk. A scroll for those days.""")

w('Shadow Blast', """A choice of damage type and of area shape in one spell, though each target picks the easier of two saves. As an occult spell he could only cast it from a scroll, without a Strike, where his own area spells serve better.""")

w('Zealous Conviction', """Temporary Hit Points and a bonus against mental effects for the whole party, lasting ten minutes. Cast before a fight it is a meaningful buffer for everyone. A scroll for a known hard encounter.""")

w('Scintillating Safeguard', """A reaction that gives up to five allies resistance against one damaging effect. Against a breath weapon or a blast it prevents a great deal at once. It needs a scroll in hand at the right moment, which is awkward for a two-handed fighter.""")

w('Spirit Blast', """Heavy spirit damage to one creature, which reaches incorporeal enemies that shrug off most attacks. From a scroll it is a direct cast only. Worth carrying for a fight against a powerful spirit.""")

w('Blanket of Stars', """A Stealth bonus, and invisibility while he stays still under an open night sky. A narrow tool for outdoor ambushes.""")

w('Shock to the System', """Brings back someone who died in the last round, heals them and speeds them up. A death undone is worth any price, and this does it for two actions with no ritual. A scroll of this is the best insurance the party can carry once he can use occult scrolls, and a wand is better still.""")

w('Ethereal Jaunt', """A minute on the Ethereal Plane: through walls, past guards, unseen. For scouting and infiltration it is nearly unstoppable. It needs sustaining and he cannot affect the material world while there. A scroll for the heist.""")

w('Visions of Danger', """An area of illusory monsters dealing mental damage each round. A full turn to cast, and enemies who disbelieve are unharmed.""")

w('Orb of Twisting Fate', """Makes an enemy waste an action each turn if it fails. It does little on a success and has a very short range.""")

w('Spirit Song', """A long cone of spirit damage that stops reactions on a failure. It reaches incorporeal creatures. From a scroll it is a direct cast, and his own cones do more through a Strike.""")

w('Spiritual Epidemic', """A lasting curse that weakens and stupefies, spreading to those who cast divine or occult spells on the victim. It needs a failed save and suits a very particular enemy.""")

w('Overwhelming Presence', """Forces any number of creatures to spend actions paying him tribute, with some effect even on a success. Against a crowd it wastes a great many enemy actions. It has incapacitation, so the strongest enemy present is the least affected.""")

w('Unfathomable Song', """Random debuffs on up to five enemies each round he sustains it. It has incapacitation and the sustain takes his recharge action.""")


# ───────────────────────── cards added on 28 November 2026 ─────────────────────────
E['Trade Items'] = ('002003', 'CBD', """Swaps a small item in his hand for one an enemy holds or carries, at 60 feet, unless the enemy succeeds at a Reflex save. Aimed at a wand, a key, a potion or the object the enemy is guarding, it takes away the one thing a fight or a theft turns on, and through Spellstrike it follows a hit on the same target.

He has to be holding something of light Bulk to give in exchange, most weapons are too heavy for it before rank 5, and a successful save wastes the cast. A scroll for the day a single object matters.""")
E['Forest of Gates'] = ('000204', 'CBD', """Carries the party up to 1,000 miles in an hour's walk, and the walk restores Hit Points and reduces doomed and drained as a night's rest would. Arrival depends on a DC 40 Arcana or Nature check, which his Arcana usually makes, and even a failure lands within 10 miles.

It does not restore spells, and Teleport covers the same distance from a rank-7 slot. A travel spell for the top slot on a day with no fight in it.""")
