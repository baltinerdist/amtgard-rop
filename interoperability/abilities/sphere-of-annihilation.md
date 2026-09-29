---
title: "Sphere of Annihilation — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Sphere of Annihilation
type: Magic Ball
school: Sorcery
targets_other_players: true
classes: ["Wizard 6th"]
---

# Sphere of Annihilation — Interoperability

[Rule text](../../rules/magic-and-abilities/sphere-of-annihilation.md) · **Magic Ball** · Sorcery School

## Summary

- **Can affect another player:** yes.
- **Works on:** 12 of 12 classes.
- **Blocked on:** no class.
- **On 1 class list:** Wizard (6th).

## What it does

Magic Ball ignoring armor and Enchantments: the player hit dies and is Cursed; Weapon and Shield Destroying.

| Effect | On | Details |
| --- | --- | --- |
| Weapon Destroying (this magic ball) | struck-player (harm) | on this-magic-ball; instant; when a weapon, arrow or ball strikes the subject or their armor |
| Shield Destroying (this magic ball) | struck-player (harm) | on this-magic-ball; instant; when a weapon, arrow or ball strikes the subject or their armor |
| Causes death | struck-player (harm) | instant; when a weapon, arrow or ball strikes the subject or their armor |
| Curses | struck-player (harm) | until respawn; when a weapon, arrow or ball strikes the subject or their armor |

**Capabilities:** attacks-equipment, can-be-lethal, causes-death, curses, defeats-armor · **Roles:** offense, equipment, debuff

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/sphere-of-annihilation.md`](../../metadata/profiles/sphere-of-annihilation.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Wizard](../classes/wizard.md) | 6th | 2 | 1 | 1 Ball / Unlimited | - | yes | Spell table | - |

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

Monks can block Magic Balls and arrows with Missile Block, but that needs an active block, so it is shown as working.

## Connected abilities

**Sphere of Annihilation names these abilities in its own text** (auto-detected):

| Ability | How | On classes |
| --- | --- | --- |
| [Phoenix Tears](phoenix-tears.md) | mentions | Healer |

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Wizard** lists it at 6th for 2 points. That level's table has 9 entries (14 points if each were bought once, including 0 Equipment traits and 3 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README).

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
