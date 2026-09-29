---
title: "Brutal Strike — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Brutal Strike
type: Verbal
school: Death
targets_other_players: true
classes: ["Anti-Paladin 4th", "Barbarian 5th"]
---

# Brutal Strike — Interoperability

[Rule text](../../rules/magic-and-abilities/brutal-strike.md) · **Verbal** · Death School · Range Unlimited

## Summary

- **Can affect another player:** yes.
- **Works on:** 11 of 12 classes.
- **Blocked on:** Paladin.
- **On 2 class lists:** Anti-Paladin (4th), Barbarian (5th).

## What it does

Wound Trigger: the player just wounded (or killed) is Cursed indefinitely and Suppressed for 30 seconds; no verbal targeting.

| Effect | On | Details |
| --- | --- | --- |
| Curses | target (harm) | until respawn; after the caster wounds an enemy (Wound Trigger) |
| Suppresses | target (harm) | 30 s; after the caster wounds an enemy (Wound Trigger) |

**Capabilities:** castable-while-moving, curses, silences · **Roles:** debuff, control, anti-magic

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/brutal-strike.md`](../../metadata/profiles/brutal-strike.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Anti-Paladin](../classes/anti-paladin.md) | 4th | - | - | 1/Life Charge x10 | Unlimited | no (ex) | Level table | Ambulant |
| [Barbarian](../classes/barbarian.md) | 5th | - | - | 1/Life Charge x3 | Unlimited | no (ex) | Level table | Ambulant |

## Effect on each class

Assumes every class is 6th level. Results do not depend on level.

| Target class | Result | Why |
| --- | --- | --- |
| [Anti-Paladin](../classes/anti-paladin.md) | Works |  |
| [Archer](../classes/archer.md) | Works |  |
| [Assassin](../classes/assassin.md) | Works |  |
| [Barbarian](../classes/barbarian.md) | Works |  |
| [Monk](../classes/monk.md) | Works |  |
| [Paladin](../classes/paladin.md) | **Blocked** | Immune to Death |
| [Scout](../classes/scout.md) | Works |  |
| [Warrior](../classes/warrior.md) | Works |  |
| [Bard](../classes/bard.md) | Works |  |
| [Druid](../classes/druid.md) | Works |  |
| [Healer](../classes/healer.md) | Works |  |
| [Wizard](../classes/wizard.md) | Works |  |

## Connected abilities

**These abilities name Brutal Strike in their text** (auto-detected). If Brutal Strike is renamed, moved or removed, check them:

| Ability | How | On classes |
| --- | --- | --- |
| [Raider](raider.md) | grants or gives | Barbarian |

**Shared with:** [Anti-Paladin](../classes/anti-paladin.md), [Barbarian](../classes/barbarian.md). Changing this ability changes it for every one of these classes unless the classes get separate versions.

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Anti-Paladin** lists it at 4th; nothing else is listed at that level.
- **Barbarian** lists it at 5th; nothing else is listed at that level. Archetype that names it: Raider (archetypes are outside this model).

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
