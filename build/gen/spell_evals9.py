"""Spell evaluations in their current wording, applied last.

The standard:
 - An evaluation judges the spell for Cyrus; the rules text sits directly above it on the card, so it is not repeated.
 - It is written in full sentences that carry their reasons with them (because, so, which means). No verbless
   openings, no lists of bare assertions, and no drawback named without saying why it matters.
 - It describes what Cyrus does with the spell and when. It gives no instructions to the reader (prepare, learn, keep,
   skip) and uses no shorthand: nothing figurative, no optimisation slang, and no wording that only makes sense to
   someone who followed the discussions behind the grades.
 - No party names, campaign, named monsters, printings, rulings or references to other pages.
 - Length follows from what needs saying. Low-graded cards are two or three sentences.
"""
from spell_evals_base import E


def w(name, text):
    r, g, _ = E[name]
    E[name] = (r, g, '\n\n'.join(' '.join(p.split()) for p in text.strip().split('\n\n')))


# ───────────────────────── cantrips ─────────────────────────
w('Gouging Claw', """Gouging Claw is the spell Cyrus puts into a Spellstrike on any turn he is not spending a slot, and no other cantrip does that as well. It deals more damage than any of them, and because a Spellstrike settles it with the Strike's attack roll, it is as accurate as his weapon and doubles on the same critical hit. Its touch range costs him nothing, since the Strike carries it to the end of his reach, and the bleeding it causes continues through the turn he spends recharging.

He chooses slashing or piercing each time, which gets round most physical resistances. The exception is a creature that cannot bleed and resists both types, and against that he uses Ignition instead.""")

w('Ignition', """Ignition is the second attack cantrip Cyrus wants, mainly because fire is the energy type that enemies are most often weak to. Through a Spellstrike it always counts as a melee casting, so he gets its larger dice, and it does only slightly less than Gouging Claw against a target with no weakness. It has no added effect unless the Strike is a critical hit, which is why Gouging Claw remains the usual choice.

Unlike Gouging Claw it can also be cast at 30 feet, which gives him something to do on a turn when no enemy is within reach.""")

w('Needle Darts', """Needle Darts has two advantages over the other attack cantrips. It takes on the properties of the metal it is cast from, so with a silver coin and a cold iron nail in his pouch Cyrus can strike at a material weakness without owning a second weapon, and its 60-foot range makes it the best cantrip he has for a turn when he cannot reach anyone.

Against a target with no such weakness it deals a little less than Gouging Claw, and its piercing damage is something Gouging Claw already offers. It is therefore worth a cantrip slot once he carries the metals, and before then Ignition is the more useful second attack cantrip.""")

w('Live Wire', """Live Wire is the only attack cantrip that still deals some damage when the Strike misses. A missed Spellstrike normally wastes most of a turn, so that protection is valuable at low levels and against enemies with high AC, and electricity gives him a third energy type.

Its damage grows at half the rate of Gouging Claw's and Ignition's, and by about level 7 the gap is too large for the reliability to make up. It is a good cantrip for the early levels that he will replace later.""")

w('Frostbite', """Frostbite is the cantrip Cyrus uses when an enemy's AC is the obstacle. Because it is settled by a Fortitude save and not by the attack roll, a heavily armoured target with poor Fortitude still takes its damage when the Strike misses, and cold is a type none of his attack cantrips deal. Its 60-foot range also makes it a reasonable spell to cast on a turn spent out of reach.

It deals less than the attack cantrips and a successful save halves it, so against most targets Gouging Claw is still the better choice. Frostbite is for the fights in which the Strike is unlikely to land.""")

w('Electric Arc', """Electric Arc is excellent for a caster who stands back and much less so for Cyrus. Its strength is that it damages two creatures, and through a Spellstrike only the creature he hits is affected, so the second target is lost.

What is left is a spell to cast from a distance at two enemies on a turn when he cannot get into melee, and a source of electricity damage. That is enough to keep it for days with flying enemies or ground that is hard to cross, although Needle Darts usually serves those turns better.""")

w('Void Warp', """Void Warp is a second Fortitude cantrip, but it does nothing to a creature that is not alive, whereas Frostbite damages everything. Its added effect appears only on a critical failure, which is rare, so there is no reason to know both and Frostbite is the one to choose.""")

w('Telekinetic Projectile', """Telekinetic Projectile deals bludgeoning, piercing or slashing damage depending on the object it throws, and it needs a loose object nearby to work at all. Gouging Claw already gives two of those types with more damage and bleeding on top, so only the bludgeoning option sets this apart, and Cyrus seldom needs that from a spell.""")

w('Tangle Vine', """Tangle Vine gives up a cantrip's damage in exchange for hindering the target. The Strike still deals its own damage, and a hit also slows the target's movement, while a critical hit holds it in place. Against an enemy trying to get past Cyrus to the allies behind him, or one that keeps moving out of his reach, that can be worth more than the dice of an attack cantrip, and the effect lasts longer as the spell heightens.

The enemy can break free with an action, although that is an action it does not spend attacking. This makes it a spell for fights against mobile enemies, with Gouging Claw remaining the choice on most turns.""")

w('Caustic Blast', """Caustic Blast is the cheapest burst Cyrus can put through Expansive Spellstrike, but it is too weak to be worth doing. Its damage is low and improves only every second rank, and the burst is so small that it rarely reaches a second enemy without also reaching an ally. The area spells he casts from slots do the same thing far better.""")

w('Scatter Scree', """Scatter Scree deals light damage and leaves a patch of difficult terrain. Its area is not a burst, cone or line, so even with Expansive Spellstrike it affects only the target's own space. Cast on its own it can slow movement through a doorway, which is a small return for one of his few cantrip slots.""")

w('Daze', """Daze is the only cantrip that targets Will, but its damage is weak and its stun needs a critical failure. It is worth knowing only if Cyrus wants a cantrip for every save, or needs to subdue someone without killing them.""")

w('Shield', """Shield suits a fighter who uses both hands on his weapon and often has a third action left over, because it costs one action, needs no free hand and adds a point of AC for the round. Its block is the more valuable part: it can reduce the damage of a spell or of one heavy hit, which an ordinary shield cannot do against magic.

Blocking takes his reaction, so from level 6 he has to choose between it and Reactive Strike, and once the block has been used the spell is unavailable for ten minutes. Even so, the AC alone repays the action on any turn that does not need a Stride or a recharge, which is why he prepares it every day.""")

w('Detect Magic', """Detect Magic does nothing in a fight and is still one of the most useful cantrips Cyrus can prepare. Knowing whether a room, a door or a stranger carries magic prevents many avoidable mistakes, and as the group's Arcana specialist he is the natural person to cast it.

Until it is heightened it tells him only that magic is present, not what kind. If another caster already keeps it running he can give the slot to something else, but otherwise it belongs on his list for any day of exploration.""")

w('Figment', """Figment creates a small illusion, which is worth more to Cyrus as a talker than as a fighter. A noise down a corridor or a shape at a window draws a guard's attention from a distance and gives him a bonus to Create a Diversion, and both fit the way he approaches infiltration and negotiation.

The illusion is crude at close range and has to be sustained, so it can distract someone but cannot disguise anything. Aspera's stave is planned to carry it from level 8, which would give him the spell without using a cantrip slot.""")

w('Telekinetic Hand', """Telekinetic Hand moves a small object from a safe distance, such as a key on a hook, a lever or a suspicious box. That is handy during exploration, but it has no use in a fight, and a ten-foot pole or a careful ally can do most of the same things.""")

w('Message', """Message lets Cyrus speak silently, with one action, to someone across a room or a courtyard. For a group that plans, splits up or works a social scene together this is very useful, whether as a warning to a scout, a cue during a negotiation or a question nobody else should hear.

In a fight it does no more than help with coordination. Because he so often does the talking for the group he gets more from it than most characters would, which justifies one of his few cantrip slots on days built around stealth or conversation.""")

w('Time Sense', """Time Sense tells Cyrus the exact time, which occasionally helps when a plan depends on timing, and the small bonus it offers almost never applies. It is the stave's cantrip because it suits Aspera's theme, and that is the only place it is worth having.""")

w('Eat Fire', """Eat Fire is a reaction that reduces one instance of fire damage and leaves Cyrus with a puff of smoke to breathe out. The resistance is small, it uses the reaction he wants for Reactive Strike, and it helps against a single damage type. On a day when fire is expected, a scroll of Resist Energy protects him far better.""")

w('Gale Blast', """Gale Blast is a small burst around Cyrus that can push adjacent enemies back to the distance where his reach weapon works and their weapons do not. That suits a reach fighter in principle, but the damage is poor and the push needs a failed save, and a Step gives him the same spacing for one action.""")

w('Puff of Poison', """Puff of Poison is a Fortitude cantrip whose persistent damage carries on while Cyrus recharges. Against that, poison is one of the most commonly resisted damage types, the range is very short, and the damage improves only every second rank. Frostbite is the better Fortitude cantrip in nearly every fight.""")

w('Spout', """Spout targets Reflex and can leave its target off-guard, which would help Cyrus a great deal if it did not need a critical failure. Without that result it is low damage that improves slowly, so it is not worth a cantrip slot.""")

w('Slashing Gust', """Slashing Gust needs a free hand to cast, and two free hands to reach a second target. Cyrus fights with both hands on his weapon, so he cannot use it in a Spellstrike at all.""")

w('Timber', """Timber is a short line of damage against Reflex, with an added effect only on a critical failure. A line that short seldom reaches a second enemy even through Expansive Spellstrike, and the damage is ordinary, so the area spells Cyrus casts from slots are a much better use of the feat.""")

w('Phase Bolt', """Phase Bolt partly ignores shields and cover, which matters a good deal against the few enemies that rely on them and not at all against the rest. Its damage also falls further behind Gouging Claw's as Cyrus gains levels. It is worth preparing only on a day when he expects shield-users or enemies fighting from cover.""")

w('Glass Shield', """Glass Shield gives the same AC as Shield but a much weaker block, with a little damage to whoever breaks it. The value of blocking comes from Shield's higher Hardness, so this is a worse version of a cantrip Cyrus already prepares.""")

w('Warp Step', """Warp Step gives two Strides for two actions with a small bonus to Speed. That bonus does not combine with the one Laughing Shadow already gives Cyrus in Arcane Cascade, so the spell adds nothing he lacks, and Dimensional Assault moves him about a fight far more effectively.""")

w('Light', """Cyrus cannot see in the dark, so on many days he needs a light, and this cantrip provides one that needs no hand and lasts until his next preparations. A torch or an everburning torch does the same without using one of his few cantrip slots, which is the only reason he does not prepare it daily.

It is worth preparing for a day underground if none of his allies is carrying a light. Because the light can be placed up to 120 feet away, it also lets him see what is ahead before he walks into it.""")

w('Prestidigitation', """Prestidigitation cleans, warms, tidies and adds small flourishes. That has some charm in social scenes where appearance counts, but it changes nothing mechanically, and Cyrus has too few cantrip slots to spend one on it.""")

w('Read Aura', """Read Aura tells Cyrus whether an object is magical and makes it easier to identify, and he is the member of the group most likely to be doing the identifying. It takes a minute to cast, so it is used in the quiet after a fight.

Detect Magic answers the first half of the question faster, and the bonus Read Aura gives is modest. It is worth preparing on days when the group expects to sort through treasure or search a magical site, and can stay in the spellbook otherwise.""")

w('Infectious Enthusiasm', """Infectious Enthusiasm costs two actions for a one-point bonus that lasts a round, and allies must spend actions of their own to share it. Cyrus needs his actions for Spellstrike and recharging, so the price is far too high for what it gives.""")

# ───────────────────────── rank 1 ─────────────────────────
w('Sure Strike', """Sure Strike is the most valuable rank-1 spell a magus can prepare. A Spellstrike stakes a whole turn's damage on one attack roll, and this spell lets Cyrus roll that attack twice and keep the better result. That raises the chance of a hit and, more importantly, the chance of a critical hit, which doubles both the Strike and the spell inside it. It also removes the miss chance from concealment, which would otherwise cost him one attack in five.

It takes an action, so he uses it on a turn that begins with an enemy in reach and Spellstrike charged, and it works only once in each fight. With one or two fights in a day, his two rank-1 slots supply exactly as many castings as he can use, which is why both hold it until higher slots take over some of that work.""")

w('Thunderstrike', """Thunderstrike is a dependable single-target damage spell that stays useful in every slot, because it gains a full set of dice with each rank. It is settled by a Reflex save, so it still deals half damage when the target succeeds and it applies even when the Strike misses. Against an enemy in metal armour it is better still, since that enemy saves at a penalty and is left easier to hit.

Against other targets it has no added effect, and agile enemies will often halve it. Sudden Bolt deals more from rank 2 upward, so Thunderstrike's place is as the standard save-based damage spell in his lower slots, and as a scroll for a turn when he has to attack from as far as 120 feet.""")

w('Dehydrate', """Dehydrate is weak in a rank-1 slot and one of the best damage spells Cyrus has once it is heightened. Every two ranks add a large amount of persistent fire damage and widen the burst, and persistent damage keeps arriving during the turns he spends recharging. Affected enemies must also keep saving or become enfeebled, which weakens the ones that fight back in melee.

Because the damage arrives over several rounds, the spell suits long fights against durable enemies and is wasted on anything that will die quickly. Its burst will also reach allies when it is placed through Expansive Spellstrike. He does best to learn it early and cast it from rank-3 slots and higher.""")

w('Fear', """Fear is the best weakening spell available for its slot, because it still works when the target succeeds at its save. A frightened enemy is worse at everything for a round or more, which makes it easier to hit, easier to affect with the next spell and less accurate when it attacks. Through a Spellstrike that comes on top of the Strike's damage, and every ally who acts before the condition fades benefits from it.

From a rank-3 slot it affects five enemies when cast without a Strike, which is a strong way to open a fight against a group. Mindless creatures and anything immune to fear ignore it, so on days when those are expected he needs something else in its place.""")

w('Fleet Step', """Fleet Step gives a large bonus to Speed for a minute. That is useful in a chase, a race to an objective or a fight spread over a very large area, and makes little difference elsewhere, because Dimensional Assault and his reach already solve most problems of position. It is a status bonus, so it replaces the Speed bonus from Laughing Shadow instead of adding to it. He prepares it only when he knows the day will need it.""")

w('Tailwind', """Tailwind from a rank-2 wand gives a Speed bonus that lasts all day, which most characters are glad to have. Cyrus gains less than they do, because it is the same kind of bonus Laughing Shadow gives him in Arcane Cascade and the two do not add together. It still helps on the turn before he has entered the stance and throughout the day outside combat, which is enough to justify the wand but never one of his slots.""")

w('Grease', """Grease is an inexpensive way to knock several enemies prone at once. Each one that falls is off-guard to Cyrus and to every ally in melee, and must spend an action to stand. It works best cast without a Strike over a doorway or a tight group in the first round, because through a Spellstrike it loses most of its area.

Everything depends on the enemies failing Reflex saves, and those with good balance are barely troubled by it. It is a reasonable use of a rank-1 slot against clumsy or heavily armoured groups, and Fear achieves more against anything else.""")

w('Befuddle', """Befuddle prepares a target for whatever follows it. Even on a successful save the target is easier to hit and worse at casting for a round, and because it is clumsy, the Reflex DC against which Cyrus rolls a Trip is lower as well. The effect ends quickly, so its value depends on his allies acting on it at once.

Fear imposes a similar penalty that applies to more of what the enemy does and fades more slowly. Befuddle is the better choice against a spellcaster, where the stupefied condition can cause its next spell to fail. Mindless creatures are immune to it.""")

w('Briny Bolt', """Briny Bolt is the best attack spell Cyrus can learn at low level. Every hit blinds the target for a round unless it spends an action clearing its eyes, so the enemy either loses that action or attacks with an even chance of missing, and a blinded enemy is off-guard to everyone. Because the spell is settled by his Strike's roll, the target gets no save against the blindness, and the damage grows with every rank.

It needs a target that relies on eyes, and bludgeoning damage rarely meets a weakness. He prepares it in whichever of his low ranks is not holding Sure Strike and continues to cast it from higher slots as he gains them.""")

w('Shocking Grasp', """Shocking Grasp deals heavy damage on an attack roll, a little more than Briny Bolt at every rank. Against an enemy in metal armour it is better again, because it becomes more accurate and leaves persistent damage behind. Its touch range is no drawback, since a Spellstrike carries it to the end of his reach.

Against other targets it has no added effect, so on most days the blindness from Briny Bolt is worth more than the extra dice. Shocking Grasp is the better choice when the aim is to finish one enemy quickly, when electricity is its weakness, or when it wears metal armour.""")

w('Force Barrage', """Force Barrage cannot go into a Spellstrike, because it has neither an attack roll nor a save. What it offers is damage that cannot miss at long range, which is useful for finishing an enemy that is fleeing or for breaking a spellcaster's concentration. That need is occasional enough to be met by a wand or a scroll, without using one of his slots.""")

w('Breathe Fire', """Breathe Fire is the plainest cone Cyrus can put through Expansive Spellstrike. Its damage keeps up as it is heightened, but it does nothing else, and the cone is short enough that it rarely reaches more than two enemies. It serves as a first area spell from level 2 to 4, after which better cones replace it.""")

w('Dizzying Colors', """Dizzying Colors can take several weak enemies out of a round at once, but it is unreliable against anything dangerous. It has the incapacitation trait, so stronger enemies treat their saves as one step better, and even weaker ones are far from certain to fail. The dazzled condition it leaves on a successful save is some compensation.

It is therefore a spell for a fight against a crowd of lower-level enemies, with the cone pointed away from allies, and a wasted slot against a single strong one.""")

w('Pummeling Rubble', """Pummeling Rubble is a small cone of weak damage that pushes enemies directly away from Cyrus, which someone fighting with a reach weapon seldom wants. Acid Grip moves an enemy in whatever direction he chooses and does so even on a successful save, so this has no use once that spell is available.""")

w('Gust of Wind', """Gust of Wind is a modest spell at low level and an important one from level 12. Until then it is a line that knocks down whatever fails a Fortitude save and holds back flying creatures and archers behind it, which makes it useful mainly for clearing fog or defending a corridor.

With Sprinting Spellstrike it becomes the cheapest way for Cyrus to cross 60 feet without provoking reactions, leaving a row of prone and off-guard enemies along his path, and it does this from a rank-1 slot. It has no effect on Huge creatures and knocks down only those that fail their saves. For those reasons it is worth learning by level 12 and preparing regularly from then on.""")

w('Goblin Pox', """Goblin Pox sickens its target even on a successful save, and through a Spellstrike Cyrus can apply it from the full length of his reach. A sickened enemy takes a penalty to everything it rolls and stays that way until it spends an action retching, so in a long fight against one living enemy the spell repays its slot well.

Fear has much the same effect, works on more kinds of enemy and fades without help. Goblin Pox is the alternative for targets that are immune to fear, provided they are alive and can catch a disease.""")

w('Leaden Steps', """Leaden Steps makes its target weak to electricity, so every later hit from Thunderstrike, Shocking Grasp or a Shock rune deals more. The target is also encumbered, which slows it and makes it easier to hit, and that helps to keep it within his reach.

Maintaining the spell takes an action each round, the same action Cyrus needs for recharging, and on a successful save it lasts only a moment. It repays the effort when several of his allies also deal electricity damage. When he is the only one who does, the turn spent casting it usually costs more damage than the weakness returns.""")

w('Command', """Command does nothing when the target succeeds at its save, and against a capable enemy that is the likely result. When it does work it wastes one of the enemy's actions. Fear uses the same slot and always achieves something, which leaves little reason to prepare this.""")

w('Curse of Slippery Steps', """Curse of Slippery Steps hampers one enemy's movement. That can spoil a charge or slow someone who is running, but it does not stop the enemy attacking, and Tangle Vine does something similar as a cantrip. It is not worth a slot.""")

w('Hydraulic Push', """Hydraulic Push deals respectable damage on an attack roll and pushes its target back. Through a Spellstrike the push can free an ally from a grapple, move an enemy into another ally's reach or send it off a ledge, and whether it happens is decided by the Strike's roll.

The push is always directly backward and only five feet on an ordinary hit, whereas Acid Grip moves a target in any direction and works even on a successful save. Briny Bolt is the better attack spell for general use, so Hydraulic Push is worth a slot only when knocking something backward is the purpose of casting it.""")

w('Grim Tendrils', """Grim Tendrils is a line of low damage against Fortitude that harms only living creatures. It is one of the few lines available at rank 1, which gives it a small use with Sprinting Spellstrike, but Gust of Wind does the same with a much better effect.""")

w('Horizon Thunder Sphere', """Horizon Thunder Sphere is a sound attack spell in its two-action form, dealing electricity damage close to Shocking Grasp's on the Strike's roll and growing with every rank. That gives Cyrus a second source of electricity damage.

Its other forms do not suit him. The three-action version leaves no room for a Strike, and the version that takes two rounds is too slow for someone who does most of his damage in single turns. As it has no added effect on an ordinary hit, Briny Bolt usually contributes more to a fight. It is worth learning only if he wants an electricity spell that, unlike Shocking Grasp, can also be cast at range.""")

w('Mystic Armor', """Mystic Armor replaces armour that Cyrus already wears. It would matter only if he gave up medium armour to gain the larger Speed bonus Laughing Shadow offers when unarmoured, and that exchange costs too much AC for someone who fights at the front.""")

w('Jump', """Jump is a one-action leap that clears a gap or reaches a ledge. It helps on broken ground before Cyrus can fly, but Dimensional Assault already covers most short movements of that kind, so a scroll is as much as it deserves.""")

w('Gentle Landing', """Gentle Landing cancels a fall, however far, for anyone within 60 feet, and it is cast as a reaction. Most falls happen outside combat, on a climb or a bridge, when his reaction is not needed for anything else.

The need is rare but complete when it comes, which makes this a spell to carry as a scroll and hold in hand while his allies climb. A prepared slot is justified only on a day of flying or of travel along cliffs.""")

w('Interposing Earth', """Interposing Earth is a defensive reaction that makes one attack or area effect less likely to hurt Cyrus and slightly smaller if it does. Before level 6 he has nothing else to spend his reaction on, so giving it a spare rank-1 slot is reasonable.

From level 6 it has to be weighed against Reactive Strike, which is usually the better use of the reaction, and its protection is small beside Hidebound or Warping Pull at rank 2. It is a spell for the early levels only.""")

w('Illusory Object', """Illusory Object is one of the most flexible spells Cyrus can know for use outside a fight. A false wall, a closed door where an open one stands or a crate to hide behind can settle an escape, an ambush or an infiltration in ways no combat spell can, and from a rank-2 slot the illusion holds up to touch and sound for an hour.

It has no direct use in combat and asks for some imagination and a little time. Aspera's stave is planned to carry it from level 8, and until then a scroll is the sensible way to keep it available.""")

w('Illusory Disguise', """Illusory Disguise is for infiltration that has been planned in advance, and it improves in higher slots, where it can copy a particular person or cover the whole group. As the one who usually does the talking, Cyrus has real use for it. Because it is never needed at a moment's notice, a scroll, and later the stave, is enough.""")

w('Helpful Steps', """Helpful Steps creates a staircase or ladder that everyone can use, which is far cheaper than giving each of them a way to fly or climb. It deals with a wall or a pit completely and does nothing else, so it is best carried as a scroll.""")

w('Runic Weapon', """Runic Weapon grants runes that his weapon already has. It would matter only if Cyrus were disarmed or had to fight with a borrowed weapon, and even then it costs two actions.""")

w('Conductive Weapon', """Conductive Weapon adds electricity damage to a metal weapon for a minute, and more against armoured enemies. Cast before a fight it adds a little to every Strike made with that weapon, whether his or an ally's. Two actions during a fight are too many for that, and a permanent rune later gives the same benefit.""")

w('Friendfetch', """Friendfetch pulls one or two allies straight to Cyrus, which can take someone out of a grapple, a hazard or an enemy's reach without costing them an action. On the day that is needed it can save a life, and on every other day the slot would go unused, so it is better carried as a scroll.""")

w('Pocket Library', """Pocket Library gives a day-long bonus to Recall Knowledge with one skill and removes the risk of a critical failure. Cyrus identifies enemies for the group, and knowing a creature's weakest save decides which spell he uses against it, so the benefit applies often. As it lasts 24 hours, it is well suited to a wand that he uses each morning.""")

w('Schadenfreude', """Schadenfreude can be cast only when Cyrus critically fails a save, which he cannot plan for and hopes will not happen. A slot kept for that moment goes unused in every fight that goes well, so the spell is a poor use of one.""")

w('Acidic Burst', """Acidic Burst deals more damage for its rank than almost any other save spell, but cast as written it burns every ally standing next to Cyrus. A Spellstrike removes that problem, because the spell then affects only the creature he strikes, anywhere within his reach. Used that way it is a strong single-target Reflex spell that deals acid damage and stays useful in every slot.

It has no added effect, and Thunderstrike and later Sudden Bolt do the same work, so the choice between them comes down mostly to damage type. Casting it without a Strike makes sense only when everything next to him is an enemy.""")

w('Agitate', """Agitate punishes an enemy for standing still, which suits someone with reach and Reactive Strike. A target that must move each turn or take damage either gives up its position or provokes a reaction, and the spell has some effect even on a successful save.

The damage is modest and can be avoided, and an enemy that meant to move anyway loses nothing. Agitate is most useful against an archer or spellcaster that has found a safe place to stand, and from level 6 against anything inside his reach. Mindless creatures are immune.""")

w('Alarm', """Alarm wards a campsite for the night, and it is an ideal spell for a wand: used every evening, it protects each rest without taking a slot. Prepared in a slot it would displace a Sure Strike, and that is not a worthwhile exchange.""")

w('Ant Haul', """Ant Haul increases carrying capacity for a day. With his Strength, Cyrus is rarely the one who needs it.""")

w('Anticipate Peril', """Anticipate Peril gives a small bonus to one initiative roll. Cyrus already improves his initiative through Incredible Initiative, and a rank-1 slot holding Sure Strike does far more for him once the fight has started.""")

w('Carryall', """Carryall creates a floating platform for cargo. It is convenient for moving treasure and has no other use, and a pack animal or a spacious pouch does the same without taking a slot.""")

w('Charm', """Charm is a social spell that Cyrus, as the group's negotiator, can use with care. When it works it makes a guard, a clerk or a reluctant witness friendly for an hour, which can open doors that Diplomacy alone would not. It fails outright against anyone his side has threatened, it has the incapacitation trait, and being seen to cast it usually ends the conversation.

Since success is uncertain, it adds to his Diplomacy without replacing it. The need is occasional and never arises in the middle of a fight, so a scroll or wand is the right way to carry it.""")

w('Chilling Spray', """Chilling Spray is a small cone that slows the movement of whatever fails its save, with weak damage that improves slowly. The Speed penalty rarely decides anything, and Breathe Fire deals more damage in the same shape.""")

w('Déjà Vu', """Déjà Vu forces an enemy to repeat its last turn, which is clever against one that has just wasted a turn, but it does nothing on a successful save. Because it has the incapacitation trait, a successful save is the usual result against anything dangerous.""")

w('Draw Ire', """Draw Ire discourages one enemy from attacking anyone but Cyrus, and it works even on a successful save. He is not the most durable member of the group, so drawing attacks is seldom what he wants, and the penalty it imposes is small.""")

w('Echoing Weapon', """Echoing Weapon deals damage that builds with the number of Strikes made in a turn. Cyrus makes one or two, so he gains almost nothing from it, and it is better suited to someone who attacks three or four times.""")

w('Endure', """Endure grants a few temporary Hit Points for one action at touch range. The amount is too small to change a fight, and any of his other rank-1 spells makes better use of the slot.""")

w('Enfeeble', """Enfeeble works mainly as protection. An enfeebled enemy hits less often and less hard and is worse at grappling and shoving, and part of that applies even on a successful save. Against a single strong melee enemy that is hurting his allies, it protects everyone that enemy attacks.

Fear weakens more of what an enemy does and also helps his side land its own attacks, so it is usually the better choice. Enfeeble is for enemies that are immune to fear or to mental effects, provided they rely on Strength.""")

w('Flourishing Flora', """Flourishing Flora is a very small burst with a choice of damage type and an added effect only on a critical failure. Its damage is poor and its area too small to justify Expansive Spellstrike, and cantrips are a better way to have a choice of damage types.""")

w('Gravitational Pull', """Gravitational Pull is interesting because it takes only one action. On a turn when Cyrus has already used his Spellstrike, he can spend his third action to drag an archer or spellcaster into his reach, set up a Reactive Strike or pull an enemy away from an ally. It can also go into a Spellstrike, although better spells exist for that.

It does nothing on a successful Fortitude save, so large and sturdy enemies ignore it. The light, fragile targets that are likely to fail are the ones he most wants to pull, which makes it a fair use of a low slot once his main spells are in higher ranks.""")

w('Kinetic Ram', """Kinetic Ram pushes enemies away from Cyrus, which is the opposite of what someone with a reach weapon and Reactive Strike usually wants. Its one-action version can free an ally from a grapple or clear a space, but Gravitational Pull is the more useful of the two spells.""")

w('Mending', """Mending repairs a broken non-magical object over ten minutes. A repair kit does the same, and Cyrus is trained in Crafting.""")

w('Mindlink', """Mindlink passes ten minutes of explanation to someone in a moment. It is occasionally handy for briefing a person silently or when time is short, but Message meets most of the same need as a cantrip.""")

w('Mud Pit', """Mud Pit creates difficult terrain over a good area with no save, which makes it reliable, but it does nothing more and it takes a full turn to cast. Entangling Flora and Web do more to the creatures caught in them.""")

w('Noxious Vapors', """Noxious Vapors surrounds Cyrus with a small poison cloud that harms allies as readily as enemies and hides everyone inside it from everyone else. The concealment hinders his side as much as it helps, and poison is widely resisted.""")

w('Penumbral Shroud', """Penumbral Shroud dims the light around one creature. It might help an ally who is sensitive to light or slightly hinder a sentry, but Cyrus has no regular use for it.""")

w('Pest Form', """Pest Form is one of the best scouting spells available to Cyrus. A rat or a sparrow goes unnoticed in places where an invisible intruder would be detected by scent or sound, and ten minutes is long enough to look round a building. From rank 4 the form can fly.

He cannot attack or cast while changed, and if he is caught he is alone and very small. The spell is valuable on days that call for reconnaissance, and since those can be anticipated, a scroll or wand is the right way to carry it.""")

w('Phantasmal Minion', """Phantasmal Minion summons a servant that fetches and carries. It takes a full turn to cast and an action each round to direct, and it has no use in a fight.""")

w('Shattering Gem', """Shattering Gem gives an ally an even chance of blocking one hit before the gem breaks. Two actions and a slot are a poor price for protection that fails half the time, particularly beside Hidebound or Warping Pull.""")

w('Shockwave', """Shockwave prepares a group of enemies for everyone who fights in melee. Those that fail the save fall prone, and those that succeed are still off-guard for a round, so every result short of a critical success gives Cyrus the extra damage Laughing Shadow adds against off-guard targets and makes his allies' Strikes easier to land. Through Expansive Spellstrike he can point the cone away from his own side.

It deals almost no damage, so the turn is spent for the benefit of the attacks that follow, and it is worth casting only when allies are in position to make them. It has no effect on creatures that are flying or otherwise off the ground. From level 4 it is a good use of a rank-1 slot.""")

w('Sleep', """Sleep is weak in a fight, because a sleeper wakes at the first loud noise or blow and the spell has the incapacitation trait. Its use is in quiet work, such as putting a sentry to sleep before an alarm can be raised, and a scroll covers that.""")

w('Snowball', """Snowball is an attack spell that also slows its target's movement. Its damage falls well behind that of Briny Bolt and Shocking Grasp as it is heightened, and the blindness from Briny Bolt is the stronger effect.""")

w('Spider Sting', """Spider Sting deals poison damage and weakens its target, but both depend on the target failing Fortitude saves over several rounds. Poison is widely resisted, so the full effect is rare, and Enfeeble weakens an enemy more reliably.""")

w('Summon Animal', """Summon Animal takes a full turn to cast and an action every round to maintain, and the creature it brings is too weak to threaten anything Cyrus is fighting. Summoning does not fit the way a magus needs to spend his actions.""")

w('Tether', """Tether keeps one enemy close. Someone running away, an enemy that keeps retreating out of reach or a spellcaster trying to back off is held within 30 feet with its Speed reduced, and on a critical failure it cannot move at all. That has clear uses for a fighter who wants enemies inside his reach.

It does nothing on a critical success and little on a success, and the tether can be cut. It is therefore a spell for the particular fights in which the enemy intends to stay away from him, and Tangle Vine offers a lighter version of the same effect as a cantrip.""")

w('Thoughtful Gift', """Thoughtful Gift sends a potion or scroll across the battlefield into an ally's hand for one action. Occasionally that saves a life, but usually the ally could have drawn an item of their own.""")

w('Ventriloquism', """Ventriloquism lets Cyrus throw his voice in support of a diversion or a bluff. That suits him in a small way as the one who does the talking, but Figment allows much the same as a cantrip.""")

w('Wall of Shrubs', """Wall of Shrubs provides light cover along a long line and improves in higher slots. It can shield his allies from archers or screen a withdrawal, but it takes a whole turn to cast, and the walls available at higher ranks do far more.""")

w('Propelling Air Stream', """Propelling Air Stream is an attack spell that also lifts Cyrus off the ground. Through a Spellstrike its damage is settled by the Strike's roll, and whether or not the Strike hits he can fly for a turn, which lets him reach an enemy on a ledge, cross a gap or pass over difficult ground. Its damage keeps up with Briny Bolt's.

The flight is brief and slow, and the spell does nothing to the target beyond damage, so on level ground Briny Bolt is the better choice. It is worth learning for fights that involve height during the levels before he can cast Fly.""")

# ───────────────────────── rank 2 ─────────────────────────
w('Acid Grip', """Acid Grip is the most dependable spell at this rank, because it accomplishes something on every result short of a critical success. Its damage is fair once the persistent acid is counted, but its value lies in the forced movement, which Cyrus directs: he can pull an enemy off a pinned ally, into a flank or out of a doorway, and the enemy then has to spend actions within his reach to get back. Strong enemies succeed at their saves more often than they fail, so a spell that still moves them on a success is worth far more than one that needs a failure.

The one case in which it is a poor choice is a lone enemy that is already where his allies want it, against which Sudden Bolt's damage serves better. In every other case it deserves a rank-2 slot, and it remains worth one at every level.""")

w('Invisibility', """Invisibility does two different things depending on the slot it is cast from. From a rank-2 slot it is for work outside a fight, such as scouting ahead, passing a guard post or getting one person out of a bad situation, and because it ends at the first hostile act it does nothing for his damage.

From a rank-4 slot it lasts through hostile acts, and it is then among the best spells Cyrus can cast as a fight begins. An enemy that cannot see him is off-guard to every Strike he makes, which gives him Laughing Shadow's extra damage without help from anyone, and every attack aimed at him must first find him. Enemies that sense without sight, or that can see invisible creatures, undo all of this. The rank-2 use is occasional enough to leave to a scroll or wand, while the rank-4 use is worth a slot until he gains Dimensional Disappearance at level 10.""")

w('Blazing Bolt', """Blazing Bolt deals fire damage at a fair rate for its rank, settled by the Strike's roll and doubled along with it on a critical hit. Through a Spellstrike it offers nothing more than that, and Briny Bolt heightened to the same slot matches the damage, adds a chance to blind and deals a type that is resisted far less often than fire.

Its one distinct use is the three-action casting, which sends rays at three enemies on a turn when Cyrus cannot reach melee, and such turns are rare for him. It is worth learning only if he needs a second damage type among his attack spells.""")

w('Telekinetic Maneuver', """Telekinetic Maneuver adds a Trip, a Shove or a Reposition to a Spellstrike. The manoeuvre is settled by the Strike's roll, so the target gets no save and Cyrus spends no separate action on Athletics. A tripped enemy is off-guard, which brings Laughing Shadow's extra damage, and from level 6 it provokes a Reactive Strike when it stands. Against one dangerous melee enemy, that can spoil two or three of its actions over a round.

The spell adds no damage, so it is a poor choice when the target simply needs to be killed, and it does little against an enemy that cannot be knocked down or moved. Dimensional Drop achieves the same prone result through a Reflex save even when the Strike misses, which leaves Telekinetic Maneuver as the better choice against agile enemies and whenever pushing an enemy is what the situation needs.""")

w('Sudden Bolt', """Sudden Bolt is the hardest single-target hit available at this rank, dealing roughly twice what the other spells of the rank manage. Because it is settled by a save, the target still takes half when it succeeds, whether or not the Strike lands. It has no added effect and no area, so its whole value is the Hit Points it removes from one enemy.

That makes it the right spell against a single tough target, and against slow or heavily armoured enemies with poor Reflex. It is poor value against a group, and agile enemies will often halve it. Acid Grip is useful in more fights, so Sudden Bolt is what Cyrus prepares when a day calls for damage and nothing else.""")

w('Acid Arrow', """Acid Arrow is adequate at the level it is learned and worse in every higher slot, because its damage grows only every second rank while Briny Bolt and Blazing Bolt grow with each rank. The persistent acid is a small addition that seldom lasts. Its damage type is the only thing in its favour, and Acid Grip already supplies acid with a far better effect.""")

w('Disintegrating Puddle', """Disintegrating Puddle is an attack spell whose value depends on where the target is standing. The hit itself is ordinary, but the acid it leaves around the target remains for the whole fight. At a doorway, on a bridge or in a corridor, every enemy that comes through is burned by it, and a magus holding such a place with a reach weapon is well positioned to take advantage.

On open ground it achieves little, since enemies simply walk out of the acid, and allies fighting beside the target stand in it too. Its short range also limits it when cast without a Strike. It is worth learning for days spent in confined spaces, and Briny Bolt is the better attack spell everywhere else.""")

w('Laughing Fit', """Laughing Fit is the best answer at this rank to an enemy whose reactions are the danger. Even a successful save stops it using reactions, which lets everyone move, cast and stand up around it freely, and a failure also costs it an action each round. Against one dangerous enemy that is a great deal to gain from a rank-2 slot.

The cost is that the spell must be sustained. Each round the action that maintains it is the action Cyrus would use to recharge his Spellstrike, so he keeps it going in place of his own damage, and it is worth doing when his allies gain more than he gives up. Mindless creatures and anything that is not alive ignore it completely. For those reasons he prepares it against a single threat he knows about, not as a matter of routine.""")

w('Stupefy', """Stupefy is aimed at spellcasters but has little effect unless the target fails its save outright, which a capable enemy often will not, and what it does on a success is over before it matters. Fear from a rank-1 slot hampers any kind of enemy, still works on a success and costs less.""")

w('Revealing Light', """Revealing Light solves a problem more than it wins a fight. It ends invisibility and concealment for everyone on his side at once, from long range, and nothing else at this rank does that. The dazzled condition it leaves is a useful extra, because it applies even on a successful save.

It deals no damage, so on a day without hidden enemies the slot is wasted, and Ignite Fireworks dazzles nearly as well while also hurting. That makes it a scroll to carry at all times and a spell to prepare only when unseen enemies are expected. Placed through Expansive Spellstrike, the burst dazzles allies next to the target as readily as enemies.""")

w('Noise Blast', """Noise Blast deals respectable area damage against Fortitude, but being deafened for a round changes little for most enemies. The stun on a critical failure is the valuable result, and strong enemies seldom fail that badly. Its burst suits Expansive Spellstrike when two or three enemies are close together and no ally stands beside the target, while its short range makes it awkward to cast without a Strike.

It is the weakest of the three Fortitude area spells at this rank. Spray of Salt deals a little more in a cone that is easier to keep away from allies, and Disorienting Flash matches its damage from twice the range with a more useful effect, so Noise Blast is worth having only when neither of those is available.""")

w('Dimensional Drop', """Dimensional Drop puts an enemy on the ground even when it succeeds at its save. Any fall that deals damage leaves a creature prone, so every result short of a critical success ends with the target off-guard and needing an action to stand, and from level 6 standing provokes a Reactive Strike. Through a Spellstrike this happens whether or not the Strike hits. The damage itself is slight and never improves.

It is the right spell against a single strong melee enemy, and it prepares that enemy well for his allies' attacks. It does nothing to a creature in the air, and one with a fly Speed can use its reaction to stop itself falling. Unrelenting Gravity needs a failed save for the same result, and Telekinetic Maneuver needs the Strike to hit.""")

w('Dispel Magic', """Dispel Magic cannot be replaced on the rare day it is needed and goes unused on all the others. When a fight depends on one enemy spell, whether a wall, a curse on an ally or an enhancement on the enemy, nothing else will remove it. Its chance of success depends on the slot it is cast from, so a rank-2 casting handles only weak magic, and the casting that matters would occupy one of his two highest slots, which he can seldom spare.

A scroll of the highest rank he can afford avoids that cost, since the answer is then at hand without reducing his damage for the day. A prepared slot makes sense only when he knows he will face enemy spellcasters.""")

w('See the Unseen', """See the Unseen lets Cyrus himself perceive invisible and incorporeal creatures, where Revealing Light exposes them to everyone. The creature remains concealed from him, so the spell helps without removing the problem, and it does nothing for allies who still cannot see the target.

Its value lies in how long it lasts. Ten minutes is enough for one wing of a dungeon, and from rank 5 it lasts most of a day, so a wand used each morning removes one way of being ambushed without taking a slot. As a prepared spell at low rank it is hard to justify when Revealing Light can be carried on a scroll.""")

w('Blur', """Blur is an ordinary defensive spell until level 7 and a very good one afterwards. Before then it costs two actions for a one-in-five chance that an attack misses, and Mirror Image gives better protection against the most dangerous enemies.

At level 7 it becomes one of his studious spells. It enters his spellbook without cost, and casting it lets him enter Arcane Cascade as a free action, so the two actions he would otherwise spend separately on his stance and on his defence become a single casting. From then on it is the natural first turn of any fight in which he expects to be attacked, and it can be placed on an ally who needs it more. That is reason enough to keep one prepared from level 7.""")

w('Mirror Image', """Mirror Image protects well against a few heavy hits and poorly against many light ones, because each attack that would have landed removes one image. Against a single hard-hitting enemy it usually absorbs two or three Strikes, which is more than any other defensive spell at this rank prevents.

It takes two actions and protects only Cyrus, so the time to cast it is the round before a fight begins, or an opening turn in which he cannot reach anyone. Cast in the middle of a fight, it costs him a Spellstrike. Blur gives less protection for longer and, from level 7, lets him enter Arcane Cascade without an action, and that is the point at which he stops preparing Mirror Image.""")

w('Resist Energy', """Resist Energy is very good when the damage type is known in advance and useless when it is not. Against an enemy that relies on one element it reduces every hit for a whole fight, and at higher ranks one casting covers several allies together.

Because it depends on that foreknowledge, it suits a scroll or wand better than a daily slot. Its ten-minute duration is long enough for it to be cast outside the door once the group knows what is behind it. A prepared slot is justified only on a day with a known elemental threat.""")

w("Loose Time's Arrow", """Loose Time's Arrow lets the whole group move quickly in a single round, and it does so from one rank-2 slot. It is for the first round of a fight spread over a large area, or an ambush in which everyone needs to close or get clear at once, and in that round it can be worth more than any damage spell Cyrus might have cast.

Outside that round it does nothing, and casting it costs him his own opening Spellstrike. Haste at rank 3 does far more for one person over a whole fight. The spell is worth a slot when his allies are slow to reach the enemy, and not otherwise.""")

w('Enlarge', """Enlarge increases damage and reach at a real cost. The extra reach widens the area in which Cyrus can make Reactive Strikes, and the damage bonus applies to every Strike. In exchange, the clumsy condition lowers his AC and Reflex, and a Large body is harder to fit into a flank or a corridor and harder to find space for when he teleports.

It usually does more for a melee ally who makes more Strikes each round than he does. Its five-minute duration allows it to be cast before a door is opened, which makes it a reasonable scroll or wand. In one of his own two rank-2 slots it is rarely better than a spell he can put into a Spellstrike.""")

w('Gecko Grip', """Gecko Grip lets Cyrus climb any surface for ten minutes without Athletics checks. It deals with walls, pits, ships' rigging and enemies shooting from a ledge, and it lets him fight from a surface where few melee enemies can follow him.

A spell this dependent on circumstances would normally be left to a scroll, but at level 7 it becomes one of his studious spells, which puts it in his spellbook without cost and lets him enter Arcane Cascade as a free action when he casts it. That makes it a sound opening action in any fight where height matters. He prepares it when he knows the ground ahead is steep or vertical, and leaves it in the spellbook on other days.""")

w('Water Breathing', """Water Breathing removes one problem completely, for the whole group, for hours. There is no reason to hold a daily slot for it, since a scroll can be bought when water is known to be ahead, and at higher ranks one casting lasts the day.""")

w('Blood Vendetta', """Blood Vendetta deals damage without using an action on his turn, which is attractive for a class as short of actions as the magus. Its persistent bleed damage is respectable for the slot, and the weakness it adds increases every slashing hit that follows, including his own.

The conditions are awkward, however. Cyrus must first be hit by the right type of damage, and the enemy then gets a save. From level 6 Reactive Strike is nearly always the better use of his reaction, and creatures that cannot bleed are unaffected. It is a reasonable choice for a low slot before level 6 and seldom worth one after.""")

w('Embed Message', """Embed Message is useful only away from a fight, as a warning, a signal or a message left behind. It is cheap and occasionally clever, but never worth a daily slot. Aspera's stave is planned to hold it, which would make it available to him at no cost.""")

w('Hidebound', """Hidebound is a reaction that reduces every Strike against one ally for a whole round. Cyrus casts it from a distance and it uses no action on his own turn. Against an enemy that attacks several times it prevents more damage in total than its small number suggests, and it improves acceptably in higher slots.

It costs his reaction and a slot. From level 6 the reaction is also wanted for Reactive Strike, so Hidebound is best in rounds when no enemy is likely to provoke one. It is not practical on a scroll or wand, because he would need the item in his hand at the moment of the attack. Warping Pull prevents more of one large hit and works against spells, whereas Hidebound is better against a series of attacks. From level 11, Axuma's Awakening can supply either of them without a slot.""")

w('Warping Pull', """Warping Pull is the stronger of his two protective reactions against a single large hit. It works against any source of damage, including spells and breath weapons, and the resistance it grants grows quickly in higher slots. The short teleport that comes with it matters as much as the resistance, because it can take an ally out of an enemy's reach before the next attack or move them into a flank.

It protects against one effect only, so Hidebound is better against an enemy that makes many attacks, and the ally must be within 30 feet. Like any spell cast as a reaction, it has to be weighed against Reactive Strike from level 6. A low-rank slot is an inexpensive place to keep it.""")

w('Propulsive Breeze', """Propulsive Breeze is a small reaction that brings a melee ally into reach one action sooner, which on a large battlefield can give them an extra Strike in the first round. It only lengthens a move in a straight line, and from level 6 it costs Cyrus his Reactive Strike for the round, so it is a minor option for a spare low slot.""")

w('Pyrefowl Rebuke', """Pyrefowl Rebuke works against the way Cyrus fights. Its damage is negligible, and the movement it grants carries him away from an enemy he wants inside his reach. A reaction spent on it is one he cannot spend on Reactive Strike or on protecting an ally.""")

w('Animated Assault', """Animated Assault deals ordinary area damage in the first round and more only if it is sustained. Each round of sustaining takes the action Cyrus needs to recharge his Spellstrike, so in practice he gets the first round of damage and little else. Ignite Fireworks and Vomit Swarm give more for the same slot.""")

w('Ash Cloud', """Ash Cloud takes a whole turn to cast and returns a small amount of damage each round and some hindrance to flying creatures. Its three actions rule out a Spellstrike, and the cloud troubles allies who enter it as much as enemies. It is worth considering only to hold back a group of flying creatures, and better spells do that at higher ranks.""")

w('Charitable Urge', """Charitable Urge is unusually strong for its rank when it works. Even a successful save costs the enemy an action, with nothing to sustain, and a failure wastes most of its next turn. Against low-level enemies holding weapons or other items it controls a target better than Laughing Fit.

The difficulty is the incapacitation trait. From a rank-2 slot, any enemy above level 4 treats its save as one step better, so the dangerous targets, which are the ones worth controlling, are barely affected. It also does nothing to a creature that carries nothing. That limits it to levels 3 and 4, unless Cyrus heightens it into slots he needs for other spells.""")

w('Darkness', """Darkness blinds Cyrus as surely as it blinds the enemy, because he has no darkvision, and it takes a full turn to cast. Its one use for him is to cover a retreat. A group in which everyone could see in the dark might build tactics on it, but he could not take part in them.""")

w('Darkvision', """Darkvision is a necessity on some days and makes no difference on others. As a human, Cyrus has no way of seeing in darkness, and fighting by torchlight gives away his position and puts him at a disadvantage against anything that sees him first.

It lasts an hour, and a full day from higher slots, so a wand used once each morning suits it well. Until he owns one, a scroll in his pack covers a cave he did not expect. A prepared slot makes sense only for a day he knows will be spent underground or at night.""")

w('Deafness', """Deafness inconveniences an enemy without stopping it doing anything that matters in most fights. A single-target spell whose best result is so slight is a poor use of any slot.""")

w('Entangling Flora', """Entangling Flora slows a group for a whole fight without needing to be sustained, which is rare at this rank. It is at its best when it divides an encounter, so that half the enemies struggle through it while his allies deal with the rest and Cyrus holds the near edge with his reach.

It needs plants or soil underfoot, so it fails on stone floors, and its area is far too large to place on a melee through Expansive Spellstrike without covering his own side. He therefore casts it without a Strike in the first round. Web holds each creature more firmly in a smaller space but takes three actions.""")

w('Environmental Endurance', """Environmental Endurance protects against heat or cold for a whole day. That matters on an expedition and nowhere else, and a scroll or wand provides it without using his daily slots.""")

w('Exploding Earth', """Exploding Earth deals damage on an attack roll with a little splash and a chance of knocking the target prone on a critical hit. It improves at half the rate of Briny Bolt, and the splash falls on allies standing beside the target, which is where his allies usually are. Cyrus has no reason to learn it.""")

w('False Vitality', """False Vitality gives Cyrus temporary Hit Points that last a working day and cost no action in a fight. They absorb the first hits of the first encounter and are then gone, and the spell works only on him.

Its long duration makes it a spell for a wand, used at breakfast for extra durability every day. In a slot it would displace spells that decide fights, and it is not worth that.""")

w('Floating Flame', """Floating Flame deals its damage only if it is sustained and moved every round, and that takes the action Cyrus needs to recharge his Spellstrike. A caster with actions to spare can make it worthwhile over a long fight, but he cannot.""")

w('Heat Metal', """Heat Metal is excellent against the right target and useless against the wrong one. On an enemy in metal armour the persistent fire keeps burning with no easy way to stop it, and over a few rounds the total exceeds any other spell at this rank. On an enemy holding a metal weapon it forces a choice between dropping the weapon and being burned.

Against anything without metal it does nothing at all, so Cyrus cannot prepare it as a matter of course. It is worth learning and then preparing when the day's enemies are known to wear armour, with Sudden Bolt as the safer general choice.""")

w('Humanoid Form', """Humanoid Form is a disguise that survives casual inspection and gives a bonus to pass as someone else. Because Cyrus does much of the talking for his allies, it has real uses in infiltration, though none in a fight, and a scroll is the right way to carry it.""")

w('Illusory Creature', """In a fight, Illusory Creature needs an action every round that Cyrus must give to his Spellstrike, and the illusion disappears at the first hit. Outside a fight it makes a convincing decoy, distraction or lure, and that second use is worth a scroll though not a slot.""")

w('Knock', """Knock gets Cyrus past a lock when none of his allies is skilled with one. The bonus is large, and he can attempt the check himself as part of the casting. Since there is no telling when a lock will appear, the spell is best kept on a scroll.""")

w('Lucky Number', """Lucky Number gives a one-in-twenty chance, once a day, to reroll a d20 that happened to show the chosen number. The odds that this falls on a roll that matters are small. It is acceptable from a wand, where it costs nothing, and not worth a slot.""")

w('Mist', """Mist conceals both sides equally and takes a whole turn to cast. It can blunt enemy archers or cover a withdrawal, but it also hides the enemy from his own allies, so it is rarely the best use of three actions.""")

w('Oaken Resilience', """Oaken Resilience grants a very small resistance at the price of a larger weakness to fire. That is a bad exchange even before the slot is counted.""")

w('Phantasmal Treasure', """Phantasmal Treasure takes one enemy out of a fight only for as long as everyone leaves it alone, and the target gets repeated chances to see through the illusion. On a successful save it does almost nothing, which makes it too unreliable to plan around.""")

w('Shrink', """Shrink is for fitting someone through a gap or hiding them. Cast on Cyrus himself it removes his reach, on which his whole way of fighting depends.""")

w('Splinter Volley', """Splinter Volley deals damage at the same rate as Briny Bolt, in a different physical type and with no added effect. Its option of a second target for a third action cannot be used through a Spellstrike. Briny Bolt should be learned first, and this adds nothing to it.""")

w('Sticky Fire', """Sticky Fire deals low damage and applies a minor penalty that lasts only until a flat check puts the fire out. Because it improves only every second rank, it starts behind the alternatives and falls further behind in every higher slot.""")

w('Summon Elemental', """Summon Elemental takes three actions to cast and one every round afterwards, which leaves no room for a Spellstrike and its recharge, and a creature summoned from a low slot contributes little. Summoning does not fit the way a magus spends his turn.""")

w('Translate', """When no one shares a language, Translate is the only way to talk or read at all, and for the one who negotiates on the group's behalf that can decide an encounter. It still belongs on a scroll or wand, because the need is occasional and never so urgent that a moment's delay matters.""")

w('Vomit Swarm', """Vomit Swarm deals solid area damage against Reflex in a cone, which is the easiest shape to use through Expansive Spellstrike, because Cyrus can point it away from his allies and catch whatever stands behind his target. Its sickened condition is the strongest penalty among the rank-2 area spells, lowering the attacks, saves and AC of everything that fails for as long as it lasts.

That condition needs a failed save, which is far from certain against capable enemies. Ignite Fireworks deals the same damage and dazzles even on a success, so it is the more dependable of the two, while Vomit Swarm is better against crowds of weak enemies that will fail often.""")

w('Water Walk', """Water Walk solves a crossing for ten minutes. A scroll bought when a river or harbour lies ahead is all it needs.""")

w('Web', """Web is the firmest area control at this rank, and its cost is a full turn with no Strike. At a doorway or in a corridor it can hold a group in place for most of a fight, which is worth the turn, but in the open enemies walk round it or burn it away.

Entangling Flora covers more ground for two actions wherever plants grow. For Cyrus, Web is a first-round spell for a position he has had time to choose, and has little use beyond that.""")

w('Marvelous Mount', """Marvelous Mount makes travel more convenient for one person. It has no bearing on a fight and is rarely better than hiring a horse.""")

w('Blazing Armory', """Blazing Armory equips someone with a weapon they did not bring. Cyrus fights with his own weapon in both hands, and any ally who needs a weapon already carries one.""")

w('Binding Muzzle', """Binding Muzzle is a narrow answer to creatures that depend on a bite or a breath weapon. Against those it is strong, because even a successful save closes the mouth for a round, and it works at long range. Against anything that fights with weapons or claws, or with spells cast without speech, it does nothing, so it is a scroll to carry when such an enemy is expected.""")

w('Spray of Salt', """Spray of Salt is the hardest-hitting Fortitude area spell at this rank, and its short cone is easy to direct away from allies through Expansive Spellstrike. Against ordinary enemies it has no added effect, so what it offers is damage against a save that slow, heavily armoured enemies tend to pass and that spellcasters and lightly built enemies tend to fail.

The cone is small and will rarely reach more than two or three enemies, and acid is a damage type his other spells already supply. It is the better choice than Disorienting Flash when the slot is wanted purely for damage, and Disorienting Flash is the better choice when flexibility matters more.""")

w('Blood Runs Cold', """Blood Runs Cold is a Fortitude spell that takes an action from a single enemy if it fails its save. Against one strong enemy a lost action is worth more than the small damage that accompanies it, and on a critical failure the persistent cold damage keeps the target slowed for longer.

A successful save reduces the spell to a few points of damage, and against a strong enemy that is the usual result. Slow at rank 3 costs its target an action even on a success, so Blood Runs Cold is a temporary measure for levels 3 and 4 against enemies with poor Fortitude and has little use afterwards.""")

w('Unrelenting Gravity', """Unrelenting Gravity is valuable chiefly for what it does on a successful save, which is to leave the target slower and easier to hit for a round. Knocking the target prone, its main effect, needs a failed save. Dimensional Drop leaves an enemy on the ground prone even when it succeeds, so that is the better spell for the purpose in most fights.

Unrelenting Gravity is worth considering against flying creatures, which it brings down on a failure, and against enemies whose Fortitude is clearly worse than their Reflex. From a rank-4 slot it affects five targets, which makes it a considerably better spell.""")

w('Disorienting Flash', """Disorienting Flash offers three sizes of Fortitude area damage from one prepared slot, which matters to someone with only two slots at each rank. The two-action burst is the version Cyrus puts into a Spellstrike. The one-action version fits a turn in which he has already made his Spellstrike, and the three-action version reaches a group he cannot get to in melee. The dazzled condition is worth having as well, because it gives each of an enemy's attacks a chance to miss.

A burst is harder to keep away from allies than a cone, the dazzled condition needs a failed save, and the damage is slightly below Spray of Salt's. Its flexibility makes it the better preparation on a day when he does not know what form the fights will take.""")

w('Ignite Fireworks', """Ignite Fireworks is the most dependable of the rank-2 area spells at hindering enemies, because it dazzles them even on a successful save. Strong enemies usually succeed, so that is the result Cyrus should expect, and a round in which several enemies each risk missing is worth more than the light damage. On a failure they stay dazzled for most of a fight.

The burst needs care through Expansive Spellstrike when allies stand beside the target, since they are dazzled too, and it is one more Reflex spell among the many he already has. Vomit Swarm matches the damage and imposes a stronger condition that needs a failed save, which leaves Ignite Fireworks as the safer choice against tough enemies.""")

# ───────────────────────── rank 3 ─────────────────────────
w('Haste', """Haste is the best enhancement Cyrus can cast, whether on himself or on an ally. A magus is always one action short, because a Stride, a Spellstrike and a recharge do not fit into three actions. The extra Stride or Strike that Haste grants each round removes that shortage for a whole fight, so he can close with an enemy and Spellstrike in the same turn, or Spellstrike and still make a second Strike.

It takes two actions to cast, so it is a first-round spell, ideally cast while the enemy is still out of reach. From level 11 it is one of his studious spells and lets him enter Arcane Cascade as a free action, which removes most of that cost. On a melee ally who attacks more often than he does it can be worth even more, and it deserves a slot from the level at which he gains rank-3 spells.""")

w('Slow', """Slow is the strongest spell Cyrus has for hindering a single enemy, because it works even when the target succeeds at its save. An action lost for a round is a third of an enemy's turn, and that is the least the spell does, since a failure costs the enemy an action every round for the whole fight. Through a Spellstrike this comes on top of a Strike, with nothing to sustain and without the incapacitation trait.

It targets Fortitude, which is usually the best save of large and dangerous enemies, so failures will be uncommon against the very targets he most wants to slow. The effect on a success is still worth the slot. Against a group it becomes worthwhile at rank 6, when it affects ten targets. He keeps one prepared on any day that holds a serious single enemy.""")

w('Time Jump', """Time Jump gives Cyrus two moves for one action, and nothing can react to them. It takes him out of an encirclement, past a line of defenders to the spellcaster behind it, or up to a target with two actions still in hand for a Spellstrike, and enemies' Reactive Strikes do not apply.

Dimensional Assault already gives him a teleport and a Strike from his Focus Points, so Time Jump is a second answer to the same need, for fights in which one such move is not enough or the distance is too great. That makes it a slot well spent on large or crowded battlefields and an indulgence on small ones.""")

w('Lightning Bolt', """Lightning Bolt is his main line spell and one of the best spells he has. Its damage is high and grows with every rank, and a line is the easiest area to keep away from allies through Expansive Spellstrike, because it begins beside the target and runs away from his own side through whatever stands behind. Even with a single enemy in the line it is strong damage against Reflex.

From level 12 it is the natural spell for Sprinting Spellstrike, which carries Cyrus along its length. It has no added effect, and electricity is occasionally resisted. He prepares it from level 5 and goes on casting it from higher slots.""")

w('Fireball', """Fireball is excellent for a caster who stands back and awkward for Cyrus. Its damage and its very long range are as good as ever when he casts it without a Strike at a group across the battlefield, which is a fair use of a turn before the two sides meet.

Through a Spellstrike it is a problem, because a 20-foot burst centred beside his target covers him and any ally nearby, so he can rarely afford to use it that way. Lightning Bolt and Crashing Wave deal similar damage in shapes he can direct. Fireball is worth learning for the long-range casting if he has a spare place in his spellbook, but his turns should not depend on it.""")

w('Cave Fangs', """Cave Fangs deals Fireball's damage as piercing and leaves difficult terrain behind for the rest of the fight. Physical damage avoids the resistances that so often reduce fire, and the terrain slows enemies who must cross it to reach his allies.

It shares Fireball's fault in a Spellstrike, since the burst is too large to place around his own position, and its range is much shorter. Cast without a Strike in the first round, at a group that has to come through the area, it is a strong opening. In other circumstances his cones and lines serve him better.""")

w('Blindness', """Blindness is crippling when it takes hold and makes little difference when it does not. An enemy blinded for a minute is effectively out of the fight, but a successful save reduces that to a moment, and the incapacitation trait gives strong enemies a better result still.

It is therefore a spell for enemies at or below his level with poor Fortitude, such as spellcasters, and against those it is among the best available. Against a single powerful enemy Slow is far more dependable, and Briny Bolt offers a round of blindness on a hit with no save at all.""")

w('Paralyze', """Paralyze is very strong against an enemy of his level or lower. Even a successful save costs the target an action, and a failure leaves it helpless for a round, off-guard and exposed to critical hits from everyone.

The incapacitation trait limits it. Anything above his level treats its save as one step better, so the spell mostly fails against the enemies he most wants stopped. It is also a mental effect, to which mindless creatures are immune. Cyrus prepares it for fights against several dangerous enemies of his own level and uses Slow against a single greater threat.""")

w('Blister Bomb', """Blister Bomb weakens enemies severely even when they succeed at their saves. Sickened 2 on a success is a heavy penalty to everything the target rolls, and it applies to every creature in a small burst that is easy to place through Expansive Spellstrike without touching allies. Until the enemies spend actions recovering, everyone on his side hits more often and is hit less.

It deals no immediate damage, so its benefit comes over the course of a longer fight, and creatures immune to disease ignore it. Against two or three tough living enemies it is one of the best uses of a rank-3 slot.""")

w('Earthbind', """Earthbind is a direct answer to a flying enemy, which Cyrus otherwise struggles to reach, and even a successful save brings the creature down for a moment. It has no other use, so the place for it is a scroll kept for the day a flying enemy appears.""")

w('Magnetic Acceleration', """Magnetic Acceleration deals damage on an attack roll at the same rate as Briny Bolt, divided between two physical types, with nothing added. Its accuracy bonus against metal applies to the spell's own attack roll, so it is unlikely to help in a Spellstrike.

Its long range makes it a respectable spell for a turn when Cyrus cannot reach melee. In a Spellstrike, Briny Bolt deals the same damage and blinds as well, so Magnetic Acceleration is worth learning only for use at range.""")

w('Widow’s Bite', """Widow's Bite is the only worthwhile Spellstrike spell that lacks the manipulate trait. Casting it does not provoke a Reactive Strike and cannot fail the flat check required of a grabbed caster, so it is the spell for a turn when a large enemy with reach, or one that has hold of him, makes any other spell risky. Its effect suits those same enemies: the target is enfeebled for as long as the poison lasts, which is decided by the Strike's roll without a save, and the persistent damage continues while he recharges.

Poison is the most commonly resisted damage type and many creatures are immune to it, in which case the enfeebled condition is lost as well, and the spell improves only every second rank. Cyrus prepares it against strong living enemies that fight in melee, and Briny Bolt is safer against an enemy he knows nothing about.""")

w("Eagle's Cry", """Eagle's Cry damages and frightens in a single casting, and the fear applies even on a successful save. Every enemy in the cone is worse at attacking and defending for at least a round, in addition to taking respectable sonic damage, and a cone is easy to direct through Expansive Spellstrike.

It targets Fortitude, so large enemies will often take only half damage, but they are still frightened. The fear does not grow stronger in higher slots. In a fight against a group, this is among the best rank-3 spells.""")

w('Wooden Double', """Wooden Double protects Cyrus at the worst moment of a fight. He decides to use it after a critical hit has been rolled against him, so the reaction is never wasted on an ordinary blow, and it turns a doubled hit from a powerful enemy into damage to a block of wood.

It takes his reaction away from Reactive Strike only in the rounds in which he is critically hit, and in those rounds surviving matters more. One low or middle slot kept for it is good value in any fight against an enemy above his level.""")

w('Ghostly Weapon', """Ghostly Weapon decides whether Cyrus can contribute against incorporeal enemies. Without the ghost touch property his weapon deals a fraction of its damage to them, and with it he fights normally for a whole encounter.

So narrow a spell would normally be left to a scroll. From level 11, however, it is one of his studious spells, which puts it in his spellbook without cost and lets him enter Arcane Cascade as a free action when he casts it, so on the right day it makes a good opening action. He carries a scroll until then and prepares the spell when incorporeal enemies are expected.""")

w("Cloud Dragon's Cloak", """Cloud Dragon's Cloak is a reaction that gives an ally an even chance of avoiding a ranged attack, and every other ranged attack that round. Against archers or spell attacks concentrated on one ally, that prevents a great deal of damage for a single reaction.

It does nothing against melee attacks, and it uses the reaction he would otherwise keep for Reactive Strike. It is best on days when the enemy fights at range and nothing is likely to provoke him in any case.""")

w('Shadow Projectile', """Shadow Projectile is a reaction that adds damage and accuracy to an ally's ranged attack. With allies who are archers, or casters who use spell attacks, it turns a reaction he was not using into some damage and a penalty for the target.

It works once against each enemy and needs the ally to be close. From level 6 Reactive Strike is the better regular use of his reaction, so this is a minor option for a spare slot.""")

w('Agonizing Despair', """Agonizing Despair deals damage and frightens its target through a Will save, and the fear applies even on a success. Through a Spellstrike it adds a modest amount of damage to the Strike and leaves the target frightened for his allies' next attacks, and it keeps improving in higher slots.

It gives Cyrus a Will spell that is not wasted when the enemy succeeds, which he otherwise lacks. Mindless creatures and anything immune to fear or mental effects ignore it. Fear provides the condition alone from a rank-1 slot, so Agonizing Despair is for the occasions when he wants the damage as well.""")

w('Aqueous Orb', """Aqueous Orb is a rolling sphere that can engulf enemies, and it has to be sustained each round to move. That is the action Cyrus needs for recharging, and the orb achieves little unless it is moved every turn.""")

w('Clairaudience', """Clairaudience lets Cyrus listen through walls from a distance for ten minutes. For a group that plans its approach, it can reveal numbers, passwords or intentions before a door is opened. It takes a minute to cast and belongs on a scroll.""")

w('Cozy Cabin', """Cozy Cabin provides shelter for a night in the wild. It is comfortable but has no bearing on a fight, and a tent does most of the same work.""")

w('Crashing Wave', """Crashing Wave deals Fireball's damage in a cone, in a damage type that almost nothing resists. The shape is what matters to Cyrus, because through Expansive Spellstrike a 30-foot cone begins beside his target and spreads away from his own side, which makes it the area spell he can use most freely in a melee.

It has no added effect. Lightning Bolt deals more to a single target and later suits Sprinting Spellstrike, whereas Crashing Wave reaches more enemies when they stand in a group, so the two are worth learning together.""")

w('Curse of Lost Time', """Curse of Lost Time makes a living target both easier to hit and weaker in its own attacks, with a brief version of the effect on a successful save. The clumsy condition also lowers the Reflex DC against which Cyrus rolls a Trip. Against constructs and objects it deals damage instead, which gives it an unusual second use.

The lasting effect needs a failed Fortitude save, and the effect on a success is over within a round. Fear and Blister Bomb impose more dependable penalties, so this is a reasonable choice against constructs and of little value otherwise.""")

w("Day's Weight", """Day's Weight lowers a living enemy's AC, saves, attacks and damage together from long range, and gives a round of that even on a successful save. On a failure it lasts for the fight. Everyone on his side benefits from the lower AC and saves, and those in melee from the weaker attacks.

It deals no damage and targets Fortitude, which strong enemies usually pass. Slow takes more from a single enemy for the same slot. Day's Weight is the better opening when his allies are about to cast spells of their own at the target, and from a rank-6 slot it affects a whole group.""")

w('Dive and Breach', """Dive and Breach combines movement with area damage. Cyrus leaves one group, appears beside another and damages creatures at both ends, with an action left over, which is an attractive turn when two clusters of enemies are within range.

In a Spellstrike he Strikes first and then dives, and only the creature he struck takes the damage, which is modest for the slot. Echo Jump does the same thing with force damage and without the Leap, so Dive and Breach is the second choice of the two, although it moves him further and gains a die with every rank.""")

w('Dream Message', """Dream Message sends a one-way message to anyone Cyrus has met, wherever they are. It is useful for reports, warnings and requests between adventures and is never urgent, so a scroll or wand is enough.""")

w('Elemental Absorption', """Elemental Absorption gives a minute of resistance to one element along with a counterattack. The resistance is small, and releasing the counterattack costs two actions that Cyrus would sooner spend on a Spellstrike. Resist Energy protects better and for longer.""")

w('Enthrall', """Enthrall holds a crowd's attention for as long as Cyrus keeps talking, which can cover an ally's movements or gain time. It suits someone who does the talking, but it has to be sustained and does nothing to anyone already hostile, so an occasional scroll is the most it justifies.""")

w('Gravity Well', """Gravity Well prepares enemies for area damage. It drags everything in a wide burst towards one point, which gathers them for a Lightning Bolt, a Crashing Wave or an ally's area spell, and it can pull them off a ledge or out of cover.

It deals no damage itself, it moves enemies far only when they fail Reflex saves, and it costs Cyrus a turn without a Strike. It repays that when his allies have area spells ready to follow it, and seldom otherwise.""")

w('Hypnotize', """Hypnotize creates a cloud that dazzles whatever is inside it and can hold weaker enemies fascinated. The dazzled condition allows no save, which is useful. Keeping the cloud in place takes an action every round, however, and fascination ends when anyone attacks the creature, so the spell is of more use against guards than in a fight to the death.""")

w('Impending Doom', """Impending Doom is a curse on one living enemy that builds over three rounds, making it off-guard, then frightened, and on a failed save stunned and damaged at the end. Part of that happens even on a successful save, and the off-guard condition gives Cyrus Laughing Shadow's extra damage from the first round.

Three rounds is longer than many fights last, and the incapacitation trait weakens the spell against strong enemies. It is best cast early against a durable enemy of his own level. Mindless creatures are immune.""")

w('Levitate', """Levitate moves one creature or object slowly up or down. It can cross a pit or lift someone to a ledge, but the penalty to attacks while floating makes it useless in a fight, and Gecko Grip and later Fly do the same work better.""")

w('Locate', """Locate points the way to a particular object, and from a higher slot to a particular creature. When something has been stolen or someone has gone missing, it can save a day of searching. The need is occasional, so a scroll is enough.""")

w('Mind Reading', """Mind Reading is useful to Cyrus as the group's negotiator. A glimpse of surface thoughts during an interrogation or a tense bargain can expose a lie or show what the other side wants, and no skill check gives that information so directly.

It needs the target to fail a Will save, and a target that succeeds may realise what was attempted, which has consequences in polite company. It is best kept on a scroll for the one conversation that matters.""")

w('Organsight', """Organsight adds precision damage to his next piercing or slashing hit, in return for a Recall Knowledge check each round. Cyrus identifies enemies anyway, so the check is one he is good at, and the damage applies to a Spellstrike.

The spell takes two actions to cast and one each round to renew, and a magus has none to spare. The return is too small for that price, except in a long fight against a single enemy.""")

w('Phantom Prison', """Phantom Prison takes one enemy out of a fight for as long as everyone leaves it alone, which against a group lets his side concentrate on the rest. That is powerful while it holds.

It takes a full turn to cast, has the incapacitation trait, depends on a failed Will save, and weakens each time the target tests the walls or is attacked. Those are too many ways to fail for someone who gives up a Spellstrike in order to cast it.""")

w('Safe Passage', """Safe Passage protects the group while it crosses one stretch of dangerous ground. It answers that particular hazard and nothing else, so a scroll is appropriate when the route is known to need it.""")

w('Shared Invisibility', """Shared Invisibility is the best way to move the whole group unseen. Ten minutes of invisibility for six people is enough to pass a guarded gate, cross open ground or set an ambush, and the first round of that ambush is worth a great deal when every enemy is off-guard.

Everyone has to stay close to Cyrus, and the first hostile act ends the spell for all of them, so it does not last into the fight itself. Because it supports a plan made in advance, a scroll can be bought for the occasion, and a slot is justified on a day devoted to infiltration.""")

w('Stinking Cloud', """Stinking Cloud can decide a fight against a group. Enemies that remain in the cloud are sickened, and those that fail their saves are slowed as well, which takes an action from each of them every round. The concealment it provides also protects his allies from archers on the far side.

The cloud affects allies in the same way, so Cyrus has to cast it without a Strike onto the enemy's side of the field, and it is far too large for Expansive Spellstrike. Immunity to poison makes it useless against many creatures that are not alive. On the right day it is a strong opening spell.""")

w('Tempest Cloak', """Tempest Cloak protects one ally from arrows and surrounds them with a ring of difficult terrain. It can keep a spellcaster safer from archers and from enemies trying to close, but it costs two actions and does nothing for Cyrus himself.""")

w('Vampiric Feast', """Vampiric Feast deals solid damage and returns part of it to Cyrus as temporary Hit Points. Through a Spellstrike its touch range extends to his reach, and it is the only spell that leaves him harder to kill after he has cast it. Because the save is a basic one, he still gets half the damage and half the temporary Hit Points when the target succeeds.

It works only on living creatures and targets Fortitude, the save that tough enemies pass most often, although void damage is rarely resisted by the living. It is a good spell for a fight in which he expects to be hit.""")

w('Wall of Thorns', """Wall of Thorns is a long barrier that hurts whatever pushes through it and gives cover across it. It can divide an encounter in two for a minute, which is a strong effect for the rank.

It takes a whole turn to cast, and determined enemies can cut a gap in a round or two. It suits a group that wants to fight half the enemy at a time and a caster with turns to spare, and Cyrus is not such a caster.""")

w('Wall of Water', """Wall of Water slows anything crossing it and hampers fire and ranged attacks that pass through, but it stops very little outright. Wall of Thorns is the better wall for the same turn.""")

w('Wall of Wind', """Wall of Wind gives almost complete protection from arrows and bolts for a minute and is a real obstacle to flying creatures. Against an ambush by archers it protects all of his allies at once.

It takes a full turn to cast and does nothing against melee attacks or spells, so it is best kept as a scroll for a fight that opens with a volley.""")

w('Warding Aggression', """Warding Aggression gives a small bonus to AC against one enemy, and only for as long as Cyrus keeps hitting it. It takes the place of a Spellstrike on the turn it is cast and protects him less than Shield does for one action.""")

w('Temporal Twin', """Temporal Twin lets an ally repeat one action from a place Cyrus chooses. On a hard-hitting ally that amounts to one extra Strike for two of his actions and a rank-3 slot, which is a poor exchange beside Haste.""")

w('Oneiric Mire', """Oneiric Mire has the effect of Entangling Flora but tests Will instead of Reflex, which helps against agile enemies. It needs a whole turn and failed saves, and difficult terrain alone is a modest return for that price.""")

w('Veil of Privacy', """Veil of Privacy protects against scrying and detection for eight hours. It matters only when the group knows it is being watched by magic, which is a rare problem to have.""")

w('Coral Scourge', """Coral Scourge slowly builds a penalty to one enemy's AC and Reflex, but it needs repeated failed saves and has the incapacitation trait. That makes it too unreliable, particularly when Fear gives a similar benefit at once.""")

w('Glass Sand', """Glass Sand is a very long cone of slashing damage with a little bleeding. Through Expansive Spellstrike its 60 feet can cover an entire group behind his target, where Crashing Wave reaches only 30.

Its damage is lower than Crashing Wave's, and slashing is resisted more often than bludgeoning. Glass Sand is therefore the better spell against large, deep formations on open ground, and Crashing Wave is better in rooms of ordinary size.""")

w('Magical Fetters', """Magical Fetters imposes a heavy penalty on one enemy's AC, Reflex and Speed for the whole fight if it fails its save, and a mild version for a round if it succeeds. Against an enemy of his own level, the full effect makes every attack on it far more likely to hit and to hit critically.

Because of the incapacitation trait it rarely takes hold on anything stronger than Cyrus. It is a spell for equal or weaker enemies with poor Reflex, against which it can be excellent.""")

w('Radiant Globe', """Radiant Globe creates a dome that destroys arrows passing through it. After a whole turn to cast, it protects a small area from archers for as long as Cyrus spends an action on it each round. Wall of Wind does more and needs no upkeep.""")

w('Disruptive Transfer', """Disruptive Transfer teleports Cyrus as far as his Speed and dazzles whoever was next to him. With Laughing Shadow's Speed that is a good distance, and the movement provokes nothing. Dimensional Assault already moves him in the same way with a Strike included, so the slot is hard to justify.""")

w('Percussive Impact', """Percussive Impact deals damage on an attack roll that starts below Briny Bolt's and catches up only in his highest slots, because it grows every second rank. Sonic and bludgeoning damage are both seldom resisted. It is an option for the highest levels at most, and nothing recommends it before then.""")

w('Trade Items', """Trade Items exchanges a small item in his hand for one that an enemy holds or carries, from up to 60 feet, unless the enemy succeeds at a Reflex save. Aimed at a wand, a key, a potion or the object the enemy is guarding, it removes the one thing on which a fight or a theft depends, and in a Spellstrike it follows a hit on the same target.

Cyrus must be holding something of light Bulk to give in exchange, most weapons are too heavy to take before rank 5, and a successful save wastes the casting. It is a scroll for the day when a single object matters.""")

w('Roaring Applause', """Roaring Applause suits someone with Reactive Strike particularly well. Even on a successful save, the target cannot use reactions for as long as Cyrus sustains the spell, which leaves everyone free to move and cast around it. On a failure it also loses an action each round, and its applause provokes his Reactive Strike at the start of each of its turns.

Sustaining the spell takes the action he would use to recharge, so he gives up some of his own damage in return for a hindered enemy and additional attacks. Against one dangerous enemy, from level 6, that exchange is worth making. Mindless creatures are immune, and the target has to be able to perceive him.""")

w('Gravity Wave', """Gravity Wave deals damage and knocks enemies down across a cone. Every enemy that fails is prone, which leaves it off-guard to Cyrus and to his allies in melee, and it must spend an action standing up where his Reactive Strike can punish it. The cone is easy to direct through Expansive Spellstrike.

The spell depends on failed Fortitude saves, which large enemies often avoid, and its damage is a step below Crashing Wave's. Against groups of ordinary enemies it is one of his best spells at this rank, while Dimensional Drop is the more certain way to put one sturdy enemy on the ground.""")

w('Skyglass Prison', """Skyglass Prison holds an enemy in place even when it succeeds at its save. A target that cannot move for a round cannot reach his allies' spellcasters and cannot withdraw from his reach, and on a failure it must spend actions breaking out. For a fighter who wants an enemy kept where he can hit it, that is ideal.

It does not stop the enemy attacking whoever is adjacent, and it targets Fortitude. It is best used on a mobile enemy, an archer or something trying to flee.""")

w('Lightning Lasso', """Lightning Lasso deals damage and holds the target if it fails its save. Keeping the hold takes an action each round, the same action Cyrus needs for recharging, and the enemy can simply Escape. Skyglass Prison holds an enemy without upkeep and does so even on a successful save.""")

w('Rend Magic', """Rend Magic is a spell for use against spellcasters. Its initial force damage is a little under what is usual for the rank and is settled by the Strike's roll, and afterwards the target is hurt every time it casts a spell, which punishes the kind of enemy Cyrus most wants to put under pressure. Force damage is almost never resisted.

Against anything that does not cast spells it is plain damage and ends at once. He prepares it when enemy spellcasters are expected, and Briny Bolt offers more on other days.""")

w('Tricks and Treats', """Tricks and Treats is a burst around Cyrus that makes enemies clumsy even on a successful save and removes their reactions on a failure. It is most useful when he is surrounded, since removing reactions lets him and his allies move freely.

Its better effect needs failed Will saves, it does nothing to enemies that carry no valuables, and in a Spellstrike it affects only the creature he strikes. It is an oddity that he will rarely have reason to prepare.""")

# ───────────────────────── rank 4 ─────────────────────────
w('Fly', """Fly answers most problems of height and terrain, and it is the only way Cyrus can fight a flying enemy with his weapon instead of throwing cantrips from the ground. Five minutes is long enough for a whole encounter, and cast on a melee ally it solves the same problem for them.

Before level 13 it costs two actions he would sooner spend attacking, so it is best cast before the fight when the need can be seen coming. At 13 it becomes one of his studious spells and lets him enter Arcane Cascade as a free action, which makes it a good opening action wherever a battlefield has height. Until he can spare the slot, a scroll keeps it available.""")

w('Translocate', """Translocate is a long teleport that needs no path and provokes nothing. In one casting it gets Cyrus out of a grapple, across a chasm, past a portcullis or next to a distant enemy, and from a higher slot it becomes an escape of up to a mile.

Dimensional Assault covers short distances within a fight at less cost, so Translocate is for the distances that spell cannot reach. From level 13 it is one of his studious spells, which puts it in his spellbook without cost and lets him enter Arcane Cascade as a free action when he casts it. It is worth a scroll before then and an occasional slot afterwards.""")

w('Vision of Death', """Vision of Death is the best spell Cyrus has against Will. Its damage is solid for the rank, and it frightens the target even on a successful save, so the slot is never wasted on a living enemy that can feel fear. In a Spellstrike it adds that damage to the Strike and leaves the target easier for everyone to hit and to affect with further spells.

Mindless creatures and anything immune to mental or death effects ignore it completely, which rules it out on some days. Where it does work, it is the strongest thing he can do to an enemy with a weak Will, as large and physically powerful creatures often have. He prepares it when the day's enemies are known to be living and capable of thought.""")

w('Containment', """Containment encloses one creature in a field of force, and it has two opposite uses. Cast on an enemy that fails its save, it takes a threat out of the fight for a while. Cast on a fallen ally, it prevents them from being killed where they lie. The second use is the more dependable, because a willing target does not attempt a save.

Nothing passes through the field in either direction, so a contained enemy cannot be attacked either, and an enemy that succeeds at its save is merely delayed. The spell is needed only occasionally and suits a scroll.""")

w('Force Rain', """Force Rain can be cast in three ways from one slot, each dealing a damage type that almost nothing resists. The two-action burst is compact and works well through Expansive Spellstrike. The one-action version is the most valuable of the three: it deals force damage to a single square against a basic save, and Cyrus can add it after a Spellstrike in the same turn without the penalty a second attack would carry. The three-action version deals a fixed amount of damage with no save at all.

It has no added effect, and it targets Reflex, as many of his spells already do. Even so, its flexibility and its damage type make it one of the most widely useful spells he can prepare at this rank.""")

w('Life-Draining Roots', """Life-Draining Roots is a short line of piercing damage that gives Cyrus temporary Hit Points for each living creature it hits. The line is too short to reach many creatures, so he usually gains little, and Lightning Bolt deals more damage in a far longer line.""")

w('Grasping Earth', """Grasping Earth holds the enemies in an area in place and leaves them off-guard, which suits Laughing Shadow and any allies who fight in melee. A grabbed enemy cannot pursue his side's spellcasters or leave his reach.

Both its damage and its lasting effect depend on its being sustained, which costs Cyrus his recharge, and it needs failed Fortitude saves from the kind of enemy that seldom fails them. Skyglass Prison holds a single enemy more reliably, so Grasping Earth is for holding several enemies that stand close together.""")

w('Confusion', """Confusion costs its target an action even on a successful save, and on a failure the enemy may turn on its own side. Against a group of dangerous enemies a failure can change the course of a fight, and in a Spellstrike the stun on a success comes on top of a Strike.

At this rank it affects one creature and needs a failed save for the larger effect, and a confused enemy may simply attack Cyrus. Mindless creatures are immune. Paralyze does more to a single enemy of his own level, so Confusion is the better choice when his side is outnumbered.""")

w('Unfettered Movement', """Unfettered Movement protects one creature for ten minutes from grapples, webs and anything else that would slow or hold it. Against an enemy that grabs or restrains, it comes close to removing the danger altogether, and a scroll read before such a fight is the right way to use it.""")

w('Clairvoyance', """Clairvoyance lets Cyrus see a place before entering it. A minute of casting gives a view of the room beyond a door, which is worth a great deal to a group that plans its approach. It has no use once a fight has begun, so it belongs on a scroll.""")

w('Wall of Mirrors', """Wall of Mirrors creates a solid wall for two actions, which is rare at any rank. The wall blocks movement, arrows and line of effect, so it can divide a fight in two, close a corridor against reinforcements or shelter his allies from a volley. It lasts a minute unless he dismisses it, and enemies that attack it are harmed for doing so.

Most walls take a whole turn to cast, whereas this one leaves Cyrus an action to Stride or to raise Shield. It deals no damage itself, and a wall in the wrong place hinders his allies as much as the enemy. Allowing for that, it is one of the strongest means of controlling a battlefield that he can prepare.""")

w('Zephyr Slip', """Zephyr Slip is a reaction that carries Cyrus away from an enemy that has just moved up to him. Neither part of that suits him, because he wants enemies within his reach and keeps his reaction for Reactive Strike.""")

w('Rebounding Barrier', """Rebounding Barrier is a reaction that reduces one physical hit against Cyrus and returns a little damage. The reduction is decent, but the reaction is also needed for Reactive Strike, and Wooden Double protects him from the hits that most endanger his life.""")

w('Bestial Curse', """Bestial Curse hampers only humanoids, and only those that fail a Fortitude save. With so narrow a target and so weak an effect, it has nothing to recommend it over Fear or Slow.""")

w('Chromatic Ray', """Chromatic Ray is a very hard-hitting attack spell with an element of chance. Its damage is among the highest Cyrus can attach to a Strike's roll at this rank, and when doubled on a critical hit it can end a fight. Three of its four colours deal heavy energy damage, and the fourth replaces the damage with a hindering effect.

He cannot choose which type of damage it deals, so an enemy that happens to resist it may take little, and the spell does not improve evenly from rank to rank. When the target has no known resistances, few spells deal more on an attack roll.""")

w('Countless Eyes', """Countless Eyes prevents one creature from being flanked. It helps an ally who is being surrounded, but two actions are a high price for so limited a benefit, and it is seldom the best use of a turn.""")

w('Creation', """Creation makes a temporary object to order, such as a ladder, a plank, a wedge or a simple tool. It is useful for solving a physical obstacle when there is a minute to spare, and a scroll or wand covers the occasional need.""")

w('Dispelling Globe', """Dispelling Globe is a stationary sphere that attempts to counter spells directed into it. In a fight that Cyrus knows will involve a great deal of enemy magic, it can protect him and whoever stands beside him. It keeps him in one place, however, which suits a fighter with a reach weapon poorly, and it counters only weaker spells.""")

w('Draw the Lightning', """Draw the Lightning damages a target that is above Cyrus, and then adds electricity damage to his first Strike in each round for a minute. The lasting bonus is the attraction, because it increases every Spellstrike for the rest of the fight at no further cost.

The target must be taller than he is or standing higher, which excludes many enemies, and the bonus on each hit is modest. The spell repays its slot over a long fight against a large creature and not otherwise.""")

w('Dull Ambition', """Dull Ambition is a curse that lowers one enemy's initiative and, on a failed save, its other checks for a long time. The strongest part of it comes too late to matter in a fight that has already begun, so it belongs to intrigue more than to combat.""")

w('Fire Shield', """Fire Shield is a sturdier magical shield than the cantrip. It needs no hand, and it burns enemies that strike Cyrus in melee. In a fight made up of many small hits, its block absorbs a good deal of damage over a minute.

Raising it takes an action each round and blocking takes his reaction, and he is always short of both. It therefore suits only a fight in which he has a spare third action each turn and does not need to keep his reaction for Reactive Strike.""")

w('Flicker', """Flicker gives resistance to nearly all damage for a minute, together with a random teleport at the end of every turn. The resistance is useful, but the teleports keep moving Cyrus out of the position he chose, which is a serious cost for someone who depends on reach and flanking.""")

w('Grasp of the Deep', """Grasp of the Deep deals moderate damage against Will and grabs the target if it fails its save. A grabbed enemy cannot move out of his reach and is off-guard, which gives Cyrus Laughing Shadow's extra damage on every later Strike, and breaking free costs the enemy an action and a check against his spell DC.

A successful save still lets half the damage through, so the slot is never wasted, although the grab needs a failure. As a mental effect it does not work on mindless creatures. It is a good second Will spell after Vision of Death, and the better of the two when he wants an enemy held in place.""")

w('Ice Storm', """Ice Storm takes a whole turn to cast and an action to sustain, in return for modest damage and difficult terrain. A caster standing well back can afford that. For Cyrus it costs two turns of Spellstrike and delivers less damage than either of them would.""")

w('Invisibility Curtain', """Invisibility Curtain is a wall that hides everyone on one side from those on the other. It can screen an approach or a retreat at the price of a turn and an action each round, but Shared Invisibility is the simpler way to move unseen.""")

w('Liminal Doorway', """Liminal Doorway opens a hidden room that lasts eight hours. That provides a safe place to rest in hostile territory, or to hide people and goods. It takes ten minutes to cast and is never needed in a hurry, so it is well suited to a scroll or wand.""")

w('Mercurial Stride', """Mercurial Stride is a double Stride that passes through one enemy and poisons it. Getting past an enemy that blocks the way has some value, but Dimensional Assault and Time Jump do that better, and the poison is minor.""")

w("Mirror's Misfortune", """Mirror's Misfortune creates an illusory double, and attackers who strike it roll worse afterwards. It protects Cyrus less reliably than Mirror Image or Blur, both of which are available two ranks lower.""")

w('Morass of Ages', """Morass of Ages is an aura that can slow every enemy near Cyrus and grows as he sustains it. An aura of this kind belongs on someone who fights surrounded by enemies, and taking an action from each of them would be powerful.

Each creature saves only once, against Fortitude, and those that succeed are unaffected for the rest of the spell, while sustaining it takes the action he needs to recharge. The spell promises a great deal but depends too much on failed saves to be relied upon.""")

w('Mountain Resilience', """Mountain Resilience gives steady resistance to physical damage, which is the kind most enemies deal. Its twenty minutes are long enough for it to be cast before a fight, and on Cyrus or on an ally in melee it reduces every weapon hit. The stronger versions from higher slots are worth far more.

Each hit shortens its duration, so it runs out quickly against a large number of attacks, and it does nothing against energy damage or spells. It makes a good scroll or wand for a fight he can see coming, whereas in a slot it would displace spells that end fights sooner.""")

w('Nightmare', """Nightmare harasses a known enemy from a distance by spoiling its sleep. That may serve a story, but it has no claim on the slots of an adventuring day.""")

w("Outcast's Curse", """Outcast's Curse makes one creature worse at social checks and disliked by those it meets, which could undermine a rival in an intrigue. It needs a touch and a failed save, and it has no use in a fight.""")

w('Peaceful Bubble', """Peaceful Bubble hides a camp from scrying and magical detection for a day. That matters only when the group is being hunted by magic, and a scroll is enough when it is.""")

w('Rust Cloud', """Rust Cloud deals heavy damage every round for a minute across a large area, and it needs no sustaining. Left on a group that cannot easily leave, such as enemies defending a room, it deals more damage in total than almost anything else at this rank, and the concealment it creates hampers their archers.

It takes a full turn to cast and harms allies who enter it, so Cyrus has to place it where his side will not be fighting, and enemies who are able to walk out will do so. It is a strong opening spell for an assault on a fixed position and is wasted in a fight where everyone is moving.""")

w('Seal Fate', """Seal Fate gives a living enemy a weakness to a damage type Cyrus chooses, briefly on a successful save and for a minute on a failure. Combined with a spell of that type, and with allies who deal the same type, the extra damage accumulates. Casting it costs him a turn he would have spent on a Spellstrike, however, and the brief version barely repays that.""")

w('Shape Stone', """Shape Stone reshapes a block of stone to make a hole in a wall, seal a doorway, form a step or raise a barricade. It solves many problems in stone buildings and caves, and a scroll covers the need.""")

w('Solid Fog', """Solid Fog creates a bank of fog that blocks sight and slows movement for everyone inside it. It takes a full turn to cast and hinders his allies as much as the enemy, so it is useful for covering a retreat and for little else.""")

w('Spell Immunity', """Spell Immunity protects against one named spell for a day. When the group knows what an enemy spellcaster is going to cast, it can cancel that enemy's most dangerous spell, and without that knowledge it is a guess. It is a scroll for a fight that has been well scouted.""")

w('Suggestion', """Suggestion can send a guard away, delay a pursuer or end a confrontation without a fight. For the one who negotiates on the group's behalf it has clear uses, and a suggestion that sounds reasonable may never be recognised as magic.

It has the incapacitation trait and needs a failed save, so it works on minor figures more readily than on anyone important, and a target that resists it strongly knows what was attempted. Cyrus is best served by carrying it as a scroll and using it where a failure would not be a disaster.""")

w('Telepathy', """Telepathy allows silent conversation in both directions with creatures nearby, and it can stand in for a shared language when there is none. Message and Translate meet most of the same needs at less cost.""")

w('Vampiric Maiden', """Vampiric Maiden deals damage against a Fortitude save and gives a small number of temporary Hit Points, and it holds the target on a failure. Vampiric Feast from rank 3 deals more damage and returns more to Cyrus, and a Spellstrike carries it to the end of his reach.""")

w('Vapor Form', """Vapor Form turns a creature into a drifting cloud that can pass through cracks and under doors. It is for infiltration and escape, since the target can do almost nothing in a fight, and it is best carried as a scroll.""")

w('Wall of Fire', """Wall of Fire is a burning line or ring that damages whatever crosses it and blocks sight. A ring round a group forces it to choose between staying where it is and being burned, and a line across a corridor harms every reinforcement that comes through.

It takes a whole turn to cast, fire is commonly resisted, and enemies with ranged attacks may simply stay behind it. It suits a caster who can afford the turn, and Wall of Mirrors blocks a passage for two actions.""")

w('Weapon Storm', """Weapon Storm deals area damage based on his weapon's damage die, either in a cone or around himself. The damage falls short of what area spells of the same rank deal and grows slowly, so Crashing Wave and Force Rain are better choices.""")

w('Winning Streak', """Winning Streak gives Cyrus or an ally extra speed for one action, and the effect continues for as long as his side keeps landing critical hits. On the right turn it gives a strong attacker an extra attack very cheaply.

How long it lasts depends on luck, and a rank-4 slot is a high price for what is usually a single round. Haste does the same for a whole fight from rank 3. Winning Streak is worth considering only alongside allies who score critical hits often.""")

w('Replicate', """Replicate creates an illusory copy of a willing person that can walk and say a few words, which can conceal an absence or serve as a decoy in an intrigue. It takes a full turn to cast and an action to sustain, and it has no use in a fight.""")

w('Discern Lies', """Discern Lies gives a large bonus to notice a lie for ten minutes. For the character who conducts the group's negotiations and interrogations, that is exactly what is needed at an important moment, and the other side gets no save against it.

It tells Cyrus that something is false without telling him what the truth is. He usually knows when an important conversation is coming, so a scroll serves well.""")

w('Planar Tether', """Planar Tether stops a creature from teleporting or leaving the plane. Against an enemy that habitually vanishes when it is losing, it can decide whether that enemy is finished off. It is narrow in use, and worth a scroll when such an enemy is known.""")

w('Sanguine Mist', """Sanguine Mist is a cloud of void damage that grows stronger, and gives Cyrus temporary Hit Points, for as long as he sustains it. The first round of damage is decent. Everything after that needs the action he uses to recharge, and the cloud harms living allies as well.""")

w("Mantis's Grasp", """Mantis's Grasp deals solid force damage from long range and holds the target in place on a failed save. Force is almost never resisted, and an immobilised enemy cannot leave his reach or get to his side's spellcasters. In a Spellstrike it is as good as anything at this rank, and it is equally good cast from a distance.

The hold needs a failed Reflex save and lasts one round unless the failure is critical. Against an enemy Cyrus wants kept in place, it is a stronger single-target spell than Force Rain.""")

w('Entangle Fate', """Entangle Fate leaves several enemies off-guard even when they succeed at their saves. That lowers their AC against everyone and gives Cyrus Laughing Shadow's extra damage without any need to flank, and with up to four enemies affected at once it is a large benefit from one casting.

It deals no damage, and its stronger effects need several failed saves. Cast as a fight against a group begins, it adds more to his side's damage over the following rounds than a damage spell would have dealt.""")

w("Infiltrator's Tunnel", """Infiltrator's Tunnel makes a door through a wall. Two linked portals let Cyrus step into a sealed room, past a locked gate or out of a cell, and from a higher slot his allies can follow. In a planned infiltration it removes obstacles that would otherwise need skill checks or noise.

In a fight it offers nothing beyond a way out, so it is a scroll for the task that needs it.""")

w('Freezing Touch', """Freezing Touch can hold an enemy in place for a whole fight. On a failed save the target is stuck until it breaks free and takes persistent cold damage throughout, and its attempts to escape cost it actions. A Spellstrike extends the touch to his reach, and even a successful save leaves some persistent damage.

It targets Fortitude, so the hold is least likely to succeed against the large enemies Cyrus would most like to stop, and the damage arrives slowly. It is best used on mobile or fragile enemies, and Skyglass Prison holds a target for a round even when it succeeds at its save.""")

w('Friends to Foes', """Friends to Foes deals damage and frightens its target through a Will save, with a condition that suits fights against groups: the fear does not fade while the target stands near its allies. In a close formation that keeps an enemy weakened for much longer than ordinary fear would, and it applies even on a successful save.

Against a lone enemy that condition never applies, and Vision of Death deals more. Mindless creatures are immune. It is the right choice for fights against several intelligent enemies who stay together.""")

w('Lost Things Returned', """Lost Things Returned takes an action from an enemy even on a successful save, as Slow does, but it tests Will instead of Fortitude. That makes it the answer to large enemies with strong bodies and weaker minds, against which Slow struggles. On a failed save the effect lasts for the fight.

An ally can end the effect early by striking the illusion, which deals a large amount of damage to the target, so his side can choose between the lost actions and the damage. Mindless creatures are immune. It is worth learning as the Will counterpart to Slow.""")

w('Gift of Dusk', """Gift of Dusk weakens an enemy's attacks for a full minute even when it succeeds at its save. Against a hard-hitting melee enemy, a minute of reduced damage is a real defensive gain for those fighting it, and a failed save makes the reduction larger.

It adds no damage and has no effect on creatures that cast no shadow, and Enfeeble gives a shorter version from rank 1. It is a fair choice against one powerful melee enemy when surviving it is the difficulty.""")

w('Unending Tears', """Unending Tears dazzles one enemy until it spends an action clearing its eyes, even on a successful save. An action lost or a chance of missing is a modest return for a rank-4 slot, and Ignite Fireworks dazzles a whole group from rank 2.""")

# ───────────────────────── rank 5 ─────────────────────────
w('Weight of the World', """Weight of the World is the best single-target spell at this rank, and the reason is what it does on a successful save. An enemy that succeeds still loses an action and spends a round dazzled, and one that fails loses two actions and remains dazzled for the fight. Against a single powerful enemy, each of whose actions is worth more than anything else in the encounter, that is the most valuable effect Cyrus can add to a Strike.

It targets Fortitude, so failures will be rare against large enemies, but the spell is worth casting for the success alone, and its damage is a secondary benefit. From level 9 it deserves one of his highest slots on any day with a serious single enemy, and when a Strike cannot reach, he can cast it from range instead.""")

w('Wall of Stone', """Wall of Stone is the strongest means of controlling a battlefield that Cyrus can cast at this rank. A hundred and twenty feet of shaped stone can divide an encounter in two, close a corridor behind his allies, shut out reinforcements or serve as a bridge or a stair. The enemy gets no save and must break the wall or go round it, and either takes rounds.

It uses his whole turn, so he casts it in the first round while the enemy is still approaching, and a badly placed wall hinders his own side as much as the enemy. On a day with a large or awkward fight ahead, one slot spent on it can be worth more than any attack spell.""")

w('Glacial Skewer', """Glacial Skewer is an attack spell that rewards attention to position. Its damage is solid for the rank and is settled by the Strike's roll, so it doubles on a critical hit, and few creatures resist both cold and piercing. If the push it causes drives the target into a wall, a pillar or another large obstacle, the target is pinned there.

Where there is no obstacle, the push moves the enemy out of his reach, which Cyrus does not always want, so he needs to choose his angle before the Strike. Indoors, with a wall behind the target, the pin makes it the best attack spell at this rank. On open ground Blood Feast deals more, and a heightened Briny Bolt serves as well.""")

w('Blazing Fissure', """Blazing Fissure is the line spell around which Cyrus plans his turns from level 9. Its damage equals the best at the rank and is divided between fire and bludgeoning, so resistance rarely stops all of it. Every enemy that fails its save is knocked prone, which leaves it off-guard to him and to his allies in melee, and it must spend an action standing up within reach of his Reactive Strike.

Through Expansive Spellstrike the line runs away from his allies, and with Sprinting Spellstrike at level 12 it carries him the length of the battlefield past a row of fallen enemies. It affects only creatures on the ground. Lightning Bolt from a higher slot deals a little more damage, but Blazing Fissure changes more about the fight.""")

w('Tornadic Gale', """Tornadic Gale is a line that draws targets into itself. It pulls smaller enemies in from either side before damaging them, which turns a loose group into a full row, and it lifts and drops those that fail their saves. With Sprinting Spellstrike it gathers enemies up as Cyrus passes.

It does not pull Large creatures, and its damage is of a single type, so a resistant enemy takes little. Blazing Fissure is the more dependable choice against large enemies standing in a file, and Tornadic Gale is better against a scattered crowd of ordinary ones.""")

w('Howling Blizzard', """Howling Blizzard is a wide and long cone of heavy cold damage that leaves difficult terrain behind for a round. Through Expansive Spellstrike its 60 feet cover most of a battlefield beyond his target, and the terrain slows whatever survives.

It offers only damage and a brief hindrance, and cold is sometimes resisted. The three-action version is an ordinary long-range area spell that Cyrus will seldom have reason to cast. Against a group it is a sound choice, though Blazing Fissure and Elemental Breath usually offer more.""")

w('Impaling Spike', """Impaling Spike deals moderate damage and pins the target on a failed save. The spike is cold iron, so creatures weak to that metal take more. An impaled enemy stays where it is until it tears itself free, which keeps it within his reach.

The pin needs a failed Reflex save, so it is least likely to work on the agile enemies Cyrus most wants to hold, and the range is short. It is a good spell against creatures with a weakness to cold iron and an ordinary one otherwise.""")

w('Shadow Siphon', """Shadow Siphon is a reaction that weakens an enemy's damaging spell for everyone it would affect. When it works it can halve an area spell that would have hurt all his allies. It depends on a counteract check, however, and it keeps a rank-5 slot in reserve for a moment that may never come.""")

w('Corrosive Muck', """Corrosive Muck creates two pools that slow and burn whatever crosses them for a minute, and it needs no sustaining. Placed across the approaches to his allies, the pools punish every enemy that advances, and the damage each round is substantial.

Cyrus casts it without a Strike before the two sides meet, because Expansive Spellstrike places only one burst. Enemies with ranged attacks can ignore it. It is a good spell for defending a position.""")

w('Banishment', """Banishment removes a creature that does not belong on this plane, completely, if it fails its save. Against summoned and extraplanar enemies it can end a fight in one casting. It does nothing to creatures native to the plane and has the incapacitation trait, so it belongs on a scroll kept for the day such enemies appear.""")

w('Space Fold Gate', """Space Fold Gate opens a passage between two points that the whole group can use for a minute. It crosses chasms and reaches distant objectives at the price of a full turn and an action each round, which makes it a spell for exploration that a scroll can hold.""")

w('Magic Passage', """Magic Passage opens a tunnel through ten feet of wall for an hour. It bypasses doors, guards and traps altogether, which is extremely useful to a group that plans its way in, and it is best carried as a scroll.""")

w('Scouting Eye', """Scouting Eye creates a mobile, invisible eye for looking ahead. It sees what Cyrus would see and goes where he would not want to go. It takes a minute to cast and an action to move, which is no hardship outside a fight, and a scroll is the right way to carry it.""")

w('Sending', """Sending carries a short message to anyone Cyrus knows well, anywhere on the same world, and brings back a reply. Nothing else keeps him in touch with distant allies and patrons in the same way, and a scroll or wand covers the need.""")

w('Drop Dead', """Drop Dead is a reaction that makes an ally appear to die when they are hit, and hides them. Against enemies that stop attacking the fallen, it takes a badly hurt ally out of danger for the price of one reaction.

The deception fails if the apparent death is implausible, it has to be sustained, and it ends when the ally acts. It also uses the reaction Cyrus keeps for Reactive Strike. It is a clever emergency measure for a spare slot, and nothing more than that.""")

w('Acid Storm', """Acid Storm rains acid over a wide area for a minute without needing to be sustained. Its damage each round is low for the slot, and enemies can walk out of it. Rust Cloud does the same thing with far more damage from rank 4.""")

w('Blink Charge', """Blink Charge resembles Dimensional Assault cast from a spell slot. Cyrus appears beside an enemy up to 60 feet away and Strikes with extra force damage, provoking nothing on the way. On a day when his Focus Points are spent, or when the distance is too great for the focus spell, it brings him into the fight with a hit.

It is not a Spellstrike, so the Strike carries only that small amount of extra damage, and a rank-5 slot is a high price for it. A scroll is worth having, but the slot rarely is.""")

w('Blister', """Blister stores damage for later turns. Each blister can be burst with a single action to release a cone of acid from the target, so in the following rounds Cyrus can Spellstrike and still, with his third action, release what amounts to a second damage spell.

The number of blisters depends on the target's Fortitude save, and a success produces only one. The cones spread outward from the target, which puts allies near it at risk. Against a durable enemy that fails its save the total damage is excellent, and against one that succeeds it is slight.""")

w('Cloak of Colors', """Cloak of Colors protects its target by hindering attackers. Enemies next to the target are dazzled without a save, and those that hit it in melee risk being blinded. On an ally fighting in melee it reduces the number of hits they take for a minute.

The blinding effect has the incapacitation trait and needs a failed save, so against strong enemies only the dazzled condition can be counted on. It costs two actions in the first round, which makes it a reasonable opening when Cyrus is not yet within reach of anyone.""")

w('Elemental Breath', """Elemental Breath is a long cone of very high damage with an added effect, in an element chosen at random. Through Expansive Spellstrike its 60 feet cover the ground beyond his target, and each element adds something useful to the damage.

With two actions Cyrus cannot choose the element, so he may roll one that the enemy resists, and the three-action version that lets him choose cannot go into a Spellstrike. When resistances are not a concern, it is the hardest-hitting cone he has at this rank.""")

w('Flowing Strike', """Flowing Strike is a long move that provokes nothing, with a Strike along the way. It takes his whole turn and achieves less than a Stride and a Spellstrike would, and from level 12 Sprinting Spellstrike does the same thing far better.""")

w('Forceful Hand', """Forceful Hand creates a floating hand that shields Cyrus or an ally for as long as he sustains it. The protection is modest, and sustaining it takes the action he needs for recharging, so it does not suit a magus.""")

w('Freezing Rain', """Freezing Rain creates difficult terrain at once and deals its damage later, after a full turn of casting and with an action each round to sustain it. That is too slow for someone whose turns are worth as much as his.""")

w('Geyser', """Geyser deals damage at very long range, throws enemies into the air and leaves them prone when they land. Prone enemies are off-guard, which brings Laughing Shadow's extra damage, and the range makes it a good spell to cast before the two sides meet.

Its area is a cylinder, which Expansive Spellstrike does not cover, so Cyrus can only cast it without a Strike. Blazing Fissure knocks enemies prone along a line that he can place with a Strike. Geyser is worth having for the long-range opening if he has a slot free.""")

w('Glimmer of Charm', """Glimmer of Charm is an aura that softens the attitude of people near Cyrus. It could ease a tense negotiation, but it has to be sustained, it has the incapacitation trait, and using magic on the people he is negotiating with carries risks of its own.""")

w('Grisly Growths', """Grisly Growths deals solid single-target damage against Fortitude, and its basic save means half of it still applies on a success. Unlike Vampiric Feast, it works on almost any creature with a body, living or not. The sight of it also sickens creatures within 30 feet that fail a Will save, the target included, which is a useful penalty to spread across a group of enemies.

That second effect does not spare allies, so the spell suits a target standing among its own side, and mindless creatures ignore the sickness. Weight of the World does far more against one strong enemy, and Grisly Growths is the choice when the aim is to finish off something whose Fortitude is not its best save.""")

w('Hallucination', """Hallucination changes what one creature perceives for an hour, so that it fails to see a person, takes a door for a wall or mistakes a stranger for a friend. For intrigue and infiltration that is subtle and powerful, and casting it draws little attention.

It has the incapacitation trait and depends on a failed save, and the target gets chances to see through it. It has no use in a fight, so it is a scroll or wand for the scheme that calls for it.""")

w('Illusory Scene', """Illusory Scene creates a complete illusion with moving figures, sound and smell that lasts an hour. It can imitate a camp, a patrol or a gathering in order to mislead pursuers or draw guards away. It takes ten minutes to cast, so it belongs to planning and to a scroll.""")

w('Imaginary Lockbox', """Imaginary Lockbox hides a container in his mind until his next preparations, which is useful for getting something past a search. Its use is very narrow.""")

w('Invoke Spirits', """Invoke Spirits deals low damage in a small burst that must be sustained and moved, and it frightens only on a critical failure. It needs the action Cyrus uses for recharging every round and returns very little for a rank-5 slot.""")

w("Mariner's Curse", """Mariner's Curse imposes a penalty that does not wear off. On a failed save the target stays sickened for the rest of the fight however often it retches, which outlasts fear and lowers its attacks, saves and AC throughout. Even on a success it is sickened until it spends an action to recover.

The spell needs a touch, which a Spellstrike extends to his reach, and a failed Will save for the lasting version. In a long fight against one durable enemy it gives more over time than Fear does, but in a short fight Fear does much the same from a slot four ranks lower.""")

w('Mind Probe', """Mind Probe questions a creature's memories directly. In an investigation it can produce answers that no ordinary interrogation would, and Cyrus is the member of the group who asks the questions.

It takes a minute to cast and needs a failed Will save, and each answer can still be resisted. It is for use outside combat on a captive or a cooperative witness, and a scroll is the way to carry it.""")

w('Mirror Malefactors', """Mirror Malefactors is the one sustained spell that repays a magus for the action it costs. The first casting deals heavy mental damage and causes fear that cannot be shaken off while the mirrors last, and each time Cyrus sustains the spell the damage is repeated. His third action therefore deals as much as a damage spell in every following round, alongside a Strike.

Sustaining it does take the action he would use to recharge his Spellstrike, so he either alternates between the two or goes without the recharge while the mirrors remain. It works on creatures of Large size or smaller that have minds. Against one tough enemy of that kind, it produces some of the highest total damage he can get from a single slot.""")

w('Pressure Zone', """Pressure Zone makes living enemies across a wide area clumsy, which lowers their AC and Reflex for every attacker and for his Trip. On a failed save the effect lasts and grows worse.

It takes his whole turn and targets Fortitude, and creatures that succeed are affected only briefly and are then immune. It is worth casting from very long range before a fight against a group, and otherwise it costs Cyrus too much of his own damage.""")

w('Quicken Time', """Quicken Time speeds up everyone in an area, enemies included. Unless his allies can occupy the area alone it helps both sides, which limits it to the opening round around his own group. Haste on one ally is more dependable.""")

w('Rewinding Step', """Rewinding Step returns Cyrus to a marked spot within ten minutes of casting. It provides a planned way out of a theft or a risky scouting trip and has no ordinary use in combat.""")

w('Slither', """Slither grabs and holds the creatures in an area without needing to be sustained. Enemies caught in it are off-guard and unable to move, and they must save again in each round they remain, so over a minute it ties a group down thoroughly. That suits Laughing Shadow and his allies in melee very well.

It takes a full turn to cast and harms allies who enter the area. Cast in the first round onto the enemy's side of the field, it is one of the better control spells at this rank for someone who can afford only one such turn in a fight.""")

w('Stagnate Time', """Stagnate Time creates an area that can take an action from every enemy inside it each round for a minute, without being sustained. Over a fight that amounts to a very large number of lost actions, provided the enemies fail their saves and stay where they are.

Nothing happens on a successful Will save, the area affects allies who enter it, and enemies are free to leave. For two actions it is still one of the strongest area effects Cyrus can cast when the enemy has to hold its ground, which makes it a spell for groups defending a particular place.""")

w('Subconscious Suggestion', """Subconscious Suggestion plants a suggestion that waits for a trigger. It suits a plan that unfolds over time, such as a steward who will leave a door unlocked or a guard who will look away at a signal. Because of the incapacitation trait it works on minor figures, and it is a scroll for intrigue.""")

w('Summon Dragon', """Summon Dragon takes a full turn to cast and an action each round to maintain, and the creature it brings is well below the level of anything Cyrus is fighting. Like every summoning spell, it uses up the actions on which his own turn depends.""")

w('Telekinetic Haul', """Telekinetic Haul moves a very heavy object from a distance. It can lift a portcullis, shift a boulder or drop something large, and a scroll covers the occasional need for that.""")

w('Toxic Cloud', """Toxic Cloud is a drifting cloud that deals heavy poison damage each round for a minute. Against breathing enemies that cannot get out of its path the total is high. It takes a full turn to cast, it drifts in a set direction once cast, it harms allies, and many creatures that are not alive are immune to poison.""")

w('Truespeech', """Truespeech removes every language barrier for an hour, and for a working day from a higher slot. For the group's negotiator it turns encounters that would have been fights or stalemates into conversations.

It is needed on particular days and never in the middle of a fight, so a wand or scroll is the right way to carry it. On a journey among strangers it is one of the most valuable spells Cyrus can have with him.""")

w('Umbral Journey', """Umbral Journey provides fast overland travel for the whole group. It shortens long journeys dramatically and has no other use, so a scroll is enough when distance is the difficulty.""")

w('Wall of Ice', """Wall of Ice is an opaque wall or dome that blocks sight and movement and chills those who break through it. A dome can trap a small group or shelter his allies for a round or two.

It takes a full turn to cast and can be shattered. Wall of Stone at the same rank is larger, stronger and more flexible, so Wall of Ice is the alternative when blocking sight matters most.""")

w('Wave of Despair', """Wave of Despair removes the reactions of every enemy in a cone, including those that succeed at their saves, and can go on to take actions from those that fail. With a whole group unable to react for a round, his allies can move, cast and withdraw without being punished, and the cone is easy to direct through Expansive Spellstrike.

The lasting effects depend on failed Will saves, mindless creatures are immune, and the spell deals no damage. Against several enemies with dangerous reactions it is a very strong way to open a fight.""")

w('Etheric Shards', """Etheric Shards creates difficult terrain that also hinders flying and incorporeal creatures and deals light damage to anything moving through it. It slows an advance, which is a small effect for a rank-5 slot.""")

w('Telepathic Bond', """Telepathic Bond allows silent communication among the whole group at any distance for eight hours. That is ideal when the group has to separate or during an infiltration, and a scroll covers the day it is wanted.""")

w("King's Castle", """King's Castle exchanges his position with a willing ally's. It can take a threatened spellcaster out of melee by putting Cyrus there instead, which is a fair exchange for someone who fights at the front. As a rescue it applies in few situations, and a rank-5 slot is a high price for it.""")

w('Control Water', """Control Water raises or lowers water over a wide area. That matters in flooded ruins and at sea and nowhere else.""")

w('Blinding Bottle', """Blinding Bottle is a very large burst that can blind a whole group for several rounds. Blinded enemies are nearly helpless, so when the spell takes hold the fight is effectively decided.

It has the incapacitation trait, targets Fortitude and is a poison, so enemies that are higher in level, physically tough or not alive are all largely unaffected, and a 30-foot burst cannot be used anywhere near his allies. Cyrus casts it without a Strike, from long range, at a crowd of weaker living enemies.""")

w('Blinding Foam', """Blinding Foam is an attack spell that blinds on a hit, with no save. In a Spellstrike, a successful Strike leaves the target blind until it spends three actions clearing its eyes, and it takes acid damage throughout. Against an enemy of his own level that comes close to winning the fight.

It has the incapacitation trait, so a higher-level enemy treats his hit as one step worse and usually avoids the blindness. Against enemies of his level it is outstanding, and against a single powerful enemy the brief blindness from Briny Bolt is more reliable.""")

w('Blood Feast', """Blood Feast is the hardest-hitting attack spell at this rank, and it gives Cyrus temporary Hit Points equal to half the damage it deals. It is settled by the Strike's roll, and a Spellstrike extends its touch range to his reach, so a hit both removes a large part of an enemy's Hit Points and makes him harder to kill in return.

It does nothing to hinder the target. It gains dice with every rank, and from a rank-6 slot it still deals more on a hit than Disintegrate does once that spell's Fortitude save is taken into account. When the aim is damage on an attack roll and he expects to be hit back, nothing at rank 5 does it better.""")

w('Boomerang Shot', """Boomerang Shot deals heavy damage on an attack roll and ignores concealment and most cover. Cast without a Strike, that makes it the answer to an archer behind a wall or an enemy in fog. In a Spellstrike those advantages seldom apply, and its damage is roughly equal to that of a heightened Briny Bolt without the blindness.""")

w('Plasma Whirl', """Plasma Whirl is a cone that can be cast in three sizes and deals two types of damage, so resistance to one type rarely stops it. The one-action cone can follow a Spellstrike in the same turn, the two-action cone works through Expansive Spellstrike, and the three-action version adds a sickening effect that Cyrus can obtain only by casting it without a Strike.

At each size its damage is a little below that of the best spells built for a single purpose. What it offers is a choice of uses from one prepared slot, which is valuable when he does not know what the day will bring.""")

w('Crucible of Iron', """Crucible of Iron hinders its target even on a successful save, leaving it dazzled and burning. On a failure the target is also weakened for the fight until it breaks free. It therefore suits a Spellstrike against an enemy that Cyrus expects to succeed at its save.

Each of the effects is mild, and Weight of the World does far more to a single enemy from the same slot. Crucible of Iron targets Reflex, which makes it the second choice for an enemy whose Fortitude is too strong for Weight of the World to be worth casting.""")

w('Scouring Pulse', """Scouring Pulse is very strong against undead and does nothing at all to the living. In the right fight it deals heavy damage throughout a column, leaves lingering damage, and marks what it hits with a glow that removes concealment and invisibility.

Its cylinder cannot be used with Expansive Spellstrike, so Cyrus has to cast it without a Strike. It is worth preparing only when undead are certain, because on any other day the slot does nothing.""")

# ───────────────────────── rank 6 ─────────────────────────
w('Disintegrate', """Disintegrate is the largest single hit Cyrus can attach to a Strike at this rank, but it comes with a condition. The attack must land, and the target then attempts a basic Fortitude save as well, so a strong enemy that has been hit will often halve the damage. Only a critical hit, which worsens the result of that save, produces the very high numbers the spell is known for.

It is therefore a spell to combine with Sure Strike, because with two rolls against an off-guard target the chance of a critical hit is high enough to justify the slot. Without that preparation Chain Lightning deals as much on average with less variation. Disintegrate also destroys walls of force and objects outright, which is occasionally the reason for casting it.""")

w('Chain Lightning', """Chain Lightning is the most dependable source of heavy damage at this rank. In a Spellstrike only the creature Cyrus strikes is affected, but that is still a very large hit against a basic save, and it applies even when the Strike misses. Cast without a Strike, it passes through every enemy on the battlefield from a great distance with no risk to allies, which no other area spell can do.

One prepared slot therefore has two excellent uses, as a single-target hit in a Spellstrike or as the safest of all area spells on a turn when he cannot reach melee. It has no added effect, and electricity is sometimes resisted. It is worth keeping prepared from level 11.""")

w('Living Thunderbolt', """Living Thunderbolt does more for the way Cyrus fights than any other spell at this rank. For a minute he flies quickly, slips out of grapples and damages every enemy he moves through, so each Stride he takes on the way to a Spellstrike is also an area attack that costs him no extra action. Flying at that speed also brings every enemy on the battlefield within the range of a single turn.

It takes two actions at the start of a fight and occupies one of his two highest slots, and all of its damage is electricity. Against a group, the total over a minute is far greater than that of any single spell, so it is worth preparing for any large fight from level 11.""")

w('Wall of Force', """Wall of Force is the strongest barrier available. It is invisible, almost unbreakable for its one-minute duration and proof against everything physical. It divides an encounter cleanly, shuts out a pursuer or gives his allies a round in which to recover.

It takes a full turn to cast, and allies cannot attack through it either. Wall of Stone covers more ground and is permanent, while Wall of Force is harder to get past. A scroll kept for a fight that has to be divided is good value.""")

w('Silver Spear', """Silver Spear deals strong damage on an attack roll, and against fiends it is exceptional, because it adds a second full set of spirit damage and can stop them teleporting away. As the spear is silver, it also exploits that weakness in creatures that have it.

Against ordinary enemies its damage is sound but unremarkable for the slot, and it has no added effect. When fiends or creatures weak to silver are expected it is the best spell Cyrus has, and on other days Chain Lightning serves better.""")

w('Petrify', """Petrify slows its target on a successful save and may remove it from the fight altogether if it fails and goes on failing. The effect on a success is the part Cyrus can count on, since it costs any enemy an action.

The later saves have the incapacitation trait, so a strong enemy is unlikely to be turned to stone, and Slow provides the same dependable effect from rank 3. Petrify suits a fight against several enemies of his own level, one of which might well be removed permanently.""")

w('Cast into Time', """Cast into Time is a short cone of mental and bludgeoning damage against Fortitude that sickens whatever fails. Its damage is below that of the better spells at this rank, the cone seldom contains more than two enemies, and the creatures it removes return before they would next have acted. Vitrifying Blast and Vampiric Exsanguination are stronger cones.""")

w('Unexpected Transposition', """Unexpected Transposition is a reaction that puts someone else in the path of an attack aimed at Cyrus. If he exchanges places with an enemy, that enemy's ally strikes it instead, and if he exchanges with a sturdy friend, he is spared a hit he could not afford.

An unwilling target gets a Will save, and the reaction is also wanted for Reactive Strike. The spell can produce a remarkable turn and can equally do nothing, so it is something for a spare slot.""")

w('Collective Transposition', """Collective Transposition rearranges a battlefield by moving two creatures to any point within 30 feet of Cyrus. Allies go willingly, so one casting can set up a flank, rescue a spellcaster or bring a melee ally into reach, and enemies that fail their saves are moved wherever his side wants them.

Enemies get a Will save, and the spell deals no damage. In a Spellstrike it moves only the creature he strikes, so moving two creatures means casting it without a Strike. It is useful when his allies fight by position, and often more than he needs.""")

w('Truesight', """Truesight sees through illusions, disguises and changes of shape for ten minutes. On a day when the enemy relies on such deceptions it is decisive, and on other days it does nothing, so it belongs on a scroll.""")

w('Mislead', """Mislead makes Cyrus invisible in a way that survives his attacks and creates a decoy that acts in his place. Enemies are off-guard to him throughout, which keeps Laughing Shadow's extra damage applying, and their attacks go to the decoy for as long as they are deceived.

It must be sustained, which takes the action he uses to recharge, and Dimensional Disappearance already makes him invisible from level 10. It is clever, but by the time he can cast it he has little need of it.""")

w('Teleport', """Teleport carries the group over long distances. It ends journeys and allows a withdrawal to safety between adventures. As it takes ten minutes to cast, it belongs on a scroll or wand and never in a slot meant for combat.""")

w('Arrow Salvo', """Arrow Salvo deals very heavy piercing damage over a large burst at range. Cast without a Strike before the two sides meet, it is one of the best area spells of the rank, and piercing damage avoids the resistances that so often reduce fire and cold.

The burst is far too large for Expansive Spellstrike, and Chain Lightning does similar work without endangering allies. It is worth having only if Cyrus wants a spell purely for area damage at long range.""")

w('Chromatic Image', """Chromatic Image works like Mirror Image, except that each image destroyed hurts or hinders the attacker. Against an enemy that makes many attacks it both prevents damage and returns some.

It costs two actions and protects only Cyrus, and from level 7 Blur defends him more cheaply while letting him enter Arcane Cascade as a free action. A rank-6 slot is a great deal to pay for it.""")

w('Cursed Metamorphosis', """Cursed Metamorphosis turns an enemy into a harmless animal for a minute if it fails its save, which removes it from the fight, and it still sickens the target on a success.

It has the incapacitation trait and targets Fortitude, so it is for enemies of his level or below, and against those the alternative is simply to kill them. It is good against one of several strong enemies of his own level and useless against a single superior one.""")

w('Dominate', """Dominate gives Cyrus control of an enemy that fails its save and turns it against its allies, and even a successful save costs the target an action. When it works on something dangerous, it reverses the fight.

The incapacitation trait restricts it to enemies of his level or lower, the target saves again every round, and mindless creatures are immune. It is a gamble, and an expensive one for someone with two slots at the rank.""")

w('Field of Razors', """Field of Razors creates damaging difficult terrain over a wide area. It hinders movement for a minute, but it takes a whole turn to cast, and Rust Cloud deals more damage from rank 4.""")

w('Flame Vortex', """Flame Vortex is a column of fire that must be sustained and steered and can be used only outdoors or under a high ceiling. Its damage is low for the rank, and Cyrus cannot spare the action to sustain it.""")

w('Frost Pillar', """Frost Pillar encases one enemy in ice on a failed save, leaving it restrained and off-guard. It has to be sustained, the ice can be broken, and a successful save merely moves the target a short distance. Skyglass Prison holds an enemy more reliably from rank 3.""")

w('Lignify', """Lignify does what Slow does, with a better result when the target fails. A successful save still costs the target an action for a round, so the spell is never wasted on a powerful enemy, and a failure keeps it slowed with a chance of removing it from the fight altogether. Cast without a Strike it reaches 120 feet.

The later saves have the incapacitation trait, so petrification is likely only for enemies of his own level. In a Spellstrike it must be compared with Slow, three ranks lower, which gives the same result on a successful save for far less. Lignify is worth casting when Cyrus has no better use for one of his highest slots against a creature of flesh.""")

w('Necrotize', """Necrotize deals void damage against Fortitude and leaves a lingering penalty. The damage is solid for the rank, and the random debilitation always adds something, whether a weakness, a penalty or a hindrance to movement.

It works only on living creatures, and Cyrus cannot choose which debilitation appears. Chain Lightning deals more against Reflex, so Necrotize is the choice when he wants the debilitation or when Fortitude is the target's weaker save.""")

w('Never Mind', """Never Mind cripples a spellcaster that fails its save and does almost nothing to one that succeeds. As it also has the incapacitation trait, it is too unreliable against the enemies whose spellcasting most needs to be stopped.""")

w('Phantasmal Calamity', """Phantasmal Calamity deals heavy mental damage over a very large area at extreme range, against Will. It is one of the few area spells that tests that save, which makes it valuable against crowds of physically strong creatures with weak minds, and it is a strong spell with which to open a fight.

The burst is too large for Expansive Spellstrike, and mindless creatures are immune. Cast without a Strike, it is his best area spell against enemies with poor Will.""")

w("Poltergeist's Fury", """Poltergeist's Fury raises a storm of debris around Cyrus that grows as he sustains it. It takes a full turn to begin and an action each round afterwards, and it endangers allies who fight beside him.""")

w('Purple Worm Sting', """Purple Worm Sting is a poison that deals heavy damage over several rounds if the target keeps failing Fortitude saves. Immunity and resistance to poison are common, and the damage arrives late, so better spells are available at every rank.""")

w('Repulsion', """Repulsion surrounds Cyrus with an aura that keeps enemies away from him. He fights by keeping enemies within his reach, so the spell works against his own purpose, although it might cover a retreat.""")

w('Spellwrack', """Spellwrack punishes an enemy for having spells in effect on it. Against an opponent protected by many spells it strips them away faster and hurts it in the meantime, and against anything else it does nothing.""")

w('Tangling Creepers', """Tangling Creepers slows everything in a vast area for ten minutes. That hampers the advance of a large force, but doing more than that takes a full turn and an action each round, and it is rarely worth one of his highest slots.""")

w('Vampiric Exsanguination', """Vampiric Exsanguination is a cone of heavy void damage that also gives Cyrus a large number of temporary Hit Points. Through Expansive Spellstrike the cone runs away from his allies, and against a group of living enemies it serves as both his area damage and his protection for the following round.

It harms only living creatures, and it targets Fortitude, the save that tough enemies pass most often. Within those limits it is one of the best cones at this rank for a fighter who expects to be hit.""")

w('Vibrant Pattern', """Vibrant Pattern dazzles whatever stands in it and can blind enemies that fail a Will save. It has to be sustained and has the incapacitation trait, so it is meant for groups of weaker enemies, against which Cyrus does better to spend his actions attacking.""")

w('Vitrifying Blast', """Vitrifying Blast is a cone that damages enemies, slows them and makes them brittle. Those that fail their saves lose an action and take extra damage from bludgeoning and sonic attacks, and even those that succeed are briefly weak to both. When his allies deal a great deal of bludgeoning damage, that weakness is worth as much as the spell's own dice.

The cone is short, so it rarely reaches more than two or three enemies, and the slowing depends on failed Reflex saves. It is a good spell when allies are able to exploit the weakness.""")

w('Wall of Metal', """Wall of Metal raises a tall metal wall. Wall of Force is stronger and Wall of Stone is larger and permanent, so this has little to offer beside them.""")

w('Zero Gravity', """Zero Gravity sets everything in a column adrift. It can leave melee enemies unable to act effectively, but it needs a full turn and an action each round, and it hampers his allies equally.""")

w('Awaken Entropy', """Awaken Entropy deals damage over time in a small area and takes a full turn to cast and an action each round to sustain. The return is far too low for a rank-6 slot.""")

w('Explosive Barrage', """Explosive Barrage creates one large burst and several small ones of mixed fire and sonic damage against Fortitude. Cast without a Strike it covers a scattered group well, and having two damage types makes resistance less of a concern.

Its several bursts cannot be placed through Expansive Spellstrike, so for Cyrus it is useful only on a turn spent at range, and Chain Lightning does the same work with no risk to allies.""")

w('Frozen Fog', """Frozen Fog is a cloud that damages enemies each round, slows them and makes them clumsy, and it lasts a minute without being sustained. On a group that has to stay where it is, the total damage is high and the penalties help his allies' attacks.

The fog conceals everything inside it, which hides the enemies from his own side as well, and it harms allies who enter. It is a sound opening spell against enemies holding a position.""")

w('Phantom Orchestra', """Phantom Orchestra deals sonic damage each time it is sustained. All of its value therefore depends on an action that Cyrus needs for recharging his Spellstrike.""")

w('Scrying', """Scrying lets Cyrus watch a particular creature from anywhere. It is the established means of finding an enemy, checking on a prisoner or learning what a rival is doing. It takes ten minutes to cast and the target gets a save, so it belongs on a scroll.""")

w('Utter Destruction', """Utter Destruction is a cone of two damage types that also deafens. Its damage is well below that of Vampiric Exsanguination and Chain Lightning at the same rank.""")

w('Missed Cue', """Missed Cue is the best Will spell Cyrus can prepare. It deals solid mental damage and frightens the target even on a successful save, and on a failure the target is also slowed for as long as it remains frightened, which costs it actions over at least two rounds. Damage, a weakened enemy and lost actions from a single Strike is as much as any spell at this rank offers.

It is a fear and mental effect, so mindless creatures and those immune to fear ignore it. Against any enemy that can feel fear, it deserves one of his highest slots.""")

w('Word of Revision', """Word of Revision is a reaction that undoes a disaster, either by letting an ally roll a failed save again or by leaving them standing after a blow that would have killed them. It works once a day for each creature, and it can prevent the worst single event of a fight.

It occupies one of his highest slots for something that may not happen. For a group facing an enemy with deadly effects that depend on saves, it is excellent protection.""")

w('Curse of the Toad Prince', """Curse of the Toad Prince turns its target into a toad for a minute on a failed save. Even on a success the target is sickened and drops what it is holding, which disarms an enemy that fights with a weapon, and few transformation spells do as much on a success.

It works only on humanoids and has the incapacitation trait, so it is meant for enemies of his level or lower. Against a humanoid of his own level it is very strong, and against anything else it does not apply.""")

w('Proximal Shift', """Proximal Shift is a teleport that knocks down the creatures Cyrus leaves and damages those he arrives beside. It moves him 60 feet without provoking anything and has a small effect at both ends.

It takes the place of a Spellstrike for the turn, and its effects are modest for a rank-6 slot. Dimensional Assault and Time Jump cover his movement at less cost.""")

# ───────────────────────── rank 7 ─────────────────────────
w('True Target', """True Target gives the benefit of Sure Strike to Cyrus and three allies for a single action. Each of them rolls a first attack against the chosen enemy twice and ignores concealment, which against a single powerful enemy raises everyone's chance of hitting, and of hitting critically, in the round that matters most. For his own Spellstrike it does everything Sure Strike does, without the ten-minute wait between uses.

It uses one of his highest slots, which would otherwise hold one of his hardest-hitting spells, and because it applies to one creature it is wasted against a crowd. In a fight against one dangerous enemy, with his allies ready to attack, it is the best single action he can take.""")

w('Frigid Flurry', """Frigid Flurry is a line that harms only enemies and carries Cyrus to its far end. Because it ignores allies he can send it straight through a melee in which both sides are mixed together, which no other line or cone allows. Its heavy damage is of two types, so resistance seldom stops it, and the movement at the end places him where he chooses without provoking reactions.

Through Expansive Spellstrike it covers the battlefield beyond his target, and no spell suits Sprinting Spellstrike better. It has no added effect. From level 13 it is the area spell he prepares before any other.""")

w('Beheading Buzz Saw', """Beheading Buzz Saw is a line of heavy slashing damage and persistent bleeding, with a small chance of killing outright. The bleeding is unusually severe and continues for rounds.

A successful save avoids all of it, with no half damage, and strong enemies usually succeed. Frigid Flurry is far more dependable, and creatures that do not bleed lose half of what this spell offers.""")

w('Eclipse Burst', """Eclipse Burst is a very large burst of cold and void damage at long range. It is far too large to use near his allies and cannot sensibly be placed through Expansive Spellstrike, so it belongs to a caster who stands well behind the fighting.""")

w('Telekinetic Bombardment', """Telekinetic Bombardment deals very heavy damage, knocks enemies down and can be cast in more than one shape. The line works with both Expansive and Sprinting Spellstrike and leaves the enemies that fail prone and off-guard, with rubble that slows whoever remains. With a range of 500 feet it is also a fine spell to open a fight.

It needs something large nearby to throw, which is not always available, and the knockdown depends on failed Reflex saves. Bludgeoning damage is almost never resisted. It is a strong alternative to Frigid Flurry when hindering the enemy matters more than sparing allies.""")

w('Comet Charge', """Comet Charge combines movement with a heavy hit on an attack roll. Cyrus flies up to 120 feet without provoking reactions and strikes with a choice of damage types, and the target is off-guard if he began above it. In a Spellstrike the damage is settled by his weapon's roll, so it is as reliable as his best attack spells and can be aimed at a known weakness.

It does nothing to hinder the target. Its value is that he can cross a long distance and make a full Spellstrike in the same turn, which would otherwise take him a round. It is a good use of one of his highest slots on a large battlefield.""")

w('Defy the Gods', """Defy the Gods weakens its target even on a successful save, leaving it drained and stupefied, which lowers its Fortitude, its Hit Points and its spellcasting together. Against divine spellcasters and creatures of the heavens or hells, it also protects Cyrus from their damage.

It adds no damage, and its effects take time to make a difference. It is a specialised spell for a known divine or unholy enemy and otherwise a poor use of a rank-7 slot.""")

w('Spell Riposte', """Spell Riposte is a reaction that attempts to turn a spell aimed at Cyrus back on its caster. When it works it both saves him and hurts the enemy. It depends on a counteract check, however, it does nothing against area spells, and it keeps one of his highest slots unused until the moment comes.""")

w('Contingency', """Contingency stores a spell that casts itself when a condition Cyrus has set is met, such as a teleport when he is badly hurt or a defensive spell when he is first attacked. It costs no action in the fight and cannot be forgotten in the moment.

It takes ten minutes to prepare and a rank-7 slot to hold a spell of rank 4 or lower, which is a high price to pay each day. A scroll read in the morning gives the same protection and leaves the slot free.""")

w('Duplicate Foe', """Duplicate Foe creates a weaker copy of an enemy that fights for Cyrus while he sustains it. A full turn to cast and an action each round is the same cost that rules out every summoning spell for him.""")

w('Energy Aegis', """Energy Aegis gives one creature resistance to almost every kind of energy for a whole day. It costs nothing during a fight and reduces every spell and breath weapon that hits, and over a long day that prevents a great deal of damage.

Its duration makes it ideal for a wand, since used each morning it never takes one of his slots. As a prepared spell it would occupy a slot of his highest rank that he needs for attacking, which is too much to give up.""")

w('Fiery Body', """Fiery Body turns Cyrus into living flame, immune to fire and stronger with fire spells but vulnerable to cold and water. Its aura rewards being touched, and he fights at reach, so its benefits do not match the way he fights.""")

w('Heaving Earth', """Heaving Earth sends a shockwave along the ground that pushes creatures in its path and strikes one target at the end. That is a moderate amount of control for one of his highest slots, and it falls far short of the line spells he already has.""")

w('Hungry Depths', """Hungry Depths creates a growing vortex that needs a full turn to cast and an action every round. Whatever damage it eventually deals, Cyrus cannot afford those actions.""")

w('Interplanar Teleport', """Interplanar Teleport carries the group between planes. A certain kind of adventure cannot happen without it, and it is useless in any other, so a scroll is appropriate when the journey requires it.""")

w('Lifewood Cage', """Lifewood Cage traps every creature in a large cube that fails its save, holding and protecting them at once. It can remove half an encounter for a minute.

It takes a full turn and an action each round, enemies that succeed are simply moved outside, and the bars shelter those inside from his allies' attacks as well. Wall of Stone divides a fight more reliably.""")

w('Mask of Terror', """Mask of Terror protects its target by frightening attackers. Each creature that tries to harm the target must save or become frightened, and may lose the action entirely. On whichever ally the enemy is concentrating on, it weakens a good share of the attacks against them for a minute.

It depends on failed saves, each creature is affected only once in a round, and mindless enemies ignore it. It is a reasonable first casting on an ally in melee when Cyrus cannot yet reach the enemy.""")

w('Momentary Recovery', """Momentary Recovery is a teleport with a pause during which Cyrus can act on himself. It gives him a moment to drink a potion or cast a personal spell out of harm's way, but Translocate moves him further for less.""")

w('Planar Palace', """Planar Palace provides a secure demiplane in which to rest until the next day. It guarantees an undisturbed night in hostile country, and it is a scroll for expeditions.""")

w('Planar Seal', """Planar Seal blocks teleportation and planar travel across a wide area for a day. It matters against enemies that arrive or escape by magic, and only then.""")

w('Power Word Blind', """Power Word Blind blinds its target for one action with no save. An enemy near his level is blind for minutes, which all but removes it from the fight, and because the spell takes one action, Cyrus still has room for a full Spellstrike in the same turn.

Its strength depends entirely on the target's level, and much stronger enemies are only dazzled. Against enemies of his level or slightly above, it is one of the most efficient actions he can take with one of his highest slots.""")

w('Prismatic Armor', """Prismatic Armor gives resistance to seven damage types for a minute, with a chance of dazzling attackers. On whoever is taking the most damage, it prevents a great deal in a fight with several kinds of energy. Energy Aegis gives similar protection for a whole day from a wand.""")

w('Prismatic Spray', """Prismatic Spray is a cone of random effects, some of them devastating. It can petrify, confuse or slow, or simply deal heavy damage, and each creature's result is rolled separately.

That randomness is the difficulty for someone with two slots at the rank, because Cyrus cannot count on the result he needs. Frigid Flurry deals a known amount of damage where he wants it.""")

w('Project Image', """Project Image lets Cyrus cast from an illusory double. His spells are carried by his weapon, so a double that cannot Strike adds little.""")

w('Reverse Gravity', """Reverse Gravity throws every creature in a wide column up to the ceiling and holds it there for a minute. Enemies that cannot fly are out of the fight or badly out of position, and most of the effect allows no save.

It takes a full turn to cast and affects allies in the area. Used from range on the enemy's formation in the first round, it is among the strongest control spells Cyrus can cast.""")

w('Retrocognition', """Retrocognition gives impressions of what has happened in a place, reaching back years if enough time is spent. In an investigation it can answer questions that nobody living can, and it belongs on a scroll.""")

w('Shadow Raid', """Shadow Raid deals area damage that harms only enemies, in a type Cyrus chooses, and it continues to hurt those who stay in the area. Because allies are safe, he can place it directly on a melee, which is rare for a large burst.

It takes a full turn to cast, the damage each round is moderate for the slot, and the enemy uses whichever of two saves is better for it. It is worth casting when the two sides are thoroughly mixed and he cannot find an angle for a line.""")

w('Time Beacon', """Time Beacon gives Cyrus a second attempt at a turn for one action. Cast first, it lets him undo a missed Spellstrike, a poor damage roll or a move that went wrong and take the turn again. When a turn depends on a spell of his highest rank and a single attack roll, that protection is worth a great deal.

It uses a high slot and an action that might have gone to Sure Strike or True Target, which improve the chance of success where Time Beacon only guards against failure. It is best kept for the one turn in a fight that has to succeed.""")

w('Vacuum', """Vacuum suffocates the creatures around Cyrus. It has the incapacitation trait, it must be sustained, and it endangers allies as much as enemies, so nothing about it suits him.""")

w('Warp Mind', """Warp Mind confuses its target for a minute with no further saves, or permanently on a critical failure. Because of the incapacitation trait it is meant for enemies of his level or lower, against which it is a strong spell, and it will not take hold on a superior enemy.""")

w('Incarnate Tempest of Shades', """Incarnate Tempest of Shades takes a full turn to summon a manifestation that drains enemies as it arrives and frightens them as it leaves. It deals no damage, and both effects need failed saves. A magus gives up too much in order to cast it.""")

w('Puppet Strings', """Puppet Strings gives Cyrus control over an enemy's movements and some of its attacks if it fails its save, and imposes a mild penalty if it succeeds. It has the incapacitation trait and has to be sustained, so it works on lesser enemies and costs him his own damage while it lasts.""")

w('Spell Turning', """Spell Turning is a ward lasting an hour that gives Cyrus one attempt to reflect a spell targeted at him. It can be cast before a fight against a known enemy spellcaster, which is its advantage over Spell Riposte. It still depends on a counteract check and uses his reaction.""")

# ───────────────────────── rank 8 ─────────────────────────
w('Arctic Rift', """Arctic Rift is a long line that targets Fortitude, which gives Cyrus a spell for Sprinting Spellstrike against enemies that dodge everything else. The damage is very heavy, each enemy that fails its save loses an action, and a critical failure freezes it in place.

Large, tough creatures pass Fortitude saves more often than not, so the lost action is least likely where it would matter most, and half damage is the usual result against them. It is the right line against agile enemies and against groups of mixed kinds. Frigid Flurry is still safer in a crowded melee, because it does not harm allies.""")

w('Disappearance', """Disappearance makes Cyrus invisible for ten minutes in a way that defeats every precise sense and does not end when he attacks. Every Strike he makes in that time is against an off-guard target, so Laughing Shadow's extra damage applies throughout, and enemies must guess which square he is in before they can even try to hit him. No other defensive spell he can cast prevents as much damage.

It lasts long enough to be cast before a fight, which means it costs no action during one. Enemies with reliable ways of finding unseen creatures reduce its value. Even with Dimensional Disappearance available, it is worth one of his highest slots for an important fight, and he can give it to an ally instead.""")

w('Quandary', """Quandary removes one enemy from a fight with no saving throw at all. The target is shut in a puzzle room until it reasons its way out against his spell DC, which usually takes a few rounds, and during that time his allies fight everyone else without interference.

The spell has to be sustained, which takes the action he would use to recharge each round, and the enemy returns unharmed. It is therefore a means of dividing a fight: the strongest enemy is removed, the others are finished, and then everyone faces it together. For that purpose nothing at this rank is as certain.""")

w('Roar of Freedom', """Roar of Freedom achieves more for one action than any other spell Cyrus can prepare. It deals heavy damage to every enemy around him, weakens those that fail their saves and gives his nearby allies temporary Hit Points, and it still leaves him two actions for a full Spellstrike in the same turn.

It harms only enemies, so the middle of a melee is the best place to cast it. The weakening needs failed Will saves, but the damage and the temporary Hit Points do not depend on them. From level 15 it deserves one of his highest slots in any fight where he expects to be surrounded.""")

w('Desiccate', """Desiccate deals heavy void damage to any number of living creatures Cyrus chooses, at up to 500 feet. Because he selects the targets it is completely safe for allies, and it can reduce an entire enemy force before the two sides meet.

It cannot be put into a Spellstrike, and it does nothing to creatures that are not alive or that contain no moisture, so it is for a turn spent at range. Chain Lightning does similar work two ranks lower against any kind of creature.""")

w('Uncontrollable Dance', """Uncontrollable Dance leaves an enemy off-guard, unable to use reactions and forced to waste an action each turn for three rounds, even when it succeeds at its save. That is a remarkable amount to gain from a successful save: it gives Cyrus Laughing Shadow's extra damage, frees all his allies from the enemy's reactions and costs the enemy a third of its turns.

It has the incapacitation trait, so a higher-level enemy treats a success as a critical success and is unaffected, and mindless creatures are immune. Against an enemy of his level or lower it is one of the strongest spells there is, and against a superior one the slot is wasted.""")

w('Falling Sky', """Falling Sky throws everything in a very large column to the ground, leaving it prone even on a successful save, and brings flying creatures down with heavy damage. Against one flying enemy or many, it settles the matter, and a prone group is off-guard to everyone on his side.

Its stun has the incapacitation trait, and the column is too large to use near allies. Cast without a Strike against airborne enemies, it is better than anything else Cyrus has.""")

w('Boil Blood', """Boil Blood deals fire damage against Fortitude and has a large second effect on a failed save: the target is drained 2, which removes two further Hit Points for each of its levels and lowers its later Fortitude saves. A failed save therefore produces one of the heaviest single-target results at this rank, and the spell is simple to use in a Spellstrike.

On a success it deals half the fire damage with no drain, and strong enemies pass Fortitude saves more often than not. Polar Ray, whose drain needs only the Strike to hit, is therefore the more reliable of the two. Creatures without blood are immune, and fire is commonly resisted. Boil Blood is the choice when Fortitude is the target's weaker save.""")

w('Confusing Colors', """Confusing Colors is a cloud that dazzles widely and confuses or stuns those that fail their saves. It has to be sustained and has the incapacitation trait, so it is a spell for crowds of lesser enemies, cast by someone who can afford the action each round.""")

w('Dream Council', """Dream Council holds a meeting in a shared dream for up to twelve people, wherever they are. It is useful for coordinating distant allies and has no bearing on a fight.""")

w('Earthquake', """Earthquake shakes a vast area, imposing penalties, opening fissures and bringing down structures. Its size makes it nearly impossible to use without including his allies, and its effects depend heavily on the terrain.""")

w('Hidden Mind', """Hidden Mind protects one creature for a day against mental effects and magical spying. Against an enemy that dominates or reads minds it protects the person most at risk, and a scroll bought for that day is enough.""")

w('Pinpoint', """Pinpoint tells Cyrus exactly where a creature or object is, wherever it may be, which ends a search at once. It takes ten minutes to cast and belongs on a scroll.""")

w('Power Word Stun', """Power Word Stun stuns its target for one action with no saving throw. Even the strongest enemy loses an action, and one of his level or a little above loses a whole round or more. Nothing else lets Cyrus take an action from a single powerful enemy with certainty and still Spellstrike in the same turn.

It works once on each target in a fight. Against one dangerous enemy, a magus could hardly find a better use for one of his highest slots.""")

w('Prismatic Wall', """Prismatic Wall harms and hinders anything that tries to pass through it, and it lasts an hour. As a barrier it is almost absolute. It takes a full turn to cast, however, and it blocks his own allies' attacks as well.""")

w('Rainbow Fumarole', """Rainbow Fumarole produces a column of random fire effects after a full turn of casting. It is both unreliable and slow.""")

w('Unrelenting Observation', """Unrelenting Observation lets several people track one creature or object perfectly. It is a specialised spell for a pursuit or for surveillance.""")

w('Whirlpool', """Whirlpool is a spell for a fight against many enemies, cast from well outside it. Its area is large enough to hold most of an encounter, and all of it is difficult terrain. Each time Cyrus sustains it the damage is repeated and creatures that fail are dragged back towards the middle, so enemies are hurt again in every round they spend getting out. By the second round of sustaining it has dealt more than a single area spell of the rank would.

Its cost is in actions. It takes a whole turn to cast, which rules out a Spellstrike, and each round of sustaining uses the action he would spend recharging. It also damages allies, so it has to be cast before the two sides meet. It is worth preparing when a large group is expected and he can open the fight from range, and Arctic Rift serves better once the fighting is at close quarters.""")

w('Sudden Transposition', """Sudden Transposition moves enemies to any point within 60 feet of Cyrus and deals solid damage to those that fail their saves. Cast without a Strike it affects two creatures, so he can pull an archer and a spellcaster into his reach or throw two dangerous melee enemies away from his allies, and the movement alone can decide a round. In a Spellstrike it affects only the creature he strikes, which is still enough to send a dangerous enemy to the far side of the fight after the hit.

Nothing happens on a successful Fortitude save, and Fortitude is the strong save of most large enemies. The spell is most useful when the enemy's position is the difficulty and the target is not especially hardy.""")

w('Incarnate Archmage', """Incarnate Archmage takes a full turn and returns light damage and some disruption of enemy magic. That is far too little for a rank-8 slot and three actions.""")

w('Take Your Places', """Take Your Places teleports up to four allies to any points within 60 feet. In one casting his side can surround an enemy, leave a trap or get its wounded clear, and no one provokes a reaction in doing so.

It moves only the willing and does nothing to the enemy directly. It is valuable when his allies plan around position and expensive at this rank otherwise.""")

w('Polar Ray', """Polar Ray is the strongest attack spell at this rank against a single powerful enemy, once its drain is counted. A hit deals moderate cold damage and leaves the target drained 2 with no save, which removes two further Hit Points for each of its levels and lowers its Fortitude saves for the rest of the fight. Against a creature of level 15 or higher that amounts to more in total than Blood Feast or a heightened Briny Bolt deals, and it makes Slow, Arctic Rift or Weight of the World more likely to succeed afterwards.

The drain is not doubled on a critical hit and does not accumulate, so a second casting on the same enemy adds only the cold damage. Constructs and other creatures immune to the drained condition take the cold damage alone. One casting, kept for the day's most dangerous enemy, is the best use of it.""")

w('Metallic Meteorite Glyph', """Metallic Meteorite Glyph deals very heavy bludgeoning damage against a basic Reflex save, in a type almost nothing resists. Its two-action form is simple and strong in a Spellstrike, and half damage on a successful save keeps it worthwhile.

The slower castings that add targets do not fit his turn. Chain Lightning heightened to the same slot is comparable and more flexible, so the Glyph is a good choice when electricity is resisted.""")

w('Foresight', """Foresight protects one person for an hour. With his reaction, Cyrus can make that ally roll a save twice, or make an enemy roll twice and take the worse result on an attack against them. Over a fight that prevents several of the worst outcomes, and an hour often covers both of a day's encounters.

Each use takes his reaction, which he also wants for Reactive Strike, and the spell occupies one of his two highest slots. It is strong when cast on himself, and may be stronger on his side's healer or its most fragile member. It costs no action once a fight has begun, which is the main reason it is rated so highly.""")

w('Remake Physiology', """Remake Physiology is the heaviest penalty Cyrus can impose on an enemy. A living target is slowed in its movement and made worse at attacking, defending, casting and seeing, all at once, and it suffers a round of this even on a successful save. On a failure the effects last for the fight, and everything his allies then do to that enemy is easier.

The spell needs a touch, which a Spellstrike extends to his reach, and it adds no damage. Cast on a single powerful enemy at the start of a fight, it is worth more than any damage spell in the same slot.""")

# ───────────────────────── rank 9 ─────────────────────────
w('Falling Stars', """Falling Stars creates four very large bursts of mixed damage anywhere within 500 feet. It covers an entire battlefield and lets Cyrus choose the energy type. Because it consists of several bursts it cannot be put into a Spellstrike, and it is too large to use near allies, so it is a spell for open battle, cast from a distance.""")

w('Phantasmagoria', """Phantasmagoria deals heavy mental damage to as many creatures as Cyrus chooses, removes their reactions even on a successful save and confuses those that fail. Because he selects the targets it is safe in any melee, and when a whole enemy force cannot react for a round, his allies can act with complete freedom.

It is cast without a Strike and is a mental effect, so mindless enemies ignore it. Of the area spells of his highest rank, it is the one he can use wherever his allies happen to be standing.""")

w('Dimensional Excision', """Dimensional Excision deals very heavy damage of no particular type, with severe bleeding, against Will. It lacks the mental trait, so almost nothing is immune, and half the damage still applies on a successful save. Creatures away from their home plane find the save much harder.

It does nothing to hinder the target. As damage alone, it is the most widely usable spell Cyrus has for his highest slot.""")

w('Implosion', """Implosion deals a large fixed amount of damage to one target, and then to a new target in each round it is sustained. The first hit can be delivered in a Spellstrike. The later ones take the action Cyrus uses to recharge, and no creature can be affected twice. The total against a group is good, but it disrupts the alternation of Spellstrike and recharge on which his turns depend.""")

w('Massacre', """Massacre is a line that kills weaker creatures outright and deals heavy damage to the rest, and if nothing dies it turns on Cyrus himself. Against a column of lesser enemies it is devastating, and against anything near his own level it puts his own Hit Points at risk.""")

w('Bilocation', """Bilocation gives Cyrus a second body for ten minutes. He can act from whichever body is better placed, both move when one moves, and between them they cover twice the ground with his reach and Reactive Strike. That makes flanking easy and lets him threaten two parts of a fight at once.

The two bodies share his Hit Points and conditions, so an area effect that covers both harms him only once, but an attack on either harms him. The spell lasts long enough to be cast beforehand. For a fighter who relies on position it is a strong and unusual use of one of his highest slots.""")

w('Detonate Magic', """Detonate Magic counters a spell or magic item and turns it into an explosion. It depends on a counteract check and on the enemy having magic worth destroying, and Dispel Magic on a scroll does the essential part.""")

w('Magnetic Dominion', """Magnetic Dominion moves every armoured or metallic creature within 100 feet wherever Cyrus wishes. Against an armoured force the effect is spectacular. It takes a full turn to cast and an action each round, and it does nothing to anything not made of metal or wearing it.""")

w('Power Word Kill', """Power Word Kill slays a weaker enemy with no save and removes a large fixed number of Hit Points from a stronger one, all for a single action. Against a powerful enemy that is damage that cannot fail and that leaves two actions for a Spellstrike, which no other spell of his highest rank offers.

It works once on each target. Whether used to finish an enemy that is already hurt or as a certain first blow, it is among the best uses of his highest slot.""")

w('Prismatic Sphere', """Prismatic Sphere surrounds a small space with a seven-layered shell that is nearly impassable for an hour. It protects a fixed position superbly, but it keeps Cyrus in one place, which is not how he fights.""")

w('Resplendent Mansion', """Resplendent Mansion provides a grand and secure dwelling until the next day. It gives the group comfort and safety between adventures and has no effect on a fight.""")

w('Telepathic Demand', """Telepathic Demand sends a message with a suggestion attached to someone Cyrus has contacted before, wherever they are. It serves intrigue at long range, with the incapacitation trait and a full turn of casting as its limits.""")

w('Unspeakable Shadow', """Unspeakable Shadow causes fear that also costs the target actions. Even on a successful save the target is frightened and must spend an action each turn dealing with its own shadow, and on a failure the fear does not fade. Against a single enemy it both weakens it and steadily reduces what it can do in its turns.

It is a mental and fear effect, so the usual immunities apply. Remake Physiology weakens a target in more ways, and Unspeakable Shadow is the better choice when taking away actions matters most.""")

w('Incarnate Draconic Legion', """Incarnate Draconic Legion takes a full turn and produces a line and a cone of heavy damage that cannot overlap. The damage is considerable, but Frigid Flurry in a Spellstrike does comparable work and leaves Cyrus the rest of his turn.""")

w('Prismatic Shield', """Prismatic Shield protects Cyrus for one round at the cost of one action. Melee attackers suffer random prismatic effects, arrows are stopped and spells aimed at him may be turned aside. On a turn when he expects the enemy's full attention it prevents a great deal and still leaves two actions for a Spellstrike.

It lasts a single round and uses his highest slot, so it is best kept for the round in which a powerful enemy turns on him.""")

w('Forest of Gates', """Forest of Gates carries the group up to 1,000 miles in an hour's walk, and the walk restores Hit Points and reduces the doomed and drained conditions as a night's rest would. Arriving at the intended place depends on a DC 40 Arcana or Nature check, which Cyrus usually makes with Arcana, and even a failure leaves the group within 10 miles of it.

It does not restore spells, and Teleport covers the same distance from a rank-7 slot. It is a travel spell that takes his highest slot, for a day on which no fight is expected.""")

w('Weird', """Weird deals heavy mental damage to any number of chosen creatures and frightens them, with a chance of death on a critical failure. It is safe for allies and frightens even those that succeed at their saves.

Phantasmagoria deals the same damage and removes reactions instead, which usually helps his allies more. Both are fear or mental effects with the same immunities, so there is no reason to know both.""")

# ───────────────────────── occult spells ─────────────────────────
w('Guidance', """Guidance is the best cantrip to take with Witch Dedication. One action adds a point to the most important roll an ally makes that round, or to his own Spellstrike, and it asks nothing else of his turn, so it suits the third action Cyrus so often has left over. Each creature can benefit only once an hour, which means it should be kept for the roll that matters most.""")

w('Forbidding Ward', """Forbidding Ward gives one ally a small, lasting bonus to AC and saves against one enemy. Against a single dangerous enemy it protects whoever that enemy is attacking for the whole fight. It takes two actions to cast and another each round to sustain, which is more upkeep than Guidance needs and takes the action Cyrus uses for recharging.""")

w('Haunting Hymn', """Haunting Hymn is a short cone of weak sonic damage against Fortitude. His arcane cantrips already deal damage better than this, so the cantrip gained from the dedication is better used for support.""")

w('Wash Your Luck', """Wash Your Luck cancels a misfortune effect on one later roll. Misfortune effects are rare enough that the cantrip would go unused in most fights.""")

w('Know the Way', """Know the Way tells Cyrus which way is north and where he last was. It is a convenience during exploration and nothing more.""")

w('Read the Air', """Read the Air is a social cantrip that gives a quick impression of a room and a small bonus to making a good first impression, which supports the scenes in which Cyrus does the talking. Guidance helps in more situations, so this is the second choice for the dedication's cantrip.""")

w('Soothe', """Soothe is healing at range that Cyrus can cast from a scroll or wand once the dedication gives him access to occult spells. It lets him revive a fallen ally when his side's healers are occupied or down. The amount healed is modest, so it is for emergencies, and a wand provides one such rescue each day.""")

w('Bless', """Bless gives his allies a small bonus to attacks within an aura around Cyrus. He fights in the middle of his allies, so the aura would be well placed, but it costs two actions at the start of a fight, and a divine caster among his allies does it better. A scroll is the most it deserves.""")

w('Bane', """Bane imposes a small penalty on the attacks of enemies near Cyrus if they fail a Will save. The effect is slight and depends on that failure, and Fear does more to one enemy with certainty.""")

w('Sanctuary', """Sanctuary makes enemies succeed at a save before they can attack the protected creature. It is at its best on a fallen or fragile ally who will not be attacking, because it ends if the target fights. That makes it useful from a scroll during a rescue.""")

w('Protection', """Protection adds a point to AC and saves for a minute. That is a small benefit for two actions. Used from a wand before a fight Cyrus knows is coming, it is a fair use of the wand, but during combat the actions are worth more.""")

w('Liberating Command', """Liberating Command takes one action and gives a grabbed or restrained ally an immediate attempt to break free. It is cheap and occasionally vital against enemies that grapple, and a scroll or wand covers the need.""")

w('Ill Omen', """Ill Omen makes one enemy roll its next attack twice and take the worse result, but only if it fails a save. Nothing happens on a success, and against a capable enemy that is the usual outcome.""")

w('Lose the Path', """Lose the Path is a reaction that spoils an enemy's Stride, which can stop a charge short of its target. It uses the reaction Cyrus keeps for Reactive Strike, and an enemy moving past him is the very thing Reactive Strike punishes.""")

w('Phantom Pain', """Phantom Pain deals light mental damage and leaves a lingering sickness if the target fails its save. The damage is poor and the sickness depends on that failure, whereas Goblin Pox from his own list sickens even on a success.""")

w('Spirit Link', """Spirit Link moves Hit Points from Cyrus to an ally each round for ten minutes. As someone who fights at the front he usually needs his own, although it could help to keep a fragile ally standing between fights.""")

w('Calm', """Calm stops a group from fighting if its members fail their saves. It can end a brawl or pacify guards without bloodshed, which suits a negotiator. It has the incapacitation trait and has to be sustained, so it works on lesser opponents.""")

w('Silence', """Silence makes one willing creature soundless, and from rank 4 it silences an area. For stealth it removes the noise of armour, and the area version prevents enemy spellcasters standing in it from casting most spells. A scroll serves for infiltration, and a rank-4 scroll for a fight against a spellcaster.""")

w('Clear Mind', """Clear Mind counters fear and the stupefied condition on an ally, and stronger mental conditions from higher slots. On a day when an enemy controls or confuses his allies it is the remedy, and it belongs on a scroll.""")

w('Cleanse Affliction', """Cleanse Affliction eases or removes a curse, disease or poison. Those are matters for after a fight, and a divine caster among his allies normally deals with them, so a scroll is enough as a reserve.""")

w('Sure Footing', """Sure Footing counters conditions that hinder movement, such as clumsy, grabbed and paralysed, and more from higher slots. A paralysed ally is one hit away from disaster, so a scroll is worth carrying against enemies that paralyse.""")

w('Paranoia', """Paranoia makes one enemy distrust everyone, which may turn it against its own side. The useful result needs a failed save, and the effect is hard to direct.""")

w('Augury', """Augury gives a vague answer about a course of action over the next half hour, which can settle a debate about which door to open. It takes ten minutes to cast and is worth a scroll at most.""")

w('Spiritual Armament', """Spiritual Armament is a spell attack that deals spirit damage and can be repeated by sustaining it. In a Spellstrike it would be settled by his Strike's roll, but his arcane spells deal more, and sustaining it takes the action he uses to recharge.""")

w('Status', """Status tells Cyrus where an ally is and how they are faring for a whole day. That is useful when the group separates, and a wand makes it routine.""")

w('Heroism', """Heroism gives a bonus to attacks, saves and skills for ten minutes. Cast on himself before a fight, it makes every Spellstrike a little more likely to hit and to hit critically, and it lasts long enough to cost no action in combat. Once he has the dedication, a scroll or wand of Heroism is one of the better things he can buy.""")

w('Hypercognition', """Hypercognition allows up to six Recall Knowledge checks for a single action. Cyrus is his side's main source of information about enemies, and learning a creature's weakest save and its resistances in the first round shapes every spell he chooses afterwards. A wand of it is an excellent purchase.""")

w('Defensive Prescience', """Defensive Prescience is a reaction that protects a familiar from an attack. It matters only if the familiar from Witch Dedication is at risk, which Cyrus can avoid by keeping it out of fights.""")

w('Begone', """Begone takes one action and hurls an enemy backward if it fails a Fortitude save. It can remove an enemy from an ally or send it over an edge, but it needs that failure, and large enemies seldom fail.""")

w('Strength of Mind', """Strength of Mind gives a bonus against mental effects and effects that hinder movement for one action. Cast before meeting an enemy that charms or frightens, it supports a weak save, and it belongs on a scroll.""")

w('Focusing Hum', """Focusing Hum helps stupefied spellcasters and steadies confused allies near Cyrus while he sustains it. Its use is too narrow, and the action to sustain it is costly.""")

w('Infectious Melody', """Infectious Melody forces enemies to sing when they speak. That hampers their coordination slightly and does little else.""")

w('Tortoise and the Hare', """Tortoise and the Hare slows an enemy for a round even on a successful save, and on a failure it also quickens Cyrus or an ally, so it amounts to Slow with an additional benefit. From a scroll it is a strong opening against a single enemy, although Slow from his own slots gives the same result on a successful save.""")

w('Read Omens', """Read Omens gives a cryptic hint about an event in the coming week. It suits a story more than it helps in practice.""")

w('Honeyed Words', """Honeyed Words gives a large bonus to Lie for ten minutes. For the one who speaks for the group during an infiltration or a tense deception it can carry a whole scene, and a scroll covers the day it is needed.""")

w('Synesthesia', """Synesthesia is one of the strongest weakening spells in the game, and it belongs to the occult list. The target is easier to hit and slower, struggles to target anyone and may lose its spells, and it suffers a round of all this even on a successful save.

Cyrus can use it only from a scroll or from the stave, so it costs two actions and cannot be combined with a Strike. Against a single powerful enemy at the start of a fight, that turn is well spent.""")

w('Strange Geometry', """Strange Geometry creates illusory terrain that slows those who believe in it, and it takes a full turn to cast. That is weak control at a high cost.""")

w('Inevitable Disaster', """Inevitable Disaster deals a large fixed amount of damage after a delay of a few rounds. The delay makes it hard to plan around, and from a scroll it cannot be combined with a Strike.""")

w('Death Ward', """Death Ward gives resistance to void damage and protection against death effects for ten minutes. Against undead and enemies that use such magic, it protects the member of the group most at risk, and it is a scroll for those days.""")

w('Shadow Blast', """Shadow Blast offers a choice of damage type and of area shape in one spell, although each target uses the better of two saves. As an occult spell Cyrus could cast it only from a scroll, without a Strike, and in that situation his own area spells serve better.""")

w('Zealous Conviction', """Zealous Conviction gives the whole group temporary Hit Points and a bonus against mental effects for ten minutes. Cast before a fight, it is a meaningful protection for everyone, and it is a scroll for an encounter known to be hard.""")

w('Scintillating Safeguard', """Scintillating Safeguard is a reaction that gives up to five allies resistance against one damaging effect. Against a breath weapon or a large area spell it prevents a great deal at once. It requires a scroll in hand at the right moment, however, which is awkward for someone who fights with both hands on his weapon.""")

w('Spirit Blast', """Spirit Blast deals heavy spirit damage to one creature, which harms incorporeal enemies that are barely affected by most attacks. From a scroll it can only be cast without a Strike. It is worth carrying for a fight against a powerful spirit.""")

w('Blanket of Stars', """Blanket of Stars gives a bonus to Stealth, and invisibility for as long as Cyrus stays still under an open night sky. It is useful for little beyond ambushes outdoors.""")

w('Ethereal Jaunt', """Ethereal Jaunt gives a minute on the Ethereal Plane, passing through walls and past guards unseen. For scouting and infiltration almost nothing can stop it. It has to be sustained, and Cyrus cannot affect the material world while he is there, so it is a scroll for a planned intrusion.""")

w('Visions of Danger', """Visions of Danger fills an area with illusory monsters that deal mental damage each round. It takes a full turn to cast, and enemies who disbelieve the illusion are unharmed.""")

w('Orb of Twisting Fate', """Orb of Twisting Fate makes an enemy waste an action each turn if it fails its save. It does little on a success and has a very short range.""")

w('Spirit Song', """Spirit Song is a long cone of spirit damage that prevents reactions on a failed save, and it harms incorporeal creatures. From a scroll Cyrus can cast it only without a Strike, and his own cones do more when combined with one.""")

w('Spiritual Epidemic', """Spiritual Epidemic is a lasting curse that weakens and stupefies its victim and spreads to those who cast divine or occult spells on them. It needs a failed save and suits one very particular kind of enemy.""")

w('Overwhelming Presence', """Overwhelming Presence forces any number of creatures to spend actions paying Cyrus tribute, with some effect even on a successful save. Against a crowd it wastes a great many enemy actions. It has the incapacitation trait, so the strongest enemy present is the one least affected.""")

w('Unfathomable Song', """Unfathomable Song imposes random penalties on up to five enemies in each round it is sustained. It has the incapacitation trait, and sustaining it takes the action Cyrus uses to recharge.""")

w('Gentle Breeze', """Gentle Breeze heals the whole group slowly over ten minutes and gives a bonus to Medicine in its area. Between fights it restores everyone without using any daily resource other than the wand itself, which makes it one of the best wands Cyrus can carry once he has the dedication.""")

w('Sound Body', """Sound Body removes blindness, deafness, sickness, weakness or the dazzled condition from an ally. When an important ally is blinded in the middle of a fight, a scroll of it puts that right, so one is worth carrying.""")

w('Shock to the System', """Shock to the System brings back someone who died within the last round, heals them and quickens them. Undoing a death is worth almost any price, and this does it for two actions without a ritual. Once Cyrus can use occult scrolls, a scroll of it is the best protection his side can carry, and a wand is better still.""")

