---
title: "Steal Life Essence — Interoperability"
section: Interoperability
rulebook_version: V8.08 "Spongy"
rulebook_date: 2026-07-25
source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)
ability: Steal Life Essence
type: Verbal
school: Death
targets_other_players: true
classes: ["Anti-Paladin 3rd", "Healer 5th", "Wizard 5th"]
---

# Steal Life Essence — Interoperability

[Rule text](../../rules/magic-and-abilities/steal-life-essence.md) · **Verbal** · Death School · Range Touch

## Summary

- **Can affect another player:** yes.
- **Works on:** 11 of 12 classes.
- **Blocked on:** Paladin.
- **On 3 class lists:** Anti-Paladin (3rd), Healer (5th), Wizard (5th).

## What it does

Curses a dead, non-Cursed player by Touch; the caster may then heal one wound or instantly Charge an ability.

| Effect | On | Details |
| --- | --- | --- |
| Curses | dead-target (harm) | until respawn |
| Heals wounds | caster (benefit) | amount one; instant; choice g1 option 1 |
| Instantly Charges an ability | caster (benefit) | instant; choice g1 option 2 |

**Capabilities:** curses, heals, more-uses · **Roles:** debuff, healing, resource

Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): [`metadata/profiles/steal-life-essence.md`](../../metadata/profiles/steal-life-essence.md).

## Where it is listed

| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Anti-Paladin](../classes/anti-paladin.md) | 3rd | - | - | 1/Life Charge x5 | Touch | yes | Level table | - |
| [Healer](../classes/healer.md) | 5th | 1 | 2 | 1/Life | Touch | yes | Spell table | - |
| [Wizard](../classes/wizard.md) | 5th | 1 | 2 | 1/Life | Touch | yes | Spell table | - |

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

Touch and Other range also need the target to be willing, dead, stunned, frozen or Insubstantial and unable to move. That applies to every class alike and is not modelled.

## Connected abilities

**These abilities name Steal Life Essence in their text** (auto-detected). If Steal Life Essence is renamed, moved or removed, check them:

| Ability | How | On classes |
| --- | --- | --- |
| [Infernal](infernal.md) | removes | Anti-Paladin |
| [Void Touched](void-touched.md) | grants or gives | Wizard |

**Shared with:** [Anti-Paladin](../classes/anti-paladin.md), [Healer](../classes/healer.md), [Wizard](../classes/wizard.md). Changing this ability changes it for every one of these classes unless the classes get separate versions.

## If you change its level

- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.
- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).

- **Anti-Paladin** lists it at 3rd; nothing else is listed at that level. Archetype that names it: Infernal (archetypes are outside this model).
- **Healer** lists it at 5th for 1 point. That level's table has 7 entries (8 points if each were bought once, including 0 Equipment traits and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README). **Experienced** (also on this list) only works on a single per-life or per-refresh Verbal of 4th level or lower. This Verbal is already too high for it.
- **Wizard** lists it at 5th for 1 point. That level's table has 8 entries (11 points if each were bought once, including 1 Equipment trait and 0 Archetypes). A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README). **Experienced** (also on this list) only works on a single per-life or per-refresh Verbal of 4th level or lower. This Verbal is already too high for it.

---
*Derived from the V8.08 "Spongy" rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*
