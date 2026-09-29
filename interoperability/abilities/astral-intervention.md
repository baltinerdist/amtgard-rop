---
title: "Astral Intervention — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Astral Intervention
type: Verbal
school: Command
targets_other_players: true
classes: ["Healer 3rd", "Wizard 2nd"]
---

# Astral Intervention — Interoperability

[Rule text](../../rules/magic-and-abilities/astral-intervention.md) · **Verbal** · Command School · Range 20'

## Summary

- **Can affect another player:** yes.
- **Works on:** 8 of 12 classes.
- **Blocked on:** Anti-Paladin, Barbarian, Monk, Paladin.
- **On 2 class lists:** Healer (3rd), Wizard (2nd).

## What it does

A player within 20' (or the caster) becomes Insubstantial for 30 seconds; if self-cast, the caster may exit at any time.

| Effect | On | Details |
| --- | --- | --- |
| Makes Insubstantial | target (depends) | 30 s; only if the ability is cast on another player |
| Makes Insubstantial | caster (benefit) | 30 s; only if the ability is cast on the caster |

**Capabilities:** makes-insubstantial, neutralizes, removes-from-play, self-protection-state · **Roles:** control, defense

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/astral-intervention.md`](../../metadata/profiles/astral-intervention.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Healer](../classes/healer.md) | 3rd | 1 | - | 1/Life Charge x3 | 20' | yes | Spell table | - |
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

**Shared with:** [Healer](../classes/healer.md), [Wizard](../classes/wizard.md). Changing this ability changes it for every one of these classes unless the classes get separate versions.

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Healer** lists it at 3rd for 1 point. That level's table has 9 entries (10 points if each were bought once, including 1 Equipment trait and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README). **Experienced** (also on this list) only works on a single per-life or per-refresh Verbal of 4th level or lower. This Verbal is eligible now but would not be if moved above 4th.
- **Wizard** lists it at 2nd for 1 point. That level's table has 8 entries (8 points if each were bought once, including 0 Equipment traits and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README). **Experienced** (also on this list) only works on a single per-life or per-refresh Verbal of 4th level or lower. This Verbal is eligible now but would not be if moved above 4th.

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
