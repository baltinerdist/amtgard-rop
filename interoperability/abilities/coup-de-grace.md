---
title: "Coup de Grace — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Coup de Grace
type: Verbal
school: Death
targets_other_players: true
classes: ["Assassin 6th"]
---

# Coup de Grace — Interoperability

[Rule text](../../rules/magic-and-abilities/coup-de-grace.md) · **Verbal** · Death School · Range 20'

## Summary

- **Can affect another player:** yes.
- **Works on:** 10 of 12 classes.
- **Blocked on:** Monk, Paladin.
- **On 1 class list:** Assassin (6th).

## What it does

Kills a target within 20' who was wounded when the Incantation began, even if healed before it ends.

| Effect | On | Details |
| --- | --- | --- |
| Causes death | target (harm) | instant |

**Capabilities:** can-be-lethal, causes-death · **Roles:** offense

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/coup-de-grace.md`](../../metadata/profiles/coup-de-grace.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Assassin](../classes/assassin.md) | 6th | - | - | 1/Life | 20' | yes | Level table | - |

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

**These abilities name Coup de Grace in their text** (auto-detected). If Coup de Grace is renamed, moved or removed, check them:

| Ability | How | On classes |
| --- | --- | --- |
| [Rogue](rogue.md) | mentions | Assassin |

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Assassin** lists it at 6th; nothing else is listed at that level. Archetype that names it: Rogue (archetypes are outside this model).

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
