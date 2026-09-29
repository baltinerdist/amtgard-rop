---
title: "Amplification — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Amplification
type: Enchantment
school: Sorcery
targets_other_players: true
classes: ["Bard 4th"]
---

# Amplification — Interoperability

[Rule text](../../rules/magic-and-abilities/amplification.md) · **Enchantment** · Sorcery School · Range Touch

## Summary

- **Can affect another player:** yes.
- **Works on:** 12 of 12 classes.
- **Blocked on:** no class.
- **On 1 class list:** Bard (4th).

## What it does

Bearer gains Extension 1/Refresh Charge x3 (m) without using purchased Extension; other sources of Extension cannot be used while worn.

| Effect | On | Details |
| --- | --- | --- |
| Grants Extension | bearer (benefit) | how gains; frequency 1/Refresh Charge x3 (m); while worn; continuously while it is worn, chanted or in effect |
| May not use other sources of ability | bearer (harm) | what use-other-sources-of-ability; while worn; continuously while it is worn, chanted or in effect |

**Capabilities:** grants-abilities, has-drawback · **Roles:** resource

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/amplification.md`](../../metadata/profiles/amplification.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Bard](../classes/bard.md) | 4th | 1 | 4 | 1/Refresh | Touch | yes | Spell table | - |

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

Touch and Other range also need the target to be willing, dead, stunned, frozen or Insubstantial and unable to move. That applies to every class alike and is not modelled.

## Connected abilities

**Amplification names these abilities in its own text** (auto-detected):

| Ability | How | On classes |
| --- | --- | --- |
| [Extension](extension.md) | grants or gives | Bard, Druid, Healer, Wizard |

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Bard** lists it at 4th for 1 point. That level's table has 9 entries (11 points if each were bought once, including 1 Equipment trait and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README).

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
