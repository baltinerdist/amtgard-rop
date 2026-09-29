---
title: "Lycanthropy — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Lycanthropy
type: Enchantment
school: Death
targets_other_players: true
classes: ["Druid 4th"]
---

# Lycanthropy — Interoperability

[Rule text](../../rules/magic-and-abilities/lycanthropy.md) · **Enchantment** · Death School · Range Other

## Summary

- **Can affect another player:** yes.
- **Works on:** 12 of 12 classes.
- **Blocked on:** no class.
- **On 1 class list:** Druid (4th).

## What it does

Bearer gains 2 points of Magic Armor, Shield Crushing wielded melee weapons, and Immunity to Command.

| Effect | On | Details |
| --- | --- | --- |
| Grants Magic Armor | bearer (benefit) | points 2; while worn; continuously while it is worn, chanted or in effect |
| Shield Crushing (bearer melee weapons) | bearer (benefit) | on bearer-melee-weapons; while worn; continuously while it is worn, chanted or in effect |
| Immune to Command | bearer (benefit) | while worn; continuously while it is worn, chanted or in effect |

**Capabilities:** attacks-equipment, protects · **Roles:** defense, offense, equipment

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/lycanthropy.md`](../../metadata/profiles/lycanthropy.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Druid](../classes/druid.md) | 4th | 1 | 2 | 1/Refresh | Other | yes | Spell table | - |

## Effect on each class

Assumes every class is 6th level. Results do not depend on level.

| Target class | Result | Why |
| --- | --- | --- |
| [Anti-Paladin](../classes/anti-paladin.md) | Works |  |
| [Archer](../classes/archer.md) | Works |  |
| [Assassin](../classes/assassin.md) | Works |  |
| [Barbarian](../classes/barbarian.md) | Works |  |
| [Monk](../classes/monk.md) | Works |  |
| [Paladin](../classes/paladin.md) | Works | Enchantments apply despite Immunity (Enchantments rule 3) |
| [Scout](../classes/scout.md) | Works |  |
| [Warrior](../classes/warrior.md) | Works |  |
| [Bard](../classes/bard.md) | Works |  |
| [Druid](../classes/druid.md) | Works |  |
| [Healer](../classes/healer.md) | Works |  |
| [Wizard](../classes/wizard.md) | Works |  |

Touch and Other range also need the target to be willing, dead, stunned, frozen or Insubstantial and unable to move. That applies to every class alike and is not modelled.

## Connected abilities

No other ability's text names it, and it names no other ability.

**Grants immunity:** the effect text says the bearer is Immune to Command. That immunity would stop any targeting ability of that School.

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Druid** lists it at 4th for 1 point. That level's table has 8 entries (12 points if each were bought once, including 1 Equipment trait and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README).

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
