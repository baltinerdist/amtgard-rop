---
title: "Pyrotechnics — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Pyrotechnics
type: Verbal
school: Flame
targets_other_players: true
classes: ["Wizard 5th"]
---

# Pyrotechnics — Interoperability

[Rule text](../../rules/magic-and-abilities/pyrotechnics.md) · **Verbal** · Flame School · Range 50'

## Summary

- **Can affect another player:** yes.
- **Works on:** 12 of 12 classes.
- **Blocked on:** no class.
- **On 1 class list:** Wizard (5th).

## What it does

Destroys all weapons and shields carried by a target within 50' when the Verbal completes; only equipment-specific protections stop it.

| Effect | On | Details |
| --- | --- | --- |
| Destroys equipment | target (harm) | what weapons-and-shields; instant |

**Capabilities:** attacks-equipment · **Roles:** equipment

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/pyrotechnics.md`](../../metadata/profiles/pyrotechnics.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Wizard](../classes/wizard.md) | 5th | 1 | 2 | 1/Refresh | 50' | yes | Spell table | - |

## Effect on each class

Assumes every class is 6th level. Results do not depend on level.

| Target class | Result | Why |
| --- | --- | --- |
| [Anti-Paladin](../classes/anti-paladin.md) | Works | Affects the player's equipment, which immunities and Enlightened Soul do not protect |
| [Archer](../classes/archer.md) | Works |  |
| [Assassin](../classes/assassin.md) | Works |  |
| [Barbarian](../classes/barbarian.md) | Works |  |
| [Monk](../classes/monk.md) | Works | Affects the player's equipment, which immunities and Enlightened Soul do not protect |
| [Paladin](../classes/paladin.md) | Works |  |
| [Scout](../classes/scout.md) | Works |  |
| [Warrior](../classes/warrior.md) | Works |  |
| [Bard](../classes/bard.md) | Works |  |
| [Druid](../classes/druid.md) | Works |  |
| [Healer](../classes/healer.md) | Works |  |
| [Wizard](../classes/wizard.md) | Works |  |

## Connected abilities

**Pyrotechnics names these abilities in its own text** (auto-detected):

| Ability | How | On classes |
| --- | --- | --- |
| [Adaptive Protection](adaptive-protection.md) | mentions | Scout, Healer |
| [Blessed Aura](blessed-aura.md) | mentions | Healer |
| [Enlightened Soul](enlightened-soul.md) | mentions | Monk, Healer |
| [Flame Blade](flame-blade.md) | mentions | Anti-Paladin, Druid |
| [Protection from Magic](protection-from-magic.md) | mentions | Paladin, Healer, Wizard |

**These abilities name Pyrotechnics in their text** (auto-detected). If Pyrotechnics is renamed, moved or removed, check them:

| Ability | How | On classes |
| --- | --- | --- |
| [Harden](harden.md) | mentions | Warrior, Healer |

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Wizard** lists it at 5th for 1 point. That level's table has 8 entries (11 points if each were bought once, including 1 Equipment trait and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README). **Experienced** (also on this list) only works on a single per-life or per-refresh Verbal of 4th level or lower. This Verbal is already too high for it.

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
