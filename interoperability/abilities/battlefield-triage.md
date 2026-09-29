---
title: "Battlefield Triage — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Battlefield Triage
type: Enchantment
school: Spirit
targets_other_players: true
classes: ["Bard 3rd"]
---

# Battlefield Triage — Interoperability

[Rule text](../../rules/magic-and-abilities/battlefield-triage.md) · **Enchantment** · Spirit School · Range Touch

## Summary

- **Can affect another player:** yes.
- **Works on:** 12 of 12 classes.
- **Blocked on:** no class.
- **On 1 class list:** Bard (3rd).

## What it does

Touch Enchantment with three strips: bearer may cast Heal (m) by incanting "Thou art made whole" and removing a strip; removed with the last strip.

| Effect | On | Details |
| --- | --- | --- |
| Casts Heal from strips | bearer (benefit) | while worn; continuously while it is worn, chanted or in effect |
| Uses up a strip | bearer (neutral) | n 1; instant; when the bearer spends one of the Enchantment's strips |

**Capabilities:** grants-abilities · **Roles:** healing

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/battlefield-triage.md`](../../metadata/profiles/battlefield-triage.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Bard](../classes/bard.md) | 3rd | 1 | 1 | 1/Refresh | Touch | yes | Spell table | - |

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

**Battlefield Triage names these abilities in its own text** (auto-detected):

| Ability | How | On classes |
| --- | --- | --- |
| [Heal](heal.md) | grants or gives | Monk, Scout, Druid, Healer |

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Bard** lists it at 3rd for 1 point. That level's table has 6 entries (7 points if each were bought once, including 1 Equipment trait and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README).

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
