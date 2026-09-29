---
title: "Poison — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Poison
type: Enchantment
school: Death
targets_other_players: true
classes: ["Anti-Paladin 2nd", "Assassin 2nd", "Druid 2nd"]
---

# Poison — Interoperability

[Rule text](../../rules/magic-and-abilities/poison.md) · **Enchantment** · Death School · Range Self (Ap, As), Other (Dr)

## Summary

- **Can affect another player:** yes.
- **Works on:** 12 of 12 classes.
- **Blocked on:** no class.
- **On 3 class lists:** Anti-Paladin (2nd), Assassin (2nd), Druid (2nd).

## What it does

The bearer's next wound dealt with a wielded melee weapon is Wounds Kill; not expended if the target does not actually receive the wound.

| Effect | On | Details |
| --- | --- | --- |
| Wounds Kill (next wound) | bearer (benefit) | on next-wound; until used; continuously while it is worn, chanted or in effect |

**Capabilities:** can-be-lethal · **Roles:** offense

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/poison.md`](../../metadata/profiles/poison.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Anti-Paladin](../classes/anti-paladin.md) | 2nd | - | - | 1/Life Charge x3 | Self | no (ex) | Level table | - |
| [Assassin](../classes/assassin.md) | 2nd | - | - | 1/Life Charge x3 | Self | no (ex) | Level table | Pick one; also the class's Look The Part, so the class has it from 1st level whatever level the table gives |
| [Druid](../classes/druid.md) | 2nd | 1 | - | 1/Life | Other | yes | Spell table | - |

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

**These abilities name Poison in their text** (auto-detected). If Poison is renamed, moved or removed, check them:

| Ability | How | On classes |
| --- | --- | --- |
| [Poison Glands](poison-glands.md) | grants or gives | Druid |

**Shared with:** [Anti-Paladin](../classes/anti-paladin.md), [Assassin](../classes/assassin.md), [Druid](../classes/druid.md). Changing this ability changes it for every one of these classes unless the classes get separate versions.

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Anti-Paladin** lists it at 2nd; nothing else is listed at that level.
- **Assassin** lists it at 2nd; 1 other entry shares that level: Poison Arrow. It is one of a group (Pick one). It is also this class's Look The Part, so the class has it at 1st level regardless.
- **Druid** lists it at 2nd for 1 point. That level's table has 9 entries (12 points if each were bought once, including 1 Equipment trait and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README).

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
