---
title: "Break Concentration — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Break Concentration
type: Verbal
school: Command
targets_other_players: true
classes: ["Bard 3rd", "Wizard 2nd"]
---

# Break Concentration — Interoperability

[Rule text](../../rules/magic-and-abilities/break-concentration.md) · **Verbal** · Command School · Range 20'

## Summary

- **Can affect another player:** yes.
- **Works on:** 8 of 12 classes.
- **Blocked on:** Anti-Paladin, Barbarian, Monk, Paladin.
- **On 2 class lists:** Bard (3rd), Wizard (2nd).

## What it does

A target within 20' is Suppressed for 10 seconds.

| Effect | On | Details |
| --- | --- | --- |
| Suppresses | target (harm) | 10 s |

**Capabilities:** silences · **Roles:** control, anti-magic

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/break-concentration.md`](../../metadata/profiles/break-concentration.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Bard](../classes/bard.md) | 3rd | 1 | 4 | 1/Life | 20' | yes | Spell table | - |
| [Wizard](../classes/wizard.md) | 2nd | 1 | - | 1/Life | 20' | yes | Spell table | - |

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

**These abilities name Break Concentration in their text** (auto-detected). If Break Concentration is renamed, moved or removed, check them:

| Ability | How | On classes |
| --- | --- | --- |
| [Discordia](discordia.md) | grants or gives | Bard |

**Shared with:** [Bard](../classes/bard.md), [Wizard](../classes/wizard.md). Changing this ability changes it for every one of these classes unless the classes get separate versions.

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Bard** lists it at 3rd for 1 point. That level's table has 6 entries (7 points if each were bought once, including 1 Equipment trait and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README). **Experienced** (also on this list) only works on a single per-life or per-refresh Verbal of 4th level or lower. This Verbal is eligible now but would not be if moved above 4th.
- **Wizard** lists it at 2nd for 1 point. That level's table has 8 entries (8 points if each were bought once, including 0 Equipment traits and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README). **Experienced** (also on this list) only works on a single per-life or per-refresh Verbal of 4th level or lower. This Verbal is eligible now but would not be if moved above 4th.

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
