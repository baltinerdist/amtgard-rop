---
title: "Ancestral Armor — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Ancestral Armor
type: Enchantment
school: Protection
targets_other_players: true
classes: ["Warrior 6th", "Healer 6th"]
---

# Ancestral Armor — Interoperability

[Rule text](../../rules/magic-and-abilities/ancestral-armor.md) · **Enchantment** · Protection School · Range Other (He), Self (Wa)

## Summary

- **Can affect another player:** yes.
- **Works on:** 12 of 12 classes.
- **Blocked on:** no class.
- **On 2 class lists:** Warrior (6th), Healer (6th).

## What it does

Ignores Magic Ball, projectile and melee hits on the bearer's armor while that location has points; the armor loses one point instead. Reusable.

| Effect | On | Details |
| --- | --- | --- |
| Ignores a hit | bearer (benefit) | from hits-on-worn-armor; except effects phasing; instant; when a weapon, arrow or ball strikes the subject or their armor; only if the struck armor still has points |
| Damages armor | bearer-equipment (harm) | points 1; instant; when a weapon, arrow or ball strikes the subject or their armor; only if the struck armor still has points |

**Capabilities:** has-drawback, protects · **Roles:** defense, equipment

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/ancestral-armor.md`](../../metadata/profiles/ancestral-armor.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Warrior](../classes/warrior.md) | 6th | - | - | 3/Refresh Charge x10 | Self | no (ex) | Level table | Swift |
| [Healer](../classes/healer.md) | 6th | 1 | - | 1/Refresh | Other | yes | Spell table | - |

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

**Ancestral Armor names these abilities in its own text** (auto-detected):

| Ability | How | On classes |
| --- | --- | --- |
| [Dispel Magic](dispel-magic.md) | mentions | Scout, Druid, Healer, Wizard |

**These abilities name Ancestral Armor in their text** (auto-detected). If Ancestral Armor is renamed, moved or removed, check them:

| Ability | How | On classes |
| --- | --- | --- |
| [Destroy Armor](destroy-armor.md) | mentions | Wizard |
| [Ironskin](ironskin.md) | borrows its effect | Druid |
| [Juggernaut](juggernaut.md) | removes | Warrior |
| [Marauder](marauder.md) | mentions | Warrior |
| [Stoneskin](stoneskin.md) | borrows its effect | Druid |

**Shared with:** [Warrior](../classes/warrior.md), [Healer](../classes/healer.md). Changing this ability changes it for every one of these classes unless the classes get separate versions.

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Warrior** lists it at 6th; nothing else is listed at that level. Archetypes that name it: Marauder, Juggernaut (archetypes are outside this model).
- **Healer** lists it at 6th for 1 point. That level's table has 9 entries (11 points if each were bought once, including 0 Equipment traits and 3 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README).

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
