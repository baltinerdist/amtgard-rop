---
title: "Enlightened Soul — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Enlightened Soul
type: Enchantment
school: Protection
targets_other_players: true
classes: ["Monk 1st", "Healer 5th"]
---

# Enlightened Soul — Interoperability

[Rule text](../../rules/magic-and-abilities/enlightened-soul.md) · **Enchantment** · Protection School · Range Other (He) Self (Mk)

## Summary

- **Can affect another player:** yes.
- **Works on:** 12 of 12 classes.
- **Blocked on:** no class.
- **On 2 class lists:** Monk (1st), Healer (5th).

## What it does

Bearer is unaffected by Verbal Magical abilities used from beyond Touch, harmful or beneficial; (ex) and Touch-range uses still work.

| Effect | On | Details |
| --- | --- | --- |
| Unaffected by | bearer (benefit) | by verbal-magical-beyond-touch; while worn; continuously while it is worn, chanted or in effect |
| Unaffected by | bearer (harm) | by verbal-magical-beyond-touch; while worn; continuously while it is worn, chanted or in effect |

**Capabilities:** has-drawback, protects · **Roles:** defense, anti-magic

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/enlightened-soul.md`](../../metadata/profiles/enlightened-soul.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Monk](../classes/monk.md) | 1st | - | - | - | Self | n/a (Trait) | Level table | - |
| [Healer](../classes/healer.md) | 5th | 1 | - | 1/Refresh | Other | yes | Spell table | - |

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

**These abilities name Enlightened Soul in their text** (auto-detected). If Enlightened Soul is renamed, moved or removed, check them:

| Ability | How | On classes |
| --- | --- | --- |
| [Destroy Armor](destroy-armor.md) | mentions | Wizard |
| [Pyrotechnics](pyrotechnics.md) | mentions | Wizard |
| [Song of Interference](song-of-interference.md) | borrows its effect | Bard |

**Shared with:** [Monk](../classes/monk.md), [Healer](../classes/healer.md). Changing this ability changes it for every one of these classes unless the classes get separate versions.

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Monk** lists it at 1st; 1 other entry shares that level: Missile Block.
- **Healer** lists it at 5th for 1 point. That level's table has 7 entries (8 points if each were bought once, including 0 Equipment traits and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README).

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
