---
title: "Greater Harden — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Greater Harden
type: Enchantment
school: Protection
targets_other_players: true
classes: ["Healer 3rd"]
---

# Greater Harden — Interoperability

[Rule text](../../rules/magic-and-abilities/greater-harden.md) · **Enchantment** · Protection School · Range Self (Wa) Other (He)

## Summary

- **Can affect another player:** yes.
- **Works on:** 12 of 12 classes.
- **Blocked on:** no class.
- **On 1 class list:** Healer (3rd).

## What it does

Shields and weapons wielded by the bearer are affected as per Harden (both, not one or the other).

| Effect | On | Details |
| --- | --- | --- |
| Works as Harden | bearer-equipment (benefit) | how as-per; while worn; continuously while it is worn, chanted or in effect |
| Protects equipment | bearer-equipment (benefit) | what weapons-and-shields; degree except-object-destroying-abilities; while worn; continuously while it is worn, chanted or in effect |

**Capabilities:** grants-abilities, protects · **Roles:** defense, equipment

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/greater-harden.md`](../../metadata/profiles/greater-harden.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Healer](../classes/healer.md) | 3rd | 1 | - | 1/Refresh | Other | yes | Spell table | - |

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

**Greater Harden names these abilities in its own text** (auto-detected):

| Ability | How | On classes |
| --- | --- | --- |
| [Harden](harden.md) | borrows its effect | Warrior, Healer |

**These abilities name Greater Harden in their text** (auto-detected). If Greater Harden is renamed, moved or removed, check them:

| Ability | How | On classes |
| --- | --- | --- |
| [Juggernaut](juggernaut.md) | grants or gives | Warrior |

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Healer** lists it at 3rd for 1 point. That level's table has 9 entries (10 points if each were bought once, including 1 Equipment trait and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README).

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
