---
title: "Poison Arrow — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Poison Arrow
type: Specialty Arrow
school: Death
targets_other_players: true
classes: ["Archer 1st, 3rd, 5th", "Assassin 2nd"]
---

# Poison Arrow — Interoperability

[Rule text](../../rules/magic-and-abilities/poison-arrow.md) · **Specialty Arrow** · Death School

## Summary

- **Can affect another player:** yes.
- **Works on:** 11 of 12 classes.
- **Partly blocked on:** Paladin (arrow still lands as a normal hit).
- **On 2 class lists:** Archer (1st, 3rd, 5th), Assassin (2nd).

## What it does

Specialty Arrow with Wounds Kill: a player it wounds dies.

| Effect | On | Details |
| --- | --- | --- |
| Wounds Kill (this arrow) | struck-player (harm) | on this-arrow; instant; when a weapon, arrow or ball strikes the subject or their armor |

**Capabilities:** can-be-lethal, castable-while-moving · **Roles:** offense

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/poison-arrow.md`](../../metadata/profiles/poison-arrow.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Archer](../classes/archer.md) | 1st, 3rd, 5th | - | - | 1 Arrow / Unlimited | - | no (ex) | Level table | Pick two of three; listed again at each of these levels; also the class's Look The Part, so the class has it from 1st level whatever level the table gives |
| [Assassin](../classes/assassin.md) | 2nd | - | - | 2 Arrows / Unlimited | - | no (ex) | Level table | Pick one; also the class's Look The Part, so the class has it from 1st level whatever level the table gives |

## Effect on each class

Assumes every class is 6th level. Results do not depend on level.

| Target class | Result | Why |
| --- | --- | --- |
| [Anti-Paladin](../classes/anti-paladin.md) | Works |  |
| [Archer](../classes/archer.md) | Works |  |
| [Assassin](../classes/assassin.md) | Works |  |
| [Barbarian](../classes/barbarian.md) | Works |  |
| [Monk](../classes/monk.md) | Works |  |
| [Paladin](../classes/paladin.md) | **Partly blocked:** arrow still lands as a normal hit | Immune to Death. Wounds Kill is Death School so it does nothing, but a Specialty Arrow still counts as a normal arrow hit (Specialty Arrows rule 5) |
| [Scout](../classes/scout.md) | Works |  |
| [Warrior](../classes/warrior.md) | Works |  |
| [Bard](../classes/bard.md) | Works |  |
| [Druid](../classes/druid.md) | Works |  |
| [Healer](../classes/healer.md) | Works |  |
| [Wizard](../classes/wizard.md) | Works |  |

Monks can block Magic Balls and arrows with Missile Block, but that needs an active block, so it is shown as working.

## Connected abilities

**Shared with:** [Archer](../classes/archer.md), [Assassin](../classes/assassin.md). Changing this ability changes it for every one of these classes unless the classes get separate versions.

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Archer** lists it at 1st, 3rd, 5th; 3 other entries share that level: Reload, Destruction Arrow, Pinning Arrow. It is one of a group (Pick two of three). It is also this class's Look The Part, so the class has it at 1st level regardless.
- **Assassin** lists it at 2nd; 1 other entry shares that level: Poison. It is one of a group (Pick one). It is also this class's Look The Part, so the class has it at 1st level regardless.

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
