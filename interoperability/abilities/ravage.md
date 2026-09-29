---
title: "Ravage — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Ravage
type: Verbal
school: Death
targets_other_players: true
classes: ["Wizard 3rd"]
---

# Ravage — Interoperability

[Rule text](../../rules/magic-and-abilities/ravage.md) · **Verbal** · Death School · Range 20'

## Summary

- **Can affect another player:** yes.
- **Works on:** 10 of 12 classes.
- **Blocked on:** Monk, Paladin.
- **On 1 class list:** Wizard (3rd).

## What it does

Makes a target within 20' Fragile, so their next wound kills them.

| Effect | On | Details |
| --- | --- | --- |
| Makes Fragile | target (harm) | until removed |

**Capabilities:** can-be-lethal · **Roles:** debuff, offense

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/ravage.md`](../../metadata/profiles/ravage.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Wizard](../classes/wizard.md) | 3rd | 1 | - | 2/Life | 20' | yes | Spell table | - |

## Effect on each class

Assumes every class is 6th level. Results do not depend on level.

| Target class | Result | Why |
| --- | --- | --- |
| [Anti-Paladin](../classes/anti-paladin.md) | Works |  |
| [Archer](../classes/archer.md) | Works |  |
| [Assassin](../classes/assassin.md) | Works |  |
| [Barbarian](../classes/barbarian.md) | Works |  |
| [Monk](../classes/monk.md) | **Blocked** | Enlightened Soul: unaffected by Verbal Magical abilities used beyond Touch (still works if cast at Touch) |
| [Paladin](../classes/paladin.md) | **Blocked** | Immune to Death |
| [Scout](../classes/scout.md) | Works |  |
| [Warrior](../classes/warrior.md) | Works |  |
| [Bard](../classes/bard.md) | Works |  |
| [Druid](../classes/druid.md) | Works |  |
| [Healer](../classes/healer.md) | Works |  |
| [Wizard](../classes/wizard.md) | Works |  |

## Connected abilities

No other ability's text names it, and it names no other ability.

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Wizard** lists it at 3rd for 1 point. That level's table has 10 entries (10 points if each were bought once, including 0 Equipment traits and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README). **Experienced** (also on this list) only works on a single per-life or per-refresh Verbal of 4th level or lower. This Verbal is eligible now but would not be if moved above 4th.

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
