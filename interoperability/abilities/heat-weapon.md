---
title: "Heat Weapon — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Heat Weapon
type: Verbal
school: Flame
targets_other_players: true
classes: ["Druid 1st", "Wizard 1st"]
---

# Heat Weapon — Interoperability

[Rule text](../../rules/magic-and-abilities/heat-weapon.md) · **Verbal** · Flame School · Range 20'

## Summary

- **Can affect another player:** yes.
- **Works on:** 11 of 12 classes.
- **Blocked on:** Anti-Paladin.
- **On 2 class lists:** Druid (1st), Wizard (1st).

## What it does

A targeted weapon within 20' cannot be wielded for 30 seconds, except by players Immune to Flame.

| Effect | On | Details |
| --- | --- | --- |
| Disables equipment | target-equipment (harm) | what weapon; 30 s |

**Capabilities:** attacks-equipment · **Roles:** equipment, control

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/heat-weapon.md`](../../metadata/profiles/heat-weapon.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Druid](../classes/druid.md) | 1st | 1 | - | 1/Life Charge x3 | 20' | yes | Spell table | - |
| [Wizard](../classes/wizard.md) | 1st | 1 | - | 1/Life | 20' | yes | Spell table | - |

## Effect on each class

Assumes every class is 6th level. Results do not depend on level.

| Target class | Result | Why |
| --- | --- | --- |
| [Anti-Paladin](../classes/anti-paladin.md) | **Blocked** | Immune to Flame. Its target is the weapon, but a Flame-Immune player may keep wielding it, so it has no effect on them |
| [Archer](../classes/archer.md) | Works |  |
| [Assassin](../classes/assassin.md) | Works |  |
| [Barbarian](../classes/barbarian.md) | Works |  |
| [Monk](../classes/monk.md) | Works | The weapon, not the person, is the target, so Enlightened Soul does not protect it |
| [Paladin](../classes/paladin.md) | Works |  |
| [Scout](../classes/scout.md) | Works |  |
| [Warrior](../classes/warrior.md) | Works |  |
| [Bard](../classes/bard.md) | Works |  |
| [Druid](../classes/druid.md) | Works |  |
| [Healer](../classes/healer.md) | Works |  |
| [Wizard](../classes/wizard.md) | Works |  |

## Connected abilities

**These abilities name Heat Weapon in their text** (auto-detected). If Heat Weapon is renamed, moved or removed, check them:

| Ability | How | On classes |
| --- | --- | --- |
| [Gift of Fire](gift-of-fire.md) | grants or gives | Druid |

**Shared with:** [Druid](../classes/druid.md), [Wizard](../classes/wizard.md). Changing this ability changes it for every one of these classes unless the classes get separate versions.

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Druid** lists it at 1st for 1 point. That level's table has 7 entries (9 points if each were bought once, including 1 Equipment trait and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README). **Experienced** (also on this list) only works on a single per-life or per-refresh Verbal of 4th level or lower. This Verbal is eligible now but would not be if moved above 4th.
- **Wizard** lists it at 1st for 1 point. That level's table has 8 entries (10 points if each were bought once, including 1 Equipment trait and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README). **Experienced** (also on this list) only works on a single per-life or per-refresh Verbal of 4th level or lower. This Verbal is eligible now but would not be if moved above 4th.

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
