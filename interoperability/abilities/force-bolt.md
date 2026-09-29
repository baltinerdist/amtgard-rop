---
title: "Force Bolt — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Force Bolt
type: Magic Ball
school: Sorcery
targets_other_players: true
classes: ["Druid 2nd", "Wizard 1st"]
---

# Force Bolt — Interoperability

[Rule text](../../rules/magic-and-abilities/force-bolt.md) · **Magic Ball** · Sorcery School

## Summary

- **Can affect another player:** yes.
- **Works on:** 12 of 12 classes.
- **Blocked on:** no class.
- **On 2 class lists:** Druid (2nd), Wizard (1st).

## What it does

Magic Ball: wounds the hit location; Weapon Destroying and Armor Breaking.

| Effect | On | Details |
| --- | --- | --- |
| Weapon Destroying (this magic ball) | struck-player (harm) | on this-magic-ball; instant; when a weapon, arrow or ball strikes the subject or their armor |
| Armor Breaking (this magic ball) | struck-player (harm) | on this-magic-ball; instant; when a weapon, arrow or ball strikes the subject or their armor |
| Inflicts a wound | struck-player (harm) | location struck; instant; when a weapon, arrow or ball strikes the subject or their armor |

**Capabilities:** attacks-equipment, defeats-armor, wounds · **Roles:** offense, equipment

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/force-bolt.md`](../../metadata/profiles/force-bolt.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Druid](../classes/druid.md) | 2nd | 1 | 2 | 2 Balls / Unlimited | - | yes | Spell table | - |
| [Wizard](../classes/wizard.md) | 1st | 1 | 8 | 3 Balls / Unlimited | - | yes | Spell table | - |

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

**These abilities name Force Bolt in their text** (auto-detected). If Force Bolt is renamed, moved or removed, check them:

| Ability | How | On classes |
| --- | --- | --- |
| [Mystic](mystic.md) | grants or gives | Monk |

**Shared with:** [Druid](../classes/druid.md), [Wizard](../classes/wizard.md). Changing this ability changes it for every one of these classes unless the classes get separate versions.

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Druid** lists it at 2nd for 1 point. That level's table has 9 entries (12 points if each were bought once, including 1 Equipment trait and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README).
- **Wizard** lists it at 1st for 1 point. That level's table has 8 entries (10 points if each were bought once, including 1 Equipment trait and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README).

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
