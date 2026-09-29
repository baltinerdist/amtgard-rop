---
title: "True Grit — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: True Grit
type: Verbal
school: Spirit
targets_other_players: false
classes: ["Warrior 3rd"]
---

# True Grit — Interoperability

[Rule text](../../rules/magic-and-abilities/true-grit.md) · **Verbal** · Spirit School · Range Self

## Summary

- **Can affect another player:** no (its range is Self or it has no target), so it has no works/blocked results. It can still be shared between classes.
- **On 1 class list:** Warrior (3rd).

## What it does

Said immediately after dying: the caster returns to life with wounds healed but is Frozen for 30 seconds; Enchantments are kept.

| Effect | On | Details |
| --- | --- | --- |
| Returns to life | caster (benefit) | instant |
| Heals wounds | caster (benefit) | amount all; instant |
| Freezes | caster (harm) | 30 s |

**Capabilities:** has-drawback, heals, revives · **Roles:** revival, healing

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/true-grit.md`](../../metadata/profiles/true-grit.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Warrior](../classes/warrior.md) | 3rd | - | - | 2/Refresh | Self | no (ex) | Level table | - |

## Effect on each class

Not applicable: this ability does not target another player.

## Connected abilities

**These abilities name True Grit in their text** (auto-detected). If True Grit is renamed, moved or removed, check them:

| Ability | How | On classes |
| --- | --- | --- |
| [Juggernaut](juggernaut.md) | removes | Warrior |

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Warrior** lists it at 3rd; nothing else is listed at that level. Archetype that names it: Juggernaut (archetypes are outside this model).

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
