---
title: "Rage — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Rage
type: Verbal
school: Sorcery
targets_other_players: false
classes: ["Barbarian 2nd, 4th"]
---

# Rage — Interoperability

[Rule text](../../rules/magic-and-abilities/rage.md) · **Verbal** · Sorcery School · Range Self

## Summary

- **Can affect another player:** no (its range is Self or it has no target), so it has no works/blocked results. It can still be shared between classes.
- **On 1 class list:** Barbarian (2nd, 4th).

## What it does

For seven seconds, counted aloud, caster is unaffected by Verbals and their melee weapons are Shield Crushing and Armor Breaking.

| Effect | On | Details |
| --- | --- | --- |
| Unaffected by | caster (benefit) | by verbal-abilities; 7 s |
| Shield Crushing (bearer melee weapons) | caster (benefit) | on bearer-melee-weapons; 7 s |
| Armor Breaking (bearer melee weapons) | caster (benefit) | on bearer-melee-weapons; 7 s |

**Capabilities:** attacks-equipment, castable-while-moving, defeats-armor, protects · **Roles:** offense, defense, equipment

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/rage.md`](../../metadata/profiles/rage.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Barbarian](../classes/barbarian.md) | 2nd, 4th | - | - | 1/Refresh Charge x10 | Self | no (ex) | Level table | Ambulant; listed again at each of these levels; also the class's Look The Part, so the class has it from 1st level whatever level the table gives |

## Effect on each class

Not applicable: this ability does not target another player.

## Connected abilities

**These abilities name Rage in their text** (auto-detected). If Rage is renamed, moved or removed, check them:

| Ability | How | On classes |
| --- | --- | --- |
| [Raider](raider.md) | removes | Barbarian |

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Barbarian** lists it at 2nd, 4th; nothing else is listed at that level. It is also this class's Look The Part, so the class has it at 1st level regardless. Archetype that names it: Raider (archetypes are outside this model).

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
