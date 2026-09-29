---
title: "Harden — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Harden
type: Enchantment
school: Protection
targets_other_players: true
classes: ["Warrior 1st", "Healer 1st"]
---

# Harden — Interoperability

[Rule text](../../rules/magic-and-abilities/harden.md) · **Enchantment** · Protection School · Range Other (He), Self (Wa)

## Summary

- **Can affect another player:** yes.
- **Works on:** 12 of 12 classes.
- **Blocked on:** no class.
- **On 2 class lists:** Warrior (1st), Healer (1st).

## What it does

Bearer's wielded weapons or shield (one or the other) can only be destroyed or damaged by object-destroying Magic Balls or Verbals.

| Effect | On | Details |
| --- | --- | --- |
| Protects equipment | bearer-equipment (benefit) | what weapons-or-shield; degree except-object-destroying-abilities; while worn; continuously while it is worn, chanted or in effect |

**Capabilities:** protects · **Roles:** defense, equipment

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/harden.md`](../../metadata/profiles/harden.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Warrior](../classes/warrior.md) | 1st | - | - | 1/Life | Self | no (ex) | Level table | - |
| [Healer](../classes/healer.md) | 1st | 1 | - | 1/Refresh | Other | yes | Spell table | - |

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

**Harden names these abilities in its own text** (auto-detected):

| Ability | How | On classes |
| --- | --- | --- |
| [Fireball](fireball.md) | mentions | Wizard |
| [Pyrotechnics](pyrotechnics.md) | mentions | Wizard |

**These abilities name Harden in their text** (auto-detected). If Harden is renamed, moved or removed, check them:

| Ability | How | On classes |
| --- | --- | --- |
| [Gift of Earth](gift-of-earth.md) | borrows its effect | Druid |
| [Greater Harden](greater-harden.md) | borrows its effect | Healer |
| [Juggernaut](juggernaut.md) | replaces | Warrior |
| [Sacred Blades](sacred-blades.md) | borrows its effect | Paladin |

**Shared with:** [Warrior](../classes/warrior.md), [Healer](../classes/healer.md). Changing this ability changes it for every one of these classes unless the classes get separate versions.

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Warrior** lists it at 1st; nothing else is listed at that level. Archetype that names it: Juggernaut (archetypes are outside this model).
- **Healer** lists it at 1st for 1 point. That level's table has 8 entries (12 points if each were bought once, including 2 Equipment traits and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README).

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
