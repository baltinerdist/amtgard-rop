---
title: "Greater Resurrect — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Greater Resurrect
type: Verbal
school: Spirit
targets_other_players: true
classes: ["Paladin 4th", "Healer 5th"]
---

# Greater Resurrect — Interoperability

[Rule text](../../rules/magic-and-abilities/greater-resurrect.md) · **Verbal** · Spirit School · Range Other

## Summary

- **Can affect another player:** yes.
- **Works on:** 12 of 12 classes.
- **Blocked on:** no class.
- **On 2 class lists:** Paladin (4th), Healer (5th).

## What it does

Returns a willing dead player (within 5' of where they died) to life with wounds healed, regardless of States, removing Cursed; Enchantments kept.

| Effect | On | Details |
| --- | --- | --- |
| Returns to life | dead-target (benefit) | instant |
| Heals wounds | dead-target (benefit) | amount all; instant |
| Ends Cursed | dead-target (benefit) | what specific-state; instant |

**Capabilities:** cleanses, heals, revives · **Roles:** revival, healing

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/greater-resurrect.md`](../../metadata/profiles/greater-resurrect.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Paladin](../classes/paladin.md) | 4th | - | - | 1/Life | Other | yes | Level table | - |
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

**These abilities name Greater Resurrect in their text** (auto-detected). If Greater Resurrect is renamed, moved or removed, check them:

| Ability | How | On classes |
| --- | --- | --- |
| [Inquisitor](inquisitor.md) | removes | Paladin |

**Shared with:** [Paladin](../classes/paladin.md), [Healer](../classes/healer.md). Changing this ability changes it for every one of these classes unless the classes get separate versions.

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Paladin** lists it at 4th; nothing else is listed at that level. Archetype that names it: Inquisitor (archetypes are outside this model).
- **Healer** lists it at 5th for 1 point. That level's table has 7 entries (8 points if each were bought once, including 0 Equipment traits and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README). **Experienced** (also on this list) only works on a single per-life or per-refresh Verbal of 4th level or lower. This Verbal is already too high for it.

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
