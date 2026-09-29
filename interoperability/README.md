---
title: "Ability and class interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
---

# Ability and class interoperability

How every ability and spell in the V8.08 "Spongy" rulebook relates to the classes: who has it, at what level, who it works on, what stops it, and which other abilities name it. Built to answer questions such as *what happens if this ability moves from 4th to 6th level*.

## Files

- [`abilities/`](abilities/): one file per ability (179 files). Start here for a specific spell.
- [`classes/`](classes/): one file per class (12): level list, what the class is immune to, what its abilities do to every other class.
- [`MATRIX.md`](MATRIX.md): every targeting ability against all 12 classes on one page.
- The interactive version is `viewer/ability-chords.html` (chord diagram).

## The model

- **Nodes:** one per (class, ability) pair on a class list. The four Magic User classes come from their spell tables, the eight martial classes from their level tables. That gives 220 pairs covering 141 distinct abilities.
- **Assumptions:** every class is 6th level and has every ability on its list, including every option of a "Pick one" group. Archetypes, spell points, purchase limits and the Equipment traits are ignored.
- **Look The Part:** each martial class also gets one ability from 1st level (Anti-Paladin Terror, Archer one arrow, Assassin Poison or Poison Arrow, Barbarian Rage, Monk Heal, Paladin Awe, Scout Heal, Warrior Insult), and a Magic User gets one extra magic point at their highest level (six at 6th level). The level in the class table is when the class earns the ability normally; Look The Part can give it earlier.
- **Can affect another player:** a Verbal or Enchantment whose range (for that class) is Other, Touch, 20', 50' or Unlimited, or any Magic Ball or Specialty Arrow. Traits and Self-only abilities cannot. 156 class-list entries qualify. Self-range abilities that grant another ability (for example Snaring Vines granting Hold Person) are not counted as targeting, but their file says what they grant.
- **Blocked** means the target class cannot be affected, for one of two reasons:
  - the ability's School is one the target class is Immune to: Anti-Paladin (Command, Flame), Barbarian (Command, Subdual), Paladin (Command, Death);
  - the target is a Monk and the ability is a Verbal Magical ability used beyond Touch (Enlightened Soul). The Monk is still affected if the ability is cast at Touch, and (ex) abilities are never stopped. Martial abilities are Magical only when their class table marks them (m); all Magic User abilities are Magical. Dispel Magic and Sever Spirit say they work "regardless of the player's Traits". This model reads that as overriding Enlightened Soul for the Enchantment removal (Dispel Magic works on a Monk; Sever Spirit is partly blocked because the Curse is not covered). That is a reading of the rule text, not an official clarification, so their files say so.
- **Enchantments ignore Immunities.** The rulebook says Immunities, Traits and other Enchantments do not prevent new Enchantments (Enchantments rule 3), and effects imparted directly by the enchantment still work. So Enchantments of an immune School (Poison, Flame Blade, Toxic Blades and the like) are shown as working. Abilities the enchantment grants are still subject to Immunity (rule 3b), which is why Undead Minion is only partly blocked on a Paladin.
- **Equipment is not protected.** Immunities and Enlightened Soul protect the player, not carried equipment or worn armor (Immune rules 2 and 4, and the Notes on Pyrotechnics, Destroy Armor, Heat Weapon and Shatter Weapon). So Pyrotechnics, Destroy Armor and Shatter Weapon are shown as working on immune classes; Heat Weapon works on a Monk but not on an Anti-Paladin (a Flame-Immune player may keep wielding the weapon).
- **Partly blocked (◐):** the player is unaffected but something still lands. Fireball and Lightning Bolt still hit an Anti-Paladin's equipment, and a Poison Arrow still counts as a normal arrow hit on a Paladin (Specialty Arrows rule 5).
- **Works** is everything else. Monk Missile Block (an active block of arrows and Magic Balls) is not counted as a block. Touch and Other range abilities (Other means Touch range) also need the target to be willing, dead, stunned, frozen or Insubstantial and unable to move; and Enchantments may only be cast on willing players. Those apply to every class equally and are not modelled.
- **Temporary defenses are out of scope**, for example Barbarian Rage (unaffected by Verbal abilities while it lasts), the Invulnerable and Insubstantial States, Circle of Protection and Sanctuary. So is Enlightened Soul or Song of Interference given to a non-Monk. Only permanent class Traits count.
- **Shared** means the same ability appears on more than one class list.
- **Connected** abilities come from automatic text matching: an ability that names another in its Effect, Limitations or Note. The relation is guessed from the wording (grants after "Gain" or "may cast", removes after "Lose", replaces, changes its numbers after "becomes", borrows after "as per", otherwise mentions). Treat these as pointers to read, not rulings.

## Answering "what if we move this ability to another level?"

1. Open `abilities/<name>.md`. **Where it is listed** shows every class that has it and its level, cost, max and frequency there, and flags Look The Part.
2. **Effect on each class** will not change: immunities are 1st-level Traits, so moving an ability between levels never changes who it works on. It only matters if the change also changes the ability's School, type or range.
3. **Its own text mentions a level** (when present) quotes rule text that depends on a level, for example Experienced only working on a Verbal of 4th level or lower, or Hunter's "only if that ability was chosen at level 4".
4. **Connected abilities** lists archetypes and other abilities that name it. Each may assume the current level or class list.
5. For a Magic User, check the level budget. The rulebook says:

   > Magic Users may purchase five magic points from each level. Unused points from higher levels can be rolled down to lower levels. A list of all magical abilities purchased must be carried at all times. All abilities purchased by Magic Users are Magical abilities. Magic Users must have an empty hand to cast their abilities.

   So a spell moved to 6th level competes for that level's five points (six with Look The Part), and points from a higher level can be used on lower levels but not the reverse. The **If you change its level** section counts the entries and points in that level's table, including the Equipment traits and Archetypes that draw on the same points.
6. For a martial class, look at the class file: the level table shows what else sits at the target level (including the class's Immune traits at 1st), and some levels are pick-one groups.
7. If the ability is shared, decide whether every class moves it or only one. The **Shared with** line names them.

## Class rule text used here

> Classes have levels. Each level unlocks new abilities you can use. Your level in a class is determined by the number of times you have signed in as that class before. See 'Credits and Levels' for more information.

---
*Generated by `scripts/gen_interop.py` from `rules/` (V8.08 "Spongy"). Regenerate after any rulebook update.*
