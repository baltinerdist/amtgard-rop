---
title: "Reload — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Reload
type: Verbal
school: Sorcery
targets_other_players: false
classes: ["Archer 1st"]
---

# Reload — Interoperability

[Rule text](../../rules/magic-and-abilities/reload.md) · **Verbal** · Sorcery School · Range Self

## Summary

- **Can affect another player:** no (its range is Self or it has no target), so it has no works/blocked results. It can still be shared between classes.
- **On 1 class list:** Archer (1st).

## What it does

Caster becomes Invulnerable to retrieve arrows, staying 10' from combat; ends at starting location or base by declaring "I return with a full quiver" x3.

| Effect | On | Details |
| --- | --- | --- |
| Makes Invulnerable | caster (benefit) | until removed |
| Moves freely | caster (benefit) | until removed |
| Must keep away | caster (harm) | feet 10; from combat; until removed; continuously while it is worn, chanted or in effect |

**Capabilities:** has-drawback, moves-self, self-protection-state · **Roles:** utility, mobility, defense

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/reload.md`](../../metadata/profiles/reload.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Archer](../classes/archer.md) | 1st | - | - | 1/Refresh Charge x3 | Self | no (ex) | Level table | - |

## Effect on each class

Not applicable: this ability does not target another player.

## Connected abilities

No other ability's text names it, and it names no other ability.

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Archer** lists it at 1st; 3 other entries share that level: Destruction Arrow, Pinning Arrow, Poison Arrow.

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
