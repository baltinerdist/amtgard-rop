---
title: "Dispel Magic — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Dispel Magic
type: Verbal
school: Sorcery
targets_other_players: true
classes: ["Scout 3rd", "Druid 3rd", "Healer 4th", "Wizard 3rd"]
---

# Dispel Magic — Interoperability

[Rule text](../../rules/magic-and-abilities/dispel-magic.md) · **Verbal** · Sorcery School · Range 20'

## Summary

- **Can affect another player:** yes.
- **Works on:** 12 of 12 classes.
- **Blocked on:** no class.
- **On 4 class lists:** Scout (3rd), Druid (3rd), Healer (4th), Wizard (3rd).

## What it does

Removes all Enchantments from a target within 20', regardless of Traits, States, Immunities or Enchantments, except Sleight of Mind; not on Invulnerable players.

| Effect | On | Details |
| --- | --- | --- |
| Removes Enchantments | target (harm) | scope all; instant |

**Capabilities:** dispels · **Roles:** anti-magic

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/dispel-magic.md`](../../metadata/profiles/dispel-magic.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Scout](../classes/scout.md) | 3rd | - | - | 1/Refresh Charge x5 | 20' | no (ex) | Level table | - |
| [Druid](../classes/druid.md) | 3rd | 1 | - | 1/Refresh | 20' | yes | Spell table | - |
| [Healer](../classes/healer.md) | 4th | 1 | - | 1/Refresh | 20' | yes | Spell table | - |
| [Wizard](../classes/wizard.md) | 3rd | 1 | - | 1/Refresh Charge x3 | 20' | yes | Spell table | - |

## Effect on each class

Assumes every class is 6th level. Results do not depend on level.

| Target class | Result | Why |
| --- | --- | --- |
| [Anti-Paladin](../classes/anti-paladin.md) | Works |  |
| [Archer](../classes/archer.md) | Works |  |
| [Assassin](../classes/assassin.md) | Works |  |
| [Barbarian](../classes/barbarian.md) | Works |  |
| [Monk](../classes/monk.md) | Works | Its text removes Enchantments 'regardless of the player's Traits', so Enlightened Soul does not stop it (a reading of the rule text, not an official ruling) |
| [Paladin](../classes/paladin.md) | Works |  |
| [Scout](../classes/scout.md) | Works |  |
| [Warrior](../classes/warrior.md) | Works |  |
| [Bard](../classes/bard.md) | Works |  |
| [Druid](../classes/druid.md) | Works |  |
| [Healer](../classes/healer.md) | Works |  |
| [Wizard](../classes/wizard.md) | Works |  |

## Connected abilities

**Dispel Magic names these abilities in its own text** (auto-detected):

| Ability | How | On classes |
| --- | --- | --- |
| [Sleight of Mind](sleight-of-mind.md) | mentions | Bard |

**These abilities name Dispel Magic in their text** (auto-detected). If Dispel Magic is renamed, moved or removed, check them:

| Ability | How | On classes |
| --- | --- | --- |
| [Ancestral Armor](ancestral-armor.md) | mentions | Warrior, Healer |
| [Naturalize Magic](naturalize-magic.md) | grants or gives | Druid |
| [Sleight of Mind](sleight-of-mind.md) | mentions | Bard |

**Shared with:** [Scout](../classes/scout.md), [Druid](../classes/druid.md), [Healer](../classes/healer.md), [Wizard](../classes/wizard.md). Changing this ability changes it for every one of these classes unless the classes get separate versions.

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Scout** lists it at 3rd; 1 other entry shares that level: Shadow Step.
- **Druid** lists it at 3rd for 1 point. That level's table has 9 entries (9 points if each were bought once, including 0 Equipment traits and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README). **Experienced** (also on this list) only works on a single per-life or per-refresh Verbal of 4th level or lower. This Verbal is eligible now but would not be if moved above 4th.
- **Healer** lists it at 4th for 1 point. That level's table has 8 entries (8 points if each were bought once, including 0 Equipment traits and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README). **Experienced** (also on this list) only works on a single per-life or per-refresh Verbal of 4th level or lower. This Verbal is eligible now but would not be if moved above 4th.
- **Wizard** lists it at 3rd for 1 point. That level's table has 10 entries (10 points if each were bought once, including 0 Equipment traits and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README). **Experienced** (also on this list) only works on a single per-life or per-refresh Verbal of 4th level or lower. This Verbal is eligible now but would not be if moved above 4th.

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
