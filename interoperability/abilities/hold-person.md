---
title: "Hold Person — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Hold Person
type: Verbal
school: Command
targets_other_players: true
classes: ["Assassin 4th", "Scout 4th", "Healer 2nd", "Wizard 3rd"]
---

# Hold Person — Interoperability

[Rule text](../../rules/magic-and-abilities/hold-person.md) · **Verbal** · Command School · Range 20'

## Summary

- **Can affect another player:** yes.
- **Works on:** 8 of 12 classes.
- **Blocked on:** Anti-Paladin, Barbarian, Monk, Paladin.
- **On 4 class lists:** Assassin (4th), Scout (4th), Healer (2nd), Wizard (3rd).

## What it does

A target within 20' is Stopped for 30 seconds.

| Effect | On | Details |
| --- | --- | --- |
| Stops | target (harm) | 30 s |

**Capabilities:** holds-in-place · **Roles:** control

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/hold-person.md`](../../metadata/profiles/hold-person.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Assassin](../classes/assassin.md) | 4th | - | - | 1/Life | 20' | yes | Level table | - |
| [Scout](../classes/scout.md) | 4th | - | - | 1/Life | 20' | yes | Level table | Pick one |
| [Healer](../classes/healer.md) | 2nd | 1 | - | 1/Life Charge x3 | 20' | yes | Spell table | - |
| [Wizard](../classes/wizard.md) | 3rd | 1 | - | 1/Life | 20' | yes | Spell table | - |

## Effect on each class

Assumes every class is 6th level. Results do not depend on level.

| Target class | Result | Why |
| --- | --- | --- |
| [Anti-Paladin](../classes/anti-paladin.md) | **Blocked** | Immune to Command |
| [Archer](../classes/archer.md) | Works |  |
| [Assassin](../classes/assassin.md) | Works |  |
| [Barbarian](../classes/barbarian.md) | **Blocked** | Immune to Command |
| [Monk](../classes/monk.md) | **Blocked** | Enlightened Soul: unaffected by Verbal Magical abilities used beyond Touch (still works if cast at Touch) |
| [Paladin](../classes/paladin.md) | **Blocked** | Immune to Command |
| [Scout](../classes/scout.md) | Works |  |
| [Warrior](../classes/warrior.md) | Works |  |
| [Bard](../classes/bard.md) | Works |  |
| [Druid](../classes/druid.md) | Works |  |
| [Healer](../classes/healer.md) | Works |  |
| [Wizard](../classes/wizard.md) | Works |  |

## Connected abilities

**These abilities name Hold Person in their text** (auto-detected). If Hold Person is renamed, moved or removed, check them:

| Ability | How | On classes |
| --- | --- | --- |
| [Apex](apex.md) | removes | Scout |
| [Hunter](hunter.md) | changes its numbers | Scout |
| [Snaring Vines](snaring-vines.md) | grants or gives | Druid |

**Shared with:** [Assassin](../classes/assassin.md), [Scout](../classes/scout.md), [Healer](../classes/healer.md), [Wizard](../classes/wizard.md). Changing this ability changes it for every one of these classes unless the classes get separate versions.

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Assassin** lists it at 4th; nothing else is listed at that level.
- **Scout** lists it at 4th; 1 other entry shares that level: Pinning Arrow. It is one of a group (Pick one). Archetypes that name it: Hunter, Apex (archetypes are outside this model).
- **Healer** lists it at 2nd for 1 point. That level's table has 9 entries (12 points if each were bought once, including 1 Equipment trait and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README). **Experienced** (also on this list) only works on a single per-life or per-refresh Verbal of 4th level or lower. This Verbal is eligible now but would not be if moved above 4th.
- **Wizard** lists it at 3rd for 1 point. That level's table has 10 entries (10 points if each were bought once, including 0 Equipment traits and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README). **Experienced** (also on this list) only works on a single per-life or per-refresh Verbal of 4th level or lower. This Verbal is eligible now but would not be if moved above 4th.

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
