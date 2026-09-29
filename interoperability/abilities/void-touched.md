---
title: "Void Touched — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Void Touched
type: Enchantment
school: Sorcery
targets_other_players: true
classes: ["Wizard 5th"]
---

# Void Touched — Interoperability

[Rule text](../../rules/magic-and-abilities/void-touched.md) · **Enchantment** · Sorcery School · Range Other (Wi) Self (Ap)

## Summary

- **Can affect another player:** yes.
- **Works on:** 12 of 12 classes.
- **Blocked on:** no class.
- **On 1 class list:** Wizard (5th).

## What it does

Armor Breaking melee weapons, Shadow Step 1/Refresh Charge x30, Steal Life Essence Unlimited, unaffected by Sorcery, Spirit and Death Magic; bearer is Cursed.

| Effect | On | Details |
| --- | --- | --- |
| Armor Breaking (bearer melee weapons) | bearer (benefit) | on bearer-melee-weapons; while worn; continuously while it is worn, chanted or in effect |
| Grants Shadow Step | bearer (benefit) | how gains; frequency 1/Refresh Charge x30 (ex); while worn; continuously while it is worn, chanted or in effect |
| Grants Steal Life Essence | bearer (benefit) | how gains; frequency Unlimited (ex); while worn; continuously while it is worn, chanted or in effect |
| Unaffected by | bearer (benefit) | by schools; schools Sorcery, Spirit, Death; while worn; continuously while it is worn, chanted or in effect |
| Curses | bearer (harm) | while worn; continuously while it is worn, chanted or in effect |

**Capabilities:** defeats-armor, grants-abilities, has-drawback, protects · **Roles:** offense, equipment, defense, anti-magic, healing

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/void-touched.md`](../../metadata/profiles/void-touched.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Wizard](../classes/wizard.md) | 5th | 1 | 2 | 1/Refresh | Other | yes | Spell table | - |

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

**Void Touched names these abilities in its own text** (auto-detected):

| Ability | How | On classes |
| --- | --- | --- |
| [Shadow Step](shadow-step.md) | grants or gives | Assassin, Scout |
| [Steal Life Essence](steal-life-essence.md) | grants or gives | Anti-Paladin, Healer, Wizard |

**These abilities name Void Touched in their text** (auto-detected). If Void Touched is renamed, moved or removed, check them:

| Ability | How | On classes |
| --- | --- | --- |
| [Corruptor](corruptor.md) | grants or gives | Anti-Paladin |

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Wizard** lists it at 5th for 1 point. That level's table has 8 entries (11 points if each were bought once, including 1 Equipment trait and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README).

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
