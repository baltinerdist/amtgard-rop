---
title: "Destruction Arrow — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Destruction Arrow
type: Specialty Arrow
school: Sorcery
targets_other_players: true
classes: ["Archer 1st, 3rd, 5th"]
---

# Destruction Arrow — Interoperability

[Rule text](../../rules/magic-and-abilities/destruction-arrow.md) · **Specialty Arrow** · Sorcery School

## Summary

- **Can affect another player:** yes.
- **Works on:** 12 of 12 classes.
- **Blocked on:** no class.
- **On 1 class list:** Archer (1st, 3rd, 5th).

## What it does

Specialty Arrow: the normal arrow hit applies, then Armor Destroying and Shield Destroying.

| Effect | On | Details |
| --- | --- | --- |
| Inflicts a wound | struck-player (harm) | location struck; instant; when a weapon, arrow or ball strikes the subject or their armor |
| Armor Destroying (this arrow) | struck-player (harm) | on this-arrow; instant; when a weapon, arrow or ball strikes the subject or their armor |
| Shield Destroying (this arrow) | struck-player (harm) | on this-arrow; instant; when a weapon, arrow or ball strikes the subject or their armor |

**Capabilities:** attacks-equipment, castable-while-moving, defeats-armor, wounds · **Roles:** equipment, offense

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/destruction-arrow.md`](../../metadata/profiles/destruction-arrow.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Archer](../classes/archer.md) | 1st, 3rd, 5th | - | - | 1 Arrow / Unlimited | - | no (ex) | Level table | Pick two of three; listed again at each of these levels; also the class's Look The Part, so the class has it from 1st level whatever level the table gives |

## Effect on each class

Assumes every class is 6th level. Results do not depend on level.

| Target class | Result | Why |
| --- | --- | --- |
| [Anti-Paladin](../classes/anti-paladin.md) | Works |  |
| [Archer](../classes/archer.md) | Works |  |
| [Assassin](../classes/assassin.md) | Works |  |
| [Barbarian](../classes/barbarian.md) | Works |  |
| [Monk](../classes/monk.md) | Works |  |
| [Paladin](../classes/paladin.md) | Works |  |
| [Scout](../classes/scout.md) | Works |  |
| [Warrior](../classes/warrior.md) | Works |  |
| [Bard](../classes/bard.md) | Works |  |
| [Druid](../classes/druid.md) | Works |  |
| [Healer](../classes/healer.md) | Works |  |
| [Wizard](../classes/wizard.md) | Works |  |

Monks can block Magic Balls and arrows with Missile Block, but that needs an active block, so it is shown as working.

## Connected abilities

No other ability's text names it, and it names no other ability.

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Archer** lists it at 1st, 3rd, 5th; 3 other entries share that level: Reload, Pinning Arrow, Poison Arrow. It is one of a group (Pick two of three). It is also this class's Look The Part, so the class has it at 1st level regardless.

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
