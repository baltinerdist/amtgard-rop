---
title: "Sever Spirit — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Sever Spirit
type: Verbal
school: Spirit
targets_other_players: true
classes: ["Healer 2nd"]
---

# Sever Spirit — Interoperability

[Rule text](../../rules/magic-and-abilities/sever-spirit.md) · **Verbal** · Spirit School · Range 20'

## Summary

- **Can affect another player:** yes.
- **Works on:** 11 of 12 classes.
- **Partly blocked on:** Monk (enchantment removal still lands, the Curse does not).
- **On 1 class list:** Healer (2nd).

## What it does

Curses a dead player within 20' and removes all their Enchantments, regardless of Traits, States, Immunities or Enchantments.

| Effect | On | Details |
| --- | --- | --- |
| Curses | dead-target (harm) | until respawn |
| Removes Enchantments | dead-target (harm) | scope all; instant |

**Capabilities:** curses, dispels · **Roles:** debuff, anti-magic

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/sever-spirit.md`](../../metadata/profiles/sever-spirit.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Healer](../classes/healer.md) | 2nd | 1 | - | 1/Life Charge x3 | 20' | yes | Spell table | - |

## Effect on each class

Assumes every class is 6th level. Results do not depend on level.

| Target class | Result | Why |
| --- | --- | --- |
| [Anti-Paladin](../classes/anti-paladin.md) | Works |  |
| [Archer](../classes/archer.md) | Works |  |
| [Assassin](../classes/assassin.md) | Works |  |
| [Barbarian](../classes/barbarian.md) | Works |  |
| [Monk](../classes/monk.md) | **Partly blocked:** enchantment removal still lands, the Curse does not | Enlightened Soul: unaffected by Verbal Magical abilities used beyond Touch. Its text removes Enchantments 'regardless of the player's Traits', so that part still lands; the Curse does not (a reading of the rule text, not an official ruling) |
| [Paladin](../classes/paladin.md) | Works |  |
| [Scout](../classes/scout.md) | Works |  |
| [Warrior](../classes/warrior.md) | Works |  |
| [Bard](../classes/bard.md) | Works |  |
| [Druid](../classes/druid.md) | Works |  |
| [Healer](../classes/healer.md) | Works |  |
| [Wizard](../classes/wizard.md) | Works |  |

## Connected abilities

**These abilities name Sever Spirit in their text** (auto-detected). If Sever Spirit is renamed, moved or removed, check them:

| Ability | How | On classes |
| --- | --- | --- |
| [Medium](medium.md) | grants or gives | Monk |

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Healer** lists it at 2nd for 1 point. That level's table has 9 entries (12 points if each were bought once, including 1 Equipment trait and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README). **Experienced** (also on this list) only works on a single per-life or per-refresh Verbal of 4th level or lower. This Verbal is eligible now but would not be if moved above 4th.

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
