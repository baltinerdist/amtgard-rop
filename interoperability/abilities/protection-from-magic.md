---
title: "Protection from Magic — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Protection from Magic
type: Enchantment
school: Protection
targets_other_players: true
classes: ["Paladin 6th", "Healer 6th", "Wizard 6th"]
---

# Protection from Magic — Interoperability

[Rule text](../../rules/magic-and-abilities/protection-from-magic.md) · **Enchantment** · Protection School · Range Other (He, Wi) Touch (Pa)

## Summary

- **Can affect another player:** yes.
- **Works on:** 12 of 12 classes.
- **Blocked on:** no class.
- **On 3 class lists:** Paladin (6th), Healer (6th), Wizard (6th).

## What it does

Bearer is unaffected by Magical abilities of every School; when the bearer dies they are Cursed.

| Effect | On | Details |
| --- | --- | --- |
| Unaffected by | bearer (benefit) | by magical-abilities; while worn; continuously while it is worn, chanted or in effect |
| Curses | bearer (harm) | until respawn; when the subject would die |

**Capabilities:** has-drawback, protects · **Roles:** defense, anti-magic

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/protection-from-magic.md`](../../metadata/profiles/protection-from-magic.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Paladin](../classes/paladin.md) | 6th | - | - | 2/Refresh | Touch | yes | Level table | - |
| [Healer](../classes/healer.md) | 6th | 1 | - | 1/Refresh | Other | yes | Spell table | - |
| [Wizard](../classes/wizard.md) | 6th | 1 | - | 1/Refresh | Other | yes | Spell table | - |

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

**These abilities name Protection from Magic in their text** (auto-detected). If Protection from Magic is renamed, moved or removed, check them:

| Ability | How | On classes |
| --- | --- | --- |
| [Destroy Armor](destroy-armor.md) | mentions | Wizard |
| [Guardian](guardian.md) | removes | Paladin |
| [Pyrotechnics](pyrotechnics.md) | mentions | Wizard |

**Shared with:** [Paladin](../classes/paladin.md), [Healer](../classes/healer.md), [Wizard](../classes/wizard.md). Changing this ability changes it for every one of these classes unless the classes get separate versions.

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Paladin** lists it at 6th; nothing else is listed at that level. Archetype that names it: Guardian (archetypes are outside this model).
- **Healer** lists it at 6th for 1 point. That level's table has 9 entries (11 points if each were bought once, including 0 Equipment traits and 3 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README).
- **Wizard** lists it at 6th for 1 point. That level's table has 9 entries (14 points if each were bought once, including 0 Equipment traits and 3 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README).

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
