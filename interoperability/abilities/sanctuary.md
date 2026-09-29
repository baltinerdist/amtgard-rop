---
title: "Sanctuary — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Sanctuary
type: Verbal
school: Protection
targets_other_players: false
classes: ["Monk 3rd"]
---

# Sanctuary — Interoperability

[Rule text](../../rules/magic-and-abilities/sanctuary.md) · **Verbal** · Protection School · Range Self

## Summary

- **Can affect another player:** no (its range is Self or it has no target), so it has no works/blocked results. It can still be shared between classes.
- **On 1 class list:** Monk (3rd).

## What it does

While chanting, caster and carried equipment are unaffected by hostile actions from within 20'; may not approach enemy bases, touch objectives or impede play.

| Effect | On | Details |
| --- | --- | --- |
| Unaffected by | caster (benefit) | by hostile-actions-within-20ft; while chanting; continuously while it is worn, chanted or in effect |
| May not approach enemy base | caster (harm) | what approach-enemy-base; while chanting; continuously while it is worn, chanted or in effect |
| May not interact with game | caster (harm) | what interact-with-game; while chanting; continuously while it is worn, chanted or in effect |
| May not impede play | caster (harm) | what impede-play; while chanting; continuously while it is worn, chanted or in effect |
| May not exit early | caster (harm) | what exit-early; while chanting; continuously while it is worn, chanted or in effect; only if the subject voluntarily carried or touched a weapon (other than blocking) |
| Unaffected by | bearer-equipment (benefit) | by hostile-actions-within-20ft; while chanting; continuously while it is worn, chanted or in effect |
| Moves freely | caster (benefit) | while chanting; continuously while it is worn, chanted or in effect |

**Capabilities:** castable-while-moving, has-drawback, moves-self, protects · **Roles:** defense, utility, equipment

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/sanctuary.md`](../../metadata/profiles/sanctuary.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Monk](../classes/monk.md) | 3rd | - | - | 1/Life Charge x5 | Self | no (ex) | Level table | Ambulant |

## Effect on each class

Not applicable: this ability does not target another player.

## Connected abilities

No other ability's text names it, and it names no other ability.

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Monk** lists it at 3rd; nothing else is listed at that level.

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
