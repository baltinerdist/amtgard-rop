---
title: "Scavenge — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Scavenge
type: Verbal
school: Sorcery
targets_other_players: false
classes: ["Warrior 2nd"]
---

# Scavenge — Interoperability

[Rule text](../../rules/magic-and-abilities/scavenge.md) · **Verbal** · Sorcery School · Range Self

## Summary

- **Can affect another player:** no (its range is Self or it has no target), so it has no works/blocked results. It can still be shared between classes.
- **On 1 class list:** Warrior (2nd).

## What it does

Kill Trigger: repairs a destroyed or damaged item the caster carries, or one point of the caster's armor in one location.

| Effect | On | Details |
| --- | --- | --- |
| Repairs equipment | bearer-equipment (benefit) | what one-item; instant; after the caster kills an enemy (Kill Trigger); choice g1 option 1 |
| Repairs armor | bearer-equipment (benefit) | amount one-point-one-location; instant; after the caster kills an enemy (Kill Trigger); choice g1 option 2 |

**Capabilities:** repairs · **Roles:** equipment

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/scavenge.md`](../../metadata/profiles/scavenge.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Warrior](../classes/warrior.md) | 2nd | - | - | Unlimited | Self | no (ex) | Level table | - |

## Effect on each class

Not applicable: this ability does not target another player.

## Connected abilities

No other ability's text names it, and it names no other ability.

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Warrior** lists it at 2nd; nothing else is listed at that level.

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
