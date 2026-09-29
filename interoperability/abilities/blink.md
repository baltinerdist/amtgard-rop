---
title: "Blink — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Blink
type: Verbal
school: Sorcery
targets_other_players: false
classes: ["Assassin 3rd"]
---

# Blink — Interoperability

[Rule text](../../rules/magic-and-abilities/blink.md) · **Verbal** · Sorcery School · Range Self

## Summary

- **Can affect another player:** no (its range is Self or it has no target), so it has no works/blocked results. It can still be shared between classes.
- **On 1 class list:** Assassin (3rd).

## What it does

Caster becomes Insubstantial and may move within 50' of their start; cannot end it within 10' of a living enemy; fails if Stopped.

| Effect | On | Details |
| --- | --- | --- |
| Makes Insubstantial | caster (benefit) | until removed |
| Moves freely | caster (benefit) | feet 50; until removed |
| May not exit early | caster (harm) | what exit-early; until removed; continuously while it is worn, chanted or in effect |

**Capabilities:** castable-while-moving, has-drawback, makes-insubstantial, moves-self, self-protection-state · **Roles:** defense, mobility

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/blink.md`](../../metadata/profiles/blink.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Assassin](../classes/assassin.md) | 3rd | - | - | 2/Life | Self | no (ex) | Level table | Ambulant |

## Effect on each class

Not applicable: this ability does not target another player.

## Connected abilities

**These abilities name Blink in their text** (auto-detected). If Blink is renamed, moved or removed, check them:

| Ability | How | On classes |
| --- | --- | --- |
| [Circle of Protection](circle-of-protection.md) | mentions | Healer |
| [Spy](spy.md) | changes its numbers | Assassin |
| [Trickery](trickery.md) | grants or gives | Assassin |

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Assassin** lists it at 3rd; nothing else is listed at that level. Archetype that names it: Spy (archetypes are outside this model).

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
