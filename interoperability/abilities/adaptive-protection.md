---
title: "Adaptive Protection — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Adaptive Protection
type: Enchantment
school: Protection
targets_other_players: true
classes: ["Scout 6th", "Healer 3rd"]
---

# Adaptive Protection — Interoperability

[Rule text](../../rules/magic-and-abilities/adaptive-protection.md) · **Enchantment** · Protection School · Range Other (He), Self (Sc)

## Summary

- **Can affect another player:** yes.
- **Works on:** 12 of 12 classes.
- **Blocked on:** no class.
- **On 2 class lists:** Scout (6th), Healer (3rd).

## What it does

Bearer is Immune to one School chosen at casting: Death, Flame, Subdual, Command or Sorcery.

| Effect | On | Details |
| --- | --- | --- |
| Immune to a chosen School | bearer (benefit) | options Death, Flame, Subdual, Command, Sorcery; while worn; continuously while it is worn, chanted or in effect |

**Capabilities:** protects · **Roles:** defense

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/adaptive-protection.md`](../../metadata/profiles/adaptive-protection.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Scout](../classes/scout.md) | 6th | - | - | 1/Life | Self | no (ex) | Level table | - |
| [Healer](../classes/healer.md) | 3rd | 1 | - | 1/Refresh | Other | yes | Spell table | - |

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

**These abilities name Adaptive Protection in their text** (auto-detected). If Adaptive Protection is renamed, moved or removed, check them:

| Ability | How | On classes |
| --- | --- | --- |
| [Destroy Armor](destroy-armor.md) | mentions | Wizard |
| [Pyrotechnics](pyrotechnics.md) | mentions | Wizard |

**Shared with:** [Scout](../classes/scout.md), [Healer](../classes/healer.md). Changing this ability changes it for every one of these classes unless the classes get separate versions.

**Grants immunity:** the effect text says the bearer is Immune to one of: Death, Flame, Subdual, Command, Sorcery. That immunity would stop any targeting ability of that School.

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Scout** lists it at 6th; nothing else is listed at that level.
- **Healer** lists it at 3rd for 1 point. That level's table has 9 entries (10 points if each were bought once, including 1 Equipment trait and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README).

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
