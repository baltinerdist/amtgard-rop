---
title: "Shadow Step — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Shadow Step
type: Verbal
school: Sorcery
targets_other_players: false
classes: ["Assassin 1st", "Scout 3rd"]
---

# Shadow Step — Interoperability

[Rule text](../../rules/magic-and-abilities/shadow-step.md) · **Verbal** · Sorcery School · Range Self

## Summary

- **Can affect another player:** no (its range is Self or it has no target), so it has no works/blocked results. It can still be shared between classes.
- **On 2 class lists:** Assassin (1st), Scout (3rd).

## What it does

Caster becomes Insubstantial in place, even while moving, until they use the Insubstantial exit incantation.

| Effect | On | Details |
| --- | --- | --- |
| Makes Insubstantial | caster (benefit) | until removed |

**Capabilities:** castable-while-moving, makes-insubstantial, self-protection-state · **Roles:** defense

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/shadow-step.md`](../../metadata/profiles/shadow-step.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Assassin](../classes/assassin.md) | 1st | - | - | 2/Life | Self | no (ex) | Level table | - |
| [Scout](../classes/scout.md) | 3rd | - | - | 1/Life | Self | no (ex) | Level table | - |

## Effect on each class

Not applicable: this ability does not target another player.

## Connected abilities

**These abilities name Shadow Step in their text** (auto-detected). If Shadow Step is renamed, moved or removed, check them:

| Ability | How | On classes |
| --- | --- | --- |
| [Spy](spy.md) | changes its numbers | Assassin |
| [Trickery](trickery.md) | grants or gives | Assassin |
| [Void Touched](void-touched.md) | grants or gives | Wizard |

**Shared with:** [Assassin](../classes/assassin.md), [Scout](../classes/scout.md). Changing this ability changes it for every one of these classes unless the classes get separate versions.

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Assassin** lists it at 1st; 2 other entries share that level: Trickery, Assassinate. Archetype that names it: Spy (archetypes are outside this model).
- **Scout** lists it at 3rd; 1 other entry shares that level: Dispel Magic.

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
