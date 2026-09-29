---
title: "Protection from Evil — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Protection from Evil
type: Enchantment
school: Protection
targets_other_players: true
classes: ["Paladin 3rd"]
---

# Protection from Evil — Interoperability

[Rule text](../../rules/magic-and-abilities/protection-from-evil.md) · **Enchantment** · Protection School · Range Other

## Summary

- **Can affect another player:** yes.
- **Works on:** 12 of 12 classes.
- **Blocked on:** no class.
- **On 1 class list:** Paladin (3rd).

## What it does

Bearer is Immune to the Death School; Persistent and stays active while the bearer is dead; one active per caster.

| Effect | On | Details |
| --- | --- | --- |
| Immune to Death | bearer (benefit) | while worn; continuously while it is worn, chanted or in effect |

**Capabilities:** protects · **Roles:** defense

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/protection-from-evil.md`](../../metadata/profiles/protection-from-evil.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Paladin](../classes/paladin.md) | 3rd | - | - | 1/Refresh Charge x5 | Other | no (ex) | Level table | - |

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

**Protection from Evil names these abilities in its own text** (auto-detected):

| Ability | How | On classes |
| --- | --- | --- |
| [Persistent](persistent.md) | mentions | Healer, Wizard |

**These abilities name Protection from Evil in their text** (auto-detected). If Protection from Evil is renamed, moved or removed, check them:

| Ability | How | On classes |
| --- | --- | --- |
| [Guardian](guardian.md) | removes | Paladin |

**Grants immunity:** the effect text says the bearer is Immune to Death. That immunity would stop any targeting ability of that School.

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Paladin** lists it at 3rd; nothing else is listed at that level. Archetype that names it: Guardian (archetypes are outside this model).

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
