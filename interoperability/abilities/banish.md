---
title: "Banish — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Banish
type: Verbal
school: Spirit
targets_other_players: true
classes: ["Monk 2nd", "Healer 1st", "Wizard 1st"]
---

# Banish — Interoperability

[Rule text](../../rules/magic-and-abilities/banish.md) · **Verbal** · Spirit School · Range 20'

## Summary

- **Can affect another player:** yes.
- **Works on:** 11 of 12 classes.
- **Blocked on:** Monk.
- **On 3 class lists:** Monk (2nd), Healer (1st), Wizard (1st).

## What it does

An Insubstantial player within 20' must return to base, their Insubstantial State replaced by Banish's, ending it on arrival.

| Effect | On | Details |
| --- | --- | --- |
| Sends to base | target (harm) | until arrival; only if the ability is cast on another player |
| Sends to base | caster (benefit) | until arrival; only if the ability is cast on the caster |

**Capabilities:** moves-others, moves-self · **Roles:** control, mobility

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/banish.md`](../../metadata/profiles/banish.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Monk](../classes/monk.md) | 2nd | - | - | 1/Life Charge x5 | 20' | yes | Level table | - |
| [Healer](../classes/healer.md) | 1st | 1 | - | 1/Life | 20' | yes | Spell table | - |
| [Wizard](../classes/wizard.md) | 1st | 1 | - | 1/Life | 20' | yes | Spell table | - |

## Effect on each class

Assumes every class is 6th level. Results do not depend on level.

| Target class | Result | Why |
| --- | --- | --- |
| [Anti-Paladin](../classes/anti-paladin.md) | Works |  |
| [Archer](../classes/archer.md) | Works |  |
| [Assassin](../classes/assassin.md) | Works |  |
| [Barbarian](../classes/barbarian.md) | Works |  |
| [Monk](../classes/monk.md) | **Blocked** | Enlightened Soul: unaffected by Verbal Magical abilities used beyond Touch (still works if cast at Touch) |
| [Paladin](../classes/paladin.md) | Works |  |
| [Scout](../classes/scout.md) | Works |  |
| [Warrior](../classes/warrior.md) | Works |  |
| [Bard](../classes/bard.md) | Works |  |
| [Druid](../classes/druid.md) | Works |  |
| [Healer](../classes/healer.md) | Works |  |
| [Wizard](../classes/wizard.md) | Works |  |

## Connected abilities

**These abilities name Banish in their text** (auto-detected). If Banish is renamed, moved or removed, check them:

| Ability | How | On classes |
| --- | --- | --- |
| [Circle of Protection](circle-of-protection.md) | mentions | Healer |

**Shared with:** [Monk](../classes/monk.md), [Healer](../classes/healer.md), [Wizard](../classes/wizard.md). Changing this ability changes it for every one of these classes unless the classes get separate versions.

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Monk** lists it at 2nd; nothing else is listed at that level.
- **Healer** lists it at 1st for 1 point. That level's table has 8 entries (12 points if each were bought once, including 2 Equipment traits and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README). **Experienced** (also on this list) only works on a single per-life or per-refresh Verbal of 4th level or lower. This Verbal is eligible now but would not be if moved above 4th.
- **Wizard** lists it at 1st for 1 point. That level's table has 8 entries (10 points if each were bought once, including 1 Equipment trait and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README). **Experienced** (also on this list) only works on a single per-life or per-refresh Verbal of 4th level or lower. This Verbal is eligible now but would not be if moved above 4th.

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
