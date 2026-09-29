---
title: "Heal — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Heal
type: Verbal
school: Spirit
targets_other_players: true
classes: ["Monk 4th", "Scout 2nd, 5th", "Druid 2nd", "Healer 1st"]
---

# Heal — Interoperability

[Rule text](../../rules/magic-and-abilities/heal.md) · **Verbal** · Spirit School · Range Touch

## Summary

- **Can affect another player:** yes.
- **Works on:** 12 of 12 classes.
- **Blocked on:** no class.
- **On 4 class lists:** Monk (4th), Scout (2nd, 5th), Druid (2nd), Healer (1st).

## What it does

Heals one wound on a player by Touch (self or another).

| Effect | On | Details |
| --- | --- | --- |
| Heals wounds | target (benefit) | amount one; instant |

**Capabilities:** heals · **Roles:** healing

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/heal.md`](../../metadata/profiles/heal.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Monk](../classes/monk.md) | 4th | - | - | 1/Life Charge x3 | Touch | no (ex) | Level table | also the class's Look The Part, so the class has it from 1st level whatever level the table gives |
| [Scout](../classes/scout.md) | 2nd, 5th | - | - | 1/Life Charge x5 | Touch | no (ex) | Level table | listed again at each of these levels; also the class's Look The Part, so the class has it from 1st level whatever level the table gives |
| [Druid](../classes/druid.md) | 2nd | 1 | - | 1/Life | Touch | yes | Spell table | - |
| [Healer](../classes/healer.md) | 1st | 1 | 1 | Unlimited | Touch | yes | Spell table | - |

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

**These abilities name Heal in their text** (auto-detected). If Heal is renamed, moved or removed, check them:

| Ability | How | On classes |
| --- | --- | --- |
| [Battlefield Triage](battlefield-triage.md) | grants or gives | Bard |
| [Gift of Water](gift-of-water.md) | grants or gives | Druid |
| [Mass Healing](mass-healing.md) | grants or gives | Healer |
| [Priest](priest.md) | mentions | Healer |
| [Regeneration](regeneration.md) | grants or gives | Druid |

**Shared with:** [Monk](../classes/monk.md), [Scout](../classes/scout.md), [Druid](../classes/druid.md), [Healer](../classes/healer.md). Changing this ability changes it for every one of these classes unless the classes get separate versions.

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Monk** lists it at 4th; nothing else is listed at that level. It is also this class's Look The Part, so the class has it at 1st level regardless.
- **Scout** lists it at 2nd, 5th; 1 other entry shares that level: Release. It is also this class's Look The Part, so the class has it at 1st level regardless.
- **Druid** lists it at 2nd for 1 point. That level's table has 9 entries (12 points if each were bought once, including 1 Equipment trait and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README). **Experienced** (also on this list) only works on a single per-life or per-refresh Verbal of 4th level or lower. This Verbal is eligible now but would not be if moved above 4th.
- **Healer** lists it at 1st for 1 point. That level's table has 8 entries (12 points if each were bought once, including 2 Equipment traits and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README). **Experienced** (also on this list) only works on a single per-life or per-refresh Verbal of 4th level or lower. This one is Unlimited, so it is not eligible at any level. Archetype that names it: Priest (archetypes are outside this model).

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
