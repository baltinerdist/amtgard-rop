---
title: "Blood and Thunder — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Blood and Thunder
type: Verbal
school: Spirit
targets_other_players: false
classes: ["Barbarian 6th"]
---

# Blood and Thunder — Interoperability

[Rule text](../../rules/magic-and-abilities/blood-and-thunder.md) · **Verbal** · Spirit School · Range Self

## Summary

- **Can affect another player:** no (its range is Self or it has no target), so it has no works/blocked results. It can still be shared between classes.
- **Indirect effects:** it grants [Blessing Against Wounds](blessing-against-wounds.md), which can affect other players; see those files for who they work on. This model does not compute the indirect effect itself.
- **On 1 class list:** Barbarian (6th).

## What it does

Kill Trigger: the caster gains Blessing Against Wounds (ex), marked with a white strip.

| Effect | On | Details |
| --- | --- | --- |
| Grants Blessing Against Wounds | caster (benefit) | how gains; frequency (ex); until used; after the caster kills an enemy (Kill Trigger) |

**Capabilities:** grants-abilities · **Roles:** defense

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/blood-and-thunder.md`](../../metadata/profiles/blood-and-thunder.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Barbarian](../classes/barbarian.md) | 6th | - | - | Unlimited | Self | no (ex) | Level table | - |

## Effect on each class

Not applicable: this ability does not target another player.

## Connected abilities

**Blood and Thunder names these abilities in its own text** (auto-detected):

| Ability | How | On classes |
| --- | --- | --- |
| [Blessing Against Wounds](blessing-against-wounds.md) | grants or gives | Healer |

**These abilities name Blood and Thunder in their text** (auto-detected). If Blood and Thunder is renamed, moved or removed, check them:

| Ability | How | On classes |
| --- | --- | --- |
| [Berserker](berserker.md) | removes | Barbarian |

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Barbarian** lists it at 6th; nothing else is listed at that level. Archetype that names it: Berserker (archetypes are outside this model).

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
