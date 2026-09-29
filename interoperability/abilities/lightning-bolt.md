---
title: "Lightning Bolt — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Lightning Bolt
type: Magic Ball
school: Flame
targets_other_players: true
classes: ["Wizard 3rd"]
---

# Lightning Bolt — Interoperability

[Rule text](../../rules/magic-and-abilities/lightning-bolt.md) · **Magic Ball** · Flame School

## Summary

- **Can affect another player:** yes.
- **Works on:** 11 of 12 classes.
- **Partly blocked on:** Anti-Paladin (equipment still hit).
- **On 1 class list:** Wizard (3rd).

## What it does

Magic Ball: wounds the hit location and Stops the player struck for 60 seconds; Weapon Destroying and Armor Breaking; Engulfing.

| Effect | On | Details |
| --- | --- | --- |
| Weapon Destroying (this magic ball) | struck-player (harm) | on this-magic-ball; instant; when a weapon, arrow or ball strikes the subject or their armor |
| Armor Breaking (this magic ball) | struck-player (harm) | on this-magic-ball; instant; when a weapon, arrow or ball strikes the subject or their armor |
| Inflicts a wound | struck-player (harm) | location struck; instant; when a weapon, arrow or ball strikes the subject or their armor |
| Stops | struck-player (harm) | 60 s; when a weapon, arrow or ball strikes the subject or their armor |

**Capabilities:** attacks-equipment, defeats-armor, holds-in-place, wounds · **Roles:** offense, control, equipment

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/lightning-bolt.md`](../../metadata/profiles/lightning-bolt.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Wizard](../classes/wizard.md) | 3rd | 1 | 4 | 1 Ball / Unlimited | - | yes | Spell table | - |

## Effect on each class

Assumes every class is 6th level. Results do not depend on level.

| Target class | Result | Why |
| --- | --- | --- |
| [Anti-Paladin](../classes/anti-paladin.md) | **Partly blocked:** equipment still hit | Immune to Flame. Weapon Destroying and Armor Breaking still hit their equipment (Immune rule 2) |
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

- **Wizard** lists it at 3rd for 1 point. That level's table has 10 entries (10 points if each were bought once, including 0 Equipment traits and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README).

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
