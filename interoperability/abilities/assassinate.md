---
title: "Assassinate — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Assassinate
type: Verbal
school: Death
targets_other_players: true
classes: ["Assassin 1st"]
---

# Assassinate — Interoperability

[Rule text](../../rules/magic-and-abilities/assassinate.md) · **Verbal** · Death School · Range 50'

## Summary

- **Can affect another player:** yes.
- **Works on:** 11 of 12 classes.
- **Blocked on:** Paladin.
- **On 1 class list:** Assassin (1st).

## What it does

Immediately after killing an enemy, Curses that dead enemy (within 50'); no verbal targeting needed.

| Effect | On | Details |
| --- | --- | --- |
| Curses | dead-target (harm) | until respawn; after the caster kills an enemy (Kill Trigger) |

**Capabilities:** castable-while-moving, curses · **Roles:** debuff

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/assassinate.md`](../../metadata/profiles/assassinate.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Assassin](../classes/assassin.md) | 1st | - | - | Unlimited | 50' | no (ex) | Level table | Ambulant |

## Effect on each class

Assumes every class is 6th level. Results do not depend on level.

| Target class | Result | Why |
| --- | --- | --- |
| [Anti-Paladin](../classes/anti-paladin.md) | Works |  |
| [Archer](../classes/archer.md) | Works |  |
| [Assassin](../classes/assassin.md) | Works |  |
| [Barbarian](../classes/barbarian.md) | Works |  |
| [Monk](../classes/monk.md) | Works |  |
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

- **Assassin** lists it at 1st; 2 other entries share that level: Trickery, Shadow Step.

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
