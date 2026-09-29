---
title: "Imbue — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Imbue
type: Enchantment
school: Protection
targets_other_players: true
classes: ["Healer 4th"]
---

# Imbue — Interoperability

[Rule text](../../rules/magic-and-abilities/imbue.md) · **Enchantment** · Protection School · Range Touch (Pa), Other (He)

## Summary

- **Can affect another player:** yes.
- **Works on:** 12 of 12 classes.
- **Blocked on:** no class.
- **On 1 class list:** Healer (4th).

## What it does

Bearer chooses shield or weapons: wielded equipment of that type cannot be destroyed or damaged and ignores Engulfing effects.

| Effect | On | Details |
| --- | --- | --- |
| Protects equipment | bearer-equipment (benefit) | what shield; degree indestructible; while worn; continuously while it is worn, chanted or in effect; choice g1 option 1 |
| Ignores Engulfing effects | bearer-equipment (benefit) | while worn; continuously while it is worn, chanted or in effect; choice g1 option 1 |
| Protects equipment | bearer-equipment (benefit) | what weapons; degree indestructible; while worn; continuously while it is worn, chanted or in effect; choice g1 option 2 |
| Ignores Engulfing effects | bearer-equipment (benefit) | while worn; continuously while it is worn, chanted or in effect; choice g1 option 2 |

**Capabilities:** protects · **Roles:** defense, equipment

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/imbue.md`](../../metadata/profiles/imbue.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Healer](../classes/healer.md) | 4th | 1 | 2 | 2/Refresh | Other | yes | Spell table | - |

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

**These abilities name Imbue in their text** (auto-detected). If Imbue is renamed, moved or removed, check them:

| Ability | How | On classes |
| --- | --- | --- |
| [Guardian](guardian.md) | grants or gives | Paladin |

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Healer** lists it at 4th for 1 point. That level's table has 8 entries (8 points if each were bought once, including 0 Equipment traits and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README).

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
