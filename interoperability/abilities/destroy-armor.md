---
title: "Destroy Armor — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Destroy Armor
type: Verbal
school: Death
targets_other_players: true
classes: ["Wizard 4th"]
---

# Destroy Armor — Interoperability

[Rule text](../../rules/magic-and-abilities/destroy-armor.md) · **Verbal** · Death School · Range 20'

## Summary

- **Can affect another player:** yes.
- **Works on:** 12 of 12 classes.
- **Blocked on:** no class.
- **On 1 class list:** Wizard (4th).

## What it does

Removes all armor points from a named hit location on a target within 20'; only armor-specific protections like Blessed Aura stop it.

| Effect | On | Details |
| --- | --- | --- |
| Destroys armor | hit-location (harm) | scope one-location; instant |

**Capabilities:** defeats-armor · **Roles:** equipment, debuff

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/destroy-armor.md`](../../metadata/profiles/destroy-armor.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Wizard](../classes/wizard.md) | 4th | 1 | - | 2/Refresh | 20' | yes | Spell table | - |

## Effect on each class

Assumes every class is 6th level. Results do not depend on level.

| Target class | Result | Why |
| --- | --- | --- |
| [Anti-Paladin](../classes/anti-paladin.md) | Works |  |
| [Archer](../classes/archer.md) | Works |  |
| [Assassin](../classes/assassin.md) | Works |  |
| [Barbarian](../classes/barbarian.md) | Works |  |
| [Monk](../classes/monk.md) | Works | Affects the hit location's armor, which immunities and Enlightened Soul do not protect |
| [Paladin](../classes/paladin.md) | Works | Affects the hit location's armor, which immunities and Enlightened Soul do not protect |
| [Scout](../classes/scout.md) | Works |  |
| [Warrior](../classes/warrior.md) | Works |  |
| [Bard](../classes/bard.md) | Works |  |
| [Druid](../classes/druid.md) | Works |  |
| [Healer](../classes/healer.md) | Works |  |
| [Wizard](../classes/wizard.md) | Works |  |

## Connected abilities

**Destroy Armor names these abilities in its own text** (auto-detected):

| Ability | How | On classes |
| --- | --- | --- |
| [Adaptive Protection](adaptive-protection.md) | mentions | Scout, Healer |
| [Ancestral Armor](ancestral-armor.md) | mentions | Warrior, Healer |
| [Blessed Aura](blessed-aura.md) | mentions | Healer |
| [Enlightened Soul](enlightened-soul.md) | mentions | Monk, Healer |
| [Protection from Magic](protection-from-magic.md) | mentions | Paladin, Healer, Wizard |

**These abilities name Destroy Armor in their text** (auto-detected). If Destroy Armor is renamed, moved or removed, check them:

| Ability | How | On classes |
| --- | --- | --- |
| [Corrosive Mist](corrosive-mist.md) | grants or gives | Druid |

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Wizard** lists it at 4th for 1 point. That level's table has 9 entries (9 points if each were bought once, including 0 Equipment traits and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README). **Experienced** (also on this list) only works on a single per-life or per-refresh Verbal of 4th level or lower. This Verbal is eligible now but would not be if moved above 4th.

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
