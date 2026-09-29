---
title: "Pinning Arrow — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Pinning Arrow
type: Specialty Arrow
school: Sorcery
targets_other_players: true
classes: ["Archer 1st, 3rd, 5th", "Scout 4th"]
---

# Pinning Arrow — Interoperability

[Rule text](../../rules/magic-and-abilities/pinning-arrow.md) · **Specialty Arrow** · Sorcery School

## Summary

- **Can affect another player:** yes.
- **Works on:** 12 of 12 classes.
- **Blocked on:** no class.
- **On 2 class lists:** Archer (1st, 3rd, 5th), Scout (4th).

## What it does

Engulfing Specialty Arrow: the player struck is Stopped for 30 seconds.

| Effect | On | Details |
| --- | --- | --- |
| Stops | struck-player (harm) | 30 s; when a weapon, arrow or ball strikes the subject or their armor |

**Capabilities:** castable-while-moving, holds-in-place · **Roles:** control

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/pinning-arrow.md`](../../metadata/profiles/pinning-arrow.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Archer](../classes/archer.md) | 1st, 3rd, 5th | - | - | 1 Arrow / Unlimited | - | no (ex) | Level table | Pick two of three; listed again at each of these levels; also the class's Look The Part, so the class has it from 1st level whatever level the table gives |
| [Scout](../classes/scout.md) | 4th | - | - | 1 Arrow / Unlimited | - | no (ex) | Level table | Pick one |

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

**These abilities name Pinning Arrow in their text** (auto-detected). If Pinning Arrow is renamed, moved or removed, check them:

| Ability | How | On classes |
| --- | --- | --- |
| [Apex](apex.md) | removes | Scout |
| [Artificer](artificer.md) | grants or gives | Archer |
| [Hunter](hunter.md) | changes its numbers | Scout |
| [Protection from Projectiles](protection-from-projectiles.md) | mentions | Healer |
| [Song of Deflection](song-of-deflection.md) | mentions | Bard |

**Shared with:** [Archer](../classes/archer.md), [Scout](../classes/scout.md). Changing this ability changes it for every one of these classes unless the classes get separate versions.

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Archer** lists it at 1st, 3rd, 5th; 3 other entries share that level: Reload, Destruction Arrow, Poison Arrow. It is one of a group (Pick two of three). It is also this class's Look The Part, so the class has it at 1st level regardless. Archetype that names it: Artificer (archetypes are outside this model).
- **Scout** lists it at 4th; 1 other entry shares that level: Hold Person. It is one of a group (Pick one). Archetypes that name it: Hunter, Apex (archetypes are outside this model).

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
